* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 分析圖片

本教學課程說明如何整合 BigQuery ML 與 Gemini，從非結構化圖片資料取得洞察資訊。在本教學課程中，您會根據 [gemini-2.5-flash](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/learn/models?hl=zh-tw#gemini-models) 建立[遠端模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model?hl=zh-tw)，並使用 [`AI.GENERATE_TEXT`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-ai-generate-text?hl=zh-tw) 函式，從一系列電影海報中自動擷取中繼資料，例如片名和上映年份。

## 目標

* 在 Cloud Storage bucket 中的圖片資料上建立 [BigQuery 物件資料表](https://docs.cloud.google.com/bigquery/docs/object-table-introduction?hl=zh-tw)。
* 建立以 Vertex AI `gemini-2.5-flash` 模型為目標的 BigQuery ML 遠端模型。
* 使用 `AI.GENERATE_TEXT` 函式搭配遠端模型，找出與一組電影海報相關聯的電影。

## 費用

本教學課程使用下列 Google Cloud計費元件：

* [BigQuery ML](https://cloud.google.com/bigquery/pricing?hl=zh-tw)
* [Vertex AI](https://docs.cloud.google.com/vertex-ai/generative-ai/pricing?hl=zh-tw)

您可以使用 [Pricing Calculator](https://cloud.google.com/products/calculator?hl=zh-tw) 根據預測用量估算費用。

完成本文所述工作後，您可以刪除建立的資源，避免繼續計費，詳情請參閱「[清除所用資源](#clean-up)」。

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

### 必要的角色

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
* 建立物件資料表：
  `bigquery.tables.create` 和
  `bigquery.tables.update`
* 建立模型並執行推論：
  + `bigquery.jobs.create`
  + `bigquery.models.create`
  + `bigquery.models.getData`
  + `bigquery.models.updateData`
  + `bigquery.models.updateMetadata`

您或許還可透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)取得這些權限。

## 準備環境

如要使用 [gemini-2.5-flash](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/learn/models?hl=zh-tw#gemini-models) 對物件資料表執行 BigQuery ML 推論，請將 BigQuery 預留項目指派給專案。如果專案已指派預留項目，可以略過這個步驟。

### 建立保留項目

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在導覽選單中，按一下「容量管理」。
3. 按一下「建立預留項目」。
4. 在「Create reservation」(建立預留項目) 頁面執行下列操作：

   1. 在「Reservation name」(預留項目名稱) 中輸入 `bqml-tutorial-reservation`。
   2. 在「位置」部分，選取「us (多個美國區域)」。
   3. 其餘設定請保留預設狀態，然後按一下「儲存」。

### 指派預訂項目

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在導覽選單中，按一下「容量管理」。
3. 在「運算單元預留項目」表格中，找出要指派給專案的預留項目。
4. 依序點按 more\_vert「查看動作」**>「建立指派項目」**。
5. 在「Create an assignment」(建立指派作業) 中，按一下「Browse」(瀏覽)，然後選取您的專案。
6. 在「Job type」(工作類型) 區段選取「QUERY」(查詢)。選取這個選項可確保 SQL 查詢使用此預留項目的運算單元。
7. 點選「建立」。

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

在公開的 Cloud Storage [bucket](https://console.cloud.google.com/storage/browser/cloud-samples-data/vertex-ai/dataset-management/datasets/classic-movie-posters;tab=objects?amp%3BforceOnObjectsSortingFiltering=false&hl=zh-tw) 中，為電影海報圖片建立物件資料表。
您可以使用物件資料表分析圖片，不必將圖片從 Cloud Storage 移出。

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中執行下列查詢，建立物件資料表：

   ```
   CREATE OR REPLACE EXTERNAL TABLE `bqml_tutorial.movie_posters`
     WITH CONNECTION DEFAULT
     OPTIONS (
       object_metadata = 'SIMPLE',
       uris =
         ['gs://cloud-samples-data/vertex-ai/dataset-management/datasets/classic-movie-posters/*']);
   ```

## 建立遠端模型

建立代表 Vertex AI `gemini-2.5-flash` 模型的遠端模型：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中執行下列查詢，建立遠端模型：

   ```
   CREATE OR REPLACE MODEL `bqml_tutorial.gemini-vision`
     REMOTE WITH CONNECTION DEFAULT
     OPTIONS (ENDPOINT = 'gemini-2.5-flash');
   ```

   查詢作業可能需要幾分鐘才能完成，完成後，`gemini-vision` 模型會顯示在「Explorer」窗格的 `bqml_tutorial` 資料集中。由於查詢是使用 `CREATE MODEL` 陳述式建立模型，因此不會有查詢結果。

## 分析電影海報

使用遠端模型分析電影海報，判斷每張海報代表的電影，然後將這項資料寫入資料表。

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中執行下列查詢，分析電影海報圖片：

   ```
   CREATE OR REPLACE TABLE
     `bqml_tutorial.movie_posters_results` AS (
     SELECT
       uri,
      result
     FROM
       AI.GENERATE_TEXT( MODEL `bqml_tutorial.gemini-vision`,
         TABLE `bqml_tutorial.movie_posters`,
         STRUCT( 0.2 AS temperature,
           'For the movie represented by this poster, what is the movie title and year of release? Answer in JSON format with two keys: title, year. title should be string, year should be integer.' AS PROMPT)));
   ```
3. 在查詢編輯器中執行下列陳述式，查看資料表資料：

   ```
   SELECT * FROM `bqml_tutorial.movie_posters_results`;
   ```

   輸出結果會與下列內容相似：

   ```
   +--------------------------------------------+----------------------------------+
   | uri                                        | result                           |
   +--------------------------------------------+----------------------------------+
   | gs://cloud-samples-data/vertex-ai/dataset- | json                          |
   | management/datasets/classic-movie-         | {                                |
   | posters/little_annie_rooney.jpg            |  "title": "Little Annie Rooney", |
   |                                            |  "year": 1912                    |
   |                                            | }                                |
   |                                            |                              |
   +--------------------------------------------+----------------------------------+
   | gs://cloud-samples-data/vertex-ai/dataset- | json                          |
   | management/datasets/classic-movie-         | {                                |
   | posters/mighty_like_a_mouse.jpg            |  "title": "Mighty Like a Moose", |
   |                                            |  "year": 1926                    |
   |                                            | }                                |
   |                                            |                              |
   +--------------------------------------------+----------------------------------+
   | gs://cloud-samples-data/vertex-ai/dataset- | json                          |
   | management/datasets/classic-movie-         | {                                |
   | posters/brown_of_harvard.jpeg              |  "title": "Brown of Harvard",    |
   |                                            |  "year": 1926                    |
   |                                            | }                                |
   |                                            |                              |
   +--------------------------------------------+----------------------------------+
   ```

## 設定模型輸出內容格式

為了方便閱讀電影名稱和年份資料，請格式化模型傳回的資料。

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中執行下列查詢，格式化資料：

   ```
   CREATE OR REPLACE TABLE
     `bqml_tutorial.movie_posters_results_formatted` AS (
     SELECT
       uri,
       JSON_QUERY(RTRIM(LTRIM(results.result, " ```json"), "```"), "$.title") AS title,
       JSON_QUERY(RTRIM(LTRIM(results.result, " ```json"), "```"), "$.year") AS year
     FROM
       `bqml_tutorial.movie_posters_results` results );
   ```
3. 在查詢編輯器中執行下列陳述式，查看資料表資料：

   ```
   SELECT * FROM `bqml_tutorial.movie_posters_results_formatted`;
   ```

   輸出結果會與下列內容相似：

   ```
   +--------------------------------------------+----------------------------+------+
   | uri                                        | title                      | year |
   +--------------------------------------------+----------------------------+------+
   | gs://cloud-samples-data/vertex-ai/dataset- | "Barque sortant du port"   | 1895 |
   | management/datasets/classic-movie-         |                            |      |
   | posters/barque_sortant_du_port.jpeg        |                            |      |
   +--------------------------------------------+----------------------------+------+
   | gs://cloud-samples-data/vertex-ai/dataset- | "The Great Train Robbery"  | 1903 |
   | management/datasets/classic-movie-         |                            |      |
   | posters/the_great_train_robbery.jpg        |                            |      |
   +--------------------------------------------+----------------------------+------+
   | gs://cloud-samples-data/vertex-ai/dataset- | "Little Annie Rooney"      | 1912 |
   | management/datasets/classic-movie-         |                            |      |
   | posters/little_annie_rooney.jpg            |                            |      |
   +--------------------------------------------+----------------------------+------+
   ```

### 刪除專案

**注意**：刪除專案會造成以下結果：

* **專案中的所有內容都會遭到刪除。**如果使用現有專案來進行本文中的任務，刪除專案將一併移除當中已完成的其他任務'。
* **自訂專案 ID 會消失。**當您之前建立這個專案時，可能建立了想要在日後使用的自訂專案 ID。如要保留使用該專案 ID 的網址 (例如 `appspot.com` 網址)，請刪除在該專案中選取的資源，而不是刪除整個專案。

如果打算探索多種架構、教學課程或快速入門導覽課程，重複使用專案可避免超出專案配額限制。

1. 前往 Google Cloud 控制台的「Manage resources」(管理資源) 頁面。

   [前往「Manage resources」(管理資源)](https://console.cloud.google.com/iam-admin/projects?hl=zh-tw)
2. 在專案清單中選取要刪除的專案，然後點選「Delete」(刪除)。
3. 在對話方塊中輸入專案 ID，然後按一下 [Shut down] (關閉) 以刪除專案。

### 刪除個別資源

如要重複使用專案，請刪除您在教學課程中建立的資源。

#### 刪除資料集

### 控制台

執行下列 SQL 指令，刪除整個 `bqml_tutorial` 資料集及其所有內容：

```
DROP SCHEMA IF EXISTS `bqml_tutorial` CASCADE;
```

### bq

刪除整個 `bqml_tutorial` 資料集和所有內容：

```
bq rm -r bqml_tutorial
```

#### 刪除保留項目

### 控制台

如果您在本教學課程中建立了 BigQuery 預留項目，請移除該項目，以免繼續產生運算單元費用。

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在導覽選單中，按一下「容量管理」。
3. 在「運算單元預留項目」表格中，找出 **`bqml-tutorial-reservation`**。
4. 依序點選 more\_vert「查看動作」 >「刪除」。

### bq

如果您在 `us` 位置建立了名為 `bqml-tutorial-reservation` 的 BigQuery 預留項目，請使用下列指令移除該項目：

```
bq rm --reservation --location=us bqml-tutorial-reservation
```

#### 刪除連線

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在左側窗格中，依序點選 explore「Explorer」、專案和「Connections」。
3. 在表格中找出連線。
4. 依序點選 more\_vert「查看動作」**> 刪除**。

### bq

刪除連線：

```
bq rm --connection --location=us CONNECTION_ID
```

將 CONNECTION\_ID 替換為連線的實際 ID。

## 後續步驟

* 進一步瞭解 [BigQuery 中的生成式 AI 函式](https://docs.cloud.google.com/bigquery/docs/generative-ai-overview?hl=zh-tw)。
* 瞭解如何[使用資料調整模型](https://docs.cloud.google.com/bigquery/docs/generate-text-tuning?hl=zh-tw)。
* 查看 Google Cloud 的參考架構、圖表和最佳做法。歡迎瀏覽我們的 [Cloud Architecture Center](https://docs.cloud.google.com/architecture?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-02 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-02 (世界標準時間)。"],[],[]]