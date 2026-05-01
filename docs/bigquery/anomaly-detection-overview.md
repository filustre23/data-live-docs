* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 異常偵測總覽

異常偵測是一種資料探勘技術，可用來找出特定資料集中的資料偏差問題。舉例來說，如果特定產品的退貨率攀升，比該產品的基準值高出許多，可能表示該產品有瑕疵，或疑似發生詐欺事件。您可以運用這項技術來偵測重大事件，如技術問題，或消費者行為變動等潛在機會。

判斷哪些資料屬於異常資料可能相當困難。如果您不確定哪些資料屬於異常資料，或是沒有標註資料可訓練模型，可以使用非監督式機器學習執行異常偵測。使用 [`AI.DETECT_ANOMALIES` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-ai-detect-anomalies?hl=zh-tw)或 [`ML.DETECT_ANOMALIES` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-detect-anomalies?hl=zh-tw)搭配下列其中一個模型，偵測訓練資料或新服務資料中的異常狀況：

| 資料類型 | 模型類型 | 函式 | 函式用途 |
| --- | --- | --- | --- |
| 時間序列 | [`TimesFM`](https://docs.cloud.google.com/bigquery/docs/timesfm-model?hl=zh-tw) | `AI.DETECT_ANOMALIES` | 偵測時間序列中的異常狀況。 |
| [`ARIMA_PLUS`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-time-series?hl=zh-tw) | `ML.DETECT_ANOMALIES` | 偵測時間序列中的異常狀況。 |
| [`ARIMA_PLUS_XREG`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-multivariate-time-series?hl=zh-tw) | `ML.DETECT_ANOMALIES` | 使用外部迴歸因子偵測時間序列中的異常狀況。 |
| [獨立同分布隨機變數 (IID)](https://en.wikipedia.org/wiki/Independent_and_identically_distributed_random_variables) | [K-means](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-kmeans?hl=zh-tw) | `ML.DETECT_ANOMALIES` | 根據輸入資料與各叢集質心之間最短的標準化距離，偵測異常狀況。如要瞭解標準化距離的定義，請參閱 [`ML.DETECT_ANOMALIES` 函式的 k-means 模型輸出內容](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-detect-anomalies?hl=zh-tw#k-means_model_output)。 |
| [自動編碼器](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-autoencoder?hl=zh-tw) | 根據均方誤差的重建損失偵測異常狀況。詳情請參閱 `ML.RECONSTRUCTION_LOSS`。`ML.RECONSTRUCTION_LOSS` 函式可以擷取所有類型的重建損失。 |
| [PCA](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-pca?hl=zh-tw) | 根據均方誤差的重建損失偵測異常狀況。 |

如果您已有標示異常狀況的資料，可以使用 [`ML.PREDICT` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-predict?hl=zh-tw)搭配下列其中一個監督式機器學習模型，執行異常偵測：

* [線性迴歸和邏輯迴歸模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-glm?hl=zh-tw)
* [強化型樹狀結構模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-boosted-tree?hl=zh-tw)
* [隨機樹系模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-random-forest?hl=zh-tw)
* [深層類神經網路 (DNN) 模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-dnn-models?hl=zh-tw)
* [廣度和深度模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-wnd-models?hl=zh-tw)
* [AutoML 模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-automl?hl=zh-tw)

## 建議的知識

只要使用 `CREATE MODEL` 陳述式和推論函式的預設設定，即使沒有太多機器學習知識，也能建立及使用異常偵測模型。不過，具備機器學習開發的基本知識，有助於您最佳化資料和模型，進而獲得更出色的結果。建議您使用下列資源，熟悉機器學習技術和程序：

* [機器學習密集課程](https://developers.google.com/machine-learning/crash-course?hl=zh-tw)
* [機器學習簡介](https://www.kaggle.com/learn/intro-to-machine-learning)
* [中階機器學習](https://www.kaggle.com/learn/intermediate-machine-learning)




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-04-30 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-04-30 (世界標準時間)。"],[],[]]