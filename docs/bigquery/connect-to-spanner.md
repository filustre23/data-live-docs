Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 連線至 Spanner

BigQuery 管理員可以建立[連線](https://docs.cloud.google.com/bigquery/docs/connections-api-intro?hl=zh-tw)，存取 Spanner 資料。資料分析師可透過這個連線[查詢 Spanner 中的資料](https://docs.cloud.google.com/bigquery/docs/spanner-federated-queries?hl=zh-tw)。

## 事前準備

* 啟用 BigQuery Connection API。  

  [啟用 API](https://console.cloud.google.com/apis/library/bigqueryconnection.googleapis.com?hl=zh-tw)
* 如要取得連線至 Spanner 所需的權限，請要求系統管理員授予您專案的「[BigQuery 連線管理員](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.connectionAdmin) 」(`roles/bigquery.connectionAdmin`) IAM 角色。如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

  您或許也能透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)，取得必要權限。

## 建立 Spanner 連線

選取下列選項之一：

### 控制台

1. 前往「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在「Explorer」窗格中，點選「新增資料」add。

   「新增資料」對話方塊隨即開啟。
3. 在「Filter By」(依據篩選) 窗格的「Data Source Type」(資料來源類型) 專區中，選取「Databases」(資料庫)。

   或者，您也可以在「Search for data sources」(搜尋資料來源) 欄位中輸入 `Spanner`。
4. 在「精選資料來源」部分，按一下「Google Cloud Spanner」。
5. 按一下「Google Cloud Spanner：BigQuery 聯盟」解決方案資訊卡。
6. 在「外部資料來源」窗格中，輸入下列資訊：

   * 在「連線類型」中，選取「Cloud Spanner」。
   * 在「Connection ID」(連線 ID) 專區中輸入連線資源的 ID。可以使用英文字母、數字和底線。
   * 在「位置類型」中，選取與[外部資料來源區域相容](https://docs.cloud.google.com/bigquery/docs/federated-queries-intro?hl=zh-tw#supported_regions)的 BigQuery 位置 (或區域)。
   * 選用：在「Friendly name」(好記名稱) 中輸入使用者容易記得的連線名稱，例如 `My connection resource`。好記名稱可以是任何值，只要您日後需要修改時可以輕鬆識別連線資源即可。
   * 選用：在「Description」(說明) 中輸入這項連線資源的說明。
   * 在「Database name」(資料庫名稱) 中，輸入 Spanner 資料庫的名稱，格式如下：`"projects/PROJECT_ID/instances/INSTANCE/databases/DATABASE"`
   * 選用：如要執行平行讀取，請選取「並行讀取資料」。Spanner 可以將特定查詢分成較小的片段 (稱為「分區」)，並平行擷取分區。詳情請參閱 Spanner 說明文件中的「[平行讀取資料](https://docs.cloud.google.com/spanner/docs/reads?hl=zh-tw#read_data_in_parallel)」。這個選項只適用於下列查詢：執行計畫中第一個運算子為[分散式聯集](https://docs.cloud.google.com/spanner/docs/query-execution-operators?hl=zh-tw#distributed-union)運算子。其他查詢則會傳回錯誤。如要查看 Spanner 查詢的查詢執行計畫，請參閱「[瞭解 Spanner 如何執行查詢](https://docs.cloud.google.com/spanner/docs/sql-best-practices?hl=zh-tw#how-execute-queries)」。
   * 選用：在「Database role」(資料庫角色) 中，輸入 Spanner 資料庫角色的名稱。如果這個欄位不是空白，這個連線預設會使用這個資料庫角色查詢 Spanner。透過這項連線提交查詢的 Spanner 精細存取控管使用者，必須由系統管理員授予這個角色的存取權，且資料庫角色必須對外部查詢中指定的所有結構定義物件具備 `SELECT` 權限。如要瞭解精細的存取控管，請參閱「[關於精細的存取控管](https://docs.cloud.google.com/spanner/docs/fgac-about?hl=zh-tw)」。
   * (選用) 如要啟用 Data Boost，請選取「使用 Spanner Data Boost」。[Data Boost](https://docs.cloud.google.com/bigquery/docs/spanner-federated-queries?hl=zh-tw#data_boost)
     可讓您執行數據分析查詢和資料匯出作業，
     對已佈建的 BigQuery 執行個體現有工作負載幾乎沒有影響。如要啟用 Data Boost，請選取「Data Boost」和「Read data in parallel」(平行讀取資料)。
7. 點選「建立連線」。

### bq

如要建立連線，請使用 [`bq mk`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#mk-connection) 指令，並加上 `--connection` 旗標。

```
bq mk --connection \
    --connection_type=CLOUD_SPANNER \
    --properties='PROPERTIES' \
    --location=LOCATION \
    --display_name='FRIENDLY_NAME' \
    --description 'DESCRIPTION' \
    CONNECTION_ID
```

更改下列內容：

* `PROPERTIES`：包含下列欄位的 JSON 物件：

  + `"database"`：連線的 Spanner 資料庫

    請以字串形式指定，格式如下：
    `"projects/PROJECT_ID/instances/INSTANCE/databases/DATABASE"`。
  + `"use_parallelism"`：(選用) 如果 `true`，這個連線會執行平行讀取作業

    預設值為 `false`。Spanner 可以將特定查詢分成較小的片段 (稱為「分區」)，並平行擷取分區。詳情請參閱 Spanner 說明文件中的「[平行讀取資料](https://docs.cloud.google.com/spanner/docs/reads?hl=zh-tw#read_data_in_parallel)」。這個選項只適用於下列查詢：執行計畫中第一個運算子為[分散式聯集](https://docs.cloud.google.com/spanner/docs/query-execution-operators?hl=zh-tw#distributed-union)運算子。其他查詢則會傳回錯誤。如要查看 Spanner 查詢的查詢執行計畫，請參閱「[瞭解 Spanner 如何執行查詢](https://docs.cloud.google.com/spanner/docs/sql-best-practices?hl=zh-tw#how-execute-queries)」。
  + `"database_role"`：(選用) 如果不為空白，這個連線預設會使用這個資料庫角色查詢 Spanner。透過這項連線提交查詢的 Spanner 精細存取控管使用者，必須由管理員授予這個角色的存取權，且資料庫角色必須對外部查詢中指定的所有結構定義物件具備 `SELECT` 權限。

    如未指定，連線會使用 Spanner 的 IAM 預先定義角色進行驗證，且執行這項連線查詢的主體必須已獲授 `roles/spanner.databaseReader` IAM 角色。

    如要瞭解精細的存取控管，請參閱「[關於精細的存取控管](https://docs.cloud.google.com/spanner/docs/fgac-about?hl=zh-tw)」。
  + `"useDataBoost"`：(選用) 如果 `true`，使用者可透過這個連線使用 [Data Boost](https://docs.cloud.google.com/bigquery/docs/spanner-federated-queries?hl=zh-tw#data_boost)。Data Boost 可讓使用者在與佈建執行個體不同的獨立運算資源中執行聯合查詢，避免影響現有工作負載。如要啟用 Data Boost，請將 `"useDataBoost"` 設為 `true`，並將 `"use_parallelism"` 設為 `true`。

    如要使用 Data Boost，透過這個連線執行查詢的主體必須已獲授 `spanner.databases.useDataBoost` 權限。根據預設，`roles/spanner.admin` 和 `roles/spanner.databaseAdmin` 角色都具備這項權限。
* `LOCATION`：[與外部資料來源區域相容](https://docs.cloud.google.com/bigquery/docs/federated-queries-intro?hl=zh-tw#supported_regions)的 BigQuery 位置。
* `CONNECTION_ID`：連線資源的 ID

  連線 ID 可以包含英文字母、數字和底線。
  如果您未提供連線 ID，BigQuery 會自動產生專屬 ID。

  以下範例會建立名為 `my_connection_id` 的新連線資源。

  ```
  bq mk --connection \
    --connection_type='CLOUD_SPANNER' \
    --properties='{"database":"projects/my_project/instances/my_instance/databases/database1"}' \
    --project_id=federation-test \
    --location=us \
    my_connection_id
  ```

### API

在 `ConnectionService` 服務中呼叫 [`CreateConnection` 方法](https://docs.cloud.google.com/bigquery/docs/reference/bigqueryconnection/rpc/google.cloud.bigquery.connection.v1?hl=zh-tw#createconnectionrequest)。

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
* 瞭解如何[查詢 Spanner 資料](https://docs.cloud.google.com/bigquery/docs/spanner-federated-queries?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-06 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-06 (世界標準時間)。"],[],[]]