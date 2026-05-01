* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見

# 使用管道查詢語法 透過集合功能整理內容 你可以依據偏好儲存及分類內容。

管道查詢語法是 GoogleSQL 的擴充功能，支援線性查詢結構，可讓您更輕鬆地讀取、撰寫及維護查詢。您可以在撰寫 GoogleSQL 的任何位置使用管道語法。

管道語法支援與現有 [GoogleSQL 查詢語法](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw)或*標準語法*相同的作業，例如選取、彙整和分組、聯結和篩選，但作業可以依任意順序套用任意次數。管道語法的線性結構可讓您編寫查詢，使查詢語法的順序與建構結果資料表的邏輯步驟順序相符。

使用管道語法的查詢，其計價、執行和最佳化方式，與對應的標準語法查詢相同。使用管道語法撰寫查詢時，請遵循相關指南[估算費用](https://docs.cloud.google.com/bigquery/docs/best-practices-costs?hl=zh-tw)，並[盡可能提高查詢運算效率](https://docs.cloud.google.com/bigquery/docs/best-practices-performance-compute?hl=zh-tw)。

標準語法有許多問題，可能導致難以讀取、編寫及維護。下表說明管道語法如何解決這些問題：

| 標準語法 | 管道語法 |
| --- | --- |
| 條款必須依特定順序顯示。 | 管道運算子可依任何順序套用。 |
| 更複雜的查詢 (例如具有多層匯總的查詢)，通常需要 CTE 或巢狀子查詢。 | 如要表示更複雜的查詢，通常會在查詢結尾加上管道運算子。 |
| 在匯總期間，系統會在 `SELECT`、`GROUP BY` 和 `ORDER BY` 子句中重複資料欄。 | 每個匯總作業只能列出一次資料欄。 |

如要使用 pipe 語法逐步建構複雜查詢，請參閱「[使用 pipe 語法分析資料](https://docs.cloud.google.com/bigquery/docs/analyze-data-pipe-syntax?hl=zh-tw)」。如需完整的語法詳細資料，請參閱「[管道查詢語法](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/pipe-syntax?hl=zh-tw)」參考文件。

## 基本語法

在管道語法中，查詢會以標準 SQL 查詢或 `FROM` 子句開頭。舉例來說，獨立的 `FROM` 子句 (例如 `FROM MyTable`) 是有效的管道語法。標準 SQL 查詢的結果或 `FROM` 子句中的資料表，接著可以做為輸入內容傳遞至管道符號 `|>`，後面接管道運算子名稱和該運算子的任何引數。管道運算子會以某種方式轉換表格，而轉換結果可以傳遞至另一個管道運算子。

您可以在查詢中使用任意數量的管道運算子，執行選取、排序、篩選、聯結或彙整資料欄等作業。管道運算子的名稱與標準語法對應項目相符，且通常具有相同行為。標準語法和管道語法的主要差異在於查詢的結構。即使查詢表示的邏輯變得更複雜，查詢仍可表示為管道運算子的線性序列，不必使用深層巢狀子查詢，因此更容易閱讀及瞭解。

管道語法具有下列主要特徵：

* 管道語法中的每個管道運算子都包含管道符號 `|>`、運算子名稱和任何引數：  
  `|> operator_name argument_list`
* 管道運算子可加到任何有效查詢的結尾。
* 管道運算子可依任意順序套用，次數不限。
* 凡是支援標準語法的地方，都適用管道語法，包括查詢、檢視區塊、傳回資料表的函式和其他環境。
* 您可以在同一項查詢中，混合使用 pipe 語法和標準語法。舉例來說，子查詢可使用與父項查詢不同的語法。
* 管道運算子可以查看管道前方的表格中存在的所有別名。
* 查詢可以[從 `FROM` 子句開始](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/pipe-syntax?hl=zh-tw#from_queries)，且管道運算子可選擇性地加在 `FROM` 子句之後。

請參考下表：

```
CREATE OR REPLACE TABLE mydataset.Produce AS (
  SELECT 'apples' AS item, 2 AS sales, 'fruit' AS category
  UNION ALL
  SELECT 'apples' AS item, 7 AS sales, 'fruit' AS category
  UNION ALL
  SELECT 'carrots' AS item, 0 AS sales, 'vegetable' AS category
  UNION ALL
  SELECT 'bananas' AS item, 15 AS sales, 'fruit' AS category);
```

下列查詢都包含有效的管道語法，可顯示如何依序建構查詢。

查詢[開頭可為 `FROM` 子句](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/pipe-syntax?hl=zh-tw#from_queries)，且不需包含管道符號：

```
-- View the table.
FROM mydataset.Produce;

/*---------+-------+-----------+
 | item    | sales | category  |
 +---------+-------+-----------+
 | apples  | 7     | fruit     |
 | apples  | 2     | fruit     |
 | carrots | 0     | vegetable |
 | bananas | 15    | fruit     |
 +---------+-------+-----------*/
```

您可以使用[`WHERE`管道運算子](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/pipe-syntax?hl=zh-tw#where_pipe_operator)進行篩選：

```
-- Filter items with no sales.
FROM mydataset.Produce
|> WHERE sales > 0;

/*---------+-------+-----------+
 | item    | sales | category  |
 +---------+-------+-----------+
 | apples  | 7     | fruit     |
 | apples  | 2     | fruit     |
 | bananas | 15    | fruit     |
 +---------+-------+-----------*/
```

如要執行匯總作業，請使用 [`AGGREGATE` 管道運算子](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/pipe-syntax?hl=zh-tw#aggregate_pipe_operator)，後面加上任意數量的匯總函式，以及 `GROUP BY` 子句。`GROUP BY` 子句是 `AGGREGATE` 管道運算子的一部分，不會以管道符號 (`|>`) 分隔。

```
-- Compute total sales by item.
FROM mydataset.Produce
|> WHERE sales > 0
|> AGGREGATE SUM(sales) AS total_sales, COUNT(*) AS num_sales
   GROUP BY item;

/*---------+-------------+-----------+
 | item    | total_sales | num_sales |
 +---------+-------------+-----------+
 | apples  | 9           | 2         |
 | bananas | 15          | 1         |
 +---------+-------------+-----------*/
```

現在假設您有下表，其中包含每個項目的 ID：

```
CREATE OR REPLACE TABLE mydataset.ItemData AS (
  SELECT 'apples' AS item, '123' AS id
  UNION ALL
  SELECT 'bananas' AS item, '456' AS id
  UNION ALL
  SELECT 'carrots' AS item, '789' AS id
);
```

您可以使用[`JOIN` 管道運算子](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/pipe-syntax?hl=zh-tw#join_pipe_operator)，將前一項查詢的結果與這個資料表彙整，納入每個項目的 ID：

```
FROM mydataset.Produce
|> WHERE sales > 0
|> AGGREGATE SUM(sales) AS total_sales, COUNT(*) AS num_sales
   GROUP BY item
|> JOIN mydataset.ItemData USING(item);

/*---------+-------------+-----------+-----+
 | item    | total_sales | num_sales | id  |
 +---------+-------------+-----------+-----+
 | apples  | 9           | 2         | 123 |
 | bananas | 15          | 1         | 456 |
 +---------+-------------+-----------+-----*/
```

## 與標準語法的主要差異

管道語法與標準語法的差異如下：

* 查詢[開頭可為 `FROM` 子句](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/pipe-syntax?hl=zh-tw#from_queries)。
* `SELECT` 管道運算子不會執行匯總作業，您必須改用[`AGGREGATE`管道運算子](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/pipe-syntax?hl=zh-tw#aggregate_pipe_operator)。
* 篩選作業一律使用 [`WHERE` 管道運算子](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/pipe-syntax?hl=zh-tw#where_pipe_operator)，可套用至任何位置。`WHERE` 管道運算子 (取代 `HAVING` 和 `QUALIFY`) 可篩選匯總或視窗函式的結果。

詳情請參閱[管道運算子](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/pipe-syntax?hl=zh-tw#pipe_operators)的完整清單。

## 用途

管道語法的常見用途包括：

* **臨時分析和增量查詢建構**：
  作業的邏輯順序可讓您更輕鬆地撰寫及偵錯查詢。任何查詢的前置字元 (直到管道符號 `|>` 為止) 都是有效查詢，可協助您查看長查詢的中間結果。工作效率提升後，整個機構的開發流程就能加快。
* **記錄檔分析**：記錄檔分析使用者經常使用其他類型的管道式語法。管道語法提供熟悉的結構，可簡化使用者加入 [Observability Analytics](https://docs.cloud.google.com/logging/docs/log-analytics?hl=zh-tw#analytics) 和 BigQuery 的程序。

## 管道語法的其他功能

除了少數例外情況，管道語法支援標準語法支援的所有運算子，且語法相同。此外，管道語法會導入額外的管道運算子，並使用經過修改的匯總和聯結語法。以下各節將說明部分運算子。如需所有支援的運算子，請參閱[管道運算子](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/pipe-syntax?hl=zh-tw#pipe_operators)的完整清單。

### `EXTEND` 管道運算子

[`EXTEND` 管道運算子](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/pipe-syntax?hl=zh-tw#extend_pipe_operator)可讓您將計算出的資料欄附加到目前的資料表。`EXTEND` 管道運算子與 `SELECT *, new_column` 陳述式類似，但可讓您更彈性地參照資料欄別名。

請看下表，其中包含每個人的兩項測驗分數：

```
CREATE OR REPLACE TABLE mydataset.Scores AS (
  SELECT 'Alex' AS student, 9 AS score1, 10 AS score2, 10 AS points_possible
  UNION ALL
  SELECT 'Dana' AS student, 5 AS score1, 7 AS score2, 10 AS points_possible);

/*---------+--------+--------+-----------------+
 | student | score1 | score2 | points_possible |
 +---------+--------+--------+-----------------+
 | Alex    | 9      | 10     | 10              |
 | Dana    | 5      | 7      | 10              |
 +---------+--------+--------+-----------------*/
```

假設您想計算每位學生在測驗中獲得的原始分數和百分比分數平均值。在標準語法中，`SELECT` 陳述式中較晚出現的資料欄無法看到較早的別名。如要避免子查詢，您必須重複平均值的運算式：

```
SELECT student,
  (score1 + score2) / 2 AS average_score,
  (score1 + score2) / 2 / points_possible AS average_percent
FROM mydataset.Scores;
```

`EXTEND` 管道運算子可以參照先前使用的別名，讓查詢更容易閱讀，且較不容易出錯：

```
FROM mydataset.Scores
|> EXTEND (score1 + score2) / 2 AS average_score
|> EXTEND average_score / points_possible AS average_percent
|> SELECT student, average_score, average_percent;

/*---------+---------------+-----------------+
 | student | average_score | average_percent |
 +---------+---------------+-----------------+
 | Alex    | 9.5           | .95             |
 | Dana    | 6.0           | 0.6             |
 +---------+---------------+-----------------*/
```

### `SET` 管道運算子

[`SET` 管道運算子](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/pipe-syntax?hl=zh-tw#set_pipe_operator)可讓您取代目前資料表中資料欄的值。`SET` 管道運算子與 `SELECT
* REPLACE (expression AS column)` 陳述式類似，您可以透過資料表別名限定資料欄名稱，藉此參照原始值。

```
FROM (SELECT 3 AS x, 5 AS y)
|> SET x = 2 * x;

/*---+---+
 | x | y |
 +---+---+
 | 6 | 5 |
 +---+---*/
```

### `DROP` 管道運算子

[`DROP`管道運算子](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/pipe-syntax?hl=zh-tw#drop_pipe_operator)可讓您從目前表格中移除資料欄。`DROP` 管道運算子與 `SELECT *
EXCEPT(column)` 陳述式類似，捨棄資料欄後，您仍可透過以資料表別名限定資料欄名稱，參照原始值。

```
FROM (SELECT 1 AS x, 2 AS y) AS t
|> DROP x;

/*---+
 | y |
 +---+
 | 2 |
 +---*/
```

### `RENAME` 管道運算子

[`RENAME` 管道運算子](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/pipe-syntax?hl=zh-tw#rename_pipe_operator)可讓您重新命名目前資料表的資料欄。`RENAME` 管道運算子與 `SELECT *
EXCEPT(old_column), old_column AS new_column` 陳述式類似。

```
FROM (SELECT 1 AS x, 2 AS y, 3 AS z) AS t
|> RENAME y AS w;

/*---+---+---+
 | x | w | z |
 +---+---+---+
 | 1 | 2 | 3 |
 +---+---+---*/
```

### `AGGREGATE` 管道運算子

如要在管道語法中執行匯總作業，請使用 [`AGGREGATE` 管道運算子](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/pipe-syntax?hl=zh-tw#aggregate_pipe_operator)，後面加上任意數量的匯總函式，以及 `GROUP BY` 子句。您不需要在 `SELECT` 子句中重複資料欄。

本節的範例使用 `Produce` 資料表：

```
CREATE OR REPLACE TABLE mydataset.Produce AS (
  SELECT 'apples' AS item, 2 AS sales, 'fruit' AS category
  UNION ALL
  SELECT 'apples' AS item, 7 AS sales, 'fruit' AS category
  UNION ALL
  SELECT 'carrots' AS item, 0 AS sales, 'vegetable' AS category
  UNION ALL
  SELECT 'bananas' AS item, 15 AS sales, 'fruit' AS category);

/*---------+-------+-----------+
 | item    | sales | category  |
 +---------+-------+-----------+
 | apples  | 7     | fruit     |
 | apples  | 2     | fruit     |
 | carrots | 0     | vegetable |
 | bananas | 15    | fruit     |
 +---------+-------+-----------*/
```

```
FROM mydataset.Produce
|> AGGREGATE SUM(sales) AS total, COUNT(*) AS num_records
   GROUP BY item, category;

/*---------+-----------+-------+-------------+
 | item    | category  | total | num_records |
 +---------+-----------+-------+-------------+
 | apples  | fruit     | 9     | 2           |
 | carrots | vegetable | 0     | 1           |
 | bananas | fruit     | 15    | 1           |
 +---------+-----------+-------+-------------*/
```

如果想在彙整後立即排序結果，可以在 `GROUP BY` 子句中標記要排序的資料欄，並加上 `ASC` 或 `DESC`。未標記的欄不會排序。

如要排序所有資料欄，可以將 `GROUP BY` 子句替換為 [`GROUP AND ORDER BY` 子句](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/pipe-syntax?hl=zh-tw#shorthand_order_pipe_syntax)，預設會依遞增順序排序每個資料欄。您可以指定 `DESC`，後面接要以遞減順序排序的資料欄。舉例來說，以下三個查詢的作用相同：

```
-- Use a separate ORDER BY clause.
FROM mydataset.Produce
|> AGGREGATE SUM(sales) AS total, COUNT(*) AS num_records
   GROUP BY category, item
|> ORDER BY category DESC, item;
```

```
-- Explicitly mark how to order columns in the GROUP BY clause.
FROM mydataset.Produce
|> AGGREGATE SUM(sales) AS total, COUNT(*) AS num_records
   GROUP BY category DESC, item ASC;
```

```
-- Only mark descending columns in the GROUP AND ORDER BY clause.
FROM mydataset.Produce
|> AGGREGATE SUM(sales) AS total, COUNT(*) AS num_records
   GROUP AND ORDER BY category DESC, item;
```

使用 `GROUP AND ORDER BY` 子句的優點是不必在兩個位置重複資料欄名稱。

如要執行完整資料表匯總，請使用 `GROUP BY()` 或完全省略 `GROUP BY` 子句：

```
FROM mydataset.Produce
|> AGGREGATE SUM(sales) AS total, COUNT(*) AS num_records;

/*-------+-------------+
 | total | num_records |
 +-------+-------------+
 | 24    | 4           |
 +-------+-------------*/
```

### `JOIN` 管道運算子

[`JOIN` 管道運算子](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/pipe-syntax?hl=zh-tw#join_pipe_operator)可讓您將目前資料表與另一個資料表合併，並支援標準的[聯結作業](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw#join_types)，包括 `CROSS`、`INNER`、`LEFT`、`RIGHT` 和 `FULL`。

以下範例會參照 `Produce` 和 `ItemData` 資料表：

```
CREATE OR REPLACE TABLE mydataset.Produce AS (
  SELECT 'apples' AS item, 2 AS sales, 'fruit' AS category
  UNION ALL
  SELECT 'apples' AS item, 7 AS sales, 'fruit' AS category
  UNION ALL
  SELECT 'carrots' AS item, 0 AS sales, 'vegetable' AS category
  UNION ALL
  SELECT 'bananas' AS item, 15 AS sales, 'fruit' AS category);
```

```
CREATE OR REPLACE TABLE mydataset.ItemData AS (
  SELECT 'apples' AS item, '123' AS id
  UNION ALL
  SELECT 'bananas' AS item, '456' AS id
  UNION ALL
  SELECT 'carrots' AS item, '789' AS id
);
```

以下範例使用 `USING` 子句，避免資料欄含糊不清：

```
FROM mydataset.Produce
|> JOIN mydataset.ItemData USING(item)
|> WHERE item = 'apples';

/*--------+-------+----------+-----+
 | item   | sales | category | id  |
 +--------+-------+----------+-----+
 | apples | 2     | fruit    | 123 |
 | apples | 7     | fruit    | 123 |
 +--------+-------+----------+-----*/
```

如要參照目前資料表中的資料欄 (例如在 `ON` 子句中消除資料欄的歧義)，您需要使用 [`AS` 管道運算子](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/pipe-syntax?hl=zh-tw#as_pipe_operator)為目前資料表建立別名。您可以選擇為彙整的資料表建立別名。您可以在後續的管道運算子後方參照這兩個別名：

```
FROM mydataset.Produce
|> AS produce_table
|> JOIN mydataset.ItemData AS item_table
   ON produce_table.item = item_table.item
|> WHERE produce_table.item = 'bananas'
|> SELECT item_table.item, sales, id;

/*---------+-------+-----+
 | item    | sales | id  |
 +---------+-------+-----+
 | bananas | 15    | 123 |
 +---------+-------+-----*/
```

彙整右側無法看到彙整左側，因此您無法將目前的表格與自身彙整。舉例來說，下列查詢會失敗：

```
-- This query doesn't work.
FROM mydataset.Produce
|> AS produce_table
|> JOIN produce_table AS produce_table_2 USING(item);
```

如要使用修改後的資料表執行自我聯結，可以在 `WITH` 子句中使用一般資料表運算式 (CTE)。

```
WITH cte_table AS (
  FROM mydataset.Produce
  |> WHERE item = 'carrots'
)
FROM cte_table
|> JOIN cte_table AS cte_table_2 USING(item);
```

## 範例

請參考下表，瞭解客戶訂單資訊：

```
CREATE OR REPLACE TABLE mydataset.CustomerOrders AS (
  SELECT 1 AS customer_id, 100 AS order_id, 'WA' AS state, 5 AS cost, 'clothing' AS item_type
  UNION ALL
  SELECT 1 AS customer_id, 101 AS order_id, 'WA' AS state, 20 AS cost, 'clothing' AS item_type
  UNION ALL
  SELECT 1 AS customer_id, 102 AS order_id, 'WA' AS state, 3 AS cost, 'food' AS item_type
  UNION ALL
  SELECT 2 AS customer_id, 103 AS order_id, 'NY' AS state, 16 AS cost, 'clothing' AS item_type
  UNION ALL
  SELECT 2 AS customer_id, 104 AS order_id, 'NY' AS state, 22 AS cost, 'housewares' AS item_type
  UNION ALL
  SELECT 2 AS customer_id, 104 AS order_id, 'WA' AS state, 45 AS cost, 'clothing' AS item_type
  UNION ALL
  SELECT 3 AS customer_id, 105 AS order_id, 'MI' AS state, 29 AS cost, 'clothing' AS item_type);
```

假設您想瞭解各州和各項目類型中，回訪顧客的平均消費金額。您可以按照下列方式撰寫查詢：

```
SELECT state, item_type, AVG(total_cost) AS average
FROM
  (
    SELECT
      SUM(cost) AS total_cost,
      customer_id,
      state,
      item_type,
      COUNT(*) OVER (PARTITION BY customer_id) AS num_orders
    FROM mydataset.CustomerOrders
    GROUP BY customer_id, state, item_type
    QUALIFY num_orders > 1
  )
GROUP BY state, item_type
ORDER BY state DESC, item_type ASC;
```

如果您從上到下讀取查詢，會發現系統在定義資料欄之前就已遇到該資料欄。`total_cost`即使在子查詢中，您也會先讀取資料欄的名稱，再查看資料欄來自哪個資料表。

如要解讀這項查詢，必須由內而外讀取。`state` 和 `item_type` 欄在 `SELECT` 和 `GROUP BY` 子句中重複多次，然後在 `ORDER BY` 子句中再次重複。

以下是使用管道語法撰寫的同等查詢：

```
FROM mydataset.CustomerOrders
|> AGGREGATE SUM(cost) AS total_cost, GROUP BY customer_id, state, item_type
|> EXTEND COUNT(*) OVER (PARTITION BY customer_id) AS num_orders
|> WHERE num_orders > 1
|> AGGREGATE AVG(total_cost) AS average GROUP BY state DESC, item_type ASC;

/*-------+------------+---------+
 | state | item_type  | average |
 +-------+------------+---------+
 | WA    | clothing   | 35.0    |
 | WA    | food       | 3.0     |
 | NY    | clothing   | 16.0    |
 | NY    | housewares | 22.0    |
 +-------+------------+---------*/
```

使用管道語法時，您可以編寫查詢，按照您可能思考的邏輯步驟解決原始問題。查詢中的語法行對應下列邏輯步驟：

* 從顧客訂單資料表開始。
* 瞭解各州每位顧客在各類商品上的消費金額。
* 計算每位顧客的訂單數量。
* 將結果限制為回購顧客。
* 找出各州和各項目類型的回訪顧客平均支出金額。

## 限制

* 您無法在管道運算子後方的 `SELECT` 陳述式中加入[差異化隱私子句](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw#dp_clause)。請改用標準語法中的差異化隱私子句，並在查詢後套用管道運算子。

## 後續步驟

* [使用 pipe 語法分析資料](https://docs.cloud.google.com/bigquery/docs/analyze-data-pipe-syntax?hl=zh-tw)
* [管道查詢語法參考資料](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/pipe-syntax?hl=zh-tw)
* [標準查詢語法參考資料](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw)
* [VLDB 2024](https://research.google/pubs/sql-has-problems-we-can-fix-them-pipe-syntax-in-sql/?hl=zh-tw) 大會論文：pipe 語法




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-04-30 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-04-30 (世界標準時間)。"],[],[]]