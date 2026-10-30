Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 資料表函式

資料表函式也稱為資料表值函式 (TVF)，是會傳回資料表的使用者定義函式。只要是可以使用資料表的地方，都可以使用資料表函式。資料表函式的行為與檢視表類似，但資料表函式可以接受參數。

## 建立資料表函式

如要建立資料表函式，請使用 [`CREATE TABLE FUNCTION`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#create_table_function_statement) 陳述式。資料表函式包含會產生資料表的查詢。函式會傳回查詢結果。下列資料表函式會採用 `INT64` 參數，並在查詢 `bigquery-public-data.usa_names.usa_1910_current` [公開資料集](https://docs.cloud.google.com/bigquery/public-data?hl=zh-tw)時，於 `WHERE` 子句中使用這個值：

```
CREATE OR REPLACE TABLE FUNCTION mydataset.names_by_year(y INT64)
AS (
  SELECT year, name, SUM(number) AS total
  FROM `bigquery-public-data.usa_names.usa_1910_current`
  WHERE year = y
  GROUP BY year, name
);
```

如要以其他方式篩選，可以將多個參數傳遞至資料表函式。下列資料表函式會依年份和名稱前置字串篩選資料：

```
CREATE OR REPLACE TABLE FUNCTION mydataset.names_by_year_and_prefix(
  y INT64, z STRING)
AS (
  SELECT year, name, SUM(number) AS total
  FROM `bigquery-public-data.usa_names.usa_1910_current`
  WHERE
    year = y
    AND STARTS_WITH(name, z)
  GROUP BY year, name
);
```

### 資料表參數

您可以將 TVF 參數設為資料表。在資料表參數名稱後方，您必須明確指定必要的資料表結構定義，方法與指定結構體欄位相同。您傳遞至 TVF 的資料表引數可以包含參數結構定義中指定以外的其他資料欄，且資料欄可以任何順序顯示。

下列資料表函式會傳回一個資料表，其中包含 `orders` 資料表中 `item_name` 的總銷售額：

```
CREATE TABLE FUNCTION mydataset.compute_sales (
  orders TABLE<sales INT64, item STRING>, item_name STRING)
AS (
  SELECT SUM(sales) AS total_sales, item
  FROM orders
  WHERE item = item_name
  GROUP BY item
);
```

在 TVF 中使用 `ANY TABLE` 類型，即可建立接受任何結構資料表的通用函式。固定資料表必須定義每個資料欄和資料類型，但 `ANY TABLE` 類型則可做為預留位置，讓函式能與不同資料集重複使用。不過，您傳入的資料表仍須包含函式中使用的特定資料欄。舉例來說，如果函式依 `created_date` 篩選，輸入資料表必須有該資料欄，否則查詢會失敗。

```
-- Simple pass-through (accepts any table, as used in your devstack)
CREATE OR REPLACE TABLE FUNCTION dataset_test.MyTVF(input_table ANY TABLE)
AS
SELECT * FROM input_table;

-- Generic filter (accepts any table, but implicitly requires a 'status' column)
CREATE TEMP TABLE FUNCTION FilterByStatus(input_table ANY TABLE, status_val STRING)
AS
SELECT * FROM input_table
WHERE status = status_val;
```

### 參數名稱

如果資料表函式參數與資料表資料欄名稱相符，可能會建立不明確的參照。在這種情況下，BigQuery 會將名稱解讀為資料表資料欄的參照，而非參數。建議做法是使用與任何參照資料表欄名稱不同的參數名稱。

## 使用資料表函式

您可以在任何資料表有效的內容中呼叫資料表函式。以下範例在 `SELECT` 陳述式的 `FROM` 子句中呼叫 `mydataset.names_by_year` 函式：

```
SELECT * FROM mydataset.names_by_year(1950)
  ORDER BY total DESC
  LIMIT 5
```

結果如下所示：

```
+------+--------+-------+
| year |  name  | total |
+------+--------+-------+
| 1950 | James  | 86447 |
| 1950 | Robert | 83717 |
| 1950 | Linda  | 80498 |
| 1950 | John   | 79561 |
| 1950 | Mary   | 65546 |
+------+--------+-------+
```

您可以將資料表函式的輸出內容與其他資料表彙整：

```
SELECT *
  FROM `bigquery-public-data.samples.shakespeare` AS s
  JOIN mydataset.names_by_year(1950) AS n
  ON n.name = s.word
```

您也可以在[子查詢](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/subqueries?hl=zh-tw#array_subquery_concepts)中使用資料表函式：

```
SELECT ARRAY(
  SELECT name FROM mydataset.names_by_year(1950)
  ORDER BY total DESC
  LIMIT 5)
```

呼叫具有資料表參數的資料表函式時，必須在資料表引數名稱前使用 `TABLE` 關鍵字。資料表引數可以包含資料表參數結構定義中未列出的資料欄：

```
CREATE TABLE FUNCTION mydataset.compute_sales (
  orders TABLE<sales INT64, item STRING>, item_name STRING)
AS (
  SELECT SUM(sales) AS total_sales, item
  FROM orders
  WHERE item = item_name
  GROUP BY item
);

WITH my_orders AS (
    SELECT 1 AS sales, "apple" AS item, 0.99 AS price
    UNION ALL
    SELECT 2, "banana", 0.49
    UNION ALL
    SELECT 5, "apple", 0.99)
SELECT *
FROM mydataset.compute_sales(TABLE my_orders, "apple");

/*-------------+-------+
 | total_sales | item  |
 +-------------+-------+
 | 6           | apple |
 +-------------+-------*/
```

### 搭配使用系統變數與 TVF

`@@session_id` 和 `@@location`
[系統變數](https://docs.cloud.google.com/bigquery/docs/reference/system-variables?hl=zh-tw)支援 TVF。您可以在函式建立陳述式的任何位置加入這些系統變數，傳回目前查詢的工作階段 ID 或位置。不支援所有其他系統變數。

## 列出資料表函式

資料表函式是一種常式。如要列出資料集中的所有常式，請參閱「[列出常式](https://docs.cloud.google.com/bigquery/docs/routines?hl=zh-tw#list_routines)」。

## 刪除資料表函式

如要刪除資料表函式，請使用 [`DROP TABLE FUNCTION`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#drop_table_function) 陳述式：

```
DROP TABLE FUNCTION mydataset.names_by_year
```

## 授權給處理常式

您可以將資料表函式授權為*常式*。授權常式可讓您與特定使用者或群組分享查詢結果，而不必直接授予基礎資料表的存取權。舉例來說，常式可以計算匯總值或查詢資料表值，並在計算中使用該值。詳情請參閱「[授權常式](https://docs.cloud.google.com/bigquery/docs/authorized-routines?hl=zh-tw)」。

## 限制

* 查詢主體必須是 `SELECT` 陳述式，且不得修改任何內容。例如，資料表函式不允許使用資料定義語言 (DDL) 和資料操縱語言 (DML) 陳述式。如需副作用，建議改為編寫[程序](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#create_procedure)。
* 資料表函式必須與參照的資料表儲存在相同位置。

## 配額

如要進一步瞭解資料表函式配額和限制，請參閱「[配額和限制](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#table_function_limits)」。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-10-28 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-10-28 (世界標準時間)。"],[],[]]