Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 分區資料表簡介

分區資料表會劃分為多個區段 (稱為分區)，管理和查詢資料時更加方便。將大型資料表分成許多較小分區，不但可以提高查詢效能，還能降低查詢讀取的位元組數，進一步控管費用。如要將資料表分區，請指定分區資料欄，BigQuery 會使用該資料欄來區隔資料表。

當查詢作業對分區資料欄套用符合的篩選器時，BigQuery 就能掃描符合篩選條件的分區，並略過其餘的分區。這個程序稱為「修剪」。

## 分區的運作方式

在分區資料表中，資料會儲存在實體區塊，每個區塊都包含一個資料分區。每個分區資料表都會維護各種中繼資料，記錄所有修改作業的排序屬性。中繼資料可讓 BigQuery 在執行查詢前，更準確地估算查詢費用。

**注意：** 「[管理資料表資料](https://docs.cloud.google.com/bigquery/docs/managing-table-data?hl=zh-tw)」中的資訊也適用於分區資料表。

## 分區的使用時機

在下列情況下，建議您將資料表分區：

* 您想只掃描資料表的一部分，提高查詢效能。
* 資料表作業超出[標準資料表配額](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#standard_tables)，您可以將資料表作業範圍限定在特定分區資料欄值，以提高[分區資料表配額](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#partitioned_tables)。
* 您想在執行查詢前，先確定查詢費用。BigQuery 會在分區資料表上執行查詢前，提供查詢費用估算值。如要計算查詢費用預估值，請[剪除](https://docs.cloud.google.com/bigquery/docs/querying-partitioned-tables?hl=zh-tw)分區資料表，然後執行查詢模擬測試，估算查詢費用。
* 您需要下列任一分區層級管理功能：
  + [設定分區到期時間](https://docs.cloud.google.com/bigquery/docs/managing-partitioned-tables?hl=zh-tw#partition-expiration)，在指定時間過後自動刪除整個分區。
  + 使用載入工作[將資料寫入特定分區](https://docs.cloud.google.com/bigquery/docs/load-data-partitioned-tables?hl=zh-tw#write-to-partition)，而不影響資料表中的其他分區。
  + [刪除特定分區](https://docs.cloud.google.com/bigquery/docs/managing-partitioned-tables?hl=zh-tw#delete_a_partition)，而不掃描整個資料表。

在下列情況下，建議您[分群](https://docs.cloud.google.com/bigquery/docs/clustered-tables?hl=zh-tw)資料表，而非分區資料表：

* 您需要比分區更精細的控制。
* 查詢通常會使用篩選器或匯總多個資料欄。
* 資料欄或資料欄群組中的值數量基數很大。
* 執行查詢前，不需要嚴格估算費用。
* 分區會導致每個分區的資料量較少 (約少於 10 GB)。建立許多小型分區會增加資料表的中繼資料，並可能影響查詢資料表時的中繼資料存取時間。
* 分區會產生大量分區，超過[分區資料表的限制](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#partitioned_tables)。
* DML 作業經常修改 (例如每隔幾分鐘) 資料表中的大部分分區。

在這種情況下，資料表分群功能可讓您根據使用者定義的排序屬性，將特定資料欄中的資料分群，藉此加快查詢速度。

您也可以結合分群和資料表分區，達到更精細的排序。如要進一步瞭解這個方法，請參閱「[合併分群和分區資料表](#combining_clustered_and_partitioned_tables)」。

## 分區類型

本節說明分區資料表的各種方式。

### 整數範圍分區

您可以根據特定 `INTEGER` 資料欄中的值範圍，將資料表分區。如要建立整數範圍分區資料表，請提供：

* 分區資料欄。
* 範圍分區的起始值 (含)。
* 範圍分區的結束值 (不含)。
* 分區中各範圍的間隔。

舉例來說，假設您建立整數範圍分區，並採用下列規格：

| 引數 | 值 |
| --- | --- |
| 資料欄名稱 | `customer_id` |
| 開始 | 0 |
| 結束 | 100 |
| interval | 10 |

資料表會依 `customer_id` 資料欄分區，間隔範圍為 10。0 到 9 的值會進入一個分區，10 到 19 的值會進入下一個分區，依此類推，直到 99。超出這個範圍的值會進入名為 `__UNPARTITIONED__` 的分區。`customer_id` 為 `NULL` 的任何資料列都會進入名為 `__NULL__` 的分區。

如要瞭解整數範圍分區資料表，請參閱「[建立整數範圍分區資料表](https://docs.cloud.google.com/bigquery/docs/creating-partitioned-tables?hl=zh-tw#create_an_integer-range_partitioned_table)」。

### 按時間單位資料欄分區

您可以依據資料表中的 `DATE`、`TIMESTAMP` 或 `DATETIME` 欄，對資料表進行分區。將資料寫入資料表時，BigQuery 會根據資料欄中的值，自動將資料放入正確的分區。

如果是 `TIMESTAMP` 和 `DATETIME` 資料欄，分區可以按小時、日、月或年劃分。如果是 `DATE` 資料欄，分區可以採用每日、每月或每年的精細程度。分區界線以世界標準時間 (UTC) 為準。

舉例來說，假設您在 `DATETIME` 資料欄上，以每月分區的方式將資料表分區。如果將下列值插入資料表，資料列會寫入下列分區：

| 列值 | 分區 (每月) |
| --- | --- |
| `DATETIME("2019-01-01")` | `201901` |
| `DATETIME("2019-01-15")` | `201901` |
| `DATETIME("2019-04-30")` | `201904` |

此外，系統還會建立兩個特殊分區：

* `__NULL__`：包含分區欄中含有 `NULL` 值的資料列。
* `__UNPARTITIONED__`：包含分區欄值早於 1960-01-01 或晚於 2159-12-31 的資料列。

如要瞭解時間單位資料欄分區資料表，請參閱「[建立時間單位資料欄分區資料表](https://docs.cloud.google.com/bigquery/docs/creating-partitioned-tables?hl=zh-tw#create_a_time-unit_column-partitioned_table)」。

### 擷取時間分區

建立依擷取時間分區的資料表時，BigQuery 會根據擷取資料的時間，自動將資料列指派至分區。您可以選擇按小時、日、月或年設定分區。分區界線以世界標準時間為準。

如果使用較精細的時間精細程度，資料可能會達到每個資料表的分區數量上限，請改用較粗略的精細程度。例如，您可以依月份 (而非日期) 分割，減少分區數量。您也可以[叢集](https://docs.cloud.google.com/bigquery/docs/clustered-tables?hl=zh-tw)分區資料欄，進一步提升效能。

擷取時間分區資料表有名為 `_PARTITIONTIME` 的虛擬資料欄。這個資料欄的值是每個資料列的擷取時間，會截斷至分區邊界 (例如每小時或每日)。舉例來說，假設您建立擷取時間分區資料表，並以小時為單位分區，然後在下列時間傳送資料：

| 擷取時間 | `_PARTITIONTIME` | 分區 (每小時) |
| --- | --- | --- |
| 2021-05-07 17:22:00 | 2021-05-07 17:00:00 | `2021050717` |
| 2021-05-07 17:40:00 | 2021-05-07 17:00:00 | `2021050717` |
| 2021-05-07 18:31:00 | 2021-05-07 18:00:00 | `2021050718` |

由於本範例中的資料表使用每小時分區，因此 `_PARTITIONTIME` 的值會截斷至小時邊界。BigQuery 會使用這個值，判斷資料的正確分區。

您也可以將資料寫入特定分區。例如，您可能需要載入歷來資料或調整時區。您可以使用 0001-01-01 到 9999-12-31 之間的任何有效日期。不過，[DML 陳述式](https://docs.cloud.google.com/bigquery/docs/data-manipulation-language?hl=zh-tw)無法參照 1970-01-01 之前或 2159-12-31 之後的日期。詳情請參閱「[將資料寫入特定分區](https://docs.cloud.google.com/bigquery/docs/load-data-partitioned-tables?hl=zh-tw#write-to-partition)」。

除了使用 `_PARTITIONTIME`，您也可以使用 [`_PARTITIONDATE`](https://docs.cloud.google.com/bigquery/docs/querying-partitioned-tables?hl=zh-tw#query_an_ingestion-time_partitioned_table)。`_PARTITIONDATE` 虛擬資料欄包含與 `_PARTITIONTIME` 虛擬資料欄中的值對應的世界標準時間日期。

### 選取每日、每小時、每月或每年分區

依時間單位資料欄或擷取時間劃分資料表時，您可以選擇分區的精細程度，例如每日、每小時、每月或每年。

* **每日分區**是預設的分區類型。如果資料分散在多個日期，或資料會隨著時間持續增加，則適合採用每日分區。
* 如果資料表含有大量資料，且資料涵蓋的日期範圍較短 (通常時間戳記值少於六個月)，請選擇「每小時分區」。如果選擇每小時分區，請確保分區數量不超過[分區限制](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#partitioned_tables)。
* 如果資料表每天的資料量相對較少，但日期範圍較廣，請選擇**每月或每年分區**。如果工作流程需要頻繁更新或新增涵蓋廣泛日期範圍 (例如超過 500 個日期) 的資料列，也建議使用這個選項。在這些情況下，請使用每月或每年分區，並在分區資料欄上進行分群，以達到最佳效能。詳情請參閱本文的「[合併叢集和分區資料表](#combining_clustered_and_partitioned_tables)」一節。

## 合併分群和分區資料表

您可以將資料表分區與[資料表分群](https://docs.cloud.google.com/bigquery/docs/clustered-tables?hl=zh-tw)結合，進行精細排序，進一步最佳化查詢。

分群資料表包含分群資料欄，可根據使用者定義的排序屬性排序資料。這些分群資料欄中的資料會分類到儲存區塊，區塊大小會根據資料表大小自動調整。執行查詢時，如果依分群資料欄篩選，BigQuery 只會根據分群資料欄掃描相關區塊，而非整個資料表或資料表分區。如果同時使用資料表分區和分群，您會先將資料表資料分割成多個分區，然後再依據分群欄將每個分區中的資料分群。

建立分群和分區資料表時，您可以進行更精細的排序，如下圖所示：

## 分區與 sharding

資料表 sharding 是指使用 `[PREFIX]_YYYYMMDD` 等命名前置字元，將資料儲存在多個資料表中。

建議您使用分區，而非資料表 sharding，因為分區資料表的效能較佳。如果使用資料分割資料表，BigQuery 必須為每個資料表維護結構定義和中繼資料的副本。BigQuery 可能也需要驗證每個查詢資料表的權限。這種做法也會增加查詢負擔，並影響查詢效能。

如果您先前建立了日期分區資料表，可以將其轉換為擷取時間分區資料表。詳情請參閱「[將日期分區資料表轉換為擷取時間分區資料表](https://docs.cloud.google.com/bigquery/docs/creating-partitioned-tables?hl=zh-tw#convert-date-sharded-tables)」。

## 分區裝飾器

分區修飾符可讓您參照資料表中的分區。例如，您可以使用這些修飾符將[資料寫入](https://docs.cloud.google.com/bigquery/docs/load-data-partitioned-tables?hl=zh-tw#write-to-partition)特定分區。

分區修飾符的形式為 `table_name$partition_id`，其中 `partition_id` 區隔的格式取決於分區類型：

| 分區類型 | 格式 | 範例 |
| --- | --- | --- |
| 每小時 | `yyyymmddhh` | `my_table$2021071205` |
| 每天 | `yyyymmdd` | `my_table$20210712` |
| 每月 | `yyyymm` | `my_table$202107` |
| 每年 | `yyyy` | `my_table$2021` |
| 整數範圍 | `range_start` | `my_table$40` |

## 瀏覽分區中的資料

如要瀏覽指定分區中的資料，請使用 [`bq head`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_head) 指令搭配分區修飾符。

舉例來說，下列指令會列出 `2018-02-24` 分區中 `my_dataset.my_table` 前 10 列的所有欄位：

```
    bq head --max_rows=10 'my_dataset.my_table$20180224'
```

## 匯出資料表資料

從分區資料表匯出所有資料的處理程序與從非分區資料表匯出資料相同。詳情請參閱「[匯出資料表資料](https://docs.cloud.google.com/bigquery/docs/exporting-data?hl=zh-tw)」。

如要從個別分區匯出資料，請使用 `bq extract` 指令，並在資料表名稱後方附加分區修飾符。例如，`my_table$20160201`。您也可以將分區名稱附加至資料表名稱，從 [`__NULL__` 和 `__UNPARTITIONED__`](https://docs.cloud.google.com/bigquery/docs/partitioned-tables?hl=zh-tw#date_timestamp_partitioned_tables) 分區匯出資料。例如 `my_table$__NULL__` 或 `my_table$__UNPARTITIONED__`。

## 限制

分區資料表有下列限制：

* 您無法使用舊版 SQL 查詢分區資料表或將查詢結果寫入分區資料表。
* BigQuery 不支援依多個資料欄分區。只能使用一個資料欄來分區資料表。
* 您無法直接將現有的非分區資料表轉換為分區資料表。分區策略是在建立資料表時定義。請改用 [`CREATE TABLE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#create_table_statement) 陳述式，透過查詢現有資料表中的資料，建立新的分區資料表。
* 時間單位資料欄分區資料表有下列限制：

  + 分區欄必須是純量 `DATE`、`TIMESTAMP` 或 `DATETIME` 欄。雖然資料欄的模式可以是 `REQUIRED` 或 `NULLABLE`，但不能是 `REPEATED` (以陣列為基礎)。
  + 此外，分區資料欄必須是頂層欄位。您無法使用 `RECORD` (`STRUCT`) 的葉欄位做為分區資料欄。

  如要瞭解時間單位資料欄分區資料表，請參閱「[建立時間單位資料欄分區資料表](https://docs.cloud.google.com/bigquery/docs/creating-partitioned-tables?hl=zh-tw#create_a_time-unit_column-partitioned_table)」。
* 整數範圍分區資料表有下列限制：

  + 分區資料欄必須是 `INTEGER` 資料欄。雖然資料欄的模式可能是 `REQUIRED` 或 `NULLABLE`，但不能是 `REPEATED` (以陣列為基礎)。
  + 此外，分區資料欄必須是頂層欄位。您無法使用 `RECORD` (`STRUCT`) 的葉欄位做為分區資料欄。

  如要瞭解整數範圍分區資料表，請參閱「[建立整數範圍分區資料表](https://docs.cloud.google.com/bigquery/docs/creating-partitioned-tables?hl=zh-tw#create_an_integer-range_partitioned_table)」。

## 配額與限制

BigQuery 對分區資料表設有[限制](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#partitioned_tables)。如要進一步瞭解所有配額和限制，請參閱「[配額與限制](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)」。

### 分區資料表工作的配額和限制

配額和限制也適用於您可以針對分區資料表執行的各類型工作，包括：

* [載入資料](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#load_jobs) (載入工作)
* [匯出資料](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#export_jobs) (擷取工作)
* [查詢資料](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#query_jobs) (查詢工作)
* [複製資料表](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#copy_jobs) (複製工作)

### 資料欄分區資料表的分區修改次數配額錯誤

如果資料欄分區資料表達到每日允許的分區修改次數配額，BigQuery 就會傳回這項錯誤。分區修改作業包括所有[載入工作](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#load_jobs)、[複製工作](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#copy_jobs)和[查詢工作](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#query_jobs)，這些工作會附加或覆寫目的地分區。

如要查看「**每個資料欄分區資料表每天的分區修改次數**」限制值，請參閱「[分區資料表](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#partitioned_tables)」。

**錯誤訊息**

```
Quota exceeded: Your table exceeded quota for
Number of partition modifications to a column partitioned table
```

#### 解析度

這項配額無法提高。如要解決這項配額錯誤，請按照下列步驟操作：

* 變更資料表的分區，讓每個分區有更多資料，以減少分區總數。例如，從[按日分區變更為按月分區](https://docs.cloud.google.com/bigquery/docs/partitioned-tables?hl=zh-tw#select_daily_hourly_monthly_or_yearly_partitioning)，或變更[資料表分區方式](https://docs.cloud.google.com/bigquery/docs/partitioned-tables?hl=zh-tw)。
* 使用[分群](https://docs.cloud.google.com/bigquery/docs/clustered-tables?hl=zh-tw#when_to_use_clustering)而非分區。
* 如果您經常從 Cloud Storage 儲存的多個小型檔案載入資料，且每個檔案都使用一項工作，請將多項載入工作合併為單一工作。您可以使用以半形逗號分隔的清單 (例如 `gs://my_path/file_1,gs://my_path/file_2`) 或萬用字元 (例如 `gs://my_path/*`)，從多個 Cloud Storage URI 載入資料。

  詳情請參閱「[批次載入資料](https://docs.cloud.google.com/bigquery/docs/batch-loading-data?hl=zh-tw#permissions-load-data-from-cloud-storage)」。
* 舉例來說，如果您使用載入、選取或複製工作，將單一資料列附加至資料表，建議您將多項工作批次處理成一項工作。BigQuery 做為關聯式資料庫時，效能不佳。最佳做法是避免頻繁執行單列附加動作。
* 如要快速附加資料，建議使用 [BigQuery Storage Write API (gRPC)](https://docs.cloud.google.com/bigquery/docs/write-api?hl=zh-tw)。建議用於高效能資料擷取。BigQuery Storage Write API (gRPC) 具備強大的功能，包括「僅傳送一次」語意。如要瞭解限制和配額，請參閱「[Storage Write API](https://cloud.google.com/bigquery/quotas?hl=zh-tw#write-api-limits)」；如要瞭解使用這個 API 的費用，請參閱「[BigQuery 資料擷取定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#data_ingestion_pricing)」。
* 如要監控資料表上修改的分區數量，請使用 [`INFORMATION_SCHEMA` 檢視表](https://docs.cloud.google.com/bigquery/docs/information-schema-jobs?hl=zh-tw#partitions-modified-by)。
* 如要瞭解如何最佳化資料表載入工作，避免達到配額限制，請參閱「[最佳化載入工作](https://docs.cloud.google.com/bigquery/docs/optimize-load-jobs?hl=zh-tw)」。

## 資料表價格

在 BigQuery 中建立和使用分區資料表時，向您收取的費用是以在分區中儲存的資料量以及針對資料執行的查詢量為計算依據：

* 如需儲存空間價格的相關資訊，請參閱[儲存空間價格](https://cloud.google.com/bigquery/pricing?hl=zh-tw#storage)。
* 如需查詢價格的相關資訊，請參閱[查詢價格](https://cloud.google.com/bigquery/pricing?hl=zh-tw#analysis_pricing_models)。

許多分區資料表作業都是免費的，包括將資料載入分區、複製分區，以及從分區匯出資料。雖然這些作業都是免費的，但仍受限於 BigQuery 的[配額和限制](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)。如需所有免費作業的相關資訊，請參閱定價頁面上的[免費作業項目](https://cloud.google.com/bigquery/pricing?hl=zh-tw#free)一節。

如要瞭解在 BigQuery 控管費用的最佳做法，請參閱「[在 BigQuery 控管費用](https://docs.cloud.google.com/bigquery/docs/best-practices-costs?hl=zh-tw)」

## 資料表安全性

分區資料表的存取控管機制與標準資料表相同。詳情請參閱「[資料表存取控管簡介](https://docs.cloud.google.com/bigquery/docs/table-access-controls-intro?hl=zh-tw)」。

## 後續步驟

* 如要瞭解如何建立分區資料表，請參閱「[建立分區資料表](https://docs.cloud.google.com/bigquery/docs/creating-partitioned-tables?hl=zh-tw)」。
* 如要瞭解如何管理及更新分區資料表，請參閱[管理分區資料表](https://docs.cloud.google.com/bigquery/docs/managing-partitioned-tables?hl=zh-tw)一文。
* 如要瞭解如何查詢分區資料表，請參閱[查詢分區資料表](https://docs.cloud.google.com/bigquery/docs/querying-partitioned-tables?hl=zh-tw)一文。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-10-29 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-10-29 (世界標準時間)。"],[],[]]