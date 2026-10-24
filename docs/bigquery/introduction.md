Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# BigQuery 簡介

BigQuery 是內建 AI 的全代管資料平台，可協助您管理及分析資料。BigQuery 採用無伺服器架構，可讓您使用 SQL 和 Python 等語言，解答貴組織最棘手的問題，完全不需要管理基礎架構。

資料分析師、資料工程師、資料倉儲管理員或資料科學家，可將 BigQuery 用於下列主要用途：

* **AI 輔助工作流程：**運用生成式 AI、向量搜尋和 Gemini 輔助功能，探索、轉換大型語言模型 (LLM)，並將其整合至資料工作流程。
* **機器學習和預測分析：**使用 SQL 或 Python，根據資料建構、訓練及部署模型。
* **商業智慧和臨時分析：**在數秒和數分鐘內分別查詢 TB 和 PB 規模的資料，協助您做出重大業務決策。
* **地理空間分析：**使用地理資訊系統 (GIS) 分析位置資料，並以圖表呈現。
* **資料治理和語意搜尋：**使用 Knowledge Catalog 內建功能，探索、整理及驗證資料和 AI 資產。
* **持續擷取資料：**即時串流結構化和非結構化資料，並支援 Apache Iceberg、Delta 和 Apache Hudi 等開放資料表格式。

## BigQuery 架構

BigQuery 架構包含兩個部分：擷取、儲存及最佳化資料的儲存層，以及提供分析功能的運算層。Google 的 PB 級網路可讓運算和儲存層之間進行必要通訊，因此這些層級能獨立運作，效率不受影響。

舊版資料庫通常必須在讀取、寫入和分析作業之間共用資源。這可能會導致資源衝突，並在資料寫入或讀取儲存空間時，降低查詢速度。如果資料庫管理工作 (例如指派或撤銷權限) 需要資源，共用資源集區可能會進一步吃緊。BigQuery 的運算和儲存層是分開的，因此各層可以動態分配資源，不會影響另一層的效能或可用性。

這項分離原則可讓 BigQuery 更快創新，因為儲存和運算改善項目可以獨立部署，不會造成停機或對系統效能造成負面影響。此外，BigQuery 工程團隊會負責更新和維護作業，因此能提供全代管的無伺服器資料倉儲。因此，您不必佈建或手動調度資源，可以專注於提供價值，而非傳統的資料庫管理工作。

BigQuery 介面包括 Google Cloud 控制台介面和 BigQuery 指令列工具。開發人員和資料科學家可以使用熟悉的程式設計語言 (包括 Python、Java、JavaScript 和 Go) 搭配用戶端程式庫，以及 BigQuery 的 REST API 和 RPC API，來轉換及管理資料。ODBC 和 JDBC 驅動程式可與現有應用程式 (包括第三方工具和公用程式) 互動。

## 開始使用 BigQuery

只要幾分鐘，就能開始探索 BigQuery。
善用 BigQuery 的免費方案或免付費沙箱，開始載入及查詢資料。

* [BigQuery 沙箱](https://docs.cloud.google.com/bigquery/docs/sandbox?hl=zh-tw)：在 BigQuery 沙箱中開始使用，無須承擔風險，也不必付費。
* [公開資料集](https://docs.cloud.google.com/bigquery/public-data?hl=zh-tw)：探索公開資料集計畫提供的大型真實資料，體驗 BigQuery 的效能。
* [Google Cloud 控制台快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-web-ui?hl=zh-tw)：熟悉 BigQuery Studio 的強大功能。

## 探索 BigQuery

BigQuery 的無伺服器基礎架構可讓您專注於資料，而非資源管理。BigQuery 結合雲端式資料倉儲和強大的分析工具。

### BigQuery 儲存空間

BigQuery 採用資料欄儲存格式，專為分析查詢最佳化。BigQuery 會以資料表、資料列和資料欄的形式呈現資料，並完整支援資料庫交易語意 ([ACID](https://en.wikipedia.org/wiki/ACID))。BigQuery 儲存空間會自動在多個位置複製，提供高可用性。

* [瞭解在資料倉儲和資料超市中，整理 BigQuery 資源的常見模式](https://docs.cloud.google.com/bigquery/docs/resource-hierarchy?hl=zh-tw#patterns)。
* [瞭解資料集](https://docs.cloud.google.com/bigquery/docs/datasets-intro?hl=zh-tw)，這是 BigQuery 中資料表和檢視表的頂層容器。
* [BigQuery 資料移轉服務](https://docs.cloud.google.com/bigquery/docs/dts-introduction?hl=zh-tw)會自動擷取資料。
* 使用下列方式[將資料載入 BigQuery](https://docs.cloud.google.com/bigquery/docs/loading-data?hl=zh-tw)：
  + 使用 [Storage Write API (gRPC)](https://docs.cloud.google.com/bigquery/docs/write-api?hl=zh-tw) [串流資料](https://docs.cloud.google.com/bigquery/docs/streaming-data-into-bigquery?hl=zh-tw)。
  + 從本機檔案或 Cloud Storage [批次載入資料](https://docs.cloud.google.com/bigquery/docs/batch-loading-data?hl=zh-tw)，支援的格式包括：[Avro](https://docs.cloud.google.com/bigquery/docs/loading-data-cloud-storage-avro?hl=zh-tw)、[Parquet](https://docs.cloud.google.com/bigquery/docs/loading-data-cloud-storage-parquet?hl=zh-tw)、[ORC](https://docs.cloud.google.com/bigquery/docs/loading-data-cloud-storage-orc?hl=zh-tw)、[CSV](https://docs.cloud.google.com/bigquery/docs/loading-data-cloud-storage-csv?hl=zh-tw)、[JSON](https://docs.cloud.google.com/bigquery/docs/loading-data-cloud-storage-json?hl=zh-tw)、[Datastore](https://docs.cloud.google.com/bigquery/docs/loading-data-cloud-datastore?hl=zh-tw)和 [Firestore](https://docs.cloud.google.com/bigquery/docs/loading-data-cloud-firestore?hl=zh-tw)格式。

詳情請參閱「[BigQuery 儲存空間總覽](https://docs.cloud.google.com/bigquery/docs/storage_overview?hl=zh-tw)」。

### BigQuery 資料分析

描述性和指示性分析用途包括商業智慧、臨時分析、地理空間分析和機器學習。
您可以查詢儲存在 BigQuery 的資料，或使用外部資料表或聯合查詢，在資料所在位置執行查詢，包括 Cloud Storage、Bigtable、Spanner 或儲存在 Google 雲端硬碟的 Google 試算表。

* ANSI 標準 SQL 查詢 ([支援 ISO/IEC 9075](https://www.iso.org/standard/76583.html))，包括支援 join、巢狀和重複欄位、分析和匯總函式、多重陳述式查詢，以及各種空間函式，並提供地理空間分析 - 地理資訊系統。
* [BigQuery DataFrames](https://docs.cloud.google.com/bigquery/docs/dataframes-quickstart?hl=zh-tw) 提供的 Pandas 相容 Python API。
* [建立檢視畫面](https://docs.cloud.google.com/bigquery/docs/views-intro?hl=zh-tw)，分享分析結果。
* 支援商業智慧工具，包括 [BI Engine](https://docs.cloud.google.com/bigquery/docs/bi-engine-intro?hl=zh-tw) 搭配[數據分析](https://docs.cloud.google.com/bigquery/docs/visualize-looker-studio?hl=zh-tw)、[Looker](https://docs.cloud.google.com/bigquery/docs/looker?hl=zh-tw)、[Google 試算表](https://docs.cloud.google.com/bigquery/docs/connected-sheets?hl=zh-tw)，以及 Tableau 和 Power BI 等第三方工具。
* [BigQuery ML](https://docs.cloud.google.com/bigquery/docs/bqml-introduction?hl=zh-tw) 提供機器學習和預測分析功能。
* [BigQuery Studio](https://docs.cloud.google.com/bigquery/docs/query-overview?hl=zh-tw#bigquery-studio) 提供 Python 筆記本等功能，以及筆記本和已儲存的查詢的版本管控。這些功能可讓您更輕鬆地在 BigQuery 中完成資料分析和機器學習 (ML) 工作流程。
* 使用[聯合查詢](https://docs.cloud.google.com/bigquery/docs/federated-queries-intro?hl=zh-tw)和[外部資料表](https://docs.cloud.google.com/bigquery/docs/external-tables?hl=zh-tw)，[查詢 BigQuery 外部的資料](https://docs.cloud.google.com/bigquery/external-data-sources?hl=zh-tw)。

詳情請參閱「[BigQuery 數據分析總覽](https://docs.cloud.google.com/bigquery/docs/query-overview?hl=zh-tw)」。

### BigQuery 管理

BigQuery 提供資料和運算資源的集中管理功能，而 [Identity and Access Management (IAM)](https://docs.cloud.google.com/iam/docs?hl=zh-tw) 則可透過 Google Cloud中使用的存取模型，協助您保護這些資源。
[Google Cloud 安全性最佳做法](https://cloud.google.com/security/best-practices?hl=zh-tw)提供可靠且彈性的方法，可包含周邊安全性或更複雜且精細的[深度防禦方法](https://cloud.google.com/security/overview/whitepaper?hl=zh-tw#technology_with_security_at_its_core)。

* [資料安全性與治理簡介](https://docs.cloud.google.com/bigquery/docs/data-governance?hl=zh-tw)可協助您瞭解資料治理，以及保護 BigQuery 資源可能需要的控管機制。
* [工作](https://docs.cloud.google.com/bigquery/docs/managing-jobs?hl=zh-tw)是 BigQuery 代您執行的動作，用於載入、匯出、查詢或複製資料。
* [預留項目](https://docs.cloud.google.com/bigquery/docs/reservations-intro?hl=zh-tw)可讓您在隨選計價和以運算資源計價之間切換。

詳情請參閱「[BigQuery 管理簡介](https://docs.cloud.google.com/bigquery/docs/admin-intro?hl=zh-tw)」。

## BigQuery 資源

探索 BigQuery 資源：

* [版本資訊](https://docs.cloud.google.com/bigquery/docs/release-notes?hl=zh-tw)提供功能、變更和淘汰項目的變更記錄。
* 分析和儲存空間[定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw)。另請參閱：[BigQuery ML](https://cloud.google.com/bigquery/pricing?hl=zh-tw#bqml)、[BI Engine](https://cloud.google.com/bigquery/pricing?hl=zh-tw#bi_engine_pricing) 和[資料移轉服務](https://cloud.google.com/bigquery/pricing?hl=zh-tw#data-transfer-service-pricing)定價。
* [位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)定義建立及儲存資料集的位置 (區域和多區域位置)。
* [Stack Overflow](https://stackoverflow.com/questions/tagged/google-bigquery) 擁有一個活躍的開發人員和分析師社群，他們都使用 BigQuery。
* [BigQuery 支援](https://docs.cloud.google.com/bigquery/docs/getting-support?hl=zh-tw)提供 BigQuery 相關協助。
* [Google BigQuery: The Definitive Guide: Data Warehousing, Analytics, and Machine Learning at Scale](https://www.google.com/books/edition/Google_BigQuery_The_Definitive_Guide/-Jq4DwAAQBAJ?hl=zh-tw) (Google BigQuery：權威指南：大規模資料倉儲、數據分析和機器學習) 由 Valliappa Lakshmanan 和 Jordan Tigani 撰寫，說明 BigQuery 的運作方式，並提供如何使用這項服務的端對端逐步操作說明。

### API、工具和參考資料

BigQuery 開發人員和分析師參考資料：

* [BigQuery API](https://docs.cloud.google.com/bigquery/docs/reference/libraries-overview?hl=zh-tw) 和[用戶端程式庫](https://docs.cloud.google.com/bigquery/docs/reference/libraries?hl=zh-tw)提供 BigQuery 功能和用途的總覽。
* [SQL 查詢語法](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw)，瞭解 GoogleSQL 的使用詳情。
* [BigQuery DataFrames API 參考資料](https://dataframes.bigquery.dev/reference/index.html)：詳細說明如何使用與 pandas 相容的 Python API。
* [BigQuery 程式碼範例](https://docs.cloud.google.com/bigquery/docs/samples?hl=zh-tw)提供數百個 [C#](https://docs.cloud.google.com/docs/samples?l=csharp&%3Bp=bigquery&hl=zh-tw)、[Go](https://docs.cloud.google.com/docs/samples?l=go&%3Bp=bigquery&hl=zh-tw)、[Java](https://docs.cloud.google.com/docs/samples?l=java&%3Bp=bigquery&hl=zh-tw)、[Node.js](https://docs.cloud.google.com/docs/samples?l=nodejs&%3Bp=bigquery&hl=zh-tw)、[Python](https://docs.cloud.google.com/docs/samples?l=python&%3Bp=bigquery&hl=zh-tw)、[Ruby](https://docs.cloud.google.com/docs/samples?l=ruby&%3Bp=bigquery&hl=zh-tw) 用戶端程式庫的程式碼片段。或查看[範例瀏覽器](https://docs.cloud.google.com/docs/samples?p=bigquery&hl=zh-tw)。
* [DML](https://docs.cloud.google.com/bigquery/docs/data-manipulation-language?hl=zh-tw)、[DDL](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw) 和 [user-defined function (UDF)](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#create_function_statement)語法可讓您管理及轉換 BigQuery 資料。
* [bq 指令列工具參考資料](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw)：說明 `bq` CLI 介面的語法、指令、旗標和引數。
* [ODBC / JDBC 整合](https://docs.cloud.google.com/bigquery/docs/reference/odbc-jdbc-drivers?hl=zh-tw)：將 BigQuery 連結至現有工具和基礎架構。

## Gemini in BigQuery 功能

Gemini in BigQuery 是 [Gemini for Google Cloud](https://docs.cloud.google.com/gemini/docs/overview?hl=zh-tw) 產品套件的一部分，提供 AI 輔助功能，協助您處理資料。

Gemini in BigQuery 提供 AI 輔助功能，可協助您執行下列操作：

* **運用資料洞察探索及瞭解資料**。資料洞察功能會使用資料表的中繼資料，產生有洞察價值的查詢，以自動化且直覺的方式發掘模式及執行統計分析。這項功能特別有助於解決早期資料探索的冷啟動問題。詳情請參閱「[在 BigQuery 中生成資料洞察](https://docs.cloud.google.com/bigquery/docs/data-insights?hl=zh-tw)」。
* **使用對話式數據分析功能與資料對話**。
  對話式數據分析可讓您以自然語言與資料對話。
  您可以建立資料代理，並設定自訂中繼資料、指令、詞彙表字詞和通過驗證的查詢，建立商業邏輯。您也可以直接與資料來源對話，包括資料表、檢視表、圖表和 Lakehouse 資料表。詳情請參閱「[對話式數據分析總覽](https://docs.cloud.google.com/bigquery/docs/conversational-analytics?hl=zh-tw)」。
* **使用 BigQuery 資料畫布探索、轉換、查詢資料，並以圖表呈現**。您可以在 Gemini in BigQuery 中使用自然語言，尋找、彙整及查詢資料表資產、以圖表呈現結果，並在整個過程中與他人順暢協作。詳情請參閱「[使用資料畫布進行分析](https://docs.cloud.google.com/bigquery/docs/data-canvas?hl=zh-tw)」。
* **取得 SQL 和 Python 資料分析輔助**。您可以使用 Gemini in BigQuery 生成或建議 SQL 或 Python 程式碼，以及說明現有的 SQL 查詢。您也可以使用自然語言查詢，開始資料分析。如要瞭解如何生成、補全及總結程式碼，請參閱下列說明文件：  
  + SQL 程式開發輔助
    - [使用 SQL 生成工具](https://docs.cloud.google.com/bigquery/docs/write-sql-gemini?hl=zh-tw#use_the_sql_generation_tool)
    - [生成 SQL 查詢的提示](https://docs.cloud.google.com/bigquery/docs/write-sql-gemini?hl=zh-tw#chat)
    - [使用 Gemini Cloud Assist 生成 SQL 查詢](https://docs.cloud.google.com/bigquery/docs/write-sql-gemini?hl=zh-tw#chat) ([預先發布版](https://cloud.google.com/products?hl=zh-tw#product-launch-stages))
    - [將註解轉換為 SQL 程式碼](https://docs.cloud.google.com/bigquery/docs/write-sql-gemini?hl=zh-tw#natural_language) ([預先發布版](https://cloud.google.com/products?hl=zh-tw#product-launch-stages))
    - [補全 SQL 查詢](https://docs.cloud.google.com/bigquery/docs/write-sql-gemini?hl=zh-tw#complete_a_sql_query) ([預先發布版](https://cloud.google.com/products?hl=zh-tw#product-launch-stages))
    - [說明 SQL 查詢](https://docs.cloud.google.com/bigquery/docs/write-sql-gemini?hl=zh-tw#explain_a_sql_query)
  + Python 程式開發輔助
    - [使用程式碼生成工具生成 Python 程式碼](https://docs.cloud.google.com/bigquery/docs/write-sql-gemini?hl=zh-tw#generate_python_code)
    - [使用 Gemini Cloud Assist 生成 Python 程式碼](https://docs.cloud.google.com/bigquery/docs/write-sql-gemini?hl=zh-tw#chat-python) ([預先發布版](https://cloud.google.com/products?hl=zh-tw#product-launch-stages))
    - [Python 程式碼補全](https://docs.cloud.google.com/bigquery/docs/write-sql-gemini?hl=zh-tw#complete_python_code)
    - [生成 BigQuery DataFrames Python 程式碼](https://docs.cloud.google.com/bigquery/docs/write-sql-gemini?hl=zh-tw#dataframe) ([預先發布版](https://cloud.google.com/products?hl=zh-tw#product-launch-stages))
* **準備要分析的資料**。BigQuery 的資料準備功能會根據情境，提供 AI 生成的轉換建議，協助您清理資料以進行分析。詳情請參閱「[使用 Gemini 準備資料](https://docs.cloud.google.com/bigquery/docs/data-prep-get-suggestions?hl=zh-tw)」。
* **使用資料工程代理建構及修改資料管道**。資料工程代理可協助您使用自然語言提示詞，建構、修改及排解資料管道問題。除了 SQL 邏輯，代理還會主動生成語意中繼資料，例如欄位說明、資料表總覽，以及系統和類型資訊等一般層面，確保資料資產在建立時就能被找到。詳情請參閱「[使用 Data Engineering Agent 建構及修改資料管道](https://docs.cloud.google.com/bigquery/docs/data-engineering-agent-pipelines?hl=zh-tw)」。
* **使用翻譯規則自訂 SQL 翻譯**。([預先發布版](https://cloud.google.com/products?hl=zh-tw#product-launch-stages)) 建立 Gemini 強化翻譯規則，在使用[互動式 SQL 翻譯器](https://docs.cloud.google.com/bigquery/docs/interactive-sql-translator?hl=zh-tw)時自訂 SQL 翻譯。您可以使用自然語言提示詞，說明要對 SQL 翻譯輸出內容進行哪些變更，或指定要尋找及取代的 SQL 模式。詳情請參閱「[建立轉譯規則](https://docs.cloud.google.com/bigquery/docs/interactive-sql-translator?hl=zh-tw#create-apply-rules)」。

如要瞭解如何設定 Gemini in BigQuery，請參閱「[設定 Gemini in BigQuery](https://docs.cloud.google.com/bigquery/docs/gemini-set-up?hl=zh-tw)」。

## BigQuery 角色和資源

BigQuery 可滿足資料專業人員在下列角色和職責方面的需求。

### 資料分析師

如需執行下列操作，請參閱工作指南：

* 使用[SQL 查詢語法](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw)，透過互動式或批次查詢[查詢 BigQuery 資料](https://docs.cloud.google.com/bigquery/docs/query-overview?hl=zh-tw)
* 使用與 pandas 相容的 [BigQuery DataFrames API](https://dataframes.bigquery.dev/reference/index.html)，[分析及轉換 BigQuery 資料](https://docs.cloud.google.com/bigquery/docs/dataframes-quickstart?hl=zh-tw)。
* 參考 SQL [函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/functions-all?hl=zh-tw)、[運算子](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/operators?hl=zh-tw)和[條件運算式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/conditional_expressions?hl=zh-tw)來查詢資料
* 使用工具分析 BigQuery 資料並以視覺化方式呈現，包括 [Looker](https://docs.cloud.google.com/bigquery/docs/looker?hl=zh-tw)、[數據分析](https://docs.cloud.google.com/bigquery/docs/visualize-looker-studio?hl=zh-tw)和 [Google 試算表](https://docs.cloud.google.com/bigquery/docs/connected-sheets?hl=zh-tw)。
* [使用地理空間分析](https://docs.cloud.google.com/bigquery/docs/gis-intro?hl=zh-tw)，透過 BigQuery 的地理資訊系統分析地理空間資料，並以圖表呈現
* 使用下列方法[盡可能提高查詢效能](https://docs.cloud.google.com/bigquery/docs/best-practices-performance-overview?hl=zh-tw)：

  + [分區資料表](https://docs.cloud.google.com/bigquery/docs/partitioned-tables?hl=zh-tw)：根據時間或整數範圍，刪除大型資料表。
  + [materialized view](https://docs.cloud.google.com/bigquery/docs/materialized-views-intro?hl=zh-tw)：定義快取檢視表，以最佳化查詢或提供永久結果。
  + [BI Engine](https://docs.cloud.google.com/bigquery/docs/bi-engine-intro?hl=zh-tw)：BigQuery 的快速記憶體內分析服務。

### 資料管理員

如需執行下列操作，請參閱工作指南：

* 透過[預留項目](https://docs.cloud.google.com/bigquery/docs/reservations-intro?hl=zh-tw)[管理費用](https://docs.cloud.google.com/bigquery/docs/controlling-costs?hl=zh-tw)，平衡隨選和以運算資源為基礎的定價。
* [瞭解資料安全性和管理](https://docs.cloud.google.com/bigquery/docs/data-governance?hl=zh-tw)，依[資料集](https://docs.cloud.google.com/bigquery/docs/control-access-to-resources-iam?hl=zh-tw)、[資料表](https://docs.cloud.google.com/bigquery/docs/control-access-to-resources-iam?hl=zh-tw)、[資料欄](https://docs.cloud.google.com/bigquery/docs/column-level-security-intro?hl=zh-tw)、[資料列](https://docs.cloud.google.com/bigquery/docs/row-level-security-intro?hl=zh-tw)或[檢視表](https://docs.cloud.google.com/bigquery/docs/authorized-views?hl=zh-tw)保護資料
* [使用資料表快照備份資料](https://docs.cloud.google.com/bigquery/docs/table-snapshots-intro?hl=zh-tw)，保留特定時間的資料表內容。
* [查看 BigQuery INFORMATION\_SCHEMA](https://docs.cloud.google.com/bigquery/docs/information-schema-intro?hl=zh-tw)，瞭解[資料集](https://docs.cloud.google.com/bigquery/docs/information-schema-datasets-schemata?hl=zh-tw)、[工作](https://docs.cloud.google.com/bigquery/docs/information-schema-jobs?hl=zh-tw)、[存取控管](https://docs.cloud.google.com/bigquery/docs/information-schema-object-privileges?hl=zh-tw)、[預留項目](https://docs.cloud.google.com/bigquery/docs/information-schema-reservations?hl=zh-tw)、[資料表](https://docs.cloud.google.com/bigquery/docs/information-schema-tables?hl=zh-tw)等的中繼資料。
* [使用工作](https://docs.cloud.google.com/bigquery/docs/managing-jobs?hl=zh-tw)，讓 BigQuery 代您載入、匯出、查詢或複製資料。
* [監控記錄和資源](https://docs.cloud.google.com/bigquery/docs/monitoring?hl=zh-tw)，瞭解 BigQuery 和工作負載。

詳情請參閱「[BigQuery 管理簡介](https://docs.cloud.google.com/bigquery/docs/admin-intro?hl=zh-tw)」。

如要直接在 Google Cloud 控制台導覽 BigQuery 資料管理功能，請按一下「Take the tour」(導覽)。

[開始導覽](https://console.cloud.google.com/?walkthrough_id=bigquery--ui-tour-data-admin&hl=zh-tw)

### 資料科學家

如需使用 [BigQuery ML 的機器學習](https://docs.cloud.google.com/bigquery/docs/bqml-introduction?hl=zh-tw)功能執行下列操作，請參閱工作指南：

* [瞭解機器學習模型的端對端使用者歷程](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-e2e-journey?hl=zh-tw)
* [管理 BigQuery ML 的存取控管](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)
* [建立及訓練 BigQuery ML 模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create?hl=zh-tw)，包括：
  + [線性迴歸](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-glm?hl=zh-tw)預測
  + [二元邏輯](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-glm?hl=zh-tw)和[多類別邏輯](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-glm?hl=zh-tw)迴歸分類
  + [k-means 分群法](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-kmeans?hl=zh-tw)：用於資料區隔
  + 使用 ARIMA+ 模型進行[時間序列](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-time-series?hl=zh-tw)預測

### 資料開發人員

如需執行下列操作，請參閱工作指南：

* [將資料載入 BigQuery](https://docs.cloud.google.com/bigquery/docs/loading-data?hl=zh-tw)，方法如下：
  + [Avro](https://docs.cloud.google.com/bigquery/docs/loading-data-cloud-storage-avro?hl=zh-tw)、[Parquet](https://docs.cloud.google.com/bigquery/docs/loading-data-cloud-storage-parquet?hl=zh-tw)、[ORC](https://docs.cloud.google.com/bigquery/docs/loading-data-cloud-storage-orc?hl=zh-tw)、[CSV](https://docs.cloud.google.com/bigquery/docs/loading-data-cloud-storage-csv?hl=zh-tw)、[JSON](https://docs.cloud.google.com/bigquery/docs/loading-data-cloud-storage-json?hl=zh-tw)
    、[Datastore](https://docs.cloud.google.com/bigquery/docs/loading-data-cloud-datastore?hl=zh-tw)
    和 [Firestore](https://docs.cloud.google.com/bigquery/docs/loading-data-cloud-firestore?hl=zh-tw)
    格式的[批次載入資料](https://docs.cloud.google.com/bigquery/docs/batch-loading-data?hl=zh-tw)
  + [BigQuery 資料移轉服務](https://docs.cloud.google.com/bigquery/docs/dts-introduction?hl=zh-tw)
  + [BigQuery Storage Write API (gRPC)](https://docs.cloud.google.com/bigquery/docs/write-api?hl=zh-tw)
* [使用程式碼範例庫](https://docs.cloud.google.com/bigquery/docs/samples?hl=zh-tw)，包括：

  + [連線範例](https://docs.cloud.google.com/bigquery/docs/samples?api=bigqueryconnectionapi&hl=zh-tw)
  + [預訂範例](https://docs.cloud.google.com/bigquery/docs/samples?api=bigqueryreservationapi&hl=zh-tw)
  + [Storage 程式碼範例](https://docs.cloud.google.com/bigquery/docs/samples?api=bigquerystorage&hl=zh-tw)
* [Google Cloud 範例瀏覽器](https://docs.cloud.google.com/docs/samples?p=bigquery&hl=zh-tw) (範圍為 BigQuery)
* [API 與程式庫總覽](https://docs.cloud.google.com/bigquery/docs/reference/libraries-overview?hl=zh-tw)
* [ODBC / JDBC 整合](https://docs.cloud.google.com/bigquery/docs/reference/odbc-jdbc-drivers?hl=zh-tw)

## 後續步驟

* 如要瞭解 BigQuery 儲存空間，請參閱「[BigQuery 儲存空間總覽](https://docs.cloud.google.com/bigquery/docs/storage_overview?hl=zh-tw)」。
* 如要瞭解 BigQuery 查詢，請參閱「[BigQuery 數據分析總覽](https://docs.cloud.google.com/bigquery/docs/query-overview?hl=zh-tw)」。
* 如需 BigQuery 管理作業的總覽，請參閱「[BigQuery 管理作業簡介](https://docs.cloud.google.com/bigquery/docs/admin-intro?hl=zh-tw)」。
* 如要瞭解 BigQuery 安全性，請參閱「[資料安全性與管理總覽](https://docs.cloud.google.com/bigquery/docs/data-governance?hl=zh-tw)」。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-10-22 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-10-22 (世界標準時間)。"],[],[]]