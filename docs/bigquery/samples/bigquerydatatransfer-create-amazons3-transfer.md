Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [範例](https://docs.cloud.google.com/bigquery/docs/samples?hl=zh-tw)

# 從 Amazon S3 載入資料 透過集合功能整理內容 你可以依據偏好儲存及分類內容。

安排從 Amazon S3 到 BigQuery 的週期性載入工作。

## 深入探索

如需包含這個程式碼範例的詳細說明文件，請參閱下列文章：

* [將 Amazon S3 資料載入 BigQuery](https://docs.cloud.google.com/bigquery/docs/s3-transfer?hl=zh-tw)

## 程式碼範例

### Java

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Java 設定說明操作。詳情請參閱 [BigQuery Java API 參考說明文件](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/overview?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import com.google.api.gax.rpc.ApiException;
import com.google.cloud.bigquery.datatransfer.v1.CreateTransferConfigRequest;
import com.google.cloud.bigquery.datatransfer.v1.DataTransferServiceClient;
import com.google.cloud.bigquery.datatransfer.v1.ProjectName;
import com.google.cloud.bigquery.datatransfer.v1.TransferConfig;
import com.google.protobuf.Struct;
import com.google.protobuf.Value;
import java.io.IOException;
import java.util.HashMap;
import java.util.Map;

// Sample to create amazon s3 transfer config.
public class CreateAmazonS3Transfer {

  public static void main(String[] args) throws IOException {
    // TODO(developer): Replace these variables before running the sample.
    final String projectId = "MY_PROJECT_ID";
    String datasetId = "MY_DATASET_ID";
    String tableId = "MY_TABLE_ID";
    // Amazon S3 Bucket Uri with read role permission
    String sourceUri = "s3://your-bucket-name/*";
    String awsAccessKeyId = "MY_AWS_ACCESS_KEY_ID";
    String awsSecretAccessId = "AWS_SECRET_ACCESS_ID";
    String sourceFormat = "CSV";
    String fieldDelimiter = ",";
    String skipLeadingRows = "1";
    Map<String, Value> params = new HashMap<>();
    params.put(
        "destination_table_name_template", Value.newBuilder().setStringValue(tableId).build());
    params.put("data_path", Value.newBuilder().setStringValue(sourceUri).build());
    params.put("access_key_id", Value.newBuilder().setStringValue(awsAccessKeyId).build());
    params.put("secret_access_key", Value.newBuilder().setStringValue(awsSecretAccessId).build());
    params.put("source_format", Value.newBuilder().setStringValue(sourceFormat).build());
    params.put("field_delimiter", Value.newBuilder().setStringValue(fieldDelimiter).build());
    params.put("skip_leading_rows", Value.newBuilder().setStringValue(skipLeadingRows).build());
    TransferConfig transferConfig =
        TransferConfig.newBuilder()
            .setDestinationDatasetId(datasetId)
            .setDisplayName("Your Aws S3 Config Name")
            .setDataSourceId("amazon_s3")
            .setParams(Struct.newBuilder().putAllFields(params).build())
            .setSchedule("every 24 hours")
            .build();
    createAmazonS3Transfer(projectId, transferConfig);
  }

  public static void createAmazonS3Transfer(String projectId, TransferConfig transferConfig)
      throws IOException {
    try (DataTransferServiceClient client = DataTransferServiceClient.create()) {
      ProjectName parent = ProjectName.of(projectId);
      CreateTransferConfigRequest request =
          CreateTransferConfigRequest.newBuilder()
              .setParent(parent.toString())
              .setTransferConfig(transferConfig)
              .build();
      TransferConfig config = client.createTransferConfig(request);
      System.out.println("Amazon s3 transfer created successfully :" + config.getName());
    } catch (ApiException ex) {
      System.out.print("Amazon s3 transfer was not created." + ex.toString());
    }
  }
}
```

## 後續步驟

如要搜尋及篩選其他 Google Cloud 產品的程式碼範例，請參閱[Google Cloud 瀏覽器範例](https://docs.cloud.google.com/docs/samples?product=bigquerydatatransfer&hl=zh-tw)。

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。




[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],[],[],[]]