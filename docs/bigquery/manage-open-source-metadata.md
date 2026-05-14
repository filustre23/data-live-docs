Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 使用 BigLake metastore (傳統版) 管理開放原始碼中繼資料

**警告：** 我們不再建議使用 BigLake metastore (傳統版) 進行 Google Cloud。請改用[Lakehouse 執行階段目錄](https://docs.cloud.google.com/bigquery/docs/about-blms?hl=zh-tw)。

BigLake metastore (傳統版) 是 Google Cloud上資料分析產品的統一實體中繼資料服務。BigLake 中繼存放區 (傳統版) 提供單一中繼資料來源，方便您管理及存取多個來源的資料。資料分析師和工程師可透過 BigQuery 和 Managed Service for Apache Spark 上的各種開放資料處理引擎存取 BigLake metastore (傳統版)，因此這項服務是實用的工具。

如要管理商務中繼資料，請參閱 [Knowledge Catalog](https://docs.cloud.google.com/dataplex?hl=zh-tw)。

## BigLake Metastore (傳統版) 的運作方式

BigLake metastore (傳統版) 是無伺服器服務，使用前不必佈建資源。您可以在 Managed Service for Apache Spark 叢集中，將其做為 [Hive Metastore](https://cwiki.apache.org/confluence/display/Hive/Design#Design-Metastore) 的無伺服器替代方案。BigLake metastore (傳統版) 的運作方式與 Hive Metastore 相同，都是透過 Hive 相容的 API 運作，因此您可以在 BigQuery 中立即查詢開放格式資料表，不必執行任何其他步驟。BigLake metastore (傳統版) 僅支援 [Apache Iceberg 資料表](https://iceberg.apache.org/docs/latest/)。

BigLake metastore (傳統版) 提供 [API](https://docs.cloud.google.com/bigquery/docs/reference/biglake/rest?hl=zh-tw)、用戶端程式庫和資料引擎整合 (例如 [Apache Spark](https://spark.apache.org/))，可管理目錄、資料庫和資料表。

## 限制

BigLake Metastore (傳統版) 有下列限制：

* BigLake metastore (傳統版) 不支援 Apache Hive 資料表。
* 身分與存取權管理 (IAM) 角色和權限只能授予專案。不支援授予資源 IAM 權限。
* 不支援 [Cloud Monitoring](https://docs.cloud.google.com/monitoring?hl=zh-tw)。
* BigLake metastore (傳統版) 目錄和資料庫有以下命名限制：
  + 名稱的長度上限為 1,024 個字元。
  + 名稱只能包含 UTF-8 字母 (大寫、小寫)、數字和底線。
  + 每個專案和區域組合的名稱不得重複。
* BigLake metastore (傳統版) 資料表遵循與 BigQuery 資料表相同的命名慣例。詳情請參閱「[資料表命名](https://docs.cloud.google.com/bigquery/docs/tables?hl=zh-tw#table_naming)」。

## 事前準備

您必須先啟用計費功能和 BigLake API，才能使用 BigLake Metastore (傳統版)。

1. 請管理員授予您專案的「服務使用情形管理員」(`roles/serviceusage.serviceUsageAdmin`) IAM 角色。如要進一步瞭解如何授予角色，請參閱「[管理存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。
2. 為 Google Cloud 專案啟用計費功能。瞭解如何[檢查專案是否已啟用計費功能](https://docs.cloud.google.com/billing/docs/how-to/verify-billing-enabled?hl=zh-tw)。
3. 啟用 BigLake API。

   [啟用 API](https://console.cloud.google.com/apis/library/biglake.googleapis.com?hl=zh-tw)

## 必要的角色

* 如要完全控管 BigLake metastore (傳統版) 資源，您需要 BigLake 管理員角色 (`roles/biglake.admin`)。如果您使用 [BigQuery Spark 連接器](https://docs.cloud.google.com/dataproc/docs/tutorials/bigquery-connector-spark-example?hl=zh-tw)服務帳戶、[Managed Service for Apache Spark 服務帳戶](https://docs.cloud.google.com/dataproc-serverless/docs/concepts/service-account?hl=zh-tw)或 [Managed Service for Apache Spark VM 服務帳戶](https://docs.cloud.google.com/dataproc/docs/concepts/iam/dataproc-principals?hl=zh-tw#vm_service_account_data_plane_identity)，請將 BigLake 管理員角色授予該帳戶。
* 如要取得 BigLake Metastore (傳統版) 資源的唯讀存取權，您需要 BigLake 檢視者角色 (`roles/biglake.viewer`)。舉例來說，在 BigQuery 中查詢 BigLake Metastore (傳統版) 資料表時，使用者或 BigQuery 連線服務帳戶必須具備 BigLake 檢視者角色。
* 如要透過連線建立 BigQuery 資料表，您需要 BigQuery 連線使用者角色 (`roles/bigquery.connectionUser`)。如要進一步瞭解如何共用連線，請參閱「[與使用者共用連線](https://docs.cloud.google.com/bigquery/docs/create-cloud-resource-connection?hl=zh-tw#share_connections)」。

視用途而定，呼叫 BigLake Metastore (舊版) 的身分可以是使用者或服務帳戶：

* **使用者：**直接呼叫 BigLake API 時，或從 BigQuery 查詢 Apache Iceberg 代管資料表，但沒有連線時。在這種情況下，BigQuery 會使用使用者的憑證。
* **[BigQuery Cloud 資源連結](https://docs.cloud.google.com/bigquery/docs/create-cloud-resource-connection?hl=zh-tw)：**從 BigQuery 透過連線查詢 Iceberg 代管資料表時，BigQuery 會使用連線服務帳戶憑證存取 BigLake 中繼存放區 (傳統版)。
* **[BigQuery Spark 連接器](https://docs.cloud.google.com/bigquery/docs/connect-to-spark?hl=zh-tw)：**在 BigQuery [Spark 預存程序](https://docs.cloud.google.com/bigquery/docs/spark-procedures?hl=zh-tw)中，搭配使用 Spark 和 BigLake 中繼存放區 (傳統版) 時。Spark 會使用 Spark Connector 的服務帳戶憑證，存取 BigLake 中繼存放區 (傳統版) 並建立 BigQuery 資料表。
* **[Managed Service for Apache Spark 服務帳戶](https://docs.cloud.google.com/dataproc-serverless/docs/concepts/service-account?hl=zh-tw)：**
  在 Managed Service for Apache Spark 中使用 Spark 和 BigLake 時，Spark 會使用服務帳戶憑證。
* **[Managed Service for Apache Spark VM 服務帳戶](https://docs.cloud.google.com/dataproc/docs/concepts/iam/dataproc-principals?hl=zh-tw#vm_service_account_data_plane_identity)：**
  使用 Managed Service for Apache Spark 時 (而非 Managed Service for Apache Spark)。Apache Spark 會使用 VM 服務帳戶憑證。

視權限而定，您可以將這些角色授予自己，或請管理員授予您這些角色。如要進一步瞭解如何授予角色，請參閱「[查看可針對資源授予的角色](https://docs.cloud.google.com/iam/docs/viewing-grantable-roles?hl=zh-tw)」。

如要查看存取 BigLake Metastore (傳統版) 資源的確切必要權限，請展開「Required permissions」(必要權限) 部分：

### 所需權限

* 專案層級的 `biglake.tables.get`，適用於所有唯讀存取權。查詢 Iceberg 代管資料表
  資料表是唯讀資料表。
* 專案層級的 `biglake.{catalogs|databases|tables}.*`，適用於所有讀取和寫入權限。一般來說，Apache Spark 需要讀取及寫入資料，包括建立、管理及查看目錄、資料庫和資料表。
* 在 BigQuery 雲端資源連結層級或更高等級，建立使用連結的 Iceberg 代管資料表。`bigquery.connections.delegate`

## 連線至 BigLake metastore (傳統版)

以下各節說明如何連線至 BigLake 中繼存放區 (傳統版)。這些章節會安裝及使用 BigLake Apache Iceberg 目錄外掛程式，以下方法中的 JAR 檔案會指出該外掛程式。目錄外掛程式會從 Apache Spark 等開放原始碼引擎，連線至 BigLake metastore (傳統版)。

### 連線至 Managed Service for Apache Spark VM

如要透過 Managed Service for Apache Spark VM 連線至 BigLake metastore (傳統版)，請完成下列步驟：

1. [使用 SSH 連線至 Managed Service for Apache Spark。](https://docs.cloud.google.com/dataproc/docs/concepts/accessing/ssh?hl=zh-tw)
2. 在 [Spark SQL CLI](https://spark.apache.org/docs/latest/sql-distributed-sql-engine-spark-sql-cli.html) 中，使用下列陳述式安裝及設定 Apache Iceberg 自訂目錄，以便搭配 BigLake 中繼資料存放區 (傳統版) 使用：

   ```
   spark-sql \
     --packages ICEBERG_SPARK_PACKAGE \
     --jars BIGLAKE_ICEBERG_CATALOG_JAR \
     --conf spark.sql.catalog.SPARK_CATALOG=org.apache.iceberg.spark.SparkCatalog \
     --conf spark.sql.catalog.SPARK_CATALOG.catalog-impl=org.apache.iceberg.gcp.biglake.BigLakeCatalog \
     --conf spark.sql.catalog.SPARK_CATALOG.gcp_project=PROJECT_ID \
     --conf spark.sql.catalog.SPARK_CATALOG.gcp_location=LOCATION \
     --conf spark.sql.catalog.SPARK_CATALOG.blms_catalog=BLMS_CATALOG \
     --conf spark.sql.catalog.SPARK_CATALOG.warehouse=GCS_DATA_WAREHOUSE_FOLDER \
     --conf spark.sql.catalog.SPARK_HMS_CATALOG=org.apache.iceberg.spark.SparkCatalog \
     --conf spark.sql.catalog.SPARK_HMS_CATALOG.type=hive \
     --conf spark.sql.catalog.SPARK_HMS_CATALOG.uri=thrift://HMS_URI:9083
   ```

更改下列內容：

* `ICEBERG_SPARK_PACKAGE`：要搭配 Spark 使用的 Apache Iceberg 版本。建議使用與 [Managed Service for Apache Spark](https://docs.cloud.google.com/dataproc/docs/concepts/versioning/dataproc-version-clusters?hl=zh-tw) 或 [Managed Service for Apache Spark](https://docs.cloud.google.com/dataproc-serverless/docs/concepts/versions/spark-runtime-versions?hl=zh-tw) 執行個體中 Spark 版本相符的 Spark 版本。如要查看可用的 Apache Iceberg 版本清單，請參閱「[Apache Iceberg 下載](https://iceberg.apache.org/releases/)」。舉例來說，Apache Spark 3.3 的標記為：  
  `--packages org.apache.iceberg:iceberg-spark-runtime-3.3_2.13:1.2.1`
* `BIGLAKE_ICEBERG_CATALOG_JAR`：要安裝的 Iceberg 自訂目錄外掛程式的 Cloud Storage URI。根據您的環境，選取下列其中一個選項：
  + `Iceberg 1.9.1`：gs://spark-lib/biglake/biglake-catalog-iceberg1.9.1-0.1.3-with-dependencies.jar
  + `Iceberg 1.5.1`：gs://spark-lib/biglake/biglake-catalog-iceberg1.5.1-0.1.2-with-dependencies.jar
  + `Iceberg 1.5.0`：gs://spark-lib/biglake/biglake-catalog-iceberg1.5.0-0.1.1-with-dependencies.jar
  + `Iceberg 1.2.0`：gs://spark-lib/biglake/biglake-catalog-iceberg1.2.0-0.1.1-with-dependencies.jar
  + `Iceberg 0.14.0`：gs://spark-lib/biglake/biglake-catalog-iceberg0.14.0-0.1.1-with-dependencies.jar
* `SPARK_CATALOG`：Spark 的目錄 ID。並連結至 BigLake 中繼資料存放區 (傳統版) 目錄。
* `PROJECT_ID`：Spark 目錄連結的 BigLake Metastore (傳統版) 目錄 Google Cloud 專案 ID。
* `LOCATION`：Spark 目錄連結的 BigLake Metastore (傳統版) 目錄的 [Google Cloud 位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)。
* `BLMS_CATALOG`：Spark 目錄連結的 BigLake Metastore (傳統版) 目錄 ID。目錄不一定要存在，可以在 Spark 中建立。
* `GCS_DATA_WAREHOUSE_FOLDER`：Spark 建立所有檔案的 Cloud Storage 資料夾。開頭為 `gs://`。
* `HMS_DB`：(選用) 包含要複製資料表的 HMS 資料庫。
* `HMS_TABLE`：(選用) 要複製的 HMS 資料表。
* `HMS_URI`：(選用) HMS Thrift 端點。

### 連線至 Managed Service for Apache Spark 叢集

或者，您也可以將 Managed Service for Apache Spark 工作提交至叢集。
下列範例會安裝適當的 [Iceberg 自訂目錄](https://iceberg.apache.org/docs/latest/custom-catalog/)。

如要連線至 Managed Service for Apache Spark 叢集，請[提交工作](https://docs.cloud.google.com/dataproc/docs/guides/submit-job?hl=zh-tw)，並符合下列規格：

```
CONFS="spark.sql.catalog.SPARK_CATALOG=org.apache.iceberg.spark.SparkCatalog,"
CONFS+="spark.sql.catalog.SPARK_CATALOG.catalog-impl=org.apache.iceberg.gcp.biglake.BigLakeCatalog,"
CONFS+="spark.sql.catalog.SPARK_CATALOG.gcp_project=PROJECT_ID,"
CONFS+="spark.sql.catalog.SPARK_CATALOG.gcp_location=LOCATION,"
CONFS+="spark.sql.catalog.SPARK_CATALOG.blms_catalog=BLMS_CATALOG,"
CONFS+="spark.sql.catalog.SPARK_CATALOG.warehouse=GCS_DATA_WAREHOUSE_FOLDER,"
CONFS+="spark.jars.packages=ICEBERG_SPARK_PACKAGE"

gcloud dataproc jobs submit spark-sql --cluster=MANAGED_SERVICE_FOR_APACHE_SPARK_CLUSTER \
  --project=MANAGED_SERVICE_FOR_APACHE_SPARK_PROJECT_ID \
  --region=MANAGED_SERVICE_FOR_APACHE_SPARK_LOCATION \
  --jars=BIGLAKE_ICEBERG_CATALOG_JAR \
  --properties="${CONFS}" \
  --file=QUERY_FILE_PATH
```

更改下列內容：

* `MANAGED_SERVICE_FOR_APACHE_SPARK_CLUSTER`：要將工作[提交](https://docs.cloud.google.com/sdk/gcloud/reference/dataproc/jobs/submit/spark?hl=zh-tw)至的 Managed Service for Apache Spark 叢集。
* `MANAGED_SERVICE_FOR_APACHE_SPARK_PROJECT_ID`：Managed Service for Apache Spark 叢集的專案 ID。這個 ID 可能與 `PROJECT_ID` 不同。
* `MANAGED_SERVICE_FOR_APACHE_SPARK_LOCATION`：Managed Service for Apache Spark 叢集的位置。這個位置可能與 `LOCATION` 不同。
* `QUERY_FILE_PATH`：包含要執行查詢的檔案路徑。

### 連結至 Managed Service for Apache Spark

同樣地，您可以將批次工作負載提交至 Managed Service for Apache Spark。如要這麼做，請按照[批次工作負載操作說明](https://docs.cloud.google.com/dataproc-serverless/docs/quickstarts/spark-batch?hl=zh-tw#submit_a_spark_batch_workload)，新增下列額外旗標：

* `--properties="${CONFS}"`
* `--jars=BIGLAKE_ICEBERG_CATALOG_JAR`

### 連結至 BigQuery 預存程序

您可以使用 BigQuery 儲存程序執行 Managed Service for Apache Spark 工作。這個程序與直接在 Managed Service for Apache Spark 中執行 [Managed Service for Apache Spark](#connect-dataproc-serverless) 工作類似。

## 建立 metastore 資源

下列各節說明如何在中繼存放區中建立資源。

### 建立目錄

目錄名稱有相關限制，詳情請參閱「[限制](#limitation)」。如要建立目錄，請選取下列任一選項：

### API

使用 [`projects.locations.catalogs.create`](https://docs.cloud.google.com/bigquery/docs/reference/biglake/rest/v1/projects.locations.catalogs/create?hl=zh-tw) 方法，並指定目錄名稱。

### Spark SQL

```
CREATE NAMESPACE SPARK_CATALOG;
```

### Terraform

這會在由「google\_biglake\_catalog.default.id」變數指定的目錄中，建立名為「my\_database」的「HIVE」類型 BigLake 資料庫。詳情請參閱 [Terraform BigLake 說明文件](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/biglake_catalog)。

```
resource "google_biglake_catalog" "default" {
name     = "my_catalog"
location = "US"
}
```

### 建立資料庫

資料庫名稱有相關限制，詳情請參閱「[限制](#limitation)」。為確保資料庫資源與資料引擎相容，建議使用資料引擎建立資料庫，而非手動製作資源主體。如要建立資料庫，請選取下列任一選項：

### API

使用 [`projects.locations.catalogs.databases.create`](https://docs.cloud.google.com/bigquery/docs/reference/biglake/rest/v1/projects.locations.catalogs.databases/create?hl=zh-tw) 方法，並指定資料庫名稱。

### Spark SQL

```
CREATE NAMESPACE SPARK_CATALOG.BLMS_DB;
```

更改下列內容：

* `BLMS_DB`：要建立的 BigLake Metastore (傳統版) 資料庫 ID

### Terraform

這會在由「google\_biglake\_catalog.default.id」變數指定的目錄中，建立名為「my\_database」的「HIVE」類型 BigLake 資料庫。詳情請參閱 [Terraform BigLake 說明文件](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/biglake_catalog)。

```
resource "google_biglake_database" "default" {
name    = "my_database"
catalog = google_biglake_catalog.default.id
type    = "HIVE"
hive_options {
  location_uri = "gs://${google_storage_bucket.default.name}/${google_storage_bucket_object.metadata_directory.name}"
  parameters = {
    "owner" = "Alex"
  }
}
}
```

### 製作表格

資料表名稱有相關限制。詳情請參閱「[資料表命名](https://docs.cloud.google.com/bigquery/docs/tables?hl=zh-tw#table_naming)」。如要建立資料表，請選取下列任一選項：

### API

使用 [`projects.locations.catalogs.databases.tables.create`](https://docs.cloud.google.com/bigquery/docs/reference/biglake/rest/v1/projects.locations.catalogs.databases.tables/create?hl=zh-tw) 方法，並指定資料表名稱。

### Spark SQL

```
CREATE TABLE SPARK_CATALOG.BLMS_DB.BLMS_TABLE
  (id bigint, data string) USING iceberg;
```

更改下列內容：

* `BLMS_TABLE`：要建立的 BigLake Metastore (傳統版) 資料表 ID

### Terraform

這會在「google\_biglake\_database.default.id」變數指定的資料庫中，註冊名稱為「my\_table」且類型為「Hive」的 BigLake Metastore (傳統版) 資料表。請注意，資料表必須先存在，才能在目錄中註冊，您可以從 Apache Spark 等引擎初始化資料表，詳情請參閱 Terraform 供應商說明文件：[BigLake 資料表](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/biglake_table)。

```
resource "google_biglake_table" "default" {
name     = "my-table"
database = google_biglake_database.default.id
type     = "HIVE"
hive_options {
  table_type = "MANAGED_TABLE"
  storage_descriptor {
    location_uri  = "gs://${google_storage_bucket.default.name}/${google_storage_bucket_object.data_directory.name}"
    input_format  = "org.apache.hadoop.mapred.SequenceFileInputFormat"
    output_format = "org.apache.hadoop.hive.ql.io.HiveSequenceFileOutputFormat"
  }
  parameters = {
    "spark.sql.create.version"          = "3.1.3"
    "spark.sql.sources.schema.numParts" = "1"
    "transient_lastDdlTime"             = "1680894197"
    "spark.sql.partitionProvider"       = "catalog"
    "owner"                             = "Alex"
    "spark.sql.sources.schema.part.0" = jsonencode({
      "type" : "struct",
      "fields" : [
        { "name" : "id", "type" : "integer",
          "nullable" : true,
          "metadata" : {}
        },
        {
          "name" : "name",
          "type" : "string",
          "nullable" : true,
          "metadata" : {}
        },
        {
          "name" : "age",
          "type" : "integer",
          "nullable" : true,
          "metadata" : {}
        }
      ]
    })
    "spark.sql.sources.provider" = "iceberg"
    "provider"                   = "iceberg"
  }
}
}
```

### 端對端 Terraform 範例

這個 [GitHub 範例](https://github.com/terraform-google-modules/terraform-docs-samples/blob/main/bigquery/biglake/biglake_metastore_create_table/main.tf)提供可執行的 E2E 範例，會建立 BigLake 中繼存放區 (傳統版) 的目錄、資料庫和資料表。如要進一步瞭解如何使用這個範例，請參閱「[基本 Terraform 指令](https://cloud.google.com/docs/terraform/basic-commands?hl=zh-tw)」。

#### 將 Iceberg 資料表從 Hive Metastore 複製到 BigLake metastore (傳統版)

如要建立 Iceberg 資料表，並將 Hive Metastore 資料表複製到 BigLake metastore (傳統版)，請使用下列 Spark SQL 陳述式：

```
CREATE TABLE SPARK_CATALOG.BLMS_DB.BLMS_TABLE
  (id bigint, data string) USING iceberg
  TBLPROPERTIES(hms_table='HMS_DB.HMS_TABLE');
```

#### 將 BigLake 資料表連結至 BigLake metastore (傳統版) 資料表

在 Spark 中建立 Iceberg 資料表時，您可以選擇同時建立連結的 Iceberg 外部資料表。

##### 自動連結表格

如要在 Spark 中建立 Iceberg 資料表，並同時自動建立 Iceberg 外部資料表，請使用下列 Spark SQL 陳述式：

```
  CREATE TABLE SPARK_CATALOG.BLMS_DB.BLMS_TABLE
    (id bigint, data string) USING iceberg
    TBLPROPERTIES(bq_table='BQ_TABLE_PATH',
    bq_connection='BQ_RESOURCE_CONNECTION');
```

更改下列內容：

* `BQ_TABLE_PATH`：要建立的 Iceberg 外部資料表路徑。請採用 [BigQuery 資料表路徑語法](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#table_path)。
  如未指定專案，系統會使用與 BigLake metastore (傳統版) 目錄相同的專案。
* `BQ_RESOURCE_CONNECTION` (選用)：格式為 `project.location.connection-id`。如果指定，BigQuery 查詢會使用 [Cloud 資源連結](https://docs.cloud.google.com/bigquery/docs/create-cloud-resource-connection?hl=zh-tw#create-cloud-resource-connection)憑證存取 BigLake Metastore (傳統版)。如未指定，BigQuery 會建立一般外部資料表，而非 BigLake 資料表。

  **注意：** 您要建立資料表的 BigQuery 資料集必須已存在。這個陳述式不會建立資料集。
  BigQuery 資料集和資料表的位置必須與 BigLake 中繼存放區 (傳統版) 目錄相同。

##### 手動連結資料表

如要使用下列 BigQuery SQL 陳述式，手動建立 Iceberg 外部資料表連結，並指定 BigLake metastore (傳統版) 資料表 URI (`blms://…`)：

```
CREATE EXTERNAL TABLE 'BQ_TABLE_PATH'
  WITH CONNECTION `BQ_RESOURCE_CONNECTION`
  OPTIONS (
          format = 'ICEBERG',
          uris = ['blms://projects/PROJECT_ID/locations/LOCATION/catalogs/BLMS_CATALOG/databases/BLMS_DB/tables/BLMS_TABLE']
          )
```

## 查看 Metastore 資源

以下各節說明如何在 BigLake 中繼存放區 (傳統版) 查看資源。

### 查看目錄

如要查看目錄中的所有資料庫，請使用 [`projects.locations.catalogs.list`](https://docs.cloud.google.com/bigquery/docs/reference/biglake/rest/v1/projects.locations.catalogs/list?hl=zh-tw) 方法並指定目錄名稱。

如要查看目錄資訊，請使用 [`projects.locations.catalogs.get`](https://docs.cloud.google.com/bigquery/docs/reference/biglake/rest/v1/projects.locations.catalogs/get?hl=zh-tw) 方法並指定目錄名稱。

### 查看資料庫

如要查看資料庫，請按照下列步驟操作：

### API

如要查看資料庫中的所有資料表，請使用 [`projects.locations.catalogs.databases.list`](https://docs.cloud.google.com/bigquery/docs/reference/biglake/rest/v1/projects.locations.catalogs.databases/list?hl=zh-tw) 方法並指定資料庫名稱。

如要查看資料庫的相關資訊，請使用 [`projects.locations.catalogs.databases.get`](https://docs.cloud.google.com/bigquery/docs/reference/biglake/rest/v1/projects.locations.catalogs.databases/get?hl=zh-tw) 方法並指定資料庫名稱。

### Spark SQL

如要查看目錄中的所有資料庫，請使用下列陳述式：

```
SHOW { DATABASES | NAMESPACES } IN SPARK_CATALOG;
```

如要查看已定義資料庫的相關資訊，請使用下列陳述式：

```
DESCRIBE { DATABASE | NAMESPACE } [EXTENDED] SPARK_CATALOG.BLMS_DB;
```

### 查看資料表

如要查看資料庫中的所有資料表或定義的資料表，請按照下列步驟操作：

### API

如要查看資料庫中的所有資料表，請使用 [`projects.locations.catalogs.databases.tables.list`](https://docs.cloud.google.com/bigquery/docs/reference/biglake/rest/v1alpha1/projects.locations.catalogs.databases.tables/list?hl=zh-tw) 方法並指定資料庫名稱。

如要查看資料表資訊，請使用 [`projects.locations.catalogs.databases.tables.get`](https://docs.cloud.google.com/bigquery/docs/reference/biglake/rest/v1alpha1/projects.locations.catalogs.databases.tables/get?hl=zh-tw) 方法並指定資料表名稱。

### Spark SQL

如要查看資料庫中的所有資料表，請使用下列陳述式：

```
SHOW TABLES IN SPARK_CATALOG.BLMS_DB;
```

如要查看已定義資料表的相關資訊，請使用下列陳述式：

```
DESCRIBE TABLE [EXTENDED] SPARK_CATALOG.BLMS_DB.BLMS_TABLE;
```

## 修改 metastore 資源

下列各節說明如何修改中繼存放區中的資源。

### 更新表格

為避免多項工作嘗試同時更新同一資料表時發生衝突，BigLake 中繼資料存放區 (傳統版) 會使用樂觀鎖定。如要使用樂觀鎖定，請先使用 `GetTable` 方法取得資料表的目前版本 (稱為 *etag*)。接著，您可以變更資料表，並使用 `UpdateTable` 方法，傳入先前擷取的 etag。如果在您擷取 etag 後，有其他工作更新資料表，`UpdateTable` 方法就會失敗。這項措施可確保一次只有一項工作能更新資料表，避免發生衝突。

如要更新表格，請選取下列其中一個選項：

### API

使用 [`projects.locations.catalogs.databases.tables.patch`](https://docs.cloud.google.com/bigquery/docs/reference/biglake/rest/v1/projects.locations.catalogs.databases.tables/patch?hl=zh-tw) 方法，並指定資料表名稱。

### Spark SQL

如需 SQL 中的資料表更新選項，請參閱 [`ALTER TABLE`](https://iceberg.apache.org/docs/latest/spark-ddl/#alter-table)。

### 重新命名表格

如要重新命名表格，請選取下列其中一個選項：

### API

使用 [`projects.locations.catalogs.databases.tables.rename`](https://docs.cloud.google.com/bigquery/docs/reference/biglake/rest/v1/projects.locations.catalogs.databases.tables/rename?hl=zh-tw) 方法，並指定資料表名稱和 `newName` 值。

### Spark SQL

```
ALTER TABLE BLMS_TABLE RENAME TO NEW_BLMS_TABLE;
```

更改下列內容：

* `NEW_BLMS_TABLE`：`BLMS_TABLE` 的新名稱。必須與 `BLMS_TABLE` 位於同一個資料集。

## 刪除中繼存放區資源

下列各節將說明如何刪除 BigLake 中繼存放區 (傳統版) 的資源。

### 刪除目錄

如要刪除目錄，請選取下列其中一個選項：

### API

使用 [`projects.locations.catalogs.delete`](https://docs.cloud.google.com/bigquery/docs/reference/biglake/rest/v1/projects.locations.catalogs/delete?hl=zh-tw) 方法，並指定目錄名稱。這個方法不會刪除 Google Cloud上的相關聯檔案。

### Spark SQL

```
DROP NAMESPACE SPARK_CATALOG;
```

### 刪除資料庫

如要刪除資料庫，請選取下列其中一個選項：

### API

使用 [`projects.locations.catalogs.databases.delete`](https://docs.cloud.google.com/bigquery/docs/reference/biglake/rest/v1/projects.locations.catalogs.databases/delete?hl=zh-tw) 方法，並指定資料庫名稱。這個方法不會刪除 Google Cloud上的相關聯檔案。

### Spark SQL

```
DROP NAMESPACE SPARK_CATALOG.BLMS_DB;
```

### 刪除資料表

如要刪除表格，請選取下列其中一個選項：

### API

使用 [`projects.locations.catalogs.databases.tables.delete`](https://docs.cloud.google.com/bigquery/docs/reference/biglake/rest/v1/projects.locations.catalogs.databases.tables/delete?hl=zh-tw) 方法，並指定資料表名稱。這個方法不會刪除 Google Cloud上的相關聯檔案。

### Spark SQL

如要只捨棄資料表，請使用下列陳述式：

```
DROP TABLE SPARK_CATALOG.BLMS_DB.BLMS_TABLE;
```

如要捨棄資料表並刪除 Google Cloud上的相關聯檔案，請使用下列陳述式：

```
DROP TABLE SPARK_CATALOG.BLMS_DB.BLMS_TABLE PURGE;
```




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-14 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-14 (世界標準時間)。"],[],[]]