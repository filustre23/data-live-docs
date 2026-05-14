Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 生成式 AI 模型的端對端使用者歷程

本文說明 BigQuery ML 遠端模型的使用者歷程，包括可用於處理遠端模型的陳述式和函式。BigQuery ML 提供下列類型的遠端模型：

* [微調後的 Google Gemini 模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model-tuned?hl=zh-tw)
* [Google、合作夥伴和開放式模型即服務](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model?hl=zh-tw)
* [Google 文字嵌入模型即服務](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model-embedding-maas?hl=zh-tw)
* [自行部署的開放式模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model-open?hl=zh-tw)
* [Cloud AI 服務](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model-service?hl=zh-tw)
* [部署至 Vertex AI 的自訂模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model-https?hl=zh-tw)

## 遠端模型使用者歷程

下表說明可用於建立、評估及產生遠端模型資料的陳述式和函式：

| 模型類別 | 模型類型 | 模型建立 | [評估](https://docs.cloud.google.com/bigquery/docs/evaluate-overview?hl=zh-tw) | [推論](https://docs.cloud.google.com/bigquery/docs/inference-overview?hl=zh-tw) | 教學課程 |
| --- | --- | --- | --- | --- | --- |
| 生成式 AI 遠端模型 | 透過 Gemini 文字生成模型使用遠端模型1 | [`CREATE MODEL`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model?hl=zh-tw) | [`ML.EVALUATE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-evaluate?hl=zh-tw) | * [`AI.GENERATE_TEXT`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-ai-generate-text?hl=zh-tw) * [`AI.GENERATE_TABLE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-generate-table?hl=zh-tw) * [`AI.GENERATE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-ai-generate?hl=zh-tw)2 * [`AI.GENERATE_BOOL`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-ai-generate-bool?hl=zh-tw)2 * [`AI.GENERATE_DOUBLE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-ai-generate-double?hl=zh-tw)2 * [`AI.GENERATE_INT`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-ai-generate-int?hl=zh-tw)2 | * [使用資料生成文字](https://docs.cloud.google.com/bigquery/docs/generate-text-tutorial?hl=zh-tw) * [使用資料產生結構化資料](https://docs.cloud.google.com/bigquery/docs/generate-table?hl=zh-tw) * [使用 Gemini 和公開資料生成文字](https://docs.cloud.google.com/bigquery/docs/generate-text-tutorial-gemini?hl=zh-tw) * [透過反覆呼叫 `ML.GENERATE_TEXT` 處理配額錯誤](https://docs.cloud.google.com/bigquery/docs/iterate-generate-text-calls?hl=zh-tw) * [使用 Gemini 模型分析圖片](https://docs.cloud.google.com/bigquery/docs/image-analysis?hl=zh-tw) * [使用公開資料調整模型](https://docs.cloud.google.com/bigquery/docs/tune-evaluate?hl=zh-tw) * [使用資料調整模型](https://docs.cloud.google.com/bigquery/docs/generate-text-tuning?hl=zh-tw) |
| 遠端模型優於合作夥伴文字生成模型 | [`CREATE MODEL`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model?hl=zh-tw) | [`ML.EVALUATE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-evaluate?hl=zh-tw) | [`AI.GENERATE_TEXT`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-ai-generate-text?hl=zh-tw) | 不適用 |
| 開放式文字生成模型上的遠端模型3 | [`CREATE MODEL`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model-open?hl=zh-tw) | [`ML.EVALUATE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-evaluate?hl=zh-tw) | [`AI.GENERATE_TEXT`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-ai-generate-text?hl=zh-tw) | [使用 Gemma 和公開資料生成文字](https://docs.cloud.google.com/bigquery/docs/generate-text-tutorial-gemma?hl=zh-tw) |
| Google 嵌入生成模型上的遠端模型 | [`CREATE MODEL`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model-embedding-maas?hl=zh-tw) | 不適用 | [`AI.GENERATE_EMBEDDING`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-ai-generate-embedding?hl=zh-tw) | * [使用資料生成文字嵌入](https://docs.cloud.google.com/bigquery/docs/generate-text-embedding?hl=zh-tw) * [使用資料生成圖片嵌入](https://docs.cloud.google.com/bigquery/docs/generate-visual-content-embedding?hl=zh-tw) * [使用資料生成影片嵌入](https://docs.cloud.google.com/bigquery/docs/generate-video-embedding?hl=zh-tw) * [透過反覆呼叫 `ML.GENERATE_EMBEDDING` 處理配額錯誤](https://docs.cloud.google.com/bigquery/docs/iterate-generate-embedding-calls?hl=zh-tw) * [使用公開資料生成及搜尋多模態嵌入](https://docs.cloud.google.com/bigquery/docs/generate-multimodal-embeddings?hl=zh-tw) |
| 透過開放式嵌入生成模型使用遠端模型3 | [`CREATE MODEL`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model-open?hl=zh-tw) | 不適用 | [`AI.GENERATE_EMBEDDING`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-ai-generate-embedding?hl=zh-tw) | [使用開放模型和 `AI.GENERATE_EMBEDDING` 函式生成文字嵌入](https://docs.cloud.google.com/bigquery/docs/generate-text-embedding-tutorial-open-models?hl=zh-tw) |
| Cloud AI 遠端模型 | 透過 Cloud Vision API 使用遠端模型 | [`CREATE MODEL`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model-service?hl=zh-tw) | 不適用 | [`ML.ANNOTATE_IMAGE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-annotate-image?hl=zh-tw) | [為圖片加上註解](https://docs.cloud.google.com/bigquery/docs/annotate-image?hl=zh-tw) |
| 透過 Cloud Translation API 使用遠端模型 | [`CREATE MODEL`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model-service?hl=zh-tw) | 不適用 | [`ML.TRANSLATE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-translate?hl=zh-tw) | [翻譯文字](https://docs.cloud.google.com/bigquery/docs/translate-text?hl=zh-tw) |
| 透過 Cloud Natural Language API 使用遠端模型 | [`CREATE MODEL`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model-service?hl=zh-tw) | 不適用 | [`ML.UNDERSTAND_TEXT`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-understand-text?hl=zh-tw) | [瞭解文字](https://docs.cloud.google.com/bigquery/docs/understand-text?hl=zh-tw) |
| 透過 Document AI API 使用遠端模型 | [`CREATE MODEL`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model-service?hl=zh-tw) | 不適用 | [`ML.PROCESS_DOCUMENT`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-process-document?hl=zh-tw) | * [處理文件](https://docs.cloud.google.com/bigquery/docs/process-document?hl=zh-tw) * [在 RAG 管道中剖析 PDF](https://docs.cloud.google.com/bigquery/docs/rag-pipeline-pdf?hl=zh-tw) |
| 透過 Speech-to-Text API 使用遠端模型 | [`CREATE MODEL`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model-service?hl=zh-tw) | 不適用 | [`ML.TRANSCRIBE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-transcribe?hl=zh-tw) | [轉錄音訊檔案](https://docs.cloud.google.com/bigquery/docs/transcribe?hl=zh-tw) |
| 透過部署至 Vertex AI 的自訂模型使用遠端模型 | 透過部署至 Vertex AI 的自訂模型使用遠端模型 | [`CREATE MODEL`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model-https?hl=zh-tw) | [`ML.EVALUATE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-evaluate?hl=zh-tw) | [`ML.PREDICT`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-predict?hl=zh-tw) | [使用自訂模型進行預測](https://docs.cloud.google.com/bigquery/docs/bigquery-ml-remote-model-tutorial?hl=zh-tw) |

1 部分 Gemini 模型支援[監督式調整](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model-tuned?hl=zh-tw#supervised_tuning)。

2 這個函式會呼叫代管的 Gemini 模型，因此您不需要使用 `CREATE MODEL` 陳述式另外建立模型。

3 建立 BigQuery ML 遠端模型時，指定模型的 Hugging Face 或 Vertex AI Model Garden ID，即可自動部署開放式模型。BigQuery 會管理以這種方式部署的開放模型 Vertex AI 資源，並讓您使用 BigQuery ML `ALTER MODEL` 和 `DROP MODEL` 陳述式與這些 Vertex AI 資源互動。您也可以設定自動取消部署模型。
詳情請參閱「[自動部署模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model-open?hl=zh-tw#automatically_deployed_models)」。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-14 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-14 (世界標準時間)。"],[],[]]