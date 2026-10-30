Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [參考資料](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 將 Apache Hive metastore 資料表遷移至Google Cloud

本文說明如何使用 [BigQuery 資料移轉服務](https://docs.cloud.google.com/bigquery/docs/dts-introduction?hl=zh-tw)，將 Apache Hive Metastore 代管的 Iceberg 和 Hive 資料表遷移至Google Cloud 。

BigQuery 資料移轉服務中的 Apache Hive Metastore 遷移連接器，可讓您大規模順暢地將 Hive Metastore 資料表遷移至 Google Cloud 。這項連接器支援地端部署安裝和雲端環境 (包括 Cloudera 設定) 的 Hive 和 Iceberg 資料表。Hive Metastore 遷移連接器支援儲存在下列資料來源中的檔案：

* Apache Hadoop 分散式檔案系統 (HDFS)
* Amazon Simple Storage Service (Amazon S3)
* Azure Blob 儲存體或 Azure Data Lake Storage Gen2

您可以使用 Hive Metastore 遷移連接器，將 Cloud Storage 做為檔案儲存空間，並向下列其中一個 metastore 註冊 Hive Metastore 資料表：

* [Lakehouse 執行階段目錄 Iceberg REST 目錄](https://docs.cloud.google.com/bigquery/docs/blms-rest-catalog?hl=zh-tw)

  建議您使用 Lakehouse 執行階段目錄 Iceberg REST 目錄，管理所有 Iceberg 資料。

  Lakehouse 執行階段目錄 Iceberg REST 目錄可為所有 Iceberg 資料提供單一事實來源，在查詢引擎之間建立互通性。除了 Apache Spark 和其他 OSS 引擎，您也可以使用 BigQuery 查詢資料。Lakehouse 執行階段目錄 Iceberg REST 目錄僅支援 Iceberg 資料表格式。
* [Lakehouse 執行階段目錄 Hive 目錄](https://docs.cloud.google.com/lakehouse/docs/about-spark-hive-metastore?hl=zh-tw) ([預先發布版](https://cloud.google.com/products?hl=zh-tw#product-launch-stages))

  建議您使用 Lakehouse 執行階段目錄 Hive Catalog，管理所有 Hive 資料表。

  Lakehouse 執行階段目錄 Hive 目錄可讓您使用 Hive 目錄，將遷移的 Hive 資料表註冊至 [Lakehouse 執行階段目錄](https://docs.cloud.google.com/lakehouse/docs/about-spark-hive-metastore?hl=zh-tw)。這項服務為 Apache Hive 資料表提供無伺服器 metastore。除了 Apache Spark 和其他 OSS 引擎，您也可以使用 BigQuery 查詢資料 (受格式限制)。

這個連接器支援完整轉移和僅轉移中繼資料。完整移轉會將資料和中繼資料從來源資料表移轉至目標 metastore。如果資料已在 Cloud Storage 中，且您只想將資料註冊至目的地 metastore，則可建立僅限中繼資料的移轉作業。

下圖概略說明遷移程序。

## 限制

Hive Metastore 資料表移轉作業有下列限制：

* Hive Metastore 轉移作業的 2 次排定執行作業之間，至少須間隔 30 分鐘。您仍可隨時觸發隨選執行作業。
* 檔案名稱必須符合 [Cloud Storage 物件命名規定](https://docs.cloud.google.com/storage/docs/objects?hl=zh-tw#naming)。
* Cloud Storage 的單一物件大小上限為 5 TiB。如果 Hive Metastore 資料表中的檔案超過 5 TiB，則無法移轉。
* 如果在移轉期間變更來源資料，Storage 移轉服務會採取特定行為。不建議在資料表遷移期間寫入資料表。如需其他 Storage 移轉服務限制的清單，請參閱「[已知限制](https://docs.cloud.google.com/storage-transfer/docs/known-limitations-transfer?hl=zh-tw)」。

### Lakehouse 執行階段目錄 Hive 目錄限制

使用 Lakehouse 執行階段目錄 Hive 目錄 (`BIGLAKE_HIVE_CATALOG`) 做為目的地 metastore 時，請注意下列限制和事項：

* Lakehouse 執行階段目錄 Hive 目錄 ID 只能使用小寫英文字母、數字和底線 (`_`)，不得使用破折號 (`-`) 或大寫英文字母。
* 您無法在 Google Cloud 控制台查看或管理 Lakehouse 執行階段目錄 Hive 目錄。不過，您可以在目標 BigQuery 資料集查看及查詢遷移的資料表。
* Lakehouse 執行階段目錄 Hive 目錄的所有限制，都適用於開放原始碼中繼資料格式和資料類型。
  + 如要瞭解 CSV 和 JSON 等格式的相容性，請參閱「[支援的儲存空間格式](https://docs.cloud.google.com/lakehouse/docs/spark-hive-formats-types?hl=zh-tw)」。
  + 如要瞭解不支援的資料類型 (例如 `UNION` 或巢狀陣列) 和資料欄統計資料，請參閱 [metastore 限制](https://docs.cloud.google.com/lakehouse/docs/spark-hive-limitations?hl=zh-tw#bigquery-limitations)和[分區限制](https://docs.cloud.google.com/lakehouse/docs/spark-hive-limitations?hl=zh-tw#partition-limitations)。

## 資料擷取選項

下列各節將進一步說明如何設定 Hive Metastore 移轉作業。

### 增量移轉作業

如果移轉設定設有週期性排程，後續每次移轉都會根據來源資料表的最新更新，更新 Google Cloud 上的資料表。舉例來說，所有資料更新，以及所有插入、刪除或更新作業 (包含結構定義變更)，都會在每次移轉時反映在 Google Cloud 中。

**注意：** 每次執行前，請確認中繼資料檔案反映最新狀態。建議[設定 `cron` 指令，自動定期上傳中繼資料](#automate-dumper)。

### 篩選分區

**注意：** 分區篩選器只能套用至 Hive 資料表。

您可以提供儲存在 Cloud Storage 的自訂篩選器 JSON 檔案，從 Hive 資料表移轉部分分區。排定移轉作業時，請使用 `partition_filter_gcs_path` 參數提供這個 JSON 檔案的完整 Cloud Storage 路徑。

以下是篩選器 JSON 檔案結構範例：

```
{
  "filters": [
    {
      "table": "db1.table1", "condition": "IN", "partitions":
      ["partition1=value1/partition2=value2"]
    },
    {
      "table": "db1.table2", "condition": "LESS_THAN", "partitions":
      ["partition1;value1"]
    },
    {
      "table": "db1.table3", "condition": "GREATER_THAN", "partitions":
      ["partition1;value1"]
    },
    {
      "table": "db1.table4", "condition": "RANGE", "partitions":
      ["partition1;value1;value2"]
    }
  ]
}
```

#### 篩選條件

JSON 檔案中的 `condition` 欄位支援下列值，每個值都有特定的 `partitions` 陣列格式：

* **`IN`**：指定要納入的確切分區路徑。`partitions` 陣列包含的字串，代表相對於資料表基本路徑的分區確切目錄結構 (例如 `["partition_key1=value1/partition_key2=value2"]`)。您可以在陣列中指定多個路徑。
* **`LESS_THAN`**：包含主要分區索引鍵值小於或等於指定值的分區。`partitions` 陣列必須包含單一字串，格式為 `["<partition_key>;<value>"]`。
* **`GREATER_THAN`**：包含主要分區鍵值大於或等於指定值的分區。`partitions` 陣列必須包含單一字串，格式為 `["<partition_key>;<value>"]`。
* **`RANGE`**：包含主要分區索引鍵值落在指定範圍內 (含) 的分區。`partitions` 陣列必須包含單一字串，格式為 `["<partition_key>;<start_value>;<end_value>"]`。

篩選條件須遵守下列規則和限制：

* **包含值：**`GREATER_THAN`、`LESS_THAN` 和 `RANGE` 的篩選條件包含提供的值。例如，值為
  的 `LESS_THAN` 篩選器會包含 `2023` 之前的分區 (含 `2023`)。
* **刪除分區：**如果現有的目的地分區符合分區篩選條件，且來源中不再存在，則會從目的地 metastore 中捨棄。不過，該分區的基礎資料檔案不會從 Cloud Storage 目的地 bucket 中刪除。
* **單一資料表限制：**
  + 同一個表格中不得包含多個篩選器。
  + 您無法在同一個資料表上混合使用不同的條件類型 (例如 `GREATER_THAN` 和 `IN`)。
* **目標分區資料欄：**`GREATER_THAN`、`LESS_THAN` 和 `RANGE` 等篩選條件必須指定主要分區資料欄。
* **前置字元限制：**指定的篩選器組合不得解析為每個資料表超過 1000 個前置字元。舉例來說，在依 `year/month/day` 分割的資料表上，`year>2020` 這類篩選器產生的不重複 `year=` 前置字元必須少於 1000 個。

## 事前準備

安排 Hive Metastore 移轉作業前，請先執行本節中的步驟。

### 啟用 API

在Google Cloud 專案中[啟用下列 API](https://docs.cloud.google.com/endpoints/docs/openapi/enable-api?hl=zh-tw)：

* Data Transfer API
* Storage Transfer API
* BigLake API

**注意：** 您必須啟用 BigLake API，才能使用 Lakehouse 執行階段目錄 Iceberg REST 目錄或 Lakehouse 執行階段目錄 Hive 目錄做為目的地 metastore。

啟用 Data Transfer API 時，系統會建立[服務代理](https://docs.cloud.google.com/bigquery/docs/enable-transfer-service?hl=zh-tw#service_agent)。

### 設定權限

如要設定 Hive Metastore 移轉作業的權限，請按照下列各節的步驟操作。

1. 建立移轉作業的使用者或服務帳戶應具備 BigQuery 管理員角色 (`roles/bigquery.admin`)。如果使用服務帳戶，該帳戶僅用於建立移轉作業。
2. 啟用 Data Transfer API 後，系統會建立[服務代理](https://docs.cloud.google.com/bigquery/docs/enable-transfer-service?hl=zh-tw#service_agent) (P4SA)。

   為確保服務代理具備執行 Hive Metastore 移轉作業所需的權限，請要求管理員在專案中，為服務代理授予下列 IAM 角色：

   **重要事項：**請務必將這些角色授予服務代理，*而非*您的使用者帳戶。如果未將角色授予正確的主體，可能會發生權限錯誤。
   * [Storage 移轉作業管理員](https://docs.cloud.google.com/iam/docs/roles-permissions/storagetransfer?hl=zh-tw#storagetransfer.admin)  (`roles/storagetransfer.admin`)
   * [服務使用情形消費者](https://docs.cloud.google.com/iam/docs/roles-permissions/serviceusage?hl=zh-tw#serviceusage.serviceUsageConsumer)  (`roles/serviceusage.serviceUsageConsumer`)
   * [儲存空間管理員](https://docs.cloud.google.com/iam/docs/roles-permissions/storage?hl=zh-tw#storage.admin)  (`roles/storage.admin`)
   * 如要將中繼資料遷移至 Lakehouse 執行階段目錄 (Iceberg REST 目錄或 Hive 目錄)：[BigLake 管理員](https://docs.cloud.google.com/iam/docs/roles-permissions/biglake?hl=zh-tw#biglake.admin)  (`roles/biglake.admin`)

   如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

   管理員或許也能透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)，將必要權限授予服務代理。
3. 如果您使用的是服務帳戶，請使用下列指令，將 `roles/iam.serviceAccountTokenCreator` 角色授予服務代理：

   ```
   gcloud iam service-accounts add-iam-policy-binding
   SERVICE_ACCOUNT --member
   serviceAccount:service-PROJECT_NUMBER@gcp-sa-bigquerydatatransfer.iam.gserviceaccount.com --role
   roles/iam.serviceAccountTokenCreator
   ```
4. 在專案中，將下列角色授予 Storage 移轉服務代理 (`project-PROJECT_NUMBER@storage-transfer-service.iam.gserviceaccount.com`)：

   * `roles/storage.admin`
   * 如果您是從地端部署或 HDFS 遷移，也必須授予 `roles/storagetransfer.serviceAgent` 角色。

   您也可以設定更精細的權限。詳情請參閱下列指南：

   * [HDFS 權限](https://docs.cloud.google.com/storage-transfer/docs/file-system-permissions?hl=zh-tw)
   * [Amazon S3 和 Microsoft Azure 權限](https://docs.cloud.google.com/storage-transfer/docs/iam-cloud?hl=zh-tw)

### 產生 Apache Hive 的中繼資料檔案

執行 `dwh-migration-dumper` 工具，[擷取 Apache Hive 的中繼資料](https://docs.cloud.google.com/bigquery/docs/hadoop-metadata?hl=zh-tw#apache-hive)。這項工具會產生名為 `hive-dumper-output.zip` 的檔案，可上傳至 Cloud Storage bucket。在本文件中，這個 Cloud Storage bucket 稱為 `DUMPER_BUCKET`。

您也可以使用指令碼，排定定期上傳作業。詳情請參閱「[使用 `cron` 工作自動執行轉儲工具](#automate-dumper)」。

### 設定 Storage 移轉服務

選取下列選項之一：

### HDFS

如要轉移地端部署或 HDFS 資料，必須使用 Storage 移轉代理程式。

如要設定代理，請按照下列步驟操作：

1. 在 地端部署 代理程式機器上[安裝 Docker](https://docs.cloud.google.com/storage-transfer/docs/on-prem-set-up?hl=zh-tw#install_docker)。
2. 在 Google Cloud 專案中[建立 Storage 移轉服務代理集區](https://docs.cloud.google.com/storage-transfer/docs/on-prem-agent-pools?hl=zh-tw#create-pool)。
3. 在地端部署代理程式機器上[安裝代理程式](https://docs.cloud.google.com/storage-transfer/docs/create-transfers/agent-based/hdfs?hl=zh-tw#install_agents)。

### Amazon S3

從 Amazon S3 轉移資料時，不需使用代理程式。

如要設定 Storage 移轉服務，以便移轉 Amazon S3 資料，請按照下列步驟操作：

1. [設定 AWS Amazon S3 的存取憑證](https://docs.cloud.google.com/storage-transfer/docs/source-amazon-s3?hl=zh-tw#access_credentials)。
2. 設定存取憑證後，請記下存取金鑰 ID 和私密存取金鑰。
3. 如果 AWS 專案設有 IP 限制，請將 Storage 移轉服務 worker 使用的 [IP 範圍新增](https://docs.cloud.google.com/storage-transfer/docs/source-amazon-s3?hl=zh-tw#ip_restrictions)至 IP 許可清單。

### Microsoft Azure

從 Microsoft Azure Storage 轉移資料時，不需使用代理程式。

如要設定 Storage 移轉服務，以便移轉 Microsoft Azure 儲存體，請按照下列步驟操作：

1. 為 Microsoft Azure 儲存體帳戶[產生共用存取簽章 (SAS) 權杖](https://docs.cloud.google.com/storage-transfer/docs/source-microsoft-azure?hl=zh-tw#sas-token)。
2. 產生 SAS 權杖後，請記下權杖。
3. 如果 Microsoft Azure 儲存體帳戶使用 IP 限制，請將 Storage 移轉服務 worker 使用的 [IP 範圍新增](https://docs.cloud.google.com/storage-transfer/docs/source-microsoft-azure?hl=zh-tw#ip_restrictions)至允許的 IP 清單。

## 排定 Hive Metastore 移轉作業

選取下列選項之一：

### 控制台

1. 前往 Google Cloud 控制台的「Data transfers」(資料移轉) 頁面。

   [前往「資料移轉」頁面](https://console.cloud.google.com/bigquery/transfers?hl=zh-tw)
2. 按一下「add 建立移轉作業」。
3. 在「Source type」(來源類型) 部分，從「Source」(來源) 清單中選取「Hive Metastore」。
4. 在「位置」部分，選取位置類型，然後選取區域。
5. 在「Transfer config name」(轉移設定名稱) 部分，「Display name」(顯示名稱) 請輸入資料移轉作業名稱。
6. 在「Schedule options」(排程選項) 部分執行下列操作：

   * 在「Repeat frequency」(重複頻率) 清單選取選項，指定這項資料移轉作業的執行頻率。如要指定自訂重複頻率，請選取「Custom」(自訂)。如果選取「On-demand」(隨選)，這項移轉作業會在您[手動觸發](https://docs.cloud.google.com/bigquery/docs/working-with-transfers?hl=zh-tw#manually_trigger_a_transfer)後執行。
   * 視情況選取「Start now」(立即開始) 或「Start at set time」(在所設時間開始執行)，並提供開始日期和執行時間。
7. 在「Data source details」(資料來源詳細資料) 部分執行下列操作：

   1. 在「Transfer strategy」(移轉策略) 部分，選取下列其中一個選項：
      * `FULL_TRANSFER`：移轉所有資料，並向目標 metastore 註冊中繼資料。這是預設選項。
      * `METADATA_ONLY`：僅註冊中繼資料。中繼資料參照的 Cloud Storage 位置必須已有資料。
   2. 在「Table name patterns」(資料表名稱模式)，提供資料表名稱或與 HDFS 資料庫中資料表相符的模式，指定要移轉的 HDFS 資料湖泊資料表。您必須使用 Java 規則運算式語法指定資料表模式。例如：
      * `db1..*` 會比對 db1 中的所有資料表。
      * `db1.table1;db2.table2` 與 db1 中的 table1 和 db2 中的 table2 相符。
   3. 在「BQMS discovery dump gcs path」(BQMS 探索轉儲 GCS 路徑)，輸入[建立 Apache Hive 中繼資料檔案](#generate-metadata-dump-for-apache-hive)時產生的 `hive-dumper-output.zip` 檔案路徑。如果您[搭配使用轉儲器輸出自動化功能和 `cron`](#automate-dumper)，請提供在 `--gcs-base-path` 中設定的 Cloud Storage 資料夾路徑，其中包含轉儲器輸出 ZIP 檔案。
      1. 在「Storage type」(儲存空間類型) 部分，選取下列其中一個選項。只有在「Transfer strategy」(移轉策略) 設為 `FULL_TRANSFER` 時，才能使用這個欄位：
      2. `HDFS`：如果檔案儲存空間為 `HDFS`，請選取這個選項。在「STS agent pool name」(STS 代理集區名稱) 欄位中，您必須提供[設定 Storage Transfer 代理](#configure-sts)時建立的代理集區名稱。
      3. `S3`：如果檔案儲存空間為 `Amazon S3`，請選取這個選項。在「Access key ID」(存取金鑰 ID) 和「Secret access key」(私密存取金鑰) 欄位中，您必須提供[設定存取憑證](#configure-sts)時建立的存取金鑰 ID 和私密存取金鑰。
      4. `AZURE`：如果檔案儲存空間為 `Azure Blob Storage`，請選取這個選項。在「SAS token」(SAS 權杖) 欄位中，您必須提供[設定存取憑證](#configure-sts)時建立的 SAS 權杖。
   4. 選用：在「Partition Filter gcs path」(分區篩選器 GCS 路徑) 部分，輸入自訂篩選器 JSON 檔案的完整 Cloud Storage 路徑，以便[篩選來源資料表的分區](#filter-partitions)。
   5. 在「Destination gcs path」(目的地 GCS 路徑) 中，輸入 Cloud Storage bucket 的路徑，用於儲存遷移的資料。
   6. 從下拉式選單中選擇目的地 metastore 類型：
      * `BIGLAKE_REST_CATALOG`：選取這個選項，即可將中繼資料儲存在 Lakehouse 執行階段目錄 Iceberg REST 目錄中。目錄是根據目的地 Cloud Storage bucket 建立。
      * `BIGLAKE_HIVE_CATALOG` ([預先發布版](https://cloud.google.com/products?hl=zh-tw#product-launch-stages))：選取這個選項，即可將中繼資料儲存在 Lakehouse 執行階段目錄 Hive 目錄中。您必須在「BigLake Metastore Hive Catalog ID」中提供目錄名稱。如果目錄不存在，系統會自動建立。
   7. 選用：在「Service account」(服務帳戶) 部分，輸入要用於這項資料移轉作業的服務帳戶。服務帳戶應與建立移轉設定和目的地資料集的Google Cloud 專案相同。

### bq

如要排定 Hive Metastore 移轉作業，請輸入 `bq mk` 指令，並提供移轉作業建立旗標 `--transfer_config`：

```
  bq mk --transfer_config
  --data_source=hadoop display_name='TRANSFER_NAME'
  --service_account_name='SERVICE_ACCOUNT'
```