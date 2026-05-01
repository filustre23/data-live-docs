* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [參考資料](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# Amazon Redshift SQL 翻譯指南

本文詳述 Amazon Redshift 和 BigQuery 之間的 SQL 語法相似與相異之處，協助您規劃遷移作業。使用[批次 SQL 翻譯](https://docs.cloud.google.com/bigquery/docs/batch-sql-translator?hl=zh-tw)大量遷移 SQL 指令碼，或使用[互動式 SQL 翻譯](https://docs.cloud.google.com/bigquery/docs/interactive-sql-translator?hl=zh-tw)翻譯臨時查詢。

本指南的目標對象為企業架構師、資料庫管理員、應用程式開發人員和 IT 安全專家。本文假設您已熟悉 Amazon Redshift。

**注意：** 在某些情況下，Amazon Redshift 和 BigQuery 中的 SQL 元素之間沒有直接對應關係。不過在大多數情況下，您可以使用替代方法，在 BigQuery 中達到 Amazon Redshift 所提供的相同功能，如本文件中的範例所示。

## 資料類型

本節說明 Amazon Redshift 和 BigQuery 中對應的資料類型。

| **Amazon Redshift** | | **BigQuery** | **附註** |
| --- | --- | --- | --- |
| **資料類型** | **別名** | **資料類型** |  |
| `SMALLINT` | `INT2` | `INT64` | Amazon Redshift 的 `SMALLINT` 為 2 個位元組，而 BigQuery 的 `INT64` 為 8 個位元組。 |
| `INTEGER` | `INT, INT4` | `INT64` | Amazon Redshift 的 `INTEGER` 為 4 個位元組，而 BigQuery 的 `INT64` 為 8 個位元組。 |
| `BIGINT` | `INT8` | `INT64` | Amazon Redshift 的 `BIGINT` 和 BigQuery 的 `INT64` 都是 8 個位元組。 |
| `DECIMAL` | `NUMERIC` | `NUMERIC` |  |
| `REAL` | `FLOAT4` | `FLOAT64` | Amazon Redshift 的 `REAL` 為 4 個位元組，而 BigQuery 的 `FLOAT64` 為 8 個位元組。 |
| `DOUBLE PRECISION` | `FLOAT8, FLOAT` | `FLOAT64` |  |
| `BOOLEAN` | `BOOL` | `BOOL` | Amazon Redshift 的 `BOOLEAN` 可使用 `TRUE`、`t`、`true`、`y`、`yes` 和 `1` 做為 true 的有效字面值。BigQuery 的`BOOL`資料類型不區分大小寫`TRUE`。 |
| `CHAR` | `CHARACTER, NCHAR, BPCHAR` | `STRING` |  |
| `VARCHAR` | `CHARACTER VARYING, NVARCHAR, TEXT` | `STRING` |  |
| `DATE` |  | `DATE` |  |
| `TIMESTAMP` | `TIMESTAMP WITHOUT TIME ZONE` | `DATETIME` |  |
| `TIMESTAMPTZ` | `TIMESTAMP WITH TIME ZONE` | `TIMESTAMP` | 注意：在 BigQuery 中，剖析時間戳記或設定時間戳記的格式以供顯示時，會使用[時區](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#time_zones)。字串格式的時間戳記可能包含時區，但 BigQuery 在剖析字串時，會將時間戳記儲存為對應的世界標準時間。如果未明確指定時區，系統會使用預設時區 (世界標準時間)。系統支援[時區名稱](https://en.wikipedia.org/wiki/List_of_time_zone_abbreviations)或[與世界標準時間的時差](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/timestamp_functions?hl=zh-tw#timezone_definitions) (-|+)HH:MM，但不支援時區縮寫，例如太平洋夏令時間 (PDT)。 |
| `GEOMETRY` |  | `GEOGRAPHY` | 支援查詢地理空間資料。 |

BigQuery 也有下列資料類型，但沒有直接對應的 Amazon Redshift 類型：

* [`ARRAY`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#array_type)
* [`BYTES`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#bytes_type)
* [`TIME`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#time_type)
* [`STRUCT`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#struct_type)

### 隱含轉換類型

遷移至 BigQuery 時，您需要將大部分的 [Amazon Redshift 隱含轉換](https://docs.aws.amazon.com/redshift/latest/dg/c_Supported_data_types.html#r_Type_conversion)轉換為 BigQuery 的明確轉換，但 BigQuery 會隱含轉換下列資料類型。

BigQuery 會對下列資料類型執行隱含轉換：

| **從 BigQuery 類型** | **BigQuery 類型** |
| --- | --- |
| `INT64` | `FLOAT64` |
| `INT64` | `NUMERIC` |
| `NUMERIC` | `FLOAT64` |

BigQuery 也會對下列常值執行隱含轉換：

| **從 BigQuery 類型** | **BigQuery 類型** |
| --- | --- |
| `STRING` 常值   (例如「2008-12-25」) | `DATE` |
| `STRING` 常值   (例如「2008-12-25 15:30:00」) | `TIMESTAMP` |
| `STRING` 常值   (例如「2008-12-25T07:30:00」) | `DATETIME` |
| `STRING`常值   (例如「15:30:00」) | `TIME` |

### 明確轉換類型

您可以使用 BigQuery 的 [`CAST(expression AS type)`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/conversion_functions?hl=zh-tw#cast)  函式或任何 [`DATE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/date_functions?hl=zh-tw) 和 [`TIMESTAMP`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/timestamp_functions?hl=zh-tw) 轉換函式，轉換 BigQuery 不會隱含轉換的 Amazon Redshift 資料類型。

遷移查詢時，請將所有出現的 Amazon Redshift [`CONVERT(type, expression)`](https://docs.aws.amazon.com/redshift/latest/dg/r_CAST_function.html#convert-function) 函式 (或 :: 語法) 變更為 BigQuery 的 [`CAST(expression AS type)`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/conversion_functions?hl=zh-tw#cast)  函式，如「[資料類型格式化函式](#data_type_formatting_functions)」一節中的表格所示。

## 查詢語法

本節說明 Amazon Redshift 和 BigQuery 之間的查詢語法差異。

### `SELECT` 陳述式

大多數 Amazon Redshift [`SELECT`](https://docs.aws.amazon.com/redshift/latest/dg/r_SELECT_synopsis.html) 陳述式都與 BigQuery 相容。下表列出一些細微差異。

| **Amazon Redshift** | **BigQuery** |
| --- | --- |
| `SELECT TOP number expression   FROM table` | `SELECT expression   FROM table   ORDER BY expression DESC   LIMIT number` |
| `SELECT   x/total AS probability,   ROUND(100 * probability, 1) AS pct   FROM raw_data`     注意：Redshift 支援在同一個 `SELECT` 陳述式中建立及參照別名。 | `SELECT   x/total AS probability,   ROUND(100 * (x/total), 1) AS pct   FROM raw_data` |

BigQuery 也支援 `SELECT` 陳述式中的下列運算式，這些運算式沒有對應的 Amazon Redshift 運算式：

* [`EXCEPT`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw#select_except)
* [`REPLACE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw#select_replace)

### `FROM` 子句

查詢中的 [`FROM`](https://docs.aws.amazon.com/redshift/latest/dg/r_FROM_clause30.html) 子句會列出選取資料的資料表參照。在 Amazon Redshift 中，可能的資料表參照包括資料表、檢視區塊和子查詢。BigQuery 支援所有這些資料表參照。

您可以使用下列項目，在 `FROM` 子句中參照 BigQuery 資料表：

* `[project_id].[dataset_id].[table_name]`
* `[dataset_id].[table_name]`
* `[table_name]`

BigQuery 也支援其他資料表參照：

* 使用 [`FOR SYSTEM_TIME AS OF`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw#for_system_time_as_of) 取得資料表定義和資料列的歷史版本。
* [欄位路徑](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw#field_path)，或解析為某資料類型內之欄位的任一路徑 (例如 `STRUCT`)。
* [扁平化陣列](https://docs.cloud.google.com/bigquery/docs/arrays?hl=zh-tw#querying_nested_arrays)。

### `JOIN` 種類型

Amazon Redshift 和 BigQuery 都支援下列類型的聯結：

* `[INNER] JOIN`
* `LEFT [OUTER] JOIN`
* `RIGHT [OUTER] JOIN`
* `FULL [OUTER] JOIN`
* 和對等的[隱含逗號交叉聯結](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw#cross_join)。`CROSS JOIN`

下表列出一些細微差異。

| **Amazon Redshift** | **BigQuery** |
| --- | --- |
| `SELECT col   FROM table1   NATURAL INNER JOIN   table2` | `SELECT col1   FROM table1   INNER JOIN   table2   USING (col1, col2 [, ...])`   注意：在 BigQuery 中，`JOIN` 子句需要 `JOIN` 條件，除非子句是 `CROSS JOIN`，或其中一個聯結資料表是資料類型或陣列中的欄位。 |

### `WITH` 子句

BigQuery [`WITH`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw#with_clause) 子句包含一或多個具名的子查詢，當後續的 `SELECT` 陳述式參照這些子查詢時，子查詢即會執行。Amazon Redshift [`WITH`](https://docs.aws.amazon.com/redshift/latest/dg/r_WITH_clause.html) 子句的行為與 BigQuery 相同，但您可以評估子句一次，並重複使用其結果。

### 集合運算子

[Amazon Redshift 集合作業](https://docs.aws.amazon.com/redshift/latest/dg/r_UNION.html#r_UNION-order-of-evaluation-for-set-operators)與 [BigQuery 集合作業](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw#set_operators)之間存在些許差異。不過，Amazon Redshift 中所有可行的集合作業，都可以在 BigQuery 中複製。

| **Amazon Redshift** | **BigQuery** |
| --- | --- |
| `SELECT * FROM table1   UNION   SELECT * FROM table2` | `SELECT * FROM table1   UNION DISTINCT   SELECT * FROM table2`  注意：BigQuery 和 Amazon Redshift 都支援 `UNION ALL` 運算子。 |
| `SELECT * FROM table1   INTERSECT   SELECT * FROM table2` | `SELECT * FROM table1   INTERSECT DISTINCT   SELECT * FROM table2` |
| `SELECT * FROM table1   EXCEPT   SELECT * FROM table2` | `SELECT * FROM table1   EXCEPT DISTINCT   SELECT * FROM table2` |
| `SELECT * FROM table1   MINUS   SELECT * FROM table2` | `SELECT * FROM table1   EXCEPT DISTINCT   SELECT * FROM table2` |
| `SELECT * FROM table1   UNION   SELECT * FROM table2   EXCEPT   SELECT * FROM table3` | `SELECT * FROM table1   UNION ALL   (   SELECT * FROM table2   EXCEPT   SELECT * FROM table3   )`   注意：BigQuery 需要使用半形括號分隔不同的集合運算。如果重複使用相同的集合運算子，則不需要括號。 |

### `ORDER BY` 子句

Amazon Redshift [`ORDER BY`](https://docs.amazonaws.cn/en_us/redshift/latest/dg/r_ORDER_BY_clause.html) 子句與 BigQuery [`ORDER BY`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw#order_by_clause) 子句之間有些許差異。

| Amazon Redshift | BigQuery |
| --- | --- |
| 在 Amazon Redshift 中，`NULL` 預設會排在最後 (遞增順序)。 | 在 BigQuery 中，`NULL` 預設會依遞增順序排序。 |
| `SELECT *   FROM table   ORDER BY expression   LIMIT ALL` | `SELECT *   FROM table   ORDER BY expression`     注意：BigQuery 不會使用 `LIMIT ALL` 語法，但預設會排序所有資料列，因此行為與 Amazon Redshift 的 `LIMIT ALL` 子句相同。`ORDER BY`強烈建議在每個 `LIMIT` 子句中加入 `ORDER BY` 子句。不必要地排序所有結果列會降低查詢執行效能。 |
| `SELECT *   FROM table   ORDER BY expression   OFFSET 10` | `SELECT *   FROM table   ORDER BY expression   LIMIT count OFFSET 10`     注意：在 BigQuery 中，`OFFSET` 必須與 `LIMIT` *count* 一起使用。請務必將 *count* `INT64` 值設為必要最低訂購列數。 不必要地排序所有結果列會降低查詢執行效能。 |

### 條件

下表列出 [Amazon Redshift 條件](https://docs.aws.amazon.com/redshift/latest/dg/r_conditions.html) (或述詞)，這些條件是 Amazon Redshift 專屬，必須轉換為 BigQuery 對等項目。

| **Amazon Redshift** | **BigQuery** |
| --- | --- |
| `a = ANY (subquery)`  `a = SOME (subquery)` | `a IN subquery` |
| `a <> ALL (subquery)`  `a != ALL (subquery)` | `a NOT IN subquery` |
| `a IS UNKNOWN`  `expression ILIKE pattern` | `a IS NULL`  `LOWER(expression) LIKE LOWER(pattern)` |
| `expression LIKE pattern ESCAPE 'escape_char'` | `expression LIKE pattern`   注意：BigQuery 不支援自訂逸出字元。您必須使用雙反斜線 \\ 做為 BigQuery 的逸出字元。 |
| `expression [NOT] SIMILAR TO pattern` | `IF(   LENGTH(   REGEXP_REPLACE(   expression,   pattern,   ''   ) = 0,   True,   False   )`   注意：如已指定 `NOT`，請將上述 `IF` 運算式包裝在 `NOT` 運算式中，如下所示：    `NOT(   IF(   LENGTH(...   )` |
| `expression [!] ~ pattern` | `[NOT] REGEXP_CONTAINS(   expression,   regex   )` |

## 函式

以下各節列出 Amazon Redshift 函式及其 BigQuery 對應函式。

### 匯總函式

下表列出常見的 Amazon Redshift 匯總、匯總分析和近似匯總函式，以及對應的 BigQuery 函式。

| Amazon Redshift | BigQuery |
| --- | --- |
| `APPROXIMATE COUNT(DISTINCT expression)` | `APPROX_COUNT_DISTINCT(expression)` |
| `APPROXIMATE PERCENTILE_DISC(   percentile   ) WITHIN GROUP (ORDER BY expression)` | `APPROX_QUANTILES(expression, 100)  [OFFSET(CAST(TRUNC(percentile * 100) as INT64))]` |
| `AVG([DISTINCT] expression)` | `AVG([DISTINCT] expression)` |
| `COUNT(expression)` | `COUNT(expression)` |
| `LISTAGG(   [DISTINCT] aggregate_expression   [, delimiter] )  [WITHIN GROUP (ORDER BY order_list)]` | `STRING_AGG(   [DISTINCT] aggregate_expression   [, delimiter]   [ORDER BY order_list] )` |
| `MAX(expression)` | `MAX(expression)` |
| `MEDIAN(median_expression)` | `PERCENTILE_CONT( median_expression, 0.5 ) OVER()` |
| `MIN(expression)` | `MIN(expression)` |
| `PERCENTILE_CONT(   percentile   ) WITHIN GROUP (ORDER BY expression)` | `PERCENTILE_CONT(   median_expression,   percentile   ) OVER()`     注意：不涵蓋匯總應用實例。 |
| `STDDEV([DISTINCT] expression)` | `STDDEV([DISTINCT] expression)` |
| `STDDEV_SAMP([DISTINCT] expression)` | `STDDEV_SAMP([DISTINCT] expression)` |
| `STDDEV_POP([DISTINCT] expression)` | `STDDEV_POP([DISTINCT] expression)` |
| `SUM([DISTINCT] expression)` | `SUM([DISTINCT] expression)` |
| `VARIANCE([DISTINCT] expression)` | `VARIANCE([DISTINCT] expression)` |
| `VAR_SAMP([DISTINCT] expression)` | `VAR_SAMP([DISTINCT] expression)` |
| `VAR_POP([DISTINCT] expression)` | `VAR_POP([DISTINCT] expression)` |

BigQuery 也提供下列[匯總](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/aggregate_functions?hl=zh-tw)、[匯總分析](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/aggregate_analytic_functions?hl=zh-tw)和[近似匯總](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/approximate_aggregate_functions?hl=zh-tw)函式，這些函式在 Amazon Redshift 中沒有直接對應的函式：

* [`ANY_VALUE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/aggregate_functions?hl=zh-tw#any_value)
* [`APPROX_TOP_COUNT`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/approximate_aggregate_functions?hl=zh-tw#approx_top_count)
* [`APPROX_TOP_SUM`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/approximate_aggregate_functions?hl=zh-tw#approx_top_sum)
* [`ARRAY_AGG`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/aggregate_functions?hl=zh-tw#array_agg)
* [`ARRAY_CONCAT_AGG`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/aggregate_functions?hl=zh-tw#array_concat_agg)
* [`COUNTIF`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/aggregate_functions?hl=zh-tw#countif)
* [`CORR`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/statistical_aggregate_functions?hl=zh-tw#corr)
* [`COVAR_POP`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/statistical_aggregate_functions?hl=zh-tw#covar_pop)
* [`COVAR_SAMP`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/statistical_aggregate_functions?hl=zh-tw#covar_samp)

### 位元匯總函式

下表列出常見的 Amazon Redshift 位元聚合函式及其對應的 BigQuery 函式。

| **Amazon Redshift** | **BigQuery** |
| --- | --- |
| `BIT_AND(expression)` | `BIT_AND(expression)` |
| `BIT_OR(expression)` | `BIT_OR(expression)` |
| `BOOL_AND>(expression)` | `LOGICAL_AND(expression)` |
| `BOOL_OR(expression)` | `LOGICAL_OR(expression)` |

BigQuery 也提供下列[位元匯總](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bit_functions?hl=zh-tw)函式，Amazon Redshift 沒有直接對應的函式：

* [`BIT_XOR`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/aggregate_functions?hl=zh-tw#bit_xor)

### 窗型函式

下表列出常見的 Amazon Redshift 視窗函式及其對應的 BigQuery 函式。BigQuery 中的視窗函式包括[分析匯總函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/aggregate_analytic_functions?hl=zh-tw)、[匯總函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/aggregate_functions?hl=zh-tw)、[導覽函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/navigation_functions?hl=zh-tw)和[編號函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/numbering_functions?hl=zh-tw)。

  

| **Amazon Redshift** | **BigQuery** |
| --- | --- |
| `AVG(expression) OVER   (  [PARTITION BY expr_list]  [ORDER BY order_list frame_clause]  )` | `AVG(expression) OVER   (  [PARTITION BY expr_list]   [ORDER BY order_list]   [frame_clause]   )` |
| `COUNT(expression) OVER   (   [PARTITION BY expr_list]   [ORDER BY order_list   frame_clause]   )` | `COUNT(expression) OVER   (   [PARTITION BY expr_list]   [ORDER BY order_list]   [frame_clause]   )` |
| `CUME_DIST() OVER   (   [PARTITION BY partition_expression]   [ORDER BY order_list]   )` | `CUME_DIST() OVER   (   [PARTITION BY partition_expression]   ORDER BY order_list   )` |
| `DENSE_RANK() OVER   (   [PARTITION BY expr_list]   [ORDER BY order_list]   )` | `DENSE_RANK() OVER   (   [PARTITION BY expr_list]   ORDER BY order_list   )` |
| `FIRST_VALUE(expression) OVER  (   [PARTITION BY expr_list]   [ORDER BY order_list   frame_clause]   )` | `FIRST_VALUE(expression) OVER   (   [PARTITION BY expr_list]   [ORDER BY order_list]   [frame_clause]   )` |
| `LAST_VALUE(expression) OVER   (   [PARTITION BY expr_list]   [ORDER BY order_list   frame_clause]   )` | `LAST_VALUE(expression) OVER   (   [PARTITION BY expr_list]   [ORDER BY order_list   frame_clause]   )` |
| `LAG(value_expr [, offset]) OVER  (   [PARTITION BY window_partition]  ORDER BY window_ordering   )` | `LAG(value_expr [, offset]) OVER   (   [PARTITION BY window_partition]   ORDER BY window_ordering   )` |
| `LEAD(value_expr [, offset]) OVER  (   [PARTITION BY window_partition]   ORDER BY window_ordering   )` | `LEAD(value_expr [, offset]) OVER  (   [PARTITION BY window_partition]   ORDER BY window_ordering   )` |
| `LISTAGG(  [DISTINCT] expression  [, delimiter]   )  [WITHIN GROUP  (ORDER BY order_list)]  OVER (  [PARTITION BY partition_expression] )` | `STRING_AGG(  [DISTINCT] aggregate_expression  [, delimiter] )   OVER (   [PARTITION BY partition_list]   [ORDER BY order_list] )` |
| `MAX(expression) OVER   (   [PARTITION BY expr_list]   [ORDER BY order_list   frame_clause]   )` | `MAX(expression) OVER   (   [PARTITION BY expr_list]   [ORDER BY order_list]   [frame_clause]   )` |
| `MEDIAN(median_expression) OVER  (   [PARTITION BY partition_expression] )` | `PERCENTILE_CONT(   median_expression,   0.5   )  OVER ( [PARTITION BY partition_expression] )` |
| `MIN(expression) OVER   (   [PARTITION BY expr_list]   [ORDER BY order_list   frame_clause]   )` | `MIN(expression) OVER   (   [PARTITION BY expr_list]   [ORDER BY order_list]   [frame_clause]   )` |
| `NTH_VALUE(expression, offset) OVER ( [PARTITION BY window_partition] [ORDER BY window_ordering frame_clause] )` | `NTH_VALUE(expression, offset) OVER   (   [PARTITION BY window_partition]  ORDER BY window_ordering   [frame_clause]   )` |
| `NTILE(expr) OVER   (   [PARTITION BY expression_list]   [ORDER BY order_list]   )` | `NTILE(expr) OVER   (   [PARTITION BY expression_list]  ORDER BY order_list   )` |
| `PERCENT_RANK() OVER   (   [PARTITION BY partition_expression]  [ORDER BY order_list]   )` | `PERCENT_RANK() OVER   (   [PARTITION BY partition_expression]  ORDER BY order_list   )` |
| `PERCENTILE_CONT(percentile)   WITHIN GROUP (ORDER BY expr) OVER  (   [PARTITION BY expr_list] )` | `PERCENTILE_CONT(expr, percentile) OVER  (   [PARTITION BY expr_list] )` |
| `PERCENTILE_DISC(percentile) WITHIN GROUP (ORDER BY expr) OVER  (   [PARTITION BY expr_list]   )` | `PERCENTILE_DISC(expr, percentile) OVER  (   [PARTITION BY expr_list] )` |
| `RANK() OVER   (   [PARTITION BY expr_list]   [ORDER BY order_list]   )` | `RANK() OVER   (   [PARTITION BY expr_list]   ORDER BY order_list   )` |
| `RATIO_TO_REPORT(ratio_expression) OVER  (   [PARTITION BY partition_expression] )` | `ratio_expression SUM(ratio_expression) OVER   (   [PARTITION BY partition_expression] )` |
| `ROW_NUMBER() OVER   (   [PARTITION BY expr_list]   [ORDER BY order_list]   )` | `ROW_NUMBER() OVER   (   [PARTITION BY expr_list]   [ORDER BY order_list]   )` |
| `STDDEV(expression) OVER   (   [PARTITION BY expr_list]  [ORDER BY order_list  frame_clause]  )` | `STDDEV(expression) OVER  (  [PARTITION BY expr_list]  [ORDER BY order_list]  [frame_clause] )` |
| `STDDEV_SAMP(expression) OVER  (  [PARTITION BY expr_list]  [ORDER BY order_list  frame_clause]  )` | `STDDEV_SAMP(expression) OVER  (  [PARTITION BY expr_list]  [ORDER BY order_list]  [frame_clause]  )` |
| `STDDEV_POP(expression) OVER  (  [PARTITION BY expr_list]  [ORDER BY order_list]  [frame_clause]  )` | `STDDEV_POP(expression) OVER  (  [PARTITION BY expr_list]  [ORDER BY order_list]  [frame_clause] )` |
| `SUM(expression) OVER  (  [PARTITION BY expr_list]  [ORDER BY order_list]  [frame_clause]  )` | `SUM(expression) OVER  (  [PARTITION BY expr_list]  [ORDER BY order_list]  [frame_clause]  )` |
| `VAR_POP(expression) OVER  (  [PARTITION BY expr_list]  [ORDER BY order_list]  [frame_clause]  )` | `VAR_POP(expression) OVER  (  [PARTITION BY expr_list]  [ORDER BY order_list] [frame_clause]  )` |
| `VAR_SAMP(expression) OVER  (  [PARTITION BY expr_list]  [ORDER BY order_list]  [frame_clause]  )` | `VAR_SAMP(expression) OVER  (  [PARTITION BY expr_list]  [ORDER BY order_list]  [frame_clause]  )` |
| `VARIANCE(expression) OVER  (  [PARTITION BY expr_list]  [ORDER BY order_list]  [frame_clause]  )` | `VARIANCE(expression) OVER  (  [PARTITION BY expr_list]  [ORDER BY order_list]  [frame_clause]  )` |

### 條件運算式

下表顯示常見的 Amazon Redshift 條件運算式與 BigQuery 對應項之間的對應。

| **Amazon Redshift** | **BigQuery** |
| --- | --- |
| `CASEexpression  WHEN value THEN result  [WHEN...]  [ELSE else_result]  END` | `CASE expression  WHEN value THEN result  [WHEN...]  [ELSE else_result]  END` |
| `COALESCE(expression1[, ...])` | `COALESCE(expression1[, ...])` |
| `DECODE(  expression,  search1, result1  [, search2, result2...]  [, default]  )` | `CASE expression  WHEN value1 THEN result1  [WHEN value2 THEN result2]  [ELSE default]  END` |
| `GREATEST(value [, ...])` | `GREATEST(value [, ...])` |
| `LEAST(value [, ...])` | `LEAST(value [, ...])` |
| `NVL(expression1[, ...])` | `COALESCE(expression1[, ...])` |
| `NVL2(  expression,  not_null_return_value,  null_return_value  )` | `IF(  expression IS NULL,  null_return_value,  not_null_return_value  )` |
| `NULLIF(expression1, expression2)` | `NULLIF(expression1, expression2)` |

BigQuery 也提供下列條件運算式，這些運算式在 Amazon Redshift 中沒有直接對應的項目：

* [`IF`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/conditional_expressions?hl=zh-tw#if)
* [`IFNULL`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/conditional_expressions?hl=zh-tw#ifnull)

### 日期和時間函式

下表列出常見的 Amazon Redshift 日期和時間函式，以及對應的 BigQuery 函式。BigQuery 的日期和時間函式包括[日期函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/date_functions?hl=zh-tw)、[日期時間](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/datetime_functions?hl=zh-tw)
[函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/datetime_functions?hl=zh-tw)、[時間函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/time_functions?hl=zh-tw)和[時間戳記函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/timestamp_functions?hl=zh-tw)。

請注意，Amazon Redshift 和 BigQuery 中看似相同的函式可能會傳回不同的資料類型。

| Amazon Redshift | BigQuery |
| --- | --- |
| `ADD_MONTHS( date,  integer )` |  |