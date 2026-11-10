Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [參考資料](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 將 PayPal 資料載入 BigQuery

**預覽**

這項功能適用《[服務專屬條款](https://docs.cloud.google.com/terms/service-terms?hl=zh-tw#1)》中「一般服務條款」一節的《正式發布前產品條款》。正式發布前功能是依「原樣」提供，支援服務可能受限。
詳情請參閱[推出階段說明](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages)。

**注意：**如要取得支援或提供這項功能的意見回饋，請傳送電子郵件至 [dts-preview-support@google.com](mailto:dts-preview-support@google.com)。

您可以透過 PayPal 連接器，使用 [BigQuery 資料移轉服務](https://docs.cloud.google.com/bigquery/docs/dts-introduction?hl=zh-tw)將資料從 PayPal 載入 BigQuery。使用 PayPal 連接器，即可排定週期性移轉工作，將 PayPal 的最新資料新增至 BigQuery。

PayPal 連接器支援正式環境和沙箱 PayPal 帳戶。

## 支援的物件

| PayPal 物件類型 | BigQuery 支援的物件 | 日期篩選器支援 | 轉移限制 |
| --- | --- | --- | --- |
| 交易 | TransactionReports | 支援 | 過去 3 年 |
| TransactionReportsCartInfoItemDetails | 支援 |
| TransactionReportsIncentiveDetails | 支援 |
| 爭議 | 爭議 | 支援 | 最近 6 個月 |
| DisputeDetails | 支援 |
| DisputeTransactions | 支援 |
| 付款 | 付款 | 支援 | 無 |
| PaymentTransactions | 支援 |
| 餘額 | 餘額 | 不支援 | 無 |
| 產品 | 產品 | 不支援 | 2,000,000 筆記錄 |
| ProductDetails | 不支援 |
| 帳單 | 帳單 | 支援 | 100,000 筆記錄 |

## 限制

PayPal 資料移轉作業有下列限制：

* PayPal 交易可能需要幾小時，才會顯示在 PayPal API 中。
  + 建議您將後續資料移轉作業排定在較長的時間間隔 (每小時不超過一次)，以免遺失資料。
* PayPal 連接器僅支援過去 3 年的[交易資料](#supported_objects)。
* PayPal 連接器僅支援過去 6 個月的[爭議資料](#supported_objects)。
* PayPal 連接器最多只能移轉 100,000 筆[應付憑據資料](#supported_objects)記錄。如果 PayPal 的應付憑據數量超過這個上限，轉移作業就會失敗。
* PayPal 連接器最多只能移轉 2,000,000 筆目錄[產品資料](#supported_objects)記錄。如果 PayPal 中的產品數量超過這項限制，轉移作業就會失敗。
* PayPal API 會針對每個資料物件使用不同的頁面大小限制。PayPal 連接器會使用 PayPal 允許的資料移轉頁面大小上限。
  + 不過，某些物件 (例如 `Payments` 或 `Payment Transactions`) 的頁面大小限制較小。這可能會導致資料移轉速度變慢，尤其是在處理大型資料集時。
* 如果網路連結是在與 Google Cloud 資料移轉專案不同的 Google Cloud 專案中建立，您必須將 `compute.networkAttachments.get` 和 `compute.networkAttachments.update` 權限授予 Google Cloud 資料移轉專案的[服務代理](https://docs.cloud.google.com/bigquery/docs/enable-transfer-service?hl=zh-tw#service_agent)。

## 事前準備

以下各節說明建立 PayPal 資料移轉作業前，必須採取的步驟。

### PayPal 必要條件

如要啟用 PayPal 資料移轉作業，您必須具備下列條件：

* 你必須擁有 PayPal 開發人員帳戶。詳情請參閱 [PayPal Developer Program](https://developer.paypal.com/developer-program/)。
* 建立 PayPal REST API 應用程式。詳情請參閱「[開始使用 PayPal REST API](https://developer.paypal.com/api/rest/)」。
  + 在「Apps & Credentials」(應用程式和憑證) 部分，記下應用程式的用戶端 ID 和密鑰。
  + 在「Features」(功能) 部分，啟用「Transaction search」(交易搜尋) 和「Invoicing」(開立應付憑據) API 權限。

### 必要的 BigQuery 角色

如要取得建立移轉作業所需的權限，請要求管理員授予您 [BigQuery 管理員](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.admin) (`roles/bigquery.admin`) IAM 角色。如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

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

## 設定 PayPal 資料移轉作業

如要將 PayPal 資料新增至 BigQuery，請使用下列任一選項設定移轉設定：

### 控制台

1. 前往 Google Cloud 控制台的「資料移轉」頁面。

   [前往「資料移轉」](https://console.cloud.google.com/bigquery/transfers?hl=zh-tw)
2. 按一下「add 建立移轉作業」。
3. 在「Source type」(來源類型) 部分，「Source」(來源) 請選取「PayPal」。
4. 在「Data source details」(資料來源詳細資料) 部分執行下列操作：

   * 在「Client Id」(用戶端 ID) 中，輸入 PayPal 用戶端 ID。詳情請參閱「[PayPal 必要條件](https://docs.cloud.google.com/bigquery/docs/paypal-transfer?hl=zh-tw#paypal-prerequisites)」。
   * 在「Client Secret」(用戶端密鑰) 部分，輸入 PayPal 用戶端密鑰。詳情請參閱「[PayPal 必要條件](https://docs.cloud.google.com/bigquery/docs/paypal-transfer?hl=zh-tw#paypal-prerequisites)」。
   * 如果您使用的是沙箱 PayPal 帳戶，請選取「Is Sandbox」。
   * 在「Start Date」(開始日期) 中，以 `YYYY-MM-DD` 格式輸入日期。資料移轉作業會從這個日期開始載入 PayPal 資料。
     + 如果這個欄位留空，這項移轉作業預設會擷取過去 3 年的資料。
     + 如要瞭解哪些物件支援開始日期篩選器，請參閱「[支援的物件](https://docs.cloud.google.com/bigquery/docs/paypal-transfer?hl=zh-tw#supported_objects)」。
   * 在「PayPal objects to transfer」(要移轉的 PayPal 物件)，輸入要移轉的 PayPal 物件名稱，或是點選「Browse」(瀏覽) 並選取要移轉的物件。
5. 在「Destination settings」(目的地設定) 部分，「Dataset」(資料集) 請選取您為了儲存資料而建立的資料集。
6. 在「Transfer config name」(轉移設定名稱) 部分，「Display name」(顯示名稱) 請輸入資料移轉作業的名稱。
7. 在「Schedule options」(排程選項) 部分執行下列操作：

   * 在「Repeat frequency」(重複頻率) 清單選取選項，指定這項資料移轉作業的執行頻率。如要指定自訂重複頻率，請選取「Custom」(自訂)。如果選取「On-demand」(隨選)，這項移轉作業會在您[手動觸發](https://docs.cloud.google.com/bigquery/docs/working-with-transfers?hl=zh-tw#manually_trigger_a_transfer)後執行。
   * 視情況選取「Start now」(立即開始) 或「Start at set time」(在所設時間開始執行)，並提供開始日期和執行時間。
8. 選用：在「Notification options」(通知選項) 專區，執行下列操作：

   * 如要啟用電子郵件通知，請將「Email notification」(電子郵件通知) 切換鈕設為開啟。當您啟用此選項時，移轉管理員會在移轉作業失敗時收到電子郵件通知。
   * 如要為這項移轉作業啟用 [Pub/Sub 移轉作業執行通知](https://docs.cloud.google.com/bigquery/docs/transfer-run-notifications?hl=zh-tw)，請將「Pub/Sub notifications」(Pub/Sub 通知) 切換至開啟位置。您可以選取[主題](https://docs.cloud.google.com/pubsub/docs/overview?hl=zh-tw#types)名稱，也可以點選「Create a topic」(建立主題) 來建立主題。
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
* DATA\_SOURCE：資料來源 - `paypal`。
* DISPLAY\_NAME：資料移轉設定的顯示名稱。移轉作業名稱可以是任意值，日後需要修改移轉作業時，能夠據此識別即可。
* DATASET：移轉設定的目標資料集。
* PARAMETERS：JSON 格式的已建立移轉設定參數。例如：`--params='{"param":"param_value"}'`。以下是 PayPal 資料移轉的參數：

  + `assets`：要納入這項移轉作業的 PayPal 物件清單。
  + `connector.authentication.clientId`：PayPal 應用程式的用戶端 ID。
  + `connector.authentication.clientSecret`：PayPal 應用程式的用戶端密鑰。
  + `connector.isSandbox`：如果您使用沙箱 PayPal 帳戶，請將值設為 `true`；如果您使用正式版 PayPal 帳戶，請將值設為 `false`。
  + `connector.createdStartDate`：(選用) 輸入日期，格式為 `YYYY-MM-DD`。資料移轉作業會從這個日期開始載入 PayPal 資料。

舉例來說，下列指令會在預設專案中建立 PayPal 資料移轉作業，並提供所有必要參數：

```
  bq mk \
      --transfer_config \
      --target_dataset=mydataset \
      --data_source=PayPal \
      --display_name='My Transfer' \
      --params='{"assets":  ["Payments", "TransactionReports"],
          "connector.authentication.clientId": "112233445566",
          "connector.authentication.clientSecret":"123456789",
          "connector.isSandbox":"false",
          "connector.createdStartDate":  "2025-01-01"}'
```

使用 bq 指令列工具建立資料移轉作業時，移轉設定會每 8 小時排定一次資料移轉作業。

**附註：**如果使用 bq 指令列工具設定移轉設定，就無法設定通知。

### API

請使用 [`projects.locations.transferConfigs.create` 方法](https://docs.cloud.google.com/bigquery/docs/reference/datatransfer/rest/v1/projects.locations.transferConfigs/create?hl=zh-tw)，並提供 [`TransferConfig` 資源](https://docs.cloud.google.com/bigquery/docs/reference/datatransfer/rest/v1/projects.locations.transferConfigs?hl=zh-tw#TransferConfig)的例項。

儲存移轉設定後，PayPal 連接器會根據您的排程選項，自動觸發移轉作業。每次執行移轉作業時，PayPal 連接器都會將 PayPal 中的所有可用資料移轉至 BigQuery。

如要在排程時間以外手動執行資料移轉作業，可以啟動[補充執行作業](https://docs.cloud.google.com/bigquery/docs/working-with-transfers?hl=zh-tw#manually_trigger_a_transfer)。

## 資料類型對應

下表列出 PayPal 資料類型與對應 BigQuery 資料類型的對應關係。

| PayPal 資料類型 | BigQuery 資料類型 |
| --- | --- |
| `String` | `STRING` |
| `Decimal` | `BIGNUMERIC` |
| `Boolean` | `BOOL` |
| `Datetime` | `TIMESTAMP` |

## 排解轉移設定問題

如果無法順利設定資料移轉作業，請參閱「[PayPal 移轉問題](https://docs.cloud.google.com/bigquery/docs/transfer-troubleshooting?hl=zh-tw#paypal-issues)」一文。

## 定價

這項功能目前為[預先發布版](https://cloud.google.com/products?hl=zh-tw#product-launch-stages)，將 PayPal 資料移轉至 BigQuery 不會產生費用。

## 後續步驟

* 如需 BigQuery 資料移轉服務的總覽，請參閱「[BigQuery 資料移轉服務簡介](https://docs.cloud.google.com/bigquery/docs/dts-introduction?hl=zh-tw)」。
* 如要瞭解如何管理移轉設定，包括如何取得資訊、列出設定及查看執行記錄，請參閱「[管理移轉作業](https://docs.cloud.google.com/bigquery/docs/working-with-transfers?hl=zh-tw)」。
* 瞭解如何[透過 BigQuery Omni 作業載入資料](https://docs.cloud.google.com/bigquery/docs/load-data-using-cross-cloud-transfer?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-11-10 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-11-10 (世界標準時間)。"],[],[]]