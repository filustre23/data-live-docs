Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# BigQuery 資料表的中繼資料索引

BigQuery 會自動為大於 1 GiB 的 BigQuery 資料表建立資料欄中繼資料索引，並使用該索引加速查詢。中繼資料包括檔案位置、分區資訊和資料欄層級屬性。根據預設，建立索引是免費的背景作業，但索引更新程度取決於可用的免費資源，且沒有效能服務水準目標 (SLO)。

如果索引新鮮度對工作負載至關重要，您可以設定 [`BACKGROUND` 預留項目](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#assignments)，分配專用資源。本文說明如何監控索引更新度和用量、設定專屬索引資源，以及設定索引警告。

## 查看中繼資料索引重新整理時間

如要查看資料表上次重新整理中繼資料索引的時間，請查詢 [`INFORMATION_SCHEMA.TABLE_STORAGE` 檢視表](https://docs.cloud.google.com/bigquery/docs/information-schema-table-storage?hl=zh-tw)的 `LAST_METADATA_INDEX_REFRESH_TIME` 資料欄。方法很簡單，按照以下步驟操作即可：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列陳述式：

   ```
   SELECT
     project_id,
     project_number,
     table_name,
     last_metadata_index_refresh_time
   FROM
     [PROJECT_ID.]region-REGION.INFORMATION_SCHEMA.TABLE_STORAGE;
   ```

   更改下列內容：

   * `PROJECT_ID`： Google Cloud 專案的 ID。如未指定，則會使用預設專案。
   * `REGION`：專案所在的[區域](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)，例如 `region-us`。
3. 按一下「play\_circle 執行」。

## 查看資料欄中繼資料索引使用情形

如要查看工作完成後是否使用資料欄中繼資料索引，請檢查[工作](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw)資源的 [`TableMetadataCacheUsage` 屬性](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#tablemetadatacacheusage)。如果 `unusedReason` 欄位空白 (未填入)，則表示使用了資料欄中繼資料索引。如果已填入，隨附的 `explanation` 欄位會提供未使用資料欄中繼資料索引的原因。

您也可以在 [`INFORMATION_SCHEMA.JOBS` 檢視表](https://docs.cloud.google.com/bigquery/docs/information-schema-jobs?hl=zh-tw)中使用 `metadata_cache_statistics` 欄位，查看資料欄中繼資料索引的使用情形。

舉例來說，下列指令會顯示 `my-job` 工作的資料欄中繼資料索引使用情形：

```
SELECT metadata_cache_statistics
FROM `region-US`.INFORMATION_SCHEMA.JOBS
WHERE job_id = 'my-job';
```

再舉一個例子，下列指令會顯示 `my-table` 資料表使用資料欄中繼資料索引的工作數量：

```
SELECT COUNT(*)
FROM
  `region-US`.INFORMATION_SCHEMA.JOBS,
  UNNEST(metadata_cache_statistics.table_metadata_cache_usage) AS stats
WHERE
  stats.table_reference.table_id='my-table' AND
  stats.table_reference.dataset_id='my-dataset' AND
  stats.table_reference.project_id='my-project' AND
  stats.unusedReason IS NULL;
```

## 設定專屬索引資源

如要在專案中設定中繼資料索引更新資源，您必須先將預留項目指派給專案。方法很簡單，按照以下步驟操作即可：

1. [建立 `BACKGROUND` 預留項目](https://docs.cloud.google.com/bigquery/docs/reservations-tasks?hl=zh-tw)。`BACKGROUND` 預留項目會在背景最佳化工作中分享資源。
2. [將專案指派給預留項目](https://docs.cloud.google.com/bigquery/docs/reservations-assignments?hl=zh-tw#assign_my_prod_project_to_prod_reservation)。

設定預留項目後，請選取下列其中一種方法，將運算單元指派給中繼資料索引工作。根據預設，如果以這種方式分配的運算單元處於閒置狀態，則會與其他工作共用。詳情請參閱「[閒置運算單元](https://docs.cloud.google.com/bigquery/docs/slots?hl=zh-tw#idle_slots)」。

### 控制台

1. 前往 Google Cloud 控制台的「Workload management」(工作負載管理) 頁面。

   [前往「Workload management」(工作負載管理)](https://console.cloud.google.com/bigquery/admin/reservations?hl=zh-tw)
2. 依序點選「more\_vert」**>「Create assignment」(建立指派作業)**。
3. 選取預留項目專案。
4. 將「Job Type」(工作類型) 設為「Background」(背景)。
5. 點選「建立」。

### bq

使用 [`bq mk`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_mk) 指令。

```
bq mk \
  --project_id=ADMIN_PROJECT_ID \
  --location=LOCATION \
  --reservation_assignment \
  --reservation_id=RESERVATION_NAME \
  --assignee_id=PROJECT_ID \
  --job_type=BACKGROUND \
  --assignee_type=PROJECT
```

更改下列內容：

* `ADMIN_PROJECT_ID`：擁有預留資源的[管理專案](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#admin-project) ID。
* `LOCATION`：預留項目的[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)。
* `RESERVATION_NAME`：預留項目名稱。
* `PROJECT_ID`：：要指派給這項
  預留項目的專案 ID。

### SQL

如要將預留項目指派給專案，請使用 [`CREATE ASSIGNMENT` DDL 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#create_assignment_statement)。

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery/?hl=zh-tw)
2. 在查詢編輯器中輸入下列陳述式：

   ```
   CREATE ASSIGNMENT
   ADMIN_PROJECT_ID.region-LOCATION.RESERVATION_NAME.ASSIGNMENT_ID
   OPTIONS (
     assignee = 'projects/PROJECT_ID',
     job_type = 'BACKGROUND');
   ```

   更改下列內容：
   * `ADMIN_PROJECT_ID`：擁有預留資源的[管理專案](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#admin-project) ID。
   * `LOCATION`：預留項目的[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)。
   * `RESERVATION_NAME`：預留項目名稱。
   * `ASSIGNMENT_ID`：作業 ID。ID 在專案和位置中不得重複，開頭和結尾須為小寫英文字母或數字，且只能包含小寫英文字母、數字和破折號。
   * `PROJECT_ID`：資料表所在的專案 ID。這項專案已指派給預留項目。
3. 按一下「play\_circle 執行」。

## 查看索引工作資訊

設定專屬索引工作後，您可以使用 [`JOBS` 檢視畫面](https://docs.cloud.google.com/bigquery/docs/information-schema-jobs?hl=zh-tw)查看索引工作的相關資訊。下列 SQL 範例顯示 `PROJECT_NAME` 中最近五項重新整理工作。

```
SELECT *
FROM
  region-us.INFORMATION_SCHEMA.JOBS
WHERE
  project_id = 'PROJECT_NAME'
  AND SEARCH(job_id, '`metadata_cache_refresh`')
ORDER BY
  creation_time DESC
LIMIT 5;
```

將 `PROJECT_NAME` 替換為中繼資料索引工作所在專案的名稱。

## 設定中繼資料索引建立快訊

如果 BigQuery 效能未達到定義的條件，Cloud Monitoring 警告程序會通知您。詳情請參閱「[快訊總覽](https://docs.cloud.google.com/monitoring/alerts?hl=zh-tw)」。有了中繼資料索引，您就能設定運算單元用量和過時程度的警告。

### 運算單元用量快訊

當背景預留項目超過指定分配百分比時，這項快訊會通知您。預設值為 95%。您可以針對特定預留項目或所有背景預留項目設定這項警告。觸發這項快訊時，建議您[增加預留項目大小](https://docs.cloud.google.com/bigquery/docs/reservations-tasks?hl=zh-tw#update_reservations)。

如要為每個背景預留項目設定這項警告，請按照下列步驟操作：

1. 如果尚未設定 [Monitoring 通知管道](https://docs.cloud.google.com/monitoring/support/notification-options?hl=zh-tw#creating_channels)，請先完成設定。
2. 前往「Integrations」(整合) 頁面。

   [前往「整合」頁面](https://console.cloud.google.com/monitoring/integrations?hl=zh-tw)
3. 找到 **BigQuery** 整合項目，然後點選「查看詳細資料」。
4. 在「Alerts」(快訊) 分頁中，選取「Slot Usage - Background Metadata Cache Slot Usage Too High」(運算單元用量 - 背景中繼資料快取運算單元用量過高)。
5. 選用：如要進一步自訂這項警告，請依序點選
   **「Show options」(顯示選項) >「Customize alert policy」(自訂警告政策)**。
6. 在「設定通知」部分，選取通知管道。
7. 點選「建立」。

### 過時警示

如果資料欄中繼資料索引的平均過時程度，比現有平均值高出太多，這項快訊就會通知您。預設門檻為 4 小時內的平均值超過先前平均值的兩倍，且持續超過 30 分鐘。觸發這項警告時，建議您[增加預留項目大小](https://docs.cloud.google.com/bigquery/docs/reservations-tasks?hl=zh-tw#update_reservations)，或建立[背景預留項目](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#assignments) (如果尚未建立)。

如要設定這項警告，請按照下列步驟操作：

1. 如果尚未設定 [Monitoring 通知管道](https://docs.cloud.google.com/monitoring/support/notification-options?hl=zh-tw#creating_channels)，請先完成設定。
2. 前往「Integrations」(整合) 頁面。

   [前往「整合」頁面](https://console.cloud.google.com/monitoring/integrations?hl=zh-tw)
3. 找到 **BigQuery** 整合項目，然後點選「查看詳細資料」。
4. 在「Alerts」(快訊) 分頁中，選取「Column Metadata Index Staleness - Too Much Percent Increase」(資料欄中繼資料索引過時程度 - 百分比增幅過高)。
5. 選用：如要進一步自訂這項警告，請依序點選
   **「Show options」(顯示選項) >「Customize alert policy」(自訂警告政策)**。
6. 在「設定通知」部分，選取通知管道。
7. 點選「建立」。

## 效能注意事項

雖然 BigQuery 會使用分區和分群功能自動剪除資料，但中繼資料索引功能可根據未用於分區或分群的資料欄剪除資料，進一步最佳化查詢。如果篩選條件欄與資料表的分割或分群欄之間存在排序依附關係，則這種剪枝作業的成效會提高。在這種情況下，即使篩選的資料欄並非資料表分群設定的一部分，掃描的位元組數仍可能低於預期。如果資料表僅分區但未分群，則隨選查詢的剪除效果有限，且掃描的位元組數可能不會減少。

## 限制

中繼資料查詢效能強化功能僅適用於 `SELECT`、`INSERT` 和 `CREATE TABLE AS SELECT` 陳述式。data manipulation language (DML) 陳述式不會因中繼資料索引而提升效能。

## 後續步驟

* 瞭解如何使用 [`JOBS` 檢視畫面](https://docs.cloud.google.com/bigquery/docs/information-schema-jobs?hl=zh-tw)查看專案中的所有工作。
* 瞭解如何[查看運算單元容量和使用率](https://docs.cloud.google.com/bigquery/docs/slot-estimator?hl=zh-tw#view_slot_capacity_and_utilization)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-10-23 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-10-23 (世界標準時間)。"],[],[]]