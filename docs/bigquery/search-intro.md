Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# BigQuery 搜尋功能簡介

**注意：** 如果預留項目是以特定 BigQuery 版本建立，可能無法使用這項功能。如要進一步瞭解各版本啟用的功能，請參閱「[BigQuery 版本簡介](https://docs.cloud.google.com/bigquery/docs/editions-intro?hl=zh-tw)」。

BigQuery 搜尋索引可讓您有效率地找出藏在非結構化文字和半結構化 JSON 資料中的不重複資料元素，不必事先瞭解資料表結構定義。搜尋索引結合了資料欄儲存庫和文字搜尋功能，可讓您有效率地執行資料列查詢，以便進行記錄分析、安全性稽核和依法呈報等工作。

BigQuery 會儲存及管理索引，因此當資料在 BigQuery 中可用時，您可以使用 [`SEARCH` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/search_functions?hl=zh-tw#search)或[其他支援的運算子和函式](https://docs.cloud.google.com/bigquery/docs/search?hl=zh-tw#operator_and_function_optimization)立即擷取資料。如要最佳化搜尋，請參閱[最佳做法](https://docs.cloud.google.com/bigquery/docs/search?hl=zh-tw#best_practices)。

**重要事項：**加入[搜尋討論群組](https://groups.google.com/g/bq-search?hl=zh-tw)，即可張貼問題和留言，並追蹤最新消息。

## 用途

BigQuery 搜尋索引可協助您執行下列工作：

* 搜尋儲存在 BigQuery 資料表中的系統、網路或應用程式記錄。
* 找出要刪除的資料元素，以遵守法規程序。
* 協助開發人員排解問題。
* 執行安全性稽核。
* 建立需要高度選擇性搜尋篩選器的資訊主頁。
* 搜尋預先處理的資料，找出完全相符的結果。

詳情請參閱「[建立搜尋索引](https://docs.cloud.google.com/bigquery/docs/search-index?hl=zh-tw)」和「[使用索引搜尋](https://docs.cloud.google.com/bigquery/docs/search?hl=zh-tw)」。

## 定價

如果貴組織中已建立索引的資料表總大小低於所在區域的[限制](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#index_limits)，則建立及重新整理搜尋索引所需的處理作業不會產生費用。如要支援超過此限制的索引，您需要[提供自己的預留項目](https://docs.cloud.google.com/bigquery/docs/search-index?hl=zh-tw#use_your_own_reservation)，以處理索引管理工作。搜尋索引啟用時會產生儲存費用。您可以在[`INFORMATION_SCHEMA.SEARCH_INDEXES`檢視畫面](https://docs.cloud.google.com/bigquery/docs/information-schema-indexes?hl=zh-tw)中查看索引儲存空間大小。

## 角色和權限

如要建立搜尋索引，您必須具備[`bigquery.tables.createIndex` IAM 權限](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bq-permissions)，才能在資料表上建立索引。如要捨棄搜尋索引，您必須具備 `bigquery.tables.deleteIndex` 權限。下列各項預先定義的 IAM 角色，都包含使用搜尋索引所需的權限：

* BigQuery 資料擁有者 (`roles/bigquery.dataOwner`)
* BigQuery 資料編輯者 (`roles/bigquery.dataEditor`)
* BigQuery 管理員 (`roles/bigquery.admin`)

## 限制

* 您無法直接在檢視表或 materialized view 建立搜尋索引，但在已建立索引的資料表檢視表上呼叫 [`SEARCH` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/search_functions?hl=zh-tw#search)，即可使用基礎搜尋索引。
* 您無法在外部資料表建立搜尋索引。
* 如果在資料表上建立搜尋索引後重新命名資料表，索引就會失效。
* `SEARCH` 函式專為點查詢設計。無法使用模糊搜尋、錯字修正、萬用字元和其他類型的文件搜尋。
* 如果搜尋索引尚未達到 100% 涵蓋率，您仍須支付 [`INFORMATION_SCHEMA.SEARCH_INDEXES` 檢視畫面](https://docs.cloud.google.com/bigquery/docs/information-schema-indexes?hl=zh-tw)中回報的所有索引儲存空間費用。
* 使用 `SEARCH` 函式或由搜尋索引最佳化的查詢，不會由 [BigQuery BI Engine](https://docs.cloud.google.com/bigquery/docs/bi-engine-intro?hl=zh-tw) 加速。
* 當 DML 陳述式修改索引資料表時，系統不會使用搜尋索引，但如果可透過搜尋索引最佳化的述詞是 DML 陳述式中子查詢的一部分，則可使用搜尋索引。

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
* [時間旅行查詢](https://docs.cloud.google.com/bigquery/docs/time-travel?hl=zh-tw)不會使用搜尋索引。

## 後續步驟

* 進一步瞭解如何[建立搜尋索引](https://docs.cloud.google.com/bigquery/docs/search-index?hl=zh-tw)。
* 進一步瞭解如何[使用搜尋索引在資料表中搜尋](https://docs.cloud.google.com/bigquery/docs/search?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-11-11 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-11-11 (世界標準時間)。"],[],[]]