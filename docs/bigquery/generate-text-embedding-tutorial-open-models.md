Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 使用開放模型和 AI.GENERATE\_EMBEDDING 函式生成文字嵌入

本教學課程說明如何建立以開放原始碼文字嵌入模型 [Qwen3-Embedding-0.6B](https://huggingface.co/Qwen/Qwen3-Embedding-0.6B) 為基礎的[遠端模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model-open?hl=zh-tw)，然後如何使用 [`AI.GENERATE_EMBEDDING` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-ai-generate-embedding?hl=zh-tw)嵌入 `bigquery-public-data.imdb.reviews` 公開資料表中的電影評論。

## 所需權限

如要執行本教學課程，您需要下列 Identity and Access Management (IAM) 角色：

* 建立及使用 BigQuery 資料集、連線和模型：BigQuery 管理員 (`roles/bigquery.admin`)。
* 將權限授予連線的服務帳戶：專案 IAM 管理員 (`roles/resourcemanager.projectIamAdmin`)。
* 在 Vertex AI 中部署及取消部署模型：Vertex AI 管理員 (`roles/aiplatform.admin`)。

這些預先定義的角色具備執行本文所述工作所需的權限。如要查看確切的必要權限，請展開「Required permissions」(必要權限) 部分：

#### 所需權限

* 建立資料集：`bigquery.datasets.create`
* 建立、委派及使用連線：
  `bigquery.connections.*`
* 設定預設連線：`bigquery.config.*`
* 設定服務帳戶權限：
  `resourcemanager.projects.getIamPolicy` 和
  `resourcemanager.projects.setIamPolicy`
* 部署及取消部署 Vertex AI 模型：
  + `aiplatform.endpoints.deploy`
  + `aiplatform.endpoints.undeploy`
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
  Vertex AI model that's represented by the remote model.

如要根據預測用量估算費用，請使用 [Pricing Calculator](https://docs.cloud.google.com/products/calculator?hl=zh-tw)。

初次使用 Google Cloud 的使用者可能符合[免費試用期](https://docs.cloud.google.com/free?hl=zh-tw)資格。

如要進一步瞭解 BigQuery 定價，請參閱 BigQuery 說明文件中的「[BigQuery 定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw)」一文。

部署至 Vertex AI 的開放式模型會依機器時數收費。也就是說，端點完全設定完成後，系統就會開始計費，直到您取消部署為止。如要進一步瞭解 Vertex AI 定價，請參閱 [Vertex AI 定價](https://cloud.google.com/vertex-ai/pricing?hl=zh-tw#prediction-prices)頁面。

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

## 建立遠端模型

建立代表代管 Vertex AI 模型的遠端模型：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中執行下列陳述式：

```
CREATE OR REPLACE MODEL `bqml_tutorial.qwen3_embedding_model`
  REMOTE WITH CONNECTION DEFAULT
  OPTIONS (
    HUGGING_FACE_MODEL_ID = 'Qwen/Qwen3-Embedding-0.6B'
);
```

查詢作業最多需要 20 分鐘才能完成，完成後，`qwen3_embedding_model` 模型會顯示在「Explorer」(探索工具) 窗格的 `bqml_tutorial` 資料集中。由於查詢是使用 `CREATE MODEL` 陳述式建立模型，因此不會有查詢結果。

## 執行文字嵌入

使用遠端模型和 `AI.GENERATE_EMBEDDING` 函式，對 [IMDB](https://www.imdb.com/) 電影評論執行文字嵌入：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列陳述式，對五則電影評論執行文字嵌入：

   ```
   SELECT
     *
   FROM
     AI.GENERATE_EMBEDDING(
       MODEL `bqml_tutorial.qwen3_embedding_model`,
       (
         SELECT
           review AS content,
           *
         FROM
           `bigquery-public-data.imdb.reviews`
         LIMIT 5
       )
     );
   ```

   結果包含下列資料欄：

   * `embedding`：代表所產生嵌入內容的雙精度浮點數陣列。
   * `status`：對應資料列的 API 回應狀態。如果作業成功，這個值會留空。
   * `content`：要從中擷取嵌入的輸入文字。
   * `bigquery-public-data.imdb.reviews` 資料表中的所有資料欄。

## 取消部署模型

如果您選擇不[刪除專案 (建議做法)](#clean_up)，請務必在 Vertex AI 中取消部署 Qwen3 嵌入模型，以免持續產生相關費用。BigQuery 會在指定閒置時間 (預設為 6.5 小時) 過後，自動取消部署模型。或者，您也可以使用 [`ALTER MODEL` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-alter-model?hl=zh-tw)立即取消部署模型，如下列範例所示：

```
ALTER MODEL `bqml_tutorial.qwen3_embedding_model`
SET OPTIONS (deploy_model = false);
```

詳情請參閱「[自動或立即取消部署開放模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model-open?hl=zh-tw#managed-model-undeployment)」。

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

* 瞭解如何[使用文字嵌入執行語意搜尋和檢索增強生成 (RAG)](https://docs.cloud.google.com/bigquery/docs/vector-index-text-search-tutorial?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-14 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-14 (世界標準時間)。"],[],[]]