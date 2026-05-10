Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 使用萬用字元資料表查詢多個資料表

**注意：** 萬用字元資料表有許多[限制](#limitations)，且效能不如利用[分區](https://docs.cloud.google.com/bigquery/docs/partitioned-tables?hl=zh-tw)和[叢集](https://docs.cloud.google.com/bigquery/docs/clustered-tables?hl=zh-tw)的 BigQuery 一般資料表。為達到最佳做法的成效，請盡可能採用分區資料表或叢集資料表。

萬用字元資料表可讓您使用精簡的 SQL 陳述式查詢多個資料表。萬用字元資料表僅適用於 GoogleSQL。如要在舊版 SQL 中使用對應的功能，請參閱[資料表萬用字元函式](https://docs.cloud.google.com/bigquery/query-reference?hl=zh-tw#tablewildcardfunctions)一文。

萬用字元資料表是符合萬用字元運算式的所有資料表的集合。舉例來說，下列 `FROM` 子句會使用萬用字元運算式 `gsod*`，比對 `noaa_gsod` 資料集中開頭為字串 `gsod` 的所有資料表。

```
FROM
  `bigquery-public-data.noaa_gsod.gsod*`
```

萬用字元資料表中的每一列都包含一個特殊資料欄 `_TABLE_SUFFIX`，當中有經萬用字元比對後所得出的值。

## 限制

萬用字元資料表查詢有下列限制。

* 萬用字元資料表功能不支援檢視區塊。如果萬用字元資料表與資料集中的任何檢視區塊相符，即使查詢在 `_TABLE_SUFFIX` 虛擬資料欄上包含 `WHERE` 子句來篩選檢視區塊，查詢仍會傳回錯誤。
* 使用萬用字元查詢多個資料表時，無法使用快取結果，即使已勾選「Use Cached Results」(使用快取結果) 選項也是如此。如果您執行相同的萬用字元查詢很多次，系統會針對每一筆查詢向您收費。
* 萬用字元資料表僅支援內建的 BigQuery 儲存空間。查詢[外部資料表](https://docs.cloud.google.com/bigquery/external-data-sources?hl=zh-tw)或[檢視表](https://docs.cloud.google.com/bigquery/docs/views?hl=zh-tw)時，不可以使用萬用字元。
* 您無法對分區不相容的資料表，或分區與非分區資料表混用的情況，使用萬用字元查詢。查詢的資料表也必須具有相同的叢集規格。
* 您可以在分區資料表中使用萬用字元資料表，且支援分區修剪和叢集修剪。不過，如果資料表已叢集處理但未分區，使用萬用字元時就無法充分發揮叢集修剪的優勢。
* 包含[資料操縱語言](https://docs.cloud.google.com/bigquery/docs/data-manipulation-language?hl=zh-tw) (DML) 陳述式的查詢，無法使用萬用字元資料表做為查詢目標。例如，可在 `UPDATE` 查詢的 `FROM` 子句中使用萬用字元資料表，但無法將萬用字元資料表做為 `UPDATE` 運算的目標。
* 包含 JavaScript 使用者定義函式的 `_TABLE_SUFFIX` 或 `_PARTITIONTIME` 虛擬資料欄篩選器，不會限制掃描萬用字元資料表中的資料表數量。
* 如果資料表受到客戶自行管理的加密金鑰 (CMEK) 保護，則不支援萬用字元查詢。
* 萬用字元查詢中參照的所有資料表，都必須具有完全相同的[標記](https://docs.cloud.google.com/bigquery/docs/tags?hl=zh-tw)鍵和值。
* 如果單一掃描的資料表有結構定義不符的情況 (也就是說，名稱相同的資料欄類型不同)，查詢就會失敗，並顯示「Cannot read field of type X as Y Field: column\_name」(無法將類型 X 的欄位讀取為類型 Y 的欄位：資料欄名稱) 錯誤訊息。即使使用等號運算子 `=`，系統也會比對所有資料表。舉例來說，在下列查詢中，系統也會掃描 `my_dataset.my_table_03_backup` 資料表。因此，查詢可能會因結構定義不符而失敗。不過，如果沒有結構定義不符的情況，結果會如預期只來自資料表 `my_dataset.my_table_03`。

  ```
  SELECT *
  FROM my_project.my_dataset.my_table_*
  WHERE _TABLE_SUFFIX = '03'
  ```
* BI Engine 不支援萬用字元資料表。
* 如果資料表具有彈性資料欄名稱或重新命名的資料欄，則不支援萬用字元資料表。如要避開這項限制，請從查詢中排除受影響的資料欄，或使用 `_TABLE_SUFFIX` 虛擬資料欄篩選資料表。

## 事前準備

* 確認您使用的是 GoogleSQL。詳情請參閱「[切換 SQL 方言](https://docs.cloud.google.com/bigquery/sql-reference/enabling-standard-sql?hl=zh-tw)」。
* 如果您使用的是舊版 SQL，請參閱[資料表萬用字元函式](https://docs.cloud.google.com/bigquery/query-reference?hl=zh-tw#tablewildcardfunctions)一節。
* 本頁面中許多範例使用了美國國家海洋暨大氣總署 (NOAA) 的公開資料集。如要進一步瞭解這些資料，請參閱 [NOAA 全球每日地面天氣摘要資料](https://console.cloud.google.com/bigquery?p=bigquery-public-data&%3Bd=noaa_gsod&%3Bpage=dataset&hl=zh-tw)。

## 使用萬用字元表格的時機

如果資料集包含多個名稱類似且具有相容結構定義的資料表，就很適合使用萬用字元資料表。一般來說，這類資料集所包含的每一個資料表都分別代表單日、單月或單一年度的資料。舉例來說，BigQuery 所託管的公開資料集 [NOAA 全球每日地面天氣摘要資料](https://console.cloud.google.com/bigquery?p=bigquery-public-data&%3Bd=noaa_gsod&%3Bpage=dataset&hl=zh-tw)包含許多資料表，分別代表 1929 年至今每一年的資料。

執行查詢以掃描 1929 年到 1940 年之間所有的資料表 ID 時，如果要在 `FROM` 子句中指定所有 12 個資料表，查詢會變得相當冗長 (以下範例已省略大部分的資料表)：

```
#standardSQL
SELECT
  max,
  ROUND((max-32)*5/9,1) celsius,
  mo,
  da,
  year
FROM (
  SELECT
    *
  FROM
    `bigquery-public-data.noaa_gsod.gsod1929` UNION ALL
  SELECT
    *
  FROM
    `bigquery-public-data.noaa_gsod.gsod1930` UNION ALL
  SELECT
    *
  FROM
    `bigquery-public-data.noaa_gsod.gsod1931` UNION ALL

  # ... Tables omitted for brevity

  SELECT
    *
  FROM
    `bigquery-public-data.noaa_gsod.gsod1940` )
WHERE
  max != 9999.9 # code for missing data
ORDER BY
  max DESC
```

如果使用萬用字元資料表，同一個查詢會變得精簡許多：

```
#standardSQL
SELECT
  max,
  ROUND((max-32)*5/9,1) celsius,
  mo,
  da,
  year
FROM
  `bigquery-public-data.noaa_gsod.gsod19*`
WHERE
  max != 9999.9 # code for missing data
  AND _TABLE_SUFFIX BETWEEN '29'
  AND '40'
ORDER BY
  max DESC
```

萬用字元資料表僅支援內建的 BigQuery 儲存空間。查詢[外部資料表](https://docs.cloud.google.com/bigquery/external-data-sources?hl=zh-tw)或[檢視表](https://docs.cloud.google.com/bigquery/docs/views?hl=zh-tw)時，不可以使用萬用字元。

## 萬用字元資料表語法

萬用字元資料表語法：

```
SELECT
FROM
  `<project-id>.<dataset-id>.<table-prefix>*`
WHERE
  bool_expression
```

<project-id>
:   Cloud Platform 專案 ID。如果您使用預設專案 ID，則為選用。

<dataset-id>
:   BigQuery 資料集 ID。

<table-prefix>
:   與萬用字元比對的所有資料表共用的字串。資料表前置字串可省略，如果省略資料表前置字串，系統會比對資料集中的所有資料表。

\* (萬用字元)
:   萬用字元「\*」代表資料表名稱的一或多個字元。萬用字元只能做為萬用字元資料表名稱的最後一個字元。

使用萬用字元資料表查詢時，`WHERE` 子句支援 `_TABLE_SUFFIX` 虛擬資料欄。這個資料欄包含與萬用字元相符的值，因此查詢可以篩選要存取的資料表。舉例來說，下列 `WHERE` 子句使用「比較運算子」篩選相符的表格：

```
WHERE
  _TABLE_SUFFIX BETWEEN '29' AND '40'

WHERE
  _TABLE_SUFFIX = '1929'

WHERE
  _TABLE_SUFFIX < '1941'
```

如要進一步瞭解 `_TABLE_SUFFIX` 虛擬資料欄，請參閱[使用 \_TABLE\_SUFFIX 篩選所選資料表](https://docs.cloud.google.com/bigquery/docs/querying-wildcard-tables?hl=zh-tw#filter_selected_tables_using_table_suffix)一節。

### 在倒引號中以萬用字元括住資料表名稱

萬用字元資料表名稱包含特殊字元 (\*)，這代表您必須將萬用字元資料表名稱括在倒引號 (`) 字元內。舉例來說，以下查詢使用了倒引號，屬於有效的查詢：

```
#standardSQL
/* Valid SQL query */
SELECT
  max
FROM
  `bigquery-public-data.noaa_gsod.gsod*`
WHERE
  max != 9999.9 # code for missing data
  AND _TABLE_SUFFIX = '1929'
ORDER BY
  max DESC
```

以下查詢因沒有正確使用倒引號而「無效」：

```
#standardSQL
/* Syntax error: Expected end of statement but got "-" at [4:11] */
SELECT
  max
FROM
  # missing backticks
  bigquery-public-data.noaa_gsod.gsod*
WHERE
  max != 9999.9 # code for missing data
  AND _TABLE_SUFFIX = '1929'
ORDER BY
  max DESC
```

引號無法運作：

```
#standardSQL
/* Syntax error: Unexpected string literal: 'bigquery-public-data.noaa_gsod.gsod*' at [4:3] */
SELECT
  max
FROM
  # quotes are not backticks
  'bigquery-public-data.noaa_gsod.gsod*'
WHERE
  max != 9999.9 # code for missing data
  AND _TABLE_SUFFIX = '1929'
ORDER BY
  max DESC
```

## 使用萬用字元資料表查詢資料表

萬用字元資料表可讓您以精簡的方式查詢多個資料表。舉例來說，BigQuery 所託管的公開資料集 [NOAA 全球每日地面天氣摘要資料](https://console.cloud.google.com/bigquery?p=bigquery-public-data&%3Bd=noaa_gsod&%3Bpage=dataset&hl=zh-tw)包含許多資料表，分別代表 1929 年至今每一年的資料，而且全都共用相同的前置字串 `gsod`，後面加上四位數的年份，資料表名稱分別為 `gsod1929`、`gsod1930`、`gsod1931` 等。

如要查詢一組前置字元都相同的資料表，請在 `FROM` 陳述式中的資料表前置字元後方加上資料表萬用字元符號 (\*)。舉例來說，以下查詢會找出 1940 年代期間所回報的最高氣溫：

```
#standardSQL
SELECT
  max,
  ROUND((max-32)*5/9,1) celsius,
  mo,
  da,
  year
FROM
  `bigquery-public-data.noaa_gsod.gsod194*`
WHERE
  max != 9999.9 # code for missing data
ORDER BY
  max DESC
```

## 使用 \_TABLE\_SUFFIX 篩選所選資料表

如要限制查詢，只掃描一組指定的資料表，請在 `WHERE` 子句中使用 `_TABLE_SUFFIX` 虛擬資料欄，並搭配常數運算式條件。

`_TABLE_SUFFIX` 虛擬資料欄包含與表格萬用字元相符的值。舉例來說，先前的範例查詢會掃描 1940 年代的所有資料表，並使用資料表萬用字元代表年份的最後一位數：

```
FROM
  `bigquery-public-data.noaa_gsod.gsod194*`
```

對應的 `_TABLE_SUFFIX` 虛擬資料欄包含 `0` 到 `9` 範圍內的值，代表表格 `gsod1940` 到 `gsod1949`。這些 `_TABLE_SUFFIX` 值可用於 `WHERE` 子句，篩選特定表格。

舉例來說，如要篩選出 1940 年到 1944 年之間的最高氣溫，請使用 `0` 和 `4` 來做為 `_TABLE_SUFFIX` 的值：

```
#standardSQL
SELECT
  max,
  ROUND((max-32)*5/9,1) celsius,
  mo,
  da,
  year
FROM
  `bigquery-public-data.noaa_gsod.gsod194*`
WHERE
  max != 9999.9 # code for missing data
  AND ( _TABLE_SUFFIX = '0'
    OR _TABLE_SUFFIX = '4' )
ORDER BY
  max DESC
```

使用 `_TABLE_SUFFIX` 可大幅減少掃描的位元組數，有助於降低查詢執行成本。

不過，如果 `_TABLE_SUFFIX` 篩選器包含沒有常數運算式的條件，就不會限制掃描萬用字元資料表的數量。舉例來說，下列查詢不會限制掃描的資料表，因為篩選條件使用 `table_id` 資料欄的動態值，因此無法限制萬用字元資料表 `bigquery-public-data.noaa_gsod.gsod19*`：

```
#standardSQL
# Scans all tables that match the prefix `gsod19`
SELECT
  ROUND((max-32)*5/9,1) celsius
FROM
  `bigquery-public-data.noaa_gsod.gsod19*`
WHERE
  _TABLE_SUFFIX = (SELECT SUBSTR(MAX(table_name), LENGTH('gsod19') + 1)
      FROM `bigquery-public-data.noaa_gsod.INFORMATION_SCHEMA.TABLES`
      WHERE table_name LIKE 'gsod194%')
```

再舉一例，下列查詢會根據第一個篩選條件 `_TABLE_SUFFIX BETWEEN '40' and '60'` 限制掃描，因為這是常數運算式。不過，以下查詢不會根據第二個篩選條件 `_TABLE_SUFFIX = (SELECT SUBSTR(MAX(table_name), LENGTH('gsod19')
+ 1) FROM bigquery-public-data.noaa_gsod.INFORMATION_SCHEMA.TABLES WHERE table_name LIKE
'gsod194%')` 限制掃描，因為這是動態運算式：

```
#standardSQL
# Scans all tables with names that fall between `gsod1940` and `gsod1960`
SELECT
  ROUND((max-32)*5/9,1) celsius
FROM
  `bigquery-public-data.noaa_gsod.gsod19*`
WHERE
  _TABLE_SUFFIX BETWEEN '40' AND '60'
  AND _TABLE_SUFFIX = (SELECT SUBSTR(MAX(table_name), LENGTH('gsod19') + 1)
      FROM `bigquery-public-data.noaa_gsod.INFORMATION_SCHEMA.TABLES`
      WHERE table_name LIKE 'gsod194%')
```

如要解決這個問題，請改為執行兩項不同的查詢，例如：

第一個查詢：

```
#standardSQL
# Get the list of tables that match the required table name prefixes
SELECT SUBSTR(MAX(table_name), LENGTH('gsod19') + 1)
      FROM `bigquery-public-data.noaa_gsod.INFORMATION_SCHEMA.TABLES`
      WHERE table_name LIKE 'gsod194%'
```

第二個查詢：

```
#standardSQL
# Construct the second query based on the values from the first query
SELECT
  ROUND((max-32)*5/9,1) celsius
FROM
  `bigquery-public-data.noaa_gsod.gsod19*`
WHERE _TABLE_SUFFIX = '49'
```

這些查詢範例使用 `INFORMATION_SCHEMA.TABLES` 檢視區塊。如要進一步瞭解 `INFORMATION_SCHEMA` 資料表，請參閱「[使用 INFORMATION\_SCHEMA 取得資料表中繼資料](https://docs.cloud.google.com/bigquery/docs/information-schema-tables?hl=zh-tw)」。

## 使用 \_TABLE\_SUFFIX 掃描特定範圍的資料表

如要掃描特定範圍的資料表，請搭配 `BETWEEN` 子句使用 `_TABLE_SUFFIX` 虛擬資料欄。舉例來說，如要找出 1929 年到 1935 年 (包含這兩年) 之間回報的最高氣溫，請使用資料表萬用字元來代表年份的最後兩位數字：

```
#standardSQL
SELECT
  max,
  ROUND((max-32)*5/9,1) celsius,
  mo,
  da,
  year
FROM
  `bigquery-public-data.noaa_gsod.gsod19*`
WHERE
  max != 9999.9 # code for missing data
  AND _TABLE_SUFFIX BETWEEN '29' and '35'
ORDER BY
  max DESC
```

## 使用 \_PARTITIONTIME 掃描特定範圍的擷取時間分區資料表

如要掃描特定範圍的擷取時間分區資料表，請搭配使用 `_PARTITIONTIME` 虛擬資料欄和 `_TABLE_SUFFIX` 虛擬資料欄。例如，下列查詢會掃描資料表 `my_dataset.mytable_id1` 中 2017 年 1 月 1 日的分區。

```
#standardSQL
SELECT
  field1,
  field2,
  field3
FROM
  `my_dataset.mytable_*`
WHERE
  _TABLE_SUFFIX = 'id1'
  AND _PARTITIONTIME = TIMESTAMP('2017-01-01')
```

## 查詢資料集中的所有資料表

如要掃描資料集中的所有資料表，可以使用空白前置字元和資料表萬用字元，這表示 `_TABLE_SUFFIX` 虛擬資料欄包含完整資料表名稱。舉例來說，下列 `FROM` 子句會掃描 GSOD 資料集中的所有資料表：

```
FROM
  `bigquery-public-data.noaa_gsod.*`
```

如果前置字元為空白，`_TABLE_SUFFIX` 虛擬資料欄會包含完整資料表名稱。舉例來說，以下查詢與前一個範例等效，可找出 1929 年到 1935 年間的最高溫度，但會在 `WHERE` 子句中使用完整資料表名稱：

```
#standardSQL
SELECT
  max,
  ROUND((max-32)*5/9,1) celsius,
  mo,
  da,
  year
FROM
  `bigquery-public-data.noaa_gsod.*`
WHERE
  max != 9999.9 # code for missing data
  AND _TABLE_SUFFIX BETWEEN 'gsod1929' and 'gsod1935'
ORDER BY
  max DESC
```

不過請注意，前置字元越長通常成效越佳。詳情請參閱[最佳做法](https://docs.cloud.google.com/bigquery/docs/wildcard-tables?hl=zh-tw#best_practices)部分。

## 查詢執行詳細資料

### 用於評估查詢作業的結構定義

如要執行使用萬用字元資料表的 GoogleSQL 查詢，BigQuery 會自動推論該資料表的結構定義。BigQuery 會使用與萬用字元相符的最新建立資料表結構定義，做為萬用字元資料表的結構定義。即使您使用 `WHERE` 子句中的 `_TABLE_SUFFIX` 虛擬資料欄，限制要從萬用字元資料表使用的資料表數量，BigQuery 仍會使用與萬用字元相符的最新建立資料表結構定義。

如果相符資料表中沒有推斷結構定義的資料欄，BigQuery 會在缺少該資料欄的資料表資料列中，為該資料欄傳回 `NULL` 值。

如果萬用字元查詢比對的資料表結構定義不一致，BigQuery 就會傳回錯誤。如果相符資料表的資料欄具有不同資料類型，或是所有相符資料表中沒有的資料欄無法假設為空值，就會發生這種情況。

## 最佳做法

* 相較於較短的前置字元，較長的前置字元通常成效較佳。舉例來說，下列查詢使用長前置字串 (`gsod200`)：

  ```
  #standardSQL
  SELECT
  max
  FROM
  `bigquery-public-data.noaa_gsod.gsod200*`
  WHERE
  max != 9999.9 # code for missing data
  AND _TABLE_SUFFIX BETWEEN '0' AND '1'
  ORDER BY
  max DESC
  ```

  以下查詢使用了空白前置字元，因此通常成效較差：

  ```
  #standardSQL
  SELECT
  max
  FROM
  `bigquery-public-data.noaa_gsod.*`
  WHERE
  max != 9999.9 # code for missing data
  AND _TABLE_SUFFIX BETWEEN 'gsod2000' AND 'gsod2001'
  ORDER BY
  max DESC
  ```
* 建議您使用分區而非分片，因為分區資料表的效能較佳。資源分割會降低效能，同時增加要管理的資料表數量。詳情請參閱「[分區與分片](https://docs.cloud.google.com/bigquery/docs/partitioned-tables?hl=zh-tw#dt_partition_shard)」。

如要瞭解在 BigQuery 中控管費用的最佳做法，請參閱「[在 BigQuery 中控管費用](https://docs.cloud.google.com/bigquery/docs/best-practices-costs?hl=zh-tw)」一文。

## 後續步驟

* 如要進一步瞭解 GoogleSQL，請參閱 [GoogleSQL 查詢參考資料](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-09 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-09 (世界標準時間)。"],[],[]]