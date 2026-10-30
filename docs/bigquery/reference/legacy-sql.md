Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [參考資料](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 舊版 SQL 語法、函式和運算子

本文詳細說明舊版 SQL 查詢語法、函式和運算子。BigQuery 偏好的查詢語法是 [GoogleSQL 語法](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw)。詳情請參閱「[舊版 SQL 功能可用性](https://docs.cloud.google.com/bigquery/docs/legacy-sql-feature-availability?hl=zh-tw)」。

## 查詢語法

**注意：**關鍵字*不*區分大小寫。在本文件中，`SELECT` 等關鍵字會以大寫表示，僅供說明之用。

### SELECT 子句

`SELECT` 子句會指定要計算的運算式清單。`SELECT` 子句中的運算式可包含欄位名稱、常值和[函式呼叫](#functions) (包括[匯總函式](#aggfunctions)和[視窗函式](#windowfunctions))，以及這三者的組合。運算式清單以半形逗號分隔。

如要為運算式指定別名，請在運算式後方加上空格和 ID。您也可選擇在運算式和別名之間加上 `AS` 關鍵字來提升可讀性。在 `SELECT` 子句中定義的別名，可以在查詢的 `GROUP BY`、`HAVING` 和 `ORDER BY` 子句中參照，但不能由 `FROM`、`WHERE` 或 `OMIT RECORD IF` 子句參照，也不能由相同 `SELECT` 子句中的其他運算式參照。

**注意：**

* 如果您在 `SELECT` 子句中使用[匯總函式](#aggfunctions)，則必須在所有運算式中使用匯總函式，或者查詢必須包含 `GROUP BY` 子句，其中包含 `SELECT` 子句中所有非匯總欄位做為分組索引鍵。例如：

  ```
  #legacySQL
  SELECT
    word,
    corpus,
    COUNT(word)
  FROM
    [bigquery-public-data:samples.shakespeare]
  WHERE
    word CONTAINS "th"
  GROUP BY
    word,
    corpus; /* Succeeds because all non-aggregated fields are group keys. */
  ```

  ```
  #legacySQL
  SELECT
    word,
    corpus,
    COUNT(word)
  FROM
    [bigquery-public-data:samples.shakespeare]
  WHERE
    word CONTAINS "th"
  GROUP BY
    word; /* Fails because corpus is not aggregated nor is it a group key. */
  ```
* 您可以使用方括號逸出[保留字詞](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/lexical?hl=zh-tw#reserved_keywords)，以便將其做為欄位名稱和別名。舉例來說，如果資料欄名稱為「partition」(BigQuery 語法中的保留字詞)，參照該欄位的查詢會失敗，並顯示模糊的錯誤訊息，除非您使用方括號逸出該欄位：

  ```
  SELECT [partition] FROM ...
  ```

##### 範例

這個範例在 `SELECT` 子句中定義別名，然後在 `ORDER BY` 子句中參照其中一個別名。請注意，`WHERE` 子句中的 *word\_alias* 無法參照 *word* 欄，必須依名稱參照。*len* 別名也不會顯示在 `WHERE` 子句中。`HAVING` 子句會顯示該變數。

```
#legacySQL
SELECT
  word AS word_alias,
  LENGTH(word) AS len
FROM
  [bigquery-public-data:samples.shakespeare]
WHERE
  word CONTAINS 'th'
ORDER BY
  len;
```

#### 匯總函式的 WITHIN 修飾符

```
aggregate_function WITHIN RECORD [ [ AS ] alias ]
```

`WITHIN` 關鍵字會使匯總函式匯總每筆記錄中的重複值。且只會為每項輸入記錄產生一個匯總結果。這類匯總稱為「範圍匯總」。由於範圍匯總會為每筆記錄產生輸出內容，因此您可以選取非匯總運算式和範圍匯總運算式，而不必使用 `GROUP BY` 子句。

使用限定範圍匯總時，最常使用 `RECORD` 範圍。如果您有非常複雜的巢狀重複結構定義，就可能需要在子記錄範圍中執行匯總作業，只要將上述語法中的 `RECORD` 關鍵字，替換成結構定義中要執行匯總的節點名稱，即可完成這項操作。如要進一步瞭解這項進階行為，請參閱「[處理資料](https://docs.cloud.google.com/bigquery/docs/data?hl=zh-tw#within)」。

##### 範例

這個範例會執行範圍 `COUNT` 匯總，然後依匯總值篩選及排序記錄。

```
#legacySQL
SELECT
  repository.url,
  COUNT(payload.pages.page_name) WITHIN RECORD AS page_count
FROM
  [bigquery-public-data:samples.github_nested]
HAVING
  page_count > 80
ORDER BY
  page_count DESC;
```

### FROM 子句

```
FROM
  [project_name:]datasetId.tableId [ [ AS ] alias ] |
  (subquery) [ [ AS ] alias ] |
  JOIN clause |
  FLATTEN clause |
  table wildcard function
```

`FROM` 子句會指定要查詢的來源資料。BigQuery 查詢可以直接對資料表、子查詢、彙整資料表，以及經由下述特殊用途運算子修改的資料表執行。您可以使用[逗號](#comma_as_union_all) (BigQuery 中的 `UNION ALL` 運算子) 查詢這些資料來源的組合。

#### 參照資料表

參照資料表時，必須同時指定 *datasetId* 和 *tableId*，*project\_name* 則可視需要使用。如未指定 *project\_name*，BigQuery 預設會使用目前的專案。如果專案名稱包含破折號，則必須以括號括住整個資料表參照。

##### 範例

```
[my-dashed-project:dataset1.tableName]
```

如要為資料表設定別名，請在資料表名稱後方依序加上空格和 ID。您可以在 *tableId* 和別名之間加入選用的 `AS` 關鍵字，提高可讀性。

參照資料表中的資料欄時，您可以使用簡單的資料欄名稱，也可以在資料欄名稱前面加上別名 (如有指定)，或加上 *datasetId* 和 *tableId* (只要未指定 *project\_name* 即可)。*project\_name* 不得包含在資料欄前置字元中，因為欄位名稱不得使用冒號字元。

##### 範例

這個範例參照的資料欄沒有資料表前置字元。

```
#legacySQL
SELECT
  word
FROM
  [bigquery-public-data:samples.shakespeare];
```

這個範例會在資料欄名稱前加上 *datasetId* 和 *tableId*。請注意，這個範例中不能包含 *project\_name*。只有在資料集位於目前的預設專案中時，這個方法才有效。

```
#legacySQL
SELECT
  samples.shakespeare.word
FROM
  samples.shakespeare;
```

這個範例會在資料欄名稱前加上資料表別名。

```
#legacySQL
SELECT
  t.word
FROM
  [bigquery-public-data:samples.shakespeare] AS t;
```

#### 整數範圍分區資料表

舊版 SQL 支援使用資料表修飾符，在整數範圍分區資料表中指定特定分區。範圍分區的定址鍵是範圍的起點。

以下範例查詢以 30 開頭的範圍分區：

```
#legacySQL
SELECT
  *
FROM
  dataset.table$30;
```

請注意，您無法使用舊版 SQL 查詢整個整數範圍分區資料表。而是傳回錯誤訊息，如下所示：

`Querying tables partitioned on a field is not supported in Legacy SQL`

#### 使用子查詢

「子查詢」是巢狀 `SELECT` 陳述式，以括號括住。在子查詢的 `SELECT` 子句中運算的運算式，可供外部查詢使用，就像[資料表](#from_tables)的資料欄一樣。

子查詢可用於計算匯總和其他運算式。且您可以在當中使用所有的 SQL 運算子。這表示子查詢本身可包含其他子查詢，且能夠執行聯結和分組匯總等作業。

#### 逗號為`UNION ALL`

與 GoogleSQL 不同，舊版 SQL 使用逗號做為 `UNION ALL` 運算子，而非 `CROSS JOIN` 運算子。這是舊版行為，因為 BigQuery 過去不支援 `CROSS JOIN`，而 BigQuery 使用者經常需要編寫 `UNION ALL` 查詢。在 GoogleSQL 中，執行聯集的查詢特別冗長。而使用逗號做為聯結運算子可讓使用者更有效率地撰寫這類查詢。舉例來說，這項查詢可用於對多天的記錄執行單一查詢。

```
#legacySQL
SELECT
  FORMAT_UTC_USEC(event.timestamp_in_usec) AS time,
  request_url
FROM
  [applogs.events_20120501],
  [applogs.events_20120502],
  [applogs.events_20120503]
WHERE
  event.username = 'root' AND
  NOT event.source_ip.is_internal;
```

一般來說，合併大量資料表的查詢，執行速度會比從單一資料表處理相同資料量的查詢慢。兩者的效能差異最高可達每個額外資料表 50 毫秒。單一查詢最多可聯集 1,000 個資料表。

#### 表格萬用字元函式

「表格萬用字元函式」一詞是指 BigQuery 獨有的一種特殊函式。這些函式用於 `FROM` 子句，可使用多種類型的篩選器之一，比對一組資料表名稱。例如，`TABLE_DATE_RANGE` 函式可用於僅查詢一組特定的每日資料表。如要進一步瞭解這些函式，請參閱「[表格萬用字元函式](#tablewildcardfunctions)」。

#### FLATTEN 運算子

```
(FLATTEN([project_name:]datasetId.tableId, field_to_be_flattened))
(FLATTEN((subquery), field_to_be_flattened))
```

與一般 SQL 處理系統不同，BigQuery 專為處理重複資料而設計。因此，BigQuery 使用者有時會需要撰寫操弄重複記錄結構的查詢，其中一個方法是使用 `FLATTEN` 運算子。

`FLATTEN` 會將結構定義中的一個節點從重複型式轉換成選用型式。如果記錄中有一或多個重複欄位值，`FLATTEN` 會建立多筆記錄，每筆記錄對應重複欄位中的一個值。系統會在每個新的輸出記錄中，複製記錄中所有其他已選取的欄位。`FLATTEN` 可重複套用，以移除多個重複層級。

如需更多資訊和範例，請參閱「[處理資料](https://docs.cloud.google.com/bigquery/docs/data?hl=zh-tw#flatten)」。

#### JOIN 運算子

BigQuery 支援在每個 `FROM` 子句中使用多個 `JOIN` 運算子。後續的 `JOIN` 作業會使用前一個 `JOIN` 作業的結果，做為左側 `JOIN` 輸入。任何前置 `JOIN` 輸入內容中的欄位，都可做為後續 `JOIN` 運算子 `ON` 子句中的索引鍵。

##### JOIN 類型

BigQuery 支援 `INNER`、`[FULL|RIGHT|LEFT] OUTER` 和 `CROSS JOIN` 作業。如未指定，預設值為 `INNER`。

`CROSS JOIN` 作業不允許 `ON` 子句。`CROSS JOIN` 可能會傳回大量資料，導致查詢速度緩慢、效率不彰，或超出每項查詢允許的資源上限。這類查詢會發生錯誤。建議盡可能使用不含 `CROSS JOIN` 的查詢。舉例來說，`CROSS JOIN` 通常用於[視窗函式](#windowfunctions)更有效率的地方。

##### EACH 修飾符

`EACH` 修飾符是提示，指示 BigQuery 使用多個分區執行 `JOIN`。如果您知道 `JOIN` 的兩側都很大，這項功能就特別實用。`EACH` 修飾符無法用於 `CROSS JOIN` 子句。

過去，我們會鼓勵使用者在許多情況下使用 `EACH`，如今則不建議這樣做。請盡可能使用不含 `EACH` 修飾符的 `JOIN`，以提升效能。如果查詢失敗，並顯示資源超出上限的錯誤訊息，請使用 `JOIN EACH`。

##### 半聯結和反聯結

除了在 `FROM` 子句中支援 `JOIN` 之外，BigQuery 也支援 `WHERE` 子句中的兩種 join 類型：半 join 和反半 join。半聯結是使用 `IN` 關鍵字和子查詢指定，反聯結則是使用 `NOT IN` 關鍵字。

###### 範例

下列查詢使用半聯結來尋找 ngram，其中 ngram 的第一個字詞也是另一個 ngram 的第二個字詞，而該 ngram 的第三個字詞為「AND」。

```
#legacySQL
SELECT
  ngram
FROM
  [bigquery-public-data:samples.trigrams]
WHERE
  first IN (SELECT
              second
            FROM
              [bigquery-public-data:samples.trigrams]
```