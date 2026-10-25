Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見

# 使用增強型樹狀模型執行分類 透過集合功能整理內容 你可以依據偏好儲存及分類內容。

本教學課程說明如何使用[提升樹狀結構分類器模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-boosted-tree?hl=zh-tw)，根據個人的人口統計資料預測收入範圍。模型會預測值是否屬於其中一個類別，在本例中，即個人年收入是否高於或低於 $50,000 美元。

本教學課程使用 [`bigquery-public-data.ml_datasets.census_adult_income`](https://console.cloud.google.com/bigquery?p=bigquery-public-data&%3Bd=ml_datasets&%3Bt=census_adult_income&%3Bpage=table&hl=zh-tw) 資料集。這個資料集包含 2000 年和 2010 年美國居民的客層和收入資訊。

## 目標

本教學課程會逐步引導您完成下列工作：

* 使用 [`CREATE MODEL` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-boosted-tree?hl=zh-tw)建立提升樹模型，預測人口普查受訪者的收入級距。
* 使用 [`ML.EVALUATE` 函式評估模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-evaluate?hl=zh-tw)。
* 使用 [`ML.PREDICT` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-predict?hl=zh-tw)從模型取得預測結果。

## 費用

本教學課程使用的 Google Cloud計費元件包括：

* BigQuery
* BigQuery ML

如要進一步瞭解 BigQuery 費用，請參閱 [BigQuery 定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw)頁面。

如要進一步瞭解 BigQuery ML 費用，請參閱「[BigQuery ML 定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#bqml)」一文。

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

1. 新專案會自動啟用 BigQuery。如要在現有的專案中啟用 BigQuery，請前往

   如果尚未啟用 BigQuery API，請啟用。

   **啟用 API 時所需的角色**

   如要啟用 API，您必須具備 `serviceusage.services.enable` 權限。如果您建立了專案，可能已透過「擁有者」角色 (`roles/owner`) 取得這項權限。否則，您可以透過「服務使用情形管理員」角色 (`roles/serviceusage.serviceUsageAdmin`) 取得這項權限。[瞭解如何授予角色](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)。

   [啟用 API](https://console.cloud.google.com/apis/enableflow?apiid=bigquery&hl=zh-tw)

## 所需權限

* 如要建立資料集，您需要 `bigquery.datasets.create` IAM 權限。
* 如要建立模型，您必須具備下列權限：

  + `bigquery.jobs.create`
  + `bigquery.models.create`
  + `bigquery.models.getData`
  + `bigquery.models.updateData`
* 如要執行推論，您需要下列權限：

  + `bigquery.models.getData`
  + `bigquery.jobs.create`

如要進一步瞭解 BigQuery 中的 IAM 角色和權限，請參閱「[IAM 簡介](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)」。

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
   * 選取「資料位置」的「美國」。

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

### BigQuery DataFrames

在嘗試這個範例之前，請按照[使用 BigQuery DataFrames 的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/dataframes-quickstart?hl=zh-tw)，完成 BigQuery DataFrames 設定。詳情請參閱 [BigQuery DataFrames 參考文件](https://docs.cloud.google.com/python/docs/reference/bigframes/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。
詳情請參閱「[為本機開發環境設定 ADC](https://docs.cloud.google.com/docs/authentication/set-up-adc-local-dev-environment?hl=zh-tw)」。

```
import google.cloud.bigquery

bqclient = google.cloud.bigquery.Client()
bqclient.create_dataset("bqml_tutorial", exists_ok=True)
```

## 準備範例資料

在本教學課程中建立的模型會根據下列特徵，預測人口普查受訪者的收入級距：

* 年齡
* 從事的工作類型
* 婚姻狀態
* 教育程度
* 職業
* 每週工作時數

訓練資料不包含 `education` 欄，因為 `education` 和 `education_num` 欄都以不同格式表示受訪者的教育程度。

您可建立衍生自 `functional_weight` 欄的新 `dataframe` 欄，將資料分成訓練、評估和預測集。80% 的資料用於訓練模型，其餘 20% 的資料則用於評估和預測。

### SQL

如要準備範例資料，請建立包含訓練資料的[檢視區塊](https://docs.cloud.google.com/bigquery/docs/views-intro?hl=zh-tw)。本教學課程稍後會使用 `CREATE MODEL` 陳述式。

執行查詢，準備範例資料：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中執行下列查詢：

   ```
   CREATE OR REPLACE VIEW
     `bqml_tutorial.input_data` AS
   SELECT
     age,
     workclass,
     marital_status,
     education_num,
     occupation,
     hours_per_week,
     income_bracket,
     CASE
       WHEN MOD(functional_weight, 10) < 8 THEN 'training'
       WHEN MOD(functional_weight, 10) = 8 THEN 'evaluation'
       WHEN MOD(functional_weight, 10) = 9 THEN 'prediction'
     END AS dataframe
   FROM
     `bigquery-public-data.ml_datasets.census_adult_income`;
   ```
3. 點選左側窗格中的 explore「Explorer」。

   如果沒有看到左側窗格，請按一下 last\_page「Expand left pane」(展開左側窗格)，開啟窗格。
4. 在「Explorer」窗格，搜尋 `bqml_tutorial` 資料集。
5. 按一下資料集，然後依序點選「總覽」**>「資料表」**。
6. 按一下「`input_data`」檢視畫面，開啟資訊窗格。「結構定義」分頁會顯示檢視區塊結構定義。

### BigQuery DataFrames

建立名為 `input_data` 的 DataFrame。在本教學課程中，您稍後會使用 `input_data` 訓練模型、評估模型及進行預測。

在嘗試這個範例之前，請按照[使用 BigQuery DataFrames 的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/dataframes-quickstart?hl=zh-tw)，完成 BigQuery DataFrames 設定。詳情請參閱 [BigQuery DataFrames 參考文件](https://docs.cloud.google.com/python/docs/reference/bigframes/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。
詳情請參閱「[為本機開發環境設定 ADC](https://docs.cloud.google.com/docs/authentication/set-up-adc-local-dev-environment?hl=zh-tw)」。

```
import bigframes.pandas as bpd

# Set partial ordering mode for BigQuery DataFrames.
# For more information, see the BigQuery DataFrames performance documentation:
# https://cloud.google.com/bigquery/docs/dataframes-performance#partial-ordering-mode
bpd.options.bigquery.ordering_mode = "partial"

input_data = bpd.read_gbq(
    "bigquery-public-data.ml_datasets.census_adult_income",
    columns=(
        "age",
        "workclass",
        "marital_status",
        "education_num",
        "occupation",
        "hours_per_week",
        "income_bracket",
        "functional_weight",
    ),
)
input_data["dataframe"] = input_data["functional_weight"].case_when(
    [
        (((input_data["functional_weight"] % 10) == 8), "evaluation"),
        (((input_data["functional_weight"] % 10) == 9), "prediction"),
        (True, "training"),
    ]
)
del input_data["functional_weight"]
```

## 建立提升樹模型

建立提升樹模型，預測人口普查受訪者的收入級距，並根據人口普查資料訓練模型。查詢作業約需 30 分鐘才能完成。

### SQL

請按照下列步驟建立模型：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中貼入下列查詢，然後點選「執行」：

   ```
   CREATE MODEL `bqml_tutorial.tree_model`
   OPTIONS(MODEL_TYPE='BOOSTED_TREE_CLASSIFIER',
           BOOSTER_TYPE = 'GBTREE',
           NUM_PARALLEL_TREE = 1,
           MAX_ITERATIONS = 50,
           TREE_METHOD = 'HIST',
           EARLY_STOP = FALSE,
           SUBSAMPLE = 0.85,
           INPUT_LABEL_COLS = ['income_bracket'])
   AS SELECT * EXCEPT(dataframe)
   FROM `bqml_tutorial.input_data`
   WHERE dataframe = 'training';
   ```

   查詢完成後，即可透過「Explorer」(探索工具) 窗格存取 `tree_model` 模型。由於查詢使用 `CREATE MODEL` 陳述式建立模型，因此您不會看到查詢結果。

### BigQuery DataFrames

在嘗試這個範例之前，請按照[使用 BigQuery DataFrames 的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/dataframes-quickstart?hl=zh-tw)，完成 BigQuery DataFrames 設定。詳情請參閱 [BigQuery DataFrames 參考文件](https://docs.cloud.google.com/python/docs/reference/bigframes/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。
詳情請參閱「[為本機開發環境設定 ADC](https://docs.cloud.google.com/docs/authentication/set-up-adc-local-dev-environment?hl=zh-tw)」。

```
import bigframes.pandas as bpd
from bigframes.bigquery import ml

# Set partial ordering mode for BigQuery DataFrames.
# For more information, see the BigQuery DataFrames performance documentation:
# https://cloud.google.com/bigquery/docs/dataframes-performance#partial-ordering-mode
bpd.options.bigquery.ordering_mode = "partial"

# input_data is defined in an earlier step.
training_data = input_data[input_data["dataframe"] == "training"].drop(
    columns=["dataframe"]
)

# For more information, see the BigQuery DataFrames API reference documentation:
# https://dataframes.bigquery.dev/reference/api/bigframes.bigquery.ml.create_model.html#bigframes.bigquery.ml.create_model
ml.create_model(
    your_model_id,  # For example: "your-project.bqml_tutorial.tree_model"
    options={
        "model_type": "BOOSTED_TREE_CLASSIFIER",
        "booster_type": "GBTREE",
        "num_parallel_tree": 1,
        "max_iterations": 1,  # For a more accurate model, try 50 iterations.
        "tree_method": "HIST",
        "early_stop": False,
        "subsample": 0.85,
        "input_label_cols": ["income_bracket"],
    },
    training_data=training_data,
    replace=True,
)
```

## 評估模型

### SQL

如要評估模型，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中貼入下列查詢，然後點選「執行」：

   ```
     SELECT
       *
     FROM
       ML.EVALUATE (MODEL `bqml_tutorial.tree_model`,
         (
         SELECT
           *
         FROM
           `bqml_tutorial.input_data`
         WHERE
           dataframe = 'evaluation'
         )
       );
   ```

   結果應如下所示：

   ```
   +---------------------+---------------------+---------------------+-------------------+---------------------+---------------------+
   | precision           | recall              | accuracy            | f1_score          | log_loss            | roc_auc             |
   +---------------------+---------------------+---------------------+-------------------+-------------------------------------------+
   | 0.67192429022082023 | 0.57880434782608692 | 0.83942963422194672 | 0.621897810218978 | 0.34405456040833338 | 0.88733566433566435 |
   +---------------------+---------------------+ --------------------+-------------------+---------------------+---------------------+
   ```

### BigQuery DataFrames

在嘗試這個範例之前，請按照[使用 BigQuery DataFrames 的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/dataframes-quickstart?hl=zh-tw)，完成 BigQuery DataFrames 設定。詳情請參閱 [BigQuery DataFrames 參考文件](https://docs.cloud.google.com/python/docs/reference/bigframes/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。
詳情請參閱「[為本機開發環境設定 ADC](https://docs.cloud.google.com/docs/authentication/set-up-adc-local-dev-environment?hl=zh-tw)」。

```
import bigframes.pandas as bpd
from bigframes.bigquery import ml

# Set partial ordering mode for BigQuery DataFrames.
# For more information, see the BigQuery DataFrames performance documentation:
# https://cloud.google.com/bigquery/docs/dataframes-performance#partial-ordering-mode
bpd.options.bigquery.ordering_mode = "partial"

# input_data is defined in an earlier step.
evaluation_data = input_data[input_data["dataframe"] == "evaluation"]

# For more information, see the BigQuery DataFrames API reference documentation:
# https://dataframes.bigquery.dev/reference/api/bigframes.bigquery.ml.evaluate.html#bigframes.bigquery.ml.evaluate
ml.evaluate(
    your_model_id,  # For example: "your-project.bqml_tutorial.tree_model"
    input_=evaluation_data,
)
# Output:
#    precision    recall  accuracy  f1_score  log_loss   roc_auc
# 0   0.671924  0.578804  0.839429  0.621897  0.344054  0.887335
```

評估指標顯示模型效能良好，尤其是[`roc_auc` 分數](https://developers.google.com/machine-learning/crash-course/classification/roc-and-auc?hl=zh-tw)大於 `0.8`。

如要進一步瞭解評估指標，請參閱「[輸出](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-evaluate?hl=zh-tw#output)」。

## 使用模型預測分類

### SQL

如要使用模型預測資料，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中貼入下列查詢，然後點選「執行」：

   ```
     SELECT
       *
     FROM
       ML.PREDICT (MODEL `bqml_tutorial.tree_model`,
         (
         SELECT
           *
         FROM
           `bqml_tutorial.input_data`
         WHERE
           dataframe = 'prediction'
         )
       );
   ```

結果的前幾欄應如下所示：

```
  +---------------------------+--------------------------------------+-------------------------------------+
  | predicted_income_bracket  | predicted_income_bracket_probs.label | predicted_income_bracket_probs.prob |
  +---------------------------+--------------------------------------+-------------------------------------+
  |  <=50K                    |  >50K                                | 0.05183430016040802                 |
  +---------------------------+--------------------------------------+-------------------------------------+
  |                           |  <50K                                | 0.94816571474075317                 |
  +---------------------------+--------------------------------------+-------------------------------------+
  |  <=50K                    |  >50K                                | 0.00365859130397439                 |
  +---------------------------+--------------------------------------+-------------------------------------+
  |                           |  <50K                                | 0.99634140729904175                 |
  +---------------------------+--------------------------------------+-------------------------------------+
  |  <=50K                    |  >50K                                | 0.037775970995426178                |
  +---------------------------+--------------------------------------+-------------------------------------+
  |                           |  <50K                                | 0.96222406625747681                 |
  +---------------------------+--------------------------------------+-------------------------------------+
```

### BigQuery DataFrames

在嘗試這個範例之前，請按照[使用 BigQuery DataFrames 的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/dataframes-quickstart?hl=zh-tw)，完成 BigQuery DataFrames 設定。詳情請參閱 [BigQuery DataFrames 參考文件](https://docs.cloud.google.com/python/docs/reference/bigframes/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。
詳情請參閱「[為本機開發環境設定 ADC](https://docs.cloud.google.com/docs/authentication/set-up-adc-local-dev-environment?hl=zh-tw)」。

```
import bigframes.pandas as bpd
from bigframes.bigquery import ml

# Set partial ordering mode for BigQuery DataFrames.
# For more information, see the BigQuery DataFrames performance documentation:
# https://cloud.google.com/bigquery/docs/dataframes-performance#partial-ordering-mode
bpd.options.bigquery.ordering_mode = "partial"

# input_data is defined in an earlier step.
prediction_data = input_data[input_data["dataframe"] == "prediction"]

# For more information, see the BigQuery DataFrames API reference documentation:
# https://dataframes.bigquery.dev/reference/api/bigframes.bigquery.ml.predict.html#bigframes.bigquery.ml.predict
ml.predict(
    your_model_id,  # For example: "your-project.bqml_tutorial.tree_model"
    input_=prediction_data,
)
# Output:
# predicted_income_bracket   predicted_income_bracket_probs.label  predicted_income_bracket_probs.prob
#                   <=50K                                   >50K                   0.05183430016040802
#                                                           <50K                   0.94816571474075317
#                   <=50K                                   >50K                   0.00365859130397439
#                                                           <50K                   0.99634140729904175
#                   <=50K                                   >50K                   0.037775970995426178
#                                                           <50K                   0.96222406625747681
```

`predicted_income_bracket` 包含模型預測值。
`predicted_income_bracket_probs.label` 會顯示模型必須從中選擇的兩個標籤，而 `predicted_income_bracket_probs.prob` 欄則會顯示指定標籤是正確標籤的機率。

如要進一步瞭解輸出資料欄，請參閱「[分類模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-predict?hl=zh-tw#classification_models)」。

## 清除所用資源

為避免因為本教學課程所用資源，導致系統向 Google Cloud 帳戶收取費用，請刪除含有相關資源的專案，或者保留專案但刪除個別資源。

* 您可以刪除建立的專案。
* 或者您可以保留專案並刪除資料集。

### 刪除資料集

刪除專案將移除專案中所有的資料集與資料表。若您希望重新使用專案，您可以刪除本教學課程中所建立的資料集。

1. 如有需要，請在Google Cloud 控制台中開啟 BigQuery 頁面。

   [前往 BigQuery 頁面](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在導覽窗格中，按一下您建立的 **bqml\_tutorial** 資料集。
3. 按一下視窗右側的「刪除資料集」。
   這個動作將會刪除資料集、資料表，以及所有資料。
4. 在「Delete dataset」(刪除資料集) 對話方塊中，輸入資料集的名稱 (`bqml_tutorial`)，然後按一下「Delete」(刪除) 來確認刪除指令。

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

* 瞭解如何[建立邏輯迴歸分類模型](https://docs.cloud.google.com/bigquery/docs/logistic-regression-prediction?hl=zh-tw)。
* 如需 BigQuery ML 的總覽，請參閱「[BigQuery 中的 AI 和 ML 簡介](https://docs.cloud.google.com/bigquery/docs/bqml-introduction?hl=zh-tw)」。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-10-24 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-10-24 (世界標準時間)。"],[],[]]