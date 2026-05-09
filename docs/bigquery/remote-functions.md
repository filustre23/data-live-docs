Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 使用遠端函式

BigQuery 遠端函式可讓您使用 SQL 和 JavaScript 以外的語言，或使用 BigQuery[使用者定義函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/user-defined-functions?hl=zh-tw)不允許的程式庫或服務，實作函式。

## 總覽

BigQuery 遠端函式可直接整合 [Cloud Run 函式](https://docs.cloud.google.com/functions/docs/concepts/overview?hl=zh-tw)和 [Cloud Run](https://docs.cloud.google.com/run/docs/overview/what-is-cloud-run?hl=zh-tw)，讓您將 GoogleSQL 功能與 BigQuery 以外的軟體整合。您可以使用 BigQuery 遠端函式，以任何支援的語言在 Cloud Run 函式或 Cloud Run 中部署函式，然後從 GoogleSQL 查詢中叫用這些函式。

### 工作流程

1. 在 Cloud Run 函式或 Cloud Run 中建立 HTTP 端點。
2. 在 BigQuery 中建立遠端函式。
   1. 建立 `CLOUD_RESOURCE` 類型的連線。
   2. 建立遠端函式。
3. 在查詢中使用遠端函式，就像使用任何其他使用者定義函式一樣。

## 限制

* 遠端函式僅支援下列其中一種[資料類型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw)做為引數類型或傳回類型：

  + 布林值
  + 位元組
  + 數字
  + 字串
  + 日期
  + 日期時間
  + 時間
  + 時間戳記
  + JSON

  遠端函式不支援 `ARRAY`、`STRUCT`、`INTERVAL` 或 `GEOGRAPHY` 型別。
* 您無法建立資料表值遠端函式。
* 建立具體化檢視表時，無法使用遠端函式。
* 系統一律會假設遠端函式的傳回值具有不確定性，因此不會快取呼叫遠端函式的查詢結果。
* 即使收到成功的回應，您也可能會看到系統重複將相同資料傳送至端點，這是因為發生暫時性網路錯誤或 BigQuery 內部錯誤。
* 如果因短路而略過部分資料列的遠端函式評估作業 (例如在[條件式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/conditional_expressions?hl=zh-tw)或含有 `WHEN [NOT] MATCHED` 的 [`MERGE` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/dml-syntax?hl=zh-tw#merge_statement)中)，系統不會對遠端函式使用批次處理。在此情況下，[HTTP 要求主體](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/remote-functions?hl=zh-tw#input_format)中的 `calls` 欄位只有一個元素。
* 如果與遠端函式相關聯的資料集透過[跨區域資料集複製](https://docs.cloud.google.com/bigquery/docs/data-replication?hl=zh-tw)作業複製到目的地區域，則只能在建立遠端函式的區域中查詢該函式。

## 建立端點

如要建立可實作商業邏輯的遠端函式，您必須使用 Cloud Run functions 或 Cloud Run 建立 HTTP 端點。端點必須能夠在單一 HTTP POST 要求中處理一批資料列，並以 HTTP 回應的形式傳回該批資料的結果。

如果您使用 [BigQuery DataFrames](https://dataframes.bigquery.dev/) 建立遠端函式，則不必手動建立 HTTP 端點，服務會自動為您建立。

如要瞭解如何編寫、部署、測試及維護 Cloud Run 函式，請參閱 [Cloud Run functions 教學課程](https://docs.cloud.google.com/functions/docs/tutorials/http?hl=zh-tw)和其他 [Cloud Run functions 說明文件](https://docs.cloud.google.com/functions/docs/writing/http?hl=zh-tw)。

請參閱[Cloud Run 快速入門導覽課程](https://docs.cloud.google.com/run/docs/quickstarts?hl=zh-tw#build-and-deploy-a-web-service)，以及其他 [Cloud Run 說明文件](https://docs.cloud.google.com/run/docs/how-to?hl=zh-tw)，瞭解如何編寫、部署、測試及維護 Cloud Run 服務。

建議您保留預設驗證，不要允許未經驗證的 Cloud Run function 或 Cloud Run 服務叫用。

### 輸入格式

BigQuery 會傳送 HTTP POST 要求，並以 JSON 主體採用下列格式：

| 欄位名稱 | 說明 | 欄位類型 |
| --- | --- | --- |
| requestId | 要求的 ID。在 GoogleSQL 查詢中，傳送至這個端點的多個要求中，這個值必須是唯一的。 | 一律提供。字串。 |
| 來電者 | 呼叫遠端函式的 GoogleSQL 查詢工作完整資源名稱。 | 一律提供。String。 |
| sessionUser | 執行 GoogleSQL 查詢的使用者電子郵件地址。 | 一律提供。字串。 |
| userDefinedContext | 在 BigQuery 中建立遠端函式時使用的使用者定義情境。 | 選用。含有鍵/值組合的 JSON 物件。 |
| 通話 | 一批輸入資料。 | 一律提供。JSON 陣列。 每個元素本身都是 JSON 陣列，也就是一個遠端函式呼叫的 JSON 編碼引數清單。 |

要求範例：

```
{
 "requestId": "124ab1c",
 "caller": "//bigquery.googleapis.com/projects/myproject/jobs/myproject:US.bquxjob_5b4c112c_17961fafeaf",
 "sessionUser": "test-user@test-company.com",
 "userDefinedContext": {
  "key1": "value1",
  "key2": "v2"
 },
 "calls": [
  [null, 1, "", "abc"],
  ["abc", "9007199254740993", null, null]
 ]
}
```

### 輸出格式

BigQuery 預期端點會傳回下列格式的 HTTP 回應，否則 BigQuery 無法使用該回覆，且呼叫遠端函式的查詢會失敗。

|  |  |  |
| --- | --- | --- |
| 欄位名稱 | 說明 | 值範圍 |
| 回覆 | 一批回傳值。 | 這是成功回應的必要條件。JSON 陣列。 每個元素都對應至外部函式的 JSON 編碼回傳值。  陣列大小必須與 HTTP 要求中 `calls` 的 JSON 陣列大小相符。舉例來說，如果 `calls` 中的 JSON 陣列有 4 個元素，這個 JSON 陣列也必須有 4 個元素。 |
| errorMessage | 傳回 HTTP 回應代碼 (非 200) 時的錯誤訊息。對於無法重試的錯誤，我們會將此錯誤做為 BigQuery 工作錯誤訊息的一部分，傳回給使用者。 | 選用。字串。大小不得超過 1 KB。 |

成功回應範例：

```
{
  "replies": [
    1,
    0
  ]
}
```

失敗的回應範例如下：

```
{
  "errorMessage": "Received but not expected that the argument 0 be null".
}
```

#### HTTP 回應碼

如果回覆成功，端點應傳回 HTTP 回應代碼 200。
如果 BigQuery 收到任何其他值，就會將回應視為失敗，並在 HTTP 回應代碼為 408、429、500、503 或 504 時重試，直到達到內部限制為止。

### SQL 資料類型的 JSON 編碼

HTTP 要求/回應中的 JSON 編碼會遵循 [現有的 BigQuery JSON 編碼](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/json_functions?hl=zh-tw#json_encodings)，適用於 [TO\_JSON\_STRING 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/json_functions?hl=zh-tw#to_json_string)。

### Cloud Run 函式程式碼範例

下列 Python 程式碼範例會實作遠端函式的所有整數引數加法。這個函式會處理要求，並使用批次呼叫的引數，然後在回應中傳回所有結果。

```
import functions_framework

from flask import jsonify

# Max INT64 value encoded as a number in JSON by TO_JSON_STRING. Larger values are encoded as
# strings.
# See https://cloud.google.com/bigquery/docs/reference/standard-sql/json_functions#json_encodings
_MAX_LOSSLESS=9007199254740992

@functions_framework.http
def batch_add(request):
  try:
    return_value = []
    request_json = request.get_json()
    calls = request_json['calls']
    for call in calls:
      return_value.append(sum([int(x) if isinstance(x, str) else x for x in call if x is not None]))
    replies = [str(x) if x > _MAX_LOSSLESS or x < -_MAX_LOSSLESS else x for x in return_value]
    return_json = jsonify( { "replies":  replies } )
    return return_json
  except Exception as e:
    return jsonify( { "errorMessage": str(e) } ), 400
```

假設函式部署在專案 `my_gcf_project` 的 `us-east1` 區域，且函式名稱為 `remote_add`，則可透過端點 `https://us-east1-my_gcf_project.cloudfunctions.net/remote_add` 存取。

### Cloud Run 程式碼範例

下列 Python 程式碼範例會實作網路服務，可建構及部署至 Cloud Run，提供相同功能。

```
import os

from flask import Flask, request, jsonify

# Max INT64 value encoded as a number in JSON by TO_JSON_STRING. Larger values are encoded as
# strings.
# See https://cloud.google.com/bigquery/docs/reference/standard-sql/json_functions#json_encodings
_MAX_LOSSLESS=9007199254740992

app = Flask(__name__)

@app.route("/", methods=['POST'])
def batch_add():
  try:
    return_value = []
    request_json = request.get_json()
    calls = request_json['calls']
    for call in calls:
      return_value.append(sum([int(x) if isinstance(x, str) else x for x in call if x is not None]))
    replies = [str(x) if x > _MAX_LOSSLESS or x < -_MAX_LOSSLESS else x for x in return_value]
    return jsonify( { "replies" :  replies } )
  except Exception as e:
    return jsonify( { "errorMessage": str(e) } ), 400

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
```

請參閱[指南](https://docs.cloud.google.com/run/docs/quickstarts/build-and-deploy/deploy-python-service?hl=zh-tw)，瞭解如何建構及部署程式碼。

假設 Cloud Run 服務部署在專案 `my_gcf_project` 的 `us-east1` 區域，且服務名稱為 `remote_add`，則可透過端點 `https://remote_add-<project_id_hash>-ue.a.run.app` 存取。

## 建立遠端函式

BigQuery 會使用 `CLOUD_RESOURCE` 連線與 Cloud Run 函式互動。如要建立遠端函式，請務必建立 `CLOUD_RESOURCE` 連線。如果您使用 [BigQuery DataFrames](https://dataframes.bigquery.dev/) 建立遠端函式，且已獲授專案 IAM 管理員 (`roles/resourcemanager.projectIamAdmin`) 角色，則不必手動建立連線並授予存取權，服務會自動為您完成這些作業。

### 建立連線

您必須有 Cloud 資源連結，才能連線至 Cloud Run 函式和 Cloud Run。

如果已設定預設連線，或您具備 BigQuery 管理員角色，可以略過這個步驟。

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

   每項專案只需要執行一次這個指令，且可以在任何目錄中執行。

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

### 設定存取權

您必須授予新連線 Cloud Run 函式或 Cloud Run 服務的唯讀權限。不建議允許未經驗證的 Cloud Run 函式或 Cloud Run 服務叫用。

如要授予角色，請按照下列步驟操作：

1. 前往「IAM & Admin」(IAM 與管理) 頁面。

   [前往「IAM & Admin」(IAM 與管理)](https://console.cloud.google.com/project/_/iam-admin?hl=zh-tw)
2. 按一下「新增」person\_add。

   「新增主體」對話方塊隨即開啟。
3. 在「新增主體」欄位，輸入先前複製的服務帳戶 ID。
4. 在「選取角色」欄位中，選取下列其中一個選項：

   * 如果您使用第 1 代 Cloud Run 函式，請選擇「Cloud Function」(Cloud 函式)，然後選取「Cloud Function Invoker role」(Cloud Function 叫用者角色)。
   * 如果您使用第 2 代 Cloud Run 函式，請選擇「Cloud Run」，然後選取「Cloud Run Invoker role」(Cloud Run 叫用者角色)。
   * 如果您使用 Cloud Run 服務，請選擇「Cloud Run」，然後選取「Cloud Run Invoker role」(Cloud Run 叫用者角色)。
5. 按一下 [儲存]。

### 建立遠端函式

如要建立遠端函式，請按照下列指示操作：

### SQL

在 BigQuery 中執行下列
[`CREATE FUNCTION`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#create_function_statement)
陳述式：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列陳述式：

   ```
   CREATE FUNCTION PROJECT_ID.DATASET_ID.remote_add(x INT64, y INT64) RETURNS INT64
   REMOTE WITH CONNECTION PROJECT_ID.LOCATION.CONNECTION_NAME
   OPTIONS (
     endpoint = 'ENDPOINT_URL'
   )
   ```

   請替換下列項目：

   * `DATASET_ID`：BigQuery 資料集的 ID。
   * `ENDPOINT_URL`：Cloud Run 函式或 Cloud Run 遠端函式端點的網址。
3. 按一下「執行」play\_circle。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

### BigQuery DataFrames

1. 啟用必要 API，並確認您已獲派必要角色，詳情請參閱[遠端函式](https://docs.cloud.google.com/bigquery/docs/dataframes-custom-python-functions?hl=zh-tw#remote-function-requirements)的「**需求條件**」一節。
2. 使用 [`remote_function` 修飾符](https://dataframes.bigquery.dev/reference/api/bigframes.pandas.remote_function.html#bigframes.pandas.remote_function)：

   ```
   import bigframes.pandas as bpd

   # Set BigQuery DataFrames options
   bpd.options.bigquery.project = your_gcp_project_id
   bpd.options.bigquery.location = "US"

   # BigQuery DataFrames gives you the ability to turn your custom scalar
   # functions into a BigQuery remote function. It requires the GCP project to
   # be set up appropriately and the user having sufficient privileges to use
   # them. One can find more details about the usage and the requirements via
   # `help` command.
   help(bpd.remote_function)

   # Read a table and inspect the column of interest.
   df = bpd.read_gbq("bigquery-public-data.ml_datasets.penguins")
   df["body_mass_g"].head(10)

   # Define a custom function, and specify the intent to turn it into a remote
   # function. It requires a BigQuery connection. If the connection is not
   # already created, BigQuery DataFrames will attempt to create one assuming
   # the necessary APIs and IAM permissions are setup in the project. In our
   # examples we will be letting the default connection `bigframes-default-connection`
   # be used. We will also set `reuse=False` to make sure we don't
   # step over someone else creating remote function in the same project from
   # the exact same source code at the same time. Let's try a `pandas`-like use
   # case in which we want to apply a user defined scalar function to every
   # value in a `Series`, more specifically bucketize the `body_mass_g` value
   # of the penguins, which is a real number, into a category, which is a
   # string.
   @bpd.remote_function(
       reuse=False,
       cloud_function_service_account="default",
   )
   def get_bucket(num: float) -> str:
       if not num:
           return "NA"
       boundary = 4000
       return "at_or_above_4000" if num >= boundary else "below_4000"

   # Then we can apply the remote function on the `Series` of interest via
   # `apply` API and store the result in a new column in the DataFrame.
   df = df.assign(body_mass_bucket=df["body_mass_g"].apply(get_bucket))

   # This will add a new column `body_mass_bucket` in the DataFrame. You can
   # preview the original value and the bucketized value side by side.
   df[["body_mass_g", "body_mass_bucket"]].head(10)

   # The above operation was possible by doing all the computation on the
   # cloud. For that, there is a google cloud function deployed by serializing
   # the user code, and a BigQuery remote function created to call the cloud
   # function via the latter's http endpoint on the data in the DataFrame.

   # The BigQuery remote function created to support the BigQuery DataFrames
   # remote function can be located via a property `bigframes_remote_function`
   # set in the remote function object.
   print(f"Created BQ remote function: {get_bucket.bigframes_remote_function}")

   # The cloud function can be located via another property
   # `bigframes_cloud_function` set in the remote function object.
   print(f"Created cloud function: {get_bucket.bigframes_cloud_function}")

   # Warning: The deployed cloud function may be visible to other users with
   # sufficient privilege in the project, so the user should be careful about
   # having any sensitive data in the code that will be deployed as a remote
   # function.

   # Let's continue trying other potential use cases of remote functions. Let's
   # say we consider the `species`, `island` and `sex` of the penguins
   # sensitive information and want to redact that by replacing with their hash
   # code instead. Let's define another scalar custom function and decorate it
   # as a remote function. The custom function in this example has external
   # package dependency, which can be specified via `packages` parameter.
   @bpd.remote_function(
       reuse=False,
       packages=["cryptography"],
       cloud_function_service_account="default",
   )
   def get_hash(input: str) -> str:
       from cryptography.fernet import Fernet

       # handle missing value
       if input is None:
           input = ""

       key = Fernet.generate_key()
       f = Fernet(key)
       return f.encrypt(input.encode()).decode()

   # We can use this remote function in another `pandas`-like API `map` that
   # can be applied on a DataFrame
   df_redacted = df[["species", "island", "sex"]].map(get_hash)
   df_redacted.head(10)
   ```

您必須在建立遠端函式的資料集上擁有 `bigquery.routines.create` 權限，並在遠端函式使用的連線上擁有 `bigquery.connections.delegate` 權限 (可透過 BigQuery 連線管理員角色取得)。

#### 提供使用者定義的情境

您可以在 `OPTIONS` 中指定 `user_defined_context` 做為鍵/值組合，這會成為傳送至端點的每個 HTTP 要求的一部分。透過使用者定義的情境，您可以建立多個遠端函式，但重複使用單一端點，根據傳遞至該端點的情境提供不同行為。

下列範例會建立兩個遠端函式，使用相同端點加密及解密 `BYTES` 資料。

```
CREATE FUNCTION `PROJECT_ID.DATASET_ID`.encrypt(x BYTES)
RETURNS BYTES
REMOTE WITH CONNECTION `PROJECT_ID.LOCATION.CONNECTION_NAME`
OPTIONS (
  endpoint = 'ENDPOINT_URL',
  user_defined_context = [("mode", "encryption")]
)

CREATE FUNCTION `PROJECT_ID.DATASET_ID`.decrypt(x BYTES)
RETURNS BYTES
REMOTE WITH CONNECTION `PROJECT_ID.LOCATION.CONNECTION_NAME`
OPTIONS (
  endpoint = 'ENDPOINT_URL',
  user_defined_context = [("mode", "decryption")]
)
```

#### 限制批次要求中的資料列數

您可以在 `OPTIONS` 中指定 `max_batching_rows`，做為每個 HTTP 要求的最大資料列數，避免 [Cloud Run 函式逾時](https://docs.cloud.google.com/functions/docs/concepts/exec?hl=zh-tw#timeout)。如果指定 `max_batching_rows`，BigQuery 會判斷批次中的資料列數量，上限為 `max_batching_rows`。如未指定，BigQuery 會自動決定要批次處理的資料列數量。

## 在查詢中使用遠端函式

請務必[授予 Cloud Run 函式的權限](#grant_permission_on_function)，讓 BigQuery 服務帳戶 (與遠端函式連結相關聯) 可以存取該函式。

您也必須在遠端函式所在的資料集上擁有 `bigquery.routines.get` 權限，以及在遠端函式使用的連線上擁有 `bigquery.connections.use` 權限 (可透過 `BigQuery Connection User` 角色取得)。

您可以在查詢中使用遠端函式，就像[使用者定義的函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/user-defined-functions?hl=zh-tw)一樣。

舉例來說，您可以在範例查詢中使用 `remote_add` 函式：

```
SELECT
  val,
  `PROJECT_ID.DATASET_ID`.remote_add(val, 2)
FROM
  UNNEST([NULL,2,3,5,8]) AS val;
```

這個範例會產生下列輸出內容：

```
+------+-----+
|  val | f0_ |
+------+-----+
| NULL |   2 |
|    2 |   4 |
|    3 |   5 |
|    5 |   7 |
|    8 |  10 |
+------+-----+
```

**注意：** 如要使用具有 `internal traffic`
[連入設定](https://docs.cloud.google.com/functions/docs/networking/network-settings?hl=zh-tw#ingress_settings)的端點，您可以透過相同的 Cloud Run 函式端點專案執行 BigQuery 查詢，或[設定 VPC-SC perimeter](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/remote-functions?hl=zh-tw#using_vpc_service_controls)。

## 支援的地區

BigQuery 中的位置類型有兩種：

* 「地區」是特定的地理位置，例如倫敦。
* 「多地區」是指包含兩個及以上地理位置的大型地理區域，例如美國。

### 單一地區

在 BigQuery 單一區域資料集中，您只能建立使用相同區域中部署的 Cloud Run 函式的遠端函式。例如：

* BigQuery 單一區域 `us-east4` 中的遠端函式只能使用 `us-east4` 中的 Cloud Run 函式。

因此，在單一區域中，只有同時支援 Cloud Run 函式和 BigQuery 的區域，才能使用遠端函式。

### 多區域

在 BigQuery 多區域 (`US`、`EU`) 資料集中，您只能建立使用 Cloud Run 函式的遠端函式，而 Cloud Run 函式必須部署在相同大型地理區域 (美國、歐盟) 內的區域。例如：

* BigQuery `US` 多區域中的遠端函式只能使用部署在美國地理區域中任一單一區域的 Cloud Run 函式，例如 `us-central1`、`us-east4`、`us-west2` 等。
* BigQuery `EU` 多區域的遠端函式只能使用部署在歐盟[成員國](https://europa.eu/european-union/about-eu/countries_en)任何單一區域的 Cloud Run 函式，例如 `europe-north1`、`europe-west3` 等。

如要進一步瞭解 BigQuery 單一地區與多地區，請參閱[資料集位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw#supported_locations)頁面。如要進一步瞭解 Cloud Run functions 區域，請參閱「[Cloud Run functions 據點](https://docs.cloud.google.com/functions/docs/locations?hl=zh-tw)」頁面。

### 連線

無論是單一區域位置或多區域位置，您都只能在與所用連線相同的位置建立遠端函式。舉例來說，如要在 `US` 多區域中建立遠端函式，請使用位於 `US` 多區域的連線。

## 定價

* 適用標準 [BigQuery 定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw)。
* 此外，使用這項功能可能會產生 Cloud Run 函式和 Cloud Run 的費用。詳情請參閱 [Cloud Run functions](https://cloud.google.com/functions/pricing?hl=zh-tw) 和 [Cloud Run](https://cloud.google.com/run/pricing?hl=zh-tw) 定價頁面。

## 使用 VPC Service Controls

[VPC Service Controls](https://docs.cloud.google.com/vpc-service-controls?hl=zh-tw) 是一項 Google Cloud 功能，可用來設定安全 perimeter 以防範資料竊取。如要搭配使用 VPC Service Controls 與遠端函式來加強安全性，或使用具有`internal traffic`
[輸入設定](https://docs.cloud.google.com/functions/docs/networking/network-settings?hl=zh-tw#ingress_settings)的端點，請按照 [VPC Service Controls 指南](https://docs.cloud.google.com/vpc-service-controls/docs/create-service-perimeters?hl=zh-tw#create_a_service_perimeter)操作：

1. 建立 service perimeter。
2. 將使用遠端函式的查詢所屬 BigQuery 專案新增至安全防護範圍。
3. 將端點專案新增至範圍，並根據端點類型在受限制的服務中設定 `Cloud Functions API` 或 `Cloud Run API`。詳情請參閱「[Cloud Run 函式 VPC Service Controls](https://docs.cloud.google.com/functions/docs/securing/using-vpc-service-controls?hl=zh-tw)」和「[Cloud Run VPC Service Controls](https://docs.cloud.google.com/run/docs/securing/using-vpc-service-controls?hl=zh-tw)」。

## 遠端函式的最佳做法

* 預先篩選輸入內容：如果輸入內容在傳遞到遠端函式之前，能夠輕易地進行篩選，您查詢的執行速度可能會更快，費用也可能會更便宜。
* 確保 Cloud Run 函式可擴充。可擴充性取決於[執行個體數量下限](https://docs.cloud.google.com/functions/docs/configuring/min-instances?hl=zh-tw)、[執行個體數量上限](https://docs.cloud.google.com/functions/docs/configuring/max-instances?hl=zh-tw)和[並行](https://docs.cloud.google.com/functions/docs/configuring/concurrency?hl=zh-tw)。

  + 盡可能為 Cloud Run 函式的執行個體數量上限使用預設值。
  + 請注意，第 1 代 HTTP Cloud Run 函式沒有預設限制。為避免第 1 代 HTTP Cloud Run 函式在測試或正式環境中無限制擴充，建議[設定限制](https://docs.cloud.google.com/functions/docs/configuring/max-instances?hl=zh-tw#setting_maximum_instances_limits)，例如 3000。
* 請按照其他 [Cloud Run 函式提示](https://docs.cloud.google.com/functions/docs/bestpractices/tips?hl=zh-tw)操作，提升效能。與高延遲 Cloud Run 函式互動的遠端函式查詢可能會因逾時而失敗。
* 實作端點，針對失敗的回應傳回正確的 HTTP 回應代碼和酬載。

  + 如要盡量減少 BigQuery 的重試次數，請針對失敗的回應使用 408、429、500、503 和 504 以外的 HTTP 回應碼，並確保在函式程式碼中擷取所有例外狀況。否則，HTTP 服務架構可能會針對任何未接收的例外狀況自動傳回 500。如果 BigQuery 重試失敗的資料分區或查詢，您可能仍會看到重試的 HTTP 要求。
  + 端點應以定義的格式傳回 JSON 酬載，表示回應失敗。雖然並非必要，但這有助於 BigQuery 區分失敗的回應是來自函式實作，還是 Cloud Run functions/Cloud Run 的基礎架構。如果是後者，BigQuery 可能會使用不同的內部限制重試。

## 配額

請參閱下列資訊，排解遠端函式的配額問題。

### 包含遠端函式的並行查詢數量上限

如果含有遠端函式的並行查詢數量超過上限，BigQuery 就會傳回這項錯誤。

如要進一步瞭解遠端函式限制，請參閱「[遠端函式](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#remote_function_limits)」。

**錯誤訊息**

```
Exceeded rate limits: too many concurrent queries with remote functions for
this project
```

這項上限可以提高。請先嘗試解決方法和最佳做法。

#### 診斷

如要瞭解包含[遠端函式](https://docs.cloud.google.com/bigquery/docs/remote-functions?hl=zh-tw)的並行查詢限制，請參閱「[遠端函式限制](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#remote_function_limits)」。

#### 解析度

* 使用遠端函式時，請遵循[遠端函式的最佳做法](https://docs.cloud.google.com/bigquery/docs/remote-functions?hl=zh-tw#best_practices_for_remote_functions)。
* 如要要求增加配額，請與[支援團隊](https://docs.cloud.google.com/bigquery/docs/getting-support?hl=zh-tw)或[銷售人員](https://cloud.google.com/contact?hl=zh-tw)聯絡。審查及處理要求可能需要幾天的時間。建議在要求中說明優先順序、用途和專案 ID。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-09 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-09 (世界標準時間)。"],[],[]]