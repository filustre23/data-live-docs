Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見

# 使用 TimesFM 單變數模型預測單一或多個時間序列 透過集合功能整理內容 你可以依據偏好儲存及分類內容。

本教學課程說明如何使用 [`AI.FORECAST` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-ai-forecast?hl=zh-tw)和 BigQuery 內建的 [TimesFM 單變數模型](https://docs.cloud.google.com/bigquery/docs/timesfm-model?hl=zh-tw)，對單一或多個時間序列執行單變數預測。

本教學課程會使用公開資料表中的資料。[`bigquery-public-data.san_francisco_bikeshare.bikeshare_trips`](https://console.cloud.google.com/bigquery?p=bigquery-public-data&%3Bd=san_francisco_bikeshare&%3Bt=bikeshare_trips&%3Bpage=table&hl=zh-tw)

## 目標

* 執行單變數預測，並以圖表呈現單一時間序列的結果。
* 執行單變數預測，並以圖表呈現多個時間序列的結果。

## 費用

本教學課程使用的 Google Cloud計費元件包括：

* BigQuery
* BigQuery ML

詳情請參閱「[BigQuery 定價](https://docs.cloud.google.com/bigquery/pricing?hl=zh-tw)」和「[BigQuery ML 定價](https://docs.cloud.google.com/bigquery/pricing?hl=zh-tw#bqml)」一文。

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

1. 如果尚未啟用 BigQuery API，請啟用。

   **啟用 API 時所需的角色**

   如要啟用 API，您必須具備 `serviceusage.services.enable` 權限。如果您建立了專案，可能已透過「擁有者」角色 (`roles/owner`) 取得這項權限。否則，您可以透過「服務使用情形管理員」角色 (`roles/serviceusage.serviceUsageAdmin`) 取得這項權限。[瞭解如何授予角色](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)。

   [啟用 API](https://console.cloud.google.com/apis/enableflow?apiid=bigquery.googleapis.com&hl=zh-tw)

   新專案會自動啟用 BigQuery API。

### 必要的角色

如要取得完成本教學課程中工作所需的權限，請要求管理員授予您下列 IAM 角色：

* 建立資料集：
  [BigQuery 資料編輯器](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.dataEditor)  (`roles/bigquery.dataEditor`)
* 建立模型：
  + [BigQuery 資料編輯者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.dataEditor)  (`roles/bigquery.dataEditor`)
  + [BigQuery 工作使用者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.jobUser)  (`roles/bigquery.jobUser`)
* 執行推論：
  + [BigQuery 資料編輯者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.dataEditor)  (`roles/bigquery.dataEditor`)
  + [BigQuery 工作使用者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.jobUser)  (`roles/bigquery.jobUser`)

如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

這些預先定義的角色具備完成本教學課程中工作所需的權限。如要查看確切的必要權限，請展開「Required permissions」(必要權限) 部分：

#### 所需權限

如要完成本教學課程中的工作，必須具備下列權限：

* 建立資料集：
  `bigquery.datasets.create`
* 建立模型：
  + `bigquery.jobs.create`
  + `bigquery.models.create`
  + `bigquery.models.getData`
  + `bigquery.models.updateData`
* 執行推論：
  + `bigquery.models.getData`
  + `bigquery.jobs.create`

您或許還可透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)取得這些權限。

如要進一步瞭解 BigQuery 中的 IAM 角色和權限，請參閱「[IAM 簡介](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)」。

## 預測單一共享單車行程時間序列

使用 `AI.FORECAST` 函式預測未來時間序列值。

下列查詢會根據前四個月的歷來資料，預測下個月每小時的訂閱者共享單車行程數 (約 720 小時)。`confidence_level` 引數表示查詢會產生信賴區間為 95% 的預測間隔。

如要使用 TimesFM 模型預測資料，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中貼入下列查詢，然後點選「執行」：

   ```
   SELECT *
   FROM
     AI.FORECAST(
       (
         SELECT TIMESTAMP_TRUNC(start_date, HOUR) as trip_hour, COUNT(*) as num_trips
   FROM `bigquery-public-data.san_francisco_bikeshare.bikeshare_trips`
   WHERE subscriber_type = 'Subscriber' AND start_date >= TIMESTAMP('2018-01-01')
   GROUP BY TIMESTAMP_TRUNC(start_date, HOUR)
       ),
       horizon => 720,
       confidence_level => 0.95,
       timestamp_col => 'trip_hour',
       data_col => 'num_trips');
   ```

   結果類似下方：

   ```
   +-------------------------+-------------------+------------------+---------------------------------+---------------------------------+--------------------+
   | forecast_timestamp      | forecast_value    | confidence_level | prediction_interval_lower_bound | prediction_interval_upper_bound | ai_forecast_status |
   +-------------------------+-------------------+------------------+---------------------------------+---------------------------------+--------------------+
   | 2018-05-01 00:00:00 UTC | 26.3045959...     |            0.95  | 21.7088378...                   | 30.9003540...                   |                    |
   +-------------------------+-------------------+------------------+---------------------------------+---------------------------------+--------------------+
   | 2018-05-01 01:00:00 UTC | 34.0890502...     |            0.95  | 2.47682913...                   | 65.7012714...                   |                    |
   +-------------------------+-------------------+------------------+---------------------------------+---------------------------------+--------------------+
   | 2018-05-01 02:00:00 UTC | 24.2154693...     |            0.95  | 2.87621605...                   | 45.5547226...                   |                    |
   +-------------------------+-------------------+------------------+---------------------------------+---------------------------------+--------------------+
   | ...                     | ...               |  ...             | ...                             |  ...                            |                    |
   +-------------------------+-------------------+------------------+---------------------------------+---------------------------------+--------------------+
   ```

## 比較預測資料與輸入資料

將 `AI.FORECAST` 函式輸出內容與部分函式輸入資料繪製成圖表，比較兩者差異。

請按照下列步驟繪製函式輸出內容的圖表：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中貼入下列查詢，然後點選「執行」：

   ```
   SELECT *
   FROM
     AI.FORECAST(
       (
         SELECT TIMESTAMP_TRUNC(start_date, HOUR) as trip_hour, COUNT(*) as num_trips
         FROM `bigquery-public-data.san_francisco_bikeshare.bikeshare_trips`
         WHERE subscriber_type = 'Subscriber' AND start_date >= TIMESTAMP('2018-01-01')
         GROUP BY TIMESTAMP_TRUNC(start_date, HOUR)
       ),
       horizon => 720,
       confidence_level => 0.95,
       timestamp_col => 'trip_hour',
       data_col => 'num_trips',
       output_historical_time_series => true);
   ```
3. 查詢執行完畢後，按一下「查詢結果」窗格中的「圖表」分頁標籤。「圖表類型」請選取「折線圖」。在「維度」部分，選取 `time_series_timestamp`。在「測量指標」中，選取 `time_series_data`、`prediction_interval_lower_bound` 和 `prediction_interval_upper_bound`。產生的圖表如下所示：

   您可以看到輸入資料和預測資料顯示的共享單車使用情形相似。您也可以看到，隨著預測時間點越往未來延伸，預測區間的下限和上限都會增加。

## 預測多個共享單車行程時間序列

以下查詢會根據過去四個月的歷來資料，預測下個月 (約 720 小時) 各訂閱者類型每小時的共享單車行程數量。`confidence_level` 引數表示查詢會產生信賴區間為 95% 的預測間隔。

如要使用 TimesFM 模型預測資料，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中貼入下列查詢，然後點選「執行」：

   ```
   SELECT *
   FROM
     AI.FORECAST(
       (
         SELECT TIMESTAMP_TRUNC(start_date, HOUR) as trip_hour, subscriber_type, COUNT(*) as num_trips
         FROM `bigquery-public-data.san_francisco_bikeshare.bikeshare_trips`
         WHERE start_date >= TIMESTAMP('2018-01-01')
         GROUP BY TIMESTAMP_TRUNC(start_date, HOUR), subscriber_type
       ),
       horizon => 720,
       confidence_level => 0.95,
       timestamp_col => 'trip_hour',
       data_col => 'num_trips',
       id_cols => ['subscriber_type']);
   ```

   結果類似下方：

   ```
   +---------------------+--------------------------+------------------+------------------+---------------------------------+---------------------------------+--------------------+
   | subscriber_type     | forecast_timestamp       | forecast_value   | confidence_level | prediction_interval_lower_bound | prediction_interval_upper_bound | ai_forecast_status |
   +---------------------+--------------------------+------------------+------------------+---------------------------------+---------------------------------+--------------------+
   | Subscriber          | 2018-05-01 00:00:00 UTC  | 26.3045959...    |            0.95  | 21.7088378...                   | 30.9003540...                   |                    |
   +---------------------+--------------------------+------------------+------------------+---------------------------------+---------------------------------+--------------------+
   | Subscriber          |  2018-05-01 01:00:00 UTC | 34.0890502...    |            0.95  | 2.47682913...                   | 65.7012714...                   |                    |
   +---------------------+-------------------+------------------+-------------------------+---------------------------------+---------------------------------+--------------------+
   | Subscriber          |  2018-05-01 02:00:00 UTC | 24.2154693...    |            0.95  | 2.87621605...                   | 45.5547226...                   |                    |
   +---------------------+--------------------------+------------------+------------------+---------------------------------+---------------------------------+--------------------+
   | ...                 | ...                      |  ...             | ...              | ...                             |  ...                            |                    |
   +---------------------+--------------------------+------------------+------------------+---------------------------------+---------------------------------+--------------------+
   ```

## 清除所用資源

為避免因為本教學課程所用資源，導致系統向 Google Cloud 帳戶收取費用，請刪除含有相關資源的專案，或者保留專案但刪除個別資源。

### 刪除專案

**注意**：刪除專案會造成以下結果：

* **專案中的所有內容都會遭到刪除。**如果使用現有專案來進行本文中的任務，刪除專案將一併移除當中已完成的其他任務'。
* **自訂專案 ID 會消失。**當您之前建立這個專案時，可能建立了想要在日後使用的自訂專案 ID。如要保留使用該專案 ID 的網址 (例如 `appspot.com` 網址)，請刪除在該專案中選取的資源，而不是刪除整個專案。

如果打算探索多種架構、教學課程或快速入門導覽課程，重複使用專案可避免超出專案配額限制。

1. 前往 Google Cloud 控制台的「Manage resources」(管理資源) 頁面。

   [前往「Manage resources」(管理資源)](https://console.cloud.google.com/iam-admin/projects?hl=zh-tw)
2. 在專案清單中選取要刪除的專案，然後點選「Delete」(刪除)。
3. 在對話方塊中輸入專案 ID，然後按一下 [Shut down] (關閉) 以刪除專案。

## 後續步驟

* 如需 BigQuery ML 的總覽，請參閱「[BigQuery 中的 AI 和 ML 簡介](https://docs.cloud.google.com/bigquery/docs/bqml-introduction?hl=zh-tw)」。
* 瞭解如何[使用 TimesFM 多變數模型預測單一時間序列](https://docs.cloud.google.com/bigquery/docs/timesfm-multivariate-single-time-series-forecasting-tutorial?hl=zh-tw)。
* 瞭解如何[使用 TimesFM 多變數模型預測多個時間序列](https://docs.cloud.google.com/bigquery/docs/timesfm-multivariate-multi-time-series-forecasting-tutorial?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-10-17 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-10-17 (世界標準時間)。"],[],[]]