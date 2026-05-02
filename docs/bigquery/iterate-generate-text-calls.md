* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 反覆呼叫 ML.GENERATE\_TEXT，處理配額錯誤

本教學課程說明如何使用 BigQuery `bqutil.procedure.bqml_generate_text` 公開預存程序，逐一呼叫 [`ML.GENERATE_TEXT` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-generate-text?hl=zh-tw)。反覆呼叫函式可解決因超出函式[配額和限制](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#cloud_ai_service_functions)而發生的任何可重試錯誤。

如要查看 GitHub 中儲存程序的原始碼，請參閱 [`bqml_generate_text.sqlx`](https://github.com/GoogleCloudPlatform/bigquery-utils/blob/master/stored_procedures/definitions/bqml_generate_text.sqlx)。`bqutil.procedure.bqml_generate_text`如要進一步瞭解預存程序參數和用法，請參閱 [README 檔案](https://github.com/GoogleCloudPlatform/bigquery-utils/blob/master/stored_procedures/README.md#bqml_generate_text-source_table-string-target_table-string-ml_model-string-prompt_column-string-key_columns-array-options_string-string)。

本教學課程會逐步引導您完成下列工作：

* 透過 `gemini-2.5-flash` 模型建立[遠端模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model?hl=zh-tw)。
* 透過對 `ML.GENERATE_TEXT` 函式的呼叫進行疊代，使用遠端模型和 `bigquery-public-data.bbc_news.fulltext` 公開資料表與 `bqutil.procedure.bqml_generate_text` 預存程序。

## 所需權限

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
  Vertex AI model.

如要根據預測用量估算費用，請使用 [Pricing Calculator](https://docs.cloud.google.com/products/calculator?hl=zh-tw)。

初次使用 Google Cloud 的使用者可能符合[免費試用期](https://docs.cloud.google.com/free?hl=zh-tw)資格。

如要進一步瞭解 BigQuery 定價，請參閱 [BigQuery 定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw)。

如要進一步瞭解 Vertex AI 定價，請參閱 [Vertex AI 定價](https://docs.cloud.google.com/vertex-ai/generative-ai/pricing?hl=zh-tw)。

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

建立 BigQuery 資料集來儲存模型和範例資料：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」**BigQuery**頁面](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在「Explorer」窗格中，按一下專案名稱。
3. 依序點按 more\_vert「View actions」(查看動作)**>「Create dataset」(建立資料集)**。
4. 在「建立資料集」頁面中，執行下列操作：

   1. 在「Dataset ID」(資料集 ID) 中輸入 `sample`。
   2. 針對「Location type」(位置類型) 選取「Multi-region」(多區域)，然後選取「US (multiple regions in United States)」(us (多個美國區域))。
   3. 其餘設定請保留預設狀態，然後按一下「建立資料集」。

## 建立文字生成模型

建立代表代管 Vertex AI `gemini-2.5-flash` 模型的遠端模型：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中執行下列陳述式：

   ```
   CREATE OR REPLACE MODEL `sample.generate_text`
     REMOTE WITH CONNECTION DEFAULT
     OPTIONS (ENDPOINT = 'gemini-2.5-flash');
   ```

   查詢作業會在幾秒內完成，完成後，`generate_text`模型會顯示在「Explorer」(探索工具) 窗格的 `sample` 資料集中。由於查詢使用 `CREATE MODEL` 陳述式建立模型，因此沒有查詢結果。

## 執行預存程序

執行 `bqutil.procedure.bqml_generate_text` 預存程序，該程序會使用 `sample.generate_text` 模型和 `bigquery-public-data.bbc_news.fulltext` 公開資料表，反覆呼叫 `ML.GENERATE_TEXT` 函式：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中執行下列陳述式：

   ```
   CALL `bqutil.procedure.bqml_generate_text`(
       "bigquery-public-data.bbc_news.fulltext",   -- source table
       "PROJECT_ID.sample.news_generated_text",  -- destination table
       "PROJECT_ID.sample.generate_text",        -- model
       "body",                                     -- content column
       ["filename"],                               -- key columns
       '{}'                                        -- optional arguments
   );
   ```

   將 `PROJECT_ID` 替換為您在本教學課程中使用的專案 ID。

   預存程序會建立 `sample.news_generated_text` 資料表，用來存放 `ML.GENERATE_TEXT` 函式的輸出內容。
3. 查詢執行完畢後，請確認 `sample.news_generated_text` 資料表中沒有包含可重試錯誤的資料列。在查詢編輯器中執行下列陳述式：

   ```
   SELECT *
   FROM `sample.news_generated_text`
   WHERE ml_generate_text_status LIKE '%A retryable error occurred%';
   ```

   查詢會傳回訊息 `No data to display`。

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