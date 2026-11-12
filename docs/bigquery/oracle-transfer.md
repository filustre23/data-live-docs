Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [參考資料](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 將 Oracle 資料載入 BigQuery

如要安排從 Oracle 資料庫到 BigQuery 的週期性資料移轉作業，請建立移轉設定，指定要移轉的資料物件，以及資料移轉作業的排程頻率。設定移轉設定後，[BigQuery 資料移轉服務](https://docs.cloud.google.com/bigquery/docs/dts-introduction?hl=zh-tw)會按照指定的時間表，將最新資料移轉至 BigQuery 資料表。

如要瞭解 Oracle 移轉作業的運作方式，請參閱「[Oracle 資料移轉簡介](https://docs.cloud.google.com/bigquery/docs/oracle-transfer-intro?hl=zh-tw)」。

## 限制

Oracle 移轉作業有下列限制：

* Oracle 資料庫的同時連線數量有限，因此單一 Oracle 資料庫的同時移轉作業數量也受到限制。
* 如果 Oracle 資料庫連線沒有可用的公開 IP，您必須[設定網路連結](https://docs.cloud.google.com/vpc/docs/create-manage-network-attachments?hl=zh-tw)，並符合下列要求：
  + 資料來源必須可從網路連結所在的子網路存取。
  + 網路連結不得位於 `240.0.0.0/24` 範圍內的子網路。
  + 如果網路連結有使用中的連線，則無法刪除。如要刪除網路連結，請[與 Cloud Customer Care 團隊聯絡](https://docs.cloud.google.com/bigquery/docs/getting-support?hl=zh-tw)。
  + 如果是 `us` 多區域，網路連結必須位於 `us-central1` 區域。如果是 `eu` 多區域，網路連結必須位於 `europe-west4` 區域。
* 如果網路連結是在與 Google Cloud 資料移轉專案不同的 Google Cloud 專案中建立，您必須將 `compute.networkAttachments.get` 和 `compute.networkAttachments.update` 權限授予 Google Cloud 資料移轉專案的[服務代理](https://docs.cloud.google.com/bigquery/docs/enable-transfer-service?hl=zh-tw#service_agent)。
* 週期性 Oracle 移轉作業之間的最短間隔時間為 15 分鐘。週期性移轉作業的預設間隔為 24 小時。
* 單一移轉設定在特定時間只能支援一項資料移轉作業。如果第二項資料移轉作業排定在第一項移轉作業完成前執行，則只有第一項資料移轉作業會完成，而與第一項移轉作業重疊的其他資料移轉作業則會略過。
  + 為避免單一移轉設定略過移轉作業，建議您設定「重複頻率」，增加大型資料移轉作業之間的時間長度。
* 在資料移轉期間，Oracle 連接器會識別已建立索引和分區的鍵資料欄，以平行批次方式移轉資料。因此，建議您在資料表中指定主鍵資料欄或使用索引資料欄，以提升效能並降低資料移轉的錯誤率。
  + 如果您有索引或主鍵限制，則只有下列資料欄類型支援建立平行批次：
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
  + 如果 Oracle 資料移轉作業未使用主鍵或索引資料欄，則每個資料表最多只能支援 2,000,000 筆記錄。
* 如果設定的網路連結和虛擬機器 (VM) 執行個體位於不同區域，從 Oracle 移轉資料時，可能會發生跨區域資料移動。

### 增量移轉作業限制

Oracle 增量移轉作業有下列限制：

* 最多只能選擇 `TIMESTAMP` 個資料欄做為浮水印欄。
* 只有具備有效浮水印資料欄的資產，才支援增量擷取。
* 基準欄中的值必須單調遞增。
* 增量移轉作業無法同步處理來源資料表中的刪除作業。
* 單一移轉設定只能支援增量或完整擷取。
* 首次執行增量擷取後，您就無法更新 `asset` 清單中的物件。
* 首次執行增量擷取後，您就無法變更移轉設定中的寫入模式。
* 首次執行增量擷取後，就無法變更基準欄或主鍵。
* 目的地 BigQuery 資料表會使用提供的主鍵進行分群，並受[分群資料表限制](https://docs.cloud.google.com/bigquery/docs/clustered-tables?hl=zh-tw#limitations)規範。
* 首次將現有移轉設定更新為遞增擷取模式時，更新後的第一次資料移轉會從資料來源移轉所有可用資料。後續的任何增量資料移轉作業，都只會從資料來源移轉新的和更新的資料列。

如要瞭解增量移轉作業的運作方式，請參閱「[完整或增量移轉作業](https://docs.cloud.google.com/bigquery/docs/oracle-transfer-intro?hl=zh-tw#full-incremental-transfers)」。

## 事前準備

下列各節說明建立 Oracle 移轉作業前須採取的步驟。

### Oracle 必要條件

* 在 Oracle 資料庫中[建立使用者憑證](https://docs.oracle.com/cd/B13789_01/server.101/b10759/statements_8003.htm)。
* [將 `Create Session` 系統權限授予使用者](https://docs.oracle.com/cd/B13789_01/server.101/b10759/statements_9013.htm)，允許建立工作階段。
* 為使用者帳戶[指派資料表空間](https://docs.oracle.com/cd/B19306_01/network.102/b14266/admusers.htm#i1006219)。

建立 Oracle 移轉作業時，您也必須提供下列 Oracle 資料庫資訊。

| 參數名稱 | 說明 |
| --- | --- |
| `database` | 資料庫名稱。 |
| `host` | 資料庫的主機名稱或 IP 位址。 |
| `port` | 資料庫的通訊埠編號。 |
| `username` | 存取資料庫的使用者名稱。 |
| `password` | 存取資料庫的密碼。 |

### BigQuery 事前準備

* 確認您已完成[啟用 BigQuery 資料移轉服務](https://docs.cloud.google.com/bigquery/docs/enable-transfer-service?hl=zh-tw)的所有必要動作。
* 請[建立 BigQuery 資料集](https://docs.cloud.google.com/bigquery/docs/datasets?hl=zh-tw)來儲存您的資料。
* 如要設定 Pub/Sub 的移轉作業執行通知，請確認您具備 `pubsub.topics.setIamPolicy` Identity and Access Management (IAM) 權限。如果只設定電子郵件通知，則不需要 Pub/Sub 權限。詳情請參閱 [BigQuery 資料移轉服務執行通知](https://docs.cloud.google.com/bigquery/docs/transfer-run-notifications?hl=zh-tw)一文。

### 必要的 BigQuery 角色

如要取得建立 BigQuery 資料移轉服務資料移轉作業所需的權限，請要求管理員授予您專案的 [BigQuery 管理員](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.admin) (`roles/bigquery.admin`) IAM 角色。如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

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

## 將 Oracle 資料載入 BigQuery

使用下列任一選項設定移轉設定，將 Oracle 資料新增至 BigQuery：

### 控制台

1. 前往 Google Cloud 控制台的「資料移轉」頁面。

   [前往「資料移轉」](https://console.cloud.google.com/bigquery/transfers?hl=zh-tw)
2. 按一下「add 建立移轉作業」。
3. 在「Source type」(來源類型) 部分，「Source」(來源) 請選取「Oracle」。
4. 在「Data source details」(資料來源詳細資料) 部分執行下列操作：

   * 在「Network attachment」(網路連結) 部分選取現有的網路連結，或是點選「Create Network Attachment」(建立網路連結)。
   * 在「Host」(主機) 部分，輸入資料庫的主機名稱或 IP。
   * 在「Port」(通訊埠) 部分，輸入 Oracle 資料庫用來接收傳入連線的通訊埠編號，例如 `1521`。
   * 在「Database name」(資料庫名稱) 部分，輸入 Oracle 資料庫的名稱。
   * 在「Connection type」(連線類型) 部分，輸入連線網址類型，例如 `SERVICE`、`SID` 或 `TNS`。
   * 在「Username」(使用者名稱) 部分，輸入啟動 Oracle 資料庫連線的使用者的名稱。
   * 在「Password」(密碼) 部分，輸入啟動 Oracle 資料庫連線的使用者密碼。
   * 在「TLS Mode」(TLS 模式) 中，從下拉式選單選取一個選項。如要進一步瞭解 TLS 模式，請參閱「[TLS 設定](https://docs.cloud.google.com/bigquery/docs/oracle-transfer-intro?hl=zh-tw#tls-configuration)」。
   * 在「Trusted PEM Certificate」(信任的 PEM 憑證) 欄位中，輸入核發資料庫伺服器 TLS 憑證的憑證授權單位 (CA) 公開憑證。詳情請參閱「[信任的伺服器憑證 (PEM)](https://docs.cloud.google.com/bigquery/docs/oracle-transfer-intro?hl=zh-tw#trusted_server_certificate_pem)」一文。
   * 在「Ingestion type」(擷取類型) 部分，選取「Full」(完整) 或「Incremental」(增量)。
     + 如果選取「Incremental」(增量) ([預先發布版](https://cloud.google.com/products?hl=zh-tw#product-launch-stages))，請在「Write mode」(寫入模式) 中選取「Append」(附加) 或「Upsert」(新增或更新)。如要進一步瞭解不同的寫入模式，請參閱「[完整或增量轉移](https://docs.cloud.google.com/bigquery/docs/oracle-transfer-intro?hl=zh-tw#full-incremental-transfers)」一節。
   * 在「Oracle objects to transfer」(要移轉的 Oracle 物件) 部分，點選「Browse」(瀏覽)：
     + 選取要轉移至 BigQuery 目的地資料集的所有物件。您也可以在這個欄位手動輸入要移轉資料的物件。
     + 如果選取「Append」(附加) 做為增量寫入模式，就必須選取一個欄做為浮水印欄。
     + 如果選取「Upsert」(新增或更新) 做為增量寫入模式，就必須選取一個欄做為浮水印欄，然後選取一或多個欄做為主鍵。
5. 在「Destination settings」(目的地設定) 部分，「Dataset」(資料集) 請選取您為了儲存資料而建立的資料集。
6. 在「Transfer config name」(轉移設定名稱) 部分，「Display name」(顯示名稱) 請輸入資料移轉作業名稱。
7. 在「Schedule options」(排程選項) 專區：

   * 在「Repeat frequency」(重複執行頻率) 清單中，選取選項，指定這項資料移轉作業的執行頻率。如要指定自訂重複頻率，請選取「Custom」(自訂)。如果選取「On-demand」(隨選)，這項移轉作業會在您[手動觸發](https://docs.cloud.google.com/bigquery/docs/working-with-transfers?hl=zh-tw#manually_trigger_a_transfer)後執行。
   * 視情況選取「Start now」(立即開始) 或「Start at set time」(在所設時間開始執行)，並提供開始日期和執行時間。
8. 選用：在「Notification options」(通知選項) 專區，執行下列操作：

   * 如要啟用電子郵件通知，請點選「Email notification」(電子郵件通知) 切換按鈕。當您啟用此選項時，移轉管理員會在移轉作業失敗時收到電子郵件通知。
   * 如要針對這項移轉作業啟用 [Pub/Sub 移轉作業執行通知](https://docs.cloud.google.com/bigquery/docs/transfer-run-notifications?hl=zh-tw)，請點選「Pub/Sub notifications」(Pub/Sub 通知) 切換按鈕。您可以選取[主題](https://docs.cloud.google.com/pubsub/docs/overview?hl=zh-tw#types)名稱，也可以點選「Create a topic」(建立主題) 來建立主題。
9. 按一下「儲存」。

### bq

輸入 [`bq mk` 指令](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_mk)，並提供移轉作業建立旗標 `--transfer_config`：

```
bq mk
    --transfer_config
    --project_id=PROJECT_ID
    --data_source=DATA_SOURCE
    --display_name=DISPLAY_NAME
    --target_dataset=DATASET
    --params='PARAMETERS'
```

其中：

* PROJECT\_ID (選用)：您的 Google Cloud 專案 ID。如未提供 `--project_id` 來指定特定專案，系統會使用預設專案。
* DATA\_SOURCE：資料來源 - `oracle`。
* DISPLAY\_NAME：移轉設定的顯示名稱。資料移轉作業名稱可以是任何值，能讓您辨識移轉作業，方便您日後在必要時進行修改。
* DATASET：移轉設定的目標資料集。
* PARAMETERS：JSON 格式的已建立移轉設定參數。例如：`--params='{"param":"param_value"}'`。以下是 Oracle 資料移轉的參數：

  + `connector.networkAttachment` (選用)：要連至 Oracle 資料庫的網路連結名稱。
  + `connector.authentication.Username`：Oracle 帳戶的使用者名稱。
  + `connector.authentication.Password`：Oracle 帳戶的密碼。
  + `connector.database`：Oracle 資料庫的名稱。
  + `connector.endpoint.host`：資料庫的主機名稱或 IP。
  + `connector.endpoint.port`：Oracle 資料庫用於接收傳入連線的通訊埠編號，例如 `1520`。
  + `connector.connectionType`：連線網址類型，例如 `SERVICE`、`SID` 或 `TNS`。
  + `connector.tls.mode`：指定要與這項轉移作業搭配使用的 [TLS 設定](https://docs.cloud.google.com/bigquery/docs/oracle-transfer-intro?hl=zh-tw#tls-configuration)：
    - `ENCRYPT_VERIFY_CA_AND_HOST`：加密資料，並驗證憑證授權單位和主機名稱
    - `ENCRYPT_VERIFY_CA`：加密資料，僅驗證憑證授權單位
    - `ENCRYPT_VERIFY_NONE` 僅用於資料加密
    - `DISABLE`：不加密或驗證
  + `connector.tls.trustedServerCertificate`：(選用) 提供一或多個 [PEM 編碼憑證](https://docs.cloud.google.com/bigquery/docs/oracle-transfer-intro?hl=zh-tw#trusted_server_certificate_pem)。只有在 `connector.tls.mode` 為 `ENCRYPT_VERIFY_CA_AND_HOST` 或 `ENCRYPT_VERIFY_CA` 時才需要。
  + `ingestionType`：指定 `full` 或 `incremental`。[預先發布版](https://cloud.google.com/products?hl=zh-tw#product-launch-stages)支援增量移轉。詳情請參閱「[完整或增量移轉](https://docs.cloud.google.com/bigquery/docs/oracle-transfer-intro?hl=zh-tw#full-incremental-transfers)」。
  + `writeMode`：指定 `WRITE_MODE_APPEND` 或 `WRITE_MODE_UPSERT`。
  + `watermarkColumns`：將資料表中的資料欄指定為浮水印欄。如要進行增量移轉，則必須填寫這個欄位。
  + `primaryKeys`：將資料表中的資料欄指定為主鍵。如要進行增量移轉，則必須填寫這個欄位。
  + `assets`：要移轉至 BigQuery 的 Oracle 物件路徑，格式如下：`DATABASE_NAME/SCHEMA_NAME/TABLE_NAME`

在增量移轉期間指定多項資產時，`watermarkColumns` 和 `primaryKeys` 欄位的值會對應至 `assets` 欄位中的值位置。在以下範例中，`dep_id` 對應至資料表 `DB1/USER1/DEPARTMENT`，而 `report_by` 和 `report_title` 則對應至資料表 `DB1/USER1/EMPLOYEES`。

```
      "primaryKeys":[['dep_id'], ['report_by','report_title']],
      "assets":["DB1/USER1/DEPARTMENT","DB1/USER1/EMPLOYEES"],
```

舉例來說，下列指令會在預設專案中建立 Oracle 資料移轉作業，並提供所有必要參數：

```
bq mk
    --transfer_config
    --target_dataset=mydataset
    --data_source=oracle
    --display_name='My Transfer'
    --params='{"assets":["DB1/USER1/DEPARTMENT","DB1/USER1/EMPLOYEES"],
        "connector.authentication.username": "User1",
        "connector.authentication.password":"ABC12345",
        "connector.database":"DB1",
        "connector.endpoint.host":"192.168.0.1",
        "connector.endpoint.port":1520,
        "connector.connectionType":"SERVICE",
        "connector.tls.mode": "ENCRYPT_VERIFY_CA_AND_HOST",
        "connector.tls.trustedServerCertificate": "PEM-encoded certificate",
        "connector.networkAttachment":
        "projects/dev-project1/regions/us-central1/networkattachments/na1"
        "ingestionType":"incremental",
        "writeMode":"WRITE_MODE_APPEND",
        "watermarkColumns":["createdAt","createdAt"],
        "primaryKeys":[['dep_id'], ['report_by','report_title']]}'
```

### API

請使用 [`projects.locations.transferConfigs.create`](https://docs.cloud.google.com/bigquery/docs/reference/datatransfer/rest/v1/projects.locations.transferConfigs/create?hl=zh-tw) 方法，並提供 [`TransferConfig`](https://docs.cloud.google.com/bigquery/docs/reference/datatransfer/rest/v1/projects.locations.transferConfigs?hl=zh-tw#TransferConfig) 資源的執行個體。

儲存移轉設定時，Oracle 連接器會根據您的排程選項，自動觸發移轉作業。每次執行移轉作業時，Oracle 連接器都會將 Oracle 中的所有可用資料移轉至 BigQuery。

如要在排程時間以外手動執行資料移轉作業，可以啟動[補充執行作業](https://docs.cloud.google.com/bigquery/docs/working-with-transfers?hl=zh-tw#manually_trigger_a_transfer)。

## 排解轉移設定問題

如果無法順利設定資料移轉作業，請參閱「[Oracle 移轉作業問題](https://docs.cloud.google.com/bigquery/docs/transfer-troubleshooting?hl=zh-tw#oracle-issues)」。

## 後續步驟

* 如要進一步瞭解 BigQuery 資料移轉服務，請參閱「[什麼是 BigQuery 資料移轉服務](https://docs.cloud.google.com/bigquery/docs/dts-introduction?hl=zh-tw)」。
* 如要瞭解如何使用移轉作業，包括取得移轉設定資訊、列出移轉設定，以及查看移轉作業的執行記錄，請參閱「