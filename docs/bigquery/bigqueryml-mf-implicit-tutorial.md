Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見

# 使用矩陣分解模型，根據隱性意見回饋建立建議 透過集合功能整理內容 你可以依據偏好儲存及分類內容。

本教學課程說明如何建立[矩陣分解模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-matrix-factorization?hl=zh-tw)，並在公開的 [`GA360_test.ga_sessions_sample` 資料表](https://console.cloud.google.com/bigquery?p=cloud-training-demos&%3Bd=GA360_test&%3Bt=ga_sessions_sample&%3Bpage=table&hl=zh-tw)中，使用 Google Analytics 360 使用者工作階段資料訓練模型。接著，您可以使用矩陣分解模型，為網站使用者生成內容建議。

使用使用者工作階段持續時間等間接顧客偏好資訊訓練模型，稱為使用*隱性意見回饋*訓練。使用隱性意見回饋做為訓練資料時，系統會使用[加權交替最小平方演算法](http://yifanhu.net/PUB/cf.pdf)訓練矩陣分解模型。

**重要事項：** 您必須預訂才能使用矩陣因式分解模型。詳情請參閱[定價](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-matrix-factorization?hl=zh-tw#pricing)。

## 目標

本教學課程會逐步引導您完成下列工作：

* 使用 `CREATE MODEL` 陳述式建立矩陣分解模型。
* 使用 [`ML.EVALUATE` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-evaluate?hl=zh-tw)評估模型。
* 使用 [`ML.RECOMMEND` 函式搭配模型，為使用者生成內容建議](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-recommend?hl=zh-tw)。

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

## 準備範例資料

將 `GA360_test.ga_sessions_sample` 資料表中的資料轉換為更適合模型訓練的結構，然後將資料寫入 BigQuery 資料表。下列查詢會計算每位使用者在每項內容的停留時間，您之後可將這項資料做為隱性意見回饋，推斷使用者對該內容的偏好。

請按照下列步驟建立訓練資料表：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 建立訓練資料表。在查詢編輯器中貼上下列查詢，然後點選「執行」：

   ```
   CREATE OR REPLACE TABLE `bqml_tutorial.analytics_session_data`
   AS
   WITH
     visitor_page_content AS (
       SELECT
         fullVisitorID,
         (
           SELECT
             MAX(
               IF(
                 index = 10,
                 value,
                 NULL))
           FROM
             UNNEST(hits.customDimensions)
         ) AS latestContentId,
         (LEAD(hits.time, 1) OVER (PARTITION BY fullVisitorId ORDER BY hits.time ASC) - hits.time)
           AS session_duration
       FROM
         `cloud-training-demos.GA360_test.ga_sessions_sample`,
         UNNEST(hits) AS hits
       WHERE
         # only include hits on pages
         hits.type = 'PAGE'
       GROUP BY
         fullVisitorId,
         latestContentId,
         hits.time
     )
   # aggregate web stats
   SELECT
     fullVisitorID AS visitorId,
     latestContentId AS contentId,
     SUM(session_duration) AS session_duration
   FROM
     visitor_page_content
   WHERE
     latestContentId IS NOT NULL
   GROUP BY
     fullVisitorID,
     latestContentId
   HAVING
     session_duration > 0
   ORDER BY
     latestContentId;
   ```
3. 查看部分訓練資料。在查詢編輯器中貼上下列查詢，然後點選「執行」：

   ```
   SELECT * FROM `bqml_tutorial.analytics_session_data` LIMIT 5;
   ```

   結果應如下所示：

   ```
   +---------------------+-----------+------------------+
   | visitorId           | contentId | session_duration |
   +---------------------+-----------+------------------+
   | 7337153711992174438 | 100074831 | 44652            |
   +---------------------+-----------+------------------+
   | 5190801220865459604 | 100170790 | 121420           |
   +---------------------+-----------+------------------+
   | 2293633612703952721 | 100510126 | 47744            |
   +---------------------+-----------+------------------+
   | 5874973374932455844 | 100510126 | 32109            |
   +---------------------+-----------+------------------+
   | 1173698801255170595 | 100676857 | 10512            |
   +---------------------+-----------+------------------+
   ```

## 建立模型

建立矩陣分解模型，並根據 `analytics_session_data` 資料表中的資料訓練模型。模型經過訓練後，可預測每個 `visitorId`-`contentId` 配對的信心評分。系統會根據工作階段持續時間中位數，以置中和縮放方式建立信賴度評分。如果記錄中的工作階段持續時間是中位數的 3.33 倍以上，系統會將其篩除為離群值。

下列 `CREATE MODEL` 陳述式會使用這些資料欄產生建議：

* `visitorId`：訪客 ID。
* `contentId`—內容 ID。
* `rating`：針對每位訪客與內容配對計算的隱含評分，範圍為 0 到 1，並經過置中和縮放。

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中貼入下列查詢，然後點選「執行」：

   ```
   CREATE OR REPLACE MODEL `bqml_tutorial.mf_implicit`
     OPTIONS (
       MODEL_TYPE = 'matrix_factorization',
       FEEDBACK_TYPE = 'implicit',
       USER_COL = 'visitorId',
       ITEM_COL = 'contentId',
       RATING_COL = 'rating',
       L2_REG = 30,
       NUM_FACTORS = 15)
   AS
   SELECT
     visitorId,
     contentId,
     0.3 * (1 + (session_duration - 57937) / 57937) AS rating
   FROM `bqml_tutorial.analytics_session_data`
   WHERE 0.3 * (1 + (session_duration - 57937) / 57937) < 1;
   ```

   查詢作業約需 10 分鐘才能完成，完成後 `mf_implicit` 模型會顯示在「Explorer」窗格中。由於查詢是使用 `CREATE MODEL` 陳述式建立模型，因此您不會看到查詢結果。

## 取得訓練統計資料

您也可以在Google Cloud 控制台中查看模型的訓練統計資料。

機器學習演算法會使用不同參數建立多個模型疊代版本，然後選取能將[損失](https://en.wikipedia.org/wiki/Loss_function)降到最低的模型版本。這項程序稱為經驗風險最小化。模型訓練統計資料會顯示模型每次疊代的相關損失。

如要查看模型的訓練統計資料，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。

   如果沒有看到左側窗格，請按一下 last\_page「Expand left pane」(展開左側窗格)，開啟窗格。
3. 在「Explorer」窗格中展開專案，然後按一下「Datasets」(資料集)。
4. 點選「`bqml_tutorial`」資料集。您也可以使用搜尋功能或篩選器來尋找資料集。
5. 按一下「模型」分頁標籤。
6. 按一下 `mf_implicit` 模型，然後按一下「訓練」分頁標籤。
7. 在「查看方式」部分，按一下「表格」。結果應如下所示：

   ```
   +-----------+--------------------+--------------------+
   | Iteration | Training Data Loss | Duration (seconds) |
   +-----------+--------------------+--------------------+
   |  5        | 0.0027             | 47.27              |
   +-----------+--------------------+--------------------+
   |  4        | 0.0028             | 39.60              |
   +-----------+--------------------+--------------------+
   |  3        | 0.0032             | 55.57              |
   +-----------+--------------------+--------------------+
   |  ...      | ...                | ...                |
   +-----------+--------------------+--------------------+
   ```

   「Training Data Loss」資料欄代表模型訓練完成後計算出來的損失指標。由於這是矩陣分解模型，因此這個資料欄會顯示[均方誤差](https://developers.google.com/machine-learning/glossary/?hl=zh-tw#MSE)。

## 評估模型

使用 `ML.EVALUATE` 函式評估模型效能。
`ML.EVALUATE` 函式會根據訓練期間計算的評估指標，評估模型傳回的預測內容分級。

請按照下列步驟評估模型：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中貼入下列查詢，然後點選「執行」：

   ```
   SELECT
     *
   FROM
     ML.EVALUATE(MODEL `bqml_tutorial.mf_implicit`);
   ```

   結果應如下所示：

   ```
   +------------------------+-----------------------+---------------------------------------+---------------------+
   | mean_average_precision |  mean_squared_error   | normalized_discounted_cumulative_gain |    average_rank     |
   +------------------------+-----------------------+---------------------------------------+---------------------+
   |     0.4434341257478137 | 0.0013381759837648962 |                    0.9433280547112802 | 0.24031636088594222 |
   +------------------------+-----------------------+---------------------------------------+---------------------+
   ```

   如要進一步瞭解 `ML.EVALUATE` 函式輸出內容，請參閱「[輸出內容](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-evaluate?hl=zh-tw#output)」。

## 取得部分訪客與內容組合的預測評分

使用 `ML.RECOMMEND` 取得五位網站訪客對每項內容的預測評分。

請按照下列步驟取得預測評分：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中貼入下列查詢，然後點選「執行」：

   ```
   SELECT
     *
   FROM
     ML.RECOMMEND(
       MODEL `bqml_tutorial.mf_implicit`,
       (
         SELECT
           visitorId
         FROM
           `bqml_tutorial.analytics_session_data`
         LIMIT 5
       ));
   ```

   結果應如下所示：

   ```
   +-------------------------------+---------------------+-----------+
   | predicted_rating_confidence   | visitorId           | contentId |
   +-------------------------------+---------------------+-----------+
   | 0.0033608418060270262         | 7337153711992174438 | 277237933 |
   +-------------------------------+---------------------+-----------+
   | 0.003602395397293956          | 7337153711992174438 | 158246147 |
   +-------------------------------+---------------------+--  -------+
   | 0.0053197670652785356         | 7337153711992174438 | 299389988 |
   +-------------------------------+---------------------+-----------+
   | ...                           | ...                 | ...       |
   +-------------------------------+---------------------+-----------+
   ```

## 生成建議

使用預測評分，為每個訪客 ID 生成前五個建議內容 ID。

請按照下列步驟產生建議：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 將預測評分寫入資料表。在查詢編輯器中貼上以下查詢，然後點選「執行」：

   ```
   CREATE OR REPLACE TABLE `bqml_tutorial.recommend_content`
   AS
   SELECT
     *
   FROM
     ML.RECOMMEND(MODEL `bqml_tutorial.mf_implicit`);
   ```
3. 為每位訪客選取前五個結果。在查詢編輯器中貼上以下查詢，然後點選「執行」：

   ```
   SELECT
     visitorId,
     ARRAY_AGG(
       STRUCT(contentId, predicted_rating_confidence)
       ORDER BY predicted_rating_confidence DESC
       LIMIT 5) AS rec
   FROM
     `bqml_tutorial.recommend_content`
   GROUP BY
     visitorId;
   ```

   結果應如下所示：

   ```
   +---------------------+-----------------+---------------------------------+
   | visitorId           | rec:contentId   | rec:predicted_rating_confidence |
   +---------------------+-----------------+-------------------------  ------+
   | 867526255058981688  | 299804319       | 0.88170525357178664             |
   |                     | 299935287       | 0.54699439944935124             |
   |                     | 299410466       | 0.53424780863188659             |
   |                     | 299826767       | 0.46949603950374219             |
   |                     | 299809748       | 0.3379991197434149              |
   +---------------------+-----------------+---------------------------------+
   | 2434264018925667659 | 299824032       | 1.3903516407308065              |
   |                     | 299410466       | 0.9921995618196483              |
   |                     | 299903877       | 0.92333625294129218             |
   |                     | 299816215       | 0.91856701667757279             |
   |                     | 299852437       | 0.86973661454890561             |
   +---------------------+-----------------+---------------------------------+
   | ...                 | ...             | ...                             |
   +---------------------+-----------------+---------------------------------+
   ```

## 清除所用資源

為避免因為本教學課程所用資源，導致系統向 Google Cloud 帳戶收取費用，請刪除含有相關資源的專案，或者保留專案但刪除個別資源。

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

* 嘗試[根據明確意見回饋建立矩陣分解模型](https://docs.cloud.google.com/bigquery/docs/bigqueryml-mf-explicit-tutorial?hl=zh-tw)。
* 如需 BigQuery ML 的總覽，請參閱 [BigQuery ML 簡介](https://docs.cloud.google.com/bigquery/docs/bqml-introduction?hl=zh-tw)。
* 如要進一步瞭解機器學習，請參閱[機器學習速成課程](https://developers.google.com/machine-learning/crash-course/?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-12 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-12 (世界標準時間)。"],[],[]]