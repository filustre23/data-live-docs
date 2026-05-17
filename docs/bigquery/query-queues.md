Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 使用查詢佇列

BigQuery 會自動決定可並行執行的查詢數量，也就是*動態並行*。其他查詢會排入佇列，直到處理資源可供使用。本文說明如何控管最大並行目標，以及設定互動式和批次查詢的佇列逾時。

## 總覽

BigQuery 會根據可用的運算資源，動態決定可同時執行的查詢數量。系統會根據隨選專案或[預訂](https://docs.cloud.google.com/bigquery/docs/reservations-intro?hl=zh-tw)，計算可同時執行的查詢數量。其他查詢會排入佇列，直到有足夠容量可供執行為止。無論專案是隨選還是使用預訂，每個專案在每個區域的佇列長度上限為 1,000 個互動式查詢和 20,000 個批次查詢。以下範例顯示當計算出的查詢並行數為 202 時，隨選專案的行為：

對於預訂，您可以選擇[設定並行目標上限](#set_the_maximum_concurrency_target)，也就是預訂中可並行執行的查詢數量上限，確保每個查詢都能分配到一定數量的運算單元。您無法為隨選專案指定並行目標上限，系統一律會動態計算。

## 排隊行為

BigQuery 會強制執行[公平排程](https://docs.cloud.google.com/bigquery/docs/slots?hl=zh-tw#fair_scheduling_in_bigquery)，確保單一專案不會耗用保留項目中的所有運算單元。

系統會優先將並行比例最低的專案查詢從佇列中移除。執行期間，系統會先將運算單元平均分配給各個專案，然後再分配給專案中的工作。

舉例來說，假設您有一個指派給兩個專案的預訂：A 和 B。BigQuery 會計算預留項目的並行數為 5。專案 A 有四項查詢同時執行，專案 B 有一項查詢正在執行，其他查詢則在佇列中等待。即使專案 B 的查詢是在專案 A 的查詢之後提交，系統仍會先將專案 B 的查詢從佇列中移除。查詢開始執行後，會獲得共用預留位置的公平分配。

除了並行查詢總數外，BigQuery 還會動態決定每個隨選專案或預訂可執行的並行批次查詢數量上限。如果並行執行的批次查詢數量達到上限，系統會優先處理互動式查詢，即使這些查詢是稍後才提交也一樣。

刪除預留項目後，所有已排入佇列的查詢都會逾時。如果指派給預留項目的專案重新指派給其他預留項目，所有已排入佇列或正在執行的要求都會繼續在舊預留項目中執行，而所有新要求都會前往新預留項目。從保留項目移除指派給保留項目的專案後，執行中的查詢會繼續使用保留項目，而新的要求和佇列要求則會使用隨選模型執行。您可以視需要[取消](https://docs.cloud.google.com/bigquery/docs/managing-jobs?hl=zh-tw#cancel_jobs)個別執行中或已排入佇列的查詢作業。

## 控制佇列逾時

如要控管互動式或批次查詢的佇列逾時，請使用 [`ALTER PROJECT SET OPTIONS` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#alter_project_set_options_statement)或 [`ALTER ORGANIZATION SET OPTIONS` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#alter_organization_set_options_statement)，在專案或機構的[預設設定](https://docs.cloud.google.com/bigquery/docs/default-configuration?hl=zh-tw)中設定 `default_interactive_query_queue_timeout_ms` 或 `default_batch_query_queue_timeout_ms` 欄位。

如要查看專案中互動式或批次查詢的佇列逾時，請查詢 [`INFORMATION_SCHEMA.EFFECTIVE_PROJECT_OPTIONS` 檢視區塊](https://docs.cloud.google.com/bigquery/docs/information-schema-effective-project-options?hl=zh-tw)。

如要停用佇列功能，請將佇列逾時設為 -1。如果達到查詢並行上限，額外查詢會失敗並顯示 `ADMISSION_DENIED` 錯誤。

## 設定並行上限目標

建立預訂時，您可以手動設定並行目標上限。根據預設，並行目標上限為零，也就是說，BigQuery 會根據可用資源動態決定並行數量。否則，如果您設定非零目標，並行目標上限會指定在預留項目中同時執行的查詢數量上限，確保每個執行的查詢都有最低的運算單元容量。

即使提高並行上限目標，系統也不一定會同時執行更多查詢。實際的並行情況取決於可用的運算資源，您可以為預留項目新增更多運算單元，藉此增加運算資源。

### 必要的角色

如要取得設定新預留項目並行數所需的權限，請要求管理員在[管理專案](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#admin-project)中授予您 [BigQuery 資源編輯者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.resourceEditor)  (`roles/bigquery.resourceEditor`) IAM 角色，該專案會維護承諾使用項目的擁有權。如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和機構的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

這個預先定義的角色具備 `bigquery.reservations.create` 權限，可為新預訂設定並行數。

您或許還可透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)取得這項權限。

如要進一步瞭解 BigQuery 中的 IAM 角色，請參閱[預先定義的角色與權限](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)一文。

### 設定預留項目的並行上限目標

選取下列選項之一：

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在導覽選單中，按一下「容量管理」。
3. 按一下「建立預留項目」。
4. 選取[預訂設定](https://docs.cloud.google.com/bigquery/docs/reservations-tasks?hl=zh-tw#create_a_reservation_with_dedicated_slots)。
5. 如要展開「進階設定」部分，請按一下expand\_more展開箭頭。
6. 如要設定目標工作並行，請將「覆寫自動目標工作並行設定」切換鈕設為開啟，然後輸入「目標工作並行」。
7. 按一下 [儲存]。

### SQL

如要為新預訂設定並行上限目標，請使用 [`CREATE RESERVATION` DDL 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#create_reservation_statement)，並設定 [`target_job_concurrency` 欄位](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#reservation_option_list)。

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列陳述式：

   ```
   CREATE RESERVATION `ADMIN_PROJECT_ID.LOCATION.RESERVATION_NAME`
     OPTIONS (
       target_job_concurrency = CONCURRENCY);
   ```

   請替換下列項目：

   * `ADMIN_PROJECT_ID`：擁有預留空間的專案
   * `LOCATION`：預訂位置，例如 `region-us`
   * `RESERVATION_NAME`：預留項目名稱
   * `CONCURRENCY`：並行作業數量上限目標
3. 按一下「執行」play\_circle。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

### bq

如要為新預留項目設定並行上限目標，請執行 [`bq mk` 指令](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_mk)：

```
bq mk \
    --project_id=ADMIN_PROJECT_ID \
    --location=LOCATION \
    --target_job_concurrency=CONCURRENCY \
    --reservation \
    RESERVATION_NAME
```

更改下列內容：

* `ADMIN_PROJECT_ID`：擁有預留空間的專案
* `LOCATION`：預訂位置
* `CONCURRENCY`：並行作業數量上限目標
* `RESERVATION_NAME`：預留項目名稱

### API

如要在 [BigQuery Reservation API](https://docs.cloud.google.com/bigquery/docs/reference/reservations/rpc?hl=zh-tw) 中設定並行上限目標，請在[預留資源](https://docs.cloud.google.com/bigquery/docs/reference/reservations/rpc/google.cloud.bigquery.reservation.v1?hl=zh-tw#reservation)中設定 `concurrency` 欄位，然後呼叫 [`CreateReservationRequest` 方法](https://docs.cloud.google.com/bigquery/docs/reference/reservations/rpc/google.cloud.bigquery.reservation.v1?hl=zh-tw#createreservationrequest)。

## 更新並行上限目標

您隨時可以更新預訂的並行上限目標。
不過，提高目標不一定會讓系統同時執行更多查詢。實際的並行情況取決於可用的運算資源。如果調降並行查詢目標上限，目前執行的查詢不會受到影響，而排入佇列的查詢會等到並行查詢數量低於新目標時才會執行。

如果將並行數量上限目標設為 0，BigQuery 會根據可用資源動態決定並行數量 (預設行為)。

### 必要的角色

如要取得更新預留項目最大並行目標所需的權限，請要求系統管理員授予您[管理專案](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#admin-project)的 [BigQuery 資源編輯者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.resourceEditor)  (`roles/bigquery.resourceEditor`) IAM 角色，該專案擁有承諾使用項目的擁有權。如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和機構的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

這個預先定義的角色具備 `bigquery.reservations.update` 權限，可更新預訂的並行上限目標。

您或許還可透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)取得這項權限。

如要進一步瞭解 BigQuery 中的 IAM 角色，請參閱[預先定義的角色與權限](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)一文。

### 更新預留項目的最大並行目標

選取下列選項之一：

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在導覽選單中，按一下「容量管理」。
3. 按一下「運算單元預留項目」分頁標籤。
4. 找出要更新的預訂。
5. 展開「動作」more\_vert選項。
6. 按一下 [編輯]。
7. 如要展開「進階設定」部分，請按一下expand\_more展開箭頭。
8. 如要設定目標工作並行，請將「覆寫自動目標工作並行設定」切換鈕設為開啟，然後輸入「目標工作並行」。
9. 按一下 [儲存]。

### SQL

如要更新現有預訂的並行上限目標，請使用 [`ALTER RESERVATION` DDL 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#alter_reservation_set_options_statement)，並設定 [`target_job_concurrency` 欄位](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#alter_reservation_option_list)。

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列陳述式：

   ```
   ALTER RESERVATION `ADMIN_PROJECT_ID.LOCATION.RESERVATION_NAME`
   SET OPTIONS (
     target_job_concurrency = CONCURRENCY);
   ```

   請替換下列項目：

   * `ADMIN_PROJECT_ID`：擁有預留空間的專案
   * `LOCATION`：預訂位置，例如 `region-us`
   * `RESERVATION_NAME`：預留項目名稱
   * `CONCURRENCY`：並行作業數量上限目標
3. 按一下「執行」play\_circle。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

### bq

如要更新現有預留項目的並行目標上限，請執行 [`bq update` 指令](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_update)：

```
bq update \
    --project_id=ADMIN_PROJECT_ID \
    --location=LOCATION \
    --target_job_concurrency=CONCURRENCY \
    --reservation \
    RESERVATION_NAME
```

更改下列內容：

* `ADMIN_PROJECT_ID`：擁有預留空間的專案
* `LOCATION`：預訂位置
* `CONCURRENCY`：並行作業數量上限目標
* `RESERVATION_NAME`：預留項目名稱

### API

如要在 [BigQuery Reservation API](https://docs.cloud.google.com/bigquery/docs/reference/reservations/rpc?hl=zh-tw) 中更新最大並行目標，請在[預訂資源](https://docs.cloud.google.com/bigquery/docs/reference/reservations/rpc/google.cloud.bigquery.reservation.v1?hl=zh-tw#reservation)中設定 `concurrency` 欄位，然後呼叫 [`UpdateReservationRequest` 方法](https://docs.cloud.google.com/bigquery/docs/reference/reservations/rpc/google.cloud.bigquery.reservation.v1?hl=zh-tw#updatereservationrequest)。

## 監控

如要瞭解哪些查詢正在執行，哪些查詢已加入佇列，請查看 [`INFORMATION_SCHEMA.JOBS_BY_*`](https://docs.cloud.google.com/bigquery/docs/information-schema-jobs?hl=zh-tw) 和 [`INFORMATION_SCHEMA.JOBS_TIMELINE_BY_*`](https://docs.cloud.google.com/bigquery/docs/information-schema-jobs-timeline?hl=zh-tw) 檢視畫面。`state` 欄位會針對正在執行的查詢設為 `RUNNING`，針對已加入佇列的查詢則設為 `PENDING`。

如要查看過去一天中，每秒達到動態並行閾值時執行的並行查詢數量，請執行下列查詢：

```
SELECT
  t1.period_start,
  t1.job_count AS dynamic_concurrency_threshold
FROM (
  SELECT
    period_start,
    state,
    COUNT(DISTINCT job_id) AS job_count
  FROM
    `PROJECT_ID.REGION_ID`.INFORMATION_SCHEMA.JOBS_TIMELINE
  WHERE
    period_start BETWEEN TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 1 DAY)
    AND CURRENT_TIMESTAMP()
    AND reservation_id = "RESERVATION_ID"
  GROUP BY
    period_start,
    state) AS t1
JOIN (
  SELECT
    period_start,
    state,
    COUNT(DISTINCT job_id) AS job_count
  FROM
    `PROJECT_ID.REGION_ID`.INFORMATION_SCHEMA.JOBS_TIMELINE
  WHERE
    state = "PENDING"
    AND period_start BETWEEN TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 1 DAY)
    AND CURRENT_TIMESTAMP()
    AND reservation_id = "RESERVATION_ID"
  GROUP BY
    period_start,
    state
  HAVING
    COUNT(DISTINCT job_id) > 0 ) AS t2
ON
  t1.period_start = t2.period_start
WHERE
  t1.state = "RUNNING";
```

更改下列內容：

* `PROJECT_ID`：您執行查詢的專案名稱
* `REGION_ID`：處理查詢的位置
* `RESERVATION_ID`：查詢執行的預留項目名稱

**注意：** 如要查看隨選專案的動態並行數，請移除預留項目篩選條件。

您可以使用 [BigQuery 管理資源圖表](https://docs.cloud.google.com/bigquery/docs/admin-resource-charts?hl=zh-tw#view-resource-utilization)，選取「待處理」指標的「工作並行」圖表，監控預留項目的查詢佇列長度。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-16 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-16 (世界標準時間)。"],[],[]]