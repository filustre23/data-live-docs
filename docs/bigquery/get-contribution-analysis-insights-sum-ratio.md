Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 使用可相加的比率指標，從貢獻度分析模型取得資料洞察

在本教學課程中，您將使用[貢獻度分析](https://docs.cloud.google.com/bigquery/docs/contribution-analysis?hl=zh-tw)模型，分析愛荷華州酒類銷售資料集中銷售成本比率的貢獻度。本教學課程會逐步引導您完成下列工作：

* 根據愛荷華州公開酒類資料建立輸入資料表。
* 建立使用[可相加比率指標](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-contribution-analysis?hl=zh-tw#use_a_summable_ratio_metric)的[貢獻度分析模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-contribution-analysis?hl=zh-tw)。這類模型會彙整兩個數值資料欄的值，並判斷控制組和測試資料集之間，各資料區隔的比例差異。
* 使用 [`ML.GET_INSIGHTS` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-get-insights?hl=zh-tw)，從模型取得指標洞察。

開始本教學課程前，請先熟悉[貢獻度分析](https://docs.cloud.google.com/bigquery/docs/contribution-analysis?hl=zh-tw)應用情境。

## 所需權限

* 如要建立資料集，您需要 `bigquery.datasets.create` Identity and Access Management (IAM) 權限。
* 如要建立模型，您需要下列權限：

  + `bigquery.jobs.create`
  + `bigquery.models.create`
  + `bigquery.models.getData`
  + `bigquery.models.updateData`
* 如要執行推論，您需要下列權限：

  + `bigquery.models.getData`
  + `bigquery.jobs.create`

## 費用

在本文件中，您會使用下列 Google Cloud的計費元件：

* **BigQuery ML**: You incur costs for the data that you
  process in BigQuery.

如要根據預測用量估算費用，請使用 [Pricing Calculator](https://docs.cloud.google.com/products/calculator?hl=zh-tw)。

初次使用 Google Cloud 的使用者可能符合[免費試用期](https://docs.cloud.google.com/free?hl=zh-tw)資格。

如要進一步瞭解 BigQuery 定價，請參閱 BigQuery 說明文件中的「[BigQuery 定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw)」一文。

## 事前準備

1. 在 Google Cloud 控制台的專案選擇器頁面中，選取或建立 Google Cloud 專案。

   **選取或建立專案所需的角色**

   * **選取專案**：選取專案時，不需要具備特定 IAM 角色，只要您已獲授角色，即可選取任何專案。
   * **建立專案**：如要建立專案，您需要具備專案建立者角色 (`roles/resourcemanager.projectCreator`)，其中包含 `resourcemanager.projects.create` 權限。[瞭解如何授予角色](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)。
   **注意**：如果您不打算保留在這項程序中建立的資源，請建立新專案，而不要選取現有專案。完成這些步驟後，您就可以刪除專案，並移除與該專案相關聯的所有資源。

   [前往專案選取器](https://console.cloud.google.com/projectselector2/home/dashboard?hl=zh-tw)
2. [確認專案已啟用計費功能 Google Cloud](https://docs.cloud.google.com/billing/docs/how-to/verify-billing-enabled?hl=zh-tw#confirm_billing_is_enabled_on_a_project) 。
3. 啟用 BigQuery API。

   **啟用 API 時所需的角色**

   如要啟用 API，您需要服務使用情形管理員 IAM 角色 (`roles/serviceusage.serviceUsageAdmin`)，其中包含 `serviceusage.services.enable` 權限。[瞭解如何授予角色](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)。

   [啟用 API](https://console.cloud.google.com/flows/enableapi?apiid=bigquery.googleapis.com&hl=zh-tw)

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

## 建立輸入資料表

建立包含測試和控制項資料的資料表，以供分析。下列查詢會建立兩個中繼資料表，分別是 2021 年酒類資料的測試資料表，以及 2020 年酒類資料的控制組資料表，然後合併中繼資料表，建立同時包含測試和控制組資料列的資料表，以及相同的資料欄集。

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中執行下列陳述式：

   ```
   CREATE OR REPLACE TABLE bqml_tutorial.iowa_liquor_sales_data AS
   (SELECT
     store_name,
     city,
     vendor_name,
     category_name,
     item_description,
     SUM(sale_dollars) AS total_sales,
     SUM(state_bottle_cost) AS total_bottle_cost,
     FALSE AS is_test
   FROM `bigquery-public-data.iowa_liquor_sales.sales`
   WHERE EXTRACT(YEAR FROM date) = 2020
   GROUP BY store_name, city, vendor_name, category_name, item_description, is_test)
   UNION ALL
   (SELECT
     store_name,
     city,
     vendor_name,
     category_name,
     item_description,
     SUM(sale_dollars) AS total_sales,
     SUM(state_bottle_cost) AS total_bottle_cost,
     TRUE AS is_test
   FROM `bigquery-public-data.iowa_liquor_sales.sales`
   WHERE EXTRACT(YEAR FROM date) = 2021
   GROUP BY store_name, city, vendor_name, category_name, item_description, is_test);
   ```

## 建立模型

建立貢獻分析模型：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中執行下列陳述式：

   ```
   CREATE OR REPLACE MODEL bqml_tutorial.liquor_sales_model
   OPTIONS(
     model_type = 'CONTRIBUTION_ANALYSIS',
     contribution_metric = 'sum(total_bottle_cost)/sum(total_sales)',
     dimension_id_cols = ['store_name', 'city', 'vendor_name', 'category_name', 'item_description'],
     is_test_col = 'is_test',
     min_apriori_support = 0.05
   ) AS
   SELECT * FROM bqml_tutorial.iowa_liquor_sales_data;
   ```

查詢作業大約需要 35 秒才能完成，完成後，模型 `liquor_sales_model` 會顯示在 `bqml_tutorial` 資料集中。由於查詢使用 `CREATE MODEL` 陳述式建立模型，因此沒有查詢結果。

## 從模型中取得洞察資料

使用 `ML.GET_INSIGHTS` 函式，取得貢獻度分析模型產生的洞察資料。

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中，執行下列陳述式，從[可加總比率指標貢獻度分析模型輸出內容](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-get-insights?hl=zh-tw#output_for_summable_ratio_metric_contribution_analysis_models)中選取資料欄：

   ```
   SELECT
   contributors,
   metric_test,
   metric_control,
   metric_test_over_metric_control,
   metric_test_over_complement,
   metric_control_over_complement,
   aumann_shapley_attribution,
   apriori_support
   contribution
   FROM
     ML.GET_INSIGHTS(
       MODEL `bqml_tutorial.liquor_sales_model`)
   ORDER BY aumann_shapley_attribution DESC;
   ```

輸出內容的前幾列應如下所示：為提升可讀性，系統會截斷值。

| 貢獻者 | metric\_test | metric\_control | metric\_test\_over\_metric\_control | metric\_test\_over\_complement | metric\_control\_over\_complement | aumann\_shapley\_attribution | apriori\_support | 貢獻 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 全部 | 0.069 | 0.071 | 0.969 | null | null | -0.00219 | 1.0 | 0.00219 |
| city=DES MOINES | 0.048 | 0.054 | 0.88 | 0.67 | 0.747 | -0.00108 | 0.08 | 0.00108 |
| vendor\_name=DIAGEO AMERICAS | 0.064 | 0.068 | 0.937 | 0.917 | 0.956 | -0.0009 | 0.184 | 0.0009 |
| vendor\_name=BACARDI USA INC | 0.071 | 0.082 | 0.857 | 1.025 | 1.167 | -0.00054 | 0.057 | 0.00054 |
| vendor\_name=PERNOD RICARD USA | 0.068 | 0.077 | 0.89 | 0.988 | 1.082 | -0.0005 | 0.061 | 0.0005 |

在輸出內容中，您可以看到資料區隔 `city=DES MOINES`
對銷售比率變化貢獻最大
。您也可以在 `metric_test` 和 `metric_control` 欄中查看這項差異，這兩欄顯示測試資料的比例低於對照組資料。其他指標 (例如 `metric_test_over_metric_control`、`metric_test_over_complement` 和 `metric_control_over_complement`) 會計算額外的統計資料，說明控制組和測試組比率之間的關係，以及這些比率與整體母體的關聯。詳情請參閱「[可加總比率指標貢獻度分析模型輸出內容](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-get-insights?hl=zh-tw#output_for_summable_ratio_metric_contribution_analysis_models)」。

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