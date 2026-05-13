Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見

# 使用 ONNX 格式的 scikit-learn 模型進行預測 透過集合功能整理內容 你可以依據偏好儲存及分類內容。

本教學課程說明如何匯入以 [scikit-learn](https://scikit-learn.org/stable/index.html) 訓練的[開放式神經網路交換](https://onnx.ai/) (ONNX) 模型。您將模型匯入 BigQuery 資料集，並使用 SQL 查詢進行預測。

ONNX 提供統一格式，可用於表示任何機器學習 (ML) 架構。BigQuery ML 支援 ONNX，因此您可以執行下列操作：

* 使用您喜愛的架構訓練模型。
* 將模型轉換為 ONNX 模型格式。
* 將 ONNX 模型匯入 BigQuery，並使用 BigQuery ML 進行預測。

## 目標

* 使用 [scikit-learn](https://scikit-learn.org/stable/index.html) 建立及訓練模型。
* 使用 [sklearn-onnx](https://onnx.ai/sklearn-onnx/) [將模型轉換為 ONNX 格式](https://github.com/onnx/tutorials#converting-to-onnx-format)。
* 使用 `CREATE MODEL` 陳述式將 ONNX 模型匯入 BigQuery。
* 使用 `ML.PREDICT` 函式，透過匯入的 ONNX 模型進行預測。

## 費用

在本文件中，您會使用下列 Google Cloud的計費元件：

* [BigQuery](https://cloud.google.com/bigquery/pricing?hl=zh-tw)
* [BigQuery ML](https://cloud.google.com/bigquery/pricing?hl=zh-tw#bqml)
* [Cloud Storage](https://docs.cloud.google.com/storage/pricing?hl=zh-tw)

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
2. 啟用 BigQuery 和 Cloud Storage API。

   **啟用 API 時所需的角色**

   如要啟用 API，您需要服務使用情形管理員 IAM 角色 (`roles/serviceusage.serviceUsageAdmin`)，其中包含 `serviceusage.services.enable` 權限。[瞭解如何授予角色](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)。

   [啟用 API](https://console.cloud.google.com/flows/enableapi?apiid=bigquery.googleapis.com%2Cstorage-component.googleapis.com&hl=zh-tw)
3. 請確認您具備[必要權限](#required_permissions)，可執行本文件中的工作。

### 必要的角色

如果您建立新專案，您就是專案擁有者，並已獲得完成本教學課程所需的所有 Identity and Access Management (IAM) 權限。

如果您使用現有專案，請按照下列步驟操作。

請確認您在專案中具備下列角色：

* [BigQuery Studio 管理員](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.studioUser) (`roles/bigquery.studioAdmin`)
* [Storage 物件建立者](https://docs.cloud.google.com/storage/docs/access-control/iam-roles?hl=zh-tw#standard-roles) (`roles/storage.objectCreator`)

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

如要進一步瞭解 BigQuery 中的 IAM 權限，請參閱 [IAM 權限](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bq-permissions)。

## 選用：訓練模型並轉換為 ONNX 格式

下列程式碼範例說明如何使用 scikit-learn 訓練分類模型，以及如何將產生的管線轉換為 ONNX 格式。本教學課程使用預先建構的範例模型，該模型儲存在 `gs://cloud-samples-data/bigquery/ml/onnx/pipeline_rf.onnx`。如果您使用範例模型，則不必完成這些步驟。

### 使用 scikit-learn 訓練分類模型

使用下列程式碼範例，在 [Iris](https://scikit-learn.org/stable/auto_examples/datasets/plot_iris_dataset.html) 資料集上建立並訓練 scikit-learn [管道](https://scikit-learn.org/stable/modules/compose.html#pipeline)。如需安裝及使用 scikit-learn 的操作說明，請參閱 [scikit-learn 安裝指南](https://scikit-learn.org/stable/install.html)。

```
import numpy
from sklearn.datasets import load_iris
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier

data = load_iris()
X = data.data[:, :4]
y = data.target

ind = numpy.arange(X.shape[0])
numpy.random.shuffle(ind)
X = X[ind, :].copy()
y = y[ind].copy()

pipe = Pipeline([('scaler', StandardScaler()),
                ('clr', RandomForestClassifier())])
pipe.fit(X, y)
```

**注意：** scikit-learn 管線可讓您納入其他程式庫 (例如 [LightGBM](https://lightgbm.readthedocs.io/en/latest/) 和 [XGBoost](https://xgboost.readthedocs.io/en/latest/)) 的模型，這些模型可由 sklearn-onnx 轉換為 ONNX。詳情請參閱「[轉換管道](https://onnx.ai/sklearn-onnx/pipeline.html#convert-a-pipeline)」和「[使用其他程式庫的轉換器](https://onnx.ai/sklearn-onnx/tutorial_1-5_external.html#using-converters-from-other-libraries)」。

### 將管道轉換為 ONNX 模型

在 [sklearn-onnx](https://onnx.ai/sklearn-onnx/) 中使用下列程式碼範例，將 scikit-learn 管道轉換為名為 `pipeline_rf.onnx` 的 ONNX 模型。

```
from skl2onnx import convert_sklearn
from skl2onnx.common.data_types import FloatTensorType

# Disable zipmap as it is not supported in BigQuery ML.
options = {id(pipe): {'zipmap': False}}

# Define input features. scikit-learn does not store information about the
# training dataset. It is not always possible to retrieve the number of features
# or their types. That's why the function needs another argument called initial_types.
initial_types = [
   ('sepal_length', FloatTensorType([None, 1])),
   ('sepal_width', FloatTensorType([None, 1])),
   ('petal_length', FloatTensorType([None, 1])),
   ('petal_width', FloatTensorType([None, 1])),
]

# Convert the model.
model_onnx = convert_sklearn(
   pipe, 'pipeline_rf', initial_types=initial_types, options=options
)

# And save.
with open('pipeline_rf.onnx', 'wb') as f:
 f.write(model_onnx.SerializeToString())
```

### 將 ONNX 模型上傳至 Cloud Storage

儲存模型後，請按照下列步驟操作：

* [建立 Cloud Storage bucket](https://docs.cloud.google.com/storage/docs/creating-buckets?hl=zh-tw) 來儲存模型。
* [將 ONNX 模型上傳至 Cloud Storage bucket](https://docs.cloud.google.com/storage/docs/uploading-objects?hl=zh-tw)。

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

### BigQuery DataFrames

在嘗試這個範例之前，請按照[使用 BigQuery DataFrames 的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/dataframes-quickstart?hl=zh-tw)中的 BigQuery DataFrames 設定說明操作。
詳情請參閱 [BigQuery DataFrames 參考文件](https://docs.cloud.google.com/python/docs/reference/bigframes/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。
詳情請參閱「[為本機開發環境設定 ADC](https://docs.cloud.google.com/docs/authentication/set-up-adc-local-dev-environment?hl=zh-tw)」。

```
import google.cloud.bigquery

bqclient = google.cloud.bigquery.Client()
bqclient.create_dataset("bqml_tutorial", exists_ok=True)
```

## 將 ONNX 模型匯入 BigQuery

下列步驟說明如何使用 [`CREATE MODEL`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-onnx?hl=zh-tw) 陳述式，從 Cloud Storage 匯入範例 ONNX 模型。

如要將 ONNX 模型匯入資料集，請選取下列其中一個選項：

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery Studio」頁面。

   [前往 BigQuery Studio](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列 `CREATE MODEL` 陳述式。

   ```
    CREATE OR REPLACE MODEL `bqml_tutorial.imported_onnx_model`
     OPTIONS (MODEL_TYPE='ONNX',
      MODEL_PATH='BUCKET_PATH')
   ```

   請將 `BUCKET_PATH` 改成您上傳至 Cloud Storage 的模型路徑。如果您使用範例模型，請將 `BUCKET_PATH` 替換為下列值：`gs://cloud-samples-data/bigquery/ml/onnx/pipeline_rf.onnx`。

   作業完成後，您會看到類似以下的訊息：`Successfully created model named imported_onnx_model`。

   新模型會顯示在「資源」面板中。模型會以模型圖示來表示：

### bq

1. 輸入下列 `CREATE MODEL` 陳述式，從 Cloud Storage 匯入 ONNX 模型。

   ```
   bq query --use_legacy_sql=false \
   "CREATE OR REPLACE MODEL
   `bqml_tutorial.imported_onnx_model`
   OPTIONS
   (MODEL_TYPE='ONNX',
     MODEL_PATH='BUCKET_PATH')"
   ```

   請將 `BUCKET_PATH` 改成您上傳至 Cloud Storage 的模型路徑。如果您使用範例模型，請將 `BUCKET_PATH` 替換為下列值：`gs://cloud-samples-data/bigquery/ml/onnx/pipeline_rf.onnx`。

   作業完成後，您會看到類似以下的訊息：`Successfully created model named imported_onnx_model`。
2. 匯入模型後，請確認模型是否顯示在資料集中。

   ```
   bq ls -m bqml_tutorial
   ```

   輸出結果會與下列內容相似：

   ```
   tableId               Type
   --------------------- -------
   imported_onnx_model  MODEL
   ```

### BigQuery DataFrames

在嘗試這個範例之前，請按照[使用 BigQuery DataFrames 的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/dataframes-quickstart?hl=zh-tw)中的 BigQuery DataFrames 設定說明操作。
詳情請參閱 [BigQuery DataFrames 參考文件](https://docs.cloud.google.com/python/docs/reference/bigframes/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。
詳情請參閱「[為本機開發環境設定 ADC](https://docs.cloud.google.com/docs/authentication/set-up-adc-local-dev-environment?hl=zh-tw)」。

使用 `ONNXModel` 物件匯入模型。

```
import bigframes
from bigframes.ml.imported import ONNXModel

bigframes.options.bigquery.project = PROJECT_ID
# You can change the location to one of the valid locations: https://cloud.google.com/bigquery/docs/locations#supported_locations
bigframes.options.bigquery.location = "US"

imported_onnx_model = ONNXModel(
    model_path="gs://cloud-samples-data/bigquery/ml/onnx/pipeline_rf.onnx"
)
```

如要進一步瞭解如何將 ONNX 模型匯入 BigQuery，包括格式和儲存空間需求，請參閱[匯入 ONNX 模型的 `CREATE MODEL` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-onnx?hl=zh-tw)。

## 使用匯入的 ONNX 模型進行預測

匯入 ONNX 模型後，您可以使用 [`ML.PREDICT` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-predict?hl=zh-tw)，透過模型進行預測。

下列步驟中的查詢會使用 `imported_onnx_model`，根據 `ml_datasets` 公開資料集 `iris` 資料表中的輸入資料進行預測。ONNX 模型預期輸入四個 `FLOAT` 值：

* `sepal_length`
* `sepal_width`
* `petal_length`
* `petal_width`

這些輸入內容與`initial_types`您[將模型轉換為 ONNX 格式](https://github.com/onnx/tutorials#converting-to-onnx-format)時定義的內容相符。

輸出內容包括 `label` 和 `probabilities` 資料欄，以及輸入資料表中的資料欄。`label` 代表預測的類別標籤。`probabilities` 是機率陣列，代表每個類別的機率。

如要使用匯入的 ONNX 模型進行預測，請選擇下列其中一種做法：

### 控制台

1. 前往「BigQuery Studio」頁面。

   [前往 BigQuery Studio](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中，輸入使用 `ML.PREDICT` 函式的查詢。

   ```
   SELECT *
     FROM ML.PREDICT(MODEL `bqml_tutorial.imported_onnx_model`,
       (
       SELECT * FROM `bigquery-public-data.ml_datasets.iris`
       )
   )
   ```

   查詢結果類似於下列內容：

### bq

執行使用 `ML.PREDICT` 的查詢。

```
bq query --use_legacy_sql=false \
'SELECT *
FROM ML.PREDICT(
MODEL `example_dataset.imported_onnx_model`,
(SELECT * FROM `bigquery-public-data.ml_datasets.iris`))'
```

### BigQuery DataFrames

在嘗試這個範例之前，請按照[使用 BigQuery DataFrames 的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/dataframes-quickstart?hl=zh-tw)中的 BigQuery DataFrames 設定說明操作。
詳情請參閱 [BigQuery DataFrames 參考文件](https://docs.cloud.google.com/python/docs/reference/bigframes/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。
詳情請參閱「[為本機開發環境設定 ADC](https://docs.cloud.google.com/docs/authentication/set-up-adc-local-dev-environment?hl=zh-tw)」。

使用 [`predict`](https://dataframes.bigquery.dev/reference/api/bigframes.ml.imported.ONNXModel.html#bigframes.ml.imported.ONNXModel.predict) 函式執行 ONNX 模型。

```
import bigframes.pandas as bpd

df = bpd.read_gbq("bigquery-public-data.ml_datasets.iris")
predictions = imported_onnx_model.predict(df)
predictions.peek(5)
```

結果大致如下：

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

或者，如要移除本教學課程中使用的個別資源，請執行下列操作：

1. [刪除匯入的模型](https://docs.cloud.google.com/bigquery/docs/deleting-models?hl=zh-tw)。
2. 選用：[刪除資料集](https://docs.cloud.google.com/bigquery/docs/managing-datasets?hl=zh-tw#delete-datasets)。

## 後續步驟

* 如要進一步瞭解如何匯入 ONNX 模型，請參閱「[ONNX 模型的 `CREATE MODEL` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-onnx?hl=zh-tw)」。
* 如要進一步瞭解可用的 ONNX 轉換器和教學課程，請參閱「[轉換為 ONNX 格式](https://github.com/onnx/tutorials#converting-to-onnx-format)」。
* 如需 BigQuery ML 的總覽，請參閱 [BigQuery ML 簡介](https://docs.cloud.google.com/bigquery/docs/bqml-introduction?hl=zh-tw)。
* 如要開始使用 BigQuery ML，請參閱[在 BigQuery ML 中建立機器學習模型](https://docs.cloud.google.com/bigquery/docs/create-machine-learning-model?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-12 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-12 (世界標準時間)。"],[],[]]