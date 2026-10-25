Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 分類總覽

機器學習的常見用途是使用以類似標籤資料訓練的模型，對新資料進行分類。舉例來說，您可能想預測電子郵件是否為垃圾內容，或是顧客的產品評論是正面、負面或中性。

您可以搭配 [`ML.PREDICT` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-predict?hl=zh-tw)使用下列任一模型進行分類：

* [邏輯迴歸模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-glm?hl=zh-tw)：將 `MODEL_TYPE` 選項設為 `LOGISTIC_REG`，即可使用[邏輯迴歸](https://developers.google.com/machine-learning/crash-course/logistic-regression?hl=zh-tw)。
* [增強型樹狀結構模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-boosted-tree?hl=zh-tw)：
  將 `MODEL_TYPE` 選項設為 `BOOSTED_TREE_CLASSIFIER`，即可使用[梯度增強決策樹](https://developers.google.com/machine-learning/decision-forests/intro-to-gbdt?hl=zh-tw)。
* [隨機樹系模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-random-forest?hl=zh-tw)：
  將 `MODEL_TYPE` 選項設為 `RANDOM_FOREST_CLASSIFIER`，即可使用[隨機樹系](https://developers.google.com/machine-learning/decision-forests/intro-to-decision-forests?hl=zh-tw)。
* [深層類神經網路 (DNN) 模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-dnn-models?hl=zh-tw)：
  將 `MODEL_TYPE` 選項設為 `DNN_CLASSIFIER`，即可使用[類神經網路](https://developers.google.com/machine-learning/crash-course/neural-networks?hl=zh-tw)。
* [廣度和深度模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-wnd-models?hl=zh-tw)：
  將 `MODEL_TYPE` 選項設為 `DNN_LINEAR_COMBINED_CLASSIFIER`，即可使用[廣度和深度學習](https://dl.acm.org/doi/10.1145/2988450.2988454)。
* [AutoML 模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-automl?hl=zh-tw)：
  將 `MODEL_TYPE` 選項設為 `AUTOML_CLASSIFIER`，即可使用 [AutoML 分類模型](https://docs.cloud.google.com/gemini-enterprise-agent-platform/machine-learning/tabular-data/classification-regression/overview?hl=zh-tw)。

或者，您可以使用 [`AI.PREDICT` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-ai-predict?hl=zh-tw)，透過內建的 [TabFM 模型](https://docs.cloud.google.com/bigquery/docs/tabfm-model?hl=zh-tw)分類資料。您可以使用 [`AI.EVALUATE` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-ai-evaluate?hl=zh-tw)評估模型成效。

## 建議的知識

您可以使用 `CREATE MODEL` 陳述式和 `ML.PREDICT` 函式的預設設定，建立及使用分類模型，即使沒有太多機器學習知識也沒問題。不過，具備機器學習開發的基本知識，有助於您最佳化資料和模型，進而獲得更出色的結果。建議您使用下列資源，熟悉機器學習技術和程序：

* [機器學習密集課程](https://developers.google.com/machine-learning/crash-course?hl=zh-tw)
* [機器學習簡介](https://www.kaggle.com/learn/intro-to-machine-learning)
* [中階機器學習](https://www.kaggle.com/learn/intermediate-machine-learning)




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-10-24 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-10-24 (世界標準時間)。"],[],[]]