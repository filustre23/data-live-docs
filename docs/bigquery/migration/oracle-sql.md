Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [參考資料](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# Oracle SQL 翻譯指南

本文詳述 Oracle 和 BigQuery 間 SQL 語法的相似與相異之處，協助您規劃遷移作業。使用[批次 SQL 翻譯](https://docs.cloud.google.com/bigquery/docs/batch-sql-translator?hl=zh-tw)大量遷移 SQL 指令碼，或使用[互動式 SQL 翻譯](https://docs.cloud.google.com/bigquery/docs/interactive-sql-translator?hl=zh-tw)翻譯臨時查詢。

**注意：** 在某些情況下，Oracle 和 BigQuery 中的 SQL 元素之間沒有直接對應關係。不過在大多數情況下，您可以使用替代方法，在 BigQuery 中達到 Oracle 所提供的相同功能，如本文件中的範例所示。

## 資料類型

本節說明 Oracle 和 BigQuery 中對等的資料類型。

| Oracle | BigQuery | 附註 |
| --- | --- | --- |
| `VARCHAR2` | `STRING` |  |
| `NVARCHAR2` | `STRING` |  |
| `CHAR` | `STRING` |  |
| `NCHAR` | `STRING` |  |
| `CLOB` | `STRING` |  |
| `NCLOB` | `STRING` |  |
| `INTEGER` | `INT64` |  |
| `SHORTINTEGER` | `INT64` |  |
| `LONGINTEGER` | `INT64` |  |
| `NUMBER` | `NUMERIC` | BigQuery 不允許使用者指定精確度或比例的自訂值。因此，Oracle 中的資料欄定義可能超出 BigQuery 支援的範圍。 此外，在儲存小數時，如果小數點後的位數超過對應資料欄的指定位數，Oracle 會將該數字無條件進位。在 BigQuery 中，這項功能可使用 `ROUND()` 函式實作。 |
| `NUMBER(*, x)` | `NUMERIC` | BigQuery 不允許使用者指定精確度或比例的自訂值。因此，Oracle 中的資料欄定義可能超出 BigQuery 支援的範圍。 此外，如果小數點後的位數超過對應資料欄的指定位數，Oracle 會先將小數向上進位，再儲存該小數。在 BigQuery 中，這項功能可使用 `ROUND()` 函式實作。 |
| `NUMBER(x, -y)` | `INT64` | 如果使用者嘗試儲存小數，Oracle 會將其四捨五入為整數。如果嘗試將十進位數字儲存在定義為 `INT64` 的資料欄中，BigQuery 會傳回錯誤。在這種情況下，應套用 `ROUND()` 函式。 BigQuery `INT64` 資料類型最多支援 18 位精確度。如果數字欄位超過 18 位數，請在 BigQuery 中使用 `FLOAT64` 資料型別。 |
| `NUMBER(x)` | `INT64` | 如果使用者嘗試儲存小數，Oracle 會將其四捨五入為整數。如果嘗試將十進位數字儲存在定義為 `INT64` 的資料欄中，BigQuery 會傳回錯誤。在這種情況下，應套用 `ROUND()` 函式。 BigQuery `INT64` 資料類型最多支援 18 位精確度。如果數字欄位超過 18 位數，請在 BigQuery 中使用 `FLOAT64` 資料型別。 |
| `FLOAT` | `FLOAT64`/`NUMERIC` | `FLOAT` 是精確資料類型，也是 Oracle 中的 `NUMBER` 子類型。在 BigQuery 中，`FLOAT64` 是近似資料類型。`NUMERIC` 可能更符合 BigQuery 中的 `FLOAT` 類型。 |
| `BINARY_DOUBLE` | `FLOAT64`/`NUMERIC` | `FLOAT` 是精確資料類型，也是 Oracle 中的 `NUMBER` 子類型。在 BigQuery 中，`FLOAT64` 是近似資料類型。`NUMERIC` 可能更符合 BigQuery 中的 `FLOAT` 類型。 |
| `BINARY_FLOAT` | `FLOAT64`/`NUMERIC` | `FLOAT` 是精確資料類型，也是 Oracle 中的 `NUMBER` 子類型。在 BigQuery 中，`FLOAT64` 是近似資料類型。`NUMERIC` 可能更符合 BigQuery 中的 `FLOAT` 類型。 |
| `LONG` | `BYTES` | `LONG` 資料類型用於舊版，不建議用於新版 Oracle 資料庫。 如需在 BigQuery 中保留 `LONG` 資料，可以使用 BigQuery 中的 `BYTES` 資料類型。較好的做法是將二進位物件放在 Cloud Storage 中，並在 BigQuery 中保留參照。 |
| `BLOB` | `BYTES` | `BYTES` 資料類型可用於儲存變數長度的二進位資料。如果不會查詢這個欄位，也不會用於分析，建議將二進位資料儲存在 Cloud Storage 中。 |
| `BFILE` | `STRING` | 二進位檔案可以儲存在 Cloud Storage 中，並使用 `STRING` 資料型別參照 BigQuery 資料表中的檔案。 |
| `DATE` | `DATETIME` |  |
| `TIMESTAMP` | `TIMESTAMP` | 相較於 Oracle 支援 0 到 9 的精確度，BigQuery 支援微秒精確度 (10-6)。 BigQuery 支援 TZ 資料庫中的時區區域名稱，以及與 UTC 的時區偏移量。  在 BigQuery 中，您必須手動執行時區轉換，才能符合 Oracle 的 `TIMESTAMP WITH LOCAL TIME ZONE` 功能。 |
| `TIMESTAMP(x)` | `TIMESTAMP` | 相較於 Oracle 支援 0 到 9 的精確度，BigQuery 支援微秒精確度 (10-6)。 BigQuery 支援 TZ 資料庫中的時區區域名稱，以及與 UTC 的時區偏移量。  在 BigQuery 中，您必須手動執行時區轉換，才能符合 Oracle 的 `TIMESTAMP WITH LOCAL TIME ZONE` 功能。 |
| `TIMESTAMP WITH TIME ZONE` | `TIMESTAMP` | 相較於 Oracle 支援 0 到 9 的精確度，BigQuery 支援微秒精確度 (10-6)。 BigQuery 支援 TZ 資料庫中的時區區域名稱，以及與 UTC 的時區偏移量。  在 BigQuery 中，您必須手動執行時區轉換，才能符合 Oracle 的 `TIMESTAMP WITH LOCAL TIME ZONE` 功能。 |
| `TIMESTAMP WITH LOCAL TIME ZONE` | `TIMESTAMP` | 相較於 Oracle 支援 0 到 9 的精確度，BigQuery 支援微秒精確度 (10-6)。 BigQuery 支援 TZ 資料庫中的時區區域名稱，以及與 UTC 的時區偏移量。  在 BigQuery 中，您必須手動執行時區轉換，才能符合 Oracle 的 `TIMESTAMP WITH LOCAL TIME ZONE` 功能。 |
| `INTERVAL YEAR TO MONTH` | `STRING` | 間隔值可以儲存為 BigQuery 中的 `STRING` 資料類型。 |
| `INTERVAL DAY TO SECOND` | `STRING` | 間隔值可以儲存為 BigQuery 中的 `STRING` 資料類型。 |
| `RAW` | `BYTES` | `BYTES` 資料類型可用於儲存變數長度的二進位資料。如果這個欄位不會用於查詢和數據分析，建議您將二進位資料儲存在 Cloud Storage 中。 |
| `LONG RAW` | `BYTES` | `BYTES` 資料類型可用於儲存變數長度的二進位資料。如果這個欄位不會用於查詢和數據分析，建議您將二進位資料儲存在 Cloud Storage 中。 |
| `ROWID` | `STRING` | Oracle 會在內部使用這些資料型別，為資料表中的資料列指定專屬位址。一般來說，應用程式不應使用 `ROWID` 或 `UROWID` 欄位。但如果是這種情況，`STRING` 資料型別可用於保存這項資料。 |

### 輸入格式

Oracle SQL 會使用一組預設格式 (設為參數)，顯示運算式和資料欄資料，並在資料類型之間轉換。舉例來說，`NLS_DATE_FORMAT` 預設會將日期格式設為 `YYYY/MM/DD`。`YYYY/MM/DD`如要進一步瞭解 [Oracle 線上說明文件中的 NLS 設定](https://docs.oracle.com/cd/B28359_01/server.111/b28298/ch3globenv.htm)，請參閱該文件。
BigQuery 沒有初始化參數。

根據預設，BigQuery 載入資料時，所有來源資料皆應為 UTF-8 編碼。如果您的 CSV 檔案是以 ISO-8859-1 格式編碼資料，您可以在匯入資料時明確指定編碼格式，這樣 BigQuery 才能在匯入過程中將資料正確轉換為 UTF-8 編碼。

您只能匯入採用 ISO-8859-1 或 UTF-8 編碼的資料。BigQuery 會以 UTF-8 編碼格式儲存及傳回資料。您可以在 [`DATE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/date_functions?hl=zh-tw) 和 [`TIMESTAMP`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/timestamp_functions?hl=zh-tw) 函式中設定預期的日期格式或時區。

### 時間戳記和日期類型格式

將 Oracle 的時間戳記和日期格式化元素轉換為 BigQuery 時，請注意 `TIMESTAMP` 和 `DATETIME` 之間的時區差異，如下表所示。

請注意，Oracle 格式中沒有括號，因為格式 (`CURRENT_*`) 是關鍵字，而非函式。



| Oracle | BigQuery | 附註 |
| --- | --- | --- |
| `CURRENT_TIMESTAMP` | Oracle 中的 `TIMESTAMP` 資訊可能含有不同的時區資訊，這些資訊是使用資料欄定義或設定 `WITH TIME ZONE`  `TIME_ZONE` 變數定義。 | 如有可能，請使用 `CURRENT_TIMESTAMP()` 函式，該函式會採用 ISO 格式。不過，輸出格式一律會顯示世界標準時間時區。(在內部，BigQuery 沒有時區)。 請注意 ISO 格式的差異：  `DATETIME` 的格式會依據輸出管道慣例而定。在 BigQuery 指令列工具和 BigQuery 控制台中，`DATETIME` 會根據 RFC 3339 使用 `T` 分隔符號格式化。不過在 Python 和 Java JDBC 中，空格會做為分隔符號。  如要使用明確格式，請使用 `FORMAT_DATETIME`() 函式，將明確轉換為字串。舉例來說，下列運算式一律會傳回空格分隔符： `CAST(CURRENT_DATETIME() AS STRING)` | |
| `CURRENT_DATE   SYSDATE` | Oracle 使用 2 種日期類型：  * 類型 12 * type 13  Oracle 儲存日期時會使用類型 12。在內部，這些是固定長度的數字。當 `SYSDATE or CURRENT_DATE` 傳回時，Oracle 會使用類型 13 | BigQuery 有專用的 `DATE` 格式，一律會以 [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) 格式傳回日期。 「`DATE_FROM_UNIX_DATE`」無法使用，因為是以 1970 年為準。 | |
| `CURRENT_DATE-3` | 日期值會以整數表示。Oracle 支援日期類型的算術運算子。 | 如果是日期類型，請使用 `DATE_ADD`() 或 `DATE_SUB`()。 BigQuery 會對資料類型使用算術運算子：`INT64`、`NUMERIC` 和 `FLOAT64`。 | |
| `NLS_DATE_FORMAT` | 設定工作階段或系統日期格式。 | BigQuery 一律使用 [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601)，因此請務必轉換 Oracle 日期和時間。 | |

## 查詢語法

本節說明 Oracle 和 BigQuery 之間的查詢語法差異。

### `SELECT` 個陳述式

大多數 Oracle `SELECT` 陳述式都與 BigQuery 相容。

## 函式、運算子和運算式

以下各節列出 Oracle 函式與 BigQuery 對應函式的對應關係。

### 比較運算子

Oracle 和 BigQuery 的比較運算子皆符合 ANSI SQL:2011 規範。下表中的比較運算子在 BigQuery 和 Oracle 中相同。您可以在 BigQuery 中使用 [`REGEXP_CONTAINS`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/string_functions?hl=zh-tw#regexp_contains)，取代 `REGEXP_LIKE`。

| 運算子 | 說明 |
| --- | --- |
| `"="` | [Equal](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/operators?hl=zh-tw#comparison_operators) |
| `<>` | [不等於](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/operators?hl=zh-tw#comparison_operators) |
| `!=` | [不等於](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/operators?hl=zh-tw#comparison_operators) |
| `>` | [大於](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/operators?hl=zh-tw#comparison_operators) |
| `>=` | [大於或等於](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/operators?hl=zh-tw#comparison_operators) |
| `<` | [小於](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/operators?hl=zh-tw#comparison_operators) |
| `<=` | [小於或等於](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/operators?hl=zh-tw#comparison_operators) |
| `IN ( )` | [比對清單中的值](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/operators?hl=zh-tw#comparison_operators) |
| `NOT` | [否定條件](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/operators?hl=zh-tw#comparison_operators) |
| `BETWEEN` | [在範圍內 (含)](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/operators?hl=zh-tw#comparison_operators) |
| `IS NULL` | [`NULL` 值](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/operators?hl=zh-tw#comparison_operators) |
| `IS NOT NULL` | [不是 `NULL` 值](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/operators?hl=zh-tw#comparison_operators) |
| `LIKE` | [使用 %進行模式比對](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/operators?hl=zh-tw#comparison_operators) |
| `EXISTS` | [如果子查詢傳回至少一個資料列，即符合條件](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/operators?hl=zh-tw#comparison_operators) |

BigQuery 和 Oracle 中的資料表運算子相同。

### 邏輯運算式和函式

| Oracle | BigQuery |
| --- | --- |
| `CASE` | `CASE` |
| `COALESCE` | `COALESCE(expr1, ..., exprN)` |
| `DECODE` | `CASE.. WHEN.. END` |
| `NANVL` | `IFNULL` |
| `FETCH NEXT>` | `LIMIT` |
| `NULLIF` | [`NULLIF(expression, expression_to_match)`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/conditional_expressions?hl=zh-tw#nullif) |
| `NVL` | `IFNULL(expr, 0), COALESCE(exp, 0)` |
| `NVL2` | `IF(expr, true_result, else_result)` |

### 匯總函式

下表顯示常見的 Oracle 匯總、統計匯總和近似匯總函式，以及對應的 BigQuery 函式：

| Oracle | BigQuery |
| --- | --- |
| `ANY_VALUE` (從 Oracle 19c) | `ANY_VALUE` |
| `APPROX_COUNT` | `HLL_COUNT set of functions with specified precision` |
| `APPROX_COUNT_DISTINCT` | `APPROX_COUNT_DISTINCT` |
| `APPROX_COUNT_DISTINCT_AGG` | `APPROX_COUNT_DISTINCT` |
| `APPROX_COUNT_DISTINCT_DETAIL` | `APPROX_COUNT_DISTINCT` |
| `APPROX_PERCENTILE(percentile) WITHIN GROUP (ORDER BY expression)` | `APPROX_QUANTILES(expression, 100)[ OFFSET(CAST(TRUNC(percentile * 100) as INT64))]`  BigQuery 不支援 Oracle 定義的其餘引數。 |
| `APPROX_PERCENTILE_AGG` | `APPROX_QUANTILES(expression, 100)[ OFFSET(CAST(TRUNC(percentile * 100) as INT64))]` |
| `APPROX_PERCENTILE_DETAIL` | `APPROX_QUANTILES(expression, 100)[OFFSET(CAST(TRUNC(percentile * 100) as INT64))]` |
| `APPROX_SUM` | `APPROX_TOP_SUM(expression, weight, number)` |
| `AVG` | `AVG` |
| `BIT_COMPLEMENT` | [位元 NOT 運算子：~](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/operators?hl=zh-tw) |
| `BIT_OR` | `BIT_OR, X | Y` |
| `BIT_XOR` | `BIT_XOR, X ^ Y` |
| `BITAND` | `BIT_AND, X & Y` |
| `CARDINALITY` | `COUNT` |
| `COLLECT` | BigQuery 不支援 `TYPE AS TABLE OF`。 請考慮在 BigQuery 中使用 `STRING_AGG()` 或 `ARRAY_AGG()`。 |
| `CORR/CORR_K/` `CORR_S` | `CORR` |
| `COUNT` | `COUNT` |
| `COVAR_POP` | `COVAR_POP` |
| `COVAR_SAMP` | `COVAR_SAMP` |
| `FIRST` | BigQuery 中沒有隱含的資料表。建議使用[使用者定義的函式 (UDF)](https://docs.cloud.google.com/bigquery/docs/user-defined-functions?hl=zh-tw)。 |
| `GROUP_ID` | BigQuery 中未使用 |
| `GROUPING` | `GROUPING` |
| `GROUPING_ID` | BigQuery 不會使用這項設定。 |
| `LAST` | BigQuery 中沒有隱含的資料表。建議使用[使用者定義函式](https://docs.cloud.google.com/bigquery/docs/user-defined-functions?hl=zh-tw)。 |
| `LISTAGG` | `STRING_AGG, ARRAY_CONCAT_AGG(expression [ORDER BY key [{ASC|DESC}] [, ... ]] [LIMIT n])` |
| `MAX` | `MAX` |
| `MIN` | `MIN` |
| `OLAP_CONDITION` | Oracle 專屬，BigQuery 中不存在。 |
| `OLAP_EXPRESSION` | Oracle 專屬，BigQuery 中不存在。 |
| `OLAP_EXPRESSION_BOOL` | Oracle 專屬，BigQuery 中不存在。 |
| `OLAP_EXPRESSION_DATE` | Oracle 專屬，BigQuery 中不存在。 |
| `OLAP_EXPRESSION_TEXT` | Oracle 專屬，BigQuery 中不存在。 |
| `OLAP_TABLE` | Oracle 專屬，BigQuery 中不存在。 |
| `POWERMULTISET` | Oracle 專屬，BigQuery 中不存在。 |
| `POWERMULTISET_BY_CARDINALITY` | Oracle 專屬，BigQuery 中不存在。 |
| `QUALIFY` | Oracle 專屬，BigQuery 中不存在。 |
| `REGR_AVGX` | `AVG(`  `IF(dep_var_expr is NULL`  `OR ind_var_expr is NULL,`  `NULL, ind_var_expr)`  `)` |
| `REGR_AVGY` | `AVG(`  `IF(dep_var_expr is NULL`  `OR ind_var_expr is NULL,`  `NULL, dep_var_expr)`  `)` |
| `REGR_COUNT` | `SUM(`  `IF(dep_var_expr is NULL`  `OR ind_var_expr is NULL,`  `NULL, 1)`  `)` |
| `REGR_INTERCEPT` | `AVG(dep_var_expr)  - AVG(ind_var_expr)  * (COVAR_SAMP(ind_var_expr,dep_var_expr)  / VARIANCE(ind_var_expr)  )` |
| `REGR_R2` | `(COUNT(dep_var_expr) *  SUM(ind_var_expr * dep_var_expr) -  SUM(dep_var_expr) * SUM(ind_var_expr))  / SQRT(  (COUNT(ind_var_expr) *  SUM(POWER(ind_var_expr, 2)) *  POWER(SUM(ind_var_expr),2)) *  (COUNT(dep_var_expr) *  SUM(POWER(dep_var_expr, 2)) *  POWER(SUM(dep_var_expr), 2)))` |
| `REGR_SLOPE` | `COVAR_SAMP(ind_var_expr,` `dep_var_expr)`  `/ VARIANCE(ind_var_expr)` |
| `REGR_SXX` | `SUM(POWER(ind_var_expr, 2)) - COUNT(ind_var_expr) * POWER(AVG(ind_var_expr),2)` |
| `REGR_SXY` | `SUM(ind_var_expr*dep_var_expr) - COUNT(ind_var_expr) * AVG(ind) * AVG(dep_var_expr)` |
| `REGR_SYY` | `SUM(POWER(dep_var_expr, 2)) - COUNT(dep_var_expr) * POWER(AVG(dep_var_expr),2)` |
| `ROLLUP` | `ROLLUP` |
| `STDDEV_POP` | `STDDEV_POP` |
| `STDDEV_SAMP` | `STDDEV_SAMP, STDDEV` |
| `SUM` | `SUM` |
| `VAR_POP` | `VAR_POP` |
| `VAR_SAMP` | `VAR_SAMP, VARIANCE` |
| `WM_CONCAT` | `STRING_AGG` |

BigQuery 提供下列其他匯總函式：

* `ANY_VALUE`
* `APPROX_TOP_COUNT`
* `COUNTIF`
* `LOGICAL_AND`
* `LOGICAL_OR`

### 分析函式

下表列出常見 Oracle 分析和匯總分析函式與 BigQuery 對應函式的對應關係。

| Oracle | BigQuery |
| --- | --- |
| `AVG` | `AVG` |
| `BIT_COMPLEMENT` | [位元 NOT 運算子：~](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/operators?hl=zh-tw) |
| `BIT_OR` | `BIT_OR, X | Y` |
| `BIT_XOR` | `BIT_XOR, X ^ Y` |
| `BITAND` | `BIT_AND, X & Y` |
| `BOOL_TO_INT` | `CAST(X AS INT64)` |
| `COUNT` | `COUNT` |
| `COVAR_POP` | `COVAR_POP` |
| `COVAR_SAMP` | `COVAR_SAMP` |
| `CUBE_TABLE` | BigQuery 不支援這項功能。考慮使用 BI 工具或自訂 UDF |
| `CUME_DIST` | `CUME_DIST` |
| `DENSE_RANK(ANSI)` | `DENSE_RANK` |
| `FEATURE_COMPARE` | BigQuery 中沒有隱含的資料表。考慮使用 UDF 和 BigQuery ML |
| `FEATURE_DETAILS` | BigQuery 中沒有隱含的資料表。考慮使用 UDF 和 BigQuery ML |
| `FEATURE_ID` | BigQuery 中沒有隱含的資料表。考慮使用 UDF 和 BigQuery ML |
| `FEATURE_SET` | BigQuery 中沒有隱含的資料表。考慮使用 UDF 和 BigQuery ML |
| `FEATURE_VALUE` | BigQuery 中沒有隱含的資料表。考慮使用 UDF 和 BigQuery ML |
| `FIRST_VALUE` | `FIRST_VALUE` |
| `HIER_CAPTION` | BigQuery 不支援階層式查詢。 |
| `HIER_CHILD_COUNT` | BigQuery 不支援階層式查詢。 |
| `HIER_COLUMN` | BigQuery 不支援階層式查詢。 |
| `HIER_DEPTH` | BigQuery 不支援階層式查詢。 |
| `HIER_DESCRIPTION` | BigQuery 不支援階層式查詢。 |
| `HIER_HAS_CHILDREN` | BigQuery 不支援階層式查詢。 |
| `HIER_LEVEL` | BigQuery 不支援階層式查詢。 |
| `HIER_MEMBER_NAME` | BigQuery 不支援階層式查詢。 |
| `HIER_ORDER` | BigQuery 不支援階層式查詢。 |
| `HIER_UNIQUE_MEMBER_NAME` | BigQuery 不支援階層式查詢。 |
| `LAST_VALUE` | `LAST_VALUE` |
| `LAG` | `LAG` |