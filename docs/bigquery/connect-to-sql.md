Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 連線至 Cloud SQL

BigQuery 管理員可以建立[連線](https://docs.cloud.google.com/bigquery/docs/connections-api-intro?hl=zh-tw)，存取 Cloud SQL 資料。資料分析師可透過這項連線[查詢 Cloud SQL 中的資料](https://docs.cloud.google.com/bigquery/docs/cloud-sql-federated-queries?hl=zh-tw)。
如要連線至 Cloud SQL，請按照下列步驟操作：

1. [建立 Cloud SQL 連線](#create-sql-connection)
2. [授予 **BigQuery Connection 服務代理人**](#access-sql)存取權。

## 事前準備

1. 選取含有 Cloud SQL 資料庫的專案。  

   [前往專案選取器](https://console.cloud.google.com/projectselector2/home/dashboard?hl=zh-tw)
2. 啟用 BigQuery Connection API。  

   [啟用 API](https://console.cloud.google.com/apis/library/bigqueryconnection.googleapis.com?hl=zh-tw)
3. 確認 Cloud SQL 執行個體具有[公開 IP 連線](https://docs.cloud.google.com/sql/docs/mysql/configure-ip?hl=zh-tw)或[私人連線](https://docs.cloud.google.com/sql/docs/mysql/configure-private-ip?hl=zh-tw)：  
   * 如要保護 Cloud SQL 執行個體，您可以新增公開 IP 連線，但不必提供授權位址。這樣一來，執行個體就無法從公用網際網路存取，但可供 BigQuery 查詢。
   * 如要讓 BigQuery 透過私人連線存取 Cloud SQL 資料，請為[新](https://docs.cloud.google.com/sql/docs/mysql/configure-private-ip?hl=zh-tw#new-private-instance)或[現有](https://docs.cloud.google.com/sql/docs/mysql/configure-private-ip?hl=zh-tw#existing-private-instance) Cloud SQL 執行個體設定私人 IP 連線，然後選取「啟用私人路徑」核取方塊。這項服務會使用內部直接路徑，而非虛擬私有雲內的私人 IP 位址。
4. 如要取得建立 Cloud SQL 連線所需的權限，請要求系統管理員在專案中授予您「BigQuery Connection 管理員」(`roles/bigquery.connectionAdmin`) IAM 角色。如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

   您或許也能透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)，取得必要權限。

## 建立 Cloud SQL 連線

最佳做法是使用連線處理資料庫憑證，連線至 Cloud SQL。連線會經過加密，並安全地儲存在 BigQuery 連線服務中。如果使用者憑證適用於來源中的其他資料，您可以重複使用該連結。舉例來說，您或許可以使用一個連線，查詢位於相同 Cloud SQL 執行個體中的多個資料庫。

選取下列任一選項，建立 Cloud SQL 連線：

### 控制台

1. 前往「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在「Explorer」窗格中，按一下 add「Add」。

   「新增資料」對話方塊隨即開啟。
3. 在「Filter By」(依據篩選) 窗格的「Data Source Type」(資料來源類型) 專區中，選取「Databases」(資料庫)。

   或者，您也可以在「Search for data sources」(搜尋資料來源) 欄位中輸入 `mysql`。
4. 在「精選資料來源」部分，按一下「MySQL」。
5. 按一下「CloudSQL (MySQL)：BigQuery Federation」解決方案資訊卡。
6. 在「外部資料來源」對話方塊中，輸入下列資訊：

   * 在「連線類型」中選取來源類型，例如「MySQL」或「PostgreSQL」。
   * 在「Connection ID」(連線 ID) 專區中輸入連線資源的 ID。可以使用英文字母、數字和底線。例如：`bq_sql_connection`。
   * 在「資料位置」部分，選取與[外部資料來源區域相容](https://docs.cloud.google.com/bigquery/docs/federated-queries-intro?hl=zh-tw#supported_regions)的 BigQuery 位置 (或區域)。
   * 選用：在「Friendly name」(好記名稱) 中輸入使用者容易記得的連線名稱，例如 `My connection resource`。好記名稱可以是任何資料值，只要您日後需要修改時可以輕鬆識別連線資源即可。
   * 選用：在「Description」(說明) 中輸入這項連線資源的說明。
   * 選用：**加密**。如要使用[客戶自行管理的加密金鑰 (CMEK)](https://docs.cloud.google.com/bigquery/docs/customer-managed-encryption?hl=zh-tw) 加密憑證，請選取「客戶自行管理的加密金鑰 (CMEK)」，然後選取客戶自行管理的金鑰。否則，系統會以預設的 Google-owned and Google-managed encryption key保護您的憑證。
   * 如果連線類型選擇 Cloud SQL MySQL 或 Postgres，請在「Cloud SQL connection name」(Cloud SQL 連線名稱) 中，輸入完整的 [Cloud SQL 執行個體名稱](https://docs.cloud.google.com/sql/docs/mysql/instance-settings?hl=zh-tw#instance-id-2ndgen)，格式通常是 `project-id:location-id:instance-id`。在要查詢的 [Cloud SQL 執行個體](https://console.cloud.google.com/sql/instances?hl=zh-tw)詳細資料頁面中，您可以找到執行個體 ID。
   * 在「Database name」(資料庫名稱) 中輸入資料庫名稱。
   * 在「Database username」(資料庫使用者名稱) 中輸入資料庫的使用者名稱。
   * 在「Database password」(資料庫密碼) 中輸入資料庫的密碼。

     + 選用：如要查看密碼，請按一下 
       visibility\_off  **顯示密碼**。**注意：** 如果同一組使用者憑證適用於外部資料來源中的其他資料庫，該使用者就能透過相同的連線資源查詢這些資料庫。
7. 點選「建立連線」。
8. 點選「前往連線」。
9. 在「連線資訊」窗格中，複製服務帳戶 ID，以供後續步驟使用。

### bq

輸入 `bq mk` 指令並提供連線旗標 `--connection`。還需加上以下旗標：

* `--connection_type`
* `--properties`
* `--connection_credential`
* `--project_id`
* `--location`

以下旗標為選用項目：

* `--display_name`：連線的易記名稱。
* `--description`：連線說明。
* `--kms_key_name`：客戶自行管理的加密金鑰。如果省略此屬性，系統會以預設的 Google-owned and Google-managed encryption key保護憑證。

`connection_id` 是選用參數，可做為指令的最後一個引數新增，用於內部儲存。如果未提供連線 ID，系統會自動產生專屬 ID。
`connection_id` 可以包含字母、數字和底線。

```
    bq mk --connection --display_name='friendly name' --connection_type=TYPE \
      --properties=PROPERTIES --connection_credential=CREDENTIALS \
      --project_id=PROJECT_ID --location=LOCATION \
      CONNECTION_ID
```

更改下列內容：

* `TYPE`：外部資料來源的類型。
* `PROPERTIES`：已建立連線的 JSON 格式參數。例如：`--properties='{"param":"param_value"}'`。如要建立連線資源，您必須提供 `instanceID`、`database` 和 `type` 參數。
* `CREDENTIALS`：參數 `username` 和 `password`。
* `PROJECT_ID`：您的專案 ID。
* `LOCATION`：Cloud SQL 執行個體所在的區域，或對應的多區域。
* `CONNECTION_ID`：連線 ID。

舉例來說，下列指令會在 ID 為 `federation-test` 的專案中新建名為 my\_new\_connection (好記名稱：「My new connection」) 的連線資源。

```
bq mk --connection --display_name='friendly name' --connection_type='CLOUD_SQL' \
  --properties='{"instanceId":"federation-test:us-central1:mytestsql","database":"mydatabase","type":"MYSQL"}' \
  --connection_credential='{"username":"myusername", "password":"mypassword"}' \
  --project_id=federation-test --location=us my_connection_id
```

### API

在 BigQuery Connection API 中，您可以在 `ConnectionService` 內叫用 `CreateConnection`，以例項化連線。詳情請參閱[用戶端程式庫頁面](https://docs.cloud.google.com/bigquery/docs/reference/bigqueryconnection?hl=zh-tw)。

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

## 授予服務代理存取權

在專案中首次建立 Cloud SQL 連線時，系統會自動建立[服務代理程式](https://docs.cloud.google.com/iam/docs/service-agents?hl=zh-tw)。服務代理的名稱為「BigQuery Connection Service Agent」。如要取得服務代理 ID，請[查看連線詳細資料](https://docs.cloud.google.com/bigquery/docs/working-with-connections?hl=zh-tw#view-connections)。服務代理 ID 的格式如下：

`service-PROJECT_NUMBER@gcp-sa-bigqueryconnection.iam.gserviceaccount.com`。

如要連線至 Cloud SQL，您必須授予新連線 Cloud SQL 唯讀存取權，這樣 BigQuery 就能代替使用者存取檔案。服務代理必須具備下列權限：

* `cloudsql.instances.connect`
* `cloudsql.instances.get`

您可以為與連線相關聯的服務代理授予[Cloud SQL 用戶端 IAM 角色](https://docs.cloud.google.com/sql/docs/mysql/iam-roles?hl=zh-tw#roles) (`roles/cloudsql.client`)，該角色已指派這些權限。如果服務代理已具備必要權限，則可略過下列步驟。

### 控制台

1. 前往「IAM & Admin」(IAM 與管理) 頁面。

   [前往「IAM & Admin」(IAM 與管理)](https://console.cloud.google.com/project/_/iam-admin?hl=zh-tw)
2. 按一下 person\_add「授予存取權」。

   「新增主體」對話方塊隨即開啟。
3. 在「新增主體」欄位中，輸入服務代理程式名稱「BigQuery Connection Service Agent」，或從[連線資訊](https://docs.cloud.google.com/bigquery/docs/working-with-connections?hl=zh-tw#view-connections)取得服務代理程式 ID。
4. 在「Select a role」(選取角色) 欄位中，依序選取「Cloud SQL」和「Cloud SQL Client」(Cloud SQL 用戶端)。
5. 按一下 [儲存]。

### gcloud

使用 [`gcloud projects add-iam-policy-binding`](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw#grant-single-role) 指令：

```
gcloud projects add-iam-policy-binding PROJECT_ID --member=serviceAccount:SERVICE_AGENT_ID --role=roles/cloudsql.client
```

提供以下這些值：

* `PROJECT_ID`： Google Cloud 專案 ID。
* `SERVICE_AGENT_ID`：從[連線資訊](https://docs.cloud.google.com/bigquery/docs/working-with-connections?hl=zh-tw#view-connections)取得的服務代理 ID。

**注意：** 如要進一步瞭解如何授予及撤銷 IAM 角色，請參閱「[管理專案、資料夾和機構的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw#view-access)」一文。

## 與使用者共用連線

您可以授予下列角色，讓使用者查詢資料及管理連線：

* `roles/bigquery.connectionUser`：可讓使用者透過連線功能連結外部資料來源，並對其執行查詢。
* `roles/bigquery.connectionAdmin`：允許使用者管理連線。

如要進一步瞭解 BigQuery 中的 IAM 角色和權限，請參閱[預先定義的角色和權限](https://docs.cloud.google.com/bigquery/access-control?hl=zh-tw)一文。

選取下列選項之一：

### 控制台

1. 前往「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)

   連線會列在專案中，位於「Connections」(連線) 群組。
2. 點選左側窗格中的 explore「Explorer」。

   如果沒有看到左側窗格，請按一下 last\_page「Expand left pane」(展開左側窗格)，開啟窗格。
3. 按一下專案，然後依序點選「連線」和所需連線。
4. 在「詳細資料」窗格中，按一下「共用」即可共用連線。
   接著，按照下列步驟操作：

   1. 在「連線權限」對話方塊中，新增或編輯主體，與其他主體共用連線。
   2. 按一下 [儲存]。

### bq

您無法使用 bq 指令列工具共用連線。
如要共用連線，請使用 Google Cloud 控制台或 BigQuery Connections API 方法共用連線。

### API

請使用 BigQuery Connections REST API 參考資料部分中的 [`projects.locations.connections.setIAM` 方法](https://docs.cloud.google.com/bigquery/docs/reference/bigqueryconnection/rest/v1/projects.locations.connections?hl=zh-tw#methods)，並提供 `policy` 資源的執行個體。

### Java

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Java 設定說明操作。詳情請參閱 [BigQuery Java API 參考說明文件](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/overview?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

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

## 後續步驟

* 瞭解不同[連線類型](https://docs.cloud.google.com/bigquery/docs/connections-api-intro?hl=zh-tw)。
* 瞭解如何[管理連線](https://docs.cloud.google.com/bigquery/docs/working-with-connections?hl=zh-tw)。
* 瞭解[聯合查詢](https://docs.cloud.google.com/bigquery/docs/federated-queries-intro?hl=zh-tw)。
* 瞭解如何[查詢 Cloud SQL 資料](https://docs.cloud.google.com/bigquery/docs/cloud-sql-federated-queries?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-14 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-14 (世界標準時間)。"],[],[]]