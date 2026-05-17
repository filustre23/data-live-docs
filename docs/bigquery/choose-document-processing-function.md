Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 選擇文件處理函式

本文將比較 BigQuery ML 提供的文件處理函式，包括 [`AI.GENERATE_TEXT`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-ai-generate-text?hl=zh-tw) 和 [`ML.PROCESS_DOCUMENT`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-process-document?hl=zh-tw)。如果函式的功能重疊，您可以參考本文資訊，決定要使用哪個函式。

這兩項函式的主要差異如下：

* `AI.GENERATE_TEXT` 非常適合執行自然語言處理 (NLP) 工作，因為部分內容位於文件中。這項功能具備下列優點：

  + 降低費用
  + 支援更多語言
  + 處理量更高
  + 模型調整功能
  + 多模態模型適用情形

  如需最適合採用這種做法的文件處理工作範例，請參閱「[使用 Gemini API 探索文件處理功能](https://ai.google.dev/gemini-api/docs/document-processing?hl=zh-tw)」。
* `ML.PROCESS_DOCUMENT` 非常適合執行需要剖析文件和預先定義結構化回應的文件處理工作。

## 函式比較

請參閱下表，比較 `AI.GENERATE_TEXT` 和 `ML.PROCESS_DOCUMENT` 函式：

|  | `AI.GENERATE_TEXT` | `ML.PROCESS_DOCUMENT` |
| --- | --- | --- |
| 目的 | 將提示傳遞至 [Gemini 或合作夥伴模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model?hl=zh-tw)，或是[開放式模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model-open?hl=zh-tw)，即可執行任何與文件相關的 NLP 工作。  舉例來說，假設您有某間公司的財務文件，可以提供「`What is the quarterly revenue for each division?`」等提示，擷取文件資訊。 | 使用 [Document AI API](https://docs.cloud.google.com/document-ai?hl=zh-tw) 針對不同類型的文件 (例如發票、稅務表單和財務報表) 執行專門的文件處理作業。您也可以執行文件分塊。 |
| 帳單 | 系統會針對處理的資料收取 BigQuery ML 費用。詳情請參閱 [BigQuery ML 定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#bigquery-ml-pricing)一文。   呼叫模型時會產生 Vertex AI 費用。如果您使用 Gemini 2.0 以上版本模型，系統會按照批次 API 費率計費。詳情請參閱「[在 Vertex AI 中建構及部署 AI 模型的費用](https://docs.cloud.google.com/vertex-ai/generative-ai/pricing?hl=zh-tw)」。 | 系統會針對處理的資料收取 BigQuery ML 費用。詳情請參閱 [BigQuery ML 定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#bigquery-ml-pricing)一文。   呼叫 Document AI API 時會產生費用。詳情請參閱 [Document AI API 定價](https://docs.cloud.google.com/document-ai/pricing?hl=zh-tw)。 |
| 每分鐘要求數 (RPM) | 不適用於 Gemini 模型。合作夥伴模型：25 到 60。詳情請參閱「[每分鐘要求次數限制](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#requests_per_minute_limits)」。 | 每種處理器類型每分鐘 120 次，每個專案每分鐘最多 600 次。 詳情請參閱[配額清單](https://docs.cloud.google.com/document-ai/quotas?hl=zh-tw#quotas_list)。 |
| 每分鐘權杖數 | 視使用的模型而定，範圍從 8,192 到超過 100 萬。 | 沒有詞元數量上限。不過，這項功能有不同的頁面限制，具體取決於您使用的處理器。詳情請參閱「[限制](https://docs.cloud.google.com/document-ai/limits?hl=zh-tw)」。 |
| 監督式調整 | [受監護微調](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/learn/models?hl=zh-tw#languages-gemini) 適用於部分模型。 | 不支援。 |
| 支援的語言 | 支援的語言會因您選擇的 LLM 而異。 | 語言支援取決於文件處理器類型，大多數只支援英文。詳情請參閱[處理器清單](https://docs.cloud.google.com/document-ai/docs/processors-list?hl=zh-tw)。 |
| 支援的地區 | 所有 Vertex AI 生成式 AI [區域](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/learn/locations?hl=zh-tw#available-regions)皆支援這項功能。 | 所有處理器都支援 `EU` 和 `US` 多區域。部分處理器也適用於特定單一區域。詳情請參閱「[區域和多區域支援](https://docs.cloud.google.com/document-ai/docs/regions?hl=zh-tw)」。 |




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-16 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-16 (世界標準時間)。"],[],[]]