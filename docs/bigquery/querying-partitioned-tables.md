Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 查詢分區資料表

在 BigQuery 中查詢[分區資料表](https://docs.cloud.google.com/bigquery/docs/partitioned-tables?hl=zh-tw)時，篩選分區資料欄可讓 BigQuery 裁剪分區，進而減少掃描的位元組數並降低查詢成本。本文說明如何查詢時間單位資料欄分區、擷取時間分區和整數範圍分區資料表，並提供分區剪除的最佳做法。

如需執行查詢的一般資訊，請參閱「[執行查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw)」。

## 總覽

當查詢作業對分區資料欄套用符合的篩選器時，BigQuery 就能掃描符合篩選條件的分區，並略過其餘的分區。這項程序稱為*分區修剪*。

BigQuery 會透過分區修剪機制，從輸入內容掃描作業中排除不必要的分區。計算查詢作業掃描的位元組數時，系統不會納入修剪的分區。一般來說，分區修剪有助於降低查詢成本。

不同分區類型的剪除行為會有所差異，因此在查詢分區方式不同但其他方面相同的資料表時，處理的位元組數可能會有所不同。如要估算查詢會處理多少位元組，請執行[模擬測試](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#dry-run)。

## 查詢時間單位資料欄分區資料表

如要在查詢[時間單位資料欄分區資料表](https://docs.cloud.google.com/bigquery/docs/partitioned-tables?hl=zh-tw#date_timestamp_partitioned_tables)時，對分區進行剪枝，請在分區資料欄中加入篩選條件。

在以下範例中，假設 `dataset.table` 是依 `transaction_date` 資料欄分區。範例查詢會對 `2016-01-01`之前的日期進行剪枝。

```
SELECT * FROM dataset.table
WHERE transaction_date >= '2016-01-01'
```

## 查詢擷取時間分區資料表

[擷取時間分區資料表](https://docs.cloud.google.com/bigquery/docs/partitioned-tables?hl=zh-tw#ingestion_time)包含名為 `_PARTITIONTIME` 的虛擬資料欄，也就是分區資料欄。資料欄的值是每個資料列的 UTC 擷取時間，會截斷至分區邊界 (例如每小時或每日)，並以 `TIMESTAMP` 值表示。

舉例來說，如果您在 2021 年 4 月 15 日 08:15:00 (世界標準時間) 附加資料，則這些資料列的 `_PARTITIONTIME` 欄會包含下列值：

* 每小時分區資料表：`TIMESTAMP("2021-04-15 08:00:00")`
* 每日分區資料表：`TIMESTAMP("2021-04-15")`
* 每月分區資料表：`TIMESTAMP("2021-04-01")`
* 按年分區的資料表：`TIMESTAMP("2021-01-01")`

如果分區精細程度為每日，資料表也會包含名為 `_PARTITIONDATE` 的虛擬資料欄。這個值等於 `_PARTITIONTIME` 截斷為 `DATE` 值。

這兩個虛擬資料欄名稱均為保留名稱。您無法在任何資料表中建立這兩個名稱的資料欄。

如要對分區進行剪枝，請篩選任一欄。舉例來說，下列查詢只會掃描 2016 年 1 月 1 日到 2016 年 1 月 2 日之間的分區：

```
SELECT
  column
FROM
  dataset.table
WHERE
  _PARTITIONTIME BETWEEN TIMESTAMP('2016-01-01') AND TIMESTAMP('2016-01-02')
```

如要選取 `_PARTITIONTIME` 虛擬資料欄，您必須使用別名。舉例來說，下列查詢會將別名 `pt` 指派給虛擬資料欄，藉此選取 `_PARTITIONTIME`：

```
SELECT
  _PARTITIONTIME AS pt, column
FROM
  dataset.table
```

如果是每日分區資料表，您可以用相同方式選取 `_PARTITIONDATE` 虛擬資料欄：

```
SELECT
  _PARTITIONDATE AS pd, column
FROM
  dataset.table
```

`SELECT *` 陳述式不會傳回 `_PARTITIONTIME` 和 `_PARTITIONDATE` 虛擬資料欄。您必須明確選取這些項目：

```
SELECT
  _PARTITIONTIME AS pt, *
FROM
  dataset.table
```

### 處理擷取時間分區資料表中的時區

`_PARTITIONTIME` 的值取決於填入欄位時的世界標準時間日期。如要根據世界標準時間以外的時區查詢資料，請選擇下列其中一個選項：

* 在 SQL 查詢中調整時區差異。
* 使用[分區修飾符](https://docs.cloud.google.com/bigquery/docs/managing-partitioned-table-data?hl=zh-tw#write-to-partition)，根據世界標準時間以外的時區，將資料載入特定擷取時間分區。

### 使用虛擬資料欄提升效能

如要提升查詢效能，請在比較作業的左側單獨使用 `_PARTITIONTIME` 虛擬資料欄。

舉例來說，下列兩項查詢等效。視資料表大小而定，第二個查詢的成效可能較佳，因為它將 `_PARTITIONTIME` 單獨放在 `>` 運算子的左側。這兩項查詢處理的資料量相同。

```
-- Might be slower.
SELECT
  field1
FROM
  dataset.table1
WHERE
  TIMESTAMP_ADD(_PARTITIONTIME, INTERVAL 5 DAY) > TIMESTAMP("2016-04-15");

-- Often performs better.
SELECT
  field1
FROM
  dataset.table1
WHERE
  _PARTITIONTIME > TIMESTAMP_SUB(TIMESTAMP('2016-04-15'), INTERVAL 5 DAY);
```

如要限制查詢中掃描的分區，請在篩選器中使用常數運算式。下列查詢會根據 `WHERE` 子句中的第一個篩選條件，限制要剪除的分區。不過，第二個篩選條件不會限制掃描的分區，因為該條件使用的是資料表值，而這些值是動態的。

```
SELECT
  column
FROM
  dataset.table2
WHERE
  -- This filter condition limits the scanned partitions:
  _PARTITIONTIME BETWEEN TIMESTAMP('2017-01-01') AND TIMESTAMP('2017-03-01')
  -- This one doesn't, because it uses dynamic table values:
  AND _PARTITIONTIME = (SELECT MAX(timestamp) from dataset.table1)
```

如要限制掃描的分區，請勿在 `_PARTITIONTIME` 篩選器中加入任何其他資料欄。舉例來說，下列查詢不會限制掃描的分區，因為 `field1` 是資料表中的資料欄。

```
-- Scans all partitions of table2. No pruning.
SELECT
  field1
FROM
  dataset.table2
WHERE
  _PARTITIONTIME + field1 = TIMESTAMP('2016-03-28');
```

如果您經常查詢特定時間範圍，建議建立篩選 `_PARTITIONTIME` 虛擬資料欄的檢視表。舉例來說，下列陳述式會建立檢視表，其中僅包含名為 `dataset.partitioned_table` 的資料表中最近七天的資料：

```
-- This view provides pruning.
CREATE VIEW dataset.past_week AS
  SELECT *
  FROM
    dataset.partitioned_table
  WHERE _PARTITIONTIME BETWEEN
    TIMESTAMP_TRUNC(TIMESTAMP_SUB(CURRENT_TIMESTAMP, INTERVAL 7 * 24 HOUR), DAY)
    AND TIMESTAMP_TRUNC(CURRENT_TIMESTAMP, DAY);
```

請參閱[建立檢視表](https://docs.cloud.google.com/bigquery/docs/views?hl=zh-tw)一文以瞭解相關詳情。

## 查詢整數範圍分區資料表

如要在查詢[整數範圍分區資料表](https://docs.cloud.google.com/bigquery/docs/partitioned-tables?hl=zh-tw#integer_range)時剪除分區，請在整數分區資料欄中加入篩選條件。

在以下範例中，假設 `dataset.table` 是整數範圍分區資料表，分區規格為 `customer_id:0:100:10`。範例查詢會掃描以 30、40 和 50 開頭的三個分區。

```
SELECT * FROM dataset.table
WHERE customer_id BETWEEN 30 AND 50

+-------------+-------+
| customer_id | value |
+-------------+-------+
|          40 |    41 |
|          45 |    46 |
|          30 |    31 |
|          35 |    36 |
|          50 |    51 |
+-------------+-------+
```

如果函式用於整數範圍分區資料欄，則不支援分區剪除。舉例來說，下列查詢會掃描整個資料表。

```
SELECT * FROM dataset.table
WHERE customer_id + 1 BETWEEN 30 AND 50
```

## 查詢寫入最佳化儲存空間中的資料

`__UNPARTITIONED__` 分區會暫時保留串流至分區資料表的資料，而資料會存放在[寫入最佳化儲存空間](https://docs.cloud.google.com/bigquery/docs/streaming-data-into-bigquery?hl=zh-tw#dataavailability)。直接串流至分區資料表特定分區的資料不會使用 `__UNPARTITIONED__` 分區。而是直接串流至分區。

寫入最佳化儲存空間的資料中，`_PARTITIONTIME` 和 `_PARTITIONDATE` 欄的值為 `NULL`。

如要查詢 `__UNPARTITIONED__` 分區中的資料，請使用含有 `NULL` 值的 `_PARTITIONTIME` 虛擬資料欄。例如：

```
SELECT
  column
FROM dataset.table
WHERE
  _PARTITIONTIME IS NULL
```

詳情請參閱「[將資料串流至分區資料表](https://docs.cloud.google.com/bigquery/docs/streaming-data-into-bigquery?hl=zh-tw#streaming_into_partitioned_tables)」。

## 分區剪除的最佳做法

本節說明編寫查詢的最佳做法，這些查詢會利用分區剪枝功能，盡可能提高查詢效能並降低成本。

### 使用常數篩選運算式

如要限制查詢中掃描的分區，請使用常數運算式 (而非動態運算式) 篩選分區資料欄。

下列查詢會剪除分區：

```
SELECT
  t1.name, t1.quantity
FROM
  table1 AS t1
WHERE
  t1.ts = CURRENT_TIMESTAMP()
```

相較之下，下列查詢不會剪除分區，因為述詞 `WHERE t1.ts = (SELECT timestamp FROM table3 WHERE key = 2)` 不是常數運算式。這項查詢會將分區欄與動態值進行比較，因此無法進行分區剪除。

```
SELECT
  t1.name, t1.quantity
FROM
  table1 AS t1
WHERE
  t1.ts = (SELECT timestamp FROM table3 WHERE key = 2)
```

此外，含有下列述詞的查詢不會對分區進行剪枝，因為這些查詢需要根據第二個非常數資料表資料欄 `ts2` 或 `duration` 進行運算：

```
WHERE ts >= ts2

WHERE ts < CURRENT_TIMESTAMP() - duration
```

### 隔離分區資料欄或使用支援的函式

如要剪除分區，篩選條件必須經過結構化，讓 BigQuery 能夠判斷要掃描哪些分區，而不必讀取資料表資料。為此，請將分區資料欄隔離在比較運算子的一側，或僅將資料欄包裝在支援的內建函式中。您可以使用[模擬測試](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#dry-run)，確認特定查詢是否支援分區剪除。

如果分區資料欄上的下列內建函式有額外引數，且引數為常數，則支援分區剪除：

* [`DATE_ADD`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/date_functions?hl=zh-tw#date_add)、[`DATE_DIFF`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/date_functions?hl=zh-tw#date_diff)、[`DATE_SUB`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/date_functions?hl=zh-tw#date_sub)、[`DATE_TRUNC`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/date_functions?hl=zh-tw#date_trunc)、[`EXTRACT`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/date_functions?hl=zh-tw#extract)，含 `YEAR` 部分
* [`DATETIME_DIFF`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/datetime_functions?hl=zh-tw#datetime_diff)
* [`TIMESTAMP_ADD`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/timestamp_functions?hl=zh-tw#timestamp_add)、[`TIMESTAMP_DIFF`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/timestamp_functions?hl=zh-tw#timestamp_diff)、[`TIMESTAMP_SUB`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/timestamp_functions?hl=zh-tw#timestamp_sub)、[`TIMESTAMP_TRUNC`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/timestamp_functions?hl=zh-tw#timestamp_trunc)、[`EXTRACT`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/timestamp_functions?hl=zh-tw#extract)，包含 `DATE` 或 `YEAR` 個部分
* [`FORMAT_TIMESTAMP`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/timestamp_functions?hl=zh-tw#format_timestamp)
  搭配下列格式指定碼：`%F`、`%Y-%m-%d` 和 `%Y%m%d`。

其他函式和複雜的數學運算則需要完整資料表掃描。

#### 範例

下列查詢顯示支援分區剪枝的範例述詞。

```
SELECT COUNT(*) FROM `bigquery-public-data.wikipedia.pageviews_2025`
WHERE datehour = '2025-03-30 12:00:00';
```

```
SELECT COUNT(*) FROM `bigquery-public-data.wikipedia.pageviews_2025`
WHERE datehour >= '2025-03-30'
  AND datehour < TIMESTAMP_ADD('2025-03-30', INTERVAL 1 DAY);
```

```
SELECT COUNT(*) FROM `bigquery-public-data.wikipedia.pageviews_2025`
WHERE DATE(datehour) = '2025-03-30';
```

```
SELECT COUNT(*) FROM `bigquery-public-data.wikipedia.pageviews_2025`
WHERE EXTRACT(DATE FROM datehour) = '2025-03-30';
```

```
SELECT COUNT(*) FROM `bigquery-public-data.wikipedia.pageviews_2025`
WHERE CAST(datehour AS DATE) = '2025-03-30';
```

```
SELECT COUNT(*) FROM `bigquery-public-data.wikipedia.pageviews_2025`
WHERE datehour >= '2025-01-01' AND datehour < '2025-02-01';
```

```
SELECT COUNT(*) FROM `bigquery-public-data.wikipedia.pageviews_2025`
WHERE TIMESTAMP_TRUNC(datehour, MONTH) >= '2025-04-01'
  AND TIMESTAMP_TRUNC(datehour, MONTH) < '2025-07-01';
```

```
SELECT COUNT(*) FROM `bigquery-public-data.wikipedia.pageviews_2025`
WHERE TIMESTAMP_DIFF(datehour, '2025-01-01', DAY) < 1;
```

```
SELECT COUNT(*) FROM `bigquery-public-data.wikipedia.pageviews_2025`
WHERE TIMESTAMP_ADD(datehour, INTERVAL 1 DAY) < '2025-01-03';
```

```
SELECT COUNT(*) FROM `bigquery-public-data.wikipedia.pageviews_2025`
WHERE TIMESTAMP_SUB(datehour, INTERVAL 1 DAY) < '2025-01-01';
```

下列查詢會略過所有分區，因為述詞不符合任何資料列。

```
SELECT COUNT(*) FROM `bigquery-public-data.wikipedia.pageviews_2025`
WHERE EXTRACT(YEAR FROM datehour) = 1900;
```

下列查詢會選取資料表中每個月的第一天，並支援分區剪除。

```
SELECT COUNT(*) FROM bigquery-public-data.wikipedia.pageviews_2025
WHERE DATE(datehour) IN UNNEST(GENERATE_DATE_ARRAY(
  DATE_TRUNC(CURRENT_DATE(), YEAR),
  DATE(DATE_TRUNC(CURRENT_DATE(), YEAR) + INTERVAL 1 YEAR - INTERVAL 1 DAY),
  INTERVAL 1 MONTH
))
```

含有下列述詞的查詢不會剪除分區，因為這些查詢會使用不支援的函式操控分區資料欄：

```
WHERE FORMAT_DATE('%Y-%m-%d %H', ts) = '2025-03-28 20';

WHERE EXTRACT(MONTH FROM ts) = 3 AND EXTRACT(HOUR FROM ts) = 20
```

同樣地，使用下列述詞的查詢不會剪除分區，因為該查詢會透過算術運算操作分區資料欄：

```
WHERE ts + INTERVAL 1 DAY > CURRENT_TIMESTAMP()
```

如要啟用分區剪除功能，您必須重寫運算式，將分區欄 `ts` 與不支援的函式或算術運算隔離。如要指定時間範圍，請使用 `>=` 和 `<` 擷取確切範圍。如果是算術，請將運算移至比較式的另一側。

下列查詢會隔離特定日期範圍的分區欄 `ts`，以便進行分區剪除：

```
WHERE ts >= '2025-03-28 20:00:00' AND ts < '2025-03-28 21:00:00'
```

下列查詢會將分區資料欄與算術運算隔離，以便進行分區剪除：

```
WHERE ts > CURRENT_TIMESTAMP() - INTERVAL 1 DAY
```

### 篩選多個資料欄

查詢中分區資料欄的述詞不會限制您篩選其他內容。您可以在同一個 `WHERE` 子句中加入其他資料欄的述詞，只要評估分區資料欄的條件符合最佳做法，系統仍會執行分區剪除。請注意，在以下範例中，`AND` 很重要。如果將 `AND` 變更為 `OR`，分區剪除功能將無法運作，因為即使分區與分區欄上的述詞不相符，仍無法剪除。這些分區中含有 `meter_id = 1234` 的資料仍符合查詢條件。

請注意，述詞不需按照特定順序編寫。在下列查詢範例中，假設對 `ts` 資料欄進行分區，無論述詞位置為何，仍會進行分區剪除。

```
WHERE meter_id = 1234
  AND ts >= '2025-03-28 20:00:00' AND ts < '2025-03-28 21:00:00'
```

### 在查詢中加入分區篩選條件

建立分區資料表時，可啟用 [Require partition filter] (需要分區篩選器) 選項，要求使用述詞篩選條件。套用這個選項後，如果嘗試查詢分區資料表，但未指定 `WHERE` 子句，就會產生下列錯誤：

`Cannot query over table 'project_id.dataset.table' without a filter that can be
used for partition elimination`。

這項規定也適用於參照分區資料表的檢視表和 materialized view 查詢。

至少須有一個述詞只參照分區資料欄，篩選器才符合分區排除條件。如果資料表依 `partition_id` 欄分區，且結構定義中包含額外的 `f` 欄，則下列兩個 `WHERE` 子句都符合要求：

```
WHERE partition_id = "20221231"

WHERE partition_id = "20221231" AND f = "20221130"
```

不過，下列內容不夠完整，會導致錯誤：

```
WHERE partition_id = "20221231" OR f = "20221130"
```

如果是擷取時間分區資料表，請使用 `_PARTITIONTIME` 或 `_PARTITIONDATE` 虛擬資料欄。

如要進一步瞭解如何在建立分區資料表時新增「必須使用分區篩選器」選項，請參閱「[建立分區資料表](https://docs.cloud.google.com/bigquery/docs/creating-partitioned-tables?hl=zh-tw)」。您也可以在現有資料表[更新](https://docs.cloud.google.com/bigquery/docs/managing-partitioned-tables?hl=zh-tw#require-filter)這項設定。

## 後續步驟

* 如需分區資料表的總覽，請參閱[分區資料表簡介](https://docs.cloud.google.com/bigquery/docs/partitioned-tables?hl=zh-tw)一文。
* 如要進一步瞭解如何建立分區資料表，請參閱「[建立分區資料表](https://docs.cloud.google.com/bigquery/docs/creating-partitioned-tables?hl=zh-tw)」。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-10-29 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-10-29 (世界標準時間)。"],[],[]]