* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [參考資料](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 「參數」檢視畫面

`INFORMATION_SCHEMA.PARAMETERS` 檢視表會為資料集中每個常式的每個參數提供一個資料列。

## 所需權限

如要查詢 `INFORMATION_SCHEMA.PARAMETERS` 檢視畫面，您必須具備下列 Identity and Access Management (IAM) 權限：

* `bigquery.routines.get`
* `bigquery.routines.list`

下列每個預先定義的 IAM 角色都包含取得例行中繼資料所需的權限：

* `roles/bigquery.admin`
* `roles/bigquery.metadataViewer`
* `roles/bigquery.dataViewer`

如要進一步瞭解 BigQuery 權限，請參閱「[使用 IAM 控管存取權](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)」。

## 結構定義

查詢 `INFORMATION_SCHEMA.PARAMETERS` 檢視表時，資料集中每個處理常式的每個參數在查詢結果中都會有一個資料列。

`INFORMATION_SCHEMA.PARAMETERS` 檢視表具有下列結構定義：

| 資料欄名稱 | 資料類型 | 值 |
| --- | --- | --- |
| `specific_catalog` | `STRING` | 其中包含定義參數之處理常式的資料集，其所屬專案的名稱 |
| `specific_schema` | `STRING` | 包含定義參數之處理常式的資料集名稱 |
| `specific_name` | `STRING` | 定義參數之處理常式的名稱 |
| `ordinal_position` | `STRING` | 從 1 開始的參數位置，或傳回值 0 |
| `parameter_mode` | `STRING` | 參數的模式，`IN`、`OUT`、`INOUT` 或 `NULL` |
| `is_result` | `STRING` | 參數是否為函式的結果，值為 `YES` 或 `NO` |
| `parameter_name` | `STRING` | 參數的名稱 |
| `data_type` | `STRING` | 如果定義為任何類型，參數類型將會是 `ANY TYPE` |
| `parameter_default` | `STRING` | 以 SQL 常值表示的參數預設值，一律為 `NULL` |
| `is_aggregate` | `STRING` | 無論是否為匯總參數，一律為 `NULL` |

為確保穩定性，建議您在資訊結構定義查詢中明確列出資料欄，而非使用萬用字元 (`SELECT *`)。明確列出資料欄可避免基礎結構定義變更時，查詢中斷。

## 範圍和語法

對這個檢視表執行的查詢必須包含資料集或區域限定詞。詳情請參閱「[語法](https://docs.cloud.google.com/bigquery/docs/information-schema-intro?hl=zh-tw#syntax)」。下表說明這個檢視畫面的區域和資源範圍：

| 檢視表名稱 | 資源範圍 | 區域範圍 |
| --- | --- | --- |
| `` [PROJECT_ID.]`region-REGION`.INFORMATION_SCHEMA.PARAMETERS `` | 專案層級 | `REGION` |
| `[PROJECT_ID.]DATASET_ID.INFORMATION_SCHEMA.PARAMETERS` | 資料集層級 | 資料集位置 |

取代下列項目：

* 選用：`PROJECT_ID`：您的 Google Cloud 專案 ID。如未指定，系統會使用預設專案。
* `REGION`：任何[資料集區域名稱](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)。
  例如：`` `region-us` ``。
* `DATASET_ID`：資料集 ID。詳情請參閱「[資料集限定符](https://docs.cloud.google.com/bigquery/docs/information-schema-intro?hl=zh-tw#dataset_qualifier)」。**注意：**您必須使用[區域限定詞](https://docs.cloud.google.com/bigquery/docs/information-schema-intro?hl=zh-tw#region_qualifier)查詢 `INFORMATION_SCHEMA` 檢視畫面。查詢執行位置必須與 `INFORMATION_SCHEMA` 檢視區塊的區域相符。

**示例**

```
-- Returns metadata for parameters of a routine in a single dataset.
SELECT * FROM myDataset.INFORMATION_SCHEMA.PARAMETERS;

-- Returns metadata for parameters of a routine in a region.
SELECT * FROM region-us.INFORMATION_SCHEMA.PARAMETERS;
```

## 範例

#### 範例

如要對預設專案以外的專案中的資料集執行查詢，請使用下列格式新增專案 ID：

```
`PROJECT_ID`.`DATASET_ID`.INFORMATION_SCHEMA.PARAMETERS
```

請替換下列項目：

* `PROJECT_ID`：專案 ID。
* `DATASET_ID`：資料集 ID。

例如 `example-project.mydataset.INFORMATION_SCHEMA.JOBS_BY_PROJECT`。

以下範例會擷取 `INFORMATION_SCHEMA.PARAMETERS` 檢視表的所有參數。系統傳回的是預設專案 (`myproject`) 中 `mydataset` 內的處理常式中繼資料。

```
SELECT
  * EXCEPT(is_typed)
FROM
  mydataset.INFORMATION_SCHEMA.PARAMETERS
WHERE
  table_type = 'BASE TABLE';
```

**注意：** `INFORMATION_SCHEMA` 檢視表名稱會區分大小寫。

結果大致如下：

```
+-------------------+------------------+---------------+------------------+----------------+-----------+----------------+-----------+-------------------+--------------+
| specific_catalog  | specific_schema  | specific_name | ordinal_position | parameter_mode | is_result | parameter_name | data_type | parameter_default | is_aggregate |
+-------------------+------------------+---------------+------------------+----------------+-----------+----------------+-----------+-------------------+--------------+
| myproject         | mydataset        | myroutine1    | 0                | NULL           | YES       | NULL           | INT64     | NULL              | NULL         |
| myproject         | mydataset        | myroutine1    | 1                | NULL           | NO        | x              | INT64     | NULL              | NULL         |
+-------------------+------------------+---------------+------------------+----------------+-----------+----------------+-----------+-------------------+--------------+
```




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-04-30 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-04-30 (世界標準時間)。"],[],[]]