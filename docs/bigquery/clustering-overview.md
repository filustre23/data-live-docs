Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 分群總覽

分群法是一種非監督式機器學習技術，可用來將類似的記錄歸為一組。如果您想瞭解資料中的群組或叢集，但沒有標籤資料可訓練模型，這種方法就非常實用。舉例來說，如果您有地鐵車票購買記錄的未標記資料，可以依據購票時間將資料分群，進一步瞭解地鐵使用量最高的時段。詳情請參閱「[什麼是叢集？](https://developers.google.com/machine-learning/clustering/overview?hl=zh-tw)」

[k-means 模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-kmeans?hl=zh-tw)廣泛用於執行分群作業。您可以搭配使用 k-means 模型與 [`ML.PREDICT` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-predict?hl=zh-tw)來分組資料，或搭配使用 [`ML.DETECT_ANOMALIES` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-detect-anomalies?hl=zh-tw)來執行[異常偵測](https://docs.cloud.google.com/bigquery/docs/anomaly-detection-overview?hl=zh-tw)。

K-means 模型會使用[以群集中心為基礎的分群](https://developers.google.com/machine-learning/clustering/clustering-algorithms?hl=zh-tw#centroid-based_clustering)，將資料整理成叢集。如要取得 k-means 模型群集中心的相關資訊，可以使用 [`ML.CENTROIDS` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-centroids?hl=zh-tw)。

## 建議的知識

只要在 `CREATE MODEL` 陳述式和推論函式中使用預設設定，即使沒有太多機器學習知識，也能建立及使用叢集模型。不過，具備機器學習開發和分群模型的基本知識，有助於改善資料和模型，進而獲得更出色的結果。建議您使用下列資源，熟悉機器學習技術和程序：

* [機器學習密集課程](https://developers.google.com/machine-learning/crash-course?hl=zh-tw)
* [機器學習簡介](https://www.kaggle.com/learn/intro-to-machine-learning)
* [中階機器學習](https://www.kaggle.com/learn/intermediate-machine-learning)
* [分群](https://developers.google.com/machine-learning/clustering?hl=zh-tw)




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-02 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-02 (世界標準時間)。"],[],[]]