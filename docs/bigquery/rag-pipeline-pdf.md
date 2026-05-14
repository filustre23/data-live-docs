Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 在檢索增強生成管道中剖析 PDF

本教學課程會逐步引導您建立檢索增強生成 (RAG) 管道，並以剖析的 PDF 內容為基礎。

由於 PDF 檔案 (例如財務文件) 結構複雜，且包含文字、圖表和表格，因此難以在 RAG 管道中使用。本教學課程說明如何搭配使用 BigQuery ML 功能和 Document AI 的版面配置剖析器，根據從 PDF 檔案擷取的關鍵資訊，建構 RAG 管道。

您也可以使用 [Colab Enterprise 筆記本](https://github.com/GoogleCloudPlatform/generative-ai/blob/main/gemini/use-cases/retrieval-augmented-generation/rag_with_bigquery.ipynb)執行本教學課程。

## 目標

本教學課程涵蓋下列工作：

* 建立 Cloud Storage bucket 並上傳範例 PDF 檔案。
* 建立[雲端資源連結](https://docs.cloud.google.com/bigquery/docs/create-cloud-resource-connection?hl=zh-tw)，以便從 BigQuery 連線至 Cloud Storage 和 Vertex AI。
* 在 PDF 檔案上建立[物件資料表](https://docs.cloud.google.com/bigquery/docs/object-table-introduction?hl=zh-tw)，讓 PDF 檔案可在 BigQuery 中使用。
* [建立 Document AI 處理器](https://docs.cloud.google.com/document-ai/docs/create-processor?hl=zh-tw#create-processor)，用於剖析 PDF 檔案。
* 建立[遠端模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model-service?hl=zh-tw)，讓您透過 BigQuery 使用 Document AI API 存取文件處理器。
* 使用 [`ML.PROCESS_DOCUMENT` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-process-document?hl=zh-tw)搭配遠端模型，將 PDF 內容剖析為區塊，然後將該內容寫入 BigQuery 資料表。
* 從 `ML.PROCESS_DOCUMENT` 函式傳回的 JSON 資料中擷取 PDF 內容，然後將該內容寫入 BigQuery 資料表。
* 建立[遠端模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model?hl=zh-tw)，以便從 BigQuery 使用 Vertex AI `text-embedding-004` 嵌入生成模型。
* 使用遠端模型和 [`AI.GENERATE_EMBEDDING` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-ai-generate-embedding?hl=zh-tw)，從剖析的 PDF 內容生成嵌入，然後將這些嵌入寫入 BigQuery 資料表。嵌入是 PDF 內容的數值表示法，可讓您對 PDF 內容執行語意搜尋和擷取。
* 使用嵌入的 [`VECTOR_SEARCH` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/search_functions?hl=zh-tw#vector_search)，找出語意相似的 PDF 內容。
* 建立[遠端模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model?hl=zh-tw)，以便從 BigQuery 使用 Gemini 文字生成模型。
* 使用 [`AI.GENERATE_TEXT` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-ai-generate-text?hl=zh-tw)，透過遠端模型執行檢索增強生成 (RAG)，生成文字、使用向量搜尋結果來增強提示輸入內容，並提升結果品質。

## 費用

在本文件中，您會使用下列 Google Cloud的計費元件：

* **BigQuery**: You incur costs for the data that you
  process in BigQuery.
* **Vertex AI**: You incur costs for calls to
  Vertex AI models.
* **Document AI**: You incur costs for calls to the
  Document AI API.
* **Cloud Storage**: You incur costs for object storage in
  Cloud Storage.

如要根據預測用量估算費用，請使用 [Pricing Calculator](https://docs.cloud.google.com/products/calculator?hl=zh-tw)。

初次使用 Google Cloud 的使用者可能符合[免費試用期](https://docs.cloud.google.com/free?hl=zh-tw)資格。

詳情請參閱下列定價頁面：

* [BigQuery 定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw)
* [Vertex AI 定價](https://cloud.google.com/vertex-ai/pricing?hl=zh-tw#generative_ai_models)
* [Document AI 定價](https://cloud.google.com/document-ai/pricing?hl=zh-tw)
* [Cloud Storage 定價](https://cloud.google.com/storage/pricing?hl=zh-tw)

## 事前準備

1. 在 Google Cloud 控制台的專案選擇器頁面中，選取或建立 Google Cloud 專案。

   **選取或建立專案所需的角色**

   * **選取專案**：選取專案時，不需要具備特定 IAM 角色，只要您已獲授角色，即可選取任何專案。
   * **建立專案**：如要建立專案，您需要「專案建立者」角色 (`roles/resourcemanager.projectCreator`)，其中包含 `resourcemanager.projects.create` 權限。[瞭解如何授予角色](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)。
   **注意**：如果您不打算保留在這項程序中建立的資源，請建立新專案，而不要選取現有專案。完成這些步驟後，您就可以刪除專案，並移除與該專案相關聯的所有資源。

   [前往專案選取器](https://console.cloud.google.com/projectselector2/home/dashboard?hl=zh-tw)
2. [確認專案已啟用計費功能 Google Cloud](https://docs.cloud.google.com/billing/docs/how-to/verify-billing-enabled?hl=zh-tw#confirm_billing_is_enabled_on_a_project) 。
3. 啟用 BigQuery、BigQuery Connection、Vertex AI、Document AI 和 Cloud Storage API。

   **啟用 API 時所需的角色**

   如要啟用 API，您需要服務使用情形管理員 IAM 角色 (`roles/serviceusage.serviceUsageAdmin`)，其中包含 `serviceusage.services.enable` 權限。[瞭解如何授予角色](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)。

   [啟用 API](https://console.cloud.google.com/flows/enableapi?apiid=bigquery.googleapis.com%2Cbigqueryconnection.googleapis.com%2Caiplatform.googleapis.com%2Cdocumentai.googleapis.com%2Cstorage.googleapis.com&hl=zh-tw)

## 必要的角色

如要執行本教學課程，您需要下列 Identity and Access Management (IAM) 角色：

* 建立 Cloud Storage bucket 和物件：Storage 管理員 (`roles/storage.storageAdmin`)
* 建立文件處理器：Document AI 編輯者 (`roles/documentai.editor`)
* 建立及使用 BigQuery 資料集、連線和模型：
  BigQuery 管理員 (`roles/bigquery.admin`)
* 將權限授予連線的服務帳戶：專案 IAM 管理員 (`roles/resourcemanager.projectIamAdmin`)

這些預先定義的角色具備執行本文所述工作所需的權限。如要查看確切的必要權限，請展開「Required permissions」(必要權限) 部分：

#### 所需權限

* 建立資料集：`bigquery.datasets.create`
* 建立、委派及使用連線：
  `bigquery.connections.*`
* 設定預設連線：`bigquery.config.*`
* 設定服務帳戶權限：
  `resourcemanager.projects.getIamPolicy` 和
  `resourcemanager.projects.setIamPolicy`
* 建立物件資料表：
  `bigquery.tables.create` 和
  `bigquery.tables.update`
* 建立 Cloud Storage bucket 和物件：
  `storage.buckets.*` 和
  `storage.objects.*`
* 建立模型並執行推論：
  + `bigquery.jobs.create`
  + `bigquery.models.create`
  + `bigquery.models.getData`
  + `bigquery.models.updateData`
  + `bigquery.models.updateMetadata`
* 建立文件處理器：
  + `documentai.processors.create`
  + `documentai.processors.update`
  + `documentai.processors.delete`

您或許還可透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-permissions?hl=zh-tw)取得這些權限。

## 建立資料集

建立 BigQuery 資料集來儲存機器學習模型。

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往 BigQuery 頁面](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在「Explorer」窗格中，按一下專案名稱。
3. 依序點按 more\_vert「View actions」(查看動作) >「Create dataset」(建立資料集)
4. 在「建立資料集」頁面中，執行下列操作：

   * 在「Dataset ID」(資料集 ID) 中輸入 `bqml_tutorial`。
   * 針對「位置類型」選取「多區域」，然後選取「美國」。
   * 其餘設定請保留預設狀態，然後按一下「建立資料集」。

### bq

如要建立新的資料集，請使用 [`bq mk --dataset` 指令](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#mk-dataset)。

1. 建立名為 `bqml_tutorial` 的資料集，並將資料位置設為 `US`。

   ```
   bq mk --dataset \
     --location=US \
     --description "BigQuery ML tutorial dataset." \
     bqml_tutorial
   ```
2. 確認資料集已建立完成：

   ```
   bq ls
   ```

### API

請呼叫 [`datasets.insert`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/datasets/insert?hl=zh-tw) 方法，搭配已定義的[資料集資源](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/datasets?hl=zh-tw)。

```
{
  "datasetReference": {
     "datasetId": "bqml_tutorial"
  }
}
```

## 建立連線

建立[Cloud 資源連線](https://docs.cloud.google.com/bigquery/docs/create-cloud-resource-connection?hl=zh-tw)，並取得連線的服務帳戶。在相同[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)建立連線。

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

## 將存取權授予服務帳戶

選取下列選項之一：

### 控制台

1. 前往「IAM & Admin」(IAM 與管理) 頁面。

   [前往「IAM & Admin」(IAM 與管理)](https://console.cloud.google.com/project/_/iam-admin?hl=zh-tw)
2. 按一下 person\_add「授予存取權」。

   「新增主體」對話方塊隨即開啟。
3. 在「新增主體」欄位，輸入先前複製的服務帳戶 ID。
4. 在「Select a role」(選取角色) 欄位中，依序選取「Document AI」和「Document AI Viewer」(Document AI 檢視者)。
5. 按一下 [Add another role] (新增其他角色)。
6. 在「Select a role」(請選擇角色) 欄位中，依序選取「Cloud Storage」和「Storage Object Viewer」(Storage 物件檢視者)。
7. 按一下 [Add another role] (新增其他角色)。
8. 在「選取角色」欄位中，選取「Vertex AI」，然後選取「Vertex AI 使用者」。
9. 按一下 [儲存]。

### gcloud

使用 [`gcloud projects add-iam-policy-binding`](https://docs.cloud.google.com/sdk/gcloud/reference/projects/add-iam-policy-binding?hl=zh-tw) 指令：

```
gcloud projects add-iam-policy-binding 'PROJECT_NUMBER' --member='serviceAccount:MEMBER' --role='roles/documentai.viewer' --condition=None
gcloud projects add-iam-policy-binding 'PROJECT_NUMBER' --member='serviceAccount:MEMBER' --role='roles/storage.objectViewer' --condition=None
gcloud projects add-iam-policy-binding 'PROJECT_NUMBER' --member='serviceAccount:MEMBER' --role='roles/aiplatform.user' --condition=None
```

請替換下列項目：

* `PROJECT_NUMBER`：您的專案編號。
* `MEMBER`：您先前複製的服務帳戶 ID。

## 將範例 PDF 上傳至 Cloud Storage

如要將範例 PDF 上傳至 Cloud Storage，請按照下列步驟操作：

1. 前往 <https://www.federalreserve.gov/publications/files/scf23.pdf>，然後按一下下載圖示 download，即可下載 `scf23.pdf` 範例 PDF。
2. [建立 Cloud Storage bucket](https://docs.cloud.google.com/storage/docs/creating-buckets?hl=zh-tw)。
3. [上傳](https://docs.cloud.google.com/storage/docs/uploading-objects?hl=zh-tw) `scf23.pdf` 檔案至 bucket。

## 建立物件資料表

在 Cloud Storage 中的 PDF 檔案上建立物件資料表：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中執行下列陳述式：

   ```
   CREATE OR REPLACE EXTERNAL TABLE `bqml_tutorial.pdf`
   WITH CONNECTION `LOCATION.CONNECTION_ID`
   OPTIONS(
     object_metadata = 'SIMPLE',
     uris = ['gs://BUCKET/scf23.pdf']);
   ```

   更改下列內容：

   * `LOCATION`：連線位置。
   * `CONNECTION_ID`：BigQuery 連線的 ID。

     在 Google Cloud 控制台中[查看連線詳細資料](https://docs.cloud.google.com/bigquery/docs/working-with-connections?hl=zh-tw#view-connections)時，`CONNECTION_ID` 是「連線 ID」中顯示的完整連線 ID 最後一個區段的值，例如 `projects/myproject/locations/connection_location/connections/myconnection`。
   * `BUCKET`：包含 `scf23.pdf` 檔案的 Cloud Storage bucket。完整的 `uri` 選項值應與 `['gs://mybucket/scf23.pdf']` 類似。

## 建立文件處理器

在 `us` 多區域中，根據[版面配置剖析器處理器](https://docs.cloud.google.com/document-ai/docs/layout-parse-chunk?hl=zh-tw)[建立文件處理器](https://docs.cloud.google.com/document-ai/docs/create-processor?hl=zh-tw#create-processor)。

## 為文件處理器建立遠端模型

建立遠端模型，存取 Document AI 處理器：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中執行下列陳述式：

   ```
   CREATE OR REPLACE MODEL `bqml_tutorial.parser_model`
   REMOTE WITH CONNECTION `LOCATION.CONNECTION_ID`
     OPTIONS(remote_service_type = 'CLOUD_AI_DOCUMENT_V1', document_processor = 'PROCESSOR_ID');
   ```

   更改下列內容：

   * `LOCATION`：連線位置。
   * `CONNECTION_ID`：BigQuery 連線的 ID。

     在 Google Cloud 控制台中[查看連線詳細資料](https://docs.cloud.google.com/bigquery/docs/working-with-connections?hl=zh-tw#view-connections)時，`CONNECTION_ID` 是「連線 ID」中顯示的完整連線 ID 最後一個區段的值，例如 `projects/myproject/locations/connection_location/connections/myconnection`。
   * `PROCESSOR_ID`：文件處理器 ID。如要找出這個值，請[查看處理器詳細資料](https://docs.cloud.google.com/document-ai/docs/create-processor?hl=zh-tw#get-processor)，然後查看「基本資訊」部分中的「ID」列。

## 將 PDF 檔案剖析為區塊

使用 `ML.PROCESS_DOCUMENT` 函式搭配文件處理器，將 PDF 檔案剖析為多個分塊，然後將內容寫入表格。`ML.PROCESS_DOCUMENT` 函式會以 JSON 格式傳回 PDF 區塊。

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中執行下列陳述式：

   ```
   CREATE or REPLACE TABLE bqml_tutorial.chunked_pdf AS (
     SELECT * FROM ML.PROCESS_DOCUMENT(
     MODEL bqml_tutorial.parser_model,
     TABLE bqml_tutorial.pdf,
     PROCESS_OPTIONS => (JSON '{"layout_config": {"chunking_config": {"chunk_size": 250}}}')
     )
   );
   ```

## 將 PDF 區塊資料剖析為不同的資料欄

從 `ML.PROCESS_DOCUMENT` 函式傳回的 JSON 資料中擷取 PDF 內容和中繼資料資訊，然後將該內容寫入表格：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中執行下列陳述式，剖析 PDF 內容：

   ```
   CREATE OR REPLACE TABLE bqml_tutorial.parsed_pdf AS (
   SELECT
     uri,
     JSON_EXTRACT_SCALAR(json , '$.chunkId') AS id,
     JSON_EXTRACT_SCALAR(json , '$.content') AS content,
     JSON_EXTRACT_SCALAR(json , '$.pageFooters[0].text') AS page_footers_text,
     JSON_EXTRACT_SCALAR(json , '$.pageSpan.pageStart') AS page_span_start,
     JSON_EXTRACT_SCALAR(json , '$.pageSpan.pageEnd') AS page_span_end
   FROM bqml_tutorial.chunked_pdf, UNNEST(JSON_EXTRACT_ARRAY(ml_process_document_result.chunkedDocument.chunks, '$')) json
   );
   ```
3. 在查詢編輯器中執行下列陳述式，即可查看已剖析 PDF 內容的子集：

   ```
   SELECT *
   FROM `bqml_tutorial.parsed_pdf`
   ORDER BY id
   LIMIT 5;
   ```

   輸出結果會與下列內容相似：

   ```
   +-----------------------------------+------+------------------------------------------------------------------------------------------------------+-------------------+-----------------+---------------+
   |                uri                |  id  |                                                 content                                              | page_footers_text | page_span_start | page_span_end |
   +-----------------------------------+------+------------------------------------------------------------------------------------------------------+-------------------+-----------------+---------------+
   | gs://mybucket/scf23.pdf           | c1   | •BOARD OF OF FEDERAL GOVERN NOR RESERVE SYSTEM RESEARCH & ANALYSIS                                   | NULL              | 1               | 1             |
   | gs://mybucket/scf23.pdf           | c10  | • In 2022, 20 percent of all families, 14 percent of families in the bottom half of the usual ...    | NULL              | 8               | 9             |
   | gs://mybucket/scf23.pdf           | c100 | The SCF asks multiple questions intended to capture whether families are credit constrained, ...     | NULL              | 48              | 48            |
   | gs://mybucket/scf23.pdf           | c101 | Bankruptcy behavior over the past five years is based on a series of retrospective questions ...     | NULL              | 48              | 48            |
   | gs://mybucket/scf23.pdf           | c102 | # Percentiles of the Distributions of Income and Net Worth                                           | NULL              | 48              | 49            |
   +-----------------------------------+------+------------------------------------------------------------------------------------------------------+-------------------+-----------------+---------------+
   ```

## 建立用於生成嵌入項目的遠端模型

建立遠端模型，代表代管的 Vertex AI 文字嵌入生成模型：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中執行下列陳述式：

   ```
   CREATE OR REPLACE MODEL `bqml_tutorial.embedding_model`
     REMOTE WITH CONNECTION `LOCATION.CONNECTION_ID`
     OPTIONS (ENDPOINT = 'text-embedding-005');
   ```

   更改下列內容：

   * `LOCATION`：連線位置。
   * `CONNECTION_ID`：BigQuery 連線的 ID。

     在 Google Cloud 控制台中[查看連線詳細資料](https://docs.cloud.google.com/bigquery/docs/working-with-connections?hl=zh-tw#view-connections)時，`CONNECTION_ID` 是「連線 ID」中顯示的完整連線 ID 最後一個區段的值，例如 `projects/myproject/locations/connection_location/connections/myconnection`。

## 生成嵌入項目

為剖析的 PDF 內容生成嵌入項目，然後寫入資料表：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中執行下列陳述式：

   ```
   CREATE OR REPLACE TABLE `bqml_tutorial.embeddings` AS
   SELECT * FROM AI.GENERATE_EMBEDDING(
     MODEL `bqml_tutorial.embedding_model`,
     TABLE `bqml_tutorial.parsed_pdf`
   );
   ```

## 執行向量搜尋

對剖析的 PDF 內容執行向量搜尋。

下列查詢會接收文字輸入內容、使用 `AI.GENERATE_EMBEDDING` 函式為該輸入內容建立嵌入，然後使用 `VECTOR_SEARCH` 函式，將輸入嵌入與最相似的 PDF 內容嵌入進行比對。結果是與輸入內容在語意上最相似的前 10 個 PDF 區塊。

1. 前往「BigQuery」頁面

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中，執行下列 SQL 陳述式：

   ```
   SELECT query.query, base.id AS pdf_chunk_id, base.content, distance
   FROM
     VECTOR_SEARCH( TABLE `bqml_tutorial.embeddings`,
       'embedding',
       (
       SELECT
         embedding,
         content AS query
       FROM
         AI.GENERATE_EMBEDDING( MODEL `bqml_tutorial.embedding_model`,
           ( SELECT 'Did the typical family net worth increase? If so, by how much?' AS content)
         )
       ),
       top_k => 10,
       OPTIONS => '{"fraction_lists_to_search": 0.01}')
   ORDER BY distance DESC;
   ```

   輸出結果會與下列內容相似：

   ```
   +-------------------------------------------------+--------------+------------------------------------------------------------------------------------------------------+---------------------+
   |                query                            | pdf_chunk_id |                                                 content                                              | distance            |
   +-------------------------------------------------+--------------+------------------------------------------------------------------------------------------------------+---------------------+
   | Did the typical family net worth increase? ,... | c9           | ## Assets                                                                                            | 0.31113668174119469 |
   |                                                 |              |                                                                                                      |                     |
   |                                                 |              | The homeownership rate increased slightly between 2019 and 2022, to 66.1 percent. For ...            |                     |
   +-------------------------------------------------+--------------+------------------------------------------------------------------------------------------------------+---------------------+
   | Did the typical family net worth increase? ,... | c50          | # Box 3. Net Housing Wealth and Housing Affordability                                                | 0.30973592073929113 |
   |                                                 |              |                                                                                                      |                     |
   |                                                 |              | For families that own their primary residence ...                                                    |                     |
   +-------------------------------------------------+--------------+------------------------------------------------------------------------------------------------------+---------------------+
   | Did the typical family net worth increase? ,... | c50          | 3 In the 2019 SCF, a small portion of the data collection overlapped with early months of            | 0.29270064592817646 |
   |                                                 |              | the COVID- ...                                                                                       |                     |
   +-------------------------------------------------+--------------+------------------------------------------------------------------------------------------------------+---------------------+
   ```

## 建立文字生成遠端模型

建立遠端模型，代表代管的 Vertex AI 文字生成模型：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中執行下列陳述式：

   ```
   CREATE OR REPLACE MODEL `bqml_tutorial.text_model`
     REMOTE WITH CONNECTION `LOCATION.CONNECTION_ID`
     OPTIONS (ENDPOINT = 'gemini-2.0-flash-001');
   ```

   更改下列內容：

   * `LOCATION`：連線位置。
   * `CONNECTION_ID`：BigQuery 連線的 ID。

     在 Google Cloud 控制台中[查看連線詳細資料](https://docs.cloud.google.com/bigquery/docs/working-with-connections?hl=zh-tw#view-connections)時，`CONNECTION_ID` 是「連線 ID」中顯示的完整連線 ID 最後一個區段的值，例如 `projects/myproject/locations/connection_location/connections/myconnection`。

## 根據向量搜尋結果生成文字

對嵌入執行向量搜尋，找出語意相似的 PDF 內容，然後搭配向量搜尋結果使用 `AI.GENERATE_TEXT` 函式，擴增提示輸入內容並提升文字生成結果。在本例中，查詢會使用 PDF 區塊中的資訊，回答有關過去十年家庭淨值變化的問題。

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中執行下列陳述式：

   ```
   SELECT
     result AS generated
     FROM
     AI.GENERATE_TEXT( MODEL `bqml_tutorial.text_model`,
       (
       SELECT
       CONCAT( 'Did the typical family net worth change? How does this compare the SCF survey a decade earlier? Be concise and use the following context:',
       STRING_AGG(FORMAT("context: %s and reference: %s", base.content, base.uri), ',\n')) AS prompt,
       FROM
         VECTOR_SEARCH( TABLE
           `bqml_tutorial.embeddings`,
           'embedding',
           (
           SELECT
             embedding,
             content AS query
           FROM
             AI.GENERATE_EMBEDDING( MODEL `bqml_tutorial.embedding_model`,
               (
               SELECT
                 'Did the typical family net worth change? How does this compare the SCF survey a decade earlier?' AS content
               )
             )
           ),
           top_k => 10,
           OPTIONS => '{"fraction_lists_to_search": 0.01}')
         ),
         STRUCT(512 AS max_output_tokens)
     );
   ```

   輸出結果會與下列內容相似：

   ```
   +-------------------------------------------------------------------------------+
   |               generated                                                       |
   +-------------------------------------------------------------------------------+
   | Between the 2019 and 2022 Survey of Consumer Finances (SCF), real median      |
   | family net worth surged 37 percent to $192,900, and real mean net worth       |
   | increased 23 percent to $1,063,700.  This represents the largest three-year   |
   | increase in median net worth in the history of the modern SCF, exceeding the  |
   | next largest by more than double.  In contrast, between 2010 and 2013, real   |
   | median net worth decreased 2 percent, and real mean net worth remained        |
   | unchanged.                                                                    |
   +-------------------------------------------------------------------------------+
   ```

## 清除所用資源

**注意**：刪除專案會造成以下結果：

* **專案中的所有內容都會遭到刪除。**如果使用現有專案來進行本文中的任務，刪除專案將一併移除當中已完成的其他任務'。
* **自訂專案 ID 會消失。**當您之前建立這個專案時，可能建立了想要在日後使用的自訂專案 ID。如要保留使用該專案 ID 的網址 (例如 `appspot.com` 網址)，請刪除在該專案中選取的資源，而不是刪除整個專案。

如果打算探索多種架構、教學課程或快速入門導覽課程，重複使用專案可避免超出專案配額限制。

1. 前往 Google Cloud 控制台的「Manage resources」(管理資源) 頁面。

   [前往「Manage resources」(管理資源)](https://console.cloud.google.com/iam-admin/projects?hl=zh-tw)
2. 在專案清單中選取要刪除的專案，然後點選「Delete」(刪除)。
3. 在對話方塊中輸入專案 ID，然後按一下 [Shut down] (關閉) 以刪除專案。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-14 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-14 (世界標準時間)。"],[],[]]