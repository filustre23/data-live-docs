Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [參考資料](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 使用舊版 SQL 查詢巢狀與重複的欄位

本文詳細說明如何使用舊版 SQL 查詢語法查詢巢狀和重複資料。我們建議使用的 BigQuery 查詢語法是 GoogleSQL。如要瞭解如何使用 GoogleSQL 處理巢狀和重複的資料，請參閱 [GoogleSQL 遷移指南](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/migrating-from-legacy-sql?hl=zh-tw#differences_in_repeated_field_handling)。

BigQuery 支援以 JSON 與 Avro 檔案格式[載入](https://docs.cloud.google.com/bigquery/docs/loading-data-cloud-storage-json?hl=zh-tw#loading_nested_and_repeated_json_data)及[匯出](https://docs.cloud.google.com/bigquery/exporting-data-from-bigquery?hl=zh-tw)巢狀與重複的資料。BigQuery 可為許多舊版 SQL 查詢自動整併資料。舉例來說，許多 `SELECT` 陳述式皆可在維持資料結構的情況下，擷取巢狀或重複的欄位；而 `WHERE` 子句則可以在維持資料結構的情況下篩選資料。相反地，`ORDER BY` 和 `GROUP BY` 子句會自動整併查詢資料。針對無法自動整併資料的環境 (例如使用舊版 SQL 查詢多個重複欄位時)，您可以使用 `FLATTEN` 與 `WITHIN` SQL 函式查詢資料。

### FLATTEN

在查詢巢狀資料時，BigQuery 會自動為您整併資料表的資料。
請參閱以下個人資料的結構定義範例：

```
   Last modified                 Schema                 Total Rows   Total Bytes   Expiration
 ----------------- ----------------------------------- ------------ ------------- ------------
  27 Sep 10:01:06   |- kind: string                     4            794
                    |- fullName: string (required)
                    |- age: integer
                    |- gender: string
                    +- phoneNumber: record
                    |  |- areaCode: integer
                    |  |- number: integer
                    +- children: record (repeated)
                    |  |- name: string
                    |  |- gender: string
                    |  |- age: integer
                    +- citiesLived: record (repeated)
                    |  |- place: string
                    |  +- yearsLived: integer (repeated)
```

請注意，有些是重複和巢狀的欄位。如果您對 person 資料表執行下列舊版 SQL 查詢：

```
SELECT
  fullName AS name,
  age,
  gender,
  citiesLived.place,
  citiesLived.yearsLived
FROM [dataset.tableId]
```

BigQuery 會將您的資料以整併的形式輸出：

```
+---------------+-----+--------+-------------------+------------------------+
|     name      | age | gender | citiesLived_place | citiesLived_yearsLived |
+---------------+-----+--------+-------------------+------------------------+
| John Doe      |  22 | Male   | Seattle           |                   1995 |
| John Doe      |  22 | Male   | Stockholm         |                   2005 |
| Mike Jones    |  35 | Male   | Los Angeles       |                   1989 |
| Mike Jones    |  35 | Male   | Los Angeles       |                   1993 |
| Mike Jones    |  35 | Male   | Los Angeles       |                   1998 |
| Mike Jones    |  35 | Male   | Los Angeles       |                   2002 |
| Mike Jones    |  35 | Male   | Washington DC     |                   1990 |
| Mike Jones    |  35 | Male   | Washington DC     |                   1993 |
| Mike Jones    |  35 | Male   | Washington DC     |                   1998 |
| Mike Jones    |  35 | Male   | Washington DC     |                   2008 |
| Mike Jones    |  35 | Male   | Portland          |                   1993 |
| Mike Jones    |  35 | Male   | Portland          |                   1998 |
| Mike Jones    |  35 | Male   | Portland          |                   2003 |
| Mike Jones    |  35 | Male   | Portland          |                   2005 |
| Mike Jones    |  35 | Male   | Austin            |                   1973 |
| Mike Jones    |  35 | Male   | Austin            |                   1998 |
| Mike Jones    |  35 | Male   | Austin            |                   2001 |
| Mike Jones    |  35 | Male   | Austin            |                   2005 |
| Anna Karenina |  45 | Female | Stockholm         |                   1992 |
| Anna Karenina |  45 | Female | Stockholm         |                   1998 |
| Anna Karenina |  45 | Female | Stockholm         |                   2000 |
| Anna Karenina |  45 | Female | Stockholm         |                   2010 |
| Anna Karenina |  45 | Female | Moscow            |                   1998 |
| Anna Karenina |  45 | Female | Moscow            |                   2001 |
| Anna Karenina |  45 | Female | Moscow            |                   2005 |
| Anna Karenina |  45 | Female | Austin            |                   1995 |
| Anna Karenina |  45 | Female | Austin            |                   1999 |
+---------------+-----+--------+-------------------+------------------------+
```

在這個範例中，`citiesLived.place` 現在是 `citiesLived_place`，而 `citiesLived.yearsLived` 現在是 `citiesLived_yearsLived`。

雖然 BigQuery 能自動整併巢狀欄位，不過您在處理超過多個重複欄位時，可能仍需明確呼叫 `FLATTEN`。例如，如果您嘗試執行與下列內容相似的舊版 SQL 查詢：

```
SELECT fullName, age
FROM [dataset.tableId]
WHERE
  (citiesLived.yearsLived > 1995 ) AND
  (children.age > 3)
```

BigQuery 會傳回如下所示的錯誤：

```
Cannot query the cross product of repeated fields children.age and citiesLived.yearsLived
```

若要查詢超過一個重複的欄位，您就必須整併其中一個欄位：

```
SELECT
  fullName,
  age,
  gender,
  citiesLived.place
FROM (FLATTEN([dataset.tableId], children))
WHERE
  (citiesLived.yearsLived > 1995) AND
  (children.age > 3)
GROUP BY fullName, age, gender, citiesLived.place
```

它會傳回：

```
+------------+-----+--------+-------------------+
|  fullName  | age | gender | citiesLived_place |
+------------+-----+--------+-------------------+
| John Doe   |  22 | Male   | Stockholm         |
| Mike Jones |  35 | Male   | Los Angeles       |
| Mike Jones |  35 | Male   | Washington DC     |
| Mike Jones |  35 | Male   | Portland          |
| Mike Jones |  35 | Male   | Austin            |
+------------+-----+--------+-------------------+
```

### WITHIN 子句

`WITHIN` 關鍵字專門搭配匯總函式使用，可在記錄與巢狀欄位中跨子女欄位與重複欄位進行匯總。指定 `WITHIN` 關鍵字時，您需要指定要匯總的範圍：

* `WITHIN RECORD`：匯總記錄中重複值的資料。
* `WITHIN node_name`：匯總指定節點中重複值的資料，其中節點是匯總函式中欄位的父項節點。

假設您想知道上一個範例內每個人有幾個小孩。您可以計算每筆記錄擁有的 children.name 數量：

```
SELECT
  fullName,
  COUNT(children.name) WITHIN RECORD AS numberOfChildren
FROM [dataset.tableId];
```

結果如下：

```
+---------------+------------------+
|   fullName    | numberOfChildren |
+---------------+------------------+
| John Doe      |                2 |
| Jane Austen   |                2 |
| Mike Jones    |                3 |
| Anna Karenina |                0 |
+---------------+------------------+
```

您可以列出所有孩童的姓名來進行比較：

```
SELECT fullName, children.name
FROM [dataset.tableId]
```

```
+---------------+---------------+
|   fullName    | children_name |
+---------------+---------------+
| John Doe      | Jane          |
| John Doe      | John          |
| Jane Austen   | Josh          |
| Jane Austen   | Jim           |
| Mike Jones    | Earl          |
| Mike Jones    | Sam           |
| Mike Jones    | Kit           |
| Anna Karenina | None          |
+---------------+---------------+
```

這與我們的 `WITHIN RECORD` 查詢結果相符：John Doe 的確有兩個名為 Jane 和 John 的小孩；Jane Austen 有兩個名為 Josh 和 Jim 的小孩；Mike Jones 有三個名為 Earl、Sam 和 Kit 的小孩；而 Anna Karenina 則沒有小孩。

現在，假設您想要知道某個人在不同地方居住過的次數。
就可以使用 `WITHIN` 子句來彙整特定節點：

```
SELECT
  fullName,
  COUNT(citiesLived.place) WITHIN RECORD AS numberOfPlacesLived,
  citiesLived.place,
  COUNT(citiesLived.yearsLived) WITHIN citiesLived AS numberOfTimesInEachCity,
FROM [dataset.tableId];
```

```
+---------------+---------------------+-------------------+-------------------------+
|   fullName    | numberOfPlacesLived | citiesLived_place | numberOfTimesInEachCity |
+---------------+---------------------+-------------------+-------------------------+
| John Doe      |                   2 | Seattle           |                       1 |
| John Doe      |                   2 | Stockholm         |                       1 |
| Mike Jones    |                   4 | Los Angeles       |                       4 |
| Mike Jones    |                   4 | Washington DC     |                       4 |
| Mike Jones    |                   4 | Portland          |                       4 |
| Mike Jones    |                   4 | Austin            |                       4 |
| Anna Karenina |                   3 | Stockholm         |                       4 |
| Anna Karenina |                   3 | Moscow            |                       3 |
| Anna Karenina |                   3 | Austin            |                       2 |
+---------------+---------------------+-------------------+-------------------------+
```

這個查詢會執行以下動作：

* 對 `citiesLived.place` 執行 `WITHIN RECORD`，並計算每個人分別居住過幾個地方
* 對 `citiesLived.yearsLived` 執行 `WITHIN`，並計算每個人分別在各個城市的居住次數 (只計算 `citiesLived`)。

其中一項 BigQuery 具有的強大功能就是可對巢狀與重複的欄位使用範圍匯總，而這通常能避免查詢中出現成本昂貴的彙整。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-02 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-02 (世界標準時間)。"],[],[]]