Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 特徵預先處理總覽

*特徵前處理*是機器學習生命週期中最重要的步驟之一。包括建立特徵和清理訓練資料。建立特徵也稱為「特徵工程」。

BigQuery ML 提供下列特徵前處理技術：

* **自動預先處理**。BigQuery ML 會在訓練期間自動執行前處理作業。詳情請參閱「[自動特徵前處理](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-auto-preprocessing?hl=zh-tw)」。
* **手動預先處理**。您可以在 `CREATE MODEL` 陳述式中使用 [`TRANSFORM` 子句](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create?hl=zh-tw#transform)，透過[手動前處理函式](https://docs.cloud.google.com/bigquery/docs/manual-preprocessing?hl=zh-tw#types_of_preprocessing_functions)定義自訂前處理作業。您也可以在 `TRANSFORM` 子句之外使用這些函式，在建立模型前處理訓練資料。

## 取得功能資訊

您可以使用 [`ML.FEATURE_INFO` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-feature?hl=zh-tw)，擷取所有輸入特徵資料欄的統計資料。

## 建議的知識

您可以使用 `CREATE MODEL` 陳述式中的預設設定和推論函式，建立及使用 BigQuery ML 模型，即使沒有太多機器學習知識也能輕鬆上手。不過，如果具備機器學習開發生命週期的基本知識，例如特徵工程和模型訓練，有助於最佳化資料和模型，進而獲得更出色的結果。建議您使用下列資源，熟悉機器學習技術和程序：

* [機器學習密集課程](https://developers.google.com/machine-learning/crash-course?hl=zh-tw)
* [機器學習簡介](https://www.kaggle.com/learn/intro-to-machine-learning)
* [資料清理](https://www.kaggle.com/learn/data-cleaning)
* [特徵工程](https://www.kaggle.com/learn/feature-engineering)
* [中階機器學習](https://www.kaggle.com/learn/intermediate-machine-learning)

## 後續步驟

* 瞭解 BigQuery ML 中的[特徵服務](https://docs.cloud.google.com/bigquery/docs/feature-serving?hl=zh-tw)。
* 如要進一步瞭解支援特徵預先處理的模型的支援 SQL 陳述式和函式，請參閱下列文件：

  + [機器學習模型的端對端使用者歷程](https://docs.cloud.google.com/bigquery/docs/e2e-journey?hl=zh-tw)
  + [時間序列預測模型的端對端使用者歷程](https://docs.cloud.google.com/bigquery/docs/e2e-journey-forecast?hl=zh-tw)
  + [貢獻分析使用者歷程](https://docs.cloud.google.com/bigquery/docs/contribution-analysis?hl=zh-tw#contribution_analysis_user_journey)




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-09 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-09 (世界標準時間)。"],[],[]]