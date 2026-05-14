Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [參考資料](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# JOBS\_BY\_ORGANIZATION 檢視畫面

`INFORMATION_SCHEMA.JOBS_BY_ORGANIZATION` 檢視畫面包含與目前專案相關聯的機構中，所有已提交工作的近乎即時中繼資料。

## 必要角色

如要取得查詢 `INFORMATION_SCHEMA.JOBS_BY_ORGANIZATION` 檢視畫面所需的權限，請要求系統管理員授予您組織的「BigQuery 資源檢視者」 (`roles/bigquery.resourceViewer`) IAM 角色。如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和機構的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

這個預先定義的角色具備 `bigquery.jobs.listAll` 權限，可查詢 `INFORMATION_SCHEMA.JOBS_BY_ORGANIZATION` 檢視畫面。

您或許還可透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)取得這項權限。

只有已定義 Google Cloud機構的使用者才能使用結構定義表格。

如要進一步瞭解 BigQuery 權限，請參閱「[使用 IAM 控管存取權](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)」。

## 結構定義

基礎資料會依 `creation_time` 資料欄分區，並依 `project_id` 和 `user_email` 叢集。「`query_info`」欄包含查詢工作的其他資訊。

`INFORMATION_SCHEMA.JOBS_BY_ORGANIZATION` 檢視表具有下列結構定義：

| **資料欄名稱** | **資料類型** | **值** |
| --- | --- | --- |
| `bi_engine_statistics` | `RECORD` | 如果專案已設定為使用 [BI Engine](https://cloud.google.com/bigquery/docs/bi-engine-intro?hl=zh-tw)，這個欄位會包含 [BiEngineStatistics](https://cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#bienginestatistics)。否則為 `NULL`。 |
| `cache_hit` | `BOOLEAN` | 這項工作的查詢結果是否來自快取。 如果您有[多重查詢陳述式工作](https://docs.cloud.google.com/bigquery/docs/multi-statement-queries?hl=zh-tw)，則父項查詢的 `cache_hit` 為 `NULL`。 |
| `creation_time` | `TIMESTAMP` | (*分區資料欄*) 這項工作的建立時間。分區依據是這個時間戳記的世界標準時間。 |
| `destination_table` | `RECORD` | 結果的目標[資料表](https://cloud.google.com/bigquery/docs/reference/rest/v2/TableReference?hl=zh-tw) (如有)。 |
| `end_time` | `TIMESTAMP` | 這項工作的結束時間，自訓練週期後的毫秒數。這個欄位代表工作進入 `DONE` 狀態的時間。 |
| `error_result` | `RECORD` | 以 [ErrorProto](https://cloud.google.com/bigquery/docs/reference/rest/v2/ErrorProto?hl=zh-tw) 物件形式呈現的任何錯誤詳細資料。 |
| `folder_numbers` | `REPEATED INTEGER` | 含有專案的資料夾 ID 編號，從直接含有專案的資料夾開始，接著是含有子資料夾的資料夾，依此類推。舉例來說，如果 `folder_numbers` 是 `[1, 2, 3]`，則資料夾 `1` 會立即包含專案，資料夾 `2` 包含 `1`，而資料夾 `3` 包含 `2`。這個欄位只會在 `JOBS_BY_FOLDER` 中填入資料。 |
| `job_creation_reason.code` | `STRING` | 指定建立作業的高層次原因。  可能的值包括：  * `REQUESTED`：要求建立工作。 * `LONG_RUNNING`：查詢要求超出系統定義的逾時時間，該時間由 `QueryRequest` 中的 [timeoutMs 欄位指定。因此，系統會將其視為長時間執行的作業，並建立工作。](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs/query?hl=zh-tw#queryrequest) * `LARGE_RESULTS`：查詢結果無法納入內嵌回應。 * `OTHER`：系統判斷查詢需要以工作形式執行。 |
| `job_id` | `STRING` | 如果已建立工作，則為工作 ID。否則，請使用「選擇性建立工作」模式查詢的查詢 ID。例如 `bquxjob_1234`。 |
| `job_stages` | `RECORD` | 這項工作的[查詢階段](https://cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#ExplainQueryStage)。 **注意**：如果查詢是從設有資料列層級存取政策的資料表讀取資料，這個資料欄的值會是空白。詳情請參閱 [BigQuery 資料列層級安全防護最佳做法](https://docs.cloud.google.com/bigquery/docs/best-practices-row-level-security?hl=zh-tw)。 |
| `job_type` | `STRING` | 工作類型。可以是 `QUERY`、`LOAD`、`EXTRACT`、`COPY` 或 `NULL`。`NULL` 值表示背景工作。 |
| `labels` | `RECORD` | 以鍵/值組合形式套用至工作的標籤陣列。 |
| `parent_job_id` | `STRING` | 父項工作的 ID (如有)。 |
| `priority` | `STRING` | 這項工作的優先順序。有效值包括 `INTERACTIVE` 和 `BATCH`。 |
| `project_id` | `STRING` | (*叢集資料欄*) 專案的 ID。 |
| `project_number` | `INTEGER` | 專案編號。 |
| `referenced_tables` | `RECORD` | `STRUCT` 值陣列，其中包含查詢參照的每個資料表下列 `STRING` 欄位：`project_id`、`dataset_id` 和 `table_id`。只有非快取命中查詢作業會填入這項資料。 |
| `reservation_id` | `STRING` | 指派給這項工作的主要預留項目名稱，格式為 `RESERVATION_ADMIN_PROJECT:RESERVATION_LOCATION.RESERVATION_NAME`。  輸出內容：  * `RESERVATION_ADMIN_PROJECT`：管理預留項目的 Google Cloud 雲端專案名稱 * `RESERVATION_LOCATION`：預訂位置 * `RESERVATION_NAME`：預留項目名稱 |
| `edition` | `STRING` | 與指派給這項工作的預留項目相關聯的版本。如要進一步瞭解版本，請參閱「[BigQuery 版本簡介](https://docs.cloud.google.com/bigquery/docs/editions-intro?hl=zh-tw)」。 |
| `session_info` | `RECORD` | 這項工作執行的[工作階段](https://cloud.google.com/bigquery/docs/sessions-intro?hl=zh-tw)詳細資料 (如有)。 |
| `start_time` | `TIMESTAMP` | 這項工作的開始時間，自記錄週期後的毫秒數。這個欄位代表工作從 `PENDING` 狀態轉換為 `RUNNING` 或 `DONE` 的時間。 |
| `state` | `STRING` | 此工作的執行狀態。有效狀態包括 `PENDING`、`RUNNING` 和 `DONE`。 |
| `statement_type` | `STRING` | 查詢陳述式類型。例如：`DELETE`、`INSERT`、`SCRIPT`、`SELECT` 或 `UPDATE`。如需有效值清單，請參閱 [QueryStatementType](https://cloud.google.com/bigquery/docs/reference/auditlogs/rest/Shared.Types/BigQueryAuditMetadata.QueryStatementType?hl=zh-tw)。 |
| `timeline` | `RECORD` | 這項工作的[查詢時間軸](https://cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#QueryTimelineSample)。包含查詢執行作業的快照。 |
| `total_bytes_billed` | `INTEGER` | 如果專案設定為使用[依用量計價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#analysis_pricing_models)，這個欄位會顯示作業的總計費位元組數。如果專案已設為使用[固定費率計價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#analysis_pricing_models)，系統就不會針對位元組收費，這個欄位僅供參考。 **注意**：如果查詢是從設有資料列層級存取政策的資料表讀取資料，這個資料欄的值會是空白。詳情請參閱 [BigQuery 資料列層級安全防護最佳做法](https://docs.cloud.google.com/bigquery/docs/best-practices-row-level-security?hl=zh-tw)。 |
| `total_bytes_processed` | `INTEGER` | 工作處理的位元組總數。  **注意**：如果查詢是從設有資料列層級存取政策的資料表讀取資料，這個資料欄的值會是空白。詳情請參閱 [BigQuery 資料列層級安全防護最佳做法](https://docs.cloud.google.com/bigquery/docs/best-practices-row-level-security?hl=zh-tw)。 |
| `total_modified_partitions` | `INTEGER` | 工作修改的分區總數。這個欄位會填入 `LOAD` 和 `QUERY` 工作。 |
| `total_slot_ms` | `INTEGER` | 工作在 `RUNNING` 狀態的整個期間內，包括重試，所用的運算單元毫秒數。 |
| `total_services_sku_slot_ms` | `INTEGER` | 在外部服務上執行的工作，以及以服務 SKU 計費的工作，其總計的時段毫秒數。這個欄位只會填入有外部服務費用的工作，且是帳單方式為 `"SERVICES_SKU"` 的費用用量總計。 |
| `transaction_id` | `STRING` | 這項工作執行的[交易](https://cloud.google.com/bigquery/docs/transactions?hl=zh-tw) ID (如有)。 |
| `user_email` | `STRING` | (*分群資料欄*) 執行作業的使用者電子郵件地址或服務帳戶。 |
| `principal_subject` | `STRING` | 執行作業的主體身分字串表示法。 |
| `query_info.resource_warning` | `STRING` | 如果查詢處理期間的資源用量超過系統的內部門檻，就會顯示警告訊息。 如果查詢工作成功，`resource_warning` 欄位就會填入資料。使用 `resource_warning`，您可取得額外的資料點，藉此最佳化查詢，並使用 `query_hashes` 設定同等查詢集的成效趨勢監控。 |
| `query_info.query_hashes.normalized_literals` | `STRING` | 包含查詢的雜湊值。`normalized_literals` 是十六進位 `STRING` 雜湊，會忽略註解、參數值、UDF 和常值。如果基礎檢視區塊變更，或查詢隱含參照資料欄 (例如 `SELECT *`)，且資料表結構定義變更，雜湊值就會不同。  這個欄位會顯示成功的 [GoogleSQL](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw) 查詢，但不會顯示快取命中。 |
| `query_info.performance_insights` | `RECORD` | 工作的[效能洞察資料](https://cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#PerformanceInsights)。 |
| `query_info.optimization_details` | `STRUCT` | 這項工作[以記錄為依據進行最佳化](https://docs.cloud.google.com/bigquery/docs/history-based-optimizations?hl=zh-tw)。只有 `JOBS_BY_PROJECT` 檢視畫面會顯示這個資料欄。 |
| `transferred_bytes` | `INTEGER` | 跨雲端查詢 (例如 BigQuery Omni 跨雲端移轉工作) 的總移轉位元組數。 |
| `materialized_view_statistics` | `RECORD` | 查詢作業中考量的[具體化檢視表統計資料](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#MaterializedViewStatistics)。([預覽](https://cloud.google.com/products?hl=zh-tw#product-launch-stages)) |
| `metadata_cache_statistics` | `RECORD` | 查詢工作所參照[資料表的中繼資料欄索引使用統計資料](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#metadatacachestatistics)。 |
| `search_statistics` | `RECORD` | [搜尋查詢的統計資料。](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#SearchStatistics) |
| `query_dialect` | `STRING` | 這個欄位將於 2025 年 5 月推出。 用於工作的查詢方言。有效值包括：   * `GOOGLE_SQL`：這項作業要求使用 GoogleSQL。 * `LEGACY_SQL`：要求工作使用舊版 SQL。 * `DEFAULT_LEGACY_SQL`：工作要求中未指定查詢方言。   BigQuery 使用 LegacySQL 的預設值。 * `DEFAULT_GOOGLE_SQL`：工作要求中未指定查詢方言。   BigQuery 使用 GoogleSQL 的預設值。   如果是使用者提交的工作，這個欄位只會填入查詢工作。 您可以透過[設定](https://docs.cloud.google.com/bigquery/docs/default-configuration?hl=zh-tw#configuration-settings)控制預設選取的查詢方言。  如果是背景作業，這個欄位的值不會受到預設查詢方言設定的控制，也不會影響使用者提交的作業。部分背景工作會省略這個值。 |
| `continuous` | `BOOLEAN` | 工作是否為[持續查詢](https://cloud.google.com/bigquery/docs/continuous-queries-introduction?hl=zh-tw)。 |
| `continuous_query_info.output_watermark` | `TIMESTAMP` | 代表持續查詢成功處理資料的點。 |
| `vector_search_statistics` | `RECORD` | [向量搜尋查詢的統計資料。](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#VectorSearchStatistics) |
| `external_service_costs` | `RECORD` | 查詢作業的外部服務費用相關資訊陣列。 |

為確保穩定性，建議您在資訊結構定義查詢中明確列出資料欄，而非使用萬用字元 (`SELECT *`)。明確列出資料欄可避免基礎結構定義變更時，查詢中斷。

## 資料保留

這個檢視畫面會顯示執行中的工作，以及過去 180 天的工作記錄。
如果專案遷移至機構 (無論是從沒有機構或從其他機構遷移)，則無法透過 `INFORMATION_SCHEMA.JOBS_BY_ORGANIZATION` 檢視遷移日期前的作業資訊，因為該檢視畫面只會保留遷移日期後的資料。

## 範圍和語法

對這個檢視表執行的查詢必須包含[區域限定詞](https://docs.cloud.google.com/bigquery/docs/information-schema-intro?hl=zh-tw#syntax)。下表說明這個檢視畫面的區域範圍：

| 檢視表名稱 | 資源範圍 | 區域範圍 |
| --- | --- | --- |
| `` [PROJECT_ID.]`region-REGION`.INFORMATION_SCHEMA.JOBS_BY_ORGANIZATION `` | 包含指定專案的機構 | `REGION` |

取代下列項目：

* 選用：`PROJECT_ID`：專案 ID。 Google Cloud 如未指定，系統會使用預設專案。
* `REGION`：任何[資料集區域名稱](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)。
  例如：`` `region-us` ``。**注意：**您必須使用[區域限定詞](https://docs.cloud.google.com/bigquery/docs/information-schema-intro?hl=zh-tw#region_qualifier)查詢 `INFORMATION_SCHEMA` 檢視畫面。查詢執行位置必須與 `INFORMATION_SCHEMA` 檢視區塊的區域相符。

**注意：** 查詢 `INFORMATION_SCHEMA.JOBS_BY_ORGANIZATION` 以找出查詢工作的摘要費用時，請排除 `SCRIPT` 陳述式類型，否則部分值可能會重複計算。`SCRIPT` 列包含所有子項作業的摘要值，這些作業是做為這項作業的一部分執行。

## 限制

`INFORMATION_SCHEMA.JOBS_BY_ORGANIZATION` 檢視畫面會顯示目前機構所屬專案執行的工作。即使其他機構的專案執行的工作會存取目前機構的資源 (例如共用資料集)，這個檢視畫面也不會顯示這些工作。舉例來說，如果您與其他機構的專案共用資料集，則專案為存取資料集中的資料而執行的任何工作，都不會納入這個檢視畫面。

## 範例

如要對預設專案以外的專案執行查詢，請使用以下格式新增專案 ID：

```
`PROJECT_ID`.`region-REGION_NAME`.INFORMATION_SCHEMA.JOBS_BY_ORGANIZATION
```

更改下列內容：

* `PROJECT_ID`：專案 ID
* `REGION_NAME`：專案的區域

例如 `` `myproject`.`region-us`.INFORMATION_SCHEMA.JOBS_BY_ORGANIZATION ``。

### 找出今天掃描最多位元組的前五個工作

以下範例說明如何找出機構在當天掃描最多位元組的五項工作。你可以進一步篩選 `statement_type`，查詢其他資訊，例如負載、匯出和查詢。

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
  total_bytes_billed DESC
LIMIT 5;
```

**注意：** `INFORMATION_SCHEMA` 檢視表名稱會區分大小寫。

結果大致如下：

```
+--------------+--------------+---------------------------+
| job_id       |  user_email  |  total_bytes_billed       |
+--------------+--------------+---------------------------+
| bquxjob_1    |  abc@xyz.com |    999999                 |
| bquxjob_2    |  def@xyz.com |    888888                 |
| bquxjob_3    |  ghi@xyz.com |    777777                 |
+--------------+--------------+---------------------------+
```

### 在機構層級匯總每位使用者的連結試算表用量

以下查詢會提供貴機構過去 30 天內，主要連結試算表使用者的摘要，並依總計帳單資料量排序。這項查詢會彙整每位使用者的查詢總數、計費位元組總數和運算單元毫秒總數。這項資訊有助於瞭解資源採用情況，以及找出資源用量最多的消費者。

```
SELECT
  user_email,
  COUNT(*) AS total_queries,
  SUM(total_bytes_billed) AS total_bytes_billed,
  SUM(total_slot_ms) AS total_slot_ms
FROM
  `region-REGION_NAME.INFORMATION_SCHEMA.JOBS_BY_ORGANIZATION`
WHERE
  -- Filter for jobs created in the last 30 days
  creation_time >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 30 DAY)
  -- Filter for jobs originating from Connected Sheets
  AND job_id LIKE 'sheets_dataconnector%'
  -- Filter for completed jobs
  AND state = 'DONE'
  AND (statement_type IS NULL OR statement_type <> 'SCRIPT')
GROUP BY
  1
ORDER BY
  total_bytes_billed DESC;
```

將 `REGION_NAME` 替換為專案的區域。例如：`region-us`。

**注意：** 您必須使用區域限定詞查詢 `INFORMATION_SCHEMA` 檢視畫面。查詢執行的位置必須與`INFORMATION_SCHEMA`檢視區塊的區域相符。

傳回的結果看起來類似下列內容：

```
+---------------------+---------------+--------------------+-----------------+
| user_email          | total_queries | total_bytes_billed | total_slot_ms   |
+---------------------+---------------+--------------------+-----------------+
| alice@example.com   | 152           | 12000000000        | 3500000         |
| bob@example.com     | 45            | 8500000000         | 2100000         |
| charles@example.com | 210           | 1100000000         | 1800000         |
+---------------------+---------------+--------------------+-----------------+
```

### 在機構層級尋找連結試算表查詢作業的工作記錄

下列查詢會提供 Google 試算表連結執行的每項個別工作詳細記錄。這項資訊有助於稽核及找出特定高成本查詢。

```
SELECT
  job_id,
  creation_time,
  user_email,
  project_id,
  total_bytes_billed,
  total_slot_ms
FROM
  `region-REGION_NAME.INFORMATION_SCHEMA.JOBS_BY_ORGANIZATION`
WHERE
  creation_time >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 30 DAY)
  AND job_id LIKE 'sheets_dataconnector%'
  AND state = 'DONE'
  AND (statement_type IS NULL OR statement_type <> 'SCRIPT')
ORDER BY
  creation_time DESC;
```

將 `REGION_NAME` 替換為專案的區域。例如：`region-us`。

**注意：** 您必須使用區域限定詞查詢 `INFORMATION_SCHEMA` 檢視畫面。查詢執行的位置必須與`INFORMATION_SCHEMA`檢視區塊的區域相符。

傳回的結果看起來類似下列內容：

```
+---------------------------------+---------------------------------+-----------------+------------+--------------------+---------------+
| job_id                          | creation_time                   | user_email      | project_id | total_bytes_billed | total_slot_ms |
+---------------------------------+---------------------------------+-----------------+------------+--------------------+---------------+
| sheets_dataconnector_bquxjob_1  | 2025-11-06 00:26:53.077000 UTC  | abc@example.com | my_project | 12000000000        | 3500000       |
| sheets_dataconnector_bquxjob_2  | 2025-11-06 00:24:04.294000 UTC  | xyz@example.com | my_project | 8500000000         | 2100000       |
| sheets_dataconnector_bquxjob_3  | 2025-11-03 23:17:25.975000 UTC  | bob@example.com | my_project | 1100000000         | 1800000       |
+---------------------------------+---------------------------------+-----------------+------------+--------------------+---------------+
```




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-14 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-14 (世界標準時間)。"],[],[]]