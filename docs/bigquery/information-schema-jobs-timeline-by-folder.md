Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [參考資料](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# JOBS\_TIMELINE\_BY\_FOLDER 檢視表

`INFORMATION_SCHEMA.JOBS_TIMELINE_BY_FOLDER` 檢視表包含近乎即時的 BigQuery 中繼資料，依時間片段列出目前專案上層資料夾中提交的所有工作，包括其子資料夾中的工作。這個檢視畫面會同時顯示執行中和已完成的工作。

## 所需權限

如要查詢 `INFORMATION_SCHEMA.JOBS_TIMELINE_BY_FOLDER` 檢視表，您必須具備上層資料夾的 `bigquery.jobs.listAll` Identity and Access Management (IAM) 權限。下列各項預先定義的 IAM 角色都包含必要權限：

* 資料夾管理員
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
| `folder_numbers` | `REPEATED INTEGER` | 專案所在資料夾的數字 ID，開頭為直接包含專案的資料夾，後面依序為包含子資料夾的資料夾，以此類推。舉例來說，如果 `folder\_numbers` 為 `[1, 2, 3]`，則資料夾 `1` 會直接包含專案，資料夾 `2` 包含 `1`，資料夾 `3` 包含 `2`。 |
| `user_email` | `STRING` | *(分群欄)* 執行工作的使用者電子郵件地址或服務帳戶。 |
| `principal_subject` | `STRING` | 執行工作的委託人身分字串表示法。 |
| `job_id` | `STRING` | 工作 ID。例如 `bquxjob_1234`。 |
| `job_type` | `STRING` | 工作類型。可以是 `QUERY`、`LOAD`、`EXTRACT`、`COPY` 或 `null`。工作類型 `null` 表示內部工作，例如指令碼工作陳述式評估或 materialized view 重新整理。 |
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
| `total_bytes_billed` | `INTEGER` | 如果專案設為使用[隨選計價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#analysis_pricing_models)，這個欄位會包含工作的計費位元組總數。如果專案設為使用[固定費率計價模式](https://cloud.google.com/bigquery/pricing?hl=zh-tw#analysis_pricing_models)，系統就不會向您收取位元組費用，這個欄位僅供參考。 |
| `total_bytes_processed` | `INTEGER` | 工作處理的位元組總數。 |
| `error_result` | `RECORD` | 錯誤詳細資料 (如有)，格式為 `ErrorProto.` |
| `cache_hit` | `BOOLEAN` | 這項工作的查詢結果是否來自快取。 |
| `period_shuffle_ram_usage_ratio` | `FLOAT` | 所選時間範圍內的重組用量比率。如果工作執行的預留項目使用自動調度資源，且基準運算單元為零，則值為 `0.0`。 |
| `period_estimated_runnable_units` | `INTEGER` | 這段期間內可立即排定的工作單位。如果預留項目中沒有其他查詢需要額外運算單元，則這些工作單元的額外運算單元會加快查詢速度。 |
| `transaction_id` | `STRING` | 執行這項工作的[交易](https://docs.cloud.google.com/bigquery/docs/transactions?hl=zh-tw) ID (如有)。([預先發布版](https://cloud.google.com/products?hl=zh-tw#product-launch-stages)) |
| `global_query_info` | `RECORD` | [全域查詢](https://docs.cloud.google.com/bigquery/docs/global-queries?hl=zh-tw)的相關資訊。 包含下列欄位：  * `parent_job_id`：主要區域中父項全域查詢工作的 ID。 * `parent_job_location`：父項全域查詢工作的所在位置。 * `remote_regions`：全域查詢參照的遠端區域陣列。 |
| `copy_job_statistics` | `RECORD` | [複製工作的統計資料。](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#CopyJobStatistics) |

為確保穩定性，建議您在資訊結構定義查詢中明確列出資料欄，而非使用萬用字元 (`SELECT *`)。明確列出資料欄可避免查詢因基礎結構定義變更而中斷。

## 資料保留

這個檢視畫面會顯示執行中的工作，以及過去 180 天的工作記錄。如果專案從無組織或不同組織遷移至某個組織，則無法透過 `INFORMATION_SCHEMA.JOBS_TIMELINE_BY_FOLDER` 檢視畫面存取遷移日期之前的任務資訊，因為該檢視畫面只會保留遷移日期之後的資料。

## 範圍和語法

對這個檢視表執行的查詢必須包含[區域限定詞](https://docs.cloud.google.com/bigquery/docs/information-schema-intro?hl=zh-tw#syntax)。如未指定區域限定詞，系統會從所有區域擷取中繼資料。下表說明這個檢視畫面的區域範圍：

| 檢視表名稱 | 資源範圍 | 區域範圍 |
| --- | --- | --- |
| `` [PROJECT_ID.]`region-REGION`.INFORMATION_SCHEMA.JOBS_TIMELINE_BY_FOLDER `` | 專案層級 | REGION |

請更改下列內容：

* 選用：`PROJECT_ID`： Google Cloud 專案的 ID。如未指定，則會使用預設專案。
* `REGION`：任何[資料集區域名稱](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)。例如：`` `region-us` ``。**注意：**您必須使用[區域限定詞](https://docs.cloud.google.com/bigquery/docs/information-schema-intro?hl=zh-tw#region_qualifier)，才能查詢 `INFORMATION_SCHEMA` 檢視表。查詢執行位置必須與 `INFORMATION_SCHEMA` 檢視表的區域相符。

## 範例

以下範例說明如何查詢 `INFORMATION_SCHEMA.JOBS_TIMELINE_BY_FOLDER` 檢視表。

### 取得不重複工作數量

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

### 計算使用的運算單元時間

下列查詢會顯示指定專案資料夾中每分鐘使用的運算單元時間：

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

**注意：** `INFORMATION_SCHEMA` 檢視表名稱會區分大小寫。**注意：**單一資料夾中的專案可以指派給多個預留項目。`JOBS_TIMELINE_BY_FOLDER` 可提供多個預留項目的資料。加總`period_slot_ms`時，請務必篩選個別預訂。

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

上次更新時間：2026-10-24 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-10-24 (世界標準時間)。"],[],[]]