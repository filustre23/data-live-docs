Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見

# 使用陣列 透過集合功能整理內容 你可以依據偏好儲存及分類內容。

在 GoogleSQL for BigQuery 中，陣列是由零或多個相同資料類型的值組成的已排序清單。您可以建構簡單資料類型的陣列 (例如 `INT64`)，或複雜資料類型的陣列 (例如 `STRUCT`)。不過，不支援陣列的陣列。如要進一步瞭解 `ARRAY` 資料類型，包括 `NULL` 處理方式，請參閱「[陣列類型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#array_type)」。

您可以使用 GoogleSQL 建構陣列常值、使用 [`ARRAY`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/array_functions?hl=zh-tw) 函式從子查詢建構陣列，以及使用 [`ARRAY_AGG`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/aggregate_functions?hl=zh-tw#array_agg) 函式將值匯總至陣列。

您可以使用如 `ARRAY_CONCAT()` 等函式來合併陣列，然後以 `ARRAY_TO_STRING()` 將陣列轉換為字串。

## 存取陣列元素

請參考名為 `Sequences` 的資料表。這個資料表包含
`ARRAY` 資料類型的 `some_numbers` 資料欄。

```
WITH
  Sequences AS (
    SELECT [0, 1, 1, 2, 3, 5] AS some_numbers UNION ALL
    SELECT [2, 4, 8, 16, 32] UNION ALL
    SELECT [5, 10]
  )
SELECT * FROM Sequences;

/*---------------------+
 | some_numbers        |
 +---------------------+
 | [0, 1, 1, 2, 3, 5]  |
 | [2, 4, 8, 16, 32]   |
 | [5, 10]             |
 +---------------------*/
```

如要存取 `some_numbers` 資料欄中的陣列元素，請指定要使用的索引類型：[`index`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/operators?hl=zh-tw#array_subscript_operator) 或 [`OFFSET(index)`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/operators?hl=zh-tw#array_subscript_operator) (用於以零為基準的索引)，或 [`ORDINAL(index)`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/operators?hl=zh-tw#array_subscript_operator) (用於以一為基準的索引)：

```
SELECT
  some_numbers,
  some_numbers[0] AS index_0,
  some_numbers[OFFSET(1)] AS offset_1,
  some_numbers[ORDINAL(1)] AS ordinal_1
FROM Sequences;

/*--------------------+---------+----------+-----------+
 | some_numbers       | index_0 | offset_1 | ordinal_1 |
 +--------------------+---------+----------+-----------+
 | [0, 1, 1, 2, 3, 5] | 0       | 1        | 0         |
 | [2, 4, 8, 16, 32]  | 2       | 4        | 2         |
 | [5, 10]            | 5       | 10       | 5         |
 +--------------------+---------+----------+-----------*/
```

**注意：** 如果索引超出範圍，`OFFSET` 和 `ORDINAL` 會引發錯誤。為避免這種情況，您可以使用 `SAFE_OFFSET` 或 `SAFE_ORDINAL` 傳回 `NULL`，而不是引發錯誤。

如要存取陣列中的第一個或最後一個元素，請使用 [`ARRAY_FIRST`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/array_functions?hl=zh-tw#array_first) 或 [`ARRAY_LAST`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/array_functions?hl=zh-tw#array_last) 函式：

```
SELECT
  some_numbers,
  ARRAY_FIRST(some_numbers) AS first_element,
  ARRAY_LAST(some_numbers) AS last_element
FROM Sequences;

/*--------------------+---------------+--------------+
 | some_numbers       | first_element | last_element |
 +--------------------+---------------+--------------+
 | [0, 1, 1, 2, 3, 5] | 0             | 5            |
 | [2, 4, 8, 16, 32]  | 2             | 32           |
 | [5, 10]            | 5             | 10           |
 +--------------------+---------------+--------------*/
```

使用 `ARRAY_FIRST` 和 `ARRAY_LAST` 函式時，如果陣列空白，函式會產生錯誤：

```
WITH
  Sequences AS (
    SELECT [0, 1, 1, 2, 3, 5] AS some_numbers
    UNION ALL
    SELECT [2, 4, 8, 16, 32]
    UNION ALL
    SELECT [] -- Empty array
  )
SELECT
  some_numbers,
  ARRAY_LAST(some_numbers) AS last_element
FROM Sequences;

-- Error: ARRAY_LAST can't get the last element of an empty array.
```

如要在存取第一個和最後一個元素時處理空白陣列，您可以在 `-1` 的 `SAFE_OFFSET` 中使用 [`ARRAY_LENGTH`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/array_functions?hl=zh-tw#array_length) 函式。查詢會針對任何空白陣列傳回 `NULL` 值，而不是錯誤：

```
SELECT
  some_numbers,
  some_numbers[SAFE_OFFSET(ARRAY_LENGTH(some_numbers) - 1)] AS last_element
FROM Sequences;

/*--------------------+--------------+
 | some_numbers       | last_element |
 +--------------------+--------------+
 | [0, 1, 1, 2, 3, 5] | 5            |
 | [2, 4, 8, 16, 32]  | 32           |
 | []                 | NULL         |
 +--------------------+--------------*/
```

`ARRAY_LENGTH(array)` 會傳回陣列中的元素數量。由於陣列偏移值是以 0 為基準，因此 `ARRAY_LENGTH(array) - 1` 會提供最後一個元素的偏移值。如果陣列為空，`ARRAY_LENGTH` 為 0，偏移量則會變成 -1。`SAFE_OFFSET(-1)` 會傳回 `NULL`，因此這個方法可以安全地處理空白陣列。

## 尋找長度

[`ARRAY_LENGTH`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/array_functions?hl=zh-tw#array_length) 函式會傳回陣列的長度。

```
WITH Sequences AS
  (SELECT [0, 1, 1, 2, 3, 5] AS some_numbers
   UNION ALL SELECT [2, 4, 8, 16, 32] AS some_numbers
   UNION ALL SELECT [5, 10] AS some_numbers)
SELECT some_numbers,
       ARRAY_LENGTH(some_numbers) AS len
FROM Sequences;

/*--------------------+--------+
 | some_numbers       | len    |
 +--------------------+--------+
 | [0, 1, 1, 2, 3, 5] | 6      |
 | [2, 4, 8, 16, 32]  | 5      |
 | [5, 10]            | 2      |
 +--------------------+--------*/
```

## 將陣列中的元素轉換為資料表中的資料列

如要將 `ARRAY` 轉換為一組資料列 (也稱為「整併」)，請使用 [`UNNEST`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw#unnest_operator) 運算子。`UNNEST` 會採取 `ARRAY`，然後傳回包含 `ARRAY` 中每個元素的單列資料表。

由於 `UNNEST` 會毀損 `ARRAY` 元素的順序，故您或許會想將資料表還原至原始順序。如要這麼做，請使用選用的 `WITH OFFSET` 子句以傳回另一包含各陣列元素之偏移值的資料欄，然後使用 `ORDER BY` 子句來按照偏移值排序資料列。

**範例**

```
SELECT *
FROM UNNEST(['foo', 'bar', 'baz', 'qux', 'corge', 'garply', 'waldo', 'fred'])
  AS element
WITH OFFSET AS offset
ORDER BY offset;

/*----------+--------+
 | element  | offset |
 +----------+--------+
 | foo      | 0      |
 | bar      | 1      |
 | baz      | 2      |
 | qux      | 3      |
 | corge    | 4      |
 | garply   | 5      |
 | waldo    | 6      |
 | fred     | 7      |
 +----------+--------*/
```

如要將 `ARRAY` 類型的整個資料欄扁平化，同時保留每列中其他資料欄的值，請使用關聯的 [`INNER JOIN`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw#inner_join)，將包含 `ARRAY` 資料欄的資料表，彙整至該 `ARRAY` 資料欄的 `UNNEST` 輸出內容。

使用「關聯」彙整時，`UNNEST` 運算子會參照來源資料表中每個資料列的 `ARRAY` 已指定類型和格式的欄，該資料欄先前會出現在 `FROM` 子句中。對於來源資料表中的每個資料列 `N`，`UNNEST` 會將資料列 `N` 中的 `ARRAY` 扁平化為一組包含 `ARRAY` 元素的資料列，然後相關的 `INNER JOIN` 或 `CROSS JOIN` 會將這組新的資料列與來源資料表中的單一資料列 `N` 結合。

**範例**

以下範例使用 [`UNNEST`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw#unnest_operator) 傳回陣列欄中每個元素的資料列。由於 `INNER JOIN`，`id` 欄會包含 `Sequences` 中包含每個數字的資料列的 `id` 值。

```
WITH
  Sequences AS (
    SELECT 1 AS id, [0, 1, 1, 2, 3, 5] AS some_numbers
    UNION ALL SELECT 2 AS id, [2, 4, 8, 16, 32] AS some_numbers
    UNION ALL SELECT 3 AS id, [5, 10] AS some_numbers
  )
SELECT id, flattened_numbers
FROM Sequences
INNER JOIN UNNEST(Sequences.some_numbers) AS flattened_numbers;

/*------+-------------------+
 | id   | flattened_numbers |
 +------+-------------------+
 |    1 |                 0 |
 |    1 |                 1 |
 |    1 |                 1 |
 |    1 |                 2 |
 |    1 |                 3 |
 |    1 |                 5 |
 |    2 |                 2 |
 |    2 |                 4 |
 |    2 |                 8 |
 |    2 |                16 |
 |    2 |                32 |
 |    3 |                 5 |
 |    3 |                10 |
 +------+-------------------*/
```

請注意，對於關聯 join，`UNNEST` 運算子為選用，`INNER JOIN` 則可表示為 `CROSS JOIN` 或逗號 cross join。使用逗號 cross join 簡寫標記法，可將上述範例合併如下：

```
WITH
  Sequences AS (
    SELECT 1 AS id, [0, 1, 1, 2, 3, 5] AS some_numbers
    UNION ALL SELECT 2 AS id, [2, 4, 8, 16, 32] AS some_numbers
    UNION ALL SELECT 3 AS id, [5, 10] AS some_numbers
  )
SELECT id, flattened_numbers
FROM Sequences, Sequences.some_numbers AS flattened_numbers;

/*------+-------------------+
 | id   | flattened_numbers |
 +------+-------------------+
 |    1 |                 0 |
 |    1 |                 1 |
 |    1 |                 1 |
 |    1 |                 2 |
 |    1 |                 3 |
 |    1 |                 5 |
 |    2 |                 2 |
 |    2 |                 4 |
 |    2 |                 8 |
 |    2 |                16 |
 |    2 |                32 |
 |    3 |                 5 |
 |    3 |                10 |
 +------+-------------------*/
```

## 查詢巢狀陣列

如果資料表含有 `STRUCT` 的 `ARRAY`，您可以[整併 `ARRAY`](#flattening_arrays) 以查詢 `STRUCT` 的欄位，也可以整併 `STRUCT` 值的 `ARRAY` 類型欄位。

### 查詢陣列中的 `STRUCT` 元素

以下範例使用 `UNNEST` 搭配 `INNER JOIN` 來整併 `STRUCT` 的 `ARRAY`。

```
WITH
  Races AS (
    SELECT
      "800M" AS race,
      [
        STRUCT("Rudisha" AS name, [23.4, 26.3, 26.4, 26.1] AS laps),
        STRUCT("Makhloufi" AS name, [24.5, 25.4, 26.6, 26.1] AS laps),
        STRUCT("Murphy" AS name, [23.9, 26.0, 27.0, 26.0] AS laps),
        STRUCT("Bosse" AS name, [23.6, 26.2, 26.5, 27.1] AS laps),
        STRUCT("Rotich" AS name, [24.7, 25.6, 26.9, 26.4] AS laps),
        STRUCT("Lewandowski" AS name, [25.0, 25.7, 26.3, 27.2] AS laps),
        STRUCT("Kipketer" AS name, [23.2, 26.1, 27.3, 29.4] AS laps),
        STRUCT("Berian" AS name, [23.7, 26.1, 27.0, 29.3] AS laps)
      ] AS participants
    )
SELECT
  race,
  participant
FROM Races AS r
INNER JOIN UNNEST(r.participants) AS participant;

/*------+---------------------------------------+
 | race | participant                           |
 +------+---------------------------------------+
 | 800M | {Rudisha, [23.4, 26.3, 26.4, 26.1]}   |
 | 800M | {Makhloufi, [24.5, 25.4, 26.6, 26.1]} |
 | 800M | {Murphy, [23.9, 26, 27, 26]}          |
 | 800M | {Bosse, [23.6, 26.2, 26.5, 27.1]}     |
 | 800M | {Rotich, [24.7, 25.6, 26.9, 26.4]}    |
 | 800M | {Lewandowski, [25, 25.7, 26.3, 27.2]} |
 | 800M | {Kipketer, [23.2, 26.1, 27.3, 29.4]}  |
 | 800M | {Berian, [23.7, 26.1, 27, 29.3]}      |
 +------+---------------------------------------*/
```

您可以在重複的欄位中發現特定資訊。舉例來說，以下查詢會傳回 800 公尺競賽中速度最快的跑者。

**注意：** 這個範例不涉及扁平化陣列，但確實代表從重複欄位取得資訊的常見方式。

**範例**

```
WITH
  Races AS (
    SELECT
      "800M" AS race,
      [
        STRUCT("Rudisha" AS name, [23.4, 26.3, 26.4, 26.1] AS laps),
        STRUCT("Makhloufi" AS name, [24.5, 25.4, 26.6, 26.1] AS laps),
        STRUCT("Murphy" AS name, [23.9, 26.0, 27.0, 26.0] AS laps),
        STRUCT("Bosse" AS name, [23.6, 26.2, 26.5, 27.1] AS laps),
        STRUCT("Rotich" AS name, [24.7, 25.6, 26.9, 26.4] AS laps),
        STRUCT("Lewandowski" AS name, [25.0, 25.7, 26.3, 27.2] AS laps),
        STRUCT("Kipketer" AS name, [23.2, 26.1, 27.3, 29.4] AS laps),
        STRUCT("Berian" AS name, [23.7, 26.1, 27.0, 29.3] AS laps)
      ] AS participants
  )
SELECT
  race,
  (
    SELECT name
    FROM UNNEST(participants)
    ORDER BY (SELECT SUM(duration) FROM UNNEST(laps) AS duration) ASC
    LIMIT 1
  ) AS fastest_racer
FROM Races;

/*------+---------------+
 | race | fastest_racer |
 +------+---------------+
 | 800M | Rudisha       |
 +------+---------------*/
```

### 查詢 struct 中的 `ARRAY` 類型欄位

您也可以從巢狀的重複欄位取得資訊。舉例來說，下列陳述式會傳回 800 公尺競賽中圈速最快的跑者。

```
WITH
  Races AS (
    SELECT
      "800M" AS race,
      [
        STRUCT("Rudisha" AS name, [23.4, 26.3, 26.4, 26.1] AS laps),
        STRUCT("Makhloufi" AS name, [24.5, 25.4, 26.6, 26.1] AS laps),
        STRUCT("Murphy" AS name, [23.9, 26.0, 27.0, 26.0] AS laps),
        STRUCT("Bosse" AS name, [23.6, 26.2, 26.5, 27.1] AS laps),
        STRUCT("Rotich" AS name, [24.7, 25.6, 26.9, 26.4] AS laps),
        STRUCT("Lewandowski" AS name, [25.0, 25.7, 26.3, 27.2] AS laps),
        STRUCT("Kipketer" AS name, [23.2, 26.1, 27.3, 29.4] AS laps),
        STRUCT("Berian" AS name, [23.7, 26.1, 27.0, 29.3] AS laps)
      ]AS participants
  )
SELECT
  race,
  (
    SELECT name
    FROM UNNEST(participants), UNNEST(laps) AS duration
    ORDER BY duration ASC
    LIMIT 1
  ) AS runner_with_fastest_lap
FROM Races;

/*------+-------------------------+
 | race | runner_with_fastest_lap |
 +------+-------------------------+
 | 800M | Kipketer                |
 +------+-------------------------*/
```

請注意，上述查詢使用逗號運算子 (`,`) 執行 cross join 並展開陣列。這相當於使用明確的 `CROSS JOIN`，或使用明確 `INNER JOIN` 的下列範例：

```
WITH
  Races AS (
    SELECT "800M" AS race,
      [
        STRUCT("Rudisha" AS name, [23.4, 26.3, 26.4, 26.1] AS laps),
        STRUCT("Makhloufi" AS name, [24.5, 25.4, 26.6, 26.1] AS laps),
        STRUCT("Murphy" AS name, [23.9, 26.0, 27.0, 26.0] AS laps),
        STRUCT("Bosse" AS name, [23.6, 26.2, 26.5, 27.1] AS laps),
        STRUCT("Rotich" AS name, [24.7, 25.6, 26.9, 26.4] AS laps),
        STRUCT("Lewandowski" AS name, [25.0, 25.7, 26.3, 27.2] AS laps),
        STRUCT("Kipketer" AS name, [23.2, 26.1, 27.3, 29.4] AS laps),
        STRUCT("Berian" AS name, [23.7, 26.1, 27.0, 29.3] AS laps)
      ] AS participants
  )
SELECT
  race,
  (
    SELECT name
    FROM UNNEST(participants)
    INNER JOIN UNNEST(laps) AS duration
    ORDER BY duration ASC LIMIT 1
  ) AS runner_with_fastest_lap
FROM Races;

/*------+-------------------------+
 | race | runner_with_fastest_lap |
 +------+-------------------------+
 | 800M | Kipketer                |
 +------+-------------------------*/
```

使用 `INNER JOIN` 簡化陣列會排除含有空白或 `NULL` 陣列的資料列。如要納入這些資料列，請使用 `LEFT JOIN`。

```
WITH
  Races AS (
    SELECT
      "800M" AS race,
      [
        STRUCT("Rudisha" AS name, [23.4, 26.3, 26.4, 26.1] AS laps),
        STRUCT("Makhloufi" AS name, [24.5, 25.4, 26.6, 26.1] AS laps),
        STRUCT("Murphy" AS name, [23.9, 26.0, 27.0, 26.0] AS laps),
        STRUCT("Bosse" AS name, [23.6, 26.2, 26.5, 27.1] AS laps),
        STRUCT("Rotich" AS name, [24.7, 25.6, 26.9, 26.4] AS laps),
        STRUCT("Lewandowski" AS name, [25.0, 25.7, 26.3, 27.2] AS laps),
        STRUCT("Kipketer" AS name, [23.2, 26.1, 27.3, 29.4] AS laps),
        STRUCT("Berian" AS name, [23.7, 26.1, 27.0, 29.3] AS laps),
        STRUCT("Nathan" AS name, ARRAY<FLOAT64>[] AS laps),
        STRUCT("David" AS name, NULL AS laps)
      ] AS participants
  )
SELECT
  Participant.name,
  SUM(duration) AS finish_time
FROM Races
INNER JOIN Races.participants AS Participant
LEFT JOIN Participant.laps AS duration
GROUP BY name;

/*-------------+--------------------+
 | name        | finish_time        |
 +-------------+--------------------+
 | Murphy      | 102.9              |
 | Rudisha     | 102.19999999999999 |
 | David       | NULL               |
 | Rotich      | 103.6              |
 | Makhloufi   | 102.6              |
 | Berian      | 106.1              |
 | Bosse       | 103.4              |
 | Kipketer    | 106                |
 | Nathan      | NULL               |
 | Lewandowski | 104.2              |
 +-------------+--------------------*/
```

## 建立陣列

您可以使用陣列常值或陣列函式建構陣列。如要進一步瞭解如何建構陣列，請參閱「[陣列類型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#constructing_an_array)」。

## 從子查詢建立陣列

處理陣列的常見工作是將子查詢結果轉成陣列。在 GoogleSQL 中，您可以使用 [`ARRAY()`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/array_functions?hl=zh-tw) 函式完成這項操作。

舉例來說，請細想對 `Sequences` 資料表執行的下列作業：

```
WITH Sequences AS
  (SELECT [0, 1, 1, 2, 3, 5] AS some_numbers
  UNION ALL SELECT [2, 4, 8, 16, 32] AS some_numbers
  UNION ALL SELECT [5, 10] AS some_numbers)
SELECT some_numbers,
  ARRAY(SELECT x * 2
        FROM UNNEST(some_numbers) AS x) AS doubled
FROM Sequences;

/*--------------------+---------------------+
 | some_numbers       | doubled             |
 +--------------------+---------------------+
 | [0, 1, 1, 2, 3, 5] | [0, 2, 2, 4, 6, 10] |
 | [2, 4, 8, 16, 32]  | [4, 8, 16, 32, 64]  |
 | [5, 10]            | [10, 20]            |
 +--------------------+---------------------*/
```

這個範例一開始有一個名為「Sequences」的資料表。這個資料表含有類型為 `ARRAY<INT64>` 的資料欄 `some_numbers`。

該查詢本身含有子查詢。這項子查詢會選取 `some_numbers` 資料欄中的每一個資料列，然後使用 [`UNNEST`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw#unnest_operator) 以一組資料列的形式傳回陣列。接著，系統會將每個值乘以二，然後使用 `ARRAY()` 運算子將資料列重新組合成陣列。

## 篩選陣列

以下範例在 `ARRAY()` 運算子的子查詢中使用 `WHERE` 子句來篩選傳回的資料列。

**注意：** 在下列範例中，產生的資料列並未排序。

```
WITH Sequences AS
  (SELECT [0, 1, 1, 2, 3, 5] AS some_numbers
   UNION ALL SELECT [2, 4, 8, 16, 32] AS some_numbers
   UNION ALL SELECT [5, 10] AS some_numbers)
SELECT
  ARRAY(SELECT x * 2
        FROM UNNEST(some_numbers) AS x
        WHERE x < 5) AS doubled_less_than_five
FROM Sequences;

/*------------------------+
 | doubled_less_than_five |
 +------------------------+
 | [0, 2, 2, 4, 6]        |
 | [4, 8]                 |
 | []                     |
 +------------------------*/
```

請注意，第三列包含空白陣列，因為對應原始列 (`[5, 10]`) 中的元素不符合 `x < 5` 的篩選條件。

您也可以使用 `SELECT DISTINCT`，只傳回陣列中非重複的元素，藉以篩選陣列。

```
WITH Sequences AS
  (SELECT [0, 1, 1, 2, 3, 5] AS some_numbers)
SELECT ARRAY(SELECT DISTINCT x
             FROM UNNEST(some_numbers) AS x) AS unique_numbers
FROM Sequences;

/*-----------------+
 | unique_numbers  |
 +-----------------+
 | [0, 1, 2, 3, 5] |
 +-----------------*/
```

您也可以使用 [`IN`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/operators?hl=zh-tw#in_operators) 關鍵字來篩選陣列的資料列。這個關鍵字藉由判定特定值是否符合陣列中的元素，來篩選含有陣列的列。

```
WITH Sequences AS
  (SELECT [0, 1, 1, 2, 3, 5] AS some_numbers
   UNION ALL SELECT [2, 4, 8, 16, 32] AS some_numbers
   UNION ALL SELECT [5, 10] AS some_numbers)
SELECT
   ARRAY(SELECT x
         FROM UNNEST(some_numbers) AS x
         WHERE 2 IN UNNEST(some_numbers)) AS contains_two
FROM Sequences;

/*--------------------+
 | contains_two       |
 +--------------------+
 | [0, 1, 1, 2, 3, 5] |
 | [2, 4, 8, 16, 32]  |
 | []                 |
 +--------------------*/
```

請再次注意，第三列包含空陣列，因為對應原始列 (`[5, 10]`) 中的陣列不含 `2`。

## 掃描陣列

如要檢查陣列是否包含特定值，請使用 [`IN`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/operators?hl=zh-tw#in_operators) 運算子搭配 [`UNNEST`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw#unnest_operator)。如要檢查陣列是否包含符合條件的值，請使用 [`EXISTS`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/operators?hl=zh-tw#exists_operator) 運算子和 `UNNEST`。

### 掃描特定值

如要掃描陣列是否含有特定值，請使用 `IN` 運算子與 `UNNEST`。

**範例**

以下範例會在陣列包含數字 2 時傳回 `true`。

```
SELECT 2 IN UNNEST([0, 1, 1, 2, 3, 5]) AS contains_value;

/*----------------+
 | contains_value |
 +----------------+
 | true           |
 +----------------*/
```

如要傳回陣列資料欄含有特定值的資料表列，請使用 `WHERE` 子句來篩選 `IN UNNEST` 的結果。

**範例**

以下範例會針對每一列，在陣列的資料欄包含數字 2 時傳回 `id` 值。

```
WITH Sequences AS
  (SELECT 1 AS id, [0, 1, 1, 2, 3, 5] AS some_numbers
   UNION ALL SELECT 2 AS id, [2, 4, 8, 16, 32] AS some_numbers
   UNION ALL SELECT 3 AS id, [5, 10] AS some_numbers)
SELECT id AS matching_rows
FROM Sequences
WHERE 2 IN UNNEST(Sequences.some_numbers)
ORDER BY matching_rows;

/*---------------+
 | matching_rows |
 +---------------+
 | 1             |
 | 2             |
 +---------------*/
```

### 掃描符合條件的值

如要掃描陣列尋找符合條件的值，請使用 `UNNEST` 傳回陣列中的元素資料表，使用 `WHERE` 來篩選子查詢中的結果資料表，並使用 `EXISTS` 來檢查篩選的資料表是否含有任何列。

**範例**

以下範例會針對每一列，在陣列的資料欄包含大於 5 的值時傳回 `id` 值。

```
WITH
  Sequences AS (
    SELECT 1 AS id, [0, 1, 1, 2, 3, 5] AS some_numbers
    UNION ALL
    SELECT 2 AS id, [2, 4, 8, 16, 32] AS some_numbers
    UNION ALL
    SELECT 3 AS id, [5, 10] AS some_numbers
  )
SELECT id AS matching_rows
FROM Sequences
WHERE EXISTS(SELECT * FROM UNNEST(some_numbers) AS x WHERE x > 5);

/*---------------+
 | matching_rows |
 +---------------+
 | 2             |
 | 3             |
 +---------------*/
```

#### 掃描符合條件的 `STRUCT` 欄位值

如要搜尋 `STRUCT` 值陣列，找出值符合條件的欄位，請使用 `UNNEST` 傳回資料表，其中每個 `STRUCT` 欄位都有一欄，然後使用 `WHERE EXISTS` 篩除資料表中不符合條件的資料列。

**範例**

以下範例會傳回陣列資料欄包含 `STRUCT`，且其中欄位 `b` 的值大於 3 的列。

```
WITH
  Sequences AS (
    SELECT 1 AS id, [STRUCT(0 AS a, 1 AS b)] AS some_numbers
    UNION ALL
    SELECT 2 AS id, [STRUCT(2 AS a, 4 AS b)] AS some_numbers
    UNION ALL
    SELECT 3 AS id, [STRUCT(5 AS a, 3 AS b), STRUCT(7 AS a, 4 AS b)] AS some_numbers
  )
SELECT id AS matching_rows
FROM Sequences
WHERE EXISTS(SELECT 1 FROM UNNEST(some_numbers) WHERE b > 3);

/*---------------+
 | matching_rows |
 +---------------+
 | 2             |
 | 3             |
 +---------------*/
```

## 陣列和匯總

使用 GoogleSQL 時，您可以使用 `ARRAY_AGG()` 將值匯總至陣列。

```
WITH Fruits AS
  (SELECT "apple" AS fruit
   UNION ALL SELECT "pear" AS fruit
   UNION ALL SELECT "banana" AS fruit)
SELECT ARRAY_AGG(fruit) AS fruit_basket
FROM Fruits;

/*-----------------------+
 | fruit_basket          |
 +-----------------------+
 | [apple, pear, banana] |
 +-----------------------*/
```

`ARRAY_AGG()` 傳回的陣列順序不固定，因為函式串連值的順序不一定。如要排序陣列元素，請使用 `ORDER BY`：

```
WITH Fruits AS
  (SELECT "apple" AS fruit
   UNION ALL SELECT "pear" AS fruit
   UNION ALL SELECT "banana" AS fruit)
SELECT ARRAY_AGG(fruit ORDER BY fruit) AS fruit_basket
FROM Fruits;

/*-----------------------+
 | fruit_basket          |
 +-----------------------+
 | [apple, banana, pear] |
 +-----------------------*/
```

您也可以將匯總函式 (如 `SUM()`) 套用於陣列中的元素。舉例來說，下列查詢會傳回 `Sequences` 資料表中每一列的陣列元素總和。

```
WITH Sequences AS
  (SELECT [0, 1, 1, 2, 3, 5] AS some_numbers
   UNION ALL SELECT [2, 4, 8, 16, 32] AS some_numbers
   UNION ALL SELECT [5, 10] AS some_numbers)
SELECT some_numbers,
  (SELECT SUM(x)
   FROM UNNEST(s.some_numbers) AS x) AS sums
FROM Sequences AS s;

/*--------------------+------+
 | some_numbers       | sums |
 +--------------------+------+
 | [0, 1, 1, 2, 3, 5] | 12   |
 | [2, 4, 8, 16, 32]  | 62   |
 | [5, 10]            | 15   |
 +--------------------+------*/
```

GoogleSQL 也支援匯總函式 `ARRAY_CONCAT_AGG()`，可串連各列的陣列欄元素。

```
WITH Aggregates AS
  (SELECT [1,2] AS numbers
   UNION ALL SELECT [3,4] AS numbers
   UNION ALL SELECT [5, 6] AS numbers)
SELECT ARRAY_CONCAT_AGG(numbers) AS count_to_six_agg
FROM Aggregates;

/*--------------------------------------------------+
 | count_to_six_agg                                 |
 +--------------------------------------------------+
 | [1, 2, 3, 4, 5, 6]                               |
 +--------------------------------------------------*/
```

**注意：** `ARRAY_CONCAT_AGG()` 傳回的陣列不具確定性，因為函式串連值的順序不一定。

## 將陣列轉換為字串

`ARRAY_TO_STRING()`函式可讓您將 `ARRAY<STRING>` 轉換成單一的 `STRING` 值，或是將 `ARRAY<BYTES>` 轉換成單一的 `BYTES` 值，而其結果值是排序串連的陣列元素。

第二個引數是函式會在輸入之間插入以產生輸出的分隔符；第二個引數的類型必須與第一個引數的元素相同。

範例：

```
WITH Words AS
  (SELECT ["Hello", "World"] AS greeting)
SELECT ARRAY_TO_STRING(greeting, " ") AS greetings
FROM Words;

/*-------------+
 | greetings   |
 +-------------+
 | Hello World |
 +-------------*/
```

選用的第三個引數會取代輸入陣列中的 `NULL` 值。

* 如果省略這個引數，則函式會忽略 `NULL` 陣列元素。
* 如果您提供空字串，則函式會替 `NULL` 陣列元素插入分隔符。

範例：

```
SELECT
  ARRAY_TO_STRING(arr, ".", "N") AS non_empty_string,
  ARRAY_TO_STRING(arr, ".", "") AS empty_string,
  ARRAY_TO_STRING(arr, ".") AS omitted
FROM (SELECT ["a", NULL, "b", NULL, "c", NULL] AS arr);

/*------------------+--------------+---------+
 | non_empty_string | empty_string | omitted |
 +------------------+--------------+---------+
 | a.N.b.N.c.N      | a..b..c.     | a.b.c   |
 +------------------+--------------+---------*/
```

## 合併陣列

在某些情況下，您可能想要將多個陣列合併成一個陣列。
您可以使用 `ARRAY_CONCAT()` 函式來完成此操作。

```
SELECT ARRAY_CONCAT([1, 2], [3, 4], [5, 6]) AS count_to_six;

/*--------------------------------------------------+
 | count_to_six                                     |
 +--------------------------------------------------+
 | [1, 2, 3, 4, 5, 6]                               |
 +--------------------------------------------------*/
```

## 更新陣列

請參考名為 `arrays_table` 的資料表。資料表的第一欄是整數陣列，第二欄則包含兩個巢狀整數陣列。

```
WITH arrays_table AS (
  SELECT
    [1, 2] AS regular_array,
    STRUCT([10, 20] AS first_array, [100, 200] AS second_array) AS nested_arrays
  UNION ALL SELECT
    [3, 4] AS regular_array,
    STRUCT([30, 40] AS first_array, [300, 400] AS second_array) AS nested_arrays
)
SELECT * FROM arrays_table;

/*---------------*---------------------------*----------------------------+
 | regular_array | nested_arrays.first_array | nested_arrays.second_array |
 +---------------+---------------------------+----------------------------+
 | [1, 2]        | [10, 20]                  | [100, 200]                 |
 | [3, 4]        | [30, 40]                  | [130, 400]                 |
 +---------------*---------------------------*----------------------------*/
```

您可以使用 `UPDATE` 陳述式更新資料表中的陣列。下列範例會將數字 5 插入 `regular_array` 欄，並將 `nested_arrays` 欄 `first_array` 欄位中的元素插入 `second_array` 欄位：

```
UPDATE
  arrays_table
SET
  regular_array = ARRAY_CONCAT(regular_array, [5]),
  nested_arrays.second_array = ARRAY_CONCAT(nested_arrays.second_array,
                                            nested_arrays.first_array)
WHERE TRUE;
SELECT * FROM arrays_table;

/*---------------*---------------------------*----------------------------+
 | regular_array | nested_arrays.first_array | nested_arrays.second_array |
 +---------------+---------------------------+----------------------------+
 | [1, 2, 5]     | [10, 20]                  | [100, 200, 10, 20]         |
 | [3, 4, 5]     | [30, 40]                  | [130, 400, 30, 40]         |
 +---------------*---------------------------*----------------------------*/
```

## 壓縮陣列

如果兩個陣列的大小相同，您可以將它們合併成一個陣列，其中包含來自輸入陣列對應位置的元素組合。這項作業有時稱為[壓縮](https://en.wikipedia.org/wiki/Convolution_(computer_science))。

您可以使用 `UNNEST` 和 `WITH OFFSET` 壓縮陣列。在這個範例中，每個值組合都會以 `STRUCT` 形式儲存在陣列中。

```
WITH
  Combinations AS (
    SELECT
      ['a', 'b'] AS letters,
      [1, 2, 3] AS numbers
  )
SELECT
  ARRAY(
    SELECT AS STRUCT
      letters[SAFE_OFFSET(index)] AS letter,
      numbers[SAFE_OFFSET(index)] AS number
    FROM Combinations
    INNER JOIN
      UNNEST(
        GENERATE_ARRAY(
          0,
          LEAST(ARRAY_LENGTH(letters), ARRAY_LENGTH(numbers)) - 1)) AS index
    ORDER BY index
  ) AS pairs;

/*------------------------------+
 | pairs                        |
 +------------------------------+
 | [{ letter: "a", number: 1 }, |
 |  { letter: "b", number: 2 }] |
 +------------------------------*/
```

您可以使用不同長度的輸入陣列，只要第一個陣列等於或小於第二個陣列的長度即可。壓縮陣列的長度會是最短輸入陣列的長度。

如要取得包含所有元素的壓縮陣列，即使輸入陣列長度不同，也請將 `LEAST` 變更為 `GREATEST`。如果任一陣列中的元素在另一個陣列中沒有相關聯的元素，則會與 `NULL` 配對。

```
WITH
  Combinations AS (
    SELECT
      ['a', 'b'] AS letters,
      [1, 2, 3] AS numbers
  )
SELECT
  ARRAY(
    SELECT AS STRUCT
      letters[SAFE_OFFSET(index)] AS letter,
      numbers[SAFE_OFFSET(index)] AS number
    FROM Combinations
    INNER JOIN
      UNNEST(
        GENERATE_ARRAY(
          0,
          GREATEST(ARRAY_LENGTH(letters), ARRAY_LENGTH(numbers)) - 1)) AS index
    ORDER BY index
  ) AS pairs;

/*-------------------------------+
 | pairs                         |
 +-------------------------------+
 | [{ letter: "a", number: 1 },  |
 |  { letter: "b", number: 2 },  |
 |  { letter: null, number: 3 }] |
 +-------------------------------*/
```

## 建立陣列的陣列

GoogleSQL 不支援直接建構[陣列的陣列](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#array_type)。您必須先建立 struct 陣列，而每個 struct 都包含 `ARRAY` 類型的欄位。為了說明這項操作，請思考以下的 `Points` 資料表：

```
/*----------+
 | point    |
 +----------+
 | [1, 5]   |
 | [2, 8]   |
 | [3, 7]   |
 | [4, 1]   |
 | [5, 7]   |
 +----------*/
```

現在，假設您要建立一個陣列，而該陣列是由 `Points` 資料表中的各個 `point` 所組成。如要完成這項工作，請包裝從 `STRUCT` 中各個資料列傳回的陣列，如下所示。

```
WITH Points AS
  (SELECT [1, 5] AS point
   UNION ALL SELECT [2, 8] AS point
   UNION ALL SELECT [3, 7] AS point
   UNION ALL SELECT [4, 1] AS point
   UNION ALL SELECT [5, 7] AS point)
SELECT ARRAY(
  SELECT STRUCT(point)
  FROM Points)
  AS coordinates;

/*-------------------+
 | coordinates       |
 +-------------------+
 | [{point: [1,5]},  |
 |  {point: [2,8]},  |
 |  {point: [5,7]},  |
 |  {point: [3,7]},  |
 |  {point: [4,1]}]  |
 +-------------------*/
```




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-10-29 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-10-29 (世界標準時間)。"],[],[]]