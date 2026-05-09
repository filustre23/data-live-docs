Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 管理設定

BigQuery 管理員和專案擁有者可以在機構和專案層級管理設定。您可以設定配置，在整個資料基礎架構中強制執行安全性、控管成本，以及提升查詢效能。設定預設值可確保法規遵循和作業效率一致，方便您管理 BigQuery 環境。

下列各節說明如何指定預設設定。預設設定是在機構或專案層級設定，但可以在工作階段或工作層級覆寫。

## 必要的角色

如要取得指定設定所需的權限，請要求管理員授予您「[BigQuery 管理員](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.admin) 」(`roles/bigquery.admin`) IAM 角色。如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

這個預先定義的角色具備 `bigquery.config.update` 權限，可指定設定。

您或許還可透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)取得這項權限。

如要進一步瞭解 BigQuery 中的 IAM 角色和權限，請參閱[預先定義的角色與權限](https://docs.cloud.google.com/bigquery/access-control?hl=zh-tw)一文。

## 指定全域設定

您可以在組織或專案層級指定全域設定。

### 限制

全域設定有下列限制：

* BigQuery [Omni 地區](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw#omni-loc)不支援全域機構和專案設定。
* 修改`default_location`全域設定後，最多可能需要 10 分鐘才會生效。在設定傳播完成前，符合資格的查詢可能會轉送至先前的預設位置。

### 設定全域機構設定

如果沒有[明確指定位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw#specify_locations)，系統會透過下列其中一種方式判斷位置：

* 要求中參照的資料集位置。舉例來說，如果查詢參考了儲存在 `asia-northeast1` 區域資料集內的資料表或檢視區塊，查詢工作就會在 `asia-northeast1` 執行。
* 要求中參照的連線指定區域。
* 目的地資料表的位置。

如果未明確指定位置，且系統無法從要求中的資源判斷位置，就會使用預設位置。如果未設定預設位置，工作會在 `US` 多區域執行。

您可以使用 [`ALTER ORGANIZATION SET OPTIONS` DDL 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#alter_organization_set_options_statement)，在機構層級設定全域設定。預設位置是唯一的全域機構設定。如果無法從要求推斷位置，系統會使用預設位置執行工作。

設定預設位置時，您不需要指定設定適用的區域。您無法在同一 DDL 陳述式中混用全域和區域設定。

**注意：** 修改`default_location`全域設定後，最多可能需要 10 分鐘才會生效。在設定傳播完成前，符合資格的查詢可能會轉送至先前的預設位置。

如要在機構層級設定 `default_location`，請按照下列步驟操作：

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery」**BigQuery**頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 按一下查詢編輯器。這個分頁標籤標示為「search\_insights」search\_insights「未命名的查詢」。
3. 如要設定 `default_location`，請在「查詢編輯器」中輸入下列 DDL 陳述式：

   ```
     ALTER ORGANIZATION
     SET OPTIONS (
     `default_location` = 'LOCATION'
     );
   ```

   將 `LOCATION` 替換為區域或多區域[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)。如果無法從要求推斷位置，系統就會使用這個值來執行工作。舉例來說，如果無法判斷查詢中資料集的位置，系統就會使用預設位置。
4. 或者，如要清除`default_location`機構層級的全域設定，請在「查詢編輯器」中輸入下列 DDL 陳述式：

   ```
     ALTER ORGANIZATION
     SET OPTIONS (
     `default_location` = NULL
     );
   ```
5. 按一下「執行」。

### bq

1. 如要在機構層級設定 `default_location`，請輸入 [`bq query`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_query) 指令，並提供下列 DDL 陳述式做為查詢參數。將 `use_legacy_sql` 旗標設為 `false`。

   ```
   ALTER ORGANIZATION
   SET OPTIONS (
   `default_location` = 'LOCATION'
   );
   ```

   將 `LOCATION` 替換為區域或多區域[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)。如果無法從要求推斷位置，系統就會使用這個值來執行工作。舉例來說，如果無法判斷查詢中資料集的位置，系統就會使用預設位置。
2. 如要在機構層級清除 `default_location`，請輸入 [`bq query`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_query) 指令，並提供下列 DDL 陳述式做為查詢參數。將 `use_legacy_sql` 旗標設為 `false`。

   ```
   ALTER ORGANIZATION
   SET OPTIONS (
   `default_location` = NULL
   );
   ```

### API

呼叫 [`jobs.query`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs/query?hl=zh-tw) 方法，並在要求主體的 `query` 屬性中提供 DDL 陳述式。

### 設定全域專案設定

如果沒有[明確指定位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw#specify_locations)，系統會透過下列其中一種方式判斷位置：

* 要求中參照的資料集位置。舉例來說，如果查詢參考了儲存在 `asia-northeast1` 區域資料集內的資料表或檢視區塊，查詢工作就會在 `asia-northeast1` 執行。
* 要求中參照的連線指定區域。
* 目的地資料表的位置。

如果未明確指定位置，且系統無法從要求中的資源判斷位置，就會使用預設位置。如果未設定預設位置，工作會在 `US` 多區域執行。

您可以使用 [`ALTER PROJECT SET OPTIONS` DDL 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#alter_project_set_options_statement)，在專案層級設定全域設定。`ALTER PROJECT SET OPTIONS` DDL 陳述式會視需要接受 `PROJECT_ID` 變數。如未指定 `PROJECT_ID`，系統會預設為您執行 `ALTER PROJECT` DDL 陳述式的目前專案。

預設位置是唯一的全域專案設定。設定預設位置時，您不需要指定設定適用的區域。您無法在同一個 DDL 陳述式中混用全域和區域設定。

專案層級設定會覆寫組織層級設定。
專案層級設定可由[工作階段層級設定](https://docs.cloud.google.com/bigquery/docs/sessions-write-queries?hl=zh-tw)覆寫，而工作階段層級設定則可由[作業層級設定](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw)覆寫。

如要在專案層級設定 `default_location`，請按照下列步驟操作：

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 按一下查詢編輯器。這個分頁標籤標示為「search\_insights」search\_insights「未命名的查詢」。
3. 如要設定 `default_location`，請在「查詢編輯器」中輸入下列 DDL 陳述式：

   ```
     ALTER PROJECT PROJECT_ID
     SET OPTIONS (
     `default_location` = 'LOCATION'
     );
   ```

   更改下列內容：

   * `PROJECT_ID`：專案 ID。
   * `LOCATION`：區域或多區域[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)。如果無法從要求推斷位置，系統就會使用這個值來執行工作。舉例來說，如果系統無法判斷查詢中資料集的位置，就會使用預設位置。
4. 或者，如要清除 `default_location` 設定，請在「Query editor」(查詢編輯器) 中輸入下列 DDL 陳述式。如果清除專案層級的 `default_location`，系統會使用機構層級的預設設定 (如有)。否則系統會使用預設設定。

   ```
     ALTER PROJECT PROJECT_ID
     SET OPTIONS (
     `default_location` = NULL
     );
   ```
5. 按一下「執行」。

### bq

1. 如要在專案層級設定 `default_location`，請輸入 [`bq query`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_query) 指令，並提供下列 DDL 陳述式做為查詢參數。將 `use_legacy_sql` 旗標設為 `false`。

   ```
   ALTER PROJECT PROJECT_ID
   SET OPTIONS (
   `default_location` = 'LOCATION'
   );
   ```

   更改下列內容：

   * `PROJECT_ID`：專案 ID。
   * `LOCATION`：區域或多區域[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)。如果無法從要求推斷位置，系統就會使用這個值來執行工作。舉例來說，如果無法判斷查詢中資料集的位置，系統就會使用預設位置。
2. 或者，如要在專案層級清除 `default_location`，請輸入 [`bq query`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_query) 指令，並提供下列 DDL 陳述式做為查詢參數。將 `use_legacy_sql` 旗標設為 `false`。如果清除專案層級的 `default_location`，系統會使用機構層級的預設設定 (如有)。否則系統會使用預設設定。

   ```
   ALTER PROJECT PROJECT_ID
   SET OPTIONS (
   `default_location` = NULL
   );
   ```

### API

呼叫 [`jobs.query`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs/query?hl=zh-tw) 方法，並在要求主體的 `query` 屬性中提供 DDL 陳述式。

## 指定區域設定

您可以在機構組織或專案層級設定區域設定。

### 管理預訂和帳單控制項

您可以控管查詢如何使用預留項目或隨選計費。這些設定可允許彈性使用預留資源，或要求查詢使用預留資源配額，確保費用可預測。

常見的預訂和帳單控制項包括 `reservation_override_mode` ([預覽](https://docs.cloud.google.com/products?hl=zh-tw#product-launch-stages)) 和 `disable_on_demand_billing` ([預覽](https://docs.cloud.google.com/products?hl=zh-tw#product-launch-stages)) 等設定。如需完整的設定和選項清單，請參閱[`ALTER PROJECT SET OPTIONS` 選項清單](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#project_set_options_list)。

### 設定區域機構設定

您可以使用 [`ALTER ORGANIZATION SET OPTIONS` DDL 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#alter_organization_set_options_statement)，在機構組織層級設定區域設定。您必須指定各項機構設定的適用區域。陳述式中只能使用一個區域。

如要設定區域機構設定，請按照下列步驟操作。以下範例指定了多項預設區域設定，包括：

* 時區：`America/Chicago`
* Cloud KMS 金鑰：使用者定義的金鑰
* 查詢逾時時間：30 分鐘 (1,800,000 毫秒)
* 互動式查詢佇列逾時時間：10 分鐘 (600,000 毫秒)
* 批次查詢佇列逾時時間：20 分鐘 (1,200,000 毫秒)
* `INFORMATION_SCHEMA`：已啟用

如要查看所有區域機構設定，請前往
[`organization_set_options_list`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#organization_set_options_list)。

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 按一下查詢編輯器。這個分頁標籤標示為「search\_insights」search\_insights「未命名的查詢」。
3. 如要設定區域機構設定，請在**查詢編輯器**中輸入下列 DDL 陳述式：

   ```
     ALTER ORGANIZATION
     SET OPTIONS (
     `region-REGION.default_time_zone`= 'America/Chicago',
     -- Ensure all service accounts under the organization have permission to KMS_KEY
     `region-REGION.default_kms_key_name` = KMS_KEY,
     `region-REGION.default_query_job_timeout_ms` = 1800000,
     `region-REGION.default_interactive_query_queue_timeout_ms` = 600000,
     `region-REGION.default_batch_query_queue_timeout_ms` = 1200000,
     `region-REGION.enable_info_schema_storage` = true);
   ```

   更改下列內容：

   * `REGION`：與專案或機構相關聯的[區域](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw#regions)，例如 `us` 或 `europe-west6`。指令中每個選項的 `REGION` 值必須相同。
   * `KMS_KEY`：使用者定義的 Cloud KMS 金鑰。詳情請參閱「[客戶管理的 Cloud KMS 金鑰](https://docs.cloud.google.com/bigquery/docs/customer-managed-encryption?hl=zh-tw)」。
4. 或者，如要清除區域機構設定，請在「Query editor」(查詢編輯器) 中輸入下列 DDL 陳述式：

   ```
     ALTER ORGANIZATION
     SET OPTIONS (
     `region-REGION.default_time_zone` = NULL,
     `region-REGION.default_kms_key_name` = NULL,
     `region-REGION.default_query_job_timeout_ms` = NULL,
     `region-REGION.default_interactive_query_queue_timeout_ms` = NULL,
     `region-REGION.default_batch_query_queue_timeout_ms` = NULL,
     `region-REGION.enable_info_schema_storage` = NULL);
   ```
5. 按一下「執行」。

### bq

如要設定區域機構設定，請輸入 [`bq query`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_query) 指令，並提供下列 DDL 陳述式做為查詢參數。將 `use_legacy_sql` 旗標設為 `false`。

```
  ALTER ORGANIZATION
  SET OPTIONS (
  `region-REGION.default_time_zone`= 'America/Chicago',
  -- Ensure all service accounts under the organization have permission to KMS_KEY
  `region-REGION.default_kms_key_name` = KMS_KEY,
  `region-REGION.default_query_job_timeout_ms` = 1800000,
  `region-REGION.default_interactive_query_queue_timeout_ms` = 600000,
  `region-REGION.default_batch_query_queue_timeout_ms` = 1200000);
```

更改下列內容：

* `REGION`：與專案或機構相關聯的[區域](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw#regions)，例如 `us` 或 `europe-west6`。指令中每個選項的 `REGION` 值必須相同。
* `KMS_KEY`：使用者定義的 Cloud KMS 金鑰。詳情請參閱「[客戶管理的 Cloud KMS 金鑰](https://docs.cloud.google.com/bigquery/docs/customer-managed-encryption?hl=zh-tw)」。

或者，如要清除區域機構設定，請輸入 [`bq query`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_query) 指令，並提供下列 DDL 陳述式做為查詢參數。將 `use_legacy_sql` 旗標設為 `false`：

```
ALTER ORGANIZATION
SET OPTIONS (
  `region-REGION.default_time_zone` = NULL,
  `region-REGION.default_kms_key_name` = NULL,
  `region-REGION.default_query_job_timeout_ms` = NULL,
  `region-REGION.default_interactive_query_queue_timeout_ms` = NULL,
  `region-REGION.default_batch_query_queue_timeout_ms` = NULL,
  `region-REGION.default_storage_billing_model`= NULL,
  `region-REGION.default_max_time_travel_hours` = NULL,
  `region-REGION.default_cloud_resource_connection_id` = NULL,
  `region-REGION.default_sql_dialect_option` = NULL,
  `region-REGION.enable_reservation_based_fairness` = NULL,
  `region-REGION.enable_global_queries_execution` = NULL,
  `region-REGION.enable_global_queries_data_access` = NULL);
```

### API

呼叫 [`jobs.query`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs/query?hl=zh-tw) 方法，並在要求主體的 `query` 屬性中提供 DDL 陳述式。

### 設定區域專案設定

您可以使用 [`ALTER PROJECT SET OPTIONS` DDL 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#alter_project_set_options_statement)，在專案層級設定區域設定。指定設定時，您必須指定套用設定的區域。每份報表只能使用一個區域。

專案層級設定會覆寫組織層級設定。
專案層級設定可由[工作階段層級設定](https://docs.cloud.google.com/bigquery/docs/sessions-write-queries?hl=zh-tw)覆寫，而工作階段層級設定則可由[作業層級設定](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw)覆寫。

`ALTER PROJECT SET OPTIONS` DDL 陳述式會視需要接受 `PROJECT_ID` 變數。如未指定 `PROJECT_ID` 變數，系統會預設為您執行 `ALTER PROJECT` DDL 陳述式的目前專案。

以下範例指定多項區域和專案層級設定，包括：

* 時區：`America/Los_Angeles`
* Cloud KMS 金鑰：範例金鑰
* 查詢逾時時間：1 小時 (1,800,000 毫秒)
* 互動式查詢佇列逾時時間：10 分鐘 (600,000 毫秒)
* 批次查詢佇列逾時時間：20 分鐘 (1,200,000 毫秒)
* 以預留項目為基礎的公平性機制：已啟用
* 全域查詢：已啟用，可執行查詢及存取資料
* `INFORMATION_SCHEMA`：已啟用

如要查看所有區域專案設定，請前往 [`project_set_options_list`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#project_set_options_list)。

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 按一下查詢編輯器。這個分頁標籤標示為「search\_insights」search\_insights「未命名的查詢」。
3. 如要設定區域專案設定，請在**查詢編輯器**中輸入下列 DDL 陳述式：

   ```
    ALTER PROJECT PROJECT_ID
    SET OPTIONS (
    `region-REGION.default_time_zone` = 'America/Los_Angeles',
    -- Ensure all service accounts under the project have permission to KMS_KEY
    `region-REGION.default_kms_key_name` = KMS_KEY,
    `region-REGION.default_query_job_timeout_ms` = 3600000,
    `region-REGION.default_interactive_query_queue_timeout_ms` = 600000,
    `region-REGION.default_batch_query_queue_timeout_ms` = 1200000,
    `region-REGION.enable_reservation_based_fairness` = true,
    `region-REGION.enable_global_queries_execution` = true,
    `region-REGION.enable_global_queries_data_access` = true,
    `region-REGION.enable_info_schema_storage` = true);
   ```

   更改下列內容：

   * `PROJECT_ID`：專案 ID。
   * `REGION`：與專案或機構相關聯的[區域](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw#regions)，例如 `us` 或 `europe-west6`。指令中每個選項的 `REGION` 值必須相同。
   * `KMS_KEY`：使用者定義的 Cloud KMS 金鑰。詳情請參閱「[客戶管理的 Cloud KMS 金鑰](https://docs.cloud.google.com/bigquery/docs/customer-managed-encryption?hl=zh-tw)」。
4. 或者，如要清除區域專案設定，請在「Query editor」(查詢編輯器) 中輸入下列 DDL 陳述式：

   ```
     ALTER PROJECT PROJECT_ID
     SET OPTIONS (
     `region-REGION.default_time_zone` = NULL,
     `region-REGION.default_kms_key_name` = NULL,
     `region-REGION.default_query_job_timeout_ms` = NULL,
     `region-REGION.default_interactive_query_queue_timeout_ms` = NULL,
     `region-REGION.default_batch_query_queue_timeout_ms` = NULL,
     `region-REGION.enable_reservation_based_fairness` = false,
     `region-REGION.enable_info_schema_storage` = NULL);
   ```
5. 按一下「執行」。

### bq

1. 如要設定區域專案設定，請輸入 [`bq query`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_query) 指令，並提供下列 DDL 陳述式做為查詢參數。將 `use_legacy_sql` 旗標設為 `false`。

   ```
   ALTER PROJECT PROJECT_ID
   SET OPTIONS (
   `region-REGION.default_time_zone`= 'America/Chicago',
   -- Ensure all service accounts under the organization have permission to KMS_KEY
   `region-REGION.default_kms_key_name` = KMS_KEY,
   `region-REGION.default_query_job_timeout_ms` = 1800000,
   `region-REGION.default_interactive_query_queue_timeout_ms` = 600000,
   `region-REGION.default_batch_query_queue_timeout_ms` = 1200000,
   `region-REGION.enable_reservation_based_fairness` = true);
   ```

   更改下列內容：

   * `PROJECT_ID`：專案 ID。
   * `REGION`：與專案或機構相關聯的[區域](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw#regions)，例如 `us` 或 `europe-west6`。指令中每個選項的 `REGION` 值必須相同。
   * `KMS_KEY`：使用者定義的 Cloud KMS 金鑰。詳情請參閱「[客戶管理的 Cloud KMS 金鑰](https://docs.cloud.google.com/bigquery/docs/customer-managed-encryption?hl=zh-tw)」。
2. 或者，如要清除區域專案設定，請輸入 [`bq query`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_query) 指令，並提供下列 DDL 陳述式做為查詢參數。將 `use_legacy_sql` 旗標設為 `false`：

   ```
   ALTER ORGANIZATION
   SET OPTIONS (
   `region-REGION.default_time_zone` = NULL,
   `region-REGION.default_kms_key_name` = NULL,
   `region-REGION.default_query_job_timeout_ms` = NULL,
   `region-REGION.default_interactive_query_queue_timeout_ms` = NULL,
   `region-REGION.default_batch_query_queue_timeout_ms` = NULL,
   `region-REGION.enable_reservation_based_fairness` = false,
   `region-REGION.enable_global_queries_execution` = NULL,
   `region-REGION.enable_global_queries_data_access` = NULL);
   ```

### API

呼叫 [`jobs.query`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs/query?hl=zh-tw) 方法，並在要求主體的 `query` 屬性中提供 DDL 陳述式。

## 擷取設定

您可以使用下列 [`INFORMATION_SCHEMA`](https://docs.cloud.google.com/bigquery/docs/information-schema-intro?hl=zh-tw) 檢視畫面，查看機構或專案的設定：

* [`INFORMATION_SCHEMA.PROJECT_OPTIONS`](https://docs.cloud.google.com/bigquery/docs/information-schema-project-options?hl=zh-tw)：套用至專案的設定。
* [`INFORMATION_SCHEMA.EFFECTIVE_PROJECT_OPTIONS`](https://docs.cloud.google.com/bigquery/docs/information-schema-effective-project-options?hl=zh-tw)：套用至專案的有效設定。有效設定包括專案層級的所有設定，以及專案從機構繼承的所有設定。
* [`INFORMATION_SCHEMA.ORGANIZATION_OPTIONS`](https://docs.cloud.google.com/bigquery/docs/information-schema-organization-options?hl=zh-tw)：
  套用至機構的設定。

新設定可能需要幾分鐘才會生效，並反映在 `INFORMATION_SCHEMA` 檢視畫面中。

### 必要的角色

如要取得擷取設定所需的權限，請要求系統管理員授予您指定專案的 [BigQuery 工作使用者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.jobUser)  (`roles/bigquery.jobUser`) IAM 角色。如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

這個預先定義的角色具備 `bigquery.config.get` 權限，可擷取設定。

您或許還可透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)取得這項權限。

如要進一步瞭解 BigQuery 中的 IAM 角色和權限，請參閱[預先定義的角色與權限](https://docs.cloud.google.com/bigquery/access-control?hl=zh-tw)一文。

### 範例

使用下列查詢範例，從 `INFORMATION_SCHEMA` 檢視畫面擷取專案和機構設定。

#### 查看全域設定

如要查看所有全域機構設定，請執行下列查詢：

```
SELECT * FROM INFORMATION_SCHEMA.ORGANIZATION_OPTIONS;
```

如要只查看預設位置的機構設定，請執行下列查詢：

```
SELECT
    option_value
FROM INFORMATION_SCHEMA.ORGANIZATION_OPTIONS
WHERE option_name = 'default_location'
```

如要查看預設專案的所有有效全域設定，請執行下列查詢：

```
SELECT * FROM INFORMATION_SCHEMA.EFFECTIVE_PROJECT_OPTIONS;
```

如要只查看預設專案的預設位置有效全域設定，請執行下列查詢：

```
SELECT
    option_value
FROM INFORMATION_SCHEMA.EFFECTIVE_PROJECT_OPTIONS
WHERE option_name = 'default_location'
```

如要查看預設專案的所有全域設定，請執行下列查詢：

```
SELECT * FROM INFORMATION_SCHEMA.PROJECT_OPTIONS;
```

如要只查看預設專案的預設位置設定，請執行下列查詢：

```
SELECT
    option_value
FROM INFORMATION_SCHEMA.PROJECT_OPTIONS
WHERE option_name = 'default_location'
```

#### 查看區域設定

如要查看 `us` 區域中機構下的設定，請執行下列查詢：

```
SELECT * FROM region-us.INFORMATION_SCHEMA.ORGANIZATION_OPTIONS;
```

如要查看 `us` 區域中預設專案的有效設定，請執行下列查詢：

```
SELECT * FROM region-us.INFORMATION_SCHEMA.EFFECTIVE_PROJECT_OPTIONS;
```

如要查看 `us` 區域中預設專案的設定，請執行下列查詢：

```
SELECT * FROM region-us.INFORMATION_SCHEMA.PROJECT_OPTIONS;
```

## 配置設定

下列各節說明可指定的設定。

### 查詢和工作執行設定

您可以使用下列設定，控管查詢的執行、計時和排隊方式。

* `default_batch_query_queue_timeout_ms`：批次查詢[排入佇列](https://docs.cloud.google.com/bigquery/docs/query-queues?hl=zh-tw)的預設時間長度，以毫秒為單位。如未設定，預設值為 24 小時。最短 1 毫秒，最長 48 小時。如要停用批次查詢佇列功能，請將值設為 `-1`。
* `default_interactive_query_queue_timeout_ms`：互動式查詢[排入佇列](https://docs.cloud.google.com/bigquery/docs/query-queues?hl=zh-tw)的預設時間長度，以毫秒為單位。如未設定，預設值為 6 小時。最短 1 毫秒，最長 48 小時。如要停用互動式查詢佇列功能，請將值設為 `-1`。
* `default_query_job_timeout_ms`：查詢工作逾時的預設時間，包括工作排入佇列的時間和執行時間。逾時時間必須介於 5 分鐘至 48 小時之間。這項逾時時間僅適用於個別查詢作業和指令碼的子項作業。如要為指令碼工作設定逾時時間，請使用 [jobs.insert](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs/insert?hl=zh-tw) API 方法並設定 `jobTimeoutMs` 欄位。

  **注意：** `default_query_job_timeout_ms` 設定也適用於[持續查詢](https://docs.cloud.google.com/bigquery/docs/continuous-queries-introduction?hl=zh-tw)作業。如要為個別持續查詢覆寫這項專案層級設定，請為相關持續查詢指派[工作逾時](https://docs.cloud.google.com/bigquery/docs/continuous-queries?hl=zh-tw#run_a_continuous_query_by_using_a_service_account)。持續查詢仍會遵守[最長執行時間](https://docs.cloud.google.com/bigquery/docs/continuous-queries-introduction?hl=zh-tw#authorization)。
* `default_location`：[`default_location` 設定](#global-settings)用於在[未設定或無法判斷位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw#specify_locations)時執行工作。
  如果未設定 `default_location`，工作會在 `US` 多區域執行。
* `enable_reservation_based_fairness`：決定如何共用閒置時段的選項。預設值為 false，表示閒置運算單元會平均分配給所有查詢專案。啟用後，系統會先在所有預留項目之間平均分配閒置運算單元，然後再分配給預留項目中的專案。詳情請參閱[以預留項目為基礎的公平性機制](https://docs.cloud.google.com/bigquery/docs/slots?hl=zh-tw#fairness)。這項功能僅支援專案層級。您無法在機構或工作層級指定這項設定。
* `default_time_zone`：受時區影響的 GoogleSQL 函式中，如未指定時區做為引數，就會使用這個預設時區。這項設定不會套用至[時間單位資料欄分區資料表](https://docs.cloud.google.com/bigquery/docs/partitioned-tables?hl=zh-tw#date_timestamp_partitioned_tables) (以世界標準時間做為時區)、[Storage 移轉服務排定移轉作業](https://docs.cloud.google.com/storage-transfer/docs/schedule-transfer-jobs?hl=zh-tw)，或是[使用 bq 指令列工具載入資料](https://docs.cloud.google.com/bigquery/docs/bq-command-line-tool?hl=zh-tw#loading_data)的情況。詳情請參閱「[時區](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#time_zones)」。

  **注意：** 如要設定預設時區，請確保使用 `DATETIME` 常值的現有查詢不受影響。包括含有明確 `DATETIME` 關鍵字的查詢、隱含轉換的字串常值 (做為 `DATETIME_DIFF('2022-10-01', ...)` 等時間函式的參數傳遞)、`PARSE_DATETIME()` 函式等。因此，建議只在新專案中設定 `default_time_zone` 參數。
* `default_query_optimizer_options`：根據記錄進行查詢最佳化。這個選項可以是下列其中一個值：

  + `'adaptive=on'`：根據記錄最佳化查詢。
  + `'adaptive=off'`：不使用以記錄為準的查詢最佳化。
  + `NULL` (預設)：使用預設的查詢最佳化設定 (根據記錄)，這等同於 `'adaptive=on'`。
* `default_sql_dialect_option`：使用 bq 指令列工具或 BigQuery API 執行查詢作業時，預設的 SQL 查詢方言。變更這項設定不會影響控制台中的預設方言。這個選項可以是下列其中之一：

  + `'default_legacy_sql'` (預設)：如果未在工作層級指定查詢方言，則使用舊版 SQL。
  + `'default_google_sql'`：如果未在工作層級指定查詢方言，請使用 GoogleSQL。
  + `'only_google_sql'`：如果未在工作層級指定查詢方言，請使用 GoogleSQL。拒絕查詢方言設為舊版 SQL 的工作。
  + `NULL`：使用預設查詢方言設定，相當於 `'default_legacy_sql'`。
* `enable_global_queries_execution`：這個選項會決定是否可執行[全域查詢](https://docs.cloud.google.com/bigquery/docs/global-queries?hl=zh-tw)。預設值為 `FALSE`，表示未啟用全域查詢。
* `enable_global_queries_data_access`：這個選項會決定[全域查詢](https://docs.cloud.google.com/bigquery/docs/global-queries?hl=zh-tw)是否可以存取儲存在該區域的資料。預設值為 `FALSE`，表示全域查詢無法從這個區域複製資料，無論查詢在哪個專案中執行都一樣。

### 資料管理設定

使用下列設定定義資料建立、安全性及生命週期的規則。

* `default_column_name_character_map`：資料欄名稱字元的預設範圍和處理方式。如未設定，載入工作的資料欄名稱含有不支援的字元時就會失敗，並出現錯誤訊息。某些較舊的資料表可能已設為替換資料欄名稱中不支援的字元。詳情請參閱 [`load_option_list`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/load-statements?hl=zh-tw#load_option_list) 的說明。
* `default_kms_key_name`：用於加密資料表資料的預設 Cloud Key Management Service 金鑰，包括臨時或匿名資料表。詳情請參閱「[客戶管理的 Cloud KMS 金鑰](https://docs.cloud.google.com/bigquery/docs/customer-managed-encryption?hl=zh-tw)」。

   **注意：**如要設定預設 Cloud KMS 金鑰，您必須將加密者/解密者角色授予專案或機構中使用的所有 BigQuery 服務帳戶。如果專案或機構組織中的服務帳戶沒有適當權限，服務帳戶執行的所有查詢都會失敗。如要瞭解如何指派加密者/解密者角色，請參閱「[指派加密者/解密者角色](https://docs.cloud.google.com/bigquery/docs/customer-managed-encryption?hl=zh-tw#assign_role)」。如果未先指派適當的角色就設定預設 Cloud KMS 金鑰，可以將值設為 `NULL`，清除預設金鑰。如需範例，請參閱「[設定機構設定](#configure-organization-settings)」和「[設定專案設定](#configure-project-settings)」。
* `default_max_time_travel_hours`：新資料集的預設時間回溯期 (以小時為單位)。這個時間長度必須介於 48 到 168 之間 (含首尾)，且必須可被 24 整除。變更預設最長旅行時間 (小時) 不會影響現有資料集。詳情請參閱「[Time Travel 和資料保留](https://docs.cloud.google.com/bigquery/docs/time-travel?hl=zh-tw#time_travel)」。
* `enable_info_schema_storage`：這個選項可存取 [`INFORMATION_SCHEMA.TABLE_STORAGE`](https://docs.cloud.google.com/bigquery/docs/information-schema-table-storage?hl=zh-tw) 和 [`SEARCH_INDEXES`](https://docs.cloud.google.com/bigquery/docs/information-schema-indexes?hl=zh-tw) 檢視畫面及其變體。這個選項預設為停用。如果您首次查詢這些檢視區塊，但未將這個選項設為 `TRUE`，查詢就會失敗，並提供啟用選項的操作說明。啟用這項選項後，查詢會立即成功，並傳回從該時間點開始產生的資料。完整回填歷來資料後，大約需要一天才能在檢視畫面中顯示。如果您在推出這項設定前使用過這些檢視畫面，這個選項就已啟用。

### 費用和資源設定

請使用下列設定，決定資源的計費和連線方式。

* `default_storage_billing_model`：新資料集的預設儲存空間計費模式。將值設為 `PHYSICAL`，即可在計算儲存空間費用時使用實體位元組；設為 `LOGICAL` 則可使用邏輯位元組。請注意，變更預設儲存空間計費模式不會影響現有資料集。詳情請參閱「[儲存空間計費模式](https://docs.cloud.google.com/bigquery/docs/datasets-intro?hl=zh-tw#dataset_storage_billing_models)」。
* `default_cloud_resource_connection_id`：建立表格和模型時要使用的預設連線。請只指定連線的 ID 或名稱，並排除附加的專案 ID 和區域前置字元。使用預設連線可能會導致系統更新授予連線服務帳戶的權限，具體情況取決於您建立的表格或模型類型。詳情請參閱[預設連線總覽](https://docs.cloud.google.com/bigquery/docs/default-connections?hl=zh-tw)。
* `reservation_override_mode` ([預先發布版](https://docs.cloud.google.com/products?hl=zh-tw#product-launch-stages))：指定如何覆寫區域中的查詢預留項目 (例如 `'ALLOW_ANY_OVERRIDE'`)。詳情請參閱[`ALTER PROJECT SET OPTIONS` 選項清單](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#project_set_options_list)。
* `disable_on_demand_billing` ([預先發布版](https://docs.cloud.google.com/products?hl=zh-tw#product-launch-stages))：決定是否要為區域中的查詢停用以量計價。如果 `true`，所有查詢都必須使用已指派的預留位置，否則會失敗。詳情請參閱[`ALTER PROJECT SET OPTIONS`
  選項
  清單](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#project_set_options_list)。

## 定價

使用 BigQuery 設定服務不需額外付費。詳情請參閱「[定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw)」。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-09 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-09 (世界標準時間)。"],[],[]]