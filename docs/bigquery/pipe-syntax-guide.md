Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見

# 使用管道查詢語法 透過集合功能整理內容 你可以依據偏好儲存及分類內容。

管道查詢語法是 GoogleSQL 的擴充功能，支援線性查詢結構，可讓您更輕鬆地讀取、寫入及維護查詢。只要是編寫 GoogleSQL 的地方，都可以使用管道語法。

管道語法支援與現有 [GoogleSQL 查詢語法](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw)或*標準語法*相同的作業，例如選取、匯總和分組、彙整及篩選，但作業可以任何順序套用，次數不限。管道語法的線性結構可讓您編寫查詢，使查詢語法的順序與建立結果資料表的邏輯步驟順序相符。

使用管道語法的查詢，其計價、執行和最佳化方式與對應的標準語法查詢相同。使用管道語法編寫查詢時，請按照指南[估算費用](https://docs.cloud.google.com/bigquery/docs/best-practices-costs?hl=zh-tw)，並[最佳化查詢運算](https://docs.cloud.google.com/bigquery/docs/best-practices-performance-compute?hl=zh-tw)。

標準語法存在一些問題，可能導致難以讀取、編寫和維護。下表說明管道語法如何解決這些問題：

| 標準語法 | Pipe 語法 |
| --- | --- |
| 子句必須按照特定順序排列。 | 管道運算子可以按照任何順序套用。 |
| 較複雜的查詢 (例如多層級匯總查詢) 通常需要 CTE 或巢狀子查詢。 | 如要表示更複雜的查詢，通常會在查詢結尾加上管道運算子。 |
| 匯總期間，`SELECT`、`GROUP BY` 和 `ORDER BY` 子句中的資料欄會重複。 | 每個匯總只能列出一次資料欄。 |

如要使用管道語法逐步建構複雜的查詢，請參閱「[使用管道語法分析資料](https://docs.cloud.google.com/bigquery/docs/analyze-data-pipe-syntax?hl=zh-tw)」。如需完整的語法詳細資料，請參閱 [Pipe 查詢語法](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/pipe-syntax?hl=zh-tw)參考文件。

## 基本語法

在管道語法中，查詢會以標準 SQL 查詢或 `FROM` 子句開頭。例如，獨立的 `FROM` 子句 (例如 `FROM MyTable`) 是有效的管道語法。標準 SQL 查詢或 `FROM` 子句中資料表的結果，可做為輸入內容傳遞至管道符號 `|>`，後面接著管道運算子名稱和該運算子的任何引數。管道運算子會以某種方式轉換資料表，並將轉換結果傳遞至另一個管道運算子。

您可以在查詢中使用任意數量的管道運算子，執行選取、排序、篩選、彙整或匯總資料欄等操作。管道運算子的名稱與標準語法對應項目相符，且行為通常相同。標準語法和管道語法的主要差異在於查詢結構。即使查詢表達的邏輯變得更複雜，查詢仍可表示為管道運算子的線性序列，不需使用深度巢狀子查詢，因此更容易閱讀和理解。

管道語法具有下列主要特性：

* 管道語法中的每個管道運算子都包含管道符號 `|>`、運算子名稱和任何引數：  
  `|> operator_name argument_list`
* 管道運算子可加在任何有效查詢的結尾。
* 管道運算子可以任何順序套用，次數不限。
* 只要是支援標準語法的地方，都能使用管道語法，包括查詢、檢視表、資料表值函式和其他情境。
* 在同一查詢中，pipe 語法可與標準語法混用。例如，子查詢可以使用與父項查詢不同的語法。
* 管道運算子可以查看管道前表格中存在的所有別名。
* 查詢可以[以 `FROM` 子句開頭](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/pipe-syntax?hl=zh-tw#from_queries)，並在 `FROM` 子句後方視需要加入管道運算子。

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

下列查詢皆包含有效的管道語法，說明如何依序建構查詢。

查詢可以[以 `FROM` 子句開頭](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/pipe-syntax?hl=zh-tw#from_queries)，且不一定要包含管道符號：

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

您可以使用[`WHERE` 管道運算子](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/pipe-syntax?hl=zh-tw#where_pipe_operator)進行篩選：

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

如要執行匯總，請使用 [`AGGREGATE` 管道運算子](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/pipe-syntax?hl=zh-tw#aggregate_pipe_operator)，後面加上任意數量的匯總函式，再接上 `GROUP BY` 子句。`GROUP BY` 子句是 `AGGREGATE` 管道運算子的一部分，不會以管道符號 (`|>`) 分隔。

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

現在假設您有以下表格，其中包含每個項目的 ID：

```
CREATE OR REPLACE TABLE mydataset.ItemData AS (
  SELECT 'apples' AS item, '123' AS id
  UNION ALL
  SELECT 'bananas' AS item, '456' AS id
  UNION ALL
  SELECT 'carrots' AS item, '789' AS id
);
```

您可以使用 [`JOIN` 管道運算子](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/pipe-syntax?hl=zh-tw#join_pipe_operator)，將前一項查詢的結果與這個資料表彙整，納入各項商品的 ID：

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

Pipe 語法與標準語法的差異如下：

* 查詢可以[以 `FROM` 子句開頭](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/pipe-syntax?hl=zh-tw#from_queries)。
* `SELECT` 管道運算子不會執行匯總。請改用 [`AGGREGATE` 管道運算子](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/pipe-syntax?hl=zh-tw#aggregate_pipe_operator)。
* 篩選一律使用 [`WHERE` 管道運算子](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/pipe-syntax?hl=zh-tw#where_pipe_operator)，可套用至任何位置。`WHERE` 管道運算子可取代 `HAVING` 和 `QUALIFY`，篩選匯總或視窗函式的結果。

如需更多詳細資料，請參閱[管道運算子](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/pipe-syntax?hl=zh-tw#pipe_operators)的完整清單。

## 用途

管道語法的常見用途包括：

* **臨時分析和漸進式查詢建構**：作業的邏輯順序可讓您更輕鬆地編寫及偵錯查詢。任何查詢的前置字串 (直到管道符號 `|>` 為止) 都是有效查詢，可協助您查看長查詢的中繼結果。提高工作效率，加快整個機構的開發流程。
* **記錄檔分析**：記錄檔分析使用者也常使用其他類型的管道式語法。Pipe 語法提供熟悉的結構，可簡化使用者開始使用 [Observability Analytics](https://docs.cloud.google.com/logging/docs/log-analytics?hl=zh-tw#analytics) 和 BigQuery 的流程。

## pipe 語法的其他功能

除了少數例外狀況，管道語法支援標準語法支援的所有運算子，且語法相同。此外，pipe 語法會導入額外的 pipe 運算子，並使用修改過的語法進行匯總和彙整。以下各節將說明其中一些運算子。如要查看所有支援的運算子，請參閱[管道運算子](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/pipe-syntax?hl=zh-tw#pipe_operators)的完整清單。

### `EXTEND` 管道運算子

[`EXTEND` 管道運算子](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/pipe-syntax?hl=zh-tw#extend_pipe_operator)可讓您將計算結果欄附加至目前的資料表。`EXTEND` 管道運算子與 `SELECT *, new_column` 陳述式類似，但參照資料欄別名時更有彈性。

請參考下表，其中包含每人的兩項測驗分數：

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

假設您想計算每位學生在測驗中獲得的平均原始分數和平均百分比分數。在標準語法中，`SELECT` 陳述式中後面的資料欄無法看到前面的別名。如要避免子查詢，您必須重複平均值的運算式：

```
SELECT student,
  (score1 + score2) / 2 AS average_score,
  (score1 + score2) / 2 / points_possible AS average_percent
FROM mydataset.Scores;
```

`EXTEND` 管道運算子可參照先前使用的別名，讓查詢更容易閱讀，也較不易出錯：

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

[`SET` 管道運算子](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/pipe-syntax?hl=zh-tw#set_pipe_operator)可讓您取代目前資料表中的資料欄值。`SET` 管道運算子與 `SELECT
* REPLACE (expression AS column)` 陳述式類似。您可以使用資料表別名限定資料欄名稱，藉此參照原始值。

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

[`DROP` 管道運算子](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/pipe-syntax?hl=zh-tw#drop_pipe_operator)可讓您從目前的資料表中移除資料欄。`DROP` 管道運算子與 `SELECT *
EXCEPT(column)` 陳述式類似。資料欄捨棄後，您仍可使用資料表別名限定資料欄名稱，藉此參照原始值。

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

如要在管道語法中執行匯總，請使用 [`AGGREGATE` 管道運算子](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/pipe-syntax?hl=zh-tw#aggregate_pipe_operator)，後面加上任意數量的匯總函式，再接 `GROUP BY` 子句。您不需要在 `SELECT` 子句中重複資料欄。

本節中的範例使用 `Produce` 資料表：

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

如要在匯總後立即排序結果，可以使用 `ASC` 或 `DESC` 標記 `GROUP BY` 子句中要排序的資料欄。未標示的資料欄不會排序。

如要排序所有資料欄，可以將 `GROUP BY` 子句替換為 [`GROUP AND ORDER BY` 子句](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/pipe-syntax?hl=zh-tw#shorthand_order_pipe_syntax)，根據預設，這會以遞增順序排序每個資料欄。您可以在要以遞減順序排序的資料欄後方指定 `DESC`。例如，下列三個查詢等效：

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

使用 `GROUP AND ORDER BY` 子句的好處是，您不必在兩個地方重複資料欄名稱。

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

[`JOIN` 管道運算子](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/pipe-syntax?hl=zh-tw#join_pipe_operator)可讓您將目前的資料表與其他資料表彙整，並支援標準[彙整作業](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw#join_types)，包括 `CROSS`、`INNER`、`LEFT`、`RIGHT` 和 `FULL`。

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

以下範例使用 `USING` 子句，避免資料欄語意模糊：

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

如要參照目前資料表中的資料欄，例如消除 `ON` 子句中資料欄的歧義，您需要使用 [`AS` 管道運算子](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/pipe-syntax?hl=zh-tw#as_pipe_operator)為目前資料表建立別名。您可以視需要為彙整資料表設定別名。您可以在後續管道運算子後方參照這兩個別名：

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

彙整的右側無法看到彙整的左側，也就是說，您無法將目前的資料表與自身彙整。例如，下列查詢會失敗：

```
-- This query doesn't work.
FROM mydataset.Produce
|> AS produce_table
|> JOIN produce_table AS produce_table_2 USING(item);
```

如要對修改過的資料表執行 self-join，可以在 `WITH` 子句中使用一般資料表運算式 (CTE)。

```
WITH cte_table AS (
  FROM mydataset.Produce
  |> WHERE item = 'carrots'
)
FROM cte_table
|> JOIN cte_table AS cte_table_2 USING(item);
```

## 範例

假設有以下顧客訂單資訊表：

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

假設您想知道各州和項目類型的回訪顧客平均消費金額。您可以按照下列方式編寫查詢：

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

如果從上到下讀取查詢，您會在定義資料欄 `total_cost` 之前遇到該資料欄。即使在子查詢中，您也會先看到資料欄名稱，然後才看到資料欄來源資料表。

如要瞭解這項查詢，請從內到外解讀。`state` 和 `item_type` 資料欄在 `SELECT` 和 `GROUP BY` 子句中重複多次，然後在 `ORDER BY` 子句中再次重複。

以下是使用管道語法編寫的等效查詢：

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

使用管道語法時，您可以按照解決原始問題時可能採取的邏輯步驟編寫查詢。查詢中的語法行對應下列邏輯步驟：

* 首先，請查看顧客訂單資料表。
* 瞭解各州每位顧客在各類商品上的消費金額。
* 計算每位顧客的訂單數量。
* 將結果限制為回訪顧客。
* 找出回訪顧客在各州和各項目類型的平均消費金額。

## 限制

* 您無法在管道運算子後方的 `SELECT` 陳述式中加入[差異化隱私子句](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw#dp_clause)。請改用標準語法的差異化隱私子句，並在查詢後方套用管道運算子。

## 後續步驟

* [使用管道語法分析資料](https://docs.cloud.google.com/bigquery/docs/analyze-data-pipe-syntax?hl=zh-tw)
* [Pipe 查詢語法參考資料](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/pipe-syntax?hl=zh-tw)
* [標準查詢語法參考資料](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw)
* [VLDB 2024](https://research.google/pubs/sql-has-problems-we-can-fix-them-pipe-syntax-in-sql/?hl=zh-tw) 研討會論文：pipe 語法




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-10-29 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-10-29 (世界標準時間)。"],[],[]]