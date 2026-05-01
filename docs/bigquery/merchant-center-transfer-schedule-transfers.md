* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [參考資料](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 安排 Merchant Center 轉移作業

**預覽**

這項產品適用《[服務專屬條款](https://docs.cloud.google.com/terms/service-terms?hl=zh-tw#1)》中「一般服務條款」一節的《正式發布前產品條款》。正式發布前的產品是按照「原樣」提供，支援範圍可能有限。詳情請參閱[推出階段說明](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages)。

**注意：** 如要取得支援或提供使用 BigQuery 資料移轉服務進行 Merchant Center 移轉的意見，請傳送電子郵件至 [gmc-transfer-preview@google.com](mailto:gmc-transfer-preview@google.com)。

## 事前準備

建立 Merchant Center 資料移轉作業前，請先完成下列事項：

* 確認您已完成[啟用 BigQuery 資料移轉服務](https://docs.cloud.google.com/bigquery/docs/enable-transfer-service?hl=zh-tw)的一切必要動作。
* [建立 BigQuery 資料集](https://docs.cloud.google.com/bigquery/docs/datasets?hl=zh-tw)，儲存 Merchant Center 資料。
  + 資料集區域方面，我們支援在美國或歐盟使用預設選項「多區域」。
  + 如要在特定區域建立資料集，Merchant Center 資料移轉功能僅支援下列區域：
  + `us-east4 (Northern Virginia)`、
  + `asia-northeast1 (Tokyo)`、
  + `asia-southeast1 (Singapore)`、
  + `australia-southeast1 (Sydney)`、
  + `europe-north1 (Finland)`、
  + `europe-west2 (London)`、
  + `europe-west6 (Zurich)`。
* 如果您想要為 Pub/Sub 設定移轉作業執行通知，您必須擁有`pubsub.topics.setIamPolicy` 權限。如果您只想設定電子郵件通知，則不需要擁有 Pub/Sub 權限。詳情請參閱 [BigQuery 資料移轉服務執行通知](https://docs.cloud.google.com/bigquery/docs/transfer-run-notifications?hl=zh-tw)。

## 所需權限

確認您已授予下列權限。

### 必要的 BigQuery 角色

如要取得建立 BigQuery 資料移轉服務資料移轉作業所需的權限，請要求管理員在專案中授予您 [BigQuery 管理員](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.admin)  (`roles/bigquery.admin`) IAM 角色。如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

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

### 必要的 Merchant Center 角色

* 在移轉作業設定中所使用 Merchant Center 帳戶的[標準存取權](https://support.google.com/merchants/answer/1637190?hl=zh-tw)。如果使用服務帳戶設定轉移，[服務帳戶必須有權存取](https://developers.google.com/merchant/api/guides/authorization/access-your-account?hl=zh-tw#give-service-account-access-account) Merchant Center 帳戶。如要驗證存取權，請按一下 [Merchant Center 使用者介面](https://merchants.google.com/?hl=zh-tw)中的「使用者」部分。
* 如要存取價格競爭力、價格分析和暢銷商品資料，你必須符合[市場洞察的資格規定](https://support.google.com/merchants/answer/9712881?hl=zh-tw)。

## 設定 Merchant Center 轉移作業

如要設定 Merchant Center 報表的資料移轉作業，必須符合下列條件：

* **商家 ID** 或**多重客戶帳戶 ID**：這是[Merchant Center 使用者介面](https://merchants.google.com/mc?hl=zh-tw)中顯示的商家 ID。

如何建立 Merchant Center 報表的資料移轉作業：

### 控制台

1. 前往 Google Cloud 控制台的「資料移轉」頁面。

   [前往「資料轉移」頁面](https://console.cloud.google.com/bigquery/transfers?hl=zh-tw)
2. 按一下 add「建立轉移作業」。
3. 在「Create Transfer」(建立轉移作業) 頁面：

   * 在「Source type」(來源類型) 區段中，針對「Source」(來源) 選擇 [Google Merchant Center]。
   * 在「Transfer config name」(轉移設定名稱) 部分，「Display name」(顯示名稱) 請輸入資料移轉作業的名稱，例如 `My Transfer`。移轉作業名稱可以是任意值，日後需要修改移轉作業時能夠據此識別。
   * 在「Schedule options」(排程選項) 專區：

     + 選取**重複頻率**。如果選取「Hours」(小時)、「Days」(天)、「Weeks」(週)或「Months」(月)，必須一併指定頻率。您也可以選取「Custom」(自訂)，指定重複頻率。如果選取「On-demand」(隨選)，這項資料移轉作業會在您[手動觸發](https://docs.cloud.google.com/bigquery/docs/working-with-transfers?hl=zh-tw#manually_trigger_a_transfer)後執行。
     + 視情況選取「Start now」(立即開始) 或「Start at set time」(在所設時間開始執行)，並提供開始日期和執行時間。
     + 針對「Start date and run time」(開始日期和執行時間)，請輸入開始移轉作業的日期和時間。這個值至少須比當下的世界標準時間晚 24 小時。如果選取「Start now」(立即開始)，這個選項就會停用。

     如果將排程選項設為「Start now」(立即開始)，就會立即開始執行第一次資料移轉作業並失敗，錯誤訊息如下：`No data to transfer found for the Merchant account. If you
     have just created this transfer, you may need to wait for up to a day
     before the data of your Merchant account are prepared and available
     for the transfer.`。下次已排定的執行作業應該會成功執行。如果您的商家帳戶資料會在相同日期準備就緒 (以世界標準時間為準)，可以為今天的執行作業[設定補充作業](https://docs.cloud.google.com/bigquery/docs/working-with-transfers?hl=zh-tw#manually_trigger_a_transfer)。
   * 在「Destination settings」(目的地設定) 部分，「Destination dataset」(目的地資料集) 請選取您為了儲存資料而建立的資料集。
   * 在「Data source details」(資料來源詳細資料) 部分，「Merchant ID」(商家 ID) 請輸入您的商家 ID 或 MCA ID。選取要移轉的報表，詳情請參閱「[支援的報表](https://docs.cloud.google.com/bigquery/docs/merchant-center-transfer?hl=zh-tw#supported_reports)」。
   * 在「Service Account」(服務帳戶) 選單，選取與貴組織Google Cloud 專案相關聯的[服務帳戶](https://docs.cloud.google.com/iam/docs/service-account-overview?hl=zh-tw)。您可以將服務帳戶與資料移轉作業建立關聯，而非使用使用者憑證。如要進一步瞭解如何搭配使用服務帳戶與資料移轉作業，請參閱[使用服務帳戶](https://docs.cloud.google.com/bigquery/docs/use-service-accounts?hl=zh-tw)的相關說明。

     + 如果使用[聯合身分](https://docs.cloud.google.com/iam/docs/workforce-identity-federation?hl=zh-tw)登入，您必須擁有服務帳戶才能建立資料移轉作業。如果是以 [Google 帳戶](https://docs.cloud.google.com/iam/docs/principals-overview?hl=zh-tw#google-account)登入，則不一定要透過服務帳戶建立移轉作業。
     + 服務帳戶必須具備[必要權限](https://docs.cloud.google.com/bigquery/docs/merchant-center-transfer-schedule-transfers?hl=zh-tw#required_permissions)。
   * (選用步驟) 在「Notification options」(通知選項) 部分執行下列操作：

     + 按一下啟用電子郵件通知的切換開關。當您啟用此選項時，移轉管理員會在移轉作業失敗時收到電子郵件通知。
     + 在「Select a Pub/Sub topic」(選取 Pub/Sub 主題) 選取[主題](https://docs.cloud.google.com/pubsub/docs/overview?hl=zh-tw#types)名稱，或是點選「Create a topic」(建立主題)。這個選項會針對移轉作業設定 Pub/Sub 執行[通知](https://docs.cloud.google.com/bigquery/docs/transfer-run-notifications?hl=zh-tw)。
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
--service_account_name=service_account_name
```

其中：

* project\_id 是您的專案 ID。
* dataset 是移轉設定的目標資料集。
* name 是移轉設定的顯示名稱。移轉作業名稱可以是任意值，日後需要修改移轉作業時，能夠據此識別即可。
* parameters 含有已建立移轉設定的 JSON 格式參數，例如：`--params='{"param":"param_value"}'`。
  + 如要轉移 Merchant Center 資料，請提供 `merchant_id` 參數。
  + `export_products` 參數可指定是否要轉移產品和產品問題資料。即使未指定 `export_products` 參數，系統預設也會納入這個參數。Google 建議您明確加入這個參數，並將其設為「true」。
  + `export_regional_inventories` 參數會指定是否要轉移區域商品目錄資料。
  + `export_local_inventories` 參數會指定是否要轉移店面商品目錄資料。
  + `export_price_competitiveness` 參數可指定是否要轉移價格競爭力資料。
  + `export_price_insights` 參數可指定是否要轉移價格分析資料。
  + `export_best_sellers_v2` 參數可指定是否要轉移暢銷商品資料。
  + `export_performance` 參數可指定是否要轉移產品成效資料。
* data\_source 是資料來源：`merchant_center`。
* service\_account\_name 是用於驗證資料移轉作業的服務帳戶名稱。服務帳戶應由用於建立轉移作業的相同 `project_id` 所擁有，且應具備所有[必要權限](#required_permissions)。

**注意：** 您無法使用指令列工具設定通知。

舉例來說，下列指令會使用商家 ID `1234` 和目標資料集 `mydataset`，建立名為 `My Transfer` 的 Merchant Center 資料移轉作業。資料移轉作業是在預設專案中建立。

```
bq mk \
--transfer_config \
--target_dataset=mydataset \
--display_name='My Transfer' \
--params='{"merchant_id":"1234","export_products":"true","export_regional_inventories":"true","export_local_inventories":"true","export_price_benchmarks":"true","export_best_sellers":"true"}' \
--data_source=merchant_center
```

首次執行指令時，您會收到類似以下的訊息：

`[URL omitted] Please copy and paste the above URL into your web browser and
follow the instructions to retrieve an authentication code.`

請按照訊息中的操作說明進行，在指令列中貼上驗證碼。

**注意：** 當您使用指令列工具建立 Merchant Center 資料移轉作業時，系統會採用「Schedule」(排程) 的預設值 (移轉作業的建立時間，每 24 小時執行一次) 來設定移轉作業的設定。第一次移轉作業會立刻開始執行，且會執行失敗，並顯示以下錯誤訊息：「No data to transfer found for the Merchant account」(找不到該商家帳戶的資料來移轉)。

如果您才剛建立這項資料移轉作業，可能必須等待最多一天，才能讓您商家帳戶的資料準備就緒，以供移轉。下一次排定的移轉作業應該就能順利執行。如果你的商家帳戶資料會在相同日期準備就緒 (以世界標準時間為準)，可以為今天的執行作業[設定補充作業](https://docs.cloud.google.com/bigquery/docs/working-with-transfers?hl=zh-tw#manually_trigger_a_transfer)。

### API

請使用 [`projects.locations.transferConfigs.create`](https://docs.cloud.google.com/bigquery/docs/reference/datatransfer/rest/v1/projects.locations.transferConfigs/create?hl=zh-tw) 方法，並提供 [`TransferConfig`](https://docs.cloud.google.com/bigquery/docs/reference/datatransfer/rest/v1/projects.locations.transferConfigs?hl=zh-tw#TransferConfig) 資源的執行個體。

## 排解 Merchant Center 轉移設定問題

如果您無法順利設定資料移轉作業，請參閱[排解 BigQuery 資料移轉服務的移轉作業設定問題](https://docs.cloud.google.com/bigquery/docs/transfer-troubleshooting?hl=zh-tw)中的 [Merchant Center 移轉問題](https://docs.cloud.google.com/bigquery/docs/transfer-troubleshooting?hl=zh-tw#merchant)小節。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-04-30 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-04-30 (世界標準時間)。"],[],[]]