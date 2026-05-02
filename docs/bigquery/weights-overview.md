* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# BigQuery ML 模型權重總覽

本文說明 BigQuery ML 如何支援機器學習 (ML) 模型的模型權重探索功能。

機器學習模型是將機器學習演算法套用至訓練資料後儲存的構件。模型代表預測所需的規則、數字和其他演算法專屬資料結構。以下提供幾個範例：

* 線性迴歸模型是由具有特定值的係數向量組成。
* 決策樹模型由一或多個樹狀結構組成，內含特定值的 if-then 陳述式。
* 深層類神經網路模型是由圖形結構組成，其中包含特定值的權重向量或矩陣。

在 BigQuery ML 中，*模型權重*一詞用於描述模型所包含的元件。

## BigQuery ML 中的模型權重供應項目

BigQuery ML 提供多種函式，可用於擷取不同模型的模型權重。

| 模型類別 | 模型類型 | 模型權重函式 | 函式用途 |
| --- | --- | --- | --- |
| 受監護裝置 | [線性與邏輯迴歸](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-glm?hl=zh-tw) | `ML.WEIGHTS` | 擷取特徵係數和截距。 |
| 非監督式模型 | [Kmeans](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-kmeans?hl=zh-tw) | `ML.CENTROIDS` | 擷取所有質心的特徵係數。 |
| [矩陣分解](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-matrix-factorization?hl=zh-tw) | `ML.WEIGHTS` | 擷取所有潛在因子的權重。這兩個矩陣分別代表使用者矩陣和項目矩陣。 |
| [PCA](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-pca?hl=zh-tw) | `ML.PRINCIPAL_COMPONENTS` | 擷取所有主成分的特徵係數，也稱為特徵向量。 |
| `ML.PRINCIPAL_COMPONENT_INFO` | 擷取每個主成分的統計資料，例如特徵值。 |
| 時間序列模型 | [ARIMA\_PLUS](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-time-series?hl=zh-tw) | `ML.ARIMA_COEFFICIENTS` | 擷取 ARIMA 模型的係數，用於模擬輸入時間序列的趨勢成分。如要瞭解其他元件 (例如時間序列中的季節性模式)，請使用 `ML.ARIMA_EVALUATE`。 |

BigQuery ML 不支援下列模型類型的模型權重函式：

* [強化型樹狀結構](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-boosted-tree?hl=zh-tw)
* [隨機森林](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-random-forest?hl=zh-tw)
* [深層類神經網路 (DNN)](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-dnn-models?hl=zh-tw)
* [廣度和深度](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-wnd-models?hl=zh-tw)
* [AutoML Tables](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-automl?hl=zh-tw)

如要查看所有模型類型的權重 (AutoML Tables 模型除外)，請將模型從 BigQuery ML 匯出至 Cloud Storage。接著，您可以使用 XGBoost 程式庫，將提升樹狀結構和隨機森林模型的樹狀結構視覺化，也可以使用 TensorFlow 程式庫，將 DNN 和寬而深模型的圖形結構視覺化。AutoML Tables 模型沒有取得模型權重資訊的方法。

如要進一步瞭解如何匯出模型，請參閱[`EXPORT MODEL` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-export-model?hl=zh-tw)和「[匯出 BigQuery ML 模型以進行線上預測](https://docs.cloud.google.com/bigquery/docs/export-model-tutorial?hl=zh-tw)」。

## 後續步驟

如要進一步瞭解 ML 模型支援的 SQL 陳述式和函式，請參閱[ML 模型端對端使用者歷程](https://docs.cloud.google.com/bigquery/docs/e2e-journey?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-02 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-02 (世界標準時間)。"],[],[]]