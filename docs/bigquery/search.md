Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 搜尋已建立索引的資料

在 BigQuery 中搜尋已建立索引的資料，可提升查詢效能，同時盡可能減少掃描的資料量。您可以對已建立索引的資料表使用 [`SEARCH` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/search_functions?hl=zh-tw#search)和[支援的運算子](#operator_and_function_optimization)，盡可能減少[處理的位元組](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#jobstatistics2)和[運算單元毫秒數](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#jobstatistics2)，尤其是在擷取總資料列的一小部分時。

## 建立搜尋索引

下表名為 `Logs`，用於顯示 `SEARCH` 函式的不同使用方式。這個範例資料表相當小，但在實際情況下，`SEARCH` 帶來的效能提升會隨著資料表的大小而增加。

```
CREATE TABLE my_dataset.Logs (Level STRING, Source STRING, Message STRING)
AS (
  SELECT 'INFO' as Level, '65.177.8.234' as Source, 'Entry Foo-Bar created' as Message
  UNION ALL
  SELECT 'WARNING', '132.249.240.10', 'Entry Foo-Bar already exists, created by 65.177.8.234'
  UNION ALL
  SELECT 'INFO', '94.60.64.181', 'Entry Foo-Bar deleted'
  UNION ALL
  SELECT 'SEVERE', '4.113.82.10', 'Entry Foo-Bar does not exist, deleted by 94.60.64.181'
  UNION ALL
  SELECT 'INFO', '181.94.60.64', 'Entry Foo-Baz created'
);
```

資料表如下所示：

```
+---------+----------------+-------------------------------------------------------+
| Level   | Source         | Message                                               |
+---------+----------------+-------------------------------------------------------+
| INFO    | 65.177.8.234   | Entry Foo-Bar created                                 |
| WARNING | 132.249.240.10 | Entry Foo-Bar already exists, created by 65.177.8.234 |
| INFO    | 94.60.64.181   | Entry Foo-Bar deleted                                 |
| SEVERE  | 4.113.82.10    | Entry Foo-Bar does not exist, deleted by 94.60.64.181 |
| INFO    | 181.94.60.64   | Entry Foo-Baz created                                 |
+---------+----------------+-------------------------------------------------------+
```

使用預設文字分析器，在 `Logs` 資料表建立搜尋索引：

```
CREATE SEARCH INDEX my_index ON my_dataset.Logs(ALL COLUMNS);
```

如要進一步瞭解搜尋索引，請參閱「[管理搜尋索引](https://docs.cloud.google.com/bigquery/docs/search-index?hl=zh-tw)」。

## 使用 `SEARCH` 函式

`SEARCH` 函式可對資料執行權杖化搜尋。`SEARCH` 應與[索引](https://docs.cloud.google.com/bigquery/docs/search-index?hl=zh-tw)搭配使用，以最佳化查詢。您可以使用 `SEARCH` 函式搜尋整個資料表，或將搜尋範圍限制在特定資料欄。

### 搜尋整個資料表

下列查詢會搜尋 `Logs` 資料表的所有資料欄，找出 `bar` 值，並傳回包含這個值的資料列，不論大小寫。由於搜尋索引使用預設文字分析器，因此您不需要在 `SEARCH` 函式中指定。

```
SELECT * FROM my_dataset.Logs WHERE SEARCH(Logs, 'bar');
```

```
+---------+----------------+-------------------------------------------------------+
| Level   | Source         | Message                                               |
+---------+----------------+-------------------------------------------------------+
| INFO    | 65.177.8.234   | Entry Foo-Bar created                                 |
| WARNING | 132.249.240.10 | Entry Foo-Bar already exists, created by 65.177.8.234 |
| INFO    | 94.60.64.181   | Entry Foo-Bar deleted                                 |
| SEVERE  | 4.113.82.10    | Entry Foo-Bar does not exist, deleted by 94.60.64.181 |
+---------+----------------+-------------------------------------------------------+
```

下列查詢會在 `Logs` 資料表的所有資料欄中搜尋 `` `94.60.64.181` `` 值，並傳回包含這個值的資料列。反引號可進行精確搜尋，因此 `Logs` 資料表中包含 `181.94.60.64` 的最後一列會遭到省略。

```
SELECT * FROM my_dataset.Logs WHERE SEARCH(Logs, '`94.60.64.181`');
```

```
+---------+----------------+-------------------------------------------------------+
| Level   | Source         | Message                                               |
+---------+----------------+-------------------------------------------------------+
| INFO    | 94.60.64.181   | Entry Foo-Bar deleted                                 |
| SEVERE  | 4.113.82.10    | Entry Foo-Bar does not exist, deleted by 94.60.64.181 |
+---------+----------------+-------------------------------------------------------+
```

### 搜尋部分資料欄

`SEARCH` 可讓您輕鬆指定要在哪些資料欄子集中搜尋資料。下列查詢會在 `Logs` 資料表的 `Message` 資料欄中搜尋 `94.60.64.181` 值，並傳回含有這個值的資料列。

```
SELECT * FROM my_dataset.Logs WHERE SEARCH(Message, '`94.60.64.181`');
```

```
+---------+----------------+-------------------------------------------------------+
| Level   | Source         | Message                                               |
+---------+----------------+-------------------------------------------------------+
| SEVERE  | 4.113.82.10    | Entry Foo-Bar does not exist, deleted by 94.60.64.181 |
+---------+----------------+-------------------------------------------------------+
```

下列查詢會同時搜尋 `Logs` 資料表的 `Source` 和 `Message` 欄。並傳回任一欄中包含 `94.60.64.181` 值的資料列。

```
SELECT * FROM my_dataset.Logs WHERE SEARCH((Source, Message), '`94.60.64.181`');
```

```
+---------+----------------+-------------------------------------------------------+
| Level   | Source         | Message                                               |
+---------+----------------+-------------------------------------------------------+
| INFO    | 94.60.64.181   | Entry Foo-Bar deleted                                 |
| SEVERE  | 4.113.82.10    | Entry Foo-Bar does not exist, deleted by 94.60.64.181 |
+---------+----------------+-------------------------------------------------------+
```

### 從搜尋中排除資料欄

如果資料表有多個資料欄，而您想搜尋其中大部分的資料欄，則可以只指定要從搜尋中排除的資料欄，這樣可能比較容易。下列查詢會搜尋 `Logs` 資料表的所有資料欄，但 `Message` 資料欄除外。並傳回 `Message` 以外任何資料欄中包含 `94.60.64.181` 值的資料列。

```
SELECT *
FROM my_dataset.Logs
WHERE SEARCH(
  (SELECT AS STRUCT Logs.* EXCEPT (Message)), '`94.60.64.181`');
```

```
+---------+----------------+---------------------------------------------------+
| Level   | Source         | Message                                           |
+---------+----------------+---------------------------------------------------+
| INFO    | 94.60.64.181   | Entry Foo-Bar deleted                             |
+---------+----------------+---------------------------------------------------+
```

### 使用其他文字分析器

下列範例會建立名為 `contact_info` 的資料表，並使用 `NO_OP_ANALYZER` [文字分析器](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/text-analysis?hl=zh-tw)建立索引：

```
CREATE TABLE my_dataset.contact_info (name STRING, email STRING)
AS (
  SELECT 'Kim Lee' AS name, 'kim.lee@example.com' AS email
  UNION ALL
  SELECT 'Kim' AS name, 'kim@example.com' AS email
  UNION ALL
  SELECT 'Sasha' AS name, 'sasha@example.com' AS email
);
CREATE SEARCH INDEX noop_index ON my_dataset.contact_info(ALL COLUMNS)
OPTIONS (analyzer = 'NO_OP_ANALYZER');
```

```
+---------+---------------------+
| name    | email               |
+---------+---------------------+
| Kim Lee | kim.lee@example.com |
| Kim     | kim@example.com     |
| Sasha   | sasha@example.com   |
+---------+---------------------+
```

下列查詢會在 `name` 欄中搜尋 `Kim`，並在 `email` 欄中搜尋 `kim`。由於搜尋索引不使用預設文字分析器，因此您必須將分析器的名稱傳遞至 `SEARCH` 函式。

```
SELECT
  name,
  SEARCH(name, 'Kim', analyzer=>'NO_OP_ANALYZER') AS name_Kim,
  email,
  SEARCH(email, 'kim', analyzer=>'NO_OP_ANALYZER') AS email_kim
FROM
  my_dataset.contact_info;
```

`NO_OP_ANALYZER` 不會修改文字，因此 `SEARCH` 函式只會針對完全比對的項目傳回 `TRUE`：

```
+---------+----------+---------------------+-----------+
| name    | name_Kim | email               | email_kim |
+---------+----------+---------------------+-----------+
| Kim Lee | FALSE    | kim.lee@example.com | FALSE     |
| Kim     | TRUE     | kim@example.com     | FALSE     |
| Sasha   | FALSE    | sasha@example.com   | FALSE     |
+---------+----------+---------------------+-----------+
```

### 設定文字分析器選項

如要自訂 `LOG_ANALYZER` 和 `PATTERN_ANALYZER` [文字分析器](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/text-analysis?hl=zh-tw)，請在設定選項中加入 JSON 格式的字串。您可以在 [`SEARCH` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/search_functions?hl=zh-tw)、[`CREATE
SEARCH INDEX` DDL 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#create_search_index_statement)和 [`TEXT_ANALYZE` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/text-analysis-functions?hl=zh-tw#text_analyze)中設定文字分析器。

以下範例會建立名為 `complex_table` 的資料表，並使用 `LOG_ANALYZER` 文字分析器建立索引。它會使用 JSON 格式的字串來設定分析器選項：

```
CREATE TABLE dataset.complex_table(
  a STRING,
  my_struct STRUCT<string_field STRING, int_field INT64>,
  b ARRAY<STRING>
);

CREATE SEARCH INDEX my_index
ON dataset.complex_table(a, my_struct, b)
OPTIONS (analyzer = 'LOG_ANALYZER', analyzer_options = '''{
  "token_filters": [
    {
      "normalizer": {"mode": "NONE"}
    }
  ]
}''');
```

下表列出使用不同文字分析器呼叫 `SEARCH` 函式的範例及其結果。第一個資料表使用預設文字分析器 `LOG_ANALYZER` 呼叫 `SEARCH` 函式：

| 函式呼叫 | 傳回 | 原因 |
| --- | --- | --- |
| SEARCH('foobarexample', NULL) | 錯誤 | search\_terms 為 `NULL`。 |
| SEARCH('foobarexample', '') | 錯誤 | search\_terms 不含任何權杖。 |
| SEARCH('foobar-example', 'foobar example') | TRUE | 「-」和「 」是分隔符號。 |
| SEARCH('foobar-example', 'foobarexample') | FALSE | search\_terms 未分割。 |
| SEARCH('foobar-example', 'foobar\\&example') | TRUE | 雙反斜線會逸出做為分隔符號的和號。 |
| SEARCH('foobar-example', R'foobar\&example') | TRUE | 單一反斜線會逸出原始字串中的和號。 |
| SEARCH('foobar-example', '`foobar&example`') | FALSE | 反引號需要與 foobar&example 完全比對。 |
| SEARCH('foobar&example', '`foobar&example`') | TRUE | 找到完全比對的項目。 |
| SEARCH('foobar-example', 'example foobar') | TRUE | 字詞的順序不會造成任何影響。 |
| SEARCH('foobar-example', 'foobar example') | TRUE | 權杖會轉換為小寫。 |
| SEARCH('foobar-example', '`foobar-example`') | TRUE | 找到完全比對的項目。 |
| SEARCH('foobar-example', '`foobar`') | FALSE | 反引號會保留大小寫。 |
| SEARCH('`foobar-example`', '`foobar-example`') | FALSE | 反引號對 data\_to\_search 和 |
| SEARCH('foobar@example.com', '`example.com`') | TRUE | 在 data\_to\_search 的分隔符號後方找到完全比對的項目。 |
| SEARCH('a foobar-example b', '`foobar-example`') | TRUE | 空格分隔符號之間有完全比對的項目。 |
| SEARCH(['foobar', 'example'], 'foobar example') | FALSE | 沒有任何陣列項目符合所有搜尋字詞。 |
| SEARCH('foobar=', '`foobar\\=`') | FALSE | search\_terms 相當於 foobar\=。 |
| SEARCH('foobar=', R'`foobar\=`') | FALSE | 這與前一個示例相同。 |
| SEARCH('foobar=', 'foobar\\=') | TRUE | 等號是資料和查詢中的分隔符號。 |
| SEARCH('foobar=', R'foobar\=') | TRUE | 這與前一個示例相同。 |
| SEARCH('foobar.example', '`foobar`') | TRUE | 找到完全比對的項目。 |
| SEARCH('foobar.example', '`foobar.`') | FALSE | `foobar.` 由於反引號而未分析； |
| SEARCH('foobar..example', '`foobar.`') | TRUE | `foobar.` 因反引號而未分析， |

下表列出使用 `NO_OP_ANALYZER` 文字分析器呼叫 `SEARCH` 函式的範例，以及各種傳回值的原因：

| 函式呼叫 | 退貨 | 原因 |
| --- | --- | --- |
| SEARCH('foobar', 'foobar', analyzer=>'NO\_OP\_ANALYZER') | TRUE | 找到完全比對的項目。 |
| SEARCH('foobar', '`foobar`', analyzer=>'NO\_OP\_ANALYZER') | FALSE | 反引號不是 NO\_OP\_ANALYZER 的特殊字元。 |
| SEARCH('Foobar', 'foobar', analyzer=>'NO\_OP\_ANALYZER') | FALSE | 大小寫不符。 |
| SEARCH('foobar example', 'foobar', analyzer=>'NO\_OP\_ANALYZER') | FALSE | NO\_OP\_ANALYZER 沒有分隔符。 |
| SEARCH('', '', analyzer=>'NO\_OP\_ANALYZER') | TRUE | NO\_OP\_ANALYZER 沒有分隔符。 |

## 其他運算子和函式

您可以使用多個運算子、函式和述詞，執行搜尋索引最佳化。

### 使用運算子和比較函式進行最佳化

BigQuery 可最佳化部分查詢，這些查詢使用[等號運算子](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/operators?hl=zh-tw#comparison_operators) (`=`)、[`IN` 運算子](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/operators?hl=zh-tw#in_operators)、[`LIKE` 運算子](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/operators?hl=zh-tw#like_operator)、[`STARTS_WITH` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/string_functions?hl=zh-tw#starts_with)或 [`ENDS_WITH` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/string_functions?hl=zh-tw#ends_with)，比較字串常值與索引資料。

### 使用字串述詞進行最佳化

下列述詞符合搜尋索引最佳化條件：

* `column_name = 'string_literal'`
* `'string_literal' = column_name`
* `struct_column.nested_field = 'string_literal'`
* `string_array_column[OFFSET(0)] = 'string_literal'`
* `string_array_column[ORDINAL(1)] = 'string_literal'`
* `column_name IN ('string_literal1', 'string_literal2', ...)`
* `column_name LIKE 'prefix%'`
* `STARTS_WITH(column_name, 'prefix')`
* `ENDS_WITH(column_name, 'some suffix')`

### 使用數值述詞進行最佳化

如果搜尋索引是以數值資料類型建立，BigQuery 可以最佳化部分查詢，這些查詢會使用等號運算子 (`=`) 或 `IN` 運算子搭配索引資料。下列述詞符合搜尋索引最佳化條件：

* `INT64(json_column.int64_field) = 1`
* `int64_column = 1`
* `int64_array_column[OFFSET(0)] = 1`
* `int64_column IN (1, 2)`
* `struct_column.nested_int64_field = 1`
* `struct_column.nested_timestamp_field = TIMESTAMP "2024-02-15 21:31:40"`
* `timestamp_column = "2024-02-15 21:31:40"`
* `timestamp_column IN ("2024-02-15 21:31:40", "2024-02-16 21:31:40")`

### 最佳化產生索引資料的函式

對已建立索引的資料套用特定函式時，BigQuery 支援搜尋索引最佳化。如果搜尋索引使用預設的 `LOG_ANALYZER` 文字分析器，則可將 [`UPPER`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/string_functions?hl=zh-tw#upper) 或 [`LOWER`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/string_functions?hl=zh-tw#lower) 函式套用至資料欄，例如 `UPPER(column_name) = 'STRING_LITERAL'`。

對於從索引 `JSON` 資料欄擷取的 `JSON` 純量字串資料，您可以套用 [`STRING`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/json_functions?hl=zh-tw#string_for_json) 函式或其安全版本 [`SAFE.STRING`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/functions-reference?hl=zh-tw#safe_prefix)。如果擷取的 `JSON` 值不是字串，`STRING` 函式會產生錯誤，`SAFE.STRING` 函式則會傳回 `NULL`。

對於已建立索引的 JSON 格式 `STRING` (而非 `JSON`) 資料，您可以套用下列函式：

* [`JSON_EXTRACT`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/json_functions?hl=zh-tw#json_extract)
* [`JSON_EXTRACT_SCALAR`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/json_functions?hl=zh-tw#json_extract_scalar)
* [`JSON_QUERY`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/json_functions?hl=zh-tw#json_query)
* [`JSON_VALUE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/json_functions?hl=zh-tw#json_value)

舉例來說，假設您有下列名為 `dataset.person_data` 的索引資料表，其中包含 `JSON` 和 `STRING` 資料欄：

```
+----------------------------------------------------------------+-----------------------------------------+
| json_column                                                    | string_column                           |
+----------------------------------------------------------------+-----------------------------------------+
| { "name" : "Ariel", "email" : "cloudysanfrancisco@gmail.com" } | { "name" : "Ariel", "job" : "doctor" }  |
+----------------------------------------------------------------+-----------------------------------------+
```

下列查詢符合最佳化條件：

```
SELECT * FROM dataset.person_data
WHERE SAFE.STRING(json_column.email) = 'cloudysanfrancisco@gmail.com';
```

```
SELECT * FROM dataset.person_data
WHERE JSON_VALUE(string_column, '$.job') IN ('doctor', 'lawyer', 'teacher');
```

這些函式的組合也經過最佳化，例如 `UPPER(JSON_VALUE(json_string_expression)) = 'FOO'`。

### 使用 JSON\_FLATTEN 進行最佳化

BigQuery 支援搜尋索引最佳化，適用於使用 [`JSON_FLATTEN` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/json_functions?hl=zh-tw#json_flatten)展開 JSON 陣列的查詢，通常與 `EXISTS` 和 `UNNEST` 搭配使用。

舉例來說，假設您有一個名為 `dataset.logs` 的資料表，其中包含 `JSON` 資料欄 `json_payload`。下列查詢符合最佳化資格：

```
SELECT json_payload
FROM dataset.logs
WHERE EXISTS(
  SELECT 1
  FROM UNNEST(JSON_FLATTEN(JSON_QUERY(json_payload, "lax recursive $.message"))) AS f
  WHERE SEARCH(f, "nullpointerexception")
);
```

## 搜尋索引使用情形

如要判斷查詢是否使用搜尋索引，您可以查看[工作詳細資料](#search_index_usage_job_details)，或查詢其中一個 [`INFORMATION_SCHEMA.JOBS*`](#search_index_usage_information_schema) 檢視表。

### 查看工作詳細資料

在「Query results」(查詢結果) 的「Job Information」(工作資訊) 中，[「Index Usage Mode」(索引使用模式)](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#indexusagemode) 和[「Index Unused Reasons」(未使用索引的原因)](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#indexunusedreason) 欄位會提供搜尋索引使用情形的詳細資訊。

您也可以透過 [Jobs.Get](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs/get?hl=zh-tw) API 方法中的 [`searchStatistics` 欄位](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#searchstatistics)，取得搜尋索引使用情形的相關資訊。`searchStatistics` 中的 `indexUsageMode` 欄位會指出是否使用了搜尋索引，並提供下列值：

* `UNUSED`：未使用搜尋索引。
* `PARTIALLY_USED`：部分查詢使用搜尋索引，部分則未使用。
* `FULLY_USED`：查詢中的每個 `SEARCH` 函式都使用了搜尋索引。

如果 `indexUsageMode` 為 `UNUSED` 或 `PARTIALLY_USED`，`indexUnusedReasons` 欄位會包含查詢未採用搜尋索引的原因。

如要查看查詢的 `searchStatistics`，請執行 `bq show` 指令。

```
bq show --format=prettyjson -j JOB_ID
```

#### 範例

假設您執行查詢，對資料表中的資料呼叫 `SEARCH` 函式。您可以查看查詢的[工作詳細資料](https://docs.cloud.google.com/bigquery/docs/managing-jobs?hl=zh-tw#view-job)，找出工作 ID，然後執行 `bq show` 指令，查看更多資訊：

```
bq show --format=prettyjson --j my_project:US.bquijob_123x456_789y123z456c
```

輸出內容包含許多欄位，其中 `searchStatistics` 欄位看起來會像下方這樣。在這個範例中，`indexUsageMode` 表示未使用索引。這是因為資料表沒有搜尋索引。如要解決這個問題，請在資料表上[建立搜尋索引](https://docs.cloud.google.com/bigquery/docs/search-index?hl=zh-tw)。如要查看查詢可能不使用搜尋索引的所有原因清單，請參閱 `indexUnusedReason` [`code` 欄位](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#Code_1)。

```
"searchStatistics": {
  "indexUnusedReasons": [
    {
      "baseTable": {
        "datasetId": "my_dataset",
        "projectId": "my_project",
        "tableId": "my_table"
      },
      "code": "INDEX_CONFIG_NOT_AVAILABLE",
      "message": "There is no search index configuration for the base table `my_project:my_dataset.my_table`."
    }
  ],
  "indexUsageMode": "UNUSED"
},
```

### 查詢 INFORMATION\_SCHEMA 檢視表

您也可以在下列檢視畫面中，查看某個區域內多項工作的搜尋索引使用情形：

* [`INFORMATION_SCHEMA.JOBS`](https://docs.cloud.google.com/bigquery/docs/information-schema-jobs?hl=zh-tw)
* [`INFORMATION_SCHEMA.JOBS_BY_USER`](https://docs.cloud.google.com/bigquery/docs/information-schema-jobs-by-user?hl=zh-tw)
* [`INFORMATION_SCHEMA.JOBS_BY_FOLDER`](https://docs.cloud.google.com/bigquery/docs/information-schema-jobs-by-folder?hl=zh-tw)
* [`INFORMATION_SCHEMA.JOBS_BY_ORGANIZATION`](https://docs.cloud.google.com/bigquery/docs/information-schema-jobs-by-organization?hl=zh-tw)

下列查詢會顯示過去 7 天內，所有可最佳化搜尋索引查詢的索引使用情形資訊：

```
SELECT
  job_id, search_statistics.index_usage_mode, index_unused_reason.code, index_unused_reason.base_table.table_id, index_unused_reason.index_name
FROM
  `region-REGION_NAME`.INFORMATION_SCHEMA.JOBS, UNNEST(search_statistics.index_unused_reasons) AS index_unused_reason
WHERE
  end_time BETWEEN TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 7 DAY) AND CURRENT_TIMESTAMP();
```

結果大致如下：

```
+-----------+----------------------------------------+-----------------------+
| job_id    | index_usage_mode | code                | table_id | index_name |
+-----------+------------------+---------------------+-----------------------+
| bquxjob_1 | UNUSED           | BASE_TABLE_TOO_SMALL| my_table | my_index   |
| bquxjob_2 | FULLY_USED       | NULL                | my_table | my_index   |
+-----------+----------------------------------------+-----------------------+
```

## 最佳做法

以下各節將說明搜尋的最佳做法。

### 選擇性搜尋

如果搜尋結果很少，搜尋功能的效果最好。盡可能具體說明搜尋內容。

### ORDER BY LIMIT 最佳化

在非常大的[分區](https://docs.cloud.google.com/bigquery/docs/partitioned-tables?hl=zh-tw)資料表上，使用 `SEARCH`、`=`、`IN`、`LIKE` 或 `STARTS_WITH` 的查詢，可透過在分區欄位上使用 `ORDER BY` 子句和 `LIMIT` 子句來最佳化。如果查詢不含 `SEARCH` 函式，您可以使用[其他運算子和函式](#operator_and_function_optimization)，充分運用最佳化功能。無論資料表是否已建立索引，系統都會套用最佳化。如果搜尋的是常見字詞，這個方法很實用。舉例來說，假設先前建立的 `Logs` 資料表，是依名為 `day` 的額外 `DATE` 已指定類型和格式的欄分區。以下查詢已最佳化：

```
SELECT
  Level, Source, Message
FROM
  my_dataset.Logs
WHERE
  SEARCH(Message, "foo")
ORDER BY
  day
LIMIT 10;
```

### 設定搜尋範圍

使用 `SEARCH` 函式時，請只搜尋預期含有搜尋字詞的資料表資料欄。這可提升效能，並減少需要掃描的位元組數。

### 使用反引號

搭配使用 `SEARCH` 函式和 `LOG_ANALYZER` 文字分析器時，如果用反引號括住搜尋查詢，系統會強制執行完全比對。如果搜尋內容區分大小寫，或包含不應解讀為分隔符號的字元，這項功能就非常實用。例如，如要搜尋 IP 位址 `192.0.2.1`，請使用 `` `192.0.2.1` ``。如果沒有反引號，搜尋會傳回包含個別符記 `192`、`0`、`2` 和 `1` 的任何資料列，順序不限。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-11-11 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-11-11 (世界標準時間)。"],[],[]]