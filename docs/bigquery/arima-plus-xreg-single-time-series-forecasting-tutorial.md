Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見

# 使用多變數模型預測單一時間序列 透過集合功能整理內容 你可以依據偏好儲存及分類內容。

本教學課程說明如何使用[多元時間序列模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-multivariate-time-series?hl=zh-tw)，根據多個輸入特徵的歷史值，預測特定資料欄的未來值。

本教學課程會預測單一時間序列。系統會針對輸入資料中的每個時間點計算一次預測值。

本教學課程會使用[`bigquery-public-data.epa_historical_air_quality`公開資料集](https://console.cloud.google.com/bigquery?p=bigquery-public-data&%3Bd=epa_historical_air_quality&%3Bpage=dataset&hl=zh-tw)的資料。這個資料集包含美國多個城市收集的每日細懸浮微粒 (PM2.5)、溫度和風速資訊。

## 目標

本教學課程會逐步引導您完成下列工作：

* 使用 [`CREATE MODEL` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-multivariate-time-series?hl=zh-tw)建立時間序列模型，預測 PM2.5 值。
* 使用 [`ML.ARIMA_EVALUATE` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-arima-evaluate?hl=zh-tw)評估模型中的自迴歸整合移動平均 (ARIMA) 資訊。
* 使用 [`ML.ARIMA_COEFFICIENTS` 函式檢查模型係數](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-arima-coefficients?hl=zh-tw)。
* 使用 [`ML.FORECAST` 函式從模型擷取預測的 PM2.5 值](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-forecast?hl=zh-tw)。
* 使用 [`ML.EVALUATE` 函式評估模型準確率](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-evaluate?hl=zh-tw)。
* 使用 [`ML.EXPLAIN_FORECAST` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-explain-forecast?hl=zh-tw)擷取時間序列的元件，例如季節性、趨勢和特徵屬性。您可以檢查這些時間序列元件，說明預測值。

## 費用

本教學課程使用的 Google Cloud計費元件包括：

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

## 建立輸入資料表

建立資料表，用來訓練及評估模型。這個資料表會合併 `bigquery-public-data.epa_historical_air_quality` 資料集中的多個資料表，提供每日天氣資料。您也會建立下列資料欄，做為模型的輸入變數：

* `date`：觀察日期
* `pm25` 每天的 PM2.5 平均值
* `wind_speed`：每天的平均風速
* `temperature`：每天的最高溫

在下列 GoogleSQL 查詢中，`FROM bigquery-public-data.epa_historical_air_quality.*_daily_summary` 子句表示您要查詢 `epa_historical_air_quality` 資料集中的 `*_daily_summary` 資料表。這些資料表是[分區資料表](https://docs.cloud.google.com/bigquery/docs/partitioned-tables?hl=zh-tw)。

請按照下列步驟建立輸入資料表：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中貼入下列查詢，然後點選「執行」：

   ```
   CREATE TABLE `bqml_tutorial.seattle_air_quality_daily`
   AS
   WITH
     pm25_daily AS (
       SELECT
         avg(arithmetic_mean) AS pm25, date_local AS date
       FROM
         `bigquery-public-data.epa_historical_air_quality.pm25_nonfrm_daily_summary`
       WHERE
         city_name = 'Seattle'
         AND parameter_name = 'Acceptable PM2.5 AQI & Speciation Mass'
       GROUP BY date_local
     ),
     wind_speed_daily AS (
       SELECT
         avg(arithmetic_mean) AS wind_speed, date_local AS date
       FROM
         `bigquery-public-data.epa_historical_air_quality.wind_daily_summary`
       WHERE
         city_name = 'Seattle' AND parameter_name = 'Wind Speed - Resultant'
       GROUP BY date_local
     ),
     temperature_daily AS (
       SELECT
         avg(first_max_value) AS temperature, date_local AS date
       FROM
         `bigquery-public-data.epa_historical_air_quality.temperature_daily_summary`
       WHERE
         city_name = 'Seattle' AND parameter_name = 'Outdoor Temperature'
       GROUP BY date_local
     )
   SELECT
     pm25_daily.date AS date, pm25, wind_speed, temperature
   FROM pm25_daily
   JOIN wind_speed_daily USING (date)
   JOIN temperature_daily USING (date);
   ```

## 以圖表呈現輸入資料

建立模型前，您可以選擇以視覺化方式呈現輸入時間序列資料，瞭解資料分布情形。您可以使用 Data Studio 達成這個目標。

請按照下列步驟將時間序列資料視覺化：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中貼入下列查詢，然後點選「執行」：

   ```
   SELECT
     *
   FROM
     `bqml_tutorial.seattle_air_quality_daily`;
   ```
3. 查詢完成後，依序點選「開啟方式」>「數據分析」。系統會在新的分頁中開啟 Data Studio。在新分頁中完成下列步驟。
4. 在數據分析中，依序點選 **插入** >
   **時間序列圖表**。
5. 在「圖表」窗格中，選擇「設定」分頁。
6. 在「指標」專區中，新增 **pm25**、**temperature** 和 **wind\_speed** 欄位，並移除預設的「記錄計數」指標。產生的圖表如下所示：

   從圖表可以看出，輸入時間序列具有每週季節性模式。

**注意：** 如要進一步瞭解數據分析支援服務，請參閱[數據分析說明和支援選項](https://docs.cloud.google.com/looker/docs/studio/contact-us?hl=zh-tw)。

## 建立時間序列模型

使用 `pm25`、`wind_speed` 和 `temperature` 資料欄值做為輸入變數，建立時間序列模型來預測 `pm25` 資料欄代表的懸浮微粒值。在 `bqml_tutorial.seattle_air_quality_daily` 資料表中的空氣品質資料上訓練模型，並選取 2012 年 1 月 1 日至 2020 年 12 月 31 日之間收集的資料。

在下列查詢中，`OPTIONS(model_type='ARIMA_PLUS_XREG',
time_series_timestamp_col='date', ...)` 子句表示您要建立具有外部迴歸因子的 ARIMA 模型。[`auto_arima` 選項](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-multivariate-time-series?hl=zh-tw#auto_arima)的 `CREATE MODEL` 陳述式預設為 `TRUE`，因此 `auto.ARIMA` 演算法會自動調整模型中的超參數。演算法會套用數十個候選模型，並選擇最佳模型，也就是[赤池資訊量準則 (AIC)](https://en.wikipedia.org/wiki/Akaike_information_criterion) 最低的模型。[`data_frequency` 陳述式的](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-multivariate-time-series?hl=zh-tw#data_frequency) `CREATE MODEL` 選項預設為 `AUTO_FREQUENCY`，因此訓練程序會自動推斷輸入時間序列的資料頻率。

請按照下列步驟建立模型：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中貼入下列查詢，然後點選「執行」：

   ```
   CREATE OR REPLACE
     MODEL
       `bqml_tutorial.seattle_pm25_xreg_model`
     OPTIONS (
       MODEL_TYPE = 'ARIMA_PLUS_XREG',
       time_series_timestamp_col = 'date',  # Identifies the column that contains time points
       time_series_data_col = 'pm25')       # Identifies the column to forecast
   AS
   SELECT
     date,                                  # The column that contains time points
     pm25,                                  # The column to forecast
     temperature,                           # Temperature input to use in forecasting
     wind_speed                             # Wind speed input to use in forecasting
   FROM
     `bqml_tutorial.seattle_air_quality_daily`
   WHERE
     date
     BETWEEN DATE('2012-01-01')
     AND DATE('2020-12-31');
   ```

   查詢大約需要 20 秒才能完成，完成後您就能存取 `seattle_pm25_xreg_model` 模型。由於查詢使用 `CREATE MODEL` 陳述式建立模型，因此您不會看到查詢結果。

**注意：** 您可能會想知道美國國定假日是否會影響時間序列。您可以嘗試將 `CREATE MODEL` 陳述式的 [`holiday_region` 選項](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-multivariate-time-series?hl=zh-tw#holiday_region)設為 `US`。如果時間序列中存在任何節慶模式，設定這個選項可讓系統更準確地模擬節慶時間點。

## 評估候選模型

使用 `ML.ARIMA_EVALUATE` 函式評估時間序列模型。`ML.ARIMA_EVALUATE` 函式會顯示自動超參數調整程序中評估的所有候選模型的評估指標。

如要評估模型，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中貼入下列查詢，然後點選「執行」：

   ```
   SELECT
    *
   FROM
    ML.ARIMA_EVALUATE(MODEL `bqml_tutorial.seattle_pm25_xreg_model`);
   ```

   結果應如下所示：

   `non_seasonal_p`、`non_seasonal_d`、`non_seasonal_q` 和 `has_drift` 輸出資料欄會在訓練管道中定義 ARIMA 模型。`log_likelihood`、`AIC` 和 `variance` 輸出資料欄與 ARIMA 模型校正程序相關。

   `auto.ARIMA` 演算法會使用 [KPSS 檢定](https://en.wikipedia.org/wiki/KPSS_test)，判斷 `non_seasonal_d` 的最佳值，也就是本例中的 `1`。當 `non_seasonal_d` 為 `1` 時，`auto.ARIMA` 演算法會平行訓練 42 個不同的候選 ARIMA 模型。在本例中，所有 42 個候選模型都有效，因此輸出內容包含 42 列，每列對應一個候選 ARIMA 模型；如果部分模型無效，則會從輸出內容中排除。這些候選模型會依 AIC 遞增順序傳回。第一列中的模型 AIC 最低，因此視為最佳模型。最佳模型會儲存為最終模型，並在您呼叫模型上的 `ML.FORECAST` 等函式時使用。

   `seasonal_periods` 欄包含時間序列資料中識別出的季節性模式相關資訊。這與 ARIMA 建模無關，因此所有輸出資料列的值都相同。這份報表顯示每週模式，與您選擇將輸入資料視覺化時看到的結果一致。

   `has_holiday_effect`、`has_spikes_and_dips` 和 `has_step_changes` 欄提供輸入時間序列資料的相關資訊，與 ARIMA 建模無關。系統傳回這些資料欄，是因為 `CREATE MODEL` 陳述式中的 `decompose_time_series` 選項值為 `TRUE`。所有輸出資料列的這些資料欄值也相同。

   「`error_message`」欄會顯示在`auto.ARIMA`擬合程序中發生的任何錯誤。如果所選的 `non_seasonal_p`、`non_seasonal_d`、`non_seasonal_q` 和 `has_drift` 欄無法穩定時間序列，就可能發生錯誤。如要擷取所有候選模型的錯誤訊息，請在建立模型時將 `show_all_candidate_models` 選項設為 `TRUE`。

   如要進一步瞭解輸出資料欄，請參閱 [`ML.ARIMA_EVALUATE` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-arima-evaluate?hl=zh-tw)。

## 檢查模型的係數

使用 `ML.ARIMA_COEFFICIENTS` 函式檢查時間序列模型的係數。

請按照下列步驟擷取模型的係數：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中貼入下列查詢，然後點選「執行」：

   ```
   SELECT
    *
   FROM
    ML.ARIMA_COEFFICIENTS(MODEL `bqml_tutorial.seattle_pm25_xreg_model`);
   ```

   結果應如下所示：

   `ar_coefficients` 輸出資料欄會顯示 ARIMA 模型自迴歸 (AR) 部分的模型係數。同樣地，`ma_coefficients` 輸出資料欄會顯示 ARIMA 模型移動平均 (MA) 部分的模型係數。這兩欄都包含陣列值，長度分別等於 `non_seasonal_p` 和 `non_seasonal_q`。您在 `ML.ARIMA_EVALUATE` 函式的輸出內容中看到，最佳模型的 `non_seasonal_p` 值為 `0`，`non_seasonal_q` 值為 `5`。因此，在 `ML.ARIMA_COEFFICIENTS` 輸出中，`ar_coefficients` 值為空陣列，而 `ma_coefficients` 值為 5 個元素的陣列。`intercept_or_drift` 值是 ARIMA 模型中的常數項。

   `processed_input`、`weight` 和 `category_weights` 輸出資料欄會顯示線性迴歸模型中每個特徵的權重和截距。如果特徵是數值特徵，權重會顯示在 `weight` 欄中。如果特徵是類別特徵，`category_weights` 值會是結構值陣列，其中每個結構值都包含特定類別的名稱和權重。

   如要進一步瞭解輸出資料欄，請參閱 [`ML.ARIMA_COEFFICIENTS` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-arima-coefficients?hl=zh-tw)。

## 使用模型預測資料

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
     ML.FORECAST(
       MODEL `bqml_tutorial.seattle_pm25_xreg_model`,
       STRUCT(30 AS horizon, 0.8 AS confidence_level),
       (
         SELECT
           date,
           temperature,
           wind_speed
         FROM
           `bqml_tutorial.seattle_air_quality_daily`
         WHERE
           date > DATE('2020-12-31')
       ));
   ```

   結果應如下所示：

   輸出資料列會依 `forecast_timestamp` 欄值的時間順序排列。在時間序列預測中，預測間隔 (以 `prediction_interval_lower_bound` 和 `prediction_interval_upper_bound` 資料欄值表示) 與 `forecast_value` 資料欄值同樣重要。`forecast_value` 值是預測間隔的中間點，預測間隔取決於 `standard_error` 和 `confidence_level` 欄的值。

   如要進一步瞭解輸出資料欄，請參閱 [`ML.FORECAST` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-forecast?hl=zh-tw)。

## 評估預測準確率

使用 `ML.EVALUATE` 函式評估模型的預測準確度。

在下列 GoogleSQL 查詢中，第二個 `SELECT` 陳述式提供含有未來特徵的資料，用於預測未來值，以便與實際資料比較。

如要評估模型準確率，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中貼入下列查詢，然後點選「執行」：

   ```
   SELECT
     *
   FROM
     ML.EVALUATE(
       MODEL `bqml_tutorial.seattle_pm25_xreg_model`,
       (
         SELECT
           date,
           pm25,
           temperature,
           wind_speed
         FROM
           `bqml_tutorial.seattle_air_quality_daily`
         WHERE
           date > DATE('2020-12-31')
       ),
       STRUCT(
         TRUE AS perform_aggregation,
         30 AS horizon));
   ```

   結果應如下所示：

   如要進一步瞭解輸出資料欄，請參閱 [`ML.EVALUATE` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-evaluate?hl=zh-tw)。

## 說明預測結果

除了預測資料，您也可以使用 `ML.EXPLAIN_FORECAST` 函式取得可解釋性指標。`ML.EXPLAIN_FORECAST` 函式會預測未來時間序列值，並傳回時間序列的所有個別元件。

與 `ML.FORECAST` 函式類似，`ML.EXPLAIN_FORECAST` 函式中使用的 `STRUCT(30 AS horizon, 0.8 AS confidence_level)` 子句表示查詢會預測未來 30 個時間點，並產生信賴度為 80% 的預測間隔。

如要說明模型的結果，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中貼入下列查詢，然後點選「執行」：

   ```
   SELECT
     *
   FROM
     ML.EXPLAIN_FORECAST(
       MODEL `bqml_tutorial.seattle_pm25_xreg_model`,
       STRUCT(30 AS horizon, 0.8 AS confidence_level),
       (
         SELECT
           date,
           temperature,
           wind_speed
         FROM
           `bqml_tutorial.seattle_air_quality_daily`
         WHERE
           date > DATE('2020-12-31')
       ));
   ```

   結果應如下所示：

   輸出資料列會依 `time_series_timestamp` 資料欄值按時間順序排序。

   如要進一步瞭解輸出資料欄，請參閱 [`ML.EXPLAIN_FORECAST` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-explain-forecast?hl=zh-tw)。

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

* 瞭解如何[使用單變數模型預測單一時間序列](https://docs.cloud.google.com/bigquery/docs/arima-single-time-series-forecasting-tutorial?hl=zh-tw)
* 瞭解如何[使用單變數模型預測多個時間序列](https://docs.cloud.google.com/bigquery/docs/arima-multiple-time-series-forecasting-tutorial?hl=zh-tw)
* 瞭解如何[在預測多個資料列的時間序列時，擴充單變數模型](https://docs.cloud.google.com/bigquery/docs/arima-speed-up-tutorial?hl=zh-tw)。
* 瞭解如何[使用單變數模型，以階層方式預測多個時間序列](https://docs.cloud.google.com/bigquery/docs/arima-time-series-forecasting-with-hierarchical-time-series?hl=zh-tw)
* 如需 BigQuery ML 的總覽，請參閱「[BigQuery 中的 AI 和 ML 簡介](https://docs.cloud.google.com/bigquery/docs/bqml-introduction?hl=zh-tw)」。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-10-29 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-10-29 (世界標準時間)。"],[],[]]