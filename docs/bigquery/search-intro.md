Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# BigQuery 搜尋功能簡介

**注意：** 使用以特定 BigQuery 版本建立的預留項目時，可能無法使用這項功能。如要進一步瞭解各版本啟用的功能，請參閱「[BigQuery 版本簡介](https://docs.cloud.google.com/bigquery/docs/editions-intro?hl=zh-tw)」。

有了 BigQuery 搜尋索引，您可以使用 GoogleSQL 找出藏在非結構化文字和半結構化 JSON 資料中的不重複資料元素，完全不需事先瞭解資料表結構。

BigQuery 透過搜尋索引在單一平台中提供強大的資料欄儲存空間和文字搜尋功能，讓您在需要尋找個別資料列時，能夠有效率地進行資料列查詢。常見用途是記錄檔分析。舉例來說，您可能想找出與使用者相關的資料列，以產生《一般資料保護規則》(GDPR) 報表，或在文字酬載中尋找特定錯誤代碼。

BigQuery 會儲存及管理索引，因此當資料在 BigQuery 中可用時，您可以使用 [`SEARCH` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/search_functions?hl=zh-tw#search)或[其他運算子和函式](https://docs.cloud.google.com/bigquery/docs/search?hl=zh-tw#operator_and_function_optimization) (例如等號 (`=`)、`IN` 或 `LIKE` 運算子，以及特定字串和 JSON 函式)，立即擷取資料。如要最佳化搜尋結果，請參閱[最佳做法](https://docs.cloud.google.com/bigquery/docs/search?hl=zh-tw#best_practices)。

**重要事項：** 加入
[搜尋討論群組](https://groups.google.com/g/bq-search?hl=zh-tw)
，即可發布問題和留言，並掌握最新動態。

## 用途

BigQuery 搜尋索引可協助您執行下列工作：

* 搜尋儲存在 BigQuery 資料表中的系統、網路或應用程式記錄。
* 找出要刪除的資料元素，以符合法規程序。
* 支援開發人員排解問題。
* 執行安全稽核。
* 建立需要高度選擇性搜尋篩選器的資訊主頁。
* 搜尋預先處理的資料，找出完全相符的結果。

詳情請參閱「[建立搜尋索引](https://docs.cloud.google.com/bigquery/docs/search-index?hl=zh-tw)」和「[使用索引進行搜尋](https://docs.cloud.google.com/bigquery/docs/search?hl=zh-tw)」。

## 定價

如果機構中建立索引的資料表總大小低於所在區域的[限制](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#index_limits)，則建立及重新整理搜尋索引所需的處理作業不會產生費用。如要支援超出此限制的索引作業，您必須[提供自己的預訂](https://docs.cloud.google.com/bigquery/docs/search-index?hl=zh-tw#use_your_own_reservation)，以處理索引管理工作。搜尋索引處於有效狀態時會產生儲存空間費用。
您可以在 [`INFORMATION_SCHEMA.SEARCH_INDEXES` 檢視畫面](https://docs.cloud.google.com/bigquery/docs/information-schema-indexes?hl=zh-tw)中查看索引儲存空間大小。

## 角色和權限

如要建立搜尋索引，您必須在要建立索引的資料表上，具備 [`bigquery.tables.createIndex` IAM 權限](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bq-permissions)。如要捨棄搜尋索引，您必須具備 `bigquery.tables.deleteIndex` 權限。下列每個預先定義的 IAM 角色都包含使用搜尋索引所需的權限：

* BigQuery 資料擁有者 (`roles/bigquery.dataOwner`)
* BigQuery 資料編輯者 (`roles/bigquery.dataEditor`)
* BigQuery 管理員 (`roles/bigquery.admin`)

## 限制

* 您無法直接在檢視表或具體化檢視表上建立搜尋索引，但對索引資料表的檢視表呼叫 [`SEARCH` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/search_functions?hl=zh-tw#search)，即可使用基礎搜尋索引。
* 您無法在外部資料表上建立搜尋索引。
* 如果為資料表建立搜尋索引後重新命名，索引就會失效。
* `SEARCH` 函式適用於點查。模糊搜尋、錯別字修正、萬用字元和其他類型的文件搜尋功能不適用。
* 如果搜尋索引的涵蓋範圍尚未達到 100%，系統仍會針對[`INFORMATION_SCHEMA.SEARCH_INDEXES`檢視畫面](https://docs.cloud.google.com/bigquery/docs/information-schema-indexes?hl=zh-tw)中回報的所有索引儲存空間收費。
* 使用 `SEARCH` 函式或透過搜尋索引最佳化的查詢，不會由 [BigQuery BI Engine](https://docs.cloud.google.com/bigquery/docs/bi-engine-intro?hl=zh-tw) 加速。
* 如果使用 DML 陳述式修改已建立索引的資料表，系統不會使用搜尋索引，但如果可透過搜尋索引最佳化的述詞是 DML 陳述式中子查詢的一部分，系統就會使用搜尋索引。

  + 下列查詢不會使用搜尋索引：

  ```
  DELETE FROM my_dataset.indexed_table
  WHERE SEARCH(user_id, '123');
  ```

  + 搜尋索引可用於下列查詢：

  ```
  DELETE FROM my_dataset.other_table
  WHERE
    user_id IN (
      SELECT user_id
      FROM my_dataset.indexed_table
      WHERE SEARCH(user_id, '123')
    );
  ```
* 查詢參照[具體化檢視表](https://docs.cloud.google.com/bigquery/docs/materialized-views-intro?hl=zh-tw)時，不會使用搜尋索引。
* [多重陳述式交易查詢](https://docs.cloud.google.com/bigquery/docs/transactions?hl=zh-tw)不會使用搜尋索引。
* [時空旅行查詢](https://docs.cloud.google.com/bigquery/docs/time-travel?hl=zh-tw)不會使用搜尋索引。

## 後續步驟

* 進一步瞭解如何[建立搜尋索引](https://docs.cloud.google.com/bigquery/docs/search-index?hl=zh-tw)。
* 進一步瞭解如何[使用搜尋索引在資料表中搜尋](https://docs.cloud.google.com/bigquery/docs/search?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-06 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-06 (世界標準時間)。"],[],[]]