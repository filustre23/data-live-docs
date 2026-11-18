Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# BigQuery ML 模型權重總覽

您可以在 BigQuery ML 中擷取模型權重，檢查訓練過的機器學習 (ML) 模型包含的特定規則、數字和元件。探索這些內部資料結構，可讓您瞭解及稽核模型用於預測的確切數學邏輯。

機器學習模型是在訓練資料上執行機器學習演算法後，儲存的構件。模型代表規則、數字和任何其他演算法專屬的資料結構，這些結構是進行預測時所必需。以下提供幾個範例：

* 線性迴歸模型是由具有特定值的係數向量組成。
* 決策樹模型由一或多個樹狀結構組成，其中包含具有特定值的 if-then 陳述式。
* 深層類神經網路模型是由圖表結構組成，其中包含具有特定值的權重向量或矩陣。

在 BigQuery ML 中，「模型權重」一詞用於描述模型組成的元件。

## BigQuery ML 提供的模型權重

BigQuery ML 提供多種函式，可用於擷取不同模型的權重。

| 模型類別 | 模型類型 | 模型權重函式 | 函式功能 |
| --- | --- | --- | --- |
| 監督式模型 | [線性與邏輯迴歸](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-glm?hl=zh-tw) | `ML.WEIGHTS` | 擷取特徵係數和截距。 |
| 非監督式模型 | [Kmeans](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-kmeans?hl=zh-tw) | `ML.CENTROIDS` | 擷取所有群集中心的特徵係數。 |
| [矩陣分解](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-matrix-factorization?hl=zh-tw) | `ML.WEIGHTS` | 擷取所有潛在因素的權重。代表兩個分解矩陣：使用者矩陣和項目矩陣。 |
| [PCA](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-pca?hl=zh-tw) | `ML.PRINCIPAL_COMPONENTS` | 擷取所有主成分的特徵係數，也稱為特徵向量。 |
| `ML.PRINCIPAL_COMPONENT_INFO` | 擷取各個主成分的統計資料，例如特徵值。 |
| 時間序列模型 | [ARIMA\_PLUS](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-time-series?hl=zh-tw) | `ML.ARIMA_COEFFICIENTS` | 擷取 ARIMA 模型的係數，用於模擬輸入時間序列的趨勢元件。如要瞭解其他元件 (例如時間序列中的季節性模式)，請使用 `ML.ARIMA_EVALUATE`。 |

BigQuery ML 不支援下列模型類型的模型權重函式：

* [提升樹](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-boosted-tree?hl=zh-tw)
* [隨機森林](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-random-forest?hl=zh-tw)
* [深層類神經網路 (DNN)](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-dnn-models?hl=zh-tw)
* [廣度和深度](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-wnd-models?hl=zh-tw)
* [AutoML Tables](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-automl?hl=zh-tw)

如要查看除了 AutoML Tables 模型以外，所有這些模型類型的權重，請將模型從 BigQuery ML 匯出至 Cloud Storage。接著，您可以使用 XGBoost 程式庫，以視覺化方式呈現梯度提升樹和隨機森林模型的樹狀結構，或使用 TensorFlow 程式庫，以視覺化方式呈現 DNN 和廣度和深度模型的圖表結構。目前沒有方法可以取得 AutoML Tables 模型的權重資訊。

如要進一步瞭解如何匯出模型，請參閱「[`EXPORT MODEL` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-export-model?hl=zh-tw)」和「[匯出 BigQuery ML 模型以進行線上預測](https://docs.cloud.google.com/bigquery/docs/export-model-tutorial?hl=zh-tw)」。

## 後續步驟

如要進一步瞭解機器學習模型支援的 SQL 陳述式和函式，請參閱「[機器學習模型的端對端使用者歷程](https://docs.cloud.google.com/bigquery/docs/e2e-journey?hl=zh-tw)」。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-11-18 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-11-18 (世界標準時間)。"],[],[]]