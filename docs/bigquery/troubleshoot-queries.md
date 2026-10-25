Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 排解查詢相關問題

本文旨在協助您排解執行查詢時的常見問題，例如找出查詢速度緩慢的原因，或提供解決步驟，排除失敗查詢傳回的常見錯誤。

## 排解執行速度緩慢的查詢

如要排解查詢效能緩慢的問題，請按照下列步驟操作：

* 查看 [Google Cloud Service Health](https://status.cloud.google.com/?hl=zh-tw) 頁面，瞭解是否有已知的 BigQuery 服務中斷情形，可能會影響查詢效能。
* 在[工作探索工具](https://docs.cloud.google.com/bigquery/docs/admin-jobs-explorer?hl=zh-tw)中查看查詢的工作時間軸，瞭解查詢各階段的執行時間。

  + 如果大部分時間都花在建立作業上，請[聯絡 Cloud Customer Care](https://docs.cloud.google.com/support?hl=zh-tw) 尋求協助。
  + 如果耗用時間大多是因為執行時間過長，請查看[查詢效能深入分析](https://docs.cloud.google.com/bigquery/docs/query-insights?hl=zh-tw)。查詢效能深入分析會告知您查詢執行時間是否超過平均執行時間，並建議可能的原因。可能原因包括查詢運算單元爭用或重組配額不足。如要進一步瞭解各項查詢效能問題和可能的解決方法，請參閱「[解讀查詢效能深入分析](https://docs.cloud.google.com/bigquery/docs/query-insights?hl=zh-tw#interpret_query_performance_insights)」。
* 請查看查詢工作的 [`JobStatistics`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#JobStatistics) 物件類型中的 `finalExecutionDurationMs` 欄位。系統可能已重試查詢。`finalExecutionDurationMs` 欄位包含這項工作最後一次嘗試執行的時間長度 (以毫秒為單位)。
* 請查看[查詢工作詳細資料頁面](https://docs.cloud.google.com/bigquery/docs/managing-jobs?hl=zh-tw#view-job)中處理的位元組，確認是否高於預期。方法是比較目前查詢處理的位元組數，與在可接受時間內完成的另一項查詢工作。如果兩項查詢處理的位元組數有很大差異，則查詢速度緩慢可能是因為資料量過大。如要瞭解如何最佳化查詢，以便處理大量資料，請參閱「[最佳化查詢運算](https://docs.cloud.google.com/bigquery/docs/best-practices-performance-compute?hl=zh-tw)」。

  您也可以使用 [`INFORMATION_SCHEMA.JOBS` 檢視表](https://docs.cloud.google.com/bigquery/docs/information-schema-jobs?hl=zh-tw#most_expensive_queries_by_project)搜尋最昂貴的查詢，找出專案中處理大量資料的查詢。
* 查看預留項目用量，並檢查是否有運算單元爭用情形。詳情請參閱「[工作負載統計資料分析](#workload-statistics-analysis)」。
* 請檢查相同查詢雜湊的先前和近期執行作業，看看速度較慢的工作是否有新的[查詢效能深入分析](https://docs.cloud.google.com/bigquery/docs/query-insights?hl=zh-tw)，例如資料輸入規模的變更。您可以在[管理工作探索工具](https://docs.cloud.google.com/bigquery/docs/admin-jobs-explorer?hl=zh-tw#filter-jobs)中，依查詢雜湊篩選。

### 比較相同查詢的執行速度

如果先前執行速度很快的查詢現在執行速度變慢，請檢查[工作 API 物件](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw)輸出內容，找出執行作業的變化。

#### 快取命中

查看 [`cacheHit`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#jobstatistics2) 值，確認工作快速執行是否為快取命中。如果快速執行查詢的值為 `true`，則查詢會使用[快取結果](https://docs.cloud.google.com/bigquery/docs/cached-results?hl=zh-tw)，而不是執行查詢。

如果您預期速度緩慢的工作會使用快取結果，請調查查詢[不再使用快取結果](https://docs.cloud.google.com/bigquery/docs/cached-results?hl=zh-tw#cache-exceptions)的原因。如果您不希望查詢從快取擷取資料，請尋找未命中快取的快速查詢執行範例，以便進行調查。

#### 配額延遲

如要判斷速度變慢是否由配額延遲造成，請檢查兩項工作的 [`quotaDeferments` 欄位](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#jobstatistics)。比較這些值，判斷較慢查詢的開始時間是否因配額延遲而延後，而較快的作業則不受影響。

#### 執行作業時間長度

如要瞭解兩項工作最後一次嘗試的執行時間長度差異，請比較 [`finalExecutionDurationMs` 欄位](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#jobstatistics2)的值。

如果 `finalExecutionDurationMs` 的值非常相似，但兩項查詢的實際執行時間差異 (計算方式為 [`startTime - endTime`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#jobstatistics)) 較大，這表示可能因暫時性問題，導致慢速工作的內部查詢執行重試。如果反覆看到這種差異模式，請[聯絡 Cloud Customer Care](https://docs.cloud.google.com/support?hl=zh-tw) 尋求協助

#### 處理的位元組數

請查看[查詢工作詳細資料頁面](https://docs.cloud.google.com/bigquery/docs/managing-jobs?hl=zh-tw#view-job)中處理的位元組，或查看 [JobStatistics](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#jobstatistics) 的 `totalBytesProcessed`，確認是否高於預期。如果兩項查詢處理的位元組數量有很大差異，則查詢速度可能會因處理的資料量變化而變慢。如要瞭解如何最佳化查詢以處理大量資料，請參閱「[最佳化查詢運算](https://docs.cloud.google.com/bigquery/docs/best-practices-performance-compute?hl=zh-tw)」。下列原因可能會導致查詢處理的位元組數增加：

* 查詢參照的資料表大小增加。
* 查詢現在會讀取資料表中較大的分區。
* 查詢參照的檢視表定義已變更。

#### 參照的資料表

分析 [`JobStatistics2`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#jobstatistics2) 中 `referencedTables` 欄位的輸出內容，確認查詢是否讀取相同的資料表。參考表格之間的差異可由下列原因解釋：

* SQL 查詢經過修改，可讀取不同的資料表。請比較查詢文字，確認是否如此。
* 檢視表定義在查詢執行期間有所變更。請檢查這項查詢參照的檢視表定義，並視需要[更新](https://docs.cloud.google.com/bigquery/docs/managing-views?hl=zh-tw)。

參照資料表之間的差異，可能可以解釋 [`totalBytesProcessed`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#jobstatistics) 的變化。

#### materialized view 用量

如果查詢參照任何[materialized view](https://docs.cloud.google.com/bigquery/docs/materialized-views-intro?hl=zh-tw)，則效能差異可能是因為在查詢執行期間選擇或拒絕 materialized view 所造成。檢查 [`MaterializedViewStatistics`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#materializedviewstatistics)，瞭解快速查詢中使用的任何 materialized view 是否在慢速查詢中遭到拒絕。查看 [`MaterializedView` 物件](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#materializedview)中的 `chosen` 和 `rejectedReason` 欄位。

#### 中繼資料快取統計資料

如果查詢涉及 Amazon S3 BigLake 資料表或已啟用中繼資料快取的 Cloud Storage BigLake 資料表，請比較 [`MetadataCacheStatistics`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#metadatacachestatistics) 的輸出內容，檢查慢速和快速查詢之間的中繼資料快取用量是否有差異，以及相應的原因。例如，中繼資料快取可能超出為資料表設定的 `maxStaleness` 時間間隔。

#### 比較 BigQuery BI Engine 統計資料

如果查詢使用 BigQuery BI Engine，請分析 [`BiEngineStatistics`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#bienginestatistics) 的輸出內容，判斷是否對慢速和快速查詢套用相同的加速模式。查看 [`BiEngineReason`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#bienginereason) 欄位，瞭解部分加速或完全未加速的大致原因，例如記憶體不足、缺少預留項目或輸入內容過大。

#### 查看查詢成效深入分析的差異

在 Google Cloud 控制台查看[**執行圖表**](https://docs.cloud.google.com/bigquery/docs/query-insights?hl=zh-tw#view_query_performance_insights)，或查看 [`StagePerformanceStandaloneInsight`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#stageperformancestandaloneinsight) 物件，比較各項查詢的[查詢效能深入分析](https://docs.cloud.google.com/bigquery/docs/query-insights?hl=zh-tw)，瞭解下列可能問題：

* 運算單元爭用情況 ([`slotContention`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#stageperformancestandaloneinsight))
* 高基數彙整 ([`highCardinalityJoins`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#highcardinalityjoin))
* 重組配額不足 ([`insufficientShuffleQuota`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#stageperformancestandaloneinsight))
* 資料偏斜 ([`partitionSkew`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#PartitionSkew))

請留意系統為慢速工作提供的洞察資料，以及快速工作產生的洞察資料之間的差異，找出影響效能的階段變化。

#### 預留項目指派

檢查指派給這兩項工作的預留項目是否有差異。變更預留項目或從隨選模式改為預留項目，可能會影響效能。詳情請參閱「[Workload Manager 模型和預留項目大小](#workload-management-models-and-reservation-size)」。

如要更徹底地分析工作執行中繼資料，您必須比較兩項工作的 [`ExplainQueryStage`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#explainquerystage) 物件，逐一檢查查詢執行的各個階段。

首先，請查看[解讀查詢階段資訊](https://docs.cloud.google.com/bigquery/docs/query-insights?hl=zh-tw#interpret_query_stage_information)一節中說明的 `Wait ms` 和 `Shuffle output bytes` 指標。

#### `INFORMATION_SCHEMA.JOBS` 檢視畫面中的資源警告

查詢 [`INFORMATION_SCHEMA.JOBS` 檢視表](https://docs.cloud.google.com/bigquery/docs/information-schema-jobs?hl=zh-tw)的 `query_info.resource_warning` 欄位，查看 BigQuery 分析的警告是否因使用的資源而有差異。

### 工作負載統計資料分析

可用的運算單元資源和運算單元爭用情況，可能會影響查詢執行時間。以下各節將說明如何瞭解特定查詢執行的運算單元用量和可用性。

#### 每秒平均運算單元數

如要計算查詢每毫秒使用的平均運算單元數，請將工作的運算單元毫秒值 (`totalSlotMs`，來自 [`JobStatistics2`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#jobstatistics2)) 除以這項工作最後一次嘗試執行的時間長度 (以毫秒為單位，`finalExecutionDurationMs`，來自 [`JobStatistics`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#jobstatistics))。

您也可以查詢 `INFORMATION_SCHEMA.JOBS` 檢視表，計算[工作每毫秒使用的平均運算單元數](https://docs.cloud.google.com/bigquery/docs/information-schema-jobs?hl=zh-tw#average_number_of_slots_per_millisecond_used_by_a_job)

如果工作執行的工作量相似，但每秒平均運算單元數量較多，完成速度就會較快。每秒平均運算單元用量較低的原因可能如下：

* 不同工作之間發生資源爭用，因此沒有額外資源可用，預留項目已達上限。
* 在執行作業的大部分時間內，工作並未要求更多運算單元。例如，資料偏斜時就可能發生這種情況。

#### Workload Manager 模型和預留項目大小

如果使用隨選計費模式，每個專案可用的運算單元數量有限。此外，如果在特定位置對隨選容量有大量爭用，則專案有時可能會較少可用運算單元。

以運算能力為基礎的模式較容易預測，可讓您指定確定的基準運算單元數量。

比較使用隨選計費模式和預留項目執行的查詢時，請考量這些差異。

建議[使用預留項目](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw)，確保查詢執行效能穩定且可預測。如要進一步瞭解隨需和依據運算能力計費的工作負載之間的差異，請參閱「[工作負載管理簡介](https://docs.cloud.google.com/bigquery/docs/reservations-intro?hl=zh-tw)」。

#### 並行工作數量

工作並行是指在查詢執行期間，工作之間競爭運算單元資源的情況。工作並行數量較高時，工作可存取的運算單元較少，因此執行速度通常較慢。

您可以查詢 `INFORMATION_SCHEMA.JOBS` 檢視表，[找出與專案中特定查詢同時執行的並行工作平均數量](https://docs.cloud.google.com/bigquery/docs/information-schema-jobs?hl=zh-tw#view_average_concurrent_jobs_running_alongside_a_particular_job_in_the_same_project)。

如果有多個專案指派給同一個預留項目，請修改查詢，使用 `JOBS_BY_ORGANIZATION` 而非 `JOBS_BY_PROJECT`，以取得準確的預留項目層級資料。

與快速工作相比，慢速工作執行期間的平均並行數量較高，是導致整體速度緩慢的原因之一。

建議您將耗用大量資源的查詢分散到不同時間或不同預留項目/專案，降低專案或預留項目中的並行數量。

另一個解決方案是購買預留項目，或增加現有預留項目的大小。建議允許預留項目[使用閒置運算單元](https://docs.cloud.google.com/bigquery/docs/reservations-tasks?hl=zh-tw#configure_whether_queries_use_idle_slots)。

如要瞭解應新增多少運算單元，請參閱「[預估運算單元容量需求](https://docs.cloud.google.com/bigquery/docs/slot-estimator?hl=zh-tw)」一文。

如果預留項目指派了多項專案，則在預留項目中執行的工作，可能會因執行專案的不同，而有不同的運算單元指派結果，但平均工作並行數相同。詳情請參閱[公平排程](https://docs.cloud.google.com/bigquery/docs/slots?hl=zh-tw#fair_scheduling_in_bigquery)。

#### 預留項目使用率

[管理員資源圖表](https://docs.cloud.google.com/bigquery/docs/admin-resource-charts?hl=zh-tw)和 [BigQuery Cloud Monitoring](https://docs.cloud.google.com/bigquery/docs/monitoring-dashboard?hl=zh-tw) 可用於監控預留項目使用率。詳情請參閱「[監控 BigQuery 預留項目](https://docs.cloud.google.com/bigquery/docs/reservations-monitoring?hl=zh-tw)」。

如要瞭解工作是否要求任何額外運算單元，請查看預估可執行單位指標，也就是 Job API 回應中的 [`estimatedRunnableUnits`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#querytimelinesample)，或 [`INFORMATION_SCHEMA.JOBS_TIMELINE` 檢視畫面](https://docs.cloud.google.com/bigquery/docs/information-schema-jobs-timeline?hl=zh-tw)中的 `period_estimated_runnable_units`。如果這項指標的值大於 0，代表工作在該時間點可能需要更多運算單元。如要估算工作執行時間中，工作可受益於額外運算單元的百分比，請對 [`INFORMATION_SCHEMA.JOBS_TIMELINE` 檢視表](https://docs.cloud.google.com/bigquery/docs/information-schema-jobs-timeline?hl=zh-tw)執行下列查詢：

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

如果百分比較低，代表在這個情境中，運算單元資源可用性並非查詢速度緩慢的主要因素。

如果百分比偏高，且預留項目在這段期間未充分利用，請[與 Cloud Customer Care 聯絡](https://docs.cloud.google.com/support?hl=zh-tw)，以便調查。

如果預留項目在工作執行速度緩慢期間已用盡，且百分比偏高，表示工作受到資源限制。請考慮降低並行、增加預留項目大小、允許預留項目使用閒置運算單元，或在工作依隨選執行時購買預留項目。

### 工作中繼資料和工作負載分析結果不確定

如果還是找不到查詢效能低於預期的原因，請[與 Cloud Customer Care 團隊聯絡](https://docs.cloud.google.com/support?hl=zh-tw)尋求協助。

## 使用 Gemini Cloud Assist 排解查詢問題

如要使用 Gemini Cloud Assist 協助[排解查詢失敗或效能問題](https://docs.cloud.google.com/bigquery/docs/use-cloud-assist?hl=zh-tw#analyze_jobs)，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在 Google Cloud 工具列，點選spark「Open or close Gemini Cloud Assist chat」(開啟或關閉 Gemini Cloud Assist 對話)。
3. 在「Cloud Assist」面板中輸入提示，並附上工作 ID，即可調查執行情形、成效指標或失敗原因。例如：

   * `為什麼 JOB_ID 失敗？`
   * `為什麼這項工作需要這麼久的時間？JOB_ID`
   * `總結我過去 24 小時的工作成效。`

## 使用 `gcpdiag` 排解查詢失敗問題

[`gcpdiag`](https://gcpdiag.dev) 是開放原始碼工具。並非官方支援的 Google Cloud 產品。您可以使用 `gcpdiag` 工具，找出並修正 Google Cloud專案問題。詳情請參閱 [GitHub 上的 gcpdiag 專案](https://github.com/GoogleCloudPlatform/gcpdiag/#gcpdiag---diagnostics-for-google-cloud-platform)。

[`gcpdiag`](https://gcpdiag.dev/) 工具可協助您分析失敗的 BigQuery 查詢，瞭解是否有已知的根本原因，以及特定失敗的緩解措施。

### 執行 `gcpdiag` 指令

您可以透過 Google Cloud CLI 執行 `gcpdiag` 指令：

## Google Cloud 控制台

1. 完成並複製下列指令。

```
gcpdiag runbook bigquery/failed-query \
   --parameter project_id=PROJECT_ID \
   --parameter bigquery_job_region=JOB_REGION \
   --parameter bigquery_job_id=JOB_ID \
   --parameter bigquery_skip_permission_check=SKIP_PERMISSION_CHECK
```

2. 開啟 Google Cloud 控制台，然後啟用 Cloud Shell。
[開啟 Cloud 控制台](https://console.cloud.google.com/bigquery?cloudshell=true&hl=zh-tw)3. 貼上複製的指令。
4. 執行 `gcpdiag` 指令，下載 `gcpdiag` Docker 映像檔，然後執行診斷檢查。如果適用，請按照輸出內容中的指示修正失敗的檢查。

## Docker

您可以[使用包裝函式執行 `gcpdiag`](https://github.com/GoogleCloudPlatform/gcpdiag?tab=readme-ov-file#installation)，在 [Docker](https://www.docker.com/) 容器中啟動 `gcpdiag`。必須安裝 Docker 或 [Podman](https://podman.io/)。

1. 複製下列指令，並在本機工作站執行。

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

查看這個 Runbook 的[可用參數](https://gcpdiag.dev/runbook/diagnostic-trees/bigquery/failed-query/#parameters)。

更改下列內容：

* PROJECT\_ID：包含資源的專案 ID。
* JOB\_REGION：執行 BigQuery 工作的區域。
* JOB\_ID：BigQuery 工作的 ID。
* SKIP\_PERMISSION\_CHECK：(選用) 如要略過相關權限檢查並加快執行手冊執行速度，請將此值設為 `True` (預設值為 `False`)。

實用旗標：

* `--universe-domain`：託管資源的[可信任合作夥伴 Sovereign Cloud](https://cloud.google.com/blog/products/identity-security/new-sovereign-controls-for-gcp-via-assured-workloads?hl=zh-tw) 網域 (如適用)
* `--parameter` 或 `-p`：Runbook 參數

如需所有 `gcpdiag` 工具旗標的清單和說明，請參閱 [`gcpdiag` 使用說明](https://github.com/GoogleCloudPlatform/gcpdiag?tab=readme-ov-file#usage)。

## Avro 結構定義解析

錯誤字串：`Cannot skip stream`

載入多個結構定義不同的 Avro 檔案時，可能會發生這項錯誤，導致結構定義解析問題，並造成匯入工作在隨機檔案失敗。

如要解決這項錯誤，請確保載入工作中按字母順序排列的最後一個檔案，包含不同結構定義的超集 (聯集)。這項規定是根據 [Avro 處理結構定義解析的方式](https://avro.apache.org/docs/1.8.1/spec.html#Schema+Resolution)而定。

## 並行查詢衝突

錯誤字串：

* `Resources exceeded during query execution: Another job JOB_ID
  is currently running in the session SESSION_ID. Concurrent jobs in
  the same session are not allowed.`
* `Session SESSION_ID has expired and is no longer
  available.`

如果多個查詢在同一個[工作階段](https://docs.cloud.google.com/bigquery/docs/sessions-intro?hl=zh-tw)中同時執行 (不支援)，或工作階段在閒置 24 小時後或建立 7 天後自動終止，就會發生這項錯誤。請參閱工作階段[限制](https://docs.cloud.google.com/bigquery/docs/sessions-intro?hl=zh-tw#limitations)和[自動終止工作階段](https://docs.cloud.google.com/bigquery/docs/sessions?hl=zh-tw#auto-terminate_a_session)。

如要解決這個問題，請採取下列任一做法：

* 請錯開共用 `session_id` 的查詢，並在前一個工作 (`JOB_ID`) 完成後再啟動下一個查詢，或在不同的工作階段中執行並行查詢。
* 如果工作階段已過期或終止，請建立新的工作階段 (並更新 `.bigqueryrc` 或 `connectionProperties` 中的 `--session_id`，如有設定)。請參閱「[建立工作階段](https://docs.cloud.google.com/bigquery/docs/sessions?hl=zh-tw#create-session)」。

## 衝突的 DML 陳述式

錯誤字串：`Could not serialize access to table due to concurrent update`

如果並行變動 data manipulation language (DML) 陳述式 (`UPDATE`、`DELETE` 或 `MERGE`) 嘗試同時修改同一個資料表分區中的資料，或是在 DML 陳述式執行期間截斷資料表，就會發生這項錯誤。

BigQuery 允許在同一個資料表上執行並行變動 DML 陳述式，只要這些陳述式修改不同的分區即可。不過，如果兩項工作嘗試修改同一個分區，則第一項提交的工作會成功，後續工作則會失敗並顯示這項錯誤。

如要解決這項錯誤，請嘗試下列做法：

* **重試失敗的工作**：如果衝突是因為與其他工作暫時重疊所致，請在衝突的工作完成後重試查詢。
* **找出並協調衝突的工作**：執行下一節的診斷查詢，找出競爭的工作，然後協調排程，確保不會同時對同一個分區執行變動 DML 作業。
* **分區資料表**：如果並行 DML 工作更新不同的資料區隔，請依日期或整數範圍分區資料表。如果並行變動 DML 陳述式修改不同的分區，則會成功執行且不會發生衝突。
* **批次 DML 作業**：將多個獨立的 `UPDATE` 或 `DELETE` 作業合併為單一 `MERGE` 陳述式或批次工作，以減少並行和修訂負擔。詳情請參閱「[最佳做法](https://docs.cloud.google.com/bigquery/docs/data-manipulation-language?hl=zh-tw#best_practices)」。

### 找出衝突的工作

如要找出發生錯誤時，有哪些工作同時更新資料表，請對 [`INFORMATION_SCHEMA.JOBS` 檢視表](https://docs.cloud.google.com/bigquery/docs/information-schema-jobs?hl=zh-tw)執行查詢：

```
SELECT
  job_id,
  query,
  start_time,
  end_time
FROM
  `region-REGION`.INFORMATION_SCHEMA.JOBS
WHERE
  creation_time BETWEEN
    TIMESTAMP_SUB(TIMESTAMP 'FAILED_JOB_START_TIME', INTERVAL 1 DAY)
    AND TIMESTAMP 'FAILED_JOB_END_TIME'
  AND destination_table.table_id = 'TABLE_NAME'
  AND destination_table.dataset_id = 'DATASET_NAME'
  AND statement_type IN ('UPDATE', 'DELETE', 'MERGE')
  AND start_time <= 'FAILED_JOB_END_TIME'
  AND (end_time >= 'FAILED_JOB_START_TIME' OR end_time IS NULL)
ORDER BY
  start_time;
```

更改下列內容：

* `REGION`：資料集所在的[區域名稱](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)，例如 `us`。
* `FAILED_JOB_START_TIME`：失敗工作開始的時間戳記，例如 `2026-09-01 09:55:00 UTC`。
* `FAILED_JOB_END_TIME`：失敗工作結束的時間戳記，例如 `2026-09-01 10:00:00 UTC`。
* `TABLE_NAME`：失敗的 DML 陳述式嘗試更新的資料表名稱。
* `DATASET_NAME`：資料表所在資料集的名稱。

如果查詢未傳回任何衝突的使用者啟動工作，則衝突可能是由其他背景作業 (例如分區到期) 引起。

### 並行更新衝突的其他原因

* **分區到期**：如果到期分區的背景系統工作在執行工作期間修改相同分區，可能會與 DML 陳述式發生衝突。如果您使用[分區到期](https://docs.cloud.google.com/bigquery/docs/managing-partitioned-tables?hl=zh-tw#partition-expiration)功能，請在分區到期時間以外的時間安排 DML 工作。
* **多陳述式交易**：當[多陳述式交易](https://docs.cloud.google.com/bigquery/docs/transactions?hl=zh-tw)變更資料表時，會封鎖該資料表上的所有其他並行 DML 陳述式，直到交易完成為止。
* **DML 陳述式影響零個資料列**：`UPDATE`、`DELETE` 或 `MERGE` 陳述式會取得目標分區的鎖定，即使沒有資料列符合篩選條件，也可能導致序列化衝突。

詳情請參閱「[DML 陳述式衝突](https://docs.cloud.google.com/bigquery/docs/data-manipulation-language?hl=zh-tw#dml_statement_conflicts)」。

## 相互關聯的子查詢

錯誤字串：`Correlated subqueries that reference other tables are not
supported unless they can be de-correlated`

如果查詢包含參照子查詢外部資料欄的子查詢 (稱為「關聯」資料欄)，就可能發生這個錯誤。系統會使用效率不佳的巢狀執行策略評估關聯子查詢，其中子查詢會針對產生關聯資料欄的外層查詢中的每個資料列進行評估。有時，BigQuery 可以在內部改寫具有關聯子查詢的查詢，以便更有效率地執行。如果 BigQuery 無法充分最佳化查詢，就會發生關聯子查詢錯誤。

如要解決這項錯誤，請嘗試下列做法：

* 從子查詢中移除任何 `ORDER BY`、`LIMIT`、`EXISTS`、`NOT EXISTS` 或 `IN` 子句。
* 使用[多重陳述式查詢](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/procedural-language?hl=zh-tw)建立臨時資料表，以便在子查詢中參照。
* 請重寫查詢，改用 `CROSS JOIN`。

## 資料欄層級存取控管權限不足

錯誤字串：

* `Access denied: Requires fineGrainedGet permission on the read columns to
  execute the DML statements`
* `Access denied: User does not have permission to access policy tag
  projects/PROJECT\_ID/locations/LOCATION/taxonomies/TAXONOMY\_ID/policyTags/POLICY\_TAG\_ID
  on column PROJECT\_ID.DATASET.TABLE.COLUMN.'

如果嘗試執行 SQL 查詢或 DML `DELETE`、`UPDATE` 或 `MERGE` 陳述式，但未獲派[精細讀取者](https://docs.cloud.google.com/bigquery/docs/column-level-security?hl=zh-tw#fine_grained_reader)角色，無法存取使用資料欄層級存取控管的資料欄，就會發生這些錯誤。設定政策標記時，系統會將這個角色指派給主體。詳情請參閱「[資料欄層級存取控管對寫入作業的影響](https://docs.cloud.google.com/bigquery/docs/column-level-security-writes?hl=zh-tw)」。

如要解決這個問題，請修改查詢，排除含有政策標記的資料欄，或將[精細讀取者](https://docs.cloud.google.com/bigquery/docs/column-level-security?hl=zh-tw#fine_grained_reader)角色授予使用者。設定政策標記時，系統會將這個角色指派給主體。詳情請參閱「[更新政策標記的權限](https://docs.cloud.google.com/bigquery/docs/column-level-security?hl=zh-tw#update_permission_policy_tags)」。

## 排解排定查詢的問題

設定或執行排定查詢時，可能會發生下列問題。

### 排定的查詢觸發重複執行作業

排定的查詢可能會在排定時間觸發多次。如果排定在整點 (例如 09:00) 執行查詢，就比較可能發生這種情況。這可能會導致非預期的結果，例如查詢執行 `INSERT` 作業時，可能會產生重複的資料。

為盡可能降低重複執行的風險，請將查詢排定在非整點時間，例如整點前後幾分鐘 (例如 08:58 或 09:03)。詳情請參閱「[排定查詢](https://docs.cloud.google.com/bigquery/docs/scheduling-queries?hl=zh-tw)」。

### 排定查詢的憑證無效

錯誤字串：

* `Error code: INVALID_USERID`
* `Error code 5: Authentication failure: User Id not found`
* `PERMISSION_DENIED: BigQuery: Permission denied while getting Drive credentials`

如果排定的查詢因憑證過期而失敗，就可能發生這項錯誤，尤其是查詢 Google 雲端硬碟資料時。

如要解決這項錯誤，請按照下列步驟操作：

* 請務必啟用 [BigQuery 資料移轉服務](https://docs.cloud.google.com/bigquery/docs/enable-transfer-service?hl=zh-tw#enable-dts)，這是使用排定查詢的[必要條件](https://docs.cloud.google.com/bigquery/docs/scheduling-queries?hl=zh-tw#before_you_begin)。
* 更新[排定查詢憑證](https://docs.cloud.google.com/bigquery/docs/scheduling-queries?hl=zh-tw#update_scheduled_query_credentials)。

### 服務帳戶憑證無效

錯誤字串：`HttpError 403 when requesting returned: The caller does not have permission`

嘗試使用服務帳戶設定排定查詢時，可能會出現這項錯誤。如要解決這項錯誤，請參閱「[授權和權限問題](https://docs.cloud.google.com/bigquery/docs/transfer-troubleshooting?hl=zh-tw#authorization_and_permission_issues)」中的疑難排解步驟。

## 目的地資料表已刪除或過期

錯誤字串：`Destination deleted/expired during operation: DETAILS`

如果查詢、載入或複製工作嘗試寫入目的地資料表，但資料表在工作執行完畢前遭到移除，就會發生這個 HTTP `400 Bad Request` 錯誤 (`reason: invalid`)。

### 診斷

這項錯誤通常是以下兩個原因之一所致：

1. **資料表或資料集已達存留時間 (TTL)。**目的地資料表 (或資料集的預設資料表到期時間) 已設定到期時間戳記。如果長時間執行的工作在資料表到期時間戳記過後仍繼續執行，BigQuery 會在工作仍在執行時刪除過期的資料表。
2. **並行明確刪除。**在工作執行期間，另一個使用者、服務帳戶或自動化工作流程 (例如自動化調度管理 DAG 或清除指令碼) 對目的地資料表執行 `DROP TABLE` 陳述式或 `tables.delete` API 呼叫。

如要判斷目的地資料表遭到刪除的原因，請查詢 [`INFORMATION_SCHEMA.TABLE_STORAGE`](https://docs.cloud.google.com/bigquery/docs/information-schema-table-storage?hl=zh-tw) 檢視表：

```
SELECT
  table_name,
  deleted,
  table_deletion_time,
  table_deletion_reason
FROM
  `PROJECT_ID`.`region-REGION`.INFORMATION_SCHEMA.TABLE_STORAGE
WHERE
  table_schema = "DATASET_ID"
  AND table_name = "TABLE_ID"
```

更改下列內容：

* `PROJECT_ID`：您的專案 ID。
* `REGION`：
  資料表所在資料集的區域。
* `DATASET_ID`：資料表所在資料集的 ID。
* `TABLE_ID`：目的地資料表的 ID。

如果資料表已過期，`table_deletion_reason` 欄會包含 `TABLE_EXPIRATION`；如果使用者刪除了資料表，則會包含 `USER_DELETED`；如果使用者刪除了包含資料表的資料集，則會包含 `DATASET_DELETION`。詳情請參閱「[找出資料表刪除原因](https://docs.cloud.google.com/bigquery/docs/restore-deleted-tables?hl=zh-tw#identify-cause)」。

如果原因是 `USER_DELETED`，請在 Logs Explorer 中查詢 Cloud 稽核記錄，找出刪除資料表的使用者。篩選工作失敗前後的項目：

```
resource.type=("bigquery_resource" OR "bigquery_dataset")
protoPayload.methodName=("tableservice.delete" OR "google.cloud.bigquery.v2.TableService.DeleteTable")
protoPayload.resourceName:"YOUR_TABLE_NAME"
```

將 `YOUR_TABLE_NAME` 替換為目的地資料表的 ID。

檢查相符記錄項目中的 `protoPayload.authenticationInfo.principalEmail` 欄位，找出刪除資料表的使用者或服務帳戶。

如果原因是 `DATASET_DELETION`，請使用「[找出資料表的刪除時間](https://docs.cloud.google.com/bigquery/docs/restore-deleted-tables?hl=zh-tw#identify_when_a_table_was_deleted)」中的資料集篩選器。

### 解析度

如要解決這項錯誤，請執行下列操作：

* **延長資料表和資料集的到期時間。**檢查目的地資料表的到期時間，以及資料集的預設資料表到期時間設定。請確保設定的存留時間夠長，足以超過寫入該資料表的工作預期執行時間上限 (包括佇列時間和重試次數)。如需操作說明，請參閱「[更新資料表的到期時間](https://docs.cloud.google.com/bigquery/docs/managing-tables?hl=zh-tw#updating_a_tables_expiration_time)」。
* **序列化管道工作。**如果自動化 ETL 管道 (例如 Managed Service for Apache Airflow、Apache Airflow 或 Dataform) 會重新建立或清理暫存資料表，請設定嚴格的工作依附關係，確保 `DROP TABLE` 或清理工作不會與針對相同資料表的有效寫入工作同時執行。
* **使用不重複的中繼資料表名稱。**執行平行管道執行個體時，請將中繼結果寫入名稱不重複的臨時或暫存資料表 (例如在多陳述式查詢中使用 `CREATE TEMP TABLE`，或附加不重複的執行 ID)，而非在並行執行作業中共用單一可變動的暫存資料表。

## 快照時間無效

錯誤字串：`Invalid snapshot time`

嘗試查詢資料集[時光旅行時間範圍](https://docs.cloud.google.com/bigquery/docs/time-travel?hl=zh-tw)以外的歷來資料時，可能會發生這項錯誤。如要解決這個錯誤，請變更查詢，在資料集的時間旅行期間內存取歷來資料。

如果查詢中使用的其中一個資料表在查詢開始後遭到捨棄並重新建立，也可能出現這項錯誤。請檢查是否有排定的查詢或應用程式執行這項作業，且與失敗的查詢同時執行。如果有，請嘗試將執行捨棄和重新建立作業的程序，移至不會與讀取該資料表的查詢衝突的時間執行。

## 工作已存在

錯誤字串：`Already Exists: Job <job name>`

如果查詢工作必須評估大型陣列，導致建立查詢工作的時間比平均時間長，就可能發生這項錯誤。例如，含有 `WHERE` 子句的查詢，例如 `WHERE column IN (<2000+ elements array>)`。

如要解決這項錯誤，請按照下列步驟操作：

* 允許 BigQuery 產生隨機 [`jobId` 值](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/JobReference?hl=zh-tw)，而非指定值。
* 使用[參數化查詢](https://docs.cloud.google.com/bigquery/docs/parameterized-queries?hl=zh-tw#use_arrays_in_parameterized_queries)載入陣列。

如果您手動設定工作 ID，但工作未在逾時期間內成功傳回，也可能發生這項錯誤。在這種情況下，您可以新增例外狀況處理常式，檢查工作是否存在。如果有的話，您就可以從工作中提取查詢結果。

## 找不到所需工作

錯誤字串：`Job not found`

如果 [`getQueryResults` 呼叫](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs/getQueryResults?hl=zh-tw)的回應未指定 `location` 欄位的值，就可能發生這項錯誤。如果是這種情況，請再次嘗試呼叫，並提供 `location` 值。

詳情請參閱「[避免多次評估相同的一般資料表運算式 (CTE)](https://docs.cloud.google.com/bigquery/docs/best-practices-performance-compute?hl=zh-tw#avoid_multiple_evaluations_of_the_same_ctes)」。

## 找不到位置

錯誤字串：`Dataset [project_id]:[dataset_id] was not found in location [region]`

如果您參照的資料集資源不存在，或要求中的位置與資料集的位置不符，就會傳回這項錯誤。

如要解決這個問題，請在查詢中指定資料集的位置，或確認資料集位於相同位置。

## 查詢超過執行時間限制

錯誤字串：`Query fails due to reaching the execution time limit` 或 `Operation timed out after 6.0 hours. Consider reducing the amount of work
performed by your operation so that it can complete within this limit.`

如果查詢達到[查詢執行時間限制](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#query_jobs)，請使用類似下列範例的查詢，查詢 [`INFORMATION_SCHEMA.JOBS` 檢視表](https://docs.cloud.google.com/bigquery/docs/information-schema-jobs?hl=zh-tw)，檢查先前查詢執行的執行時間：

```
SELECT TIMESTAMP_DIFF(end_time, start_time, SECOND) AS runtime_in_seconds
FROM `region-us`.INFORMATION_SCHEMA.JOBS
WHERE statement_type = 'QUERY'
AND query = "my query string";
```

如果先前執行查詢的時間明顯較短，請使用[查詢效能深入分析](https://docs.cloud.google.com/bigquery/docs/query-insights?hl=zh-tw)，判斷並解決根本問題。

## 查詢超過計費位元組數上限

錯誤字串：`Query exceeded limit for bytes billed: LIMIT_BYTES. REQUIRED_BYTES or higher required.`

如果查詢預估會產生費用的位元組數 (`REQUIRED_BYTES`) 超過 [`maximumBytesBilled`](https://docs.cloud.google.com/bigquery/docs/best-practices-costs?hl=zh-tw#restrict-bytes-billed) (`LIMIT_BYTES`) 設定的位元組限制，就會發生這個 HTTP `400 Bad Request` 錯誤 (`reason: bytesBilledLimitExceeded`)。BigQuery 會在執行前失敗工作，且不會收取查詢費用。

由於[隨選定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#on_demand_pricing)會對每個參照資料表強制執行 10 MB (`10,485,760` 位元組) 的下限，且分群資料表的預先執行估算會在分群修剪發生前，計算所有相符分區的上限，因此 `REQUIRED_BYTES` 可能會高於查詢執行時掃描的實際位元組數。

如要解決這個問題，請採取下列任一做法：

* **透過模擬測試預覽預估位元組數。**執行[模擬測試](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#dry-run) (bq CLI 中的 `bq query --dry_run` 或 API 中的 `configuration.dryRun = true`)，或在 Google Cloud 控制台中查看查詢驗證工具，在執行查詢前檢查 `totalBytesProcessed`。
* **最佳化查詢，減少掃描的位元組數。**請只選取查詢所需的資料欄，而非執行 `SELECT *`，並篩選分區資料欄，讓 BigQuery 在預先執行估算期間能剪除分區。篩選分群欄可減少查詢執行時實際計費的位元組數，但不會減少執行前根據 `maximumBytesBilled` 檢查的預估上限。詳情請參閱「[減少處理的資料](https://docs.cloud.google.com/bigquery/docs/best-practices-performance-compute?hl=zh-tw#reduce-data-processed)」。
* **提高 `maximumBytesBilled` 限制。**請使用 Google Cloud 控制台中的「Maximum bytes billed」(計費位元組數上限) (位於「Query settings」(查詢設定) >「Advanced options」(進階選項) 下方)、bq CLI 中的 `--maximum_bytes_billed` 旗標，或 API 中的 `configuration.query.maximumBytesBilled` 工作設定屬性，將 [`maximumBytesBilled`](https://docs.cloud.google.com/bigquery/docs/best-practices-costs?hl=zh-tw#restrict-bytes-billed) 位元組限制設為等於或高於錯誤訊息中回報的 `REQUIRED_BYTES` 值。

## 查詢回應過大

錯誤字串：`responseTooLarge`

如果查詢結果大於[回應大小上限](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#query_jobs)，或單一資料列超過 REST API 資料列大小限制，就會發生這項錯誤。

部分查詢會分多個階段執行，如果任何階段傳回的回應大小過大，即使最終結果小於上限，也會發生這項錯誤。如果查詢使用 `ORDER BY` 子句，通常會發生這個錯誤。移除 `ORDER BY` 子句或新增 `LIMIT` 子句有時會有所幫助。為確保能傳回大型結果，請在工作設定中指定目的地資料表。如果是舊版 SQL 查詢，您也必須將 `configuration.query.allowLargeResults` 屬性設為 `true`。詳情請參閱「[寫入大型查詢結果](https://docs.cloud.google.com/bigquery/docs/writing-results?hl=zh-tw#large-results)」。

### 超過單列回應大小上限

錯誤字串：

* `Response too large to return. Message before conversion exceeds max row limit, limit: LIMIT actual: ACTUAL`
* `Response too large to return. single row too big to return due to byte limit, actual: ACTUAL limit: LIMIT`

使用 [`jobs.getQueryResults`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs/getQueryResults?hl=zh-tw) 或 [`tabledata.list`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tabledata/list?hl=zh-tw) REST API 方法讀取查詢結果或資料表列 (包括在 Google Cloud 控制台或 bq 指令列工具中顯示結果) 時，如果單一未巢狀序列化資料列超過 REST 分頁端點支援的大小上限 (`jobs.getQueryResults` 為 [20 MB](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#jobs.getQueryResults_max_row_size)，`tabledata.list` 為 [100 MB](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#tabledata.list_max_row_size))，就會發生這個 HTTP `403 Forbidden` 錯誤 (`reason: responseTooLarge`)。如果資料表具有寬結構定義、深度巢狀重複 `ARRAY` 或 `STRUCT` 欄位，或大型 `STRING` 或 `BYTES` 值，通常會發生這種情況。

如要讀取超過 REST API 資料列大小限制的資料列，請採取下列任一做法：

* **使用 BigQuery Storage Read API。**使用 [Storage Read API](https://docs.cloud.google.com/bigquery/docs/reference/storage?hl=zh-tw) 讀取資料表或臨時查詢目的地資料表，該 API 會以二進位 Apache Arrow 或 Avro 格式串流資料，並支援大型和複雜資料列結構的高處理量讀取作業。
* **將資料表匯出至 Cloud Storage。**使用 [`EXPORT DATA` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/export-statements?hl=zh-tw#export_data_statement)或[擷取工作](https://docs.cloud.google.com/bigquery/docs/exporting-data?hl=zh-tw)，將資料表或查詢結果匯出至 Cloud Storage (例如 Avro、Parquet 或 JSON 格式)，然後從 Cloud Storage 讀取匯出的檔案。
* **投影或匯總較少的資料欄。**請勿執行 `SELECT *`，而是只選取應用程式所需的特定資料欄或子欄位，或在查詢中取消巢狀重複陣列，讓個別輸出資料列不超過大小限制。

## 缺少必要參數

錯誤字串：`Required parameter is missing: PARAMETER_NAME`

這項 HTTP `400 Bad Request` 錯誤 (`reason: required`) 是預先執行的 API 驗證錯誤，會在 API 要求酬載或網址中未提供必要欄位，或用戶端程式庫設定物件的必要屬性為 `null` 或 `None` 時發生。

如要解決這項錯誤，請執行下列操作：

* **查看 REST API 參考資料。**檢查錯誤訊息中的 `PARAMETER_NAME`，並在 [BigQuery REST API 參考資料](https://docs.cloud.google.com/bigquery/docs/reference/rest?hl=zh-tw)中查看該方法所需的要求主體和查詢參數，確保程式碼填入所有必要欄位。
* **驗證用戶端程式庫參數。**如果您使用 BigQuery 用戶端程式庫 (例如 Java 或 Python 用戶端程式庫)，請參閱[用戶端程式庫說明文件](https://docs.cloud.google.com/bigquery/docs/reference/libraries?hl=zh-tw)，瞭解所呼叫方法的必要參數。
* **呼叫 API 前，請先檢查設定物件。**在 API 呼叫執行前，請使用偵錯工具或記錄陳述式，立即檢查工作或要求設定物件，並確認指派給必要屬性 (例如 `destinationTable`) 的 `None` 或 `null` 值。

## 找不到預留項目或缺少運算單元

錯誤字串：`Cannot run query: project does not have the reservation in the data region or no slots are configured`

如果指派給查詢區域中專案的預留項目未指派任何運算單元，就會發生這項錯誤。您可以將運算單元新增至預留項目、允許預留項目使用閒置運算單元、使用其他預留項目，或移除指派作業並視需求執行查詢。

## 找不到資料表

錯誤字串：`Not found: Table [project_id]:[dataset].[table_name] was not found in location [region]`

如果查詢中的資料表不在指定的資料集或區域，就會發生這項錯誤。如要解決這項錯誤，請執行下列任一操作：

* 請檢查查詢是否包含正確的專案、資料集和資料表名稱，並確認 ID 的大小寫完全正確 (請參閱「[區分大小寫](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/lexical?hl=zh-tw#case_sensitivity)」)。如果查詢省略專案 ID，BigQuery 預設會使用執行工作的計費專案。查詢其他專案中的資料表時，請指定完整 `PROJECT_ID.DATASET_ID.TABLE_NAME`。
* 請確認資料表存在於查詢執行位置。根據預設，查詢讀取或寫入的每個資料集，都必須與查詢工作位於相同位置。如果您自行設定工作位置 (例如使用 `--location` 旗標或工作參照中的 `location` 屬性)，請務必確保該位置與資料集的位置相符。單一區域 (例如 `us-central1`) 與多區域 (例如 `US`) 不相符。詳情請參閱「[指定位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw#specify_locations)」。
* 如要在單一查詢中查詢不同位置的資料表，請使用[全域查詢](https://docs.cloud.google.com/bigquery/docs/global-queries?hl=zh-tw)
  [(預先發布版)](https://docs.cloud.google.com/products?hl=zh-tw#product-launch-stages)。執行查詢的專案和包含資料的專案都必須啟用全域查詢，且沙箱模式不支援全域查詢。
* 請查詢 [`INFORMATION_SCHEMA.TABLE_STORAGE`](https://docs.cloud.google.com/bigquery/docs/information-schema-table-storage?hl=zh-tw)，或檢查 Cloud 稽核記錄中的 `DeleteTable` 或 `InternalTableExpired` 事件，確認資料表或資料集是否已過期或刪除。如果資料表是在[時間旅行期間](https://docs.cloud.google.com/bigquery/docs/time-travel?hl=zh-tw) (最多 7 天) 內刪除，您可以[還原刪除的資料表](https://docs.cloud.google.com/bigquery/docs/restore-deleted-tables?hl=zh-tw)。如果父項資料集也已刪除，請先重新建立名稱和位置完全相同的空白資料集，再複製歷來快照。
* 如果您在以底線 (`_`) 開頭的隱藏資料集中，查詢匿名快取結果資料表，請注意，快取結果資料表會在約 24 小時後過期。請重新執行原始查詢，或將輸出內容寫入永久目的地資料表。
* 如果您查詢的是由 Cloud Storage 或 Google 雲端硬碟支援的外部資料表，請確認基礎來源檔案仍存在於設定的 URI 路徑 (`Not found: URI`、`Not found: Uris` 或 `Not found: Files`)。
* 請確認資料表在工作執行期間未遭到捨棄及重新建立。否則，中繼資料傳播不完整可能會導致這項錯誤。

## DML 陳述式過多

錯誤字串：`Too many DML statements outstanding against <table-name>, limit is 20`

如果單一資料表的佇列中，處於 `PENDING` 狀態的[變動 DML 陳述式超過 20 個](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#data-manipulation-language-statements)，就會發生這項錯誤。如果提交 DML 工作的速度超過 BigQuery 處理單一資料表的速度，通常就會發生這項錯誤。

如要查看佇列中處於 `PENDING` 狀態的工作，以及可能導致這些工作無法移出佇列的 `RUNNING` 工作，請查詢 [`INFORMATION_SCHEMA.JOBS` 檢視表](https://docs.cloud.google.com/bigquery/docs/information-schema-jobs?hl=zh-tw)：

```
SELECT
  project_id,
  job_id,
  creation_time,
  user_email,
  statement_type,
  state
FROM
  `region-us`.INFORMATION_SCHEMA.JOBS
WHERE
  statement_type IN ('UPDATE', 'DELETE', 'MERGE', 'TRUNCATE_TABLE')
  AND state IN ('RUNNING', 'PENDING')
ORDER BY
  creation_time DESC;
```

**注意：** `limit is 20` 佇列長度僅適用於變動 DML (`UPDATE`、`DELETE` 和 `MERGE`) 和 `TRUNCATE TABLE` 陳述式。`INSERT`
陳述式會維護獨立佇列，上限為 100。

其中一個可能的解決方案是將多個較小的 DML 作業分組，變成較大但數量較少的工作，例如批次更新和插入。將較小的工作分組為較大的工作時，執行較大工作的成本會分攤，且執行速度會更快。一般來說，合併會影響相同資料的 DML 陳述式，可提高 DML 工作的效率，且較不易超出佇列大小配額限制。如要進一步瞭解如何最佳化 DML 作業，請參閱「[避免使用更新或插入單一資料列的 DML 陳述式](https://docs.cloud.google.com/bigquery/docs/best-practices-performance-compute?hl=zh-tw#avoid-dml-update-single-rows)」。

其他提高 DML 效率的解決方案包括將資料表分區或分群。詳情請參閱「[最佳做法](https://docs.cloud.google.com/bigquery/docs/data-manipulation-language?hl=zh-tw#best_practices)」。

## 錯誤 403：超過配額

錯誤字串：`403 Quota exceeded: Your table exceeded quota for total number of
DML jobs writing to a table, pending + running.`

如果寫入單一資料表的 DML 工作 (`INSERT`、`UPDATE`、`DELETE` 和 `MERGE`) 總數 (包括 `PENDING` 和 `RUNNING` 狀態) 超過資料表的並行配額，就會發生這項錯誤。

`limit is 20` 錯誤會特別限制 `PENDING` 佇列，不允許變更 DML 陳述式 (`UPDATE`、`DELETE` 和 `MERGE`)，而 `403 Quota
exceeded` 錯誤則適用於同時寫入資料表的所有 DML 工作 (`INSERT` 加上變更 DML) 總和。由於 DML 異動作業已受限於 20 個工作的佇列限制，因此當您對單一資料表提交過多並行 `INSERT` 查詢時，最常發生這項 403 配額錯誤。如要解決這項錯誤，請按照下列步驟操作：

* *增加預留運算單元*：增加預留運算單元數量，加快工作完成速度，並減少工作並行。這可減少佇列中待處理工作的數量，避免達到上限。
* *最佳化工作流程自動化調度管理*：限制自動化調度管理工具中的並行 DML 工作數量，避免超出資料表層級的並行限制 (包括針對相同資料表的高頻率 `INSERT` 查詢)。
* *批次 DML 作業*：將多個較小的 DML 陳述式合併成較少、較大的陳述式，減少資料表排入佇列的工作總數。

## 巢狀檢視表或 persistent user-defined function 過多

錯誤字串：`Too many nested views/persistent user-defined functions or possible circular reference of views/persistent user-defined functions referenced in query. Only 16 levels of nested views/persistent user-defined functions are allowed.`

如果查詢
或檢視表建立作業參照的檢視表鏈結或永久使用者定義
函式 (UDF) 超過支援的巢狀深度上限 (16 層)
，或查詢參照的檢視表或 UDF 在循環
相依迴圈中相互參照 (例如 `view_a` 查詢 `view_b`，而 查詢
`view_a`)，就會發生這個 HTTP `400 Bad Request` 錯誤 (`reason: invalidQuery`)。如要進一步瞭解檢視表和常式限制，請參閱
「[檢視表限制](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#view_limits)」和
「[UDF 限制](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#udf_limits)」。如果錯誤是因為 `STRUCT` (`RECORD`) 欄、載入檔案或巢狀常式引數和傳回類型超過 15 層巢狀結構限制所造成，請參閱「[排解結構定義、檔案和常式巢狀結構限制錯誤](https://docs.cloud.google.com/bigquery/docs/troubleshoot-schemas?hl=zh-tw#ts-schema-nested-too-deeply)」。

您最多可以建立 16 層巢狀結構的檢視表，但查詢只能參照最多 15 層巢狀結構的檢視表。

此上限無法提高。如要解決這項錯誤，請執行下列操作：

* **檢查是否有循環參照。**檢查查詢鏈結中的檢視表和 persistent UDF 定義，確認沒有任何檢視表或函式直接或間接參照自身。
* **整合巢狀檢視畫面。**將中繼邏輯合併到單一檢視表或查詢中的通用資料表運算式 (`WITH` 子句)，藉此重構巢狀檢視表鏈結。
* **具體化中繼層。**將深層檢視區塊階層中的中繼層，替換為寫入實體資料表的排定查詢，或使用支援的 [materialized view](https://docs.cloud.google.com/bigquery/docs/materialized-views-intro?hl=zh-tw)。

## 並行更新導致交易中止

錯誤字串：`Transaction is aborted due to concurrent update against table [table_name]`

如果兩個不同的 DML 異動陳述式嘗試同時更新同一個資料表，就可能發生這項錯誤。舉例來說，假設您在工作階段中啟動[交易](https://docs.cloud.google.com/bigquery/docs/transactions?hl=zh-tw)，其中包含變動 DML 陳述式，後面接著錯誤。如果沒有例外狀況處理常式，BigQuery 會在工作階段結束時自動復原交易，最多需要 24 小時。在此期間，其他嘗試在資料表上執行變動 DML 陳述式的作業都會失敗。

如要解決這項錯誤，請[列出有效工作階段](https://docs.cloud.google.com/bigquery/docs/sessions?hl=zh-tw#list-sessions)，並檢查其中是否有任何查詢工作的狀態為 `ERROR`，且在資料表上執行了變動 DML 陳述式。在該工作階段中執行 `ROLLBACK TRANSACTION;`，復原未提交的交易，或執行 `CALL BQ.ABORT_SESSION(SESSION_ID);` [終止該工作階段](https://docs.cloud.google.com/bigquery/docs/sessions?hl=zh-tw#terminate-session)。為避免失敗的多重陳述式交易在工作階段到期前保留資料表鎖定，請在[多重陳述式交易](https://docs.cloud.google.com/bigquery/docs/transactions?hl=zh-tw#transaction_scope)中加入 `EXCEPTION WHEN ERROR THEN ROLLBACK TRANSACTION;` 處理常式。

## 錯誤 412：工作參照的資料表屬於容錯移轉資料集

錯誤字串：`Error 412: The job references a table that belongs to a failover dataset in the ... region (PROJECT_ID:DATASET_ID). However, only jobs that run on a reservation with the "ENTERPRISE_PLUS" edition can modify or write to failover datasets. Please also make sure that the job that is writing to the failover dataset is running in the current primary location.`

這表示工作並非在 BigQuery Enterprise Plus 版本下執行，或是在容錯移轉資料集主要位置以外的區域執行。詳情請參閱「[代管災難復原](https://docs.cloud.google.com/bigquery/docs/managed-disaster-recovery?hl=zh-tw)」。

## 使用快取結果時，載入檢視畫面發生錯誤

錯誤字串：`BigQuery data export: There was an error loading this view. IAM
setPolicy failed for Dataset <PROJECT_ID>. One or more users named in the policy
do not belong to a permitted customer.`

這項錯誤表示您的 Google Workspace 客戶 ID 未獲得組織政策限制的存取權。如要瞭解如何使用 `iam.allowedPolicyMemberDomains` 限制，請參閱「[使用 `iam.allowedPolicyMemberDomains` 限制實施網域限定共用](https://docs.cloud.google.com/organization-policy/restrict-domains?hl=zh-tw#predefined-constraint)」。

## 舊版 SQL 錯誤

使用舊版 SQL 時，可能會發生下列錯誤。

### `Cannot be queried with legacy SQL`

錯誤字串：`cannot be queried with legacy SQL. Please consider switching to standard SQL`

發生這項錯誤的原因有兩種：

* 查詢是以標準 SQL 編寫，但已佈建明確使用舊版 SQL 的選項。請務必按照[公開說明文件](https://docs.cloud.google.com/bigquery/docs/introduction-sql?hl=zh-tw#bigquery-sql-dialects)，使用標準 SQL 執行查詢，例如透過 bq 指令列工具提供 `--use_legacy_sql=false`。
* 您嘗試使用舊版 SQL 查詢含有定序的資料表，但系統[不支援](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/collation-concepts?hl=zh-tw)這項操作。

### 無法使用舊版 SQL 查詢資料欄重新命名的資料表

錯誤字串：`Table project:dataset.table with renamed columns cannot be queried with legacy SQL. Please consider switching to standard SQL or dropping column my_column`

如果使用舊版 SQL 查詢資料欄已重新命名的資料表，就會發生這項錯誤。請改用[標準 SQL](https://docs.cloud.google.com/bigquery/docs/introduction-sql?hl=zh-tw#bigquery-sql-dialects)。

## 使用者沒有權限

錯誤字串：

* `Access Denied: Project [project_id]: User does not have bigquery.jobs.create
  permission in project [project_id].`
* `User does not have permission to query table project-id:dataset.table.`
* `Access Denied: User does not have permission to query table or perhaps it
  does not exist.`

執行查詢時，如果對執行查詢的專案沒有 `bigquery.jobs.create` 權限，就可能發生這些錯誤，無論您對包含資料的專案具備哪些權限。

如果服務帳戶、使用者或群組對查詢參照的所有資料表和檢視表沒有 `bigquery.tables.getData` 權限，也可能收到這些錯誤。如要進一步瞭解執行查詢所需的權限，請參閱「[必要角色](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#required_permissions)」。

如果資料表不存在於查詢的區域 (例如 `asia-south1`)，也可能發生這些錯誤。您可以檢查[資料集位置](https://docs.cloud.google.com/bigquery/docs/datasets-intro?hl=zh-tw#dataset_location)來驗證區域。

解決這些錯誤時，請考量下列事項：

* *服務帳戶*：服務帳戶必須具備執行專案的 `bigquery.jobs.create` 權限，以及查詢參照的所有資料表和檢視表的 `bigquery.tables.getData` 權限。
* *自訂角色*：自訂 IAM 角色必須在相關角色中明確包含 `bigquery.jobs.create` 權限，且必須具備查詢參照的所有資料表和檢視表的 `bigquery.tables.getData` 權限。
* *共用資料集*：在獨立專案中使用共用資料集時，您可能仍需要專案中的 `bigquery.jobs.create` 權限，才能在該資料集中執行查詢或工作。

如要授予資料表或檢視表的存取權，請參閱「[授予資料表或檢視表的存取權](https://docs.cloud.google.com/bigquery/docs/control-access-to-resources-iam?hl=zh-tw#grant_access_to_a_table_or_view)」。

**注意：** 如果使用者帳戶或服務帳戶受到拒絕政策影響，即使帳戶具備正確權限，您仍可能收到 `Access denied` 錯誤。詳情請參閱「[拒絕政策](https://docs.cloud.google.com/iam/docs/deny-overview?hl=zh-tw)」。

### 預留項目的權限「`bigquery.reservations.use`」遭拒

錯誤字串：

* `Access Denied: Reservation projects/project/locations/region/reservations/reservation_name: Permission bigquery.reservations.use denied on reservation projects/project/locations/region/reservations/reservation_name (or it may not exist)`

如果使用 `SET @@reservation` 陳述式指派查詢在特定預留項目中執行，但使用者或服務帳戶缺少 `bigquery.reservations.use` 權限，就會發生這項錯誤。您可以在 Cloud Logging 或 BigQuery 工作頁面中檢查失敗原因，找出嘗試執行這項作業的主體。

### 其他 `Access Denied` 項錯誤

錯誤字串：

* `Access Denied: Dataset project_id:dataset_id: Permission bigquery.datasets.get denied on dataset project_id:dataset_id (or it may not exist).`
* `Access Denied: Dataset project_id:dataset_id: Permission bigquery.datasets.update denied on dataset project_id:dataset_id (or it may not exist).`
* `Access Denied: BigQuery BigQuery: User does not have permission to access data protected by policy tag`

如要排解 BigQuery 中的一般 `Access Denied` 錯誤，請使用[政策分析工具](https://docs.cloud.google.com/policy-intelligence/docs/analyze-iam-policies?hl=zh-tw)[判斷主體對資源具備哪些存取權](https://docs.cloud.google.com/policy-intelligence/docs/analyze-iam-policies?hl=zh-tw#access-query)。

在政策分析工具中，提供您嘗試存取的 BigQuery 資源 (例如 `//bigquery.googleapis.com/projects/YOUR_PROJECT/datasets/YOUR_DATASET/tables/YOUR_TABLE`)，以及收到 `Access Denied` 錯誤的使用者或服務帳戶電子郵件地址做為主體。分析結果會顯示主體對資源的權限，您可以與錯誤訊息中缺少的權限進行比較。

## 指令碼不支援目的地加密

錯誤字串：`configuration.query.destinationEncryptionConfiguration cannot be set for scripts`

嘗試為 BigQuery 指令碼工作設定目的地加密設定時，就會發生這項錯誤，因為系統[不支援](https://docs.cloud.google.com/bigquery/docs/customer-managed-encryption?hl=zh-tw#script-limitations)這項操作。

## 組織政策禁止存取

錯誤字串：
`IAM setPolicy failed for Dataset DATASET: Operation
denied by org policy on resource.`

如果組織政策禁止主體查詢 BigQuery 資源，就會發生這項錯誤。[組織政策服務](https://docs.cloud.google.com/resource-manager/docs/organization-policy/overview?hl=zh-tw)可讓您在整個組織階層中，對[支援的資源](https://docs.cloud.google.com/resource-manager/docs/organization-policy/org-policy-constraints?hl=zh-tw)強制執行限制。

如果主體應有資源存取權，請使用可用的 [VPC 疑難排解工具](https://docs.cloud.google.com/vpc/docs/troubleshooting-policy-and-access-problems?hl=zh-tw#troubleshooting_tools)，診斷組織政策問題。

## 資源超出問題

如果 BigQuery 沒有足夠的資源來完成查詢，就會發生下列問題。

### 查詢超過 CPU 資源

錯誤字串：`Query exceeded resource limits. This query used
CPU_SECONDS_USED CPU seconds but would charge only
ANALYSIS_MEGABYTES_BILLEDM Analysis bytes. This exceeds the ratio
supported by the on-demand pricing model. Please consider moving this workload
to a capacity-based pricing model, which does not have this limit.
CPU_SECONDS_USED CPU seconds were used, and this query must use less
than CPU_SECONDS_LIMIT CPU seconds.`

如果查詢採用隨選定價模式，且超出[每掃描資料的 CPU 用量上限](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#max_cpu_usage_on-demand) (每 MiB 掃描資料約 256 CPU 秒)，就會發生這項錯誤 (`billingTierLimitExceeded`)。如果隨選查詢對相對少量的掃描資料執行 CPU 密集作業，例如不受限制的 `CROSS
JOIN` 作業、不精確的彙整條件、複雜的規則運算式、未分區的分析視窗函式，或運算量大的 JavaScript UDF，就會發生這種情況。

如要解決這個錯誤，請執行下列任一操作：

* **最佳化查詢。**重構 SQL，減少掃描資料的運算負擔，例如移除非預期的笛卡兒乘積 (不含篩選條件的 `CROSS
  JOIN` 作業)、取代不精確的 join 述詞、簡化複雜的規則運算式、在大型未分區視窗的 window 函式中加入 `PARTITION BY` 子句，或最佳化 JavaScript UDF。詳情請參閱「[避免反 SQL 模式](https://docs.cloud.google.com/bigquery/docs/best-practices-performance-compute?hl=zh-tw#avoid-anti-sql-patterns)」、「[最佳化查詢效能簡介](https://docs.cloud.google.com/bigquery/docs/best-practices-performance-overview?hl=zh-tw)」和「[排解資源超出問題](#ts-resources-exceeded)」。
* **改用依運算資源計價模式。**使用[以運算資源 (運算單元) 為基礎的定價模式](https://docs.cloud.google.com/bigquery/docs/reservations-intro?hl=zh-tw)執行工作負載。在依運算資源計價模式中，查詢不受隨選 CPU 與位元組比率限制。

### 查詢超過記憶體資源

錯誤字串：`Resources exceeded during query execution: The query could not be executed in the allotted memory`

如果是 [`SELECT` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw#select_list)，當查詢使用的資源過多時，就會發生這項錯誤。如要解決這項錯誤，請參閱「[排解資源超出問題](#ts-resources-exceeded)」。

### 堆疊空間不足

錯誤字串：`Out of stack space due to deeply nested query expression during query resolution.`

如果查詢包含過多巢狀函式呼叫，就可能發生這項錯誤。有時，查詢的某些部分會在剖析期間轉譯為函式呼叫。例如，具有重複[串連運算子](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/operators?hl=zh-tw#concatenation_operator)的運算式 (例如 `A || B || C || ...`) 會變成 `CONCAT(A, CONCAT(B, CONCAT(C, ...)))`。

如要解決這個錯誤，請重寫查詢，減少巢狀結構數量。

### 查詢執行期間資源超出上限

錯誤字串：`Resources exceeded during query execution: The query could not be executed in the allotted memory. Peak usage: [percentage]% of limit. Top memory consumer(s): ORDER BY operations.`

`ORDER BY ... LIMIT ... OFFSET ...` 查詢可能會發生這種情況。由於實作細節，排序可能會在單一運算單元上進行，如果需要在套用 `LIMIT` 和 `OFFSET` 之前處理過多資料列，可能會發生記憶體不足，尤其是 `OFFSET` 較大時。

如要解決這項錯誤，請避免在 `ORDER BY` ... `LIMIT` 查詢中使用過大的 `OFFSET` 值。或者，您也可以使用可擴充的 `ROW_NUMBER()` 視窗函式，根據所選順序指派排名，然後在 `WHERE` 子句中篩選這些排名。例如：

```
SELECT ...
FROM (
  SELECT ROW_NUMBER() OVER (ORDER BY ...) AS rn
  FROM ...
)
WHERE rn > @start_index AND rn <= @page_size + @start_index  -- note that row_number() starts with 1
```

### TensorFlow worker 記憶體不足

錯誤字串：`Resources exceeded during query execution: TensorFlow worker out
of memory`。

如果模型超出記憶體限制 (通常為 250 MB)，特別是使用 `ML.EXPLAIN_PREDICT` 等需要大量資源的函式時，就可能觸發這項錯誤。

如要解決這項錯誤，請執行下列任一操作：

1. *使用 Gemini Enterprise Agent Platform 遠端模型*：如果模型超出記憶體限制，請按照 Vertex AI SDK for Python 的[部署模型](https://docs.cloud.google.com/gemini-enterprise-agent-platform/machine-learning/predictions/deploy-model-api?hl=zh-tw)步驟，將模型部署至 Agent Platform，然後使用[遠端模型](https://docs.cloud.google.com/bigquery/docs/bigquery-ml-remote-model-tutorial?hl=zh-tw)存取。這會將記憶體需求卸載至專屬的 Agent Platform 基礎架構。
2. *最佳化模型*：使用架構簡化、量化或剪枝，減少模型的 RAM 占用空間。
3. *使用較不耗費資源的函式*：如果錯誤發生在 `ML.EXPLAIN_PREDICT` 呼叫期間，請嘗試使用 `ML.PREDICT` 執行工作，判斷模型是否能在不耗費額外資源的情況下執行可解釋性功能。
4. *分析輸入資料大小*：個別資料列過大可能會導致記憶體耗盡。使用下列指令，查看最大資料列的大小：

   ```
   SELECT BYTE_LENGTH(TO_JSON_STRING(t)) AS row_size
   FROM your_table AS t
   ORDER BY row_size DESC
   LIMIT 10
   ```

### 查詢超過重組資源

錯誤字串：`Resources exceeded during query execution: Your project or organization exceeded the maximum disk and memory limit available for shuffle operations`

如果查詢無法存取足夠的重組資源，就會發生這項錯誤。

如要解決這項錯誤，請佈建更多運算單元，或減少查詢處理的資料量。如要進一步瞭解如何執行這項操作，請參閱「[重組配額不足](https://docs.cloud.google.com/bigquery/docs/query-insights?hl=zh-tw#insufficient_shuffle_quota)」。

如果使用[隨選](https://cloud.google.com/bigquery/pricing?hl=zh-tw#on_demand_pricing)定價模式，則[最多只能使用 2,000 個運算單元](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#query_jobs)。如要增加運算單元數量，必須改用[依運算資源計費](https://cloud.google.com/bigquery/pricing?hl=zh-tw#capacity_compute_analysis_pricing)的定價模式。

如要進一步瞭解如何解決這些問題，請參閱「[排解資源超出問題](#ts-resources-exceeded)」。

### 查詢過於複雜

錯誤字串：

* `Resources exceeded during query execution: Not enough resources for query planning - too many subqueries or query is too complex.`
* `Resources exceeded during query execution: Not enough resources for query planning - too many fields accessed or query is too complex.`
* `Resources exceeded during query execution: Not enough resources for query planning - query is too complex.`
* `Resources exceeded during query execution: The query is too complex.`

在查詢規劃期間展開檢視表、`WITH` 子句和 SQL user-defined function (UDF) 後，如果查詢過於複雜，就會發生這項錯誤。造成複雜性的主要原因如下：

* `WITH` 子句深度巢狀或重複使用。
* 深度巢狀或重複使用的檢視畫面。
* 重複使用 [`UNION ALL` 運算子](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw#union_example)。
* 複雜的 [SQL UDF](https://docs.cloud.google.com/bigquery/docs/user-defined-functions?hl=zh-tw#sql-udf-structure) 或新增多個資料欄的寬參照資料表。

如要解決這項錯誤，請嘗試下列方法：

* 將查詢分割成多個查詢，然後使用[程序語言](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/procedural-language?hl=zh-tw)，以共用狀態依序執行這些查詢。
* 使用臨時資料表，而非 `WITH` 子句或深度巢狀檢視表。請參閱「[避免多次評估相同的 CTE](https://docs.cloud.google.com/bigquery/docs/best-practices-performance-compute?hl=zh-tw#avoid_multiple_evaluations_of_the_same_ctes)」。
* 改寫查詢，減少參照的物件、資料欄和比較項目數量。

您可以使用 [`INFORMATION_SCHEMA.JOBS` 檢視表](https://docs.cloud.google.com/bigquery/docs/information-schema-jobs?hl=zh-tw)中的 `query_info.resource_warning` 欄位，主動監控複雜度接近上限的查詢。下列範例會傳回過去三天內資源用量偏高的查詢：

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

如要進一步瞭解如何解決這些問題，請參閱「[排解資源超出問題](#ts-resources-exceeded)」。

### 疑難排解資源超出問題

**查詢工作**：

如要最佳化查詢，請嘗試下列步驟：

* 請嘗試移除 `ORDER BY` 子句 (特別是子查詢或 `WITH` 子句中的子句)、新增 `LIMIT` 子句，或在回報 `Top memory consumer(s): ORDER BY
  operations` 時使用 `ROW_NUMBER() OVER (ORDER BY
  ...)` 而非大型 `OFFSET` 進行分頁。請參閱「[查詢超出記憶體資源](#query_not_executed)」。
* 如果查詢失敗，並顯示 `Top memory consumer(s): sort operations used for
  analytic OVER() clauses` 或 `analytic OVER() clauses`，請重寫查詢，減少每個視窗分區中的資料量 (新增或精簡 `PARTITION BY` 鍵)，或在適用情況下，將 `RANGE BETWEEN` 替換為有界限的 `ROWS BETWEEN` 視窗框架。
* 如果查詢使用 `JOIN` (或因 `Top memory consumer(s): JOIN
  operations` 失敗)，請確認較大的資料表位於子句左側，且資料不含重複的 join 鍵。如果 `CROSS JOIN` 後面接著 `GROUP BY` 超過記憶體，請先將 `CROSS JOIN` 的中繼結果儲存至暫存資料表，再執行 `GROUP BY`。
* 如果變動 DML 陳述式失敗並顯示 `Top memory consumer(s): sort operation
  used for table update (UPDATE/DELETE/MERGE)`，請分割 `UPDATE` 或 `MERGE` 陳述式，一次更新較少資料列或資料欄 (或將使用 `ON FALSE` 的 `MERGE` 替換為[多陳述式交易](https://docs.cloud.google.com/bigquery/docs/transactions?hl=zh-tw)中的 `INSERT` 和 `DELETE`)。
* 如果查詢失敗並顯示 `Top memory consumer(s): query parsing and
  optimization`，請將大型硬式編碼常值清單儲存在臨時資料表，而非內嵌在查詢文字中，或將查詢拆分為較小的查詢。
* 如果查詢失敗並顯示 `UDF out of memory` 或 `Top memory consumer(s):
  non-SQL user-defined functions`，請避免在 JavaScript UDF 中累積過多本機狀態、以較小的區塊處理輸入資料，或使用 [SQL UDF](https://docs.cloud.google.com/bigquery/docs/user-defined-functions?hl=zh-tw#sql-udf-structure) 或內建 GoogleSQL 函式重寫 UDF。請參閱「[JavaScript UDF 最佳做法](https://docs.cloud.google.com/bigquery/docs/user-defined-functions?hl=zh-tw#best-practices-for-javascript-udfs)」。
* 如果查詢使用 `FLATTEN`，請判斷是否需要用於您的用途。詳情請參閱[巢狀與重複的資料](https://docs.cloud.google.com/bigquery/docs/data?hl=zh-tw#nested)。
* 如果查詢使用 `EXACT_COUNT_DISTINCT`，建議改用 [`COUNT(DISTINCT)`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/aggregate_functions?hl=zh-tw#count)。
* 如果查詢使用 `COUNT(DISTINCT <value>, <n>)` 且 `<n>` 值很大，建議改用 `GROUP BY`。詳情請參閱 [`COUNT(DISTINCT)`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/aggregate_functions?hl=zh-tw#count)。
* 如果查詢使用 `UNIQUE`，建議改用 `GROUP BY`，或在子選取項目中使用[視窗函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/window-function-calls?hl=zh-tw)。
* 如果查詢使用 `LIMIT` 子句具體化許多資料列，請考慮篩選其他資料欄 (例如 `ROW_NUMBER()`)，或完全移除 `LIMIT` 子句，以允許寫入平行處理。
* 如果查詢使用深度巢狀檢視表和 `WITH` 子句，複雜度可能會呈指數級成長，進而達到上限。
* 使用暫存資料表，而非 `WITH` 子句。`WITH` 子句可能需要重新計算多次，導致查詢變得複雜，進而降低速度。將中繼結果保存在臨時資料表中，可降低複雜度。
* 避免使用 `UNION ALL` 查詢。
* 如果查詢使用 `MATCH_RECOGNIZE`，請修改 [`PARTITION BY` 子句](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw#match_recognize_partition_by)來縮減分區大小，或新增 `PARTITION BY` 子句 (如果沒有的話)。
* 如果工作失敗並顯示 `Table TABLE_NAME will have
  N partitions when the job finishes, exceeding limit 10000`，請在 [`INFORMATION_SCHEMA.PARTITIONS`](https://docs.cloud.google.com/bigquery/docs/information-schema-partitions?hl=zh-tw) 中檢查資料表的分區數量、設定[分區到期時間](https://docs.cloud.google.com/bigquery/docs/managing-partitioned-tables?hl=zh-tw#partition-expiration)，或明確刪除不必要的分區 (因為最近到期的分區可能需要一段時間才會反映，除非明確刪除)。請參閱[分區資料表配額](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#partitioned_tables)。
* 如果工作失敗並顯示 `Too many DML statements outstanding against table
  TABLE_NAME, limit is 20`，請將多個較小的 `UPDATE`、`DELETE` 或 `MERGE` 陳述式分組為較少、較大的工作，或對目標資料表進行分區和分群。請參閱「[DML 陳述式過多](#too_many_DML)」和「[資料表有過多待處理的 DML 陳述式](https://docs.cloud.google.com/bigquery/docs/troubleshoot-quotas?hl=zh-tw#ts-too-many-dml-statements-against-table-quota)」。
* 如果工作失敗並顯示 `All our servers are busy processing data transferred
  between regions. Please try again shortly.`，請重試查詢，或降低跨雲端 (`BigQuery Omni`) join、`CREATE TABLE AS SELECT`、`INSERT INTO SELECT` 或 `LOAD DATA` 查詢的並行率 (或[與支援團隊聯絡](https://docs.cloud.google.com/bigquery/docs/getting-support?hl=zh-tw)，要求提高跨區域移轉查詢頻率限制)。請參閱「[BigQuery Omni join 限制](https://docs.cloud.google.com/bigquery/docs/biglake-intro?hl=zh-tw#cross-cloud_join_limitations)」和「[使用跨雲端移轉功能載入資料](https://docs.cloud.google.com/bigquery/docs/load-data-using-cross-cloud-transfer?hl=zh-tw)」。
* 如果工作失敗並顯示 `Google Sheets service overloaded for spreadsheet
  id: SPREADSHEET_ID`，請重試暫時性的 Google 試算表超載，或將試算表資料複製到永久 [BigQuery 資料表](https://docs.cloud.google.com/bigquery/docs/writing-results?hl=zh-tw#permanent-table) (並重構檢視表或錯開[排定的查詢](https://docs.cloud.google.com/bigquery/docs/scheduling-queries?hl=zh-tw)，減少對同一試算表的並行讀取)。
* 如果 BigQuery Omni 查詢失敗並顯示 `Response too large. Query returned ACTUAL_MBMB, and limit is
  LIMIT_MBMB.`，表示查詢輸出內容超出 [BigQuery Omni 查詢結果大小上限](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#max_result_size_query_omni)或[跨雲端移轉限制](https://docs.cloud.google.com/bigquery/docs/load-data-using-cross-cloud-transfer?hl=zh-tw#filter-data)。篩選或匯總查詢，傳回較小的結果，或使用 [`EXPORT DATA` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/export-statements?hl=zh-tw)，將大型結果直接匯出至外部儲存空間，而非目的地資料表。

詳情請參閱下列資源：

* [最佳化調整查詢運算](https://docs.cloud.google.com/bigquery/docs/best-practices-performance-compute?hl=zh-tw)。
* [進一步瞭解資源警告](https://docs.cloud.google.com/bigquery/docs/information-schema-jobs?hl=zh-tw#get_details_about_a_resource_warning)
* [監控健康狀態、資源使用率和工作](https://docs.cloud.google.com/bigquery/docs/admin-resource-charts?hl=zh-tw)

**載入工作**：

如果您要載入 Avro 或 Parquet 檔案，請縮減檔案中的資料列大小。請查看載入檔案格式的特定大小限制：

* [Avro 輸入檔案規定](https://docs.cloud.google.com/bigquery/docs/loading-data-cloud-storage-avro?hl=zh-tw#input_file_requirements)
* [Parquet 輸入檔案規定](https://docs.cloud.google.com/bigquery/docs/loading-data-cloud-storage-parquet?hl=zh-tw#input_file_requirements)

如果載入 ORC 檔案時收到這則錯誤訊息，請[與支援團隊聯絡](https://docs.cloud.google.com/support?hl=zh-tw)。

**Storage API：**

錯誤字串：`Stream memory usage exceeded`

在 Storage Read API `ReadRows` 呼叫期間，部分記憶體用量偏高的串流可能會收到 `RESOURCE_EXHAUSTED` 錯誤，並顯示這則訊息。讀取寬資料表或結構定義複雜的資料表時，就可能發生這種情況。如要解決這個問題，請減少要讀取的資料欄 (使用 [`selected_fields` 參數](https://docs.cloud.google.com/bigquery/docs/reference/storage/rpc/google.cloud.bigquery.storage.v1?hl=zh-tw#tablereadoptions))，或簡化資料表結構定義，藉此縮減結果列大小。

## 排解連線問題

下列各節說明如何排解嘗試與 BigQuery 互動時發生的連線問題：

### 將 Google DNS 加入許可清單

使用 [Google IP Dig 工具](https://toolbox.googleapps.com/apps/dig/#A/)，將 BigQuery DNS 端點 `bigquery.googleapis.com` 解析為單一「A」記錄 IP。請確認防火牆設定未封鎖這個 IP。

一般來說，建議您將 Google DNS 名稱加入許可清單。<https://www.gstatic.com/ipranges/goog.json> 和 <https://www.gstatic.com/ipranges/cloud.json> 檔案中分享的 IP 範圍經常變更，因此建議您改為將 Google DNS 名稱加入許可清單。以下是我們建議加入許可清單的常見 DNS 名稱：

* `*.1e100.net`
* `*.google.com`
* `*.gstatic.com`
* `*.googleapis.com`
* `*.googleusercontent.com`
* `*.appspot.com`
* `*.gvt1.com`

### 找出捨棄封包的 Proxy 或防火牆

如要找出用戶端和 Google Front End (GFE) 之間的所有封包躍點，請在用戶端機器上執行 [`traceroute`](https://en.wikipedia.org/wiki/Traceroute) 指令，找出捨棄導向 GFE 封包的伺服器。以下是 `traceroute` 指令範例：

```
traceroute -T -p 443 bigquery.googleapis.com
```

如果問題與特定 IP 位址有關，您也可以找出特定 GFE IP 位址的封包躍點：

```
traceroute -T -p 443 142.250.178.138
```

如果發生 Google 端逾時問題，您會看到要求一路傳送至 GFE。

如果封包從未到達 GFE，請與網路管理員聯絡，解決這個問題。

### 生成 PCAP 檔案並分析防火牆或 Proxy

產生封包擷取檔案 (PCAP) 並加以分析，確認防火牆或 Proxy 未篩除傳送至 Google IP 的封包，且允許封包傳送至 GFE。

以下是可透過 [`tcpdump`](https://www.tcpdump.org/) 工具執行的指令範例：

```
tcpdump -s 0 -w debug.pcap -K -n host bigquery.googleapis.com
```

### 設定間歇性連線問題的重試機制

在某些情況下，GFE 負載平衡器可能會捨棄來自用戶端 IP 的連線，例如偵測到 DDoS 流量模式，或負載平衡器執行個體縮減，導致端點 IP 遭到回收。如果 GFE 負載平衡器中斷連線，用戶端必須擷取逾時要求，並重新向 DNS 端點傳送要求。在要求成功前，請勿使用相同的 IP 位址，因為 IP 位址可能已變更。

如果您發現 Google 端持續逾時，且重試也無法解決問題，請[與 Cloud Customer Care 聯絡](https://docs.cloud.google.com/support?hl=zh-tw)，並務必附上新的 PCAP 檔案，該檔案應由 [tcpdump](https://www.tcpdump.org/) 等封包擷取工具產生。

## 後續步驟

* [取得查詢成效洞察](https://docs.cloud.google.com/bigquery/docs/query-insights?hl=zh-tw)。
* 進一步瞭解如何[盡可能提高查詢效能](https://docs.cloud.google.com/bigquery/docs/best-practices-performance-overview?hl=zh-tw)。
* 查看查詢的[配額與限制](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#query_jobs)。
* 進一步瞭解其他 [BigQuery 錯誤訊息](https://docs.cloud.google.com/bigquery/docs/error-messages?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-10-24 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-10-24 (世界標準時間)。"],[],[]]