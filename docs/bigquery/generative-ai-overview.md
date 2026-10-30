Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 生成式 AI 資訊摘要

本文說明 BigQuery 支援的生成式人工智慧 (AI) 函式。這些函式接受自然語言輸入，並使用預先訓練的 [Gemini Enterprise Agent Platform 模型](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/learn/models?hl=zh-tw)和內建 BigQuery 模型。

BigQuery 提供多種 AI 函式，可協助您執行下列工作：

* 生成創意內容。
* 分析文字或非結構化資料 (例如圖片)、偵測情緒，以及回答相關問題。
* 總結內容傳達的主要想法或印象。
* 擷取文字中的結構化資料。
* 將文字或非結構化資料分類至使用者定義的類別。
* 生成嵌入，搜尋相似的文字、圖片和影片。
* 為輸入內容評分，以便依品質、相似度或其他條件排序。

AI 函式分為下列類別，可協助您完成這些工作：

* **[通用 AI 函式](#general_purpose_ai)：**這類函式可讓您完全掌控及瞭解要使用的模型、提示和參數。

  + [執行 LLM 推論](#inference)，例如回答資料相關問題

    - `AI.GENERATE` 是最靈活的推論函式，可讓您分析任何結構化或非結構化資料。
    - `AI.GENERATE_TEXT` 是 `AI.GENERATE` 的資料表值版本，也支援合作夥伴模型和開放式模型。
  + [生成結構化輸出內容](#generate_structured_data)，例如從文字、文件或圖片中擷取姓名、地址或物件說明。

    - `AI.GENERATE`，指定輸出內容結構定義。
    - `AI.GENERATE_TABLE` 是 `AI.GENERATE` 的資料表值版本，可呼叫遠端模型，並讓您指定自訂輸出內容結構定義。
    - 如果輸出結構定義只有一個欄位，您可以使用下列其中一個專用函式：`AI.GENERATE_BOOL`、`AI.GENERATE_DOUBLE` 或 `AI.GENERATE_INT`。
  + [生成嵌入項目](#text_embedding)，用於語意搜尋和分群

    - `AI.EMBED`：從文字或圖片資料建立嵌入。
    - `AI.GENERATE_EMBEDDING`：資料表值函式，可將內嵌文字、圖片、音訊、影片或文件資料的資料欄新增至資料表。
* **[代管 AI 函式](#managed_ai_functions)：**這類函式的語法簡潔，且經過最佳化，可兼顧成本和品質。使用[最佳化模式](https://docs.cloud.google.com/bigquery/docs/optimize-ai-functions?hl=zh-tw) (預先發布版) 時，這些函式可擴充至數百萬或數十億列。

  + `AI.IF`：使用自然語言條件篩選資料。
  + `AI.SCORE`：評估輸入內容，例如品質或情緒。
  + `AI.CLASSIFY`：將輸入內容分類至使用者定義的類別。
  + `AI.AGG`：匯總輸入內容，以歸納或分析資料。
* **公用函式：**執行查詢前，請使用 [`AI.COUNT_TOKENS` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-ai-count-tokens?hl=zh-tw)估算輸入提示中的詞元數量。
* **[特定工作函式](#task-specific_functions)：**這些函式會使用 Cloud AI API 協助您執行自然語言處理、機器翻譯、文件處理、音訊轉錄和電腦視覺等工作。

## 通用 AI 函式

通用 AI 函式可讓您完全掌控及瞭解所選用的模型、提示和參數。輸出內容包含模型呼叫的詳細資訊，包括狀態和完整模型回覆，其中可能包含安全評分或引用資訊。

### 執行 LLM 推論

[`AI.GENERATE` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-ai-generate?hl=zh-tw)是彈性的推論函式，運作方式是將要求傳送至 Gemini Enterprise Agent Platform Gemini 模型，並傳回該模型的回覆。您可以使用這項函式分析文字、圖片、音訊、影片或 PDF 資料。舉例來說，您可以分析居家擺設的圖片，為 `design_type` 欄生成文字，讓擺設 SKU 具有相關聯的說明，例如 `mid-century modern` 或 `farmhouse`。

您可以使用 BigQuery ML 中的遠端模型，參照部署或託管於 Agent Platform 的模型，並透過 [`AI.GENERATE_TEXT` 資料表值函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-ai-generate-text?hl=zh-tw)執行生成式 AI 任務。您可以使用下列類型的[遠端模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model?hl=zh-tw)：

* 透過任何[正式發布](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/models?hl=zh-tw#generally_available_models)或[預先發布版](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/models?hl=zh-tw#preview_models)的 Gemini 模型，使用遠端模型分析標準資料表或物件資料表中的文字、圖片、音訊、影片或 PDF 內容，並以函式引數的形式提供提示。
* 透過 [Anthropic Claude](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/partner-models/use-claude?hl=zh-tw)、[Mistral AI](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/partner-models/mistral?hl=zh-tw)  或 [Llama](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/partner-models/llama?hl=zh-tw) 合作夥伴模型，或[支援的開放式模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model-open?hl=zh-tw#supported_open_models)，分析您在查詢中或[標準表格](https://docs.cloud.google.com/bigquery/docs/tables-intro?hl=zh-tw#standard-tables)的資料欄中提供的提示。

請參閱下列主題，嘗試在 BigQuery ML 中生成文字：

* [使用 Gemini 模型和 `AI.GENERATE_TEXT` 函式生成文字](https://docs.cloud.google.com/bigquery/docs/generate-text-tutorial-gemini?hl=zh-tw)。
* [使用 Gemma 模型和 `AI.GENERATE_TEXT` 函式生成文字](https://docs.cloud.google.com/bigquery/docs/generate-text-tutorial-gemma?hl=zh-tw)。
* [使用 Gemini 模型分析圖片](https://docs.cloud.google.com/bigquery/docs/image-analysis?hl=zh-tw)。
* [使用 `AI.GENERATE_TEXT` 函式和資料生成文字](https://docs.cloud.google.com/bigquery/docs/generate-text?hl=zh-tw)。
* [使用資料調整模型](https://docs.cloud.google.com/bigquery/docs/tune-evaluate?hl=zh-tw)。

對於某些模型，您可以選擇設定[監督式調整](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model-tuned?hl=zh-tw#supervised_tuning)，使用自己的資料訓練模型，使其更適合您的用途。所有推論作業都會在 Agent Platform 執行。結果會儲存在 BigQuery 中。

### 生成結構化資料

生成結構化資料與生成文字非常相似，但您可以指定 SQL 結構定義，設定模型回覆的格式。舉例來說，您可以根據通話轉錄稿生成表格，其中包含客戶姓名、電話號碼、地址、要求和報價。

您可以透過下列方式產生結構化資料：

* [`AI.GENERATE` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-ai-generate?hl=zh-tw)會呼叫 Agent Platform 端點，並可使用自訂結構定義產生 `STRUCT` 值。

  如要試用，請參閱如何在使用 `AI.GENERATE` 函式時
  [使用結構化輸出](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-ai-generate?hl=zh-tw#use_structured_output)
  。
* [`AI.GENERATE_TABLE` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-generate-table?hl=zh-tw)會呼叫遠端模型，並以資料表值函式形式，產生具有自訂結構定義的資料表。

  如要嘗試建立結構化資料，請參閱「[使用 `AI.GENERATE_TABLE` 函式生成結構化資料](https://docs.cloud.google.com/bigquery/docs/generate-table?hl=zh-tw)」。
* 如果是單一輸出欄位，您可以使用下列其中一種專門推論函式：

  + [`AI.GENERATE_BOOL`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-ai-generate-bool?hl=zh-tw)
  + [`AI.GENERATE_DOUBLE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-ai-generate-double?hl=zh-tw)
  + [`AI.GENERATE_INT`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-ai-generate-int?hl=zh-tw)

### 生成嵌入項目

嵌入是高維度數值向量，代表特定實體，例如文字片段或音訊檔案。生成嵌入項目後，您就能擷取資料的語意，更輕鬆地推論及比較資料。

生成嵌入維度的常見用途如下：

* 使用檢索增強生成 (RAG) 技術，參考可信來源的其他資料，強化模型對使用者查詢的回覆。RAG 可提供更準確的事實和一致的回覆，並能存取比模型訓練資料更新的資料。
* 執行多模態搜尋。例如使用文字輸入內容搜尋圖片。
* 執行語意搜尋，找出類似項目，用於推薦、替代和記錄重複資料刪除。
* 建立嵌入，以便與 k-means 模型搭配使用，進行分群。

如要進一步瞭解如何生成嵌入項目，並使用這些項目執行上述工作，請參閱「[嵌入項目和向量搜尋簡介](https://docs.cloud.google.com/bigquery/docs/vector-search-intro?hl=zh-tw)」。

## 代管 AI 函式

代管 AI 函式可簡化篩選、分類或匯總等例行工作。這些函式可以分析文字、圖片、音訊、影片或 PDF 資料。這些函式會使用 Gemini，不需要自訂。BigQuery 會使用提示工程，並選取適當的模型和參數，用於特定工作，以最佳化結果的品質和一致性。每個函式都會傳回純量值，例如 `BOOL`、`FLOAT64` 或 `STRING`，且不包含模型提供的其他狀態資訊。下列代管 AI 函式可供使用：

* [`AI.IF`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-ai-if?hl=zh-tw)：根據提示篩選文字或多模態資料，例如在 `WHERE` 或 `JOIN` 子句中。舉例來說，你可以篩選出適合做為禮物的產品說明。
* [`AI.SCORE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-ai-score?hl=zh-tw)：
  根據提示評估輸入內容，依品質、相似度或其他條件排列資料列。您可以在 `ORDER BY` 子句中使用此函式，根據分數擷取前 K 個項目。舉例來說，您可以找出產品最正面或最負面的前 10 則使用者評論。
* [`AI.CLASSIFY`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-ai-classify?hl=zh-tw)：將文字分類至使用者定義的類別。您可以在 `GROUP BY` 子句中使用這個函式，根據您定義的類別將輸入內容分組。舉例來說，您可以根據支援單是否與帳單、運送、產品品質或其他事項有關，將支援單分類。
* [`AI.AGG`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-ai-agg?hl=zh-tw)：根據自然語言指令匯總輸入內容，以便摘要或分析資料。例如，您可以掃描使用者應用程式工作階段的記錄，判斷客戶遇到困難的地方，也可以總結大量圖片的內容。

**注意：** 如要更有效率地處理大型資料集，可以對 `AI.IF` 和 `AI.CLASSIFY` 函式使用*最佳化模式* (預先發布版)。這種模式會使用資料樣本訓練輕量精簡模型，然後使用該模型對大部分資料列進行推論。這種做法可避免為每個資料列呼叫 LLM，因此在處理數千甚至數十億個資料列時，[可減少詞元消耗量和延遲時間](https://docs.cloud.google.com/bigquery/docs/optimize-ai-functions?hl=zh-tw)。

如需教學課程，瞭解如何使用這些函式，請參閱「[使用代管 AI 函式執行語意分析](https://docs.cloud.google.com/bigquery/docs/semantic-analysis?hl=zh-tw)」。

如需筆記本教學課程，瞭解如何使用代管和通用 AI 函式，請參閱「[使用 AI 函式進行語意分析](https://github.com/GoogleCloudPlatform/generative-ai/blob/main/gemini/use-cases/applying-llms-to-data/bigquery_ai_operators.ipynb)」。

## 特定工作的函式

除了前幾節所述的一般函式外，您也可以使用 Cloud AI API，在 BigQuery ML 中開發特定工作的解決方案。支援的工作包括：

* [自然語言處理](https://docs.cloud.google.com/bigquery/docs/ai-application-overview?hl=zh-tw#natural_language_processing)
* [機器翻譯](https://docs.cloud.google.com/bigquery/docs/ai-application-overview?hl=zh-tw#machine_translation)
* [文件處理](https://docs.cloud.google.com/bigquery/docs/ai-application-overview?hl=zh-tw#document_processing)
* [語音轉錄](https://docs.cloud.google.com/bigquery/docs/ai-application-overview?hl=zh-tw#audio_transcription)
* [電腦視覺](https://docs.cloud.google.com/bigquery/docs/ai-application-overview?hl=zh-tw#computer_vision)

詳情請參閱「[工作專屬解決方案總覽](https://docs.cloud.google.com/bigquery/docs/ai-application-overview?hl=zh-tw)」。

## 位置

文字生成和嵌入模型支援的位置，會因使用的模型類型和版本而異。詳情請參閱「[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw#bqml-loc)」。

BigQuery 支援下列模型：

* `gemini-4-argon`
* `gemini-3.8-flash`
* `gemini-3.7-flash`
* `gemini-3.6-flash`
* `gemini-3.5-flash-lite`
* `gemini-3.5-flash`
* `gemini-3.1-flash-lite`

Agent Platform 僅支援這些模型的多區域端點。不支援區域端點。
如果指定的端點名稱簡短，且省略區域 (例如 `gemini-3.5-flash`)，BigQuery 會根據下列規則選取端點：

* 如果查詢是在 `us` 區域或美國境內的任何單一區域執行，BigQuery 會使用 `us` 端點。
* 如果查詢是在 `eu` 區域，或歐盟境內任何單一區域 (`europe-west2` 或 `europe-west6` 除外) 執行，BigQuery 會使用 `eu` 端點。
* 對於所有其他位置 (包括 `europe-west2` 和 `europe-west6`)，BigQuery 會使用 `global` 端點。

如要指定特定端點，請使用下列其中一種格式的完整多區域端點名稱：

* `https://aiplatform.us.rep.googleapis.com/v1/projects/PROJECT_ID/locations/us/publishers/google/models/MODEL_ID`
* `https://aiplatform.eu.rep.googleapis.com/v1/projects/PROJECT_ID/locations/eu/publishers/google/models/MODEL_ID`
* `https://aiplatform.googleapis.com/v1/projects/PROJECT_ID/locations/global/publishers/google/models/MODEL_ID`

如果查詢在 `asia-south1` 區域執行，則必須使用完整全域端點名稱。

## 限制

在 [VPC Service Controls](https://docs.cloud.google.com/bigquery/docs/vpc-sc?hl=zh-tw) 範圍內，AI 函式無法處理使用[委派存取權](https://docs.cloud.google.com/bigquery/docs/work-with-objectref?hl=zh-tw#delegated-access)的 [`ObjectRef` 值](https://docs.cloud.google.com/bigquery/docs/work-with-objectref?hl=zh-tw)。委派存取權會為物件產生已簽署的 HTTPS 網址，而 Agent Platform 會封鎖 perimeter 內專案的 HTTP 和 HTTPS 擷取作業。函式會將下列錯誤寫入輸出的 `status` 欄位：

`INVALID_ARGUMENT: HTTP links are not supported for requests restricted by VPCSC.`

由於[物件資料表](https://docs.cloud.google.com/bigquery/docs/object-table-introduction?hl=zh-tw)的 `ref` 欄一律使用物件資料表的連線做為授權者，因此將 `ref` 傳遞至 perimeter 內的 AI 函式時，一律會傳回這項錯誤。如要分析物件，請改為傳遞單一引數 `OBJ.MAKE_REF(uri)` 值，該值會使用[直接存取](https://docs.cloud.google.com/bigquery/docs/work-with-objectref?hl=zh-tw#direct-access)，並將 Cloud Storage URI 傳送至模型，而不產生經簽署的網址。

## 定價

您必須為執行模型查詢所用的運算資源付費。遠端模型會呼叫 Agent Platform 模型，因此對遠端模型發出的查詢也會產生 Agent Platform 費用。

詳情請參閱「[BigQuery ML 定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#bigquery-ml-pricing)」。

## 追蹤詞元用量

呼叫生成式 AI 函式時，如果使用的 Gemini 模型不是嵌入模型，您可以查看查詢處理的各類詞元總數。在「Query results」(查詢結果) 窗格中，點選「Job information」(工作資訊)。系統會顯示下列計數，並視情況依模態細分：

* **輸入詞元數：**查詢中呼叫的所有生成式 AI 函式，其輸入詞元總數。
* **輸出詞元數。**查詢生成的所有候選回覆的權杖總數。
* **思考詞元數。**模型生成的思考過程所含的詞元總數 (如適用)。
* **快取詞元數。**查詢[隱含快取](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/context-cache/context-cache-overview?hl=zh-tw#implicit-caching)的輸入詞元總數。

## 追蹤費用

BigQuery 的生成式 AI 函式會將要求傳送至 Gemini Enterprise Agent Platform，因此可能會產生費用。如要在執行查詢前估算輸入詞元數量，請使用 [`AI.COUNT_TOKENS` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-ai-count-tokens?hl=zh-tw)。如要追蹤在 BigQuery 執行的工作所產生的 Agent Platform 費用，請按照下列步驟操作：

1. 在 Cloud Billing 中[查看帳單報表](https://docs.cloud.google.com/billing/docs/how-to/reports?hl=zh-tw)。
2. [使用篩選器](https://docs.cloud.google.com/billing/docs/how-to/reports?hl=zh-tw#filters)縮小結果範圍。

   選取「Vertex AI」服務。
3. 如要查看特定工作的費用，請[依標籤篩選](https://docs.cloud.google.com/billing/docs/how-to/reports?hl=zh-tw#filter-by-labels)。

   將鍵設為 `bigquery_job_id_prefix`，並將值設為工作的[工作 ID](https://docs.cloud.google.com/bigquery/docs/managing-jobs?hl=zh-tw#view-job)。如果工作 ID 超過 63 個字元，請只使用前 63 個字元。如果工作 ID 包含任何大寫字元，請將其變更為小寫。或者，您也可以[將工作與自訂標籤建立關聯](https://docs.cloud.google.com/bigquery/docs/adding-labels?hl=zh-tw#adding-label-to-session)，方便日後查詢。

部分費用最多可能需要 24 小時才會顯示在 Cloud Billing。

## 監控

如要進一步瞭解在 BigQuery 中呼叫的 AI 函式行為，可以啟用要求和回應記錄功能。如要記錄傳送至 Agent Platform 的完整要求，以及從 Agent Platform 收到的完整回應，請按照下列步驟操作：

1. 在 Gemini Enterprise Agent Platform [啟用要求/回覆記錄](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/multimodal/request-response-logging?hl=zh-tw)。記錄檔會儲存在 BigQuery 中。
   您必須分別為每個基礎模型和區域啟用記錄功能。如要記錄在 `us` 區域中執行的查詢，請在要求中指定 `us-central1` 區域。如要記錄在 `eu` 區域執行的查詢，請在要求中指定 `europe-west4` 區域。
2. 使用 AI 函式執行查詢，透過您在上一個步驟中啟用記錄的模型，呼叫 Agent Platform。
3. 如要查看完整的 Agent Platform 要求和回應，請查詢記錄資料表，找出 `full_request` 欄位 `labels.bigquery_job_id_prefix` 欄位與[工作 ID](https://docs.cloud.google.com/bigquery/docs/managing-jobs?hl=zh-tw#view-job) 前 63 個字元相符的資料列。(選用) 您可以[使用自訂查詢標籤](https://docs.cloud.google.com/bigquery/docs/adding-labels?hl=zh-tw#adding-label-to-session)，在記錄中查詢查詢。

   舉例來說，您可以使用類似下列的查詢：

   ```
   SELECT *
   FROM `my_project.my_dataset.request_response_logging`
   WHERE JSON_VALUE(full_request, '$.labels.bigquery_job_id_prefix') = 'bquxjob_123456...';
   ```

## 錯誤管理

如果 AI 函式超出遠端服務的配額或限制，可能會發生資料列層級的錯誤，例如 `RESOURCE_EXHAUSTED`。發生資料列層級錯誤時，函式會針對該資料列傳回 `NULL`，導致查詢結果不完整。

所有 AI 函式都可能發生這些錯誤。不過，代管 AI 函式 (`AI.IF`、`AI.CLASSIFY` 和 `AI.SCORE`) 支援 `max_error_ratio` 引數，可協助您管理函式。使用這個引數設定失敗門檻，即使發生資料列層級失敗，查詢仍可成功。

`max_error_ratio` 的預設值為 `1.0`。如要降低容錯率，請將容錯率設為較小的值 (例如 `0.2`)，這樣查詢就會失敗，而不是部分失敗但成功。如需語法詳細資料，請參閱 [`AI.IF`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-ai-if?hl=zh-tw#arguments)、[`AI.CLASSIFY`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-ai-classify?hl=zh-tw#arguments) 或 [`AI.SCORE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-ai-score?hl=zh-tw#arguments) 的參考說明文件。

如果查詢成功，但部分失敗，BigQuery 會傳回警告。如要進一步瞭解函式錯誤，請前往 Google Cloud 控制台，在查詢結果的「Job information」(工作資訊) 分頁中，查看「Gen AI function errors」(生成式 AI 函式錯誤) 欄位。

**注意：** 錯誤率的計算方式是將失敗的資料列數量，除以模型處理的資料列總數。

如果查詢包含 `LIMIT` 子句，系統會在模型處理完一批資料列*後*套用限制。因此，最終結果集中 `NULL` 值的比例可能會高於指定的 `max_error_ratio`。

舉例來說，假設您的查詢包含 `LIMIT 10` 子句和 `max_error_ratio` 的 `0.2`。系統可能會先處理 20 列，再套用限制。如果這 20 列中有 3 列失敗，錯誤率為 `0.15` (15%)，在 20% 的門檻內。不過，如果 `LIMIT` 子句選取的資料列子集剛好包含所有 3 個失敗的資料列，可見輸出內容就會包含 30% 的 `NULL` 值。

## 後續步驟

* 如要瞭解 BigQuery 中的 AI 和機器學習，請參閱「[BigQuery 中的 AI 和機器學習簡介](https://docs.cloud.google.com/bigquery/docs/bqml-introduction?hl=zh-tw)」。
* 如要進一步瞭解如何對機器學習模型執行推論，請參閱「[模型推論總覽](https://docs.cloud.google.com/bigquery/docs/inference-overview?hl=zh-tw)」。
* 如要進一步瞭解生成式 AI 模型支援的 SQL 陳述式和函式，請參閱「[生成式 AI 模型的端對端使用者歷程](https://docs.cloud.google.com/bigquery/docs/e2e-journey-genai?hl=zh-tw)」。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-10-29 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-10-29 (世界標準時間)。"],[],[]]