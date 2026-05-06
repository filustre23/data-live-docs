Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 標籤簡介

您可以在資料集、資料表、預留空間和檢視表中加入標籤，協助您整理 BigQuery 資源。標籤是您可以附加至資源的鍵/值組合。建立 BigQuery 資源時可以選擇是否要加上標籤。

為您的資源加上標籤後，您就可以根據標籤值搜尋資源。例如，您可以使用標籤依照用途、環境和部門等將資料集分組。

## 什麼是標籤？

標籤是可指派給 Google Cloud BigQuery 資源的鍵/值組合。有助於在大規模環境下整理資源，並依所需精細程度管理成本。每項資源均可加上標籤，並根據標籤篩選資源。標籤相關資訊會轉送到帳單系統，方便依照標籤詳細分析帳單費用。使用內建的[帳單報表](https://docs.cloud.google.com/billing/docs/how-to/reports?hl=zh-tw)，可依資源標籤篩選成本並加以分組。 此外，亦可使用標籤查詢[帳單資料匯出檔](https://docs.cloud.google.com/billing/docs/how-to/bq-examples?hl=zh-tw)。

## 標籤需求條件

套用於資源的標籤必須符合下列需求條件：

* 每項資源最多可以有 64 個標籤。
* 每個標籤都必須是鍵/值組合。
* 鍵的長度必須至少為 1 個字元，最多 63 個字元，且不能空白。值可以空白，長度上限為 63 個字元。
* 鍵和值只能使用小寫字母、數字字元、底線和連字號。所有字元都必須使用 UTF-8 編碼，允許國際字元。鍵的開頭必須是小寫字母或國際字元。
* 標籤中的鍵部分不得重複，但可讓多個資源使用相同的鍵。

上述限制適用於各個標籤的鍵和值，以及帶有標籤的個別 Google Cloud 資源；但是在每項專案內，所有資源可套用的標籤總數並無上限。

## 標籤的常見用法

以下是一些常見的標籤用途：

* **團隊或成本中心標籤**：依據團隊或成本中心來新增標籤，藉此區別不同團隊 (例如，`team:research` 和 `team:analytics`) 擁有的 BigQuery 資源。這個類型的標籤可用於成本會計或預算編列作業。
* **元件標籤**：例如 `component:redis`、`component:frontend`、`component:ingest` 和 `component:dashboard`。
* **環境或階段標籤**：例如 `environment:production` 和 `environment:test`。
* **狀態標籤**：例如 `state:active`、`state:readytodelete` 和 `state:archive`。
* **擁有權標籤**：用於識別各項作業的責任團隊，例如：`team:shopping-cart`。

**注意：** 請勿在標籤中加入機密資訊，包括個人識別資訊，例如個人姓名或職稱。標籤不適合用來處理機密資訊。

我們不建議建立大量的不重複標籤，例如幫時間戳記或每個 API 呼叫的個別值建立標籤。這種做法的問題在於，如果標籤值頻繁變更，或標籤鍵使目錄變得雜亂，就難以有效篩選資源並製作報表。

## 標籤和標記

標籤是一種註解，可用於查詢資源，但無法設定政策條件。標記則可作為判斷條件：系統可依據資源是否具備特定標記，允許或拒絕相應的政策，進而實現精細的政策控管。詳情請參閱「[標記總覽](https://docs.cloud.google.com/resource-manager/docs/tags/tags-overview?hl=zh-tw)」。

## 限制

* 使用 BigQuery Storage Write API 擷取資料時，無法套用 BigQuery 標籤。

## 後續步驟

* 瞭解如何為 BigQuery 資源[加上標籤](https://docs.cloud.google.com/bigquery/docs/adding-labels?hl=zh-tw)。
* 瞭解如何在 BigQuery 資源中[查看標籤](https://docs.cloud.google.com/bigquery/docs/viewing-labels?hl=zh-tw)。
* 瞭解如何在 BigQuery 資源中[更新標籤](https://docs.cloud.google.com/bigquery/docs/updating-labels?hl=zh-tw)。
* 瞭解如何[使用標籤篩選資源](https://docs.cloud.google.com/bigquery/docs/filtering-labels?hl=zh-tw)。
* 瞭解如何在 BigQuery 資源中[刪除標籤](https://docs.cloud.google.com/bigquery/docs/deleting-labels?hl=zh-tw)。
* 閱讀 Resource Manager 說明文件中的[使用標籤](https://docs.cloud.google.com/resource-manager/docs/using-labels?hl=zh-tw)相關說明。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-06 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-06 (世界標準時間)。"],[],[]]