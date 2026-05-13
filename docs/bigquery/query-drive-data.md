Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 查詢雲端硬碟資料

本文說明如何查詢儲存在 [Google 雲端硬碟外部資料表](https://docs.cloud.google.com/bigquery/docs/external-data-drive?hl=zh-tw)中的資料。

BigQuery 同時支援查詢個人雲端硬碟檔案和共用檔案。如要進一步瞭解雲端硬碟，請參閱「[Google 雲端硬碟訓練課程和相關說明](https://support.google.com/a/users/answer/9282958?hl=zh-tw)」。

您可以透過[永久外部資料表](#permanent-tables)或[臨時外部資料表](#temporary-tables)查詢雲端硬碟資料，臨時外部資料表會在您執行查詢時建立。

## 限制

如要瞭解外部資料表的相關限制，請參閱[外部資料表限制](https://docs.cloud.google.com/bigquery/docs/external-tables?hl=zh-tw#limitations)。

## 必要的角色

如要查詢雲端硬碟外部資料表，請確認您具備下列角色：

* BigQuery 資料檢視者 (`roles/bigquery.dataViewer`)
* BigQuery 使用者 (`roles/bigquery.user`)

視權限而定，您可以將這些角色授予自己，或請系統管理員授予您這些角色。如要進一步瞭解如何授予角色，請參閱「[查看可針對資源授予的角色](https://docs.cloud.google.com/iam/docs/viewing-grantable-roles?hl=zh-tw)」。

如要查看查詢外部資料表所需的確切 BigQuery 權限，請展開「Required permissions」(必要權限) 部分：

#### 所需權限

* `bigquery.jobs.create`
* `bigquery.readsessions.create` (只有在[使用 BigQuery Storage Read API 讀取資料](https://docs.cloud.google.com/bigquery/docs/reference/storage?hl=zh-tw)時才需要)
* `bigquery.tables.get`
* `bigquery.tables.getData`

您或許還可透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)取得這些權限。

## 雲端硬碟權限

您至少必須擁有連結至外部資料表之 Google 雲端硬碟檔案的 [`View`](https://support.google.com/drive/answer/2494822?co=GENIE.Platform%3DDesktop&hl=zh-tw) 權限，才能查詢 Google 雲端硬碟中的外部資料。

## Compute Engine 執行個體的範圍

建立 Compute Engine 執行個體時，您可以指定執行個體的範圍清單。這個範圍會控管執行個體對 Google Cloud產品 (包含雲端硬碟) 的存取權。在 VM 上執行的應用程式會使用服務帳戶呼叫 Google Cloud API。

如果將 Compute Engine 執行個體設為以[服務帳戶](https://docs.cloud.google.com/compute/docs/access/create-enable-service-accounts-for-instances?hl=zh-tw)的形式執行，且這個服務帳戶會存取連結至雲端硬碟資料來源的外部資料表，則您必須為執行個體新增 [雲端硬碟的 OAuth 範圍](https://developers.google.com/identity/protocols/googlescopes?hl=zh-tw#drivev3) (`https://www.googleapis.com/auth/drive.readonly`)。

如需為 Compute Engine 執行個體套用範圍的相關資訊，請參閱[變更執行個體的服務帳戶與存取權範圍](https://docs.cloud.google.com/compute/docs/access/create-enable-service-accounts-for-instances?hl=zh-tw#changeserviceaccountandscopes)一節。如要進一步瞭解 Compute Engine 服務帳戶，請參閱[服務帳戶](https://docs.cloud.google.com/compute/docs/access/service-accounts?hl=zh-tw)一文。

## 使用永久外部資料表查詢雲端硬碟資料

建立雲端硬碟外部資料表後，您可以使用 [GoogleSQL 語法查詢資料表](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw)，就像查詢標準 BigQuery 資料表一樣。例如：`SELECT field1, field2
FROM mydataset.my_drive_table;`。

## 使用臨時資料表查詢雲端硬碟資料

使用臨時資料表查詢外部資料來源，對於一次性、臨時查詢外部資料，或對擷取、轉換和載入 (ETL) 處理程序而言非常有用。

如要查詢外部資料來源，但不想建立永久資料表，請提供臨時資料表的資料表定義，然後在指令或呼叫中使用該資料表定義，查詢臨時資料表。您可以透過下列任一方式提供資料表定義：

* [資料表定義檔](https://docs.cloud.google.com/bigquery/external-table-definition?hl=zh-tw)
* 內嵌結構定義
* [JSON 結構定義檔案](https://docs.cloud.google.com/bigquery/docs/schemas?hl=zh-tw#specifying_a_json_schema_file)

系統會使用資料表定義檔或提供的結構定義來建立臨時外部資料表，然後對臨時外部資料表執行查詢。

使用臨時外部資料表時，並不會在某個 BigQuery 資料集中建立資料表。因為資料表不會永久儲存在資料集中，所以無法與其他使用者分享。

### 建立及查詢臨時資料表

您可以使用 bq 指令列工具、API 或用戶端程式庫，建立和查詢連結到外部資料來源的臨時資料表。

### bq

您可以搭配 `--external_table_definition` 旗標使用 `bq query` 指令，查詢已連結至外部資料來源的臨時資料表。使用 bq 指令列工具查詢連結至外部資料來源的臨時資料表時，可以透過以下項目識別資料表的結構定義：

* [資料表定義檔](https://docs.cloud.google.com/bigquery/external-table-definition?hl=zh-tw) (儲存在本機)
* 內嵌結構定義
* JSON 結構定義檔 (儲存在本機)

如要使用資料表定義檔查詢已連結至外部資料來源的臨時資料表，請輸入下列指令。

```
bq --location=LOCATION query \
--external_table_definition=TABLE::DEFINITION_FILE \
'QUERY'
```

其中：

* `LOCATION` 是您的[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)。`--location` 是選用旗標。
* `TABLE` 是要建立的臨時資料表名稱。
* `DEFINITION_FILE` 是本機電腦上[資料表定義檔](https://docs.cloud.google.com/bigquery/external-table-definition?hl=zh-tw)的路徑。
* `QUERY` 是要提交至臨時資料表的查詢。

舉例來說，下列指令會使用名為 `sales_def` 的資料表定義檔，建立及查詢名為 `sales` 的臨時資料表。

```
bq query \
--external_table_definition=sales::sales_def \
'SELECT
   Region,Total_sales
 FROM
   sales'
```

如要使用內嵌結構定義來查詢連結至外部資料來源的臨時資料表，請輸入下列指令。

```
bq --location=LOCATION query \
--external_table_definition=TABLE::SCHEMA@SOURCE_FORMAT=DRIVE_URI \
'QUERY'
```

其中：

* `LOCATION` 是您的[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)。`--location` 是選用旗標。
* `TABLE` 是要建立的臨時資料表名稱。
* `SCHEMA` 是結構定義，格式為 `FIELD:DATA_TYPE,FIELD:DATA_TYPE`。
* `SOURCE_FORMAT` 為 `CSV`、`NEWLINE_DELIMITED_JSON`、`AVRO` 或 `GOOGLE_SHEETS`。
* `DRIVE_URI` 是您的 [雲端硬碟 URI](#drive-uri)。
* `QUERY` 是要提交至臨時資料表的查詢。

舉例來說，下列指令會使用 `Region:STRING,Quarter:STRING,Total_sales:INTEGER` 結構定義，建立和查詢名為 `sales` 的臨時資料表，且此表會連結至儲存在雲端硬碟中的 CSV 檔案。

```
bq --location=US query \
--external_table_definition=sales::Region:STRING,Quarter:STRING,Total_sales:INTEGER@CSV=https://drive.google.com/open?id=1234_AbCD12abCd \
'SELECT
   Region,Total_sales
 FROM
   sales'
```

如要使用 JSON 結構定義檔來查詢連接外部資料來源的臨時資料表，請輸入下列指令。

```
bq --location=LOCATION query \
--external_table_definition=SCHEMA_FILE@SOURCE_FORMT=DRIVE_URI \
'QUERY'
```

其中：

* `LOCATION` 是您的[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)。`--location` 是選用旗標。
* `SCHEMA_FILE` 是您本機上的 JSON 結構定義檔路徑。
* `SOURCE_FILE` 為 `CSV`、`NEWLINE_DELIMITED_JSON`、`AVRO` 或 `GOOGLE_SHEETS`。
* `DRIVE_URI` 是您的 [雲端硬碟 URI](#drive-uri)。
* `QUERY` 是要提交至臨時資料表的查詢。

舉例來說，下列指令會使用 `/tmp/sales_schema.json` 結構定義檔，建立和查詢名為 `sales` 的臨時資料表，且此表會連結至儲存在雲端硬碟中的 CSV 檔案。

```
bq query \
--external_table_definition=sales::/tmp/sales_schema.json@CSV=https://drive.google.com/open?id=1234_AbCD12abCd \
'SELECT
   Total_sales
 FROM
   sales'
```

### API

* 建立[查詢工作設定](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#jobconfigurationquery)。如需有關呼叫 [`jobs.query`](https://docs.cloud.google.com/bigquery/docs/reference/v2/jobs/query?hl=zh-tw) 和 [`jobs.insert`](https://docs.cloud.google.com/bigquery/docs/reference/v2/jobs/insert?hl=zh-tw) 的資訊，請參閱[查詢資料](https://docs.cloud.google.com/bigquery/querying-data?hl=zh-tw)的相關說明。
* 建立 [`ExternalDataConfiguration`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables?hl=zh-tw#externaldataconfiguration) 以指定外部資料來源。

### Python

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Python 設定說明操作。詳情請參閱 [BigQuery Python API 參考說明文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
from google.cloud import bigquery
import google.auth

# Create credentials with Drive & BigQuery API scopes.
# Both APIs must be enabled for your project before running this code.
credentials, project = google.auth.default(
    scopes=[
        "https://www.googleapis.com/auth/drive",
        "https://www.googleapis.com/auth/bigquery",
    ]
)

# Construct a BigQuery client object.
client = bigquery.Client(credentials=credentials, project=project)

# Configure the external data source and query job.
external_config = bigquery.ExternalConfig("GOOGLE_SHEETS")

# Use a shareable link or grant viewing access to the email address you
# used to authenticate with BigQuery (this example Sheet is public).
sheet_url = (
    "https://docs.google.com/spreadsheets"
    "/d/1i_QCL-7HcSyUZmIbP9E6lO_T5u3HnpLe7dnpHaijg_E/edit?usp=sharing"
)
external_config.source_uris = [sheet_url]
external_config.schema = [
    bigquery.SchemaField("name", "STRING"),
    bigquery.SchemaField("post_abbr", "STRING"),
]
external_config.options.skip_leading_rows = 1  # Optionally skip header row.
external_config.options.range = (
    "us-states!A20:B49"  # Optionally set range of the sheet to query from.
)
table_id = "us_states"
job_config = bigquery.QueryJobConfig(table_definitions={table_id: external_config})

# Example query to find states starting with "W".
sql = 'SELECT * FROM `{}` WHERE name LIKE "W%"'.format(table_id)

query_job = client.query(sql, job_config=job_config)  # Make an API request.

# Wait for the query to complete.
w_states = list(query_job)
print(
    "There are {} states with names starting with W in the selected range.".format(
        len(w_states)
    )
)
```

### Java

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Java 設定說明操作。詳情請參閱 [BigQuery Java API 參考說明文件](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/overview?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import com.google.auth.oauth2.GoogleCredentials;
import com.google.auth.oauth2.ServiceAccountCredentials;
import com.google.cloud.bigquery.BigQuery;
import com.google.cloud.bigquery.BigQueryException;
import com.google.cloud.bigquery.BigQueryOptions;
import com.google.cloud.bigquery.ExternalTableDefinition;
import com.google.cloud.bigquery.Field;
import com.google.cloud.bigquery.GoogleSheetsOptions;
import com.google.cloud.bigquery.QueryJobConfiguration;
import com.google.cloud.bigquery.Schema;
import com.google.cloud.bigquery.StandardSQLTypeName;
import com.google.cloud.bigquery.TableResult;
import com.google.common.collect.ImmutableSet;
import java.io.IOException;

// Sample to queries an external data source using a temporary table
public class QueryExternalSheetsTemp {

  public static void main(String[] args) {
    // TODO(developer): Replace these variables before running the sample.
    String tableName = "MY_TABLE_NAME";
    String sourceUri =
        "https://docs.google.com/spreadsheets/d/1i_QCL-7HcSyUZmIbP9E6lO_T5u3HnpLe7dnpHaijg_E/edit?usp=sharing";
    Schema schema =
        Schema.of(
            Field.of("name", StandardSQLTypeName.STRING),
            Field.of("post_abbr", StandardSQLTypeName.STRING));
    String query = String.format("SELECT * FROM %s WHERE name LIKE 'W%%'", tableName);
    queryExternalSheetsTemp(tableName, sourceUri, schema, query);
  }

  public static void queryExternalSheetsTemp(
      String tableName, String sourceUri, Schema schema, String query) {
    try {

      // Create credentials with Drive & BigQuery API scopes.
      // Both APIs must be enabled for your project before running this code.
      GoogleCredentials credentials =
          ServiceAccountCredentials.getApplicationDefault()
              .createScoped(
                  ImmutableSet.of(
                      "https://www.googleapis.com/auth/bigquery",
                      "https://www.googleapis.com/auth/drive"));

      // Initialize client that will be used to send requests. This client only needs to be created
      // once, and can be reused for multiple requests.
      BigQuery bigquery =
          BigQueryOptions.newBuilder().setCredentials(credentials).build().getService();

      // Skip header row in the file.
      GoogleSheetsOptions sheetsOptions =
          GoogleSheetsOptions.newBuilder()
              .setSkipLeadingRows(1) // Optionally skip header row.
              .setRange("us-states!A20:B49") // Optionally set range of the sheet to query from.
              .build();

      // Configure the external data source and query job.
      ExternalTableDefinition externalTable =
          ExternalTableDefinition.newBuilder(sourceUri, sheetsOptions).setSchema(schema).build();
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
    } catch (BigQueryException | InterruptedException | IOException e) {
      System.out.println("Query not performed \n" + e.toString());
    }
  }
}
```

## 疑難排解

錯誤字串：`Resources exceeded during query execution: Google Sheets service
overloaded.`

這可能是暫時性錯誤，重新執行查詢即可修正。如果重新執行查詢後仍發生錯誤，請考慮簡化試算表，例如盡量減少使用公式。詳情請參閱「[外部資料表限制](https://docs.cloud.google.com/bigquery/docs/external-tables?hl=zh-tw#limitations)」。

錯誤字串：`Access Denied: BigQuery BigQuery: Permission denied while getting
Drive credentials`

如要解決這項錯誤，請按照下列步驟操作：

* 確認您具有連結至外部資料表的雲端硬碟檔案檢視者權限。
* 如果 bq 指令列工具版本為 `2.1.12` 或更舊，請使用 `--enable-gdrive-access` 旗標。
* 確認您或執行查詢的服務帳戶已獲授必要角色，可查詢 Google 雲端硬碟外部資料表。

## 後續步驟

* 瞭解如何[在 BigQuery 中使用 SQL](https://docs.cloud.google.com/bigquery/docs/introduction-sql?hl=zh-tw)。
* 瞭解[外部資料表](https://docs.cloud.google.com/bigquery/docs/external-tables?hl=zh-tw)。
* 瞭解 [BigQuery 配額](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-13 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-13 (世界標準時間)。"],[],[]]