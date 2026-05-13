Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [參考資料](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 「JOBS」檢視畫面

「`INFORMATION_SCHEMA.JOBS`」檢視畫面包含目前專案中所有 BigQuery 工作的近乎即時中繼資料。

**注意：** 「檢視畫面名稱」`INFORMATION_SCHEMA.JOBS`和`INFORMATION_SCHEMA.JOBS_BY_PROJECT`
是同義詞，可互換使用。

## 必要角色

如要取得查詢 `INFORMATION_SCHEMA.JOBS` 檢視畫面所需的權限，請要求系統管理員授予您專案的「[BigQuery 資源檢視者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.resourceViewer) 」(`roles/bigquery.resourceViewer`) IAM 角色。如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和機構的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

這個預先定義的角色具備 `bigquery.jobs.listAll` 權限，可查詢 `INFORMATION_SCHEMA.JOBS` 檢視畫面。

您或許還可透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)取得這項權限。

如要進一步瞭解 BigQuery 權限，請參閱「[使用 IAM 控管存取權](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)」。

## 結構定義

基礎資料會依 `creation_time` 資料欄分區，並依 `project_id` 和 `user_email` 分群。「`query_info`」欄包含查詢工作的其他資訊。

`INFORMATION_SCHEMA.JOBS` 檢視表具有下列結構定義：

| **資料欄名稱** | **資料類型** | **值** |
| --- | --- | --- |
| `bi_engine_statistics` | `RECORD` | 如果專案已設定為使用 [BI Engine](https://cloud.google.com/bigquery/docs/bi-engine-intro?hl=zh-tw)，這個欄位會包含 [BiEngineStatistics](https://cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#bienginestatistics)。否則為 `NULL`。 |
| `cache_hit` | `BOOLEAN` | 這項工作的查詢結果是否來自快取。 如果您有[多重查詢陳述式工作](https://docs.cloud.google.com/bigquery/docs/multi-statement-queries?hl=zh-tw)，則父項查詢的 `cache_hit` 為 `NULL`。 |
| `creation_time` | `TIMESTAMP` | (*分區資料欄*) 這項工作的建立時間。分區依據是這個時間戳記的世界標準時間。 |
| `destination_table` | `RECORD` | 結果的目標[資料表](https://cloud.google.com/bigquery/docs/reference/rest/v2/TableReference?hl=zh-tw) (如有)。 |
| `dml_statistics` | `RECORD` | 如果工作是含有 DML 陳述式的查詢，則值為含有下列欄位的記錄：   * `inserted_row_count`：插入的資料列數。 * `deleted_row_count`：已刪除的資料列數。 * `updated_row_count`：更新的資料列數。  如果是其他工作，值為 `NULL`。  這個資料欄會顯示在「`INFORMATION_SCHEMA.JOBS_BY_USER`」和「`INFORMATION_SCHEMA.JOBS_BY_PROJECT`」檢視畫面中。 |
| `end_time` | `TIMESTAMP` | 這項工作的結束時間，自訓練週期後的毫秒數。這個欄位代表工作進入 `DONE` 狀態的時間。 |
| `error_result` | `RECORD` | 以 [ErrorProto](https://cloud.google.com/bigquery/docs/reference/rest/v2/ErrorProto?hl=zh-tw) 物件形式呈現的任何錯誤詳細資料。 |
| `job_creation_reason.code` | `STRING` | 指定建立作業的高層次原因。  可能的值包括：  * `REQUESTED`：要求建立工作。 * `LONG_RUNNING`：查詢要求超出系統定義的逾時時間，該時間由 `QueryRequest` 中的 [timeoutMs 欄位指定。因此，系統會將其視為長時間執行的作業，並建立工作。](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs/query?hl=zh-tw#queryrequest) * `LARGE_RESULTS`：查詢結果無法納入內嵌回應。 * `OTHER`：系統判斷查詢需要以工作形式執行。 |
| `job_id` | `STRING` | 如果已建立工作，則為工作 ID。否則，請使用「選擇性建立工作」模式查詢的查詢 ID。例如 `bquxjob_1234`。 |
| `job_stages` | `RECORD` | 這項工作的[查詢階段](https://cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#ExplainQueryStage)。 **注意**：如果查詢是從設有資料列層級存取政策的資料表讀取資料，這個資料欄的值會是空白。詳情請參閱 [BigQuery 資料列層級安全防護最佳做法](https://docs.cloud.google.com/bigquery/docs/best-practices-row-level-security?hl=zh-tw)。 |
| `job_type` | `STRING` | 工作類型。可以是 `QUERY`、`LOAD`、`EXTRACT`、`COPY` 或 `NULL`。`NULL` 值表示背景工作。 |
| `labels` | `RECORD` | 以鍵/值組合形式套用至工作的標籤陣列。 |
| `parent_job_id` | `STRING` | 父項工作的 ID (如有)。 |
| `priority` | `STRING` | 這項工作的優先順序。有效值包括 `INTERACTIVE` 和 `BATCH`。 |
| `project_id` | `STRING` | (*叢集資料欄*) 專案的 ID。 |
| `project_number` | `INTEGER` | 專案編號。 |
| `query` | `STRING` | SQL 查詢文字。 |
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

查詢 `INFORMATION_SCHEMA.JOBS` 以找出查詢工作的摘要費用時，請排除 `SCRIPT` 陳述式類型，否則部分值可能會重複計算。`SCRIPT` 列包含所有子項工作的摘要值，這些子項工作是這項工作的一部分。

為確保穩定性，建議您在資訊結構定義查詢中明確列出資料欄，而非使用萬用字元 (`SELECT *`)。明確列出資料欄可避免基礎結構定義變更時，查詢中斷。

## 多陳述式查詢工作

多重陳述式查詢工作是指使用[程序語言](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/procedural-language?hl=zh-tw)的查詢工作。多重陳述式查詢作業通常會使用 `DECLARE` 定義變數，或使用控制流程陳述式 (例如 `IF` 或 `WHILE`)。查詢 `INFORMATION_SCHEMA.JOBS` 時，您可能需要瞭解多重陳述式查詢工作和其他工作的差異。多重陳述式查詢作業具有下列特徵：

* `statement_type` = `SCRIPT`
* `reservation_id` = `NULL`

### 子項工作

多重陳述式查詢工作的每個子工作都有 `parent_job_id`，指向多重陳述式查詢工作本身。包括所有做為這項工作一部分執行的子項工作的摘要值。

如果您查詢 `INFORMATION_SCHEMA.JOBS` 是為了找出查詢工作的費用摘要，則應排除 `SCRIPT` 陳述式類型。否則，系統可能會重複計算部分值，例如 `total_slot_ms`。

## 資料保留

這個檢視畫面會顯示執行中的工作，以及過去 180 天的工作記錄。
如果專案遷移至機構 (無論是從沒有機構或從其他機構遷移)，您都無法透過 `INFORMATION_SCHEMA.JOBS` 檢視遷移日期前的作業資訊，因為該檢視畫面只會保留遷移日期後的資料。

## 範圍和語法

對這個檢視表執行的查詢必須包含[區域限定詞](https://docs.cloud.google.com/bigquery/docs/information-schema-intro?hl=zh-tw#syntax)。下表說明這個檢視畫面的區域範圍：

| 檢視表名稱 | 資源範圍 | 區域範圍 |
| --- | --- | --- |
| `` [PROJECT_ID.]`region-REGION`.INFORMATION_SCHEMA.JOBS[_BY_PROJECT] `` | 專案層級 | `REGION` |

取代下列項目：

* 選用：`PROJECT_ID`：專案 ID。 Google Cloud 如未指定，系統會使用預設專案。
* `REGION`：任何[資料集區域名稱](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)。
  例如：`` `region-us` ``。**注意：**您必須使用[區域限定詞](https://docs.cloud.google.com/bigquery/docs/information-schema-intro?hl=zh-tw#region_qualifier)查詢 `INFORMATION_SCHEMA` 檢視畫面。查詢執行位置必須與 `INFORMATION_SCHEMA` 檢視區塊的區域相符。

## 查詢模擬測試估算值

如果您對參照 `INFORMATION_SCHEMA.JOBS` 檢視區塊的查詢執行模擬測試，估算的處理位元組數可能會遠高於查詢執行期間實際處理的位元組數。

發生高估情況的原因是，試算表計算時只會考量基礎資料的 `creation_time` 分區資料欄篩選器。如果 `WHERE` 子句中指定了隱含 `project_id` 篩選器或 `user_email` 篩選器，則系統不會將這些篩選器納入[叢集資料欄](#schema)的考量。實際掃描的資料量可能遠低於模擬測試估計值，尤其是工作較少的專案或使用者。

如果未在 `creation_time` 上指定篩選器，系統就不會進行分區修剪，而模擬測試預估值會反映基礎資料的所有分區掃描結果。不過，資料叢集仍可能減少實際處理的位元組數，低於這項估算值。

## 範例

如要對預設專案以外的專案執行查詢，請使用以下格式新增專案 ID：

```
`PROJECT_ID`.`region-REGION_NAME`.INFORMATION_SCHEMA.JOBS
```

更改下列內容：

* `PROJECT_ID`：專案 ID。
* `REGION_NAME`：專案的區域。

例如 `` `myproject`.`region-us-central1`.INFORMATION_SCHEMA.JOBS ``。

**注意：** 為盡可能提高查詢效率，請盡量依 `creation_time` 欄位篩選。這樣 BigQuery 就能縮減分區，進而提升查詢效能並降低成本。

### 比較以量計價的工作用量與帳單資料

如果專案採用[以量計價方案](https://cloud.google.com/bigquery/pricing?hl=zh-tw#on_demand_pricing)，您可以使用 `INFORMATION_SCHEMA.JOBS` 檢視畫面，查看特定期間的運算費用。

如果專案採用[以容量為準 (配額) 的定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#capacity_compute_analysis_pricing)，您可以使用 [`INFORMATION_SCHEMA.RESERVATIONS_TIMELINE`](https://docs.cloud.google.com/bigquery/docs/information-schema-reservation-timeline?hl=zh-tw) 查看特定期間的運算費用。

下列查詢會產生每日預估的帳單 TiB 總計，以及由此產生的費用。「[限制](#limitations)」一節說明這些預估值可能與帳單不符的情況。

僅限這個範例，您必須設定下列其他變數。您可以在這裡編輯這些設定，方便使用。

* `START_DATE`：最早的匯總日期 (含)。
* `END_DATE`：要匯總的最新日期 (含)。
* `PRICE_PER_TIB`：用於帳單預估的[每 TiB 以量計價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#on_demand_pricing)。

```
CREATE TEMP FUNCTION isBillable(error_result ANY TYPE)
AS (
  -- You aren't charged for queries that return an error.
  error_result IS NULL
  -- However, canceling a running query might incur charges.
  OR error_result.reason = 'stopped'
);

-- BigQuery hides the number of bytes billed on all queries against tables with
-- row-level security.
CREATE TEMP FUNCTION isMaybeUsingRowLevelSecurity(
  job_type STRING, tib_billed FLOAT64, error_result ANY TYPE)
AS (
  job_type = 'QUERY'
  AND tib_billed IS NULL
  AND isBillable(error_result)
);

WITH
  query_params AS (
    SELECT
      date 'START_DATE' AS start_date,  -- inclusive
      date 'END_DATE' AS end_date,  -- inclusive
  ),
  usage_with_multiplier AS (
    SELECT
      job_type,
      error_result,
      creation_time,
      -- Jobs are billed by end_time in PST8PDT timezone, regardless of where
      -- the job ran.
      EXTRACT(date FROM end_time AT TIME ZONE 'PST8PDT') billing_date,
      total_bytes_billed / 1024 / 1024 / 1024 / 1024 total_tib_billed,
      CASE statement_type
        WHEN 'SCRIPT' THEN 0
        WHEN 'CREATE_MODEL' THEN 50 * PRICE_PER_TIB
        ELSE PRICE_PER_TIB
        END AS multiplier,
    FROM `region-REGION_NAME`.INFORMATION_SCHEMA.JOBS
    WHERE statement_type <> 'SCRIPT'
  )
SELECT
  billing_date,
  sum(total_tib_billed * multiplier) estimated_charge,
  sum(total_tib_billed) estimated_usage_in_tib,
  countif(isMaybeUsingRowLevelSecurity(job_type, total_tib_billed, error_result))
    AS jobs_using_row_level_security,
FROM usage_with_multiplier, query_params
WHERE
  1 = 1
  -- Filter by creation_time for partition pruning.
  AND date(creation_time) BETWEEN date_sub(start_date, INTERVAL 2 day) AND date_add(end_date, INTERVAL 1 day)
  AND billing_date BETWEEN start_date AND end_date
  AND isBillable(error_result)
GROUP BY billing_date
ORDER BY billing_date;
```

#### 限制

* 如果查詢的資料表採用資料列層級安全防護機制，BigQuery 會[隱藏部分統計資料](https://docs.cloud.google.com/bigquery/docs/best-practices-row-level-security?hl=zh-tw#limit-side-channel-attacks)。提供的查詢會計算受影響的作業數量 (如 `jobs_using_row_level_security` 所示)，但無法存取可計費用量。
* BigQuery ML [以量計價的查詢費用](https://cloud.google.com/bigquery/pricing?hl=zh-tw#ml_on_demand_pricing)取決於建立的模型類型。`INFORMATION_SCHEMA.JOBS` 不會追蹤建立的模型類型，因此提供的查詢會假設所有 CREATE\_MODEL 陳述式都建立較高費用的模型類型。
* Apache Spark 程序採用[類似的定價模式](https://docs.cloud.google.com/bigquery/docs/spark-procedures?hl=zh-tw#pricing)，但費用會以 [BigQuery Enterprise 版即付即用 SKU](https://cloud.google.com/bigquery/pricing?hl=zh-tw#capacity_compute_analysis_pricing) 形式列出。`INFORMATION_SCHEMA.JOBS` 會將這項用量記錄為 `total_bytes_billed`，但無法判斷用量代表哪個 SKU。

### 計算平均運算單元用量

以下範例會計算特定專案在過去 7 天內，所有查詢的平均運算單元用量。請注意，如果專案在一週內使用的時段一致，這項計算結果就會最準確。如果專案的運算單元用量不穩定，這個數字可能會低於預期。

執行查詢：

```
SELECT
  SUM(total_slot_ms) / (1000 * 60 * 60 * 24 * 7) AS avg_slots
FROM
  `region-REGION_NAME`.INFORMATION_SCHEMA.JOBS
WHERE
  -- Filter by the partition column first to limit the amount of data scanned.
  -- Eight days allows for jobs created before the 7 day end_time filter.
  creation_time BETWEEN TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 8 DAY) AND CURRENT_TIMESTAMP()
  AND job_type = 'QUERY'
  AND statement_type != 'SCRIPT'
  AND end_time BETWEEN TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 7 DAY) AND CURRENT_TIMESTAMP();
```

**注意：** `INFORMATION_SCHEMA` 檢視表名稱會區分大小寫。

結果大致如下：

```
+------------+
| avg_slots  |
+------------+
| 3879.1534  |
+------------+
```

您可以使用 `WHERE reservation_id = "…"` 檢查特定預留項目的用量。這有助於判斷一段時間內保留項目的使用百分比。如果是指令碼工作，父項工作也會回報子項工作的總運算單元用量。為避免重複計算，請使用 `WHERE statement_type != "SCRIPT"` 排除父項工作。

如要檢查個別作業的平均工作階段使用率，請改用 `total_slot_ms / TIMESTAMP_DIFF(end_time, start_time, MILLISECOND)`。

### 依查詢優先順序計算近期執行中的查詢數量

以下範例會顯示過去 7 小時內啟動的查詢數量，並依優先順序 (互動式或批次) 分組：

```
SELECT
  priority,
  COUNT(*) active_jobs
FROM
  `region-REGION_NAME`.INFORMATION_SCHEMA.JOBS
WHERE
  creation_time > TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 7 hour)
  AND job_type = 'QUERY'
GROUP BY priority;
```

結果大致如下：

```
+-------------+-------------+
| priority    | active_jobs |
+-------------+-------------+
| INTERACTIVE |           2 |
| BATCH       |           3 |
+-------------+-------------+
```

`priority` 欄位會指出查詢是 `INTERACTIVE` 還是 `BATCH`。

### 查看載入工作記錄

下列範例會列出為指定專案提交批次載入工作的所有使用者或服務帳戶。由於未指定時間界線，這項查詢會掃描所有可用的記錄。

```
SELECT
  user_email AS user,
  COUNT(*) num_jobs
FROM
  `region-REGION_NAME`.INFORMATION_SCHEMA.JOBS
WHERE
  job_type = 'LOAD'
GROUP BY
  user_email;
```

**注意：** `INFORMATION_SCHEMA` 檢視表名稱會區分大小寫。

結果大致如下：

```
+--------------+
| user         |
+--------------+
| abc@xyz.com  |
| xyz@xyz.com  |
| bob@xyz.com  |
+--------------+
```

### 取得載入工作數量，判斷每日工作配額用量

以下範例會依據日期、資料集和資料表傳回工作數量，方便您判斷每日工作配額的使用量。

```
SELECT
    DATE(creation_time) as day,
    destination_table.project_id as project_id,
    destination_table.dataset_id as dataset_id,
    destination_table
```