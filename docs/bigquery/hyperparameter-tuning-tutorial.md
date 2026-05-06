Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見

# 透過超參數調整提升模型效能 透過集合功能整理內容 你可以依據偏好儲存及分類內容。

本教學課程說明如何使用 BigQuery ML 中的[超參數調整](https://docs.cloud.google.com/bigquery/docs/hp-tuning-overview?hl=zh-tw)功能，調整機器學習模型並提升效能。

如要執行超參數調整，請指定 `CREATE MODEL` 陳述式的 [`NUM_TRIALS` 選項](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create?hl=zh-tw#num_trials)，並搭配其他模型專屬選項。設定這些選項後，BigQuery ML 會訓練多個版本的模型 (或稱「試驗」)，每個版本都使用略有不同的參數，並傳回成效最佳的試驗。

本教學課程使用公開的[`tlc_yellow_trips_2018`範例資料表](https://console.cloud.google.com/bigquery?p=bigquery-public-data&%3Bd=new_york_taxi_trips&%3Bt=tlc_yellow_trips_2018&%3Bpage=table&hl=zh-tw)，其中包含 2018 年紐約市的計程車車程資訊。

## 目標

本教學課程會逐步引導您完成下列工作：

* 使用 [`CREATE MODEL` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-glm?hl=zh-tw)建立基準線性迴歸模型。
* 使用 [`ML.EVALUATE` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-evaluate?hl=zh-tw)評估基準模型。
* 使用 `CREATE MODEL` 陳述式搭配超參數調整選項，訓練線性迴歸模型二十次。
* 使用 [`ML.TRIAL_INFO` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-trial-info?hl=zh-tw)查看測試。
* 使用 `ML.EVALUATE` 函式評估試驗。
* 使用 [`ML.PREDICT` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-predict?hl=zh-tw)，從試驗中找出最佳模型，並取得計程車行程的預測結果。

## 費用

本教學課程使用 Google Cloud的計費元件，包括：

* BigQuery
* BigQuery ML

如要進一步瞭解 BigQuery 費用，請參閱 [BigQuery 定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw)頁面。

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

## 建立訓練資料表

根據`tlc_yellow_trips_2018`資料表資料的子集，建立訓練資料表。

請按照下列步驟建立資料表：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中貼入下列查詢，然後點選「執行」：

   ```
   CREATE OR REPLACE TABLE `bqml_tutorial.taxi_tip_input`
   AS
   SELECT * EXCEPT (tip_amount), tip_amount AS label
   FROM
     `bigquery-public-data.new_york_taxi_trips.tlc_yellow_trips_2018`
   WHERE
     tip_amount IS NOT NULL
   LIMIT 100000;
   ```

## 建立基準線性迴歸模型

建立線性迴歸模型，但不進行超參數調整，並在 `taxi_tip_input` 資料表資料上訓練模型。

請按照下列步驟建立模型：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中貼入下列查詢，然後點選「執行」：

   ```
   CREATE OR REPLACE MODEL `bqml_tutorial.baseline_taxi_tip_model`
     OPTIONS (
       MODEL_TYPE = 'LINEAR_REG'
     )
   AS
   SELECT
     *
   FROM
     `bqml_tutorial.taxi_tip_input`;
   ```

   查詢大約需要 2 分鐘才能完成。

## 評估基準模型

使用 `ML.EVALUATE` 函式評估模型效能。
`ML.EVALUATE` 函式會根據模型訓練期間計算的評估指標，評估模型傳回的預測內容分級。

請按照下列步驟評估模型：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中貼入下列查詢，然後點選「執行」：

   ```
   SELECT *
   FROM
     ML.EVALUATE(MODEL `bqml_tutorial.baseline_taxi_tip_model`);
   ```

   結果類似下方：

   ```
   +---------------------+--------------------+------------------------+-----------------------+---------------------+---------------------+
   | mean_absolute_error | mean_squared_error | mean_squared_log_error | median_absolute_error |      r2_score       | explained_variance  |
   +---------------------+--------------------+------------------------+-----------------------+---------------------+---------------------+
   |  2.5853895559690323 | 23760.416358496139 |   0.017392406523370374 | 0.0044248227819481123 | -1934.5450533482465 | -1934.3513857946277 |
   +---------------------+--------------------+------------------------+-----------------------+---------------------+---------------------+
   ```

基準模型的 `r2_score` 值為負數，表示資料不適合使用該模型；[R2 分數](https://en.wikipedia.org/wiki/Coefficient_of_determination)越接近 1，表示模型越適合使用。

## 建立線性迴歸模型並調整超參數

建立線性迴歸模型並調整超參數，然後使用 `taxi_tip_input` 資料表資料訓練模型。

您可以在 `CREATE MODEL` 陳述式中使用下列超參數調整選項：

* 將測試次數設為 20 次。[`NUM_TRIALS`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-glm?hl=zh-tw#num_trials)
* [`MAX_PARALLEL_TRIALS`選項](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-glm?hl=zh-tw#max_parallel_trials)：在每個訓練工作中執行兩項試驗，總共執行十項工作和二十項試驗。這可縮短訓練所需時間。不過，這兩項並行試驗不會互相參考訓練結果。
* [`L1_REG`選項](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-glm?hl=zh-tw#l1_reg)，可在不同試驗中嘗試不同的 L1 正規化值。L1 正則化會從模型中移除不相關的特徵，有助於避免[過度配適](https://developers.google.com/machine-learning/glossary/?hl=zh-tw#overfitting)。

模型支援的其他超參數調整選項會使用預設值，如下所示：

* `L1_REG`：`0`
* `HPARAM_TUNING_ALGORITHM`：`'VIZIER_DEFAULT'`
* `HPARAM_TUNING_OBJECTIVES`：`['R2_SCORE']`

請按照下列步驟建立模型：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中貼入下列查詢，然後點選「執行」：

   ```
   CREATE OR REPLACE MODEL `bqml_tutorial.hp_taxi_tip_model`
     OPTIONS (
       MODEL_TYPE = 'LINEAR_REG',
       NUM_TRIALS = 20,
       MAX_PARALLEL_TRIALS = 2,
       L1_REG = HPARAM_RANGE(0, 5))
   AS
   SELECT
     *
   FROM
     `bqml_tutorial.taxi_tip_input`;
   ```

   查詢約需 20 分鐘才能完成。

## 取得訓練試驗的相關資訊

使用 `ML.TRIAL_INFO` 函式，取得所有試驗的相關資訊，包括超參數值、目標和狀態。這個函式也會根據這項資訊，傳回效能最佳的試驗。

如要查看試用資訊，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中貼入下列查詢，然後點選「執行」：

   ```
   SELECT *
   FROM
     ML.TRIAL_INFO(MODEL `bqml_tutorial.hp_taxi_tip_model`)
   ORDER BY is_optimal DESC;
   ```

   結果類似下方：

   ```
   +----------+-------------------------------------+-----------------------------------+--------------------+--------------------+-----------+---------------+------------+
   | trial_id |           hyperparameters           | hparam_tuning_evaluation_metrics  |   training_loss    |     eval_loss      |  status   | error_message | is_optimal |
   +----------+-------------------------------------+-----------------------------------+--------------------+--------------------+-----------+---------------+------------+
   |        7 |      {"l1_reg":"4.999999999999985"} |  {"r2_score":"0.653653627638174"} | 4.4677841296238165 |  4.478469742512195 | SUCCEEDED | NULL          |       true |
   |        2 |  {"l1_reg":"2.402163664510254E-11"} | {"r2_score":"0.6532493667964732"} |  4.457692508421795 |  4.483697081650438 | SUCCEEDED | NULL          |      false |
   |        3 |  {"l1_reg":"1.2929452948742316E-7"} |  {"r2_score":"0.653249366811995"} |   4.45769250849513 |  4.483697081449748 | SUCCEEDED | NULL          |      false |
   |        4 |  {"l1_reg":"2.5787102060628228E-5"} | {"r2_score":"0.6532493698925899"} |  4.457692523040582 |  4.483697041615808 | SUCCEEDED | NULL          |      false |
   |      ... |                             ...     |                           ...     |              ...   |             ...    |       ... |          ...  |        ... |
   +----------+-------------------------------------+-----------------------------------+--------------------+--------------------+-----------+---------------+------------+
   ```

   `is_optimal` 資料欄值表示微調作業傳回的最佳模型是試驗 7。

## 評估微調模型試驗

使用 `ML.EVALUATE` 函式評估試驗成效。`ML.EVALUATE` 函式會根據訓練期間計算出的所有試驗評估指標，評估模型傳回的預測內容分級。

請按照下列步驟評估模型試驗：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中貼入下列查詢，然後點選「執行」：

   ```
   SELECT *
   FROM
     ML.EVALUATE(MODEL `bqml_tutorial.hp_taxi_tip_model`)
   ORDER BY r2_score DESC;
   ```

   結果類似下方：

   ```
   +----------+---------------------+--------------------+------------------------+-----------------------+--------------------+--------------------+
   | trial_id | mean_absolute_error | mean_squared_error | mean_squared_log_error | median_absolute_error |      r2_score      | explained_variance |
   +----------+---------------------+--------------------+------------------------+-----------------------+--------------------+--------------------+
   |        7 |   1.151814398002232 |  4.109811493266523 |     0.4918733252641176 |    0.5736103414025084 | 0.6652110305659145 | 0.6652144696114834 |
   |       19 |  1.1518143358927102 |  4.109811921460791 |     0.4918672150119582 |    0.5736106106914161 | 0.6652109956848206 | 0.6652144346901685 |
   |        8 |   1.152747850702547 |  4.123625876152422 |     0.4897808307399327 |    0.5731702310239184 | 0.6640856984144734 |  0.664088410199906 |
   |        5 |   1.152895108945439 |  4.125775524878872 |    0.48939088205957937 |    0.5723300569616766 | 0.6639105860807425 | 0.6639132416838652 |
   |      ... |                ...  |                ... |                    ... |                   ... |                ... |                ... |
   +----------+---------------------+--------------------+------------------------+-----------------------+--------------------+--------------------+
   ```

   最佳模型 (試驗 7) 的 `r2_score` 值為 `0.66521103056591446`，相較於基準模型有顯著改善。

您可以在 `ML.EVALUATE` 函式中指定 `TRIAL_ID` 引數，評估特定試驗。

如要進一步瞭解`ML.TRIAL_INFO`目標`ML.EVALUATE`與評估指標的差異，請參閱「[提供模型函式](https://docs.cloud.google.com/bigquery/docs/hp-tuning-overview?hl=zh-tw#model_serving_functions)」。

## 使用微調模型預測計程車小費

使用微調作業傳回的最佳模型，預測不同計程車行程的小費。除非您指定 `TRIAL_ID` 引數來選取其他試用版，否則 `ML.PREDICT` 函式會自動使用最佳模型。預測結果會顯示在 `predicted_label` 欄中。

請按照下列步驟取得預測結果：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中貼入下列查詢，然後點選「執行」：

   ```
   SELECT *
   FROM
     ML.PREDICT(
       MODEL `bqml_tutorial.hp_taxi_tip_model`,
       (
         SELECT
           *
         FROM
           `bqml_tutorial.taxi_tip_input`
         LIMIT 5
       ));
   ```

   結果類似下方：

   ```
   +----------+--------------------+-----------+---------------------+---------------------+-----------------+---------------+-----------+--------------------+--------------+-------------+-------+---------+--------------+---------------+--------------+--------------------+---------------------+----------------+-----------------+-------+
   | trial_id |  predicted_label   | vendor_id |   pickup_datetime   |  dropoff_datetime   | passenger_count | trip_distance | rate_code | store_and_fwd_flag | payment_type | fare_amount | extra | mta_tax | tolls_amount | imp_surcharge | total_amount | pickup_location_id | dropoff_location_id | data_file_year | data_file_month | label |
   +----------+--------------------+-----------+---------------------+---------------------+-----------------+---------------+-----------+--------------------+--------------+-------------+-------+---------+--------------+---------------+--------------+--------------------+---------------------+----------------+-----------------+-------+
   |        7 |  1.343367839584448 | 2         | 2018-01-15 18:55:15 | 2018-01-15 18:56:18 |               1 |             0 | 1         | N                  | 1            |           0 |     0 |       0 |            0 |             0 |            0 | 193                | 193                 |           2018 |               1 |     0 |
   |        7 | -1.176072791783461 | 1         | 2018-01-08 10:26:24 | 2018-01-08 10:26:37 |               1 |             0 | 5         | N                  | 3            |        0.01 |     0 |       0 |            0 |           0.3 |         0.31 | 158                | 158                 |           2018 |               1 |     0 |
   |        7 |  3.839580104168765 | 1         | 2018-01-22 10:58:02 | 2018-01-22 12:01:11 |               1 |          16.1 | 1         | N                  | 1            |        54.5 |     0 |     0.5 |            0 |           0.3 |         55.3 | 140                | 91                  |           2018 |               1 |     0 |
   |        7 |  4.677393985230036 | 1         | 2018-01-16 10:14:35 | 2018-01-16 11:07:28 |               1 |            18 | 1         | N                  | 2            |        54.5 |     0 |     0.5 |            0 |           0.3 |         55.3 | 138                | 67                  |           2018 |               1 |     0 |
   |        7 |  7.938988937253062 | 2         | 2018-01-16 07:05:15 | 2018-01-16 08:06:31 |               1 |          17.8 | 1         | N                  | 1            |        54.5 |     0 |     0.5 |            0 |           0.3 |        66.36 | 132                | 255                 |           2018 |               1 | 11.06 |
   +----------+--------------------+-----------+---------------------+---------------------+-----------------+---------------+-----------+--------------------+--------------+-------------+-------+---------+--------------+---------------+--------------+--------------------+---------------------+----------------+-----------------+-------+
   ```

## 清除所用資源

為避免因為本教學課程所用資源，導致系統向 Google Cloud 帳戶收取費用，請刪除含有相關資源的專案，或者保留專案但刪除個別資源。

* 您可以刪除建立的專案。
* 或者您可以保留專案並刪除資料集。

### 刪除資料集

刪除專案將移除專案中所有的資料集與資料表。若您希望重新使用專案，您可以刪除本教學課程中所建立的資料集。

1. 如有必要，請在Google Cloud 控制台中開啟 BigQuery 頁面。

   [前往 BigQuery 頁面](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在導覽面板中，按一下您建立的 **bqml\_tutorial** 資料集。
3. 在視窗右側，按一下「刪除資料集」。這項操作會刪除資料集、資料表和所有資料。
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

* 如要進一步瞭解機器學習，請參閱[機器學習速成課程](https://developers.google.com/machine-learning/crash-course/?hl=zh-tw)。
* 如需 BigQuery ML 的總覽，請參閱 [BigQuery ML 簡介](https://docs.cloud.google.com/bigquery/docs/bqml-introduction?hl=zh-tw)。
* 如要進一步瞭解 Google Cloud 控制台，請參閱「[使用 Google Cloud 控制台](https://docs.cloud.google.com/bigquery/bigquery-web-ui?hl=zh-tw)」。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-06 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-06 (世界標準時間)。"],[],[]]