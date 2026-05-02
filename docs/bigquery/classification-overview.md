* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 分類總覽

機器學習的常見用途，就是使用以類似已標記資料訓練的模型，分類新資料。舉例來說，您可能想預測電子郵件是否為垃圾郵件，或是顧客的產品評論是正面、負面或中立。

您可以搭配下列任一模型使用 [`ML.PREDICT` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-predict?hl=zh-tw)來執行分類作業：

* [邏輯迴歸模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-glm?hl=zh-tw)：將 `MODEL_TYPE` 選項設為 `LOGISTIC_REG`，即可使用[邏輯迴歸](https://developers.google.com/machine-learning/crash-course/logistic-regression?hl=zh-tw)。
* [增強型樹狀模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-boosted-tree?hl=zh-tw)：將 `MODEL_TYPE` 選項設為 `BOOSTED_TREE_CLASSIFIER`，即可使用[梯度提升決策樹](https://developers.google.com/machine-learning/decision-forests/intro-to-gbdt?hl=zh-tw)。
* [隨機樹系模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-random-forest?hl=zh-tw)：將 `MODEL_TYPE` 選項設為 `RANDOM_FOREST_CLASSIFIER`，即可使用[隨機樹系](https://developers.google.com/machine-learning/decision-forests/intro-to-decision-forests?hl=zh-tw)。
* [深層類神經網路 (DNN) 模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-dnn-models?hl=zh-tw)：將 `MODEL_TYPE` 選項設為 `DNN_CLASSIFIER`，即可使用[神經網路](https://developers.google.com/machine-learning/crash-course/neural-networks?hl=zh-tw)。
* [廣度和深度模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-wnd-models?hl=zh-tw)：將 `MODEL_TYPE` 選項設為 `DNN_LINEAR_COMBINED_CLASSIFIER`，即可使用[廣度和深度學習](https://dl.acm.org/doi/10.1145/2988450.2988454)。
* [AutoML 模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-automl?hl=zh-tw)：將 `MODEL_TYPE` 選項設為 `AUTOML_CLASSIFIER`，即可使用 [AutoML 分類模型](https://docs.cloud.google.com/vertex-ai/docs/tabular-data/classification-regression/overview?hl=zh-tw)。

## 建議的知識

只要使用 `CREATE MODEL` 陳述式和 `ML.PREDICT` 函式中的預設設定，即使沒有太多機器學習知識，也能建立及使用分類模型。不過，瞭解機器學習開發的基本知識，有助您最佳化資料和模型，進而獲得更優異的結果。建議您參考下列資源，熟悉機器學習技術和程序：

* [機器學習密集課程](https://developers.google.com/machine-learning/crash-course?hl=zh-tw)
* [機器學習簡介](https://www.kaggle.com/learn/intro-to-machine-learning)
* [中級機器學習](https://www.kaggle.com/learn/intermediate-machine-learning)




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-02 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-02 (世界標準時間)。"],[],[]]