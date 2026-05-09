Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 使用 ARIMA\_PLUS 單變數模型預測階層式時間序列

本教學課程說明如何使用[`ARIMA_PLUS`單變數時間序列模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-time-series?hl=zh-tw)預測階層式時間序列。這項功能會根據指定資料欄的歷史值，預測該資料欄的未來值，並計算該資料欄中一或多個感興趣維度的綜覽值。

系統會針對每個時間點，以及一或多個指定感興趣維度的資料欄中的每個值，計算預測值。舉例來說，如果您想預測每日交通事件，並指定包含州別資料的維度資料欄，預測資料會包含州別 A 每天的值，然後是州別 B 每天的值，依此類推。如果您想預測每日交通事件，並指定包含州和城市資料的維度資料欄，預測資料會包含 A 州和 A 市每天的值，然後是 A 州和 B 市每天的值，依此類推。在階層式時間序列模型中，[階層式對帳](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-time-series?hl=zh-tw#hierarchical_reconciliation)用於匯總每個子項時間序列，並與其父項對帳。舉例來說，A 州所有城市的預測值總和，必須等於 A 州的預測值。

在本教學課程中，您將使用相同資料建立兩個時間序列模型，一個使用階層式預測，另一個則否。這項功能可讓您比較模型傳回的結果。

[本教學課程使用公開資料表中的資料。](https://console.cloud.google.com/bigquery?p=bigquery-public-data&%3Bd=iowa_liquor_sales&%3Bt=sales&%3Bpage=table&hl=zh-tw)`bigquery-public-data.iowa_liquor.sales.sales`這份表格包含愛荷華州公開酒類銷售資料，內有不同商店超過 100 萬種酒類產品的資訊。

閱讀本教學課程前，強烈建議您先參閱「[使用單變數模型預測多個時間序列](https://docs.cloud.google.com/bigquery/docs/arima-single-time-series-forecasting-tutorial?hl=zh-tw)」。

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

## 目標

在本教學課程中，您會使用下列項目：

* 使用 [`CREATE MODEL` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-multivariate-time-series?hl=zh-tw)，建立多個時間序列模型和多個階層式時間序列模型，預測瓶裝飲料的銷售值。
* 使用 [`ML.FORECAST` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-forecast?hl=zh-tw)，從模型中擷取預測的瓶裝水銷售值。

## 費用

本教學課程使用 Google Cloud的計費元件，包括：

* BigQuery
* BigQuery ML

如要進一步瞭解 BigQuery 費用，請參閱 [BigQuery 定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw)頁面。

如要進一步瞭解 BigQuery ML 費用，請參閱 [BigQuery ML 定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#bqml)。

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

## 建立時間序列模型

使用愛荷華州酒類銷售資料建立時間序列模型。

下列 GoogleSQL 查詢會建立模型，預測 2015 年在 Polk、Linn 和 Scott 郡售出的瓶裝水總數。

在下列查詢中，`OPTIONS(model_type='ARIMA_PLUS', time_series_timestamp_col='date', ...)` 子句表示您要建立以 [ARIMA](https://en.wikipedia.org/wiki/Autoregressive_integrated_moving_average) 為基礎的時間序列模型。您可以使用 `CREATE MODEL` 陳述式的 [`TIME_SERIES_ID` 選項](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-time-series?hl=zh-tw#time_series_id_col)，指定要取得預測結果的輸入資料中一或多個資料欄。`CREATE MODEL` 陳述式的 [`auto_arima_max_order` 選項](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-time-series?hl=zh-tw#auto_arima_max_order)會控管 `auto.ARIMA` 演算法中超參數調整的搜尋空間。`CREATE MODEL` 陳述式的 [`decompose_time_series` 選項](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-time-series?hl=zh-tw#decompose_time_series)預設為 `TRUE`，因此在下一個步驟中評估模型時，系統會傳回時間序列資料的相關資訊。

`OPTIONS(model_type='ARIMA_PLUS', time_series_timestamp_col='date', ...)` 子句代表您要建立以 [ARIMA](https://en.wikipedia.org/wiki/Autoregressive_integrated_moving_average) 為基礎的時間序列模型。根據預設，[`auto_arima=TRUE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-time-series?hl=zh-tw#auto_arima)，因此 `auto.ARIMA` 演算法會自動調整 `ARIMA_PLUS` 模型中的超參數。演算法會套用數十個候選模型，並選擇最佳模型，也就是[赤池訊息量準則 (AIC)](https://en.wikipedia.org/wiki/Akaike_information_criterion) 最低的模型。如果時間序列中存在美國節慶模式，將 [`holiday_region` 選項](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-time-series?hl=zh-tw#holiday_region)設為 `US`，即可更準確地模擬這些美國節慶時間點。

請按照下列步驟建立模型：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中貼入下列查詢，然後點選「執行」：

   ```
   CREATE OR REPLACE MODEL `bqml_tutorial.liquor_forecast`
     OPTIONS (
       MODEL_TYPE = 'ARIMA_PLUS',
       TIME_SERIES_TIMESTAMP_COL = 'date',
       TIME_SERIES_DATA_COL = 'total_bottles_sold',
       TIME_SERIES_ID_COL = ['store_number', 'zip_code', 'city', 'county'],
       HOLIDAY_REGION = 'US')
   AS
   SELECT
     store_number,
     zip_code,
     city,
     county,
     date,
     SUM(bottles_sold) AS total_bottles_sold
   FROM
     `bigquery-public-data.iowa_liquor_sales.sales`
   WHERE
     date BETWEEN DATE('2015-01-01') AND DATE('2015-12-31')
     AND county IN ('POLK', 'LINN', 'SCOTT')
   GROUP BY store_number, date, city, zip_code, county;
   ```

   查詢約需 37 秒才能完成，完成後即可存取 `liquor_forecast` 模型。由於查詢是使用 `CREATE MODEL` 陳述式建立模型，因此不會有查詢結果。

## 使用模型預測資料

使用 `ML.FORECAST` 函式預測未來時間序列值。

在下列查詢中，`STRUCT(20 AS horizon, 0.8 AS confidence_level)` 子句表示查詢會預測 20 個未來時間點，並產生信賴水準為 80% 的預測間隔。

如要使用模型預測資料，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中貼入下列查詢，然後點選「執行」：

   ```
   SELECT *
   FROM
     ML.FORECAST(
       MODEL `bqml_tutorial.liquor_forecast`,
       STRUCT(20 AS horizon, 0.8 AS confidence_level))
   ORDER BY store_number, county, city, zip_code, forecast_timestamp;
   ```

   結果應如下所示：

   輸出內容會先顯示第一個時間序列的預測資料；`store_number=2190`、`zip_code=50314`、`city=DES MOINES`、`county=POLK`。捲動瀏覽資料時，您會看到每個後續不重複時間序列的預測結果。如要產生不同維度的總計預測，例如特定縣市的預測，您必須產生階層式預測。

## 建立階層式時間序列模型

使用愛荷華州酒類銷售資料，建立階層式時間序列預測。

下列 GoogleSQL 查詢會建立模型，針對 Polk、Linn 和 Scott 郡 2015 年的每日總瓶裝水銷量，生成階層式預測。

在下列查詢中，`CREATE MODEL` 陳述式中的 `HIERARCHICAL_TIME_SERIES_COLS` 選項表示您要根據指定的一組資料欄建立階層式預測。這些資料欄都會經過彙整和匯總。舉例來說，在先前的查詢中，這表示 `store_number` 資料欄值會匯總，以顯示每個 `county`、`city` 和 `zip_code` 值的預測結果。此外，`zip_code` 和 `store_number` 值也會分別匯總，顯示每個 `county` 和 `city` 值的預測結果。欄的順序很重要，因為這會定義階層的結構。

請按照下列步驟建立模型：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中貼入下列查詢，然後點選「執行」：

   ```
   CREATE OR REPLACE MODEL `bqml_tutorial.liquor_forecast_hierarchical`
     OPTIONS (
       MODEL_TYPE = 'ARIMA_PLUS',
       TIME_SERIES_TIMESTAMP_COL = 'date',
       TIME_SERIES_DATA_COL = 'total_bottles_sold',
       TIME_SERIES_ID_COL = ['store_number', 'zip_code', 'city', 'county'],
       HIERARCHICAL_TIME_SERIES_COLS = ['zip_code', 'store_number'],
       HOLIDAY_REGION = 'US')
   AS
   SELECT
     store_number,
     zip_code,
     city,
     county,
     date,
     SUM(bottles_sold) AS total_bottles_sold
   FROM
     `bigquery-public-data.iowa_liquor_sales.sales`
   WHERE
     date BETWEEN DATE('2015-01-01') AND DATE('2015-12-31')
     AND county IN ('POLK', 'LINN', 'SCOTT')
   GROUP BY store_number, date, city, zip_code, county;
   ```

   查詢作業約需 45 秒才能完成，完成後即可在「Explorer」窗格中存取 `bqml_tutorial.liquor_forecast_hierarchical` 模型。由於查詢是使用 `CREATE MODEL` 陳述式建立模型，因此不會有查詢結果。

## 使用階層式模型預測資料

使用 `ML.FORECAST` 函式從模型擷取階層式預測資料。

如要使用模型預測資料，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中貼入下列查詢，然後點選「執行」：

   ```
   SELECT
     *
   FROM
     ML.FORECAST(
       MODEL `bqml_tutorial.liquor_forecast_hierarchical`,
       STRUCT(30 AS horizon, 0.8 AS confidence_level))
   WHERE city = 'LECLAIRE'
   ORDER BY county, city, zip_code, store_number, forecast_timestamp;
   ```

   結果應如下所示：

   請注意，系統會顯示 LeClaire 市的匯總預測，`store_number=NULL`、`zip_code=NULL`、`city=LECLAIRE`、`county=SCOTT`。查看其餘資料列時，請注意其他子群組的預測結果。舉例來說，下圖顯示郵遞區號 `52753`、`store_number=NULL`、`zip_code=52753`、`city=LECLAIRE`、`county=SCOTT` 的匯總預報：

## 清除所用資源

如要避免系統向您的 Google Cloud 帳戶收取本教學課程所用資源的費用，請刪除含有相關資源的專案，或者保留專案但刪除個別資源。

* 您可以刪除建立的專案。
* 或者您可以保留專案並刪除資料集。

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

* 瞭解如何[使用單變數模型預測單一時間序列](https://docs.cloud.google.com/bigquery/docs/arima-single-time-series-forecasting-tutorial?hl=zh-tw)
* 瞭解如何[使用單變數模型預測多個時間序列](https://docs.cloud.google.com/bigquery/docs/arima-multiple-time-series-forecasting-tutorial?hl=zh-tw)
* 瞭解如何[在預測多個資料列的時間序列時，擴充單變數模型](https://docs.cloud.google.com/bigquery/docs/arima-speed-up-tutorial?hl=zh-tw)。
* 瞭解如何[使用多變數模型預測單一時間序列](https://docs.cloud.google.com/bigquery/docs/arima-plus-xreg-single-time-series-forecasting-tutorial?hl=zh-tw)
* 如需 BigQuery ML 的總覽，請參閱 [BigQuery 中的 AI 和 ML 簡介](https://docs.cloud.google.com/bigquery/docs/bqml-introduction?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-09 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-09 (世界標準時間)。"],[],[]]