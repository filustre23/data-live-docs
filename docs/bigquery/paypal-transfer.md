Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

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

**注意：** 如要取得支援或針對這項功能提供意見回饋，請傳送電子郵件至 [dts-preview-support@google.com](mailto:dts-preview-support@google.com)。

您可以使用 PayPal 連接器和 [BigQuery 資料移轉服務](https://docs.cloud.google.com/bigquery/docs/dts-introduction?hl=zh-tw)，將 PayPal 資料載入 BigQuery。透過 PayPal 連接器，您可以安排週期性移轉工作，將 PayPal 的最新資料新增至 BigQuery。

PayPal 連接器支援正式環境和沙箱 PayPal 帳戶。

## 支援的物件

| PayPal 物件類型 | BigQuery 支援的物件 | 支援日期篩選器 |
| --- | --- | --- |
| 交易 | TransactionReports | 支援 |
| TransactionReportsCartInfoItemDetails | 支援 |
| TransactionReportsIncentiveDetails | 支援 |
| 爭議 | 爭議 | 支援 |
| DisputeDetails | 支援 |
| DisputeTransactions | 支援 |
| 付款 | 付款 | 支援 |
| PaymentTransactions | 支援 |
| 餘額 | 餘額 | 不支援 |
| 產品 | 產品 | 不支援 |
| ProductDetails | 不支援 |
| 應付憑據 | 應付憑據 | 支援 |

## 限制

PayPal 資料轉移作業有以下限制：

* 透過 PayPal API 存取 PayPal 交易時，可能會延遲數小時。
  + 建議您排定後續資料轉移作業時，間隔時間拉長 (每小時最多一次)，以免遺失資料。
* PayPal 連接器僅支援過去 3 年的[交易資料](#supported_objects)。
* PayPal 連接器僅支援過去 6 個月的[爭議資料](#supported_objects)。
* PayPal API 對每個資料物件都有不同的頁面大小限制。在資料移轉作業中，PayPal 連接器會使用 PayPal 允許的最大網頁大小。
  + 不過，`Payments` 或 `Payment Transactions` 等部分物件會使用較小的網頁大小限制。這可能會導致資料傳輸速度變慢，尤其是在處理大型資料集時。

## 事前準備

下列各節說明建立 PayPal 資料移轉作業前必須執行的步驟。

### PayPal 先決條件

如要啟用 PayPal 資料移轉功能，您必須具備下列條件：

* 你必須擁有 PayPal 開發人員帳戶。詳情請參閱 [PayPal 開發人員計畫](https://developer.paypal.com/developer-program/)。
* 建立 PayPal REST API 應用程式。詳情請參閱「[開始使用 PayPal REST API](https://developer.paypal.com/api/rest/)」。
  + 在「應用程式和憑證」部分，記下應用程式的用戶端 ID 和密鑰。
  + 在「功能」部分，啟用「交易搜尋」和「月結單」API 權限。

### 必要的 BigQuery 角色

如要取得建立移轉作業所需的權限，請要求管理員授予您「[BigQuery 管理員](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.admin) 」(`roles/bigquery.admin`) IAM 角色。如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

這個預先定義的角色具備建立轉移作業所需的權限。如要查看確切的必要權限，請展開「Required permissions」(必要權限) 部分：

#### 所需權限

如要建立移轉作業，必須具備下列權限：

* `bigquery.transfers.update`
  使用者
* `bigquery.datasets.get`
  目標資料集
* `bigquery.datasets.update`
  目標資料集

您或許還可透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)取得這些權限。

### BigQuery 必要條件

* 確認您已完成[啟用 BigQuery 資料移轉服務](https://docs.cloud.google.com/bigquery/docs/enable-transfer-service?hl=zh-tw)的一切必要動作。
* 請[建立 BigQuery 資料集](https://docs.cloud.google.com/bigquery/docs/datasets?hl=zh-tw)來儲存您的資料。
* 如要為 Pub/Sub 設定移轉作業執行通知，請確認您擁有 `pubsub.topics.setIamPolicy` 身分與存取權管理 (IAM) 權限。如果您只想設定電子郵件通知，則不需要擁有 Pub/Sub 權限。詳情請參閱 [BigQuery 資料移轉服務執行通知](https://docs.cloud.google.com/bigquery/docs/transfer-run-notifications?hl=zh-tw)一文。

## 設定 PayPal 資料移轉

如要將 PayPal 資料新增至 BigQuery，請使用下列任一方法設定移轉設定：

### 控制台

1. 前往 Google Cloud 控制台的「資料移轉」頁面。

   [前往「資料轉移」頁面](https://console.cloud.google.com/bigquery/transfers?hl=zh-tw)
2. 按一下 add「建立轉移作業」。
3. 在「Source type」(來源類型) 部分，「Source」(來源) 請選取「PayPal」。
4. 在「Data source details」(資料來源詳細資料) 部分執行下列操作：

   * 在「Client Id」(用戶端 ID) 輸入 PayPal 用戶端 ID。詳情請參閱「[PayPal 先決條件](https://docs.cloud.google.com/bigquery/docs/paypal-transfer?hl=zh-tw#paypal-prerequisites)」。
   * 在「Client Secret」(用戶端密鑰) 部分，輸入 PayPal 用戶端密鑰。詳情請參閱「[PayPal 先決條件](https://docs.cloud.google.com/bigquery/docs/paypal-transfer?hl=zh-tw#paypal-prerequisites)」。
   * 如果您使用沙箱 PayPal 帳戶，請選取「Is Sandbox」。
   * 在「開始日期」中，以 `YYYY-MM-DD` 格式輸入日期。資料轉移作業會從這個日期開始載入 PayPal 資料。
     + 如果將這個欄位留空，系統預設會擷取過去 3 年的資料。
     + 如要瞭解哪些物件支援開始日期篩選器，請參閱「[支援的物件](https://docs.cloud.google.com/bigquery/docs/paypal-transfer?hl=zh-tw#supported_objects)」。
   * 在「PayPal objects to transfer」(要移轉的 PayPal 物件)，輸入要移轉的 PayPal 物件名稱，或是點選「Browse」(瀏覽) 並選取要移轉的物件。
5. 在「Destination settings」(目的地設定) 部分，「Dataset」(資料集) 請選取您為了儲存資料而建立的資料集。
6. 在「Transfer config name」(轉移設定名稱) 部分，「Display name」(顯示名稱) 請輸入資料移轉作業的名稱。
7. 在「Schedule options」(排程選項) 部分執行下列操作：

   * 在「Repeat frequency」(重複頻率) 清單選取選項，指定這項資料移轉作業的執行頻率。如要指定自訂重複頻率，請選取「Custom」(自訂)。如果選取「On-demand」(隨選)，這項移轉作業會在您[手動觸發](https://docs.cloud.google.com/bigquery/docs/working-with-transfers?hl=zh-tw#manually_trigger_a_transfer)後執行。
   * 視情況選取「Start now」(立即開始) 或「Start at set time」(在所設時間開始執行)，並提供開始日期和執行時間。
8. 選用：在「Notification options」(通知選項) 專區，執行下列操作：

   * 如要啟用電子郵件通知，請將「Email notification」(電子郵件通知) 切換按鈕設為開啟。當您啟用此選項時，移轉管理員會在移轉作業失敗時收到電子郵件通知。
   * 如要針對這項移轉作業啟用 [Pub/Sub 移轉作業執行通知](https://docs.cloud.google.com/bigquery/docs/transfer-run-notifications?hl=zh-tw)，請將「Pub/Sub notifications」(Pub/Sub 通知) 切換按鈕設為開啟。您可以選取[主題](https://docs.cloud.google.com/pubsub/docs/overview?hl=zh-tw#types)名稱，也可以點選「Create a topic」(建立主題) 來建立主題。
9. 按一下 [儲存]。

### bq

輸入 [`bq mk` 指令](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_mk)
並加上移轉建立標記
`--transfer_config`：

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

* PROJECT\_ID (選用)：您的 Google Cloud 專案 ID。
  如未提供 `--project_id` 指定特定專案，系統會使用預設專案。
* DATA\_SOURCE：資料來源 - `paypal`。
* DISPLAY\_NAME：資料移轉設定的顯示名稱。移轉作業名稱可以是任意值，日後需要修改移轉作業時，能夠據此識別即可。
* DATASET：移轉設定的目標資料集。
* PARAMETERS：已建立移轉設定的 JSON 格式參數。例如：`--params='{"param":"param_value"}'`。以下是 PayPal 資料移轉的參數：

  + `assets`：要納入這項轉移作業的 PayPal 物件清單。
  + `connector.authentication.clientId`：PayPal 應用程式的用戶端 ID。
  + `connector.authentication.clientSecret`：PayPal 應用程式的用戶端密鑰。
  + `connector.isSandbox`：如果您使用沙箱 PayPal 帳戶，請將值設為 `true`；如果您使用正式版 PayPal 帳戶，請將值設為 `false`。
  + `connector.createdStartDate`：(選用) 輸入日期，格式為 `YYYY-MM-DD`。資料轉移作業會從這個日期開始載入 PayPal 資料。

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

使用 bq 指令列工具建立資料移轉作業時，移轉設定會排定每 8 小時移轉一次資料。

**注意：** 如果您使用 bq 指令列工具設定移轉設定，就無法設定通知。

### API

請使用 [`projects.locations.transferConfigs.create` 方法](https://docs.cloud.google.com/bigquery/docs/reference/datatransfer/rest/v1/projects.locations.transferConfigs/create?hl=zh-tw)，並提供 [`TransferConfig` 資源](https://docs.cloud.google.com/bigquery/docs/reference/datatransfer/rest/v1/projects.locations.transferConfigs?hl=zh-tw#TransferConfig)的執行個體。

儲存移轉設定後，PayPal 連接器會根據排程選項自動觸發移轉作業。每次執行移轉作業時，PayPal 連接器都會將 PayPal 中的所有可用資料移轉至 BigQuery。

如要在正常排程以外手動執行資料移轉作業，可以啟動[回填作業](https://docs.cloud.google.com/bigquery/docs/working-with-transfers?hl=zh-tw#manually_trigger_a_transfer)。

## 資料類型對應

下表列出 PayPal 資料類型與對應 BigQuery 資料類型的對應關係。

| PayPal 資料類型 | BigQuery 資料類型 |
| --- | --- |
| `String` | `STRING` |
| `Decimal` | `BIGNUMERIC` |
| `Boolean` | `BOOL` |
| `Datetime` | `TIMESTAMP` |

## 排解轉移設定問題

如果您無法順利設定資料移轉作業，請參閱「[PayPal 移轉問題](https://docs.cloud.google.com/bigquery/docs/transfer-troubleshooting?hl=zh-tw#paypal-issues)」。

## 定價

這項功能處於[預覽](https://cloud.google.com/products?hl=zh-tw#product-launch-stages)階段時，將 PayPal 資料移轉至 BigQuery 不會產生費用。

## 後續步驟

* 如需 BigQuery 資料移轉服務的總覽，請參閱 [BigQuery 資料移轉服務簡介](https://docs.cloud.google.com/bigquery/docs/dts-introduction?hl=zh-tw)一文。
* 如要瞭解如何管理移轉設定，包括取得資訊、列出設定及查看執行記錄，請參閱「[管理移轉作業](https://docs.cloud.google.com/bigquery/docs/working-with-transfers?hl=zh-tw)」。
* 瞭解如何[透過跨雲端作業載入資料](https://docs.cloud.google.com/bigquery/docs/load-data-using-cross-cloud-transfer?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-12 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-12 (世界標準時間)。"],[],[]]