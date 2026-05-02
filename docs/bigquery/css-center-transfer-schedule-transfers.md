* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [參考資料](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 排定 Comparison Shopping Service Center 轉移作業

**預覽**

這項產品適用《[服務專屬條款](https://docs.cloud.google.com/terms/service-terms?hl=zh-tw#1)》中「一般服務條款」一節的《正式發布前產品條款》。正式發布前的產品是按照「原樣」提供，支援範圍可能有限。
詳情請參閱[推出階段說明](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages)。

**注意：** 如要取得支援，或針對透過 BigQuery 資料移轉服務進行的購物比較服務 (CSS) 中心移轉作業提供意見回饋，請傳送電子郵件至 [gmc-transfer-preview@google.com](mailto:gmc-transfer-preview@google.com)。

本文將說明如何使用 [BigQuery 資料移轉服務](https://docs.cloud.google.com/bigquery/docs/dts-introduction?hl=zh-tw)，排定及管理 CSS Center 報表資料的週期性載入工作。

## 事前準備

建立 CSS Center 資料移轉作業前的準備事項如下：

* [啟用 BigQuery 資料移轉服務](https://docs.cloud.google.com/bigquery/docs/enable-transfer-service?hl=zh-tw)。
* [建立 BigQuery 資料集](https://docs.cloud.google.com/bigquery/docs/datasets?hl=zh-tw)來儲存 CSS Center 資料。
  + 資料集區域方面，我們支援在美國或歐盟使用預設選項「多區域」。
  + 如要在特定區域建立資料集，CSS Center 資料移轉功能僅支援下列區域：
  + `us-east4 (Northern Virginia)`、
  + `asia-northeast1 (Tokyo)`、
  + `asia-southeast1 (Singapore)`、
  + `australia-southeast1 (Sydney)`、
  + `europe-north1 (Finland)`、
  + `europe-west2 (London)`、
  + `europe-west6 (Zurich)`。
* 你必須擁有 CSS 網域 ID，才能建立 CSS Center 資料移轉作業。
* 如要為 Pub/Sub 設定移轉作業執行通知，您必須擁有 `pubsub.topics.setIamPolicy` 權限。如果您只想設定電子郵件通知，則不需要擁有 Pub/Sub 權限。詳情請參閱 [BigQuery 資料移轉服務執行通知](https://docs.cloud.google.com/bigquery/docs/transfer-run-notifications?hl=zh-tw)。

## 所需權限

確認您已授予下列權限。

### 必要的 BigQuery 角色

如要取得建立 BigQuery 資料移轉服務資料移轉作業所需的權限，請要求系統管理員在專案中授予您 [BigQuery 管理員](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.admin)  (`roles/bigquery.admin`) IAM 角色。如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

這個預先定義的角色具備建立 BigQuery 資料移轉服務資料移轉作業所需的權限。如要查看確切的必要權限，請展開「Required permissions」(必要權限) 部分：

#### 所需權限

如要建立 BigQuery 資料移轉服務資料移轉作業，您必須具備下列權限：

* BigQuery 資料移轉服務權限：
  + `bigquery.transfers.update`
  + `bigquery.transfers.get`
* BigQuery 權限：
  + `bigquery.datasets.get`
  + `bigquery.datasets.getIamPolicy`
  + `bigquery.datasets.update`
  + `bigquery.datasets.setIamPolicy`
  + `bigquery.jobs.create`

您或許還可透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)取得這些權限。

詳情請參閱「[授予 `bigquery.admin` 存取權](https://docs.cloud.google.com/bigquery/docs/enable-transfer-service?hl=zh-tw#grant_bigqueryadmin_access)」。

### 必要的 CSS Center 角色

您必須有權存取轉移設定中使用的 CSS Center 帳戶。

## 設定 CSS Center 轉移作業

如要建立 CSS Center 報表的資料移轉作業，請按照下列步驟操作：

### 控制台

1. 前往 Google Cloud 控制台的「資料移轉」頁面。

   [前往「資料轉移」頁面](https://console.cloud.google.com/bigquery/transfers?hl=zh-tw)
2. 按一下 add「建立轉移作業」。
3. 在「Create Transfer」(建立轉移作業) 頁面：

   * 在「Source type」(來源類型) 部分，「Source」(來源) 請選取「Google CSS Center」。
   * 在「Transfer config name」(轉移設定名稱) 部分，「Display name」(顯示名稱) 請輸入資料移轉作業的名稱，例如 `My Transfer`。移轉作業名稱可以是任意值，日後需要修改移轉作業時能夠據此識別。
   * 您無法設定「Schedule options」(排程選項) 部分，CSS Center 資料移轉作業的排程為每 24 小時執行一次。
   * 在「Destination settings」(目的地設定) 部分，「Destination dataset」(目的地資料集) 請選取您為了儲存資料而建立的資料集。
   * 在「Data source details」(資料來源詳細資料) 部分，「CSS ID」請輸入您的 CSS 網域 ID。
   * 選取要移轉的報表，詳情請參閱[支援的報表](https://docs.cloud.google.com/bigquery/docs/css-center-transfer?hl=zh-tw#supported_reports)相關說明。
   * (選用步驟) 在「Notification options」(通知選項) 部分執行下列操作：

     + 按一下啟用電子郵件通知的切換開關。當您啟用此選項時，移轉管理員會在移轉作業失敗時收到電子郵件通知。
     + 在「Select a Pub/Sub topic」(選取 Pub/Sub 主題) 選取[主題](https://docs.cloud.google.com/pubsub/docs/overview?hl=zh-tw#types)名稱，或是點選「Create a topic」(建立主題)。這個選項會針對資料移轉作業設定 Pub/Sub 執行[通知](https://docs.cloud.google.com/bigquery/docs/transfer-run-notifications?hl=zh-tw)。
4. 按一下 [儲存]。

### bq

輸入 `bq mk` 指令並提供移轉建立標記 - `--transfer_config`。還需加上以下旗標：

* `--data_source`
* `--target_dataset`
* `--display_name`
* `--params`

您還可以提供 `--project_id` 標記來指定特定專案。如果您沒有指定 `--project_id`，系統會使用預設專案。

```
bq mk \
--transfer_config \
--project_id=project_id \
--target_dataset=dataset \
--display_name=name \
--params='parameters' \
--data_source=data_source
```

其中：

* project\_id 是您的專案 ID。
* dataset 是資料移轉設定的目標資料集。
* name 是資料移轉設定的顯示名稱。移轉作業名稱可以是任意值，日後需要修改移轉作業時，能夠據此識別即可。
* parameters 含有已建立資料移轉設定的 JSON 格式參數。例如：`--params='{"param":"param_value"}'`。
  + `css_id`：CSS 網域 ID。
  + `export_products`：是否要轉移產品和產品問題資料。即使未指定 `export_products` 參數，系統預設也會納入這個參數。建議您明確加入這個參數，並將其設為 `true`。
* data\_source 是資料來源：`css_center`。

**注意：** 您無法使用指令列工具設定通知。

舉例來說，下列指令會使用 CSS 網域 ID `1234` 和目標資料集 `mydataset`，建立名為 `My Transfer` 的 CSS Center 資料移轉作業。資料移轉作業是在預設專案中建立。

```
bq mk \
--transfer_config \
--target_dataset=mydataset \
--display_name='My Transfer' \
--params='{"css_id":"1234","export_products":"true","export_regional_inventories":"true","export_local_inventories":"true","export_price_benchmarks":"true","export_best_sellers":"true"}' \
--data_source=css_center
```

首次執行指令時，您會收到類似以下的訊息：

`[URL omitted] Please copy and paste the above URL into your web browser and
follow the instructions to retrieve an authentication code.`

請按照訊息中的操作說明進行，在指令列中貼上驗證碼。

### API

請使用 [`projects.locations.transferConfigs.create`](https://docs.cloud.google.com/bigquery/docs/reference/datatransfer/rest/v1/projects.locations.transferConfigs/create?hl=zh-tw) 方法，並提供 [`TransferConfig`](https://docs.cloud.google.com/bigquery/docs/reference/datatransfer/rest/v1/projects.locations.transferConfigs?hl=zh-tw#TransferConfig) 資源的執行個體。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-02 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-02 (世界標準時間)。"],[],[]]