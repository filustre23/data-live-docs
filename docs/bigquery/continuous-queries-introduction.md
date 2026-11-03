Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

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

BigQuery 持續查詢是會不斷執行的 SQL 陳述式，持續查詢功能可即時分析傳入 BigQuery 的資料。您可以將持續查詢產生的輸出資料列，寫入或匯出至下列目的地：

* BigQuery 資料表
* [Apache Iceberg 代管資料表](https://docs.cloud.google.com/bigquery/docs/biglake-iceberg-tables-in-bigquery?hl=zh-tw)
* Pub/Sub 主題
* Bigtable 資料表
* Spanner 資料表

持續查詢可透過下列任一方法，處理寫入[標準 BigQuery 資料表](https://docs.cloud.google.com/bigquery/docs/tables-intro?hl=zh-tw#standard-tables)或 [Apache Iceberg 代管資料表](https://docs.cloud.google.com/bigquery/docs/biglake-iceberg-tables-in-bigquery?hl=zh-tw)的資料：

* [BigQuery Storage Write API (gRPC)](https://docs.cloud.google.com/bigquery/docs/write-api?hl=zh-tw)
* [BigQuery Storage Write API (REST)](https://docs.cloud.google.com/bigquery/docs/streaming-data-into-bigquery?hl=zh-tw)
* [批次載入](https://docs.cloud.google.com/bigquery/docs/batch-loading-data?hl=zh-tw)
* [`INSERT` DML 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/dml-syntax?hl=zh-tw#insert_statement)
* [將資料匯出至 Pub/Sub](https://docs.cloud.google.com/bigquery/docs/export-to-pubsub?hl=zh-tw) 時，會變更[資料操縱語言 (DML) 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/dml-syntax?hl=zh-tw)，例如 `DELETE`、`UPDATE` 和 `MERGE`。
* 將[批次查詢結果寫入永久資料表](https://docs.cloud.google.com/bigquery/docs/writing-results?hl=zh-tw#permanent-table)
* [將 BigQuery 持續查詢結果寫入永久資料表](https://docs.cloud.google.com/bigquery/docs/continuous-queries?hl=zh-tw#write-bigquery)
* [Pub/Sub BigQuery 訂閱項目](https://docs.cloud.google.com/pubsub/docs/bigquery?hl=zh-tw)
* 從 [Dataflow 寫入 BigQuery](https://docs.cloud.google.com/dataflow/docs/guides/write-to-bigquery?hl=zh-tw)
* 使用[僅限附加寫入模式](https://docs.cloud.google.com/datastream/docs/destination-bigquery?hl=zh-tw#append-only_write_mode)，從 Datastream 寫入 BigQuery

您可以使用持續查詢執行具時效性的工作，例如建立並立即根據洞察資料採取行動、套用即時機器學習 (ML) 推論，以及將資料複製到其他平台。這樣一來，您就能將 BigQuery 做為事件導向的資料處理引擎，用於應用程式的決策邏輯。

下圖顯示常見的持續查詢工作流程：

## 用途

以下是可能需要使用持續查詢的常見用途：

* **個人化客戶互動服務**：使用生成式 AI，為每次客戶互動建立量身打造的訊息。
* **異常偵測**：建構解決方案，即時偵測複雜資料中的異常狀況和威脅，以便更快因應問題。
* **可自訂的事件導向管道**：將持續查詢與 Pub/Sub 整合，根據傳入的資料觸發下游應用程式。
* **資料充實和實體擷取**：使用 SQL 函式和機器學習模型，透過持續查詢執行即時資料充實和轉換。
* **反向擷取、轉換和載入 (ETL)**：執行即時反向 ETL，將資料載入其他更適合低延遲應用程式服務的儲存系統。例如，分析或強化寫入 BigQuery 的事件資料，然後串流至 Bigtable、Spanner 或 Apache Iceberg 代管資料表，供應用程式使用。
* **自動觸發代理**：根據即時資料串流中偵測到的複雜事件，即時觸發代理資料管道。如需範例，請參閱「[使用 BigQuery 和 Agent Development Kit (ADK) 建構事件導向的資料代理](https://codelabs.developers.google.com/bigquery-adk-event-driven-agents?hl=zh-tw)」程式碼實驗室。
* **自主代理監控**：使用 [BigQuery 代理數據分析外掛程式](https://adk.dev/integrations/bigquery-agent-analytics/)，開發即時自動監控和警示功能，用於即時代理互動。此外掛程式會將所有代理追蹤資料、工具使用情形和作業記錄直接串流至 BigQuery，深入觀測 AI 員工。

## 支援的功能

持續查詢支援下列作業：

* 執行 [`INSERT` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/dml-syntax?hl=zh-tw#insert_statement)，將持續查詢的資料寫入 BigQuery 資料表或 [Iceberg 代管資料表](https://docs.cloud.google.com/bigquery/docs/biglake-iceberg-tables-in-bigquery?hl=zh-tw)。
* 執行 [`EXPORT DATA` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/export-statements?hl=zh-tw)，將持續查詢輸出內容[發布](https://docs.cloud.google.com/pubsub/docs/publish-message-overview?hl=zh-tw)至 Pub/Sub 主題。

  將資料匯出至 Pub/Sub 的持續查詢，必須使用[服務帳戶](https://docs.cloud.google.com/bigquery/docs/continuous-queries?hl=zh-tw#run_a_continuous_query_by_using_a_service_account)執行。詳情請參閱「[將資料匯出至 Pub/Sub](https://docs.cloud.google.com/bigquery/docs/export-to-pubsub?hl=zh-tw)」。

  您可以將 Pub/Sub 主題中的資料用於其他服務，例如使用 Dataflow 執行串流分析，或在 Application Integration 工作流程中使用資料。
* 執行 `EXPORT DATA` 陳述式，將資料從 BigQuery 匯出至 [Bigtable 資料表](https://docs.cloud.google.com/bigtable/docs/managing-tables?hl=zh-tw)。詳情請參閱「[將資料匯出至 Bigtable](https://docs.cloud.google.com/bigquery/docs/export-to-bigtable?hl=zh-tw)」。
* 執行 `EXPORT DATA` 陳述式，將資料從 BigQuery 匯出至 Spanner 資料表。詳情請參閱「[將資料匯出至 Spanner (反向 ETL)](https://docs.cloud.google.com/bigquery/docs/export-to-spanner?hl=zh-tw)」。
* 呼叫下列生成式 AI 函式：

  + [`AI.GENERATE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-ai-generate?hl=zh-tw)
  + [`AI.GENERATE_TEXT`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-ai-generate-text?hl=zh-tw)

    - 如要使用這項函式，您必須在 [Gemini Enterprise Agent Platform 模型](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/learn/models?hl=zh-tw)上建立 [BigQuery ML 遠端模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model?hl=zh-tw)。
* 呼叫下列 AI 函式：

  + [`ML.UNDERSTAND_TEXT`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-understand-text?hl=zh-tw)
  + [`ML.TRANSLATE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-translate?hl=zh-tw)

  您必須具備 Cloud AI API 上的 [BigQuery ML 遠端模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model-service?hl=zh-tw)，才能使用這些函式。
* 使用 [`ML.NORMALIZER` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-normalizer?hl=zh-tw)正規化數值型資料。
* 分析及處理 `JSON` 資料，包括支援 [JSON 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/json_functions?hl=zh-tw)和 [JSON 取消巢狀結構](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw#unnest_operator)。
* 使用無狀態 GoogleSQL 函式，例如[轉換函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/conversion_functions?hl=zh-tw)。在無狀態函式中，每個資料列的處理方式都與資料表中的其他資料列無關。
* 使用[有狀態作業](https://docs.cloud.google.com/bigquery/docs/continuous-queries-introduction?hl=zh-tw#supported_stateful_operations)，例如 [`JOIN`、匯總和視窗匯總](https://docs.cloud.google.com/bigquery/docs/continuous-queries?hl=zh-tw#join-agg-window-example)。在有狀態作業中，系統會保留多個資料列或時間間隔內擷取資料的狀態，以便計算準確的結果。
* 使用 [`APPENDS`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/time-series-functions?hl=zh-tw#appends) 變更記錄函式，從標準 BigQuery 資料表或 [Apache Iceberg 代管資料表](https://docs.cloud.google.com/bigquery/docs/biglake-iceberg-tables-in-bigquery?hl=zh-tw)的特定時間點處理附加資料。
* [將資料匯出至 Pub/Sub](https://docs.cloud.google.com/bigquery/docs/export-to-pubsub?hl=zh-tw) 時，使用 [`CHANGES`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/time-series-functions?hl=zh-tw#changes) 變更記錄函式，處理特定時間點後的變更資料，包括附加和變動。不過，使用[有狀態作業](https://docs.cloud.google.com/bigquery/docs/continuous-queries-introduction?hl=zh-tw#supported_stateful_operations)或查詢 [Iceberg 代管資料表](https://docs.cloud.google.com/bigquery/docs/biglake-iceberg-tables-in-bigquery?hl=zh-tw)時，不支援 `CHANGES`。
* 查詢[檢視表](https://docs.cloud.google.com/bigquery/docs/views?hl=zh-tw)，前提是檢視表的基礎 SQL 查詢是有效的持續查詢。

## 支援的有狀態作業

**預覽**

這項功能適用《[服務專屬條款](https://docs.cloud.google.com/terms/service-terms?hl=zh-tw#1)》中「一般服務條款」一節的《正式發布前產品條款》。正式發布前功能是依「原樣」提供，支援服務可能受限。
詳情請參閱[推出階段說明](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages)。

如要尋求支援或針對這項功能提供意見回饋，請傳送電子郵件至 [bq-continuous-queries-feedback@google.com](mailto:bq-continuous-queries-feedback@google.com)。

有狀態作業可讓持續查詢執行複雜分析，這類分析需要保留多個資料列或時間間隔的資訊。無狀態函式會獨立處理每一列，而有狀態作業則會維護擷取資料的狀態，以支援 [`JOIN`、匯總和視窗匯總](https://docs.cloud.google.com/bigquery/docs/continuous-queries?hl=zh-tw#join-agg-window-example)等函式。這項功能可讓您在查詢執行期間，將必要資料儲存在記憶體中，藉此建立不同串流事件之間的關聯，或計算一段時間內的指標 (例如 30 分鐘平均值)。

持續查詢支援下列有狀態作業：

* [JOIN](https://docs.cloud.google.com/bigquery/docs/continuous-query-joins?hl=zh-tw)
* [匯總和時間範圍](https://docs.cloud.google.com/bigquery/docs/window-aggregations?hl=zh-tw)
* [UNION ALL](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw#union)

## 授權

執行持續查詢工作時使用的[Google Cloud 存取權杖](https://docs.cloud.google.com/docs/authentication/token-types?hl=zh-tw#access-tokens)，如果是由使用者帳戶產生，存留時間 (TTL) 為兩天。因此，這類工作會在兩天後停止執行。服務帳戶產生的存取權杖可以執行更長時間，但仍須遵守查詢執行時間上限。詳情請參閱「[使用服務帳戶執行持續查詢](https://docs.cloud.google.com/bigquery/docs/continuous-queries?hl=zh-tw#run_a_continuous_query_by_using_a_service_account)」。

## 位置

如需支援的地區清單，請參閱「[BigQuery 持續查詢位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw#continuous-query-loc)」。

## 限制

持續查詢有下列限制：

* 系統只會針對[預先發布版中的特定有狀態作業](#supported_stateful_operations)，維護擷取資料的狀態。雖然持續查詢現在支援某些類型的 `JOIN`、匯總和視窗匯總，但僅限於特定有狀態作業。並非所有類型的有狀態作業都支援。
* 除非下列 SQL 功能列為[支援的有狀態作業](#supported_stateful_operations)，否則無法在持續查詢中使用：

  + 下列[查詢](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw)運算子：

    - [`PIVOT`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw#pivot_operator)
    - [`UNPIVOT`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw#unpivot_operator)
    - [`TABLESAMPLE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw#tablesample_operator)
  + 查詢[集合運算子](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw#set_operators) (`UNION ALL` 除外)。
  + [`SELECT DISTINCT` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw#select_distinct)
  + [`EXISTS` 或 `NOT EXISTS` 子查詢](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/subqueries?hl=zh-tw#exists_subquery_concepts)
  + [遞迴 CTE](https://docs.cloud.google.com/bigquery/docs/recursive-ctes?hl=zh-tw)
  + [user-defined function](https://docs.cloud.google.com/bigquery/docs/user-defined-functions?hl=zh-tw)
  + [視窗函式呼叫](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/window-function-calls?hl=zh-tw)
  + 「[支援的功能](#supported_functionality)」一節未列出的 BigQuery ML 函式
  + [資料定義語言 (DDL) 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw)
  + [data manipulation language (DML) 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/dml-syntax?hl=zh-tw)，但 `INSERT` 除外。
  + [資料控制語言 (DCL) 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-control-language?hl=zh-tw)
  + 不指定 Bigtable、Pub/Sub 或 Spanner 的 `EXPORT DATA` 陳述式。
  + [程序語言](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/procedural-language?hl=zh-tw)
  + [偵錯陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/debugging-statements?hl=zh-tw)
* 持續查詢不支援下列資料來源：

  + [外部資料表](https://docs.cloud.google.com/bigquery/docs/external-data-sources?hl=zh-tw)。
  + [資訊結構定義檢視表](https://docs.cloud.google.com/bigquery/docs/information-schema-intro?hl=zh-tw)。
  + [Wildcard 資料表](https://docs.cloud.google.com/bigquery/docs/querying-wildcard-tables?hl=zh-tw)。
  + [變更資料擷取 (CDC) upsert](https://docs.cloud.google.com/bigquery/docs/change-data-capture?hl=zh-tw) 資料。
  + [materialized view](https://docs.cloud.google.com/bigquery/docs/materialized-views-intro?hl=zh-tw)。
  + 基礎 SQL 查詢使用不支援功能的[檢視表](https://docs.cloud.google.com/bigquery/docs/views?hl=zh-tw)，例如使用者定義函式、外部資料表或啟用 CDC 的資料表。
* 持續查詢不支援[column-](https://docs.cloud.google.com/bigquery/docs/column-level-security-intro?hl=zh-tw)和[資料列層級](https://docs.cloud.google.com/bigquery/docs/row-level-security-intro?hl=zh-tw)安全防護功能。
* 持續查詢的輸出內容受限於輸出內容匯出目標服務的固有配額和限制。
* 將資料匯出至 Bigtable、Spanner 或 [Pub/Sub 位置端點](https://docs.cloud.google.com/pubsub/docs/reference/service_apis_overview?hl=zh-tw#pubsub_endpoints)時，只能指定與 BigQuery 資料集位於相同 Google Cloud區域邊界的 Bigtable、Spanner 或 Pub/Sub 資源，該資料集包含您查詢的資料表。將資料匯出至 Pub/Sub 全域端點時，則不受這項限制。如要進一步瞭解如何匯出至 [Bigtable 應用程式設定檔](https://docs.cloud.google.com/bigtable/docs/app-profiles?hl=zh-tw)路由政策，請參閱「[位置考量事項](https://docs.cloud.google.com/bigquery/docs/export-to-bigtable?hl=zh-tw#data-locations)」。
* 您無法從[資料畫布](https://docs.cloud.google.com/bigquery/docs/data-canvas?hl=zh-tw)執行持續查詢。
* 持續查詢工作執行期間，您無法修改持續查詢使用的 SQL。詳情請參閱「[修改持續查詢的 SQL](https://docs.cloud.google.com/bigquery/docs/continuous-queries?hl=zh-tw#modify_the_sql_of_a_continuous_query)」。
* 如果持續查詢工作處理傳入資料的速度落後，且[輸出浮水印延遲時間](https://docs.cloud.google.com/bigquery/docs/monitoring-dashboard?hl=zh-tw#metrics)超過 48 小時，就會失敗。您可以再次執行查詢，並使用 [`APPENDS`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/time-series-functions?hl=zh-tw#appends) 或 [`CHANGES`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/time-series-functions?hl=zh-tw#changes) 變更記錄函式，從上次停止持續查詢工作的時間點繼續處理。詳情請參閱「[從特定時間點開始持續查詢](https://docs.cloud.google.com/bigquery/docs/continuous-queries?hl=zh-tw#start_a_continuous_query_from_a_particular_point_in_time)」。
* 使用使用者帳戶設定的持續查詢，最多可執行兩天。設定服務帳戶後，持續查詢最多可執行 150 天。達到查詢執行時間上限時，查詢就會失敗，並停止處理傳入的資料。
* 雖然持續查詢是使用 [BigQuery 可靠性功能](https://docs.cloud.google.com/bigquery/docs/reliability-intro?hl=zh-tw)建構，但有時仍可能發生暫時性問題。問題可能會導致持續查詢自動重新處理，進而造成持續查詢輸出內容中出現重複資料。設計下游系統時，請考量這類情況。

### 預留項目限制

* 您必須建立 Enterprise 或 Enterprise Plus 版本的[預留項目](https://docs.cloud.google.com/bigquery/docs/reservations-intro?hl=zh-tw)，並使用 [`CONTINUOUS` 指派類型](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#assignments)，才能執行持續查詢。持續查詢不支援隨選運算計費模式。
* 建立`CONTINUOUS`
  [預留項目指派作業](https://docs.cloud.google.com/bigquery/docs/reservations-assignments?hl=zh-tw)時，相關聯的預留項目最多只能有 500 個運算單元。如要申請提高這項限制，請與 [bq-continuous-queries-feedback@google.com](mailto:bq-continuous-queries-feedback@google.com) 聯絡。
* 您無法建立預留項目指派作業，在與持續查詢預留項目指派作業相同的預留項目中，使用不同的[工作類型](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#assignments)。
* BigQuery 會根據使用 `CONTINUOUS` 工作類型的預留項目指派作業設定大小，決定每項專案可同時執行的持續查詢數量。如要接受新工作，BigQuery 要求每項持續查詢工作至少要有 10 個運算單元。在正常執行期間，查詢不一定會耗用所有 10 個運算單元。這項門檻可確保每項執行中的持續查詢，都能維持足夠的基準運算能力，處理突然增加的傳入資料量，不會落後或影響低延遲處理。

  為確保查詢順利執行，且不會達到並行限制，建議您使用[運算單元自動調度資源](#slots_autoscaling)功能。啟用自動調度資源功能後，整體運算單元用量會根據實際資源需求動態調整。您可以設定較小的基準預留項目，並設定自動調度資源上限，輕鬆涵蓋預期並行查詢的每項查詢 10 個運算單元門檻。
* 使用相同預留項目執行多項持續查詢時，個別工作可能無法按照 [BigQuery 公平性](https://docs.cloud.google.com/bigquery/docs/slots?hl=zh-tw#fair_scheduling_in_bigquery)定義，公平分配可用資源。

## 運算單元自動調整資源配置

持續查詢可使用[運算單元自動調度資源](https://docs.cloud.google.com/bigquery/docs/slots-autoscaling-intro?hl=zh-tw)功能，動態調整分配的容量，以因應工作負載。隨著持續查詢工作負載增減，BigQuery 會動態調整運算單元。

持續查詢開始執行後，會主動*監聽*傳入的資料，這會耗用運算單元資源。雖然預留項目在執行持續查詢時，不會縮減至零個運算單元，但主要監聽傳入資料的閒置持續查詢，預計會耗用極少量的運算單元，通常約為 1 個運算單元。

## 閒置運算單元共用

持續查詢可使用[閒置運算單元共用](https://docs.cloud.google.com/bigquery/docs/slots?hl=zh-tw#idle_slots)功能，與其他預留項目和[工作類型](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#assignments)共用未使用的運算單元資源。

* 您仍須[指派預留項目](https://docs.cloud.google.com/bigquery/docs/reservations-assignments?hl=zh-tw)`CONTINUOUS`，才能執行持續查詢，無法只依賴其他預留項目的閒置運算單元。因此，`CONTINUOUS` 預留項目指派作業需要非零的運算單元基準，或非零的運算單元自動調度資源設定。
* 只有閒置的基準運算單元，或 `CONTINUOUS` 預留項目指派作業中的承諾使用運算單元，才能共用。[自動調度資源的運算單元](https://docs.cloud.google.com/bigquery/docs/slots-autoscaling-intro?hl=zh-tw)無法做為其他預留項目的閒置運算單元共用。

## 定價

持續查詢可以使用 [BigQuery 流暢擴充](https://docs.cloud.google.com/bigquery/docs/slots?hl=zh-tw#fluid-scaling)。

持續查詢採用 [BigQuery 運算資源運算定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#capacity_compute_analysis_pricing)，以[運算單元](https://docs.cloud.google.com/bigquery/docs/slots?hl=zh-tw)為單位。如要執行持續查詢，您必須具備使用 [Enterprise 或 Enterprise Plus 版本](https://docs.cloud.google.com/bigquery/docs/editions-intro?hl=zh-tw)的[預留項目](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw)，以及使用 `CONTINUOUS` 工作類型的[預留項目指派作業](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#assignments)。

使用其他 BigQuery 資源 (例如資料擷取和儲存) 時，則按照 [BigQuery 定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw)頁面顯示的費率計費。

如果其他服務會接收持續查詢結果，或在持續查詢處理期間遭到呼叫，則會按照這些服務的公告費率計費。如要瞭解持續查詢使用的其他 Google Cloud 服務定價，請參閱下列主題：

* [Bigtable 定價](https://cloud.google.com/bigtable/pricing?hl=zh-tw)
* [Pub/Sub 定價](https://cloud.google.com/pubsub/pricing?hl=zh-tw)
* [Spanner 定價](https://cloud.google.com/spanner/pricing?hl=zh-tw)
* [Agent Platform 定價](https://cloud.google.com/vertex-ai/pricing?hl=zh-tw)

### 估算運算單元容量需求

由於每個工作負載都不同，因此通常無法預先準確估算持續查詢所需的運算單元。持續查詢所需的運算單元數量取決於多項因素：

* 同時執行的持續查詢數量。
* SQL 陳述式的複雜度。
* 使用有狀態處理函式，包括視窗時間長度、`JOIN` 和匯總。
* 資料傳入的速率或速度。
* 擷取資料的結構和大小。

概念上，您可以根據持續查詢工作負載，估算所需的運算單元總數：

*預估運算單元 ≈ 持續查詢數量 x ∑ (資料速率 x 查詢複雜度)*

由於實際運算單元用量很大程度上取決於您的特定工作負載和資料模式，因此最準確的費用預估方法是監控執行中的工作。您可以使用 `INFORMATION_SCHEMA` 檢視表，評估獨立持續查詢執行的尖峰運算單元用量。如需詳細操作說明和查詢範例，瞭解如何追蹤一段時間內的運算單元用量，請參閱「[查看運算單元消耗資訊](https://docs.cloud.google.com/bigquery/docs/continuous-queries-monitor?hl=zh-tw#view_slot_consumption_information)」。

## 後續步驟

請嘗試[建立持續查詢](https://docs.cloud.google.com/bigquery/docs/continuous-queries?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-11-02 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-11-02 (世界標準時間)。"],[],[]]