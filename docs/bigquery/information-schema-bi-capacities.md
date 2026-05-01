* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [參考資料](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# INFORMATION\_SCHEMA.BI\_CAPACITIES 檢視畫面

`INFORMATION_SCHEMA.BI_CAPACITIES` 檢視畫面包含 BI Engine 容量目前狀態的中繼資料。如要查看 BI Engine 預留空間的變更記錄，請參閱[`INFORMATION_SCHEMA.BI_CAPACITY_CHANGES` 檢視畫面](https://docs.cloud.google.com/bigquery/docs/information-schema-bi-capacity-changes?hl=zh-tw)。

## 必要權限

如要查詢 `INFORMATION_SCHEMA.BI_CAPACITIES` 檢視畫面，您需要 BI Engine 預留空間的 `bigquery.bireservations.get` Identity and Access Management (IAM) 權限。

如要進一步瞭解 BigQuery 權限，請參閱「[使用 IAM 控管存取權](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)」。

## 結構定義

查詢 `INFORMATION_SCHEMA.BI_CAPACITIES` 檢視表時，查詢結果會包含一個資料列，其中列出 BI Engine 容量的目前狀態。

`INFORMATION_SCHEMA.BI_CAPACITIES` 檢視表具有下列結構定義：

| 資料欄名稱 | 資料類型 | 值 |
| --- | --- | --- |
| `project_id` | `STRING` | 包含 BI Engine 容量的專案 ID。 |
| `project_number` | `INTEGER` | 包含 BI Engine 容量的專案編號。 |
| `bi_capacity_name` | `STRING` | 物件的名稱。每個專案只能有一個容量，因此名稱一律會設為 `default`。 |
| `size` | `INTEGER` | BI Engine RAM (以位元組為單位) |
| `preferred_tables` | `REPEATED STRING` | 這組偏好資料表必須使用 BI Engine 容量。如果設為 `null`，目前專案中的所有查詢都會使用 BI Engine 容量 |

為確保穩定性，建議您在資訊結構定義查詢中明確列出資料欄，而非使用萬用字元 (`SELECT *`)。明確列出資料欄可避免基礎結構定義變更時，查詢中斷。

## 範圍和語法

對這個檢視表執行的查詢必須包含[區域限定詞](https://docs.cloud.google.com/bigquery/docs/information-schema-intro?hl=zh-tw#syntax)。專案 ID 為選填欄位。如未指定專案 ID，系統會使用查詢執行的專案。

| 檢視表名稱 | 資源範圍 | 區域範圍 |
| --- | --- | --- |
| `` [PROJECT_ID.]`region-REGION`.INFORMATION_SCHEMA.BI_CAPACITIES `` | 專案層級 | `REGION` |

取代下列項目：

* 選用：`PROJECT_ID`：您的 Google Cloud 專案 ID。如未指定，系統會使用預設專案。
* `REGION`：任何[資料集區域名稱](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)。
  例如：`` `region-us` ``。**注意：**您必須使用[區域限定詞](https://docs.cloud.google.com/bigquery/docs/information-schema-intro?hl=zh-tw#region_qualifier)查詢 `INFORMATION_SCHEMA` 檢視畫面。查詢執行位置必須與 `INFORMATION_SCHEMA` 檢視區塊的區域相符。

**示例**

```
-- Returns current state of BI Engine capacity.
SELECT * FROM myproject.`region-us`.INFORMATION_SCHEMA.BI_CAPACITIES;
```

## 範例

以下範例會從 `INFORMATION_SCHEMA.BI_CAPACITIES` 檢視表擷取目前的 BI Engine 容量變更。

如要對查詢執行所在的專案以外的專案執行查詢，請使用下列格式將專案 ID 新增至區域：`` `project_id`.`region_id`.INFORMATION_SCHEMA.BI_CAPACITIES ``。

以下範例顯示 ID 為「my-project-id」的專案中，BI Engine 的目前狀態：

```
SELECT *
FROM `my-project-id.region-us`.INFORMATION_SCHEMA.BI_CAPACITIES
```

傳回的結果看起來類似下列內容：

```
  +---------------+----------------+------------------+--------------+-----------------------------------------------------------------------------------------------+
  |  project_id   | project_number | bi_capacity_name |     size     |                                               preferred_tables                                |
  +---------------+----------------+------------------+--------------+-----------------------------------------------------------------------------------------------+
  | my-project-id |   123456789000 | default          | 268435456000 | "my-company-project-id.dataset1.table1","bigquery-public-data.chicago_taxi_trips.taxi_trips"] |
  +---------------+----------------+------------------+--------------+-----------------------------------------------------------------------------------------------+
```

以下範例會傳回查詢專案的 BI Engine 容量大小 (以 GB 為單位)：

```
SELECT
  project_id,
  size/1024.0/1024.0/1024.0 AS size_gb
FROM `region-us`.INFORMATION_SCHEMA.BI_CAPACITIES
```

傳回的結果看起來類似下列內容：

```
  +---------------+---------+
  |  project_id   | size_gb |
  +---------------+---------+
  | my-project-id |  250.0  |
  +---------------+---------+
```




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-04-30 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-04-30 (世界標準時間)。"],[],[]]