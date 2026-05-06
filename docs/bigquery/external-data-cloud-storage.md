Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# Cloud Storage 的外部資料表

BigQuery 可以查詢下列格式的 Cloud Storage 資料：

* 逗號分隔值 (CSV)
* JSON (以換行符號分隔)
* Avro
* ORC
* Parquet
* Datastore 匯出檔案
* Firestore 匯出

BigQuery 支援在下列[儲存空間級別](https://docs.cloud.google.com/storage/docs/storage-classes?hl=zh-tw)查詢 Cloud Storage 資料：

* 標準
* Nearline
* Coldline
* 封存

如要查詢 Cloud Storage 外部資料表，您必須同時具備外部資料表和 Cloud Storage 檔案的權限。建議您盡可能改用 [BigLake 資料表](https://docs.cloud.google.com/bigquery/docs/biglake-intro?hl=zh-tw)。BigLake 資料表提供存取權委派功能，因此您只需要 BigLake 資料表的權限，就能查詢 Cloud Storage 資料。

查詢儲存在 Cloud Storage 中的資料時，請務必[考慮資料集和 Cloud Storage 值區的位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw#data-locations)。

## 事前準備

授予身分與存取權管理 (IAM) 角色，讓使用者擁有執行本文件各項工作所需的權限。執行工作所需的權限 (如有) 會列在工作的「必要權限」部分。

## 必要的角色

如要建立外部資料表，您需要 `bigquery.tables.create`
BigQuery Identity and Access Management (IAM) 權限。

下列預先定義的 Identity and Access Management 角色都具備這項權限：

* BigQuery 資料編輯者 (`roles/bigquery.dataEditor`)
* BigQuery 資料擁有者 (`roles/bigquery.dataOwner`)
* BigQuery 管理員 (`roles/bigquery.admin`)

如要存取包含資料的 Cloud Storage 值區，您也需要下列權限：

* `storage.buckets.get`
* `storage.objects.get`
* `storage.objects.list` (如果您使用 URI [萬用字元](#wildcard-support)，則為必要目錄)

Cloud Storage Storage 管理員 (`roles/storage.admin`) 預先定義的 Identity and Access Management 角色包含這些權限。

如果您不具備上述任一角色，請要求管理員授予存取權或為您建立外部資料表。

如要進一步瞭解 BigQuery 中的 Identity and Access Management 角色和權限，請參閱「[預先定義的角色和權限](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)」。

### Compute Engine 執行個體的存取範圍

如果需要從 Compute Engine 執行個體查詢連結至 Cloud Storage 來源的外部資料表，執行個體至少須具備 Cloud Storage 唯讀[存取權範圍](https://docs.cloud.google.com/compute/docs/access/service-accounts?hl=zh-tw#accesscopesiam) (`https://www.googleapis.com/auth/devstorage.read_only`)。

這些範圍可控管 Compute Engine 執行個體對產品 (包括 Cloud Storage) 的存取權。 Google Cloud在執行個體上執行的應用程式會使用附加至執行個體的服務帳戶呼叫 Google Cloud API。

如果將 Compute Engine 執行個體設為以[預設的 Compute Engine 服務帳戶](https://docs.cloud.google.com/compute/docs/access/service-accounts?hl=zh-tw#default_service_account)執行，則該執行個體預設會獲得多個[預設範圍](https://docs.cloud.google.com/compute/docs/access/service-accounts?hl=zh-tw#default_scopes)，包括 `https://www.googleapis.com/auth/devstorage.read_only` 範圍。

如果您改為使用自訂服務帳戶設定執行個體，請務必明確授予執行個體 `https://www.googleapis.com/auth/devstorage.read_only` 範圍。

如要瞭解如何為 Compute Engine 執行個體套用範圍，請參閱「[變更執行個體的服務帳戶與存取範圍](https://docs.cloud.google.com/compute/docs/access/create-enable-service-accounts-for-instances?hl=zh-tw#changeserviceaccountandscopes)」。如要進一步瞭解 Compute Engine 服務帳戶，請參閱[服務帳戶](https://docs.cloud.google.com/compute/docs/access/service-accounts?hl=zh-tw)一文。

## 在未分區資料上建立外部資料表

您可以透過下列方式建立已連結至外部資料來源的永久資料表：

* 使用 Google Cloud 控制台
* 使用 [`bq mk`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_mk) 指令
* 在使用 [`tables.insert`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables/insert?hl=zh-tw) API 方法時建立 [`ExternalDataConfiguration`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables?hl=zh-tw#externaldataconfiguration)
* 執行[`CREATE EXTERNAL TABLE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#create_external_table_statement)資料定義語言 (DDL) 陳述式。
* 使用用戶端程式庫

選取下列選項之一：

### 控制台

1. 前往「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。

   如果沒有看到左側窗格，請按一下 last\_page「Expand left pane」(展開左側窗格)，開啟窗格。
3. 在「Explorer」窗格中展開專案，按一下「Datasets」(資料集)，然後選取資料集。
4. 展開「動作」more\_vert選項，然後按一下「建立資料表」。
5. 在「來源」部分，指定下列詳細資料：

   1. 在「Create table from」(使用下列資料建立資料表) 區段，選取「Google Cloud Storage」
   2. 在「Select file from GCS bucket or use a URI pattern」(從 GCS bucket 選取檔案或使用 URI 模式) 中，瀏覽並選取要使用的 bucket 和檔案，或輸入 `gs://bucket_name/[folder_name/]file_name` 格式的路徑。

      您無法在 Google Cloud 控制台中指定多個 URI，但可以指定一個星號 (`*`) 萬用字元，選取多個檔案。例如：`gs://mybucket/file_name*`。詳情請參閱「[Cloud Storage URI 的萬用字元支援](https://docs.cloud.google.com/bigquery/docs/external-data-cloud-storage?hl=zh-tw#wildcard-support)」。

      Cloud Storage 值區的位置必須與要建立的資料表所在的資料集位置相同。
   3. 在「File format」(檔案格式) 部分，選取與檔案相符的格式。
6. 在「目的地」部分，指定下列詳細資料：

   1. 在「Project」(專案) 部分，選擇要在其中建立資料表的專案。
   2. 在「Dataset」(資料集) 部分，選擇要建立資料表的資料集。
   3. 在「Table」(資料表) 中，輸入要建立的資料表名稱。
   4. 在「Table type」(資料表類型) 中，選取「External table」(外部資料表)。
7. 在「Schema」(結構定義) 區段中，您可以啟用[結構定義自動偵測](https://docs.cloud.google.com/bigquery/docs/schema-detect?hl=zh-tw)功能，也可以手動指定結構定義 (如有來源檔案)。如果沒有來源檔案，就必須手動指定結構定義。

   * 如要啟用結構定義自動偵測功能，請選取「自動偵測」選項。
   * 如要手動指定結構定義，請取消勾選「自動偵測」選項。啟用「以文字形式編輯」，然後以 [JSON 陣列](https://docs.cloud.google.com/bigquery/docs/schemas?hl=zh-tw#specifying_a_json_schema_file)的形式輸入資料表結構定義。
8. 如要忽略含有與結構定義不符之額外資料欄值的資料列，請展開「進階選項」部分，然後選取「不明的值」。
9. 點選「建立資料表」。

建立永久資料表後，您就可以把這個資料表當做原生 BigQuery 資料表一樣執行查詢。查詢完成後，可以[匯出結果](https://docs.cloud.google.com/bigquery/docs/writing-results?hl=zh-tw)為 CSV 或 JSON 檔案、將結果儲存為資料表，或將結果儲存至 Google 試算表。

### SQL

您可以執行 [`CREATE EXTERNAL TABLE` DDL 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#create_external_table_statement)，建立永久外部資料表。您可以明確指定結構定義，也可以使用[結構定義自動偵測](https://docs.cloud.google.com/bigquery/docs/schema-detect?hl=zh-tw)功能，從外部資料推斷結構定義。

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列陳述式：

   ```
   CREATE EXTERNAL TABLE `PROJECT_ID.DATASET.EXTERNAL_TABLE_NAME`
     OPTIONS (
       format ="TABLE_FORMAT",
       uris = ['BUCKET_PATH'[,...]]
       );
   ```

   請替換下列項目：

   * `PROJECT_ID`：要在其中建立資料表的專案名稱，例如 `myproject`
   * `DATASET`：您要在其中建立資料表的 BigQuery 資料集名稱，例如 `mydataset`
   * `EXTERNAL_TABLE_NAME`：要建立的資料表名稱，例如 `mytable`
   * `TABLE_FORMAT`：要建立的資料表格式，例如 `PARQUET`
   * `BUCKET_PATH`：包含外部資料表資料的 Cloud Storage 值區路徑，格式為 `['gs://bucket_name/[folder_name/]file_name']`。

     如要在路徑中指定一個星號 (`*`) 萬用字元，即可從 bucket 選取多個檔案。例如，`['gs://mybucket/file_name*']`。詳情請參閱「[Cloud Storage URI 的萬用字元支援](https://docs.cloud.google.com/bigquery/docs/external-data-cloud-storage?hl=zh-tw#wildcard-support)」。

     如要為 `uris` 選項指定多個值區，請提供多個路徑。

     以下範例顯示有效的 `uris` 值：

     + `['gs://bucket/path1/myfile.csv']`
     + `['gs://bucket/path1/*.csv']`
     + `['gs://bucket/path1/*', 'gs://bucket/path2/file00*']`

     指定以多個檔案為目標的 `uris` 值時，所有這些檔案都必須共用相容的結構定義。

     如要進一步瞭解如何在 BigQuery 中使用 Cloud Storage URI，請參閱[Cloud Storage 資源路徑](https://docs.cloud.google.com/bigquery/docs/external-data-cloud-storage?hl=zh-tw#google-cloud-storage-uri)。
3. 按一下「執行」play\_circle。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

**範例**

以下範例會使用結構定義自動偵測功能，建立名為 `sales` 的外部資料表，且此表會連結至儲存在 Cloud Storage 中的 CSV 檔案：

```
CREATE OR REPLACE EXTERNAL TABLE mydataset.sales
  OPTIONS (
  format = 'CSV',
  uris = ['gs://mybucket/sales.csv']);
```

下一個範例會明確指定結構定義，並略過 CSV 檔案中的第一列：

```
CREATE OR REPLACE EXTERNAL TABLE mydataset.sales (
  Region STRING,
  Quarter STRING,
  Total_Sales INT64
) OPTIONS (
    format = 'CSV',
    uris = ['gs://mybucket/sales.csv'],
    skip_leading_rows = 1);
```

### bq

如要建立外部資料表，請使用 [`bq mk` 指令](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_mk)並加上 [`--external_table_definition`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#external_table_definition_flag) 旗標。這個標記包含[資料表定義檔](https://docs.cloud.google.com/bigquery/docs/external-table-definition?hl=zh-tw)的路徑，或是內嵌資料表定義。

**選項 1：資料表定義檔**

使用 [`bq mkdef`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_mkdef) 指令建立資料表定義檔，然後將檔案路徑傳遞至 `bq mk` 指令，如下所示：

```
bq mkdef --source_format=SOURCE_FORMAT \
  BUCKET_PATH > DEFINITION_FILE

bq mk --table \
  --external_table_definition=DEFINITION_FILE \
  DATASET_NAME.TABLE_NAME \
  SCHEMA
```

更改下列內容：

* `SOURCE_FORMAT`：外部資料來源的格式。
  例如：`CSV`。
* `BUCKET_PATH`：包含資料表的資料的 Cloud Storage bucket 路徑，格式為 `gs://bucket_name/[folder_name/]file_pattern`。

  如要在 `file_pattern` 中選取 bucket 中的多個檔案，請在 `file_pattern` 中指定一個星號 (`*`) 萬用字元。例如：`gs://mybucket/file00*.parquet`。詳情請參閱「[Cloud Storage URI 的萬用字元支援](https://docs.cloud.google.com/bigquery/docs/external-data-cloud-storage?hl=zh-tw#wildcard-support)」。

  如要為 `uris` 選項指定多個值區，請提供多個路徑。

  以下範例顯示有效的 `uris` 值：

  + `gs://bucket/path1/myfile.csv`
  + `gs://bucket/path1/*.parquet`
  + `gs://bucket/path1/file1*`、`gs://bucket1/path1/*`

  指定以多個檔案為目標的 `uris` 值時，所有檔案都必須共用相容的結構定義。

  如要進一步瞭解如何在 BigQuery 中使用 Cloud Storage URI，請參閱「[Cloud Storage 資源路徑](https://docs.cloud.google.com/bigquery/docs/external-data-cloud-storage?hl=zh-tw#google-cloud-storage-uri)」。
* `DEFINITION_FILE`：本機上[資料表定義檔](https://docs.cloud.google.com/bigquery/docs/external-table-definition?hl=zh-tw)的路徑。
* `DATASET_NAME`：包含資料表的資料集名稱。
* `TABLE_NAME`：您要建立的資料表名稱。
* `SCHEMA`：指定 [JSON 結構定義檔](https://docs.cloud.google.com/bigquery/docs/schemas?hl=zh-tw#specifying_a_json_schema_file)的路徑，或以 `field:data_type,field:data_type,...` 形式指定結構定義。

範例：

```
bq mkdef --source_format=CSV gs://mybucket/sales.csv > mytable_def

bq mk --table --external_table_definition=mytable_def \
  mydataset.mytable \
  Region:STRING,Quarter:STRING,Total_sales:INTEGER
```

如要使用結構定義自動偵測功能，請在 `mkdef` 指令中設定 `--autodetect=true` 標記，並省略結構定義：

```
bq mkdef --source_format=CSV --autodetect=true \
  gs://mybucket/sales.csv > mytable_def

bq mk --table --external_table_definition=mytable_def \
  mydataset.mytable
```

**選項 2：內嵌表格定義**

您可以直接將資料表定義傳遞至 `bq mk` 指令，不必建立資料表定義檔：

```
bq mk --table \
  --external_table_definition=@SOURCE_FORMAT=BUCKET_PATH \
  DATASET_NAME.TABLE_NAME \
  SCHEMA
```

更改下列內容：

* `SOURCE_FORMAT`：外部資料來源的格式

  例如 `CSV`。
* `BUCKET_PATH`：包含資料表的資料的 Cloud Storage bucket 路徑，格式為 `gs://bucket_name/[folder_name/]file_pattern`。

  如要在 `file_pattern` 中選取 bucket 中的多個檔案，請在 `file_pattern` 中指定一個星號 (`*`) 萬用字元。例如：`gs://mybucket/file00*.parquet`。詳情請參閱「[Cloud Storage URI 的萬用字元支援](https://docs.cloud.google.com/bigquery/docs/external-data-cloud-storage?hl=zh-tw#wildcard-support)」。

  如要為 `uris` 選項指定多個值區，請提供多個路徑。

  以下範例顯示有效的 `uris` 值：

  + `gs://bucket/path1/myfile.csv`
  + `gs://bucket/path1/*.parquet`
  + `gs://bucket/path1/file1*`、`gs://bucket1/path1/*`

  指定以多個檔案為目標的 `uris` 值時，所有檔案都必須共用相容的結構定義。

  如要進一步瞭解如何在 BigQuery 中使用 Cloud Storage URI，請參閱「[Cloud Storage 資源路徑](https://docs.cloud.google.com/bigquery/docs/external-data-cloud-storage?hl=zh-tw#google-cloud-storage-uri)」。
* `DATASET_NAME`：包含該資料表的資料集名稱。
* `TABLE_NAME`：您要建立的資料表名稱。
* `SCHEMA`：指定 [JSON 結構定義檔](https://docs.cloud.google.com/bigquery/docs/schemas?hl=zh-tw#specifying_a_json_schema_file)的路徑，或以 `field:data_type,field:data_type,...` 形式指定結構定義。如要使用結構定義自動偵測功能，請省略這個引數。

範例：

```
bq mkdef --source_format=CSV gs://mybucket/sales.csv > mytable_def
bq mk --table --external_table_definition=mytable_def \
  mydataset.mytable \
  Region:STRING,Quarter:STRING,Total_sales:INTEGER
```

### API

呼叫 [`tables.insert` 方法](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables/insert?hl=zh-tw) API 方法，並在您傳入的 [`Table` 資源](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables?hl=zh-tw#Table)中建立 [`ExternalDataConfiguration`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables?hl=zh-tw#externaldataconfiguration)。

指定 `schema` 屬性，或將 `autodetect` 屬性設為 `true`，為支援的資料來源啟用結構定義自動偵測功能。

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
import com.google.cloud.bigquery.TableId;
import com.google.cloud.bigquery.TableInfo;
import com.google.cloud.bigquery.TableResult;

// Sample to queries an external data source using a permanent table
public class QueryExternalGCSPerm {

  public static void runQueryExternalGCSPerm() {
    // TODO(developer): Replace these variables before running the sample.
    String datasetName = "MY_DATASET_NAME";
    String tableName = "MY_TABLE_NAME";
    String sourceUri = "gs://cloud-samples-data/bigquery/us-states/us-states.csv";
    Schema schema =
        Schema.of(
            Field.of("name", StandardSQLTypeName.STRING),
            Field.of("post_abbr", StandardSQLTypeName.STRING));
    String query =
        String.format("SELECT * FROM %s.%s WHERE name LIKE 'W%%'", datasetName, tableName);
    queryExternalGCSPerm(datasetName, tableName, sourceUri, schema, query);
  }

  public static void queryExternalGCSPerm(
      String datasetName, String tableName, String sourceUri, Schema schema, String query) {
    try {
      // Initialize client that will be used to send requests. This client only needs to be created
      // once, and can be reused for multiple requests.
      BigQuery bigquery = BigQueryOptions.getDefaultInstance().getService();

      // Skip header row in the file.
      CsvOptions csvOptions = CsvOptions.newBuilder().setSkipLeadingRows(1).build();

      TableId tableId = TableId.of(datasetName, tableName);
      // Create a permanent table linked to the GCS file
      ExternalTableDefinition externalTable =
          ExternalTableDefinition.newBuilder(sourceUri, csvOptions).setSchema(schema).build();
      bigquery.create(TableInfo.of(tableId, externalTable));

      // Example query to find states starting with 'W'
      TableResult results = bigquery.query(QueryJobConfiguration.of(query));

      results
          .iterateAll()
          .forEach(row -> row.forEach(val -> System.out.printf("%s,", val.toString())));

      System.out.println("Query on external permanent table performed successfully.");
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

async function queryExternalGCSPerm() {
  // Queries an external data source using a permanent table

  /**
   * TODO(developer): Uncomment the following lines before running the sample.
   */
  // const datasetId = "my_dataset";
  // const tableId = "my_table";

  // Configure the external data source
  const dataConfig = {
    sourceFormat: 'CSV',
    sourceUris: ['gs://cloud-samples-data/bigquery/us-states/us-states.csv'],
    // Optionally skip header row
    csvOptions: {skipLeadingRows: 1},
  };

  // For all options, see https://cloud.google.com/bigquery/docs/reference/v2/tables#resource
  const options = {
    schema: schema,
    externalDataConfiguration: dataConfig,
  };

  // Create an external table linked to the GCS file
  const [table] = await bigquery
    .dataset(datasetId)
    .createTable(tableId, options);

  console.log(`Table ${table.id} created.`);

  // Example query to find states starting with 'W'
  const query = `SELECT post_abbr
  FROM \`${datasetId}.${tableId}\`
  WHERE name LIKE 'W%'`;

  // Run the query as a job
  const [job] = await bigquery.createQueryJob(query);
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

# TODO(developer): Set table_id to the ID of the table to create.
table_id = "your-project.your_dataset.your_table_name"

# TODO(developer): Set the external source format of your table.
# Note that the set of allowed values for external data sources is
# different than the set used for loading data (see :class:`~google.cloud.bigquery.job.SourceFormat`).
external_source_format = "AVRO"

# TODO(developer): Set the source_uris to point to your data in Google Cloud
source_uris = [
    "gs://cloud-samples-data/bigquery/federated-formats-reference-file-schema/a-twitter.avro",
    "gs://cloud-samples-data/bigquery/federated-formats-reference-file-schema/b-twitter.avro",
    "gs://cloud-samples-data/bigquery/federated-formats-reference-file-schema/c-twitter.avro",
]

# Create ExternalConfig object with external source format
external_config = bigquery.ExternalConfig(external_source_format)
# Set source_uris that point to your data in Google Cloud
external_config.source_uris = source_uris

# TODO(developer) You have the option to set a reference_file_schema_uri, which points to
# a reference file for the table schema
reference_file_schema_uri = "gs://cloud-samples-data/bigquery/federated-formats-reference-file-schema/b-twitter.avro"

external_config.reference_file_schema_uri = reference_file_schema_uri

table = bigquery.Table(table_id)
# Set the external data configuration of the table
table.external_data_configuration = external_config
table = client.create_table(table)  # Make an API request.

print(
    f"Created table with external source format {table.external_data_configuration.source_format}"
)
```

## 在分區資料上建立外部資料表

您可以為 Cloud Storage 中的 Hive 分區資料建立外部資料表。建立外部分區資料表後，您就無法變更分區鍵。如要變更分割區鍵，您必須重新建立資料表。

如要為 Hive 分區資料建立外部資料表，請選擇下列其中一個選項：

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往 BigQuery](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中展開專案，按一下「Datasets」(資料集)，然後選取資料集。
4. 按一下「動作」more\_vert，然後點選「建立資料表」。系統會開啟「建立資料表」窗格。
5. 在「來源」部分，指定下列詳細資料：

1. 在「Create table from」(使用下列資料建立資料表) 部分，選取「Google Cloud Storage」。
2. 在「Select file from Cloud Storage bucket」(從 Cloud Storage 值區選取檔案)  中，使用[萬用字元](https://docs.cloud.google.com/bigquery/docs/batch-loading-data?hl=zh-tw#load-wildcards)輸入 Cloud Storage 資料夾的路徑。例如：`my_bucket/my_files*`。Cloud Storage 值區的位置必須與要建立、附加或覆寫的資料表所在的資料集位置相同。
3. 從「檔案格式」清單中選取檔案類型。
4. 選取「來源資料分割」核取方塊，然後在「選取來源 URI 前置字元」中輸入 Cloud Storage URI 前置字元。例如：`gs://my_bucket/my_files`。
5. 在「Partition inference mode」(分割區推論模式) 部分中，選取下列其中一個選項：
   * **自動推斷類型**：將分區結構定義偵測模式設為 `AUTO`。
   * **將所有資料欄視為字串**：將分區結構定義偵測模式設為 `STRINGS`。
   * **提供我自己的**：將分區結構定義偵測模式設為 `CUSTOM`，然後手動輸入分區鍵的結構定義資訊。詳情請參閱「[提供自訂分區索引鍵結構定義](https://docs.cloud.google.com/bigquery/docs/hive-partitioned-loads-gcs?hl=zh-tw#custom_partition_key_schema)」。
6. 選用：如要要求所有查詢都必須使用分區篩選器，請選取「Require partition filter」(需要分區篩選器) 核取方塊。使用分區篩選器可以降低成本並提升效能。詳情請參閱「[在查詢中對分區鍵強制使用述詞篩選器](https://docs.cloud.google.com/bigquery/docs/hive-partitioned-queries-gcs?hl=zh-tw#requiring_predicate_filters_on_partition_keys_in_queries)」。

6. 在「目的地」部分，指定下列詳細資料：
   1. 在「Project」(專案) 部分，選取要在其中建立資料表的專案。
   2. 在「Dataset」(資料集) 部分，選取要建立資料表的資料集。
   3. 在「Table」(資料表) 中，輸入要建立的資料表名稱。
   4. 在「Table type」(資料表類型) 部分，選取「External table」(外部資料表)。
7. 在「Schema」(結構定義) 區段中，輸入[結構定義](https://docs.cloud.google.com/bigquery/docs/schemas?hl=zh-tw)。
8. 如要啟用結構定義[自動偵測](https://docs.cloud.google.com/bigquery/docs/schema-detect?hl=zh-tw)功能，請選取「自動偵測」。
9. 如要忽略含多餘資料欄值 (與結構定義不符) 的資料列，請展開「進階選項」部分，然後選取「不明的值」。
10. 點選「建立資料表」。

### SQL

使用 [`CREATE EXTERNAL TABLE`DDL 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#create_external_table_statement)。

以下範例使用 Hive 分區索引鍵的自動偵測功能：

```
CREATE EXTERNAL TABLE `PROJECT_ID.DATASET.EXTERNAL_TABLE_NAME`
WITH PARTITION COLUMNS
OPTIONS (
format = 'SOURCE_FORMAT',
uris = ['GCS_URIS'],
hive_partition_uri_prefix = 'GCS_URI_SHARED_PREFIX',
require_hive_partition_filter = BOOLEAN);
```

更改下列內容：

* `SOURCE_FORMAT`：外部資料來源的格式，例如 `PARQUET`
* `GCS_URIS`：Cloud Storage 資料夾的路徑，使用萬用字元格式
* `GCS_URI_SHARED_PREFIX`：不含萬用字元的來源 URI 前置字串
* `BOOLEAN`：是否要在查詢時要求述詞篩選器。這個標記是選用的，預設值為 `false`。

下列範例會在 `WITH PARTITION COLUMNS` 子句中列出自訂 Hive 分區索引鍵和類型：

```
CREATE EXTERNAL TABLE `PROJECT_ID.DATASET.EXTERNAL_TABLE_NAME`
WITH PARTITION COLUMNS (PARTITION_COLUMN_LIST)
OPTIONS (
format = 'SOURCE_FORMAT',
uris = ['GCS_URIS'],
hive_partition_uri_prefix = 'GCS_URI_SHARED_PREFIX',
require_hive_partition_filter = BOOLEAN);
```

更改下列內容：

* `PARTITION_COLUMN_LIST`：資料欄清單，順序與 Cloud Storage 資料夾路徑相同，格式如下：

```
KEY1 TYPE1, KEY2 TYPE2
```

下列範例會建立外部分區資料表。這項指令會使用結構定義自動偵測功能，偵測檔案結構定義和 Hive 分割版面配置。如果外部路徑為 `gs://bucket/path/field_1=first/field_2=1/data.parquet`，系統會將分區資料欄偵測為 `field_1` (`STRING`) 和 `field_2` (`INT64`)。

```
CREATE EXTERNAL TABLE dataset.AutoHivePartitionedTable
WITH PARTITION COLUMNS
OPTIONS (
uris = ['gs://bucket/path/*'],
format = 'PARQUET',
hive_partition_uri_prefix = 'gs://bucket/path',
require_hive_partition_filter = false);
```

下列範例會明確指定分區資料欄，建立外部分區資料表。這個範例假設外部檔案路徑的模式為 `gs://bucket/path/field_1=first/field_2=1/data.parquet`。

```
CREATE EXTERNAL TABLE dataset.CustomHivePartitionedTable
WITH PARTITION COLUMNS (
field_1 STRING, -- column order must match the external path
field_2 INT64)
OPTIONS (
uris = ['gs://bucket/path/*'],
format = 'PARQUET',
hive_partition_uri_prefix = 'gs://bucket/path',
require_hive_partition_filter = false);
```

### bq

首先，請使用 [`bq mkdef`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_mkdef) 指令建立資料表定義檔：

```
bq mkdef \
--source_format=SOURCE_FORMAT \
--hive_partitioning_mode=PARTITIONING_MODE \
--hive_partitioning_source_uri_prefix=GCS_URI_SHARED_PREFIX \
--require_hive_partition_filter=BOOLEAN \
 GCS_URIS > DEFINITION_FILE
```

更改下列內容：

* `SOURCE_FORMAT`：外部資料來源的格式。例如：`CSV`。
* `PARTITIONING_MODE`：Hive 分區模式。請使用下列其中一個值：
  + `AUTO`：自動偵測索引鍵名稱和類型。
  + `STRINGS`：自動將鍵名轉換為字串。
  + `CUSTOM`：在來源 URI 前置字串中編碼索引鍵結構定義。
* `GCS_URI_SHARED_PREFIX`：來源 URI 前置字串。
* `BOOLEAN`：指定是否要在查詢時要求述詞篩選器。這個標記是選用的，預設值為 `false`。
* `GCS_URIS`：Cloud Storage 資料夾的路徑，使用萬用字元格式。
* `DEFINITION_FILE`：本機電腦上[資料表定義檔](https://docs.cloud.google.com/bigquery/external-table-definition?hl=zh-tw)的路徑。

如果 `PARTITIONING_MODE` 為 `CUSTOM`，請在來源 URI 前置字串中加入分區索引鍵結構定義，格式如下：

```
--hive_partitioning_source_uri_prefix=GCS_URI_SHARED_PREFIX/{KEY1:TYPE1}/{KEY2:TYPE2}/...
```

建立資料表定義檔後，請使用 [`bq mk`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#mk-table) 指令建立外部資料表：

```
bq mk --external_table_definition=DEFINITION_FILE \
DATASET_NAME.TABLE_NAME \
SCHEMA
```

更改下列內容：

* `DEFINITION_FILE`：資料表定義檔的路徑。
* `DATASET_NAME`：包含資料表的資料集名稱。
* `TABLE_NAME`：您要建立的資料表名稱。
* `SCHEMA`：指定 [JSON 結構定義檔](https://docs.cloud.google.com/bigquery/docs/schemas?hl=zh-tw#specifying_a_json_schema_file)的路徑，或以 `field:data_type,field:data_type,...` 形式指定結構定義。如要使用結構定義自動偵測功能，請省略這個引數。

**範例**

以下範例使用 `AUTO` Hive 分割模式：

```
bq mkdef --source_format=CSV \
  --hive_partitioning_mode=AUTO \
  --hive_partitioning_source_uri_prefix=gs://myBucket/myTable \
  gs://myBucket/myTable/* > mytable_def

bq mk --external_table_definition=mytable_def \
  mydataset.mytable \
  Region:STRING,Quarter:STRING,Total_sales:INTEGER
```

以下範例使用 `STRING` Hive 分割模式：

```
bq mkdef --source_format=CSV \
  --hive_partitioning_mode=STRING \
  --hive_partitioning_source_uri_prefix=gs://myBucket/myTable \
  gs://myBucket/myTable/* > mytable_def

bq mk --external_table_definition=mytable_def \
  mydataset.mytable \
  Region:STRING,Quarter:STRING,Total_sales:INTEGER
```

以下範例使用 `CUSTOM` Hive 分割模式：

```
bq mkdef --source_format=CSV \
  --hive_partitioning_mode=CUSTOM \
  --hive_partitioning_source_uri_prefix=gs://myBucket/myTable/{dt:DATE}/{val:STRING} \
  gs://myBucket/myTable/* > mytable_def

bq mk --external_table_definition=mytable_def \
  mydataset.mytable \
  Region:STRING,Quarter:STRING,Total_sales:INTEGER
```

### API

如要使用 BigQuery API 設定 Hive 分區，請在建立[資料表定義檔](https://docs.cloud.google.com/bigquery/external-table-definition?hl=zh-tw)時，將 [hivePartitioningOptions](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables?hl=zh-tw#hivepartitioningoptions) 物件納入 [ExternalDataConfiguration](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables?hl=zh-tw#externaldataconfiguration) 物件。

如果將 `hivePartitioningOptions.mode` 欄位設為 `CUSTOM`，則必須在 `hivePartitioningOptions.sourceUriPrefix` 欄位中編碼分區索引鍵結構定義，如下所示：`gs://BUCKET/PATH_TO_TABLE/{KEY1:TYPE1}/{KEY2:TYPE2}/...`

如要在查詢時強制使用述詞篩選器，請將 `hivePartitioningOptions.requirePartitionFilter` 欄位設為 `true`。

### Java

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Java 設定說明操作。詳情請參閱 [BigQuery Java API 參考說明文件](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/overview?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import com.google.cloud.bigquery.BigQuery;
import com.google.cloud.bigquery.BigQueryException;
import com.google.cloud.bigquery.BigQueryOptions;
import com.google.cloud.bigquery.ExternalTableDefinition;
import com.google.cloud.bigquery.FormatOptions;
import com.google.cloud.bigquery.HivePartitioningOptions;
import com.google.cloud.bigquery.TableId;
import com.google.cloud.bigquery.TableInfo;

// Sample to create external table using hive partitioning
public class SetHivePartitioningOptions {

  public static void main(String[] args) {
    // TODO(developer): Replace these variables before running the sample.
    String datasetName = "MY_DATASET_NAME";
    String tableName = "MY_TABLE_NAME";
    String sourceUri = "gs://cloud-samples-data/bigquery/hive-partitioning-samples/customlayout/*";
    String sourceUriPrefix =
        "gs://cloud-samples-data/bigquery/hive-partitioning-samples/customlayout/{pkey:STRING}/";
    setHivePartitioningOptions(datasetName, tableName, sourceUriPrefix, sourceUri);
  }

  public static void setHivePartitioningOptions(
      String datasetName, String tableName, String sourceUriPrefix, String sourceUri) {
    try {
      // Initialize client that will be used to send requests. This client only needs to be created
      // once, and can be reused for multiple requests.
      BigQuery bigquery = BigQueryOptions.getDefaultInstance().getService();

      // Configuring partitioning options
      HivePartitioningOptions hivePartitioningOptions =
          HivePartitioningOptions.newBuilder()
              .setMode("CUSTOM")
              .setRequirePartitionFilter(true)
              .setSourceUriPrefix(sourceUriPrefix)
              .build();

      TableId tableId = TableId.of(datasetName, tableName);
      ExternalTableDefinition customTable =
          ExternalTableDefinition.newBuilder(sourceUri, FormatOptions.parquet())
              .setAutodetect(true)
              .setHivePartitioningOptions(hivePartitioningOptions)
              .build();
      bigquery.create(TableInfo.of(tableId, customTable));
      System.out.println("External table created using hivepartitioningoptions");
    } catch (BigQueryException e) {
      System.out.println("External table was not created" + e.toString());
    }
  }
}
```

## 查詢外部資料表

詳情請參閱「[在外部資料表中查詢 Cloud Storage 資料](https://docs.cloud.google.com/bigquery/docs/query-cloud-storage-data?hl=zh-tw)」一文。

## 將外部資料表升級為 BigLake

將外部資料表連結至連線，即可將以 Cloud Storage 為基礎的資料表升級為 BigLake 資料表。如要搭配 BigLake 資料表使用[中繼資料快取](https://docs.cloud.google.com/bigquery/docs/biglake-intro?hl=zh-tw#metadata_caching_for_performance)，可以同時指定相關設定。如要取得資料表詳細資料 (例如來源格式和來源 URI)，請參閱「[取得資料表資訊](https://docs.cloud.google.com/bigquery/docs/tables?hl=zh-tw#get_table_information)」。

如要將外部資料表更新為 BigLake 資料表，請選取下列其中一個選項：

### SQL

使用 [`CREATE OR REPLACE EXTERNAL TABLE` DDL 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#create_external_table_statement)更新資料表：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列陳述式：

   ```
   CREATE OR REPLACE EXTERNAL TABLE
     `PROJECT_ID.DATASET.EXTERNAL_TABLE_NAME`
     WITH CONNECTION {`REGION.CONNECTION_ID` | DEFAULT}
     OPTIONS(
       format ="TABLE_FORMAT",
       uris = ['BUCKET_PATH'],
       max_staleness = STALENESS_INTERVAL,
       metadata_cache_mode = 'CACHE_MODE'
       );
   ```

   請替換下列項目：

   * `PROJECT_ID`：包含資料表的專案名稱
   * `DATASET`：包含資料表的資料集名稱
   * `EXTERNAL_TABLE_NAME`：資料表名稱
   * `REGION`：包含連線的區域
   * `CONNECTION_ID`：要使用的連線名稱

     如要使用[預設連線](https://docs.cloud.google.com/bigquery/docs/default-connections?hl=zh-tw)，請指定 `DEFAULT`，而非包含 `REGION.CONNECTION_ID` 的連線字串。
   * `TABLE_FORMAT`：資料表使用的格式

     更新資料表時無法變更這項設定。
   * `BUCKET_PATH`：包含外部資料表資料的 Cloud Storage 值區路徑，格式為 `['gs://bucket_name/[folder_name/]file_name']`。

     如要在路徑中指定一個星號 (`*`) 萬用字元，即可從 bucket 選取多個檔案。例如，`['gs://mybucket/file_name*']`。詳情請參閱「[Cloud Storage URI 的萬用字元支援](https://docs.cloud.google.com/bigquery/docs/external-data-cloud-storage?hl=zh-tw#wildcard-support)」。

     如要為 `uris` 選項指定多個值區，請提供多個路徑。

     以下範例顯示有效的 `uris` 值：

     + `['gs://bucket/path1/myfile.csv']`
     + `['gs://bucket/path1/*.csv']`
     + `['gs://bucket/path1/*', 'gs://bucket/path2/file00*']`

     指定以多個檔案為目標的 `uris` 值時，所有這些檔案都必須共用相容的結構定義。

     如要進一步瞭解如何在 BigQuery 中使用 Cloud Storage URI，請參閱[Cloud Storage 資源路徑](https://docs.cloud.google.com/bigquery/docs/external-data-cloud-storage?hl=zh-tw#google-cloud-storage-uri)。
   * `STALENESS_INTERVAL`：指定對資料表執行的作業是否使用快取中繼資料，以及快取中繼資料必須有多新，作業才能使用

     如要進一步瞭解中繼資料快取注意事項，請參閱「[中繼資料快取，提升效能](https://docs.cloud.google.com/bigquery/docs/biglake-intro?hl=zh-tw#metadata_caching_for_performance)」。

     如要停用中繼資料快取功能，請指定 0。這是目前的預設做法。

     如要啟用中繼資料快取功能，請指定介於 30 分鐘至 7 天之間的[間隔常值](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/lexical?hl=zh-tw#interval_literals)。舉例來說，如要指定 4 小時的過時間隔，請輸入 `INTERVAL 4 HOUR`。如果資料表在過去 4 小時內重新整理過，針對該資料表執行的作業就會使用快取中繼資料。如果快取中繼資料的建立時間較早，作業就會改為從 Cloud Storage 擷取中繼資料。
   * `CACHE_MODE`：指定中繼資料快取是否自動或手動重新整理

     如要進一步瞭解中繼資料快取注意事項，請參閱「[中繼資料快取，提升效能](https://docs.cloud.google.com/bigquery/docs/biglake-intro?hl=zh-tw#metadata_caching_for_performance)」。

     設為 `AUTOMATIC`，中繼資料快取就會以系統定義的時間間隔 (通常介於 30 到 60 分鐘之間) 重新整理。

     如要依您決定的時間表重新整理中繼資料快取，請設為 `MANUAL`。在這種情況下，您可以呼叫 [`BQ.REFRESH_EXTERNAL_METADATA_CACHE` 系統程序](https://docs.cloud.google.com/bigquery/docs/reference/system-procedures?hl=zh-tw#bqrefresh_external_metadata_cache)來重新整理快取。

     如果 `STALENESS_INTERVAL` 設為大於 0 的值，您就必須設定 `CACHE_MODE`。
3. 按一下「執行」play\_circle。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

### bq

使用 [`bq mkdef`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_mkdef) 和 [`bq update`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_update) 指令更新資料表：

1. 產生[外部資料表定義](https://docs.cloud.google.com/bigquery/external-table-definition?hl=zh-tw#table-definition)，說明要變更的資料表層面：

   ```
   bq mkdef --connection_id=PROJECT_ID.REGION.CONNECTION_ID \
   --source_format=TABLE_FORMAT \
   --metadata_cache_mode=CACHE_MODE \
   "BUCKET_PATH" > /tmp/DEFINITION_FILE
   ```

   更改下列內容：

   * `PROJECT_ID`：包含連線的專案名稱
   * `REGION`：包含連線的區域
   * `CONNECTION_ID`：要使用的連線名稱
   * `TABLE_FORMAT`：資料表使用的格式。更新資料表時無法變更這項設定。
   * `CACHE_MODE`：指定中繼資料快取是否自動或手動重新整理。如要進一步瞭解中繼資料快取考量事項，請參閱「[中繼資料快取提升效能](https://docs.cloud.google.com/bigquery/docs/biglake-intro?hl=zh-tw#metadata_caching_for_performance)」一文。

     設為 `AUTOMATIC`，中繼資料快取就會以系統定義的時間間隔重新整理，通常介於 30 到 60 分鐘之間。

     如要依您決定的時間表重新整理中繼資料快取，請設為 `MANUAL`。在這種情況下，您可以呼叫 [`BQ.REFRESH_EXTERNAL_METADATA_CACHE` 系統程序](https://docs.cloud.google.com/bigquery/docs/reference/system-procedures?hl=zh-tw#bqrefresh_external_metadata_cache)來重新整理快取。

     如果 `STALENESS_INTERVAL` 設為大於 0 的值，就必須設定 `CACHE_MODE`。
   * `BUCKET_PATH`：Cloud Storage bucket 的路徑，其中包含外部資料表的資料，格式為 `gs://bucket_name/[folder_name/]file_name`。

     如要在路徑中指定一個星號 (`*`) 萬用字元，可以限制從值區選取的檔案。例如，`gs://mybucket/file_name*`。詳情請參閱「[Cloud Storage URI 的萬用字元支援](https://docs.cloud.google.com/bigquery/docs/external-data-cloud-storage?hl=zh-tw#wildcard-support)」。

     如要為 `uris` 選項指定多個值區，請提供多個路徑。

     以下範例顯示有效的 `uris` 值：

     + `gs://bucket/path1/myfile.csv`
     + `gs://bucket/path1/*.csv`
     + `gs://bucket/path1/*,gs://bucket/path2/file00*`

     指定以多個檔案為目標的 `uris` 值時，所有檔案都必須共用相容的結構定義。

     如要進一步瞭解如何在 BigQuery 中使用 Cloud Storage URI，請參閱「[Cloud Storage 資源路徑](https://docs.cloud.google.com/bigquery/docs/external-data-cloud-storage?hl=zh-tw#google-cloud-storage-uri)」。
   * `DEFINITION_FILE`：您要建立的資料表定義檔名稱。
2. 使用新的外部資料表定義更新資料表：

   ```
   bq update --max_staleness=STALENESS_INTERVAL \
   --external_table_definition=/tmp/DEFINITION_FILE \
   PROJECT_ID:DATASET.EXTERNAL_TABLE_NAME
   ```

   更改下列內容：

   * `STALENESS_INTERVAL`：指定對資料表執行的作業是否使用快取中繼資料，以及作業必須使用多新的快取中繼資料。如要進一步瞭解中繼資料快取注意事項，請參閱「[中繼資料快取，提升效能](https://docs.cloud.google.com/bigquery/docs/biglake-intro?hl=zh-tw#metadata_caching_for_performance)」。

     如要停用中繼資料快取功能，請指定 0。這是目前的預設做法。

     如要啟用中繼資料快取，請使用[`INTERVAL` 資料類型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#interval_type)文件所述的 `Y-M D H:M:S` 格式，指定 30 分鐘到 7 天之間的間隔值。舉例來說，如要指定 4 小時的過時間隔，請輸入 `0-0 0 4:0:0`。如果資料表在過去 4 小時內重新整理過，針對該資料表執行的作業就會使用快取中繼資料。如果快取中繼資料較舊，作業會改為從 Cloud Storage 擷取中繼資料。
   * `DEFINITION_FILE`：您建立或更新的資料表定義檔案名稱。
   * `PROJECT_ID`：包含資料表的專案名稱
   * `DATASET`：含有資料表的資料集名稱
   * `EXTERNAL_TABLE_NAME`：資料表名稱。

## Cloud Storage 資源路徑

根據 Cloud Storage 資料來源建立外部資料表時，您必須提供資料路徑。

Cloud Storage 資源路徑包含您的值區名稱和物件 (檔名)。舉例來說，如果 Cloud Storage bucket 名為 `mybucket`，資料檔案名為 `myfile.csv`，則資源路徑為 `gs://mybucket/myfile.csv`。

BigQuery 不支援 Cloud Storage 資源路徑在初始雙斜線後還有多個連續斜線。Cloud Storage 物件名稱可以包含多個連續的斜線 (「/」) 字元，但 BigQuery 會將多個連續斜線轉換為一個斜線。舉例來說，下列資源路徑在 Cloud Storage 中有效，但在 BigQuery 中則無效：`gs://bucket/my//object//name`。

如要擷取 Cloud Storage 資源路徑，請按照下列步驟操作：

1. 開啟 Cloud Storage 主控台。

   [Cloud Storage 主控台](https://console.cloud.google.com/storage/browser?hl=zh-tw)
2. 瀏覽至含有來源資料的物件 (檔案) 位置。
3. 按一下物件名稱。

   「物件詳細資料」頁面隨即開啟。
4. 複製「gsutil URI」欄位中提供的值，開頭為 `gs://`。

**附註：** 您也可以使用 [`gcloud storage ls`](https://docs.cloud.google.com/sdk/gcloud/reference/storage/ls?hl=zh-tw) 指令列出值區或物件。

### Cloud Storage URI 的萬用字元支援

如果資料分成多個檔案，可以使用星號 (\*) 萬用字元選取多個檔案。使用星號萬用字元時，必須遵守下列規則：

* 星號可以出現在物件名稱內或物件名稱的末端。
* 系統不支援使用多個星號。例如，`gs://mybucket/fed-*/temp/*.csv` 是無效的路徑。
* 系統不支援在 bucket 名稱中使用星號。

範例：

* 以下範例說明如何選取所有資料夾中，開頭為前置字元 `gs://mybucket/fed-samples/fed-sample` 的所有檔案：

  ```
  gs://mybucket/fed-samples/fed-sample*
  ```
* 以下範例說明如何只選取名為 `fed-samples` 的資料夾和 `fed-samples` 的任何子資料夾中，副檔名為 `.csv` 的檔案：

  ```
  gs://mybucket/fed-samples/*.csv
  ```
* 以下範例說明如何在名為 `fed-samples` 的資料夾中，選取命名模式為 `fed-sample*.csv` 的檔案。這個範例不會選取 `fed-samples` 子資料夾中的檔案。

  ```
  gs://mybucket/fed-samples/fed-sample*.csv
  ```

使用 bq 指令列工具時，您可能需要在某些平台上逸出星號。

建立連結至 Datastore 或 Firestore 匯出檔案的外部資料表時，無法使用星號萬用字元。

## 定價

系統會針對 BigQuery 要求收取下列 Cloud Storage 擷取與資料移轉費用：

* Nearline、Coldline 和 Archive Storage 級別的擷取費用會按照現有的[定價說明文件](https://cloud.google.com/storage/pricing?hl=zh-tw#retrieval-pricing)和[擷取 SKU](https://docs.cloud.google.com/bigquery/docs/skus?filter=95FF-2EF5-5EA1+Retrieval&%3Bcurrency=USD&hl=zh-tw) 計費。
* 如果某個位置的 BigQuery 工作讀取儲存在其他位置 Cloud Storage bucket 中的資料，則系統會收取[跨區域網路資料移轉費用](https://cloud.google.com/storage/pricing?hl=zh-tw#network-buckets)。這類費用會計入下列 SKU：
  + Google Cloud 在第 1 洲和第 2 洲之間的儲存空間資料移轉。舉例來說，如要將資料從 `us-central1` 移轉至 `europe-west1`，請參閱「[Google Cloud Storage Data Transfer between Northern America and Europe](https://docs.cloud.google.com/bigquery/docs/skus?currency=USD&%3Bfilter=C7FF-4F9E-C0DB&%3Be=48754805&hl=zh-tw)」。
  + 網路資料移轉 Google Cloud 同一洲內的跨區域。舉例來說，如要將資料從 `us-east4` 移轉至 `US`，請參閱「[北美洲地區 GCP 跨區域網路資料移轉 Google Cloud](https://docs.cloud.google.com/bigquery/docs/skus?currency=USD&%3Bfilter=8878-37D4-D2AC&%3Be=48754805&hl=zh-tw) 」。

## 限制

如要瞭解外部資料表的限制，請參閱「[外部資料表限制](https://docs.cloud.google.com/bigquery/docs/external-tables?hl=zh-tw#limitations)」。

## 後續步驟

* 瞭解[外部資料表](https://docs.cloud.google.com/bigquery/docs/external-tables?hl=zh-tw)。
* 瞭解 [BigLake 資料表](https://docs.cloud.google.com/bigquery/docs/biglake-intro?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-06 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-06 (世界標準時間)。"],[],[]]