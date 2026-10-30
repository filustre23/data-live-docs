Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 連線至 Apache Spark

BigQuery 中的 Apache Spark [連線](https://docs.cloud.google.com/bigquery/docs/connections-api-intro?hl=zh-tw)可讓使用者將 BigQuery 連結至 Managed Service for Apache Spark，以便[執行 Apache Spark 預存程序](https://docs.cloud.google.com/bigquery/docs/spark-procedures?hl=zh-tw)。您可以建立這項連線、將必要權限授予其服務帳戶，並與使用者共用連線。

## 事前準備

* 啟用 BigQuery Connection API。

  [啟用 API](https://console.cloud.google.com/apis/library/bigqueryconnection.googleapis.com?hl=zh-tw)
* 如要取得建立 Spark 連線所需的權限，請要求管理員授予您專案的 [BigQuery 連線管理員](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.connectionAdmin)  (`roles/bigquery.connectionAdmin`) IAM 角色。如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

  您或許也能透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)，取得必要權限。
* 選用：如要使用 [Dataproc Metastore](https://docs.cloud.google.com/dataproc-metastore/docs/overview?hl=zh-tw) 管理中繼資料，請確認您已[建立 Dataproc Metastore 服務](https://docs.cloud.google.com/dataproc-metastore/docs/create-service?hl=zh-tw)。
* 選用：如要[使用 Spark History Server 網頁介面查看工作記錄](https://docs.cloud.google.com/dataproc/docs/concepts/jobs/history-server?hl=zh-tw#spark_history_server_web_interface)，請務必[建立 Managed Service for Apache Spark 永久記錄伺服器 (PHS)](https://docs.cloud.google.com/dataproc/docs/concepts/jobs/history-server?hl=zh-tw#create_a_phs_cluster)。

### 位置注意事項

選擇資料的位置時，請考慮下列事項：

#### 多區域

您必須指定位於相同大型地理區域的 Google Cloud 資源：

* BigQuery 美國多區域中的連線，可以參照美國地理區域中任何單一區域的 [Spark 記錄伺服器](https://docs.cloud.google.com/dataproc/docs/concepts/jobs/history-server?hl=zh-tw) 或 [Dataproc Metastore](https://docs.cloud.google.com/dataproc-metastore/docs/overview?hl=zh-tw)，例如 `us-central1`、`us-east4` 或 `us-west2`。
* BigQuery 歐盟多區域中的連線，可以參照歐盟[成員國](https://europa.eu/european-union/about-eu/countries_en)中的 Spark 記錄伺服器或 Dataproc Metastore，例如 `europe-north1` 或 `europe-west3`。

#### 單一地區

單一區域中的連線只能參照同一區域中的 Google Cloud資源。例如，單一區域 `us-east4` 中的連線只能參照 `us-east4` 中的 Spark 記錄伺服器或 Dataproc metastore。

## 建立連線

選取下列選項之一：

### 控制台

1. 前往「BigQuery」頁面

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在「Explorer」窗格中，點選「add 新增資料」。

   「新增資料」對話方塊隨即開啟。
3. 在「篩選依據」窗格的「資料來源類型」部分，選取「業務應用程式」。

   或者，您也可以在「Search for data sources」(搜尋資料來源) 欄位中輸入 `Spark`。
4. 在「精選資料來源」部分，按一下「Apache Spark」。
5. 點選「Apache Spark: BigQuery Federation」解決方案資訊卡。
6. 在「外部資料來源」窗格，輸入下列資訊：

   * 在「Connection type」(連線類型) 清單中，選取「Apache Spark」。
   * 在「Connection ID」(連線 ID) 欄位中，輸入連線名稱，例如 `spark_connection`。
   * 在「Data location」(資料位置) 清單中選取區域。

   您可以在[支援 BigQuery 的區域和多區域](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)建立連線。詳情請參閱「[位置考量](#location-considerations)」。

   * 選用：從「Metastore service」(Metastore 服務) 清單中，選取「Dataproc Metastore」。
   * 選用：在「History server cluster」(記錄伺服器叢集) 欄位中，輸入 [Managed Service for Apache Spark 永久記錄伺服器](https://docs.cloud.google.com/dataproc/docs/concepts/jobs/history-server?hl=zh-tw#create_a_phs_cluster)。
7. 點選「建立連線」。
8. 點選「前往連線」。
9. 在「連線資訊」窗格中，複製服務帳戶 ID，以便在後續步驟中使用。

### bq

1. 在指令列環境中，使用 [`bq mk` 指令](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_mk)建立連線：

   ```
   bq mk --connection --connection_type='SPARK' \
    --properties=PROPERTIES \
    --project_id=PROJECT_ID \
    --location=LOCATION
    CONNECTION_ID
   ```

   更改下列內容：

   * `PROPERTIES`：鍵/值組合，以 JSON 格式提供連線專屬參數

     例如：

     ```
     --properties='{
     "metastoreServiceConfig": {"metastoreService": "METASTORE_SERVICE_NAME"},
     "sparkHistoryServerConfig": {"dataprocCluster": "MANAGED_SERVICE_FOR_APACHE_SPARK_CLUSTER_NAME"}
     }'
     ```

     更改下列內容：

     + `METASTORE_SERVICE_NAME`：[採用 gRPC 網路設定的 Dataproc Metastore](https://docs.cloud.google.com/dataproc-metastore/docs/endpoint-protocol?hl=zh-tw#grpc_network_configuration)，例如 `projects/my-project-id/locations/us-central1/services/my-service`

       詳情請參閱如何[使用端點通訊協定存取儲存的 Hive metastore 中繼資料](https://docs.cloud.google.com/dataproc-metastore/docs/endpoint-protocol?hl=zh-tw)。
     + `MANAGED_SERVICE_FOR_APACHE_SPARK_CLUSTER_NAME`：Spark 記錄伺服器設定，例如 `projects/my-project-id/regions/us-central1/clusters/my-cluster`

       詳情請參閱「[建立永久記錄伺服器叢集](https://docs.cloud.google.com/dataproc/docs/concepts/jobs/history-server?hl=zh-tw#create_a_phs_cluster)」。
   * `PROJECT_ID`：您的 Google Cloud 專案 ID
   * `LOCATION`：要儲存連線的位置，例如 `US`
   * `CONNECTION_ID`：連線 ID，例如 `myconnection`

     在 Google Cloud 控制台中[查看連線詳細資料](https://docs.cloud.google.com/bigquery/docs/working-with-connections?hl=zh-tw#view-connections)時，連線 ID 是「Connection ID」(連線 ID) 中顯示的完整連線 ID 最後一個部分的值，例如 `projects/.../locations/.../connections/myconnection`
2. 擷取並複製服務帳戶 ID，因為您會在其他步驟中用到：

   ```
   bq show --location=LOCATION --connection PROJECT_ID.LOCATION.CONNECTION_ID
   ```

   輸出結果會與下列內容相似：

   ```
   Connection myproject.us.myconnection

          name           type                    properties
   ---------------------- ------- ---------------------------------------------------
   myproject.us.myconnection  SPARK   {"serviceAccountId": "bqserver@example.iam.gserviceaccount.com"}
   ```

如要瞭解如何管理連結，請參閱「[管理連結](https://docs.cloud.google.com/bigquery/docs/working-with-connections?hl=zh-tw)」。

## 將存取權授予服務帳戶

如要讓 Apache Spark 預存程序存取 Google Cloud資源，您必須為與預存程序連線相關聯的服務帳戶，授予必要的 IAM 權限。或者，您也可以使用[自訂服務帳戶](https://docs.cloud.google.com/bigquery/docs/spark-procedures?hl=zh-tw#use_a_custom_service_account)存取資料。

* 如要讀取及寫入 BigQuery 資料，您必須將下列 IAM 權限授予服務帳戶：

  + BigQuery 資料表上的`bigquery.tables.*`
  + 專案的`bigquery.readsessions.*`

  `roles/bigquery.admin` IAM 角色包含服務帳戶所需的權限，可從 BigQuery 讀取資料及寫入資料。

  **注意：** 如果預存程序將資料寫入暫時 Cloud Storage bucket，然後[將 Cloud Storage 資料載入 BigQuery](https://docs.cloud.google.com/bigquery/docs/batch-loading-data?hl=zh-tw)，則必須為服務帳戶授予專案的 `bigquery.jobs.create` 權限。如要進一步瞭解 BigQuery 的 IAM 角色和權限，請參閱「[使用 IAM 存取控管](https://docs.cloud.google.com/bigquery/access-control?hl=zh-tw)」。
* 如要讀取及寫入 Cloud Storage 的資料，您必須為服務帳戶授予 Cloud Storage 物件的 `storage.objects.*` 權限。

  `roles/storage.objectAdmin` IAM 角色包含服務帳戶所需的權限，可從 Cloud Storage 讀取資料及寫入資料。
* 如果您在建立連線時指定 Dataproc Metastore，則必須在 Dataproc Metastore 上授予服務帳戶 `metastore.services.get` 權限，BigQuery 才能擷取 metastore 設定的詳細資料。

  預先定義的 `roles/metastore.metadataViewer` 角色包含服務帳戶所需的權限，可擷取 metastore 設定的詳細資料。

  您也必須為服務帳戶授予 Cloud Storage bucket 的 `roles/storage.objectAdmin` 角色，預存程序才能存取 Dataproc metastore (`hive.metastore.warehouse.dir`) 的 Hive 倉儲目錄。如果預存程序會對 metastore 執行作業，您可能需要授予其他權限。如要進一步瞭解 Dataproc Metastore 的 IAM 角色和權限，請參閱「[Dataproc Metastore 預先定義的角色和權限](https://docs.cloud.google.com/dataproc-metastore/docs/iam-roles?hl=zh-tw)」。
* 如果您在建立連線時指定 Managed Service for Apache Spark 永久記錄伺服器，則須將下列角色授予服務帳戶：

  + Managed Service for Apache Spark Persistent History Server 的 `roles/dataproc.viewer` 角色，其中包含 `dataproc.clusters.get` 權限。
  + 建立 Managed Service for Apache Spark Persistent History Server 時，為 `spark:spark.history.fs.logDirectory` 屬性指定的 Cloud Storage bucket `roles/storage.objectAdmin` 角色。

  詳情請參閱「[Managed Service for Apache Spark Persistent History Server](https://docs.cloud.google.com/dataproc/docs/concepts/jobs/history-server?hl=zh-tw#create_a_phs_cluster)」和「[Managed Service for Apache Spark 角色和權限](https://docs.cloud.google.com/dataproc/docs/concepts/iam/iam?hl=zh-tw)」。

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

## 後續步驟

* 瞭解不同的[連線類型](https://docs.cloud.google.com/bigquery/docs/connections-api-intro?hl=zh-tw)。
* 瞭解如何[管理連結](https://docs.cloud.google.com/bigquery/docs/working-with-connections?hl=zh-tw)。
* 瞭解如何[建立 Apache Spark 預存程序](https://docs.cloud.google.com/bigquery/docs/spark-procedures?hl=zh-tw)。
* 瞭解如何[管理預存程序](https://docs.cloud.google.com/bigquery/docs/routines?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-10-29 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-10-29 (世界標準時間)。"],[],[]]