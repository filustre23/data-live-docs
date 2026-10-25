Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 查詢 Cloud Storage BigLake 資料表

本文說明如何查詢儲存在 [Cloud Storage BigLake 資料表](https://docs.cloud.google.com/bigquery/docs/create-cloud-storage-table-biglake?hl=zh-tw)中的資料。

## 事前準備

確認您有 [Cloud Storage BigLake 資料表](https://docs.cloud.google.com/bigquery/docs/create-cloud-storage-table-biglake?hl=zh-tw)。

### 必要的角色

如要查詢 Cloud Storage BigLake 資料表，請確認您具備下列角色：

* BigQuery 資料檢視者 (`roles/bigquery.dataViewer`)
* BigQuery 使用者 (`roles/bigquery.user`)

視權限而定，您可以將這些角色授予自己，或要求管理員授予。如要進一步瞭解如何授予角色，請參閱「[查看可針對資源授予的角色](https://docs.cloud.google.com/iam/docs/viewing-grantable-roles?hl=zh-tw)」。

如要查看查詢 Cloud Storage BigLake 資料表所需的確切權限，請展開「Required permissions」(必要權限) 部分：

#### 所需權限

* `bigquery.jobs.create`
* `bigquery.readsessions.create` (只有在[使用 BigQuery Storage Read API 讀取資料](https://docs.cloud.google.com/bigquery/docs/reference/storage?hl=zh-tw)時才需要)
* `bigquery.tables.get`
* `bigquery.tables.getData`

您或許還可透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)取得這些權限

## 查詢 BigLake 資料表

建立 Cloud Storage BigLake 資料表後，您可以[使用 GoogleSQL 語法查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw)，就像查詢標準 BigQuery 資料表一樣。例如：`SELECT field1, field2 FROM mydataset.my_cloud_storage_table;`。

## 使用外部資料處理工具查詢 BigLake 資料表

您可以搭配使用 BigQuery 連接器和其他資料處理工具，存取 Cloud Storage 上的 BigLake 資料表。詳情請參閱「[連接器](https://docs.cloud.google.com/bigquery/docs/biglake-intro?hl=zh-tw#connectors)」。

### Apache Spark

以下範例使用 [Managed Service for Apache Spark](https://docs.cloud.google.com/dataproc?hl=zh-tw)，但也適用於任何使用 [Spark-BigQuery 連接器](https://docs.cloud.google.com/dataproc/docs/tutorials/bigquery-connector-spark-example?hl=zh-tw)的 Spark 部署作業。

在這個範例中，您會在[建立叢集](https://docs.cloud.google.com/dataproc/docs/guides/create-cluster?hl=zh-tw)時，提供 Spark-BigQuery 連接器做為初始化動作。這項操作可讓您使用 Zeppelin 筆記本，並執行資料分析師使用者歷程。

如要查看 Spark-BigQuery 連接器版本，請前往 GitHub 的 [GoogleCloudDataproc/spark-bigquery-connector 存放區](https://github.com/GoogleCloudDataproc/spark-bigquery-connector/releases)。

使用 Spark-BigQuery 連接器的初始化動作，建立單一節點叢集：

```
gcloud dataproc clusters create biglake-demo-cluster \
    --optional-components=ZEPPELIN \
    --region=REGION \
    --enable-component-gateway \
    --single-node \
    --initialization-actions gs://goog-dataproc-initialization-actions-REGION/connectors/connectors.sh \
    --metadata spark-bigquery-connector-url= gs://spark-lib/bigquery/spark-bigquery-with-dependencies_SCALA_VERSION-CONNECTOR_VERSION.jar
```

### Apache Hive

下列範例使用 [Managed Service for Apache Spark](https://docs.cloud.google.com/dataproc?hl=zh-tw)，但也適用於任何使用 [Hive-BigQuery 連接器](https://github.com/GoogleCloudDataproc/hive-bigquery-connector)的 Hive 部署作業。

[在本範例中，您會在
建立叢集](https://docs.cloud.google.com/dataproc/docs/guides/create-cluster?hl=zh-tw)時，提供 Hive-BigQuery 連接器做為初始化動作。

如要查看 Hive-BigQuery 連接器版本，請前往 GitHub 的 [GoogleCloudDataproc/hive-bigquery-connector 存放區](https://github.com/GoogleCloudDataproc/hive-bigquery-connector/releases)。

使用 Hive-BigQuery 連接器的初始化動作，建立單一節點叢集：

```
gcloud dataproc clusters create biglake-hive-demo-cluster \
    --region=REGION \
    --single-node \
    --initialization-actions gs://goog-dataproc-initialization-actions-REGION/connectors/connectors.sh \
    --metadata hive-bigquery-connector-url=gs://goog-dataproc-artifacts-REGION/hive-bigquery/hive-bigquery-connector-CONNECTOR_VERSION.jar
```

如要進一步瞭解 Hive-BigQuery 連接器，請參閱「[使用 Hive-BigQuery 連接器](https://docs.cloud.google.com/dataproc/docs/concepts/connectors/hive-bigquery?hl=zh-tw)」。

### Dataflow

如要從 [Dataflow](https://docs.cloud.google.com/dataflow?hl=zh-tw) 讀取 BigLake 資料表，請在 `DIRECT_READ` 模式下使用 Dataflow 連接器，以便使用 BigQuery Storage API。也支援從查詢字串讀取。請參閱 Apache Beam 說明文件中的 [BigQuery I/O](https://beam.apache.org/documentation/io/built-in/google-bigquery/)。

**注意：** Dataflow 不支援預設的 `EXPORT` 模式。

## 查詢臨時 BigLake 資料表

使用臨時資料表查詢外部資料來源，適合用於對外部資料執行一次性、臨時查詢，或用於擷取、轉換和載入 (ETL) 程序。

如要查詢外部資料來源，但不想建立永久資料表，請提供臨時資料表的資料表定義，然後在指令或呼叫中使用該資料表定義，查詢臨時資料表。您可以透過下列任一方式提供資料表定義：

* [資料表定義檔案](https://docs.cloud.google.com/bigquery/external-table-definition?hl=zh-tw)
* 內嵌結構定義
* [JSON 結構定義檔案](https://docs.cloud.google.com/bigquery/docs/schemas?hl=zh-tw#specifying_a_json_schema_file)

系統會使用資料表定義檔案或提供的結構定義，建立臨時外部資料表，並對該資料表執行查詢。

使用臨時外部資料表時，並不會在某個 BigQuery 資料集中建立資料表。由於資料表並非永久儲存在資料集中，因此無法與他人共用。

您可以使用 bq 指令列工具、API 或用戶端程式庫，建立及查詢連結至外部資料來源的臨時資料表。

### bq

使用 [`bq query`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_query) 指令，並加上 [`--external_table_definition` 旗標](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_query_external_table_definition)。

(選用) 提供 `--location` 旗標，並將值設為您的[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)。

如要使用資料表定義檔查詢連接外部資料來源的臨時資料表，請輸入下列指令。

```
bq --location=LOCATION query \
--external_table_definition=TABLE::DEFINITION_FILE \
'QUERY'
```

更改下列內容：

* `LOCATION`：[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)名稱。`--location` 是選用旗標。舉例來說，如果您在東京地區使用 BigQuery，就可以將該旗標的值設定為 `asia-northeast1`。您可以使用 [.bigqueryrc 檔案](https://docs.cloud.google.com/bigquery/docs/bq-command-line-tool?hl=zh-tw#setting_default_values_for_command-line_flags)設定位置的預設值。
* `TABLE`：要建立的臨時資料表名稱。
* `DEFINITION_FILE`：本機電腦上的[資料表定義檔案](https://docs.cloud.google.com/bigquery/docs/external-table-definition?hl=zh-tw)路徑。
* `QUERY`：您要提交至臨時資料表的查詢。

舉例來說，下列指令會使用名為 `sales_def` 的資料表定義檔，建立及查詢名為 `sales` 的臨時資料表。

```
bq query \
--external_table_definition=sales::sales_def@us.myconnection \
'SELECT
  Region,
  Total_sales
FROM
  sales'
```

如要使用內嵌結構定義來查詢連結至外部資料來源的臨時資料表，請輸入下列指令。

```
bq --location=LOCATION query \
--external_table_definition=TABLE::SCHEMA@SOURCE_FORMAT=BUCKET_PATH@projects/PROJECT_ID/locations/REGION/connections/CONNECTION_ID \
'query'
```

更改下列內容：

* `LOCATION`：[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)名稱。`--location` 是選用旗標。舉例來說，如果您在東京地區使用 BigQuery，就可以將該旗標的值設定為 `asia-northeast1`。您可以使用 [.bigqueryrc 檔案](https://docs.cloud.google.com/bigquery/docs/bq-command-line-tool?hl=zh-tw#setting_default_values_for_command-line_flags)設定位置的預設值。
* `TABLE`：要建立的臨時資料表名稱。
* `SCHEMA`：內嵌結構定義定義，格式為 `field:data_type,field:data_type`。
* `SOURCE_FORMAT`：外部資料來源的格式，例如 `CSV`。
* `BUCKET_PATH`：Cloud Storage bucket 的路徑，其中包含資料表的資料，格式為 `gs://bucket_name/[folder_name/]file_pattern`。

  您可以在 `file_pattern` 中指定一個星號 (`*`) 萬用字元，從 bucket 中選取多個檔案。例如：`gs://mybucket/file00*.parquet`。詳情請參閱「[Cloud Storage URI 的萬用字元支援](https://docs.cloud.google.com/bigquery/docs/external-data-cloud-storage?hl=zh-tw#wildcard-support)」。

  您可以提供多個路徑，為 `uris` 選項指定多個 bucket。

  以下範例顯示有效的 `uris` 值：

  + `gs://bucket/path1/myfile.csv`
  + `gs://bucket/path1/*.parquet`
  + `gs://bucket/path1/file1*`、`gs://bucket1/path1/*`

  指定多個檔案的 `uris` 值時，所有檔案都必須共用相容的結構定義。

  如要進一步瞭解如何在 BigQuery 中使用 Cloud Storage URI，請參閱「[Cloud Storage 資源路徑](https://docs.cloud.google.com/bigquery/docs/external-data-cloud-storage?hl=zh-tw#google-cloud-storage-uri)」。
* `PROJECT_ID`：連線所在的專案。
* `REGION`：連線所在的區域，例如 `us`。
* `CONNECTION_ID`：連線名稱，例如 `myconnection`。
* `QUERY`：您要提交至臨時資料表的查詢。

舉例來說，下列指令會使用 `Region:STRING,Quarter:STRING,Total_sales:INTEGER` 結構定義，建立和查詢名為 `sales` 的臨時資料表，且此表會連結至儲存在 Cloud Storage 中的 CSV 檔案。

```
bq query \
--external_table_definition=sales::Region:STRING,Quarter:STRING,Total_sales:INTEGER@CSV=gs://mybucket/sales.csv@us.myconnection \
'SELECT
  Region,
  Total_sales
FROM
  sales'
```

如要使用 JSON 結構定義檔來查詢連接外部資料來源的臨時資料表，請輸入下列指令。

```
bq --location=LOCATION query \
--external_table_definition=SCHEMA_FILE@SOURCE_FORMAT=BUCKET_PATH@projects/PROJECT_ID/locations/REGION/connections/CONNECTION_ID \
'QUERY'
```

更改下列內容：

* `LOCATION`：[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)名稱。`--location` 是選用旗標。舉例來說，如果您在東京地區使用 BigQuery，就可以將該旗標的值設定為 `asia-northeast1`。您可以使用 [.bigqueryrc 檔案](https://docs.cloud.google.com/bigquery/docs/bq-command-line-tool?hl=zh-tw#setting_default_values_for_command-line_flags)設定位置的預設值。
* `SCHEMA_FILE`：本機電腦上的 JSON 結構定義檔案路徑。
* `SOURCE_FORMAT`：外部資料來源的格式，例如 `CSV`。
* `BUCKET_PATH`：Cloud Storage bucket 的路徑，其中包含資料表的資料，格式為 `gs://bucket_name/[folder_name/]file_pattern`。

  您可以在 `file_pattern` 中指定一個星號 (`*`) 萬用字元，從 bucket 中選取多個檔案。例如：`gs://mybucket/file00*.parquet`。詳情請參閱「[Cloud Storage URI 的萬用字元支援](https://docs.cloud.google.com/bigquery/docs/external-data-cloud-storage?hl=zh-tw#wildcard-support)」。

  您可以提供多個路徑，為 `uris` 選項指定多個 bucket。

  以下範例顯示有效的 `uris` 值：

  + `gs://bucket/path1/myfile.csv`
  + `gs://bucket/path1/*.parquet`
  + `gs://bucket/path1/file1*`、`gs://bucket1/path1/*`

  指定多個檔案的 `uris` 值時，所有檔案都必須共用相容的結構定義。

  如要進一步瞭解如何在 BigQuery 中使用 Cloud Storage URI，請參閱「[Cloud Storage 資源路徑](https://docs.cloud.google.com/bigquery/docs/external-data-cloud-storage?hl=zh-tw#google-cloud-storage-uri)」。
* `PROJECT_ID`：連線所在的專案。
* `REGION`：連線所在的區域，例如 `us`。
* `CONNECTION_ID`：連線名稱，例如 `myconnection`。
* `QUERY`：您要提交至臨時資料表的查詢。

舉例來說，下列指令會使用 `/tmp/sales_schema.json` 結構定義檔，建立和查詢名為 `sales` 的臨時資料表，且此表會連結至儲存在 Cloud Storage 中的 CSV 檔案。

```
  bq query \
  --external_table_definition=sales::/tmp/sales_schema.json@CSV=gs://mybucket/sales.csv@us.myconnection \
  'SELECT
      Region,
      Total_sales
    FROM
      sales'
```

### API

如要使用 API 執行查詢，請按照下列步驟操作：

1. 建立 [`Job` 物件](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw)。
2. 使用 [`JobConfiguration` 物件](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#JobConfiguration)填入 `Job` 物件的 `configuration` 區段。
3. 使用 [`JobConfigurationQuery` 物件](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#jobconfigurationquery)填入 `JobConfiguration` 物件的 `query` 區段。
4. 使用 [`ExternalDataConfiguration` 物件](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables?hl=zh-tw#externaldataconfiguration)填入 `JobConfigurationQuery` 物件的 `tableDefinitions` 區段。在 `connectionId` 欄位中，指定要用於連線至 Cloud Storage 的連線。
5. 呼叫 [`jobs.insert` 方法](https://docs.cloud.google.com/bigquery/docs/reference/v2/jobs/insert?hl=zh-tw)以非同步方式執行查詢，或呼叫 [`jobs.query` 方法](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs/query?hl=zh-tw)以同步方式執行查詢，並傳入 `Job` 物件。

## 後續步驟

* 瞭解如何[在 BigQuery 中使用 SQL](https://docs.cloud.google.com/bigquery/docs/introduction-sql?hl=zh-tw)。
* 瞭解 [BigLake 資料表](https://docs.cloud.google.com/bigquery/docs/biglake-intro?hl=zh-tw)。
* 瞭解 [BigQuery 配額](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-10-24 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-10-24 (世界標準時間)。"],[],[]]