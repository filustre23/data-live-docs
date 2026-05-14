Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 匯入模型的端對端使用者歷程

本文說明從 Cloud Storage 匯入至 BigQuery ML 的機器學習模型使用者歷程，包括可用於處理匯入模型的陳述式和函式。BigQuery ML 提供下列類型的匯入模型：

* [開放類神經網路交換格式 (ONNX)](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-onnx?hl=zh-tw)
* [TensorFlow](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-tensorflow?hl=zh-tw)
* [TensorFlow Lite](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-tflite?hl=zh-tw)
* [XGBoost](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-xgboost?hl=zh-tw)

## 匯入的模型使用者歷程

下表說明可用於建立及使用匯入模型的陳述式和函式：

| 模型類型 | 模型建立 | [推論](https://docs.cloud.google.com/bigquery/docs/inference-overview?hl=zh-tw) | 教學課程 |
| --- | --- | --- | --- |
| TensorFlow | [`CREATE MODEL`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-tensorflow?hl=zh-tw) | [`ML.PREDICT`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-predict?hl=zh-tw) | [使用匯入的 TensorFlow 模型進行預測](https://docs.cloud.google.com/bigquery/docs/making-predictions-with-imported-tensorflow-models?hl=zh-tw) |
| TensorFlow Lite | [`CREATE MODEL`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-tflite?hl=zh-tw) | [`ML.PREDICT`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-predict?hl=zh-tw) | 不適用 |
| 開放類神經網路交換格式 (ONNX) | [`CREATE MODEL`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-onnx?hl=zh-tw) | [`ML.PREDICT`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-predict?hl=zh-tw) | * [使用 ONNX 格式的 scikit-learn 模型進行預測](https://docs.cloud.google.com/bigquery/docs/making-predictions-with-sklearn-models-in-onnx-format?hl=zh-tw) * [以 ONNX 格式預測 PyTorch 模型](https://docs.cloud.google.com/bigquery/docs/making-predictions-with-pytorch-models-in-onnx-format?hl=zh-tw) |
| XGBoost | [`CREATE MODEL`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-xgboost?hl=zh-tw) | [`ML.PREDICT`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-predict?hl=zh-tw) | 不適用 |




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-14 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-14 (世界標準時間)。"],[],[]]