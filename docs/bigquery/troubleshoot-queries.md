Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 排解查詢問題

本文旨在協助您排解與執行查詢相關的常見問題，例如找出查詢速度緩慢的原因，或是針對查詢失敗時傳回的常見錯誤提供解決步驟。

## 排解查詢速度緩慢的問題

如要排解查詢效能緩慢的問題，請按照下列步驟操作：

* 查看「[Google Cloud Service Health](https://status.cloud.google.com/?hl=zh-tw)」頁面，瞭解可能影響查詢效能的已知 BigQuery 服務中斷情形。
* 在[管理工作探索工具](https://docs.cloud.google.com/bigquery/docs/admin-jobs-explorer?hl=zh-tw)中查看查詢的工作時間軸，瞭解查詢各階段的執行時間。

  + 如果大部分經過的時間都是因為建立時間過長，請[與 Cloud Customer Care 團隊聯絡](https://docs.cloud.google.com/support?hl=zh-tw)以尋求協助。
  + 如果大部分經過的時間都是因為執行時間過長，請查看[查詢效能深入分析](https://docs.cloud.google.com/bigquery/docs/query-insights?hl=zh-tw)。查詢效能洞察功能會通知您查詢的執行時間是否長於平均執行時間，並提供可能原因。可能原因包括查詢時段爭用或重組配額不足。如要進一步瞭解各項查詢效能問題和可能的解決方法，請參閱「[解讀查詢效能洞察](https://docs.cloud.google.com/bigquery/docs/query-insights?hl=zh-tw#interpret_query_performance_insights)」。
* 請檢查查詢工作的 [`JobStatistics`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#JobStatistics) 物件類型中的 `finalExecutionDurationMs` 欄位。查詢可能已重試。`finalExecutionDurationMs` 欄位包含這項工作最後一次嘗試執行的時間長度 (以毫秒為單位)。
* 查看[查詢工作詳細資料頁面](https://docs.cloud.google.com/bigquery/docs/managing-jobs?hl=zh-tw#view-job)中處理的位元組數，確認是否高於預期。方法是比較目前查詢處理的位元組數，以及在可接受時間內完成的另一個查詢工作。如果兩個查詢處理的位元組有顯著差異，可能是因為資料量過大，導致查詢速度緩慢。如要瞭解如何最佳化查詢來處理大量資料，請參閱「[最佳化查詢運算](https://docs.cloud.google.com/bigquery/docs/best-practices-performance-compute?hl=zh-tw)」一文。

  您也可以使用 [`INFORMATION_SCHEMA.JOBS` 檢視畫面](https://docs.cloud.google.com/bigquery/docs/information-schema-jobs?hl=zh-tw#most_expensive_queries_by_project)搜尋費用最高的查詢，找出專案中處理大量資料的查詢。
* 查看預留項目用量，並檢查運算單元爭用情形。詳情請參閱「[工作負載統計資料分析](#workload-statistics-analysis)」。
* 檢查先前和最近執行的相同查詢雜湊，查看較慢的工作是否有新的[查詢成效洞察](https://docs.cloud.google.com/bigquery/docs/query-insights?hl=zh-tw)，例如資料輸入規模的變化。您可以在[管理工作探索器](https://docs.cloud.google.com/bigquery/docs/admin-jobs-explorer?hl=zh-tw#filter-jobs)中，依查詢雜湊進行篩選。

### 比較同一項查詢的執行速度緩慢和快速的情況

如果查詢先前執行速度很快，現在卻變慢，請檢查 [Job API 物件](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw)輸出內容，找出執行作業的變化。

#### 快取命中

查看 [`cacheHit`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#jobstatistics2) 值，確認工作快速執行是否為快取命中。如果值為 `true`，表示查詢是快速執行，且查詢使用[快取結果](https://docs.cloud.google.com/bigquery/docs/cached-results?hl=zh-tw)，而非執行查詢。

如果預期緩慢的作業會使用快取結果，請調查查詢[不再使用快取結果](https://docs.cloud.google.com/bigquery/docs/cached-results?hl=zh-tw#cache-exceptions)的原因。如果您不希望查詢作業從快取擷取資料，請尋找未命中快取的快速查詢執行範例，以利進行調查。

#### 配額延遲

如要判斷速度變慢是否是由任何配額延期所致，請檢查這兩項工作的 [`quotaDeferments` 欄位](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#jobstatistics)。比較這些值，判斷較慢的查詢是否因配額延期而延遲開始時間，但較快的作業並未受到影響。

#### 執行作業時間長度

如要瞭解這兩項作業最後一次嘗試的執行時間差異，請比較 [`finalExecutionDurationMs` 欄位的值](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#jobstatistics2)。

如果 `finalExecutionDurationMs` 的值非常相似，但兩個查詢之間的實際執行時間差異 (計算方式為 [`startTime - endTime`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#jobstatistics)) 卻大得多，表示可能發生暫時性問題，導致系統內部重試執行緩慢的工作。如果反覆出現這種差異模式，請[與 Cloud Customer Care 團隊聯絡](https://docs.cloud.google.com/support?hl=zh-tw)，尋求協助

#### 處理的位元組數

查看[查詢工作詳細資料頁面](https://docs.cloud.google.com/bigquery/docs/managing-jobs?hl=zh-tw#view-job)中處理的位元組，或查看 [JobStatistics](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#jobstatistics) 中的 `totalBytesProcessed`，確認是否高於預期。如果兩項查詢處理的位元組數差異很大，則查詢速度可能會因處理的資料量變化而變慢。如要瞭解如何最佳化查詢來處理大量資料，請參閱「[最佳化查詢運算](https://docs.cloud.google.com/bigquery/docs/best-practices-performance-compute?hl=zh-tw)」。
下列原因可能導致查詢處理的位元組數增加：

* 查詢參照的資料表大小增加。
* 查詢現在會讀取資料表較大的分區。
* 查詢參照的檢視區塊定義已變更。

#### 參照資料表

分析 [`JobStatistics2`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#jobstatistics2) 中的 `referencedTables` 欄位輸出內容，檢查查詢是否讀取相同的資料表。參考資料表中的差異可由下列原因說明：

* SQL 查詢已修改為讀取不同資料表。比較查詢文字以確認。
* 查詢執行期間，檢視定義有所變更。檢查這項查詢中參照的檢視區塊定義，並視需要[更新](https://docs.cloud.google.com/bigquery/docs/managing-views?hl=zh-tw)。

參考表格的差異可能說明 [`totalBytesProcessed`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#jobstatistics) 的變化。

#### Materialized view 用量

如果查詢參照任何[具體化檢視區塊](https://docs.cloud.google.com/bigquery/docs/materialized-views-intro?hl=zh-tw)，查詢執行期間選擇或拒絕具體化檢視區塊，可能會導致效能差異。檢查 [`MaterializedViewStatistics`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#materializedviewstatistics)，瞭解慢速查詢是否拒絕使用快速查詢中的任何具體化檢視區塊。查看 [`MaterializedView` 物件中的 `chosen` 和 `rejectedReason` 欄位](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#materializedview)。

#### 中繼資料快取統計資料

如果查詢涉及 Amazon S3 BigLake 資料表或已啟用中繼資料快取的 Cloud Storage BigLake 資料表，請比較 [`MetadataCacheStatistics`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#metadatacachestatistics) 的輸出內容，檢查慢速和快速查詢之間的中繼資料快取用量是否有差異，以及對應的原因。舉例來說，中繼資料快取可能位於資料表的 `maxStaleness` 視窗外。

#### 比較 BigQuery BI Engine 統計資料

如果查詢使用 BigQuery BI Engine，請分析 [`BiEngineStatistics`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#bienginestatistics) 的輸出內容，判斷慢速和快速查詢是否套用相同的加速模式。查看 [`BiEngineReason`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#bienginereason) 欄位，瞭解部分加速或完全未加速的高階原因，例如記憶體不足、缺少預留項目或輸入內容過大。

#### 查看查詢成效洞察資料的差異

在 Google Cloud 控制台或 [`StagePerformanceStandaloneInsight`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#stageperformancestandaloneinsight) 物件中查看「執行圖」，比較各項查詢的[查詢效能洞察](https://docs.cloud.google.com/bigquery/docs/query-insights?hl=zh-tw)，瞭解下列可能問題：

* 運算單元爭用情況 ([`slotContention`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#stageperformancestandaloneinsight))
* 高基數聯結 ([`highCardinalityJoins`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#highcardinalityjoin))
* 重組配額不足 ([`insufficientShuffleQuota`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#stageperformancestandaloneinsight))
* 資料偏斜 ([`partitionSkew`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#PartitionSkew))

請注意慢速工作提供的洞察資料，以及快速工作產生的洞察資料之間的差異，找出影響效能的階段變化。

#### 預留項目指派

檢查指派給這兩項工作的預訂項目是否有差異。變更預訂或從隨選方案改為預訂方案，可能會影響效能。詳情請參閱「[工作負載管理模型和預訂大小](#workload-management-models-and-reservation-size)」。

如要更徹底地分析工作執行中繼資料，請比較這兩項工作的 [`ExplainQueryStage`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#explainquerystage) 物件，逐一檢查查詢執行的各個階段。

如要開始使用，請參閱「[解讀查詢階段資訊](https://docs.cloud.google.com/bigquery/docs/query-insights?hl=zh-tw#interpret_query_stage_information)」一節所述的 `Wait ms` 和 `Shuffle output bytes` 指標。

#### 「`INFORMATION_SCHEMA.JOBS`」檢視畫面中的資源警告

查詢 [`INFORMATION_SCHEMA.JOBS` 檢視區塊](https://docs.cloud.google.com/bigquery/docs/information-schema-jobs?hl=zh-tw)的 `query_info.resource_warning` 欄位，查看 BigQuery 分析的警告與所用資源是否有差異。

### 工作負載統計資料分析

可用運算單元資源和運算單元爭用情況可能會影響查詢執行時間。
以下各節有助於瞭解特定查詢執行作業的時段用量和可用性。

#### 每秒平均運算單元數

如要計算查詢每毫秒使用的平均運算單元數，請將這項工作的運算單元毫秒值 ([`JobStatistics2`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#jobstatistics2) 中的 `totalSlotMs`) 除以這項工作最後一次嘗試執行的毫秒數 ([`JobStatistics`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#jobstatistics) 中的 `finalExecutionDurationMs`)。

您也可以查詢 `INFORMATION_SCHEMA.JOBS` 檢視畫面，計算[作業每毫秒使用的平均運算單元數](https://docs.cloud.google.com/bigquery/docs/information-schema-jobs?hl=zh-tw#average_number_of_slots_per_millisecond_used_by_a_job)

如果工作執行的工作量相似，但每秒的平均時段數較多，完成速度就會更快。每秒平均運算單元用量偏低的原因可能如下：

* 由於不同工作之間發生資源爭用，因此沒有額外資源可用，預訂量已達上限。
* 在執行作業的大部分時間，這項工作並未要求更多時段。舉例來說，如果資料偏斜，就可能發生這種情況。

#### 工作負載管理模型和預訂大小

如果您使用隨選計費模式，每個專案可用的運算單元數量有限。此外，如果在特定位置對隨選容量有大量爭用，則專案可用運算單元數量有時可能會較少。

容量型模式更具可預測性，可讓您指定已確認的基準運算單元數量。

比較使用隨選與預留項目執行的查詢時，請將這些差異納入考量。

建議[使用預留項目](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw)，確保查詢執行效能穩定且可預測。如要進一步瞭解隨選和以容量為準工作負載之間的差異，請參閱「[工作負載管理簡介](https://docs.cloud.google.com/bigquery/docs/reservations-intro?hl=zh-tw)」。

#### 並行工作數量

工作並行數代表查詢執行期間，工作之間對運算單元資源的競爭。工作並行程度越高，工作執行速度通常會越慢，因為工作可用的運算單元較少。

您可以查詢 `INFORMATION_SCHEMA.JOBS` 檢視畫面，[找出專案中與特定查詢同時執行的平均並行工作數](https://docs.cloud.google.com/bigquery/docs/information-schema-jobs?hl=zh-tw#view_average_concurrent_jobs_running_alongside_a_particular_job_in_the_same_project)。

如果預訂方案已指派多個專案，請修改查詢，改用 `JOBS_BY_ORGANIZATION` 而非 `JOBS_BY_PROJECT`，以取得準確的預訂方案層級資料。

如果工作執行緩慢時的平均並行數高於工作執行快速時的平均並行數，就會導致整體速度變慢。

請考慮在專案或預訂中減少並行作業，方法是在預訂或專案中分散資源密集型查詢，或分散到不同的預訂或專案。

另一個解決方案是購買預留容量，或增加現有預留容量的大小。建議允許預留項目[使用閒置運算單元](https://docs.cloud.google.com/bigquery/docs/reservations-tasks?hl=zh-tw#configure_whether_queries_use_idle_slots)。

如要瞭解要新增多少運算單元，請參閱[估算運算單元容量需求](https://docs.cloud.google.com/bigquery/docs/slot-estimator?hl=zh-tw)。

如果預留項目指派給多個專案，則在平均工作並行數相同的情況下，工作可能會因執行專案而獲得不同的運算單元指派結果。詳情請參閱[公平排程](https://docs.cloud.google.com/bigquery/docs/slots?hl=zh-tw#fair_scheduling_in_bigquery)的說明。

#### 預留項目使用率

[管理員資源圖表](https://docs.cloud.google.com/bigquery/docs/admin-resource-charts?hl=zh-tw)和 [BigQuery Cloud Monitoring](https://docs.cloud.google.com/bigquery/docs/monitoring-dashboard?hl=zh-tw) 可用於監控預留項目使用率。詳情請參閱「[監控 BigQuery 預留項目](https://docs.cloud.google.com/bigquery/docs/reservations-monitoring?hl=zh-tw)」。

如要瞭解工作是否要求任何額外時段，請查看「預估可執行的單位」指標，該指標位於 Job API 回應中，或 `period_estimated_runnable_units` 位於 [`INFORMATION_SCHEMA.JOBS_TIMELINE` 檢視畫面](https://docs.cloud.google.com/bigquery/docs/information-schema-jobs-timeline?hl=zh-tw)。[`estimatedRunnableUnits`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#querytimelinesample)如果這項指標的值大於 0，表示該工作當時可能需要更多時段。如要估算工作執行時間的百分比，瞭解工作是否能從額外時段獲益，請對 [`INFORMATION_SCHEMA.JOBS_TIMELINE` 檢視區塊](https://docs.cloud.google.com/bigquery/docs/information-schema-jobs-timeline?hl=zh-tw)執行下列查詢：

```
SELECT
  ROUND(COUNTIF(period_estimated_runnable_units > 0) / COUNT(*) * 100, 1) AS execution_duration_percentage
FROM `myproject`.`region-us`.INFORMATION_SCHEMA.JOBS_TIMELINE
WHERE job_id = 'my_job_id'
GROUP BY job_id;
```

結果大致如下：

```
+---------------------------------+
|   execution_duration_percentage |
+---------------------------------+
|                            96.7 |
+---------------------------------+
```

百分比較低表示在這個情境中，查詢速度緩慢的主要原因並非是可用的時段資源不足。

如果百分比偏高，且預訂在此期間未充分運用，請[與 Cloud Customer Care 聯絡](https://docs.cloud.google.com/support?hl=zh-tw)以進行調查。

如果預留項目在工作執行緩慢期間已完全用盡，且百分比偏高，表示工作受到資源限制。請考慮減少並行數、增加預留項目大小、允許預留項目使用閒置運算單元，或在工作以隨選模式執行時購買預留項目。

### 工作的中繼資料和工作負載分析結果不確定

如果還是找不到原因，請[與 Cloud Customer Care 聯絡](https://docs.cloud.google.com/support?hl=zh-tw)，尋求協助。

## 使用 Gemini Cloud Assist 排解查詢失敗問題

如要使用 Gemini Cloud Assist [找出查詢失敗的原因](https://docs.cloud.google.com/bigquery/docs/use-cloud-assist?hl=zh-tw#analyze_jobs)，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在 Google Cloud 工具列，點選 spark「開啟或關閉 Gemini Cloud Assist 對話」。
3. 在「Cloud Assist」面板中輸入提示，並加入工作 ID，例如 `Why did JOB_ID fail?`

## 使用 `gcpdiag` 排解查詢失敗問題

[`gcpdiag`](https://gcpdiag.dev)
是開放原始碼工具。這並非正式支援的 Google Cloud 產品。
您可以使用 `gcpdiag` 工具找出並修正 Google Cloud專案問題。詳情請參閱 [GitHub 上的 gcpdiag 專案](https://github.com/GoogleCloudPlatform/gcpdiag/#gcpdiag---diagnostics-for-google-cloud-platform)。

[`gcpdiag`](https://gcpdiag.dev/) 工具可協助您分析失敗的 BigQuery 查詢，瞭解特定失敗是否有已知的根本原因和解決方法。

### 執行 `gcpdiag` 指令

您可以從 Google Cloud CLI 執行 `gcpdiag` 指令：

## Google Cloud 控制台

1. 完成下列指令，然後複製。

```
gcpdiag runbook bigquery/failed-query \
   --parameter project_id=PROJECT_ID \
   --parameter bigquery_job_region=JOB_REGION \
   --parameter bigquery_job_id=JOB_ID \
   --parameter bigquery_skip_permission_check=SKIP_PERMISSION_CHECK
```

2. 開啟 Google Cloud 控制台並啟用 Cloud Shell。
[開啟 Cloud 控制台](https://console.cloud.google.com/bigquery?cloudshell=true&hl=zh-tw)3. 貼上複製的指令。
4. 執行 `gcpdiag` 指令，下載 `gcpdiag` Docker 映像檔，然後執行診斷檢查。如適用，請按照輸出內容中的操作說明修正檢查失敗的問題。

## Docker

您可以使用啟動 [Docker](https://www.docker.com/) 容器中 `gcpdiag` 的 wrapper [執行 `gcpdiag`](https://github.com/GoogleCloudPlatform/gcpdiag?tab=readme-ov-file#installation)。必須安裝 Docker 或 [Podman](https://podman.io/)。

1. 在本機工作站上複製並執行下列指令。

   ```
   curl https://gcpdiag.dev/gcpdiag.sh >gcpdiag && chmod +x gcpdiag
   ```
2. 執行 `gcpdiag` 指令。

   ```
   ./gcpdiag runbook bigquery/failed-query \
      --parameter project_id=PROJECT_ID \
      --parameter bigquery_job_region=JOB_REGION \
      --parameter bigquery_job_id=JOB_ID \
      --parameter bigquery_skip_permission_check=SKIP_PERMISSION_CHECK
   ```

查看這本 Runbook 的[可用參數](https://gcpdiag.dev/runbook/diagnostic-trees/bigquery/failed-query/#parameters)。

更改下列內容：

* PROJECT\_ID：包含資源的專案 ID。
* JOB\_REGION：執行 BigQuery 作業的區域。
* JOB\_ID：BigQuery 工作的作業 ID。
* SKIP\_PERMISSION\_CHECK：(選用) 如要略過相關權限檢查並加快 Runbook 執行速度，請將此值設為 `True` (預設值為 `False`)。

實用旗標：

* `--universe-domain`：如果適用，則為代管資源的[信任合作夥伴 Sovereign Cloud](https://cloud.google.com/blog/products/identity-security/new-sovereign-controls-for-gcp-via-assured-workloads?hl=zh-tw)網域
* `--parameter` 或 `-p`：Runbook 參數

如需所有 `gcpdiag` 工具旗標的清單和說明，請參閱 [`gcpdiag` 使用說明](https://github.com/GoogleCloudPlatform/gcpdiag?tab=readme-ov-file#usage)。

## Avro 結構定義解析

錯誤字串：`Cannot skip stream`

載入具有不同結構定義的多個 Avro 檔案時，可能會發生這個錯誤，導致結構定義解析問題，並造成匯入工作在隨機檔案中失敗。

如要解決這項錯誤，請確認載入作業中最後一個依字母順序排列的檔案，包含不同結構定義的超集 (聯集)。這是根據 [Avro 處理結構定義解析的方式](https://avro.apache.org/docs/1.8.1/spec.html#Schema+Resolution)所做的規定。

## 並行查詢發生衝突

錯誤字串：`Concurrent jobs in the same session are not allowed`

如果工作階段中同時執行多項查詢 (不支援此做法)，就可能發生這項錯誤。請參閱工作階段[限制](https://docs.cloud.google.com/bigquery/docs/sessions-intro?hl=zh-tw#limitations)。

## DML 陳述式衝突

錯誤字串：`Could not serialize access to table due to concurrent update`

如果對同一資料表執行的資料操縱語言 (DML) 陳述式發生衝突，或是資料表在 DML 陳述式變異期間遭到截斷，就可能發生這項錯誤。詳情請參閱「[DML 陳述式衝突](https://docs.cloud.google.com/bigquery/docs/data-manipulation-language?hl=zh-tw#dml_statement_conflicts)」。

如要解決這個錯誤，請執行影響單一資料表的 DML 作業，確保作業不會重疊。

## 相互關聯的子查詢

錯誤字串：`Correlated subqueries that reference other tables are not
supported unless they can be de-correlated`

如果查詢包含參照子查詢外部資料欄的子查詢 (稱為「關聯」資料欄)，就可能發生這個錯誤。系統會使用效率不彰的巢狀執行策略評估相關子查詢，也就是針對產生相關資料欄的外部查詢中每個資料列，評估子查詢。有時 BigQuery 會在內部改寫含有相關子查詢的查詢，以便更有效率地執行查詢。如果 BigQuery 無法充分最佳化查詢，就會發生相關子查詢錯誤。

如要解決這項錯誤，請嘗試下列做法：

* 從子查詢中移除所有 `ORDER BY`、`LIMIT`、`EXISTS`、`NOT EXISTS` 或 `IN` 子句。
* 使用[多重陳述式查詢](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/procedural-language?hl=zh-tw)建立臨時資料表，以供子查詢參照。
* 請重新撰寫查詢，改為使用 `CROSS JOIN`。

## 資料欄層級存取控管權限不足

錯誤字串：

* `Access denied: Requires fineGrainedGet permission on the read columns to
  execute the DML statements`
* `Access denied: User does not have permission to access policy tag
  projects/PROJECT\_ID/locations/LOCATION/taxonomies/TAXONOMY\_ID/policyTags/POLICY\_TAG\_ID
  on column PROJECT\_ID.DATASET.TABLE.COLUMN.'

如果您嘗試執行 SQL 查詢或 DML `DELETE`、`UPDATE` 或 `MERGE` 陳述式，但未獲授與使用資料欄層級存取控管的資料欄 [Fine-Grained Reader](https://docs.cloud.google.com/bigquery/docs/column-level-security?hl=zh-tw#fine_grained_reader) 角色，就會發生這些錯誤。設定政策標記時，系統會將這個角色指派給主體。詳情請參閱「[欄層級存取權控管對寫入作業的影響](https://docs.cloud.google.com/bigquery/docs/column-level-security-writes?hl=zh-tw)」。

如要解決這個問題，請修改查詢，排除含有政策標記的資料欄，或授予使用者「精細讀取者」角色。設定政策標記時，系統會將這個角色指派給主體。詳情請參閱「[更新政策標記的權限](https://docs.cloud.google.com/bigquery/docs/column-level-security?hl=zh-tw#update_permission_policy_tags)」。

## 排解已排定查詢的問題

設定或執行排定查詢時，可能會發生下列問題。

### 排程查詢觸發重複的執行作業

系統可能會在排定時間多次觸發排定查詢。
如果查詢排程的時間正好是整點 (例如 09:00)，就比較有可能發生這種情況。
這可能會導致非預期的結果，例如查詢執行 `INSERT` 作業時產生重複資料。

為盡量降低重複執行的風險，請在整點以外的時間安排查詢，例如整點前或後幾分鐘 (例如 08:58 或 09:03)。詳情請參閱「[排定查詢時間](https://docs.cloud.google.com/bigquery/docs/scheduling-queries?hl=zh-tw)」。

### 排定查詢的憑證無效

錯誤字串：

* `Error code: INVALID_USERID`
* `Error code 5: Authentication failure: User Id not found`
* `PERMISSION_DENIED: BigQuery: Permission denied while getting Drive credentials`

如果排定查詢作業因憑證過時而失敗，就可能發生這項錯誤，尤其是查詢 Google 雲端硬碟資料時。

如要解決這項錯誤，請按照下列步驟操作：

* 請確認您已啟用 [BigQuery 資料移轉服務](https://docs.cloud.google.com/bigquery/docs/enable-transfer-service?hl=zh-tw#enable-dts)，這是使用已排定查詢的[必要條件](https://docs.cloud.google.com/bigquery/docs/scheduling-queries?hl=zh-tw#before_you_begin)。
* 更新[排程查詢憑證](https://docs.cloud.google.com/bigquery/docs/scheduling-queries?hl=zh-tw#update_scheduled_query_credentials)。

### 服務帳戶憑證無效

錯誤字串：`HttpError 403 when requesting returned: The caller does not have permission`

如果您嘗試使用服務帳戶設定排程查詢，可能會看到這則錯誤訊息。如要解決這項錯誤，請參閱「[授權和權限問題](https://docs.cloud.google.com/bigquery/docs/transfer-troubleshooting?hl=zh-tw#authorization_and_permission_issues)」一文中的疑難排解步驟。

## 快照時間無效

錯誤字串：`Invalid snapshot time`

嘗試查詢資料集[時間旅行視窗](https://docs.cloud.google.com/bigquery/docs/time-travel?hl=zh-tw)外的歷來資料時，可能會發生這項錯誤。如要修正這項錯誤，請變更查詢，在資料集的時間旅行視窗中存取歷來資料。

如果查詢開始後，查詢中使用的其中一個資料表遭到捨棄並重新建立，也可能會出現這項錯誤。檢查是否有排定的查詢或應用程式執行這項作業，且執行時間與失敗的查詢相同。如果有的話，請嘗試將執行捨棄和重新建立作業的程序移至不會與讀取該資料表的查詢衝突的時間執行。

## 工作已存在

錯誤字串：`Already Exists: Job <job name>`

如果查詢工作必須評估大型陣列，建立查詢工作所需的時間就會比平均時間長，這時就可能發生這項錯誤。舉例來說，具有 `WHERE` 子句的查詢 (例如 `WHERE column IN (<2000+ elements array>)`)。

如要解決這項錯誤，請按照下列步驟操作：

* 允許 BigQuery 產生隨機 [`jobId` 值](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/JobReference?hl=zh-tw)，而非指定值。
* 使用[參數化查詢](https://docs.cloud.google.com/bigquery/docs/parameterized-queries?hl=zh-tw#use_arrays_in_parameterized_queries)載入陣列。

如果您手動設定工作 ID，但工作未在逾時期限內傳回成功，也可能會發生這項錯誤。在這種情況下，您可以新增例外狀況處理常式，檢查工作是否存在。如果有的話，您就可以從該工作提取查詢結果。

## 找不到所需工作

錯誤字串：`Job not found`

如果對 [`getQueryResults` 呼叫](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs/getQueryResults?hl=zh-tw)的回應中，`location` 欄位未指定任何值，就會發生這項錯誤。如果是這種情況，請再次嘗試呼叫，並提供 `location` 值。

詳情請參閱「[避免多次評估相同的通用資料表運算式 (CTE)](https://docs.cloud.google.com/bigquery/docs/best-practices-performance-compute?hl=zh-tw#avoid_multiple_evaluations_of_the_same_ctes)」。

## 找不到所在位置

錯誤字串：`Dataset [project_id]:[dataset_id] was not found in location [region]`

當您參照不存在的資料集資源，或要求中的位置與資料集的位置不符時，系統就會傳回這個錯誤。

如要解決這個問題，請在查詢中指定資料集位置，或確認資料集位於相同位置。

## 查詢超過執行時間限制

錯誤字串：`Query fails due to reaching the execution time limit`

如果查詢達到[查詢執行時間限制](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#query_jobs)，請查詢 [`INFORMATION_SCHEMA.JOBS` 檢視區塊](https://docs.cloud.google.com/bigquery/docs/information-schema-jobs?hl=zh-tw)，瞭解先前執行查詢的執行時間，查詢內容類似於下列範例：

```
SELECT TIMESTAMP_DIFF(end_time, start_time, SECOND) AS runtime_in_seconds
FROM `region-us`.INFORMATION_SCHEMA.JOBS
WHERE statement_type = 'QUERY'
AND query = "my query string";
```

如果先前執行查詢的時間明顯較短，請使用[查詢效能深入分析](https://docs.cloud.google.com/bigquery/docs/query-insights?hl=zh-tw)找出並解決根本問題。

## 查詢回應過大

錯誤字串：`responseTooLarge`

當查詢的結果超出[回應大小上限](https://docs.cloud.google.com/bigquery/quota-policy?hl=zh-tw#query_jobs)時，系統就會傳回這個錯誤。

如要解決這個錯誤，請參閱[錯誤表格](https://docs.cloud.google.com/bigquery/docs/error-messages?hl=zh-tw#errortable)中 `responseTooLarge` 錯誤訊息的指引。

## 找不到預訂項目或缺少運算單元

錯誤字串：`Cannot run query: project does not have the reservation in the data region or no slots are configured`

如果指派給查詢區域中專案的預留項目沒有任何指派的時段，就會發生這個錯誤。您可以將配額新增至預留項目、允許預留項目使用閒置配額、使用其他預留項目，或是移除指派項目並視需要執行查詢。

## 找不到資料表

錯誤字串：`Not found: Table [project_id]:[dataset].[table_name] was not found in location [region]`

如果您指定的資料集或區域中找不到查詢中的資料表，就會發生這個錯誤。如要解決這項錯誤，請按照下列步驟操作：

* 確認查詢包含正確的專案、資料集和資料表名稱。
* 確認資料表位於您執行查詢的區域。
* 請確認在執行作業期間，資料表未遭捨棄並重新建立。否則，不完整的中繼資料傳播可能會導致這個錯誤。

## DML 陳述式過多

錯誤字串：`Too many DML statements outstanding against <table-name>, limit is 20`

如果單一資料表佇列中處於 `PENDING` 狀態的 DML 陳述式超過 [20 個](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#data-manipulation-language-statements)，就會發生這項錯誤。如果您提交 DML 工作至單一資料表的速度，比 BigQuery 的處理速度快，通常就會發生這個錯誤。

其中一個可能的解決方法是將多個較小的 DML 作業分組，變成較大但數量較少的工作，例如批次更新和插入。將較小的工作分組為較大的工作時，執行較大工作的成本會攤銷，執行速度也會更快。合併影響相同資料的 DML 陳述式通常可提高 DML 工作效率，且較不可能超出佇列大小配額限制。如要進一步瞭解如何最佳化 DML 作業，請參閱「[避免使用更新或插入單列的 DML 陳述式](https://docs.cloud.google.com/bigquery/docs/best-practices-performance-compute?hl=zh-tw#avoid-dml-update-single-rows)」。

如要提高 DML 效率，也可以將資料表分區或分群。詳情請參閱「[最佳做法](https://docs.cloud.google.com/bigquery/docs/data-manipulation-language?hl=zh-tw#best_practices)」。

## 錯誤 403：超過配額

錯誤字串：`403 Quota exceeded: Your table exceeded quota for total number of
DML jobs writing to a table, pending + running.`

系統會為每個資料表將 UPDATE、DELETE 和 MERGE 等變動 DML 陳述式排入佇列，佇列長度上限為 20。如果資料表已有 20 個處於待處理或執行中的工作，您又提交額外的變異 DML 陳述式，就會發生這項錯誤。如要解決這項錯誤，請按照下列步驟操作：

* *增加預留運算單元數量*：增加預留運算單元數量，有助於加快工作完成速度並減少工作並行數。這樣可減少佇列中待處理的工作數量，並避免達到上限。
* *最佳化工作流程自動調度*：在自動調度工具中限制並行 DML 工作數量，確保針對同一資料表執行的變更陳述式不超過 20 個。
* *批次 DML 作業*：將多個較小的 DML 陳述式合併為較少、較大的陳述式，以減少針對資料表排隊的作業總數。

## 並行更新導致交易中止

錯誤字串：`Transaction is aborted due to concurrent update against table [table_name]`

如果兩個不同的變動 DML 陳述式嘗試同時更新相同資料表，就會發生這項錯誤。舉例來說，假設您在某個工作階段中啟動[交易](https://docs.cloud.google.com/bigquery/docs/transactions?hl=zh-tw)，該工作階段包含變動 DML 陳述式，後面接著發生錯誤。如果沒有例外狀況處理常式，BigQuery 會在工作階段結束時自動回溯交易，最多需要 24 小時。在此期間，其他嘗試對資料表執行變動 DML 陳述式的行為都會失敗。

如要解決這項錯誤，請[列出有效工作階段](https://docs.cloud.google.com/bigquery/docs/sessions?hl=zh-tw#list-sessions)，並檢查是否有任何工作階段包含狀態為 `ERROR` 的查詢工作，該工作在資料表上執行了變動 DML 陳述式。然後終止該工作階段。

## 錯誤 412：工作參照的資料表屬於容錯移轉資料集

錯誤字串：`Error 412: The job references a table that belongs to a failover dataset in the ... region (PROJECT_ID:DATASET_ID). However, only jobs that run on a reservation with the "ENTERPRISE_PLUS" edition can modify or write to failover datasets. Please also make sure that the job that is writing to the failover dataset is running in the current primary location.`

這表示工作並非在 BigQuery Enterprise Plus 版本下執行，或工作執行的區域並非容錯移轉資料集的主要位置。詳情請參閱[受管理災難復原](https://docs.cloud.google.com/bigquery/docs/managed-disaster-recovery?hl=zh-tw)。

## 使用快取的結果時，載入檢視畫面發生錯誤

錯誤字串：`BigQuery data export: There was an error loading this view. IAM
setPolicy failed for Dataset <PROJECT_ID>. One or more users named in the policy
do not belong to a permitted customer.`

這項錯誤表示您的 Google Workspace 客戶 ID 尚未在貴機構政策限制中獲得存取權。如要瞭解如何使用 `iam.allowedPolicyMemberDomains` 限制條件，請參閱「[使用 `iam.allowedPolicyMemberDomains` 限制條件實作網域限定共用](https://docs.cloud.google.com/organization-policy/restrict-domains?hl=zh-tw#predefined-constraint)」。

## 舊版 SQL 錯誤

使用舊版 SQL 時，可能會發生下列錯誤。

### `Cannot be queried with legacy SQL`

錯誤字串：`cannot be queried with legacy SQL. Please consider switching to standard SQL`

這個錯誤可能在下列兩種情況中發生：

* 查詢是以標準 SQL 編寫，但已提供明確使用舊版 SQL 的選項。請務必按照[公開說明文件](https://docs.cloud.google.com/bigquery/docs/introduction-sql?hl=zh-tw#bigquery-sql-dialects)的指示，使用標準 SQL 執行查詢，例如使用 bq 指令列工具提供 `--use_legacy_sql=false`。
* 您嘗試使用舊版 SQL 查詢具有排序規則的資料表，但[不支援](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/collation-concepts?hl=zh-tw)這項操作。

### 無法使用舊版 SQL 查詢重新命名資料欄的資料表

錯誤字串：`Table project:dataset.table with renamed columns cannot be queried with legacy SQL. Please consider switching to standard SQL or dropping column my_column`

如果您使用舊版 SQL 查詢含有更名資料欄的資料表，就會發生這個錯誤。請改用[標準 SQL](https://docs.cloud.google.com/bigquery/docs/introduction-sql?hl=zh-tw#bigquery-sql-dialects)。

## 使用者沒有權限

錯誤字串：

* `Access Denied: Project [project_id]: User does not have bigquery.jobs.create
  permission in project [project_id].`
* `User does not have permission to query table project-id:dataset.table.`
* `Access Denied: User does not have permission to query table or perhaps it
  does not exist.`

如果您在執行查詢的專案中沒有 `bigquery.jobs.create` 權限，無論您在含有資料的專案中擁有何種權限，都可能發生這些錯誤。

如果服務帳戶、使用者或群組在查詢參照的所有表格和檢視區塊中，沒有 `bigquery.tables.getData` 權限，也可能會收到這些錯誤。如要進一步瞭解執行查詢所需的權限，請參閱「[必要角色](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#required_permissions)」。

如果查詢的區域中沒有資料表 (例如 `asia-south1`)，也可能會發生這類錯誤。您可以檢查[資料集位置](https://docs.cloud.google.com/bigquery/docs/datasets-intro?hl=zh-tw#dataset_location)來確認區域。

解決這些錯誤時，請注意下列事項：

* *服務帳戶*：服務帳戶必須具備執行所在專案的 `bigquery.jobs.create` 權限，以及查詢參照的所有資料表和檢視區塊的 `bigquery.tables.getData` 權限。
* *自訂角色*：自訂 IAM 角色必須在相關角色中明確包含 `bigquery.jobs.create` 權限，且必須對查詢參照的所有資料表和檢視區塊具有 `bigquery.tables.getData` 權限。
* *共用資料集*：在其他專案中使用共用資料集時，您可能仍需具備專案的 `bigquery.jobs.create` 權限，才能在該資料集中執行查詢或工作。

如要授予資料表或檢視表的存取權，請參閱「[授予資料表或檢視表的存取權](https://docs.cloud.google.com/bigquery/docs/control-access-to-resources-iam?hl=zh-tw#grant_access_to_a_table_or_view)」。

**注意：** 如果使用者帳戶或服務帳戶受到拒絕政策影響，即使帳戶具有正確權限，您仍可能會收到 `Access denied` 錯誤。詳情請參閱「[拒絕政策](https://docs.cloud.google.com/iam/docs/deny-overview?hl=zh-tw)」。

### 預訂的權限 `bigquery.reservations.use` 遭拒

錯誤字串：

* `Access Denied: Reservation projects/project/locations/region/reservations/reservation_name: Permission bigquery.reservations.use denied on reservation projects/project/locations/region/reservations/reservation_name (or it may not exist)`

如果使用 `SET @@reservation` 陳述式將查詢指派至特定預留位置執行，但使用者或服務帳戶缺少 `bigquery.reservations.use` 權限，就會發生這個錯誤。您可以在 Cloud Logging 或 BigQuery 工作頁面中檢查失敗情形，找出嘗試執行這項作業的主體。

### 其他 `Access Denied` 錯誤

錯誤字串：

* `Access Denied: Dataset project_id:dataset_id: Permission bigquery.datasets.get denied on dataset project_id:dataset_id (or it may not exist).`
* `Access Denied: Dataset project_id:dataset_id: Permission bigquery.datasets.update denied on dataset project_id:dataset_id (or it may not exist).`
* `Access Denied: BigQuery BigQuery: User does not have permission to access data protected by policy tag`

如要排解 BigQuery 中的一般 `Access Denied` 錯誤，請使用[政策分析工具](https://docs.cloud.google.com/policy-intelligence/docs/analyze-iam-policies?hl=zh-tw)[判斷主體對資源的存取權](https://docs.cloud.google.com/policy-intelligence/docs/analyze-iam-policies?hl=zh-tw#access-query)。

在政策分析工具中，提供您嘗試存取的 BigQuery 資源 (例如 `//bigquery.googleapis.com/projects/YOUR_PROJECT/datasets/YOUR_DATASET/tables/YOUR_TABLE`)，以及收到 `Access Denied` 錯誤的使用者或服務帳戶的電子郵件地址做為主體。分析結果會顯示資源的主體權限，您可以與錯誤訊息中缺少的權限進行比較。

## 指令碼不支援目的地加密

錯誤字串：`configuration.query.destinationEncryptionConfiguration cannot be set for scripts`

嘗試為 BigQuery 指令碼工作設定目的地加密設定時，會發生這個錯誤，因為[不支援](https://docs.cloud.google.com/bigquery/docs/customer-managed-encryption?hl=zh-tw#script-limitations)這項操作。

## 存取權遭機構政策拒絕

錯誤字串：
`IAM setPolicy failed for Dataset DATASET: Operation
denied by org policy on resource.`

如果機構政策禁止主體查詢 BigQuery 資源，就會發生這個錯誤。[機構政策服務](https://docs.cloud.google.com/resource-manager/docs/organization-policy/overview?hl=zh-tw)可讓您在整個機構階層中，對[支援的資源](https://docs.cloud.google.com/resource-manager/docs/organization-policy/org-policy-constraints?hl=zh-tw)強制執行限制。

如果主體應有權存取資源，您需要使用可用的 [VPC 疑難排解工具](https://docs.cloud.google.com/vpc/docs/troubleshooting-policy-and-access-problems?hl=zh-tw#troubleshooting_tools)，診斷機構政策的問題。

## 超出資源上限問題

如果 BigQuery 資源不足，無法完成查詢，就會發生下列問題。

### 查詢超出 CPU 資源

錯誤字串：`Query exceeded resource limits`

如果隨選查詢使用的 CPU 相對掃描的資料量過多，就會發生這個錯誤。如要瞭解如何解決這些問題，請參閱「[排解資源超出上限的問題](#ts-resources-exceeded)」。

### 查詢超出記憶體資源

錯誤字串：`Resources exceeded during query execution: The query could not be executed in the allotted memory`

如果是 [`SELECT` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw#select_list)，當查詢使用的資源過多時，就會發生這個錯誤。如要解決這個錯誤，請參閱「[排解資源超出上限的問題](#ts-resources-exceeded)」。

### 堆疊空間不足

錯誤字串：`Out of stack space due to deeply nested query expression during query resolution.`

如果查詢包含過多巢狀函式呼叫，就可能發生這個錯誤。有時，剖析期間會將查詢的部分內容翻譯為函式呼叫。舉例來說，含有重複[串連運算子](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/operators?hl=zh-tw#concatenation_operator)的運算式 (例如 `A || B || C || ...`) 會變成 `CONCAT(A, CONCAT(B, CONCAT(C, ...)))`。

如要修正這項錯誤，請重新編寫查詢，減少巢狀結構的數量。

### 查詢執行期間資源超出上限

錯誤字串：`Resources exceeded during query execution: The query could not be executed in the allotted memory. Peak usage: [percentage]% of limit. Top memory consumer(s): ORDER BY operations.`

這類情況可能會發生在 `ORDER BY ... LIMIT ... OFFSET ...` 查詢中。由於實作細節，排序作業可能會在單一運算單元上進行，如果需要處理的資料列過多，運算單元可能會耗盡記憶體，特別是使用大型 `OFFSET` 時。`LIMIT``OFFSET`

如要解決這項錯誤，請避免在 `ORDER BY` ... `LIMIT` 查詢中使用較大的 `OFFSET` 值。或者，您也可以使用可擴充的 `ROW_NUMBER()` window 函式，根據所選順序指派排名，然後在 `WHERE` 子句中篩選這些排名。例如：

```
SELECT ...
FROM (
  SELECT ROW_NUMBER() OVER (ORDER BY ...) AS rn
  FROM ...
)
WHERE rn > @start_index AND rn <= @page_size + @start_index  -- note that row_number() starts with 1
```

### TensorFlow 工作站記憶體不足

錯誤字串：`Resources exceeded during query execution: TensorFlow worker out
of memory`。

如果模型超出記憶體上限 (通常為 250 MB)，特別是使用 `ML.EXPLAIN_PREDICT` 等耗用大量資源的函式時，就可能觸發這項錯誤。

如要解決這項錯誤，請按照下列步驟操作：

1. *使用 Vertex AI 遠端模型*：如要使用超出記憶體限制的模型，請按照 [部署模型](https://docs.cloud.google.com/vertex-ai/docs/predictions/deploy-model-api?hl=zh-tw)的步驟，使用 Vertex AI SDK for Python 將模型部署至 Vertex AI，然後使用[遠端模型](https://docs.cloud.google.com/bigquery/docs/bigquery-ml-remote-model-tutorial?hl=zh-tw)存取模型。這會將記憶體需求卸載至專屬的 Vertex AI 基礎架構。
2. *最佳化模型*：使用架構簡化、量化或剪枝，減少模型的 RAM 占用空間。
3. *使用較不密集的函式*：如果錯誤發生在 `ML.EXPLAIN_PREDICT` 呼叫期間，請嘗試使用 `ML.PREDICT` 執行工作，判斷模型是否能在沒有可解釋性功能額外負荷的情況下執行。
4. *分析輸入資料大小*：個別資料列過大可能會導致記憶體耗盡。使用下列指令檢查最大資料列的大小：

   ```
   SELECT BYTE_LENGTH(TO_JSON_STRING(t)) AS row_size
   FROM your_table AS t
   ORDER BY row_size DESC
   LIMIT 10
   ```

### 查詢超出隨機播放資源

錯誤字串：`Resources exceeded during query execution: Your project or organization exceeded the maximum disk and memory limit available for shuffle operations`

如果查詢無法存取足夠的重組資源，就會發生這項錯誤。

如要解決這個錯誤，請佈建更多運算單元，或減少查詢處理的資料量。如要進一步瞭解如何解決這個問題，請參閱「[洗牌配額不足](https://docs.cloud.google.com/bigquery/docs/query-insights?hl=zh-tw#insufficient_shuffle_quota)」。

如要進一步瞭解如何解決這些問題，請參閱「[排解資源超出上限的問題](#ts-resources-exceeded)」。

### 查詢過於複雜

錯誤字串：`Resources exceeded during query execution: Not enough resources for query planning - too many subqueries or query is too complex`

如果查詢過於複雜，就會發生這個錯誤。造成複雜度的主要原因如下：

* `WITH` 深度巢狀或重複使用的子句。
* 深度巢狀結構或重複使用的檢視區塊。
* 重複使用 [`UNION ALL` 運算子](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw#union_example)。

如要解決這個錯誤，請嘗試下列方法：

* 將查詢分割為多個查詢，然後使用[程序語言](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/procedural-language?hl=zh-tw)，依序執行這些查詢並共用狀態。
* 請改用暫時性資料表，而非 `WITH` 子句。
* 改寫查詢，減少參照的物件和比較次數。

您可以使用 [`INFORMATION_SCHEMA.JOBS` 檢視區塊](https://docs.cloud.google.com/bigquery/docs/information-schema-jobs?hl=zh-tw)中的 `query_info.resource_warning` 欄位，主動監控即將達到複雜度上限的查詢。下列範例會傳回過去三天內資源用量高的查詢：

```
SELECT
  ANY_VALUE(query) AS query,
  MAX(query_info.resource_warning) AS resource_warning
FROM
  <your_project_id>.`region-us`.INFORMATION_SCHEMA.JOBS
WHERE
  creation_time > TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 3 DAY)
  AND query_info.resource_warning IS NOT NULL
GROUP BY
  query_info.query_hashes.normalized_literals
LIMIT
  1000
```

如要進一步瞭解如何解決這些問題，請參閱「[排解資源超出上限的問題](#ts-resources-exceeded)」。

### 排解超出資源上限的問題

**查詢工作**：

如要最佳化查詢，請嘗試下列步驟：

* 請嘗試移除 `ORDER BY` 子句。
* 如果您的查詢使用 `JOIN`，請確保較大的資料表位於子句的左側。此外，請確認資料中沒有重複的聯結鍵。
* 如果您的查詢使用 `FLATTEN`，請判斷這是否有必要。詳情請參閱[巢狀與重複的資料](https://docs.cloud.google.com/bigquery/docs/data?hl=zh-tw#nested)。
* 如果您的查詢使用 `EXACT_COUNT_DISTINCT`，請考慮改用 [`COUNT(DISTINCT)`](https://docs.cloud.google.com/bigquery/query-reference?hl=zh-tw#countdistinct)。
* 如果您的查詢使用 `COUNT(DISTINCT <value>, <n>)`，並搭配較大的 `<n>` 值，請考慮改用 `GROUP BY`。詳情請參閱「[`COUNT(DISTINCT)`](https://docs.cloud.google.com/bigquery/query-reference?hl=zh-tw#countdistinct)」。
* 如果您的查詢使用 `UNIQUE`，請考慮改用 `GROUP BY`，或是位於 subselect 內部的[window 函式](https://docs.cloud.google.com/bigquery/query-reference?hl=zh-tw#windowfunctions)。
* 如果查詢使用 `LIMIT` 子句具現化許多資料列，請考慮篩選其他資料欄 (例如 `ROW_NUMBER()`)，或完全移除 `LIMIT` 子句，以允許寫入平行化。
* 如果查詢使用深度巢狀檢視區塊和 `WITH` 子句，複雜度可能會呈指數成長，進而達到限制。
* 請改用暫時性資料表，而非 `WITH` 子句。`WITH` 子句可能需要重新計算多次，這會使查詢變得複雜，因此速度較慢。改為將中繼結果保留在臨時資料表中，可降低複雜度。
* 避免使用 `UNION ALL` 查詢。
* 如果查詢使用 `MATCH_RECOGNIZE`，請修改 [`PARTITION BY` 子句](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw#match_recognize_partition_by)，縮小分區大小，或新增 `PARTITION BY` 子句 (如果沒有的話)。

詳情請參閱下列資源：

* [最佳化調整查詢運算](https://docs.cloud.google.com/bigquery/docs/best-practices-performance-compute?hl=zh-tw)。
* [進一步瞭解資源警告](https://docs.cloud.google.com/bigquery/docs/information-schema-jobs?hl=zh-tw#get_details_about_a_resource_warning)
* [監控健康狀態、資源使用率和工作](https://docs.cloud.google.com/bigquery/docs/admin-resource-charts?hl=zh-tw)

**載入工作**：

如果您載入 Avro 或 Parquet 檔案，請縮減檔案中的列大小。請檢查要載入的檔案格式是否有特定大小限制：

* [Avro 輸入檔案規定](https://docs.cloud.google.com/bigquery/docs/loading-data-cloud-storage-avro?hl=zh-tw#input_file_requirements)
* [Parquet 輸入檔案規定](https://docs.cloud.google.com/bigquery/docs/loading-data-cloud-storage-parquet?hl=zh-tw#input_file_requirements)

如果在載入 ORC 檔案時收到這則錯誤訊息，請[與支援團隊聯絡](https://docs.cloud.google.com/support?hl=zh-tw)。

**Storage API：**

錯誤字串：`Stream memory usage exceeded`

在 Storage Read API `ReadRows` 呼叫期間，部分記憶體用量高的串流可能會收到 `RESOURCE_EXHAUSTED` 錯誤，並顯示這則訊息。如果讀取寬資料表或結構定義複雜的資料表，就可能發生這種情況。為解決這個問題，請選取較少的資料欄來讀取 (使用 [`selected_fields` 參數](https://docs.cloud.google.com/bigquery/docs/reference/storage/rpc/google.cloud.bigquery.storage.v1?hl=zh-tw#tablereadoptions))，或是簡化資料表結構定義，藉此縮減結果列大小。

## 排解連線問題

下列各節說明如何排解嘗試與 BigQuery 互動時的連線問題：

### 將 Google DNS 加入允許清單

使用 [Google IP Dig 工具](https://toolbox.googleapps.com/apps/dig/#A/)，將 BigQuery DNS 端點 `bigquery.googleapis.com` 解析為單一「A」記錄 IP。請確認防火牆設定並未封鎖這個 IP 位址。

一般來說，我們建議將 Google DNS 名稱加入允許清單。<https://www.gstatic.com/ipranges/goog.json> 和 <https://www.gstatic.com/ipranges/cloud.json> 檔案中分享的 IP 範圍經常變更，因此建議改為將 Google DNS 名稱加入允許清單。以下是建議加入許可清單的常見 DNS 名稱：

* `*.1e100.net`
* `*.google.com`
* `*.gstatic.com`
* `*.googleapis.com`
* `*.googleusercontent.com`
* `*.appspot.com`
* `*.gvt1.com`

### 找出會捨棄封包的 Proxy 或防火牆

如要找出用戶端和 Google Front End (GFE) 之間的所有封包躍點，請在用戶端電腦上執行 [`traceroute`](https://en.wikipedia.org/wiki/Traceroute) 指令，這項指令會醒目顯示捨棄導向 GFE 封包的伺服器。以下是 `traceroute` 指令範例：

```
traceroute -T -p 443 bigquery.googleapis.com
```

如果問題與特定 IP 位址有關，您也可以找出特定 GFE IP 位址的封包躍點：

```
traceroute -T -p 443 142.250.178.138
```

如果發生 Google 端逾時問題，您會看到要求一路傳送至 GFE。

如果發現封包從未抵達 GFE，請與網路管理員聯絡，以解決這個問題。

### 產生 PCAP 檔案並分析防火牆或 Proxy

產生封包擷取檔案 (PCAP)，並分析該檔案，確保防火牆或 Proxy 不會濾除傳送至 Google IP 的封包，且允許封包傳送至 GFE。

以下是可使用 [`tcpdump`](https://www.tcpdump.org/) 工具執行的指令範例：

```
tcpdump -s 0 -w debug.pcap -K -n host bigquery.googleapis.com
```

### 針對間歇性連線問題設定重試機制

在某些情況下，GFE 負載平衡器可能會捨棄來自用戶端 IP 的連線，例如偵測到 DDoS 流量模式，或是負載平衡器執行個體縮減規模，導致端點 IP 遭到回收。如果 GFE 負載平衡器中斷連線，用戶端必須擷取逾時要求，並對 DNS 端點重試要求。請務必不要使用相同的 IP 位址，直到要求最終成功為止，因為 IP 位址可能已變更。

如果您發現 Google 端持續發生逾時問題，且重試無效，請[與 Cloud Customer Care 團隊聯絡](https://docs.cloud.google.com/support?hl=zh-tw)，並附上透過執行 [tcpdump](https://www.tcpdump.org/) 等封包擷取工具產生的最新 PCAP 檔案。

## 後續步驟

* [取得查詢效能洞察資料](https://docs.cloud.google.com/bigquery/docs/query-insights?hl=zh-tw)。
* 進一步瞭解如何[最佳化查詢效能](https://docs.cloud.google.com/bigquery/docs/best-practices-performance-overview?hl=zh-tw)。
* 查看查詢的[配額與限制](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#query_jobs)。
* 進一步瞭解其他 [BigQuery 錯誤訊息](https://docs.cloud.google.com/bigquery/docs/error-messages?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-14 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-14 (世界標準時間)。"],[],[]]