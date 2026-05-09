Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 將資料匯出至 Spanner (反向 ETL)

本文說明如何設定從 BigQuery 到 Spanner 的反向擷取、轉換及載入 (反向 ETL) 工作流程。您可以使用 [`EXPORT DATA` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/export-statements?hl=zh-tw)，從 BigQuery 資料來源 (包括 [Iceberg 資料表](https://docs.cloud.google.com/bigquery/docs/iceberg-tables?hl=zh-tw)) 匯出資料至 [Spanner](https://docs.cloud.google.com/spanner/docs/overview?hl=zh-tw) 資料表。

這項反向 ETL 工作流程結合了 BigQuery 的分析功能，以及 Spanner 的低延遲和高處理量。這個工作流程可讓您為應用程式使用者提供資料，同時避免耗盡 BigQuery 的配額和限制。

## 事前準備

* 建立 [Spanner 資料庫](https://docs.cloud.google.com/spanner/docs/create-manage-databases?hl=zh-tw)，包括接收匯出資料的資料表。
* 授予[身分與存取權管理 (IAM) 角色](#required_roles)，讓使用者擁有執行本文中各項工作所需的權限。
* 建立[企業版或更高等級的預留項目](https://docs.cloud.google.com/bigquery/docs/reservations-tasks?hl=zh-tw#create_reservations)。如果將基準運算單元容量設為零並啟用[自動調度資源](https://docs.cloud.google.com/bigquery/docs/slots-autoscaling-intro?hl=zh-tw)，在將資料一次性匯出至 Spanner 時，或許能降低 BigQuery 運算費用。

### 必要的角色

如要取得將 BigQuery 資料匯出至 Spanner 所需的權限，請要求管理員在專案中授予您下列 IAM 角色：

* 從 BigQuery 資料表匯出資料：
  [BigQuery 資料檢視者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.dataViewer)  (`roles/bigquery.dataViewer`)
* 執行擷取工作：
  [BigQuery 使用者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.user)  (`roles/bigquery.user`)
* 檢查 Spanner 執行個體的參數：
  [Cloud Spanner 檢視者](https://docs.cloud.google.com/iam/docs/roles-permissions/spanner?hl=zh-tw#spanner.viewer)  (`roles/spanner.viewer`)
* 將資料寫入 Spanner 資料表：
  [Cloud Spanner 資料庫使用者](https://docs.cloud.google.com/iam/docs/roles-permissions/spanner?hl=zh-tw#spanner.databaseUser)  (`roles/spanner.databaseUser`)

如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

您或許也能透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)，取得必要權限。

## 限制

* Assured Workloads 不支援這項功能。
* 下列 BigQuery 資料類型在 Spanner 中沒有對應項目，因此不支援：

| Spanner 資料庫方言 | 不支援的 BigQuery 類型 |
| --- | --- |
| 所有方言 | * `STRUCT` * `GEOGRAPHY` * `DATETIME` * `RANGE` * `TIME` |
| GoogleSQL | * `BIGNUMERIC`：支援的 `NUMERIC` 類型不夠廣泛。請考慮在查詢中將明確轉換新增至 `NUMERIC` 型別。 |

* 匯出資料列的大小上限為 1 MiB。
* Spanner 會在匯出期間強制執行參照完整性。如果目標資料表是另一個資料表的子項 (INTERLEAVE IN PARENT)，或目標資料表有外鍵限制，系統會在匯出期間驗證外鍵和父項鍵。如果匯出的資料列寫入的資料表具有 INTERLEAVE IN PARENT，但父項資料列不存在，匯出作業就會失敗，並顯示「Parent row is missing. 無法寫入資料列」錯誤。如果匯出的資料列寫入的資料表具有外鍵限制，且參照的鍵不存在，匯出作業就會失敗，並顯示「違反外鍵限制」錯誤。匯出至多個資料表時，建議您依序匯出，確保匯出作業維持參照完整性。這通常表示要先匯出父項資料表和外鍵參照的資料表，再匯出參照這些資料表的資料表。

  如果匯出目標資料表有外鍵限制，或是另一個資料表的子項 (INTERLEAVE IN PARENT)，則必須先填入父項資料表，再匯出子項資料表，且父項資料表應包含所有對應的鍵。如果父項資料表沒有完整的相關鍵，嘗試匯出子項資料表就會失敗。
* BigQuery 工作 (例如擷取至 Spanner 的工作) 的最長執行時間為 6 小時。如要瞭解如何最佳化大型擷取工作，請參閱「[匯出最佳化](#export_optimization)」。或者，您也可以考慮將輸入內容分割成個別資料區塊，然後以個別擷取工作匯出。
* 只有 BigQuery Enterprise 或 Enterprise Plus 版本支援匯出至 Spanner。不支援 BigQuery Standard 版和隨選運算。
* 您無法使用持續查詢，將資料匯出至具有[自動產生主鍵](https://docs.cloud.google.com/spanner/docs/primary-key-default-value?hl=zh-tw)的 Spanner 資料表。
* 您無法使用連續查詢，將資料匯出至 PostgreSQL 方言資料庫中的 Spanner 資料表。
* 使用連續查詢匯出至 Spanner 資料表時，請務必選擇與 BigQuery 資料表中單調遞增整數不相符的主鍵。否則可能會導致匯出作業發生效能問題。如要瞭解 Spanner 中的主鍵，以及如何減輕這些效能問題，請參閱「[選擇主鍵](https://docs.cloud.google.com/spanner/docs/schema-and-data-model?hl=zh-tw#choose_a_primary_key)」。

## 使用「`spanner_options`」選項設定匯出作業

您可以使用 `spanner_options` 選項指定目標 Spanner 資料庫和資料表。設定會以 JSON 字串的形式表示，如下列範例所示：

```
EXPORT DATA OPTIONS(
   uri="https://spanner.googleapis.com/projects/PROJECT_ID/instances/INSTANCE_ID/databases/DATABASE_ID",
  format='CLOUD_SPANNER',
   spanner_options = """{
      "table": "TABLE_NAME",
      "change_timestamp_column": "CHANGE_TIMESTAMP",
      "priority": "PRIORITY",
      "tag": "TAG",
   }"""
)
```

更改下列內容：

* `PROJECT_ID`：您 Google Cloud 專案的名稱。
* `INSTANCE_ID`：資料庫執行個體的名稱。
* `DATABASE_ID`：資料庫名稱。
* `TABLE_NAME`：現有目的地資料表的名稱。
* `CHANGE_TIMESTAMP`：目的地 Spanner 資料表中 `TIMESTAMP` 型別資料欄的名稱。這個選項會在匯出期間使用，追蹤最新列更新的時間戳記。指定這個選項後，匯出作業會先讀取 Spanner 資料表中的資料列，確保只寫入最新的資料列更新。執行[持續匯出](#export_continuously)時，建議指定 `TIMESTAMP` 型別資料欄，因為具有相同主鍵的資料列變更順序非常重要。
* `PRIORITY` (選用)：寫入要求的[優先順序](https://docs.cloud.google.com/spanner/docs/reference/rest/v1/RequestOptions?hl=zh-tw#priority)。允許的值：`LOW`、`MEDIUM`、`HIGH`。預設值：`MEDIUM`。
* `TAG` (選用)：
  [要求標記](https://docs.cloud.google.com/spanner/docs/introspection/troubleshooting-with-tags?hl=zh-tw)
  有助於在 Spanner 監控中識別匯出工具流量。
  預設值為 `bq_export`。

## 匯出查詢條件

如要將查詢結果匯出至 Spanner，結果必須符合下列條件：

* 結果集中的所有資料欄都必須存在於目的地資料表中，且類型必須相符或[可轉換](#type_conversions)。
* 結果集必須包含目的地資料表的所有 `NOT NULL` 欄。
* 資料欄值不得超過資料表中的 Spanner [資料大小限制](https://docs.cloud.google.com/spanner/quotas?hl=zh-tw#tables)。
* 匯出至 Spanner 前，必須將所有不支援的資料欄類型轉換為支援的類型。

### 類型轉換

為方便使用，Spanner 匯出工具會自動套用下列型別轉換：

| BigQuery 類型 | Spanner 類型 |
| --- | --- |
| BIGNUMERIC | NUMERIC (僅限 PostgreSQL 方言) |
| FLOAT64 | FLOAT32 |
| BYTES | PROTO |
| INT64 | ENUM |

## 匯出資料

您可以使用 [`EXPORT DATA` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/export-statements?hl=zh-tw)，將資料從 BigQuery 資料表匯出至 Spanner 資料表。

下列範例會從名為 `mydataset.table1` 的資料表匯出所選欄位：

```
EXPORT DATA OPTIONS (
  uri="https://spanner.googleapis.com/projects/PROJECT_ID/instances/INSTANCE_ID/databases/DATABASE_ID",
  format='CLOUD_SPANNER',
  spanner_options="""{ "table": "TABLE_NAME" }"""
)
AS SELECT * FROM mydataset.table1;
```

更改下列內容：

* `PROJECT_ID`：您 Google Cloud 專案的名稱
* `INSTANCE_ID`：資料庫執行個體的名稱
* `DATABASE_ID`：資料庫名稱
* `TABLE_NAME`：現有目的地資料表的名稱

## 匯出具有相同 `rowkey` 值的多個結果

匯出含有多個相同 `rowkey` 值的資料列時，寫入 Spanner 的值會位於同一個 Spanner 資料列。匯出作業產生的 Spanner 資料列集只會包含單一相符的 BigQuery 資料列 (無法保證是哪一個)。

## 使用 `CLOUD_RESOURCE` 連線匯出

您可以將寫入權限委派給 BigQuery [`CLOUD_RESOURCE`](https://docs.cloud.google.com/bigquery/docs/create-cloud-resource-connection?hl=zh-tw) 連線，以便執行匯出作業，不必授予使用者 Spanner 資料庫的直接存取權。

使用 `CLOUD_RESOURCE` 連線匯出至 Spanner 前，請先完成下列步驟：

### 建立連線

您可以建立或使用現有的 [`CLOUD_RESOURCE` 連線](https://docs.cloud.google.com/bigquery/docs/create-cloud-resource-connection?hl=zh-tw)，連線至 Spanner。

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

建立連線後，請開啟連線。在「連線資訊」窗格中，複製服務帳戶 ID。設定連線權限時，您會需要這個 ID。建立連線資源時，BigQuery 會建立專屬的系統服務帳戶，並將其與連線建立關聯。

### 設定存取權

您必須授予與新連線相關聯的服務帳戶，對 Spanner 執行個體或資料庫的寫入權限。建議您使用**Cloud Spanner 資料庫使用者** (`roles/spanner.databaseUser`) 預先定義的 IAM 角色。這些步驟需要您在建立連線時複製的服務帳戶 ID。

如要授予服務帳戶資料庫層級角色存取權，請按照下列步驟操作：

1. 前往 Spanner 執行個體頁面。

   [前往執行個體頁面](https://console.cloud.google.com/spanner/instances?hl=zh-tw)
2. 按一下包含資料庫的執行個體名稱。
3. 在「Overview」(總覽) 分頁中，選取資料庫的核取方塊。
4. 系統會隨即顯示「資訊面板」對話方塊。按一下「新增主體」。
5. 在「新增主體」中，輸入先前複製的服務帳戶 ID。
6. 在「Select a role」(選取角色) 欄位中，選取具有 `spanner.databases.write` 權限的角色。建議您使用「Cloud Spanner Database User」(Cloud Spanner 資料庫使用者) 角色。
7. 按一下 [儲存]。

### 使用 `CLOUD_RESOURCE` 連線執行匯出作業

建立連線並授予適當存取權後，您可以使用 `CLOUD_RESOURCE` 連線執行匯出作業。以下範例顯示使用 `CLOUD_RESOURCE` 連線匯出的 `EXPORT` 指令。

```
EXPORT DATA WITH CONNECTION `PROJECT_ID.LOCATION.CONNECTION_NAME` OPTIONS (
  uri="https://spanner.googleapis.com/projects/PROJECT_ID/instances/INSTANCE_ID/databases/DATABASE_ID",
  format='CLOUD_SPANNER',
  spanner_options="""{ "table": "SPANNER_TABLE_NAME" }"""
)
AS SELECT * FROM my_bq_dataset.table1;
```

請替換下列項目：

* `PROJECT_ID`：您 Google Cloud 專案的名稱。
* `LOCATION`：您建立連線的位置，例如 `us`。
* `CONNECTION_NAME`：用於執行匯出的連線名稱，例如 `myconnection`。
* `INSTANCE_ID`：Spanner 資料庫執行個體的名稱。
* `DATABASE_ID`：Spanner 資料庫的名稱。
* `SPANNER_TABLE_NAME`：現有目的地 Spanner 資料表的名稱。

## 持續匯出

如要持續處理匯出查詢，請參閱[建立持續查詢](https://docs.cloud.google.com/bigquery/docs/continuous-queries?hl=zh-tw)的操作說明和[程式碼範例](https://docs.cloud.google.com/bigquery/docs/continuous-queries?hl=zh-tw#spanner-example)。

## 匯出最佳化

如要盡量縮短從 BigQuery 匯出記錄至 Spanner 的時間，可以嘗試下列做法：

* [增加 Spanner 目的地執行個體中的節點數量](https://docs.cloud.google.com/spanner/docs/compute-capacity?hl=zh-tw)。在匯出作業的初期，增加執行個體中的節點數量可能不會立即提高匯出輸送量。Spanner 執行[以負載為準的分割](https://docs.cloud.google.com/spanner/docs/schema-and-data-model?hl=zh-tw#load-based_splitting)時，可能會稍微延遲。依負載進行分割後，匯出作業的處理量會增加並趨於穩定。使用 `EXPORT DATA` 陳述式批次處理資料，以最佳化 Spanner 的寫入作業。詳情請參閱「[成效總覽](https://docs.cloud.google.com/spanner/docs/performance?hl=zh-tw)」。
* 在 [`spanner_options`](#spanner_options) 中指定 `HIGH` 優先順序。如果 Spanner 執行個體已啟用[自動調度資源](https://docs.cloud.google.com/spanner/docs/autoscaling-overview?hl=zh-tw)，設定 `HIGH` 優先順序有助於確保 CPU 使用率達到觸發調度資源的必要門檻。這樣一來，自動配置器就能根據匯出負載新增運算資源，進而提升整體匯出處理量。

  **注意：** 使用 `HIGH` 優先順序可能會導致同一 Spanner 執行個體服務的其他工作負載效能大幅降低。只有在 Spanner 執行個體專用於這項匯出作業，或是不會受到效能影響的其他工作負載時，才考慮使用 `HIGH` 優先順序。

  以下範例顯示設為 `HIGH` 優先順序的 Spanner 匯出指令：

  ```
  EXPORT DATA OPTIONS (
    uri="https://spanner.googleapis.com/projects/PROJECT_ID/instances/INSTANCE_ID/databases/DATABASE_ID",
    format='CLOUD_SPANNER',
    spanner_options="""{ "table": "TABLE_NAME", "priority": "LOW" }"""
  )
  ```
* 避免排序查詢結果。如果結果集包含所有主鍵欄，匯出工具會自動排序目的地資料表的主鍵，以簡化寫入作業並減少爭用。

  如果目的地表格的主鍵包含產生的資料欄，請將產生的資料欄運算式新增至查詢，確保匯出的資料經過適當排序和批次處理。

  舉例來說，在下列 Spanner 結構定義中，`SaleYear` 和 `SaleMonth` 是構成 Spanner 主鍵開頭的產生資料欄：

  ```
  CREATE TABLE Sales (
    SaleId STRING(36) NOT NULL,
    ProductId INT64 NOT NULL,
    SaleTimestamp TIMESTAMP NOT NULL,
    Amount FLOAT64,
    -- Generated columns
    SaleYear INT64 AS (EXTRACT(YEAR FROM SaleTimestamp)) STORED,
    SaleMonth INT64 AS (EXTRACT(MONTH FROM SaleTimestamp)) STORED,
  ) PRIMARY KEY (SaleYear, SaleMonth, SaleId);
  ```

  從 BigQuery 匯出資料至 Spanner 資料表時，如果主鍵使用產生的資料欄，建議 (但非必要) 在 `EXPORT DATA` 查詢中加入這些產生資料欄的運算式。這樣 BigQuery 就能正確預先排序資料，這對有效率地批次處理資料並寫入 Spanner 至關重要。`EXPORT DATA` 陳述式中產生的資料欄值不會在 Spanner 中提交，因為這些值是由 Spanner 自動產生，但會用於最佳化匯出作業。

  以下範例會將資料匯出至 Spanner `Sales` 資料表，該資料表的主鍵使用產生的資料欄。為提升寫入效能，查詢會包含與產生的 `SaleYear` 和 `SaleMonth` 資料欄相符的 `EXTRACT` 運算式，讓 BigQuery 在匯出前預先排序資料：

  ```
  EXPORT DATA OPTIONS (
    uri="https://spanner.googleapis.com/projects/PROJECT_ID/instances/INSTANCE_ID/databases/DATABASE_ID",
    format='CLOUD_SPANNER',
    spanner_options="""{ "table": "Sales" }"""
  )
  AS SELECT
    s.SaleId,
    s.ProductId,
    s.SaleTimestamp,
    s.Amount,
    -- Add expressions that match the generated columns in the Spanner PK
    EXTRACT(YEAR FROM s.SaleTimestamp) AS SaleYear,
    EXTRACT(MONTH FROM s.SaleTimestamp) AS SaleMonth
  FROM my_dataset.sales_export AS s;
  ```
* 為避免工作長時間執行，請依分區匯出資料。使用分區鍵 (例如查詢中的時間戳記) 將 BigQuery 資料分片：

  ```
  EXPORT DATA OPTIONS (
    uri="https://spanner.googleapis.com/projects/PROJECT_ID/instances/INSTANCE_ID/databases/DATABASE_ID",
    format='CLOUD_SPANNER',
    spanner_options="""{ "table": "TABLE_NAME", "priority": "MEDIUM" }"""
  )
  AS SELECT *
  FROM 'mydataset.table1' d
  WHERE
  d.timestamp >= TIMESTAMP '2025-08-28T00:00:00Z' AND
  d.timestamp < TIMESTAMP '2025-08-29T00:00:00Z';
  ```

  這樣查詢就能在 6 小時的工作執行時間內完成。如要進一步瞭解這些限制，請參閱「[查詢工作限制](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#query_jobs)」。
* 如要提升資料載入效能，請在匯入資料的 Spanner 表格中捨棄索引。然後在匯入完成後重新建立。
* 建議您先從一個 Spanner 節點 (1000 個處理器單元) 和最少的 BigQuery 運算單元預留開始。例如 100 個運算單元，或 0 個基準運算單元 (搭配自動調度資源)。如果匯出資料量小於 100 GB，這項設定通常會在 6 小時的工作限制內完成。如要匯出超過 100 GB 的資料，請視需要擴充 Spanner 節點和 BigQuery 運算單元預留，以提高處理量。每個節點的處理量約為 5 MiB/秒。

## 定價

使用 `EXPORT DATA` 陳述式將資料匯出至 Spanner 時，系統會按照 [BigQuery 容量運算定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#capacity_compute_analysis_pricing)計費。

如要使用持續查詢功能，將資料持續匯出至 Spanner，您必須擁有 [BigQuery Enterprise 或 Enterprise Plus 版](https://docs.cloud.google.com/bigquery/docs/editions-intro?hl=zh-tw)的運算單元預留項目，以及使用 `CONTINUOUS` 工作類型的[預留項目指派作業](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#assignments)。

如果 BigQuery 匯出至 Spanner 的資料跨越區域界線，系統會按照資料擷取費率收費。詳情請參閱 [BigQuery 定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#data_extraction_pricing)。為避免資料移轉費用，請確保 BigQuery 匯出作業與 Spanner [預設領導者](https://docs.cloud.google.com/spanner/docs/instance-configurations?hl=zh-tw#configure-leader-region)位於相同區域。

匯出資料之後，系統會因您在 Spanner 中儲存資料而向您收取費用。詳情請參閱 [Spanner 定價](https://cloud.google.com/spanner/pricing?hl=zh-tw#storage)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-08 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-08 (世界標準時間)。"],[],[]]