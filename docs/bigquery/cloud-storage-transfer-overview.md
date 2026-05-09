Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [參考資料](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# Cloud Storage 移轉簡介

Cloud Storage 專用的 [BigQuery 資料移轉服務](https://docs.cloud.google.com/bigquery/docs/dts-introduction?hl=zh-tw)可讓您安排從 [Cloud Storage 值區](https://docs.cloud.google.com/storage/docs/buckets?hl=zh-tw)到 BigQuery 的週期性資料載入工作。Cloud Storage 中儲存資料的路徑和目的地資料表皆可[參數化](https://docs.cloud.google.com/bigquery/docs/gcs-transfer-parameters?hl=zh-tw)，讓您依日期順序從 Cloud Storage 值區載入資料。

## 支援的檔案格式

BigQuery 資料移轉服務支援透過下列格式從 Cloud Storage 載入資料：

* 逗號分隔值 (CSV)
* JSON (以換行符號分隔)
* Avro
* Parquet
* ORC

## 支援的壓縮類型

Cloud Storage 專用的 BigQuery 資料移轉服務支援載入壓縮資料。BigQuery 資料移轉服務支援的壓縮類型和 BigQuery 載入工作支援的相同。詳情請參閱[載入壓縮與未壓縮資料](https://docs.cloud.google.com/bigquery/docs/batch-loading-data?hl=zh-tw#loading_compressed_and_uncompressed_data)。

## Cloud Storage 移轉的資料擷取作業

[設定 Cloud Storage 移轉作業](https://docs.cloud.google.com/bigquery/docs/cloud-storage-transfer?hl=zh-tw#set_up_a_cloud_storage_transfer)時，您可以在移轉設定中選取「寫入偏好設定」，指定資料載入 BigQuery 的方式。

寫入偏好設定有兩種：[增量轉移](#incremental_transfers)和[截斷轉移](#truncated_transfers)。

### 增量移轉

如果移轉設定採用 **`APPEND`** 或 **`WRITE_APPEND`** 寫入偏好設定 (也稱為增量移轉)，系統會將上次成功移轉後的新資料，增量附加至 BigQuery 目的地資料表。如果移轉設定以 **`APPEND`** 寫入偏好設定執行，BigQuery 資料移轉服務會篩選出上次成功執行移轉作業後修改的檔案。為判斷檔案的修改時間，BigQuery 資料移轉服務會查看檔案中繼資料的「上次修改時間」屬性。舉例來說，BigQuery 資料移轉服務會查看 Cloud Storage 檔案中的 [`updated` 時間戳記屬性](https://docs.cloud.google.com/storage/docs/metadata?hl=zh-tw#timestamps)。如果 BigQuery 資料移轉服務發現任何「上次修改時間」晚於上次成功移轉時間戳記的檔案，就會透過增量移轉作業移轉這些檔案。

為示範增量轉移的運作方式，請參考下列 Cloud Storage 轉移範例。使用者在 2023 年 7 月 1 日 00:00 (UTC) 於 Cloud Storage bucket 中建立名為 `file_1` 的檔案。`file_1` 的[`updated`時間戳記](https://docs.cloud.google.com/storage/docs/metadata?hl=zh-tw#timestamps)是檔案的建立時間。接著，使用者從 Cloud Storage bucket 建立增量移轉作業，並排定從 2023-07-01T03:00Z 開始，每天在 03:00Z 執行一次。

* 第一次轉移作業會在 2023 年 7 月 1 日 03:00 (UTC) 開始。由於這是這項設定的首次移轉作業，BigQuery 資料移轉服務會嘗試將符合來源 URI 的所有檔案載入目的地 BigQuery 資料表。移轉作業成功執行，且 BigQuery 資料移轉服務已將 `file_1` 載入目的地 BigQuery 資料表。
* 下一次轉移作業 (2023-07-02T03:00Z) 偵測到沒有任何檔案的 `updated` 時間戳記屬性大於上次成功轉移作業 (2023-07-01T03:00Z)。移轉作業會順利完成，但不會將任何額外資料載入目的地 BigQuery 資料表。

上例說明 BigQuery 資料移轉服務如何查看來源檔案的 `updated` 時間戳記屬性，判斷來源檔案是否經過變更，並在偵測到變更時轉移這些變更。

沿用上述範例，假設使用者隨後在 2023 年 7 月 3 日 00:00 (UTC) 於 Cloud Storage bucket 中建立另一個名為 `file_2` 的檔案。`file_2` 的[`updated`時間戳記](https://docs.cloud.google.com/storage/docs/metadata?hl=zh-tw#timestamps)是檔案的建立時間。

* 下一次轉移作業 (2023-07-03T03:00Z) 會偵測到 `file_2` 的 `updated` 時間戳記大於上次成功轉移作業 (2023-07-01T03:00Z)。假設轉移作業開始時，因暫時性錯誤而失敗。在此情況下，`file_2` 不會載入至目的地 BigQuery 資料表。上次成功執行資料移轉的時間戳記仍為 2023-07-01T03:00Z。
* 下一次轉移作業 (2023-07-04T03:00Z) 會偵測到 `file_2` 的 `updated` 時間戳記大於上次成功轉移作業 (2023-07-01T03:00Z)。這次移轉作業順利完成，因此 `file_2` 成功載入目的地 BigQuery 資料表。
* 下一次移轉作業 (2023-07-05T03:00Z) 偵測不到任何檔案，因為 `updated` 時間戳記大於上次成功移轉作業 (2023-07-04T03:00Z)。移轉作業會成功完成，但不會將任何額外資料載入目的地 BigQuery 資料表。

上例顯示，如果移轉失敗，系統不會將任何檔案移轉至 BigQuery 目的地資料表。下次成功傳輸時，系統會傳輸所有檔案變更。如果轉移失敗，後續成功轉移的資料不會重複。如果移轉失敗，您也可以選擇在定期排定時間以外[手動觸發移轉](https://docs.cloud.google.com/bigquery/docs/working-with-transfers?hl=zh-tw#manually_trigger_a_transfer)。

**警告：** BigQuery 資料移轉服務會根據每個來源檔案的「上次修改時間」屬性，判斷要移轉哪些檔案，如增量移轉範例所示。修改這些屬性可能會導致轉移作業略過特定檔案，或多次載入相同檔案。在 BigQuery 資料移轉服務支援的每個儲存系統中，這個屬性可以有不同的名稱。舉例來說，Cloud Storage 物件會將這項屬性稱為 [`updated`](https://docs.cloud.google.com/storage/docs/metadata?hl=zh-tw#timestamps)。

### 截斷的轉移作業

如果移轉設定採用 **`MIRROR`** 或 **`WRITE_TRUNCATE`** 寫入偏好設定 (也稱為截斷式移轉)，則每次執行移轉作業時，系統都會使用符合來源 URI 的所有檔案資料，覆寫 BigQuery 目的地資料表中的資料。**`MIRROR`** 會覆寫目的地資料表中的最新資料副本。如果目的地資料表使用分區修飾符，轉移作業只會覆寫指定分區中的資料。含有分區修飾符的目的地資料表格式為 `my_table${run_date}`，例如 `my_table$20230809`。

一天內重複進行相同的增量或截斷移轉作業，不會導致資料重複。不過，如果您執行多個不同的移轉設定，且這些設定會影響相同的 BigQuery 目的地資料表，BigQuery 資料移轉服務可能會重複資料。

## Cloud Storage 資源路徑

如要從 Cloud Storage 資料來源載入資料，您必須提供資料路徑。

Cloud Storage 資源路徑包含您的值區名稱和物件 (檔名)。舉例來說，如果 Cloud Storage bucket 名為 `mybucket`，資料檔案名為 `myfile.csv`，則資源路徑為 `gs://mybucket/myfile.csv`。

BigQuery 不支援 Cloud Storage 資源路徑在初始雙斜線後還有多個連續斜線。Cloud Storage 物件名稱可以包含多個連續的斜線 (「/」) 字元，但 BigQuery 會將多個連續斜線轉換為一個斜線。舉例來說，下列資源路徑在 Cloud Storage 中有效，但在 BigQuery 中則無效：`gs://bucket/my//object//name`。

如要擷取 Cloud Storage 資源路徑，請按照下列步驟操作：

1. 開啟 Cloud Storage 主控台。

   [Cloud Storage 主控台](https://console.cloud.google.com/storage/browser?hl=zh-tw)
2. 瀏覽至含有來源資料的物件 (檔案) 位置。
3. 按一下物件名稱。

   「物件詳細資料」頁面隨即開啟。
4. 複製「gsutil URI」欄位中提供的值，開頭為 `gs://`。

**附註：** 您也可以使用 [`gcloud storage ls`](https://docs.cloud.google.com/sdk/gcloud/reference/storage/ls?hl=zh-tw) 指令列出值區或物件。

### Cloud Storage 資源路徑的萬用字元支援

如果您的 Cloud Storage 資料分成多個共用通用基礎名稱的檔案，那麼當您載入資料時，可以在資源路徑中使用萬用字元。

如要新增萬用字元至 Cloud Storage 資源路徑，請為基礎名稱加上星號 (\*)。舉例來說，如果您有兩個名為 `fed-sample000001.csv` 和 `fed-sample000002.csv` 的檔案，則資源路徑會是 `gs://mybucket/fed-sample*`。然後這個萬用字元就可以在Google Cloud 控制台或 Google Cloud CLI 中使用。

對於值區內的物件 (檔案名稱)，您可以使用多個萬用字元。萬用字元可以出現在物件名稱內的任何位置。

萬用字元不會展開 `gs://bucket/` 中的目錄。舉例來說，`gs://bucket/dir/*` 會在 `dir` 目錄中尋找檔案，但不會在 `gs://bucket/dir/subdir/` 子目錄中尋找檔案。

您也無法比對不含萬用字元的前置字元。舉例來說，`gs://bucket/dir` 不符合 `gs://bucket/dir/file.csv` 和 `gs://bucket/file.csv`。

不過，您可以在值區內的檔案名稱中使用多個萬用字元。
例如，`gs://bucket/dir/*/*.csv` 符合 `gs://bucket/dir/subdir/file.csv`。

如需萬用字元支援與參數化資料表名稱搭配使用的範例，請參閱「[移轉作業中的執行階段參數](https://docs.cloud.google.com/bigquery/docs/gcs-transfer-parameters?hl=zh-tw)」。

## 配額與限制

BigQuery 資料移轉服務會使用載入工作，將 Cloud Storage 資料載入至 BigQuery。

所有 BigQuery 對載入工作的[配額與限制](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#load_jobs)均適用於週期性 Cloud Storage 載入工作，但須注意下列事項：

| 值 | 限制 |
| --- | --- |
| 每個載入工作轉移作業的大小上限 | 15 TB |
| 每次傳輸作業的檔案數量上限 | 10,000 個檔案 |

## 定價

資料移轉至 BigQuery 之後，即適用標準的 BigQuery [儲存空間](https://docs.cloud.google.com/bigquery/pricing?hl=zh-tw#storage)和[查詢](https://docs.cloud.google.com/bigquery/pricing?hl=zh-tw#queries)計價方式。

如果是從 Cloud Storage 進行跨位置轉移，定價取決於 Cloud Storage bucket 的位置和目的地 BigQuery 資料集的位置。詳情請參閱「[在 Google Cloud](https://docs.cloud.google.com/storage/pricing?hl=zh-tw#network-buckets)內轉移資料」。

如要進一步瞭解價格，請參閱「[BigQuery 定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#data-transfer-service-pricing)」一文。

## 後續步驟

* 瞭解如何[設定 Cloud Storage 移轉作業](https://docs.cloud.google.com/bigquery/docs/cloud-storage-transfer?hl=zh-tw)。
* 瞭解 [Cloud Storage 移轉作業中的執行階段參數](https://docs.cloud.google.com/bigquery/docs/gcs-transfer-parameters?hl=zh-tw)。
* 進一步瞭解 [BigQuery 資料移轉服務](https://docs.cloud.google.com/bigquery/docs/dts-introduction?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-09 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-09 (世界標準時間)。"],[],[]]