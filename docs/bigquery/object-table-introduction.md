Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 物件資料表簡介

本文說明物件資料表，這類資料表是 Cloud Storage 中非結構化資料物件的唯讀資料表。

您可以使用物件資料表分析 Cloud Storage 中的非結構化資料。您可以使用遠端函式執行分析，或使用 BigQuery ML 執行推論，然後將這些作業的結果與 BigQuery 中的其餘結構化資料彙整。

與 BigLake 資料表一樣，物件資料表會使用存取權委派，將物件資料表的存取權與 Cloud Storage 物件的存取權分開。與服務帳戶相關聯的[外部連線](https://docs.cloud.google.com/bigquery/docs/working-with-connections?hl=zh-tw)會用於連線至 Cloud Storage，因此您只需要授予使用者物件資料表的存取權。這項功能可讓您強制執行[資料列層級](https://docs.cloud.google.com/bigquery/docs/row-level-security-intro?hl=zh-tw)安全防護機制，並管理使用者可存取的物件。

您可以使用 [`CREATE EXTERNAL TABLE` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#create_external_table_statement)建立物件資料表，如下列範例所示：

```
CREATE EXTERNAL TABLE `myproject.mydataset.myobjecttable`
WITH CONNECTION `myproject.us.myconnection`
OPTIONS ( object_metadata = 'SIMPLE', uris = ['gs://mybucket/*'] );
```

如要進一步瞭解如何建立物件資料表，請參閱「[建立物件資料表](https://docs.cloud.google.com/bigquery/docs/object-tables?hl=zh-tw)」一文。

**注意：**
管理[外部身分識別資訊提供者](https://docs.cloud.google.com/iam/docs/workforce-identity-federation?hl=zh-tw)中使用者存取權時，請將 Google 帳戶主體 ID (例如 `user:kiran@example.com`、`group:support@example.com` 和 `domain:example.com`) 替換為適當的[員工身分聯盟主體 ID](https://docs.cloud.google.com/iam/docs/principal-identifiers?hl=zh-tw)。

## 物件資料表結構定義

物件資料表會針對指定 Cloud Storage 值區中的非結構化資料物件，提供中繼資料索引。資料表的每一列都對應到一個物件，而資料表的欄則對應到 Cloud Storage 產生的物件中繼資料，包括任何[自訂中繼資料](https://docs.cloud.google.com/storage/docs/metadata?hl=zh-tw#custom-metadata)。

物件資料表也包含 `data` 虛擬資料欄，代表原始位元組中的檔案內容，建立物件資料表時會自動填入。對圖片資料執行推論時，[`ML.DECODE_IMAGE` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-decode-image?hl=zh-tw)會使用這個虛擬資料欄。您無法在查詢中加入 `data` 虛擬資料欄，且該資料欄不會顯示為物件表格結構定義的一部分。

下表說明物件資料表使用的固定結構定義：

| **欄位名稱** | **類型** | **眾數** | **說明** |
| --- | --- | --- | --- |
| `uri` | STRING | NULLABLE | `uri`：物件的統一資源識別碼 (URI)，格式為 `gs://bucket_name/[folder_name/]object_name`。 |
| `generation` | INTEGER | NULLABLE | 這個物件的[產生](https://docs.cloud.google.com/storage/docs/metadata?hl=zh-tw#generation-number)編號，用於識別物件版本。 |
| `content_type` | STRING | NULLABLE | 物件資料的 [Content-Type](https://docs.cloud.google.com/storage/docs/metadata?hl=zh-tw#content-type)，用於識別媒體類型。如果儲存物件時未指定 Content-Type，系統會將其視為 application/octet-stream。 |
| `size` | INTEGER | NULLABLE | 資料的 [Content-Length](https://datatracker.ietf.org/doc/html/rfc7230#section-3.3.2) (以位元組為單位)。 |
| `md5_hash` | STRING | NULLABLE | 資料的 [MD5 雜湊](https://wikipedia.org/wiki/MD5)，使用 [base64](https://datatracker.ietf.org/doc/html/rfc4648#section-4) 編碼。 如要進一步瞭解如何使用 MD5 雜湊值，請參閱 [Cloud Storage 物件中繼資料](https://docs.cloud.google.com/storage/docs/metadata?hl=zh-tw#md5)。 |
| `updated` | TIMESTAMP | NULLABLE | 上次修改物件中繼資料的時間。 |
| `metadata` | RECORD | REPEATED | 物件的[自訂中繼資料](https://docs.cloud.google.com/storage/docs/metadata?hl=zh-tw#custom-metadata)。每個中繼資料都以鍵值組合的形式，顯示在 `metadata` 欄位的子項 `(metadata.)name` 和 `(metadata.)value` 欄位中。 |
| `(metadata.)name` | STRING | NULLABLE | 輸入個別中繼資料項目。 |
| `(metadata.)value` | STRING | NULLABLE | 個別中繼資料項目的值。 |
| `ref` | STRUCT | NULLABLE | 以 [`ObjectRef` 格式儲存的 Google 管理 Cloud Storage 中繼資料](https://docs.cloud.google.com/bigquery/docs/work-with-objectref?hl=zh-tw)。   您可以使用這個資料欄 [在標準表格中維護 `ObjectRef` 值](https://docs.cloud.google.com/bigquery/docs/objectref-columns?hl=zh-tw)。 `ObjectRef` 值可讓您整合物件資料和結構化資料。 |

物件資料表中的資料列類似於下列內容：

```
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
|  uri                 | generation | content_type | size  | md5_hash   | updated                        | metadata...name | metadata...value  | ref.uri              | ref.version | ref.authorizer | ref.details                                              |
—----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
| gs://mybucket/a.jpeg | 165842…    | image/jpeg   | 26797 | 8c33be10f… | 2022-07-21 17:35:40.148000 UTC | null            | null              | gs://mybucket/a.jpeg | 12345678    | us.conn        | {"gcs_metadata":{"content_type":"image/jpeg","md5_hash"… |
—----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
| gs://mybucket/b.bmp  | 305722…    | image/bmp    | 57932 | 44eb90cd1… | 2022-05-14 12:09:38.114000 UTC | null            | null              | gs://mybucket/b.bmp  | 23456789    | us.conn        | {"gcs_metadata":{"content_type":"image/bmp","md5_hash"…  |
—----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
```

## 用途

查詢物件資料表中的中繼資料時，方法與查詢任何其他 BigQuery 資料表相同。不過，物件表格的主要用途是讓非結構化資料可供分析。您可以使用 BigQuery ML，透過 TensorFlow、TensorFlow Lite 和 PyTorch 模型，對圖像物件表格[執行推論作業](https://docs.cloud.google.com/bigquery/docs/object-table-inference?hl=zh-tw)。您也可以使用[遠端函式](https://docs.cloud.google.com/bigquery/docs/remote-functions?hl=zh-tw)，以幾乎任何方式[分析非結構化資料](https://docs.cloud.google.com/bigquery/docs/object-table-remote-function?hl=zh-tw)。舉例來說，您可以建立遠端函式，使用 [Cloud Vision](https://docs.cloud.google.com/vision/docs?hl=zh-tw) 分析圖片，或是使用 [Apache Tika](https://tika.apache.org/) 從 PDF 文件擷取中繼資料。

下表說明可用於對物件表格資料執行機器學習的整合點：

| **整合** | **說明** | **用途** | **教學課程** |
| --- | --- | --- | --- |
| [`AI.GENERATE_TEXT` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-ai-generate-text?hl=zh-tw) | 使用 Vertex AI、合作夥伴或開放原始碼模型生成文字。 | 您想從物件資料生成文字。 | [使用 `AI.GENERATE_TEXT` 函式生成文字](https://docs.cloud.google.com/bigquery/docs/generate-text?hl=zh-tw) |
| [`AI.GENERATE_EMBEDDING` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-ai-generate-embedding?hl=zh-tw) | 使用 Vertex AI 多模態模型生成嵌入。 | 您想為影片或圖片資料生成嵌入項目，以用於向量搜尋、模型輸入或其他用途。 | [使用 `AI.GENERATE_EMBEDDING` 函式生成圖片嵌入](https://docs.cloud.google.com/bigquery/docs/generate-visual-content-embedding?hl=zh-tw)   [使用 `AI.GENERATE_EMBEDDING` 函式生成影片嵌入](https://docs.cloud.google.com/bigquery/docs/generate-video-embedding?hl=zh-tw) |
| [匯入的 BigQuery ML 模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/inference-overview?hl=zh-tw#inference_using_imported_models) | 將 [TensorFlow](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-tensorflow?hl=zh-tw)、[TensorFlow Lite](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-tflite?hl=zh-tw) 或 [ONNX](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-onnx?hl=zh-tw) 模型匯入 BigQuery ML，即可在 BigQuery 中執行本機推論。 | 您使用的開放原始碼或自訂模型符合[支援的限制](https://docs.cloud.google.com/bigquery/docs/object-table-inference?hl=zh-tw#limitations)。 | [教學課程：使用特徵向量模型對物件資料表執行推論](https://docs.cloud.google.com/bigquery/docs/inference-tutorial-mobilenet?hl=zh-tw) |
| [Cloud Run functions](https://docs.cloud.google.com/bigquery/docs/object-table-remote-function?hl=zh-tw) | 使用 Cloud Run functions 呼叫服務或代管模型。這是最通用的整合方式。 | 您在 Compute Engine、Google Kubernetes Engine 或其他客戶擁有的基礎架構上自行代管模型。 |  |
| [`ML.ANNOTATE_IMAGE` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-annotate-image?hl=zh-tw) | 使用 Cloud Vision API 為圖片加上註解。 | 您想使用 Vision API 預先訓練模型為圖片加上註解。 | [使用 `ML.ANNOTATE_IMAGE` 函式為圖片加上註解](https://docs.cloud.google.com/bigquery/docs/annotate-image?hl=zh-tw) |
| [`ML.PROCESS_DOCUMENT` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-process-document?hl=zh-tw) | 使用 Document AI API 擷取文件洞察資訊。 | 您想使用 Document AI 預先訓練或自訂文件處理器。 | [使用 `ML.PROCESS_DOCUMENT` 函式處理文件](https://docs.cloud.google.com/bigquery/docs/process-document?hl=zh-tw) |
| [`ML.TRANSCRIBE` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-transcribe?hl=zh-tw) | 使用 Speech-to-Text API 轉錄音訊檔案。 | 您想使用 Speech-to-Text 預先訓練或自訂的語音辨識器。 | [使用 `ML.TRANSCRIBE` 函式轉錄音訊檔案](https://docs.cloud.google.com/bigquery/docs/transcribe?hl=zh-tw) |

如要將分析結果與其他結構化資料合併，可以從分析結果建立檢視畫面或表格。舉例來說，下列陳述式會根據推論結果建立資料表：

```
CREATE TABLE my_dataset.my_inference_results AS
SELECT uri, content_type, vision_feature
FROM ML.PREDICT(
  MODEL my_dataset.vision_model,
  SELECT ML.DECODE_IMAGE(data) AS vision_input
  FROM my_dataset.object_table
);
```

建立資料表後，您可以根據標準或自訂中繼資料欄位，將資料表與其他資料表彙整，如下所示：

```
SELECT a.vision_feature, a.uri, b.description
FROM my_dataset.my_inference_results a
JOIN my_dataset.image_description b
ON a.uri = b.uri;
```

您也可以[建立搜尋索引](https://docs.cloud.google.com/bigquery/docs/search-index?hl=zh-tw)，以便搜尋分析結果。舉例來說，下列陳述式會針對從 PDF 檔案擷取的資料建立搜尋索引：

```
CREATE SEARCH INDEX my_index ON pdf_text_extract(ALL COLUMNS);
```

接著，您可以使用索引在這些結果中尋找所需內容：

```
SELECT * FROM pdf_text_extract WHERE SEARCH(pdf_text, 'Google');
```

## 優點

在 BigQuery 中以原生方式分析非結構化資料，可帶來以下優點：

* 可自動執行預先處理步驟 (例如根據模型需求調整圖片大小)，減少手動作業。
* 您可以使用熟悉的 SQL 介面處理非結構化資料。
* 這項功能可讓您使用現有的 BigQuery 運算單元，不必佈建新的運算形式，有助於節省成本。

## 經簽署的網址

如要存取物件代表的資料，請產生簽署網址。您可以使用經簽署的網址直接查看物件資料，也可以[將經簽署的網址傳遞至遠端函式](https://docs.cloud.google.com/bigquery/docs/object-table-remote-function?hl=zh-tw)，讓函式處理物件資料表資料。

使用 [`EXTERNAL_OBJECT_TRANSFORM` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/table-functions-built-in?hl=zh-tw#external_object_transform)產生已簽署的網址，如下列範例所示：

```
SELECT uri, signed_url
FROM EXTERNAL_OBJECT_TRANSFORM(TABLE `mydataset.myobjecttable`, ['SIGNED_URL']);
```

這會傳回類似下列內容的結果：

```
---------------------------------------------------------------------------------------------------
|  uri                 | signed_url                                                               |
—--------------------------------------------------------------------------------------------------
| gs://mybucket/a.docx | https://storage.googleapis.com/mybucket/a.docx?X-Goog-Signature=abcd&... |
—-------------------------------------------------------------------------------------------------
| gs://mybucket/b.pdf  | https://storage.googleapis.com/mybucket/b.pdf?X-Goog-Signature=wxyz&...  |
—--------------------------------------------------------------------------------------------------
```

從物件資料表產生的已簽署網址，可讓任何擁有該網址的使用者或程序讀取對應的物件。產生的已簽署網址會在 6 小時後失效。詳情請參閱「[Cloud Storage 簽署網址](https://docs.cloud.google.com/storage/docs/access-control/signed-urls?hl=zh-tw)」。

## 存取權控管

物件資料表是以 BigLake 為基礎建構，因此會使用以服務帳戶為基礎的[外部連線](https://docs.cloud.google.com/bigquery/docs/working-with-connections?hl=zh-tw)，存取 Cloud Storage 資料。這項功能透過存取權委派，將資料表的存取權與基礎物件儲存庫的存取權分開。您授予服務帳戶權限，從物件存取資料和中繼資料，並在資料表中顯示。您只會授予使用者資料表的權限，並可使用 Identity and Access Management (IAM) 和[資料列層級安全性](https://docs.cloud.google.com/bigquery/docs/row-level-security-intro?hl=zh-tw)控管資料存取權。

物件資料表與使用存取權委派的其他資料表不同，因為存取物件資料表的資料列時，也會授予基礎檔案內容的存取權。使用者無法直接存取物件，但可以產生[經簽署的網址](#signed_urls)，查看檔案內容。舉例來說，如果使用者有權存取代表 `flower.jpg` 圖片檔案的物件資料表列，就能產生經簽署的網址來顯示該檔案，並查看檔案內容為雛菊圖片。

在物件資料表上設定資料列層級存取政策，可限制使用者或群組存取所選資料列中的物件中繼資料，以及這些資料列代表的物件。舉例來說，下列陳述式只會授予使用者 Alice 存取權，讓她存取 2022 年 6 月 25 日前建立的物件所代表的資料列：

```
CREATE ROW ACCESS POLICY before_20220625
ON my_dataset.my_object_table
GRANT TO ("user:alice@example.com")
FILTER USING (updated < TIMESTAMP("2022-06-25"));
```

有了這項資料列層級存取權政策，Alice 會遇到下列情況：

* 執行 `SELECT * FROM my_dataset.my_object_table;` 查詢只會傳回 2022 年 6 月 25 日前的 `updated` 值。
* 對 `my_dataset.my_object_table` 執行推論只會傳回 2022 年 6 月 25 日前具有 `updated` 值的物件預測結果。
* 為 `my_dataset.my_object_table` 產生已簽署的網址，只會為 2022 年 6 月 25 日前具有 `updated` 值的物件建立網址。

您也可以使用自訂中繼資料，限制物件資料表列的存取權。
舉例來說，下列陳述式會限制 `users` 群組，只能存取已標記為不含任何個人識別資訊的資料列：

```
CREATE ROW ACCESS POLICY no_pii
ON my_dataset.my_object_table
GRANT TO ("group:users@example.com")
FILTER USING (ARRAY_LENGTH(metadata)=1
AND metadata[OFFSET(0)].name="no_pii")
```

## 安全性模型

管理及使用物件資料表時，通常會涉及下列機構角色：

* **資料湖泊管理員**：這類管理員通常會管理 Cloud Storage 值區和物件的身分與存取權管理 (IAM) 政策。
* **資料倉儲管理員**。這類管理員通常會建立、刪除及更新表格。
* **資料分析師**：分析師通常會讀取資料及執行查詢。

資料湖泊管理員負責建立連線，並與資料倉儲管理員共用連線。資料倉儲管理員則會建立資料表、設定適當的存取權控管機制，並與資料分析師共用資料表。

**注意：**資料分析師**不應**具備下列權限：

* 直接從 Cloud Storage 讀取物件 (請參閱[儲存空間物件檢視者 IAM 角色](https://docs.cloud.google.com/storage/docs/access-control/iam-roles?hl=zh-tw))，讓資料分析師規避資料倉儲管理員設定的存取控管。
* 將資料表繫結至連線 (例如 BigQuery 連線管理員)。

  否則，資料分析師可以建立沒有任何存取權控管的新資料表，藉此規避資料倉儲管理員設定的控管機制。

## 支援的物件檔案

您可以針對任何類型和大小的非結構化資料檔案建立物件資料表，也可以建立遠端函式來處理任何類型的非結構化資料。不過，如要使用 BigQuery ML 執行推論作業，物件資料表只能包含符合大小和類型規定的圖片檔案。詳情請參閱「[限制](https://docs.cloud.google.com/bigquery/docs/object-table-inference?hl=zh-tw#limitations)」一節。

## 中繼資料快取功能可提升效能

您可以使用快取中繼資料，提升物件資料表的推論和其他類型分析的效能。如果物件資料表參照大量物件，中繼資料快取功能就特別實用。BigQuery 使用 CMETA 做為分散式中繼資料系統，有效處理大型資料表。CMETA 提供資料欄和區塊層級的精細中繼資料，可透過系統資料表存取。這個系統會最佳化資料存取和處理程序，進而提升查詢效能。為進一步提升大型資料表的查詢效能，BigQuery 會維護中繼資料快取。CMETA 重新整理作業會讓這個快取保持在最新狀態。

中繼資料包括檔案名稱、分區資訊，以及來自檔案的實體中繼資料，例如列數。你可以選擇是否在資料表上啟用中繼資料快取功能。如果查詢的檔案數量龐大，且包含 Apache Hive 分區篩選器，中繼資料快取功能就能發揮最大效益。

如果未啟用中繼資料快取，查詢資料表時必須讀取外部資料來源，才能取得物件中繼資料。讀取這項資料會增加查詢延遲時間；從外部資料來源列出數百萬個檔案可能需要幾分鐘。啟用中繼資料快取功能後，查詢作業就能避免列出外部資料來源中的檔案，並更快地分割及修剪檔案。

中繼資料快取也會與 Cloud Storage 物件版本管理功能整合。快取填入或重新整理時，會根據當時 Cloud Storage 物件的即時版本擷取中繼資料。因此，即使 Cloud Storage 中有較新的使用中版本，啟用中繼資料快取的查詢作業仍會讀取與特定快取物件版本相應的資料。如要存取 Cloud Storage 中任何後續更新的物件版本資料，必須重新整理中繼資料快取。

有兩個屬性可控制這項功能：

* **最大過時程度**：指定查詢何時使用快取中繼資料。
* 「中繼資料快取模式」會指定中繼資料的收集方式。

啟用中繼資料快取功能後，您可以指定可接受的資料表作業中繼資料過時間隔上限。舉例來說，如果指定間隔為 1 小時，只要資料表的中繼資料在過去 1 小時內重新整理過，針對該資料表執行的作業就會使用快取中繼資料。如果快取中繼資料的建立時間早於此時間，作業會改為從 Cloud Storage 擷取中繼資料。過時間隔可指定的範圍為 30 分鐘至 7 天。

為 BigLake 或物件資料表啟用中繼資料快取時，BigQuery 會觸發中繼資料產生重新整理工作。你可以選擇自動或手動重新整理快取：

* 如果是自動重新整理，系統會以定義的間隔重新整理快取，通常是 30 到 60 分鐘。如果 Cloud Storage 中的檔案是以隨機間隔新增、刪除或修改，自動重新整理快取就是不錯的做法。如要控管重新整理時間，例如在擷取、轉換及載入作業結束時觸發重新整理，請使用手動重新整理。
* 如要手動重新整理，請執行 [`BQ.REFRESH_EXTERNAL_METADATA_CACHE` 系統程序](https://docs.cloud.google.com/bigquery/docs/reference/system-procedures?hl=zh-tw#bqrefresh_external_metadata_cache)，按照符合您需求的排程重新整理中繼資料快取。如果 Cloud Storage 中的檔案是以已知間隔新增、刪除或修改 (例如管道的輸出內容)，手動重新整理快取就是不錯的做法。

  如果您同時發出多個手動重新整理要求，只有一個會成功。

如果未重新整理，中繼資料快取會在 7 天後過期。

手動和自動重新整理快取時，都會以 [`INTERACTIVE`](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw) 查詢優先順序執行。

### 使用 `BACKGROUND` 預留項目

如果選擇使用自動重新整理功能，建議您建立[預訂](https://docs.cloud.google.com/bigquery/docs/reservations-intro?hl=zh-tw)，然後為執行中繼資料快取重新整理工作的專案，建立[工作類型為 `BACKGROUND` 的指派](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#assignments)。使用`BACKGROUND`預留項目時，重新整理作業會使用專屬資源集區，避免與使用者查詢競爭，並防止作業因資源不足而可能失敗。

使用共用運算單元集區不會產生額外費用，但改用`BACKGROUND`預留資源可分配專屬資源集區，提供更穩定的效能，並提升 BigQuery 中的重新整理作業可靠性及整體查詢效率。

設定陳舊間隔和中繼資料快取模式值之前，請先考量這些值之間的互動方式。請見以下範例：

* 如果您要手動重新整理資料表的中繼資料快取，並將過時間隔設為 2 天，則必須每 2 天或更短的時間執行 `BQ.REFRESH_EXTERNAL_METADATA_CACHE` 系統程序，才能讓針對資料表執行的作業使用快取中繼資料。
* 如果您自動重新整理資料表的 Metadata 快取，並將過時間隔設為 30 分鐘，則如果 Metadata 快取重新整理作業耗時較長 (通常為 30 到 60 分鐘)，您對資料表執行的部分作業可能會從 Cloud Storage 讀取資料。

如要查詢中繼資料重新整理作業的相關資訊，請查詢 [`INFORMATION_SCHEMA.JOBS` 檢視區塊](https://docs.cloud.google.com/bigquery/docs/information-schema-jobs?hl=zh-tw)，如下列範例所示：

```
SELECT *
FROM `region-us.INFORMATION_SCHEMA.JOBS_BY_PROJECT`
WHERE job_id LIKE '%metadata_cache_refresh%'
AND creation_time > TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 6 HOUR)
ORDER BY start_time DESC
LIMIT 10;
```

詳情請參閱「[中繼資料快取](https://docs.cloud.google.com/bigquery/docs/metadata-caching?hl=zh-tw)」。

如要進一步瞭解如何設定中繼資料快取選項，請參閱「[建立物件資料表](https://docs.cloud.google.com/bigquery/docs/object-tables?hl=zh-tw#create-object-table)」。

## 限制

* 物件資料表是唯讀資料表，因為這類資料表會對應至 Cloud Storage 中的非結構化資料物件。您無法變更物件資料表或修改物件資料表資料。
* 舊版 SQL 或其他雲端環境 (例如 Amazon Web Services (AWS) 和 Microsoft Azure) 不支援物件資料表。
* 如要使用 BigQuery ML 執行推論作業，您使用的模型和物件資料表必須符合「[限制](https://docs.cloud.google.com/bigquery/docs/object-table-inference?hl=zh-tw#limitations)」一節所述的規定。
* 如果查詢包含物件資料表，則無法存取超過 10 GB 的物件中繼資料。舉例來說，如果查詢透過簽署的 URL 從物件資料表和物件資料中的中繼資料欄存取 100 TB，則這 100 TB 中只有 10 GB 可能來自中繼資料欄。
* 物件資料表與所有其他 BigQuery 外部資料表一樣，都受到相同限制。詳情請參閱「[配額](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#external_tables)」。
* 物件資料表的查詢與所有其他 BigQuery 查詢一樣，都受到相同限制。詳情請參閱「[配額](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#query_jobs)」。
* 處理物件資料表非結構化資料的遠端函式，與所有其他遠端函式一樣，都受到相同的[限制](https://docs.cloud.google.com/bigquery/docs/remote-functions?hl=zh-tw#limitations)。
* 為物件資料表中的物件產生的已簽署網址會在 6 小時後過期，這是[查詢執行時間限制](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#query_jobs)。
* 以量計價或 Standard 版不支援使用 BigQuery ML 進行推論。
* 下列函式不支援隨選價格或標準版：

  + [`ML.CONVERT_COLOR_SPACE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-convert-color-space?hl=zh-tw)
  + [`ML.CONVERT_IMAGE_TYPE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-convert-image-type?hl=zh-tw)
  + [`ML.RESIZE_IMAGE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-resize-image?hl=zh-tw)
* 物件表格最多可有 3 億列。
* 系統不支援合併空物件資料表和非空物件資料表的 `UNION ALL` 作業，且可能會傳回錯誤。

## 費用

物件資料表的下列方面會產生費用：

* 查詢資料表。
* [重新整理中繼資料快取](#metadata_caching_for_performance)。

如果您有[運算單元預留](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw)，查詢外部資料表時不會產生費用。而是會耗用這些查詢的配額。

下表說明定價模式如何影響這些費用的適用方式：

|  | **以量計價** | **Standard、Enterprise 和 Enterprise Plus 版本** |
| --- | --- | --- |
| 查詢 | 系統會[根據使用者查詢處理的位元組數](https://cloud.google.com/bigquery/pricing?hl=zh-tw#on_demand_pricing)向您收費。 | 查詢期間會耗用[保留項目指派中的[運算單元](https://cloud.google.com/bigquery/pricing?hl=zh-tw#capacity_compute_analysis_pricing)，且`QUERY`工作類型](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#assignments)為查詢。 |
| 手動重新整理中繼資料快取。 | 系統會[針對重新整理快取所處理的位元組向您收費](https://cloud.google.com/bigquery/pricing?hl=zh-tw#on_demand_pricing)。 | 在快取重新整理期間，會耗用[保留項目指派中的[運算單元](https://cloud.google.com/bigquery/pricing?hl=zh-tw#capacity_compute_analysis_pricing)，`QUERY`工作類型](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#assignments)為： |
| 自動重新整理中繼資料快取。 | 系統會[針對重新整理快取所處理的位元組向您收費](https://cloud.google.com/bigquery/pricing?hl=zh-tw#on_demand_pricing)。 | 在快取重新整理期間，會耗用[保留項目指派中的[運算單元](https://cloud.google.com/bigquery/pricing?hl=zh-tw#capacity_compute_analysis_pricing)，`BACKGROUND`工作類型](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#assignments)為：    如果沒有可用的 `BACKGROUND` 預留項目來重新整理中繼資料快取，且您使用的是 Enterprise 或 Enterprise Plus 版本，BigQuery 會自動改用 `QUERY` 預留項目中的運算單元。 |

系統也會依據各產品的價格規定，針對 [Cloud Storage](https://cloud.google.com/storage/pricing?hl=zh-tw)、[Amazon S3](https://aws.amazon.com/s3/pricing/) 和 [Azure Blob Storage](https://azure.microsoft.com/pricing/details/storage/blobs/) 的儲存空間和資料存取權向您收費。

BigQuery 與 Cloud Storage 互動時，可能會產生下列 Cloud Storage 費用：

* 儲存資料的資料儲存費用。
* 存取 [Nearline](https://docs.cloud.google.com/storage/docs/storage-classes?hl=zh-tw#nearline)、[Coldline](https://docs.cloud.google.com/storage/docs/storage-classes?hl=zh-tw#coldline) 和 [Archive](https://docs.cloud.google.com/storage/docs/storage-classes?hl=zh-tw#archive) 儲存空間級別中的資料時，會產生資料擷取費用。對這些儲存空間類別查詢資料表或重新整理中繼資料快取時，請務必謹慎操作，因為費用可能相當高昂。
* 讀取不同區域的資料時，會產生網路用量費用，例如 BigQuery 資料集和 Cloud Storage bucket 位於不同區域時。
* 資料處理費用。不過，如果是 BigQuery 代表您發出的 API 呼叫 (例如列出或取得資源)，則不會收取費用。

## 透過 BigQuery sharing 功能使用物件資料表

物件資料表與 BigQuery sharing (舊稱 Analytics Hub) 相容。
含有物件資料表的資料集可以發布為[共用項目](https://docs.cloud.google.com/bigquery/docs/analytics-hub-introduction?hl=zh-tw#listings)。共用訂閱者可以訂閱這些資訊，在專案中佈建唯讀資料集 (稱為[*連結資料集*](https://docs.cloud.google.com/bigquery/docs/analytics-hub-introduction?hl=zh-tw#linked_datasets))。訂閱者可以查詢連結資料集中的所有資料表，包括所有物件資料表。詳情請參閱「[訂閱房源](https://docs.cloud.google.com/bigquery/docs/analytics-hub-view-subscribe-listings?hl=zh-tw#subscribe-listings)」。

## 後續步驟

* 瞭解如何[建立物件資料表](https://docs.cloud.google.com/bigquery/docs/object-tables?hl=zh-tw)。
* 瞭解如何[使用物件表格，在標準表格中維護 `ObjectRef` 資料欄](https://docs.cloud.google.com/bigquery/docs/objectref-columns?hl=zh-tw)。
* 瞭解如何[對圖片物件資料表執行推論](https://docs.cloud.google.com/bigquery/docs/object-table-inference?hl=zh-tw)。
* 瞭解如何[使用遠端函式分析物件資料表](https://docs.cloud.google.com/bigquery/docs/object-table-remote-function?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-14 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-14 (世界標準時間)。"],[],[]]