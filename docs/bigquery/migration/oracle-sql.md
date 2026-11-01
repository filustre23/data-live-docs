Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [參考資料](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# Oracle SQL 翻譯指南

本文詳細說明 Oracle 和 BigQuery 在 SQL 語法方面的異同，協助您規劃遷移作業。使用[批次 SQL 翻譯](https://docs.cloud.google.com/bigquery/docs/batch-sql-translator?hl=zh-tw)大量遷移 SQL 指令碼，或使用[互動式 SQL 翻譯](https://docs.cloud.google.com/bigquery/docs/interactive-sql-translator?hl=zh-tw)翻譯臨時查詢。

**注意：** 在某些情況下，Oracle 和 BigQuery 中的 SQL 元素之間沒有直接對應關係。不過，在大多數情況下，您可以使用替代方法在 BigQuery 中實現與 Oracle 相同的功能，如本文件中的範例所示。

## 資料類型

本節說明 Oracle 和 BigQuery 資料類型之間的對應關係。

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
| `NUMBER` | `NUMERIC` | BigQuery 不允許使用者指定精確度或小數位數的自訂值。因此，Oracle 中的資料欄定義可能超出 BigQuery 支援的範圍。 此外，如果小數點後的位數超過對應資料欄指定的位數，Oracle 會先將小數點後的數字四捨五入，再儲存該數字。在 BigQuery 中，這項功能可透過 `ROUND()` 函式實作。 |
| `NUMBER(*, x)` | `NUMERIC` | BigQuery 不允許使用者指定精確度或小數位數的自訂值。因此，Oracle 中的資料欄定義可能超出 BigQuery 支援的範圍。 此外，如果小數點後的位數超過對應資料欄指定的位數，Oracle 會先將小數點後的數字四捨五入，再儲存該數字。在 BigQuery 中，這項功能可透過 `ROUND()` 函式實作。 |
| `NUMBER(x, -y)` | `INT64` | 如果使用者嘗試儲存小數，Oracle 會將其四捨五入為整數。在 BigQuery 中，如果嘗試將十進位數字儲存在定義為 `INT64` 的資料欄，會發生錯誤。在這種情況下，應套用 `ROUND()` 函式。 BigQuery `INT64` 資料類型最多可支援 18 位數的精確度。如果數字欄位超過 18 位數，則應在 BigQuery 中使用 `FLOAT64` 資料類型。 |
| `NUMBER(x)` | `INT64` | 如果使用者嘗試儲存小數，Oracle 會將其四捨五入為整數。在 BigQuery 中，如果嘗試將十進位數字儲存在定義為 `INT64` 的資料欄，會發生錯誤。在這種情況下，應套用 `ROUND()` 函式。 BigQuery `INT64` 資料類型最多可支援 18 位數的精確度。如果數字欄位超過 18 位數，則應在 BigQuery 中使用 `FLOAT64` 資料類型。 |
| `FLOAT` | `FLOAT64`/`NUMERIC` | `FLOAT` 是精確的資料類型，也是 Oracle 中的 `NUMBER` 子類型。在 BigQuery 中，`FLOAT64` 是近似資料類型。`NUMERIC` 可能更適合 BigQuery 中的 `FLOAT` 類型。 |
| `BINARY_DOUBLE` | `FLOAT64`/`NUMERIC` | `FLOAT` 是精確的資料類型，也是 Oracle 中的 `NUMBER` 子類型。在 BigQuery 中，`FLOAT64` 是近似資料類型。`NUMERIC` 可能更適合 BigQuery 中的 `FLOAT` 類型。 |
| `BINARY_FLOAT` | `FLOAT64`/`NUMERIC` | `FLOAT` 是精確的資料類型，也是 Oracle 中的 `NUMBER` 子類型。在 BigQuery 中，`FLOAT64` 是近似資料類型。`NUMERIC` 可能更適合 BigQuery 中的 `FLOAT` 類型。 |
| `LONG` | `BYTES` | `LONG` 資料類型用於舊版，不建議用於新版 Oracle Database。 如果需要在 BigQuery 中保留 `LONG` 資料，可以使用 BigQuery 中的 `BYTES` 資料類型。較好的做法是將二進位物件放入 Cloud Storage，並在 BigQuery 中保留參照。 |
| `BLOB` | `BYTES` | `BYTES` 資料類型可用於儲存可變長度的二進位資料。如果這個欄位不會用於查詢和分析，建議將二進位檔資料儲存在 Cloud Storage。 |
| `BFILE` | `STRING` | 二進位檔案可以儲存在 Cloud Storage 中，`STRING` 資料類型則可用於參照 BigQuery 資料表中的檔案。 |
| `DATE` | `DATETIME` |  |
| `TIMESTAMP` | `TIMESTAMP` | BigQuery 支援微秒精確度 (10-6)，而 Oracle 支援的精確度範圍為 0 到 9。 BigQuery 支援 TZ 資料庫中的時區區域名稱，以及與世界標準時間 (UTC) 的時差。  在 BigQuery 中，應手動執行時區轉換，以符合 Oracle 的 `TIMESTAMP WITH LOCAL TIME ZONE` 功能。 |
| `TIMESTAMP(x)` | `TIMESTAMP` | BigQuery 支援微秒精確度 (10-6)，而 Oracle 支援的精確度範圍為 0 到 9。 BigQuery 支援 TZ 資料庫中的時區區域名稱，以及與世界標準時間 (UTC) 的時差。  在 BigQuery 中，應手動執行時區轉換，以符合 Oracle 的 `TIMESTAMP WITH LOCAL TIME ZONE` 功能。 |
| `TIMESTAMP WITH TIME ZONE` | `TIMESTAMP` | BigQuery 支援微秒精確度 (10-6)，而 Oracle 支援的精確度範圍為 0 到 9。 BigQuery 支援 TZ 資料庫中的時區區域名稱，以及與世界標準時間 (UTC) 的時差。  在 BigQuery 中，應手動執行時區轉換，以符合 Oracle 的 `TIMESTAMP WITH LOCAL TIME ZONE` 功能。 |
| `TIMESTAMP WITH LOCAL TIME ZONE` | `TIMESTAMP` | BigQuery 支援微秒精確度 (10-6)，而 Oracle 支援的精確度範圍為 0 到 9。 BigQuery 支援 TZ 資料庫中的時區區域名稱，以及與世界標準時間 (UTC) 的時差。  在 BigQuery 中，應手動執行時區轉換，以符合 Oracle 的 `TIMESTAMP WITH LOCAL TIME ZONE` 功能。 |
| `INTERVAL YEAR TO MONTH` | `STRING` | 在 BigQuery 中，間隔值可以儲存為 `STRING` 資料類型。 |
| `INTERVAL DAY TO SECOND` | `STRING` | 在 BigQuery 中，間隔值可以儲存為 `STRING` 資料類型。 |
| `RAW` | `BYTES` | `BYTES` 資料類型可用於儲存可變長度的二進位資料。如果不會查詢這個欄位，也不會用於數據分析，建議將二進位檔資料儲存在 Cloud Storage。 |
| `LONG RAW` | `BYTES` | `BYTES` 資料類型可用於儲存可變長度的二進位資料。如果不會查詢這個欄位，也不會用於數據分析，建議將二進位檔資料儲存在 Cloud Storage。 |
| `ROWID` | `STRING` | Oracle 內部會使用這些資料類型，為資料表中的資料列指定不重複的位址。一般來說，應用程式不應使用 `ROWID` 或 `UROWID` 欄位。但如果是這種情況，可以使用 `STRING` 資料類型來保存這項資料。 |

### 類型格式

Oracle SQL 會使用一組預設格式做為參數，用於顯示運算式和資料欄資料，以及在資料類型之間進行轉換。例如，`NLS_DATE_FORMAT` 設為 `YYYY/MM/DD` 時，預設會將日期格式設為 `YYYY/MM/DD`。如要進一步瞭解 NLS 設定，請參閱 [Oracle 線上說明文件](https://docs.oracle.com/cd/B28359_01/server.111/b28298/ch3globenv.htm)。BigQuery 沒有初始化參數。

根據預設，BigQuery 預期所有來源資料在載入時都採用 UTF-8 編碼。如果 CSV 檔案中的資料採用 ISO-8859-1 格式編碼，您可以在匯入資料時明確指定編碼，讓 BigQuery 在匯入過程中正確將資料轉換為 UTF-8。

只能匯入 ISO-8859-1 或 UTF-8 編碼的資料。BigQuery 會以 UTF-8 編碼格式儲存及傳回資料。您可以在 [`DATE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/date_functions?hl=zh-tw) 和 [`TIMESTAMP`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/timestamp_functions?hl=zh-tw) 函式中設定預期的日期格式或時區。

### 時間戳記和日期類型格式

將時間戳記和日期格式元素從 Oracle 轉換為 BigQuery 時，請務必留意 `TIMESTAMP` 和 `DATETIME` 之間的時區差異，如下表所示。

請注意，Oracle 格式中沒有括號，因為格式 (`CURRENT_*`) 是關鍵字，而非函式。



| Oracle | BigQuery | 附註 |
| --- | --- | --- |
| `CURRENT_TIMESTAMP` | Oracle 中的 `TIMESTAMP` 資訊可能會有不同的時區資訊，這些資訊是使用資料欄定義中的 `WITH TIME ZONE` 或設定  `TIME_ZONE` 變數定義。 | 建議您使用 `CURRENT_TIMESTAMP()` 函式，其格式為 ISO 格式。不過，輸出格式一律會顯示世界標準時間時區。(在內部，BigQuery 沒有時區)。 請注意下列 ISO 格式差異：  `DATETIME` 的格式會依據輸出管道慣例設定。在 BigQuery 指令列工具和 BigQuery 控制台中，`DATETIME` 會根據 RFC 3339 使用 `T` 分隔符格式化。不過，在 Python 和 Java JDBC 中，空格會做為分隔符號。  如要使用明確格式，請使用 `FORMAT_DATETIME`() 函式，將字串明確轉換。舉例來說，下列運算式一律會傳回空格分隔符： `CAST(CURRENT_DATETIME() AS STRING)` | |
| `CURRENT_DATE   SYSDATE` | Oracle 使用 2 種日期類型：  * type 12 * type 13  Oracle 儲存日期時會使用類型 12。在內部，這些是固定長度的數字。`SYSDATE or CURRENT_DATE` 傳回日期時，Oracle 會使用類型 13 | BigQuery 具有獨立的 `DATE` 格式，一律會以 [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) 格式傳回日期。 `DATE_FROM_UNIX_DATE` 是以 1970 年為基準，因此無法使用。 | |
| `CURRENT_DATE-3` | 日期值會以整數表示。Oracle 支援日期類型的算術運算子。 | 如果是日期類型，請使用 `DATE_ADD`() 或 `DATE_SUB`()。BigQuery 會對 `INT64`、`NUMERIC` 和 `FLOAT64` 資料類型使用算術運算子。 | |
| `NLS_DATE_FORMAT` | 設定工作階段或系統日期格式。 | BigQuery 一律使用 [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601)，因此請務必轉換 Oracle 日期和時間。 | |

## 查詢語法

本節說明 Oracle 和 BigQuery 之間的查詢語法差異。

### `SELECT` 個陳述式

大多數 Oracle `SELECT` 陳述式都與 BigQuery 相容。

## 函式、運算子和運算式

以下各節列出 Oracle 函式與 BigQuery 對等函式之間的對應關係。

### 比較運算子

Oracle 和 BigQuery 比較運算子符合 ANSI SQL:2011 規範。下表中的比較運算子在 BigQuery 和 Oracle 中相同。在 BigQuery 中，您可以使用 [`REGEXP_CONTAINS`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/string_functions?hl=zh-tw#regexp_contains)，而非 `REGEXP_LIKE`。

| Operator | 說明 |
| --- | --- |
| `"="` | [等於](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/operators?hl=zh-tw#comparison_operators) |
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
| `IS NOT NULL` | [Not `NULL` value](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/operators?hl=zh-tw#comparison_operators) |
| `LIKE` | [使用 %進行模式比對](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/operators?hl=zh-tw#comparison_operators) |
| `EXISTS` | [如果子查詢傳回至少一列，則符合條件](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/operators?hl=zh-tw#comparison_operators) |

BigQuery 和 Oracle 的資料表運算子相同。

### 邏輯運算式和函式

| Oracle | BigQuery |
| --- | --- |
| `CASE` | `CASE` |
| `COALESCE` | `COALESCE(expr1, ..., exprN)` |
| `DECODE` | `CASE.. WHEN.. END` |
| `NANVL` | `IFNULL` |
| `FETCH NEXT>` | `LIMIT` |
| `NULLIF` | [`NULLIF(expression, expres`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/conditional_expressions?hl=zh-tw#nullif) |