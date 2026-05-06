Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [範例](https://docs.cloud.google.com/bigquery/docs/samples?hl=zh-tw)

# 建立 Cloud SQL 連線 透過集合功能整理內容 你可以依據偏好儲存及分類內容。

新增憑證，將 BigQuery 連結至 Cloud SQL。

## 深入探索

如需包含這個程式碼範例的詳細說明文件，請參閱下列文章：

* [連線至 Cloud SQL](https://docs.cloud.google.com/bigquery/docs/connect-to-sql?hl=zh-tw)

## 程式碼範例

### Java

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Java 設定說明操作。詳情請參閱 [BigQuery Java API 參考說明文件](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/overview?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import com.google.cloud.bigquery.connection.v1.CloudSqlCredential;
import com.google.cloud.bigquery.connection.v1.CloudSqlProperties;
import com.google.cloud.bigquery.connection.v1.Connection;
import com.google.cloud.bigquery.connection.v1.CreateConnectionRequest;
import com.google.cloud.bigquery.connection.v1.LocationName;
import com.google.cloud.bigqueryconnection.v1.ConnectionServiceClient;
import java.io.IOException;

// Sample to create a connection with cloud MySql database
public class CreateConnection {

  public static void main(String[] args) throws IOException {
    // TODO(developer): Replace these variables before running the sample.
    String projectId = "MY_PROJECT_ID";
    String location = "MY_LOCATION";
    String connectionId = "MY_CONNECTION_ID";
    String database = "MY_DATABASE";
    String instance = "MY_INSTANCE";
    String instanceLocation = "MY_INSTANCE_LOCATION";
    String username = "MY_USERNAME";
    String password = "MY_PASSWORD";
    String instanceId = String.format("%s:%s:%s", projectId, instanceLocation, instance);
    CloudSqlCredential cloudSqlCredential =
        CloudSqlCredential.newBuilder().setUsername(username).setPassword(password).build();
    CloudSqlProperties cloudSqlProperties =
        CloudSqlProperties.newBuilder()
            .setType(CloudSqlProperties.DatabaseType.MYSQL)
            .setDatabase(database)
            .setInstanceId(instanceId)
            .setCredential(cloudSqlCredential)
            .build();
    Connection connection = Connection.newBuilder().setCloudSql(cloudSqlProperties).build();
    createConnection(projectId, location, connectionId, connection);
  }

  static void createConnection(
      String projectId, String location, String connectionId, Connection connection)
      throws IOException {
    try (ConnectionServiceClient client = ConnectionServiceClient.create()) {
      LocationName parent = LocationName.of(projectId, location);
      CreateConnectionRequest request =
          CreateConnectionRequest.newBuilder()
              .setParent(parent.toString())
              .setConnection(connection)
              .setConnectionId(connectionId)
              .build();
      Connection response = client.createConnection(request);
      System.out.println("Connection created successfully :" + response.getName());
    }
  }
}
```

### Python

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Python 設定說明操作。詳情請參閱 [BigQuery Python API 參考說明文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
from google.cloud import bigquery_connection_v1 as bq_connection

"""This sample shows how to create a BigQuery connection with a Cloud SQL for MySQL database"""


def main() -> None:
    # TODO(developer): Set all variables for your Cloud SQL for MySQL connection.
    project_id = "your-project-id"  # set project_id
    location = "US"  # set location
    # See: https://cloud.google.com/bigquery/docs/locations for a list of
    # available locations.
    database = "my-database"  # set database name
    username = "my-username"  # set database username
    password = "my-password"  # set database password
    cloud_sql_conn_name = ""  # set the name of your connection
    transport = "grpc"  # Set the transport to either "grpc" or "rest"
    connection_id = "my-sample-connection"

    cloud_sql_credential = bq_connection.CloudSqlCredential(
        {
            "username": username,
            "password": password,
        }
    )
    cloud_sql_properties = bq_connection.CloudSqlProperties(
        {
            "type_": bq_connection.CloudSqlProperties.DatabaseType.MYSQL,
            "database": database,
            "instance_id": cloud_sql_conn_name,
            "credential": cloud_sql_credential,
        }
    )
    create_mysql_connection(
        connection_id, project_id, location, cloud_sql_properties, transport
    )


def create_mysql_connection(
    connection_id: str,
    project_id: str,
    location: str,
    cloud_sql_properties: bq_connection.CloudSqlProperties,
    transport: str,
) -> None:
    connection = bq_connection.types.Connection({"cloud_sql": cloud_sql_properties})
    client = bq_connection.ConnectionServiceClient(transport=transport)
    parent = client.common_location_path(project_id, location)
    request = bq_connection.CreateConnectionRequest(
        {
            "parent": parent,
            "connection": connection,
            # connection_id is optional, but can be useful to identify
            # connections by name. If not supplied, one is randomly
            # generated.
            "connection_id": connection_id,
        }
    )
    response = client.create_connection(request)
    print(f"Created connection successfully: {response.name}")
```

## 後續步驟

如要搜尋及篩選其他 Google Cloud 產品的程式碼範例，請參閱[Google Cloud 範例瀏覽工具](https://docs.cloud.google.com/docs/samples?product=bigqueryconnection&hl=zh-tw)。

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。




[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],[],[],[]]