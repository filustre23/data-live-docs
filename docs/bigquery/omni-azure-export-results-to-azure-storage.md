Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 將查詢結果匯出至 Blob 儲存體

BigQuery 可讓您使用 `EXPORT DATA` 陳述式，將對 [BigLake 資料表](https://docs.cloud.google.com/bigquery/docs/biglake-intro?hl=zh-tw)執行的查詢結果直接匯出至 Azure Blob Storage。匯出查詢結果後，您就能在外部雲端儲存空間中儲存及使用處理過的資料，不必透過 BigQuery 儲存空間移轉結果。

如要瞭解資料如何在 BigQuery 和 Azure Blob Storage 之間流動，請參閱「[匯出資料時的資料流程](https://docs.cloud.google.com/bigquery/docs/omni-introduction?hl=zh-tw#export-data)」。

## 限制

如要查看適用於 Amazon S3 和 Blob 儲存體 BigLake 資料表的完整限制清單，請參閱「[限制](https://docs.cloud.google.com/bigquery/docs/omni-introduction?hl=zh-tw#limitations)」。

## 事前準備

請確認您具備下列資源：

* [可存取 Blob 儲存體的連線](https://docs.cloud.google.com/bigquery/docs/omni-azure-create-connection?hl=zh-tw)。在連線中，您必須為要匯出的 Blob 儲存體容器路徑建立政策。然後在該政策中，建立具有 `Microsoft.Storage/storageAccounts/blobServices/containers/write` 權限的角色。
* [Blob 儲存體 BigLake 資料表](https://docs.cloud.google.com/bigquery/docs/omni-azure-create-external-table?hl=zh-tw)。

* 如果您採用[依運算資源計價模式](https://cloud.google.com/bigquery/pricing?hl=zh-tw#capacity_compute_analysis_pricing)，請務必為專案啟用 [BigQuery Reservation API](https://console.cloud.google.com/apis/library/bigqueryreservation.googleapis.com?hl=zh-tw)。如要瞭解定價，請參閱「[BigQuery Omni 定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#bqomni)」。

## 匯出查詢結果

BigQuery Omni 會寫入指定的 Blob 儲存體位置，無論是否有任何現有內容。匯出查詢可以覆寫現有資料，或將查詢結果與現有資料混合。建議您將查詢結果匯出至空白的 Blob 儲存體容器。

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在「Query editor」(查詢編輯器) 欄位中，輸入 GoogleSQL 匯出查詢：

   ```
   EXPORT DATA WITH CONNECTION \`CONNECTION_REGION.CONNECTION_NAME\`
   OPTIONS(
     uri="azure://AZURE_STORAGE_ACCOUNT_NAME.blob.core.windows.net/CONTAINER_NAME/FILE_PATH/*",
     format="FORMAT"
   )
   AS QUERY
   ```

   更改下列內容：

   * `CONNECTION_REGION`：建立連線的區域。
   * `CONNECTION_NAME`：您建立的連線名稱，具備寫入容器的必要權限。
   * `AZURE_STORAGE_ACCOUNT_NAME`：要寫入查詢結果的 Blob 儲存體帳戶名稱。
   * `CONTAINER_NAME`：要寫入查詢結果的容器名稱。
   * `FILE_PATH`：要寫入匯出檔案的路徑。路徑字串的葉目錄中必須包含一個萬用字元 `*`，例如 `../aa/*`、`../aa/b*c`、`../aa/*bc` 和 `../aa/bc*`。BigQuery 會根據匯出的檔案數量，將 `*` 替換為 `0000..N`。BigQuery 會判斷檔案數量和大小。如果 BigQuery 決定匯出兩個檔案，則第一個檔案名稱中的 `*` 會替換為 `000000000000`，第二個檔案名稱中的 `*` 則會替換為 `000000000001`。
   * `FORMAT`：支援的格式為 `JSON`、`AVRO`、`CSV` 和 `PARQUET`。
   * `QUERY`：用於分析 BigLake 資料表所儲存資料的查詢。

**注意：** 如要覆寫預設專案，請使用 `--project_id=PROJECT_ID` 參數。將 `PROJECT_ID` 替換為 Google Cloud 專案 ID。

## 疑難排解

如果收到與 `quota failure` 相關的錯誤，請檢查是否已為查詢保留運算資源。如要進一步瞭解運算單元預留項目，請參閱本文的「[事前準備](#before_you_begin)」一節。

## 後續步驟

* 瞭解 [BigQuery Omni](https://docs.cloud.google.com/bigquery/docs/omni-introduction?hl=zh-tw)。
* 瞭解如何[匯出表格資料](https://docs.cloud.google.com/bigquery/docs/exporting-data?hl=zh-tw)。
* 瞭解如何[查詢儲存在 Blob 儲存體中的資料](https://docs.cloud.google.com/bigquery/docs/query-azure-data?hl=zh-tw)。
* 瞭解如何[為 BigQuery Omni 設定 VPC Service Controls](https://docs.cloud.google.com/bigquery/docs/omni-vpc-sc?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-10-29 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-10-29 (世界標準時間)。"],[],[]]