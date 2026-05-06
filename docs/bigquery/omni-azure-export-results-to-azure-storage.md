Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 將查詢結果匯出至 Blob 儲存體

本文說明如何將針對 [BigLake 資料表](https://docs.cloud.google.com/bigquery/docs/biglake-intro?hl=zh-tw)執行的查詢結果匯出至 Azure Blob 儲存體。

如要瞭解 BigQuery 和 Azure Blob Storage 之間的資料流動方式，請參閱「[匯出資料時的資料流動](https://docs.cloud.google.com/bigquery/docs/omni-introduction?hl=zh-tw#export-data)」。

## 限制

如需適用於 Amazon S3 和 Blob 儲存體 BigLake 資料表的完整限制清單，請參閱「[限制](https://docs.cloud.google.com/bigquery/docs/omni-introduction?hl=zh-tw#limitations)」。

## 事前準備

請確認您已備妥下列資源：

* [Blob 儲存體存取權連線](https://docs.cloud.google.com/bigquery/docs/omni-azure-create-connection?hl=zh-tw)。在連線中，您必須為要匯出的 Blob 儲存體容器路徑建立政策。接著，在該政策中建立具有 `Microsoft.Storage/storageAccounts/blobServices/containers/write` 權限的角色。
* [Blob 儲存空間 BigLake 資料表](https://docs.cloud.google.com/bigquery/docs/omni-azure-create-external-table?hl=zh-tw)。

* 如果您採用[容量定價模式](https://cloud.google.com/bigquery/pricing?hl=zh-tw#capacity_compute_analysis_pricing)，請確認您已為專案啟用 [BigQuery Reservation API](https://console.cloud.google.com/apis/library/bigqueryreservation.googleapis.com?hl=zh-tw)。如要瞭解價格，請參閱 [BigQuery Omni 定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#bqomni)。

## 匯出查詢結果

無論現有內容為何，BigQuery Omni 都會寫入指定的 Blob 儲存體位置。匯出查詢可以覆寫現有資料，或將查詢結果與現有資料混合。建議您將查詢結果匯出至空 Blob 儲存體容器。

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往 BigQuery](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在「Query editor」(查詢編輯器) 欄位中輸入 GoogleSQL 匯出查詢：

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
   * `CONNECTION_NAME`：您建立的連線名稱，具有寫入容器的必要權限。
   * `AZURE_STORAGE_ACCOUNT_NAME`：您要寫入查詢結果的 Blob 儲存體帳戶名稱。
   * `CONTAINER_NAME`：您要寫入查詢結果的容器名稱。
   * `FILE_PATH`：您要將匯出檔案寫入的路徑。路徑字串的葉目錄中必須包含正確的萬用字元 `*`，例如 `../aa/*`、`../aa/b*c`、`../aa/*bc` 和 `../aa/bc*`。視匯出的檔案數量而定，BigQuery 會將 `*` 替換為 `0000..N`。BigQuery 會決定檔案數量和大小。如果 BigQuery 決定匯出兩個檔案，則第一個檔案的檔案名稱中的 `*` 會替換為 `000000000000`，第二個檔案的檔案名稱中的 `*` 會替換為 `000000000001`。
   * `FORMAT`：支援的格式為 `JSON`、`AVRO`、`CSV` 和 `PARQUET`。
   * `QUERY`：用於分析 BigLake 資料表中儲存的資料的查詢。

**注意：** 如要覆寫預設專案，請使用 `--project_id=PROJECT_ID` 參數。將 `PROJECT_ID` 替換為您的 Google Cloud 專案 ID。

## 疑難排解

如果您收到與 `quota failure` 相關的錯誤訊息，請檢查是否已為查詢保留容量。如要進一步瞭解時段預留功能，請參閱本文件的[事前準備](#before_you_begin)。

## 後續步驟

* 瞭解 [BigQuery Omni](https://docs.cloud.google.com/bigquery/docs/omni-introduction?hl=zh-tw)。
* 瞭解如何[匯出資料表資料](https://docs.cloud.google.com/bigquery/docs/exporting-data?hl=zh-tw)。
* 瞭解如何[查詢儲存在 Blob 儲存體中的資料](https://docs.cloud.google.com/bigquery/docs/query-azure-data?hl=zh-tw)。
* 瞭解如何[為 BigQuery Omni 設定 VPC Service Controls](https://docs.cloud.google.com/bigquery/docs/omni-vpc-sc?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-06 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-06 (世界標準時間)。"],[],[]]