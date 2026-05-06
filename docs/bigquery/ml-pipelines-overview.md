Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 機器學習管道總覽

本文件將概略說明您可用來建構機器學習管道，以管理 BigQuery ML [MLOps](https://docs.cloud.google.com/architecture/mlops-continuous-delivery-and-automation-pipelines-in-machine-learning?hl=zh-tw) 工作流程的服務。

機器學習管道是 MLOps 工作流程的代表，由一系列*管道工作*組成。每個管道工作都會執行 MLOps 工作流程中的特定步驟，以便訓練及部署模型。將每個步驟分割為標準化且可重複使用的任務，即可在機器學習實務中自動化及監控可重複的程序。

您可以使用下列任一服務建立 BigQuery ML 機器學習管道：

* 使用 Vertex AI Pipelines 建立可移植且可擴充的機器學習管道。
* 使用 GoogleSQL 查詢建立較不複雜的 SQL 機器學習管道。
* 使用 Dataform 建立更複雜的 SQL 機器學習管道，或需要使用版本控制的機器學習管道。

## Vertex AI Pipelines

在 [Vertex AI Pipelines](https://docs.cloud.google.com/vertex-ai/docs/pipelines/introduction?hl=zh-tw) 中，機器學習管道的結構是使用輸入/輸出依附元件相互連結的容器化管道工作，以有向無環圖 (DAG) 的形式呈現。每個[管道工作](https://docs.cloud.google.com/vertex-ai/docs/pipelines/introduction?hl=zh-tw#pipeline-task)都是[管道元件](https://docs.cloud.google.com/vertex-ai/docs/pipelines/introduction?hl=zh-tw#pipeline-component)的例項化，並具有特定輸入內容。定義機器學習管道時，您可以將一個管道工作的輸出內容，路由至機器學習工作流程中下一個管道工作的輸入內容，藉此連結多個管道工作，形成 DAG。您也可以將 ML 管道的原始輸入內容，用做特定管道工作的輸入內容。

使用 Google Cloud Pipeline Components SDK 的 [BigQuery ML 元件](https://docs.cloud.google.com/vertex-ai/docs/pipelines/bigqueryml-component?hl=zh-tw)，在 Vertex AI Pipelines 中組合機器學習管道。如要開始使用 BigQuery ML 元件，請參閱下列 Notebook：

* [開始使用 BigQuery ML 管道元件](https://github.com/GoogleCloudPlatform/vertex-ai-samples/blob/main/notebooks/community/ml_ops/stage3/get_started_with_bqml_pipeline_components.ipynb)
* [訓練及評估需求預測模型](https://github.com/GoogleCloudPlatform/vertex-ai-samples/blob/main/notebooks/community/pipelines/google_cloud_pipeline_components_bqml_pipeline_demand_forecasting.ipynb)

## GoogleSQL 查詢

您可以使用 [GoogleSQL 程序語言](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/procedural-language?hl=zh-tw)，在[多個陳述式查詢](https://docs.cloud.google.com/bigquery/docs/multi-statement-queries?hl=zh-tw)中執行多個陳述式。您可以使用多個陳述式查詢執行以下操作：

* 依序執行多個陳述式，並共用狀態。
* 自動執行管理工作，例如建立或刪除資料表。
* 使用 `IF` 和 `WHILE` 等程式設計結構，實作複雜的邏輯。

建立多語句查詢後，您可以[儲存](https://docs.cloud.google.com/bigquery/docs/saved-queries-introduction?hl=zh-tw)並[排程](https://docs.cloud.google.com/bigquery/docs/scheduling-queries?hl=zh-tw)查詢，以便自動執行模型訓練、推論和監控作業。

如果您的 ML 管道包含 [`ML.GENERATE_TEXT` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-generate-text?hl=zh-tw)，請參閱[透過重複呼叫 `ML.GENERATE_TEXT` 處理配額錯誤](https://docs.cloud.google.com/bigquery/docs/iterate-generate-text-calls?hl=zh-tw)，進一步瞭解如何使用 SQL 重複呼叫函式。重複呼叫函式可讓您解決因超出[配額和限制](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#cloud_ai_service_functions)而發生的任何可重試錯誤。

## Dataform

您可以使用 [Dataform](https://docs.cloud.google.com/dataform/docs/overview?hl=zh-tw) 在 BigQuery 中開發、測試、版本管控，並安排資料轉換複雜的 SQL 工作流程。您可以使用 Dataform 執行資料整合的擷取、載入和轉換 (ELT) 程序中的資料轉換等工作。從來源系統擷取原始資料並載入 BigQuery 後，Dataform 可協助您將這些資料轉換為經過明確定義、測試及記錄的資料表套件。

如果 ML 管道包含 [`ML.GENERATE_TEXT` 函式的用法](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-generate-text?hl=zh-tw)，您可以調整 [`structured_table_ml.js` 範例程式庫](https://github.com/dataform-co/dataform-bqml/blob/main/modules/structured_table_ml.js)，以便對函式進行呼叫迭代。重複呼叫函式可讓您解決因超出函式適用的配額和限制而發生的任何可重試錯誤。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-02 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-02 (世界標準時間)。"],[],[]]