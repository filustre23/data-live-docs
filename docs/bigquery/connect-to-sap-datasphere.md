Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 連線至 SAP Datasphere

**預覽**

這項產品或功能適用《[服務專屬條款](https://docs.cloud.google.com/terms/service-terms?hl=zh-tw#1)》中「一般服務條款」一節的《正式發布前產品條款》。正式發布前的產品和功能是按照「原樣」提供，支援範圍可能有限。
詳情請參閱[推出階段說明](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages)。

**注意：** 如要取得支援或針對這項預先發布版功能提供意見回饋，請傳送電子郵件至 [bq-sap-federation-support@google.com](mailto:bq-sap-federation-support@google.com)。

BigQuery 管理員可以建立[連線](https://docs.cloud.google.com/bigquery/docs/connections-api-intro?hl=zh-tw)，存取 SAP Datasphere 資料。建立連線後，資料分析師就能[查詢 SAP Datasphere 中的資料](https://docs.cloud.google.com/bigquery/docs/sap-datasphere-federated-queries?hl=zh-tw)。

## 事前準備

1. 啟用 BigQuery Connection API。

   [啟用 API](https://console.cloud.google.com/apis/library/bigqueryconnection.googleapis.com?hl=zh-tw)
2. [建立 SAP Datasphere 資料庫使用者](https://help.sap.com/docs/SAP_DATASPHERE/be5967d099974c69b77f4549425ca4c0/798e3fd6707940c3bd2219b2d1ebaac2.html?locale=en-US)。
   請記下 BigQuery 的使用者名稱、密碼、主機名稱和連接埠。
3. 設定 SAP Datasphere 租戶，接受來自所選 IP 位址的流量，方法如下：

   * 將所有 [Google IP 位址範圍](https://www.gstatic.com/ipranges/goog.json)新增至 SAP Datasphere 的「信任的 IP」許可清單。
   * 將 `0.0.0.0/0` 新增至允許清單，開放所有 IP 位址連線至 SAP Datasphere 租戶。
   * [使用網路附件設定連線](https://docs.cloud.google.com/bigquery/docs/connections-with-network-attachment?hl=zh-tw)，讓 BigQuery 從靜態 IP 位址開啟連線。

     **注意：** 如果設定的網路連結和 VM 位於不同區域，使用這個連線查詢 SAP Datasphere 資料時，可能會發生跨區域資料移動。

   如要進一步瞭解如何設定 SAP Datasphere 租戶，請參閱「[將 IP 位址新增至 IP 許可清單](https://help.sap.com/docs/SAP_DATASPHERE/9f804b8efa8043539289f42f372c4862/a3c214514ef94e899459f68f4c1e2a23.html?locale=en-US)」。

### 必要的角色

如要取得連線至 SAP Datasphere 所需的權限，請要求系統管理員授予您專案的「[BigQuery 連線管理員](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.connectionAdmin) 」(`roles/bigquery.connectionAdmin`) IAM 角色。如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

您或許也能透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)，取得必要權限。

### 將 BigQuery 連結至 SAP Datasphere

您可以在 Google Cloud 控制台或 bq 指令列工具中，將 BigQuery 連線至 SAP Datasphere。

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在「Explorer」窗格中，點選「新增資料」add。

   「新增資料」對話方塊隨即開啟。
3. 在「Filter By」(依據篩選) 窗格的「Data Source Type」(資料來源類型) 專區中，選取「Databases」(資料庫)。

   或者，您也可以在「Search for data sources」(搜尋資料來源) 欄位中輸入 `SAP HANA`。
4. 在「精選資料來源」部分，按一下「SAP HANA」。
5. 按一下「SAP HANA：BigQuery Federation」解決方案資訊卡。
6. 在「外部資料來源」對話方塊中，執行下列操作：

   * 在「連線類型」部分，選取 `SAP HANA`。
   * 在「Connection ID」(連線 ID) 專區中輸入連線 ID，以識別這項連線。
   * 在「Location type」(位置類型) 中，指定要與 SAP Datasphere 資料合併的 BigQuery 資料集區域。使用這個連線的查詢必須從這個區域執行。
   * 選用：在「Friendly name」(好記名稱) 中輸入使用者容易記得的連線名稱，例如 `My connection resource`。好記名稱可以是任何資料值，只要您日後需要修改時可以輕鬆識別連線資源即可。
   * 選用：在「Description」(說明) 中輸入這項連線資源的說明。
   * 在「Encryption」(加密) 部分，選取「**Google-managed encryption key**」或「Customer-managed encryption key (CMEK)」(客戶自行管理的加密金鑰 (CMEK))。您可以選擇是否使用 CMEK。
   * 在「Host:port」(主機: 通訊埠) 部分，輸入 SAP 資料庫執行個體的主機和通訊埠，格式為 `HOST:PORT`，如 SAP Datasphere 網頁控制台的「Database User Details」(資料庫使用者詳細資料) 所示。
   * 選用：在「網路連結」中，輸入[網路連結](https://docs.cloud.google.com/bigquery/docs/connections-with-network-attachment?hl=zh-tw)的路徑，該連結會定義用於建立與 SAP Datasphere 連線的網路設定。
   * 在「Username」(使用者名稱) 中，輸入 SAP Datasphere 網頁版控制台「Database User Details」(資料庫使用者詳細資料) 中的資料庫使用者名稱。例如：`MY_SPACE#BIGQUERY`。
   * 在「Password」(密碼) 中輸入資料庫使用者的密碼。
7. 點選「建立連線」。

### bq

使用加上以下旗標的 [`bq mk`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_mk) 指令：

```
  bq mk \
  --connection \
  --location=LOCATION \
  --project_id=PROJECT_ID \
  --connector_configuration '{
    "connector_id": "saphana",
    "endpoint": {
      "host_port": "HOST_PORT"
    },
    "authentication": {
      "username_password": {
        "username": "USERNAME",
        "password": {
          "plaintext": "PASSWORD"
        }
      }
    },
    "network": {
      "private_service_connect": {
        "network_attachment": "NETWORK_ATTACHMENT"
      }
    }
  }' \
  CONNECTION_ID
```

更改下列內容：

* `LOCATION`：指定要與 SAP Datasphere 資料合併的 BigQuery 資料集區域。使用這個連線的查詢必須從這個區域執行。
* `PROJECT_ID`：輸入 Google Cloud 專案 ID。
* `HOST_PORT`：輸入 SAP 資料庫執行個體的主機和連接埠，格式為 `HOST:PORT`，如 SAP Datasphere 網頁控制台的「Database User Details」(資料庫使用者詳細資料) 所示。
* `NETWORK_ATTACHMENT` (選用)：以 `projects/{project}/regions/{region}/networkAttachments/{networkattachment}` 格式輸入[網路連結](https://docs.cloud.google.com/bigquery/docs/connections-with-network-attachment?hl=zh-tw)。您可以使用這個欄位設定 SAP Datasphere 連線，讓 BigQuery 從靜態 IP 位址開啟連線。
* `USERNAME`：在 SAP Datasphere 網頁版控制台的「Database User Details」(資料庫使用者詳細資料) 中，輸入資料庫使用者名稱。例如：`MY_SPACE#BIGQUERY`。
* `PASSWORD`：輸入資料庫使用者的密碼。
* `CONNECTION_ID`：輸入連線 ID，識別這個連線。

選用旗標：

* `--kms_key_name`：客戶自行管理的加密金鑰。如果省略此屬性，系統會以預設的 Google-owned and Google-managed encryption key保護憑證。

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
* 瞭解如何[查詢 SAP Datasphere 資料](https://docs.cloud.google.com/bigquery/docs/sap-datasphere-federated-queries?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-16 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-16 (世界標準時間)。"],[],[]]