Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 將查詢結果匯出至檔案

您可以將 BigQuery 查詢結果儲存至本機檔案、Google 雲端硬碟、Google 試算表或 Cloud Storage，以便分享結果或在其他工具中分析。如果是本機檔案，您可以選擇 CSV 和以換行符號分隔的 JSON 等格式。

## 限制

BigQuery 不支援將巢狀或重複資料 (`RECORD` / `STRUCT` 或 `ARRAY` 資料類型) 匯出為 CSV 格式。即使 `RECORD` 或 `STRUCT` 欄位看起來並非深度巢狀，BigQuery 仍會將其視為巢狀結構定義欄位，並傳回錯誤，指出結構定義無法巢狀。

如要將查詢結果匯出為結構化 CSV 檔案，必須將查詢正規化為平面結構，每個查詢資料欄一個欄位。您可以使用點標記法選取個別欄位，藉此正規化巢狀結構，或使用 `UNNEST` 運算子正規化重複陣列。

舉例來說，如果資料表包含 struct `customer` 和陣列 `items`，請先將查詢正規化，再執行並將結果儲存為 CSV：

```
SELECT
  customer.id AS customer_id,
  customer.name AS customer_name,
  item
FROM
  `my_project.my_dataset.my_table`,
  UNNEST(items) AS item;
```

## 將查詢結果下載至本機檔案

bq 指令列工具或 API 不支援將查詢結果下載至本機檔案。

如要將查詢結果下載為 CSV 或以換行符號分隔的 JSON 檔案，請使用Google Cloud 控制台：

1. 在 Google Cloud 控制台開啟「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 按一下「add\_box SQL 查詢」。
3. 在「查詢編輯器」文字區域中，輸入有效的 GoogleSQL 查詢。
4. (選用) 如要變更處理位置，請依序點選「Edit」(編輯) >「Query settings」(查詢設定)。在「Data location」(資料位置) 部分，選擇資料的[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)。
5. 按一下「執行」。
6. 傳回結果後，按一下「Save results」(儲存結果)，然後選取要儲存結果的格式或位置。

   檔案會下載至瀏覽器的預設下載位置。

## 將查詢結果儲存至 Google 雲端硬碟

**Beta 版**

這項功能適用《[服務專屬條款](https://docs.cloud.google.com/terms/service-terms?hl=zh-tw#1)》中「一般服務條款」一節的《正式發布前產品條款》。正式發布前功能是依「原樣」提供，支援服務可能受限。
詳情請參閱[推出階段說明](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages)。

bq 指令列工具或 API 不支援將查詢結果儲存至 Google 雲端硬碟。

嘗試將 BigQuery 結果儲存至 Google 雲端硬碟時，可能會發生錯誤。這項錯誤是因為 Drive SDK API 無法存取 Google Workspace。如要解決這個問題，您必須允許使用者帳戶透過 Drive SDK API [存取 Google 雲端硬碟](https://support.google.com/a/answer/6105699?hl=zh-tw)。

如要將查詢結果儲存至 Google 雲端硬碟，請使用 Google Cloud 控制台：

1. 在 Google Cloud 控制台開啟「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 按一下「add\_box SQL 查詢」。
3. 在「查詢編輯器」文字區域中，輸入有效的 GoogleSQL 查詢。
4. 按一下「執行」。
5. 傳回結果後，按一下「儲存結果」。
6. 在「Google 雲端硬碟」下方，選取「CSV」或「JSON」。將結果儲存至 Google 雲端硬碟時，您無法選擇位置。結果一律會儲存至「我的雲端硬碟」根目錄。
7. 系統可能需要幾分鐘的時間，才能將結果儲存至 Google 雲端硬碟。結果儲存後，您會收到對話方塊訊息，其中包含檔案名稱 `bq-results-[TIMESTAMP]-[RANDOM_CHARACTERS].[CSV or JSON]`。
8. 在對話方塊訊息中，按一下 **開啟** 開啟檔案，或前往 Google 雲端硬碟，然後按一下 **我的雲端硬碟**。

## 將查詢結果儲存至 Google 試算表

bq 指令列工具或 API 不支援將查詢結果儲存至 Google 試算表。

嘗試從 Google 試算表開啟 BigQuery 結果時，可能會發生錯誤。這項錯誤是因為 Drive SDK API 無法存取 Google Workspace。如要解決這個問題，您必須啟用使用者帳戶，才能透過 Drive SDK API [存取 Google 試算表](https://support.google.com/a/answer/6105699?hl=zh-tw)。

如要將查詢結果儲存至 Google 試算表，請使用 Google Cloud 控制台：

1. 在 Google Cloud 控制台開啟「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 按一下「add\_box SQL 查詢」。
3. 在「查詢編輯器」文字區域中，輸入有效的 GoogleSQL 查詢。
4. (選用) 如要變更處理位置，請依序點選「Edit」(編輯) >「Query settings」(查詢設定)。在「Data location」(資料位置)**部分，選擇資料的[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)。**
5. 按一下「執行」。
6. 傳回結果時，按一下 [Save results] (儲存結果) 並選取 [Google Sheets] (Google 試算表)。
7. 如有必要，請按照提示登入使用者帳戶，然後按一下「Allow」(允許)，授予 BigQuery 將資料寫入 Google 雲端硬碟 `My Drive` 資料夾的權限。

   按照提示操作後，您應該會收到一封電子郵件，確認 BigQuery 用戶端工具已連結至您的使用者帳戶。電子郵件會列出您授予的權限，以及移除權限的步驟。
8. 儲存結果後， Google Cloud 控制台的查詢結果下方會顯示類似以下的訊息：`Saved to Sheets as
   "results-20190225-103531"`。按一下訊息中的連結，即可在 Google 試算表中查看結果，或前往 `My Drive` 資料夾並手動開啟檔案。

   將查詢結果儲存至 Google 試算表時，檔案名稱會以 `results-[DATE]` 開頭，其中 `[DATE]` 是當天日期，格式為 `YYYYMMDD`。

   **注意：** bq 指令列工具或 API 不支援將結果儲存至 Google 試算表。詳情請參閱「[使用連結試算表](https://docs.cloud.google.com/bigquery/docs/connected-sheets?hl=zh-tw)」。

### 排解將結果儲存至 Google 試算表的問題

將資料從 BigQuery 儲存至 Google 試算表時，您可能會發現試算表中的某些儲存格是空白的。如果寫入儲存格的資料超過 Google 試算表的 50,000 個字元限制，就會發生這種情況。如要解決這個問題，請在 GoogleSQL 查詢中使用[字串函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/string_functions?hl=zh-tw#split)，將含有長資料的資料欄分割成兩個以上的資料欄，然後再次將結果儲存至試算表。

## 將查詢結果儲存至 Cloud Storage

您可以按照下列步驟，在 Google Cloud 控制台中將查詢結果匯出至 Cloud Storage：

1. 在 Google Cloud 控制台開啟「BigQuery」頁面。

   [前往「BigQuery」頁面](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 按一下「add\_box SQL 查詢」。
3. 在「查詢編輯器」文字區域中，輸入有效的 GoogleSQL 查詢。
4. 按一下「執行」。
5. 傳回結果後，依序點選「儲存結果」>「Cloud Storage」。
6. 在「Export to Google Storage」(匯出至 Google Cloud Storage) 對話方塊中：

   * 在「GCS Location」(GCS 位置)，瀏覽要匯出資料的值區、資料夾或檔案。
   * 在「Export format」(匯出格式)，選擇匯出資料的格式：CSV、JSON (以換行符號分隔)、Avro 或 Parquet。
   * 在「Compression」(壓縮) 部分，選取壓縮格式，或選取 `None` 表示不壓縮。
7. 按一下「儲存」，匯出查詢結果。

如要查看工作進度，請展開「Job history」(工作記錄) 窗格，然後尋找類型為 `EXTRACT` 的工作。

## 限制下載查詢結果

如要禁止使用者從 Google Cloud 控制台下載查詢結果，請採用下列任一方法：

* 設定 [VPC Service Controls](https://docs.cloud.google.com/vpc-service-controls/docs/overview?hl=zh-tw) perimeter，防止資料竊取。這可防止使用者在既定範圍邊界外下載及匯出資料。
* 請與 [Cloud Customer Care](https://docs.cloud.google.com/support?hl=zh-tw) 聯絡，要求將 Google Cloud 專案或組織加入受限清單。這會直接在 Google Cloud 控制台中停用資料下載和匯出選項。

## 後續步驟

* 瞭解如何透過程式輔助方式[將資料表匯出為 JSON 檔案](https://docs.cloud.google.com/bigquery/docs/samples/bigquery-extract-table-json?hl=zh-tw)。
* 瞭解[擷取工作的配額](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#export_jobs)。
* 瞭解 [BigQuery 儲存空間定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#storage)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-10-29 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-10-29 (世界標準時間)。"],[],[]]