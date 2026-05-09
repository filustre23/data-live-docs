Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 時間序列預測模型的端對端使用者歷程

本文說明 BigQuery ML 時間序列預測模型的使用者歷程，包括可用於處理時間序列預測模型的陳述式和函式。BigQuery ML 提供下列類型的時間序列預測模型：

* [`ARIMA_PLUS`單變數模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-time-series?hl=zh-tw)
* [`ARIMA_PLUS_XREG` 多變數模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-multivariate-time-series?hl=zh-tw)
* [TimesFM 單變數模型](https://docs.cloud.google.com/bigquery/docs/timesfm-model?hl=zh-tw)

## 模型建立使用者歷程

下表說明可用於建立時間序列預測模型的陳述式和函式：

| 模型類型 | 模型建立 | [預先處理特徵](https://docs.cloud.google.com/bigquery/docs/preprocess-overview?hl=zh-tw) | [超參數調整](https://docs.cloud.google.com/bigquery/docs/hp-tuning-overview?hl=zh-tw) | [模型權重](https://docs.cloud.google.com/bigquery/docs/weights-overview?hl=zh-tw) | 教學課程 |
| --- | --- | --- | --- | --- | --- |
| `ARIMA_PLUS` | [`CREATE MODEL`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-time-series?hl=zh-tw) | [自動預先處理](https://docs.cloud.google.com/bigquery/docs/auto-preprocessing?hl=zh-tw) | [auto.ARIMA1](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-time-series?hl=zh-tw#auto_arima) 自動微調 | [`ML.ARIMA_COEFFICIENTS`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-arima-coefficients?hl=zh-tw) | * [預測單一時間序列](https://docs.cloud.google.com/bigquery/docs/arima-single-time-series-forecasting-tutorial?hl=zh-tw) * [預測多個時間序列](https://docs.cloud.google.com/bigquery/docs/arima-multiple-time-series-forecasting-tutorial?hl=zh-tw) * [預測數百萬個時間序列](https://docs.cloud.google.com/bigquery/docs/arima-speed-up-tutorial?hl=zh-tw) * [使用自訂節慶](https://docs.cloud.google.com/bigquery/docs/time-series-forecasting-holidays-tutorial?hl=zh-tw) * [限制預估值](https://docs.cloud.google.com/bigquery/docs/arima-time-series-forecasting-with-limits-tutorial?hl=zh-tw) * [執行階層式時間序列預測](https://docs.cloud.google.com/bigquery/docs/arima-time-series-forecasting-with-hierarchical-time-series?hl=zh-tw) * [使用多變數時間序列預測模型執行異常偵測](https://docs.cloud.google.com/bigquery/docs/time-series-anomaly-detection-tutorial?hl=zh-tw) |
| `ARIMA_PLUS_XREG` | [`CREATE MODEL`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-multivariate-time-series?hl=zh-tw) | [自動預先處理](https://docs.cloud.google.com/bigquery/docs/auto-preprocessing?hl=zh-tw) | [auto.ARIMA1](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-multivariate-time-series?hl=zh-tw#auto_arima) 自動微調 | [`ML.ARIMA_COEFFICIENTS`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-arima-coefficients?hl=zh-tw) | * [預測單一時間序列](https://docs.cloud.google.com/bigquery/docs/arima-plus-xreg-single-time-series-forecasting-tutorial?hl=zh-tw) * [預測多個時間序列](https://docs.cloud.google.com/bigquery/docs/arima-plus-xreg-multiple-time-series-forecasting-tutorial?hl=zh-tw) |
| TimesFM | 不適用 | 不適用 | 不適用 | 不適用 | [預測多個時間序列](https://docs.cloud.google.com/bigquery/docs/timesfm-time-series-forecasting-tutorial?hl=zh-tw) |

1 auto.ARIMA 演算法會對趨勢模組執行超參數調整。整個模型化管道不支援超參數調整。詳情請參閱[模型化管道](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-time-series?hl=zh-tw#modeling-pipeline)。

## 模擬使用者的歷程

下表說明可用於評估、說明及取得時間序列預測模型預測結果的陳述式和函式：

| 模型類型 | [評估](https://docs.cloud.google.com/bigquery/docs/evaluate-overview?hl=zh-tw) | [推論](https://docs.cloud.google.com/bigquery/docs/inference-overview?hl=zh-tw) | [AI 說明](https://docs.cloud.google.com/bigquery/docs/xai-overview?hl=zh-tw) |
| --- | --- | --- | --- |
| `ARIMA_PLUS` | [`ML.EVALUATE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-evaluate?hl=zh-tw)1   [`ML.ARIMA_EVALUATE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-arima-evaluate?hl=zh-tw)   [`ML.HOLIDAY_INFO`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-holiday-info?hl=zh-tw) | [`ML.FORECAST`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-forecast?hl=zh-tw)   [`ML.DETECT_ANOMALIES`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-detect-anomalies?hl=zh-tw) | [`ML.EXPLAIN_FORECAST`2](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-explain-forecast?hl=zh-tw) |
| `ARIMA_PLUS_XREG` | [`ML.EVALUATE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-evaluate?hl=zh-tw)1   [`ML.ARIMA_EVALUATE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-arima-evaluate?hl=zh-tw)   [`ML.HOLIDAY_INFO`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-holiday-info?hl=zh-tw) | [`ML.FORECAST`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-forecast?hl=zh-tw)   [`ML.DETECT_ANOMALIES`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-detect-anomalies?hl=zh-tw) | [`ML.EXPLAIN_FORECAST`2](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-explain-forecast?hl=zh-tw) |
| TimesFM | [`AI.EVALUATE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-ai-evaluate?hl=zh-tw) | [`AI.FORECAST`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-ai-forecast?hl=zh-tw) | 不適用 |

1 您可以將評估資料輸入 `ML.EVALUATE` 函式，計算預測指標，例如平均絕對百分比誤差 (MAPE)。如果沒有評估資料，可以使用 `ML.ARIMA_EVALUATE` 函式輸出模型相關資訊，例如漂移和變異數。

2：`ML.EXPLAIN_FORECAST` 函式包含 `ML.FORECAST` 函式，因為其輸出內容是 `ML.FORECAST` 結果的超集。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-08 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-08 (世界標準時間)。"],[],[]]