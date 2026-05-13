Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見

# 使用 Vertex AI 上的遠端模型進行預測 透過集合功能整理內容 你可以依據偏好儲存及分類內容。

在本教學課程中，您將 Vertex AI 端點註冊為 BigQuery 中的遠端模型。接著，您可以使用 [`ML.PREDICT` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-predict?hl=zh-tw)，透過遠端模型進行預測。

當模型過大而無法匯入 BigQuery 時，您可以使用遠端模型。如要針對線上、批次和微批次用途使用單一推論點，這項功能也十分實用。

**注意：** 如要查看使用 BigQuery 筆記本中 Python 的教學課程版本，請參閱 GitHub 中的 [BQML 遠端模型教學課程](https://github.com/GoogleCloudPlatform/bigquery-ml-utils/blob/master/notebooks/bqml-inference-remote-model-tutorial.md)。

## 目標

* 將預先訓練的 TensorFlow 模型匯入 Vertex AI Model Registry。
* 將模型部署至 Vertex AI 端點。
* 建立 Cloud 資源連結。
* 使用 `CREATE MODEL` 陳述式在 BigQuery 中建立遠端模型。
* 使用 `ML.PREDICT` 函式，透過遠端模型進行預測。

## 費用

在本文件中，您會使用下列 Google Cloud的計費元件：

* [BigQuery](https://cloud.google.com/bigquery/pricing?hl=zh-tw)
* [BigQuery ML](https://cloud.google.com/bigquery/pricing?hl=zh-tw#bqml)
* [Vertex AI](https://docs.cloud.google.com/vertex-ai/pricing?hl=zh-tw)

如要根據預測用量估算費用，請使用 [Pricing Calculator](https://docs.cloud.google.com/products/calculator?hl=zh-tw)。

初次使用 Google Cloud 的使用者可能符合[免費試用期](https://docs.cloud.google.com/free?hl=zh-tw)資格。

完成本文所述工作後，您可以刪除建立的資源，避免繼續計費，詳情請參閱「[清除所用資源](#clean-up)」。

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

1. [確認專案已啟用計費功能 Google Cloud](https://docs.cloud.google.com/billing/docs/how-to/verify-billing-enabled?hl=zh-tw#confirm_billing_is_enabled_on_a_project) 。
2. 啟用 BigQuery、Vertex AI、Cloud Storage 和 BigQuery Connection API。

   **啟用 API 時所需的角色**

   如要啟用 API，您需要服務使用情形管理員 IAM 角色 (`roles/serviceusage.serviceUsageAdmin`)，其中包含 `serviceusage.services.enable` 權限。[瞭解如何授予角色](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)。

   [啟用 API](https://console.cloud.google.com/flows/enableapi?apiid=bigquery.googleapis.com%2Caiplatform.googleapis.com%2Cstorage-component.googleapis.com%2Cbigqueryconnection.googleapis.com&hl=zh-tw)
3. 請確認您具備[必要權限](#required_permissions)，可執行本文件中的工作。

### 必要的角色

如果您建立新專案，您就是專案擁有者，並會獲得完成本教學課程所需的所有 IAM 權限。

如果您使用現有專案，請執行下列操作。

請確認您在專案中具備下列角色：

* [BigQuery Studio 管理員](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.studioAdmin) (`roles/bigquery.studioAdmin`)
* [Vertex AI 使用者](https://docs.cloud.google.com/iam/docs/roles-permissions/aiplatform?hl=zh-tw#aiplatform.user) (`roles/aiplatform.user`)
* [BigQuery Connection 管理員](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.connectionAdmin) (`roles/bigquery.connectionAdmin`)

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

如要進一步瞭解 BigQuery 中的 IAM 權限，請參閱「[BigQuery 權限](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bq-permissions)」。

## 將模型匯入 Vertex AI Model Registry

在本教學課程中，您會使用 Cloud Storage 中 `gs://cloud-samples-data/bigquery/ml/remote_model_tutorial/` 提供的預先訓練 TensorFlow 模型。Cloud Storage bucket 位於 `US` 多區域位置。

模型是名為 `saved_model.pb` 的 TensorFlow 模型。這是自訂情緒分析模型，以純文字 IMDB 電影評論資料微調 BERT 模型而建立。模型會使用電影評論的文字輸入內容，並傳回介於 0 到 1 之間的情緒分數。將模型匯入 Model Registry 時，您會使用預先建構的 TensorFlow 容器。

**注意：** 如需建立範例模型的教學課程，請參閱 TensorFlow 說明文件中的「[使用 BERT 分類文字](https://www.tensorflow.org/text/tutorials/classify_text_with_bert?hl=zh-tw)」。

請按照下列步驟匯入模型。

1. 前往 Google Cloud 控制台的 Vertex AI「Model Registry」頁面。

   [前往「Model Registry」](https://console.cloud.google.com/vertex-ai/models?hl=zh-tw)
2. 按一下「匯入」。
3. 在「步驟一：名稱和區域」中，執行下列操作：

   1. 選取「匯入為新模型」。
   2. 在「Name」(名稱) 中輸入 `bert_sentiment`。
   3. 在「說明」中輸入 `BQML tutorial model`。
   4. 在「區域」中選取 `us-central1`。您必須選擇美國境內的區域，因為 Cloud Storage bucket 位於`US`多區域位置。
   5. 按一下「繼續」。
4. 如要完成**步驟二：模型設定**，請執行下列操作：

   1. 選取「將模型構件匯入新的預建容器」。
   2. 在「預先建構的容器設定」部分，執行下列操作：

      1. 在**「Model framework」(模型架構)** 中選擇「TensorFlow」。
      2. 在「Model framework version」(模型架構版本) 中選擇「2.15」。
      3. 在「Accelerator type」(加速器類型) 部分，選擇「GPU」。
      4. 在「Model artifact location」(模型構件位置) 中，輸入 `gs://cloud-samples-data/bigquery/ml/remote_model_tutorial/`。
      5. 其餘選項均保留預設值，然後按一下「匯入」。

匯入完成後，模型會顯示在「Model Registry」(模型登錄) 頁面。

## 將模型部署至 Vertex AI 端點

請按照下列步驟將模型部署至端點。

1. 在 Google Cloud 控制台中，前往 Vertex AI 的「Model Registry」頁面。

   [前往「Model Registry」](https://console.cloud.google.com/vertex-ai/models?hl=zh-tw)
2. 在「Name」(名稱) 欄中，按一下 **`bert_sentiment`**。
3. 按一下「Deploy & Test」(部署及測試) 分頁標籤。
4. 按一下「Deploy to endpoint」(部署至端點)。
5. 如要完成步驟一「**定義端點**」，請按照下列步驟操作：

   1. 按一下「建立新端點」。
   2. 在「端點名稱」部分，輸入 **`bert sentiment endpoint`**。
   3. 其餘設定均保留預設值，然後點選「繼續」。
6. 在步驟二「模型設定」中，請執行下列操作：

   1. 在「Compute settings」(運算設定) 部分，為「Minimum number of compute nodes」(運算節點數量下限) 輸入 `1`。這是模型隨時可用的節點數量。

      **注意：** 在正式版中，您應設定運算節點數量上限。這個選項會開啟 Vertex AI 的自動調度資源功能，讓端點在 BigQuery 資料表含有大量資料列時，處理更多要求。
   2. 在「進階縮放選項」部分，針對「機型」選擇「標準 (n1-standard-2)」。由於您在匯入模型時選擇 GPU 做為加速器類型，因此選擇機型後，系統會自動設定加速器類型和加速器數量。
   3. 保留其餘預設值，然後按一下「部署」。

      模型部署到端點後，狀態會變更為 `Active`。
   4. 複製「ID」欄中的數字端點 ID，以及「Region」欄中的值。稍後會用到。

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

## 建立 BigQuery Cloud 資源連結

您必須建立 Cloud 資源連結，才能連至 Vertex AI 端點。

### 控制台

1. 前往「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。

   如果沒有看到左側窗格，請按一下 last\_page「Expand left pane」(展開左側窗格)，開啟窗格。
3. 在「Explorer」窗格中，點選「新增資料」add。

   「新增資料」對話方塊隨即開啟。
4. 在「Filter By」(依據篩選) 窗格的「Data Source Type」(資料來源類型) 專區中，選取「Databases」(資料庫)。

   或者，您也可以在「Search for data sources」(搜尋資料來源) 欄位中輸入 `Vertex AI`。
5. 在「精選資料來源」部分，點選「Vertex AI」。
6. 按一下「Vertex AI Models: BigQuery Federation」解決方案資訊卡。
7. 在「連線類型」清單中，選取「Vertex AI 遠端模型、遠端函式和 BigLake (Cloud 資源)」。
8. 在「連線 ID」欄位中輸入 `bqml_tutorial`。
9. 確認已選取「多區域 - 美國」。
10. 點選「建立連線」。
11. 按一下視窗底部的「前往連線」。或者，在「Explorer」窗格中，依序點選「Connections」和 **`us.bqml_tutorial`**。
12. 在「連線資訊」窗格中，複製服務帳戶 ID。設定連線的權限時，您需要這個 ID。建立連線資源時，BigQuery 會建立專屬的系統服務帳戶，並將其與連線建立關聯。

### bq

1. 建立連線：

   ```
   bq mk --connection --location=US --project_id=PROJECT_ID \
       --connection_type=CLOUD_RESOURCE bqml_tutorial
   ```

   將 `PROJECT_ID` 替換為Google Cloud 專案 ID。`--project_id` 參數會覆寫預設專案。

   建立連線資源時，BigQuery 會建立專屬的系統服務帳戶，並將其與連線建立關聯。

   **疑難排解**：如果收到下列連線錯誤訊息，請[更新 Google Cloud SDK](https://docs.cloud.google.com/sdk/docs/quickstart?hl=zh-tw)：

   ```
   Flags parsing error: flag --connection_type=CLOUD_RESOURCE: value should be one of...
   ```
2. 擷取並複製服務帳戶 ID，以供後續步驟使用：

   ```
   bq show --connection PROJECT_ID.us.bqml_tutorial
   ```

   輸出結果會與下列內容相似：

   ```
   name                          properties
   1234.REGION.CONNECTION_ID {"serviceAccountId": "connection-1234-9u56h9@gcp-sa-bigquery-condel.iam.gserviceaccount.com"}
   ```

## 設定連線存取權

為 Cloud 資源連線的服務帳戶授予 Vertex AI 使用者角色。您必須在建立遠端模型端點的專案中授予這個角色。

**注意：** 如果連線位於不同專案中，系統會傳回以下錯誤：
`bqcx-1234567890-xxxx@gcp-sa-bigquery-condel.iam.gserviceaccount.com does not have the permission to access
resource`。

如要授予角色，請按照下列步驟操作：

1. 前往「IAM & Admin」(IAM 與管理) 頁面。

   [前往「IAM & Admin」(IAM 與管理)](https://console.cloud.google.com/project/_/iam-admin?hl=zh-tw)
2. 按一下 person\_add「授予存取權」。
3. 在「新增主體」欄位，輸入先前複製的 Cloud 資源連線服務帳戶 ID。
4. 在「選取角色」欄位中，選擇「Vertex AI」，然後選取「Vertex AI 使用者」。
5. 按一下 [儲存]。

## 建立 BigQuery ML 遠端模型

您可以使用 `REMOTE WITH CONNECTION` 子句搭配 `CREATE MODEL` 陳述式，建立 BigQuery ML 遠端模型。如要進一步瞭解 `CREATE MODEL` 陳述式，請參閱「[透過自訂模型建立遠端模型的 CREATE MODEL 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model-https?hl=zh-tw)」。

在 `US` 多區域位置建立模型。在 BigQuery 多區域 (`US`、`EU`) 資料集中，您只能建立連線至端點的遠端模型，該端點部署在相同多區域位置 (`US`、`EU`) 內的區域。

建立遠端模型時，您需要[將模型部署至 Vertex AI](#deploy-model) 時產生的端點 ID。此外，輸入和輸出欄位名稱與類型必須與 Vertex AI 模型的輸入和輸出完全相同。在這個範例中，輸入內容是文字 `STRING`，輸出內容則是 `FLOAT64` 類型的 `ARRAY`。

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 如要**建立新項目**，請按一下「SQL 查詢」。
3. 在查詢編輯器中輸入這個 `CREATE MODEL` 陳述式，然後按一下「執行」：

   ```
   CREATE OR REPLACE MODEL `PROJECT_ID.bqml_tutorial.bert_sentiment`
   INPUT (text STRING)
   OUTPUT(scores ARRAY<FLOAT64>)
   REMOTE WITH CONNECTION `PROJECT_ID.us.bqml_tutorial`
   OPTIONS(ENDPOINT = 'https://us-central1-aiplatform.googleapis.com/v1/projects/PROJECT_ID/locations/us-central1/endpoints/ENDPOINT_ID')
   ```

   更改下列內容：

   * PROJECT\_ID：您的專案名稱。
   * ENDPOINT\_ID：先前複製的端點 ID。

   作業完成後，畫面上會顯示類似如下的訊息：`Successfully created model named bert_sentiment`。

   新模型會顯示在「資源」面板中。模型會以模型圖示

   在「Resources」(資源) 面板中選取新模型，「Query editor」(查詢編輯器) 下方就會顯示該模型的相關資訊。

### bq

1. 輸入下列 `CREATE MODEL` 陳述式，建立遠端模型：

   ```
   bq query --use_legacy_sql=false \
   "CREATE OR REPLACE MODEL `PROJECT_ID.bqml_tutorial.bert_sentiment`
   INPUT (text STRING)
   OUTPUT(scores ARRAY<FLOAT64>)
   REMOTE WITH CONNECTION `PROJECT_ID.us.bqml_tutorial`
   OPTIONS(ENDPOINT = 'https://us-central1-aiplatform.googleapis.com/v1/projects/PROJECT_ID/locations/us-central1/endpoints/ENDPOINT_ID')"
   ```

   更改下列內容：

   * PROJECT\_ID：您的專案名稱。
   * ENDPOINT\_ID：先前複製的端點 ID。
2. 建立模型後，請確認模型是否顯示在資料集中：

   ```
   bq ls -m bqml_tutorial
   ```

   輸出結果會與下列內容相似：

   ```
   Id               Model Type   Labels    Creation Time
   ---------------- ------------ -------- -----------------
   bert_sentiment                         28 Jan 17:39:43
   ```

## 使用 `ML.PREDICT` 取得預測結果

您可以使用 `ML.PREDICT` 函式，從遠端模型取得情緒預測結果。輸入內容是文字資料欄 (`review`)，內含 `bigquery-public-data.imdb.reviews` 資料表的電影評論。

在本例中，我們選取了 10,000 筆記錄，並傳送進行預測。遠端模型預設要求批量大小為 128 個執行個體。

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在「建立新項目」部分，按一下「SQL 查詢」。
3. 在查詢編輯器中輸入使用 `ML.PREDICT` 函式的查詢，然後按一下「執行」。

   ```
   SELECT *
   FROM ML.PREDICT (
       MODEL `PROJECT_ID.bqml_tutorial.bert_sentiment`,
       (
           SELECT review as text
           FROM `bigquery-public-data.imdb.reviews`
           LIMIT 10000
       )
   )
   ```

   查詢結果應該會與下方示例類似：

### bq

輸入下列指令，執行使用 `ML.PREDICT` 的查詢。

```
bq query --use_legacy_sql=false \
'SELECT *
FROM ML.PREDICT (
MODEL `PROJECT_ID.bqml_tutorial.bert_sentiment`,
  (
    SELECT review as text
    FROM `bigquery-public-data.imdb.reviews`
    LIMIT 10000
  )
)'
```

## 清除所用資源

為避免因為本教學課程所用資源，導致系統向 Google Cloud 收取費用，請刪除含有相關資源的專案，或者保留專案但刪除個別資源。

### 刪除專案

### 控制台

**注意**：刪除專案會造成以下結果：

* **專案中的所有內容都會遭到刪除。**如果使用現有專案來進行本文中的任務，刪除專案將一併移除當中已完成的其他任務'。
* **自訂專案 ID 會消失。**當您之前建立這個專案時，可能建立了想要在日後使用的自訂專案 ID。如要保留使用該專案 ID 的網址 (例如 `appspot.com` 網址)，請刪除在該專案中選取的資源，而不是刪除整個專案。

如果打算探索多種架構、教學課程或快速入門導覽課程，重複使用專案可避免超出專案配額限制。

1. 前往 Google Cloud 控制台的「Manage resources」(管理資源) 頁面。

   [前往「Manage resources」(管理資源)](https://console.cloud.google.com/iam-admin/projects?hl=zh-tw)
2. 在專案清單中選取要刪除的專案，然後點選「Delete」(刪除)。
3. 在對話方塊中輸入專案 ID，然後按一下 [Shut down] (關閉) 以刪除專案。

### gcloud

**注意**：刪除專案會造成以下結果：

* **專案中的所有內容都會遭到刪除。**如果使用現有專案來進行本文中的任務，刪除專案將一併移除當中已完成的其他任務'。
* **自訂專案 ID 會消失。**當您之前建立這個專案時，可能建立了想要在日後使用的自訂專案 ID。如要保留使用該專案 ID 的網址 (例如 `appspot.com` 網址)，請刪除在該專案中選取的資源，而不是刪除整個專案。

如果打算探索多種架構、教學課程或快速入門導覽課程，重複使用專案可避免超出專案配額限制。

刪除 Google Cloud 專案：

```
gcloud projects delete PROJECT_ID
```

### 刪除個別資源

或者，如要移除本教學課程中使用的個別資源，請按照下列步驟操作：

1. [刪除模型](https://docs.cloud.google.com/bigquery/docs/deleting-models?hl=zh-tw)。
2. 選用：[刪除資料集](https://docs.cloud.google.com/bigquery/docs/managing-datasets?hl=zh-tw#delete-datasets)。
3. [取消部署模型並刪除端點](https://docs.cloud.google.com/vertex-ai/docs/general/deployment?hl=zh-tw#undeploy_a_model_and_delete_the_endpoint)。
4. [從 Model Registry 刪除模型](https://docs.cloud.google.com/vertex-ai/docs/model-registry/delete-model?hl=zh-tw)。
5. [刪除 Cloud 資源連結](https://docs.cloud.google.com/bigquery/docs/working-with-connections?hl=zh-tw#delete-connections)。

## 後續步驟

* 如需 BigQuery ML 的總覽，請參閱 [BigQuery ML 中的 AI 和 ML 簡介](https://docs.cloud.google.com/bigquery/docs/bqml-introduction?hl=zh-tw)。
* 如要進一步瞭解如何使用 `CREATE MODEL` 陳述式建立遠端模型，請參閱[透過自訂模型建立遠端模型的 CREATE MODEL 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model-https?hl=zh-tw)。
* 如要進一步瞭解如何使用 BigQuery 筆記本，請參閱[筆記本簡介](https://docs.cloud.google.com/bigquery/docs/notebooks-introduction?hl=zh-tw)。
* 如要進一步瞭解 BigQuery 單一地區與多地區，請參閱「[支援的地區](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw#supported_locations)」頁面。
* 如要進一步瞭解如何在 Vertex AI Model Registry 中匯入模型，請參閱「[將模型匯入 Vertex AI](https://docs.cloud.google.com/vertex-ai/docs/model-registry/import-model?hl=zh-tw)」。
* 如要進一步瞭解 Vertex AI Model Registry 中的模型版本管理，請參閱「[使用 Model Registry 進行模型版本管理](https://docs.cloud.google.com/vertex-ai/docs/model-registry/versioning?hl=zh-tw)」。
* 如要瞭解如何使用 Vertex AI VPC Service Controls，請參閱「[搭配使用 VPC Service Controls 與 Vertex AI](https://docs.cloud.google.com/vertex-ai/docs/general/vpc-service-controls?hl=zh-tw)」。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-12 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-12 (世界標準時間)。"],[],[]]