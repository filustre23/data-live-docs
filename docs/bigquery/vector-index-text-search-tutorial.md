Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見

# 執行語意搜尋和檢索增強生成 透過集合功能整理內容 你可以依據偏好儲存及分類內容。

在本教學課程中，您將使用[遠端模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model?hl=zh-tw)和 [`AI.GENERATE_EMBEDDING` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-ai-generate-embedding?hl=zh-tw)，在 BigQuery 資料表中生成[文字嵌入](https://docs.cloud.google.com/bigquery/docs/generative-ai-overview?hl=zh-tw#text_embedding)。接著，您會建立[向量索引](https://docs.cloud.google.com/bigquery/docs/vector-index?hl=zh-tw)，為嵌入建立索引，以提升搜尋效能。

您可以使用 [`VECTOR_SEARCH` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/search_functions?hl=zh-tw#vector_search)和嵌入，搜尋相似文字。向量搜尋是一種技術，可使用嵌入項目比較相似的物件。嵌入項目是高維度數值向量，代表特定實體，例如一段文字。

最後，您會使用 [`AI.GENERATE_TEXT` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-ai-generate-text?hl=zh-tw)生成文字，執行[檢索增強生成 (RAG)](https://cloud.google.com/use-cases/retrieval-augmented-generation?hl=zh-tw)。RAG 是一種 AI 框架，結合資訊檢索系統 (如搜尋和資料庫) 的優勢，以及生成式大型語言模型 (LLM) 的功能。如果將您的資料和世界知識與 LLM 語言技術加以結合，根據基準生成的內容就會更為準確、符合現況，也更切合您的特定需求。

本教學課程使用 [Google 專利 Research 公開資料集](https://console.cloud.google.com/bigquery?p=patents-public-data&%3Bd=google_patents_research&%3Bpage=dataset&%3Bws=%211m5%211m4%213m2%211spatents-public-data%212sgoogle_patents_research%2123sLEGACY_URL_PARAM&hl=zh-tw)的資料。

## 目標

* 透過 Gemini Enterprise Agent Platform 嵌入模型建立 BigQuery ML 遠端模型。
* 使用 `AI.GENERATE_EMBEDDING` 函式搭配遠端模型，從 BigQuery 資料表中的文字生成嵌入。
* 建立向量索引，為嵌入建立索引，以提升搜尋效能。
* 使用 `VECTOR_SEARCH` 函式和嵌入項目搜尋類似文字。
* 使用 `AI.GENERATE_TEXT` 函式生成文字，並運用向量搜尋結果擴增提示輸入內容，藉此執行 RAG，提升結果品質。

## 費用

在本文件中，您會使用下列 Google Cloud的計費元件：

* **BigQuery ML**: You incur costs for the data that you
  process in BigQuery.
* **Gemini Enterprise Agent Platform**: You incur costs for
  calls to the Agent Platform service that's
  represented by the remote model.

如要根據預測用量估算費用，請使用 [Pricing Calculator](https://docs.cloud.google.com/products/calculator?hl=zh-tw)。

初次使用 Google Cloud 的使用者可能符合[免費試用期](https://docs.cloud.google.com/free?hl=zh-tw)資格。

詳情請參閱下列定價頁面：

* [BigQuery 定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw)
* [Agent Platform 定價](https://cloud.google.com/vertex-ai/pricing?hl=zh-tw#generative_ai_models)

## 事前準備

1. 在 Google Cloud 控制台的專案選擇器頁面中，選取或建立 Google Cloud 專案。

   **選取或建立專案所需的角色**

   * **選取專案**：選取專案時，不需要具備特定 IAM 角色，只要您在專案中獲派角色，即可選取該專案。
   * **建立專案**：如要建立專案，您需要「專案建立者」角色 (`roles/resourcemanager.projectCreator`)，其中包含 `resourcemanager.projects.create` 權限。[瞭解如何授予角色](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)。
   **注意**：如果您不打算保留在這項程序中建立的資源，請建立新專案，而不要選取現有專案。完成這些步驟後，您就可以刪除專案，並移除與該專案相關聯的所有資源。

   [前往專案選取器](https://console.cloud.google.com/projectselector2/home/dashboard?hl=zh-tw)
2. [確認專案已啟用計費功能 Google Cloud](https://docs.cloud.google.com/billing/docs/how-to/verify-billing-enabled?hl=zh-tw#confirm_billing_is_enabled_on_a_project) 。
3. 啟用 BigQuery、Cloud Storage 和 Gemini Enterprise Agent Platform API (如果尚未啟用)。

   **啟用 API 時所需的角色**

   如要啟用 API，您必須具備 `serviceusage.services.enable` 權限。如果您建立了專案，可能已透過「擁有者」角色 (`roles/owner`) 取得這項權限。否則，您可以透過「服務使用情形管理員」角色 (`roles/serviceusage.serviceUsageAdmin`) 取得這項權限。[瞭解如何授予角色](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)。

   [啟用 API](https://console.cloud.google.com/apis/enableflow?apiid=bigquery.googleapis.com%2Cstorage.googleapis.com%2Caiplatform.googleapis.com&hl=zh-tw)

### 必要的角色

如要取得完成本教學課程所需的權限，請要求管理員授予您下列 IAM 角色：

* 建立資料集、資料表和模型：
  [BigQuery 資料擁有者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.dataOwner)  (`roles/bigquery.dataOwner`)
* 執行 BigQuery 工作：
  [BigQuery 工作使用者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.jobUser)  (`roles/bigquery.jobUser`)
* 建立及管理連線：
  [BigQuery 連線管理員](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.connectionAdmin)  (`roles/bigquery.connectionAdmin`)

如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

您或許也能透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)，取得必要權限。

## 建立資料集

如要建立 BigQuery 資料集，請選取下列任一選項：

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。

   如果沒有看到左側窗格，請按一下 last\_page「Expand left pane」(展開左側窗格)，開啟窗格。
3. 在「Explorer」中展開專案，然後按一下「Datasets」。
4. 在「資料集」頁面，按一下 add「建立資料集」。
5. 在「建立資料集」窗格中，執行下列操作：

   * 在「Dataset ID」(資料集 ID) 中輸入 `bqml_tutorial`。
   * 選取「資料位置」的「美國」。

   其餘預設設定均保留原樣。
6. 點選「建立資料集」。

### bq

如要建立新的資料集，請使用 [`bq mk --dataset` 指令](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#mk-dataset)。

1. 建立名為 `bqml_tutorial` 的資料集，並將資料位置設為 `US`：

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

使用已定義的[資料集資源](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/datasets?hl=zh-tw)呼叫 [`datasets.insert`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/datasets/insert?hl=zh-tw) 方法：

```
{
  "datasetReference": {
     "datasetId": "bqml_tutorial"
  }
}
```

## 建立用於生成文字嵌入的遠端模型

在本節中，您會建立遠端模型，代表代管的 Agent Platform 文字嵌入生成模型。建立模型時，您可以使用 [`DEFAULT` 連線](https://docs.cloud.google.com/bigquery/docs/default-connections?hl=zh-tw)呼叫 [Text embeddings API](https://docs.cloud.google.com/gemini-enterprise-agent-platform/reference/models/text-embeddings-api?hl=zh-tw)，透過 `text-embedding-005` 模型取得文字嵌入。如果您沒有預設連線，`CREATE MODEL` 陳述式會為您建立連線。

如要建立文字嵌入模型，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 如要建立模型，請將這項指令貼到查詢編輯器，然後按一下 play\_circle「執行」：

   ```
   CREATE OR REPLACE MODEL `bqml_tutorial.embedding_model`
     REMOTE WITH CONNECTION DEFAULT
     OPTIONS (ENDPOINT = 'text-embedding-005');
   ```

   查詢會在幾秒內完成，之後即可透過「Explorer」窗格存取模型 `embedding_model`。

   你會收到類似以下的確認訊息：`Successfully created
   model named embedding_model.`

## 生成文字嵌入

使用 [`AI.GENERATE_EMBEDDING` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-ai-generate-embedding?hl=zh-tw)從專利摘要生成文字嵌入，然後將這些嵌入寫入 BigQuery 資料表，以便進行搜尋。

使用 [`AI.GENERATE_EMBEDDING` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-ai-generate-embedding?hl=zh-tw)產生嵌入內容時，可能會因 Agent Platform LLM [配額](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#cloud_ai_service_functions)或服務無法使用而失敗。如果失敗，查詢結果的 `status` 欄會傳回錯誤詳細資料。

如要瞭解 BigQuery 中其他文字嵌入生成方法，請參閱[使用預先訓練的 TensorFlow 模型嵌入文字的教學課程](https://docs.cloud.google.com/bigquery/docs/generate-embedding-with-tensorflow-models?hl=zh-tw)。

如要生成文字嵌入，請將這項指令貼到查詢編輯器，然後按一下 play\_circle「執行」：

```
  CREATE OR REPLACE TABLE bqml_tutorial.embeddings AS
  SELECT * FROM AI.GENERATE_EMBEDDING(
    MODEL bqml_tutorial.embedding_model,
    (
      SELECT *, abstract AS content
      FROM patents-public-data.google_patents_research.publications
      WHERE LENGTH(abstract) > 0 AND LENGTH(title) > 0 AND country = 'Singapore'
    )
  )
  WHERE LENGTH(status) = 0;
```

這項查詢需要幾分鐘才能完成。你會收到類似下方的確認訊息：`This statement created a new table named
embeddings.`

## 建立向量索引

如果您在嵌入欄中建立向量索引，對該欄執行的向量搜尋會使用[近似最鄰近項目](https://en.wikipedia.org/wiki/Nearest_neighbor_search#Approximation_methods)搜尋技術。這項技術可提升向量搜尋效能，並傳回更多近似結果，但[召回率](https://developers.google.com/machine-learning/crash-course/classification/precision-and-recall?hl=zh-tw#recallsearch_term_rules)會降低。

如要建立向量索引，請使用[`CREATE VECTOR INDEX`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#create_vector_index_statement)資料定義語言 (DDL) 陳述式。如要確認索引是否可用，請查詢 [`INFORMATION_SCHEMA.VECTOR_INDEXES` 檢視區塊](https://docs.cloud.google.com/bigquery/docs/information-schema-vector-indexes?hl=zh-tw)，確認 `coverage_percentage` 欄值大於 `0`，且 `last_refresh_time` 欄值不是 `NULL`。

如要建立及驗證向量索引，請按照下列步驟操作：

1. 如要建立向量索引，請將這項指令貼到查詢編輯器，然後按一下「執行」play\_circle：

   ```
   CREATE OR REPLACE VECTOR INDEX my_index
   ON `bqml_tutorial.embeddings`(embedding)
   OPTIONS(index_type = 'IVF',
     distance_type = 'COSINE',
     ivf_options = '{"num_lists":500}');
   ```

   你會收到類似以下的確認訊息：`The vector index
   creation on table bqml_tutorial.embeddings was initiated. Please query
   bqml_tutorial.INFORMATION_SCHEMA.VECTOR_INDEXES to check the progress of the
   index.`

   建立向量索引通常只需要幾秒鐘。向量索引會以非同步方式填入資料，因此需要另外兩到三分鐘。
2. 如要確認索引是否已可供使用，請將下列指令貼到查詢編輯器，然後按一下「執行」play\_circle：

   ```
   SELECT table_name, index_name, index_status,
   coverage_percentage, last_refresh_time, disable_reason
   FROM `PROJECT_ID.bqml_tutorial.INFORMATION_SCHEMA.VECTOR_INDEXES`;
   ```

   將 `PROJECT_ID` 替換為專案 ID。

   執行查詢後，如果結果中的 `index_status` 欄顯示索引為 `ACTIVE`，且 `coverage_percentage` 值為 `100`，則表示索引可用。

## 使用向量索引執行文字相似度搜尋

使用 [`VECTOR_SEARCH` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/search_functions?hl=zh-tw#vector_search)，搜尋與文字查詢產生的嵌入項目相符的相關專利。

`top_k` 引數會決定要傳回的相符項目數量，在本例中為五個。`fraction_lists_to_search` 選項會決定要搜尋的向量索引清單百分比。[您建立的向量索引](#create_a_vector_index)有 500 個清單，因此 `.01` 的 `fraction_lists_to_search` 值表示這項向量搜尋會掃描其中五個清單。如這裡所示，較低的 `fraction_lists_to_search` 值可提供較低的[召回](https://developers.google.com/machine-learning/crash-course/classification/accuracy-precision-recall?hl=zh-tw#recall)率和更快的效能。

如要進一步瞭解向量索引清單，請參閱 `num_lists`「
[向量索引選項](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#vector_index_option_list)」。

您必須使用與要比較資料表相同的模型，才能在這項查詢中生成嵌入，否則搜尋結果不會準確。

如要執行文字相似度搜尋，請將下列指令貼到查詢編輯器，然後點選 play\_circle「執行」：

```
  SELECT query.query, base.publication_number, base.title, base.abstract
  FROM VECTOR_SEARCH(
    TABLE bqml_tutorial.embeddings, 'embedding',
    (
    SELECT embedding, content AS query
    FROM AI.GENERATE_EMBEDDING(
    MODEL bqml_tutorial.embedding_model,
    (SELECT 'improving password security' AS content))
    ),
    top_k => 5, options => '{"fraction_lists_to_search": 0.01}');
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

如要建立遠端模型，代表代管的 Agent Platform 文字生成模型，請將這項指令貼到查詢編輯器，然後按一下「執行」play\_circle：

```
  CREATE OR REPLACE MODEL bqml_tutorial.text_model
    REMOTE WITH CONNECTION DEFAULT
    OPTIONS (ENDPOINT = 'gemini-2.5-flash');
```

你會收到類似以下的確認訊息：
`Successfully created model named text_model.`

## 根據向量搜尋結果生成文字

將搜尋結果做為提示，使用 [`AI.GENERATE_TEXT` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-ai-generate-text?hl=zh-tw)生成文字。

如要擴增向量搜尋結果，請將下列指令貼到查詢編輯器，然後點選 play\_circle「執行」：

```
  SELECT result AS generated, prompt
  FROM AI.GENERATE_TEXT(
    MODEL bqml_tutorial.text_model,
    (
      SELECT CONCAT(
        'Propose some project ideas to improve user password security using the context below: ',
        STRING_AGG(
          FORMAT("patent title: %s, patent abstract: %s", base.title, base.abstract),
          ',\n')
        ) AS prompt,
      FROM VECTOR_SEARCH(
        TABLE bqml_tutorial.embeddings, 'embedding',
        (
          SELECT embedding, content AS query
          FROM AI.GENERATE_EMBEDDING(
            MODEL bqml_tutorial.embedding_model,
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

為避免因為本教學課程所用資源，導致系統向 Google Cloud 帳戶收取費用，請刪除含有相關資源的專案，或者保留專案但刪除個別資源。

**注意**：刪除專案會造成以下結果：

* **專案中的所有內容都會遭到刪除。**如果使用現有專案來進行本文中的任務，刪除專案將一併移除當中已完成的其他任務'。
* **自訂專案 ID 會消失。**當您之前建立這個專案時，可能建立了想要在日後使用的自訂專案 ID。如要保留使用該專案 ID 的網址 (例如 `appspot.com` 網址)，請刪除在該專案中選取的資源，而不是刪除整個專案。

如果打算探索多種架構、教學課程或快速入門導覽課程，重複使用專案可避免超出專案配額限制。

1. 前往 Google Cloud 控制台的「Manage resources」(管理資源) 頁面。

   [前往「Manage resources」(管理資源)](https://console.cloud.google.com/iam-admin/projects?hl=zh-tw)
2. 在專案清單中選取要刪除的專案，然後點選「Delete」(刪除)。
3. 在對話方塊中輸入專案 ID，然後按一下 [Shut down] (關閉) 以刪除專案。

如要保留專案，但刪除本教學課程中使用的資源，請按照下列步驟操作：

1. 前往「BigQuery」頁面

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在左側窗格中展開專案，然後按一下「資料集」。
3. 針對 `bqml_tutorial` 資料集，依序點按 more\_vert
   **「Open actions」(開啟動作) >「Delete」(刪除)**。
4. 在「Delete dataset」(刪除資料集) 對話方塊中，按一下「Delete」(刪除) 進行確認。
5. 按一下左側窗格中的「連線」。
6. 如要刪除 `__default_cloudresource_connection__` 連結，請依序點按
   more\_vert **「開啟動作」>
   「刪除」**。
7. 在「Delete connection」(刪除連結) 對話方塊中輸入 `delete`，然後按一下「Delete」(刪除) 確認操作。

## 後續步驟

* 如要瞭解如何根據剖析的 PDF 內容建立 RAG 管道，請參閱「[在檢索增強生成管道中剖析 PDF](https://docs.cloud.google.com/bigquery/docs/rag-pipeline-pdf?hl=zh-tw)」。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-10-24 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-10-24 (世界標準時間)。"],[],[]]