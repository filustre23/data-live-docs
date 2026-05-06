Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 使用多變數時間序列預測模型執行異常偵測

本教學課程說明如何執行下列工作：

* 建立[`ARIMA_PLUS_XREG`時間序列預測模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-multivariate-time-series?hl=zh-tw)。
* 對模型執行 [`ML.DETECT_ANOMALIES` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-detect-anomalies?hl=zh-tw)，偵測時間序列資料中的異常狀況。

本教學課程會使用公開 `epa_historical_air_quality` 資料集中的下列資料表，其中包含從美國多個城市收集的每日 PM 2.5、溫度和風速資訊：

* [`epa_historical_air_quality.pm25_nonfrm_daily_summary`](https://console.cloud.google.com/bigquery?p=bigquery-public-data&%3Bd=epa_historical_air_quality&%3Bt=pm25_nonfrm_daily_summary&%3Bpage=table&hl=zh-tw)
* [`epa_historical_air_quality.wind_daily_summary`](https://console.cloud.google.com/bigquery?p=bigquery-public-data&%3Bd=epa_historical_air_quality&%3Bt=wind_daily_summary&%3Bpage=table&hl=zh-tw)
* [`epa_historical_air_quality.temperature_daily_summary`](https://console.cloud.google.com/bigquery?p=bigquery-public-data&%3Bd=epa_historical_air_quality&%3Bt=temperature_daily_summary&%3Bpage=table&hl=zh-tw)

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

## 費用

在本文件中，您會使用下列 Google Cloud的計費元件：

* **BigQuery:** You incur costs for the data you
  process in BigQuery.

如要根據預測用量估算費用，請使用 [Pricing Calculator](https://docs.cloud.google.com/products/calculator?hl=zh-tw)。

初次使用 Google Cloud 的使用者可能符合[免費試用期](https://docs.cloud.google.com/free?hl=zh-tw)資格。

詳情請參閱「[BigQuery 定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw)」一文。

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

  [Enable the API](https://console.cloud.google.com/flows/enableapi?apiid=bigquery.googleapis.com&hl=zh-tw)

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

  [Enable the API](https://console.cloud.google.com/flows/enableapi?apiid=bigquery.googleapis.com&hl=zh-tw)

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

## 準備訓練資料

PM2.5、溫度和風速資料分別位於不同表格。結合這些公開資料表中的資料，建立訓練資料的 `bqml_tutorial.seattle_air_quality_daily` 資料表。`bqml_tutorial.seattle_air_quality_daily` 包含下列資料欄：

* `date`：觀察日期
* `PM2.5`：每天的平均 PM2.5 值
* `wind_speed`：每天的平均風速
* `temperature`：每天的最高溫

新資料表包含 2009 年 8 月 11 日至 2022 年 1 月 31 日的每日資料。

1. 前往「BigQuery」頁面

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在 SQL 編輯器窗格中，執行下列 SQL 陳述式：

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
   JOIN temperature_daily USING (date)
   ```

## 建立模型

使用 `bqml_tutorial.seattle_air_quality_daily` 中的資料做為訓練資料，建立多元時間序列模型。

1. 前往「BigQuery」頁面

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在 SQL 編輯器窗格中，執行下列 SQL 陳述式：

   ```
   CREATE OR REPLACE MODEL `bqml_tutorial.arimax_model`
     OPTIONS (
       model_type = 'ARIMA_PLUS_XREG',
       auto_arima=TRUE,
       time_series_data_col = 'temperature',
       time_series_timestamp_col = 'date'
       )
   AS
   SELECT
     *
   FROM
     `bqml_tutorial.seattle_air_quality_daily`
   WHERE
     date < "2023-02-01";
   ```

   查詢作業會在幾秒內完成，之後模型 `arimax_model` 會顯示在 `bqml_tutorial` 資料集中，並可在「Explorer」窗格中存取。

   由於查詢是使用 `CREATE MODEL` 陳述式建立模型，因此不會有查詢結果。

## 對歷來資料執行異常偵測

針對用於訓練模型的歷來資料執行異常偵測。

1. 前往「BigQuery」頁面

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在 SQL 編輯器窗格中，執行下列 SQL 陳述式：

   ```
   SELECT
     *
   FROM
     ML.DETECT_ANOMALIES (
      MODEL `bqml_tutorial.arimax_model`,
      STRUCT(0.6 AS anomaly_prob_threshold)
     )
   ORDER BY
     date ASC;
   ```

   結果類似下方：

   ```
   +-------------------------+-------------+------------+--------------------+--------------------+---------------------+
   | date                    | temperature | is_anomaly | lower_bound        | upper_bound        | anomaly_probability |
   +--------------------------------------------------------------------------------------------------------------------+
   | 2009-08-11 00:00:00 UTC | 70.1        | false      | 67.647370742988727 | 72.552629257011262 | 0                   |
   +--------------------------------------------------------------------------------------------------------------------+
   | 2009-08-12 00:00:00 UTC | 73.4        | false      | 71.7035428351283   | 76.608801349150838 | 0.20478819992561115 |
   +--------------------------------------------------------------------------------------------------------------------+
   | 2009-08-13 00:00:00 UTC | 64.6        | true       | 67.740408724826068 | 72.6456672388486   | 0.945588334903206   |
   +-------------------------+-------------+------------+--------------------+--------------------+---------------------+
   ```

## 對新資料執行異常偵測

對您產生新資料執行異常偵測。

1. 前往「BigQuery」頁面

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在 SQL 編輯器窗格中，執行下列 SQL 陳述式：

   ```
   SELECT
     *
   FROM
     ML.DETECT_ANOMALIES (
      MODEL `bqml_tutorial.arimax_model`,
      STRUCT(0.6 AS anomaly_prob_threshold),
      (
        SELECT
          *
        FROM
          UNNEST(
            [
              STRUCT<date TIMESTAMP, pm25 FLOAT64, wind_speed FLOAT64, temperature FLOAT64>
              ('2023-02-01 00:00:00 UTC', 8.8166665, 1.6525, 44.0),
              ('2023-02-02 00:00:00 UTC', 11.8354165, 1.558333, 40.5),
              ('2023-02-03 00:00:00 UTC', 10.1395835, 1.6895835, 46.5),
              ('2023-02-04 00:00:00 UTC', 11.439583500000001, 2.0854165, 45.0),
              ('2023-02-05 00:00:00 UTC', 9.7208335, 1.7083335, 46.0),
              ('2023-02-06 00:00:00 UTC', 13.3020835, 2.23125, 43.5),
              ('2023-02-07 00:00:00 UTC', 5.7229165, 2.377083, 47.5),
              ('2023-02-08 00:00:00 UTC', 7.6291665, 2.24375, 44.5),
              ('2023-02-09 00:00:00 UTC', 8.5208335, 2.2541665, 40.5),
              ('2023-02-10 00:00:00 UTC', 9.9086955, 7.333335, 39.5)
            ]
          )
        )
      );
   ```

   結果類似下方：

   ```
   +-------------------------+-------------+------------+--------------------+--------------------+---------------------+------------+------------+
   | date                    | temperature | is_anomaly | lower_bound        | upper_bound        | anomaly_probability | pm25       | wind_speed |
   +----------------------------------------------------------------------------------------------------------------------------------------------+
   | 2023-02-01 00:00:00 UTC | 44.0        | true       | 36.89918003713138  | 41.8044385511539   | 0.88975675709801583 | 8.8166665  | 1.6525     |
   +----------------------------------------------------------------------------------------------------------------------------------------------+
   | 2023-02-02 00:00:00 UTC | 40.5        | false      | 34.439946284051572 | 40.672021330796483 | 0.57358239699845348 | 11.8354165 | 1.558333   |
   +--------------------------------------------------------------------------------------------------------------------+-------------------------+
   | 2023-02-03 00:00:00 UTC | 46.5        | true       | 33.615139992931191 | 40.501364463964549 | 0.97902867696346974 | 10.1395835 | 1.6895835  |
   +-------------------------+-------------+------------+--------------------+--------------------+---------------------+-------------------------+
   ```

## 清除所用資源

**注意**：刪除專案會造成以下結果：

* **專案中的所有內容都會遭到刪除。**如果使用現有專案來進行本文中的任務，刪除專案將一併移除當中已完成的其他任務'。
* **自訂專案 ID 會消失。**當您之前建立這個專案時，可能建立了想要在日後使用的自訂專案 ID。如要保留使用該專案 ID 的網址 (例如 `appspot.com` 網址)，請刪除在該專案中選取的資源，而不是刪除整個專案。

如果打算探索多種架構、教學課程或快速入門導覽課程，重複使用專案可避免超出專案配額限制。

1. 前往 Google Cloud 控制台的「Manage resources」(管理資源) 頁面。

   [前往「Manage resources」(管理資源)](https://console.cloud.google.com/iam-admin/projects?hl=zh-tw)
2. 在專案清單中選取要刪除的專案，然後點選「Delete」(刪除)。
3. 在對話方塊中輸入專案 ID，然後按一下 [Shut down] (關閉) 以刪除專案。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-06 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-06 (世界標準時間)。"],[],[]]