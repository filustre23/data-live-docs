Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見

# 使用匯入的 TensorFlow 模型進行預測 透過集合功能整理內容 你可以依據偏好儲存及分類內容。

在本教學課程中，您會將 TensorFlow 模型匯入 BigQuery ML 資料集。接著，您可以使用 SQL 查詢，從匯入的模型進行預測。

## 目標

* 使用 `CREATE MODEL` 陳述式將 TensorFlow 模型匯入 BigQuery ML。
* 使用 `ML.PREDICT` 函式，透過匯入的 TensorFlow 模型進行預測。

## 費用

在本文件中，您會使用下列 Google Cloud的計費元件：

* [BigQuery](https://cloud.google.com/bigquery/pricing?hl=zh-tw)
* [BigQuery ML](https://cloud.google.com/bigquery/pricing?hl=zh-tw#bqml)

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
2. 確認已啟用 BigQuery API。

   [啟用 API](https://console.cloud.google.com/flows/enableapi?apiid=bigquery&hl=zh-tw)
3. 請確認您具備[必要權限](#required_permissions)，可執行本文件中的工作。

### 必要的角色

如果您建立新專案，您就是專案擁有者，並已獲得完成本教學課程所需的所有必要 Identity and Access Management (IAM) 權限。

如果您使用現有專案，[BigQuery Studio 管理員](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.studioAdmin) (`roles/bigquery.studioAdmin`) 角色會授予完成本教學課程所需的所有權限。

請確認您在專案中擁有下列角色：
[BigQuery Studio 管理員](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.studioAdmin) (`roles/bigquery.studioAdmin`)。

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

如要進一步瞭解 BigQuery 中的 IAM 權限，請參閱 [BigQuery 權限](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bq-permissions)。

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

## 匯入 TensorFlow 模型

下列步驟說明如何從 Cloud Storage 匯入模型。模型路徑為 `gs://cloud-training-demos/txtclass/export/exporter/1549825580/*`。匯入的模型名稱為 `imported_tf_model`。

請注意，Cloud Storage URI 的結尾是萬用字元 (`*`)。這個字元表示 BigQuery ML 應匯入與模型相關聯的所有資產。

匯入的模型為 TensorFlow 文字分類程式模型，可預測發布特定文章標題的網站。

如要將 TensorFlow 模型匯入資料集，請按照下列步驟操作。

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往 BigQuery 頁面](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 如要**建立新項目**，請按一下「SQL 查詢」。
3. 在查詢編輯器中輸入這項 `CREATE MODEL` 陳述式，然後點選「執行」。

   ```
     CREATE OR REPLACE MODEL `bqml_tutorial.imported_tf_model`
     OPTIONS (MODEL_TYPE='TENSORFLOW',
       MODEL_PATH='gs://cloud-training-demos/txtclass/export/exporter/1549825580/*')
   ```

   作業完成後，您應該會看到類似 `Successfully created model named imported_tf_model` 的訊息。
4. 新模型會顯示在「資源」面板中。模型會以模型圖示
5. 在「Resources」(資源) 面板中選取新模型，「Query editor」(查詢編輯器) 下方就會顯示該模型的相關資訊。

### bq

1. 輸入下列 `CREATE MODEL` 陳述式，從 Cloud Storage 匯入 TensorFlow 模型。

   ```
   bq query --use_legacy_sql=false \
   "CREATE OR REPLACE MODEL
     `bqml_tutorial.imported_tf_model`
   OPTIONS
     (MODEL_TYPE='TENSORFLOW',
       MODEL_PATH='gs://cloud-training-demos/txtclass/export/exporter/1549825580/*')"
   ```
2. 匯入模型後，請確認模型是否顯示在資料集中。

   ```
   bq ls -m bqml_tutorial
   ```

   輸出結果會與下列內容相似：

   ```
   tableId             Type
   ------------------- -------
   imported_tf_model   MODEL
   ```

### API

[插入新工作](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs/insert?hl=zh-tw)，並在要求主體中填入 [jobs#configuration.query](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs/query?hl=zh-tw) 屬性。

```
{
  "query": "CREATE MODEL `PROJECT_ID:bqml_tutorial.imported_tf_model` OPTIONS(MODEL_TYPE='TENSORFLOW' MODEL_PATH='gs://cloud-training-demos/txtclass/export/exporter/1549825580/*')"
}
```

將 `PROJECT_ID` 替換為您的專案和資料集名稱。

### BigQuery DataFrames

在嘗試這個範例之前，請按照[使用 BigQuery DataFrames 的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/dataframes-quickstart?hl=zh-tw)中的 BigQuery DataFrames 設定說明操作。
詳情請參閱 [BigQuery DataFrames 參考文件](https://docs.cloud.google.com/python/docs/reference/bigframes/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。
詳情請參閱「[為本機開發環境設定 ADC](https://docs.cloud.google.com/docs/authentication/set-up-adc-local-dev-environment?hl=zh-tw)」。

使用 `TensorFlowModel` 物件匯入模型。

```
import bigframes
from bigframes.ml.imported import TensorFlowModel

bigframes.options.bigquery.project = PROJECT_ID
# You can change the location to one of the valid locations: https://cloud.google.com/bigquery/docs/locations#supported_locations
bigframes.options.bigquery.location = "US"

imported_tensorflow_model = TensorFlowModel(
    model_path="gs://cloud-training-demos/txtclass/export/exporter/1549825580/*"
)
```

如要進一步瞭解如何將 TensorFlow 模型匯入 BigQuery ML，包括格式和儲存空間需求，請參閱[`CREATE MODEL` 陳述式，瞭解如何匯入 TensorFlow 模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-tensorflow?hl=zh-tw)。

## 使用匯入的 TensorFlow 模型進行預測

匯入 TensorFlow 模型後，您可以使用 [`ML.PREDICT` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-predict?hl=zh-tw)，透過模型進行預測。

以下查詢會使用 `imported_tf_model`，根據公開資料集 `hacker_news` 中 `full` 資料表的輸入資料進行預測。在查詢中，TensorFlow 模型的 `serving_input_fn` 函式會指定模型預期一個名為「input」的輸入字串，`input`子查詢會將別名 `input` 指派給子查詢 `SELECT` 陳述式中的 `title` 資料欄。

如要使用匯入的 TensorFlow 模型進行預測，請按照下列步驟操作。

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往 BigQuery 頁面](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在「建立新項目」下方，點按「SQL 查詢」。
3. 在查詢編輯器中，輸入使用 `ML.PREDICT` 函式的查詢。

   ```
   SELECT *
     FROM ML.PREDICT(MODEL `bqml_tutorial.imported_tf_model`,
       (
        SELECT title AS input
        FROM bigquery-public-data.hacker_news.full
       )
   )
   ```

   查詢結果應如下所示：

### bq

輸入下列指令，執行使用 `ML.PREDICT` 的查詢。

```
bq query \
--use_legacy_sql=false \
'SELECT *
FROM ML.PREDICT(
  MODEL `bqml_tutorial.imported_tf_model`,
  (SELECT title AS input FROM `bigquery-public-data.hacker_news.full`))'
```

結果應如下所示：

```
+------------------------------------------------------------------------+----------------------------------------------------------------------------------+
|                               dense_1                                  |                                       input                                      |
+------------------------------------------------------------------------+----------------------------------------------------------------------------------+
|   ["0.6251608729362488","0.2989124357700348","0.07592673599720001"]    | How Red Hat Decides Which Open Source Companies t...                             |
|   ["0.014276246540248394","0.972910463809967","0.01281337533146143"]   | Ask HN: Toronto/GTA mastermind around side income for big corp. dev?             |
|   ["0.9821603298187256","1.8601855117594823E-5","0.01782100833952427"] | Ask HN: What are good resources on strategy and decision making for your career? |
|   ["0.8611106276512146","0.06648492068052292","0.07240450382232666"]   | Forget about promises, use harvests                                              |
+------------------------------------------------------------------------+----------------------------------------------------------------------------------+
```

### API

[插入新工作](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs/insert?hl=zh-tw)並填入 [jobs#configuration.query](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs/query?hl=zh-tw) 屬性，如下列要求主體所示：將 `project_id` 替換為您的專案名稱。

```
{
  "query": "SELECT * FROM ML.PREDICT(MODEL `project_id.bqml_tutorial.imported_tf_model`, (SELECT * FROM input_data))"
}
```

### BigQuery DataFrames

在嘗試這個範例之前，請按照[使用 BigQuery DataFrames 的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/dataframes-quickstart?hl=zh-tw)中的 BigQuery DataFrames 設定說明操作。
詳情請參閱 [BigQuery DataFrames 參考文件](https://docs.cloud.google.com/python/docs/reference/bigframes/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。
詳情請參閱「[為本機開發環境設定 ADC](https://docs.cloud.google.com/docs/authentication/set-up-adc-local-dev-environment?hl=zh-tw)」。

使用 [`predict`](https://docs.cloud.google.com/python/docs/reference/bigframes/latest/bigframes.ml.llm.PaLM2TextGenerator?hl=zh-tw#bigframes_ml_llm_PaLM2TextGenerator_predict) 函式執行 TensorFlow 模型：

```
import bigframes.pandas as bpd

df = bpd.read_gbq("bigquery-public-data.hacker_news.full")
df_pred = df.rename(columns={"title": "input"})
predictions = imported_tensorflow_model.predict(df_pred)
predictions.head(5)
```

結果應如下所示：

在查詢結果中，`dense_1` 資料欄包含機率值陣列，`input` 資料欄則包含輸入資料表中的對應字串值。每個陣列元素值表示相應輸入字串是某出版內容中的文章標題的機率。

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

或者，您也可以移除本教學課程中使用的個別資源：

1. [刪除匯入的模型](https://docs.cloud.google.com/bigquery/docs/deleting-models?hl=zh-tw)。
2. 選用：[刪除資料集](https://docs.cloud.google.com/bigquery/docs/managing-datasets?hl=zh-tw#delete-datasets)。

## 後續步驟

* 如需 BigQuery ML 的總覽，請參閱 [BigQuery ML 簡介](https://docs.cloud.google.com/bigquery/docs/bqml-introduction?hl=zh-tw)。
* 如要開始使用 BigQuery ML，請參閱[在 BigQuery ML 中建立機器學習模型](https://docs.cloud.google.com/bigquery/docs/create-machine-learning-model?hl=zh-tw)。
* 如要進一步瞭解如何匯入 TensorFlow 模型，請參閱[匯入 TensorFlow 模型的 `CREATE MODEL` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-tensorflow?hl=zh-tw)。
* 如要進一步瞭解模型的使用方式，請參閱下列資源：
  + [取得模型中繼資料](https://docs.cloud.google.com/bigquery/docs/getting-model-metadata?hl=zh-tw)
  + [更新模型中繼資料](https://docs.cloud.google.com/bigquery/docs/updating-model-metadata?hl=zh-tw)
  + [管理模型](https://docs.cloud.google.com/bigquery/docs/managing-models?hl=zh-tw)
* 如要進一步瞭解如何在 BigQuery 筆記本中使用 BigQuery DataFrames API，請參閱：
  + [BigQuery 筆記本簡介](https://docs.cloud.google.com/bigquery/docs/notebooks-introduction?hl=zh-tw)
  + [BigQuery DataFrames 總覽](https://docs.cloud.google.com/python/docs/reference/bigframes/latest?hl=zh-tw)




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-14 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-14 (世界標準時間)。"],[],[]]