Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [範例](https://docs.cloud.google.com/bigquery/docs/samples?hl=zh-tw)

# 刪除資料移轉設定 透過集合功能整理內容 你可以依據偏好儲存及分類內容。

刪除 BigQuery 資料移轉服務中的資料移轉設定。刪除設定後，系統會停止日後的移轉作業，但不會移除已移轉至 BigQuery 的資料。

## 深入探索

如需包含這個程式碼範例的詳細說明文件，請參閱下列文章：

* [管理轉移作業](https://docs.cloud.google.com/bigquery/docs/working-with-transfers?hl=zh-tw)
* [排定查詢](https://docs.cloud.google.com/bigquery/docs/scheduling-queries?hl=zh-tw)

## 程式碼範例

### Java

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Java 設定說明操作。詳情請參閱 [BigQuery Java API 參考說明文件](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/overview?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import com.google.api.gax.rpc.ApiException;
import com.google.cloud.bigquery.datatransfer.v1.DataTransferServiceClient;
import com.google.cloud.bigquery.datatransfer.v1.DeleteTransferConfigRequest;
import java.io.IOException;

// Sample to delete a transfer config
public class DeleteTransferConfig {

  public static void main(String[] args) throws IOException {
    // TODO(developer): Replace these variables before running the sample.
    // i.e projects/{project_id}/transferConfigs/{config_id}` or
    // `projects/{project_id}/locations/{location_id}/transferConfigs/{config_id}`
    String configId = "MY_CONFIG_ID";
    deleteTransferConfig(configId);
  }

  public static void deleteTransferConfig(String configId) throws IOException {
    try (DataTransferServiceClient dataTransferServiceClient = DataTransferServiceClient.create()) {
      DeleteTransferConfigRequest request =
          DeleteTransferConfigRequest.newBuilder().setName(configId).build();
      dataTransferServiceClient.deleteTransferConfig(request);
      System.out.println("Transfer config deleted successfully");
    } catch (ApiException ex) {
      System.out.println("Transfer config was not deleted." + ex.toString());
    }
  }
}
```

### Node.js

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Node.js 設定說明操作。詳情請參閱 [BigQuery Node.js API 參考說明文件](https://googleapis.dev/nodejs/bigquery/latest/index.html)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
const {
  DataTransferServiceClient,
} = require('@google-cloud/bigquery-data-transfer');
const {status} = require('@grpc/grpc-js');

const client = new DataTransferServiceClient();

/**
 * Deletes a data transfer configuration.
 * This sample demonstrates how to delete a transfer configuration, which also
 * removes its associated transfer runs and logs.
 *
 * @param {string} projectId Your Google Cloud project ID, for example 'example-project-id'
 * @param {string} location The BigQuery location, for example 'us-central1'
 * @param {string} configId The transfer configuration ID, for example '1234a567-b89c-12d3-45e6-f789g01h23i4'
 */
async function deleteTransferConfig(projectId, location, configId) {
  const name = client.projectLocationTransferConfigPath(
    projectId,
    location,
    configId,
  );
  const request = {
    name,
  };

  try {
    await client.deleteTransferConfig(request);
    console.log(`Transfer config deleted '${configId}'`);
  } catch (err) {
    if (err.code === status.NOT_FOUND) {
      console.error(`Transfer config '${configId}' not found.`);
    } else {
      console.error(`Error deleting transfer config '${configId}':`, err);
    }
  }
}
```

## 後續步驟

如要搜尋及篩選其他 Google Cloud 產品的程式碼範例，請參閱[Google Cloud 範例瀏覽工具](https://docs.cloud.google.com/docs/samples?product=bigquerydatatransfer&hl=zh-tw)。

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。




[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],[],[],[]]