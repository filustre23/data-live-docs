Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 預測總覽

預測指的是分析歷來資料，然後據以預測未來趨勢的技術。舉例來說，您可以分析多個門市的銷售資料，以便預測這些門市未來的銷售業績。在 BigQuery ML 中，您會對[時間序列](https://en.wikipedia.org/wiki/Time_series)資料執行預測。

您可以透過下列方式進行預測：

* 使用內建的 [TimesFM 模型](https://docs.cloud.google.com/bigquery/docs/timesfm-model?hl=zh-tw)搭配 [`AI.FORECAST` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-ai-forecast?hl=zh-tw)。如要預測單一變數的未來值，請使用這個方法。這種做法不需要建立及管理模型。
* 使用 [`ML.FORECAST` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-forecast?hl=zh-tw)搭配 [`ARIMA_PLUS` 模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-time-series?hl=zh-tw)。如要執行以 ARIMA 為基礎的建模管道，並將時間序列分解為多個元件來解釋結果，請使用這個方法。這種做法需要您建立及管理模型。
* 使用 [`ML.FORECAST` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-forecast?hl=zh-tw)和 [`ARIMA_PLUS_XREG` 模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-multivariate-time-series?hl=zh-tw)。如要預測多個變數的未來值，請使用這種方法。這種做法需要您建立及管理模型。

除了預測之外，您也可以使用 `ARIMA_PLUS` 和 `ARIMA_PLUS_XREG` 模型偵測異常狀況。詳情請參閱下列文件：

* [異常偵測總覽](https://docs.cloud.google.com/bigquery/docs/anomaly-detection-overview?hl=zh-tw)
* [使用多變數時間序列預測模型執行異常偵測](https://docs.cloud.google.com/bigquery/docs/time-series-anomaly-detection-tutorial?hl=zh-tw)

## 比較 `ARIMA_PLUS` 模型和 TimesFM 模型

請參閱下表，根據您的用途決定要使用 TimesFM、`ARIMA_PLUS` 或 `ARIMA_PLUS_XREG` 模型：

| 模型類型 | `ARIMA_PLUS` 和 `ARIMA_PLUS_XREG` | `TimesFM` |
| --- | --- | --- |
| 模型詳細資料 | 統計模型，趨勢成分使用 `ARIMA` 演算法，非趨勢成分則使用各種其他演算法。詳情請參閱下方的[時間序列模型化管道](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-time-series?hl=zh-tw#modeling-pipeline)和發布內容。 | 以 Transformer 為基礎的基礎模型。詳情請參閱下一列的出版品。 |
| Publication | [ARIMA\_PLUS：Google BigQuery 中大規模、準確、自動且可解讀的資料庫內時間序列預測和異常偵測](https://arxiv.org/abs/2510.24452) | [時間序列預測專用的僅限解碼器基礎模型](https://arxiv.org/pdf/2310.10688) |
| 需要訓練 | 是，每個時間序列都會訓練一個 `ARIMA_PLUS` 或 `ARIMA_PLUS_XREG` 模型。 | 否，TimesFM 模型是預先訓練的模型。 |
| SQL 易用性 | 高。需要 `CREATE MODEL` 陳述式和函式呼叫。 | 非常高。需要單一函式呼叫。 |
| 使用的資料記錄 | 使用訓練資料中的所有時間點，但可自訂為使用較少時間點。 | 使用 512 個時間點。 |
| 準確率 | 非常高。詳情請參閱前幾列列出的出版品。 | 非常高。詳情請參閱前幾列列出的出版品。 |
| 自訂 | 高。[`CREATE MODEL` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-time-series?hl=zh-tw)提供引數，可讓您調整許多模型設定，例如：  * 季節性 * 節慶特效 * 步驟變更 * 趨勢 * 移除尖峰和低谷 * 預測上下限 | 低。 |
| 支援共變數 | 是，使用 [`ARIMA_PLUS_XREG` 模型時可以。](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-multivariate-time-series?hl=zh-tw) | 不用 |
| 可解釋性 | 高。您可以使用 [`ML.EXPLAIN_FORECAST` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-explain-forecast?hl=zh-tw)檢查模型元件。 | 低。 |
| 最佳用途 | * 您想要完全掌控模型，包括自訂模型。 * 您需要模型輸出內容的可解釋性。 | * 您希望盡量簡化設定，不必先建立模型就能進行預測。 |

## 建議的知識

使用 BigQuery ML 陳述式和函式的預設設定，即使沒有太多機器學習知識，也能建立及使用預測模型。不過，如果具備機器學習開發作業的基本知識，尤其是預測模型，有助於您同時最佳化資料和模型，進而獲得更出色的結果。建議您使用下列資源，熟悉機器學習技術和程序：

* [機器學習密集課程](https://developers.google.com/machine-learning/crash-course?hl=zh-tw)
* [機器學習簡介](https://www.kaggle.com/learn/intro-to-machine-learning)
* [中階機器學習](https://www.kaggle.com/learn/intermediate-machine-learning)
* [時間序列](https://www.kaggle.com/learn/time-series)




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-09 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-09 (世界標準時間)。"],[],[]]