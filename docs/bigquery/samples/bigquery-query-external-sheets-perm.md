Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [範例](https://docs.cloud.google.com/bigquery/docs/samples?hl=zh-tw)

# 使用永久資料表查詢試算表 透過集合功能整理內容 你可以依據偏好儲存及分類內容。

建立永久資料表，查詢 Google 試算表檔案中的資料。

## 程式碼範例

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
import com.google.cloud.bigquery.TableId;
import com.google.cloud.bigquery.TableInfo;
import com.google.cloud.bigquery.TableResult;
import com.google.common.collect.ImmutableSet;
import java.io.IOException;

// Sample to queries an external data source using a permanent table
public class QueryExternalSheetsPerm {

  public static void main(String[] args) {
    // TODO(developer): Replace these variables before running the sample.
    String datasetName = "MY_DATASET_NAME";
    String tableName = "MY_TABLE_NAME";
    String sourceUri =
        "https://docs.google.com/spreadsheets/d/1i_QCL-7HcSyUZmIbP9E6lO_T5u3HnpLe7dnpHaijg_E/edit?usp=sharing";
    Schema schema =
        Schema.of(
            Field.of("name", StandardSQLTypeName.STRING),
            Field.of("post_abbr", StandardSQLTypeName.STRING));
    String query =
        String.format("SELECT * FROM %s.%s WHERE name LIKE 'W%%'", datasetName, tableName);
    queryExternalSheetsPerm(datasetName, tableName, sourceUri, schema, query);
  }

  public static void queryExternalSheetsPerm(
      String datasetName, String tableName, String sourceUri, Schema schema, String query) {
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

      TableId tableId = TableId.of(datasetName, tableName);
      // Create a permanent table linked to the Sheets file.
      ExternalTableDefinition externalTable =
          ExternalTableDefinition.newBuilder(sourceUri, sheetsOptions).setSchema(schema).build();
      bigquery.create(TableInfo.of(tableId, externalTable));

      // Example query to find states starting with 'W'
      TableResult results = bigquery.query(QueryJobConfiguration.of(query));

      results
          .iterateAll()
          .forEach(row -> row.forEach(val -> System.out.printf("%s,", val.toString())));

      System.out.println("Query on external permanent table performed successfully.");
    } catch (BigQueryException | InterruptedException | IOException e) {
      System.out.println("Query not performed \n" + e.toString());
    }
  }
}
```

### Python

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Python 設定說明操作。詳情請參閱 [BigQuery Python API 參考說明文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
from google.cloud import bigquery
import google.auth

# Create credentials with Drive & BigQuery API scopes.
# Both APIs must be enabled for your project before running this code.
#
# If you are using credentials from gcloud, you must authorize the
# application first with the following command:
#
# gcloud auth application-default login \
#   --scopes=https://www.googleapis.com/auth/drive,https://www.googleapis.com/auth/cloud-platform
credentials, project = google.auth.default(
    scopes=[
        "https://www.googleapis.com/auth/drive",
        "https://www.googleapis.com/auth/bigquery",
    ]
)

# Construct a BigQuery client object.
client = bigquery.Client(credentials=credentials, project=project)

# TODO(developer): Set dataset_id to the ID of the dataset to fetch.
# dataset_id = "your-project.your_dataset"

# Configure the external data source.
dataset = client.get_dataset(dataset_id)
table_id = "us_states"
schema = [
    bigquery.SchemaField("name", "STRING"),
    bigquery.SchemaField("post_abbr", "STRING"),
]
table = bigquery.Table(dataset.table(table_id), schema=schema)
external_config = bigquery.ExternalConfig("GOOGLE_SHEETS")
# Use a shareable link or grant viewing access to the email address you
# used to authenticate with BigQuery (this example Sheet is public).
sheet_url = (
    "https://docs.google.com/spreadsheets"
    "/d/1i_QCL-7HcSyUZmIbP9E6lO_T5u3HnpLe7dnpHaijg_E/edit?usp=sharing"
)
external_config.source_uris = [sheet_url]
options = external_config.google_sheets_options
assert options is not None
options.skip_leading_rows = 1  # Optionally skip header row.
options.range = (
    "us-states!A20:B49"  # Optionally set range of the sheet to query from.
)
table.external_data_configuration = external_config

# Create a permanent table linked to the Sheets file.
table = client.create_table(table)  # Make an API request.

# Example query to find states starting with "W".
sql = 'SELECT * FROM `{}.{}` WHERE name LIKE "W%"'.format(dataset_id, table_id)

results = client.query_and_wait(sql)  # Make an API request.

# Wait for the query to complete.
w_states = list(results)
print(
    "There are {} states with names starting with W in the selected range.".format(
        len(w_states)
    )
)
```

## 後續步驟

如要搜尋及篩選其他 Google Cloud 產品的程式碼範例，請參閱[Google Cloud 範例瀏覽工具](https://docs.cloud.google.com/docs/samples?product=bigquery&hl=zh-tw)。

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。




[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],[],[],[]]