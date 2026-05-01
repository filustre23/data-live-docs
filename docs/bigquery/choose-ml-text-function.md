* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 選擇自然語言處理函式

本文將比較 BigQuery ML 提供的自然語言處理函式，包括 [`AI.GENERATE_TEXT`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-ai-generate-text?hl=zh-tw)、[`ML.TRANSLATE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-translate?hl=zh-tw) 和 [`ML.UNDERSTAND_TEXT`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-understand-text?hl=zh-tw)。如果函式的功能重疊，您可以參考本文資訊，決定要使用哪個函式。

這兩項函式的主要差異如下：

* `AI.GENERATE_TEXT` 是以較低成本執行自訂自然語言處理 (NLP) 工作的理想選擇。這項功能支援更多語言、輸送量更快、可調整模型，且適用於多模態模型。
* `ML.TRANSLATE` 是執行翻譯專屬 NLP 工作的好選擇，可支援每分鐘高查詢率。
* `ML.UNDERSTAND_TEXT` 是執行 Cloud Natural Language API 支援的 NLP 工作時的理想選擇。

## 函式比較

請參閱下表，比較 `AI.GENERATE_TEXT`、`ML.TRANSLATE` 和 `ML.UNDERSTAND_TEXT` 函式：

|  | `AI.GENERATE_TEXT` | `ML.TRANSLATE` | `ML.UNDERSTAND_TEXT` |
| --- | --- | --- | --- |
| 目的 | 將提示傳遞至 [Gemini 或合作夥伴模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model?hl=zh-tw)，或是[開放式模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model-open?hl=zh-tw)，即可執行任何自然語言處理工作。  舉例來說，如要執行問答工作，可以提供類似 `CONCAT("What are the key concepts in the following article?: ", article_text)` 的提示。 | 使用 [Cloud Translation API](https://docs.cloud.google.com/translate?hl=zh-tw) 執行下列工作：  * [`TRANSLATE_TEXT`](https://docs.cloud.google.com/translate/docs/advanced/translating-text-v3?hl=zh-tw) * [`DETECT_LANGUAGE`](https://docs.cloud.google.com/translate/docs/advanced/detecting-language-v3?hl=zh-tw) | 使用 [Cloud Natural Language API](https://docs.cloud.google.com/natural-language?hl=zh-tw) 執行下列工作：  * [`ANALYZE_ENTITIES`](https://docs.cloud.google.com/natural-language/docs/analyzing-entities?hl=zh-tw) * [`ANALYZE_ENTITY_SENTIMENT`](https://docs.cloud.google.com/natural-language/docs/analyzing-entity-sentiment?hl=zh-tw) * [`ANALYZE_SENTIMENT`](https://docs.cloud.google.com/natural-language/docs/analyzing-sentiment?hl=zh-tw) * [`ANALYZE_SYNTAX`](https://docs.cloud.google.com/natural-language/docs/analyzing-syntax?hl=zh-tw) * [`CLASSIFY_TEXT`](https://docs.cloud.google.com/natural-language/docs/classifying-text?hl=zh-tw) |
| 帳單 | 系統會針對處理的資料收取 BigQuery ML 費用。詳情請參閱 [BigQuery ML 定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#bigquery-ml-pricing)一文。  模型呼叫會產生 Vertex AI 費用。如果您使用 Gemini 2.0 以上版本模型，系統會按照批次 API 費率計費。詳情請參閱「[在 Vertex AI 中建構及部署 AI 模型的費用](https://docs.cloud.google.com/vertex-ai/generative-ai/pricing?hl=zh-tw)」。 | 系統會針對處理的資料收取 BigQuery ML 費用。詳情請參閱 [BigQuery ML 定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#bigquery-ml-pricing)一文。   呼叫 Cloud Translation API 會產生費用。詳情請參閱「[Cloud Translation API 定價](https://docs.cloud.google.com/translate/pricing?hl=zh-tw)」。 | 系統會針對處理的資料收取 BigQuery ML 費用。詳情請參閱 [BigQuery ML 定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#bigquery-ml-pricing)一文。  呼叫 Cloud Natural Language API 時會產生費用。詳情請參閱 [Cloud Natural Language API 定價](https://docs.cloud.google.com/translate/pricing?hl=zh-tw)。 |
| 每分鐘要求數 | 不適用於 Gemini 模型。合作夥伴模型：25 到 60。詳情請參閱「[每分鐘要求次數限制](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#requests_per_minute_limits)」。 | 200。詳情請參閱[雲端 AI 服務函式](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#cloud_ai_service_functions)。 | 600。詳情請參閱[雲端 AI 服務函式](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#cloud_ai_service_functions)。 |
| 每分鐘權杖數 | 視使用的模型而定，範圍從 8,192 到超過 100 萬。 | 沒有詞元數量上限。不過，`ML_TRANSLATE` 有 [30,000 個位元組的限制](https://docs.cloud.google.com/translate/quotas?hl=zh-tw#content-limit)。 | [100,000](https://docs.cloud.google.com/natural-language/quotas?hl=zh-tw#content)。 |
| 輸入資料 | 支援 BigQuery 標準資料表和物件資料表中的文字和非結構化資料。 | 支援 BigQuery 標準資料表的文字資料。 | 支援 BigQuery 標準資料表的文字資料。 |
| 函式輸出 | 即使使用相同的提示，模型呼叫的輸出內容也可能有所不同。 | 針對每次成功呼叫 API，為特定工作類型產生相同的輸出內容。輸出內容包括輸入語言的相關資訊。 | 針對每次成功呼叫 API，為特定工作類型產生相同的輸出內容。輸出內容會包含情緒分析工作的情緒強度資訊。 |
| 資料脈絡 | 您可以在提交的提示中提供資料背景資訊。 | 不支援。 | 不支援。 |
| 監督式調整 | [受監護微調](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/learn/models?hl=zh-tw#languages-gemini) 適用於部分模型。 | 不支援。 | 不支援。 |
| 支援的語言 | 支援的語言會因您選擇的 LLM 而異。 | 支援 Cloud Translation API [語言](https://docs.cloud.google.com/translate/docs/languages?hl=zh-tw)。 | 支援 Cloud Natural Language API [語言](https://docs.cloud.google.com/natural-language/docs/languages?hl=zh-tw)。 |
| 支援的地區 | 所有 Vertex AI 生成式 AI [區域](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/learn/locations?hl=zh-tw#available-regions)皆支援這項功能。 | 支援 `EU` 和 `US` 多區域。 | 支援 `EU` 和 `US` 多區域。 |




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-04-30 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-04-30 (世界標準時間)。"],[],[]]