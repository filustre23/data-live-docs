Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [參考資料](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# INFORMATION\_SCHEMA.BI\_CAPACITY\_CHANGES 檢視畫面

`INFORMATION_SCHEMA.BI_CAPACITY_CHANGES`檢視畫面會顯示 BI Engine 容量的變更記錄。如要查看 BI Engine 預留項目的目前狀態，請參閱[`INFORMATION_SCHEMA.BI_CAPACITIES` 檢視畫面](https://docs.cloud.google.com/bigquery/docs/information-schema-bi-capacities?hl=zh-tw)。

## 必要權限

如要查詢 `INFORMATION_SCHEMA.BI_CAPACITY_CHANGES` 檢視畫面，您需要 BI Engine 預留空間的 `bigquery.bireservations.get` Identity and Access Management (IAM) 權限。

如要進一步瞭解 BigQuery 權限，請參閱「[使用 IAM 控管存取權](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)」。

## 結構定義

查詢 `INFORMATION_SCHEMA.BI_CAPACITY_CHANGES` 檢視表時，查詢結果會針對 BI Engine 容量的每次更新 (包括目前狀態)，各列出一個相對應的資料列。

`INFORMATION_SCHEMA.BI_CAPACITY_CHANGES` 檢視表具有下列結構定義：

| 資料欄名稱 | 資料類型 | 值 |
| --- | --- | --- |
| `change_timestamp` | `TIMESTAMP` | 上次更新 BI Engine 容量的時間戳記。 |
| `project_id` | `STRING` | 包含 BI Engine 容量的專案 ID。 |
| `project_number` | `INTEGER` | 包含 BI Engine 容量的專案編號。 |
| `bi_capacity_name` | `STRING` | 物件的名稱。每個專案只能有一個容量，因此名稱一律為 `default`。 |
| `size` | `INTEGER` | BI Engine RAM (以位元組為單位)。 |
| `user_email` | `STRING` | 進行變更的使用者電子郵件地址或[員工身分聯盟](https://docs.cloud.google.com/iam/docs/workforce-identity-federation?hl=zh-tw)主體。`google`，瞭解 Google 進行的變更。`NULL`：如果電子郵件地址不明。 |
| `preferred_tables` | `REPEATED STRING` | 這組偏好資料表必須使用這個 BI Engine 容量。如果設為 `null`，目前專案中的所有查詢都會使用 BI Engine 容量。 |

為確保穩定性，建議您在資訊結構定義查詢中明確列出資料欄，而非使用萬用字元 (`SELECT *`)。明確列出資料欄可避免基礎結構定義變更時，查詢中斷。

## 語法

對這個檢視表執行的查詢必須包含[區域限定詞](https://docs.cloud.google.com/bigquery/docs/information-schema-intro?hl=zh-tw#syntax)。專案 ID 為選填欄位。如未指定專案 ID，系統會使用查詢執行的專案。

| 檢視表名稱 | 資源範圍 | 區域範圍 |
| --- | --- | --- |
| `` [PROJECT_ID.]`region-REGION`.INFORMATION_SCHEMA.BI_CAPACITY_CHANGES `` | 專案層級 | `REGION` |

取代下列項目：

* 選用：`PROJECT_ID`：您的 Google Cloud 專案 ID。如未指定，系統會使用預設專案。
* `REGION`：任何[資料集區域名稱](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)。
  例如：`` `region-us` ``。**注意：**您必須使用[區域限定詞](https://docs.cloud.google.com/bigquery/docs/information-schema-intro?hl=zh-tw#region_qualifier)查詢 `INFORMATION_SCHEMA` 檢視畫面。查詢執行位置必須與 `INFORMATION_SCHEMA` 檢視區塊的區域相符。

```
-- Returns the history of BI Engine capacity.
SELECT * FROM myproject.`region-us`.INFORMATION_SCHEMA.BI_CAPACITY_CHANGES;
```

## 範例

以下範例會從 `INFORMATION_SCHEMA.BI_CAPACITY_CHANGES` 檢視表擷取目前的 BI Engine 容量變化。

如要對查詢執行所在的專案以外的專案執行查詢，請使用下列格式將專案 ID 新增至區域：`` `project_id`.`region_id`.INFORMATION_SCHEMA.BI_CAPACITY_CHANGES ``。

以下範例會取得電子郵件地址為 `email@mycompanymail.com` 的使用者對 BI Engine 容量所做的所有變更：

```
SELECT *
FROM `my-project-id.region-us`.INFORMATION_SCHEMA.BI_CAPACITY_CHANGES
WHERE user_email = "email@mycompanymail.com"
```

傳回的結果看起來類似下列內容：

```
  +---------------------+---------------+----------------+------------------+--------------+---------------------+----------------------------------------------------------------------------------------+
  |  change_timestamp   |  project_id   | project_number | bi_capacity_name |     size     |     user_email      |                                               preferred_tables                         |
  +---------------------+---------------+----------------+------------------+--------------+---------------------+----------------------------------------------------------------------------------------+
  | 2022-06-14 02:22:18 | my-project-id |   123456789000 | default          | 268435456000 | email@mycompany.com | ["my-project-id.dataset1.table1","bigquery-public-data.chicago_taxi_trips.taxi_trips"] |
  | 2022-06-08 20:25:51 | my-project-id |   123456789000 | default          | 268435456000 | email@mycompany.com | ["bigquery-public-data.chicago_taxi_trips.taxi_trips"]                                 |
  | 2022-04-01 21:06:49 | my-project-id |   123456789000 | default          | 161061273600 | email@mycompany.com | [""]                                                                                   |
  +---------------------+---------------+----------------+------------------+--------------+---------------------+----------------------------------------------------------------------------------------+
```

以下範例會取得過去七天的 BI Engine 容量變化：

```
SELECT
  change_timestamp,
  size,
  user_email,
  preferred_tables
FROM `my-project-id.region-us`.INFORMATION_SCHEMA.BI_CAPACITY_CHANGES
WHERE change_timestamp > TIMESTAMP_SUB(CURRENT_DATE(), INTERVAL 7 DAY)
```

傳回的結果看起來類似下列內容：

```
  +---------------------+--------------+----------------------+-------------------+
  |  change_timestamp   |     size     |     user_email       |  preferred_tables |                                                                                    |
  +---------------------+--------------+----------------------+-------------------+
  | 2023-07-08 18:25:09 | 268435456000 | sundar@mycompany.com | [""]              |
  | 2023-07-09 17:47:26 | 161061273600 | pichai@mycompany.com | ["pr.dataset.t1"] |
  +---------------------+--------------+----------------------+-------------------+
```




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-14 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-14 (世界標準時間)。"],[],[]]