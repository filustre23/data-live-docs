Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [參考資料](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# VECTOR\_INDEX\_OPTIONS 檢視畫面

`INFORMATION_SCHEMA.VECTOR_INDEX_OPTIONS` 檢視表中的每個資料列，代表資料集中的一個向量索引選項。

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

查詢 `INFORMATION_SCHEMA.VECTOR_INDEX_OPTIONS` 檢視表時，資料集中每個向量索引選項在查詢結果中都會有一個資料列。

`INFORMATION_SCHEMA.VECTOR_INDEX_OPTIONS` 檢視表具有下列結構定義：

| 資料欄名稱 | 資料類型 | 值 |
| --- | --- | --- |
| `index_catalog` | `STRING` | 資料集所屬專案的名稱。 |
| `index_schema` | `STRING` | 包含向量索引的資料集名稱。 |
| `table_name` | `STRING` | 要建立向量索引的資料表名稱。 |
| `index_name` | `STRING` | 向量索引的名稱。 |
| `option_name` | `STRING` | 用於資料定義語言 (DDL) 陳述式中的選項名稱，用來建立向量索引。 |
| `option_type` | `STRING` | 選項資料類型。 |
| `option_value` | `STRING` | 選項值。 |

為確保穩定性，建議您在資訊結構定義查詢中明確列出資料欄，而非使用萬用字元 (`SELECT *`)。明確列出資料欄可避免基礎結構定義變更時，查詢中斷。

## 範圍和語法

對這個檢視表執行的查詢必須具有[資料集限定詞](https://docs.cloud.google.com/bigquery/docs/information-schema-intro?hl=zh-tw#syntax)。下表說明這個檢視畫面的區域範圍：

| 檢視表名稱 | 資源範圍 | 區域範圍 |
| --- | --- | --- |
| `[PROJECT_ID.]DATASET_ID.INFORMATION_SCHEMA.VECTOR_INDEX_OPTIONS` | 資料集層級 | 資料集位置 |

取代下列項目：

* 選用：`PROJECT_ID`：您的 Google Cloud 專案 ID。如未指定，系統會使用預設專案。
* `DATASET_ID`：資料集 ID。詳情請參閱「[資料集限定符](https://docs.cloud.google.com/bigquery/docs/information-schema-intro?hl=zh-tw#dataset_qualifier)」。**注意：**您必須使用[區域限定詞](https://docs.cloud.google.com/bigquery/docs/information-schema-intro?hl=zh-tw#region_qualifier)查詢 `INFORMATION_SCHEMA` 檢視畫面。查詢執行位置必須與 `INFORMATION_SCHEMA` 檢視區塊的區域相符。

**示例**

```
-- Returns metadata for vector indexes in a single dataset.
SELECT * FROM myDataset.INFORMATION_SCHEMA.VECTOR_INDEX_OPTIONS;
```

## 範例

以下查詢會擷取向量索引選項的相關資訊：

```
SELECT table_name, index_name, option_name, option_type, option_value
FROM my_project.dataset.INFORMATION_SCHEMA.VECTOR_INDEX_OPTIONS;
```

結果大致如下：

```
+------------+------------+------------------+------------------+-------------------------------------------------------------------+
| table_name | index_name | option_name      | option_type      | option_value                                                      |
+------------+------------+------------------+------------------+-------------------------------------------------------------------+
| table1     | indexa     | index_type       | STRING           | IVF                                                               |
| table1     | indexa     | distance_type    | STRING           | EUCLIDEAN                                                         |
| table1     | indexa     | ivf_options      | STRING           | {"num_lists": 100}                                                |
| table2     | indexb     | index_type       | STRING           | IVF                                                               |
| table2     | indexb     | distance_type    | STRING           | COSINE                                                            |
| table2     | indexb     | ivf_options      | STRING           | {"num_lists": 500}                                                |
| table3     | indexc     | index_type       | STRING           | TREE_AH                                                           |
| table3     | indexc     | distance_type    | STRING           | DOT_PRODUCT                                                       |
| table3     | indexc     | tree_ah_options  | STRING           | {"leaf_node_embedding_count": 1000, "normalization_type": "NONE"} |
+------------+------------+------------------+------------------+-------------------------------------------------------------------+
```




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-09 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-09 (世界標準時間)。"],[],[]]