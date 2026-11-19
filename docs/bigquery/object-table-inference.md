Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見

# 針對圖片物件資料表執行推論 透過集合功能整理內容 你可以依據偏好儲存及分類內容。

BigQuery 可讓您對[物件資料表](https://docs.cloud.google.com/bigquery/docs/object-table-introduction?hl=zh-tw)執行 SQL 查詢，分類或擷取 Cloud Storage 圖片中的特徵。您可以直接在 BigQuery 中套用自訂或預先訓練的影像模型，用於目錄標記、內容審核和瑕疵偵測，不必移動檔案或建構管道。

在本教學課程中，您將建立寵物產品範例圖片的物件資料表、匯入 ResNet-18 [ONNX](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-onnx?hl=zh-tw) 模型，並生成類別預測。

## 目標

* 建立 BigQuery 預留項目，以便在物件資料表上使用匯入的模型執行推論。
* 建立資料集、Cloud 資源連線，以及 Cloud Storage 中範例產品圖片的物件資料表。
* 將預先訓練的 ResNet-18 ONNX 模型匯入 BigQuery ML，並檢查其輸入和輸出欄位。
* 使用 `ML.DECODE_IMAGE`、`ML.RESIZE_IMAGE` 和 `ML.PREDICT` 函式預先處理及分類圖片。

## 費用

在本文件中，您會使用下列 Google Cloud計費元件：

* **BigQuery**: You incur slot capacity costs for the
  reservation that you create, storage costs for the object table, and query
  processing costs.
* **BigQuery ML**: You incur costs for creating the model
  and running inference in BigQuery ML.
* **Cloud Storage**: You incur costs if you store your own
  images or model artifacts in Cloud Storage.

您可以使用 [Pricing Calculator](https://docs.cloud.google.com/products/calculator?hl=zh-tw)，根據預測用量估算費用。

初次使用 Google Cloud 的使用者可能符合[免費試用期](https://docs.cloud.google.com/free?hl=zh-tw)資格。

詳情請參閱 [BigQuery 定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw)、[BigQuery ML 定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#bqml)和 [Cloud Storage 定價](https://cloud.google.com/storage/pricing?hl=zh-tw)。

## 事前準備

- 登入 Google Cloud 帳戶。如果您未曾使用過 Google Cloud，歡迎[建立帳戶](https://console.cloud.google.com/freetrial?hl=zh-tw)，親自體驗實際使用我們產品的成效。新客戶還能獲得價值 $300 美元的免費抵免額，用於執行、測試及部署工作負載。
- In the Google Cloud console, on the project selector page,
  select or create a Google Cloud project.

  **Roles required to select or create a project**

  * **Select a project**: Selecting a project doesn't require a specific
    IAM role—you can select any project that you've been
    granted a role on.
  * **Create a project**: To create a project, you need the Project Creator role
    (`roles/resourcemanager.projectCreator`), which contains the
    `resourcemanager.projects.create` permission. [Learn how to grant
    roles](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw).
  **Note**: If you don't plan to keep the
  resources that you create in this procedure, create a project instead of
  selecting an existing project. After you finish these steps, you can
  delete the project, removing all resources associated with the project.

  [Go to project selector](https://console.cloud.google.com/projectselector2/home/dashboard?hl=zh-tw)
- If you're using an existing project for this guide,
  [verify that you have
  the permissions required to complete this guide](#required-roles). If you created a new
  project, then you already have the required permissions.
- [Verify that billing is enabled for your Google Cloud project](https://docs.cloud.google.com/billing/docs/how-to/verify-billing-enabled?hl=zh-tw#confirm_billing_is_enabled_on_a_project).
- Enable the BigQuery, BigQuery Connection, and BigQuery Reservation APIs, if any are not already enabled.

  **Roles required to enable APIs**

  To enable APIs, you need the `serviceusage.services.enable` permission. If you
  created the project, then you likely already have this permission through the
  Owner role (`roles/owner`). Otherwise, you can get this permission through the
  Service Usage Admin role (`roles/serviceusage.serviceUsageAdmin`).
  [Learn how to grant roles](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw).

  [Enable the APIs](https://console.cloud.google.com/apis/enableflow?apiid=bigquery.googleapis.com%2Cbigqueryconnection.googleapis.com%2Cbigqueryreservation.googleapis.com&hl=zh-tw)

- In the Google Cloud console, on the project selector page,
  select or create a Google Cloud project.

  **Roles required to select or create a project**

  * **Select a project**: Selecting a project doesn't require a specific
    IAM role—you can select any project that you've been
    granted a role on.
  * **Create a project**: To create a project, you need the Project Creator role
    (`roles/resourcemanager.projectCreator`), which contains the
    `resourcemanager.projects.create` permission. [Learn how to grant
    roles](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw).
  **Note**: If you don't plan to keep the
  resources that you create in this procedure, create a project instead of
  selecting an existing project. After you finish these steps, you can
  delete the project, removing all resources associated with the project.

  [Go to project selector](https://console.cloud.google.com/projectselector2/home/dashboard?hl=zh-tw)
- If you're using an existing project for this guide,
  [verify that you have
  the permissions required to complete this guide](#required-roles). If you created a new
  project, then you already have the required permissions.
- [Verify that billing is enabled for your Google Cloud project](https://docs.cloud.google.com/billing/docs/how-to/verify-billing-enabled?hl=zh-tw#confirm_billing_is_enabled_on_a_project).
- Enable the BigQuery, BigQuery Connection, and BigQuery Reservation APIs, if any are not already enabled.

  **Roles required to enable APIs**

  To enable APIs, you need the `serviceusage.services.enable` permission. If you
  created the project, then you likely already have this permission through the
  Owner role (`roles/owner`). Otherwise, you can get this permission through the
  Service Usage Admin role (`roles/serviceusage.serviceUsageAdmin`).
  [Learn how to grant roles](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw).

  [Enable the APIs](https://console.cloud.google.com/apis/enableflow?apiid=bigquery.googleapis.com%2Cbigqueryconnection.googleapis.com%2Cbigqueryreservation.googleapis.com&hl=zh-tw)

### 必要的角色

如要取得完成本教學課程所需的權限，請要求管理員在專案中授予您下列 IAM 角色：

* 建立資料集、物件資料表和模型：[BigQuery 資料編輯者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.dataEditor) (`roles/bigquery.dataEditor`)
* 建立、委派及使用連線：[BigQuery 連線管理員](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.connectionAdmin) (`roles/bigquery.connectionAdmin`)
* 將權限授予連線的服務帳戶：[專案 IAM 管理員](https://docs.cloud.google.com/iam/docs/roles-permissions/resourcemanager?hl=zh-tw#resourcemanager.projectIamAdmin) (`roles/resourcemanager.projectIamAdmin`)
* 建立預留項目和預留項目指派作業：[BigQuery 資源管理員](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.resourceAdmin) (`roles/bigquery.resourceAdmin`)
* 執行 BigQuery 工作：[BigQuery 工作使用者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.jobUser) (`roles/bigquery.jobUser`)
* 將自訂模型或圖片上傳至 Cloud Storage (選用)：[Storage 物件管理員](https://docs.cloud.google.com/iam/docs/roles-permissions/storage?hl=zh-tw#storage.objectAdmin) (`roles/storage.objectAdmin`)

如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

您或許也能透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)，取得必要權限。

## 限制

使用匯入的模型對圖片物件資料表執行推論時，有下列限制：

* **定價和預留項目：**如要搭配物件資料表使用 BigQuery ML [匯入的模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/inference-overview?hl=zh-tw#inference_using_imported_models)，必須透過 [Enterprise 或 Enterprise Plus 版](https://docs.cloud.google.com/bigquery/docs/editions-intro?hl=zh-tw)的預留項目，採用依運算資源計價的模式。不支援隨選定價。
* **圖片檔：**物件資料表參照的圖片必須符合下列規定：
  + 每個圖片檔的大小不得超過 20 MB，且必須為 JPEG、PNG 或 BMP 格式。將圖片傳遞至 `ML.DECODE_IMAGE` 時，圖片大小不得超過 10 MB。
  + 物件資料表中所有圖片檔的總大小必須小於 1 TB。
  + 在物件資料表的 `uris` 選項中，最多指定 10 個來源 URI。如果指定超過 10 個 bucket URI，在列出大量檔案時，查詢可能會失敗並顯示 `Resources exceeded during query execution` 記憶體錯誤。如需參照超過 10 個 bucket，請將這些 bucket 分散到多個物件資料表。
* **匯入的模型：**模型必須符合下列規定：
  + 模型必須是 [TensorFlow](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-tensorflow?hl=zh-tw) 或 [TensorFlow Lite](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-tflite?hl=zh-tw) 模型，或是 [ONNX 格式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-onnx?hl=zh-tw)的 PyTorch 模型，且必須符合該模型類型的一般限制。
  + 序列化模型大小必須小於 450 MB，反序列化 (記憶體內) 模型大小則必須小於 1,000 MB。
  + 模型輸入張量的資料類型必須是 `tf.float32` (值為 `[0, 1)`) 或 `tf.uint8` (值為 `[0, 255)`)，形狀為 `[batch_size, width, height, 3]`，其中 `batch_size` 為 `-1`、`None` 或 `1`，且 `width` 和 `height` 大於 `0`。
  + 模型必須使用 `RGB`、`HSV`、`YIQ`、`YUV` 或 `GRAYSCALE` 色域的圖片進行訓練。您可以使用 [`ML.CONVERT_COLOR_SPACE` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-convert-color-space?hl=zh-tw)轉換輸入圖片，以符合模型的色域。

## 建立預留項目

如要使用匯入的模型，在物件資料表執行 BigQuery ML 推論，您必須為專案指派 BigQuery 預留項目 (Enterprise 或 Enterprise Plus 版本)，用於`QUERY`工作。如果專案已在 `US` 多區域指派預留項目，可以略過這個部分。

### 建立運算單元預留項目

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在導覽選單中，按一下「Workload management」(工作負載管理)。
3. 點選「Create reservation」(建立預留項目)。
4. 在「Create reservation」(建立預留項目) 頁面，設定預留項目：

   1. 在「Reservation name」(預留項目名稱) 欄位輸入 `bqml-tutorial-reservation`。
   2. 在「位置」部分，選取「us (多個美國區域)」。
   3. 其他設定均保留預設值，然後點選「Save」(儲存)。

### 將預留項目指派給專案

1. 在「Capacity management」(容量管理) 頁面的「Slot reservations」(運算單元預留項目) 表格中，找到 `bqml-tutorial-reservation`。
2. 依序點選「more\_vert
   **動作」>「建立作業」**。
3. 在「Create an assignment」(建立指派作業) 窗格中，按一下「Browse」(瀏覽)，然後選取您的專案。
4. 在「Job type」(工作類型) 部分，選取「QUERY」(查詢)。
5. 點選「建立」。

## 建立資料集

在 `US` 多區域中建立 `bqml_tutorial` 資料集，用於儲存物件資料表和匯入的模型。

如要建立 BigQuery 資料集，請選取下列其中一個選項：

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。

   如果沒有看到左側窗格，請按一下 last\_page「Expand left pane」(展開左側窗格)，開啟窗格。
3. 在「Explorer」中展開專案，然後點選「資料集」。
4. 在「Datasets」(資料集) 頁面，按一下「Create dataset」(建立資料集)。add
5. 在「建立資料集」窗格中，執行下列操作：

   * 在「Dataset ID」(資料集 ID) 中輸入 `bqml_tutorial`。
   * 在「資料位置」部分，選取「US」。

   其餘設定均保留預設值。
6. 點選「建立資料集」。

### bq

如要建立新的資料集，請使用 [`bq mk --dataset` 指令](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#mk-dataset)。

1. 建立名為 `bqml_tutorial` 的資料集，並將資料位置設為 `US`：

   ```
   bq mk --dataset \
     --location=US \
     --description "BigQuery ML tutorial dataset." \
     bqml_tutorial
   ```
2. 確認資料集已建立：

   ```
   bq ls
   ```

### API

使用定義的[資料集資源](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/datasets?hl=zh-tw)呼叫 [`datasets.insert`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/datasets/insert?hl=zh-tw) 方法：

```
{
  "datasetReference": {
     "datasetId": "bqml_tutorial"
  }
}
```

## 建立連線

在建立資料集的 `US` 多區域中，建立 [Cloud 資源連結](https://docs.cloud.google.com/bigquery/docs/create-cloud-resource-connection?hl=zh-tw)，然後複製連結的服務帳戶 ID。BigQuery 會使用這個連線，從 Cloud Storage 讀取圖片檔。

選取下列選項之一：

### 控制台

1. 前往「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。

   如果沒有看到左側窗格，請按一下 last\_page「Expand left pane」(展開左側窗格)，開啟窗格。
3. 在「Explorer」窗格中展開專案名稱，然後點選「Connections」(連線)。
4. 在「Connections」(連線) 頁面，按一下「Create connection」(建立連線)。
5. 在「連線類型」部分，選擇「Vertex AI 遠端模型、遠端函式、BigLake 和 Spanner (Cloud 資源)」。
6. 在「連線 ID」欄位中，輸入連線名稱。
7. 在「位置類型」部分，選取連線位置。連線應與其他資源 (例如資料集) 位於相同位置。
8. 點選「建立連線」。
9. 點選「前往連線」。
10. 在「連線資訊」窗格中，複製服務帳戶 ID，以便在後續步驟中使用。

### SQL

使用 [`CREATE CONNECTION` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#create_connection_statement)：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列陳述式：

   ```
   CREATE CONNECTION [IF NOT EXISTS] `CONNECTION_NAME`
   OPTIONS (
     connection_type = "CLOUD_RESOURCE",
     friendly_name = "FRIENDLY_NAME",
     description = "DESCRIPTION"
     );
   ```

   替換下列內容：

   * `CONNECTION_NAME`：連線名稱，格式為 `PROJECT_ID.LOCATION.CONNECTION_ID`、`LOCATION.CONNECTION_ID` 或 `CONNECTION_ID`。如果省略專案或位置，系統會根據執行陳述式的專案和位置推斷。
   * `FRIENDLY_NAME` (選用)：連線的描述性名稱。
   * `DESCRIPTION` (選用)：連線說明。
3. 按一下「play\_circle 執行」。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

### bq

1. 在指令列環境中建立連線：

   ```
   bq mk --connection --location=REGION --project_id=PROJECT_ID \
       --connection_type=CLOUD_RESOURCE CONNECTION_ID
   ```

   `--project_id` 參數會覆寫預設專案。

   更改下列內容：

   * `REGION`：[連線區域](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw#supported_locations)
   * `PROJECT_ID`：您的 Google Cloud 專案 ID
   * `CONNECTION_ID`：連線 ID

   建立連線資源時，BigQuery 會建立專屬的系統服務帳戶，並與連線建立關聯。

   **疑難排解**：如果收到下列連線錯誤訊息，請[更新 Google Cloud SDK](https://docs.cloud.google.com/sdk/docs/quickstart?hl=zh-tw)：

   ```
   Flags parsing error: flag --connection_type=CLOUD_RESOURCE: value should be one of...
   ```
2. 擷取並複製服務帳戶 ID，以便在後續步驟中使用：

   ```
   bq show --connection PROJECT_ID.REGION.CONNECTION_ID
   ```

   輸出結果會與下列內容相似：

   ```
   name                          properties
   1234.REGION.CONNECTION_ID     {"serviceAccountId": "connection-1234-9u56h9@gcp-sa-bigquery-condel.iam.gserviceaccount.com"}
   ```

### Python

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Python 設定操作說明進行操作。詳情請參閱 [BigQuery Python API 參考文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import google.api_core.exceptions
from google.cloud import bigquery_connection_v1

client = bigquery_connection_v1.ConnectionServiceClient()


def create_connection(
    project_id: str,
    location: str,
    connection_id: str,
):
    """Creates a BigQuery connection to a Cloud Resource.

    Cloud Resource connection creates a service account which can then be
    granted access to other Google Cloud resources for federated queries.

    Args:
        project_id: The Google Cloud project ID.
        location: The location of the connection (for example, "us-central1").
        connection_id: The ID of the connection to create.
    """

    parent = client.common_location_path(project_id, location)

    connection = bigquery_connection_v1.Connection(
        friendly_name="Example Connection",
        description="A sample connection for a Cloud Resource.",
        cloud_resource=bigquery_connection_v1.CloudResourceProperties(),
    )

    try:
        created_connection = client.create_connection(
            parent=parent, connection_id=connection_id, connection=connection
        )
        print(f"Successfully created connection: {created_connection.name}")
        print(f"Friendly name: {created_connection.friendly_name}")
        print(
            f"Service Account: {created_connection.cloud_resource.service_account_id}"
        )

    except google.api_core.exceptions.AlreadyExists:
        print(f"Connection with ID '{connection_id}' already exists.")
        print("Please use a different connection ID.")
    except Exception as e:
        print(f"An unexpected error occurred while creating the connection: {e}")
```

### Node.js

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Node.js 設定操作說明進行操作。詳情請參閱 [BigQuery Node.js API 參考文件](https://googleapis.dev/nodejs/bigquery/latest/index.html)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
const {ConnectionServiceClient} =
  require('@google-cloud/bigquery-connection').v1;
const {status} = require('@grpc/grpc-js');

const client = new ConnectionServiceClient();

/**
 * Creates a new BigQuery connection to a Cloud Resource.
 *
 * A Cloud Resource connection creates a service account that can be granted access
 * to other Google Cloud resources.
 *
 * @param {string} projectId The Google Cloud project ID. for example, 'example-project-id'
 * @param {string} location The location of the project to create the connection in. for example, 'us-central1'
 * @param {string} connectionId The ID of the connection to create. for example, 'example-connection-id'
 */
async function createConnection(projectId, location, connectionId) {
  const parent = client.locationPath(projectId, location);

  const connection = {
    friendlyName: 'Example Connection',
    description: 'A sample connection for a Cloud Resource',
    // The service account for this cloudResource will be created by the API.
    // Its ID will be available in the response.
    cloudResource: {},
  };

  const request = {
    parent,
    connectionId,
    connection,
  };

  try {
    const [response] = await client.createConnection(request);

    console.log(`Successfully created connection: ${response.name}`);
    console.log(`Friendly name: ${response.friendlyName}`);

    console.log(`Service Account: ${response.cloudResource.serviceAccountId}`);
  } catch (err) {
    if (err.code === status.ALREADY_EXISTS) {
      console.log(`Connection '${connectionId}' already exists.`);
    } else {
      console.error(`Error creating connection: ${err.message}`);
    }
  }
}
```

### Java

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Java 設定操作說明進行操作。詳情請參閱 [BigQuery Java API 參考文件](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/overview?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import com.google.api.gax.rpc.AlreadyExistsException;
import com.google.api.gax.rpc.ApiException;
import com.google.cloud.bigquery.connection.v1.CloudResourceProperties;
import com.google.cloud.bigquery.connection.v1.Connection;
import com.google.cloud.bigquery.connection.v1.CreateConnectionRequest;
import com.google.cloud.bigquery.connection.v1.LocationName;
import com.google.cloud.bigqueryconnection.v1.ConnectionServiceClient;
import java.io.IOException;

public class CreateConnection {

  /**
   * Creates a BigQuery connection to a Cloud Resource. A Cloud Resource connection provisions a
   * service account that can be granted access to other Google Cloud resources for federated
   * queries.
   *
   * @param projectId The Google Cloud project ID (for example, "example-project-id").
   * @param location The geographic location of the connection (for example, "us-central1").
   * @param connectionId The ID of the connection to create (for example, "example-connection-id").
   */
  public static void createConnection(String projectId, String location, String connectionId) {
    LocationName parent = LocationName.of(projectId, location);

    // CloudResourceProperties provisions a managed Google Cloud service account on creation.
    CloudResourceProperties cloudResourceProperties = CloudResourceProperties.newBuilder().build();
    Connection connection =
        Connection.newBuilder()
            .setFriendlyName("Example Connection")
            .setDescription("Cloud Resource connection for federated queries.")
            .setCloudResource(cloudResourceProperties)
            .build();

    CreateConnectionRequest request =
        CreateConnectionRequest.newBuilder()
            .setParent(parent.toString())
            .setConnectionId(connectionId)
            .setConnection(connection)
            .build();

    try (ConnectionServiceClient client = ConnectionServiceClient.create()) {
      Connection response = client.createConnection(request);

      System.out.printf("Successfully created connection: %s%n", response.getName());
      System.out.printf("Friendly name: %s%n", response.getFriendlyName());
      System.out.printf(
          "Service Account: %s%n", response.getCloudResource().getServiceAccountId());
    } catch (AlreadyExistsException err) {
      System.err.printf(
          "error: connection '%s' already exists in location '%s' for project '%s': %s%n",
          connectionId, location, projectId, err.getMessage());
    } catch (ApiException | IOException err) {
      System.err.printf(
          "error: failed to create connection '%s' in location '%s' for project '%s': %s%n",
          connectionId, location, projectId, err.getMessage());
    }
  }
```

### Terraform

使用 [`google_bigquery_connection`](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/bigquery_connection) 資源。

**注意：**如要使用 Terraform 建立 BigQuery 物件，必須啟用 [Cloud Resource Manager API](https://docs.cloud.google.com/resource-manager/reference/rest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

下列範例會在 `US` 區域中建立名為 `my_cloud_resource_connection` 的 Cloud 資源連結：

```
# This queries the provider for project information.
data "google_project" "default" {}

# This creates a cloud resource connection in the US region named my_cloud_resource_connection.
# Note: The cloud resource nested object has only one output field - serviceAccountId.
resource "google_bigquery_connection" "default" {
  connection_id = "my_cloud_resource_connection"
  project       = data.google_project.default.project_id
  location      = "US"
  cloud_resource {}
}
```

如要在 Google Cloud 專案中套用 Terraform 設定，請完成下列各節的步驟。

## 準備 Cloud Shell

1. 啟動 [Cloud Shell](https://shell.cloud.google.com/?hl=zh-tw)。
2. 設定要套用 Terraform 設定的預設 Google Cloud 專案。

   這項指令在每個專案中只需執行一次，且可在任何目錄中執行。

   ```
   export GOOGLE_CLOUD_PROJECT=PROJECT_ID
   ```

   如果您在 Terraform 設定檔中設定明確的值，環境變數就會遭到覆寫。

## 準備目錄

每個 Terraform 設定檔都必須有自己的目錄 (也稱為「根模組」)。

1. 在 [Cloud Shell](https://shell.cloud.google.com/?hl=zh-tw) 中建立目錄，並在該目錄中建立新檔案。檔案名稱必須有 `.tf` 副檔名，例如 `main.tf`。在本教學課程中，這個檔案稱為 `main.tf`。

   ```
   mkdir DIRECTORY && cd DIRECTORY && touch main.tf
   ```
2. 如果您正在進行教學課程，可以複製每個章節或步驟中的程式碼範例。

   將程式碼範例複製到新建立的 `main.tf`。

   您也可以從 GitHub 複製程式碼。如果 Terraform 程式碼片段是端對端解決方案的一部分，建議您採用這種做法。
3. 請查看並修改範例參數，以便套用至您的環境。
4. 儲存變更。
5. 初始化 Terraform。每個目錄只需執行一次這項操作。

   ```
   terraform init
   ```

   如要使用最新版 Google 供應商，請視需要加入 `-upgrade` 選項：

   ```
   terraform init -upgrade
   ```

## 套用變更

1. 查看設定，確認 Terraform 要建立或更新的資源符合預期：

   ```
   terraform plan
   ```

   視需要修正設定。
2. 執行下列指令，並在提示中輸入 `yes`，套用 Terraform 設定：

   ```
   terraform apply
   ```

   等待 Terraform 顯示「Apply complete!」訊息。
3. [開啟 Google Cloud 專案](https://console.cloud.google.com/?hl=zh-tw)即可查看結果。在 Google Cloud 控制台的 UI 中前往資源，確認 Terraform 已建立或更新資源。

**注意：**Terraform 範例通常會假設 Google Cloud 專案已啟用必要的 API。

### 將權限授予連線的服務帳戶

將 Storage 物件檢視者 (`roles/storage.objectViewer`) 角色授予連線的服務帳戶，讓物件資料表能讀取 Cloud Storage 中的圖片檔：

### 控制台

1. 前往「IAM & Admin」(IAM 與管理) 頁面。

   [前往「IAM & Admin」(IAM 與管理) 頁面](https://console.cloud.google.com/project/_/iam-admin?hl=zh-tw)
2. 按一下person\_add「Grant access」(授予存取權)。
3. 在「新增主體」欄位，輸入先前複製的服務帳戶 ID。
4. 在「Select a role」(請選擇角色) 欄位中，依序選取「Cloud Storage」和「Storage Object Viewer」(Storage 物件檢視者)。
5. 按一下「儲存」。

### gcloud

使用 [`gcloud projects add-iam-policy-binding`](https://docs.cloud.google.com/sdk/gcloud/reference/projects/add-iam-policy-binding?hl=zh-tw) 指令：

```
gcloud projects add-iam-policy-binding PROJECT_ID \
    --member='serviceAccount:MEMBER' \
    --role='roles/storage.objectViewer' \
    --condition=None
```

更改下列內容：

* `PROJECT_ID`：您的 Google Cloud 專案 ID
* `MEMBER`：您先前複製的服務帳戶 ID

## 建立物件資料表

使用 [`CREATE EXTERNAL TABLE` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#create_external_table_statement)，在 Cymbal Pets 產品圖片的公開 Cloud Storage bucket 上，建立名為 `product_images` 的[物件資料表](https://docs.cloud.google.com/bigquery/docs/object-tables?hl=zh-tw)：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中執行下列陳述式：

   ```
   CREATE OR REPLACE EXTERNAL TABLE `bqml_tutorial.product_images`
     WITH CONNECTION `us.CONNECTION_ID`
     OPTIONS (
       object_metadata = 'SIMPLE',
       uris = ['gs://cloud-samples-data/bigquery/tutorials/cymbal-pets/images/*.png']
     );
   ```

   將 `CONNECTION_ID` 替換為您建立的 BigQuery 連線 ID，例如 `myconnection`。在 Google Cloud 控制台中[查看連線詳細資料](https://docs.cloud.google.com/bigquery/docs/working-with-connections?hl=zh-tw#view-connections)時，這個值是「Connection ID」(連線 ID) 中顯示的完整 ID 的最後一個區段 (例如 `projects/myproject/locations/us/connections/myconnection`)。

## 將模型匯入 BigQuery ML

使用 [`CREATE MODEL` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-onnx?hl=zh-tw)，從公開 Cloud Storage bucket 將預先建構的 ResNet-18 圖片分類模型 (ONNX 格式) 匯入資料集。如要使用自己的 TensorFlow、TensorFlow Lite 或 ONNX 模型，請[將模型構件上傳](https://docs.cloud.google.com/storage/docs/uploading-objects?hl=zh-tw)至 Cloud Storage bucket，並在 `MODEL_PATH` 中指定 bucket URI。

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中執行下列陳述式：

   ```
   CREATE OR REPLACE MODEL `bqml_tutorial.imported_onnx_model`
     OPTIONS (
       MODEL_TYPE = 'ONNX',
       MODEL_PATH = 'gs://cloud-samples-data/bigquery/ml/onnx/resnet18.onnx'
     );
   ```

   查詢會在幾秒內完成，完成後，`imported_onnx_model` 會顯示在「Explorer」窗格的 `bqml_tutorial` 資料集中。由於查詢使用 `CREATE MODEL` 陳述式，因此沒有查詢結果。

## 檢查模型

檢查匯入的模型，找出預期的輸入和輸出欄位名稱。對物件資料表執行推論時，您會參照這些欄位名稱：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。如果沒有看到左側窗格，請按一下 last\_page「Expand left pane」(展開左側窗格)，開啟窗格。
3. 在「Explorer」窗格中展開專案，依序點選「Datasets」(資料集) 和 `bqml_tutorial`。
4. 按一下「Models」分頁標籤，然後點選 `imported_onnx_model`。

   * 「Label Column」(標籤欄) 顯示模型傳回的輸出欄位：`class_label` (`INT64`)，代表預測的 [ImageNet 類別 ID](https://raw.githubusercontent.com/pytorch/hub/master/imagenet_classes.txt)。
   * **「Feature Columns」(特徵欄)** 顯示模型預期的輸入欄位：`input` (`FLOAT64` `REPEATED`)。對於 ResNet-18，每個解碼圖片的大小必須調整為 `224` 乘以 `224` 像素，並別名為 `input`。

   如果您匯入自己的 TensorFlow SavedModel，且需要檢查確切的輸入張量維度，請在本機安裝 TensorFlow，並執行 [`saved_model_cli show` 指令](https://www.tensorflow.org/guide/saved_model?hl=zh-tw#show_command)。

## 對物件資料表執行推論

使用 [`ML.PREDICT` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-predict?hl=zh-tw)，分類 `product_images` 物件資料表中的球類產品圖片。在輸入子查詢中，[`ML.DECODE_IMAGE` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-decode-image?hl=zh-tw)會將物件資料表 `data` 欄中的原始圖片位元組轉換為多維 `ARRAY`，而 [`ML.RESIZE_IMAGE` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-resize-image?hl=zh-tw)會將每張圖片的大小調整為 `224` x `224` 像素，以符合模型的 `input` 特徵。如果模型需要不同的色域或 `[0, 255)` 整數像素值，您也可以鏈結 [`ML.CONVERT_COLOR_SPACE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-convert-color-space?hl=zh-tw) 或 [`ML.CONVERT_IMAGE_TYPE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-convert-image-type?hl=zh-tw) 函式。

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器執行下列陳述式，將物件資料表中 URI 含有 *ball* 一詞的產品分類：

   ```
   SELECT
     uri,
     class_label
   FROM
     ML.PREDICT(
       MODEL `bqml_tutorial.imported_onnx_model`,
       (
         SELECT
           uri,
           ML.RESIZE_IMAGE(ML.DECODE_IMAGE(data), 224, 224, FALSE) AS input
         FROM
           `bqml_tutorial.product_images`
         WHERE
           uri LIKE '%-ball%'
       )
     );
   ```

   輸出結果會與下列內容相似：

   ```
   +-----------------------------------------------------------------------------------------------------+-------------+
   | uri                                                                                                 | class_label |
   +-----------------------------------------------------------------------------------------------------+-------------+
   | gs://cloud-samples-data/bigquery/tutorials/cymbal-pets/images/playful-pup-tennis-ball.png           | 852         |
   | gs://cloud-samples-data/bigquery/tutorials/cymbal-pets/images/cozy-naps-catnip-toy-ball.png         | 911         |
   | gs://cloud-samples-data/bigquery/tutorials/cymbal-pets/images/fluffy-buns-hamster-exercise-ball.png | 768         |
   | ...                                                                                                 | ...         |
   +-----------------------------------------------------------------------------------------------------+-------------+
   ```

   每個 `class_label` 值都會對應至 [ImageNet 標籤](https://raw.githubusercontent.com/pytorch/hub/master/imagenet_classes.txt)清單中以零為索引的項目。例如，`852` 對應 Playful Pup 網球產品圖片的 `tennis ball`。

## 儲存預先處理的圖片，以便重複推論

如果您打算執行多個推論查詢，或在相同圖片上比較多個模型，可以將解碼和調整大小後的圖片陣列具體化，並儲存在標準 BigQuery 資料表中，這樣就不必在每次查詢時解碼原始圖片檔：

1. 在查詢編輯器中，將解碼和調整大小後的圖片寫入標準資料表：

   ```
   CREATE OR REPLACE TABLE `bqml_tutorial.preprocessed_images` AS (
     SELECT
       uri,
       ML.RESIZE_IMAGE(ML.DECODE_IMAGE(data), 224, 224, FALSE) AS input
     FROM
       `bqml_tutorial.product_images`
     WHERE
       uri LIKE '%-ball%'
   );
   ```
2. 直接在 `preprocessed_images` 資料表上執行 `ML.PREDICT`：

   ```
   SELECT
     uri,
     class_label
   FROM
     ML.PREDICT(
       MODEL `bqml_tutorial.imported_onnx_model`,
       (
         SELECT
           uri,
           input
         FROM
           `bqml_tutorial.preprocessed_images`
       )
     );
   ```

   查詢會傳回相同的 `uri` 和 `class_label` 預測結果，不會重新讀取或解碼 Cloud Storage 中的來源 PNG 檔案。

## 清除所用資源

為避免因為本教學課程所用資源，導致系統向 Google Cloud 收取費用，請刪除含有相關資源的專案，或者保留專案但刪除個別資源。

### 刪除專案

**注意**：刪除專案會造成以下影響：

* **專案中的所有內容都會遭到刪除。**如果使用現有專案來進行本文中的任務，刪除專案將一併移除當中已完成的其他任務'。
* **自訂專案 ID 會消失。**當您之前建立這個專案時，可能建立了想要在日後使用的自訂專案 ID。如要保留使用該專案 ID 的網址 (例如 `appspot.com` 網址)，請刪除在該專案中選取的資源，而不是刪除整個專案。

如果打算探索多種架構、教學課程或快速入門導覽課程，重複使用專案可避免超出專案配額限制。

刪除 Google Cloud 專案：

```
gcloud projects delete PROJECT_ID
```

### 刪除個別資源

如要重複使用專案，請刪除您為本教學課程建立的個別資源：

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 刪除 `bqml_tutorial` 資料集。刪除資料集也會一併刪除物件資料表、`preprocessed_images` 資料表和匯入的模型：

   1. 在「Explorer」窗格中展開專案，然後點選「資料集」。
   2. 按一下「`bqml_tutorial`」。
   3. 在詳細資料窗格中，按一下「delete 刪除」。
   4. 在「Delete dataset」(刪除資料集) 對話方塊中，按一下「Delete」(刪除)。
3. 刪除連結：

   1. 在「Explorer」窗格中展開專案，然後按一下「Connections」(連結)。
   2. 按一下您建立的連線。
   3. 在詳細資料窗格中，按一下「delete 刪除」。
   4. 在「Delete connection」(刪除連線) 對話方塊中輸入 `delete`，然後按一下「Delete」(刪除)。
4. 如果您為本教學課程建立了 `bqml-tutorial-reservation` 預留項目，請刪除指派作業和預留項目，以免持續產生運算單元費用：

   1. 在導覽選單中，點選「容量管理」。
   2. 在「Slot reservations」(運算單元預留項目) 表格中，展開 `bqml-tutorial-reservation`。
   3. 依序點選專案指派項目旁的more\_vert「Actions」(動作)**>「Delete」(刪除)**，然後確認刪除。
   4. 依序點選 `bqml-tutorial-reservation` 旁的 more\_vert「Actions」(動作) >「Delete」(刪除)，然後確認刪除。

### bq

1. 刪除 `bqml_tutorial` 資料集，以及當中的所有資料表和模型：

   ```
   bq rm --dataset --recursive --force bqml_tutorial
   ```
2. 刪除連結：

   ```
   bq rm --connection PROJECT_ID.us.CONNECTION_ID
   ```

   更改下列內容：

   * `PROJECT_ID`：專案 ID
   * `CONNECTION_ID`：您建立的連線 ID
3. 如果您建立了 `bqml-tutorial-reservation` 預留項目，請移除其專案指派作業，並刪除預留項目：

   ```
   bq rm --project_id=PROJECT_ID --location=us \
     --reservation_assignment \
     bqml-tutorial-reservation.ASSIGNMENT_ID
   bq rm --project_id=PROJECT_ID --location=us \
     --reservation bqml-tutorial-reservation
   ```

   更改下列內容：

   * `PROJECT_ID`：專案 ID
   * `ASSIGNMENT_ID`：預留項目指派作業的 ID。如要取得指派作業 ID，請參閱「[尋找專案的預留項目指派作業](https://docs.cloud.google.com/bigquery/docs/reservations-assignments?hl=zh-tw#list-assignment)」。

## 後續步驟

* 嘗試[使用 ResNet 50 分類模型，對物件資料表執行推論](https://docs.cloud.google.com/bigquery/docs/inference-tutorial-resnet?hl=zh-tw)。
* 嘗試[使用 MobileNet V3 特徵向量模型，對物件資料表執行推論](https://docs.cloud.google.com/bigquery/docs/inference-tutorial-mobilenet?hl=zh-tw)。
* 瞭解如何[使用 Gemini 模型分析圖片](https://docs.cloud.google.com/bigquery/docs/image-analysis?hl=zh-tw)，或[使用 `ML.ANNOTATE_IMAGE` 函式為圖片加上註解](https://docs.cloud.google.com/bigquery/docs/annotate-image?hl=zh-tw)。
* 瞭解如何[使用遠端函式分析物件資料表](https://docs.cloud.google.com/bigquery/docs/object-table-remote-function?hl=zh-tw)。
* 如需更多圖片預先處理範例，請參閱 [`ML.DECODE_IMAGE` 參考文件](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-decode-image?hl=zh-tw#examples)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-11-18 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-11-18 (世界標準時間)。"],[],[]]