Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [參考資料](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# Snowflake SQL 翻譯指南

本文詳細說明 Snowflake 和 BigQuery 之間 SQL 語法的異同，協助您加速規劃及執行將 EDW (企業資料倉儲) 遷移至 BigQuery 的作業。Snowflake 資料倉儲技術專為搭配 Snowflake 專屬 SQL 語法而設計。由於各服務的 SQL 方言不同，為 Snowflake 編寫的指令碼可能需要修改，才能在 BigQuery 中使用。使用[批次 SQL 翻譯](https://docs.cloud.google.com/bigquery/docs/batch-sql-translator?hl=zh-tw)大量遷移 SQL 指令碼，或使用[互動式 SQL 翻譯](https://docs.cloud.google.com/bigquery/docs/interactive-sql-translator?hl=zh-tw)翻譯臨時查詢。這兩項工具都支援 Snowflake SQL ([預先發布版](https://cloud.google.com/products?hl=zh-tw#product-launch-stages))。

**注意：** 在某些情況下，Snowflake 和 BigQuery 中的 SQL 元素之間沒有直接對應關係。不過，在大多數情況下，您可以使用替代方法在 BigQuery 中實現與 Snowflake 相同的功能，如本文件中的範例所示。

## 資料類型

本節說明 Snowflake 和 BigQuery 資料類型之間的對應關係。

  
  

| Snowflake | BigQuery | 附註 |
| --- | --- | --- |
| `NUMBER/ DECIMAL/NUMERIC` | `NUMERIC/BIGNUMERIC` | 可對應至 `NUMERIC` 或 `BIGNUMERIC`，視精確度和規模而定。   Snowflake 的 `NUMBER` 資料類型支援 38 位數的有效位數和 37 位數的小數位數。使用者可指定精確度和規模。    BigQuery 支援 `NUMERIC` 和 `BIGNUMERIC`，[可選擇在特定範圍內指定精確度和規模](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#decimal_types)。 |
| [`INT/INTEGER`](https://docs.snowflake.com/en/sql-reference/data-types-numeric.html#int-integer-bigint-smallint-tinyint-byteint) | `BIGNUMERIC` | `INT/INTEGER` 和所有其他類似 `INT` 的資料類型 (例如 `BIGINT, TINYINT, SMALLINT, BYTEINT`) 代表 `NUMBER` 資料類型的別名，其中無法指定精確度和規模，且一律為 `NUMBER(38, 0)`    BigQuery 預設會將 `INTEGER` 轉換為 `INT64`。如要設定 SQL 轉譯功能，將其轉換為其他資料類型，可以使用 [`REWRITE_ZERO_SCALE_NUMERIC_AS_INTEGER` 設定選項](https://docs.cloud.google.com/bigquery/docs/config-yaml-translation?hl=zh-tw#optimize_and_improve_the_performance_of_translated_sql) |
| `BIGINT` | `BIGNUMERIC` |  |
| `SMALLINT` | `BIGNUMERIC` |  |
| `TINYINT` | `BIGNUMERIC` |  |
| `BYTEINT` | `BIGNUMERIC` |  |
| `FLOAT/  FLOAT4/  FLOAT8` | `FLOAT64` | Snowflake 中的 `FLOAT` 資料類型會將「NaN」設為 > X，其中 X 是任何 FLOAT 值 (「NaN」本身除外)。    BigQuery 中的 `FLOAT` 資料類型會將「NaN」設為 < X，其中 X 是任何 FLOAT 值 (「NaN」本身除外)。 |
| `DOUBLE/  DOUBLE PRECISION/`  `REAL` | `FLOAT64` | Snowflake 中的 `DOUBLE` 資料類型與 Snowflake 中的 `FLOAT` 資料類型同義，但通常會誤顯示為 `FLOAT`。並以 `DOUBLE` 格式妥善儲存。 |
| `VARCHAR` | `STRING` | Snowflake 的 `VARCHAR` 資料類型長度上限為 128 MB (未壓縮)。如未指定長度，則預設為長度上限。    BigQuery 中的 `STRING` 資料類型會儲存為可變長度的 UTF-8 編碼 Unicode。如要進一步瞭解資料欄和資料列限制，請參閱「[查詢工作](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#query_jobs)」。 |
| `CHAR/CHARACTER` | `STRING` |
| `STRING/TEXT` | `STRING` | Snowflake 中的 `STRING` 資料類型與 Snowflake 的 VARCHAR 同義。 |
| `BINARY` | `BYTES` |  |
| `VARBINARY` | `BYTES` |  |
| `BOOLEAN` | `BOOL` | BigQuery 中的 `BOOL` 資料類型只能接受 `TRUE/FALSE`，而 Snowflake 中的 `BOOL` 資料類型則可接受 TRUE/FALSE/NULL。 |
| `DATE` | `DATE` | Snowflake 的 `DATE` 類型接受大多數常見的日期格式，而 BigQuery 的 `DATE` 類型僅接受「YYYY-[M]M-[D]D」格式的日期。 |
| `TIME` | `TIME` | Snowflake 的 TIME 類型支援 0 到 9 奈秒的精確度，而 BigQuery 的 TIME 類型支援 0 到 6 奈秒的精確度。 |
| `TIMESTAMP` | `DATETIME` | `TIMESTAMP` 是使用者可設定的別名，預設為 `TIMESTAMP_NTZ`，對應至 BigQuery 中的 `DATETIME`。 |
| `TIMESTAMP_LTZ` | `TIMESTAMP` |  |
| `TIMESTAMP_NTZ/DATETIME` |
| `DATETIME` |  |
| `TIMESTAMP_TZ` | `TIMESTAMP` |  |
| `OBJECT` | `JSON` |  |
| `VARIANT` | `JSON` |  |
| `ARRAY` | `ARRAY<JSON>` | SQL 翻譯服務會保留類型陣列的資料類型。如果是 `ARRAY<VARIANT>` 等無類型陣列，BigQuery 會將其轉換為 `ARRAY<JSON>` |

BigQuery 還有下列資料類型，沒有直接對應的 Snowflake 資料類型：

* [`DATETIME`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#datetime_type)
* [`GEOGRAPHY`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#geography_type)

## `CREATE FUNCTION` 語法

下表說明 Snowflake 和 BigQuery 在 SQL UDF 建立語法方面的差異。

| **Snowflake** | BigQuery |
| --- | --- |
| `CREATE [ OR REPLACE ] FUNCTION`  `function_name`  `([sql_arg_name sql_arg_data_type[,..]])`  `RETURNS data_type`  `AS sql_function_definition`  `s` | `CREATE [OR REPLACE] FUNCTION function_name`  `([sql_arg_name sql_arg_data_type[,..]])`  `AS sql_function_definition`   注意：在 BigQuery [SQL UDF](https://docs.cloud.google.com/bigquery/docs/user-defined-functions?hl=zh-tw#sql-udf-structure) 中，傳回資料類型為選用項目。當查詢呼叫函式時，BigQuery 會從 SQL 函式主體推論函式的結果類型。 |
| `CREATE [OR REPLACE] FUNCTION`  `function_name`  `([sql_arg_name sql_arg_data_type[,..]])`  `RETURNS TABLE (col_name, col_data_type[,..])`  `AS sql_function_definition` | `CREATE [OR REPLACE] FUNCTION function_name`  `([sql_arg_name sql_arg_data_type[,..]])`  `RETURNS data_type`  `AS sql_function_definition`   注意：BigQuery [SQL UDF](https://docs.cloud.google.com/bigquery/docs/user-defined-functions?hl=zh-tw#sql-udf-structure) 不支援傳回資料表類型，但這項功能已列入產品藍圖，很快就會推出。不過，BigQuery 支援傳回 STRUCT 類型的 ARRAY。 |
| `CREATE [SECURE] FUNCTION`  `function_name`  `([sql_arg_name sql_arg_data_type[,..]])`  `RETURNS data_type`  `AS sql_function_definition`   注意：Snowflake 提供安全選項，可限制只有授權使用者 (即獲派檢視表擁有者角色的使用者) 才能存取 UDF 定義和詳細資料。 | `CREATE FUNCTION`  `function_name`  `([sql_arg_name sql_arg_data_type[,..]])`  `RETURNS data_type`  `AS sql_function_definition`   注意：函式安全性並非 BigQuery 的可設定參數。BigQuery 支援建立 IAM 角色和權限，可限制基礎資料和函式定義的存取權。 |
| `CREATE [OR REPLACE] FUNCTION`  `function_name`  `([sql_arg_name sql_arg_data_type[,..]])`  `RETURNS data_type`  `[ { CALLED ON NULL INPUT | { RETURNS NULL ON NULL INPUT | STRICT } } ]`  `AS sql_function_definition` | `CREATE [OR REPLACE] FUNCTION function_name`  `([sql_arg_name sql_arg_data_type[,..]])`  `RETURNS data_type`  `AS sql_function_definition`   注意：BigQuery 會隱含處理空值輸入內容的函式行為，不需指定為獨立選項。 |
| `CREATE [OR REPLACE] FUNCTION`  `function_name`  `([sql_arg_name sql_arg_data_type[,..]])`  `RETURNS data_type`  `[VOLATILE | IMMUTABLE]`  `AS sql_function_definition` | `CREATE [OR REPLACE] FUNCTION`  `function_name`  `([sql_arg_name sql_arg_data_type[,..]])`  `RETURNS data_type`  `AS sql_function_definition`   注意：函式波動性並非 BigQuery 的可設定參數。所有 BigQuery UDF 波動性都等同於 Snowflake 的 `IMMUTABLE` 波動性 (也就是說，不會執行資料庫查詢，或使用未直接出現在引數清單中的資訊)。 |
| `CREATE [OR REPLACE] FUNCTION`  `function_name`  `([sql_arg_name sql_arg_data_type[,..]])`  `RETURNS data_type`  `AS [' | $$]`  `sql_function_definition`  `[' | $$]` | `CREATE [OR REPLACE] FUNCTION`   `function_name`  `([sql_arg_name sql_arg_data_type[,..]])`  `RETURNS data_type`  `AS sql_function_definition`   注意：使用單引號或錢幣符號引號 ($$) is not required or supported in BigQuery. BigQuery implicitly interprets the SQL expression. |
| `CREATE [OR REPLACE] FUNCTION`  `function_name`  `([sql_arg_name sql_arg_data_type[,..]])`  `RETURNS data_type`  `[COMMENT = '<string_literal>']`  `AS sql_function_definition` | `CREATE [OR REPLACE] FUNCTION`  `function_name`  `([sql_arg_name sql_arg_data_type[,..]])`  `RETURNS data_type`  `AS sql_function_definition`   Note: Adding comments or descriptions in UDFs is not supported in BigQuery. |
| `CREATE [OR REPLACE] FUNCTION function_name`  `(x integer, y integer)`  `RETURNS integer`  `AS $$   SELECT x + y  $$   Note: Snowflake does not support ANY TYPE for SQL UDFs. However, it supports using VARIANT data types.` | `CREATE [OR REPLACE] FUNCTION function_name`  `(x ANY TYPE, y ANY TYPE)`  `AS`  `SELECT x + y`     Note: BigQuery supports using ANY TYPE as argument type. The function will accept an input of any type for this argument. For more information, see [templated parameter](https://docs.cloud.google.com/bigquery/docs/user-defined-functions?hl=zh-tw#templated-sql-udf-parameters) in BigQuery. |

BigQuery also supports the `CREATE FUNCTION IF NOT EXISTS` statement
which treats the query as successful and takes no action if a function with the
same name already exists.

BigQuery's `CREATE FUNCTION` statement also supports creating
[`TEMPORARY or TEMP functions`](https://docs.cloud.google.com/bigquery/docs/user-defined-functions?hl=zh-tw), which do
not have a Snowflake equivalent. See
[calling UDFs](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/syntax?hl=zh-tw#calling_persistent_user-defined_functions_udfs)
for details on executing a BigQuery persistent UDF.

## `DROP FUNCTION` syntax

The following table addresses differences in DROP FUNCTION syntax between
Snowflake and BigQuery.

| **Snowflake** | BigQuery |
| --- | --- |
| `DROP FUNCTION [IF EXISTS]`  `function_name`  `([arg_data_type, ... ])` | `DROP FUNCTION [IF EXISTS] dataset_name.function_name`   Note: BigQuery does not require using the function's signature (argument data type) for deleting the function. |

BigQuery requires that you specify the `project_name` if the function
is not located in the current project.

## Additional function commands

This section covers additional UDF commands supported by Snowflake that are not
directly available in BigQuery.

### `ALTER FUNCTION` syntax

Snowflake supports the following operations using
[`ALTER FUNCTION`](https://docs.snowflake.net/manuals/sql-reference/sql/alter-function.html)
syntax.

* Renaming a UDF
* Converting to (or reverting from) a secure UDF
* Adding, overwriting, removing a comment for a UDF

As configuring function security and adding function comments is not available
in BigQuery, `ALTER FUNCTION` syntax is not supported. However,
the [CREATE FUNCTION](https://docs.cloud.google.com/bigquery/docs/user-defined-functions?hl=zh-tw#sql-udf-structure)
statement can be used to create a UDF with the same function definition but a
different name.

### `DESCRIBE FUNCTION` syntax

Snowflake supports describing a UDF using
[DESC[RIBE] FUNCTION](https://docs.snowflake.net/manuals/sql-reference/sql/desc-function.html)
syntax. This is not supported in BigQuery. However, querying
UDF metadata via INFORMATION SCHEMA will be available soon as part of the
product roadmap.

### `SHOW USER FUNCTIONS` syntax

In Snowflake,
[SHOW USER FUNCTIONS](https://docs.snowflake.net/manuals/sql-reference/sql/show-user-functions.html)
syntax can be used to list all UDFs for which users have access privileges. This
is not supported in BigQuery. However, querying UDF metadata
via INFORMATION SCHEMA will be available soon as part of the product roadmap.

## Stored procedures

Snowflake
[stored procedures](https://docs.snowflake.net/manuals/sql-reference/stored-procedures-usage.html)
are written in JavaScript, which can execute SQL statements by calling a
JavaScript API. In BigQuery, stored procedures are defined using a
[block](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/scripting?hl=zh-tw#begin) of SQL
statements.

### `CREATE PROCEDURE` syntax

In Snowflake, a stored procedure is executed with a
[CALL](https://docs.snowflake.net/manuals/sql-reference/sql/call.html) command
while in BigQuery, stored procedures are
[executed](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#create_procedure)
like any other BigQuery function.

The following table addresses differences in stored procedure creation syntax
between Snowflake and BigQuery.

| **Snowflake** | BigQuery |
| --- | --- |
| `CREATE [OR REPLACE] PROCEDURE`  `procedure_name`  `([arg_name arg_data_type[,..]])`  `RETURNS data_type`  `AS procedure_definition;`   Note: Snowflake requires that stored procedures return a single value. Hence, return data type is a required option. | `CREATE [OR REPLACE] PROCEDURE`  `procedure_name`  `([arg_mode arg_name arg_data_type[,..]])`  `BEGIN`  `procedure_definition`  `END;`   `arg_mode: IN | OUT | INOUT`   Note: BigQuery doesn't support a return type for stored procedures. Also, it requires specifying argument mode for each argument passed. |
| `CREATE [OR REPLACE] PROCEDURE`  `procedure_name`  `([arg_name arg_data_type[,..]])`  `RETURNS data_type`  `AS`  `$$`  `javascript_code`  `$$;` | `CREATE [OR REPLACE] PROCEDURE`  `procedure_name`  `([arg_name arg_data_type[,..]])`  `BEGIN`  `statement_list`  `END;` |
| `C` |