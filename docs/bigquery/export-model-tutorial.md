Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見

# 匯出 BigQuery ML 模型以進行線上預測 透過集合功能整理內容 你可以依據偏好儲存及分類內容。

**注意：**如果使用 Vertex AI Model Registry，則不需要匯出模型，即可在 Vertex AI 上部署。 如要進一步瞭解登錄檔，請參閱「[在 Model Registry 中管理 BigQuery ML 模型](https://docs.cloud.google.com/bigquery/docs/managing-models-vertex?hl=zh-tw)」。

本教學課程說明如何[匯出 BigQuery ML 模型](https://docs.cloud.google.com/bigquery/docs/exporting-models?hl=zh-tw)，然後在 Vertex AI 或本機電腦上部署模型。您將使用 BigQuery 公開資料集中的 [`iris` 資料表](https://console.cloud.google.com/bigquery?p=bigquery-public-data&%3Bd=ml_datasets&%3Bt=iris&%3Bpage=table&hl=zh-tw)，完成下列三個端對端情境：

* 訓練及部署邏輯迴歸模型 - 也適用於 DNN 分類器、DNN 迴歸器、k-means、線性迴歸和矩陣分解模型。
* 訓練及部署提升決策樹分類器模型 - 也適用於提升決策樹迴歸模型。
* 訓練及部署 AutoML 分類器模型 - 也適用於 AutoML 迴歸模型。

## 費用

本教學課程使用 Google Cloud的計費元件，包括：

* BigQuery ML
* Cloud Storage
* Vertex AI (選用，用於線上預測)

如要進一步瞭解 BigQuery ML 費用，請參閱 [BigQuery ML 定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#bqml)。

如要進一步瞭解 Cloud Storage 費用，請參閱 [Cloud Storage 定價](https://cloud.google.com/storage/pricing?hl=zh-tw)頁面。

如要進一步瞭解 Vertex AI 費用，請參閱「[自訂訓練模型](https://cloud.google.com/vertex-ai/pricing?hl=zh-tw#custom-trained_models)」。

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

1. 新專案會自動啟用 BigQuery。如要在現有專案中啟用 BigQuery，請前往

   啟用 BigQuery API。

   **啟用 API 時所需的角色**

   如要啟用 API，您需要服務使用情形管理員 IAM 角色 (`roles/serviceusage.serviceUsageAdmin`)，其中包含 `serviceusage.services.enable` 權限。[瞭解如何授予角色](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)。

   [啟用 API](https://console.cloud.google.com/flows/enableapi?apiid=bigquery&hl=zh-tw)
2. 啟用 AI Platform Training and Prediction API 和 Compute Engine API。

   **啟用 API 時所需的角色**

   如要啟用 API，您需要服務使用情形管理員 IAM 角色 (`roles/serviceusage.serviceUsageAdmin`)，其中包含 `serviceusage.services.enable` 權限。[瞭解如何授予角色](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)。

   [啟用 API](https://console.cloud.google.com/flows/enableapi?apiid=ml.googleapis.com%2Ccompute_component&hl=zh-tw)
3. 安裝 [Google Cloud CLI](https://docs.cloud.google.com/sdk/install?hl=zh-tw) 和 [Google Cloud CLI](https://docs.cloud.google.com/sdk/downloads?hl=zh-tw#interactive)。

## 建立您的資料集

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

## 訓練及部署邏輯迴歸模型

請參閱下列各節，瞭解如何訓練及部署邏輯迴歸模型。

### 訓練模型

使用 BigQuery ML [`CREATE MODEL`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create?hl=zh-tw#create_model_syntax) 陳述式，訓練可預測鳶尾花類型的邏輯迴歸模型。這項訓練工作大約 1 分鐘就能完成。

```
bq query --use_legacy_sql=false \
  'CREATE MODEL `bqml_tutorial.iris_model`
  OPTIONS (model_type="logistic_reg",
      max_iterations=10, input_label_cols=["species"])
  AS SELECT
    *
  FROM
    `bigquery-public-data.ml_datasets.iris`;'
```

### 匯出模型

使用 [bq 指令列工具](https://docs.cloud.google.com/bigquery/docs/bq-command-line-tool?hl=zh-tw)將模型匯出至 Cloud Storage bucket。如需其他匯出模型的方法，請參閱「[匯出 BigQuery ML 模型](https://docs.cloud.google.com/bigquery/docs/exporting-models?hl=zh-tw)」。這項擷取作業應可在 1 分鐘內完成。

```
bq extract -m bqml_tutorial.iris_model gs://some/gcs/path/iris_model
```

### 在本機部署及放送

您可以使用 TensorFlow Serving Docker 容器，部署匯出的 TensorFlow 模型。下列步驟需要安裝 [Docker](https://hub.docker.com/search/?type=edition&offering=community)。

#### 將匯出的模型檔案下載至暫時目錄

```
mkdir tmp_dir
gcloud storage cp gs://some/gcs/path/iris_model tmp_dir --recursive
```

#### 建立版本子目錄

這個步驟會為模型設定版本號碼 (本例為 1)。

```
mkdir -p serving_dir/iris_model/1
cp -r tmp_dir/iris_model/* serving_dir/iris_model/1
rm -r tmp_dir
```

#### 提取 Docker 映像檔

```
docker pull tensorflow/serving
```

#### 執行 Docker 容器

```
docker run -p 8500:8500 --network="host" --mount type=bind,source=`pwd`/serving_dir/iris_model,target=/models/iris_model -e MODEL_NAME=iris_model -t tensorflow/serving &
```

#### 執行預測

```
curl -d '{"instances": [{"sepal_length":5.0, "sepal_width":2.0, "petal_length":3.5, "petal_width":1.0}]}' -X POST http://localhost:8501/v1/models/iris_model:predict
```

### 線上部署和供應

本節將使用 [Google Cloud CLI](https://docs.cloud.google.com/sdk/gcloud?hl=zh-tw) 部署匯出的模型，並根據該模型執行預測。

如要進一步瞭解如何將模型部署至 Vertex AI，以進行線上或批次預測，請參閱「[將模型部署至端點](https://docs.cloud.google.com/vertex-ai/docs/general/deployment?hl=zh-tw)」一文。

#### 建立模型資源

```
MODEL_NAME="IRIS_MODEL"
gcloud ai-platform models create $MODEL_NAME
```

#### 建立模型版本

1) 設定環境變數：

```
MODEL_DIR="gs://some/gcs/path/iris_model"
// Select a suitable version for this model
VERSION_NAME="v1"
FRAMEWORK="TENSORFLOW"
```

2) 建立版本：

```
gcloud ai-platform versions create $VERSION_NAME --model=$MODEL_NAME --origin=$MODEL_DIR --runtime-version=1.15 --framework=$FRAMEWORK
```

這個步驟可能需要幾分鐘才能完成。您應該會看到「`Creating version (this might take a few minutes)......`」訊息。

3) (選用) 取得新版本的相關資訊：

```
gcloud ai-platform versions describe $VERSION_NAME --model $MODEL_NAME
```

畫面會顯示類似以下的輸出：

```
createTime: '2020-02-28T16:30:45Z'
deploymentUri: gs://your_bucket_name
framework: TENSORFLOW
machineType: mls1-c1-m2
name: projects/[YOUR-PROJECT-ID]/models/IRIS_MODEL/versions/v1
pythonVersion: '2.7'
runtimeVersion: '1.15'
state: READY
```

#### 線上預測

如要進一步瞭解如何針對已部署的模型執行線上預測，請參閱「[透過自訂訓練模型取得線上推論結果](https://docs.cloud.google.com/vertex-ai/docs/predictions/get-online-predictions?hl=zh-tw)」。

1) 建立以換行符號分隔的 JSON 輸入檔案，例如：`instances.json`
含有下列內容的檔案：

```
{"sepal_length":5.0, "sepal_width":2.0, "petal_length":3.5, "petal_width":1.0}
{"sepal_length":5.3, "sepal_width":3.7, "petal_length":1.5, "petal_width":0.2}
```

2) 設定預測的環境變數：

```
INPUT_DATA_FILE="instances.json"
```

3) 執行預測：

```
gcloud ai-platform predict --model $MODEL_NAME --version $VERSION_NAME --json-instances $INPUT_DATA_FILE
```

## 訓練及部署提升決策樹分類器模型

請參閱下列各節，瞭解如何訓練及部署升級樹狀結構分類器模型。

### 訓練模型

使用 [`CREATE MODEL`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create?hl=zh-tw#create_model) 陳述式訓練提升樹狀結構分類器模型，預測鳶尾花類型。這項訓練工作大約需要 7 分鐘才能完成。

```
bq query --use_legacy_sql=false \
  'CREATE MODEL `bqml_tutorial.boosted_tree_iris_model`
  OPTIONS (model_type="boosted_tree_classifier",
      max_iterations=10, input_label_cols=["species"])
  AS SELECT
    *
  FROM
    `bigquery-public-data.ml_datasets.iris`;'
```

### 匯出模型

使用 [bq 指令列工具](https://docs.cloud.google.com/bigquery/docs/bq-command-line-tool?hl=zh-tw)將模型匯出至 Cloud Storage bucket。如要瞭解其他模型匯出方式，請參閱「[匯出 BigQuery ML 模型](https://docs.cloud.google.com/bigquery/docs/exporting-models?hl=zh-tw)」。

```
bq extract --destination_format ML_XGBOOST_BOOSTER -m bqml_tutorial.boosted_tree_iris_model gs://some/gcs/path/boosted_tree_iris_model
```

### 在本機部署及放送

匯出的檔案中會有 `main.py` 檔案，可供在本機執行。

#### 將匯出的模型檔案下載至本機目錄

```
mkdir serving_dir
gcloud storage cp gs://some/gcs/path/boosted_tree_iris_model serving_dir --recursive
```

#### 擷取預測因子

```
tar -xvf serving_dir/boosted_tree_iris_model/xgboost_predictor-0.1.tar.gz -C serving_dir/boosted_tree_iris_model/
```

#### 安裝 XGBoost 程式庫

安裝 [XGBoost 程式庫](https://xgboost.readthedocs.io/en/latest/build.html) (0.82 以上版本)。

#### 執行預測

```
cd serving_dir/boosted_tree_iris_model/
python main.py '[{"sepal_length":5.0, "sepal_width":2.0, "petal_length":3.5, "petal_width":1.0}]'
```

### 線上部署和供應

本節將使用 [Google Cloud CLI](https://docs.cloud.google.com/sdk/gcloud?hl=zh-tw) 部署匯出的模型，並根據該模型執行預測。詳情請參閱「[透過自訂訓練模型取得線上推論結果](https://docs.cloud.google.com/vertex-ai/docs/predictions/get-online-predictions?hl=zh-tw)」。

**注意：** 如要在 [Vertex AI](https://docs.cloud.google.com/vertex-ai/docs?hl=zh-tw) Prediction 上提供服務，請按照「[要求預測](https://docs.cloud.google.com/vertex-ai/docs/predictions/getting-predictions?hl=zh-tw)」一文的說明操作，並根據所在區域使用下列容器：
1) us-docker.pkg.dev/vertex-ai/bigquery-ml/xgboost-cpu.1-0:latest
2) europe-docker.pkg.dev/vertex-ai/bigquery-ml/xgboost-cpu.1-0:latest
3) asia-docker.pkg.dev/vertex-ai/bigquery-ml/xgboost-cpu.1-0:latest

如要進一步瞭解如何將模型部署至 Vertex AI，以便使用自訂常式進行線上或批次預測，請參閱「[將模型部署至端點](https://docs.cloud.google.com/vertex-ai/docs/general/deployment?hl=zh-tw)」。

#### 建立模型資源

```
MODEL_NAME="BOOSTED_TREE_IRIS_MODEL"
gcloud ai-platform models create $MODEL_NAME
```

#### 建立模型版本

1) 設定環境變數：

```
MODEL_DIR="gs://some/gcs/path/boosted_tree_iris_model"
VERSION_NAME="v1"
```

2) 建立版本：

```
gcloud beta ai-platform versions create $VERSION_NAME --model=$MODEL_NAME --origin=$MODEL_DIR --package-uris=${MODEL_DIR}/xgboost_predictor-0.1.tar.gz --prediction-class=predictor.Predictor --runtime-version=1.15
```

這個步驟可能需要幾分鐘才能完成。您應該會看到「`Creating version (this might take a few minutes)......`」訊息。

3) (選用) 取得新版本的相關資訊：

```
gcloud ai-platform versions describe $VERSION_NAME --model $MODEL_NAME
```

畫面會顯示類似以下的輸出：

```
createTime: '2020-02-07T00:35:42Z'
deploymentUri: gs://some/gcs/path/boosted_tree_iris_model
etag: rp090ebEnQk=
machineType: mls1-c1-m2
name: projects/[YOUR-PROJECT-ID]/models/BOOSTED_TREE_IRIS_MODEL/versions/v1
packageUris:
- gs://some/gcs/path/boosted_tree_iris_model/xgboost_predictor-0.1.tar.gz
predictionClass: predictor.Predictor
pythonVersion: '2.7'
runtimeVersion: '1.15'
state: READY
```

#### 線上預測

如要進一步瞭解如何針對已部署的模型執行線上預測，請參閱「[透過自訂訓練模型取得線上推論結果](https://docs.cloud.google.com/vertex-ai/docs/predictions/get-online-predictions?hl=zh-tw)」。

1) 建立以換行符號分隔的輸入內容 JSON 檔案。例如，`instances.json` 檔案包含下列內容：

```
{"sepal_length":5.0, "sepal_width":2.0, "petal_length":3.5, "petal_width":1.0}
{"sepal_length":5.3, "sepal_width":3.7, "petal_length":1.5, "petal_width":0.2}
```

2) 設定預測的環境變數：

```
INPUT_DATA_FILE="instances.json"
```

3) 執行預測：

```
gcloud ai-platform predict --model $MODEL_NAME --version $VERSION_NAME --json-instances $INPUT_DATA_FILE
```

## 訓練及部署 AutoML 分類器模型

請參閱下列各節，瞭解如何訓練及部署 AutoML 分類器模型。

### 訓練模型

使用 [`CREATE MODEL`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create?hl=zh-tw) 陳述式，訓練可預測鳶尾花類型的 AutoML 分類器模型。AutoML 模型至少需要 1000 列輸入資料。由於 `ml_datasets.iris` 只有 150 個資料列，因此我們將資料複製 10 次。這項訓練工作大約需要 **2 小時**才能完成。

```
bq query --use_legacy_sql=false \
  'CREATE MODEL `bqml_tutorial.automl_iris_model`
  OPTIONS (model_type="automl_classifier",
      budget_hours=1, input_label_cols=["species"])
  AS SELECT
    * EXCEPT(multiplier)
  FROM
    `bigquery-public-data.ml_datasets.iris`, unnest(GENERATE_ARRAY(1, 10)) as multiplier;'
```

### 匯出模型

使用 [bq 指令列工具](https://docs.cloud.google.com/bigquery/docs/bq-command-line-tool?hl=zh-tw)將模型匯出至 Cloud Storage bucket。如需其他模型匯出方式，請參閱「[匯出 BigQuery ML 模型](https://docs.cloud.google.com/bigquery/docs/exporting-models?hl=zh-tw)」。

```
bq extract -m bqml_tutorial.automl_iris_model gs://some/gcs/path/automl_iris_model
```

### 在本機部署及放送

如要瞭解如何建構 AutoML 容器，請參閱「[匯出 AutoML 表格型模型](https://docs.cloud.google.com/vertex-ai/docs/export/export-model-tabular?hl=zh-tw)」。下列步驟需要安裝 [Docker](https://hub.docker.com/search/?type=edition&offering=community)。

#### 將匯出的模型檔案複製到本機目錄

```
mkdir automl_serving_dir
gcloud storage cp gs://some/gcs/path/automl_iris_model/* automl_serving_dir/ --recursive
```

#### 提取 AutoML Docker 映像檔

```
docker pull gcr.io/cloud-automl-tables-public/model_server
```

#### 啟動 Docker 容器

```
docker run -v `pwd`/automl_serving_dir:/models/default/0000001 -p 8080:8080 -it gcr.io/cloud-automl-tables-public/model_server
```

#### 執行預測

1) 建立以換行符號分隔的輸入內容 JSON 檔案。例如，`input.json` 檔案包含下列內容：

```
{"instances": [{"sepal_length":5.0, "sepal_width":2.0, "petal_length":3.5, "petal_width":1.0},
{"sepal_length":5.3, "sepal_width":3.7, "petal_length":1.5, "petal_width":0.2}]}
```

2) 進行預測呼叫：

```
curl -X POST --data @input.json http://localhost:8080/predict
```

### 線上部署和供應

Vertex AI 不支援 AutoML 迴歸模型和 AutoML 分類器模型的線上預測。

## 清除所用資源

為避免因為本教學課程所用資源，導致系統向 Google Cloud 帳戶收取費用，請刪除含有相關資源的專案，或者保留專案但刪除個別資源。

* 您可以刪除建立的專案。
* 或者，您也可以保留專案，並刪除資料集和 Cloud Storage 值區。

### 停止 Docker 容器

1) 列出所有正在執行的 Docker 容器。

```
docker ps
```

2) 從容器清單中，找出適用的容器 ID 並停止容器。

```
docker stop container_id
```

### 刪除 Vertex AI 資源

1) 刪除模型版本。

```
gcloud ai-platform versions delete $VERSION_NAME --model=$MODEL_NAME
```

2) 刪除模型。

```
gcloud ai-platform models delete $MODEL_NAME
```

### 刪除資料集

刪除專案將移除專案中所有的資料集與資料表。若您希望重新使用專案，您可以刪除本教學課程中所建立的資料集。

1. 如有必要，請在Google Cloud 控制台中開啟 BigQuery 頁面。

   [前往 BigQuery 頁面](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在導覽窗格中，按一下您建立的 **bqml\_tutorial** 資料集。
3. 按一下視窗右側的「刪除資料集」。
   這個動作將會刪除資料集、資料表，以及所有資料。
4. 在「Delete dataset」(刪除資料集) 對話方塊中，輸入資料集的名稱 (`bqml_tutorial`)，然後按一下「Delete」(刪除) 來確認刪除指令。

### 刪除 Cloud Storage 值區

刪除專案會移除專案中的所有 Cloud Storage 值區。若您希望重新使用專案，可以刪除本教學課程中所建立的 bucket

1. 前往 Google Cloud 控制台的「Cloud Storage bucket」頁面。  

   [前往「Buckets」(值區) 頁面](https://console.cloud.google.com/storage/browser?hl=zh-tw)
2. 找到您要刪除的值區，並選取旁邊的核取方塊。
3. 按一下 [Delete] (刪除)。
4. 在出現的重疊視窗中，確認您要刪除的值區及內容，然後按一下 [Delete] (刪除)。

### 刪除專案

如要刪除專案，請進行以下操作：

**注意**：刪除專案會造成以下結果：

* **專案中的所有內容都會遭到刪除。**如果使用現有專案來進行本文中的任務，刪除專案將一併移除當中已完成的其他任務'。
* **自訂專案 ID 會消失。**當您之前建立這個專案時，可能建立了想要在日後使用的自訂專案 ID。如要保留使用該專案 ID 的網址 (例如 `appspot.com` 網址)，請刪除在該專案中選取的資源，而不是刪除整個專案。

如果打算探索多種架構、教學課程或快速入門導覽課程，重複使用專案可避免超出專案配額限制。

1. 前往 Google Cloud 控制台的「Manage resources」(管理資源) 頁面。

   [前往「Manage resources」(管理資源)](https://console.cloud.google.com/iam-admin/projects?hl=zh-tw)
2. 在專案清單中選取要刪除的專案，然後點選「Delete」(刪除)。
3. 在對話方塊中輸入專案 ID，然後按一下 [Shut down] (關閉) 以刪除專案。

## 後續步驟

* 如需 BigQuery ML 的總覽，請參閱 [BigQuery ML 簡介](https://docs.cloud.google.com/bigquery/docs/bqml-introduction?hl=zh-tw)。
* 如要瞭解如何匯出模型，請參閱「[匯出模型](https://docs.cloud.google.com/bigquery/docs/exporting-models?hl=zh-tw)」。
* 如要瞭解如何建立模型，請參閱 [`CREATE MODEL`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create?hl=zh-tw) 語法頁面。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-02 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-02 (世界標準時間)。"],[],[]]