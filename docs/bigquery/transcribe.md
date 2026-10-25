Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 使用 ML.TRANSCRIBE 函式轉錄音訊檔案

本教學課程說明如何轉錄音訊檔案 (例如客服通話、Podcast 或會議錄音)，擷取文字用於下游分析、關鍵字搜尋或情緒分析。

您將使用 [`ML.TRANSCRIBE` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-transcribe?hl=zh-tw)和[遠端模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model-service?hl=zh-tw)，轉錄儲存在[物件資料表](https://docs.cloud.google.com/bigquery/docs/object-table-introduction?hl=zh-tw)中的音訊檔案。

## 支援的地區

您必須在下列其中一個[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)建立本程序使用的遠端模型：

* `asia-northeast1`
* `asia-south1`
* `asia-southeast1`
* `australia-southeast1`
* `eu`
* `europe-west1`
* `europe-west2`
* `europe-west3`
* `europe-west4`
* `northamerica-northeast1`
* `us`
* `us-central1`
* `us-east1`
* `us-east4`
* `us-west1`

您必須在遠端模型所在的區域中執行 `ML.TRANSCRIBE` 函式。

## 必要的角色

如要建立遠端模型並轉錄音訊檔案，您必須在專案層級具備下列 Identity and Access Management (IAM) 角色：

* 建立語音辨識器：Cloud Speech 編輯者 (`roles/speech.editor`)
* 建立及使用 BigQuery 資料集、資料表和模型：BigQuery 資料編輯者 (`roles/bigquery.dataEditor`)
* 建立、委派及使用 BigQuery 連線：BigQuery 連線管理員 (`roles/bigquery.connectionsAdmin`)

  如果您未設定[預設連線](https://docs.cloud.google.com/bigquery/docs/default-connections?hl=zh-tw)，可以在執行 `CREATE MODEL` 陳述式時建立並設定。如要執行這項操作，您必須具備專案的 BigQuery 管理員 (`roles/bigquery.admin`) 角色。詳情請參閱「[設定預設連線](https://docs.cloud.google.com/bigquery/docs/default-connections?hl=zh-tw#configure_the_default_connection)」。
* 將權限授予連線的服務帳戶：專案 IAM 管理員 (`roles/resourcemanager.projectIamAdmin`)
* 建立 BigQuery 工作：BigQuery 工作使用者 (`roles/bigquery.jobUser`)

這些預先定義的角色具備執行本文件所述工作所需的權限。如要查看確切的必要權限，請展開「Required permissions」(必要權限) 部分：

#### 所需權限

* 建立資料集：`bigquery.datasets.create`
* 建立、委派及使用連線：
  `bigquery.connections.*`
* 設定服務帳戶權限：`resourcemanager.projects.getIamPolicy`和`resourcemanager.projects.setIamPolicy`
* 建立模型並執行推論：
  + `bigquery.jobs.create`
  + `bigquery.models.create`
  + `bigquery.models.getData`
  + `bigquery.models.updateData`
  + `bigquery.models.updateMetadata`
* 建立物件資料表：`bigquery.tables.create` 和 `bigquery.tables.update`
* 建立語音辨識器：
  + `speech.recognizers.create`
  + `speech.recognizers.get`
  + `speech.recognizers.recognize`
  + `speech.recognizers.update`

您或許還可透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-permissions?hl=zh-tw)取得這些權限。

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
- [Verify that billing is enabled for your Google Cloud project](https://docs.cloud.google.com/billing/docs/how-to/verify-billing-enabled?hl=zh-tw#confirm_billing_is_enabled_on_a_project).
- Enable the BigQuery, BigQuery Connection API, and Speech-to-Text APIs, if any are not already enabled.

  **Roles required to enable APIs**

  To enable APIs, you need the `serviceusage.services.enable` permission. If you
  created the project, then you likely already have this permission through the
  Owner role (`roles/owner`). Otherwise, you can get this permission through the
  Service Usage Admin role (`roles/serviceusage.serviceUsageAdmin`).
  [Learn how to grant roles](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw).

  [Enable the APIs](https://console.cloud.google.com/apis/enableflow?apiid=bigquery.googleapis.com%2Cbigqueryconnection.googleapis.com%2Cspeech.googleapis.com&hl=zh-tw)

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
- [Verify that billing is enabled for your Google Cloud project](https://docs.cloud.google.com/billing/docs/how-to/verify-billing-enabled?hl=zh-tw#confirm_billing_is_enabled_on_a_project).
- Enable the BigQuery, BigQuery Connection API, and Speech-to-Text APIs, if any are not already enabled.

  **Roles required to enable APIs**

  To enable APIs, you need the `serviceusage.services.enable` permission. If you
  created the project, then you likely already have this permission through the
  Owner role (`roles/owner`). Otherwise, you can get this permission through the
  Service Usage Admin role (`roles/serviceusage.serviceUsageAdmin`).
  [Learn how to grant roles](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw).

  [Enable the APIs](https://console.cloud.google.com/apis/enableflow?apiid=bigquery.googleapis.com%2Cbigqueryconnection.googleapis.com%2Cspeech.googleapis.com&hl=zh-tw)

## 費用

在本文件中，您會使用下列 Google Cloud計費元件：

* [BigQuery](https://cloud.google.com/bigquery/pricing?hl=zh-tw)
* [Speech-to-Text](https://cloud.google.com/speech-to-text/pricing?hl=zh-tw)

您可以使用 [Pricing Calculator](https://docs.cloud.google.com/products/calculator?hl=zh-tw)，根據預測用量估算費用。

初次使用 Google Cloud 的使用者可能符合[免費試用期](https://docs.cloud.google.com/free?hl=zh-tw)資格。

## 建立辨識器

Speech-to-Text 支援稱為辨識器的資源。辨識器代表已儲存且可重複使用的辨識設定。您可以[建立辨識器](https://docs.cloud.google.com/speech-to-text/v2/docs/recognizers?hl=zh-tw)，以邏輯方式將應用程式的語音轉錄或流量分組。

您可以選擇是否要建立語音辨識器。如果選擇建立語音辨識器，請記下辨識器的專案 ID、位置和辨識器 ID，以便在 `CREATE MODEL` 陳述式中使用，詳情請參閱「[`SPEECH_RECOGNIZER`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model-service?hl=zh-tw#speech_recognizer)」。如果選擇不建立語音辨識器，則必須為 `ML.TRANSCRIBE` 函式的 [`recognition_config` 引數](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-transcribe?hl=zh-tw#arguments)指定值。

您只能在語音辨識工具或提供的 `recognition_config` 值中，使用 `chirp`
[語音轉錄模型](https://docs.cloud.google.com/speech-to-text/v2/docs/transcription-model?hl=zh-tw#transcription_models)。

## 建立資料集

建立 BigQuery 資料集來存放資源：

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。

   如果沒有看到左側窗格，請按一下 last\_page「Expand left pane」(展開左側窗格)，開啟窗格。
3. 在「Explorer」窗格中，點選專案名稱。
4. 依序點選 more\_vert「View actions」(查看動作)**>「Create dataset」(建立資料集)**。
5. 在「Create dataset」(建立資料集) 頁面執行下列操作：

   1. 在「資料集 ID」部分，輸入資料集名稱。
   2. 在「位置類型」部分，選取「區域」或「多區域」。

      * 如果選取「Region」(區域)，請從「Region」(區域) 清單中選取位置。
      * 如果選取「Multi-region」(多區域)，請從「Multi-region」(多區域) 清單中選取「US」(美國) 或「Europe」(歐洲)。
   3. 點選「建立資料集」。

### bq

1. 如要建立新的資料集，請使用 [`bq mk`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#mk-dataset) 指令並加上 `--location` 旗標：

   ```
   bq --location=LOCATION mk -d DATASET_ID
   ```

   更改下列內容：

   * `LOCATION`：資料集的[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)。
   * `DATASET_ID`：您要建立的資料集 ID。
2. 確認資料集已建立：

   ```
   bq ls
   ```

## 建立連線

建立 [Cloud 資源連結](https://docs.cloud.google.com/bigquery/docs/create-cloud-resource-connection?hl=zh-tw)，並取得連結的服務帳戶。建立連線時，請選擇與上一步建立的資料集相同的[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)。

如果您已設定預設連線，或具備 BigQuery 管理員角色，則可略過這個步驟。

選取下列選項之一：

### 控制台

1. 前往「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。

   如果沒有看到左側窗格，請按一下 last\_page「Expand left pane」(展開左側窗格)，開啟窗格。
3. 在「Explorer」窗格中展開專案名稱，然後點選「Connections」(連線)。
4. 在「Connections」(連線) 頁面，按一下「Create connection」(建立連線)。
5. 在「連線類型」部分，選擇「Vertex AI 遠端模型、遠端函式、BigLake 和 Spanner (Cloud 資源)」。
6. 在「連線 ID」欄位輸入連線名稱。
7. 在「位置類型」部分，選取連線位置。連線應與資料集等其他資源位於相同位置。
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

   * `CONNECTION_NAME`：連線名稱，格式為 `PROJECT_ID.LOCATION.CONNECTION_ID`、`LOCATION.CONNECTION_ID` 或 `CONNECTION_ID`。如果省略專案或位置，系統會根據執行陳述式的專案和位置推論。
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

   **疑難排解**：如果收到下列連線錯誤，請[更新 Google Cloud SDK](https://docs.cloud.google.com/sdk/docs/quickstart?hl=zh-tw)：

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

**注意：** 如要使用 Terraform 建立 BigQuery 物件，必須啟用 [Cloud Resource Manager API](https://docs.cloud.google.com/resource-manager/reference/rest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

下列範例會在 `US` 區域建立名為 `my_cloud_resource_connection` 的 Cloud 資源連結：

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

   每個專案只需執行這個指令一次，而且可以在任何目錄中執行。

   ```
   export GOOGLE_CLOUD_PROJECT=PROJECT_ID
   ```

   如果您在 Terraform 設定檔中設定明確的值，環境變數就會遭到覆寫。

## 準備目錄

每個 Terraform 設定檔都必須有自己的目錄 (也稱為*根模組*)。

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
3. [開啟 Google Cloud 專案](https://console.cloud.google.com/?hl=zh-tw)即可查看結果。在 Google Cloud 控制台的使用者介面中，前往資源頁面，確認 Terraform 已建立或更新資源。

**注意：**Terraform 範例通常會假設 Google Cloud 專案已啟用必要的 API。

### 將存取權授予服務帳戶

選取下列選項之一：

### 控制台

1. 前往「IAM & Admin」(IAM 與管理) 頁面。

   [前往「IAM & Admin」(IAM 與管理) 頁面](https://console.cloud.google.com/project/_/iam-admin?hl=zh-tw)
2. 按一下 person\_add「Grant Access」(授予存取權)。

   「Add principals」(新增主體) 對話方塊隨即開啟。
3. 在「新增主體」欄位，輸入先前複製的服務帳戶 ID。
4. 按一下「Select a role」(請選擇角色) 欄位，然後在「Filter」(篩選器) 中輸入 `Cloud Speech Client`。
5. 按一下 [Add another role] (新增其他角色)。
6. 在「Select a role」(請選擇角色) 欄位中，依序選取「Cloud Storage」和「Storage Object Viewer」(Storage 物件檢視者)。
7. 按一下 [儲存]。

### gcloud

使用 [`gcloud projects add-iam-policy-binding`](https://docs.cloud.google.com/sdk/gcloud/reference/projects/add-iam-policy-binding?hl=zh-tw) 指令：

```
gcloud projects add-iam-policy-binding 'PROJECT_NUMBER' --member='serviceAccount:MEMBER' --role='roles/speech.client' --condition=None
gcloud projects add-iam-policy-binding 'PROJECT_NUMBER' --member='serviceAccount:MEMBER' --role='roles/storage.objectViewer' --condition=None
```

替換下列內容：

* `PROJECT_NUMBER`：您的專案編號。
* `MEMBER`：您先前複製的服務帳戶 ID。

如未授予權限，會導致 `Permission denied` 錯誤。

**注意：**如果建立辨識器的專案，與物件資料表使用的 Cloud Storage bucket 所在專案不同，請按照下列方式授予服務帳戶 Identity and Access Management (IAM) 角色：

* 在包含辨識器的專案中，將 Cloud Speech 用戶端角色授予服務帳戶。
* 在包含 Cloud Storage bucket 的專案中，將 Storage 物件檢視者角色授予服務帳戶。
* 在包含 Cloud Storage bucket 的專案中，將 Storage 物件檢視者角色授予 Speech-to-Text 服務代理 (`service-my_project_number@gcp-sa-speech.iam.gserviceaccount.com`)。

## 建立物件資料表

在 Cloud Storage 中，針對一組音訊檔案[建立物件資料表](https://docs.cloud.google.com/bigquery/docs/object-tables?hl=zh-tw)。物件資料表中的音訊檔案必須是[支援的類型](https://docs.cloud.google.com/speech-to-text/docs/encoding?hl=zh-tw#audio-encodings)。

物件資料表使用的 Cloud Storage bucket，應位於您要建立模型及呼叫 `ML.TRANSCRIBE` 函式的專案中。如要呼叫 `ML.TRANSCRIBE` 函式，且該函式所在的專案與物件資料表使用的 Cloud Storage bucket 所在專案不同，您必須[在 bucket 層級將 Storage 管理員角色授予](https://docs.cloud.google.com/storage/docs/access-control/using-iam-permissions?hl=zh-tw#bucket-add) `service-A@gcp-sa-aiplatform.iam.gserviceaccount.com` 服務帳戶。

## 建立模型

建立遠端模型，[`REMOTE_SERVICE_TYPE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model-service?hl=zh-tw#remote_service_type) 為 `CLOUD_AI_SPEECH_TO_TEXT_V2`：

```
CREATE OR REPLACE MODEL
`PROJECT_ID.DATASET_ID.MODEL_NAME`
REMOTE WITH CONNECTION {`PROJECT_ID.REGION.CONNECTION_ID`}
OPTIONS (
  REMOTE_SERVICE_TYPE = 'CLOUD_AI_SPEECH_TO_TEXT_V2',
  SPEECH_RECOGNIZER = 'projects/PROJECT_NUMBER/locations/LOCATION/recognizers/RECOGNIZER_ID'
);
```

替換下列內容：

* `PROJECT_ID`：您的專案 ID。
* `DATASET_ID`：要包含模型的資料集 ID。
* `MODEL_NAME`：模型名稱。
* `REGION`：連線使用的區域。
* `CONNECTION_ID`：連線 ID，例如 `myconnection`。

  在 Google Cloud 控制台[查看連線詳細資料](https://docs.cloud.google.com/bigquery/docs/working-with-connections?hl=zh-tw#view-connections)時，連線 ID 是「Connection ID」(連線 ID) 中顯示的完整連線 ID 最後一個部分的值，例如 `projects/myproject/locations/connection_location/connections/myconnection`。
* `PROJECT_NUMBER`：語音辨識器所在專案的專案編號。您可以在 Google Cloud 控制台「資訊主頁」頁面的「專案資訊」資訊卡中找到這個值。
* `LOCATION`：語音辨識器使用的位置。您可以在
  Google Cloud 控制台的「
  [**List recognizers**」(辨識器清單) 頁面](https://console.cloud.google.com/speech/recognizers/list?hl=zh-tw)，找到「**Location**」(位置) 欄位中的這個值。
* `RECOGNIZER_ID`：語音辨識器 ID。您可以在 Google Cloud 控制台的「[**List recognizers**」(列出辨識工具) 頁面的「**ID**」欄位中找到這個值。](https://console.cloud.google.com/speech/recognizers/list?hl=zh-tw)

  這個選項並非必要。如未指定值，系統會使用預設辨識器。在這種情況下，您必須為
  `ML.TRANSCRIBE` 函式的 `recognition_config` 參數
  指定值，才能為預設辨識器提供設定。

  您只能在提供的 `recognition_config` 值中使用 `chirp`
  [語音轉錄模型](https://docs.cloud.google.com/speech-to-text/v2/docs/transcription-model?hl=zh-tw#transcription_models)。

**重要事項：** 即使連線位於預設專案中，您也必須指定連線的專案 ID。

## 轉錄音訊檔案

使用 `ML.TRANSCRIBE` 函式轉錄音訊檔案：

```
SELECT *
FROM ML.TRANSCRIBE(
  MODEL `PROJECT_ID.DATASET_ID.MODEL_NAME`,
  TABLE `PROJECT_ID.DATASET_ID.OBJECT_TABLE_NAME`,
  RECOGNITION_CONFIG => ( JSON 'recognition_config')
);
```

替換下列內容：

* `PROJECT_ID`：您的專案 ID。
* `DATASET_ID`：模型所在資料集的 ID。
* `MODEL_NAME`：模型名稱。
* `OBJECT_TABLE_NAME`：物件資料表的名稱，其中包含要處理的音訊檔案 URI。
* `recognition_config`：JSON 格式的 [`RecognitionConfig` 資源](https://docs.cloud.google.com/speech-to-text/v2/docs/reference/rest/v2/projects.locations.recognizers?hl=zh-tw#recognitionconfig)。

  如果已使用 [`SPEECH_RECOGNIZER` 選項](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model-service?hl=zh-tw#speech_recognizer)為遠端模型指定辨識器，則無法指定 `recognition_config` 值。

  如果未使用 `SPEECH_RECOGNIZER` 選項為遠端模型指定辨識器，則必須指定 `recognition_config` 值。這個值用於提供預設辨識器的設定。

  您只能在提供的 `recognition_config` 值中使用 `chirp`
  [語音轉錄模型](https://docs.cloud.google.com/speech-to-text/v2/docs/transcription-model?hl=zh-tw#transcription_models)。

## 範例

**範例 1**

下列範例會轉錄 `audio` 資料表代表的音訊檔案，但不會覆寫辨識器的預設設定：

```
SELECT *
FROM ML.TRANSCRIBE(
  MODEL `myproject.mydataset.transcribe_model`,
  TABLE `myproject.mydataset.audio`
);
```

下列範例會轉錄 `audio` 資料表代表的音訊檔案，並提供預設辨識器的設定：

```
SELECT *
FROM ML.TRANSCRIBE(
  MODEL `myproject.mydataset.transcribe_model`,
  TABLE `myproject.mydataset.audio`,
  recognition_config => ( JSON '{"language_codes": ["en-US" ],"model": "chirp","auto_decoding_config": {}}')
);
```

## 清除所用資源

如要避免系統向您的 Google Cloud 帳戶收取本教學課程所用資源的費用，請刪除含有相關資源的專案，或者保留專案但刪除個別資源。

### 刪除專案

### 控制台

**注意**：刪除專案會造成以下影響：

* **專案中的所有內容都會遭到刪除。**如果使用現有專案來進行本文中的任務，刪除專案將一併移除當中已完成的其他任務'。
* **自訂專案 ID 會消失。**當您之前建立這個專案時，可能建立了想要在日後使用的自訂專案 ID。如要保留使用該專案 ID 的網址 (例如 `appspot.com` 網址)，請刪除在該專案中選取的資源，而不是刪除整個專案。

如果打算探索多種架構、教學課程或快速入門導覽課程，重複使用專案可避免超出專案配額限制。

1. 前往 Google Cloud 控制台的「Manage resources」(管理資源) 頁面。

   [前往「Manage resources」(管理資源)](https://console.cloud.google.com/iam-admin/projects?hl=zh-tw)
2. 在專案清單中選取要刪除的專案，然後點選「Delete」(刪除)。
3. 在對話方塊中輸入專案 ID，然後按一下 [Shut down] (關閉) 以刪除專案。

### gcloud

**注意**：刪除專案會造成以下影響：

* **專案中的所有內容都會遭到刪除。**如果使用現有專案來進行本文中的任務，刪除專案將一併移除當中已完成的其他任務'。
* **自訂專案 ID 會消失。**當您之前建立這個專案時，可能建立了想要在日後使用的自訂專案 ID。如要保留使用該專案 ID 的網址 (例如 `appspot.com` 網址)，請刪除在該專案中選取的資源，而不是刪除整個專案。

如果打算探索多種架構、教學課程或快速入門導覽課程，重複使用專案可避免超出專案配額限制。

刪除 Google Cloud 專案：

```
gcloud projects delete PROJECT_ID
```

### 刪除個別資源

如果您打算保留本教學課程使用的專案，可以刪除建立的個別資源，以免產生更多費用：

1. **刪除資料集：**刪除資料集也會一併移除遠端模型，以及在資料集中建立的物件資料表。

   * 前往 Google Cloud 控制台的「BigQuery」頁面。
   * 在「Explorer」窗格中展開專案，然後選取您建立的資料集。
   * 按一下 more\_vert「View actions」(查看動作)，然後按一下「Delete」(刪除)。
   * 在對話方塊中輸入 `delete`，然後按一下「Delete」(刪除)。
2. **刪除連結：**

   * 在「Explorer」窗格中展開專案名稱，然後點選「連線」。
   * 按一下所建連結旁的 more\_vert「查看動作」圖示，然後選取「刪除」。
   * 在對話方塊中，按一下「Delete」(刪除) 進行確認。
3. **刪除 Speech-to-Text 辨識器 (如有建立)：**

   * 前往 [Speech-to-Text 辨識器頁面](https://console.cloud.google.com/speech/recognizers/list?hl=zh-tw)。
   * 勾選您建立的辨識器旁的方塊，然後按一下「刪除」。

## 後續步驟

* 如要進一步瞭解 BigQuery ML 中的模型推論，請參閱「[模型推論總覽](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/inference-overview?hl=zh-tw)」。
* 如要進一步瞭解如何使用 Cloud AI API 執行 AI 任務，請參閱「[AI 應用程式總覽](https://docs.cloud.google.com/bigquery/docs/ai-application-overview?hl=zh-tw)」。
* 如要進一步瞭解生成式 AI 模型支援的 SQL 陳述式和函式，請參閱「[生成式 AI 模型的端對端使用者歷程](https://docs.cloud.google.com/bigquery/docs/e2e-journey-genai?hl=zh-tw)」。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-10-24 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-10-24 (世界標準時間)。"],[],[]]