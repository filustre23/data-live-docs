Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [範例](https://docs.cloud.google.com/bigquery/docs/samples?hl=zh-tw)

# 取得轉移作業 透過集合功能整理內容 你可以依據偏好儲存及分類內容。

從 BigQuery 資料移轉服務擷取特定移轉作業的相關資訊。

## 深入探索

如需包含這個程式碼範例的詳細說明文件，請參閱下列文章：

* [管理轉移作業](https://docs.cloud.google.com/bigquery/docs/working-with-transfers?hl=zh-tw)

## 程式碼範例

### Java

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Java 設定說明操作。詳情請參閱 [BigQuery Java API 參考說明文件](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/overview?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import com.google.api.gax.rpc.ApiException;
import com.google.cloud.bigquery.datatransfer.v1.DataTransferServiceClient;
import com.google.cloud.bigquery.datatransfer.v1.GetTransferRunRequest;
import com.google.cloud.bigquery.datatransfer.v1.TransferRun;
import java.io.IOException;

// Sample to get run details from transfer config.
public class RunDetails {

  public static void main(String[] args) throws IOException {
    // TODO(developer): Replace these variables before running the sample.
    // runId examples:
    // `projects/{project_id}/transferConfigs/{config_id}/runs/{run_id}` or
    // `projects/{project_id}/locations/{location_id}/transferConfigs/{config_id}/runs/{run_id}`
    String runId = "MY_RUN_ID";
    runDetails(runId);
  }

  public static void runDetails(String runId) throws IOException {
    try (DataTransferServiceClient dataTransferServiceClient = DataTransferServiceClient.create()) {
      GetTransferRunRequest request = GetTransferRunRequest.newBuilder().setName(runId).build();
      TransferRun run = dataTransferServiceClient.getTransferRun(request);
      System.out.print("Run details retrieved successfully :" + run.getName() + "\n");
    } catch (ApiException ex) {
      System.out.print("Run details not found." + ex.toString());
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
 * Gets a transfer run.
 * A transfer run represents a single execution of a data transfer configuration.
 *
 * @param {string} projectId The Google Cloud project ID, for example 'example-project-id'.
 * @param {string} location The location of the transfer config, for example 'us-central1'.
 * @param {string} transferConfigId The ID of the transfer configuration, for example '1234a-5678-9012b'.
 * @param {string} runId The ID of the transfer run, for example 'abcdef-0123-4567-8901-fedcba987654'.
 */
async function getTransferRun(
  projectId,
  location = 'us-central1',
  transferConfigId = '1234a-5678-9012b',
  runId = 'abcdef-0123-4567-8901-fedcba987654',
) {
  const name = client.projectLocationTransferConfigRunPath(
    projectId,
    location,
    transferConfigId,
    runId,
  );
  const request = {
    name,
  };

  try {
    const [run] = await client.getTransferRun(request);
    console.log(`Got transfer run: ${run.name}`);
    console.log(`  Data Source Id: ${run.dataSourceId}`);
    if (run.runTime && run.runTime.seconds) {
      console.log(
        `  Run time: ${new Date(run.runTime.seconds * 1000).toISOString()}`,
      );
    }
    console.log(`  State: ${run.state}`);
  } catch (err) {
    if (err.code === status.NOT_FOUND) {
      console.error(`Transfer run ${name} not found.`);
    } else {
      console.error(`Error getting transfer run ${name}:`, err);
    }
  }
}
```

### Python

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Python 設定說明操作。詳情請參閱 [BigQuery Python API 參考說明文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import google.api_core.exceptions
from google.cloud import bigquery_datatransfer_v1


client = bigquery_datatransfer_v1.DataTransferServiceClient()


def get_transfer_run(
    project_id: str,
    location: str,
    transfer_config_id: str,
    run_id: str,
) -> None:
    """Gets information about a transfer run.

    Args:
        project_id: The Google Cloud project ID.
        location: The geographic location of the transfer run, for example, 'us' or 'europe-west1'.
        transfer_config_id: The transfer configuration ID.
        run_id: The transfer run ID.
    """
    run_name = client.run_path(
        project=f"{project_id}/locations/{location}",
        transfer_config=transfer_config_id,
        run=run_id,
    )

    try:
        transfer_run = client.get_transfer_run(name=run_name)
        print(f"Got transfer run: {transfer_run.name}")
        print(f"State: {transfer_run.state.name}")
    except google.api_core.exceptions.NotFound:
        print(f"Error: Transfer run '{run_name}' not found.")
```

## 後續步驟

如要搜尋及篩選其他 Google Cloud 產品的程式碼範例，請參閱[Google Cloud 瀏覽器範例](https://docs.cloud.google.com/docs/samples?product=bigquerydatatransfer&hl=zh-tw)。

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。




[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],[],[],[]]