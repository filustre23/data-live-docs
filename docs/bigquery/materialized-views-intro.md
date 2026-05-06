Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 具體化檢視表簡介

具體化檢視表是預先計算的檢視表，會定期儲存 SQL 查詢的結果。在某些情況下，具體化檢視區會減少每項查詢掃描的資料量，進而縮短總處理時間並降低相關費用。您可以像查詢其他資料資源一樣查詢具體化檢視表。

以下用途可突顯具體化檢視區塊的價值：

* **預先處理資料**。準備匯總、篩選器、聯結和叢集，提高查詢效能。
* **資訊主頁加速**。為 Looker 等商業智慧工具提供支援，這些工具經常查詢相同的匯總指標，例如每日活躍使用者。
* **對大型串流進行即時分析**。可針對接收高速串流資料的表格，提供更快速的回應。
* **成本管理**。減少對大型資料集重複執行昂貴查詢的成本。

**注意：** 使用以特定 BigQuery 版本建立的預留項目時，無法使用具體化檢視表。如要進一步瞭解各版本啟用的功能，請參閱「[BigQuery 版本簡介](https://docs.cloud.google.com/bigquery/docs/editions-intro?hl=zh-tw)」。

具體化檢視區塊的主要特徵包括：

* **免維護**。基礎資料表變更時，具體化檢視表會在背景預先計算。基礎資料表中的任何增量資料變更都會自動新增至具體化檢視區塊，使用者不需採取任何動作。
* **提供最新資料**：具體化檢視表會傳回最新資料。如果底層資料表的變更可能會導致具體化檢視失效，系統會直接從底層資料表讀取資料。如果基本資料表的變更不會使具體化檢視失效，系統就會從具體化檢視讀取其餘資料，並只從基本資料表讀取變更。
* **智慧調整**。如果查詢基本資料表的任何部分可透過查詢具體化檢視表來解決，BigQuery 就會重新導向查詢，改用具體化檢視表，以提升效能和效率。如要瞭解智慧微調功能如何以及何時能改善查詢，請參閱「[使用具體化檢視區塊](https://docs.cloud.google.com/bigquery/docs/materialized-views-use?hl=zh-tw#smart_tuning)」。

### 漸進式和非漸進式具體化檢視表

具體化檢視區塊基本上有兩種類型：

* *增量具體化檢視表*僅支援部分功能。如要進一步瞭解系統支援的具體化檢視表 SQL 語法，請參閱「[建立具體化檢視表](https://docs.cloud.google.com/bigquery/docs/materialized-views-create?hl=zh-tw)」。只有增量具體化檢視畫面可以運用[智慧微調](https://docs.cloud.google.com/bigquery/docs/materialized-views-use?hl=zh-tw#smart_tuning)。
* *非遞增函式*支援大多數遞增具體化檢視表不支援的語法。

建立具體化檢視表時，BigQuery 預設只允許您根據*增量*查詢建立檢視表。如要建立非累加檢視區塊，您可以在具體化檢視區塊的定義中指定 `allow_non_incremental_definition = true`。

要使用哪種具體化檢視區塊，取決於您的情況。下表比較遞增和非遞增具體化檢視區塊的功能：

| **類別** | **增量** | **非增量** |
| --- | --- | --- |
| 支援查詢 | [受限](https://docs.cloud.google.com/bigquery/docs/materialized-views-create?hl=zh-tw#aggregate_requirements) | [最多查詢](https://docs.cloud.google.com/bigquery/docs/materialized-views-create?hl=zh-tw#create-non-inc) |
| 維護費用 | 可降低常用查詢的成本。如要瞭解具體化檢視區塊的更新方式，請參閱[增量更新](https://docs.cloud.google.com/bigquery/docs/materialized-views-use?hl=zh-tw#incremental_updates)。 | 每次重新整理都會執行完整查詢。 |
| 智慧微調支援 | 支援大部分的瀏覽次數查詢。 | 否 |
| 一律顯示最新結果 | 支援。即使基礎資料表在上次重新整理後有所變更，增量檢視區塊仍會傳回最新的查詢結果。 | 否 |

## 授權具體化檢視表

您可以建立授權具體化檢視表，將來源資料集中的部分資料分享至次要資料集的檢視表。接著，您可以將這個檢視畫面分享給特定使用者和群組 (主體)，讓他們查看您分享的資料。主體可以查詢您在檢視區塊中提供的資料，但無法直接存取來源資料集。

授權 view 和授權 materialized view 的授權方式相同。詳情請參閱「[授權檢視表](https://docs.cloud.google.com/bigquery/docs/authorized-views?hl=zh-tw)」。

## 與其他 BigQuery 功能互動

下列 BigQuery 功能可與具體化檢視區塊透明地搭配運作：

* **[查詢計畫說明](https://docs.cloud.google.com/bigquery/docs/query-plan-explanation?hl=zh-tw)：**查詢計畫會反映掃描的具體化檢視表 (如有)，並顯示從具體化檢視表和基本資料表讀取的位元組總數。
* **[查詢快取](https://docs.cloud.google.com/bigquery/docs/cached-results?hl=zh-tw)：**BigQuery 使用具體化檢視表重新編寫的查詢結果，可根據一般限制條件進行快取 (使用確定性函式、不串流至基本資料表等)。
* **[費用限制](https://docs.cloud.google.com/bigquery/docs/best-practices-costs?hl=zh-tw#restrict-bytes-billed)：**
  如果您已設定計費位元組數上限，且查詢讀取的位元組數超過上限，查詢就會失敗，不會產生費用，無論查詢是使用具體化檢視區塊、基本資料表或兩者皆是。
* **[使用模擬測試估算費用](https://docs.cloud.google.com/bigquery/docs/best-practices-costs?hl=zh-tw#perform-dry-run)：**
  模擬測試會使用可用的具體化檢視區塊重複查詢重寫邏輯，並提供費用估算值。您可以使用這項功能測試特定查詢是否使用任何具體化檢視區塊。
* **[跨區域資料複製](https://docs.cloud.google.com/bigquery/docs/data-replication?hl=zh-tw)：**
  您可以在已啟用跨區域複製功能的 BigQuery 資料表上建立具體化檢視區塊，但只能在主要區域建立。如果使用次要區域，您可能會看到下列錯誤訊息：
  `The dataset replica of the cross region dataset {PROJECT}:{DATASET} in region {REGION} is read-only because it's not the primary replica.`

### 已啟用變更資料擷取的資料表

您可以透過啟用[變更資料擷取](https://docs.cloud.google.com/bigquery/docs/change-data-capture?hl=zh-tw) (CDC) 功能的資料表建立具體化檢視區塊。這些具體化檢視表的功能與 BigQuery 資料表的具體化檢視表類似，包括自動重新整理的優點。具體化檢視區塊無法執行[執行階段合併查詢](https://docs.cloud.google.com/bigquery/docs/change-data-capture?hl=zh-tw#query-max-staleness)，因此必須設定足夠的 `max_staleness`，才能避免執行階段合併作業。詳情請參閱「[Limitations of materialized views over 資料表 with active 變更資料擷取](#cdc_limits)」。

### 啟用 BigLake 中繼資料快取的資料表

[已啟用 BigLake 中繼資料快取](https://docs.cloud.google.com/bigquery/docs/biglake-intro?hl=zh-tw#metadata_caching_for_performance)的資料表具體化檢視區塊，可參照儲存在 Cloud Storage 和 Amazon Simple Storage Service (Amazon S3) 的結構化資料。這些具體化檢視表的功能與 BigQuery 管理的儲存空間資料表具體化檢視表類似，包括自動重新整理和智慧微調等優點。其他優點包括預先匯總、預先篩選及預先聯結儲存在 BigQuery 外部的資料。BigLake 資料表的具體化檢視區塊會儲存在 [BigQuery 代管儲存空間](https://docs.cloud.google.com/bigquery/docs/storage_overview?hl=zh-tw)中，並具備該儲存空間的所有特性。

**注意：** 重新整理具有中繼資料快取的 BigLake 資料表上的具體化檢視區時，具體化檢視區的快取資料會包含外部資料表的所有更新，直到最近一次建立中繼資料快取為止。

在 Amazon S3 BigLake 資料表上建立具體化檢視表時，具體化檢視表中的資料無法與 BigQuery 資料聯結。如要讓 materialized view 中的 Amazon S3 資料可供聯結，請建立 materialized view 的[副本](https://docs.cloud.google.com/bigquery/docs/load-data-using-cross-cloud-transfer?hl=zh-tw#materialized_view_replicas)。您只能在[已授權的具體化檢視表](https://docs.cloud.google.com/bigquery/docs/authorized-views?hl=zh-tw)上建立副本。

## 限制

* 可能適用基本表格參照限制和其他限制。如要進一步瞭解具體化檢視限制，請參閱「[配額和限制](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#materialized_view_limits)」。
* 您無法使用 `COPY`、`EXPORT`、`LOAD`、`WRITE` 等作業或資料操縱語言 (DML) 陳述式，直接更新或操縱具體化檢視表的資料。
* 建立 materialized view 後，就無法更新 materialized view SQL。
* 具體化檢視區塊必須與其基本資料表位於同一個機構，如果專案不屬於任何機構，則必須位於同一個專案。
* 具體化檢視表使用受限的 SQL 語法和一組有限的匯總函式。詳情請參閱「[支援的具體化檢視區塊](https://docs.cloud.google.com/bigquery/docs/materialized-views?hl=zh-tw#supported-mvs)」。
* 具體化檢視表無法巢狀內嵌在其他具體化檢視表中。
* 實體化檢視表無法查詢外部或萬用字元資料表、邏輯檢視表1或快照。
* 具體化檢視表不支援[系統變數](https://docs.cloud.google.com/bigquery/docs/reference/system-variables?hl=zh-tw)，包括 `@@session_id` 系統變數。
* `max_staleness` 選項的值必須介於 30 分鐘至 3 天之間 (含)。
* 實體化檢視區塊僅支援 GoogleSQL 方言。
* 您可以為具體化檢視設定說明，但無法為具體化檢視中的個別資料欄設定說明。
* 如果刪除基礎資料表時未先刪除具體化檢視，查詢和重新整理具體化檢視就會失敗。如果重新建立基礎資料表，也必須重新建立具體化檢視區塊。
* 只有非遞增式具體化檢視表可以有 [Spanner 外部資料集基本資料表](https://docs.cloud.google.com/bigquery/docs/spanner-external-datasets?hl=zh-tw)。如果非遞增式具體化檢視表的上次重新整理時間不在 `max_staleness` 間隔內，查詢就會讀取基礎 Spanner 外部資料集資料表。如要進一步瞭解 Spanner 外部資料集資料表，請參閱「[透過 Spanner 外部資料集建立具體化檢視區塊](https://docs.cloud.google.com/bigquery/docs/materialized-views-create?hl=zh-tw#spanner)」。
* 如果查詢是針對參照 [Spanner 外部資料集資料表](https://docs.cloud.google.com/bigquery/docs/spanner-external-datasets?hl=zh-tw)的非遞增具體化檢視區塊執行，系統不會快取查詢結果。
* 實體化檢視區塊無法繼承或明確定義[參數化資料類型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#parameterized_data_types) (例如 `STRING(n)`)，因為參數化資料類型僅適用於基本資料表資料欄和指令碼變數。

1邏輯檢視畫面參照支援功能目前為[預先發布版](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages)。詳情請參閱[參考邏輯檢視區塊](https://docs.cloud.google.com/bigquery/docs/materialized-views-create?hl=zh-tw#reference_logical_views)。

### 透過已啟用 CDC 的資料表使用具體化檢視表的限制

如果具體化檢視區塊使用主動式變更資料擷取基本資料表，則有下列限制：

* 如果 materialized view 有啟用[變更資料擷取](https://docs.cloud.google.com/bigquery/docs/change-data-capture?hl=zh-tw)功能的基本資料表，則查詢中不能同時參照該資料表和 materialized view。
* 如果您在啟用變更資料擷取的資料表上建立具體化檢視，具體化檢視就無法執行基礎 CDC 資料表的執行階段合併工作。將具體化檢視的 [`max_staleness` 值](https://docs.cloud.google.com/bigquery/docs/materialized-views-create?hl=zh-tw#max_staleness)設為至少是基本資料表的 `max_staleness` 值的兩倍。如果基礎 CDC 資料表的目前版本比具體化檢視 `max_staleness` 舊，針對具體化檢視的查詢就會失敗。
* 如果資料表正在擷取變更資料，系統就不支援對該資料表建立的具體化檢視表進行智慧調整。

### BigLake 資料表的具體化檢視表限制

* 系統不支援具體化檢視表的分區功能。基礎資料表可以使用 Hive 分區，但具體化檢視儲存空間無法在 BigLake 資料表中分區。也就是說，如果刪除基礎資料表中的任何內容，materialized view 就會全面重新整理。詳情請參閱「[增量更新](https://docs.cloud.google.com/bigquery/docs/materialized-views-use?hl=zh-tw#incremental_updates)」。
* 具體化檢視區塊的 [`--max_staleness` 選項](https://docs.cloud.google.com/bigquery/docs/materialized-views-create?hl=zh-tw#max_staleness)值必須大於 BigLake 基本資料表的值。
* 單一具體化檢視定義不支援 BigQuery 代管資料表與 BigLake 資料表之間的聯結。
* BigQuery BI Engine 不支援加速處理 BigLake 資料表上的具體化檢視區塊。

## 具體化檢視表定價

具體化檢視表的費用與下列項目相關：

* 查詢具體化檢視表。
* 維護具體化檢視表，例如重新整理具體化檢視表。自動重新整理的費用會計入檢視區塊所在的專案。手動重新整理的費用會計入執行手動重新整理工作的專案。如要進一步瞭解如何控管維護費用，請參閱「[重新整理作業維護](https://docs.cloud.google.com/bigquery/docs/materialized-views-manage?hl=zh-tw#refresh)」。
* 儲存具體化檢視表。

| 元件 | 以量計價 | 以容量為基礎的定價方式 |
| --- | --- | --- |
| 查詢 | 具體化檢視區塊處理的位元組數，以及基本資料表的任何必要部分。1 | 查詢期間會消耗運算單元。 |
| 維護 | 重新整理期間處理的位元組數。 | 系統會在重新整理期間消耗運算單元。 |
| 儲存空間 | 儲存在具體化檢視表中的位元組數。 | 儲存在具體化檢視表中的位元組數。 |

1 盡可能只讀取上次重新整理檢視區塊後發生的變更。詳情請參閱「[增量更新](https://docs.cloud.google.com/bigquery/docs/materialized-views-use?hl=zh-tw#incremental_updates)」。

### 儲存空間費用詳細資料

對於 materialized view 中的 `AVG`、`ARRAY_AGG` 和 `APPROX_COUNT_DISTINCT` 匯總值，系統不會直接儲存最終值。BigQuery 會在內部將具體化檢視區塊儲存為中介*草圖*，並使用該草圖產生最終值。

舉例來說，請參考以下指令建立的具體化檢視區塊：

```
CREATE MATERIALIZED VIEW project-id.my_dataset.my_mv_table AS
SELECT date, AVG(net_paid) AS avg_paid
FROM project-id.my_dataset.my_base_table
GROUP BY date
```

雖然 `avg_paid` 欄會向使用者顯示為 `NUMERIC` 或 `FLOAT64`，但內部會儲存為 `BYTES`，內容則是專有格式的中間草稿。如要瞭解[資料量的計算方式](https://cloud.google.com/bigquery/pricing?hl=zh-tw#data)，請將該欄視為 `BYTES`。

## 後續步驟

* [邏輯檢視區塊和具體化檢視區塊總覽](https://docs.cloud.google.com/bigquery/docs/logical-materialized-view-overview?hl=zh-tw)
* [建立具體化檢視表](https://docs.cloud.google.com/bigquery/docs/materialized-views-create?hl=zh-tw)
* [使用具體化檢視表](https://docs.cloud.google.com/bigquery/docs/materialized-views-use?hl=zh-tw)
* [管理具體化檢視表](https://docs.cloud.google.com/bigquery/docs/materialized-views-manage?hl=zh-tw)




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-06 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-06 (世界標準時間)。"],[],[]]