* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 維度縮減總覽

降低維度是數學技術的常用術語，這類技術可用於擷取高維度空間中資料的形狀和關係，並將這項資訊轉換為低維度空間。

處理可能包含數千個特徵的大型資料集時，降低維度非常重要。在如此龐大的資料空間中，資料點之間距離範圍越廣，模型輸出結果就越難解讀。舉例來說，這會導致您難以瞭解哪些資料點的位置較近，因此代表的資料也較為相似。降低維度技術可協助您減少特徵數量，同時保留資料集最重要的特徵。減少特徵數量也有助於縮短使用資料做為輸入內容的任何模型訓練時間。

BigQuery ML 提供下列降維模型：

* [主成分分析 (PCA)](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-pca?hl=zh-tw)
* [自動編碼器](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-autoencoder?hl=zh-tw)

您可以使用 PCA 和自動編碼器模型，搭配 [`ML.PREDICT`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-predict?hl=zh-tw) 或 [`AI.GENERATE_EMBEDDING`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-ai-generate-embedding?hl=zh-tw) 函式，將資料嵌入維度較低的空間，並搭配 [`ML.DETECT_ANOMALIES` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-detect-anomalies?hl=zh-tw)執行[異常情況偵測](https://docs.cloud.google.com/bigquery/docs/anomaly-detection-overview?hl=zh-tw)。

您可以將降維模型輸出內容用於下列工作：

* **相似性搜尋**：根據嵌入內容找出彼此相似的資料點。這項功能非常適合尋找相關產品、推薦類似內容，或是找出重複或異常的項目。
* **分群**：將嵌入做為 k-means 模型中的輸入特徵，根據資料點的相似性將其分組。這有助於發掘資料中隱藏的模式和深入分析資訊。
* **機器學習**：將嵌入做為分類或迴歸模型的輸入特徵。

## 建議的知識

即使沒有太多機器學習知識，您也可以使用 `CREATE MODEL` 陳述式和推論函式中的預設設定，建立及使用降維模型。不過，具備機器學習開發的基本知識，有助於您最佳化資料和模型，進而獲得更出色的結果。建議您使用下列資源，熟悉機器學習技術和程序：

* [機器學習密集課程](https://developers.google.com/machine-learning/crash-course?hl=zh-tw)
* [機器學習簡介](https://www.kaggle.com/learn/intro-to-machine-learning)
* [中階機器學習](https://www.kaggle.com/learn/intermediate-machine-learning)




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-04-30 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-04-30 (世界標準時間)。"],[],[]]