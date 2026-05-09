Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [參考資料](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# VECTOR\_INDEX\_COLUMNS 檢視畫面

`INFORMATION_SCHEMA.VECTOR_INDEX_COLUMNS` 檢視表會針對資料集中每個資料表上經過向量索引的資料欄，分別列出一個相對應的資料列。

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

查詢 `INFORMATION_SCHEMA.VECTOR_INDEX_COLUMNS` 檢視表時，資料集中每個資料表的每個索引資料欄，在查詢結果中都會有一個相對應的資料列。

`INFORMATION_SCHEMA.VECTOR_INDEX_COLUMNS` 檢視表具有下列結構定義：

| 資料欄名稱 | 資料類型 | 值 |
| --- | --- | --- |
| `index_catalog` | `STRING` | 資料集所屬專案的名稱。 |
| `index_schema` | `STRING` | 包含向量索引的資料集名稱。 |
| `table_name` | `STRING` | 要建立向量索引的資料表名稱。 |
| `index_name` | `STRING` | 向量索引的名稱。 |
| `index_column_name` | `STRING` | 已建立索引的資料欄名稱。 |
| `index_field_path` | `STRING` | 展開索引欄位的完整路徑，開頭為欄名。欄位以半形句號分隔。 |

為確保穩定性，建議您在資訊結構定義查詢中明確列出資料欄，而非使用萬用字元 (`SELECT *`)。明確列出資料欄可避免基礎結構定義變更時，查詢中斷。

## 範圍和語法

對這個檢視表執行的查詢必須具有[資料集限定詞](https://docs.cloud.google.com/bigquery/docs/information-schema-intro?hl=zh-tw#syntax)。下表說明這個檢視畫面的區域範圍：

| 檢視表名稱 | 資源範圍 | 區域範圍 |
| --- | --- | --- |
| `[PROJECT_ID.]DATASET_ID.INFORMATION_SCHEMA.VECTOR_INDEX_COLUMNS` | 資料集層級 | 資料集位置 |

取代下列項目：

* 選用：`PROJECT_ID`：您的 Google Cloud 專案 ID。如未指定，系統會使用預設專案。
* `DATASET_ID`：資料集 ID。詳情請參閱「[資料集限定符](https://docs.cloud.google.com/bigquery/docs/information-schema-intro?hl=zh-tw#dataset_qualifier)」。**注意：**您必須使用[區域限定詞](https://docs.cloud.google.com/bigquery/docs/information-schema-intro?hl=zh-tw#region_qualifier)查詢 `INFORMATION_SCHEMA` 檢視畫面。查詢執行位置必須與 `INFORMATION_SCHEMA` 檢視區塊的區域相符。

**示例**

```
-- Returns metadata for vector indexes in a single dataset.
SELECT * FROM myDataset.INFORMATION_SCHEMA.VECTOR_INDEX_COLUMNS;
```

## 範例

下列查詢會擷取具有向量索引的資料欄相關資訊：

```
SELECT table_name, index_name, index_column_name, index_field_path
FROM my_project.dataset.INFORMATION_SCHEMA.VECTOR_INDEX_COLUMNS;
```

結果大致如下：

```
+------------+------------+-------------------+------------------+
| table_name | index_name | index_column_name | index_field_path |
+------------+------------+-------------------+------------------+
| table1     | indexa     | embeddings        | embeddings       |
| table2     | indexb     | vectors           | vectors          |
| table3     | indexc     | vectors           | vectors          |
+------------+------------+-------------------+------------------+
```




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-08 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-08 (世界標準時間)。"],[],[]]