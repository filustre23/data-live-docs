Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 對外部資料來源使用中繼資料快取

本文說明如何使用中繼資料快取 (也稱為*資料欄中繼資料索引*)，提升物件資料表和某些類型 BigLake 資料表的查詢效能。

物件資料表和某些類型的 BigLake 資料表，可以快取外部資料儲存庫 (例如 Cloud Storage) 中檔案的中繼資料資訊。下列類型的 BigLake 資料表支援中繼資料快取：

* Amazon S3 BigLake 資料表
* Cloud Storage BigLake 資料表

中繼資料包括檔案名稱、分區資訊，以及檔案的中繼資料 (例如資料列數)。您可以選擇是否要啟用資料表的中繼資料快取功能。如果查詢含有大量檔案和 Hive 分區篩選器，中繼資料快取可帶來最大效益。

如未啟用中繼資料快取功能，資料表查詢就必須讀取外部資料來源，才能取得物件中繼資料。讀取這類資料會增加查詢延遲時間；從外部資料來源列出數百萬個檔案可能需要幾分鐘的時間。啟用中繼資料快取功能後，查詢作業就不必列出外部資料來源中的檔案，而且能更快分區及剪除檔案。

建立 BigLake 或物件資料表時，您可以啟用中繼資料快取功能。如要進一步瞭解如何建立物件資料表，請參閱「[建立物件資料表](https://docs.cloud.google.com/bigquery/docs/object-tables?hl=zh-tw)」。如要進一步瞭解如何建立 BigLake 資料表，請參閱下列任一主題：

* [建立 Amazon S3 BigLake 外部資料表](https://docs.cloud.google.com/bigquery/docs/omni-aws-create-external-table?hl=zh-tw)
* [建立 Cloud Storage 的 BigLake 外部資料表](https://docs.cloud.google.com/bigquery/docs/create-cloud-storage-table-biglake?hl=zh-tw)

## 中繼資料快取設定

有兩項屬性可控制這項功能的行為：

* **最大過時時間**指定查詢使用快取中繼資料的時間。
* **中繼資料快取模式**會指定中繼資料的收集方式。

啟用中繼資料快取功能後，您可以指定資料表作業可接受的中繼資料過時時間間隔上限。舉例來說，如果您指定 1 小時的間隔，則資料表作業會使用過去一小時內重新整理的快取中繼資料。如果快取的中繼資料超過這個時間，作業就會改為從資料儲存庫 (Amazon S3 或 Cloud Storage) 擷取中繼資料。您可以指定 30 分鐘至 7 天的過時時間間隔。

您可以選擇自動或手動重新整理快取：

* 如果是自動重新整理，快取會按照系統定義的間隔重新整理，通常介於 30 到 60 分鐘之間。如果資料儲存庫中的檔案會不定期新增、刪除或修改，自動重新整理快取是很好的做法。如需控制重新整理的時間點 (例如在擷取、轉換和載入工作結束時觸發重新整理)，請使用手動重新整理。
* 如要手動重新整理，請執行 [`BQ.REFRESH_EXTERNAL_METADATA_CACHE` 系統程序](https://docs.cloud.google.com/bigquery/docs/reference/system-procedures?hl=zh-tw#bqrefresh_external_metadata_cache)，按照您決定的時間表重新整理中繼資料快取。如果是 BigLake 資料表，您可以提供資料表資料目錄的子目錄，選擇性重新整理中繼資料。這種做法可避免不必要的中繼資料處理。如果資料儲存庫中的檔案是以已知間隔新增、刪除或修改 (例如做為管道的輸出內容)，則手動重新整理快取是很好的做法。

手動和自動快取重新整理都會以 [`INTERACTIVE`](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw) 查詢優先順序執行。

如果您選擇使用自動重新整理功能，建議您建立[預留項目](https://docs.cloud.google.com/bigquery/docs/reservations-intro?hl=zh-tw)，然後為執行中繼資料快取重新整理工作的專案建立[具有 `BACKGROUND` 工作類型的指派作業](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#assignments)。這樣可以避免重新整理工作與使用者查詢競爭資源，以及在資源不足時可能失敗的情況。

設定過時時間間隔和中繼資料快取模式值之前，請先考量兩者之間的互動方式。請見以下範例：

* 如果資料表的中繼資料快取設為需要手動重新整理，且過時時間間隔設為 2 天，則您必須每 2 天或更短時間執行一次 `BQ.REFRESH_EXTERNAL_METADATA_CACHE` 系統程序，才能對資料表使用快取的中繼資料。
* 如果資料表的中繼資料快取設為自動重新整理，且過時時間間隔設為 30 分鐘，則當中繼資料快取重新整理時間超過一般的 30 到 60 分鐘時，針對資料表執行的部分作業可能會從資料儲存庫讀取。

如要進一步瞭解如何設定 BigLake 資料表的中繼資料快取選項，請參閱「[建立 Amazon S3 BigLake 外部資料表](https://docs.cloud.google.com/bigquery/docs/omni-aws-create-external-table?hl=zh-tw)」或「[建立 Cloud Storage 的 BigLake 外部資料表](https://docs.cloud.google.com/bigquery/docs/create-cloud-storage-table-biglake?hl=zh-tw)」。

如要進一步瞭解如何設定物件資料表的中繼資料快取選項，請參閱「[建立物件資料表](https://docs.cloud.google.com/bigquery/docs/object-tables?hl=zh-tw#create-object-table)」。

## 取得中繼資料快取重新整理工作的相關資訊

如要查看中繼資料快取重新整理工作的相關資訊，請查詢 [`INFORMATION_SCHEMA.JOBS` 檢視表](https://docs.cloud.google.com/bigquery/docs/information-schema-jobs?hl=zh-tw)，如下例所示：

```
SELECT *
FROM `region-us.INFORMATION_SCHEMA.JOBS`
WHERE job_id LIKE '%metadata_cache_refresh%'
AND creation_time > TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 6 HOUR)
ORDER BY start_time DESC
LIMIT 10;
```

## 使用客戶自行管理的加密金鑰搭配快取中繼資料

快取中繼資料會受到[客戶自行管理的加密金鑰 (CMEK)](https://docs.cloud.google.com/bigquery/docs/customer-managed-encryption?hl=zh-tw) 保護，該金鑰用於與快取中繼資料相關聯的資料表。這可能是直接套用至資料表的 CMEK，也可能是資料表從資料集或專案繼承的 CMEK。

如果為專案或資料集設定預設 CMEK，或變更專案或資料集的現有 CMEK，不會影響現有資料表或其快取中繼資料。您必須[變更資料表的金鑰](https://docs.cloud.google.com/bigquery/docs/customer-managed-encryption?hl=zh-tw#change_key)，才能將新金鑰套用至資料表及其快取的中繼資料。

在 BigQuery 中建立的 CMEK 不適用於 BigLake 和物件資料表使用的 Cloud Storage 檔案。如要取得端對端 CMEK 加密，請[在 Cloud Storage 中為這些檔案設定 CMEK](https://docs.cloud.google.com/storage/docs/encryption/customer-managed-keys?hl=zh-tw)。

## 取得查詢工作的中繼資料快取用量資訊

如要取得查詢工作的元資料快取用量資訊，請呼叫該工作的 [`jobs.get` 方法](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs/get?hl=zh-tw)，並查看 `Job` 資源 [`JobStatistics2` 區段](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#jobstatistics2)中的 [`MetadataCacheStatistics` 欄位](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#metadatacachestatistics)。這個欄位會提供下列資訊：查詢使用了哪些已啟用中繼資料快取的資料表、查詢是否使用了中繼資料快取，以及未使用中繼資料快取的原因。

## 資料表統計資料

如果是以 Parquet 檔案為基礎的 BigLake 資料表，系統會在重新整理中繼資料快取時收集資料表統計資料。系統會在自動和手動重新整理期間收集資料表統計資料，並保留與中繼資料快取相同的時間。

收集的資料表統計資料包括檔案資訊，例如列數、實體和未壓縮檔案大小，以及資料欄的基數。在 Parquet BigLake 資料表執行查詢時，這些統計資料會提供給查詢最佳化工具，以便改善查詢計畫，並可能提升某些查詢類型的效能。舉例來說，常見的查詢最佳化是動態限制傳播，查詢最佳化工具會從較小的維度資料表，動態推論 join 中較大事實資料表的述詞。雖然這項最佳化功能可使用正規化資料表結構定義來加快查詢速度，但需要準確的資料表統計資料。中繼資料快取收集的資料表統計資料，可進一步最佳化 BigQuery 和 Apache Spark 的查詢計畫。

## 限制

中繼資料快取有下列限制：

* 如果同時發出多個手動重新整理要求，只有一個會成功。
* 如果未重新整理，中繼資料快取會在 7 天後過期。
* 如果您更新資料表的來源 URI，中繼資料快取不會自動重新整理，後續查詢會傳回過時快取中的資料。為避免這種情況，請手動重新整理中繼資料快取。如果資料表的中繼資料快取設為自動重新整理，您必須將資料表的重新整理模式變更為手動，執行手動重新整理，然後再將資料表的重新整理模式設回自動。
* 如果您手動重新整理中繼資料快取，且目標資料集和 Cloud Storage bucket 位於[區域](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw#regions)位置，則必須在執行 [`BQ.REFRESH_EXTERNAL_METADATA_CACHE`](https://docs.cloud.google.com/bigquery/docs/reference/system-procedures?hl=zh-tw#bqrefresh_external_metadata_cache) 程序呼叫時明確指定這個位置。方法如下：

  ### 控制台

  1. 前往「BigQuery」頁面。

     [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
  2. 在編輯器中選取分頁。
  3. 依序點選「編輯」>「查詢設定」。
  4. 在「Location」(位置) 區段中，取消選取「Automatic location selection」(自動選取位置) 核取方塊，然後指定目標區域。
  5. 按一下 [儲存]。
  6. 在該編輯器分頁中，執行包含 `BQ.REFRESH_EXTERNAL_METADATA_CACHE` 程序呼叫的查詢。

  ### bq

  如果使用 [`bq query`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_query) 執行含有 `BQ.REFRESH_EXTERNAL_METADATA_CACHE` 程序呼叫的查詢，請務必指定 [`--location` 旗標](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#global_flags)。

## 後續步驟

* 進一步瞭解如何[建立具備中繼資料快取功能的 Cloud Storage BigLake 資料表](https://docs.cloud.google.com/bigquery/docs/create-cloud-storage-table-biglake?hl=zh-tw)。
* 進一步瞭解如何[建立具備中繼資料快取功能的 Amazon S3 BigLake 資料表](https://docs.cloud.google.com/bigquery/docs/omni-aws-create-external-table?hl=zh-tw)。
* 進一步瞭解如何[建立具備中繼資料快取功能的物件資料表](https://docs.cloud.google.com/bigquery/docs/object-tables?hl=zh-tw)。
* 瞭解如何[對已啟用 BigLake 中繼資料快取的資料表使用 materialized view](https://docs.cloud.google.com/bigquery/docs/materialized-views-intro?hl=zh-tw#biglake)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-10-16 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-10-16 (世界標準時間)。"],[],[]]