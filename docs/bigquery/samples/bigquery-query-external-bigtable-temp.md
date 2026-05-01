* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [範例](https://docs.cloud.google.com/bigquery/docs/samples?hl=zh-tw)

# 使用臨時資料表來查詢 Bigtable 透過集合功能整理內容 你可以依據偏好儲存及分類內容。

建立臨時資料表，查詢 Bigtable 執行個體的資料。

## 深入探索

如需包含這個程式碼範例的詳細說明文件，請參閱下列文章：

* [查詢 Bigtable 資料](https://docs.cloud.google.com/bigquery/docs/external-data-bigtable?hl=zh-tw)

## 程式碼範例

### Java

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Java 設定說明操作。詳情請參閱 [BigQuery Java API 參考說明文件](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/overview?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import com.google.api.client.util.Base64;
import com.google.cloud.bigquery.BigQuery;
import com.google.cloud.bigquery.BigQueryException;
import com.google.cloud.bigquery.BigQueryOptions;
import com.google.cloud.bigquery.BigtableColumn;
import com.google.cloud.bigquery.BigtableColumnFamily;
import com.google.cloud.bigquery.BigtableOptions;
import com.google.cloud.bigquery.ExternalTableDefinition;
import com.google.cloud.bigquery.QueryJobConfiguration;
import com.google.cloud.bigquery.TableResult;
import com.google.common.collect.ImmutableList;

// Sample to queries an external bigtable data source using a temporary table
public class QueryExternalBigtableTemp {

  public static void main(String[] args) {
    // TODO(developer): Replace these variables before running the sample.
    String projectId = "MY_PROJECT_ID";
    String bigtableInstanceId = "MY_INSTANCE_ID";
    String bigtableTableName = "MY_BIGTABLE_NAME";
    String bigqueryTableName = "MY_TABLE_NAME";
    String sourceUri =
        String.format(
            "https://googleapis.com/bigtable/projects/%s/instances/%s/tables/%s",
            projectId, bigtableInstanceId, bigtableTableName);
    String query = String.format("SELECT * FROM %s ", bigqueryTableName);
    queryExternalBigtableTemp(bigqueryTableName, sourceUri, query);
  }

  public static void queryExternalBigtableTemp(String tableName, String sourceUri, String query) {
    try {
      // Initialize client that will be used to send requests. This client only needs to be created
      // once, and can be reused for multiple requests.
      BigQuery bigquery = BigQueryOptions.getDefaultInstance().getService();

      BigtableColumnFamily.Builder statsSummary = BigtableColumnFamily.newBuilder();

      // Configuring Columns
      BigtableColumn connectedCell =
          BigtableColumn.newBuilder()
              .setQualifierEncoded(Base64.encodeBase64String("connected_cell".getBytes()))
              .setFieldName("connected_cell")
              .setType("STRING")
              .setEncoding("TEXT")
              .build();
      BigtableColumn connectedWifi =
          BigtableColumn.newBuilder()
              .setQualifierEncoded(Base64.encodeBase64String("connected_wifi".getBytes()))
              .setFieldName("connected_wifi")
              .setType("STRING")
              .setEncoding("TEXT")
              .build();
      BigtableColumn osBuild =
          BigtableColumn.newBuilder()
              .setQualifierEncoded(Base64.encodeBase64String("os_build".getBytes()))
              .setFieldName("os_build")
              .setType("STRING")
              .setEncoding("TEXT")
              .build();

      // Configuring column family and columns
      statsSummary
          .setColumns(ImmutableList.of(connectedCell, connectedWifi, osBuild))
          .setFamilyID("stats_summary")
          .setOnlyReadLatest(true)
          .setEncoding("TEXT")
          .setType("STRING")
          .build();

      // Configuring BigtableOptions is optional.
      BigtableOptions options =
          BigtableOptions.newBuilder()
              .setIgnoreUnspecifiedColumnFamilies(true)
              .setReadRowkeyAsString(true)
              .setColumnFamilies(ImmutableList.of(statsSummary.build()))
              .build();

      // Configure the external data source and query job.
      ExternalTableDefinition externalTable =
          ExternalTableDefinition.newBuilder(sourceUri, options).build();
      QueryJobConfiguration queryConfig =
          QueryJobConfiguration.newBuilder(query)
              .addTableDefinition(tableName, externalTable)
              .build();

      // Example query
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

## 後續步驟

如要搜尋及篩選其他 Google Cloud 產品的程式碼範例，請參閱[Google Cloud 範例瀏覽工具](https://docs.cloud.google.com/docs/samples?product=bigquery&hl=zh-tw)。

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。




[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],[],[],[]]