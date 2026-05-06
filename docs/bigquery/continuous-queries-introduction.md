Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 持續查詢簡介

本文說明 BigQuery 持續查詢。

BigQuery 持續查詢是會不斷執行的 SQL 陳述式，持續查詢功能可讓您即時分析 BigQuery 中的傳入資料。您可以將持續查詢產生的輸出資料列插入 BigQuery 資料表，或匯出至 Pub/Sub、Bigtable 或 Spanner。持續查詢可使用下列其中一種方法，處理已寫入[標準 BigQuery 資料表](https://docs.cloud.google.com/bigquery/docs/tables-intro?hl=zh-tw#standard-tables)的資料：

* [BigQuery Storage Write API](https://docs.cloud.google.com/bigquery/docs/write-api?hl=zh-tw)
* [`tabledata.insertAll` 方法](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tabledata/insertAll?hl=zh-tw)
* [批次載入](https://docs.cloud.google.com/bigquery/docs/batch-loading-data?hl=zh-tw)
* [`INSERT` DML 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/dml-syntax?hl=zh-tw#insert_statement)
* [資料操縱語言 (DML) 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/dml-syntax?hl=zh-tw) (例如 `DELETE`、`UPDATE` 和 `MERGE`) [將資料匯出至 Pub/Sub](https://docs.cloud.google.com/bigquery/docs/export-to-pubsub?hl=zh-tw) 時發生突變。
* 將[批次查詢結果寫入永久資料表](https://docs.cloud.google.com/bigquery/docs/writing-results?hl=zh-tw#permanent-table)
* [將 BigQuery 持續查詢的結果寫入永久資料表](https://docs.cloud.google.com/bigquery/docs/continuous-queries?hl=zh-tw#write-bigquery)
* [Pub/Sub BigQuery 訂閱項目](https://docs.cloud.google.com/pubsub/docs/bigquery?hl=zh-tw)
* 從 [Dataflow 寫入 BigQuery](https://docs.cloud.google.com/dataflow/docs/guides/write-to-bigquery?hl=zh-tw)
* 使用[僅限附加的寫入模式](https://docs.cloud.google.com/datastream/docs/destination-bigquery?hl=zh-tw#append-only_write_mode)，將資料從 Datastream 寫入 BigQuery

您可以使用持續查詢執行具時效性的工作，例如建立洞察資料並立即採取行動、套用即時機器學習 (ML) 推論，以及將資料複製到其他平台。這樣一來，您就能將 BigQuery 做為應用程式決策邏輯的事件驅動式資料處理引擎。

下圖顯示常見的持續查詢工作流程：

## 用途

以下是您可能想使用連續查詢的常見用途：

* **個人化顧客互動服務**：使用生成式 AI 建立專屬訊息，為每次顧客互動提供客製化服務。
* **異常偵測**：建構解決方案，即時對複雜資料執行異常狀況和威脅偵測，以便更快應對問題。
* **可自訂的事件導向管道**：整合 Pub/Sub 持續查詢，根據傳入的資料觸發下游應用程式。
* **資料擴充和實體擷取**：使用持續查詢，透過 SQL 函式和 ML 模型執行即時資料擴充和轉換。
* **反向擷取、轉換及載入 (ETL)**：執行即時反向 ETL，將資料載入至其他更適合低延遲應用程式服務的儲存系統。舉例來說，您可以分析或改善寫入 BigQuery 的事件資料，然後將資料串流至 Bigtable 或 Spanner，以用於應用程式服務。
* **自主觸發代理程式**：根據即時資料串流中偵測到的複雜事件，即時觸發代理程式資料管道。如需範例，請參閱[使用 BigQuery 和 Agent Development Kit (ADK) 建構事件導向的資料代理程式碼實驗室](https://codelabs.developers.google.com/bigquery-adk-event-driven-agents?hl=zh-tw)。
* **自主式代理程式監控**：使用 [BigQuery 代理程式分析外掛程式](https://adk.dev/integrations/bigquery-agent-analytics/)，針對即時代理功能互動開發即時自動監控和警報功能，將所有代理程式追蹤記錄資料、工具用量和作業記錄直接串流到 BigQuery，深入觀察 AI 員工。

## 支援的功能

持續查詢支援下列作業：

* 執行 [`INSERT` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/dml-syntax?hl=zh-tw#insert_statement)，將持續查詢的資料寫入 BigQuery 資料表。
* 執行 [`EXPORT DATA` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/export-statements?hl=zh-tw)，將持續查詢的輸出內容[發布](https://docs.cloud.google.com/pubsub/docs/publish-message-overview?hl=zh-tw)至 Pub/Sub 主題。詳情請參閱「[將資料匯出至 Pub/Sub](https://docs.cloud.google.com/bigquery/docs/export-to-pubsub?hl=zh-tw)」一節。

  您可以透過 Pub/Sub 主題使用資料，例如使用 Dataflow 執行串流分析，或在應用程式整合工作流程中使用資料。
* 執行 `EXPORT DATA` 陳述式，將資料從 BigQuery 匯出至 [Bigtable 資料表](https://docs.cloud.google.com/bigtable/docs/managing-tables?hl=zh-tw)。詳情請參閱[將資料匯出至 Bigtable](https://docs.cloud.google.com/bigquery/docs/export-to-bigtable?hl=zh-tw)。
* 執行 `EXPORT DATA` 陳述式，將資料從 BigQuery 匯出至 Spanner 資料表。詳情請參閱「[將資料匯出至 Spanner (反向 ETL)](https://docs.cloud.google.com/bigquery/docs/export-to-spanner?hl=zh-tw)」。
* 呼叫下列生成式 AI 函式：

  + [`AI.GENERATE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-ai-generate?hl=zh-tw)
  + [`AI.GENERATE_TEXT`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-ai-generate-text?hl=zh-tw)

    - 如要使用這項函式，您必須透過 [Vertex AI 模型](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/learn/models?hl=zh-tw)建立 [BigQuery ML 遠端模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model?hl=zh-tw)。
* 呼叫下列 AI 函式：

  + [`ML.UNDERSTAND_TEXT`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-understand-text?hl=zh-tw)
  + [`ML.TRANSLATE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-translate?hl=zh-tw)

  如要使用這些函式，您必須透過 Cloud AI API 建立 [BigQuery ML 遠端模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model-service?hl=zh-tw)。
* 使用 [`ML.NORMALIZER` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-normalizer?hl=zh-tw)正規化數值型資料。
* 分析及處理 `JSON` 資料，包括支援 [JSON 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/json_functions?hl=zh-tw)和 [JSON 取消巢狀結構](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw#unnest_operator)。
* 使用無狀態 GoogleSQL 函式，例如[轉換函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/conversion_functions?hl=zh-tw)。在無狀態函式中，系統會獨立處理資料表中的每一列。
* 使用[有狀態作業](https://docs.cloud.google.com/bigquery/docs/continuous-queries-introduction?hl=zh-tw#supported_stateful_operations)，例如 [`JOIN`s、匯總和視窗匯總](https://docs.cloud.google.com/bigquery/docs/continuous-queries?hl=zh-tw#join-agg-window-example)。在有狀態的作業中，系統會跨多個資料列或時間間隔保留擷取的資料狀態，以便計算準確的結果。
* 使用 [`APPENDS`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/time-series-functions?hl=zh-tw#appends) 變更記錄函式，處理特定時間點附加的資料。
* 使用[`CHANGES`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/time-series-functions?hl=zh-tw#changes)
  變更記錄函式處理變更的資料，包括從特定時間點[匯出資料至 Pub/Sub](https://docs.cloud.google.com/bigquery/docs/export-to-pubsub?hl=zh-tw) 時的附加和變動。
  不過，使用[有狀態作業](https://docs.cloud.google.com/bigquery/docs/continuous-queries-introduction?hl=zh-tw#supported_stateful_operations)時，系統不支援 `CHANGES`。

## 支援的有狀態作業

**預覽**

這項功能適用《[服務專屬條款](https://docs.cloud.google.com/terms/service-terms?hl=zh-tw#1)》中「一般服務條款」一節的《正式發布前產品條款》。正式發布前功能是依「原樣」提供，支援服務可能受限。
詳情請參閱[推出階段說明](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages)。

如要尋求支援或針對這項功能提供意見回饋，請傳送電子郵件至 [bq-continuous-queries-feedback@google.com](mailto:bq-continuous-queries-feedback@google.com)。

有狀態作業可讓連續查詢執行複雜分析，這類分析需要保留多個資料列或時間間隔的資訊。無狀態函式會獨立處理每個資料列，有狀態作業則會維護擷取資料的狀態，以支援 [`JOIN`、匯總和視窗匯總](https://docs.cloud.google.com/bigquery/docs/continuous-queries?hl=zh-tw#join-agg-window-example)等函式。這項功能可讓您在查詢執行期間，將必要資料儲存在記憶體中，藉此關聯不同串流的事件，或計算一段時間內的指標 (例如 30 分鐘平均值)。

持續查詢支援下列有狀態作業：

* [JOIN](https://docs.cloud.google.com/bigquery/docs/continuous-query-joins?hl=zh-tw)
* [匯總和視窗化](https://docs.cloud.google.com/bigquery/docs/window-aggregations?hl=zh-tw)

## 授權

執行持續查詢作業時使用的[Google Cloud 存取權杖](https://docs.cloud.google.com/docs/authentication/token-types?hl=zh-tw#access-tokens)，如果是由使用者帳戶產生，存留時間 (TTL) 為兩天。因此，這類工作會在兩天後停止執行。服務帳戶產生的存取權杖可執行較長時間，但仍須遵守查詢執行時間上限。詳情請參閱「[使用服務帳戶執行持續查詢](https://docs.cloud.google.com/bigquery/docs/continuous-queries?hl=zh-tw#run_a_continuous_query_by_using_a_service_account)」。

## 位置

如要查看支援的區域清單，請參閱「[BigQuery 持續查詢位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw#continuous-query-loc)」。

## 限制

持續查詢必須遵循以下限制：

* 只有[預先發布版中的特定有狀態作業](#supported_stateful_operations)，才會維護擷取資料的狀態。雖然連續查詢現在支援某些類型的 `JOIN`、匯總和視窗匯總，但這些僅限於特定有狀態作業。系統僅支援特定類型的有狀態作業。
* 除非下列 SQL 功能列為[支援的具狀態作業](#supported_stateful_operations)，否則無法在持續查詢中使用：

  + 下列[查詢](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw)運算子：

    - [`PIVOT`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw#pivot_operator)
    - [`UNPIVOT`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw#unpivot_operator)
    - [`TABLESAMPLE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw#tablesample_operator)
  + 查詢[集合運算子](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw#set_operators)
  + [`SELECT DISTINCT` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw#select_distinct)
  + [`EXISTS` 或 `NOT EXISTS` 子查詢](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/subqueries?hl=zh-tw#exists_subquery_concepts)
  + [遞迴 CTE](https://docs.cloud.google.com/bigquery/docs/recursive-ctes?hl=zh-tw)
  + [使用者定義函式](https://docs.cloud.google.com/bigquery/docs/user-defined-functions?hl=zh-tw)
  + [window 函式呼叫](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/window-function-calls?hl=zh-tw)
  + [支援的功能](#supported_functionality)中未列出的 BigQuery ML 函式
  + [資料定義語言 (DDL) 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw)
  + [資料操縱語言 (DML) 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/dml-syntax?hl=zh-tw)，但 `INSERT` 除外。
  + [資料控制語言 (DCL) 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-control-language?hl=zh-tw)
  + 不以 Bigtable、Pub/Sub 或 Spanner 為目標的 `EXPORT DATA` 陳述式。
  + [程序語言](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/procedural-language?hl=zh-tw)
  + [偵錯陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/debugging-statements?hl=zh-tw)
* 持續查詢不支援下列資料來源：

  + [外部資料表](https://docs.cloud.google.com/bigquery/docs/external-data-sources?hl=zh-tw)。
  + [資訊結構定義檢視畫面](https://docs.cloud.google.com/bigquery/docs/information-schema-intro?hl=zh-tw)。
  + [Apache Iceberg 代管資料表](https://docs.cloud.google.com/bigquery/docs/iceberg-tables?hl=zh-tw)。
  + [萬用字元資料表](https://docs.cloud.google.com/bigquery/docs/querying-wildcard-tables?hl=zh-tw)。
  + [變更資料擷取 (CDC) 新增或更新](https://docs.cloud.google.com/bigquery/docs/change-data-capture?hl=zh-tw)
    資料。
  + [具體化檢視表](https://docs.cloud.google.com/bigquery/docs/materialized-views-intro?hl=zh-tw)。
  + 受其他持續查詢限制定義的[檢視區塊](https://docs.cloud.google.com/bigquery/docs/views?hl=zh-tw)，例如 `JOIN` 作業、匯總函式、user-defined function 或已啟用變更資料擷取的資料表。
* 持續查詢不支援[column-](https://docs.cloud.google.com/bigquery/docs/column-level-security-intro?hl=zh-tw)和[資料列層級](https://docs.cloud.google.com/bigquery/docs/row-level-security-intro?hl=zh-tw)安全功能。
* 持續查詢的輸出內容須遵守輸出目的地服務的固有配額和限制。
* 將資料匯出至 Bigtable、Spanner 或 [Pub/Sub 地理位置端點](https://docs.cloud.google.com/pubsub/docs/reference/service_apis_overview?hl=zh-tw#pubsub_endpoints)時，您只能以 Bigtable、Spanner 或 Pub/Sub 資源為目標，且這些資源必須與包含所查詢資料表的 BigQuery 資料集位於相同的 Google Cloud地區界線內。將資料匯出至 Pub/Sub 全域端點時，不適用這項限制。如要進一步瞭解如何匯出至 [Bigtable 應用程式設定檔](https://docs.cloud.google.com/bigtable/docs/app-profiles?hl=zh-tw)路由政策，請參閱[位置注意事項](https://docs.cloud.google.com/bigquery/docs/export-to-bigtable?hl=zh-tw#data-locations)。
* 您無法從[資料畫布](https://docs.cloud.google.com/bigquery/docs/data-canvas?hl=zh-tw)執行持續查詢。
* 持續查詢工作執行期間，您無法修改持續查詢中使用的 SQL。詳情請參閱「[修改持續查詢的 SQL](https://docs.cloud.google.com/bigquery/docs/continuous-queries?hl=zh-tw#modify_the_sql_of_a_continuous_query)」。
* 如果持續查詢工作在處理傳入資料時落後，且[輸出時間戳記延遲](https://docs.cloud.google.com/bigquery/docs/monitoring-dashboard?hl=zh-tw#metrics)超過 48 小時，就會失敗。您可以再次執行查詢，並使用 [`APPENDS`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/time-series-functions?hl=zh-tw#appends) 或 [`CHANGES`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/time-series-functions?hl=zh-tw#changes) 變更記錄函式，從您停止先前持續查詢工作時的時間點繼續處理。詳情請參閱「[從特定時間點開始持續查詢](https://docs.cloud.google.com/bigquery/docs/continuous-queries?hl=zh-tw#start_a_continuous_query_from_a_particular_point_in_time)」。
* 以使用者帳戶設定的持續查詢最多可執行兩天。透過服務帳戶設定的持續查詢最多可執行 150 天。達到查詢執行時間上限時，查詢會失敗並停止處理傳入資料。
* 雖然持續查詢是使用 [BigQuery 可靠性功能](https://docs.cloud.google.com/bigquery/docs/reliability-intro?hl=zh-tw)建構而成，但偶爾還是會發生暫時性問題。問題可能會導致系統自動重新處理部分持續查詢，進而造成持續查詢輸出內容出現重複資料。請設計下游系統來處理這類情況。

### 預訂限制

* 您必須建立 Enterprise 或 Enterprise Plus 版本[預留](https://docs.cloud.google.com/bigquery/docs/reservations-intro?hl=zh-tw)，才能執行連續查詢。連續查詢不支援隨選運算計費模式。
* 建立`CONTINUOUS`
  [預留項目指派](https://docs.cloud.google.com/bigquery/docs/reservations-assignments?hl=zh-tw)時，相關聯的預留項目最多只能有 500 個運算單元。如要提高這項限制，請傳送電子郵件至 [bq-continuous-queries-feedback@google.com](mailto:bq-continuous-queries-feedback@google.com)。
* 您無法在與持續查詢預留項目指派相同的預留項目中，建立使用不同[工作類型](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#assignments)的預留項目指派。
* 您無法設定持續查詢的並行作業。BigQuery 會根據使用 `CONTINUOUS` 工作類型的可用保留項目指派作業，自動決定可同時執行的連續查詢數量。
* 使用相同預留項目執行多項持續查詢時，個別工作可能無法公平分配可用資源，如 [BigQuery 公平性](https://docs.cloud.google.com/bigquery/docs/slots?hl=zh-tw#fair_scheduling_in_bigquery)所定義。

## 運算單元自動調度資源

持續查詢可使用[運算單元自動調度資源](https://docs.cloud.google.com/bigquery/docs/slots-autoscaling-intro?hl=zh-tw)功能，動態調整分配的容量，以因應工作負載。隨著持續查詢工作負載的增減，BigQuery 會動態調整運算單元。

持續查詢開始執行後，會主動*監聽*傳入資料，這會耗用 Slot 資源。如果保留項目正在執行持續查詢，不會縮減至零個時段。不過，如果持續查詢處於閒置狀態，主要是在監聽傳入資料，預期會消耗最少的時段，通常約 1 個時段。

## 閒置運算單元共用

持續查詢可使用[閒置運算單元共用](https://docs.cloud.google.com/bigquery/docs/slots?hl=zh-tw#idle_slots)功能，與其他預留項目和[作業類型](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#assignments)共用未使用的運算單元資源。

* 您仍須`CONTINUOUS`
  [指派預留項目](https://docs.cloud.google.com/bigquery/docs/reservations-assignments?hl=zh-tw)，才能執行持續查詢，且不能只依賴其他預留項目的閒置運算單元。因此，`CONTINUOUS` 預留項目指派作業需要非零的運算單元基準，或非零的運算單元自動調度資源設定。
* 只有閒置的基準運算單元，或來自 `CONTINUOUS` 預留項目指派的承諾使用運算單元可以共用。[自動調度的運算單元](https://docs.cloud.google.com/bigquery/docs/slots-autoscaling-intro?hl=zh-tw)無法做為其他預留項目的閒置運算單元共用。

## 定價

持續查詢會採用 [BigQuery 容量運算定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#capacity_compute_analysis_pricing)，並以[運算單元](https://docs.cloud.google.com/bigquery/docs/slots?hl=zh-tw)為單位計算。如要執行連續查詢，您必須擁有使用 [Enterprise 或 Enterprise Plus 版本](https://docs.cloud.google.com/bigquery/docs/editions-intro?hl=zh-tw)的[預留位置](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw)，以及使用 `CONTINUOUS` 工作類型的[預留位置指派](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#assignments)。

使用其他 BigQuery 資源 (例如資料擷取和儲存空間) 時，系統會按照[BigQuery 定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw)頁面顯示的費率計費。

如果使用其他服務接收持續查詢結果，或在持續查詢處理期間呼叫其他服務，系統會按照這些服務的公開費率收費。如要瞭解其他 Google Cloud 服務的定價，請參閱下列主題：

* [Bigtable 定價](https://cloud.google.com/bigtable/pricing?hl=zh-tw)
* [Pub/Sub 定價](https://cloud.google.com/pubsub/pricing?hl=zh-tw)
* [Spanner 定價](https://cloud.google.com/spanner/pricing?hl=zh-tw)
* [Vertex AI 定價](https://cloud.google.com/vertex-ai/pricing?hl=zh-tw)

## 後續步驟

請嘗試[建立持續查詢](https://docs.cloud.google.com/bigquery/docs/continuous-queries?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-06 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-06 (世界標準時間)。"],[],[]]