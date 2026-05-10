Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 參考模式

本頁面提供 BigQuery ML 用途的業務用途說明、程式碼範例，以及技術參考指南的連結。請運用這些資源找出最佳做法，加快應用程式開發作業。

## 邏輯迴歸

本模式說明如何使用邏輯迴歸，為遊戲應用程式執行傾向度模擬。

瞭解如何使用 BigQuery ML 訓練、評估及取得多種不同類型的意願模型預測結果。傾向模型可協助您判斷特定使用者回訪應用程式的可能性，讓您在行銷決策中運用這項資訊。

* 網誌文章：[遊戲開發人員使用 Google Analytics 4 和 BigQuery ML 預測流失情形](https://cloud.google.com/blog/topics/developers-practitioners/churn-prediction-game-developers-using-google-analytics-4-ga4-and-bigquery-ml?hl=zh-tw)
* 筆記本：[流失預測解決方案筆記本](https://github.com/GoogleCloudPlatform/analytics-componentized-patterns/tree/master/gaming/propensity-model/bqml)

## 時間序列預測

這些模式說明如何建立時間序列預測解決方案。

### 建立需求預測模型

瞭解如何建立時間序列模型，用於預測多項產品的零售需求。

* 網誌文章：[如何使用 BigQuery ML 建構需求預測模型](https://cloud.google.com/blog/topics/developers-practitioners/how-build-demand-forecasting-models-bigquery-ml?hl=zh-tw)
* 筆記本：[需求預測解決方案筆記本](https://github.com/GoogleCloudPlatform/analytics-componentized-patterns/blob/master/retail/time-series/bqml-demand-forecasting/bqml_retail_demand_forecasting.ipynb)

### 使用 BigQuery ML 透過 Google 試算表進行預測

瞭解如何在 BigQuery ML 中結合[連結的試算表](https://docs.cloud.google.com/bigquery/docs/connected-sheets?hl=zh-tw)與預測模型，藉此將機器學習納入業務流程。本模式會逐步說明如何使用 Google Analytics 資料，建立網站流量預測模型。您可以擴充此模式，以便與其他資料類型和其他機器學習模型搭配使用。

* 網誌文章：[如何透過 BigQuery ML 使用 Google 試算表中的機器學習模型](https://cloud.google.com/blog/topics/developers-practitioners/how-use-machine-learning-model-google-sheet-using-bigquery-ml?hl=zh-tw)
* 程式碼範例：[使用試算表進行 BigQuery ML 預測](https://github.com/googleworkspace/ml-integration-samples/tree/master/apps-script/BQMLForecasting)
* 範本：[使用試算表進行 BigQuery ML 預測](https://docs.google.com/spreadsheets/d/1njedwGjBOkUbTS_HYD0wIPuQIDHgobp1D80qO-OsNH0/copy?hl=zh-tw)

## 異常偵測

這個模式說明如何使用異常偵測功能，找出即時信用卡詐欺行為。

瞭解如何使用交易和客戶資料，在 BigQuery ML 中訓練機器學習模型，以便在即時資料管道中識別、分析及觸發潛在信用卡詐欺的警報。

* 程式碼範例：[即時信用卡詐欺偵測](https://github.com/googlecloudplatform/fraudfinder)
* 總覽影片：[Fraudfinder：針對實際資料科學問題提供全面解決方案](https://io.google/2022/program/9a759b60-9a9b-4744-bd22-6e21a4a864cd/?hl=zh-tw)




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-09 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-09 (世界標準時間)。"],[],[]]