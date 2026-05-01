* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [參考資料](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# ROUTINE\_OPTIONS 檢視畫面

`INFORMATION_SCHEMA.ROUTINE_OPTIONS` 檢視表包含資料集中每個常式的每個選項，各佔一行。

## 所需權限

如要查詢 `INFORMATION_SCHEMA.ROUTINE_OPTIONS` 檢視畫面，您必須具備下列 Identity and Access Management (IAM) 權限：

* `bigquery.routines.get`
* `bigquery.routines.list`

下列每個預先定義的 IAM 角色都包含取得例行中繼資料所需的權限：

* `roles/bigquery.admin`
* `roles/bigquery.metadataViewer`
* `roles/bigquery.dataViewer`

如要進一步瞭解 BigQuery 權限，請參閱「[使用 IAM 控管存取權](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)」。

## 結構定義

查詢 `INFORMATION_SCHEMA.ROUTINE_OPTIONS` 檢視表時，資料集中每個處理常式的每個選項在查詢結果都會有一個資料列。

`INFORMATION_SCHEMA.ROUTINE_OPTIONS` 檢視表具有下列結構定義：

| 資料欄名稱 | 資料類型 | 值 |
| --- | --- | --- |
| `specific_catalog` | `STRING` | 包含定義選項之處理常式的專案名稱 |
| `specific_schema` | `STRING` | 包含定義選項之處理常式的資料集名稱 |
| `specific_name` | `STRING` | 處理常式的名稱 |
| `option_name` | `STRING` | [選項表格](#options_table)中的其中一個名稱值 |
| `option_type` | `STRING` | [選項表格](#options_table)中的其中一個資料類型值 |
| `option_value` | `STRING` | [選項表格](#options_table)中的其中一個值選項 |

##### 選項表格

| `OPTION_NAME` | `OPTION_TYPE` | `OPTION_VALUE` |
| --- | --- | --- |
| `description` | `STRING` | 處理常式的說明 (如有定義) |
| `library` | `ARRAY` | 處理常式中參照的資料庫名稱。僅適用於 JavaScript UDF |
| `data_governance_type` | `DataGovernanceType` | 支援的資料治理類型名稱。例如：`DATA_MASKING`。 |

為確保穩定性，建議您在資訊結構定義查詢中明確列出資料欄，而非使用萬用字元 (`SELECT *`)。明確列出資料欄可避免基礎結構定義變更時，查詢中斷。

## 範圍和語法

對這個檢視表執行的查詢必須包含資料集或區域限定詞。詳情請參閱「[語法](https://docs.cloud.google.com/bigquery/docs/information-schema-intro?hl=zh-tw#syntax)」。下表說明這個檢視畫面的區域和資源範圍：

| 檢視表名稱 | 資源範圍 | 區域範圍 |
| --- | --- | --- |
| `` [PROJECT_ID.]`region-REGION`.INFORMATION_SCHEMA.ROUTINE_OPTIONS `` | 專案層級 | `REGION` |
| `[PROJECT_ID.]DATASET_ID.INFORMATION_SCHEMA.ROUTINE_OPTIONS` | 資料集層級 | 資料集位置 |

取代下列項目：

* 選用：`PROJECT_ID`：您的 Google Cloud 專案 ID。如未指定，系統會使用預設專案。
* `REGION`：任何[資料集區域名稱](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)。
  例如：`` `region-us` ``。
* `DATASET_ID`：資料集 ID。詳情請參閱「[資料集限定符](https://docs.cloud.google.com/bigquery/docs/information-schema-intro?hl=zh-tw#dataset_qualifier)」。**注意：**您必須使用[區域限定詞](https://docs.cloud.google.com/bigquery/docs/information-schema-intro?hl=zh-tw#region_qualifier)查詢 `INFORMATION_SCHEMA` 檢視畫面。查詢執行位置必須與 `INFORMATION_SCHEMA` 檢視區塊的區域相符。

**示例**

```
-- Returns metadata for routines in a single dataset.
SELECT * FROM myDataset.INFORMATION_SCHEMA.ROUTINE_OPTIONS;

-- Returns metadata for routines in a region.
SELECT * FROM region-us.INFORMATION_SCHEMA.ROUTINE_OPTIONS;
```

## 範例

##### 範例 1：

以下範例藉由查詢 `INFORMATION_SCHEMA.ROUTINE_OPTIONS` 檢視表，擷取預設專案 (`myproject`) 中 `mydataset` 內所有處理常式的處理常式選項：

```
SELECT
  *
FROM
  mydataset.INFORMATION_SCHEMA.ROUTINE_OPTIONS;
```

**注意：** `INFORMATION_SCHEMA` 檢視表名稱會區分大小寫。

結果大致如下：

```
+-------------------+------------------+---------------+----------------------+---------------+------------------+
| specific_catalog  | specific_schema  | specific_name |     option_name      | option_type   | option_value     |
+-------------------+------------------+---------------+----------------------+---------------+------------------+
| myproject         | mydataset        | myroutine1    | description          | STRING        | "a description"  |
| myproject         | mydataset        | myroutine2    | library              | ARRAY<STRING> | ["a.js", "b.js"] |
+-------------------+------------------+---------------+----------------------+---------------+------------------+
```




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-04-30 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-04-30 (世界標準時間)。"],[],[]]