Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# BI Engine 簡介

您可以使用 BigQuery BI Engine 加速 BigQuery 中的 SQL 查詢和互動式商業智慧 (BI) 資訊主頁，不必手動調整或資料分層。BI Engine 會快取最常查詢的資料，協助您實現低延遲查詢效能，同時繼續使用現有的 BI 工具和自訂應用程式，無須進行任何修改。

## BI Engine 簡介

BigQuery BI Engine 是一項快速的記憶體內分析服務，可智慧快取最常用的資料，加快 BigQuery 中許多 SQL 查詢的速度。您可以[分群資料表](https://docs.cloud.google.com/bigquery/docs/clustered-tables?hl=zh-tw)和[分區資料表](https://docs.cloud.google.com/bigquery/docs/partitioned-tables?hl=zh-tw)，進一步最佳化大型資料表的 BI Engine 效能。

舉例來說，如果資訊主頁只顯示上一季的資料，您可以依時間將資料表分區，這樣就只會將最新的分區載入記憶體。接著，您可以使用[具體化檢視表](https://docs.cloud.google.com/bigquery/docs/materialized-views-intro?hl=zh-tw)彙整及簡維資料，然後將產生的檢視表和基礎資料表標示為偏好資料表，確保 BI Engine 加速功能只套用至所需資料。

BI Engine 具備下列優點：

* **BigQuery API 相容性**：BI Engine 直接與 BigQuery API 整合。任何商業智慧解決方案或自訂應用程式，只要透過 [REST API](https://docs.cloud.google.com/bigquery/docs/reference/rest?hl=zh-tw) 或 [JDBC 和 ODBC 驅動程式](https://docs.cloud.google.com/bigquery/docs/reference/odbc-jdbc-drivers?hl=zh-tw)等標準機制與 BigQuery API 搭配使用，就能直接使用 BI Engine，無須修改。
* **向量化執行階段**：在執行引擎中使用向量化處理，一次處理多批資料，更有效率地運用現代 CPU 架構。BI Engine 也會使用進階資料編碼 (特別是字典遊程編碼)，進一步壓縮儲存在記憶體內層的資料。
* **完美整合**：BI Engine 可與 BigQuery 功能和中繼資料搭配使用，包括授權檢視表、資料欄層級安全性和資料遮蓋。
* **預留項目分配**：BI Engine 預留項目會分別管理各專案和區域的記憶體配置。BI Engine 只會快取資料欄和分區中查詢的部分。您可以透過[偏好資料表](#preferred_tables)，指定哪些資料表要使用 BI Engine 加速功能。

在多數組織中，BI Engine 是由帳單管理員啟用，他們會使用適當的[版本](https://docs.cloud.google.com/bigquery/docs/editions-intro?hl=zh-tw#administration_features)預留容量，以便加速 BI Engine。詳情請參閱「[預留 BI Engine 運算資源](https://docs.cloud.google.com/bigquery/docs/bi-engine-reserve-capacity?hl=zh-tw)」。

## BI Engine 架構

BI Engine 透過 BigQuery API 與 Looker、數據分析、Tableau 和 Power BI 等 BI 工具以及自訂應用程式整合，可加快資料探索和分析速度：

## BI Engine 用途

BI Engine 可大幅加快許多 SQL 查詢的速度，包括用於 BI 資訊主頁的查詢。如要發揮加速功能的最大效益，請找出查詢作業不可或缺的資料表，並將其指定為「偏好資料表」。如要使用 BI Engine，請在區域中建立預留項目並指定大小。您可以讓 BigQuery 根據專案的使用模式，決定要快取哪些資料表，也可以指定資料表，避免其他流量干擾加速作業。

BI Engine 適用於下列用途：

* **使用 BI 工具分析資料**：無論是在 BigQuery 控制台、數據分析或 Tableau 等 BI 工具、用戶端程式庫、API，還是 ODBC 或 JDBC 連接器中執行，BI Engine 都能加速 BigQuery 查詢。這項功能可大幅提升透過內建連結 (API) 或連接器連結至 BigQuery 的資訊主頁效能。
* **您有經常查詢的資料表**：BI Engine 可讓您指定要加速的偏好資料表。如果有一部分資料表查詢頻率較高，或用於高能見度的資訊主頁，這項功能就非常實用。

在下列情況下，BI Engine 可能不符合您的需求：

* **在查詢中使用萬用字元**：BI Engine 不支援參照 Wildcard 資料表的查詢，因此無法加速。
* **您需要 BI Engine 不支援的 BigQuery 功能**：雖然 BI Engine 支援大多數 SQL 函式和運算子，但[不支援的功能](#unsupported-features)包括外部資料表、資料列層級安全性，以及非 SQL user-defined function。

## BI Engine 注意事項

決定如何設定 BI Engine 時，請考量下列事項：

### 確保特定查詢加速

如要確保一組查詢能加速執行，請建立獨立專案，並指派專屬 BI Engine 預留項目。首先，請[預估查詢所需的運算能力](https://docs.cloud.google.com/bigquery/docs/bi-engine-reserve-capacity?hl=zh-tw#estimate_and_measure_capacity)，然後將這些資料表指定為 BI Engine 的[偏好資料表](#preferred_tables)。

### 盡量減少彙整

BI Engine 最適合用於預先彙整或預先匯總的資料，以及彙整數量較少的查詢。如果彙整的一端很大，而其他端小得多，這種行為就特別明顯，例如查詢大型事實資料表，並與較小的維度資料表彙整。您可以將 BI Engine 與[實體化檢視表](https://docs.cloud.google.com/bigquery/docs/materialized-views-intro?hl=zh-tw)結合，透過彙整作業產生單一大型平面資料表。這種做法可避免為每項查詢執行相同的彙整作業。建議使用過時的 materialized view，以獲得最佳查詢效能。

### 瞭解 BI Engine 的影響

如要瞭解 BI Engine 的使用情形，請參閱「[透過 Cloud Monitoring 監控 BI Engine](https://docs.cloud.google.com/bigquery/docs/bi-engine-monitor?hl=zh-tw)」，或查詢 [`INFORMATION_SCHEMA.BI_CAPACITIES`](https://docs.cloud.google.com/bigquery/docs/information-schema-bi-capacities?hl=zh-tw) 和 [`INFORMATION_SCHEMA.BI_CAPACITY_CHANGES`](https://docs.cloud.google.com/bigquery/docs/information-schema-bi-capacity-changes?hl=zh-tw) 檢視表。請務必停用 BigQuery 中的「Use cached results」(使用快取結果) 選項，才能取得最準確的比較結果。詳情請參閱「[使用快取查詢結果](https://docs.cloud.google.com/bigquery/docs/cached-results?hl=zh-tw)」。

### 偏好資料表

您可以透過 BI Engine 偏好資料表，將 BI Engine 加速功能限制在特定資料表。所有其他資料表的查詢則使用一般 BigQuery 運算單元。舉例來說，您可以透過偏好資料表，只加速對業務重要的資料表和資訊主頁。

如果專案中的記憶體不足，無法容納所有偏好的資料表，BI Engine 會卸載最近未存取的分區和資料欄。這個程序會釋出記憶體，供需要加速的新查詢使用。

#### 偏好資料表限制

BI Engine 偏好資料表有下列限制：

* 您無法將邏輯檢視表新增至偏好資料表預訂項目清單。BI Engine 偏好資料表僅支援資料表。
* 只有在 materialized view 和基礎資料表都位於偏好資料表清單中時，系統才會加速查詢 materialized view。
* 不支援指定要加速的分區或資料欄。
* BI Engine 不支援`JSON`已指定類型和格式的欄，也不會加速處理。
* 只有在所有資料表都是偏好資料表時，存取多個資料表的查詢才會加速。舉例來說，查詢中含有 `JOIN` 的所有資料表都必須位於偏好資料表清單中，才能加速。只要有任何資料表不在偏好清單中，查詢就無法使用 BI Engine。
* Google Cloud 控制台不支援公開資料集。如要將公開資料表新增為偏好資料表，請使用 API 或 DDL。

## 查詢最佳化和加速

BigQuery (以及 BI Engine) 會將查詢計畫分成多個子查詢。子查詢包含掃描、篩選、運算或匯總資料等作業，並做為執行單位。

雖然所有支援的 BigQuery SQL 查詢都能透過 BI Engine 正確執行，但 BI Engine 會選擇性地最佳化特定階段：

* **葉層級子查詢**：BI Engine 最適合用於葉層級子查詢，可從儲存空間掃描資料，並執行篩選、運算、匯總、排序 (`ORDER BY`) 和支援的 join 等作業。
* **備用執行**：如果查詢階段或子查詢無法由 BI Engine 加速，系統會自動改用標準 BigQuery 執行運算單元，不會導致查詢失敗。

由於這種選擇性最佳化，較簡單的商業智慧或資訊主頁類型查詢，最能從 BI Engine 獲益，因為其大部分執行時間都花在處理分葉層級子查詢中的原始資料。

## 限制

如要使用 BI Engine，貴組織必須預留支援版本的 BI Engine 容量。詳情請參閱「[瞭解 BigQuery 版本](https://docs.cloud.google.com/bigquery/docs/editions-intro?hl=zh-tw#administration_features)」一文。

此外，BI Engine 也有一些限制，詳情請參閱下列各節。

### 彙整次數

BI Engine 可加快特定類型的 join 查詢。加速作業會在具有 `INNER` 和 `LEFT OUTER` 彙整的葉層級子查詢上進行，其中大型事實資料表會與最多四個較小的維度資料表彙整。小型維度資料表有下列限制：

* 少於 500 萬列
* 大小限制：
  + 未分區資料表：5 GiB 以下
  + 分區資料表：參照的分區不超過 1 GiB

### 窗型函式

[視窗函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/window-function-calls?hl=zh-tw) (又稱*分析函式*) 經 BI Engine 加速後，會受到下列限制：

* 不含視窗函式的輸入階段會由 BI Engine 加速。在這種情況下，`INFORMATION_SCHEMA.JOBS` 檢視畫面會將 `bi_engine_statistics.acceleration_mode` 回報為 `FULL_INPUT`。
* 如果含有 window 函式的查詢輸入階段符合 [BI Engine window 函式限制](#window_function_limitations)，BI Engine 就會加速處理。在這種情況下，輸入階段或完整查詢會在 BI Engine 中執行，而 `INFORMATION_SCHEMA.JOBS` 檢視畫面會將 `bi_engine_statistics.acceleration_mode` 回報為 `FULL_INPUT` 或 `FULL_QUERY`。

如要進一步瞭解 `BiEngineStatistics` 欄位，請參閱[工作參考資料](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#bienginestatistics)。

#### BI Engine 視窗函式限制

只有在符合下列所有條件時，含有視窗函式的查詢才會在 BI Engine 中執行：

* 查詢只會掃描一個資料表。
  + 資料表未分區。
  + 資料表少於 500 萬列。
* 查詢沒有 `JOIN` 運算子。
* 掃描的資料表大小乘以視窗函式運算子數量，不超過 300 MiB。

兩個視窗函式如果具有相同的 `OVER` 子句和相同的直接輸入內容，則可共用同一個視窗函式運算子。例如：

* `SELECT ROW_NUMBER() OVER (ORDER BY x), SUM(x) OVER (ORDER BY x) FROM my_table` 只有一個視窗函式運算子。
* `SELECT ROW_NUMBER() OVER (ORDER BY x), SUM(x) OVER (PARTITION BY y ORDER BY x) FROM my_table` 有兩個視窗函式運算子，因為這兩個函式有不同的 `OVER` 子句。
* `SELECT ROW_NUMBER() OVER (ORDER BY x) FROM (SELECT SUM(x) OVER (ORDER BY x) AS x FROM my_table)` 有兩個視窗函式運算子，因為這兩個函式的直接輸入內容不同，但 `OVER` 子句看起來相同。

#### 支援的視窗函式

系統支援下列視窗函式：

* `ANY_VALUE`
* `AVG`
* `BIT_AND`
* `BIT_OR`
* `BIT_XOR`
* `CORR`
* `COUNT`
* `COUNTIF`
* `COVAR_POP`
* `COVAR_SAMP`
* `CUME_DIST`
* `DENSE_RANK`
* `FIRST_VALUE`
* `LAG`
* `LAST_VALUE`
* `LEAD`
* `LOGICAL_AND`
* `LOGICAL_OR`
* `MAX`
* `MIN`
* `NTH_VALUE`
* `NTILE`
* `PERCENT_RANK`
* `PERCENTILE_CONT`
* `PERCENTILE_DISC`
* `RANK`
* `ROW_NUMBER`
* `ST_CLUSTERDBSCAN`
* `STDDEV_POP`
* `STDDEV_SAMP`
* `STDDEV`
* `STRING_AGG`
* `SUM`
* `VAR_POP`
* `VAR_SAMP`
* `VARIANCE`

如果系統不支援視窗函式，您可能會看到下列錯誤訊息：

`Analytic function is incompatible with other operators or its inputs are too large`

### 不支援的 BI Engine 限制

下列功能不支援 BI Engine 加速：

* JavaScript UDF 和遠端函式。
* 外部資料表，包括 BigLake 資料表。
* 正在查詢`JSON`資料 (錯誤訊息：`JSON native type is not supported.`)。
* 正在查詢`RANGE`資料 (錯誤訊息：`RANGE native type is not supported.`)。
* 將結果寫入永久 BigQuery 資料表。
* 資料表包含使用 [BigQuery 變更資料擷取擷取功能](https://docs.cloud.google.com/bigquery/docs/change-data-capture?hl=zh-tw)的 upsert。
* [交易](https://docs.cloud.google.com/bigquery/docs/transactions?hl=zh-tw)。
* 傳回超過 1 GiB 資料的查詢 (對於延遲敏感的應用程式，建議回應大小不超過 1 MiB)。
* 資料列層級安全性。
* 使用搜尋和向量搜尋函式 (例如 [`SEARCH` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/search_functions?hl=zh-tw#search)或 [`VECTOR_SEARCH` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/search_functions?hl=zh-tw#vector_search))，或由[搜尋索引](https://docs.cloud.google.com/bigquery/docs/search-intro?hl=zh-tw)或[向量索引](https://docs.cloud.google.com/bigquery/docs/vector-search-intro?hl=zh-tw)最佳化的查詢。
* 使用 `RECURSIVE` 的遞迴查詢。
* BigQuery ML 查詢。

#### 不支援功能的解決方法

如果查詢使用不支援的 SQL 功能，可以採用下列解決方法：

1. 在 BigQuery 中編寫查詢。
2. 將查詢結果儲存至資料表。
3. [安排查詢時間](https://docs.cloud.google.com/bigquery/docs/scheduling-queries?hl=zh-tw)，定期更新資料表。建議每小時或每天重新整理一次。如果每分鐘重新整理一次，快取可能會太常失效。
4. 在對效能要求極高的查詢中，請參照這個資料表。

## 配額與限制

如要瞭解 BI Engine 適用的配額和限制，請參閱「[BigQuery 配額和限制](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#biengine-limits)」。

## 定價

您需要為 BI Engine 容量建立的預留項目支付費用。如要瞭解 BI Engine 定價，請參閱「[BigQuery 定價](https://docs.cloud.google.com/bigquery/pricing?hl=zh-tw#bi_engine_pricing)」。

## 後續步驟

* 如要瞭解如何建立預留項目，請參閱「[預留 BI Engine 容量](https://docs.cloud.google.com/bigquery/docs/bi-engine-reserve-capacity?hl=zh-tw)」。
* 如要瞭解如何指定偏好表格，請參閱「[偏好表格](#preferred_tables)」。
* 如要瞭解如何監控使用率，請參閱「[透過 Cloud Monitoring 監控 BI Engine](https://docs.cloud.google.com/bigquery/docs/bi-engine-monitor?hl=zh-tw)」。
* 瞭解如何搭配使用 BI Engine 與[數據分析](https://docs.cloud.google.com/bigquery/docs/visualize-looker-studio?hl=zh-tw)和 [Tableau](https://docs.cloud.google.com/bigquery/docs/analyze-data-tableau?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-11-23 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-11-23 (世界標準時間)。"],[],[]]