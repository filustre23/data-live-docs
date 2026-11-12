Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 選擇文字生成函式

本文比較 BigQuery ML 的 [`AI.GENERATE_TEXT`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-ai-generate-text?hl=zh-tw) 和 [`AI.GENERATE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-ai-generate?hl=zh-tw) 文字生成函式。如果函式功能重疊，您可以參考本文資訊，決定要使用哪一個函式。

## 函式相似度

`AI.GENERATE_TEXT` 和 `AI.GENERATE` 函式在以下方面相似：

* **用途**：將提示傳遞至大型語言模型 (LLM) 來生成文字。
* **計費**：BigQuery ML 會針對處理的資料收取費用。詳情請參閱「[BigQuery ML 定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#bigquery-ml-pricing)」。呼叫 LLM 時，會產生 Gemini Enterprise Agent Platform 費用。如果使用 Gemini 2.0 以上版本模型，則會依 Batch API 費率計費。詳情請參閱「[在 Agent Platform 建構及部署 AI 模型的成本](https://docs.cloud.google.com/vertex-ai/generative-ai/pricing?hl=zh-tw)」。
* **擴充性**：每項 6 小時查詢工作可處理 100 萬到 1,000 萬列資料。實際處理量取決於輸入資料列中的平均權杖長度等因素。詳情請參閱「[生成式 AI 函式](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#generative_ai_functions)」。
* **輸入資料**：支援 BigQuery 標準資料表和物件資料表中的文字和非結構化資料。

## 功能差異

請參考下表，評估 `AI.GENERATE_TEXT` 和 `AI.GENERATE` 函式之間的差異：

|  | `AI.GENERATE_TEXT` | `AI.GENERATE` |
| --- | --- | --- |
| 函式簽章 | 資料表值函式，會將資料表做為輸入內容，並傳回資料表做為輸出內容。 | 純量函式：接受單一值做為輸入內容，並傳回單一值做為輸出內容。 |
| 支援的 LLM | * Gemini 模型 * 合作夥伴模型，例如 Anthropic Claude、Llama 和 Mistral AI * 開放式模型 | Gemini 模型 |
| 函式輸出內容 | Gemini 模型的函式輸出內容：   * 生成的文字 * 負責任的 AI 技術 (RAI) 結果 * Google 搜尋基準建立結果 (如已啟用) * LLM 呼叫狀態   其他類型模型的函式輸出內容：   * 生成的文字 * LLM 呼叫狀態 | * 生成的文字 * JSON 格式的完整模型回覆 * LLM 呼叫狀態 |
| 函式輸出格式 | 產生的值會傳回至單一 JSON 資料欄或個別資料表資料欄，具體取決於 `flatten_json_output` 引數值。 | 生成的值會以 `STRUCT` 物件中的欄位形式傳回。 |
| 使用者歷程 | 您必須先建立[遠端模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model?hl=zh-tw#create_model_syntax)，才能使用函式。 | 您可以直接使用函式，不必建立遠端模型。 |
| 權限設定 | 您必須手動建立 BigQuery 連線，並將 Agent Platform 使用者角色權限授予連線的服務帳戶。如果您使用的是 BigQuery [預設連線](https://docs.cloud.google.com/bigquery/docs/default-connections?hl=zh-tw#example-remote-model)，可以略過這個步驟。 | 您可以使用 [Google 帳戶使用者憑證](https://docs.cloud.google.com/bigquery/docs/permissions-for-ai-functions?hl=zh-tw)呼叫這個函式。 |
| 優點 | 可使用更靈活的輸入和輸出格式。 | 更容易整合至 SQL 查詢。 |
| 擴充函式 | 您可以使用 [`AI.GENERATE_TABLE` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-generate-table?hl=zh-tw)，根據指定的 SQL 輸出結構定義生成結構化輸出內容。 | 您可以使用 [`AI.GENERATE_BOOL`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-ai-generate-bool?hl=zh-tw)、[`AI.GENERATE_INT`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-ai-generate-int?hl=zh-tw) 和 [`AI.GENERATE_DOUBLE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-ai-generate-double?hl=zh-tw) 函式，生成不同類型的純量值。 |




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-11-12 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-11-12 (世界標準時間)。"],[],[]]