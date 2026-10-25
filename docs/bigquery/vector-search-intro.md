Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 嵌入和向量搜尋簡介

本文件概略說明 BigQuery 中的嵌入和向量搜尋。向量搜尋是一種使用嵌入項目比較相似物件的技術，用於支援 Google 產品，包括 Google 搜尋、YouTube 和 Google Play。您可以使用向量搜尋大規模執行語意搜尋，也可以執行**混合搜尋**，結合語意搜尋和詞彙 (關鍵字) 搜尋。搭配向量搜尋使用[向量索引](https://docs.cloud.google.com/bigquery/docs/vector-index?hl=zh-tw)時，您可以運用反向檔案索引 (IVF) 和 [ScaNN 演算法](https://research.google/blog/announcing-scann-efficient-vector-similarity-search/?hl=zh-tw)等基礎技術。

向量搜尋是以嵌入為基礎建構而成。嵌入是高維度數值向量，代表特定實體，例如文字或音訊檔案。機器學習 (ML) 模型會使用嵌入技術，將這類實體的語意編碼，方便推論及比較。舉例來說，分群、分類和推薦模型中的常見作業，是測量[嵌入空間](https://en.wikipedia.org/wiki/Latent_space)中向量之間的距離，找出語意最相似的項目。

當您考量如何繪製不同項目時，會發現語意相似度和嵌入空間中的距離，可以透過視覺化方式呈現。舉例來說，「貓」、「狗」和「獅子」等字詞都代表動物類型，因此在這個空間中，這些字詞會因語意特徵相同而分在同一組。同樣地，*汽車*、*卡車*和較通用的*車輛*等字詞會形成另一個叢集。如下圖所示：

您可以看到動物和車輛叢集的位置相距甚遠。群組之間的區隔說明瞭一項原則：在嵌入空間中，物件越接近，語意越相似；距離越遠，語意差異越大。

## 用途

結合嵌入生成和向量搜尋，可實現許多有趣的用途。以下是部分可能用途：

* **[檢索增強生成 (RAG)](https://cloud.google.com/use-cases/retrieval-augmented-generation?hl=zh-tw)：**
  在 BigQuery 中，使用 Gemini 模型剖析文件、對內容執行向量搜尋，並生成自然語言問題的摘要回覆。如需說明這個情境的筆記本，請參閱「[使用 BigQuery DataFrames 建構向量搜尋應用程式](https://github.com/googleapis/python-bigquery-dataframes/blob/main/notebooks/generative_ai/bq_dataframes_llm_vector_search.ipynb)」。
* **推薦替代產品或相符產品：**根據顧客行為和產品相似度，建議替代產品，強化電子商務應用程式。
* **記錄檔分析：**協助團隊主動分類記錄中的異常狀況，並加快調查速度。您也可以使用這項功能，為 LLM 增補情境資訊，以改善威脅偵測、鑑識和疑難排解工作流程。如要查看說明這個情境的筆記本，請參閱「[使用文字嵌入和 BigQuery 向量搜尋偵測及調查記錄檔異常狀況](https://github.com/GoogleCloudPlatform/generative-ai/blob/main/embeddings/use-cases/outlier-detection/bq-vector-search-outlier-detection-audit-logs.ipynb)」。
* **分群和指定目標：**精確區隔目標對象。舉例來說，連鎖醫院可以使用自然語言附註和結構化資料將病患分群，行銷人員則可根據查詢意圖指定廣告。如需說明這個情境的筆記本，請參閱「[Create-Campaign-Customer-Segmentation](https://github.com/GoogleCloudPlatform/chocolate-ai/blob/main/colab-enterprise/Create-Campaign-Customer-Segmentation.ipynb)」。
* **實體解析與簡化：**清理及整合資料。舉例來說，廣告公司可以簡化個人識別資訊 (PII) 記錄，房地產公司則可找出相符的郵寄地址。

## 生成嵌入項目

以下各節說明 BigQuery 提供的函式，可協助您生成或使用嵌入項目。

### 生成單一嵌入

您可以搭配使用 [`AI.EMBED` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-ai-embed?hl=zh-tw)和 Gemini Enterprise Agent Platform 嵌入模型，為輸入內容生成單一嵌入。

`AI.EMBED` 函式支援下列輸入類型：

* 文字資料。
* 以 [`ObjectRef`](https://docs.cloud.google.com/bigquery/docs/work-with-objectref?hl=zh-tw) 值表示的圖片資料。

### 生成嵌入項目資料表

您可以使用 [`AI.GENERATE_EMBEDDING`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-ai-generate-embedding?hl=zh-tw)，建立一個資料表，其中包含輸入資料表中某個資料欄的所有資料嵌入。`AI.GENERATE_EMBEDDING` 支援所有類型的模型，可處理[標準資料表](https://docs.cloud.google.com/bigquery/docs/tables-intro?hl=zh-tw#standard-tables)中的結構化資料。如果是多模態嵌入模型，`AI.GENERATE_EMBEDDING` 也適用於[包含 `ObjectRef` 值的標準資料表資料欄](https://docs.cloud.google.com/bigquery/docs/objectref-columns?hl=zh-tw)，或[物件資料表](https://docs.cloud.google.com/bigquery/docs/object-table-introduction?hl=zh-tw)中的視覺內容。

如果是遠端模型，所有推論都會在 Agent Platform 中進行。如果是其他模型類型，所有推論作業都會在 BigQuery 中進行。結果會儲存在 BigQuery 中。

請參閱下列主題，嘗試在 BigQuery ML 中生成嵌入：

* 使用 `AI.GENERATE_EMBEDDING` 函式生成[文字](https://docs.cloud.google.com/bigquery/docs/generate-text-embedding?hl=zh-tw)、[圖片](https://docs.cloud.google.com/bigquery/docs/generate-visual-content-embedding?hl=zh-tw)或[影片](https://docs.cloud.google.com/bigquery/docs/generate-video-embedding?hl=zh-tw)。
* [生成及搜尋多模態嵌入](https://docs.cloud.google.com/bigquery/docs/generate-multimodal-embeddings?hl=zh-tw)
* [執行語意搜尋和檢索增強生成](https://docs.cloud.google.com/bigquery/docs/vector-index-text-search-tutorial?hl=zh-tw)

### 自主生成嵌入

您可以使用[自主嵌入生成](https://docs.cloud.google.com/bigquery/docs/autonomous-embedding-generation?hl=zh-tw)功能，簡化建立、維護及查詢嵌入的程序。BigQuery 會根據來源資料欄，在資料表中維護嵌入資料欄。您在來源資料欄新增或修改資料時，BigQuery 會使用 Agent Platform 嵌入模型，自動生成或更新該項資料的嵌入資料欄。如果來源資料會定期更新，且您希望 BigQuery 維護嵌入，這個方法就非常實用。

## 搜尋

您可以使用下列搜尋函式，執行語意向量搜尋，或結合語意搜尋和詞彙關鍵字搜尋的**混合搜尋**：

* [`VECTOR_SEARCH`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/search_functions?hl=zh-tw#vector_search)：使用 SQL 執行語意向量搜尋或混合搜尋。
* [`AI.SEARCH`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-ai-search?hl=zh-tw)：執行語意或混合搜尋，找出與您提供的字串相近的結果。如果資料表已啟用[自主嵌入生成](#autonomous_embedding_generation)功能，就能使用這個函式。
* [`AI.SIMILARITY`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-ai-similarity?hl=zh-tw)：
  比較兩個輸入內容，方法是計算兩者嵌入之間的[餘弦相似度](https://wikipedia.org/wiki/Cosine_similarity)。如果您想執行少量比較，且尚未預先計算任何嵌入內容，這項函式就非常適合。如果效能至關重要，且您要處理大量嵌入，請使用 `VECTOR_SEARCH`。[比較這些函式的功能](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-ai-similarity?hl=zh-tw#related_functions)，選擇最適合您用途的函式。

您也可以
使用
[`CREATE VECTOR INDEX` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#create_vector_index_statement)建立[向量索引](https://docs.cloud.google.com/bigquery/docs/vector-index?hl=zh-tw)。使用向量索引時，`VECTOR_SEARCH` 和 `AI.SEARCH` 函式會採用[近似最鄰近](https://en.wikipedia.org/wiki/Nearest_neighbor_search#Approximation_methods)搜尋技術，提高向量搜尋效能，但代價是[喚回度](https://developers.google.com/machine-learning/crash-course/classification/precision-and-recall?hl=zh-tw#recallsearch_term_rules)降低，因此會傳回更多近似結果。如果沒有向量索引，這些函式會使用[暴力搜尋](https://en.wikipedia.org/wiki/Brute-force_search)來測量每筆記錄的距離。即使有向量索引，您也可以選擇使用暴力破解法取得精確結果。

## 定價

`VECTOR_SEARCH` 和 `AI.SEARCH` 函式以及 `CREATE VECTOR INDEX` 陳述式採用 [BigQuery 運算定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#analysis_pricing_models)。

* `VECTOR_SEARCH` 和 `AI.SEARCH` 函式：系統會依據相似度搜尋，按照隨選或版本定價計費。

  + 隨選：系統會根據基礎資料表、索引和搜尋查詢中掃描的位元組數收費。
  + 版本定價：系統會根據預留版本中完成工作所需的運算單元數量收費。相似度計算越複雜、規模越大，費用就越高。

    **注意：** [標準版](https://docs.cloud.google.com/bigquery/docs/editions-intro?hl=zh-tw)不支援使用索引。
* `CREATE VECTOR INDEX` 聲明：只要索引資料表資料總大小低於貴組織的[限制](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#vector_index_maximum_table_size)，就不會產生建構及重新整理向量索引所需的處理費用。如要支援超出此限制的索引作業，您必須[提供自己的預留空間](https://docs.cloud.google.com/bigquery/docs/vector-index?hl=zh-tw#use_your_own_reservation)，以處理索引管理工作。

儲存空間也是嵌入和索引的考量因素。以嵌入和索引形式儲存的位元組數量，會產生[有效儲存空間費用](https://cloud.google.com/bigquery/pricing?hl=zh-tw#storage)。

* 向量索引啟用時會產生儲存費用。
* 您可以使用 [`INFORMATION_SCHEMA.VECTOR_INDEXES` 檢視畫面](https://docs.cloud.google.com/bigquery/docs/information-schema-vector-indexes?hl=zh-tw)查看索引儲存空間大小。如果向量索引涵蓋率尚未達到 100%，系統仍會針對已建立索引的內容收費。您可以使用 `INFORMATION_SCHEMA.VECTOR_INDEXES` 檢視畫面查看索引涵蓋範圍。

## 配額與限制

詳情請參閱「[向量索引限制](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#vector_index_limits)」和「[生成式 AI 函式限制](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#generative_ai_functions)」。

## 限制

* [BigQuery BI Engine](https://docs.cloud.google.com/bigquery/docs/bi-engine-intro?hl=zh-tw) 不會加速含有 `VECTOR_SEARCH` 或 `AI.SEARCH` 函式的查詢。
* 只有在篩選「分區資料欄」或「儲存的資料欄」時，系統才會針對 `VECTOR_SEARCH` 和 `AI.SEARCH` 查詢預先篩選資料修剪作業進行最佳化，篩選「叢集資料欄」時則不會。在預先篩選子查詢中使用非儲存的叢集資料欄，會導致完整的資料表掃描。詳情請參閱「[預先篩選限制](https://docs.cloud.google.com/bigquery/docs/vector-index?hl=zh-tw#pre-filtering_limitations)」。

## 後續步驟

* 進一步瞭解如何[建立向量索引](https://docs.cloud.google.com/bigquery/docs/vector-index?hl=zh-tw)，以及[搭配混合型搜尋使用向量索引](https://docs.cloud.google.com/bigquery/docs/vector-index?hl=zh-tw#use_vector_indexes_with_hybrid_search)。
* 瞭解如何使用 [`VECTOR_SEARCH` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/search_functions?hl=zh-tw#vector_search)執行語意或混合搜尋。
* 瞭解如何使用 [`AI.SEARCH` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-ai-search?hl=zh-tw)執行語意或混合搜尋。
* 進一步瞭解[自主嵌入生成功能](https://docs.cloud.google.com/bigquery/docs/autonomous-embedding-generation?hl=zh-tw)。
* 請試用「[使用向量搜尋功能搜尋嵌入](https://docs.cloud.google.com/bigquery/docs/vector-search?hl=zh-tw)」教學課程，瞭解如何建立向量索引，然後在有和沒有索引的情況下，對嵌入執行向量搜尋。
* 試用「[執行語意搜尋和檢索增強生成](https://docs.cloud.google.com/bigquery/docs/vector-index-text-search-tutorial?hl=zh-tw)」教學課程，瞭解如何執行下列工作：

  + 生成文字嵌入。
  + 在嵌入上建立向量索引。
  + 使用嵌入執行向量搜尋，找出相似文字。
  + 使用向量搜尋結果執行檢索增強生成 (RAG)，強化提示輸入並改善結果。
* 請參閱「[在檢索增強生成管道中剖析 PDF](https://docs.cloud.google.com/bigquery/docs/rag-pipeline-pdf?hl=zh-tw)」教學課程，瞭解如何根據剖析的 PDF 內容建立 RAG 管道。
* 您也可以在 Python 中使用 BigQuery DataFrames 執行向量搜尋。如需說明這個方法的筆記本，請參閱「[使用 BigQuery DataFrames 建構向量搜尋應用程式](https://github.com/googleapis/python-bigquery-dataframes/blob/main/notebooks/generative_ai/bq_dataframes_llm_vector_search.ipynb)」。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-10-24 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-10-24 (世界標準時間)。"],[],[]]