Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [參考資料](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 將 PostgreSQL 資料載入 BigQuery

您可以使用 PostgreSQL 連接器的 [BigQuery 資料移轉服務](https://docs.cloud.google.com/bigquery/docs/dts-introduction?hl=zh-tw)，將資料從 PostgreSQL 載入至 BigQuery。這個連接器支援託管於地端部署環境、Cloud SQL，以及其他公有雲供應商 (例如 Amazon Web Services (AWS) 和 Microsoft Azure) 的 PostgreSQL 執行個體。您可以使用 BigQuery 資料移轉服務，安排週期性移轉工作，將 PostgreSQL 的最新資料新增至 BigQuery。

## 限制

PostgreSQL 資料移轉作業有下列限制：

* 單一 PostgreSQL 資料庫可同時執行的遷移作業數量上限，取決於 [PostgreSQL 資料庫支援的並行連線數量上限](https://www.postgresql.org/docs/current/runtime-config-connection.html#GUC-MAX-CONNECTIONS)。並行傳輸作業的數量應限制在小於 PostgreSQL 資料庫支援的並行連線數量上限。
* 單一移轉設定在特定時間只能支援一次資料移轉作業。如果排定在第一筆資料移轉作業完成前執行第二筆資料移轉作業，則系統只會完成第一筆資料移轉作業，並略過與第一筆作業重疊的任何其他資料移轉作業。

  為避免在單一轉移設定中略過轉移作業，建議您設定重複頻率，增加大型資料轉移作業之間的時間間隔。
* 資料移轉期間，PostgreSQL 連接器會識別已建立索引和已分割的鍵欄，以便以平行批次方式移轉資料。因此，我們建議您在資料表中指定主鍵欄或使用索引欄，以提升資料轉移的效能並降低錯誤率。請考量下列事項：

  + 如果您有索引或主鍵限制，建立平行批次時，系統僅支援下列資料欄類型：
    - `INTEGER`
    - `TINYINT`
    - `SMALLINT`
    - `FLOAT`
    - `REAL`
    - `DOUBLE`
    - `NUMERIC`
    - `BIGINT`
    - `DECIMAL`
    - `DATE`
  + 如果 PostgreSQL 資料移轉作業未使用主鍵或索引資料欄，每個資料表最多只能支援 2,000,000 筆記錄。

### 增量移轉限制

PostgreSQL 增量移轉作業有以下限制：

* 浮水印欄只能選擇 `TIMESTAMP` 欄。
* 只有含有有效浮水印欄的資產，才支援增量擷取。
* 浮水印資料欄中的值必須單調遞增。
* 增量轉移作業無法同步處理來源資料表中的刪除作業。
* 單一轉移設定只能支援增量或完整擷取。
* 第一次執行增量擷取後，就無法更新 `asset` 清單中的物件。
* 首次執行增量擷取後，就無法在轉移設定中變更寫入模式。
* 第一次執行遞增式擷取後，就無法變更時間戳記欄或主鍵。
* 目的地 BigQuery 資料表會使用提供的主鍵叢集，並受[分群資料表限制](https://docs.cloud.google.com/bigquery/docs/clustered-tables?hl=zh-tw#limitations)約束。
* 首次將現有轉移設定更新為增量擷取模式時，更新後的第一次資料移轉作業會移轉資料來源中的所有可用資料。後續的增量資料轉移作業只會轉移資料來源中的新資料列和更新資料列。
* 建議您在浮水印資料欄上建立索引。這個連接器會使用浮水印資料欄做為遞增轉移中的篩選器，因此為這些資料欄建立索引可提升效能。
* 進行增量轉移時，必須使用更新後的資料類型對應。

## 資料擷取選項

以下各節提供設定 PostgreSQL 資料移轉時的資料擷取選項相關資訊。

### 傳輸層安全標準 (TLS) 設定

PostgreSQL 連接器支援傳輸層級安全 (TLS) 的設定，可加密傳輸至 BigQuery 的資料。PostgreSQL 連接器支援下列 TLS 設定：

* 「加密資料，並驗證 CA 和主機名稱」模式。這個模式會使用 TCPS 通訊協定透過 TLS 完整驗證伺服器。這項功能會加密所有傳輸中的資料，並驗證資料庫伺服器的憑證是否由信任的憑證授權單位 (CA) 簽署。這個模式也會檢查您連線的主機名稱，是否與伺服器憑證中的一般名稱 (CN) 或主體別名 (SAN) 完全相符。這個模式可防止攻擊者使用其他網域的有效憑證，冒充資料庫伺服器。

  如果主機名稱與憑證 CN 或 SAN 不符，連線就會失敗。您必須設定 DNS 解析，使其與憑證相符，或使用其他安全模式。如要採取最安全的做法，防止中間人 (PITM) 攻擊，請使用這個模式。
* 「加密資料，但僅驗證 CA」模式。這個模式會透過 TCPS 通訊協定使用 TLS 加密所有資料，並驗證伺服器的憑證是否由用戶端信任的 CA 簽署。不過，這個模式不會驗證伺服器的主機名稱。只要憑證有效且由可信任的 CA 發行，這個模式就能成功連線，無論憑證中的主機名稱是否與您連線的主機名稱相符。

  如果您想確保連線至憑證由信任的 CA 簽署的伺服器，但主機名稱無法驗證，或您無法控管主機名稱設定，請使用這個模式。
* 「僅加密」模式。這個模式會加密用戶端與伺服器之間傳輸的所有資料。不會執行任何憑證或主機名稱驗證。

  這個模式會保護傳輸中的資料，提供一定程度的安全性，但可能容易受到中間人攻擊。

  如果您需要確保所有資料都經過加密，但無法或不想驗證伺服器的身分，請使用這個模式。使用私人虛擬私有雲時，建議採用這個模式。
* 「未加密或未驗證」模式。這個模式不會加密任何資料，也不會執行任何憑證或主機名稱驗證。所有資料都會以純文字形式傳送。

  在處理機密資料的環境中，不建議使用這個模式。建議您只在安全無虞的獨立網路中，將這個模式用於測試。

#### 信任的伺服器憑證 (PEM)

如果您使用「加密資料，並驗證 CA 和主機名稱」模式或「加密資料，並驗證 CA」模式，也可以提供一或多個 PEM 編碼的憑證。在某些情況下，BigQuery 資料移轉服務需要驗證資料庫伺服器的身分，因此必須使用這些憑證：

* 如果您使用貴機構內部私有 CA 簽署的憑證，或是自行簽署的憑證，則必須提供完整的憑證鏈結或單一自行簽署憑證。如果是透過代管雲端服務供應商 (例如 Amazon Relational Database Service (RDS)) 的內部 CA 發行的憑證，則必須執行這項操作。
* 如果資料庫伺服器憑證是由公開 CA 簽署 (例如 Let's Encrypt、DigiCert 或 GlobalSign)，您就不需要提供憑證。BigQuery 資料移轉服務已預先安裝並信任這些公開 CA 的根憑證。

您可以在轉移設定的「信任的 PEM 憑證」欄位中指定 PEM 編碼憑證，但須符合下列規定：

* 憑證必須是有效的 PEM 編碼憑證鏈結。
* 憑證必須完全正確。如果鏈結中缺少任何憑證或內容有誤，TLS 連線就會失敗。
* 如果是單一憑證，您可以提供資料庫伺服器中的單一自行簽署憑證。
* 如為私人 CA 核發的完整憑證鏈結，您必須提供完整的信任鏈結。包括資料庫伺服器的憑證，以及任何中繼和根 CA 憑證。

### 完整或累加轉移

[設定 PostgreSQL 轉移作業](#set-up)時，您可以在轉移作業設定中選取「完整」或「增量」寫入偏好設定，指定資料載入 BigQuery 的方式。[預先發布版](https://cloud.google.com/products?hl=zh-tw#product-launch-stages)支援增量轉移。

**注意：** 如要提供意見回饋或取得增量資料移轉支援，請傳送電子郵件至 [dts-preview-support@google.com](mailto:dts-preview-support@google.com)。
您可以設定*完整*資料移轉，在每次資料移轉時，轉移 PostgreSQL 資料集的所有資料。

或者，您也可以設定*增量*資料移轉作業 ([搶先版](https://cloud.google.com/products?hl=zh-tw#product-launch-stages))，只移轉上次資料移轉後變更的資料，而不是在每次資料移轉時載入整個資料集。如果為資料移轉作業選取「增量」**Incremental**，則必須指定「附加」**Append**或「插入或更新」**Upsert**寫入模式，定義在增量資料移轉期間，資料如何寫入 BigQuery。以下各節說明可用的寫入模式。

#### 附加寫入模式

附加寫入模式只會將新資料列插入目的地資料表。這個選項會嚴格附加移轉的資料，不會檢查現有記錄，因此這個模式可能會導致目的地資料表中的資料重複。

選取附加模式時，必須選取浮水印欄。PostgreSQL 連接器必須使用浮水印資料欄，才能追蹤來源資料表中的變更。

如要轉移 PostgreSQL 資料，建議選取只在建立記錄時更新的資料欄，且不會在後續更新時變更。例如「`CREATED_AT`」欄。

#### Upsert 寫入模式

新增或更新寫入模式會檢查主鍵，以更新資料列或在目的地資料表中插入新的資料列。您可以指定主鍵，讓 PostgreSQL 連接器判斷需要哪些變更，才能讓目的地資料表與來源資料表保持同步。如果在資料移轉期間，指定的主鍵出現在目標 BigQuery 資料表中，PostgreSQL 連接器就會使用來源資料表中的新資料更新該列。如果資料移轉期間沒有主鍵，PostgreSQL 連接器就會插入新列。

選取「新增或更新」模式時，必須選取浮水印欄和主鍵：

* PostgreSQL 連接器必須使用水位線資料欄，才能追蹤來源資料表中的變更。
  + 選取每次修改資料列時都會更新的水印資料欄。建議使用與 `UPDATED_AT` 或 `LAST_MODIFIED` 欄類似的資料欄。

* 主鍵可以是資料表上的一或多個資料欄，PostgreSQL 連接器需要這些資料欄來判斷是否需要插入或更新資料列。

  選取包含非空值的資料欄，這些值在資料表的所有資料列中都是不重複的。建議您使用包含系統產生 ID、專屬參照代碼 (例如自動遞增 ID) 或不可變動的時間序列 ID 的資料欄。

  為避免資料遺失或損毀，您選取的主鍵資料欄必須具有不重複的值。如果您對所選主鍵欄的唯一性有疑慮，建議改用附加寫入模式。

### 增量擷取行為

在資料來源中變更資料表結構定義時，這些資料表的增量資料移轉作業會以以下方式反映在 BigQuery 中：

| 資料來源異動 | 增量擷取行為 |
| --- | --- |
| 新增資料欄 | 目的地 BigQuery 資料表會新增資料欄。 這個資料欄的所有先前記錄都會有空值。 |
| 刪除資料欄 | 刪除的資料欄仍會保留在目的地 BigQuery 資料表中。系統會在新項目中填入空值。 |
| 變更資料欄中的資料類型 | 連接器僅支援 `ALTER COLUMN` DDL 陳述式支援的資料類型轉換。如果轉換成其他資料類型，資料移轉作業就會失敗。 如果遇到任何問題，建議建立新的轉移設定。 |
| 重新命名資料欄 | 原始資料欄會保留在目的地 BigQuery 資料表中，而目的地資料表會新增一個名稱更新的資料欄。 |

## 事前準備

* 在 PostgreSQL 資料庫中[建立使用者](https://www.postgresql.org/docs/16/app-createuser.html)。
* 確認您已完成[啟用 BigQuery 資料移轉服務](https://docs.cloud.google.com/bigquery/docs/enable-transfer-service?hl=zh-tw)的一切必要動作。
* 請[建立 BigQuery 資料集](https://docs.cloud.google.com/bigquery/docs/datasets?hl=zh-tw)來儲存您的資料。
* 請確認您具備[必要角色](#required-roles)，才能完成本文中的工作。

### 必要的角色

如要為 Pub/Sub 設定移轉作業執行通知，請確認您擁有 `pubsub.topics.setIamPolicy` 身分與存取權管理 (IAM) 權限。如果您只想設定電子郵件通知，則不需要擁有 Pub/Sub 權限。詳情請參閱 [BigQuery 資料移轉服務執行通知](https://docs.cloud.google.com/bigquery/docs/transfer-run-notifications?hl=zh-tw)。

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

### 網路連線數

如果 PostgreSQL 資料庫連線沒有可用的公開 IP 位址，請務必[設定網路附件](https://docs.cloud.google.com/vpc/docs/create-manage-network-attachments?hl=zh-tw)。

如需必要網路設定的詳細操作說明，請參閱下列文件：

* 如果是從 Cloud SQL 轉移，請參閱「[設定 Cloud SQL 執行個體存取權](https://docs.cloud.google.com/bigquery/docs/cloud-sql-instance-access?hl=zh-tw)」。
* 如果是從 AWS 轉移，請參閱「[設定 AWS-Google Cloud VPN 和網路附件](https://docs.cloud.google.com/bigquery/docs/aws-vpn-network-attachment?hl=zh-tw)」。
* 如要從 Azure 轉移，請參閱[設定 Azure-Google Cloud VPN 和網路附件](https://docs.cloud.google.com/bigquery/docs/azure-vpn-network-attachment?hl=zh-tw)。

## 設定 PostgreSQL 資料移轉

如要將 PostgreSQL 資料新增至 BigQuery，請使用下列任一方法設定移轉作業：

### 控制台

1. 前往「資料轉移」頁面。

   [前往「資料轉移」頁面](https://console.cloud.google.com/bigquery/transfers?hl=zh-tw)
2. 按一下 add「建立轉移作業」。
3. 在「Source type」(來源類型) 部分，「Source」(來源) 請選取「PostgreSQL」。
4. 在「Data source details」(資料來源詳細資料) 部分執行下列操作：

   * 在「Network attachment」(網路連結) 部分選取現有的網路連結，或是點選「Create Network Attachment」(建立網路連結)。詳情請參閱本文的「[網路連線](#network-connections)」一節。
   * 在「Host」(主機) 部分，輸入 PostgreSQL 資料庫伺服器的主機名稱或 IP 位址。
   * 在「Port number」(通訊埠編號) 中，輸入 PostgreSQL 資料庫伺服器的通訊埠編號。
   * 在「Database name」(資料庫名稱) 中輸入 PostgreSQL 資料庫的名稱。
   * 在「使用者名稱」欄位中，輸入啟動 PostgreSQL 資料庫連線的 PostgreSQL 使用者名稱。
   * 在「Password」(密碼) 部分，輸入啟動 PostgreSQL 資料庫連線的 PostgreSQL 使用者密碼。
   * 在「TLS Mode」(TLS 模式) 中，從選單選取一個選項。如要進一步瞭解 TLS 模式，請參閱「[TLS 設定](#tls_configuration)」。
   * 在「Trusted PEM Certificate」(信任的 PEM 憑證) 欄位中，輸入核發資料庫伺服器 TLS 憑證的憑證授權單位 (CA) 公開憑證。詳情請參閱「[信任的伺服器憑證 (PEM)](https://docs.cloud.google.com/bigquery/docs/postgresql-transfer?hl=zh-tw#trusted_server_certificate_pem)」一文。
   * 在「Enable legacy mapping」(啟用舊版對應) 部分，選取「true」(預設)，即可使用[舊版資料類型對應](#data_type_mapping)。選取「false」即可使用更新後的資料類型對應。如果您要進行增量轉移，這個值必須為 **false**。如要進一步瞭解資料類型對應更新，請參閱「[2027 年 3 月 16 日](https://docs.cloud.google.com/bigquery/docs/transfer-changes?hl=zh-tw#Mar16-postgresql)」。
     資料庫伺服器。
   * 在「Ingestion type」(擷取類型) 部分，選取「Full」(完整) 或「Incremental」(增量)。
     + 如果選取「Incremental」(增量) ([預先發布版](https://cloud.google.com/products?hl=zh-tw#product-launch-stages))，請在「Write mode」(寫入模式) 中選取「Append」(附加) 或「Upsert」(新增或更新)。如要進一步瞭解不同的寫入模式，請參閱「[完整或增量轉移](#full_or_incremental_transfers)」一節的說明。
   * 在「要轉移的 PostgreSQL 物件」部分，按一下「瀏覽」。

     選取要轉移至 BigQuery 目的地資料集的所有物件。您也可以在這個欄位手動輸入要移轉資料的物件。

     + 如果選取「Append」(附加) 做為增量寫入模式，就必須選取一個欄做為浮水印欄。
     + 如果已選取「Upsert」(新增或更新) 做為增量寫入模式，則必須選取一個欄做為浮水印欄，然後選取一或多個欄做為主鍵。
5. 在「Transfer config name」(轉移設定名稱) 部分，「Display name」(顯示名稱) 請輸入移轉作業的名稱。移轉作業名稱可以是任意值，日後需要修改移轉作業時能夠據此識別。
6. 在「Schedule options」(排程選項) 部分執行下列操作：

   * 選取重複頻率。如果選取「小時」、「天數」(預設)、「週數」或「月數」選項，則必須一併指定頻率。你也可以選取「Custom」(自訂) 選項，建立專屬的重複頻率。如果選取「On-demand」(隨選)，這項資料移轉作業會在您[手動觸發](https://docs.cloud.google.com/bigquery/docs/working-with-transfers?hl=zh-tw#manually_trigger_a_transfer)後執行。
   * 視情況選取「立即開始」或「在所設時間開始執行」選項，並提供開始日期和執行時間。
7. 在「Destination settings」(目的地設定) 部分，「Dataset」(資料集) 請選取您為了儲存資料而建立的資料集，或按一下「Create new dataset」(建立新的資料集)，然後建立一個做為目的地資料集。
8. 選用：在「Notification options」(通知選項) 專區，執行下列操作：

   * 如要啟用電子郵件通知，請點選「電子郵件通知」切換按鈕，將其設為開啟。啟用這個選項之後，若移轉失敗，移轉作業管理員就會收到電子郵件通知。
   * 如要為移轉作業設定 Pub/Sub 執行[通知](https://docs.cloud.google.com/bigquery/docs/transfer-run-notifications?hl=zh-tw)，請點選「Pub/Sub notifications」(Pub/Sub 通知) 切換按鈕，將其設為開啟。您可以選取[主題](https://docs.cloud.google.com/pubsub/docs/admin?hl=zh-tw)名稱，或點選「Create a topic」(建立主題) 來建立主題。
9. 按一下 [儲存]。

### bq

輸入 [`bq mk` 指令](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_mk)，並加上移轉建立標記 `--transfer_config`：

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

* PROJECT\_ID (選用)：您的 Google Cloud 專案 ID。
  如未提供 `--project_id` 標記指定特定專案，系統會使用預設專案。
* DATA\_SOURCE：資料來源，即 `postgresql`。
* DISPLAY\_NAME：資料移轉設定的顯示名稱。移轉作業名稱可以是任意值，日後需要修改移轉作業時，能夠據此識別即可。
* DATASET：資料移轉設定的目標資料集。
* PARAMETERS：已建立移轉設定的 JSON 格式參數。例如：`--params='{"param":"param_value"}'`。以下是 PostgreSQL 轉移作業的參數：

  + `connector.networkAttachment` (選用)：要連線至 PostgreSQL 資料庫的網路附件名稱。
  + `connector.database`：PostgreSQL 資料庫的名稱。
  + `connector.endpoint.host`：資料庫的主機名稱或 IP 位址。
  + `connector.endpoint.port`：資料庫的通訊埠編號。
  + `connector.authentication.username`：資料庫使用者的使用者名稱。
  + `connector.authentication.password`：資料庫使用者的密碼。
  + `connector.tls.mode`：指定要用於這項轉移作業的 [TLS 設定](#tls_configuration)：
    - `ENCRYPT_VERIFY_CA_AND_HOST` 加密資料，並驗證 CA 和主機名稱
    - `ENCRYPT_VERIFY_CA` 加密資料，且僅驗證 CA
    - `ENCRYPT_VERIFY_NONE` 僅適用於資料加密
    - `DISABLE`，因為沒有加密或驗證
  + `connector.tls.trustedServerCertificate`：(選用) 提供一或多個 [PEM 編碼的憑證](https://docs.cloud.google.com/bigquery/docs/postgresql-transfer?hl=zh-tw#trusted_server_certificate_pem)。只有在 `connector.tls.mode` 為 `ENCRYPT_VERIFY_CA_AND_HOST` 或 `ENCRYPT_VERIFY_CA` 時才需要提供。
  + `ingestionType`：指定 `full` 或 `incremental`。[預先發布版](https://cloud.google.com/products?hl=zh-tw#product-launch-stages)支援增量轉移。詳情請參閱「[完整或增量轉移](#full_or_incremental_transfers)」。
  + `writeMode`：指定 `WRITE_MODE_APPEND` 或 `WRITE_MODE_UPSERT`。
  + `watermarkColumns`：將資料表中的資料欄指定為浮水印資料欄。如要進行增量轉移，這個欄位為必填。
  + `primaryKeys`：將資料表中的資料欄指定為主鍵。
    如要進行增量轉移，這個欄位為必填。
  + `connector.legacyMapping`：設為 `true` (預設)，即可使用[舊版資料類型對應](#data_type_mapping)。如要使用更新後的資料類型對應，請將這個值設為 `false`。如果您要進行增量轉移，這個值必須是 `false`。如要進一步瞭解資料類型對應更新，請參閱「[2027 年 3 月 16 日](https://docs.cloud.google.com/bigquery/docs/transfer-changes?hl=zh-tw#Mar16-postgresql)」。
  + `assets`：要從 PostgreSQL 資料庫轉移的 PostgreSQL 資料表名稱清單。

舉例來說，下列指令會建立名為 `My Transfer` 的 PostgreSQL 轉移作業：

```
bq mk
    --transfer_config
    --target_dataset=mydataset
    --data_source=postgresql
    --display_name='My Transfer'
    --params='{"assets":["DB1/PUBLIC/DEPARTMENT","DB1/PUBLIC/EMPLOYEES"],
        "connector.authentication.username": "User1",
        "connector.authentication.password":"ABC12345",
        "connector.database":"DB1",
        "connector.endpoint.host":"192.168.0.1",
        "connector.endpoint.port":5432,
        "ingestionType":"incremental",
        "writeMode":"WRITE_MODE_APPEND",
        "watermarkColumns":["createdAt","createdAt"],
        "primaryKeys":[['dep_id'], ['report_by','report_title']],
        "connector.tls.mode": "ENCRYPT_VERIFY_CA_AND_HOST",
        "connector.tls.trustedServerCertificate": "PEM-encoded certificate"}'
```

在增量轉移期間指定多個資產時，`watermarkColumns` 和 `primaryKeys` 欄位的值會對應至 `assets` 欄位中的值位置。在下列範例中，`dep_id` 對應於資料表 `DB1/USER1/DEPARTMENT`，而 `report_by` 和 `report_title` 則對應於資料表 `DB1/USER1/EMPLOYEES`。

```
      "primaryKeys":[['dep_id'], ['report_by','report_title']],
      "assets":["DB1/USER1/DEPARTMENT","DB1/USER1/EMPLOYEES"],
```

### API

請使用 [`projects.locations.transferConfigs.create` 方法](https://docs.cloud.google.com/bigquery/docs/reference/datatransfer/rest/v1/projects.locations.transferConfigs/create?hl=zh-tw)，並提供 [`TransferConfig` 資源](https://docs.cloud.google.com/bigquery/docs/reference/datatransfer/rest/v1/projects.locations.transferConfigs?hl=zh-tw#TransferConfig)的執行個體。

儲存移轉設定後，PostgreSQL 連接器會根據排程選項自動觸發移轉作業。每次執行轉移作業時，PostgreSQL 連接器都會將 PostgreSQL 中的所有可用資料轉移至 BigQuery。

如要在正常排程以外手動執行資料移轉作業，可以啟動[回填作業](https://docs.cloud.google.com/bigquery/docs/working-with-transfers?hl=zh-tw#manually_trigger_a_transfer)。

## 資料類型對應

**注意：** PostgreSQL 連接器將於 2027 年 3 月 16 日更新部分資料類型對應。詳情請參閱「[2027 年 3 月 16 日](https://docs.cloud.google.com/bigquery/docs/transfer-changes?hl=zh-tw#Mar16-postgresql)」。

下表列出 PostgreSQL 資料類型對應的 BigQuery 資料類型。

| PostgreSQL 資料類型 | BigQuery 資料類型 | [更新的 BigQuery 資料類型](https://docs.cloud.google.com/bigquery/docs/transfer-changes?hl=zh-tw#Mar16-postgresql) |
| --- | --- | --- |
| `array` | `STRING` |  |
| `bigint` | `INTEGER` |  |
| `bigserial` | `INTEGER` |  |
| `bit(n)` | `STRING` |  |
| `bit varying(n)` | `STRING` |  |
| `boolean` | `BOOLEAN` |  |
| `box` | `STRING` |  |
| `bytea` | `BYTES` |  |
| `character` | `STRING` |  |
| `character varying` | `STRING` |  |
| `cidr` | `STRING` |  |
| `circle` | `STRING` |  |
| `circularstring` | `STRING` |  |
| `compoundcurve` | `STRING` |  |
| `curvepolygon` | `STRING` |  |
| `date` | `DATE` |  |
| `double precision` | `FLOAT` |  |
| `enum` | `STRING` |  |
| `geometrycollection` | `STRING` |  |
| `inet` | `STRING` |  |
| `integer` | `INTEGER` |  |
| `interval` | `STRING` |  |
| `json` | `STRING` | `JSON` |
| `jsonb` | `STRING` | `JSON` |
| `line` | `STRING` |  |
| `linestring` | `STRING` |  |
| `lseg` | `STRING` |  |
| `macaddr` | `STRING` |  |
| `macaddr8` | `STRING` |  |
| `money` | `STRING` |  |
| `multicurve` | `STRING` |  |
| `multilinestring` | `STRING` |  |
| `multipoint` | `STRING` |  |
| `multipolygon` | `STRING` |  |
| `multisurface` | `STRING` |  |
| `numeric(precision, scale)/decimal(precision, scale)` | `NUMERIC` |  |
| `path` | `STRING` |  |
| `point` | `STRING` |  |
| `polygon` | `STRING` |  |
| `polyhedralsurface` | `STRING` |  |
| `range` | `STRING` |  |
| `real` | `FLOAT` |  |
| `serial` | `INTEGER` |  |
| `smallint` | `INTEGER` |  |
| `smallserial` | `INTEGER` |  |
| `text` | `STRING` |  |
| `time [ (p) ] [ without timezone ]` | `TIMESTAMP` |  |
| `time [ (p) ] with time zone` | `TIMESTAMP` |  |
| `tin` | `STRING` |  |
| `timestamp [ (p) ] [ without timezone ]` | `TIMESTAMP` | `DATETIME` |
| `timestamp [ (p) ] with time zone` | `TIMESTAMP` |  |
| `triangle` | `STRING` |  |
| `tsquery` | `STRING` |  |
| `tsvector` | `STRING` |  |
| `uuid` | `STRING` |  |
| `xml` | `STRING` |  |

## 疑難排解

如果您無法順利設定資料移轉作業，請參閱 [PostgreSQL 移轉問題](https://docs.cloud.google.com/bigquery/docs/transfer-troubleshooting?hl=zh-tw#postgresql-issues)。

## 定價

如要瞭解 PostgreSQL 移轉作業的定價資訊，請參閱[資料移轉服務定價](https://docs.cloud.google.com/bigquery/pricing?hl=zh-tw#data-transfer-service-pricing)。

## 後續步驟

* 請參閱 [BigQuery 資料移轉服務總覽](https://docs.cloud.google.com/bigquery/docs/dts-introduction?hl=zh-tw)。
* 瞭解如何[管理移轉作業](https://docs.cloud.google.com/bigquery/docs/working-with-transfers?hl=zh-tw)，包括取得移轉設定資訊、列出移轉設定，以及查看移轉作業的執行記錄。
* 瞭解如何[透過跨雲端作業載入資料](https://docs.cloud.google.com/bigquery/docs/load-data-using-cross-cloud-transfer?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-12 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-12 (世界標準時間)。"],[],[]]