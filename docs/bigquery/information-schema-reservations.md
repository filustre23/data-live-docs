Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [參考資料](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 「預留項目」檢視畫面

`INFORMATION_SCHEMA.RESERVATIONS` 檢視畫面包含管理專案中所有目前預留項目的近乎即時清單。每一列代表一筆目前的預留項目。現有預留項目是指尚未刪除的預留項目。如要進一步瞭解預留項目，請參閱「[預留項目簡介](https://docs.cloud.google.com/bigquery/docs/reservations-intro?hl=zh-tw)」。

**注意：** 檢視表名稱 `INFORMATION_SCHEMA.RESERVATIONS` 和 `INFORMATION_SCHEMA.RESERVATIONS_BY_PROJECT` 是同義詞，可以交替使用。

## 必要權限

如要查詢 `INFORMATION_SCHEMA.RESERVATIONS` 檢視表，您必須具備專案的 `bigquery.reservations.list` Identity and Access Management (IAM) 權限。下列每個預先定義的 IAM 角色都包含必要權限：

* BigQuery 資源管理員 (`roles/bigquery.resourceAdmin`)
* BigQuery 資源編輯者 (`roles/bigquery.resourceEditor`)
* BigQuery 資源檢視者 (`roles/bigquery.resourceViewer`)
* BigQuery 使用者 (`roles/bigquery.user`)
* BigQuery 管理員 (`roles/bigquery.admin`)

如要進一步瞭解 BigQuery 權限，請參閱「[BigQuery IAM 角色和權限](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)」。

## 結構定義

`INFORMATION_SCHEMA.RESERVATIONS` 檢視表包含下列結構定義：

| 資料欄名稱 | 資料類型 | 值 |
| --- | --- | --- |
| `ddl` | `STRING` | 用來建立這個預留項目的 DDL 陳述式。 |
| `project_id` | `STRING` | 管理專案的 ID。 |
| `project_number` | `INTEGER` | 管理專案的編號。 |
| `reservation_name` | `STRING` | 使用者提供的預留項目名稱。 |
| `ignore_idle_slots` | `BOOL` | 如果設為 false，使用這項預留項目的查詢，就能使用其他運算能力承諾使用合約中未使用的閒置運算單元。 |
| `slot_capacity` | `INTEGER` | 預留項目的基準運算單元數量。 |
| `target_job_concurrency` | `INTEGER` | 可同時執行的查詢數量目標，受限於可用資源。如果設為零，系統會根據可用資源自動計算這個值。 |
| `autoscale` | `STRUCT` | 預留項目的自動調度資源容量資訊。欄位包括：   * `current_slots`：自動調度資源功能新增至預留項目的運算單元數量。   **注意：**使用者減少 `max_slots` 後，可能需要一段時間才能傳播，因此 `current_slots` 可能會維持原始值，且在短暫期間 (不到一分鐘) 內可能大於 `max_slots`。 * `max_slots`：自動調度資源功能可新增至預留項目的運算單元數量上限。 |
| `edition` | `STRING` | 與這個預留項目相關聯的版本。如要進一步瞭解版本，請參閱「[BigQuery 版本簡介](https://docs.cloud.google.com/bigquery/docs/editions-intro?hl=zh-tw)」。 |
| `primary_location` | `STRING` | 預留項目主要副本的目前位置。只有使用[代管災難復原功能](https://docs.cloud.google.com/bigquery/docs/managed-disaster-recovery?hl=zh-tw)的預留項目，才會設定這個欄位。 |
| `secondary_location` | `STRING` | 預留項目次要副本目前的位置。只有使用[代管災難復原功能](https://docs.cloud.google.com/bigquery/docs/managed-disaster-recovery?hl=zh-tw)的預留項目，才會設定這個欄位。 |
| `original_primary_location` | `STRING` | 最初建立預留項目的位置。 |
| `labels` | `RECORD` | 與預訂相關聯的標籤陣列。 |
| `reservation_group_path` | `ARRAY<STRING>` | 預留項目連結的預留項目群組。舉例來說，如果預留項目連結至群組 `my-group`，`reservation_group_path` 欄位會包含類似 `[my-group]` 的清單。 |
| `max_slots` | `INTEGER` | 這項預留項目可使用的運算單元數量上限，包括基準運算單元 (`slot_capacity`)、閒置運算單元 (如果 `ignore_idle_slots` 為 false) 和自動調度資源運算單元。使用者指定這個欄位，即可使用[預留項目可預測性功能](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#predictable)。 |
| `scaling_mode` | `STRING` | 預留項目的調度資源模式，決定預留項目如何從基準調度至 `max_slots`。使用者指定這個欄位，即可使用[預留項目可預測性功能](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#predictable)。 |

為確保穩定性，建議您在資訊結構定義查詢中明確列出資料欄，而非使用萬用字元 (`SELECT *`)。明確列出資料欄可避免查詢因基礎結構定義變更而中斷。

## 範圍和語法

對這個檢視表執行的查詢必須包含[區域限定詞](https://docs.cloud.google.com/bigquery/docs/information-schema-intro?hl=zh-tw#syntax)。下表說明這個檢視畫面的區域範圍：

| 檢視表名稱 | 資源範圍 | 區域範圍 |
| --- | --- | --- |
| `` [PROJECT_ID.]`region-REGION`.INFORMATION_SCHEMA.RESERVATIONS[_BY_PROJECT] `` | 專案層級 | `REGION` |

請更改下列內容：

* 選用：`PROJECT_ID`： Google Cloud 專案的 ID。如未指定，則會使用預設專案。
* `REGION`：任何[資料集區域名稱](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)。例如：`` `region-us` ``。**注意：**您必須使用[區域限定詞](https://docs.cloud.google.com/bigquery/docs/information-schema-intro?hl=zh-tw#region_qualifier)，才能查詢 `INFORMATION_SCHEMA` 檢視表。查詢執行位置必須與 `INFORMATION_SCHEMA` 檢視表的區域相符。

## 彙整預留項目檢視表和工作檢視表

[工作檢視畫面](https://docs.cloud.google.com/bigquery/docs/information-schema-jobs-by-user?hl=zh-tw)包含 `reservation_id` 欄。如果工作是在已指派預留項目的專案中執行，`reservation_id` 會採用以下格式：`reservation-admin-project:reservation-location.reservation-name`。

如要彙整預留項目檢視表和工作檢視表，您可以彙整工作檢視表資料欄 `reservation_id` 和預留項目檢視表資料欄 `project_id` 和 `reservation_name`。以下範例說明如何在預留項目和工作檢視表之間使用 `JOIN` 子句。

## 範例

以下範例顯示過去一小時內，指派預留項目的專案運算單元用量、運算單元容量和指派的預留項目。運算單元用量的單位為每秒運算單元毫秒數。

```
WITH
  job_data AS (
  SELECT
    job.period_start,
    job.reservation_id,
    job.period_slot_ms,
    job.job_id,
    job.job_type
  FROM
    `my-project.region-us`.INFORMATION_SCHEMA.JOBS_TIMELINE AS job
  WHERE
    job.period_start > TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 1 HOUR))
SELECT
  reservation.reservation_name AS reservation_name,
  job.period_start,
  reservation.slot_capacity,
  job.period_slot_ms,
  job.job_id,
  job.job_type
FROM
  job_data AS job
INNER JOIN
  `reservation-admin-project.region-us`.INFORMATION_SCHEMA.RESERVATIONS AS reservation
ON
  (job.reservation_id = CONCAT(reservation.project_id, ":", "US", ".", reservation.reservation_name));
```

輸出結果會與下列內容相似：

```
+------------------+---------------------+---------------+----------------+------------------+----------+
| reservation_name |    period_start     | slot_capacity | period_slot_ms |           job_id | job_type |
+------------------+---------------------+---------------+----------------+------------------+----------+
| my_reservation   | 2021-04-30 17:30:54 |           100 |          11131 | bquxjob_66707... | QUERY    |
| my_reservation   | 2021-04-30 17:30:55 |           100 |          49978 | bquxjob_66707... | QUERY    |
| my_reservation   | 2021-04-30 17:30:56 |           100 |           9038 | bquxjob_66707... | QUERY    |
| my_reservation   | 2021-04-30 17:30:57 |           100 |          17237 | bquxjob_66707... | QUERY    |
```

這項查詢會使用 `RESERVATIONS` 檢視表取得預留項目資訊。如果預留項目在過去一小時內有所變更，`reservation_slot_capacity` 欄可能不準確。

查詢會將 `RESERVATIONS` 與 [`JOBS_TIMELINE`](https://docs.cloud.google.com/bigquery/docs/information-schema-jobs-timeline?hl=zh-tw) 彙整，將工作時間片段與預留資訊建立關聯。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-10-24 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-10-24 (世界標準時間)。"],[],[]]