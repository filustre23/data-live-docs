Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見

# 使用 BigQuery ML 預測企鵝重量 透過集合功能整理內容 你可以依據偏好儲存及分類內容。

在本教學課程中，您將使用 BigQuery ML 中的[線性迴歸模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-glm?hl=zh-tw)，根據企鵝的人口統計資訊預測企鵝的體重。線性迴歸是一種迴歸模型，可根據輸入特徵的線性組合產生連續值。

本教學課程使用 [`bigquery-public-data.ml_datasets.penguins`](https://console.cloud.google.com/bigquery?p=bigquery-public-data&%3Bd=ml_datasets&%3Bt=penguins&%3Bpage=table&hl=zh-tw) 資料集。

## 目標

在本教學課程中，您將執行下列工作：

* 建立線性迴歸模型。
* 評估模型。
* 使用模型進行預測。

## 費用

本教學課程使用 Google Cloud的計費元件，包括：

* BigQuery
* BigQuery ML

如要進一步瞭解 BigQuery 費用，請參閱 [BigQuery 定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw)頁面。

如要進一步瞭解 BigQuery ML 費用，請參閱「[BigQuery ML 定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#bqml)」一文。

## 事前準備

1. 在 Google Cloud 控制台的專案選擇器頁面中，選取或建立 Google Cloud 專案。

   **選取或建立專案所需的角色**

   * **選取專案**：選取專案時，不需要具備特定 IAM 角色，只要您在專案中獲派角色，即可選取該專案。
   * **建立專案**：如要建立專案，您需要「專案建立者」角色 (`roles/resourcemanager.projectCreator`)，其中包含 `resourcemanager.projects.create` 權限。[瞭解如何授予角色](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)。
   **注意**：如果您不打算保留在這項程序中建立的資源，請建立新專案，而不要選取現有專案。完成這些步驟後，您就可以刪除專案，並移除與該專案相關聯的所有資源。

   [前往專案選取器](https://console.cloud.google.com/projectselector2/home/dashboard?hl=zh-tw)
2. [確認專案已啟用計費功能 Google Cloud](https://docs.cloud.google.com/billing/docs/how-to/verify-billing-enabled?hl=zh-tw#confirm_billing_is_enabled_on_a_project) 。
3. 如果尚未啟用 BigQuery API，請啟用。

   **啟用 API 時所需的角色**

   如要啟用 API，您必須具備 `serviceusage.services.enable` 權限。如果您建立了專案，可能已透過「擁有者」角色 (`roles/owner`) 取得這項權限。否則，您可以透過「服務使用情形管理員」角色 (`roles/serviceusage.serviceUsageAdmin`) 取得這項權限。[瞭解如何授予角色](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)。

   [啟用 API](https://console.cloud.google.com/apis/enableflow?apiid=bigquery.googleapis.com&hl=zh-tw)

## 所需權限

如要使用 BigQuery ML 建立模型，您需要下列 IAM 權限：

* `bigquery.jobs.create`
* `bigquery.models.create`
* `bigquery.models.getData`
* `bigquery.models.updateData`
* `bigquery.models.updateMetadata`

如要執行推論，您需要下列權限：

* 模型上的 `bigquery.models.getData`
* `bigquery.jobs.create`

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

## 建立模型

使用 BigQuery 的 Analytics 範例資料集建立線性迴歸模型。

### SQL

您可以使用 [`CREATE MODEL` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-glm?hl=zh-tw)建立線性迴歸模型，並指定模型類型為 `LINEAR_REG`。建立模型包括訓練模型。

以下是 `CREATE MODEL` 陳述式的實用資訊：

* [`input_label_cols`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-glm?hl=zh-tw#input_label_cols) 選項會指定 `SELECT` 陳述式中的哪個資料欄做為標籤資料欄。這裡的標籤資料欄是 `body_mass_g`。針對線性迴歸模型，標籤資料欄必須是實值，也就是說，資料欄值必須是實數。
* 這項查詢的 `SELECT` 陳述式會使用 `bigquery-public-data.ml_datasets.penguins` 資料表中的下列資料欄，預測企鵝的體重：

  + `species`：企鵝的物種。
  + `island`：企鵝所在的島嶼。
  + `culmen_length_mm`：企鵝的喙長，單位為毫米。
  + `culmen_depth_mm`：企鵝喙的深度 (以毫米為單位)。
  + `flipper_length_mm`：企鵝翅膀的長度 (以毫米為單位)。
  + `sex`：企鵝的性別。
* 這項查詢的 `SELECT` 陳述式中的 `WHERE` 子句 (`WHERE body_mass_g IS
  NOT NULL`) 會排除 `body_mass_g` 欄為 `NULL` 的資料列。

執行查詢來建立線性迴歸模型：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中執行下列查詢：

   ```
   CREATE OR REPLACE MODEL `bqml_tutorial.penguins_model`
   OPTIONS
     (model_type='linear_reg',
     input_label_cols=['body_mass_g']) AS
   SELECT
     *
   FROM
     `bigquery-public-data.ml_datasets.penguins`
   WHERE
     body_mass_g IS NOT NULL;
   ```
3. 建立 `penguins_model` 模型大約需要 30 秒。

   如要查看模型，請按照下列步驟操作：

   1. 點選左側窗格中的 explore「Explorer」。

      如果沒有看到左側窗格，請按一下 last\_page「Expand left pane」(展開左側窗格)，開啟窗格。
   2. 在「Explorer」窗格中展開專案，然後按一下「Datasets」(資料集)。
   3. 按一下「`bqml_tutorial`」資料集。
   4. 按一下「模型」分頁標籤。

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

# Load data from BigQuery
bq_df = bpd.read_gbq("bigquery-public-data.ml_datasets.penguins")

# Drop rows with nulls to get training data
training_data = bq_df.dropna(subset=["body_mass_g"])

# A Linear Regression model predicts a continuous numerical value.
#
# Use ml.create_model to create and train the model in BigQuery.
# The options parameter specifies the model type and the label column.
# For more information, see the BigQuery DataFrames API reference documentation:
# https://dataframes.bigquery.dev/reference/api/bigframes.bigquery.ml.create_model.html#bigframes.bigquery.ml.create_model
ml.create_model(
    your_model_id,  # For example: "bqml_tutorial.penguins_model",
    options={
        "model_type": "LINEAR_REG",
        "input_label_cols": ["body_mass_g"],
    },
    training_data=training_data,
    replace=True,
)
```

建立模型大約需要 30 秒。如要查看模型，請按照下列步驟操作：

1. 點選左側窗格中的 explore「Explorer」。
2. 在「Explorer」窗格中展開專案，然後按一下「Datasets」(資料集)。
3. 按一下「`bqml_tutorial`」資料集。
4. 按一下「模型」分頁標籤。

## 取得訓練統計資料

如要查看模型訓練結果，可以使用 [`ML.TRAINING_INFO` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-train?hl=zh-tw)，也可以在 Google Cloud 控制台中查看統計資料。在本教學課程中，您將使用 Google Cloud 控制台。

機器學習演算法建構模型時，會檢視大量的例子，藉此找出能將損失降到最低的模型。這個過程稱為經驗風險最小化。

損失是預測錯誤的懲罰。這個數字代表模型對單一範例的預測有多不準確。如果這個模型的預測是完美的，則損失為 0，否則損失會大於 0。訓練模型的目的是從所有例子中找到平均損失分數低的一組權重和偏誤。

查看執行 `CREATE MODEL` 查詢時產生的模型訓練統計資料：

1. 點選左側窗格中的 explore「Explorer」。
2. 在「Explorer」窗格中展開專案，然後按一下「Datasets」(資料集)。
3. 按一下「`bqml_tutorial`」資料集。
4. 按一下「模型」分頁標籤。
5. 如要開啟模型資訊窗格，請按一下「penguins\_model」**penguins\_model**。
6. 點選「訓練」分頁標籤，然後點選「表格」。結果應如下所示：

   「Training Data Loss」資料欄代表在訓練資料集上訓練模型後計算出來的損失指標。由於您執行的是線性迴歸，這個資料欄會顯示[均方誤差](https://developers.google.com/machine-learning/glossary/?hl=zh-tw#MSE)值。這項訓練會自動使用[normal\_equation](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-glm?hl=zh-tw#optimize_strategy)最佳化策略，因此只需一次疊代，即可收斂至最終模型。如要進一步瞭解如何設定模型最佳化策略，請參閱 [`optimize_strategy`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-glm?hl=zh-tw#optimize_strategy)。

## 評估模型

建立模型後，請使用 [`ML.EVALUATE` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-evaluate?hl=zh-tw)或 [`bigframes.bigquery.ml.evaluate` BigQuery DataFrames 函式](https://dataframes.bigquery.dev/reference/api/bigframes.bigquery.ml.evaluate.html#bigframes.bigquery.ml.evaluate)，根據實際資料評估模型產生的預測值，藉此評估模型成效。

### SQL

`ML.EVALUATE` 函式會將訓練好的模型和資料集做為輸入內容，而資料集必須符合您用來訓練模型的資料結構定義。在正式環境中，您應使用與模型訓練資料不同的資料評估模型。如果您在執行 `ML.EVALUATE` 時未提供輸入資料，函式會擷取訓練期間計算的評估指標。系統會使用自動保留的評估資料集計算這些指標：

```
    SELECT
      *
    FROM
      ML.EVALUATE(MODEL bqml_tutorial.penguins_model);
```

執行 `ML.EVALUATE` 查詢：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中執行下列查詢：

   ```
     SELECT
       *
     FROM
       ML.EVALUATE(MODEL `bqml_tutorial.penguins_model`,
         (
         SELECT
           *
         FROM
           `bigquery-public-data.ml_datasets.penguins`
         WHERE
           body_mass_g IS NOT NULL));
   ```

### BigQuery DataFrames

在嘗試這個範例之前，請按照[使用 BigQuery DataFrames 的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/dataframes-quickstart?hl=zh-tw)，完成 BigQuery DataFrames 設定。詳情請參閱 [BigQuery DataFrames 參考文件](https://docs.cloud.google.com/python/docs/reference/bigframes/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。
詳情請參閱「[為本機開發環境設定 ADC](https://docs.cloud.google.com/docs/authentication/set-up-adc-local-dev-environment?hl=zh-tw)」。

```
# Use the ml.evaluate method to evaluate the model with test data.
# For more information, see the BigQuery DataFrames API reference documentation:
# https://dataframes.bigquery.dev/reference/api/bigframes.bigquery.ml.evaluate.html#bigframes.bigquery.ml.evaluate
ml.evaluate(
    your_model_id,  # For example: "bqml_tutorial.penguins_model",
    input_=training_data,
)
# Expected output results:
# index  mean_absolute_error  mean_squared_error  mean_squared_log_error  median_absolute_error  r2_score  explained_variance
#   0        227.012237         81838.159892            0.00507                173.080816        0.872377    0.872377
#   1 rows x 6 columns
```

結果應如下所示：

由於您執行了線性迴歸，因此結果包含以下資料欄：

* `mean_absolute_error`
* `mean_squared_error`
* `mean_squared_log_error`
* `median_absolute_error`
* `r2_score`
* `explained_variance`

評估結果中的重要指標是 [R2 分數](https://en.wikipedia.org/wiki/Coefficient_of_determination)。R2 分數是統計測量值，可判斷線性迴歸預測值是否與實際資料相近。`0` 值表示模型無法說明回應資料在平均值附近的變異性。`1` 值表示模型會說明回應資料在平均值附近的所有變異性。

您也可以在 Google Cloud 控制台
查看模型的資訊窗格，瞭解評估指標：

## 使用模型預測結果

現在您已評估了模型，下一步將要用此模型來預測結果，您可以在模型上執行 [`ML.PREDICT` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-predict?hl=zh-tw)或 [`bigframes.bigquery.ml.predict` BigQuery DataFrames 函式](https://dataframes.bigquery.dev/reference/api/bigframes.bigquery.ml.predict.html#bigframes.bigquery.ml.predict)，預測居住在比斯科群島的所有企鵝體重 (以公克為單位)。

### SQL

就輸入內容而言，`ML.PREDICT` 函式會採用訓練好的模型和資料集，該資料集符合您用來訓練模型的資料結構定義，但不包括標籤欄。

執行 `ML.PREDICT` 查詢：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中執行下列查詢：

   ```
   SELECT
   *
   FROM
   ML.PREDICT(MODEL `bqml_tutorial.penguins_model`,
     (
     SELECT
       *
     FROM
       `bigquery-public-data.ml_datasets.penguins`
     WHERE island = 'Biscoe'));
   ```

### BigQuery DataFrames

在嘗試這個範例之前，請按照[使用 BigQuery DataFrames 的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/dataframes-quickstart?hl=zh-tw)，完成 BigQuery DataFrames 設定。詳情請參閱 [BigQuery DataFrames 參考文件](https://docs.cloud.google.com/python/docs/reference/bigframes/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。
詳情請參閱「[為本機開發環境設定 ADC](https://docs.cloud.google.com/docs/authentication/set-up-adc-local-dev-environment?hl=zh-tw)」。

```
# Load data from BigQuery
bq_df = bpd.read_gbq("bigquery-public-data.ml_datasets.penguins")

# Use 'contains' function to filter by island containing the string
# "Biscoe".
biscoe_data = bq_df[bq_df["island"].str.contains("Biscoe")]

# Use the ml.predict method to predict results using your model.
# For more information, see the BigQuery DataFrames API reference documentation:
# https://dataframes.bigquery.dev/reference/api/bigframes.bigquery.ml.predict.html#bigframes.bigquery.ml.predict
ml.predict(
    your_model_id,  # For example: "bqml_tutorial.penguins_model",
    input_=biscoe_data,
)

# Expected output results:
#     predicted_body_mass_g  	      species	                island	 culmen_length_mm  culmen_depth_mm   body_mass_g 	flipper_length_mm	sex
# 23	  4681.782896	   Gentoo penguin (Pygoscelis papua)	Biscoe	      <NA>	            <NA>	        <NA>	          <NA>	        <NA>
# 332	  4740.7907	       Gentoo penguin (Pygoscelis papua)	Biscoe	      46.2	            14.4	        214.0	          4650.0	    <NA>
# 160	  4731.310452	   Gentoo penguin (Pygoscelis papua)	Biscoe	      44.5	            14.3	        216.0	          4100.0	    <NA>
```

結果應如下所示：

## 說明預測結果

### SQL

如要瞭解模型產生這些預測結果的原因，可以使用 [`ML.EXPLAIN_PREDICT` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-explain-predict?hl=zh-tw)。

`ML.EXPLAIN_PREDICT` 是 `ML.PREDICT` 函式的擴充版本。
`ML.EXPLAIN_PREDICT` 不僅會輸出預測結果，還會輸出額外資料欄來解釋預測結果。實務上，您可以執行 `ML.EXPLAIN_PREDICT`，而不是 `ML.PREDICT`。詳情請參閱 [BigQuery ML 可解釋 AI 總覽](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-xai-overview?hl=zh-tw#explainable_ai_offerings_in_bigquery_ml)。

執行 `ML.EXPLAIN_PREDICT` 查詢：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

[前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)

1. 在查詢編輯器中執行下列查詢：

```
SELECT
  *
FROM
  ML.EXPLAIN_PREDICT(MODEL `bqml_tutorial.penguins_model`,
    (
    SELECT
      *
    FROM
      `bigquery-public-data.ml_datasets.penguins`
    WHERE island = 'Biscoe'),
    STRUCT(3 as top_k_features));
```

1. 結果應如下所示：

**注意：** `ML.EXPLAIN_PREDICT` 查詢會輸出所有輸入特徵資料欄，與 `ML.PREDICT` 的做法類似。為方便閱讀，上圖只顯示一個特徵資料欄 `species`。

### BigQuery DataFrames

在嘗試這個範例之前，請按照[使用 BigQuery DataFrames 的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/dataframes-quickstart?hl=zh-tw)，完成 BigQuery DataFrames 設定。詳情請參閱 [BigQuery DataFrames 參考文件](https://docs.cloud.google.com/python/docs/reference/bigframes/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。
詳情請參閱「[為本機開發環境設定 ADC](https://docs.cloud.google.com/docs/authentication/set-up-adc-local-dev-environment?hl=zh-tw)」。

```
# Use the ml.explain_predict method to understand why the model is
# generating these prediction results.
# For more information, see the BigQuery DataFrames API reference documentation:
# https://dataframes.bigquery.dev/reference/api/bigframes.bigquery.ml.explain_predict.html#bigframes.bigquery.ml.explain_predict
#
# Using the trained model and utilizing data specific to Biscoe Island,
# explain the predictions of the top 3 features.
ml.explain_predict(
    your_model_id,  # For example: "bqml_tutorial.penguins_model",
    input_=biscoe_data,
    top_k_features=3,
)

# Expected results:
#   predicted_body_mass_g               top_feature_attributions	        baseline_prediction_value	prediction_value	approximation_error	              species	            island	culmen_length_mm	culmen_depth_mm	flipper_length_mm	body_mass_g	    sex
# 0	 5413.510134	        [{'feature': 'island', 'attribution': 7348.877...	-5320.222128	          5413.510134	            0.0	         Gentoo penguin (Pygoscelis papua)	Biscoe	    45.2	              16.4	        223.0	           5950.0	    MALE
# 1	 4768.351092            [{'feature': 'island', 'attribution': 7348.877...	-5320.222128	          4768.351092	            0.0	         Gentoo penguin (Pygoscelis papua)	Biscoe	    46.5	              14.5	        213.0	           4400.0	   FEMALE
# 2	 3235.896372	        [{'feature': 'island', 'attribution': 7348.877...	-5320.222128	          3235.896372	            0.0	        Adelie Penguin (Pygoscelis adeliae)	Biscoe	    37.7	              16.0          183.0	           3075.0	   FEMALE
# 3	 5349.603734	        [{'feature': 'island', 'attribution': 7348.877...	-5320.222128	          5349.603734	            0.0	         Gentoo penguin (Pygoscelis papua)	Biscoe	    46.4	              15.6	        221.0	           5000.0	    MALE
# 4	 4637.165037	        [{'feature': 'island', 'attribution': 7348.877...	-5320.222128	          4637.165037	            0.0	         Gentoo penguin (Pygoscelis papua)	Biscoe	    46.1	              13.2	        211.0	           4500.0	   FEMALE
```

對於線性迴歸模型，系統會使用夏普利值，為模型中的每個特徵產生特徵歸因值。輸出內容會包含 `penguins` 表格中每列的前三項特徵歸因，因為 `top_k_features` 已設為 `3`。這些歸因會依歸因的絕對值遞減排序。在所有範例中，特徵 `sex` 對整體預測的影響最大。

## 從全域角度說明模型

### SQL

如要瞭解哪些特徵通常最重要，可決定企鵝權重，請使用 [`ML.GLOBAL_EXPLAIN` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-global-explain?hl=zh-tw)。如要使用 `ML.GLOBAL_EXPLAIN`，請務必將 `ENABLE_GLOBAL_EXPLAIN` 選項設為 `TRUE`，然後重新訓練模型。

重新訓練模型並取得全域說明：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

[前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)

1. 在查詢編輯器中執行下列查詢，重新訓練模型：

   ```
   #standardSQL
   CREATE OR REPLACE MODEL `bqml_tutorial.penguins_model`
   OPTIONS (
     model_type = 'linear_reg',
     input_label_cols = ['body_mass_g'],
     enable_global_explain = TRUE)
   AS
   SELECT
   *
   FROM
   `bigquery-public-data.ml_datasets.penguins`
   WHERE
   body_mass_g IS NOT NULL;
   ```
2. 在查詢編輯器中執行下列查詢，取得全域說明：

   ```
   SELECT
   *
   FROM
   ML.GLOBAL_EXPLAIN(MODEL `bqml_tutorial.penguins_model`)
   ```
3. 結果應如下所示：

### BigQuery DataFrames

在嘗試這個範例之前，請按照[使用 BigQuery DataFrames 的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/dataframes-quickstart?hl=zh-tw)，完成 BigQuery DataFrames 設定。詳情請參閱 [BigQuery DataFrames 參考文件](https://docs.cloud.google.com/python/docs/reference/bigframes/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。
詳情請參閱「[為本機開發環境設定 ADC](https://docs.cloud.google.com/docs/authentication/set-up-adc-local-dev-environment?hl=zh-tw)」。

```
# To use the ml.global_explain method, the model must be created with
# enable_global_explain set to True.
#
# Use ml.create_model to create and train the model in BigQuery.
# The options parameter specifies the model type and the label column.
# For more information, see the BigQuery DataFrames API reference documentation:
# https://dataframes.bigquery.dev/reference/api/bigframes.bigquery.ml.create_model.html#bigframes.bigquery.ml.create_model
training_data = bq_df.dropna(subset=["body_mass_g"])
ml.create_model(
    your_model_id,  # For example: "bqml_tutorial.penguins_model",
    options={
        "model_type": "LINEAR_REG",
        "input_label_cols": ["body_mass_g"],
        "enable_global_explain": True,
    },
    training_data=training_data,
    replace=True,
)

# Use the ml.global_explain method to explain the model.
# For more information, see the BigQuery DataFrames API reference documentation:
# https://dataframes.bigquery.dev/reference/api/bigframes.bigquery.ml.global_explain.html#bigframes.bigquery.ml.global_explain
ml.global_explain(
    your_model_id,  # For example: "bqml_tutorial.penguins_model",
)

# Expected results:
#                       attribution
# feature
# island	            5737.315921
# species	            4073.280549
# sex	                622.070896
# flipper_length_mm	    193.612051
# culmen_depth_mm	    117.084944
# culmen_length_mm	    94.366793
```

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
4. 在「Delete dataset」(刪除資料集) 對話方塊中，輸入資料集的名稱 (`bqml_tutorial`)，然後按一下 [Delete] (刪除) 來確認刪除指令。

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
* 如要瞭解如何建立模型，請參閱[`CREATE MODEL`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create?hl=zh-tw)語法頁面。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-10-22 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-10-22 (世界標準時間)。"],[],[]]