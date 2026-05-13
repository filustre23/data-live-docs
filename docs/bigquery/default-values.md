Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 指定預設資料欄值

本頁說明如何為 BigQuery 資料表中的資料欄設定預設值。如果將資料列新增至不含預設值資料欄資料的表格，系統會改為將預設值寫入該資料欄。

## 預設值運算式

資料欄的預設值運算式必須是[常值](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/lexical?hl=zh-tw#literals)，或是下列其中一個函式：

* [`CURRENT_DATE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/date_functions?hl=zh-tw#current_date)
* [`CURRENT_DATETIME`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/datetime_functions?hl=zh-tw#current_datetime)
* [`CURRENT_TIME`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/time_functions?hl=zh-tw#current_time)
* [`CURRENT_TIMESTAMP`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/timestamp_functions?hl=zh-tw#current_timestamp)
* [`GENERATE_UUID`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/utility-functions?hl=zh-tw#generate_uuid)
* [`RAND`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/mathematical_functions?hl=zh-tw#rand)
* [`SESSION_USER`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/security_functions?hl=zh-tw#session_user)
* [`ST_GEOGPOINT`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/geography_functions?hl=zh-tw#st_geogpoint)

您可以使用這些函式撰寫 STRUCT 或 ARRAY 預設值，例如 `[CURRENT_DATE(), DATE '2020-01-01']`。

在作業處理期間，系統會在資料寫入資料表之前評估函式。預設值的類型必須與所套用資料欄的類型相符或[強制轉型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/conversion_rules?hl=zh-tw#comparison_chart)為該類型。如未設定預設值，預設值為 `NULL`。

## 設定預設值

建立新資料表時，您可以設定資料欄的預設值。您可以使用 [`CREATE TABLE` DDL 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#create_table_statement)，在資料欄名稱和類型後方新增 `DEFAULT` 關鍵字和預設值運算式。下列範例會建立名為 `simple_table` 的資料表，其中包含兩個 `STRING` 資料欄：`a` 和 `b`。資料欄 `b` 的預設值為 `'hello'`。

```
CREATE TABLE mydataset.simple_table (
  a STRING,
  b STRING DEFAULT 'hello');
```

將資料插入 `simple_table` 時，如果省略資料欄 `b`，系統會改用預設值 `'hello'`，例如：

```
INSERT mydataset.simple_table (a) VALUES ('val1'), ('val2');
```

資料表 `simple_table` 包含下列值：

```
+------+-------+
| a    | b     |
+------+-------+
| val1 | hello |
| val2 | hello |
+------+-------+
```

如果資料欄的類型為 `STRUCT`，則必須為整個 `STRUCT` 欄位設定預設值。您無法為部分欄位設定預設值。陣列的預設值不得為 `NULL` 或包含任何 `NULL` 元素。以下範例會建立名為 `complex_table` 的資料表，並為包含巢狀欄位的 `struct_col` 資料欄設定預設值，包括 `ARRAY` 型別：

```
CREATE TABLE mydataset.complex_table (
  struct_col STRUCT<x STRUCT<x1 TIMESTAMP, x2 NUMERIC>, y ARRAY<DATE>>
    DEFAULT ((CURRENT_TIMESTAMP(), NULL),
             [DATE '2022-01-01', CURRENT_DATE()])
);
```

您無法設定違反資料欄限制的預設值，例如不符合[參數化型別](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#parameterized_data_types)的預設值，或是資料欄的[模式](https://docs.cloud.google.com/bigquery/docs/schemas?hl=zh-tw#modes)為 `REQUIRED` 時的 `NULL` 預設值。

## 變更預設值

如要變更資料欄的預設值，請選取下列其中一個選項：

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。

   如果沒有看到左側窗格，請按一下 last\_page「Expand left pane」(展開左側窗格)，開啟窗格。
3. 在「Explorer」窗格中展開專案，按一下「Datasets」，然後選取資料集。
4. 依序點選「總覽」**>「資料表」**，然後按一下資料表。
5. 按一下「結構定義」分頁標籤。
6. 點選「編輯結構定義」。你可能需要捲動頁面才能看到這個按鈕。
7. 在「目前的結構定義」頁面中，找出要變更的頂層欄位。
8. 輸入該欄位的預設值。
9. 按一下 [儲存]。

### SQL

使用 [`ALTER COLUMN SET DEFAULT`DDL 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#alter_column_set_default_statement)。

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列陳述式：

   ```
   ALTER TABLE mydataset.mytable
   ALTER COLUMN column_name SET DEFAULT default_expression;
   ```
3. 按一下「執行」play\_circle。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

設定資料欄的預設值只會影響日後插入資料表的值。
不會變更任何現有表格資料。以下範例會將資料欄 `a` 的預設值設為 `SESSION_USER()`；

```
ALTER TABLE mydataset.simple_table ALTER COLUMN a SET DEFAULT SESSION_USER();
```

如果您在 `simple_table` 中插入省略 `a` 欄的資料列，系統會改用目前的工作階段使用者。

```
INSERT mydataset.simple_table (b) VALUES ('goodbye');
```

資料表 `simple_table` 包含下列值：

```
+------------------+---------+
| a                | b       |
+------------------+---------+
| val1             | hello   |
| val2             | hello   |
| user@example.com | goodbye |
+------------------+---------+
```

## 移除預設值

如要移除資料欄的預設值，請選取下列其中一個選項：

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。

   如果沒有看到左側窗格，請按一下 last\_page「Expand left pane」(展開左側窗格)，開啟窗格。
3. 在「Explorer」窗格中展開專案，按一下「Datasets」(資料集)，然後選取資料集。
4. 依序點選「總覽」**>「表格」**，然後選取所需表格。
5. 在詳細資料窗格中，按一下「結構定義」分頁標籤。
6. 點選「編輯結構定義」。你可能需要捲動頁面才能看到這個按鈕。
7. 在「目前的結構定義」頁面中，找出要變更的頂層欄位。
8. 輸入 `NULL` 做為預設值。
9. 按一下 [儲存]。

### SQL

使用 [`ALTER COLUMN DROP DEFAULT`DDL 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#alter_column_drop_default_statement)。

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列陳述式：

   ```
   ALTER TABLE mydataset.mytable ALTER COLUMN column_name DROP DEFAULT;
   ```

   您也可以使用 [`ALTER COLUMN SET DEFAULT` DDL 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#alter_column_set_default_statement)，將資料欄的值變更為 `NULL`，從資料欄中移除預設值。
3. 按一下「執行」play\_circle。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

## 使用含預設值的 DML 陳述式

您可以使用 [`INSERT` DML 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/dml-syntax?hl=zh-tw#insert_statement)，將含有預設值的資料列新增至資料表。如果未指定資料欄的值，或使用關鍵字 `DEFAULT` 取代值運算式，系統就會採用預設值。以下範例會建立資料表，並插入每個值都是預設值的資料列：

```
CREATE TABLE mydataset.mytable (
  x TIME DEFAULT CURRENT_TIME(),
  y INT64 DEFAULT 5,
  z BOOL);

INSERT mydataset.mytable (x, y, z) VALUES (DEFAULT, DEFAULT, DEFAULT);
```

資料表 `mytable` 如下所示：

```
+-----------------+---+------+
| x               | y | z    |
+-----------------+---+------+
| 22:13:24.799555 | 5 | null |
+-----------------+---+------+
```

欄 `z` 沒有預設值，因此系統會使用 `NULL` 做為預設值。如果預設值是函式 (例如 `CURRENT_TIME()`)，系統會在寫入值時評估該函式。再次使用資料欄 `x` 的預設值呼叫 `INSERT`，會導致 `TIME` 的值不同。在下列範例中，只有資料欄 `z` 設有明確值，省略的資料欄則使用預設值：

```
INSERT mydataset.mytable (z) VALUES (TRUE);
```

資料表 `mytable` 如下所示：

```
+-----------------+---+------+
| x               | y | z    |
+-----------------+---+------+
| 22:13:24.799555 | 5 | null |
| 22:18:29.890547 | 5 | true |
+-----------------+---+------+
```

您可以使用 [`MERGE` DML 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/dml-syntax?hl=zh-tw#merge_statement)，以預設值更新資料表。以下範例會建立兩個資料表，並使用 `MERGE` 陳述式更新其中一個資料表：

```
CREATE TABLE mydataset.target_table (
  a STRING,
  b STRING DEFAULT 'default_b',
  c STRING DEFAULT SESSION_USER())
AS (
  SELECT
    'val1' AS a, 'hi' AS b, '123@google.com' AS c
  UNION ALL
  SELECT
    'val2' AS a, 'goodbye' AS b, SESSION_USER() AS c
);

CREATE TABLE mydataset.source_table (
  a STRING DEFAULT 'default_val',
  b STRING DEFAULT 'Happy day!')
AS (
  SELECT
    'val1' AS a, 'Good evening！' AS b
  UNION ALL
  SELECT
    'val3' AS a, 'Good morning!' AS b
);

MERGE mydataset.target_table T
USING mydataset.source_table S
ON T.a = S.a
WHEN NOT MATCHED THEN
  INSERT(a, b) VALUES (a, DEFAULT);
```

結果如下：

```
+------+-----------+--------------------+
| a    | b         | c                  |
+------+-----------+--------------------+
| val1 | hi        | 123@google.com     |
| val2 | goodbye   | default@google.com |
| val3 | default_b | default@google.com |
+------+-----------+--------------------+
```

您可以使用 [`UPDATE` DML 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/dml-syntax?hl=zh-tw#update_statement)，以預設值更新資料表。以下範例會更新 `source_table` 資料表，使資料欄 `b` 的每個資料列都等於預設值：

```
UPDATE mydataset.source_table
SET b =  DEFAULT
WHERE TRUE;
```

結果如下：

```
+------+------------+
| a    | b          |
+------+------------+
| val1 | Happy day! |
| val3 | Happy day! |
+------+------------+
```

## 附加資料表

您可以搭配使用 `bq query` 指令和 `--append_table` 旗標，將查詢結果附加至具有預設值的目的地資料表。如果查詢省略了含有預設值的資料欄，系統會指派預設值。以下範例會附加資料，僅指定資料欄 `z` 的值：

```
bq query \
    --nouse_legacy_sql \
    --append_table \
    --destination_table=mydataset.mytable \
    'SELECT FALSE AS z UNION ALL SELECT FALSE AS Z'
```

資料表 `mytable` 會使用資料欄 `x` 和 `y` 的預設值：

```
+-----------------+---+-------+
|        x        | y |   z   |
+-----------------+---+-------+
| 22:13:24.799555 | 5 |  NULL |
| 22:18:29.890547 | 5 |  true |
| 23:05:18.841683 | 5 | false |
| 23:05:18.841683 | 5 | false |
+-----------------+---+-------+
```

## 載入資料

您可以使用 [`bq load` 指令](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_load)或 [`LOAD DATA` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/other-statements?hl=zh-tw#load_data_statement)，將資料[載入](https://docs.cloud.google.com/bigquery/docs/loading-data?hl=zh-tw)含有預設值的資料表。如果載入的資料欄數少於目的地資料表，系統會套用預設值。載入資料中的 `NULL` 值不會轉換為預設值。

二進位格式 (例如 AVRO、Parquet 或 ORC) 具有編碼的檔案結構定義。如果檔案結構定義省略部分資料欄，系統會套用預設值。

JSON 和 CSV 等文字格式沒有編碼的檔案結構定義。如要使用 bq 指令列工具指定結構定義，可以使用 `--autodetect` 旗標或提供 [JSON 結構定義](https://docs.cloud.google.com/bigquery/docs/schemas?hl=zh-tw#specifying_a_json_schema_file)。如要使用 `LOAD DATA` 陳述式指定結構定義，您必須提供資料欄清單。以下範例只會從 CSV 檔案載入 `a` 欄：

```
LOAD DATA INTO mydataset.insert_table (a)
FROM FILES(
  uris = ['gs://test-bucket/sample.csv'],
  format = 'CSV');
```

## Write API

只有在[寫入串流](https://docs.cloud.google.com/bigquery/docs/reference/storage/rpc/google.cloud.bigquery.storage.v1?hl=zh-tw#google.cloud.bigquery.storage.v1.WriteStream)結構定義缺少目的地資料表結構定義中的欄位時，Storage Write API 才會填入預設值。在這種情況下，系統會在每次寫入時，為欄位填入預設值。如果欄位存在於寫入串流結構定義中，但資料本身缺少該欄位，系統會以 `NULL` 填入缺少的欄位。舉例來說，假設您要將資料寫入具有下列結構定義的 BigQuery 資料表：

```
[
  {
    "name": "a",
    "mode": "NULLABLE",
    "type": "STRING",
  },
  {
    "name": "b",
    "mode": "NULLABLE",
    "type": "STRING",
    "defaultValueExpression": "'default_b'"
  },
  {
    "name": "c",
    "mode": "NULLABLE",
    "type": "STRING",
    "defaultValueExpression": "'default_c'"
  }
]
```

下列[寫入串流結構定義](https://docs.cloud.google.com/bigquery/docs/reference/storage/rpc/google.cloud.bigquery.storage.v1?hl=zh-tw#google.cloud.bigquery.storage.v1.TableSchema)缺少目的地資料表中的「`c`」欄位：

```
[
  {
    "name": "a",
    "type": "STRING",
  },
  {
    "name": "b",
    "type": "STRING",
  }
]
```

假設您將下列值串流至資料表：

```
{'a': 'val_a', 'b': 'val_b'}
{'a': 'val_a'}
```

結果如下：

```
+-------+-------+-----------+
| a     | b     | c         |
+-------+-------+-----------+
| val_a | val_b | default_c |
| val_a | NULL  | default_c |
+-------+-------+-----------+
```

寫入串流結構定義包含 `b` 欄位，因此即使未指定欄位值，系統也不會使用預設值 `default_b`。由於寫入串流結構定義不含 `c` 欄位，因此 `c` 欄中的每一列都會填入目的地資料表的預設值 `default_c`。

下列寫入串流結構定義與您要寫入的資料表結構定義相符：

```
[
  {
    "name": "a",
    "type": "STRING",
  },
  {
    "name": "b",
    "type": "STRING",
  }
  {
    "name": "c",
    "type": "STRING",
  }
]
```

假設您將下列值串流至資料表：

```
{'a': 'val_a', 'b': 'val_b'}
{'a': 'val_a'}
```

寫入串流結構定義不會遺漏目的地資料表中的任何欄位，因此無論串流資料中是否填入欄位，系統都不會套用任何資料欄的預設值：

```
+-------+-------+------+
| a     | b     | c    |
+-------+-------+------+
| val_a | val_b | NULL |
| val_a | NULL  | NULL |
+-------+-------+------+
```

您可以在 [`AppendRowsRequest` 訊息](https://docs.cloud.google.com/bigquery/docs/reference/storage/rpc/google.cloud.bigquery.storage.v1?hl=zh-tw#google.cloud.bigquery.storage.v1.AppendRowsRequest)的 `default_missing_value_interpretation` 中指定連線層級的預設值設定。如果值設為 `DEFAULT_VALUE`，即使資料欄出現在使用者結構定義中，遺漏的值也會採用預設值。

您也可以在 [`AppendRowsRequest` 訊息](https://docs.cloud.google.com/bigquery/docs/reference/storage/rpc/google.cloud.bigquery.storage.v1?hl=zh-tw#google.cloud.bigquery.storage.v1.AppendRowsRequest)的 `missing_value_interpretations` 對應中指定要求層級的預設值。每個鍵都是資料欄的名稱，而其[值](https://docs.cloud.google.com/bigquery/docs/reference/storage/rpc/google.cloud.bigquery.storage.v1?hl=zh-tw#missingvalueinterpretation)則表示如何解讀遺漏值。

舉例來說，地圖 `{'col1': NULL_VALUE, 'col2': DEFAULT_VALUE}` 表示 `col1` 中的所有遺漏值都會解讀為 `NULL`，而 `col2` 中的所有遺漏值都會解讀為資料表結構定義中為 `col2` 設定的預設值。

如果欄位不在這個對應表中，且缺少值，系統會將缺少的值解讀為 `NULL`。

鍵只能是頂層資料欄名稱。索引鍵不得為結構體子欄位，例如 `col1.subfield1`。

## 使用 `insertAll` API 方法

當資料寫入資料表時，[`tabledata.insertAll` API 方法](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tabledata/insertAll?hl=zh-tw)會在資料列層級填入預設值。如果資料列缺少具有預設值的資料欄，系統會將預設值套用至這些資料欄。

舉例來說，假設您有下列資料表結構定義：

```
[
  {
    "name": "a",
    "mode": "NULLABLE",
    "type": "STRING",
  },
  {
    "name": "b",
    "mode": "NULLABLE",
    "type": "STRING",
    "defaultValueExpression": "'default_b'"
  },
  {
    "name": "c",
    "mode": "NULLABLE",
    "type": "STRING",
    "defaultValueExpression": "'default_c'"
  }
]
```

假設您將下列值串流至資料表：

```
{'a': 'val_a', 'b': 'val_b'}
{'a': 'val_a'}
{}
```

結果如下：

```
+-------+------------+-----------+
| a     | b          | c         |
+-------+------------+-----------+
| val_a | val_b      | default_c |
| val_a | default_b  | default_c |
| NULL  | default_b  | default_c |
+-------+------------+-----------+
```

插入的第一列不包含欄位 `c` 的值，因此系統會將預設值 `default_c` 寫入欄 `c`。第二個插入的資料列不含 `b` 或 `c` 欄位的值，因此系統會將預設值寫入 `b` 和 `c` 欄。插入的第三列不含任何值。由於未設定其他預設值，因此寫入「`a`」欄的值為「`NULL`」。預設值 `default_b` 和 `default_c` 會寫入 `b` 和 `c` 欄。

## 查看預設值

如要查看資料欄的預設值，請查詢 `INFORMATION_SCHEMA.COLUMNS` 檢視區塊。`column_default` 欄位包含資料欄的預設值。如未設定預設值，則為 `NULL`。以下範例顯示資料表 `mytable` 的資料欄名稱和預設值：

```
SELECT
  column_name,
  column_default
FROM
  mydataset.INFORMATION_SCHEMA.COLUMNS
WHERE
  table_name = 'mytable';
```

結果大致如下：

```
+-------------+----------------+
| column_name | column_default |
+-------------+----------------+
| x           | CURRENT_TIME() |
| y           | 5              |
| z           | NULL           |
+-------------+----------------+
```

## 限制

* 您可以使用舊版 SQL 讀取含有預設值的資料表，但無法使用舊版 SQL 寫入含有預設值的資料表。
* 您無法在現有資料表中新增含有預設值的新資料欄。
  不過，您可以新增沒有預設值的資料欄，然後使用 `ALTER COLUMN SET DEFAULT` DDL 陳述式變更預設值。
* 如果目的地資料表的資料欄比來源資料表多，且額外資料欄有預設值，您就無法複製來源資料表並附加至目的地資料表。您可以改為執行 `INSERT destination_table SELECT * FROM source_table` 來複製資料。

## 後續步驟

* 如要進一步瞭解如何將資料載入 BigQuery，請參閱「[載入資料簡介](https://docs.cloud.google.com/bigquery/docs/loading-data?hl=zh-tw)」。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-12 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-12 (世界標準時間)。"],[],[]]