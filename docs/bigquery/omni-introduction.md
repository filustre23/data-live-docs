Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# BigQuery Omni 簡介

**注意：** 使用以特定 BigQuery 版本建立的預留項目時，可能無法使用這項功能。如要進一步瞭解各版本啟用的功能，請參閱「[BigQuery 版本簡介](https://docs.cloud.google.com/bigquery/docs/editions-intro?hl=zh-tw)」。

透過 BigQuery Omni，您可以使用 BigLake 資料表，對儲存在 Amazon Simple Storage Service (Amazon S3) 或 Azure Blob 儲存體中的資料執行 BigQuery 數據分析。

許多機構會將資料儲存在多個公有雲中。通常這些資料最後會遭到孤立，因為難以取得所有資料的洞察。您希望使用經濟實惠的多雲資料工具快速分析資料，且不會造成分散式資料控管的額外負擔。使用 BigQuery Omni 統一介面，可減少這些摩擦。

如要對外部資料執行 BigQuery 分析，您必須先[連線至 Amazon S3](https://docs.cloud.google.com/bigquery/docs/omni-aws-create-connection?hl=zh-tw) 或 [Blob 儲存體](https://docs.cloud.google.com/bigquery/docs/omni-azure-create-connection?hl=zh-tw)。如要查詢外部資料，您需要建立參照 Amazon S3 或 Blob 儲存空間資料的 [BigLake 資料表](https://docs.cloud.google.com/bigquery/docs/biglake-intro?hl=zh-tw)。

## BigQuery Omni 工具

您可以使用下列 BigQuery Omni 工具，對外部資料執行 BigQuery 數據分析：

* [跨雲端聯結](https://docs.cloud.google.com/bigquery/docs/biglake-intro?hl=zh-tw#cross-cloud_joins)：直接從 BigQuery 地區執行查詢，聯結 BigQuery Omni 地區的資料。
* [跨雲端具體化檢視區塊](https://docs.cloud.google.com/bigquery/docs/load-data-using-cross-cloud-transfer?hl=zh-tw#materialized_view_replicas)：使用[具體化檢視區塊副本](https://docs.cloud.google.com/bigquery/docs/load-data-using-cross-cloud-transfer?hl=zh-tw#materialized_view_replicas)，持續從 BigQuery Omni 區域複製資料。支援資料篩選。
* [使用 `SELECT` 進行跨雲端移轉](https://docs.cloud.google.com/bigquery/docs/load-data-using-cross-cloud-transfer?hl=zh-tw)：在 BigQuery Omni 區域中，使用 `CREATE TABLE AS SELECT` 或 `INSERT INTO SELECT` 陳述式執行查詢，然後將結果移至 BigQuery 區域。
* [使用 `LOAD`](https://docs.cloud.google.com/bigquery/docs/load-data-using-cross-cloud-transfer?hl=zh-tw) 進行跨雲端移轉：
  使用 [`LOAD DATA` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/load-statements?hl=zh-tw)，將資料直接從 Amazon Simple Storage Service (Amazon S3) 或 Azure Blob 儲存空間載入 BigQuery

下表列出各項跨雲端工具的主要功能：

|  | 跨雲端聯結 | 跨雲端具體化檢視表 | 使用「`SELECT`」進行跨雲端轉移 | 使用「`LOAD`」進行跨雲端轉移 |
| --- | --- | --- | --- | --- |
| 建議用途 | 查詢一次性使用的外部資料，您可以與本機資料表聯結，或聯結兩個不同 BigQuery Omni 區域之間的資料，例如 AWS 和 Azure Blob 儲存體區域。如果資料量不大，且快取不是主要需求，請使用跨雲端聯結 | 設定重複或排定的查詢，持續以遞增方式轉移外部資料，其中快取是主要需求。舉例來說，如要維護資訊主頁 | 從 BigQuery Omni 區域到 BigQuery 區域，查詢一次性使用的外部資料，其中快取和查詢最佳化等手動控制項是主要需求，以及使用複雜查詢 (不支援跨雲端聯結或跨雲端具體化檢視區塊) 時 | 遷移大型資料集時，無須篩選資料，可使用排程查詢功能移動原始資料 |
| 支援在移動資料前進行篩選 | 可以。部分查詢運算子設有上限。詳情請參閱「[跨雲端加入限制](https://docs.cloud.google.com/bigquery/docs/biglake-intro?hl=zh-tw#cross-cloud_join_limitations)」一文。 | 可以。部分查詢運算子設有限制，例如匯總函式和 `UNION` 運算子 | 可以。查詢運算子沒有限制 | 否 |
| 轉移大小限制 | [每次轉移 60 GB](https://docs.cloud.google.com/bigquery/docs/biglake-intro?hl=zh-tw#cross-cloud_join_limitations) (每個傳送至遠端區域的子查詢都會產生一次轉移) | 不限 | [每次轉移 60 GB](https://docs.cloud.google.com/bigquery/docs/load-data-using-cross-cloud-transfer?hl=zh-tw#limitations_2) (每個傳送至遠端區域的子查詢都會產生一次轉移) | 不限 |
| 資料移轉壓縮 | 線路壓縮 | 資料欄 | 線路壓縮 | 線材壓縮 |
| 快取 | 不支援 | 支援[啟用快取功能的資料表和具體化檢視表](https://docs.cloud.google.com/bigquery/docs/omni-introduction?hl=zh-tw#cache-enabled_tables_with_materialized_views) | 不支援 | 不支援 |
| 輸出定價 | AWS 輸出和跨洲費用 | AWS 輸出和跨洲費用 | AWS 輸出和跨洲費用 | AWS 輸出和跨洲費用 |
| 資料傳輸的運算用量 | 使用來源 AWS 或 Azure Blob 儲存體區域中的時段 (預留或隨選) | 未使用 | 使用來源 AWS 或 Azure Blob 儲存體區域中的時段 (預留或隨選) | 未使用 |
| 用於篩選的運算用量 | 使用來源 AWS 或 Azure Blob 儲存體區域中的時段 (預留或隨選) | 使用來源 AWS 或 Azure Blob 儲存體區域中的時段 (預留或隨選)，計算本機具體化檢視區塊和中繼資料 | 使用來源 AWS 或 Azure Blob 儲存體區域中的時段 (預留或隨選) | 未使用 |
| 增量移轉作業 | 不支援 | 支援非匯總具體化檢視表 | 不支援 | 不支援 |

您也可以考慮使用下列替代方案，將資料從 Amazon Simple Storage Service (Amazon S3) 或 Azure Blob 儲存體轉移至 Google Cloud：

* [Storage 移轉服務](https://docs.cloud.google.com/storage-transfer?hl=zh-tw)：在 Google Cloud 和 Amazon Simple Storage Service (Amazon S3) 或 Azure Blob 儲存空間之間，轉移物件和檔案儲存空間的資料。
* [BigQuery 資料移轉服務](https://docs.cloud.google.com/bigquery/docs/dts-introduction?hl=zh-tw)：設定自動將資料移轉至 BigQuery，並依排程代管。支援[多種來源](https://docs.cloud.google.com/bigquery/docs/dts-introduction?hl=zh-tw#supported_data_sources)，適合用於資料遷移。BigQuery 資料移轉服務不支援篩選功能。

## 架構

BigQuery 的架構將運算資源與儲存空間分開，因此 BigQuery 可視需要擴充，以處理非常大的工作負載。BigQuery Omni 會在其他雲端中執行 BigQuery 查詢引擎，進而擴充這項架構。因此，您不必將資料實際移至 BigQuery 儲存空間。處理作業會在資料所在位置進行。

查詢結果可以透過安全連線傳回 Google Cloud ，例如顯示在 Google Cloud 控制台中。或者，您也可以直接將結果寫入 Amazon S3 值區或 Blob 儲存空間。在這種情況下，查詢結果不會跨雲端移動。

BigQuery Omni 會使用標準 AWS IAM 角色或 Azure Active Directory 主體，存取訂閱方案中的資料。您可以將 BigQuery Omni 的讀取或寫入存取權委派給其他使用者，並隨時撤銷存取權。

**注意：** 只有在您想將查詢結果寫回 Amazon S3 值區或 Blob 儲存體容器時，才需要寫入權限。

### 查詢資料時的資料流程

下圖說明資料在 Google Cloud 和 AWS 或 Azure 之間移動的方式，適用於下列查詢：

* `SELECT` 陳述式
* `CREATE EXTERNAL TABLE` 陳述式



1. BigQuery 控制平面會透過Google Cloud 主控台、bq 指令列工具、API 方法或用戶端程式庫，接收您提交的查詢工作。
2. BigQuery 控制層會將查詢工作傳送至 AWS 或 Azure 上的 BigQuery 資料層，以進行處理。
3. BigQuery 資料平面會透過 VPN 連線，接收控制平面傳送的查詢。
4. BigQuery 資料平面會從 Amazon S3 值區或 Blob 儲存體讀取資料表資料。
5. BigQuery 資料平面會在資料表資料上執行查詢工作。
   系統會在指定的 AWS 或 Azure 區域處理表格資料。
6. 查詢結果會透過 VPN 連線，從資料層傳輸至控制層。
7. BigQuery 控制平面會接收查詢工作結果，並在查詢工作的回應中向您顯示。這類資料最多保留 24 小時。
8. 查詢結果會傳回給您。

詳情請參閱[查詢 Amazon S3 資料](https://docs.cloud.google.com/bigquery/docs/omni-aws-create-external-table?hl=zh-tw)和 [Blob 儲存體資料](https://docs.cloud.google.com/bigquery/docs/omni-azure-create-external-table?hl=zh-tw)。

### 匯出資料時的資料流程

下圖說明在 `EXPORT DATA` 陳述式執行期間，資料如何在 Google Cloud 和 AWS 或 Azure 之間移動。



1. BigQuery 控制平面會透過 Google Cloud 主控台、bq 指令列工具、API 方法或用戶端程式庫，接收您提交的匯出查詢工作。查詢包含 Amazon S3 儲存桶或 Blob 儲存空間中查詢結果的目的地路徑。
2. BigQuery 控制層會將匯出查詢工作傳送至 BigQuery 資料層 (位於 AWS 或 Azure)，以進行處理。
3. BigQuery 資料平面會透過 VPN 連線，接收控制平面的匯出查詢。
4. BigQuery 資料平面會從 Amazon S3 值區或 Blob 儲存體讀取資料表資料。
5. BigQuery 資料平面會在資料表資料上執行查詢工作。
   系統會在指定的 AWS 或 Azure 區域處理表格資料。
6. BigQuery 會將查詢結果寫入 Amazon S3 值區或 Blob 儲存體中指定的目的地路徑。

詳情請參閱「[將查詢結果匯出至 Amazon S3](https://docs.cloud.google.com/bigquery/docs/omni-aws-export-results-to-s3?hl=zh-tw)」和「[Blob 儲存體](https://docs.cloud.google.com/bigquery/docs/omni-azure-export-results-to-azure-storage?hl=zh-tw)」。

## 優點

**效能：**由於資料不會跨雲端複製，且查詢會在資料所在區域執行，因此您能更快取得洞察資訊。

**費用。**由於資料不會移動，因此可節省輸出資料移轉費用。由於查詢是在 Google 管理的叢集上執行，因此 AWS 或 Azure 帳戶不會產生與 BigQuery Omni 相關的額外分析費用。您只需要根據 BigQuery 定價模式，支付執行查詢的費用。

**安全性與資料管理。**您可以在自己的 AWS 或 Azure 訂閱項目中管理資料。您不需要將原始資料移出或複製到公有雲。所有運算作業都會在 BigQuery 多租戶服務中進行，該服務與您的資料位於相同區域。

**無伺服器架構。**與 BigQuery 的其他功能一樣，BigQuery Omni 也是無伺服器服務。Google 會部署及管理執行 BigQuery Omni 的叢集。您不需要佈建任何資源或管理任何叢集。

**輕鬆管理。**BigQuery Omni 提供統一的管理介面，可透過 Google Cloud存取。BigQuery Omni 可以使用現有的 Google Cloud 帳戶和 BigQuery 專案。您可以在 Google Cloud 控制台中編寫 GoogleSQL 查詢，查詢 AWS 或 Azure 中的資料，並在 Google Cloud 控制台中查看結果。

**跨雲端轉移。**您可以從 S3 值區和 Blob 儲存空間，將資料載入標準 BigQuery 資料表。詳情請參閱「[將 Amazon S3 資料移轉至 BigQuery](https://docs.cloud.google.com/bigquery/docs/omni-aws-cross-cloud-transfer?hl=zh-tw)」和「[將 Blob 儲存空間資料移轉至 BigQuery](https://docs.cloud.google.com/bigquery/docs/omni-azure-cross-cloud-transfer?hl=zh-tw)」。

## 中繼資料快取功能可提升效能

您可以利用快取的中繼資料，提升參照 Amazon S3 資料的 BigLake 資料表查詢效能。如果您要處理大量檔案，或是資料經過 Apache Hive 分割，這項功能就特別實用。

BigQuery 使用 CMETA 做為分散式中繼資料系統，有效處理大型資料表。CMETA 提供資料欄和區塊層級的精細中繼資料，可透過系統資料表存取。這個系統會最佳化資料存取和處理方式，進而提升查詢效能。為進一步提升大型資料表的查詢效能，BigQuery 會維護中繼資料快取。CMETA 重新整理作業會讓這個快取保持在最新狀態。

中繼資料包括檔案名稱、分割資訊，以及來自檔案的實體中繼資料，例如列數。您可以選擇是否在資料表上啟用中繼資料快取功能。如果查詢的檔案數量龐大，且包含 Apache Hive 分區篩選器，中繼資料快取功能就能發揮最大效益。

如果未啟用中繼資料快取，查詢資料表時必須讀取外部資料來源，才能取得物件中繼資料。讀取這項資料會增加查詢延遲時間；列出外部資料來源中的數百萬個檔案可能需要幾分鐘。啟用中繼資料快取功能後，查詢作業就能避免列出外部資料來源中的檔案，並更快地分割及修剪檔案。

中繼資料快取也會與 Cloud Storage 物件版本管理功能整合。快取填入或重新整理時，會根據當時 Cloud Storage 物件的即時版本擷取中繼資料。因此，即使 Cloud Storage 中出現較新版本，啟用中繼資料快取功能的查詢也會讀取特定快取物件版本對應的資料。如要存取 Cloud Storage 中任何後續更新的物件版本資料，必須重新整理中繼資料快取。

有兩個屬性可控制這項功能：

* **最大過時程度**：指定查詢何時使用快取中繼資料。
* 「中繼資料快取模式」會指定中繼資料的收集方式。

啟用中繼資料快取功能後，您可以指定可接受的資料表作業中繼資料過時間隔上限。舉例來說，如果您指定 1 小時的間隔，則對資料表執行的作業會使用快取中繼資料 (如果該資料在過去 1 小時內已重新整理)。如果快取中繼資料較舊，作業會改為從 Amazon S3 擷取中繼資料。過時間隔可指定的範圍為 30 分鐘至 7 天。

為 BigLake 或物件資料表啟用中繼資料快取時，BigQuery 會觸發中繼資料產生重新整理工作。你可以選擇自動或手動重新整理快取：

* 如果是自動重新整理，系統會以定義的間隔重新整理快取，通常是 30 到 60 分鐘。如果 Amazon S3 中的檔案是以隨機間隔新增、刪除或修改，建議自動重新整理快取。如要控管重新整理時間，例如在擷取、轉換及載入作業結束時觸發重新整理，請使用手動重新整理。
* 如要手動重新整理，請執行 [`BQ.REFRESH_EXTERNAL_METADATA_CACHE` 系統程序](https://docs.cloud.google.com/bigquery/docs/reference/system-procedures?hl=zh-tw#bqrefresh_external_metadata_cache)，依據您的需求排程重新整理中繼資料快取。如果 Amazon S3 中的檔案是以已知間隔新增、刪除或修改 (例如管道的輸出內容)，手動重新整理快取是個好方法。

  如果您同時發出多個手動重新整理要求，只有一個會成功。

如果中繼資料快取未更新，會在 7 天後過期。

手動和自動重新整理快取時，都會以 [`INTERACTIVE`](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw) 查詢優先順序執行。

### 使用 `BACKGROUND` 預留項目

如果選擇使用自動重新整理功能，建議您建立[預訂](https://docs.cloud.google.com/bigquery/docs/reservations-intro?hl=zh-tw)，然後為執行中繼資料快取重新整理工作的專案，建立[指派作業，並將工作類型設為 `BACKGROUND`](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#assignments)。使用`BACKGROUND`預留項目時，重新整理作業會使用專屬資源集區，避免重新整理作業與使用者查詢競爭，並防止作業因資源不足而可能失敗。

使用共用運算單元集區不會產生額外費用，但改用`BACKGROUND`預留資源可分配專用資源集區，提供更穩定的效能，並提升 BigQuery 中重新整理作業的可靠性，以及整體查詢效率。

設定陳舊間隔和中繼資料快取模式值之前，請先考量這些值之間的互動方式。請見以下範例：

* 如果您要手動重新整理資料表的中繼資料快取，並將過時間隔設為 2 天，則必須每 2 天或更短的時間執行 `BQ.REFRESH_EXTERNAL_METADATA_CACHE` 系統程序，才能讓針對資料表執行的作業使用快取中繼資料。
* 如果您自動重新整理資料表的 Metadata 快取，並將過時間隔設為 30 分鐘，如果 Metadata 快取重新整理時間較長，可能需要 30 到 60 分鐘，則您對資料表執行的部分作業可能會從 Amazon S3 讀取資料。

如要查詢中繼資料重新整理工作相關資訊，請查詢[`INFORMATION_SCHEMA.JOBS` 檢視區塊](https://docs.cloud.google.com/bigquery/docs/information-schema-jobs?hl=zh-tw)，如下列範例所示：

```
SELECT *
FROM `region-us.INFORMATION_SCHEMA.JOBS_BY_PROJECT`
WHERE job_id LIKE '%metadata_cache_refresh%'
AND creation_time > TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 6 HOUR)
ORDER BY start_time DESC
LIMIT 10;
```

詳情請參閱「[中繼資料快取](https://docs.cloud.google.com/bigquery/docs/metadata-caching?hl=zh-tw)」。

### 具體化檢視表搭配啟用快取的資料表

您可以[在啟用 Amazon Simple Storage Service (Amazon S3) 中繼資料快取功能的資料表上使用具體化檢視區塊](https://docs.cloud.google.com/bigquery/docs/materialized-views-intro?hl=zh-tw#biglake)，查詢儲存在 Amazon S3 中的結構化資料時，就能提升效能和效率。這些具體化檢視區塊的運作方式與 BigQuery 管理的儲存空間資料表上的具體化檢視區塊相同，包括[自動重新整理](https://docs.cloud.google.com/bigquery/docs/materialized-views-manage?hl=zh-tw#automatic-refresh)和[智慧微調](https://docs.cloud.google.com/bigquery/docs/materialized-views-use?hl=zh-tw#smart_tuning)等優點。

如要在[支援的 BigQuery 區域](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw#omni-loc)中，將具體化檢視表中的 Amazon S3 資料用於聯結，請[建立具體化檢視表的副本](https://docs.cloud.google.com/bigquery/docs/load-data-using-cross-cloud-transfer?hl=zh-tw#materialized_view_replicas)。您只能透過[授權的具體化檢視表](https://docs.cloud.google.com/bigquery/docs/authorized-views?hl=zh-tw)建立具體化檢視表副本。

## 限制

除了 [BigLake 資料表的限制](https://docs.cloud.google.com/bigquery/docs/biglake-intro?hl=zh-tw#limitations)外，下列限制也適用於 BigQuery Omni，包括以 Amazon S3 和 Blob 儲存體資料為基礎的 BigLake 資料表：

* Standard 和 Enterprise Plus 版本不支援在任何 [BigQuery Omni 區域](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw#omni-loc)中使用資料。如要進一步瞭解版本，請參閱 [BigQuery 版本簡介](https://docs.cloud.google.com/bigquery/docs/editions-intro?hl=zh-tw)。
* 以 Amazon S3 和 Blob Storage 資料為基礎的 BigLake 資料表，無法使用 `OBJECT_PRIVILEGES`、`STREAMING_TIMELINE_BY_*`、`TABLE_SNAPSHOTS`、`TABLE_STORAGE`、`TABLE_CONSTRAINTS`、`KEY_COLUMN_USAGE`、`CONSTRAINT_COLUMN_USAGE` 和 `PARTITIONS`
  [`INFORMATION_SCHEMA` 檢視畫面](https://docs.cloud.google.com/bigquery/docs/information-schema-intro?hl=zh-tw)。
* Blob 儲存體不支援具體化檢視區塊。
* 系統不支援 JavaScript UDF。
* 系統不支援下列 SQL 陳述式：

  + [BigQuery ML](https://docs.cloud.google.com/bigquery/docs/bqml-introduction?hl=zh-tw) 陳述式。
  + [資料定義語言 (DDL) 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw)，需要 BigQuery 管理的資料。舉例來說，系統支援 `CREATE EXTERNAL TABLE`、`CREATE SCHEMA` 或 `CREATE RESERVATION`，但不支援 `CREATE TABLE`。
  + [資料操縱語言 (DML) 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/dml-syntax?hl=zh-tw)。
* 查詢及讀取目的地暫時性資料表時，請注意下列限制：

  + 系統不支援使用 `SELECT` 陳述式查詢目的地暫時資料表。
* [排程查詢](https://docs.cloud.google.com/bigquery/docs/scheduling-queries?hl=zh-tw)
  僅支援透過 API 或 CLI 方法。查詢的「目的地資料表」選項已停用。僅允許 [`EXPORT DATA`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/export-statements?hl=zh-tw) 查詢。
* [BigQuery Storage API](https://docs.cloud.google.com/bigquery/docs/reference/storage/libraries?hl=zh-tw) 不適用於 [BigQuery Omni 區域](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw#omni-loc)。
* 如果查詢使用 `ORDER BY` 子句，且結果大小超過 256 MB，查詢就會失敗。如要解決這個問題，請縮減結果大小，或從查詢中移除 `ORDER BY` 子句。如要進一步瞭解 BigQuery Omni 配額，請參閱「[配額與限制](#quotas_and_limits)」。
* 不支援將客戶管理的加密金鑰 (CMEK) 與資料集和外部資料表搭配使用。

## 定價

如要瞭解 BigQuery Omni 的定價和限時優惠，請參閱 [BigQuery Omni 定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#bqomni)。

## 配額與限制

如要瞭解 BigQuery Omni 配額，請參閱「[配額與限制](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#query_jobs)」。

如果查詢結果大於 20 GiB，請考慮將結果匯出至 [Amazon S3](https://docs.cloud.google.com/bigquery/docs/omni-aws-export-results-to-s3?hl=zh-tw) 或 [Blob Storage](https://docs.cloud.google.com/bigquery/docs/omni-azure-export-results-to-azure-storage?hl=zh-tw)。
如要瞭解 BigQuery Connection API 的配額，請參閱 [BigQuery Connection API](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#connection_api)。

## 位置

BigQuery Omni 會在與包含所查詢資料表的資料集相同位置處理查詢。建立資料集後，就無法變更位置。您的資料會儲存在 AWS 或 Azure 帳戶中。BigQuery Omni 區域支援 Enterprise 版本的預留項目和隨選運算 (分析) 定價。如要進一步瞭解版本，請參閱「[BigQuery 版本簡介](https://docs.cloud.google.com/bigquery/docs/editions-intro?hl=zh-tw)」。

|  | 地區說明 | 地區名稱 | 共置 BigQuery 區域 |
| --- | --- | --- | --- |
| **AWS** | | | |
|  | AWS - 美國東部 (北維吉尼亞州) | `aws-us-east-1` | `us-east4` |
|  | AWS - 美國西部 (奧勒岡州) | `aws-us-west-2` | `us-west1` |
|  | AWS - 亞太地區 (首爾) | `aws-ap-northeast-2` | `asia-northeast3` |
|  | AWS - 亞太地區 (雪梨) | `aws-ap-southeast-2` | `australia-southeast1` |
|  | AWS - 歐洲 (愛爾蘭) | `aws-eu-west-1` | `europe-west1` |
|  | AWS - 歐洲 (法蘭克福) | `aws-eu-central-1` | `europe-west3` |
| **Azure** | | | |
|  | Azure - 美國東部 2 | `azure-eastus2` | `us-east4` |

## 後續步驟

* 瞭解如何[連結至 Amazon S3](https://docs.cloud.google.com/bigquery/docs/omni-aws-create-connection?hl=zh-tw) 和 [Blob 儲存體](https://docs.cloud.google.com/bigquery/docs/omni-azure-create-connection?hl=zh-tw)。
* 瞭解如何建立 [Amazon S3](https://docs.cloud.google.com/bigquery/docs/omni-aws-create-external-table?hl=zh-tw) 和 [Blob 儲存體](https://docs.cloud.google.com/bigquery/docs/omni-azure-create-external-table?hl=zh-tw) BigLake 資料表。
* 瞭解如何查詢 [Amazon S3](https://docs.cloud.google.com/bigquery/docs/query-aws-data?hl=zh-tw) 和 [Blob 儲存體](https://docs.cloud.google.com/bigquery/docs/query-azure-data?hl=zh-tw) BigLake 資料表。
* 瞭解如何使用[跨雲端聯結](https://docs.cloud.google.com/bigquery/docs/biglake-intro?hl=zh-tw#cross-cloud_joins)，將 [Amazon S3](https://docs.cloud.google.com/bigquery/docs/query-aws-data?hl=zh-tw) 和 [Blob 儲存體](https://docs.cloud.google.com/bigquery/docs/query-azure-data?hl=zh-tw) BigLake 資料表與 Google Cloud 資料表聯結。
* 瞭解如何[將查詢結果匯出至 Amazon S3](https://docs.cloud.google.com/bigquery/docs/omni-aws-export-results-to-s3?hl=zh-tw) 和 [Blob 儲存體](https://docs.cloud.google.com/bigquery/docs/omni-azure-export-results-to-azure-storage?hl=zh-tw)。
* 瞭解如何[將資料從 Amazon S3 移轉至 BigQuery](https://docs.cloud.google.com/bigquery/docs/omni-aws-cross-cloud-transfer?hl=zh-tw)，以及如何[將資料從 Blob 儲存空間移轉至 BigQuery](https://docs.cloud.google.com/bigquery/docs/omni-azure-cross-cloud-transfer?hl=zh-tw)。
* 瞭解如何[設定 VPC Service Controls 範圍](https://docs.cloud.google.com/bigquery/docs/omni-vpc-sc?hl=zh-tw)。
* 瞭解如何[指定位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw#specify_locations)




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-02 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-02 (世界標準時間)。"],[],[]]