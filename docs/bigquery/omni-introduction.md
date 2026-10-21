Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# BigQuery Omni 簡介

**注意：** 如果預留項目是以特定 BigQuery 版本建立，可能無法使用這項功能。如要進一步瞭解各版本啟用的功能，請參閱「[BigQuery 版本簡介](https://docs.cloud.google.com/bigquery/docs/editions-intro?hl=zh-tw)」。

有了 BigQuery Omni，您就能使用 BigLake 資料表，對儲存在 Amazon Simple Storage Service (Amazon S3) 或 Azure Blob Storage 的資料執行 BigQuery 分析。

許多機構會將資料儲存在多個公有雲中。通常這些資料最後會遭到孤立，因為難以取得所有資料的洞察。您希望使用多雲端資料工具分析資料，這項工具必須便宜、快速，且不會產生分散式資料治理的額外負擔。使用 BigQuery Omni，我們就能透過統一介面減少這些摩擦。

如要對外部資料執行 BigQuery 分析，您必須先[連線至 Amazon S3](https://docs.cloud.google.com/bigquery/docs/omni-aws-create-connection?hl=zh-tw) 或 [Blob 儲存體](https://docs.cloud.google.com/bigquery/docs/omni-azure-create-connection?hl=zh-tw)。如要查詢外部資料，您必須建立參照 Amazon S3 或 Blob 儲存體資料的 [BigLake 資料表](https://docs.cloud.google.com/bigquery/docs/biglake-intro?hl=zh-tw)。

## BigQuery Omni 工具

您可以使用下列 BigQuery Omni 工具，對外部資料執行 BigQuery 分析：

* [BigQuery Omni 彙整](https://docs.cloud.google.com/bigquery/docs/biglake-intro?hl=zh-tw#cross-cloud_joins)：直接從 BigQuery 區域執行查詢，彙整 BigQuery Omni 區域的資料。
* [BigQuery Omni materialized view](https://docs.cloud.google.com/bigquery/docs/load-data-using-cross-cloud-transfer?hl=zh-tw#materialized_view_replicas)：使用 [materialized view 副本](https://docs.cloud.google.com/bigquery/docs/load-data-using-cross-cloud-transfer?hl=zh-tw#materialized_view_replicas)，持續複製 BigQuery Omni 區域的資料。支援資料篩選。
* [使用 `SELECT` 進行 BigQuery Omni 移轉](https://docs.cloud.google.com/bigquery/docs/load-data-using-cross-cloud-transfer?hl=zh-tw)：在 BigQuery Omni 區域中使用 `CREATE TABLE AS SELECT` 或 `INSERT INTO SELECT` 陳述式執行查詢，並將結果移至 BigQuery 區域。
* [使用 `LOAD`](https://docs.cloud.google.com/bigquery/docs/load-data-using-cross-cloud-transfer?hl=zh-tw) 進行 BigQuery Omni 移轉作業：使用 [`LOAD DATA` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/load-statements?hl=zh-tw)，直接從 Amazon Simple Storage Service (Amazon S3) 或 Azure Blob Storage 將資料載入 BigQuery

下表列出各項 BigQuery Omni 工具的主要功能和特色：

|  | BigQuery Omni 彙整 | BigQuery Omni materialized view | 使用 `SELECT` 進行 BigQuery Omni 移轉 | 使用 `LOAD` 進行 BigQuery Omni 移轉 |
| --- | --- | --- | --- | --- |
| 建議用法 | 查詢一次性使用的外部資料，您可以將這些資料與本機資料表彙整，或彙整兩個不同 BigQuery Omni 區域之間的資料，例如 AWS 和 Azure Blob 儲存體區域。如果資料量不大，且快取並非主要需求，請使用 BigQuery Omni 彙整 | 設定重複或排定的查詢，持續以遞增方式移轉外部資料，其中快取是關鍵需求。例如，如要維護資訊主頁 | 從 BigQuery Omni 區域向 BigQuery 區域查詢外部資料，用於一次性用途，且需要手動控制快取和查詢最佳化等功能，以及使用 BigQuery Omni 彙整或 BigQuery Omni materialized view 不支援的複雜查詢 | 原封不動遷移大型資料集，不需篩選，並使用排定的查詢移動原始資料 |
| 支援在移動資料前進行篩選 | 可以。特定查詢運算子設有限制。詳情請參閱「[BigQuery Omni 彙整限制](https://docs.cloud.google.com/bigquery/docs/biglake-intro?hl=zh-tw#cross-cloud_join_limitations)」 | 可以。特定查詢運算子 (例如匯總函式和 `UNION` 運算子) 設有限制 | 可以。查詢運算子數量不限 | 否 |
| 轉移大小限制 | [每次轉移 60 GB](https://docs.cloud.google.com/bigquery/docs/biglake-intro?hl=zh-tw#cross-cloud_join_limitations) (每個對遠端區域的子查詢都會產生一次轉移) | 不限 | [每次轉移 60 GB](https://docs.cloud.google.com/bigquery/docs/load-data-using-cross-cloud-transfer?hl=zh-tw#limitations_2) (每個對遠端區域的子查詢都會產生一次轉移) | 不限 |
| 資料移轉壓縮 | 線路壓縮 | 資料欄 | 線路壓縮 | 電線壓合 |
| 快取 | 不支援 | 支援[已啟用快取的資料表和 materialized view](https://docs.cloud.google.com/bigquery/docs/omni-introduction?hl=zh-tw#cache-enabled_tables_with_materialized_views) | 不支援 | 不支援 |
| 輸出定價 | AWS 輸出和跨洲費用 | AWS 輸出和跨洲費用 | AWS 輸出和跨洲費用 | AWS 輸出和跨洲費用 |
| 資料移轉的運算用量 | 使用來源 AWS 或 Azure Blob 儲存體區域中的運算單元 (預留或隨選) | 未使用 | 使用來源 AWS 或 Azure Blob 儲存體區域中的運算單元 (預留或隨選) | 未使用 |
| 篩選運算用量 | 使用來源 AWS 或 Azure Blob 儲存體區域中的運算單元 (預留或隨選) | 使用來源 AWS 或 Azure Blob 儲存體區域中的運算單元 (預留或隨選)，運算本機 materialized view 和中繼資料 | 使用來源 AWS 或 Azure Blob 儲存體區域中的運算單元 (預留或隨選) | 未使用 |
| 增量移轉作業 | 不支援 | 支援非匯總 materialized view | 不支援 | 不支援 |

您也可以考慮下列替代方案，將資料從 Amazon Simple Storage Service (Amazon S3) 或 Azure Blob Storage 移轉至 Google Cloud：

* [Storage 移轉服務](https://docs.cloud.google.com/storage-transfer?hl=zh-tw)：在 Google Cloud 和 Amazon Simple Storage Service (Amazon S3) 或 Azure Blob Storage 之間，轉移物件和檔案儲存空間中的資料。
* [BigQuery 資料移轉服務](https://docs.cloud.google.com/bigquery/docs/dts-introduction?hl=zh-tw)：設定自動資料移轉，按照指定的時間和設定將資料移至 BigQuery。支援[多種來源](https://docs.cloud.google.com/bigquery/docs/dts-introduction?hl=zh-tw#supported_data_sources)，適合用於資料遷移。BigQuery 資料移轉服務不支援篩選功能。

## 架構

BigQuery 的架構會將運算與儲存空間分開，因此可視需要水平擴充，處理極大型工作負載。BigQuery Omni 則在其他雲端中執行 BigQuery 查詢引擎，進一步擴充這項架構。因此，您不必實際將資料移至 BigQuery 儲存空間。處理作業會在資料所在位置進行。

查詢結果可以透過安全連線傳回 Google Cloud ，例如顯示在 Google Cloud 控制台中。或者，您也可以直接將結果寫入 Amazon S3 bucket 或 Blob Storage。在這種情況下，查詢結果不會跨雲端移動。

BigQuery Omni 會使用標準 AWS IAM 角色或 Azure Active Directory 主體，存取訂閱項目中的資料。您可以將讀取或寫入權限委派給 BigQuery Omni，並隨時撤銷存取權。

**注意：** 只有在您想將查詢結果寫回 Amazon S3 bucket 或 Blob Storage 容器時，才需要寫入權限。

### 查詢資料時的資料流程

下圖說明下列查詢的資料如何在 Google Cloud 與 AWS 或 Azure 之間移動：

* `SELECT` 陳述式
* `CREATE EXTERNAL TABLE` 陳述式

**圖 1：** Google Cloud 和 AWS 或 Azure 之間的資料移動，用於查詢。

1. BigQuery 控制層會透過Google Cloud 控制台、bq 指令列工具、API 方法或用戶端程式庫，接收您提交的查詢工作。
2. BigQuery 控制層會將查詢工作傳送至 AWS 或 Azure 上的 BigQuery 資料層進行處理。
3. BigQuery 資料層會透過 VPN 連線，從控制層接收查詢。
4. BigQuery 資料層會從 Amazon S3 bucket 或 Blob 儲存體讀取資料表資料。
5. BigQuery 資料層會對資料表資料執行查詢工作。資料表資料會在指定的 AWS 或 Azure 區域處理。
6. 查詢結果會透過 VPN 連線
   從資料層傳輸至控制層
7. BigQuery 控制層會接收查詢工作結果，並顯示給您，做為查詢工作的回應。這類資料最多會保留 24 小時。
8. 系統會傳回查詢結果。

詳情請參閱「[查詢 Amazon S3 資料](https://docs.cloud.google.com/bigquery/docs/omni-aws-create-external-table?hl=zh-tw)」和「[Blob 儲存體資料](https://docs.cloud.google.com/bigquery/docs/omni-azure-create-external-table?hl=zh-tw)」。

### 匯出資料時的資料流程

下圖說明在 `EXPORT DATA` 陳述式期間，資料如何在 Google Cloud 與 AWS 或 Azure 之間移動。

**圖 2：** Google Cloud 和 AWS 或 Azure 之間的資料移動，用於匯出查詢。

1. BigQuery 控制層會透過 Google Cloud 控制台、bq 指令列工具、API 方法或用戶端程式庫，接收您傳送的匯出查詢工作。查詢包含 Amazon S3 bucket 或 Blob Storage 中查詢結果的目的地路徑。
2. BigQuery 控制層會將匯出查詢工作傳送至 BigQuery 資料層 (位於 AWS 或 Azure)，以便進行處理。
3. BigQuery 資料層會透過 VPN 連線，從控制層接收匯出查詢。
4. BigQuery 資料層會從 Amazon S3 bucket 或 Blob 儲存體讀取資料表資料。
5. BigQuery 資料層會對資料表資料執行查詢工作。資料表資料會在指定的 AWS 或 Azure 區域處理。
6. BigQuery 會將查詢結果寫入 Amazon S3 bucket 或 Blob Storage 中的指定目的地路徑。

詳情請參閱「[將查詢結果匯出至 Amazon S3](https://docs.cloud.google.com/bigquery/docs/omni-aws-export-results-to-s3?hl=zh-tw)」和「[Blob 儲存體](https://docs.cloud.google.com/bigquery/docs/omni-azure-export-results-to-azure-storage?hl=zh-tw)」。

## 優點

**效能：**資料不會跨雲端複製，且查詢會在資料所在區域執行，因此能更快取得洞察資訊。

**費用：**由於資料不會移動，因此可以節省傳出資料移轉費用。由於查詢是在 Google 代管的叢集上執行，因此 AWS 或 Azure 帳戶不會產生與 BigQuery Omni 數據分析相關的額外費用。系統只會根據 BigQuery 定價模式，向您收取執行查詢的費用。

**安全性與資料治理：**您可以在自己的 AWS 或 Azure 訂閱項目中管理資料。您不必將原始資料移出或複製出公有雲。所有運算作業都會在 BigQuery 多租戶服務中進行，該服務與資料在相同區域內執行。

**無伺服器架構**：與 BigQuery 的其他部分一樣，BigQuery Omni 也是無伺服器產品。Google 會部署及管理執行 BigQuery Omni 的叢集。您不需要佈建任何資源或管理任何叢集。

**輕鬆管理：**BigQuery Omni 透過 Google Cloud提供統一的管理介面。BigQuery Omni 可使用您現有的 Google Cloud 帳戶和 BigQuery 專案。您可以在 Google Cloud 控制台編寫 GoogleSQL 查詢，查詢 AWS 或 Azure 中的資料，並在 Google Cloud 控制台查看結果。

**BigQuery Omni 移轉作業。**您可以從 S3 bucket 和 Blob 儲存體，將資料載入標準 BigQuery 資料表。詳情請參閱「[移轉 Amazon S3 資料](https://docs.cloud.google.com/bigquery/docs/omni-aws-cross-cloud-transfer?hl=zh-tw)」和「[將 Blob 儲存體資料移轉至 BigQuery](https://docs.cloud.google.com/bigquery/docs/omni-azure-cross-cloud-transfer?hl=zh-tw)」。

## 中繼資料快取，提升效能

您可以運用快取中繼資料，提升參照 Amazon S3 資料的 BigLake 資料表查詢效能。如果需要處理大量檔案，或資料已依 Apache Hive 分區，這項功能就特別實用。

BigQuery 使用 CMETA 做為分散式中繼資料系統，有效率地處理大型資料表。CMETA 提供資料欄和區塊層級的精細中繼資料，可透過系統資料表存取。這個系統會最佳化資料存取和處理作業，進而提升查詢效能。為進一步提升大型資料表的查詢效能，BigQuery 會維護中繼資料快取。CMETA 重新整理工作會讓這個快取保持在最新狀態。

中繼資料包括檔案名稱、分區資訊，以及檔案的實體中繼資料，例如資料列數。您可以選擇是否要啟用資料表的中繼資料快取功能。含有大量檔案和 Apache Hive 分區篩選器的查詢，最能發揮中繼資料快取的效益。

如未啟用中繼資料快取功能，資料表查詢就必須讀取外部資料來源，才能取得物件中繼資料。讀取這類資料會增加查詢延遲時間；從外部資料來源列出數百萬個檔案可能需要幾分鐘的時間。啟用中繼資料快取功能後，查詢作業就不必列出外部資料來源中的檔案，而且能更快分區及剪除檔案。

中繼資料快取也與 Cloud Storage 物件版本管理功能整合。填入或重新整理快取時，系統會根據當時 Cloud Storage 物件的使用中版本擷取中繼資料。因此，啟用中繼資料快取的查詢會讀取與特定快取物件版本對應的資料，即使 Cloud Storage 中有較新的版本也一樣。如要存取 Cloud Storage 中後續更新的物件版本資料，必須重新整理中繼資料快取。

有兩個屬性可控制這項功能：

* **最大過時時間**指定查詢使用快取中繼資料的時間。
* **中繼資料快取模式**會指定中繼資料的收集方式。

啟用中繼資料快取功能後，您可以指定資料表作業可接受的中繼資料過時時間間隔上限。舉例來說，如果您指定 1 小時的間隔，則資料表作業會使用過去一小時內重新整理的快取中繼資料。如果快取的中繼資料超過這個時間，作業就會改為從 Amazon S3 擷取中繼資料。您可以指定 30 分鐘至 7 天的過時間隔。

為 BigLake 或物件資料表啟用中繼資料快取時，BigQuery 會觸發中繼資料生成重新整理工作。您可以選擇自動或手動重新整理快取：

* 如果是自動重新整理，快取會按照系統定義的時間間隔重新整理，通常介於 30 到 60 分鐘之間。如果 Amazon S3 中的檔案會不定期新增、刪除或修改，自動重新整理快取是不錯的做法。如需控制重新整理的時間點 (例如在擷取、轉換和載入工作結束時觸發重新整理)，請使用手動重新整理。
* 如要手動重新整理，請執行 [`BQ.REFRESH_EXTERNAL_METADATA_CACHE` 系統程序](https://docs.cloud.google.com/bigquery/docs/reference/system-procedures?hl=zh-tw#bqrefresh_external_metadata_cache)，按照符合需求的時間表重新整理中繼資料快取。如果 Amazon S3 中的檔案是以已知間隔新增、刪除或修改 (例如管道的輸出內容)，手動重新整理快取是不錯的做法。

  如果同時發出多個手動重新整理要求，只有一個會成功。

如果未重新整理，中繼資料快取會在 7 天後過期。

手動和自動快取重新整理都會以 [`INTERACTIVE`](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw) 查詢優先順序執行。

### 使用 `BACKGROUND` 預留項目

如果您選擇使用自動重新整理功能，建議您建立[預留項目](https://docs.cloud.google.com/bigquery/docs/reservations-intro?hl=zh-tw)，然後為執行中繼資料快取重新整理工作的專案建立[具有 `BACKGROUND` 工作類型的指派作業](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#assignments)。使用 `BACKGROUND` 預留項目時，重新整理工作會使用專屬資源集區，因此不會與使用者查詢競爭資源，也不會因資源不足而失敗。

雖然使用共用運算單元集區不會產生額外費用，但改用 `BACKGROUND` 預留項目可分配專屬資源集區，提供更穩定的效能，並提高 BigQuery 重新整理工作的可靠性和整體查詢效率。

設定過時時間間隔和中繼資料快取模式值之前，請先考量兩者之間的互動方式。請見以下範例：

* 如果您手動重新整理資料表的中繼資料快取，並將過時時間間隔設為 2 天，則必須每 2 天 (或更短時間) 執行一次 `BQ.REFRESH_EXTERNAL_METADATA_CACHE` 系統程序，才能對資料表執行作業，使用快取的中繼資料。
* 如果您自動重新整理資料表的詮釋資料快取，並將過時時間間隔設為 30 分鐘，則對資料表執行的部分作業可能會從 Amazon S3 讀取，前提是詮釋資料快取重新整理作業的時間超過一般的 30 到 60 分鐘。

如要查看中繼資料重新整理工作的相關資訊，請查詢 [`INFORMATION_SCHEMA.JOBS` 檢視表](https://docs.cloud.google.com/bigquery/docs/information-schema-jobs?hl=zh-tw)，如下例所示：

```
SELECT *
FROM `region-us.INFORMATION_SCHEMA.JOBS_BY_PROJECT`
WHERE job_id LIKE '%metadata_cache_refresh%'
AND creation_time > TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 6 HOUR)
ORDER BY start_time DESC
LIMIT 10;
```

詳情請參閱「[中繼資料快取](https://docs.cloud.google.com/bigquery/docs/metadata-caching?hl=zh-tw)」。

### 啟用快取且含 materialized view 的資料表

您可以[對已啟用 Amazon Simple Storage Service (Amazon S3) 中繼資料快取的資料表使用 materialized view](https://docs.cloud.google.com/bigquery/docs/materialized-views-intro?hl=zh-tw#biglake)，提高查詢 Amazon S3 結構化資料的效能和效率。這些 materialized view 的運作方式與 BigQuery 代管儲存空間資料表的 materialized view 相同，包括[自動重新整理](https://docs.cloud.google.com/bigquery/docs/materialized-views-manage?hl=zh-tw#automatic-refresh)和[智慧微調](https://docs.cloud.google.com/bigquery/docs/materialized-views-use?hl=zh-tw#smart_tuning)等優點。

如要將 materialized view 中的 Amazon S3 資料，提供給[支援的 BigQuery 區域](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw#omni-loc)進行 join 作業，請[建立 materialized view 的副本](https://docs.cloud.google.com/bigquery/docs/load-data-using-cross-cloud-transfer?hl=zh-tw#materialized_view_replicas)。您只能透過[已授權的 materialized view](https://docs.cloud.google.com/bigquery/docs/authorized-views?hl=zh-tw) 建立 materialized view 副本。

## 限制

除了 [BigLake 資料表的限制](https://docs.cloud.google.com/bigquery/docs/biglake-intro?hl=zh-tw#limitations)之外，BigQuery Omni (包括以 Amazon S3 和 Blob 儲存體資料為基礎的 BigLake 資料表) 也適用下列限制：

* Standard 和 Enterprise Plus 版本不支援在任何 [BigQuery Omni 區域](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw#omni-loc)處理資料。如要進一步瞭解版本，請參閱「[BigQuery 版本簡介](https://docs.cloud.google.com/bigquery/docs/editions-intro?hl=zh-tw)」。
* `OBJECT_PRIVILEGES`、`STREAMING_TIMELINE_BY_*`、`TABLE_SNAPSHOTS`、`TABLE_STORAGE`、`TABLE_CONSTRAINTS`、`KEY_COLUMN_USAGE`、`CONSTRAINT_COLUMN_USAGE` 和 `PARTITIONS`
  [`INFORMATION_SCHEMA` 檢視表](https://docs.cloud.google.com/bigquery/docs/information-schema-intro?hl=zh-tw)不適用於以 Amazon S3 和 Blob Storage 資料為基礎的 BigLake 資料表。
* Blob 儲存體不支援 materialized view。
* 不支援 JavaScript UDF。
* 不支援下列 SQL 陳述式：

  + [BigQuery ML](https://docs.cloud.google.com/bigquery/docs/bqml-introduction?hl=zh-tw) 陳述式。
  + 需要 BigQuery 代管資料的[資料定義語言 (DDL) 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw)。例如，系統支援 `CREATE EXTERNAL TABLE`、`CREATE SCHEMA` 或 `CREATE RESERVATION`，但不支援 `CREATE TABLE`。
  + [data manipulation language (DML) 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/dml-syntax?hl=zh-tw)。
* 查詢及讀取目的地臨時資料表時，須遵守下列限制：

  + 不支援使用 `SELECT` 陳述式查詢目的地臨時資料表。
* [排定查詢](https://docs.cloud.google.com/bigquery/docs/scheduling-queries?hl=zh-tw)僅支援 API 或 CLI 方法。查詢的「destination table」(目的地資料表) 選項已停用。只能使用 [`EXPORT DATA`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/export-statements?hl=zh-tw) 查詢。
* [BigQuery Omni 區域](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw#omni-loc)不提供 [BigQuery Storage API](https://docs.cloud.google.com/bigquery/docs/reference/storage/libraries?hl=zh-tw)。
* 如果查詢使用 `ORDER BY` 子句，且結果大小超過 256 MB，查詢就會失敗。如要解決這個問題，請縮減結果大小，或從查詢中移除 `ORDER BY` 子句。如要進一步瞭解 BigQuery Omni 配額，請參閱「[配額與限制](#quotas_and_limits)」。
* 不支援對資料集和外部資料表使用客戶自行管理的加密金鑰 (CMEK)。

## 定價

如要瞭解 BigQuery Omni 的定價和限時優惠，請參閱「[BigQuery Omni 定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#bqomni)」。

## 配額與限制

如要瞭解 BigQuery Omni 配額，請參閱「[配額與限制](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#query_jobs)」。

如果查詢結果超過 20 GiB，建議將結果匯出至 [Amazon S3](https://docs.cloud.google.com/bigquery/docs/omni-aws-export-results-to-s3?hl=zh-tw) 或 [Blob 儲存體](https://docs.cloud.google.com/bigquery/docs/omni-azure-export-results-to-azure-storage?hl=zh-tw)。如要瞭解 BigQuery Connection API 的配額，請參閱「[BigQuery Connection API](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#connection_api)」。

## 位置

BigQuery Omni 處理查詢的位置，與包含查詢資料表的資料集相同。資料集建立後即無法變更位置。您的資料會保留在 AWS 或 Azure 帳戶中。BigQuery Omni 區域支援 Enterprise 版本預留項目和隨選運算 (分析) 定價。如要進一步瞭解版本，請參閱「[BigQuery 版本簡介](https://docs.cloud.google.com/bigquery/docs/editions-intro?hl=zh-tw)」。

|  | 地區說明 | 區域名稱 | 共置 BigQuery 區域 |
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
* 瞭解如何使用 [BigQuery Omni 彙整](https://docs.cloud.google.com/bigquery/docs/biglake-intro?hl=zh-tw#cross-cloud_joins)，將 [Amazon S3](https://docs.cloud.google.com/bigquery/docs/query-aws-data?hl=zh-tw) 和 [Blob 儲存體](https://docs.cloud.google.com/bigquery/docs/query-azure-data?hl=zh-tw) BigLake 資料表與 Google Cloud 資料表彙整。
* 瞭解如何[將查詢結果匯出至 Amazon S3](https://docs.cloud.google.com/bigquery/docs/omni-aws-export-results-to-s3?hl=zh-tw) 和 [Blob 儲存體](https://docs.cloud.google.com/bigquery/docs/omni-azure-export-results-to-azure-storage?hl=zh-tw)。
* 瞭解如何[從 Amazon S3](https://docs.cloud.google.com/bigquery/docs/omni-aws-cross-cloud-transfer?hl=zh-tw) 和 [Blob 儲存體將資料移轉至 BigQuery](https://docs.cloud.google.com/bigquery/docs/omni-azure-cross-cloud-transfer?hl=zh-tw)。
* 瞭解如何[設定 VPC Service Controls 範圍](https://docs.cloud.google.com/bigquery/docs/omni-vpc-sc?hl=zh-tw)。
* 瞭解如何[指定位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw#specify_locations)




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-10-19 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-10-19 (世界標準時間)。"],[],[]]