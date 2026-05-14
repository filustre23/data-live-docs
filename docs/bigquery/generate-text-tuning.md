Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 使用資料調整模型

本文說明如何建立參照 Vertex AI 模型的 BigQuery ML [遠端模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model-tuned?hl=zh-tw)，然後設定模型以執行監督式微調。Vertex AI 模型必須是下列其中一項：

* `gemini-2.5-pro`
* `gemini-2.5-flash-lite`
* `gemini-2.0-flash-001`
* `gemini-2.0-flash-lite-001`

建立遠端模型後，請使用 [`ML.EVALUATE` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-evaluate?hl=zh-tw)評估模型，並確認模型效能是否符合您的用途。接著，您可以使用模型和 [`AI.GENERATE_TEXT` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-ai-generate-text?hl=zh-tw)，分析 BigQuery 資料表中的文字。

詳情請參閱「[Vertex AI Gemini API 模型監督式微調](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/models/tune-gemini-overview?hl=zh-tw)」。

## 必要的角色

如要建立及評估微調模型，您需要下列 Identity and Access Management (IAM) 角色：

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

您或許還可透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)取得這些權限。

## 事前準備

1. 在 Google Cloud 控制台的專案選擇器頁面中，選取或建立 Google Cloud 專案。

   **選取或建立專案所需的角色**

   * **選取專案**：選取專案時，不需要具備特定 IAM 角色，只要您已獲授角色，即可選取任何專案。
   * **建立專案**：如要建立專案，您需要「專案建立者」角色 (`roles/resourcemanager.projectCreator`)，其中包含 `resourcemanager.projects.create` 權限。[瞭解如何授予角色](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)。
   **注意**：如果您不打算保留在這項程序中建立的資源，請建立新專案，而不要選取現有專案。完成這些步驟後，您就可以刪除專案，並移除與該專案相關聯的所有資源。

   [前往專案選取器](https://console.cloud.google.com/projectselector2/home/dashboard?hl=zh-tw)
2. [確認專案已啟用計費功能 Google Cloud](https://docs.cloud.google.com/billing/docs/how-to/verify-billing-enabled?hl=zh-tw#confirm_billing_is_enabled_on_a_project) 。
3. 啟用 BigQuery、BigQuery Connection、Vertex AI 和 Compute Engine API。

   **啟用 API 時所需的角色**

   如要啟用 API，您需要服務使用情形管理員 IAM 角色 (`roles/serviceusage.serviceUsageAdmin`)，其中包含 `serviceusage.services.enable` 權限。[瞭解如何授予角色](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)。

   [啟用 API](https://console.cloud.google.com/flows/enableapi?apiid=bigquery.googleapis.com%2Cbigqueryconnection.googleapis.com%2Caiplatform.googleapis.com%2Ccompute.googleapis.com&hl=zh-tw)

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

### 授予連線的服務帳戶存取權

為連線的服務帳戶授予 Vertex AI 服務代理人角色。

如果您打算在建立遠端模型時將端點指定為網址 (例如 `endpoint = 'https://us-central1-aiplatform.googleapis.com/v1/projects/myproject/locations/us-central1/publishers/google/models/gemini-2.0-flash'`)，請在網址指定的專案中授予這個角色。

如果您打算在建立遠端模型時使用模型名稱指定端點 (例如 `endpoint = 'gemini-2.0-flash'`)，請在您打算建立遠端模型的專案中授予這個角色。

在其他專案中授予角色會導致錯誤 `bqcx-1234567890-wxyz@gcp-sa-bigquery-condel.iam.gserviceaccount.com does not have the permission to access resource`。

如要授予角色，請按照下列步驟操作：

### 控制台

1. 前往「IAM & Admin」(IAM 與管理) 頁面。

   [前往「IAM & Admin」(IAM 與管理)](https://console.cloud.google.com/project/_/iam-admin?hl=zh-tw)
2. 按一下 person\_add「授予存取權」。
3. 在「新增主體」中，輸入先前複製的服務帳戶 ID。
4. 按一下「選擇角色」。
5. 在「篩選器」中輸入 `Vertex AI Service Agent`，然後選取該角色。
6. 按一下 [儲存]。

### gcloud

使用 [`gcloud projects add-iam-policy-binding`](https://docs.cloud.google.com/sdk/gcloud/reference/projects/add-iam-policy-binding?hl=zh-tw) 指令：

```
gcloud projects add-iam-policy-binding 'PROJECT_NUMBER' --member='serviceAccount:MEMBER' --role='roles/aiplatform.serviceAgent' --condition=None
```

請替換下列項目：

* `PROJECT_NUMBER`：您的專案編號。
* `MEMBER`：您先前複製的服務帳戶 ID。

與連線相關聯的服務帳戶是「BigQuery 連線委派服務代理」的執行個體，因此可以指派服務代理角色。

## 建立經過監督式調整的模型

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中執行下列查詢，建立[遠端模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model-tuned?hl=zh-tw)：

   ```
   CREATE OR REPLACE MODEL
   `PROJECT_ID.DATASET_ID.MODEL_NAME`
   REMOTE WITH CONNECTION {DEFAULT | `PROJECT_ID.REGION.CONNECTION_ID`}
   OPTIONS (
     ENDPOINT = 'ENDPOINT',
     MAX_ITERATIONS = MAX_ITERATIONS,
     LEARNING_RATE_MULTIPLIER = LEARNING_RATE_MULTIPLIER,
     DATA_SPLIT_METHOD = 'DATA_SPLIT_METHOD',
     DATA_SPLIT_EVAL_FRACTION = DATA_SPLIT_EVAL_FRACTION,
     DATA_SPLIT_COL = 'DATA_SPLIT_COL',
     EVALUATION_TASK = 'EVALUATION_TASK',
     PROMPT_COL = 'INPUT_PROMPT_COL',
     INPUT_LABEL_COLS = INPUT_LABEL_COLS)
   AS SELECT PROMPT_COLUMN, LABEL_COLUMN
   FROM `TABLE_PROJECT_ID.TABLE_DATASET.TABLE_NAME`;
   ```

   請替換下列項目：

   * `PROJECT_ID`：要在其中建立模型的專案 ID。
   * `DATASET_ID`：要包含模型的資料集 ID。這個資料集必須位於[支援的 Vertex AI 區域](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/learn/locations?hl=zh-tw)。
   * `MODEL_NAME`：模型名稱。
   * `REGION`：連線使用的區域。
   * `CONNECTION_ID`：BigQuery 連線的 ID。這個連線必須與您使用的資料集位於相同的[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)。

     在 Google Cloud 控制台中[查看連線詳細資料](https://docs.cloud.google.com/bigquery/docs/working-with-connections?hl=zh-tw#view-connections)時，這是顯示在「連線 ID」中的完整連線 ID 最後一個部分的值，例如 `projects/myproject/locations/connection_location/connections/myconnection`。
   * `ENDPOINT`：`STRING` 值，指定要使用的模型名稱。
   * `MAX_ITERATIONS`：`INT64` 值，指定要執行的監督式微調步驟數。`MAX_ITERATIONS` 值必須介於 `1` 至 `∞` 之間。

     Gemini 模型會使用「週期」而非「步驟」訓練，因此 BigQuery ML 會將 `MAX_ITERATIONS` 值轉換為週期。`MAX_ITERATIONS` 的預設值是輸入資料中的列數，相當於一個訓練週期。如要使用多個訓練週期，請指定訓練資料中的資料列數倍數。舉例來說，如果您有 100 列輸入資料，並想使用兩個訓練週期，請為引數值指定 `200`。如果您提供的值不是輸入資料列數的倍數，BigQuery ML 會無條件進位至最接近的訓練週期。舉例來說，如果您有 100 列輸入資料，並為 `MAX_ITERATIONS` 值指定 `101`，則訓練會執行兩個訓練週期。

     如要進一步瞭解用於調整 Gemini 模型的參數，請參閱「[建立調整作業](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/models/gemini-use-supervised-tuning?hl=zh-tw#create_a_text_model_supervised_tuning_job)」。
   * `DATA_SPLIT_METHOD`：`STRING` 值，指定將輸入資料拆分成訓練集和評估集的方法。有效選項如下：
     + `AUTO_SPLIT`：BigQuery ML 會自動分割資料。資料的分割方式取決於輸入表格中的列數。這是預設值。
     + `RANDOM`：資料會先隨機化，再分成多個集合。如要自訂資料分割，可以搭配 `DATA_SPLIT_EVAL_FRACTION` 選項使用這個選項。
     + `CUSTOM`：使用 `DATA_SPLIT_COL` 選項中提供的資料欄分割資料。`DATA_SPLIT_COL` 值必須是 `BOOL` 類型資料欄的名稱。含有 `TRUE` 或 `NULL` 值的資料列會做為評估資料使用，含有 `FALSE` 值的資料列則做為訓練資料使用。
     + `SEQ`：使用 `DATA_SPLIT_COL` 選項中提供的資料欄分割資料。`DATA_SPLIT_COL` 值必須是下列其中一種類型的資料欄名稱：
       - `NUMERIC`
       - `BIGNUMERIC`
       - `STRING`
       - `TIMESTAMP`

       系統會根據指定資料欄，由小到大排序資料。

       前 *n* 列會做為評估資料使用，其中 *n* 是 `DATA_SPLIT_EVAL_FRACTION` 的指定值。其餘資料列則做為訓練資料使用。
     + `NO_SPLIT`：不分割資料，所有輸入資料都會做為訓練資料。

     如要進一步瞭解這些資料分割選項，請參閱 [`DATA_SPLIT_METHOD`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model-tuned?hl=zh-tw#data_split_method)。
   * `DATA_SPLIT_EVAL_FRACTION`：一個 `FLOAT64` 值，指定執行監督式微調時，要將多少比例的資料做為評估資料。值必須介於 `[0, 1.0]`。預設值為 `0.2`。

     當您將 `RANDOM` 或 `SEQ` 指定為 `DATA_SPLIT_METHOD` 選項的值時，請使用這個選項。如要自訂資料分割，可以使用 `DATA_SPLIT_METHOD` 選項搭配 `DATA_SPLIT_EVAL_FRACTION` 選項。
   * `DATA_SPLIT_COL`：`STRING` 值，指定用於將輸入資料排序至訓練或評估集的資料欄名稱。指定 `CUSTOM` 或 `SEQ` 做為 `DATA_SPLIT_METHOD` 選項的值時，請使用 `CUSTOM`。
   * `EVALUATION_TASK`：`STRING` 值，指定要微調模型執行的工作類型。有效選項如下：
     + `TEXT_GENERATION`
     + `CLASSIFICATION`
     + `SUMMARIZATION`
     + `QUESTION_ANSWERING`
     + `UNSPECIFIED`

     預設值為 `UNSPECIFIED`。
   * `INPUT_PROMPT_COL`：`STRING` 值，其中包含執行監督式微調時要使用的訓練資料表中的提示資料欄名稱。預設值為 `prompt`。
   * `INPUT_LABEL_COLS`：`ARRAY<<STRING>` 值，其中包含訓練資料表中的標籤資料欄名稱，可用於監督式微調。陣列中只能指定一個元素。預設值為空陣列。這會導致 `label` 成為 `LABEL_COLUMN` 引數的預設值。
   * `PROMPT_COLUMN`：訓練資料表中的資料欄，內含用於評估 `LABEL_COLUMN` 資料欄內容的提示。這個資料欄必須是 `STRING` 類型，或轉換為 `STRING`。如果您為 `INPUT_PROMPT_COL` 選項指定值，則必須為 `PROMPT_COLUMN` 指定相同的值。否則，這個值必須是 `prompt`。如果資料表沒有 `prompt` 資料欄，請使用別名指定現有資料表資料欄。例如：`AS SELECT hint AS prompt, label FROM mydataset.mytable`。
   * `LABEL_COLUMN`：訓練資料表中的資料欄，內含用於訓練模型的範例。這個資料欄必須是 `STRING` 類型，或轉換為 `STRING`。如果您為 `INPUT_LABEL_COLS` 選項指定值，則必須為 `LABEL_COLUMN` 指定相同的值。否則，這個值必須是 `label`。如果資料表沒有 `label` 資料欄，請使用別名指定現有資料表資料欄。例如：`AS SELECT prompt, feature AS label FROM mydataset.mytable`。
   * `TABLE_PROJECT_ID`：包含訓練資料表的專案 ID。
   * `TABLE_DATASET`：包含訓練資料表的資料集名稱。
   * `TABLE_NAME`：包含用於訓練模型資料的資料表名稱。

## 評估微調後的模型

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中執行下列查詢，評估微調模型：

   ```
   SELECT
   *
   FROM
   ML.EVALUATE(
     MODEL `PROJECT_ID.DATASET_ID.MODEL_NAME`,
     TABLE `TABLE_PROJECT_ID.TABLE_DATASET.TABLE_NAME`,
     STRUCT('TASK_TYPE' AS task_type, TOKENS AS max_output_tokens,
       TEMPERATURE AS temperature, TOP_K AS top_k,
       TOP_P AS top_p));
   ```

   請替換下列項目：

   * `PROJECT_ID`：包含模型的專案 ID。
   * `DATASET_ID`：包含模型的資料集 ID。
   * `MODEL_NAME`：模型名稱。
   * `TABLE_PROJECT_ID`：包含評估資料表的專案 ID。
   * `TABLE_DATASET`：包含評估資料表的資料集名稱。
   * `TABLE_NAME`：包含評估資料的資料表名稱。

     資料表必須包含一個資料欄，其名稱與模型訓練期間提供的提示資料欄名稱相符。您可以在模型訓練期間使用 `prompt_col` 選項提供這個值。如未指定 `prompt_col`，系統會使用訓練資料中名為 `prompt` 的資料欄。如果沒有名為 `prompt` 的資料欄，系統會傳回錯誤。

     資料表必須有一個資料欄，其名稱與模型訓練期間提供的標籤資料欄名稱相符。您可以在模型訓練期間使用 `input_label_cols` 選項提供這個值。如果未指定 `input_label_cols`，系統會使用訓練資料中名為「label」的資料欄。`label`如果沒有名為 `label` 的資料欄，系統會傳回錯誤。
   * `TASK_TYPE`：`STRING` 值，指定要評估模型效能的任務類型。有效選項如下：
     + `TEXT_GENERATION`
     + `CLASSIFICATION`
     + `SUMMARIZATION`
     + `QUESTION_ANSWERING`
     + `UNSPECIFIED`
   * `TOKENS`：`INT64` 值，用於設定回覆中可生成的詞元數量上限。這個值必須介於 `[1,1024]` 的範圍之間。
     如要取得較短的回覆，請指定較低的值；如要取得較長的回覆，請調高此值。預設值為 `128`。
   * `TEMPERATURE`：介於 `[0.0,1.0]` 範圍內的 `FLOAT64` 值，可控制選取詞元時的隨機程度。預設值為 `0`。

     如果希望提示生成更具確定性、較不具開放性和創意性的回覆，建議調低 `temperature` 值。另一方面，如果 `temperature` 值較高，則可能產生較多元或有創意的結果。如果 `0` 為 `temperature`，則模型一律會選取可能性最高的回覆。
   * `TOP_K`：`INT64` 值，範圍為 `[1,40]`，可決定模型選取時考量的初始詞元集區。如要取得較不隨機的回覆，請指定較低的值；如要取得較隨機的回覆，請調高此值。預設值為 `40`。
   * `TOP_P`：`FLOAT64` 範圍 `[0.0,1.0]` 中的 `FLOAT64` 值，有助於判斷要從 `TOP_K` 決定的集區中選取哪些權杖。如要取得較不隨機的回覆，請指定較低的值；如要取得較隨機的回覆，請調高此值。預設值為 `0.95`。

## 生成文字

使用 [`AI.GENERATE_TEXT` 函式生成文字：](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-ai-generate-text?hl=zh-tw)

### 提示資料欄

使用資料表欄位提供提示，生成文字。

```
SELECT *
FROM AI.GENERATE_TEXT(
  MODEL `PROJECT_ID.DATASET_ID.MODEL_NAME`,
  TABLE PROJECT_ID.DATASET_ID.TABLE_NAME,
  STRUCT(TOKENS AS max_output_tokens, TEMPERATURE AS temperature,
  TOP_P AS top_p,
  STOP_SEQUENCES AS stop_sequences)
);
```

請替換下列項目：

* `PROJECT_ID`：您的專案 ID。
* `DATASET_ID`：包含模型的資料集 ID。
* `MODEL_NAME`：模型名稱。
* `TABLE_NAME`：包含提示的資料表名稱。這個資料表必須有一個資料欄，名稱與微調模型中的特徵欄名稱相符。建立模型時，可以使用 `PROMPT_COL` 選項設定模型中的特徵資料欄名稱。否則，模型中的特徵欄名稱預設為 `prompt`，您也可以使用別名來使用名稱不同的資料欄。
* `TOKENS`：`INT64` 值，用於設定回覆中可生成的詞元數量上限。
  這個值必須介於 `[1,8192]` 的範圍之間。
  如要取得較短的回覆，請指定較低的值；如要取得較長的回覆，請調高此值。預設值為 `128`。
* `TEMPERATURE`：
  介於 `[0.0,1.0]` 之間的 `FLOAT64` 值，
  可控制選取詞元時的隨機程度。
  預設值為 `0`。

  如果希望提示生成更具確定性、較不具開放性和創意性的回覆，建議調低 `temperature` 值。另一方面，如果 `temperature` 值較高，則可能產生較多元或有創意的結果。如果 `0` 為 `temperature`，則模型一律會選取可能性最高的回覆。
* `TOP_P`：`[0.0,1.0]` 範圍內的 `FLOAT64` 值有助於判斷所選符記的機率。如要取得較不隨機的回覆，請指定較低的值；如要取得較隨機的回覆，請調高此值。預設值為 `0.95`。
* `STOP_SEQUENCES`：`ARRAY<STRING>` 值，可移除模型回應中包含的指定字串。字串必須完全相符，包括大小寫。預設值為空陣列。
* `GROUND_WITH_GOOGLE_SEARCH`：決定 Vertex AI 模型在生成回覆時是否要使用[以 Google 搜尋強化事實基礎](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/grounding/overview?hl=zh-tw#ground-public)的 `BOOL` 值。建立基準後，模型就能在生成回覆時使用網路上其他資訊，讓回覆內容更具體且符合事實。如果將這個欄位設為 `True`，結果中會包含額外的 `grounding_result` 欄，提供模型用來收集額外資訊的來源。預設值為 `FALSE`。
* `SAFETY_SETTINGS`：`ARRAY<STRUCT<STRING AS category, STRING AS threshold>>` 值，可設定內容安全門檻來篩選回應。結構體中的第一個元素會指定有害類別，第二個元素則會指定對應的封鎖門檻。模型會篩除違反這些設定的內容。每個類別只能指定一次。舉例來說，您無法同時指定 `STRUCT('HARM_CATEGORY_DANGEROUS_CONTENT' AS category, 'BLOCK_MEDIUM_AND_ABOVE' AS threshold)` 和 `STRUCT('HARM_CATEGORY_DANGEROUS_CONTENT' AS category, 'BLOCK_ONLY_HIGH' AS threshold)`。如果特定類別沒有安全設定，系統會使用 `BLOCK_MEDIUM_AND_ABOVE` 安全設定。

  支援的類別如下：

  + `HARM_CATEGORY_HATE_SPEECH`
  + `HARM_CATEGORY_DANGEROUS_CONTENT`
  + `HARM_CATEGORY_HARASSMENT`
  + `HARM_CATEGORY_SEXUALLY_EXPLICIT`

  支援的門檻如下：

  + `BLOCK_NONE` ([受限](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/multimodal/configure-safety-attributes?hl=zh-tw#how_to_remove_automated_response_blocking_for_select_safety_attributes))
  + `BLOCK_LOW_AND_ABOVE`
  + `BLOCK_MEDIUM_AND_ABOVE` (預設)
  + `BLOCK_ONLY_HIGH`
  + `HARM_BLOCK_THRESHOLD_UNSPECIFIED`

  詳情請參閱[安全類別](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/multimodal/configure-safety-attributes?hl=zh-tw#safety_attribute_scoring)和[封鎖門檻](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/multimodal/configure-safety-attributes?hl=zh-tw#safety-settings)的定義。
* `REQUEST_TYPE`：`STRING` 值，指定要傳送至 Gemini 模型的推論要求類型。要求類型會決定要求使用的配額。有效值如下：
  + `DEDICATED`：`AI.GENERATE_TEXT` 函式只會使用佈建輸送量配額。如果沒有可用的佈建輸送量配額，`AI.GENERATE_TEXT` 函式會傳回 `Provisioned throughput is not purchased or is not
    active` 錯誤。
  + `SHARED`：即使您已購買佈建輸送量配額，`AI.GENERATE_TEXT` 函式也只會使用[動態共用配額 (DSQ)](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/dynamic-shared-quota?hl=zh-tw)。
  + `UNSPECIFIED`：`AI.GENERATE_TEXT` 函式會依下列方式使用配額：
    - 如未購買佈建輸送量配額，`AI.GENERATE_TEXT` 函式會使用 DSQ 配額。
    - 如果您已購買佈建輸送量配額，`AI.GENERATE_TEXT` 函式會優先使用該配額。如果要求超出佈建輸送量配額，溢出的流量會使用 DSQ 配額。

  預設值為 `UNSPECIFIED`。

  詳情請參閱「[使用 Vertex AI 佈建輸送量](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-generate-text?hl=zh-tw#provisioned-throughput)」。
* `MODEL_PARAMS`：JSON 格式的字串常值，可為模型提供參數。這個值必須符合[`generateContent` 要求內容](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/reference/rest/v1/projects.locations.endpoints/generateContent?hl=zh-tw)格式。您可以為要求主體中的任何欄位提供值，但 `contents[]` 欄位除外。如果您設定這個欄位，就無法在 `AI.GENERATE_TEXT` 函式的頂層結構體引數中指定任何模型參數。您必須在 `MODEL_PARAMS` 欄位中指定每個模型參數，或是省略這個欄位並分別指定每個參數。

以下範例顯示具有這些特徵的要求：

* 使用 `prompts` 資料表的 `prompt` 資料欄做為提示。
* 傳回簡短且中等可能性的回覆。
* 並在不同資料欄中傳回生成的文字和安全屬性。

```
SELECT *
FROM
  AI.GENERATE_TEXT(
    MODEL `mydataset.mymodel`,
    TABLE mydataset.prompts,
    STRUCT(
      0.4 AS temperature, 100 AS max_output_tokens, 0.5 AS top_p));
```

### 提示詞查詢

使用查詢提供提示，生成文字。

```
SELECT *
FROM AI.GENERATE_TEXT(
  MODEL `PROJECT_ID.DATASET_ID.MODEL_NAME`,
  (PROMPT_QUERY),
  STRUCT(TOKENS AS max_output_tokens, TEMPERATURE AS temperature,
  TOP_P AS top_p,
  STOP_SEQUENCES AS stop_sequences)
);
```

請替換下列項目：

* `PROJECT_ID`：您的專案 ID。
* `DATASET_ID`：包含模型的資料集 ID。
* `MODEL_NAME`：模型名稱。
* `PROMPT_QUERY`：提供提示資料的查詢。
* `TOKENS`：`INT64` 值，用於設定回覆中可生成的詞元數量上限。
  這個值必須介於 `[1,8192]` 的範圍之間。
  如要取得較短的回覆，請指定較低的值；如要取得較長的回覆，請調高此值。預設值為 `128`。
* `TEMPERATURE`：
  介於 `[0.0,1.0]` 之間的 `FLOAT64` 值，
  可控制選取詞元時的隨機程度。
  預設值為 `0`。

  如果希望提示生成更具確定性、較不具開放性和創意性的回覆，建議調低 `temperature` 值。另一方面，如果 `temperature` 值較高，則可能產生較多元或有創意的結果。如果 `0` 為 `temperature`，則模型一律會選取可能性最高的回覆。
* `TOP_P`：`[0.0,1.0]` 範圍內的 `FLOAT64` 值有助於判斷所選符記的機率。如要取得較不隨機的回覆，請指定較低的值；如要取得較隨機的回覆，請調高此值。預設值為 `0.95`。
* `STOP_SEQUENCES`：`ARRAY<STRING>` 值，可移除模型回應中包含的指定字串。字串必須完全相符，包括大小寫。預設值為空陣列。
* `GROUND_WITH_GOOGLE_SEARCH`：決定 Vertex AI 模型在生成回覆時是否要使用[以 Google 搜尋強化事實基礎](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/grounding/overview?hl=zh-tw#ground-public)的 `BOOL` 值。建立基準後，模型就能在生成回覆時使用網路上其他資訊，讓回覆內容更具體且符合事實。如果將這個欄位設為 `True`，結果中會包含額外的 `grounding_result` 欄，提供模型用來收集額外資訊的來源。預設值為 `FALSE`。
* `SAFETY_SETTINGS`：`ARRAY<STRUCT<STRING AS category, STRING AS threshold>>` 值，可設定內容安全門檻來篩選回應。結構體中的第一個元素會指定有害類別，第二個元素則會指定對應的封鎖門檻。模型會篩除違反這些設定的內容。每個類別只能指定一次。舉例來說，您無法同時指定 `STRUCT('HARM_CATEGORY_DANGEROUS_CONTENT' AS category, 'BLOCK_MEDIUM_AND_ABOVE' AS threshold)` 和 `STRUCT('HARM_CATEGORY_DANGEROUS_CONTENT' AS category, 'BLOCK_ONLY_HIGH' AS threshold)`。如果特定類別沒有安全設定，系統會使用 `BLOCK_MEDIUM_AND_ABOVE` 安全設定。

  支援的類別如下：

  + `HARM_CATEGORY_HATE_SPEECH`
  + `HARM_CATEGORY_DANGEROUS_CONTENT`
  + `HARM_CATEGORY_HARASSMENT`
  + `HARM_CATEGORY_SEXUALLY_EXPLICIT`

  支援的門檻如下：

  + `BLOCK_NONE` ([受限](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/multimodal/configure-safety-attributes?hl=zh-tw#how_to_remove_automated_response_blocking_for_select_safety_attributes))
  + `BLOCK_LOW_AND_ABOVE`
  + `BLOCK_MEDIUM_AND_ABOVE` (預設)
  + `BLOCK_ONLY_HIGH`
  + `HARM_BLOCK_THRESHOLD_UNSPECIFIED`

  詳情請參閱[安全類別](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/multimodal/configure-safety-attributes?hl=zh-tw#safety_attribute_scoring)和[封鎖門檻](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/multimodal/configure-safety-attributes?hl=zh-tw#safety-settings)的定義。
* `REQUEST_TYPE`：`STRING` 值，指定要傳送至 Gemini 模型的推論要求類型。要求類型會決定要求使用的配額。有效值如下：
  + `DEDICATED`：`AI.GENERATE_TEXT` 函式只會使用佈建輸送量配額。如果沒有可用的佈建輸送量配額，`AI.GENERATE_TEXT` 函式會傳回 `Provisioned throughput is not purchased or is not
    active` 錯誤。
  + `SHARED`：即使您已購買佈建輸送量配額，`AI.GENERATE_TEXT` 函式也只會使用[動態共用配額 (DSQ)](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/dynamic-shared-quota?hl=zh-tw)。
  + `UNSPECIFIED`：`AI.GENERATE_TEXT` 函式會依下列方式使用配額：
    - 如未購買佈建輸送量配額，`AI.GENERATE_TEXT` 函式會使用 DSQ 配額。
    - 如果您已購買佈建輸送量配額，`AI.GENERATE_TEXT` 函式會優先使用該配額。如果要求超出佈建輸送量配額，溢出的流量會使用 DSQ 配額。

  預設值為 `UNSPECIFIED`。

  詳情請參閱「[使用 Vertex AI 佈建輸送量](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-generate-text?hl=zh-tw#provisioned-throughput)」。
* `MODEL_PARAMS`：JSON 格式的字串常值，可為模型提供參數。這個值必須符合[`generateContent` 要求內容](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/reference/rest/v1/projects.locations.endpoints/generateContent?hl=zh-tw)格式。您可以為要求主體中的任何欄位提供值，但 `contents[]` 欄位除外。如果您設定這個欄位，就無法在 `AI.GENERATE_TEXT` 函式的頂層結構體引數中指定任何模型參數。您必須在 `MODEL_PARAMS` 欄位中指定每個模型參數，或是省略這個欄位並分別指定每個參數。

**範例 1**

以下範例顯示具有這些特徵的要求：

* 提示：要求提供 `articles` 表格中 `body` 欄的文字摘要。
* 傳回中等長度且較有可能的回覆。
* 並在不同資料欄中傳回生成的文字和安全屬性。

```
SELECT *
FROM
  AI.GENERATE_TEXT(
    MODEL `mydataset.mymodel`,
    (
      SELECT CONCAT('Summarize this text', body) AS prompt
      FROM mydataset.articles
    ),
    STRUCT(
      0.2 AS temperature, 650 AS max_output_tokens, 0.2 AS top_p));
```

**示例 2**

以下範例顯示具有這些特徵的要求：

* 使用查詢串連字串，提供含有資料表欄的提示[前置字元](https://docs.cloud.google.com/vertex-ai/docs/generative-ai/text/text-prompts?hl=zh-tw#prompt_structure)，藉此建立提示資料。
* 傳回簡短且中等可能性的回覆。
* 不會在個別資料欄中傳回生成的文字和安全屬性。

```
SELECT *
FROM
  AI.GENERATE_TEXT(
    MODEL `mydataset.mytuned_model`,
    (
      SELECT CONCAT(question, 'Text:', description, 'Category') AS prompt
      FROM mydataset.input_table
    ),
    STRUCT(
      0.4 AS temperature, 100 AS max_output_tokens, 0.5 AS top_p));
```




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-14 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-14 (世界標準時間)。"],[],[]]