Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# BigQuery Explainable AI 總覽

本文說明 BigQuery ML 如何支援可解釋的 AI (有時稱為 XAI)。

Explainable AI 可協助您瞭解預測機器學習模型為分類和迴歸工作產生的結果，方法是定義資料列中各項特徵對預測結果的影響程度。這類資訊通常稱為「功能歸因」。有了這項資訊，您就能確認模型的行為是否符合預期、找出模型偏誤，以及探索改善模型和訓練資料的方式。

BigQuery ML 和 Vertex AI 都提供 Explainable AI，可提供特徵式解釋。您可以在 BigQuery ML 中執行可解釋性作業，也可以在 Vertex AI 中[註冊模型](https://docs.cloud.google.com/bigquery/docs/managing-models-vertex?hl=zh-tw#register_models)，然後在該處執行可解釋性作業。

## 局部與全域可解釋性

可解釋性分為兩種：局部可解釋性和全域可解釋性。這分別稱為「區域特徵重要性」和「全域特徵重要性」。

* 局部可解釋性會傳回每個已說明範例的特徵歸因值。這些值說明特定特徵對預測的影響程度，相較於基準預測。
* 全域可解釋性會傳回特徵對模型的整體影響，通常是透過彙整整個資料集的特徵歸因來取得。絕對值越高，表示該特徵對模型預測結果的影響越大。

## BigQuery ML 中的 Explainable AI 產品

BigQuery ML 中的 Explainable AI 支援各種機器學習模型，包括時間序列和非時間序列模型。每個模型都採用不同的可解釋性方法。

| 模型類別 | 模型類型 | 可解釋性方法 | 方法基本說明 | 本機說明函式 | 全域說明函式 |
| --- | --- | --- | --- | --- | --- |
| 受監護裝置 | [線性與邏輯迴歸](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-glm?hl=zh-tw) | [Shapley 值](https://christophm.github.io/interpretable-ml-book/shapley.html#the-shapley-value-in-detail) | 線性模型的 Shapley 值等於 `model weight * feature value`，其中特徵值經過標準化，且模型權重是使用標準化特徵值訓練而得。 | [`ML.EXPLAIN_PREDICT`1](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-explain-predict?hl=zh-tw) | [`ML.GLOBAL_EXPLAIN`2](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-global-explain?hl=zh-tw) |
| [標準差](https://en.wikipedia.org/wiki/Standard_error)和 [P 值](https://en.wikipedia.org/wiki/P-value) | 標準差和 p 值用於針對模型權重進行顯著性測試。 | 不適用 | [`ML.ADVANCED_WEIGHTS`4](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-advanced-weights?hl=zh-tw) |
| [強化型樹狀結構](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-boosted-tree?hl=zh-tw)  [隨機森林](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-random-forest?hl=zh-tw) | [Tree SHAP](https://docs.seldon.io/projects/alibi/en/stable/methods/TreeSHAP.html) | Tree SHAP 演算法可計算決策樹狀結構模型的確切 [SHAP 值](https://christophm.github.io/interpretable-ml-book/shap.html)。 | [`ML.EXPLAIN_PREDICT`1](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-explain-predict?hl=zh-tw) | [`ML.GLOBAL_EXPLAIN`2](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-global-explain?hl=zh-tw) |
| [概略功能貢獻](http://blog.datadive.net/interpreting-random-forests/) | 估算特徵貢獻值。相較於 Tree SHAP，這項功能更快速簡單。 | [`ML.EXPLAIN_PREDICT`1](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-explain-predict?hl=zh-tw) | [`ML.GLOBAL_EXPLAIN`2](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-global-explain?hl=zh-tw) |
| [以吉尼指數為準的特徵重要性](https://xgboost.readthedocs.io/en/latest/python/python_api.html#xgboost.XGBRegressor.feature_importances_) | 全域特徵重要性分數，表示在訓練期間建構升壓樹狀結構或隨機森林模型時，各項特徵的實用性或價值。 | 不適用 | [`ML.FEATURE_IMPORTANCE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-importance?hl=zh-tw) |
| [深層類神經網路 (DNN)](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-dnn-models?hl=zh-tw)   [廣度和深度](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-wnd-models?hl=zh-tw) | [積分梯度](https://docs.cloud.google.com/ai-platform/prediction/docs/ai-explanations/overview?hl=zh-tw#ig) | 以梯度為準的方法，可有效計算特徵歸因，並具備與夏普利值相同的公理屬性。這項工具可提供確切特徵歸因的近似取樣。準確度由 [`integrated_gradients_num_steps`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-explain-predict?hl=zh-tw#arguments) 參數控制。 | [`ML.EXPLAIN_PREDICT`1](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-explain-predict?hl=zh-tw) | [`ML.GLOBAL_EXPLAIN`2](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-global-explain?hl=zh-tw) |
| [AutoML Tables](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-automl?hl=zh-tw) | [Sampled Shapley](https://docs.cloud.google.com/vertex-ai/docs/explainable-ai/overview?hl=zh-tw#compare-methods) | 取樣 Shapley 會為每項特徵指派模型結果額度，並考慮不同特徵的排列組合。這個方法會提供確切 Shapley 值的近似取樣。 | 不適用 | [`ML.GLOBAL_EXPLAIN`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-global-explain?hl=zh-tw)2 |
| 時間序列模型 | [ARIMA\_PLUS](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-time-series?hl=zh-tw) | [時間序列分解](https://otexts.com/fpp2/decomposition.html) | 如果時間序列中存在多個元件，系統會將時間序列分解為多個元件。這些因素包括趨勢、季節性、節慶、階段性變化，以及尖峰和低谷。詳情請參閱 ARIMA\_PLUS [建模管道](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-time-series?hl=zh-tw#modeling-pipeline)。 | [`ML.EXPLAIN_FORECAST`3](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-explain-forecast?hl=zh-tw) | 不適用 |
| [ARIMA\_PLUS\_XREG](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-multivariate-time-series?hl=zh-tw) | [時間序列分解](https://otexts.com/fpp2/decomposition.html) 和   [Shapley 值](https://christophm.github.io/interpretable-ml-book/shapley.html#the-shapley-value-in-detail) | 將時間序列分解為多個元件，包括趨勢、季節性、節慶、逐步變化，以及尖峰和低谷 (類似於 [ARIMA\_PLUS](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-time-series?hl=zh-tw))。系統會根據 Shapley 值計算每個外部迴歸量的歸因，這等於 `model weight * feature value`。 | [`ML.EXPLAIN_FORECAST`3](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-explain-forecast?hl=zh-tw) | 不適用 |

1`ML_EXPLAIN_PREDICT` 是 `ML.PREDICT` 的擴充版本。

2`ML.GLOBAL_EXPLAIN` 會傳回全域可解釋性，方法是計算評估資料集中所有資料列的每個特徵所獲得的平均絕對歸因。

3`ML.EXPLAIN_FORECAST` 是 `ML.FORECAST` 的擴充版本。

4`ML.ADVANCED_WEIGHTS` 是 `ML.WEIGHTS` 的擴充版本。

## Vertex AI 中的 Explainable AI

Vertex AI 支援下列可匯出監督式學習模型的子集，並提供 Explainable AI 功能：

| 模型類型 | Explainable AI 方法 |
| --- | --- |
| dnn\_classifier | 積分梯度 |
| dnn\_regressor | 積分梯度 |
| dnn\_linear\_combined\_classifier | 積分梯度 |
| dnn\_linear\_combined\_regressor | 積分梯度 |
| boosted\_tree\_regressor | Shapley 取樣 |
| boosted\_tree\_classifier | Shapley 取樣 |
| random\_forest\_regressor | Shapley 取樣 |
| random\_forest\_classifier | Shapley 取樣 |

如要進一步瞭解這些方法，請參閱「[功能歸因方法](https://docs.cloud.google.com/vertex-ai/docs/explainable-ai/overview?hl=zh-tw#feature-attribution-methods)」。

### 在 Model Registry 中啟用 Explainable AI

在 Model Registry 中註冊 BigQuery ML 模型後，如果模型類型支援 Explainable AI，您可以在將模型部署至端點時啟用 Explainable AI。註冊 BigQuery ML 模型時，系統會自動填入所有相關聯的中繼資料。

**注意：** Explainable AI 會產生少許額外費用。如要瞭解詳情，請參閱 [Vertex AI 定價](https://cloud.google.com/vertex-ai/pricing?hl=zh-tw)。

1. [將 BigQuery ML 模型註冊至 Model Registry](https://docs.cloud.google.com/bigquery/docs/managing-models-vertex?hl=zh-tw#register_models)。
2. 前往 Google Cloud 控制台的 BigQuery 專區，然後前往「Model Registry」頁面。
3. 從 Model Registry 選取 BigQuery ML 模型，然後按一下模型版本，重新導向至模型詳細資料頁面。
4. 選取模型版本中的「更多動作」。
   more\_vert
5. 按一下「Deploy to endpoint」(部署至端點)。
6. 定義端點：建立端點名稱，然後按一下「繼續」。
7. 選取機器類型，例如 `n1-standard-2`。
8. 在「模型設定」下方的記錄部分，勾選核取方塊，啟用可解釋性選項。
9. 依序點選「完成」和「繼續」，即可部署至端點。

如要瞭解如何對 Model Registry 中的模型使用 XAI，請參閱「[使用已部署的模型取得線上說明](https://docs.cloud.google.com/vertex-ai/docs/tabular-data/classification-regression/get-online-predictions?hl=zh-tw#online-explanation)」。如要進一步瞭解 Vertex AI 中的 XAI，請參閱「[取得說明](https://docs.cloud.google.com/vertex-ai/docs/explainable-ai/getting-explanations?hl=zh-tw)」。

## 後續步驟

* 瞭解如何[在 Vertex AI 中管理 BigQuery ML 模型](https://docs.cloud.google.com/bigquery/docs/managing-models-vertex?hl=zh-tw)。
* 如要進一步瞭解支援可解釋性的模型所支援的 SQL 陳述式和函式，請參閱[機器學習模型端對端使用者歷程](https://docs.cloud.google.com/bigquery/docs/e2e-journey?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-06 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-06 (世界標準時間)。"],[],[]]