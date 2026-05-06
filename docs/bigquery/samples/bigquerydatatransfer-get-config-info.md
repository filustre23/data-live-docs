Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [範例](https://docs.cloud.google.com/bigquery/docs/samples?hl=zh-tw)

# 取得移轉設定 透過集合功能整理內容 你可以依據偏好儲存及分類內容。

從 BigQuery 資料移轉服務擷取移轉設定的詳細資料，例如排程和目的地。

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
import com.google.cloud.bigquery.datatransfer.v1.GetTransferConfigRequest;
import com.google.cloud.bigquery.datatransfer.v1.TransferConfig;
import java.io.IOException;

// Sample to get config info.
public class GetTransferConfigInfo {

  public static void main(String[] args) throws IOException {
    // TODO(developer): Replace these variables before running the sample.
    String configId = "MY_CONFIG_ID";
    // i.e projects/{project_id}/transferConfigs/{config_id}` or
    // `projects/{project_id}/locations/{location_id}/transferConfigs/{config_id}`
    getTransferConfigInfo(configId);
  }

  public static void getTransferConfigInfo(String configId) throws IOException {
    try (DataTransferServiceClient dataTransferServiceClient = DataTransferServiceClient.create()) {
      GetTransferConfigRequest request =
          GetTransferConfigRequest.newBuilder().setName(configId).build();
      TransferConfig info = dataTransferServiceClient.getTransferConfig(request);
      System.out.print("Config info retrieved successfully." + info.getName() + "\n");
    } catch (ApiException ex) {
      System.out.print("config not found." + ex.toString());
    }
  }
}
```

### Node.js

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Node.js 設定說明操作。詳情請參閱 [BigQuery Node.js API 參考說明文件](https://googleapis.dev/nodejs/bigquery/latest/index.html)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
const {DataTransferServiceClient} =
  require('@google-cloud/bigquery-data-transfer').v1;
const {status} = require('@grpc/grpc-js');

const client = new DataTransferServiceClient();

/**
 * Gets a transfer configuration for a BigQuery data transfer.
 * A transfer configuration contains all metadata needed to perform a data transfer.
 *
 * @param {string} projectId The Google Cloud project ID (for example, 'example-project-id').
 * @param {string} location The Google Cloud region (for example, 'us-central1').
 * @param {string} configId The transfer configuration ID (for example, '1234a567-b89c-12d3-45e6-f789g01h23i4').
 */
async function getTransferConfig(projectId, location, configId) {
  const name = client.projectLocationTransferConfigPath(
    projectId,
    location,
    configId,
  );
  const request = {
    name,
  };

  try {
    const [config] = await client.getTransferConfig(request);
    console.log(`Got transfer config: ${config.name}`);
    console.log(`  Display Name: ${config.displayName}`);
    console.log(`  Data Source ID: ${config.dataSourceId}`);
    console.log(`  Destination Dataset ID: ${config.destinationDatasetId}`);
    console.log(`  State: ${config.state}`);
  } catch (err) {
    if (err.code === status.NOT_FOUND) {
      console.error(
        `Transfer config ${configId} not found in project ${projectId} in location ${location}.`,
      );
    } else {
      console.error(`Error getting transfer config ${configId}:`, err);
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


def get_transfer_config(
    project_id: str,
    location: str,
    transfer_config_id: str,
) -> None:
    """Gets information about a data transfer configuration.

    This sample demonstrates how to retrieve the details of a BigQuery
    Data Transfer Service configuration, which contains metadata about a
    data transfer, such as its schedule and destination.

    Args:
        project_id: The Google Cloud project ID.
        location: The geographic location of the transfer config, for example "us-central1"
        transfer_config_id: The transfer configuration ID
    """

    try:
        transfer_config_name = client.transfer_config_path(
            project=f"{project_id}/locations/{location}",
            transfer_config=transfer_config_id,
        )
        transfer_config = client.get_transfer_config(name=transfer_config_name)

        print(f"Got transfer config: {transfer_config.name}")
        print(f"Display name: {transfer_config.display_name}")
        print(f"Destination dataset: {transfer_config.destination_dataset_id}")
        print(f"Data source: {transfer_config.data_source_id}")
        if "time_based_schedule" in transfer_config.schedule_options_v2:
            print(
                f"Schedule: {transfer_config.schedule_options_v2.time_based_schedule.schedule}"
            )
        else:
            print("Schedule: None")
    except google.api_core.exceptions.NotFound:
        print(f"Error: Transfer config '{transfer_config_name}' not found.")
```

## 後續步驟

如要搜尋及篩選其他 Google Cloud 產品的程式碼範例，請參閱[Google Cloud 瀏覽器範例](https://docs.cloud.google.com/docs/samples?product=bigquerydatatransfer&hl=zh-tw)。

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。




[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],[],[],[]]