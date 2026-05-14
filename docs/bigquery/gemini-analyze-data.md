Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 在 Gemini 協助下分析資料

本教學課程說明如何使用 [Gemini in BigQuery](https://docs.cloud.google.com/bigquery/docs/gemini-overview?hl=zh-tw) 的 AI 輔助功能分析資料。

以本教學課程的範例來說，假設您是資料分析師，需要分析資料集並預測產品銷售量。

本教學課程假設您熟悉 SQL 和基本的資料分析工作，但不必具備 Google Cloud 產品知識。如果您剛開始使用 BigQuery，請參考 [BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts?hl=zh-tw)。

## 目標

* 使用 Gemini in BigQuery 回答有關 BigQuery 如何處理特定資料分析工作的問題。
* 運用提示詞，讓 Gemini in BigQuery 尋找資料集，並說明及生成 SQL 查詢。
* 建構機器學習 (ML) 模型，預測未來週期。

## 費用

本教學課程使用下列可計費 Google Cloud 產品：

* [BigQuery](https://cloud.google.com/bigquery/pricing?hl=zh-tw)
* [BigQuery ML](https://cloud.google.com/bigquery/pricing?hl=zh-tw#bqml)

如要根據預測用量估算費用，請使用 [Pricing Calculator](https://cloud.google.com/products/calculator?hl=zh-tw)。

## 事前準備

1. 在 Google Cloud 控制台的專案選擇器頁面中，選取或建立 Google Cloud 專案。

   **選取或建立專案所需的角色**

   * **選取專案**：選取專案時，不需要具備特定 IAM 角色，只要您已獲授角色，即可選取任何專案。
   * **建立專案**：如要建立專案，您需要具備專案建立者角色 (`roles/resourcemanager.projectCreator`)，其中包含 `resourcemanager.projects.create` 權限。[瞭解如何授予角色](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)。
   **注意**：如果您不打算保留在這項程序中建立的資源，請建立新專案，而不要選取現有專案。完成這些步驟後，您就可以刪除專案，並移除與該專案相關聯的所有資源。

   [前往專案選取器](https://console.cloud.google.com/projectselector2/home/dashboard?hl=zh-tw)
2. [確認已為 Google Cloud 專案設定 Gemini 版 BigQuery](https://docs.cloud.google.com/bigquery/docs/gemini-set-up?hl=zh-tw)。
3. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
4. [建立名為 `bqml_tutorial` 的資料集](https://docs.cloud.google.com/bigquery/docs/datasets?hl=zh-tw)。您可以使用資料集儲存資料庫物件，包括資料表和模型。
5. 如要開啟完成本教學課程所需的 Gemini in BigQuery 功能，請在 BigQuery 工具列中，依序點選「pen\_spark」pen\_spark**Gemini**「Gemini」，然後選取下列選項：

   * **自動完成**
   * **自動生成**
   * **說明**

## 瞭解 BigQuery 功能

開始之前，請先瞭解 BigQuery 如何處理資料查詢。如需說明，可以向 Gemini in BigQuery 傳送自然語言陳述式 (即*提示詞*)，例如：

* 「如何開始使用 BigQuery？」
* 「將 BigQuery 用於資料分析的好處為何？」
* 「BigQuery 如何針對查詢自動調整資源配置？」

Gemini in BigQuery 也能提供資料分析方式的相關資訊。如需這類協助，您可以傳送下列提示：

* 「如何在 BigQuery 中建立時間序列預測模型？」
* 「如何將不同類型的資料載入 BigQuery？」

## 存取及分析資料

Gemini for Google Cloud產品仍處於早期技術階段，因此可能會生成看似合理卻與事實不符的輸出內容。使用輸出內容前，請一律確認 Gemini for Google Cloud 產品輸出內容是否屬實。詳情請參閱「[Gemini for Google Cloud 和負責任的 AI 技術](https://docs.cloud.google.com/gemini/docs/discover/responsible-ai?hl=zh-tw)」。

Gemini in BigQuery 可協助您瞭解可存取哪些資料進行分析，以及如何分析這些資料。

在這個範例中，假設您需要以下方面的協助：

* 尋找要分析的銷售資料集和資料表。
* 瞭解銷售資料集內資料表和查詢的關聯。
* 瞭解複雜查詢，並撰寫使用資料集的查詢。

### 尋找資料

開始查詢資料前，您需要知道自己可存取哪些資料。每種資料產品整理和儲存資料的方式不盡相同。

如需說明，可以向 Gemini in BigQuery 傳送提示詞，例如「如何得知我可以在 BigQuery 使用哪些資料集和資料表？」

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在 Google Cloud 控制台工具列，點選「spark」「開啟或關閉 Gemini Cloud Assist 對話」。
3. 在「Cloud Assist」面板中輸入提示 `How do I learn which
   datasets and tables are available to me in BigQuery?`。
4. 點選「傳送提示詞」按鈕 send。

   瞭解 [Gemini for Google Cloud 如何使用您的資料](https://docs.cloud.google.com/gemini/docs/discover/data-governance?hl=zh-tw)。

   回應中包含列出專案、資料集或資料集內資料表的多種方式。
5. 選用：如要重設對話記錄，請在「Cloud Assist」面板中，依序點選 delete「清除對話」和「重設對話」。

   **注意：** 對話記錄狀態只會保存在記憶體，您切換至其他工作區或關閉 Google Cloud 控制台後，系統不會保留這類資料。

### 瞭解及編寫 BigQuery 中的 SQL

以這個範例來說，假設您已選取要分析的資料，現在要查詢該資料。Gemini in BigQuery 可協助您處理 SQL，無論是瞭解複雜且難以剖析的查詢，還是生成新的 SQL 查詢，都能派上用場。

#### 提示 Gemini 說明 SQL 查詢

假設您想瞭解他人撰寫的複雜查詢。
Gemini in BigQuery 可以用簡單易懂的語言說明查詢，例如查詢語法、基礎結構定義和業務情境。

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中，開啟或貼上您想要 Gemini 說明的查詢。
   例如：

   ```
   SELECT
     u.id AS user_id,
     u.first_name,
     u.last_name,
     avg(oi.sale_price) AS avg_sale_price
   FROM `bigquery-public-data.thelook_ecommerce.users` AS u
   JOIN `bigquery-public-data.thelook_ecommerce.order_items` AS oi
     ON u.id = oi.user_id
   GROUP BY 1, 2, 3
   ORDER BY avg_sale_price DESC
   LIMIT 10
   ```
3. 醒目顯示查詢，然後按一下「auto\_awesome
   說明所選的這項查詢」。

   **Cloud Assist** 面板會傳回類似以下的回應：

   ```
   The intent of this query is to find the top 10 users by average sale price.
   The query first joins the users and order_items tables on the user_id
   column. It then groups the results by user_id, first_name, and last_name,
   and calculates the average sale price for each group. The results are then
   ordered by average sale price in descending order, and the top 10 results
   are returned.
   ```

#### 產生 SQL 查詢，根據日期和產品分類銷售資料

在這個範例中，您要產生查詢，列出每天的熱銷產品。接著，您可以使用 `thelook_ecommerce` 資料集內的資料表，透過提示讓 BigQuery 中的 Gemini 產生查詢，根據訂單產品和產品名稱計算銷售量。

這類查詢通常很複雜，但您可以使用 Gemini in BigQuery 自動建立陳述式。您可以使用提示詞，要求 Gemini 根據資料結構定義產生 SQL 查詢。即使您未編寫程式碼、不太瞭解資料結構定義，或只具備 SQL 語法的基礎知識，Gemini 輔助功能都可以建議一或多個 SQL 陳述式。

如要提示 Gemini in BigQuery 生成查詢，列出熱門產品，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在導覽選單中，按一下「Studio」。
3. 按一下「SQL 查詢」add\_box。
   「探索工具」窗格會自動載入所選資料庫。
4. 在查詢編輯器中輸入下列提示，然後按下 `Enter` 鍵：

   ```
   # select the sum of sales by date and product casted to day from bigquery-public-data.thelook_ecommerce.order_items joined with bigquery-public-data.thelook_ecommerce.products
   ```

   井字 (`#`) 字元會提示 Gemini in BigQuery 產生 SQL。Gemini in BigQuery 會提供類似下列內容的 SQL 查詢建議：

   ```
   SELECT
     sum(sale_price),
     DATE(created_at),
     product_id
   FROM
     `bigquery-public-data.thelook_ecommerce.order_items`
       AS t1
   INNER JOIN `bigquery-public-data.thelook_ecommerce.products` AS t2
     ON t1.product_id = t2.id
   GROUP BY 2, 3
   ```

   **注意：** Gemini in BigQuery 可能會針對提示建議多個 SQL 陳述式。
5. 如要接受建議的程式碼，請按下 **Tab** 鍵並點按「執行」，開始執行 SQL 陳述式。您也可以捲動瀏覽建議的 SQL 程式碼，接受陳述式中建議的特定字詞。
6. 在「查詢結果」窗格，檢視查詢結果。

## 建構預測模型並查看結果

在本範例中，您會使用 BigQuery ML 執行下列操作：

* 使用趨勢查詢建構預測模型。
* 使用 Gemini in BigQuery 說明及協助您撰寫查詢，以查看預測模型的結果。

您將搭配使用以下範例查詢與實際銷售資料，這類資料會輸入至模型。查詢會用來建立機器學習模型。

1. 如要建立機器學習預測模型，請在查詢編輯器中執行下列 SQL 查詢：

   ```
   CREATE MODEL bqml_tutorial.sales_forecasting_model
     OPTIONS (
       MODEL_TYPE = 'ARIMA_PLUS',
       time_series_timestamp_col = 'date_col',
       time_series_data_col = 'total_sales',
       time_series_id_col = 'product_id')
   AS
   SELECT
     sum(sale_price) AS total_sales,
     DATE(created_at) AS date_col,
     product_id
   FROM
     `bigquery-public-data.thelook_ecommerce.order_items`
       AS t1
   INNER JOIN `bigquery-public-data.thelook_ecommerce.products` AS t2
     ON t1.product_id = t2.id
   GROUP BY 2, 3;
   ```

   您可以使用 Gemini in BigQuery [瞭解這項查詢](#prompt-gemini-explain-sql-queries)。

   **注意：** 模型執行期間，您也可以在 **Cloud Assist** 面板中，使用 `What is an ARIMA_PLUS model type?` 等問題提示 BigQuery 中的 Gemini。

   模型建立後，「查詢結果」窗格的「結果」分頁會顯示類似以下的訊息：

   ```
   Successfully created model named sales_forecasting_model.
   ```
2. 在「Cloud Assist」面板中輸入提示，讓 Gemini in BigQuery 協助撰寫查詢，在模型完成時取得預測結果。舉例來說，輸入 `How can I get a forecast in SQL from the model?`

   根據提示的上下文，回覆會包含預測銷售情形的機器學習模型範例：

   ```
   SELECT
     *
   FROM
     ML.FORECAST(
       MODEL `PROJECT_ID.bqml_tutorial.sales_forecasting_model`,
       STRUCT(
         7 AS horizon,
         0.95 AS confidence_level))
   ```

   在此回應中，`PROJECT_ID` 是您的Google Cloud 專案。

   **注意：** Gemini in BigQuery 會使用即時通訊工作階段的內容，協助回答同一工作階段中的問題。
3. 在「Cloud Assist」面板中，複製 SQL 查詢。
4. 在查詢編輯器中執行 SQL 查詢。

## 清除所用資源

如要避免系統向您的 Google Cloud 帳戶收取本教學課程所用資源的費用，請刪除您為本教學課程建立的 Google Cloud 專案。或者，您也可以刪除個別資源。

### 刪除專案

**注意**：刪除專案會造成以下結果：

* **專案中的所有內容都會遭到刪除。**如果使用現有專案來進行本文中的任務，刪除專案將一併移除當中已完成的其他任務'。
* **自訂專案 ID 會消失。**當您之前建立這個專案時，可能建立了想要在日後使用的自訂專案 ID。如要保留使用該專案 ID 的網址 (例如 `appspot.com` 網址)，請刪除在該專案中選取的資源，而不是刪除整個專案。

如果打算探索多種架構、教學課程或快速入門導覽課程，重複使用專案可避免超出專案配額限制。

1. 前往 Google Cloud 控制台的「Manage resources」(管理資源) 頁面。

   [前往「Manage resources」(管理資源)](https://console.cloud.google.com/iam-admin/projects?hl=zh-tw)
2. 在專案清單中選取要刪除的專案，然後點選「Delete」(刪除)。
3. 在對話方塊中輸入專案 ID，然後按一下 [Shut down] (關閉) 以刪除專案。

### 刪除資料集

刪除專案將移除專案中所有的資料集與資料表。若您希望重新使用專案，可以刪除本教學課程中所建立的資料集。

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在導覽選單中，選取您建立的 **`bqml_tutorial`** 資料集。
3. 如要刪除資料集、資料表和所有資料，請按一下「刪除資料集」。
4. 如要確認刪除，請在「Delete dataset」(刪除資料集) 對話方塊中輸入資料集名稱 (`bqml_tutorial`)，然後按一下「Delete」(刪除)。

## 後續步驟

* 閱讀 [Gemini for Google Cloud 總覽](https://docs.cloud.google.com/gemini/docs/overview?hl=zh-tw)。
* 瞭解 [Gemini for Google Cloud 的配額與限制](https://docs.cloud.google.com/gemini/docs/quotas?hl=zh-tw)。
* 瞭解 [Gemini for Google Cloud](https://docs.cloud.google.com/gemini/docs/locations?hl=zh-tw) 的適用國家/地區。
* 瞭解如何[生成資料洞察以探索資料](https://docs.cloud.google.com/bigquery/docs/data-insights?hl=zh-tw)。
* 進一步瞭解如何[在 BigQuery 中透過 Gemini 輔助撰寫查詢](https://docs.cloud.google.com/bigquery/docs/write-sql-gemini?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-14 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-14 (世界標準時間)。"],[],[]]