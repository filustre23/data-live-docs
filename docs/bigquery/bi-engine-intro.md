Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# BI Engine 簡介

BigQuery BI Engine 是一種快速的記憶體內分析服務，可智慧快取最常使用的資料，藉此加快 BigQuery 中許多 SQL 查詢的速度。BI Engine 可加速處理來自任何來源的 SQL 查詢 (包括資料視覺化工具編寫的查詢)，並管理快取資料表，持續進行最佳化。您不必手動調整或分層資料，就能提升查詢效能。您可以[叢集](https://docs.cloud.google.com/bigquery/docs/clustered-tables?hl=zh-tw)和[分區](https://docs.cloud.google.com/bigquery/docs/partitioned-tables?hl=zh-tw)資料表，進一步提升大型資料表的 BI Engine 效能。

舉例來說，如果資訊主頁只顯示上季資料，您可以按時間分割資料表，這樣系統只會將最新分割區載入記憶體。您也可以結合[materialized view](https://docs.cloud.google.com/bigquery/docs/materialized-views-intro?hl=zh-tw)和 BI Engine 的優點。如果具體化檢視區是用來聯結及攤平資料，以最佳化 BI Engine 的結構，這個方法就特別有效。

BI Engine 具有下列優點：

* **BigQuery API 相容性：**BI Engine 會直接與 BigQuery API 整合。任何透過標準機制 (例如 [REST](https://docs.cloud.google.com/bigquery/docs/reference/rest?hl=zh-tw) 或 [JDBC 和 ODBC 驅動程式](https://docs.cloud.google.com/bigquery/docs/reference/odbc-jdbc-drivers?hl=zh-tw)) 使用 BigQuery API 的 BI 解決方案或自訂應用程式，都可以直接使用 BI Engine，不需進行任何修改。
* **向量化執行階段：**在執行引擎中使用向量化處理，一次處理批次資料，可更有效運用現代 CPU 架構。BI Engine 也會使用進階資料編碼 (具體來說是字典行程長度編碼)，進一步壓縮儲存在記憶體內層的資料。
* **完美整合：**BI Engine 可與 BigQuery 功能和中繼資料搭配使用，包括授權檢視區塊、資料欄層級安全防護機制和資料遮蓋。
* **預留項目分配：**BI Engine 預留項目會分別管理每個專案和區域的記憶體配置。BI Engine 只會快取查詢的必要資料欄和資料分割部分。您可以使用[偏好資料表](https://docs.cloud.google.com/bigquery/docs/bi-engine-preferred-tables?hl=zh-tw)，指定要使用 BI Engine 加速的資料表。

在大多數機構中，帳單管理員會啟用 BI Engine，並使用適當的[版本](https://docs.cloud.google.com/bigquery/docs/editions-intro?hl=zh-tw#administration_features)預留 BI Engine 加速功能容量。詳情請參閱「[預留 BI Engine 容量](https://docs.cloud.google.com/bigquery/docs/bi-engine-reserve-capacity?hl=zh-tw)」。

## BI Engine 用途

BI Engine 可大幅加快許多 SQL 查詢的速度，包括用於 BI 資訊主頁的查詢。如果您找出對查詢至關重要的資料表，然後將這些資料表標示為[偏好資料表](https://docs.cloud.google.com/bigquery/docs/bi-engine-preferred-tables?hl=zh-tw)，加速功能就能發揮最大效益。如要使用 BI Engine，請在區域中建立預留項目並指定大小。您可以讓 BigQuery 根據專案的使用模式決定要快取哪些資料表，也可以指定資料表，避免其他流量干擾加速作業。

BI Engine 適用於下列用途：

* **使用商業智慧工具分析資料**：無論 BigQuery 查詢是在 BigQuery 控制台、商業智慧工具 (例如數據分析或 Tableau)，還是用戶端程式庫、API，或 ODBC 或 JDBC 連接器中執行，BI Engine 都能加快查詢速度。這能大幅提升透過內建連線 (API) 或連結器連線至 BigQuery 的資訊主頁效能。
* **您有經常查詢的資料表**：
  BI Engine 可讓您指定偏好資料表來加快速度。如果您有經常查詢或用於高曝光度資訊主頁的資料表子集，這項功能就相當實用。

在下列情況下，BI Engine 可能不符合您的需求：

* **查詢中使用萬用字元**：BI Engine 不支援參照萬用字元資料表的查詢，因此無法加速這類查詢。
* **您需要使用 BI Engine 不支援的 BigQuery 功能**：
  雖然 BI Engine 支援大多數的 SQL 函式和運算子，但[BI Engine 不支援的功能](https://docs.cloud.google.com/bigquery/docs/bi-engine-optimized-sql?hl=zh-tw#unsupported-features)包括外部資料表、資料列層級安全性，以及非 SQL 使用者定義函式。

## BI Engine 注意事項

決定如何設定 BI Engine 時，請考量下列事項：

### 確保特定查詢的加速功能

如要確保一組查詢獲得加速，請建立專屬的 BI Engine 預留項目，並將其用於獨立專案。首先，請[估算查詢所需的運算容量](https://docs.cloud.google.com/bigquery/docs/bi-engine-reserve-capacity?hl=zh-tw#estimate_and_measure_capacity)，然後將這些資料表指定為 BI Engine 的[偏好資料表](https://docs.cloud.google.com/bigquery/docs/bi-engine-preferred-tables?hl=zh-tw)。

### 盡量減少聯結

BI Engine 最適合用於預先聯結或預先匯總的資料，以及聯結次數較少的查詢。如果聯結的一側很大，另一側很小，例如查詢大型事實資料表並聯結較小的維度資料表，就特別適合使用這項功能。您可以將 BI Engine 與[具體化檢視區塊](https://docs.cloud.google.com/bigquery/docs/materialized-views-intro?hl=zh-tw)結合，執行聯結作業，產生單一大型無格式資料表。這樣一來，系統就不會為每個查詢執行相同的聯結。建議使用過時的 materialized view，以獲得最佳查詢效能。

### 瞭解 BI Engine 的影響

如要瞭解 BI Engine 的使用情形，請參閱「[透過 Cloud Monitoring 監控 BI Engine](https://docs.cloud.google.com/bigquery/docs/bi-engine-monitor?hl=zh-tw)」一文，或查詢 [`INFORMATION_SCHEMA.BI_CAPACITIES`](https://docs.cloud.google.com/bigquery/docs/information-schema-bi-capacities?hl=zh-tw) 和 [`INFORMATION_SCHEMA.BI_CAPACITY_CHANGES`](https://docs.cloud.google.com/bigquery/docs/information-schema-bi-capacity-changes?hl=zh-tw) 檢視畫面。請務必在 BigQuery 中停用「使用快取的結果」選項，以取得最準確的比較結果。詳情請參閱「[使用快取查詢結果](https://docs.cloud.google.com/bigquery/docs/cached-results?hl=zh-tw)」一文。

### 偏好的資料表

BI Engine 偏好資料表可讓您將 BI Engine 加速功能限制在特定資料表。查詢所有其他資料表時，會使用一般 BigQuery 專用配額。舉例來說，您可以只加速處理您認為對業務重要的表格和資訊主頁。

如果專案的 RAM 不足以容納所有偏好的資料表，BI Engine 會卸載最近未存取的資料表分割區和資料欄。這個程序會釋放記憶體，供需要加速的新查詢使用。

#### 偏好資料表的限制

BI Engine 偏好資料表有下列限制：

* 您無法將檢視畫面新增至偏好資料表預訂清單。
  BI Engine 偏好資料表僅支援資料表。
* 只有在具體化檢視表和基礎資料表都位於偏好資料表清單中時，系統才會加速處理具體化檢視表的查詢。
* 系統不支援指定要加速的分區或資料欄。
* BI Engine 不支援 `JSON` 類型的資料欄，因此不會加速處理。
* 只有在所有資料表都是偏好資料表時，存取多個資料表的查詢才會加速。舉例來說，查詢中含有 `JOIN` 的所有資料表都必須位於偏好資料表清單中，才能加速查詢。如果連一個資料表都不在偏好清單中，查詢就無法使用 BI Engine。
* Google Cloud 控制台不支援公開資料集。如要將公開資料表新增為偏好資料表，請使用 API 或 DDL。

## 限制

如要使用 BI Engine，貴機構必須建立 BI Engine 預留項目，並搭配支援的版本，才能購買 BI Engine 容量。詳情請參閱[瞭解 BigQuery 版本](https://docs.cloud.google.com/bigquery/docs/editions-intro?hl=zh-tw#administration_features)。

此外，BigQuery BI Engine 還有下列限制。

### 彙整

BI Engine 可加快特定類型的聯結查詢。加速作業會在葉層級子查詢中進行，並使用 `INNER` 和 `LEFT OUTER JOINS`，其中大型事實資料表會與最多四個較小的「維度」資料表聯結。小型維度資料表有下列限制：

* 少於 500 萬列
* 大小限制：
  + 未分區資料表：5 GiB 以下
  + 分區資料表：參照的分區大小為 1 GB 以下

### 窗型函式

[窗型函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/window-function-calls?hl=zh-tw) (又稱分析函式) 在 BigQuery BI Engine 加速時，有下列限制：

* 如果輸入階段沒有視窗函式，BigQuery BI Engine 會加速處理這些階段。在本例中，請查看 `INFORMATION_SCHEMA.JOBS` 檢視畫面報表 `bi_engine_statistics`。以`FULL_INPUT`呈現的`acceleration_mode`。
* 輸入階段中含有窗型函式的查詢，其輸入階段會由 BI Engine 加速，但不會受到「[BI Engine 窗型函式限制](#window_function_limitations)」一節所述的限制。在這種情況下，輸入階段或完整查詢會在 BI Engine 中執行。在本例中，請查看 `INFORMATION_SCHEMA.JOBS` 檢視畫面報表 `bi_engine_statistics`。以 `FULL_INPUT` 或 `FULL_QUERY` 格式指定的 `acceleration_mode`。

如要進一步瞭解 `BiEngineStatistics` 欄位，請參閱[工作參考資料](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#bienginestatistics)。

#### BI Engine 窗型函式限制

只有在符合下列所有條件時，含有視窗函式的查詢才會在 BI Engine 中執行：

* 查詢只會掃描一個資料表。
  + 資料表未分區。
  + 表格列數少於 500 萬列。
* 查詢沒有 `JOIN` 運算子。
* 掃描的資料表大小乘以 window 函式運算子數量，不得超過 300 MiB。

具有相同 `OVER` 子句和相同直接輸入內容的兩個 window 函式，可以共用相同的 window 函式運算子。例如：

* `SELECT ROW_NUMBER() OVER (ORDER BY x), SUM(x) OVER (ORDER BY x)
  FROM my_table` 只有一個 window 函式運算子。
* `SELECT ROW_NUMBER() OVER (ORDER BY x), SUM(x) OVER (PARTITION BY
  y ORDER BY x) FROM my_table` 有兩個視窗函式運算子，因為這兩個函式有不同的 `OVER` 子句。
* `SELECT ROW_NUMBER() OVER (ORDER BY x) FROM (SELECT SUM(x) OVER
  (ORDER BY x) AS x FROM my_table)` 有兩個 window 函式運算子，因為這兩個函式有不同的直接輸入，但 `OVER` 子句看起來相同。

#### 支援的窗型函式

系統支援下列參照的視窗函式：

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

**分析函式與其他運算子不相容，或輸入內容過大**

### 其他 BI Engine 限制

下列功能不支援 BI Engine 加速：

* JavaScript UDF
* 外部資料表，包括 BigLake 資料表
* 查詢 JSON 資料 - 錯誤訊息：**JSON native type is not supported**
* 將結果寫入永久 BigQuery 資料表
* 使用 [BigQuery 變更資料擷取功能](https://docs.cloud.google.com/bigquery/docs/change-data-capture?hl=zh-tw)擷取資料的資料表
* [交易](https://docs.cloud.google.com/bigquery/docs/transactions?hl=zh-tw)
* 傳回超過 1 GiB 資料的查詢。對於易受延遲影響的應用程式，建議回應大小小於 1 MiB。
* 資料列層級安全性
* 使用 [`SEARCH` 函式的查詢](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/search_functions?hl=zh-tw#search)
  或透過[搜尋索引](https://docs.cloud.google.com/bigquery/docs/search-intro?hl=zh-tw)最佳化的查詢

### 不支援功能的替代方案

雖然 BigQuery BI Engine 不支援部分 SQL 功能，但您可以使用下列解決方法：

1. 在 BigQuery 中撰寫查詢。
2. 將查詢結果儲存至資料表。
3. [排定查詢時間](https://docs.cloud.google.com/bigquery/docs/scheduling-queries?hl=zh-tw)，定期更新資料表。建議每小時或每天更新一次。
   每分鐘重新整理一次可能會導致快取過於頻繁地失效。
4. 在對效能要求極高的查詢中，請參照這個表格。

## 配額與限制

如要瞭解 BI Engine 適用的配額與限制，請參閱 [BigQuery 配額與限制](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#biengine-limits)。

## 定價

您需要支付為 BI Engine 容量建立預留項目所產生的費用。如要瞭解 BI Engine 的計價方式，請參閱 [BigQuery 定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#bi_engine_pricing)頁面。

## 後續步驟

* 如要瞭解如何建立 BI Engine 預留項目，請參閱「[預留 BI Engine 容量](https://docs.cloud.google.com/bigquery/docs/bi-engine-reserve-capacity?hl=zh-tw)」。
* 如要瞭解如何指定偏好資料表，請參閱「[BI Engine 偏好資料表](https://docs.cloud.google.com/bigquery/docs/bi-engine-preferred-tables?hl=zh-tw)」。
* 如要瞭解 BI Engine 的使用情形，請參閱「[透過 Cloud Monitoring 監控 BI Engine](https://docs.cloud.google.com/bigquery/docs/bi-engine-monitor?hl=zh-tw)」。
* 瞭解 [BI Engine 最佳化函式](https://docs.cloud.google.com/bigquery/docs/bi-engine-optimized-sql?hl=zh-tw)
* 瞭解如何搭配下列項目使用 BI Engine：
  + [數據分析](https://docs.cloud.google.com/bigquery/docs/visualize-looker-studio?hl=zh-tw)
  + [Tableau](https://docs.cloud.google.com/bigquery/docs/analyze-data-tableau?hl=zh-tw)




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-02 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-02 (世界標準時間)。"],[],[]]