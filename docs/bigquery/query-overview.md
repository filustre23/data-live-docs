Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# BigQuery 數據分析總覽

本文說明 BigQuery 如何處理查詢，並概略介紹有助於瞭解及分析資料的幾項功能。

BigQuery 經過最佳化調整，能對大型資料集執行分析查詢，包括在幾秒內查詢 TB 級資料，以及在幾分鐘內查詢 PB 級資料。瞭解這項服務的功能和查詢處理方式，有助於您充分發揮資料分析投資效益。

## 分析工作流程

BigQuery 支援多種資料分析工作流程：

* **臨時分析。**BigQuery 使用 [GoogleSQL](https://docs.cloud.google.com/bigquery/docs/introduction-sql?hl=zh-tw) (BigQuery 中的 SQL 語法) 支援即時分析。您可以在 Google Cloud 控制台中執行查詢，也可以透過與 BigQuery 整合的[第三方工具](https://docs.cloud.google.com/bigquery/docs/query-overview?hl=zh-tw#third-party_tool_integration)執行查詢。
* **地理空間分析**。BigQuery 使用地理資料類型和 GoogleSQL 地理函式，讓您分析及視覺化地理空間資料。如要瞭解這些資料類型和函式，請參閱「[地理空間分析簡介](https://docs.cloud.google.com/bigquery/docs/geospatial-intro?hl=zh-tw)」。
* **圖形分析。**[BigQuery Graph](https://docs.cloud.google.com/bigquery/docs/graph-overview?hl=zh-tw) 可讓您將資料建模為具有節點和邊緣的圖。您可以使用 Graph Query Language (GQL) 找出資料點之間複雜且隱藏的關係，這類關係很難使用 SQL 找出。
* **搜尋資料。**您可以[為資料建立索引](https://docs.cloud.google.com/bigquery/docs/search-index?hl=zh-tw)，對非結構化文字或半結構化 JSON 資料執行彈性且最佳化的[搜尋](https://docs.cloud.google.com/bigquery/docs/search?hl=zh-tw)。
* **搜尋 Google Cloud 資源。**使用[自然語言搜尋](https://docs.cloud.google.com/bigquery/docs/search-resources?hl=zh-tw) ([搶先版](https://cloud.google.com/products?hl=zh-tw#product-launch-stages)) 在 BigQuery 中探索 Google Cloud 資源。
* **機器學習。**[BigQuery ML](https://docs.cloud.google.com/bigquery/docs/bqml-introduction?hl=zh-tw)
  可讓您使用 GoogleSQL 查詢，在 BigQuery 中建立及執行機器學習 (ML) 模型。
* **商業智慧。**[BigQuery BI Engine](https://docs.cloud.google.com/bigquery/docs/bi-engine-intro?hl=zh-tw) 是一種快速的記憶體內分析服務，可讓您建構豐富的互動式資訊主頁和報表，且不會影響效能、擴充性、安全性或資料更新間隔。
* **AI 輔助。**您可以使用 [Gemini in BigQuery](https://docs.cloud.google.com/bigquery/docs/gemini-overview?hl=zh-tw) 準備及探索資料、生成 SQL 查詢和 Python 程式碼，並以視覺化方式呈現結果。

## 資料探索

在開始編寫 SQL 查詢之前，BigQuery 可協助您瞭解資料。如果您想尋找資料、不熟悉資料、不知道要問哪些問題，或是需要撰寫 SQL 的協助，請使用下列功能：

* [**知識目錄**](https://docs.cloud.google.com/bigquery/docs/search-resources?hl=zh-tw)。在 BigQuery 中尋找Google Cloud 資源，例如資料集和資料表。
* [**資料表探索工具**](https://docs.cloud.google.com/bigquery/docs/table-explorer?hl=zh-tw)。以視覺化方式探索表格中的值範圍和頻率，並以互動方式建構查詢。
* [**資料洞察。**](https://docs.cloud.google.com/bigquery/docs/data-insights?hl=zh-tw)生成有關資料的自然語言問題，以及回答這些問題的 SQL 查詢。
* [**資料剖析掃描。**](https://docs.cloud.google.com/bigquery/docs/data-profile-scan?hl=zh-tw)查看資料的統計特徵，包括平均值、不重複值、最大值和最小值。
* [**資料畫布。**](https://docs.cloud.google.com/bigquery/docs/data-canvas?hl=zh-tw)使用自然語言查詢資料、以圖表呈現結果，以及提出後續問題。

## 查詢

在 BigQuery 中分析資料的主要方式是[執行 SQL 查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw)。[GoogleSQL 方言](https://docs.cloud.google.com/bigquery/docs/introduction-sql?hl=zh-tw)支援 [SQL:2011](https://www.iso.org/standard/53681.html)，並包含支援地理空間分析和機器學習的擴充功能。

### 資料來源

BigQuery 可讓您查詢下列類型的資料來源：

* **儲存在 BigQuery 中的資料。**您可以[將資料載入 BigQuery](https://docs.cloud.google.com/bigquery/docs/loading-data?hl=zh-tw)、使用[資料操作語言 (DML) 陳述式](https://docs.cloud.google.com/bigquery/docs/data-manipulation-language?hl=zh-tw)修改現有資料，或[將查詢結果寫入資料表](https://docs.cloud.google.com/bigquery/docs/writing-results?hl=zh-tw)。您可以在時間回溯期內，[查詢特定時間點的歷來資料](https://docs.cloud.google.com/bigquery/docs/access-historical-data?hl=zh-tw)。

  您可以查詢儲存在單一區域或多區域位置的資料。如果查詢存取儲存在多個位置的資料，則可視為[全域查詢](https://docs.cloud.google.com/bigquery/docs/global-queries?hl=zh-tw) [(預覽版)](https://docs.cloud.google.com/products?hl=zh-tw#product-launch-stages)。
  即使一個區域是單一區域位置，另一個區域是包含單一區域位置的多區域位置，只要查詢參照多個位置的資料，一律會視為全域查詢。
* **外部資料。**您可以查詢各種外部資料來源，例如 Cloud Storage，或是 Spanner 或 Cloud SQL 等資料庫服務。如要瞭解如何設定外部來源的連線，請參閱「[外部資料來源簡介](https://docs.cloud.google.com/bigquery/docs/external-data-sources?hl=zh-tw)」
* **多雲端資料。**您可以查詢儲存在其他公有雲 (例如 AWS 或 Azure) 中的資料。如要瞭解如何設定與 Amazon Simple Storage Service (Amazon S3) 或 Azure Blob 儲存體的連線，請參閱「[BigQuery Omni 簡介](https://docs.cloud.google.com/bigquery/docs/omni-introduction?hl=zh-tw)」。
* **公開資料集**。您可以分析[公開資料集市集](https://docs.cloud.google.com/bigquery/public-data?hl=zh-tw)中的任何資料集。
* **BigQuery sharing (舊稱 Analytics Hub)。**您可以發布及訂閱 BigQuery 資料集和 Pub/Sub 主題，在機構界線之間共用資料。詳情請參閱 [BigQuery sharing 簡介](https://docs.cloud.google.com/bigquery/docs/analytics-hub-introduction?hl=zh-tw)。

### 查詢作業的類型

您可以使用下列其中一種查詢工作類型[查詢 BigQuery 資料](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw)：

* **[互動式查詢作業](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)**。根據預設，BigQuery 會以互動式查詢工作執行查詢，這類工作會盡快開始執行。
* **[批次查詢工作](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#batch)**。批次查詢的優先順序低於互動式查詢。如果專案或預訂項目已用盡所有可用的運算資源，批次查詢就更有可能排入佇列，並留在佇列中。批次查詢開始執行後，運作方式與互動式查詢相同。詳情請參閱「[查詢佇列](https://docs.cloud.google.com/bigquery/docs/query-queues?hl=zh-tw)」。
* **[持續查詢工作](https://docs.cloud.google.com/bigquery/docs/continuous-queries-introduction?hl=zh-tw)**。
  有了這些工作，查詢就會持續執行，讓您即時分析 BigQuery 中的輸入資料，然後將結果寫入 BigQuery 資料表，或將結果匯出至 Bigtable 或 Pub/Sub。您可以使用這項功能執行具時效性的工作，例如建立洞察資料並立即採取行動、套用即時機器學習 (ML) 推論，以及建構事件導向資料管道。

您可以使用下列方法執行查詢工作：

* 在[Google Cloud 控制台](https://docs.cloud.google.com/bigquery/bigquery-web-ui?hl=zh-tw#overview)中編寫及執行查詢。
* 在 [bq 指令列工具](https://docs.cloud.google.com/bigquery/bq-command-line-tool?hl=zh-tw)中執行 `bq query` 指令。
* 透過程式呼叫 BigQuery [REST API](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2?hl=zh-tw) 中的 [`jobs.query`](https://docs.cloud.google.com/bigquery/docs/reference/v2/jobs/query?hl=zh-tw) 或 [`jobs.insert`](https://docs.cloud.google.com/bigquery/docs/reference/v2/jobs/insert?hl=zh-tw) 方法。
* 使用 BigQuery [用戶端程式庫](https://docs.cloud.google.com/bigquery/docs/reference/libraries?hl=zh-tw)。

### 多陳述式查詢

您可以使用[多重陳述式查詢](https://docs.cloud.google.com/bigquery/docs/multi-statement-queries?hl=zh-tw)，依序執行多個陳述式並共用狀態。多重陳述式查詢通常用於[預存程序](https://docs.cloud.google.com/bigquery/docs/procedures?hl=zh-tw)，並支援[程序語言陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/procedural-language?hl=zh-tw)，可讓您定義變數及實作控制流程。

### 已儲存及共用的查詢

BigQuery 可讓您[儲存查詢](https://docs.cloud.google.com/bigquery/docs/work-with-saved-queries?hl=zh-tw#create_saved_queries)，以及與他人[共用查詢](https://docs.cloud.google.com/bigquery/docs/work-with-saved-queries?hl=zh-tw#share-saved-query)。

儲存查詢時，您可以將查詢設為不公開 (只有您可以檢視)、在專案層級共用 (特定主體可以檢視)，或是公開 (任何人都可以檢視)。詳情請參閱「[使用已儲存的查詢](https://docs.cloud.google.com/bigquery/docs/work-with-saved-queries?hl=zh-tw)」。

### BigQuery 如何處理查詢

BigQuery 執行查詢時會進行下列程序：

* **執行樹狀結構。**執行查詢時，BigQuery 會產生*執行樹狀結構*，將查詢分成多個階段。這些階段包含可平行執行的步驟。
* **隨機播放層級。**這些階段會透過快速的分散式*重組層級*來彼此通訊，並儲存階段工作人員產生的中繼資料。在允許的情況下，Shuffle 層會運用 Petabit 網路和 RAM 等技術，將資料快速移至工作節點。
* **查詢計畫**。BigQuery 取得執行查詢所需的所有資訊後，就會產生*查詢計畫*。您可以在 Google Cloud 控制台中[查看查詢計畫](https://docs.cloud.google.com/bigquery/docs/query-plan-explanation?hl=zh-tw)，並使用該計畫排解問題或[提升查詢效能](https://docs.cloud.google.com/bigquery/docs/best-practices-performance-compute?hl=zh-tw)。
* **查詢執行圖表。**您可以查看任何查詢 (無論是正在執行或已完成) 的圖形格式查詢計畫資訊，並查看[效能洞察](https://docs.cloud.google.com/bigquery/docs/query-insights?hl=zh-tw)，進一步最佳化查詢。
* **查詢監控和動態規劃。**除了執行查詢計畫本身工作的背景工作程序外，其他背景工作程序也會監控並引導整個系統的工作進度。隨著查詢進度，BigQuery 可能會動態調整查詢計畫，以配合各階段的結果。
* **查詢結果**。查詢完成後，BigQuery 會將結果寫入永久儲存空間，並傳回給使用者。這樣一來，下次執行查詢時，BigQuery 就能提供[快取結果](https://docs.cloud.google.com/bigquery/docs/cached-results?hl=zh-tw)。

### 查詢並行數和效能

在相同資料上重複執行的查詢，其效能可能會有所不同，這是因為 BigQuery 環境是共用的，而且會使用快取的查詢結果，或是在查詢執行期間動態調整查詢計畫。對於一般繁忙的系統 (同時執行許多查詢)，BigQuery 會使用多個程序來消除查詢效能的差異：

* BigQuery 會平行執行多個查詢，並可[將查詢排入佇列](https://docs.cloud.google.com/bigquery/docs/query-queues?hl=zh-tw)，等到資源可用時再執行。
* 查詢開始和結束時，BigQuery 會在新查詢和執行中的查詢之間公平地重新分配資源。這項程序可確保查詢效能不會取決於查詢的提交順序，而是取決於特定時間執行的查詢數量。

### 查詢最佳化

執行查詢時，您可以在 Google Cloud 控制台[查看查詢計畫](https://docs.cloud.google.com/bigquery/docs/query-insights?hl=zh-tw)。您也可以使用 [`INFORMATION_SCHEMA.JOBS*` 檢視畫面](https://docs.cloud.google.com/bigquery/docs/information-schema-jobs?hl=zh-tw)或 [`jobs.get` REST API 方法](https://docs.cloud.google.com/bigquery/docs/query-plan-explanation?hl=zh-tw#api_sample_representation)，要求執行詳細資料。

查詢計畫包含查詢階段和步驟的詳細資料。這些詳細資料可協助您找出提升查詢效能的方法。舉例來說，如果您發現某個階段寫入的輸出內容比其他階段多很多，可能表示您需要在查詢中更早進行篩選。

如要進一步瞭解查詢計畫和查詢最佳化，請參閱下列資源：

* 如要進一步瞭解查詢計畫，並查看計畫資訊如何協助您提升查詢效能的範例，請參閱「[查詢計畫和時間軸](https://docs.cloud.google.com/bigquery/docs/query-plan-explanation?hl=zh-tw)」。
* 如要進一步瞭解查詢最佳化，請參閱「[最佳化查詢效能簡介](https://docs.cloud.google.com/bigquery/docs/best-practices-performance-overview?hl=zh-tw)」。

### 查詢監控

如要在雲端執行可靠的應用程式，監控和記錄功能至關重要。BigQuery 工作負載也不例外，尤其是大量或對業務至關重要的工作負載。BigQuery 提供各種指標、記錄和中繼資料檢視畫面，協助您監控 BigQuery 用量。

詳情請參閱下列資源：

* 如要瞭解 BigQuery 的監控選項，請參閱「[BigQuery 監控簡介](https://docs.cloud.google.com/bigquery/docs/monitoring?hl=zh-tw)」。
* 如要瞭解稽核記錄和如何分析查詢行為，請參閱「[BigQuery 稽核記錄](https://docs.cloud.google.com/bigquery/docs/reference/auditlogs?hl=zh-tw)」一文。

### 查詢定價

BigQuery 提供兩種用於分析的計價模式：

* **[以量計價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#on_demand_pricing)。**
  您只需為查詢所掃描過的資料付費。每個專案都有固定的[查詢處理容量](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#max_concurrent_slots_on-demand)，費用則取決於處理的位元組數。
* **[以容量為準的定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#capacity_compute_analysis_pricing)。**
  購買查詢處理作業專用容量。

如要瞭解這兩種計費模式，以及如何預留以容量為準的計費方案，請參閱「[預留項目簡介](https://docs.cloud.google.com/bigquery/docs/reservations-intro?hl=zh-tw)」。

### 控管配額和查詢費用

BigQuery 會對執行查詢作業強制採用專案層級配額。如需查詢配額的相關資訊，請參閱[配額與限制](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)。

BigQuery 提供了多種選項來協助您控管查詢費用，包括自訂配額和帳單快訊。詳情請參閱[建立自訂的費用控管機制](https://docs.cloud.google.com/bigquery/docs/custom-quotas?hl=zh-tw)。

## 資料分析功能

BigQuery 支援描述性和預測分析，並可協助您透過 AI 輔助工具、SQL、機器學習、筆記本和其他第三方整合服務探索資料。

### BigQuery Studio

BigQuery Studio 提供下列功能，協助您探索、分析及對 BigQuery 中的資料執行推論：

* 功能強大的 [SQL 編輯器](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw)，可提供程式碼完成和生成、查詢驗證，以及處理的位元組估算。
* 使用 [Colab Enterprise](https://docs.cloud.google.com/colab/docs/introduction?hl=zh-tw) 建立的內嵌 [Python 筆記本](https://docs.cloud.google.com/bigquery/docs/notebooks-introduction?hl=zh-tw)。筆記本提供一鍵式 Python 開發執行階段，並內建 [BigQuery DataFrames](https://docs.cloud.google.com/python/docs/reference/bigframes/latest?hl=zh-tw) 支援功能。
* [PySpark 編輯器](https://docs.cloud.google.com/bigquery/docs/spark-procedures?hl=zh-tw#use-python-pyspark-editor)：可讓您建立 Apache Spark 的預存 Python 程序。
* 程式碼資產 (例如筆記本和[儲存的查詢](https://docs.cloud.google.com/bigquery/docs/saved-queries-introduction?hl=zh-tw)) 的資產管理和版本記錄，以 [Dataform](https://docs.cloud.google.com/dataform?hl=zh-tw) 為基礎。
* 在 SQL 編輯器和筆記本中輔助開發程式碼，以 [Gemini 生成式 AI](https://docs.cloud.google.com/bigquery/docs/write-sql-gemini?hl=zh-tw) 為基礎 ([搶先版](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages))。
* [Knowledge Catalog](https://docs.cloud.google.com/dataplex?hl=zh-tw) 功能，可進行[資料探索](https://docs.cloud.google.com/bigquery/docs/bigquery-web-ui?hl=zh-tw#search-page)、[資料剖析](https://docs.cloud.google.com/bigquery/docs/data-profile-scan?hl=zh-tw)，以及[資料品質](https://docs.cloud.google.com/bigquery/docs/data-quality-scan?hl=zh-tw)掃描。
* 可依使用者或專案查看[工作記錄](https://docs.cloud.google.com/bigquery/docs/bigquery-web-ui?hl=zh-tw#studio-overview)。
* 可連結 Looker 和 Google 試算表等其他工具，分析已儲存的查詢結果，並匯出已儲存的查詢結果，供其他應用程式使用。

**注意：**BigQuery Studio 需要下列 API，這些 API 會在 2024 年 3 月 24 日後建立的專案和自動化指令碼中預設啟用：

* [Compute Engine API](https://docs.cloud.google.com/compute/docs/reference/rest/v1?hl=zh-tw)
* [Analytics Hub API](https://docs.cloud.google.com/bigquery/docs/reference/analytics-hub/rest?hl=zh-tw)
* [Dataform API](https://docs.cloud.google.com/dataform/reference/rest?hl=zh-tw)
* [Vertex AI API](https://docs.cloud.google.com/vertex-ai/docs/reference/rest?hl=zh-tw)
* [BigQuery Connection API](https://docs.cloud.google.com/bigquery/docs/reference/bigqueryconnection/rest?hl=zh-tw)
* [BigQuery Data Policy API](https://docs.cloud.google.com/bigquery/docs/reference/bigquerydatapolicy/rest?hl=zh-tw)
* [BigQuery Reservation API](https://docs.cloud.google.com/bigquery/docs/reference/reservations/rest?hl=zh-tw)
* [Dataplex API](https://docs.cloud.google.com/dataplex/docs/reference/rest?hl=zh-tw)

### BigQuery ML

BigQuery ML 可讓您在 BigQuery 中使用 SQL 執行機器學習 (ML) 和預測分析。詳情請參閱 [BigQuery ML 簡介](https://docs.cloud.google.com/bigquery/docs/bqml-introduction?hl=zh-tw)。

[對話式數據分析代理](https://docs.cloud.google.com/bigquery/docs/conversational-analytics?hl=zh-tw)可讓您使用對話式語言與資料互動。這個代理程式包含一或多個資料來源，以及一組用於處理資料的特定用途指令。對話式數據分析支援使用[部分 BigQuery ML 函式](https://docs.cloud.google.com/bigquery/docs/conversational-analytics?hl=zh-tw#bigquery-ml-support)。

### 整合 Analytics 工具

除了在 BigQuery 中執行查詢，您也可以使用與 BigQuery 整合的各種分析和商業智慧工具分析資料，例如：

* **Looker**。Looker 是企業平台，提供商業智慧、資料應用程式和嵌入式分析服務。Looker 平台可與許多資料儲存庫搭配使用，包括 BigQuery。如要瞭解如何將 Looker 連線至 BigQuery，請參閱「[使用 Looker](https://docs.cloud.google.com/bigquery/docs/looker?hl=zh-tw)」。
* **數據分析**。查詢執行完畢後，您可以直接在Google Cloud 控制台的 BigQuery 中啟動 Google 數據分析。接著，您可以在數據分析中建立圖表，並探索查詢傳回的資料。如要瞭解數據分析，請參閱[數據分析總覽](https://lookerstudio.google.com/overview?hl=zh-tw)。
* **連結試算表**。您也可以在控制台中，直接從 BigQuery 啟動連結試算表。除了您要求之外，「連結試算表」也可以根據預先排定的時間表，在 BigQuery 中代替您執行查詢。這些查詢的結果會儲存在試算表中，方便您分析及共用資料。如要瞭解連結試算表，請參閱「[使用連結試算表](https://docs.cloud.google.com/bigquery/docs/connected-sheets?hl=zh-tw)」。
* **Tableau**。您可以[從 Tableau 連結至資料集](https://docs.cloud.google.com/bigquery/docs/analyze-data-tableau?hl=zh-tw)。使用 BigQuery 製作圖表、資訊主頁和其他資料視覺化內容。

### 整合第三方工具

多種第三方分析工具都支援 BigQuery。
舉例來說，您可以將 [Tableau](https://docs.cloud.google.com/bigquery/docs/analyze-data-tableau?hl=zh-tw) 連結至 BigQuery 資料，並使用其視覺化工具分析及分享分析結果。如要進一步瞭解使用第三方工具時的注意事項，請參閱[第三方工具整合](https://docs.cloud.google.com/bigquery/docs/third-party-integration?hl=zh-tw)。

您可以使用 ODBC 和 JDBC 驅動程式，將應用程式與 BigQuery 整合。這些驅動程式旨在協助使用者透過現有工具和基礎架構，運用 BigQuery 的強大功能。如要瞭解最新版本和已知問題，請參閱「[適用於 BigQuery 的 ODBC 和 JDBC 驅動程式](https://docs.cloud.google.com/bigquery/docs/reference/odbc-jdbc-drivers?hl=zh-tw)」。

您可以使用 pandas 程式庫 (例如 `pandas-gbq`) 在 Jupyter 筆記本中與 BigQuery 資料互動。如要瞭解這個程式庫，以及與使用 BigQuery [Python 用戶端程式庫](https://docs.cloud.google.com/bigquery/docs/reference/libraries?hl=zh-tw)的比較，請參閱「[與 `pandas-gbq` 比較](https://docs.cloud.google.com/bigquery/docs/pandas-gbq-migration?hl=zh-tw)」。

您也可以搭配其他筆記本和分析工具使用 BigQuery。詳情請參閱「[程式輔助分析工具](https://docs.cloud.google.com/bigquery/docs/programmatic-analysis?hl=zh-tw)」。

如需 BigQuery 數據分析和更廣泛技術合作夥伴的完整清單，請參閱 BigQuery 產品頁面的「[合作夥伴](https://docs.cloud.google.com/bigquery?hl=zh-tw#section-12)」清單。

## 後續步驟

* 如需簡介及支援的 SQL 陳述式總覽，請參閱「[BigQuery 中的 SQL 簡介](https://docs.cloud.google.com/bigquery/docs/introduction-sql?hl=zh-tw)」。
* 如要瞭解用於查詢 BigQuery 資料的 GoogleSQL 語法，請參閱「[GoogleSQL 中的查詢語法](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw)」。
* 瞭解如何在 BigQuery 中[執行查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw)。
* 進一步瞭解如何[盡可能提高查詢效能](https://docs.cloud.google.com/bigquery/docs/best-practices-performance-overview?hl=zh-tw)。
* 瞭解如何開始使用[筆記本](https://docs.cloud.google.com/bigquery/docs/programmatic-analysis?hl=zh-tw)。
* 瞭解如何[排定週期性查詢](https://docs.cloud.google.com/bigquery/docs/scheduling-queries?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-02 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-02 (世界標準時間)。"],[],[]]