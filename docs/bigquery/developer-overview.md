Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 開發人員工具簡介

BigQuery 提供一組開發人員工具，可讓您在開發環境中存取 BigQuery、將 BigQuery 連結至外部應用程式，以及開發端對端解決方案。使用這些工具前，請先熟悉標準 BigQuery 概念，例如[分析](https://docs.cloud.google.com/bigquery/docs/query-overview?hl=zh-tw)和[資源組織](https://docs.cloud.google.com/bigquery/docs/resource-hierarchy?hl=zh-tw)。

## 在開發環境中存取 BigQuery 的工具

BigQuery API 和用戶端程式庫是核心開發人員工具，用於在Google Cloud 控制台和 bq 指令列工具之外發出 BigQuery 要求。透過這種方式存取 BigQuery 時，您也必須提供某種形式的驗證。

### API

BigQuery 提供 [REST 和 gRPC API](https://docs.cloud.google.com/bigquery/docs/reference/libraries-overview?hl=zh-tw)，可透過程式輔助方式與各種服務互動。可用的 API 如下：

* [BigQuery API](https://docs.cloud.google.com/bigquery/docs/reference/rest?hl=zh-tw)
* [BigQuery Data Policy API](https://docs.cloud.google.com/bigquery/docs/reference/bigquerydatapolicy/rest?hl=zh-tw)
* [BigQuery Connection API](https://docs.cloud.google.com/bigquery/docs/reference/bigqueryconnection/rest?hl=zh-tw)
* [BigQuery Migration API](https://docs.cloud.google.com/bigquery/docs/reference/migration/rest?hl=zh-tw)
* [BigQuery Storage API](https://docs.cloud.google.com/bigquery/docs/reference/storage/rpc?hl=zh-tw)
* [BigQuery Reservation API](https://docs.cloud.google.com/bigquery/docs/reference/reservations/rest?hl=zh-tw)
* [BigQuery Analytics Hub API](https://docs.cloud.google.com/bigquery/docs/reference/analytics-hub/rest?hl=zh-tw)
* [BigQuery Data Transfer Service API](https://docs.cloud.google.com/bigquery/docs/reference/datatransfer/rest?hl=zh-tw)

### 用戶端程式庫

雖然您可以直接向伺服器發出要求來使用 BigQuery API，但使用 [BigQuery 用戶端程式庫](https://docs.cloud.google.com/bigquery/docs/reference/libraries?hl=zh-tw)可簡化 BigQuery API 呼叫，大幅減少需要編寫的程式碼數量。BigQuery 支援的語言包括 C#、Go、Java、Node.js、PHP、Python 和 Ruby。如要試用 BigQuery 用戶端程式庫的快速入門導覽課程，請參閱「[使用 BigQuery 用戶端程式庫查詢公開資料集](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」。

### 驗證

「驗證」是透過憑證確認身分的程序。在開發環境中存取 BigQuery 時，一律需要進行驗證。BigQuery 開發人員最常用的驗證方式是[應用程式預設憑證](https://docs.cloud.google.com/bigquery/docs/authentication/getting-started?hl=zh-tw#adc)，可根據環境自動尋找憑證。如要進一步瞭解一般驗證原則和其他驗證方式，請參閱「[向 BigQuery 驗證](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw)」。

## 將 BigQuery 連結至外部應用程式的工具

您可以使用多種自訂連線工具，將 BigQuery 功能與第三方應用程式整合。

### MCP Toolbox for Databases

Model Context Protocol (MCP) 是一種開放式通訊協定，可將大型語言模型 (LLM) 連結至 BigQuery 等資料來源。[MCP Toolbox for Databases](https://docs.cloud.google.com/bigquery/docs/pre-built-tools-with-mcp-toolbox?hl=zh-tw) 可將 BigQuery 專案連結至各種整合式開發環境 (IDE) 和開發人員工具，讓您運用 BigQuery 資料建構更強大的 AI 代理。

### BigQuery 代理分析

BigQuery 代理數據分析是第一方開放原始碼解決方案，可大規模擷取、分析及視覺化多模態代理互動資料。這項解決方案可讓開發人員將原始代理互動 (例如要求、回覆、工具呼叫和錯誤) 直接串流至 BigQuery。

如要進一步瞭解這項解決方案，請參閱「[使用 BigQuery 代理數據分析](https://docs.cloud.google.com/bigquery/docs/bigquery-agent-analytics?hl=zh-tw)」。

### ODBC 和 JDBC 驅動程式

開放式資料庫連線 (ODBC) 和 Java 資料庫連線 (JDBC) 驅動程式可將應用程式連結至資料庫。Google 與 [Simba](https://insightsoftware.com/simba/) 合作，提供 [BigQuery 的 ODBC 和 JDBC 驅動程式](https://docs.cloud.google.com/bigquery/docs/reference/odbc-jdbc-drivers?hl=zh-tw)，您可以使用這些驅動程式，透過偏好的工具和基礎架構，建構與資料庫無關的軟體應用程式。您也可以使用 [Google 開發的 BigQuery 專用 JDBC 驅動程式](https://docs.cloud.google.com/bigquery/docs/jdbc-for-bigquery?hl=zh-tw)。

### Data Agent Kit

[Google Cloud Data Agent Kit](https://docs.cloud.google.com/data-agent-kit?hl=zh-tw) 提供代理程式編碼工具 (例如 VS Code、Antigravity 和 Cursor) 的擴充功能，可讓您直接在代理程式環境中與 BigQuery 資源互動。您可以使用 Data Agent Kit 瀏覽資料集、管理管道、執行查詢，以及提示代理在偏好的 IDE 中直接執行其他 BigQuery 工作。

Data Agent Kit 也提供一組外掛程式，可與各種指令列工具搭配使用，包括 Antigravity CLI、Gemini CLI、Claude Code 和 Codex CLI。

## 開發端對端解決方案的工具

使用 BigQuery 建構複雜的解決方案時，Google 提供多種途徑協助您，其中最值得注意的是程式碼範例、存放區和工作區功能，以及各種 BigQuery 整合。

### 程式碼範例

[BigQuery 程式碼範例](https://docs.cloud.google.com/bigquery/docs/samples?hl=zh-tw)提供程式碼片段，可用於完成 BigQuery 中的常見工作，例如建立資料表、列出連線、查看容量承諾和預留項目，以及載入資料。您可以使用這些程式碼範例，開始建構更複雜的解決方案。

### 存放區和工作區

**預覽**

這項產品或功能適用《[服務專屬條款](https://docs.cloud.google.com/terms/service-terms?hl=zh-tw#1)》中「一般服務條款」一節的《正式發布前產品條款》。正式發布前的產品和功能是按照「原樣」提供，支援範圍可能有限。
詳情請參閱[推出階段說明](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages)。

您可以使用[存放區](https://docs.cloud.google.com/bigquery/docs/repository-intro?hl=zh-tw)，對 BigQuery 中使用的檔案進行版本管控，並使用這些存放區中的[工作區](https://docs.cloud.google.com/bigquery/docs/workspaces-intro?hl=zh-tw)編輯程式碼。BigQuery 會使用 Git 記錄變更及管理檔案版本。您可以使用 BigQuery 內建的 Git 功能，也可以連線至第三方 Git 存放區。

### 整合式服務和工具

下列 Google 服務和工具與 BigQuery 整合，並提供建構解決方案的其他功能：

* [**Managed Service for Apache Spark**](https://docs.cloud.google.com/managed-spark/docs/concepts/clusters-overview?hl=zh-tw)：全代管服務，用於執行 Apache Hadoop 和 Apache Spark 工作。Managed Service for Apache Spark 提供 [BigQuery 連接器](https://docs.cloud.google.com/managed-spark/docs/concepts/connectors/bigquery?hl=zh-tw)，可讓 Hadoop 和 Spark 直接處理 BigQuery 中的資料。
* [**Dataflow**](https://docs.cloud.google.com/dataflow/docs/overview?hl=zh-tw)。這項全代管服務可大規模執行 Apache Beam 工作。[Beam 的 BigQuery I/O 連接器](https://beam.apache.org/documentation/io/built-in/google-bigquery/)可讓 Beam 管道在 BigQuery 中讀取及寫入資料。
* [**Managed Service for Apache Airflow**](https://docs.cloud.google.com/composer/docs/composer-3/composer-overview?hl=zh-tw)。以 Apache Airflow 為基礎建構的全代管工作流程排程服務。[BigQuery 運算子](https://airflow.apache.org/docs/apache-airflow-providers-google/stable/operators/cloud/bigquery.html)可讓 Airflow 工作流程管理資料集和資料表、執行查詢及驗證資料。
* [**Pub/Sub**](https://docs.cloud.google.com/pubsub/docs/overview?hl=zh-tw)。非同步且可擴充的訊息服務。Pub/Sub 提供 [BigQuery 訂閱項目](https://docs.cloud.google.com/pubsub/docs/bigquery?hl=zh-tw)，可在收到訊息時，將訊息寫入現有的 BigQuery 資料表。
* [**Dataform**](https://docs.cloud.google.com/dataform/docs/overview?hl=zh-tw)。這項服務可讓資料分析師在 BigQuery 中開發、測試、版本管控，並安排資料轉換複雜的 SQL 工作流程。
* [**BigQuery Terraform 模組**](https://github.com/terraform-google-modules/terraform-google-bigquery/blob/master/README.md)。這個模組可自動例項化及部署 BigQuery 資料集和資料表。
* [**bq 指令列工具**](https://docs.cloud.google.com/bigquery/docs/bq-command-line-tool?hl=zh-tw)。BigQuery 專用的 Python 指令列工具。

Google 也透過 [Google Cloud Ready - BigQuery](https://docs.cloud.google.com/bigquery/docs/bigquery-ready-overview?hl=zh-tw) 計畫，驗證數十種 BigQuery 合作夥伴解決方案和整合項目。這些合作夥伴已通過核心要求，確保與 BigQuery 相容。

## 後續步驟

* 如要瞭解 Google Cloud開發人員資源和近期活動，請前往[開發人員中心](https://cloud.google.com/developers?hl=zh-tw)。
* 如要瞭解其他公司如何使用 Google Cloud，請參閱「[ISV 的 Data Cloud](https://cloud.google.com/solutions/data-cloud-isvs?hl=zh-tw)」。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-11-11 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-11-11 (世界標準時間)。"],[],[]]