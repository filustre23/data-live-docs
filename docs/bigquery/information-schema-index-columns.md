Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [參考資料](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# SEARCH\_INDEX\_COLUMNS 檢視畫面

`INFORMATION_SCHEMA.SEARCH_INDEX_COLUMNS` 檢視表會針對資料集中每個資料表上經過搜尋索引的資料欄，分別列出一個相對應的資料列。

## 所需權限

如要查看[搜尋索引](https://docs.cloud.google.com/bigquery/docs/search-index?hl=zh-tw)中繼資料，您必須具備索引所在資料表的 `bigquery.tables.get` 或 `bigquery.tables.list` Identity and Access Management (IAM) 權限。下列每個預先定義的 IAM 角色都至少包含其中一項權限：

* `roles/bigquery.admin`
* `roles/bigquery.dataEditor`
* `roles/bigquery.dataOwner`
* `roles/bigquery.dataViewer`
* `roles/bigquery.metadataViewer`
* `roles/bigquery.user`

如要進一步瞭解 BigQuery 權限，請參閱「[使用 IAM 控管存取權](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)」。

## 結構定義

查詢 `INFORMATION_SCHEMA.SEARCH_INDEX_COLUMNS` 檢視表時，資料集中每個資料表的每個索引資料欄，在查詢結果中都會有一個相對應的資料列。

`INFORMATION_SCHEMA.SEARCH_INDEX_COLUMNS` 檢視表具有下列結構定義：

| 資料欄名稱 | 資料類型 | 值 |
| --- | --- | --- |
| `index_catalog` | `STRING` | 資料集所屬專案的名稱。 |
| `index_schema` | `STRING` | 包含索引的資料集名稱。 |
| `table_name` | `STRING` | 建立索引的基礎資料表名稱。 |
| `index_name` | `STRING` | 索引的名稱。 |
| `index_column_name` | `STRING` | 頂層索引資料欄的名稱。 |  |
| `index_field_path` | `STRING` | 展開索引欄位的完整路徑，開頭為欄名。欄位以半形句號分隔。 |

為確保穩定性，建議您在資訊結構定義查詢中明確列出資料欄，而非使用萬用字元 (`SELECT *`)。明確列出資料欄可避免基礎結構定義變更時，查詢中斷。

## 範圍和語法

對這個檢視表執行的查詢必須具有[資料集限定詞](https://docs.cloud.google.com/bigquery/docs/information-schema-intro?hl=zh-tw#syntax)。下表說明這個檢視畫面的區域範圍：

| 檢視表名稱 | 資源範圍 | 區域範圍 |
| --- | --- | --- |
| `[PROJECT_ID.]DATASET_ID.INFORMATION_SCHEMA.SEARCH_INDEX_COLUMNS` | 資料集層級 | 資料集位置 |

取代下列項目：

* 選用：`PROJECT_ID`：專案 ID。 Google Cloud 如未指定，系統會使用預設專案。
* `DATASET_ID`：資料集的 ID。詳情請參閱「[資料集限定符](https://docs.cloud.google.com/bigquery/docs/information-schema-intro?hl=zh-tw#dataset_qualifier)」。

**範例**

```
-- Returns metadata for search indexes in a single dataset.
SELECT * FROM myDataset.INFORMATION_SCHEMA.SEARCH_INDEX_COLUMNS;
```

## 範例

以下範例會在 `my_table` 的所有資料欄上建立搜尋索引。

```
CREATE TABLE dataset.my_table(
  a STRING,
  b INT64,
  c STRUCT <d INT64,
            e ARRAY<STRING>,
            f STRUCT<g STRING, h INT64>>) AS
SELECT 'hello' AS a, 10 AS b, (20, ['x', 'y'], ('z', 30)) AS c;

CREATE SEARCH INDEX my_index
ON dataset.my_table(ALL COLUMNS);
```

下列查詢會擷取已建立索引的欄位資訊。
`index_field_path` 表示資料欄的哪個欄位已建立索引。只有在 `STRUCT` 的情況下，這與 `index_column_name` 不同，因為系統會提供已編入索引欄位的完整路徑。在這個範例中，資料欄 `c` 包含 `ARRAY<STRING>` 欄位 `e` 和另一個名為 `STRUCT` 的欄位 `f`，其中包含 `STRING` 欄位 `g`，每個欄位都會建立索引。

```
SELECT table_name, index_name, index_column_name, index_field_path
FROM my_project.dataset.INFORMATION_SCHEMA.SEARCH_INDEX_COLUMNS
```

結果大致如下：

```
+------------+------------+-------------------+------------------+
| table_name | index_name | index_column_name | index_field_path |
+------------+------------+-------------------+------------------+
| my_table   | my_index   | a                 | a                |
| my_table   | my_index   | c                 | c.e              |
| my_table   | my_index   | c                 | c.f.g            |
+------------+------------+-------------------+------------------+
```

下列查詢會將 `INFORMATION_SCHEMA.SEARCH_INDEX_COLUMNS` 檢視區塊與 `INFORMATION_SCHEMA.SEARCH_INDEXES` 和 `INFORMATION_SCHEMA.COLUMNS` 檢視區塊聯結，以納入搜尋索引狀態和每個資料欄的資料類型：

```
SELECT
  index_columns_view.index_catalog AS project_name,
  index_columns_view.index_SCHEMA AS dataset_name,
  indexes_view.TABLE_NAME AS table_name,
  indexes_view.INDEX_NAME AS index_name,
  indexes_view.INDEX_STATUS AS status,
  index_columns_view.INDEX_COLUMN_NAME AS column_name,
  index_columns_view.INDEX_FIELD_PATH AS field_path,
  columns_view.DATA_TYPE AS data_type
FROM
  mydataset.INFORMATION_SCHEMA.SEARCH_INDEXES indexes_view
INNER JOIN
  mydataset.INFORMATION_SCHEMA.SEARCH_INDEX_COLUMNS index_columns_view
  ON
    indexes_view.TABLE_NAME = index_columns_view.TABLE_NAME
    AND indexes_view.INDEX_NAME = index_columns_view.INDEX_NAME
LEFT OUTER JOIN
  mydataset.INFORMATION_SCHEMA.COLUMNS columns_view
  ON
    indexes_view.INDEX_CATALOG = columns_view.TABLE_CATALOG
    AND indexes_view.INDEX_SCHEMA = columns_view.TABLE_SCHEMA
    AND index_columns_view.TABLE_NAME = columns_view.TABLE_NAME
    AND index_columns_view.INDEX_COLUMN_NAME = columns_view.COLUMN_NAME
ORDER BY
  project_name,
  dataset_name,
  table_name,
  column_name;
```

結果大致如下：

```
+------------+------------+----------+------------+--------+-------------+------------+---------------------------------------------------------------+
| project    | dataset    | table    | index_name | status | column_name | field_path | data_type                                                     |
+------------+------------+----------+------------+--------+-------------+------------+---------------------------------------------------------------+
| my_project | my_dataset | my_table | my_index   | ACTIVE | a           | a          | STRING                                                        |
| my_project | my_dataset | my_table | my_index   | ACTIVE | c           | c.e        | STRUCT<d INT64, e ARRAY<STRING>, f STRUCT<g STRING, h INT64>> |
| my_project | my_dataset | my_table | my_index   | ACTIVE | c           | c.f.g      | STRUCT<d INT64, e ARRAY<STRING>, f STRUCT<g STRING, h INT64>> |
+------------+------------+----------+------------+--------+-------------+------------+---------------------------------------------------------------+
```




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-08 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-08 (世界標準時間)。"],[],[]]