Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 查詢外部資料表中的 Cloud Storage 資料

本文說明如何查詢儲存在 [Cloud Storage 外部資料表](https://docs.cloud.google.com/bigquery/docs/external-data-cloud-storage?hl=zh-tw)中的資料。

## 事前準備

確認您有 [Cloud Storage 外部資料表](https://docs.cloud.google.com/bigquery/docs/external-data-cloud-storage?hl=zh-tw)。

### 必要的角色

如要查詢 Cloud Storage 外部資料表，請確認您具備下列角色：

* BigQuery 資料檢視者 (`roles/bigquery.dataViewer`)
* BigQuery 使用者 (`roles/bigquery.user`)
* Storage 物件檢視者 (`roles/storage.objectViewer`)

視權限而定，您可以將這些角色授予自己，或請系統管理員授予您這些角色。如要進一步瞭解如何授予角色，請參閱「[查看可針對資源授予的角色](https://docs.cloud.google.com/iam/docs/viewing-grantable-roles?hl=zh-tw)」。

如要查看查詢外部資料表所需的確切 BigQuery 權限，請展開「Required permissions」(必要權限) 部分：

#### 所需權限

* `bigquery.jobs.create`
* `bigquery.readsessions.create` (只有在[使用 BigQuery Storage Read API 讀取資料](https://docs.cloud.google.com/bigquery/docs/reference/storage?hl=zh-tw)時才需要)
* `bigquery.tables.get`
* `bigquery.tables.getData`

您或許還可透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)取得這些權限。

## 查詢永久外部資料表

建立 Cloud Storage 外部資料表後，您可以使用 [GoogleSQL 語法查詢資料表](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw)，就像查詢標準 BigQuery 資料表一樣。例如：`SELECT field1, field2
FROM mydataset.my_cloud_storage_table;`。

## 查詢臨時外部資料表

使用臨時資料表查詢外部資料來源，對於一次性、臨時查詢外部資料，或對擷取、轉換和載入 (ETL) 處理程序而言非常有用。

如要查詢外部資料來源，但不想建立永久資料表，請提供臨時資料表的資料表定義，然後在指令或呼叫中使用該資料表定義，查詢臨時資料表。您可以透過下列任一方式提供資料表定義：

* [資料表定義檔](https://docs.cloud.google.com/bigquery/external-table-definition?hl=zh-tw)
* 內嵌結構定義
* [JSON 結構定義檔案](https://docs.cloud.google.com/bigquery/docs/schemas?hl=zh-tw#specifying_a_json_schema_file)

系統會使用資料表定義檔或提供的結構定義來建立臨時外部資料表，然後對臨時外部資料表執行查詢。

使用臨時外部資料表時，並不會在某個 BigQuery 資料集中建立資料表。因為資料表不會永久儲存在資料集中，所以無法與其他使用者分享。

您可以使用 bq 指令列工具、API 或用戶端程式庫，建立和查詢連結到外部資料來源的臨時資料表。

### bq

您可以搭配 [`--external_table_definition` 旗標](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_query_external_table_definition)使用 [`bq query`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_query) 指令，查詢已連結至外部資料來源的臨時資料表。使用 bq 指令列工具查詢連結至外部資料來源的臨時資料表時，可以透過以下項目識別資料表的結構定義：

* [資料表定義檔](https://docs.cloud.google.com/bigquery/docs/external-table-definition?hl=zh-tw) (儲存在本機)
* 內嵌結構定義
* [JSON 結構定義檔](https://docs.cloud.google.com/bigquery/docs/schemas?hl=zh-tw#specifying_a_json_schema_file) (儲存在本機)

(選用) 提供 `--location` 旗標，並將值設為您的[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)。

如要使用資料表定義檔查詢連接外部資料來源的臨時資料表，請輸入下列指令。

```
bq --location=LOCATION query \
--external_table_definition=TABLE::DEFINITION_FILE \
'QUERY'
```

更改下列內容：

* `LOCATION`：您[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)的名稱。`--location` 是選用旗標。舉例來說，如果您在東京地區使用 BigQuery，就可以將該旗標的值設定為 `asia-northeast1`。您可以使用 [.bigqueryrc 檔案](https://docs.cloud.google.com/bigquery/docs/bq-command-line-tool?hl=zh-tw#setting_default_values_for_command-line_flags)設定位置的預設值。
* `TABLE`：要建立的臨時資料表名稱。
* `DEFINITION_FILE`：本機電腦上[資料表定義檔](https://docs.cloud.google.com/bigquery/docs/external-table-definition?hl=zh-tw)的路徑。
* `QUERY`：要提交至臨時資料表的查詢。

舉例來說，下列指令會使用名為 `sales_def` 的資料表定義檔，建立及查詢名為 `sales` 的臨時資料表。

```
bq query \
--external_table_definition=sales::sales_def \
'SELECT
  Region,
  Total_sales
FROM
  sales'
```

如要使用內嵌結構定義來查詢連結至外部資料來源的臨時資料表，請輸入下列指令。

```
bq --location=LOCATION query \
--external_table_definition=TABLE::SCHEMA@SOURCE_FORMAT=BUCKET_PATH \
'QUERY'
```

更改下列內容：

* `LOCATION`：您[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)的名稱。`--location` 是選用旗標。舉例來說，如果您在東京地區使用 BigQuery，就可以將該旗標的值設定為 `asia-northeast1`。您可以使用 [.bigqueryrc 檔案](https://docs.cloud.google.com/bigquery/docs/bq-command-line-tool?hl=zh-tw#setting_default_values_for_command-line_flags)設定位置的預設值。
* `TABLE`：要建立的臨時資料表名稱。
* `SCHEMA`：內嵌結構定義，格式為 `field:data_type,field:data_type`。
* `SOURCE_FORMAT`：外部資料來源的格式，例如 `CSV`。
* `BUCKET_PATH`：包含資料表的資料的 Cloud Storage bucket 路徑，格式為 `gs://bucket_name/[folder_name/]file_pattern`。

  如要在 `file_pattern` 中選取 bucket 中的多個檔案，請在 `file_pattern` 中指定一個星號 (`*`) 萬用字元。例如：`gs://mybucket/file00*.parquet`。詳情請參閱「[Cloud Storage URI 的萬用字元支援](https://docs.cloud.google.com/bigquery/docs/external-data-cloud-storage?hl=zh-tw#wildcard-support)」。

  如要為 `uris` 選項指定多個值區，請提供多個路徑。

  以下範例顯示有效的 `uris` 值：

  + `gs://bucket/path1/myfile.csv`
  + `gs://bucket/path1/*.parquet`
  + `gs://bucket/path1/file1*`、`gs://bucket1/path1/*`

  指定以多個檔案為目標的 `uris` 值時，所有檔案都必須共用相容的結構定義。

  如要進一步瞭解如何在 BigQuery 中使用 Cloud Storage URI，請參閱「[Cloud Storage 資源路徑](https://docs.cloud.google.com/bigquery/docs/external-data-cloud-storage?hl=zh-tw#google-cloud-storage-uri)」。
* `QUERY`：要提交至臨時資料表的查詢。

舉例來說，下列指令會使用 `Region:STRING,Quarter:STRING,Total_sales:INTEGER` 結構定義，建立和查詢名為 `sales` 的臨時資料表，且此表會連結至儲存在 Cloud Storage 中的 CSV 檔案。

```
bq query \
--external_table_definition=sales::Region:STRING,Quarter:STRING,Total_sales:INTEGER@CSV=gs://mybucket/sales.csv \
'SELECT
  Region,
  Total_sales
FROM
  sales'
```

如要使用 JSON 結構定義檔來查詢連接外部資料來源的臨時資料表，請輸入下列指令。

```
bq --location=LOCATION query \
--external_table_definition=SCHEMA_FILE@SOURCE_FORMAT=BUCKET_PATH \
'QUERY'
```

更改下列內容：

* `LOCATION`：您[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)的名稱。`--location` 是選用旗標。舉例來說，如果您在東京地區使用 BigQuery，就可以將該旗標的值設定為 `asia-northeast1`。您可以使用 [.bigqueryrc 檔案](https://docs.cloud.google.com/bigquery/docs/bq-command-line-tool?hl=zh-tw#setting_default_values_for_command-line_flags)設定位置的預設值。
* `SCHEMA_FILE`：您本機上的 JSON 結構定義檔路徑。
* `SOURCE_FORMAT`：外部資料來源的格式，例如 `CSV`。
* `BUCKET_PATH`：包含資料表的資料的 Cloud Storage bucket 路徑，格式為 `gs://bucket_name/[folder_name/]file_pattern`。

  如要在 `file_pattern` 中選取 bucket 中的多個檔案，請在 `file_pattern` 中指定一個星號 (`*`) 萬用字元。例如：`gs://mybucket/file00*.parquet`。詳情請參閱「[Cloud Storage URI 的萬用字元支援](https://docs.cloud.google.com/bigquery/docs/external-data-cloud-storage?hl=zh-tw#wildcard-support)」。

  如要為 `uris` 選項指定多個值區，請提供多個路徑。

  以下範例顯示有效的 `uris` 值：

  + `gs://bucket/path1/myfile.csv`
  + `gs://bucket/path1/*.parquet`
  + `gs://bucket/path1/file1*`、`gs://bucket1/path1/*`

  指定以多個檔案為目標的 `uris` 值時，所有檔案都必須共用相容的結構定義。

  如要進一步瞭解如何在 BigQuery 中使用 Cloud Storage URI，請參閱「[Cloud Storage 資源路徑](https://docs.cloud.google.com/bigquery/docs/external-data-cloud-storage?hl=zh-tw#google-cloud-storage-uri)」。
* `QUERY`：要提交至臨時資料表的查詢。

舉例來說，下列指令會使用 `/tmp/sales_schema.json` 結構定義檔，建立和查詢名為 `sales` 的臨時資料表，且此表會連結至儲存在 Cloud Storage 中的 CSV 檔案。

```
  bq query \
  --external_table_definition=sales::/tmp/sales_schema.json@CSV=gs://mybucket/sales.csv \
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
4. 使用 [`ExternalDataConfiguration` 物件](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables?hl=zh-tw#externaldataconfiguration)填入 `JobConfigurationQuery` 物件的 `tableDefinitions` 區段。
5. 呼叫 [`jobs.insert` 方法](https://docs.cloud.google.com/bigquery/docs/reference/v2/jobs/insert?hl=zh-tw)，以非同步方式執行查詢，或呼叫 [`jobs.query` 方法](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs/query?hl=zh-tw)，以同步方式執行查詢，並傳入 `Job` 物件。

### Java

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Java 設定說明操作。詳情請參閱 [BigQuery Java API 參考說明文件](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/overview?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import com.google.cloud.bigquery.BigQuery;
import com.google.cloud.bigquery.BigQueryException;
import com.google.cloud.bigquery.BigQueryOptions;
import com.google.cloud.bigquery.CsvOptions;
import com.google.cloud.bigquery.ExternalTableDefinition;
import com.google.cloud.bigquery.Field;
import com.google.cloud.bigquery.QueryJobConfiguration;
import com.google.cloud.bigquery.Schema;
import com.google.cloud.bigquery.StandardSQLTypeName;
import com.google.cloud.bigquery.TableResult;

// Sample to queries an external data source using a temporary table
public class QueryExternalGCSTemp {

  public static void runQueryExternalGCSTemp() {
    // TODO(developer): Replace these variables before running the sample.
    String tableName = "MY_TABLE_NAME";
    String sourceUri = "gs://cloud-samples-data/bigquery/us-states/us-states.csv";
    Schema schema =
        Schema.of(
            Field.of("name", StandardSQLTypeName.STRING),
            Field.of("post_abbr", StandardSQLTypeName.STRING));
    String query = String.format("SELECT * FROM %s WHERE name LIKE 'W%%'", tableName);
    queryExternalGCSTemp(tableName, sourceUri, schema, query);
  }

  public static void queryExternalGCSTemp(
      String tableName, String sourceUri, Schema schema, String query) {
    try {
      // Initialize client that will be used to send requests. This client only needs to be created
      // once, and can be reused for multiple requests.
      BigQuery bigquery = BigQueryOptions.getDefaultInstance().getService();

      // Skip header row in the file.
      CsvOptions csvOptions = CsvOptions.newBuilder().setSkipLeadingRows(1).build();

      // Configure the external data source and query job.
      ExternalTableDefinition externalTable =
          ExternalTableDefinition.newBuilder(sourceUri, csvOptions).setSchema(schema).build();
      QueryJobConfiguration queryConfig =
          QueryJobConfiguration.newBuilder(query)
              .addTableDefinition(tableName, externalTable)
              .build();

      // Example query to find states starting with 'W'
      TableResult results = bigquery.query(queryConfig);

      results
          .iterateAll()
          .forEach(row -> row.forEach(val -> System.out.printf("%s,", val.toString())));

      System.out.println("Query on external temporary table performed successfully.");
    } catch (BigQueryException | InterruptedException e) {
      System.out.println("Query not performed \n" + e.toString());
    }
  }
}
```

### Node.js

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Node.js 設定說明操作。詳情請參閱 [BigQuery Node.js API 參考說明文件](https://googleapis.dev/nodejs/bigquery/latest/index.html)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
// Import the Google Cloud client library and create a client
const {BigQuery} = require('@google-cloud/bigquery');
const bigquery = new BigQuery();

async function queryExternalGCSTemp() {
  // Queries an external data source using a temporary table.

  const tableId = 'us_states';

  // Configure the external data source
  const externalDataConfig = {
    sourceFormat: 'CSV',
    sourceUris: ['gs://cloud-samples-data/bigquery/us-states/us-states.csv'],
    // Optionally skip header row.
    csvOptions: {skipLeadingRows: 1},
    schema: {fields: schema},
  };

  // Example query to find states starting with 'W'
  const query = `SELECT post_abbr
  FROM \`${tableId}\`
  WHERE name LIKE 'W%'`;

  // For all options, see https://cloud.google.com/bigquery/docs/reference/v2/tables#resource
  const options = {
    query,
    tableDefinitions: {[tableId]: externalDataConfig},
  };

  // Run the query as a job
  const [job] = await bigquery.createQueryJob(options);
  console.log(`Job ${job.id} started.`);

  // Wait for the query to finish
  const [rows] = await job.getQueryResults();

  // Print the results
  console.log('Rows:');
  console.log(rows);
}
```

### Python

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Python 設定說明操作。詳情請參閱 [BigQuery Python API 參考說明文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
from google.cloud import bigquery

# Construct a BigQuery client object.
client = bigquery.Client()

# Configure the external data source and query job.
external_config = bigquery.ExternalConfig("CSV")
external_config.source_uris = [
    "gs://cloud-samples-data/bigquery/us-states/us-states.csv"
]
external_config.schema = [
    bigquery.SchemaField("name", "STRING"),
    bigquery.SchemaField("post_abbr", "STRING"),
]
external_config.options.skip_leading_rows = 1
table_id = "us_states"
job_config = bigquery.QueryJobConfig(table_definitions={table_id: external_config})

# Example query to find states starting with 'W'.
sql = 'SELECT * FROM `{}` WHERE name LIKE "W%"'.format(table_id)

query_job = client.query(sql, job_config=job_config)  # Make an API request.

w_states = list(query_job)  # Wait for the job to complete.
print("There are {} states with names starting with W.".format(len(w_states)))
```

## 查詢 `_FILE_NAME` 虛擬資料欄

以外部資料來源為基礎的資料表可提供名為 `_FILE_NAME` 的虛擬資料欄。這個資料欄含有該列所屬檔案的完整路徑。此資料欄僅適用於參照儲存在 **Cloud Storage**、**Google 雲端硬碟**、**Amazon S3** 和 **Azure Blob 儲存體**中的外部資料的資料表。

系統會保留 `_FILE_NAME` 資料欄名稱，這表示您無法在任何資料表中使用該名稱建立資料欄。如要選取 `_FILE_NAME` 的值，您必須使用別名。下方範例查詢示範如何透過指派別名 `fn` 給虛擬資料欄的方式來選取 `_FILE_NAME`。

```
  bq query \
  --project_id=PROJECT_ID \
  --use_legacy_sql=false \
  'SELECT
     name,
     _FILE_NAME AS fn
   FROM
     `DATASET.TABLE_NAME`
   WHERE
     name contains "Alex"'
```

更改下列內容：

* `PROJECT_ID` 是有效的專案 ID (如果您使用 Cloud Shell，或是在 Google Cloud CLI 中設定預設專案，則此為選用標記)
* `DATASET` 是儲存永久外部資料表的資料集名稱
* `TABLE_NAME` 是永久外部資料表的名稱

如果查詢在 `_FILE_NAME` 虛擬資料欄上設有篩選述詞，BigQuery 會嘗試略過不符合篩選條件的檔案。使用 `_FILE_NAME` 虛擬資料欄建構查詢述詞時，請套用與[使用虛擬資料欄查詢擷取時間分區資料表](https://docs.cloud.google.com/bigquery/docs/querying-partitioned-tables?hl=zh-tw#query_an_ingestion-time_partitioned_table)類似的建議。

## 最佳化外部資料表查詢

使用外部資料表查詢 Cloud Storage 資料時，請考慮啟用快速快取。Rapid Cache 為 Cloud Storage 值區提供以 SSD 為基礎的可用區讀取快取，查詢外部資料表時，可望提升查詢效能並降低查詢費用。詳情請參閱「[最佳化 Cloud Storage 外部資料表查詢](https://docs.cloud.google.com/bigquery/docs/external-tables?hl=zh-tw#cloud-storage-query-optimization)」。

## 後續步驟

* 瞭解如何[在 BigQuery 中使用 SQL](https://docs.cloud.google.com/bigquery/docs/introduction-sql?hl=zh-tw)。
* 瞭解[外部資料表](https://docs.cloud.google.com/bigquery/docs/external-tables?hl=zh-tw)。
* 瞭解 [BigQuery 配額](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-09 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-09 (世界標準時間)。"],[],[]]