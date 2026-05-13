Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 執行語意搜尋和檢索增強生成

本教學課程將逐步說明如何建立及使用[文字嵌入項目](https://docs.cloud.google.com/bigquery/docs/generative-ai-overview?hl=zh-tw#text_embedding)，進行語意搜尋和[檢索增強生成 (RAG)](https://cloud.google.com/use-cases/retrieval-augmented-generation?hl=zh-tw)。

本教學課程涵蓋下列工作：

* 透過 Vertex AI 嵌入模型建立 BigQuery ML [遠端模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model?hl=zh-tw)。
* 使用 [`AI.GENERATE_EMBEDDING` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-ai-generate-embedding?hl=zh-tw)搭配遠端模型，從 BigQuery 資料表中的文字生成嵌入。
* 建立[向量索引](https://docs.cloud.google.com/bigquery/docs/vector-index?hl=zh-tw)，為嵌入建立索引，以提升搜尋效能。
* 使用 [`VECTOR_SEARCH` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/search_functions?hl=zh-tw#vector_search)搭配嵌入項目，搜尋相似文字。
* 使用 [`AI.GENERATE_TEXT` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-ai-generate-text?hl=zh-tw)生成文字，並運用向量搜尋結果擴增提示輸入內容，藉此執行 RAG，提升結果品質。

本教學課程使用 BigQuery 公開資料表 `patents-public-data.google_patents_research.publications`。

## 必要的角色

如要執行本教學課程，您需要下列 Identity and Access Management (IAM) 角色：

* 建立及使用 BigQuery 資料集、連線和模型：BigQuery 管理員 (`roles/bigquery.admin`)。
* 將權限授予連線的服務帳戶：專案 IAM 管理員 (`roles/resourcemanager.projectIamAdmin`)。

這些預先定義的角色具備執行本文所述工作所需的權限。如要查看確切的必要權限，請展開「Required permissions」(必要權限) 部分：

#### 所需權限

* 建立資料集：`bigquery.datasets.create`
* 建立、委派及使用連線：
  `bigquery.connections.*`
* 設定預設連線：`bigquery.config.*`
* 設定服務帳戶權限：
  `resourcemanager.projects.getIamPolicy` 和
  `resourcemanager.projects.setIamPolicy`
* 建立模型並執行推論：
  + `bigquery.jobs.create`
  + `bigquery.models.create`
  + `bigquery.models.getData`
  + `bigquery.models.updateData`
  + `bigquery.models.updateMetadata`

您或許還可透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)取得這些權限。

## 費用

在本文件中，您會使用下列 Google Cloud的計費元件：

* **BigQuery ML**: You incur costs for the data that you
  process in BigQuery.
* **Vertex AI**: You incur costs for calls to the
  Vertex AI service that's represented by the remote model.

如要根據預測用量估算費用，請使用 [Pricing Calculator](https://docs.cloud.google.com/products/calculator?hl=zh-tw)。

初次使用 Google Cloud 的使用者可能符合[免費試用期](https://docs.cloud.google.com/free?hl=zh-tw)資格。

如要進一步瞭解 BigQuery 定價，請參閱 BigQuery 說明文件中的「[BigQuery 定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw)」一文。

如要進一步瞭解 Vertex AI 定價，請參閱 [Vertex AI 定價](https://cloud.google.com/vertex-ai/pricing?hl=zh-tw#generative_ai_models)頁面。

## 事前準備

1. 在 Google Cloud 控制台的專案選擇器頁面中，選取或建立 Google Cloud 專案。

   **選取或建立專案所需的角色**

   * **選取專案**：選取專案時，不需要具備特定 IAM 角色，只要您已獲授角色，即可選取任何專案。
   * **建立專案**：如要建立專案，您需要「專案建立者」角色 (`roles/resourcemanager.projectCreator`)，其中包含 `resourcemanager.projects.create` 權限。[瞭解如何授予角色](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)。
   **注意**：如果您不打算保留在這項程序中建立的資源，請建立新專案，而不要選取現有專案。完成這些步驟後，您就可以刪除專案，並移除與該專案相關聯的所有資源。

   [前往專案選取器](https://console.cloud.google.com/projectselector2/home/dashboard?hl=zh-tw)
2. [確認專案已啟用計費功能 Google Cloud](https://docs.cloud.google.com/billing/docs/how-to/verify-billing-enabled?hl=zh-tw#confirm_billing_is_enabled_on_a_project) 。
3. 啟用 BigQuery、BigQuery Connection 和 Vertex AI API。

   **啟用 API 時所需的角色**

   如要啟用 API，您需要服務使用情形管理員 IAM 角色 (`roles/serviceusage.serviceUsageAdmin`)，其中包含 `serviceusage.services.enable` 權限。[瞭解如何授予角色](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)。

   [啟用 API](https://console.cloud.google.com/flows/enableapi?apiid=bigquery.googleapis.com%2Cbigqueryconnection.googleapis.com%2Caiplatform.googleapis.com&hl=zh-tw)

## 建立資料集

建立 BigQuery 資料集來儲存機器學習模型。

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往 BigQuery 頁面](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在「Explorer」窗格中，按一下專案名稱。
3. 依序點按 more\_vert「View actions」(查看動作) >「Create dataset」(建立資料集)
4. 在「建立資料集」頁面中，執行下列操作：

   * 在「Dataset ID」(資料集 ID) 中輸入 `bqml_tutorial`。
   * 針對「位置類型」選取「多區域」，然後選取「美國」。
   * 其餘設定請保留預設狀態，然後按一下「建立資料集」。

### bq

如要建立新的資料集，請使用 [`bq mk --dataset` 指令](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#mk-dataset)。

1. 建立名為 `bqml_tutorial` 的資料集，並將資料位置設為 `US`。

   ```
   bq mk --dataset \
     --location=US \
     --description "BigQuery ML tutorial dataset." \
     bqml_tutorial
   ```
2. 確認資料集已建立完成：

   ```
   bq ls
   ```

### API

請呼叫 [`datasets.insert`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/datasets/insert?hl=zh-tw) 方法，搭配已定義的[資料集資源](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/datasets?hl=zh-tw)。

```
{
  "datasetReference": {
     "datasetId": "bqml_tutorial"
  }
}
```

## 建立用於生成文字嵌入的遠端模型

建立遠端模型，代表代管的 Vertex AI 文字嵌入生成模型：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中執行下列陳述式：

   ```
   CREATE OR REPLACE MODEL `bqml_tutorial.embedding_model`
     REMOTE WITH CONNECTION DEFAULT
     OPTIONS (ENDPOINT = 'text-embedding-005');
   ```

   查詢會在幾秒內完成，之後即可透過「Explorer」窗格存取模型
   `embedding_model`。由於查詢是使用 `CREATE MODEL` 陳述式建立模型，因此不會有查詢結果。

## 生成文字嵌入

使用 [`AI.GENERATE_EMBEDDING` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-ai-generate-embedding?hl=zh-tw)從專利摘要產生文字嵌入，然後寫入 BigQuery 資料表，以便搜尋。

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中執行下列陳述式：

   ```
   CREATE OR REPLACE TABLE `bqml_tutorial.embeddings` AS
   SELECT * FROM AI.GENERATE_EMBEDDING(
     MODEL `bqml_tutorial.embedding_model`,
     (
       SELECT *, abstract AS content
       FROM `patents-public-data.google_patents_research.publications`
       WHERE LENGTH(abstract) > 0 AND LENGTH(title) > 0 AND country = 'Singapore'
     )
   )
   WHERE LENGTH(status) = 0;
   ```

這項查詢大約需要 5 分鐘才能完成。

使用 [`AI.GENERATE_EMBEDDING` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-ai-generate-embedding?hl=zh-tw)產生嵌入可能會失敗，原因在於 Vertex AI LLM [配額](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#cloud_ai_service_functions)或服務無法使用。錯誤詳細資料會傳回至 `status` 欄。如果資料欄為空白，表示已成功產生嵌入內容。`status`

如要瞭解 BigQuery 中其他產生文字嵌入的方法，請參閱[使用預先訓練的 TensorFlow 模型嵌入文字教學課程](https://docs.cloud.google.com/bigquery/docs/generate-embedding-with-tensorflow-models?hl=zh-tw)。

## 建立向量索引

如果您在嵌入欄中建立向量索引，對該欄執行的向量搜尋會使用[近似最鄰近項目](https://en.wikipedia.org/wiki/Nearest_neighbor_search#Approximation_methods)搜尋技術。這項技術可提升向量搜尋效能，但會降低[召回率](https://developers.google.com/machine-learning/crash-course/classification/precision-and-recall?hl=zh-tw#recallsearch_term_rules)，因此傳回的結果會更近似。

如要建立向量索引，請使用[`CREATE VECTOR INDEX`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#create_vector_index_statement)資料定義語言 (DDL) 陳述式：

1. 前往「BigQuery」頁面

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中，執行下列 SQL 陳述式：

   ```
   CREATE OR REPLACE VECTOR INDEX my_index
   ON `bqml_tutorial.embeddings`(embedding)
   OPTIONS(index_type = 'IVF',
     distance_type = 'COSINE',
     ivf_options = '{"num_lists":500}')
   ```

建立向量索引通常只需要幾秒鐘。向量索引需要再 2 到 3 分鐘才能填入資料並供您使用。

### 確認向量索引是否準備就緒

系統會以非同步方式填入向量索引。您可以查詢 [`INFORMATION_SCHEMA.VECTOR_INDEXES` 檢視區塊](https://docs.cloud.google.com/bigquery/docs/information-schema-vector-indexes?hl=zh-tw)，並確認 `coverage_percentage` 欄值大於 `0`，且 `last_refresh_time` 欄值不是 `NULL`，藉此檢查索引是否已可供使用。

1. 前往「BigQuery」頁面

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中，執行下列 SQL 陳述式：

   ```
   SELECT table_name, index_name, index_status,
   coverage_percentage, last_refresh_time, disable_reason
   FROM `PROJECT_ID.bqml_tutorial.INFORMATION_SCHEMA.VECTOR_INDEXES`
   ```

   將 `PROJECT_ID` 替換為專案 ID。

## 使用向量索引執行文字相似度搜尋

使用 [`VECTOR_SEARCH` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/search_functions?hl=zh-tw#vector_search)，搜尋與文字查詢產生的嵌入項目相符的相關專利。

`top_k` 引數會決定要傳回的相符項目數量，在本例中為五個。`fraction_lists_to_search` 選項會決定要搜尋的向量索引清單百分比。[您建立的向量索引](#create_a_vector_index)有 500 個清單，因此 `.01` 的 `fraction_lists_to_search` 值表示這項向量搜尋會掃描其中五個清單。如這裡所示，`fraction_lists_to_search` 值越低，[召回率](https://developers.google.com/machine-learning/crash-course/classification/accuracy-precision-recall?hl=zh-tw#recall)就越低，但效能會越快。如要進一步瞭解向量索引清單，請參閱`num_lists`
[向量索引選項](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#vector_index_option_list)。

您必須使用與要比較資料表相同的模型，才能產生這項查詢中的嵌入，否則搜尋結果不會準確。

1. 前往「BigQuery」頁面

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中，執行下列 SQL 陳述式：

   ```
   SELECT query.query, base.publication_number, base.title, base.abstract
   FROM VECTOR_SEARCH(
     TABLE `bqml_tutorial.embeddings`, 'embedding',
     (
     SELECT embedding, content AS query
     FROM AI.GENERATE_EMBEDDING(
     MODEL `bqml_tutorial.embedding_model`,
     (SELECT 'improving password security' AS content))
     ),
     top_k => 5, options => '{"fraction_lists_to_search": 0.01}')
   ```

   輸出結果會與下列內容相似：

   ```
   +-----------------------------+--------------------+-------------------------------------------------+-------------------------------------------------+
   |            query            | publication_number |                       title                     |                      abstract                   |
   +-----------------------------+--------------------+-------------------------------------------------+-------------------------------------------------+
   | improving password security | SG-120868-A1       | Data storage device security method and a...    | Methods for improving security in data stora... |
   | improving password security | SG-10201610585W-A  | Passsword management system and process...      | PASSSWORD MANAGEMENT SYSTEM AND PROCESS ...     |
   | improving password security | SG-148888-A1       | Improved system and method for...               | IMPROVED SYSTEM AND METHOD FOR RANDOM...        |
   | improving password security | SG-194267-A1       | Method and system for protecting a password...  | A system for providing security for a...        |
   | improving password security | SG-120868-A1       | Data storage device security...                 | Methods for improving security in data...       |
   +-----------------------------+--------------------+-------------------------------------------------+-------------------------------------------------+
   ```

## 建立文字生成遠端模型

建立遠端模型，代表代管的 Vertex AI 文字生成模型：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中執行下列陳述式：

   ```
   CREATE OR REPLACE MODEL `bqml_tutorial.text_model`
     REMOTE WITH CONNECTION DEFAULT
     OPTIONS (ENDPOINT = 'gemini-2.0-flash-001');
   ```

   查詢會在幾秒內完成，之後即可透過「Explorer」窗格存取模型
   `text_model`。由於查詢是使用 `CREATE MODEL` 陳述式建立模型，因此不會有查詢結果。

## 根據向量搜尋結果生成文字

將搜尋結果做為提示，使用 [`AI.GENERATE_TEXT` 函式生成文字](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-ai-generate-text?hl=zh-tw)

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中執行下列陳述式：

   ```
   SELECT result AS generated, prompt
   FROM AI.GENERATE_TEXT(
     MODEL `bqml_tutorial.text_model`,
     (
       SELECT CONCAT(
         'Propose some project ideas to improve user password security using the context below: ',
         STRING_AGG(
           FORMAT("patent title: %s, patent abstract: %s", base.title, base.abstract),
           ',\n')
         ) AS prompt,
       FROM VECTOR_SEARCH(
         TABLE `bqml_tutorial.embeddings`, 'embedding',
         (
           SELECT embedding, content AS query
           FROM AI.GENERATE_EMBEDDING(
             MODEL `bqml_tutorial.embedding_model`,
            (SELECT 'improving password security' AS content)
           )
         ),
       top_k => 5, options => '{"fraction_lists_to_search": 0.01}')
     ),
     STRUCT(600 AS max_output_tokens));
   ```

   輸出結果會與下列內容相似：

   ```
   +------------------------------------------------+------------------------------------------------------------+
   |            generated                           | prompt                                                     |
   +------------------------------------------------+------------------------------------------------------------+
   | These patents suggest several project ideas to | Propose some project ideas to improve user password        |
   | improve user password security.  Here are      | security using the context below: patent title: Active     |
   | some, categorized by the patent they build     | new password entry dialog with compact visual indication   |
   | upon:                                          | of adherence to password policy, patent abstract:          |
   |                                                | An active new password entry dialog provides a compact     |
   | **I. Projects based on "Active new password    | visual indication of adherence to password policies. A     |
   | entry dialog with compact visual indication of | visual indication of progress towards meeting all          |
   | adherence to password policy":**               | applicable password policies is included in the display    |
   |                                                | and updated as new password characters are being...        |
   +------------------------------------------------+------------------------------------------------------------+
   ```

## 清除所用資源

**注意**：刪除專案會造成以下結果：

* **專案中的所有內容都會遭到刪除。**如果使用現有專案來進行本文中的任務，刪除專案將一併移除當中已完成的其他任務'。
* **自訂專案 ID 會消失。**當您之前建立這個專案時，可能建立了想要在日後使用的自訂專案 ID。如要保留使用該專案 ID 的網址 (例如 `appspot.com` 網址)，請刪除在該專案中選取的資源，而不是刪除整個專案。

如果打算探索多種架構、教學課程或快速入門導覽課程，重複使用專案可避免超出專案配額限制。

1. 前往 Google Cloud 控制台的「Manage resources」(管理資源) 頁面。

   [前往「Manage resources」(管理資源)](https://console.cloud.google.com/iam-admin/projects?hl=zh-tw)
2. 在專案清單中選取要刪除的專案，然後點選「Delete」(刪除)。
3. 在對話方塊中輸入專案 ID，然後按一下 [Shut down] (關閉) 以刪除專案。

## 後續步驟

* 請試用「[在檢索增強生成管道中剖析 PDF](https://docs.cloud.google.com/bigquery/docs/rag-pipeline-pdf?hl=zh-tw)」教學課程，瞭解如何根據剖析的 PDF 內容建立 RAG 管道。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-12 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-12 (世界標準時間)。"],[],[]]