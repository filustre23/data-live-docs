Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 特定工作的解決方案總覽

本文說明 BigQuery ML 支援的人工智慧 (AI) 功能。您可以使用這些功能，透過 Cloud AI API 在 BigQuery ML 中開發特定工作解決方案。支援的任務包括：

* [自然語言處理](#natural_language_processing)
* [機器翻譯](#machine_translation)
* [語音轉錄](#audio_transcription)
* [文件處理](#document_processing)
* [電腦視覺](#computer_vision)

如要存取 Cloud AI API 來執行其中一項功能，請在 BigQuery ML 中建立代表 API 端點的[遠端模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model-service?hl=zh-tw)。針對要使用的 AI 資源建立遠端模型後，只要對遠端模型執行 BigQuery ML 函式，即可存取該資源的功能。

採用這種做法，您不必瞭解 Python 或熟悉 API，就能使用基礎 API 的功能。

## 工作流程

您可以搭配使用
[透過 Vertex AI 模型執行的遠端模型](https://docs.cloud.google.com/bigquery/docs/generative-ai-overview?hl=zh-tw)
和
透過 Cloud AI 服務執行的遠端模型
與 BigQuery ML 函式，完成複雜的資料分析和生成式 AI 工作。

下圖顯示一些常見工作流程，您可能會一起使用這些功能：

## 自然語言處理

您可以運用自然語言處理技術，對資料執行分類和情緒分析等作業，例如分析產品意見回饋，藉此評估顧客是否喜歡特定產品。

如要執行自然語言工作，您可以建立遠端模型並指定 `REMOTE_SERVICE_TYPE` 的 `CLOUD_AI_NATURAL_LANGUAGE_V1` 值，藉此建立 [Cloud Natural Language API](https://docs.cloud.google.com/natural-language?hl=zh-tw) 的參照。然後使用 [`ML.UNDERSTAND_TEXT` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-understand-text?hl=zh-tw)與該服務互動。`ML.UNDERSTAND_TEXT` 可處理[標準資料表](https://docs.cloud.google.com/bigquery/docs/tables-intro?hl=zh-tw#standard-tables)中的資料。所有推論作業都會在 Vertex AI 中進行。結果會儲存在 BigQuery 中。

如要瞭解詳情，請嘗試[使用 `ML.UNDERSTAND_TEXT` 函式解讀文字](https://docs.cloud.google.com/bigquery/docs/understand-text?hl=zh-tw)。

## 機器翻譯

機器翻譯技術可用來將文字資料翻譯成其他語言。
舉例來說，如果客戶是以您不熟悉的語言撰寫意見回饋，您可以將該資料翻譯成自己慣用的語言。

如要執行機器翻譯工作，請建立遠端模型並為 `REMOTE_SERVICE_TYPE` 值指定 `CLOUD_AI_TRANSLATE_V3`，藉此建立 [Cloud Translation API](https://docs.cloud.google.com/translate?hl=zh-tw) 的參照。然後使用 [`ML.TRANSLATE` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-translate?hl=zh-tw)與該服務互動。`ML.TRANSLATE` 可處理[標準資料表](https://docs.cloud.google.com/bigquery/docs/tables-intro?hl=zh-tw#standard-tables)中的資料。所有推論作業都會在 Vertex AI 中進行。結果會儲存在 BigQuery 中。

如要瞭解詳情，請嘗試[使用 `ML.TRANSLATE` 函式翻譯文字](https://docs.cloud.google.com/bigquery/docs/translate-text?hl=zh-tw)。

## 音訊轉錄

你可以運用音訊轉錄功能，將音訊檔案內容轉錄成書面文字，例如將語音留言錄音內容轉錄為文字訊息。

如要執行音訊轉錄工作，請建立遠端模型並指定 `CLOUD_AI_SPEECH_TO_TEXT_V2` 的 `REMOTE_SERVICE_TYPE` 值，藉此建立 [Speech-to-Text API](https://docs.cloud.google.com/speech-to-text?hl=zh-tw) 的參照。您可以選擇[指定要使用的辨識器](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model-service?hl=zh-tw#speech_recognizer)，處理音訊內容。然後使用 [`ML.TRANSCRIBE` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-transcribe?hl=zh-tw)轉錄音訊檔案。`ML.TRANSCRIBE` 可處理[物件表格](https://docs.cloud.google.com/bigquery/docs/object-table-introduction?hl=zh-tw)中的音訊檔案。所有推論作業都會在 Vertex AI 中進行。結果會儲存在 BigQuery 中。

如要瞭解詳情，請嘗試[使用 `ML.TRANSCRIBE` 函式轉錄音訊檔案](https://docs.cloud.google.com/bigquery/docs/transcribe?hl=zh-tw)。

## 文件處理

您可以運用文件處理功能，從非結構化文件中擷取出洞察資訊，例如擷取應付憑據檔案中的相關資訊，以便輸入會計軟體。

如要執行文件處理工作，請建立遠端模型，藉此建立 [Document AI API](https://docs.cloud.google.com/document-ai?hl=zh-tw) 的參照，並為 `REMOTE_SERVICE_TYPE` 值指定 `CLOUD_AI_DOCUMENT_V1`，然後[指定要使用的處理器](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model-service?hl=zh-tw#document_processor)來處理文件內容。然後，您可以使用 [`ML.PROCESS_DOCUMENT` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-process-document?hl=zh-tw)處理文件。`ML.PROCESS_DOCUMENT` 可處理[物件資料表](https://docs.cloud.google.com/bigquery/docs/object-table-introduction?hl=zh-tw)中的文件。所有推論作業都會在 Vertex AI 中進行。結果會儲存在 BigQuery 中。

如要瞭解詳情，請嘗試[使用 `ML.PROCESS_DOCUMENT` 函式處理文件](https://docs.cloud.google.com/bigquery/docs/process-document?hl=zh-tw)。

## 電腦視覺

您可以運用電腦視覺技術，執行圖像分析工作，例如分析圖像來偵測當中是否有臉孔，或生成描述圖中物體的標籤。

如要執行電腦視覺工作，請建立遠端模型並指定 `REMOTE_SERVICE_TYPE` 的 `CLOUD_AI_VISION_V1` 值為 `CLOUD_AI_VISION_V1`，藉此建立 [Cloud Vision API](https://docs.cloud.google.com/vision?hl=zh-tw) 的參照。然後，您可以使用[`ML.ANNOTATE_IMAGE` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-annotate-image?hl=zh-tw)，透過該服務為圖片加上註解。`ML.ANNOTATE_IMAGE` 會處理[物件資料表](https://docs.cloud.google.com/bigquery/docs/object-table-introduction?hl=zh-tw)中的資料。所有推論作業都會在 Vertex AI 中進行。結果會儲存在 BigQuery 中。

如要瞭解詳情，請嘗試[使用 `ML.ANNOTATE_IMAGE` 函式為物件表格圖片加上註解](https://docs.cloud.google.com/bigquery/docs/annotate-image?hl=zh-tw)。

## 後續步驟

* 如要進一步瞭解如何對機器學習模型執行推論，請參閱[模型推論總覽](https://docs.cloud.google.com/bigquery/docs/inference-overview?hl=zh-tw)。
* 如要進一步瞭解生成式 AI 模型支援的 SQL 陳述式和函式，請參閱[生成式 AI 模型的端對端使用者歷程](https://docs.cloud.google.com/bigquery/docs/e2e-journey-genai?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-16 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-16 (世界標準時間)。"],[],[]]