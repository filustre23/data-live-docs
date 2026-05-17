Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 限制 ARIMA\_PLUS 時間序列模型的預測值

本教學課程說明如何使用限制，縮小 `ARIMA_PLUS` 時間序列模型傳回的預測結果範圍。在本教學課程中，您將針對相同資料建立兩個時間序列模型，一個模型使用限制，另一個模型則不使用限制。您可以比較模型傳回的結果，瞭解指定限制帶來的差異。

您會使用 [`new_york.citibike_trips`](https://console.cloud.google.com/bigquery?p=bigquery-public-data&%3Bd=new_york&%3Bt=citibike_trips&%3Bpage=table&hl=zh-tw) 資料訓練本教學課程中的模型。這個資料集包含紐約市 Citi Bike 行程的相關資訊。

按照本教學課程操作前，您應熟悉單一時間序列預測。如要瞭解這個主題，請完成「[Google Analytics 資料的單一時間序列預測](https://docs.cloud.google.com/bigquery/docs/arima-single-time-series-forecasting-tutorial?hl=zh-tw)」教學課程。

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

## 目標

在本教學課程中，您會使用下列項目：

* [`CREATE MODEL`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-time-series?hl=zh-tw) 陳述式：用於建立時間序列模型。
* [`ML.FORECAST`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-forecast?hl=zh-tw) 函式：預測每日總造訪次數。

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
- Enable the BigQuery API.

  **Roles required to enable APIs**

  To enable APIs, you need the Service Usage Admin IAM
  role (`roles/serviceusage.serviceUsageAdmin`), which
  contains the `serviceusage.services.enable` permission. [Learn how to grant
  roles](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw).

  [Enable the API](https://console.cloud.google.com/apis/enableflow?apiid=bigquery.googleapis.com&hl=zh-tw)

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
- Enable the BigQuery API.

  **Roles required to enable APIs**

  To enable APIs, you need the Service Usage Admin IAM
  role (`roles/serviceusage.serviceUsageAdmin`), which
  contains the `serviceusage.services.enable` permission. [Learn how to grant
  roles](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw).

  [Enable the API](https://console.cloud.google.com/apis/enableflow?apiid=bigquery.googleapis.com&hl=zh-tw)

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

## 將要預測的時間序列視覺化

建立模型前，建議先查看輸入時間序列的樣貌。

### SQL

在下列查詢中，`FROM bigquery-public-data.new_york.citibike_trips` 子句表示您要查詢 `new_york` 資料集中的 `citibike_trips` 資料表。

在 `SELECT` 陳述式中，查詢會使用 [`EXTRACT` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/timestamp_functions?hl=zh-tw#extract)從 `starttime` 資料欄擷取日期資訊。這項查詢會使用 `COUNT(*)` 子句，取得每日的 Citi Bike 總行程數。

```
#standardSQL
SELECT
  EXTRACT(DATE from starttime) AS date,
  COUNT(*) AS num_trips
FROM
`bigquery-public-data`.new_york.citibike_trips
GROUP BY date
```

如要執行查詢，請按照下列步驟操作：

1. 在 Google Cloud 控制台中，按一下「撰寫新查詢」按鈕。
2. 在查詢編輯器中輸入下列 GoogleSQL 查詢。

   ```
   #standardSQL
   SELECT
    EXTRACT(DATE from starttime) AS date,
    COUNT(*) AS num_trips
   FROM
    `bigquery-public-data`.new_york.citibike_trips
   GROUP BY date
   ```
3. 按一下「執行」。查詢結果類似下方。
4. 使用 Google Cloud 控制台繪製時間序列資料圖表。在「查詢結果」窗格中，按一下「圖表」分頁標籤。在「圖表設定」窗格中，為「圖表類型」選擇「長條圖」：

### BigQuery DataFrames

在嘗試這個範例之前，請按照[使用 BigQuery DataFrames 的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/dataframes-quickstart?hl=zh-tw)中的 BigQuery DataFrames 設定說明操作。
詳情請參閱 [BigQuery DataFrames 參考文件](https://docs.cloud.google.com/python/docs/reference/bigframes/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。
詳情請參閱「[為本機開發環境設定 ADC](https://docs.cloud.google.com/docs/authentication/set-up-adc-local-dev-environment?hl=zh-tw)」。

在下列範例中，`bigquery-public-data.new_york.citibike_trips` 表示您正在查詢 `new_york` 資料集中的 `citibike_trips` 資料表。

```
import bigframes.pandas as bpd

df = bpd.read_gbq("bigquery-public-data.new_york.citibike_trips")

features = bpd.DataFrame(
    {
        "num_trips": df.starttime,
        "date": df["starttime"].dt.date,
    }
)
num_trips = features.groupby(["date"]).count()

num_trips.plot.line()
```

結果大致如下：

## 建立時間序列模型

使用紐約市 Citi Bike 行程資料建立時間序列模型。

以下 GoogleSQL 查詢會建立模型，預測每日單車行程總數。[`CREATE MODEL`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-time-series?hl=zh-tw) 陳述式會建立並訓練名為 `bqml_tutorial.nyc_citibike_arima_model` 的模型。

```
#standardSQL
CREATE OR REPLACE MODEL bqml_tutorial.nyc_citibike_arima_model
  OPTIONS (
    model_type = 'ARIMA_PLUS',
    time_series_timestamp_col = 'date',
    time_series_data_col = 'num_trips',
    time_series_id_col = 'start_station_id')
AS
SELECT
  EXTRACT(DATE FROM starttime) AS date,
  COUNT(*) AS num_trips,
  start_station_id
FROM
  `bigquery-public-data`.new_york.citibike_trips
WHERE starttime > '2014-07-11' AND starttime < '2015-02-11'
GROUP BY date, start_station_id;
```

`OPTIONS(model_type='ARIMA_PLUS', time_series_timestamp_col='date', ...)` 子句代表您要建立以 [ARIMA](https://en.wikipedia.org/wiki/Autoregressive_integrated_moving_average) 為基礎的時間序列模型。根據預設，[`auto_arima=TRUE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-time-series?hl=zh-tw#auto_arima)，因此 `auto.ARIMA` 演算法會自動調整 `ARIMA_PLUS` 模型中的超參數。演算法會套用數十個候選模型，並選擇[赤池訊息量準則 (AIC)](https://en.wikipedia.org/wiki/Akaike_information_criterion) 最低的最佳模型。此外，由於預設值為 `data_frequency='AUTO_FREQUENCY'`，訓練程序會自動推斷輸入時間序列的資料頻率。`CREATE MODEL` 陳述式預設會使用 [`decompose_time_series=TRUE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-time-series?hl=zh-tw#decompose_time_series)，因此時間序列的歷史記錄和預測部分都會儲存在模型中。設定 `time_series_id_col = 'start_station_id'` 參數會導致模型根據 `start_station_id`，使用單一查詢來調整及預測多個時間序列。您可以擷取季節性週期等個別時間序列元件，進一步瞭解時間序列的預測方式。

執行 `CREATE MODEL` 查詢來建立及訓練模型：

1. 在 Google Cloud 控制台中，按一下「撰寫新查詢」按鈕。
2. 在查詢編輯器中輸入下列 GoogleSQL 查詢。

   ```
   #standardSQL
   CREATE OR REPLACE MODEL bqml_tutorial.nyc_citibike_arima_model
   OPTIONS (
     model_type = 'ARIMA_PLUS',
     time_series_timestamp_col = 'date',
     time_series_data_col = 'num_trips',
     time_series_id_col = 'start_station_id')
   AS
   SELECT
   EXTRACT(DATE FROM starttime) AS date,
   COUNT(*) AS num_trips,
   start_station_id
   FROM
   `bigquery-public-data`.new_york.citibike_trips
   WHERE starttime > '2014-07-11' AND starttime < '2015-02-11'
   GROUP BY date, start_station_id;
   ```
3. 按一下「執行」。

   查詢作業約需 80 秒才能完成，完成後您就能存取 (`nyc_citibike_arima_model`) 模型。由於查詢是使用 `CREATE MODEL` 建立模型，因此不會有查詢結果。

**附註：** 您可能會想知道美國節慶是否會影響時間序列。您可以嘗試在查詢的 `OPTIONS` 清單中加入 [holiday\_region='US'](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-time-series?hl=zh-tw#holiday_region)。如果時間序列中確實有美國節慶模式，這項功能就能更準確地模擬這些美國節慶時間點。

## 預測時間序列並以視覺化方式呈現結果

如要說明時間序列的預測方式，請使用 [`ML.FORECAST`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-forecast?hl=zh-tw) 函式，將所有子時間序列元件 (例如季節性和趨勢) 視覺化。

詳細步驟如下：

1. 在 Google Cloud 控制台中，按一下「撰寫新查詢」按鈕。
2. 在查詢編輯器中輸入下列 GoogleSQL 查詢。

   ```
   #standardSQL
   SELECT
   forecast_timestamp AS forecast_timestamp,
   start_station_id AS start_station_id,
   history_value AS history_value,
   forecast_value AS forecast_value
   FROM
   (
     (
        SELECT
        DATE(forecast_timestamp) AS forecast_timestamp,
        NULL AS history_value,
        forecast_value AS forecast_value,
        start_station_id AS start_station_id,
        FROM
        ML.FORECAST(
           MODEL bqml_tutorial.`nyc_citibike_arima_model`,
           STRUCT(
              365 AS horizon,
              0.9 AS confidence_level))
     )
     UNION ALL
     (
        SELECT
        DATE(date_name) AS forecast_timestamp,
        num_trips AS history_value,
        NULL AS forecast_value,
        start_station_id AS start_station_id,
        FROM
        (
           SELECT
              EXTRACT(DATE FROM starttime) AS date_name,
              COUNT(*) AS num_trips,
              start_station_id AS start_station_id
           FROM
              `bigquery-public-data`.new_york.citibike_trips
           WHERE
              starttime > '2014-07-11'
              AND starttime < '2015-02-11'
           GROUP BY
              date_name, start_station_id
        )
     )
   )
   WHERE start_station_id = 79
   ORDER BY
   forecast_timestamp, start_station_id
   ```
3. 按一下「執行」。查詢結果大致如下：
4. 使用 Google Cloud 控制台繪製時間序列資料圖表。在「查詢結果」窗格中，按一下「視覺呈現」分頁標籤：

圖表顯示，Citi Bike 每日總趟次數的預測值 `start_station_id=79` 為負數，這並無參考價值。改用設有限制的模型，可提升預測資料的準確度。

## 建立設有上限的時間序列模型

使用紐約市 Citi Bike 行程資料，建立設有上限的時間序列模型。

以下 GoogleSQL 查詢會建立模型，預測每日單車行程總數。[`CREATE MODEL`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-time-series?hl=zh-tw) 陳述式會建立並訓練名為 `bqml_tutorial.nyc_citibike_arima_model_with_limits` 的模型。這個模型與[先前建立的模型](#forecast_the_time_series_and_visualize_the_results)的主要差異在於新增了 `forecast_limit_lower_bound=0` 選項。這個選項會讓模型只根據 `time_series_data_col` 引數 (在本例中為 `num_trips`) 指定的資料欄值，預測大於 0 的值。

```
#standardSQL
CREATE OR REPLACE MODEL bqml_tutorial.nyc_citibike_arima_model
   OPTIONS (
      model_type = 'ARIMA_PLUS',
      time_series_timestamp_col = 'date',
      time_series_data_col = 'num_trips',
      time_series_id_col = 'start_station_id',
      forecast_limit_lower_bound = 0)
   AS
   SELECT
   EXTRACT(DATE FROM starttime) AS date,
   COUNT(*) AS num_trips,
   start_station_id
   FROM
   `bigquery-public-data`.new_york.citibike_trips
   WHERE starttime > '2014-07-11' AND starttime < '2015-02-11'
   GROUP BY date, start_station_id;
```

執行 `CREATE MODEL` 查詢來建立及訓練模型：

1. 在 Google Cloud 控制台中，按一下「撰寫新查詢」按鈕。
2. 在查詢編輯器中輸入下列 GoogleSQL 查詢。

   ```
   #standardSQL
   CREATE OR REPLACE MODEL bqml_tutorial.nyc_citibike_arima_model
   OPTIONS (
     model_type = 'ARIMA_PLUS',
     time_series_timestamp_col = 'date',
     time_series_data_col = 'num_trips',
     time_series_id_col = 'start_station_id',
     forecast_limit_lower_bound = 0)
   AS
   SELECT
   EXTRACT(DATE FROM starttime) AS date,
   COUNT(*) AS num_trips,
   start_station_id
   FROM
   `bigquery-public-data`.new_york.citibike_trips
   WHERE starttime > '2014-07-11' AND starttime < '2015-02-11'
   GROUP BY date, start_station_id;
   ```
3. 按一下「執行」。

   查詢作業約需 100 秒才能完成，完成後您就能存取 (`nyc_citibike_arima_model_with_limits`) 模型。由於查詢是使用 `CREATE MODEL` 陳述式建立模型，因此不會有查詢結果。

**附註：** 您可能會想知道美國節慶是否會影響時間序列。您可以嘗試在查詢的 `OPTIONS` 清單中加入 [holiday\_region='US'](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-time-series?hl=zh-tw#holiday_region)。如果時間序列中確實有美國節慶模式，這項功能就能更準確地模擬這些美國節慶時間點。

## 使用設有上限的模型預測時間序列

1. 在 Google Cloud 控制台中，按一下「撰寫新查詢」按鈕。
2. 在查詢編輯器中輸入下列 GoogleSQL 查詢。

   ```
   #standardSQL
   SELECT
   forecast_timestamp AS forecast_timestamp,
   start_station_id AS start_station_id,
   history_value AS history_value,
   forecast_value AS forecast_value
   FROM
   (
     (
        SELECT
        DATE(forecast_timestamp) AS forecast_timestamp,
        NULL AS history_value,
        forecast_value AS forecast_value,
        start_station_id AS start_station_id,
        FROM
        ML.FORECAST(
           MODEL bqml_tutorial.`nyc_citibike_arima_model`,
           STRUCT(
              365 AS horizon,
              0.9 AS confidence_level))
     )
     UNION ALL
     (
        SELECT
        DATE(date_name) AS forecast_timestamp,
        num_trips AS history_value,
        NULL AS forecast_value,
        start_station_id AS start_station_id,
        FROM
        (
           SELECT
              EXTRACT(DATE FROM starttime) AS date_name,
              COUNT(*) AS num_trips,
              start_station_id AS start_station_id
           FROM
              `bigquery-public-data`.new_york.citibike_trips
           WHERE
              starttime > '2014-07-11'
              AND starttime < '2015-02-11'
           GROUP BY
              date_name, start_station_id
        )
     )
   )
   WHERE start_station_id = 79
   ORDER BY forecast_timestamp, start_station_id
   ```
3. 按一下「執行」。
4. 使用 Google Cloud 控制台繪製時間序列資料圖表。在「查詢結果」窗格中，按一下「視覺呈現」分頁標籤：

ARIMA PLUS 模型偵測到 Citi Bike 的每日總行程數正在減少。`start_station_id=79`未來的預測值會遵循這項趨勢，而且預測時間越長，預測值就越小。圖表顯示，Citi Bike 每日總行程數的預測值為正數，這更有參考價值。`start_station_id=79`設有限制的模型會偵測到 `start_station_id=79` 的 Citi Bike 每日總趟次數正在減少，但仍會提供有意義的預測值。

如本教學課程所示，`forecast_limit_lower_bound` 和 `forecast_limit_upper_bound` 選項可協助您在類似情境中取得更有意義的預測值，例如預測股價或未來銷售量時。

### 刪除資料集

刪除專案將移除專案中所有的資料集與資料表。若您希望重新使用專案，您可以刪除本教學課程中所建立的資料集。

1. 如有必要，請在Google Cloud 控制台中開啟 BigQuery 頁面。

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

* 瞭解如何[使用紐約市 Citi Bike 行程資料，以單一查詢進行多重時間序列預測](https://docs.cloud.google.com/bigquery/docs/arima-multiple-time-series-forecasting-tutorial?hl=zh-tw)。
* 瞭解如何[加速 ARIMA\_PLUS，在數小時內預測 100 萬個時間序列](https://docs.cloud.google.com/bigquery/docs/arima-speed-up-tutorial?hl=zh-tw)。
* 如要進一步瞭解機器學習，請參閱[機器學習速成課程](https://developers.google.com/machine-learning/crash-course/?hl=zh-tw)。
* 如需 BigQuery ML 的總覽，請參閱 [BigQuery ML 簡介](https://docs.cloud.google.com/bigquery/docs/bqml-introduction?hl=zh-tw)。
* 如要進一步瞭解 Google Cloud 控制台，請參閱「[使用 Google Cloud 控制台](https://docs.cloud.google.com/bigquery/bigquery-web-ui?hl=zh-tw)」。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-16 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-16 (世界標準時間)。"],[],[]]