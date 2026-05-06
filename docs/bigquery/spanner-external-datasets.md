Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 建立 Spanner 外部資料集

本文說明如何在 BigQuery 中建立外部資料集 (又稱聯合資料集)，並連結至 [Spanner](https://docs.cloud.google.com/spanner/docs?hl=zh-tw) 中現有的 GoogleSQL 或 PostgreSQL 資料庫。

外部資料集是 BigQuery 與外部資料來源在資料集層級的連結。您可以使用 GoogleSQL 查詢 Spanner 資料庫中的交易資料，不必將所有資料從 Spanner 複製或匯入 BigQuery 儲存空間。這些查詢結果會[儲存在 BigQuery](https://docs.cloud.google.com/bigquery/docs/writing-results?hl=zh-tw#temporary_and_permanent_tables) 中。

系統會自動從相應的外部資料來源，填入外部資料集中的資料表。您可以在 BigQuery 中直接查詢這些資料表，但無法修改、新增或刪除資料。不過，您在外部資料來源中進行的任何更新，都會自動反映在 BigQuery 中。

查詢 Spanner 時，查詢結果預設會儲存到暫時性資料表。您也可以選擇將這些資料儲存為新的 BigQuery 資料表、與其他資料表彙整，或使用 [DML](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/dml-syntax?hl=zh-tw) 與現有資料表合併。

## 所需權限

如要取得建立外部資料集所需的權限，請要求系統管理員授予您「[BigQuery 使用者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.user) 」(`roles/bigquery.user`) IAM 角色。如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

這個預先定義的角色具備  `bigquery.datasets.create` 權限，可建立外部資料集。

您或許還可透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)取得這項權限。

如要進一步瞭解 BigQuery 中的 IAM 角色和權限，請參閱「[IAM 簡介](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)」。

## 使用 `CLOUD_RESOURCE` 連線

(選用) Spanner 外部資料集可使用 `CLOUD_RESOURCE` 連線與 Spanner 資料庫互動，因此您可透過 BigQuery 提供使用者 Spanner 資料存取權，不必直接授予他們 Spanner 資料庫存取權。由於 `CLOUD_RESOURCE` 連線的服務帳戶會負責從 Spanner 擷取資料，您只需要授予使用者 Spanner 外部資料集的存取權即可。

使用 `CLOUD_RESOURCE` 連線建立 Spanner 外部資料集前，請先完成下列工作：

### 建立連線

您可以建立或使用現有的[`CLOUD_RESOURCE`連線](https://docs.cloud.google.com/bigquery/docs/create-cloud-resource-connection?hl=zh-tw)連線至 Spanner。請務必在您打算建立 Spanner 外部資料集的[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)建立連線。

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

建立連線後，請開啟連線，並在「連線資訊」窗格中複製服務帳戶 ID。設定連線權限時，您需要這個 ID。建立連線資源時，BigQuery 會建立專屬的系統服務帳戶，並將其與連線建立關聯。

### 設定存取權

您必須授予與新連線相關聯的服務帳戶，對 Spanner 執行個體或資料庫的讀取權限。建議使用「Cloud Spanner 資料庫讀取者 (使用 Data Boost)」(`roles/spanner.databaseReaderWithDataBoost`) 預先定義的 IAM 角色。

請按照下列步驟，為先前從連線複製的服務帳戶授予資料庫層級的角色存取權：

1. 前往 Spanner「Instances」(執行個體) 頁面。

   [前往執行個體頁面](https://console.cloud.google.com/spanner/instances?hl=zh-tw)
2. 點選包含您的資料庫的執行個體名稱，前往「執行個體詳細資料」頁面。
3. 在「Overview」(總覽) 分頁中，選取資料庫的核取方塊。  
   「Info panel」(資訊面板) 隨即出現。
4. 按一下「Add principal」(新增主體)。
5. 在「新增主體」面板的「新增主體」中，輸入先前複製的服務帳戶 ID。
6. 在「請選擇角色」欄位中，選取「Cloud Spanner 資料庫讀取者 (使用 Data Boost)」角色。
7. 按一下 [儲存]。

## 建立外部資料集

如要建立外部資料集，請按照下列步驟操作：

### 控制台

1. 在 Google Cloud 控制台中開啟 BigQuery 頁面。

   [前往 BigQuery 頁面](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。

   如果沒有看到左側窗格，請按一下 last\_page「Expand left pane」(展開左側窗格)，開啟窗格。
3. 在「Explorer」窗格中，選取要建立資料集的專案。
4. 按一下 more\_vert「View actions」(查看動作)，然後點選「Create dataset」(建立資料集)。
5. 在「建立資料集」頁面中，執行下列操作：

   * 針對「Dataset ID」(資料集 ID)，輸入唯一的資料集名稱。
   * 在「位置類型」中，選擇資料集的位置，例如 `us-central1` 或多區域 `us`。資料集建立後，就無法變更位置。
   * 以「外部資料集」來說，請執行下列操作：

     + 勾選「外部資料集的連結」旁邊的方塊。
     + 在「External dataset type」(外部資料集類型) 中，選取 `Spanner`。
     + 在「外部來源」中，輸入 Spanner 資料庫的完整 ID，格式如下：`projects/PROJECT_ID/instances/INSTANCE/databases/DATABASE`。例如：`projects/my_project/instances/my_instance/databases/my_database`。
     + (選用) 在「Database role」(資料庫角色) 中輸入 Spanner 資料庫角色的名稱。如要進一步瞭解用於[建立 Spanner 連線](https://docs.cloud.google.com/bigquery/docs/connect-to-spanner?hl=zh-tw#create-spanner-connection)的資料庫角色，請參閱這篇文章
     + 如要使用連線建立外部資料集，請勾選「使用 Cloud 資源連結」旁的方塊。
   * 其他預設設定則保留不變。
6. 點選「建立資料集」。

### SQL

使用[`CREATE EXTERNAL SCHEMA`資料定義語言 (DDL) 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#create_external_schema_statement)。

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列陳述式：

   ```
   CREATE EXTERNAL SCHEMA DATASET_NAME
     OPTIONS (
       external_source = 'SPANNER_EXTERNAL_SOURCE',
       location = 'LOCATION');
   /*
     Alternatively, create with a connection:
   */
   CREATE EXTERNAL SCHEMA DATASET_NAME
     WITH CONNECTION PROJECT_ID.LOCATION.CONNECTION_NAME
     OPTIONS (
       external_source = 'SPANNER_EXTERNAL_SOURCE',
       location = 'LOCATION');
   ```

   請替換下列項目：

   * `DATASET_NAME`：BigQuery 中新資料集的名稱。
   * `SPANNER_EXTERNAL_SOURCE`：完整的合格 Spanner 資料庫名稱，並加上前置字元來識別來源，格式如下：`google-cloudspanner://[DATABASE_ROLE@]/projects/PROJECT_ID/instances/INSTANCE/databases/DATABASE`。例如：
     `google-cloudspanner://admin@/projects/my_project/instances/my_instance/databases/my_database` 或 `google-cloudspanner:/projects/my_project/instances/my_instance/databases/my_database`。
   * `LOCATION`：BigQuery 中新資料集的位置，例如 `us-central1`。建立資料集後，就無法變更位置。
   * (選用)`CONNECTION_NAME`：Cloud 資源連結的名稱。
3. 按一下「執行」play\_circle。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

### bq

在指令列環境中，使用 [`bq mk` 指令](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#mk-dataset)建立外部資料集：

```
bq --location=LOCATION mk --dataset \
    --external_source SPANNER_EXTERNAL_SOURCE \
    DATASET_NAME
```

或者，使用連線建立：

```
bq --location=LOCATION mk --dataset \
    --external_source SPANNER_EXTERNAL_SOURCE \
    --connection_id PROJECT_ID.LOCATION.CONNECTION_NAME \
    DATASET_NAME
```

更改下列內容：

* `LOCATION`：BigQuery 中新資料集的位置，例如 `us-central1`。建立資料集後，就無法變更位置。您可以使用 [`.bigqueryrc` 檔案](https://docs.cloud.google.com/bigquery/docs/bq-command-line-tool?hl=zh-tw#setting_default_values_for_command-line_flags)設定預設位置值。
* `SPANNER_EXTERNAL_SOURCE`：完整的合格 Spanner 資料庫名稱，並加上前置字元來識別來源，格式如下：`google-cloudspanner://[DATABASE_ROLE@]/projects/PROJECT_ID/instances/INSTANCE/databases/DATABASE`。例如：`google-cloudspanner://admin@/projects/my_project/instances/my_instance/databases/my_database` 或 `google-cloudspanner:/projects/my_project/instances/my_instance/databases/my_database`。
* `DATASET_NAME`：BigQuery 中新資料集的名稱。如要在非預設專案中建立資料集，請採用下列格式將專案 ID 新增至資料集名稱：`PROJECT_ID`:`DATASET_NAME`。
* (選用)`CONNECTION_NAME`：Cloud 資源連結的名稱。

### Terraform

使用 [`google_bigquery_dataset` 資源](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/bigquery_dataset#example-usage---bigquery-dataset-external-reference-aws-docs)。

**注意：** 如要使用 Terraform 建立 BigQuery 物件，必須啟用 [Cloud Resource Manager API](https://docs.cloud.google.com/resource-manager/reference/rest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

以下範例會建立 Spanner 外部資料集：

```
resource "google_bigquery_dataset" "default" {
  dataset_id    = "my_external_dataset"
  friendly_name = "My external dataset"
  description   = "This is a test description."
  location      = "US"
  external_dataset_reference {
    # The full identifier of your Spanner database.
    external_source = "google-cloudspanner:/projects/my_project/instances/my_instance/databases/my_database"
    # Must be empty for a Spanner external dataset.
    connection = ""
  }
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

### API

使用已定義的[資料集資源](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/datasets?hl=zh-tw)和 Spanner 資料庫的 [`externalDatasetReference` 欄位](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/datasets?hl=zh-tw#ExternalDatasetReference)，呼叫 [`datasets.insert` 方法](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/datasets/insert?hl=zh-tw)。

請注意，外部資料集中的資料表名稱不區分大小寫。

使用 `CLOUD_RESOURCE` 連線建立外部資料集時，您必須對外部資料集使用的連線具備 `bigquery.connections.delegate` 權限 (可透過 BigQuery 連線管理員角色取得)。

## 控管資料表的存取權

Spanner 外部資料集支援使用者憑證 (EUC)。也就是說，從外部資料集存取 Spanner 資料表時，存取權是由 Spanner 控制。使用者必須在 Spanner 中獲得存取權，才能查詢這些資料表。

Spanner 外部資料集也支援存取權委派。存取權委派功能可將 Spanner 資料表的存取權，與外部資料集和基礎 Spanner 資料表的直接存取權分開。與服務帳戶相關聯的 Cloud 資源連結，可用於連線至 Spanner。即使使用者未在 Spanner 中獲得授權，也能從外部資料集查詢這些 Spanner 資料表。

## 列出外部資料集中的資料表

如要列出外部資料集中可供查詢的資料表，請參閱[列出資料集](https://docs.cloud.google.com/bigquery/docs/listing-datasets?hl=zh-tw)。

## 取得資料表資訊

如要取得外部資料集中的資料表資訊 (例如結構定義詳細資料)，請參閱「[取得資料表資訊](https://docs.cloud.google.com/bigquery/docs/tables?hl=zh-tw#get_table_information)」。

## 查詢 Spanner 資料

[查詢外部資料集中的資料表](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw)，與查詢任何其他 BigQuery 資料集中的資料表相同。不過，系統不支援資料修改作業 (DML)。

查詢 Spanner 外部資料集中的資料表時，系統預設會使用 [Data Boost](https://docs.cloud.google.com/bigquery/docs/spanner-federated-queries?hl=zh-tw#data_boost)，且無法變更。因此，您需要[額外權限](https://docs.cloud.google.com/bigquery/docs/spanner-federated-queries?hl=zh-tw#before_you_begin_2)才能執行這類查詢。

## 在外部資料集中建立檢視區塊

您無法在外來資料集中建立檢視區塊。不過，您可以在標準資料集中建立檢視區塊，並以外部資料集中的資料表為基礎。詳情請參閱「[建立檢視區塊](https://docs.cloud.google.com/bigquery/docs/views?hl=zh-tw)」。

## 刪除外部資料集

刪除外部資料集與刪除任何其他 BigQuery 資料集相同。刪除外部資料集不會影響 Spanner 資料庫中的資料表。詳情請參閱「[刪除資料集](https://docs.cloud.google.com/bigquery/docs/managing-datasets?hl=zh-tw#delete-datasets)」。

## 根據外部資料集中的資料表建立非遞增 materialized view

繼續操作前，請先使用[`CLOUD_RESOURCE`連線](https://docs.cloud.google.com/bigquery/docs/spanner-external-datasets?hl=zh-tw#use_a_cloud_resource_connection)建立基礎 Spanner 外部資料集。

您可以使用 `allow_non_incremental_definition` 選項，建立參照 [Spanner 外部資料集資料表](https://docs.cloud.google.com/bigquery/docs/spanner-external-datasets?hl=zh-tw)的非遞增具體化檢視區塊。以下範例使用基礎 Spanner 外部資料集資料表：

```
/*
  You must create the spanner_external_dataset with a CLOUD_RESOURCE connection.
*/
CREATE MATERIALIZED VIEW sample_dataset.sample_spanner_mv
  OPTIONS (
      enable_refresh = true, refresh_interval_minutes = 60,
      max_staleness = INTERVAL "24" HOUR,
        allow_non_incremental_definition = true)
AS
  SELECT COUNT(*) cnt FROM spanner_external_dataset.spanner_table;
```

## 限制

* 適用 BigQuery 聯合查詢的[限制](https://docs.cloud.google.com/bigquery/docs/federated-queries-intro?hl=zh-tw#limitations)。
* BigQuery 只能存取預設 Spanner 結構定義中的資料表。系統不支援[已命名結構定義](https://docs.cloud.google.com/spanner/docs/schema-and-data-model?hl=zh-tw#named-schemas)中的表格。
* 在 BigQuery 中，您看不到 Spanner 資料庫中定義的主鍵和外鍵。
* 如果 Spanner 資料庫中的資料表含有 BigQuery 不支援的類型資料欄，則無法在 BigQuery 端存取該資料欄。
* 您無法在 Spanner 外部資料集中的資料表新增、刪除或更新資料或中繼資料。
* 您無法在 Spanner 外部資料集中建立新的資料表、檢視區塊或具體化檢視區塊。
* 不支援[`INFORMATION_SCHEMA`檢視](https://docs.cloud.google.com/bigquery/docs/information-schema-intro?hl=zh-tw)。
* 不支援[中繼資料快取](https://docs.cloud.google.com/bigquery/docs/biglake-intro?hl=zh-tw#metadata_caching_for_performance)。
* 與資料表建立預設值相關的資料集層級設定不會影響外部資料集，因為您無法手動建立資料表。
* 不支援 Write API 和 Read API。
* 不支援列層級安全防護機制、資料欄層級安全防護機制和資料遮蓋。
* 系統不支援以 Spanner 外部資料集中的資料表為基礎的增量具體化檢視表，但預先發布版支援非增量具體化檢視表。
* 不支援與 Knowledge Catalog 整合。例如，系統不支援資料設定檔和資料品質掃描。
* 系統不支援表格層級的標記。
* 撰寫查詢時，SQL 自動完成功能不適用於 Spanner 外部資料表。
* 外部資料集不支援「[透過 Sensitive Data Protection 掃描](https://docs.cloud.google.com/bigquery/docs/scan-with-dlp?hl=zh-tw#scanning-bigquery-data-using-the-cloud-console)」。
* BigQuery sharing (舊稱 Analytics Hub) 不支援共用外部資料集。
* 如果 Spanner 外部資料集使用使用者憑證 (EUC)，您可以建立參照外部資料集的授權 view。不過，查詢這個檢視區塊時，執行查詢者的 EUC 會傳送至 Spanner。
* 如果 Spanner 外部資料集使用 Cloud 資源連結進行存取權委派，您可以建立參照外部資料集的授權 view 或授權常式。

## 後續步驟

* 進一步瞭解 [Spanner 聯合查詢](https://docs.cloud.google.com/bigquery/docs/spanner-federated-queries?hl=zh-tw)。
* 進一步瞭解如何[透過 Spanner 外部資料集建立具體化檢視區塊](https://docs.cloud.google.com/bigquery/docs/materialized-views-create?hl=zh-tw#spanner)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-06 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-06 (世界標準時間)。"],[],[]]