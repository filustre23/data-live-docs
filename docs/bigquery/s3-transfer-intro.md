Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [參考資料](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# Amazon S3 移轉簡介

透過 Amazon S3 專用的 [BigQuery 資料移轉服務](https://docs.cloud.google.com/bigquery/docs/dts-introduction?hl=zh-tw)，您可以自動安排及管理從 Amazon S3 到 BigQuery 的週期性載入工作。

## 支援的檔案格式

BigQuery 資料移轉服務支援以以下格式從 Amazon S3 載入資料：

* 逗號分隔值 (CSV)
* JSON (以換行符號分隔)
* Avro
* Parquet
* ORC

## 支援的壓縮類型

Amazon S3 專用的 BigQuery 資料移轉服務支援載入壓縮資料。BigQuery 資料移轉服務支援的壓縮類型和 BigQuery 載入工作支援的相同。詳情請參閱[載入壓縮與未壓縮資料](https://docs.cloud.google.com/bigquery/docs/batch-loading-data?hl=zh-tw#loading_compressed_and_uncompressed_data)。

## Amazon S3 必備條件

從 Amazon S3 資料來源載入資料的必要事項

* 提供您來源資料的 Amazon S3 URI
* 具備存取金鑰 ID
* 具備私密存取金鑰
* 至少要針對 Amazon S3 來源資料設定 AWS 代管政策 [`AmazonS3ReadOnlyAccess`](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_manage.html)

## Amazon S3 URI

在提供 Amazon S3 URI 時，路徑必須採用以下格式
`s3://bucket/folder1/folder2/...` 只有頂層值區名稱是必要的。不一定要提供資料夾名稱。如果指定的 URI 僅含有值區名稱，則會移轉值區中的所有檔案並載入到 BigQuery 中。

## Amazon S3 移轉執行階段參數化

Amazon S3 URI 和目的地資料表都可以[參數化](https://docs.cloud.google.com/bigquery/docs/s3-transfer-parameters?hl=zh-tw)，可讓您以按日期排列的 Amazon S3 值區載入資料。請注意，URI 的值區部分無法參數化。Amazon S3 移轉作業使用的參數與 Cloud Storage 移轉作業使用的參數相同。

詳情請參閱「[在移轉作業中使用執行階段參數](https://docs.cloud.google.com/bigquery/docs/s3-transfer-parameters?hl=zh-tw)」。

## Amazon S3 移轉作業資料擷取

[設定 Amazon S3 移轉作業](https://docs.cloud.google.com/bigquery/docs/s3-transfer?hl=zh-tw#set_up_an_amazon_s3_data_transfer)時，您可以在移轉設定中選取「寫入偏好設定」，指定資料載入 BigQuery 的方式。

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

## Amazon S3 URI 對於萬用字元的支援範圍

如果來源資料分成多個含有相同基礎名稱的檔案，則可以在載入資料時，在 URI 中使用萬用字元。萬用字元由星號 (&ast;) 組成，可出現在 Amazon S3 URI 的任何位置，但不得做為值區名稱。

雖然 Amazon S3 URI 中可使用多個萬用字元，但如果 Amazon S3 URI 只指定單一萬用字元，則可進行一些最佳化：

* 每次轉移作業的檔案數量上限[較高](#quotas_and_limits)。
* 萬用字元會跨越目錄界線。舉例來說，Amazon S3 URI `s3://my-bucket/*.csv` 會與檔案 `s3://my-bucket/my-folder/my-subfolder/my-file.csv` 相符。

## Amazon S3 URI 範例

### 範例 1

如要將單一檔案從 Amazon S3 載入 BigQuery，請指定該檔案的 Amazon S3 URI。

```
s3://my-bucket/my-folder/my-file.csv
```

### 範例 2

如要將 Amazon S3 值區中的所有檔案載入 BigQuery，請只指定值區名稱，可使用萬用字元，也可以不使用。

```
s3://my-bucket/
```

或

```
s3://my-bucket/*
```

請注意，`s3://my-bucket*` 不是允許的 Amazon S3 URI，因為值區名稱中不能使用萬用字元。

### 範例 3

如要載入 Amazon S3 中具有相同前置字串的所有檔案，請指定通用前置字串，然後加上萬用字元。

```
s3://my-bucket/my-folder/*
```

請注意，與從頂層 Amazon S3 值區載入所有檔案不同，如要載入任何檔案，必須在 Amazon S3 URI 結尾指定萬用字元。

### 範例 4

如要從 Amazon S3 載入路徑類似的所有檔案，請指定通用前置字元，然後加上萬用字元。

```
s3://my-bucket/my-folder/*.csv
```

### 範例 5

請注意，萬用字元會跨越目錄，因此 `my-folder` 中的任何 `csv` 檔案，以及 `my-folder` 子資料夾中的檔案都會載入 BigQuery。

如果這些來源檔案位於 `logs` 資料夾中：

```
s3://my-bucket/logs/logs.csv
s3://my-bucket/logs/system/logs.csv
s3://my-bucket/logs/some-application/system_logs.log
s3://my-bucket/logs/logs_2019_12_12.csv
```

則以下內容會識別這些項目：

```
s3://my-bucket/logs/*
```

### 範例 6

如果您有這些來源檔案，但只想轉移檔案名稱為 `logs.csv` 的檔案：

```
s3://my-bucket/logs.csv
s3://my-bucket/metadata.csv
s3://my-bucket/system/logs.csv
s3://my-bucket/system/users.csv
s3://my-bucket/some-application/logs.csv
s3://my-bucket/some-application/output.csv
```

則下列項目會識別名稱中含有 `logs.csv` 的檔案：

```
s3://my-bucket/*logs.csv
```

### 範例 7

使用多個萬用字元可更精細地控管要轉移的檔案，但[限制會較嚴格](#quotas_and_limits)。使用多個萬用字元時，每個萬用字元只會比對子目錄中路徑的結尾。舉例來說，假設 Amazon S3 中有下列來源檔案：

```
s3://my-bucket/my-folder1/my-file1.csv
s3://my-bucket/my-other-folder2/my-file2.csv
s3://my-bucket/my-folder1/my-subfolder/my-file3.csv
s3://my-bucket/my-other-folder2/my-subfolder/my-file4.csv
```

如果只想轉移 `my-file1.csv` 和 `my-file2.csv`，請使用下列值做為 Amazon S3 URI：

```
s3://my-bucket/*/*.csv
```

由於萬用字元不會跨越目錄，這個 URI 會將轉移作業限制為僅轉移 `my-folder1` 和 `my-other-folder2` 中的 CSV 檔案。子資料夾不會納入轉移範圍。

## AWS 存取金鑰

存取金鑰 ID 和私密存取金鑰用於代表您存取 Amazon S3 資料。最佳做法是建立 Amazon S3 移轉作業專用的唯一存取金鑰 ID 和私密存取金鑰，以提供 BigQuery 資料移轉服務的最低存取權。如需有關管理存取金鑰的資訊，請參閱 [AWS 一般參考說明文件](https://docs.aws.amazon.com/general/latest/gr/managing-aws-access-keys.html)。

## IP 限制

如果您使用 IP 限制存取 Amazon S3，請務必將 BigQuery 資料移轉服務工作站使用的 IP 範圍加入 IP 許可清單。

如要將 IP 範圍新增為 Amazon S3 允許的公開 IP 位址，請參閱「[IP 限制](https://docs.cloud.google.com/storage-transfer/docs/source-amazon-s3?hl=zh-tw#ip_restrictions)」。

## 一致性考量

從 Amazon S3 移轉資料時，有些資料可能無法移轉到 BigQuery，如果最近才將檔案新增至值區中，更是如此。將檔案新增至值區後，BigQuery 資料移轉服務可能需要大約 5 分鐘才能提供該檔案。

**重要事項：** 為降低遺失資料的可能性，將檔案新增至 bucket 後，請等待至少 5 分鐘再安排 Amazon S3 移轉作業。

## 傳出資料移轉費用的最佳做法

如果目的地資料表設定有誤，從 Amazon S3 進行的移轉作業可能會失敗。設定不當的原因可能包括：

* 目的地資料表不存在。
* 未定義資料表結構定義。
* 資料表結構定義與要轉移的資料不相容。

為避免產生 Amazon S3 外送資料移轉費用，您應先使用一小部分但具代表性的檔案測試移轉作業。「小型」是指測試應具有較小的資料大小和檔案計數。

## 定價

如要瞭解 BigQuery 資料移轉服務定價，請參閱[定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#data-transfer-service-pricing)頁面。

請注意，使用這項服務可能必須支付其他產品 (非 Google) 的使用費用。詳情請參閱 [Amazon S3 定價頁面](https://aws.amazon.com/s3/pricing/)。

## 配額與限制

BigQuery 資料移轉服務會使用載入工作，將 Amazon S3 資料載入到 BigQuery 中。所有 BigQuery 載入工作的[配額和限制](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#load_jobs)均適用於週期性的 Amazon S3 移轉作業，但須注意以下事項：

| 值 | 限制 |
| --- | --- |
| 每個載入工作轉移作業的大小上限 | 15 TB |
| Amazon S3 URI 包含 0 或 1 個萬用字元時，每次移轉作業的檔案數量上限 | 10,000,000 個檔案 |
| Amazon S3 URI 包含超過 1 個萬用字元時，每次移轉作業的檔案數量上限 | 10,000 個檔案 |

## 後續步驟

* 瞭解如何[設定 Amazon S3 移轉作業](https://docs.cloud.google.com/bigquery/docs/s3-transfer?hl=zh-tw)。
* 瞭解 [S3 移轉作業中的執行階段參數](https://docs.cloud.google.com/bigquery/docs/s3-transfer-parameters?hl=zh-tw)。
* 進一步瞭解 [BigQuery 資料移轉服務](https://docs.cloud.google.com/bigquery/docs/dts-introduction?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-02 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-02 (世界標準時間)。"],[],[]]