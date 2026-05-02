* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見

# 使用 ARIMA\_PLUS 單變數模型預測單一時間序列 透過集合功能整理內容 你可以依據偏好儲存及分類內容。

本教學課程將說明如何使用[`ARIMA_PLUS`單變數時間序列模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-time-series?hl=zh-tw)，根據特定資料欄的歷來值，預測該資料欄的未來值。

本教學課程會預測單一時間序列。系統會針對輸入資料中的每個時間點計算一次預測值。

本教學課程使用公開的[`bigquery-public-data.google_analytics_sample.ga_sessions`範例資料表](https://console.cloud.google.com/bigquery?p=bigquery-public-data&%3Bd=google_analytics_sample&%3Bt=ga_sessions_20170801&%3Bpage=table&hl=zh-tw)資料。這份表格包含 Google 商品網路商店的模糊處理電子商務資料。

## 目標

本教學課程會逐步引導您完成下列工作：

* 使用 [`CREATE MODEL` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-time-series?hl=zh-tw)建立時間序列模型，預測網站流量。
* 使用 [`ML.ARIMA_EVALUATE` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-arima-evaluate?hl=zh-tw)評估模型中的自迴歸整合移動平均 (ARIMA) 資訊。
* 使用 [`ML.ARIMA_COEFFICIENTS` 函式檢查模型係數](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-arima-coefficients?hl=zh-tw)。
* 使用 [`ML.FORECAST` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-forecast?hl=zh-tw)從模型中擷取預測的網站流量資訊。
* 使用 [`ML.EXPLAIN_FORECAST` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-explain-forecast?hl=zh-tw)擷取時間序列的元件，例如季節性和趨勢。您可以檢查這些時間序列元件，藉此說明預測值。

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

如要進一步瞭解 BigQuery 中的 IAM 角色和權限，請參閱「[IAM 簡介](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)」。

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

## 以視覺化方式呈現輸入資料

建立模型前，您可以選擇將輸入的時間序列資料視覺化，瞭解資料分布情形。您可以使用數據分析達成此目的。

請按照下列步驟，以視覺化方式呈現時間序列資料：

### SQL

在下列 GoogleSQL 查詢中，`SELECT` 陳述式會將輸入資料表中的 `date` 欄剖析為 `TIMESTAMP` 型別，並重新命名為 `parsed_date`，然後使用 `SUM(...)` 子句和 `GROUP BY date` 子句建立每日 `totals.visits` 值。

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中貼入下列查詢，然後點選「執行」：

   ```
   SELECT
   PARSE_TIMESTAMP("%Y%m%d", date) AS parsed_date,
   SUM(totals.visits) AS total_visits
   FROM
   `bigquery-public-data.google_analytics_sample.ga_sessions_*`
   GROUP BY date;
   ```

   1. 查詢完成後，依序點選「開啟方式」>「數據分析」。系統會在新的分頁中開啟數據分析。在新分頁中完成下列步驟。
   2. 在數據分析中，依序點選「插入」>「時間序列圖」。
   3. 在「圖表」窗格中，選擇「設定」分頁。
   4. 在「指標」專區中新增「total\_visits」欄位，並移除預設的「記錄計數」指標。產生的圖表如下所示：

      從圖表可以看出，輸入時間序列具有每週季節性模式。

      **注意：** 如要進一步瞭解數據分析支援服務，請參閱[數據分析說明和支援選項](https://docs.cloud.google.com/looker/docs/studio/contact-us?hl=zh-tw)。

### BigQuery DataFrames

在嘗試這個範例之前，請按照[使用 BigQuery DataFrames 的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/dataframes-quickstart?hl=zh-tw)中的 BigQuery DataFrames 設定說明操作。
詳情請參閱 [BigQuery DataFrames 參考文件](https://docs.cloud.google.com/python/docs/reference/bigframes/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。
詳情請參閱「[為本機開發環境設定 ADC](https://docs.cloud.google.com/docs/authentication/set-up-adc-local-dev-environment?hl=zh-tw)」。

```
import bigframes.pandas as bpd

# Start by loading the historical data from BigQuerythat you want to analyze and forecast.
# This clause indicates that you are querying the ga_sessions_* tables in the google_analytics_sample dataset.
# Read and visualize the time series you want to forecast.
df = bpd.read_gbq("bigquery-public-data.google_analytics_sample.ga_sessions_*")
parsed_date = bpd.to_datetime(df.date, format="%Y%m%d", utc=True)
parsed_date.name = "parsed_date"
visits = df["totals"].struct.field("visits")
visits.name = "total_visits"
total_visits = visits.groupby(parsed_date).sum()

# Expected output: total_visits.head()
# parsed_date
# 2016-08-01 00:00:00+00:00    1711
# 2016-08-02 00:00:00+00:00    2140
# 2016-08-03 00:00:00+00:00    2890
# 2016-08-04 00:00:00+00:00    3161
# 2016-08-05 00:00:00+00:00    2702
# Name: total_visits, dtype: Int64

total_visits.plot.line()
```

結果大致如下：

## 建立時間序列模型

建立時間序列模型，預測以 `totals.visits` 欄表示的網站總造訪次數，並使用 Google Analytics 360 資料訓練模型。

### SQL

在下列查詢中，`OPTIONS(model_type='ARIMA_PLUS', time_series_timestamp_col='date', ...)` 子句表示您要建立以 [ARIMA](https://en.wikipedia.org/wiki/Autoregressive_integrated_moving_average) 為基礎的時間序列模型。`CREATE MODEL` 陳述式的 [`auto_arima` 選項](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-multivariate-time-series?hl=zh-tw#auto_arima)預設為 `TRUE`，因此 `auto.ARIMA` 演算法會自動調整模型中的超參數。演算法會套用數十個候選模型，並選擇最佳模型，也就是[赤池訊息量準則 (AIC)](https://en.wikipedia.org/wiki/Akaike_information_criterion) 最低的模型。`CREATE MODEL` 陳述式的[`data_frequency` 選項](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-multivariate-time-series?hl=zh-tw#data_frequency)預設為 `AUTO_FREQUENCY`，因此訓練程序會自動推斷輸入時間序列的資料頻率。`CREATE MODEL` 陳述式的 [`decompose_time_series` 選項](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-time-series?hl=zh-tw#decompose_time_series)預設為 `TRUE`，因此在下一個步驟中評估模型時，系統會傳回時間序列資料的相關資訊。

請按照下列步驟建立模型：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中貼入下列查詢，然後點選「執行」：

   ```
   CREATE OR REPLACE MODEL `bqml_tutorial.ga_arima_model`
   OPTIONS
   (model_type = 'ARIMA_PLUS',
    time_series_timestamp_col = 'parsed_date',
    time_series_data_col = 'total_visits',
    auto_arima = TRUE,
    data_frequency = 'AUTO_FREQUENCY',
    decompose_time_series = TRUE
   ) AS
   SELECT
   PARSE_TIMESTAMP("%Y%m%d", date) AS parsed_date,
   SUM(totals.visits) AS total_visits
   FROM
   `bigquery-public-data.google_analytics_sample.ga_sessions_*`
   GROUP BY date;
   ```

   查詢約需 4 秒即可完成，之後您就能存取 `ga_arima_model` 模型。由於查詢是使用 `CREATE MODEL` 陳述式建立模型，因此您看不到查詢結果。

**注意：** 您可能會想知道美國節慶是否會影響時間序列。您可以嘗試將 `CREATE MODEL` 陳述式的 [`holiday_region` 選項](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-multivariate-time-series?hl=zh-tw#holiday_region)設為 `US`。如果時間序列中有任何節慶模式，設定這個選項可更準確地模擬節慶時間點。

### BigQuery DataFrames

在嘗試這個範例之前，請按照[使用 BigQuery DataFrames 的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/dataframes-quickstart?hl=zh-tw)中的 BigQuery DataFrames 設定說明操作。
詳情請參閱 [BigQuery DataFrames 參考文件](https://docs.cloud.google.com/python/docs/reference/bigframes/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。
詳情請參閱「[為本機開發環境設定 ADC](https://docs.cloud.google.com/docs/authentication/set-up-adc-local-dev-environment?hl=zh-tw)」。

```
from bigframes.ml import forecasting
import bigframes.pandas as bpd

# Create a time series model to forecast total site visits:
# The auto_arima option defaults to True, so the auto.ARIMA algorithm automatically
# tunes the hyperparameters in the model.
# The data_frequency option defaults to 'auto_frequency so the training
# process automatically infers the data frequency of the input time series.
# The decompose_time_series option defaults to True, so that information about
# the time series data is returned when you evaluate the model in the next step.
model = forecasting.ARIMAPlus()
model.auto_arima = True
model.data_frequency = "auto_frequency"
model.decompose_time_series = True

# Use the data loaded in the previous step to fit the model
training_data = total_visits.to_frame().reset_index(drop=False)

X = training_data[["parsed_date"]]
y = training_data[["total_visits"]]

model.fit(X, y)
```

## 評估候選模型

### SQL

使用 `ML.ARIMA_EVALUATE` 函式評估時間序列模型。`ML.ARIMA_EVALUATE` 函式會顯示自動超參數調整程序中評估的所有候選模型評估指標。

請按照下列步驟評估模型：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中貼入下列查詢，然後點選「執行」：

   ```
   SELECT
   *
   FROM
   ML.ARIMA_EVALUATE(MODEL `bqml_tutorial.ga_arima_model`);
   ```

   結果應如下所示：

### BigQuery DataFrames

在嘗試這個範例之前，請按照[使用 BigQuery DataFrames 的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/dataframes-quickstart?hl=zh-tw)中的 BigQuery DataFrames 設定說明操作。
詳情請參閱 [BigQuery DataFrames 參考文件](https://docs.cloud.google.com/python/docs/reference/bigframes/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。
詳情請參閱「[為本機開發環境設定 ADC](https://docs.cloud.google.com/docs/authentication/set-up-adc-local-dev-environment?hl=zh-tw)」。

```
# Evaluate the time series models by using the summary() function. The summary()
# function shows you the evaluation metrics of all the candidate models evaluated
# during the process of automatic hyperparameter tuning.
summary = model.summary(
    show_all_candidate_models=True,
)
print(summary.peek())

# Expected output:
# row   non_seasonal_p	non_seasonal_d	non_seasonal_q	has_drift	log_likelihood	AIC	variance	seasonal_periods	has_holiday_effect	has_spikes_and_dips	has_step_changes	error_message
#  0	      0	              1	               3	      True	     -2464.255656	4938.511313	     42772.506055	        ['WEEKLY']	            False	        False	            True
#  1	      2	              1	               0	      False	     -2473.141651	4952.283303	     44942.416463	        ['WEEKLY']	            False	        False	            True
#  2	      1	              1	               0 	      False	     -2479.880885	4963.76177	     46642.953433	        ['WEEKLY']	            False	        False	            True
#  3	      0	              1	               1	      False	     -2470.632377	4945.264753	     44319.379307	        ['WEEKLY']	            False	        False	            True
#  4	      2	              1	               1	      True	     -2463.671247	4937.342493	     42633.299513	        ['WEEKLY']	            False	        False	            True
```

`non_seasonal_p`、`non_seasonal_d`、`non_seasonal_q` 和 `has_drift` 輸出資料欄會在訓練管道中定義 ARIMA 模型。`log_likelihood`、`AIC` 和 `variance` 輸出資料欄與 ARIMA 模型擬合程序相關。

`auto.ARIMA` 演算法會使用 [KPSS 檢定](https://en.wikipedia.org/wiki/KPSS_test)，判斷 `non_seasonal_d` 的最佳值，在本例中為 `1`。當 `non_seasonal_d` 為 `1` 時，`auto.ARIMA` 演算法會平行訓練 42 個不同的候選 ARIMA 模型。在本例中，所有 42 個候選模型都有效，因此輸出內容包含 42 個資料列，每個候選 ARIMA 模型各佔一行；如果部分模型無效，則會從輸出內容中排除。這些候選模型會依 AIC 升序傳回。第一列中的模型 AIC 最低，因此視為最佳模型。最佳模型會儲存為最終模型，並在您對模型呼叫 `ML.FORECAST` 等函式時使用

`seasonal_periods` 欄包含時間序列資料中識別出的季節性模式相關資訊。這與 ARIMA 建模無關，因此所有輸出資料列的值都相同。這份報表顯示每週模式，與您選擇將輸入資料視覺化時看到的結果一致。

只有在 `decompose_time_series=TRUE` 時，系統才會填入 `has_holiday_effect`、`has_spikes_and_dips` 和 `has_step_changes` 欄。這些資料欄也會反映輸入時間序列資料的相關資訊，與 ARIMA 模型無關。所有輸出資料列的這些資料欄值也相同。

「`error_message`」欄會顯示在`auto.ARIMA`試裝過程中發生的任何錯誤。如果所選的 `non_seasonal_p`、`non_seasonal_d`、`non_seasonal_q` 和 `has_drift` 欄無法穩定時間序列，就可能發生錯誤。如要擷取所有候選模型的錯誤訊息，請在建立模型時，將 `show_all_candidate_models` 選項設為 `TRUE`。

如要進一步瞭解輸出資料欄，請參閱 [`ML.ARIMA_EVALUATE` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-arima-evaluate?hl=zh-tw)。

## 檢查模型的係數

### SQL

使用 `ML.ARIMA_COEFFICIENTS` 函式檢查時間序列模型的係數。

請按照下列步驟擷取模型的係數：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中貼入下列查詢，然後點選「執行」：

   ```
   SELECT
   *
   FROM
   ML.ARIMA_COEFFICIENTS(MODEL `bqml_tutorial.ga_arima_model`);
   ```

`ar_coefficients` 輸出資料欄會顯示 ARIMA 模型自迴歸 (AR) 部分的模型係數。同樣地，`ma_coefficients` 輸出資料欄會顯示 ARIMA 模型移動平均 (MA) 部分的模型係數。這兩個資料欄都包含陣列值，長度分別等於 `non_seasonal_p` 和 `non_seasonal_q`。您在 `ML.ARIMA_EVALUATE` 函式的輸出內容中看到，最佳模型的 `non_seasonal_p` 值為 `2`，`non_seasonal_q` 值為 `3`。因此，在 `ML.ARIMA_COEFFICIENTS` 輸出內容中，`ar_coefficients` 值是 2 元素陣列，而 `ma_coefficients` 值是 3 元素陣列。`intercept_or_drift` 值是 ARIMA 模型中的常數項。

如要進一步瞭解輸出資料欄，請參閱 [`ML.ARIMA_COEFFICIENTS` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-arima-coefficients?hl=zh-tw)。

### BigQuery DataFrames

使用 `coef_` 函式檢查時間序列模型的係數。

在嘗試這個範例之前，請按照[使用 BigQuery DataFrames 的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/dataframes-quickstart?hl=zh-tw)中的 BigQuery DataFrames 設定說明操作。
詳情請參閱 [BigQuery DataFrames 參考文件](https://docs.cloud.google.com/python/docs/reference/bigframes/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。
詳情請參閱「[為本機開發環境設定 ADC](https://docs.cloud.google.com/docs/authentication/set-up-adc-local-dev-environment?hl=zh-tw)」。

```
coef = model.coef_
print(coef.peek())

# Expected output:
#       ar_coefficients   ma_coefficients   intercept_or_drift
#   0	 [0.40944762]	   [-0.81168198]	      0.0
```

`ar_coefficients` 輸出資料欄會顯示 ARIMA 模型自迴歸 (AR) 部分的模型係數。同樣地，`ma_coefficients` 輸出資料欄會顯示 ARIMA 模型移動平均 (MA) 部分的模型係數。這兩個資料欄都包含陣列值，長度分別等於 `non_seasonal_p` 和 `non_seasonal_q`。

## 使用模型預測資料

### SQL

使用 `ML.FORECAST` 函式預測未來時間序列值。

在下列 GoogleSQL 查詢中，`STRUCT(30 AS horizon, 0.8 AS confidence_level)` 子句表示查詢會預測未來 30 個時間點，並產生信賴水準為 80% 的預測間隔。

如要使用模型預測資料，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中貼入下列查詢，然後點選「執行」：

   ```
   SELECT
   *
   FROM
   ML.FORECAST(MODEL `bqml_tutorial.ga_arima_model`,
             STRUCT(30 AS horizon, 0.8 AS confidence_level));
   ```

   結果應如下所示：

### BigQuery DataFrames

使用 `predict` 函式預測未來時間序列值。

在嘗試這個範例之前，請按照[使用 BigQuery DataFrames 的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/dataframes-quickstart?hl=zh-tw)中的 BigQuery DataFrames 設定說明操作。
詳情請參閱 [BigQuery DataFrames 參考文件](https://docs.cloud.google.com/python/docs/reference/bigframes/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。
詳情請參閱「[為本機開發環境設定 ADC](https://docs.cloud.google.com/docs/authentication/set-up-adc-local-dev-environment?hl=zh-tw)」。

```
prediction = model.predict(horizon=30, confidence_level=0.8)

print(prediction.peek())
# Expected output:
#           forecast_timestamp	   forecast_value	standard_error	confidence_level	prediction_interval_lower_bound	    prediction_interval_upper_bound	    confidence_interval_lower_bound	    confidence_interval_upper_bound
# 11	2017-08-13 00:00:00+00:00	1845.439732	      328.060405	      0.8	                 1424.772257	                      2266.107208	                     1424.772257	                     2266.107208
# 29	2017-08-31 00:00:00+00:00	2615.993932	      431.286628	      0.8	                 2062.960849	                      3169.027015	                     2062.960849	                     3169.027015
# 7	    2017-08-09 00:00:00+00:00	2639.285993	      300.301186	      0.8	                 2254.213792	                      3024.358193	                     2254.213792	                     3024.358193
# 25	2017-08-27 00:00:00+00:00	1853.735689	      410.596551	      0.8	                 1327.233216	                      2380.238162	                     1327.233216	                     2380.238162
# 1	    2017-08-03 00:00:00+00:00	2621.33159	      241.093355	      0.8	                 2312.180802	                      2930.482379	                     2312.180802	                     2930.482379
```

輸出資料列會依 `forecast_timestamp` 資料欄值依時間順序排列。在時間序列預測中，預測間隔 (以 `prediction_interval_lower_bound` 和 `prediction_interval_upper_bound` 欄值表示) 與 `forecast_value` 欄值同樣重要。`forecast_value` 值是預測間隔的中間點。預測區間取決於 `standard_error` 和 `confidence_level` 資料欄值。

如要進一步瞭解輸出資料欄，請參閱 [`ML.FORECAST` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-forecast?hl=zh-tw)。

## 說明預測結果

### SQL

您可以使用 `ML.EXPLAIN_FORECAST` 函式，除了取得預測資料，還能取得可解釋性指標。`ML.EXPLAIN_FORECAST` 函式會預測未來時間序列值，並傳回時間序列的所有個別元件。

與 `ML.FORECAST` 函式類似，`ML.EXPLAIN_FORECAST` 函式中使用的 `STRUCT(30 AS horizon, 0.8 AS confidence_level)` 子句表示查詢會預測未來 30 個時間點，並產生信賴度為 80% 的預測區間。

請按照下列步驟說明模型的結果：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中貼入下列查詢，然後點選「執行」：

   ```
   SELECT
   *
   FROM
   ML.EXPLAIN_FORECAST(MODEL `bqml_tutorial.ga_arima_model`,
    STRUCT(30 AS horizon, 0.8 AS confidence_level));
   ```

   結果應如下所示：

   輸出資料列會依 `time_series_timestamp` 資料欄值的時間順序排序。

   如要進一步瞭解輸出資料欄，請參閱 [`ML.EXPLAIN_FORECAST` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-explain-forecast?hl=zh-tw)。

### BigQuery DataFrames

您可以使用 `predict_explain` 函式，除了取得預測資料，還能取得可解釋性指標。`predict_explain` 函式會預測未來時間序列值，並傳回時間序列的所有個別元件。

與 `predict` 函式類似，`predict_explain` 函式中使用的 `horizon=30, confidence_level=0.8` 子句表示查詢會預測未來 30 個時間點，並產生信賴度為 80% 的預測間隔。

在嘗試這個範例之前，請按照[使用 BigQuery DataFrames 的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/dataframes-quickstart?hl=zh-tw)中的 BigQuery DataFrames 設定說明操作。
詳情請參閱 [BigQuery DataFrames 參考文件](https://docs.cloud.google.com/python/docs/reference/bigframes/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。
詳情請參閱「[為本機開發環境設定 ADC](https://docs.cloud.google.com/docs/authentication/set-up-adc-local-dev-environment?hl=zh-tw)」。

```
ex_pred = model.predict_explain(horizon=30, confidence_level=0.8)

print(ex_pred.head(4))
# Expected output:
#       time_series_timestamp	  time_series_type	    time_series_data	time_series_adjusted_data	 standard_error	   confidence_level	   prediction_interval_lower_bound	   prediction_interval_upper_bound	  trend	   seasonal_period_yearly	  seasonal_period_quarterly	    seasonal_period_monthly	   seasonal_period_weekly	  seasonal_period_daily	    holiday_effect	   spikes_and_dips	   step_changes	   residual
# 0	  2016-08-01 00:00:00+00:00	      history	             1711.0	               505.716474	           206.939556	         <NA>	                    <NA>	                            <NA>	               0.0	           <NA>	                        <NA>	                     <NA>	                 169.611938	                  <NA>	                <NA>	            <NA>	       1205.283526	   336.104536
# 1	  2016-08-02 00:00:00+00:00	      history	             2140.0	               623.137701	           206.939556	         <NA>	                    <NA>	                            <NA>	            336.104428	       <NA>	                        <NA>	                     <NA>	                 287.033273	                  <NA>	                <NA>	            <NA>	       1205.283526	   311.578773
# 2	  2016-08-03 00:00:00+00:00	      history	             2890.0	               1008.655091	           206.939556	         <NA>	                    <NA>	                            <NA>	            563.514213	       <NA>	                        <NA>	                     <NA>	                 445.140878	                  <NA>	                <NA>	            <NA>	       1205.283526	   676.061383
# 3	  2016-08-04 00:00:00+00:00	      history	             3161.0	               1389.40959	           206.939556	         <NA>	                    <NA>	                            <NA>	            986.317236	       <NA>	                        <NA>	                     <NA>	                 403.092354	                  <NA>	                <NA>	            <NA>	       1205.283526	   566.306884
# 4	  2016-08-05 00:00:00+00:00	      history	             2702.0	               1394.395741	           206.939556	         <NA>	                    <NA>	                            <NA>	            1248.707386	       <NA>	                        <NA>	                     <NA>	                 145.688355	                  <NA>	                <NA>	            <NA>	       1205.283526	   102.320733
# 5	  2016-08-06 00:00:00+00:00	      history	             1663.0	               437.09243	           206.939556	         <NA>	                    <NA>	                            <NA>	            1188.59004	       <NA>	                        <NA>	                     <NA>	                 -751.49761	                  <NA>	                <NA>	            <NA>	       1205.283526	    20.624044
```

如要以視覺化方式呈現結果，可以使用數據分析，如「[以視覺化方式呈現輸入資料](https://docs.cloud.google.com/bigquery/docs/arima-single-time-series-forecasting-tutorial?hl=zh-tw#visualize_the_input_data)」一節所述，並使用下列資料欄做為指標來建立圖表：

* `time_series_data`
* `prediction_interval_lower_bound`
* `prediction_interval_upper_bound`
* `trend`
* `seasonal_period_weekly`
* `step_changes`

## 清除所用資源

為避免因為本教學課程所用資源，導致系統向 Google Cloud 帳戶收取費用，請刪除含有相關資源的專案，或者保留專案但刪除個別資源。

* 您可以刪除建立的專案。
* 或者您可以保留專案並刪除資料集。

### 刪除資料集

刪除專案將移除專案中所有的資料集與資料表。若您希望重新使用專案，您可以刪除本教學課程中所建立的資料集。

1. 如有必要，請在Google Cloud 控制台中開啟 BigQuery 頁面。

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

* 瞭解如何[使用多變數模型預測單一時間序列](https://docs.cloud.google.com/bigquery/docs/arima-plus-xreg-single-time-series-forecasting-tutorial?hl=zh-tw)
* 瞭解如何[使用單變數模型預測多個時間序列](https://docs.cloud.google.com/bigquery/docs/arima-multiple-time-series-forecasting-tutorial?hl=zh-tw)
* 瞭解如何[在預測多個資料列的時間序列時，擴充單變數模型](https://docs.cloud.google.com/bigquery/docs/arima-speed-up-tutorial?hl=zh-tw)。
* 瞭解如何[使用單變數模型，以階層方式預測多個時間序列](https://docs.cloud.google.com/bigquery/docs/arima-time-series-forecasting-with-hierarchical-time-series?hl=zh-tw)
* 如需 BigQuery ML 的總覽，請參閱 [BigQuery 中的 AI 和 ML 簡介](https://docs.cloud.google.com/bigquery/docs/bqml-introduction?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-02 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-02 (世界標準時間)。"],[],[]]