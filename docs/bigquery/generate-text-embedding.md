Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 使用 AI.GENERATE\_EMBEDDING 函式生成文字嵌入

本文說明如何建立參照嵌入模型的 BigQuery ML [遠端模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model?hl=zh-tw)。接著，您將使用前面建立的模型和 [`AI.GENERATE_EMBEDDING` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-ai-generate-embedding?hl=zh-tw)，透過 BigQuery [標準資料表](https://docs.cloud.google.com/bigquery/docs/tables-intro?hl=zh-tw#standard-tables)中的資料建立文字嵌入。

支援的遠端模型類型如下：

* [遠端模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model?hl=zh-tw)
  透過
  [Vertex AI 嵌入模型](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/models?hl=zh-tw#embeddings-models)。
* [遠端模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model-open?hl=zh-tw)
  超過
  [支援的開放式模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model-open?hl=zh-tw#supported_open_models)。

## 必要的角色

如要建立遠端模型並使用 `AI.GENERATE_EMBEDDING` 函式，您需要下列 Identity and Access Management (IAM) 角色：

* 建立及使用 BigQuery 資料集、資料表和模型：
  專案的 BigQuery 資料編輯器 (`roles/bigquery.dataEditor`)。
* 建立、委派及使用 BigQuery 連線：專案的 BigQuery 連線管理員 (`roles/bigquery.connectionsAdmin`)。

  如果沒有設定[預設連線](https://docs.cloud.google.com/bigquery/docs/default-connections?hl=zh-tw)，您可以在執行 `CREATE MODEL` 陳述式時建立並設定連線。如要這麼做，您必須具備專案的 BigQuery 管理員角色 (`roles/bigquery.admin`)。詳情請參閱「[設定預設連線](https://docs.cloud.google.com/bigquery/docs/default-connections?hl=zh-tw#configure_the_default_connection)」。
* 將權限授予連線的服務帳戶：在包含 Vertex AI 端點的專案中，授予「專案 IAM 管理員」(`roles/resourcemanager.projectIamAdmin`) 角色。這是您透過將模型名稱指定為端點所建立遠端模型的目前專案。這是您透過指定網址做為端點所建立遠端模型的網址中識別的專案。
* 建立 BigQuery 工作：專案中的 BigQuery 工作使用者 (`roles/bigquery.jobUser`)。

這些預先定義的角色具備執行本文所述工作所需的權限。如要查看確切的必要權限，請展開「Required permissions」(必要權限) 部分：

#### 所需權限

* 建立資料集：`bigquery.datasets.create`
* 建立、委派及使用連線：
  `bigquery.connections.*`
* 設定服務帳戶權限：
  `resourcemanager.projects.getIamPolicy` 和
  `resourcemanager.projects.setIamPolicy`
* 建立模型並執行推論：
  + `bigquery.jobs.create`
  + `bigquery.models.create`
  + `bigquery.models.getData`
  + `bigquery.models.updateData`
  + `bigquery.models.updateMetadata`
* 查詢資料表資料：`bigquery.tables.getData`

您或許還可透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)取得這些權限。

## 事前準備

1. 在 Google Cloud 控制台的專案選擇器頁面中，選取或建立 Google Cloud 專案。

   **選取或建立專案所需的角色**

   * **選取專案**：選取專案時，不需要具備特定 IAM 角色，只要您已獲授角色，即可選取任何專案。
   * **建立專案**：如要建立專案，您需要「專案建立者」角色 (`roles/resourcemanager.projectCreator`)，其中包含 `resourcemanager.projects.create` 權限。[瞭解如何授予角色](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)。
   **注意**：如果您不打算保留在這項程序中建立的資源，請建立新專案，而不要選取現有專案。完成這些步驟後，您就可以刪除專案，並移除與該專案相關聯的所有資源。

   [前往專案選取器](https://console.cloud.google.com/projectselector2/home/dashboard?hl=zh-tw)
2. [確認專案已啟用計費功能 Google Cloud](https://docs.cloud.google.com/billing/docs/how-to/verify-billing-enabled?hl=zh-tw#confirm_billing_is_enabled_on_a_project) 。
3. 啟用 BigQuery、BigQuery Connection 和 Vertex AI API。

   **啟用 API 時所需的角色**

   如要啟用 API，您需要服務使用情形管理員 IAM 角色 (`roles/serviceusage.serviceUsageAdmin`)，其中包含 `serviceusage.services.enable` 權限。[瞭解如何授予角色](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)。

   [啟用 API](https://console.cloud.google.com/apis/enableflow?apiid=bigquery.googleapis.com%2Cbigqueryconnection.googleapis.com%2Caiplatform.googleapis.com&hl=zh-tw)

## 建立資料集

建立 BigQuery 資料集來存放資源：

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。

   如果沒有看到左側窗格，請按一下 last\_page「Expand left pane」(展開左側窗格)，開啟窗格。
3. 在「Explorer」窗格中，按一下專案名稱。
4. 依序點按 more\_vert「View actions」(查看動作) >「Create dataset」(建立資料集)。
5. 在「建立資料集」頁面中，執行下列操作：

   1. 在「Dataset ID」(資料集 ID) 部分，輸入資料集的名稱。
   2. 在「位置類型」部分，選取「區域」或「多區域」。

      * 如果選取「區域」，請從「區域」清單中選取位置。
      * 如果選取「多區域」，請從「多區域」清單中選取「美國」或「歐洲」。
   3. 點選「建立資料集」。

### bq

1. 如要建立新的資料集，請使用 [`bq mk`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#mk-dataset) 指令，並加上 `--location` 旗標：

   ```
   bq --location=LOCATION mk -d DATASET_ID
   ```

   更改下列內容：

   * `LOCATION`：資料集的[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)。
   * `DATASET_ID` 是您要建立的資料集 ID。
2. 確認資料集已建立完成：

   ```
   bq ls
   ```

## 建立連線

建立[Cloud 資源連線](https://docs.cloud.google.com/bigquery/docs/create-cloud-resource-connection?hl=zh-tw)，並取得連線的服務帳戶。在與上一步建立的資料集相同的[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)中建立連線。

如果已設定預設連線，或您具備 BigQuery 管理員角色，可以略過這個步驟。

選取下列選項之一：

### 控制台

1. 前往「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。

   如果沒有看到左側窗格，請按一下 last\_page「Expand left pane」(展開左側窗格)，開啟窗格。
3. 在「Explorer」窗格中展開專案名稱，然後按一下「Connections」。
4. 在「Connections」(連線) 頁面中，按一下「Create connection」(建立連線)。
5. 在「連線類型」中，選擇「Vertex AI 遠端模型、遠端函式、BigLake 和 Spanner (Cloud 資源)」。
6. 在「連線 ID」欄位中，輸入連線名稱。
7. 在「位置類型」部分，選取連線位置。連線應與資料集等其他資源位於同一位置。
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

   請替換下列項目：

   * `CONNECTION_NAME`：連線名稱，格式為 `PROJECT_ID.LOCATION.CONNECTION_ID`、`LOCATION.CONNECTION_ID` 或 `CONNECTION_ID`。如果省略專案或位置，系統會從執行陳述式的專案和位置推斷。
   * `FRIENDLY_NAME` (選用)：連線的描述性名稱。
   * `DESCRIPTION` (選用)：連線說明。
3. 按一下「執行」play\_circle。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

### bq

1. 在指令列環境中建立連線：

   ```
   bq mk --connection --location=REGION --project_id=PROJECT_ID \
       --connection_type=CLOUD_RESOURCE CONNECTION_ID
   ```

   `--project_id` 參數會覆寫預設專案。

   更改下列內容：

   * `REGION`：您的[連線區域](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw#supported_locations)
   * `PROJECT_ID`：您的 Google Cloud 專案 ID
   * `CONNECTION_ID`：連線的 ID

   建立連線資源時，BigQuery 會建立專屬的系統服務帳戶，並將其與連線建立關聯。

   **疑難排解**：如果收到下列連線錯誤訊息，請[更新 Google Cloud SDK](https://docs.cloud.google.com/sdk/docs/quickstart?hl=zh-tw)：

   ```
   Flags parsing error: flag --connection_type=CLOUD_RESOURCE: value should be one of...
   ```
2. 擷取並複製服務帳戶 ID，以供後續步驟使用：

   ```
   bq show --connection PROJECT_ID.REGION.CONNECTION_ID
   ```

   輸出結果會與下列內容相似：

   ```
   name                          properties
   1234.REGION.CONNECTION_ID     {"serviceAccountId": "connection-1234-9u56h9@gcp-sa-bigquery-condel.iam.gserviceaccount.com"}
   ```

### Python

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Python 設定說明操作。詳情請參閱 [BigQuery Python API 參考說明文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

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

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Node.js 設定說明操作。詳情請參閱 [BigQuery Node.js API 參考說明文件](https://googleapis.dev/nodejs/bigquery/latest/index.html)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

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

### Terraform

請使用 [`google_bigquery_connection`](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/bigquery_connection) 資源。

**注意：** 如要使用 Terraform 建立 BigQuery 物件，必須啟用 [Cloud Resource Manager API](https://docs.cloud.google.com/resource-manager/reference/rest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

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

   您只需要為每項專案執行一次這個指令，且可以在任何目錄中執行。

   ```
   export GOOGLE_CLOUD_PROJECT=PROJECT_ID
   ```

   如果您在 Terraform 設定檔中設定明確值，環境變數就會遭到覆寫。

## 準備目錄

每個 Terraform 設定檔都必須有自己的目錄 (也稱為*根模組*)。

1. 在 [Cloud Shell](https://shell.cloud.google.com/?hl=zh-tw) 中建立目錄，並在該目錄中建立新檔案。檔案名稱的副檔名必須是 `.tf`，例如 `main.tf`。在本教學課程中，這個檔案稱為 `main.tf`。

   ```
   mkdir DIRECTORY && cd DIRECTORY && touch main.tf
   ```
2. 如果您正在學習教學課程，可以複製每個章節或步驟中的程式碼範例。

   將程式碼範例複製到新建立的 `main.tf`。

   視需要從 GitHub 複製程式碼。如果 Terraform 代码片段是端對端解決方案的一部分，建議您使用這個方法。
3. 查看並修改範例參數，套用至您的環境。
4. 儲存變更。
5. 初始化 Terraform。每個目錄只需執行一次這項操作。

   ```
   terraform init
   ```

   如要使用最新版 Google 供應商，請加入 `-upgrade` 選項：

   ```
   terraform init -upgrade
   ```

## 套用變更

1. 查看設定，確認 Terraform 即將建立或更新的資源符合您的預期：

   ```
   terraform plan
   ```

   視需要修正設定。
2. 執行下列指令，並在提示中輸入 `yes`，套用 Terraform 設定：

   ```
   terraform apply
   ```

   等待 Terraform 顯示「Apply complete!」訊息。
3. [開啟 Google Cloud 專案](https://console.cloud.google.com/?hl=zh-tw)即可查看結果。在 Google Cloud 控制台中，前往 UI 中的資源，確認 Terraform 已建立或更新這些資源。

**注意：**Terraform 範例通常會假設 Google Cloud 專案已啟用必要的 API。

### 將角色指派給遠端模型連線的服務帳戶

您必須為連線的服務帳戶授予 Vertex AI 使用者角色。

如果您打算在建立遠端模型時將端點指定為網址 (例如 `endpoint = 'https://us-central1-aiplatform.googleapis.com/v1/projects/myproject/locations/us-central1/publishers/google/models/text-embedding-005'`)，請在網址指定的專案中授予這個角色。

如果您打算在建立遠端模型時使用模型名稱指定端點 (例如 `endpoint = 'text-embedding-005'`)，請在您要建立遠端模型的專案中授予這個角色。

在其他專案中授予角色會導致錯誤 `bqcx-1234567890-wxyz@gcp-sa-bigquery-condel.iam.gserviceaccount.com does not have the permission to access resource`。

如要授予角色，請按照下列步驟操作：

### 控制台

1. 前往「IAM & Admin」(IAM 與管理) 頁面。

   [前往「IAM & Admin」(IAM 與管理)](https://console.cloud.google.com/project/_/iam-admin?hl=zh-tw)
2. 按一下 person\_add「授予存取權」。

   「新增主體」對話方塊隨即開啟。
3. 在「新增主體」欄位，輸入先前複製的服務帳戶 ID。
4. 在「選取角色」欄位中，依序選取「Vertex AI」和「Vertex AI 使用者」。
5. 按一下 [儲存]。

### gcloud

使用 [`gcloud projects add-iam-policy-binding`](https://docs.cloud.google.com/sdk/gcloud/reference/projects/add-iam-policy-binding?hl=zh-tw) 指令：

```
gcloud projects add-iam-policy-binding 'PROJECT_NUMBER' --member='serviceAccount:MEMBER' --role='roles/aiplatform.user' --condition=None
```

請替換下列項目：

* `PROJECT_NUMBER`：您的專案編號
* `MEMBER`：您先前複製的服務帳戶 ID

## 選擇開放模型部署方式

如果您要透過[支援的開放式模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model-open?hl=zh-tw#supported_open_models)建立遠端模型，可以在 `CREATE MODEL` 陳述式中指定 Vertex AI Model Garden 或 Hugging Face 模型 ID，在建立遠端模型的同時自動部署開放式模型。或者，您也可以先手動部署開放模型，然後在 `CREATE MODEL` 陳述式中指定模型端點，將該開放模型與遠端模型搭配使用。詳情請參閱「[部署開放模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model-open?hl=zh-tw#deploy_open_models)」。

## 建立 BigQuery ML 遠端模型

建立遠端模型：

### Vertex AI 模型

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 使用 SQL 編輯器建立[遠端模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model?hl=zh-tw)：

   ```
   CREATE OR REPLACE MODEL
   `PROJECT_ID.DATASET_ID.MODEL_NAME`
   REMOTE WITH CONNECTION {DEFAULT | `PROJECT_ID.REGION.CONNECTION_ID`}
   OPTIONS (ENDPOINT = 'ENDPOINT');
   ```

   請替換下列項目：

   * `PROJECT_ID`：您的專案 ID。
   * `DATASET_ID`：要包含模型的資料集 ID。這個資料集必須與您使用的連線位於相同的[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)。
   * `MODEL_NAME`：模型名稱。
   * `REGION`：連線使用的區域。
   * `CONNECTION_ID`：BigQuery 連線的 ID。

     如要取得這個值，請在 Google Cloud 控制台中[查看連線詳細資料](https://docs.cloud.google.com/bigquery/docs/working-with-connections?hl=zh-tw#view-connections)，然後複製「連線 ID」中顯示的完整連線 ID 最後一個部分的值。例如：`projects/myproject/locations/connection_location/connections/myconnection`。
   * `ENDPOINT`：要使用的嵌入模型名稱。詳情請參閱 [`ENDPOINT`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model?hl=zh-tw#endpoint)。

     您指定的 Vertex AI 模型必須位於建立遠端模型的位置。詳情請參閱「[位置](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model?hl=zh-tw#locations)」。

### 全新開放式模型

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

   請替換下列項目：

   * `PROJECT_ID`：您的專案 ID。
   * `DATASET_ID`：要包含模型的資料集 ID。這個資料集必須與您使用的連線位於相同的[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)。
   * `MODEL_NAME`：模型名稱。
   * `REGION`：連線使用的區域。
   * `CONNECTION_ID`：BigQuery 連線的 ID。

     如要取得這個值，請在 Google Cloud 控制台中[查看連線詳細資料](https://docs.cloud.google.com/bigquery/docs/working-with-connections?hl=zh-tw#view-connections)，然後複製「連線 ID」中顯示的完整連線 ID 最後一個部分的值。例如：`projects/myproject/locations/connection_location/connections/myconnection`。
   * `HUGGING_FACE_MODEL_ID`：`STRING` 值，指定[支援的 Hugging Face 模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model-open?hl=zh-tw#hugging-face-models)的 ID，格式為 `provider_name`/`model_name`，例如 `deepseek-ai/DeepSeek-R1`。如要取得模型 ID，請在 Hugging Face Model Hub 中按一下模型名稱，然後從模型資訊卡的頂端複製模型 ID。
   * `MODEL_GARDEN_MODEL_NAME`：`STRING` 值，指定[支援的 Vertex AI Model Garden 模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model-open?hl=zh-tw#model-garden-models)的模型 ID 和模型版本，格式為 `publishers/publisher`/models/`model_name`@`model_version`。
     例如：`publishers/openai/models/gpt-oss@gpt-oss-120b`。如要取得模型 ID，請在 Vertex AI Model Garden 中按一下模型資訊卡，然後從「模型 ID」欄位複製模型 ID。如要取得預設模型版本，請從模型資訊卡上的「版本」欄位複製。如要查看其他可用的模型版本，請按一下「部署模型」，然後點選「資源 ID」欄位。
   * `HUGGING_FACE_TOKEN`：指定要使用的 Hugging Face [User Access Token](https://huggingface.co/docs/hub/en/security-tokens) 的 `STRING` 值。只有在同時指定 `HUGGING_FACE_MODEL_ID` 選項的值時，才能為這個選項指定值。

     權杖至少須具備 `read` 角色，但範圍較廣的權杖也適用。如果 `HUGGING_FACE_MODEL_ID` 值所識別的模型是 Hugging Face [封閉式](https://huggingface.co/docs/hub/en/models-gated)或私人模型，則必須使用這個選項。

     部分受限模型需要明確同意服務條款，才能取得存取權。如要同意這些條款，請按照下列步驟操作：

     1. 前往 Hugging Face 網站上的模型頁面。
     2. 找出並詳閱模型服務條款。服務協議的連結通常會顯示在模型資訊卡上。
     3. 按照頁面上的提示接受條款。
   * `MACHINE_TYPE`：`STRING` 值，用於指定將模型部署至 Vertex AI 時要使用的機型。如要瞭解支援的機器類型，請參閱「[機器類型](https://docs.cloud.google.com/vertex-ai/docs/predictions/configure-compute?hl=zh-tw#machine-types)」。如果未指定 `MACHINE_TYPE` 選項的值，系統會使用模型的 Vertex AI Model Garden 預設機型。
   * `MIN_REPLICA_COUNT`：`INT64` 值，用於指定在 Vertex AI 端點上部署模型時使用的最少機器副本數。服務會視端點的推論負載，增加或減少副本數量。使用的副本數量絕不會低於 `MIN_REPLICA_COUNT` 值，也不會高於 `MAX_REPLICA_COUNT` 值。`MIN_REPLICA_COUNT` 值必須介於 `[1, 4096]` 之間。預設值為 `1`。
   * `MAX_REPLICA_COUNT`：`INT64` 值，指定在 Vertex AI 端點上部署模型時使用的機器副本數量上限。服務會視端點的推論負載，增加或減少副本數量。使用的副本數量絕不會低於 `MIN_REPLICA_COUNT` 值，也不會高於 `MAX_REPLICA_COUNT` 值。`MAX_REPLICA_COUNT` 值必須介於 `[1, 4096]` 之間。預設值為 `MIN_REPLICA_COUNT` 值。
   * `RESERVATION_AFFINITY_TYPE`：判斷已部署的模型是否使用 [Compute Engine 預留項目](https://docs.cloud.google.com/compute/docs/instances/reservations-overview?hl=zh-tw)，確保在提供預測時虛擬機器 (VM) 可用性，並指定模型是否使用所有可用預留項目的 VM，或僅使用特定預留項目的 VM。詳情請參閱「[Compute Engine 預留資源親和性](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model-open?hl=zh-tw#reservation-affinity)」。

     您只能使用與 Vertex AI 共用的 Compute Engine 預留項目。詳情請參閱「[允許使用預留項目](https://docs.cloud.google.com/vertex-ai/docs/predictions/use-reservations?hl=zh-tw#allow-consumption)」。

     支援的值如下：

     + `NO_RESERVATION`：將模型部署至 Vertex AI 端點時，不會消耗任何預留項目。指定 `NO_RESERVATION` 的效果與未指定預留項目親和性相同。
     + `ANY_RESERVATION`：Vertex AI 模型部署作業會從目前專案中，或[與專案共用](https://docs.cloud.google.com/compute/docs/instances/reservations-overview?hl=zh-tw#how-shared-reservations-work)的 Compute Engine 預留項目，取用虛擬機器 (VM)，且這些預留項目[已設定為自動取用](https://docs.cloud.google.com/compute/docs/instances/reservations-consume?hl=zh-tw#consuming_instances_from_any_matching_reservation)。系統只會使用符合下列資格的 VM：
       - 並使用 `MACHINE_TYPE` 值指定的機型。
       - 如果您要在單一區域的 BigQuery 資料集中建立遠端模型，預留項目必須位於相同區域。如果資料集位於`US`多區域，預留位置就必須位於`us-central1`區域。如果資料集位於`EU`多區域，預留位置必須位於`europe-west4`區域。

       如果可用預留容量不足，或找不到合適的預留項目，系統會佈建隨選 Compute Engine VM，以滿足資源需求。
     + `SPECIFIC_RESERVATION`：Vertex AI 模型部署只會耗用您在 `RESERVATION_AFFINITY_VALUES` 值中指定的預留項目 VM。這項預留項目必須[設定為明確指定的用量](https://docs.cloud.google.com/compute/docs/instances/reservations-consume?hl=zh-tw#consuming_instances_from_a_specific_reservation)。
       如果指定的預留項目容量不足，部署作業就會失敗。
   * `RESERVATION_AFFINITY_KEY`：字串
     `compute.googleapis.com/reservation-name`。當 `RESERVATION_AFFINITY_TYPE` 值為 `SPECIFIC_RESERVATION` 時，您必須指定這個選項。
   * `RESERVATION_AFFINITY_VALUES`：`ARRAY<STRING>` 值，指定 Compute Engine 預留項目的完整資源名稱，格式如下：  
       
     `projects/myproject/zones/reservation_zone/reservations/reservation_name`

     例如：`RESERVATION_AFFINITY_values = ['projects/myProject/zones/us-central1-a/reservations/myReservationName']`。

     您可以在 Google Cloud 控制台的「預留項目」頁面取得預留項目名稱和區域。詳情請參閱「[查看預留項目](https://docs.cloud.google.com/compute/docs/instances/reservations-view?hl=zh-tw#view-reservations)」。

     當 `RESERVATION_AFFINITY_TYPE` 值為 `SPECIFIC_RESERVATION` 時，您必須指定這個選項。
   * `ENDPOINT_IDLE_TTL`：`INTERVAL` 值，指定開放模型在閒置多久後，會自動從 Vertex AI 端點取消部署。

     如要啟用自動取消部署功能，請指定介於 390 分鐘 (6.5 小時) 至 7 天之間的[間隔常值](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/lexical?hl=zh-tw#interval_literals)值。舉例來說，指定 `INTERVAL 8 HOUR` 可讓模型在閒置 8 小時後解除部署。預設值為 390 分鐘 (6.5 小時)。

     模型閒置時間是指自對模型執行下列任一作業後經過的時間：

     + 正在執行 [`CREATE MODEL` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model-open?hl=zh-tw)。
     + 執行 [`ALTER MODEL` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-alter-model?hl=zh-tw)，並將 `DEPLOY_MODEL` 引數設為 `TRUE`。
     + 向模型端點傳送推論要求。舉例來說，您可以執行 [`AI.GENERATE_EMBEDDING`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-ai-generate-embedding?hl=zh-tw) 或 [`AI.GENERATE_TEXT`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-ai-generate-text?hl=zh-tw) 函式。

     這些作業都會將閒置計時器重設為零。在執行作業的 BigQuery 工作開始時，系統會觸發重設作業。

     取消部署模型後，傳送至模型的推論要求會傳回錯誤。BigQuery 模型物件維持不變，包括模型中繼資料。如要再次使用模型進行推論，請對模型執行 `ALTER MODEL` 陳述式，並將 `DEPLOY_MODEL` 選項設為 `TRUE`，重新部署模型。

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

   請替換下列項目：

   * `PROJECT_ID`：您的專案 ID。
   * `DATASET_ID`：要包含模型的資料集 ID。這個資料集必須與您使用的連線位於相同的[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)。
   * `MODEL_NAME`：模型名稱。
   * `REGION`：連線使用的區域。
   * `CONNECTION_ID`：BigQuery 連線的 ID。

     如要取得這個值，請在 Google Cloud 控制台中[查看連線詳細資料](https://docs.cloud.google.com/bigquery/docs/working-with-connections?hl=zh-tw#view-connections)，然後複製「連線 ID」中顯示的完整連線 ID 最後一個部分的值。例如：`projects/myproject/locations/connection_location/connections/myconnection`。
   * `ENDPOINT_REGION`：部署開放模型的區域。
   * `ENDPOINT_PROJECT_ID`：部署開放式模型的專案。
   * `ENDPOINT_ID`：開放模型使用的 HTTPS 端點 ID。如要取得端點 ID，請在「線上預測」頁面中找到已開啟的模型，然後複製「ID」欄位中的值。

## 生成文字嵌入

使用資料表欄或查詢中的文字資料，透過 [`AI.GENERATE_EMBEDDING` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-ai-generate-embedding?hl=zh-tw)生成文字嵌入。

一般來說，您會針對僅限文字的應用情境使用文字嵌入模型，並針對跨模式搜尋應用情境使用多模態嵌入模型，在相同的語意空間中生成文字和視覺內容的嵌入項目。

### Vertex AI Text

透過 Vertex AI 文字嵌入模型，使用遠端模型生成文字嵌入：

```
SELECT *
FROM AI.GENERATE_EMBEDDING(
  MODEL `PROJECT_ID.DATASET_ID.MODEL_NAME`,
  {TABLE PROJECT_ID.DATASET_ID.TABLE_NAME | (CONTENT_QUERY)},
  STRUCT(TASK_TYPE AS task_type,
    OUTPUT_DIMENSIONALITY AS output_dimensionality)
);
```

請替換下列項目：

* `PROJECT_ID`：您的專案 ID。
* `DATASET_ID`：包含模型的資料集 ID。
* `MODEL_NAME`：嵌入模型上的遠端模型名稱。
* `TABLE_NAME`：包含要嵌入文字的資料表名稱。這個資料表必須有名為 `content` 的資料欄，您也可以使用別名來使用名稱不同的資料欄。
* `CONTENT_QUERY`：查詢，結果包含名為 `content` 的 `STRING` 資料欄。
* `TASK_TYPE`：`STRING` 常值，用於指定預期的下游應用程式，協助模型產生品質較佳的嵌入。`TASK_TYPE`
  接受下列值：
  + `RETRIEVAL_QUERY`：指定給定文字是搜尋或擷取設定中的查詢。
  + `RETRIEVAL_DOCUMENT`：指定給定文字是搜尋或擷取設定中的文件。

    使用這類工作時，建議在查詢陳述式中加入文件標題，以提升嵌入品質。文件標題必須位於名為 `title` 或別名為 `title` 的資料欄中，例如：

    ```
          SELECT *
          FROM
            AI.GENERATE_EMBEDDING(
              MODEL mydataset.embedding_model,
              (SELECT abstract as content, header as title, publication_number
              FROM mydataset.publications),
              STRUCT('RETRIEVAL_DOCUMENT' as task_type)
          );
    ```

    在輸入查詢中指定標題資料欄，即可填入傳送至模型的要求主體中的 [`title` 欄位](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/model-reference/text-embeddings-api?hl=zh-tw#request_body)。如果使用任何其他工作類型時指定 `title` 值，系統會忽略該輸入內容，且不會對嵌入結果造成影響。
  + `SEMANTIC_SIMILARITY`：指定給定文字將用於語意文字相似度 (STS)。
  + `CLASSIFICATION`：指定嵌入內容將用於分類。
  + `CLUSTERING`：指定要將嵌入內容用於叢集。
  + `QUESTION_ANSWERING`：指定嵌入內容將用於問答。
  + `FACT_VERIFICATION`：指定嵌入內容將用於事實查證。
  + `CODE_RETRIEVAL_QUERY`：指定嵌入內容將用於程式碼擷取。
* `OUTPUT_DIMENSIONALITY`：`INT64` 值，指定產生嵌入時要使用的維度數量。舉例來說，如果您指定 `256 AS
  output_dimensionality`，則 `embedding` 輸出資料欄會包含每個輸入值的 256 維度嵌入。

  如果是透過 `gemini-embedding-2-preview` 或 `gemini-embedding-001` 模型執行的遠端模型，`OUTPUT_DIMENSIONALITY` 值必須在 `[1, 3072]` 範圍內。預設值為 `3072`。如果是透過 `text-embedding` 模型執行的遠端模型，`OUTPUT_DIMENSIONALITY` 值必須介於 `[1, 768]` 之間。預設值為 `768`。

**範例：在表格中嵌入文字**

以下範例顯示如何要求嵌入 `text_data` 資料表的 `content` 欄：

```
SELECT *
FROM
  AI.GENERATE_EMBEDDING(
    MODEL `mydataset.embedding_model`,
    TABLE mydataset.text_data,
    STRUCT('CLASSIFICATION' AS task_type)
  );
```

### 開放式文字

**預覽**

這項產品或功能適用《[服務專屬條款](https://docs.cloud.google.com/terms/service-terms?hl=zh-tw#1)》中「一般服務條款」一節的《正式發布前產品條款》。正式發布前的產品和功能是按照「原樣」提供，支援範圍可能有限。
詳情請參閱[推出階段說明](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages)。

注意：如要提供意見回饋或尋求這項功能支援，請傳送電子郵件至 [bqml-feedback@google.com](mailto:bqml-feedback@google.com)。

透過開放式嵌入模型，使用遠端模型生成文字嵌入：

```
SELECT *
FROM AI.GENERATE_EMBEDDING(
  MODEL `PROJECT_ID.DATASET_ID.MODEL_NAME`,
  {TABLE PROJECT_ID.DATASET_ID.TABLE_NAME | (CONTENT_QUERY)},
);
```

請替換下列項目：

* `PROJECT_ID`：您的專案 ID。
* `DATASET_ID`：包含模型的資料集 ID。
* `MODEL_NAME`：嵌入模型上的遠端模型名稱。
* `TABLE_NAME`：包含要嵌入文字的資料表名稱。這個資料表必須有名為 `content` 的資料欄，您也可以使用別名來使用名稱不同的資料欄。
* `CONTENT_QUERY`：查詢，結果包含名為 `content` 的 `STRING` 資料欄。

### Vertex AI 多模態

透過 Vertex AI 多模態嵌入模型，使用遠端模型生成文字嵌入：

```
SELECT *
FROM AI.GENERATE_EMBEDDING(
  MODEL `PROJECT_ID.DATASET_ID.MODEL_NAME`,
  {TABLE PROJECT_ID.DATASET_ID.TABLE_NAME | (CONTENT_QUERY)},
  STRUCT(OUTPUT_DIMENSIONALITY AS output_dimensionality)
);
```

請替換下列項目：

* `PROJECT_ID`：您的專案 ID。
* `DATASET_ID`：包含模型的資料集 ID。
* `MODEL_NAME`：遠端模型名稱，透過 `multimodalembedding@001` 模型。
* `TABLE_NAME`：包含要嵌入文字的資料表名稱。這個資料表必須有名為 `content` 的資料欄，您也可以使用別名來使用名稱不同的資料欄。
* `CONTENT_QUERY`：查詢，結果包含名為 `content` 的 `STRING` 資料欄。
* `OUTPUT_DIMENSIONALITY`：`INT64` 值，指定產生嵌入時要使用的維度數量。有效值為 `128`、`256`、`512` 和 `1408`。預設值為 `1408`。舉例來說，如果您指定 `256 AS output_dimensionality`，則輸出資料欄會包含每個輸入值的 256 維度嵌入。`embedding`

**範例：使用嵌入功能依語意相似度排序**

以下範例會嵌入一系列電影評論，並使用 [`VECTOR_SEARCH` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/search_functions?hl=zh-tw#vector_search)，依據與「這部電影很普通」評論的餘弦距離排序。距離越小，表示語意相似度越高。

如要進一步瞭解向量搜尋和向量索引，請參閱「[向量搜尋簡介](https://docs.cloud.google.com/bigquery/docs/vector-search-intro?hl=zh-tw)」。

```
CREATE TEMPORARY TABLE movie_review_embeddings AS (
  SELECT *
  FROM
    AI.GENERATE_EMBEDDING(
      MODEL `bqml_tutorial.embedding_model`,
      (
        SELECT "This movie was fantastic" AS content
        UNION ALL
        SELECT "This was the best movie I've ever seen!!" AS content
        UNION ALL
        SELECT "This movie was just okay..." AS content
        UNION ALL
        SELECT "This movie was terrible." AS content
      )
    )
);

WITH average_review_embedding AS (
  SELECT embedding
  FROM
    AI.GENERATE_EMBEDDING(
      MODEL `bqml_tutorial.embedding_model`,
      (SELECT "This movie was average" AS content)
    )
)
SELECT
  base.content AS content,
  distance AS distance_to_average_review
FROM
  VECTOR_SEARCH(
    TABLE movie_review_embeddings,
    "embedding",
    (SELECT embedding FROM average_review_embedding),
    distance_type=>"COSINE",
    top_k=>-1
  )
ORDER BY distance_to_average_review;
```

結果大致如下：

```
+------------------------------------------+----------------------------+
| content                                  | distance_to_average_review |
+------------------------------------------+----------------------------+
| This movie was just okay...              | 0.062789813467745592       |
| This movie was fantastic                 |  0.18579561313064263       |
| This movie was terrible.                 |  0.35707466240930985       |
| This was the best movie I've ever seen!! |  0.41844932504542975       |
+------------------------------------------+----------------------------+
```

## 後續步驟

* 瞭解如何[使用文字和圖像嵌入執行文字轉圖像的語意搜尋](https://docs.cloud.google.com/bigquery/docs/generate-multimodal-embeddings?hl=zh-tw)。
* 瞭解如何[使用文字嵌入執行語意搜尋和檢索增強生成 (RAG)](https://docs.cloud.google.com/bigquery/docs/vector-index-text-search-tutorial?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-16 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-16 (世界標準時間)。"],[],[]]