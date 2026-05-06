Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 外部資料表的中繼資料快取

本文說明如何使用中繼資料快取 (又稱*資料欄中繼資料索引*)，提升物件資料表和部分 BigLake 資料表的查詢效能。

物件資料表和某些類型的 BigLake 資料表可以快取外部資料存放區 (例如 Cloud Storage) 中檔案的中繼資料資訊。下列類型的 BigLake 資料表支援中繼資料快取：

* Amazon S3 BigLake 資料表
* Cloud Storage BigLake 資料表

中繼資料包括檔案名稱、分區資訊，以及檔案的中繼資料，例如列數。您可以選擇是否要在資料表上啟用中繼資料快取。如果查詢包含大量檔案，且使用 Hive 分區篩選器，中繼資料快取功能可發揮最大效益。

如果未啟用中繼資料快取，查詢資料表時必須讀取外部資料來源，才能取得物件中繼資料。讀取這項資料會增加查詢延遲時間；從外部資料來源列出數百萬個檔案可能需要幾分鐘。啟用中繼資料快取功能後，查詢作業就能避免列出外部資料來源中的檔案，並更快地分割及修剪檔案。

建立 BigLake 或物件資料表時，您可以啟用中繼資料快取。如要進一步瞭解如何建立物件資料表，請參閱「[建立物件資料表](https://docs.cloud.google.com/bigquery/docs/object-tables?hl=zh-tw)」一文。如要進一步瞭解如何建立 BigLake 資料表，請參閱下列主題：

* [建立 Amazon S3 BigLake 外部資料表](https://docs.cloud.google.com/bigquery/docs/omni-aws-create-external-table?hl=zh-tw)
* [為 Cloud Storage 建立 BigLake 外部資料表](https://docs.cloud.google.com/bigquery/docs/create-cloud-storage-table-biglake?hl=zh-tw)

## 中繼資料快取設定

有兩個屬性可控制這項功能的行為：

* **最大過時程度**：指定查詢何時使用快取中繼資料。
* 「中繼資料快取模式」會指定中繼資料的收集方式。

啟用中繼資料快取功能後，您可以指定可接受的資料表作業中繼資料過時間隔上限。舉例來說，如果指定間隔為 1 小時，只要資料表的中繼資料在過去 1 小時內重新整理過，針對該資料表執行的作業就會使用快取中繼資料。如果快取中繼資料的建立時間早於該時間，作業會改為從資料存放區 (Amazon S3 或 Cloud Storage) 擷取中繼資料。您可以指定介於 30 分鐘至 7 天之間的過時間隔。

你可以選擇自動或手動重新整理快取：

* 如果是自動重新整理，系統會以預設間隔重新整理快取，通常是 30 到 60 分鐘。如果資料儲存庫中的檔案是以隨機間隔新增、刪除或修改，建議自動重新整理快取。如要控管重新整理時間，例如在擷取、轉換及載入作業結束時觸發重新整理，請使用手動重新整理。
* 如要手動重新整理，請執行 [`BQ.REFRESH_EXTERNAL_METADATA_CACHE` 系統程序](https://docs.cloud.google.com/bigquery/docs/reference/system-procedures?hl=zh-tw#bqrefresh_external_metadata_cache)，依您決定的排程重新整理中繼資料快取。如果是 BigLake 資料表，您可以提供資料表資料目錄的子目錄，選擇性地重新整理中繼資料。這麼做可避免不必要的中繼資料處理作業。如果資料存放區中的檔案是以已知間隔新增、刪除或修改 (例如管道的輸出)，手動重新整理快取是個不錯的方法。

手動和自動重新整理快取時，都會以 [`INTERACTIVE`](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw) 查詢優先順序執行。

如果選擇使用自動重新整理功能，建議您建立[預訂](https://docs.cloud.google.com/bigquery/docs/reservations-intro?hl=zh-tw)，然後為執行中繼資料快取重新整理工作的專案，建立[工作類型為 `BACKGROUND` 的指派](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#assignments)。這樣一來，重新整理工作就不會與使用者查詢資源的要求競爭，而且如果沒有足夠的資源，重新整理工作可能會失敗。

設定陳舊間隔和中繼資料快取模式值之前，請先考量這些值之間的互動方式。請見以下範例：

* 如果資料表的中繼資料快取設定為需要手動重新整理，且過時間隔設為 2 天，您就必須每 2 天或更短的時間執行 `BQ.REFRESH_EXTERNAL_METADATA_CACHE` 系統程序，才能讓針對資料表執行的作業使用快取中繼資料。
* 如果資料表的 metadata 快取設定為自動重新整理，且過時間隔設為 30 分鐘，當 metadata 快取重新整理時間較長 (通常為 30 到 60 分鐘) 時，對資料表執行的部分作業可能會從資料存放區讀取資料。

如要進一步瞭解如何為 BigLake 資料表設定中繼資料快取選項，請參閱「[建立 Amazon S3 BigLake 外部資料表](https://docs.cloud.google.com/bigquery/docs/omni-aws-create-external-table?hl=zh-tw)」或「[建立 Cloud Storage 的 BigLake 外部資料表](https://docs.cloud.google.com/bigquery/docs/create-cloud-storage-table-biglake?hl=zh-tw)」。

如要進一步瞭解如何設定物件資料表的中繼資料快取選項，請參閱「[建立物件資料表](https://docs.cloud.google.com/bigquery/docs/object-tables?hl=zh-tw#create-object-table)」一文。

## 取得中繼資料快取重新整理作業的相關資訊

如要查詢中繼資料快取重新整理作業的相關資訊，請查詢 [`INFORMATION_SCHEMA.JOBS` 檢視區塊](https://docs.cloud.google.com/bigquery/docs/information-schema-jobs?hl=zh-tw)，如下列範例所示：

```
SELECT *
FROM `region-us.INFORMATION_SCHEMA.JOBS`
WHERE job_id LIKE '%metadata_cache_refresh%'
AND creation_time > TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 6 HOUR)
ORDER BY start_time DESC
LIMIT 10;
```

## 將客戶管理的加密金鑰與快取中繼資料搭配使用

快取中繼資料會受到[客戶代管加密金鑰 (CMEK)](https://docs.cloud.google.com/bigquery/docs/customer-managed-encryption?hl=zh-tw) 保護，該金鑰用於與快取中繼資料相關聯的資料表。這可能是直接套用至資料表的 CMEK，或是資料表從資料集或專案繼承的 CMEK。

如果為專案或資料集設定預設 CMEK，或是變更專案或資料集的現有 CMEK，這不會影響現有資料表或其快取中繼資料。您必須[變更表格的鍵](https://docs.cloud.google.com/bigquery/docs/customer-managed-encryption?hl=zh-tw#change_key)，才能將新鍵套用至表格及其快取中繼資料。

在 BigQuery 中建立的 CMEK 不適用於 BigLake 和物件資料表使用的 Cloud Storage 檔案。如要取得端對端 CMEK 加密，請[在 Cloud Storage 中為這些檔案設定 CMEK](https://docs.cloud.google.com/storage/docs/encryption/customer-managed-keys?hl=zh-tw)。

## 取得查詢工作的中繼資料快取用量資訊

如要取得查詢作業的中繼資料快取用量資訊，請呼叫該作業的 [`jobs.get` 方法](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs/get?hl=zh-tw)，並查看 `Job` 資源的 [`JobStatistics2` 區段](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#jobstatistics2)中的 [`MetadataCacheStatistics` 欄位](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#metadatacachestatistics)。這個欄位提供查詢使用的中繼資料快取啟用資料表資訊、查詢是否使用中繼資料快取，以及未使用的原因。

## 表格統計資料

如果是以 Parquet 檔案為基礎的 BigLake 資料表，系統會在重新整理中繼資料快取時收集資料表統計資料。系統會在自動和手動重新整理期間收集資料表統計資料，並將統計資料保留與中繼資料快取相同的時間長度。

收集的資料表統計資料包括檔案資訊，例如列數、實體和未壓縮的檔案大小，以及資料欄的基數。在以 Parquet 為基礎的 BigLake 表格上執行查詢時，這些統計資料會提供給查詢最佳化工具，以便進行更完善的查詢規劃，並可能提升某些類型查詢的效能。舉例來說，常見的查詢最佳化方式是動態限制條件傳播，也就是查詢最佳化工具會從較小的維度資料表，動態推斷聯結中較大事實資料表的述詞。雖然這項最佳化作業可使用正規化資料表結構定義加快查詢速度，但需要準確的資料表統計資料。中繼資料快取收集的資料表統計資料，可進一步最佳化 BigQuery 和 Apache Spark 中的查詢計畫。

## 限制

中繼資料快取有以下限制：

* 如果您同時發出多個手動重新整理要求，只有一個會成功。
* 如果未重新整理，中繼資料快取會在 7 天後過期。
* 如果您更新資料表的來源 URI，系統不會自動重新整理中繼資料快取，後續查詢會從過時的快取傳回資料。為避免發生這種情況，請手動重新整理中繼資料快取。如果資料表的後設資料快取設為自動重新整理，您必須將資料表的重新整理模式變更為手動，執行手動重新整理，然後將資料表的重新整理模式改回自動。
* 如果您要手動重新整理中繼資料快取，且目標資料集和 Cloud Storage 值區位於[區域](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw#regions)位置，則執行 [`BQ.REFRESH_EXTERNAL_METADATA_CACHE`](https://docs.cloud.google.com/bigquery/docs/reference/system-procedures?hl=zh-tw#bqrefresh_external_metadata_cache) 程序呼叫時，必須明確指定這個位置。你可以透過下列任一方式執行此操作：

  ### 控制台

  1. 前往「BigQuery」頁面。

     [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
  2. 在編輯器中選取分頁標籤。
  3. 按一下「更多」settings，然後按一下「查詢設定」。
  4. 在「位置」部分，取消勾選「自動選取位置」核取方塊，然後指定目標區域。
  5. 按一下 [儲存]。
  6. 在該編輯器分頁中，執行包含 `BQ.REFRESH_EXTERNAL_METADATA_CACHE` 程序呼叫的查詢。

  ### bq

  如果使用 [`bq query`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_query) 執行含有 `BQ.REFRESH_EXTERNAL_METADATA_CACHE` 程序呼叫的查詢，請務必指定 [`--location` 旗標](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#global_flags)。

## 後續步驟

* 進一步瞭解如何[建立 Cloud Storage BigLake 資料表並快取中繼資料](https://docs.cloud.google.com/bigquery/docs/create-cloud-storage-table-biglake?hl=zh-tw)。
* 進一步瞭解如何[建立含中繼資料快取的 Amazon S3 BigLake 資料表](https://docs.cloud.google.com/bigquery/docs/omni-aws-create-external-table?hl=zh-tw)。
* 進一步瞭解如何[建立物件資料表並快取中繼資料](https://docs.cloud.google.com/bigquery/docs/object-tables?hl=zh-tw)。
* 瞭解如何[在啟用 BigLake 中繼資料快取的資料表上使用具體化檢視表](https://docs.cloud.google.com/bigquery/docs/materialized-views-intro?hl=zh-tw#biglake)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-06 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-06 (世界標準時間)。"],[],[]]