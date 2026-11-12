Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [參考資料](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 將 Stripe 資料載入 BigQuery

**預覽**

這項功能適用《[服務專屬條款](https://docs.cloud.google.com/terms/service-terms?hl=zh-tw#1)》中「一般服務條款」一節的《正式發布前產品條款》。正式發布前功能是依「原樣」提供，支援服務可能受限。
詳情請參閱[推出階段說明](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages)。

**注意：**如要取得支援或提供這項功能的意見回饋，請傳送電子郵件至 [dts-preview-support@google.com](mailto:dts-preview-support@google.com)。

您可以使用 Stripe 連接器搭配 [BigQuery 資料移轉服務](https://docs.cloud.google.com/bigquery/docs/dts-introduction?hl=zh-tw)，將資料從 Stripe 載入 BigQuery。使用 Stripe 連接器，即可排定週期性移轉工作，將 Stripe 的最新資料新增至 BigQuery。

## 限制

Stripe 資料移轉作業有下列限制：

* Stripe 資料移轉作業會根據 Stripe 的輔幣單位載入貨幣。詳情請參閱「[API 金額中的輔幣單位](https://docs.stripe.com/currencies#minor-units)」。
* Stripe 連接器只會為每個 Stripe 帳戶移轉預先產生的報表。Stripe 連接器不會根據新的 Stripe 資料產生新報表。
  + 如要移轉最新報表，請先在 Stripe 資訊主頁手動產生報表，再開始 Stripe 資料移轉作業。
  + 詳情請參閱「[Stripe 報表](https://docs.stripe.com/stripe-reports)」。
* Stripe 連接器不支援 Webhook 事件、即時更新或 Stripe Sigma。
* 從[預先發布版 Stripe 區域](https://stripe.com/global)移轉 Stripe 資料時，可能會遇到下列問題：
  + 在 Stripe 預先發布版區域，篩選選項會受到限制或無法使用。
  + Stripe 預先發布版區域不支援條件式資料移轉和查詢。
  + 從 Stripe 預先發布版區域移轉資料時，資料移轉作業可能需要較長時間。
* Stripe 連接器支援部分含有 `StartDate` 篩選器的物件。
  + `StartDate` 篩選器的必要格式為 `YYYY-MM-DD`。如未提供開始日期，連接器預設為目前日期前三年。如果提供的日期早於 2011 年 1 月 1 日，連接器會自動使用 2011 年 1 月 1 日。
  + 如需支援的物件清單，請參閱「[支援 `StartDate` 篩選器的物件](#objects_with_startdate_filter_support)」。
* 單一移轉設定在特定時間只能支援一項資料移轉作業。如果第二項資料移轉作業排定在第一項移轉作業完成前執行，則只有第一項資料移轉作業會完成，與第一項移轉作業重疊的其他資料移轉作業則會略過。
  + 為避免單一移轉設定略過移轉作業，建議您設定「重複頻率」，增加大型資料移轉作業之間的時間長度。
* 如果網路連結是在與 Google Cloud 資料移轉專案不同的 Google Cloud 專案中建立，您必須將 `compute.networkAttachments.get` 和 `compute.networkAttachments.update` 權限授予 Google Cloud 資料移轉專案的[服務代理](https://docs.cloud.google.com/bigquery/docs/enable-transfer-service?hl=zh-tw#service_agent)。

## 事前準備

以下各節說明建立 Stripe 資料移轉作業前，必須採取的步驟。

### Stripe 必要條件

* 您必須擁有 Stripe 開發人員帳戶，才能授權 Stripe 資料移轉。如要註冊 Stripe 帳戶，請參閱「[註冊 Stripe](https://dashboard.stripe.com/register)」。
* 請按照下列步驟設定 Stripe 平台應用程式：
  1. 前往 Stripe 資訊主頁的「Developers」部分。
  2. 在「Connect」下方，設定平台支援「Standard」和「Express」帳戶。
* 如要建立 Stripe 資料移轉作業，必須提供下列資訊：
  + 記下 Stripe 帳戶 ID。詳情請參閱「[建立帳戶](https://docs.stripe.com/get-started/account)」。
  + 記下密鑰或受限制金鑰。詳情請參閱「[API 金鑰](https://docs.stripe.com/keys)」。
* 如果您打算從連結帳戶轉移資料，請確認平台已設定 Stripe Connect，並具備必要帳戶功能的存取權。如要進一步瞭解 Stripe Connect，請參閱「[Platforms and marketplaces with Stripe Connect](https://docs.stripe.com/connect)」(Stripe Connect 支援的平台和市集)。
  + 如要進一步瞭解連結帳戶，請參閱「[連結帳戶類型](https://docs.stripe.com/connect/accounts)」。

### 必要的 BigQuery 角色

如要取得建立移轉作業所需的權限，請要求管理員授予您專案的 [BigQuery 管理員](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.admin) (`roles/bigquery.admin`) IAM 角色。如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

這個預先定義的角色具備建立移轉作業所需的權限。如要查看確切的必要權限，請展開「Required permissions」(必要權限) 部分：

#### 所需權限

您必須具備下列權限，才能建立移轉作業：

* `bigquery.transfers.update`
  使用者
* 目標資料集上的 `bigquery.datasets.get`
* 目標資料集上的 `bigquery.datasets.update`

您或許還可透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)取得這些權限。

### BigQuery 事前準備

* 確認您已完成[啟用 BigQuery 資料移轉服務](https://docs.cloud.google.com/bigquery/docs/enable-transfer-service?hl=zh-tw)的所有必要動作。
* 請[建立 BigQuery 資料集](https://docs.cloud.google.com/bigquery/docs/datasets?hl=zh-tw)來儲存您的資料。
* 如要設定 Pub/Sub 的移轉作業執行通知，請確認您具備 `pubsub.topics.setIamPolicy` Identity and Access Management (IAM) 權限。如果只設定電子郵件通知，則不需要 Pub/Sub 權限。詳情請參閱 [BigQuery 資料移轉服務執行通知](https://docs.cloud.google.com/bigquery/docs/transfer-run-notifications?hl=zh-tw)一文。

## Stripe 帳戶類型

Stripe 連接器支援 Stripe 平台帳戶和 Stripe 連結帳戶。詳 hip 請參閱「[連結帳戶類型](https://docs.stripe.com/connect/accounts)」。

### 連結平台帳戶

如要僅從一個平台帳戶執行 Stripe 資料移轉作業，請在[設定移轉設定](#transfer-setup)時執行下列操作：

* 在「Account Id」欄位中，輸入平台帳戶 ID。
* 在「Secret/API Key」欄位中，輸入平台帳戶的密鑰或受限金鑰。
* 在「SyncAllConnectedAccounts」部分，選取「False」。

如要為多個帳戶執行 Stripe 資料移轉作業 (例如與連結帳戶連結的平台帳戶)，請在[設定移轉設定](#transfer-setup)時執行下列操作：

* 在「Account Id」欄位中，輸入平台帳戶 ID。
* 在「Secret/API Key」欄位中，輸入平台帳戶的密鑰或受限金鑰。
* 在「SyncAllConnectedAccounts」部分，選取「True」。

### 連結至連結帳戶

連結帳戶是指使用 Stripe Connect 連結至 Stripe 的 Stripe 帳戶。

如要從連結帳戶執行 Stripe 資料移轉作業，請在[設定移轉設定](#transfer-setup)時，執行下列操作：

* 在「Account Id」欄位中，輸入連結帳戶的平台帳戶 ID。
* 在「Secret/API Key」(密鑰/API 金鑰) 欄位中，輸入連結帳戶所連結平台帳戶的密鑰或受限制金鑰。
* 在「SyncAllConnectedAccounts」部分，選取「False」。

## 設定 Stripe 資料移轉作業

使用下列任一選項設定移轉設定，將 Stripe 資料新增至 BigQuery：

### 控制台

1. 前往 Google Cloud 控制台的「資料移轉」頁面。

   [前往「資料移轉」](https://console.cloud.google.com/bigquery/transfers?hl=zh-tw)
2. 按一下「add 建立移轉作業」。
3. 在「Source type」(來源類型) 部分，「Source」(來源) 請選取「Stripe」。
4. 在「Data source details」(資料來源詳細資料) 部分執行下列操作：

   * 在「平台/連結帳戶 ID」部分，輸入 Stripe 帳戶 ID。詳情請參閱「[Stripe 必要條件](https://docs.cloud.google.com/bigquery/docs/stripe-transfer?hl=zh-tw#stripe-prerequisites)」。
   * 在「Stripe Secret Key」(Stripe 密鑰) 部分，輸入 Stripe 帳戶的 API 金鑰。詳情請參閱「[Stripe 必要條件](https://docs.cloud.google.com/bigquery/docs/stripe-transfer?hl=zh-tw#stripe-prerequisites)」。
   * 在「Start Date」(開始日期) 中，以 `YYYY-MM-DD` 格式輸入日期。資料移轉作業會從這個日期開始載入 Stripe 資料。
   * 選取「同步處理所有連結帳戶」，即可同步處理所有連結帳戶。
   * 在「Stripe objects to transfer」(要移轉的 Stripe 物件)，輸入要移轉的 Stripe 物件名稱，或是點選「Browse」(瀏覽) 並選取要移轉的物件。
5. 在「Destination settings」(目的地設定) 部分，「Dataset」(資料集) 請選取您為了儲存資料而建立的資料集。
6. 在「Transfer config name」(轉移設定名稱) 部分，「Display name」(顯示名稱) 請輸入資料移轉作業的名稱。
7. 在「Schedule options」(排程選項) 部分執行下列操作：

   * 在「Repeat frequency」(重複頻率) 清單選取選項，指定這項資料移轉作業的執行頻率。如要指定自訂重複頻率，請選取「Custom」(自訂)。如果選取「On-demand」(隨選)，這項移轉作業會在您[手動觸發](https://docs.cloud.google.com/bigquery/docs/working-with-transfers?hl=zh-tw#manually_trigger_a_transfer)後執行。
   * 視情況選取「Start now」(立即開始) 或「Start at set time」(在所設時間開始執行)，並提供開始日期和執行時間。
8. 選用：在「Notification options」(通知選項) 專區，執行下列操作：

   * 如要啟用電子郵件通知，請點選「Email notification」(電子郵件通知) 切換按鈕。啟用這個選項後，若移轉失敗，移轉作業管理員就會收到電子郵件通知。
   * 如要為這項移轉作業啟用 [Pub/Sub 移轉作業執行通知](https://docs.cloud.google.com/bigquery/docs/transfer-run-notifications?hl=zh-tw)，請點選「Pub/Sub notifications」(Pub/Sub 通知) 切換按鈕。您可以選取[主題](https://docs.cloud.google.com/pubsub/docs/overview?hl=zh-tw#types)名稱，或點選「Create a topic」(建立主題) 來建立主題。
9. 按一下「儲存」。

### bq

輸入 [`bq mk` 指令](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_mk)，並提供移轉作業建立旗標 `--transfer_config`：

```
bq mk
    --transfer_config
    --project_id=PROJECT_ID
    --data_source=DATA_SOURCE
    --display_name=DISPLAY_NAME
    --target_dataset=DATASET
    --params='PARAMETERS'
```

其中：

* PROJECT\_ID (選用)：您的 Google Cloud 專案 ID。如未提供 `--project_id` 來指定特定專案，系統會使用預設專案。
* DATA\_SOURCE：資料來源 - `stripe`。
* DISPLAY\_NAME：資料移轉設定的顯示名稱。移轉作業名稱可以是任意值，日後需要修改移轉作業時，能夠據此識別即可。
* DATASET：移轉設定的目標資料集。
* PARAMETERS：JSON 格式的已建立移轉設定參數。例如：`--params='{"param":"param_value"}'`。以下是 Stripe 資料移轉的參數：

  + `assets`：要納入這項移轉作業的 Stripe 物件清單。
  + `connector.accountId`：Stripe 帳戶 ID。
  + `connector.secretKey`：Stripe 帳戶的 API 金鑰。
  + `connector.syncAllConnectedAccounts`：指定 `true` 即可同步所有連結帳戶。
  + `connector.startDate`：輸入日期，格式為 `YYYY-MM-DD`。資料移轉作業會從這個日期開始載入 Stripe 資料。

舉例來說，下列指令會在預設專案中建立 Stripe 資料移轉作業，並提供所有必要參數：

```
  bq mk \
      --transfer_config \
      --target_dataset=mydataset \
      --data_source=stripe \
      --display_name='My Transfer' \
      --params= ' {
  "assets" : [ "Customers" , "Accounts", "BalanceSummaryReport"] ,
  "connector.accountId" : "acct_000000000000",
  "connector.secretKey" : "sk_test_000000000",
  "connector.syncAllConnectedAccounts" : "true",
  "connector.startDate": "2025-05-20"
  }'
```

### API

請使用 [`projects.locations.transferConfigs.create` 方法](https://docs.cloud.google.com/bigquery/docs/reference/datatransfer/rest/v1/projects.locations.transferConfigs/create?hl=zh-tw)，並提供 [`TransferConfig` 資源](https://docs.cloud.google.com/bigquery/docs/reference/datatransfer/rest/v1/projects.locations.transferConfigs?hl=zh-tw#TransferConfig)的例項。

儲存移轉設定時，Stripe 連接器會根據您的排程選項，自動觸發移轉作業。每次執行移轉作業時，Stripe 連接器都會將 Stripe 中的所有可用資料移轉至 BigQuery。

如要在排程時間以外手動執行資料移轉作業，可以啟動[補充執行作業](https://docs.cloud.google.com/bigquery/docs/working-with-transfers?hl=zh-tw#manually_trigger_a_transfer)。

## 資料類型對應

下表列出 Stripe 資料類型與對應 BigQuery 資料類型的對應關係。

| Stripe 資料類型 | BigQuery 資料類型 | 附註 |
| --- | --- | --- |
| `String` | `STRING` |
| `Dictionary` | `STRING` | 巢狀物件載入 BigQuery 時，會轉換為扁平化物件。接著，這個扁平化物件會以單一常值字串的形式儲存在資料表中。 |
| `Integer` | `INT64` |
| `Double` | `DOUBLE` |
| `Float` | `FLOAT` |
| `Decimal` | `BIGNUMERIC` |
| `BigInt (long)` | `BIGNUMERIC` |
| `Boolean` | `BOOL` |
| `Datetime` | `TIMESTAMP` |
| `Unix timestamp` | `TIMESTAMP` |

## 支援`StartDate`篩選器的物件

下列 Stripe 物件支援 `StartDate` 篩選器，可讓您載入時間資料：

* 帳戶
* 收費金額
* 優待券
* 客戶
* 爭議
* InvoiceItems
* 帳單
* PaymentIntent
* 款項撥付
* 方案
* 價格
* 產品
* PromotionCodes
* 退款
* ShippingRates
* 訂閱項目
* TaxRates
* TopUps
* 移轉
* ValueListItems
* ValueLists

## 排解轉移設定問題

如果無法順利設定資料移轉作業，請參閱「[Stripe 移轉問題](https://docs.cloud.google.com/bigquery/docs/transfer-troubleshooting?hl=zh-tw#stripe-issues)」。

## 定價

這項功能目前為[預先發布版](https://cloud.google.com/products?hl=zh-tw#product-launch-stages)，將 Stripe 資料移轉至 BigQuery 不會產生費用。

## 後續步驟

* 如需 BigQuery 資料移轉服務的總覽，請參閱「[BigQuery 資料移轉服務簡介](https://docs.cloud.google.com/bigquery/docs/dts-introduction?hl=zh-tw)」。
* 如要瞭解如何使用移轉作業，包括取得移轉設定、列出移轉設定以及查看移轉設定的執行記錄，請參閱[使用移轉功能](https://docs.cloud.google.com/bigquery/docs/working-with-transfers?hl=zh-tw)一文。
* 瞭解如何[透過 BigQuery Omni 作業載入資料](https://docs.cloud.google.com/bigquery/docs/load-data-using-cross-cloud-transfer?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-11-11 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-11-11 (世界標準時間)。"],[],[]]