Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見

# 反覆呼叫 ML.GENERATE\_TEXT，處理配額錯誤 透過集合功能整理內容 你可以依據偏好儲存及分類內容。

BigQuery `bqutil.procedure.bqml_generate_text` 公開儲存程序可讓您疊代批次呼叫 [`ML.GENERATE_TEXT` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-generate-text?hl=zh-tw)，以便處理大型資料集，而不會超過端點[配額和限制](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#generative_ai_functions)。即使函式在個別資料列上失敗，BigQuery 查詢工作仍會完成，因此大量要求可能會在輸出資料表中留下 `RESOURCE EXHAUSTED` 個可重試的錯誤。在本教學課程中，您將建立遠端模型並執行預存程序，反覆重試失敗的資料列，直到處理完公開新聞資料集中的所有記錄。

如要在 GitHub 中查看預存程序的原始碼，請參閱 [`bqml_generate_text.sqlx`](https://github.com/GoogleCloudPlatform/bigquery-utils/blob/master/stored_procedures/definitions/bqml_generate_text.sqlx)。如要進一步瞭解預存程序參數和用法，請參閱 [README 檔案](https://github.com/GoogleCloudPlatform/bigquery-utils/blob/master/stored_procedures/README.md#bqml_generate_text-source_table-string-target_table-string-ml_model-string-prompt_column-string-key_columns-array-options_string-string)。

## 目標

* 建立 BigQuery 資料集。
* 在 `gemini-3.5-flash-lite` 模型上建立 BigQuery ML [遠端模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model?hl=zh-tw)。
* 執行 `bqutil.procedure.bqml_generate_text` 預存程序，從 `bigquery-public-data.bbc_news.fulltext` 公開資料集反覆生成文字。
* 驗證生成的文字結果，並確認沒有任何可重試的配額錯誤。

## 費用

在本文件中，您會使用下列 Google Cloud計費元件：

* **BigQuery ML**: You incur costs for the data that you
  process in BigQuery.
* **Gemini Enterprise Agent Platform**: You incur costs for
  calls to the Agent Platform model.

您可以使用 [Pricing Calculator](https://docs.cloud.google.com/products/calculator?hl=zh-tw)，根據預測用量估算費用。

初次使用 Google Cloud 的使用者可能符合[免費試用期](https://docs.cloud.google.com/free?hl=zh-tw)資格。

詳情請參閱 [BigQuery 定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw)和 [Agent Platform 定價](https://docs.cloud.google.com/vertex-ai/generative-ai/pricing?hl=zh-tw)。

## 事前準備

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

1. 啟用 BigQuery、BigQuery Connection 和 Agent Platform API (如有尚未啟用的 API)。

   **啟用 API 所需的角色**

   如要啟用 API，您必須具備 `serviceusage.services.enable` 權限。如果您建立了專案，可能已透過擁有者角色 (`roles/owner`) 取得這項權限。否則，您可以透過 Service Usage 管理員角色 (`roles/serviceusage.serviceUsageAdmin`) 取得這項權限。[瞭解如何授予角色](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)。

   [啟用 API](https://console.cloud.google.com/apis/enableflow?apiid=bigquery.googleapis.com%2Cbigqueryconnection.googleapis.com%2Caiplatform.googleapis.com&hl=zh-tw)

### 必要的角色

如要取得完成本教學課程所需的權限，請要求管理員授予您下列 IAM 角色：

* 建立及使用 BigQuery 資料集、連結和模型：專案的 [BigQuery 管理員](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.admin) (`roles/bigquery.admin`)
* 將權限授予連線的服務帳戶：專案的[專案 IAM 管理員](https://docs.cloud.google.com/iam/docs/roles-permissions/resourcemanager?hl=zh-tw#resourcemanager.projectIamAdmin) (`roles/resourcemanager.projectIamAdmin`)

如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

這些預先定義的角色具備完成本教學課程所需的權限。如要查看確切的必要權限，請展開「Required permissions」(必要權限) 部分：

#### 所需權限

您必須具備下列權限，才能完成本教學課程：

* 建立資料集：
  `bigquery.datasets.create`
* 建立、委派及使用連線：`bigquery.connections.*`
* 設定預設連線：
  `bigquery.config.*`
* 設定服務帳戶權限：
  + `resourcemanager.projects.getIamPolicy`
  + `resourcemanager.projects.setIamPolicy`
* 建立模型並執行推論：
  + `bigquery.jobs.create`
  + `bigquery.models.create`
  + `bigquery.models.getData`
  + `bigquery.models.updateData`
  + `bigquery.models.updateMetadata`

您或許還可透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)取得這些權限。

## 建立資料集

如要建立 BigQuery 資料集，請選取下列其中一個選項：

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。

   如果沒有看到左側窗格，請按一下 last\_page「Expand left pane」(展開左側窗格)，開啟窗格。
3. 在「Explorer」中展開專案，然後按一下「資料集」。
4. 在「Datasets」(資料集) 頁面，按一下add「Create dataset」(建立資料集)。
5. 在「建立資料集」窗格中，執行下列操作：

   * 在「Dataset ID」(資料集 ID) 中輸入 `bqml_tutorial`。
   * 在「資料位置」部分，選取「US」。

   其餘預設設定則保持不變。
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

## 建立遠端模型

使用 [`CREATE MODEL` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model?hl=zh-tw)建立遠端模型，代表託管的 Agent Platform `gemini-3.5-flash-lite` 模型：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中執行下列陳述式：

   ```
   CREATE OR REPLACE MODEL `bqml_tutorial.generate_text`
     REMOTE WITH CONNECTION DEFAULT
     OPTIONS (ENDPOINT = 'gemini-3.5-flash-lite');
   ```

   查詢會在幾秒內完成，之後 `generate_text` 模型就會顯示在「Explorer」窗格的 `bqml_tutorial` 資料集中。由於查詢使用 `CREATE MODEL` 陳述式建立模型，因此不會有查詢結果。

## 執行預存程序

使用 [`CALL` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/procedural-language?hl=zh-tw#call)執行 `bqutil.procedure.bqml_generate_text` 預存程序。這個預存程序會使用 `bqml_tutorial.generate_text` 模型和 `bigquery-public-data.bbc_news.fulltext` 公開資料表，反覆呼叫 [`ML.GENERATE_TEXT` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-generate-text?hl=zh-tw)：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中執行下列陳述式：

   ```
   CALL `bqutil.procedure.bqml_generate_text`(
       "bigquery-public-data.bbc_news.fulltext",          -- source table
       "PROJECT_ID.bqml_tutorial.news_generated_text",  -- destination table
       "PROJECT_ID.bqml_tutorial.generate_text",        -- model
       "body",                                            -- prompt column
       ["filename"],                                      -- key columns
       '{"flatten_json_output": true}'                    -- optional arguments
   );
   ```

   將 `PROJECT_ID` 替換為專案 ID。

   預存程序會建立 `bqml_tutorial.news_generated_text` 資料表，用於存放 `ML.GENERATE_TEXT` 函式的輸出內容。
3. 查詢執行完畢後，請確認 `bqml_tutorial.news_generated_text` 資料表中沒有任何資料列含有可重試的錯誤。在查詢編輯器中執行下列陳述式：

   ```
   SELECT *
   FROM `bqml_tutorial.news_generated_text`
   WHERE ml_generate_text_status LIKE '%A retryable error occurred%';
   ```

   查詢會傳回 `There is no data to display` 訊息。
4. 在查詢編輯器中執行下列陳述式，檢查生成的文字結果範例：

   ```
   SELECT
     filename,
     prompt,
     ml_generate_text_llm_result,
     ml_generate_text_status
   FROM `bqml_tutorial.news_generated_text`
   LIMIT 3;
   ```

   輸出結果會與下列內容相似：

   ```
   +------------------------+------------------------------------------+-----------------------------------------------------------+-------------------------+
   | filename               | prompt                                   | ml_generate_text_llm_result                               | ml_generate_text_status |
   +------------------------+------------------------------------------+-----------------------------------------------------------+-------------------------+
   | bbc/tech/209.txt       | A 20-year-old US man is selling...       | It looks like you shared a news article about Andrew...   |                         |
   | bbc/business/375.txt   | South Korea's largest credit card...     | It looks like you shared a news article about the 2004... |                         |
   | bbc/sport/139.txt      | A brave defensive display, led by...     | It looks like you have shared a match report from a...    |                         |
   +------------------------+------------------------------------------+-----------------------------------------------------------+-------------------------+
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

### 刪除個別資源

如要重複使用專案，請刪除您為本教學課程建立的資源：

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 刪除 `bqml_tutorial` 資料集。刪除資料集也會一併刪除遠端模型和輸出資料表：

   1. 在「Explorer」窗格中展開專案，然後點選「資料集」。
   2. 在「Datasets」(資料集) 清單中，點選 `bqml_tutorial` 資料集。
   3. 在詳細資料窗格中，按一下「delete 刪除」。
   4. 在「Delete dataset」(刪除資料集) 對話方塊中，按一下「Delete」(刪除)。

### bq

刪除 `bqml_tutorial` 資料集、遠端模型和輸出表格：

```
bq rm --dataset --recursive bqml_tutorial
```

## 後續步驟

* 進一步瞭解 [`ML.GENERATE_TEXT` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-generate-text?hl=zh-tw)和 [`AI.GENERATE_TEXT` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-ai-generate-text?hl=zh-tw)。
* 進一步瞭解 [BigQuery 的生成式 AI](https://docs.cloud.google.com/bigquery/docs/generative-ai-overview?hl=zh-tw)。
* 瞭解如何[選擇文字生成函式](https://docs.cloud.google.com/bigquery/docs/choose-text-generation-function?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-11-11 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-11-11 (世界標準時間)。"],[],[]]