Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# BigQuery Data Catalog 總覽



**注意：**Data Catalog 已[淘汰](https://docs.cloud.google.com/data-catalog/docs/deprecations?hl=zh-tw)，
建議改用 [Knowledge Catalog](https://docs.cloud.google.com/dataplex/docs/catalog-overview?hl=zh-tw)。
Knowledge Catalog 也與 BigQuery 整合，提供類似功能。如要瞭解如何使用切面豐富資料，請參閱「[管理切面及豐富中繼資料](https://docs.cloud.google.com/dataplex/docs/enrich-entries-metadata?hl=zh-tw)」一文。切面相當於 Data Catalog 標記。

本文將概要說明 Data Catalog 與 BigQuery 的關係。

Data Catalog 是可擴充的全代管中繼資料管理服務。

## Data Catalog 用途

BigQuery 會使用 Data Catalog 執行下列用途：

* 以視覺化方式呈現資料歷程。
* 搜尋您有權存取的資源。
* 以中繼資料標記資源。

如要進一步瞭解 Data Catalog，請參閱「[什麼是 Data Catalog](https://docs.cloud.google.com/data-catalog/docs/concepts/overview?hl=zh-tw)」。

## Data Catalog 的運作方式

Data Catalog 可分類 BigQuery 資料來源的中繼資料。中繼資料編目完成後，您可以使用標記，將自己的中繼資料新增至這些資料來源。對於指定的 BigQuery 專案，Data Catalog 會自動將資料集、資料表、檢視和模型相關的 BigQuery 中繼資料分類。Data Catalog 會處理兩種中繼資料：*技術中繼資料*和*業務中繼資料*。如要進一步瞭解中繼資料，請參閱「[資料目錄中繼資料](https://docs.cloud.google.com/data-catalog/docs/concepts/metadata?hl=zh-tw)」。

## 搜尋與探索

Data Catalog 提供強大的述詞式搜尋體驗，可搜尋與 BigQuery 資料來源相關聯的 Data Catalog 項目，並找出技術和業務中繼資料。您必須具備資源中繼資料的讀取權限，才能對中繼資料套用搜尋與發現功能。Data Catalog 不會為資源內的資料建立索引。Data Catalog 只會為描述 BigQuery 資料來源的
中繼資料建立索引。

Data Catalog 會控管部分中繼資料，例如使用者產生的標記。對於所有來自 BigQuery 的中繼資料，Data Catalog 都是唯讀服務，可反映 BigQuery 提供的中繼資料和權限。您可以在 BigQuery 中編輯資料項目的中繼資料，包括新增、更新或刪除。

如要進一步瞭解 Data Catalog 搜尋功能，請參閱「[搜尋 BigQuery 資源](https://docs.cloud.google.com/bigquery/docs/data-catalog?hl=zh-tw#search-for-bq-resources)」。

## 存取 Data Catalog

您可以使用下列介面存取 Data Catalog 功能：

* [Google Cloud 控制台](https://console.cloud.google.com/bigquery?hl=zh-tw)中的「BigQuery」**BigQuery**頁面
* [Google Cloud 控制台](https://console.cloud.google.com/dataplex?hl=zh-tw)中的「Dataplex」頁面
* [Google Cloud CLI](https://docs.cloud.google.com/sdk/gcloud/reference/data-catalog?hl=zh-tw)
* [資料目錄 API](https://docs.cloud.google.com/data-catalog/docs/reference?hl=zh-tw)
* [Cloud 用戶端程式庫](https://docs.cloud.google.com/data-catalog/docs/reference/libraries?hl=zh-tw)

## 後續步驟

* 如要開始使用 Data Catalog 和 BigQuery，請參閱[使用 Data Catalog](https://docs.cloud.google.com/bigquery/docs/data-catalog?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-02 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-02 (世界標準時間)。"],[],[]]