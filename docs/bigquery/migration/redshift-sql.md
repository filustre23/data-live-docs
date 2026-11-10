Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [參考資料](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# Amazon Redshift SQL 翻譯指南

本文詳細說明 Amazon Redshift 和 BigQuery 在 SQL 語法方面的異同，協助您規劃遷移作業。使用[批次 SQL 翻譯](https://docs.cloud.google.com/bigquery/docs/batch-sql-translator?hl=zh-tw)大量遷移 SQL 指令碼，或使用[互動式 SQL 翻譯](https://docs.cloud.google.com/bigquery/docs/interactive-sql-translator?hl=zh-tw)翻譯臨時查詢。

本指南的目標對象為企業架構師、資料庫管理員、應用程式開發人員和 IT 安全性專家。並假設您熟悉 Amazon Redshift。

**注意：**在某些情況下，Amazon Redshift 和 BigQuery 的 SQL 元素之間沒有直接對應關係。不過，在大多數情況下，您可以使用替代方法在 BigQuery 中實現與 Amazon Redshift 相同的功能，如本文件中的範例所示。

## 資料類型

本節說明 Amazon Redshift 和 BigQuery 資料類型之間的對應關係。

| **Amazon Redshift** | | **BigQuery** | **注意事項** |
| --- | --- | --- | --- |
| **資料類型** | **別名** | **資料類型** |  |
| `SMALLINT` | `INT2` | `INT64` | Amazon Redshift 的 `SMALLINT` 為 2 個位元組，而 BigQuery 的 `INT64` 為 8 個位元組。 |
| `INTEGER` | `INT, INT4` | `INT64` | Amazon Redshift 的 `INTEGER` 為 4 個位元組，而 BigQuery 的 `INT64` 為 8 個位元組。 |
| `BIGINT` | `INT8` | `INT64` | Amazon Redshift 的 `BIGINT` 和 BigQuery 的 `INT64` 都是 8 位元組。 |
| `DECIMAL` | `NUMERIC` | `NUMERIC` |  |
| `REAL` | `FLOAT4` | `FLOAT64` | Amazon Redshift 的 `REAL` 為 4 個位元組，而 BigQuery 的 `FLOAT64` 為 8 個位元組。 |
| `DOUBLE PRECISION` | `FLOAT8, FLOAT` | `FLOAT64` |  |
| `BOOLEAN` | `BOOL` | `BOOL` | Amazon Redshift 的 `BOOLEAN` 可使用 `TRUE`、`t`、`true`、`y`、`yes` 和 `1` 做為 true 的有效常值。BigQuery 的 `BOOL` 資料類型使用不區分大小寫的 `TRUE`。 |
| `CHAR` | `CHARACTER, NCHAR, BPCHAR` | `STRING` |  |
| `VARCHAR` | `CHARACTER VARYING, NVARCHAR, TEXT` | `STRING` |  |
| `DATE` |  | `DATE` |  |
| `TIMESTAMP` | `TIMESTAMP WITHOUT TIME ZONE` | `DATETIME` |  |
| `TIMESTAMPTZ` | `TIMESTAMP WITH TIME ZONE` | `TIMESTAMP` | 注意：在 BigQuery 中，剖析時間戳記或設定時間戳記的顯示格式時，會使用[時區](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#time_zones)。字串格式的時間戳記可能包含時區，但 BigQuery 剖析字串時，會以等效的 UTC 時間儲存時間戳記。如未明確指定時區，系統會使用預設時區 (世界標準時間)。系統支援[時區名稱](https://en.wikipedia.org/wiki/List_of_time_zone_abbreviations)或[與世界標準時間的時差](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/timestamp_functions?hl=zh-tw#timezone_definitions) (使用 (-|+)HH:MM)，但不支援 PDT 等時區縮寫。 |
| `GEOMETRY` |  | `GEOGRAPHY` | 支援查詢地理空間資料。 |

BigQuery 還有下列資料類型，沒有直接對應的 Amazon Redshift 類型：

* [`ARRAY`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#array_type)
* [`BYTES`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#bytes_type)
* [`TIME`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#time_type)
* [`STRUCT`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#struct_type)

### 隱含轉換類型

遷移至 BigQuery 時，您需要將大部分的 [Amazon Redshift 隱含轉換](https://docs.aws.amazon.com/redshift/latest/dg/c_Supported_data_types.html#r_Type_conversion)轉換為 BigQuery 的明確轉換，但下列資料類型除外，BigQuery 會隱含轉換這些資料類型。

BigQuery 會對下列資料類型執行隱含轉換：

| **從 BigQuery 類型** | **轉換為 BigQuery 類型** |
| --- | --- |
| `INT64` | `FLOAT64` |
| `INT64` | `NUMERIC` |
| `NUMERIC` | `FLOAT64` |

BigQuery 也會對下列常值執行隱含轉換：

| **從 BigQuery 類型** | **轉換為 BigQuery 類型** |
| --- | --- |
| `STRING` 常值   (例如「2008-12-25」) | `DATE` |
| `STRING` 常值   (例如「2008-12-25 15:30:00」) | `TIMESTAMP` |
| `STRING` 常值   (例如「2008-12-25T07:30:00」) | `DATETIME` |
| `STRING`常值   (例如「15:30:00」) | `TIME` |

### 明確轉換類型

您可以使用 BigQuery 的 [`CAST(expression AS type)`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/conversion_functions?hl=zh-tw#cast)  函式，或任何 [`DATE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/date_functions?hl=zh-tw) 和 [`TIMESTAMP`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/timestamp_functions?hl=zh-tw) 轉換函式，轉換 BigQuery 不會隱含轉換的 Amazon Redshift 資料類型。

遷移查詢時，請將所有 Amazon Redshift [`CONVERT(type, expression)`](https://docs.aws.amazon.com/redshift/latest/dg/r_CAST_function.html#convert-function) 函式 (或 :: 語法) 變更為 BigQuery 的 [`CAST(expression AS type)`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/conversion_functions?hl=zh-tw#cast) 函式，如「[資料類型格式設定函式](#data_type_formatting_functions)」一節的表格所示。

## 查詢語法

本節說明 Amazon Redshift 和 BigQuery 之間的查詢語法差異。

### `SELECT` 陳述式

大多數 Amazon Redshift [`SELECT`](https://docs.aws.amazon.com/redshift/latest/dg/r_SELECT_synopsis.html) 陳述式都與 BigQuery 相容。下表列出細微差異。

| **Amazon Redshift** | **BigQuery** |
| --- | --- |
| `SELECT TOP number expression   FROM table` | `SELECT expression   FROM table   ORDER BY expression DESC   LIMIT number` |
| `SELECT   x/total AS probability,   ROUND(100 * probability, 1) AS pct   FROM raw_data`     注意：Redshift 支援在同一個 `SELECT` 陳述式中建立及參照別名。 | `SELECT   x/total AS probability,   ROUND(100 * (x/total), 1) AS pct   FROM raw_data` |

BigQuery 也支援 `SELECT` 陳述式中的下列運算式，這些運算式沒有 Amazon Redshift 對等項目：

* [`EXCEPT`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw#select_except)
* [`REPLACE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw#select_replace)

### `FROM` 子句

查詢中的 [`FROM`](https://docs.aws.amazon.com/redshift/latest/dg/r_FROM_clause30.html) 子句會列出選取資料的資料表參照。在 Amazon Redshift 中，可能的資料表參照包括資料表、檢視表和子查詢。BigQuery 支援所有這些資料表參照。

您可以使用下列方式，在 `FROM` 子句中參照 BigQuery 資料表：

* `[project_id].[dataset_id].[table_name]`
* `[dataset_id].[table_name]`
* `[table_name]`

BigQuery 也支援其他資料表參照：

* 使用 [`FOR SYSTEM_TIME AS OF`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw#for_system_time_as_of) 查詢資料表定義和資料列的歷來版本。
* [欄位路徑](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw#field_path)，或任何解析為資料類型中欄位的路徑 (例如 `STRUCT`)。
* [扁平化陣列](https://docs.cloud.google.com/bigquery/docs/arrays?hl=zh-tw#querying_nested_arrays)。

### `JOIN` 種類型

Amazon Redshift 和 BigQuery 都支援下列類型的彙整：

* `[INNER] JOIN`
* `LEFT [OUTER] JOIN`
* `RIGHT [OUTER] JOIN`
* `FULL [OUTER] JOIN`
* `CROSS JOIN` 和等效的[隱含逗號 cross join](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw#cross_join)。

下表列出細微差異。

| **Amazon Redshift** | **BigQuery** |
| --- | --- |
| `SELECT col   FROM table1   NATURAL INNER JOIN   table2` | `SELECT col1   FROM table1   INNER JOIN   table2   USING (col1, col2 [, ...])`   注意：在 BigQuery 中，`JOIN` 子句需要 `JOIN` 條件，除非子句是 `CROSS JOIN`，或其中一個彙整資料表是資料類型或陣列中的欄位。 |

### `WITH` 子句

BigQuery [`WITH`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw#with_clause) 子句包含一或多個具名子查詢，會在後續 `SELECT` 陳述式參照時執行。Amazon Redshift [`WITH`](https://docs.aws.amazon.com/redshift/latest/dg/r_WITH_clause.html) 子句的行為與 BigQuery 相同，但您可以評估子句一次並重複使用其結果。

### 集合運算子

[Amazon Redshift 集合運算子](https://docs.aws.amazon.com/redshift/latest/dg/r_UNION.html#r_UNION-order-of-evaluation-for-set-operators)和 [BigQuery 集合](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw#set_operators)[運算子](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw#set_operators)之間有一些細微差異。不過，Amazon Redshift 中可行的所有集合運算，都可以在 BigQuery 中複製。

| **Amazon Redshift** | **BigQuery** |
| --- | --- |
| `SELECT * FROM table1   UNION   SELECT * FROM table2` | `SELECT * FROM table1   UNION DISTINCT   SELECT * FROM table2`  注意：BigQuery 和 Amazon Redshift 都支援 `UNION ALL` 運算子。 |
| `SELECT * FROM table1   INTERSECT   SELECT * FROM table2` | `SELECT * FROM table1   INTERSECT DISTINCT   SELECT * FROM table2` |
| `SELECT * FROM table1   EXCEPT   SELECT * FROM table2` | `SELECT * FROM table1   EXCEPT DISTINCT   SELECT * FROM table2` |
| `SELECT * FROM table1   MINUS   SELECT * FROM table2` | `SELECT * FROM table1   EXCEPT DISTINCT   SELECT * FROM table2` |
| `SELECT * FROM table1   UNION   SELECT * FROM table2   EXCEPT   SELECT * FROM table3` | `SELECT * FROM table1   UNION ALL   (   SELECT * FROM table2   EXCEPT   SELECT * FROM table3   )`   注意：BigQuery 規定必須使用括號分隔不同的集合運算。如果重複使用相同的集合運算子，則不需要使用括號。 |

### `ORDER BY` 子句

Amazon Redshift [`ORDER BY`](https://docs.amazonaws.cn/en_us/redshift/latest/dg/r_ORDER_BY_clause.html) 子句和 BigQuery [`ORDER BY`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw#order_by_clause) 子句之間有些許差異。

| Amazon Redshift | BigQuery |
| --- | --- |
| 在 Amazon Redshift 中，`NULL` 預設會排在最後 (遞增排序)。 | 在 BigQuery 中，`NULL` 預設會排在最前面 (遞增排序)。 |
| `SELECT *   FROM table   ORDER BY expression   LIMIT ALL` | `SELECT *   FROM table   ORDER BY expression`     注意：BigQuery 不會使用 `LIMIT ALL` 語法，但 `ORDER BY` 預設會排序所有資料列，因此行為與 Amazon Redshift 的 `LIMIT ALL` 子句相同。強烈建議在每個 `ORDER BY` 子句中加入 `LIMIT` 子句。不必要地排序所有結果列會降低查詢執行效能。 |
| `SELECT *   FROM table   ORDER BY expression   OFFSET 10` | `SELECT *   FROM table   ORDER BY expression   LIMIT count OFFSET 10`     注意：在 BigQuery 中，`OFFSET` 必須與 `LIMIT` *count* 搭配使用。請務必將 *count* `INT64` 值設為必要的最低排序資料列數。排序所有結果列   會不必要地降低查詢執行效能。 |

### 條件

下表列出 Amazon Redshift 專屬的 [Amazon Redshift 條件](https://docs.aws.amazon.com/redshift/latest/dg/r_conditions.html)或述詞，必須轉換為 BigQuery 對等項目。

| **Amazon Redshift** | **BigQuery** |
| --- | --- |
| `a = ANY (subquery)`  `a = SOME (subquery)` | `a IN subquery` |
| `a <> ALL (subquery)`  `a != ALL (subquery)` | `a NOT IN subquery` |
| `a IS UNKNOWN`  `expression ILIKE pattern` | `a IS NULL`  `LOWER(expression) LIKE LOWER(pattern)` |
| `expression LIKE pattern ESCAPE 'escape_char'` | `expression LIKE pattern`   注意：BigQuery 不支援自訂逸出字元。您必須使用兩個反斜線 \\ 做為 BigQuery 的逸出字元。 |
| `expression [NOT] SIMILAR TO pattern` | `IF(   LENGTH(   REGEXP_REPLACE(   expression,   pattern,   ''   ) = 0,   True,   False   )`   注意：如果指定 `NOT`，請將上述 `IF` 運算式包裝在 `NOT` 運算式中，如下所示：    `NOT(   IF(   LENGTH(...   )` |
| `expression` |