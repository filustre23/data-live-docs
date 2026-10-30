Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 連線至 AlloyDB for PostgreSQL

在 BigQuery 中，AlloyDB for PostgreSQL [連線](https://docs.cloud.google.com/bigquery/docs/connections-api-intro?hl=zh-tw)可讓使用者即時[查詢 AlloyDB 中的資料](https://docs.cloud.google.com/bigquery/docs/alloydb-federated-queries?hl=zh-tw)，不必將資料複製或移至 BigQuery。如要設定這項連線，請[建立 AlloyDB 連線](#create-alloydb-connection)，並[授予服務帳戶存取權](#access-alloydb)。

## 事前準備

1. 啟用 BigQuery Connection API。  

   [啟用 API](https://console.cloud.google.com/apis/library/bigqueryconnection.googleapis.com?hl=zh-tw)
2. 如要取得建立 AlloyDB 連線所需的權限，請要求管理員授予您專案的 [BigQuery 連線管理員](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.connectionAdmin)  (`roles/bigquery.connectionAdmin`) IAM 角色。如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

   您或許也能透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)，取得必要權限。

## 建立 AlloyDB 連線

連線至 AlloyDB 時，建議您使用連線來處理資料庫憑證。連線會經過加密，並安全地儲存在 BigQuery 連線服務中。如果使用者憑證對來源中的其他資料有效，您可以重複使用連線。例如，您可以使用一個連線，多次查詢 AlloyDB 執行個體中的同一個資料庫。

選取下列其中一個選項，建立 AlloyDB 連線：

### 控制台

1. 前往「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在「Explorer」窗格中，點選「add 新增」。

   「新增資料」對話方塊隨即開啟。
3. 在「篩選依據」窗格的「資料來源類型」部分，選取「資料庫」。

   或者，您也可以在「Search for data sources」(搜尋資料來源) 欄位中輸入 `alloydb`。
4. 在「精選資料來源」部分，按一下「Google Cloud AlloyDB」。
5. 點選「AlloyDB: BigQuery Federation」解決方案資訊卡。
6. 在「外部資料來源」對話方塊，輸入下列資訊：

   * 在「Connection type」(連線類型) 部分，選取「AlloyDB」。
   * 在「Connection ID」(連線 ID) 專區中輸入連線資源的 ID。可以使用英文字母、數字和底線，例如：`bq_alloydb_connection`。
   * 在「Data location」(資料位置) 部分，選取[與外部資料來源區域相容](https://docs.cloud.google.com/bigquery/docs/federated-queries-intro?hl=zh-tw#supported_regions)的 BigQuery 位置 (或區域)。
   * (選用) 在「Friendly name」(好記名稱) 部分，輸入使用者容易記得的連線名稱，例如 `My connection resource`。這可以是任何值，只要日後需修改時能輕鬆識別即可。
   * 選用：在「Description」(說明) 部分，輸入這項連線資源的說明。
   * 選用：**加密**：如要使用[客戶自行管理的加密金鑰 (CMEK)](https://docs.cloud.google.com/bigquery/docs/customer-managed-encryption?hl=zh-tw) 加密憑證，請選取「客戶自行管理的加密金鑰 (CMEK)」，然後選取客戶自行管理的金鑰。否則，憑證會受到預設 Google-owned and Google-managed encryption key保護。
   * 在「Database name」(資料庫名稱) 中輸入資料庫名稱。
   * 在「Database username」(資料庫使用者名稱) 部分，輸入資料庫的使用者名稱。
   * 在「Database password」(資料庫密碼) 部分，輸入資料庫密碼。
     + 選用：如要查看密碼，請按一下 
       visibility\_off 「顯示密碼」。
   * 在「AlloyDB Instance」(AlloyDB 執行個體) 部分，輸入 AlloyDB 主要或唯讀執行個體的連線 URI，並加上 **//alloydb.googleapis.com** 前置字串。

     + URI 範例：`//alloydb.googleapis.com/projects/PROJECT_ID/locations/REGION_ID/clusters/CLUSTER_NAME/instances/INSTANCE_ID`**注意：** 如果相同的使用者憑證對外部資料來源中的其他資料庫有效，該使用者可以透過相同的連線資源查詢這些資料庫。
7. 點選「建立連線」。
8. 點選「前往連線」。
9. 在「連線資訊」窗格中，複製服務帳戶 ID，以便在[下一個步驟](https://docs.cloud.google.com/bigquery/docs/connect-to-alloydb?hl=zh-tw#access-alloydb)中授予正確的 IAM 權限。

### bq

輸入 [`bq mk`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_mk) 指令，並加上下列旗標：

```
  bq mk \
  --connection \
  --location=LOCATION \
  --project_id=PROJECT_ID \
  --connector_configuration '{
    "connector_id": "google-alloydb",
    "asset": {
      "database": "DATABASE",
      "google_cloud_resource": "RESOURCE_PATH"
    },
    "authentication": {
      "username_password": {
        "username": "USERNAME",
        "password": {
          "plaintext": "PASSWORD"
        }
      }
    }
  }' \
  CONNECTION_ID
```

更改下列內容：

* `LOCATION`：指定要與 AlloyDB 資料合併的 BigQuery 資料集區域。使用這個連線的查詢必須從這個區域執行。
* `PROJECT_ID`：輸入 Google Cloud 專案 ID。
* `DATABASE`：輸入資料庫名稱。
* `RESOURCE_PATH`：輸入 AlloyDB 主要或唯讀執行個體的連線 URI，並加上 **//alloydb.googleapis.com** 前置字元。
  + URI 範例：`//alloydb.googleapis.com/projects/PROJECT_ID/locations/REGION_ID/clusters/CLUSTER_NAME/instances/INSTANCE_ID`
* `USERNAME`：輸入資料庫使用者名稱。
* `PASSWORD`：輸入資料庫使用者的密碼。
* `CONNECTION_ID`：輸入連線 ID，用於識別這項
  連線。

選用旗標：

* `--kms_key_name`：客戶自行管理的加密金鑰。如果省略，憑證會受到預設 Google-owned and Google-managed encryption key保護。

### API

在 BigQuery Connection API 中，您可以叫用 `ConnectionService` 內的 `CreateConnection`，將連線例項化。詳情請參閱[用戶端程式庫頁面](https://docs.cloud.google.com/bigquery/docs/reference/bigqueryconnection?hl=zh-tw)。

## 將存取權授予服務帳戶

在專案中建立第一個連線時，系統會自動建立[服務帳戶](https://docs.cloud.google.com/iam/docs/service-agents?hl=zh-tw)。服務帳戶名稱為 **BigQuery Connection 服務代理**。如要取得服務帳戶 ID，請[查看連線詳細資料](https://docs.cloud.google.com/bigquery/docs/working-with-connections?hl=zh-tw#view-connections)。服務帳戶 ID 的格式如下：

`service-PROJECT_NUMBER@gcp-sa-bigqueryconnection.iam.gserviceaccount.com`。

**注意：** 連線使用的服務帳戶是 Google 代管的服務代理。根據設計，這個服務帳戶預設不會顯示在「IAM & Admin」(IAM 與管理) 頁面上。如要在「IAM & Admin」(IAM 與管理) 頁面查看 Google 提供的角色授權，請勾選「Include Google-provided role grants」(包含 Google 提供的角色授權) 核取方塊。

如要連線至 AlloyDB，您必須授予新連線 AlloyDB 存取權，讓 BigQuery 能代使用者存取資料。服務帳戶必須具備下列權限：

* `alloydb.instances.connect`

您可以將 [AlloyDB 用戶端 IAM 角色](https://docs.cloud.google.com/alloydb/docs/reference/iam-roles-permissions?hl=zh-tw#roles)授予與連線相關聯的服務帳戶，該角色已具備這項權限。如果服務帳戶已具備必要權限，則可略過這個步驟。

### 控制台

1. 前往「IAM & Admin」(IAM 與管理) 頁面。

   [前往「IAM & Admin」(IAM 與管理) 頁面](https://console.cloud.google.com/project/_/iam-admin?hl=zh-tw)
2. 按一下 person\_add「Grant Access」(授予存取權)。

   「Add principals」(新增主體) 對話方塊隨即開啟。
3. 在「New principals」(新增主體) 欄位中，輸入從[連線資訊](https://docs.cloud.google.com/bigquery/docs/working-with-connections?hl=zh-tw#view-connections)取得的服務帳戶 ID。
4. 在「指派角色」部分，選取「AlloyDB 用戶端」(`roles/alloydb.client`)。
5. 按一下 [儲存]。

### gcloud

使用 [`gcloud projects add-iam-policy-binding`](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw#grant-single-role) 指令：

```
gcloud projects add-iam-policy-binding PROJECT_ID --member=serviceAccount:SERVICE_ACCOUNT_ID --role=roles/alloydb.client
```

提供以下這些值：

* `PROJECT_ID`： Google Cloud 專案 ID。
* `SERVICE_ACCOUNT_ID`：從[連線資訊](https://docs.cloud.google.com/bigquery/docs/working-with-connections?hl=zh-tw#view-connections)取得的服務帳戶 ID。

**注意：** 如要進一步瞭解如何授予及撤銷 IAM 角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw#view-access)」。

## 與使用者共用連線

您可以授予下列角色，讓使用者查詢資料及管理連結：

* `roles/bigquery.connectionUser`：可讓使用者透過連線，連至外部資料來源並執行查詢。
* `roles/bigquery.connectionAdmin`：可讓使用者管理連線。

如要進一步瞭解 BigQuery 的 IAM 角色和權限，請參閱「[預先定義的角色和權限](https://docs.cloud.google.com/bigquery/access-control?hl=zh-tw)」。

選取下列選項之一：

### 控制台

1. 前往「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)

   連線會列在專案中名為「Connections」(連線)  的群組。
2. 點選左側窗格中的 explore「Explorer」。

   如果沒有看到左側窗格，請按一下 last\_page「Expand left pane」(展開左側窗格)，開啟窗格。
3. 在「Explorer」窗格中，展開專案名稱。
4. 按一下「連線」，然後點選連線。
5. 在「詳細資料」窗格中，按一下「共用」即可共用連線。接著，按照下列步驟操作：

   1. 在「Connection permissions」(連線權限) 對話方塊中，新增或編輯主體，與其他主體共用連線。
   2. 按一下 [儲存]。

### bq

使用下列 [`set-iam-policy` 指令](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_set-iam-policy)：

```
  bq set-iam-policy RESOURCE FILE_NAME
```

更改下列內容：

* `RESOURCE`：請以 `project_id.region.connection_id` 或 `region.connection_id` 格式輸入資源名稱。
* `FILE_NAME`：輸入包含 JSON 格式 IAM 政策的檔案名稱。

如要進一步瞭解 set-iam-policy 指令，請參閱「[使用 IAM 控管資源存取權](https://docs.cloud.google.com/bigquery/docs/control-access-to-resources-iam?hl=zh-tw#bq)」。

### API

使用 BigQuery Connections REST API 參考資料區段中的 [`projects.locations.connections.setIAM` 方法](https://docs.cloud.google.com/bigquery/docs/reference/bigqueryconnection/rest/v1/projects.locations.connections?hl=zh-tw#methods)，並提供 `policy` 資源的執行個體。

## 後續步驟

* 瞭解不同的[連線類型](https://docs.cloud.google.com/bigquery/docs/connections-api-intro?hl=zh-tw)。
* 瞭解如何[管理連結](https://docs.cloud.google.com/bigquery/docs/working-with-connections?hl=zh-tw)。
* 瞭解[聯合查詢](https://docs.cloud.google.com/bigquery/docs/federated-queries-intro?hl=zh-tw)。
* 瞭解如何[查詢 AlloyDB 資料](https://docs.cloud.google.com/bigquery/docs/alloydb-federated-queries?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-10-29 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-10-29 (世界標準時間)。"],[],[]]