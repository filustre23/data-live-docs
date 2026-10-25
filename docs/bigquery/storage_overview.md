Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# BigQuery 儲存空間總覽

BigQuery 儲存空間經過最佳化調整，能對大型資料集執行分析查詢。此外，這項服務也支援高處理量的串流擷取和讀取作業。瞭解 BigQuery 儲存空間，有助於最佳化工作負載。

## 總覽

BigQuery 架構的主要特色之一，是將儲存和運算作業分開。因此 BigQuery 可視需求分別調度儲存和運算資源。

**圖 1：**BigQuery 架構。

執行查詢時，查詢引擎會將工作平行分配給多個 worker，這些 worker 會掃描儲存空間中的相關資料表、處理查詢，然後收集結果。BigQuery 完全在記憶體中執行查詢，並使用 Pb 級網路，確保資料能以極快的速度移至 worker 節點。

以下是 BigQuery 儲存空間的幾項重要功能：

* **代管**。BigQuery 儲存空間是完全代管的服務。您不必佈建儲存空間資源或預留儲存空間單位。當您將資料載入系統時，BigQuery 會自動為您分配儲存空間。您只需支付實際使用的儲存空間費用。BigQuery 的計費模式會分別收取運算和儲存費用。如需定價詳情，請參閱「[BigQuery 定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#storage)」。
* **Durable**。BigQuery 儲存空間的年度耐用性高達 99.999999999% (11 個 9)。BigQuery 會在多個可用區複製資料，避免因機器層級故障或[可用區](https://docs.cloud.google.com/docs/geography-and-regions?hl=zh-tw#zonal_resources)故障而遺失資料。詳情請參閱「[可靠性：災難規劃](https://docs.cloud.google.com/bigquery/docs/reliability-intro?hl=zh-tw#disaster_planning)」。
* **加密**。BigQuery 會在資料寫入磁碟前自動加密，您可以提供自己的加密金鑰，或讓 Google 管理加密金鑰。詳情請參閱「[靜態資料加密](https://docs.cloud.google.com/bigquery/docs/encryption-at-rest?hl=zh-tw)」。
* **高效率**：BigQuery 儲存空間採用高效編碼格式，專為分析工作負載最佳化。
  如要進一步瞭解 BigQuery 的儲存格式，請參閱網誌文章「[Inside Capacitor, BigQuery's next-generation columnar storage format](https://cloud.google.com/blog/products/bigquery/inside-capacitor-bigquerys-next-generation-columnar-storage-format?hl=zh-tw)」(Capacitor 內部：BigQuery 的新一代欄式儲存格式)。

## 資料表內容

您在 BigQuery 中儲存的大部分資料都是資料表資料。資料表資料包括標準資料表、資料表複製、資料表快照和 materialized view。系統會根據您用於這些資源的儲存空間計費。詳情請參閱「[儲存空間定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#storage)」。

* [標準資料表](https://docs.cloud.google.com/bigquery/docs/tables-intro?hl=zh-tw)包含結構化資料。每個資料表都有結構定義，結構定義中的每個資料欄都有資料類型。BigQuery 會以資料欄格式儲存資料。請參閱本文的「[儲存空間版面配置](#storage_layout)」一節。
* [資料表本機副本](https://docs.cloud.google.com/bigquery/docs/table-clones-intro?hl=zh-tw)是標準資料表的輕量可寫入副本。BigQuery 只會儲存資料表複製版本與基礎資料表之間的差異。
* [資料表快照](https://docs.cloud.google.com/bigquery/docs/table-snapshots-intro?hl=zh-tw)是資料表的特定時間點副本。資料表快照為唯讀，但您可以從資料表快照還原資料表。BigQuery 只會儲存資料表快照與基礎資料表之間的差異。
* [materialized view](https://docs.cloud.google.com/bigquery/docs/materialized-views-intro?hl=zh-tw) 是預先運算的 view，會定期快取 view 查詢的結果。快取結果會儲存在 BigQuery 儲存空間中。

此外，[快取查詢結果](https://docs.cloud.google.com/bigquery/docs/cached-results?hl=zh-tw)會儲存為臨時資料表。儲存在暫存資料表中的快取查詢結果不會產生費用。

「外部資料表」是一種特殊類型的資料表，資料位於 BigQuery 外部的資料儲存庫，例如 Cloud Storage。外部資料表與標準資料表一樣，都有資料表結構定義，但資料表定義會指向外部資料儲存庫。在這種情況下，BigQuery 儲存空間只會保留資料表中繼資料。BigQuery 不會針對外部資料表儲存空間收取費用，但外部資料儲存庫可能會收取儲存空間費用。

BigQuery 會將資料表和其他資源整理成邏輯容器，稱為「資料集」。BigQuery 資源的分組方式會影響 BigQuery 工作負載的權限、配額、計費和其他方面。如需更多資訊和最佳做法，請參閱「[資源階層簡介](https://docs.cloud.google.com/bigquery/docs/resource-hierarchy?hl=zh-tw)」。

資料表使用的資料保留政策，取決於資料表所在資料集的設定。詳情請參閱「[透過時間旅行和安全防護機制保留資料](https://docs.cloud.google.com/bigquery/docs/time-travel?hl=zh-tw)」。

## 中繼資料

BigQuery 儲存空間也會保存 BigQuery 資源的中繼資料。中繼資料儲存空間不收費。

在 BigQuery 建立任何永久實體 (例如資料表、檢視表或 user-defined function (UDF)) 時，BigQuery 會儲存實體的中繼資料。即使資源不含任何資料表資料 (例如 UDF 和邏輯檢視表)，也適用這項規定。

中繼資料包含資料表結構定義、分區和分群規格、資料表到期時間等資訊。這類中繼資料會向使用者顯示，您可以在建立資源時設定。此外，BigQuery 會儲存中繼資料，並在內部使用這些資料來最佳化查詢。使用者無法直接看到這項中繼資料。

## 儲存空間配置

許多傳統資料庫系統會以資料列導向格式儲存資料，也就是將資料列儲存在一起，且每個資料列中的欄位會依序顯示在磁碟上。以資料列為主的資料庫可有效查詢個別記錄。不過，在多筆記錄中執行分析函式時，效率可能較低，因為系統在存取記錄時必須讀取每個欄位。

**圖 2.** 資料列導向格式。

BigQuery 會以*資料欄*格式儲存資料表資料，也就是說，每個資料欄都會分開儲存。資料欄導向資料庫在掃描整個資料集的個別資料欄時，效率特別高。

資料欄導向資料庫經過最佳化，適合用於匯總大量記錄資料的分析工作負載。分析查詢通常只需要讀取資料表中的幾個資料欄。舉例來說，如果您想計算某個資料欄在數百萬列中的總和，BigQuery 可以讀取該資料欄的資料，而不必讀取每一列的每個欄位。

資料欄導向資料庫的另一個優點是，資料欄內的資料通常比資料列中的資料更具備備援性。這項特性可讓您使用遊程編碼等技術，進一步壓縮資料，進而提升讀取效能。

**圖 3.** 資料欄導向格式。

## 儲存空間計費模式

BigQuery 提供兩種儲存空間計費模式：**邏輯** (未壓縮) 和**實體** (壓縮)。

變更儲存空間計費模式只會變更計量設定，不涉及資料遷移、檔案格式轉換或任何基礎架構變更。資料一律會以相同的壓縮實體格式儲存。變更這項設定不會影響查詢效能、延遲時間，或與其他應用程式 (例如 Looker) 的整合。

所選模式只會決定系統如何根據[儲存空間定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#storage)，衡量儲存位元組並計價：

* **邏輯計費：**依據未壓縮的資料大小計費。這是預設模型。
* **實體計費：**根據磁碟上資料的壓縮大小計費。

無論選擇哪種計費模式，資料都會以實際位元組的形式儲存。

您可以在資料集層級設定儲存空間計費模式。如果您在建立資料集時未指定儲存空間計費模式，系統預設會使用邏輯儲存空間計費模式。不過，您可以在建立資料集後[變更其儲存空間計費模式](https://docs.cloud.google.com/bigquery/docs/updating-datasets?hl=zh-tw#update_storage_billing_models)。變更資料集的儲存空間計費模式後，必須等待 14 天才能再次變更。

變更資料集的計費模式後，變更會在 24 小時後生效。變更資料集的計費模式時，長期儲存空間中的任何資料表或資料表分區都不會重設為使用中儲存空間。變更資料集的計費模式不會影響查詢效能和查詢延遲時間。

資料集會使用[時間旅行](https://docs.cloud.google.com/bigquery/docs/time-travel?hl=zh-tw#time_travel)和[安全防護](https://docs.cloud.google.com/bigquery/docs/time-travel?hl=zh-tw#fail-safe)儲存空間來保留資料。如果採用實體儲存空間計費模式，系統會按照使用中儲存空間費率，分別收取時光旅行和防故障儲存空間的費用。如果採用邏輯儲存空間計費模式，則會按照基本費率收取費用。您可以修改資料集的時間回溯時間範圍，在實體儲存空間費用和資料保留之間取得平衡。您無法修改安全防護時間範圍。如要進一步瞭解資料集資料保留，請參閱「[使用時間旅行和防故障功能保留資料](https://docs.cloud.google.com/bigquery/docs/time-travel?hl=zh-tw)」。如要進一步瞭解如何預測儲存空間費用，請參閱「[預測儲存空間費用](https://docs.cloud.google.com/bigquery/docs/information-schema-table-storage?hl=zh-tw#forecast_storage_billing)」。

如果貴組織在資料集所在區域有任何舊版[固定費率運算單元承諾使用合約](https://docs.cloud.google.com/bigquery/docs/reservations-commitments-legacy?hl=zh-tw)，就無法為資料集註冊實體儲存空間計費模式。這項規定不適用於透過 [BigQuery 版本](https://docs.cloud.google.com/bigquery/docs/editions-intro?hl=zh-tw)購買的承諾使用合約。

## 儲存空間最佳化

最佳化 BigQuery 儲存空間可提升查詢效能並控管成本。如要查看資料表儲存空間中繼資料，請查詢下列 `INFORMATION_SCHEMA` 檢視表：

* [`INFORMATION_SCHEMA.TABLE_STORAGE`](https://docs.cloud.google.com/bigquery/docs/information-schema-table-storage?hl=zh-tw)
* [`INFORMATION_SCHEMA.TABLE_STORAGE_BY_ORGANIZATION`](https://docs.cloud.google.com/bigquery/docs/information-schema-table-storage-by-organization?hl=zh-tw)

如要瞭解如何最佳化儲存空間，請參閱「[最佳化 BigQuery 儲存空間](https://docs.cloud.google.com/bigquery/docs/best-practices-storage?hl=zh-tw)」。

## 載入資料

將資料擷取至 BigQuery 的基本模式有幾種。

* **批次載入：**透過單一批次作業，將來源資料載入 BigQuery 資料表。這可以是一次性作業，也能是依排程自動執行。批次載入作業可建立新資料表，或將資料附加到現有資料表。
* **串流：**持續串流較小批次的資料，以便近乎即時地查詢資料。
* **產生資料：**使用 SQL 陳述式將資料列插入現有資料表，或將查詢結果寫入資料表。

如要進一步瞭解何時應選擇這些擷取方法，請參閱「[載入資料簡介](https://docs.cloud.google.com/bigquery/docs/loading-data?hl=zh-tw)」。如需定價資訊，請參閱「[資料擷取定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#data_ingestion_pricing)」。

## 從 BigQuery 儲存空間讀取資料

在大多數情況下，您會將資料儲存在 BigQuery 中，以便對資料執行分析[查詢](https://docs.cloud.google.com/bigquery/docs/query-overview?hl=zh-tw)。不過，有時您可能想直接從資料表讀取記錄。BigQuery 提供多種讀取資料表資料的方法：

* **[BigQuery API](https://docs.cloud.google.com/bigquery/docs/reference/rest?hl=zh-tw)：**使用 [`tabledata.list`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tabledata/list?hl=zh-tw) 方法同步分頁存取。資料會以序列方式讀取，每次叫用一頁。詳情請參閱「[瀏覽資料表資料](https://docs.cloud.google.com/bigquery/docs/managing-table-data?hl=zh-tw#browse-table)」。
* **[BigQuery Storage API](https://docs.cloud.google.com/bigquery/docs/reference/storage?hl=zh-tw)：**串流高處理量存取，也支援伺服器端資料欄投影和篩選。將讀取作業分割成多個不相交的串流，即可在多個讀取器之間平行處理讀取作業。
* **[匯出](https://docs.cloud.google.com/bigquery/docs/exporting-data?hl=zh-tw)：**使用擷取工作或 [`EXPORT DATA` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/export-statements?hl=zh-tw)，以非同步方式將高處理量資料複製到 Google Cloud Storage。如要複製 Cloud Storage 中的資料，請使用擷取工作或 `EXPORT DATA` 陳述式匯出資料。
* **[複製](https://docs.cloud.google.com/bigquery/docs/copying-datasets?hl=zh-tw)：**在 BigQuery 中非同步複製資料集。如果來源和目的地位置相同，系統會以邏輯方式完成複製。

如需定價資訊，請參閱「[資料擷取定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#data_extraction_pricing)」。

您可以根據應用程式需求，讀取資料表資料：

* **讀取及複製：**如需在 Cloud Storage 中建立靜態副本，請使用擷取工作或 `EXPORT DATA` 陳述式匯出資料。如果只想讀取資料，請使用 BigQuery Storage API。如要在 BigQuery 內建立副本，請使用複製工作。
* **規模：**BigQuery API 是效率最低的方法，不應用於大量讀取。如果每天需要匯出超過 50 TB 的資料，請使用 `EXPORT DATA` 陳述式或 BigQuery Storage API。
* **傳回第一列所需的時間：**BigQuery API 是傳回第一列最快的方法，但只能用於讀取少量資料。BigQuery Storage API 傳回第一列的速度較慢，但處理量高得多。匯出和複製作業必須先完成，才能讀取任何資料列，因此這類工作的首列時間可能長達數分鐘。

## 刪除

刪除資料表後，資料至少會保留[時間回溯期](https://docs.cloud.google.com/bigquery/docs/time-travel?hl=zh-tw)。
之後，系統會在[Google Cloud 刪除時間軸](https://docs.cloud.google.com/docs/security/deletion?hl=zh-tw#deletion_timeline)內，從磁碟中清除資料。
部分刪除作業 (例如 [`DROP COLUMN` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#alter_table_drop_column_statement)) 僅限中繼資料作業。在這種情況下，下次修改受影響的資料列時，系統就會釋出儲存空間。如果不修改資料表，則無法保證釋出儲存空間的時間。
詳情請參閱「 [Google Cloud的資料刪除](https://docs.cloud.google.com/docs/security/deletion?hl=zh-tw)」。

## 後續步驟

* 瞭解如何[使用表格](https://docs.cloud.google.com/bigquery/docs/tables-intro?hl=zh-tw)。
* 瞭解如何[最佳化儲存空間](https://docs.cloud.google.com/bigquery/docs/best-practices-storage?hl=zh-tw)。
* 瞭解如何[在 BigQuery 中查詢資料](https://docs.cloud.google.com/bigquery/docs/query-overview?hl=zh-tw)。
* 瞭解[資料安全性與管理](https://docs.cloud.google.com/bigquery/docs/data-governance?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-10-24 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-10-24 (世界標準時間)。"],[],[]]