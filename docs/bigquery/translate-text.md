Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見

# 使用 AI.TRANSLATE 函式翻譯文字 透過集合功能整理內容 你可以依據偏好儲存及分類內容。

[`AI.TRANSLATE` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-ai-translate?hl=zh-tw)可讓您直接在 BigQuery 中翻譯文字。舉例來說，您可以將產品目錄本地化、為全球支援團隊翻譯客戶意見回饋，或將多語言問卷調查回覆標準化，而不必建立個別的資料管道。函式會使用您的使用者憑證，將 BigQuery 連結至 Cloud Translation API，因此您不需要建立連線或遠端模型。

在本教學課程中，您將建立多語言顧客意見回饋的範例資料表、使用自動偵測語言功能將文字翻譯成英文、檢查翻譯中繼資料，以及使用[翻譯 LLM](https://docs.cloud.google.com/translate/docs/translation-llm?hl=zh-tw) 模型將電影評論翻譯成西班牙文。

## 目標

* 建立資料集和多語言文字範例資料表。
* 自動偵測語言，將多語言文字翻譯成英文。
* 傳回翻譯中繼資料和偵測到的原文語言代碼。
* 使用 Translation LLM 模型翻譯細緻的文字。

## 費用

在本文件中，您會使用下列 Google Cloud計費元件：

* **BigQuery.** You incur costs for the data that you
  process in BigQuery.
* **Cloud Translation.** You incur costs for calls to the
  Cloud Translation API.

您可以使用 [Pricing Calculator](https://docs.cloud.google.com/products/calculator?hl=zh-tw)，根據預測用量估算費用。

初次使用 Google Cloud 的使用者可能符合[免費試用期](https://docs.cloud.google.com/free?hl=zh-tw)資格。

詳情請參閱 [BigQuery 定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw)和 [Translation 定價](https://cloud.google.com/translate/pricing?hl=zh-tw)。

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
- Enable the BigQuery and Translation APIs, if any are not already enabled.

  **Roles required to enable APIs**

  To enable APIs, you need the `serviceusage.services.enable` permission. If you
  created the project, then you likely already have this permission through the
  Owner role (`roles/owner`). Otherwise, you can get this permission through the
  Service Usage Admin role (`roles/serviceusage.serviceUsageAdmin`).
  [Learn how to grant roles](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw).

  [Enable the APIs](https://console.cloud.google.com/apis/enableflow?apiid=bigquery.googleapis.com%2Ctranslate.googleapis.com&hl=zh-tw)

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
- Enable the BigQuery and Translation APIs, if any are not already enabled.

  **Roles required to enable APIs**

  To enable APIs, you need the `serviceusage.services.enable` permission. If you
  created the project, then you likely already have this permission through the
  Owner role (`roles/owner`). Otherwise, you can get this permission through the
  Service Usage Admin role (`roles/serviceusage.serviceUsageAdmin`).
  [Learn how to grant roles](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw).

  [Enable the APIs](https://console.cloud.google.com/apis/enableflow?apiid=bigquery.googleapis.com%2Ctranslate.googleapis.com&hl=zh-tw)

1. 確認您具備下列專案角色：
   **BigQuery 資料編輯者**、
   **BigQuery 工作使用者**、
   **Cloud Translation API 使用者**。

   #### 檢查角色

   1. 前往 Google Cloud 控制台的「IAM」頁面。

      [前往「IAM」頁面](https://console.cloud.google.com/projectselector/iam-admin/iam?supportedpurview=project&hl=zh-tw)
   2. 選取專案。
   3. 在「Principal」(主體) 欄中，找出所有代表您或您所屬群組的資料列。如要瞭解您所屬的群組，請與管理員聯絡。
   4. 針對指定或包含您的所有資料列，請查看「Role」(角色) 欄，確認角色清單是否包含必要角色。


   #### 授予角色

   1. 前往 Google Cloud 控制台的「IAM」頁面。

      [前往「IAM」頁面](https://console.cloud.google.com/projectselector/iam-admin/iam?supportedpurview=project&hl=zh-tw)
   2. 選取專案。
   3. 按一下person\_add「Grant access」(授予存取權)。
   4. 在「New principals」(新增主體) 欄位中，輸入您的使用者 ID。
      這通常是指 Google 帳戶的電子郵件地址。
   5. 按一下「Select a role」(選取角色)，然後搜尋角色。
   6. 如要授予其他角色，請按一下add「Add another role」(新增其他角色)，然後新增其他角色。
   7. 按一下「Save」(儲存)。

### gcloud

- 登入 Google Cloud 帳戶。如果您未曾使用過 Google Cloud，歡迎[建立帳戶](https://console.cloud.google.com/freetrial?hl=zh-tw)，親自體驗實際使用我們產品的成效。新客戶還能獲得價值 $300 美元的免費抵免額，用於執行、測試及部署工作負載。
- [安裝](https://docs.cloud.google.com/sdk/docs/install?hl=zh-tw) Google Cloud CLI。
- 如果採用外部識別資訊提供者 (IdP)，必須先[使用聯合身分登入 gcloud CLI](https://docs.cloud.google.com/iam/docs/workforce-log-in-gcloud?hl=zh-tw)。
- 執行下列指令，[初始化](https://docs.cloud.google.com/sdk/docs/initializing?hl=zh-tw) gcloud CLI：

  ```
  gcloud init
  ```
- [建立或選取 Google Cloud 專案](https://cloud.google.com/resource-manager/docs/creating-managing-projects?hl=zh-tw)。

  **選取或建立專案所需的角色**

  * **選取專案**：選取專案時，不需具備特定 IAM 角色，只要您在專案中獲派角色，即可選取該專案。
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
- 啟用 BigQuery 和 Translation API (如果尚未啟用)：

  **啟用 API 所需的角色**

  如要啟用 API，您必須具備 `serviceusage.services.enable` 權限。如果您建立了專案，可能已透過「擁有者」角色 (`roles/owner`) 取得這項權限。否則，您可以透過「Service Usage 管理員」角色 (`roles/serviceusage.serviceUsageAdmin`) 取得這項權限。[瞭解如何授予角色](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)。

  ```
  gcloud services enable bigquery.googleapis.com translate.googleapis.com
  ```

- [安裝](https://docs.cloud.google.com/sdk/docs/install?hl=zh-tw) Google Cloud CLI。
- 如果採用外部識別資訊提供者 (IdP)，必須先[使用聯合身分登入 gcloud CLI](https://docs.cloud.google.com/iam/docs/workforce-log-in-gcloud?hl=zh-tw)。
- 執行下列指令，[初始化](https://docs.cloud.google.com/sdk/docs/initializing?hl=zh-tw) gcloud CLI：

  ```
  gcloud init
  ```
- [建立或選取 Google Cloud 專案](https://cloud.google.com/resource-manager/docs/creating-managing-projects?hl=zh-tw)。

  **選取或建立專案所需的角色**

  * **選取專案**：選取專案時，不需具備特定 IAM 角色，只要您在專案中獲派角色，即可選取該專案。
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
- 啟用 BigQuery 和 Translation API (如果尚未啟用)：

  **啟用 API 所需的角色**

  如要啟用 API，您必須具備 `serviceusage.services.enable` 權限。如果您建立了專案，可能已透過「擁有者」角色 (`roles/owner`) 取得這項權限。否則，您可以透過「Service Usage 管理員」角色 (`roles/serviceusage.serviceUsageAdmin`) 取得這項權限。[瞭解如何授予角色](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)。

  ```
  gcloud services enable bigquery.googleapis.com translate.googleapis.com
  ```

1. 將角色授予使用者帳戶。針對下列各個 IAM 角色執行下列指令一次：`roles/bigquery.dataEditor,
   roles/bigquery.jobUser,
   roles/cloudtranslate.user`

   ```
   gcloud projects add-iam-policy-binding PROJECT_ID --member="user:USER_IDENTIFIER" --role=ROLE
   ```

   更改下列內容：

   * `PROJECT_ID`：專案 ID。
   * `USER_IDENTIFIER`：使用者帳戶的 ID。 例如：`myemail@example.com`。
   * `ROLE`：您授予使用者帳戶的 IAM 角色。

## 建立資料集

如要建立 BigQuery 資料集，請選取下列其中一個選項：

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。

   如果沒有看到左側窗格，請按一下 last\_page「Expand left pane」(展開左側窗格)，開啟窗格。
3. 在「Explorer」中展開專案，然後點選「資料集」。
4. 在「Datasets」(資料集) 頁面，按一下add「Create dataset」(建立資料集)。
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

## 建立範例資料表

使用 [`CREATE TABLE` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#create_table_statement)，在 `bqml_tutorial` 資料集中建立多語言顧客意見回饋資料表：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中執行下列陳述式：

   ```
   CREATE OR REPLACE TABLE `bqml_tutorial.customer_feedback` AS (
     SELECT
       *
     FROM
       UNNEST(
         [
           STRUCT<feedback_id INT64, feedback_text STRING>(
             1, 'El servicio de entrega fue rápido y confiable.'),
           (2, 'Je suis très satisfait de la qualité de ce produit.'),
           (3, 'Die Benutzeroberfläche der App ist sehr übersichtlich.'),
           (4, 'O suporte ao cliente resolveu meu problema com rapidez.')
         ])
   );
   ```

## 翻譯多語言文字

使用 [`AI.TRANSLATE` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-ai-translate?hl=zh-tw)將顧客意見回饋翻譯成英文 (`en`)。如果省略 `source_language` 引數，Cloud Translation API 會自動偵測每一列的原文語言，並使用預設的[神經機器翻譯 (NMT)](https://docs.cloud.google.com/translate/docs/advanced/nmt-model?hl=zh-tw) 模型翻譯文字：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中執行下列陳述式，將意見回饋翻譯成英文：

   ```
   SELECT
     feedback_id,
     feedback_text,
     AI.TRANSLATE(feedback_text, 'en') AS translated_text
   FROM
     `bqml_tutorial.customer_feedback`;
   ```

   如需有效的譯文語言代碼清單，請參閱「[支援的語言](https://docs.cloud.google.com/translate/docs/languages?hl=zh-tw)」。

   輸出結果會與下列內容相似：

   ```
   +-------------+-----------------------------+-----------------------------+
   | feedback_id | feedback_text               | translated_text             |
   +-------------+-----------------------------+-----------------------------+
   | 1           | El servicio de entrega fue  | The delivery service was    |
   |             | rápido y confiable.         | fast and reliable.          |
   +-------------+-----------------------------+-----------------------------+
   | 2           | Je suis très satisfait de   | I am very satisfied with    |
   |             | la qualité de ce produit.   | the quality of this         |
   |             |                             | product.                    |
   +-------------+-----------------------------+-----------------------------+
   | 3           | Die Benutzeroberfläche der  | The app's user interface is |
   |             | App ist sehr übersichtlich. | very clear.                 |
   +-------------+-----------------------------+-----------------------------+
   | 4           | O suporte ao cliente        | Customer support resolved   |
   |             | resolveu meu problema com   | my issue quickly.           |
   |             | rapidez.                    |                             |
   +-------------+-----------------------------+-----------------------------+
   ```

## 傳回翻譯詳細資料和偵測到的語言

處理多個區域的文字時，您可能需要記錄偵測到的來源語言和各項翻譯，或檢查每列是否有錯誤。在 [`AI.TRANSLATE` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-ai-translate?hl=zh-tw)中設定 `return_details => TRUE`，傳回包含翻譯文字、執行狀態和 API 回應中繼資料的 `STRUCT` 值：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中執行下列陳述式，擷取偵測到的語言代碼、翻譯文字和各列的狀態：

   ```
   WITH
     translations AS (
       SELECT
         feedback_id,
         AI.TRANSLATE(
           feedback_text,
           'en',
           return_details => TRUE) AS translation
       FROM
         `bqml_tutorial.customer_feedback`
     )
   SELECT
     feedback_id,
     STRING(translation.details.detected_language_code) AS detected_language,
     translation.result AS translated_text,
     translation.status
   FROM
     translations;
   ```

   輸出結果會與下列內容相似：

   ```
   +-------------+-------------------+-----------------------------+--------+
   | feedback_id | detected_language | translated_text             | status |
   +-------------+-------------------+-----------------------------+--------+
   | 1           | es                | The delivery service was    | OK     |
   |             |                   | fast and reliable.          |        |
   +-------------+-------------------+-----------------------------+--------+
   | 2           | fr                | I am very satisfied with    | OK     |
   |             |                   | the quality of this         |        |
   |             |                   | product.                    |        |
   +-------------+-------------------+-----------------------------+--------+
   | 3           | de                | The app's user interface is | OK     |
   |             |                   | very clear.                 |        |
   +-------------+-------------------+-----------------------------+--------+
   | 4           | pt                | Customer support resolved   | OK     |
   |             |                   | my issue quickly.           |        |
   +-------------+-------------------+-----------------------------+--------+
   ```

   `return_details` 設為 `TRUE` 時，傳回的 `STRUCT` 包含下列欄位：

   * `result`：包含翻譯文字的 `STRING` 值，如果發生錯誤，則為 `NULL`。
   * `status`：`STRING` 值，在作業成功時包含 `OK`，或在發生錯誤時包含錯誤訊息。
   * `details`：`JSON` 值，包含該列的 Cloud Translation API 回應，包括自動偵測到來源語言時的 `detected_language_code`，或發生錯誤時的錯誤詳細資料。

## 使用翻譯 LLM 翻譯文字

如果文字包含非正式用語、俚語或複雜情緒 (例如顧客或電影評論)，請在 [`AI.TRANSLATE` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-ai-translate?hl=zh-tw)中設定 `model => 'translation-llm'`，改用 [Translation LLM](https://docs.cloud.google.com/translate/docs/translation-llm?hl=zh-tw) 模型，而非預設的 NMT 模型。如果您知道輸入資料欄的語言，也可以指定 `source_language` 引數：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中執行下列陳述式，將公開資料集中的五則英文電影評論翻譯成西班牙文 (`es`)：

   ```
   SELECT
     review,
     AI.TRANSLATE(
       review,
       'es',
       source_language => 'en',
       model => 'translation-llm') AS translated_review
   FROM
     `bigquery-public-data.imdb.reviews`
   LIMIT 5;
   ```

   輸出結果會與下列內容相似：

   ```
   +------------------------------------+------------------------------------+
   | review                             | translated_review                  |
   +------------------------------------+------------------------------------+
   | Once again Mr. Costner has dragged | Una vez más, el Sr. Costner ha     |
   | out a movie for far longer than... | alargado una película mucho más... |
   +------------------------------------+------------------------------------+
   | This movie is amazing because the  | Esta película es increíble porque  |
   | fact that real people portray...   | las personas reales se...          |
   +------------------------------------+------------------------------------+
   | ...                                | ...                                |
   +------------------------------------+------------------------------------+
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

如要重複使用專案，請刪除您為本教學課程建立的資料集：

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 刪除 `bqml_tutorial` 資料集。刪除資料集也會一併刪除 `customer_feedback` 資料表：

   1. 在「Explorer」窗格中展開專案，然後按一下「Datasets」(資料集)。
   2. 在「Datasets」(資料集) 清單中，點選 `bqml_tutorial` 資料集。
   3. 在詳細資料窗格中，按一下「delete 刪除」。
   4. 在「Delete dataset」(刪除資料集) 對話方塊中，按一下「Delete」(刪除)。

### gcloud

* 刪除 `bqml_tutorial` 資料集和 `customer_feedback` 資料表：

```
bq rm --dataset --recursive bqml_tutorial
```

## 後續步驟

* 進一步瞭解 [`AI.TRANSLATE` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-ai-translate?hl=zh-tw)。
* 進一步瞭解[翻譯 LLM](https://docs.cloud.google.com/translate/docs/translation-llm?hl=zh-tw) 和[神經機器翻譯](https://docs.cloud.google.com/translate/docs/advanced/nmt-model?hl=zh-tw)模型。
* 請參閱「[選擇自然語言處理函式](https://docs.cloud.google.com/bigquery/docs/choose-ml-text-function?hl=zh-tw)」，比較文字分析選項。
* 進一步瞭解 [BigQuery 的生成式 AI](https://docs.cloud.google.com/bigquery/docs/generative-ai-overview?hl=zh-tw)。
* 如要查看支援的 SQL 陳述式和函式，請參閱「[生成式 AI 模型的端對端使用者歷程](https://docs.cloud.google.com/bigquery/docs/e2e-journey-genai?hl=zh-tw)」。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-11-13 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-11-13 (世界標準時間)。"],[],[]]