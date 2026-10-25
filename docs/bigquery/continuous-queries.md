Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 建立持續查詢

本文說明如何在 BigQuery 執行[持續查詢](https://docs.cloud.google.com/bigquery/docs/continuous-queries-introduction?hl=zh-tw)。

BigQuery 持續查詢是持續執行的 SQL 陳述式，能近乎即時地處理資料。您可以將持續查詢產生的輸出資料列，寫入或匯出至下列目的地：

* BigQuery 資料表
* [Apache Iceberg 代管資料表](https://docs.cloud.google.com/bigquery/docs/biglake-iceberg-tables-in-bigquery?hl=zh-tw)
* Pub/Sub 主題
* Bigtable 資料表
* Spanner 資料表

## 選擇帳戶類型

您可以使用使用者帳戶建立及執行持續查詢工作，也可以使用使用者帳戶建立持續查詢工作，然後使用[服務帳戶](https://docs.cloud.google.com/iam/docs/service-account-overview?hl=zh-tw)執行。您必須使用服務帳戶，才能執行將結果匯出至 Pub/Sub 主題的持續查詢。

如果使用使用者帳戶，持續查詢最多可執行兩天。使用服務帳戶時，持續查詢最多可執行 150 天。詳情請參閱「[授權](https://docs.cloud.google.com/bigquery/docs/continuous-queries-introduction?hl=zh-tw#authorization)」。

## 所需權限

本節說明建立及執行持續查詢所需的權限。除了上述 Identity and Access Management (IAM) 角色，您也可以透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)取得必要權限。

### 使用使用者帳戶時的權限

本節說明使用使用者帳戶建立及執行持續查詢所需的角色和權限。

如要在 BigQuery 中建立工作，使用者帳戶必須具備 `bigquery.jobs.create` IAM 權限。下列各項 IAM 角色都會授予 `bigquery.jobs.create` 權限：

* [BigQuery 使用者 (`roles/bigquery.user`)](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.user)
* [BigQuery 工作使用者 (`roles/bigquery.jobUser`)](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.jobUser)
* [BigQuery 管理員 (`roles/bigquery.admin`)](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.admin)

如要從 BigQuery 資料表匯出資料，使用者帳戶必須具備 `bigquery.tables.export` IAM 權限。下列各項 IAM 角色都會授予 `bigquery.tables.export` 權限：

* [BigQuery 資料檢視者 (`roles/bigquery.dataViewer`)](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.dataViewer)
* [BigQuery 資料編輯者 (`roles/bigquery.dataEditor`)](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.dataEditor)
* [BigQuery 資料擁有者 (`roles/bigquery.dataOwner`)](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.dataOwner)
* [BigQuery 管理員 (`roles/bigquery.admin`)](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.admin)

如要將資料寫入 BigQuery 資料表，使用者帳戶必須具備 `bigquery.tables.updateData` IAM 權限。下列各項 IAM 角色都會授予 `bigquery.tables.updateData` 權限：

* [BigQuery 資料編輯者 (`roles/bigquery.dataEditor`)](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.dataEditor)
* [BigQuery 資料擁有者 (`roles/bigquery.dataOwner`)](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.dataOwner)
* [BigQuery 管理員 (`roles/bigquery.admin`)](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.admin)

如果使用者帳戶必須啟用持續查詢用途所需的 API，則須具備[服務使用情形管理員 (`roles/serviceusage.serviceUsageAdmin`)](https://docs.cloud.google.com/iam/docs/roles-permissions/serviceusage?hl=zh-tw#serviceusage.serviceUsageAdmin) 角色。

如要將資料寫入 [Apache Iceberg 代管資料表](https://docs.cloud.google.com/bigquery/docs/biglake-iceberg-tables-in-bigquery?hl=zh-tw)，除了 BigQuery 權限外，使用者帳戶還必須具備 [BigQuery 連線使用者 (`roles/bigquery.connectionUser`)](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.connectionUser) 角色，才能使用與 Iceberg 代管資料表相關聯的 Google Cloud 資源連線。此外，與該連線相關聯的服務帳戶必須具備基礎 Cloud Storage bucket 的適當權限 (例如 [`roles/storage.objectUser`](https://docs.cloud.google.com/storage/docs/access-control/iam-roles?hl=zh-tw#storage.objectUser) 和 `roles/storage.legacyBucketReader`)。詳情請參閱「[建立及使用 Apache Iceberg 代管資料表](https://docs.cloud.google.com/bigquery/docs/biglake-iceberg-tables-in-bigquery?hl=zh-tw)」。

### 使用服務帳戶時的權限

本節說明建立持續查詢的使用者帳戶，以及執行持續查詢的服務帳戶，分別需要哪些角色和權限。

#### 使用者帳戶權限

如要在 BigQuery 中建立工作，使用者帳戶必須具備 `bigquery.jobs.create` IAM 權限。下列各項 IAM 角色會授予 `bigquery.jobs.create` 權限：

* [BigQuery 使用者 (`roles/bigquery.user`)](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.user)
* [BigQuery 工作使用者 (`roles/bigquery.jobUser`)](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.jobUser)
* [BigQuery 管理員 (`roles/bigquery.admin`)](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.admin)

如要提交使用服務帳戶執行的工作，使用者帳戶必須具備[服務帳戶使用者 (`roles/iam.serviceAccountUser`)](https://docs.cloud.google.com/iam/docs/service-account-permissions?hl=zh-tw#user-role) 角色。如果您使用相同的使用者帳戶建立服務帳戶，則使用者帳戶必須具備[服務帳戶管理員 (`roles/iam.serviceAccountAdmin`)](https://docs.cloud.google.com/iam/docs/roles-permissions/iam?hl=zh-tw#iam.serviceAccountUser) 角色。如要瞭解如何限制使用者只能存取單一服務帳戶，而非專案中的所有服務帳戶，請參閱「[授予單一角色](https://docs.cloud.google.com/iam/docs/manage-access-service-accounts?hl=zh-tw#grant-single-role)」。

如果使用者帳戶必須啟用持續查詢用途所需的 API，則須具備[服務使用情形管理員 (`roles/serviceusage.serviceUsageAdmin`)](https://docs.cloud.google.com/iam/docs/roles-permissions/serviceusage?hl=zh-tw#serviceusage.serviceUsageAdmin) 角色。

#### 服務帳戶權限

如要從 BigQuery 資料表匯出資料，服務帳戶必須具備 `bigquery.tables.export` IAM 權限。下列各項 IAM 角色都會授予 `bigquery.tables.export` 權限：

* [BigQuery 資料檢視者 (`roles/bigquery.dataViewer`)](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.dataViewer)
* [BigQuery 資料編輯者 (`roles/bigquery.dataEditor`)](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.dataEditor)
* [BigQuery 資料擁有者 (`roles/bigquery.dataOwner`)](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.dataOwner)
* [BigQuery 管理員 (`roles/bigquery.admin`)](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.admin)

如要將資料寫入 BigQuery 資料表，服務帳戶必須具備 `bigquery.tables.updateData` IAM 權限。下列各項 IAM 角色都會授予 `bigquery.tables.updateData` 權限：

* [BigQuery 資料編輯者 (`roles/bigquery.dataEditor`)](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.dataEditor)
* [BigQuery 資料擁有者 (`roles/bigquery.dataOwner`)](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.dataOwner)
* [BigQuery 管理員 (`roles/bigquery.admin`)](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.admin)

如要將資料寫入 [Apache Iceberg 代管資料表](https://docs.cloud.google.com/bigquery/docs/biglake-iceberg-tables-in-bigquery?hl=zh-tw)，除了 BigQuery 權限外，服務帳戶還必須具備 [BigQuery 連線使用者 (`roles/bigquery.connectionUser`)](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.connectionUser) 角色，才能使用與 Iceberg 代管資料表相關聯的 Google Cloud 資源連線。此外，與該連線相關聯的服務帳戶，必須具備基礎 Cloud Storage bucket 的適當權限 (例如 [`roles/storage.objectUser`](https://docs.cloud.google.com/storage/docs/access-control/iam-roles?hl=zh-tw#storage.objectUser) 和 `roles/storage.legacyBucketReader`)。詳情請參閱「[建立及使用 Apache Iceberg 代管資料表](https://docs.cloud.google.com/bigquery/docs/biglake-iceberg-tables-in-bigquery?hl=zh-tw)」。

## 事前準備

1. 在 Google Cloud 控制台的專案選取器頁面中，選取或建立 Google Cloud 專案。

   **選取或建立專案所需的角色**

   * **選取專案**：選取專案時，不需具備特定 IAM 角色，只要您在專案中獲派角色，即可選取該專案。
   * **建立專案**：如要建立專案，您必須具備專案建立者角色 (`roles/resourcemanager.projectCreator`)，其中包含 `resourcemanager.projects.create` 權限。[瞭解如何授予角色](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)。
   **注意**：如果您不打算保留在這項程序中建立的資源，請建立新專案，不要選取現有專案。如果採用這種做法，當您完成這些步驟後，就可以直接刪除該專案，並移除相關聯的所有資源。

   [前往專案選取器](https://console.cloud.google.com/projectselector2/home/dashboard?hl=zh-tw)
2. [確認 Google Cloud 專案已啟用計費功能](https://docs.cloud.google.com/billing/docs/how-to/verify-billing-enabled?hl=zh-tw#confirm_billing_is_enabled_on_a_project)。
3. 啟用 BigQuery API (如果尚未啟用)。

   **啟用 API 所需的角色**

   如要啟用 API，您必須具備 `serviceusage.services.enable` 權限。如果您建立了專案，可能已透過擁有者角色 (`roles/owner`) 取得這項權限。否則，您可以透過服務使用情形管理員角色 (`roles/serviceusage.serviceUsageAdmin`) 取得這項權限。[瞭解如何授予角色](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)。

   [啟用 API](https://console.cloud.google.com/apis/enableflow?apiid=bigquery.googleapis.com&hl=zh-tw)

### 建立預留項目

[建立 Enterprise 或 Enterprise Plus 版預留項目](https://docs.cloud.google.com/bigquery/docs/reservations-tasks?hl=zh-tw#create_reservations)，然後[建立預留項目指派作業](https://docs.cloud.google.com/bigquery/docs/reservations-assignments?hl=zh-tw#create_reservation_assignments)，並指定 `CONTINUOUS` 工作類型。這項預留項目可以使用[自動調度資源](https://docs.cloud.google.com/bigquery/docs/continuous-queries-introduction?hl=zh-tw#slots_autoscaling)和[閒置運算單元共用](https://docs.cloud.google.com/bigquery/docs/slots?hl=zh-tw#idle_slots)功能。持續查詢的預留項目指派作業有[預留項目限制](https://docs.cloud.google.com/bigquery/docs/continuous-queries-introduction?hl=zh-tw#reservation_limitations)。

## 匯出至 Pub/Sub

如要將資料匯出至 Pub/Sub，必須具備額外的 API、IAM 權限和 Google Cloud 資源。詳情請參閱「[匯出至 Pub/Sub](https://docs.cloud.google.com/bigquery/docs/export-to-pubsub?hl=zh-tw)」。

### 使用 `CHANGES` 處理異動

**預覽**

這項功能適用《[服務專屬條款](https://docs.cloud.google.com/terms/service-terms?hl=zh-tw#1)》中「一般服務條款」一節的《正式發布前產品條款》。正式發布前功能是依「原樣」提供，支援服務可能受限。
詳情請參閱[推出階段說明](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages)。

將資料匯出至 Pub/Sub 時，您可以選擇使用 [`CHANGES` 變更記錄函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/time-series-functions?hl=zh-tw#changes)。`CHANGES` 函式會處理來源資料表中所有已變更的資料列，包括附加和變動。

### 將自訂屬性嵌入 Pub/Sub 訊息做為中繼資料

您可以使用 [Pub/Sub 屬性](https://docs.cloud.google.com/pubsub/docs/publisher?hl=zh-tw#using-attributes)提供訊息的其他資訊，例如優先順序、來源、目的地或其他中繼資料。您也可以使用屬性[篩選訂閱項目的訊息](https://docs.cloud.google.com/pubsub/docs/subscription-message-filter?hl=zh-tw)。

在持續查詢結果中，如果資料欄名稱為 `_ATTRIBUTES`，其值會複製到 Pub/Sub 訊息屬性。`_ATTRIBUTES` 中提供的欄位會做為屬性鍵。

`_ATTRIBUTES` 欄必須是 `JSON` 類型，格式為 `ARRAY<STRUCT<STRING, STRING>>` 或 `STRUCT<STRING>`。

如需範例，請參閱「[將資料匯出至 Pub/Sub 主題](https://docs.cloud.google.com/bigquery/docs/continuous-queries?hl=zh-tw#pubsub-example)」。

## 匯出至 Bigtable

您需要額外的 API、IAM 權限和 Google Cloud資源，才能將資料匯出至 Bigtable。詳情請參閱「[匯出至 Bigtable](https://docs.cloud.google.com/bigquery/docs/export-to-bigtable?hl=zh-tw)」。

## 匯出至 Spanner

您必須具備其他 API、IAM 權限和 Google Cloud資源，才能將資料匯出至 Spanner。詳情請參閱「[匯出至 Spanner (反向 ETL)](https://docs.cloud.google.com/bigquery/docs/export-to-spanner?hl=zh-tw)」。

## 將資料寫入 BigQuery 資料表或 Apache Iceberg 代管資料表

您可以使用 [`INSERT` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/dml-syntax?hl=zh-tw#insert_statement)，將資料寫入 BigQuery 資料表或 [Iceberg 代管資料表](https://docs.cloud.google.com/bigquery/docs/biglake-iceberg-tables-in-bigquery?hl=zh-tw)。

將持續查詢輸出內容寫入 Iceberg 代管資料表時：

* 建立持續查詢前，目的地 Iceberg 代管資料表必須已存在。如要瞭解如何建立 Iceberg 代管資料表，請參閱「[建立及使用 Apache Iceberg 代管資料表](https://docs.cloud.google.com/bigquery/docs/biglake-iceberg-tables-in-bigquery?hl=zh-tw)」。
* 查詢語法與寫入標準 BigQuery 資料表相同。您可以在 `INSERT INTO` 子句中指定目的地資料表，不必在 SQL 陳述式中指定連線或 bucket 選項。
* 執行持續查詢的使用者帳戶或服務帳戶，必須具備目的地資料表、 Google Cloud 資源連線和基礎 Cloud Storage bucket 的必要權限。詳情請參閱「[必要權限](#required_permissions)」。

如需範例，請參閱「[將資料寫入 BigQuery 資料表或 Apache Iceberg 代管資料表](#bigquery-insert-example)」。

## 使用 AI 函式

您必須具備其他 API、IAM 權限和 Google Cloud資源，才能在持續查詢中使用[支援的](https://docs.cloud.google.com/bigquery/docs/continuous-queries-introduction?hl=zh-tw#supported_functionality) AI 函式。詳情請參閱下列主題 (視您的用途而定)：

* [使用 `AI.GENERATE_TEXT` 函式生成文字](https://docs.cloud.google.com/bigquery/docs/generate-text-tutorial?hl=zh-tw)
* [使用 `AI.GENERATE_EMBEDDING` 函式生成文字嵌入](https://docs.cloud.google.com/bigquery/docs/generate-text-embedding?hl=zh-tw)
* [使用 `ML.UNDERSTAND_TEXT` 函式解讀文字](https://docs.cloud.google.com/bigquery/docs/understand-text?hl=zh-tw)
* [使用 `ML.TRANSLATE` 函式翻譯文字](https://docs.cloud.google.com/bigquery/docs/translate-text?hl=zh-tw)

在持續查詢中使用 AI 函式時，請考量查詢輸出內容是否會超出函式的[配額](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#cloud_ai_service_functions)。如果超出配額，您可能需要另外處理未處理的記錄。

## 指定持續查詢的開始時間

您必須在持續查詢的 `FROM` 子句中，使用 [`APPENDS` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/time-series-functions?hl=zh-tw#appends)，或在[匯出至 Pub/Sub](https://docs.cloud.google.com/bigquery/docs/export-to-pubsub?hl=zh-tw) 時使用 [`CHANGES` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/time-series-functions?hl=zh-tw#changes)，指定要處理的最早資料。例如：`APPENDS(TABLE my_table, start_timestamp)`。

`start_timestamp` 引數定義持續查詢開始處理資料的時間點。舉例來說，`APPENDS(TABLE my_table, CURRENT_TIMESTAMP() - INTERVAL 10 MINUTE)` 會指示 BigQuery 處理在持續查詢開始前最多 10 分鐘內，新增至資料表 `my_table` 的資料。隨後新增至 `my_table` 的資料會在傳入時處理。資料處理不會延遲。

指定 `start_timestamp` 引數時，值必須落在資料表的[時間旅行](https://docs.cloud.google.com/bigquery/docs/time-travel?hl=zh-tw)視窗內，標準資料表的預設值為七天。如果將 `start_timestamp` 設為 `NULL`，系統會預設為資料表的建立時間。不建議使用 `NULL` 值，因為如果資料表建立時間早於時間旅行時間範圍，系統會傳回錯誤。使用 `NULL` 的查詢可能會在新建立的資料表上成功，但如果資料表的建立時間戳記超過七天，則會在之後失敗。

在持續查詢中使用 `APPENDS` 函式時，請勿提供 `end_timestamp` 引數。

**注意：** 在持續查詢中使用 `APPENDS` 函式時，該函式會視為處於[正式發布](https://cloud.google.com/products?hl=zh-tw#product-launch-stages) (GA) 階段。

以下範例說明如何使用 `APPENDS` 函式，從特定時間點開始持續查詢，查詢對象是接收計程車行程資訊串流的 BigQuery 資料表：

```
EXPORT DATA
  OPTIONS (format = 'CLOUD_PUBSUB',
    uri = 'https://pubsub.googleapis.com/projects/myproject/topics/taxi-real-time-rides') AS (
  SELECT
    TO_JSON_STRING(STRUCT(ride_id,
        timestamp,
        latitude,
        longitude)) AS message
  FROM
    APPENDS(TABLE `myproject.real_time_taxi_streaming.taxirides`,
      -- Configure the APPENDS TVF start_timestamp to specify when you want to
      -- start processing data using your continuous query.
      -- This example starts processing at 10 minutes before the current time.
      CURRENT_TIMESTAMP() - INTERVAL 10 MINUTE)
  WHERE
    ride_status = 'enroute');
```

### 指定早於時間旅行期間的起始點

如要納入 7 天時光旅行時間範圍以外的資料，請使用標準查詢回填資料至特定時間點，然後從該時間點開始執行持續查詢。「交接」時間戳記必須在七天內，這樣持續查詢才能從標準查詢中斷的地方繼續執行。

下列範例說明如何從接收計程車乘車資訊串流的 BigQuery 資料表回填舊資料，然後轉換為持續查詢。

1. 執行標準查詢，回填特定時間點之前的資料：

   ```
   INSERT INTO `myproject.real_time_taxi_streaming.transformed_taxirides`
   SELECT
     timestamp,
     meter_reading,
     ride_status,
     passenger_count,
     ST_Distance(
       ST_GeogPoint(pickup_longitude, pickup_latitude),
       ST_GeogPoint(dropoff_longitude, dropoff_latitude)) AS euclidean_trip_distance,
       SAFE_DIVIDE(meter_reading, passenger_count) AS cost_per_passenger
   FROM `myproject.real_time_taxi_streaming.taxirides`
     -- Include all data inserted into the table up to this handoff point.
     -- This handoff timestamp must be within the time travel window.
     FOR SYSTEM_TIME AS OF '2025-01-01 00:00:00 UTC'
   WHERE
     ride_status = 'dropoff';
   ```
2. 從查詢停止的時間點執行持續查詢：

   ```
   INSERT INTO `myproject.real_time_taxi_streaming.transformed_taxirides`
   SELECT
     timestamp,
     meter_reading,
     ride_status,
     passenger_count,
     ST_Distance(
       ST_GeogPoint(pickup_longitude, pickup_latitude),
       ST_GeogPoint(dropoff_longitude, dropoff_latitude)) AS euclidean_trip_distance,
       SAFE_DIVIDE(meter_reading, passenger_count) AS cost_per_passenger
   FROM
     APPENDS(TABLE `myproject.real_time_taxi_streaming.taxirides`,
       -- Configure the APPENDS TVF start_timestamp to start processing
       -- data right where the batch query left off + 1 microsecond.
       -- This timestamp must be within the time travel window.
       TIMESTAMP '2025-01-01 00:00:00 UTC' + INTERVAL 1 MICROSECOND)
   WHERE
     ride_status = 'dropoff';
   ```

## 使用使用者帳戶執行持續查詢

本節說明如何使用使用者帳戶執行持續查詢。持續查詢開始執行後，您可以關閉 Google Cloud 控制台、終端機視窗或應用程式，不會中斷查詢執行。使用者帳戶執行的持續查詢最多會執行兩天，然後自動停止。如要繼續處理新傳入的資料，請啟動新的持續查詢，並[指定起始點](#start_a_continuous_query_from_a_particular_point_in_time)。如要自動執行這項程序，請參閱「[重試失敗的查詢](https://docs.cloud.google.com/bigquery/docs/continuous-queries-monitor?hl=zh-tw#retry)」。

**注意：** 您必須使用[服務帳戶](#run_a_continuous_query_by_using_a_service_account)，才能執行將結果匯出至 Pub/Sub 主題的持續查詢。您無法使用使用者帳戶。

如要執行持續查詢，請按照下列步驟操作：

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中，依序點選「編輯」>「查詢模式」>「持續查詢」。如要確認這項選擇，請按一下「Confirm」(確認)。
3. 選用：如要控制查詢執行時間，請依序點選「編輯」「查詢設定」，然後以毫秒為單位設定「工作逾時」。
4. 在查詢編輯器中，輸入持續查詢的 SQL 陳述式。SQL 陳述式只能包含[支援的操作](https://docs.cloud.google.com/bigquery/docs/continuous-queries-introduction?hl=zh-tw#supported_functionality)。
5. 按一下「執行」。

### bq

1. 在 Google Cloud 控制台啟用 Cloud Shell。

   [啟用 Cloud Shell](https://console.cloud.google.com/?cloudshell=true&hl=zh-tw)

   Google Cloud 控制台底部會開啟 [Cloud Shell](https://docs.cloud.google.com/shell/docs/how-cloud-shell-works?hl=zh-tw) 工作階段，並顯示指令列提示。Cloud Shell 是已安裝 Google Cloud CLI 的殼層環境，並已設定適用於您目前專案的值。工作階段可能要幾秒鐘的時間才能初始化。
2. 在 Cloud Shell 中，使用 [`bq query` 指令](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_query)和 `--continuous` 旗標執行持續查詢：

   ```
   bq query --use_legacy_sql=false --continuous=true
   'QUERY'
   ```

   將 `QUERY` 替換為持續查詢的 SQL 陳述式。SQL 陳述式只能包含[支援的操作](https://docs.cloud.google.com/bigquery/docs/continuous-queries-introduction?hl=zh-tw#supported_functionality)。您可以使用 `--job_timeout_ms` 旗標，控管查詢執行時間。

### API

呼叫 [`jobs.insert` 方法](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs/insert?hl=zh-tw)，執行持續查詢。您必須在傳入的 [`Job` 資源](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw)的 [`JobConfigurationQuery`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#JobConfigurationQuery) 中，將 `continuous` 欄位設為 `true`。您可以視需要設定 [`jobTimeoutMs` 欄位](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#JobConfiguration.FIELDS.job_timeout_ms)，控管查詢執行時間。

```
curl --request POST \
  "https://bigquery.googleapis.com/bigquery/v2/projects/PROJECT_ID/jobs" \
  --header "Authorization: Bearer $(gcloud auth print-access-token)" \
  --header "Content-Type: application/json; charset=utf-8" \
  --data '{"configuration":{"query":{"query":"QUERY","useLegacySql":false,"continuous":true}}}' \
  --compressed
```

更改下列內容：

* `PROJECT_ID`：您的專案 ID。
* `QUERY`：持續查詢的 SQL 陳述式。SQL 陳述式只能包含[支援的操作](https://docs.cloud.google.com/bigquery/docs/continuous-queries-introduction?hl=zh-tw#supported_functionality)。

## 使用服務帳戶執行持續查詢

本節說明如何使用服務帳戶執行持續查詢。持續查詢開始執行後，您可以關閉 Google Cloud 控制台、終端機視窗或應用程式，不會中斷查詢執行。使用服務帳戶執行的持續查詢最多可執行 150 天，之後會自動停止。如要繼續處理新傳入的資料，請啟動新的持續查詢，並[指定起始點](#start_a_continuous_query_from_a_particular_point_in_time)。如要自動執行這項程序，請參閱「[重試失敗的查詢](https://docs.cloud.google.com/bigquery/docs/continuous-queries-monitor?hl=zh-tw#retry)」。

如果您使用服務帳戶跨專案執行持續查詢，必須更新組織政策，允許將某個專案的服務帳戶附加至其他專案的資源。詳情請參閱「[啟用跨專案附加服務帳戶的功能](https://docs.cloud.google.com/iam/docs/attach-service-accounts?hl=zh-tw#cross-project)」。

如要使用服務帳戶執行持續查詢，請按照下列步驟操作：

### 控制台

1. [建立服務帳戶](https://docs.cloud.google.com/iam/docs/service-accounts-create?hl=zh-tw)。
2. 將必要的[權限](#service_account_permissions)[授予](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)服務帳戶。
3. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
4. 在查詢編輯器中，依序點選「編輯」>「查詢模式」>「持續查詢」。按一下「確認」，確認這項選擇。
5. 在查詢編輯器中，依序點選「編輯」>「查詢設定」。
6. 在「Continuous query」(持續查詢) 區段，使用「Service account」(服務帳戶) 方塊選取您建立的服務帳戶。
7. 選用：如要控制查詢執行時間，請以毫秒為單位設定「Job timeout」(工作逾時)。
8. 按一下 [儲存]。
9. 在查詢編輯器中，輸入持續查詢的 SQL 陳述式。SQL 陳述式只能包含[支援的操作](https://docs.cloud.google.com/bigquery/docs/continuous-queries-introduction?hl=zh-tw#supported_functionality)。
10. 按一下「執行」。

### bq

1. [建立服務帳戶](https://docs.cloud.google.com/iam/docs/service-accounts-create?hl=zh-tw)。
2. [授予](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)服務帳戶必要的[權限](#service_account_permissions)。
3. 在 Google Cloud 控制台啟用 Cloud Shell。

   [啟用 Cloud Shell](https://console.cloud.google.com/?cloudshell=true&hl=zh-tw)

   Google Cloud 控制台底部會開啟 [Cloud Shell](https://docs.cloud.google.com/shell/docs/how-cloud-shell-works?hl=zh-tw) 工作階段，並顯示指令列提示。Cloud Shell 是已安裝 Google Cloud CLI 的殼層環境，並已設定適用於您目前專案的值。工作階段可能要幾秒鐘的時間才能初始化。
4. 在指令列中，使用 [`bq query` 指令](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_query)和下列旗標執行持續查詢：

   * 將 `--continuous` 旗標設為 `true`，即可持續查詢。
   * 使用 `--connection_property` 旗標指定要使用的服務帳戶。
   * 選用：設定 `--job_timeout_ms` 旗標，限制查詢執行階段。

   ```
   bq query --project_id=PROJECT_ID --use_legacy_sql=false \
   --continuous=true --connection_property=service_account=SERVICE_ACCOUNT_EMAIL \
   'QUERY'
   ```

   更改下列內容：

   * `PROJECT_ID`：您的專案 ID。
   * `SERVICE_ACCOUNT_EMAIL`：服務帳戶電子郵件地址。您可以前往 Google Cloud 控制台的[「Service accounts」(服務帳戶) 頁面](https://console.cloud.google.com/iam-admin/serviceaccounts?hl=zh-tw)，取得服務帳戶電子郵件地址。
   * `QUERY`：持續查詢的 SQL 陳述式。SQL 陳述式只能包含[支援的操作](https://docs.cloud.google.com/bigquery/docs/continuous-queries-introduction?hl=zh-tw#supported_functionality)。

### API

1. [建立服務帳戶](https://docs.cloud.google.com/iam/docs/service-accounts-create?hl=zh-tw)。
2. 將必要的[權限](#service_account_permissions)[授予](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)服務帳戶。
3. 呼叫 [`jobs.insert` 方法](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs/insert?hl=zh-tw)，執行持續查詢。在傳入的 [`Job` 資源](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw)中，設定 [`JobConfigurationQuery` 資源](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#JobConfigurationQuery)的下列欄位：

   * 將 `continuous` 欄位設為 `true`，即可持續執行查詢。
   * 使用 `connectionProperties` 欄位指定要使用的服務帳戶。

   您也可以在 [`JobConfiguration` 資源](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#jobconfiguration)中設定 [`jobTimeoutMs` 欄位](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#JobConfiguration.FIELDS.job_timeout_ms)，控管查詢執行時間。

   ```
   curl --request POST \
     "https://bigquery.googleapis.com/bigquery/v2/projects/PROJECT_ID/jobs" \
     --header "Authorization: Bearer $(gcloud auth print-access-token)" \
     --header "Content-Type: application/json; charset=utf-8" \
     --data '{"configuration":{"query":{"query":"QUERY","useLegacySql":false,"continuous":true,"connectionProperties":[{"key":"service_account","value":"SERVICE_ACCOUNT_EMAIL"}]}}}' \
     --compressed
   ```

   更改下列內容：

   * `PROJECT_ID`：您的專案 ID。
   * `QUERY`：持續查詢的 SQL 陳述式。SQL 陳述式只能包含[支援的操作](https://docs.cloud.google.com/bigquery/docs/continuous-queries-introduction?hl=zh-tw#supported_functionality)。
   * `SERVICE_ACCOUNT_EMAIL`：服務帳戶電子郵件地址。您可以在 Google Cloud 控制台的[「Service accounts」(服務帳戶) 頁面](https://console.cloud.google.com/iam-admin/serviceaccounts?hl=zh-tw)取得服務帳戶電子郵件。

## 建立自訂工作 ID

每項查詢工作都會指派工作 ID，可用於搜尋及管理工作。根據預設，工作 ID 是隨機產生。如要使用[工作記錄](https://docs.cloud.google.com/bigquery/docs/managing-jobs?hl=zh-tw#list_jobs_in_a_project)或[工作探索工具](https://docs.cloud.google.com/bigquery/docs/admin-jobs-explorer?hl=zh-tw#filter-jobs)，輕鬆搜尋持續查詢的工作 ID，可以指派自訂工作 ID 前置字串：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中，依序點選「Edit」(編輯) >「Query mode」(查詢模式) >「Continuous query」(持續查詢)。
3. 按一下「確認」。
4. 在查詢編輯器中，依序點選「編輯」>「查詢設定」。
5. 在「Custom job ID prefix」(自訂工作 ID 前置字串) 部分，輸入自訂名稱前置字串。
6. 按一下 [儲存]。

## 使用 `JOIN` 和視窗匯總進行有狀態處理

有狀態作業可保留多個資料列或時間間隔的資訊，讓持續查詢執行複雜的分析。這些作業包括 `JOIN` 和視窗化匯總。

如要進一步瞭解如何使用這些有狀態作業，請參閱下列主題：

* [持續查詢`JOIN`](https://docs.cloud.google.com/bigquery/docs/continuous-query-joins?hl=zh-tw)會對多個時間導向的資料串流執行即時關聯。
* [視窗匯總](https://docs.cloud.google.com/bigquery/docs/window-aggregations?hl=zh-tw)會將串流資料分組為一致的時間間隔，以便使用匯總函式進行分析。

## 範例

下列 SQL 範例說明持續查詢的常見用途。

### 將資料匯出至 Pub/Sub 主題

下列範例顯示一項持續查詢，可篩選接收計程車乘車資訊串流的 BigQuery 資料表中的資料，並透過訊息屬性，將取消乘車的資料即時發布至 Pub/Sub 主題：

```
EXPORT DATA
  OPTIONS (
    format = 'CLOUD_PUBSUB',
    uri = 'https://pubsub.googleapis.com/projects/myproject/topics/taxi-real-time-rides')
AS (
  SELECT
    TO_JSON_STRING(
      STRUCT(
        ride_id,
        timestamp,
        latitude,
        longitude)) AS message,
    TO_JSON(
      STRUCT(
        CAST(passenger_comment AS STRING) AS passenger_comment))
  FROM
    CHANGES(TABLE `myproject.real_time_taxi_streaming.taxi_rides`,
      -- Configure the CHANGES TVF start_timestamp to specify when you want to
      -- start processing data using your continuous query.
      -- This example starts processing at 10 minutes before the current time.
      CURRENT_TIMESTAMP() - INTERVAL 10 MINUTE)
  WHERE _CHANGE_TYPE = 'DELETE'
);
```

### 將資料匯出至 Bigtable 資料表

下列範例顯示一項持續查詢，可篩選接收計程車行程資訊串流的 BigQuery 資料表，並將資料即時匯出至 Bigtable 資料表：

```
EXPORT DATA
  OPTIONS (
    format = 'CLOUD_BIGTABLE',
    truncate = TRUE,
    overwrite = TRUE,
    uri = 'https://bigtable.googleapis.com/projects/myproject/instances/mybigtableinstance/tables/taxi-real-time-rides')
AS (
  SELECT
    CAST(CONCAT(ride_id, timestamp, latitude, longitude) AS STRING) AS rowkey,
    STRUCT(
      timestamp,
      latitude,
      longitude,
      meter_reading,
      ride_status,
      passenger_count) AS features
  FROM
    APPENDS(TABLE `myproject.real_time_taxi_streaming.taxirides`,
      -- Configure the APPENDS TVF start_timestamp to specify when you want to
      -- start processing data using your continuous query.
      -- This example starts processing at 10 minutes before the current time.
      CURRENT_TIMESTAMP() - INTERVAL 10 MINUTE)
  WHERE ride_status = 'enroute'
);
```

### 將資料匯出至 Spanner 資料表

下列範例顯示一項持續查詢，可篩選 BigQuery 資料表中的資料 (該資料表會接收計程車搭乘資訊串流)，然後將資料即時匯出至 Spanner 資料表：

```
EXPORT DATA
 OPTIONS (
   format = 'CLOUD_SPANNER',
   uri = 'https://spanner.googleapis.com/projects/myproject/instances/myspannerinstance/databases/taxi-real-time-rides',
   spanner_options ="""{
      "table": "rides",
      -- To ensure data is written to Spanner in the correct sequence
      -- during a continuous export, use the change_timestamp_column
      -- option. This should be mapped to a timestamp column from your
      -- BigQuery data. If your source data lacks a timestamp, the
      -- _CHANGE_TIMESTAMP pseudocolumn provided by the APPENDS function
      -- will be automatically mapped to the "change_timestamp" column.
      "change_timestamp_column": "change_timestamp"
   }"""
  )
  AS (
  SELECT
    ride_id,
    latitude,
    longitude,
    meter_reading,
    ride_status,
    passenger_count,
    _CHANGE_TIMESTAMP as change_timestamp
  FROM APPENDS(
        TABLE `myproject.real_time_taxi_streaming.taxirides`,
        -- Configure the APPENDS TVF start_timestamp to specify when you want to
        -- start processing data using your continuous query.
        -- This example starts processing at 10 minutes before the current time.
        CURRENT_TIMESTAMP() - INTERVAL 10 MINUTE)
  WHERE ride_status = 'enroute'
  );
```

### 將資料寫入 BigQuery 資料表或 Apache Iceberg 代管資料表

下列範例顯示一項持續查詢，可篩選及轉換 BigQuery 資料表中的資料 (該資料表會接收串流計程車搭乘資訊)，然後即時將資料寫入另一個 BigQuery 資料表或 Iceberg 代管資料表。這樣一來，您就能在 BigQuery 或開放格式湖倉中，進一步分析下游資料。

```
INSERT INTO `myproject.real_time_taxi_streaming.transformed_taxirides`
SELECT
  timestamp,
  meter_reading,
  ride_status,
  passenger_count,
  ST_Distance(
    ST_GeogPoint(pickup_longitude, pickup_latitude),
    ST_GeogPoint(dropoff_longitude, dropoff_latitude)) AS euclidean_trip_distance,
    SAFE_DIVIDE(meter_reading, passenger_count) AS cost_per_passenger
FROM
  APPENDS(TABLE `myproject.real_time_taxi_streaming.taxirides`,
    -- Configure the APPENDS TVF start_timestamp to specify when you want to
    -- start processing data using your continuous query.
    -- This example starts processing at 10 minutes before the current time.
    CURRENT_TIMESTAMP() - INTERVAL 10 MINUTE)
WHERE
  ride_status = 'dropoff';
```

如要將持續查詢輸出內容寫入 Iceberg 代管資料表，請將 `myproject.real_time_taxi_streaming.transformed_taxirides` 替換為目標 Iceberg 代管資料表的名稱。語法相同，因為連線詳細資料和湖倉儲存庫設定是在目的地資料表本身定義。

### 使用 Gemini Enterprise Agent Platform 模型處理資料

下列範例顯示持續查詢，使用 Agent Platform 模型，根據計程車乘客目前的經緯度生成廣告，然後將結果即時匯出至 Pub/Sub 主題：

```
EXPORT DATA
  OPTIONS (
    format = 'CLOUD_PUBSUB',
    uri = 'https://pubsub.googleapis.com/projects/myproject/topics/taxi-real-time-rides')
AS (
  SELECT
    TO_JSON_STRING(
      STRUCT(
        ride_id,
        timestamp,
        latitude,
        longitude,
        prompt,
        result)) AS message
  FROM
    AI.GENERATE_TEXT(
      MODEL `myproject.real_time_taxi_streaming.taxi_ml_generate_model`,
      (
        SELECT
          timestamp,
          ride_id,
          latitude,
          longitude,
          CONCAT(
            'Generate an ad based on the current latitude of ',
            latitude,
            ' and longitude of ',
            longitude) AS prompt
        FROM
          APPENDS(TABLE `myproject.real_time_taxi_streaming.taxirides`,
            -- Configure the APPENDS TVF start_timestamp to specify when you
            -- want to start processing data using your continuous query.
            -- This example starts processing at 10 minutes before the current time.
            CURRENT_TIMESTAMP() - INTERVAL 10 MINUTE)
        WHERE ride_status = 'enroute'
      ),
      STRUCT(
        50 AS max_output_tokens,
        1.0 AS temperature,
        40 AS top_k,
        1.0 AS top_p))
      AS ml_output
);
```

### 執行 `JOIN` 和視窗匯總

以下範例顯示執行 `JOIN` 和視窗化匯總的持續查詢。

假設您想彙整計程車乘車資料表和計程車要求資料表，瞭解各鄰近地區每五分鐘的計程車健康狀態。使用匯總函式，您可以擷取每個鄰近地區的計程車需求量，以及乘客叫車時與計程車的最小、最大、平均和標準差距離。

```
INSERT INTO
 `real_time_taxi_streaming.neighborhood_taxi_health`
WITH potential_matches AS (
 SELECT
   requests._CHANGE_TIMESTAMP AS bq_changed_ts,
   requests.geohash,
   requests.latitude,
   requests.longitude,
   ST_DISTANCE(
     ST_GEOGPOINT(requests.longitude, requests.latitude),
     ST_GEOGPOINT(taxis.longitude, taxis.latitude)
   ) AS distance_in_meters
 FROM
   APPENDS(TABLE `real_time_taxi_streaming.ride_requests`,
     CURRENT_TIMESTAMP() - INTERVAL 10 MINUTE) AS requests
 INNER JOIN
   APPENDS(TABLE `real_time_taxi_streaming.taxirides`,
     CURRENT_TIMESTAMP() - INTERVAL 10 MINUTE) AS taxis
 ON requests.geohash = taxis.geohash
 WHERE
   taxis.ride_status = 'available'
   AND taxis._CHANGE_TIMESTAMP BETWEEN (requests._CHANGE_TIMESTAMP - INTERVAL 5 MINUTE) AND requests._CHANGE_TIMESTAMP
   AND ST_Dwithin(
     ST_GEOGPOINT(requests.longitude, requests.latitude),
     ST_GEOGPOINT(taxis.longitude, taxis.latitude),
     2000 -- Distance in meters
   )
)
SELECT
 window_end,
 geohash,
 ROUND(AVG(latitude), 6) AS avg_latitude,
 ROUND(AVG(longitude), 6) AS avg_longitude,
 COUNT(*) AS taxi_demand_volume,
 ROUND(AVG(distance_in_meters), 2) AS avg_proximity_meters,
 ROUND(MIN(distance_in_meters), 2) AS min_proximity_meters,
 ROUND(MAX(distance_in_meters), 2) AS max_proximity_meters,
 ROUND(STDDEV(distance_in_meters), 2) AS proximity_stddev
FROM
 TUMBLE(TABLE potential_matches, "bq_changed_ts", INTERVAL 5 MINUTE)
GROUP BY
 window_end,
 geohash;
```

## 修改持續查詢的 SQL

持續查詢工作執行期間，您無法更新持續查詢使用的 SQL。您必須取消持續查詢工作、修改 SQL，然後從停止原始持續查詢工作的位置，啟動新的持續查詢工作。

如要修改持續查詢使用的 SQL，請按照下列步驟操作：

1. [查看要更新的持續查詢工作詳細資料](https://docs.cloud.google.com/bigquery/docs/managing-jobs?hl=zh-tw#view-job)，並記下工作 ID。
2. 如果可以，請暫停收集上游資料。如果無法這麼做，重新啟動持續查詢時，可能會出現重複資料。
3. [取消要修改的持續查詢](https://docs.cloud.google.com/bigquery/docs/continuous-queries?hl=zh-tw#cancel_a_continuous_query)。
4. 使用 `INFORMATION_SCHEMA` [`JOBS` 檢視表](https://docs.cloud.google.com/bigquery/docs/information-schema-jobs?hl=zh-tw)，取得原始持續查詢工作的 `end_time` 值：

   ```
   SELECT end_time
   FROM `PROJECT_ID.region-REGION`.INFORMATION_SCHEMA.JOBS_BY_PROJECT
   WHERE
     EXTRACT(DATE FROM creation_time) = current_date()
   AND error_result.reason = 'stopped'
   AND job_id = 'JOB_ID';
   ```

   更改下列內容：

   * `PROJECT_ID`：您的專案 ID。
   * `REGION`：專案使用的區域。
   * `JOB_ID`：您在步驟 1 找到的持續查詢工作 ID。
5. 修改持續查詢 SQL 陳述式，[從特定時間點開始持續查詢](https://docs.cloud.google.com/bigquery/docs/continuous-queries?hl=zh-tw#start_a_continuous_query_from_a_particular_point_in_time)，並使用在步驟 5 擷取的 `end_time` 值做為起點。
6. 修改持續查詢 SQL 陳述式，反映所需變更。
7. 執行修改後的持續查詢。

## 取消持續查詢

您可以像取消其他工作一樣[取消](https://docs.cloud.google.com/bigquery/docs/managing-jobs?hl=zh-tw#cancel_jobs)持續查詢工作。工作取消後，查詢可能需要一分鐘才會停止執行。

如果取消後重新啟動查詢，重新啟動的查詢會視為新的獨立查詢。重新啟動的查詢不會從先前工作停止的位置開始處理資料，也無法參照先前查詢的結果。請參閱「[從特定時間點開始持續查詢](#start_a_continuous_query_from_a_particular_point_in_time)」。

## 監控查詢及處理錯誤

持續查詢可能會因資料不一致、結構定義變更、暫時性服務中斷或維護等因素而中斷。雖然 BigQuery 會處理部分暫時性錯誤，但如要提高工作彈性，最佳做法包括：

* [監控持續查詢](https://docs.cloud.google.com/bigquery/docs/continuous-queries-monitor?hl=zh-tw)。
* [查詢失敗時發出警告](https://docs.cloud.google.com/bigquery/docs/continuous-queries-monitor?hl=zh-tw#alert)。
* [重試失敗的查詢](https://docs.cloud.google.com/bigquery/docs/continuous-queries-monitor?hl=zh-tw#retry)。

## 後續步驟

* [監控持續查詢](https://docs.cloud.google.com/bigquery/docs/continuous-queries-monitor?hl=zh-tw)




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-10-24 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-10-24 (世界標準時間)。"],[],[]]