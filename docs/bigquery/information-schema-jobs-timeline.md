Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [參考資料](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# JOBS\_TIMELINE 時間軸檢視畫面

`INFORMATION_SCHEMA.JOBS_TIMELINE` 檢視表包含目前專案中提交的所有工作，並依時間切片提供近乎即時的 BigQuery 中繼資料。這個檢視畫面會顯示目前執行中和已完成的工作。

**注意：** 檢視畫面名稱 `INFORMATION_SCHEMA.JOBS_TIMELINE` 和 `INFORMATION_SCHEMA.JOBS_TIMELINE_BY_PROJECT` 是同義詞，可以交替使用。

## 所需權限

如要查詢 `INFORMATION_SCHEMA.JOBS_TIMELINE` 檢視表，您必須具備專案的 `bigquery.jobs.listAll` Identity and Access Management (IAM) 權限。下列每個預先定義的 IAM 角色都包含必要權限：

* 專案擁有者
* BigQuery 管理員

如要進一步瞭解 BigQuery 權限，請參閱「[使用 IAM 控管存取權](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)」。

## 結構定義

查詢 `INFORMATION_SCHEMA.JOBS_TIMELINE_BY_*` 檢視表時，查詢結果會針對每項 BigQuery 工作的每秒執行時間，顯示一個資料列。每個時段都從整秒間隔開始，持續時間剛好一秒。

`INFORMATION_SCHEMA.JOBS_TIMELINE_BY_*` 檢視表具有下列結構定義：

**注意：** 基礎資料會依 `job_creation_time` 欄分區，並依 `project_id` 和 `user_email` 分類。

| 資料欄名稱 | 資料類型 | 值 |
| --- | --- | --- |
| `period_start` | `TIMESTAMP` | 這個時段的開始時間。 |
| `period_slot_ms` | `INTEGER` | 這段期間內耗用的運算單元時間 (毫秒)。 |
| `project_id` | `STRING` | *(分群欄)* 專案 ID。 |
| `project_number` | `INTEGER` | 專案編號。 |
| `user_email` | `STRING` | *(分群欄)* 執行工作的使用者電子郵件地址或服務帳戶。 |
| `principal_subject` | `STRING` | 執行工作的委託人身分字串表示法。 |
| `job_id` | `STRING` | 工作 ID。例如 `bquxjob_1234`。 |
| `job_type` | `STRING` | 工作類型。可以是 `QUERY`、`LOAD`、`EXTRACT`、`COPY` 或 `NULL`。`NULL` 值表示背景工作。 |
| `labels` | `RECORD` | 套用至工作的標籤陣列，以鍵/值組合表示。 |
| `statement_type` | `STRING` | 查詢陳述式的類型 (如果有效)。例如：`SELECT`、`INSERT`、`UPDATE` 或 `DELETE`。 |
| `priority` | `STRING` | 這項工作的優先順序。有效值包括 `INTERACTIVE` 和 `BATCH`。 |
| `parent_job_id` | `STRING` | 父項工作的 ID (如有)。 |
| `job_creation_time` | `TIMESTAMP` | *(分區資料欄)* 這項工作的建立時間。分區依據為這個時間戳記的世界標準時間。 |
| `job_start_time` | `TIMESTAMP` | 這項工作的開始時間。 |
| `job_end_time` | `TIMESTAMP` | 這項工作的結束時間。 |
| `state` | `STRING` | 這段期間結束時的工作執行狀態。有效狀態包括 `PENDING`、`RUNNING` 和 `DONE`。 |
| `reservation_id` | `STRING` | 這段期間結束時，指派給這項工作的主要預留項目名稱 (如適用)。 |
| `reservation_group_path` | `ARRAY<STRING>` | 預留項目連結的預留項目群組。舉例來說，如果預留項目連結至群組 `my-group`，`reservation_group_path` 欄位會包含類似 `[my-group]` 的清單。 |
| `edition` | `STRING` | 與指派給這項工作的預留項目相關聯的版本。如要進一步瞭解版本，請參閱「[BigQuery 版本簡介](https://docs.cloud.google.com/bigquery/docs/editions-intro?hl=zh-tw)」。 |
| `total_bytes_billed` | `INTEGER` | 如果專案設為使用[隨選計價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#analysis_pricing_models)，這個欄位會包含工作的計費位元組總數。如果專案設為使用[固定費率定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#analysis_pricing_models)，系統就不會向您收取位元組費用，而這個欄位僅供參考。這個欄位只會填入已完成工作的資料，並包含工作整個執行期間計費的總位元組數。 |
| `total_bytes_processed` | `INTEGER` | 工作處理的位元組總數。這個欄位只會填入已完成工作的資料，並包含工作整個執行期間處理的位元組總數。 |
| `error_result` | `RECORD` | 錯誤詳細資料 (如有)，格式為 `ErrorProto.` |
| `cache_hit` | `BOOLEAN` | 這項工作的查詢結果是否來自快取。 |
| `period_shuffle_ram_usage_ratio` | `FLOAT` | 所選時間範圍內的重組用量比率。如果工作執行的預留項目使用自動調度資源，且基準運算單元為零，則值為 `0.0`。 |
| `period_estimated_runnable_units` | `INTEGER` | 這段期間內可立即排定的工作單位。如果預留項目中沒有其他查詢需要額外運算單元，則這些工作單元的額外運算單元會加快查詢速度。 |
| `transaction_id` | `STRING` | 執行這項工作的[交易](https://docs.cloud.google.com/bigquery/docs/transactions?hl=zh-tw) ID (如果有的話)。 |
| `global_query_info` | `RECORD` | [全域查詢](https://docs.cloud.google.com/bigquery/docs/global-queries?hl=zh-tw)的相關資訊。 包含下列欄位：  * `parent_job_id`：主要區域中父項全域查詢工作的 ID。 * `parent_job_location`：父項全域查詢工作的所在位置。 * `remote_regions`：全域查詢參照的遠端區域陣列。 |
| `copy_job_statistics` | `RECORD` | [複製工作的統計資料。](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#CopyJobStatistics) |

為確保穩定性，建議您在資訊結構定義查詢中明確列出資料欄，而非使用萬用字元 (`SELECT *`)。明確列出資料欄可避免查詢因基礎結構定義變更而中斷。

## 資料保留

這個檢視畫面會顯示執行中的工作，以及過去 180 天的工作記錄。如果專案遷移至某個組織 (無論是從無組織狀態或從其他組織遷移)，則遷移日期之前的作業資訊無法透過 `INFORMATION_SCHEMA.JOBS_TIMELINE` 檢視畫面存取，因為該檢視畫面只會保留遷移日期之後的資料。

## 範圍和語法

對這個檢視表執行的查詢必須包含[區域限定詞](https://docs.cloud.google.com/bigquery/docs/information-schema-intro?hl=zh-tw#syntax)。如未指定區域限定詞，系統會從所有區域擷取中繼資料。下表說明這個檢視畫面的區域範圍：

| 檢視表名稱 | 資源範圍 | 區域範圍 |
| --- | --- | --- |
| `` [PROJECT_ID.]`region-REGION`.INFORMATION_SCHEMA.JOBS_TIMELINE[_BY_PROJECT] `` | 專案層級 | `REGION` |

請更改下列內容：

* 選用：`PROJECT_ID`： Google Cloud 專案的 ID。如未指定，則會使用預設專案。
* `REGION`：任何[資料集區域名稱](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)。例如：`` `region-us` ``。**注意：**您必須使用[區域限定詞](https://docs.cloud.google.com/bigquery/docs/information-schema-intro?hl=zh-tw#region_qualifier)，才能查詢 `INFORMATION_SCHEMA` 檢視表。查詢執行位置必須與 `INFORMATION_SCHEMA` 檢視表的區域相符。

## 範例

如要對預設專案以外的專案執行查詢，請按照下列格式新增專案 ID：

```
`PROJECT_ID`.`region-REGION_NAME`.INFORMATION_SCHEMA.VIEW
```

例如 `` `myproject`.`region-us`.INFORMATION_SCHEMA.JOBS_TIMELINE ``。

下列範例會計算過去 1 天內每秒鐘的運算單元用量：

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

您可以使用 `WHERE reservation_id = "…"` 查看特定預留項目的用量。如果是指令碼工作，父項工作也會回報子項工作的總運算單元用量。為避免重複計算，請使用 `WHERE statement_type != "SCRIPT"` 排除父項工作。

### `RUNNING`和`PENDING`工作數量變化趨勢

如要對預設專案以外的專案執行查詢，請按照下列格式新增專案 ID：

```
`PROJECT_ID`.`region-REGION_NAME`.INFORMATION_SCHEMA.VIEW
```

例如 `` `myproject`.`region-us`.INFORMATION_SCHEMA.JOBS_TIMELINE ``。

以下範例會計算過去一天內每秒的 `RUNNING` 和 `PENDING` 工作數量：

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

如要對預設專案以外的專案執行查詢，請按照下列格式新增專案 ID：

```
`PROJECT_ID`.`region-REGION_NAME`.INFORMATION_SCHEMA.VIEW
```

例如 `` `myproject`.`region-us`.INFORMATION_SCHEMA.JOBS ``。

以下範例會傳回在特定時間點執行的所有工作 `job_id`，以及這些工作在該一秒期間的資源用量：

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

### 比對管理資源圖表的運算單元用量行為

您可以使用[管理資源圖表](https://docs.cloud.google.com/bigquery/docs/admin-resource-charts?hl=zh-tw)，監控組織的健康狀態、運算單元用量，以及 BigQuery 工作在一段時間內的效能。以下範例會查詢 `INFORMATION_SCHEMA.JOBS_TIMELINE` 檢視表，以一小時為間隔取得運算單元用量時間軸，類似於管理資源圖表中提供的資訊。

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
      ((job_creation_time >= TIMESTAMP_SUB(start_time, INTERVAL 1200 MINUTE
```