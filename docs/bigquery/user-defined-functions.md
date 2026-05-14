Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 使用者定義函式

使用者定義函式 (UDF) 可讓您使用 SQL 運算式或 JavaScript 程式碼建立函式。UDF 可接受輸入資料欄、對輸入內容執行動作，並將執行結果以值的形式傳回。

您可以將 UDF 定義為永久或暫時函式。您可以在多項查詢中重複使用永久 UDF，而單項查詢的範圍內只能有一個暫時性 UDF。

**注意：** 如果擁有者之間共用持續性 UDF，可以安全地呼叫這些 UDF。UDF 無法變更資料、與外部系統通訊，或將記錄傳送至 Google Cloud Observability 或類似應用程式。

如要建立 UDF，請使用 [`CREATE FUNCTION`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#create_function_statement) 陳述式。如要刪除永久使用者定義函式，請使用 [`DROP FUNCTION`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#drop_function_statement) 陳述式。暫時性 UDF 會在查詢完成時立即失效。`DROP
FUNCTION` 陳述式僅適用於[多重陳述式查詢](https://docs.cloud.google.com/bigquery/docs/multi-statement-queries?hl=zh-tw)和[程序](https://docs.cloud.google.com/bigquery/docs/procedures?hl=zh-tw)中的暫時性 UDF。

如要瞭解舊版 SQL 中的 UDF，請參閱[舊版 SQL 中的使用者定義函式](https://docs.cloud.google.com/bigquery/docs/user-defined-functions-legacy?hl=zh-tw)。

## SQL UDF

下列範例會建立名為 `AddFourAndDivide` 的暫時性 SQL UDF，並從 `SELECT` 陳述式中呼叫該 UDF：

```
CREATE TEMP FUNCTION AddFourAndDivide(x INT64, y INT64)
RETURNS FLOAT64
AS (
  (x + 4) / y
);

SELECT
  val, AddFourAndDivide(val, 2)
FROM
  UNNEST([2,3,5,8]) AS val;
```

這個範例會產生下列輸出內容：

```
+-----+-----+
| val | f0_ |
+-----+-----+
|   2 | 3.0 |
|   3 | 3.5 |
|   5 | 4.5 |
|   8 | 6.0 |
+-----+-----+
```

下一個範例會建立與永久 UDF 相同的函式：

```
CREATE FUNCTION mydataset.AddFourAndDivide(x INT64, y INT64)
RETURNS FLOAT64
AS (
  (x + 4) / y
);
```

由於這個 UDF 是永久性的，因此您必須為函式指定資料集 (本例中為 `mydataset`)。執行 `CREATE FUNCTION` 陳述式後，即可從查詢呼叫函式：

```
SELECT
  val, mydataset.AddFourAndDivide(val, 2)
FROM
  UNNEST([2,3,5,8,12]) AS val;
```

### 範本 SQL UDF 參數

類型等於 `ANY TYPE` 的參數可以在呼叫函式時比對多個引數類型。

* 如有多項參數的類型均為 `ANY TYPE`，則 BigQuery 不會強制在這些引數之間建立任何類型的關係。
* 函式傳回類型不得為 `ANY TYPE`。您必須省略傳回類型，也就是由系統依據 `sql_expression` 自動決定類型，或指定明確的類型。
* 如果您傳送的函式引數類型與函式定義不相容，系統會在函式呼叫時產生錯誤。

下方範例顯示了使用範本參數的 SQL UDF。

```
CREATE TEMP FUNCTION addFourAndDivideAny(x ANY TYPE, y ANY TYPE)
AS (
  (x + 4) / y
);

SELECT
  addFourAndDivideAny(3, 4) AS integer_input,
  addFourAndDivideAny(1.59, 3.14) AS floating_point_input;
```

這個範例會產生下列輸出內容：

```
+----------------+-----------------------+
| integer_input  |  floating_point_input |
+----------------+-----------------------+
| 1.75           | 1.7802547770700636    |
+----------------+-----------------------+
```

下一個範例使用範本參數，傳回任意類型陣列中的最後一項元素：

```
CREATE TEMP FUNCTION lastArrayElement(arr ANY TYPE)
AS (
  arr[ORDINAL(ARRAY_LENGTH(arr))]
);

SELECT
  lastArrayElement(x) AS last_element
FROM (
  SELECT [2,3,5,8,13] AS x
);
```

這個範例會產生下列輸出內容：

```
+--------------+
| last_element |
+--------------+
| 13           |
+--------------+
```

### Scalar subquery

SQL UDF 可以傳回[純量子查詢](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/subqueries?hl=zh-tw#scalar_subquery_concepts)的值。純量子查詢必須選取單一資料欄。

以下範例顯示的 SQL UDF 會使用純量子查詢，計算使用者資料表中特定年齡的使用者人數：

```
CREATE TEMP TABLE users
AS (
  SELECT
    1 AS id, 10 AS age
  UNION ALL
  SELECT
    2 AS id, 30 AS age
  UNION ALL
  SELECT
    3 AS id, 10 AS age
);

CREATE TEMP FUNCTION countUserByAge(userAge INT64)
AS (
  (SELECT COUNT(1) FROM users WHERE age = userAge)
);

SELECT
  countUserByAge(10) AS count_user_age_10,
  countUserByAge(20) AS count_user_age_20,
  countUserByAge(30) AS count_user_age_30;
```

這個範例會產生下列輸出內容：

```
+-------------------+-------------------+-------------------+
| count_user_age_10 | count_user_age_20 | count_user_age_30 |
+-------------------+-------------------+-------------------+
|                 2 |                 0 |                 1 |
+-------------------+-------------------+-------------------+
```

### SQL 運算式中的預設專案

在 SQL UDF 的主體中，除非實體位於包含 UDF 的專案中，否則任何對 BigQuery 實體 (例如資料表或檢視區塊) 的參照都必須包含專案 ID。

舉例來說，請看以下陳述：

```
CREATE FUNCTION project1.mydataset.myfunction()
AS (
  (SELECT COUNT(*) FROM mydataset.mytable)
);
```

如果您從 `project1` 執行這項陳述式，且 `project1` 存在於 `project1` 中，則陳述式會成功執行。`mydataset.mytable`不過，如果您從其他專案執行這項陳述式，陳述式就會失敗。如要修正錯誤，請在表格參照中加入專案 ID：

```
CREATE FUNCTION project1.mydataset.myfunction()
AS (
  (SELECT COUNT(*) FROM project1.mydataset.mytable)
);
```

您也可以參照與建立函式時不同的專案或資料集中的實體：

```
CREATE FUNCTION project1.mydataset.myfunction()
AS (
  (SELECT COUNT(*) FROM project2.another_dataset.another_table)
);
```

### 搭配 SQL UDF 使用系統變數

SQL UDF 支援 `@@session_id` 和 `@@location`
[系統變數](https://docs.cloud.google.com/bigquery/docs/reference/system-variables?hl=zh-tw)。您可以在函式建立陳述式中的任何位置加入這些系統變數，傳回目前查詢的會期 ID 或位置。系統不支援其他系統變數。

## JavaScript UDF

JavaScript UDF 可讓您從 SQL 查詢呼叫以 JavaScript 編寫的程式碼。與標準 SQL 查詢相比，JavaScript UDF 通常會耗用更多 slot 資源，導致工作效能降低。如果函式可以 SQL 表示，通常以標準 SQL 查詢作業的形式執行程式碼會更理想。

以下範例顯示 JavaScript UDF。JavaScript 程式碼會以[原始字串](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/lexical?hl=zh-tw#string_and_bytes_literals)的形式加上引號。

```
CREATE TEMP FUNCTION multiplyInputs(x FLOAT64, y FLOAT64)
RETURNS FLOAT64
LANGUAGE js
AS r"""
  return x*y;
""";

WITH numbers AS
  (SELECT 1 AS x, 5 as y
  UNION ALL
  SELECT 2 AS x, 10 as y
  UNION ALL
  SELECT 3 as x, 15 as y)
SELECT x, y, multiplyInputs(x, y) AS product
FROM numbers;
```

這個範例會產生下列輸出內容：

```
+-----+-----+--------------+
| x   | y   | product      |
+-----+-----+--------------+
| 1   | 5   | 5            |
| 2   | 10  | 20           |
| 3   | 15  | 45           |
+-----+-----+--------------+
```

下一個範例會將指定 JSON 字串中名為「foo」的所有欄位值加總。`foo`

```
CREATE TEMP FUNCTION SumFieldsNamedFoo(json_row STRING)
RETURNS FLOAT64
LANGUAGE js
AS r"""
  function SumFoo(obj) {
    var sum = 0;
    for (var field in obj) {
      if (obj.hasOwnProperty(field) && obj[field] != null) {
        if (typeof obj[field] == "object") {
          sum += SumFoo(obj[field]);
        } else if (field == "foo") {
          sum += obj[field];
        }
      }
    }
    return sum;
  }
  var row = JSON.parse(json_row);
  return SumFoo(row);
""";

WITH Input AS (
  SELECT
    STRUCT(1 AS foo, 2 AS bar, STRUCT('foo' AS x, 3.14 AS foo) AS baz) AS s,
    10 AS foo
  UNION ALL
  SELECT
    NULL,
    4 AS foo
  UNION ALL
  SELECT
    STRUCT(NULL, 2 AS bar, STRUCT('fizz' AS x, 1.59 AS foo) AS baz) AS s,
    NULL AS foo
)
SELECT
  TO_JSON_STRING(t) AS json_row,
  SumFieldsNamedFoo(TO_JSON_STRING(t)) AS foo_sum
FROM Input AS t;
```

這個範例會產生下列輸出內容：

```
+---------------------------------------------------------------------+---------+
| json_row                                                            | foo_sum |
+---------------------------------------------------------------------+---------+
| {"s":{"foo":1,"bar":2,"baz":{"x":"foo","foo":3.14}},"foo":10}       | 14.14   |
| {"s":null,"foo":4}                                                  | 4       |
| {"s":{"foo":null,"bar":2,"baz":{"x":"fizz","foo":1.59}},"foo":null} | 1.59    |
+---------------------------------------------------------------------+---------+
```

### 支援的 JavaScript UDF 資料類型

有些 SQL 類型可以直接對應至 JavaScript 類型，其他類型則不能。BigQuery 會以下列方式表示類型：

| BigQuery 資料類型 | JavaScript 資料類型 |
| --- | --- |
| ARRAY | ARRAY |
| BOOL | BOOLEAN |
| BYTES | base64 編碼的 STRING |
| FLOAT64 | 數字 |
| NUMERIC、BIGNUMERIC | 如果 NUMERIC 或 BIGNUMERIC 值能夠以 [IEEE 754 浮點](https://en.wikipedia.org/wiki/Floating-point_arithmetic#IEEE_754:_floating_point_in_modern_computers)值準確表示，且沒有任何小數部分，則可以當成數字加以編碼。這些值的範圍必須是 [-253, 253]。否則，該值會編碼為字串。 |
| STRING | STRING |
| STRUCT | OBJECT，其中每個 STRUCT 欄位都是已命名欄位 |
| TIMESTAMP | DATE，其微秒欄位包含時間戳記的 `microsecond` 部分 |
| DATE | DATE |
| JSON | JSON 物件、陣列和值會轉換為對等的 JavaScript 物件、陣列和值。  JavaScript 不支援 INT64 值。只有在 [-253, 253] 範圍內的 JSON 數字會精確轉換。否則，系統會將數值四捨五入，導致精確度降低。 |

因為 JavaScript 不支援 64 位元整數類型，因此 JavaScript UDF 也不支援使用 `INT64` 的輸入類型。請改用 `FLOAT64` 將整數值以數字表示，或用 `STRING` 將整數值以字串表示。

BigQuery 不支援 `INT64` 做為 JavaScript UDF 中的傳回類型。在這種情況下，JavaScript 函式主體可以傳回 JavaScript 數字或字串。然後，BigQuery 會將這兩種類型轉換成 `INT64`。

如果 JavaScript UDF 的傳回值為 [`Promise`](https://tc39.es/ecma262/#sec-promise-objects)，BigQuery 會等到 `Promise` 安定下來為止。`Promise`如果安定下來的 `Promise` 處於完成狀態，則 BigQuery 傳回其結果。如果安定下來的 `Promise` 處於遭拒狀態，BigQuery 就會傳回錯誤。

### 引號規則

您必須使用引號包覆 JavaScript 程式碼。對於單行程式碼片段，您可以使用標準的加引號字串：

```
CREATE TEMP FUNCTION plusOne(x FLOAT64)
RETURNS FLOAT64
LANGUAGE js
AS "return x+1;";

SELECT val, plusOne(val) AS result
FROM UNNEST([1, 2, 3, 4, 5]) AS val;
```

這個範例會產生下列輸出內容：

```
+-----------+-----------+
| val       | result    |
+-----------+-----------+
| 1         | 2.0       |
| 2         | 3.0       |
| 3         | 4.0       |
| 4         | 5.0       |
| 5         | 6.0       |
+-----------+-----------+
```

如果程式碼片段包含引號，或者由多行組成，請使用加三引號的區塊：

```
CREATE TEMP FUNCTION customGreeting(a STRING)
RETURNS STRING
LANGUAGE js
AS r"""
  var d = new Date();
  if (d.getHours() < 12) {
    return 'Good Morning, ' + a + '!';
  } else {
    return 'Good Evening, ' + a + '!';
  }
""";

SELECT customGreeting(names) AS everyone
FROM UNNEST(['Hannah', 'Max', 'Jakob']) AS names;
```

這個範例會產生下列輸出內容：

```
+-----------------------+
| everyone              |
+-----------------------+
| Good Morning, Hannah! |
| Good Morning, Max!    |
| Good Morning, Jakob!  |
+-----------------------+
```

### 加入 JavaScript 程式庫

您可以使用 `OPTIONS` 區段來擴充 JavaScript UDF，這個區段可讓您為 UDF 指定外部程式碼資料庫。

```
CREATE TEMP FUNCTION myFunc(a FLOAT64, b STRING)
RETURNS STRING
LANGUAGE js
  OPTIONS (
    library=['gs://my-bucket/path/to/lib1.js', 'gs://my-bucket/path/to/lib2.js'])
AS r"""
  // Assumes 'doInterestingStuff' is defined in one of the library files.
  return doInterestingStuff(a, b);
""";

SELECT myFunc(3.14, 'foo');
```

在前例中，`lib1.js` 和 `lib2.js` 中的程式碼均可供 UDF `[external_code]` 區段的任何程式碼使用。

### JavaScript UDF 的最佳做法

**預先篩選您的輸入內容**

如果輸入內容在傳遞到 JavaScript UDF 之前，能夠輕易地進行篩選，您查詢的執行速度可能會更快，費用也可能會更便宜。

**避免永久的可變動狀態**

請勿在不同的 JavaScript UDF 呼叫之間儲存或存取可變動的狀態。舉例來說，請避免以下模式：

```
-- Avoid this pattern
CREATE FUNCTION temp.mutable()
RETURNS INT64
LANGUAGE js
AS r"""
  var i = 0; // Mutable state
  function dontDoThis() {
    return ++i;
  }
  return dontDoThis()
""";
```

**有效率地使用記憶體**

JavaScript 處理環境限制了每個查詢可用的記憶體。
如果 JavaScript UDF 查詢累積過多本機狀態，可能會因記憶體耗盡而失敗。

## 授權處理常式

您可以將 UDF 授權為*常式*。授權常式可讓您與特定使用者或群組分享查詢結果，而不授予他們產生結果的基礎資料表存取權。舉例來說，授權常式可以計算資料的匯總值，或查閱資料表值並用於計算。詳情請參閱「[已授權的日常安排](https://docs.cloud.google.com/bigquery/docs/authorized-routines?hl=zh-tw)」。

## 為 UDF 新增說明

如要為 UDF 新增說明，請按照下列步驟操作：

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。

   如果沒有看到左側窗格，請按一下 last\_page「Expand left pane」(展開左側窗格)，開啟窗格。
3. 在「Explorer」窗格中展開專案，然後按一下「Datasets」(資料集)。
4. 按一下資料集。您也可以使用搜尋功能或篩選器尋找資料集。
5. 按一下「常式」分頁標籤，然後選取所需功能。
6. 在詳細資料窗格中，按一下「編輯日常安排詳細資料」mode\_edit，編輯說明文字。
7. 在對話方塊中輸入說明，或編輯現有的說明。按一下「儲存」即可儲存新的說明文字。

### SQL

如要更新函式的說明，請使用 [`CREATE FUNCTION` DDL 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#create_function_statement)重新建立函式，並在 `OPTIONS` 清單中設定 `description` 欄位：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列陳述式：

   ```
   CREATE OR REPLACE FUNCTION mydataset.my_function(...)
   AS (
     ...
   ) OPTIONS (
     description = 'DESCRIPTION'
   );
   ```
3. 按一下「執行」play\_circle。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

## 建立自訂遮蓋常式

**注意：** 使用以特定 BigQuery 版本建立的預留項目時，這項功能可能無法使用。如要進一步瞭解各版本啟用的功能，請參閱「[BigQuery 版本簡介](https://docs.cloud.google.com/bigquery/docs/editions-intro?hl=zh-tw)」。

您可以建立 UDF，用於[自訂遮蓋常式](https://docs.cloud.google.com/bigquery/docs/column-data-masking-intro?hl=zh-tw#custom_mask)。您應建立專屬資料集，並設定適當的 IAM 權限，以管理遮蓋 UDF。自訂遮蓋常式必須符合下列規定：

* 自訂遮蓋常式必須是 SQL UDF。
* 在 `OPTIONS` 函式中，`data_governance_type` 選項必須設為 `DATA_MASKING`。
* 自訂遮蓋常式支援下列函式：
  + [`AEAD.DECRYPT_BYTES`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/aead_encryption_functions?hl=zh-tw#aeaddecrypt_bytes) AEAD 加密函式 (不支援原始金鑰用法)`KEYS.KEYSET_CHAIN`
  + [`AEAD.DECRYPT_STRING`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/aead_encryption_functions?hl=zh-tw#aeaddecrypt_string) AEAD 加密函式 (不支援原始金鑰用法)`KEYS.KEYSET_CHAIN`
  + [`AEAD.ENCRYPT`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/aead_encryption_functions?hl=zh-tw#aeadencrypt) 使用 keyset\_chain 的 AEAD 加密函式 (不支援原始金鑰用法)
  + [`CAST`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/conversion_functions?hl=zh-tw#cast)
    轉換函式
  + [`CONCAT`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/string_functions?hl=zh-tw#concat)
    字串函式
  + [`CURRENT_DATETIME`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/datetime_functions?hl=zh-tw#current_datetime)
    日期時間函式
  + [`CURRENT_DATE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/date_functions?hl=zh-tw#current_date)
    日期函式
  + [`CURRENT_TIMESTAMP`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/timestamp_functions?hl=zh-tw#current_timestamp)
    時間戳記函式
  + [`CURRENT_TIME`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/time_functions?hl=zh-tw#current_time)
    時間函式
  + [`DETERMINISTIC_DECRYPT_BYTES`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/aead_encryption_functions?hl=zh-tw#deterministic_decrypt_bytes) AEAD 加密函式 (不支援原始金鑰用法)`KEYS.KEYSET_CHAIN`
  + [`DETERMINISTIC_DECRYPT_STRING`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/aead_encryption_functions?hl=zh-tw#deterministic_decrypt_string) AEAD 加密函式 (不支援原始金鑰用法)`KEYS.KEYSET_CHAIN`
  + [`DETERMINISTIC_ENCRYPT`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/aead_encryption_functions?hl=zh-tw#deterministic_encrypt) AEAD 加密函式 (不支援原始金鑰用法)`KEYS.KEYSET_CHAIN`
  + [`FARM_FINGERPRINT`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/hash_functions?hl=zh-tw#farm_fingerprint)
    雜湊函式
  + [`FROM_BASE32`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/string_functions?hl=zh-tw#from_base32)
    字串函式
  + [`FROM_BASE64`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/string_functions?hl=zh-tw#from_base64)
    字串函式
  + [`FROM_HEX`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/string_functions?hl=zh-tw#from_hex)
    字串函式
  + [`GENERATE_UUID`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/utility-functions?hl=zh-tw#generate_uuid)
    公用函式
  + [`KEYS.KEYSET_CHAIN`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/aead_encryption_functions?hl=zh-tw#keyskeyset_chain) AEAD 加密函式
  + [`LENGTH`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/string_functions?hl=zh-tw#length) 字串函式
  + [`LOWER`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/string_functions?hl=zh-tw#lower)
    字串函式
  + [`LPAD`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/string_functions?hl=zh-tw#lpad)
    字串函式
  + [`LTRIM`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/string_functions?hl=zh-tw#ltrim)
    字串函式
  + [`MD5`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/hash_functions?hl=zh-tw#md5)
    雜湊函式
  + [`REGEXP_REPLACE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/string_functions?hl=zh-tw#regexp_replace)
    字串函式
  + [`REGEXP_EXTRACT`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/string_functions?hl=zh-tw#regexp_extract)
    字串函式
  + [`REPLACE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/string_functions?hl=zh-tw#replace)
    字串函式
  + [`RPAD`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/string_functions?hl=zh-tw#rpad)
    字串函式
  + [`RTRIM`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/string_functions?hl=zh-tw#rtrim)
    字串函式
  + [`SAFE_CAST`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/conversion_functions?hl=zh-tw#safe_casting) 轉換函式
  + [`SHA1`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/hash_functions?hl=zh-tw#sha1)
    雜湊函式
  + [`SHA256`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/hash_functions?hl=zh-tw#sha256)
    雜湊函式
  + [`SHA512`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/hash_functions?hl=zh-tw#sha512)
    雜湊函式
  + [`STARTS_WITH`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/string_functions?hl=zh-tw#starts_with) 字串函式
  + [`SUBSTRING`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/string_functions?hl=zh-tw#substring)
    字串函式
  + [`SUBSTR`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/string_functions?hl=zh-tw#substr) 字串函式
  + [`TO_BASE32`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/string_functions?hl=zh-tw#to_base32)
    字串函式
  + [`TO_BASE64`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/string_functions?hl=zh-tw#to_base64)
    字串函式
  + [`TO_HEX`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/string_functions?hl=zh-tw#to_hex)
    字串函式
  + [`TRIM`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/string_functions?hl=zh-tw#trim)
    字串函式
  + [`UPPER`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/string_functions?hl=zh-tw#upper)
    字串函式
* 自訂遮蓋常式可接受零個或一個 [BigQuery 資料型別](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw)的輸入內容，但 `GEOGRAPHY` 和 `STRUCT` 除外。自訂遮蓋常式不支援 `GEOGRAPHY` 和 `STRUCT`。
* 不支援[範本 SQL UDF 參數](https://docs.cloud.google.com/bigquery/docs/user-defined-functions?hl=zh-tw#templated-sql-udf-parameters)。
* 提供輸入內容時，輸入和輸出資料類型必須相同。
* 必須提供輸出類型。
* 定義主體中不得參照其他 UDF、子查詢、資料表或檢視區塊。
* 建立遮蓋常式後，常式就無法變更為標準函式。也就是說，如果 `data_governance_type` 選項設為 `DATA_MASKING`，您就無法使用 DDL 陳述式或 API 呼叫變更 `data_governance_type`。
* 自訂遮蓋常式支援 [CASE](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/conditional_expressions?hl=zh-tw#case) 和 [CASE expr](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/conditional_expressions?hl=zh-tw#case_expr) 陳述式。下列運算子可與 `CASE` 和 `CASE expr` 陳述式搭配使用：
  + [`Comparison Operators`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/operators?hl=zh-tw#comparison_operators) - `<`、`<=`、`>`、`>=`、`=`、`!=`、`IN`
  + [`Logical Operators`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/operators?hl=zh-tw#logical_operators) - `AND`、`OR`、`NOT`
  + [`IS Operator`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/operators?hl=zh-tw#is_operators)

舉例來說，如果遮蓋常式會將使用者的身分證字號替換為 `XXX-XX-XXXX`，看起來會如下所示：

```
  CREATE OR REPLACE FUNCTION SSN_Mask(ssn STRING) RETURNS STRING
  OPTIONS (data_governance_type="DATA_MASKING") AS (
  SAFE.REGEXP_REPLACE(ssn, '[0-9]', 'X') # 123-45-6789 -> XXX-XX-XXXX
  );
```

以下範例使用 [`SHA256`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/hash_functions?hl=zh-tw#sha256) 函式，並以使用者提供的 [salt](https://en.wikipedia.org/wiki/Salt_(cryptography)) 進行雜湊：

```
CREATE OR REPLACE FUNCTION `project.dataset.masking_routine1`(
  ssn STRING)
RETURNS STRING OPTIONS (data_governance_type = 'DATA_MASKING')
AS (
  CAST(SHA256(CONCAT(ssn, 'salt')) AS STRING format 'HEX')
);
```

以下範例會使用常數值遮蓋 `DATETIME` 資料欄：

```
CREATE OR REPLACE FUNCTION `project.dataset.masking_routine2`(
  column DATETIME)
RETURNS DATETIME OPTIONS (data_governance_type = 'DATA_MASKING')
AS (
  SAFE_CAST('2023-09-07' AS DATETIME)
);
```

**最佳做法是盡可能使用 [`SAFE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/functions-reference?hl=zh-tw#safe_prefix) 前置字元，避免透過錯誤訊息公開原始資料。**

建立自訂遮蓋常式後，即可在「建立資料政策」中做為遮蓋規則使用。

## 社群提供的函式

社群提供的 UDF 可在`bigquery-public-data.persistent_udfs`公開資料集和開放原始碼 [`bigquery-utils` GitHub 存放區](https://github.com/GoogleCloudPlatform/bigquery-utils)中取得。如要查看所有[社群 UDF](https://github.com/GoogleCloudPlatform/bigquery-utils/tree/master/udfs/community)，請在 Google Cloud 控制台的「Explorer」窗格中[為](https://docs.cloud.google.com/bigquery/docs/quickstarts/query-public-dataset-console?hl=zh-tw#open_a_public_dataset) `bigquery-public-data` 專案加上星號，然後展開該專案中的巢狀 `persistent_udfs` 資料集。

### 允許在 VPC Service Controls 範圍內存取社群貢獻的函式

如果專案已啟用 VPC Service Controls，且 BigQuery 是受保護的服務，您必須為 `bigquery-public-data` 專案 (專案 ID：1057666841514) 定義輸出規則。

這項規則必須允許下列作業：

* `bigquery.routines.get` (用於使用日常安排)
* `bigquery.tables.getData` (用於查詢 BigQuery 資料表)

以下程式碼顯示 YAML 設定範例：

```
  - egressFrom:
      identityType: ANY_IDENTITY
    egressTo:
      operations:
      - serviceName: 'bigquery.googleapis.com'
        methodSelectors:
        - permission: 'bigquery.routines.get'
        - permission: 'bigquery.tables.getData'
      resources:
      - projects/1057666841514 # bigquery-public-data
```

如要為這個存放區的 UDF 貢獻心力，請參閱「[貢獻 UDF](https://github.com/GoogleCloudPlatform/bigquery-utils/blob/master/udfs/CONTRIBUTING.md)」一文的操作說明。

## 在多個區域統一存取日常安排

如要在多個區域的查詢中使用 UDF，含有 UDF 的查詢必須在每個區域中執行。因此，您應在可能使用 UDF 查詢的任何區域中，建立及維護 UDF。即使資料表相同，您也必須維護兩個版本的函式。舉例來說，如果您將銷售資料儲存在 `EU` 和 `US` 多區域，則應在每個區域維護函式版本。例如：

`EU` 多區域的查詢：

```
  SELECT
    id,
    europe_dataset.my_function(value)
  FROM
    sales;
```

`US` 多區域的查詢：

```
  SELECT
    id,
    us_dataset.my_function(value)
  FROM
    sales;
```

此外，如果函式定義有所變更，您必須在所有區域更新函式。

如要讓 UDF 不受地區限制，可以使用[跨地區資料集複製](https://docs.cloud.google.com/bigquery/docs/data-replication?hl=zh-tw)：

1. [建立新的專屬資料集](https://docs.cloud.google.com/bigquery/docs/datasets?hl=zh-tw) (例如 `my_utils`)，儲存所有必要的 UDF。請注意，新增至這個資料集的任何資料表都會遭到複製，這會增加費用。不過，複製 UDF 和程序不會產生額外費用。
2. 將所有 UDF 新增至新資料集。這也包括社群 UDF，例如從 [GitHub](https://github.com/GoogleCloudPlatform/bigquery-utils/tree/master/udfs) 複製的 `bqutil`。
3. [啟用資料集複製功能](https://docs.cloud.google.com/bigquery/docs/data-replication?hl=zh-tw#replicate_a_dataset)。將這個資料集設定為複製到所有需要執行查詢的區域，這些查詢會呼叫這些 UDF。這會將函式複製到這些區域，並保持同步。

執行查詢時，BigQuery 會自動使用本機資料集副本中的 UDF 本機版本，不必指定函式定義所在的區域，讓查詢可在不同位置之間移植。例如：

```
  SELECT
    id,
    my_utils.my_function(value)
  FROM
    sales;
```

## 限制

以下限制適用於暫時性和永久性的使用者定義函式：

* 系統不支援 `Window`、`Document` 和 `Node` 等 DOM 物件，以及需要使用這些物件的函式。
* JavaScript 函式會在沙箱環境中運作，如果函式依附於基礎系統程式碼，可能會因系統呼叫受限而失敗。
* JavaScript UDF 可能會逾時，造成查詢無法完成。逾時可能只有短短 5 分鐘，但可能因多種因素而異，包括您的函式占用多少使用者 CPU 作業時間，以及對於 JavaScript 函式的輸入和輸出有多大。
* JavaScript 中的位元作業僅處理最重要的 32 位元。
* UDF 須遵守特定頻率限制和配額限制。詳情請參閱「[UDF 限制](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#udf_limits)」。

以下限制適用於永久性使用者定義函式：

* 每個資料集只能含有一個使用相同名稱的 persistent UDF。不過，您可以在同一資料集中建立與資料表同名的 UDF。
* 從其他永久 UDF 或邏輯檢視表參照永久 UDF 時，您必須使用資料集來限定名稱。例如：  
  `CREATE FUNCTION mydataset.referringFunction()
  AS (mydataset.referencedFunction());`

以下限制適用於暫時性使用者定義函式。

* 建立 temporary UDF 時，`function_name` 不得包含句號。
* 檢視區塊和永久性 UDF 不得參照暫時性 UDF。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-14 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-14 (世界標準時間)。"],[],[]]