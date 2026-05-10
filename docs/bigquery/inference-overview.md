Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 模型推論總覽

本文說明 BigQuery ML 支援的批次推論類型，包括：

* [批次預測](#prediction)
* [線上預測](#online_prediction)

機器學習推論是指將資料點傳送至機器學習模型，據此計算輸出結果，例如單一數值分數。這個程序也稱為「將機器學習模型投入運作」或「將機器學習模型投入正式環境」。

## 批次預測

以下各節說明在 BigQuery ML 中執行預測的可用方式。

### 使用 BigQuery ML 訓練的模型進行推論

BigQuery ML 中的*預測*功能不僅適用於監督式學習模型，也適用於非監督式學習模型。

BigQuery ML 支援透過 [`ML.PREDICT` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-predict?hl=zh-tw)進行預測，支援的模型如下：

| 模型類別 | 模型類型 | `ML.PREDICT` 的用途 |
| --- | --- | --- |
| 監督式學習 | [線性和邏輯迴歸](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-glm?hl=zh-tw)   [提升樹狀結構](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-boosted-tree?hl=zh-tw)   [隨機森林](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-random-forest?hl=zh-tw)   [深層神經網路](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-dnn-models?hl=zh-tw)   [Wide-and-Deep](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-wnd-models?hl=zh-tw)   [AutoML Tables](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-automl?hl=zh-tw) | 預測標籤，迴歸工作會預測數值，分類工作則會預測類別值。 |
| 非監督式學習 | [K-means](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-kmeans?hl=zh-tw) | 將叢集指派給實體。 |
| [PCA](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-pca?hl=zh-tw) | 將實體轉換為特徵向量所跨越的空間，即可對實體套用降維。 |
| [自動編碼器](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-autoencoder?hl=zh-tw) | 將實體轉換為內嵌空間。 |

### 使用匯入的模型進行推論

採用這種方法時，您會在 BigQuery 以外建立及訓練模型，然後使用 [`CREATE MODEL` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create?hl=zh-tw)匯入模型，並使用 [`ML.PREDICT` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-predict?hl=zh-tw)對模型執行推論作業。所有推論處理作業都會在 BigQuery 中進行，並使用 BigQuery 中的資料。匯入的模型可以執行監督式或非監督式學習。

BigQuery ML 支援下列類型的匯入模型：

* [開放式神經網路交換格式 (ONNX)](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-onnx?hl=zh-tw)，適用於以 PyTorch、scikit-learn 和其他熱門機器學習架構訓練的模型。
* [TensorFlow](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-tensorflow?hl=zh-tw)
* [TensorFlow Lite](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-tflite?hl=zh-tw)
* [XGBoost](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-xgboost?hl=zh-tw)

運用這種方法，即可使用各種機器學習架構開發的自訂模型，同時享有 BigQuery ML 的推論速度和資料共置優勢。

如要瞭解詳情，請嘗試下列任一教學課程：

* [使用匯入的 TensorFlow 模型進行預測](https://docs.cloud.google.com/bigquery/docs/making-predictions-with-imported-tensorflow-models?hl=zh-tw)
* [使用 ONNX 格式的 scikit-learn 模型進行預測](https://docs.cloud.google.com/bigquery/docs/making-predictions-with-sklearn-models-in-onnx-format?hl=zh-tw)
* [使用 ONNX 格式的 PyTorch 模型進行預測](https://docs.cloud.google.com/bigquery/docs/making-predictions-with-pytorch-models-in-onnx-format?hl=zh-tw)

### 使用遠端模型進行推論

採用這種做法時，您可以使用 [`CREATE MODEL` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model?hl=zh-tw)，建立對 [Vertex AI 推論](https://docs.cloud.google.com/vertex-ai/docs/predictions/get-predictions?hl=zh-tw)中代管模型的參照，然後使用 [`ML.PREDICT` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-predict?hl=zh-tw)對模型執行推論。所有推論處理作業都會在 Vertex AI 中進行，並使用 BigQuery 中的資料。遠端模型可以執行監督式或非監督式學習。

使用這種方法，對需要 Vertex AI 提供 GPU 硬體支援的大型模型執行推論作業。如果大部分模型都由 Vertex AI 代管，您也可以使用 SQL 對這些模型執行推論，不必手動建構資料管道，將資料傳送至 Vertex AI，再將預測結果傳回 BigQuery。

如需逐步操作說明，請參閱「[在 Vertex AI 上使用遠端模型進行預測](https://docs.cloud.google.com/bigquery/docs/bigquery-ml-remote-model-tutorial?hl=zh-tw)」。

### 在 Vertex AI 中使用 BigQuery 模型進行批次推論

BigQuery ML 內建批次預測支援功能，不需要使用 Vertex AI。您也可以將 BigQuery ML 模型註冊至 Model Registry，以便在 Vertex AI 中使用 BigQuery 表格做為輸入內容，執行批次預測。不過，這項操作只能透過 Vertex AI API 進行，並將 [`InstanceConfig.instanceType`](https://docs.cloud.google.com/vertex-ai/docs/reference/rest/v1/projects.locations.batchPredictionJobs?hl=zh-tw#instanceconfig) 設為 `object`。

## 線上預測

BigQuery ML 的內建推論功能經過最佳化，適用於大規模用途，例如批次預測。BigQuery ML 處理小型輸入資料時，可提供低延遲的推論結果，但您可透過與 [Vertex AI](https://docs.cloud.google.com/bigquery/docs/managing-models-vertex?hl=zh-tw) 的無縫整合，加快線上預測速度。

您可以在 Vertex AI 環境中[管理 BigQuery ML 模型](https://docs.cloud.google.com/bigquery/docs/managing-models-vertex?hl=zh-tw)，不必先從 BigQuery ML 匯出模型，再將模型部署為 Vertex AI 端點。在 Vertex AI 中管理模型，即可存取所有 Vertex AI MLOps 功能，以及 [Vertex AI 特徵儲存庫](https://docs.cloud.google.com/vertex-ai/docs/featurestore/latest/overview?hl=zh-tw)等功能。

此外，您也可以彈性地[將 BigQuery ML 模型匯出](https://docs.cloud.google.com/bigquery/docs/exporting-models?hl=zh-tw)至 Cloud Storage，以便在其他模型代管平台使用。

## 後續步驟

* 如要進一步瞭解如何使用 Vertex AI 模型生成文字和嵌入，請參閱「[生成式 AI 總覽](https://docs.cloud.google.com/bigquery/docs/generative-ai-overview?hl=zh-tw)」。
* 如要進一步瞭解如何使用 Cloud AI API 執行 AI 工作，請參閱「[AI 應用程式總覽](https://docs.cloud.google.com/bigquery/docs/ai-application-overview?hl=zh-tw)」。
* 如要進一步瞭解不同模型類型支援的 SQL 陳述式和函式，請參閱下列文件：

  + [生成式 AI 模型的端對端使用者歷程](https://docs.cloud.google.com/bigquery/docs/e2e-journey-genai?hl=zh-tw)
  + [時間序列預測模型的端對端使用者歷程](https://docs.cloud.google.com/bigquery/docs/e2e-journey-forecast?hl=zh-tw)
  + [機器學習模型的端對端使用者歷程](https://docs.cloud.google.com/bigquery/docs/e2e-journey?hl=zh-tw)
  + [匯入模型的端對端使用者歷程](https://docs.cloud.google.com/bigquery/docs/e2e-journey-import?hl=zh-tw)




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-09 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-09 (世界標準時間)。"],[],[]]