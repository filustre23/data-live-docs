Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 使用 AI.GENERATE\_TEXT 函式生成文字

本文說明如何建立代表 Gemini Enterprise Agent Platform 模型的 BigQuery ML [遠端模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model?hl=zh-tw)，然後搭配 [`AI.GENERATE_TEXT` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-ai-generate-text?hl=zh-tw)使用該遠端模型生成文字。

支援下列類型的遠端模型：

* [遠端模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model?hl=zh-tw)。
* [遠端模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model?hl=zh-tw)，而非 [Anthropic Claude 模型](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/partner-models/use-claude?hl=zh-tw)。
* [Llama 模型](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/partner-models/llama?hl=zh-tw)的[遠端模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model?hl=zh-tw)
* [Mistral AI 模型](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/partner-models/mistral?hl=zh-tw)的[遠端模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model?hl=zh-tw)
* [支援的開放式模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model-open?hl=zh-tw#supported_open_models)上的[遠端模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model-open?hl=zh-tw)。

視您選擇的 Agent Platform 模型而定，您可以根據[物件資料表](https://docs.cloud.google.com/bigquery/docs/object-table-introduction?hl=zh-tw)中的非結構化資料輸入內容，或[標準資料表](https://docs.cloud.google.com/bigquery/docs/tables-intro?hl=zh-tw#standard-tables)中的文字輸入內容生成文字。

## 必要的角色

如要建立遠端模型並生成文字，您需要下列 Identity and Access Management (IAM) 角色：

* 建立及使用 BigQuery 資料集、資料表和模型：專案的 BigQuery 資料編輯者 (`roles/bigquery.dataEditor`)。
* 建立、委派及使用 BigQuery 連線：專案的 BigQuery 連線管理員 (`roles/bigquery.connectionsAdmin`)。

  如果您未設定[預設連線](https://docs.cloud.google.com/bigquery/docs/default-connections?hl=zh-tw)，可以在執行 `CREATE MODEL` 陳述式時建立並設定。如要執行這項操作，您必須具備專案的 BigQuery 管理員 (`roles/bigquery.admin`) 角色。詳情請參閱「[設定預設連線](https://docs.cloud.google.com/bigquery/docs/default-connections?hl=zh-tw#configure_the_default_connection)」。
* 將權限授予連線的服務帳戶：在含有 Gemini Enterprise Agent Platform 端點的專案中，具備專案 IAM 管理員 (`roles/resourcemanager.projectIamAdmin`) 角色。這是您將模型名稱指定為端點，所建立遠端模型的目前專案。如果您指定網址做為端點，並建立遠端模型，這個專案就是網址中指定的專案。

  如果您使用遠端模型分析物件資料表中的非結構化資料，且物件資料表使用的 Cloud Storage bucket 與 Agent Platform 端點位於不同專案，則您也必須具備物件資料表所用 Cloud Storage bucket 的 Storage 管理員 (`roles/storage.admin`) 角色。
* 建立 BigQuery 工作：專案的 BigQuery 工作使用者 (`roles/bigquery.jobUser`)。

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

您或許還可透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)取得這些權限。

## 事前準備

1. 在 Google Cloud 控制台的專案選取器頁面中，選取或建立 Google Cloud 專案。

   **選取或建立專案所需的角色**

   * **選取專案**：選取專案時不需要特定 IAM 角色，只要您獲派某個專案的角色，即可選取該專案。
   * **建立專案**：如要建立專案，您必須具備專案建立者角色 (`roles/resourcemanager.projectCreator`)，其中包含 `resourcemanager.projects.create` 權限。[瞭解如何授予角色](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)。
   **注意**：如果您不打算保留在這項程序中建立的資源，請建立新專案，不要選取現有專案。如果採用這種做法，當您完成這些步驟後，就可以直接刪除該專案，並移除相關聯的所有資源。

   [前往專案選取器](https://console.cloud.google.com/projectselector2/home/dashboard?hl=zh-tw)
2. [確認 Google Cloud 專案已啟用計費功能](https://docs.cloud.google.com/billing/docs/how-to/verify-billing-enabled?hl=zh-tw#confirm_billing_is_enabled_on_a_project)。
3. 啟用 BigQuery、BigQuery Connection 和 Agent Platform API (如有尚未啟用的 API)。

   **啟用 API 所需的角色**

   您必須具備 `serviceusage.services.enable` 權限，才能啟用 API。如果您建立了專案，可能已透過「擁有者」角色 (`roles/owner`) 取得這項權限。否則，您可以透過「Service Usage 管理員」角色 (`roles/serviceusage.serviceUsageAdmin`) 取得這項權限。[瞭解如何授予角色](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)。

   [啟用 API](https://console.cloud.google.com/apis/enableflow?apiid=bigquery.googleapis.com%2Cbigqueryconnection.googleapis.com%2Caiplatform.googleapis.com&hl=zh-tw)

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

建立遠端模型要使用的 [Cloud 資源連結](https://docs.cloud.google.com/bigquery/docs/create-cloud-resource-connection?hl=zh-tw)，並取得連結的服務帳戶。建立連線時，請選擇與上一步建立的資料集相同的[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)。

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

### 將角色授予遠端模型連線的服務帳戶

您必須將 Agent Platform 使用者角色授予遠端模型所用連線的服務帳戶。

如果您打算將遠端模型的端點指定為網址 (例如 `endpoint = 'https://us-central1-aiplatform.googleapis.com/v1/projects/myproject/locations/us-central1/publishers/google/models/gemini-2.0-flash'`)，請在網址指定的專案中授予這個角色。

如果您打算使用模型名稱 (例如 `endpoint = 'gemini-2.0-flash'`) 指定遠端模型的端點，請在要建立遠端模型的專案中授予這個角色。

在其他專案中授予角色會導致錯誤 `bqcx-1234567890-wxyz@gcp-sa-bigquery-condel.iam.gserviceaccount.com does not have the permission to access resource`。

如要授予 Agent Platform 使用者角色，請按照下列步驟操作：

### 控制台

1. 前往「IAM & Admin」(IAM 與管理) 頁面。

   [前往「IAM & Admin」(IAM 與管理) 頁面](https://console.cloud.google.com/project/_/iam-admin?hl=zh-tw)
2. 按一下「person\_add 新增」。

   「Add principals」(新增主體) 對話方塊隨即開啟。
3. 在「新增主體」欄位，輸入先前複製的服務帳戶 ID。
4. 在「選取角色」欄位中，搜尋「Agent Platform 使用者」。
5. 按一下 [儲存]。

### gcloud

使用 [`gcloud projects add-iam-policy-binding`](https://docs.cloud.google.com/sdk/gcloud/reference/projects/add-iam-policy-binding?hl=zh-tw) 指令。

```
gcloud projects add-iam-policy-binding 'PROJECT_NUMBER' --member='serviceAccount:MEMBER' --role='roles/aiplatform.user' --condition=None
```

替換下列內容：

* `PROJECT_NUMBER`：您的專案編號
* `MEMBER`：您先前複製的服務帳戶 ID

## 將角色授予物件資料表連線的服務帳戶

如要使用遠端模型，根據物件資料表資料生成文字，請在要建立遠端模型的專案中，將 Agent Platform 使用者角色授予物件資料表連線的服務帳戶。您也可以略過這個步驟。

如要找出物件資料表連線的服務帳戶，請按照下列步驟操作：

1. 前往「BigQuery」頁面

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。

   如果沒有看到左側窗格，請按一下 last\_page「Expand left pane」(展開左側窗格)，開啟窗格。
3. 在「Explorer」窗格中，按一下「Datasets」(資料集)，然後選取含有物件資料表的資料集。
4. 依序點選**「總覽」>「資料表」**，然後選取物件資料表。
5. 在編輯器窗格中，按一下「Details」(詳細資料) 分頁標籤。
6. 記下「連線 ID」欄位中的連線名稱。
7. 在「Explorer」窗格中，點選「連線」。
8. 選取與物件資料表「Connection ID」(連線 ID) 欄位相符的連線。
9. 複製「Service account ID」(服務帳戶 ID) 欄位中的值。

如要授予角色，請按照下列步驟操作：

### 控制台

1. 前往「IAM & Admin」(IAM 與管理) 頁面。

   [前往「IAM & Admin」(IAM 與管理) 頁面](https://console.cloud.google.com/project/_/iam-admin?hl=zh-tw)
2. 按一下「person\_add 新增」。

   「Add principals」(新增主體) 對話方塊隨即開啟。
3. 在「新增主體」欄位，輸入先前複製的服務帳戶 ID。
4. 在「選取角色」欄位中，搜尋「Agent Platform 使用者」。
5. 按一下 [儲存]。

### gcloud

使用 [`gcloud projects add-iam-policy-binding`](https://docs.cloud.google.com/sdk/gcloud/reference/projects/add-iam-policy-binding?hl=zh-tw) 指令。

```
gcloud projects add-iam-policy-binding 'PROJECT_NUMBER' --member='serviceAccount:MEMBER' --role='roles/aiplatform.user' --condition=None
```

替換下列內容：

* `PROJECT_NUMBER`：您的專案編號
* `MEMBER`：您先前複製的服務帳戶 ID

## 啟用合作夥伴模型

只有在要使用 Anthropic Claude、Llama 或 Mistral AI 模型時，才需要執行這個步驟。

1. 前往 Google Cloud 控制台的 Agent Platform「Model Garden」頁面。

   [前往 Model Garden](https://console.cloud.google.com/vertex-ai/model-garden?hl=zh-tw)
2. 搜尋或瀏覽要使用的合作夥伴模型。
3. 按一下模型資訊卡。
4. 在模型頁面中，按一下「啟用」。
5. 填寫必要的啟用資訊，然後點選「下一步」。
6. 在「條款及細則」部分，勾選核取方塊。
7. 按一下「同意」，接受條款及細則並啟用模型。

## 選擇開放原始碼模型部署方法

如果您是透過[支援的開放模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model-open?hl=zh-tw#supported_open_models)建立遠端模型，可以在 `CREATE MODEL` 陳述式中指定 Agent Platform Model Garden 或 Hugging Face 模型 ID，在建立遠端模型的同時自動部署開放模型。或者，您也可以先手動部署開放原始碼模型，然後在 `CREATE MODEL` 陳述式中指定模型端點，將該開放原始碼模型與遠端模型搭配使用。詳情請參閱「[部署開放原始碼模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model-open?hl=zh-tw#deploy_open_models)」。

## 建立 BigQuery ML 遠端模型

建立遠端模型：

### Agent Platform 模型

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 使用 SQL 編輯器建立[遠端模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model?hl=zh-tw)：

   ```
   CREATE OR REPLACE MODEL
   `PROJECT_ID.DATASET_ID.MODEL_NAME`
   REMOTE WITH CONNECTION {DEFAULT | `PROJECT_ID.REGION.CONNECTION_ID`}
   OPTIONS (ENDPOINT = 'ENDPOINT');
   ```

   替換下列內容：

   * `PROJECT_ID`：您的專案 ID。
   * `DATASET_ID`：要包含模型的資料集 ID。這個資料集必須與您使用的連線位於相同[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)。
   * `MODEL_NAME`：模型名稱。
   * `REGION`：連線使用的區域。
   * `CONNECTION_ID`：BigQuery 連線的 ID。

     如要取得這個值，請在 Google Cloud 控制台中[查看連線詳細資料](https://docs.cloud.google.com/bigquery/docs/working-with-connections?hl=zh-tw#view-connections)，然後複製「Connection ID」中顯示的完整連線 ID 最後一個部分的值。例如：`projects/myproject/locations/connection_location/connections/myconnection`。
   * `ENDPOINT`：要使用的 Agent Platform 模型端點。

     如果是預先訓練的 Agent Platform 模型、Claude 模型和 Mistral AI 模型，請指定模型名稱。對於其中部分模型，您可以在名稱中指定模型的特定[版本](https://docs.cloud.google.com/vertex-ai/docs/generative-ai/learn/model-versioning?hl=zh-tw)。如果是支援的 Gemini 模型，您可以指定[全域端點](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model?hl=zh-tw#global-endpoint)，提高可用性。

     如果是 Llama 模型，請以 `openapi/<publisher_name>/<model_name>` 格式指定 [OpenAI API](https://platform.openai.com/docs/api-reference/introduction) 端點。例如：`openapi/meta/llama-3.1-405b-instruct-maas`。

     如要瞭解支援的模型名稱和版本，請參閱「[`ENDPOINT`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model?hl=zh-tw#endpoint)」。

     您指定的 Agent Platform 模型必須位於您建立遠端模型的地區。詳情請參閱「[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw#locations-for-remote-models)」。

### 全新開放原始碼模型

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 使用 SQL 編輯器建立[遠端模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model-open?hl=zh-tw)：

   ```
   CREATE OR REPLACE MODEL
   `PROJECT_ID.DATASET_ID.MODEL_NAME`
   REMOTE WITH CONNECTION {DEFAULT | `PROJECT_ID.REGION.CONNECTION_ID`}
   OPTIONS (
     {HUGGING_FACE_MODEL_ID = 'HUGGING_FACE_MODEL_ID' |
        MODEL_GARDEN_MODEL_NAME = 'MODEL_GARDEN_MODEL_NAME'}
     [, HUGGING_FACE_TOKEN = 'HUGGING_FACE_TOKEN' ]
     [, MACHINE_TYPE = 'MACHINE_TYPE' ]
     [, MIN_REPLICA_COUNT = MIN_REPLICA_COUNT ]
     [, MAX_REPLICA_COUNT = MAX_REPLICA_COUNT ]
     [, RESERVATION_AFFINITY_TYPE = {'NO_RESERVATION' | 'ANY_RESERVATION' | 'SPECIFIC_RESERVATION'} ]
     [, RESERVATION_AFFINITY_KEY = 'compute.googleapis.com/reservation-name' ]
     [, RESERVATION_AFFINITY_VALUES = RESERVATION_AFFINITY_VALUES ]
     [, ENDPOINT_IDLE_TTL = ENDPOINT_IDLE_TTL ]
   );
   ```

   替換下列內容：

   * `PROJECT_ID`：您的專案 ID。
   * `DATASET_ID`：要包含模型的資料集 ID。這個資料集必須與您使用的連線位於相同[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)。
   * `MODEL_NAME`：模型名稱。
   * `REGION`：連線使用的區域。
   * `CONNECTION_ID`：BigQuery 連線的 ID。

     如要取得這個值，請在 Google Cloud 控制台中[查看連線詳細資料](https://docs.cloud.google.com/bigquery/docs/working-with-connections?hl=zh-tw#view-connections)，然後複製「Connection ID」中顯示的完整連線 ID 最後一個部分的值。例如：`projects/myproject/locations/connection_location/connections/myconnection`。
   * `HUGGING_FACE_MODEL_ID`：`STRING` 值，指定[支援的 Hugging Face 模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model-open?hl=zh-tw#hugging-face-models) ID，格式為 `provider_name`/`model_name`。例如 `deepseek-ai/DeepSeek-R1`。如要取得模型 ID，請在 Hugging Face Model Hub 中點選模型名稱，然後從模型資訊卡頂端複製模型 ID。
   * `MODEL_GARDEN_MODEL_NAME`：`STRING` 值，指定[支援的 Gemini Enterprise Agent Platform Model Garden 模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model-open?hl=zh-tw#model-garden-models) ID 和版本，格式為 `publishers/publisher`/models/`model_name`@`model_version`。例如：`publishers/openai/models/gpt-oss@gpt-oss-120b`。如要取得模型 ID，請在 Agent Platform Model Garden 中點選模型資訊卡，然後複製「Model ID」(模型 ID) 欄位中的模型 ID。如要取得預設模型版本，請從模型資訊卡的「Version」(版本) 欄位複製。如要查看其他可用的模型版本，請按一下「Deploy model」(部署模型)，然後點選「Resource ID」(資源 ID) 欄位。
   * `HUGGING_FACE_TOKEN`：`STRING` 值，指定要使用的 Hugging Face [使用者存取權杖](https://huggingface.co/docs/hub/en/security-tokens)。只有在指定 `HUGGING_FACE_MODEL_ID` 選項的值時，才能指定這個選項的值。

     權杖至少須具備 `read` 角色，但範圍較廣的權杖也適用。如果 `HUGGING_FACE_MODEL_ID` 值識別的模型是 Hugging Face [封閉式](https://huggingface.co/docs/hub/en/models-gated)或私人模型，則必須使用這個選項。

     部分受限模型需要明確同意服務條款，才能授予存取權。如要同意這些條款，請按照下列步驟操作：

     1. 前往 Hugging Face 網站的模型頁面。
     2. 找出並詳閱模型的服務條款。服務合約的連結通常位於模型資訊卡。
     3. 按照頁面提示接受條款。
   * `MACHINE_TYPE`：`STRING` 值，指定將模型部署至 Agent Platform 時要使用的機器類型。如要瞭解支援的機型，請參閱「[機型](https://docs.cloud.google.com/vertex-ai/docs/predictions/configure-compute?hl=zh-tw#machine-types)」。如未指定 `MACHINE_TYPE` 選項的值，系統會使用模型的 Agent Platform Model Garden 預設機器類型。
   * `MIN_REPLICA_COUNT`：`INT64` 值，指定將模型部署至 Agent Platform 端點時，使用的機器副本數量下限。服務會根據端點的推論負載，視需要增加或減少副本數量。使用的副本數量一律不會低於 `MIN_REPLICA_COUNT` 值，也不會高於 `MAX_REPLICA_COUNT` 值。`MIN_REPLICA_COUNT` 值必須介於 `[1, 4096]` 之間。預設值為 `1`。
   * `MAX_REPLICA_COUNT`：`INT64` 值，指定將模型部署至 Agent Platform 端點時，使用的機器副本數量上限。服務會根據端點的推論負載，視需要增加或減少副本數量。使用的副本數量一律不會低於 `MIN_REPLICA_COUNT` 值，也不會高於 `MAX_REPLICA_COUNT` 值。`MAX_REPLICA_COUNT` 值必須介於 `[1, 4096]` 之間。預設值為 `MIN_REPLICA_COUNT` 值。
   * `RESERVATION_AFFINITY_TYPE`：決定部署的模型是否使用 [Compute Engine 預留項目](https://docs.cloud.google.com/compute/docs/instances/reservations-overview?hl=zh-tw)，在提供預測時確保虛擬機器 (VM) 可用性，並指定模型是否使用所有可用預留項目或僅使用一個特定預留項目的 VM。詳情請參閱「[Compute Engine 預留項目相似度](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model-open?hl=zh-tw#reservation-affinity)」。

     您只能使用與 Agent Platform 共用的 Compute Engine 預留項目。詳情請參閱「[允許使用預留項目](https://docs.cloud.google.com/vertex-ai/docs/predictions/use-reservations?hl=zh-tw#allow-consumption)」。

     支援的值如下：

     + `NO_RESERVATION`：將模型部署至 Agent Platform 端點時，不會耗用預留項目。指定 `NO_RESERVATION` 的效果與不指定預留項目相似度相同。
     + `ANY_RESERVATION`：代理平台模型部署作業會使用 Compute Engine 預留項目的虛擬機器 (VM)，這些預留項目位於目前專案或[與專案共用](https://docs.cloud.google.com/compute/docs/instances/reservations-overview?hl=zh-tw#how-shared-reservations-work)，且[設為自動使用](https://docs.cloud.google.com/compute/docs/instances/reservations-consume?hl=zh-tw#consuming_instances_from_any_matching_reservation)。只有符合下列條件的 VM 才會用於這項作業：
       - 這些節點會使用 `MACHINE_TYPE` 值指定的機型。
       - 如果建立遠端模型的 BigQuery 資料集位於單一區域，則預留項目必須位於相同區域。如果資料集位於 `US` 多區域，則預留項目必須位於 `us-central1` 區域。如果資料集位於 `EU` 多區域，則預留項目必須位於 `europe-west4` 區域。

       如果可用預留項目的容量不足，或找不到合適的預留項目，系統會佈建隨需 Compute Engine VM，以滿足資源需求。
     + `SPECIFIC_RESERVATION`：Agent Platform 模型部署作業只會使用您在 `RESERVATION_AFFINITY_VALUES` 值中指定的預留項目 VM。這項預留項目必須[設為明確指定的消耗模式](https://docs.cloud.google.com/compute/docs/instances/reservations-consume?hl=zh-tw#consuming_instances_from_a_specific_reservation)。如果指定的預留項目容量不足，部署作業就會失敗。
   * `RESERVATION_AFFINITY_KEY`：字串 `compute.googleapis.com/reservation-name`。如果 `RESERVATION_AFFINITY_TYPE` 值為 `SPECIFIC_RESERVATION`，則必須指定這個選項。
   * `RESERVATION_AFFINITY_VALUES`：`ARRAY<STRING>` 值，指定 Compute Engine 預留項目的完整資源名稱，格式如下：  
       
     `projects/myproject/zones/reservation_zone/reservations/reservation_name`

     例如：`RESERVATION_AFFINITY_values = ['projects/myProject/zones/us-central1-a/reservations/myReservationName']`。

     您可以前往 Google Cloud 控制台的「Reservations」(預留項目) 頁面，取得預留項目名稱和可用區。詳情請參閱「[查看預留項目](https://docs.cloud.google.com/compute/docs/instances/reservations-view?hl=zh-tw#view-reservations)」。

     當 `RESERVATION_AFFINITY_TYPE` 值為 `SPECIFIC_RESERVATION` 時，您必須指定這個選項。
   * `ENDPOINT_IDLE_TTL`：`INTERVAL` 值，指定閒置多久後，系統會自動從 Agent Platform 端點取消部署開放原始碼模型。

     如要啟用自動取消部署功能，請指定介於 390 分鐘 (6.5 小時) 至 7 天之間的[間隔常值](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/lexical?hl=zh-tw#interval_literals)值。舉例來說，指定 `INTERVAL 8 HOUR` 即可在模型閒置 8 小時後取消部署。預設值為 390 分鐘 (6.5 小時)。

     模型閒置時間是指對模型執行下列任一作業後經過的時間：

     + 執行 [`CREATE MODEL` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model-open?hl=zh-tw)。
     + 執行 [`ALTER MODEL` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-alter-model?hl=zh-tw)，並將 `DEPLOY_MODEL` 引數設為 `TRUE`。
     + 向模型端點傳送推論要求。例如，執行 [`AI.GENERATE_EMBEDDING`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-ai-generate-embedding?hl=zh-tw) 或 [`AI.GENERATE_TEXT`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-ai-generate-text?hl=zh-tw) 函式。

     每項操作都會將閒置計時器重設為零。重設作業會在執行作業的 BigQuery 工作開始時觸發。

     模型取消部署後，傳送至模型的推論要求會傳回錯誤。BigQuery 模型物件 (包括模型中繼資料) 則維持不變。如要再次使用模型進行推論，您必須對模型執行 `ALTER MODEL` 陳述式，並將 `DEPLOY_MODEL` 選項設為 `TRUE`，藉此重新部署模型。

### 已部署的開放式模型

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 使用 SQL 編輯器建立[遠端模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model-open?hl=zh-tw)：

   ```
   CREATE OR REPLACE MODEL
   `PROJECT_ID.DATASET_ID.MODEL_NAME`
   REMOTE WITH CONNECTION {DEFAULT | `PROJECT_ID.REGION.CONNECTION_ID`}
   OPTIONS (
     ENDPOINT = 'https://ENDPOINT_REGION-aiplatform.googleapis.com/v1/projects/ENDPOINT_PROJECT_ID/locations/ENDPOINT_REGION/endpoints/ENDPOINT_ID'
   );
   ```

   替換下列內容：

   * `PROJECT_ID`：您的專案 ID。
   * `DATASET_ID`：要包含模型的資料集 ID。這個資料集必須與您使用的連線位於相同[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)。
   * `MODEL_NAME`：模型名稱。
   * `REGION`：連線使用的區域。
   * `CONNECTION_ID`：BigQuery 連線的 ID。

     如要取得這個值，請在 Google Cloud 控制台中[查看連線詳細資料](https://docs.cloud.google.com/bigquery/docs/working-with-connections?hl=zh-tw#view-connections)，然後複製「Connection ID」中顯示的完整連線 ID 最後一個部分的值。例如：`projects/myproject/locations/connection_location/connections/myconnection`。
   * `ENDPOINT_REGION`：部署開放原始碼模型的區域。
   * `ENDPOINT_PROJECT_ID`：部署開放式模型的專案。
   * `ENDPOINT_ID`：開放原始碼模型使用的 HTTPS 端點 ID。如要取得端點 ID，請在「[線上預測](https://console.cloud.google.com/vertex-ai/online-prediction/endpoints?hl=zh-tw)」頁面找到開啟的模型，然後複製「ID」欄位中的值。

## 根據標準表格資料生成文字

使用 [`AI.GENERATE_TEXT` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-ai-generate-text?hl=zh-tw)，搭配標準資料表中的提示資料生成文字：

### Gemini

```
SELECT *
FROM AI.GENERATE_TEXT(
  MODEL `PROJECT_ID.DATASET_ID.MODEL_NAME`,
  {TABLE PROJECT_ID.DATASET_ID.TABLE_NAME | (PROMPT_QUERY)},
  STRUCT(
  {
    {
      [MAX_OUTPUT_TOKENS AS max_output_tokens]
      [, TOP_P AS top_p]
      [, TEMPERATURE AS temperature]
      [, STOP_SEQUENCES AS stop_sequences]
      [, GROUND_WITH_GOOGLE_SEARCH AS ground_with_google_search]
      [, SAFETY_SETTINGS AS safety_settings]
    }
    |
    [, MODEL_PARAMS AS model_params]
  }
  [, REQUEST_TYPE AS request_type])
);
```

替換下列內容：

* `PROJECT_ID`：您的專案 ID。
* `DATASET_ID`：模型所在資料集的 ID。
* `MODEL_NAME`：模型名稱。
* `TABLE_NAME`：包含提示詞的資料表名稱。這個資料表必須有名為 `prompt` 的資料欄，或者您可以使用別名，改用其他名稱的資料欄。
* `PROMPT_QUERY`：提供提示資料的查詢。這項查詢必須產生名為 `prompt` 的資料欄。

  **注意：**

  建議不要在提示查詢中使用 [`LIMIT and OFFSET` 子句](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw#limit_and_offset_clause)。使用這個子句會導致查詢先處理所有輸入資料，然後套用 `LIMIT` 和 `OFFSET`。
* `TOKENS`：`INT64` 值，用於設定回覆中可生成的詞元數量上限。這個值必須介於 `[1,8192]` 之間。
  如要取得較短的回覆，請指定較低的值；如要取得較長的回覆，請調高此值。預設值為 `128`。
* `TEMPERATURE`：`FLOAT64` 值，範圍為 `[0.0,1.0]`，可控制選取詞元的隨機程度。預設值為 `0`。

  如果想藉由提示生成更具確定性、較不具開放性和創意性的回覆，建議調低 `temperature`。另一方面，如果 `temperature` 較高，則可能產生較多元或有創意的結果。如果 `temperature` 的值為 `0`，則具有確定性，即模型一律會選取可能性最高的回覆。
* `TOP_P`：`[0.0,1.0]` 範圍內的 `FLOAT64` 值，有助於判斷所選詞元的機率。如要取得較不隨機的回覆，請指定較低的值；如要取得較隨機的回覆，請調高此值。預設為 `0.95`。
* `STOP_SEQUENCES`：`ARRAY<STRING>` 值，如果模型的回覆中包含指定字串，則會移除這些字串。字串必須完全相符，包括大小寫。預設為空陣列。
* `GROUND_WITH_GOOGLE_SEARCH`：`BOOL` 值，決定 Gemini Enterprise Agent Platform 模型在生成回覆時，是否要以 Google 搜尋強化事實基礎。建立基準後，模型就能在生成回覆時，使用網際網路上的額外資訊，讓回覆更具體且符合事實。如果這個欄位設為 `True`，結果中會額外包含 `grounding_result` 欄，提供模型用來收集額外資訊的來源。預設值為 `FALSE`。
* `SAFETY_SETTINGS`：`ARRAY<STRUCT<STRING AS category, STRING AS threshold>>` 值，用於設定內容安全門檻，篩選回覆。struct 中的第一個元素指定危害類別，第二個元素則指定對應的封鎖門檻。模型會篩除違反這些設定的內容。每個類別只能指定一次。舉例來說，您無法同時指定 `STRUCT('HARM_CATEGORY_DANGEROUS_CONTENT' AS category, 'BLOCK_MEDIUM_AND_ABOVE' AS threshold)` 和 `STRUCT('HARM_CATEGORY_DANGEROUS_CONTENT' AS category, 'BLOCK_ONLY_HIGH' AS threshold)`。如果特定類別沒有安全設定，系統會使用 `BLOCK_MEDIUM_AND_ABOVE` 安全設定。
  支援的類別如下：
  + `HARM_CATEGORY_HATE_SPEECH`
  + `HARM_CATEGORY_DANGEROUS_CONTENT`
  + `HARM_CATEGORY_HARASSMENT`
  + `HARM_CATEGORY_SEXUALLY_EXPLICIT`支援的門檻如下：
  + `BLOCK_NONE` ([受限](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/multimodal/configure-safety-attributes?hl=zh-tw#how_to_remove_automated_response_blocking_for_select_safety_attributes))
  + `BLOCK_LOW_AND_ABOVE`
  + `BLOCK_MEDIUM_AND_ABOVE` (預設)
  + `BLOCK_ONLY_HIGH`
  + `HARM_BLOCK_THRESHOLD_UNSPECIFIED`詳情請參閱[安全類別](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/multimodal/configure-safety-attributes?hl=zh-tw#safety_attribute_scoring)和[封鎖門檻](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/multimodal/configure-safety-attributes?hl=zh-tw#safety-settings)的定義。
* `REQUEST_TYPE`：`STRING` 值，指定要傳送至 Gemini 模型的推論要求類型。要求類型會決定要求使用的配額。有效值如下：
  + `DEDICATED`：`AI.GENERATE_TEXT` 函式只會使用佈建輸送量配額。如果沒有可用的佈建輸送量配額，`AI.GENERATE_TEXT` 函式會傳回 `Provisioned throughput is not purchased or is not
    active` 錯誤。
  + `SHARED`：即使您已購買佈建輸送量配額，`AI.GENERATE_TEXT` 函式也只會使用[動態共用配額 (DSQ)](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/dynamic-shared-quota?hl=zh-tw)。
  + `UNSPECIFIED`：`AI.GENERATE_TEXT` 函式會使用下列配額：
    - 如未購買佈建輸送量配額，`AI.GENERATE_TEXT` 函式會使用 DSQ 配額。
    - 如果您已購買佈建輸送量配額，`AI.GENERATE_TEXT` 函式會先使用佈建輸送量配額。如果要求超出佈建輸送量配額，溢出的流量會使用 DSQ 配額。

  預設值為 `UNSPECIFIED`。

  詳情請參閱「[使用 Agent Platform 佈建輸送量](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-generate-text?hl=zh-tw#provisioned-throughput)」。
* `MODEL_PARAMS`：JSON 格式的字串常值，可為模型提供參數。這個值必須符合 [`generateContent` 要求主體](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/reference/rest/v1/projects.locations.endpoints/generateContent?hl=zh-tw)格式。您可以為要求主體中的任何欄位提供值，但 `contents[]` 欄位除外。如果設定這個欄位，就無法在 `AI.GENERATE_TEXT` 函式的頂層結構體引數中指定任何模型參數。您必須在 `MODEL_PARAMS` 欄位中指定每個模型參數，或省略這個欄位並分別指定每個參數。

**範例 1**

以下範例顯示具有這些特性的要求：

* 提示詞，用於摘要 `articles` 資料表 `body` 欄中的文字。

```
SELECT *
FROM
  AI.GENERATE_TEXT(
    MODEL `mydataset.text_model`,
    (
      SELECT CONCAT('Summarize this text', body) AS prompt
      FROM mydataset.articles
    ));
```

**示例 2**

以下範例顯示具有這些特性的要求：

* 使用查詢，串連提供提示[前置字元](https://docs.cloud.google.com/vertex-ai/docs/generative-ai/text/text-prompts?hl=zh-tw#prompt_structure)的字串與資料表資料欄，建立提示資料。
* 傳回簡短回覆。

```
SELECT *
FROM
  AI.GENERATE_TEXT(
    MODEL `mydataset.text_model`,
    (
      SELECT CONCAT(question, 'Text:', description, 'Category') AS prompt
      FROM mydataset.input_table
    ),
    STRUCT(
      100 AS max_output_tokens));
```

**範例 3**

以下範例顯示具有這些特性的要求：

* 使用 `prompts` 資料表的 `prompt` 欄做為提示。

```
SELECT *
FROM
  AI.GENERATE_TEXT(
    MODEL `mydataset.text_model`,
    TABLE mydataset.prompts);
```

**範例 4**

以下範例顯示具有這些特性的要求：

* 使用 `prompts` 資料表的 `prompt` 欄做為提示。
* 傳回簡短回覆。
* 擷取並傳回公開網路資料，用於建立回覆基準。
* 使用兩項安全設定篩除不安全的回覆。

```
SELECT *
FROM
  AI.GENERATE_TEXT(
    MODEL `mydataset.text_model`,
    TABLE mydataset.prompts,
    STRUCT(
      100 AS max_output_tokens, 0.5 AS top_p,
      TRUE AS ground_with_google_search,
      [STRUCT('HARM_CATEGORY_HATE_SPEECH' AS category,
        'BLOCK_LOW_AND_ABOVE' AS threshold),
      STRUCT('HARM_CATEGORY_DANGEROUS_CONTENT' AS category,
        'BLOCK_MEDIUM_AND_ABOVE' AS threshold)] AS safety_settings));
```

**範例 5**

以下範例顯示具有這些特性的要求：

* 使用 `prompts` 資料表的 `prompt` 欄做為提示。
* 傳回較長的回覆。

```
SELECT *
FROM
  AI.GENERATE_TEXT(
    MODEL `mydataset.flash_2_model`,
    TABLE mydataset.prompts,
    STRUCT(
      0.4 AS temperature, 8192 AS max_output_tokens));
```

**範例 6**

以下範例顯示具有這些特性的要求：

* 提示詞，用於摘要 `articles` 資料表 `body` 欄中的文字。
* 擷取並傳回公開網路資料，做為回覆基準。
* 使用兩項安全設定篩除不安全的回覆。

```
SELECT *
FROM
  AI.GENERATE_TEXT(
    MODEL `mydataset.text_model`,
    (
      SELECT CONCAT('Summarize this text', body) AS prompt
      FROM mydataset.articles
    ),
    STRUCT(
      .1 AS TEMPERATURE,
      TRUE AS ground_with_google_search,
      [STRUCT('HARM_CATEGORY_HATE_SPEECH' AS category,
        'BLOCK_LOW_AND_ABOVE' AS threshold),
      STRUCT('HARM_CATEGORY_DANGEROUS_CONTENT' AS category,
        'BLOCK_MEDIUM_AND_ABOVE' AS threshold)] AS safety_settings));
```

### Claude

```
SELECT *
FROM AI.GENERATE_TEXT(
  MODEL `PROJECT_ID.DATASET_ID.MODEL_NAME`,
  {TABLE PROJECT_ID.DATASET_ID.TABLE_NAME | (PROMPT_QUERY)},
  STRUCT(
  {
    {
      [MAX_OUTPUT_TOKENS AS max_output_tokens]
      [, TOP_K AS top_k]
      [, TOP_P AS top_p]
    }
    |
    [, MODEL_PARAMS AS model_params]
  })
);
```

替換下列內容：

* `PROJECT_ID`：您的專案 ID。
* `DATASET_ID`：模型所在資料集的 ID。
* `MODEL_NAME`：模型名稱。
* `TABLE_NAME`：包含提示詞的資料表名稱。這個資料表必須有名為 `prompt` 的資料欄，或者您可以使用別名，改用其他名稱的資料欄。
* `PROMPT_QUERY`：提供提示資料的查詢。這項查詢必須產生名為 `prompt` 的資料欄。

  **注意：**

  建議不要在提示查詢中使用 [`LIMIT and OFFSET` 子句](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw#limit_and_offset_clause)。使用這個子句會導致查詢先處理所有輸入資料，然後套用 `LIMIT` 和 `OFFSET`。
* `TOKENS`：`INT64` 值，設定回覆中可生成的詞元數量上限。這個值必須介於 `[1,4096]` 之間。
  如要取得較短的回覆，請指定較低的值；如要取得較長的回覆，請調高此值。預設值為 `128`。
* `TOP_K`：`[1,40]` 範圍內的 `INT64` 值，決定模型考慮選取的初始詞元集區。如要取得較不隨機的回覆，請指定較低的值；如要取得較隨機的回覆，請調高此值。如未指定值，模型會決定適當的值。
* `TOP_P`：`[0.0,1.0]` 範圍內的 `FLOAT64` 值，有助於判斷所選詞元的機率。如要取得較不隨機的回覆，請指定較低的值；如要取得較隨機的回覆，請調高此值。如未指定值，模型會決定適當的值。
* `MODEL_PARAMS`：JSON 格式的字串常值，可為模型提供參數。這個值必須符合 [`generateContent` 要求主體](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/reference/rest/v1/projects.locations.endpoints/generateContent?hl=zh-tw)格式。您可以為要求主體中的任何欄位提供值，但 `contents[]` 欄位除外。如果設定這個欄位，就無法在 `AI.GENERATE_TEXT` 函式的頂層結構體引數中指定任何模型參數。您必須在 `MODEL_PARAMS` 欄位中指定每個模型參數，或省略這個欄位並分別指定每個參數。

**範例 1**

以下範例顯示具有這些特性的要求：

* 提示詞，用於摘要 `articles` 資料表 `body` 欄中的文字。

```
SELECT *
FROM
  AI.GENERATE_TEXT(
    MODEL `mydataset.text_model`,
    (
      SELECT CONCAT('Summarize this text', body) AS prompt
      FROM mydataset.articles
    ));
```

**示例 2**

以下範例顯示具有這些特性的要求：

* 使用查詢，串連提供提示[前置字元](https://docs.cloud.google.com/vertex-ai/docs/generative-ai/text/text-prompts?hl=zh-tw#prompt_structure)的字串與資料表資料欄，建立提示資料。
* 傳回簡短回覆。

```
SELECT *
FROM
  AI.GENERATE_TEXT(
    MODEL `mydataset.text_model`,
    (
      SELECT CONCAT(question, 'Text:', description, 'Category') AS prompt
      FROM mydataset.input_table
    ),
    STRUCT(
      100 AS max_output_tokens));
```

**範例 3**

以下範例顯示具有這些特性的要求：

* 使用 `prompts` 資料表的 `prompt` 欄做為提示。

```
SELECT *
FROM
  AI.GENERATE_TEXT(
    MODEL `mydataset.text_model`,
    TABLE mydataset.prompts);
```

### Llama

```
SELECT *
FROM AI.GENERATE_TEXT(
  MODEL `PROJECT_ID.DATASET_ID.MODEL_NAME`,
  {TABLE PROJECT_ID.DATASET_ID.TABLE_NAME | (PROMPT_QUERY)},
  STRUCT(
  {
    {
      [MAX_OUTPUT_TOKENS AS max_output_tokens]
      [, TOP_P AS top_p]
      [, TEMPERATURE AS temperature]
      [, STOP_SEQUENCES AS stop_sequences]
    |
    }
    [, MODEL_PARAMS AS model_params]
  })
);
```

替換下列內容：

* `PROJECT_ID`：您的專案 ID。
* `DATASET_ID`：模型所在資料集的 ID。
* `MODEL_NAME`：模型名稱。
* `TABLE_NAME`：包含提示詞的資料表名稱。這個資料表必須有名為 `prompt` 的資料欄，或者您可以使用別名，改用其他名稱的資料欄。
* `PROMPT_QUERY`：提供提示資料的查詢。這項查詢必須產生名為 `prompt` 的資料欄。

  **注意：**

  建議不要在提示查詢中使用 [`LIMIT and OFFSET` 子句](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw#limit_and_offset_clause)。使用這個子句會導致查詢先處理所有輸入資料，然後套用 `LIMIT` 和 `OFFSET`。
* `TOKENS`：`INT64` 值，設定回覆中可生成的詞元數量上限。這個值必須介於 `[1,4096]` 之間。
  如要取得較短的回覆，請指定較低的值；如要取得較長的回覆，請調高此值。預設值為 `128`。
* `TEMPERATURE`：`FLOAT64` 值，範圍為 `[0.0,1.0]`，可控制選取詞元的隨機程度。預設值為 `0`。

  如果想藉由提示生成更具確定性、較不具開放性和創意性的回覆，建議調低 `temperature`。另一方面，如果 `temperature` 較高，則可能產生較多元或有創意的結果。如果 `temperature` 的值為 `0`，則具有確定性，即模型一律會選取可能性最高的回覆。
* `TOP_P`：`[0.0,1.0]` 範圍內的 `FLOAT64` 值，有助於判斷所選詞元的機率。如要取得較不隨機的回覆，請指定較低的值；如要取得較隨機的回覆，請調高此值。預設為 `0.95`。
* `STOP_SEQUENCES`：`ARRAY<STRING>` 值，如果模型的回覆中包含指定字串，則會移除這些字串。字串必須完全相符，包括大小寫。預設為空陣列。
* `MODEL_PARAMS`：JSON 格式的字串常值，可為模型提供參數。這個值必須符合 [`generateContent` 要求主體](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/reference/rest/v1/projects.locations.endpoints/generateContent?hl=zh-tw)格式。您可以為要求主體中的任何欄位提供值，但 `contents[]` 欄位除外。如果設定這個欄位，就無法在 `AI.GENERATE_TEXT` 函式的頂層結構體引數中指定任何模型參數。您必須在 `MODEL_PARAMS` 欄位中指定每個模型參數，或省略這個欄位並分別指定每個參數。

**範例 1**

以下範例顯示具有這些特性的要求：

* 提示詞，用於摘要 `articles` 資料表 `body` 欄中的文字。

```
SELECT *
FROM
  AI.GENERATE_TEXT(
    MODEL `mydataset.text_model`,
    (
      SELECT CONCAT('Summarize this text', body) AS prompt
      FROM mydataset.articles
    ));
```

**示例 2**

以下範例顯示具有這些特性的要求：

* 使用查詢，串連提供提示[前置字元](https://docs.cloud.google.com/vertex-ai/docs/generative-ai/text/text-prompts?hl=zh-tw#prompt_structure)的字串與資料表資料欄，建立提示資料。
* 傳回簡短回覆。

```
SELECT *
FROM
  AI.GENERATE_TEXT(
    MODEL `mydataset.text_model`,
    (
      SELECT CONCAT(question, 'Text:', description, 'Category') AS prompt
      FROM mydataset.input_table
    ),
    STRUCT(
      100 AS max_output_tokens));
```

**範例 3**

以下範例顯示具有這些特性的要求：

* 使用 `prompts` 資料表的 `prompt` 欄做為提示。

```
SELECT *
FROM
  AI.GENERATE_TEXT(
    MODEL `mydataset.text_model`,
    TABLE mydataset.prompts);
```

### Mistral AI

```
SELECT *
FROM AI.GENERATE_TEXT(
  MODEL `PROJECT_ID.DATASET_ID.MODEL_NAME`,
  {TABLE PROJECT_ID.DATASET_ID.TABLE_NAME | (PROMPT_QUERY)},
  STRUCT(
  {
    {
      [MAX_OUTPUT_TOKENS AS max_output_tokens]
      [, TOP_P AS top_p]
      [, TEMPERATURE AS temperature]
      [, STOP_SEQUENCES AS stop_sequences]
    |
    }
    [, MODEL_PARAMS AS model_params]
  })
);
```

替換下列內容：

* `PROJECT_ID`：您的專案 ID。
* `DATASET_ID`：模型所在資料集的 ID。
* `MODEL_NAME`：模型名稱。
* `TABLE_NAME`：包含提示詞的資料表名稱。這個資料表必須有名為 `prompt` 的資料欄，或者您可以使用別名，改用其他名稱的資料欄。
* `PROMPT_QUERY`：提供提示資料的查詢。這項查詢必須產生名為 `prompt` 的資料欄。

  **注意：**

  建議不要在提示查詢中使用 [`LIMIT and OFFSET` 子句](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw#limit_and_offset_clause)。使用這個子句會導致查詢先處理所有輸入資料，然後套用 `LIMIT` 和 `OFFSET`。
* `TOKENS`：`INT64` 值，設定回覆中可生成的詞元數量上限。這個值必須介於 `[1,4096]` 之間。
  如要取得較短的回覆，請指定較低的值；如要取得較長的回覆，請調高此值。預設值為 `128`。
* `TEMPERATURE`：`FLOAT64` 值，範圍為 `[0.0,1.0]`，可控制選取詞元的隨機程度。預設值為 `0`。

  如果想藉由提示生成更具確定性、較不具開放性和創意性的回覆，建議調低 `temperature`。另一方面，如果 `temperature` 較高，則可能產生較多元或有創意的結果。如果 `temperature` 的值為 `0`，則具有確定性，即模型一律會選取可能性最高的回覆。
* `TOP_P`：`[0.0,1.0]` 範圍內的 `FLOAT64` 值，有助於判斷所選詞元的機率。如要取得較不隨機的回覆，請指定較低的值；如要取得較隨機的回覆，請調高此值。預設為 `0.95`。
* `STOP_SEQUENCES`：`ARRAY<STRING>` 值，如果模型的回覆中包含指定字串，則會移除這些字串。字串必須完全相符，包括大小寫。預設為空陣列。
* `MODEL_PARAMS`：JSON 格式的字串常值，可為模型提供參數。值必須符合 [`generateContent` 要求主體](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/reference/rest/v1/projects.locations.endpoints/generateContent?hl=zh-tw)格式。您可以為要求主體中的任何欄位提供值，但 `contents[]` 欄位除外。如果設定這個欄位，就無法在 `AI.GENERATE_TEXT` 函式的頂層結構體引數中指定任何模型參數。您必須在 `MODEL_PARAMS` 欄位中指定每個模型參數，或省略這個欄位並分別指定每個參數。

**範例 1**

以下範例顯示具有這些特性的要求：

* 提示詞，用於摘要 `articles` 資料表 `body` 欄中的文字。

```
SELECT *
FROM
  AI.GENERATE_TEXT(
    MODEL `mydataset.text_model`,
    (
      SELECT CONCAT('Summarize this text', body) AS prompt
      FROM mydataset.articles
    ));
```

**示例 2**

以下範例顯示具有這些特性的要求：

* 使用查詢，串連提供提示[前置字元](https://docs.cloud.google.com/vertex-ai/docs/generative-ai/text/text-prompts?hl=zh-tw#prompt_structure)的字串與資料表資料欄，建立提示資料。
* 傳回簡短回覆。

```
SELECT *
FROM
  AI.GENERATE_TEXT(
    MODEL `mydataset.text_model`,
    (
      SELECT CONCAT(question, 'Text:', description, 'Category') AS prompt
      FROM mydataset.input_table
    ),
    STRUCT(
      100 AS max_output_tokens));
```

**範例 3**

以下範例顯示具有這些特性的要求：

* 使用 `prompts` 資料表的 `prompt` 欄做為提示。

```
SELECT *
FROM
  AI.GENERATE_TEXT(
    MODEL `mydataset.text_model`,
    TABLE mydataset.prompts);
```

### 開放式模型

**注意：** 您必須先在 Gemini Enterprise Agent Platform 部署開放原始碼模型，才能使用這些模型。詳情請參閱「[部署開放原始碼模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model-open?hl=zh-tw#deploy_open_models)」。

```
SELECT *
FROM AI.GENERATE_TEXT(
  MODEL `PROJECT_ID.DATASET_ID.MODEL_NAME`,
  {TABLE PROJECT_ID.DATASET_ID.TABLE_NAME | (PROMPT_QUERY)},
  STRUCT(
  {
    {
      [MAX_OUTPUT_TOKENS AS max_output_tokens]
      [, TOP_K AS top_k]
      [, TOP_P AS top_p]
      [, TEMPERATURE AS temperature]
    }
    |
    [, MODEL_PARAMS AS model_params]
  })
);
```

替換下列內容：

* `PROJECT_ID`：您的專案 ID。
* `DATASET_ID`：模型所在資料集的 ID。
* `MODEL_NAME`：模型名稱。
* `TABLE_NAME`：包含提示詞的資料表名稱。這個資料表必須有名為 `prompt` 的資料欄，或者您可以使用別名，改用其他名稱的資料欄。
* `PROMPT_QUERY`：提供提示資料的查詢。這項查詢必須產生名為 `prompt` 的資料欄。

  **注意：**

  建議不要在提示查詢中使用 [`LIMIT and OFFSET` 子句](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw#limit_and_offset_clause)。使用這個子句會導致查詢先處理所有輸入資料，然後套用 `LIMIT` 和 `OFFSET`。
* `TOKENS`：`INT64` 值，設定回覆中可生成的詞元數量上限。這個值必須介於 `[1,4096]` 之間。
  如要取得較短的回覆，請指定較低的值；如要取得較長的回覆，請調高此值。如未指定值，模型會決定適當的值。
* `TEMPERATURE`：`FLOAT64` 值，範圍為 `[0.0,1.0]`，可控制選取詞元的隨機程度。如未指定值，模型會決定適當的值。

  如果想藉由提示生成更具確定性、較不具開放性和創意性的回覆，建議調低 `temperature`。另一方面，如果 `temperature` 較高，則可能產生較多元或有創意的結果。如果 `temperature` 的值為 `0`，則具有確定性，即模型一律會選取可能性最高的回覆。
* `TOP_K`：`[1,40]` 範圍內的 `INT64` 值，決定模型考慮選取的初始詞元集區。如要取得較不隨機的回覆，請指定較低的值；如要取得較隨機的回覆，請調高此值。如未指定值，模型會決定適當的值。
* `TOP_P`：`[0.0,1.0]` 範圍內的 `FLOAT64` 值，有助於判斷所選詞元的機率。如要取得較不隨機的回覆，請指定較低的值；如要取得較隨機的回覆，請調高此值。如未指定值，模型會決定適當的值。
* `MODEL_PARAMS`：JSON 格式的字串常值，可為模型提供參數。這個值必須符合 [`generateContent` 要求主體](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/reference/rest/v1/projects.locations.endpoints/generateContent?hl=zh-tw)格式。您可以為要求主體中的任何欄位提供值，但 `contents[]` 欄位除外。如果設定這個欄位，就無法在 `AI.GENERATE_TEXT` 函式的頂層結構體引數中指定任何模型參數。您必須在 `MODEL_PARAMS` 欄位中指定每個模型參數，或省略這個欄位並分別指定每個參數。

**範例 1**

以下範例顯示具有這些特性的要求：

* 提示詞，用於摘要 `articles` 資料表 `body` 欄中的文字。

```
SELECT *
FROM
  AI.GENERATE_TEXT(
    MODEL `mydataset.text_model`,
    (
      SELECT CONCAT('Summarize this text', body) AS prompt
      FROM mydataset.articles
    ));
```

**示例 2**

以下範例顯示具有這些特性的要求：

* 使用查詢，串連提供提示[前置字元](https://docs.cloud.google.com/vertex-ai/docs/generative-ai/text/text-prompts?hl=zh-tw#prompt_structure)的字串與資料表資料欄，建立提示資料。
* 傳回簡短回覆。

```
SELECT *
FROM
  AI.GENERATE_TEXT(
    MODEL `mydataset.text_model`,
    (
      SELECT CONCAT(question, 'Text:', description, 'Category') AS prompt
      FROM mydataset.input_table
    ),
    STRUCT(
      100 AS max_output_tokens));
```

**範例 3**

以下範例顯示具有這些特性的要求：

* 使用 `prompts` 資料表的 `prompt` 欄做為提示。

```
SELECT *
FROM
  AI.GENERATE_TEXT(
    MODEL `mydataset.text_model`,
    TABLE mydataset.prompts);
```

## 根據物件資料表資料生成文字

使用 [`AI.GENERATE_TEXT` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-ai-generate-text?hl=zh-tw)搭配 Gemini 模型生成文字，分析物件資料表中的非結構化資料。您可以在 `prompt` 參數中提供提示資料。

```
SELECT *
FROM AI.GENERATE_TEXT(
MODEL `PROJECT_ID.DATASET.MODEL`,
{ TABLE `PROJECT_ID.DATASET.TABLE` | (QUERY_STATEMENT) },
STRUCT(
  PROMPT AS prompt
  {
    {
      [, MAX_OUTPUT_TOKENS AS max_output_tokens]
      [, TOP_P AS top_p]
      [, TEMPERATURE AS temperature]
      [, STOP_SEQUENCES AS stop_sequences]
      [, SAFETY_SETTINGS AS safety_settings]
    }
    |
    [, MODEL_PARAMS AS model_params]
  })
);
```

更改下列內容：

* `PROJECT_ID`：包含資源的專案。
* `DATASET`：包含資源的資料集。
* `MODEL`：Gemini Enterprise Agent Platform 模型上的遠端模型名稱。如要進一步瞭解如何建立這類遠端模型，請參閱「[透過 LLM 建立遠端模型的 `CREATE MODEL` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model?hl=zh-tw)」。

  如要確認遠端模型使用的模型，請開啟 Google Cloud 控制台，然後查看模型詳細資料頁面中的「Remote endpoint」(遠端端點) 欄位。

  注意：使用以 Gemini 2.5 模型為基礎的遠端模型，會產生[思考程序](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/thinking?hl=zh-tw)費用。
* `TABLE`：[物件資料表](https://docs.cloud.google.com/bigquery/docs/object-table-introduction?hl=zh-tw)的名稱，其中包含要分析的內容。如要進一步瞭解可分析的內容類型，請參閱「[輸入](#input)」。

  輸入物件資料表使用的 Cloud Storage bucket，必須位於您建立模型及呼叫 `AI.GENERATE_TEXT` 函式的專案中。
* `QUERY_STATEMENT`：生成圖片資料的 GoogleSQL 查詢。您只能在查詢中指定 `WHERE` 和 `ORDER BY` 子句。
* `PROMPT`：`STRING` 值，包含用於分析影像內容的提示。`prompt` 值必須少於 16,000 個權杖。一個詞元可能比一個字詞還短，約為四個字元。100 個詞元約等於 60 到 80 個字。

#### 顯示其他選用參數

* `MAX_OUTPUT_TOKENS`：`INT64` 值，用於設定回覆中可生成的詞元數量上限。這個值必須介於 `[1,8192]` 之間。如要取得較短的回覆，請指定較低的值；如要取得較長的回覆，請調高此值。預設值為 `1024`。
* `TOP_P`：`[0.0,1.0]` 範圍內的 `FLOAT64` 值，會影響模型選取輸出詞元的方式。如要取得較不隨機的回覆，請指定較低的值；如要取得較隨機的回覆，請調高此值。預設為 `0.95`。

  模型會按照機率最高到最低的順序選取詞元，直到所選詞元的機率總和等於 `TOP_P` 值。舉例來說，假設詞元 A、B 和 C 的可能性分別為 `0.3`、`0.2` 和 `0.1`，而 `TOP_P` 值為 `0.5`，模型會依據 `TEMPERATURE` 值選擇 A 或 B 做為下一個詞元，並排除 C。
* `TEMPERATURE`：`FLOAT64` 值，範圍為 `[0.0,1.0]`，可控制選取詞元的隨機程度。如果想藉由提示生成更具確定性、較不具開放性和創意性的回覆，建議調低 `TEMPERATURE`。另一方面，如果 `TEMPERATURE` 較高，則可能產生較多元或有創意的結果。`TEMPERATURE` 值為 `0` 代表具有確定性，即模型一律會選取可能性最高的回覆。預設為 `0`。
* `STOP_SEQUENCES`：`ARRAY` 值，如果模型回覆中包含指定字串，就會移除這些字串。字串必須完全相符，包括大小寫。預設值為空陣列。
* `SAFETY_SETTINGS`：`ARRAY>` 值，用於設定內容安全門檻來篩選回覆。struct 中的第一個元素指定有害內容類別，第二個元素則指定對應的封鎖門檻。模型會篩除違反這些設定的內容。每個類別只能指定一次。舉例來說，您無法同時指定 `STRUCT('HARM_CATEGORY_DANGEROUS_CONTENT' AS category,
  'BLOCK_MEDIUM_AND_ABOVE' AS threshold)` 和 `STRUCT('HARM_CATEGORY_DANGEROUS_CONTENT' AS category,
  'BLOCK_ONLY_HIGH' AS threshold)`。如果特定類別沒有安全設定，系統會使用 `BLOCK_MEDIUM_AND_ABOVE` 安全設定。

  支援的類別如下：

  + `HARM_CATEGORY_HATE_SPEECH`
  + `HARM_CATEGORY_DANGEROUS_CONTENT`
  + `HARM_CATEGORY_HARASSMENT`
  + `HARM_CATEGORY_SEXUALLY_EXPLICIT`

  支援的門檻如下：

  + `BLOCK_NONE`
    ([受限](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/multimodal/configure-safety-attributes?hl=zh-tw#how_to_remove_automated_response_blocking_for_select_safety_attributes))