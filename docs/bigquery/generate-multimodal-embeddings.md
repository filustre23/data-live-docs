Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 生成及搜尋多模態嵌入項目

本教學課程說明如何使用 BigQuery 和 Vertex AI，為圖片和文字生成多模態嵌入項目，然後使用這些嵌入項目執行文字轉圖像的語意搜尋。

本教學課程涵蓋下列工作：

* 在 Cloud Storage bucket 中的圖片資料上建立 [BigQuery 物件資料表](https://docs.cloud.google.com/bigquery/docs/object-table-introduction?hl=zh-tw)。
* 使用 [BigQuery 中的 Colab Enterprise 筆記本](https://docs.cloud.google.com/bigquery/docs/notebooks-introduction?hl=zh-tw)探索圖片資料。
* 建立以 [Vertex AI `multimodalembedding` 基礎模型](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/learn/models?hl=zh-tw#foundation_model_apis)為目標的 BigQuery ML [遠端模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model?hl=zh-tw)。
* 使用 [`AI.GENERATE_EMBEDDING` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-ai-generate-embedding?hl=zh-tw)搭配遠端模型，從物件資料表中的圖片生成嵌入。
* 修正任何嵌入生成錯誤。
* 選擇性步驟：建立[向量索引](https://docs.cloud.google.com/bigquery/docs/vector-index?hl=zh-tw)，為圖片嵌入項目建立索引。
* 為指定搜尋字串建立文字嵌入。
* 使用 [`VECTOR_SEARCH` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/search_functions?hl=zh-tw#vector_search)，對與文字嵌入類似的圖片嵌入執行語意搜尋。
* 使用筆記本將結果製成圖表。

本教學課程使用[大都會藝術博物館](https://www.metmuseum.org/)的公共領域藝術圖像，這些圖像位於公開的 Cloud Storage [`gcs-public-data--met` bucket](https://console.cloud.google.com/storage/browser/gcs-public-data--met;tab=objects?amp%3BforceOnObjectsSortingFiltering=false&hl=zh-tw)。

## 必要的角色

如要執行本教學課程，您需要下列 Identity and Access Management (IAM) 角色：

* 建立及使用 BigQuery 資料集、連線、模型和筆記本：
  BigQuery Studio 管理員 (`roles/bigquery.studioAdmin`)。
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
* 建立物件資料表：
  `bigquery.tables.create` 和
  `bigquery.tables.update`
* 建立模型並執行推論：
  + `bigquery.jobs.create`
  + `bigquery.models.create`
  + `bigquery.models.getData`
  + `bigquery.models.updateData`
  + `bigquery.models.updateMetadata`
* 建立及使用筆記本：
  + `resourcemanager.projects.get`
  + `resourcemanager.projects.list`
  + `bigquery.config.get`
  + `bigquery.jobs.create`
  + `bigquery.readsessions.create`
  + `bigquery.readsessions.getData`
  + `bigquery.readsessions.update`
  + `dataform.locations.get`
  + `dataform.locations.list`
  + `dataform.repositories.create`  
      
    擁有 `dataform.repositories.create` 權限的使用者，可以使用預設的 Dataform 服務帳戶和授予該服務帳戶的所有權限執行程式碼。詳情請參閱「[Dataform 權限的安全考量](https://docs.cloud.google.com/dataform/docs/access-control?hl=zh-tw#security-considerations-permissions)」。
  + `dataform.repositories.list`
  + `dataform.collections.create`
  + `dataform.collections.list`
  + `aiplatform.notebookRuntimeTemplates.apply`
  + `aiplatform.notebookRuntimeTemplates.get`
  + `aiplatform.notebookRuntimeTemplates.list`
  + `aiplatform.notebookRuntimeTemplates.getIamPolicy`
  + `aiplatform.notebookRuntimes.assign`
  + `aiplatform.notebookRuntimes.get`
  + `aiplatform.notebookRuntimes.list`
  + `aiplatform.operations.list`
  + `aiplatform.notebookRuntimeTemplates.apply`

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
   * **建立專案**：如要建立專案，您需要具備專案建立者角色 (`roles/resourcemanager.projectCreator`)，其中包含 `resourcemanager.projects.create` 權限。[瞭解如何授予角色](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)。
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

## 建立物件資料表

在公開的 Cloud Storage [`gcs-public-data--met` bucket](https://console.cloud.google.com/storage/browser/gcs-public-data--met;tab=objects?amp%3BforceOnObjectsSortingFiltering=false&hl=zh-tw) 中，針對藝術圖片建立物件資料表。
有了物件表格，您就能分析圖片，不必將圖片從 Cloud Storage 移出。

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中執行下列查詢：

   ```
   CREATE OR REPLACE EXTERNAL TABLE `bqml_tutorial.met_images`
   WITH CONNECTION DEFAULT
   OPTIONS
     ( object_metadata = 'SIMPLE',
       uris = ['gs://gcs-public-data--met/*']
     );
   ```

## 探索圖片資料

在 BigQuery 中建立 [Colab Enterprise 筆記本](https://docs.cloud.google.com/colab/docs/introduction?hl=zh-tw)，探索圖片資料。

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. [使用 BigQuery 編輯器建立筆記本](https://docs.cloud.google.com/bigquery/docs/create-notebooks?hl=zh-tw#create-notebook-console)。
3. [將筆記本連線至預設執行階段](https://docs.cloud.google.com/bigquery/docs/create-notebooks?hl=zh-tw#connect_to_the_default_runtime)。
4. 設定筆記本：

   1. 在筆記本中新增程式碼儲存格。
   2. 複製下列程式碼，並貼到程式碼儲存格中：

      ```
      #@title Set up credentials

      from google.colab import auth
      auth.authenticate_user()
      print('Authenticated')

      PROJECT_ID='PROJECT_ID'
      from google.cloud import bigquery
      client = bigquery.Client(PROJECT_ID)
      ```

      將 `PROJECT_ID` 替換為您在本教學課程中使用的專案名稱。
   3. 執行程式碼儲存格。
5. 啟用表格顯示功能：

   1. 在筆記本中新增程式碼儲存格。
   2. 複製下列程式碼，並貼到程式碼儲存格中：

      ```
      #@title Enable data table display
      %load_ext google.colab.data_table
      ```
   3. 執行程式碼儲存格。
6. 建立函式來顯示圖片：

   1. 在筆記本中新增程式碼儲存格。
   2. 複製下列程式碼，並貼到程式碼儲存格中：

      ```
      #@title Util function to display images
      import io
      from PIL import Image
      import matplotlib.pyplot as plt
      import tensorflow as tf

      def printImages(results):
       image_results_list = list(results)
       amt_of_images = len(image_results_list)

       fig, axes = plt.subplots(nrows=amt_of_images, ncols=2, figsize=(20, 20))
       fig.tight_layout()
       fig.subplots_adjust(hspace=0.5)
       for i in range(amt_of_images):
         gcs_uri = image_results_list[i][0]
         text = image_results_list[i][1]
         f = tf.io.gfile.GFile(gcs_uri, 'rb')
         stream = io.BytesIO(f.read())
         img = Image.open(stream)
         axes[i, 0].axis('off')
         axes[i, 0].imshow(img)
         axes[i, 1].axis('off')
         axes[i, 1].text(0, 0, text, fontsize=10)
       plt.show()
      ```
   3. 執行程式碼儲存格。
7. 顯示圖片：

   1. 在筆記本中新增程式碼儲存格。
   2. 複製下列程式碼，並貼到程式碼儲存格中：

      ```
      #@title Display Met images

      inspect_obj_table_query = """
      SELECT uri, content_type
      FROM bqml_tutorial.met_images
      WHERE content_type = 'image/jpeg'
      Order by uri
      LIMIT 10;
      """
      printImages(client.query(inspect_obj_table_query))
      ```
   3. 執行程式碼儲存格。

      結果應如下所示：
8. 將筆記本儲存為 `met-image-analysis`。

## 建立遠端模型

建立遠端模型，代表代管的 Vertex AI 多模態嵌入模型：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中執行下列查詢：

   ```
   CREATE OR REPLACE MODEL `bqml_tutorial.multimodal_embedding_model`
     REMOTE WITH CONNECTION DEFAULT
     OPTIONS (ENDPOINT = 'gemini-embedding-2-preview');
   ```

   查詢會在幾秒內完成，之後您就能存取 `bqml_tutorial` 資料集中顯示的 `multimodal_embedding_model` 模型。由於查詢是使用 `CREATE MODEL` 陳述式建立模型，因此不會有查詢結果。

## 生成圖片嵌入

使用 [`AI.GENERATE_EMBEDDING` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-ai-generate-embedding?hl=zh-tw)，從物件資料表中的圖片產生嵌入內容，然後將這些內容寫入資料表，以供後續步驟使用。產生嵌入內容的作業成本高昂，因此查詢會使用包含 `LIMIT` 子句的子查詢，將嵌入內容的產生作業限制為 10,000 張圖片，而不是嵌入 601,294 張圖片的完整資料集。這也有助於將圖片數量控制在 `AI.GENERATE_EMBEDDING` 函式的 25,000 張上限內。這項查詢大約需要 40 分鐘才能執行完畢。

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中執行下列查詢：

   ```
   CREATE OR REPLACE TABLE `bqml_tutorial.met_image_embeddings`
   AS
   SELECT *
   FROM
     AI.GENERATE_EMBEDDING(
       MODEL `bqml_tutorial.multimodal_embedding_model`,
       (SELECT * FROM `bqml_tutorial.met_images` WHERE content_type = 'image/jpeg' LIMIT 10000))
   ```

## 修正任何嵌入生成錯誤

檢查並修正任何嵌入生成錯誤。由於 [Vertex AI 的生成式 AI 配額](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/quotas?hl=zh-tw)或服務無法使用，導致無法產生嵌入。

`AI.GENERATE_EMBEDDING` 函式會在 `status` 欄中傳回錯誤詳細資料。如果成功產生嵌入內容，這個資料欄會是空白；如果產生失敗，則會顯示錯誤訊息。

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中執行下列查詢，查看是否有任何嵌入生成失敗：

   ```
   SELECT DISTINCT(status),
     COUNT(uri) AS num_rows
   FROM bqml_tutorial.met_image_embeddings
   GROUP BY 1;
   ```
3. 如果傳回含有錯誤的資料列，請捨棄任何無法產生嵌入內容的資料列：

   ```
   DELETE FROM `bqml_tutorial.met_image_embeddings`
   WHERE status = 'A retryable error occurred: RESOURCE_EXHAUSTED error from remote service/endpoint.';
   ```

## 建立向量索引

您可以視需要使用 [`CREATE VECTOR INDEX` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#create_vector_index_statement)，在 `met_images_embeddings` 資料表的 `embedding` 資料欄上建立 `met_images_index` 向量索引。向量索引可讓您更快執行向量搜尋，但會降低召回率，因此傳回的結果會更近似。

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中執行下列查詢：

   ```
   CREATE OR REPLACE
     VECTOR INDEX `met_images_index`
   ON
     bqml_tutorial.met_image_embeddings(embedding)
     OPTIONS (
       index_type = 'IVF',
       distance_type = 'COSINE');
   ```
3. 系統會以非同步方式建立向量索引。如要檢查向量索引是否已建立，請查詢 [`INFORMATION_SCHEMA.VECTOR_INDEXES` 檢視區塊](https://docs.cloud.google.com/bigquery/docs/information-schema-vector-indexes?hl=zh-tw)，並確認 `coverage_percentage` 值大於 `0`，且 `last_refresh_time` 值不是 `NULL`：

   ```
   SELECT table_name, index_name, index_status,
     coverage_percentage, last_refresh_time, disable_reason
   FROM bqml_tutorial.INFORMATION_SCHEMA.VECTOR_INDEXES
   WHERE index_name = 'met_images_index';
   ```

## 為搜尋文字生成嵌入

如要搜尋與指定文字搜尋字串相應的圖片，您必須先為該字串建立文字嵌入。使用與建立圖像嵌入相同的遠端模型建立文字嵌入，然後將文字嵌入寫入表格，以供後續步驟使用。搜尋字串為 `pictures of white or cream colored dress from victorian era`。

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中執行下列查詢：

   ```
   CREATE OR REPLACE TABLE `bqml_tutorial.search_embedding`
   AS
   SELECT * FROM AI.GENERATE_EMBEDDING(
     MODEL `bqml_tutorial.multimodal_embedding_model`,
     (
       SELECT 'pictures of white or cream colored dress from victorian era' AS content
     )
   );
   ```

## 執行文字轉圖片語意搜尋

使用 [`VECTOR_SEARCH` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/search_functions?hl=zh-tw#vector_search)，根據文字嵌入所代表的搜尋字串，執行語意搜尋，找出最相符的圖片。

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中執行下列查詢，進行語意搜尋並將結果寫入資料表：

   ```
   CREATE OR REPLACE TABLE `bqml_tutorial.vector_search_results` AS
   SELECT base.uri AS gcs_uri, distance
   FROM
     VECTOR_SEARCH(
       TABLE `bqml_tutorial.met_image_embeddings`,
       'embedding',
       TABLE `bqml_tutorial.search_embedding`,
       'embedding',
       top_k => 3);
   ```

## 以視覺化方式呈現語意搜尋結果

使用筆記本以視覺化的方式顯示語意搜尋結果。

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 開啟您先前建立的 `met-image-analysis` 筆記本。
3. 以視覺化方式呈現向量搜尋結果：

   1. 在筆記本中新增程式碼儲存格。
   2. 複製下列程式碼，並貼到程式碼儲存格中：

      ```
      query = """
        SELECT * FROM `bqml_tutorial.vector_search_results`
        ORDER BY distance;
      """

      printImages(client.query(query))
      ```
   3. 執行程式碼儲存格。

      結果應如下所示：

## 清除所用資源

**注意**：刪除專案會造成以下結果：

* **專案中的所有內容都會遭到刪除。**如果使用現有專案來進行本文中的任務，刪除專案將一併移除當中已完成的其他任務'。
* **自訂專案 ID 會消失。**當您之前建立這個專案時，可能建立了想要在日後使用的自訂專案 ID。如要保留使用該專案 ID 的網址 (例如 `appspot.com` 網址)，請刪除在該專案中選取的資源，而不是刪除整個專案。

如果打算探索多種架構、教學課程或快速入門導覽課程，重複使用專案可避免超出專案配額限制。

1. 前往 Google Cloud 控制台的「Manage resources」(管理資源) 頁面。

   [前往「Manage resources」(管理資源)](https://console.cloud.google.com/iam-admin/projects?hl=zh-tw)
2. 在專案清單中選取要刪除的專案，然後點選「Delete」(刪除)。
3. 在對話方塊中輸入專案 ID，然後按一下 [Shut down] (關閉) 以刪除專案。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-02 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-02 (世界標準時間)。"],[],[]]