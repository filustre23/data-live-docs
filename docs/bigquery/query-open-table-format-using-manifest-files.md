* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 使用資訊清單查詢開放式資料表格式

本文說明如何使用資訊清單檔案，查詢以開放式資料表格式 (例如 [Apache Hudi](https://github.com/apache/hudi) 和 [Delta Lake](https://github.com/delta-io)) 儲存的資料。

部分開放資料表格式 (例如 Hudi 和 Delta Lake) 會將目前狀態匯出為一或多個資訊清單檔案。資訊清單檔案包含構成資料表的資料檔案清單。BigQuery 支援資訊清單，因此您可以查詢及載入以開放資料表格式儲存的資料。

## 事前準備

* 啟用 BigQuery Connection、BigQuery Reservation 和 BigLake API。

  **啟用 API 時所需的角色**

  如要啟用 API，您需要服務使用情形管理員 IAM 角色 (`roles/serviceusage.serviceUsageAdmin`)，其中包含 `serviceusage.services.enable` 權限。[瞭解如何授予角色](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)。

  [啟用 API](https://console.cloud.google.com/flows/enableapi?apiid=bigqueryconnection.googleapis.com%2Cbiglake.googleapis.com%2C%5Cnbigqueryreservation.googleapis.com&%3Bredirect=https%3A%2F%2Fconsole.cloud.google.com&hl=zh-tw)
* 如要建立 BigLake 資料表，可以使用下列其中一種方法執行 Spark 指令：

  + [建立 Managed Service for Apache Spark 叢集](https://docs.cloud.google.com/dataproc/docs/guides/create-cluster?hl=zh-tw)。如要查詢 Hudi 資料表，請將 `--optional-components` 欄位設為 `HUDI`。如要查詢 Delta 資料表，請將 `--optional-components` 設為 `Presto`。
  + 在 BigQuery 中使用 Spark 預存程序。請按照以下步驟操作：

    1. [建立 Spark 連線](https://docs.cloud.google.com/bigquery/docs/connect-to-spark?hl=zh-tw#create-spark-connection)。
    2. [為該連線設定存取控管機制](https://docs.cloud.google.com/bigquery/docs/connect-to-spark?hl=zh-tw#grant-access)。
* 如要在 Cloud Storage 中儲存資訊清單檔案，請[建立 Cloud Storage 值區](https://docs.cloud.google.com/storage/docs/creating-buckets?hl=zh-tw)。您必須連線至 Cloud Storage bucket，才能存取資訊清單檔案。請按照以下步驟操作：

  1. [建立 Cloud 資源連結](https://docs.cloud.google.com/bigquery/docs/create-cloud-resource-connection?hl=zh-tw#create-cloud-resource-connection)。
  2. [設定該連結的存取權](https://docs.cloud.google.com/bigquery/docs/create-cloud-resource-connection?hl=zh-tw#access-storage)。

### 必要的角色

如要根據 Hudi 和 Delta Lake 資料查詢 BigLake 資料表，請確認您具備下列角色：

* BigQuery 連線使用者 (`roles/bigquery.connectionUser`)
* BigQuery 資料檢視者 (`roles/bigquery.dataViewer`)
* BigQuery 使用者 (`roles/bigquery.user`)

您也可以查詢 Hudi 外部資料表。不過，建議您[將外部資料表升級為 BigLake](#upgrade-external-to-biglake)。
如要查詢 Hudi 外部資料表，請確保您具備下列角色：

* BigQuery 資料檢視者 (`roles/bigquery.dataViewer`)
* BigQuery 使用者 (`roles/bigquery.user`)
* Storage 物件檢視者 (`roles/storage.objectViewer`)

視權限而定，您可以將這些角色授予自己，或請系統管理員授予您這些角色。如要進一步瞭解如何授予角色，請參閱「[查看可針對資源授予的角色](https://docs.cloud.google.com/iam/docs/viewing-grantable-roles?hl=zh-tw)」。

如要查看查詢 BigLake 表格所需的確切權限，請展開「必要權限」部分：

#### 所需權限

* `bigquery.connections.use`
* `bigquery.jobs.create`
* `bigquery.readsessions.create` (只有在[使用 BigQuery Storage Read API 讀取資料](https://docs.cloud.google.com/bigquery/docs/reference/storage?hl=zh-tw)時才需要)
* `bigquery.tables.get`
* `bigquery.tables.getData`

您或許還可透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)取得這些權限。

## 查詢 Hudi 工作負載

**重要事項：** 如要執行下列章節所述的動作，您必須使用 [Hudi-BigQuery 連接器](https://hudi.apache.org/docs/gcp_bigquery/) 0.14.0 以上版本，或 Managed Service for Apache Spark 2.1 中的 Hudi 元件，該元件已回溯移植適當版本的連接器。在舊版中，連接器會在資訊清單檔案上建立檢視區塊，但這並非查詢效能的最佳做法。如果您使用舊版連接器，則必須捨棄 BigQuery 中代表 Hudi 資料表的現有檢視區塊，避免發生結構定義不符錯誤。

如要[查詢 Hudi 資料](#query-biglake-external-table)，請按照下列步驟操作：

1. 根據 Hudi 資料[建立外部資料表](#create-hudi-external-tables)。
2. [將外部資料表升級為 BigLake](#upgrade-biglake-tables)。

### 建立 Hudi 外部資料表

使用 Hudi 和 BigQuery 的同步工具同步處理資料表時，請啟用 `use-bq-manifest-file` 旗標，改用資訊清單檔案方法。這個標記也會匯出 BigQuery 支援格式的資訊清單檔案，並使用該檔案建立外部資料表，名稱則為 `--table` 參數中指定的名稱。

如要建立 Hudi 外部資料表，請按照下列步驟操作：

1. 如要建立 Hudi 外部資料表，請[將工作提交](https://docs.cloud.google.com/dataproc/docs/guides/submit-job?hl=zh-tw)至現有的 Managed Service for Apache Spark 叢集。建構 Hudi-BigQuery 連接器時，請啟用 `use-bq-manifest-file` 旗標，改用資訊清單檔案方法。這個標記會匯出 BigQuery 支援格式的資訊清單檔案，並使用該檔案建立外部資料表，名稱則是在 `--table` 參數中指定。

   ```
   spark-submit \
      --master yarn \
      --packages com.google.cloud:google-cloud-bigquery:2.10.4 \
      --class org.apache.hudi.gcp.bigquery.BigQuerySyncTool  \
      JAR \
      --project-id PROJECT_ID \
      --dataset-name DATASET \
      --dataset-location LOCATION \
      --table TABLE \
      --source-uri URI  \
      --source-uri-prefix URI_PREFIX \
      --base-path BASE_PATH  \
      --partitioned-by PARTITION_BY \
      --use-bq-manifest-file
   ```

   更改下列內容：

   * `JAR`：如果您使用 Hudi-BigQuery 連接器，請指定 `hudi-gcp-bundle-0.14.0.jar`。如果您在 Managed Service for Apache Spark 2.1 中使用 Hudi 元件，請指定 `/usr/lib/hudi/tools/bq-sync-tool/hudi-gcp-bundle-0.12.3.1.jar`
   * `PROJECT_ID`：您要在當中建立 Hudi BigLake 資料表的專案 ID
   * `DATASET`：您要在其中建立 Hudi BigLake 資料集的資料集
   * `LOCATION`：要建立 Hudi BigLake 資料表的位置
   * `TABLE`：要建立的資料表名稱

     如果您要從舊版 Hudi-BigQuery 連接器 (0.13.0 以下版本) 遷移，該連接器會在資訊清單檔案上建立檢視區塊，請務必使用相同的資料表名稱，這樣才能保留現有的下游管道程式碼。
   * `URI`：您建立的 Cloud Storage URI，用於儲存 Hudi 資訊清單檔案

     這個 URI 會指向第一層分區，請務必加入分區索引鍵。例如 `gs://mybucket/hudi/mydataset/EventDate=*`。
   * `URI_PREFIX`：Cloud Storage URI 路徑的前置字元，通常是 Hudi 資料表的路徑
   * `BASE_PATH`：Hudi 表格的基礎路徑

     例如 `gs://mybucket/hudi/mydataset/`。
   * `PARTITION_BY`：分割區值

     例如 `EventDate`。

   如要進一步瞭解連接器的設定，請參閱「[Hudi-BigQuery 連接器](https://hudi.apache.org/docs/gcp_bigquery/)」。
2. 如要設定適當的精細控制項，或啟用中繼資料快取來提升效能，請參閱「[升級 BigLake 資料表](#upgrade-biglake-tables)」。

## 查詢 Delta 工作負載

現在[原生支援](https://docs.cloud.google.com/bigquery/docs/create-delta-lake-table?hl=zh-tw) Delta 資料表。建議您為 Delta 工作負載建立 Delta BigLake 資料表。Delta Lake BigLake 資料表支援更進階的 [Delta Lake 資料表](https://github.com/delta-io)，包括具有資料欄重新對應和刪除向量的資料表。此外，Delta BigLake 資料表會直接讀取最新快照，因此更新會立即生效。

如要[查詢 Delta 工作負載](#query-biglake-external-table)，請按照下列步驟操作：

1. [產生資訊清單檔案](#generate-manifest-file)。
2. [根據資訊清單檔案建立 BigLake 資料表](#create-delta-lake-biglake-tables)。
3. 設定適當的精細控制項，或啟用中繼資料快取功能，提升效能。如要執行這項操作，請參閱「[升級 BigLake 資料表](#upgrade-biglake-tables)」。

### 產生資訊清單檔案

BigQuery 支援 [`SymLinkTextInputFormat`](https://github.com/apache/hive/blob/master/ql/src/java/org/apache/hadoop/hive/ql/io/SymlinkTextInputFormat.java) 格式的資訊清單檔案，也就是以換行符號分隔的 URI 清單。如要進一步瞭解如何產生資訊清單檔案，請參閱「[設定 Presto 與 Delta Lake 的整合，並查詢 Delta 資料表](https://docs.delta.io/latest/presto-integration.html#set-up-the-presto-trino-or-athena-to-delta-lake-integration-and-query-delta-tables)」。

如要產生資訊清單檔案，請[將工作提交](https://docs.cloud.google.com/dataproc/docs/guides/submit-job?hl=zh-tw)至現有的 Managed Service for Apache Spark 叢集：

### SQL

使用 Spark 在位置 `path-to-delta-table` 的 Delta 資料表上執行下列指令：

```
GENERATE symlink_format_manifest FOR TABLE delta.`<path-to-delta-table>`
```

### Scala

使用 Spark 在位置 `path-to-delta-table` 的 Delta 資料表上執行下列指令：

```
val deltaTable = DeltaTable.forPath(<path-to-delta-table>)
deltaTable.generate("symlink_format_manifest")
```

### Java

使用 Spark 在位置 `path-to-delta-table` 的 Delta 資料表上執行下列指令：

```
DeltaTable deltaTable = DeltaTable.forPath(<path-to-delta-table>);
deltaTable.generate("symlink_format_manifest");
```

### Python

使用 Spark 在位置 `path-to-delta-table` 的 Delta 資料表上執行下列指令：

```
deltaTable = DeltaTable.forPath(<path-to-delta-table>)
deltaTable.generate("symlink_format_manifest")
```

### 建立 Delta BigLake 資料表

如要建立 Delta BigLake 資料表，請使用 [`CREATE EXTERNAL TABLE` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#create_external_table_statement)，並將 `file_set_spec_type` 欄位設為 `NEW_LINE_DELIMITED_MANIFEST`：

1. 前往「BigQuery」頁面

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中執行 `CREATE EXTERNAL TABLE` 陳述式：

   ```
   CREATE EXTERNAL TABLE PROJECT_ID.DATASET_NAME.TABLE_NAME
   WITH PARTITION COLUMNS(
   `PARTITION_COLUMN PARTITION_COLUMN_TYPE`,)
   WITH CONNECTION `PROJECT_IDREGION.CONNECTION_NAME`
   OPTIONS (
      format = "DATA_FORMAT",
      uris = ["URI"],
      file_set_spec_type = 'NEW_LINE_DELIMITED_MANIFEST',
      hive_partition_uri_prefix = "PATH_TO_DELTA_TABLE"
      max_staleness = STALENESS_INTERVAL,
      metadata_cache_mode = 'CACHE_MODE');
   ```

   更改下列內容：

   * `DATASET_NAME`：您建立的資料集名稱
   * `TABLE_NAME`：您要為這個資料表指定的名稱
   * `REGION`：連線所在位置 (例如 `us-east1`)
   * `CONNECTION_NAME`：您建立的連線名稱
   * `DATA_FORMAT`：任何支援的[格式](https://docs.cloud.google.com/bigquery/docs/biglake-intro?hl=zh-tw) (例如 `PARQUET`)
   * `URI`：資訊清單檔案的路徑 (例如 `gs://mybucket/path`)
   * `PATH_TO_DELTA_TABLE`：所有來源 URI 在分區索引鍵編碼開始前的通用前置字串
   * `STALENESS_INTERVAL`：指定對 BigLake 資料表執行的作業是否使用快取中繼資料，以及快取中繼資料必須有多新，作業才能使用。如要進一步瞭解中繼資料快取注意事項，請參閱「[中繼資料快取，提升效能](https://docs.cloud.google.com/bigquery/docs/omni-introduction?hl=zh-tw#metadata_caching_for_performance)」。

     如要停用中繼資料快取功能，請指定 0。這是目前的預設做法。

     如要啟用中繼資料快取功能，請指定介於 30 分鐘至 7 天之間的[間隔常值](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/lexical?hl=zh-tw#interval_literals)。舉例來說，如要指定 4 小時的過時間隔，請輸入 `INTERVAL 4 HOUR`。如果資料表在過去 4 小時內重新整理過，針對該資料表執行的作業就會使用快取中繼資料。如果快取中繼資料的舊於該時間，作業會改為從 Delta Lake 擷取中繼資料。
   * `CACHE_MODE`：指定中繼資料快取是否自動或手動重新整理。如要進一步瞭解中繼資料快取注意事項，請參閱「[中繼資料快取，提升效能](https://docs.cloud.google.com/bigquery/docs/omni-introduction?hl=zh-tw#metadata_caching_for_performance)」。

     設為 `AUTOMATIC`，中繼資料快取就會以系統定義的時間間隔 (通常介於 30 到 60 分鐘之間) 重新整理。

     如要依您決定的時間表重新整理中繼資料快取，請設為 `MANUAL`。在這種情況下，您可以呼叫 [`BQ.REFRESH_EXTERNAL_METADATA_CACHE` 系統程序](https://docs.cloud.google.com/bigquery/docs/reference/system-procedures?hl=zh-tw#bqrefresh_external_metadata_cache)來重新整理快取。

     如果 `STALENESS_INTERVAL` 設為大於 0 的值，您就必須設定 `CACHE_MODE`。

   範例：

   ```
   CREATE EXTERNAL TABLE mydataset.mytable
   WITH CONNECTION `us-east1.myconnection`
   OPTIONS (
       format="PARQUET",
       uris=["gs://mybucket/path/partitionpath=*"],
       file_set_spec_type = 'NEW_LINE_DELIMITED_MANIFEST'
       hive_partition_uri_prefix = "gs://mybucket/path/"
       max_staleness = INTERVAL 1 DAY,
       metadata_cache_mode = 'AUTOMATIC'
   );
   ```

## 升級 BigLake 資料表

您也可以運用[中繼資料快取](https://docs.cloud.google.com/bigquery/docs/biglake-intro?hl=zh-tw#metadata_caching_for_performance)和[具體化檢視表](https://docs.cloud.google.com/bigquery/docs/materialized-views-intro?hl=zh-tw#biglake)，[提升工作負載的效能](https://cloud.google.com/blog/products/data-analytics/deep-dive-on-how-biglake-accelerates-query-performance?hl=zh-tw)。如要使用中繼資料快取，可以同時指定相關設定。如要取得資料表詳細資料 (例如來源格式和來源 URI)，請參閱「[取得資料表資訊](https://docs.cloud.google.com/bigquery/docs/tables?hl=zh-tw#get_table_information)」。

如要將外部資料表更新為 BigLake 資料表，或更新現有的 BigLake，請選取下列其中一個選項：

### SQL

使用 [`CREATE OR REPLACE EXTERNAL TABLE` DDL 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#create_external_table_statement)更新資料表：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列陳述式：

   ```
   CREATE OR REPLACE EXTERNAL TABLE
     `PROJECT_ID.DATASET.EXTERNAL_TABLE_NAME`
     WITH CONNECTION {`REGION.CONNECTION_ID` | DEFAULT}
     OPTIONS(
       format ="TABLE_FORMAT",
       uris = ['BUCKET_PATH'],
       max_staleness = STALENESS_INTERVAL,
       metadata_cache_mode = 'CACHE_MODE'
       );
   ```

   請替換下列項目：

   * `PROJECT_ID`：包含資料表的專案名稱
   * `DATASET`：包含資料表的資料集名稱
   * `EXTERNAL_TABLE_NAME`：資料表名稱
   * `REGION`：包含連線的區域
   * `CONNECTION_ID`：要使用的連線名稱

     如要使用[預設連線](https://docs.cloud.google.com/bigquery/docs/default-connections?hl=zh-tw)，請指定 `DEFAULT`，而非包含 `REGION.CONNECTION_ID` 的連線字串。
   * `TABLE_FORMAT`：資料表使用的格式

     更新資料表時無法變更這項設定。
   * `BUCKET_PATH`：包含外部資料表資料的 Cloud Storage 值區路徑，格式為 `['gs://bucket_name/[folder_name/]file_name']`。

     如要在路徑中指定一個星號 (`*`) 萬用字元，即可從 bucket 選取多個檔案。例如，`['gs://mybucket/file_name*']`。詳情請參閱「[Cloud Storage URI 的萬用字元支援](https://docs.cloud.google.com/bigquery/docs/external-data-cloud-storage?hl=zh-tw#wildcard-support)」。

     如要為 `uris` 選項指定多個值區，請提供多個路徑。

     以下範例顯示有效的 `uris` 值：

     + `['gs://bucket/path1/myfile.csv']`
     + `['gs://bucket/path1/*.csv']`
     + `['gs://bucket/path1/*', 'gs://bucket/path2/file00*']`

     指定以多個檔案為目標的 `uris` 值時，所有這些檔案都必須共用相容的結構定義。

     如要進一步瞭解如何在 BigQuery 中使用 Cloud Storage URI，請參閱[Cloud Storage 資源路徑](https://docs.cloud.google.com/bigquery/docs/external-data-cloud-storage?hl=zh-tw#google-cloud-storage-uri)。
   * `STALENESS_INTERVAL`：指定對資料表執行的作業是否使用快取中繼資料，以及快取中繼資料必須有多新，作業才能使用

     如要進一步瞭解中繼資料快取注意事項，請參閱「[中繼資料快取，提升效能](https://docs.cloud.google.com/bigquery/docs/biglake-intro?hl=zh-tw#metadata_caching_for_performance)」。

     如要停用中繼資料快取功能，請指定 0。這是目前的預設做法。

     如要啟用中繼資料快取功能，請指定介於 30 分鐘至 7 天之間的[間隔常值](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/lexical?hl=zh-tw#interval_literals)。舉例來說，如要指定 4 小時的過時間隔，請輸入 `INTERVAL 4 HOUR`。如果資料表在過去 4 小時內重新整理過，針對該資料表執行的作業就會使用快取中繼資料。如果快取中繼資料的建立時間較早，作業就會改為從 Cloud Storage 擷取中繼資料。
   * `CACHE_MODE`：指定中繼資料快取是否自動或手動重新整理

     如要進一步瞭解中繼資料快取注意事項，請參閱「[中繼資料快取，提升效能](https://docs.cloud.google.com/bigquery/docs/biglake-intro?hl=zh-tw#metadata_caching_for_performance)」。

     設為 `AUTOMATIC`，中繼資料快取就會以系統定義的時間間隔 (通常為 30 到 60 分鐘) 重新整理。

     如要依您決定的時間表重新整理中繼資料快取，請設為 `MANUAL`。在這種情況下，您可以呼叫 [`BQ.REFRESH_EXTERNAL_METADATA_CACHE` 系統程序](https://docs.cloud.google.com/bigquery/docs/reference/system-procedures?hl=zh-tw#bqrefresh_external_metadata_cache)來重新整理快取。

     如果 `STALENESS_INTERVAL` 設為大於 0 的值，您就必須設定 `CACHE_MODE`。
3. 按一下「執行」play\_circle。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

### bq

使用 [`bq mkdef`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_mkdef) 和 [`bq update`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_update) 指令更新資料表：

1. 產生[外部資料表定義](https://docs.cloud.google.com/bigquery/external-table-definition?hl=zh-tw#table-definition)，說明要變更的資料表層面：

   ```
   bq mkdef --connection_id=PROJECT_ID.REGION.CONNECTION_ID \
   --source_format=TABLE_FORMAT \
   --metadata_cache_mode=CACHE_MODE \
   "BUCKET_PATH" > /tmp/DEFINITION_FILE
   ```

   更改下列內容：

   * `PROJECT_ID`：包含連線的專案名稱
   * `REGION`：包含連線的區域
   * `CONNECTION_ID`：要使用的連線名稱
   * `TABLE_FORMAT`：資料表使用的格式。更新資料表時無法變更這項設定。
   * `CACHE_MODE`：指定中繼資料快取是否自動或手動重新整理。如要進一步瞭解中繼資料快取考量事項，請參閱「[中繼資料快取提升效能](https://docs.cloud.google.com/bigquery/docs/biglake-intro?hl=zh-tw#metadata_caching_for_performance)」一文。

     設為 `AUTOMATIC`，中繼資料快取就會以系統定義的時間間隔重新整理，通常介於 30 到 60 分鐘之間。

     如要依您決定的時間表重新整理中繼資料快取，請設為 `MANUAL`。在這種情況下，您可以呼叫 [`BQ.REFRESH_EXTERNAL_METADATA_CACHE` 系統程序](https://docs.cloud.google.com/bigquery/docs/reference/system-procedures?hl=zh-tw#bqrefresh_external_metadata_cache)來重新整理快取。

     如果 `STALENESS_INTERVAL` 設為大於 0 的值，就必須設定 `CACHE_MODE`。
   * `BUCKET_PATH`：Cloud Storage bucket 的路徑，其中包含外部資料表的資料，格式為 `gs://bucket_name/[folder_name/]file_name`。

     如要在路徑中指定一個星號 (`*`) 萬用字元，可以限制從值區選取的檔案。例如，`gs://mybucket/file_name*`。詳情請參閱「[Cloud Storage URI 的萬用字元支援](https://docs.cloud.google.com/bigquery/docs/external-data-cloud-storage?hl=zh-tw#wildcard-support)」。

     如要為 `uris` 選項指定多個值區，請提供多個路徑。

     以下範例顯示有效的 `uris` 值：

     + `gs://bucket/path1/myfile.csv`
     + `gs://bucket/path1/*.csv`
     + `gs://bucket/path1/*,gs://bucket/path2/file00*`

     指定以多個檔案為目標的 `uris` 值時，所有檔案都必須共用相容的結構定義。

     如要進一步瞭解如何在 BigQuery 中使用 Cloud Storage URI，請參閱「[Cloud Storage 資源路徑](https://docs.cloud.google.com/bigquery/docs/external-data-cloud-storage?hl=zh-tw#google-cloud-storage-uri)」。
   * `DEFINITION_FILE`：您要建立的資料表定義檔名稱。
2. 使用新的外部資料表定義更新資料表：

   ```
   bq update --max_staleness=STALENESS_INTERVAL \
   --external_table_definition=/tmp/DEFINITION_FILE \
   PROJECT_ID:DATASET.EXTERNAL_TABLE_NAME
   ```

   更改下列內容：

   * `STALENESS_INTERVAL`：指定對資料表執行的作業是否使用快取中繼資料，以及作業必須使用多新的快取中繼資料。如要進一步瞭解中繼資料快取注意事項，請參閱「[中繼資料快取，提升效能](https://docs.cloud.google.com/bigquery/docs/biglake-intro?hl=zh-tw#metadata_caching_for_performance)」。

     如要停用中繼資料快取功能，請指定 0。這是目前的預設做法。

     如要啟用中繼資料快取，請使用[`INTERVAL` 資料類型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#interval_type)文件所述的 `Y-M D H:M:S` 格式，指定 30 分鐘到 7 天之間的間隔值。舉例來說，如要指定 4 小時的過時間隔，請輸入 `0-0 0 4:0:0`。如果資料表在過去 4 小時內重新整理過，針對該資料表執行的作業就會使用快取中繼資料。如果快取中繼資料較舊，作業會改為從 Cloud Storage 擷取中繼資料。
   * `DEFINITION_FILE`：您建立或更新的資料表定義檔案名稱。
   * `PROJECT_ID`：包含資料表的專案名稱
   * `DATASET`：含有資料表的資料集名稱
   * `EXTERNAL_TABLE_NAME`：資料表名稱。

## 查詢 BigLake 和外部資料表

建立 BigLake 資料表後，您就可以[使用 GoogleSQL 語法查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw)，就像查詢標準 BigQuery 資料表一樣。例如：`SELECT field1, field2 FROM mydataset.my_cloud_storage_table;`。

## 限制

* BigQuery 僅支援查詢 [Delta Lake 讀取器](https://github.com/delta-io/delta/blob/master/PROTOCOL.md#protocol-evolution)第 1 版資料表。
* Hudi 和 BigQuery 整合功能僅適用於 Hive 樣式的分區 `copy-on-write` 資料表。

## 後續步驟

* 瞭解如何[在 BigQuery 中使用 SQL](https://docs.cloud.google.com/bigquery/docs/introduction-sql?hl=zh-tw)。
* 瞭解 [BigLake 資料表](https://docs.cloud.google.com/bigquery/docs/biglake-intro?hl=zh-tw)。
* 瞭解 [BigQuery 配額](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-02 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-02 (世界標準時間)。"],[],[]]