Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [參考資料](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# SEARCH\_INDEXES 檢視畫面

`INFORMATION_SCHEMA.SEARCH_INDEXES` 檢視表會為資料集中的每個搜尋索引包含一個資料列。

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

查詢 `INFORMATION_SCHEMA.SEARCH_INDEXES` 檢視表時，資料集中每個搜尋索引在查詢結果都會有一個資料列。

`INFORMATION_SCHEMA.SEARCH_INDEXES` 檢視表具有下列結構定義：

| 資料欄名稱 | 資料類型 | 值 |
| --- | --- | --- |
| `index_catalog` | `STRING` | 資料集所屬專案的名稱。 |
| `index_schema` | `STRING` | 包含索引的資料集名稱。 |
| `table_name` | `STRING` | 建立索引的基礎資料表名稱。 |
| `index_name` | `STRING` | 索引的名稱。 |
| `index_status` | `STRING` | 索引的狀態：`ACTIVE`、`PENDING DISABLEMENT`、`TEMPORARILY DISABLED` 或 `PERMANENTLY DISABLED`。  * `ACTIVE` 表示索引可用或正在建立中。請參閱 `coverage_percentage`，查看索引建立進度。 * `PENDING DISABLEMENT` 表示建立索引的基礎資料表總大小超出貴機構的[限制](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#index_limits)，因此系統已將索引排入刪除佇列。處於這個狀態時，索引可用於搜尋查詢，且系統會向您收取搜尋索引儲存空間費用。 * `TEMPORARILY DISABLED` 表示建立索引的基礎資料表總大小超出貴機構的[限制](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#index_limits)，或是基礎索引資料表小於 10 GB。處於這個狀態時，索引不會用於搜尋查詢，您也不會因搜尋索引儲存空間而產生費用。 * `PERMANENTLY DISABLED` 表示基本資料表有不相容的結構定義變更，例如將索引資料欄的類型從 `STRING` 變更為 `INT64`。 |
| `creation_time` | `TIMESTAMP` | 索引的建立時間。 |
| `last_modification_time` | `TIMESTAMP` | 上次修改索引設定的時間。例如刪除已建立索引的資料欄。 |
| `last_refresh_time` | `TIMESTAMP` | 上次為表格資料建立索引的時間。`NULL` 值表示索引尚未提供。 |
| `disable_time` | `TIMESTAMP` | 索引狀態設為「`DISABLED`」的時間。如果索引狀態不是 `DISABLED`，值為 `NULL`。 |
| `disable_reason` | `STRING` | 索引停用的原因。如果索引狀態不是 `DISABLED`，請使用 `NULL`。 |
| `DDL` | `STRING` | 用於建立索引的 DDL 陳述式。 |
| `coverage_percentage` | `INTEGER` | 已建立索引的資料表資料約略百分比。0% 表示索引無法用於 `SEARCH` 查詢，即使部分資料已建立索引也一樣。 |
| `unindexed_row_count` | `INTEGER` | 尚未建立索引的基本資料表列數。 |
| `total_logical_bytes` | `INTEGER` | 索引的可計費邏輯位元組數。 |
| `total_storage_bytes` | `INTEGER` | 索引的可計費儲存空間位元組數。 |
| `analyzer` | `STRING` | 用於為搜尋索引產生權杖的[文字分析器](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/text-analysis?hl=zh-tw)。 |

為確保穩定性，建議您在資訊結構定義查詢中明確列出資料欄，而非使用萬用字元 (`SELECT *`)。明確列出資料欄可避免基礎結構定義變更時，查詢中斷。

## 範圍和語法

對這個檢視表執行的查詢必須具有[資料集限定詞](https://docs.cloud.google.com/bigquery/docs/information-schema-intro?hl=zh-tw#syntax)。下表說明這個檢視畫面的區域範圍：

| 檢視表名稱 | 資源範圍 | 區域範圍 |
| --- | --- | --- |
| `[PROJECT_ID.]DATASET_ID.INFORMATION_SCHEMA.SEARCH_INDEXES` | 資料集層級 | 資料集位置 |

取代下列項目：

* 選用：`PROJECT_ID`：您的 Google Cloud 專案 ID。如未指定，系統會使用預設專案。
* `DATASET_ID`：資料集 ID。詳情請參閱「[資料集限定符](https://docs.cloud.google.com/bigquery/docs/information-schema-intro?hl=zh-tw#dataset_qualifier)」。

**範例**

```
-- Returns metadata for search indexes in a single dataset.
SELECT * FROM myDataset.INFORMATION_SCHEMA.SEARCH_INDEXES;
```

## 範例

以下範例會顯示專案 `my_project` 中，資料集 `my_dataset` 內資料表的所有有效搜尋索引。包括名稱、用於建立這些項目的 DDL 陳述式、涵蓋率百分比和文字分析器。如果編入索引的基礎資料表小於 10 GB，系統就不會填入索引，此時 `coverage_percentage` 為 0。

```
SELECT table_name, index_name, ddl, coverage_percentage, analyzer
FROM my_project.my_dataset.INFORMATION_SCHEMA.SEARCH_INDEXES
WHERE index_status = 'ACTIVE';
```

結果應如下所示：

```
+-------------+-------------+--------------------------------------------------------------------------------------+---------------------+----------------+
| table_name  | index_name  | ddl                                                                                  | coverage_percentage | analyzer       |
+-------------+-------------+--------------------------------------------------------------------------------------+---------------------+----------------+
| small_table | names_index | CREATE SEARCH INDEX `names_index` ON `my_project.my_dataset.small_table`(names)      | 0                   | NO_OP_ANALYZER |
| large_table | logs_index  | CREATE SEARCH INDEX `logs_index` ON `my_project.my_dataset.large_table`(ALL COLUMNS) | 100                 | LOG_ANALYZER   |
+-------------+-------------+--------------------------------------------------------------------------------------+---------------------+----------------+
```

## 疑難排解

如要啟用這個檢視畫面，請在專案或機構中將 `enable_info_schema_storage` 的值設為 `TRUE`。如要進一步瞭解如何管理設定，請參閱「[管理設定](https://docs.cloud.google.com/bigquery/docs/default-configuration?hl=zh-tw)」。

如果尚未設定，您會看到下列錯誤訊息：

```
INFORMATION_SCHEMA.SEARCH_INDEXES hasn't been enabled for project <myproject>.
Consider using one of the following SQL statements to enable data collection:
ALTER PROJECT `<myproject>`
SET OPTIONS (`region-<region>.enable_info_schema_storage` = TRUE)

Or to enable for the entire organization:
ALTER ORGANIZATION
SET OPTIONS (`region-<region>.enable_info_schema_storage` = TRUE)

After enabling, please allow around 1 day for the complete historical data to
become available.
```

執行錯誤訊息中說明的 SQL 陳述式，啟用檢視畫面。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-16 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-16 (世界標準時間)。"],[],[]]