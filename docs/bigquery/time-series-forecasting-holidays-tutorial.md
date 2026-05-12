Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 在 ARIMA\_PLUS 時間序列預測模型中使用自訂節慶假日

本教學課程說明如何執行下列工作：

* 建立僅使用內建節慶的[`ARIMA_PLUS`時間序列預測模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-time-series?hl=zh-tw)。
* 建立 `ARIMA_PLUS` 時間序列預測模型，除了內建節慶外，還使用自訂節慶。
* 以視覺化方式呈現這些模型的預測結果。
* 檢查模型，瞭解模型模擬的節慶。
* 評估自訂節日對預測結果的影響。
* 比較只使用內建節慶的模型成效，以及除了內建節慶外還使用自訂節慶的模型成效。

本教學課程使用 `bigquery-public-data.wikipedia.pageviews_*` 公開資料表。

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

## 準備時間序列資料

將「Google I/O」網頁的維基百科網頁瀏覽資料匯總到單一表格中，並依日期分組：

1. 前往「BigQuery」頁面

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在 SQL 編輯器窗格中，執行下列 SQL 陳述式：

   ```
   CREATE OR REPLACE TABLE `bqml_tutorial.googleio_page_views`
   AS
   SELECT
     DATETIME_TRUNC(datehour, DAY) AS date,
     SUM(views) AS views
   FROM
     `bigquery-public-data.wikipedia.pageviews_*`
   WHERE
     datehour >= '2017-01-01'
     AND datehour < '2023-01-01'
     AND title = 'Google_I/O'
   GROUP BY
     DATETIME_TRUNC(datehour, DAY)
   ```

## 建立使用內建節慶的預測模型

根據 2022 年前的網頁瀏覽資料，並考量內建的節慶假日，建立模型來預測 Wikipedia「Google I/O」網頁的每日瀏覽量：

1. 前往「BigQuery」頁面

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在 SQL 編輯器窗格中，執行下列 SQL 陳述式：

   ```
   CREATE OR REPLACE MODEL `bqml_tutorial.forecast_googleio`
     OPTIONS (
       model_type = 'ARIMA_PLUS',
       holiday_region = 'US',
       time_series_timestamp_col = 'date',
       time_series_data_col = 'views',
       data_frequency = 'DAILY',
       horizon = 365)
   AS
   SELECT
     *
   FROM
     `bqml_tutorial.googleio_page_views`
   WHERE
     date < '2022-01-01';
   ```

## 以圖表呈現預測結果

使用內建節慶建立模型後，請將 `bqml_tutorial.googleio_page_views` 資料表中的原始資料與 [`ML.EXPLAIN_FORECAST` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-explain-forecast?hl=zh-tw)的預測值合併，然後[使用數據分析](https://docs.cloud.google.com/bigquery/docs/visualize-looker-studio?hl=zh-tw)以視覺化方式呈現：

1. 前往「BigQuery」頁面

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在 SQL 編輯器窗格中，執行下列 SQL 陳述式：

   ```
   SELECT
     original.date,
     original.views AS original_views,
     explain_forecast.time_series_adjusted_data
       AS adjusted_views_without_custom_holiday,
   FROM
     `bqml_tutorial.googleio_page_views` original
   INNER JOIN
     (
       SELECT
         *
       FROM
         ML.EXPLAIN_FORECAST(
           MODEL `bqml_tutorial.forecast_googleio`,
           STRUCT(365 AS horizon))
     ) explain_forecast
     ON
       TIMESTAMP(original.date)
       = explain_forecast.time_series_timestamp
   ORDER BY
     original.date;
   ```
3. 在「查詢結果」窗格中，依序點選「開啟方式」>「數據分析」。系統會在新的分頁中開啟 數據分析。
4. 在數據分析分頁中，按一下 **新增圖表**，然後點選時間序列圖表：

   將圖表放到報表上。
5. ****在「圖表」窗格的「設定」分頁中，按一下「新增指標」並選取「adjusted\_views\_without\_custom\_holiday」：****

   圖表看起來類似如下：

   您可以看到預測模型相當準確地掌握了整體趨勢。不過，這項工具無法擷取與先前 Google I/O 活動相關的流量增加情形，也無法為

   1. 接下來的章節將說明如何因應部分限制。

## 建立使用內建和自訂節慶假日的時間序列預測模型

如[Google I/O 歷史記錄](https://en.wikipedia.org/wiki/Google_I/O#History)所示，2017 年至 2022 年的 Google I/O 大會舉辦日期不盡相同。如要將這項變異納入考量，請根據 2022 年前的網頁瀏覽資料建立模型，預測 Wikipedia「Google\_I/O」網頁在 2022 年的網頁瀏覽次數，並使用自訂節慶代表每年的 Google I/O 活動。在這個模型中，您也會調整節慶效應時間範圍，涵蓋活動日期前後三天，以便更完整地擷取活動前後的潛在網頁流量。

1. 前往「BigQuery」頁面

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在 SQL 編輯器窗格中，執行下列 SQL 陳述式：

   ```
   CREATE OR REPLACE MODEL `bqml_tutorial.forecast_googleio_with_custom_holiday`
     OPTIONS (
       model_type = 'ARIMA_PLUS',
       holiday_region = 'US',
       time_series_timestamp_col = 'date',
       time_series_data_col = 'views',
       data_frequency = 'DAILY',
       horizon = 365)
   AS (
     training_data AS (
         SELECT
           *
         FROM
           `bqml_tutorial.googleio_page_views`
         WHERE
           date < '2022-01-01'
       ),
     custom_holiday AS (
         SELECT
           'US' AS region,
           'GoogleIO' AS holiday_name,
           primary_date,
           1 AS preholiday_days,
           2 AS postholiday_days
         FROM
           UNNEST(
             [
               DATE('2017-05-17'),
               DATE('2018-05-08'),
               DATE('2019-05-07'),
               -- cancelled in 2020 due to pandemic
               DATE('2021-05-18'),
               DATE('2022-05-11')])
             AS primary_date
       )
   );
   ```

## 以圖表呈現預測結果

使用自訂節慶建立模型後，請將 `bqml_tutorial.googleio_page_views` 資料表中的原始資料與 [`ML.EXPLAIN_FORECAST` 函式中的預測值合併](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-explain-forecast?hl=zh-tw)，然後[使用數據分析](https://docs.cloud.google.com/bigquery/docs/visualize-looker-studio?hl=zh-tw)以視覺化方式呈現：

1. 前往「BigQuery」頁面

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在 SQL 編輯器窗格中，執行下列 SQL 陳述式：

   ```
   SELECT
     original.date,
     original.views AS original_views,
     explain_forecast.time_series_adjusted_data
       AS adjusted_views_with_custom_holiday,
   FROM
     `bqml_tutorial.googleio_page_views` original
   INNER JOIN
     (
       SELECT
         *
       FROM
         ML.EXPLAIN_FORECAST(
           MODEL
             `bqml_tutorial.forecast_googleio_with_custom_holiday`,
           STRUCT(365 AS horizon))
     ) explain_forecast
     ON
       TIMESTAMP(original.date)
       = explain_forecast.time_series_timestamp
   ORDER BY
     original.date;
   ```
3. 在「查詢結果」窗格中，依序點按「探索資料」和「透過數據分析探索」。系統會在新的分頁中開啟 數據分析。
4. 在數據分析分頁中，依序點選「新增圖表」和時間序列圖表，然後將圖表放在報表上。
5. 在「圖表」窗格的「設定」分頁中，按一下「新增指標」，然後選取「adjusted\_views\_with\_custom\_holiday」。

   圖表看起來類似如下：

   如您所見，自訂節慶活動提升了預測模型的成效。現在可有效擷取 Google I/O 帶來的網頁瀏覽次數增幅。

## 檢查節慶資訊

使用 [`ML.HOLIDAY_INFO` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-holiday-info?hl=zh-tw)，檢查在模型建構期間考量的節日清單：

1. 前往「BigQuery」頁面

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在 SQL 編輯器窗格中，執行下列 SQL 陳述式：

   ```
   SELECT *
   FROM
     ML.HOLIDAY_INFO(
       MODEL `bqml_tutorial.forecast_googleio_with_custom_holiday`);
   ```

   結果會顯示 Google I/O 和內建節慶：

## 評估自訂節日的影響

使用 [`ML.EXPLAIN_FORECAST` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-explain-forecast?hl=zh-tw)，評估自訂節慶對預測結果的影響：

1. 前往「BigQuery」頁面

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在 SQL 編輯器窗格中，執行下列 SQL 陳述式：

   ```
   SELECT
     time_series_timestamp,
     holiday_effect_GoogleIO,
     holiday_effect_US_Juneteenth,
     holiday_effect_Christmas,
     holiday_effect_NewYear
   FROM
     ML.EXPLAIN_FORECAST(
       model
         `bqml_tutorial.forecast_googleio_with_custom_holiday`,
       STRUCT(365 AS horizon))
   WHERE holiday_effect != 0;
   ```

   結果顯示，Google I/O 對預測結果的節慶效應貢獻良多：

## 比較模型效能

使用 [`ML.EVALUATE` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-evaluate?hl=zh-tw)比較第一個模型 (未建立自訂節慶) 和第二個模型 (已建立自訂節慶) 的成效。如要查看第二個模型在預測未來自訂節慶時的成效，請將時間範圍設為 2022 年 Google I/O 大會當週：

1. 前往「BigQuery」頁面

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在 SQL 編輯器窗格中，執行下列 SQL 陳述式：

   ```
   SELECT
     "original" AS model_type,
     *
   FROM
     ml.evaluate(
       MODEL `bqml_tutorial.forecast_googleio`,
       (
         SELECT
           *
         FROM
           `bqml_tutorial.googleio_page_views`
         WHERE
           date >= '2022-05-08'
           AND date < '2022-05-12'
       ),
       STRUCT(
         365 AS horizon,
         TRUE AS perform_aggregation))
   UNION ALL
   SELECT
     "with_custom_holiday" AS model_type,
     *
   FROM
     ml.evaluate(
       MODEL
         `bqml_tutorial.forecast_googleio_with_custom_holiday`,
       (
         SELECT
           *
         FROM
           `bqml_tutorial.googleio_page_views`
         WHERE
           date >= '2022-05-08'
           AND date < '2022-05-12'
       ),
       STRUCT(
         365 AS horizon,
         TRUE AS perform_aggregation));
   ```

   結果顯示，第二個模型可大幅提升效能：

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

上次更新時間：2026-05-12 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-12 (世界標準時間)。"],[],[]]