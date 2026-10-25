Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 邏輯檢視表簡介

「邏輯檢視表」是由 SQL 查詢定義的虛擬資料表，也是 BigQuery 中的預設檢視表類型。邏輯檢視表可讓您重複使用複雜的查詢，並簡化計算和彙整邏輯。您也可以透過[授權檢視表](https://docs.cloud.google.com/bigquery/docs/authorized-views?hl=zh-tw)，授予使用者部分資料的存取權，而不必授予基礎資料表的存取權。

每次查詢邏輯檢視表時，系統都會執行定義邏輯檢視表的查詢，因此結果只會包含查詢指定的資料表和欄位中的目前資料。本文說明邏輯檢視表的常見用途、限制、配額、定價和安全性。

## 用途

檢視表的常見用途包括：

* 為複雜查詢或有限資料集提供可重複使用的名稱，然後[授權](https://docs.cloud.google.com/bigquery/docs/authorized-views?hl=zh-tw)其他使用者存取。建立檢視表後，使用者可以像查詢資料表一樣[查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw)檢視表。
* 在通用物件中擷取並儲存計算和彙整邏輯，簡化查詢作業。
* 提供部分資料和計算邏輯的存取權，但不提供基礎資料表的存取權。
* 針對[多種用途](https://docs.cloud.google.com/bigquery/docs/materialized-views-intro?hl=zh-tw#use_cases)，最佳化運算成本高且資料集結果小的查詢。

您也可以在其他情況下使用檢視表：

* 做為 [數據分析](https://docs.cloud.google.com/looker/docs?hl=zh-tw) 等視覺化工具的資料來源。
* 將資料提供給 [BigQuery sharing (舊稱 Analytics Hub)](https://docs.cloud.google.com/bigquery/docs/analytics-hub-introduction?hl=zh-tw) 的訂閱者。

如要比較邏輯、materialized view 和授權 view，請參閱「[邏輯和 materialized view 總覽](https://docs.cloud.google.com/bigquery/docs/logical-materialized-view-overview?hl=zh-tw)」。

## 邏輯檢視表限制

BigQuery 資料檢視有下列幾項限制：

* 檢視表為唯讀狀態。例如，您無法執行插入、更新或刪除資料的查詢。
* 如果檢視表參照遠端[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)的資料表，您必須先啟用[全域查詢](https://docs.cloud.google.com/bigquery/docs/global-queries?hl=zh-tw)，才能建立檢視表。
* 檢視表內的參照必須符合資料集。預設資料集不會影響檢視表主體。
* 您無法使用 `TableDataList` JSON API 方法從檢視表擷取資料。詳情請參閱 [Tabledata：list](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tabledata/list?hl=zh-tw) 的相關說明。
* 使用檢視表時，您無法混合使用 GoogleSQL 和舊版 SQL 查詢。GoogleSQL 查詢無法參照使用舊版 SQL 語法定義的檢視表。
* 您無法在檢視表中參照[查詢參數](https://docs.cloud.google.com/bigquery/docs/parameterized-queries?hl=zh-tw)。
* 建立檢視表時，系統會將基礎資料表的結構定義和檢視表一併儲存。如果在建立檢視表後新增、刪除或修改資料欄，檢視表不會自動更新，且回報的結構定義會維持不準確狀態，直到檢視表 SQL 定義變更或重新建立檢視表為止。雖然回報的結構定義可能不準確，但所有提交的查詢都會產生準確的結果。
* 您無法自動將舊版 SQL 檢視表更新為 GoogleSQL 語法。如要修改用於定義檢視表的查詢，可以使用下列指令：
  + Google Cloud 控制台中的「Edit query」(編輯查詢) 選項
  + bq 指令列工具中的 [`bq update --view`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_update) 指令
  + [BigQuery 用戶端程式庫](https://docs.cloud.google.com/bigquery/docs/reference/libraries?hl=zh-tw)
  + [update](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables/update?hl=zh-tw) 或 [patch](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables/patch?hl=zh-tw) API 方法。
* 在定義檢視表的 SQL 查詢中，不得包含 temporary user-defined function 或臨時資料表。
* 您無法在[萬用字元資料表](https://docs.cloud.google.com/bigquery/docs/querying-wildcard-tables?hl=zh-tw)查詢中參照檢視表。
* 邏輯檢視表無法繼承或明確定義[參數化資料類型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#parameterized_data_types) (例如 `STRING(n)`)，因為參數化資料類型僅適用於基礎資料表資料欄和指令碼變數。

## 邏輯檢視表配額

如要瞭解檢視表的配額和限制，請參閱「[檢視表限制](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#view_limits)」。用於定義檢視表的 SQL 查詢也受[查詢工作](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#query_jobs)配額限制。

## 邏輯檢視表定價

BigQuery 預設使用邏輯檢視表，而非[具體化檢視表](https://docs.cloud.google.com/bigquery/docs/materialized-views-intro?hl=zh-tw)。根據預設，檢視表不會具體化，因此每次查詢檢視表時，都會執行定義檢視表的查詢。查詢費用是根據頂層查詢直接或間接參照的所有資料表欄位中的資料總量計算。

* 如要瞭解一般查詢定價，請參閱「[隨選運算定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#on_demand_pricing)」。
* 如要瞭解 materialized view 的相關定價，請參閱「[materialized view 定價](https://docs.cloud.google.com/bigquery/docs/materialized-views-intro?hl=zh-tw#materialized_views_pricing)」。

## 邏輯檢視表安全性

如要控管 BigQuery 檢視表的存取權，請參閱「[授權檢視表](https://docs.cloud.google.com/bigquery/docs/authorized-views?hl=zh-tw)」。

## 後續步驟

* 如要瞭解如何建立檢視表，請參閱[建立檢視表](https://docs.cloud.google.com/bigquery/docs/views?hl=zh-tw)一文。
* 如要瞭解如何建立授權檢視表，請參閱[建立授權檢視表](https://docs.cloud.google.com/bigquery/docs/authorized-views?hl=zh-tw)一文。
* 如要瞭解如何取得檢視表中繼資料，請參閱[取得檢視表相關資訊](https://docs.cloud.google.com/bigquery/docs/view-metadata?hl=zh-tw)一文。
* 如要進一步瞭解如何管理檢視表，請參閱「[管理檢視表](https://docs.cloud.google.com/bigquery/docs/managing-views?hl=zh-tw)」。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-10-24 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-10-24 (世界標準時間)。"],[],[]]