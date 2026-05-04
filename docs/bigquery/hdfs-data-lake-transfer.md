* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [參考資料](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 將 Apache Hive Metastore 資料表遷移至Google Cloud

本文說明如何使用 [BigQuery 資料移轉服務](https://docs.cloud.google.com/bigquery/docs/dts-introduction?hl=zh-tw)，將 Apache Hive Metastore 管理的 Iceberg 和 Hive 資料表遷移至Google Cloud 。

BigQuery 資料移轉服務中的 Apache Hive Metastore 遷移連接器，可讓您 Google Cloud 大規模無縫遷移 Hive Metastore 資料表。這個連結器支援地端部署和雲端環境 (包括 Cloudera 設定) 的 Hive 和 Iceberg 資料表。Hive Metastore 遷移連接器支援儲存在下列資料來源中的檔案：

* Apache Hadoop 分散式檔案系統 (HDFS)
* Amazon Simple Storage Service (Amazon S3)
* Azure Blob 儲存體或 Azure Data Lake Storage Gen2

透過 Hive Metastore 遷移連接器，您可以使用 Cloud Storage 做為檔案儲存空間，並向下列任一 metastore 註冊 Hive Metastore 資料表：

* [Lakehouse 執行階段目錄 Iceberg REST 目錄](https://docs.cloud.google.com/bigquery/docs/blms-rest-catalog?hl=zh-tw)

  建議您使用 Lakehouse 執行階段目錄 Iceberg REST 目錄，處理所有 Iceberg 資料。

  Lakehouse 執行階段目錄 Iceberg REST 目錄可為所有 Iceberg 資料提供單一事實來源，在查詢引擎之間建立互通性。除了 Apache Spark 和其他 OSS 引擎，您也可以使用 BigQuery 查詢資料。Lakehouse 執行階段目錄 Iceberg REST 目錄僅支援 Iceberg 資料表格式。
* [Dataproc Metastore](https://docs.cloud.google.com/dataproc-metastore/docs/overview?hl=zh-tw)

  Dataproc Metastore 支援 Hive 和 Iceberg 資料表格式。您只能使用 Apache Spark 和其他 OSS 引擎，從 Dataproc Metastore 讀取及寫入資料。

這個連接器支援完整轉移和僅轉移中繼資料。完整轉移會將來源資料表中的資料和中繼資料，一併轉移至目標中繼資料存放區。如果資料已儲存在 Cloud Storage 中，且您只想將資料登錄至目的地中繼存放區，則可以建立僅含中繼資料的轉移作業。

下圖概述遷移程序。

## 限制

Hive Metastore 資料表轉移作業有下列限制：

* Hive Metastore 轉移作業的排定執行時間間隔至少須為 30 分鐘。您仍可隨時觸發隨選執行作業。
* 如要遷移 Hive 資料表，必須使用 Dataproc Metastore 做為目的地中繼存放區。
* 檔案名稱必須符合 [Cloud Storage 物件命名規定](https://docs.cloud.google.com/storage/docs/objects?hl=zh-tw#naming)。
* Cloud Storage 的單一物件大小上限為 5 TiB。如果 Hive Metastore 表格中的檔案大於 5 TiB，系統就無法轉移。
* 如果資料在移轉作業進行期間於來源端變更，Storage 移轉服務會有特定行為。我們不建議在資料表主動遷移期間寫入資料表。如需其他 Storage 移轉服務限制的清單，請參閱「[已知限制](https://docs.cloud.google.com/storage-transfer/docs/known-limitations-transfer?hl=zh-tw)」。

## 資料擷取選項

以下各節將詳細說明如何設定 Hive Metastore 轉移作業。

### 增量移轉

如果移轉設定設有週期性時間表，後續每次移轉都會更新 Google Cloud 中的資料表，反映來源資料表的最新變更。舉例來說，所有資料更新，以及所有插入、刪除或更新作業 (含結構定義變更) 都會反映在 Google Cloud 中，每次轉移都會更新。

**注意：** 每次執行前，請確認中繼資料檔案反映最新狀態。建議[設定 `cron` 指令，自動定期上傳中繼資料](#automate-dumper)。

### 篩選分區

**注意：** 分區篩選器只能套用至 Hive 資料表。

您可以提供儲存在 Cloud Storage 中的自訂篩選器 JSON 檔案，從 Hive 表格移轉部分分割區。排定轉移作業時，請使用 `partition_filter_gcs_path` 參數，提供這個 JSON 檔案的完整 Cloud Storage 路徑。

以下是篩選器 JSON 檔案結構範例：

```
{
  "filters": [
    {
      "table": "db1.table1", "condition": "IN", "partition":
      ["partition1=value1/partition2=value2"]
    },
    {
      "table": "db1.table2", "condition": "LESS_THAN", "partition":
      ["partition1;value1"]
    },
    {
      "table": "db1.table3", "condition": "GREATER_THAN", "partition":
      ["partition1;value1"]
    },
    {
      "table": "db1.table4", "condition": "RANGE", "partition":
      ["partition1;value1;value2"]
    }
  ]
}
```

#### 篩選條件

JSON 檔案中的 `condition` 欄位支援下列值，每個值都有 `partition` 陣列的特定格式：

* **`IN`**：指定要納入的確切分割區路徑。`partition` 陣列包含字串，代表相對於資料表基本路徑的分割區確切目錄結構 (例如 `["partition_key1=value1/partition_key2=value2"]`)。您可以在陣列中指定多個路徑。
* **`LESS_THAN`**：包含主要分區鍵值小於或等於指定值的分區。`partition` 陣列必須包含格式為 `["<partition_key>;<value>"]` 的單一字串。
* **`GREATER_THAN`**：包含主要分區鍵值大於或等於指定值的分區。`partition` 陣列必須包含格式為 `["<partition_key>;<value>"]` 的單一字串。
* **`RANGE`**：包含主要分區鍵值落在指定範圍內 (含) 的分區。`partition` 陣列必須包含格式為 `["<partition_key>;<start_value>;<end_value>"]` 的單一字串。

篩選條件須遵守下列規則和限制：

* **包含的值：**`GREATER_THAN`、`LESS_THAN` 和 `RANGE` 的篩選條件包含提供的值。舉例來說，值為 `2023` 的 `LESS_THAN` 篩選器會納入 `2023` 之前 (含 `2023`) 的所有分區。
* **刪除分區：**如果現有的目的地分區符合分區篩選器，但來源中已不再存在，系統就會從目的地中繼存放區捨棄該分區。不過，該資料分割的基礎資料檔案不會從 Cloud Storage 目的地值區刪除。
* **單一表格限制：**
  + 同一個表格中不得包含多個篩選器。
  + 您無法在同一張表格中混用不同類型的條件 (例如：`GREATER_THAN` 和 `IN`)。
* **目標分區資料欄：**`GREATER_THAN`、`LESS_THAN` 和 `RANGE` 等篩選條件必須以主要分區資料欄為目標。
* **前置字串限制：**指定的篩選條件組合不得為每個資料表解析出超過 1000 個前置字串。舉例來說，如果資料表是依 `year/month/day` 分割，則 `year>2020` 等篩選條件必須產生少於 1000 個不重複的 `year=` 前置字元。

## 事前準備

排定 Hive Metastore 轉移作業前，請先執行本節中的步驟。

### 啟用 API

在Google Cloud 專案中[啟用下列 API](https://docs.cloud.google.com/endpoints/docs/openapi/enable-api?hl=zh-tw)：

* Data Transfer API
* Storage Transfer API

啟用 Data Transfer API 時，系統會建立[服務代理程式](https://docs.cloud.google.com/bigquery/docs/enable-transfer-service?hl=zh-tw#service_agent)。

### 設定權限

如要設定 Hive Metastore 轉移作業的權限，請按照下列各節的步驟操作。

1. 建立轉移作業的使用者或服務帳戶應具備 BigQuery 管理員角色 (`roles/bigquery.admin`)。如果您使用服務帳戶，該帳戶只會用於建立轉移作業。
2. 啟用 Data Transfer API 時，系統會建立[服務代理程式](https://docs.cloud.google.com/bigquery/docs/enable-transfer-service?hl=zh-tw#service_agent) (P4SA)。

   為確保服務代理具備執行 Hive Metastore 轉移作業的必要權限，請要求管理員在專案中授予服務代理下列 IAM 角色：

   **重要事項：**您必須將這些角色授予服務代理，*而非*使用者帳戶。如果未將角色授予正確的主體，可能會導致權限錯誤。
   * [Storage Transfer 管理員](https://docs.cloud.google.com/iam/docs/roles-permissions/storagetransfer?hl=zh-tw#storagetransfer.admin)  (`roles/storagetransfer.admin`)
   * [服務使用情形消費者](https://docs.cloud.google.com/iam/docs/roles-permissions/serviceusage?hl=zh-tw#serviceusage.serviceUsageConsumer)  (`roles/serviceusage.serviceUsageConsumer`)
   * [儲存空間管理員](https://docs.cloud.google.com/iam/docs/roles-permissions/storage?hl=zh-tw#storage.admin) (`roles/storage.admin`)
   * 如要將中繼資料遷移至 Lakehouse 執行階段目錄 Iceberg REST 目錄，請按照下列步驟操作：
     [BigLake 管理員](https://docs.cloud.google.com/iam/docs/roles-permissions/biglake?hl=zh-tw#biglake.admin)  (`roles/biglake.admin`)
   * 如要將中繼資料遷移至 Dataproc Metastore，請按照下列步驟操作：
     [Dataproc Metastore 資料擁有者](https://docs.cloud.google.com/iam/docs/roles-permissions/metastore?hl=zh-tw#metastore.metadataOwner)  (`roles/metastore.metadataOwner`)

   如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

   管理員或許也能透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)，授予服務代理必要權限。
3. 如果您使用服務帳戶，請執行下列指令，將 `roles/iam.serviceAccountTokenCreator` 角色授予服務代理程式：

   ```
   gcloud iam service-accounts add-iam-policy-binding
   SERVICE_ACCOUNT --member
   serviceAccount:service-PROJECT_NUMBER@gcp-sa-bigquerydatatransfer.iam.gserviceaccount.com --role
   roles/iam.serviceAccountTokenCreator
   ```
4. 在專案中，將下列角色授予 Storage 移轉服務代理程式 (`project-PROJECT_NUMBER@storage-transfer-service.iam.gserviceaccount.com`)：

   * `roles/storage.admin`
   * 如果您是從地端部署/HDFS 遷移，也必須授予 `roles/storagetransfer.serviceAgent` 角色。

   您也可以設定更精細的權限。詳情請參閱下列指南：

   * [HDFS 權限](https://docs.cloud.google.com/storage-transfer/docs/file-system-permissions?hl=zh-tw)
   * [Amazon S3 和 Microsoft Azure 權限](https://docs.cloud.google.com/storage-transfer/docs/iam-cloud?hl=zh-tw)

### 產生 Apache Hive 的中繼資料檔案

執行 `dwh-migration-dumper` 工具，[擷取](https://docs.cloud.google.com/bigquery/docs/hadoop-metadata?hl=zh-tw#apache-hive) Apache Hive 的中繼資料。這項工具會產生名為 `hive-dumper-output.zip` 的檔案，可上傳至 Cloud Storage bucket。本文將這個 Cloud Storage bucket 稱為 `DUMPER_BUCKET`。

您也可以使用指令碼，排定定期上傳時間。詳情請參閱[使用 `cron` 工作自動執行傾印工具](#automate-dumper)。

### 設定 Storage 移轉服務

選取下列選項之一：

### HDFS

如要轉移地端部署或 HDFS 資料，必須使用儲存空間轉移代理程式。

如要設定代理程式，請按照下列步驟操作：

1. 在內部部署代理程式機器上[安裝 Docker](https://docs.cloud.google.com/storage-transfer/docs/on-prem-set-up?hl=zh-tw#install_docker)。
2. 在 Google Cloud 專案中[建立 Storage 移轉服務代理集區](https://docs.cloud.google.com/storage-transfer/docs/on-prem-agent-pools?hl=zh-tw#create-pool)。
3. 在您的地端部署代理程式電腦上[安裝代理程式](https://docs.cloud.google.com/storage-transfer/docs/create-transfers/agent-based/hdfs?hl=zh-tw#install_agents)。

### Amazon S3

從 Amazon S3 移轉資料時，不需要代理程式。

如要設定 Storage 移轉服務以進行 Amazon S3 移轉作業，請按照下列步驟操作：

1. [設定 AWS Amazon S3 的存取憑證](https://docs.cloud.google.com/storage-transfer/docs/source-amazon-s3?hl=zh-tw#access_credentials)。
2. 設定存取憑證後，請記下存取金鑰 ID 和私密存取金鑰。
3. 如果 AWS 專案使用 IP 限制，請將 Storage 移轉服務 工作人員使用的 [IP 範圍](https://docs.cloud.google.com/storage-transfer/docs/source-amazon-s3?hl=zh-tw#ip_restrictions)新增至許可 IP 清單。

### Microsoft Azure

從 Microsoft Azure 儲存體轉移資料時，不需要代理程式。

如要設定 Storage 移轉服務，以便移轉 Microsoft Azure 儲存空間，請按照下列步驟操作：

1. 為 Microsoft Azure 儲存空間帳戶[產生共用存取簽章 (SAS) 權杖](https://docs.cloud.google.com/storage-transfer/docs/source-microsoft-azure?hl=zh-tw#sas-token)。
2. 產生 SAS 權杖後，請記下該權杖。
3. 如果 Microsoft Azure 儲存體帳戶使用 IP 限制，請將 Storage 移轉服務工作站使用的 [IP 範圍](https://docs.cloud.google.com/storage-transfer/docs/source-microsoft-azure?hl=zh-tw#ip_restrictions)加入允許的 IP 清單。

## 排定 Hive Metastore 轉移作業

選取下列選項之一：

### 控制台

1. 前往 Google Cloud 控制台的「資料移轉」頁面。

   [前往「資料轉移」頁面](https://console.cloud.google.com/bigquery/transfers?hl=zh-tw)
2. 按一下「建立轉移作業」add。
3. 在「來源類型」部分，從「來源」清單中選取「Hive Metastore」。
4. 在「位置」下方選取位置類型，然後選取區域。
5. 在「Transfer config name」(轉移設定名稱) 部分，「Display name」(顯示名稱) 請輸入資料移轉作業名稱。
6. 在「Schedule options」(排程選項) 部分執行下列操作：

   * 在「Repeat frequency」(重複頻率) 清單選取選項，指定這項資料移轉作業的執行頻率。如要指定自訂重複頻率，請選取「Custom」(自訂)。如果選取「On-demand」(隨選)，這項移轉作業會在您[手動觸發](https://docs.cloud.google.com/bigquery/docs/working-with-transfers?hl=zh-tw#manually_trigger_a_transfer)後執行。
   * 視情況選取「Start now」(立即開始) 或「Start at set time」(在所設時間開始執行)，並提供開始日期和執行時間。
7. 在「Data source details」(資料來源詳細資料) 部分執行下列操作：

   1. 在「轉移策略」中，選取下列任一選項：
      * `FULL_TRANSFER`：轉移所有資料，並向目標中繼存放區註冊中繼資料。這是預設選項。
      * `METADATA_ONLY`：僅註冊中繼資料。您必須在元資料中參照的正確 Cloud Storage 位置中，預先存有資料。
   2. 在「Table name patterns」(資料表名稱格式) 部分，提供符合 HDFS 資料庫中資料表的名稱或格式，指定要轉移的 HDFS 資料湖泊資料表。您必須使用 Java 規則運算式語法指定表格模式。例如：
      * `db1..*` 會比對 db1 中的所有資料表。
      * `db1.table1;db2.table2` 會比對 db1 中的 table1 和 db2 中的 table2。
   3. 在「BQMS discovery dump gcs path」(BQMS 探索傾印 GCS 路徑) 中，輸入您在[為 Apache Hive 建立中繼資料檔案](#generate-metadata-dump-for-apache-hive)時產生的 `hive-dumper-output.zip` 檔案路徑。如果您使用 [dumper 輸出自動化功能搭配 `cron`](#automate-dumper)，請提供 `--gcs-base-path` 中設定的 Cloud Storage 資料夾路徑，其中包含 dumper 輸出 ZIP 檔案。
      1. 在「儲存空間類型」中，選取下列其中一個選項。只有在「轉移策略」設為 `FULL_TRANSFER` 時，才能使用這個欄位：
      2. `HDFS`：如果檔案儲存空間是 `HDFS`，請選取這個選項。在「STS agent pool name」(STS 代理程式集區名稱) 欄位中，您必須提供[設定 Storage Transfer Agent](#configure-sts) 時建立的代理程式集區名稱。
      3. `S3`：如果檔案儲存空間是 `Amazon S3`，請選取這個選項。在「Access key ID」(存取金鑰 ID) 和「Secret access key」(存取密鑰) 欄位中，您必須提供[設定存取憑證](#configure-sts)時建立的存取金鑰 ID 和存取密鑰。
      4. `AZURE`：如果檔案儲存空間是 `Azure Blob Storage`，請選取這個選項。在「SAS token」(SAS 權杖) 欄位中，您必須提供[設定存取憑證](#configure-sts)時建立的 SAS 權杖。
   4. 選用：在「Partition Filter gcs path」(分區篩選器 GCS 路徑) 欄位中，輸入自訂篩選器 JSON 檔案的完整 Cloud Storage 路徑，以[篩選來源資料表中的分區](#filter-partitions)。
   5. 在**「Destination gcs path」(目的地 GCS 路徑)** 中，輸入 Cloud Storage bucket 的路徑，以儲存遷移的資料。
   6. 從下拉式清單中選擇目的地 Metastore 類型：
      * `DATAPROC_METASTORE`(舊版)：選取這個選項，將中繼資料儲存在 [Dataproc Metastore](https://docs.cloud.google.com/dataproc-metastore/docs/overview?hl=zh-tw) 中。您必須在「Dataproc metastore url」(Dataproc Metastore 網址) 中提供 Dataproc Metastore 的網址。
      * `BIGLAKE_REST_CATALOG`：選取這個選項，將中繼資料儲存在 Lakehouse 執行階段目錄 Iceberg REST 目錄中。系統會根據目標 Cloud Storage 值區建立目錄。
   7. 選用：針對「服務帳戶」，輸入要用於這項資料移轉作業的服務帳戶。服務帳戶應屬於建立移轉設定和目的地資料集的相同Google Cloud 專案。

### bq

如要排定 Hive Metastore 移轉作業，請輸入 `bq mk` 指令並加上移轉建立作業旗標 `--transfer_config`：

```
  bq mk --transfer_config
  --data_source=hadoop display_name='TRANSFER_NAME'
  --service_account_name='SERVICE_ACCOUNT'
  --project_id='PROJECT_ID' location='REGION'
  --params='{
    "transfer_strategy":"TRANSFER_STRATEGY",
    "table_name_patterns":"LIST_OF_TABLES",
    "table_metadata_path":"gs://DUMPER_BUCKET/hive-dumper-output.zip",
    "target_gcs_file_path":"gs://MIGRATION_BUCKET",
    "metastore":"METASTORE",
    "destination_dataproc_metastore":"DATAPROC_METASTORE_URL",
    "destination_bigquery_dataset":"BIGLAKE_METASTORE_DATASET",
    "translation_output_gcs_path":"gs://TRANSLATION_OUTPUT_BUCKET/metadata/config/default_database/",
    "storage_type":"STORAGE_TYPE",
    "agent_pool_name":"AGENT_POOL_NAME",
    "aws_access_key_id":"AWS_ACCESS_KEY_ID",
    "aws_secret_access_key":"AWS_SECRET_ACCESS_KEY",
    "azure_sas_token":"AZURE_SAS_TOKEN",
    "partition_filter_gcs_path":"FILTER_GCS_PATH"
    }'
```

更改下列內容：

* `TRANSFER_NAME`：移轉設定的顯示名稱。移轉作業名稱可以是任意值，日後需要修改移轉作業時，能夠據此識別即可。
* `SERVICE_ACCOUNT`：用於建立轉移作業的服務帳戶名稱。服務帳戶應屬於同一個Google Cloud 專案，該專案會建立轉移設定和目的地資料集。
* `PROJECT_ID`：您的 Google Cloud 專案 ID。如未提供 `--project_id` 指定特定專案，系統會使用預設專案。
* `REGION`：這項移轉設定的位置。
* `TRANSFER_STRATEGY`：(選用) 指定下列其中一個值：
  + `FULL_TRANSFER`：轉移所有資料，並向目標 Metastore 註冊中繼資料。這是預設值。
  + `METADATA_ONLY`：僅註冊中繼資料。您必須已在元資料中參照的正確 Cloud Storage 位置中提供資料。
* `LIST_OF_TABLES`：要轉移的實體清單。使用階層式命名規格 -
  `database.table`。這個欄位支援 RE2 規則運算式，可指定資料表。例如：
  + `db1..*`：指定資料庫中的所有資料表
  + `db1.table1;db2.table2`：資料表清單
* `DUMPER_BUCKET`：包含 `hive-dumper-output.zip` 檔案的 Cloud Storage bucket。如果您使用 [dumper 輸出自動化功能搭配 `cron`](#automate-dumper)，請將 `table_metadata_path` 變更為使用 `--gcs-base-path` 在 cron 設定中設定的 Cloud Storage 資料夾路徑，例如：`"table_metadata_path":"<var>GCS_PATH_TO_UPLOAD_DUMPER_OUTPUT</var>"`。
* `MIGRATION_BUCKET`：所有基礎檔案的載入目的地 GCS 路徑。只有在 `transfer_strategy` 為 `FULL_TRANSFER` 時，才能使用這項功能。
* `METASTORE`：要遷移的 Metastore 類型。請將此值設為下列其中一個值：
  + `DATAPROC_METASTORE`：將中繼資料轉移至 Dataproc Metastore。
  + `BIGLAKE_REST_CATALOG`：將中繼資料轉移至 Lakehouse 執行階段目錄 Iceberg REST 目錄。
* `DATAPROC_METASTORE_URL`：Dataproc Metastore 的網址。如果 `metastore` 為 `DATAPROC_METASTORE`，則為必要欄位。
* `BIGLAKE_METASTORE_DATASET`：Lakehouse 執行階段目錄的 BigQuery 資料集。如果 `metastore` 為 `BIGLAKE_METASTORE`，且 `transfer_strategy` 為 `FULL_TRANSFER`，則為必要欄位。
* `STORAGE_TYPE`：指定資料表的基礎檔案儲存空間。支援的類型為 `HDFS`、`S3` 和 `AZURE`。如果 `transfer_strategy` 為 `FULL_TRANSFER`，則為必填。
* `AGENT_POOL_NAME`：用於建立代理程式的代理程式集區名稱。如果 `storage_type` 為 `HDFS`，則為必要欄位。
* `AWS_ACCESS_KEY_ID`：[存取憑證](#configure-sts)中的存取金鑰 ID。如果 `storage_type` 為 `S3`，則為必要欄位。
* `AWS_SECRET_ACCESS_KEY`：來自[存取憑證](#configure-sts)的私密存取金鑰。如果 `storage_type` 為 `S3`，則為必要欄位。
* `AZURE_SAS_TOKEN`：來自[存取憑證](#configure-sts)的 SAS 權杖。如果 `storage_type` 為 `AZURE`，則為必要欄位。
* `FILTER_GCS_PATH`：(選用) 自訂篩選器 JSON 檔案的完整 Cloud Storage 路徑，用於[篩選分割區](#filter-partitions)。

執行這項指令，建立移轉設定並開始移轉 Hive 受管理資料表。根據預設，系統每隔 24 小時就會執行移轉作業，但您可以使用[移轉排程選項](#transfer_scheduling_options)進行設定。

轉移完成後，Hadoop 叢集中的資料表就會遷移至 `MIGRATION_BUCKET`。

## 使用 `cron` 工作自動執行傾印工具

您可以透過[`cron`](https://man7.org/linux/man-pages/man8/cron.8.html)工作執行 `dwh-migration-dumper` 工具，自動執行增量轉移作業。自動擷取中繼資料，確保資料來源的最新傾印檔可用於後續的增量轉移作業。

### 事前準備

使用這項自動化指令碼前，請先完成下列步驟：

1. 完成[傾印工具的所有必要條件](https://docs.cloud.google.com/bigquery/docs/generate-metadata?hl=zh-tw#prerequisites)。
2. [安裝 Google Cloud CLI](https://docs.cloud.google.com/sdk/docs/install?hl=zh-tw)。這個指令碼會使用 `gsutil` 指令列工具，將傾印器輸出內容上傳至 Cloud Storage。
3. 如要驗證 Google Cloud 以允許
   `gsutil`將檔案上傳至 Cloud Storage，請執行下列指令：

   ```
   gcloud auth application-default login
   ```

### 安排自動化動作

1. 將下列指令碼儲存到本機檔案。這個指令碼的設計宗旨，是透過 `cron` Daemon 進行設定及執行，自動擷取及上傳傾印器輸出內容。

   ```
   #!/bin/bash

   # Exit immediately if a command exits with a non-zero status.
   set -e
   # Treat unset variables as an error when substituting.
   set -u
   # Pipelines return the exit status of the last command to exit with a non-zero status.
   set -o pipefail

   # These values are used if not overridden by command-line options.
   DUMPER_EXECUTABLE="DUMPER_PATH/dwh-migration-dumper"
   GCS_BASE_PATH="gs://PATH_TO_DUMPER_OUTPUT"
   LOCAL_BASE_DIR="LOCAL_BASE_DIRECTORY_PATH"

   # Optional arguments for cloud environments
   DUMPER_HOST=""
   DUMPER_PORT=""
   HIVE_KERBEROS_URL=""
   HIVEQL_RPC_PROTECTION=""
   KERBEROS_AUTHENTICATION="false"

   # Function to display usage information
   usage() {
     echo "Usage: $0 [options]"
     echo ""
     echo "Runs the dwh-migration-dumper tool and uploads its output to provided Cloud Storage path."
     echo ""
     echo "Required Options:"
     echo "  --dumper-executable   The full path to the dumper executable."
     echo "  --gcs-base-path       The base Cloud Storage folder to upload dumper output files to. The script generates timestamped ZIP files in this folder."
     echo "  --local-base-dir      The local base directory for logs and temp files."
     echo ""
     echo "Optional Hive connection options:"
     echo "  --host              The hostname for the dumper connection."
     echo "  --port              The port number for the dumper connection."
     echo ""
     echo "To use Kerberos authentication, include the following options."
     echo "If --kerberos-authentication is specified, then --host, --port,"
     echo "--hive-kerberos-url and --hiveql-rpc-protection are all required:"
     echo ""
     echo "  --kerberos-authentication   Enable Kerberos authentication."
     echo "  --hive-kerberos-url    The Hive Kerberos URL."
     echo "  --hiveql-rpc-protection "
     echo "                            The hiveql-rpc-protection level, equal to the value of"
     echo "                            'hadoop.rpc.protection' in '/etc/hadoop/conf/core-site.xml',"
     echo "                            with one of the following values:"
     echo "                            - authentication"
     echo "                            - integrity"
     echo "                            - privacy"
     echo ""
     echo "Other Options:"
     echo "  -h, --help                  Display this help message and exit."
     exit 1
   }

   # This loop processes command-line options and overrides the default configuration.
   while [[ "$#" -gt 0 ]]; do
     case $1 in
         --dumper-executable)
             DUMPER_EXECUTABLE="$2"
             shift # past argument
             shift # past value
             ;;
         --gcs-base-path)
             GCS_BASE_PATH="$2"
             shift
             shift
             ;;
         --local-base-dir)
             LOCAL_BASE_DIR="$2"
             shift
             shift
             ;;
         --host)
             DUMPER_HOST="$2"
             shift
             shift
             ;;
         --port)
             DUMPER_PORT="$2"
             shift
             shift
             ;;
         --hive-kerberos-url)
             HIVE_KERBEROS_URL="$2"
             shift
             shift
             ;;
         --hiveql-rpc-protection)
             HIVEQL_RPC_PROTECTION="$2"
             shift
             shift
             ;;
         --kerberos-authentication)
             KERBEROS_AUTHENTICATION="true"
             shift
             ;;
         -h|--help)
             usage
             ;;
         *)
             echo "Unknown option: $1"
             usage
             ;;
     esac
   done

   # This runs AFTER parsing arguments to ensure no placeholder values are left.
   if [[ "$DUMPER_EXECUTABLE" == "DUMPER_PATH"* || "$GCS_BASE_PATH" == "gs://PATH_TO_DUMPER_OUTPUT" || "$LOCAL_BASE_DIR" == "LOCAL_BASE_DIRECTORY_PATH" ]]; then
     echo "ERROR: One or more configuration variables have not been set. Please provide them as command-line arguments or edit the script." >&2
     echo "Run with --help for more information." >&2
     exit 1
   fi

   # If Kerberos authentication is enabled, check for required fields.
   if [[ "$KERBEROS_AUTHENTICATION" == "true" ]]; then
     if [[ -z "$DUMPER_HOST" || -z "$DUMPER_PORT" || -z "$HIVE_KERBEROS_URL" || -z "$HIVEQL_RPC_PROTECTION" ]]; then
         echo "ERROR: If --kerberos-authentication is enabled, --host, --port, --hive-kerberos-url and --hiveql-rpc-protection must be provided." >&2
         echo "Run with --help for more information." >&2
         exit 1
     fi
   fi

   # Remove trailing slashes from GCS_BASE_PATH, if any.
   GCS_BASE_PATH=$(echo "${GCS_BASE_PATH}" | sed 's:/*$::')

   # Create unique timestamp and directories for this run
   EPOCH=$(date +%s)
   LOCAL_LOG_DIR="${LOCAL_BASE_DIR}/logs"
   mkdir -p "${LOCAL_LOG_DIR}" # Ensures the base and logs directories exist

   # Define the unique log and zip file path for this run
   LOG_FILE
   ```