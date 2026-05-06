Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 使用 AI.GENERATE\_EMBEDDING 函式生成影片嵌入

本文說明如何建立參照 Vertex AI 嵌入[基礎模型](https://docs.cloud.google.com/vertex-ai/docs/generative-ai/learn/models?hl=zh-tw#foundation_models)的 BigQuery ML [遠端模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model?hl=zh-tw)。接著，您將使用前面建立的模型和 [`AI.GENERATE_EMBEDDING` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-ai-generate-embedding?hl=zh-tw)，透過 BigQuery [物件資料表](https://docs.cloud.google.com/bigquery/docs/object-table-introduction?hl=zh-tw)中的資料建立影片嵌入。

## 必要的角色

如要建立遠端模型並產生嵌入內容，您需要下列 Identity and Access Management (IAM) 角色：

* 建立及使用 BigQuery 資料集、資料表和模型：
  專案中的 BigQuery 資料編輯者 (`roles/bigquery.dataEditor`)。
* 建立、委派及使用 BigQuery 連線：專案的 BigQuery 連線管理員 (`roles/bigquery.connectionsAdmin`)。

  如果沒有設定[預設連線](https://docs.cloud.google.com/bigquery/docs/default-connections?hl=zh-tw)，您可以在執行 `CREATE MODEL` 陳述式時建立並設定連線。如要這麼做，您必須具備專案的 BigQuery 管理員角色 (`roles/bigquery.admin`)。詳情請參閱「[設定預設連線](https://docs.cloud.google.com/bigquery/docs/default-connections?hl=zh-tw#configure_the_default_connection)」。
* 將權限授予連線的服務帳戶：在包含 Vertex AI 端點的專案中，授予「專案 IAM 管理員」(`roles/resourcemanager.projectIamAdmin`) 角色。這是您透過將模型名稱指定為端點所建立遠端模型的目前專案。這是您透過指定網址做為端點所建立遠端模型網址中識別的專案。

  如果您使用遠端模型分析物件資料表中的非結構化資料，且物件資料表使用的 Cloud Storage bucket 與 Vertex AI 端點位於不同專案，您也必須在物件資料表使用的 Cloud Storage bucket 上擁有 Storage 管理員 (`roles/storage.admin`) 角色。
* 建立 BigQuery 工作：專案中的 BigQuery 工作使用者 (`roles/bigquery.jobUser`)。

這些預先定義的角色具備執行本文所述工作所需的權限。如要查看確切的必要權限，請展開「Required permissions」(必要權限) 部分：

#### 所需權限

* 建立資料集：`bigquery.datasets.create`
* 建立、委派及使用連線：
  `bigquery.connections.*`
* 設定服務帳戶權限：
  `resourcemanager.projects.getIamPolicy` 和
  `resourcemanager.projects.setIamPolicy`
* 建立物件資料表：
  `bigquery.tables.create` 和
  `bigquery.tables.update`
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
3. 啟用 BigQuery、BigQuery Connection、Cloud Storage 和 Vertex AI API。

   **啟用 API 時所需的角色**

   如要啟用 API，您需要服務使用情形管理員 IAM 角色 (`roles/serviceusage.serviceUsageAdmin`)，其中包含 `serviceusage.services.enable` 權限。[瞭解如何授予角色](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)。

   [啟用 API](https://console.cloud.google.com/flows/enableapi?apiid=bigquery.googleapis.com%2Cbigqueryconnection.googleapis.com%2Cstorage.googleapis.com%2Caiplatform.googleapis.com&hl=zh-tw)

## 建立資料集

建立 BigQuery 資料集來存放資源：

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。

   如果沒有看到左側窗格，請按一下「展開左側窗格」圖示 last\_page 開啟窗格。
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

如果您已設定預設連線，或具備 BigQuery 管理員角色，可以略過這個步驟。

選取下列選項之一：

### 控制台

1. 前往「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。

   如果沒有看到左側窗格，請按一下「展開左側窗格」圖示 last\_page 開啟窗格。
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
3. 按一下 play\_circle **執行**。

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

   視需要從 GitHub 複製程式碼。如果 Terraform 程式碼片段是端對端解決方案的一部分，建議您使用這個方法。
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

1. 檢查設定，確認 Terraform 即將建立或更新的資源符合您的預期：

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

### 授予服務帳戶存取權

為連線的服務帳戶授予 Vertex AI 使用者和 Storage 物件檢視者角色。

如果您打算在建立遠端模型時將端點指定為網址 (例如 `endpoint = 'https://us-central1-aiplatform.googleapis.com/v1/projects/myproject/locations/us-central1/publishers/google/models/gemini-2.0-flash'`)，請在網址指定的專案中授予這個角色。

如果您打算在建立遠端模型時使用模型名稱指定端點 (例如 `endpoint = 'gemini-2.0-flash'`)，請在您打算建立遠端模型的專案中授予這個角色。

在其他專案中授予角色會導致錯誤 `bqcx-1234567890-wxyz@gcp-sa-bigquery-condel.iam.gserviceaccount.com does not have the permission to access resource`。

如要授予這些角色，請按照下列步驟操作：

### 控制台

1. 前往「IAM & Admin」(IAM 與管理) 頁面。

   [前往「IAM & Admin」(IAM 與管理)](https://console.cloud.google.com/project/_/iam-admin?hl=zh-tw)
2. 按一下「新增」person\_add。

   「新增主體」對話方塊隨即開啟。
3. 在「新增主體」欄位，輸入先前複製的服務帳戶 ID。
4. 在「選取角色」欄位中，依序選取「Vertex AI」和「Vertex AI 使用者」。
5. 按一下 [Add another role] (新增其他角色)。
6. 在「Select a role」(請選擇角色) 欄位中，依序選取「Cloud Storage」和「Storage Object Viewer」(Storage 物件檢視者)。
7. 按一下 [儲存]。

### gcloud

使用 [`gcloud projects add-iam-policy-binding`](https://docs.cloud.google.com/sdk/gcloud/reference/projects/add-iam-policy-binding?hl=zh-tw) 指令。

```
gcloud projects add-iam-policy-binding 'PROJECT_NUMBER' --member='serviceAccount:MEMBER' --role='roles/aiplatform.user' --condition=None
gcloud projects add-iam-policy-binding 'PROJECT_NUMBER' --member='serviceAccount:MEMBER' --role='roles/storage.objectViewer' --condition=None
```

請替換下列項目：

* `PROJECT_NUMBER`：要授予角色的專案編號。
* `MEMBER`：您先前複製的服務帳戶 ID。

## 建立物件資料表

如要分析影片，但不想將影片從 Cloud Storage 移出，請建立物件資料表。

如要建立物件資料表，請按照下列步驟操作：

### SQL

使用 [`CREATE EXTERNAL TABLE` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#create_external_table_statement)。

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列陳述式：

   ```
   CREATE EXTERNAL TABLE `PROJECT_ID.DATASET_ID.TABLE_NAME`
   WITH CONNECTION {`PROJECT_ID.REGION.CONNECTION_ID`| DEFAULT}
   OPTIONS(
     object_metadata = 'SIMPLE',
     uris = ['BUCKET_PATH'[,...]],
     max_staleness = STALENESS_INTERVAL,
     metadata_cache_mode = 'CACHE_MODE');
   ```

   請替換下列項目：

   * `PROJECT_ID`：您的專案 ID。
   * `DATASET_ID`：您[建立的資料集](#create_a_dataset) ID。
   * `TABLE_NAME`：物件資料表的名稱。
   * `REGION`：包含連線的[區域或多區域](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw#supported_locations)。
   * `CONNECTION_ID`：您[建立的連線](#create_a_connection) ID。

     在 Google Cloud 控制台中[查看連線詳細資料](https://docs.cloud.google.com/bigquery/docs/working-with-connections?hl=zh-tw#view-connections)時，這是「連線 ID」中顯示的完整連線 ID 最後一個部分的值，例如 `projects/myproject/locations/connection_location/connections/myconnection`。

     如要使用[預設連線](https://docs.cloud.google.com/bigquery/docs/default-connections?hl=zh-tw)，請指定 `DEFAULT`，而非包含 `PROJECT_ID.REGION.CONNECTION_ID` 的連線字串。
   * `BUCKET_PATH`：包含影片的 Cloud Storage 值區路徑，格式為 `['gs://bucket_name/[folder_name/]*']`。

     您使用的 Cloud Storage 值區應位於同一個專案，您打算在該專案中建立模型並呼叫 `AI.GENERATE_EMBEDDING` 函式。如要呼叫的 `AI.GENERATE_EMBEDDING` 函式與物件表格使用的 Cloud Storage 值區位於不同專案，您必須[在值區層級授予 Storage Admin 角色](https://docs.cloud.google.com/storage/docs/access-control/using-iam-permissions?hl=zh-tw#bucket-add)給 `service-A@gcp-sa-aiplatform.iam.gserviceaccount.com` 服務帳戶。
   * `STALENESS_INTERVAL`：指定針對物件資料表執行的作業是否使用快取中繼資料，以及作業必須使用多新的快取中繼資料。如要進一步瞭解中繼資料快取注意事項，請參閱「[中繼資料快取，提升效能](https://docs.cloud.google.com/bigquery/docs/object-table-introduction?hl=zh-tw#metadata_caching_for_performance)」。

     如要停用中繼資料快取功能，請指定 0。這是目前的預設做法。

     如要啟用中繼資料快取功能，請指定介於 30 分鐘至 7 天之間的[間隔常值](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/lexical?hl=zh-tw#interval_literals)。舉例來說，如要指定 4 小時的過時間隔，請輸入 `INTERVAL 4 HOUR`。如果資料表在過去 4 小時內重新整理過，針對資料表執行的作業就會使用快取中繼資料。如果快取中繼資料的建立時間早於該時間，作業會改為從 Cloud Storage 擷取中繼資料。
   * `CACHE_MODE`：指定中繼資料快取是否自動或手動重新整理。如要進一步瞭解中繼資料快取注意事項，請參閱「[中繼資料快取，提升效能](https://docs.cloud.google.com/bigquery/docs/object-table-introduction?hl=zh-tw#metadata_caching_for_performance)」。

     設為 `AUTOMATIC`，中繼資料快取就會以系統定義的時間間隔 (通常為 30 到 60 分鐘) 重新整理。

     如要依您決定的時間表重新整理中繼資料快取，請設為 `MANUAL`。在這種情況下，您可以呼叫 [`BQ.REFRESH_EXTERNAL_METADATA_CACHE` 系統程序](https://docs.cloud.google.com/bigquery/docs/reference/system-procedures?hl=zh-tw#bqrefresh_external_metadata_cache)來重新整理快取。

     如果 `STALENESS_INTERVAL` 設為大於 0 的值，您就必須設定 `CACHE_MODE`。
3. 按一下 play\_circle **執行**。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

### bq

使用 [`bq mk`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#mk-table) 指令。

```
bq mk --table \
--external_table_definition=BUCKET_PATH@REGION.CONNECTION_ID \
--object_metadata=SIMPLE \
--max_staleness=STALENESS_INTERVAL \
--metadata_cache_mode=CACHE_MODE \
PROJECT_ID:DATASET_ID.TABLE_NAME
```

請替換下列項目：

* `BUCKET_PATH`：包含影片的 Cloud Storage 值區路徑，格式為 `['gs://bucket_name/[folder_name/]*']`。

  您使用的 Cloud Storage 值區應位於同一個專案，您打算在該專案中建立模型並呼叫 `AI.GENERATE_EMBEDDING` 函式。如要呼叫的 `AI.GENERATE_EMBEDDING` 函式與物件表格使用的 Cloud Storage 值區位於不同專案，您必須[在值區層級授予 Storage Admin 角色](https://docs.cloud.google.com/storage/docs/access-control/using-iam-permissions?hl=zh-tw#bucket-add)給 `service-A@gcp-sa-aiplatform.iam.gserviceaccount.com` 服務帳戶。
* `REGION`：包含連線的[區域或多區域](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw#supported_locations)。
* `CONNECTION_ID`：您[建立的連線](#create_a_connection) ID。

  在 Google Cloud 控制台中[查看連線詳細資料](https://docs.cloud.google.com/bigquery/docs/working-with-connections?hl=zh-tw#view-connections)時，這是「連線 ID」中顯示的完整連線 ID 最後一個部分的值，例如 `projects/myproject/locations/connection_location/connections/myconnection`。
* `STALENESS_INTERVAL`：指定針對物件資料表執行的作業是否使用快取中繼資料，以及作業必須使用多新的快取中繼資料。如要進一步瞭解中繼資料快取注意事項，請參閱「[中繼資料快取，提升效能](https://docs.cloud.google.com/bigquery/docs/object-table-introduction?hl=zh-tw#metadata_caching_for_performance)」。

  如要停用中繼資料快取功能，請指定 0。這是目前的預設做法。

  如要啟用中繼資料快取功能，請指定介於 30 分鐘至 7 天之間的[間隔常值](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/lexical?hl=zh-tw#interval_literals)。舉例來說，如要指定 4 小時的過時間隔，請輸入 `INTERVAL 4 HOUR`。如果資料表在過去 4 小時內重新整理過，針對資料表執行的作業就會使用快取中繼資料。如果快取中繼資料的建立時間早於該時間，作業會改為從 Cloud Storage 擷取中繼資料。
* `CACHE_MODE`：指定中繼資料快取是否自動或手動重新整理。如要進一步瞭解中繼資料快取注意事項，請參閱「[中繼資料快取，提升效能](https://docs.cloud.google.com/bigquery/docs/object-table-introduction?hl=zh-tw#metadata_caching_for_performance)」。

  設為 `AUTOMATIC`，中繼資料快取就會以系統定義的時間間隔 (通常為 30 到 60 分鐘) 重新整理。

  如要依您決定的時間表重新整理中繼資料快取，請設為 `MANUAL`。在這種情況下，您可以呼叫 [`BQ.REFRESH_EXTERNAL_METADATA_CACHE` 系統程序](https://docs.cloud.google.com/bigquery/docs/reference/system-procedures?hl=zh-tw#bqrefresh_external_metadata_cache)來重新整理快取。

  如果 `STALENESS_INTERVAL` 設為大於 0 的值，您就必須設定 `CACHE_MODE`。
* `PROJECT_ID`：您的專案 ID。
* `DATASET_ID`：您[建立的資料集](#create_a_dataset) ID。
* `TABLE_NAME`：物件資料表的名稱。

## 建立模型

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 使用 SQL 編輯器建立[遠端模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model?hl=zh-tw)：

   ```
   CREATE OR REPLACE MODEL `PROJECT_ID.DATASET_ID.MODEL_NAME`
   REMOTE WITH CONNECTION {DEFAULT | `PROJECT_ID.REGION.CONNECTION_ID`}
   OPTIONS (ENDPOINT = 'ENDPOINT');
   ```

   請替換下列項目：

   * `PROJECT_ID`：您的專案 ID。
   * `DATASET_ID`：您[建立的資料集](#create_a_dataset) ID。
   * `MODEL_NAME`：模型名稱。
   * `REGION`：包含連線的[區域或多區域](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw#supported_locations)。
   * `CONNECTION_ID`：您[建立的連線](#create_a_connection) ID。

     在 Google Cloud 控制台中[查看連線詳細資料](https://docs.cloud.google.com/bigquery/docs/working-with-connections?hl=zh-tw#view-connections)時，這是「連線 ID」中顯示的完整連線 ID 最後一個部分的值，例如 `projects/myproject/locations/connection_location/connections/myconnection`。
   * `ENDPOINT`：要使用的[嵌入模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model?hl=zh-tw#endpoint)，在本例中為 `multimodalembedding@001`。

     如果您在建立遠端模型時指定網址做為端點 (例如 `endpoint = 'https://us-central1-aiplatform.googleapis.com/v1/projects/myproject/locations/us-central1/publishers/google/models/multimodalembedding@001'`)，請確保網址中指定的專案，是您已將 Vertex AI 使用者角色授予連線服務帳戶的專案。

     您建立遠端模型的位置必須提供 `multimodalembedding@001` 模型。詳情請參閱[位置](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model?hl=zh-tw#locations)。

## 生成影片嵌入

使用物件資料表中的影片資料，透過 [`AI.GENERATE_EMBEDDING` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-ai-generate-embedding?hl=zh-tw)生成影片嵌入項目：

```
SELECT *
FROM AI.GENERATE_EMBEDDING(
  MODEL `PROJECT_ID.DATASET_ID.MODEL_NAME`,
  TABLE PROJECT_ID.DATASET_ID.TABLE_NAME,
  STRUCT(
    START_SECOND AS start_second,
    END_SECOND AS end_second,
    INTERVAL_SECONDS AS interval_seconds)
);
```

請替換下列項目：

* `PROJECT_ID`：您的專案 ID。
* `DATASET_ID`：包含模型的資料集 ID。
* `MODEL_NAME`：遠端模型名稱，透過 `multimodalembedding@001` 模型。
* `TABLE_NAME`：包含要嵌入影片的物件資料表名稱。
* `START_SECOND`：`FLOAT64` 值，指定影片的嵌入開始時間 (以秒為單位)。預設值為 `0`。這個值必須為正數，且小於 `end_second` 值。
* `END_SECOND`：`FLOAT64` 值，指定影片中要結束嵌入的秒數。預設值為 `120`。
  這個值必須為正數，且大於 `start_second` 值。
* `INTERVAL_SECONDS`：`FLOAT64` 值，用於指定建立嵌入時使用的間隔。舉例來說，如果您設定 `start_second = 0`、`end_second = 120` 和 `interval_seconds = 10`，影片就會分割成十二個 10 秒片段 (`[0, 10), [10, 20), [20, 30)...`)，並為每個片段產生嵌入內容。這個值必須大於 `4`，且小於 `120`。預設值為 `16`。

## 範例

以下範例說明如何為 `videos` 物件資料表中的影片建立嵌入內容。系統會針對每部影片中 10 秒到 40 秒之間，每 5 秒的間隔建立嵌入。

```
SELECT *
FROM
  AI.GENERATE_EMBEDDING(
    MODEL `mydataset.embedding_model`,
    TABLE `mydataset.videos`,
    STRUCT(
    10 AS start_second,
    40 AS end_second,
    5 AS interval_seconds)
  );
```

## 後續步驟

* 瞭解如何[使用文字和圖像嵌入執行文字轉圖像的語意搜尋](https://docs.cloud.google.com/bigquery/docs/generate-multimodal-embeddings?hl=zh-tw)。
* 瞭解如何[使用文字嵌入執行語意搜尋和檢索增強生成 (RAG)](https://docs.cloud.google.com/bigquery/docs/vector-index-text-search-tutorial?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-02 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-02 (世界標準時間)。"],[],[]]