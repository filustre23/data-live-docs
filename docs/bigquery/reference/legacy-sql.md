Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [參考資料](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 舊版 SQL 語法、函式和運算子

本文詳細說明舊版 SQL 查詢語法、函式和運算子。BigQuery 查詢的慣用語法是 [GoogleSQL 語法](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw)。詳情請參閱[舊版 SQL 功能的適用情形](https://docs.cloud.google.com/bigquery/docs/legacy-sql-feature-availability?hl=zh-tw)。

## 查詢語法

**注意：**關鍵字「不」區分大小寫。在本文中，`SELECT` 等關鍵字會以大寫標示，僅供說明用途。

### SELECT 子句

`SELECT` 子句會指定要計算的運算式清單。`SELECT` 子句中的運算式可包含欄位名稱、常值和[函式呼叫](#functions) (包括[匯總函式](#aggfunctions)和[窗型函式](#windowfunctions))，以及這三種項目的組合。運算式清單以半形逗號分隔。

在運算式後方加入空格和 ID，即可為每個運算式指定別名。您也可選擇在運算式和別名之間加上 `AS` 關鍵字來提升可讀性。在 `SELECT` 子句中定義的別名，可參照查詢的 `GROUP BY`、`HAVING` 和 `ORDER BY` 子句，但不能參照 `FROM`、`WHERE` 或 `OMIT RECORD IF` 子句，也不能參照同一個 `SELECT` 子句中的其他運算式。

**注意：**

* 如要在 `SELECT` 子句中使用[匯總函式](#aggfunctions)，您必須在所有運算式中使用匯總函式，或查詢中的 `GROUP BY` 子句必須包含 `SELECT` 子句中的所有非匯總欄位做為分組鍵。例如：

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
* 您可以使用方括號來逸出[保留字詞](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/lexical?hl=zh-tw#reserved_keywords)，這樣就能將保留字詞做為欄位名稱和別名。舉例來說，如果您有名為「partition」的資料欄，由於這在 BigQuery 語法中屬於保留字詞，因此參照該欄位的查詢會發生不明錯誤。如要避免這項錯誤，請在「partition」前後加上方括號：

  ```
  SELECT [partition] FROM ...
  ```

##### 範例

這個範例會在 `SELECT` 子句中定義別名，然後在 `ORDER BY` 子句中參照其中一個別名。請注意，「word」資料欄不能透過 `WHERE` 子句中的「word\_alias」參照，而必須透過名稱參照。「len」別名也不會出現在 `WHERE` 子句中，這項資訊會顯示在 `HAVING` 子句中。

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

`WITHIN` 關鍵字會導致匯總函式匯總每個記錄中的重複值。且只會為每項輸入記錄產生一個匯總結果。這類匯總作業稱為「範圍匯總」。由於範圍匯總會為每筆記錄產生輸出內容，因此您可以選取非匯總運算式，以及範圍匯總運算式，而不使用 `GROUP BY` 子句。

在大多數的情況下，您會搭配 `RECORD` 範圍使用範圍匯總。如果您有非常複雜的巢狀重複結構定義，就可能需要在子記錄範圍中執行匯總作業，如要這麼做，請將上述語法中的 `RECORD` 關鍵字，替換為要在結構定義中執行匯總作業的節點名稱。如要進一步瞭解這項進階行為，請參閱「[處理資料](https://docs.cloud.google.com/bigquery/docs/data?hl=zh-tw#within)」。

##### 範例

這個範例會執行範圍內的 `COUNT` 匯總，然後依匯總值篩選及排序記錄。

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

`FROM` 子句會指定要查詢的來源資料。BigQuery 查詢可以直接對資料表、子查詢、聯結資料表，以及經由下文所述特殊用途運算子修改的資料表執行。使用[逗號](#comma_as_union_all) (這是 BigQuery 的 `UNION ALL` 運算子) 即可查詢這些資料來源的組合。

#### 參照資料表

參照資料表時，必須同時指定 *datasetId* 和 *tableId*；*project\_name* 則是選填項目。如未指定 *project\_name*，BigQuery 預設會使用目前的專案。如果專案名稱包含破折號，您必須以方括號括住整個資料表參照。

##### 範例

```
[my-dashed-project:dataset1.tableName]
```

在資料表名稱後方加上空格和 ID，即可為資料表提供別名。您也可以選擇在「tableId」*tableId*和別名之間加上 `AS` 關鍵字來提升可讀性。

從資料表參照資料欄時，您可以使用簡單的資料欄名稱，也可以在資料欄名稱加上前置字元，也就是別名 (如有指定)，或是 *datasetId* 和 *tableId* (只要未指定 *project\_name* 即可)。欄前置字串不得包含 *project\_name*，因為欄位名稱不得包含半形冒號。

##### 範例

這個範例參照的資料欄沒有資料表前置字元。

```
#legacySQL
SELECT
  word
FROM
  [bigquery-public-data:samples.shakespeare];
```

這個範例會在資料欄名稱加上 *datasetId* 和 *tableId* 前置字元。請注意，本範例中不得包含 *project\_name*。只有在資料集屬於目前預設專案的情況下，這種做法才有效。

```
#legacySQL
SELECT
  samples.shakespeare.word
FROM
  samples.shakespeare;
```

這個範例會在資料欄名稱前面加上資料表別名。

```
#legacySQL
SELECT
  t.word
FROM
  [bigquery-public-data:samples.shakespeare] AS t;
```

#### 整數範圍分區資料表

舊版 SQL 支援使用資料表修飾符，處理整數範圍分區資料表中的特定分區。範圍分區的處理關鍵是範圍的起始值。

以下範例會查詢開頭為 30 的範圍分區：

```
#legacySQL
SELECT
  *
FROM
  dataset.table$30;
```

請注意，您無法使用舊版 SQL 查詢整個整數範圍分區資料表。而是傳回類似下列內容的錯誤：

`Querying tables partitioned on a field is not supported in Legacy SQL`

#### 使用子查詢

「子查詢」是前後加上括號的巢狀 `SELECT` 陳述式。如同[資料表](#from_tables)的資料欄，子查詢的 `SELECT` 子句中計算用的運算式也可供外部查詢使用。

子查詢可用於計算匯總和其他運算式。且您可以在當中使用所有的 SQL 運算子。這表示子查詢本身可包含其他子查詢，且能夠執行聯結和分組匯總等作業。

#### 逗號：`UNION ALL`

與 GoogleSQL 不同，舊版 SQL 使用半形逗號做為 `UNION ALL` 運算子，而非 `CROSS JOIN` 運算子。這是舊版行為，因為 BigQuery 過去不支援 `CROSS JOIN`，而 BigQuery 使用者經常需要編寫 `UNION ALL` 查詢。在 GoogleSQL 中，執行聯集的查詢特別冗長。而使用逗號做為聯結運算子可讓使用者更有效率地撰寫這類查詢。舉例來說，這項查詢可用於對多天的記錄執行單一查詢。

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

一般來說，在處理的資料量相同的情況下，如果查詢會聯結大量資料表，其執行速度會比處理單一資料表的查詢要慢。兩者的效能差異最高可達每個額外資料表 50 毫秒。單一查詢最多可聯集 1,000 個資料表。

#### 資料表萬用字元函式

*資料表萬用字元函式*是指 BigQuery 獨有的特殊函式類型。
這些函式用於 `FROM` 子句，可使用多種篩選器類型之一，比對資料表名稱集合。舉例來說，`TABLE_DATE_RANGE` 函式可用於只查詢特定的一組每日資料表。如要進一步瞭解這些函式，請參閱[資料表萬用字元函式](#tablewildcardfunctions)。

#### FLATTEN 運算子

```
(FLATTEN([project_name:]datasetId.tableId, field_to_be_flattened))
(FLATTEN((subquery), field_to_be_flattened))
```

與一般 SQL 處理系統不同，BigQuery 的設計宗旨是處理重複資料。因此，BigQuery 使用者有時會需要撰寫操弄重複記錄結構的查詢，其中一種做法是使用 `FLATTEN` 運算子。

`FLATTEN` 會將結構定義中的一個節點從重複型式轉換成選用型式。如果記錄中含有重複欄位的一或多個值，`FLATTEN` 會建立多筆記錄，重複欄位中的每個值各對應一筆記錄。系統會在每個新的輸出記錄中，複製記錄中所有其他已選取的欄位。`FLATTEN` 可重複套用，移除多個重複層級。

如需更多資訊和範例，請參閱「[處理資料](https://docs.cloud.google.com/bigquery/docs/data?hl=zh-tw#flatten)」。

#### JOIN 運算子

BigQuery 支援在每個 `FROM` 子句中使用多個 `JOIN` 運算子。
後續的 `JOIN` 作業會將先前 `JOIN` 作業的結果做為左側 `JOIN` 輸入內容。任何先前 `JOIN` 輸入內容的欄位，都可以做為後續 `JOIN` 運算子 `ON` 子句中的鍵。

##### JOIN 類型

BigQuery 支援 `INNER`、`[FULL|RIGHT|LEFT] OUTER` 和 `CROSS JOIN` 作業。如未指定，則預設值為 `INNER`。

`CROSS JOIN` 作業不允許使用 `ON` 子句。`CROSS JOIN`
可能會傳回大量資料，導致查詢速度緩慢且效率不彰，或查詢超出每個查詢允許的資源上限。這類查詢會發生錯誤。請盡可能不要在查詢中使用 `CROSS JOIN`。舉例來說，`CROSS JOIN` 通常是用在[窗型函式](#windowfunctions)較有效率的情況下。

##### EACH 修飾符

`EACH` 修飾符會提示 BigQuery 使用多個分割區執行 `JOIN`。如果您知道 `JOIN` 兩側的值都很大，這項功能就特別實用。`EACH` 修飾符無法用於 `CROSS JOIN` 子句。

過去，我們會鼓勵使用者在許多情況下使用 `EACH`，如今則不建議這樣做。請儘可能在不加入 `EACH` 修飾符的情況下使用 `JOIN`，以提高執行效能。發生查詢資源超出上限的錯誤時才需使用 `JOIN EACH`。

##### 半聯結和反聯結

除了支援在 `FROM` 子句中使用 `JOIN` 以外，BigQuery 還支援在 `WHERE` 子句中使用兩種聯結，分別是半聯結和反半聯結。半聯結的指定方式是使用 `IN` 關鍵字和子查詢，反聯結的指定方式則是使用 `NOT IN` 關鍵字。

###### 範例

下列查詢會使用半聯結，找出 ngram 中第一個字詞也是另一個 ngram 中第二個字詞的 ngram，且該 ngram 的第三個字詞為「AND」。

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
            WHERE
              third = "AND")
LIMIT 10;
```

以下查詢使用了半聯結來傳回符合特定條件的女性數量，這類女性的年齡超過 50 歲，且曾在美國新生兒人數最多的 10 個州生過小孩。

```
#legacySQL
SELECT
  mother_age,
  COUNT(mother_age) total
FROM
  [bigquery-public-data:samples.natality]
WHERE
  state IN (SELECT
              state
            FROM
              (SELECT
                 state,
                 COUNT(state) total
               FROM
                 [bigquery-public-data:samples.natality]
               GROUP BY
                 state
               ORDER BY
                 total DESC
               LIMIT 10))
  AND mother_age > 50
GROUP BY
  mother_age
ORDER BY
  mother_age DESC
```

如要查看其他 40 州的數據，您可以使用反聯結。以下查詢與前述範例幾乎一樣，但使用了 `NOT IN` (而不是 `IN`) 來傳回符合特定條件的女性數量，這類女性的年齡超過 50 歲，且曾在美國新生兒人數最少的 40 個州生過小孩。

```
#legacySQL
SELECT
  mother_age,
  COUNT(mother_age) total
FROM
  [bigquery-public-data:samples.natality]
WHERE
  state NOT IN (SELECT
                  state
                FROM
                  (SELECT
                     state,
                     COUNT(state) total
                   FROM
                     [bigquery-public-data:samples.natality]
                   GROUP BY
                     state
                   ORDER BY
                     total DESC
                   LIMIT 10))
  AND mother_age > 50
GROUP BY
  mother_age
ORDER BY
  mother_age DESC
```

注意：

* BigQuery 不支援相關半聯結或反半聯結。子查詢無法參照外部查詢中的任何欄位。
* 半聯結或反半聯結中使用的子查詢只能選取一個欄位。
* 所選欄位和 `WHERE` 子句中外部查詢所用欄位的類型必須完全相符。BigQuery 不會對半聯結或反半聯結執行任何型別強制轉換。

### WHERE 子句

`WHERE` 子句 (有時稱為述詞) 會使用布林運算式，篩選 `FROM` 子句產生的記錄。多個條件可由布林值 `AND` 和 `OR` 子句聯結，並可選擇以括號 () 括住，將條件分組。`WHERE` 子句中列出的欄位不需在對應的 `SELECT` 子句中選取，且 `WHERE` 子句運算式無法參照 `WHERE` 子句所屬查詢的 `SELECT` 子句中計算的運算式。

**注意：**匯總函式不能用於 `WHERE` 子句。如果您需要篩選匯總函式的輸出結果，請使用 [`HAVING`](#having) 子句和外部查詢。

##### 範例

以下範例在 `WHERE` 子句中使用布林運算式的析取，也就是以 `OR` 運算子聯結的兩個運算式。如果任一運算式傳回 `true`，輸入記錄就會通過 `WHERE` 篩選器。

```
#legacySQL
SELECT
  word
FROM
  [bigquery-public-data:samples.shakespeare]
WHERE
  (word CONTAINS 'prais' AND word CONTAINS 'ing') OR
  (word CONTAINS 'laugh' AND word CONTAINS 'ed');
```

### OMIT RECORD IF 子句

`OMIT RECORD IF` 子句是 BigQuery 獨有的建構函式。特別適合用來處理巢狀重複結構定義。這與 `WHERE` 子句類似，但有兩項重大差異。首先，這個區塊會使用排除條件，也就是說，如果運算式傳回 `true`，系統就會省略記錄，但如果運算式傳回 `false` 或 `null`，系統就會保留記錄。其次，`OMIT RECORD IF` 子句可以在條件中使用範圍匯總函式 (通常會這麼做)。

除了篩選完整記錄以外，`OMIT...IF` 還可指定更小的範圍，藉此只篩選部分記錄，方法是使用結構定義中非分葉節點的名稱，而不要在 `OMIT...IF` 子句中使用 `RECORD`。BigQuery 使用者很少使用這項功能。您可以透過上方的 [`WITHIN`](#within) 說明文件連結，找到這項進階行為的更多相關說明。

如果您使用 [`OMIT...IF`](https://docs.cloud.google.com/bigquery/docs/reference/legacy-sql?hl=zh-tw#omit) 排除重複欄位中記錄的一部分，且查詢同時選取了其他獨立的重複欄位，BigQuery 就會排除查詢中其他重複記錄的一部分。如果看到這項錯誤，建議您改用 GoogleSQL。`Cannot perform OMIT IF on repeated scope <scope> with independently repeating pass through field <field>,`如要瞭解如何將 `OMIT...IF` 陳述式遷移至 GoogleSQL，請參閱[遷移至 GoogleSQL](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/migrating-from-legacy-sql?hl=zh-tw#filtering_rows_with_omit_record_if) 一文。

##### 範例

回顧 `WITHIN` 修飾符的範例，`OMIT RECORD IF` 可用於完成 `WITHIN` 和 `HAVING` 在該範例中執行的相同操作。

```
#legacySQL
SELECT
  repository.url
FROM
  [bigquery-public-data:samples.github_nested]
OMIT RECORD IF
  COUNT(payload.pages.page_name) <= 80;
```

### GROUP BY 子句

`GROUP BY` 子句可讓您將特定欄位或欄位集具有相同值的資料列分組，以便計算相關欄位的匯總。分組作業會在 `WHERE` 子句中執行篩選作業後進行，但會在計算 `SELECT` 子句中的運算式前完成。運算式結果不得做為 `GROUP BY` 子句中的群組鍵。

##### 範例

這項查詢會找出三元組樣本資料集中最常見的前十個*第一個字*。
除了示範如何使用 `GROUP BY` 子句，這個範例也說明如何在 `GROUP BY` 和 `ORDER BY` 子句中使用位置索引，而非欄位名稱。

```
#legacySQL
SELECT
  first,
  COUNT(ngram)
FROM
  [bigquery-public-data:samples.trigrams]
GROUP BY
  1
ORDER BY
  2 DESC
LIMIT 10;
```

使用 `GROUP BY` 子句執行的匯總作業稱為「分組匯總」。與[範圍匯總](#scopedaggregation)不同，分組匯總在大多數 SQL 處理系統中都很常見。

#### `EACH` 修飾符

`EACH` 修飾符會提示 BigQuery 使用多個分割區執行 `GROUP BY`。如果資料集包含大量群組鍵的相異值，這個方法就特別實用。

`EACH`在許多情況下都曾受到鼓勵，但現在已非如此。
在不加入 `EACH` 修飾符的情況下使用 `GROUP BY` 通常效能較佳。
發生查詢資源超出上限的錯誤時才需使用 `GROUP EACH BY`。

#### `ROLLUP` 函式

使用 `ROLLUP` 函式時，BigQuery 會在查詢結果中新增額外資料列，代表匯總的「總計」。`ROLLUP` 後列出的所有欄位都必須以一組括號括住。在因 `ROLLUP` 函式而新增的資料列中，`NULL` 表示匯總作業的匯總對象資料欄。

##### 範例

這項查詢會從範例出生率資料集，產生每年男嬰和女嬰的出生人數。

```
#legacySQL
SELECT
  year,
  is_male,
  COUNT(1) as count
FROM
  [bigquery-public-data:samples.natality]
WHERE
  year >= 2000
  AND year <= 2002
GROUP BY
  ROLLUP(year, is_male)
ORDER BY
  year,
  is_male;
```

這些是查詢結果。您會發現有些資料列的一或兩個分組鍵為 `NULL`。這些資料列是*匯總*資料列。

```
+------+---------+----------+
| year | is_male |  count   |
+------+---------+----------+
| NULL |    NULL | 12122730 |
| 2000 |    NULL |  4063823 |
| 2000 |   false |  1984255 |
| 2000 |    true |  2079568 |
| 2001 |    NULL |  4031531 |
| 2001 |   false |  1970770 |
| 2001 |    true |  2060761 |
| 2002 |    NULL |  4027376 |
| 2002 |   false |  1966519 |
| 2002 |    true |  2060857 |
+------+---------+----------+
```

使用 `ROLLUP` 函式時，您可以運用 `GROUPING` 函式，區分因 `ROLLUP` 函式而新增的資料列，以及群組鍵實際具有 `NULL` 值的資料列。

##### 範例

這個查詢會在先前的範例中加入 `GROUPING` 函式，以便更清楚識別因 `ROLLUP` 函式而新增的資料列。

```
#legacySQL
SELECT
  year,
  GROUPING(year) as rollup_year,
  is_male,
  GROUPING(is_male) as rollup_gender,
  COUNT(1) as count
FROM
  [bigquery-public-data:samples.natality]
WHERE
  year >= 2000
  AND year <= 2002
GROUP BY
  ROLLUP(year, is_male)
OR
```