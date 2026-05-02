* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [參考資料](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# JOBS\_TIMELINE 檢視畫面

`INFORMATION_SCHEMA.JOBS_TIMELINE` 檢視畫面包含目前專案中提交的所有工作，以時間切片為單位，提供近乎即時的 BigQuery 中繼資料。這個檢視畫面會顯示目前執行中和已完成的工作。

**注意：** 檢視區塊名稱 `INFORMATION_SCHEMA.JOBS_TIMELINE` 和 `INFORMATION_SCHEMA.JOBS_TIMELINE_BY_PROJECT` 是同義詞，可以互換使用。

## 所需權限

如要查詢 `INFORMATION_SCHEMA.JOBS_TIMELINE` 檢視畫面，您需要專案的 `bigquery.jobs.listAll` Identity and Access Management (IAM) 權限。下列預先定義的 IAM 角色都包含必要權限：

* 專案擁有者
* BigQuery 管理員

如要進一步瞭解 BigQuery 權限，請參閱「[使用 IAM 控管存取權](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)」。

## 結構定義

查詢 `INFORMATION_SCHEMA.JOBS_TIMELINE_BY_*` 檢視表時，查詢結果會針對每項 BigQuery 工作執行期間的每秒，各列出一個相對應的資料列。每個週期都從整秒間隔開始，且持續時間正好為一秒。

`INFORMATION_SCHEMA.JOBS_TIMELINE_BY_*` 檢視表具有下列結構定義：

**注意：** 基礎資料會依 `job_creation_time` 資料欄分區，並依 `project_id` 和 `user_email` 分群。

| 資料欄名稱 | 資料類型 | 值 |
| --- | --- | --- |
| `period_start` | `TIMESTAMP` | 這個期間的開始時間。 |
| `period_slot_ms` | `INTEGER` | 這段期間消耗的運算單元時間 (毫秒)。 |
| `project_id` | `STRING` | *(叢集資料欄)* 專案 ID。 |
| `project_number` | `INTEGER` | 專案編號。 |
| `user_email` | `STRING` | *(叢集資料欄)* 執行工作的使用者電子郵件地址或服務帳戶。 |
| `principal_subject` | `STRING` | 執行作業的主體身分字串表示法。 |
| `job_id` | `STRING` | 工作 ID。例如 `bquxjob_1234`。 |
| `job_type` | `STRING` | 工作類型。可能的值為 `QUERY`、`LOAD`、`EXTRACT`、`COPY` 或 `NULL`。`NULL` 值表示背景工作。 |
| `labels` | `RECORD` | 以鍵/值組合形式套用至工作的標籤陣列。 |
| `statement_type` | `STRING` | 查詢陳述式類型 (如有效)。例如 `SELECT`、`INSERT`、`UPDATE` 或 `DELETE`。 |
| `priority` | `STRING` | 這項工作的優先順序。有效值包括 `INTERACTIVE` 和 `BATCH`。 |
| `parent_job_id` | `STRING` | 父項工作的 ID (如有)。 |
| `job_creation_time` | `TIMESTAMP` | *(分區資料欄)* 這項工作的建立時間。分區作業會根據這個時間戳記的世界標準時間進行。 |
| `job_start_time` | `TIMESTAMP` | 這項工作的開始時間。 |
| `job_end_time` | `TIMESTAMP` | 這項工作的結束時間。 |
| `state` | `STRING` | 這段期間結束時的工作執行狀態。有效狀態包括 `PENDING`、`RUNNING` 和 `DONE`。 |
| `reservation_id` | `STRING` | 如果適用，這個期間結束時指派給這項作業的主要預留項目名稱。 |
| `edition` | `STRING` | 與指派給這項工作的預留項目相關聯的版本。如要進一步瞭解版本，請參閱「[BigQuery 版本簡介](https://docs.cloud.google.com/bigquery/docs/editions-intro?hl=zh-tw)」。 |
| `total_bytes_billed` | `INTEGER` | 如果專案設定為使用[依用量計價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#analysis_pricing_models)，這個欄位會顯示作業的總計費位元組數。如果專案已設為使用[固定費率計價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#analysis_pricing_models)，系統就不會針對位元組收費，這個欄位僅供參考。這個欄位只會填入已完成的工作，並包含整個工作期間的總計費位元組數。 |
| `total_bytes_processed` | `INTEGER` | 工作處理的位元組總數。這個欄位只會填入已完成的工作，並包含工作整個期間處理的位元組總數。 |
| `error_result` | `RECORD` | 錯誤詳細資料 (如有)，以 `ErrorProto.` 形式呈現 |
| `cache_hit` | `BOOLEAN` | 這項工作的查詢結果是否來自快取。 |
| `period_shuffle_ram_usage_ratio` | `FLOAT` | 所選時間範圍內的重組用量比率。如果作業是透過使用自動調度的預留資源執行，且基準配額為零，則值為 `0.0`。 |
| `period_estimated_runnable_units` | `INTEGER` | 這段期間可立即排定的工作單元。如果預訂中的其他查詢不需要額外運算單元，這些作業單元的額外運算單元就能加快查詢速度。 |
| `transaction_id` | `STRING` | 這項工作執行的[交易](https://docs.cloud.google.com/bigquery/docs/transactions?hl=zh-tw) ID (如有)。 |

為確保穩定性，建議您在資訊結構定義查詢中明確列出資料欄，而非使用萬用字元 (`SELECT *`)。明確列出資料欄可避免基礎結構定義變更時，查詢中斷。

## 資料保留

這個檢視畫面會顯示執行中的工作，以及過去 180 天的工作記錄。
如果專案遷移至機構 (無論是從沒有機構或從其他機構遷移)，您都無法透過 `INFORMATION_SCHEMA.JOBS_TIMELINE` 檢視遷移日期前的作業資訊，因為該檢視畫面只會保留遷移日期後的資料。

## 範圍和語法

對這個檢視表執行的查詢必須包含[區域限定詞](https://docs.cloud.google.com/bigquery/docs/information-schema-intro?hl=zh-tw#syntax)。如未指定區域限定符，系統會從所有區域擷取中繼資料。下表說明這個檢視畫面的區域範圍：

| 檢視表名稱 | 資源範圍 | 區域範圍 |
| --- | --- | --- |
| `` [PROJECT_ID.]`region-REGION`.INFORMATION_SCHEMA.JOBS_TIMELINE[_BY_PROJECT] `` | 專案層級 | `REGION` |

取代下列項目：

* 選用：`PROJECT_ID`：專案 ID。 Google Cloud 如未指定，系統會使用預設專案。
* `REGION`：任何[資料集區域名稱](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)。
  例如：`` `region-us` ``。**注意：**您必須使用[區域限定詞](https://docs.cloud.google.com/bigquery/docs/information-schema-intro?hl=zh-tw#region_qualifier)查詢 `INFORMATION_SCHEMA` 檢視畫面。查詢執行位置必須與`INFORMATION_SCHEMA`檢視區塊的區域相符。

## 範例

如要對預設專案以外的專案執行查詢，請使用以下格式新增專案 ID：

```
`PROJECT_ID`.`region-REGION_NAME`.INFORMATION_SCHEMA.VIEW
```

例如 `` `myproject`.`region-us`.INFORMATION_SCHEMA.JOBS_TIMELINE ``。

以下範例會計算過去 1 天內每秒鐘的運算單元用量：

```
SELECT
  period_start,
  SUM(period_slot_ms) AS total_slot_ms,
FROM
  `reservation-admin-project.region-us`.INFORMATION_SCHEMA.JOBS_TIMELINE
WHERE
  period_start BETWEEN TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 1 DAY) AND CURRENT_TIMESTAMP()
GROUP BY
  period_start
ORDER BY
  period_start DESC;
```

**注意：** `INFORMATION_SCHEMA` 檢視表名稱會區分大小寫。

結果大致如下：

```
+---------------------+---------------+
|    period_start     | total_slot_ms |
+---------------------+---------------+
| 2020-07-29 03:52:14 |     122415176 |
| 2020-07-29 03:52:15 |     141107048 |
| 2020-07-29 03:52:16 |     173335142 |
| 2020-07-28 03:52:17 |     131107048 |
+---------------------+---------------+
```

您可以使用 `WHERE reservation_id = "…"` 檢查特定預留項目的用量。如果是指令碼工作，父項工作也會回報子項工作的總計使用量。為避免重複計算，請使用 `WHERE statement_type != "SCRIPT"` 排除父項工作。

### `RUNNING`和`PENDING`工作數量的變化趨勢

如要對預設專案以外的專案執行查詢，請使用以下格式新增專案 ID：

```
`PROJECT_ID`.`region-REGION_NAME`.INFORMATION_SCHEMA.VIEW
```

例如 `` `myproject`.`region-us`.INFORMATION_SCHEMA.JOBS_TIMELINE ``。

下列範例會計算過去一天內每秒的 `RUNNING` 和 `PENDING` 工作數量：

```
SELECT
  period_start,
  SUM(IF(state = "PENDING", 1, 0)) as PENDING,
  SUM(IF(state = "RUNNING", 1, 0)) as RUNNING
FROM
  `reservation-admin-project.region-us`.INFORMATION_SCHEMA.JOBS_TIMELINE
WHERE
  period_start BETWEEN TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 1 DAY) AND CURRENT_TIMESTAMP()
GROUP BY
  period_start;
```

**注意：** `INFORMATION_SCHEMA` 檢視表名稱會區分大小寫。

結果大致如下：

```
+---------------------+---------+---------+
|    period_start     | PENDING | RUNNING |
+---------------------+---------+---------+
| 2020-07-29 03:52:14 |       7 |      27 |
| 2020-07-29 03:52:15 |       1 |      21 |
| 2020-07-29 03:52:16 |       5 |      21 |
| 2020-07-29 03:52:17 |       4 |      22 |
+---------------------+---------+---------+
```

### 特定時間點的工作資源用量

如要對預設專案以外的專案執行查詢，請使用以下格式新增專案 ID：

```
`PROJECT_ID`.`region-REGION_NAME`.INFORMATION_SCHEMA.VIEW
```

例如 `` `myproject`.`region-us`.INFORMATION_SCHEMA.JOBS ``。

以下範例會傳回特定時間點執行的所有工作，以及該一秒期間的資源用量：`job_id`

```
SELECT
  job_id,
  period_slot_ms
FROM
  `reservation-admin-project.region-us`.INFORMATION_SCHEMA.JOBS_TIMELINE_BY_PROJECT
WHERE
  period_start = '2020-07-29 03:52:14'
  AND (statement_type != 'SCRIPT' OR statement_type IS NULL);
```

**注意：** `INFORMATION_SCHEMA` 檢視表名稱會區分大小寫。

結果大致如下：

```
+------------------+
| job_id | slot_ms |
+------------------+
| job_1  | 2415176 |
| job_2  | 4417245 |
| job_3  |  427416 |
| job_4  | 1458122 |
+------------------+
```

### 從管理資源圖表比對運算單元用量行為

您可以使用[管理資源圖表](https://docs.cloud.google.com/bigquery/docs/admin-resource-charts?hl=zh-tw)，監控機構的健康狀態、運算單元用量，以及 BigQuery 工作效能的變化。以下範例會查詢 `INFORMATION_SCHEMA.JOBS_TIMELINE` 檢視區塊，取得每小時的時段使用時間軸，與管理資源圖表中的資訊類似。

```
DECLARE
  start_time timestamp DEFAULT TIMESTAMP(START_TIME);
DECLARE
  end_time timestamp DEFAULT TIMESTAMP(END_TIME);

WITH
  snapshot_data AS (
  SELECT
    UNIX_MILLIS(period_start) AS period_start,
    IFNULL(SUM(period_slot_ms), 0) AS period_slot_ms,
    DIV(UNIX_MILLIS(period_start), 3600000 * 1) * 3600000 * 1 AS time_ms
  FROM (
    SELECT
      *
    FROM
      `PROJECT_ID.region-US`.INFORMATION_SCHEMA.JOBS_TIMELINE_BY_PROJECT
    WHERE
      ((job_creation_time >= TIMESTAMP_SUB(start_time, INTERVAL 1200 MINUTE)
          AND job_creation_time < TIMESTAMP(end_time))
        AND period_start >= TIMESTAMP(start_time)
        AND period_start < TIMESTAMP(end_time))
      AND (statement_type != "SCRIPT"
        OR statement_type IS NULL)
      AND REGEXP_CONTAINS(reservation_id, "^PROJECT_ID:") )
  GROUP BY
    period_start,
    time_ms ),
  converted_percentiles_data AS (
  SELECT
    time_ms,
    100 - CAST(SAFE_DIVIDE(3600000 * 1 * 1 / 1000, COUNT(*)) AS INT64) AS converted_percentiles,
  FROM
    snapshot_data
  GROUP BY
    time_ms ),
  data_by_time AS (
  SELECT
    time_ms,
  IF
    (converted_percentiles <= 0, 0, APPROX_QUANTILES(period_slot_ms, 100)[SAFE_OFFSET(converted_percentiles)] / 1000) AS p99_slots,
    SUM(period_slot_ms) / (3600000 * 1) AS avg_slots
  FROM
    snapshot_data
  JOIN
    converted_percentiles_data AS c
  USING
    (time_ms)
  GROUP BY
    time_ms,
    converted_percentiles )
SELECT
  time_ms,
  TIMESTAMP_MILLIS(time_ms) AS time_stamp,
  IFNULL(avg_slots, 0) AS avg_slots,
  IFNULL(p99_slots, 0) AS p99_slots,
FROM (
  SELECT
    time_ms * 3600000 * 1 AS time_ms
  FROM
    UNNEST(GENERATE_ARRAY(DIV(UNIX_MILLIS(start_time), 3600000 * 1), DIV(UNIX_MILLIS(end_time), 3600000 * 1) - 1, 1)) AS time_ms )
LEFT JOIN
  data_by_time
USING
  (time_ms)
ORDER BY
  time_ms DESC;
```

### 計算有待處理工作的執行時間百分比

如要對預設專案以外的專案執行查詢，請使用以下格式新增專案 ID：

```
`PROJECT_ID`.`region-REGION_NAME`.INFORMATION_SCHEMA.VIEW
```

例如 `` `myproject`.`region-us`.INFORMATION_SCHEMA.JOBS ``。

以下範例會傳回浮點值，代表 [`period_estimated_runnable_units`](https://docs.cloud.google.com/bigquery/docs/information-schema-jobs-timeline?hl=zh-tw#schema) 值不為零的總工作執行時間百分比，也就是工作要求更多時段。值越大表示作業的時段競爭越激烈，值越小則表示作業在大部分的執行時間內都未要求時段，因此時段競爭程度很低或沒有競爭。

如果結果值很大，您可以嘗試新增更多時段，瞭解影響並判斷時段爭用是否為唯一瓶頸。

```
SELECT ROUND(COUNTIF(period_estimated_runnable_units > 0) / COUNT(*) * 100, 1) as execution_duration_percentage
FROM `myproject`.`region-us`.INFORMATION_SCHEMA.JOBS_TIMELINE
WHERE job_id = 'my_job_id'
GROUP BY job_id
```

如果您知道查詢的執行日期，請在查詢中加入 `DATE(period_start) = 'YYYY-MM-DD'` 子句，減少處理的位元組數量，並加快執行速度。例如：`DATE(period_start) = '2025-08-22'`。

**注意：** `INFORMATION_SCHEMA` 檢視表名稱會區分大小寫。

結果大致如下：

```
+-------------------------------+
| execution_duration_percentage |
+-------------------------------+
|                          96.7 |
+-------------------------------+
```




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-02 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-02 (世界標準時間)。"],[],[]]