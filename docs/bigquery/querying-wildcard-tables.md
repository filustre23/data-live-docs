Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 使用 Wildcard 資料表查詢多個資料表

**注意：** Wildcard 資料表有許多[限制](#limitations)，效能不如採用[分區](https://docs.cloud.google.com/bigquery/docs/partitioned-tables?hl=zh-tw)和[分群](https://docs.cloud.google.com/bigquery/docs/clustered-tables?hl=zh-tw)的一般 BigQuery 資料表。最佳做法是盡可能使用分區或分群資料表。

BigQuery 的 Wildcard 資料表可讓您查詢多個名稱相似且結構定義相容的資料表。Wildcard 資料表代表與萬用字元運算式相符的所有資料表聯集。因此，您可以分析分散的資料集，不必編寫包含 `UNION ALL` 陳述式的冗長複雜查詢。

## 限制

Wildcard 資料表查詢有下列限制。

* Wildcard 資料表僅適用於 GoogleSQL。如需舊版 SQL 的同等功能，請參閱「[表格萬用字元函式](https://docs.cloud.google.com/bigquery/query-reference?hl=zh-tw#tablewildcardfunctions)」。
* Wildcard 資料表功能不支援檢視表。如果 Wildcard 資料表與資料集中的任何檢視表相符，即使查詢包含 `_TABLE_SUFFIX` 虛擬資料欄的 `WHERE` 子句來篩除檢視表，查詢也會傳回錯誤。
* 無論是否已勾選「Use Cached Results」(使用快取結果)，目前使用萬用字元查詢多個資料表時，不支援快取結果。如果多次執行相同的萬用字元查詢，系統會針對每次查詢向您收費。
* Wildcard 資料表僅支援內建 BigQuery 儲存空間。您無法使用萬用字元查詢[外部資料表](https://docs.cloud.google.com/bigquery/external-data-sources?hl=zh-tw)或[檢視表](https://docs.cloud.google.com/bigquery/docs/views?hl=zh-tw)。
* 如果資料表的分區不相容，或同時包含分區和非分區資料表，則無法使用萬用字元查詢。查詢的資料表也必須具有相同的分群規格。
* Wildcard 資料表可與分區資料表搭配使用，且支援分區剪除和叢集剪除。不過，如果資料表已分群但未分區，使用萬用字元就無法充分發揮分群修剪功能。
* 含有[資料操縱語言](https://docs.cloud.google.com/bigquery/docs/data-manipulation-language?hl=zh-tw) (DML) 陳述式的查詢，無法使用萬用字元資料表做為查詢目標。舉例來說，Wildcard 資料表可用於 `UPDATE` 查詢的 `FROM` 子句，但無法做為 `UPDATE` 作業的目標。
* 如果 `_TABLE_SUFFIX` 或 `_PARTITIONTIME` 虛擬資料欄的篩選器包含 JavaScript user-defined function，則不會限制 Wildcard 資料表中掃描的資料表數量。
* 萬用字元查詢不支援受客戶自行管理的加密金鑰 (CMEK) 保護的資料表。
* 萬用字元查詢中參照的所有資料表，都必須具有完全相同的[標記](https://docs.cloud.google.com/bigquery/docs/tags?hl=zh-tw)鍵和值組合。
* 如果單一掃描資料表的結構定義不相符 (即同名資料欄的類型不同)，查詢就會失敗，並顯示「Cannot read field of type X as Y Field: column\_name」錯誤。即使使用等號運算子 `=`，系統也會比對所有資料表。舉例來說，在下列查詢中，系統也會掃描 `my_dataset.my_table_03_backup` 資料表。因此，查詢可能會因結構定義不相符而失敗。不過，如果結構定義沒有不相符，結果就會如預期，僅來自資料表 `my_dataset.my_table_03`。

  ```
  SELECT *
  FROM my_project.my_dataset.my_table_*
  WHERE _TABLE_SUFFIX = '03'
  ```
* BI Engine 不支援 Wildcard 資料表。
* 如果資料表具有彈性資料欄名稱或重新命名的資料欄，則不支援 Wildcard 資料表。如要避開這項限制，請從查詢中排除受影響的資料欄，或使用 `_TABLE_SUFFIX` 虛擬資料欄篩選資料表。

## 事前準備

* 確認您使用的是 GoogleSQL。詳情請參閱「[切換 SQL 方言](https://docs.cloud.google.com/bigquery/sql-reference/enabling-standard-sql?hl=zh-tw)」。
* 如果您使用的是舊版 SQL，請參閱[表格萬用字元函式](https://docs.cloud.google.com/bigquery/query-reference?hl=zh-tw#tablewildcardfunctions)一文。
* 本頁面中許多範例使用了美國國家海洋暨大氣總署 (NOAA) 的公開資料集。如要進一步瞭解這些資料，請參閱 [NOAA 全球每日地面天氣摘要資料](https://console.cloud.google.com/bigquery?p=bigquery-public-data&%3Bd=noaa_gsod&%3Bpage=dataset&hl=zh-tw)。

## 萬用字元資料表的使用時機

如果資料集包含多個名稱相似且架構相容的 Wildcard 資料表，Wildcard 資料表就非常實用。一般來說，這類資料集所包含的每一個資料表都分別代表單日、單月或單一年度的資料。舉例來說，BigQuery 所託管的公開資料集 [NOAA 全球每日地面天氣摘要資料](https://console.cloud.google.com/bigquery?p=bigquery-public-data&%3Bd=noaa_gsod&%3Bpage=dataset&hl=zh-tw)包含許多資料表，分別代表 1929 年至今每一年的資料。

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

使用 Wildcard 資料表的相同查詢則簡潔得多：

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

Wildcard 資料表僅支援內建的 BigQuery 儲存空間。查詢[外部資料表](https://docs.cloud.google.com/bigquery/external-data-sources?hl=zh-tw)或[檢視表](https://docs.cloud.google.com/bigquery/docs/views?hl=zh-tw)時，無法使用萬用字元。

## Wildcard 資料表語法

Wildcard 資料表語法：

```
SELECT
FROM
  `<project-id>.<dataset-id>.<table-prefix>*`
WHERE
  bool_expression
```

<project-id>
:   Cloud Platform 專案 ID。如果使用預設專案 ID，則可省略。

<dataset-id>
:   BigQuery 資料集 ID。

<table-prefix>
:   萬用字元比對的所有資料表共用的字串。資料表前置字串可省略，如果省略資料表前置字串，則會比對資料集中的所有資料表。

\* (萬用字元)
:   萬用字元「\*」代表資料表名稱中的一或多個字元。萬用字元只能出現在 Wildcard 資料表名稱的最後一個字元。

使用 Wildcard 資料表的查詢，支援 `WHERE` 子句中的 `_TABLE_SUFFIX` 虛擬資料欄。這個資料欄包含與萬用字元相符的值，因此查詢可以篩選要存取的資料表。舉例來說，下列 `WHERE` 子句會使用[比較運算子](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/operators?hl=zh-tw#comparison_operators)篩選相符的資料表：

```
WHERE
  _TABLE_SUFFIX BETWEEN '29' AND '40'

WHERE
  _TABLE_SUFFIX = '1929'

WHERE
  _TABLE_SUFFIX < '1941'
```

如要進一步瞭解 `_TABLE_SUFFIX` 虛擬資料欄，請參閱「[使用 \_TABLE\_SUFFIX 篩選所選資料表](https://docs.cloud.google.com/bigquery/docs/querying-wildcard-tables?hl=zh-tw#filter_selected_tables_using_table_suffix)」。

### 在倒引號中以萬用字元括住資料表名稱

Wildcard 資料表名稱包含特殊字元 (\*)，因此必須用反引號 (`) 括住。舉例來說，以下查詢使用了倒引號，屬於有效的查詢：

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

## 使用 Wildcard 資料表查詢資料表

Wildcard 資料表可讓您精簡地查詢多個資料表。舉例來說，BigQuery 代管的公開資料集 [NOAA Global Surface Summary of the Day Weather Data](https://console.cloud.google.com/bigquery?p=bigquery-public-data&%3Bd=noaa_gsod&%3Bpage=dataset&hl=zh-tw) 包含 1929 年至今每年的資料表，這些資料表都共用前置字串 `gsod`，後面接著四位數年份。資料表名稱為 `gsod1929`、`gsod1930`、`gsod1931` 等。

如要查詢共用相同前置字元的一組資料表，請在 `FROM` 陳述式中的資料表前置字元後方，使用資料表萬用字元符號 (\*)。舉例來說，以下查詢會找出 1940 年代期間所回報的最高氣溫：

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

如要限制查詢，使其僅掃描一組指定的資料表，請在 `WHERE` 子句中使用 `_TABLE_SUFFIX` 虛擬資料欄，並將條件設為常數運算式。

`_TABLE_SUFFIX` 虛擬資料欄包含與表格萬用字元相符的值。舉例來說，先前的範例查詢會掃描 1940 年代的所有資料表，並使用表格萬用字元代表年份的最後一位數：

```
FROM
  `bigquery-public-data.noaa_gsod.gsod194*`
```

對應的 `_TABLE_SUFFIX` 虛擬資料欄包含 `0` 到 `9` 範圍內的值，代表 `gsod1940` 到 `gsod1949` 資料表。這些 `_TABLE_SUFFIX` 值可用於 `WHERE` 子句，篩選特定資料表。

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

使用 `_TABLE_SUFFIX` 可大幅減少掃描的位元組數，進而降低執行查詢的費用。

不過，如果 `_TABLE_SUFFIX` 的篩選器包含不含常數運算式的條件，就不會限制 Wildcard 資料表中掃描的資料表數量。舉例來說，下列查詢不會限制萬用字元資料表 `bigquery-public-data.noaa_gsod.gsod19*` 掃描的資料表，因為篩選器使用 `table_id` 資料欄的動態值：

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

再舉一個例子，下列查詢會根據第一個篩選條件 `_TABLE_SUFFIX BETWEEN '40' and '60'` 限制掃描，因為這是常數運算式。不過，下列查詢不會根據第二個篩選條件 `_TABLE_SUFFIX = (SELECT SUBSTR(MAX(table_name), LENGTH('gsod19')
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

如要解決這個問題，您可以改為執行兩項不同的查詢，例如：

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

這些查詢範例使用 `INFORMATION_SCHEMA.TABLES` 檢視表。如要進一步瞭解 `INFORMATION_SCHEMA` 資料表，請參閱「[使用 INFORMATION\_SCHEMA 取得資料表中繼資料](https://docs.cloud.google.com/bigquery/docs/information-schema-tables?hl=zh-tw)」。

## 使用 \_TABLE\_SUFFIX 掃描特定範圍的資料表

如要掃描一系列資料表，請使用 `_TABLE_SUFFIX` 虛擬資料欄和 `BETWEEN` 子句。舉例來說，如要找出 1929 年至 1935 年 (含) 之間回報的最高溫度，請使用表格萬用字元代表年份的最後兩位數：

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

如要掃描一系列擷取時間分區資料表，請搭配使用 `_PARTITIONTIME` 虛擬資料欄和 `_TABLE_SUFFIX` 虛擬資料欄。舉例來說，下列查詢會掃描 `my_dataset.mytable_id1` 資料表中 2017 年 1 月 1 日的分區。

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

如要掃描資料集中的所有資料表，可以使用空白前置字串和資料表萬用字元，這表示 `_TABLE_SUFFIX` 虛擬資料欄包含完整資料表名稱。舉例來說，下列 `FROM` 子句會掃描 GSOD 資料集中的所有資料表：

```
FROM
  `bigquery-public-data.noaa_gsod.*`
```

如果前置字串空白，`_TABLE_SUFFIX` 虛擬資料欄會包含完整資料表名稱。舉例來說，下列查詢與前一個範例相同，都是找出 1929 年至 1935 年之間的最高溫度，但在 `WHERE` 子句中使用完整資料表名稱：

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

為了執行使用 Wildcard 資料表的 GoogleSQL 查詢，BigQuery 會自動推論該資料表的結構定義。BigQuery 會使用最近建立且符合萬用字元的資料表結構定義，做為 Wildcard 資料表的結構定義。即使您使用 `WHERE` 子句中的 `_TABLE_SUFFIX` 虛擬資料欄，限制要從 Wildcard 資料表使用的資料表數量，BigQuery 仍會使用與萬用字元相符、最近建立的資料表結構定義。

如果推論結構定義中的資料欄不存在於相符的資料表中，BigQuery 會在缺少該資料欄的資料表資料列中，為該資料欄傳回 `NULL` 值。

如果萬用字元查詢比對出的資料表結構定義不一致，BigQuery 就會傳回錯誤。如果相符資料表的資料欄具有不同的資料類型，或並非所有相符資料表都存在的資料欄無法假設為空值，就會發生這種情況。

## 最佳做法

* 相較於較短的前置字元，較長的前置字元通常成效較佳。例如，下列查詢使用長前置字元 (`gsod200`)：

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
* 建議您使用分區，而非資料分割，因為分區資料表的效能較佳。資料分割會降低效能，並建立更多資料表來管理。詳情請參閱「[分區與 sharding](https://docs.cloud.google.com/bigquery/docs/partitioned-tables?hl=zh-tw#dt_partition_shard)」。

如要瞭解在 BigQuery 控管費用的最佳做法，請參閱「[在 BigQuery 控管費用](https://docs.cloud.google.com/bigquery/docs/best-practices-costs?hl=zh-tw)」

## 後續步驟

* 如要進一步瞭解 GoogleSQL，請參閱 [GoogleSQL 查詢參考資料](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-10-30 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-10-30 (世界標準時間)。"],[],[]]