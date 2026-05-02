* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [參考資料](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# RESERVATIONS\_TIMELINE 檢視畫面

`INFORMATION_SCHEMA.RESERVATIONS_TIMELINE` 檢視畫面會即時顯示每個預留項目管理專案的預留項目中繼資料時間切片，每分鐘更新一次。此外，`per_second_details` 陣列會顯示每秒的自動調整規模詳細資料。

**注意：** 檢視區塊名稱 `INFORMATION_SCHEMA.RESERVATIONS_TIMELINE` 和 `INFORMATION_SCHEMA.RESERVATIONS_TIMELINE_BY_PROJECT` 是同義詞，可以互換使用。

## 必要權限

如要查詢 `INFORMATION_SCHEMA.RESERVATIONS_TIMELINE` 檢視畫面，您需要專案的 `bigquery.reservations.list` Identity and Access Management (IAM) 權限。下列預先定義的 IAM 角色都包含必要權限：

* BigQuery 資源管理員 (`roles/bigquery.resourceAdmin`)
* BigQuery 資源編輯者 (`roles/bigquery.resourceEditor`)
* BigQuery 資源檢視者 (`roles/bigquery.resourceViewer`)
* BigQuery 使用者 (`roles/bigquery.user`)
* BigQuery 管理員 (`roles/bigquery.admin`)

如要進一步瞭解 BigQuery 權限，請參閱 [BigQuery IAM 角色和權限](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)。

## 結構定義

查詢 `INFORMATION_SCHEMA.RESERVATIONS_TIMELINE` 檢視表時，過去 180 天內每分鐘的每個 BigQuery 預留項目，在查詢結果中都會有一個相對應的資料列。如果發生時間超過 180 天，每分鐘的預留項目變更也會有一個相對應的資料列。每個週期都從整分鐘間隔開始，且持續整整一分鐘。

`INFORMATION_SCHEMA.RESERVATIONS_TIMELINE` 檢視表具有下列結構定義：

| 資料欄名稱 | 資料類型 | 值 |
| --- | --- | --- |
| `autoscale` | `STRUCT` | 內含預留項目的自動調度資源容量相關資訊。欄位包括：   * `current_slots`：預訂可用的自動調度資源配額數量。   因為 `current_slots` 可能在一分鐘內更新多次，   請改用 `per_second_details.autoscale_current_slots`。   反映每秒的準確狀態。 此外，使用者減少 `max_slots` 後，可能需要一段時間才能傳播，因此 `current_slots` 可能會維持原始值，且在短時間內 (不到一分鐘) 可能會大於 `max_slots`。 * `max_slots`：自動調度資源可為預留項目新增的運算單元數量上限。 **注意：**如果經常變更 `max_slots`，建議改用 `per_second_details.autoscale_max_slots`。 |
| `edition` | `STRING` | 與這項預訂相關聯的版本。如要進一步瞭解版本，請參閱「[BigQuery 版本簡介](https://docs.cloud.google.com/bigquery/docs/editions-intro?hl=zh-tw)」。 |
| `ignore_idle_slots` | `BOOL` | 如果已啟用運算單元共用功能，則為 False，否則為 True。 |
| `labels` | `RECORD` | 與預訂項目相關聯的標籤陣列。 |
| `reservation_group_path` | `STRING` | 預訂項目所連結的階層式群組結構。 舉例來說，如果群組結構包含上層群組和子項群組，則 `reservation_group_path` 欄位會包含類似 `[parent group, child group]` 的清單。這個欄位為[預先發布版](https://cloud.google.com/products?hl=zh-tw#product-launch-stages)。 |
| `period_start` | `TIMESTAMP` | 這個一分鐘期間的開始時間。 |
| `per_second_details` | `STRUCT` | 包含每秒的預訂容量和使用量資訊。欄位包括：   * `start_time`：秒的確切時間戳記。 * `autoscale_current_slots`：此秒預留項目可用的自動調度資源運算單元數量。這個數字不含基準運算單元。   **注意：**減少 `max_slots` 時，變更可能不會立即生效。在這段短暫期間 (不到一分鐘)，`current_slots` 可能會維持原始值，而原始值可能高於 `max_slots` 的值。 * `autoscale_max_slots`：自動調度資源功能在這個時間點可為預留項目新增的運算單元數量上限。   這個數字不含基準運算單元。 * `slots_assigned`：這個預留項目在該秒分配到的運算單元數量。這等於預留項目的基準運算單元數量。 * `slots_max_assigned`：這個預留項目的運算單元容量上限，包括目前運算單元共用量。如果 `ignore_idle_slots` 為 true，這個欄位與 `slots_assigned` 相同。否則，`slots_max_assigned` 欄位會顯示管理專案中所有容量使用承諾的總配額數。 * `borrowed_slots`：從閒置時段分享功能使用的時段數量。只有在 `ignore_idle_slots` 為 false，且這段時間內使用了閒置運算單元時，才會填入這個欄位。 * `lent_slots`：其他預留項目從這個預留項目的基準運算單元集區使用的運算單元數量。只有在 `ignore_idle_slots` 為 false，且其他預留項目在這段時間內使用了閒置運算單元時，才會填入這個欄位。   如果在這 1 分鐘內有任何自動調度資源或預訂異動，陣列會填入 60 列。不過，如果非自動調整規模的預訂項目在這 1 分鐘內維持不變，陣列就會是空白，否則系統會重複相同數字 60 次。 |
| `project_id` | `STRING` | 預訂管理專案的 ID。 |
| `project_number` | `INTEGER` | 專案編號。 |
| `reservation_id` | `STRING` | 用於與 jobs\_timeline 表格聯結。格式為 *project\_id*:*location*.*reservation\_name*。 |
| `reservation_name` | `STRING` | 預訂名稱。 |
| `slots_assigned` | `INTEGER` | 指派給這個預留項目的運算單元數量。 |
| `slots_max_assigned` | `INTEGER` | 這個預留項目的運算單元容量上限，包括運算單元共用。如為 true，這與 `slots_assigned` 相同，否則這是管理專案中所有容量使用承諾的運算單元總數。`ignore_idle_slots` |
| `max_slots` | `INTEGER` | 這個預留項目可使用的運算單元數量上限，包括基準運算單元 (`slot_capacity`)、閒置運算單元 (如果 `ignore_idle_slots` 為 false) 和自動調度運算單元。使用者會指定這個欄位，以使用[預訂預測功能](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#predictable)。 |
| `scaling_mode` | `STRING` | 預留項目的縮放模式，決定預留項目如何從基準縮放至 `max_slots`。使用者會指定這個欄位，以使用[預訂預測功能](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#predictable)。 |
| `period_autoscale_slot_seconds` | `INTEGER` | 自動調整功能在特定分鐘內收取的總時段秒數 (每個資料列對應一分鐘)。 |
| `is_creation_region` | `BOOLEAN` | 指定目前區域是否為建立預訂的所在地。這個位置用於決定基準預留運算單元的價格。如果是容錯移轉[災難復原 (DR)](https://docs.cloud.google.com/bigquery/docs/managed-disaster-recovery?hl=zh-tw) 預留項目，`TRUE` 值表示原始主要位置；如果是非 DR 預留項目，`TRUE` 值表示預留項目位置。  如果預訂項目不是容錯移轉項目，這個值一律為 `TRUE`。如果是容錯移轉預留項目，值取決於區域：原始主要區域為 `TRUE`，原始次要區域為 `FALSE`。 |

為確保穩定性，建議您在資訊結構定義查詢中明確列出資料欄，而非使用萬用字元 (`SELECT *`)。明確列出資料欄可避免基礎結構定義變更時，查詢中斷。

## 範圍和語法

對這個檢視表執行的查詢必須包含[區域限定詞](https://docs.cloud.google.com/bigquery/docs/information-schema-intro?hl=zh-tw#syntax)。如未指定區域限定符，系統會從所有區域擷取中繼資料。下表說明這個檢視畫面的區域和資源範圍：

| 檢視表名稱 | 資源範圍 | 區域範圍 |
| --- | --- | --- |
| `` [PROJECT_ID.]`region-REGION`.INFORMATION_SCHEMA.RESERVATIONS_TIMELINE[_BY_PROJECT] `` | 專案層級 | `REGION` |

取代下列項目：

* 選用：`PROJECT_ID`：您的 Google Cloud 專案 ID。如未指定，系統會使用預設專案。
* `REGION`：任何[資料集區域名稱](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)。
  例如：`` `region-us` ``。**注意：**您必須使用[區域限定詞](https://docs.cloud.google.com/bigquery/docs/information-schema-intro?hl=zh-tw#region_qualifier)查詢 `INFORMATION_SCHEMA` 檢視畫面。查詢執行位置必須與 `INFORMATION_SCHEMA` 檢視區塊的區域相符。

## 範例

#### 範例：查看每秒自動調度資源的次數

以下範例顯示所有工作每秒的自動調度資源 `YOUR_RESERVATION_ID` 規模：

```
SELECT s.start_time, s.autoscale_current_slots
FROM `region-us.INFORMATION_SCHEMA.RESERVATIONS_TIMELINE` m
JOIN m.per_second_details s
WHERE period_start BETWEEN '2025-09-28' AND '2025-09-29'
  AND reservation_id = 'YOUR_RESERVATION_ID'
ORDER BY period_start, s.start_time
```

結果大致如下：

```
+---------------------+-------------------------+
|     start_time      | autoscale_current_slots |
+---------------------+-------------------------+
| 2025-09-28 00:00:00 |                    1600 |
| 2025-09-28 00:00:01 |                    1600 |
| 2025-09-28 00:00:02 |                    1600 |
| 2025-09-28 00:00:03 |                    1600 |
| 2025-09-28 00:00:04 |                    1600 |
+---------------------+-------------------------+
```


**注意：**`period_start` 資料欄是分區索引鍵，因此請務必依 `period_start` 篩選，以提高查詢效率。

#### 範例：查看每秒的運算單元總用量

如要對預設專案以外的專案執行查詢，請使用以下格式新增專案 ID：

```
`PROJECT_ID`.`region-REGION_NAME`.INFORMATION_SCHEMA.JOBS_TIMELINE_BY_ORGANIZATION
```

例如 `` `myproject`.`region-us`.INFORMATION_SCHEMA.JOBS_TIMELINE_BY_ORGANIZATION ``。

以下範例顯示指派給 `YOUR_RESERVATION_ID` 的專案在所有工作中的每秒時段用量：

```
SELECT
  jobs.period_start,
  SUM(jobs.period_slot_ms) / 1000 AS period_slot_seconds,
  ANY_VALUE(COALESCE(s.slots_assigned, res.slots_assigned)) AS estimated_slots_assigned,
  ANY_VALUE(COALESCE(s.slots_max_assigned, res.slots_max_assigned)) AS estimated_slots_max_assigned
FROM `region-us`.INFORMATION_SCHEMA.JOBS_TIMELINE_BY_ORGANIZATION jobs
JOIN `region-us`.INFORMATION_SCHEMA.RESERVATIONS_TIMELINE res
  ON jobs.reservation_id = res.reservation_id
  AND TIMESTAMP_TRUNC(jobs.period_start, MINUTE) = res.period_start
LEFT JOIN UNNEST(res.per_second_details) s
  ON jobs.period_start = s.start_time
WHERE
  jobs.job_creation_time
    BETWEEN TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 1 DAY)
        AND CURRENT_TIMESTAMP()
  AND res.period_start
    BETWEEN TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 1 DAY)
        AND CURRENT_TIMESTAMP()
  AND res.reservation_id = 'YOUR_RESERVATION_ID'
  AND (jobs.statement_type != "SCRIPT" OR jobs.statement_type IS NULL)  -- Avoid duplicate byte counting in parent and children jobs.
GROUP BY
  period_start
ORDER BY
  period_start DESC;
```

結果大致如下：

```
+-----------------------+---------------------+--------------------------+------------------------------+
|     period_start      | period_slot_seconds | estimated_slots_assigned | estimated_slots_max_assigned |
+-----------------------+---------------------+--------------------------+------------------------------+
|2021-06-08 21:33:59 UTC|       100.000       |         100              |           100                |
|2021-06-08 21:33:58 UTC|        96.753       |         100              |           100                |
|2021-06-08 21:33:57 UTC|        41.668       |         100              |           100                |
+-----------------------+---------------------+--------------------------+------------------------------+
```

#### 範例：依預留項目劃分的運算單元用量

以下範例顯示過去 1 天內每個預訂項目每秒的運算單元用量：

```
SELECT
  jobs.period_start,
  res.reservation_id,
  SUM(jobs.period_slot_ms) / 1000 AS period_slot_seconds,
  ANY_VALUE(COALESCE(s.slots_assigned, res.slots_assigned)) AS estimated_slots_assigned,
  ANY_VALUE(COALESCE(s.slots_max_assigned, res.slots_max_assigned)) AS estimated_slots_max_assigned
FROM `region-us`.INFORMATION_SCHEMA.JOBS_TIMELINE_BY_ORGANIZATION jobs
JOIN `region-us`.INFORMATION_SCHEMA.RESERVATIONS_TIMELINE res
  ON jobs.reservation_id = res.reservation_id
  AND TIMESTAMP_TRUNC(jobs.period_start, MINUTE) = res.period_start
LEFT JOIN UNNEST(res.per_second_details) s
  ON jobs.period_start = s.start_time
WHERE
  jobs.job_creation_time
      BETWEEN TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 1 DAY)
          AND CURRENT_TIMESTAMP()
  AND res.period_start
      BETWEEN TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 1 DAY)
          AND CURRENT_TIMESTAMP()
  AND (jobs.statement_type != "SCRIPT" OR jobs.statement_type IS NULL)  -- Avoid duplicate byte counting in parent and children jobs.
GROUP BY
  period_start,
  reservation_id
ORDER BY
  period_start DESC,
  reservation_id;
```

結果大致如下：

```
+-----------------------+----------------+---------------------+--------------------------+------------------------------+
|     period_start      | reservation_id | period_slot_seconds | estimated_slots_assigned | estimated_slots_max_assigned |
+-----------------------+----------------+---------------------+--------------------------+------------------------------+
|2021-06-08 21:33:59 UTC|     prod01     |       100.000       |             100          |              100             |
|2021-06-08 21:33:58 UTC|     prod02     |       177.201       |             200          |              500             |
|2021-06-08 21:32:57 UTC|     prod01     |        96.753       |             100          |              100             |
|2021-06-08 21:32:56 UTC|     prod02     |       182.329       |             200          |              500             |
+-----------------------+----------------+---------------------+--------------------------+------------------------------+
```




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-02 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-02 (世界標準時間)。"],[],[]]