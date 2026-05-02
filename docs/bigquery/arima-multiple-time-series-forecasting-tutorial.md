* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見

# 使用 ARIMA\_PLUS 單變數模型預測多個時間序列 透過集合功能整理內容 你可以依據偏好儲存及分類內容。

本教學課程說明如何使用[`ARIMA_PLUS`單變數時間序列模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-time-series?hl=zh-tw)，根據特定資料欄的歷史值，預測該資料欄的未來值。

本教學課程會預測多個時間序列。系統會針對一或多個指定資料欄中的每個值，計算每個時間點的預測值。舉例來說，如果您想預測天氣，並指定包含城市資料的資料欄，預測資料會包含 A 城市所有時間點的預測值，接著是 B 城市所有時間點的預測值，依此類推。

[本教學課程使用公開資料表中的資料。](https://console.cloud.google.com/bigquery?p=bigquery-public-data&%3Bd=new_york&%3Bt=citibike_trips&%3Bpage=table&hl=zh-tw)`bigquery-public-data.new_york.citibike_trips`這個資料表包含紐約市 Citi Bike 行程的相關資訊。

建議您先閱讀「[使用單變數模型預測單一時間序列](https://docs.cloud.google.com/bigquery/docs/arima-single-time-series-forecasting-tutorial?hl=zh-tw)」，再閱讀本教學課程。

## 目標

本教學課程會逐步引導您完成下列工作：

* 使用 [`CREATE MODEL` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-time-series?hl=zh-tw)建立時間序列模型，預測自行車行程數量。
* 使用 [`ML.ARIMA_EVALUATE` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-arima-evaluate?hl=zh-tw)評估模型中的自迴歸整合移動平均 (ARIMA) 資訊。
* 使用 [`ML.ARIMA_COEFFICIENTS` 函式檢查模型係數](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-arima-coefficients?hl=zh-tw)。
* 使用 [`ML.FORECAST` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-forecast?hl=zh-tw)從模型擷取預測的自行車騎乘資訊。
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

建立模型前，您可以選擇將輸入的時間序列資料視覺化，瞭解資料分布情形。您可以使用數據分析達成這個目標。

### SQL

下列查詢的 `SELECT` 陳述式使用 [`EXTRACT` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/timestamp_functions?hl=zh-tw#extract)從 `starttime` 資料欄中擷取日期資訊。這項查詢會使用 `COUNT(*)` 子句，取得每日的 Citi Bike 行程總數。

請按照下列步驟，以視覺化方式呈現時間序列資料：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中貼入下列查詢，然後點選「執行」：

   ```
   SELECT
    EXTRACT(DATE from starttime) AS date,
    COUNT(*) AS num_trips
   FROM
   `bigquery-public-data.new_york.citibike_trips`
   GROUP BY date;
   ```
3. 查詢完成後，依序點選「開啟方式」>「數據分析」。系統會在新的分頁中開啟數據分析。在新分頁中完成下列步驟。
4. 在數據分析中，依序點選「插入」>「時間序列圖」。
5. 在「圖表」窗格中，選擇「設定」分頁。
6. 在「指標」專區中新增「num\_trips」欄位，並移除預設的「記錄計數」指標。產生的圖表如下所示：

### BigQuery DataFrames

在嘗試這個範例之前，請按照[使用 BigQuery DataFrames 的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/dataframes-quickstart?hl=zh-tw)中的 BigQuery DataFrames 設定說明操作。
詳情請參閱 [BigQuery DataFrames 參考文件](https://docs.cloud.google.com/python/docs/reference/bigframes/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。
詳情請參閱「[為本機開發環境設定 ADC](https://docs.cloud.google.com/docs/authentication/set-up-adc-local-dev-environment?hl=zh-tw)」。

```
import bigframes.pandas as bpd

df = bpd.read_gbq("bigquery-public-data.new_york.citibike_trips")

features = bpd.DataFrame(
    {
        "num_trips": df.starttime,
        "date": df["starttime"].dt.date,
    }
)
date = df["starttime"].dt.date
df.groupby([date])
num_trips = features.groupby(["date"]).count()

# Results from running "print(num_trips)"

#                num_trips
# date
# 2013-07-01      16650
# 2013-07-02      22745
# 2013-07-03      21864
# 2013-07-04      22326
# 2013-07-05      21842
# 2013-07-06      20467
# 2013-07-07      20477
# 2013-07-08      21615
# 2013-07-09      26641
# 2013-07-10      25732
# 2013-07-11      24417
# 2013-07-12      19006
# 2013-07-13      26119
# 2013-07-14      29287
# 2013-07-15      28069
# 2013-07-16      29842
# 2013-07-17      30550
# 2013-07-18      28869
# 2013-07-19      26591
# 2013-07-20      25278
# 2013-07-21      30297
# 2013-07-22      25979
# 2013-07-23      32376
# 2013-07-24      35271
# 2013-07-25      31084

num_trips.plot.line(
    # Rotate the x labels so they are more visible.
    rot=45,
)
```

## 建立時間序列模型

您想預測每個 Citi Bike 車站的單車行程數量，這需要許多時間序列模型，也就是輸入資料中每個 Citi Bike 車站各需要一個模型。您可以建立多個模型來完成這項作業，但這可能相當繁瑣且耗時，尤其是當您有大量時間序列時。您可以改用單一查詢建立及調整一組時間序列模型，一次預測多個時間序列。

### SQL

在下列查詢中，`OPTIONS(model_type='ARIMA_PLUS', time_series_timestamp_col='date', ...)` 子句表示您要建立以 [ARIMA](https://en.wikipedia.org/wiki/Autoregressive_integrated_moving_average) 為基礎的時間序列模型。您可以使用 `CREATE MODEL` 陳述式的 [`time_series_id_col` 選項，指定要取得預測結果的輸入資料欄 (在本例中為 Citi Bike 車站，以 `start_station_name` 資料欄表示)。](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-time-series?hl=zh-tw#time_series_id_col)您可以使用 `WHERE` 子句，將起點站限制為名稱中含有 `Central Park` 的車站。`CREATE MODEL` 陳述式的 [`auto_arima_max_order` 選項](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-time-series?hl=zh-tw#auto_arima_max_order)會控管 `auto.ARIMA` 演算法中超參數調整的搜尋空間。`CREATE MODEL` 陳述式的 [`decompose_time_series` 選項](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-time-series?hl=zh-tw#decompose_time_series)預設為 `TRUE`，因此在下一個步驟中評估模型時，系統會傳回時間序列資料的相關資訊。

請按照下列步驟建立模型：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中貼入下列查詢，然後點選「執行」：

   ```
   CREATE OR REPLACE MODEL `bqml_tutorial.nyc_citibike_arima_model_group`
   OPTIONS
   (model_type = 'ARIMA_PLUS',
    time_series_timestamp_col = 'date',
    time_series_data_col = 'num_trips',
    time_series_id_col = 'start_station_name',
    auto_arima_max_order = 5
   ) AS
   SELECT
    start_station_name,
    EXTRACT(DATE from starttime) AS date,
    COUNT(*) AS num_trips
   FROM
   `bigquery-public-data.new_york.citibike_trips`
   WHERE start_station_name LIKE '%Central Park%'
   GROUP BY start_station_name, date;
   ```

   查詢作業約需 24 秒才能完成，完成後您就能存取 `nyc_citibike_arima_model_group` 模型。由於查詢使用 `CREATE MODEL` 陳述式，因此您不會看到查詢結果。

這項查詢會建立十二個時間序列模型，輸入資料中十二個 Citi Bike 起始車站各有一個模型。由於平行處理，時間成本約為 24 秒，只比建立單一時間序列模型多 1.4 倍。不過，如果您移除 `WHERE ... LIKE ...` 子句，則會有 600 多個時間序列需要預測，而且由於運算單元容量限制，這些時間序列不會完全平行預測。在這種情況下，查詢大約需要 15 分鐘才能完成。如要縮短查詢執行時間，但可能稍微降低模型品質，可以減少 `auto_arima_max_order` 的值。這會縮小演算法中超參數調整的搜尋空間。`auto.ARIMA`詳情請參閱「[`Large-scale time series forecasting best practices`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-time-series?hl=zh-tw#large-scale-time-series-forecasting-best-practices)」。

### BigQuery DataFrames

在下列程式碼片段中，您要建立以 [ARIMA](https://en.wikipedia.org/wiki/Autoregressive_integrated_moving_average) 為基礎的時間序列模型。

在嘗試這個範例之前，請按照[使用 BigQuery DataFrames 的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/dataframes-quickstart?hl=zh-tw)中的 BigQuery DataFrames 設定說明操作。
詳情請參閱 [BigQuery DataFrames 參考文件](https://docs.cloud.google.com/python/docs/reference/bigframes/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。
詳情請參閱「[為本機開發環境設定 ADC](https://docs.cloud.google.com/docs/authentication/set-up-adc-local-dev-environment?hl=zh-tw)」。

```
from bigframes.ml import forecasting
import bigframes.pandas as bpd

model = forecasting.ARIMAPlus(
    # To reduce the query runtime with the compromise of a potential slight
    # drop in model quality, you could decrease the value of the
    # auto_arima_max_order. This shrinks the search space of hyperparameter
    # tuning in the auto.ARIMA algorithm.
    auto_arima_max_order=5,
)

df = bpd.read_gbq("bigquery-public-data.new_york.citibike_trips")

# This query creates twelve time series models, one for each of the twelve
# Citi Bike start stations in the input data. If you remove this row
# filter, there would be 600+ time series to forecast.
df = df[df["start_station_name"].str.contains("Central Park")]

features = bpd.DataFrame(
    {
        "start_station_name": df["start_station_name"],
        "num_trips": df["starttime"],
        "date": df["starttime"].dt.date,
    }
)
num_trips = features.groupby(
    ["start_station_name", "date"],
    as_index=False,
).count()

X = num_trips["date"].to_frame()
y = num_trips["num_trips"].to_frame()

model.fit(
    X,
    y,
    # The input data that you want to get forecasts for,
    # in this case the Citi Bike station, as represented by the
    # start_station_name column.
    id_col=num_trips["start_station_name"].to_frame(),
)

# The model.fit() call above created a temporary model.
# Use the to_gbq() method to write to a permanent location.
model.to_gbq(
    your_model_id,  # For example: "bqml_tutorial.nyc_citibike_arima_model",
    replace=True,
)
```

這會建立十二個時間序列模型，輸入資料中的十二個 Citi Bike 起始站點各有一個模型。由於平行處理，建立單一時間序列模型的時間成本約為 24 秒，僅增加 1.4 倍。

## 評估模型

### SQL

使用 `ML.ARIMA_EVALUATE` 函式評估時間序列模型。`ML.ARIMA_EVALUATE` 函式會顯示在自動超參數調整程序中，為模型產生的評估指標。

請按照下列步驟評估模型：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中貼入下列查詢，然後點選「執行」：

   ```
   SELECT
   *
   FROM
   ML.ARIMA_EVALUATE(MODEL `bqml_tutorial.nyc_citibike_arima_model_group`);
   ```

   結果應如下所示：

   `auto.ARIMA` 會評估每個時間序列的數十個候選 ARIMA 模型，但根據預設，`ML.ARIMA_EVALUATE` 只會輸出最佳模型的資訊，讓輸出表格更精簡。如要查看所有候選模型，您可以將 `ML.ARIMA_EVALUATE` 函式的 [`show_all_candidate_model` 引數](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-arima-evaluate?hl=zh-tw#arguments)設為 `TRUE`。

### BigQuery DataFrames

在嘗試這個範例之前，請按照[使用 BigQuery DataFrames 的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/dataframes-quickstart?hl=zh-tw)中的 BigQuery DataFrames 設定說明操作。
詳情請參閱 [BigQuery DataFrames 參考文件](https://docs.cloud.google.com/python/docs/reference/bigframes/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。
詳情請參閱「[為本機開發環境設定 ADC](https://docs.cloud.google.com/docs/authentication/set-up-adc-local-dev-environment?hl=zh-tw)」。

```
# Evaluate the time series models by using the summary() function. The summary()
# function shows you the evaluation metrics of all the candidate models evaluated
# during the process of automatic hyperparameter tuning.
summary = model.summary()
print(summary.peek())

# Expected output:
#    start_station_name                  non_seasonal_p  non_seasonal_d   non_seasonal_q  has_drift  log_likelihood           AIC     variance ...
# 1         Central Park West & W 72 St               0               1                5      False    -1966.449243   3944.898487  1215.689281 ...
# 8            Central Park W & W 96 St               0               0                5      False     -274.459923    562.919847   655.776577 ...
# 9        Central Park West & W 102 St               0               0                0      False     -226.639918    457.279835    258.83582 ...
# 11        Central Park West & W 76 St               1               1                2      False    -1700.456924   3408.913848   383.254161 ...
# 4   Grand Army Plaza & Central Park S               0               1                5      False    -5507.553498  11027.106996   624.138741 ...
```

「`start_station_name`」欄會指出建立時間序列的輸入資料欄。這是您在建立模型時，使用 `time_series_id_col` 選項指定的資料欄。

`non_seasonal_p`、`non_seasonal_d`、`non_seasonal_q` 和 `has_drift` 輸出資料欄會在訓練管道中定義 ARIMA 模型。`log_likelihood`、`AIC` 和 `variance` 輸出資料欄與 ARIMA 模型擬合程序相關。在每個時間序列中，配適程序會使用 `auto.ARIMA` 演算法，找出最合適的 ARIMA 模型。

`auto.ARIMA`演算法會使用 [KPSS 測試](https://en.wikipedia.org/wiki/KPSS_test)，判斷 `non_seasonal_d` 的最佳值，在本例中為 `1`。當 `non_seasonal_d` 為 `1` 時，auto.ARIMA 演算法會平行訓練 42 個不同的候選 ARIMA 模型。在本例中，所有 42 個候選模型都有效，因此輸出內容包含 42 個資料列，每個候選 ARIMA 模型各佔一列；如果部分模型無效，則會從輸出內容中排除。這些候選模型會依 AIC 升序傳回。第一列中的模型 AIC 最低，因此視為最佳模型。這個最佳模型會儲存為最終模型，並用於預測資料、評估模型，以及檢查模型的係數，如下列步驟所示。

`seasonal_periods` 欄包含時間序列資料中識別出的季節性模式相關資訊。每個時間序列可能都有不同的季節性模式。舉例來說，從圖中可以看出，其中一個時間序列具有年度模式，其他則沒有。

只有在 `decompose_time_series=TRUE` 時，系統才會填入 `has_holiday_effect`、`has_spikes_and_dips` 和 `has_step_changes` 欄。這些資料欄也會反映輸入時間序列資料的相關資訊，與 ARIMA 模型無關。所有輸出資料列的這些資料欄值也相同。

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
   ML.ARIMA_COEFFICIENTS(MODEL `bqml_tutorial.nyc_citibike_arima_model_group`);
   ```

   查詢會在不到一秒的時間內完成。結果應如下所示：

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
#    start_station_name                                              ar_coefficients                                   ma_coefficients intercept_or_drift
# 5    Central Park West & W 68 St                                                [] [-0.41014089  0.21979212 -0.59854213 -0.251438...                0.0
# 6         Central Park S & 6 Ave                                                [] [-0.71488957 -0.36835772  0.61008532  0.183290...                0.0
# 0    Central Park West & W 85 St                                                [] [-0.39270166 -0.74494638  0.76432596  0.489146...                0.0
# 3    W 82 St & Central Park West                         [-0.50219511 -0.64820817]             [-0.20665325  0.67683137 -0.68108631]                0.0
# 11  W 106 St & Central Park West [-0.70442887 -0.66885553 -0.25030325 -0.34160669]                                                []                0.0
```

「`start_station_name`」欄會指出建立時間序列的輸入資料欄。這是您在建立模型時，於 `time_series_id_col` 選項中指定的資料欄。

`ar_coefficients` 輸出資料欄會顯示 ARIMA 模型自迴歸 (AR) 部分的模型係數。同樣地，`ma_coefficients` 輸出資料欄會顯示 ARIMA 模型移動平均 (MA) 部分的模型係數。這兩個資料欄都包含陣列值，長度分別等於 `non_seasonal_p` 和 `non_seasonal_q`。`intercept_or_drift` 值是 ARIMA 模型中的常數項。

## 使用模型預測資料

### SQL

使用 `ML.FORECAST` 函式預測未來時間序列值。

在下列 GoogleSQL 查詢中，`STRUCT(3 AS horizon, 0.9 AS confidence_level)` 子句表示查詢會預測 3 個未來時間點，並產生信賴水準為 90% 的預測間隔。

如要使用模型預測資料，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中貼入下列查詢，然後點選「執行」：

   ```
   SELECT
   *
   FROM
   ML.FORECAST(MODEL `bqml_tutorial.nyc_citibike_arima_model_group`,
    STRUCT(3 AS horizon, 0.9 AS confidence_level))
   ```
3. 按一下「執行」。

   查詢會在不到一秒的時間內完成。結果應如下所示：

如要進一步瞭解輸出資料欄，請參閱 [`ML.FORECAST` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-forecast?hl=zh-tw)。

### BigQuery DataFrames

使用 `predict` 函式預測未來時間序列值。

在嘗試這個範例之前，請按照[使用 BigQuery DataFrames 的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/dataframes-quickstart?hl=zh-tw)中的 BigQuery DataFrames 設定說明操作。
詳情請參閱 [BigQuery DataFrames 參考文件](https://docs.cloud.google.com/python/docs/reference/bigframes/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。
詳情請參閱「[為本機開發環境設定 ADC](https://docs.cloud.google.com/docs/authentication/set-up-adc-local-dev-environment?hl=zh-tw)」。

```
prediction = model.predict(horizon=3, confidence_level=0.9)

print(prediction.peek())
# Expected output:
#            forecast_timestamp                             start_station_name  forecast_value  standard_error  confidence_level ...
# 4   2016-10-01 00:00:00+00:00                         Central Park S & 6 Ave      302.377201       32.572948               0.9 ...
# 14  2016-10-02 00:00:00+00:00  Central Park North & Adam Clayton Powell Blvd      263.917567       45.284082               0.9 ...
# 1   2016-09-25 00:00:00+00:00                    Central Park West & W 85 St      189.574706       39.874856               0.9 ...
# 20  2016-10-02 00:00:00+00:00                    Central Park West & W 72 St      175.474862       40.940794               0.9 ...
# 12  2016-10-01 00:00:00+00:00                   W 106 St & Central Park West        63.88163       18.088868               0.9 ...
```

第一欄 `start_station_name` 會註解每個時間序列模型所要比對的時間序列。每個 `start_station_name` 都有三列預測結果，如 `horizon` 值所指定。

每個 `start_station_name` 的輸出資料列會依 `forecast_timestamp` 資料欄值依時間順序排列。在時間序列預測中，預測間隔 (以 `prediction_interval_lower_bound` 和 `prediction_interval_upper_bound` 欄值表示) 與 `forecast_value` 欄值同樣重要。`forecast_value` 值是預測間隔的中間點。預測區間取決於 `standard_error` 和 `confidence_level` 資料欄值。

## 說明預測結果

### SQL

您可以使用 `ML.EXPLAIN_FORECAST` 函式，除了取得預測資料，還能取得可解釋性指標。`ML.EXPLAIN_FORECAST` 函式會預測未來時間序列值，並傳回時間序列的所有個別元件。如果只想傳回預測資料，請改用 `ML.FORECAST` 函式，如「[使用模型預測資料](https://docs.cloud.google.com/bigquery/docs/arima-multiple-time-series-forecasting-tutorial?hl=zh-tw#use_the_model_to_forecast_data)」一文所示。

`ML.EXPLAIN_FORECAST` 函式中使用的 `STRUCT(3 AS horizon, 0.9 AS confidence_level)` 子句表示查詢會預測未來 3 個時間點，並產生信賴度為 90% 的預測間隔。

請按照下列步驟說明模型的結果：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中貼入下列查詢，然後點選「執行」：

   ```
   SELECT
   *
   FROM
   ML.EXPLAIN_FORECAST(MODEL `bqml_tutorial.nyc_citibike_arima_model_group`,
    STRUCT(3 AS horizon, 0.9 AS confidence_level));
   ```

   查詢會在不到一秒的時間內完成。結果應如下所示：

   傳回的前一千列都是歷史資料。您必須捲動瀏覽結果，才能查看預測資料。

   輸出資料列會先依 `start_station_name` 排序，再依 `time_series_timestamp` 資料欄值依時間順序排序。在時間序列預測中，預測間隔 (以 `prediction_interval_lower_bound` 和 `prediction_interval_upper_bound` 欄值表示) 與 `forecast_value` 欄值同樣重要。`forecast_value` 值是預測間隔的中間點。預測區間取決於 `standard_error` 和 `confidence_level` 資料欄值。

   如要進一步瞭解輸出資料欄，請參閱[`ML.EXPLAIN_FORECAST`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-explain-forecast?hl=zh-tw)。

### BigQuery DataFrames

您可以使用 `predict_explain` 函式，除了取得預測資料，還能取得可解釋性指標。`predict_explain` 函式會預測未來時間序列值，並傳回時間序列的所有個別元件。如果只想傳回預測資料，請改用 `predict` 函式，如「[使用模型預測資料](https://docs.cloud.google.com/bigquery/docs/arima-multiple-time-series-forecasting-tutorial?hl=zh-tw#use_the_model_to_forecast_data)」一文所示。

`predict_explain` 函式中使用的 `horizon=3, confidence_level=0.9` 子句表示查詢會預測未來 3 個時間點，並產生信賴度為 90% 的預測間隔。

在嘗試這個範例之前，請按照[使用 BigQuery DataFrames 的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/dataframes-quickstart?hl=zh-tw)中的 BigQuery DataFrames 設定說明操作。
詳情請參閱 [BigQuery DataFrames 參考文件](https://docs.cloud.google.com/python/docs/reference/bigframes/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。
詳情請參閱「[為本機開發環境設定 ADC](https://docs.cloud.google.com/docs/authentication/set-up-adc-local-dev-environment?hl=zh-tw)」。

```
explain = model.predict_explain(horizon=3, confidence_level=0.9)

print(explain.peek(5))
# Expected output:
#   time_series_timestamp	        start_station_name	            time_series_type	    time_series_data	    time_series_adjusted_data	    standard_error	    confidence_level	    prediction_interval_lower_bound	    prediction_interval_upper_bound	    trend	    seasonal_period_yearly	    seasonal_period_quarterly	    seasonal_period_monthly	    seasonal_period_weekly	    seasonal_period_daily	    holiday_effect	    spikes_and_dips	    step_changes	    residual
# 0	2013-07-01 00:00:00+00:00	Central Park S & 6 Ave	                history	                  69.0	                   154.168527	              32.572948	             <NA>	                        <NA>	                            <NA>	                 0.0	          35.477484	                       <NA>	                        <NA>	                  -28.402102	                 <NA>	                <NA>	               0.0	         -85.168527	        147.093145
# 1	2013-07-01 00:00:00+00:00	Grand Army Plaza & Central Park S	    history	                  79.0	                      79.0	                  24.982769	             <NA>	                        <NA>	                            <NA>	                 0.0	          43.46428	                       <NA>	                        <NA>	                  -30.01599	                     <NA>	                <NA>	               0.0	            0.0	             65.55171
# 2	2013-07-02 00:00:00+00:00	Central Park S & 6 Ave	                history	                  180.0	                   204.045651	              32.572948	             <NA>	                        <NA>	                            <NA>	              147.093045	      72.498327	                       <NA>	                        <NA>	                  -15.545721	                 <NA>	                <NA>	               0.0	         -85.168527	         61.122876
# 3	2013-07-02 00:00:00+00:00	Grand Army Plaza & Central Park S	    history	                  129.0	                    99.556269	              24.982769	             <NA>	                        <NA>	                            <NA>	               65.551665	      45.836432	                       <NA>	                        <NA>	                  -11.831828	                 <NA>	                <NA>	               0.0	            0.0	             29.443731
# 4	2013-07-03 00:00:00+00:00	Central Park S & 6 Ave	                history	                  115.0	                   205.968236	              32.572948	             <NA>	                        <NA>	                            <NA>	               191.32754	      59.220766	                       <NA>	                        <NA>	                  -44.580071	                 <NA>	                <NA>	               0.0	         -85.168527	        -5.799709
```

輸出資料列會先依 `time_series_timestamp` 排序，再依 `start_station_name` 資料欄值依時間順序排序。在時間序列預測中，預測間隔 (以 `prediction_interval_lower_bound` 和 `prediction_interval_upper_bound` 欄值表示) 與 `forecast_value` 欄值同樣重要。`forecast_value` 值是預測間隔的中間點。預測區間取決於 `standard_error` 和 `confidence_level` 資料欄值。

## 清除所用資源

為避免因為本教學課程所用資源，導致系統向 Google Cloud 帳戶收取費用，請刪除含有相關資源的專案，或者保留專案但刪除個別資源。

* 您可以刪除建立的專案。
* 或者您可以保留專案並刪除資料集。

### 刪除資料集

刪除專案將移除專案中所有的資料集與資料表。若您希望重新使用專案，您可以刪除本教學課程中所建立的資料集。

1. 如有必要，請在Google Cloud 控制台中開啟 BigQuery 頁面。

   [前往 BigQuery 頁面](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在導覽窗格中，按一下您建立的 **bqml\_tutorial** 資料集。
3. 按一下「刪除資料集」，即可刪除資料集、資料表和所有資料。
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

* 瞭解如何[使用單變數模型預測單一時間序列](https://docs.cloud.google.com/bigquery/docs/arima-single-time-series-forecasting-tutorial?hl=zh-tw)
* 瞭解如何[使用多變數模型預測單一時間序列](https://docs.cloud.google.com/bigquery/docs/arima-plus-xreg-single-time-series-forecasting-tutorial?hl=zh-tw)
* 瞭解如何[在預測多個資料列的時間序列時，擴充單變數模型](https://docs.cloud.google.com/bigquery/docs/arima-speed-up-tutorial?hl=zh-tw)。
* 瞭解如何[使用單變數模型，以階層方式預測多個時間序列](https://docs.cloud.google.com/bigquery/docs/arima-time-series-forecasting-with-hierarchical-time-series?hl=zh-tw)
* 如需 BigQuery ML 的總覽，請參閱 [BigQuery 中的 AI 和 ML 簡介](https://docs.cloud.google.com/bigquery/docs/bqml-introduction?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-02 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-02 (世界標準時間)。"],[],[]]