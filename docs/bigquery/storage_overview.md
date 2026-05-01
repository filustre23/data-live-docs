* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# BigQuery 儲存空間總覽

本頁說明 BigQuery 的儲存空間元件。

BigQuery 儲存空間經過最佳化調整，能對大型資料集進行分析式查詢。此外，它也支援高處理量的串流擷取和讀取作業。瞭解 BigQuery 儲存空間有助於最佳化工作負載。

## 總覽

BigQuery 架構的主要功能之一，就是將儲存空間和運算資源分開。因此 BigQuery 可視需求分別調度儲存和運算資源。



執行查詢時，查詢引擎會將工作平行分配給多個 worker，這些 worker 會掃描儲存空間中的相關資料表、處理查詢，然後收集結果。BigQuery 會完全在記憶體中執行查詢，並使用 Pb 級網路，確保資料能極快地移至工作節點。

以下是 BigQuery 儲存空間的幾項重要功能：

* **受管理**。BigQuery 儲存空間是全代管服務。您不需要佈建儲存空間資源或保留儲存空間單位。將資料載入系統時，BigQuery 會自動為您分配儲存空間。您只需要為自己使用的儲存空間支付費用。BigQuery 計費模式會分別收取運算和儲存空間費用。如需定價詳情，請參閱 [BigQuery 定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#storage)。
* **Durable**。BigQuery 儲存空間專為達成 99.999999999% (11 個 9) 的年度耐用性而設計，BigQuery 會跨多個可用區複製資料，避免因機器層級或[區域](https://docs.cloud.google.com/docs/geography-and-regions?hl=zh-tw#zonal_resources)故障而遺失資料。詳情請參閱「[可靠性：災難規劃](https://docs.cloud.google.com/bigquery/docs/reliability-intro?hl=zh-tw#disaster_planning)」。
* **已加密**。BigQuery 會在將所有資料寫入磁碟之前，自動加密資料，您可以提供自己的加密金鑰，也可以讓 Google 管理加密金鑰。詳情請參閱「[靜態加密](https://docs.cloud.google.com/bigquery/docs/encryption-at-rest?hl=zh-tw)」。
* **效率出眾**。BigQuery 儲存空間採用高效率的編碼格式，最適合用於分析工作負載。
  如要進一步瞭解 BigQuery 的儲存格式，請參閱「[Inside Capacitor, BigQuery's next-generation columnar storage format](https://cloud.google.com/blog/products/bigquery/inside-capacitor-bigquerys-next-generation-columnar-storage-format?hl=zh-tw)」這篇網誌文章。

## 資料表內容

您儲存在 BigQuery 中的大部分資料都是表格資料。資料表資料包括標準資料表、資料表副本、資料表快照和具體化檢視區塊。您必須為這些資源使用的儲存空間付費。詳情請參閱[儲存空間價格](https://cloud.google.com/bigquery/pricing?hl=zh-tw#storage)。

* [標準資料表](https://docs.cloud.google.com/bigquery/docs/tables-intro?hl=zh-tw)包含結構化資料。每個資料表都有結構定義，且結構定義中的每個資料欄都有資料類型。BigQuery 會以資料欄格式儲存資料。請參閱本文的「[儲存空間配置](#storage_layout)」一節。
* [資料表本機副本](https://docs.cloud.google.com/bigquery/docs/table-clones-intro?hl=zh-tw)是標準資料表的輕量型可寫入副本。BigQuery 只會儲存資料表副本與基礎資料表之間的差異。
* [資料表快照](https://docs.cloud.google.com/bigquery/docs/table-snapshots-intro?hl=zh-tw)是資料表在特定時間點的副本。資料表快照為唯讀，但您可以從資料表快照還原資料表。BigQuery 只會儲存資料表快照與其基礎資料表之間的差異。
* [具體化檢視區塊](https://docs.cloud.google.com/bigquery/docs/materialized-views-intro?hl=zh-tw)是預先計算的檢視區塊，會定期快取檢視區塊查詢的結果。快取結果會儲存在 BigQuery 儲存空間中。

此外，[快取的查詢結果](https://docs.cloud.google.com/bigquery/docs/cached-results?hl=zh-tw)會儲存為暫時性資料表。系統不會針對儲存在臨時資料表中的快取查詢結果收費。

[外部資料表](https://docs.cloud.google.com/bigquery/docs/external-tables?hl=zh-tw)是一種特殊類型的資料表，資料位於 BigQuery 外部的資料存放區，例如 Cloud Storage。外部資料表與標準資料表一樣有資料表結構，但資料表定義會指向外部資料存放區。在這種情況下，只有資料表的中繼資料會保留在 BigQuery 儲存空間中。BigQuery 不會收取外部資料表儲存空間的費用，但外部資料儲存空間可能會收取儲存空間費用。

BigQuery 會將資料表和其他資源整理成稱為「資料集」的邏輯容器。BigQuery 資源的分組方式會影響權限、配額、帳單，以及 BigQuery 工作負載的其他層面。如需更多資訊和最佳做法，請參閱「[整理 BigQuery 資源](https://docs.cloud.google.com/bigquery/docs/resource-hierarchy?hl=zh-tw)」。

資料表使用的資料保留政策取決於包含該資料表的資料集設定。詳情請參閱「[資料保留與時間旅行和容錯移轉](https://docs.cloud.google.com/bigquery/docs/time-travel?hl=zh-tw)」。

## 中繼資料

BigQuery 儲存空間也會保留 BigQuery 資源的中繼資料。系統不會收取中繼資料儲存費用。

在 BigQuery 中建立任何永久實體 (例如資料表、檢視區塊或使用者定義函式 (UDF)) 時，BigQuery 會儲存實體的相關中繼資料。即使資源不含任何資料表資料 (例如 UDF 和邏輯檢視表)，也適用這項規定。

中繼資料包括資料表結構定義、分割和叢集規格、資料表到期時間等資訊。這類中繼資料會向使用者顯示，且可在建立資源時設定。此外，BigQuery 會儲存內部使用的中繼資料，以最佳化查詢。使用者無法直接看到這項中繼資料。

## 儲存空間配置

許多傳統資料庫系統會以資料列導向格式儲存資料，也就是將資料列儲存在一起，且每個資料列中的欄位會依序顯示在磁碟上。以資料列為準的資料庫可有效率地查閱個別記錄。不過，在許多記錄中執行分析函式時，效率可能較低，因為系統存取記錄時必須讀取每個欄位。



BigQuery 會以*資料欄*格式儲存資料表資料，也就是分別儲存每個資料欄。以資料欄為導向的資料庫特別擅長掃描整個資料集中的個別資料欄。

以資料欄為導向的資料庫經過最佳化調整，可處理分析工作負載，匯總大量記錄中的資料。通常，分析查詢只需要讀取資料表中的幾個資料欄。舉例來說，如果您想計算數百萬列資料中某個資料欄的總和，BigQuery 可以讀取該資料欄的資料，而不必讀取每列資料的每個欄位。

以欄為導向的資料庫另一個優點是，欄內的資料通常比列內的資料更冗餘。這項特性可使用行程長度編碼等技術，進一步壓縮資料，進而提升讀取效能。



## 儲存空間計費模式

系統會以邏輯或實體 (壓縮) 位元組，或兩者合併計算 BigQuery 資料儲存空間費用。您選擇的儲存空間計費模式會決定[儲存空間價格](https://cloud.google.com/bigquery/pricing?hl=zh-tw#storage)。您選擇的儲存空間計費模式不會影響 BigQuery 效能。無論選擇哪種計費模式，資料都會以實際位元組的形式儲存。

您可以在資料集層級設定儲存空間帳單模型。
如果您在建立資料集時未指定儲存空間計費模式，系統預設會採用邏輯儲存空間計費模式。不過，您可以在建立資料集後[變更資料集的儲存空間計費模式](https://docs.cloud.google.com/bigquery/docs/updating-datasets?hl=zh-tw#update_storage_billing_models)。變更資料集的儲存空間計費模式後，必須等待 14 天才能再次變更。

變更資料集的計費模式後，需要 24 小時才會生效。變更資料集的計費模式時，長期儲存空間中的任何資料表或資料表分區都不會重設為近期內容儲存空間。變更資料集的計費模式不會影響查詢效能和查詢延遲。

資料集會使用[時空旅行](https://docs.cloud.google.com/bigquery/docs/time-travel?hl=zh-tw#time_travel)和[安全](https://docs.cloud.google.com/bigquery/docs/time-travel?hl=zh-tw#fail-safe)儲存空間來保留資料。使用實體儲存空間計費時，時間旅行和安全儲存空間會以有效儲存空間費率另外計費，但使用邏輯儲存空間計費時，則會納入基本費率。您可以修改資料集使用的時空旅行時間範圍，在實體儲存空間費用與資料保留之間取得平衡。您無法修改安全期。如要進一步瞭解資料集資料保留機制，請參閱「[使用時間旅行和容錯機制保留資料](https://docs.cloud.google.com/bigquery/docs/time-travel?hl=zh-tw)」。如要進一步瞭解如何預估儲存空間費用，請參閱「[預估儲存空間帳單](https://docs.cloud.google.com/bigquery/docs/information-schema-table-storage?hl=zh-tw#forecast_storage_billing)」。

如果貴機構在與資料集相同的地區中，有任何現有的舊版[固定費率配額承諾](https://docs.cloud.google.com/bigquery/docs/reservations-commitments-legacy?hl=zh-tw)，就無法為資料集註冊實體儲存空間帳單。這不適用於使用 [BigQuery 版本](https://docs.cloud.google.com/bigquery/docs/editions-intro?hl=zh-tw)購買的承諾。

## 儲存空間最佳化

將 BigQuery 儲存空間最佳化，可提升查詢效能並控管費用。如要查看資料表儲存空間中繼資料，請查詢下列 `INFORMATION_SCHEMA` 檢視畫面：

* [`INFORMATION_SCHEMA.TABLE_STORAGE`](https://docs.cloud.google.com/bigquery/docs/information-schema-table-storage?hl=zh-tw)
* [`INFORMATION_SCHEMA.TABLE_STORAGE_BY_ORGANIZATION`](https://docs.cloud.google.com/bigquery/docs/information-schema-table-storage-by-organization?hl=zh-tw)

如要瞭解如何最佳化儲存空間，請參閱「[在 BigQuery 中最佳化儲存空間](https://docs.cloud.google.com/bigquery/docs/best-practices-storage?hl=zh-tw)」。

## 載入資料

將資料擷取至 BigQuery 的基本模式有幾種。

* **批次載入：**在單一批次作業中，將來源資料載入 BigQuery 資料表。這可以是一次性作業，也能是依排程自動執行。批次載入作業可建立新資料表或將資料附加到現有資料表中。
* **串流：**持續串流較小批次的資料，如此一來就能近乎即時地查詢資料。
* **產生資料：**使用 SQL 陳述式將資料列插入現有資料表，或將查詢結果寫入資料表。

如要進一步瞭解何時該選擇哪種擷取方法，請參閱[載入資料簡介](https://docs.cloud.google.com/bigquery/docs/loading-data?hl=zh-tw)。如要查看定價資訊，請參閱「[資料擷取定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#data_ingestion_pricing)」。

## 從 BigQuery 儲存空間讀取資料

在大多數情況下，您會在 BigQuery 中儲存資料，以便對該資料執行分析[查詢](https://docs.cloud.google.com/bigquery/docs/query-overview?hl=zh-tw)。不過，有時您可能想直接從資料表讀取記錄。BigQuery 提供多種讀取資料表資料的方法：

* **[BigQuery API](https://docs.cloud.google.com/bigquery/docs/reference/rest?hl=zh-tw)：**
  使用 [`tabledata.list`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tabledata/list?hl=zh-tw) 方法進行同步分頁存取。
  資料會依序讀取，每次呼叫讀取一頁。詳情請參閱[瀏覽資料表資料](https://docs.cloud.google.com/bigquery/docs/managing-table-data?hl=zh-tw#browse-table)。
* **[BigQuery Storage API](https://docs.cloud.google.com/bigquery/docs/reference/storage?hl=zh-tw)：**
  支援高輸送量存取，也支援伺服器端欄位投影和篩選。您可以將讀取作業區隔為多個不相交的串流，在多個讀取器之間平行處理。
* **[匯出](https://docs.cloud.google.com/bigquery/docs/exporting-data?hl=zh-tw)：**
  以非同步方式將資料大量複製到 Google Cloud Storage，可透過擷取作業或 [`EXPORT DATA` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/export-statements?hl=zh-tw)進行。如要複製 Cloud Storage 中的資料，請使用擷取工作或 `EXPORT DATA` 陳述式匯出資料。
* **[複製](https://docs.cloud.google.com/bigquery/docs/copying-datasets?hl=zh-tw)：**
  在 BigQuery 中非同步複製資料集。如果來源和目的地位置相同，系統會以邏輯方式複製。

如需定價資訊，請參閱「[資料擷取定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#data_extraction_pricing)」。

根據應用程式需求，您可以讀取資料表資料：

* **讀取和複製：**如要在 Cloud Storage 中取得靜態副本，請使用擷取工作或 `EXPORT DATA` 陳述式匯出資料。如果只想讀取資料，請使用 BigQuery Storage API。如要在 BigQuery 中複製資料，請使用複製作業。
* **規模：**BigQuery API 的效率最低，不應用於大量讀取作業。如要每天匯出超過 50 TB 的資料，請使用 `EXPORT DATA` 陳述式或 BigQuery Storage API。
* **傳回第一列資料的時間：**BigQuery API 是傳回第一列資料最快的方法，但只應用於讀取少量資料。BigQuery Storage API 傳回第一列資料的速度較慢，但輸送量高出許多。匯出和複製作業必須完成，才能讀取任何資料列，因此這類工作的首列時間可能需要幾分鐘。

## 刪除

刪除資料表後，資料至少會在[時間回溯期](https://docs.cloud.google.com/bigquery/docs/time-travel?hl=zh-tw)內保留。
之後，系統會在[Google Cloud 刪除時間軸](https://docs.cloud.google.com/docs/security/deletion?hl=zh-tw#deletion_timeline)內，從磁碟清除資料。
部分刪除作業 (例如 [`DROP COLUMN` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#alter_table_drop_column_statement)) 僅限中繼資料作業。在這種情況下，下次修改受影響的資料列時，系統就會釋出儲存空間。如果您未修改資料表，系統無法保證何時會釋出儲存空間。
詳情請參閱 [Google Cloud的資料刪除](https://docs.cloud.google.com/docs/security/deletion?hl=zh-tw)。

## 後續步驟

* 瞭解如何[使用表格](https://docs.cloud.google.com/bigquery/docs/tables-intro?hl=zh-tw)。
* 瞭解如何[最佳化儲存空間](https://docs.cloud.google.com/bigquery/docs/best-practices-storage?hl=zh-tw)。
* 瞭解如何[在 BigQuery 中查詢資料](https://docs.cloud.google.com/bigquery/docs/query-overview?hl=zh-tw)。
* 瞭解[資料安全與管理](https://docs.cloud.google.com/bigquery/docs/data-governance?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-04-30 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-04-30 (世界標準時間)。"],[],[]]