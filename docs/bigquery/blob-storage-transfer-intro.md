Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [參考資料](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# Blob 儲存體轉移作業簡介

透過 Azure Blob 儲存體專用的 [BigQuery 資料移轉服務](https://docs.cloud.google.com/bigquery/docs/dts-introduction?hl=zh-tw)，您可以自動安排及管理從 Azure Blob 儲存體和 [Azure Data Lake Storage Gen2](https://learn.microsoft.com/en-us/azure/storage/blobs/data-lake-storage-introduction) 到 BigQuery 的週期性載入工作。

## 支援的檔案格式

BigQuery 資料移轉服務支援以以下格式從 Blob 儲存空間載入資料：

* 逗號分隔值 (CSV)
* JSON (以換行符號分隔)
* Avro
* Parquet
* ORC

## 支援的壓縮類型

Blob 儲存空間專用的 BigQuery 資料移轉服務支援載入壓縮資料。BigQuery 資料移轉服務支援的壓縮類型和 BigQuery 載入工作支援的相同。詳情請參閱[載入壓縮與未壓縮資料](https://docs.cloud.google.com/bigquery/docs/batch-loading-data?hl=zh-tw#loading_compressed_and_uncompressed_data)。

## 轉移作業必備條件

如要從 Blob 儲存空間資料來源載入資料，請先收集下列資訊：

* 來源資料的 Blob 儲存體帳戶名稱、容器名稱和資料路徑 (選用)。資料路徑欄位為選填，用於比對常見的物件前置字元和副檔名。如果省略資料路徑，系統會轉移容器中的所有檔案。
* Azure 共用存取簽章 (SAS) 權杖，可授予資料來源的讀取權限。如要進一步瞭解如何建立 SAS 權杖，請參閱「[共用存取簽章 (SAS)](#shared-access-signature)」。

## 轉移執行階段參數化

Blob 儲存空間資料路徑和目的地資料表皆可參數化，讓您依日期順序從容器載入資料。Blob Storage 移轉作業使用的參數與 Cloud Storage 移轉作業使用的參數相同。詳情請參閱「[在移轉作業中使用執行階段參數](https://docs.cloud.google.com/bigquery/docs/blob-storage-transfer-parameters?hl=zh-tw)」。

## Azure Blob 移轉作業資料擷取

[設定 Azure Blob 移轉作業](https://docs.cloud.google.com/bigquery/docs/blob-storage-transfer?hl=zh-tw#set_up_an_azure_blob_storage_data_transfer)時，您可以在移轉設定中選取「寫入偏好設定」，指定資料載入 BigQuery 的方式。

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

## 支援 Blob 儲存體資料路徑的萬用字元

如要選取分成多個檔案的來源資料，請在資料路徑中指定一或多個星號 (`*`) 萬用字元。

資料路徑中可使用多個萬用字元，但如果只使用一個萬用字元，則可進行部分最佳化：

* 每次轉移作業的檔案數量上限[較高](#quotas_and_limits)。
* 萬用字元會跨越目錄界線。舉例來說，資料路徑 `my-folder/*.csv` 會比對檔案 `my-folder/my-subfolder/my-file.csv`。

## Blob 儲存空間資料路徑範例

以下是 Blob 儲存體移轉作業的有效資料路徑範例。請注意，資料路徑開頭不是 `/`。

### 範例：單一檔案

如要將單一檔案從 Blob 儲存空間載入至 BigQuery，請指定 Blob 儲存空間檔案名稱：

```
my-folder/my-file.csv
```

### 範例：所有檔案

如要將 Blob 儲存空間容器中的所有檔案載入 BigQuery，請將資料路徑設為單一萬用字元：

```
*
```

### 範例：具有相同前置字串的檔案

如要載入 Blob 儲存空間中具有相同前置字串的所有檔案，請指定前置字串 (可使用萬用字元)：

```
my-folder/
```

或

```
my-folder/*
```

### 範例：路徑相似的檔案

如要從 Blob 儲存體載入路徑相似的所有檔案，請指定通用前置字串和後置字串：

```
my-folder/*.csv
```

如果只使用單一萬用字元，就會跨目錄。在本例中，系統會選取 `my-folder` 中的每個 CSV 檔案，以及 `my-folder` 每個子資料夾中的每個 CSV 檔案。

### 範例：路徑結尾的萬用字元

請參考下列資料路徑：

```
logs/*
```

選取下列所有檔案：

```
logs/logs.csv
logs/system/logs.csv
logs/some-application/system_logs.log
logs/logs_2019_12_12.csv
```

### 範例：路徑開頭的萬用字元

請參考下列資料路徑：

```
*logs.csv
```

選取下列所有檔案：

```
logs.csv
system/logs.csv
some-application/logs.csv
```

且未選取下列任一檔案：

```
metadata.csv
system/users.csv
some-application/output.csv
```

### 範例：多個萬用字元

使用多個萬用字元可進一步控管檔案選取作業，但[限制較嚴格](#quotas_and_limits)。使用多個萬用字元時，每個萬用字元只會涵蓋單一子目錄。

請參考下列資料路徑：

```
*/*.csv
```

選取下列兩個檔案：

```
my-folder1/my-file1.csv
my-other-folder2/my-file2.csv
```

且未選取下列任一檔案：

```
my-folder1/my-subfolder/my-file3.csv
my-other-folder2/my-subfolder/my-file4.csv
```

## 共用存取簽章 (SAS)

Azure SAS 權杖用於代表您存取 Blob 儲存體資料。請按照下列步驟，為轉移作業建立 SAS 權杖：

1. 建立或使用現有的 Blob 儲存空間使用者，存取 Blob 儲存空間容器的儲存空間帳戶。
2. 在**儲存空間帳戶**層級建立 SAS 權杖。如要使用 Azure 入口網站建立 SAS 權杖，請按照下列步驟操作：

   1. 在「Allowed services」(允許的服務) 中，選取「Blob」(Blob)。
   2. 在「Allowed resource types」(允許的資源類型) 中，選取「Container」(容器) 和「Object」(物件)。
   3. 在「允許的權限」部分，選取「讀取」和「列出」。
   4. SAS 權杖的預設到期時間為 8 小時。設定適合移轉時間表的到期時間。
   5. 請勿在「允許的 IP 位址」欄位中指定任何 IP 位址。
   6. 在「允許的通訊協定」部分，選取「僅限 HTTPS」。
3. 建立 SAS 權杖後，請記下傳回的「SAS 權杖」值。設定轉移作業時，您需要這個值。

## IP 限制

如果您使用 Azure 儲存空間防火牆限制 Azure 資源的存取權，請務必將 BigQuery 資料移轉服務工作站使用的 IP 範圍，加入允許的 IP 清單。

如要將 IP 範圍新增為 Azure 儲存體防火牆允許的 IP，請參閱「[IP 限制](https://docs.cloud.google.com/storage-transfer/docs/source-microsoft-azure?hl=zh-tw#ip_restrictions)」。

## 一致性考量

將檔案新增至 Blob 儲存空間容器後，BigQuery 資料移轉服務可能需要大約 5 分鐘才能提供該檔案。

**重要事項：** 為降低遺失資料的可能性，將檔案新增至容器後，請等待至少 5 分鐘再安排 BLOB 儲存空間移轉作業。

## 控管輸出費用的最佳做法

如果目的地資料表設定有誤，Blob 儲存體移轉作業可能會失敗。設定不當的可能原因包括：

* 目的地資料表不存在。
* 未定義資料表結構定義。
* 資料表結構定義與要轉移的資料不相容。

為避免產生額外的 Blob 儲存空間輸出費用，請先使用少量但具代表性的檔案子集測試轉移作業。請確保這項測試的資料大小和檔案數量都不大。

此外，請注意，系統會在從 Blob 儲存空間傳輸檔案前，先比對資料路徑的前置字元，但會在 Google Cloud內比對萬用字元。如果檔案轉移至Google Cloud ，但未載入 BigQuery，這項差異可能會增加 Blob 儲存空間的輸出費用。

舉例來說，請看以下資料路徑：

```
folder/*/subfolder/*.csv
```

下列兩個檔案都會轉移至 Google Cloud，因為檔案名稱的前置字串都是 `folder/`：

```
folder/any/subfolder/file1.csv
folder/file2.csv
```

不過，只有 `folder/any/subfolder/file1.csv` 檔案會載入 BigQuery，因為該檔案符合完整資料路徑。

## 定價

詳情請參閱 [BigQuery 資料移轉服務定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#bqdts)。

使用這項服務也可能必須支付其他產品 (非 Google) 的使用費用。詳情請參閱 [Blob Storage 定價](https://azure.microsoft.com/en-us/pricing/details/storage/blobs/)。

## 配額與限制

BigQuery 資料移轉服務會使用載入工作，將 Blob 儲存體資料載入至 BigQuery。所有 BigQuery 載入工作的[配額與限制](https://cloud.google.com/bigquery/quotas?hl=zh-tw#load_jobs)均適用於週期性 Blob Storage 移轉作業，但請注意下列事項：

| 限制 | 預設 |
| --- | --- |
| 每個載入工作轉移作業的大小上限 | 15 TB |
| Blob 儲存空間資料路徑包含 0 或 1 個萬用字元時，每次轉移作業的檔案數量上限 | 10,000,000 個檔案 |
| Blob 儲存空間資料路徑包含 2 個以上的萬用字元時，每次移轉作業的檔案數量上限 | 10,000 個檔案 |

## 後續步驟

* 進一步瞭解如何[設定 Blob 儲存體轉移作業](https://docs.cloud.google.com/bigquery/docs/blob-storage-transfer?hl=zh-tw)。
* 進一步瞭解[移轉作業中的執行階段參數](https://docs.cloud.google.com/bigquery/docs/blob-storage-transfer-parameters?hl=zh-tw)。
* 進一步瞭解 [BigQuery 資料移轉服務](https://docs.cloud.google.com/bigquery/docs/dts-introduction?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-14 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-14 (世界標準時間)。"],[],[]]