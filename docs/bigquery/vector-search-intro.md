Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 嵌入和向量搜尋簡介

本文將概要說明 BigQuery 中的嵌入和向量搜尋功能。向量搜尋是一種技術，可使用嵌入項目比較相似的物件，並用於支援 Google 搜尋、YouTube 和 Google Play 等 Google 產品。您可以使用向量搜尋大規模執行搜尋。使用向量搜尋時，您可以搭配[向量索引](https://docs.cloud.google.com/bigquery/docs/vector-index?hl=zh-tw)，運用反向檔案索引 (IVF) 和 [ScaNN 演算法](https://research.google/blog/announcing-scann-efficient-vector-similarity-search/?hl=zh-tw)等基礎技術。

向量搜尋是以嵌入為基礎建構而成。嵌入是高維度數值向量，代表特定實體，例如一段文字或音訊檔案。機器學習 (ML) 模型會使用嵌入技術，將這類實體的語意編碼，方便推理及比較。舉例來說，在分群、分類和建議模型中，常見的作業是測量[嵌入空間](https://en.wikipedia.org/wiki/Latent_space)中向量之間的距離，找出語意上最相似的項目。

當您考量如何繪製不同項目時，即可透過視覺化方式瞭解嵌入空間中的語意相似度和距離。舉例來說，*貓*、*狗*和*獅子*等字詞都代表動物類型，因此在這個空間中會因語意特徵相似而緊密相連。同樣地，「汽車」、「卡車」和較籠統的「車輛」等字詞會形成另一個叢集。如下圖所示：

您會發現動物和車輛叢集彼此相距甚遠。群組之間的間隔說明瞭以下原則：物件在嵌入空間中的距離越近，語意相似度就越高；距離越遠，語意相似度就越低。

## 用途

結合嵌入生成和向量搜尋，可實現許多有趣的使用案例。以下是幾個可能的應用實例：

* **[檢索增強生成 (RAG)](https://cloud.google.com/use-cases/retrieval-augmented-generation?hl=zh-tw)：**
  在 BigQuery 中，使用 Gemini 模型剖析文件、對內容執行向量搜尋，並生成自然語言問題的摘要答案。如需說明這個情境的筆記本，請參閱「[使用 BigQuery DataFrames 建構向量搜尋應用程式](https://github.com/googleapis/python-bigquery-dataframes/blob/main/notebooks/generative_ai/bq_dataframes_llm_vector_search.ipynb)」。
* **推薦替代或相符產品：**根據顧客行為和產品相似度，建議替代產品，提升電子商務應用程式的效能。
* **記錄檔分析：**協助團隊主動分類記錄檔中的異常狀況，並加快調查速度。您也可以使用這項功能，為 LLM 增補情境資訊，以改善威脅偵測、鑑識和疑難排解工作流程。如需說明這個情境的筆記本，請參閱「[Log Anomaly Detection & Investigation with Text Embeddings + BigQuery Vector Search](https://github.com/GoogleCloudPlatform/generative-ai/blob/main/embeddings/use-cases/outlier-detection/bq-vector-search-outlier-detection-audit-logs.ipynb)」。
* **分群和指定目標：**精確區隔目標對象。舉例來說，連鎖醫院可以運用自然語言附註和結構化資料，將病患分群；行銷人則可根據查詢意圖指定廣告。如需說明這個情境的筆記本，請參閱「[Create-Campaign-Customer-Segmentation](https://github.com/GoogleCloudPlatform/chocolate-ai/blob/main/colab-enterprise/Create-Campaign-Customer-Segmentation.ipynb)」。
* **實體解析與重複資料刪除：**清理及彙整資料。
  舉例來說，廣告公司可以對個人識別資訊 (PII) 記錄進行重複資料刪除，房地產公司則可找出相符的郵寄地址。

## 生成嵌入項目

以下各節說明 BigQuery 提供的函式，可協助您產生或使用嵌入內容。

### 生成單一嵌入

您可以使用 [`AI.EMBED` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-ai-embed?hl=zh-tw)和 Vertex AI 嵌入模型，為輸入內容生成單一嵌入。

`AI.EMBED` 函式支援下列輸入類型：

* 文字資料。
* 以 [`ObjectRef`](https://docs.cloud.google.com/bigquery/docs/work-with-objectref?hl=zh-tw) 值表示的圖片資料。
* 以 [`ObjectRefRuntime`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/objectref_functions?hl=zh-tw#objectrefruntime) 值表示的圖片資料。

### 生成嵌入資料表

您可以使用
[`AI.GENERATE_EMBEDDING`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-ai-generate-embedding?hl=zh-tw)
建立資料表，其中包含輸入資料表欄中所有資料的嵌入。對於所有類型的支援模型，`AI.GENERATE_EMBEDDING` 都能處理[標準資料表](https://docs.cloud.google.com/bigquery/docs/tables-intro?hl=zh-tw#standard-tables)中的結構化資料。如果是多模態嵌入模型，`AI.GENERATE_EMBEDDING` 也適用於來自標準資料表[資料欄 (包含 `ObjectRef` 值)](https://docs.cloud.google.com/bigquery/docs/objectref-columns?hl=zh-tw) 或[物件資料表](https://docs.cloud.google.com/bigquery/docs/object-table-introduction?hl=zh-tw)的視覺內容。

如果是遠端模型，所有推論作業都會在 Vertex AI 中進行。如果是其他模型類型，所有推論作業都會在 BigQuery 中進行。結果會儲存在 BigQuery 中。

請參閱下列主題，瞭解如何在 BigQuery ML 中產生嵌入內容：

* 使用 `AI.GENERATE_EMBEDDING` 函式生成[文字](https://docs.cloud.google.com/bigquery/docs/generate-text-embedding?hl=zh-tw)、[圖片](https://docs.cloud.google.com/bigquery/docs/generate-visual-content-embedding?hl=zh-tw)或[影片](https://docs.cloud.google.com/bigquery/docs/generate-video-embedding?hl=zh-tw)。
* [生成及搜尋多模態嵌入](https://docs.cloud.google.com/bigquery/docs/generate-multimodal-embeddings?hl=zh-tw)
* [執行語意搜尋和檢索增強生成](https://docs.cloud.google.com/bigquery/docs/vector-index-text-search-tutorial?hl=zh-tw)

### 自主生成嵌入

**預覽**

這項功能適用《[服務專屬條款](https://docs.cloud.google.com/terms/service-terms?hl=zh-tw#1)》中「一般服務條款」一節的《正式發布前產品條款》。正式發布前功能是依「原樣」提供，支援服務可能受限。
詳情請參閱[推出階段說明](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages)。

**注意：** 如要提供意見回饋或尋求這項功能的支援，請傳送電子郵件至 [bq-vector-search@google.com](mailto:bq-vector-search@google.com)。

您可以使用[自主嵌入生成](https://docs.cloud.google.com/bigquery/docs/autonomous-embedding-generation?hl=zh-tw)功能，簡化建立、維護及查詢嵌入內容的程序。BigQuery 會根據來源資料欄，在資料表上維護嵌入項目資料欄。在來源資料欄中新增或修改資料時，BigQuery 會使用 Vertex AI 嵌入模型，自動為該資料產生或更新嵌入資料欄。如果來源資料會定期更新，這項功能就非常實用，可讓 BigQuery 維護您的嵌入內容。

## 搜尋

可用的搜尋功能如下：

* [`VECTOR_SEARCH`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/search_functions?hl=zh-tw#vector_search)：使用 SQL 執行向量搜尋。
* [`AI.SEARCH`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-ai-search?hl=zh-tw)
  ([預覽](https://cloud.google.com/products?hl=zh-tw#product-launch-stages))：
  搜尋與您提供的字串相近的結果。如果資料表已啟用[自主嵌入生成](#autonomous_embedding_generation)功能，即可使用這項函式。
* [`AI.SIMILARITY`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-ai-similarity?hl=zh-tw)：比較兩個輸入內容，方法是計算兩者嵌入之間的[餘弦相似度](https://wikipedia.org/wiki/Cosine_similarity)。如果您想執行少量比較，且尚未預先計算任何嵌入，就很適合使用這項函式。如果效能至關重要，且您要處理大量嵌入內容，就應該使用 `VECTOR_SEARCH`。[比較兩者的功能](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-ai-similarity?hl=zh-tw#related_functions)，選擇最適合您用途的函式。

您也可以選擇使用 [`CREATE VECTOR INDEX` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#create_vector_index_statement)建立[向量索引](https://docs.cloud.google.com/bigquery/docs/vector-index?hl=zh-tw)。使用向量索引時，`VECTOR_SEARCH` 和 `AI.SEARCH` 函式會採用[近似最鄰近](https://en.wikipedia.org/wiki/Nearest_neighbor_search#Approximation_methods)搜尋技術，提升向量搜尋效能，但會降低[召回率](https://developers.google.com/machine-learning/crash-course/classification/precision-and-recall?hl=zh-tw#recallsearch_term_rules)，因此傳回的結果較為近似。如果沒有向量索引，這些函式會使用[暴力搜尋](https://en.wikipedia.org/wiki/Brute-force_search)來測量每筆記錄的距離。您也可以選擇使用暴力搜尋法，即使有向量索引，也能取得確切結果。

## 定價

`VECTOR_SEARCH` 和 `AI.SEARCH` 函式以及 `CREATE VECTOR INDEX` 陳述式會採用 [BigQuery 計算定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#analysis_pricing_models)。

* `VECTOR_SEARCH` 和 `AI.SEARCH` 函式：系統會根據以量計價或版本計價方式，收取相似性搜尋費用。

  + 以量計價：系統會根據掃描的位元組數向您收費，包括基本資料表、索引和搜尋查詢。
  + 方案價格：系統會根據預留方案中完成工作所需的運算單元向您收費。如果相似度計算的範圍較大或較複雜，費用就會較高。

    **注意：** [標準版](https://docs.cloud.google.com/bigquery/docs/editions-intro?hl=zh-tw)不支援使用索引。
* `CREATE VECTOR INDEX`聲明：只要索引資料表資料的總大小低於機構的[限制](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#vector_index_maximum_table_size)，建立及重新整理向量索引所需的處理作業就不會產生費用。如要支援超出此限制的索引作業，您必須[自行預留資源](https://docs.cloud.google.com/bigquery/docs/vector-index?hl=zh-tw#use_your_own_reservation)，以處理索引管理工作。

儲存空間也是嵌入和索引的考量因素。以嵌入和索引形式儲存的位元組數量，會產生[動態儲存費用](https://cloud.google.com/bigquery/pricing?hl=zh-tw#storage)。

* 向量索引處於有效狀態時會產生儲存空間費用。
* 您可以使用 [`INFORMATION_SCHEMA.VECTOR_INDEXES` 檢視畫面](https://docs.cloud.google.com/bigquery/docs/information-schema-vector-indexes?hl=zh-tw)找出索引儲存空間大小。如果向量索引的涵蓋範圍尚未達到 100%，系統仍會針對已建立索引的內容向您收費。您可以使用 `INFORMATION_SCHEMA.VECTOR_INDEXES` 檢視畫面檢查索引涵蓋範圍。

## 配額與限制

詳情請參閱「[向量索引限制](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#vector_index_limits)」和「[生成式 AI 函式限制](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#generative_ai_functions)」。

## 限制

含有 `VECTOR_SEARCH` 或 `AI.SEARCH` 函式的查詢不會透過 [BigQuery BI Engine](https://docs.cloud.google.com/bigquery/docs/bi-engine-intro?hl=zh-tw) 加速。

## 後續步驟

* 進一步瞭解如何[建立向量索引](https://docs.cloud.google.com/bigquery/docs/vector-index?hl=zh-tw)。
* 瞭解如何使用 [`VECTOR_SEARCH` 函式執行向量搜尋](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/search_functions?hl=zh-tw#vector_search)。
* 瞭解如何使用 [`AI.SEARCH` 函式執行語意搜尋](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-ai-search?hl=zh-tw)。
* 進一步瞭解[自主產生嵌入內容](https://docs.cloud.google.com/bigquery/docs/autonomous-embedding-generation?hl=zh-tw)。
* 請參閱[使用向量搜尋功能搜尋嵌入](https://docs.cloud.google.com/bigquery/docs/vector-search?hl=zh-tw)教學課程，瞭解如何建立向量索引，然後使用索引和不使用索引，對嵌入執行向量搜尋。
* 請試用「執行語意搜尋和檢索增強生成」
  教學課程，瞭解如何執行下列工作：

  + 生成文字嵌入。
  + 在嵌入上建立向量索引。
  + 使用嵌入執行向量搜尋，尋找相似文字。
  + 使用向量搜尋結果增強提示輸入內容，執行檢索增強生成 (RAG)，提升結果品質。
* 請參閱「[在檢索增強生成管道中剖析 PDF](https://docs.cloud.google.com/bigquery/docs/rag-pipeline-pdf?hl=zh-tw)」教學課程，瞭解如何根據剖析的 PDF 內容建立 RAG 管道。
* 您也可以在 Python 中使用 BigQuery DataFrames 執行向量搜尋。如需說明此方法的筆記本，請參閱「[使用 BigQuery DataFrame 建構向量搜尋應用程式](https://github.com/googleapis/python-bigquery-dataframes/blob/main/notebooks/generative_ai/bq_dataframes_llm_vector_search.ipynb)」。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-09 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-09 (世界標準時間)。"],[],[]]