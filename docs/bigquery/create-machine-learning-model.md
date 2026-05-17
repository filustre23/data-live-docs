Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 使用 SQL 在 BigQuery ML 中建立機器學習模型

本教學課程說明如何使用 BigQuery ML SQL 查詢建立邏輯迴歸模型。

BigQuery ML 可讓您使用 SQL 查詢，在 BigQuery 中建立及訓練機器學習模型。這樣一來，您就能使用 BigQuery SQL 編輯器等熟悉的工具，更輕鬆地運用機器學習技術，並省去將資料移至獨立機器學習環境的麻煩，進而加快開發速度。

在本教學課程中，不論網站訪客是否確實完成交易，都可以使用 [BigQuery 專用的 Google Analytics 樣本資料集](https://support.google.com/analytics/answer/7586738?ref_topic=3416089&hl=zh-tw)來建立一個預測模型。如要瞭解 Analytics 資料集的結構定義，請參閱 Analytics 說明中心內的「[BigQuery 匯出結構定義](https://support.google.com/analytics/answer/3437719?hl=zh-tw)」。

如要瞭解如何使用 Google Cloud 控制台使用者介面建立模型，請參閱[使用使用者介面處理模型](https://docs.cloud.google.com/bigquery/docs/create-machine-learning-model-console?hl=zh-tw)。

## 目標

本教學課程說明如何執行下列工作：

* 使用 [`CREATE MODEL` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create?hl=zh-tw)建立二元邏輯迴歸模型。
* 使用 [`ML.EVALUATE` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-evaluate?hl=zh-tw)評估模型。
* 使用 [`ML.PREDICT` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-predict?hl=zh-tw)，透過模型進行預測。

## 費用

本教學課程使用 Google Cloud的計費元件，包括：

* BigQuery
* BigQuery ML

如要進一步瞭解 BigQuery 費用，請參閱 [BigQuery 定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw)頁面。

如要進一步瞭解 BigQuery ML 費用，請參閱 [BigQuery ML 定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#bigquery-ml-pricing)。

## 必要的角色

* 如要建立模型及執行推論，您必須獲得下列角色：

  + BigQuery 資料編輯者 (`roles/bigquery.dataEditor`)
  + BigQuery 使用者 (`roles/bigquery.user`)

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
- Make sure that you have the following role or roles on the project:
  BigQuery Data Editor, BigQuery Job User, Service Usage Admin

  #### Check for the roles

  1. In the Google Cloud console, go to the **IAM** page.

     [Go to IAM](https://console.cloud.google.com/projectselector/iam-admin/iam?supportedpurview=project&hl=zh-tw)
  2. Select the project.
  3. In the **Principal** column, find all rows that identify you or a group that
     you're included in. To learn which groups you're included in, contact your
     administrator.
  4. For all rows that specify or include you, check the **Role** column to see whether
     the list of roles includes the required roles.


  #### Grant the roles

  1. In the Google Cloud console, go to the **IAM** page.

     [Go to IAM](https://console.cloud.google.com/projectselector/iam-admin/iam?supportedpurview=project&hl=zh-tw)
  2. Select the project.
  3. Click person\_add **Grant access**.
  4. In the **New principals** field, enter your user identifier.
     This is typically the email address for a Google Account.
  5. Click **Select a role**, then search for the role.- To grant additional roles, click add **Add
       another role** and add each additional role.
     - Click **Save**.

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
- Make sure that you have the following role or roles on the project:
  BigQuery Data Editor, BigQuery Job User, Service Usage Admin

  #### Check for the roles

  1. In the Google Cloud console, go to the **IAM** page.

     [Go to IAM](https://console.cloud.google.com/projectselector/iam-admin/iam?supportedpurview=project&hl=zh-tw)
  2. Select the project.
  3. In the **Principal** column, find all rows that identify you or a group that
     you're included in. To learn which groups you're included in, contact your
     administrator.
  4. For all rows that specify or include you, check the **Role** column to see whether
     the list of roles includes the required roles.


  #### Grant the roles

  1. In the Google Cloud console, go to the **IAM** page.

     [Go to IAM](https://console.cloud.google.com/projectselector/iam-admin/iam?supportedpurview=project&hl=zh-tw)
  2. Select the project.
  3. Click person\_add **Grant access**.
  4. In the **New principals** field, enter your user identifier.
     This is typically the email address for a Google Account.
  5. Click **Select a role**, then search for the role.- To grant additional roles, click add **Add
       another role** and add each additional role.
     - Click **Save**.

1. 新專案會自動啟用 BigQuery。如要在現有專案中啟用 BigQuery，請前往

   啟用 BigQuery API。

   **啟用 API 時所需的角色**

   如要啟用 API，您需要服務使用情形管理員 IAM 角色 (`roles/serviceusage.serviceUsageAdmin`)，其中包含 `serviceusage.services.enable` 權限。[瞭解如何授予角色](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)。

   [啟用 API](https://console.cloud.google.com/apis/enableflow?apiid=bigquery&hl=zh-tw)

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

## 建立邏輯迴歸模型

使用 BigQuery 的 Analytics 範例資料集建立邏輯迴歸模型。

### SQL

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中執行下列陳述式：

   ```
   CREATE OR REPLACE MODEL `bqml_tutorial.sample_model`
   OPTIONS(model_type='logistic_reg') AS
   SELECT
   IF(totals.transactions IS NULL, 0, 1) AS label,
   IFNULL(device.operatingSystem, "") AS os,
   device.isMobile AS is_mobile,
   IFNULL(geoNetwork.country, "") AS country,
   IFNULL(totals.pageviews, 0) AS pageviews
   FROM
   `bigquery-public-data.google_analytics_sample.ga_sessions_*`
   WHERE
   _TABLE_SUFFIX BETWEEN '20160801' AND '20170630'
   ```

   查詢需要幾分鐘才會完成。初次的疊代作業完成後，您的模型 (`sample_model`) 將出現在導覽面板中。由於查詢是使用 `CREATE MODEL` 陳述式建立模型，因此您不會看到查詢結果。

**查詢詳細資料**

`CREATE MODEL` 陳述式會建立模型，然後使用查詢的 `SELECT` 陳述式擷取的資料訓練模型。

`OPTIONS(model_type='logistic_reg')` 子句會建立[邏輯迴歸](https://en.wikipedia.org/wiki/Logistic_regression)模型。邏輯迴歸模型會將輸入資料分成兩個類別，然後估算資料屬於其中一個類別的機率。您想偵測的內容 (例如電子郵件是否為垃圾郵件) 會以 1 表示，其他值則以 0 表示。介於 0 到 1 之間的值表示指定值屬於您要偵測的類別的可能性。舉例來說，如果電子郵件的機率估計值為 0.9，則該郵件有 90% 的機率是垃圾郵件。

這個查詢的 `SELECT` 語法會擷取下列欄位，模型會使用這些欄位預測顧客完成交易的機率：

* `totals.transactions`：訪客於當次工作階段內所達成的電子商務交易總數，若交易次數是 `NULL`，`label` 欄位的值就會被設為 `0`，否則該欄位就會被設定為 `1`，這些值皆可用來表示可能的結果。若要在 `CREATE MODEL` 陳述式中設定 `input_label_cols=` 選項，那麼建立一個名為 `label` 的別名是可行的替代方案。
* `device.operatingSystem`：訪客裝置的作業系統。
* `device.isMobile`：用來表示訪客的裝置是否為行動裝置。
* `geoNetwork.country`：以 IP 位址為依據，顯示工作階段的來源國家/地區。
* `totals.pageviews`：當次工作階段的總檢視頁數。

`FROM` 子句 - 導致查詢使用 `bigquery-public-data.google_analytics_sample.ga_sessions` 範例資料表訓練模型。這些資料表會依日期分割，因此您可以在資料表名稱中使用萬用字元來匯總資料表：`google_analytics_sample.ga_sessions_*`。

`WHERE` 子句 (`_TABLE_SUFFIX BETWEEN '20160801' AND '20170630'`) 會限制查詢掃描的資料表數量。而所掃描的日期區間則是從 2016 年 8 月 1 日到 2017 年 6 月 30 日。

### BigQuery DataFrames

在嘗試這個範例之前，請按照[使用 BigQuery DataFrames 的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/dataframes-quickstart?hl=zh-tw)中的 BigQuery DataFrames 設定說明操作。
詳情請參閱 [BigQuery DataFrames 參考文件](https://docs.cloud.google.com/python/docs/reference/bigframes/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。
詳情請參閱「[為本機開發環境設定 ADC](https://docs.cloud.google.com/docs/authentication/set-up-adc-local-dev-environment?hl=zh-tw)」。

```
from bigframes.ml.linear_model import LogisticRegression
import bigframes.pandas as bpd

# Start by selecting the data you'll use for training. `read_gbq` accepts
# either a SQL query or a table ID. Since this example selects from multiple
# tables via a wildcard, use SQL to define this data. Watch issue
# https://github.com/googleapis/python-bigquery-dataframes/issues/169
# for updates to `read_gbq` to support wildcard tables.

df = bpd.read_gbq_table(
    "bigquery-public-data.google_analytics_sample.ga_sessions_*",
    filters=[
        ("_table_suffix", ">=", "20160801"),
        ("_table_suffix", "<=", "20170630"),
    ],
)

# Extract the total number of transactions within
# the Google Analytics session.
#
# Because the totals column is a STRUCT data type, call
# Series.struct.field("transactions") to extract the transactions field.
# See the reference documentation below:
# https://cloud.google.com/python/docs/reference/bigframes/latest/bigframes.operations.structs.StructAccessor#bigframes_operations_structs_StructAccessor_field
transactions = df["totals"].struct.field("transactions")

# The "label" values represent the outcome of the model's
# prediction. In this case, the model predicts if there are any
# ecommerce transactions within the Google Analytics session.
# If the number of transactions is NULL, the value in the label
# column is set to 0. Otherwise, it is set to 1.
label = transactions.notnull().map({True: 1, False: 0}).rename("label")

# Extract the operating system of the visitor's device.
operating_system = df["device"].struct.field("operatingSystem")
operating_system = operating_system.fillna("")

# Extract whether the visitor's device is a mobile device.
is_mobile = df["device"].struct.field("isMobile")

# Extract the country from which the sessions originated, based on the IP address.
country = df["geoNetwork"].struct.field("country").fillna("")

# Extract the total number of page views within the session.
pageviews = df["totals"].struct.field("pageviews").fillna(0)

# Combine all the feature columns into a single DataFrame
# to use as training data.
features = bpd.DataFrame(
    {
        "os": operating_system,
        "is_mobile": is_mobile,
        "country": country,
        "pageviews": pageviews,
    }
)

# Logistic Regression model splits data into two classes, giving the
# a confidence score that the data is in one of the classes.
model = LogisticRegression()
model.fit(features, label)

# The model.fit() call above created a temporary model.
# Use the to_gbq() method to write to a permanent location.
model.to_gbq(
    your_model_id,  # For example: "bqml_tutorial.sample_model",
    replace=True,
)
```

## 查看模型的損失統計資料

機器學習是指建立一個可透過資料進行預測的模型，此模型是一個可接收資料輸入的功能，並且能夠針對輸入資料進行運算，進而產生輸出，也就是預測。

機器學習演算法會採用多個已知預測結果的範例 (例如使用者購物記錄)，並反覆調整模型中的各種權重，使模型的預測結果與實際值相符。能達到這個目標，是因為機器學習演算法透過「遺失」指標降低模型的錯誤預測。

預期每次疊代時，損失應會減少，最好是降至零。遺失值 0，代表模型具有 100% 的正確率。

訓練模型時，BigQuery ML 會自動將輸入資料拆分為[訓練集和評估集](https://en.wikipedia.org/wiki/Training,_validation,_and_test_data_sets)，避免模型[過度配適](https://en.wikipedia.org/wiki/Overfitting)。這是必要步驟，因為訓練演算法不能過度貼近訓練資料，否則就無法歸納新樣本。

使用 Google Cloud 控制台，查看模型在訓練疊代期間的損失變化：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。

   如果沒有看到左側窗格，請按一下 last\_page「Expand left pane」(展開左側窗格)，開啟窗格。
3. 在「Explorer」窗格中展開專案，按一下「Datasets」，然後按一下 `bqml_tutorial` 資料集。
4. 按一下「模型」分頁標籤，然後按一下 `sample_model` 模型。
5. 按一下「訓練」分頁標籤，然後查看「損失」圖表。「損失」圖表會顯示訓練資料集疊代期間的損失指標變化。將游標懸停在圖表上，您會看到「訓練損失」和「評估損失」的線條。由於您執行的是邏輯迴歸，因此訓練損失值是使用訓練資料計算出的[對數損失](https://en.wikipedia.org/wiki/Cross-entropy#Cross-entropy_loss_function_and_logistic_regression)。評估損失是在評估資料上計算的對數損失。這兩種損失類型都代表平均損失值，是針對每次疊代中各資料集的所有範例計算平均值。

您也可以使用 [`ML.TRAINING_INFO` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-train?hl=zh-tw)查看模型訓練結果。

## 評估模型

使用 `ML.EVALUATE` 函式評估模型效能。`ML.EVALUATE` 函式會根據實際資料來評估模型產生的預測值，如要計算邏輯迴歸專用的指標，可以使用 [`ML.ROC_CURVE` SQL 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-roc?hl=zh-tw)或 [`bigframes.ml.metrics.roc_curve` BigQuery DataFrames 函式](https://dataframes.bigquery.dev/reference/api/bigframes.ml.metrics.roc_curve.html#bigframes.ml.metrics.roc_curve)。

在本教學課程中，您會使用偵測交易的二元分類模型。「`label`」欄中的值是模型產生的兩個類別：「`0`」(無交易) 和「`1`」(已完成交易)。

### SQL

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中執行下列陳述式：

   ```
   SELECT
   *
   FROM
   ML.EVALUATE(MODEL `bqml_tutorial.sample_model`, (
   SELECT
   IF(totals.transactions IS NULL, 0, 1) AS label,
   IFNULL(device.operatingSystem, "") AS os,
   device.isMobile AS is_mobile,
   IFNULL(geoNetwork.country, "") AS country,
   IFNULL(totals.pageviews, 0) AS pageviews
   FROM
   `bigquery-public-data.google_analytics_sample.ga_sessions_*`
   WHERE
   _TABLE_SUFFIX BETWEEN '20170701' AND '20170801'))
   ```

   結果應如下所示：

   ```
     +--------------------+---------------------+---------------------+---------------------+---------------------+--------------------+
     |     precision      |       recall        |      accuracy       |      f1_score       |      log_loss       | roc_auc                   |
     +--------------------+---------------------+---------------------+---------------------+---------------------+--------------------+
     | 0.468503937007874  | 0.11080074487895716 | 0.98534315834767638 | 0.17921686746987953 | 0.04624221101176898    | 0.98174125874125873 |
     +--------------------+---------------------+---------------------+---------------------+---------------------+--------------------+
   ```

   由於您執行了邏輯迴歸，因此結果包含以下資料欄：

   * [`precision`](https://developers.google.com/machine-learning/glossary/?hl=zh-tw#precision)：分類模型的指標，該指標可確認當模型預測到正向類別時的正確發生頻率。
   * [`recall`](https://developers.google.com/machine-learning/glossary/?hl=zh-tw#recall)：分類模型的指標，可用來回答下列問題：在所有可能的正向標籤中，模型可以正確辨識出多少個標籤？
   * [`accuracy`](https://developers.google.com/machine-learning/glossary/?hl=zh-tw#accuracy)：準確率就是分類模型預測成功的比例。
   * [`f1_score`](https://en.wikipedia.org/wiki/F1_score)：
     衡量模型準確率的指標，f1 分數是精確度與召回率的調和平均數，f1 分數的最佳值為 1，最差值為 0。
   * [`log_loss`](https://en.wikipedia.org/wiki/Cross_entropy#Cross-entropy_error_function_and_logistic_regression)：用於邏輯迴歸中的損失函式，可衡量模型預測結果與正確標籤之間的差距。
   * [`roc_auc`](https://developers.google.com/machine-learning/glossary/?hl=zh-tw#AUC)：
     [ROC](https://developers.google.com/machine-learning/glossary/?hl=zh-tw#ROC) 曲線下的面積。也就是分類器對於隨機挑選的正向樣本確實是正向的信心，高於隨機挑選的負向樣本其實是正向的情況發生機率。詳情請參閱機器學習密集課程中的「[分類](https://developers.google.com/machine-learning/crash-course/classification/video-lecture?hl=zh-tw)」一文。

**查詢詳細資料**

初始 `SELECT` 陳述式會擷取模型中的資料欄。

`FROM` 子句會對模型使用 `ML.EVALUATE` 函式。

巢狀 `SELECT` 陳述式和 `FROM` 子句與 `CREATE MODEL` 查詢中的相同。

`WHERE` 子句 (`_TABLE_SUFFIX BETWEEN '20170701' AND '20170801'`) 會限制查詢掃描的資料表數量。而所掃描的日期區間則是從 2017 年 7 月 1 日到 2017 年 8 月 1 日，這正是您用來評估模型預測效能的資料。上述資料收集的時間點是在訓練資料所橫跨的時間區段之後、緊接著的隔月。

### BigQuery DataFrames

在嘗試這個範例之前，請按照[使用 BigQuery DataFrames 的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/dataframes-quickstart?hl=zh-tw)中的 BigQuery DataFrames 設定說明操作。
詳情請參閱 [BigQuery DataFrames 參考文件](https://docs.cloud.google.com/python/docs/reference/bigframes/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。
詳情請參閱「[為本機開發環境設定 ADC](https://docs.cloud.google.com/docs/authentication/set-up-adc-local-dev-environment?hl=zh-tw)」。

```
import bigframes.pandas as bpd

# Select model you'll use for evaluating. `read_gbq_model` loads model data from a
# BigQuery, but you could also use the `model` object from the previous steps.
model = bpd.read_gbq_model(
    your_model_id,  # For example: "bqml_tutorial.sample_model",
)

# The filters parameter limits the number of tables scanned by the query.
# The date range scanned is July 1, 2017 to August 1, 2017. This is the
# data you're using to evaluate the predictive performance of the model.
# It was collected in the month immediately following the time period
# spanned by the training data.
df = bpd.read_gbq_table(
    "bigquery-public-data.google_analytics_sample.ga_sessions_*",
    filters=[
        ("_table_suffix", ">=", "20170701"),
        ("_table_suffix", "<=", "20170801"),
    ],
)

transactions = df["totals"].struct.field("transactions")
label = transactions.notnull().map({True: 1, False: 0}).rename("label")
operating_system = df["device"].struct.field("operatingSystem")
operating_system = operating_system.fillna("")
is_mobile = df["device"].struct.field("isMobile")
country = df["geoNetwork"].struct.field("country").fillna("")
pageviews = df["totals"].struct.field("pageviews").fillna(0)
features = bpd.DataFrame(
    {
        "os": operating_system,
        "is_mobile": is_mobile,
        "country": country,
        "pageviews": pageviews,
    }
)

# Some models include a convenient .score(X, y) method for evaluation with a preset accuracy metric:

# Because you performed a logistic regression, the results include the following columns:

# - precision — A metric for classification models. Precision identifies the frequency with
# which a model was correct when predicting the positive class.

# - recall — A metric for classification models that answers the following question:
# Out of all the possible positive labels, how many did the model correctly identify?

# - accuracy — Accuracy is the fraction of predictions that a classification model got right.

# - f1_score — A measure of the accuracy of the model. The f1 score is the harmonic average of
# the precision and recall. An f1 score's best value is 1. The worst value is 0.

# - log_loss — The loss function used in a logistic regression. This is the measure of how far the
# model's predictions are from the correct labels.

# - roc_auc — The area under the ROC curve. This is the probability that a classifier is more confident that
# a randomly chosen positive example
# is actually positive than that a randomly chosen negative example is positive. For more information,
# see ['Classification']('https://developers.google.com/machine-learning/crash-course/classification/video-lecture')
# in the Machine Learning Crash Course.

model.score(features, label)
#    precision    recall  accuracy  f1_score  log_loss   roc_auc
# 0   0.412621  0.079143  0.985074  0.132812  0.049764  0.974285
# [1 rows x 6 columns]
```

## 使用模型預測結果

使用模型預測各國家/地區網站訪客的交易次數。

### SQL

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中執行下列陳述式：

   ```
   SELECT
   country,
   SUM(predicted_label) as total_predicted_purchases
   FROM
   ML.PREDICT(MODEL `bqml_tutorial.sample_model`, (
   SELECT
   IFNULL(device.operatingSystem, "") AS os,
   device.isMobile AS is_mobile,
   IFNULL(totals.pageviews, 0) AS pageviews,
   IFNULL(geoNetwork.country, "") AS country
   FROM
   `bigquery-public-data.google_analytics_sample.ga_sessions_*`
   WHERE
   _TABLE_SUFFIX BETWEEN '20170701' AND '20170801'))
   GROUP BY country
   ORDER BY total_predicted_purchases DESC
   LIMIT 10
   ```

   結果應如下所示：

   ```
   +----------------+---------------------------+
   |    country     | total_predicted_purchases |
   +----------------+---------------------------+
   | United States  |                       220 |
   | Taiwan         |                         8 |
   | Canada         |                         7 |
   | India          |                         2 |
   | Turkey         |                         2 |
   | Japan          |                         2 |
   | Italy          |                         1 |
   | Brazil         |                         1 |
   | Singapore      |                         1 |
   | Australia      |                         1 |
   +----------------+---------------------------+
   ```

**查詢詳細資料**

初始 `SELECT` 陳述式會擷取 `country` 資料欄，並加總 `predicted_label` 資料欄。`predicted_label` 資料欄是由 `ML.PREDICT` 函式產生。使用 `ML.PREDICT` 函式時，模型的輸出資料欄名稱為 `predicted_<label_column_name>`。對線性迴歸模型來說，`predicted_label` 是 `label` 的估計值。對於邏輯迴歸模型，`predicted_label` 是最能描述指定輸入資料值的標籤，也就是 `0` 或 `1`。

`ML.PREDICT` 函式用於透過模型預測結果。

巢狀 `SELECT` 陳述式和 `FROM` 子句與 `CREATE MODEL` 查詢中的相同。

`WHERE` 子句 (`_TABLE_SUFFIX BETWEEN '20170701' AND '20170801'`) 會限制查詢掃描的資料表數量。而所掃描的日期區間則是從 2017 年 7 月 1 日到 2017 年 8 月 1 日，這正是您執行預測所使用的資料。每當時間區段橫跨訓練資料之後，就會立刻收集月份資料。

`GROUP BY` 和 `ORDER BY` 子句會依國家/地區將結果分組，並依預測購買量總和遞減排序。

`LIMIT` 子句在此處的用途是僅顯示前 10 筆查詢結果。

### BigQuery DataFrames

在嘗試這個範例之前，請按照[使用 BigQuery DataFrames 的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/dataframes-quickstart?hl=zh-tw)中的 BigQuery DataFrames 設定說明操作。
詳情請參閱 [BigQuery DataFrames 參考文件](https://docs.cloud.google.com/python/docs/reference/bigframes/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。
詳情請參閱「[為本機開發環境設定 ADC](https://docs.cloud.google.com/docs/authentication/set-up-adc-local-dev-environment?hl=zh-tw)」。

```
import bigframes.pandas as bpd

# Select model you'll use for predicting.
# `read_gbq_model` loads model data from
# BigQuery, but you could also use the `model`
# object from the previous steps.
model = bpd.read_gbq_model(
    your_model_id,  # For example: "bqml_tutorial.sample_model",
)

# The filters parameter limits the number of tables scanned by the query.
# The date range scanned is July 1, 2017 to August 1, 2017. This is the
# data you're using to make the prediction.
# It was collected in the month immediately following the time period
# spanned by the training data.
df = bpd.read_gbq_table(
    "bigquery-public-data.google_analytics_sample.ga_sessions_*",
    filters=[
        ("_table_suffix", ">=", "20170701"),
        ("_table_suffix", "<=", "20170801"),
    ],
)

operating_system = df["device"].struct.field("operatingSystem")
operating_system = operating_system.fillna("")
is_mobile = df["device"].struct.field("isMobile")
country = df["geoNetwork"].struct.field("country").fillna("")
pageviews = df["totals"].struct.field("pageviews").fillna(0)
features = bpd.DataFrame(
    {
        "os": operating_system,
        "is_mobile": is_mobile,
        "country": country,
        "pageviews": pageviews,
    }
)
# Use Logistic Regression predict method to predict results
# using your model.
# Find more information here in
# [BigFrames](https://cloud.google.com/python/docs/reference/bigframes/latest/bigframes.ml.linear_model.LogisticRegression#bigframes_ml_linear_model_LogisticRegression_predict)

predictions = model.predict(features)

# Call groupby method to group predicted_label by country.
# Call sum method to get the total_predicted_label by country.
total_predicted_purchases = predictions.groupby(["country"])[
    ["predicted_label"]
].sum()

# Call the sort_values method with the parameter
# ascending = False to get the highest values.
# Call head method to limit to the 10 highest values.
total_predicted_purchases.sort_values(ascending=False).head(10)

# country
# United States    220
# Taiwan             8
# Canada             7
# India              2
# Japan              2
# Turkey             2
# Australia          1
# Brazil             1
# Germany            1
# Guyana             1
# Name: predicted_label, dtype: Int64
```

## 預測各使用者的購買量

預測每位網站訪客的交易次數。

### SQL

這項查詢與前一節的查詢相同，只有 `GROUP BY` 子句不同。這裡的 `GROUP BY` 子句 `GROUP BY fullVisitorId`
是用來依訪客 ID 分組結果。

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中執行下列陳述式：

   ```
   SELECT
   fullVisitorId,
   SUM(predicted_label) as total_predicted_purchases
   FROM
   ML.PREDICT(MODEL `bqml_tutorial.sample_model`, (
   SELECT
   IFNULL(device.operatingSystem, "") AS os,
   device.isMobile AS is_mobile,
   IFNULL(totals.pageviews, 0) AS pageviews,
   IFNULL(geoNetwork.country, "") AS country,
   fullVisitorId
   FROM
   `bigquery-public-data.google_analytics_sample.ga_sessions_*`
   WHERE
   _TABLE_SUFFIX BETWEEN '20170701' AND '20170801'))
   GROUP BY fullVisitorId
   ORDER BY total_predicted_purchases DESC
   LIMIT 10
   ```

   結果應如下所示：

   ```
     +---------------------+---------------------------+
     |    fullVisitorId    | total_predicted_purchases |
     +---------------------+---------------------------+
     | 9417857471295131045 |                         4 |
     | 112288330928895942  |                         2 |
     | 2158257269735455737 |                         2 |
     | 489038402765684003  |                         2 |
     | 057693500927581077  |                         2 |
     | 2969418676126258798 |                         2 |
     | 5073919761051630191 |                         2 |
     | 7420300501523012460 |                         2 |
     | 0456807427403774085 |                         2 |
     | 2105122376016897629 |                         2 |
     +---------------------+---------------------------+
   ```

### BigQuery DataFrames

在嘗試這個範例之前，請按照[使用 BigQuery DataFrames 的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/dataframes-quickstart?hl=zh-tw)中的 BigQuery DataFrames 設定說明操作。
詳情請參閱 [BigQuery DataFrames 參考文件](https://docs.cloud.google.com/python/docs/reference/bigframes/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。
詳情請參閱「[為本機開發環境設定 ADC](https://docs.cloud.google.com/docs/authentication/set-up-adc-local-dev-environment?hl=zh-tw)」。

```
import bigframes.pandas as bpd

# Select model you'll use for predicting.
# `read_gbq_model` loads model data from
# BigQuery, but you could also use the `model`
# object from the previous steps.
model = bpd.read_gbq_model(
    your_model_id,  # For example: "bqml_tutorial.sample_model",
)

# The filters parameter limits the number of tables scanned by the query.
# The date range scanned is July 1, 2017 to August 1, 2017. This is the
# data you're using to make the prediction.
# It was collected in the month immediately following the time period
# spanned by the training data.
df = bpd.read_gbq_table(
    "bigquery-public-data.google_analytics_sample.ga_sessions_*",
    filters=[
        ("_table_suffix", ">=", "20170701"),
        ("_table_suffix", "<=", "20170801"),
    ],
)

operating_system = df["device"].struct.field("operatingSystem")
operating_system = operating_system.fillna("")
is_mobile = df["device"].struct.field("isMobile")
country = df["geoNetwork"].struct.field("country").fillna("")
pageviews = df["totals"].struct.field("pageviews").fillna(0)
full_visitor_id = df["fullVisitorId"]

features = bpd.DataFrame(
    {
        "os": operating_system,
        "is_mobile": is_mobile,
        "country": country,
        "pageviews": pageviews,
        "fullVisitorId": full_visitor_id,
    }
)

predictions = model.predict(features)

# Call groupby method to group predicted_label by visitor.
# Call sum method to get the total_predicted_label by visitor.
total_predicted_purchases = predictions.groupby(["fullVisitorId"])[
    ["predicted_label"]
].sum()

# Call the sort_values method with the parameter
# ascending = False to get the highest values.
# Call head method to limit to the 10 highest values.
total_predicted_purchases.sort_values(ascending=False).head(10)

# fullVisitorId
# 9417857471295131045    4
# 0376394056092189113    2
# 0456807427403774085    2
# 057693500927581077     2
# 112288330928895942     2
# 1280993661204347450    2
# 2105122376016897629    2
# 2158257269735455737    2
# 2969418676126258798    2
# 489038402765684003     2
# Name: predicted_label, dtype: Int64
```

## 清除所用資源

為了避免系統向您的 Google Cloud 帳戶收取本頁面所用資源的費用，請按照下列步驟操作。

您可以刪除建立的專案，或保留專案並刪除資料集。

### 刪除資料集

刪除專案將移除專案中所有的資料集與資料表。若您希望重新使用專案，您可以刪除本教學課程中所建立的資料集。

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中展開專案，按一下「Datasets」(資料集)，然後點選您建立的 `bqml_tutorial` 資料集。
4. 點選「刪除」。
5. 在「Delete dataset」(刪除資料集) 對話方塊中，輸入 `delete` 來確認刪除指令。
6. 點選「刪除」。

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

* 如要進一步瞭解機器學習，請參閱[機器學習速成課程](https://developers.google.com/machine-learning/crash-course/?hl=zh-tw)。
* 如需 BigQuery ML 的總覽，請參閱 [BigQuery ML 簡介](https://docs.cloud.google.com/bigquery/docs/bqml-introduction?hl=zh-tw)。
* 如要進一步瞭解 Google Cloud 控制台，請參閱「[使用 Google Cloud 控制台](https://docs.cloud.google.com/bigquery/bigquery-web-ui?hl=zh-tw)」。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-16 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-16 (世界標準時間)。"],[],[]]