Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [參考資料](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 將 PostgreSQL 資料載入 BigQuery

如要安排從 PostgreSQL 到 BigQuery 的週期性資料移轉作業，您可以建立移轉設定，指定要移轉的資料物件，以及資料移轉作業的排程頻率。設定移轉設定後，[BigQuery 資料移轉服務](https://docs.cloud.google.com/bigquery/docs/dts-introduction?hl=zh-tw)就會按照指定時間表，將最新資料移轉至 BigQuery 資料表。

如要瞭解 PostgreSQL 轉移作業的運作方式，請參閱「[PostgreSQL 資料轉移簡介](https://docs.cloud.google.com/bigquery/docs/postgresql-transfer-intro?hl=zh-tw)」。

## 限制

PostgreSQL 資料移轉作業有下列限制：

* 單一 PostgreSQL 資料庫可同時執行的遷移作業數量上限，取決於 [PostgreSQL 資料庫支援的並行連線數量上限](https://www.postgresql.org/docs/current/runtime-config-connection.html#GUC-MAX-CONNECTIONS)。並行傳輸作業的數量應限制在小於 PostgreSQL 資料庫支援的並行連線數量上限值。
* 單一移轉設定一次只能支援一項資料移轉作業。如果排定在第一次資料移轉完成前執行第二次資料移轉，則系統只會完成第一次資料移轉，並略過與第一次資料移轉重疊的任何其他資料移轉。

  為避免單一移轉設定略過移轉作業，建議您設定重複頻率，增加大型資料移轉作業之間的時間長度。
* 資料移轉期間，PostgreSQL 連接器會找出已建立索引和分區的鍵資料欄，以平行批次方式移轉資料。因此，建議您指定主鍵資料欄，或使用資料表中的索引資料欄，以提升效能並降低資料移轉錯誤率。請考量下列事項：

  + 如有索引或主鍵限制，建立平行批次時僅支援下列資料欄類型：
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
  + 如果 PostgreSQL 資料移轉作業未使用主鍵或索引資料欄，則每個資料表最多只能支援 2,000,000 筆記錄。

### 增量移轉作業限制

PostgreSQL 遞增移轉作業有下列限制：

* 浮水印欄只能選擇 `TIMESTAMP` 欄。
* 只有具備有效浮水印資料欄的資產，才支援增量擷取。
* 基準欄中的值必須單調遞增。
* 增量轉移作業無法同步處理來源表格中的刪除作業。
* 單一移轉設定只能支援增量或完整擷取。
* 首次執行增量擷取後，您就無法更新 `asset` 清單中的物件。
* 首次執行增量擷取後，您就無法變更移轉設定中的寫入模式。
* 第一次增量擷取作業執行後，您就無法變更浮水印欄或主鍵。
* 目的地 BigQuery 資料表會使用提供的
  主鍵進行分群，並受限於[分群資料表限制](https://docs.cloud.google.com/bigquery/docs/clustered-tables?hl=zh-tw#limitations)。
* 首次將現有移轉設定更新為增量擷取模式時，更新後的第一次資料移轉會從資料來源移轉所有可用資料。後續的任何增量資料移轉作業，都只會從資料來源移轉新的和更新的資料列。
* 建議您在基準欄建立索引。這個連接器會使用浮水印資料欄，在遞增移轉作業中篩選資料，因此為這些資料欄建立索引可提升效能。
* 執行增量移轉作業時，必須使用更新後的資料類型對應。

## 事前準備

* 在 PostgreSQL 資料庫中[建立使用者](https://www.postgresql.org/docs/16/app-createuser.html)。
* 確認您已完成[啟用 BigQuery 資料移轉服務](https://docs.cloud.google.com/bigquery/docs/enable-transfer-service?hl=zh-tw)所需的所有動作。
* 請[建立 BigQuery 資料集](https://docs.cloud.google.com/bigquery/docs/datasets?hl=zh-tw)來儲存您的資料。
* 確認您具備[必要角色](#required-roles)，可完成本文件中的工作。

### 必要的角色

如要設定 Pub/Sub 的移轉作業執行通知，請確認您具備 `pubsub.topics.setIamPolicy` Identity and Access Management (IAM) 權限。如果您只設定電子郵件通知，則不需要 Pub/Sub 權限。詳情請參閱「[BigQuery 資料移轉服務執行通知](https://docs.cloud.google.com/bigquery/docs/transfer-run-notifications?hl=zh-tw)」。

如要取得建立 BigQuery 資料移轉服務資料移轉作業所需的權限，請要求管理員授予您專案的 [BigQuery 管理員](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.admin)  (`roles/bigquery.admin`) IAM 角色。如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

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

如果 PostgreSQL 資料庫連線沒有公開 IP 位址，您必須[設定網路連結](https://docs.cloud.google.com/vpc/docs/create-manage-network-attachments?hl=zh-tw)。

如需必要網路設定的詳細操作說明，請參閱下列文件：

* 如要從 Cloud SQL 移轉，請參閱「[設定 Cloud SQL 執行個體存取權](https://docs.cloud.google.com/bigquery/docs/cloud-sql-instance-access?hl=zh-tw)」。
* 如果您是從 AWS 轉移，請參閱「[設定 AWS-Google Cloud VPN 和網路連結](https://docs.cloud.google.com/bigquery/docs/aws-vpn-network-attachment?hl=zh-tw)」。
* 如要從 Azure 轉移，請參閱「[設定 Azure-Google Cloud VPN 和網路連結](https://docs.cloud.google.com/bigquery/docs/azure-vpn-network-attachment?hl=zh-tw)」。

## 設定 PostgreSQL 資料移轉作業

使用下列任一選項設定移轉設定，將 PostgreSQL 資料新增至 BigQuery：

### 控制台

1. 前往「Data transfers」(資料移轉) 頁面。

   [前往「資料移轉」頁面](https://console.cloud.google.com/bigquery/transfers?hl=zh-tw)
2. 按一下「add 建立移轉作業」。
3. 在「Source type」(來源類型) 部分，「Source」(來源) 請選取「PostgreSQL」。
4. 在「Data source details」(資料來源詳細資料) 部分執行下列操作：

   * 在「Network attachment」(網路連結) 部分選取現有的網路連結，或是點選「Create Network Attachment」(建立網路連結)。詳情請參閱本文的「[網路連線](#network-connections)」一節。
   * 在「Host」(主機) 部分，輸入 PostgreSQL 資料庫伺服器的主機名稱或 IP 位址。
   * 在「Port number」(通訊埠編號) 中，輸入 PostgreSQL 資料庫伺服器的通訊埠編號。
   * 在「Database name」(資料庫名稱) 部分，輸入 PostgreSQL 資料庫的名稱。
   * 在「Username」(使用者名稱) 部分，輸入發起 PostgreSQL 資料庫連線的 PostgreSQL 使用者名稱。
   * 在「Password」(密碼) 部分，輸入啟動 PostgreSQL 資料庫連線的 PostgreSQL 使用者密碼。
   * 在「TLS Mode」(TLS 模式) 中，從選單選取一個選項。如要進一步瞭解 TLS 模式，請參閱「[TLS 設定](https://docs.cloud.google.com/bigquery/docs/postgresql-transfer-intro?hl=zh-tw#tls-configuration)」。
   * 在「Trusted PEM Certificate」(信任的 PEM 憑證) 欄位中，輸入核發資料庫伺服器 TLS 憑證的憑證授權單位 (CA) 公開憑證。詳情請參閱「[信任的伺服器憑證 (PEM)](https://docs.cloud.google.com/bigquery/docs/postgresql-transfer-intro?hl=zh-tw#trusted_server_certificate_pem)」一文。
   * 在「Enable legacy mapping」(啟用舊版對應) 部分，選取「true」(預設)，即可使用[舊版資料類型對應](https://docs.cloud.google.com/bigquery/docs/postgresql-transfer-intro?hl=zh-tw#data-type-mapping)。選取「false」即可使用更新版資料類型對應。如果您要進行增量轉移，這個值必須為 **false**。如要進一步瞭解資料類型對應更新，請參閱「[2027 年 3 月 16 日](https://docs.cloud.google.com/bigquery/docs/transfer-changes?hl=zh-tw#Mar16-postgresql)」。
     資料庫伺服器。
   * 在「Ingestion type」(擷取類型) 部分，選取「Full」(完整) 或「Incremental」(增量)。
     + 如果選取「Incremental」(增量)，請在「Write mode」(寫入模式) 中選取「Append」(附加) 或「Upsert」(新增或更新)。如要進一步瞭解不同的寫入模式，請參閱「[完整或增量轉移](https://docs.cloud.google.com/bigquery/docs/postgresql-transfer-intro?hl=zh-tw#full-incremental-transfers)」一節的說明。
   * 在「PostgreSQL objects to transfer」(要移轉的 PostgreSQL 物件) 部分，按一下「Browse」(瀏覽)。

     選取要轉移至 BigQuery 目的地資料集的所有物件。您也可以在這個欄位手動輸入要移轉資料的物件。

     + 如果選取「Append」(附加) 做為增量寫入模式，就必須選取一個欄做為浮水印欄。
     + 如果選取「Upsert」(新增或更新) 做為增量寫入模式，則必須選取一個欄做為浮水印欄，然後選取一或多個欄做為主鍵。
5. 在「Transfer config name」(移轉設定名稱) 部分，「Display name」(顯示名稱) 請輸入移轉作業的名稱。移轉作業名稱可以是任何值，能讓您辨識移轉作業，方便您日後在必要時進行修改。
6. 在「Schedule options」(排程選項) 部分執行下列操作：

   * 選取重複頻率。如果選取「小時」、「天」(預設)、「週」或「月」選項，必須一併指定頻率。您也可以選取「Custom」(自訂) 選項，建立專屬的重複頻率。如果選取「On-demand」(隨選)，這項資料移轉作業會在您[手動觸發](https://docs.cloud.google.com/bigquery/docs/working-with-transfers?hl=zh-tw#manually_trigger_a_transfer)後執行。
   * 視情況選取「立即開始」或「在所設時間開始執行」選項，並提供開始日期和執行時間。
7. 在「Destination settings」(目的地設定) 部分，「Dataset」(資料集) 請選取您為了儲存資料而建立的資料集，或按一下「建立新的資料集」，然後建立一個做為目的地資料集。
8. 選用：在「Notification options」(通知選項) 專區，執行下列操作：

   * 如要啟用電子郵件通知，請將「Email notifications」切換按鈕設為開啟。啟用這個選項之後，若移轉失敗，移轉作業管理員就會收到電子郵件通知。
   * 如要設定移轉作業的 Pub/Sub 執行[通知](https://docs.cloud.google.com/bigquery/docs/transfer-run-notifications?hl=zh-tw)，請將「Pub/Sub notifications」(Pub/Sub 通知) 切換鈕撥到開啟位置。您可以選取[主題](https://docs.cloud.google.com/pubsub/docs/admin?hl=zh-tw)名稱，或點選「Create a topic」(建立主題) 來建立主題。
9. 按一下 [儲存]。

### bq

輸入 [`bq mk` 指令](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_mk)，
並提供轉移建立旗標 `--transfer_config`：

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

* PROJECT\_ID (選用)： Google Cloud 專案 ID。如未提供 `--project_id` 旗標來指定特定專案，系統會使用預設專案。
* DATA\_SOURCE：資料來源，即 `postgresql`。
* DISPLAY\_NAME：資料移轉設定的顯示名稱。移轉作業名稱可以是任意值，日後需要修改移轉作業時，能夠據此識別即可。
* DATASET：資料移轉設定的目標資料集。
* PARAMETERS：以 JSON 格式建立的轉移設定參數。例如：`--params='{"param":"param_value"}'`。以下是 PostgreSQL 移轉作業的參數：

  + `connector.networkAttachment` (選用)：要連線至 PostgreSQL 資料庫的網路連結名稱。
  + `connector.database`：PostgreSQL 資料庫的名稱。
  + `connector.endpoint.host`：資料庫的主機名稱或 IP 位址。
  + `connector.endpoint.port`：資料庫的通訊埠編號。
  + `connector.authentication.username`：資料庫使用者的使用者名稱。
  + `connector.authentication.password`：資料庫使用者的密碼。
  + `connector.tls.mode`：指定要與這項轉移作業搭配使用的 [TLS 設定](https://docs.cloud.google.com/bigquery/docs/postgresql-transfer-intro?hl=zh-tw#tls-configuration)：
    - `ENCRYPT_VERIFY_CA_AND_HOST`：加密資料，並驗證憑證授權單位和主機名稱
    - `ENCRYPT_VERIFY_CA`：加密資料，且僅驗證憑證授權單位
    - `ENCRYPT_VERIFY_NONE` 僅用於資料加密
    - `DISABLE`，不加密或驗證
  + `connector.tls.trustedServerCertificate`：(選用) 提供一或多個 [PEM 編碼憑證](https://docs.cloud.google.com/bigquery/docs/postgresql-transfer-intro?hl=zh-tw#trusted_server_certificate_pem)。只有在 `connector.tls.mode` 為 `ENCRYPT_VERIFY_CA_AND_HOST` 或 `ENCRYPT_VERIFY_CA` 時才需要。
  + `ingestionType`：指定 `full` 或 `incremental`。[預先發布版](https://cloud.google.com/products?hl=zh-tw#product-launch-stages)支援增量移轉。詳情請參閱「[完整或增量轉移](https://docs.cloud.google.com/bigquery/docs/postgresql-transfer-intro?hl=zh-tw#full-incremental-transfers)」。
  + `writeMode`：指定 `WRITE_MODE_APPEND` 或 `WRITE_MODE_UPSERT`。
  + `watermarkColumns`：將資料表中的資料欄指定為浮水印資料欄。
    如要進行增量移轉，則必須填寫這個欄位。
  + `primaryKeys`：將資料表中的資料欄指定為主鍵。
    如要進行增量移轉，則必須填寫這個欄位。
  + `connector.legacyMapping`：設為 `true` (預設)，即可使用[舊版資料類型對應](https://docs.cloud.google.com/bigquery/docs/postgresql-transfer-intro?hl=zh-tw#data-type-mapping)。設為 `false` 即可使用更新版資料類型對應。如要進行增量移轉，這個值必須是 `false`。如要進一步瞭解資料類型對應更新，請參閱「[2027 年 3 月 16 日](https://docs.cloud.google.com/bigquery/docs/transfer-changes?hl=zh-tw#Mar16-postgresql)」。
  + `assets`：要從 PostgreSQL 資料庫移轉的 PostgreSQL 資料表名稱清單。

舉例來說，下列指令會建立名為 `My Transfer` 的 PostgreSQL 移轉作業：

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

在增量轉移期間指定多個資產時，`watermarkColumns` 和 `primaryKeys` 欄位的值會對應至 `assets` 欄位中的值位置。在以下範例中，`dep_id` 對應至資料表 `DB1/USER1/DEPARTMENT`，而 `report_by` 和 `report_title` 則對應至資料表 `DB1/USER1/EMPLOYEES`。

```
      "primaryKeys":[['dep_id'], ['report_by','report_title']],
      "assets":["DB1/USER1/DEPARTMENT","DB1/USER1/EMPLOYEES"],
```

### API

請使用 [`projects.locations.transferConfigs.create` 方法](https://docs.cloud.google.com/bigquery/docs/reference/datatransfer/rest/v1/projects.locations.transferConfigs/create?hl=zh-tw)，並提供 [`TransferConfig` 資源](https://docs.cloud.google.com/bigquery/docs/reference/datatransfer/rest/v1/projects.locations.transferConfigs?hl=zh-tw#TransferConfig)的例項。

儲存移轉設定時，PostgreSQL 連接器會根據排程選項自動觸發移轉作業。每次執行移轉作業時，PostgreSQL 連接器都會將 PostgreSQL 中的所有可用資料移轉至 BigQuery。

如要手動執行資料移轉 (不在正常排程內)，可以啟動[回填作業](https://docs.cloud.google.com/bigquery/docs/working-with-transfers?hl=zh-tw#manually_trigger_a_transfer)。

## 疑難排解

如果無法順利設定資料移轉作業，請參閱「[PostgreSQL 移轉問題](https://docs.cloud.google.com/bigquery/docs/transfer-troubleshooting?hl=zh-tw#postgresql-issues)」。

## 轉移中繼資料

**預覽**

這項產品適用《[服務專屬條款](https://docs.cloud.google.com/terms/service-terms?hl=zh-tw#1)》中「一般服務條款」一節的《正式發布前產品條款》。正式發布前的產品是按照「原樣」提供，支援範圍可能有限。
詳情請參閱[推出階段說明](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages)。

您也可以使用 PostgreSQL 連接器，[將中繼資料轉移至 Knowledge Catalog](https://docs.cloud.google.com/knowledge-catalog/docs/connectors?hl=zh-tw)。詳情請參閱「[將 PostgreSQL 中繼資料載入 Knowledge Catalog](https://docs.cloud.google.com/knowledge-catalog/docs/postgresql-transfer?hl=zh-tw)」。

## 後續步驟

* 請參閱 [BigQuery 資料移轉服務總覽](https://docs.cloud.google.com/bigquery/docs/dts-introduction?hl=zh-tw)。
* 瞭解如何[管理移轉作業](https://docs.cloud.google.com/bigquery/docs/working-with-transfers?hl=zh-tw)，包括取得移轉設定資訊、列出移轉設定，以及查看移轉作業的執行記錄。
* 瞭解如何[透過 BigQuery Omni 作業載入資料](https://docs.cloud.google.com/bigquery/docs/load-data-using-cross-cloud-transfer?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-10-22 (世界標準時間)。