* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [參考資料](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# SEARCH\_INDEX\_OPTIONS 檢視畫面

`INFORMATION_SCHEMA.SEARCH_INDEX_OPTIONS` 檢視表會針對資料集中的每個搜尋索引選項，分別列出一個相對應的資料列。

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

查詢 `INFORMATION_SCHEMA.SEARCH_INDEX_OPTIONS` 檢視表時，資料集中每個搜尋索引選項在查詢結果都會有一個資料列。

`INFORMATION_SCHEMA.SEARCH_INDEX_OPTIONS` 檢視表具有下列結構定義：

| 資料欄名稱 | 資料類型 | 值 |
| --- | --- | --- |
| `index_catalog` | `STRING` | 資料集所屬專案的名稱。 |
| `index_schema` | `STRING` | 包含索引的資料集名稱。 |
| `table_name` | `STRING` | 建立索引的基礎資料表名稱。 |
| `index_name` | `STRING` | 索引的名稱。 |
| `option_name` | `STRING` | 選項名稱，可以是下列其中一項：`analyzer`、`analyzer_options`、`data_types` 或 `default_index_column_granularity`。 |
| `option_type` | `STRING` | 選項類型。 |
| `option_value` | `STRING` | 選項的值。 |

**注意：** 如未指定搜尋索引選項，查詢會產生包含預設搜尋索引選項的資料列。無論 DDL 中是否指定 `analyzer` 和 `data_types` 選項，系統一律會在 `SEARCH_INDEX_OPTIONS` 檢視區塊中填入這些選項。如未指定，系統會分別產生預設的 `LOG_ANALYZER` 和 `["STRING"]` 值。只有在 `SEARCH_INDEX_OPTIONS` 中指定其他選項時，這些選項才會填入 `CREATE SEARCH INDEX DDL` 檢視畫面。

為確保穩定性，建議您在資訊結構定義查詢中明確列出資料欄，而非使用萬用字元 (`SELECT *`)。明確列出資料欄可避免基礎結構定義變更時，查詢中斷。

## 範圍和語法

對這個檢視表執行的查詢必須具有[資料集限定詞](https://docs.cloud.google.com/bigquery/docs/information-schema-intro?hl=zh-tw#syntax)。下表說明這個檢視畫面的區域範圍：

| 檢視表名稱 | 資源範圍 | 區域範圍 |
| --- | --- | --- |
| `[PROJECT_ID.]DATASET_ID.INFORMATION_SCHEMA.SEARCH_INDEX_OPTIONS` | 資料集層級 | 資料集位置 |

取代下列項目：

* 選用：`PROJECT_ID`：您的 Google Cloud 專案 ID。如未指定，系統會使用預設專案。
* `DATASET_ID`：資料集 ID。詳情請參閱「[資料集限定符](https://docs.cloud.google.com/bigquery/docs/information-schema-intro?hl=zh-tw#dataset_qualifier)」。

**示例**

```
-- Returns metadata for search index options in a single dataset.
SELECT * FROM myDataset.INFORMATION_SCHEMA.SEARCH_INDEX_OPTIONS;
```

## 範例

以下範例會為資料欄建立三個搜尋索引選項，然後從已建立索引的欄位中擷取這些選項：`table1`

```
CREATE SEARCH INDEX myIndex ON `mydataset.table1` (ALL COLUMNS) OPTIONS (
  analyzer = 'LOG_ANALYZER',
  analyzer_options = '{ "delimiters" : [".", "-"] }',
  data_types = ['STRING', 'INT64', 'TIMESTAMP']
);

SELECT index_name, option_name, option_type, option_value
FROM mydataset.INFORMATION_SCHEMA.SEARCH_INDEX_OPTIONS
WHERE table_name='table1';
```

結果大致如下：

```
+------------+------------------+---------------+----------------------------------+
| index_name |  option_name     | option_type   | option_value                     |
+------------+------------------+---------------+----------------------------------+
| myIndex    | analyzer         | STRING        | LOG_ANALYZER                     |
| myIndex    | analyzer_options | STRING        | { "delimiters": [".", "-"] }     |
| myIndex    | data_types       | ARRAY<STRING> | ["STRING", "INT64", "TIMESTAMP"] |
+------------+------------------+---------------+----------------------------------+
```

以下範例會為資料欄建立一個搜尋索引選項，然後從已建立索引的欄位中擷取這些選項。`table1`如果選項不存在，系統會產生預設選項：

```
CREATE SEARCH INDEX myIndex ON `mydataset.table1` (ALL COLUMNS) OPTIONS (
  analyzer = 'NO_OP_ANALYZER'
);

SELECT index_name, option_name, option_type, option_value
FROM mydataset.INFORMATION_SCHEMA.SEARCH_INDEX_OPTIONS
WHERE table_name='table1';
```

結果大致如下：

```
+------------+------------------+---------------+----------------+
| index_name |  option_name     | option_type   | option_value   |
+------------+------------------+---------------+----------------+
| myIndex    | analyzer         | STRING        | NO_OP_ANALYZER |
| myIndex    | data_types       | ARRAY<STRING> | ["STRING"]     |
+------------+------------------+---------------+----------------+
```

以下範例不會為 `table1` 的資料欄建立任何搜尋索引選項，然後從已建立索引的欄位中擷取預設選項：

```
CREATE SEARCH INDEX myIndex ON `mydataset.table1` (ALL COLUMNS);

SELECT index_name, option_name, option_type, option_value
FROM mydataset.INFORMATION_SCHEMA.SEARCH_INDEX_OPTIONS
WHERE table_name='table1';
```

結果大致如下：

```
+------------+------------------+---------------+----------------+
| index_name |  option_name     | option_type   | option_value   |
+------------+------------------+---------------+----------------+
| myIndex    | analyzer         | STRING        | LOG_ANALYZER   |
| myIndex    | data_types       | ARRAY<STRING> | ["STRING"]     |
+------------+------------------+---------------+----------------+
```




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-02 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-02 (世界標準時間)。"],[],[]]