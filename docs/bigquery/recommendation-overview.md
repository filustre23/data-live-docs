* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 建議總覽

推薦系統是機器學習在商業上最成功也最廣泛的應用。您可以利用推薦系統，協助使用者找到絕佳內容，避免遭到巨量內容淹沒。舉例來說，Google Play 商店提供數百萬個應用程式，而 YouTube 上則有數十億部影片，應用程式和影片的數量每天都在增加。使用者可透過搜尋找到新內容，但這會受限於所用的搜尋字詞。如果使用推薦系統，就能向使用者推薦他們可能沒想過要搜尋的內容。詳情請參閱[推薦系統總覽](https://developers.google.com/machine-learning/recommendation/overview/types?hl=zh-tw)。

推薦系統中的機器學習演算法通常分為以下幾類：

* 依據內容篩選：根據商品相似度提供建議。舉例來說，如果使用者觀看了兩部可愛的貓咪影片，推薦系統就能向該使用者推薦更多可愛的動物影片。
* 協同過濾：根據使用者之間的相似程度 (以使用者查詢為依據) 提供建議。舉例來說，如果使用者 A 搜尋的內容與使用者 B 相似，且使用者 B 喜歡影片 1，那麼推薦系統可以向使用者 A 推薦影片 1，即使使用者 A 從未觀看與影片 1 相似的影片。

## 矩陣分解模型

[矩陣分解模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-matrix-factorization?hl=zh-tw)廣泛用於推薦系統，做為協同過濾方法。

在矩陣因數分解模型中，使用者項目配對會對應至二維矩陣，其中一個軸代表不重複使用者，另一個軸則代表不重複項目。使用者對項目的評分會顯示在矩陣的儲存格中。
這個矩陣不必填滿，因為使用者通常不會為每個項目提供值。矩陣分解模型的目標是建立兩個較小的密集權重矩陣，相乘後可近似原始矩陣儲存格值，並為空白矩陣儲存格提供預測評分。

其中一個較小的矩陣包含一個軸上的不重複使用者，以及另一個軸上的潛在因素數量，如 `CREATE MODEL` 陳述式的 [`NUM_FACTORS` 選項](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-matrix-factorization?hl=zh-tw#num_factors)所指定。另一個較小的矩陣則包含一個軸上的不重複項目，以及另一個軸上的潛在因素數量。在這個矩陣中，潛在因子權重是由用於訓練模型的演算法產生，依據是輸入矩陣中的使用者項目組合。

詳情請參閱「[矩陣分解](https://developers.google.com/machine-learning/recommendation/collaborative/matrix?hl=zh-tw)」。

您可以使用矩陣分解模型搭配 [`ML.RECOMMEND` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-recommend?hl=zh-tw)，提供建議。

## 其他建議模型

如要擴充協同過濾式推薦系統，使其功能超出矩陣分解模型可達成的範圍，可以使用[深層類神經網路 (DNN)](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-dnn-models?hl=zh-tw) 和[廣度和深度](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-wnd-models?hl=zh-tw)模型，並搭配 [`ML.PREDICT` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-predict?hl=zh-tw)來提供推薦內容。這些模型可納入查詢和項目特徵，提升推薦內容的關聯性。詳情請參閱下列資源：

* [使用深層類神經網路模型提供建議](https://developers.google.com/machine-learning/recommendation/dnn/softmax?hl=zh-tw)
* [Deep Neural Networks for YouTube Recommendations](https://research.google/pubs/pub45530?hl=zh-tw)
* [Wide & Deep Learning for Recommender Systems](https://arxiv.org/pdf/1606.07792.pdf)

## 建議的知識

只要在 `CREATE MODEL` 陳述式和推論函式中使用預設設定，即使沒有太多機器學習知識，也能建立及使用建議模型。不過，具備機器學習開發的基本知識，尤其是推薦模型，有助於您同時最佳化資料和模型，進而獲得更出色的結果。建議您使用下列資源，熟悉機器學習技術和程序：

* [機器學習密集課程](https://developers.google.com/machine-learning/crash-course?hl=zh-tw)
* [機器學習簡介](https://www.kaggle.com/learn/intro-to-machine-learning)
* [中階機器學習](https://www.kaggle.com/learn/intermediate-machine-learning)
* [推薦系統](https://developers.google.com/machine-learning/recommendation?hl=zh-tw)




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-04-30 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-04-30 (世界標準時間)。"],[],[]]