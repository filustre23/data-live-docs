Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見

# 將 ARIMA\_PLUS 單變數時間序列模型擴展至數百萬個時間序列 透過集合功能整理內容 你可以依據偏好儲存及分類內容。

在本教學課程中，您將瞭解如何大幅加快一組 [`ARIMA_PLUS` 單變量時間序列模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-time-series?hl=zh-tw)的訓練速度，以便透過單一查詢執行多項時間序列預測。您也會瞭解如何評估預測準確度。

本教學課程會預測多個時間序列。系統會針對每個時間點，計算一或多個指定資料欄中每個值的預測值。舉例來說，如果您想預測天氣，並指定包含城市資料的資料欄，預測資料就會包含城市 A 所有時間點的預測值，接著是城市 B 所有時間點的預測值，依此類推。

本教學課程使用公開 [`bigquery-public-data.new_york.citibike_trips`](https://console.cloud.google.com/bigquery?p=bigquery-public-data&%3Bd=new_york&%3Bt=citibike_trips&%3Bpage=table&hl=zh-tw) 和 [`iowa_liquor_sales.sales`](https://console.cloud.google.com/bigquery?p=bigquery-public-data&%3Bd=iowa_liquor_sales&%3Bt=sales&%3Bpage=table&hl=zh-tw) 資料表中的資料。單車行程資料僅包含數百個時間序列，因此可用於說明加速模型訓練的各種策略。酒類銷售資料有超過 100 萬個時間序列，因此可用於大規模的時間序列預測。

閱讀本教學課程前，請先參閱「[使用單變數模型預測多個時間序列](https://docs.cloud.google.com/bigquery/docs/arima-multiple-time-series-forecasting-tutorial?hl=zh-tw)」和「[大規模時間序列預測最佳做法](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-time-series?hl=zh-tw#large-scale-time-series-forecasting-best-practices)」。

## 目標

在本教學課程中，您會使用下列項目：

* 使用 [`CREATE MODEL` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-multivariate-time-series?hl=zh-tw)建立時間序列模型。
* 使用 [`ML.EVALUATE` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-evaluate?hl=zh-tw)評估模型準確率。
* 使用 `CREATE MODEL` 陳述式的 [`AUTO_ARIMA_MAX_ORDER`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-time-series?hl=zh-tw#auto_arima_max_order)、[`TIME_SERIES_LENGTH_FRACTION`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-time-series?hl=zh-tw#time_series_length_fraction)、[`MIN_TIME_SERIES_LENGTH`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-time-series?hl=zh-tw#min_time_series_length) 和 [`MAX_TIME_SERIES_LENGTH`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-time-series?hl=zh-tw#max_time_series_length) 選項，大幅縮短模型訓練時間。

為求簡化，本教學課程不會說明如何使用 [`ML.FORECAST`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-forecast?hl=zh-tw) 或 [`ML.EXPLAIN_FORECAST`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-explain-forecast?hl=zh-tw) 函式生成預測。如要瞭解如何使用這些函式，請參閱「[使用單變數模型預測多個時間序列](https://docs.cloud.google.com/bigquery/docs/arima-multiple-time-series-forecasting-tutorial?hl=zh-tw)」。

## 費用

本教學課程使用 Google Cloud的計費元件，包括：

* BigQuery
* BigQuery ML

如要進一步瞭解費用，請參閱 [BigQuery 定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw)頁面和 [BigQuery ML 定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#bqml)頁面。

## 事前準備

- 登入 Google Cloud 帳戶。如果您未曾使用過 Google Cloud，歡迎[建立帳戶](https://console.cloud.google.com/freetrial?hl=zh-tw)，親自體驗實際使用我們產品的成效。新客戶還能獲得價值 $300 美元的免費抵免額，用於執行、測試及部署工作負載。
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

   啟用 BigQuery API (如果尚未啟用)。

   **啟用 API 所需的角色**

   您必須具備 `serviceusage.services.enable` 權限，才能啟用 API。如果您建立了專案，可能已透過擁有者角色 (`roles/owner`) 取得這項權限。否則，您可以透過 Service Usage 管理員角色 (`roles/serviceusage.serviceUsageAdmin`) 取得這項權限。[瞭解如何授予角色](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)。

   [啟用 API](https://console.cloud.google.com/apis/enableflow?apiid=bigquery&hl=zh-tw)

## 所需權限

* 如要建立資料集，您必須具備 `bigquery.datasets.create` IAM 權限。
* 如要建立模型，您必須具備下列權限：

  + `bigquery.jobs.create`
  + `bigquery.models.create`
  + `bigquery.models.getData`
  + `bigquery.models.updateData`
* 如要執行推論，您必須具備下列權限：

  + `bigquery.models.getData`
  + `bigquery.jobs.create`

如要進一步瞭解 BigQuery 的 IAM 角色和權限，請參閱「[IAM 簡介](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)」。

## 建立資料集

如要建立 BigQuery 資料集，請選取下列其中一個選項：

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。

   如果沒有看到左側窗格，請按一下 last\_page「Expand left pane」(展開左側窗格)，開啟窗格。
3. 在「Explorer」中展開專案，然後按一下「資料集」。
4. 在「Datasets」(資料集) 頁面，按一下add「Create dataset」(建立資料集)。
5. 在「建立資料集」窗格中，執行下列操作：

   * 在「Dataset ID」(資料集 ID) 中輸入 `bqml_tutorial`。
   * 在「資料位置」部分，選取「US」。

   其餘預設設定則保持不變。
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
2. 確認資料集已建立：

   ```
   bq ls
   ```

### API

使用定義的[資料集資源](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/datasets?hl=zh-tw)呼叫 [`datasets.insert`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/datasets/insert?hl=zh-tw) 方法：

```
{
  "datasetReference": {
     "datasetId": "bqml_tutorial"
  }
}
```

## 建立輸入資料表

下列查詢的 `SELECT` 陳述式會使用 [`EXTRACT` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/timestamp_functions?hl=zh-tw#extract)，從 `starttime` 欄擷取日期資訊。查詢會使用 `COUNT(*)` 子句，取得每日 Citi Bike 行程總數。

`table_1`有 679 個時間序列。查詢會使用額外的 `INNER JOIN` 邏輯，選取時間點超過 400 個的所有時間序列，總共會產生 383 個時間序列。

請按照下列步驟建立輸入資料表：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中貼上以下查詢，然後點選「執行」：

   ```
   CREATE OR REPLACE TABLE
     `bqml_tutorial.nyc_citibike_time_series` AS
   WITH input_time_series AS
   (
     SELECT
       start_station_name,
       EXTRACT(DATE FROM starttime) AS date,
       COUNT(*) AS num_trips
     FROM
       `bigquery-public-data.new_york.citibike_trips`
     GROUP BY
       start_station_name, date
   )
   SELECT table_1.*
   FROM input_time_series AS table_1
   INNER JOIN (
     SELECT start_station_name,  COUNT(*) AS num_points
     FROM input_time_series
     GROUP BY start_station_name) table_2
   ON
     table_1.start_station_name = table_2.start_station_name
   WHERE
     num_points > 400;
   ```

## 使用預設參數建立多個時間序列的模型

您想預測每個 Citi Bike 站點的單車行程數量，這需要許多時間序列模型，每個模型分別對應輸入資料中包含的各個 Citi Bike 站點。您可以編寫多個 [`CREATE MODEL`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-time-series?hl=zh-tw) 查詢來執行這項操作，但這項程序可能相當繁瑣且耗時，尤其是在有大量時間序列的情況下。您可以改用單一查詢建立及擬合一組時間序列模型，一次預測多個時間序列。

`OPTIONS(model_type='ARIMA_PLUS', time_series_timestamp_col='date', ...)` 子句表示您正在建立一組以 [ARIMA](https://en.wikipedia.org/wiki/Autoregressive_integrated_moving_average) 為基礎的時間序列 `ARIMA_PLUS` 模型。`time_series_timestamp_col` 選項會指定包含時間序列的資料欄，`time_series_data_col` 選項會指定要預測的資料欄，`time_series_id_col` 則會指定要建立時間序列的一或多個維度。

這個範例會省略 2016 年 6 月 1 日之後的時間序列時間點，以便稍後使用 `ML.EVALUATE` 函式評估預測準確度。

請按照下列步驟建立模型：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中貼上以下查詢，然後點選「執行」：

   ```
   CREATE OR REPLACE MODEL `bqml_tutorial.nyc_citibike_arima_model_default`
   OPTIONS
     (model_type = 'ARIMA_PLUS',
     time_series_timestamp_col = 'date',
     time_series_data_col = 'num_trips',
     time_series_id_col = 'start_station_name'
     ) AS
   SELECT *
   FROM bqml_tutorial.nyc_citibike_time_series
   WHERE date < '2016-06-01';
   ```

   查詢作業約需 15 分鐘才能完成。

## 評估每個時間序列的預測準確度

使用 `ML.EVALUATE` 函式評估模型的預測準確度。

請按照下列步驟評估模型：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中貼上以下查詢，然後點選「執行」：

   ```
   SELECT *
   FROM
     ML.EVALUATE(MODEL `bqml_tutorial.nyc_citibike_arima_model_default`,
     TABLE `bqml_tutorial.nyc_citibike_time_series`,
     STRUCT(7 AS horizon, TRUE AS perform_aggregation));
   ```

   這項查詢會回報多項預測指標，包括：

   結果應大致如下：

   `ML.EVALUATE` 函式中的 `TABLE` 子句會識別含有基準真相資料的資料表。系統會將預測結果與基準真相資料進行比較，計算準確度指標。在本例中，`nyc_citibike_time_series` 包含 2016 年 6 月 1 日前後的時間序列點。2016 年 6 月 1 日之後的點是基準真相資料。2016 年 6 月 1 日之前的資料點會用於訓練模型，以產生該日期之後的預測資料。計算指標時，只需要 2016 年 6 月 1 日之後的資料點。計算指標時，系統會忽略 2016 年 6 月 1 日之前的資料點。

   `ML.EVALUATE` 函式中的 `STRUCT` 子句指定了函式的參數。`horizon` 值為 `7`，表示查詢會根據七點預測計算預測準確度。請注意，如果基準真相資料的比較點少於七個，系統只會根據可用的點計算準確度指標。`perform_aggregation` 值為 `TRUE`，表示預測準確度指標是依時間點匯總。如果將 `perform_aggregation` 值指定為 `FALSE`，系統會傳回每個預測時間點的預測準確率。

   如要進一步瞭解輸出資料欄，請參閱「[`ML.EVALUATE` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-evaluate?hl=zh-tw)」。

## 評估整體預測準確度

評估所有 383 個時間序列的預測準確度。

在 [`ML.EVALUATE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-evaluate?hl=zh-tw) 傳回的預測指標中，只有[平均絕對百分比誤差](https://en.wikipedia.org/wiki/Mean_absolute_percentage_error)和[對稱平均絕對百分比誤差](https://en.wikipedia.org/wiki/Symmetric_mean_absolute_percentage_error)與時間序列值無關。因此，如要評估一組時間序列的整體預測準確度，只有這兩項指標的匯總值才有意義。

請按照下列步驟評估模型：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中貼上以下查詢，然後點選「執行」：

   ```
   SELECT
     AVG(mean_absolute_percentage_error) AS MAPE,
     AVG(symmetric_mean_absolute_percentage_error) AS sMAPE
   FROM
     ML.EVALUATE(MODEL `bqml_tutorial.nyc_citibike_arima_model_default`,
       TABLE `bqml_tutorial.nyc_citibike_time_series`,
       STRUCT(7 AS horizon, TRUE AS perform_aggregation));
   ```

這項查詢會傳回 `0.3471` 的 `MAPE` 值，以及 `0.2563` 的 `sMAPE` 值。

## 建立模型，以較小的超參數搜尋空間預測多個時間序列

在「[使用預設參數建立多個時間序列的模型](#arima-model-group)」一節中，您對所有訓練選項 (包括 `auto_arima_max_order` 選項) 使用預設值。這個選項可控制 `auto.ARIMA` 演算法中超參數調整的搜尋空間。

在下列查詢建立的模型中，您將 `auto_arima_max_order` 選項值從預設的 `5` 變更為 `2`，藉此縮小超參數的搜尋空間。

請按照下列步驟評估模型：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中貼上以下查詢，然後點選「執行」：

   ```
   CREATE OR REPLACE MODEL `bqml_tutorial.nyc_citibike_arima_model_max_order_2`
   OPTIONS
     (model_type = 'ARIMA_PLUS',
     time_series_timestamp_col = 'date',
     time_series_data_col = 'num_trips',
     time_series_id_col = 'start_station_name',
     auto_arima_max_order = 2
     ) AS
   SELECT *
   FROM `bqml_tutorial.nyc_citibike_time_series`
   WHERE date < '2016-06-01';
   ```

   查詢作業大約需要 2 分鐘才能完成。先前模型在 `auto_arima_max_order` 值為 `5` 時，需要約 15 分鐘才能完成，因此這項變更可將模型訓練速度提升約 7 倍。如果您想知道為什麼速度提升幅度不是 `5/2=2.5x`，這是因為當 `auto_arima_max_order` 值增加時，候選模型的數量和複雜度都會增加。這會導致模型訓練時間增加。

## 評估超參數搜尋空間較小的模型預測準確度

請按照下列步驟評估模型：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中貼上以下查詢，然後點選「執行」：

   ```
   SELECT
     AVG(mean_absolute_percentage_error) AS MAPE,
     AVG(symmetric_mean_absolute_percentage_error) AS sMAPE
   FROM
     ML.EVALUATE(MODEL `bqml_tutorial.nyc_citibike_arima_model_max_order_2`,
       TABLE `bqml_tutorial.nyc_citibike_time_series`,
       STRUCT(7 AS horizon, TRUE AS perform_aggregation));
   ```

這項查詢會傳回 `0.3337` 的 `MAPE` 值，以及 `0.2337` 的 `sMAPE` 值。

在「[評估整體預測準確度](#evaluate_overall_forecasting_accuracy)」一節中，您評估了超參數搜尋空間較大的模型，其中 `auto_arima_max_order` 選項值為 `5`。這會產生 `0.3471` 的 `MAPE` 值，以及 `0.2563` 的 `sMAPE` 值。在這個例子中，您可以看到較小的超參數搜尋空間，實際上能提供更高的預測準確度。其中一個原因是，`auto.ARIMA` 演算法只會針對整個建模管道的趨勢模組執行超參數調整。`auto.ARIMA` 演算法選出的最佳 ARIMA 模型，不一定能為整個管道產生最佳預測結果。

## 建立模型，以較小的超參數搜尋空間和智慧快速訓練策略，預測多個時間序列

在這個步驟中，您會使用較小的超參數搜尋空間，並透過一或多個 `max_time_series_length`、`max_time_series_length` 或 `time_series_length_fraction` 訓練選項，採用智慧快速訓練策略。

雖然季節性等週期性建模需要一定數量的時間點，但趨勢建模需要的時間點較少。同時，趨勢建模的運算成本也比季節性等其他時間序列元件高得多。使用上述快速訓練選項，您就能有效率地使用時間序列子集，為趨勢元件建立模型，而其他時間序列元件則使用整個時間序列。

以下範例使用 `max_time_series_length` 選項，快速完成訓練。將 `max_time_series_length` 選項值設為 `30`，系統只會使用最近 30 個時間點來建立趨勢元件模型。所有 383 個時間序列仍用於模擬非趨勢元件。

請按照下列步驟建立模型：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中貼上以下查詢，然後點選「執行」：

   ```
   CREATE OR REPLACE MODEL `bqml_tutorial.nyc_citibike_arima_model_max_order_2_fast_training`
   OPTIONS
     (model_type = 'ARIMA_PLUS',
     time_series_timestamp_col = 'date',
     time_series_data_col = 'num_trips',
     time_series_id_col = 'start_station_name',
     auto_arima_max_order = 2,
     max_time_series_length = 30
     ) AS
   SELECT *
   FROM `bqml_tutorial.nyc_citibike_time_series`
   WHERE date < '2016-06-01';
   ```

   查詢作業約需 35 秒才能完成。這比您在「[建立模型，以較小的超參數搜尋空間預測多個時間序列](#small-search-space)」一節中使用的查詢快 3 倍。由於查詢的非訓練部分 (例如資料預先處理) 具有固定的時間負擔，因此當時間序列數量遠大於本範例時，速度提升幅度會更高。如果有一百萬個時間序列，速度提升幅度會接近時間序列長度與 `max_time_series_length` 選項值的比率。在這種情況下，速度提升幅度會超過 10 倍。

## 使用超參數搜尋空間較小的模型和智慧快速訓練策略，評估預測準確度

請按照下列步驟評估模型：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中貼上以下查詢，然後點選「執行」：

   ```
   SELECT
     AVG(mean_absolute_percentage_error) AS MAPE,
     AVG(symmetric_mean_absolute_percentage_error) AS sMAPE
   FROM
     ML.EVALUATE(MODEL `bqml_tutorial.nyc_citibike_arima_model_max_order_2_fast_training`,
       TABLE `bqml_tutorial.nyc_citibike_time_series`,
       STRUCT(7 AS horizon, TRUE AS perform_aggregation));
   ```

這項查詢會傳回 `0.3515` 的 `MAPE` 值，以及 `0.2473` 的 `sMAPE` 值。

請注意，如果不使用快速訓練策略，預測準確度的 `MAPE` 值為 `0.3337`，`sMAPE` 值為 `0.2337`。兩組指標值的差異在 3% 以內，不具統計顯著性。

簡而言之，您使用較小的超參數搜尋空間和智慧型快速訓練策略，在不犧牲預測準確度的情況下，將模型訓練速度提升 20 倍以上。如前所述，時間序列越多，智慧快速訓練策略提升的速度就越顯著。此外，`ARIMA_PLUS` 模型使用的基礎 ARIMA 程式庫也經過最佳化，執行速度比以往快 5 倍。這些優勢結合起來，就能在數小時內預測數百萬個時間序列。

## 建立模型來預測一百萬個時間序列

在這個步驟中，您將使用公開的愛荷華州酒類銷售資料，預測不同商店中超過 100 萬種酒類產品的銷售量。模型訓練會使用小型超參數搜尋空間，以及智慧快速訓練策略。

請按照下列步驟評估模型：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中貼上以下查詢，然後點選「執行」：

   ```
   CREATE OR REPLACE MODEL
     `bqml_tutorial.liquor_forecast_by_product`
   OPTIONS(
     MODEL_TYPE = 'ARIMA_PLUS',
     TIME_SERIES_TIMESTAMP_COL = 'date',
     TIME_SERIES_DATA_COL = 'total_bottles_sold',
     TIME_SERIES_ID_COL = ['store_number', 'item_description'],
     HOLIDAY_REGION = 'US',
     AUTO_ARIMA_MAX_ORDER = 2,
     MAX_TIME_SERIES_LENGTH = 30
   ) AS
   SELECT
     store_number,
     item_description,
     date,
     SUM(bottles_sold) as total_bottles_sold
   FROM
     `bigquery-public-data.iowa_liquor_sales.sales`
   WHERE date BETWEEN DATE("2015-01-01") AND DATE("2021-12-31")
   GROUP BY store_number, item_description, date;
   ```

   查詢作業約需 1 小時 16 分鐘才能完成。

## 清除所用資源

為避免因為本教學課程所用資源，導致系統向 Google Cloud 帳戶收取費用，請刪除含有相關資源的專案，或者保留專案但刪除個別資源。

* 您可以刪除建立的專案。
* 或者您可以保留專案並刪除資料集。

### 刪除資料集

刪除專案將移除專案中所有的資料集與資料表。若您希望重新使用專案，您可以刪除本教學課程中所建立的資料集。

1. 如有需要，請在Google Cloud 控制台開啟 BigQuery 頁面。

   [前往「BigQuery」頁面](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在導覽窗格中，按一下您建立的 **bqml\_tutorial** 資料集。
3. 按一下「Delete dataset」(刪除資料集)，即可刪除資料集、資料表和所有資料。
4. 在「Delete dataset」(刪除資料集) 對話方塊中，輸入資料集名稱 (`bqml_tutorial`) 來確認刪除指令，然後點選「Delete」(刪除)。

### 刪除專案

如要刪除專案，請進行以下操作：

**警告**：刪除專案會出現以下結果：

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
* 瞭解如何[使用單變數模型預測多個時間序列](https://docs.cloud.google.com/bigquery/docs/arima-multiple-time-series-forecasting-tutorial?hl=zh-tw)
* 瞭解如何[使用單變數模型，以階層方式預測多個時間序列](https://docs.cloud.google.com/bigquery/docs/arima-time-series-forecasting-with-hierarchical-time-series?hl=zh-tw)
* 如要瞭解 BigQuery ML，請參閱「[BigQuery AI 和機器學習簡介](https://docs.cloud.google.com/bigquery/docs/bqml-introduction?hl=zh-tw)」。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-11-08 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-11-08 (世界標準時間)。"],[],[]]