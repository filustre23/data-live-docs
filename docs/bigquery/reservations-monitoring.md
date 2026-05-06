Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 監控 BigQuery 保留項目

BigQuery 管理員可以查看專案和預留運算單元用量，監控專案中的預留項目，也可以查看以容量為準的帳單。

## 查看專案和預留項目運算單元用量

您可以透過下列方式查看專案和預訂運算單元用量：

* **`INFORMATION_SCHEMA` 次觀看。**如要擷取專案和預留項目使用量資訊，請查詢 [`INFORMATION_SCHEMA.JOBS*` 檢視區塊](https://docs.cloud.google.com/bigquery/docs/information-schema-jobs?hl=zh-tw#examples)。

  `INFORMATION_SCHEMA.JOBS*` 檢視區塊中的 [`reservation_id`](https://docs.cloud.google.com/bigquery/docs/information-schema-jobs?hl=zh-tw#schema) 欄位包含預留項目名稱。
* **Google Cloud console.** Google Cloud 控制台會顯示圖表，說明時段使用情形。詳情請參閱「[使用管理資源圖表](https://docs.cloud.google.com/bigquery/docs/admin-resource-charts?hl=zh-tw)」。
* **稽核記錄**。使用[稽核記錄](https://docs.cloud.google.com/bigquery/docs/reference/auditlogs?hl=zh-tw)查看有關時段用量的指標。
* **`Jobs` 方法。**使用 [`Jobs` API 方法](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs?hl=zh-tw)，查看作業的時段用量指標。
* **Cloud Monitoring**。您可以使用 [Cloud Monitoring](https://docs.cloud.google.com/bigquery/docs/monitoring-dashboard?hl=zh-tw) 建立資訊主頁，監控已分配的時段。透過 Cloud Monitoring 資訊主頁，您可以查看每個預訂和每個作業類型的運算單元用量，以及預訂中的所有專案。如要查看從預留項目取用容量的所有專案的時段用量指標，您必須明確將這些取用容量的專案新增至監控指標的專案[指標範圍](https://docs.cloud.google.com/monitoring/settings?hl=zh-tw)。如要進一步瞭解 Cloud Monitoring 資訊主頁可用的指標，請參閱「[可供視覺化的指標](https://docs.cloud.google.com/bigquery/docs/monitoring-dashboard?hl=zh-tw#metrics)」。

**注意：** 由於 BigQuery 為預留項目佈建資源的方式，因此使用的運算單元數量可能會高於預留的運算單元數量。系統不會針對超出預留運算單元數量的運算單元向您收費。

## 查看以容量為準的帳單

如要即時查看以容量為準的帳單，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「帳單」頁面。

   [前往「**帳單**」](https://console.cloud.google.com/billing?hl=zh-tw)。
2. 選取要查看帳單的帳單帳戶專案。
3. 前往「報表」部分，然後在「篩選器」部分中執行下列操作：

   1. 在「服務」清單中，選取「BigQuery」，然後選取所有適用的項目。
   2. 從「SKU」清單中選取「所有 SKU」。

**注意：** BigQuery 年約和三年約的價格是以月為單位計算。您的帳單不會因月份天數的不同而改變。如果您的時段用量維持不變，每月費率也會相同。

## 預留費用歸因

這項功能可讓您將預留費用歸因於使用預留項目的任何專案，並追溯至特定查詢用量。這樣一來，每個專案的淨成本就會更準確。

所有 [BigQuery Reservations API](https://docs.cloud.google.com/bigquery/docs/reservations-commitments?hl=zh-tw#enabling-reservations-api) 客戶的 Cloud Billing 資料中，都會有「分析配額歸因」行項目。這項委刊項會顯示在「帳單」頁面和 Cloud Billing 匯出資料中。

這個委刊項會顯示每個專案使用的時段時數。這不會產生任何費用，也不會影響月結單總計。

## 稽核記錄

建立、刪除及更新與 [BigQuery 預留項目](https://docs.cloud.google.com/bigquery/docs/reservations-concepts?hl=zh-tw)相關的資源時，系統會在專案擁有者的稽核記錄中記錄這些作業。詳情請參閱「[稽核記錄](https://docs.cloud.google.com/bigquery/docs/reference/auditlogs?hl=zh-tw#auditlog_format)」。

## 使用資訊結構定義監控自動調度資源

您可以使用下列 SQL 指令碼，查看特定版本的計費時段秒數。您必須在建立預訂的專案中執行這些指令碼。第一個指令碼顯示`commitment_plan`涵蓋的計費廣告空間秒數，第二個指令碼則顯示承諾未涵蓋的計費廣告空間秒數。

您只需要設定三個變數的值，即可執行這些指令碼：

* `start_time`
* `end_time`
* `edition_to_check`

這些指令碼有下列注意事項：

* 資料保留期限結束時，系統會從資訊結構定義檢視畫面中移除已刪除的預訂和運算資源承諾。指定最近的時間範圍，確保該範圍不含已刪除的預訂和承諾，以取得正確結果。
* 由於四捨五入的小誤差，指令碼結果可能與帳單不完全一致。

下列指令碼會彙整各版本的自動調度資源配額。

#### 展開即可查看計算各版本自動調度資源時數的指令碼。

```
SELECT
  edition,
  SUM(s.autoscale_current_slots) AS autoscale_slot_seconds
FROM
  `region-us.INFORMATION_SCHEMA.RESERVATIONS_TIMELINE` m
JOIN
  m.per_second_details s
WHERE
  period_start BETWEEN '2025-09-28'
  AND '2025-09-29'
GROUP BY
  edition
ORDER BY
  edition
```

下列指令碼會彙整每個預留項目的自動調度資源配額。

#### 展開即可查看計算每個預訂的自動調度時段秒數的指令碼。

```
select reservation_id, sum(s.autoscale_current_slots) as autoscale_slot_seconds
from `region-us.INFORMATION_SCHEMA.RESERVATIONS_TIMELINE` m
LEFT JOIN m.per_second_details s
WHERE period_start between '2025-09-28' and '2025-09-29'
group by reservation_id
order by reservation_id
```

下列指令碼會檢查特定版本的承諾涵蓋的空位用量。

#### 展開即可查看從承諾計算廣告空間秒數的指令碼。

```
DECLARE start_time,end_time TIMESTAMP;

DECLARE
  edition_to_check STRING;

/* Google uses Pacific Time to calculate the billing period for all customers,
regardless of their time zone. Use the following format if you want to match the
billing report. Change the start_time and end_time values to match the desired
window. */

/* The following three variables (start_time, end_time, and edition_to_check)
are the only variables that you need to set in the script.

During daylight savings time, the start_time and end_time variables should
follow this format: 2024-02-20 00:00:00-08. */

SET start_time = "2023-07-20 00:00:00-07";
SET end_time = "2023-07-28 00:00:00-07";
SET edition_to_check = 'ENTERPRISE';

/* The following function returns the slot seconds for the time window between
two capacity changes. For example, if there are 100 slots between (2023-06-01
10:00:00, 2023-06-01 11:00:00), then during that window the total slot seconds
will be 100 * 3600.

This script calculates a specific window (based on the variables defined above),
which is why the following script includes script_start_timestamp_unix_millis
and script_end_timestamp_unix_millis. */

CREATE TEMP FUNCTION
GetSlotSecondsBetweenChanges(
  slots FLOAT64,
  range_begin_timestamp_unix_millis FLOAT64,
  range_end_timestamp_unix_millis FLOAT64,
  script_start_timestamp_unix_millis FLOAT64,
  script_end_timestamp_unix_millis FLOAT64)
RETURNS INT64
LANGUAGE js
AS r"""
    if (script_end_timestamp_unix_millis < range_begin_timestamp_unix_millis || script_start_timestamp_unix_millis > range_end_timestamp_unix_millis) {
      return 0;
    }
    var begin = Math.max(script_start_timestamp_unix_millis, range_begin_timestamp_unix_millis)
    var end = Math.min(script_end_timestamp_unix_millis, range_end_timestamp_unix_millis)
    return slots * Math.ceil((end - begin) / 1000.0)
""";

/*
Sample CAPACITY_COMMITMENT_CHANGES data (unrelated columns ignored):
+---------------------+------------------------+-----------------+--------+------------+--------+
|  change_timestamp   | capacity_commitment_id | commitment_plan | state  | slot_count | action |
+---------------------+------------------------+-----------------+--------+------------+--------+
| 2023-07-20 19:30:27 | 12954109101902401697   | ANNUAL          | ACTIVE |        100 | CREATE |
| 2023-07-27 22:29:21 | 11445583810276646822   | FLEX            | ACTIVE |        100 | CREATE |
| 2023-07-27 23:10:06 | 7341455530498381779    | MONTHLY         | ACTIVE |        100 | CREATE |
| 2023-07-27 23:11:06 | 7341455530498381779    | FLEX            | ACTIVE |        100 | UPDATE |

The last row indicates a special change from MONTHLY to FLEX, which happens
because of commercial migration.

*/

WITH
  /*
  Information containing which commitment might have plan
  updated (e.g. renewal or commercial migration). For example:
  +------------------------+------------------+--------------------+--------+------------+--------+-----------+----------------------------+
  |  change_timestamp   | capacity_commitment_id | commitment_plan | state  | slot_count | action | next_plan | next_plan_change_timestamp |
  +---------------------+------------------------+-----------------+--------+------------+--------+-----------+----------------------------+
  | 2023-07-20 19:30:27 | 12954109101902401697   | ANNUAL          | ACTIVE |        100 | CREATE | ANNUAL    |        2023-07-20 19:30:27 |
  | 2023-07-27 22:29:21 | 11445583810276646822   | FLEX            | ACTIVE |        100 | CREATE | FLEX      |        2023-07-27 22:29:21 |
  | 2023-07-27 23:10:06 | 7341455530498381779    | MONTHLY         | ACTIVE |        100 | CREATE | FLEX      |        2023-07-27 23:11:06 |
  | 2023-07-27 23:11:06 | 7341455530498381779    | FLEX            | ACTIVE |        100 | UPDATE | FLEX      |        2023-07-27 23:11:06 |
  */
  commitments_with_next_plan AS (
    SELECT
      *,
      IFNULL(
        LEAD(commitment_plan)
          OVER (
            PARTITION BY capacity_commitment_id ORDER BY change_timestamp ASC
          ),
        commitment_plan)
        next_plan,
      IFNULL(
        LEAD(change_timestamp)
          OVER (
            PARTITION BY capacity_commitment_id ORDER BY change_timestamp ASC
          ),
        change_timestamp)
        next_plan_change_timestamp
    FROM
      `region-us.INFORMATION_SCHEMA.CAPACITY_COMMITMENT_CHANGES_BY_PROJECT`
  ),

  /*
  Insert a 'DELETE' action for those with updated plans. The FLEX commitment
  '7341455530498381779' is has no 'CREATE' action, and is instead labeled as an
  'UPDATE' action.

  For example:
  +---------------------+------------------------+-----------------+--------+------------+--------+
  |  change_timestamp   | capacity_commitment_id | commitment_plan | state  | slot_count | action |
  +---------------------+------------------------+-----------------+--------+------------+--------+
  | 2023-07-20 19:30:27 | 12954109101902401697   | ANNUAL          | ACTIVE |        100 | CREATE |
  | 2023-07-27 22:29:21 | 11445583810276646822   | FLEX            | ACTIVE |        100 | CREATE |
  | 2023-07-27 23:10:06 | 7341455530498381779    | MONTHLY         | ACTIVE |        100 | CREATE |
  | 2023-07-27 23:11:06 | 7341455530498381779    | FLEX            | ACTIVE |        100 | UPDATE |
  | 2023-07-27 23:11:06 | 7341455530498381779    | MONTHLY         | ACTIVE |        100 | DELETE |
  */

  capacity_changes_with_additional_deleted_event_for_changed_plan AS (
    SELECT
      next_plan_change_timestamp AS change_timestamp,
      project_id,
      project_number,
      capacity_commitment_id,
      commitment_plan,
      state,
      slot_count,
      'DELETE' AS action,
      commitment_start_time,
      commitment_end_time,
      failure_status,
      renewal_plan,
      user_email,
      edition,
      is_flat_rate,
    FROM commitments_with_next_plan
    WHERE commitment_plan <> next_plan
    UNION ALL
    SELECT * FROM `region-us.INFORMATION_SCHEMA.CAPACITY_COMMITMENT_CHANGES_BY_PROJECT`
  ),

  /*
  The committed_slots change the history. For example:
  +---------------------+------------------------+------------------+-----------------+
  |  change_timestamp   | capacity_commitment_id | slot_count_delta | commitment_plan |
  +---------------------+------------------------+------------------+-----------------+
  | 2023-07-20 19:30:27 | 12954109101902401697   |              100 | ANNUAL          |
  | 2023-07-27 22:29:21 | 11445583810276646822   |              100 | FLEX            |
  | 2023-07-27 23:10:06 | 7341455530498381779    |              100 | MONTHLY         |
  | 2023-07-27 23:11:06 | 7341455530498381779    |             -100 | MONTHLY         |
  | 2023-07-27 23:11:06 | 7341455530498381779    |              100 | FLEX            |
  */

  capacity_commitment_slot_data AS (
    SELECT
      change_timestamp,
      capacity_commitment_id,
      CASE
        WHEN action = "CREATE" OR action = "UPDATE"
          THEN
            IFNULL(
              IF(
                LAG(action)
                  OVER (
                    PARTITION BY capacity_commitment_id ORDER BY change_timestamp ASC, action ASC
                  )
                  IN UNNEST(['CREATE', 'UPDATE']),
                slot_count - LAG(slot_count)
                  OVER (
                    PARTITION BY capacity_commitment_id ORDER BY change_timestamp ASC, action ASC
                  ),
                slot_count),
              slot_count)
        ELSE
          IF(
            LAG(action)
              OVER (PARTITION BY capacity_commitment_id ORDER BY change_timestamp ASC, action ASC)
              IN UNNEST(['CREATE', 'UPDATE']),
            -1 * slot_count,
            0)
        END
        AS slot_count_delta,
      commitment_plan
    FROM
      capacity_changes_with_additional_deleted_event_for_changed_plan
    WHERE
      state = "ACTIVE"
      AND edition = edition_to_check
      AND change_timestamp <= end_time
  ),

  /*
  The total_committed_slots history for each plan. For example:
  +---------------------+---------------+-----------------+
  |  change_timestamp   | capacity_slot | commitment_plan |
  +---------------------+---------------+-----------------+
  | 2023-07-20 19:30:27 |           100 | ANNUAL          |
  | 2023-07-27 22:29:21 |           100 | FLEX            |
  | 2023-07-27 23:10:06 |           100 | MONTHLY         |
  | 2023-07-27 23:11:06 |             0 | MONTHLY         |
  | 2023-07-27 23:11:06 |           200 | FLEX            |
  */

  running_capacity_commitment_slot_data AS (
    SELECT
      change_timestamp,
      SUM(slot_count_delta)
        OVER (
          PARTITION BY commitment_plan
          ORDER BY change_timestamp
          RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
        )
        AS capacity_slot,
      commitment_plan,
    FROM
      capacity_commitment_slot_data
  ),

  /*

  The slot_seconds between each changes, partitioned by each plan. For example:
  +---------------------+--------------+-----------------+
  |  change_timestamp   | slot_seconds | commitment_plan |
  +---------------------+--------------+-----------------+
  | 2023-07-20 19:30:27 |     64617300 | ANNUAL          |
  | 2023-07-27 22:29:21 |       250500 | FLEX            |
  | 2023-07-27 23:10:06 |         6000 | MONTHLY         |
  | 2023-07-27 23:11:06 |            0 | MONTHLY         |
  | 2023-07-27 23:11:06 |      5626800 | FLEX            |
  */

  slot_seconds_data AS (
    SELECT
      change_timestamp,
      GetSlotSecondsBetweenChanges(
        capacity_slot,
        UNIX_MILLIS(change_timestamp),
        UNIX_MILLIS(
          IFNULL(
            LEAD(change_timestamp)
              OVER (PARTITION BY commitment_plan ORDER BY change_timestamp ASC),
            CURRENT_TIMESTAMP())),
        UNIX_MILLIS(start_time),
        UNIX_MILLIS(end_time)) AS slot_seconds,
      commitment_plan,
    FROM
      running_capacity_commitment_slot_data
    WHERE
      change_timestamp <= end_time
  )

/*

The final result is similar to the following:
+-----------------+--------------------+
| commitment_plan | total_slot_seconds |
+-----------------+--------------------+
| ANNUAL          |           64617300 |
| MONTHLY         |               6000 |
| FLEX            |            5877300 |
*/

SELECT
  commitment_plan,
  SUM(slot_seconds) AS total_slot_seconds
FROM
  slot_seconds_data
GROUP BY
  commitment_plan
```

下列指令碼會檢查特定版本的約定未涵蓋的空位使用情形。這項用量包含兩種運算單元：已調度運算單元和未納入承諾的基準運算單元。

#### 展開即可查看計算承諾未涵蓋的時段秒數的指令碼

```
/*
This script has several parts:
1. Calculate the baseline and scaled slots for reservations
2. Calculate the committed slots
3. Join the two results above to calculate the baseline not covered by committed
   slots
4. Aggregate the number
*/

-- variables
DECLARE start_time, end_time TIMESTAMP;

DECLARE
  edition_to_check STRING;

/* Google uses Pacific Time to calculate the billing period for all customers,
regardless of their time zone. Use the following format if you want to match the
billing report. Change the start_time and end_time values to match the desired
window. */

/* The following three variables (start_time, end_time, and edition_to_check)
are the only variables that you need to set in the script.

During daylight savings time, the start_time and end_time variables should
follow this format: 2024-02-20 00:00:00-08. */

SET start_time = "2023-07-20 00:00:00-07";
SET end_time = "2023-07-28 00:00:00-07";
SET edition_to_check = 'ENTERPRISE';

/*
The following function returns the slot seconds for the time window between
two capacity changes. For example, if there are 100 slots between (2023-06-01
10:00:00, 2023-06-01 11:00:00), then during that window the total slot seconds
will be 100 * 3600.

This script calculates a specific window (based on the variables defined above),
which is why the following script includes script_start_timestamp_unix_millis
and script_end_timestamp_unix_millis. */

CREATE TEMP FUNCTION GetSlotSecondsBetweenChanges(
  slots FLOAT64,
  range_begin_timestamp_unix_millis FLOAT64,
  range_end_timestamp_unix_millis FLOAT64,
  script_start_timestamp_unix_millis FLOAT64,
  script_end_timestamp_unix_millis FLOAT64)
RETURNS INT64
LANGUAGE js
AS r"""
    if (script_end_timestamp_unix_millis < range_begin_timestamp_unix_millis || script_start_timestamp_unix_millis > range_end_timestamp_unix_millis) {
      return 0;
    }
    var begin = Math.max(script_start_timestamp_unix_millis, range_begin_timestamp_unix_millis)
    var end = Math.min(script_end_timestamp_unix_millis, range_end_timestamp_unix_millis)
    return slots * Math.ceil((end - begin) / 1000.0)
""";
/*
Sample RESERVATION_CHANGES data (unrelated columns ignored):
+---------------------+------------------+--------+---------------+---------------+
|  change_timestamp   | reservation_name | action | slot_capacity | current_slots |
+---------------------+------------------+--------+---------------+---------------+
| 2023-07-27 22:24:15 | res1             | CREATE |           300 |             0 |
| 2023-07-27 22:25:21 | res1             | UPDATE |           300 |           180 |
| 2023-07-27 22:39:14 | res1             | UPDATE |           300 |           100 |
| 2023-07-27 22:40:20 | res2             | CREATE |           300 |             0 |
| 2023-07-27 22:54:18 | res2             | UPDATE |           300 |           120 |
| 2023-07-27 22:55:23 | res1             | UPDATE |           300 |             0 |

Sample CAPACITY_COMMITMENT_CHANGES data (unrelated columns ignored):
+---------------------+------------------------+-----------------+--------+------------+--------+
|  change_timestamp   | capacity_commitment_id | commitment_plan | state  | slot_count | action |
+---------------------+------------------------+-----------------+--------+------------+--------+
| 2023-07-20 19:30:27 | 12954109101902401697   | ANNUAL          | ACTIVE |        100 | CREATE |
| 2023-07-27 22:29:21 | 11445583810276646822   | FLEX            | ACTIVE |        100 | CREATE |
| 2023-07-27 23:10:06 | 7341455530498381779    | MONTHLY         | ACTIVE |        100 | CREATE |
*/

WITH
  /*
  The scaled_slots & baseline change history:
  +---------------------+------------------+------------------------------+---------------------+
  |  change_timestamp   | reservation_name | autoscale_current_slot_delta | baseline_slot_delta |
  +---------------------+------------------+------------------------------+---------------------+
  | 2023-07-27 22:24:15 | res1             |                            0 |                 300 |
  | 2023-07-27 22:25:21 | res1             |                          180 |                   0 |
  | 2023-07-27 22:39:14 | res1             |                          -80 |                   0 |
  | 2023-07-27 22:40:20 | res2             |                            0 |                 300 |
  | 2023-07-27 22:54:18 | res2             |                          120 |                   0 |
  | 2023-07-27 22:55:23 | res1             |                         -100 |                   0 |
  */
  reservation_slot_data AS (
    SELECT
      change_timestamp,
      reservation_name,
      CASE action
        WHEN "CREATE" THEN autoscale.current_slots
        WHEN "UPDATE"
          THEN
            IFNULL(
              autoscale.current_slots - LAG(autoscale.current_slots)
                OVER (
                  PARTITION BY project_id, reservation_name
                  ORDER BY change_timestamp ASC, action ASC
                ),
              IFNULL(
                autoscale.current_slots,
                IFNULL(
                  -1 * LAG(autoscale.current_slots)
                    OVER (
                      PARTITION BY project_id, reservation_name
                      ORDER BY change_timestamp ASC, action ASC
                    ),
                  0)))
        WHEN "DELETE"
          THEN
            IF(
              LAG(action)
                OVER (
                  PARTITION BY project_id, reservation_name
                  ORDER BY change_timestamp ASC, action ASC
                )
                IN UNNEST(['CREATE', 'UPDATE']),
              -1 * autoscale.current_slots,
              0)
        END
        AS autoscale_current_slot_delta,
      CASE action
        WHEN "CREATE" THEN slot_capacity
        WHEN "UPDATE"
          THEN
            IFNULL(
              slot_capacity - LAG(slot_capacity)
                OVER (
                  PARTITION BY project_id, reservation_name
                  ORDER BY change_timestamp ASC, action ASC
                ),
              IFNULL(
                slot_capacity,
                IFNULL(
                  -1 * LAG(slot_capacity)
                    OVER (
                      PARTITION BY project_id, reservation_name
                      ORDER BY change_timestamp ASC, action ASC
                    ),
                  0)))
        WHEN "DELETE"
          THEN
            IF(
              LAG(action)
                OVER (
                  PARTITION BY project_id, reservation_name
                  ORDER BY change_timestamp ASC, action ASC
                )
                IN UNNEST(['CREATE', 'UPDATE']),
              -1 * slot_capacity,
              0)
        END
        AS baseline_slot_delta,
    FROM
      `region-us.INFORMATION_SCHEMA.RESERVATION_CHANGES`
    WHERE
      edition = edition_to_check
      AND change_timestamp <= end_time
  ),

  -- Convert the above to running total
  /*
  +---------------------+-------------------------+----------------+
  |  change_timestamp   | autoscale_current_slots | baseline_slots |
  +---------------------+-------------------------+----------------+
  | 2023-07-27 22:24:15 |                       0 |            300 |
  | 2023-07-27 22:25:21 |                     180 |            300 |
  | 2023-07-27 22:39:14 |                     100 |            300 |
  | 2023-07-27 22:40:20 |                     100 |            600 |
  | 2023-07-27 22:54:18 |                     220 |            600 |
  | 2023-07-27 22:55:23 |                     120 |            600 |
  */
  running_reservation_slot_data AS (
    SELECT
      change_timestamp,
      SUM(autoscale_current_slot_delta)
        OVER (ORDER BY change_timestamp RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)
        AS autoscale_current_slots,
      SUM(baseline_slot_delta)
        OVER (ORDER BY change_timestamp RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)
        AS baseline_slots,
    FROM
      reservation_slot_data
  ),

  /*
  The committed_slots change history. For example:
  +---------------------+------------------------+------------------+
  |  change_timestamp   | capacity_commitment_id | slot_count_delta |
  +---------------------+------------------------+------------------+
  | 2023-07-20 19:30:27 | 12954109101902401697   |              100 |
  | 2023-07-27 22:29:21 | 11445583810276646822   |              100 |
  | 2023-07-27 23:10:06 | 7341455530498381779    |              100 |
  */
  capacity_commitment_slot_data AS (
    SELECT
      change_timestamp,
      capacity_commitment_id,
      CASE
        WHEN action = "CREATE" OR action = "UPDATE"
          THEN
            IFNULL(
              IF(
                LAG(action)
                  OVER (
                    PARTITION BY capacity_commitment_id ORDER BY change_timestamp ASC, action ASC
                  )
                  IN UNNEST(['CREATE', 'UPDATE']),
                slot_count - LAG(slot_count)
                  OVER (
                    PARTITION BY capacity_commitment_id ORDER BY change_timestamp ASC, action ASC
                  ),
                slot_count),
              slot_count)
        ELSE
          IF(
            LAG(action)
              OVER (PARTITION BY capacity_commitment_id ORDER BY change_timestamp ASC, action ASC)
              IN UNNEST(['CREATE', 'UPDATE']),
            -1 * slot_count,
            0)
        END
        AS slot_count_delta
    FROM
      `region-us.INFORMATION_SCHEMA.CAPACITY_COMMITMENT_CHANGES_BY_PROJECT`
    WHERE
      state = "ACTIVE"
      AND edition = edition_to_check
      AND change_timestamp <= end_time
  ),

  /*
  The total_committed_slots history. For example:
  +---------------------+---------------+
  |  change_timestamp   | capacity_slot |
  +---------------------+---------------+
  | 2023-07-20 19:30:27 |           100 |
  | 2023-07-27 22:29:21 |           200 |
  | 2023-07-27 23:10:06 |           300 |
  */
  running_capacity_commitment_slot_data AS (
    SELECT
      change_timestamp,
      SUM(slot_count_delta)
        OVER (ORDER BY change_timestamp RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)
        AS capacity_slot
    FROM
      capacity_commitment_slot_data
  ),

  /* Add next_change_timestamp to the above data,
   which will be used when joining with reservation data. For example:
  +---------------------+-----------------------+---------------+
  |  change_timestamp   | next_change_timestamp | capacity_slot |
  +---------------------+-----------------------+---------------+
  | 2023-07-20 19:30:27 |   2023-07-27 22:29:21 |           100 |
  | 2023-07-27 22:29:21 |   2023-07-27 23:10:06 |           200 |
  | 2023-07-27 23:10:06 |   2023-07-31 00:14:37 |           300 |
  */
  running_capacity_commitment_slot_data_with_next_change AS (
    SELECT
      change_timestamp,
      IFNULL(LEAD(change_timestamp) OVER (ORDER BY change_timestamp ASC), CURRENT_TIMESTAMP())
        AS next_change_timestamp,
      capacity_slot
    FROM
      running_capacity_commitment_slot_data
  ),

  /*
  Whenever we have a change in reservations or commitments,
  the scaled_slots_and_baseline_not_covered_by_commitments will be changed.
  Hence we get a collection of all the change_timestamp from both tables.
  +---------------------+
  |  change_timestamp   |
  +---------------------+
  | 2023-07-20 19:30:27 |
  | 2023-07-27 22:24:15 |
  | 2023-07-27 22:25:21 |
  | 2023-07-27 22:29:21 |
  | 2023-07-27 22:39:14 |
  | 2023-07-27 22:40:20 |
  | 2023-07-27 22:54:18 |
  | 2023-07-27 22:55:23 |
  | 2023-07-27 23:10:06 |
  */
  merged_timestamp AS (
    SELECT
      change_timestamp
    FROM
      running_reservation_slot_data
    UNION DISTINCT
    SELECT
      change_timestamp
    FROM
      running_capacity_commitment_slot_data
  ),

  /*
  Change running reservation-slots and make sure we have one row when commitment changes.
  +---------------------+-------------------------+----------------+
  |  change_timestamp   | autoscale_current_slots | baseline_slots |
  +---------------------+-------------------------+----------------+
  | 2023-07-20 19:30:27 |                       0 |              0 |
  | 2023-07-27 22:24:15 |                       0 |            300 |
  | 2023-07-27 22:25:21 |                     180 |            300 |
  | 2023-07-27 22:29:21 |                     180 |            300 |
  | 2023-07-27 22:39:14 |                     100 |            300 |
  | 2023-07-27 22:40:20 |                     100 |            600 |
  | 2023-07-27 22:54:18 |                     220 |            600 |
  | 2023-07-27 22:55:23 |                     120 |            600 |
  | 2023-07-27 23:10:06 |                     120 |            600 |
  */
  running_reservation_slot_data_with_merged_timestamp AS (
    SELECT
      change_timestamp,
      IFNULL(
        autoscale_current_slots,
        IFNULL(
          LAST_VALUE(autoscale_current_slots IGNORE NULLS) OVER (ORDER BY change_timestamp ASC), 0))
        AS autoscale_current_slots,
      IFNULL(
        baseline_slots,
        IFNULL(LAST_VALUE(baseline_slots IGNORE NULLS) OVER (ORDER BY change_timestamp ASC), 0))
        AS baseline_slots
    FROM
      running_reservation_slot_data
    RIGHT JOIN
      merged_timestamp
      USING (change_timestamp)
  ),

  /*
  Join the above, so that we will know the number for baseline not covered by commitments.
  +---------------------+-----------------------+-------------------------+------------------------------------+
  |  change_timestamp   | next_change_timestamp | autoscale_current_slots | baseline_not_covered_by_commitment |
  +---------------------+-----------------------+-------------------------+------------------------------------+
  | 2023-07-20 19:30:27 |   2023-07-27 22:24:15 |                       0 |                                  0 |
  | 2023-07-27 22:24:15 |   2023-07-27 22:25:21 |                       0 |                                200 |
  | 2023-07-27 22:25:21 |   2023-07-27 22:29:21 |                     180 |                                200 |
  | 2023-07-27 22:29:21 |   2023-07-27 22:39:14 |                     180 |                                100 |
  | 2023-07-27 22:39:14 |   2023-07-27 22:40:20 |                     100 |                                100 |
  | 2023-07-27 22:40:20 |   2023-07-27 22:54:18 |                     100 |                                400 |
  | 2023-07-27 22:54:18 |   2023-07-27 22:55:23 |                     220 |                                400 |
  | 2023-07-27 22:55:23 |   2023-07-27 23:10:06 |                     120 |                                400 |
  | 2023-07-27 23:10:06 |   2023-07-31 00:16:07 |                     120 |                                300 |
  */
  scaled_slots_and_baseline_not_covered_by_commitments AS (
    SELECT
      r.change_timestamp,
      IFNULL(LEAD(r.change_timestamp) OVER (ORDER BY r.change_timestamp ASC), CURRENT_TIMESTAMP())
        AS next_change_timestamp,
      r.autoscale_current_slots,
      IF(
        r.baseline_slots - IFNULL(c.capacity_slot, 0) > 0,
        r.baseline_slots - IFNULL(c.capacity_slot, 0),
        0) AS baseline_not_covered_by_commitment
    FROM
      running_reservation_slot_data_with_merged_timestamp r
    LEFT JOIN
      running_capacity_commitment_slot_data_with_next_change c
      ON
        r.change_timestamp >= c.change_timestamp
        AND r.change_timestamp < c.next_change_timestamp
  ),

  /*
  The slot_seconds between each changes. For example:
  +---------------------+--------------------+
  |  change_timestamp   | slot_seconds |
  +---------------------+--------------+
  | 2023-07-20 19:30:27 |            0 |
  | 2023-07-27 22:24:15 |        13400 |
  | 2023-07-27 22:25:21 |        91580 |
  | 2023-07-27 22:29:21 |       166320 |
  | 2023-07-27 22:39:14 |        13200 |
  | 2023-07-27 22:40:20 |       419500 |
  | 2023-07-27 22:54:18 |        40920 |
  | 2023-07-27 22:55:23 |       459160 |
  | 2023-07-27 23:10:06 |     11841480 |
  */
  slot_seconds_data AS (
    SELECT
      change_timestamp,
      GetSlotSecondsBetweenChanges(
        autoscale_current_slots + baseline_not_covered_by_commitment,
        UNIX_MILLIS(change_timestamp),
        UNIX_MILLIS(next_change_timestamp),
        UNIX_MILLIS(start_time),
        UNIX_MILLIS(end_time)) AS slot_seconds
    FROM
      scaled_slots_and_baseline_not_covered_by_commitments
    WHERE
      change_timestamp <= end_time AND next_change_timestamp > start_time
  )

/*
Final result for this example:
+--------------------+
| total_slot_seconds |
+--------------------+
|           13045560 |
*/
SELECT
  SUM(slot_seconds) AS total_slot_seconds
FROM
  slot_seconds_data
```

## 疑難排解

本節說明如何解決監控 BigQuery 預留位置和配額用量時的常見問題。

### 運算單元用量指標不一致 `INFORMATION_SCHEMA`

如果資源圖表中的時段使用量指標與 `INFORMATION_SCHEMA` 資料不一致，請嘗試下列做法：

* **降低精細度。**將圖表精細程度變更為 1 秒間隔，而非 1 小時間隔。
* **調整匯總。**請確保您使用的匯總方法與資源圖表和 `INFORMATION_SCHEMA` 資料一致。舉例來說，如要更準確地反映資源圖表中的尖峰用量，請將指標彙整方式一律改為 p99 或 p90。

### 停用閒置運算單元後，系統會顯示借用的運算單元

即使已為一或多個預訂設定 `ignore_idle_slots=true`，監控圖表仍可能會顯示 `borrowed_slots` 的非零值。這項設定可防止預留項目*借用*閒置運算單元，但不會阻止預留項目將未使用的運算單元*借給*其他預留項目。

在下列情況下，系統會顯示這些借用的時段：

* **借用給其他預留項目：**如果預留項目設為 `ignore_idle_slots=true`，即可將未使用的基準運算單元借用給相同版本中*允許*借用閒置運算單元的其他預留項目 (`ignore_idle_slots=false`)。如果版本中的所有預留項目都設為 `ignore_idle_slots=true`，則這些預留項目不會共用閒置運算單元。

  舉例來說，假設保留項目 A 有 100 個運算單元，用量為 0，且已設定 `ignore_idle_slots=true`。保留項目 B 位於相同版本和專案中，有 100 個運算單元，工作負載需要 150 個運算單元，且已設定 `ignore_idle_slots=false`。預留項目 B 可以從預留項目 A 借用 50 個閒置運算單元，以滿足需求。發生這種情況時，監控圖表會回報預留項目 A 為 50 `lent_slots`，預留項目 B 為 50 `borrowed_slots`。
* **用量超出容量：**如果預留項目的運算單元用量暫時超出容量 (基準值 + 自動調度運算單元)，監控圖表會將這項差異顯示為 `borrowed_slots`。即使預訂包含 `ignore_idle_slots=true` 也可能發生這種情況。

運算單元用量有時可能會超過基準運算單元和調度運算單元的總和。如果運算單元用量超過基準運算單元加上縮放運算單元，您就不必支付相關費用。

### 預留項目用盡前，借用的運算單元會顯示

監控資訊主頁會使用取樣資料，因此可能無法準確反映取樣間隔內使用時段的確切時間。

如要更準確地分析時段使用情形，請查詢與閒置時段相關的資料欄，例如 [`INFORMATION_SCHEMA.RESERVATIONS_TIMELINE` 檢視表](https://docs.cloud.google.com/bigquery/docs/information-schema-reservation-timeline?hl=zh-tw#schema)中的 `borrowed_slots` 和 `lent_slots` 資料欄。

## 後續步驟

* 瞭解[容量承諾使用方案](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#slot_commitments)。
* 瞭解如何[使用管理資源圖表](https://docs.cloud.google.com/bigquery/docs/admin-resource-charts?hl=zh-tw)。
* 瞭解 [BigQuery 定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-02 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-02 (世界標準時間)。"],[],[]]