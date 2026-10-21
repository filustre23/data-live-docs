Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [參考資料](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 將 ServiceNow 資料載入 BigQuery

你可以使用 ServiceNow 連接器的 [BigQuery 資料移轉服務](https://docs.cloud.google.com/bigquery/docs/dts-introduction?hl=zh-tw)，將資料從 ServiceNow 載入 BigQuery。透過 BigQuery 資料移轉服務，您可以安排週期性移轉工作，將 ServiceNow 的最新資料新增至 BigQuery。

## 限制

ServiceNow 資料移轉作業有下列限制：

* ServiceNow 連接器僅支援 [ServiceNow 資料表 API](https://www.servicenow.com/docs/bundle/zurich-api-reference/page/integrate/inbound-rest/concept/c_TableAPI.html)。
* 我們不建議在同一個 ServiceNow 執行個體上同時進行資料移轉。這可能會因 ServiceNow 執行個體負載過重，導致延遲或失敗。
  + 建議您錯開轉移作業的開始時間，以免轉移作業重疊。
* 為提升資料移轉效能，建議您將每次資料移轉的資產數量限制在 20 項。
* 週期性資料移轉作業之間的最短時間間隔為 15 分鐘。週期性移轉作業的預設間隔為 24 小時。
* 單一移轉設定一次只能支援一項資料移轉作業。如果排定在第一次資料移轉完成前執行第二次資料移轉，則只有第一次資料移轉會完成，任何與第一次資料移轉重疊的資料移轉都會略過。
  + 為避免在單一移轉設定中略過轉移作業，建議您設定「重複頻率」，增加大型資料移轉作業之間的時間間隔。
* 如要透過網路連結進行資料移轉，請務必先[定義靜態 IP 位址，再建立網路連結](https://docs.cloud.google.com/bigquery/docs/connect-to-sap-datasphere?hl=zh-tw#create-network-attachment)。

### 增量移轉限制

ServiceNow 增量移轉作業有下列限制：

* 浮水印欄只能選擇 `DATETIME` 欄。
* 只有含有有效浮水印欄的資產，才支援增量擷取。
* 基準欄中的值必須單調遞增。
* 增量移轉作業無法同步處理來源資料表中的刪除作業。
* 單一移轉設定只能支援增量或完整擷取。
* 首次執行增量擷取後，您就無法更新 `asset` 清單中的物件。
* 首次執行增量擷取作業後，您就無法在移轉設定中變更寫入模式。
* 首次執行增量擷取後，就無法變更基準值資料欄或主鍵。
* 目的地 BigQuery 資料表會使用提供的主鍵進行分群，並受[分群資料表限制](https://docs.cloud.google.com/bigquery/docs/clustered-tables?hl=zh-tw#limitations)規範。
* 首次將現有移轉設定更新為增量擷取模式時，更新後的第一次資料移轉會從資料來源移轉所有可用資料。後續的任何增量資料移轉作業，都只會從資料來源移轉新的和更新的資料列。

## 資料擷取選項

以下各節說明設定 ServiceNow 資料移轉作業時，可用的資料擷取選項。

### 完整或增量轉移

[設定 ServiceNow 移轉作業](#servicenow_transfer_setup)時，您可以在移轉設定中選取「Full」(完整) 或「Incremental」(遞增) 寫入偏好設定，指定資料載入 BigQuery 的方式。

您可以設定「完整」資料移轉，在每次資料移轉時，從 ServiceNow 資料集移轉所有資料。

或者，您也可以設定*增量*資料移轉，只移轉上次資料移轉後變更的資料，而不是每次資料移轉時都載入整個資料集。如果選取「Incremental」(增量) 做為資料移轉模式，則必須指定「Append」(附加) 或「Upsert」(新增或更新) 寫入模式，定義在增量資料移轉期間，資料寫入 BigQuery 的方式。以下各節說明可用的寫入模式。

#### Upsert 寫入模式

透過 upsert 寫入模式，系統會檢查主鍵，藉此更新資料列或在目的地資料表中插入新資料列。您可以指定主鍵，讓 ServiceNow 連接器判斷需要進行哪些變更，確保目的地資料表與來源資料表保持同步。如果資料移轉期間，目的地 BigQuery 資料表中有指定的主鍵，ServiceNow 連接器就會使用來源資料表的新資料更新該資料列。如果資料移轉期間沒有主鍵，ServiceNow 連接器會插入新資料列。

選取「新增或更新」模式時，必須選取浮水印欄和主鍵：

* ServiceNow 連接器需要浮水印資料欄，才能追蹤來源資料表的變更。

  選取每次修改資料列時都會更新的水印欄。建議使用與 `UPDATED_AT` 或 `LAST_MODIFIED` 欄類似的資料欄。

* 主鍵可以是資料表上的一或多個資料欄，ServiceNow 連接器會根據這些資料欄判斷是否需要插入或更新資料列。

  選取包含非空值且在資料表所有列中都是唯一值的資料欄。建議您使用包含系統產生的 ID、專屬參照代碼 (例如自動遞增 ID) 或不可變動的時間序列 ID 的資料欄。

  為避免資料遺失或損毀，您選取的主鍵資料欄必須包含不重複的值。如果您不確定所選主鍵欄是否不重複，建議改用完整擷取。

### 增量擷取行為

變更資料來源中的資料表結構定義時，這些資料表的遞增資料移轉作業會以下列方式反映在 BigQuery 中：

| 資料來源異動 | 增量擷取行為 |
| --- | --- |
| 新增資料欄 | 目的地 BigQuery 資料表會新增資料欄。這個資料欄的所有先前記錄都會有空值。 |
| 刪除資料欄 | 刪除的資料欄會保留在目的地 BigQuery 資料表中。系統會為這個已刪除資料欄的新項目填入空值。 |
| 變更資料欄中的資料類型 | 連接器僅支援[`ALTER COLUMN` DDL 陳述式支援的資料類型轉換](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#alter_column_set_data_type_statement)。任何其他資料類型轉換都會導致資料移轉失敗。 如果遇到任何問題，建議建立新的轉移設定。 |
| 重新命名資料欄 | 原始資料欄會保留在目的地 BigQuery 資料表中，而目的地資料表會新增一個資料欄，並使用更新後的名稱。 |

## 事前準備

建立 ServiceNow 資料移轉作業前，請先為 ServiceNow 和 BigQuery 執行下列操作。

### ServiceNow 必要條件

* 如要存取 ServiceNow API，請建立 [OAuth 憑證](https://www.servicenow.com/docs/csh?topicname=t_CreateEndpointforExternalClients.html&version=latest)。
* 您必須在 ServiceNow 執行個體中啟用下列所有 ServiceNow 應用程式：

  + [採購](https://docs.servicenow.com/csh?topicname=t_ActivateProcurement.html&version=latest)
  + [產品目錄](https://docs.servicenow.com/csh?topicname=c_ProductCatalog.html&version=latest)
  + [合約管理](https://docs.servicenow.com/csh?topicname=c_ContractManagement.html&version=latest)
* 如要開始轉移 ServiceNow 資料，您必須具備正確的憑證，才能連線至 ServiceNow 執行個體。

  + 如要取得 ServiceNow 開發人員執行個體的憑證，請登入 [ServiceNow 開發人員入口網站](https://developer.servicenow.com/dev.do)。您可以使用「Manage instance password」(管理執行個體密碼) 頁面中列出的使用者名稱和密碼。如要瞭解如何重設 ServiceNow 密碼，請參閱「[重設密碼](https://www.servicenow.com/docs/csh?topicname=password-reset-landing-page.html&version=latest)」
  + 如要取得 ServiceNow 正式版或子正式版執行個體的憑證，請與 ServiceNow 客戶管理員聯絡，要求提供使用者名稱和密碼。

### BigQuery 必要條件

* 完成[啟用 BigQuery 資料移轉服務](https://docs.cloud.google.com/bigquery/docs/enable-transfer-service?hl=zh-tw)的所有必要動作。
* [建立 BigQuery 資料集](https://docs.cloud.google.com/bigquery/docs/datasets?hl=zh-tw)，用於儲存資料。
* 如要設定 Pub/Sub 的移轉作業執行通知，請確認您具備 `pubsub.topics.setIamPolicy` Identity and Access Management (IAM) 權限。如果您只設定電子郵件通知，則不需要 Pub/Sub 權限。詳情請參閱「[BigQuery 資料移轉服務執行通知](https://docs.cloud.google.com/bigquery/docs/transfer-run-notifications?hl=zh-tw)」。

### 必要的 BigQuery 角色

如要取得建立 BigQuery 資料移轉服務資料移轉作業所需的權限，請要求管理員授予您專案的 [BigQuery 管理員](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.admin)  (`roles/bigquery.admin`) IAM 角色。如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

這個預先定義的角色具備建立 BigQuery 資料移轉服務資料移轉作業所需的權限。如要查看確切的必要權限，請展開「Required permissions」(必要權限) 部分：

#### 所需權限

您必須具備下列權限，才能建立 BigQuery 資料移轉服務資料移轉作業：

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

如要將 ServiceNow 資料新增至 BigQuery，請使用下列任一選項設定移轉設定：

### 控制台

1. 前往 Google Cloud 控制台的「Data transfers」(資料移轉) 頁面。

   [前往「資料轉移」頁面](https://console.cloud.google.com/bigquery/transfers?hl=zh-tw)
2. 按一下「add 建立移轉作業」。
3. 在「Source type」(來源類型) 部分，「Source」(來源) 請選取「ServiceNow」。
4. 在「Data source details」(資料來源詳細資料) 部分執行下列操作：

   * (選用) 在「Network attachment」(網路連結) 部分，從下拉式選單中選取網路連結，或是點選「Create Network Attachment」(建立網路連結)。
     + 選取網路連結，將這項資料移轉作業設定為使用單一且一致的 IP 位址。如果 ServiceNow 執行個體設為只接受來自特定 IP 位址的流量，可以使用這個選項。
     + 如要進一步瞭解如何建立網路連結，請參閱「[使用網路連結設定連線](https://docs.cloud.google.com/bigquery/docs/connect-to-sap-datasphere?hl=zh-tw#create-network-attachment)」
     + 如要進一步瞭解如何在 ServiceNow 定義 IP 位址，請參閱「[定義允許的 ServiceNow 內部 IP 位址](https://www.servicenow.com/docs/csh?topicname=sc-ip-addresses-access-allowlist.html&version=latest)」
   * 在「Instance ID」(執行個體 ID) 輸入 ServiceNow 執行個體 ID。您可以從 ServiceNow 網址取得這組 ID，例如 `https://INSTANCE_ID.service-now.com`。
   * (選用) 在「ServiceNow Cloud Type」(ServiceNow 雲端類型) 部分，選取 ServiceNow 帳戶的雲端類型：
     + 如果 ServiceNow 執行個體網址符合 `https://INSTANCE_ID.service-now.com` 模式，請選取「Commercial」(商業用途)。這是預設值。
     + 如果 ServiceNow 執行個體網址符合 `https://INSTANCE_ID.servicenowservices.com` 模式，請選取「Government Community Cloud (GCC)」(政府機構社群雲端 (GCC))。
   * 在「Username」(使用者名稱) 輸入要用於連線的 ServiceNow 使用者名稱。
   * 在「Password」(密碼) 輸入 ServiceNow 密碼。
   * 在「Client ID」(用戶端 ID) 輸入 OAuth 憑證中的用戶端 ID。如要產生憑證，請參閱[建立 OAuth 憑證](https://docs.oracle.com/cd/B13789_01/server.101/b10759/statements_9013.htm)的相關說明。
   * 在「Client secret」(用戶端密鑰) 輸入 OAuth 憑證中的用戶端密鑰。
   * 在「Enable legacy mapping」(啟用舊版對應) 部分，選取「true」(預設)，即可使用[舊版資料類型對應](https://docs.cloud.google.com/bigquery/docs/servicenow-transfer?hl=zh-tw#data_type_mapping)。選取「false」即可使用更新版資料類型對應。如要進一步瞭解資料類型對應更新，請參閱「[2027 年 3 月 16 日](https://docs.cloud.google.com/bigquery/docs/transfer-changes?hl=zh-tw#Mar16-servicenow)」。
   * 在「Ingestion type」(擷取類型) 部分，選取「Full」(完整) 或「Incremental」(增量)。
     + 如果選取「Incremental」(增量)，請在「Write mode」(寫入模式) 選取「Upsert」(新增或更新)。如要進一步瞭解寫入模式，請參閱「[完整或增量轉移](https://docs.cloud.google.com/bigquery/docs/servicenow-transfer?hl=zh-tw#full_or_incremental_transfers)」一節的說明。
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

輸入 [`bq mk`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_mk) 指令，並提供移轉作業建立旗標 `--transfer_config`：

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
* `DISPLAY_NAME`：移轉設定的顯示名稱。資料移轉作業名稱可以是任何值，能讓您辨識移轉作業，方便您日後在必要時進行修改。
* `DATASET`：移轉設定的目標資料集。
* `PARAMETERS`：所建立移轉設定的參數，採用 JSON 格式。例如：`--params='{"param":"param_value"}'`。ServiceNow 資料移轉作業的參數如下：

  | ServiceNow 參數 | 必要或選填 | 說明 |
  | --- | --- | --- |
  | `connector.networkAttachment` | 選用 | 網路連結名稱，用於確保與 ServiceNow 執行個體的連線能力。 |
  | `connector.instanceId` | 必填 | ServiceNow 執行個體的執行個體 ID |
  | `connector.authentication.username` | 必填 | 使用者 ServiceNow 執行個體的使用者名稱。 |
  | `connector.authentication.password` | 必填 | 使用者 ServiceNow 執行個體的密碼。 |
  | `connector.authentication.oauth.clientId` | 必填 | 用於透過 OAuth 驗證 ServiceNow 執行個體的用戶端 ID。 |
  | `connector.authentication.oauth.clientSecret` | 必填 | 用於透過 OAuth 驗證 ServiceNow 執行個體的用戶端密鑰。 |
  | `connector.instanceCloudType` | 選用 | 指定 ServiceNow 帳戶的雲端類型。 支援的值如下： + 如果 ServiceNow 執行個體網址符合 `https://INSTANCE_ID.service-now.com` 模式，請選取「`COMMERCIAL_CLOUD`」 + 如果 ServiceNow 執行個體網址符合 `https://INSTANCE_ID.servicenowservices.com` 模式，請選取「`GOVERNMENT_COMMUNITY_CLOUD`」 |
  | `ingestionType` | 選用 | 定義從來源 ServiceNow 傳輸資料至目的地的做法，決定要重新載入完整資料集，還是執行有效率的增量更新。 |
  | `writeMode` | 選用 | 如果使用增量擷取，則決定增量擷取的同步策略。如要進行增量轉移，這個欄位為必填。支援的值為 `WRITE_MODE_UPSERT`。 |
  | `assets` | 必填 | ServiceNow 資料表名稱清單，這些資料表會從 ServiceNow 移轉。 |
  | `watermarkColumns` | 選用 | 如果使用遞增擷取，來源資料表欄位 (通常是日期時間) 會用於追蹤上次成功同步處理的時間點，讓連接器能有效率地查詢及轉移自該特定時間以來建立或修改的記錄。如要進行增量轉移，這個欄位為必填。 |
  | `primaryKeys` | 選用 | 如果使用增量擷取，則為用來明確識別來源資料表中每個資料列的專屬資料欄或資料欄組合。如要進行增量移轉，則必須填寫這個欄位。 |
  | `valueType` | 選用 | 控制 ServiceNow 的特定資料類型如何對應至 BigQuery 資料類型。 |
  | `connector.legacyMapping` | 必填 | 設為 `true` (預設)，即可使用[舊版資料類型對應](#data_type_mapping)。設為 `false` 即可使用更新版資料類型對應。如要進行增量移轉，這個值必須是 `false`。如要進一步瞭解資料類型對應更新，請參閱「[2027 年 3 月 16 日](https://docs.cloud.google.com/bigquery/docs/transfer-changes?hl=zh-tw#Mar16-servicenow)」。 |

  在遞增移轉期間指定多項資產時，`watermarkColumns` 和 `primaryKeys` 欄位的值會對應至 `assets` 欄位中的值位置。請確保所有相關設定清單中的資料表和對應資料欄順序保持一致。

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

  下列指令會在預設專案中建立遞增 ServiceNow 資料移轉作業，並使用 `UPSERT` 寫入模式。

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

儲存移轉設定時，ServiceNow 連接器會根據您的排程選項，自動觸發移轉作業。每次執行移轉作業時，ServiceNow 連接器都會將 ServiceNow 中的所有可用資料移轉至 BigQuery。

如要手動執行資料移轉 (不在正常排程內)