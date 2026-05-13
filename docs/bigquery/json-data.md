Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 在 GoogleSQL 中使用 JSON 資料

本文說明如何建立含有 `JSON` 欄的資料表、將 JSON 資料插入 BigQuery 資料表，以及查詢 JSON 資料。

BigQuery 原生支援使用 [`JSON`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#json_type) 資料類型的 JSON 資料。

JSON 是一種廣為使用的格式，可處理半結構化資料，因為不需要結構定義。應用程式可使用「讀取時結構定義」方法，也就是應用程式會擷取資料，然後根據對該資料結構定義的假設進行查詢。這與 BigQuery 中的 `STRUCT` 類型不同，後者需要固定結構定義，且會對儲存在 `STRUCT` 類型資料欄中的所有值強制執行。

使用 `JSON` 資料類型，您就能將半結構化 JSON 載入 BigQuery，不必預先提供 JSON 資料的結構定義。您可以儲存及查詢不一定符合固定結構定義和資料類型的資料。將 JSON 資料擷取為 `JSON` 資料類型後，BigQuery 就能個別編碼及處理每個 JSON 欄位。然後，您可以使用欄位存取運算子，查詢 JSON 資料中的欄位值和陣列元素，讓 JSON 查詢直覺易懂且經濟實惠。

## 限制

* 如果您使用[批次載入作業](https://docs.cloud.google.com/bigquery/docs/batch-loading-data?hl=zh-tw)將 JSON 資料擷取至資料表，來源資料必須是 CSV、Avro 或 JSON 格式。系統不支援其他批次載入格式。
* `JSON` 資料類型的巢狀結構限制為 500。
* 您無法使用[舊版 SQL](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/migrating-from-legacy-sql?hl=zh-tw) 查詢含有 `JSON` 型別的資料表。
* 資料列層級存取政策無法套用至 `JSON` 欄。

如要瞭解 `JSON` 資料類型的屬性，請參閱 [`JSON` 類型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#json_type)。

## 建立含有 `JSON` 資料欄的資料表

您可以使用 SQL 或 bq 指令列工具，建立含有 `JSON` 資料欄的空白資料表。

### SQL

使用 [`CREATE TABLE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#create_table_statement) 陳述式，並宣告 `JSON` 型別的資料欄。

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列陳述式：

   ```
   CREATE TABLE mydataset.table1(
     id INT64,
     cart JSON
   );
   ```
3. 按一下「執行」play\_circle。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

### bq

使用 [`bq mk`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#mk-table) 指令，並提供具有 `JSON` 資料類型的資料表結構。

```
bq mk --table mydataset.table1 id:INT64,cart:JSON
```

您無法根據 `JSON` 資料欄對資料表分區或叢集，因為等號和比較運算子未在 `JSON` 型別中定義。

## 建立 `JSON` 值

您可以透過下列方式建立 `JSON` 值：

* 使用 SQL 建立 [`JSON` 常值](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/lexical?hl=zh-tw#json_literals)。
* 使用 [`PARSE_JSON`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/json_functions?hl=zh-tw#parse_json) 函式將 `STRING` 值轉換為 [`JSON` 值](https://www.json.org/json-en.html)。
* 使用 [`TO_JSON`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/json_functions?hl=zh-tw#to_json) 函式將 SQL 值轉換為 [`JSON` 值](https://www.json.org/json-en.html)。
* 使用 [`JSON_ARRAY`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/json_functions?hl=zh-tw#json_array) 函式從 SQL 值建立 JSON 陣列。
* 使用 [`JSON_OBJECT`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/json_functions?hl=zh-tw#json_object) 函式，從鍵/值組合建立 JSON 物件。

### 建立`JSON`值

以下範例會將 `JSON` 值插入資料表：

```
INSERT INTO mydataset.table1 VALUES
(1, JSON '{"name": "Alice", "age": 30}'),
(2, JSON_ARRAY(10, ['foo', 'bar'], [20, 30])),
(3, JSON_OBJECT('foo', 10, 'bar', ['a', 'b']));
```

### 將 `STRING` 型別轉換為 `JSON` 型別

下列範例使用 [`PARSE_JSON`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/json_functions?hl=zh-tw#parse_json) 函式，轉換 JSON 格式的 `STRING` 值。這個範例會將現有資料表的資料欄轉換為 `JSON` 型別，並將結果儲存到新資料表。

```
CREATE OR REPLACE TABLE mydataset.table_new
AS (
  SELECT
    id, SAFE.PARSE_JSON(cart) AS cart_json
  FROM
    mydataset.old_table
);
```

本例中使用的 [`SAFE` 前置字元](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/functions-reference?hl=zh-tw#safe_prefix)可確保所有轉換錯誤都會以 `NULL` 值傳回。

### 將結構定義資料轉換為 JSON

以下範例使用 [`JSON_OBJECT`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/json_functions?hl=zh-tw#json_object) 函式，將鍵/值組合轉換為 JSON。

```
WITH Fruits AS (
SELECT 0 AS id, 'color' AS k, 'Red' AS v UNION ALL
SELECT 0, 'fruit', 'apple' UNION ALL
SELECT 1, 'fruit','banana' UNION ALL
SELECT 1, 'ripe', 'true'
)

SELECT JSON_OBJECT(ARRAY_AGG(k), ARRAY_AGG(v)) AS json_data
FROM Fruits
GROUP BY id
```

結果如下：

```
+----------------------------------+
| json_data                        |
+----------------------------------+
| {"color":"Red","fruit":"apple"}  |
| {"fruit":"banana","ripe":"true"} |
+----------------------------------+
```

### 將 SQL 型別轉換為 `JSON` 型別

以下範例使用 [`TO_JSON`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/json_functions?hl=zh-tw#to_json) 函式，將 SQL `STRUCT` 值轉換為 `JSON` 值：

```
SELECT TO_JSON(STRUCT(1 AS id, [10,20] AS coordinates)) AS pt;
```

結果如下：

```
+--------------------------------+
| pt                             |
+--------------------------------+
| {"coordinates":[10,20],"id":1} |
+--------------------------------+
```

## 擷取 JSON 資料

您可以透過下列方式將 JSON 資料擷取至 BigQuery 資料表：

* 使用批次載入工作，從下列格式載入 `JSON` 欄。
  + [CSV](https://docs.cloud.google.com/bigquery/docs/loading-data-cloud-storage-csv?hl=zh-tw)
  + [Avro](https://docs.cloud.google.com/bigquery/docs/loading-data-cloud-storage-avro?hl=zh-tw#extract_json_data_from_avro_data)
  + [JSON](https://docs.cloud.google.com/bigquery/docs/loading-data-cloud-storage-json?hl=zh-tw#loading_semi-structured_json_data)
* 使用 [BigQuery Storage Write API](https://docs.cloud.google.com/bigquery/docs/write-api?hl=zh-tw)。
* 使用舊版
  [`tabledata.insertAll` 串流 API](https://docs.cloud.google.com/bigquery/docs/streaming-data-into-bigquery?hl=zh-tw)

### 從 CSV 檔案載入

以下範例假設您有名為 `file1.csv` 的 CSV 檔案，其中包含下列記錄：

```
1,20
2,"""This is a string"""
3,"{""id"": 10, ""name"": ""Alice""}"
```

請注意，第二欄包含以字串編碼的 JSON 資料。這包括正確逸出 CSV 格式的引號。在 CSV 格式中，引號會使用 `""` 雙字元序列逸出。

如要使用 bq 指令列工具載入這個檔案，請使用 [`bq load`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_load) 指令：

```
bq load --source_format=CSV mydataset.table1 file1.csv id:INTEGER,json_data:JSON

bq show mydataset.table1

Last modified          Schema         Total Rows   Total Bytes
----------------- -------------------- ------------ -------------
 22 Dec 22:10:32   |- id: integer       3            63
                   |- json_data: json
```

### 從以換行符號分隔的 JSON 檔案載入

以下範例假設您有名為 `file1.jsonl` 的檔案，其中包含下列記錄：

```
{"id": 1, "json_data": 20}
{"id": 2, "json_data": "This is a string"}
{"id": 3, "json_data": {"id": 10, "name": "Alice"}}
```

如要使用 bq 指令列工具載入這個檔案，請使用 [`bq load`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_load) 指令：

```
bq load --source_format=NEWLINE_DELIMITED_JSON mydataset.table1 file1.jsonl id:INTEGER,json_data:JSON

bq show mydataset.table1

Last modified          Schema         Total Rows   Total Bytes
----------------- -------------------- ------------ -------------
 22 Dec 22:10:32   |- id: integer       3            63
                   |- json_data: json
```

### 使用 Storage Write API

您可以使用 [Storage Write API](https://docs.cloud.google.com/bigquery/docs/write-api?hl=zh-tw) 擷取 JSON 資料。以下範例使用 Storage Write API [Python 用戶端](https://docs.cloud.google.com/bigquery/docs/write-api?hl=zh-tw#python_client)，將資料寫入含有 JSON 資料類型資料欄的資料表。

定義通訊協定緩衝區，用來保存序列化的串流資料。JSON 資料會編碼為字串。在下列範例中，`json_col` 欄位會保留 JSON 資料。

```
message SampleData {
  optional string string_col = 1;
  optional int64 int64_col = 2;
  optional string json_col = 3;
}
```

將每一列的 JSON 資料格式設為 `STRING` 值：

```
row.json_col = '{"a": 10, "b": "bar"}'
row.json_col = '"This is a string"' # The double-quoted string is the JSON value.
row.json_col = '10'
```

如[程式碼範例](https://docs.cloud.google.com/bigquery/docs/write-api-streaming?hl=zh-tw#at-least-once)所示，將資料列附加至寫入串流。
用戶端程式庫會處理序列化為通訊協定緩衝區格式的作業。

如果無法格式化傳入的 JSON 資料，您需要在程式碼中使用 `json.dumps()` 方法。範例如下：

```
import json

...

row.json_col = json.dumps({"a": 10, "b": "bar"})
row.json_col = json.dumps("This is a string") # The double-quoted string is the JSON value.
row.json_col = json.dumps(10)

...
```

### 使用舊版串流 API

以下範例會從本機檔案載入 JSON 資料，並使用[舊版串流 API](https://docs.cloud.google.com/bigquery/docs/streaming-data-into-bigquery?hl=zh-tw) 將資料串流至 BigQuery 資料表，該資料表含有名為 `json_data` 的 JSON 資料類型資料欄。

```
from google.cloud import bigquery
import json

# TODO(developer): Replace these variables before running the sample.
project_id = 'MY_PROJECT_ID'
table_id = 'MY_TABLE_ID'

client = bigquery.Client(project=project_id)
table_obj = client.get_table(table_id)

# The column json_data is represented as a JSON data-type column.
rows_to_insert = [
    {"id": 1, "json_data": 20},
    {"id": 2, "json_data": "This is a string"},
    {"id": 3, "json_data": {"id": 10, "name": "Alice"}}
]

# If the column json_data is represented as a String data type, modify the rows_to_insert values:
#rows_to_insert = [
#    {"id": 1, "json_data": json.dumps(20)},
#    {"id": 2, "json_data": json.dumps("This is a string")},
#    {"id": 3, "json_data": json.dumps({"id": 10, "name": "Alice"})}
#]

# Throw errors if encountered.
# https://cloud.google.com/python/docs/reference/bigquery/latest/google.cloud.bigquery.client.Client#google_cloud_bigquery_client_Client_insert_rows

errors = client.insert_rows(table=table_obj, rows=rows_to_insert)
if errors == []:
    print("New rows have been added.")
else:
    print("Encountered errors while inserting rows: {}".format(errors))
```

詳情請參閱[以串流方式將資料傳入 BigQuery](https://docs.cloud.google.com/bigquery/docs/streaming-data-into-bigquery?hl=zh-tw#streaminginsertexamples)。

## 查詢 JSON 資料

本節說明如何使用 GoogleSQL 從 JSON 擷取值。JSON 區分大小寫，且欄位和值都支援 UTF-8。

本節範例使用下表：

```
CREATE OR REPLACE TABLE mydataset.table1(id INT64, cart JSON);

INSERT INTO mydataset.table1 VALUES
(1, JSON """{
        "name": "Alice",
        "items": [
            {"product": "book", "price": 10},
            {"product": "food", "price": 5}
        ]
    }"""),
(2, JSON """{
        "name": "Bob",
        "items": [
            {"product": "pen", "price": 20}
        ]
    }""");
```

### 以 JSON 格式擷取值

在 BigQuery 中，如果類型為 `JSON`，您可以使用[欄位存取運算子](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/operators?hl=zh-tw#field_access_operator)，存取 JSON 運算式中的欄位。以下範例會傳回 `cart` 資料欄的 `name` 欄位。

```
SELECT cart.name
FROM mydataset.table1;
```

```
+---------+
|  name   |
+---------+
| "Alice" |
| "Bob"   |
+---------+
```

如要存取陣列元素，請使用 [JSON 下標運算子](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/operators?hl=zh-tw#json_subscript_operator)。以下範例會傳回 `items` 陣列的第一個元素：

```
SELECT
  cart.items[0] AS first_item
FROM mydataset.table1
```

```
+-------------------------------+
|          first_item           |
+-------------------------------+
| {"price":10,"product":"book"} |
| {"price":20,"product":"pen"}  |
+-------------------------------+
```

您也可以使用 JSON 下標運算子，依名稱參照 JSON 物件的成員：

```
SELECT cart['name']
FROM mydataset.table1;
```

```
+---------+
|  name   |
+---------+
| "Alice" |
| "Bob"   |
+---------+
```

如果是下標作業，方括號內的運算式可以是任意字串或整數運算式，包括非常數運算式：

```
DECLARE int_val INT64 DEFAULT 0;

SELECT
  cart[CONCAT('it','ems')][int_val + 1].product AS item
FROM mydataset.table1;
```

```
+--------+
|  item  |
+--------+
| "food" |
| NULL   |
+--------+
```

欄位存取和下標運算子都會傳回 `JSON` 型別，因此您可以串連使用這些運算子的運算式，或將結果傳遞至採用 `JSON` 型別的其他函式。

這些運算子可提升[`JSON_QUERY`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/json_functions?hl=zh-tw#json_query)函式基本功能的可讀性。舉例來說，運算式 `cart.name` 等同於 `JSON_QUERY(cart, "$.name")`。

如果在 JSON 物件中找不到具有指定名稱的成員，或 JSON 陣列沒有指定位置的元素，這些運算子就會傳回 SQL `NULL`。

```
SELECT
  cart.address AS address,
  cart.items[1].price AS item1_price
FROM
  mydataset.table1;
```

```
+---------+-------------+
| address | item1_price |
+---------+-------------+
| NULL    | NULL        |
| NULL    | 5           |
+---------+-------------+
```

等號和比較運算子未在 `JSON` 資料類型中定義。
因此，您無法直接在 `GROUP BY` 或 `ORDER BY` 等子句中使用 `JSON` 值。請改用 `JSON_VALUE` 函式，以 SQL 字串形式擷取欄位值，如下一節所述。

### 以字串形式擷取值

[`JSON_VALUE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/json_functions?hl=zh-tw#json_value) 函式會擷取純量值，並以 SQL 字串形式傳回。如果 `cart.name` 未指向 JSON 中的純量值，則會傳回 SQL `NULL`。

```
SELECT JSON_VALUE(cart.name) AS name
FROM mydataset.table1;
```

```
+-------+
| name  |
+-------+
| Alice |
+-------+
```

您可以在需要相等或比較的環境中使用 `JSON_VALUE` 函式，例如 `WHERE` 子句和 `GROUP BY` 子句。以下範例顯示根據 `JSON` 值篩選的 `WHERE` 子句：

```
SELECT
  cart.items[0] AS first_item
FROM
  mydataset.table1
WHERE
  JSON_VALUE(cart.name) = 'Alice';
```

```
+-------------------------------+
| first_item                    |
+-------------------------------+
| {"price":10,"product":"book"} |
+-------------------------------+
```

或者，您也可以使用 [`STRING`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/json_functions?hl=zh-tw#string_for_json) 函式擷取 JSON 字串，然後以 SQL `STRING` 形式傳回該值。例如：

```
SELECT STRING(JSON '"purple"') AS color;
```

```
+--------+
| color  |
+--------+
| purple |
+--------+
```

除了 [`STRING`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/json_functions?hl=zh-tw#string_for_json)，您可能還需要擷取 `JSON` 值，並以其他 SQL 資料類型傳回。以下是可用的值擷取函式：

* [`STRING`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/json_functions?hl=zh-tw#string_for_json)
* [`BOOL`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/json_functions?hl=zh-tw#bool_for_json)
* [`INT64`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/json_functions?hl=zh-tw#int64_for_json)
* [`FLOAT64`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/json_functions?hl=zh-tw#double_for_json)

如要取得 `JSON` 值的型別，可以使用 [`JSON_TYPE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/json_functions?hl=zh-tw#json_type) 函式。

### 彈性轉換 JSON

您可以使用 [`LAX conversion`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/json_functions?hl=zh-tw#lax_converters) 函式，彈性地將 `JSON` 值轉換為純量 SQL 值。

以下範例使用 [`LAX_INT64` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/json_functions?hl=zh-tw#lax_int64)，從 `JSON` 值擷取 `INT64` 值。

```
SELECT LAX_INT64(JSON '"10"') AS id;
```

```
+----+
| id |
+----+
| 10 |
+----+
```

除了 [`LAX_INT64`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/json_functions?hl=zh-tw#lax_int64)，您也可以使用下列函式，彈性地將其他 SQL 型別轉換為 JSON：

* [`LAX_STRING`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/json_functions?hl=zh-tw#lax_string)
* [`LAX_BOOL`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/json_functions?hl=zh-tw#lax_bool)
* [`LAX_INT64`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/json_functions?hl=zh-tw#lax_int64)
* [`LAX_FLOAT64`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/json_functions?hl=zh-tw#lax_double)

### 從 JSON 擷取陣列

JSON 可以包含 JSON 陣列，但這類陣列與 BigQuery 中的 `ARRAY<JSON>` 型別並不完全相同。您可以使用下列函式，從 JSON 擷取 BigQuery `ARRAY`：

* [`JSON_QUERY_ARRAY`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/json_functions?hl=zh-tw#json_query_array)：
  擷取陣列並以 JSON 形式的 `ARRAY<JSON>` 傳回。
* [`JSON_VALUE_ARRAY`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/json_functions?hl=zh-tw#json_value_array)：
  擷取純量值陣列，並以純量值 `ARRAY<STRING>` 形式傳回。

下列範例使用 `JSON_QUERY_ARRAY` 擷取 JSON 陣列：

```
SELECT JSON_QUERY_ARRAY(cart.items) AS items
FROM mydataset.table1;
```

```
+----------------------------------------------------------------+
| items                                                          |
+----------------------------------------------------------------+
| [{"price":10,"product":"book"}","{"price":5,"product":"food"}] |
| [{"price":20,"product":"pen"}]                                 |
+----------------------------------------------------------------+
```

如要將陣列分割為個別元素，請使用 [`UNNEST`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw#unnest_operator) 運算子，這個運算子會傳回一個資料表，當中陣列的每項元素都會顯示為一個資料列。下列範例會從 `items` 陣列的每個成員選取 `product` 成員：

```
SELECT
  id,
  JSON_VALUE(item.product) AS product
FROM
  mydataset.table1, UNNEST(JSON_QUERY_ARRAY(cart.items)) AS item
ORDER BY id;
```

```
+----+---------+
| id | product |
+----+---------+
|  1 | book    |
|  1 | food    |
|  2 | pen     |
+----+---------+
```

下一個範例與上述範例類似，但使用 [`ARRAY_AGG`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/aggregate_functions?hl=zh-tw#array_agg) 函式將值匯總回 SQL 陣列。

```
SELECT
  id,
  ARRAY_AGG(JSON_VALUE(item.product)) AS products
FROM
  mydataset.table1, UNNEST(JSON_QUERY_ARRAY(cart.items)) AS item
GROUP BY id
ORDER BY id;
```

```
+----+-----------------+
| id | products        |
+----+-----------------+
|  1 | ["book","food"] |
|  2 | ["pen"]         |
+----+-----------------+
```

如要進一步瞭解陣列，請參閱「[在 GoogleSQL 中使用陣列](https://docs.cloud.google.com/bigquery/docs/arrays?hl=zh-tw)」。

## JSON 空值

`JSON` 型別具有與 SQL `NULL` 不同的特殊 `null` 值。JSON `null` 不會視為 SQL `NULL` 值，如下列範例所示。

```
SELECT JSON 'null' IS NULL;
```

```
+-------+
| f0_   |
+-------+
| false |
+-------+
```

使用 `null` 值擷取 JSON 欄位時，行為會因函式而異：

* `JSON_QUERY` 函式會傳回 JSON `null`，因為這是有效的 `JSON` 值。
* `JSON_VALUE` 函式會傳回 SQL `NULL`，因為 JSON `null` 不是純量值。

以下範例顯示不同的行為：

```
SELECT
  json.a AS json_query, -- Equivalent to JSON_QUERY(json, '$.a')
  JSON_VALUE(json, '$.a') AS json_value
FROM (SELECT JSON '{"a": null}' AS json);
```

```
+------------+------------+
| json_query | json_value |
+------------+------------+
| null       | NULL       |
+------------+------------+
```

**注意：** 這項行為不適用於儲存在 `STRING` 類型中的 JSON 值。
如果傳遞 `STRING` 值，`JSON_QUERY` 函式會傳回 SQL `NULL` 值，取代 JSON `null` 值。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-12 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-12 (世界標準時間)。"],[],[]]