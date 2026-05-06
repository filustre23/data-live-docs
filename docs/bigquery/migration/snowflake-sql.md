Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [參考資料](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# Snowflake SQL 翻譯指南

本文詳述 Snowflake 和 BigQuery 這兩者之間的 SQL 語法相似與相異之處，協助加速將企業資料倉儲 (EDW) 移至 BigQuery 的規劃與執行作業。Snowflake 資料倉儲技術專為與 Snowflake 專屬的 SQL 語法搭配使用而設計。由於 SQL 方言會因為服務不同而有差異，針對 Snowflake 撰寫的指令碼必須先進行修改才可在 BigQuery 中使用。使用[批次 SQL 翻譯](https://docs.cloud.google.com/bigquery/docs/batch-sql-translator?hl=zh-tw)大量遷移 SQL 指令碼，或使用[互動式 SQL 翻譯](https://docs.cloud.google.com/bigquery/docs/interactive-sql-translator?hl=zh-tw)翻譯臨時查詢。這兩項工具的[預先發布版](https://cloud.google.com/products?hl=zh-tw#product-launch-stages)都支援 Snowflake SQL。

**注意：** 在某些情況下，Snowflake 和 BigQuery 中的 SQL 元素之間沒有直接對應關係。不過在大多數情況下，您可以使用替代方法，在 BigQuery 中達到 Snowflake 所提供的相同功能，如本文件中的範例所示。

## 資料類型

本節說明 Snowflake 和 BigQuery 中對應的資料類型。

  
  

| Snowflake | BigQuery | 附註 |
| --- | --- | --- |
| `NUMBER/ DECIMAL/NUMERIC` | `NUMERIC/BIGNUMERIC` | 視精確度和比例而定，可對應至 `NUMERIC` 或 `BIGNUMERIC`。   Snowflake 中的 `NUMBER` 資料類型支援 38 位精確度，以及 37 位小數位數。可根據使用者指定精確度和比例。    BigQuery 支援 `NUMERIC` 和 `BIGNUMERIC`，並[在特定範圍內選擇性指定精確度和比例](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#decimal_types)。 |
| [`INT/INTEGER`](https://docs.snowflake.com/en/sql-reference/data-types-numeric.html#int-integer-bigint-smallint-tinyint-byteint) | `BIGNUMERIC` | 和所有其他類似 `INT` 的資料類型 (例如 `BIGINT, TINYINT, SMALLINT, BYTEINT`) 代表 `NUMBER` 資料類型的別名，其中無法指定精確度和比例，且一律為 `NUMBER(38, 0)`    BigQuery 預設會將 `INTEGER` 轉換為 `INT64`。`INT/INTEGER`如要設定 SQL 轉換，將其轉換為其他資料類型，可以使用 [`REWRITE_ZERO_SCALE_NUMERIC_AS_INTEGER` 設定選項](https://docs.cloud.google.com/bigquery/docs/config-yaml-translation?hl=zh-tw#optimize_and_improve_the_performance_of_translated_sql) |
| `BIGINT` | `BIGNUMERIC` |  |
| `SMALLINT` | `BIGNUMERIC` |  |
| `TINYINT` | `BIGNUMERIC` |  |
| `BYTEINT` | `BIGNUMERIC` |  |
| `FLOAT/  FLOAT4/  FLOAT8` | `FLOAT64` | Snowflake 中的 `FLOAT` 資料型別會將「NaN」設為 > X，其中 X 是任何 FLOAT 值 (「NaN」本身除外)。    BigQuery 中的 `FLOAT` 資料類型會將「NaN」設為 < X，其中 X 是任何 FLOAT 值 (「NaN」本身除外)。 |
| `DOUBLE/  DOUBLE PRECISION/`  `REAL` | `FLOAT64` | Snowflake 中的 `DOUBLE` 資料類型與 Snowflake 中的 `FLOAT` 資料類型同義，但通常會錯誤顯示為 `FLOAT`。並妥善儲存為 `DOUBLE`。 |
| `VARCHAR` | `STRING` | Snowflake 中的 `VARCHAR` 資料類型長度上限為 128 MB (未壓縮)。如未指定長度，預設為最大長度。    BigQuery 中的 `STRING` 資料類型會儲存為可變長度的 UTF-8 編碼 Unicode。如要進一步瞭解欄和列的限制，請參閱「[查詢作業](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#query_jobs)」。 |
| `CHAR/CHARACTER` | `STRING` |
| `STRING/TEXT` | `STRING` | Snowflake 中的 `STRING` 資料類型與 Snowflake 的 VARCHAR 同義。 |
| `BINARY` | `BYTES` |  |
| `VARBINARY` | `BYTES` |  |
| `BOOLEAN` | `BOOL` | BigQuery 中的 `BOOL` 資料類型只能接受 `TRUE/FALSE`，不像 Snowflake 中的 `BOOL` 資料類型可以接受 TRUE/FALSE/NULL。 |
| `DATE` | `DATE` | Snowflake 中的 `DATE` 型別接受大多數常見的日期格式，但 BigQuery 中的 `DATE` 型別只接受「YYYY-[M]M-[D]D」格式的日期。 |
| `TIME` | `TIME` | Snowflake 的 TIME 類型支援 0 到 9 奈秒的精確度，而 BigQuery 的 TIME 類型則支援 0 到 6 奈秒的精確度。 |
| `TIMESTAMP` | `DATETIME` | `TIMESTAMP` 是使用者可設定的別名，預設為 `TIMESTAMP_NTZ`，對應至 BigQuery 中的 `DATETIME`。 |
| `TIMESTAMP_LTZ` | `TIMESTAMP` |  |
| `TIMESTAMP_NTZ/DATETIME` |
| `DATETIME` |  |
| `TIMESTAMP_TZ` | `TIMESTAMP` |  |
| `OBJECT` | `JSON` |  |
| `VARIANT` | `JSON` |  |
| `ARRAY` | `ARRAY<JSON>` | SQL 翻譯服務會保留型別陣列的資料型別。如果是未輸入型別的陣列 (例如 `ARRAY<VARIANT>`)，BigQuery 會將這些陣列轉換為 `ARRAY<JSON>` |

BigQuery 也有下列資料類型，但沒有直接對應的 Snowflake 類型：

* [`DATETIME`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#datetime_type)
* [`GEOGRAPHY`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#geography_type)

## `CREATE FUNCTION` 語法

下表說明 Snowflake 和 BigQuery 之間 SQL UDF 建立語法的差異。

| **雪花** | BigQuery |
| --- | --- |
| `CREATE [ OR REPLACE ] FUNCTION`  `function_name`  `([sql_arg_name sql_arg_data_type[,..]])`  `RETURNS data_type`  `AS sql_function_definition`  `s` | `CREATE [OR REPLACE] FUNCTION function_name`  `([sql_arg_name sql_arg_data_type[,..]])`  `AS sql_function_definition`   注意：在 BigQuery [SQL UDF](https://docs.cloud.google.com/bigquery/docs/user-defined-functions?hl=zh-tw#sql-udf-structure) 中，傳回資料類型為選用項目。當查詢呼叫函式時，BigQuery 會從 SQL 函式主體推測出函式的結果類型。 |
| `CREATE [OR REPLACE] FUNCTION`  `function_name`  `([sql_arg_name sql_arg_data_type[,..]])`  `RETURNS TABLE (col_name, col_data_type[,..])`  `AS sql_function_definition` | `CREATE [OR REPLACE] FUNCTION function_name`  `([sql_arg_name sql_arg_data_type[,..]])`  `RETURNS data_type`  `AS sql_function_definition`   注意：BigQuery [SQL UDF](https://docs.cloud.google.com/bigquery/docs/user-defined-functions?hl=zh-tw#sql-udf-structure) 不支援傳回資料表類型，但這項功能已列入產品藍圖，很快就會推出。不過，BigQuery 支援傳回 STRUCT 類型的 ARRAY。 |
| `CREATE [SECURE] FUNCTION`  `function_name`  `([sql_arg_name sql_arg_data_type[,..]])`  `RETURNS data_type`  `AS sql_function_definition`   注意：Snowflake 提供安全選項，可將 UDF 定義和詳細資料限制為僅供授權使用者存取 (即獲派檢視擁有者角色的使用者)。 | `CREATE FUNCTION`  `function_name`  `([sql_arg_name sql_arg_data_type[,..]])`  `RETURNS data_type`  `AS sql_function_definition`   注意：函式安全性不是 BigQuery 中可設定的參數。BigQuery 支援建立 IAM 角色和權限，限制對基礎資料和函式定義的存取權。 |
| `CREATE [OR REPLACE] FUNCTION`  `function_name`  `([sql_arg_name sql_arg_data_type[,..]])`  `RETURNS data_type`  `[ { CALLED ON NULL INPUT | { RETURNS NULL ON NULL INPUT | STRICT } } ]`  `AS sql_function_definition` | `CREATE [OR REPLACE] FUNCTION function_name`  `([sql_arg_name sql_arg_data_type[,..]])`  `RETURNS data_type`  `AS sql_function_definition`   注意：BigQuery 會隱含處理空值輸入的函式行為，因此不必指定為個別選項。 |
| `CREATE [OR REPLACE] FUNCTION`  `function_name`  `([sql_arg_name sql_arg_data_type[,..]])`  `RETURNS data_type`  `[VOLATILE | IMMUTABLE]`  `AS sql_function_definition` | `CREATE [OR REPLACE] FUNCTION`  `function_name`  `([sql_arg_name sql_arg_data_type[,..]])`  `RETURNS data_type`  `AS sql_function_definition`   注意：BigQuery 中無法設定函式變動性參數。所有 BigQuery UDF 變動性都等同於 Snowflake 的 `IMMUTABLE` 變動性 (也就是說，不會進行資料庫查詢，也不會使用引數清單中未直接提供的資訊)。 |
| `CREATE [OR REPLACE] FUNCTION`  `function_name`  `([sql_arg_name sql_arg_data_type[,..]])`  `RETURNS data_type`  `AS [' | $$]`  `sql_function_definition`  `[' | $$]` | `CREATE [OR REPLACE] FUNCTION`   `function_name`  `([sql_arg_name sql_arg_data_type[,..]])`  `RETURNS data_type`  `AS sql_function_definition`   注意：使用單引號或字元序列 (例如以錢幣符號引號括住)$$) is not required or supported in BigQuery. BigQuery implicitly interprets the SQL expression. |
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
| `CREATE [OR REPLACE] PROCEDURE`  `procedure_name`  `([arg_name arg_data_type[,..]])`  `RETURNS data_type`  `[{CALLED ON NULL INPUT | {RETURNS NULL ON NULL INPUT | STRICT}}]`  `AS procedure_definition;` | `CREATE [OR REPLACE] PROCEDURE`  `procedure_name`  `([arg_name arg_data_type[,..]])`  `BEGIN`  `procedure_definition`  `END;`   注意：BigQuery 會隱含處理空值輸入的程序行為，因此不必指定為個別選項。 |
| `CREATE [OR REPLACE] PROCEDURE`  `procedure_name`  `([arg_name arg_data_type[,..]])`  `RETURNS data_type`  `[VOLATILE | IMMUTABLE]`  `AS procedure_definition;` | `CREATE [OR REPLACE] PROCEDURE`  `procedure_name`  `([arg_name arg_data_type[,..]])`  `BEGIN`  `procedure_definition`  `END;`   注意：程序變異性不是 BigQuery 中的可設定參數。這相當於 Snowflake 的 `IMMUTABLE` 波動性。 |
| `CREATE [OR REPLACE] PROCEDURE`  `procedure_name`  `([arg_name arg_data_type[,..]])`  `RETURNS data_type`  `[COMMENT = '<string_literal>']`  `AS procedure_definition;` | `CREATE [OR REPLACE] PROCEDURE`  `procedure_name`  `([arg_name arg_data_type[,..]])`  `BEGIN`  `procedure_definition`  `END;`   注意：BigQuery 不支援在程序定義中加入註解或說明。 |
| `CREATE [OR REPLACE] PROCEDURE`  `procedure_name`  `([arg_name arg_data_type[,..]])`  `RETURNS data_type`  `[EXECUTE AS { CALLER | OWNER }]`  `AS procedure_definition;`   注意：Snowflake 支援指定程序的呼叫端或擁有者，以利執行作業 | `CREATE [OR REPLACE] PROCEDURE`  `procedure_name`  `([arg_name arg_data_type[,..]])`  `BEGIN`  `procedure_definition`  `END;`   注意：BigQuery 預存程序一律會以呼叫端身分執行 |

BigQuery 也支援 `CREATE PROCEDURE IF NOT EXISTS` 陳述式，如果已有名稱相同的函式，系統會將查詢視為成功執行且不採取任何動作。

### `DROP PROCEDURE` 語法

下表說明 Snowflake 和 BigQuery 之間 DROP FUNCTION 語法的差異。

| **雪花** | BigQuery |
| --- | --- |
| `DROP PROCEDURE [IF EXISTS]`  `procedure_name`  `([arg_data_type, ... ])` | `DROP PROCEDURE [IF EXISTS] dataset_name.procedure_name`   注意：BigQuery 不會要求使用程序的簽章 (引數資料類型) 刪除程序。 |

如果程序並非位在目前專案中，BigQuery 會要求您指定 `project_name`。

### 其他程序指令

Snowflake 提供其他指令，例如 [`ALTER PROCEDURE`](https://docs.snowflake.net/manuals/sql-reference/sql/alter-procedure.html)、[`DESC[RIBE] PROCEDURE`](https://docs.snowflake.net/manuals/sql-reference/sql/desc-procedure.html) 和 [`SHOW PROCEDURES`](https://docs.snowflake.net/manuals/sql-reference/sql/show-procedures.html)，可管理預存程序。BigQuery 不支援這些功能。

## 中繼資料和交易 SQL 陳述式

| **雪花** | BigQuery |
| --- | --- |
| `BEGIN [ { WORK | TRANSACTION } ] [ NAME <name> ]; START_TRANSACTION [ name <name> ];` | BigQuery 一律使用快照隔離。詳情請參閱本文件其他部分的「[一致性保證](#consistency-guarantees-and-transaction-isolation)」。 |
| `COMMIT;` | BigQuery 不會使用這項資訊。 |
| `ROLLBACK;` | BigQuery 未使用 |
| `SHOW LOCKS [ IN ACCOUNT ]; SHOW TRANSACTIONS [ IN ACCOUNT ]; Note: If the user has the ACCOUNTADMIN role, the user can see locks/transactions for all users in the account.` | BigQuery 不會使用這項資訊。 |

## 多陳述式和多行 SQL 陳述式

Snowflake 和 BigQuery 都支援交易 (工作階段)，因此支援以半形分號分隔的陳述式，這些陳述式會一併執行。詳情請參閱「[多重陳述式交易](https://docs.cloud.google.com/bigquery/docs/transactions?hl=zh-tw)」。

## 暫存檔案的中繼資料欄

Snowflake 會自動為內部和外部階段中的檔案產生中繼資料。這類中繼資料可[查詢](https://docs.snowflake.net/manuals/user-guide/querying-stage.html)及[載入](https://docs.snowflake.net/manuals/sql-reference/sql/copy-into-table.html)至資料表，與一般資料欄並列。可使用的中繼資料欄如下：

* [METADATA$FILENAME](https://docs.snowflake.net/manuals/user-guide/querying-metadata.html#metadata-columns)
* [METADATA$FILE\_ROW\_NUMBER](https://docs.snowflake.net/manuals/user-guide/querying-metadata.html#metadata-columns)

## 一致性保證和交易隔離

Snowflake 和 BigQuery 都是不可分割的，也就是說，在多個資料列中，每個變動層級都符合 ACID 標準。

### 交易

系統會為每筆 Snowflake 交易指派不重複的開始時間 (包括毫秒)，並將其設為交易 ID。Snowflake 僅支援 [`READ COMMITTED`](https://docs.snowflake.net/manuals/sql-reference/transactions.html#read-committed-isolation) 隔離層級。不過，如果兩個陳述式都位於同一項交易中，即使變更尚未提交，陳述式仍可查看其他陳述式所做的變更。修改資源 (資料表) 時，Snowflake 交易會取得資源的鎖定。使用者可以調整封鎖陳述式等待逾時的時間上限。如果啟用 [`AUTOCOMMIT`](https://docs.snowflake.net/manuals/sql-reference/parameters.html#autocommit) 參數，系統會自動提交 DML 陳述式。

BigQuery 也[支援交易](https://docs.cloud.google.com/bigquery/docs/transactions?hl=zh-tw)。BigQuery 可透過[快照隔離](https://en.wikipedia.org/wiki/Snapshot_isolation)確保[樂觀並行控制](https://en.wikipedia.org/wiki/Optimistic_concurrency_control) (先提交者勝出)，查詢會讀取查詢開始前最後提交的資料。這種做法可確保每列、每次變異和相同 DML 陳述式中的資料列都具有相同的一致性，同時避免死結。如果針對同一個資料表進行多項 DML 更新，BigQuery 會改用[悲觀並行控制](https://docs.cloud.google.com/bigquery/docs/data-manipulation-language?hl=zh-tw#dml-limitations)。載入工作可以完全獨立執行，並附加至資料表。不過，BigQuery 不提供明確的交易界線或工作階段。

## 復原

如果 Snowflake 交易的工作階段在交易提交或復原前意外終止，交易就會處於分離狀態。使用者應執行 SYSTEM$ABORT\_TRANSACTION，中止已分離的交易，否則 Snowflake 會在閒置四小時後復原已分離的交易。如果發生死結，Snowflake 會偵測到死結，並選取較新的陳述式來復原。如果明確開啟的交易中，DML 陳述式失敗，系統會復原變更，但交易會保持開啟狀態，直到確認或復原為止。Snowflake 中的 DDL 陳述式會自動提交，因此無法回溯。

BigQuery 支援 [`ROLLBACK TRANSACTION` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/procedural-language?hl=zh-tw#rollback_transaction)。BigQuery 中沒有 [`ABORT` 陳述式](https://docs.teradata.com/reader/huc7AEHyHSROUkrYABqNIg/c6KYQ4ySu4QTCkKS4f5A2w)。

## 資料庫限制

請務必查看 [BigQuery 公開說明文件](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)，瞭解最新的配額和限制。如要提高大量使用者的許多配額，請與 Cloud 支援團隊聯絡。

所有 Snowflake 帳戶預設都會設定軟性限制。軟性限制是在建立帳戶時設定，且可能有所不同。許多 Snowflake 軟性限制都可以透過 Snowflake 帳戶團隊或支援單提高。

下表比較 Snowflake 和 BigQuery 的資料庫限制。

| **限制** | **雪花** | BigQuery |
| --- | --- | --- |
| 查詢文字大小 | 1 MB | 1 MB |
| 並行查詢數量上限 | XS Warehouse - 8  S Warehouse - 16  M Warehouse - 32  *L Warehouse - 64  XL Warehouse - 128* | 100 |




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-02 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-02 (世界標準時間)。"],[],[]]