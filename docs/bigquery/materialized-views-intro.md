Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 具體化檢視表簡介

BigQuery 具體化檢視表是預先運算的資料表，可針對經常執行的可預測查詢，提升查詢效能並降低執行成本。具體化檢視表會定期儲存查詢結果，因此在重複查詢具有可預測匯總模式的大型資料集時，可解決查詢延遲和掃描成本過高的問題。透過自動合併預先計算的資料和基本資料表中的近期變更，具體化檢視畫面可確保查詢結果為最新狀態，且不需要手動資料管道。

這份文件適用於設計高效能分析管道的資料工程師、資料庫管理員和商業智慧 (BI) 開發人員。如要順利導入具體化檢視表，您應熟悉 BigQuery 資料集結構、GoogleSQL 匯總函式和查詢費用結構。

## 具體化檢視表的好處

以下用途可突顯具體化檢視區塊的價值：

* **預先處理資料**：準備匯總、篩選器、聯結和叢集，提高查詢效能。
* **資訊主頁加速**。為 Looker 等商業智慧工具提供支援，這些工具經常查詢相同的匯總指標，例如每日活躍使用者。
* **即時分析大型串流**。可針對接收高速串流資料的表格，提供更快速的回應。
* **成本管理**。減少對大型資料集進行重複且昂貴查詢的成本。

## 主要特性

具體化檢視區塊的主要特徵包括：

* **免維護**。當基礎資料表變更時，BigQuery 會在背景預先計算具體化檢視表。BigQuery 會自動將基礎資料表中的增量資料變更新增至具體化檢視區塊，不需要使用者採取任何動作。
* **提供最新資料**。具體化檢視表會傳回最新資料。如果基礎資料表的變更可能會導致具體化檢視區失效，BigQuery 就會直接從基礎資料表讀取資料。如果基礎資料表的變更不會使具體化檢視區失效，BigQuery 會從具體化檢視區讀取其餘資料，並只從基礎資料表讀取變更。

  下圖顯示用於合併即時資料變更的邏輯：
* **智慧微調**。如果查詢基礎資料表的任何部分可透過查詢 materialized view 解決，BigQuery 就會重新導向查詢，使用 materialized view 來提升效能和效率。如要瞭解智慧微調功能如何及何時能改善查詢，請參閱「[使用具體化檢視區塊](https://docs.cloud.google.com/bigquery/docs/materialized-views-use?hl=zh-tw#smart_tuning)」。

  下圖顯示智慧微調的查詢重新轉送工作流程：

## 具體化檢視表類型

具體化檢視區塊基本上有兩種：

* *遞增具體化檢視區塊*僅支援部分功能。如要進一步瞭解 materialized view 支援的 SQL 語法，請參閱「[建立 materialized view](https://docs.cloud.google.com/bigquery/docs/materialized-views-create?hl=zh-tw)」。只有增量具體化檢視畫面可以運用[智慧微調](https://docs.cloud.google.com/bigquery/docs/materialized-views-use?hl=zh-tw#smart_tuning)。
* *非累加式具體化檢視區塊*支援大多數累加式具體化檢視區塊不支援的語法。

建立具體化檢視表時，BigQuery 預設只允許您根據*增量*查詢建立檢視表。如要建立非遞增檢視區塊，您可以在具體化檢視區塊的定義中指定 `allow_non_incremental_definition = true`。

要使用哪種具體化檢視區塊，取決於您的情況。下表比較了遞增和非遞增具體化檢視區塊的功能：

| **類別** | **增量** | **非增量** |
| --- | --- | --- |
| 支援查詢 | [受限](https://docs.cloud.google.com/bigquery/docs/materialized-views-create?hl=zh-tw#aggregate_requirements) | [最多查詢](https://docs.cloud.google.com/bigquery/docs/materialized-views-create?hl=zh-tw#create-non-inc) |
| 維護費用 | 可降低常用查詢的成本。如要瞭解具體化檢視區塊的更新方式，請參閱[增量更新](https://docs.cloud.google.com/bigquery/docs/materialized-views-use?hl=zh-tw#incremental_updates)。 | 每次重新整理都會執行完整查詢。 |
| 智慧微調支援 | 支援大多數檢視查詢。 | 否 |
| 一律顯示最新結果 | 支援。即使基礎資料表在上次重新整理後有所變更，遞增檢視區塊仍會傳回最新的查詢結果。 | 否 |

## 授權具體化檢視表

您可以建立授權具體化 view，將來源資料集中的部分資料分享至次要資料集中的 view。然後與特定使用者和群組 (主體) 分享這個檢視畫面。主體可以查詢您在檢視畫面中提供的資料，但無法直接存取來源資料集。

授權 view 和授權 materialized view 的授權方式相同。詳情請參閱「[已授權檢視畫面](https://docs.cloud.google.com/bigquery/docs/authorized-views?hl=zh-tw)」。

## 與其他 BigQuery 功能互動

下列 BigQuery 功能可與具體化檢視表透明地搭配運作：

* **[查詢計畫說明](https://docs.cloud.google.com/bigquery/docs/query-plan-explanation?hl=zh-tw)。**查詢計畫會顯示掃描的具體化檢視表 (如有)，以及從具體化檢視表和基本資料表讀取的位元組總數。
* **[查詢快取](https://docs.cloud.google.com/bigquery/docs/cached-results?hl=zh-tw)。**BigQuery 使用具體化檢視表重新編寫查詢時，查詢結果可能會受到一般限制 (使用確定性函式、不串流至基本資料表等)，並快取結果。
* **[費用限制](https://docs.cloud.google.com/bigquery/docs/best-practices-costs?hl=zh-tw#restrict-bytes-billed)。**
  如果您指定計費位元組數上限，且查詢讀取的資料超出該上限，則無論查詢使用具體化檢視區塊、基本資料表或兩者，查詢都會失敗，不會產生費用。
* **[使用模擬測試估算費用](https://docs.cloud.google.com/bigquery/docs/best-practices-costs?hl=zh-tw#perform-dry-run)。**
  模擬測試會使用可用的具體化檢視表，重複執行查詢重寫邏輯，並提供費用預估值。您可以使用這項功能測試特定查詢是否使用任何具體化檢視區塊。
* **[跨區域資料複製](https://docs.cloud.google.com/bigquery/docs/data-replication?hl=zh-tw)。**
  您可以在啟用跨區域複製功能的 BigQuery 資料表上建立具體化檢視區塊，但只能在主要區域建立。如果使用次要區域，可能會看到下列錯誤訊息：
  `The dataset replica of the cross region dataset {PROJECT}:{DATASET} in region {REGION} is read-only because it's not the primary replica.`

除了這些功能，您也可以針對具有特定功能的資料表建立具體化檢視區塊，詳情請參閱下列各節。

### 已啟用變更資料擷取的資料表

您可以針對啟用[變更資料擷取](https://docs.cloud.google.com/bigquery/docs/change-data-capture?hl=zh-tw) (CDC) 功能的資料表建立具體化檢視區塊，持續擷取資料庫或資料表的變更。這些具體化檢視區塊的功能與 BigQuery 資料表的具體化檢視區塊類似，包括自動重新整理的優點。具體化檢視表無法執行[執行階段合併查詢](https://docs.cloud.google.com/bigquery/docs/change-data-capture?hl=zh-tw#query-max-staleness)，因此您必須使用足夠的 `max_staleness` 設定具體化檢視表，避免執行階段合併作業。詳情請參閱「[Limitations of materialized views over 資料表 with active 變更資料擷取](#cdc_limits)」。

### 啟用 BigLake 中繼資料快取的資料表

[已啟用 BigLake 中繼資料快取功能的資料表](https://docs.cloud.google.com/bigquery/docs/biglake-intro?hl=zh-tw#metadata_caching_for_performance)具體化檢視表可參照儲存在 Cloud Storage 和 Amazon Simple Storage Service (Amazon S3) 中的結構化資料。這些具體化檢視表的功能與 BigQuery 管理的儲存空間資料表具體化檢視表類似，包括自動重新整理和智慧調整等優點。其他優點包括預先匯總、預先篩選及預先聯結儲存在 BigQuery 外部的資料。BigLake 資料表的具體化檢視區塊會儲存在 [BigQuery 代管儲存空間](https://docs.cloud.google.com/bigquery/docs/storage_overview?hl=zh-tw)中，並具備該儲存空間的所有特性。

**注意：** 重新整理 BigLake 資料表 (含已快取的中繼資料) 的具體化檢視區時，具體化檢視區的快取資料會包含外部資料表的所有更新，直到最近一次建立中繼資料快取為止。

在 Amazon S3 BigLake 資料表上建立具體化檢視表時，具體化檢視表中的資料無法與 BigQuery 資料聯結。如要讓 materialized view 中的 Amazon S3 資料可供聯結，請建立 materialized view 的[副本](https://docs.cloud.google.com/bigquery/docs/load-data-using-cross-cloud-transfer?hl=zh-tw#materialized_view_replicas)。您只能透過[已授權的具體化檢視表](https://docs.cloud.google.com/bigquery/docs/authorized-views?hl=zh-tw)建立具體化檢視表副本。

## 限制

BigQuery 具體化檢視區塊須遵守下列各節所述的功能和作業限制。

### SQL 和語法限制

* **方言**。僅支援 GoogleSQL 方言。
* **SQL 語法**在這個方塊中輸入查詢。具體化檢視表使用受限的 SQL 語法和一組有限的匯總函式。詳情請參閱「[具體化檢視區塊查詢支援](https://docs.cloud.google.com/bigquery/docs/materialized-views-create?hl=zh-tw#supported-mvs)」。
* **系統變數**。具體化檢視區塊不支援[系統變數](https://docs.cloud.google.com/bigquery/docs/reference/system-variables?hl=zh-tw)，例如 `@@session_id` 系統變數。
* **參數化資料類型**。實體化檢視區塊無法繼承或明確定義[參數化資料型別](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#parameterized_data_types)，例如 `STRING(n)`，因為參數化資料型別僅支援基礎資料表欄和指令碼變數。
* **資料欄說明**。您可以為具體化檢視區塊設定說明，但無法為具體化檢視區塊中的個別資料欄設定說明。
* **查詢修改**。建立 materialized view 後，您就無法更新查詢。
* **資料修改**。您無法使用 `COPY`、`EXPORT`、`LOAD`、`WRITE` 或資料操作語言 (DML) 陳述式等作業，直接更新或操作具體化檢視區塊資料。
  **耗用大量 CPU 的運算子**。如果使用大量 CPU 資源的運算子 (例如 `UNPIVOT` 或大量 `UNNEST` 轉換)，可能會導致隨選計費的重新整理作業失敗。如要解決這個問題，您可以改用以容量為準的計價方式，在建立檢視區塊前將轉換後的資料具體化至基礎資料表，或是使用[排定查詢](https://docs.cloud.google.com/bigquery/docs/scheduling-queries?hl=zh-tw)。

### 基礎資料表和巢狀結構限制

* **巢狀結構**。您無法在其他具體化檢視表上巢狀建立具體化檢視表。
* **來源類型**。具體化檢視表無法查詢外部資料表 (BigLake 資料表除外)、萬用字元資料表、邏輯檢視區塊1或快照。
* **刪除行為**：如果刪除基礎資料表時未先刪除具體化檢視區塊，查詢和重新整理具體化檢視區塊就會失敗。如果重新建立基礎資料表，也必須重新建立具體化檢視區塊。
* **Spanner 外部資料集**。只有非漸進式具體化檢視區塊可以有 [Spanner 外部資料集基礎資料表](https://docs.cloud.google.com/bigquery/docs/spanner-external-datasets?hl=zh-tw)。如果非增量具體化檢視區塊上次重新整理的時間不在 `max_staleness` 間隔內，查詢就會讀取基礎 Spanner 外部資料集資料表。詳情請參閱「[透過 Spanner 外部資料集建立具體化檢視區塊](https://docs.cloud.google.com/bigquery/docs/materialized-views-create?hl=zh-tw#spanner)」。
* **使用 Spanner 進行快取**。如果查詢是針對參照 [Spanner 外部資料集資料表](https://docs.cloud.google.com/bigquery/docs/spanner-external-datasets?hl=zh-tw)的非遞增具體化檢視區塊執行，BigQuery 就不會快取查詢結果。

### 適用範圍和區域限制

* **機構邊界**。materialized view 必須與其基礎資料表位於相同專案或機構區塊。
* **過時程度設定**。`max_staleness` 選項的值必須介於 30 分鐘至 3 天之間 (含)。
* **資源查詢**。可能會有基礎資料表參照限制和其他限制。詳情請參閱「[配額與限制](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#materialized_view_limits)」。

1邏輯檢視畫面參照支援功能目前為[預先發布版](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages)。詳情請參閱「[參考邏輯檢視畫面](https://docs.cloud.google.com/bigquery/docs/materialized-views-create?hl=zh-tw#reference_logical_views)」。

### 透過已啟用 CDC 的資料表使用具體化檢視表的限制

如果具體化檢視區塊的變更資料擷取 (CDC) 基準資料表處於啟用狀態，則會有下列限制：

* 如果具體化檢視區有啟用[變更資料擷取](https://docs.cloud.google.com/bigquery/docs/change-data-capture?hl=zh-tw)的基礎資料表，您就無法在同時參照具體化檢視區的查詢中參照該資料表。
* 如果資料表已啟用變更資料擷取功能，您就無法在該資料表上建立具體化檢視區塊，因為具體化檢視區塊無法執行基礎 CDC 資料表的執行階段合併作業。將具體化檢視區塊的 [`max_staleness` 值](https://docs.cloud.google.com/bigquery/docs/materialized-views-create?hl=zh-tw#max_staleness)設為基礎資料表 `max_staleness` 值的至少兩倍。如果基礎 CDC 資料表的目前版本比 materialized view `max_staleness`舊，針對 materialized view 執行的查詢就會失敗。
* 如果資料表已啟用變更資料擷取功能，就無法對具體化檢視區塊使用智慧微調功能。

### BigLake 資料表的具體化檢視表限制

BigLake 資料表的具體化檢視表有下列限制：

* 您無法對具體化檢視區隔分區。基礎資料表可以使用 Apache Hive 分區，但您無法在 BigLake 資料表中分割具體化檢視區塊儲存空間。也就是說，只要刪除基礎資料表中的任何內容，materialized view 就會完整重新整理。詳情請參閱「[增量更新](https://docs.cloud.google.com/bigquery/docs/materialized-views-use?hl=zh-tw#incremental_updates)」。
* 實體化檢視區塊的 [`--max_staleness`
  選項](https://docs.cloud.google.com/bigquery/docs/materialized-views-create?hl=zh-tw#max_staleness)值必須大於 BigLake 基本資料表的值。
* 您無法在單一 materialized view 定義中，對 BigQuery 代管資料表和 BigLake 資料表執行聯結。
* BigQuery BI Engine (快速的記憶體內分析服務) 不支援加速處理 BigLake 表格的具體化檢視表。

## 具體化檢視表定價

**注意：** 使用特定 BigQuery 版本建立的預留項目時，無法使用具體化檢視表。如要進一步瞭解各版本啟用的功能，請參閱「[BigQuery 版本簡介](https://docs.cloud.google.com/bigquery/docs/editions-intro?hl=zh-tw)」一文。

具體化檢視表會產生下列費用：

* 查詢具體化檢視表。
* 維護具體化檢視表，例如重新整理具體化檢視表。自動重新整理的費用會計入檢視畫面所在的專案。手動重新整理的費用會計入執行手動重新整理工作的專案。如要進一步瞭解如何控管維護費用，請參閱「[重新整理作業維護](https://docs.cloud.google.com/bigquery/docs/materialized-views-manage?hl=zh-tw#refresh)」。
* 儲存具體化檢視表。

下表列出具體化檢視表的定價項目：

| 元件 | 以量計價 | 以容量為準的定價 |
| --- | --- | --- |
| 查詢 | 具體化檢視區塊處理的位元組，以及基礎資料表的任何必要部分。1 | 查詢期間會消耗運算單元。 |
| 維護 | 重新整理時處理的位元組數。 | 系統會在重新整理期間消耗運算單元。 |
| 儲存空間 | 儲存在具體化檢視表中的位元組數。 | 儲存在具體化檢視表中的位元組數。 |

1 盡可能只讀取上次重新整理檢視區塊後發生的變更。詳情請參閱「[增量更新](https://docs.cloud.google.com/bigquery/docs/materialized-views-use?hl=zh-tw#incremental_updates)」。

### 儲存費用詳細資料

BigQuery 儲存特定匯總值的方式會影響儲存空間大小的計算方式。對於具體化檢視區塊中的 `AVG`、`ARRAY_AGG` 和 `APPROX_COUNT_DISTINCT` 匯總值，系統不會直接儲存最終值。BigQuery 會在內部將具體化檢視表儲存為中繼*草圖*，用於產生最終值。

舉例來說，請參考以下指令建立的具體化檢視區塊：

```
CREATE MATERIALIZED VIEW project-id.my_dataset.my_mv_table AS
SELECT date, AVG(net_paid) AS avg_paid
FROM project-id.my_dataset.my_base_table
GROUP BY date
```

`avg_paid` 欄會顯示為 `NUMERIC` 或 `FLOAT64`，
但內部會儲存為 `BYTES`，內容則是專有格式的中間草圖。如果是[資料量計算](https://cloud.google.com/bigquery/pricing?hl=zh-tw#data)，系統會將該欄視為 `BYTES`。

## 開始使用工作流程

設定具體化檢視表時，請按照下列工作流程操作：

1. **設計及驗證查詢**。請按照 GoogleSQL 指南，草擬匯總查詢。
2. **建立 materialized view**。使用 Google Cloud 控制台、bq 指令列工具或 BigQuery API 執行 `CREATE MATERIALIZED VIEW` 陳述式。
3. **讓智慧微調功能執行**。BigQuery 會自動將對基礎資料表的查詢重新導向至具體化檢視區塊，因此查詢或應用程式不必重新編寫目標。

如要開始建立，請參閱「[建立具體化檢視區塊](https://docs.cloud.google.com/bigquery/docs/materialized-views-create?hl=zh-tw)」。

## 後續步驟

* [邏輯檢視區塊和具體化檢視區塊總覽](https://docs.cloud.google.com/bigquery/docs/logical-materialized-view-overview?hl=zh-tw)
* [建立具體化檢視表](https://docs.cloud.google.com/bigquery/docs/materialized-views-create?hl=zh-tw)
* [使用具體化檢視表](https://docs.cloud.google.com/bigquery/docs/materialized-views-use?hl=zh-tw)
* [管理具體化檢視表](https://docs.cloud.google.com/bigquery/docs/materialized-views-manage?hl=zh-tw)
* [排解具體化檢視表問題](https://docs.cloud.google.com/bigquery/docs/materialized-views-troubleshoot?hl=zh-tw)




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-10-29 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-10-29 (世界標準時間)。"],[],[]]