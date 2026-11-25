Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [參考資料](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# Apache Hive SQL 翻譯指南

本文詳細說明 Apache Hive 和 BigQuery 之間 SQL 語法的異同，協助您規劃遷移作業。如要大量遷移 SQL 指令碼，請使用[批次 SQL 轉譯](https://docs.cloud.google.com/bigquery/docs/batch-sql-translator?hl=zh-tw)。如要翻譯臨時查詢，請使用[互動式 SQL 翻譯](https://docs.cloud.google.com/bigquery/docs/interactive-sql-translator?hl=zh-tw)。

在某些情況下，Hive 和 BigQuery 中的 SQL 元素之間沒有直接對應關係。不過，在大多數情況下，BigQuery 會提供 Hive 的替代元素，協助您達成相同功能，如本文件中的範例所示。

本文件的目標對象為企業架構師、資料庫管理員、應用程式開發人員和 IT 安全性專家。並假設您熟悉 Hive。

## 資料類型

Hive 和 BigQuery 採用不同的資料類型系統。在多數情況下，您可以將 Hive 中的資料類型對應至 [BigQuery 資料類型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw)，但有少數例外狀況，例如 `MAP` 和 `UNION`。Hive 支援的隱含類型轉換比 BigQuery 多。因此，批次 SQL 翻譯器會插入許多明確轉換。

| **Hive** | **BigQuery** |
| --- | --- |
| `TINYINT` | `INT64` |
| `SMALLINT` | `INT64` |
| `INT` | `INT64` |
| `BIGINT` | `INT64` |
| `DECIMAL` | `NUMERIC` |
| `FLOAT` | `FLOAT64` |
| `DOUBLE` | `FLOAT64` |
| `BOOLEAN` | `BOOL` |
| `STRING` | `STRING` |
| `VARCHAR` | `STRING` |
| `CHAR` | `STRING` |
| `BINARY` | `BYTES` |
| `DATE` | `DATE` |
| - | `DATETIME` |
| - | `TIME` |
| `TIMESTAMP` | `DATETIME/TIMESTAMP` |
| `INTERVAL` | - |
| `ARRAY` | `ARRAY` |
| `STRUCT` | `STRUCT` |
| `MAPS` | `STRUCT` 搭配鍵/值 (`REPEAT` 欄位) |
| `UNION` | `STRUCT` (不同類型) |
| - | `GEOGRAPHY` |
| - | `JSON` |

## 查詢語法

本節說明 Hive 和 BigQuery 之間的查詢語法差異。

### `SELECT` 陳述式

大多數 Hive [`SELECT`](https://cwiki.apache.org/confluence/display/hive/languagemanual+select#LanguageManualSelect-SelectSyntax) 陳述式都與 BigQuery 相容。下表列出細微差異：

| **充電盒** | **Hive** | **BigQuery** |
| --- | --- | --- |
| 子查詢 | `SELECT * FROM (   SELECT 10 as col1, "test" as col2, "test" as col3   ) tmp_table;` | `SELECT * FROM (   SELECT 10 as col1, "test" as col2, "test" as col3   );` |
| 資料欄篩選 | `` SET hive.support.quoted.identifiers=none;   SELECT `(col2|col3)?+.+` FROM (   SELECT 10 as col1, "test" as col2, "test" as col3   ) tmp_table; `` | `SELECT * EXCEPT(col2,col3) FROM (   SELECT 10 as col1, "test" as col2, "test" as col3   );` |
| 展開陣列 | `SELECT tmp_table.pageid, adid FROM (   SELECT 'test_value' pageid, Array(1,2,3) ad_id) tmp_table   LATERAL VIEW   explode(tmp_table.ad_id) adTable AS adid;` | `SELECT tmp_table.pageid, ad_id FROM (  SELECT 'test_value' pageid, [1,2,3] ad_id) tmp_table,   UNNEST(tmp_table.ad_id) ad_id;` |

### `FROM` 子句

查詢中的 `FROM` 子句會列出選取資料的資料表參照。在 Hive 中，可能的資料表參照包括資料表、檢視表和子查詢。BigQuery 也支援所有這些資料表參照。

您可以使用下列方式，在 `FROM` 子句中參照 BigQuery 資料表：

* `[project_id].[dataset_id].[table_name]`
* `[dataset_id].[table_name]`
* `[table_name]`

BigQuery 也支援[其他資料表參照](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw#from_clause)：

* 使用 [`FOR SYSTEM_TIME AS OF`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw#for_system_time_as_of) 的資料表定義和資料列歷來版本
* [欄位路徑](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw#field_path)，或任何解析為資料類型中欄位的路徑 (例如 `STRUCT`)
* [扁平化陣列](https://docs.cloud.google.com/bigquery/docs/arrays?hl=zh-tw#querying_nested_arrays)

### 比較運算子

下表詳細說明如何將運算子從 Hive 轉換為 BigQuery：

| **函式或運算子** | **Hive** | **BigQuery** |
| --- | --- | --- |
| `-` 一元減號   `*` 乘法   `/` 除法   `+` 加法   `-` 減法 | 所有[數字類型](https://cwiki.apache.org/confluence/display/Hive/LanguageManual+Types#LanguageManualTypes-NumericTypes) | 所有[數字類型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#numeric_types)。  為避免除法運算期間發生錯誤，建議您使用 `SAFE_DIVIDE` 或 `IEEE_DIVIDE`。 |
| `~` 位元 NOT   `|` 位元 OR   `&` 位元 AND   `^` 位元 XOR | 布林值資料類型 | 布林值資料類型。 |
| 左移 | `shiftleft(TINYINT|SMALLINT|INT a, INT b)  shiftleft(BIGINT a, INT b)` | `<<`  整數或位元組  `A << B`，其中 `B` 必須與 `A` 屬於相同類型 |
| 右移 | `shiftright(TINYINT|SMALLINT|INT a, INT b)  shiftright(BIGINT a, INT b)` | `>>` 整數或位元組  `A >> B`，其中 `B` 必須與 `A` 屬於相同類型 |
| 模數 (餘數) | `X % Y`  所有[數字類型](https://cwiki.apache.org/confluence/display/Hive/LanguageManual+Types#LanguageManualTypes-NumericTypes) | `MOD(X, Y)` |
| 整數除法 | `A DIV B` 和 `A/B`，可提供精確的詳細資料 | 所有[數字類型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#numeric_types)。  注意：為避免在除法運算期間發生錯誤，建議您使用 `SAFE_DIVIDE` 或 `IEEE_DIVIDE`。 |
| 一元否定 | `!`、`NOT` | `NOT` |
| 支援等式比較的類型 | 所有[原始類型](https://cwiki.apache.org/confluence/display/Hive/LanguageManual+Types#LanguageManualTypes-Overview) | 所有[可比較的類型和 `STRUCT`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw)。 |
|  | `a <=> b` | 不支援。翻譯成以下語言：  `(a = b AND b IS NOT NULL OR a IS NULL)` |
|  | `a <> b` | 不支援。翻譯成以下語言：  `NOT (a = b AND b IS NOT NULL OR a IS NULL)` |
| 關係運算子 ( `=, ==, !=, <, >, >=` ) | 所有[原始類型](https://cwiki.apache.org/confluence/display/Hive/LanguageManual+UDF#LanguageManualUDF-RelationalOperators) | 所有[可比較類型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/operators?hl=zh-tw#comparison_operators)。 |
| 字串比較 | `RLIKE`，`REGEXP` | `REGEXP_CONTAINS` 內建函式。使用 BigQuery [字串函式的規則運算式語法](https://github.com/google/re2/wiki/Syntax)，建立規則運算式模式。 |
| `[NOT] LIKE, [NOT] BETWEEN, IS [NOT] NULL` | `A [NOT] BETWEEN B AND C, A IS [NOT] (TRUE|FALSE), A [NOT] LIKE B` | 與 Hive 相同。此外，BigQuery 也支援 [`IN` 運算子](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/operators?hl=zh-tw#in_operators)。 |

### JOIN 條件

Hive 和 BigQuery 都支援下列類型的 join：

* `[INNER] JOIN`
* `LEFT [OUTER] JOIN`
* `RIGHT [OUTER] JOIN`
* `FULL [OUTER] JOIN`
* `CROSS JOIN` 和等效的隱含[逗號 cross join](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw#cross_join)

詳情請參閱「[彙整作業](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw#join_types)」和「[Hive 彙整](https://cwiki.apache.org/confluence/display/hive/languagemanual+joins)」。

### 類型轉換和轉型

下表提供將函式從 Hive 轉換為 BigQuery 的詳細資料：

| **函式或運算子** | **Hive** | **BigQuery** |
| --- | --- | --- |
| 類型轉換 | 如果轉換失敗，系統會傳回 `NULL`。 | 語法與 Hive 相同。如要進一步瞭解 BigQuery 類型轉換規則，請參閱「[轉換規則](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/conversion_rules?hl=zh-tw)」。  如果投放失敗，系統會顯示錯誤。如要採用與 Hive 相同的行為，請改用 `SAFE_CAST`。 |
| `SAFE` 次函式呼叫 |  | 如果在函式呼叫前加上 [`SAFE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/functions-reference?hl=zh-tw#safe_prefix)，函式會傳回 `NULL`，而不是回報失敗。例如，`SAFE.SUBSTR('foo', 0, -2) AS safe_output;` 會傳回 `NULL`。  注意：如要安全轉換且不發生錯誤，請使用 `SAFE_CAST`。 |

#### 隱含轉換類型

遷移至 BigQuery 時，您需要將大部分的 [Hive 隱含轉換](https://cwiki.apache.org/confluence/display/hive/languagemanual+types#LanguageManualTypes-AllowedImplicitConversions)轉換為 BigQuery 明確轉換，但下列 BigQuery 隱含轉換的資料類型除外。

| **從 BigQuery 類型** | **轉換為 BigQuery 類型** |
| --- | --- |
| `INT64` | `FLOAT64`、`NUMERIC`、`BIGNUMERIC` |
| `BIGNUMERIC` | `FLOAT64` |
| `NUMERIC` | `BIGNUMERIC`、`FLOAT64` |

BigQuery 也會對下列常值執行隱含轉換：

| **從 BigQuery 類型** | **轉換為 BigQuery 類型** |
| --- | --- |
| `STRING` 常值 (例如 `"2008-12-25"`) | `DATE` |
| `STRING` 常值 (例如 `"2008-12-25 15:30:00"`) | `TIMESTAMP` |
| `STRING` 常值 (例如 `"2008-12-25T07:30:00"`) | `DATETIME` |
| `STRING` 常值 (例如 `"15:30:00"`) | `TIME` |

#### 明確轉換類型

如要轉換 BigQuery 不會隱含轉換的 Hive 資料類型，請使用 BigQuery [`CAST(expression AS type)` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/conversion_functions?hl=zh-tw#cast)。

## 函式

本節將說明 Hive 和 BigQuery 中常用的函式。

### 匯總函式

下表列出常見 Hive 匯總、統計匯總和近似匯總函式與 BigQuery 對應函式之間的對應關係：

| **Hive** | **BigQuery** |
| --- | --- |
| `count(DISTINCT expr[, expr...])` | `count(DISTINCT expr[, expr...])` |
| `percentile_approx(DOUBLE col, array(p1 [, p2]...) [, B]) WITHIN GROUP (ORDER BY expression)` | `APPROX_QUANTILES(expression, 100)[OFFSET(CAST(TRUNC(percentile * 100) as INT64))]`  BigQuery 不支援 Hive 定義的其他引數。 |
| `AVG` | `AVG` |
| `X | Y` | `BIT_OR / X | Y` |
| `X ^ Y` | `BIT_XOR / X ^ Y` |
| `X & Y` | `BIT_AND / X & Y` |
| `COUNT` | `COUNT` |
| `COLLECT_SET(col), \ COLLECT_LIST(col`) | `ARRAY_AGG(col)` |
| `COUNT` | `COUNT` |
| `MAX` | `MAX` |
| `MIN` | `MIN` |
| `REGR_AVGX` | `AVG(` `IF(dep_var_expr is NULL`  `OR ind_var_expr is NULL,`  `NULL, ind_var_expr)`  `)` |
| `REGR_AVGY` | `AVG(` `IF(dep_var_expr is NULL`  `OR ind_var_expr is NULL,`  `NULL, dep_var_expr)`  `)` |
| `REGR_COUNT` | `SUM(` `IF(dep_var_expr is NULL`  `OR ind_var_expr is NULL,`  `NULL, 1)`  `)` |
| `REGR_INTERCEPT` | `AVG(dep_var_expr)`  `- AVG(ind_var_expr)`  `* (COVAR_SAMP(ind_var_expr,dep_var_expr)`  `/ VARIANCE(ind_var_expr)`  `)` |
| `REGR_R2` | `(COUNT(dep_var_expr) *` `SUM(ind_var_expr * dep_var_expr) -`  `SUM(dep_var_expr) * SUM(ind_var_expr))`  `/ SQRT(`  `(COUNT(ind_var_expr) *`  `SUM(POWER(ind_var_expr, 2)) *`  `POWER(SUM(ind_var_expr),2)) *`  `(COUNT(dep_var_expr) *`  `SUM(POWER(dep_var_expr, 2)) *`  `POWER(SUM(dep_var_expr), 2)))` |
| `REGR_SLOPE` | `COVAR_SAMP(ind_var_expr,` `dep_var_expr)`  `/ VARIANCE(ind_var_expr)` |
| `REGR_SXX` | `SUM(POWER(ind_var_expr, 2)) - COUNT(ind_var_expr) * POWER(AVG(ind_var_expr),2)` |
| `REGR_SXY` | `SUM(ind_var_expr*dep_var_expr) - COUNT(ind_var_expr) * AVG(ind) * AVG(dep_var_expr)` |
| `REGR_SYY` | `SUM(POWER(dep_var_expr, 2)) - COUNT(dep_var_expr) * POWER(AVG(dep_var_expr),2)` |
| `ROLLUP` | `ROLLUP` |
| `STDDEV_POP` | `STDDEV_POP` |
| `STDDEV_SAMP` | `STDDEV_SAMP, STDDEV` |
| `SUM` | `SUM` |
| `VAR_POP` | `VAR_POP` |</