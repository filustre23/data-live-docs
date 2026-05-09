Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 使用可相加的指標，從貢獻度分析模型取得資料洞察

在本教學課程中，您將使用[貢獻度分析](https://docs.cloud.google.com/bigquery/docs/contribution-analysis?hl=zh-tw)模型，分析愛荷華州酒類銷售資料集中 2020 年和 2021 年的銷售變化。本教學課程會逐步引導您完成下列工作：

* 根據愛荷華州公開酒類資料建立輸入資料表。
* 建立使用[可相加指標](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-contribution-analysis?hl=zh-tw#use_a_summable_metric)的[貢獻度分析模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-contribution-analysis?hl=zh-tw)。這類模型會針對資料中一或多個維度的組合，匯總特定指標，藉此判斷這些維度對指標值的影響。
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

建立包含測試和控制項資料的資料表，以供分析。測試資料表包含 2021 年的酒類資料，控制組資料表則包含 2020 年的酒類資料。下列查詢會將測試和控制組資料合併為單一輸入資料表：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中執行下列陳述式：

   ```
   CREATE OR REPLACE TABLE bqml_tutorial.iowa_liquor_sales_sum_data AS (
     (SELECT
       store_name,
       city,
       vendor_name,
       category_name,
       item_description,
       SUM(sale_dollars) AS total_sales,
       FALSE AS is_test
     FROM `bigquery-public-data.iowa_liquor_sales.sales`
     WHERE EXTRACT(YEAR from date) = 2020
     GROUP BY store_name, city, vendor_name, category_name, item_description, is_test)
     UNION ALL
     (SELECT
       store_name,
       city,
       vendor_name,
       category_name,
       item_description,
       SUM(sale_dollars) AS total_sales,
       TRUE AS is_test
     FROM `bigquery-public-data.iowa_liquor_sales.sales`
     WHERE EXTRACT (YEAR FROM date) = 2021
     GROUP BY store_name, city, vendor_name, category_name, item_description, is_test)
   );
   ```

## 建立模型

建立貢獻分析模型：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中執行下列陳述式：

   ```
   CREATE OR REPLACE MODEL bqml_tutorial.iowa_liquor_sales_sum_model
     OPTIONS(
       model_type='CONTRIBUTION_ANALYSIS',
       contribution_metric = 'sum(total_sales)',
       dimension_id_cols = ['store_name', 'city', 'vendor_name', 'category_name',
         'item_description'],
       is_test_col = 'is_test',
       min_apriori_support=0.05
     ) AS
   SELECT * FROM bqml_tutorial.iowa_liquor_sales_sum_data;
   ```

查詢作業完成 (約需 60 秒) 後，模型 `iowa_liquor_sales_sum_model` 會顯示在 `bqml_tutorial` 資料集中。由於查詢是使用 `CREATE MODEL` 陳述式建立模型，因此不會有查詢結果。

## 從模型中取得洞察資料

使用 `ML.GET_INSIGHTS` 函式，取得貢獻度分析模型產生的洞察資料。

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中，執行下列陳述式，從[可加總指標貢獻度分析模型輸出內容](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-get-insights?hl=zh-tw#output_for_summable_metric_contribution_analysis_models)中選取資料欄：

   ```
   SELECT
     contributors,
     metric_test,
     metric_control,
     difference,
     relative_difference,
     unexpected_difference,
     relative_unexpected_difference,
     apriori_support,
     contribution
   FROM
     ML.GET_INSIGHTS(
       MODEL `bqml_tutorial.iowa_liquor_sales_sum_model`);
   ```

輸出內容的前幾列應如下所示：為提升可讀性，系統會截斷值。

| 貢獻者 | metric\_test | metric\_control | 差異 | relative\_difference | unexpected\_difference | relative\_unexpected\_difference | apriori\_support | 貢獻 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 全部 | 428068179 | 396472956 | 31595222 | 0.079 | 31595222 | 0.079 | 1.0 | 31595222 |
| vendor\_name=SAZERAC COMPANY INC | 52327307 | 38864734 | 13462573 | 0.346 | 11491923 | 0.281 | 0.122 | 13462573 |
| city=DES MOINES | 49521322 | 41746773 | 7774549 | 0.186 | 4971158 | 0.111 | 0.115 | 7774549 |
| vendor\_name=DIAGEO AMERICAS | 84681073 | 77259259 | 7421814 | 0.096 | 1571126 | 0.018 | 0.197 | 7421814 |
| category\_name=100% AGAVE TEQUILA | 23915100 | 17252174 | 6662926 | 0.386 | 5528662 | 0.3 | 0.055 | 6662926 |

輸出內容會自動依貢獻度 (或 `ABS(difference)`) 遞減排序。在 `all` 列中，「`difference`」欄顯示 2020 年至 2021 年的總銷售額增加了 $31,595,222 美元，如「`relative_difference`」欄所示，增幅為 7.9%。在第二列中，`vendor_name=SAZERAC COMPANY INC`為 $11,491,923，`unexpected_difference`表示這個資料區隔的成長率比整體資料的成長率高出 28%，如 `relative_unexpected_difference` 欄所示。詳情請參閱「[可加總的指標輸出資料欄](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-get-insights?hl=zh-tw#output_for_summable_metric_contribution_analysis_models)」。

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

上次更新時間：2026-05-08 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-08 (世界標準時間)。"],[],[]]