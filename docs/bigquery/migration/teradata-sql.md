Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [參考資料](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# Teradata SQL 翻譯指南

本文詳述 SQL 語法中 Teradata 和 BigQuery 之間的相似與差異之處，協助您規劃遷移作業。使用[批次 SQL 翻譯](https://docs.cloud.google.com/bigquery/docs/batch-sql-translator?hl=zh-tw)功能大量遷移 SQL 指令碼，或使用[互動式 SQL 翻譯](https://docs.cloud.google.com/bigquery/docs/interactive-sql-translator?hl=zh-tw)功能翻譯臨時查詢。

## 資料類型

本節說明 Teradata 和 BigQuery 的資料類型對應關係。

**注意：** Teradata 支援 [`DEFAULT`](https://docs.teradata.com/r/Enterprise_IntelliFlex_VMware/SQL-Data-Definition-Language-Syntax-and-Examples/Table-Statements/CREATE-TABLE-and-CREATE-TABLE-AS/Syntax-Elements/column_partition_definition/column_data_type_attribute/DEFAULT?tocId=FGX%7EnkdqLciLCOJTJMvFnA) 和其他[限制](https://docs.teradata.com/r/Enterprise_IntelliFlex_VMware/SQL-Data-Definition-Language-Syntax-and-Examples/Table-Statements/CREATE-TABLE-and-CREATE-TABLE-AS/Syntax-Elements/column_partition_definition/table_constraint)，但這些項目不會用於 BigQuery。


| Teradata | BigQuery | 附註 |
| --- | --- | --- |
| `INTEGER` | `INT64` |  |
| `SMALLINT` | `INT64` |  |
| `BYTEINT` | `INT64` |  |
| `BIGINT` | `INT64` |  |
| `DECIMAL` | `NUMERIC, DECIMAL`  `BIGNUMERIC, BIGDECIMAL` | 如果精度 (小數點後的位數) 小於或等於 9，請使用 BigQuery 的 `NUMERIC` (別名 `DECIMAL`)。  如果比例為 9 以上，請使用 BigQuery 的 `BIGNUMERIC` (別名 `BIGDECIMAL`)。  如果您需要強制執行自訂位數或比例邊界 (限制)，請使用 BigQuery 的[參數化](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#parameterized_decimal_type)小數資料類型。  Teradata 可讓您透過捨入儲存值來插入精確度較高的值，但會在計算中保留高精確度。這可能會導致與 ANSI 標準相比，產生[非預期的捨入行為](https://docs.teradata.com/r/SQL-Data-Types-and-Literals/July-2021/Numeric-Data-Types/Rounding)。 |
| `FLOAT` | `FLOAT64` |  |
| `NUMERIC` | `NUMERIC, DECIMAL`  `BIGNUMERIC, BIGDECIMAL` | 如果精度 (小數點後的位數) 小於或等於 9，請使用 BigQuery 的 `NUMERIC` (別名 `DECIMAL`)。  如果比例為 9 以上，請使用 BigQuery 的 `BIGNUMERIC` (別名 `BIGDECIMAL`)。  如果您需要強制執行自訂位數或比例邊界 (限制)，請使用 BigQuery 的[參數化](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#parameterized_decimal_type)小數資料類型。  Teradata 可讓您透過捨入儲存值來插入精確度較高的值，但會在計算中保留高精確度。這可能會導致與 ANSI 標準相比，產生[非預期的捨入行為](https://docs.teradata.com/r/SQL-Data-Types-and-Literals/July-2021/Numeric-Data-Types/Rounding)。 |
| `NUMBER` | `NUMERIC, DECIMAL`  `BIGNUMERIC, BIGDECIMAL` | 如果精度 (小數點後的位數) 小於或等於 9，請使用 BigQuery 的 `NUMERIC` (別名 `DECIMAL`)。  如果比例為 9 以上，請使用 BigQuery 的 `BIGNUMERIC` (別名 `BIGDECIMAL`)。  如果您需要強制執行自訂位數或比例邊界 (限制)，請使用 BigQuery 的[參數化](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#parameterized_decimal_type)小數資料類型。  Teradata 可讓您透過捨入儲存值來插入精確度較高的值，但會在計算中保留高精確度。這可能會導致與 ANSI 標準相比，產生[非預期的捨入行為](https://docs.teradata.com/r/SQL-Data-Types-and-Literals/July-2021/Numeric-Data-Types/Rounding)。 |
| `REAL` | `FLOAT64` |  |
| `CHAR/CHARACTER` | `STRING` | 如果您需要強制設定字元長度上限，請使用 BigQuery 的 [參數化](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#parameterized_string_type) `STRING` 資料類型。 |
| `VARCHAR` | `STRING` | 如果您需要強制設定字元長度上限，請使用 BigQuery 的 [參數化](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#parameterized_string_type) `STRING` 資料類型。 |
| `CLOB` | `STRING` |  |
| `JSON` | `JSON` |  |
| `BLOB` | `BYTES` |  |
| `BYTE` | `BYTES` |  |
| `VARBYTE` | `BYTES` |  |
| `DATE` | `DATE` | BigQuery 不支援 SDF 中 Teradata 支援的自訂格式。 |
| `TIME` | `TIME` |  |
| `TIME WITH TIME ZONE` | `TIME` | Teradata 會以 UTC 格式儲存 `TIME` 資料類型，並允許您使用 `WITH TIME ZONE` 語法傳遞 UTC 時差。BigQuery 中的 `TIME` 資料類型代表不受任何日期或時區影響的時間。 |
| `TIMESTAMP` | `TIMESTAMP` | Teradata 和 BigQuery 的 `TIMESTAMP` 資料類型都具有微秒精確度 (但 Teradata 支援閏秒，而 BigQuery 不支援)。    Teradata 和 BigQuery 資料類型通常都會與 UTC 時區相關聯 ([詳情](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#time_zones))。 |
| `TIMESTAMP WITH TIME ZONE` | `TIMESTAMP` | Teradata `TIMESTAMP` 可設定為系統層級、每個使用者或每個資料欄的不同時區 (使用 `WITH TIME ZONE`)。    如果您未明確指定時區，BigQuery `TIMESTAMP` 類型會假設為世界標準時間。請務必正確匯出時區資訊 (不要在沒有時區資訊的情況下連結 `DATE` 和 `TIME` 值)，以便 BigQuery 在匯入時進行轉換。或者，請務必在匯出前將時區資訊轉換為世界標準時間。    BigQuery 提供 `DATETIME`，用於將公元時間與 `TIMESTAMP` 之間的差異抽象化，前者在輸出時不會顯示時區，後者則是精確的時間點，一律會顯示世界標準時間。 |
| `ARRAY` | `ARRAY` |  |
| `MULTI-DIMENSIONAL ARRAY` | `ARRAY` | 在 BigQuery 中，請使用結構體陣列，其中每個結構體都包含 `ARRAY` 類型的欄位 (詳情請參閱 BigQuery [說明文件](https://docs.cloud.google.com/bigquery/docs/arrays?hl=zh-tw#building_arrays_of_arrays))。 |
| `INTERVAL HOUR` | `INT64` |  |
| `INTERVAL MINUTE` | `INT64` |  |
| `INTERVAL SECOND` | `INT64` |  |
| `INTERVAL DAY` | `INT64` |  |
| `INTERVAL MONTH` | `INT64` |  |
| `INTERVAL YEAR` | `INT64` |  |
| `PERIOD(DATE)` | `DATE`，`DATE` | `PERIOD(DATE)` 應轉換為包含開始日期和結束日期的兩個 `DATE` 資料欄，以便與時間窗口函式搭配使用。 |
| `PERIOD(TIMESTAMP WITH TIME ZONE)` | `TIMESTAMP`，`TIMESTAMP` |  |
| `PERIOD(TIMESTAMP)` | `TIMESTAMP`，`TIMESTAMP` |  |
| `PERIOD(TIME)` | `TIME`，`TIME` |  |
| `PERIOD(TIME WITH TIME ZONE)` | `TIME`，`TIME` |  |
| `UDT` | `STRING` |  |
| `XML` | `STRING` |  |
| `TD_ANYTYPE` | `STRING` |  |

如要進一步瞭解型別轉換，請參閱下一節。

### Teradata 類型格式設定

Teradata SQL 會使用一組預設格式，用於顯示運算式和資料欄資料，以及在資料類型之間進行轉換。例如，`INTEGERDATE` 模式中的 `PERIOD(DATE)` 資料類型預設格式為 `YY/MM/DD`。建議您盡可能使用 ANSIDATE 模式，確保符合 ANSI SQL 規範，並利用這個機會清理舊版格式。

Teradata 可讓您使用 `FORMAT` 子句自動套用自訂格式，而無須變更基礎儲存空間，無論是使用 DDL 建立資料表時，或是在衍生運算式中，都可以將其做為資料類型屬性。例如，`FORMAT` 規格 `9.99` 會將任何 `FLOAT` 值四捨五入至兩位數。在 BigQuery 中，必須使用 `ROUND()` 函式才能轉換這項功能。

這項功能需要處理複雜的極端情況。舉例來說，當 `FORMAT` 子句套用至 `NUMERIC` 欄時，您必須[考量特殊捨入和格式規則](https://docs.teradata.com/r/SQL-Data-Types-and-Literals/July-2021/Data-Type-Formats-and-Format-Phrases/FORMAT-Phrase-and-NUMERIC-Formats)。您可以使用 `FORMAT` 子句，將 `INTEGER` 紀元值隱含轉換為 `DATE` 格式。或者，`VARCHAR` 欄上的 `FORMAT` 規格 `X(6)` 會截斷資料欄值，因此您必須轉換為 `SUBSTR()` 函式。這項行為不符合 ANSI SQL 規範。因此，我們建議您不要將資料欄格式遷移至 BigQuery。

如果必須使用資料欄格式，請使用[檢視畫面](https://docs.cloud.google.com/bigquery/docs/views?hl=zh-tw)或[使用者定義函式 (UDF)](https://docs.cloud.google.com/bigquery/docs/user-defined-functions?hl=zh-tw)。

如要瞭解 Teradata SQL 為每種資料類型使用的預設格式，請參閱 [Teradata 預設格式](https://docs.teradata.com/r/SQL-Data-Types-and-Literals/July-2021/Data-Type-Formats-and-Format-Phrases/Data-Type-Default-Formats)說明文件。

### 時間戳記和日期類型格式

下表概略說明 Teradata SQL 和 GoogleSQL 之間的時間戳記和日期格式化元素差異。

**注意：** Teradata 格式中沒有括號，因為這些格式 (`CURRENT_*`) 是關鍵字，而非函式。

| Teradata 格式 | Teradata 說明 | BigQuery |
| --- | --- | --- |
| `CURRENT_TIMESTAMP  CURRENT_TIME` | Teradata 中的 `TIME` 和 `TIMESTAMP` 資訊可能會有不同的時區資訊，這些資訊會使用 `WITH TIME ZONE` 定義。 | 盡可能使用採用 ISO 格式的 `CURRENT_TIMESTAMP()`。不過，輸出格式一律會顯示世界標準時間時區。(BigQuery 內部並未設定時區)。    請注意下列 ISO 格式差異的詳細說明。    `DATETIME` 會根據輸出管道慣例進行格式設定。在 BigQuery 指令列工具和 BigQuery 主控台中，這項資訊會根據 RFC 3339 使用 `T` 分隔符進行格式設定。不過，在 Python 和 Java JDBC 中，空格會用來做為分隔符。    如果您想使用明確的格式，請使用 `FORMAT_DATETIME()`，這樣就能明確將值轉換為字串。例如，下列運算式一律會傳回空格分隔符：    `CAST(CURRENT_DATETIME() AS STRING)`    Teradata 支援 `TIME` 資料欄中的 `DEFAULT` 關鍵字，用於設定目前時間 (時間戳記)；這項功能不會在 BigQuery 中使用。 |
| `CURRENT_DATE` | 日期會以 `INT64` 值的形式儲存在 Teradata 中，並使用以下公式：    `(YEAR - 1900) * 10000 + (MONTH * 100) + DAY`    日期可設為整數格式。 | BigQuery 有個獨立的 `DATE` 格式，一律會以 ISO 8601 格式傳回日期。    `DATE_FROM_UNIX_DATE` 無法使用，因為它是以 1970 年為基準。    Teradata 支援在 `DATE` 資料欄中使用 `DEFAULT` 關鍵字來設定目前日期，但這並未在 BigQuery 中使用。 |
| `CURRENT_DATE-3` | 日期值會以整數表示。Teradata 支援日期類型的算術運算子。 | 如為日期類型，請使用 `DATE_ADD()` 或 `DATE_SUB()`。    BigQuery 會使用算術運算子處理資料類型：`INT64`、`NUMERIC` 和 `FLOAT64`。 |
| `SYS_CALENDAR.CALENDAR` | Teradata 提供日曆運算檢視畫面，可用於執行整數運算以外的作業。 | 在 BigQuery 中不使用。 |
| `SET SESSION DATEFORM=ANSIDATE` | 將工作階段或系統日期格式設為 ANSI (ISO 8601)。 | BigQuery 一律使用 ISO 8601，因此請務必轉換 Teradata 日期和時間。 |

## 查詢語法

本節將說明 Teradata 和 BigQuery 之間的查詢語法差異。

### `SELECT` 陳述式

大部分的 Teradata [`SELECT` 陳述式](https://docs.teradata.com/r/SQL-Data-Manipulation-Language/July-2021/SELECT-Statements)都與 BigQuery 相容。下表列出一些細微差異。

| Teradata |  | BigQuery |
| --- | --- | --- |
| `SEL` |  | 轉換為 `SELECT`。BigQuery 不會使用 `SEL` 縮寫。 |
| `SELECT    (subquery) AS flag,    CASE WHEN flag = 1 THEN ...` |  | 在 BigQuery 中，資料欄無法參照同一個選取清單中定義的其他資料欄輸出內容。建議將子查詢移至 `WITH` 子句。    `WITH flags AS (    subquery  ),  SELECT    CASE WHEN flags.flag = 1 THEN ...` |
| `SELECT * FROM table  WHERE A LIKE ANY ('string1', 'string2')` |  | BigQuery 不會使用 `ANY` 邏輯述詞。    您可以使用多個 `OR` 運算子來達成相同的功能：    `SELECT * FROM table  WHERE col LIKE 'string1' OR        col LIKE 'string2'`    在這種情況下，字串比較也會有所不同。請參閱「[比較運算子](#comparison_operators)」。 |
| `SELECT TOP 10 * FROM table` |  | BigQuery 會在查詢結尾使用 `LIMIT`，而非在 `SELECT` 關鍵字後使用 `TOP n`。 |

### 比較運算子

下表列出 Teradata 專用的 Teradata 比較運算子，必須轉換為 BigQuery 使用的 ANSI SQL:2011 相容運算子。

如要瞭解 BigQuery 中的運算子，請參閱 BigQuery 說明文件中的「[運算子](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/operators?hl=zh-tw)」一節。



| Teradata | BigQuery | 附註 |
| --- | --- | --- |
| `exp EQ exp2`  `exp IN (exp2, exp3)` | `exp = exp2`  `exp IN (exp2, exp3)`    如要保留 `NOT CASESPECIFIC` 的非 ANSI 語意，您可以使用   `RTRIM(UPPER(exp)) = RTRIM(UPPER(exp2))` | 比較字串是否相等時，Teradata「可能」會忽略結尾空白，而 BigQuery 會將空白視為字串的一部分。舉例來說，`'xyz'=' xyz'` 在 Teradata 中為 `TRUE`，但在 BigQuery 中為 `FALSE`。    Teradata 也提供 `NOT CASESPECIFIC` 資料欄屬性，可指示 Teradata 在比較兩個字串時忽略大小寫。比較字串時，BigQuery 一律會區分大小寫。舉例來說，`'xYz' = 'xyz'` 在 Teradata 中為 `TRUE`，但在 BigQuery 中為 `FALSE`。 |
| `exp LE exp2` | `exp <= exp2` |  |
| `exp LT exp2` | `exp < exp2` |  |
| `exp NE exp2` | `exp <> exp2  exp != exp2` |  |
| `exp GE exp2` | `exp >= exp2` |  |
| `exp GT exp2` | `exp > exp2` |  |

### `JOIN` 個條件

BigQuery 和 Teradata 支援相同的 `JOIN`、`ON` 和 `USING` 條件。下表列出一些細微差異。



| Teradata | BigQuery | 附註 |
| --- | --- | --- |
| `FROM A JOIN B ON A.date > B.start_date AND A.date < B.end_date` | `FROM A LEFT OUTER JOIN B ON A.date > B.start_date AND A.date < B.end_date` | BigQuery 支援不等式 `JOIN` 子句，適用於所有內聯結或至少提供一個相等條件 (=)。但 `OUTER JOIN` 中不只支援一個不等式條件 (= 和 <)。這類結構有時會用於查詢日期或整數範圍。BigQuery 可防止使用者不小心建立大型交叉彙整。 |
| `FROM A, B ON A.id = B.id` | `FROM A JOIN B ON A.id = B.id` | 在 Teradata 中，資料表之間使用半形逗號等同於 `INNER JOIN`，而在 BigQuery 中則等同於 `CROSS JOIN` (笛卡兒積)。由於 BigQuery [舊版 SQL 中的逗號會視為 `UNION`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/migrating-from-legacy-sql?hl=zh-tw#comma_operator_with_tables)，因此建議您明確指定運算，以免造成混淆。 |
| `FROM A JOIN B ON (COALESCE(A.id , 0) = COALESCE(B.id, 0))` | `FROM A JOIN B ON (COALESCE(A.id , 0) = COALESCE(B.id, 0))` | 純量 (常數) 函式則沒有差異。 |
| `FROM A JOIN B ON A.id = (SELECT MAX(B.id) FROM B)` | `FROM A JOIN (SELECT MAX(B.id) FROM B) B1 ON A.id = B1.id` | BigQuery 會禁止使用者在彙整述詞中使用子查詢、關聯子查詢或匯總。這樣一來，BigQuery 就能並行執行查詢。 |

### 類型轉換和轉換

BigQuery 的資料類型比 Teradata 少，但範圍更廣，因此 BigQuery 在轉換時必須更加嚴格。



| Teradata | BigQuery | 附註 |
| --- | --- | --- |
| `exp EQ exp2`  `exp IN (exp2, exp3)` | `exp = exp2`  `exp IN (exp2, exp3)`    如要保留 `NOT CASESPECIFIC` 的非 ANSI 語意，您可以使用   `RTRIM(UPPER(exp)) = RTRIM(UPPER(exp2))` | 比較字串是否相等時，Teradata「可能」會忽略結尾空白，而 BigQuery 會將空白視為字串的一部分。舉例來說，`'xyz'=' xyz'` 在 Teradata 中為 `TRUE`，但在 BigQuery 中為 `FALSE`。    Teradata 也提供 `NOT CASESPECIFIC` 資料欄屬性，可指示 Teradata 在比較兩個字串時忽略大小寫。比較字串時，BigQuery 一律會區分大小寫。舉例來說，`'xYz' = 'xyz'` 在 Teradata 中為 `TRUE`，但在 BigQuery 中為 `FALSE`。 |
| `CAST(long_varchar_column AS CHAR(6))` | `LPAD(long_varchar_column, 6)` | 在 Teradata 中轉換字元欄時，有時會用來建立填入的子字串，但這並非標準做法，也不是最佳做法。 |
| `CAST(92617 AS TIME) 92617 (FORMAT '99:99:99')` | `PARSE_TIME("%k%M%S", CAST(92617 AS STRING))` | 相較於 BigQuery，Teradata 會執行更多[隱含類型轉換](https://docs.teradata.com/r/SQL-Data-Types-and-Literals/July-2021/Data-Type-Conversions/Implicit-Type-Conversions)和捨入作業，且通常會更嚴格地強制執行 ANSI 標準。  (這個範例會傳回 09:26:17) |
| `CAST(48.5 (FORMAT 'zz') AS FLOAT)` | `CAST(SUBSTR(CAST(48.5 AS STRING), 0, 2) AS FLOAT64)` | 浮點和數值資料類型在套用貨幣等格式時，可能需要特殊的[捨入規則](https://docs.teradata.com/r/SQL-Data-Types-and-Literals/July-2021/Numeric-Data-Types/Rounding)。 (這個範例會傳回 48) |

#### 將 `FLOAT`/`DECIMAL` 投放到 `INT`

如果 Teradata 使用高斯和銀行家演算法將數字四捨五入，請在 BigQuery 中使用 [`ROUND_HALF_EVEN` `RoundingMode`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/RoundingMode?hl=zh-tw)：

```
round(CAST(2.5 as Numeric),0, 'ROUND_HALF_EVEN')
```

#### 將 `STRING` 投放到 `NUMERIC` 或 `BIGNUMERIC`

從 `STRING` 轉換為數值時，請根據 `STRING` 值的小數點數使用正確的資料類型，也就是 `NUMERIC` 或 `BIGNUMERIC`。

如要進一步瞭解 BigQuery 支援的數字精確度和小數位數，請參閱「[十進制類型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#decimal_types)」。

另請參閱[比較運算子](#comparison_operators)和[欄格式](#type_formatting)。比較和資料欄格式化都會像型別轉換一樣運作。

### `QUALIFY`、`ROWS` 子句

Teradata 中的 `QUALIFY` 子句可讓您[篩選窗型函式的結果](https://docs.teradata.com/reader/2_MC9vCtAJRlKle2Rpb0mA/19NnI91neorAi7LX6SJXBw)。或者，您也可以使用 [`ROWS` 片語](https://docs.teradata.com/r/SQL-Functions-Expressions-and-Predicates/July-2021/Ordered-Analytical/Window-Aggregate-Functions/The-Window-Feature/ROWS-Phrase)來執行相同的任務。這些運算方式與 `GROUP` 子句的 `HAVING` 條件類似，可限制 BigQuery 中稱為[時間窗口函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/window-function-calls?hl=zh-tw)的輸出內容。



| Teradata | BigQuery |
| --- | --- |
| `SELECT col1, col2  FROM table  QUALIFY ROW_NUMBER() OVER (PARTITION BY col1 ORDER BY col2) = 1;` | 在 BigQuery 中，含有 `ROW_NUMBER()`、`SUM()`、`COUNT()` 等時間窗口函式和 `OVER PARTITION BY` 的 Teradata `QUALIFY` 子句會以包含分析值的子查詢中的 `WHERE` 子句表示。    使用 `ROW_NUMBER()`：    `SELECT col1, col2   FROM (    SELECT col1, col2,     ROW_NUMBER() OVER (PARTITION BY col1 ORDER BY col2) RN     FROM table  ) WHERE RN = 1;`    使用支援較大分割區的 `ARRAY_AGG`：    `SELECT    result.*  FROM (    SELECT      ARRAY_AGG(table ORDER BY table.col2        DESC LIMIT 1)[OFFSET(0)]    FROM table    GROUP BY col1  ) AS result;` |
| `SELECT col1, col2  FROM table  AVG(col1) OVER (PARTITION BY col1 ORDER BY col2 ROWS BETWEEN 2 PRECEDING AND CURRENT ROW);` | `SELECT col1, col2  FROM table  AVG(col1) OVER (PARTITION BY col1 ORDER BY col2 RANGE BETWEEN 2 PRECEDING AND CURRENT ROW);`    在 BigQuery 中，`RANGE` 和 `ROWS` 都可以用於窗格框架子句。不過，窗型子句只能搭配 `AVG()` 等窗型函式使用，不能搭配 `ROW_NUMBER()` 等編號函式使用。 |
| `SELECT col1, col2  FROM table  QUALIFY ROW_NUMBER() OVER (PARTITION BY col1 ORDER BY col2) = 1;` | `SELECT col1, col2 FROM   Dataset-name.table  QUALIFY row_number() OVER (PARTITION BY upper(a.col1) ORDER BY upper(a.col2)) = 1` |

### `NORMALIZE` 關鍵字

Teradata 為 `SELECT` 子句提供 [`NORMALIZE`](https://docs.teradata.com/r/Enterprise_IntelliFlex_VMware/SQL-Data-Definition-Language-Syntax-and-Examples/Table-Statements/ALTER-TABLE/ALTER-TABLE-Syntax-Elements/ALTER-TABLE-Syntax-Elements-Basic/ALTER-TABLE-Basic-Options/NORMALIZE) 關鍵字，可將重疊的期間或間隔合併為單一期間或間隔，涵蓋所有個別期間值。

BigQuery 不支援 `PERIOD` 類型，因此 Teradata 中的任何 `PERIOD` 類型欄必須以兩個個別的 `DATE` 或 `DATETIME` 欄位插入 BigQuery，這些欄位對應於期間的開始和結束時間。

| Teradata | BigQuery |
| --- | --- |
| `SELECT NORMALIZE      client_id,      item_sid,      BEGIN(period) AS min_date,      END(period) AS max_date,    FROM  &` |