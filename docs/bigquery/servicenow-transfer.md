Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [參考資料](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 將 ServiceNow 資料載入 BigQuery

您可以使用 ServiceNow 連接器的 [BigQuery 資料移轉服務](https://docs.cloud.google.com/bigquery/docs/dts-introduction?hl=zh-tw)，將資料從 ServiceNow 載入 BigQuery。您可以使用 BigQuery 資料移轉服務，安排週期性移轉工作，將 ServiceNow 的最新資料新增至 BigQuery。

## 限制

ServiceNow 資料移轉作業會受到下列限制：

* ServiceNow 連接器僅支援 [ServiceNow 資料表 API](https://www.servicenow.com/docs/bundle/zurich-api-reference/page/integrate/inbound-rest/concept/c_TableAPI.html)。
* 我們不建議在同一個 ServiceNow 執行個體上同時執行資料轉移作業。這可能會導致 ServiceNow 執行個體負載過重，進而造成延遲或失敗。
  + 建議您錯開轉移作業的開始時間，避免轉移作業重疊。
* 為提升資料移轉效能，建議每次移轉的資產數量不要超過 20 個。
* 週期性資料轉移作業之間的最短時間間隔為 15 分鐘。
  預設的週期性轉移間隔為 24 小時。
* 單一移轉設定在特定時間只能支援一次資料移轉作業。如果排定在第一次資料移轉完成前執行第二次資料移轉，則系統只會完成第一次資料移轉，並略過任何與第一次移轉重疊的資料移轉。
  + 為避免在單一轉移設定中略過轉移作業，建議您設定「重複頻率」，增加大型資料轉移作業之間的時間間隔。
* 如要透過網路連結進行資料移轉，請務必先[定義靜態 IP 位址，再建立網路連結](https://docs.cloud.google.com/bigquery/docs/connections-with-network-attachment?hl=zh-tw)。

### 增量移轉限制

ServiceNow 增量移轉作業有下列限制：

* 浮水印欄只能選擇 `DATETIME` 欄。
* 只有含有有效浮水印欄的資產，才支援增量擷取。
* 浮水印資料欄中的值必須單調遞增。
* 增量轉移作業無法同步處理來源資料表中的刪除作業。
* 單一轉移設定只能支援增量或完整擷取。
* 第一次執行增量擷取後，就無法更新 `asset` 清單中的物件。
* 首次執行增量擷取後，就無法在轉移設定中變更寫入模式。
* 第一次執行遞增式擷取後，就無法變更時間戳記欄或主鍵。
* 目的地 BigQuery 資料表會使用提供的主鍵叢集，並受[分群資料表限制](https://docs.cloud.google.com/bigquery/docs/clustered-tables?hl=zh-tw#limitations)約束。
* 首次將現有轉移設定更新為增量擷取模式時，更新後的第一次資料移轉作業會移轉資料來源中的所有可用資料。後續的增量資料轉移作業只會轉移資料來源中的新資料列和更新資料列。

## 資料擷取選項

這些章節說明設定 ServiceNow 資料移轉作業時，可用的資料擷取選項。

### 完整或累加轉移

[設定 ServiceNow 轉移作業](#servicenow_transfer_setup)時，請在轉移設定中選取「完整」或「增量」寫入偏好設定，指定資料載入 BigQuery 的方式。
[預先發布版](https://cloud.google.com/products?hl=zh-tw#product-launch-stages)支援增量轉移。

**注意：** 如要提供意見或取得增量資料移轉支援，請傳送電子郵件至 [dts-preview-support@google.com](mailto:dts-preview-support@google.com)。
您可以設定*完整*資料移轉，在每次資料移轉時，移轉 ServiceNow 資料集的所有資料。

或者，您也可以設定*增量*資料移轉作業 ([搶先版](https://cloud.google.com/products?hl=zh-tw#product-launch-stages))，只移轉上次資料移轉後變更的資料，而不是在每次資料移轉時載入整個資料集。如果為資料移轉作業選取「增量」**Incremental**，則必須指定「附加」**Append**或「插入或更新」**Upsert**寫入模式，定義在增量資料移轉期間，資料如何寫入 BigQuery。以下各節說明可用的寫入模式。

#### Upsert 寫入模式

新增或更新寫入模式會檢查主鍵，以更新資料列或在目的地資料表中插入新的資料列。您可以指定主鍵，讓 ServiceNow 連接器判斷需要哪些變更，才能讓目的地資料表與來源資料表保持同步。如果在資料移轉期間，指定的主鍵出現在目標 BigQuery 資料表中，ServiceNow 連接器就會使用來源資料表中的新資料更新該資料列。如果資料移轉期間沒有主鍵，ServiceNow 連接器就會插入新列。

選取「新增或更新」模式時，必須選取浮水印欄和主鍵：

* ServiceNow 連接器必須使用浮水印資料欄，才能追蹤來源資料表中的變更。

  選取每次修改資料列時都會更新的水印資料欄。建議使用與 `UPDATED_AT` 或 `LAST_MODIFIED` 資料欄類似的資料欄。

* 主鍵可以是資料表上的一或多個資料欄，ServiceNow 連接器必須使用這些資料欄，判斷是否需要插入或更新資料列。

  選取包含非空值的資料欄，這些值在資料表的所有資料列中都是不重複的。建議您使用包含系統產生 ID、專屬參照代碼 (例如自動遞增 ID) 或不可變動的時間序列 ID 的資料欄。

  為避免資料遺失或損毀，您選取的主鍵資料欄必須具有不重複的值。如果您對所選主鍵欄位的唯一性有疑慮，建議改用完整擷取。

### 增量擷取行為

在資料來源中變更資料表結構定義時，這些資料表的增量資料移轉作業會以以下方式反映在 BigQuery 中：

| 資料來源異動 | 增量擷取行為 |
| --- | --- |
| 新增資料欄 | 目的地 BigQuery 資料表會新增資料欄。 這個資料欄的所有先前記錄都會有空值。 |
| 刪除資料欄 | 刪除的資料欄仍會保留在目的地 BigQuery 資料表中。系統會在新項目中填入空值。 |
| 變更資料欄中的資料類型 | 連接器僅支援 `ALTER COLUMN` DDL 陳述式支援的資料類型轉換。如果轉換成其他資料類型，資料移轉作業就會失敗。 如果遇到任何問題，建議建立新的轉移設定。 |
| 重新命名資料欄 | 原始資料欄會保留在目的地 BigQuery 資料表中，而目的地資料表會新增一個名稱更新的資料欄。 |

## 事前準備

建立 ServiceNow 資料移轉作業前，請先為 ServiceNow 和 BigQuery 執行下列操作。

### ServiceNow 必備條件

* 如要存取 ServiceNow API，請建立 [OAuth 憑證](https://www.servicenow.com/docs/csh?topicname=t_CreateEndpointforExternalClients.html&version=latest)。
* 您必須在 ServiceNow 執行個體中啟用下列所有 ServiceNow 應用程式：

  + [取得](https://docs.servicenow.com/csh?topicname=t_ActivateProcurement.html&version=latest)
  + [產品目錄](https://docs.servicenow.com/csh?topicname=c_ProductCatalog.html&version=latest)
  + [合約管理](https://docs.servicenow.com/csh?topicname=c_ContractManagement.html&version=latest)
* 如要開始轉移 ServiceNow，您必須具備正確的憑證，才能連線至 ServiceNow 執行個體。

  + 如要取得 ServiceNow 開發人員執行個體的憑證，請登入 [ServiceNow 開發人員入口網站](https://developer.servicenow.com/dev.do)。你可以使用「管理執行個體密碼」頁面中列出的使用者名稱和密碼。如要瞭解如何重設 ServiceNow 密碼，請參閱「[Password Reset](https://www.servicenow.com/docs/csh?topicname=password-reset-landing-page.html&version=latest)」(密碼重設)
  + 如要取得 ServiceNow 實際工作環境或子實際工作環境執行個體的憑證，請與 ServiceNow 客戶管理員聯絡，要求提供使用者名稱和密碼。

### BigQuery 必要條件

* 完成[啟用 BigQuery 資料移轉服務](https://docs.cloud.google.com/bigquery/docs/enable-transfer-service?hl=zh-tw)的一切必要動作。
* [建立 BigQuery 資料集](https://docs.cloud.google.com/bigquery/docs/datasets?hl=zh-tw)來儲存資料。
* 如要為 Pub/Sub 設定移轉作業執行通知，請確認您擁有 `pubsub.topics.setIamPolicy` 身分與存取權管理 (IAM) 權限。如果您只設定電子郵件通知，則不需要 Pub/Sub 權限。詳情請參閱 [BigQuery 資料移轉服務執行通知](https://docs.cloud.google.com/bigquery/docs/transfer-run-notifications?hl=zh-tw)。

### 必要的 BigQuery 角色

如要取得建立 BigQuery 資料移轉服務資料移轉作業所需的權限，請要求系統管理員在專案中授予您 [BigQuery 管理員](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.admin)  (`roles/bigquery.admin`) IAM 角色。如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

這個預先定義的角色具備建立 BigQuery 資料移轉服務資料移轉作業所需的權限。如要查看確切的必要權限，請展開「Required permissions」(必要權限) 部分：

#### 所需權限

如要建立 BigQuery 資料移轉服務資料移轉作業，您必須具備下列權限：

* BigQuery 資料移轉服務權限：
  + `bigquery.transfers.update`
  + `bigquery.transfers.get`
* BigQuery 權限：
  + `bigquery.datasets.get`
  + `bigquery.datasets.getIamPolicy`
  + `bigquery.datasets.update`
  + `bigquery.datasets.setIamPolicy`
  + `bigquery.jobs.create`

您或許還可透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)取得這些權限。

詳情請參閱「[授予 `bigquery.admin` 存取權](https://docs.cloud.google.com/bigquery/docs/enable-transfer-service?hl=zh-tw#grant_bigqueryadmin_access)」。

## 設定 ServiceNow 資料移轉作業

如要將 ServiceNow 資料新增至 BigQuery，請使用下列任一方法設定移轉設定：

### 控制台

1. 前往 Google Cloud 控制台的「資料移轉」頁面。

   [前往「資料轉移」頁面](https://console.cloud.google.com/bigquery/transfers?hl=zh-tw)
2. 按一下 add「建立轉移作業」。
3. 在「Source type」(來源類型) 部分，「Source」(來源) 請選取「ServiceNow」。
4. 在「Data source details」(資料來源詳細資料) 部分執行下列操作：

   * (選用) 在「Network attachment」(網路連結) 部分，從下拉式選單中選取網路連結，或是點選「Create Network Attachment」(建立網路連結)。
     + 選取網路連結，將這項資料移轉作業設定為使用單一且一致的 IP 位址。如果 ServiceNow 執行個體設為只接受來自特定 IP 位址的流量，可以使用這個選項。
     + 如要進一步瞭解如何建立網路連結，請參閱「[使用網路連結設定連線](https://docs.cloud.google.com/bigquery/docs/connections-with-network-attachment?hl=zh-tw)」
     + 如要進一步瞭解如何在 ServiceNow 定義 IP 位址，請參閱「[定義允許的 ServiceNow 內部 IP 位址](https://www.servicenow.com/docs/csh?topicname=sc-ip-addresses-access-allowlist.html&version=latest)」
   * 在「Instance ID」(執行個體 ID) 輸入 ServiceNow 執行個體 ID。您可以從 ServiceNow 網址取得這組 ID，例如 `https://INSTANCE_ID.service-now.com`。
   * (選用) 在「ServiceNow Cloud Type」(ServiceNow 雲端類型) 部分，選取 ServiceNow 帳戶的雲端類型：
     + 如果 ServiceNow 執行個體網址符合 `https://INSTANCE_ID.service-now.com` 模式，請選取「Commercial」(商業用途)。這是預設值。
     + 如果 ServiceNow 執行個體網址符合 `https://INSTANCE_ID.servicenowservices.com` 模式，請選取「Government Community Cloud (GCC)」(政府機構社群雲端 (GCC))。
   * 在「Username」(使用者名稱) 輸入要用於連線的 ServiceNow 使用者名稱。
   * 在「Password」(密碼) 輸入 ServiceNow 密碼。
   * 在「Client ID」(用戶端 ID) 輸入 OAuth 憑證中的用戶端 ID。如要產生憑證，請參閱[建立 OAuth 憑證](https://docs.oracle.com/cd/B13789_01/server.101/b10759/statements_9013.htm)的相關說明。
   * 在「Client secret」(用戶端密鑰) 輸入 OAuth 憑證中的用戶端密鑰。
   * 在「Enable legacy mapping」(啟用舊版對應) 部分，選取「true」(預設)，即可使用[舊版資料類型對應](https://docs.cloud.google.com/bigquery/docs/servicenow-transfer?hl=zh-tw#data_type_mapping)。選取「false」即可使用更新的資料類型對應。如要進一步瞭解資料類型對應更新，請參閱「[2027 年 3 月 16 日](https://docs.cloud.google.com/bigquery/docs/transfer-changes?hl=zh-tw#Mar16-servicenow)」。
   * 在「Ingestion type」(擷取類型) 部分，選取「Full」(完整) 或「Incremental」(增量)。
     + 如果選取「Incremental」(增量) ([預先發布版](https://cloud.google.com/products?hl=zh-tw#product-launch-stages))，請在「Write mode」(寫入模式) 中選取「Upsert」(新增或更新)。如要進一步瞭解寫入模式，請參閱「[完整或增量轉移](https://docs.cloud.google.com/bigquery/docs/servicenow-transfer?hl=zh-tw#full_or_incremental_transfers)」一節的說明。
   * 在「ServiceNow tables to transfer」(要移轉的 ServiceNow 資料表)，點選「Browse」(瀏覽)：
     + 選取要轉移至 BigQuery 目的地資料集的所有物件。您也可以在這個欄位手動輸入要移轉資料的物件。
     + 如果已選取「Upsert」(新增或更新) 做為增量寫入模式，則必須選取一個欄做為浮水印欄，然後選取一或多個欄做為主鍵。
   * 在「Value type」(值類型) 選取下列其中一個選項：
     + 如要移轉資料庫中儲存的資料值，請選取「Actual」(實際)。
     + 如要移轉資料欄的顯示值，請選取「Display」(顯示)。
5. 在「Destination settings」(目的地設定) 部分，「Dataset」(資料集) 請選取您為了儲存資料而建立的資料集。
6. 在「Transfer config name」(轉移設定名稱) 部分，「Display name」(顯示名稱) 請輸入資料移轉作業名稱。
7. 在「Schedule options」(排程選項) 部分執行下列操作：

   * 在「Repeat frequency」(重複頻率) 清單選取選項，指定這項資料移轉作業的執行頻率。如要指定自訂重複頻率，請選取「Custom」(自訂)。如果選取「On-demand」(隨選)，這項資料移轉作業會在您[手動觸發](https://docs.cloud.google.com/bigquery/docs/working-with-transfers?hl=zh-tw#manually_trigger_a_transfer)後執行。
   * 視情況選取「Start now」(立即開始) 或「Start at set time」(在所設時間開始執行)，並提供開始日期和執行時間。
8. 選用：在「Notification options」(通知選項) 專區，執行下列操作：

   * 如要啟用電子郵件通知，請點選「Email notification」(電子郵件通知) 切換按鈕。啟用這個選項之後，若移轉失敗，移轉作業管理員就會收到電子郵件通知。
   * 如要針對這項資料移轉作業啟用 [Pub/Sub 移轉作業執行通知](https://docs.cloud.google.com/bigquery/docs/transfer-run-notifications?hl=zh-tw)，請點選「Pub/Sub notifications」(Pub/Sub 通知) 切換按鈕。您可以選取[主題](https://docs.cloud.google.com/pubsub/docs/overview?hl=zh-tw#types)名稱，也可以點選「Create a topic」(建立主題) 來建立主題。
9. 按一下「儲存」。

### bq

輸入 [`bq mk`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_mk) 指令，並加上移轉建立標記 `--transfer_config`：

```
bq mk
    --transfer_config
    --project_id=PROJECT_ID
    --data_source=DATA_SOURCE
    --display_name=DISPLAY_NAME
    --target_dataset=DATASET
    --params='PARAMETERS'
```

更改下列內容：

* `PROJECT_ID` (選用)：您的 Google Cloud 專案 ID。
  如未指定專案 ID，系統會使用預設專案。
* `DATA_SOURCE`：資料來源 (例如 `servicenow`)。
* `DISPLAY_NAME`：移轉設定的顯示名稱。資料移轉作業名稱可以是任意值，日後需要修改移轉作業時，能夠據此識別即可。
* `DATASET`：移轉設定的目標資料集。
* `PARAMETERS`：已建立移轉設定的 JSON 格式參數。例如：`--params='{"param":"param_value"}'`。以下是 ServiceNow 資料移轉的參數：

  | ServiceNow 參數 | 必要或選填 | 說明 |
  | --- | --- | --- |
  | `connector.networkAttachment` | 選用 | 用於確保連線至 ServiceNow 執行個體的網路附件名稱。 |
  | `connector.instanceId` | 必填 | ServiceNow 執行個體的執行個體 ID |
  | `connector.authentication.username` | 必填 | 使用者的 ServiceNow 執行個體使用者名稱。 |
  | `connector.authentication.password` | 必填 | ServiceNow 執行個體使用者的密碼。 |
  | `connector.authentication.oauth.clientId` | 必填 | 用於透過 ServiceNow 執行個體進行 OAuth 驗證的用戶端 ID。 |
  | `connector.authentication.oauth.clientSecret` | 必填 | 用於透過 ServiceNow 執行個體進行 OAuth 驗證的用戶端密鑰。 |
  | `connector.instanceCloudType` | 選用 | 指定 ServiceNow 帳戶的雲端類型。 支援的值如下： + 如果 ServiceNow 執行個體網址符合 `https://INSTANCE_ID.service-now.com` 模式，請選取「`COMMERCIAL_CLOUD`」 + 如果 ServiceNow 執行個體網址符合 `https://INSTANCE_ID.servicenowservices.com` 模式，請選取「Government Community Cloud (GCC)」(政府機構社群雲端 (GCC))`GOVERNMENT_COMMUNITY_CLOUD`。 |
  | `ingestionType` | 選用 | 定義從來源 ServiceNow 服務轉移資料至目的地的轉移方法，決定要重新載入完整資料集，還是執行有效率的增量更新。 |
  | `writeMode` | 選用 | 如果使用遞增式擷取，則決定遞增式擷取的同步策略。如要進行增量轉移，這個欄位為必填。支援的值為 `WRITE_MODE_UPSERT`。 |
  | `assets` | 必填 | 要從 ServiceNow 移轉的 ServiceNow 資料表名稱清單。 |
  | `watermarkColumns` | 選用 | 如果使用遞增擷取，則來源資料表欄位 (通常是日期時間) 會用於追蹤上次成功同步的點，讓連接器只查詢並轉移自該特定時間建立或修改的記錄。如要進行增量轉移，這個欄位為必填。 |
  | `primaryKeys` | 選用 | 如果使用增量擷取，則為用來明確識別來源資料表中每個資料列的專屬資料欄或資料欄組合。如要進行增量轉移，這個欄位為必填。 |
  | `valueType` | 選用 | 控制 ServiceNow 的特定資料類型如何對應至 BigQuery 資料類型。 |
  | `connector.legacyMapping` | 必填 | 設為 `true` (預設值) 即可使用[舊版資料類型對應](#data_type_mapping)。如要使用更新後的資料類型對應，請將這個值設為 `false`。如果您要進行增量轉移，這個值必須是 `false`。如要進一步瞭解資料類型對應更新，請參閱「[2027 年 3 月 16 日](https://docs.cloud.google.com/bigquery/docs/transfer-changes?hl=zh-tw#Mar16-servicenow)」。 |

  在增量轉移期間指定多項資產時，`watermarkColumns` 和 `primaryKeys` 欄位的值會對應至 `assets` 欄位中的值位置。請確保所有相關設定清單中的資料表和對應資料欄順序一致。

  舉例來說，下列指令會在預設專案中建立 ServiceNow 資料移轉作業，並提供所有必要參數：

  ```
    bq mk
      --transfer_config
      --target_dataset=mydataset
      --data_source=servicenow
      --display_name='My Transfer'
      --params='{"connector.authentication.oauth.clientId": "1234567890",
          "connector.authentication.oauth.clientSecret":"ABC12345",
          "connector.authentication.username":"user1",
          "connector.authentication.password":"abcdef1234",
          "connector.instanceId":"dev-instance",
          "connector.networkAttachment": "projects/dev-project1/regions/us-central1/networkattachments/na1"}'
  ```

  下列指令會在預設專案中建立 ServiceNow 增量資料移轉作業，並使用 `UPSERT` 寫入模式。

  ```
    bq mk
        --transfer_config
        --target_dataset=mydataset
        --data_source=servicenow
        --display_name='My Transfer'
        --params='{"assets": ["incident", "change_request"],
            "connector.authentication.oauth.clientId": "1234567890",
            "connector.authentication.oauth.clientSecret":"ABC12345",
            "connector.authentication.username":"user1",
            "connector.authentication.password":"abcdef1234",
            "connector.instanceId":"dev-instance",
            "ingestionType":"incremental",
            "writeMode":"WRITE_MODE_UPSERT",
            "watermarkColumns":["sys_updated_on","sys_updated_on"],
            "primaryKeys":[["sys_id"], ["sys_id"]]}'
  ```

### API

請使用 [`projects.locations.transferConfigs.create`](https://docs.cloud.google.com/bigquery/docs/reference/datatransfer/rest/v1/projects.locations.transferConfigs/create?hl=zh-tw) 方法，並提供 [`TransferConfig`](https://docs.cloud.google.com/bigquery/docs/reference/datatransfer/rest/v1/projects.locations.transferConfigs?hl=zh-tw#TransferConfig) 資源的執行個體。

儲存移轉設定後，ServiceNow 連接器會根據排程選項自動觸發移轉作業。每次執行移轉作業時，ServiceNow 連接器都會將 ServiceNow 中的所有可用資料移轉至 BigQuery。

如要在正常排程以外手動執行資料移轉作業，可以啟動[回填作業](https://docs.cloud.google.com/bigquery/docs/working-with-transfers?hl=zh-tw#manually_trigger_a_transfer)。

## 資料類型對應

**注意：** 2027 年 3 月 16 日，ServiceNow 連接器將更新部分資料類型對應。詳情請參閱「[2027 年 3 月 16 日](https://docs.cloud.google.com/bigquery/docs/transfer-changes?hl=zh-tw#Mar16-servicenow)」。

下表說明 ServiceNow 資料移轉作業中的資料類型對應方式：

| ServiceNow 資料類型 | BigQuery 資料類型 | [更新的 BigQuery 資料類型](https://docs.cloud.google.com/bigquery/docs/transfer-changes?hl=zh-tw#Mar16-servicenow) |
| --- | --- | --- |
| `decimal` | `FLOAT64` |  |
| `integer` | `INTEGER` |  |
| `boolean` | `BOOLEAN` |  |
| `glide_date` | `DATE` |  |
| `glide_date_time` | `DATETIME` |  |
| `glide_list` | `STRING` | `ARRAY` |
| `glide_time` | `INT64` |  |
| `reference` | `STRING` |  |
| `currency` | `STRING` |  |
| `sys_class_name` | `STRING` |  |
| `domain_id` | `STRING` |  |
| `domain_path` | `STRING` |  |
| `guid` | `STRING` |  |
| `translated_html` | `STRING` |  |
| `journal` | `STRING` |  |
| `string` | `STRING` |  |
| `list` | `STRING` | `ARRAY` |

## 排解轉移程序的相關問題

以下各節將詳細說明設定 ServiceNow 資料移轉時的常見問題。

詳情請參閱「[排解移轉設定問題](https://docs.cloud.google.com/bigquery/docs/transfer-troubleshooting?hl=zh-tw)」。

### 啟用 ServiceNow 導致轉移失敗

如果未在 ServiceNow 中啟用「採購」、「產品目錄」或「合約管理」應用程式，就會發生問題，導致資料移轉失敗。如要修正這個問題，請啟用下列三個應用程式：

* [取得](https://www.servicenow.com/docs/csh?topicname=t_ActivateProcurement.html&version=latest)
* [產品目錄](https://www.servicenow.com/docs/csh?topicname=t_ActivateAProductCatalogItem.html&version=latest)
* [合約管理](https://www.servicenow.com/docs/csh?topicname=c_ContractManagement.html&version=latest) (預設啟用)

### 轉移作業執行期間發生問題

發生問題，導致系統無法如預期建立轉移作業。如要解決這個問題，請按照下列步驟操作：

* 確認 ServiceNow 帳戶憑證 (例如「使用者名稱」、「密碼」、「用戶端 ID」和「用戶端密鑰」值) 有效。
* 確認執行個體 ID 是 ServiceNow 執行個體的有效 ID。

### 其他錯誤

如要瞭解 ServiceNow 資料移轉期間發生的其他錯誤，請參閱「[ServiceNow 移轉問題](https://docs.cloud.google.com/bigquery/docs/transfer-troubleshooting?hl=zh-tw#servicenow-issues)」一文。

## 定價

如要瞭解 ServiceNow 移轉作業的定價資訊，請參閱「[資料移轉服務定價](https://docs.cloud.google.com/bigquery/pricing?hl=zh-tw#bqdts)」。

## 後續步驟

* 如需 BigQuery 資料移轉服務的總覽，請參閱
  [BigQuery 資料移轉服務簡介](https://docs.cloud.google.com/bigquery/docs/dts-introduction?hl=zh-tw)。
* 如要瞭解如何使用移轉作業，包括取得移轉設定、列出移轉設定以及查看移轉設定的執行記錄，請參閱[使用移轉功能](https://docs.cloud.google.com/bigquery/docs/working-with-transfers?hl=zh-tw)一文。
* 瞭解如何[透過跨雲端作業載入資料](https://docs.cloud.google.com/bigquery/docs/load-data-using-cross-cloud-transfer?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-16 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-16 (世界標準時間)。"],[],[]]