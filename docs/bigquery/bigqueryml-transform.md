Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見

# 使用 TRANSFORM 子句執行特徵工程 透過集合功能整理內容 你可以依據偏好儲存及分類內容。

本教學課程說明如何使用 `CREATE MODEL` 陳述式的 [`TRANSFORM` 子句](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create?hl=zh-tw#transform)，在建立及訓練模型的同時執行特徵工程。您可以使用 `TRANSFORM` 子句，指定一或多個[前置處理](https://docs.cloud.google.com/bigquery/docs/manual-preprocessing?hl=zh-tw)函式，轉換用於訓練模型的輸入資料。當您搭配使用模型與 [`ML.EVALUATE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-evaluate?hl=zh-tw) 和 [`ML.PREDICT`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-predict?hl=zh-tw) 函式時，系統會自動套用您對模型套用的預先處理。

本教學課程使用公開的 [`bigquery-public-data.ml_datasets.penguin` 資料集](https://console.cloud.google.com/bigquery?p=bigquery-public-data&%3Bd=ml_datasets&%3Bt=penguins&%3Bpage=table&hl=zh-tw)。

## 目標

本教學課程會逐步引導您完成下列工作：

* 使用 [`CREATE MODEL` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-glm?hl=zh-tw)建立線性迴歸模型，預測服務通話類型。在 `CREATE MODEL` 陳述式中，使用 [`ML.QUANTILE_BUCKETIZE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-quantile-bucketize?hl=zh-tw) 和 [`ML.FEATURE_CROSS`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-feature-cross?hl=zh-tw) 函式預先處理資料。
* 使用 [`ML.EVALUATE` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-evaluate?hl=zh-tw)評估模型。
* 使用 [`ML.PREDICT` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-predict?hl=zh-tw)取得模型的預測結果。

## 費用

本教學課程使用 Google Cloud的計費元件，包括：

* BigQuery
* BigQuery ML

如要進一步瞭解 BigQuery 費用，請參閱「[BigQuery 定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw)」頁面。

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

## 建立模型

建立線性迴歸模型來預測企鵝體重，並使用 `penguins` 樣本資料表訓練模型。

`OPTIONS(model_type='linear_reg', input_label_cols=['body_mass_g'])` 子句表示您正在建立[線性迴歸](https://en.wikipedia.org/wiki/Linear_regression)模型。線性迴歸模型會根據輸入特徵的線性組合，產生連續值。`body_mass_g` 欄是輸入標籤欄。如果是線性迴歸模型，標籤欄必須是實數值 (也就是說，欄值必須是實數)。

這項查詢的 `TRANSFORM` 子句會使用 `SELECT` 陳述式中的下列資料欄：

* `body_mass_g`：用於訓練，不進行任何變更。
* `culmen_depth_mm`：用於訓練，不進行任何變更。
* `flipper_length_mm`：用於訓練，不進行任何變更。
* `bucketized_culmen_length`：使用 `ML.QUANTILE_BUCKETIZE()` 分析函式，根據分位數將 `culmen_length_mm` 分桶，從 `culmen_length_mm` 產生。
* `culmen_length_mm`：原始 `culmen_length_mm` 值，轉換為 `STRING` 值並用於訓練。
* `species_sex`：使用 `ML.FEATURE_CROSS` 函式交叉 `species` 和 `sex` 產生。

您不需要在 `TRANSFORM` 子句中使用訓練資料表的所有資料欄。

`WHERE` 子句 `WHERE body_mass_g IS NOT NULL AND RAND() < 0.2` 會排除企鵝體重為 `NULL` 的資料列，並使用 `RAND` 函式隨機抽取資料樣本。

請按照下列步驟建立模型：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中貼上以下查詢，然後點選「執行」：

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

   查詢約需 15 分鐘才能完成，完成後，`penguin_transform` 模型會顯示在「Explorer」窗格中。由於查詢使用 `CREATE MODEL` 陳述式建立模型，因此不會顯示查詢結果。

## 評估模型

使用 `ML.EVALUATE` 函式評估模型效能。`ML.EVALUATE` 函式會根據訓練資料中的實際企鵝體重，評估模型傳回的預測企鵝體重。

這項查詢的巢狀 `SELECT` 陳述式和 `FROM` 子句與 `CREATE MODEL` 查詢中的相同。由於您在建立模型時使用了 `TRANSFORM` 子句，因此不需要在 `ML.EVALUATE` 函式中再次指定資料欄和轉換。函式會自動從模型中擷取這些值。

請按照下列步驟評估模型：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中貼上以下查詢，然後點選「執行」：

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

   結果應大致如下：

   ```
   +---------------------+--------------------+------------------------+-----------------------+--------------------+--------------------+
   | mean_absolute_error | mean_squared_error | mean_squared_log_error | median_absolute_error |      r2_score      | explained_variance |
   +---------------------+--------------------+------------------------+-----------------------+--------------------+--------------------+
   |   64.21134350607677 | 13016.433317859564 |   7.140935762696211E-4 |     15.31788461553515 | 0.9813042531507734 | 0.9813186268757634 |
   +---------------------+--------------------+------------------------+-----------------------+--------------------+--------------------+
   ```

   評估結果中的重要指標是 [R2 分數](https://en.wikipedia.org/wiki/Coefficient_of_determination)。R2 分數是統計測量數，可判斷線性迴歸預測是否接近實際資料。如果值為 `0`，表示模型無法解釋回應資料在平均值附近的變異性。如果值為 `1`，表示模型可解釋平均值附近的所有回應資料變異。

   如要進一步瞭解 `ML.EVALUATE` 函式輸出內容，請參閱「[輸出內容](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-evaluate?hl=zh-tw#output)」。

   您也可以呼叫 `ML.EVALUATE`，而不提供輸入資料。系統會使用訓練期間計算的評估指標。

## 使用模型預測企鵝體重

使用模型搭配 `ML.PREDICT` 函式，預測雄性企鵝的體重。

`ML.PREDICT` 函式會輸出 `predicted_label_column_name` 欄中的預測值，在本例中為 `predicted_body_mass_g`。

使用 `ML.PREDICT` 函式時，您不必傳入模型訓練中使用的所有資料欄。您只需要提供在 `TRANSFORM` 子句中使用的資料欄。與 `ML.EVALUATE` 類似，`ML.PREDICT` 函式會自動從模型擷取 `TRANSFORM` 資料欄和轉換。

請按照下列步驟，取得模型的預測結果：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中貼上以下查詢，然後點選「執行」：

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

   結果應大致如下：

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

1. 如有需要，請在Google Cloud 控制台開啟 BigQuery 頁面。

   [前往「BigQuery」頁面](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在導覽面板中，點選您建立的 **bqml\_tutorial** 資料集。
3. 按一下視窗右側的「刪除資料集」。這項操作會刪除資料集、資料表和所有資料。
4. 在「Delete dataset」(刪除資料集) 對話方塊中，輸入資料集的名稱 (`bqml_tutorial`)，然後按一下 [Delete] (刪除) 來確認刪除指令。

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

* 如要進一步瞭解機器學習，請參閱[機器學習速成課程](https://developers.google.com/machine-learning/crash-course/?hl=zh-tw)。
* 如需 BigQuery ML 的總覽，請參閱 [BigQuery ML 簡介](https://docs.cloud.google.com/bigquery/docs/bqml-introduction?hl=zh-tw)。
* 如要進一步瞭解 Google Cloud 控制台，請參閱「[使用 Google Cloud 控制台](https://docs.cloud.google.com/bigquery/bigquery-web-ui?hl=zh-tw)」一文。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-11-08 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-11-08 (世界標準時間)。"],[],[]]