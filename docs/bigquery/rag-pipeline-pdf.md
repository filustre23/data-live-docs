Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見

# 在檢索增強生成管道中剖析 PDF 透過集合功能整理內容 你可以依據偏好儲存及分類內容。

本教學課程會逐步說明如何根據剖析的 PDF 內容，建立檢索增強生成 (RAG) 管道。

由於 PDF 檔案 (例如財務文件) 結構複雜，且包含文字、圖表和表格，因此難以在 RAG 管道中使用。本教學課程說明如何搭配使用 [`AI.PARSE_DOCUMENT` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-ai-parse-document?hl=zh-tw)和 Document AI 的版面配置剖析器，根據從 PDF 檔案擷取的關鍵資訊，建構 RAG pipeline。

## 目標

本教學課程涵蓋下列工作：

* 建立 Cloud Storage bucket 並上傳範例 PDF 檔案。
* [建立 Document AI 處理器](https://docs.cloud.google.com/document-ai/docs/create-processor?hl=zh-tw#create-processor)，用於剖析 PDF 檔案。
* 使用 [`AI.PARSE_DOCUMENT` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-ai-parse-document?hl=zh-tw)將 PDF 內容剖析為區塊，然後將該內容寫入 BigQuery 資料表。
* 從剖析的 PDF 內容生成嵌入項目，然後將這些嵌入項目寫入 BigQuery 資料表。嵌入是 PDF 內容的數值表示法，可讓您對 PDF 內容執行語意搜尋和擷取。
* 在嵌入上使用 [`VECTOR_SEARCH` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/search_functions?hl=zh-tw#vector_search)，找出語意相似的 PDF 內容。
* 使用 [`AI.GENERATE` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-ai-generate?hl=zh-tw)生成文字，並運用向量搜尋結果加強提示輸入內容，進而提升結果品質，執行檢索增強生成 (RAG) 作業。

## 費用

在本文件中，您會使用下列 Google Cloud的計費元件：

* [BigQuery](https://cloud.google.com/bigquery/pricing?hl=zh-tw): You incur costs for the data that you
  process in BigQuery.
* [Gemini Enterprise Agent Platform](https://cloud.google.com/gemini-enterprise-agent-platform/generative-ai/pricing?hl=zh-tw): You incur costs for calls to
  Agent Platform models.
* [Document AI](https://cloud.google.com/document-ai/pricing?hl=zh-tw): You incur costs for calls to the
  Document AI API.
* [Cloud Storage](https://cloud.google.com/storage/pricing?hl=zh-tw): You incur costs for object storage in
  Cloud Storage.

如要根據預測用量估算費用，請使用 [Pricing Calculator](https://docs.cloud.google.com/products/calculator?hl=zh-tw)。

初次使用 Google Cloud 的使用者可能符合[免費試用期](https://docs.cloud.google.com/free?hl=zh-tw)資格。

完成本文所述工作後，您可以刪除建立的資源，避免繼續計費，詳情請參閱「[清除所用資源](#clean-up)」。

## 事前準備

### 控制台

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
- Enable the BigQuery, BigQuery Connection, Vertex AI, Document AI, and Cloud Storage APIs.

  **Roles required to enable APIs**

  To enable APIs, you need the Service Usage Admin IAM
  role (`roles/serviceusage.serviceUsageAdmin`), which
  contains the `serviceusage.services.enable` permission. [Learn how to grant
  roles](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw).

  [Enable the APIs](https://console.cloud.google.com/apis/enableflow?apiid=bigquery.googleapis.com%2Cbigqueryconnection.googleapis.com%2Caiplatform.googleapis.com%2Cdocumentai.googleapis.com%2Cstorage.googleapis.com&hl=zh-tw)

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
- Enable the BigQuery, BigQuery Connection, Vertex AI, Document AI, and Cloud Storage APIs.

  **Roles required to enable APIs**

  To enable APIs, you need the Service Usage Admin IAM
  role (`roles/serviceusage.serviceUsageAdmin`), which
  contains the `serviceusage.services.enable` permission. [Learn how to grant
  roles](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw).

  [Enable the APIs](https://console.cloud.google.com/apis/enableflow?apiid=bigquery.googleapis.com%2Cbigqueryconnection.googleapis.com%2Caiplatform.googleapis.com%2Cdocumentai.googleapis.com%2Cstorage.googleapis.com&hl=zh-tw)

1. 請確認您在專案中具備下列一或多個角色：
   **Storage 管理員**、
   **Document AI 編輯者**、
   **BigQuery 管理員**、
   **專案 IAM 管理員**

   #### 檢查角色

   1. 前往 Google Cloud 控制台的「IAM」頁面。

      [前往「IAM」頁面](https://console.cloud.google.com/projectselector/iam-admin/iam?supportedpurview=project&hl=zh-tw)
   2. 選取專案。
   3. 在「主體」欄中，找出所有識別您或您所屬群組的資料列。如要瞭解自己所屬的群組，請與管理員聯絡。
   4. 針對指定或包含您的所有列，請檢查「角色」欄，確認角色清單是否包含必要角色。


   #### 授予角色

   1. 前往 Google Cloud 控制台的「IAM」頁面。

      [前往「IAM」頁面](https://console.cloud.google.com/projectselector/iam-admin/iam?supportedpurview=project&hl=zh-tw)
   2. 選取專案。
   3. 按一下person\_add「Grant access」(授予存取權)。
   4. 在「New principals」(新增主體) 欄位中，輸入您的使用者 ID。 這通常是指 Google 帳戶的電子郵件地址。
   5. 按一下「選取角色」，然後搜尋角色。
   6. 如要授予其他角色，請按一下add「Add another role」(新增其他角色)，然後新增其他角色。
   7. 按一下「Save」(儲存)。

### gcloud

- 登入 Google Cloud 帳戶。如果您是 Google Cloud新手，歡迎[建立帳戶](https://console.cloud.google.com/freetrial?hl=zh-tw)，親自評估產品在實際工作環境中的成效。新客戶還能獲得價值 $300 美元的免費抵免額，可用於執行、測試及部署工作負載。
- [安裝](https://docs.cloud.google.com/sdk/docs/install?hl=zh-tw) Google Cloud CLI。
- 若您採用的是外部識別資訊提供者 (IdP)，請先[使用聯合身分登入 gcloud CLI](https://docs.cloud.google.com/iam/docs/workforce-log-in-gcloud?hl=zh-tw)。
- 執行下列指令，[初始化](https://docs.cloud.google.com/sdk/docs/initializing?hl=zh-tw) gcloud CLI：

  ```
  gcloud init
  ```
- [建立或選取 Google Cloud 專案](https://cloud.google.com/resource-manager/docs/creating-managing-projects?hl=zh-tw)。

  **選取或建立專案所需的角色**

  * **選取專案**：選取專案時，不需要具備特定 IAM 角色，只要您已獲授角色，即可選取任何專案。
  * **建立專案**：如要建立專案，您需要「專案建立者」角色 (`roles/resourcemanager.projectCreator`)，其中包含 `resourcemanager.projects.create` 權限。[瞭解如何授予角色](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)。
  **注意**：如果您不打算保留在這項程序中建立的資源，請建立新專案，而不要選取現有專案。完成這些步驟後，您就可以刪除專案，並移除與該專案相關聯的所有資源。
  * 建立 Google Cloud 專案：

    ```
    gcloud projects create PROJECT_ID
    ```

    將 `PROJECT_ID` 替換為您要建立的 Google Cloud 專案名稱。
  * 選取您建立的 Google Cloud 專案：

    ```
    gcloud config set project PROJECT_ID
    ```

    將 `PROJECT_ID` 替換為 Google Cloud 專案名稱。
- [確認專案已啟用計費功能 Google Cloud](https://docs.cloud.google.com/billing/docs/how-to/verify-billing-enabled?hl=zh-tw#confirm_billing_is_enabled_on_a_project) 。
- 啟用 BigQuery、BigQuery Connection、Vertex AI、Document AI 和 Cloud Storage API：

  **啟用 API 時所需的角色**

  如要啟用 API，您需要具備服務使用情形管理員 IAM 角色 (`roles/serviceusage.serviceUsageAdmin`)，其中包含 `serviceusage.services.enable` 權限。[瞭解如何授予角色](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)。

  ```
  gcloud services enable bigquery.googleapis.com bigqueryconnection.googleapis.com aiplatform.googleapis.com documentai.googleapis.com storage.googleapis.com
  ```

- [安裝](https://docs.cloud.google.com/sdk/docs/install?hl=zh-tw) Google Cloud CLI。
- 若您採用的是外部識別資訊提供者 (IdP)，請先[使用聯合身分登入 gcloud CLI](https://docs.cloud.google.com/iam/docs/workforce-log-in-gcloud?hl=zh-tw)。
- 執行下列指令，[初始化](https://docs.cloud.google.com/sdk/docs/initializing?hl=zh-tw) gcloud CLI：

  ```
  gcloud init
  ```
- [建立或選取 Google Cloud 專案](https://cloud.google.com/resource-manager/docs/creating-managing-projects?hl=zh-tw)。

  **選取或建立專案所需的角色**

  * **選取專案**：選取專案時，不需要具備特定 IAM 角色，只要您已獲授角色，即可選取任何專案。
  * **建立專案**：如要建立專案，您需要「專案建立者」角色 (`roles/resourcemanager.projectCreator`)，其中包含 `resourcemanager.projects.create` 權限。[瞭解如何授予角色](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)。
  **注意**：如果您不打算保留在這項程序中建立的資源，請建立新專案，而不要選取現有專案。完成這些步驟後，您就可以刪除專案，並移除與該專案相關聯的所有資源。
  * 建立 Google Cloud 專案：

    ```
    gcloud projects create PROJECT_ID
    ```

    將 `PROJECT_ID` 替換為您要建立的 Google Cloud 專案名稱。
  * 選取您建立的 Google Cloud 專案：

    ```
    gcloud config set project PROJECT_ID
    ```

    將 `PROJECT_ID` 替換為 Google Cloud 專案名稱。
- [確認專案已啟用計費功能 Google Cloud](https://docs.cloud.google.com/billing/docs/how-to/verify-billing-enabled?hl=zh-tw#confirm_billing_is_enabled_on_a_project) 。
- 啟用 BigQuery、BigQuery Connection、Vertex AI、Document AI 和 Cloud Storage API：

  **啟用 API 時所需的角色**

  如要啟用 API，您需要具備服務使用情形管理員 IAM 角色 (`roles/serviceusage.serviceUsageAdmin`)，其中包含 `serviceusage.services.enable` 權限。[瞭解如何授予角色](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)。

  ```
  gcloud services enable bigquery.googleapis.com bigqueryconnection.googleapis.com aiplatform.googleapis.com documentai.googleapis.com storage.googleapis.com
  ```

1. 將角色授予使用者帳戶。針對下列每個 IAM 角色，執行一次下列指令：
   `roles/storage.admin,
   roles/documentai.editor,
   roles/bigquery.admin,
   roles/resourcemanager.projectIamAdmin`

   ```
   gcloud projects add-iam-policy-binding PROJECT_ID --member="user:USER_IDENTIFIER" --role=ROLE
   ```

   更改下列內容：

   * `PROJECT_ID`：專案 ID。
   * `USER_IDENTIFIER`：使用者帳戶的 ID。 例如：`myemail@example.com`。
   * `ROLE`：授予使用者帳戶的 IAM 角色。

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

## 將範例 PDF 上傳至 Cloud Storage

如要將範例 PDF 上傳至 Cloud Storage，請按照下列步驟操作：

1. 前往 <https://www.federalreserve.gov/publications/files/scf23.pdf>，然後按一下下載圖示 download，即可下載 `scf23.pdf` 範例 PDF。
2. [建立 Cloud Storage bucket](https://docs.cloud.google.com/storage/docs/creating-buckets?hl=zh-tw)。
3. [上傳](https://docs.cloud.google.com/storage/docs/uploading-objects?hl=zh-tw) `scf23.pdf` 檔案至 bucket。

## 建立文件處理器

[建立文件處理器](https://docs.cloud.google.com/document-ai/docs/create-processor?hl=zh-tw#create-processor)，以 `us` 多區域中的[版面配置剖析器處理器](https://docs.cloud.google.com/document-ai/docs/layout-parse-chunk?hl=zh-tw)為基礎。從「處理器詳細資料」頁面複製預測端點，以供下一節使用。

## 將 PDF 檔案剖析為區塊

使用 `AI.PARSE_DOCUMENT` 函式搭配文件處理器，將 PDF 檔案剖析為區塊，然後將該內容寫入表格。

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中執行下列陳述式：

   ```
   CREATE OR REPLACE TABLE bqml_tutorial.parsed_pdf
   AS (
     SELECT *
     FROM
       AI.PARSE_DOCUMENT(
         (
           SELECT
             OBJ.MAKE_REF("gs://BUCKET/scf23.pdf") AS ref
         ),
         endpoint => "PREDICTION_ENDPOINT",
         chunk_size => 250)
   );
   ```

## 生成嵌入項目

為剖析的 PDF 內容生成嵌入項目，然後寫入資料表：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中執行下列陳述式：

   ```
   CREATE OR REPLACE TABLE `bqml_tutorial.embeddings` AS (
     SELECT *, AI.EMBED(content, endpoint => 'text-embedding-005') AS embedding
     FROM bqml_tutorial.parsed_pdf
   );
   ```

## 執行向量搜尋

對剖析的 PDF 內容執行向量搜尋。

下列查詢會接收文字輸入內容、使用 `AI.EMBED` 函式為該輸入內容建立嵌入，然後使用 `VECTOR_SEARCH` 函式，將輸入嵌入與最相似的 PDF 內容嵌入進行比對。結果會顯示與家庭淨資產變動最相關的十個 PDF 區塊。

1. 前往「BigQuery」頁面

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中，執行下列 SQL 陳述式：

   ```
   SELECT distance, base.chunk_id, base.start_page, base.end_page, base.content
   FROM
     VECTOR_SEARCH(
       TABLE `bqml_tutorial.embeddings`,
       'embedding',
       query_value =>
         AI.EMBED(
           'Did the typical family net worth increase? If so, by how much?',
           endpoint => 'text-embedding-005').result,
       top_k => 3,
       OPTIONS => '{"fraction_lists_to_search": 0.01}')
   ORDER BY distance DESC;
   ```

   輸出結果會與下列內容相似：

   ```
   +----------+----------+------------+----------+-----------------------------------+
   | distance | chunk_id | start_page | end_page | content                           |
   +----------+----------+------------+----------+-----------------------------------+
   | 0.645685 | 26       | 17         | 18       | 18 Between the first quarter of   |
   |          |          |            |          | 2019 and the first quarter of...  |
   +----------+----------+------------+----------+-----------------------------------+
   | 0.602665 | 30       | 19         | 21       | ## Net Worth by Family            |
   |          |          |            |          | Characteristics...                |
   +----------+----------+------------+----------+-----------------------------------+
   | 0.599438 | 24       | 17         | 21       | # Net Worth                       |
   |          |          |            |          | The net improvements in...        |
   +----------+----------+------------+----------+-----------------------------------+
   ```

## 根據向量搜尋結果生成文字

對嵌入執行向量搜尋，找出語意相似的 PDF 內容，然後搭配向量搜尋結果使用 `AI.GENERATE_TEXT` 函式，擴增提示輸入內容並提升文字生成結果。在本例中，查詢會使用 PDF 區塊中的資訊，回答有關過去十年家庭淨值變化的問題。

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中執行下列陳述式：

   ```
   SELECT
     AI.GENERATE(
       CONCAT('Did the typical family net worth change? How does this compare the SCF survey a decade earlier? Be concise and use the following context:',
               STRING_AGG(FORMAT("context: %s", base.content), ',\n')
       )
     ).result AS response
   FROM
     VECTOR_SEARCH(
       TABLE `bqml_tutorial.embeddings`,
       'embedding',
       query_value =>
         AI.EMBED(
           'Did the typical family net worth increase? If so, by how much?',
           endpoint => 'text-embedding-005').result,
       top_k => 3,
       OPTIONS => '{"fraction_lists_to_search": 0.01}')
   ```

   輸出結果會與下列內容相似：

   ```
   +-------------------------------------------------------------------------+
   | response                                                                |
   +-------------------------------------------------------------------------+
   | Yes, the typical family net worth changed significantly.                |
   |                                                                         |
   | Real median net worth surged 37% between the 2019 and 2022 SCF surveys. |
   | This contrasts sharply with a decade earlier (2010-2013), when real     |
   | median net worth decreased 2%.                                          |
   +-------------------------------------------------------------------------+
   ```

## 清除所用資源

為避免因為本教學課程所用資源，導致系統向 Google Cloud 收取費用，請刪除含有相關資源的專案，或者保留專案但刪除個別資源。

### 刪除專案

**注意**：刪除專案會造成以下結果：

* **專案中的所有內容都會遭到刪除。**如果使用現有專案來進行本文中的任務，刪除專案將一併移除當中已完成的其他任務'。
* **自訂專案 ID 會消失。**當您之前建立這個專案時，可能建立了想要在日後使用的自訂專案 ID。如要保留使用該專案 ID 的網址 (例如 `appspot.com` 網址)，請刪除在該專案中選取的資源，而不是刪除整個專案。

如果打算探索多種架構、教學課程或快速入門導覽課程，重複使用專案可避免超出專案配額限制。

刪除 Google Cloud 專案：

```
gcloud projects delete PROJECT_ID
```

## 後續步驟

- 進一步瞭解 [`AI.PARSE_DOCUMENT` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-ai-parse-document?hl=zh-tw)。- 進一步瞭解如何執行[語意搜尋和 RAG](https://docs.cloud.google.com/bigquery/docs/vector-index-text-search-tutorial?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-19 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-19 (世界標準時間)。"],[],[]]