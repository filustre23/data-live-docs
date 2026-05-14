Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見

# 使用 TRANSFORM 子句執行特徵工程 透過集合功能整理內容 你可以依據偏好儲存及分類內容。

本教學課程說明如何使用 `CREATE MODEL` 陳述式的 [`TRANSFORM` 子句](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create?hl=zh-tw#transform)，在建立及訓練模型的同時執行特徵工程。使用 `TRANSFORM` 子句，您可以指定一或多個[預先處理](https://docs.cloud.google.com/bigquery/docs/manual-preprocessing?hl=zh-tw)函式，轉換用於訓練模型的輸入資料。使用 [`ML.EVALUATE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-evaluate?hl=zh-tw) 和 [`ML.PREDICT`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-predict?hl=zh-tw) 函式時，系統會自動套用您對模型執行的前處理作業。

本教學課程使用公開的[`bigquery-public-data.ml_datasets.penguin`資料集](https://console.cloud.google.com/bigquery?p=bigquery-public-data&%3Bd=ml_datasets&%3Bt=penguins&%3Bpage=table&hl=zh-tw)。

## 目標

本教學課程會逐步引導您完成下列工作：

* 使用 [`CREATE MODEL` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-glm?hl=zh-tw)建立線性迴歸模型，預測服務呼叫類型。在 `CREATE MODEL` 陳述式中，使用 [`ML.QUANTILE_BUCKETIZE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-quantile-bucketize?hl=zh-tw) 和 [`ML.FEATURE_CROSS`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-feature-cross?hl=zh-tw) 函式預先處理資料。
* 使用 [`ML.EVALUATE` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-evaluate?hl=zh-tw)評估模型。
* 使用 [`ML.PREDICT` 函式從模型取得預測結果](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-predict?hl=zh-tw)。

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

## 建立模型

建立線性迴歸模型來預測企鵝體重，並在 `penguins` 範例資料表上訓練模型。

`OPTIONS(model_type='linear_reg', input_label_cols=['body_mass_g'])`
子句代表您在建立[線性迴歸](https://en.wikipedia.org/wiki/Linear_regression)模型。線性迴歸模型會從輸入特徵的線性組合產生連續值。`body_mass_g` 資料欄是輸入標籤欄。對線性迴歸模型而言，標籤欄必須為實際的值 (也就是資料欄值必須為實數)。

這個查詢的 `TRANSFORM` 子句會使用 `SELECT` 陳述式中的下列資料欄：

* `body_mass_g`：用於訓練，不進行任何變更。
* `culmen_depth_mm`：用於訓練，不進行任何變更。
* `flipper_length_mm`：用於訓練，不進行任何變更。
* `bucketized_culmen_length`：透過使用 `ML.QUANTILE_BUCKETIZE()` 分析函式，根據分位數將 `culmen_length_mm` 區化，從 `culmen_length_mm` 產生。
* `culmen_length_mm`：原始 `culmen_length_mm` 值，轉換為 `STRING` 值並用於訓練。
* `species_sex`：使用 `ML.FEATURE_CROSS` 函式，從 `species` 和 `sex` 的交集產生。

您不需要在 `TRANSFORM` 子句中使用訓練資料表中的所有資料欄。

`WHERE` 子句 - `WHERE body_mass_g IS NOT NULL AND RAND() < 0.2` - 排除企鵝體重為 `NULL` 的資料列，並使用 `RAND` 函數來進行隨機資料抽樣。

請按照下列步驟建立模型：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中貼入下列查詢，然後點選「執行」：

   ```
   CREATE OR REPLACE MODEL `bqml_tutorial.penguin_transform`
     TRANSFORM(
       body_mass_g,
       culmen_depth_mm,
       flipper_length_mm,
       ML.QUANTILE_BUCKETIZE(culmen_length_mm, 10) OVER () AS bucketized_culmen_length,
       CAST(culmen_length_mm AS string) AS culmen_length_mm,
       ML.FEATURE_CROSS(STRUCT(species, sex)) AS species_sex)
     OPTIONS (
       model_type = 'linear_reg',
       input_label_cols = ['body_mass_g'])
   AS
   SELECT
     *
   FROM
     `bigquery-public-data.ml_datasets.penguins`
   WHERE
     body_mass_g IS NOT NULL
     AND RAND() < 0.2;
   ```

   查詢作業約需 15 分鐘才能完成，完成後 `penguin_transform` 模型會顯示在「Explorer」窗格中。由於查詢是使用 `CREATE MODEL` 陳述式建立模型，因此您不會看到查詢結果。

## 評估模型

使用 `ML.EVALUATE` 函式評估模型效能。
`ML.EVALUATE` 函式會根據訓練資料中的實際企鵝體重，評估模型傳回的預測企鵝體重。

這個查詢的巢狀 `SELECT` 陳述式及 `FROM` 子句與 `CREATE MODEL` 查詢中的相同。由於您在建立模型時使用了 `TRANSFORM` 子句，因此不必在 `ML.EVALUATE` 函式中再次指定資料欄和轉換。這項函式會自動從模型中擷取這些值。

請按照下列步驟評估模型：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中貼入下列查詢，然後點選「執行」：

   ```
   SELECT
     *
   FROM
     ML.EVALUATE(
       MODEL `bqml_tutorial.penguin_transform`,
       (
         SELECT
           *
         FROM
           `bigquery-public-data.ml_datasets.penguins`
         WHERE
           body_mass_g IS NOT NULL
       ));
   ```

   結果應如下所示：

   ```
   +---------------------+--------------------+------------------------+-----------------------+--------------------+--------------------+
   | mean_absolute_error | mean_squared_error | mean_squared_log_error | median_absolute_error |      r2_score      | explained_variance |
   +---------------------+--------------------+------------------------+-----------------------+--------------------+--------------------+
   |   64.21134350607677 | 13016.433317859564 |   7.140935762696211E-4 |     15.31788461553515 | 0.9813042531507734 | 0.9813186268757634 |
   +---------------------+--------------------+------------------------+-----------------------+--------------------+--------------------+
   ```

   評估結果中有個重要的指標，就是 [R2 分數](https://en.wikipedia.org/wiki/Coefficient_of_determination)。R2 分數是種統計量具，用來確認線性迴歸的預測結果是否趨近於實際資料。`0` 值代表模型無法解釋平均值周圍之回應資料的變化。`1` 值代表模型能夠解釋所有平均值周圍之回應資料的所有變化。

   如要進一步瞭解 `ML.EVALUATE` 函式輸出內容，請參閱「[輸出內容](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-evaluate?hl=zh-tw#output)」。

   您也可以呼叫 `ML.EVALUATE`，而不提供輸入資料。並使用訓練期間計算的評估指標。

## 使用模型預測企鵝體重

使用 `ML.PREDICT` 函式搭配模型，預測雄性企鵝的體重。

`ML.PREDICT` 函式會在 `predicted_label_column_name` 資料欄中輸出預測值，在本例中為 `predicted_body_mass_g`。

使用 `ML.PREDICT` 函式時，不必傳遞模型訓練中使用的所有資料欄。您只需要在 `TRANSFORM` 子句中使用過的資料欄。與 `ML.EVALUATE` 類似，`ML.PREDICT` 函式會自動從模型擷取 `TRANSFORM` 欄和轉換。

請按照下列步驟，從模型取得預測結果：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中貼入下列查詢，然後點選「執行」：

   ```
   SELECT
     predicted_body_mass_g
   FROM
     ML.PREDICT(
       MODEL `bqml_tutorial.penguin_transform`,
       (
         SELECT
           *
         FROM
           `bigquery-public-data.ml_datasets.penguins`
         WHERE
           sex = 'MALE'
       ));
   ```

   結果應如下所示：

   ```
   +-----------------------+
   | predicted_body_mass_g |
   +-----------------------+
   |    2810.2868541725757 |
   +-----------------------+
   |    3813.6574220842676 |
   +-----------------------+
   |     4098.844698262214 |
   +-----------------------+
   |     4256.587135004173 |
   +-----------------------+
   |     3008.393497302691 |
   +-----------------------+
   |     ...               |
   +-----------------------+
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
4. 在「Delete dataset」(刪除資料集) 對話方塊中，輸入資料集的名稱 (`bqml_tutorial`)，然後按一下 [Delete] (刪除) 來確認刪除指令。

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

上次更新時間：2026-05-14 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-14 (世界標準時間)。"],[],[]]