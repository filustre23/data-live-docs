Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# BigQuery 可解釋 AI 總覽

本文說明 BigQuery ML 如何支援可解釋的 AI (有時稱為 XAI)。

可解釋 AI 可定義資料列中各項特徵對預測結果的影響程度，協助您瞭解預測機器學習模型為分類和迴歸工作產生的結果。這項資訊通常稱為「功能歸因」。有了這項資訊，您就能確認模型的行為是否符合預期、找出模型偏誤，以及探索改善模型和訓練資料的方式。

## 局部與全域可解釋性

可解釋性分為兩種：局部可解釋性和全域可解釋性。這分別稱為「本機特徵重要性」和「全域特徵重要性」。

* 局部可解釋性會傳回每個已說明範例的特徵歸因值。這些值說明特定特徵對預測的影響程度，相較於基準預測。
* 全域可解釋性會傳回特徵對模型的整體影響，通常是透過彙整整個資料集的特徵歸因來取得。絕對值越大，表示該特徵對模型預測結果的影響越大。

## BigQuery ML 中的可解釋 AI 產品

BigQuery ML 中的可解釋 AI 支援各種機器學習模型，包括時間序列和非時間序列模型。每個模型都採用不同的可解釋性方法。

| 模型類別 | 模型類型 | 可解釋性方法 | 方法基本說明 | 本機說明函式 | 全域說明函式 |
| --- | --- | --- | --- | --- | --- |
| 受監護裝置 | [線性與邏輯迴歸](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-glm?hl=zh-tw) | [Shapley 值](https://christophm.github.io/interpretable-ml-book/shapley.html#the-shapley-value-in-detail) | 線性模型的 Shapley 值等於 `model weight * feature value`，其中特徵值經過標準化，模型權重則以標準化特徵值訓練。 | [`ML.EXPLAIN_PREDICT`1](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-explain-predict?hl=zh-tw) | [`ML.GLOBAL_EXPLAIN`2](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-global-explain?hl=zh-tw) |
| [標準差](https://en.wikipedia.org/wiki/Standard_error)和 [P 值](https://en.wikipedia.org/wiki/P-value) | 標準差和 p 值可用於針對模型權重進行顯著性測試。 | 不適用 | [`ML.ADVANCED_WEIGHTS`4](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-advanced-weights?hl=zh-tw) |
| [提升樹](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-boosted-tree?hl=zh-tw)  [隨機森林](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-random-forest?hl=zh-tw) | [Tree SHAP](https://docs.seldon.io/projects/alibi/en/stable/methods/TreeSHAP.html) | Tree SHAP 是一種演算法，可計算決策樹狀結構模型的確切 [SHAP 值](https://christophm.github.io/interpretable-ml-book/shap.html)。 | [`ML.EXPLAIN_PREDICT`1](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-explain-predict?hl=zh-tw) | [`ML.GLOBAL_EXPLAIN`2](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-global-explain?hl=zh-tw) |
| [特徵貢獻概略值](http://blog.datadive.net/interpreting-random-forests/) | 估算特徵貢獻值。與 Tree SHAP 相比，這項功能更快速簡單。 | [`ML.EXPLAIN_PREDICT`1](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-explain-predict?hl=zh-tw) | [`ML.GLOBAL_EXPLAIN`2](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-global-explain?hl=zh-tw) |
| [以吉尼指數為準的特徵重要性](https://xgboost.readthedocs.io/en/latest/python/python_api.html#xgboost.XGBRegressor.feature_importances_) | 全域特徵重要性分數，表示在訓練期間建構提升樹狀結構或隨機森林模型時，各項特徵的實用性或價值。 | 不適用 | [`ML.FEATURE_IMPORTANCE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-importance?hl=zh-tw) |
| [AutoML Tables](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-automl?hl=zh-tw) | [取樣 Shapley](https://docs.cloud.google.com/vertex-ai/docs/explainable-ai/overview?hl=zh-tw#compare-methods) | 取樣 Shapley 值會為每項特徵指派模型結果的功勞，並考量特徵的不同排列組合。這個方法會提供確切 Shapley 值的近似取樣。 | 不適用 | [`ML.GLOBAL_EXPLAIN`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-global-explain?hl=zh-tw)2 |
| 時間序列模型 | [ARIMA\_PLUS](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-time-series?hl=zh-tw) | [時間序列分解](https://otexts.com/fpp2/decomposition.html) | 如果時間序列中存在多個元件，系統會將時間序列分解為這些元件。這些成分包括趨勢、季節性、節慶、階段性變化，以及尖峰和低谷。詳情請參閱 ARIMA\_PLUS [建模管道](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-time-series?hl=zh-tw#modeling-pipeline)。 | [`ML.EXPLAIN_FORECAST`3](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-explain-forecast?hl=zh-tw) | 不適用 |
| [ARIMA\_PLUS\_XREG](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-multivariate-time-series?hl=zh-tw) | [時間序列分解](https://otexts.com/fpp2/decomposition.html) 和   [Shapley 值](https://christophm.github.io/interpretable-ml-book/shapley.html#the-shapley-value-in-detail) | 將時間序列分解為多個元件，包括趨勢、季節性、節慶、步階變化、尖峰和低谷 (類似於 [ARIMA\_PLUS](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-time-series?hl=zh-tw))。系統會根據 Shapley 值計算每個外部迴歸量的歸因，該值等於 `model weight * feature value`。 | [`ML.EXPLAIN_FORECAST`3](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-explain-forecast?hl=zh-tw) | 不適用 |

1`ML_EXPLAIN_PREDICT` 是 `ML.PREDICT` 的擴充版本。

2`ML.GLOBAL_EXPLAIN` 會傳回全域可解釋性，方法是計算評估資料集中所有資料列的每個特徵所獲得的平均絕對歸因。

3`ML.EXPLAIN_FORECAST` 是 `ML.FORECAST` 的擴充版本。

4`ML.ADVANCED_WEIGHTS` 是 `ML.WEIGHTS` 的擴充版本。

## 後續步驟

* 如要進一步瞭解支援可解釋性的模型適用的 SQL 陳述式和函式，請參閱「[機器學習模型端對端使用者歷程](https://docs.cloud.google.com/bigquery/docs/e2e-journey?hl=zh-tw)」。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-10-29 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-10-29 (世界標準時間)。"],[],[]]