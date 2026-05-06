Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 什麼是 BI Engine？

BigQuery BI Engine 是一種快速的記憶體內分析服務，可智慧快取最常使用的資料，藉此加快 BigQuery 中許多 SQL 查詢的速度。BI Engine 可加速處理來自任何來源的 SQL 查詢 (包括資料視覺化工具編寫的查詢)，並管理快取資料表，持續進行最佳化。您不必手動調整或分層資料，就能提升查詢效能。您可以運用[叢集](https://docs.cloud.google.com/bigquery/docs/clustered-tables?hl=zh-tw)和[分區](https://docs.cloud.google.com/bigquery/docs/partitioned-tables?hl=zh-tw)，進一步提升 BI Engine 大型資料表的效能。

舉例來說，如果資訊主頁只顯示上季資料，請考慮按時間劃分資料表，這樣只有最新的分區會載入記憶體。您也可以結合[具體化檢視區塊](https://docs.cloud.google.com/bigquery/docs/materialized-views-intro?hl=zh-tw)和 BI Engine 的優點。如果具體化檢視區是用來聯結及平坦化資料，以最佳化 BI Engine 的結構，這個做法就特別有效。

BI Engine 具有下列優點：

1. **BigQuery API：**BI Engine 會直接與 BigQuery API 整合。任何透過標準機制 (例如 [REST](https://docs.cloud.google.com/bigquery/docs/reference/rest?hl=zh-tw) 或 [JDBC 和 ODBC 驅動程式](https://docs.cloud.google.com/bigquery/docs/reference/odbc-jdbc-drivers?hl=zh-tw)) 使用 BigQuery API 的 BI 解決方案或自訂應用程式，都可以直接使用 BI Engine，不需進行任何修改。
2. **向量化執行階段：**透過 BI Engine，BigQuery 會使用稱為「向量化處理」的現代技術。在執行引擎中使用向量化處理，可一次處理批次資料，更有效運用現代 CPU 架構。BI Engine 也會使用進階資料編碼 (具體來說是字典和行程長度編碼)，進一步壓縮儲存在記憶體層中的資料。
3. **完美整合：**BI Engine 可與 BigQuery 功能和中繼資料搭配使用，包括授權檢視畫面、資料欄和資料列層級安全防護，以及資料遮蓋。
4. **預留項目：**BI Engine 預留項目會在專案位置層級管理記憶體分配。BI Engine 會快取查詢的特定資料欄或分區，並優先處理標示為偏好的資料表。

### BI Engine 架構

BI Engine 可與任何商業智慧 (BI) 工具整合，包括 Looker、Tableau、Power BI 和自訂應用程式，加快資料探索和分析速度。

## BI Engine 用途

BI Engine 可大幅加快許多 SQL 查詢的速度，包括用於 BI 資訊主頁的查詢。如要發揮最佳加速效果，請找出查詢作業不可或缺的資料表，然後將這些資料表標示為[偏好的資料表](https://docs.cloud.google.com/bigquery/docs/bi-engine-preferred-tables?hl=zh-tw)。如要使用 BI Engine，請建立預留項目，定義專供 BI Engine 使用的儲存空間容量。您可以讓 BigQuery 根據專案的使用模式決定要快取哪些資料表，也可以標記特定資料表，避免其他流量干擾加速作業。

BI Engine 適用於下列用途：

* **使用 BI 工具分析資料**：無論 BigQuery 查詢是在 BigQuery 控制台、用戶端程式庫中執行，還是透過 API 或 ODBC/JDBC 連接器執行，BI Engine 都能加速查詢。這項功能可大幅提升透過內建連線 (API) 或連接器連線至 BigQuery 的資訊主頁效能。
* **您有最常查詢的特定資料表**：
  BI Engine 可讓您指定要加速的偏好資料表。如果您有經常查詢或用於高曝光度資訊主頁的資料表子集，這項功能就相當實用。

在下列情況下，BI Engine 可能不符合您的需求：

* **您在查詢中使用萬用字元**：BI Engine 不支援參照萬用字元資料表的查詢，且無法加速這類查詢。
* **您大量使用不支援的 BigQuery 功能**：將商業智慧 (BI) 工具連線至 BigQuery 時，BI Engine 支援大多數的 [SQL 函式和運算子](https://docs.cloud.google.com/bigquery/docs/bi-engine-optimized-sql?hl=zh-tw)，但仍有[不支援的功能](https://docs.cloud.google.com/bigquery/docs/bi-engine-optimized-sql?hl=zh-tw#unsupported-features)，包括外部資料表和非 SQL 使用者定義函式。

## BI Engine 注意事項

決定如何設定 BI Engine 時，請考量下列事項：

### 確保特定查詢的加速功能

您可以建立含有 BI Engine 預留項目的獨立專案，確保特定查詢集一律會加速執行。如要這麼做，請確保專案中的 BI Engine 預留項目夠大，足以容納這些查詢中使用的所有資料表，並將這些資料表指定為 BI Engine 的[偏好資料表](https://docs.cloud.google.com/bigquery/docs/bi-engine-preferred-tables?hl=zh-tw)。只有需要加速的查詢才應在該專案中執行。

### 盡量減少聯結

BI Engine 最適合搭配預先彙整或預先彙整的資料，以及少量彙整的資料。如果聯結的一側很大，另一側很小，例如查詢大型事實資料表並聯結小型維度資料表時，這種情況尤其明顯。您可以將 BI Engine 與[具體化檢視區塊](https://docs.cloud.google.com/bigquery/docs/materialized-views-intro?hl=zh-tw)結合，執行聯結作業，產生單一大型平面資料表。這樣一來，就不必在每次查詢時執行相同的聯結。

### 瞭解 BI Engine 的影響

如要進一步瞭解工作負載如何從 BI Engine 受益，請[查看 Cloud Monitoring 中的使用統計資料](https://docs.cloud.google.com/bigquery/docs/bi-engine-intro?hl=zh-tw#limitations)，或在 BigQuery 中查詢 [INFORMATION\_SCHEMA](https://docs.cloud.google.com/bigquery/docs/bi-engine-monitor?hl=zh-tw#information_schema)。請務必在 BigQuery 中停用「使用快取的結果」選項，以取得最準確的比較結果。詳情請參閱「[使用快取查詢結果](https://docs.cloud.google.com/bigquery/docs/cached-results?hl=zh-tw)」一文。

## 限制

含有 [`VECTOR_SEARCH` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/search_functions?hl=zh-tw#vector_search)的查詢不會透過 [BigQuery BI Engine](https://docs.cloud.google.com/bigquery/docs/bi-engine-intro?hl=zh-tw) 加速。

## 配額與限制

如要瞭解 BI Engine 適用的配額與限制，請參閱 [BigQuery 配額與限制](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#biengine-limits)。

## 定價

如要瞭解 BI Engine 的計價方式，請參閱 [BigQuery 定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#bi_engine_pricing)頁面。

## 查詢最佳化和加速

**注意：** 如要瞭解 BI Engine 預留項目大小上限，請參閱「[配額與限制](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#biengine-limits)」一文。

BigQuery (以及 BI Engine) 會將 SQL 查詢產生的查詢計畫分解為子查詢。子查詢包含多項作業，例如掃描、篩選或彙整資料，通常是分片上的執行單元。

雖然 BI Engine 會正確執行所有 BigQuery 支援的 SQL 查詢，但只會最佳化特定子查詢。具體來說，BI Engine 最適合用於從儲存空間掃描資料的葉層級子查詢，並執行篩選、運算、匯總、排序依據和特定類型的聯結等作業。其他尚未完全由 BI Engine 加速的子查詢，則會還原為 BigQuery 執行。

由於這項選擇性最佳化功能，簡單的商業智慧或資訊主頁類型查詢最能從 BI Engine 受益 (因此子查詢較少)，因為大部分的執行時間都花在處理原始資料的葉層級子查詢。

## 後續步驟

* 瞭解 [BI Engine 最佳化函式](https://docs.cloud.google.com/bigquery/docs/bi-engine-optimized-sql?hl=zh-tw)。
* 如要瞭解如何建立 BI Engine 預留項目，請參閱「[預留 BI Engine 容量](https://docs.cloud.google.com/bigquery/docs/bi-engine-reserve-capacity?hl=zh-tw)」。
* 如要瞭解如何指定偏好資料表，請參閱「[BI Engine 偏好資料表](https://docs.cloud.google.com/bigquery/docs/bi-engine-preferred-tables?hl=zh-tw)」。
* 如要瞭解 BI Engine 的使用率，請參閱「[透過 Cloud Monitoring 監控 BI Engine](https://docs.cloud.google.com/bigquery/docs/bi-engine-monitor?hl=zh-tw)」。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-06 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-06 (世界標準時間)。"],[],[]]