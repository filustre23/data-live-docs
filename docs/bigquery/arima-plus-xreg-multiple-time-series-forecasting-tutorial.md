Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見

# 使用多變數模型預測多個時間序列 透過集合功能整理內容 你可以依據偏好儲存及分類內容。

本教學課程說明如何使用[多變量時間序列模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-multivariate-time-series?hl=zh-tw)，根據多個輸入特徵的歷來值，預測指定資料欄的未來值。

本教學課程會預測多個時間序列。系統會針對每個時間點，計算一或多個指定資料欄中每個值的預測值。舉例來說，如果您想預測天氣，並指定包含州資料的資料欄，則預測資料會包含州 A 所有時間點的預測值，然後是州 B 所有時間點的預測值，依此類推。如果您想預測天氣，並指定包含州和城市資料的資料欄，預測資料就會包含州 A 和城市 A 所有時間點的預測值，接著是州 A 和城市 B 所有時間點的預測值，依此類推。

本教學課程使用公開 [`bigquery-public-data.iowa_liquor_sales.sales`](https://console.cloud.google.com/bigquery?p=bigquery-public-data&%3Bd=iowa_liquor_sales&%3Bpage=dataset&%3Bt=sales&%3Bpage=table&hl=zh-tw) 和 [`bigquery-public-data.covid19_weathersource_com.postal_code_day_history`](https://console.cloud.google.com/bigquery?p=bigquery-public-data&%3Bd=covid19_weathersource_com&%3Bpage=dataset&%3Bt=postal_code_day_history&%3Bpage=table&hl=zh-tw) 資料表中的資料。`bigquery-public-data.iowa_liquor_sales.sales` 資料表包含從愛荷華州多個城市收集的酒類銷售資料。`bigquery-public-data.covid19_weathersource_com.postal_code_day_history` 資料表包含世界各地的歷史天氣資料，例如溫度和濕度。

閱讀本教學課程之前，強烈建議您先參閱「[使用多變數模型預測單一時間序列](https://docs.cloud.google.com/bigquery/docs/arima-plus-xreg-single-time-series-forecasting-tutorial?hl=zh-tw)」。

## 目標

本教學課程會逐步引導您完成下列工作：

* 使用 [`CREATE MODEL` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-multivariate-time-series?hl=zh-tw)建立時間序列模型，預測酒類商店訂單。
* 使用 [`ML.FORECAST` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-forecast?hl=zh-tw)從模型擷取預測訂單價值。
* 使用 [`ML.EXPLAIN_FORECAST` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-explain-forecast?hl=zh-tw)擷取時間序列的元件，例如季節性、趨勢和特徵歸因。您可以檢查這些時間序列元件，以說明預測值。
* 使用 [`ML.EVALUATE` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-evaluate?hl=zh-tw)評估模型準確率。
* 使用 [`ML.DETECT_ANOMALIES` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-detect-anomalies?hl=zh-tw)搭配模型偵測異常狀況。

## 費用

本教學課程使用 Google Cloud的計費元件，包括：

* BigQuery
* BigQuery ML

如要進一步瞭解 BigQuery 費用，請參閱「[BigQuery 定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw)」頁面。

如要進一步瞭解 BigQuery ML 費用，請參閱「[BigQuery ML 定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#bqml)」。

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

建立資料表，用於訓練及評估模型。這份資料表結合了 `bigquery-public-data.iowa_liquor_sales.sales` 和 `bigquery-public-data.covid19_weathersource_com.postal_code_day_history` 資料表的資料欄，用於分析天氣如何影響酒類商店訂購的商品類型和數量。您也可以建立下列額外資料欄，做為模型的輸入變數：

* `date`：訂單日期
* `store_number`：下單商店的專屬編號
* `item_number`：訂購商品的專屬編號
* `bottles_sold`：相關商品的訂購瓶數
* `temperature`：訂單日期當天，商店地點的平均溫度
* `humidity`：訂單日期當天，商店地點的平均濕度

請按照下列步驟建立輸入資料表：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中貼上以下查詢，然後點選「執行」：

   ```
   CREATE OR REPLACE TABLE
     `bqml_tutorial.iowa_liquor_sales_with_weather` AS
   WITH
     sales AS (
       SELECT
         DATE,
         store_number,
         item_number,
         bottles_sold,
         SAFE_CAST(SAFE_CAST(zip_code AS FLOAT64) AS INT64) AS zip_code
       FROM
         `bigquery-public-data.iowa_liquor_sales.sales` AS sales
       WHERE
         SAFE_CAST(zip_code AS FLOAT64) IS NOT NULL
     ),
     aggregated_sales AS (
       SELECT
         DATE,
         store_number,
         item_number,
         ANY_VALUE(zip_code) AS zip_code,
         SUM(bottles_sold) AS bottles_sold,
       FROM
         sales
       GROUP BY
         DATE,
         store_number,
         item_number
     ),
     weather AS (
       SELECT
         DATE,
         SAFE_CAST(postal_code AS INT64) AS zip_code,
         avg_temperature_air_2m_f AS temperature,
         avg_humidity_specific_2m_gpkg AS humidity,
       FROM
         `bigquery-public-data.covid19_weathersource_com.postal_code_day_history`
       WHERE
         country = 'US' AND
         SAFE_CAST(postal_code AS INT64) IS NOT NULL
     )
   SELECT
     aggregated_sales.date,
     aggregated_sales.store_number,
     aggregated_sales.item_number,
     aggregated_sales.bottles_sold,
     weather.temperature AS temperature,
     weather.humidity AS humidity
   FROM
     aggregated_sales
     LEFT JOIN weather ON aggregated_sales.zip_code=weather.zip_code
     AND aggregated_sales.DATE=weather.DATE;
   ```

## 建立時間序列模型

建立時間序列模型，預測 2022 年 9 月 1 日前，`bqml_tutorial.iowa_liquor_sales_with_weather` 資料表中每個日期，各商店 ID 和項目 ID 組合的酒瓶銷售量。使用商店位置在各日期的平均溫度和濕度，做為預測期間要評估的特徵。`bqml_tutorial.iowa_liquor_sales_with_weather` 資料表中的商品編號和商店編號有大約 100 萬種不重複組合，也就是說，有 100 萬個不同的時間序列需要預測。

請按照下列步驟建立模型：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中貼上以下查詢，然後點選「執行」：

   ```
   CREATE
   OR REPLACE MODEL `bqml_tutorial.multi_time_series_arimax_model`
   OPTIONS(
     model_type = 'ARIMA_PLUS_XREG',
     time_series_id_col = ['store_number', 'item_number'],
     time_series_data_col = 'bottles_sold',
     time_series_timestamp_col = 'date'
   )
   AS SELECT
     *
   FROM
     `bqml_tutorial.iowa_liquor_sales_with_weather`
   WHERE
     DATE < DATE('2022-09-01');
   ```

   查詢約需 38 分鐘才能完成，完成後即可存取 `multi_time_series_arimax_model` 模型。由於查詢使用 `CREATE MODEL` 陳述式建立模型，因此不會顯示查詢結果。

## 使用模型預測資料

使用 `ML.FORECAST` 函式預測未來時間序列值。

在下列 GoogleSQL 查詢中，`STRUCT(5 AS horizon, 0.8 AS confidence_level)` 子句表示查詢會預測 5 個未來時間點，並產生信賴水準為 80% 的預測區間。

`ML.FORECAST` 函式的輸入資料簽章，與您用來建立模型的訓練資料簽章相同。輸入內容不含 `bottles_sold` 欄，因為這是模型要預測的資料。

請按照下列步驟，使用模型預測資料：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中貼上以下查詢，然後點選「執行」：

   ```
   SELECT
     *
   FROM
     ML.FORECAST (
       model `bqml_tutorial.multi_time_series_arimax_model`,
       STRUCT (5 AS horizon, 0.8 AS confidence_level),
       (
         SELECT
           * EXCEPT (bottles_sold)
         FROM
           `bqml_tutorial.iowa_liquor_sales_with_weather`
         WHERE
           DATE>=DATE('2022-09-01')
       )
     );
   ```

   結果應大致如下：

   輸出資料列會依 `store_number` 值排序，接著依 `item_ID` 值排序，然後依 `forecast_timestamp` 欄值的時間順序排序。在時間序列預測中，`prediction_interval_lower_bound` 和 `prediction_interval_upper_bound` 欄值代表的預測間隔，與 `forecast_value` 欄值一樣重要。`forecast_value` 值是預測區間的中間點。預測間隔取決於 `standard_error` 和 `confidence_level` 欄的值。

   如要進一步瞭解輸出資料欄，請參閱 [`ML.FORECAST`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-forecast?hl=zh-tw)。

## 說明預測結果

除了預測資料外，您也可以使用 `ML.EXPLAIN_FORECAST` 函式取得可解釋性指標。`ML.EXPLAIN_FORECAST` 函式會預測未來時間序列值，並傳回時間序列的所有個別元件。

與 `ML.FORECAST` 函式類似，`ML.EXPLAIN_FORECAST` 函式中使用的 `STRUCT(5 AS horizon, 0.8 AS confidence_level)` 子句表示查詢會預測 30 個未來時間點，並產生信賴水準為 80% 的預測區間。

`ML.EXPLAIN_FORECAST` 函式會提供歷來資料和預測資料。如要只查看預測資料，請在查詢中加入 `time_series_type` 選項，並將選項值指定為 `forecast`。

請按照下列步驟說明模型結果：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中貼上以下查詢，然後點選「執行」：

   ```
   SELECT
     *
   FROM
     ML.EXPLAIN_FORECAST (
       model `bqml_tutorial.multi_time_series_arimax_model`,
       STRUCT (5 AS horizon, 0.8 AS confidence_level),
       (
         SELECT
           * EXCEPT (bottles_sold)
         FROM
           `bqml_tutorial.iowa_liquor_sales_with_weather`
         WHERE
           DATE >= DATE('2022-09-01')
       )
     );
   ```

   結果應大致如下：

   輸出資料列會依 `time_series_timestamp` 欄值按時間順序排列。

   如要進一步瞭解輸出資料欄，請參閱 [`ML.EXPLAIN_FORECAST`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-explain-forecast?hl=zh-tw)。

## 評估預測準確度

在模型未經訓練的資料上執行模型，評估模型的預測準確度。方法是使用 `ML.EVALUATE` 函式。`ML.EVALUATE` 函式會獨立評估每個時間序列。

在下列 GoogleSQL 查詢中，第二個 `SELECT` 陳述式會提供具有未來特徵的資料，用於預測未來值，以便與實際資料進行比較。

請按照下列步驟評估模型準確率：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中貼上以下查詢，然後點選「執行」：

   ```
   SELECT
     *
   FROM
     ML.EVALUATE (
       model `bqml_tutorial.multi_time_series_arimax_model`,
       (
         SELECT
           *
         FROM
          `bqml_tutorial.iowa_liquor_sales_with_weather`
         WHERE
           DATE >= DATE('2022-09-01')
       )
     );
   ```

   結果應大致如下：

   如要進一步瞭解輸出資料欄，請參閱 [`ML.EVALUATE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-evaluate?hl=zh-tw)。

## 使用模型偵測異常狀況

使用 `ML.DETECT_ANOMALIES` 函式偵測訓練資料中的異常狀況。

在下列查詢中，`STRUCT(0.95 AS anomaly_prob_threshold)` 子句會使 `ML.DETECT_ANOMALIES` 函式以 95% 的信賴水準找出異常資料點。

請按照下列步驟偵測訓練資料中的異常狀況：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中貼上以下查詢，然後點選「執行」：

   ```
   SELECT
     *
   FROM
     ML.DETECT_ANOMALIES (
       model `bqml_tutorial.multi_time_series_arimax_model`,
       STRUCT (0.95 AS anomaly_prob_threshold)
     );
   ```

   結果應大致如下：

   結果中的 `anomaly_probability` 欄會指出特定 `bottles_sold` 欄值為異常值的可能性。

   如要進一步瞭解輸出資料欄，請參閱 [`ML.DETECT_ANOMALIES`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-detect-anomalies?hl=zh-tw)。

### 偵測新資料中的異常狀況

將輸入資料提供給 `ML.DETECT_ANOMALIES` 函式，偵測新資料中的異常狀況。新資料必須與訓練資料具有相同的資料簽章。

請按照下列步驟偵測新資料中的異常狀況：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中貼上以下查詢，然後點選「執行」：

   ```
   SELECT
     *
   FROM
     ML.DETECT_ANOMALIES (
       model `bqml_tutorial.multi_time_series_arimax_model`,
       STRUCT (0.95 AS anomaly_prob_threshold),
       (
         SELECT
           *
         FROM
           `bqml_tutorial.iowa_liquor_sales_with_weather`
         WHERE
           DATE >= DATE('2022-09-01')
       )
     );
   ```

   結果應大致如下：

## 清除所用資源

為避免因為本教學課程所用資源，導致系統向 Google Cloud 帳戶收取費用，請刪除含有相關資源的專案，或者保留專案但刪除個別資源。

* 您可以刪除建立的專案。
* 或者您可以保留專案並刪除資料集。

### 刪除資料集

刪除專案將移除專案中所有的資料集與資料表。若您希望重新使用專案，您可以刪除本教學課程中所建立的資料集。

1. 如有需要，請在Google Cloud 控制台開啟 BigQuery 頁面。

   [前往「BigQuery」頁面](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在導覽窗格中，按一下您建立的 **bqml\_tutorial** 資料集。
3. 按一下視窗右側的「刪除資料集」。這個動作將會刪除資料集、資料表，以及所有資料。
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
* 瞭解如何[使用單變數模型預測多個時間序列](https://docs.cloud.google.com/bigquery/docs/arima-multiple-time-series-forecasting-tutorial?hl=zh-tw)
* 瞭解如何[在預測多個資料列的多個時間序列時，擴充單變數模型](https://docs.cloud.google.com/bigquery/docs/arima-speed-up-tutorial?hl=zh-tw)。
* 瞭解如何[使用單變數模型，以階層方式預測多個時間序列](https://docs.cloud.google.com/bigquery/docs/arima-time-series-forecasting-with-hierarchical-time-series?hl=zh-tw)
* 如要瞭解 BigQuery ML，請參閱「[BigQuery AI 和機器學習簡介](https://docs.cloud.google.com/bigquery/docs/bqml-introduction?hl=zh-tw)」。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-11-11 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-11-11 (世界標準時間)。"],[],[]]