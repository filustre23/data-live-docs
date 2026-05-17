Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [參考資料](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# JOBS\_TIMELINE\_BY\_FOLDER 檢視畫面

`INFORMATION_SCHEMA.JOBS_TIMELINE_BY_FOLDER` 檢視畫面包含目前專案上層資料夾中，所有已提交工作 (包括子資料夾中的工作) 的近乎即時 BigQuery 中繼資料 (以時間切片為單位)。這個檢視畫面會顯示執行中和已完成的工作。

## 所需權限

如要查詢 `INFORMATION_SCHEMA.JOBS_TIMELINE_BY_FOLDER` 檢視畫面，您需要父項資料夾的 `bigquery.jobs.listAll` Identity and Access Management (IAM) 權限。下列每個預先定義的 IAM 角色都包含必要權限：

* 資料夾管理員
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
| `folder_numbers` | `REPEATED INTEGER` | 含有專案的資料夾 ID 號碼，從直接含有專案的資料夾開始，接著是含有子資料夾的資料夾，依此類推。舉例來說，如果 `folder\_numbers` 是 `[1, 2, 3]`，則資料夾 `1` 會立即包含專案，資料夾 `2` 包含 `1`，資料夾 `3` 包含 `2`。 |
| `user_email` | `STRING` | *(叢集資料欄)* 執行工作的使用者電子郵件地址或服務帳戶。 |
| `principal_subject` | `STRING` | 執行作業的主體身分字串表示法。 |
| `job_id` | `STRING` | 工作 ID。例如 `bquxjob_1234`。 |
| `job_type` | `STRING` | 工作類型。可能的值為 `QUERY`、`LOAD`、`EXTRACT`、`COPY` 或 `null`。工作類型 `null` 表示內部工作，例如指令碼工作陳述式評估或具體化檢視畫面重新整理。 |
| `statement_type` | `STRING` | 查詢陳述式類型 (如有效)。例如：`SELECT`、`INSERT`、`UPDATE` 或 `DELETE`。 |
| `priority` | `STRING` | 這項工作的優先順序。有效值包括 `INTERACTIVE` 和 `BATCH`。 |
| `parent_job_id` | `STRING` | 父項工作的 ID (如有)。 |
| `job_creation_time` | `TIMESTAMP` | *(分區資料欄)* 這項工作的建立時間。分區依據是這個時間戳記的世界標準時間。 |
| `job_start_time` | `TIMESTAMP` | 這項工作的開始時間。 |
| `job_end_time` | `TIMESTAMP` | 這項工作的結束時間。 |
| `state` | `STRING` | 這段期間結束時的工作執行狀態。有效狀態包括 `PENDING`、`RUNNING` 和 `DONE`。 |
| `reservation_id` | `STRING` | 如果適用，這個期間結束時指派給這項工作的主要預留項目名稱。 |
| `edition` | `STRING` | 與指派給這項工作的預留項目相關聯的版本。如要進一步瞭解版本，請參閱「[BigQuery 版本簡介](https://docs.cloud.google.com/bigquery/docs/editions-intro?hl=zh-tw)」。 |
| `total_bytes_billed` | `INTEGER` | 如果專案設定為使用[依用量計價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#analysis_pricing_models)，這個欄位會顯示作業的總計費位元組數。如果專案已設為使用[固定費率計價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#analysis_pricing_models)，系統就不會針對位元組收費，這個欄位僅供參考。 |
| `total_bytes_processed` | `INTEGER` | 工作處理的位元組總數。 |
| `error_result` | `RECORD` | 錯誤詳細資料 (如有)，格式為 `ErrorProto.` |
| `cache_hit` | `BOOLEAN` | 這項工作的查詢結果是否來自快取。 |
| `period_shuffle_ram_usage_ratio` | `FLOAT` | 所選時間範圍內的重組用量比率。如果作業是透過使用自動調度的預留項目執行，且基準配額為零，則值為 `0.0`。 |
| `period_estimated_runnable_units` | `INTEGER` | 這段期間可立即排定的工作單元。如果預訂中的其他查詢不需要額外運算單元，這些作業單元的額外運算單元就能加快查詢速度。 |
| `transaction_id` | `STRING` | 這項工作執行的[交易](https://docs.cloud.google.com/bigquery/docs/transactions?hl=zh-tw) ID (如有)。([預覽](https://cloud.google.com/products?hl=zh-tw#product-launch-stages)) |

為確保穩定性，建議您在資訊結構定義查詢中明確列出資料欄，而非使用萬用字元 (`SELECT *`)。明確列出資料欄可避免基礎結構定義變更時，查詢中斷。

## 資料保留

這個檢視畫面會顯示執行中的工作，以及過去 180 天的工作記錄。
如果專案遷移至機構 (無論是從沒有機構或從其他機構遷移)，您都無法透過 `INFORMATION_SCHEMA.JOBS_TIMELINE_BY_FOLDER` 檢視遷移日期前的作業資訊，因為檢視畫面只會保留遷移日期後的資料。

## 範圍和語法

對這個檢視表執行的查詢必須包含[區域限定詞](https://docs.cloud.google.com/bigquery/docs/information-schema-intro?hl=zh-tw#syntax)。如未指定區域限定符，系統會從所有區域擷取中繼資料。下表說明這個檢視畫面的區域範圍：

| 檢視表名稱 | 資源範圍 | 區域範圍 |
| --- | --- | --- |
| `` [PROJECT_ID.]`region-REGION`.INFORMATION_SCHEMA.JOBS_TIMELINE_BY_FOLDER `` | 專案層級 | REGION |

取代下列項目：

* 選用：`PROJECT_ID`：您的 Google Cloud 專案 ID。如未指定，系統會使用預設專案。
* `REGION`：任何[資料集區域名稱](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)。
  例如：`` `region-us` ``。**注意：**您必須使用[區域限定詞](https://docs.cloud.google.com/bigquery/docs/information-schema-intro?hl=zh-tw#region_qualifier)查詢 `INFORMATION_SCHEMA` 檢視畫面。查詢執行位置必須與 `INFORMATION_SCHEMA` 檢視區塊的區域相符。

## 範例

下列範例說明如何查詢 `INFORMATION_SCHEMA.JOBS_TIMELINE_BY_FOLDER` 檢視區塊。

### 取得不重複職缺數量

下列查詢會顯示指定專案資料夾中，每分鐘執行的不重複工作數量：

```
SELECT
  TIMESTAMP_TRUNC(period_start, MINUTE) AS per_start,
  COUNT(DISTINCT job_id) AS unique_jobs
FROM
  `region-us`.INFORMATION_SCHEMA.JOBS_TIMELINE_BY_FOLDER,
  UNNEST(folder_numbers) f
WHERE
  my_folder_number = f
GROUP BY
  per_start
ORDER BY
  per_start DESC;
```

**注意：** `INFORMATION_SCHEMA` 檢視表名稱會區分大小寫。

結果大致如下：

```
+---------------------------+---------------------------------+
|  per_start                |  unique_jobs                    |
+---------------------------+---------------------------------+
|  2019-10-10 00:04:00 UTC  |  5                              |
|  2019-10-10 00:03:00 UTC  |  2                              |
|  2019-10-10 00:02:00 UTC  |  3                              |
|  2019-10-10 00:01:00 UTC  |  4                              |
|  2019-10-10 00:00:00 UTC  |  4                              |
+---------------------------+---------------------------------+
```

### 計算運算單元時間

以下查詢會顯示指定專案資料夾每分鐘使用的時段時間：

```
SELECT
  TIMESTAMP_TRUNC(period_start, MINUTE) AS per_start,
  SUM(period_slot_ms) AS slot_ms
FROM
  `region-us`.INFORMATION_SCHEMA.JOBS_TIMELINE_BY_FOLDER,
  UNNEST(folder_numbers) f
WHERE
  my_folder_number = f
  AND reservation_id = "my reservation id"
  AND statement_type != "SCRIPT"
GROUP BY
  per_start
ORDER BY
  per_start DESC;
```

**注意：** `INFORMATION_SCHEMA` 檢視表名稱會區分大小寫。**注意：**單一資料夾中的專案可指派給多個預訂。`JOBS_TIMELINE_BY_FOLDER` 可提供多個預訂項目的資料。加總 `period_slot_ms` 時，請務必篩選個別預訂記錄。

結果大致如下：

```
+---------------------------+---------------------------------+
|  per_start                |  slot_ms                        |
+---------------------------+---------------------------------+
|  2019-10-10 00:04:00 UTC  |  500                            |
|  2019-10-10 00:03:00 UTC  |  1000                           |
|  2019-10-10 00:02:00 UTC  |  3000                           |
|  2019-10-10 00:01:00 UTC  |  4000                           |
|  2019-10-10 00:00:00 UTC  |  4000                           |
+---------------------------+---------------------------------+
```




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-16 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-16 (世界標準時間)。"],[],[]]