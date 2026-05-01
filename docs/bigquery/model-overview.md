* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 模型建立

BigQuery ML 可讓您使用 SQL，在 BigQuery 中建立機器學習 (ML) 模型，並對資料執行該模型。

BigQuery ML 中的模型開發工作流程通常如下：

1. 使用 [`CREATE MODEL` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create?hl=zh-tw)建立模型。
2. 執行特徵預先處理。系統會[自動](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-auto-preprocessing?hl=zh-tw)進行部分前置處理，此外，您還可以在 [`TRANSFORM` 子句](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create?hl=zh-tw#transform)中使用[手動前置處理函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-preprocessing-functions?hl=zh-tw)，進行額外的前置處理。
3. 執行[超參數調整](https://docs.cloud.google.com/bigquery/docs/hp-tuning-overview?hl=zh-tw)，讓模型符合訓練資料，進而修正模型。
4. [評估模型](https://docs.cloud.google.com/bigquery/docs/evaluate-overview?hl=zh-tw)，評估模型在訓練集以外資料上的表現，並視需要與其他模型比較。
5. [執行推論作業](https://docs.cloud.google.com/bigquery/docs/inference-overview?hl=zh-tw)，使用模型分析資料。
6. 提供模型[可解釋性](https://docs.cloud.google.com/bigquery/docs/xai-overview?hl=zh-tw)，說明特定特徵如何影響特定預測結果和整體模型。
7. 使用[模型權重](https://docs.cloud.google.com/bigquery/docs/weights-overview?hl=zh-tw)，進一步瞭解構成模型的元件。

由於您可以在 BigQuery ML 中使用許多不同類型的模型，因此每個模型可用的函式各不相同。如要進一步瞭解各模型類型支援的 SQL 陳述式和函式，請參閱下列文件：

* [生成式 AI 模型的端對端使用者歷程](https://docs.cloud.google.com/bigquery/docs/e2e-journey-genai?hl=zh-tw)
* [時間序列預測模型的端對端使用者歷程](https://docs.cloud.google.com/bigquery/docs/e2e-journey-forecast?hl=zh-tw)
* [機器學習模型的端對端使用者歷程](https://docs.cloud.google.com/bigquery/docs/e2e-journey?hl=zh-tw)
* [匯入模型的端對端使用者歷程](https://docs.cloud.google.com/bigquery/docs/e2e-journey-import?hl=zh-tw)
* [貢獻分析使用者歷程](https://docs.cloud.google.com/bigquery/docs/contribution-analysis?hl=zh-tw#contribution_analysis_user_journey)




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-04-30 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-04-30 (世界標準時間)。"],[],[]]