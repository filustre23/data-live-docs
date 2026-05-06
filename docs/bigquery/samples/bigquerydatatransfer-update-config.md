Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [範例](https://docs.cloud.google.com/bigquery/docs/samples?hl=zh-tw)

# 更新移轉設定 透過集合功能整理內容 你可以依據偏好儲存及分類內容。

更新 BigQuery 資料移轉服務中現有移轉設定的顯示名稱。

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
import com.google.cloud.bigquery.datatransfer.v1.TransferConfig;
import com.google.cloud.bigquery.datatransfer.v1.UpdateTransferConfigRequest;
import com.google.protobuf.FieldMask;
import com.google.protobuf.util.FieldMaskUtil;
import java.io.IOException;

// Sample to update transfer config.
public class UpdateTransferConfig {

  public static void main(String[] args) throws IOException {
    // TODO(developer): Replace these variables before running the sample.
    String configId = "MY_CONFIG_ID";
    TransferConfig transferConfig =
        TransferConfig.newBuilder()
            .setName(configId)
            .setDisplayName("UPDATED_DISPLAY_NAME")
            .build();
    FieldMask updateMask = FieldMaskUtil.fromString("display_name");
    updateTransferConfig(transferConfig, updateMask);
  }

  public static void updateTransferConfig(TransferConfig transferConfig, FieldMask updateMask)
      throws IOException {
    try (DataTransferServiceClient dataTransferServiceClient = DataTransferServiceClient.create()) {
      UpdateTransferConfigRequest request =
          UpdateTransferConfigRequest.newBuilder()
              .setTransferConfig(transferConfig)
              .setUpdateMask(updateMask)
              .build();
      TransferConfig updateConfig = dataTransferServiceClient.updateTransferConfig(request);
      System.out.println("Transfer config updated successfully :" + updateConfig.getDisplayName());
    } catch (ApiException ex) {
      System.out.print("Transfer config was not updated." + ex.toString());
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
 * Updates a transfer configuration for a BigQuery data transfer.
 *
 * This sample shows how to update properties of an existing transfer configuration, such as its display name.
 * An update mask is required to specify which fields to modify.
 *
 * @param {string} projectId The Google Cloud project ID, for example 'example-project-id'
 * @param {string} location The location of the transfer config, for example 'us-central1'
 * @param {string} configId The ID of the transfer config to update, for example '1234a-5678-9012b-3456c'
 */
async function updateTransferConfig(projectId, location, configId) {
  const transferConfig = {
    name: `projects/${projectId}/locations/${location}/transferConfigs/${configId}`,
    displayName: 'Example Data Transfer (Update)',
  };

  const request = {
    transferConfig,
    updateMask: {
      paths: ['display_name'],
    },
  };

  try {
    const [response] = await client.updateTransferConfig(request);
    console.log(`Transfer config: ${response.name}`);
    console.log(`  Updated display name: ${response.displayName}`);
  } catch (err) {
    if (err.code === status.NOT_FOUND) {
      console.error(`Transfer config not found: ${transferConfig.name}`);
    } else {
      console.error('An error occurred:', err);
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
from google.protobuf import field_mask_pb2


client = bigquery_datatransfer_v1.DataTransferServiceClient()


def update_transfer_config(
    project_id: str,
    location: str,
    transfer_config_id: str,
) -> None:
    """Updates a data transfer configuration.

    This sample shows how to update the display name for a transfer
    configuration.

    Args:
        project_id: The Google Cloud project ID.
        location: The geographic location of the transfer config, for example "us-central1"
        transfer_config_id: The transfer configuration ID
    """
    transfer_config_name = client.transfer_config_path(
        project=f"{project_id}/locations/{location}",
        transfer_config=transfer_config_id,
    )

    transfer_config = bigquery_datatransfer_v1.types.TransferConfig(
        name=transfer_config_name,
        display_name="My New Transfer Config display name",
    )
    update_mask = field_mask_pb2.FieldMask(paths=["display_name"])

    try:
        response = client.update_transfer_config(
            transfer_config=transfer_config,
            update_mask=update_mask,
        )

        print(f"Updated transfer config: {response.name}")
        print(f"New display name: {response.display_name}")
    except google.api_core.exceptions.NotFound:
        print(f"Error: Transfer config '{transfer_config_name}' not found.")
```

## 後續步驟

如要搜尋及篩選其他 Google Cloud 產品的程式碼範例，請參閱[Google Cloud 範例瀏覽工具](https://docs.cloud.google.com/docs/samples?product=bigquerydatatransfer&hl=zh-tw)。

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。




[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],[],[],[]]