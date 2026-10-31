Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [參考資料](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# JOBS\_BY\_ORGANIZATION 檢視表

`INFORMATION_SCHEMA.JOBS_BY_ORGANIZATION` 檢視表包含與目前專案相關聯的組織中，所有提交工作的近乎即時中繼資料。

## 必要角色

如要取得查詢 `INFORMATION_SCHEMA.JOBS_BY_ORGANIZATION` 檢視表所需的權限，請要求管理員授予您組織的 [BigQuery 資源檢視者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.resourceViewer)  (`roles/bigquery.resourceViewer`) IAM 角色。如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

這個預先定義的角色具備 `bigquery.jobs.listAll` 權限，可查詢 `INFORMATION_SCHEMA.JOBS_BY_ORGANIZATION` 檢視表。

您或許還可透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)取得這項權限。

只有已定義 Google Cloud組織的使用者，才能使用結構定義資料表。

如要進一步瞭解 BigQuery 權限，請參閱「[使用 IAM 控管存取權](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)」。

## 結構定義

基礎資料會依 `creation_time` 欄分區，並依 `project_id` 和 `user_email` 分群。`query_info` 欄包含查詢工作的其他資訊。

`INFORMATION_SCHEMA.JOBS_BY_ORGANIZATION` 檢視表具有下列結構定義：

| **資料欄名稱** | **資料類型** | **值** |
| --- | --- | --- |
| `bi_engine_statistics` | `RECORD` | 如果專案已設為使用 [BI Engine](https://docs.cloud.google.com/bigquery/docs/bi-engine-intro?hl=zh-tw)，這個欄位會包含 [BiEngineStatistics](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#bienginestatistics)。否則為 `NULL`。 |
| `cache_hit` | `BOOLEAN` | 這項工作的查詢結果是否來自快取。如果您有[多查詢陳述式工作](https://docs.cloud.google.com/bigquery/docs/multi-statement-queries?hl=zh-tw)，則父項查詢的 `cache_hit` 為 `NULL`。 |
| `copy_job_statistics` | `RECORD` | [複製工作的統計資料。](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#CopyJobStatistics) |
| `creation_time` | `TIMESTAMP` | (*分區資料欄*) 這項工作的建立時間。分區依據為這個時間戳記的世界標準時間。 |
| `destination_table` | `RECORD` | 結果的目的地[資料表](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/TableReference?hl=zh-tw) (如果有的話)。 |
| `end_time` | `TIMESTAMP` | 這項工作的結束時間，以毫秒為單位 (自 Epoch 起算)。這個欄位代表工作進入 `DONE` 狀態的時間。 |
| `error_result` | `RECORD` | 任何錯誤的詳細資料，以 [ErrorProto](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/ErrorProto?hl=zh-tw) 物件表示。 |
| `global_query_info` | `RECORD` | [全域查詢](https://docs.cloud.google.com/bigquery/docs/global-queries?hl=zh-tw)的相關資訊。 包含下列欄位：  * `parent_job_id`：主要區域中父項全域查詢工作的 ID。 * `parent_job_location`：父項全域查詢工作的所在位置。 * `remote_regions`：全域查詢參照的遠端區域陣列。 |
| `job_creation_reason.code` | `STRING` | 指定建立工作的主要原因。  可能的值包括：  * `REQUESTED`：已要求建立工作。 * `LONG_RUNNING`：查詢要求執行時間超過 `QueryRequest` 中 [timeoutMs   欄位指定的系統定義逾時時間。因此，系統會將這項作業視為長時間執行的作業，並建立工作。](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs/query?hl=zh-tw#queryrequest) * `LARGE_RESULTS`：查詢結果無法放入內嵌回應。 * `OTHER`：系統判定查詢必須以工作形式執行。 |
| `job_id` | `STRING` | 如果已建立工作，則為工作 ID。否則，則為使用選用工作建立模式的查詢 ID。例如 `bquxjob_1234`。 |
| `job_stages` | `RECORD REPEATED` | 工作的[查詢階段](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#ExplainQueryStage)。 **注意**：如果查詢是從具有資料列層級存取權政策的資料表讀取，則此資料欄的值會是空白。詳情請參閱「[BigQuery 資料列層級安全性的最佳做法](https://docs.cloud.google.com/bigquery/docs/best-practices-row-level-security?hl=zh-tw)」。 |
| `job_type` | `STRING` | 工作類型。可以是 `QUERY`、`LOAD`、`EXTRACT`、`COPY` 或 `NULL`。`NULL` 值表示背景工作。 |
| `labels` | `RECORD` | 套用至工作的標籤陣列，以鍵/值組合表示。 |
| `object_storage_stats` | `RECORD REPEATED` | 查詢工作的物件儲存庫和快取用量統計資料。這個值是重複記錄，包含下列欄位：   * `cloud_provider`：託管物件儲存庫的雲端服務供應商 (例如 `AWS`)。 * `object_storage_bytes_read`：直接從物件儲存庫讀取的位元組總數。 * `cache_bytes_read`：：從快取讀取的位元組總數。 |
| `parent_job_id` | `STRING` | 上層工作的 ID (如有)。 |
| `priority` | `STRING` | 這項工作的優先順序。有效值包括 `INTERACTIVE` 和 `BATCH`。 |
| `project_id` | `STRING` | (*分群欄*) 專案 ID。 |
| `project_number` | `INTEGER` | 專案編號。 |
| `referenced_tables` | `RECORD` | `STRUCT` 值陣列，其中包含查詢參照的每個資料表的下列 `STRING` 欄位：`project_id`、`dataset_id` 和 `table_id`。只有非快取命中的查詢工作會填入這項資料。 |
| `referenced_logical_views` | `RECORD` | `STRUCT` 值陣列，其中包含查詢參照的每個邏輯檢視表的下列 `STRING` 欄位：`project_id`、`dataset_id` 和 `table_id`。只有非快取命中的查詢工作會填入這項資料。 |
| `reservation_id` | `STRING` | 指派給這項工作的主要預留項目名稱，格式為 `RESERVATION_ADMIN_PROJECT:RESERVATION_LOCATION.RESERVATION_NAME`。  在這項輸出內容中：  * `RESERVATION_ADMIN_PROJECT`：   管理預留項目的 Google Cloud 專案名稱 * `RESERVATION_LOCATION`：預留項目的位置 * `RESERVATION_NAME`：預留項目名稱 |
| `reservation_group_path` | `ARRAY<STRING>` | 預留項目連結的預留項目群組。舉例來說，如果預留項目連結至群組 `my-group`，`reservation_group_path` 欄位會包含類似 `[my-group]` 的清單。 |
| `edition` | `STRING` | 與指派給這項工作的預留項目相關聯的版本。如要進一步瞭解版本，請參閱「[BigQuery 版本簡介](https://docs.cloud.google.com/bigquery/docs/editions-intro?hl=zh-tw)」。 |
| `session_info` | `RECORD` | 執行這項工作的[工作階段](https://docs.cloud.google.com/bigquery/docs/sessions-intro?hl=zh-tw)詳細資料 (如有)。 |
| `start_time` | `TIMESTAMP` | 這項工作的開始時間，以毫秒為單位 (從 Epoch 紀元時間起算)。這個欄位代表工作從 `PENDING` 狀態轉換為 `RUNNING` 或 `DONE` 的時間。 |
| `state` | `STRING` | 此工作的執行狀態。有效狀態包括 `PENDING`、`RUNNING` 和 `DONE`。 |
| `statement_type` | `STRING` | 查詢陳述式的類型。例如：`DELETE`、`INSERT`、`SCRIPT`、`SELECT` 或 `UPDATE`。如需有效值清單，請參閱 [QueryStatementType](https://docs.cloud.google.com/bigquery/docs/reference/auditlogs/rest/Shared.Types/BigQueryAuditMetadata.QueryStatementType?hl=zh-tw)。 |
| `timeline` | `RECORD` | 工作的[查詢時間軸](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#QueryTimelineSample)。包含查詢執行的快照。 |
| `total_bytes_billed` | `INTEGER` | 如果專案設為採用[隨選計價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#analysis_pricing_models)模式，這個欄位會顯示工作的計費位元組總數。如果專案設為使用[固定費率定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#analysis_pricing_models)，系統就不會向您收取位元組費用，而這個欄位僅供參考。 **注意**：如果查詢是從具有資料列層級存取權政策的資料表讀取，則此資料欄的值會是空白。詳情請參閱「[BigQuery 資料列層級安全性的最佳做法](https://docs.cloud.google.com/bigquery/docs/best-practices-row-level-security?hl=zh-tw)」。 |
| `total_bytes_processed` | `INTEGER` | 工作處理的位元組總數。  **注意**：如果查詢是從具有資料列層級存取權政策的資料表讀取，則此資料欄的值會是空白。詳情請參閱「[BigQuery 資料列層級安全性的最佳做法](https://docs.cloud.google.com/bigquery/docs/best-practices-row-level-security?hl=zh-tw)」。 |
| `total_modified_partitions` | `INTEGER` | 工作修改的分區總數。系統會為 `LOAD` 和 `QUERY` 工作填入這個欄位。 |
| `total_slot_ms` | `INTEGER` | 上次執行工作的運算單元時間 (毫秒)，不含先前的重試 (如有)。 |
| `total_services_sku_slot_ms` | `INTEGER` | 在外部服務上執行的工作，其總運算單元毫秒數，並依服務 SKU 計費。這個欄位只會填入產生外部服務費用的工作，且為計費方式為 `"SERVICES_SKU"` 的費用總用量。 |
| `transaction_id` | `STRING` | 執行這項工作的[交易](https://docs.cloud.google.com/bigquery/docs/transactions?hl=zh-tw) ID (如果有的話)。 |
| `user_email` | `STRING` | (*分群欄*) 執行工作的使用者電子郵件地址或服務帳戶。 |
| `principal_subject` | `STRING` | 執行工作的實體身分字串表示法。 |
| `query_info.resource_warning` | `STRING` | 如果查詢處理期間的資源用量超過系統內部門檻，就會顯示警告訊息。 如果查詢工作成功，系統會填入 `resource_warning` 欄位。`resource_warning` 可提供額外的資料點，協助您最佳化查詢，並使用 `query_hashes` 設定監控功能，追蹤一組同等查詢的效能趨勢。 |
| `query_info.query_hashes.normalized_literals` | `STRING` | 包含查詢的雜湊值。`normalized_literals` 是十六進位 `STRING` 雜湊，會忽略註解、參數值、UDF 和常值。如果基礎檢視表變更，或查詢隱含參照資料欄 (例如 `SELECT *`)，且資料表結構定義變更，雜湊值就會不同。  如果 [GoogleSQL](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw) 查詢成功，但未命中快取，就會顯示這個欄位。 |
| `query_info.performance_insights` | `RECORD` | 工作的[效能深入分析](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#PerformanceInsights)。 |
| `transferred_bytes` | `INTEGER` | BigQuery Omni 查詢 (例如 BigQuery Omni 移轉工作) 移轉的總位元組數。 |
| `materialized_view_statistics` | `RECORD` | 查詢工作中考量的[materialized view 統計資料](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#MaterializedViewStatistics)。([預先發布版](https://cloud.google.com/products?hl=zh-tw#product-launch-stages)) |
| `metadata_cache_statistics` | `RECORD` | 查詢工作中參照的[資料表中繼資料欄索引使用情形統計資料](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#metadatacachestatistics)。 |
| `search_statistics` | `RECORD` | [搜尋查詢的統計資料。](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#SearchStatistics) |
| `query_dialect` | `STRING` | 這個欄位將於 2025 年 5 月推出。 工作使用的查詢方言。有效值包括：   * `GOOGLE_SQL`：工作要求使用 GoogleSQL。 * `LEGACY_SQL`：工作要求使用 LegacySQL。 * `DEFAULT_LEGACY_SQL`：工作要求中未指定查詢方言。   BigQuery 使用 LegacySQL 的預設值。 * `DEFAULT_GOOGLE_SQL`：工作要求中未指定查詢方言。   BigQuery 使用 GoogleSQL 的預設值。   如果是使用者提交的工作，這個欄位只會填入查詢工作。 您可以透過[設定](https://docs.cloud.google.com/bigquery/docs/default-configuration?hl=zh-tw#configuration-settings)控制查詢方言的預設選項。  如果是背景工作，這個欄位的值不受預設查詢方言設定控制，也不會影響使用者提交的工作。如果是某些背景工作，系統會省略這個值。 |
| `continuous` | `BOOLEAN` | 工作是否為[持續查詢](https://docs.cloud.google.com/bigquery/docs/continuous-queries-introduction?hl=zh-tw)。 |
| `continuous_query_info.output_watermark` | `TIMESTAMP` | 代表持續查詢已成功處理資料的時間點。 |
| `vector_search_statistics` | `RECORD` | [向量搜尋查詢的統計資料。](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#VectorSearchStatistics) |
| `external_service_costs` | `RECORD` | 查詢工作的外部服務費用資訊陣列。 |
| `ml_statistics.model_type` | `STRING` | 如果工作是 BigQuery ML 模型建立查詢，這個欄位會指定要建立的[模型類型](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/models?hl=zh-tw#ModelType)。如果是其他工作，這個值會是 `NULL`。 |

為確保穩定性，建議您在資訊結構定義查詢中明確列出資料欄，而非使用萬用字元 (`SELECT *`)。明確列出資料欄可避免查詢在基礎結構定義變更時中斷。

## 資料保留

這個檢視畫面會顯示執行中的工作，以及過去 180 天的工作記錄。如果專案從無機構狀態或不同機構遷移至某個機構，則無法透過 `INFORMATION_SCHEMA.JOBS_BY_ORGANIZATION` 檢視畫面存取遷移日期之前的作業資訊，因為該檢視畫面只會保留遷移日期之後的資料。

## 範圍和語法

對這個檢視表執行的查詢必須包含[區域限定詞](https://docs.cloud.google.com/bigquery/docs/information-schema-intro?hl=zh-tw#syntax)。下表說明這個檢視畫面的區域範圍：

| 檢視表名稱 | 資源範圍 | 區域範圍 |
| --- | --- | --- |
| `` [PROJECT_ID.]`region-REGION`.INFORMATION_SCHEMA.JOBS_BY_ORGANIZATION `` | 包含指定專案的組織 | `REGION` |

請替換下列項目：

* 選用：`PROJECT_ID`： Google Cloud 專案的 ID。如未指定，則會使用預設專案。
* `REGION`：任何[資料集區域名稱](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)。例如：`` `region-us` ``。**注意：**您必須使用[區域限定詞](https://docs.cloud.google.com/bigquery/docs/information-schema-intro?hl=zh-tw#region_qualifier)，才能查詢 `INFORMATION_SCHEMA` 檢視表。查詢執行位置必須與 `INFORMATION_SCHEMA` 檢視表的區域相符。

**注意：** 查詢 `INFORMATION_SCHEMA.JOBS_BY_ORGANIZATION` 以找出查詢工作的費用摘要時，請排除 `SCRIPT` 陳述式類型，否則部分值可能會重複計算。`SCRIPT` 列包含這項工作執行的所有子項工作摘要值。

## 限制

`INFORMATION_SCHEMA.JOBS_BY_ORGANIZATION` 檢視表包含目前組織所屬專案執行的工作。即使其他組織的專案執行的工作存取了目前組織中的資源 (例如共用資料集)，這類工作也不會顯示在這個檢視畫面中。舉例來說，如果您與其他組織的專案共用資料集，則該專案為存取資料集內資料而執行的任何工作，都不會包含在這個檢視表中。

## 範例

如要對預設專案以外的專案執行查詢，請按照下列格式新增專案 ID：

```
`PROJECT_ID`.`region-REGION_NAME`.INFORMATION_SCHEMA.JOBS_BY_ORGANIZATION
```

更改下列內容：

* `PROJECT_ID`：專案 ID
* `REGION_NAME`：專案的區域

例如 `` `myproject`.`region-us`.INFORMATION_SCHEMA.JOBS_BY_ORGANIZATION ``。

### 找出今天掃描最多位元組的前五項工作

以下範例說明如何找出組織當天掃描最多位元組的五項工作。您可以進一步篩選 `statement_type`，查詢其他資訊，例如載入、匯出和查詢。

```
SELECT
  job_id,
  user_email,
  total_bytes_billed
FROM
  `region-REGION_NAME`.INFORMATION_SCHEMA.JOBS_BY_ORGANIZATION
WHERE
  EXTRACT(DATE FROM  creation_time) = current_date()
ORDER BY
```