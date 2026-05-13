Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 使用預先訓練的 TensorFlow 模型嵌入文字

本教學課程說明如何使用預先訓練的 TensorFlow 模型，在 BigQuery 中生成 NNLM、SWIVEL 和 BERT 文字嵌入。文字嵌入是文字片段的稠密向量表示法，如果兩個文字片段在語意上相似，則其各自的嵌入在嵌入向量空間中會很接近。

## NNLM、SWIVEL 和 BERT 模型

NNLM、SWIVEL 和 BERT 模型的大小、準確率、擴充性和成本各不相同。請參閱下表，判斷要使用哪個模型：

| 型號 | 模型大小 | 嵌入項目維度 | 用途 | 說明 |
| --- | --- | --- | --- | --- |
| [NNLM](https://tfhub.dev/google/nnlm-en-dim50-with-normalization/2) | <150MB | 50 | 短句、新聞、推文、評論 | 類神經網路語言模型 |
| [SWIVEL](https://tfhub.dev/google/tf2-preview/gnews-swivel-20dim/1) | <150MB | 20 | 短句、新聞、推文、評論 | Submatrix-wise Vector Embedding Learner |
| [BERT](https://tfhub.dev/tensorflow/bert_en_cased_L-12_H-768_A-12/4) | ~200MB | 768 | 短句、新聞、推文、評論、短段落 | 基於變換器的雙向編碼器表示技術 |

在本教學課程中，NNLM 和 SWIVEL 模型是[匯入的 TensorFlow 模型](https://docs.cloud.google.com/bigquery/docs/making-predictions-with-imported-tensorflow-models?hl=zh-tw)，而 BERT 模型則是 [Vertex AI 上的遠端模型](https://docs.cloud.google.com/bigquery/docs/bigquery-ml-remote-model-tutorial?hl=zh-tw)。

## 所需權限

* 如要建立資料集，您需要 `bigquery.datasets.create` Identity and Access Management (IAM) 權限。
* 如要建立 bucket，您需要 `storage.buckets.create` IAM 權限。
* 如要將模型上傳至 Cloud Storage，您需要 `storage.objects.create` 和 `storage.objects.get` IAM 權限。
* 如要建立連線資源，您需要下列 IAM 權限：

  + `bigquery.connections.create`
  + `bigquery.connections.get`
* 如要將模型載入 BigQuery ML，您需要下列 IAM 權限：

  + `bigquery.jobs.create`
  + `bigquery.models.create`
  + `bigquery.models.getData`
  + `bigquery.models.updateData`
* 如要執行推論，您需要下列 IAM 權限：

  + `bigquery.tables.getData` 物件表格
  + 模型上的 `bigquery.models.getData`
  + `bigquery.jobs.create`

## 費用

在本文件中，您會使用下列 Google Cloud的計費元件：

* **BigQuery:** You incur costs for the queries that you run in
  BigQuery.
* **BigQuery ML:** You incur costs for the model that you
  create and the inference that you perform in BigQuery ML.
* **Cloud Storage:** You incur costs for the objects that you
  store in Cloud Storage.
* **Vertex AI:** If you follow the instructions for
  generating the BERT model, then you incur costs for deploying the model to
  an endpoint.

如要根據預測用量估算費用，請使用 [Pricing Calculator](https://docs.cloud.google.com/products/calculator?hl=zh-tw)。

初次使用 Google Cloud 的使用者可能符合[免費試用期](https://docs.cloud.google.com/free?hl=zh-tw)資格。

詳情請參閱下列資源：

* [儲存空間定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#storage)
* [BigQuery ML 定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#bqml)
* [Cloud Storage 定價](https://cloud.google.com/storage/pricing?hl=zh-tw)
* [Vertex AI 定價](https://cloud.google.com/vertex-ai/pricing?hl=zh-tw)

## 事前準備

- 登入 Google Cloud 帳戶。如果您是 Google Cloud新手，歡迎[建立帳戶](https://console.cloud.google.com/freetrial?hl=zh-tw)，親自評估產品在實際工作環境中的成效。新客戶還能獲得價值 $300 美元的免費抵免額，可用於執行、測試及部署工作負載。
- In the Google Cloud console, on the project selector page,
  select or create a Google Cloud project.

  **Roles required to select or create a project**

  * **Select a project**: Selecting a project doesn't require a specific
    IAM role—you can select any project that you've been
    granted a role on.
  * **Create a project**: To create a project, you need the Project Creator role
    (`roles/resourcemanager.projectCreator`), which contains the
    `resourcemanager.projects.create` permission. [Learn how to grant
    roles](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw).
  **Note**: If you don't plan to keep the
  resources that you create in this procedure, create a project instead of
  selecting an existing project. After you finish these steps, you can
  delete the project, removing all resources associated with the project.

  [Go to project selector](https://console.cloud.google.com/projectselector2/home/dashboard?hl=zh-tw)
- [Verify that billing is enabled for your Google Cloud project](https://docs.cloud.google.com/billing/docs/how-to/verify-billing-enabled?hl=zh-tw#confirm_billing_is_enabled_on_a_project).
- Enable the BigQuery, BigQuery Connection, and Vertex AI APIs.

  **Roles required to enable APIs**

  To enable APIs, you need the Service Usage Admin IAM
  role (`roles/serviceusage.serviceUsageAdmin`), which
  contains the `serviceusage.services.enable` permission. [Learn how to grant
  roles](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw).

  [Enable the APIs](https://console.cloud.google.com/flows/enableapi?apiid=bigquery.googleapis.com%2Caiplatform.googleapis.com%2Cbigqueryconnection.googleapis.com&hl=zh-tw)

- In the Google Cloud console, on the project selector page,
  select or create a Google Cloud project.

  **Roles required to select or create a project**

  * **Select a project**: Selecting a project doesn't require a specific
    IAM role—you can select any project that you've been
    granted a role on.
  * **Create a project**: To create a project, you need the Project Creator role
    (`roles/resourcemanager.projectCreator`), which contains the
    `resourcemanager.projects.create` permission. [Learn how to grant
    roles](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw).
  **Note**: If you don't plan to keep the
  resources that you create in this procedure, create a project instead of
  selecting an existing project. After you finish these steps, you can
  delete the project, removing all resources associated with the project.

  [Go to project selector](https://console.cloud.google.com/projectselector2/home/dashboard?hl=zh-tw)
- [Verify that billing is enabled for your Google Cloud project](https://docs.cloud.google.com/billing/docs/how-to/verify-billing-enabled?hl=zh-tw#confirm_billing_is_enabled_on_a_project).
- Enable the BigQuery, BigQuery Connection, and Vertex AI APIs.

  **Roles required to enable APIs**

  To enable APIs, you need the Service Usage Admin IAM
  role (`roles/serviceusage.serviceUsageAdmin`), which
  contains the `serviceusage.services.enable` permission. [Learn how to grant
  roles](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw).

  [Enable the APIs](https://console.cloud.google.com/flows/enableapi?apiid=bigquery.googleapis.com%2Caiplatform.googleapis.com%2Cbigqueryconnection.googleapis.com&hl=zh-tw)


**注意：** 只有 BERT 模型需要 Vertex AI API 和 BigQuery Connection API。

## 建立資料集

如要建立名為 `tf_models_tutorial` 的資料集來儲存您建立的模型，請選取下列其中一個選項：

### SQL

使用 [`CREATE SCHEMA` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#create_schema_statement)：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列陳述式：

   ```
   CREATE SCHEMA `PROJECT_ID.tf_models_tutorial`;
   ```

   將 `PROJECT_ID` 替換為您的專案 ID。
3. 按一下「執行」play\_circle。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

### bq

1. 在 Google Cloud 控制台中啟用 Cloud Shell。

   [啟用 Cloud Shell](https://console.cloud.google.com/?cloudshell=true&hl=zh-tw)
2. 如要建立資料集，請執行 [`bq mk` 指令](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#mk-dataset)：

   ```
   bq mk --dataset --location=us PROJECT_ID:tf_models_tutorial
   ```

   將 `PROJECT_ID` 替換為專案 ID。

## 生成模型並上傳至 Cloud Storage

如需使用預先訓練的 TensorFlow 模型產生文字嵌入的詳細操作說明，請參閱 [Colab 筆記本](https://github.com/GoogleCloudPlatform/bigquery-ml-utils/blob/master/notebooks/bqml-generate-text-embedding-model.ipynb)。否則請選取下列其中一個模型：

### NNLM

1. 使用 pip 安裝 [`bigquery-ml-utils` 程式庫](https://github.com/GoogleCloudPlatform/bigquery-ml-utils#installation)：

   ```
   pip install bigquery-ml-utils
   ```
2. 生成 NNLM 模型。下列 Python 程式碼會從 TensorFlow Hub 載入 NNLM 模型，並為 BigQuery 準備該模型：

   ```
   from bigquery_ml_utils import model_generator
   import tensorflow_text

   # Establish an instance of TextEmbeddingModelGenerator.
   text_embedding_model_generator = model_generator.TextEmbeddingModelGenerator()

   # Generate an NNLM model.
   text_embedding_model_generator.generate_text_embedding_model('nnlm', OUTPUT_MODEL_PATH)
   ```

   請將 `OUTPUT_MODEL_PATH` 替換為本機資料夾的路徑，您可以在該資料夾中暫時儲存模型。
3. 選用：列印產生的模型簽章：

   ```
   import tensorflow as tf

   reload_embedding_model = tf.saved_model.load(OUTPUT_MODEL_PATH)
   print(reload_embedding_model.signatures["serving_default"])
   ```
4. 如要將產生的模型從本機資料夾複製到 Cloud Storage bucket，請使用 [Google Cloud CLI](https://docs.cloud.google.com/sdk/gcloud/reference/storage?hl=zh-tw)：

   ```
   gcloud storage cp OUTPUT_MODEL_PATH gs://BUCKET_PATH/nnlm_model --recursive
   ```

   將 `BUCKET_PATH` 替換為要複製模型的 Cloud Storage bucket 名稱。

### SWIVEL

1. 使用 pip 安裝 [`bigquery-ml-utils` 程式庫](https://github.com/GoogleCloudPlatform/bigquery-ml-utils#installation)：

   ```
   pip install bigquery-ml-utils
   ```
2. 生成 SWIVEL 模型。下列 Python 程式碼會從 TensorFlow Hub 載入 SWIVEL 模型，並為 BigQuery 準備模型：

   ```
   from bigquery_ml_utils import model_generator
   import tensorflow_text

   # Establish an instance of TextEmbeddingModelGenerator.
   text_embedding_model_generator = model_generator.TextEmbeddingModelGenerator()

   # Generate a SWIVEL model.
   text_embedding_model_generator.generate_text_embedding_model('swivel', OUTPUT_MODEL_PATH)
   ```

   請將 `OUTPUT_MODEL_PATH` 替換為本機資料夾的路徑，您可以在該資料夾中暫時儲存模型。
3. 選用：列印產生的模型簽章：

   ```
   import tensorflow as tf

   reload_embedding_model = tf.saved_model.load(OUTPUT_MODEL_PATH)
   print(reload_embedding_model.signatures["serving_default"])
   ```
4. 如要將產生的模型從本機資料夾複製到 Cloud Storage bucket，請使用 [Google Cloud CLI](https://docs.cloud.google.com/sdk/gcloud/reference/storage?hl=zh-tw)：

   ```
   gcloud storage cp OUTPUT_MODEL_PATH gs://BUCKET_PATH/swivel_model --recursive
   ```

   將 `BUCKET_PATH` 替換為要複製模型的 Cloud Storage bucket 名稱。

### BERT

1. 使用 pip 安裝 [`bigquery-ml-utils` 程式庫](https://github.com/GoogleCloudPlatform/bigquery-ml-utils#installation)：

   ```
   pip install bigquery-ml-utils
   ```
2. 生成 BERT 模型。下列 Python 程式碼會從 TensorFlow Hub 載入 BERT 模型，並為 BigQuery 準備模型：

   ```
   from bigquery_ml_utils import model_generator
   import tensorflow_text

   # Establish an instance of TextEmbeddingModelGenerator.
   text_embedding_model_generator = model_generator.TextEmbeddingModelGenerator()

   # Generate a BERT model.
   text_embedding_model_generator.generate_text_embedding_model('bert', OUTPUT_MODEL_PATH)
   ```

   請將 `OUTPUT_MODEL_PATH` 替換為本機資料夾的路徑，您可以在該資料夾中暫時儲存模型。
3. 選用：列印產生的模型簽章：

   ```
   import tensorflow as tf

   reload_embedding_model = tf.saved_model.load(OUTPUT_MODEL_PATH)
   print(reload_embedding_model.signatures["serving_default"])
   ```
4. 如要將產生的模型從本機資料夾複製到 Cloud Storage bucket，請使用 [Google Cloud CLI](https://docs.cloud.google.com/sdk/gcloud/reference/storage?hl=zh-tw)：

   ```
   gcloud storage cp OUTPUT_MODEL_PATH gs://BUCKET_PATH/bert_model --recursive
   ```

   將 `BUCKET_PATH` 替換為要複製模型的 Cloud Storage bucket 名稱。

## 將模型載入 BigQuery

選取下列其中一個模型：

### NNLM

使用 [`CREATE MODEL` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create?hl=zh-tw)：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列陳述式：

   ```
   CREATE OR REPLACE MODEL tf_models_tutorial.nnlm_model
   OPTIONS (
     model_type = 'TENSORFLOW',
     model_path = 'gs://BUCKET_NAME/nnlm_model/*');
   ```

   將 `BUCKET_NAME` 改成您先前建立的值區名稱。
3. 按一下「執行」play\_circle。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

### SWIVEL

使用 [`CREATE MODEL` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create?hl=zh-tw)：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列陳述式：

   ```
   CREATE OR REPLACE MODEL tf_models_tutorial.swivel_model
   OPTIONS (
     model_type = 'TENSORFLOW',
     model_path = 'gs://BUCKET_NAME/swivel_model/*');
   ```

   將 `BUCKET_NAME` 改成您先前建立的值區名稱。
3. 按一下「執行」play\_circle。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

### BERT

如要將 BERT 模型載入 BigQuery，請將 BERT 模型匯入 Vertex AI、將模型部署至 Vertex AI 端點、建立連線，然後在 BigQuery 中建立遠端模型。

如要將 BERT 模型匯入 Vertex AI，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的 Vertex AI「模型登錄」頁面。

   [前往 Model Registry](https://console.cloud.google.com/vertex-ai/models?hl=zh-tw)
2. 按一下「匯入」，然後執行下列操作：

   * 在「Name」(名稱) 中輸入 `BERT`。
   * 在「Region」(區域)，選取與 Cloud Storage 值區區域相符的區域。
3. 按一下「繼續」，然後執行下列操作：

   * 在**「Model framework version」(模型架構版本)** 中選取「1.12」`2.8`。
   * 在「模型構件位置」中，輸入儲存模型檔案的 Cloud Storage 值區路徑。例如：`gs://BUCKET_PATH/bert_model`。
4. 按一下 [匯入]。匯入完成後，模型會顯示在「模型登錄」頁面。

如要將 BERT 模型部署至 Vertex AI 端點，並連結至 BigQuery，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的 Vertex AI「模型登錄」頁面。

   [前往 Model Registry](https://console.cloud.google.com/vertex-ai/models?hl=zh-tw)
2. 按一下模型名稱。
3. 按一下「Deploy & test」(部署及測試)。
4. 按一下「Deploy to endpoint」(部署至端點)。
5. 在「端點名稱」部分，輸入 `bert_model_endpoint`。
6. 按一下「繼續」。
7. 選取運算資源。
8. 點選「Deploy」(部署)。
9. [建立 BigQuery Cloud 資源連結](https://docs.cloud.google.com/bigquery/docs/create-cloud-resource-connection?hl=zh-tw#create-cloud-resource-connection)，並[授予連線服務帳戶存取權](https://docs.cloud.google.com/bigquery/docs/bigquery-ml-remote-model-tutorial?hl=zh-tw#set_up_connection_access)。

如要根據 Vertex AI 端點建立遠端模型，請使用 [`CREATE MODEL` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create?hl=zh-tw)：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列陳述式：

   ```
   CREATE OR REPLACE MODEL tf_models_tutorial.bert_model
   INPUT(content STRING)
   OUTPUT(embedding ARRAY<FLOAT64>)
   REMOTE WITH CONNECTION `PROJECT_ID.CONNECTION_LOCATION.CONNECTION_ID`
   OPTIONS (
     ENDPOINT = "https://ENDPOINT_LOCATION-aiplatform.googleapis.com/v1/projects/PROJECT_ID/locations/ENDPOINT_LOCATION/endpoints/ENDPOINT_ID");
   ```

   請替換下列項目：

   * `PROJECT_ID`：專案 ID
   * `CONNECTION_LOCATION`：BigQuery 連線的位置
   * `CONNECTION_ID`：BigQuery 連線的 ID

     在 Google Cloud 控制台中[查看連線詳細資料](https://docs.cloud.google.com/bigquery/docs/working-with-connections?hl=zh-tw#view-connections)時，這是「連線 ID」中顯示的完整連線 ID 最後一個部分的值，例如 `projects/myproject/locations/connection_location/connections/myconnection`
   * `ENDPOINT_LOCATION`：Vertex AI 端點的位置。例如「us-central1」。
   * `ENDPOINT_ID`：模型端點的 ID
3. 按一下「執行」play\_circle。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

## 生成文字嵌入

在本節中，您將使用[`ML.PREDICT()` 推論函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-predict?hl=zh-tw)，從公開資料集 `bigquery-public-data.imdb.reviews` 的 `review` 欄生成文字嵌入。查詢會將表格限制為 500 列，以減少處理的資料量。

### NNLM

```
SELECT
  *
FROM
  ML.PREDICT(
    MODEL `tf_models_tutorial.nnlm_model`,
    (
    SELECT
      review AS content
    FROM
      `bigquery-public-data.imdb.reviews`
    LIMIT
      500)
  );
```

結果大致如下：

```
+-----------------------+----------------------------------------+
| embedding             | content                                |
+-----------------------+----------------------------------------+
|  0.08599445223808289  | Isabelle Huppert must be one of the... |
| -0.04862852394580841  |                                        |
| -0.017750458791851997 |                                        |
|  0.8658871650695801   |                                        |
| ...                   |                                        |
+-----------------------+----------------------------------------+
```

### SWIVEL

```
SELECT
  *
FROM
  ML.PREDICT(
    MODEL `tf_models_tutorial.swivel_model`,
    (
    SELECT
      review AS content
    FROM
      `bigquery-public-data.imdb.reviews`
    LIMIT
      500)
  );
```

結果大致如下：

```
+----------------------+----------------------------------------+
| embedding            | content                                |
+----------------------+----------------------------------------+
|  2.5952553749084473  | Isabelle Huppert must be one of the... |
| -4.015787601470947   |                                        |
|  3.6275434494018555  |                                        |
| -6.045154333114624   |                                        |
| ...                  |                                        |
+----------------------+----------------------------------------+
```

### BERT

```
SELECT
  *
FROM
  ML.PREDICT(
    MODEL `tf_models_tutorial.bert_model`,
    (
    SELECT
      review AS content
    FROM
      `bigquery-public-data.imdb.reviews`
    LIMIT
      500)
  );
```

結果大致如下：

```
+--------------+---------------------+----------------------------------------+
| embedding    | remote_model_status | content                                |
+--------------+---------------------+----------------------------------------+
| -0.694072425 | null                | Isabelle Huppert must be one of the... |
|  0.439208865 |                     |                                        |
|  0.99988997  |                     |                                        |
| -0.993487895 |                     |                                        |
| ...          |                     |                                        |
+--------------+---------------------+----------------------------------------+
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




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-12 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-12 (世界標準時間)。"],[],[]]