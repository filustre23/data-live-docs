Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [參考資料](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 「VIEWS」檢視畫面

`INFORMATION_SCHEMA.VIEWS` 檢視表包含檢視表的中繼資料。

## 所需權限

如要取得檢視中繼資料，您需要下列 Identity and Access Management (IAM) 權限：

* `bigquery.tables.get`
* `bigquery.tables.list`

下列每個預先定義的 IAM 角色都包含檢視中繼資料所需的權限：

* `roles/bigquery.admin`
* `roles/bigquery.dataEditor`
* `roles/bigquery.metadataViewer`
* `roles/bigquery.dataViewer`

如要進一步瞭解 BigQuery 權限，請參閱「[使用 IAM 控管存取權](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)」。

## 結構定義

當您查詢 `INFORMATION_SCHEMA.VIEWS` 檢視表時，資料集中的每個檢視表都會有一列相對應的查詢結果。

`INFORMATION_SCHEMA.VIEWS` 檢視表具有下列結構定義：

| 資料欄名稱 | 資料類型 | 值 |
| --- | --- | --- |
| `table_catalog` | `STRING` | 包含資料集的專案名稱 |
| `table_schema` | `STRING` | 包含檢視表的資料集名稱 (又稱為資料集 `id`) |
| `table_name` | `STRING` | 檢視表的名稱 (又稱為資料表 `id`) |
| `view_definition` | `STRING` | 定義檢視表的 SQL 查詢 |
| `check_option` | `STRING` | 傳回的值一律為 `NULL` |
| `use_standard_sql` | `STRING` | 如果檢視表是使用 GoogleSQL 查詢建立，即為 `YES`；如果將 `useLegacySql` 設為 `true`，則為 `NO` |

為確保穩定性，建議您在資訊結構定義查詢中明確列出資料欄，而非使用萬用字元 (`SELECT *`)。明確列出資料欄可避免基礎結構定義變更時，查詢中斷。

## 範圍和語法

對這個檢視表執行的查詢必須包含資料集或區域限定詞。如果是含有資料集限定符的查詢，您必須具備該資料集的權限。如要查詢含有區域限定符的資料，您必須具備專案權限。詳情請參閱「[語法](https://docs.cloud.google.com/bigquery/docs/information-schema-intro?hl=zh-tw#syntax)」。下表說明這個檢視畫面的區域和資源範圍：

| 檢視表名稱 | 資源範圍 | 區域範圍 |
| --- | --- | --- |
| `` [PROJECT_ID.]`region-REGION`.INFORMATION_SCHEMA.VIEWS `` | 專案層級 | `REGION` |
| `[PROJECT_ID.]DATASET_ID.INFORMATION_SCHEMA.VIEWS` | 資料集層級 | 資料集位置 |

取代下列項目：

* 選用：`PROJECT_ID`：您的 Google Cloud 專案 ID。如未指定，系統會使用預設專案。
* `REGION`：任何[資料集區域名稱](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)。
  例如：`` `region-us` ``。
* `DATASET_ID`：資料集 ID。詳情請參閱「[資料集限定符](https://docs.cloud.google.com/bigquery/docs/information-schema-intro?hl=zh-tw#dataset_qualifier)」。**注意：**您必須使用[區域限定詞](https://docs.cloud.google.com/bigquery/docs/information-schema-intro?hl=zh-tw#region_qualifier)查詢 `INFORMATION_SCHEMA` 檢視畫面。查詢執行位置必須與 `INFORMATION_SCHEMA` 檢視區塊的區域相符。

例如：

```
-- Returns metadata for views in a single dataset.
SELECT * FROM myDataset.INFORMATION_SCHEMA.VIEWS;

-- Returns metadata for all views in a region.
SELECT * FROM region-us.INFORMATION_SCHEMA.VIEWS;
```

## 範例

##### 範例 1：

下列範例從 `INFORMATION_SCHEMA.VIEWS` 檢視表擷取了所有資料欄，但保留 `check_option` 以供未來使用。系統傳回的是預設專案 (`myproject`) 中 `mydataset` 內所有檢視表的中繼資料。

如要對預設專案以外的專案執行查詢，請使用以下格式將專案 ID 新增至資料集：`` `project_id`.dataset.INFORMATION_SCHEMA.view ``；例如 `` `myproject`.mydataset.INFORMATION_SCHEMA.VIEWS ``。

```
SELECT
  * EXCEPT (check_option)
FROM
  mydataset.INFORMATION_SCHEMA.VIEWS;
```

**注意：** `INFORMATION_SCHEMA` 檢視表名稱會區分大小寫。

結果大致如下：

```
  +----------------+---------------+---------------+---------------------------------------------------------------------+------------------+
  | table_catalog  | table_schema  |  table_name   |                        view_definition                              | use_standard_sql |
  +----------------+---------------+---------------+---------------------------------------------------------------------+------------------+
  | myproject      | mydataset     | myview        | SELECT column1, column2 FROM [myproject:mydataset.mytable] LIMIT 10 | NO               |
  +----------------+---------------+---------------+---------------------------------------------------------------------+------------------+
```

請注意，結果顯示這個檢視表是使用舊版 SQL 查詢建立。

##### 範例 2：

以下範例會擷取用來在預設專案 (`myproject`) 中的 `mydataset` 內定義 `myview` 的 SQL 查詢與查詢語法。

如要對預設專案以外的專案執行查詢，請使用以下格式將專案 ID 新增至資料集：`` `project_id`.dataset.INFORMATION_SCHEMA.view ``；例如 `` `myproject`.mydataset.INFORMATION_SCHEMA.VIEWS ``。

```
SELECT
  table_name, view_definition, use_standard_sql
FROM
  mydataset.INFORMATION_SCHEMA.VIEWS
WHERE
  table_name = 'myview';
```

**注意：** `INFORMATION_SCHEMA` 檢視表名稱會區分大小寫。

結果大致如下：

```
  +---------------+---------------------------------------------------------------+------------------+
  |  table_name   |                        view_definition                        | use_standard_sql |
  +---------------+---------------------------------------------------------------+------------------+
  | myview        | SELECT column1, column2, column3 FROM mydataset.mytable       | YES              |
  +---------------+---------------------------------------------------------------+------------------+
```

請注意，結果顯示這個檢視表是使用 GoogleSQL 查詢建立。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-16 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-16 (世界標準時間)。"],[],[]]