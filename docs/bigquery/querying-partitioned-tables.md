Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 查詢分區資料表

本文說明在 BigQuery 中查詢[分區資料表](https://docs.cloud.google.com/bigquery/docs/partitioned-tables?hl=zh-tw)時，需要注意的特定事項。

如需在 BigQuery 中執行查詢的一般資訊，請參閱[執行互動式與批次查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw)。

## 總覽

當查詢作業對分區資料欄套用符合的篩選器時，BigQuery 就能掃描符合篩選條件的分區，並略過其餘的分區。這項程序稱為「分區修剪」。

BigQuery 會透過分區修剪機制，從輸入內容掃描作業中排除不必要的分區。計算查詢作業掃描的位元組數時，系統不會納入修剪的分區。一般來說，分區修剪有助於降低查詢費用。

不同類型的分區資料表會採用不同的修剪行為，因此查詢分區方式不同但其他方面相同的資料表時，您可能會發現處理的位元組數有所差異。如要估算查詢會處理多少位元組，請執行[試算表](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#dry-run)。

## 查詢時間單位資料欄分區資料表

如要在查詢[時間單位資料欄分區資料表](https://docs.cloud.google.com/bigquery/docs/partitioned-tables?hl=zh-tw#date_timestamp_partitioned_tables)時進行剪枝，請在分區資料欄中加入篩選條件。

在下列範例中，假設 `dataset.table` 是根據 `transaction_date` 資料欄進行分區。範例查詢會對 `2016-01-01` 之前的日期進行剪枝。

```
SELECT * FROM dataset.table
WHERE transaction_date >= '2016-01-01'
```

## 查詢擷取時間分區資料表

[擷取時間分區資料表](https://docs.cloud.google.com/bigquery/docs/partitioned-tables?hl=zh-tw#ingestion_time)包含名為 `_PARTITIONTIME` 的虛擬資料欄，也就是分區資料欄。資料欄的值是每個資料列的 UTC 擷取時間，截斷至分區邊界 (例如每小時或每日)，以 `TIMESTAMP` 值表示。

舉例來說，如果您在 2021 年 4 月 15 日 08:15:00 (UTC) 附加資料，這些資料列的 `_PARTITIONTIME` 欄會包含下列值：

* 每小時分區資料表：`TIMESTAMP("2021-04-15 08:00:00")`
* 每日分區資料表：`TIMESTAMP("2021-04-15")`
* 每月分區資料表：`TIMESTAMP("2021-04-01")`
* 按年分區的資料表：`TIMESTAMP("2021-01-01")`

如果分區精細程度為每日，資料表也會包含名為 `_PARTITIONDATE` 的偽資料欄。這個值等於截斷為 `DATE` 值的 `_PARTITIONTIME`。

這兩個虛擬資料欄名稱都已保留，您無法在任何資料表中建立這兩個名稱的資料欄。

如要剪除分區，請篩選任一欄。舉例來說，下列查詢只會掃描 2016 年 1 月 1 日至 2016 年 1 月 2 日之間的分區：

```
SELECT
  column
FROM
  dataset.table
WHERE
  _PARTITIONTIME BETWEEN TIMESTAMP('2016-01-01') AND TIMESTAMP('2016-01-02')
```

如要選取 `_PARTITIONTIME` 虛擬資料欄，您必須使用別名。舉例來說，以下查詢會透過指派別名 `pt` 給虛擬資料欄的方式來選取 `_PARTITIONTIME`：

```
SELECT
  _PARTITIONTIME AS pt, column
FROM
  dataset.table
```

如果是每日分區資料表，您可以選取 `_PARTITIONDATE` 虛擬資料欄，方法如下：

```
SELECT
  _PARTITIONDATE AS pd, column
FROM
  dataset.table
```

`SELECT *` 陳述式不會傳回 `_PARTITIONTIME` 和 `_PARTITIONDATE` 虛擬資料欄，您必須明確選取這些資料欄：

```
SELECT
  _PARTITIONTIME AS pt, *
FROM
  dataset.table
```

### 處理擷取時間分區資料表中的時區

`_PARTITIONTIME` 的值是以填入欄位時的世界標準時間日期為準。如要查詢依據非世界標準時間的時區劃分的資料，請選擇下列其中一個選項：

* 在 SQL 查詢中調整時區差異。
* 使用[分區修飾符](https://docs.cloud.google.com/bigquery/docs/managing-partitioned-table-data?hl=zh-tw#write-to-partition)，依據非世界標準時間的時區，將資料載入特定擷取時間分區。

### 透過虛擬資料欄提升效能

如要提升查詢效能，請在比較作業的左側單獨使用 `_PARTITIONTIME` 虛擬資料欄。

舉例來說，以下兩個查詢的作用相同。視資料表大小而定，第二個查詢的成效可能較佳，因為它在 `>` 運算子的左側單獨放置 `_PARTITIONTIME`。這兩項查詢處理的資料量相同。

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

如要限制查詢中掃描的分區，請在篩選條件中使用常數運算式。以下查詢會根據 `WHERE` 子句中的第一個篩選條件，限制要縮減哪些分區。不過，第二個篩選條件不會限制掃描的分區，因為它使用動態的資料表值。

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

如要限制掃描的分區，請勿在 `_PARTITIONTIME` 篩選器中包含任何其他資料欄。舉例來說，以下查詢不會限制掃描的分區，因為 `field1` 是資料表中的資料欄。

```
-- Scans all partitions of table2. No pruning.
SELECT
  field1
FROM
  dataset.table2
WHERE
  _PARTITIONTIME + field1 = TIMESTAMP('2016-03-28');
```

如果您經常查詢特定時間範圍，建議建立以 `_PARTITIONTIME` 虛擬資料欄為篩選條件的檢視表。舉例來說，下列陳述式會建立檢視表，只包含名為 `dataset.partitioned_table` 的資料表中最近七天的資料：

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

如要在查詢[整數範圍分區資料表](https://docs.cloud.google.com/bigquery/docs/partitioned-tables?hl=zh-tw#integer_range)時修剪分區，請在整數分區資料欄中加入篩選器。

在下列範例中，假設 `dataset.table` 是整數範圍分區資料表，分區規格為 `customer_id:0:100:10`。範例查詢會掃描開頭為 30、40 和 50 的 3 個分區。

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

系統不支援對整數範圍分區資料欄上的函式使用分區修剪。舉例來說，下列查詢會掃描整個資料表。

```
SELECT * FROM dataset.table
WHERE customer_id + 1 BETWEEN 30 AND 50
```

## 查詢寫入最佳化儲存空間中的資料

`__UNPARTITIONED__` 分區會暫時保管串流至分區資料表且位於[寫入最佳化儲存空間](https://docs.cloud.google.com/bigquery/docs/streaming-data-into-bigquery?hl=zh-tw#dataavailability)的資料。直接串流至分區資料表特定分區的資料不會使用 `__UNPARTITIONED__` 分區，而是直接串流至分區。

寫入最佳化儲存空間的資料中，「分區時間」和「分區日期」欄位的值為 `NULL`。`_PARTITIONTIME``_PARTITIONDATE`

如要查詢 `__UNPARTITIONED__` 分區中的資料，請使用 `_PARTITIONTIME` 虛擬資料欄和 `NULL` 值。例如：

```
SELECT
  column
FROM dataset.table
WHERE
  _PARTITIONTIME IS NULL
```

詳情請參閱[以串流方式將資料傳入分區資料表](https://docs.cloud.google.com/bigquery/docs/streaming-data-into-bigquery?hl=zh-tw#streaming_into_partitioned_tables)一節。

## 分割區修剪的最佳做法

本節說明撰寫查詢的最佳做法，運用分區修剪功能提升查詢效能並降低成本。

### 使用常數篩選運算式

如要限制查詢中掃描的分區，請使用常數運算式篩選分區資料欄，而非動態運算式。

下列查詢會縮減分區：

```
SELECT
  t1.name, t1.quantity
FROM
  table1 AS t1
WHERE
  t1.ts = CURRENT_TIMESTAMP()
```

相較之下，下列查詢不會縮減分區，因為述詞 `WHERE t1.ts = (SELECT timestamp FROM table3 WHERE key = 2)` 不是常數運算式。這項查詢會將分區資料欄與動態值進行比較，因此無法修剪分區。

```
SELECT
  t1.name, t1.quantity
FROM
  table1 AS t1
WHERE
  t1.ts = (SELECT timestamp FROM table3 WHERE key = 2)
```

此外，具有下列述詞的查詢不會縮減分區，因為這類查詢需要根據第二個非常數資料表欄位 `ts2` 或 `duration` 進行運算：

```
WHERE ts >= ts2

WHERE ts < CURRENT_TIMESTAMP() - duration
```

### 隔離分區資料欄或使用支援的函式

如要剪除分區，篩選條件的結構必須讓 BigQuery 能夠判斷要掃描哪些分區，而不必讀取資料表資料。如要達成這個目標，請在比較運算子的一側隔離分區資料欄，或只在支援的內建函式中包裝資料欄。您可以執行[模擬測試](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#dry-run)，確認特定查詢是否支援分區修剪。

如果分區資料欄的下列內建函式有額外常數引數，則支援分區修剪：

* [`DATE_ADD`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/date_functions?hl=zh-tw#date_add)、
  [`DATE_DIFF`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/date_functions?hl=zh-tw#date_diff)、
  [`DATE_SUB`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/date_functions?hl=zh-tw#date_sub)、
  [`DATE_TRUNC`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/date_functions?hl=zh-tw#date_trunc)、
  [`EXTRACT`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/date_functions?hl=zh-tw#extract) (含
  `YEAR` 部分)
* [`DATETIME_DIFF`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/datetime_functions?hl=zh-tw#datetime_diff)、
* [`TIMESTAMP_ADD`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/timestamp_functions?hl=zh-tw#timestamp_add)、
  [`TIMESTAMP_DIFF`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/timestamp_functions?hl=zh-tw#timestamp_diff)、
  [`TIMESTAMP_SUB`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/timestamp_functions?hl=zh-tw#timestamp_sub)、
  [`TIMESTAMP_TRUNC`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/timestamp_functions?hl=zh-tw#timestamp_trunc)、
  [`EXTRACT`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/timestamp_functions?hl=zh-tw#extract)
  含 `DATE` 或 `YEAR` 部分，
* [`FORMAT_TIMESTAMP`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/timestamp_functions?hl=zh-tw#format_timestamp)
  使用下列格式指定碼：`%F`、`%Y-%m-%d` 和 `%Y%m%d`。

其他函式和複雜的數學運算則需要完整掃描資料表。

#### 範例

下列查詢顯示支援分區修剪的範例述詞。

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

由於述詞與任何資料列都不相符，因此下列查詢會略過所有分區。

```
SELECT COUNT(*) FROM `bigquery-public-data.wikipedia.pageviews_2025`
WHERE EXTRACT(YEAR FROM datehour) = 1900;
```

下列查詢會選取資料表中每個月的第一天，並支援分區修剪。

```
SELECT COUNT(*) FROM bigquery-public-data.wikipedia.pageviews_2025
WHERE DATE(datehour) IN UNNEST(GENERATE_DATE_ARRAY(
  DATE_TRUNC(CURRENT_DATE(), YEAR),
  DATE(DATE_TRUNC(CURRENT_DATE(), YEAR) + INTERVAL 1 YEAR - INTERVAL 1 DAY),
  INTERVAL 1 MONTH
))
```

如果查詢包含下列述詞，系統就不會縮減分區，因為這些述詞會使用不支援的函式來操控分區資料欄：

```
WHERE FORMAT_DATE('%Y-%m-%d %H', ts) = '2025-03-28 20';

WHERE EXTRACT(MONTH FROM ts) = 3 AND EXTRACT(HOUR FROM ts) = 20
```

同樣地，如果查詢包含下列述詞，由於會透過算術運算操控分區資料欄，因此不會縮減分區：

```
WHERE ts + INTERVAL 1 DAY > CURRENT_TIMESTAMP()
```

如要啟用分區剪枝，您必須重新編寫運算式，將分區資料欄 `ts` 從不支援的函式或算術運算中分離出來。如要指定時間範圍，請使用 `>=` 和 `<` 擷取確切範圍。如果是算術，請將運算移至比較式的另一側。

下列查詢會隔離時間範圍的分區資料欄 `ts`，以縮減分區：

```
WHERE ts >= '2025-03-28 20:00:00' AND ts < '2025-03-28 21:00:00'
```

下列查詢會將分區資料欄與算術運算隔離，藉此縮減分區：

```
WHERE ts > CURRENT_TIMESTAMP() - INTERVAL 1 DAY
```

### 篩選多個資料欄

查詢中分區資料欄的述語不會限制您可篩選的其他項目。您可以在同一個子句中加入其他資料欄的述詞，只要評估分割資料欄的條件遵循最佳做法，系統仍會進行分割修剪。`WHERE`請注意，在下列範例中，`AND`
相當重要。如果 `AND` 變更為 `OR`，即使資料分割不符合資料分割欄的述詞，仍無法修剪，因此資料分割修剪將無法運作。這些分區中的資料仍符合查詢條件。`meter_id = 1234`

請注意，述詞不需要按照特定順序編寫。在下列範例查詢中，假設 `ts` 資料欄已分區，無論述語位置為何，系統仍會修剪分區。

```
WHERE meter_id = 1234
  AND ts >= '2025-03-28 20:00:00' AND ts < '2025-03-28 21:00:00'
```

### 在查詢中加入分區篩選條件

建立分區資料表時，可啟用 [Require partition filter] (需要分區篩選器) 選項，要求使用述詞篩選條件。套用此選項時，如嘗試在未指定 `WHERE` 子句的情況下查詢分區資料表，將會產生下列錯誤：

`Cannot query over table 'project_id.dataset.table' without a filter that can be
used for partition elimination`。

這項規定也適用於參照分區資料表的檢視表和具體化檢視表查詢。

篩選條件必須至少有一個述詞只參照分區資料欄，才符合分區排除條件。如果資料表是依據資料欄 `partition_id` 分區，且結構定義中含有額外資料欄 `f`，則下列兩個 `WHERE` 子句都符合需求：

```
WHERE partition_id = "20221231"

WHERE partition_id = "20221231" AND f = "20221130"
```

但下列做法不足，會導致錯誤：

```
WHERE partition_id = "20221231" OR f = "20221130"
```

如果是擷取時間分區資料表，請使用 `_PARTITIONTIME` 或 `_PARTITIONDATE` 虛擬資料欄。

如要進一步瞭解如何在建立分區資料表時新增「需要分區篩選器」選項，請參閱「[建立分區資料表](https://docs.cloud.google.com/bigquery/docs/creating-partitioned-tables?hl=zh-tw)」一節。您也可以在現有表格中[更新](https://docs.cloud.google.com/bigquery/docs/managing-partitioned-tables?hl=zh-tw#require-filter)這項設定。

## 後續步驟

* 如需分區資料表的總覽，請參閱[分區資料表簡介](https://docs.cloud.google.com/bigquery/docs/partitioned-tables?hl=zh-tw)一文。
* 如要進一步瞭解如何建立分區資料表，請參閱[建立分區資料表](https://docs.cloud.google.com/bigquery/docs/creating-partitioned-tables?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-07-05 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-07-05 (世界標準時間)。"],[],[]]