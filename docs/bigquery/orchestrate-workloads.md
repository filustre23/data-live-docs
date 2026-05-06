Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 排定工作負載

BigQuery 工作通常是較大型工作負載的一部分，外部工作會觸發 BigQuery 作業，然後由這些作業觸發。工作負載排程可協助資料管理員、分析師和開發人員整理及最佳化這一連串的動作，在資料資源和程序之間建立順暢的連結。排程方法和工具可協助設計、建構、實作及監控這些複雜的資料工作負載。

## 選擇排程方式

如要選取排程方法，請判斷工作負載是由事件驅動、時間驅動，還是兩者皆是。「事件」是指狀態變更，例如資料庫中的資料變更，或是儲存系統中新增了檔案。在*事件驅動排程*中，網站上的動作可能會觸發資料活動，或是抵達特定值區的物件可能需要立即處理。在*時間驅動排程*中，可能需要每天載入一次新資料，或頻繁載入資料，才能產生每小時的報表。在需要即時將物件載入資料湖泊，但資料湖泊的活動報表只會每日產生一次的情況下，您可以使用事件導向和時間導向排程。

## 選擇排程工具

排程工具可協助您管理複雜的資料工作負載，例如將多個 Google Cloud 或第三方服務與 BigQuery 工作合併，或平行執行多個 BigQuery 工作。每項工作負載都有獨特的依附元件和參數管理需求，確保工作以正確順序執行，並使用正確的資料。 Google Cloud 提供多種排程選項，可根據排程方法和工作負載需求選擇。

建議您在多數情況下使用 Dataform、Workflows、Managed Airflow 或 Vertex AI Pipelines。請參閱下表，瞭解並排比較結果：

|  | [Dataform](#dataform) | [Workflows](#workflows) | [Managed Airflow](#composer) | [Vertex AI Pipelines](#vertex) |
| --- | --- | --- | --- | --- |
| 聚焦 | 資料轉換 | 微服務 | ETL 或 ELT | 機器學習 |
| 複雜度 | \* | \*\* | \*\*\* | \*\* |
| 使用者個人資料 | 資料分析師或管理員 | 資料架構師 | 資料工程師 | 資料分析師 |
| 程式碼類型 | JavaScript、SQL、[Python 筆記本](https://docs.cloud.google.com/bigquery/docs/orchestrate-notebooks?hl=zh-tw) | YAML 或 JSON | Python | Python |
| 無伺服器？ | 是 | 是 | 全代管 | 是 |
| 不適用於 | 外部服務鏈 | 資料轉換和處理 | 低延遲或事件導向管道 | 基礎架構工作 |

以下各節將詳細說明這些排程工具和其他工具。

### 已排定的查詢

最簡單的工作負載排程形式，就是直接在 BigQuery 中[排定週期性查詢](https://docs.cloud.google.com/bigquery/docs/scheduling-queries?hl=zh-tw)。這是最簡單的排程方式，但我們建議只針對沒有外部依附元件的簡單查詢鏈使用。以這種方式排定的查詢必須以 [GoogleSQL](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw) 編寫，且可包含[資料定義語言 (DDL)](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw) 和[資料操作語言 (DML)](https://docs.cloud.google.com/bigquery/docs/data-manipulation-language?hl=zh-tw) 陳述式。

**排程方法**：以時間為準

### Dataform

[Dataform](https://docs.cloud.google.com/dataform/docs/overview?hl=zh-tw) 是以 SQL 為基礎的免費轉換框架，可排定 BigQuery 中複雜的資料轉換任務。將原始資料載入 BigQuery 時，Dataform 可協助您建立經過測試、版本受控的資料集和資料表集合。使用 Dataform 安排[資料準備](https://docs.cloud.google.com/bigquery/docs/orchestrate-data-preparations?hl=zh-tw)、[筆記本](https://docs.cloud.google.com/bigquery/docs/orchestrate-notebooks?hl=zh-tw)和 [BigQuery 管道](https://docs.cloud.google.com/bigquery/docs/schedule-pipelines?hl=zh-tw)的執行時間。

**排程方法**：以時間為準

**注意：** 如果您在 BigQuery 存放區中建立資產 (例如查詢、筆記本 (包括含 Apache Spark 工作的筆記本)、BigQuery 管道或 Dataform 工作流程)，則無法在 Dataform 中排定執行時間。您必須改用 BigQuery 執行和排程功能。詳情請參閱「[排定查詢的執行時間](https://docs.cloud.google.com/bigquery/docs/scheduling-queries?hl=zh-tw)」、「[排定筆記本的執行時間](https://docs.cloud.google.com/bigquery/docs/orchestrate-notebooks?hl=zh-tw)」和「[排定管道的執行時間](https://docs.cloud.google.com/bigquery/docs/schedule-pipelines?hl=zh-tw)」。

### 工作流程

[工作流程](https://docs.cloud.google.com/workflows/docs/overview?hl=zh-tw)是一種無伺服器工具，可排定以 HTTP 為基礎的服務，延遲時間極短。最適合用於串連微服務、自動執行基礎架構工作、與外部系統整合，或在 Google Cloud中建立一連串作業。如要進一步瞭解如何搭配使用 Workflows 和 BigQuery，請參閱「[平行執行多項 BigQuery 工作](https://docs.cloud.google.com/workflows/docs/tutorials/bigquery-parallel-jobs?hl=zh-tw)」。

**排程方法**：事件驅動和時間驅動

### Managed Service for Apache Airflow

[Managed Airflow](https://docs.cloud.google.com/composer/docs/concepts/overview?hl=zh-tw) 是以 Apache Airflow 為基礎建構的全代管工具，這項服務最適合擷取、轉換和載入 (ETL) 或擷取、載入和轉換 (ELT) 工作負載，因為它支援多種[運算子](https://airflow.apache.org/docs/apache-airflow/stable/concepts/operators.html)類型和模式，以及其他 Google Cloud產品和外部目標的任務執行作業。如要進一步瞭解如何搭配使用 Managed Airflow 與 BigQuery，請參閱「[在 Google Cloud](https://docs.cloud.google.com/composer/docs/data-analytics-googlecloud?hl=zh-tw)中執行資料分析 DAG」。

**排程方法**：以時間為準

### Vertex AI Pipelines

[Vertex AI Pipelines](https://docs.cloud.google.com/vertex-ai/docs/pipelines/introduction?hl=zh-tw) 是以 Kubeflow Pipelines 為基礎的無伺服器工具，專為排定機器學習工作負載而設計。從訓練資料到程式碼，這項服務會自動執行並連結模型開發和部署的所有工作，讓您全面瞭解模型的運作方式。如要進一步瞭解如何搭配使用 Vertex AI Pipelines 與 BigQuery，請參閱「[匯出及部署 BigQuery 機器學習模型，以進行預測](https://codelabs.developers.google.com/codelabs/bqml-vertex-prediction?hl=zh-tw#0)」。

**排程方法**：事件驅動

### Apigee Integration

[Apigee Integration](https://docs.cloud.google.com/apigee/docs/api-platform/integration/what-is-apigee-integration?hl=zh-tw) 是 Apigee 平台的擴充功能，內含連接器和資料轉換工具。最適合與 Salesforce 等外部企業應用程式整合。如要進一步瞭解如何搭配使用 Apigee Integration 與 BigQuery，請參閱「[開始使用 Apigee Integration 和 Salesforce 觸發程序](https://docs.cloud.google.com/apigee/docs/api-platform/integration/getting-started-salesforce-updates?hl=zh-tw)」。

**排程方法**：事件驅動和時間驅動

### Cloud Data Fusion

[Cloud Data Fusion](https://docs.cloud.google.com/data-fusion?hl=zh-tw) 是一項資料整合工具，提供無程式碼的 ELT/ETL 管道，以及超過 150 個預先設定的連接器和轉換。如要進一步瞭解如何搭配使用 Cloud Data Fusion 與 BigQuery，請參閱[將資料從 MySQL 複製到 BigQuery](https://docs.cloud.google.com/data-fusion/docs/tutorials/replicating-data/mysql-to-bigquery?hl=zh-tw)。

**排程方法**：事件驅動和時間驅動

### Cloud Scheduler

[Cloud Scheduler](https://docs.cloud.google.com/scheduler/docs/overview?hl=zh-tw) 是全代管的排程器，適用於應在特定時間間隔執行的工作，例如批次串流或基礎架構作業。如要進一步瞭解如何將 Cloud Scheduler 與 BigQuery 搭配使用，請參閱[使用 Cloud Scheduler 安排工作流程](https://docs.cloud.google.com/scheduler/docs/tut-workflows?hl=zh-tw)。

**排程方法**：以時間為準

### Cloud Tasks

[Cloud Tasks](https://docs.cloud.google.com/tasks/docs/dual-overview?hl=zh-tw) 是一項全代管服務，可非同步分配工作，這些工作可獨立執行，不屬於主要工作負載。最適合用於委派緩慢的背景作業，或管理 API 呼叫率。如要進一步瞭解如何搭配使用 Cloud Tasks 和 BigQuery，請參閱「[將任務新增至 Cloud Tasks 佇列](https://docs.cloud.google.com/tasks/docs/add-task-queue?hl=zh-tw)」。

**排程方法**：事件驅動

### 第三方工具

您也可以使用 CData 和 SnapLogic 等多種熱門第三方工具連線至 BigQuery。BigQuery Ready 計畫提供[經過驗證的合作夥伴解決方案完整清單](https://docs.cloud.google.com/bigquery/docs/bigquery-ready-partners?hl=zh-tw)。

## 訊息工具

許多資料工作負載都需要在分離的微服務之間建立額外的訊息傳輸連線，且只有在發生特定事件時才需要啟用。Google Cloud 提供兩種工具，可與 BigQuery 整合。

### Pub/Sub

[Pub/Sub](https://docs.cloud.google.com/pubsub/docs/overview?hl=zh-tw) 是非同步訊息傳遞工具，適用於資料整合管道。這項服務的設計目的是擷取及分配資料，例如伺服器事件和使用者互動。此外，您也可以使用這項服務，從 IoT 裝置進行平行處理和資料串流。如要進一步瞭解如何搭配使用 Pub/Sub 和 BigQuery，請參閱「[從 Pub/Sub 串流至 BigQuery](https://docs.cloud.google.com/dataflow/docs/tutorials/dataflow-stream-to-bigquery?hl=zh-tw)」。

### Eventarc

[Eventarc](https://docs.cloud.google.com/eventarc/docs/overview?hl=zh-tw) 是一種事件驅動工具，可讓您管理整個資料管道的狀態變更流程。這項工具的用途十分廣泛，包括自動修正錯誤、資源標記、修飾圖片等。如要進一步瞭解如何搭配使用 Eventarc 與 BigQuery，請參閱「[使用 Eventarc 建立 BigQuery 處理管道](https://docs.cloud.google.com/eventarc/docs/run/bigquery?hl=zh-tw)」。

## 後續步驟

* 瞭解如何[直接在 BigQuery 中排定週期性查詢](https://docs.cloud.google.com/bigquery/docs/scheduling-queries?hl=zh-tw)。
* 開始使用 [Dataform](https://docs.cloud.google.com/dataform/docs/overview?hl=zh-tw)。
* 開始使用 [Workflows](https://docs.cloud.google.com/workflows/docs/overview?hl=zh-tw)。
* 開始使用 [Managed Airflow](https://docs.cloud.google.com/composer/docs/concepts/overview?hl=zh-tw)。
* 開始使用 [Vertex AI Pipelines](https://docs.cloud.google.com/vertex-ai/docs/pipelines/introduction?hl=zh-tw)。
* 開始使用 [Apigee Integration](https://docs.cloud.google.com/apigee/docs/api-platform/integration/what-is-apigee-integration?hl=zh-tw)。
* 開始使用 [Cloud Data Fusion](https://docs.cloud.google.com/data-fusion?hl=zh-tw)。
* 開始使用 [Cloud Scheduler](https://docs.cloud.google.com/scheduler/docs/overview?hl=zh-tw)。
* 開始使用 [Pub/Sub](https://docs.cloud.google.com/pubsub/docs/overview?hl=zh-tw)。
* 開始使用 [Eventarc](https://docs.cloud.google.com/eventarc/docs/overview?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-02 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-02 (世界標準時間)。"],[],[]]