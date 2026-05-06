Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 使用 DML 更新分區資料表資料

本頁提供分區資料表的資料操縱語言 (DML) 支援總覽。

如需有關 DML 的詳細資訊，請參閱：

* [DML 簡介](https://docs.cloud.google.com/bigquery/docs/data-manipulation-language?hl=zh-tw)
* [DML 語法](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/dml-syntax?hl=zh-tw)
* [使用資料操縱語言更新資料表資料](https://docs.cloud.google.com/bigquery/docs/updating-data?hl=zh-tw)

## 範例中使用的資料表

以下 JSON 結構定義代表本頁面的範例中使用的資料表。

`mytable`：[擷取時間分區資料表](https://docs.cloud.google.com/bigquery/docs/partitioned-tables?hl=zh-tw#ingestion_time)

```
    [
      {"name": "field1", "type": "INTEGER"},
      {"name": "field2", "type": "STRING"}
    ]
```

`mytable2`：標準 (未分區) 資料表

```
    [
      {"name": "id", "type": "INTEGER"},
      {"name": "ts", "type": "TIMESTAMP"}
    ]
```

`mycolumntable`：利用 `ts` `TIMESTAMP` 資料欄進行分區的[分區資料表](https://docs.cloud.google.com/bigquery/docs/partitioned-tables?hl=zh-tw#date_timestamp_partitioned_tables)

```
    [
      {"name": "field1", "type": "INTEGER"},
      {"name": "field2", "type": "STRING"}
      {"name": "field3", "type": "BOOLEAN"}
      {"name": "ts", "type": "TIMESTAMP"}
    ]
```

在出現 COLUMN\_ID 的範例中，請將其替換為要執行的資料欄名稱。

## 插入資料

使用 DML [`INSERT` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/dml-syntax?hl=zh-tw#insert_statement)在分區資料表中新增資料列。

### 將資料插入至擷取時間分區資料表

使用 DML 陳述式新增資料列至擷取時間分區資料表時，可指定資料列應新增至哪個分區。您可以使用 [`_PARTITIONTIME` 虛擬資料欄](https://docs.cloud.google.com/bigquery/docs/querying-partitioned-tables?hl=zh-tw#query_an_ingestion-time_partitioned_table)來參照分區。

例如，以下 `INSERT` 陳述式會新增資料列至 `mytable` 的 2017 年 5 月 1 日分區，也就是 `“2017-05-01”`。

```
INSERT INTO
  project_id.dataset.mytable (_PARTITIONTIME,
    field1,
    field2)
SELECT
  TIMESTAMP("2017-05-01"),
  1,
  "one"
```

僅可使用與日期界線完全對應的時間戳記。例如，下列 DML 陳述式會傳回錯誤：

```
INSERT INTO
  project_id.dataset.mytable (_PARTITIONTIME,
    field1,
    field2)
SELECT
  TIMESTAMP("2017-05-01 21:30:00"),
  1,
  "one"
```

**注意：** `_PARTITIONTIME` 虛擬資料欄位亦可透過 [`UPDATE` 陳述式](#updating_data)來修改。

### 將資料插入至分區資料表

使用 DML 將資料插入至分區資料表的程序，與將資料插入至非分區資料表的程序相同。

例如，以下 `INSERT` 陳述式會從 `mytable2` (未分區資料表) 選取資料，藉此新增資料列至分區資料表 `mycolumntable`。

```
INSERT INTO
  project_id.dataset.mycolumntable (ts,
    field1)
SELECT
  ts,
  id
FROM
  project_id.dataset.mytable2
```

## 刪除資料

請使用 DML [`DELETE` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/dml-syntax?hl=zh-tw#delete_statement)來刪除分區資料表中的資料列。

### 刪除擷取時間分區資料表中的資料

下列 `DELETE` 陳述式會刪除 `mytable` 的 2017 年 6 月 1 日分區 (`"2017-06-01"`) 中，`field1` 等於`21` 的所有資料列。請使用 [`_PARTITIONTIME` 虛擬資料欄](https://docs.cloud.google.com/bigquery/docs/querying-partitioned-tables?hl=zh-tw#query_an_ingestion-time_partitioned_table)來參照分區。

```
DELETE
  project_id.dataset.mytable
WHERE
  field1 = 21
  AND _PARTITIONTIME = "2017-06-01"
```

### 刪除分區資料表中的資料

使用 DML 從分區資料表中刪除資料的程序，與從非分區資料表中刪除資料的程序相同。

舉例來說，下列 `DELETE` 陳述式會刪除 `mycolumntable` 的 2017 年 6 月 1 日分區 (`"2017-06-01"`) 中，`field1` 等於 `21` 的所有資料列。

```
DELETE
  project_id.dataset.mycolumntable
WHERE
  field1 = 21
  AND DATE(ts) = "2017-06-01"
```

## 使用 DML DELETE 刪除分區

如果符合條件的 `DELETE` 陳述式涵蓋分區中的所有資料列，BigQuery 就會移除整個分區。這項移除作業不會掃描位元組或耗用配額。以下 `DELETE` 陳述式範例涵蓋 `_PARTITIONDATE` 虛擬資料欄上篩選條件的整個分區：

```
DELETE mydataset.mytable
WHERE _PARTITIONDATE IN ('2076-10-07', '2076-03-06');
```

### 常見的資格不符情形

如果查詢具有下列特徵，可能無法透過最佳化獲得改善：

* 部分分區涵蓋範圍
* 參照非分區資料欄
* 透過 BigQuery [Storage Write API](https://docs.cloud.google.com/bigquery/docs/write-api?hl=zh-tw) 或[舊版串流 API](https://docs.cloud.google.com/bigquery/streaming-data-into-bigquery?hl=zh-tw) [最近擷取的資料](https://docs.cloud.google.com/bigquery/docs/write-api?hl=zh-tw#stream_into_partitioned_tables)
* 含有子查詢或不支援述詞的篩選器

最佳化資格可能因分區類型、基礎儲存空間中繼資料和篩選器述詞而異。最佳做法是執行試運算，確認查詢結果處理的位元組為 0。

### 多陳述式交易

這項最佳化功能適用於[多陳述式交易](https://docs.cloud.google.com/bigquery/docs/transactions?hl=zh-tw)。以下查詢範例會在單一交易中，以另一個資料表的資料取代分區，且不會掃描分區的 `DELETE` 陳述式。

```
DECLARE REPLACE_DAY DATE;
BEGIN TRANSACTION;

-- find the partition which we want to replace
SET REPLACE_DAY = (SELECT MAX(d) FROM mydataset.mytable_staging);

-- delete the entire partition from mytable
DELETE FROM mydataset.mytable WHERE part_col = REPLACE_DAY;

-- insert the new data into the same partition in mytable
INSERT INTO mydataset.mytable
SELECT * FROM mydataset.mytable_staging WHERE part_col = REPLACE_DAY;

COMMIT TRANSACTION;
```

## 更新資料

請使用 [`UPDATE` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/dml-syntax?hl=zh-tw#update_statement)來更新分區資料表中的資料列。

### 更新擷取時間分區資料表中的資料

以下 `UPDATE` 陳述式會將資料列從一個分區移至另一個分區。`mytable` 的 2017 年 5 月 1 日分區 (`“2017-05-01”`) 中，`field1` 等於 `21` 的所有資料列都會移至 2017 年 6 月 1 日分區 (`“2017-06-01”`)。

```
UPDATE
  project_id.dataset.mytable
SET
  _PARTITIONTIME = "2017-06-01"
WHERE
  _PARTITIONTIME = "2017-05-01"
  AND field1 = 21
```

### 更新分區資料表中的資料

使用 DML 更新分區資料表中資料的程序，與更新非分區資料表中資料的程序相同。例如，以下 `UPDATE` 陳述式會將資料列從一個分區移至另一個分區。`mytable` 的 2017 年 5 月 1 日分區 (`“2017-05-01”`) 中，`field1` 等於 `21` 的所有資料列都會移至 2017 年 6 月 1 日分區 (`“2017-06-01”`)。

```
UPDATE
  project_id.dataset.mycolumntable
SET
  ts = "2017-06-01"
WHERE
  DATE(ts) = "2017-05-01"
  AND field1 = 21
```

## 每小時、每月和每年分區資料表的 DML

您可以使用 DML 陳述式修改每小時、每月或每年分區的資料表。提供相關日期/時間戳記/日期時間的小時、月份或年份範圍，如下列每月分區資料表的範例所示：

```
    bq query --nouse_legacy_sql 'DELETE FROM my_dataset.my_table WHERE
    TIMESTAMP_TRUNC(ts_column, MONTH) = "2020-01-01 00:00:00";'
```

或是 `DATETIME` 資料欄分區資料表的另一個範例：

```
    bq query --nouse_legacy_sql 'DELETE FROM my_dataset.my_table WHERE
    dt_column BETWEEN DATETIME("2020-01-01")
    AND DATETIME("2020-05-01");'
```

## 使用 `MERGE` 陳述式

您可以使用 DML [`MERGE` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/dml-syntax?hl=zh-tw#merge_statement)，將分區資料表的 `INSERT`、`UPDATE` 和 `DELETE` 作業合併成單一陳述式，並以不可分割的形式予以執行。

### 在使用 `MERGE` 陳述式時縮減分區

對分區資料表執行 `MERGE` 陳述式時，可以在子查詢篩選器、`search_condition` 篩選器或 `merge_condition` 篩選器中加入分區資料欄，限制掃描的分區。掃描來源資料表、目標資料表或兩者時，都可能發生修剪作業。

下面每一個範例均使用 `_PARTITIONTIME` 虛擬資料欄做為篩選條件，查詢擷取時間分區資料表。

#### 使用子查詢篩選來源資料

在下列 `MERGE` 陳述式中，`USING` 子句中的子查詢會依據來源資料表中的 `_PARTITIONTIME` 虛擬資料欄進行篩選。

```
MERGE dataset.target T
USING (SELECT * FROM dataset.source WHERE _PARTITIONTIME = '2018-01-01') S
ON T.COLUMN_ID = S.COLUMN_ID
WHEN MATCHED THEN
  DELETE
```

查看查詢執行計畫，子查詢會先執行。系統只會掃描來源資料表中 `'2018-01-01'` 分區的資料列。以下是查詢計畫中的相關階段：

```
READ $10:name, $11:_PARTITIONTIME
FROM temp.source
WHERE equal($11, 1514764800.000000000)
```

#### 在 `when_clause` 的 `search_condition` 中使用篩選器

如果 `search_condition` 包含篩選器，查詢最佳化工具會嘗試縮減分區。舉例來說，在下列 `MERGE` 陳述式中，每個 `WHEN
MATCHED` 和 `WHEN NOT MATCHED` 子句都包含 `_PARTITIONTIME` 虛擬資料欄的篩選條件。

```
MERGE dataset.target T
USING dataset.source S
ON T.COLUMN_ID = S.COLUMN_ID
WHEN MATCHED AND T._PARTITIONTIME = '2018-01-01' THEN
  UPDATE SET COLUMN_ID = S.COLUMN_ID
WHEN MATCHED AND T._PARTITIONTIME = '2018-01-02' THEN
  UPDATE SET COLUMN_ID = S.COLUMN_ID + 10
WHEN NOT MATCHED BY SOURCE AND T._PARTITIONTIME = '2018-01-03' THEN
  DELETE
```

在聯結階段，系統只會掃描目標資料表中的下列分區：`'2018-01-01'`、`'2018-01-02'` 和 `'2018-01-03'`，也就是所有 `search_condition` 篩選條件的聯集。

從查詢執行計畫：

```
READ
$1:COLUMN_ID, $2:_PARTITIONTIME, $3:$file_temp_id, $4:$row_temp_id
FROM temp.target
WHERE or(equal($2, 1514764800.000000000), equal($2, 1514851200.000000000), equal($2, 1514937600.000000000))
```

不過，在下列範例中，`WHEN NOT MATCHED BY SOURCE` 子句沒有篩選運算式：

```
MERGE dataset.target T
USING dataset.source S
ON T.COLUMN_ID = S.COLUMN_ID
WHEN MATCHED AND T._PARTITIONTIME = '2018-01-01' THEN
  UPDATE SET COLUMN_ID = S.COLUMN_ID
WHEN NOT MATCHED BY SOURCE THEN
  UPDATE SET COLUMN_ID = COLUMN_ID + 1
```

這項查詢必須掃描整個目標資料表，才能計算 `WHEN NOT MATCHED BY
SOURCE` 子句。因此不會修剪任何分區。

#### 在 `merge_condition` 中使用常數 false 述詞

如果同時使用 `WHEN NOT MATCHED` 和 `WHEN NOT MATCHED BY SOURCE` 子句，BigQuery 通常會執行完整外部聯結，而這無法修剪。不過，如果合併條件使用常數假述詞，BigQuery 就能使用篩選條件來縮減分區。如要進一步瞭解如何使用常數 false 述詞，請參閱[`MERGE` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/dml-syntax?hl=zh-tw#merge_statement)說明文件中的 `merge_condition` 子句說明。

下列範例只會掃描目標和來源資料表中的 `'2018-01-01'` 分區。

```
MERGE dataset.target T
USING dataset.source S
ON FALSE
WHEN NOT MATCHED AND _PARTITIONTIME = '2018-01-01' THEN
  INSERT(COLUMN_ID) VALUES(COLUMN_ID)
WHEN NOT MATCHED BY SOURCE AND _PARTITIONTIME = '2018-01-01' THEN
  DELETE
```

#### 在 `merge_condition` 中使用篩選器

查詢最佳化工具會嘗試在 `merge_condition` 中使用篩選器來縮減分區。查詢最佳化工具不一定能將述詞下推至資料表掃描階段，視彙整類型而定。

在下列範例中，`merge_condition` 會做為述詞，用來彙整來源和目標資料表。查詢最佳化工具掃描這兩個資料表時，可以將這個述詞下推。因此，查詢只會掃描目標和來源資料表中的 `'2018-01-01'` 分區。

```
MERGE dataset.target T
USING dataset.source S
ON T.COLUMN_ID = S.COLUMN_ID AND
  T._PARTITIONTIME = '2018-01-01' AND
  S._PARTITIONTIME = '2018-01-01'
WHEN MATCHED THEN
  UPDATE SET COLUMN_ID = NEW_VALUE
```

在下一個範例中，`merge_condition` 不包含來源資料表的述詞，因此無法對來源資料表執行分區修剪作業。陳述式確實包含目標資料表的述詞，但陳述式使用 `WHEN NOT MATCHED BY SOURCE` 子句，而非 `WHEN MATCHED` 子句。也就是說，查詢必須掃描整個目標資料表，找出不相符的資料列。

```
MERGE dataset.target T
USING dataset.source S
ON T.COLUMN_ID = S.COLUMN_ID AND T._PARTITIONTIME = '2018-01-01'
WHEN NOT MATCHED BY SOURCE THEN
  UPDATE SET COLUMN_ID = NEW_VALUE
```

## 限制

如要瞭解 DML 的限制，請參閱[DML 參考資料](https://docs.cloud.google.com/bigquery/docs/data-manipulation-language?hl=zh-tw)頁面上的[限制](https://docs.cloud.google.com/bigquery/docs/data-manipulation-language?hl=zh-tw#dml-limitations)一節。

## 配額

如要瞭解 DML 配額資訊，請參閱[配額與限制](https://docs.cloud.google.com/bigquery/quota-policy?hl=zh-tw)頁面上的「[DML 陳述式](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#data-manipulation-language-statements)」一節。

## 定價

如要瞭解 DML 定價，請參閱[分區資料表](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/dml-syntax?hl=zh-tw#partitioned_tables)上執行的 DML 陳述式查詢大小計算方式。

## 表格安全性

如要控管 BigQuery 資料表的存取權，請參閱「[使用 IAM 控管資源存取權](https://docs.cloud.google.com/bigquery/docs/control-access-to-resources-iam?hl=zh-tw)」。

## 後續步驟

* 瞭解如何[建立分區資料表](https://docs.cloud.google.com/bigquery/docs/creating-partitioned-tables?hl=zh-tw)
* 瞭解如何[查詢分區資料表](https://docs.cloud.google.com/bigquery/docs/querying-partitioned-tables?hl=zh-tw)
* 取得 [DML 簡介](https://docs.cloud.google.com/bigquery/docs/data-manipulation-language?hl=zh-tw)
* 瞭解如何使用 [DML 語法](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/dml-syntax?hl=zh-tw)撰寫 DML 陳述式




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-06 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-06 (世界標準時間)。"],[],[]]