* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見

# 使用矩陣分解模型，根據明確意見回饋建立建議 透過集合功能整理內容 你可以依據偏好儲存及分類內容。

本教學課程說明如何建立[矩陣分解模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-matrix-factorization?hl=zh-tw)，並使用 [`movielens1m`](https://grouplens.org/datasets/movielens/1m/) 資料集中的顧客電影評分訓練模型。然後使用矩陣分解模型，為使用者產生電影建議。

使用顧客提供的評分訓練模型，稱為使用*明確意見回饋*訓練。使用明確意見回饋做為訓練資料時，系統會使用[交替最小平方演算法](https://en.wikipedia.org/wiki/Matrix_completion#Alternating_least_squares_minimization)訓練矩陣分解模型。

**重要事項：** 您必須預訂才能使用矩陣因式分解模型。詳情請參閱[定價](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-matrix-factorization?hl=zh-tw#pricing)。

## 目標

本教學課程會逐步引導您完成下列工作：

* 使用 `CREATE MODEL` 陳述式建立矩陣分解模型。
* 使用 [`ML.EVALUATE` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-evaluate?hl=zh-tw)評估模型。
* 使用 [`ML.RECOMMEND` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-recommend?hl=zh-tw)，透過模型為使用者產生電影推薦。

## 費用

本教學課程使用 Google Cloud的計費元件，包括：

* BigQuery
* BigQuery ML

如要進一步瞭解 BigQuery 費用，請參閱 [BigQuery 定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw)頁面。

如要進一步瞭解 BigQuery ML 費用，請參閱 [BigQuery ML 定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#bqml)。

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

## 所需權限

* 如要建立資料集，您需要 `bigquery.datasets.create` IAM 權限。
* 如要建立模型，您需要下列權限：

  + `bigquery.jobs.create`
  + `bigquery.models.create`
  + `bigquery.models.getData`
  + `bigquery.models.updateData`
* 如要執行推論，您需要下列權限：

  + `bigquery.models.getData`
  + `bigquery.jobs.create`

如要進一步瞭解 BigQuery 中的 IAM 角色和權限，請參閱 [IAM 簡介](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)。

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
詳情請參閱 [BigQuery DataFrames 參考說明文件](https://docs.cloud.google.com/python/docs/reference/bigframes/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。
詳情請參閱「[為本機開發環境設定 ADC](https://docs.cloud.google.com/docs/authentication/set-up-adc-local-dev-environment?hl=zh-tw)」。

```
import google.cloud.bigquery

bqclient = google.cloud.bigquery.Client()
bqclient.create_dataset("bqml_tutorial", exists_ok=True)
```

## 上傳 Movielens 資料

將 `movielens1m` 資料上傳至 BigQuery。

### CLI

請按照下列步驟，使用 [bq 指令列工具](https://docs.cloud.google.com/bigquery/docs/bq-command-line-tool?hl=zh-tw)上傳 `movielens1m` 資料：

1. 開啟 Cloud Shell：

   [啟用 Cloud Shell](https://console.cloud.google.com/bigquery?cloudshell=true&hl=zh-tw)
2. 將評分資料上傳至 `ratings` 資料表。在指令列中，貼上以下查詢並按下 `Enter`：

   ```
   curl -O 'http://files.grouplens.org/datasets/movielens/ml-1m.zip'
   unzip ml-1m.zip
   sed 's/::/,/g' ml-1m/ratings.dat > ratings.csv
   bq load --source_format=CSV bqml_tutorial.ratings ratings.csv \
     user_id:INT64,item_id:INT64,rating:FLOAT64,timestamp:TIMESTAMP
   ```
3. 將電影資料上傳至 `movies` 資料表。在指令列中，貼上下列查詢並按下 `Enter`：

   ```
   sed 's/::/@/g' ml-1m/movies.dat > movie_titles.csv
   bq load --source_format=CSV --field_delimiter=@ \
   bqml_tutorial.movies movie_titles.csv \
   movie_id:INT64,movie_title:STRING,genre:STRING
   ```

### BigQuery DataFrames

在嘗試這個範例之前，請按照[使用 BigQuery DataFrames 的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/dataframes-quickstart?hl=zh-tw)中的 BigQuery DataFrames 設定說明操作。
詳情請參閱 [BigQuery DataFrames 參考說明文件](https://docs.cloud.google.com/python/docs/reference/bigframes/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。
詳情請參閱「[為本機開發環境設定 ADC](https://docs.cloud.google.com/docs/authentication/set-up-adc-local-dev-environment?hl=zh-tw)」。

首先，請使用 `bqclient = google.cloud.bigquery.Client()` 建立 `Client` 物件，然後將 `movielens1m` 資料載入您在上一個步驟中建立的資料集。

```
import io
import zipfile

import google.api_core.exceptions
import requests

try:
    # Check if you've already created the Movielens tables to avoid downloading
    # and uploading the dataset unnecessarily.
    bqclient.get_table("bqml_tutorial.ratings")
    bqclient.get_table("bqml_tutorial.movies")
except google.api_core.exceptions.NotFound:
    # Download the https://grouplens.org/datasets/movielens/1m/ dataset.
    ml1m = requests.get("http://files.grouplens.org/datasets/movielens/ml-1m.zip")
    ml1m_file = io.BytesIO(ml1m.content)
    ml1m_zip = zipfile.ZipFile(ml1m_file)

    # Upload the ratings data into the ratings table.
    with ml1m_zip.open("ml-1m/ratings.dat") as ratings_file:
        ratings_content = ratings_file.read()

    ratings_csv = io.BytesIO(ratings_content.replace(b"::", b","))
    ratings_config = google.cloud.bigquery.LoadJobConfig()
    ratings_config.source_format = "CSV"
    ratings_config.write_disposition = "WRITE_TRUNCATE"
    ratings_config.schema = [
        google.cloud.bigquery.SchemaField("user_id", "INT64"),
        google.cloud.bigquery.SchemaField("item_id", "INT64"),
        google.cloud.bigquery.SchemaField("rating", "FLOAT64"),
        google.cloud.bigquery.SchemaField("timestamp", "TIMESTAMP"),
    ]
    bqclient.load_table_from_file(
        ratings_csv, "bqml_tutorial.ratings", job_config=ratings_config
    ).result()

    # Upload the movie data into the movies table.
    with ml1m_zip.open("ml-1m/movies.dat") as movies_file:
        movies_content = movies_file.read()

    movies_csv = io.BytesIO(movies_content.replace(b"::", b"@"))
    movies_config = google.cloud.bigquery.LoadJobConfig()
    movies_config.source_format = "CSV"
    movies_config.field_delimiter = "@"
    movies_config.write_disposition = "WRITE_TRUNCATE"
    movies_config.schema = [
        google.cloud.bigquery.SchemaField("movie_id", "INT64"),
        google.cloud.bigquery.SchemaField("movie_title", "STRING"),
        google.cloud.bigquery.SchemaField("genre", "STRING"),
    ]
    bqclient.load_table_from_file(
        movies_csv, "bqml_tutorial.movies", job_config=movies_config
    ).result()
```

## 建立模型

建立矩陣分解模型，並根據 `ratings` 資料表中的資料訓練模型。模型會根據顧客提供的電影評分進行訓練，預測每個使用者與項目配對的評分。

### SQL

下列 `CREATE MODEL` 陳述式會使用這些資料欄產生建議：

* `user_id`：使用者 ID。
* `item_id`：電影 ID。
* `rating`：使用者給予項目的明確評分，範圍為 1 到 5。

請按照下列步驟建立模型：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中貼入下列查詢，然後點選「執行」：

   ```
   CREATE OR REPLACE MODEL `bqml_tutorial.mf_explicit`
   OPTIONS (
     MODEL_TYPE = 'matrix_factorization',
     FEEDBACK_TYPE = 'explicit',
     USER_COL = 'user_id',
     ITEM_COL = 'item_id',
     L2_REG = 9.83,
     NUM_FACTORS = 34)
   AS
   SELECT
   user_id,
   item_id,
   rating
   FROM `bqml_tutorial.ratings`;
   ```

   查詢作業約需 10 分鐘才能完成，完成後 `mf_explicit` 模型會顯示在「Explorer」窗格中。由於查詢是使用 `CREATE MODEL` 陳述式建立模型，因此您不會看到查詢結果。

### BigQuery DataFrames

在嘗試這個範例之前，請按照[使用 BigQuery DataFrames 的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/dataframes-quickstart?hl=zh-tw)中的 BigQuery DataFrames 設定說明操作。
詳情請參閱 [BigQuery DataFrames 參考說明文件](https://docs.cloud.google.com/python/docs/reference/bigframes/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。
詳情請參閱「[為本機開發環境設定 ADC](https://docs.cloud.google.com/docs/authentication/set-up-adc-local-dev-environment?hl=zh-tw)」。

```
from bigframes.ml import decomposition
import bigframes.pandas as bpd

# Load data from BigQuery
bq_df = bpd.read_gbq(
    "bqml_tutorial.ratings", columns=("user_id", "item_id", "rating")
)

# Create the Matrix Factorization model
model = decomposition.MatrixFactorization(
    num_factors=34,
    feedback_type="explicit",
    user_col="user_id",
    item_col="item_id",
    rating_col="rating",
    l2_reg=9.83,
)
model.fit(bq_df)
model.to_gbq(
    your_model_id, replace=True  # For example: "bqml_tutorial.mf_explicit"
)
```

程式碼約需 10 分鐘才能完成，完成後 `mf_explicit` 模型會顯示在「Explorer」窗格中。

## 取得訓練統計資料

您也可以在Google Cloud 控制台中查看模型的訓練統計資料。

機器學習演算法會使用不同參數建立多個模型疊代版本，然後選取可將[損失](https://en.wikipedia.org/wiki/Loss_function)降到最低的模型版本。這項程序稱為經驗風險最小化。模型訓練統計資料會顯示模型每次疊代的相關損失。

如要查看模型的訓練統計資料，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。

   如果沒有看到左側窗格，請按一下「展開左側窗格」圖示 last\_page 開啟窗格。
3. 在「Explorer」窗格中展開專案，按一下「Datasets」，然後按一下 `bqml_tutorial` 資料集。
4. 按一下「模型」分頁標籤。
5. 按一下 `mf_explicit` 模型，然後按一下「訓練」分頁標籤。
6. 在「查看方式」部分，按一下「表格」。結果應如下所示：

   ```
   +-----------+--------------------+--------------------+
   | Iteration | Training Data Loss | Duration (seconds) |
   +-----------+--------------------+--------------------+
   |  11       | 0.3943             | 42.59              |
   +-----------+--------------------+--------------------+
   |  10       | 0.3979             | 27.37              |
   +-----------+--------------------+--------------------+
   |   9       | 0.4038             | 40.79              |
   +-----------+--------------------+--------------------+
   |  ...      | ...                | ...                |
   +-----------+--------------------+--------------------+
   ```

   「Training Data Loss」資料欄代表模型訓練完成後計算出來的損失指標。由於這是矩陣分解模型，因此這個資料欄會顯示[均方誤差](https://developers.google.com/machine-learning/glossary/?hl=zh-tw#MSE)。

您也可以使用 [`ML.TRAINING_INFO` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-train?hl=zh-tw)查看模型訓練統計資料。

## 評估模型

比較模型傳回的預測電影評分與訓練資料中的實際使用者電影評分，評估模型效能。

### SQL

使用 `ML.EVALUATE` 函式評估模型：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中貼入下列查詢，然後點選「執行」：

   ```
   SELECT
   *
   FROM
   ML.EVALUATE(
     MODEL `bqml_tutorial.mf_explicit`,
     (
       SELECT
         user_id,
         item_id,
         rating
       FROM
         `bqml_tutorial.ratings`
     ));
   ```

   結果應如下所示：

   ```
   +---------------------+---------------------+------------------------+-----------------------+--------------------+--------------------+
   | mean_absolute_error | mean_squared_error  | mean_squared_log_error | median_absolute_error |      r2_score      | explained_variance |
   +---------------------+---------------------+------------------------+-----------------------+--------------------+--------------------+
   | 0.48494444327829156 | 0.39433706592870565 |   0.025437895793637522 |   0.39017059802629905 | 0.6840033369412044 | 0.6840033369412264 |
   +---------------------+---------------------+------------------------+-----------------------+--------------------+--------------------+
   ```

   評估結果中有個重要的指標，就是 [R2 分數](https://en.wikipedia.org/wiki/Coefficient_of_determination)。R2 分數是種統計量具，用來確認線性迴歸的預測結果是否趨近於實際資料。`0` 值代表模型無法解釋平均值周圍之回應資料的變化。`1` 值代表模型能夠解釋所有平均值周圍之回應資料的所有變化。

   如要進一步瞭解 `ML.EVALUATE` 函式輸出內容，請參閱「[輸出內容](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-evaluate?hl=zh-tw#output)」。

您也可以呼叫 `ML.EVALUATE`，不必提供輸入資料。並使用訓練期間計算的評估指標。

### BigQuery DataFrames

在嘗試這個範例之前，請按照[使用 BigQuery DataFrames 的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/dataframes-quickstart?hl=zh-tw)中的 BigQuery DataFrames 設定說明操作。
詳情請參閱 [BigQuery DataFrames 參考說明文件](https://docs.cloud.google.com/python/docs/reference/bigframes/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。
詳情請參閱「[為本機開發環境設定 ADC](https://docs.cloud.google.com/docs/authentication/set-up-adc-local-dev-environment?hl=zh-tw)」。

呼叫 [`model.score()`](https://dataframes.bigquery.dev/reference/api/bigframes.ml.decomposition.MatrixFactorization#bigframes.ml.decomposition.MatrixFactorization.score) 評估模型。

```
# Evaluate the model using the score() function
model.score(bq_df)
# Output:
# mean_absolute_error	mean_squared_error	mean_squared_log_error	median_absolute_error	r2_score	explained_variance
# 0.485403	                0.395052	        0.025515	            0.390573	        0.68343	        0.68343
```

## 取得部分使用者項目組合的預測評分

取得五位使用者對每部電影的預測評分。

### SQL

使用 `ML.RECOMMEND` 函式取得預測評分：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中貼入下列查詢，然後點選「執行」：

   ```
   SELECT
   *
   FROM
   ML.RECOMMEND(
     MODEL `bqml_tutorial.mf_explicit`,
     (
       SELECT
         user_id
       FROM
         `bqml_tutorial.ratings`
       LIMIT 5
     ));
   ```

   結果應如下所示：

   ```
   +--------------------+---------+---------+
   | predicted_rating   | user_id | item_id |
   +--------------------+---------+---------+
   | 4.2125303962491873 | 4       | 3169    |
   +--------------------+---------+---------+
   | 4.8068920531981263 | 4       | 3739    |
   +--------------------+---------+---------+
   | 3.8742203494732403 | 4       | 3574    |
   +--------------------+---------+---------+
   | ...                | ...     | ...     |
   +--------------------+---------+---------+
   ```

### BigQuery DataFrames

在嘗試這個範例之前，請按照[使用 BigQuery DataFrames 的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/dataframes-quickstart?hl=zh-tw)中的 BigQuery DataFrames 設定說明操作。
詳情請參閱 [BigQuery DataFrames 參考說明文件](https://docs.cloud.google.com/python/docs/reference/bigframes/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。
詳情請參閱「[為本機開發環境設定 ADC](https://docs.cloud.google.com/docs/authentication/set-up-adc-local-dev-environment?hl=zh-tw)」。

呼叫 [`model.predict()`](https://dataframes.bigquery.dev/reference/api/bigframes.ml.decomposition.MatrixFactorization#bigframes.ml.decomposition.MatrixFactorization.predict) 即可取得預測評分。

```
# Use predict() to get the predicted rating for each movie for 5 users
subset = bq_df[["user_id"]].head(5)
predicted = model.predict(subset)
print(predicted)
# Output:
#   predicted_rating	user_id	 item_id	rating
# 0	    4.206146	     4354	  968	     4.0
# 1	    4.853099	     3622	  3521	     5.0
# 2	    2.679067	     5543	  920	     2.0
# 3	    4.323458	     445	  3175	     5.0
# 4	    3.476911	     5535	  235	     4.0
```

## 生成建議

根據預測評分，為每位使用者產生前五名推薦電影。

### SQL

請按照下列步驟產生建議：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 將預測評分寫入資料表。在查詢編輯器中貼上以下查詢，然後點選「執行」：

   ```
   CREATE OR REPLACE TABLE `bqml_tutorial.recommend`
   AS
   SELECT
   *
   FROM
   ML.RECOMMEND(MODEL `bqml_tutorial.mf_explicit`);
   ```
3. 將預測評分與電影資訊合併，然後選取每位使用者前五名的結果。在查詢編輯器中貼上以下查詢，然後點選「執行」：

```
  SELECT
    user_id,
    ARRAY_AGG(STRUCT(movie_title, genre, predicted_rating) ORDER BY predicted_rating DESC LIMIT 5)
  FROM
    (
      SELECT
        user_id,
        item_id,
        predicted_rating,
        movie_title,
        genre
      FROM
        `bqml_tutorial.recommend`
      JOIN
        `bqml_tutorial.movies`
        ON
          item_id = movie_id
    )
  GROUP BY
    user_id;
```

結果應如下所示：

```
  +---------+-------------------------------------+------------------------+--------------------+
  | user_id | f0_movie_title                      | f0_genre               | predicted_rating   |
  +---------+-------------------------------------+------------------------+--------------------+
  | 4597    | Song of Freedom (1936)              | Drama                  | 6.8495752907364009 |
  |         | I Went Down (1997)                  | Action/Comedy/Crime    | 6.7203235758772877 |
  |         | Men With Guns (1997)                | Action/Drama           | 6.399407352232001  |
  |         | Kid, The (1921)                     | Action                 | 6.1952890198126731 |
  |         | Hype! (1996)                        | Documentary            | 6.1895766097451475 |
  +---------+-------------------------------------+------------------------+--------------------+
  | 5349    | Fandango (1985)                     | Comedy                 | 9.944574012151549  |
  |         | Breakfast of Champions (1999)       | Comedy                 | 9.55661860430112   |
  |         | Funny Bones (1995)                  | Comedy                 | 9.52778917835076   |
  |         | Paradise Road (1997)                | Drama/War              | 9.1643621767929133 |
  |         | Surviving Picasso (1996)            | Drama                  | 8.807353289233772  |
  +---------+-------------------------------------+------------------------+--------------------+
  | ...     | ...                                 | ...                    | ...                |
  +---------+-------------------------------------+------------------------+--------------------+
```

### BigQuery DataFrames

在嘗試這個範例之前，請按照[使用 BigQuery DataFrames 的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/dataframes-quickstart?hl=zh-tw)中的 BigQuery DataFrames 設定說明操作。
詳情請參閱 [BigQuery DataFrames 參考說明文件](https://docs.cloud.google.com/python/docs/reference/bigframes/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。
詳情請參閱「[為本機開發環境設定 ADC](https://docs.cloud.google.com/docs/authentication/set-up-adc-local-dev-environment?hl=zh-tw)」。

呼叫 [`model.predict()`](https://dataframes.bigquery.dev/reference/api/bigframes.ml.decomposition.MatrixFactorization#bigframes.ml.decomposition.MatrixFactorization.predict) 即可取得預測評分。

```
# import bigframes.bigquery as bbq

# Load movies
movies = bpd.read_gbq("bqml_tutorial.movies")

# Merge the movies df with the previously created predicted df
merged_df = bpd.merge(predicted, movies, left_on="item_id", right_on="movie_id")

# Separate users and predicted data, setting the index to 'movie_id'
users = merged_df[["user_id", "movie_id"]].set_index("movie_id")

# Take the predicted data and sort it in descending order by 'predicted_rating', setting the index to 'movie_id'
sort_data = (
    merged_df[["movie_title", "genre", "predicted_rating", "movie_id"]]
    .sort_values(by="predicted_rating", ascending=False)
    .set_index("movie_id")
)

# re-merge the separated dfs by index
merged_user = sort_data.join(users, how="outer")

# group the users and set the user_id as the index
merged_user.groupby("user_id").head(5).set_index("user_id").sort_index()
print(merged_user)
# Output:
# 	            movie_title	                genre	        predicted_rating
# user_id
#   1	    Saving Private Ryan (1998)	Action|Drama|War	    5.19326
#   1	        Fargo (1996)	       Crime|Drama|Thriller	    4.996954
#   1	    Driving Miss Daisy (1989)	    Drama	            4.983671
#   1	        Ben-Hur (1959)	       Action|Adventure|Drama	4.877622
#   1	     Schindler's List (1993)	   Drama|War	        4.802336
#   2	    Saving Private Ryan (1998)	Action|Drama|War	    5.19326
#   2	        Braveheart (1995)	    Action|Drama|War	    5.174145
#   2	        Gladiator (2000)	      Action|Drama	        5.066372
#   2	        On Golden Pond (1981)	     Drama	            5.01198
#   2	    Driving Miss Daisy (1989)	     Drama	            4.983671
```

## 清除所用資源

為避免因為本教學課程所用資源，導致系統向 Google Cloud 帳戶收取費用，請刪除含有相關資源的專案，或者保留專案但刪除個別資源。

* 您可以刪除建立的專案。
* 或者您可以保留專案並刪除資料集。

### 刪除資料集

刪除專案將移除專案中所有的資料集與資料表。若您希望重新使用專案，您可以刪除本教學課程中所建立的資料集。

1. 如有必要，請在 Google Cloud 控制台中開啟 BigQuery 頁面。

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

* 嘗試[根據隱性意見回饋建立矩陣分解模型](https://docs.cloud.google.com/bigquery/docs/bigqueryml-mf-implicit-tutorial?hl=zh-tw)。
* 如需 BigQuery ML 的總覽，請參閱 [BigQuery ML 簡介](https://docs.cloud.google.com/bigquery/docs/bqml-introduction?hl=zh-tw)。
* 如要進一步瞭解機器學習，請參閱[機器學習速成課程](https://developers.google.com/machine-learning/crash-course/?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-02 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-02 (世界標準時間)。"],[],[]]