Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [參考資料](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# SCHEMATA 檢視畫面

`INFORMATION_SCHEMA.SCHEMATA` 檢視畫面會提供專案或區域中資料集的相關資訊。這個檢視區會為每個資料集傳回一個資料列。

## 事前準備

如要查詢資料集的中繼資料檢視畫面 `SCHEMATA`，您需要專案層級的「身分與存取權管理」(IAM) `bigquery.datasets.get` 權限。

下列預先定義的 IAM 角色都包含必要權限，可讓您取得 `SCHEMATA` 檢視畫面：

* `roles/bigquery.admin`
* `roles/bigquery.dataEditor`
* `roles/bigquery.dataOwner`
* `roles/bigquery.dataViewer`

如要進一步瞭解 BigQuery 權限，請參閱「[使用 IAM 控管存取權](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)」。

## 結構定義

查詢 `INFORMATION_SCHEMA.SCHEMATA` 檢視表時，指定專案中的每個資料集在查詢結果中都會有一個資料列。

`INFORMATION_SCHEMA.SCHEMATA` 檢視表具有下列結構定義：

| 資料欄名稱 | 資料類型 | 值 |
| --- | --- | --- |
| `catalog_name` | `STRING` | 包含資料集的專案名稱 |
| `schema_name` | `STRING` | 資料集的名稱，又稱為 `datasetId` |
| `schema_owner` | `STRING` | 此值一律為 `NULL` |
| `creation_time` | `TIMESTAMP` | 資料集的建立時間 |
| `last_modified_time` | `TIMESTAMP` | 資料集的上次修改時間 |
| `location` | `STRING` | 資料集的地理位置 |
| `ddl` | `STRING` | 可用於建立資料集的 `CREATE SCHEMA` DDL 陳述式 |
| `default_collation_name` | `STRING` | 預設[排序規格](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/collation-concepts?hl=zh-tw)的名稱 (如有)，否則為 `NULL`。 |
| `sync_status` | `JSON` | 主要和次要副本之間的同步狀態，適用於[跨區域複製](https://docs.cloud.google.com/bigquery/docs/data-replication?hl=zh-tw)和[災難復原](https://docs.cloud.google.com/bigquery/docs/managed-disaster-recovery?hl=zh-tw)資料集。如果副本是主要副本，或資料集未使用複製功能，則傳回 `NULL`。 |

為確保穩定性，建議您在資訊結構定義查詢中明確列出資料欄，而非使用萬用字元 (`SELECT *`)。明確列出資料欄可避免基礎結構定義變更時，查詢中斷。

## 範圍和語法

對這個檢視表執行的查詢必須包含[區域限定詞](https://docs.cloud.google.com/bigquery/docs/information-schema-intro?hl=zh-tw#syntax)。如未指定地區限定符，系統會從美國地區擷取中繼資料。下表說明這個檢視畫面的區域範圍：

| 檢視表名稱 | 資源範圍 | 區域範圍 |
| --- | --- | --- |
| `[PROJECT_ID.]INFORMATION_SCHEMA.SCHEMATA` | 專案層級 | 美國區域 |
| `` [PROJECT_ID.]`region-REGION`.INFORMATION_SCHEMA.SCHEMATA `` | 專案層級 | `REGION` |

取代下列項目：

* 選用：`PROJECT_ID`：您的 Google Cloud 專案 ID。如未指定，系統會使用預設專案。
* `REGION`：任何[資料集區域名稱](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)。
  例如：`` `region-us` ``。**注意：**您必須使用[區域限定詞](https://docs.cloud.google.com/bigquery/docs/information-schema-intro?hl=zh-tw#region_qualifier)查詢 `INFORMATION_SCHEMA` 檢視畫面。查詢執行位置必須與 `INFORMATION_SCHEMA` 檢視區塊的區域相符。

**示例**

```
-- Returns metadata for datasets in a region.
SELECT * FROM region-us.INFORMATION_SCHEMA.SCHEMATA;
```

## 範例

如要對預設專案以外的專案執行查詢，請使用以下格式將專案 ID 新增至資料集：

```
`PROJECT_ID`.INFORMATION_SCHEMA.SCHEMATA
```

例如：`` `myproject`.INFORMATION_SCHEMA.SCHEMATA ``。

```
SELECT
  * EXCEPT (schema_owner)
FROM
  INFORMATION_SCHEMA.SCHEMATA;
```

**注意：** `INFORMATION_SCHEMA` 檢視表名稱會區分大小寫。

結果大致如下。為了方便閱讀，部分資料欄已從結果中排除。

```
+----------------+---------------+---------------------+---------------------+------------+------------------------------------------+
|  catalog_name  |  schema_name  |    creation_time    | last_modified_time  |  location  |                   ddl                    |
+----------------+---------------+---------------------+---------------------+------------+------------------------------------------+
| myproject      | mydataset1    | 2018-11-07 19:50:24 | 2018-11-07 19:50:24 | US         | CREATE SCHEMA `myproject.mydataset1`     |
|                |               |                     |                     |            | OPTIONS(                                 |
|                |               |                     |                     |            |   location="us"                          |
|                |               |                     |                     |            | );                                       |
+----------------+---------------+---------------------+---------------------+------------+------------------------------------------+
| myproject      | mydataset2    | 2018-07-16 04:24:22 | 2018-07-16 04:24:22 | US         | CREATE SCHEMA `myproject.mydataset2`     |
|                |               |                     |                     |            | OPTIONS(                                 |
|                |               |                     |                     |            |   default_partition_expiration_days=3.0, |
|                |               |                     |                     |            |   location="us"                          |
|                |               |                     |                     |            | );                                       |
+----------------+---------------+---------------------+---------------------+------------+------------------------------------------+
| myproject      | mydataset3    | 2018-02-07 21:08:45 | 2018-05-01 23:32:53 | US         | CREATE SCHEMA `myproject.mydataset3`     |
|                |               |                     |                     |            | OPTIONS(                                 |
|                |               |                     |                     |            |   description="My dataset",              |
|                |               |                     |                     |            |   location="us"                          |
|                |               |                     |                     |            | );                                       |
+----------------+---------------+---------------------+---------------------+------------+------------------------------------------+
```




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-08 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-08 (世界標準時間)。"],[],[]]