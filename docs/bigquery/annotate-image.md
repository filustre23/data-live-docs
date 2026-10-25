Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見

# 使用 ML.ANNOTATE\_IMAGE 函式為圖片加上註解 透過集合功能整理內容 你可以依據偏好儲存及分類內容。

本教學課程說明如何使用 [`ML.ANNOTATE_IMAGE` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-annotate-image?hl=zh-tw)，從非結構化圖片資料擷取洞察資訊。處理大量圖片存放區時，您可能需要自動分類檔案、偵測特定物件，或擷取圖片屬性，讓資料集可供搜尋。建立連結至 Cloud Vision API 的 BigQuery ML [遠端模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model-service?hl=zh-tw)，即可直接在 BigQuery [物件資料表](https://docs.cloud.google.com/bigquery/docs/object-table-introduction?hl=zh-tw)上使用標準 SQL 執行這些圖片分析工作，不必移動檔案或建構複雜的資料管道。

## 目標

* 建立資料集和資源連線。
* 為儲存在 Cloud Storage 中的圖片檔案建立物件資料表。
* 建立連線至 Cloud Vision API 的遠端模型。
* 使用 `ML.ANNOTATE_IMAGE` 函式為圖片加上註解。

## 費用

在本文件中，您將使用下列 Google Cloud計費元件：

* [BigQuery](https://cloud.google.com/bigquery/pricing?hl=zh-tw)
* [Cloud Vision API](https://cloud.google.com/vision/pricing?hl=zh-tw)

如要根據預測用量估算費用，請使用 [Pricing Calculator](https://docs.cloud.google.com/products/calculator?hl=zh-tw)。

初次使用 Google Cloud 的使用者可能符合[免費試用期](https://docs.cloud.google.com/free?hl=zh-tw)資格。

## 事前準備

- 登入 Google Cloud 帳戶。如果您是 Google Cloud新手，歡迎[建立帳戶](https://console.cloud.google.com/freetrial?hl=zh-tw)，親自體驗產品的實際應用成效。新客戶還能獲得價值 $300 美元的免費抵免額，能用於執行、測試及部署工作負載。
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
- Enable the BigQuery, BigQuery Connection API, and Cloud Vision API APIs, if any are not already enabled.

  **Roles required to enable APIs**

  To enable APIs, you need the `serviceusage.services.enable` permission. If you
  created the project, then you likely already have this permission through the
  Owner role (`roles/owner`). Otherwise, you can get this permission through the
  Service Usage Admin role (`roles/serviceusage.serviceUsageAdmin`).
  [Learn how to grant roles](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw).

  [Enable the APIs](https://console.cloud.google.com/apis/enableflow?apiid=bigquery.googleapis.com%2Cbigqueryconnection.googleapis.com%2Cvision.googleapis.com&hl=zh-tw)

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
- Enable the BigQuery, BigQuery Connection API, and Cloud Vision API APIs, if any are not already enabled.

  **Roles required to enable APIs**

  To enable APIs, you need the `serviceusage.services.enable` permission. If you
  created the project, then you likely already have this permission through the
  Owner role (`roles/owner`). Otherwise, you can get this permission through the
  Service Usage Admin role (`roles/serviceusage.serviceUsageAdmin`).
  [Learn how to grant roles](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw).

  [Enable the APIs](https://console.cloud.google.com/apis/enableflow?apiid=bigquery.googleapis.com%2Cbigqueryconnection.googleapis.com%2Cvision.googleapis.com&hl=zh-tw)

### 必要的角色

如要取得完成本教學課程所需的權限，請要求管理員在專案中授予您下列 IAM 角色：

* 建立及使用 BigQuery 資料集、資料表和模型：
  [BigQuery 資料編輯器](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.dataEditor)  (`roles/bigquery.dataEditor`)
* 建立、委派及使用 BigQuery 連線：
  [BigQuery 連線管理員](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.connectionAdmin)  (`roles/bigquery.connectionAdmin`)
* 將權限授予連線的服務帳戶：
  「專案 IAM 管理員」 (`roles/resourcemanager.projectIamAdmin`)
* 建立 BigQuery 工作：
  [BigQuery 工作使用者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.jobUser)  (`roles/bigquery.jobUser`)

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
   * 在「資料位置」部分，選取「美國」。

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

## 建立物件資料表

[建立名為 `my_object_table` 的物件資料表](https://docs.cloud.google.com/bigquery/docs/object-tables?hl=zh-tw)
，其中包含圖片內容。有了物件資料表，您就能分析圖片，不必將圖片從 Cloud Storage 移出。

物件資料表使用的 Cloud Storage bucket 應與您打算建立模型並呼叫 `ML.ANNOTATE_IMAGE` 函式的專案位於同一位置。如要呼叫與物件資料表所用 Cloud Storage bucket 所在專案不同的 `ML.ANNOTATE_IMAGE` 函式，請[在 bucket 層級授予 Storage 管理員角色](https://docs.cloud.google.com/storage/docs/access-control/using-iam-permissions?hl=zh-tw#bucket-add)。

## 建立模型

使用 `CLOUD_AI_VISION_V1` 建立名為 `my_model` 的遠端模型 [`REMOTE_SERVICE_TYPE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model-service?hl=zh-tw#remote_service_type)：

```
CREATE OR REPLACE MODEL
`PROJECT_ID.bqml_tutorial.my_model`
REMOTE WITH CONNECTION DEFAULT
OPTIONS (REMOTE_SERVICE_TYPE = 'CLOUD_AI_VISION_V1');
```

將 `PROJECT_ID` 替換為專案 ID。

## 為圖片加註

使用 `ML.ANNOTATE_IMAGE` 函式和偏好的[功能](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-annotate-image?hl=zh-tw#syntax)，在物件表格中為圖片加上註解。

1. 如要標示圖片中顯示的項目，請搭配 [`label_detection`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-annotate-image?hl=zh-tw#syntax) 功能使用 `ML.ANNOTATE_IMAGE` 函式：

   ```
   SELECT *
   FROM ML.ANNOTATE_IMAGE(
   MODEL `PROJECT_ID.bqml_tutorial.my_model`,
   TABLE `PROJECT_ID.bqml_tutorial.my_object_table`,
   STRUCT(['label_detection'] AS vision_features)
   );
   ```

   將 `PROJECT_ID` 替換為專案 ID。
2. 如要偵測圖片中顯示的任何臉部，並傳回圖片屬性 (例如主要顏色)，請搭配使用 `ML.ANNOTATE_IMAGE` 函式與 [`face_detection`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-annotate-image?hl=zh-tw#syntax) 和 [`image_properties`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-annotate-image?hl=zh-tw#syntax) 功能：

   ```
   SELECT *
   FROM ML.ANNOTATE_IMAGE(
   MODEL `PROJECT_ID.bqml_tutorial.my_model`,
   TABLE `PROJECT_ID.bqml_tutorial.my_object_table`,
   STRUCT(['face_detection', 'image_properties'] AS vision_features)
   );
   ```

   將 `PROJECT_ID` 替換為專案 ID。

## 清除所用資源

為避免因為本教學課程所用資源，導致系統向 Google Cloud 收取費用，請刪除含有相關資源的專案，或者保留專案但刪除個別資源。

### 刪除專案

### 控制台

**警告**：刪除專案會出現以下結果：

* **專案中的所有內容都會遭到刪除。**如果使用現有專案來進行本文中的任務，刪除專案將一併移除當中已完成的其他任務'。
* **自訂專案 ID 會消失。**當您之前建立這個專案時，可能建立了想要在日後使用的自訂專案 ID。如要保留使用該專案 ID 的網址 (例如 `appspot.com` 網址)，請刪除在該專案中選取的資源，而不是刪除整個專案。

如果打算探索多種架構、教學課程或快速入門導覽課程，重複使用專案可避免超出專案配額限制。

1. 前往 Google Cloud 控制台的「Manage resources」(管理資源) 頁面。

   [前往「Manage resources」(管理資源)](https://console.cloud.google.com/iam-admin/projects?hl=zh-tw)
2. 在專案清單中選取要刪除的專案，然後點選「Delete」(刪除)。
3. 在對話方塊中輸入專案 ID，然後按一下 [Shut down] (關閉) 以刪除專案。

### gcloud

**警告**：刪除專案會出現以下結果：

* **專案中的所有內容都會遭到刪除。**如果使用現有專案來進行本文中的任務，刪除專案將一併移除當中已完成的其他任務'。
* **自訂專案 ID 會消失。**當您之前建立這個專案時，可能建立了想要在日後使用的自訂專案 ID。如要保留使用該專案 ID 的網址 (例如 `appspot.com` 網址)，請刪除在該專案中選取的資源，而不是刪除整個專案。

如果打算探索多種架構、教學課程或快速入門導覽課程，重複使用專案可避免超出專案配額限制。

刪除 Google Cloud 專案：

```
gcloud projects delete PROJECT_ID
```

### 刪除個別資源

如果您打算保留用於本教學課程的專案，可以刪除您建立的個別資源，以免產生額外費用：

1. **刪除資料集：**刪除資料集也會移除遠端模型，以及您在其中建立的物件資料表。

   * 前往 Google Cloud 控制台的「BigQuery Studio」。
   * 在「Explorer」窗格中展開專案，然後選取您建立的資料集。
   * 按一下 more\_vert「View actions」(查看動作)，然後按一下「Delete」(刪除)。
   * 在對話方塊中輸入 `delete`，然後按一下「刪除」。
2. **刪除連結：**

   * 在「Explorer」窗格中展開專案名稱，然後按一下「Connections」。
   * 點選所建立連結旁的「查看動作」more\_vert圖示，然後選取「刪除」。
   * 在對話方塊中，按一下「刪除」確認。

## 後續步驟

* 如要進一步瞭解 BigQuery ML 中的模型推論，請參閱「[模型推論總覽](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/inference-overview?hl=zh-tw)」。
* 如要進一步瞭解如何使用 Cloud AI API 執行 AI 任務，請參閱「[AI 應用程式總覽](https://docs.cloud.google.com/bigquery/docs/ai-application-overview?hl=zh-tw)」。
* 如要瞭解生成式 AI 模型支援的 SQL 陳述式和函式，請參閱「[生成式 AI 模型端對端使用者歷程](https://docs.cloud.google.com/bigquery/docs/e2e-journey-genai?hl=zh-tw)」。
* 試用「[Unstructured data analytics with BigQuery ML and Gemini Enterprise Agent Platform pre-trained models](https://github.com/GoogleCloudPlatform/vertex-ai-samples/blob/main/notebooks/community/bigquery_ml/bq_ml_with_vision_translation_nlp.ipynb)」筆記本。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-10-24 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-10-24 (世界標準時間)。"],[],[]]