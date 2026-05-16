Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 資料表簡介

BigQuery 資料表含有以資料列分組的個人記錄，每筆記錄是由資料欄所組成 (也稱為「欄位」)。

每份資料表都按包含資料欄名稱、資料類型和其他資訊的「結構定義」定義。建立資料表時，您可以指定資料表的結構定義，或者您也可以建立一份沒有結構定義的資料表，並在首次填入資料的查詢或載入工作中宣告結構定義。

使用 GoogleSQL 時，請採用 `projectname.datasetname.tablename` 格式完整指定資料表名稱；使用 bq 指令列工具時，請採用 `projectname:datasetname.tablename` 格式完整指定資料表名稱。

## 資料表類型

以下各節說明 BigQuery 支援的資料表類型。

* [標準 BigQuery 資料表](#standard-tables)：儲存在 BigQuery 儲存空間中的結構化資料。
* [外部資料表](#external_tables)：參照儲存在 BigQuery 外部資料的資料表。
* [檢視區塊](#views)：使用 SQL 查詢建立的邏輯資料表。

### 標準 BigQuery 資料表

標準 BigQuery 資料表包含結構化資料，並以直欄格式儲存在 BigQuery 儲存空間中。您也可以使用符合 [`ObjectRef`](https://docs.cloud.google.com/bigquery/docs/work-with-objectref?hl=zh-tw) 格式的 struct 資料欄，在標準資料表中儲存非結構化資料的參照。如要進一步瞭解如何使用 `ObjectRef` 值，請參閱「[在資料表結構定義中指定 ObjectRef 欄](https://docs.cloud.google.com/bigquery/docs/objectref-columns?hl=zh-tw)」。

BigQuery 支援下列資料表類型：

* 資料表，其中包含結構定義，且結構定義中的每個資料欄都有資料類型。

  如要瞭解如何建立資料表，請參閱「[建立資料表](https://docs.cloud.google.com/bigquery/docs/tables?hl=zh-tw#create-table)」。
* [資料表副本](https://docs.cloud.google.com/bigquery/docs/table-clones-intro?hl=zh-tw)：BigQuery 資料表的輕量級可寫入副本。BigQuery 只會儲存資料表副本與基礎資料表之間的差異。

  如要瞭解如何建立資料表副本，請參閱「[建立資料表副本](https://docs.cloud.google.com/bigquery/docs/table-clones-create?hl=zh-tw)」。
* [資料表快照](https://docs.cloud.google.com/bigquery/docs/table-snapshots-intro?hl=zh-tw)：資料表在特定時間點的副本。資料表快照為唯讀，但您可以從資料表快照還原資料表。BigQuery 會儲存快照與基礎資料表之間不同的位元組，因此資料表快照的儲存空間用量通常會比資料表的完整副本少。

  如要瞭解如何建立資料表快照，請參閱「[建立資料表快照](https://docs.cloud.google.com/bigquery/docs/table-snapshots-create?hl=zh-tw)」。

### 外部資料表

外部資料表儲存在 BigQuery 儲存空間外部，並參照儲存在 BigQuery 外部的資料。詳情請參閱[外部資料來源簡介](https://docs.cloud.google.com/bigquery/docs/external-data-sources?hl=zh-tw)。
外部資料表包含下列類型：

* [BigLake 資料表](https://docs.cloud.google.com/bigquery/docs/biglake-intro?hl=zh-tw)，參照儲存在資料儲存庫 (例如 Cloud Storage、Amazon Simple Storage Service (Amazon S3) 和 Azure Blob 儲存體) 中的結構化資料。您可以使用這些資料表，在資料表層級強制執行精細的安全性。

  如要瞭解如何建立 BigLake 資料表，請參閱下列主題：

  + [Cloud Storage](https://docs.cloud.google.com/bigquery/docs/query-cloud-storage-using-biglake?hl=zh-tw)
  + [Amazon S3](https://docs.cloud.google.com/bigquery/docs/omni-aws-create-external-table?hl=zh-tw)
  + [Blob Storage](https://docs.cloud.google.com/bigquery/docs/omni-azure-create-external-table?hl=zh-tw)
* [物件資料表](https://docs.cloud.google.com/bigquery/docs/object-table-introduction?hl=zh-tw)：參照儲存在 Cloud Storage 等資料儲存庫中的非結構化資料。

  如要瞭解如何建立物件資料表，請參閱「[建立物件資料表](https://docs.cloud.google.com/bigquery/docs/object-tables?hl=zh-tw)」一文。
* [非 BigLake 外部資料表](https://docs.cloud.google.com/bigquery/docs/external-tables?hl=zh-tw)：參照儲存在資料儲存區 (例如 Cloud Storage、Google 雲端硬碟和 Bigtable) 中的結構化資料。與 BigLake 資料表不同，您無法在這些資料表強制執行資料表層級的精細安全防護機制。

  如要瞭解如何建立非 BigLake 外部資料表，請參閱下列主題：

  + [Cloud Storage](https://docs.cloud.google.com/bigquery/docs/external-data-cloud-storage?hl=zh-tw)
  + [Google 雲端硬碟](https://docs.cloud.google.com/bigquery/docs/external-data-drive?hl=zh-tw)
  + [Bigtable](https://docs.cloud.google.com/bigquery/docs/external-data-bigtable?hl=zh-tw)

### 瀏覽次數

檢視表是使用 SQL 查詢定義的邏輯資料表。包括下列類型：

* [檢視表](https://docs.cloud.google.com/bigquery/docs/views-intro?hl=zh-tw)：使用 SQL 查詢定義的邏輯資料表。這些查詢會定義每次查詢檢視表時執行的檢視表。

  如要瞭解如何建立檢視表，請參閱「[建立檢視表](https://docs.cloud.google.com/bigquery/docs/views?hl=zh-tw)」。
* [具體化檢視區塊](https://docs.cloud.google.com/bigquery/docs/materialized-views-intro?hl=zh-tw)：預先計算的檢視區塊，會定期快取檢視區塊查詢的結果。快取結果會儲存在 BigQuery 儲存空間中。

  如要瞭解如何建立具體化檢視表，請參閱「[建立具體化檢視表](https://docs.cloud.google.com/bigquery/docs/materialized-views-create?hl=zh-tw)」。

## 資料表限制

BigQuery 資料表有以下限制：

* 各資料集中的資料表名稱不得重複。
* 匯出 BigQuery 資料表資料時，系統僅支援以 Cloud Storage 做為目的地。
* 如使用 API 呼叫，當資料集中的資料表數接近 50,000 個時，列舉效能會下降。
* Google Cloud 控制台最多可為每個資料集顯示 50,000 個資料表。

如要瞭解 BigQuery 外部資料表的限制，請參閱下列主題：

* [BigLake 資料表](https://docs.cloud.google.com/bigquery/docs/biglake-intro?hl=zh-tw#limitations)
* [物件資料表](https://docs.cloud.google.com/bigquery/docs/object-table-introduction?hl=zh-tw#limitations)
* [外部資料表](https://docs.cloud.google.com/bigquery/docs/external-tables?hl=zh-tw#limitations)

## 資料表配額

配額和限制適用於您可對資料表執行的各種工作類型，包括下列配額：

* [將資料載入資料表](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#load_jobs) (載入工作)
* [從資料表匯出資料](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#export_jobs) (擷取工作)
* [查詢資料表資料](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#query_jobs) (查詢工作)
* [複製資料表](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#copy_jobs) (複製工作)

如要進一步瞭解所有配額和限制，請參閱[配額與限制](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)一文。

如要排解資料表的配額錯誤，請參閱 [BigQuery 疑難排解頁面](https://docs.cloud.google.com/bigquery/docs/troubleshoot-quotas?hl=zh-tw)。

下列配額錯誤專屬於資料表：

* [資料表匯入或查詢附加配額錯誤](https://docs.cloud.google.com/bigquery/docs/troubleshoot-quotas?hl=zh-tw#ts-table-import-quota)
* [針對資料表待處理的 DML 陳述式過多](https://docs.cloud.google.com/bigquery/docs/troubleshoot-quotas?hl=zh-tw#ts-too-many-dml-statements-against-table-quota)

## 資料表價格

您在 BigQuery 中建立及使用資料表時，系統會根據儲存在資料表和分區中的資料量，以及您對資料表資料執行的查詢量計算費用：

* 如需儲存空間定價的相關資訊，請參閱[儲存空間定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#storage)一節。
* 如需查詢定價的相關資訊，請參閱[查詢的定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#analysis_pricing_models)一節。

許多資料表作業都是免費的，包括載入、複製及匯出資料。
雖然這些作業都是免費的，但仍受限於 BigQuery 的[配額與限制](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)。如需所有免費作業的相關資訊，請參閱定價頁面上的「[免費作業](https://cloud.google.com/bigquery/pricing?hl=zh-tw#free)」一節。

## 資料表安全性

如要控管 BigQuery 資料表的存取權，請參閱「[使用 IAM 控管資源存取權](https://docs.cloud.google.com/bigquery/docs/control-access-to-resources-iam?hl=zh-tw)」。

## 後續步驟

* 瞭解如何[建立及使用資料表](https://docs.cloud.google.com/bigquery/docs/tables?hl=zh-tw)。
* 瞭解如何[管理表格](https://docs.cloud.google.com/bigquery/docs/managing-tables?hl=zh-tw)。
* 瞭解如何[修改資料表結構定義](https://docs.cloud.google.com/bigquery/docs/managing-table-schemas?hl=zh-tw)。
* 瞭解如何[使用資料表資料](https://docs.cloud.google.com/bigquery/docs/managing-table-data?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-16 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-16 (世界標準時間)。"],[],[]]