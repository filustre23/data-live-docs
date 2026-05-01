* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [範例](https://docs.cloud.google.com/bigquery/docs/samples?hl=zh-tw)

# 列出移轉執行作業 透過集合功能整理內容 你可以依據偏好儲存及分類內容。

列出 BigQuery 資料移轉服務轉移設定的所有執行作業。

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
import com.google.cloud.bigquery.datatransfer.v1.ListTransferRunsRequest;
import java.io.IOException;

// Sample to get run history from transfer config.
public class RunHistory {

  public static void main(String[] args) throws IOException {
    // TODO(developer): Replace these variables before running the sample.
    String configId = "MY_CONFIG_ID";
    // i.e projects/{project_id}/transferConfigs/{config_id}` or
    // `projects/{project_id}/locations/{location_id}/transferConfigs/{config_id}`
    runHistory(configId);
  }

  public static void runHistory(String configId) throws IOException {
    try (DataTransferServiceClient dataTransferServiceClient = DataTransferServiceClient.create()) {
      ListTransferRunsRequest request =
          ListTransferRunsRequest.newBuilder().setParent(configId).build();
      dataTransferServiceClient
          .listTransferRuns(request)
          .iterateAll()
          .forEach(run -> System.out.print("Success! Run ID :" + run.getName() + "\n"));
    } catch (ApiException ex) {
      System.out.println("Run history not found due to error." + ex.toString());
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
 * Lists transfer runs for a given transfer configuration.
 *
 * This sample shows how to list all the transfer runs for a specific transfer
 * configuration, to monitor and audit data transfer jobs.
 *
 * @param {string} projectId The Google Cloud project ID, for example 'example-project-id'.
 * @param {string} location The Google Cloud region, for example 'us-central1'.
 * @param {string} configId The BigQuery Transfer Service config ID, for example 'example-config-id'.
 */
async function listTransferRuns(projectId, location, configId) {
  const parent = `projects/${projectId}/locations/${location}/transferConfigs/${configId}`;
  const request = {
    parent,
  };

  try {
    const [transferRuns] = await client.listTransferRuns(request);
    if (transferRuns.length === 0) {
      console.error(
        `No transfer runs found in project ${projectId} for ${location}.`,
      );
      return;
    }
    console.log(`Transfer runs for config '${configId}':`);
    for (const run of transferRuns) {
      console.log(`\nTransfer Run: ${run.name}`);
      console.log(`  Data Source Id: ${run.dataSourceId}`);
      if (run.runTime && run.runTime.seconds) {
        console.log(
          `  Run time: ${new Date(run.runTime.seconds * 1000).toISOString()}`,
        );
      }
      console.log(`  State: ${run.state}`);
    }
  } catch (err) {
    if (err.code === status.NOT_FOUND) {
      console.error(`Transfer run not found: ${parent}`);
    } else {
      console.error('Error listing transfer runs:', err);
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


def list_transfer_runs(project_id: str, transfer_config_id: str, location: str) -> None:
    """Lists transfer runs for a given transfer configuration.

    This method retrieves a history of runs for a specific data transfer job.

    Args:
        project_id: The Google Cloud project ID.
        transfer_config_id: The data transfer configuration ID.
        location: The geographic location of the transfer configuration (e.g., 'us-central1').
    """

    parent = client.transfer_config_path(
        project=f"{project_id}/locations/{location}",
        transfer_config=transfer_config_id,
    )
    request = bigquery_datatransfer_v1.ListTransferRunsRequest(
        parent=parent,
    )

    try:
        pager = client.list_transfer_runs(request=request)
        for run in pager:
            print(f"  Run: {run.name}, State: {run.state.name}")
    except google.api_core.exceptions.NotFound:
        print(
            f"Error: Transfer configuration not found: '{parent}'."
            "Please verify that the project ID, location, and transfer config ID are correct."
        )
```

## 後續步驟

如要搜尋及篩選其他 Google Cloud 產品的程式碼範例，請參閱[Google Cloud 瀏覽器範例](https://docs.cloud.google.com/docs/samples?product=bigquerydatatransfer&hl=zh-tw)。

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。




[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],[],[],[]]