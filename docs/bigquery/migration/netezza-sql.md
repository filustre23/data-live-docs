Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [參考資料](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# IBM Netezza SQL 翻譯指南

IBM Netezza 資料倉儲技術專為與 Netezza 專屬的 SQL 語法搭配使用而設計。Netezza SQL 以 Postgres 7.2 為基礎，針對 Netezza 撰寫的 SQL 指令碼無法直接在 BigQuery 資料倉儲中使用，因為 SQL 方言不同。

本文詳述 Netezza 和 BigQuery 在下列領域的 SQL 語法相似與相異之處：

* 資料類型
* SQL 語言元素
* 查詢語法
* 資料操縱語言 (DML)
* 資料定義語言 (DDL)
* 預存程序
* 函式

您也可以使用[批次 SQL 翻譯](https://docs.cloud.google.com/bigquery/docs/batch-sql-translator?hl=zh-tw)大量遷移 SQL 指令碼，或使用[互動式 SQL 翻譯](https://docs.cloud.google.com/bigquery/docs/interactive-sql-translator?hl=zh-tw)翻譯臨時查詢。這兩項工具的[預先發布版](https://cloud.google.com/products?hl=zh-tw#product-launch-stages)都支援 IBM Netezza SQL/NZPLSQL。

## 資料類型

| **Netezza** | **BigQuery** | **附註** |
| --- | --- | --- |
| `INTEGER/INT/INT4` | [`INT64`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#integer_types) |  |
| `SMALLINT/INT2` | [`INT64`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#integer_types) |  |
| `BYTEINT/INT1` | [`INT64`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#integer_types) |  |
| `BIGINT/INT8` | [`INT64`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#integer_types) |  |
| `DECIMAL` | [`NUMERIC`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#numeric-type) | Netezza 中的 `DECIMAL` 資料類型是 `NUMERIC` 資料類型的別名。 |
| `NUMERIC`] | [`NUMERIC`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#numeric-type) [`INT64`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#integer_types) |  |
| `NUMERIC(p,s)` | [`NUMERIC`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#numeric-type) | BigQuery 中的 `NUMERIC` 類型不會強制執行自訂位數或比例界限 (限制)，這與 Netezza 不同。BigQuery 的小數點後位數固定為 9 位，而 Netezza 則允許自訂設定。在 Netezza 中，精確度 `p` 可介於 1 至 38 之間，而比例 `s` 則介於 0 至精確度之間。 |
| `FLOAT(p)` | [`FLOAT64`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#floating_point_types) |  |
| `REAL/FLOAT(6)` | [`FLOAT64`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#floating_point_types) |  |
| `DOUBLE PRECISION/FLOAT(14)` | [`FLOAT64`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#floating_point_types) |  |
| `CHAR/CHARACTER` | [`STRING`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/timestamp_functions?hl=zh-tw#string) | BigQuery 中的 `STRING` 類型為變數長度，不需要手動設定字元長度上限，這與 Netezza `CHARACTER` 和 `VARCHAR` 類型不同。`CHAR(n)` 中 `n` 的預設值為 1。字串大小上限為 64,000 個字元。 |
| `VARCHAR` | [`STRING`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/timestamp_functions?hl=zh-tw#string) | BigQuery 中的 `STRING` 類型為變數長度，不需要手動設定字元長度上限，這與 Netezza `CHARACTER` 和 `VARCHAR` 類型不同。字串大小上限為 64,000 個字元。 |
| `NCHAR` | [`STRING`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/timestamp_functions?hl=zh-tw#string) | BigQuery 中的 `STRING` 型別會儲存為變數長度 UTF-8 編碼的 Unicode。長度上限為 16,000 個字元。 |
| `NVARCHAR` | [`STRING`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/timestamp_functions?hl=zh-tw#string) | BigQuery 中的 `STRING` 類型會儲存為變數長度的 UTF-8 編碼 Unicode。長度上限為 16,000 個字元。 |
| `VARBINARY` | [`BYTES`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#bytes_type) |  |
| `ST_GEOMETRY` | [`GEOGRAPHY`](https://docs.cloud.google.com/bigquery/docs/gis-data?hl=zh-tw) |  |
| `BOOLEAN/BOOL` | [`BOOL`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#boolean_type) | BigQuery 中的 `BOOL` 類型只能接受 `TRUE/FALSE`，不像 Netezza 中的 `BOOL` 類型可以接受各種值，例如 `0/1`、`yes/no`、`true/false,` `on/off`。 |
| `DATE` | [`DATE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#date_type) |  |
| `TIME` | [`TIME`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#time_type) |  |
| `TIMETZ/TIME WITH TIME ZONE` | [`TIME`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#time_type) | Netezza 會以世界標準時間儲存 `TIME` 資料類型，並允許您使用 `WITH TIME ZONE` 語法傳遞與世界標準時間的時差。BigQuery 中的 `TIME` 資料類型代表時間，與任何日期或時區無關。 |
| `TIMESTAMP` | [`DATETIME`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#datetime_type) | Netezza `TIMESTAMP` 類型不含時區，與 BigQuery `DATETIME` 類型相同。 |
|  | [`ARRAY`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#array_type) | Netezza 中沒有陣列資料型別。陣列類型會改為儲存在 varchar 欄位中。 |

## 時間戳記和日期類型格式設定

將日期類型格式化元素從 Netezza 轉換為 GoogleSQL 時，請特別注意 `TIMESTAMP` 和 `DATETIME` 之間的時區差異，如下表所示：

| **Netezza** | **BigQuery** |
| --- | --- |
| `CURRENT_TIMESTAMP`  `CURRENT_TIME`    Netezza 中的 `TIME` 資訊可能包含不同的時區資訊，這些資訊是使用 `WITH TIME ZONE` 語法定義。 | 如有可能，請使用格式正確的 `CURRENT_TIMESTAMP` 函式。不過，輸出格式不一定會顯示 UTC 時區 (在內部，BigQuery 沒有時區)。bq 指令列工具和Google Cloud 控制台中的 `DATETIME` 物件會使用 `T` 分隔符號，根據 RFC 3339 格式化。不過，在 Python 和 Java JDBC 中，空格會做為分隔符。使用明確的 [`FORMAT_DATETIME`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/datetime_functions?hl=zh-tw#format_datetime) 函式，正確定義日期格式。否則，系統會明確轉換為字串，例如：  `CAST(CURRENT_DATETIME() AS STRING)`  這也會傳回空格分隔符。 |
| `CURRENT_DATE` | [`CURRENT_DATE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/date_functions?hl=zh-tw#current_date) |
| `CURRENT_DATE-3` | BigQuery 不支援算術資料運算。請改用 [`DATE_ADD`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/date_functions?hl=zh-tw#date_add) 函式。 |

## `SELECT` 陳述式

一般來說，Netezza `SELECT` 陳述式與 BigQuery 相容。下表列出例外狀況：

| **Netezza** | **BigQuery** |
| --- | --- |
| 不含 `FROM` 子句的 `SELECT` 陳述式 | 支援下列特殊情況： `SELECT 1 UNION ALL SELECT 2;` |
| ``` SELECT   (subquery) AS flag,   CASE WHEN flag = 1 THEN ... ``` | 在 BigQuery 中，資料欄無法參照在同一查詢中定義的其他資料欄輸出內容。您必須複製邏輯，或將邏輯移至巢狀查詢。 選項 1       ``` SELECT   (subquery) AS flag,   CASE WHEN (subquery) = 1 THEN ... ```     選項 2       ``` SELECT   q.*,   CASE WHEN flag = 1 THEN ... FROM (   SELECT     (subquery) AS flag,     ...   ) AS q ``` |

## 比較運算子

| **Netezza** | **BigQuery** | **說明** |
| --- | --- | --- |
| `exp = exp2` | [`exp = exp2`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/operators?hl=zh-tw#comparison_operators) | 等於 |
| `exp <= exp2` | [`exp <= exp2`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/operators?hl=zh-tw#comparison_operators) | 小於或等於 |
| `exp < exp2` | [`exp < exp2`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/operators?hl=zh-tw#comparison_operators) | 小於 |
| `exp <> exp2`  `exp != exp2` | [`exp <> exp2`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/operators?hl=zh-tw#comparison_operators)  [`exp != exp2`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/operators?hl=zh-tw#comparison_operators) | 不等於 |
| `exp >= exp2` | [`exp >= exp2`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/operators?hl=zh-tw#comparison_operators) | 大於或等於 |
| `exp > exp2` | [`exp > exp2`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/operators?hl=zh-tw#comparison_operators) | 大於 |

## 內建 SQL 函式

| **Netezza** | **BigQuery** | **說明** |
| --- | --- | --- |
| `CURRENT_DATE` | [`CURRENT_DATE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/date_functions?hl=zh-tw#current_date) | 取得目前日期 (年、月和日)。 |
| `CURRENT_TIME` | [`CURRENT_TIME`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/time_functions?hl=zh-tw#current_time) | 取得目前時間， 包含分數。 |
| `CURRENT_TIMESTAMP` | [`CURRENT_TIMESTAMP`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/timestamp_functions?hl=zh-tw#current_timestamp) | 取得目前系統日期和時間，精確度為整秒。 |
| `NOW` | [`CURRENT_TIMESTAMP`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/timestamp_functions?hl=zh-tw#current_timestamp) | 取得目前的系統日期和時間，精確度為秒。 |
| `COALESCE(exp, 0)` | [`COALESCE(exp, 0)`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/conditional_expressions?hl=zh-tw#coalesce) | 將 `NULL` 替換為零。 |
| `NVL(exp, 0)` | [`IFNULL(exp, 0)`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/conditional_expressions?hl=zh-tw#ifnull) | 將 `NULL` 替換為零。 |
| `EXTRACT(DOY FROM timestamp_expression)` | [`EXTRACT(DAYOFYEAR FROM timestamp_expression)`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/date_functions?hl=zh-tw#extract) | 傳回自年初算起的天數。 |
| `ADD_MONTHS(date_expr, num_expr)` | [`DATE_ADD(date, INTERVAL k MONTH)`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/date_functions?hl=zh-tw#date_add) | 在日期中新增月份。 |
| `DURATION_ADD(date, k)` | [`DATE_ADD(date, INTERVAL k DAY)`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/date_functions?hl=zh-tw#date_add) | 對日期執行加法運算。 |
| `DURATION_SUBTRACT(date, k)` | [`DATE_SUB(date, INTERVAL k DAY)`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/date_functions?hl=zh-tw#date_sub) | 對日期執行減法運算。 |
| `str1 || str2` | [`CONCAT(str1, str2)`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/string_functions?hl=zh-tw#concat) | 串連字串。 |

## 函式

本節比較 Netezza 和 BigQuery 函式。

### 匯總函式

| **Netezza** | **BigQuery** |
| --- | --- |
|  | [`ANY_VALUE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/aggregate_functions?hl=zh-tw#any_value) |
|  | [`APPROX_COUNT_DISTINCT`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/approximate_aggregate_functions?hl=zh-tw#approx_count_distinct) |
|  | [`APPROX_QUANTILES`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/approximate_aggregate_functions?hl=zh-tw#approx_quantiles) |
|  | [`APPROX_TOP_COUNT`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/approximate_aggregate_functions?hl=zh-tw#approx_top_count) |
|  | [`APPROX_TOP_SUM`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/approximate_aggregate_functions?hl=zh-tw#approx_top_sum) |
| `AVG` | [`AVG`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/aggregate_functions?hl=zh-tw#avg) |
| `intNand` | [`BIT_AND`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/aggregate_functions?hl=zh-tw#bit_and) |
| `intNnot` | 位元 NOT 運算子：[`~`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/operators?hl=zh-tw#bitwise_operators) |
| `intNor` | [`BIT_OR`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/aggregate_functions?hl=zh-tw#bit_or) |
| `intNxor` | [`BIT_XOR`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/aggregate_functions?hl=zh-tw#bit_xor) |
| `intNshl` |  |
| `intNshr` |  |
| `CORR` | [`CORR`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/statistical_aggregate_functions?hl=zh-tw#corr) |
| `COUNT` | [`COUNT`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/aggregate_functions?hl=zh-tw#count) |
|  | [`COUNTIF`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/aggregate_functions?hl=zh-tw#countif) |
| `COVAR_POP` | [`COVAR_POP`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/statistical_aggregate_functions?hl=zh-tw#covar_pop) |
| `COVAR_SAMP` | [`COVAR_SAMP`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/statistical_aggregate_functions?hl=zh-tw#covar_samp) |
| `GROUPING` |  |
|  | [`LOGICAL_AND`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/aggregate_functions?hl=zh-tw#logical_and) |
|  | [`LOGICAL_OR`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/aggregate_functions?hl=zh-tw#logical_or) |
| `MAX` | [`MAX`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/aggregate_functions?hl=zh-tw#max) |
| `MIN` | [`MIN`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/aggregate_functions?hl=zh-tw#min) |
| `MEDIAN` | [`PERCENTILE_CONT`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/navigation_functions?hl=zh-tw#percentile_cont)`(x, 0.5)` |
| `STDDEV_POP` | [`STDDEV_POP`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/statistical_aggregate_functions?hl=zh-tw#stddev_pop) |
| `STDDEV_SAMP` | [`STDDEV_SAMP`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/statistical_aggregate_functions?hl=zh-tw#stddev_samp)  [`STDDEV`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/statistical_aggregate_functions?hl=zh-tw#stddev) |
|  | [`STRING_AGG`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/aggregate_functions?hl=zh-tw#string_agg) |
| `SUM` | [`SUM`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/aggregate_functions?hl=zh-tw#sum) |
| `VAR_POP` | [`VAR_POP`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/statistical_aggregate_functions?hl=zh-tw#var_pop) |
| `VAR_SAMP` | [`VAR_SAMP`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/statistical_aggregate_functions?hl=zh-tw#var_samp)  [`VARIANCE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/statistical_aggregate_functions?hl=zh-tw#variance) |

### 分析函式

| **Netezza** | **BigQuery** |
| --- | --- |
|  | [`ANY_VALUE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/aggregate_functions?hl=zh-tw#any_value) |
|  | [`ARRAY_AGG`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/aggregate_functions?hl=zh-tw#array_agg) |
| `ARRAY_CONCAT` | [`ARRAY_CONCAT_AGG`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/aggregate_functions?hl=zh-tw#array_concat_agg) |
| `ARRAY_COMBINE` |  |
| `ARRAY_COUNT` |  |
| `ARRAY_SPLIT` |  |
| `ARRAY_TYPE` |  |
| `AVG` | [`AVG`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/aggregate_functions?hl=zh-tw#avg) |
| `intNand` | [`BIT_AND`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/aggregate_functions?hl=zh-tw#bit_and) |
| `intNnot` | 位元 NOT 運算子：[`~`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/operators?hl=zh-tw#bitwise_operators) |
| `intNor` | [`BIT_OR`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/aggregate_functions?hl=zh-tw#bit_or) |
| `intNxor` | [`BIT_XOR`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/aggregate_functions?hl=zh-tw#bit_xor) |
| `intNshl` |  |
| `intNshr` |  |
| `CORR` | [`CORR`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/statistical_aggregate_functions?hl=zh-tw#corr) |
| `COUNT` | [`COUNT`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/aggregate_functions?hl=zh-tw#count) |
|  | [`COUNTIF`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/aggregate_functions?hl=zh-tw#countif) |
| `COVAR_POP` | [`COVAR_POP`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/statistical_aggregate_functions?hl=zh-tw#covar_pop) |
| `COVAR_SAMP` | [`COVAR_SAMP`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/statistical_aggregate_functions?hl=zh-tw#covar_samp) |
| `CUME_DIST` | [`CUME_DIST`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/numbering_functions?hl=zh-tw#cume_dist) |
| `DENSE_RANK` | [`DENSE_RANK`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/numbering_functions?hl=zh-tw#dense_rank) |
| `FIRST_VALUE` | [`FIRST_VALUE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/navigation_functions?hl=zh-tw#first_value) |
| `LAG` | [`LAG`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/navigation_functions?hl=zh-tw#lag) |
| `LAST_VALUE` | [`LAST_VALUE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/navigation_functions?hl=zh-tw#last_value) |
| `LEAD` | [`LEAD`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/navigation_functions?hl=zh-tw#lead) |
| `AND` | [`LOGICAL_AND`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/aggregate_functions?hl=zh-tw#logical_and) |
| `OR` | [`LOGICAL_OR`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/aggregate_functions?hl=zh-tw#logical_or) |
| `MAX` | [`MAX`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/aggregate_functions?hl=zh-tw#max) |
| `MIN` | [`MIN`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/aggregate_functions?hl=zh-tw#min) |
|  | [`NTH_VALUE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/navigation_functions?hl=zh-tw#nth_value) |
| `NTILE` | [`NTILE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/numbering_functions?hl=zh-tw#ntile) |
| `PERCENT_RANK` | [`PERCENT_RANK`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/numbering_functions?hl=zh-tw#percent_rank) |
| `PERCENTILE_CONT` | [`PERCENTILE_CONT`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/navigation_functions?hl=zh-tw#percentile_cont) |
| `PERCENTILE_DISC` | [`PERCENTILE_DISC`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/navigation_functions?hl=zh-tw#percentile_disc) |
| `RANK` | [`RANK`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/numbering_functions?hl=zh-tw#rank) |
| `ROW_NUMBER` | [`ROW_NUMBER`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/numbering_functions?hl=zh-tw#row_number) |
| `STDDEV` | [`STDDEV`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/statistical_aggregate_functions?hl=zh-tw#stddev) |
| `STDDEV_POP` | [`STDDEV_POP`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/statistical_aggregate_functions?hl=zh-tw#stddev_pop) |
| `STDDEV_SAMP` | [`STDDEV_SAMP`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/statistical_aggregate_functions?hl=zh-tw#stddev_samp) |
|  | [`STRING_AGG`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/aggregate_functions?hl=zh-tw#string_agg) |
| `SUM` | [`SUM`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/aggregate_functions?hl=zh-tw#sum) |
| `VARIANCE` | [`VARIANCE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/statistical_aggregate_functions?hl=zh-tw#variance) |
| `VAR_POP` | [`VAR_POP`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/statistical_aggregate_functions?hl=zh-tw#var_pop) |
| `VAR_SAMP` | [`VAR_SAMP`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/statistical_aggregate_functions?hl=zh-tw#var_samp)  [`VARIANCE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/statistical_aggregate_functions?hl=zh-tw#variance) |
| `WIDTH_BUCKET` |  |

### 日期和時間函式

| **Netezza** | **BigQuery** |
| --- | --- |
| `ADD_MONTHS` | [`DATE_ADD`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/date_functions?hl=zh-tw#date_add)  [`TIMESTAMP_ADD`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/timestamp_functions?hl=zh-tw#timestamp_add) |
| `AGE` |  |
| `CURRENT_DATE` | [`CURRENT_DATE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/date_functions?hl=zh-tw#current_date) |
|  | [`CURRENT_DATETIME`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/datetime_functions?hl=zh-tw#current_datetime) |
| `CURRENT_TIME` | [`CURRENT_TIME`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/time_functions?hl=zh-tw#current_time) |
| `CURRENT_TIME(p)` |  |
| `CURRENT_TIMESTAMP` | [`CURRENT_TIMESTAMP`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/timestamp_functions?hl=zh-tw#current_timestamp) |
| `CURRENT_TIMESTAMP(p)` |  |
|  | [`DATE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/date_functions?hl=zh-tw#date) |
|  | [`DATE_ADD`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/date_functions?hl=zh-tw#date_add) |
|  | [`DATE_DIFF`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/date_functions?hl=zh-tw#date_diff) |
|  | [`DATE_FROM_UNIX_DATE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/date_functions?hl=zh-tw#date_from_unix_date) |
|  | [`DATE_SUB`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/date_functions?hl=zh-tw#date_sub) |
| `DATE_TRUNC` | [`DATE_TRUNC`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/date_functions?hl=zh-tw#date_trunc) |
| `DATE_PART` |  |
|  | [`DATETIME`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/datetime_functions?hl=zh-tw#datetime) |
|  | [`DATETIME_ADD`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/datetime_functions?hl=zh-tw#datetime_add) |
|  | [`DATETIME_DIFF`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/datetime_functions?hl=zh-tw#datetime_diff) |
|  | [`DATETIME_SUB`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/datetime_functions?hl=zh-tw#datetime_sub) |
|  | [`DATETIME_TRUNC`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/datetime_functions?hl=zh-tw#datetime_trunc) |
| `DURATION_ADD` |  |
| `DURATION_SUBTRACT` |  |
| `EXTRACT` | [`EXTRACT (DATE)`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/date_functions?hl=zh-tw#extract)  [`EXTRACT (TIMESTAMP)`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/timestamp_functions?hl=zh-tw#extract) |
|  | [`FORMAT_DATE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/date_functions?hl=zh-tw#format_date) |
|  | [`FORMAT_DATETIME`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/datetime_functions?hl=zh-tw#format_datetime) |
|  | [`FORMAT_TIME`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/time_functions?hl=zh-tw#format_time) |
|  | [`FORMAT_TIMESTAMP`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/timestamp_functions?hl=zh-tw#format_timestamp) |
| `LAST_DAY` | [`DATE_SUB`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/date_functions?hl=zh-tw#date_sub)`(` [`DATE_TRUNC`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/date_functions?hl=zh-tw#date_trunc)`(` [`DATE_ADD`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/date_functions?hl=zh-tw#date_add)`(` `date_expression, INTERVAL 1 MONTH ), MONTH ),` `INTERVAL 1 DAY )` |
| `MONTHS_BETWEEN` | [`DATE_DIFF`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/date_functions?hl=zh-tw#date_diff)`(date_expression,` `date_expression, MONTH)` |
| `NEXT_DAY` |  |
| `NOW` |  |
| `OVERLAPS` |  |
|  | [`PARSE_DATE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/date_functions?hl=zh-tw#parse_date) |
|  | [`PARSE_DATETIME`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/datetime_functions?hl=zh-tw#parse_datetime) |
|  | [`PARSE_TIME`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/time_functions?hl=zh-tw#parse_time) |
|  | [`PARSE_TIMESTAMP`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/timestamp_functions?hl=zh-tw#parse_timestamp) |
|  | [`STRING`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/timestamp_functions?hl=zh-tw#string) |
|  | [`TIME`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/time_functions?hl=zh-tw#time) |
|  | [`TIME_ADD`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/time_functions?hl=zh-tw#time_add) |
|  | [`TIME_DIFF`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/time_functions?hl=zh-tw#time_diff) |
|  | [`TIME_SUB`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/time_functions?hl=zh-tw#time_sub) |
|  | [`TIME_TRUNC`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/time_functions?hl=zh-tw#time_trunc) |
| `TIMEOFDAY` |  |
| `TIMESTAMP` | [`DATETIME`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/datetime_functions?hl=zh-tw#datetime) |
|  | [`TIMESTAMP_ADD`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/timestamp_functions?hl=zh-tw#timestamp_add) |
|  | [`TIMESTAMP_DIFF`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/timestamp_functions?hl=zh-tw#timestamp_diff) |
|  | [`TIMESTAMP_MICROS`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/timestamp_functions?hl=zh-tw#timestamp_micros) |
|  | [`TIMESTAMP_MILLIS`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/timestamp_functions?hl=zh-tw#timestamp_millis) |
|  | [`TIMESTAMP_SECONDS`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/timestamp_functions?hl=zh-tw#timestamp_seconds) |
|  | [`TIMESTAMP_SUB`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/timestamp_functions?hl=zh-tw#timestamp_sub) |
|  | [`TIMESTAMP_TRUNC`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/timestamp_functions?hl=zh-tw#timestamp_trunc) |
| `TIMEZONE` |  |
| `TO_DATE` | [`PARSE_DATE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/date_functions?hl=zh-tw#parse_date) |
| `TO_TIMESTAMP` | [`PARSE_TIMESTAMP`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/timestamp_functions?hl=zh-tw#parse_timestamp) |
|  | [`UNIX_DATE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/date_functions?hl=zh-tw#unix_date) |
|  | [`UNIX_MICROS`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/timestamp_functions?hl=zh-tw#unix_micros) |
|  | [`UNIX_MILLIS`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/timestamp_functions?hl=zh-tw#unix_millis) |
|  | [`UNIX_SECONDS`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/timestamp_functions?hl=zh-tw#unix_seconds) |

### 字串函式

| **Netezza** | **BigQuery** |
| --- | --- |
| `ASCII` | [`TO_CODE_POINTS`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/string_functions?hl=zh-tw#to_code_points)`(string_expr)[OFFSET(0)]` |
|  | [`BYTE_LENGTH`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/string_functions?hl=zh-tw#byte_length) |
|  | [`TO_HEX`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/string_functions?hl=zh-tw#to_hex) |
|  | [`CHAR_LENGTH`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/string_functions?hl=zh-tw#char_length) |
|  | [`CHARACTER_LENGTH`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/string_functions?hl=zh-tw#character_length) |
|  | [`CODE_POINTS_TO_BYTES`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/string_functions?hl=zh-tw#code_points_to_bytes) |
| `BTRIM` |  |
| `CHR` | [`CODE_POINTS_TO_STRING`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/string_functions?hl=zh-tw#code_points_to_string)`([numeric_expr])` |
|  | [`CONCAT`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/string_functions?hl=zh-tw#concat) |
| `DBL_MP` |  |
| `DLE_DST` |  |
|  | [`ENDS_WITH`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/string_functions?hl=zh-tw#ends_with) |
|  | [`FORMAT`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/string_functions?hl=zh-tw#format_string) |
|  | [`FROM_BASE32`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/string_functions?hl=zh-tw#from_base32) |
|  | [`FROM_BASE64`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/string_functions?hl=zh-tw#from_base64) |
|  | [`FROM_HEX`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/string_functions?hl=zh-tw#from_hex) |
| `HEX_TO_BINARY` |  |
| `HEX_TO_GEOMETRY` |  |
| `INITCAP` |  |
| `INSTR` |  |
| `INT_TO_STRING` |  |
| `LE_DST` |  |
| `LENGTH` | [`LENGTH`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/string_functions?hl=zh-tw#length) |
| `LOWER` | [`LOWER`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/string_functions?hl=zh-tw#lower) |
| `LPAD` | [`LPAD`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/string_functions?hl=zh-tw#lpad) |
| `LTRIM` | [`LTRIM`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/string_functions?hl=zh-tw#ltrim) |
|  | [`NORMALIZE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/string_functions?hl=zh-tw#normalize) |
|  | [`NORMALIZE_AND_CASEFOLD`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/string_functions?hl=zh-tw#normalize_and_casefold) |
| `PRI_MP` |  |
|  | [`REGEXP_CONTAINS`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/string_functions?hl=zh-tw#regexp_contains) |
| `REGEXP_EXTRACT` | [`REGEXP_EXTRACT`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/string_functions?hl=zh-tw#regexp_extract) |
| `REGEXP_EXTRACT_ALL` | [`REGEXP_EXTRACT_ALL`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/string_functions?hl=zh-tw#regexp_extract_all) |
| `REGEXP_EXTRACT_ALL_SP` |  |
| `REGEXP_EXTRACT_SP` |  |
| `REGEXP_INSTR` | [`STRPOS`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/string_functions?hl=zh-tw#strpos)`(col,` [`REGEXP_EXTRACT`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/string_functions?hl=zh-tw#regexp_extract)`()`) |
| `REGEXP_LIKE` |  |
| `REGEXP_MATCH_COUNT` |  |
| `REGEXP_REPLACE` | [`REGEXP_REPLACE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/string_functions?hl=zh-tw#regexp_replace) |
| `REGEXP_REPLACE_SP` | `IF(`[`REGEXP_CONTAINS`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/string_functions?hl=zh-tw#regexp_contains)`,1,0)` |
|  | [`REGEXP_EXTRACT`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/string_functions?hl=zh-tw#regexp_extract) |
| `REPEAT` | [`REPEAT`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/string_functions?hl=zh-tw#repeat) |
|  | [`REPLACE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/string_functions?hl=zh-tw#replace) |
|  | [`REVERSE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/string_functions?hl=zh-tw#reverse) |
| `RPAD` | [`RPAD`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/string_functions?hl=zh-tw#rpad) |
| `RTRIM` | [`RTRIM`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/string_functions?hl=zh-tw#rtrim) |
|  | [`SAFE_CONVERT_BYTES_TO_STRING`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/string_functions?hl=zh-tw#safe_convert_bytes_to_string) |
| `SCORE_MP` |  |
| `SEC_MP` |  |
| `SOUNDEX` |  |
|  | [`SPLIT`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/string_functions?hl=zh-tw#split) |
|  | [`STARTS_WITH`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/string_functions?hl=zh-tw#starts_with) |
| `STRING_TO_INT` |  |
| `STRPOS` | [`STRPOS`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/string_functions?hl=zh-tw#strpos) |
| `SUBSTR` | [`SUBSTR`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/string_functions?hl=zh-tw#substr) |
|  | [`TO_BASE32`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/string_functions?hl=zh-tw#to_base32) |
|  | [`TO_BASE64`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/string_functions?hl=zh-tw#to_base64) |
| `TO_CHAR` |  |
| `TO_DATE` |  |
| `TO_NUMBER` |  |
| `TO_TIMESTAMP` |  |
|  | [`TO_CODE_POINTS`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/string_functions?hl=zh-tw#to_code_points) |
|  | [`TO_HEX`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/string_functions?hl=zh-tw#to_hex) |
| `TRANSLATE` |  |
|  | [`TRIM`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/string_functions?hl=zh-tw#trim) |
| `UPPER` | [`UPPER`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/string_functions?hl=zh-tw#upper) |
| `UNICODE` |  |
| `UNICODES` |  |

### 數學函式

| **Netezza** | **BigQuery** |
| --- | --- |
| `ABS` | [`ABS`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/mathematical_functions?hl=zh-tw#abs) |
| `ACOS` | [`ACOS`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/mathematical_functions?hl=zh-tw#acos) |
|  | [`ACOSH`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/mathematical_functions?hl=zh-tw#acosh) |
| `ASIN` | [`ASIN`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/mathematical_functions?hl=zh-tw#asin) |
|  | [`ASINH`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/mathematical_functions?hl=zh-tw#asinh) |
| `ATAN` | [`ATAN`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/mathematical_functions?hl=zh-tw#atan) |
| `ATAN2` | [`ATAN2`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/mathematical_functions?hl=zh-tw#atan2) |
|  | [`ATANH`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/mathematical_functions?hl=zh-tw#atanh) |
| `CEIL`  `DCEIL` |  |