Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# BigQuery 中的機器學習簡介

**注意：** 使用以特定 BigQuery 版本建立的預留項目時，這項功能可能無法使用。如要進一步瞭解各版本啟用的功能，請參閱「[BigQuery 版本簡介](https://docs.cloud.google.com/bigquery/docs/editions-intro?hl=zh-tw)」。

BigQuery ML 可讓您使用 GoogleSQL 查詢或 Google Cloud 控制台，[建立及執行機器學習 (ML) 模型](https://docs.cloud.google.com/bigquery/docs/e2e-journey?hl=zh-tw)。BigQuery ML 模型會儲存在 BigQuery 資料集中，與資料表和檢視區塊類似。您也可以透過 BigQuery ML 存取 [Vertex AI 模型](https://docs.cloud.google.com/bigquery/docs/generative-ai-overview?hl=zh-tw)和 [Cloud AI API](https://docs.cloud.google.com/bigquery/docs/ai-application-overview?hl=zh-tw)，執行人工智慧 (AI) 任務，例如生成文字或進行機器翻譯。Gemini 版 Google Cloud 也提供 AI 輔助功能，可協助您處理 BigQuery 工作。如要查看 BigQuery 的 AI 輔助功能清單，請參閱 [Gemini in BigQuery 總覽](https://docs.cloud.google.com/bigquery/docs/gemini-overview?hl=zh-tw)。

一般來說，對大型資料集執行機器學習或 AI 技術，需要經過大量程式設計，並具備機器學習架構的知識。因此每間公司只有少數人員能開發解決方案。這些人還不包含資料分析師，因為分析師雖然瞭解資料，但機器學習和程式設計專業知識有限。但透過 BigQuery ML，SQL 從業人員能運用現有的 SQL 工具和技能來建構及評估模型，並以 LLM 和 Cloud AI API 生成結果。

您可以透過以下管道使用 BigQuery ML 功能：

* Google Cloud 控制台使用者介面，可[透過 UI 使用模型](https://docs.cloud.google.com/bigquery/docs/create-machine-learning-model-console?hl=zh-tw)。([預覽](https://cloud.google.com/products?hl=zh-tw#product-launch-stages))
* Google Cloud 控制台查詢編輯器，可使用 SQL 查詢處理模型。
* bq 指令列工具
* BigQuery REST API
* BigQuery 中的整合式 [Colab Enterprise 筆記本](https://docs.cloud.google.com/bigquery/docs/notebooks-introduction?hl=zh-tw)
* Jupyter 筆記本或商業智慧平台等外部工具

## 使用 BigQuery ML 的好處

相較於其他將機器學習或 AI 與雲端式資料倉儲搭配使用的做法，BigQuery ML 能為您帶來多項好處：

* 透過 BigQuery ML，資料分析人員可以使用現有的商業智慧工具與試算表來建立及執行模型，讓所有人員都能使用機器學習和 AI 技術。預測分析可以提供資訊，做為整個機構的業務決策依據。
* 您不必使用 Python 或 Java 設計機器學習/AI 解決方案，您可以使用資料分析師熟悉的 SQL 語言訓練模型及存取 AI 資源。
* BigQuery ML 可免除從資料倉儲移動資料的需求，進而加快模型開發和創新速度。BigQuery ML 會將機器學習技術導入資料中，這有以下優點：

  + 需要的工具較少，因此複雜度降低。
  + 您不需要針對 Python 機器學習架構，遷移大量資料並設定資料格式，就能在 BigQuery 訓練資料，因此可加快投入生產的速度。

  詳情請觀看「[如何運用 BigQuery ML 加快機器學習開發作業](https://www.youtube.com/watch?v=EUPBVv9tp38&hl=zh-tw)」影片。

## 建議的知識

您可以使用 `CREATE MODEL` 陳述式和推論函式的預設設定，建立及使用 BigQuery ML 模型，即使沒有太多機器學習知識也能輕鬆上手。不過，如果具備機器學習開發生命週期的基本知識，例如特徵工程和模型訓練，有助於最佳化資料和模型，進而獲得更出色的結果。建議您使用下列資源，熟悉機器學習技術和程序：

* [機器學習密集課程](https://developers.google.com/machine-learning/crash-course?hl=zh-tw)
* [機器學習簡介](https://www.kaggle.com/learn/intro-to-machine-learning)
* [資料清理](https://www.kaggle.com/learn/data-cleaning)
* [特徵工程](https://www.kaggle.com/learn/feature-engineering)
* [中階機器學習](https://www.kaggle.com/learn/intermediate-machine-learning)

## 使用時間序列

您可以使用 TimesFM、`ARIMA_PLUS` 和 `ARIMA_PLUS_XREG` 模型，對時間序列資料執行[預測](https://docs.cloud.google.com/bigquery/docs/forecasting-overview?hl=zh-tw)和[異常偵測](https://docs.cloud.google.com/bigquery/docs/anomaly-detection-overview?hl=zh-tw)。

## 執行貢獻分析

您可以建立[貢獻度分析](https://docs.cloud.google.com/bigquery/docs/contribution-analysis?hl=zh-tw)模型，產生多維度資料中重要指標變化的洞察資料。舉例來說，您可以找出哪些資料導致收益變動。

## 支援的模型

BigQuery ML 中的[模型](https://developers.google.com/machine-learning/glossary/?hl=zh-tw#model)會呈現 ML 系統自訓練資料學習到的內容。以下各節說明 BigQuery ML 支援的模型類型。如要進一步瞭解如何為不同類型的模型建立預留指派作業，請參閱「[將運算單元指派給 BigQuery ML 工作負載](https://docs.cloud.google.com/bigquery/docs/reservations-assignments?hl=zh-tw#assign-ml-workload)」。

### 內部訓練的模型

BigQuery ML 內建下列模型：

* [貢獻度分析](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-contribution-analysis?hl=zh-tw)可判斷一或多個維度對特定指標值的影響。例如，查看商店位置和銷售日期對商店收益的影響。詳情請參閱「[貢獻分析總覽](https://docs.cloud.google.com/bigquery/docs/contribution-analysis?hl=zh-tw)」。
* [線性迴歸](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-glm?hl=zh-tw)：使用以類似遠端資料訓練的模型，預測新資料的數值指標值。標籤為實值，也就是說，標籤不可為正無限大、負無限大或 NaN (非數字)。
* [邏輯迴歸](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-glm?hl=zh-tw)適用於分類兩個以上的可能值，例如輸入是 `low-value`、`medium-value` 或 `high-value`。標籤最多可有 50 個不重複的值。
* [K-means 叢集](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-kmeans?hl=zh-tw)：適用於資料區隔。舉例來說，這個模型會找出顧客區隔。K-means 是一種非監督式的學習技術，讓模型訓練無須藉助標籤或拆分資料即可執行訓練或評估。
* [矩陣分解](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-matrix-factorization?hl=zh-tw)適用於建立產品建議系統。您可以根據過往的顧客行為、交易和產品評分建立產品建議，然後將這些建議用於個人化顧客體驗。
* [主成分分析 (PCA)](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-pca?hl=zh-tw) 是指計算主成分，並使用這些主成分對資料執行基底變更的程序。通常用於維度縮減，方法是將每個資料點投影到前幾個主成分上，以取得低維度資料，同時盡可能保留資料的變異。
* 時間序列可用於執行時間序列預測和異常偵測。
  [`ARIMA_PLUS`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-time-series?hl=zh-tw)
  和
  [`ARIMA_PLUS_XREG`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-multivariate-time-series?hl=zh-tw)
  時間序列模型提供多種調整選項，並自動處理異常狀況、季節性和節慶。

  如果不想自行管理時間序列預測模型，可以使用 [`AI.FORECAST` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-ai-forecast?hl=zh-tw)，搭配 BigQuery ML 內建的 [TimesFM 時間序列模型](https://docs.cloud.google.com/bigquery/docs/timesfm-model?hl=zh-tw) ([搶先版](https://cloud.google.com/products?hl=zh-tw#product-launch-stages)) 執行預測。

您可以對內部訓練的模型執行 [模擬測試](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#dry-run)，估算執行 `CREATE MODEL` 陳述式時，模型會處理多少資料。

### 外部訓練的模型

下列模型屬於 BigQuery ML 外部模型，且在 Vertex AI 中訓練：

* [深層類神經網路 (DNN)](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-dnn-models?hl=zh-tw)：用於建立以 TensorFlow 為基礎的深層類神經網路，適用於分類和迴歸模型。
* [Wide & Deep](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-wnd-models?hl=zh-tw)
  適用於一般的大規模迴歸和分類問題，
  且輸入內容稀疏
  ([類別特徵](https://en.wikipedia.org/wiki/Categorical_variable)具有大量可能的特徵值)，例如推薦系統、搜尋和排名問題。
* [自動編碼器](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-autoencoder?hl=zh-tw)：用於建立以 TensorFlow 為基礎的模型，並支援稀疏資料表示法。您可以在 BigQuery ML 中使用這些模型，執行非監督式異常偵測和非線性降維等工作。
* [增強型樹狀結構](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-boosted-tree?hl=zh-tw)：用於建立以 [XGBoost](https://xgboost.readthedocs.io/en/latest/) 為基礎的分類和迴歸模型。
* [隨機森林](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-random-forest?hl=zh-tw)：
  在訓練期間，建構多個學習方法決策樹，用於分類、迴歸和其他工作。
* [AutoML](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-automl?hl=zh-tw)
  是一種監督式機器學習服務，可快速且大規模地建構及部署表格資料的分類和迴歸模型。

您無法對外部訓練模型執行 [模擬測試](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#dry-run)，以估算執行 `CREATE MODEL` 陳述式時處理的資料量。

### 遠端模型

您可以在 BigQuery 建立[遠端模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model?hl=zh-tw#endpoint)，使用部署至 [Vertex AI](https://docs.cloud.google.com/vertex-ai/docs?hl=zh-tw) 的模型。您必須在遠端模型的 `CREATE MODEL` 陳述式中，指定部署的模型 [HTTPS 端點](https://docs.cloud.google.com/vertex-ai/docs/general/deployment?hl=zh-tw#what_happens_when_you_deploy_a_model)，藉此參照該模型。

遠端模型的 `CREATE MODEL` 陳述式不會處理任何資料，因此不會產生 BigQuery 費用。

### 匯入的模型

BigQuery ML 可讓您匯入在 BigQuery 以外訓練的自訂模型，然後在 BigQuery 內執行預測作業。您可以將 [Cloud Storage](https://docs.cloud.google.com/storage?hl=zh-tw) 中的以下模型匯入 BigQuery：

* [開放式神經網路交換格式 (ONNX)](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-onnx?hl=zh-tw) 是表示機器學習模型的開放標準格式。使用 ONNX，您可以在 BigQuery ML 中使用以 PyTorch 和 scikit-learn 等熱門機器學習架構訓練的模型。
* [TensorFlow](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-tensorflow?hl=zh-tw) 是免費的開放原始碼軟體程式庫，適用於機器學習和人工智慧。TensorFlow 可用於各種工作，但特別著重於訓練和推論深度類神經網路。您可以將先前訓練的 TensorFlow 模型載入 BigQuery，做為 BigQuery ML 模型，然後在 BigQuery ML 中執行預測。
* [TensorFlow Lite](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-tflite?hl=zh-tw) 是 TensorFlow 的輕量版本，適用於行動裝置、微控制器和其他邊緣裝置。TensorFlow 會最佳化現有的 TensorFlow 模型，以縮減模型大小並加快推論速度。
* [XGBoost](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-xgboost?hl=zh-tw) 是一種經過最佳化的分散式梯度提升程式庫，具備高效率、彈性和可攜性。這個架構會在[梯度提升](https://en.wikipedia.org/wiki/Gradient_boosting)架構下實作機器學習演算法。

匯入的模型 `CREATE MODEL` 陳述式不會處理任何位元組，因此不會產生 BigQuery 費用。

在 BigQuery ML 中，您可以將模型與多個 BigQuery 資料集的資料搭配使用，以便進行訓練和預測。

### 模型選取指南

[下載模型選擇決策樹狀圖。](https://docs.cloud.google.com/static/bigquery/images/ml-model-cheatsheet.pdf?hl=zh-tw)

## BigQuery ML 和 Vertex AI

BigQuery ML 與 Vertex AI 整合，後者是 Google Cloud中 AI 和 ML 的端對端平台。您可以將 BigQuery ML 模型註冊至 Model Registry，以便將這些模型部署至端點以進行線上預測。詳情請參閱下列文章：

* 如要進一步瞭解如何搭配使用 BigQuery ML 模型與 Vertex AI，請參閱「[透過 Vertex AI 管理 BigQuery ML 模型](https://docs.cloud.google.com/bigquery/docs/managing-models-vertex?hl=zh-tw)」。
* 如果您不熟悉 Vertex AI，並想進一步瞭解如何與 BigQuery ML 整合，請參閱「[Vertex AI for BigQuery users](https://docs.cloud.google.com/vertex-ai/docs/beginner/bqml?hl=zh-tw)」(適用於 BigQuery 使用者的 Vertex AI)。
* 觀看「[如何透過 Vertex AI 和 BigQuery ML 簡化 AI 模型](https://www.youtube.com/watch?v=AVwwkqLOito&hl=zh-tw)」影片。

## BigQuery ML 和 Colab Enterprise

您現在可以使用 Colab Enterprise 筆記本，在 BigQuery 中執行機器學習工作流程。您可以使用 SQL、Python 和其他熱門程式庫和語言，在 Notebook 中完成機器學習工作。詳情請參閱「[建立筆記本](https://docs.cloud.google.com/bigquery/docs/create-notebooks?hl=zh-tw)」。

## 支援的地區

BigQuery ML 支援的區域與 BigQuery 相同。詳情請參閱 [BigQuery ML 位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw#bqml-loc)。

## 定價

您需要支付訓練模型和對模型執行查詢所用的運算資源費用。您建立的模型類型會影響模型的訓練位置，以及適用於該作業的價格。對模型執行的查詢一律會在 BigQuery 中執行，並採用 [BigQuery 計算價格](https://cloud.google.com/bigquery/pricing?hl=zh-tw#analysis_pricing_models)。由於[遠端模型](#remote_models)會呼叫 Vertex AI 模型，因此對遠端模型發出的查詢也會產生 Vertex AI 費用。

我們會根據 [BigQuery 儲存空間定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#storage)，向您收取訓練模型所用儲存空間的費用。

詳情請參閱「[BigQuery ML 定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#bqml)」一文。

## 配額

除了 [BigQuery ML 特有的限制](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#bqml-quotas)之外，使用 BigQuery ML 函式和 `CREATE MODEL` 陳述式的查詢也受限於 BigQuery [查詢工作](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#query_jobs)的配額和限制。

## 限制

* BigQuery ML 不適用於[標準版](https://docs.cloud.google.com/bigquery/docs/editions-intro?hl=zh-tw)。

## 後續步驟

* 如要開始使用 BigQuery ML，請參閱[在 BigQuery ML 中建立機器學習模型](https://docs.cloud.google.com/bigquery/docs/create-machine-learning-model?hl=zh-tw)。
* 如要進一步瞭解機器學習與 BigQuery ML，請參考下列資源：
  + [智慧型數據分析和資料管理](https://cloud.google.com/learn/training/data-engineering-and-analytics?hl=zh-tw)訓練計畫
  + [機器學習密集課程](https://developers.google.com/machine-learning/crash-course/?hl=zh-tw)
  + [機器學習詞彙表](https://developers.google.com/machine-learning/glossary/?hl=zh-tw)
* 如要瞭解如何透過 Model Registry 執行 MLOps，請參閱「
  [在 Vertex AI 中管理 BigQuery ML 模型](https://docs.cloud.google.com/bigquery/docs/managing-models-vertex?hl=zh-tw)」。
* 如要進一步瞭解不同模型類型支援的 SQL 陳述式和函式，請參閱下列文件：

  + [生成式 AI 模型的端對端使用者歷程](https://docs.cloud.google.com/bigquery/docs/e2e-journey-genai?hl=zh-tw)
  + [時間序列預測模型的端對端使用者歷程](https://docs.cloud.google.com/bigquery/docs/e2e-journey-forecast?hl=zh-tw)
  + [機器學習模型的端對端使用者歷程](https://docs.cloud.google.com/bigquery/docs/e2e-journey?hl=zh-tw)
  + [匯入模型的端對端使用者歷程](https://docs.cloud.google.com/bigquery/docs/e2e-journey-import?hl=zh-tw)
  + [貢獻分析使用者歷程](https://docs.cloud.google.com/bigquery/docs/contribution-analysis?hl=zh-tw#contribution_analysis_user_journey)




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-16 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-16 (世界標準時間)。"],[],[]]