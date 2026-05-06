Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [參考資料](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# TABLE\_OPTIONS 檢視畫面

`INFORMATION_SCHEMA.TABLE_OPTIONS` 檢視表會針對資料集中的每個資料表或檢視表，分別列出一個相對應的資料列。`TABLES` 和 `TABLE_OPTIONS` 檢視表也包含檢視表的相關高階資訊。如需詳細資訊，請查詢 [`INFORMATION_SCHEMA.VIEWS`](https://docs.cloud.google.com/bigquery/docs/information-schema-views?hl=zh-tw) 檢視畫面。

## 所需權限

如要查詢 `INFORMATION_SCHEMA.TABLE_OPTIONS` 檢視畫面，您必須具備下列 Identity and Access Management (IAM) 權限：

* `bigquery.tables.get`
* `bigquery.tables.list`
* `bigquery.routines.get`
* `bigquery.routines.list`

下列每個預先定義的 IAM 角色都包含上述權限：

* `roles/bigquery.admin`
* `roles/bigquery.dataViewer`
* `roles/bigquery.metadataViewer`

如要進一步瞭解 BigQuery 權限，請參閱「[使用 IAM 控管存取權](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)」。

## 結構定義

查詢 `INFORMATION_SCHEMA.TABLE_OPTIONS` 檢視表時，資料集中每個資料表或檢視表的每個選項在查詢結果都會有一個資料列。如要進一步瞭解檢視區塊，請改為查詢 [`INFORMATION_SCHEMA.VIEWS` 檢視區塊](https://docs.cloud.google.com/bigquery/docs/information-schema-views?hl=zh-tw)。

`INFORMATION_SCHEMA.TABLE_OPTIONS` 檢視表具有下列結構定義：

| 資料欄名稱 | 資料類型 | 值 |
| --- | --- | --- |
| `table_catalog` | `STRING` | 資料集所屬專案的專案 ID |
| `table_schema` | `STRING` | 資料表或檢視表所屬資料集的名稱 (又稱為 `datasetId`) |
| `table_name` | `STRING` | 資料表或檢視表的名稱 (又稱為 `tableId`) |
| `option_name` | `STRING` | [選項表格](#options_table)中的其中一個名稱值 |
| `option_type` | `STRING` | [選項表格](#options_table)中的其中一個資料類型值 |
| `option_value` | `STRING` | [選項表格](#options_table)中的其中一個值選項 |

##### 選項表格

| `OPTION_NAME` | `OPTION_TYPE` | `OPTION_VALUE` |
| --- | --- | --- |
| `description` | `STRING` | 資料表的說明 |
| `enable_refresh` | `BOOL` | 具體化檢視表是否啟用自動重新整理功能 |
| `expiration_timestamp` | `TIMESTAMP` | 這個資料表的到期時間 |
| `friendly_name` | `STRING` | 資料表的描述性名稱 |
| `kms_key_name` | `STRING` | 用來加密資料表的 Cloud KMS 金鑰名稱 |
| `labels` | `ARRAY<STRUCT<STRING, STRING>>` | 代表資料表標籤的 `STRUCT` 陣列 |
| `max_staleness` | `INTERVAL` | 設定資料表的最大延遲時間，適用於 [BigQuery 變更資料擷取 (CDC) upsert 作業](https://docs.cloud.google.com/bigquery/docs/change-data-capture?hl=zh-tw#manage_table_staleness) |
| `partition_expiration_days` | `FLOAT64` | 分區資料表中所有分區的預設生命週期 (以天為單位) |
| `refresh_interval_minutes` | `FLOAT64` | 具體化檢視表的重新整理頻率 |
| `require_partition_filter` | `BOOL` | 查詢資料表時是否需要分區篩選器 |
| `tags` | `ARRAY<STRUCT<STRING, STRING>>` | 以命名空間限定的 <鍵, 值> 語法附加至表格的標記。詳情請參閱「[標記和條件式存取](https://docs.cloud.google.com/iam/docs/tags-access-control?hl=zh-tw)」。 |

如果是外部資料表，則可選擇下列選項：

| 選項 | |
| --- | --- |
| `allow_jagged_rows` | `BOOL`  如果 `true`，允許缺少結尾自選欄的資料列。  適用於 CSV 資料。 |
| `allow_quoted_newlines` | `BOOL`  如果為 `true`，允許檔案中包含換行符號字元的引用資料區段。  適用於 CSV 資料。 |
| `bigtable_options` | `STRING`  建立 Bigtable 外部資料表時才需要。  以 JSON 格式指定 Bigtable 外部資料表的結構定義。  如需 Bigtable 資料表定義選項清單，請參閱 REST API 參考資料中的 `BigtableOptions`。 |
| `column_name_character_map` | `STRING`  定義支援的資料欄名稱字元範圍，以及如何處理不支援的字元。預設設定為 `STRICT`，表示 BigQuery 會針對不支援的字元擲回錯誤。`V1` 和 `V2` 會將任何不支援的字元替換為底線。  支援的值包括：   * `STRICT`。啟用[彈性資料欄名稱](https://docs.cloud.google.com/bigquery/docs/schemas?hl=zh-tw#flexible-column-names)。這是預設值。載入工作的資料欄名稱含有不支援的字元時就會失敗，並出現錯誤訊息。如要將不支援的字元替換為底線，讓載入工作順利完成，請指定 [`default_column_name_character_map`](https://docs.cloud.google.com/bigquery/docs/default-configuration?hl=zh-tw) 設定。 * `V1`。資料欄名稱只能包含[標準資料欄名稱字元](https://docs.cloud.google.com/bigquery/docs/schemas?hl=zh-tw#column_names)。不支援的字元 ([Parquet 檔案資料欄名稱中的句號除外](https://docs.cloud.google.com/bigquery/docs/loading-data-cloud-storage-parquet?hl=zh-tw#limitations_2)) 會替換為底線。這是 `column_name_character_map` 推出前建立的資料表預設行為。 * `V2`。除了[標準資料欄名稱字元](https://docs.cloud.google.com/bigquery/docs/schemas?hl=zh-tw#column_names)，也支援[彈性資料欄名稱](https://docs.cloud.google.com/bigquery/docs/schemas?hl=zh-tw#flexible-column-names)。不支援的字元 ([Parquet 檔案資料欄名稱中的句號除外](https://docs.cloud.google.com/bigquery/docs/loading-data-cloud-storage-parquet?hl=zh-tw#limitations_2)) 會替換為底線。  適用於 CSV 和 Parquet 資料。 |
| `compression` | `STRING`  資料來源的壓縮類型。支援的值包括： `GZIP`。如未指定，資料來源將不會經過壓縮。  適用於 CSV 和 JSON 資料。 |
| `decimal_target_types` | `ARRAY<STRING>`  決定如何轉換 `Decimal` 型別。等同於 [ExternalDataConfiguration.decimal\_target\_types](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables?hl=zh-tw#ExternalDataConfiguration.FIELDS.decimal_target_types)  範例：`["NUMERIC", "BIGNUMERIC"]`。 |
| `description` | `STRING`  這個表格的說明。 |
| `enable_list_inference` | `BOOL`  如果 `true`，請專門針對 Parquet LIST 邏輯型別使用結構定義推論。  適用於 Parquet 資料。 |
| `enable_logical_types` | `BOOL`  如果為 `true`，請將 Avro 邏輯類型轉換為對應的 SQL 類型。詳情請參閱[邏輯型別](https://docs.cloud.google.com/bigquery/docs/loading-data-cloud-storage-avro?hl=zh-tw#logical_types)。  適用於 Avro 資料。 |
| `encoding` | `STRING`  資料的字元編碼。支援的值包括： `UTF8` (或 `UTF-8`)、`ISO_8859_1` (或 `ISO-8859-1`)、`UTF-16BE`、 `UTF-16LE`、`UTF-32BE` 或 `UTF-32LE`。 預設值為 `UTF-8`。  適用於 CSV 資料。 |
| `enum_as_string` | `BOOL`  如果 `true`，則預設會將 Parquet ENUM 邏輯型別推斷為 STRING，而非 BYTES。  適用於 Parquet 資料。 |
| `expiration_timestamp` | `TIMESTAMP`  這個資料表的到期時間。如未指定，資料表就不會過期。  範例：`"2025-01-01 00:00:00 UTC"`。 |
| `field_delimiter` | `STRING`  CSV 檔案中的欄位分隔符。  適用於 CSV 資料。 |
| `format` | `STRING`  外部資料的格式。 [`CREATE EXTERNAL TABLE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#create_external_table_statement) 支援的值包括：`AVRO`、`CLOUD_BIGTABLE`、`CSV`、`DATASTORE_BACKUP`、`DELTA_LAKE` ([預覽版](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages))、`GOOGLE_SHEETS`、`NEWLINE_DELIMITED_JSON` (或 `JSON`)、`ORC`、`PARQUET`。  [支援的值包括：`AVRO`、`CSV`、`DELTA_LAKE` ([預覽版](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages))、`NEWLINE_DELIMITED_JSON` (或 `JSON`)、`ORC`、`PARQUET`。](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/load-statements?hl=zh-tw)`LOAD DATA`  值 `JSON` 相當於 `NEWLINE_DELIMITED_JSON`。 |
| `hive_partition_uri_prefix` | `STRING`  分區索引鍵編碼開始前，所有來源 URI 的通用前置字串。僅適用於 Hive 分區外部資料表。  適用於 Avro、CSV、JSON、Parquet 和 ORC 資料。  範例：`"gs://bucket/path"`。 |
| `file_set_spec_type` | `STRING`  指定如何解讀載入工作和外部資料表的來源 URI。  支援的值包括：   * `FILE_SYSTEM_MATCH`：列出物件儲存空間中的檔案，藉此擴充來源 URI。如果未設定 FileSetSpecType，系統會預設採用此行為。 * `NEW_LINE_DELIMITED_MANIFEST`：表示提供的 URI 是以換行符分隔的資訊清單檔案，每行一個 URI。資訊清單檔案不支援萬用字元 URI，且所有參照的資料檔案都必須與資訊清單檔案位於同一個 bucket。   舉例來說，如果來源 URI 為 `"gs://bucket/path/file"`，且 `file_set_spec_type` 為 `FILE_SYSTEM_MATCH`，則該檔案會直接做為資料檔案。如果 `file_set_spec_type` 為 `NEW_LINE_DELIMITED_MANIFEST`，系統會將檔案中的每一行解讀為指向資料檔案的 URI。 |
| `ignore_unknown_values` | `BOOL`  如果為 `true`，則忽略不在資料表結構定義中的其他值，不會傳回錯誤。  適用於 CSV 和 JSON 資料。 |
| `json_extension` | `STRING`  如果是 JSON 資料，則表示特定的 JSON 互換格式。如果未指定，BigQuery 會將資料讀取為一般 JSON 記錄。  支援的值包括：  `GEOJSON`。以換行符號分隔的 GeoJSON 資料。詳情請參閱「[從以換行符分隔的 GeoJSON 檔案建立外部資料表](https://docs.cloud.google.com/bigquery/docs/geospatial-data?hl=zh-tw#external-geojson)」。 |
| `max_bad_records` | `INT64`  讀取資料時可忽略的錯誤記錄數量上限。  適用於：CSV、JSON 和 Google 試算表資料。 |
| `max_staleness` | `INTERVAL`  適用於 [BigLake 資料表](https://docs.cloud.google.com/bigquery/docs/biglake-intro?hl=zh-tw#metadata_caching_for_performance)和[物件資料表](https://docs.cloud.google.com/bigquery/docs/object-table-introduction?hl=zh-tw#metadata_caching_for_performance)。  指定對資料表執行的作業是否使用快取中繼資料，以及作業必須使用多新的快取中繼資料。  如要停用中繼資料快取功能，請指定 0。這是目前的預設做法。  如要啟用中繼資料快取功能，請指定介於 30 分鐘至 7 天之間的[間隔常值](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/lexical?hl=zh-tw#interval_literals)。舉例來說，如要指定 4 小時的過時間隔，請輸入 `INTERVAL 4 HOUR`。如果資料表在過去 4 小時內重新整理過，針對該資料表執行的作業就會使用快取中繼資料。如果快取中繼資料較舊，作業會改為從 Cloud Storage 擷取中繼資料。 |
| `null_marker` | `STRING`  代表 CSV 檔案中 `NULL` 值的字串。  適用於 CSV 資料。 |
| `null_markers` | `ARRAY<STRING>`  代表 CSV 檔案中 `NULL` 值的字串清單。  這個選項無法與 `null_marker` 選項搭配使用。  適用於 CSV 資料。 |
| `object_metadata` | `STRING`  只有在建立[物件資料表](https://docs.cloud.google.com/bigquery/docs/object-table-introduction?hl=zh-tw)時才需要。  建立物件資料表時，請將這個選項的值設為 `SIMPLE`。 |
| `preserve_ascii_control_characters` | `BOOL`  如果是 `true`，則會保留內嵌的 ASCII 控制字元，也就是 ASCII 表格中的前 32 個字元，範圍從 '\x00' 到 '\x1F'。  適用於 CSV 資料。 |
| `projection_fields` | `STRING`  要載入的實體屬性清單。  適用於 Datastore 資料。 |
| `quote` | `STRING`  在 CSV 檔案中用來引用資料區段的字串。如果資料包含引用的換行符號字元，請將 `allow_quoted_newlines` 屬性設為 `true`。  適用於 CSV 資料。 |
| `reference_file_schema_uri` | `STRING`  使用者提供的參考檔案，內含資料表結構定義。  適用於 Parquet/ORC/AVRO 資料。  範例：`"gs://bucket/path/reference_schema_file.parquet"`。 |
| `require_hive_partition_filter` | `BOOL`  如果 `true`，查詢這個資料表時，都需要可刪除分區的分區篩選器，才能讀取資料。僅適用於 Hive 分區外部資料表。  適用於 Avro、CSV、JSON、Parquet 和 ORC 資料。 |
| `sheet_range` | `STRING`  要查詢的 Google 試算表範圍。  適用於 Google 試算表資料。  範例：`"sheet1!A1:B20"` |
| `skip_leading_rows` | `INT64`  讀取資料時要略過檔案開頭的列數。  適用於 CSV 和 Google 試算表資料。 |
| `source_column_match` | `STRING`  這項設定可控管策略，以便比對載入的資料欄與結構定義。  如未指定這個值，預設值會根據結構定義的提供方式而定。如果啟用自動偵測功能，系統預設會依名稱比對資料欄。否則，系統預設會依位置比對資料欄。這是為了確保行為回溯相容。  支援的值包括：   * `POSITION`：依位置比對。這個選項會假設資料欄的順序與結構定義相同。 * `NAME`：依名稱比對。這個選項會將標題列讀取為資料欄名稱，並重新排序資料欄，以符合結構定義中的欄位名稱。系統會根據 `skip_leading_rows` 屬性，從最後略過的資料列讀取資料欄名稱。 |
| `tags` | `<ARRAY<STRUCT<STRING, STRING>>>` 資料表的 IAM 標記陣列，以鍵/值組合表示。鍵應為[命名空間限定鍵名稱](https://docs.cloud.google.com/iam/docs/tags-access-control?hl=zh-tw#definitions)，值應為[簡稱](https://docs.cloud.google.com/iam/docs/tags-access-control?hl=zh-tw#definitions)。 |
| `time_zone` | `STRING`  如果剖析的時間戳記值未指定時區，就會採用這個預設時區。  請查看[有效的時區名稱](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#time_zone_name)。  如果沒有這個值，系統會使用預設時區 UTC 剖析未指定時區的時間戳記值。  適用於 CSV 和 JSON 資料。 |
| `date_format` | `STRING`  [格式元素](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/format-elements?hl=zh-tw#format_string_as_datetime)，可以定義輸入檔案中的 DATE 值格式 (例如 `MM/DD/YYYY`)。  如果存在這個值，則只有這個格式與 DATE 相容。[自動偵測結構定義](https://docs.cloud.google.com/bigquery/docs/schema-detect?hl=zh-tw#date_and_time_values)也會根據這個格式決定 DATE 資料欄類型，而非現有格式。  如果沒有這個值，系統會使用[預設格式](https://docs.cloud.google.com/bigquery/docs/loading-data-cloud-storage-csv?hl=zh-tw#data_types)剖析 DATE 欄位。  適用於 CSV 和 JSON 資料。 |
| `datetime_format` | `STRING`  [格式元素](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/format-elements?hl=zh-tw#format_string_as_datetime)，可以定義輸入檔案中的 DATETIME 值格式 (例如 `MM/DD/YYYY HH24:MI:SS.FF3`)。  如果存在這個值，則只有這個格式與 DATETIME 相容。[結構定義自動偵測](https://docs.cloud.google.com/bigquery/docs/schema-detect?hl=zh-tw#date_and_time_values)也會根據這個格式決定 DATETIME 資料欄類型，而非現有格式。  如果沒有這個值，系統會使用[預設格式](https://docs.cloud.google.com/bigquery/docs/loading-data-cloud-storage-csv?hl=zh-tw#data_types)剖析 DATETIME 欄位。  適用於 CSV 和 JSON 資料。 |
| `time_format` | `STRING`  [格式元素](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/format-elements?hl=zh-tw#format_string_as_datetime)，可以定義輸入檔案中的 TIME 值格式 (例如 `HH24:MI:SS.FF3`)。  如果存在這個值，這個格式就是唯一相容的 TIME 格式。[結構定義自動偵測](https://docs.cloud.google.com/bigquery/docs/schema-detect?hl=zh-tw#date_and_time_values)也會根據這個格式決定 TIME 資料欄類型，而非現有格式。  如果沒有這個值，系統會使用[預設格式](https://docs.cloud.google.com/bigquery/docs/loading-data-cloud-storage-csv?hl=zh-tw#data_types)剖析 TIME 欄位。  適用於 CSV 和 JSON 資料。 |
| `timestamp_format` | `STRING`  [格式元素](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/format-elements?hl=zh-tw#format_string_as_datetime)，可以定義輸入檔案中的 TIMESTAMP 值格式，例如 `MM/DD/YYYY HH24:MI:SS.FF3`。  如果存在這個值，這個格式就是唯一相容的 TIMESTAMP 格式。[自動偵測結構定義](https://docs.cloud.google.com/bigquery/docs/schema-detect?hl=zh-tw#date_and_time_values)也會根據這個格式 (而非現有格式) 決定 TIMESTAMP 欄類型。  如果沒有這個值，系統會使用[預設格式](https://docs.cloud.google.com/bigquery/docs/loading-data-cloud-storage-csv?hl=zh-tw#data_types)剖析 TIMESTAMP 欄位。  適用於 CSV 和 JSON 資料。 |
| `uris` | 如果是外部資料表 (包括物件資料表)，但不是 Bigtable 資料表：  `ARRAY<STRING>`  外部資料位置的完整 URI 陣列。 每個 URI 都可以包含一個星號 (`*`) [萬用字元](https://docs.cloud.google.com/bigquery/docs/loading-data-cloud-storage?hl=zh-tw#load-wildcards)，且必須出現在值區名稱之後。指定以多個檔案為目標的 `uris` 值時，所有這些檔案都必須共用相容的結構定義。  以下範例顯示有效的 `uris` 值：   * `['gs://bucket/path1/myfile.csv']` * `['gs://bucket/path1/*.csv']` * `['gs://bucket/path1/*', 'gs://bucket/path2/file00*']`    Bigtable 資料表：  `STRING`  URI，用於識別要當做資料來源的 Bigtable 資料表。您只能指定一個 Bigtable URI。  示例： `https://googleapis.com/bigtable/projects/project_id/instances/instance_id[/appProfiles/app_profile]/tables/table_name`  如要進一步瞭解如何建構 Bigtable URI，請參閱「[擷取 Bigtable URI](https://docs.cloud.google.com/bigquery/docs/create-bigtable-external-table?hl=zh-tw#bigtable-uri)」。 |

為確保穩定性，建議您在資訊結構定義查詢中明確列出資料欄，而非使用萬用字元 (`SELECT *`)。明確列出資料欄可避免基礎結構定義變更時，查詢中斷。

## 範圍和語法

對這個檢視表執行的查詢必須包含資料集或區域限定詞。如果是含有資料集限定符的查詢，您必須具備該資料集的權限。如要查詢含有區域限定符的資料，您必須具備專案權限。詳情請參閱「[語法](https://docs.cloud.google.com/bigquery/docs/information-schema-intro?hl=zh-tw#syntax)」。下表說明這個檢視畫面的區域和資源範圍：

| 檢視表名稱 | 資源範圍 | 區域範圍 |
| --- | --- | --- |
| `` [PROJECT_ID.]`region-REGION`.INFORMATION_SCHEMA.TABLE_OPTIONS `` | 專案層級 | `REGION` |
| `[PROJECT_ID.]DATASET_ID.INFORMATION_SCHEMA.TABLE_OPTIONS` | 資料集層級 | 資料集位置 |

取代下列項目：

* 選用：`PROJECT_ID`：您的 Google Cloud 專案 ID。如未指定，系統會使用預設專案。
* `REGION`：任何[資料集區域名稱](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)。
  例如：`` `region-us` ``。
* `DATASET_ID`：資料集 ID。詳情請參閱「[資料集限定符](https://docs.cloud.google.com/bigquery/docs/information-schema-intro?hl=zh-tw#dataset_qualifier)」。**注意：**您必須使用[區域限定詞](https://docs.cloud.google.com/bigquery/docs/information-schema-intro?hl=zh-tw#region_qualifier)查詢 `INFORMATION_SCHEMA` 檢視畫面。查詢執行位置必須與 `INFORMATION_SCHEMA` 檢視區塊的區域相符。

## 範例

##### 範例 1：

下列範例會透過查詢 `INFORMATION_SCHEMA.TABLE_OPTIONS` 檢視表，擷取預設專案 (`myproject`) 中 `mydataset` 內所有資料表的預設資料表到期時間。

如要對預設專案以外的專案執行查詢，請使用以下格式將專案 ID 新增至資料集：`` `project_id`.dataset.INFORMATION_SCHEMA.view ``；例如 `` `myproject`.mydataset.INFORMATION_SCHEMA.TABLE_OPTIONS ``。

**注意：** `INFORMATION_SCHEMA` 檢視表名稱會區分大小寫。

```
  SELECT
    *
  FROM
    mydataset.INFORMATION_SCHEMA.TABLE_OPTIONS
  WHERE
    option_name = 'expiration_timestamp';
```

結果大致如下：

```
  +----------------+---------------+------------+----------------------+-------------+--------------------------------------+
  | table_catalog  | table_schema  | table_name |     option_name      | option_type |             option_value             |
  +----------------+---------------+------------+----------------------+-------------+--------------------------------------+
  | myproject      | mydataset     | mytable1   | expiration_timestamp | TIMESTAMP   | TIMESTAMP "2020-01-16T21:12:28.000Z" |
  | myproject      | mydataset     | mytable2   | expiration_timestamp | TIMESTAMP   | TIMESTAMP "2021-01-01T21:12:28.000Z" |
  +----------------+---------------+------------+----------------------+-------------+--------------------------------------+
```

**注意：**系統會從查詢結果中排除沒有到期時間的資料表。

##### 範例 2：

以下範例會擷取 `mydataset` 中包含測試資料的所有資料表相關中繼資料。此查詢使用 `description` 選項中的值來尋找說明中的任意位置包含「test」的資料表。`mydataset` 在您的預設專案 (`myproject`) 中。

如要對預設專案以外的專案執行查詢，請使用以下格式將專案 ID 新增至資料集：`` `project_id`.dataset.INFORMATION_SCHEMA.view ``；例如 `` `myproject`.mydataset.INFORMATION_SCHEMA.TABLE_OPTIONS ``。

```
  SELECT
    *
  FROM
    mydataset.INFORMATION_SCHEMA.TABLE_OPTIONS
  WHERE
    option_name = 'description'
    AND option_value LIKE '%test%';
```

結果大致如下：

```
  +----------------+---------------+------------+-------------+-------------+--------------+
  | table_catalog  | table_schema  | table_name | option_name | option_type | option_value |
  +----------------+---------------+------------+-------------+-------------+--------------+
  | myproject      | mydataset     | mytable1   | description | STRING      | "test data"  |
  | myproject      | mydataset     | mytable2   | description | STRING      | "test data"  |
  +----------------+---------------+------------+-------------+-------------+--------------+
```




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-02 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-02 (世界標準時間)。"],[],[]]