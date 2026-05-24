Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [範例](https://docs.cloud.google.com/bigquery/docs/samples?hl=zh-tw)

# 設定 Hive 分區選項 透過集合功能整理內容 你可以依據偏好儲存及分類內容。

設定 Hive 分區選項

## 深入探索

如需包含這個程式碼範例的詳細說明文件，請參閱下列文章：

* [建立 Cloud Storage 外部資料表](https://docs.cloud.google.com/bigquery/docs/external-data-cloud-storage?hl=zh-tw)

## 程式碼範例

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
public class CreateTableExternalHivePartitioned {

  public static void main(String[] args) {
    // TODO(developer): Replace these variables before running the sample.
    String datasetName = "MY_DATASET_NAME";
    String tableName = "MY_TABLE_NAME";
    String sourceUri = "gs://cloud-samples-data/bigquery/hive-partitioning-samples/customlayout/*";
    String sourceUriPrefix =
        "gs://cloud-samples-data/bigquery/hive-partitioning-samples/customlayout/{pkey:STRING}/";
    createTableExternalHivePartitioned(datasetName, tableName, sourceUriPrefix, sourceUri);
  }

  public static void createTableExternalHivePartitioned(
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

## 後續步驟

如要搜尋及篩選其他 Google Cloud 產品的程式碼範例，請參閱[Google Cloud 範例瀏覽工具](https://docs.cloud.google.com/docs/samples?product=bigquery&hl=zh-tw)。

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。




[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],[],[],[]]