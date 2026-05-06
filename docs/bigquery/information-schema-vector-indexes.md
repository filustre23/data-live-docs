Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [參考資料](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# VECTOR\_INDEXES 檢視畫面

`INFORMATION_SCHEMA.VECTOR_INDEXES` 檢視表中的每個資料列，代表資料集中的一個向量索引。

## 所需權限

如要查看[向量索引](https://docs.cloud.google.com/bigquery/docs/vector-index?hl=zh-tw)中繼資料，您必須具備索引資料表的 `bigquery.tables.get` 或 `bigquery.tables.list` 身分與存取權管理 (IAM) 權限。下列每個預先定義的 IAM 角色都至少包含其中一項權限：

* `roles/bigquery.admin`
* `roles/bigquery.dataEditor`
* `roles/bigquery.dataOwner`
* `roles/bigquery.dataViewer`
* `roles/bigquery.metadataViewer`
* `roles/bigquery.user`

如要進一步瞭解 BigQuery 權限，請參閱「[使用 IAM 控管存取權](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)」。

## 結構定義

查詢 `INFORMATION_SCHEMA.VECTOR_INDEXES` 檢視表時，資料集中每個向量索引在查詢結果都會有一個資料列。

`INFORMATION_SCHEMA.VECTOR_INDEXES` 檢視表具有下列結構定義：

| 資料欄名稱 | 資料類型 | 值 |
| --- | --- | --- |
| `index_catalog` | `STRING` | 資料集所屬專案的名稱。 |
| `index_schema` | `STRING` | 包含索引的資料集名稱。 |
| `table_name` | `STRING` | 要建立索引的資料表名稱。 |
| `index_name` | `STRING` | 向量索引的名稱。 |
| `index_status` | `STRING` | 索引的狀態：`ACTIVE`、`PENDING DISABLEMENT`、`TEMPORARILY DISABLED` 或 `PERMANENTLY DISABLED`。  * `ACTIVE` 表示索引可用或正在建立中。請參閱 `coverage_percentage`，查看索引建立進度。 * `PENDING DISABLEMENT` 表示建立索引的資料表總大小超出貴機構的[限制](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#index_limits)，系統已將索引排入刪除佇列。處於這個狀態時，索引可用於向量搜尋查詢，且您需要支付向量索引儲存空間費用。 * `TEMPORARILY DISABLED` 表示已建立索引的資料表總大小超出貴機構的[限制](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#index_limits)，或是已建立索引的資料表小於 10 MB。處於這個狀態時，向量搜尋查詢不會使用索引，且您不必支付向量索引儲存空間的費用。 * `PERMANENTLY DISABLED` 表示索引資料表有不相容的結構定義變更。 |
| `creation_time` | `TIMESTAMP` | 索引的建立時間。 |
| `last_modification_time` | `TIMESTAMP` | 上次修改索引設定的時間。例如刪除已建立索引的資料欄。 |
| `last_refresh_time` | `TIMESTAMP` | 上次為表格資料建立索引的時間。`NULL` 值表示索引尚未提供。 |
| `disable_time` | `TIMESTAMP` | 索引狀態設為 `DISABLED` 的時間。如果索引狀態不是 `DISABLED`，值為 `NULL`。 |
| `disable_reason` | `STRING` | 索引停用的原因。如果索引狀態不是 `DISABLED`，則為 `NULL`。 |
| `DDL` | `STRING` | 用於建立索引的資料定義語言 (DDL) 陳述式。 |
| `coverage_percentage` | `INTEGER` | 已建立索引的資料表資料約略百分比。 0% 代表索引無法用於 `VECTOR_SEARCH` 查詢，即使部分資料已建立索引也一樣。 |
| `unindexed_row_count` | `INTEGER` | 資料表中未建立索引的資料列數。 |
| `total_logical_bytes` | `INTEGER` | 索引的可計費邏輯位元組數。 |
| `total_storage_bytes` | `INTEGER` | 索引的可計費儲存空間位元組數。 |
| `last_index_alteration_info` | `RECORD` | 最新使用者觸發的索引變更詳細資料，包含下列欄位：  * `status`：表示變更狀態的 `STRING` 值。可能的值為 `NULL` (完成)、`IN_PROGRESS` 和 `FAILED`。 * `message`：包含 `FAILED` 狀態詳細資料的 `STRUCT` 欄位，格式為 [ErrorProto](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/ErrorProto?hl=zh-tw)。其他狀態的值為 `NULL`。 * `new_coverage_percentage`：`INT64` 值，其中包含已為變更建立索引的資料表資料概略百分比。 * `start_time`：啟動變更的時間戳記。 * `end_time`：變更進入 `FAILED` 狀態的時間戳記。 * `ddl`：用於變更索引的資料定義語言 (DDL) 陳述式。 |
| `last_model_build_time` | `TIMESTAMP` | 上次建立索引模型的時間。 |

為確保穩定性，建議您在資訊結構定義查詢中明確列出資料欄，而非使用萬用字元 (`SELECT *`)。明確列出資料欄可避免基礎結構定義變更時，查詢中斷。

## 範圍和語法

對這個檢視表執行的查詢必須具有[資料集限定詞](https://docs.cloud.google.com/bigquery/docs/information-schema-intro?hl=zh-tw#syntax)。下表說明這個檢視畫面的區域範圍：

| 檢視表名稱 | 資源範圍 | 區域範圍 |
| --- | --- | --- |
| `[PROJECT_ID.]DATASET_ID.INFORMATION_SCHEMA.VECTOR_INDEXES` | 資料集層級 | 資料集位置 |

取代下列項目：

* 選用：`PROJECT_ID`：您的 Google Cloud 專案 ID。如未指定，系統會使用預設專案。
* `DATASET_ID`：資料集 ID。詳情請參閱「[資料集限定符](https://docs.cloud.google.com/bigquery/docs/information-schema-intro?hl=zh-tw#dataset_qualifier)」。**注意：**您必須使用[區域限定詞](https://docs.cloud.google.com/bigquery/docs/information-schema-intro?hl=zh-tw#region_qualifier)查詢 `INFORMATION_SCHEMA` 檢視畫面。查詢執行位置必須與 `INFORMATION_SCHEMA` 檢視區塊的區域相符。

**範例**

```
-- Returns metadata for vector indexes in a single dataset.
SELECT * FROM myDataset.INFORMATION_SCHEMA.VECTOR_INDEXES;
```

## 範例

以下範例會顯示專案 `my_project` 中，資料集 `my_dataset` 內資料表的所有有效向量索引。包括名稱、用於建立這些物件的 DDL 陳述式，以及涵蓋範圍百分比。如果編入索引的基礎資料表小於 10 MB，系統就不會填入索引，此時 `coverage_percentage` 值為 0。

```
SELECT table_name, index_name, ddl, coverage_percentage
FROM my_project.my_dataset.INFORMATION_SCHEMA.VECTOR_INDEXES
WHERE index_status = 'ACTIVE';
```

結果大致如下：

```
+------------+------------+-------------------------------------------------------------------------------------------------+---------------------+
| table_name | index_name | ddl                                                                                             | coverage_percentage |
+------------+------------+-------------------------------------------------------------------------------------------------+---------------------+
| table1     | indexa     | CREATE VECTOR INDEX `indexa` ON `my_project.my_dataset.table1`(embeddings)                      | 100                 |
|            |            | OPTIONS (distance_type = 'EUCLIDEAN', index_type = 'IVF', ivf_options = '{"num_lists": 100}')   |                     |
+------------+------------+-------------------------------------------------------------------------------------------------+---------------------+
| table2     | indexb     | CREATE VECTOR INDEX `indexb` ON `my_project.my_dataset.table2`(vectors)                         | 42                  |
|            |            | OPTIONS (distance_type = 'COSINE', index_type = 'IVF', ivf_options = '{"num_lists": 500}')      |                     |
+------------+------------+-------------------------------------------------------------------------------------------------+---------------------+
| table3     | indexc     | CREATE VECTOR INDEX `indexc` ON `my_project.my_dataset.table3`(vectors)                         | 98                  |
|            |            | OPTIONS (distance_type = 'DOT_PRODUCT', index_type = 'TREE_AH',                                 |                     |
|            |            |          tree_ah_options = '{"leaf_node_embedding_count": 1000, "normalization_type": "NONE"}') |                     |
+------------+------------+-------------------------------------------------------------------------------------------------+---------------------+
```




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-06 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-06 (世界標準時間)。"],[],[]]