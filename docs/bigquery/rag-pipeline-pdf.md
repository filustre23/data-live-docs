Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見

# 在檢索增強生成管道中剖析 PDF 透過集合功能整理內容 你可以依據偏好儲存及分類內容。

本教學課程將引導您根據剖析的 PDF 內容，建立檢索增強生成 (RAG) 管道。

PDF 檔案 (例如財務文件) 結構複雜，且包含文字、圖表和表格，因此在 RAG 管道中可能難以使用。本教學課程說明如何使用 [`AI.CHUNK_DOCUMENT` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-ai-chunk-document?hl=zh-tw)，根據從 PDF 檔案擷取的重要資訊建構 RAG 管道。

## 目標

本教學課程涵蓋下列工作：

* 建立 Cloud Storage bucket 並上傳範例 PDF 檔案。
* 使用 [`AI.CHUNK_DOCUMENT` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-ai-chunk-document?hl=zh-tw)將 PDF 內容剖析為區塊，然後將內容寫入 BigQuery 資料表。
* 從分塊的 PDF 內容生成嵌入，然後將這些嵌入寫入 BigQuery 資料表。嵌入是 PDF 內容的數值表示法，可讓您對 PDF 內容執行語意搜尋和檢索。
* 對嵌入項目使用 [`VECTOR_SEARCH` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/search_functions?hl=zh-tw#vector_search)，找出語意相似的 PDF 內容。
* 使用 [`AI.GENERATE` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-ai-generate?hl=zh-tw)執行檢索增強生成 (RAG) 來生成文字，並使用向量搜尋結果來增強提示輸入內容，進而改善結果。

## 費用

在本文件中，您會使用下列 Google Cloud計費元件：

* [BigQuery](https://cloud.google.com/bigquery/pricing?hl=zh-tw): You incur costs for the data that you
  process in BigQuery.
* [Gemini Enterprise Agent Platform](https://cloud.google.com/gemini-enterprise-agent-platform/generative-ai/pricing?hl=zh-tw): You incur costs for calls to
  Agent Platform models.
* [Document AI](https://cloud.google.com/document-ai/pricing?hl=zh-tw): You incur costs for calls to the
  Document AI API.
* [Cloud Storage](https://cloud.google.com/storage/pricing?hl=zh-tw): You incur costs for object storage in
  Cloud Storage.

您可以使用 [Pricing Calculator](https://docs.cloud.google.com/products/calculator?hl=zh-tw)，根據預測用量估算費用。

初次使用 Google Cloud 的使用者可能符合[免費試用期](https://docs.cloud.google.com/free?hl=zh-tw)資格。

完成本文所述工作後，您可以刪除建立的資源，避免繼續計費，詳情請參閱「[清除所用資源](#clean-up)」。

## 事前準備

### 控制台

- 登入 Google Cloud 帳戶。如果您未曾使用過 Google Cloud，歡迎[建立帳戶](https://console.cloud.google.com/freetrial?hl=zh-tw)，親自體驗實際使用我們產品的成效。新客戶還能獲得價值 $300 美元的免費抵免額，用於執行、測試及部署工作負載。
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
- Enable the BigQuery, BigQuery Connection, Vertex AI, Document AI, and Cloud Storage APIs, if any are not already enabled.

  **Roles required to enable APIs**

  To enable APIs, you need the `serviceusage.services.enable` permission. If you
  created the project, then you likely already have this permission through the
  Owner role (`roles/owner`). Otherwise, you can get this permission through the
  Service Usage Admin role (`roles/serviceusage.serviceUsageAdmin`).
  [Learn how to grant roles](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw).

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
- Enable the BigQuery, BigQuery Connection, Vertex AI, Document AI, and Cloud Storage APIs, if any are not already enabled.

  **Roles required to enable APIs**

  To enable APIs, you need the `serviceusage.services.enable` permission. If you
  created the project, then you likely already have this permission through the
  Owner role (`roles/owner`). Otherwise, you can get this permission through the
  Service Usage Admin role (`roles/serviceusage.serviceUsageAdmin`).
  [Learn how to grant roles](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw).

  [Enable the APIs](https://console.cloud.google.com/apis/enableflow?apiid=bigquery.googleapis.com%2Cbigqueryconnection.googleapis.com%2Caiplatform.googleapis.com%2Cdocumentai.googleapis.com%2Cstorage.googleapis.com&hl=zh-tw)

1. 確認您在專案中具備下列角色：
   **Storage 管理員**、**Document AI 編輯者**、**BigQuery 管理員**、**專案 IAM 管理員**

   #### 檢查角色

   1. 前往 Google Cloud 控制台的「IAM」頁面。

      [前往「IAM」頁面](https://console.cloud.google.com/projectselector/iam-admin/iam?supportedpurview=project&hl=zh-tw)
   2. 選取專案。
   3. 在「Principal」(主體) 欄中，找出所有代表您或您所屬群組的資料列。如要瞭解您所屬的群組，請與管理員聯絡。
   4. 在指定或包含您的所有資料列中，查看「Role」(角色) 欄，確認角色清單是否包含必要角色。


   #### 授予角色

   1. 前往 Google Cloud 控制台的「IAM」頁面。

      [前往「IAM」頁面](https://console.cloud.google.com/projectselector/iam-admin/iam?supportedpurview=project&hl=zh-tw)
   2. 選取專案。
   3. 按一下person\_add「Grant access」(授予存取權)。
   4. 在「New principals」(新增主體) 欄位中，輸入您的使用者 ID。 這通常是指 Google 帳戶的電子郵件地址。
   5. 按一下「Select a role」(選取角色)，然後搜尋角色。
   6. 如要授予其他角色，請按一下add「Add another role」(新增其他角色)，然後新增其他角色。
   7. 按一下「Save」(儲存)。

### gcloud

- 登入 Google Cloud 帳戶。如果您未曾使用過 Google Cloud，歡迎[建立帳戶](https://console.cloud.google.com/freetrial?hl=zh-tw)，親自體驗實際使用我們產品的成效。新客戶還能獲得價值 $300 美元的免費抵免額，用於執行、測試及部署工作負載。
- [安裝](https://docs.cloud.google.com/sdk/docs/install?hl=zh-tw) Google Cloud CLI。
- 若您採用的是外部識別資訊提供者 (IdP)，請先[使用聯合身分登入 gcloud CLI](https://docs.cloud.google.com/iam/docs/workforce-log-in-gcloud?hl=zh-tw)。
- 執行下列指令，[初始化](https://docs.cloud.google.com/sdk/docs/initializing?hl=zh-tw) gcloud CLI：

  ```
  gcloud init
  ```
- [建立或選取 Google Cloud 專案](https://cloud.google.com/resource-manager/docs/creating-managing-projects?hl=zh-tw)。

  **選取或建立專案所需的角色**

  * **選取專案**：選取專案時不需要特定 IAM 角色，只要您獲派某個專案的角色，即可選取該專案。
  * **建立專案**：如要建立專案，您必須具備專案建立者角色 (`roles/resourcemanager.projectCreator`)，其中包含 `resourcemanager.projects.create` 權限。[瞭解如何授予角色](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)。
  **注意**：如果您不打算保留在這項程序中建立的資源，請建立新專案，不要選取現有專案。如果採用這種做法，當您完成這些步驟後，就可以直接刪除該專案，並移除相關聯的所有資源。
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
- [確認 Google Cloud 專案已啟用計費功能](https://docs.cloud.google.com/billing/docs/how-to/verify-billing-enabled?hl=zh-tw#confirm_billing_is_enabled_on_a_project)。
- 啟用 BigQuery、BigQuery Connection、Vertex AI、Document AI 和 Cloud Storage API (如有尚未啟用的 API)：

  **啟用 API 所需的角色**

  您必須具備 `serviceusage.services.enable` 權限，才能啟用 API。如果您建立了專案，可能已透過擁有者角色 (`roles/owner`) 取得這項權限。否則，您可以透過服務使用情形管理員角色 (`roles/serviceusage.serviceUsageAdmin`) 取得這項權限。[瞭解如何授予角色](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)。

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

  * **選取專案**：選取專案時不需要特定 IAM 角色，只要您獲派某個專案的角色，即可選取該專案。
  * **建立專案**：如要建立專案，您必須具備專案建立者角色 (`roles/resourcemanager.projectCreator`)，其中包含 `resourcemanager.projects.create` 權限。[瞭解如何授予角色](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)。
  **注意**：如果您不打算保留在這項程序中建立的資源，請建立新專案，不要選取現有專案。如果採用這種做法，當您完成這些步驟後，就可以直接刪除該專案，並移除相關聯的所有資源。
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
- [確認 Google Cloud 專案已啟用計費功能](https://docs.cloud.google.com/billing/docs/how-to/verify-billing-enabled?hl=zh-tw#confirm_billing_is_enabled_on_a_project)。
- 啟用 BigQuery、BigQuery Connection、Vertex AI、Document AI 和 Cloud Storage API (如有尚未啟用的 API)：

  **啟用 API 所需的角色**

  您必須具備 `serviceusage.services.enable` 權限，才能啟用 API。如果您建立了專案，可能已透過擁有者角色 (`roles/owner`) 取得這項權限。否則，您可以透過服務使用情形管理員角色 (`roles/serviceusage.serviceUsageAdmin`) 取得這項權限。[瞭解如何授予角色](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)。

  ```
  gcloud services enable bigquery.googleapis.com bigqueryconnection.googleapis.com aiplatform.googleapis.com documentai.googleapis.com storage.googleapis.com
  ```

1. 將角色授予使用者帳戶。針對下列各個 IAM 角色執行下列指令一次：`roles/storage.admin,
   roles/documentai.editor,
   roles/bigquery.admin,
   roles/resourcemanager.projectIamAdmin`

   ```
   gcloud projects add-iam-policy-binding PROJECT_ID --member="user:USER_IDENTIFIER" --role=ROLE
   ```

   更改下列內容：

   * `PROJECT_ID`：專案 ID。
   * `USER_IDENTIFIER`：使用者帳戶 ID。 例如：`myemail@example.com`。
   * `ROLE`：授予使用者帳戶的 IAM 角色。

## 建立資料集

如要建立 BigQuery 資料集，請選取下列其中一個選項：

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。

   如果沒有看到左側窗格，請按一下 last\_page「Expand left pane」(展開左側窗格)，開啟窗格。
3. 在「Explorer」中展開專案，然後按一下「資料集」。
4. 在「Datasets」(資料集) 頁面，按一下「Create dataset」(建立資料集)add。
5. 在「建立資料集」窗格中，執行下列操作：

   * 在「Dataset ID」(資料集 ID) 中輸入 `bqml_tutorial`。
   * 在「資料位置」部分，選取「US」。

   其餘設定均保留預設值。
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
2. 確認資料集已建立：

   ```
   bq ls
   ```

### API

使用定義的[資料集資源](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/datasets?hl=zh-tw)呼叫 [`datasets.insert`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/datasets/insert?hl=zh-tw) 方法：

```
{
  "datasetReference": {
     "datasetId": "bqml_tutorial"
  }
}
```

## 將範例 PDF 上傳至 Cloud Storage

如要將範例 PDF 上傳至 Cloud Storage，請按照下列步驟操作：

1. 前往 <https://www.federalreserve.gov/publications/files/scf23.pdf>，然後點選「下載」圖示 download，下載 `scf23.pdf` 範例 PDF。
2. [建立 Cloud Storage bucket](https://docs.cloud.google.com/storage/docs/creating-buckets?hl=zh-tw)。
3. 將 `scf23.pdf` 檔案[上傳](https://docs.cloud.google.com/storage/docs/uploading-objects?hl=zh-tw)至 bucket。

## 將 PDF 檔案剖析成多個區塊

使用文件處理器和 `AI.CHUNK_DOCUMENT` 函式，將 PDF 檔案剖析為區塊，然後將內容寫入資料表：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中執行下列陳述式：

   ```
   CREATE or REPLACE TABLE bqml_tutorial.chunked_pdf AS (
     SELECT *
     FROM AI.CHUNK_DOCUMENT('gs://BUCKET_NAME/scf23.pdf', chunk_size => 250)
   );
   ```
3. 在查詢編輯器中執行下列查詢，查看剖析後的 PDF 內容子集：

   ```
   SELECT
     chunk_id,
     start_page,
     end_page,
     content
   FROM `bqml_tutorial.chunked_pdf`
   ORDER BY chunk_id
   LIMIT 3;
   ```

   輸出結果會與下列內容相似：

   ```
   +----------+------------+----------+-------------------------------------------+
   | chunk_id | start_page | end_page | content                                   |
   +----------+------------+----------+-------------------------------------------+
   | 1        | 1          | 1        | OF NORS. • BOARD OF GOVERNO FEDERAL       |
   |          |            |          | RESERVE SYSTEM RESEARCH & ANALYSIS        |
   | 2        | 1          | 7        | # Changes in U.S. Family Finances from    |
   |          |            |          | 2019 to 2022                              |
   |          |            |          |                                           |
   |          |            |          | Evidence from the Survey of Consumer...   |
   | 3        | 3          | 5        | # Changes in U.S. Family Finances from    |
   |          |            |          | 2019 to 2022                              |
   |          |            |          |                                           |
   |          |            |          | ## Contents...                            |
   +----------+------------+----------+-------------------------------------------+
   ```

## 生成嵌入項目

為剖析後的 PDF 內容生成嵌入項目，然後寫入資料表：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中執行下列陳述式：

   ```
   CREATE OR REPLACE TABLE `bqml_tutorial.embeddings` AS (
     SELECT *, AI.EMBED(content, endpoint => 'text-embedding-005').result AS embedding
     FROM bqml_tutorial.chunked_pdf
   );
   ```

## 執行向量搜尋

對剖析後的 PDF 內容執行向量搜尋。

下列查詢會接收文字輸入內容，使用 `AI.EMBED` 函式為該輸入內容建立嵌入，然後使用 `VECTOR_SEARCH` 函式，將輸入嵌入與最相似的 PDF 內容嵌入進行比對。結果會顯示與家庭淨資產變化最相關的前十個 PDF 區塊。

1. 前往「BigQuery」頁面

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中執行下列 SQL 陳述式：

   ```
   SELECT
     distance,
     base.chunk_id AS chunk_id,
     base.start_page AS start_page,
     base.end_page AS end_page,
     base.content
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
   | 0.608587 | 25       | 17         | 18       | # Net Worth                       |
   |          |          |            |          |                                   |
   |          |          |            |          | 18 Between the first quarter of   |
   |          |          |            |          | 2019 and the first quarter of...  |
   +----------+----------+------------+----------+-----------------------------------+
   | 0.606387 | 29       | 19         | 21       | ## Net Worth                      |
   |          |          |            |          |                                   |
   |          |          |            |          | ## Net Worth by Family            |
   |          |          |            |          | Characteristics...                |
   +----------+----------+------------+----------+-----------------------------------+
   | 0.599438 | 23       | 17         | 21       | # Net Worth                       |
   |          |          |            |          |                                   |
   |          |          |            |          | The net improvements in...        |
   +----------+----------+------------+----------+-----------------------------------+
   ```

## 生成文字，並以向量搜尋結果強化

對嵌入執行向量搜尋，找出語意相似的 PDF 內容，然後搭配向量搜尋結果使用 `AI.GENERATE` 函式，擴充提示詞輸入內容並改善文字生成結果。在這個例子中，查詢會使用 PDF 區塊中的資訊，回答過去十年家庭淨資產變化的問題。

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
   | Yes, the typical family net worth changed significantly. Between 2019   |
   | and 2022, real median net worth surged by 37% to $192,900.              |
   |                                                                         |
   | This growth contrasts sharply with the period a decade earlier. Between |
   | the 2010 and 2013 SCF surveys, real median net worth actually decreased |
   | by 2%.                                                                  |
   +-------------------------------------------------------------------------+
   ```

## 清除所用資源

為避免因為本教學課程所用資源，導致系統向 Google Cloud 收取費用，請刪除含有相關資源的專案，或者保留專案但刪除個別資源。

### 刪除專案

**注意**：刪除專案會造成以下影響：

* **專案中的所有內容都會遭到刪除。**如果使用現有專案來進行本文中的任務，刪除專案將一併移除當中已完成的其他任務'。
* **自訂專案 ID 會消失。**當您之前建立這個專案時，可能建立了想要在日後使用的自訂專案 ID。如要保留使用該專案 ID 的網址 (例如 `appspot.com` 網址)，請刪除在該專案中選取的資源，而不是刪除整個專案。

如果打算探索多種架構、教學課程或快速入門導覽課程，重複使用專案可避免超出專案配額限制。

刪除 Google Cloud 專案：

```
gcloud projects delete PROJECT_ID
```

## 後續步驟

* 進一步瞭解[嵌入和向量搜尋](https://docs.cloud.google.com/bigquery/docs/vector-search-intro?hl=zh-tw)。
* 進一步瞭解如何執行[語意搜尋和 RAG](https://docs.cloud.google.com/bigquery/docs/vector-index-text-search-tutorial?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-10-24 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-10-24 (世界標準時間)。"],[],[]]