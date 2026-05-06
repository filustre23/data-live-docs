Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [範例](https://docs.cloud.google.com/bigquery/docs/samples?hl=zh-tw)

# 建立資料移轉設定 透過集合功能整理內容 你可以依據偏好儲存及分類內容。

在 BigQuery 資料移轉服務中建立移轉設定，排定從支援的資料來源到 BigQuery 資料集的週期性資料移轉作業。

## 深入探索

如需包含這個程式碼範例的詳細說明文件，請參閱下列文章：

* [將 Cloud Storage 資料載入 BigQuery](https://docs.cloud.google.com/bigquery/docs/cloud-storage-transfer?hl=zh-tw)

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

// Sample to create google cloud storage transfer config
public class CreateCloudStorageTransfer {

  public static void main(String[] args) throws IOException {
    // TODO(developer): Replace these variables before running the sample.
    final String projectId = "MY_PROJECT_ID";
    String datasetId = "MY_DATASET_ID";
    String tableId = "MY_TABLE_ID";
    // GCS Uri
    String sourceUri = "gs://cloud-samples-data/bigquery/us-states/us-states.csv";
    String fileFormat = "CSV";
    String fieldDelimiter = ",";
    String skipLeadingRows = "1";
    Map<String, Value> params = new HashMap<>();
    params.put(
        "destination_table_name_template", Value.newBuilder().setStringValue(tableId).build());
    params.put("data_path_template", Value.newBuilder().setStringValue(sourceUri).build());
    params.put("write_disposition", Value.newBuilder().setStringValue("APPEND").build());
    params.put("file_format", Value.newBuilder().setStringValue(fileFormat).build());
    params.put("field_delimiter", Value.newBuilder().setStringValue(fieldDelimiter).build());
    params.put("skip_leading_rows", Value.newBuilder().setStringValue(skipLeadingRows).build());
    TransferConfig transferConfig =
        TransferConfig.newBuilder()
            .setDestinationDatasetId(datasetId)
            .setDisplayName("Your Google Cloud Storage Config Name")
            .setDataSourceId("google_cloud_storage")
            .setParams(Struct.newBuilder().putAllFields(params).build())
            .setSchedule("every 24 hours")
            .build();
    createCloudStorageTransfer(projectId, transferConfig);
  }

  public static void createCloudStorageTransfer(String projectId, TransferConfig transferConfig)
      throws IOException {
    try (DataTransferServiceClient client = DataTransferServiceClient.create()) {
      ProjectName parent = ProjectName.of(projectId);
      CreateTransferConfigRequest request =
          CreateTransferConfigRequest.newBuilder()
              .setParent(parent.toString())
              .setTransferConfig(transferConfig)
              .build();
      TransferConfig config = client.createTransferConfig(request);
      System.out.println("Cloud storage transfer created successfully :" + config.getName());
    } catch (ApiException ex) {
      System.out.print("Cloud storage transfer was not created." + ex.toString());
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
 * Creates a transfer configuration for a Google Cloud Storage transfer.
 *
 * This sample demonstrates how to create a transfer configuration that appends
 * data from Google Cloud Storage to a BigQuery dataset.
 *
 * @param {string} projectId The Google Cloud project ID. (for example, 'example-project-id')
 * @param {string} location The BigQuery location where the transfer config should be created. (for example, 'us-central1')
 * @param {string} sourceDataCloudStorageUri The source data to be transferred into BigQuery.
 *   Expects a Cloud Storage object URI. (for example, 'gs://example-bucket/example-data.csv')
 * @param {string} destinationDatasetId The destination BigQuery dataset ID. (for example, 'example_dataset')
 * @param {string} destinationTableName The destination table in the BigQuery dataset. (for example, 'example_destination_table')
 * @param {string} serviceAccountName The service account used by the data transfer process to read data from Google Cloud Storage.
 *   Make sure it has IAM read access to the sourceDataCloudStorageUri [example IAM role: roles/storage.objectViewer]. (for example, 'data-transfer-service-account@example-project-id.iam.gserviceaccount.com')
 */
async function createTransferConfig(
  projectId,
  location,
  sourceDataCloudStorageUri,
  destinationDatasetId,
  destinationTableName,
  serviceAccountName,
) {
  const transferConfig = {
    destinationDatasetId,
    displayName: 'Example Cloud Storage Transfer',
    dataSourceId: 'google_cloud_storage',
    // Params are in google.protobuf.Struct format.
    params: {
      fields: {
        data_path_template: {stringValue: sourceDataCloudStorageUri},
        destination_table_name_template: {stringValue: destinationTableName},
        file_format: {stringValue: 'CSV'},
        skip_leading_rows: {stringValue: '1'},
      },
    },
  };

  const request = {
    parent: `projects/${projectId}/locations/${location}`,
    transferConfig,
    serviceAccountName,
  };

  try {
    const [config] = await client.createTransferConfig(request);
    console.log(`Created transfer config: ${config.name}`);
    console.log(`  Display Name: ${config.displayName}`);
    console.log(`  Data Source ID: ${config.dataSourceId}`);
    console.log(`  Destination Dataset ID: ${config.destinationDatasetId}`);
  } catch (err) {
    if (err.code === status.INVALID_ARGUMENT) {
      console.error(
        `Error: Invalid argument provided for creating Migration '${transferConfig.displayName}'. ` +
          `Details: ${err.message}. Make sure request parameters are valid.`,
      );
      console.error(err);
    } else {
      console.error('Error creating transfer config:', err);
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
from google.protobuf import struct_pb2

client = bigquery_datatransfer_v1.DataTransferServiceClient()


def create_transfer_config(
    project_id: str,
    location: str,
    source_cloud_storage_uri: str,
    destination_dataset_id: str,
    destination_table_name: str,
    service_account: str = None,
) -> None:
    """Creates a transfer configuration for a Google Cloud Storage transfer.

    This sample demonstrates how to create a transfer configuration for a
    one-time Google Cloud Storage transfer. It specifies the source data path,
    destination table, and other parameters for the transfer.

    Args:
        project_id: The Google Cloud project ID.
        location: The geographic location of the transfer config, for example "us-central1"
        source_data_path: The Cloud Storage URL of the source data, for example "gs://example-bucket/example-data.csv"
        destination_dataset_id: The BigQuery dataset ID to which data is transferred.
        destination_table_name: The BigQuery table name to which data is transferred.
            Cloud Storage transfers support runtime parameters https://docs.cloud.google.com/bigquery/docs/gcs-transfer-parameters
        service_account: The optional IAM Service Account to use as the transfer owner. Otherwise, the current user is the owner.
    """

    parent = f"projects/{project_id}/locations/{location}"
    data_source_id = "google_cloud_storage"
    params = struct_pb2.Struct()
    params.update(
        {
            "data_path_template": source_cloud_storage_uri,
            "destination_table_name_template": destination_table_name,
            "file_format": "CSV",
            "skip_leading_rows": "1",  # assumes the first line in the CSV is the header
        }
    )
    transfer_config = bigquery_datatransfer_v1.TransferConfig(
        display_name="My Cloud Storage Data Transfer",
        data_source_id=data_source_id,
        destination_dataset_id=destination_dataset_id,
        params=params,
    )

    try:
        request = bigquery_datatransfer_v1.CreateTransferConfigRequest(
            parent=parent,
            transfer_config=transfer_config,
            service_account_name=service_account,
        )

        response = client.create_transfer_config(request=request)
        print(f"Created transfer config: {response.name}")
    except google.api_core.exceptions.InvalidArgument as e:
        print(
            f"Error: Could not create transfer config due to an invalid argument: {e}. Please check the destination dataset and other parameters."
        )
    except google.api_core.exceptions.GoogleAPICallError as e:
        print(f"Error: Could not create transfer config: {e}")
```

## 後續步驟

如要搜尋及篩選其他 Google Cloud 產品的程式碼範例，請參閱[Google Cloud 瀏覽器範例](https://docs.cloud.google.com/docs/samples?product=bigquerydatatransfer&hl=zh-tw)。

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。




[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],[],[],[]]