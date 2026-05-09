Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 針對外部資料來源建立資料表定義檔

本頁面說明如何建立資料表定義檔。使用 bq 指令列工具建立[外部資料來源](https://docs.cloud.google.com/bigquery/docs/external-data-sources?hl=zh-tw)時，必須先建立這個檔案。如要建立外部資料來源，請執行 [`bg mk --table` 指令](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#mk-table) ，並使用 `--external_table_definition` 旗標指定資料表定義檔。

資料表定義檔內含外部資料表的結構定義和中繼資料，例如資料表的資料格式和相關屬性。您可以在資料表定義檔中設定與 REST API 中[`ExternalDataConfiguration` 資源](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables?hl=zh-tw#externaldataconfiguration)相同的屬性。

您可以建立資料表定義檔，說明下列外部資料來源的[永久或臨時外部資料表](https://docs.cloud.google.com/bigquery/docs/external-tables?hl=zh-tw#temporary_table_support)：

* Cloud Storage

  + 逗號分隔值 (CSV)
  + 換行符號分隔的 JSON
  + Avro 檔案
  + Datastore 匯出檔案
  + ORC 檔案
  + Parquet 檔案
  + Firestore 匯出檔案
* Google 雲端硬碟

  + 逗號分隔值 (CSV)
  + 換行符號分隔的 JSON
  + Avro 檔案
  + Google 試算表
* Bigtable

## 事前準備

如要建立資料表定義檔，您必須備妥資料來源的 URI：

* 如果資料來源是雲端硬碟，必須備妥 [雲端硬碟 URI](https://docs.cloud.google.com/bigquery/docs/external-data-drive?hl=zh-tw#drive-uri)
* 如果資訊來源是 Cloud Storage，必須備妥 [Cloud Storage URI](https://docs.cloud.google.com/bigquery/docs/external-data-cloud-storage?hl=zh-tw#google-cloud-storage-uri)
* 如果資料來源是 Bigtable，必須備妥 [Bigtable URI](https://docs.cloud.google.com/bigquery/docs/create-bigtable-external-table?hl=zh-tw#bigtable-uri)

## 為 CSV、JSON 或 Google 試算表檔案建立定義檔

在 Cloud Storage 或雲端硬碟中，為 CSV、JSON 或 Google 試算表檔案建立資料表定義檔時，可以透過下列方式指定資料表結構定義：

* [使用 `autodetect` 旗標](#use-auto-detect-flag)
* [使用內嵌結構定義](#use-inline-schema)
* [使用 JSON 結構定義檔](#use-json-schema)

### 使用 `autodetect` 旗標

如果您指定了 CSV、JSON 或 Google 試算表檔案，但未加入內嵌結構定義描述或結構定義檔，可以在資料表定義檔中使用 `--autodetect` 旗標將 `"autodetect"`選項設為 `true`。啟用自動偵測時，BigQuery 會儘可能嘗試自動推測結構定義。詳情請參閱[自動偵測外部資料來源的結構定義](https://docs.cloud.google.com/bigquery/docs/schema-detect?hl=zh-tw#schema_auto-detection_for_external_data_sources)。

#### 搭配 Cloud Storage 資料來源使用自動偵測功能

建立 Cloud Storage 資料來源的資料表定義檔：

1. 使用 [`bq mkdef` 指令](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_mkdef)與 `--autodetect` 旗標建立資料表定義檔。`mkdef` 指令會產生 JSON 格式的資料表定義檔。以下範例建立了資料表定義，並且將輸出內容寫入 `/tmp/file_name` 檔案。

   ```
   bq mkdef \
     --autodetect \
     --source_format=SOURCE_FORMAT \
     "URI" > /tmp/FILE_NAME
   ```

   更改下列內容：

   * `SOURCE_FORMAT`：檔案格式
   * `FILE_NAME`：資料表定義檔的名稱
   * `URI`：[Cloud Storage URI](https://docs.cloud.google.com/bigquery/docs/external-data-cloud-storage?hl=zh-tw#google-cloud-storage-uri)

     例如 `gs://mybucket/myfile`。
2. (選用) 在文字編輯器中開啟資料表定義檔。舉例來說，指令 `nano /tmp/file_name` 會在 nano 中開啟檔案。CSV 外部資料來源的檔案應會如下所示。請注意 `"autodetect"` 設為 `true`。

   ```
   {
   "autodetect": true,
   "csvOptions": {
     "allowJaggedRows": false,
     "allowQuotedNewlines": false,
     "encoding": "UTF-8",
     "fieldDelimiter": ",",
     "quote": "\"",
     "skipLeadingRows": 0
   },
   "sourceFormat": "CSV",
   "sourceUris": [
     "URI"
   ]
   }
   ```
3. (選用) 手動編輯資料表定義檔以修改、新增或刪除一般設定，如 `maxBadRecords` 和 `ignoreUnknownValues`。JSON 來源檔案沒有專屬的配置設定，但有設定會套用至 [CSV](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables?hl=zh-tw#CsvOptions) 和 [Google 試算表](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables?hl=zh-tw#GoogleSheetsOptions)檔案。詳情請參閱 API 參考資料中的 [`ExternalDataConfiguration`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables?hl=zh-tw#externaldataconfiguration)。

#### 搭配雲端硬碟資料來源使用自動偵測功能

為雲端硬碟資料來源建立資料表定義檔：

1. 使用 [`bq mkdef` 指令](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_mkdef)搭配 `--autodetect` 旗標建立資料表定義。`mkdef` 指令會產生 JSON 格式的資料表定義檔。以下範例建立了資料表定義，並且將輸出內容寫入 `/tmp/file_name` 檔案。

   ```
   bq mkdef \
      --autodetect \
      --source_format=SOURCE_FORMAT \
      "URI" > /tmp/FILE_NAME
   ```

   更改下列內容：

   * `SOURCE_FORMAT`：檔案格式
   * `FILE_NAME`：資料表定義檔的名稱
   * `URI`：[雲端硬碟 URI](https://docs.cloud.google.com/bigquery/docs/external-data-drive?hl=zh-tw#drive-uri)

     例如 `https://drive.google.com/open?id=123ABCD123AbcD123Abcd`。
2. 在文字編輯器中開啟資料表定義檔。舉例來說，指令 `nano /tmp/file_name` 會在 nano 中開啟檔案。Google 試算表外部資料來源的檔案應會如下所示。請注意 `"autodetect"` 設為 `true`。

   ```
   {
   "autodetect": true,
   "sourceFormat": "GOOGLE_SHEETS",
   "sourceUris": [
     "URI"
   ]
   }
   ```
3. (選用) 手動編輯資料表定義檔以修改、新增或刪除一般設定，如 `maxBadRecords` 和 `ignoreUnknownValues`。JSON 來源檔案沒有專屬的配置設定，但有設定會套用至 [CSV](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables?hl=zh-tw#CsvOptions) 和 [Google 試算表](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables?hl=zh-tw#GoogleSheetsOptions)檔案。詳情請參閱 API 參考資料中的 [`ExternalDataConfiguration`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables?hl=zh-tw#externaldataconfiguration)。
4. 如要在 Google 試算表檔案中指定特定的工作表或儲存格範圍，請將 `range` 屬性新增至資料表定義檔中的 [`GoogleSheetsOptions` 物件](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables?hl=zh-tw#googlesheetsoptions)。如要查詢特定工作表，請指定工作表名稱。如要查詢儲存格範圍，請使用 `sheet_name!top_left_cell_id:bottom_right_cell_id` 格式指定範圍，例如 `"Sheet1!A1:B20"`。如果未指定 `range` 參數，則會使用檔案中的第一個工作表。

### 使用內嵌結構定義

如果不想使用結構定義自動偵測，則可透過提供內嵌結構定義的方式建立資料表定義檔。如要提供內嵌結構定義，請在指令列中列出欄位和資料類型，格式如下：`FIELD:DATA_TYPE,FIELD:DATA_TYPE`。

#### 搭配 Cloud Storage 或 Google 雲端硬碟資料來源使用內嵌結構定義

使用內嵌結構定義，為 Cloud Storage 或雲端硬碟資料來源建立資料表定義：

1. 使用 [`bq mkdef` 指令](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_mkdef)搭配 `--noautodetect` 旗標建立資料表定義。`mkdef` 指令會產生 JSON 格式的資料表定義檔。以下範例建立了資料表定義，並且將輸出內容寫入 `/tmp/file_name` 檔案。

   ```
   bq mkdef \
     --noautodetect \
     --source_format=SOURCE_FORMAT \
     "URI" \
     FIELD:DATA_TYPE,FIELD:DATA_TYPE > /tmp/FILE_NAME
   ```

   請替換下列項目：

   * `SOURCE_FORMAT`：來源檔案格式
   * `URI`：[Cloud Storage URI](https://docs.cloud.google.com/bigquery/docs/external-data-cloud-storage?hl=zh-tw#google-cloud-storage-uri) 或 [Google 雲端硬碟 URI](https://docs.cloud.google.com/bigquery/docs/external-data-drive?hl=zh-tw#drive-uri)

     例如，Cloud Storage 的範圍為 `gs://mybucket/myfile`，Google 雲端硬碟的範圍為 `https://drive.google.com/open?id=123ABCD123AbcD123Abcd`。
   * `FIELD:DATA_TYPE,FIELD:DATA_TYPE`：結構定義

     例如 `Name:STRING,Address:STRING, ...`。
   * `FILE_NAME`：資料表定義檔的名稱
2. (選用) 在文字編輯器中開啟資料表定義檔。舉例來說，指令 `nano /tmp/file_name` 會在 nano 中開啟檔案。檔案內容大致如下。請注意，`"autodetect"` 未啟用，且結構定義資訊寫入了資料表定義檔。

   ```
   {
   "schema": {
     "fields": [
       {
         "name": "FIELD",
         "type": "DATA_TYPE"
       },
       {
         "name": "FIELD",
         "type": "DATA_TYPE"
       }
       ...
     ]
   },
   "sourceFormat": "NEWLINE_DELIMITED_JSON",
   "sourceUris": [
     "URI"
   ]
   }
   ```
3. (選用) 手動編輯資料表定義檔以修改、新增或刪除一般設定，如 `maxBadRecords` 和 `ignoreUnknownValues`。JSON 來源檔案沒有專屬的配置設定，但有設定會套用至 [CSV](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables?hl=zh-tw#CsvOptions) 和 [Google 試算表](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables?hl=zh-tw#GoogleSheetsOptions)檔案。詳情請參閱 API 參考資料中的 [`ExternalDataConfiguration`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables?hl=zh-tw#externaldataconfiguration)。

### 使用 JSON 結構定義檔

如果您不要使用自動偵測或提供內嵌結構定義，則可建立 JSON 結構定義檔，並於建立資料表定義檔時參照 JSON 結構定義檔。在本機上，手動建立 JSON 結構定義檔。
如果 JSON 結構定義檔儲存在 Cloud Storage 或雲端硬碟中，則無法參照。

#### 搭配 Cloud Storage 資料來源使用結構定義檔案

使用 JSON 結構定義檔建立 Cloud Storage 資料來源的資料表定義：

1. 使用 [`bq mkdef` 指令](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_mkdef)搭配 `--noautodetect` 旗標建立資料表定義。`mkdef` 指令會產生 JSON 格式的資料表定義檔。以下範例建立了資料表定義，並且將輸出內容寫入 `/tmp/file_name` 檔案。

   ```
   bq mkdef \
      --noautodetect \
      --source_format=SOURCE_FORMAT \
      "URI" \
     PATH_TO_SCHEMA_FILE > /tmp/FILE_NAME
   ```

   更改下列內容：

   * `SOURCE_FORMAT`：檔案格式
   * `FILE_NAME`：資料表定義檔的名稱
   * `URI`：[Cloud Storage URI](https://docs.cloud.google.com/bigquery/docs/external-data-cloud-storage?hl=zh-tw#google-cloud-storage-uri)

     例如 `gs://mybucket/myfile`。
   * `PATH_TO_SCHEMA_FILE`：本機上 JSON 結構定義檔案的位置
2. (選用) 在文字編輯器中開啟資料表定義檔。舉例來說，指令 `nano /tmp/file_name` 會在  
   nano 中開啟檔案。檔案內容大致如下。請注意，`"autodetect"` 未啟用，且結構定義資訊寫入了資料表定義檔。

   ```
   {
   "schema": {
     "fields": [
       {
         "name": "FIELD",
         "type": "DATA_TYPE"
       },
       {
         "name": "FIELD",
         "type": "DATA_TYPE"
       }
       ...
     ]
   },
   "sourceFormat": "NEWLINE_DELIMITED_JSON",
   "sourceUris": [
     "URI"
   ]
   }
   ```
3. (選用) 手動編輯資料表定義檔以修改、新增或刪除一般設定，如 `maxBadRecords` 和 `ignoreUnknownValues`。JSON 來源檔案沒有專屬的配置設定，但有設定會套用至 [CSV](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables?hl=zh-tw#CsvOptions) 和 [Google 試算表](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables?hl=zh-tw#GoogleSheetsOptions)檔案。詳情請參閱 API 參考資料中的 [`ExternalDataConfiguration`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables?hl=zh-tw#externaldataconfiguration)。

#### 搭配雲端硬碟資料來源使用結構定義檔案

使用 JSON 結構定義檔建立雲端硬碟資料來源的資料表定義：

1. 使用 [`bq mkdef` 指令](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_mkdef)搭配 `--noautodetect` 旗標建立資料表定義。`mkdef` 指令會產生 JSON 格式的資料表定義檔。以下範例建立了資料表定義，並且將輸出內容寫入 `/tmp/file_name` 檔案。

   ```
   bq mkdef \
      --noautodetect \
      --source_format=source_format \
      "URI" \
      PATH_TO_SCHEMA_FILE > /tmp/FILE_NAME
   ```

   更改下列內容：

   * `SOURCE_FORMAT`：來源檔案格式
   * `URI`：[雲端硬碟 URI](https://docs.cloud.google.com/bigquery/docs/external-data-drive?hl=zh-tw#drive-uri)

     例如 `https://drive.google.com/open?id=123ABCD123AbcD123Abcd`。
   * `PATH_TO_SCHEMA_FILE`：本機上 JSON 結構定義檔案的位置
   * `FILE_NAME`：資料表定義檔的名稱
2. 在文字編輯器中開啟資料表定義檔。舉例來說，指令 `nano /tmp/file_name` 會在 nano 中開啟檔案。檔案內容大致如下。請注意，`"autodetect"` 未啟用，且結構定義資訊寫入了資料表定義檔。

   ```
   {
   "schema": {
     "fields": [
       {
         "name": "FIELD",
         "type": "DATA_TYPE"
       },
       {
         "name": "FIELD",
         "type": "DATA_TYPE"
       }
       ...
     ]
   },
   "sourceFormat": "GOOGLE_SHEETS",
   "sourceUris": [
     "URI"
   ]
   }
   ```
3. (選用) 手動編輯資料表定義檔以修改、新增或刪除一般設定，如 `maxBadRecords` 和 `ignoreUnknownValues`。JSON 來源檔案沒有專屬的配置設定，但有設定會套用至 [CSV](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables?hl=zh-tw#CsvOptions) 和 [Google 試算表](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables?hl=zh-tw#GoogleSheetsOptions)檔案。詳情請參閱 API 參考資料中的 [`ExternalDataConfiguration`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables?hl=zh-tw#externaldataconfiguration)。
4. 如要在 Google 試算表檔案中指定特定的工作表或儲存格範圍，請將 `range` 屬性新增至資料表定義檔中的 [`GoogleSheetsOptions` 物件](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables?hl=zh-tw#googlesheetsoptions)。如要查詢特定工作表，請指定工作表名稱。如要查詢儲存格範圍，請使用 `sheet_name!top_left_cell_id:bottom_right_cell_id` 格式指定範圍，例如 `"Sheet1!A1:B20"`。如果未指定 `range` 參數，則會使用檔案中的第一個工作表。

## 為自述式格式建立定義檔

Avro、Parquet 和 ORC 都是*自述式*格式。這些格式的資料檔案包含自己的結構定義資訊。如果您使用這些格式做為外部資料來源，BigQuery 會自動使用來源資料擷取結構定義。建立資料表定義時，不必使用結構定義自動偵測，也不須提供內嵌結構定義或結構定義檔。

對於儲存在 Cloud Storage 或雲端硬碟的 Avro、Parquet 或 ORC 資料，您可以建立資料表定義檔：

1. 使用 [`bq mkdef` 指令](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_mkdef)建立資料表定義。

   ```
   bq mkdef \
       --source_format=FORMAT \
       "URI" > FILE_NAME
   ```

   更改下列內容：

   * `FORMAT`：來源格式
   * `URI`：[Cloud Storage URI](https://docs.cloud.google.com/bigquery/docs/external-data-cloud-storage?hl=zh-tw#google-cloud-storage-uri) 或 [Google 雲端硬碟 URI](https://docs.cloud.google.com/bigquery/docs/external-data-drive?hl=zh-tw#drive-uri)

     例如 Cloud Storage 的 `gs://mybucket/myfile` 或 Google 雲端硬碟的 `https://drive.google.com/open?id=123ABCD123AbcD123Abcd`。
   * `FILE_NAME`：資料表定義檔的名稱
2. 選用：在文字編輯器中開啟資料表定義檔。檔案內容大致如下：

   ```
   {
      "sourceFormat": "AVRO",
      "sourceUris": [
      "URI"
       ]
   }
   ```
3. 選用：手動編輯資料表定義檔，修改、新增或刪除一般設定，如 `maxBadRecords` 和 `ignoreUnknownValues`。
   詳情請參閱 API 參考資料中的 [`ExternalDataConfiguration`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables?hl=zh-tw#externaldataconfiguration)。

## 為 Hive 分區資料建立定義檔

使用 [`bq mkdef` 指令](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_mkdef)搭配 `hive_partitioning_mode` 和 `hive_partitioning_source_uri_prefix` 旗標，[為儲存在 Cloud Storage、Amazon Simple Storage Service (Amazon S3) 或 Azure Blob 儲存空間的 Hive 分割資料建立定義檔](https://docs.cloud.google.com/bigquery/docs/hive-partitioned-queries?hl=zh-tw)。

## 為 Datastore 和 Firestore 建立定義檔

如果您使用 Datastore 或 Firestore 匯出做為外部資料來源，BigQuery 會自動使用該自述式來源資料擷取結構定義。建立資料表定義時，不必提供內嵌結構定義或結構定義檔。

對於儲存在 Cloud Storage 的 Datastore 和 Firestore 匯出資料，您可以建立資料表定義檔：

1. 使用 [`bq mkdef` 指令](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_mkdef)建立資料表定義。您不必針對 Datastore 或 Firestore 備份檔案使用 `--noautodetect` 旗標，對於這些檔案類型，系統不會啟用結構定義自動偵測。`mkdef` 指令會產生 JSON 格式的資料表定義檔。以下範例建立了資料表定義，並且將輸出內容寫入 `/tmp/file_name` 檔案。

   ```
   bq mkdef \
   --source_format=DATASTORE_BACKUP \
   "URI" > /tmp/FILE_NAME
   ```

   更改下列內容：

   * `URI`：[Cloud Storage URI](https://docs.cloud.google.com/bigquery/docs/external-data-cloud-storage?hl=zh-tw#google-cloud-storage-uri)
   * `FILE_NAME`：資料表定義檔的名稱

   Datastore 和 Firestore 皆使用 `DATASTORE_BACKUP` 來源格式。
2. (選用) 在文字編輯器中開啟資料表定義檔。舉例來說，指令 `nano /tmp/file_name` 會在 nano 中開啟檔案。檔案內容大致如下。請注意，這裡不必使用 `"autodetect"` 設定。

   ```
   {
   "sourceFormat": "DATASTORE_BACKUP",
   "sourceUris": [
     "gs://URI"
   ]
   }
   ```
3. (選用) 手動編輯資料表定義檔以修改、新增或刪除設定，如 `maxBadRecords` 和 `ignoreUnknownValues`。Datastore 和 Firestore 匯出檔案沒有專屬的配置設定。詳情請參閱 API 參考資料中的 [`ExternalDataConfiguration`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables?hl=zh-tw#externaldataconfiguration)。

## 建立 Bigtable 的定義檔

針對 Bigtable 建立資料表定義檔時，請手動產生 JSON 格式的檔案。目前無法針對 Bigtable 資料來源使用 `mkdef` 指令建立資料表定義。結構定義自動偵測也不適用於 Bigtable。如需 Bigtable 資料表定義選項清單，請參閱 REST API 參考資料中的 [`BigtableOptions`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables?hl=zh-tw#bigtableoptions) 說明。

Bigtable 的 JSON 資料表定義檔內容大致如下。
使用此資料表定義檔時，BigQuery 會從單一資料欄系列讀取資料，將值解讀為二進位編碼整數。

```
{
    "sourceFormat": "BIGTABLE",
    "sourceUris": [
        "https://googleapis.com/bigtable/projects/PROJECT_ID/instances/INSTANCE_ID[/appProfiles/APP_PROFILE_ID]/tables/TABLE_NAME"
    ],
    "bigtableOptions": {
        "columnFamilies" : [
            {
                "familyId": "FAMILY_ID",
                "type": "INTEGER",
                "encoding": "BINARY"
            }
        ]
    }
}
```

更改下列內容：

* `PROJECT_ID`：包含 Bigtable 叢集的專案
* `INSTANCE_ID`：Bigtable 執行個體 ID
* `APP_PROFILE_ID` (選用)：您要用來讀取 Bigtable 資料的應用程式設定檔 ID。[應用程式設定檔設定](https://docs.cloud.google.com/bigtable/docs/app-profiles?hl=zh-tw)會指出外部資料表是否使用 Data Boost 或佈建節點進行運算。
* `TABLE_NAME`：要查詢的資料表名稱
* `FAMILY_ID`：資料欄系列 ID

詳情請參閱「[擷取 Bigtable URI](https://docs.cloud.google.com/bigquery/docs/create-bigtable-external-table?hl=zh-tw#bigtable-uri)」。

## 資料表定義檔的萬用字元支援

如果資料分成多個檔案，可以使用星號 (\*) 萬用字元選取多個檔案。使用星號萬用字元時，必須遵守下列規則：

* 星號可以出現在物件名稱內或物件名稱的末端。
* 系統不支援使用多個星號。舉例來說，路徑 `gs://mybucket/fed-*/temp/*.csv` 無效。
* 系統不支援在 bucket 名稱中使用星號。

範例：

* 以下範例說明如何選取所有資料夾中以 `gs://mybucket/fed-samples/fed-sample` 前置字元開頭的所有檔案：

  ```
  gs://mybucket/fed-samples/fed-sample*
  ```
* 以下範例說明如何只選取名為 `fed-samples` 的資料夾和 `fed-samples` 的任何子資料夾中，副檔名為 `.csv` 的檔案：

  ```
  gs://mybucket/fed-samples/*.csv
  ```
* 以下範例說明如何在名為 `fed-samples` 的資料夾中，選取命名模式為 `fed-sample*.csv` 的檔案。這個範例不會選取 `fed-samples` 子資料夾中的檔案。

  ```
  gs://mybucket/fed-samples/fed-sample*.csv
  ```

使用 bq 指令列工具時，您可能需要在某些平台上逸出星號。

如果使用星號萬用字元，請以引號括住值區和檔案名稱。舉例來說，如果您有兩個名為 `fed-sample000001.csv` 和 `fed-sample000002.csv` 的檔案，並想使用星號選取這兩個檔案，則值區 URI 會是 `"gs://mybucket/fed-sample*"`。

針對下列資料來源建立資料表定義檔時，無法使用 `*` 萬用字元：

* **Bigtable**。對於 Bigtable 資料，您只能指定一個資料來源。URI 值必須是 Bigtable 資料表的有效 HTTPS 網址。
* **Datastore** 或 **Firestore**。儲存在 Cloud Storage 中的 Datastore 或 Firestore 匯出資料。對於 Datastore 備份，您只能指定一個資料來源。URI 值必須以 `.backup_info` 或 `.export_metadata` 結尾。
* **雲端硬碟**。儲存在雲端硬碟中的資料。

## 後續步驟

* 瞭解如何查詢 [Cloud Storage 資料](https://docs.cloud.google.com/bigquery/docs/query-cloud-storage-using-biglake?hl=zh-tw)。
* 瞭解如何查詢 [Google 雲端硬碟資料](https://docs.cloud.google.com/bigquery/docs/external-data-drive?hl=zh-tw)。
* 瞭解如何查詢 [Bigtable 資料](https://docs.cloud.google.com/bigquery/docs/external-data-bigtable?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-08 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-08 (世界標準時間)。"],[],[]]