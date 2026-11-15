Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 選擇文件處理函式

您可以比較 BigQuery ML 提供的文件處理函式，選擇最適合分析非結構化文字和文件的工具。瞭解 [`AI.GENERATE_TEXT`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-ai-generate-text?hl=zh-tw) 和 [`ML.PROCESS_DOCUMENT`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-process-document?hl=zh-tw) 函式之間的差異，有助於最佳化資料工作流程，兼顧成本、語言支援和結構化文件剖析。

這些函式的主要差異如下：

* `AI.GENERATE_TEXT` 適合用於執行自然語言處理 (NLP) 工作，其中部分內容位於文件中。這項功能有以下優點：

  + 降低費用
  + 支援更多語言
  + 處理量更高
  + 模型調整功能
  + 多模態模型的適用情形

  如需最適合這種做法的文件處理工作範例，請參閱「[使用 Gemini API 探索文件處理功能](https://ai.google.dev/gemini-api/docs/document-processing?hl=zh-tw)」。
* `ML.PROCESS_DOCUMENT` 適合用於執行文件處理工作，這類工作需要剖析文件，並提供預先定義的結構化回覆。

## 函式比較

請參閱下表，比較 `AI.GENERATE_TEXT` 和 `ML.PROCESS_DOCUMENT` 函式：

|  | `AI.GENERATE_TEXT` | `ML.PROCESS_DOCUMENT` |
| --- | --- | --- |
| 目的 | 將提示傳送至 [Gemini 或合作夥伴模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model?hl=zh-tw)，或[開放式模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model-open?hl=zh-tw)，即可執行任何與文件相關的自然語言處理工作。  舉例來說，假設您有一份公司的財務文件，只要提供「`What is the quarterly revenue for each division?`」等提示，即可擷取文件資訊。 | 使用 [Document AI API](https://docs.cloud.google.com/document-ai?hl=zh-tw)，針對不同文件類型 (例如應付憑據、稅務表單和財務報表) 執行專門的文件處理作業。您也可以執行文件分塊。 |
| 帳單 | 會產生 BigQuery ML 資料處理費用。詳情請參閱「[BigQuery ML 定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#bigquery-ml-pricing)」。   呼叫模型會產生 Gemini Enterprise Agent Platform 費用。如果使用 Gemini 2.0 以上版本模型，則會按照 Batch API 費率計費。詳情請參閱「[在 Agent Platform 建構及部署 AI 模型的成本](https://docs.cloud.google.com/vertex-ai/generative-ai/pricing?hl=zh-tw)」。 | 會產生 BigQuery ML 資料處理費用。詳情請參閱「[BigQuery ML 定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#bigquery-ml-pricing)」。   呼叫 Document AI API 會產生費用。詳情請參閱 [Document AI API 定價](https://docs.cloud.google.com/document-ai/pricing?hl=zh-tw)。 |
| 每分鐘要求數 (RPM) | 不適用於 Gemini 模型。合作夥伴模型則介於 25 到 60 之間。詳情請參閱「[每分鐘要求數限制](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#requests_per_minute_limits)」。 | 每種處理器類型每分鐘 120 次，每項專案每分鐘總計 600 次。 詳情請參閱[配額清單](https://docs.cloud.google.com/document-ai/quotas?hl=zh-tw#quotas_list)。 |
| 每分鐘詞元數 | 視使用的模型而定，範圍從 8,192 到超過 100 萬。 | 沒有詞元限制。不過，這項功能確實有不同的頁數限制，具體取決於您使用的處理器。詳情請參閱「[限制](https://docs.cloud.google.com/document-ai/limits?hl=zh-tw)」。 |
| 監督式調整 | 部分模型支援[監督式調整](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/learn/models?hl=zh-tw#languages-gemini)。 | 不支援。 |
| 支援的語言 | 支援情形會因您選擇的大型語言模型而異。 | 支援的語言取決於文件處理器類型，大多數僅支援英文。詳情請參閱[處理器清單](https://docs.cloud.google.com/document-ai/docs/processors-list?hl=zh-tw)。 |
| 支援的地區 | 支援所有 Generative AI for Agent Platform [區域](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/learn/locations?hl=zh-tw#available-regions)。 | 所有處理器均支援 `EU` 和 `US` 多區域。部分處理器也適用於特定單一區域。詳情請參閱「[區域和多區域支援](https://docs.cloud.google.com/document-ai/docs/regions?hl=zh-tw)」。 |




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-11-13 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-11-13 (世界標準時間)。"],[],[]]