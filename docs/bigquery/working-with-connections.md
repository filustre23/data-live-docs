Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 管理連結

本文說明如何查看、列出、共用、編輯、刪除 BigQuery 連線，以及排解相關問題。

BigQuery 管理員可以建立及管理連線，用於連結服務和外部資料來源。BigQuery 分析師會使用這些連線，對外部資料來源提交查詢，不必將資料移至或複製到 BigQuery。您可以建立下列類型的連結：

* [Amazon S3 連線](https://docs.cloud.google.com/bigquery/docs/omni-aws-create-connection?hl=zh-tw)
* [Apache Spark 連線](https://docs.cloud.google.com/bigquery/docs/connect-to-spark?hl=zh-tw)
* [Blob 儲存體連線](https://docs.cloud.google.com/bigquery/docs/omni-azure-create-connection?hl=zh-tw)
* [Cloud 資源連結](https://docs.cloud.google.com/bigquery/docs/create-cloud-resource-connection?hl=zh-tw)：用於連結 Cloud Storage 資料及實作[遠端函式](https://docs.cloud.google.com/bigquery/docs/remote-functions?hl=zh-tw)
* [Spanner 連線](https://docs.cloud.google.com/bigquery/docs/connect-to-spanner?hl=zh-tw)
* [Cloud SQL 連線](https://docs.cloud.google.com/bigquery/docs/connect-to-sql?hl=zh-tw)
* [AlloyDB 連線](https://docs.cloud.google.com/bigquery/docs/connect-to-alloydb?hl=zh-tw)

如要為專案建立預設連線，請參閱「[預設連線總覽](https://docs.cloud.google.com/bigquery/docs/default-connections?hl=zh-tw)」。

**提示：** 您也可以使用「Pipelines & Connections」(管道和連線) 頁面，透過[簡化的 BigQuery 專屬工作流程](https://docs.cloud.google.com/bigquery/docs/pipeline-connection-page?hl=zh-tw)建立及管理連線。這項功能為[預先發布版](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages)。

## 事前準備

* 確認[網路連線](https://docs.cloud.google.com/bigquery/docs/connections-api-intro?hl=zh-tw)正常運作。連線[依類型而定](https://docs.cloud.google.com/bigquery/docs/connections-api-intro?hl=zh-tw#connection_types)，並取決於連結的外部資料來源。
* 啟用 BigQuery Connection API。

  [啟用 API](https://console.cloud.google.com/apis/library/bigqueryconnection.googleapis.com?hl=zh-tw)
* 確認您可以查看[專案中的服務帳戶清單](https://docs.cloud.google.com/iam/docs/service-accounts-list-edit?hl=zh-tw#listing)。BigQuery 會建立並使用[服務帳戶](https://docs.cloud.google.com/iam/docs/service-agents?hl=zh-tw)，連線至外部資料來源。建立連線時，系統會代您建立 [Google Cloud代管的 Identity and Access Management (IAM) 服務帳戶](https://docs.cloud.google.com/iam/docs/service-account-types?hl=zh-tw#google-managed)。如要查看附加至特定連線的服務帳戶，請[查看連線詳細資料](https://docs.cloud.google.com/bigquery/docs/working-with-connections?hl=zh-tw#view-connections)。

### 必要的角色

如要取得管理連線所需的權限，請要求管理員授予您下列 IAM 角色：

* [查看連線詳細資料](#view-connections)：資料集的 [BigQuery 連線使用者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.connectionUser)  (`roles/bigquery.connectionUser`)
* [列出所有連線](#list-connections)：資料集的 [BigQuery 連線使用者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.connectionUser)  (`roles/bigquery.connectionUser`)
* [共用連線](#share-connections)：連線的 [BigQuery 連線管理員](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.connectionAdmin)  (`roles/bigquery.connectionAdmin`)
* [編輯連線](#edit-connections)：連線的 [BigQuery 連線管理員](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.connectionAdmin)  (`roles/bigquery.connectionAdmin`)
* [刪除連線](#delete-connections)：連線的 [BigQuery 連線管理員](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.connectionAdmin)  (`roles/bigquery.connectionAdmin`)

如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

您或許也能透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)，取得必要權限。

如要瞭解建立及使用預設連線所需的角色，請參閱「[必要角色和權限](https://docs.cloud.google.com/bigquery/docs/default-connections?hl=zh-tw#required_roles_and_permissions)」。

這些預先定義的角色具備執行本文件所述工作所需的權限。如要查看確切的必要權限，請展開「Required permissions」(必要權限) 部分：

#### 所需權限

* 查看連線詳細資料：`bigquery.connections.get`
* 列出所有連線：`bigquery.connections.list`
* 編輯及刪除連結：`bigquery.connections.update`
* 分享連線：`bigquery.connections.setIamPolicy`

## 列出所有連線

選取下列選項之一：

### 控制台

1. 前往「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)

   連線會列在專案的「連線」群組中。
2. 點選左側窗格中的 explore「Explorer」。

   如果沒有看到左側窗格，請按一下 last\_page「Expand left pane」(展開左側窗格)，開啟窗格。
3. 在「Explorer」窗格中，依序點選專案名稱和「Connections」(連線)，即可查看所有連線的清單。

### bq

輸入 `bq ls` 指令，並指定 `--connection` 旗標。您可以視需要指定 `--project_id` 和 `--location` 旗標，找出要列出的連線專案和位置。

```
bq ls --connection --project_id=PROJECT_ID --location=REGION
```

更改下列內容：

* `PROJECT_ID`：您的 Google Cloud 專案 ID
* `REGION`：[連線區域](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw#supported_locations)

### API

[使用 REST API 參考資料部分中的 `projects.locations.connections.list` 方法](https://docs.cloud.google.com/bigquery/docs/reference/bigqueryconnection/rest/v1/projects.locations.connections?hl=zh-tw#methods)。

### Python

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Python 設定操作說明進行操作。詳情請參閱 [BigQuery Python API 參考文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import google.api_core.exceptions
from google.cloud import bigquery_connection_v1


def list_connections(project_id: str, location: str):
    """Prints all connections in a given project and location.

    Args:
        project_id: The Google Cloud project ID.
        location: The geographic location of the connections (for example, "us", "us-central1").
    """
    client = bigquery_connection_v1.ConnectionServiceClient()

    parent = client.common_location_path(project_id, location)

    request = bigquery_connection_v1.ListConnectionsRequest(
        parent=parent,
        page_size=100,
    )

    print(f"Listing connections in project '{project_id}' and location '{location}':")

    try:
        for connection in client.list_connections(request=request):
            print(f"Connection ID: {connection.name.split('/')[-1]}")
            print(f"Friendly Name: {connection.friendly_name}")
            print(f"Has Credential: {connection.has_credential}")
            print("-" * 20)

        print("Finished listing connections.")

    except google.api_core.exceptions.InvalidArgument as e:
        print(
            f"Could not list connections. Please check that the project ID '{project_id}' "
            f"and location '{location}' are correct. Details: {e}"
        )
```

### Node.js

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Node.js 設定操作說明進行操作。詳情請參閱 [BigQuery Node.js API 參考文件](https://googleapis.dev/nodejs/bigquery/latest/index.html)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
const {ConnectionServiceClient} = require('@google-cloud/bigquery-connection');
const {status} = require('@grpc/grpc-js');

const client = new ConnectionServiceClient();

/**
 * Lists BigQuery connections in a given project and location.
 *
 * @param {string} projectId The Google Cloud project ID. for example, 'example-project-id'
 * @param {string} location The location to list connections for. for example, 'us-central1'
 */
async function listConnections(projectId, location) {
  const parent = client.locationPath(projectId, location);

  const request = {
    parent,
    pageSize: 100,
  };

  try {
    const [connections] = await client.listConnections(request, {
      autoPaginate: false,
    });

    if (connections.length === 0) {
      console.log(
        `No connections found in ${location} for project ${projectId}.`,
      );
      return;
    }

    console.log('Connections:');
    for (const connection of connections) {
      console.log(`  Name: ${connection.name}`);
      console.log(`  Friendly Name: ${connection.friendlyName}`);
    }
  } catch (err) {
    if (err.code === status.NOT_FOUND) {
      console.log(
        `Project '${projectId}' or location '${location}' not found.`,
      );
    } else {
      console.error('Error listing connections:', err);
    }
  }
}
```

### Java

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Java 設定操作說明進行操作。詳情請參閱 [BigQuery Java API 參考文件](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/overview?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import com.google.api.gax.rpc.ApiException;
import com.google.api.gax.rpc.InvalidArgumentException;
import com.google.cloud.bigquery.connection.v1.Connection;
import com.google.cloud.bigquery.connection.v1.ListConnectionsRequest;
import com.google.cloud.bigquery.connection.v1.LocationName;
import com.google.cloud.bigqueryconnection.v1.ConnectionServiceClient;
import java.io.IOException;

public class ListConnections {

  /**
   * Lists all BigQuery connections in a given project and location.
   *
   * @param projectId The Google Cloud project ID (for example, "example-project-id").
   * @param location The geographic location of the connections (for example, "us-central1").
   */
  public static void listConnections(String projectId, String location) {
    LocationName parent = LocationName.of(projectId, location);

    ListConnectionsRequest request =
        ListConnectionsRequest.newBuilder().setParent(parent.toString()).setPageSize(100).build();

    try (ConnectionServiceClient client = ConnectionServiceClient.create()) {
      System.out.printf(
          "Listing connections in project '%s' and location '%s':%n", projectId, location);

      for (Connection connection : client.listConnections(request).iterateAll()) {
        System.out.printf("Connection Name: %s%n", connection.getName());
        System.out.printf("Friendly Name: %s%n", connection.getFriendlyName());
        System.out.printf("Has Credential: %b%n", connection.getHasCredential());
      }

      System.out.println("Finished listing connections.");
    } catch (InvalidArgumentException err) {
      System.err.printf(
          "error: invalid argument listing connections in location '%s' for project '%s': %s%n",
          location, projectId, err.getMessage());
    } catch (ApiException | IOException err) {
      System.err.printf(
          "error: failed to list connections in location '%s' for project '%s': %s%n",
          location, projectId, err.getMessage());
    }
  }
```

## 查看連線詳細資料

建立連線後，您可以取得連線設定的相關資訊。設定包含您在建立移轉作業時提供的值。

選取下列選項之一：

### 控制台

1. 前往「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 連線會列在專案的「連線」群組中。
3. 點選左側窗格中的 explore「Explorer」。
4. 在「Explorer」窗格中，依序點選專案名稱和「Connections」(連線)，即可查看所有連線的清單。
5. 點選連線即可查看詳細資料。

### bq

輸入 `bq show` 指令，並指定 `--connection` 旗標。您可以視需要使用專案 ID 和連線區域，限定連線 ID。

```
bq show --connection PROJECT_ID.REGION.CONNECTION_ID
```

更改下列內容：

* `PROJECT_ID`：您的 Google Cloud 專案 ID
* `REGION`：[連線區域](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw#supported_locations)
* `CONNECTION_ID`：連線 ID

### API

使用 REST API 參考資料部分的 [`projects.locations.connections.get` 方法](https://docs.cloud.google.com/bigquery/docs/reference/bigqueryconnection/rest/v1/projects.locations.connections?hl=zh-tw#methods)。

### Python

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Python 設定操作說明進行操作。詳情請參閱 [BigQuery Python API 參考文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import google.api_core.exceptions
from google.cloud import bigquery_connection_v1

client = bigquery_connection_v1.ConnectionServiceClient()


def get_connection(project_id: str, location: str, connection_id: str):
    """Retrieves connection metadata about a specified BigQuery connection.

    A connection stores metadata about an external data source and credentials to access it.

    Args:
        project_id: The Google Cloud project ID.
        location: The geographic location of the connection (for example, "us-central1").
        connection_id: The ID of the connection to retrieve.
    """

    name = client.connection_path(project_id, location, connection_id)

    try:
        connection = client.get_connection(name=name)

        print(f"Successfully retrieved connection: {connection.name}")
        print(f"Friendly name: {connection.friendly_name}")
        print(f"Description: {connection.description}")
        if connection.cloud_sql:
            print(f"Cloud SQL instance ID: {connection.cloud_sql.instance_id}")
    except google.api_core.exceptions.NotFound:
        print(f"Connection '{name}' not found.")
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
 * Retrieves connection metadata about a specified BigQuery connection.
 *
 * A connection stores metadata about an external data source and credentials to access it.
 *
 * @param {string} projectId - Google Cloud project ID. for example, 'example-project-id'
 * @param {string} location - The location of the connection. for example, 'us-central1'
 * @param {string} connectionId - The ID of the connection to retrieve. for example, 'example_connection'
 */
async function getConnection(projectId, location, connectionId) {
  const name = client.connectionPath(projectId, location, connectionId);

  const request = {
    name,
  };

  try {
    const [connection] = await client.getConnection(request);

    console.log(`Successfully retrieved connection: ${connection.name}`);
    console.log(`  Friendly name: ${connection.friendlyName}`);
    console.log(`  Description: ${connection.description}`);
    console.log(`  Has credential: ${connection.hasCredential}`);

    if (connection.cloudSql) {
      console.log(`  Cloud SQL instance ID: ${connection.cloudSql.instanceId}`);
      console.log(`  Cloud SQL database: ${connection.cloudSql.database}`);
      console.log(`  Cloud SQL type: ${connection.cloudSql.type}`);
    }
  } catch (err) {
    if (err.code === status.NOT_FOUND) {
      console.log(`Connection ${name} not found.`);
    } else {
      console.error(`Error getting connection ${name}:`, err);
    }
  }
}
```

### Java

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Java 設定操作說明進行操作。詳情請參閱 [BigQuery Java API 參考文件](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/overview?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import com.google.api.gax.rpc.ApiException;
import com.google.api.gax.rpc.NotFoundException;
import com.google.cloud.bigquery.connection.v1.Connection;
import com.google.cloud.bigquery.connection.v1.ConnectionName;
import com.google.cloud.bigqueryconnection.v1.ConnectionServiceClient;
import java.io.IOException;

public class GetConnection {

  /**
   * Retrieves metadata about a specified BigQuery connection.
   *
   * @param projectId The Google Cloud project ID (for example, "example-project-id").
   * @param location The geographic location of the connection (for example, "us-central1").
   * @param connectionId The ID of the connection to retrieve (for example,
   *     "example-connection-id").
   */
  public static void getConnection(String projectId, String location, String connectionId) {
    ConnectionName name = ConnectionName.of(projectId, location, connectionId);

    try (ConnectionServiceClient client = ConnectionServiceClient.create()) {
      Connection connection = client.getConnection(name);

      System.out.printf("Successfully retrieved connection: %s%n", connection.getName());
      System.out.printf("Friendly name: %s%n", connection.getFriendlyName());
      System.out.printf("Description: %s%n", connection.getDescription());
      if (connection.hasCloudResource()) {
        System.out.printf(
            "Service Account: %s%n", connection.getCloudResource().getServiceAccountId());
      }
      if (connection.hasCloudSql()) {
        System.out.printf(
            "Cloud SQL instance ID: %s%n", connection.getCloudSql().getInstanceId());
      }
    } catch (NotFoundException err) {
      System.err.printf(
          "error: connection '%s' not found in location '%s' for project '%s': %s%n",
          connectionId, location, projectId, err.getMessage());
    } catch (ApiException | IOException err) {
      System.err.printf(
          "error: failed to get connection '%s' in location '%s' for project '%s': %s%n",
          connectionId, location, projectId, err.getMessage());
    }
  }
```

## 取得連線的身分與存取權管理 (IAM) 政策

請按照下列步驟，取得連線的 IAM 政策：

### Python

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Python 設定操作說明進行操作。詳情請參閱 [BigQuery Python API 參考文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import google.api_core.exceptions
from google.cloud import bigquery_connection_v1

client = bigquery_connection_v1.ConnectionServiceClient()


def get_connection_iam_policy(
    project_id: str,
    location: str,
    connection_id: str,
):
    """Gets the IAM policy of a connection.

    Args:
        project_id: The Google Cloud project ID.
        location: The geographic location of the connection (for example, "us").
        connection_id: The ID of the connection.
    """

    resource = client.connection_path(project_id, location, connection_id)

    try:
        policy = client.get_iam_policy(resource=resource)

        print(f"Successfully retrieved IAM policy for connection: {resource}")
        if not policy.bindings:
            print("This policy is empty and has no bindings.")

        for binding in policy.bindings:
            print(f"Role: {binding.role}")
            print("Members:")
            for member in binding.members:
                print(f"    - {member}")

    except google.api_core.exceptions.NotFound:
        print(f"Connection not found: {resource}")
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
 * Gets the IAM policy for a BigQuery connection.
 * @param {string} projectId Google Cloud project ID (for example, 'example-project-id').
 * @param {string} location The location of the connection (for example, 'us').
 * @param {string} connectionId The connection ID (for example, 'example-connection').
 */
async function getIamPolicy(projectId, location, connectionId) {

  const resource = client.connectionPath(projectId, location, connectionId);

  const request = {
    resource,
  };

  try {

    const [policy] = await client.getIamPolicy(request);

    console.log(
      `Successfully retrieved IAM policy for connection: ${connectionId}`,
    );

    if (policy.bindings && policy.bindings.length > 0) {
      console.log('Bindings:');
      policy.bindings.forEach(binding => {
        console.log(`  Role: ${binding.role}`);
        console.log('  Members:');
        binding.members.forEach(member => {
          console.log(`    - ${member}`);
        });
      });
    } else {
      console.log('No policy bindings found.');
    }
  } catch (err) {

    if (err.code === status.NOT_FOUND) {
      console.log(
        `Connection '${connectionId}' not found in project '${projectId}' at location '${location}'.`,
      );
    } else {
      console.error('An error occurred while getting the IAM policy:', err);
    }
  }
}
```

### Java

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Java 設定操作說明進行操作。詳情請參閱 [BigQuery Java API 參考文件](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/overview?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import com.google.api.gax.rpc.ApiException;
import com.google.api.gax.rpc.NotFoundException;
import com.google.cloud.bigquery.connection.v1.ConnectionName;
import com.google.cloud.bigqueryconnection.v1.ConnectionServiceClient;
import com.google.iam.v1.Binding;
import com.google.iam.v1.GetIamPolicyRequest;
import com.google.iam.v1.Policy;
import java.io.IOException;

public class GetIamPolicy {

  /**
   * Retrieves the IAM policy of a specified BigQuery connection.
   *
   * @param projectId The Google Cloud project ID (for example, "example-project-id").
   * @param location The geographic location of the connection (for example, "us-central1").
   * @param connectionId The ID of the connection (for example, "example-connection-id").
   */
  public static void getIamPolicy(
      String projectId, String location, String connectionId) {
    ConnectionName resource = ConnectionName.of(projectId, location, connectionId);

    GetIamPolicyRequest request =
        GetIamPolicyRequest.newBuilder().setResource(resource.toString()).build();

    try (ConnectionServiceClient client = ConnectionServiceClient.create()) {
      Policy policy = client.getIamPolicy(request);

      System.out.printf("Successfully retrieved IAM policy for connection: %s%n", resource);
      if (policy.getBindingsList().isEmpty()) {
        System.out.println("Policy is empty and has no bindings.");
      }

      for (Binding binding : policy.getBindingsList()) {
        System.out.printf("Role: %s%n", binding.getRole());
        System.out.println("Members:");
        for (String member : binding.getMembersList()) {
          System.out.printf("  - %s%n", member);
        }
      }
    } catch (NotFoundException err) {
      System.err.printf(
          "error: connection '%s' not found in location '%s' for project '%s': %s%n",
          connectionId, location, projectId, err.getMessage());
    } catch (ApiException | IOException err) {
      System.err.printf(
          "error: failed to get IAM policy for connection '%s' in location '%s' for project '%s': %s%n",
          connectionId, location, projectId, err.getMessage());
    }
  }
```

## 與使用者共用連線

您可以授予下列角色，讓使用者查詢資料及管理連結：

* `roles/bigquery.connectionUser`：可讓使用者透過連線，連至外部資料來源並執行查詢。
* `roles/bigquery.connectionAdmin`：可讓使用者管理連線。

如要進一步瞭解 BigQuery 的 IAM 角色和權限，請參閱「[預先定義的角色和權限](https://docs.cloud.google.com/bigquery/access-control?hl=zh-tw)」。

選取下列選項之一：

### 控制台

1. 前往「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)

   連線會列在專案的「連線」群組中。
2. 點選左側窗格中的 explore「Explorer」。

   如果沒有看到左側窗格，請按一下 last\_page「Expand left pane」(展開左側窗格)，開啟窗格。
3. 依序點選專案和「連線」，然後選取連線。
4. 在「詳細資料」窗格中，按一下「共用」即可共用連線。接著，按照下列步驟操作：

   1. 在「Connection permissions」(連線權限) 對話方塊中，新增或編輯主體，與其他主體共用連線。
   2. 按一下 [儲存]。

### bq

您無法使用 bq 指令列工具共用連線。如要共用連線，請使用 Google Cloud 控制台或 BigQuery Connections API 方法。

### API

使用 BigQuery Connections REST API 參考資料部分的 [`projects.locations.connections.setIAM` 方法](https://docs.cloud.google.com/bigquery/docs/reference/bigqueryconnection/rest/v1/projects.locations.connections?hl=zh-tw#methods)，並提供 `policy` 資源的執行個體。

### Java

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Java 設定操作說明進行操作。詳情請參閱 [BigQuery Java API 參考文件](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/overview?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import com.google.api.resourcenames.ResourceName;
import com.google.cloud.bigquery.connection.v1.ConnectionName;
import com.google.cloud.bigqueryconnection.v1.ConnectionServiceClient;
import com.google.iam.v1.Binding;
import com.google.iam.v1.Policy;
import com.google.iam.v1.SetIamPolicyRequest;
import java.io.IOException;

// Sample to share connections
public class ShareConnection {

  public static void main(String[] args) throws IOException {
    // TODO(developer): Replace these variables before running the sample.
    String projectId = "MY_PROJECT_ID";
    String location = "MY_LOCATION";
    String connectionId = "MY_CONNECTION_ID";
    shareConnection(projectId, location, connectionId);
  }

  static void shareConnection(String projectId, String location, String connectionId)
      throws IOException {
    try (ConnectionServiceClient client = ConnectionServiceClient.create()) {
      ResourceName resource = ConnectionName.of(projectId, location, connectionId);
      Binding binding =
          Binding.newBuilder()
              .addMembers("group:example-analyst-group@google.com")
              .setRole("roles/bigquery.connectionUser")
              .build();
      Policy policy = Policy.newBuilder().addBindings(binding).build();
      SetIamPolicyRequest request =
          SetIamPolicyRequest.newBuilder()
              .setResource(resource.toString())
              .setPolicy(policy)
              .build();
      client.setIamPolicy(request);
      System.out.println("Connection shared successfully");
    }
  }
}
```

## 編輯連線

連線會使用建立者的憑證。如需變更與連線連結的使用者，可以更新使用者的憑證。如果建立連線的使用者已離開貴組織，這項功能就非常實用。

您無法編輯連結的下列元素：

* 連線類型
* 連線 ID
* 位置

選取下列選項之一：

### 控制台

1. 前往「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)

   連線會列在專案中名為「Connections」(連線)  的群組。
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中，依序點選專案名稱和「Connections」(連線)，即可查看所有連線的清單。
4. 如要查看詳細資料，請按一下連線。
5. 在「Connection info」(連線資訊) 部分，按一下 mode\_edit「Edit details」(編輯詳細資料)。接著，按照下列步驟操作：

   1. 在「Edit connection」(編輯連線) 對話方塊中，編輯連線詳細資料，包括使用者憑證。
   2. 按一下「Update connection」(更新連線)。

### bq

輸入 `bq update` 指令，並提供連線旗標：`--connection`。必須提供完整的 `connection_id`。

```
  bq update --connection --connection_type='CLOUD_SQL'
      --properties='{"instanceId" : "INSTANCE",
      "database" : "DATABASE", "type" : "MYSQL" }'
      --connection_credential='{"username":"USERNAME", "password":"PASSWORD"}'
      PROJECT.REGION.CONNECTION_ID
```

更改下列內容：

* `INSTANCE`：Cloud SQL 執行個體
* `DATABASE`：資料庫名稱
* `USERNAME`：Cloud SQL 資料庫的使用者名稱
* `PASSWORD`：Cloud SQL 資料庫的密碼
* `PROJECT`： Google Cloud 專案 ID
* `REGION`：[連線區域](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw#supported_locations)
* `CONNECTION_ID`：連線 ID

舉例來說，下列指令會更新專案中的連線，專案 ID 為 `federation-test`，連線 ID 為 `test-mysql`。

```
bq update --connection --connection_type='CLOUD_SQL'
    --properties='{"instanceId" : "federation-test:us-central1:new-mysql",
    "database" : "imdb2", "type" : "MYSQL" }'
    --connection_credential='{"username":"my_username",
    "password":"my_password"}' federation-test.us.test-mysql
```

### API

請參閱 REST API 參考資料部分的 [`projects.locations.connections.patch` 方法](https://docs.cloud.google.com/bigquery/docs/reference/bigqueryconnection/rest/v1/projects.locations.connections?hl=zh-tw#methods)，並提供 `connection` 的執行個體。

### Python

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Python 設定操作說明進行操作。詳情請參閱 [BigQuery Python API 參考文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import google.api_core.exceptions
from google.cloud import bigquery_connection_v1
from google.protobuf import field_mask_pb2

client = bigquery_connection_v1.ConnectionServiceClient()


def update_connection(
```