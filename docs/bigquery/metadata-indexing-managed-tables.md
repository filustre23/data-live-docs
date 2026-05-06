Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# BigQuery 資料表的中繼資料索引

本文說明 BigQuery 中的資料欄中繼資料索引，並說明如何分配專屬資源，提升索引新鮮度和查詢效能。

如果 BigQuery 資料表超過 1 GiB，BigQuery 會自動為中繼資料建立索引。這類中繼資料包括檔案位置、分割資訊和資料欄層級屬性，BigQuery 會使用這些資料來最佳化及加速查詢。

根據預設，BigQuery 中的中繼資料索引作業是免費的背景作業，您不必執行任何操作。不過，索引新鮮度取決於可用的免費資源，且沒有效能服務等級目標 (SLO)。如果索引新鮮度對您的用途至關重要，建議設定[`BACKGROUND`預訂](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#assignments)，在背景最佳化作業之間共用資源。

## 查看中繼資料索引的重新整理時間

如要查看資料表的上次中繼資料索引重新整理時間，請查詢 [`INFORMATION_SCHEMA.TABLE_STORAGE` 檢視的 `LAST_METADATA_INDEX_REFRESH_TIME` 欄](https://docs.cloud.google.com/bigquery/docs/information-schema-table-storage?hl=zh-tw)。方法如下：

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

   * `PROJECT_ID`： Google Cloud 專案的 ID。
     如未指定，系統會使用預設專案。
   * `REGION`：專案所在的[區域](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)，例如 `region-us`。
3. 按一下「執行」play\_circle。

## 查看資料欄中繼資料索引使用情況

如要查看工作完成後是否使用了資料欄中繼資料索引，請檢查 [Job](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw) 資源的 [`TableMetadataCacheUsage` 屬性](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#tablemetadatacacheusage)。如果 `unusedReason` 欄位空白 (未填入資料)，系統就會使用資料欄中繼資料索引。如果已填入值，隨附的 `explanation` 欄位會說明未使用資料欄中繼資料索引的原因。

您也可以使用 [`INFORMATION_SCHEMA.JOBS` 檢視區塊中的 `metadata_cache_statistics` 欄位，查看資料欄中繼資料索引的使用情形](https://docs.cloud.google.com/bigquery/docs/information-schema-jobs?hl=zh-tw)。

舉例來說，以下顯示 `my-job` 工作的資料欄中繼資料索引使用情形：

```
SELECT metadata_cache_statistics
FROM `region-US`.INFORMATION_SCHEMA.JOBS
WHERE job_id = 'my-job';
```

再舉一例，以下顯示使用 `my-table` 資料表資料欄中繼資料索引的工作數量：

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

## 設定專屬的索引資源

如要在專案中設定中繼資料索引更新的資源，您必須先為專案指派預留項目。方法如下：

1. [建立`BACKGROUND`預留項目](https://docs.cloud.google.com/bigquery/docs/reservations-tasks?hl=zh-tw)。
2. [將專案指派給預留項目](https://docs.cloud.google.com/bigquery/docs/reservations-assignments?hl=zh-tw#assign_my_prod_project_to_prod_reservation)。

設定預留空間後，請選取下列其中一種方法，將配額指派給中繼資料索引工作。根據預設，以這種方式分配的運算單元會在閒置時與其他工作共用。詳情請參閱「[閒置時段](https://docs.cloud.google.com/bigquery/docs/slots?hl=zh-tw#idle_slots)」。

### 控制台

1. 前往 Google Cloud 控制台的「容量管理」頁面。

   [前往「容量管理」](https://console.cloud.google.com/bigquery/admin/reservations?hl=zh-tw)
2. 依序點選 more\_vert「預訂動作」**>「建立指派項目」**。
3. 選取預留專案。
4. 將「Job Type」(工作類型) 設為「Background」(背景)。
5. 點選「建立」。

### bq

使用 [`bq mk` 指令](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_mk)。

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

* `ADMIN_PROJECT_ID`：[管理專案](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#admin-project)的專案 ID，該專案擁有預留資源。
* `LOCATION`：預訂的[地點](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)。
* `RESERVATION_NAME`：預訂名稱。
* `PROJECT_ID`：要指派給這項預留量的專案 ID。

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

   請替換下列項目：
   * `ADMIN_PROJECT_ID`：[管理專案](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#admin-project)的專案 ID，該專案擁有預留資源。
   * `LOCATION`：預訂的[地點](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)。
   * `RESERVATION_NAME`：預訂名稱。
   * `ASSIGNMENT_ID`：作業 ID。ID 在專案和位置中不得重複，只能使用小寫英文字母、數字和破折號，開頭和結尾須為小寫英文字母或數字。
   * `PROJECT_ID`：包含表格的專案 ID。這項專案已指派給預留項目。
3. 按一下「執行」play\_circle。

## 查看索引工作資訊

設定專屬的索引工作後，您可以使用 [`JOBS` 檢視畫面](https://docs.cloud.google.com/bigquery/docs/information-schema-jobs?hl=zh-tw)，查看索引工作的相關資訊。下列 SQL 範例會顯示 PROJECT\_NAME 中最新的五項重新整理工作。

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

將 `PROJECT_NAME` 替換為包含中繼資料索引作業的專案名稱。

## 設定中繼資料索引警告

如果 BigQuery 效能未達到既定條件，Cloud Monitoring 快訊程序會通知您。詳情請參閱「[快訊總覽](https://docs.cloud.google.com/monitoring/alerts?hl=zh-tw)」。透過中繼資料索引，您可以設定版位用量和過時的快訊。

### 運算單元用量快訊

如果背景預訂量超過分配量的特定百分比，系統就會發送這則快訊。預設值為 95%。您可以針對特定預訂或所有背景預訂設定這項快訊。觸發這項快訊時，建議您[增加預訂大小](https://docs.cloud.google.com/bigquery/docs/reservations-tasks?hl=zh-tw#update_reservations)。

如要為每個背景預訂設定這項快訊，請按照下列步驟操作：

1. 如果尚未設定，請先設定[監控通知管道](https://docs.cloud.google.com/monitoring/support/notification-options?hl=zh-tw#creating_channels)。
2. 前往「整合」頁面。

   [前往「整合」](https://console.cloud.google.com/monitoring/integrations?hl=zh-tw)
3. 找到 **BigQuery** 整合功能，然後按一下「查看詳細資料」。
4. 在「快訊」分頁中，選取「Slot Usage - Background Metadata Cache Slot Usage Too High」。
5. (選用) 如要進一步自訂這項快訊，請依序點選「顯示選項」**>「自訂快訊政策」**。
6. 在「設定通知」中，選取通知管道。
7. 點選「建立」。

### 過時警報

如果資料欄中繼資料索引的平均過時程度與現有平均值相比增加太多，系統就會發送這則快訊。預設門檻為：如果 4 小時的平均值超過前一個平均值的兩倍，且持續超過 30 分鐘，觸發這項快訊時，建議您[增加預訂大小](https://docs.cloud.google.com/bigquery/docs/reservations-tasks?hl=zh-tw#update_reservations)，或建立[背景預訂](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#assignments) (如果沒有的話)。

如要設定這項快訊，請按照下列步驟操作：

1. 如果尚未設定，請先設定[監控通知管道](https://docs.cloud.google.com/monitoring/support/notification-options?hl=zh-tw#creating_channels)。
2. 前往「整合」頁面。

   [前往「整合」](https://console.cloud.google.com/monitoring/integrations?hl=zh-tw)
3. 找到 **BigQuery** 整合功能，然後按一下「查看詳細資料」。
4. 在「快訊」分頁中，選取「資料欄中繼資料索引過時程度 - 增加百分比過高」。
5. (選用) 如要進一步自訂這項快訊，請依序點選「顯示選項」**>「自訂快訊政策」**。
6. 在「設定通知」中，選取通知管道。
7. 點選「建立」。

## 限制

中繼資料查詢效能提升功能僅適用於 `SELECT`、`INSERT` 和 `CREATE TABLE AS SELECT` 陳述式。資料操縱語言 (DML) 陳述式不會因中繼資料索引而有所改善。

## 後續步驟

* 瞭解如何使用 [`JOBS` 檢視畫面](https://docs.cloud.google.com/bigquery/docs/information-schema-jobs?hl=zh-tw)查看專案中的所有工作。
* 瞭解如何[查看運算單元數量和使用率](https://docs.cloud.google.com/bigquery/docs/slot-estimator?hl=zh-tw#view_slot_capacity_and_utilization)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-06 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-06 (世界標準時間)。"],[],[]]