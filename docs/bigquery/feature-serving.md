Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 特徵供應

您可以使用多種服務選項，將[特徵](https://docs.cloud.google.com/bigquery/docs/preprocess-overview?hl=zh-tw)用於 BigQuery ML 模型訓練和推論。無論選擇哪種方式，都必須先將特徵儲存在 BigQuery 資料表中。

## 時間點正確性

用來訓練模型的資料通常內建時間依附關係。為時效性特徵建立特徵資料表時，請加入時間戳記資料欄，代表各資料列在特定時間的特徵值。接著，您可以在查詢這些特徵資料表中的資料時，使用時間點查詢函式，確保訓練和提供服務之間不會發生[資料外洩](https://en.wikipedia.org/wiki/Leakage_(machine_learning))。這項程序可確保時間點正確性。

擷取時效性特徵時，請使用下列函式指定時間點截止：

* [`ML.FEATURES_AT_TIME`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-feature-time?hl=zh-tw)
* [`ML.ENTITY_FEATURES_AT_TIME`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-entity-feature-time?hl=zh-tw)

## 在 BigQuery ML 中提供特徵

如要在 BigQuery ML 中訓練模型及執行批次推論，您可以使用「[時間點正確性](#point-in-time_correctness)」一節所述的時間點查詢函式，擷取特徵。您可以在 `CREATE MODEL` 陳述式的 [`query_statement` 子句](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create?hl=zh-tw#query_statement)中加入這些函式，用於訓練，或在適當資料表值函式 (例如 [`ML.PREDICT`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-predict?hl=zh-tw)) 的 `query_statement` 子句中加入這些函式，用於提供服務。

## 使用 Vertex AI 特徵儲存庫提供特徵

如要將特徵提供給[在 Gemini Enterprise Agent Platform 註冊](https://docs.cloud.google.com/bigquery/docs/managing-models-vertex?hl=zh-tw#register_models)的 BigQuery ML 模型，可以使用 [Vertex AI 特徵儲存庫](https://docs.cloud.google.com/gemini-enterprise-agent-platform/machine-learning/featurestore/latest/overview?hl=zh-tw)。Vertex AI 特徵儲存庫會以 BigQuery 中的特徵資料表為基礎，管理及提供特徵，且延遲時間極短。您可以使用[線上提供](https://docs.cloud.google.com/gemini-enterprise-agent-platform/machine-learning/featurestore/latest/serve-feature-values?hl=zh-tw)功能，即時擷取特徵進行線上預測，也可以使用[離線提供](https://docs.cloud.google.com/gemini-enterprise-agent-platform/machine-learning/featurestore/latest/serve-historical-features?hl=zh-tw)功能，擷取特徵進行模型訓練。

如要進一步瞭解如何準備 BigQuery 特徵資料，以便在 Vertex AI 特徵儲存庫 中使用，請參閱「[準備資料來源](https://docs.cloud.google.com/gemini-enterprise-agent-platform/machine-learning/featurestore/latest/prepare-data-source?hl=zh-tw)」。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-10-22 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-10-22 (世界標準時間)。"],[],[]]