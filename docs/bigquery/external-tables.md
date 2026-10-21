Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 外部資料表簡介

本文說明如何使用外部資料表，處理儲存在 BigQuery 外部的資料。如要使用外部資料來源，您也可以使用[外部資料集](https://docs.cloud.google.com/bigquery/docs/datasets-intro?hl=zh-tw#external_datasets)。

外部資料表可讓您查詢外部資料儲存庫中的結構化資料。如要查詢外部資料表，您必須具備外部資料表和外部資料來源的權限。例如，如要查詢使用 Cloud Storage 資料來源的外部資料表，您必須具備下列權限：

* `bigquery.tables.getData`
* `bigquery.jobs.create`
* `storage.buckets.get`
* `storage.objects.get`

## 支援的資料儲存庫

您可以將非 BigLake 外部資料表與下列資料儲存庫搭配使用：

* [Cloud Storage](https://docs.cloud.google.com/bigquery/docs/external-data-cloud-storage?hl=zh-tw)
* [Bigtable](https://docs.cloud.google.com/bigquery/docs/external-data-bigtable?hl=zh-tw)
* [Google 雲端硬碟](https://docs.cloud.google.com/bigquery/docs/external-data-drive?hl=zh-tw)

## 臨時資料表支援

您可以在 BigQuery 中使用永久資料表或臨時資料表查詢外部資料來源。永久資料表是在資料集中建立並連結至外部資料來源的資料表。由於資料表是永久性的，您可以使用[存取控管](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)功能，與其他有權存取基礎外部資料來源的使用者共用資料表，並隨時查詢資料表。

使用臨時資料表查詢外部資料來源時，您必須提交內含查詢的指令，並建立連結至外部資料來源的非永久資料表。使用臨時資料表時，不用在 BigQuery 資料集內建立資料表。因為資料表不會永久儲存在資料集中，所以無法與其他使用者分享。使用臨時資料表查詢外部資料來源，適合用於對外部資料執行一次性、臨時查詢，或用於擷取、轉換和載入 (ETL) 程序。

## 多個來源檔案

如果您根據 Cloud Storage 建立非 BigLake 外部資料表，則可以使用多個外部資料來源，前提是這些資料來源具有相同的結構定義。這項功能不支援以 Bigtable 或 Google 雲端硬碟為基礎的非 BigLake 外部資料表。

## 限制

外部資料表有以下限制：

* BigQuery 不保證外部資料表的資料一致性。如果基礎資料在查詢執行期間遭到變更，可能會導致非預期的行為。
* 與查詢標準 BigQuery 資料表中的資料相比，外部資料表的查詢效能可能較慢。如果查詢速度是優先考量，請[將資料載入 BigQuery](https://docs.cloud.google.com/bigquery/loading-data?hl=zh-tw)，而非設定外部資料來源。包含外部資料表的查詢效能取決於外部儲存空間類型。舉例來說，查詢儲存在 Cloud Storage 中的資料會比查詢 Google 雲端硬碟中的資料快。一般來說，外部資料表的查詢效能應等同於直接從資料來源讀取資料。
* 您無法使用 DML 或其他方法修改外部資料表。外部資料表在 BigQuery 中為唯讀。
* 您無法使用 `TableDataList` JSON API 方法從外部資料表擷取資料。詳情請參閱 [`tabledata.list`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tabledata/list?hl=zh-tw)。如要避開這項限制，可以將查詢結果儲存至目的地資料表。接著，您可以在結果資料表上使用 `TableDataList` 方法。
* 您無法執行從外部資料表匯出資料的 BigQuery 工作。如要避開這項限制，可以將查詢結果儲存至目的地資料表。接著，對結果資料表執行擷取工作。
* 無法複製外部資料表。
* 您無法在[萬用字元資料表](https://docs.cloud.google.com/bigquery/docs/querying-wildcard-tables?hl=zh-tw)查詢中參照外部資料表。
* 外部資料表不支援分群。這類資料庫支援有限的分區方式。詳情請參閱「[查詢外部分區資料](https://docs.cloud.google.com/bigquery/docs/hive-partitioned-queries-gcs?hl=zh-tw)」。
* 查詢 Cloud Storage 以外的外部資料來源時，系統不會[快取](https://docs.cloud.google.com/bigquery/docs/cached-results?hl=zh-tw)結果。(支援對 Cloud Storage 執行 GoogleSQL 查詢)。每次查詢外部資料表，系統均會向您收費，即使您是發出多次相同的查詢也一樣。如果您需要對不常變更的外部資料表重複發出查詢，請考慮[將查詢結果寫入永久性資料表](https://docs.cloud.google.com/bigquery/docs/writing-results?hl=zh-tw#permanent-table)，然後改對永久性資料表執行查詢。
* 對 Bigtable 外部資料來源執行的並行查詢數量上限為 16 個。
* 如果聯合查詢使用外部資料表，即使傳回資料列，模擬測試仍可能回報資料下限為 0 位元組。這是因為從外部資料表處理的資料量，要等到實際查詢完成後才能確定。執行聯合查詢會產生處理這項資料的費用。
* 外部資料表的資料欄名稱不得使用 `_object_metadata`。保留供內部使用。
* BigQuery 不支援顯示外部資料表的資料表儲存空間統計資料。
* 外部資料表不支援[彈性資料欄名稱](https://docs.cloud.google.com/bigquery/docs/schemas?hl=zh-tw#flexible-column-names)。
* BI Engine 不支援查詢外部資料表。
* BigQuery 不支援[資料提升](https://docs.cloud.google.com/bigquery/docs/spanner-federated-queries?hl=zh-tw#data_boost)功能，無法[從 BigQuery 讀取 Bigtable 資料](https://docs.cloud.google.com/bigquery/docs/create-bigtable-external-table?hl=zh-tw)。
* BigQuery 不支援外部資料表的[時間旅行或安全資料保留期](https://docs.cloud.google.com/bigquery/docs/time-travel?hl=zh-tw)。不過，如果是 Apache Iceberg 外部資料表，您可以使用 [`FOR SYSTEM_TIME AS OF` 子句](https://docs.cloud.google.com/bigquery/docs/access-historical-data?hl=zh-tw#query_data_at_a_point_in_time)，存取保留在 Iceberg 中繼資料中的快照。
* 所有格式專屬限制皆適用：
  + [CSV 限制](https://docs.cloud.google.com/bigquery/docs/loading-data-cloud-storage-csv?hl=zh-tw#limitations)
  + [JSON 限制](https://docs.cloud.google.com/bigquery/docs/loading-data-cloud-storage-json?hl=zh-tw#limitations)
  + [Parquet 限制](https://docs.cloud.google.com/bigquery/docs/loading-data-cloud-storage-parquet?hl=zh-tw#limitations)
  + [ORC 限制](https://docs.cloud.google.com/bigquery/docs/loading-data-cloud-storage-orc?hl=zh-tw#limitations)
  + [Avro 限制](https://docs.cloud.google.com/bigquery/docs/loading-data-cloud-storage-avro?hl=zh-tw#limitations)
  + [Iceberg 限制](https://docs.cloud.google.com/bigquery/docs/iceberg-tables?hl=zh-tw#limitations)
  + [Delta Lake 限制](https://docs.cloud.google.com/bigquery/docs/omni-azure-create-external-table?hl=zh-tw#limitations)

## 位置注意事項

選擇外部資料表的位置時，必須同時考量 BigQuery 資料集和外部資料來源的位置。

### Cloud Storage

使用 [BigLake](https://docs.cloud.google.com/bigquery/docs/query-cloud-storage-using-biglake?hl=zh-tw) 或[非 BigLake 外部資料表](https://docs.cloud.google.com/bigquery/docs/query-cloud-storage-data?hl=zh-tw)查詢 Cloud Storage 中的資料時，bucket 必須與包含外部資料表定義的 BigQuery 資料集位於相同位置。例如：

* [單一區域 bucket](https://docs.cloud.google.com/storage/docs/locations?hl=zh-tw#location-r)

  如果 Cloud Storage bucket 位於 `us-central1` (愛荷華州) 區域，BigQuery 資料集必須位於 `us-central1` (愛荷華州) 區域或 `US` 多區域。

  如果 Cloud Storage bucket 位於 `europe-west4` (荷蘭) 區域，BigQuery 資料集必須位於 `europe-west4` (荷蘭) 區域或 `EU` 多區域。

  如果 Cloud Storage bucket 位於 `europe-west1` (比利時) 區域，對應的 BigQuery 資料集也必須位於 `europe-west1` (比利時) 或 `EU` 多區域。
* [雙區域 bucket](https://docs.cloud.google.com/storage/docs/locations?hl=zh-tw#location-dr)

  如果 Cloud Storage bucket 位於 `NAM4` 預先定義的雙區域，或任何包含 `us-central1` (愛荷華州) 區域的可設定雙區域，則對應的 BigQuery 資料集必須位於 `us-central1` (愛荷華州) 區域「或」`US` 多區域。

  如果 Cloud Storage bucket 位於 `EUR4` 預先定義的雙區域，或任何包含 `europe-west4` (荷蘭) 區域的可設定雙區域，則對應的 BigQuery 資料集必須位於 `europe-west4` (荷蘭) 區域*或* `EU` 多區域。

  如果 Cloud Storage bucket 位於 `ASIA1` 預先定義的雙區域，對應的 BigQuery 資料集必須位於 `asia-northeast1` (東京)「或」`asia-northeast2` (大阪) 區域。

  如果 Cloud Storage bucket 使用可設定的雙區域，其中包含 `australia-southeast1` (雪梨) 和 `australia-southeast2` (墨爾本) 區域，則對應的 BigQuery bucket 必須位於 `australia-southeast1` (雪梨) *或* `australia-southeast2` (墨爾本) 區域。
* [多區域 bucket](https://docs.cloud.google.com/storage/docs/locations?hl=zh-tw#location-mr)

  對於外部資料表，*不*建議將多區域資料集位置與多區域 Cloud Storage bucket 搭配使用，因為外部查詢效能取決於最低延遲時間和最佳網路頻寬。

  如果 BigQuery 資料集位於 `US` 多區域，則對應的 Cloud Storage bucket 必須位於 `US` 多區域、單一區域 `us-central1` (愛荷華州)，或包含 `us-central1` (愛荷華州) 的雙區域 (例如 `NAM4` 雙區域)，或包含 `us-central1` 的可設定雙區域。

  如果 BigQuery 資料集位於 `EU` 多區域，則對應的 Cloud Storage bucket 必須位於 `EU` 多區域、單一區域 `europe-west1` (比利時) 或 `europe-west4` (荷蘭)，或包含 `europe-west1` (比利時) 或 `europe-west4` (荷蘭) 的雙區域 (例如 `EUR4` 雙區域)，或包含 `europe-west1` 或 `europe-west4` 的可設定雙區域。

如要進一步瞭解支援的 Cloud Storage 位置，請參閱 Cloud Storage 說明文件中的「[值區位置](https://docs.cloud.google.com/storage/docs/bucket-locations?hl=zh-tw)」。

### Bigtable

透過 BigQuery 外部資料表[查詢 Bigtable 中的資料](https://docs.cloud.google.com/bigquery/docs/external-data-bigtable?hl=zh-tw)時，Bigtable 執行個體必須與 BigQuery 資料集位於相同位置：

* 單一區域：如果 BigQuery 資料集位於比利時 (`europe-west1`) 區域位置，對應的 Bigtable 執行個體必須位於比利時區域。
* 多區域：外部查詢效能取決於最低延遲時間和最佳網路頻寬，因此*不建議*在 Bigtable 外部資料表使用多區域資料集位置。

如要進一步瞭解支援的 Bigtable 位置，請參閱「[Bigtable 位置](https://docs.cloud.google.com/bigquery/docs/create-bigtable-external-table?hl=zh-tw#supported_regions_and_zones)」。

### Google 雲端硬碟

位置考量不適用於 [Google 雲端硬碟](https://docs.cloud.google.com/bigquery/external-data-drive?hl=zh-tw)外部資料來源。

## 在不同位置之間移動資料

如要手動將資料集從某個位置移至其他位置，請按照下列步驟操作：

1. 將 BigQuery 資料表中的[資料匯出](https://docs.cloud.google.com/bigquery/docs/exporting-data?hl=zh-tw)至 Cloud Storage bucket。

   從 BigQuery 中匯出資料並不需要付費，但是在 Cloud Storage [儲存匯出的資料](https://docs.cloud.google.com/storage/pricing?hl=zh-tw#storage-pricing)則會產生費用。BigQuery 匯出作業受[擷取工作](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#export_jobs)限制。
2. 將資料從匯出 Cloud Storage bucket 複製或移至您在目的地位置建立的新 bucket。舉例來說，如果您要將資料從 `US` 多區域移至 `asia-northeast1` 東京區域，則應將資料轉移至在東京建立的 bucket。如要瞭解如何移轉 Cloud Storage 物件，請參閱 Cloud Storage 說明文件中的「[複製、重新命名及移動物件](https://docs.cloud.google.com/storage/docs/copying-renaming-moving-objects?hl=zh-tw)」。

   在區域之間移轉資料時，Cloud Storage 會收取[網路輸出費用](https://docs.cloud.google.com/storage/pricing?hl=zh-tw#network-pricing)。
3. 在新位置建立新的 BigQuery 資料集，然後將 Cloud Storage bucket 中的資料載入新資料集。

   將資料載入 BigQuery 無須支付費用，但將資料儲存於 Cloud Storage 則須支付費用，直到您刪除資料或值區為止。載入資料之後，將資料儲存至 BigQuery 亦須支付相關費用。將資料載入 BigQuery 時，須遵守[載入工作](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#load_jobs)限制。

您也可以使用 [Managed Service for Apache Airflow](https://cloud.google.com/blog/products/data-analytics/how-to-transfer-bigquery-tables-between-locations-with-cloud-composer?hl=zh-tw)，透過程式輔助方式移動及複製大型資料集。

如要進一步瞭解如何使用 Cloud Storage 儲存及移動大型資料集，請參閱「[搭配使用 Cloud Storage 與大數據](https://docs.cloud.google.com/storage/docs/working-with-big-data?hl=zh-tw)」。

## 最佳化 Cloud Storage 外部資料表查詢

使用外部資料表查詢 Cloud Storage 中的資料時，如要提高效能並降低成本，建議啟用 [Rapid Cache](https://docs.cloud.google.com/storage/docs/rapid/rapid-cache?hl=zh-tw)。

Rapid Cache 為 Cloud Storage bucket 提供採用 SSD 的可用區讀取快取。啟用後，BigQuery 會運用 Rapid Cache 處理物件讀取要求，提供下列優勢：

* **加速查詢效能**：從 Cloud Storage 更快讀取資料，用於 BigQuery 工作負載。
* **降低網路資料移轉費用**：降低由多區域 bucket 支援的 BigQuery 工作負載資料移轉費用。從快取讀取資料產生的網路費用，低於直接從多區域 bucket 讀取資料。

BigQuery 是區域性服務，但其基礎運算資源可在可用區之間轉移，以平衡負載，因此建議您在執行 BigQuery 工作負載的區域內，為所有可用區啟用 Rapid Cache。無論 BigQuery 運算使用哪個可用區，都能確保快取執行個體可用。詳情請參閱「[Rapid Cache 定價](https://cloud.google.com/storage/pricing?hl=zh-tw#rapid-cache)」。

如要判斷 Rapid Cache 是否適合您，建議使用 [Rapid Cache 建議工具](https://docs.cloud.google.com/storage/docs/rapid/rapid-cache-recommender?hl=zh-tw)。Rapid Cache 建議工具會分析資料用量和儲存空間，針對在 bucket 與可用區組合中建立快取提供建議和洞察資訊。

## 定價

從 BigQuery 查詢外部資料表時，如果使用 [BigQuery 隨選](https://cloud.google.com/bigquery/pricing?hl=zh-tw#on_demand_pricing) (每 TiB) 定價，則須支付執行查詢和適用讀取位元組數的費用；如果使用 [BigQuery 容量](https://cloud.google.com/bigquery/pricing?hl=zh-tw#capacity_compute_analysis_pricing) (每運算單元小時) 定價，則須支付運算單元消耗量的費用。

如果資料是以 ORC 或 Parquet 格式儲存在 Cloud Storage，請參閱「[資料大小計算](https://docs.cloud.google.com/bigquery/docs/best-practices-costs?hl=zh-tw#estimate-query-costs)」。

系統也會依據應用程式的價格規定，針對來源應用程式所儲存的資料和使用的任何資源，向您收費：

* 如要瞭解 Cloud Storage 定價，請參閱「[Cloud Storage 定價](https://cloud.google.com/storage/pricing?hl=zh-tw)」。Cloud Storage 費用可能包含下列項目：

  + 資料儲存費用。
  + 存取 [Nearline](https://docs.cloud.google.com/storage/docs/storage-classes?hl=zh-tw#nearline)、[Coldline](https://docs.cloud.google.com/storage/docs/storage-classes?hl=zh-tw#coldline) 和 [Archive](https://docs.cloud.google.com/storage/docs/storage-classes?hl=zh-tw#archive) 儲存空間級別中的資料時，會產生資料擷取費用。
  + 跨不同區域讀取資料的網路用量費用。
  + 資料處理費用。不過，BigQuery 代為執行的 API 呼叫不會產生費用。
* 如要瞭解 Bigtable 定價，請參閱「[定價](https://cloud.google.com/bigtable/pricing?hl=zh-tw)」。
* 如要瞭解雲端硬碟定價，請參閱「[定價](https://gsuite.google.com/pricing.html?hl=zh-tw)」。

## 後續步驟

* 瞭解如何[建立 Bigtable 外部資料表](https://docs.cloud.google.com/bigquery/docs/create-bigtable-external-table?hl=zh-tw)。
* 瞭解如何[建立 Cloud Storage 外部資料表](https://docs.cloud.google.com/bigquery/docs/external-data-cloud-storage?hl=zh-tw)。
* 瞭解如何[建立雲端硬碟外部資料表](https://docs.cloud.google.com/bigquery/docs/external-data-drive?hl=zh-tw)。
* 瞭解如何[使用 Knowledge Catalog 排定及執行資料品質檢查](https://docs.cloud.google.com/bigquery/docs/dataplex-shared-introduction?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-10-20 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-10-20 (世界標準時間)。"],[],[]]