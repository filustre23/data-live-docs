Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 資料表函式

資料表函式 (也稱為資料表值函式 (TVF)) 是使用者定義的函式，會傳回資料表。您可以在任何可使用資料表的地方使用資料表函式。資料表函式的行為與檢視類似，但資料表函式可以採用參數。

## 建立資料表函式

如要建立資料表函式，請使用 [`CREATE TABLE FUNCTION`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#create_table_function_statement) 陳述式。資料表函式包含產生資料表的查詢。函式會傳回查詢結果。下列資料表函式會採用 `INT64` 參數，並在查詢的 `WHERE` 子句中使用這個值，查詢名為 `bigquery-public-data.usa_names.usa_1910_current` 的[公開資料集](https://docs.cloud.google.com/bigquery/public-data?hl=zh-tw)：

```
CREATE OR REPLACE TABLE FUNCTION mydataset.names_by_year(y INT64)
AS (
  SELECT year, name, SUM(number) AS total
  FROM `bigquery-public-data.usa_names.usa_1910_current`
  WHERE year = y
  GROUP BY year, name
);
```

如要以其他方式篩選，可以將多個參數傳遞至表格函式。
下列資料表函式會依年份和名稱前置字元篩選資料：

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

### 表格參數

**預覽**

這項功能適用《[服務專屬條款](https://docs.cloud.google.com/terms/service-terms?hl=zh-tw#1)》中「一般服務條款」一節的《正式發布前產品條款》。正式發布前功能是依「原樣」提供，支援服務可能受限。
詳情請參閱[推出階段說明](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages)。

注意：如要尋求支援或針對這項功能提供意見回饋，請傳送電子郵件至 [bq-dcr-eng@google.com](mailto:bq-dcr-eng@google.com)。

您可以將 TVF 參數設為資料表。在資料表參數名稱後方，您必須明確指定必要的資料表結構，指定方式與結構體的欄位相同。傳遞至 TVF 的表格引數可包含參數結構定義中指定的資料欄以外的資料欄，且資料欄可依任意順序顯示。

下列資料表函式會傳回包含 `item_name` 資料表總銷售額的資料表 (來自 `orders` 資料表)：

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

### 參數名稱

如果資料表函式參數與資料表欄的名稱相符，可能會建立不明確的參照。在這種情況下，BigQuery 會將名稱解讀為資料表欄的參照，而非參數。建議您使用與任何參照資料表欄名稱不同的參數名稱。

## 使用資料表函式

您可以在任何資料表有效的環境中呼叫資料表函式。下列範例會在 `SELECT` 陳述式的 `FROM` 子句中呼叫 `mydataset.names_by_year` 函式：

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

您可以將資料表函式的輸出內容與另一個資料表彙整：

```
SELECT *
  FROM `bigquery-public-data.samples.shakespeare` AS s
  JOIN mydataset.names_by_year(1950) AS n
  ON n.name = s.word
```

您也可以在[子查詢](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/subqueries?hl=zh-tw#array_subquery_concepts)中使用表格函式：

```
SELECT ARRAY(
  SELECT name FROM mydataset.names_by_year(1950)
  ORDER BY total DESC
  LIMIT 5)
```

呼叫含有資料表參數的資料表函式時，您必須在資料表引數名稱前使用 `TABLE` 關鍵字。資料表引數可以有資料表參數結構定義中未列出的資料欄：

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

### 搭配 TVF 使用系統變數

TVF 支援 `@@session_id` 和 `@@location`
[系統變數](https://docs.cloud.google.com/bigquery/docs/reference/system-variables?hl=zh-tw)。您可以在函式建立陳述式中的任何位置加入這些系統變數，傳回目前查詢的工作階段 ID 或位置。系統不支援其他系統變數。

## 列出資料表函式

資料表函式是一種常式，如要列出資料集中的所有常式，請參閱「[列出常式](https://docs.cloud.google.com/bigquery/docs/routines?hl=zh-tw#list_routines)」。

## 刪除資料表函式

如要刪除資料表函式，請使用
[`DROP TABLE FUNCTION`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#drop_table_function)
陳述式：

```
DROP TABLE FUNCTION mydataset.names_by_year
```

## 授權處理常式

您可以將資料表函式授權為*常式*。授權常式可讓您與特定使用者或群組分享查詢結果，而不授予他們產生結果的基礎資料表存取權。舉例來說，授權常式可以計算資料的匯總值，或查閱資料表值並用於計算。詳情請參閱「[已授權的日常安排](https://docs.cloud.google.com/bigquery/docs/authorized-routines?hl=zh-tw)」。

## 限制

* 查詢主體必須是 `SELECT` 陳述式，且不得修改任何內容。舉例來說，資料定義語言 (DDL) 和資料操縱語言 (DML) 陳述式不允許用於資料表函式。如果需要副作用，建議改為編寫[程序](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#create_procedure)。
* 資料表函式必須與參照的資料表儲存在相同位置。

## 配額

如要進一步瞭解表格函式配額和限制，請參閱[配額和限制](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#table_function_limits)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-02 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-02 (世界標準時間)。"],[],[]]