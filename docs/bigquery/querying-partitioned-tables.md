* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 查詢分區資料表

本文件說明在 BigQuery 中查詢[分區資料表](https://docs.cloud.google.com/bigquery/docs/partitioned-tables?hl=zh-tw)時，應考量的特定事項。

如要進一步瞭解如何在 BigQuery 中執行查詢，請參閱「[執行互動式與批次查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw)」一文。

## 總覽

如果查詢作業對分區資料欄套用符合的篩選器，BigQuery 就能掃描符合篩選條件的分區，並略過其餘的分區。這項程序稱為「區塊修剪」。

分區修剪是 BigQuery 用來從輸入內容掃描作業中排除不必要的分區的機制。計算查詢作業所掃描的位元組數時，系統不會納入修剪的分區。一般來說，分區修剪有助於降低查詢成本。

不同的分區類型會有不同的修剪行為，因此在查詢分區方式不同但其他方面相同的資料表時，您可能會發現處理的位元組數量有所不同。如要預估查詢會處理多少位元組，請執行[模擬測試](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#dry-run)。

## 查詢時間單位資料欄分區資料表

如要在查詢[時間單位資料欄分區資料表](https://docs.cloud.google.com/bigquery/docs/partitioned-tables?hl=zh-tw#date_timestamp_partitioned_tables)時修剪分區，請在區資料欄上加入篩選器。

在以下範例中，假設 `dataset.table` 是根據 `transaction_date` 資料欄進行分區。範例查詢會刪除 `2016-01-01` 之前的日期。

```
SELECT * FROM dataset.table
WHERE transaction_date >= '2016-01-01'
```

## 查詢擷取時間分區資料表

[擷取時間分區資料表](https://docs.cloud.google.com/bigquery/docs/partitioned-tables?hl=zh-tw#ingestion_time)包含名為 `_PARTITIONTIME` 的虛擬資料欄，也就是分區欄。資料欄的值是每個資料列的世界標準時間攝入時間，以 `TIMESTAMP` 值截斷至分區邊界 (例如每小時或每日)。

舉例來說，如果您在 2021 年 4 月 15 日 08:15:00 UTC 附加資料，這些資料列的 `_PARTITIONTIME` 資料欄會包含下列值：

* 每小時分區資料表：`TIMESTAMP("2021-04-15 08:00:00")`
* 每日分區表格：`TIMESTAMP("2021-04-15")`
* 按月分割的表格：`TIMESTAMP("2021-04-01")`
* 按年分區的資料表：`TIMESTAMP("2021-01-01")`

如果分區精細程度為每日，資料表也會包含名為 `_PARTITIONDATE` 的虛擬資料欄。這個值等於 `_PARTITIONTIME` 截斷為 `DATE` 值。

這兩個虛擬資料欄名稱均為保留名稱。您無法在任何資料表中建立這兩個名稱的資料欄。

如要裁剪分區，請篩選任一欄。例如，以下查詢僅會掃描分區資料表中日期介於 2016 年 1 月 1 日至 2016 年 1 月 2 日的分區：

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

對於每日分區的資料表，您可以以相同的方式選取 `_PARTITIONDATE` 虛擬欄：

```
SELECT
  _PARTITIONDATE AS pd, column
FROM
  dataset.table
```

`SELECT *` 陳述式不會傳回 `_PARTITIONTIME` 和 `_PARTITIONDATE` 擬資料欄。您必須明確選取這些權限：

```
SELECT
  _PARTITIONTIME AS pt, *
FROM
  dataset.table
```

### 在擷取時間分區資料表中處理時區

`_PARTITIONTIME` 的值以填入欄位的 UTC 日期為準。如果您想查詢以非世界標準時間的時區劃分的資料，請選擇下列任一選項：

* 調整 SQL 查詢中的時區差異。
* 使用[分區修飾符](https://docs.cloud.google.com/bigquery/docs/managing-partitioned-table-data?hl=zh-tw#write-to-partition)，依據非世界標準時間的時區，將資料載入特定的擷取時間分區。

### 透過虛擬資料欄提升效能

如要提升查詢效能，請在比較的左側使用 `_PARTITIONTIME` 虛擬欄。

舉例來說，以下兩個查詢的作用相同。視資料表大小而定，第二個查詢可能會提供較佳效能，因為它在 `>` 運算子的左側單獨放置 `_PARTITIONTIME`。兩個查詢處理的資料量相同。

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

如要限制在查詢中掃描的分區，請在篩選器中使用常數運算式。以下查詢會根據 `WHERE` 子句中的第一個篩選條件，限制要縮減的分區。不過，第二個篩選器條件會使用動態的資料表值，因此不會限制掃描的分區。

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

如要限制掃描的分區，請勿在 `_PARTITIONTIME` 篩選器中加入任何其他資料欄。例如，以下查詢不會限制掃描的分區，因為 `field1` 是資料表中的資料欄。

```
-- Scans all partitions of table2. No pruning.
SELECT
  field1
FROM
  dataset.table2
WHERE
  _PARTITIONTIME + field1 = TIMESTAMP('2016-03-28');
```

如果您經常查詢特定時間範圍，建議建立篩選 `_PARTITIONTIME` 虛擬欄的檢視畫面。例如，下列陳述式會建立只包含名為 `dataset.partitioned_table` 的資料表中最近七天資料的檢視表：

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

如要在查詢[整數範圍分區資料表](https://docs.cloud.google.com/bigquery/docs/partitioned-tables?hl=zh-tw#integer_range)時修剪分區，請在整數分區資料欄上加入篩選器。

在下列範例中，假設 `dataset.table` 是整數範圍分區資料表，其分區規格為 `customer_id:0:100:10`。範例查詢會掃描開頭為 30、40 和 50 的三個分區。

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

## 在針對寫入作業最佳化的儲存空間中查詢資料

`__UNPARTITIONED__` 分區會暫時保管串流至分區資料表且位於[寫入最佳化儲存空間](https://docs.cloud.google.com/bigquery/docs/streaming-data-into-bigquery?hl=zh-tw#dataavailability)的資料。直接串流至分區資料表特定分區的資料不會使用 `__UNPARTITIONED__` 分區。相反地，資料會直接串流至分區。

在寫入最佳化儲存空間中的資料，在 `_PARTITIONTIME` 和 `_PARTITIONDATE` 資料欄中會有 `NULL` 值。

如要查詢 `__UNPARTITIONED__` 分區中的資料，請使用含有 `NULL` 值的 `_PARTITIONTIME` 虛擬資料欄。例如：

```
SELECT
  column
FROM dataset.table
WHERE
  _PARTITIONTIME IS NULL
```

詳情請參閱「[以串流方式將資料傳入分區資料表](https://docs.cloud.google.com/bigquery/docs/streaming-data-into-bigquery?hl=zh-tw#streaming_into_partitioned_tables)」。

## 分割區裁舊的最佳做法

### 使用常數篩選器運算式

如要限制在查詢中掃描的分區，請在篩選器中使用常數運算式。如果您在查詢篩選器中使用動態運算式，BigQuery 就必須掃描所有分區。

例如，下列查詢會縮減分區，因為篩選器包含常數運算式：

```
SELECT
  t1.name,
  t2.category
FROM
  table1 AS t1
INNER JOIN
  table2 AS t2
ON t1.id_field = t2.field2
WHERE
  t1.ts = CURRENT_TIMESTAMP()
```

不過，下列查詢不會縮減分區，因為篩選器 `WHERE t1.ts = (SELECT timestamp from table where key = 2)` 並非常數運算式，而是取決於 `timestamp` 和 `key` 欄位的動態值：

```
SELECT
  t1.name,
  t2.category
FROM
  table1 AS t1
INNER JOIN
  table2 AS t2
ON
  t1.id_field = t2.field2
WHERE
  t1.ts = (SELECT timestamp from table3 where key = 2)
```

### 在篩選器中隔離分區資料欄

在表示篩選器時隔離分區資料欄。需要多個欄位的資料進行運算的篩選器不會縮減分區。例如，如果查詢具有使用分區資料欄與第二個欄位的日期比較運算子，或包含部分欄位串連，將不會縮減分區。

例如，下列篩選器就不會縮減分區，因為它需要依據分區欄位 `ts` 與第二個欄位 `ts2` 來進行運算：

`WHERE TIMESTAMP_ADD(ts, INTERVAL 6 HOUR) > ts2`

### 在查詢中要求使用分區篩選器

建立分區資料表時，可啟用 [Require partition filter] (需要分區篩選器) 選項，要求使用述詞篩選條件。套用此選項時，如嘗試在未指定 `WHERE` 子句的情況下查詢分區資料表，將會產生下列錯誤：

`Cannot query over table 'project_id.dataset.table' without a filter that can be
used for partition elimination`。

這項規定也適用於參照分區資料表的檢視表和具體化檢視表查詢。

篩選器必須至少包含一個只參照分區欄的述詞，才能視為符合刪除分區的資格。舉例來說，如果資料表是依據 `partition_id` 欄分區，且結構定義中另有 `f` 欄，則下列兩個 `WHERE` 子句都符合需求：

```
WHERE partition_id = "20221231"
WHERE partition_id = "20221231" AND f = "20221130"
```

不過，`WHERE (partition_id = "20221231" OR f = "20221130")` 並不足以處理這項作業。

對於擷取時間分區資料表，請使用 `_PARTITIONTIME` 或 `_PARTITIONDATE` 虛擬資料欄。

如要進一步瞭解如何在建立分區資料表時新增「Require partition filter」選項，請參閱「[建立分區資料表](https://docs.cloud.google.com/bigquery/docs/creating-partitioned-tables?hl=zh-tw)」一文。您也可以[更新](https://docs.cloud.google.com/bigquery/docs/managing-partitioned-tables?hl=zh-tw#require-filter)現有資料表的這項設定。

## 後續步驟

* 如需分區資料表的總覽，請參閱[分區資料表簡介](https://docs.cloud.google.com/bigquery/docs/partitioned-tables?hl=zh-tw)一文。
* 如要進一步瞭解如何建立分區資料表，請參閱「[建立分區資料表](https://docs.cloud.google.com/bigquery/docs/creating-partitioned-tables?hl=zh-tw)」一文。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-02 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-02 (世界標準時間)。"],[],[]]