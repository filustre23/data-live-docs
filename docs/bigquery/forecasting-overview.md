Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 預測功能總覽

您可以使用 BigQuery ML 的預測模型分析歷來[時間序列](https://en.wikipedia.org/wiki/Time_series)資料，做出明智的未來趨勢預測。將這些機器學習 (ML) 技術套用至資料，即可預測未來結果，例如預測多個商店地點的近期銷售量。

您可以透過下列方式進行預測：

* 使用 [`AI.FORECAST` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-ai-forecast?hl=zh-tw)搭配內建的 [TimesFM 模型](https://docs.cloud.google.com/bigquery/docs/timesfm-model?hl=zh-tw)。如需預測單一或多個變數的未來值，請使用這個方法。這種方法不需要建立及管理模型。
* 搭配使用 [`ML.FORECAST` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-forecast?hl=zh-tw)和 [`ARIMA_PLUS` 模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-time-series?hl=zh-tw)。如需執行以 ARIMA 為基礎的模型建立管道，並將時間序列分解為多個元件，以便解釋結果，請使用這個方法。這種方法需要您建立及管理模型。
* 搭配使用 [`ML.FORECAST` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-forecast?hl=zh-tw)和 [`ARIMA_PLUS_XREG` 模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-multivariate-time-series?hl=zh-tw)。如需預測多個變數的未來值，請使用這個方法。這種方法需要您建立及管理模型。

除了預測之外，您也可以使用 `ARIMA_PLUS`、`ARIMA_PLUS_XREG` 和 TimesFM 模型偵測異常狀況。詳情請參閱下列文件：

* [異常偵測總覽](https://docs.cloud.google.com/bigquery/docs/anomaly-detection-overview?hl=zh-tw)
* [使用多變數時間序列預測模型執行異常偵測](https://docs.cloud.google.com/bigquery/docs/time-series-anomaly-detection-tutorial?hl=zh-tw)

## 比較 `ARIMA_PLUS` 模型和 TimesFM 模型

請參閱下表，根據您的用途選擇 TimesFM、`ARIMA_PLUS` 或 `ARIMA_PLUS_XREG` 模型：

| 模型類型 | `ARIMA_PLUS` 和 `ARIMA_PLUS_XREG` | `TimesFM` |
| --- | --- | --- |
| 模型詳細資料 | 統計模型，使用 `ARIMA` 演算法處理趨勢元件，並使用各種其他演算法處理非趨勢元件。詳情請參閱「[時間序列建模管道](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-time-series?hl=zh-tw#modeling-pipeline)」和下一列的出版品。 | Transformer 基礎模型。詳情請參閱下一列的出版品。 |
| Publication | [ARIMA\_PLUS：BigQuery 中大規模、準確、自動且可解讀的資料庫內時間序列預測和異常偵測](https://arxiv.org/abs/2510.24452) | * [A Decoder-only Foundation Model for Time-series Forecasting](https://arxiv.org/pdf/2310.10688) * [TimesFM-3：多變數時間序列預測的零樣本基礎模型](https://research.google/blog/timesfm-3-a-zero-shot-foundation-model-for-multivariate-forecasting/?hl=zh-tw) |
| 需要訓練 | 是，系統會為每個時間序列訓練一個 `ARIMA_PLUS` 或 `ARIMA_PLUS_XREG` 模型。 | 否，TimesFM 模型已預先訓練。 |
| SQL 易用性 | 高。需要 `CREATE MODEL` 陳述式和函式呼叫。 | 非常高。需要單一函式呼叫。 |
| 使用的資料記錄 | 使用訓練資料中的所有時間點，但可自訂為使用較少的時間點。 | 可使用 [`AI.FORECAST` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-ai-forecast?hl=zh-tw)的 `context_window` 參數自訂。 |
| 準確率 | 非常高。詳情請參閱前一列列出的出版品。 | 非常高。詳情請參閱前一列列出的出版品。 |
| 自訂 | 高。[`CREATE MODEL` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-time-series?hl=zh-tw)提供引數，可讓您調整多項模型設定，例如：  * 季節性 * 節慶效果 * 步驟變更 * 趨勢 * 移除高峰期和低谷期 * 預測上下限 | 低。 |
| 支援共變量 | 是，使用 [`ARIMA_PLUS_XREG` 模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-multivariate-time-series?hl=zh-tw)時。 | 是，使用 `TimesFM 3.0` 模型 ([預先發布版](https://cloud.google.com/products?hl=zh-tw#product-launch-stages)) 時。 |
| 可解釋性 | 高。您可以使用 [`ML.EXPLAIN_FORECAST` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-explain-forecast?hl=zh-tw)檢查模型元件。 | 低。 |
| 模型評估 | 使用 [`ML.ARIMA_EVALUATE` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-arima-evaluate?hl=zh-tw)。 | 使用 [`AI.EVALUATE` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-ai-evaluate?hl=zh-tw)。 |
| 最佳用途 | * 您想完全控管模型，包括自訂。 * 您需要模型輸出的可解釋性。 | * 您想在不建立模型的情況下進行預測。 * 您需要高效能、預先訓練的基礎模型。 |

## 元件分析

如要深入瞭解資料並改善預測，請使用時間序列元件分析，將時間序列分解為基本模式。下列函式可用於元件分析和預測：

* [`ML.SEASONALITY`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-seasonality?hl=zh-tw)：擷取時間序列的*季節性元件*，代表固定時間範圍 (例如年、週或日) 內重複出現的模式。
* [`ML.TREND`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-trend?hl=zh-tw)：擷取時間序列的*趨勢元件*，代表指標隨時間變化的方向軌跡，並忽略短期波動或雜訊。
* [`ML.DETECT_CHANGE_POINTS`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-detect-change-points?hl=zh-tw)：找出時間序列資料的統計行為或屬性發生變化的時間間隔。這項功能可深入分析重大結構性中斷，而非暫時性或孤立事件。

## 建議的知識

只要使用 BigQuery ML 陳述式和函式的預設設定，即使不具備豐富的機器學習知識，也能建立及使用預測模型。不過，具備機器學習開發的基本知識，尤其是預測模型，有助於您最佳化資料和模型，進而取得更理想的結果。建議您使用下列資源，熟悉機器學習技術和程序：

* [機器學習密集課程](https://developers.google.com/machine-learning/crash-course?hl=zh-tw)
* [機器學習簡介](https://www.kaggle.com/learn/intro-to-machine-learning)
* [中級機器學習](https://www.kaggle.com/learn/intermediate-machine-learning)
* [時間序列](https://www.kaggle.com/learn/time-series)




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-11-23 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-11-23 (世界標準時間)。"],[],[]]