Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# BigQuery ML 模型評估總覽

本文說明 BigQuery ML 如何支援機器學習 (ML) 模型評估。

## 模型評估總覽

您可以使用 ML 模型評估指標，達到下列目的：

* 評估模型與資料的擬合品質。
* 比較不同模型。
* 預測每個模型在特定資料集上的準確度，以利選取模型。

監督式和非監督式學習模型的評估方式不同：

* 監督式學習模型的評估方式明確，評估集是模型尚未分析的資料，通常會從訓練集中排除，然後用於評估模型效能。建議您不要使用訓練集進行評估，因為這樣會導致模型在一般化新資料的預測結果時，效能不佳。這種結果稱為*過度擬合*。
* 對於非監督式學習模型，模型評估的定義較不明確，通常會因模型而異。由於非監督式學習模型不會保留評估集，因此評估指標是使用整個輸入資料集計算而得。

## 模型評估服務

BigQuery ML 提供下列函式，可計算機器學習模型的評估指標：

| 模型類別 | 模型類型 | 模型評估函式 | 函式用途 |
| --- | --- | --- | --- |
| 監督式學習 | [線性迴歸](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-glm?hl=zh-tw)  [提升樹狀結構迴歸器](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-boosted-tree?hl=zh-tw)  [隨機森林迴歸器](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-random-forest?hl=zh-tw)  [DNN 迴歸器](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-dnn-models?hl=zh-tw)  [廣而深迴歸器](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-wnd-models?hl=zh-tw)  [AutoML Tables 迴歸器](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-automl?hl=zh-tw) | `ML.EVALUATE` | 報表會顯示下列指標：   * 平均絕對誤差 * 均方誤差 * 均方對數誤差 * 中位數絕對誤差 * r2 分數 * 解釋變異數 |
| [羅吉斯迴歸](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-glm?hl=zh-tw)  [提升樹狀結構分類器](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-boosted-tree?hl=zh-tw)  [隨機森林分類器](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-random-forest?hl=zh-tw)  [DNN 分類器](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-dnn-models?hl=zh-tw)  [廣而深分類器](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-wnd-models?hl=zh-tw)  [AutoML Tables 分類器](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-automl?hl=zh-tw) | `ML.EVALUATE` | 報表會顯示下列指標：   * 精確度 * recall * 準確率 * F1 分數 * 對數損失 * roc auc |
| `ML.CONFUSION_MATRIX` | 回報[混淆矩陣](https://en.wikipedia.org/wiki/Confusion_matrix)。 |
| `ML.ROC_CURVE` | 報表會顯示不同門檻值的指標，包括：   * recall * 偽陽率 * 真陽性 * 誤判 * 真陰性 * 偽陰性   僅適用於二元分類模型。 |
| 非監督式學習 | [K-means](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-kmeans?hl=zh-tw) | `ML.EVALUATE` | 回報 [Davies-Bouldin 指數](https://en.wikipedia.org/wiki/Davies%E2%80%93Bouldin_index)，以及資料點與所指派群集質心之間的均方距離。 |
| [矩陣分解](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-matrix-factorization?hl=zh-tw) | `ML.EVALUATE` | 如果是以[明確意見回饋](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-matrix-factorization?hl=zh-tw#feedback_type)為依據的模型，報表會提供下列指標：   * 平均絕對誤差 * 均方誤差 * 均方對數誤差 * 中位數絕對誤差 * r2 分數 * 解釋變異數 |
| 如果是以[隱性意見回饋](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-matrix-factorization?hl=zh-tw#feedback_type)為基礎的模型，則會回報下列指標：   * [平均精確度的平均值](https://en.wikipedia.org/wiki/Evaluation_measures_(information_retrieval)#Mean_average_precision) * 均方誤差 * [正規化折減累計增益](https://en.wikipedia.org/wiki/Discounted_cumulative_gain#Normalized_DCG) * 平均排名 |
| [PCA](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-pca?hl=zh-tw) | `ML.EVALUATE` | 回報總變異解釋率。 |
| [自動編碼器](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-autoencoder?hl=zh-tw) | `ML.EVALUATE` | 報表會顯示下列指標：   * 平均絕對誤差 * 均方誤差 * 均方對數誤差 |
| 時間序列 | [ARIMA\_PLUS](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-time-series?hl=zh-tw) | `ML.EVALUATE` | 報表會顯示下列指標：   * 平均絕對誤差 * 均方誤差 * 平均絕對百分比誤差 * 對稱平均絕對百分比誤差   這個函式需要新資料做為輸入內容。 |
| `ML.ARIMA_EVALUATE` | 針對以不同 (p、d、q、has\_drift) 元組為特徵的所有 ARIMA 候選模型，回報下列指標：   * [log\_likelihood](https://en.wikipedia.org/wiki/Likelihood_function#Log-likelihood) * [AIC](https://en.wikipedia.org/wiki/Akaike_information_criterion) * 變異數    此外，這項功能還會回報季節性、節慶效應，以及尖峰和低谷離群值等其他資訊。  這項功能不需要輸入新資料。 |

## 在 `CREATE MODEL` 陳述式中自動評估

BigQuery ML 支援在模型建立期間自動評估。視模型類型、資料分割訓練選項，以及是否使用超參數調整功能而定，系統會根據保留的評估資料集、保留的測試資料集或整個輸入資料集計算評估指標。

* 對於 k 平均值、PCA、自動編碼器和 ARIMA\_PLUS 模型，BigQuery ML 會將所有輸入資料做為訓練資料，並根據整個輸入資料集計算評估指標。
* 對於線性迴歸、邏輯迴歸、提升樹狀結構、隨機森林、DNN、Wide-and-deep 和矩陣分解模型，系統會根據下列 `CREATE MODEL` 選項指定的資料集計算評估指標：

  + [`DATA_SPLIT_METHOD`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-glm?hl=zh-tw#data_split_method)
  + [`DATA_SPLIT_EVAL_FRACTION`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-glm?hl=zh-tw#data_split_eval_fraction)
  + [`DATA_SPLIT_COL`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-glm?hl=zh-tw#data_split_col)

  使用超參數調整功能訓練這類模型時，[`DATA_SPLIT_TEST_FRACTION`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-hyperparameter-tuning?hl=zh-tw#data_split) 選項也有助於定義用於計算評估指標的資料集。詳情請參閱「[資料分割](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-hyperparameter-tuning?hl=zh-tw#data_split)」一文。
* 如為 AutoML Tables 模型，請參閱「[AutoML 模型資料分割作業簡介](https://docs.cloud.google.com/vertex-ai/docs/general/ml-use?hl=zh-tw)」。

如要取得模型建立期間計算的評估指標，請使用評估函式 (例如 `ML.EVALUATE`)，但不要指定輸入資料。如需範例，請參閱[未指定輸入資料的 `ML.EVALUATE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-evaluate?hl=zh-tw#mlevaluate_with_no_input_data_specified)。

## 使用新資料集進行評估

模型建立完成後，您可以指定新的資料集進行評估。如要提供新資料集，請使用評估函式 (例如 `ML.EVALUATE`) 搭配指定的輸入資料。如需範例，請參閱[`ML.EVALUATE`，瞭解如何使用自訂門檻和輸入資料。](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-evaluate?hl=zh-tw#mlevaluate_with_a_custom_threshold_and_input_data)

## 後續步驟

如要進一步瞭解支援評估的模型的 SQL 陳述式和函式，請參閱下列文件：

* [生成式 AI 模型的端對端使用者歷程](https://docs.cloud.google.com/bigquery/docs/e2e-journey-genai?hl=zh-tw)
* [機器學習模型的端對端使用者歷程](https://docs.cloud.google.com/bigquery/docs/e2e-journey?hl=zh-tw)




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-06 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-06 (世界標準時間)。"],[],[]]