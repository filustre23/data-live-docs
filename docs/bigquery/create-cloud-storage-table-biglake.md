Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# Cloud Storage 的外部資料表

本文說明如何建立 Cloud Storage BigLake 資料表。[BigLake 資料表](https://docs.cloud.google.com/bigquery/docs/biglake-intro?hl=zh-tw)可讓您使用存取權委派功能，查詢 Cloud Storage 中的結構化資料。存取權委派功能可將 BigLake 資料表的存取權，與基礎資料儲存空間的存取權分開。

## 事前準備

1. 在 Google Cloud 控制台的專案選擇器頁面中，選取或建立 Google Cloud 專案。

   **選取或建立專案所需的角色**

   * **選取專案**：選取專案時，不需要具備特定 IAM 角色，只要您已獲授角色，即可選取任何專案。
   * **建立專案**：如要建立專案，您需要具備專案建立者角色 (`roles/resourcemanager.projectCreator`)，其中包含 `resourcemanager.projects.create` 權限。[瞭解如何授予角色](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)。
   **注意**：如果您不打算保留在這項程序中建立的資源，請建立新專案，而不要選取現有專案。完成這些步驟後，您就可以刪除專案，並移除與該專案相關聯的所有資源。

   [前往專案選取器](https://console.cloud.google.com/projectselector2/home/dashboard?hl=zh-tw)
2. [確認專案已啟用計費功能 Google Cloud](https://docs.cloud.google.com/billing/docs/how-to/verify-billing-enabled?hl=zh-tw#confirm_billing_is_enabled_on_a_project) 。
3. 啟用 BigQuery Connection API。

   **啟用 API 時所需的角色**

   如要啟用 API，您需要服務使用情形管理員 IAM 角色 (`roles/serviceusage.serviceUsageAdmin`)，其中包含 `serviceusage.services.enable` 權限。[瞭解如何授予角色](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)。

   [啟用 API](https://console.cloud.google.com/flows/enableapi?apiid=bigqueryconnection.googleapis.com&hl=zh-tw)

   如要從 Apache Spark 等開放原始碼引擎讀取 BigLake 資料表，請啟用 [BigQuery Storage Read API](https://console.cloud.google.com/apis/library/bigquerystorage.googleapis.com?hl=zh-tw)。
4. 在 Google Cloud 控制台中啟用 Cloud Shell。

   [啟用 Cloud Shell](https://console.cloud.google.com/?cloudshell=true&hl=zh-tw)
5. 確認您有 BigQuery [資料集](https://docs.cloud.google.com/bigquery/docs/datasets?hl=zh-tw)。
6. 確認 Google Cloud SDK 版本為 366.0.0 以上：

   ```
   gcloud version
   ```

   視需要[更新 Google Cloud SDK](https://docs.cloud.google.com/sdk/docs/quickstart?hl=zh-tw)。

   1. 選用：如果是 Terraform，則必須使用 `terraform-provider-google` 4.25.0 以上版本。`terraform-provider-google` 版本列於 [GitHub](https://github.com/hashicorp/terraform-provider-google/releases)。您可以從 [HashiCorp Terraform 下載頁面](https://www.terraform.io/downloads)下載最新版本。
7. 建立 Cloud 資源連結，或設定與外部資料來源的預設連線。連線需要額外的角色和權限。詳情請參閱「[建立 Cloud 資源連線](https://docs.cloud.google.com/bigquery/docs/create-cloud-resource-connection?hl=zh-tw)」和「[預設連線總覽](https://docs.cloud.google.com/bigquery/docs/default-connections?hl=zh-tw)」。

### 必要的角色

如要建立 BigLake 資料表，您需要下列 BigQuery Identity and Access Management (IAM) 權限：

* `bigquery.tables.create`
* `bigquery.connections.delegate`

BigQuery 管理員 (`roles/bigquery.admin`) 預先定義的身分與存取權管理角色包含這些權限。

如果您不是這個角色的主體，請要求管理員授予存取權，或為您建立 BigLake 資料表。

如要進一步瞭解 BigQuery 中的 Identity and Access Management 角色和權限，請參閱「[預先定義的角色和權限](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)」。

### 位置注意事項

使用 Cloud Storage 儲存資料檔案時，建議使用 Cloud Storage [單一區域](https://docs.cloud.google.com/storage/docs/locations?hl=zh-tw#available-locations)或[雙區域](https://docs.cloud.google.com/storage/docs/locations?hl=zh-tw#location-dr) bucket，而非多區域 bucket，以提升效能。

## 在未分區資料上建立外部資料表

如果您知道如何在 BigQuery 建立資料表，建立外部資料表的程序也大同小異。資料表可使用外部資料表支援的任何檔案格式。詳情請參閱「[限制](https://docs.cloud.google.com/bigquery/docs/biglake-intro?hl=zh-tw#limitations)」一文。

建立 BigLake 資料表前，您需要[資料集](https://docs.cloud.google.com/bigquery/docs/datasets?hl=zh-tw)和[可[存取 Cloud Storage](https://docs.cloud.google.com/bigquery/docs/create-cloud-resource-connection?hl=zh-tw#access-storage) 的 Cloud 資源連線](https://docs.cloud.google.com/bigquery/docs/create-cloud-resource-connection?hl=zh-tw#create-cloud-resource-connection)。

如要建立 BigLake 資料表，請選取下列任一選項：

### 控制台

1. 前往「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。

   如果沒有看到左側窗格，請按一下 last\_page「Expand left pane」(展開左側窗格)，開啟窗格。
3. 在「Explorer」窗格中展開專案，按一下「Datasets」(資料集)，然後選取資料集。
4. 展開「動作」more\_vert選項，然後按一下「建立資料表」。
5. 在「來源」部分，指定下列詳細資料：

   1. 在「Create table from」(使用下列資料建立資料表) 區段，選取「Google Cloud Storage」
   2. 在「Select file from GCS bucket or use a URI pattern」(從 GCS bucket 選取檔案或使用 URI 模式) 中，瀏覽並選取要使用的 bucket 和檔案，或輸入 `gs://bucket_name/[folder_name/]file_name` 格式的路徑。

      您無法在 Google Cloud 控制台中指定多個 URI，但可以指定一個星號 (`*`) 萬用字元，選取多個檔案。例如：`gs://mybucket/file_name*`。詳情請參閱「[Cloud Storage URI 的萬用字元支援](https://docs.cloud.google.com/bigquery/docs/external-data-cloud-storage?hl=zh-tw#wildcard-support)」。

      Cloud Storage 值區的位置必須與要建立的資料表所在的資料集位置相同。
   3. 在「File format」(檔案格式) 部分，選取與檔案相符的格式。
6. 在「目的地」部分，指定下列詳細資料：

   1. 在「Project」(專案) 部分，選擇要在其中建立資料表的專案。
   2. 在「Dataset」(資料集) 部分，選擇要建立資料表的資料集。
   3. 在「Table」(資料表) 中，輸入要建立的資料表名稱。
   4. 在「Table type」(資料表類型) 中，選取「External table」(外部資料表)。
   5. 選取「使用 Cloud 資源連結建立 BigLake 資料表」。
   6. 在「Connection ID」(連線 ID) 部分，選取您先前建立的連線。
7. 在「Schema」(結構定義) 區段中，您可以啟用[結構定義自動偵測](https://docs.cloud.google.com/bigquery/docs/schema-detect?hl=zh-tw)功能，也可以手動指定結構定義 (如有來源檔案)。如果沒有來源檔案，就必須手動指定結構定義。

   * 如要啟用結構定義自動偵測功能，請選取「自動偵測」選項。
   * 如要手動指定結構定義，請取消勾選「自動偵測」選項。啟用「以文字形式編輯」，然後以 [JSON 陣列](https://docs.cloud.google.com/bigquery/docs/schemas?hl=zh-tw#specifying_a_json_schema_file)的形式輸入資料表結構定義。
8. 如要忽略含有與結構定義不符之額外資料欄值的資料列，請展開「進階選項」部分，然後選取「不明的值」。
9. 點選「建立資料表」。

建立永久資料表後，您就可以把這個資料表當做原生 BigQuery 資料表一樣執行查詢。查詢完成後，可以[匯出結果](https://docs.cloud.google.com/bigquery/docs/writing-results?hl=zh-tw)為 CSV 或 JSON 檔案、將結果儲存為資料表，或將結果儲存至 Google 試算表。

### SQL

使用 [`CREATE EXTERNAL TABLE` DDL 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#create_external_table_statement)。您可以明確指定結構定義，也可以使用[結構定義自動偵測](https://docs.cloud.google.com/bigquery/docs/schema-detect?hl=zh-tw)功能，從外部資料推斷結構定義。

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列陳述式：

   ```
   CREATE EXTERNAL TABLE `PROJECT_ID.DATASET.EXTERNAL_TABLE_NAME`
     WITH CONNECTION {`PROJECT_ID.REGION.CONNECTION_ID` | DEFAULT}
     OPTIONS (
       format ="TABLE_FORMAT",
       uris = ['BUCKET_PATH'[,...]],
       max_staleness = STALENESS_INTERVAL,
       metadata_cache_mode = 'CACHE_MODE'
       );
   ```

   請替換下列項目：

   * `PROJECT_ID`：要在其中建立資料表的專案名稱，例如 `myproject`
   * `DATASET`：您要在其中建立資料表的 BigQuery 資料集名稱，例如 `mydataset`
   * `EXTERNAL_TABLE_NAME`：要建立的資料表名稱，例如 `mytable`
   * `REGION`：包含連線的區域，例如 `us`
   * `CONNECTION_ID`：連線 ID，例如 `myconnection`

     在 Google Cloud 控制台中[查看連線詳細資料](https://docs.cloud.google.com/bigquery/docs/working-with-connections?hl=zh-tw#view-connections)時，連線 ID 是「連線 ID」中顯示的完整連線 ID 最後一部分的值，例如 `projects/myproject/locations/connection_location/connections/myconnection`。

     如要使用[預設連線](https://docs.cloud.google.com/bigquery/docs/default-connections?hl=zh-tw)，請指定 `DEFAULT`，而不是包含 PROJECT\_ID.REGION.CONNECTION\_ID 的連線字串。
   * `TABLE_FORMAT`：要建立的資料表格式，例如 `PARQUET`

     如要進一步瞭解支援的格式，請參閱「[限制](https://docs.cloud.google.com/bigquery/docs/biglake-intro?hl=zh-tw#limitations)」一節。
   * `BUCKET_PATH`：包含外部資料表資料的 Cloud Storage 值區路徑，格式為 `['gs://bucket_name/[folder_name/]file_name']`。

     如要在路徑中指定一個星號 (`*`) 萬用字元，即可從 bucket 選取多個檔案。例如，`['gs://mybucket/file_name*']`。詳情請參閱「[Cloud Storage URI 的萬用字元支援](https://docs.cloud.google.com/bigquery/docs/external-data-cloud-storage?hl=zh-tw#wildcard-support)」。

     如要為 `uris` 選項指定多個值區，請提供多個路徑。

     以下範例顯示有效的 `uris` 值：

     + `['gs://bucket/path1/myfile.csv']`
     + `['gs://bucket/path1/*.csv']`
     + `['gs://bucket/path1/*', 'gs://bucket/path2/file00*']`

     指定以多個檔案為目標的 `uris` 值時，所有這些檔案都必須共用相容的結構定義。

     如要進一步瞭解如何在 BigQuery 中使用 Cloud Storage URI，請參閱[Cloud Storage 資源路徑](https://docs.cloud.google.com/bigquery/docs/external-data-cloud-storage?hl=zh-tw#google-cloud-storage-uri)。
   * `STALENESS_INTERVAL`：指定對 BigLake 資料表執行的作業是否使用快取中繼資料，以及作業必須使用多新的快取中繼資料。如要進一步瞭解中繼資料快取注意事項，請參閱「[中繼資料快取，提升效能](https://docs.cloud.google.com/bigquery/docs/biglake-intro?hl=zh-tw#metadata_caching_for_performance)」。

     如要停用中繼資料快取功能，請指定 0。這是目前的預設做法。

     如要啟用中繼資料快取功能，請指定介於 30 分鐘至 7 天之間的[間隔常值](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/lexical?hl=zh-tw#interval_literals)。舉例來說，如要指定 4 小時的過時間隔，請輸入 `INTERVAL 4 HOUR`。如果資料表在過去 4 小時內重新整理過，針對該資料表執行的作業就會使用快取中繼資料。如果快取中繼資料的建立時間較早，作業就會改為從 Cloud Storage 擷取中繼資料。
   * `CACHE_MODE`：指定中繼資料快取是否自動或手動重新整理。如要進一步瞭解中繼資料快取注意事項，請參閱「[中繼資料快取，提升效能](https://docs.cloud.google.com/bigquery/docs/biglake-intro?hl=zh-tw#metadata_caching_for_performance)」。

     設為 `AUTOMATIC`，中繼資料快取就會以系統定義的時間間隔 (通常介於 30 到 60 分鐘之間) 重新整理。

     如要依您決定的時間表重新整理中繼資料快取，請設為 `MANUAL`。在這種情況下，您可以呼叫 [`BQ.REFRESH_EXTERNAL_METADATA_CACHE` 系統程序](https://docs.cloud.google.com/bigquery/docs/reference/system-procedures?hl=zh-tw#bqrefresh_external_metadata_cache)來重新整理快取。

     如果 `STALENESS_INTERVAL` 設為大於 0 的值，您就必須設定 `CACHE_MODE`。
3. 按一下「執行」play\_circle。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

### bq

**選項 1：資料表定義檔**

使用 [`bq mkdef` 指令](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_mkdef)建立資料表定義檔，然後將路徑傳遞至 [`bq mk` 指令](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_mk)，如下所示：

```
bq mkdef \
    --connection_id=CONNECTION_ID \
    --source_format=SOURCE_FORMAT \
  BUCKET_PATH > DEFINITION_FILE

bq mk --table \
    --external_table_definition=DEFINITION_FILE \
    --max_staleness=STALENESS_INTERVAL \
    PROJECT_ID:DATASET.EXTERNAL_TABLE_NAME \
    SCHEMA
```

更改下列內容：

* `CONNECTION_ID`：連線 ID，例如 `myconnection`

  在 Google Cloud 控制台中[查看連線詳細資料](https://docs.cloud.google.com/bigquery/docs/working-with-connections?hl=zh-tw#view-connections)時，連線 ID 是「連線 ID」中顯示的完整連線 ID 最後一個區段的值，例如 `projects/myproject/locations/connection_location/connections/myconnection`。

  如要使用[預設連線](https://docs.cloud.google.com/bigquery/docs/default-connections?hl=zh-tw)，請指定 `DEFAULT`，而非包含 PROJECT\_ID.REGION.CONNECTION\_ID 的連線字串。
* `SOURCE_FORMAT`：外部資料來源的格式。
  例如：`PARQUET`。
* `BUCKET_PATH`：包含資料表的資料的 Cloud Storage bucket 路徑，格式為 `gs://bucket_name/[folder_name/]file_pattern`。

  如要在 `file_pattern` 中選取 bucket 中的多個檔案，請在 `file_pattern` 中指定一個星號 (`*`) 萬用字元。例如：`gs://mybucket/file00*.parquet`。詳情請參閱「[Cloud Storage URI 的萬用字元支援](https://docs.cloud.google.com/bigquery/docs/external-data-cloud-storage?hl=zh-tw#wildcard-support)」。

  如要為 `uris` 選項指定多個值區，請提供多個路徑。

  以下範例顯示有效的 `uris` 值：

  + `gs://bucket/path1/myfile.csv`
  + `gs://bucket/path1/*.parquet`
  + `gs://bucket/path1/file1*`、`gs://bucket1/path1/*`

  指定以多個檔案為目標的 `uris` 值時，所有檔案都必須共用相容的結構定義。

  如要進一步瞭解如何在 BigQuery 中使用 Cloud Storage URI，請參閱「[Cloud Storage 資源路徑](https://docs.cloud.google.com/bigquery/docs/external-data-cloud-storage?hl=zh-tw#google-cloud-storage-uri)」。
* `DEFINITION_FILE`：本機上[資料表定義檔](https://docs.cloud.google.com/bigquery/docs/external-table-definition?hl=zh-tw)的路徑。
* `STALENESS_INTERVAL`：指定對 BigLake 資料表執行的作業是否使用快取中繼資料，以及快取中繼資料必須有多新，作業才能使用。如要進一步瞭解中繼資料快取注意事項，請參閱「[中繼資料快取，提升效能](https://docs.cloud.google.com/bigquery/docs/biglake-intro?hl=zh-tw#metadata_caching_for_performance)」。

  如要停用中繼資料快取功能，請指定 0。這是目前的預設做法。

  如要啟用中繼資料快取，請使用[`INTERVAL` 資料類型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#interval_type)文件所述的 `Y-M D H:M:S` 格式，指定 30 分鐘到 7 天之間的間隔值。舉例來說，如要指定 4 小時的過時間隔，請輸入 `0-0 0 4:0:0`。如果資料表在過去 4 小時內重新整理過，針對該資料表執行的作業就會使用快取中繼資料。如果快取中繼資料較舊，作業會改為從 Cloud Storage 擷取中繼資料。
* `DATASET`：您要在其中建立資料表的 BigQuery 資料集名稱，例如 `mydataset`
* `EXTERNAL_TABLE_NAME`：要建立的資料表名稱，例如 `mytable`
* `SCHEMA`：BigLake 資料表的結構定義

範例：

```
bq mkdef
    --connection_id=myconnection
    --metadata_cache_mode=CACHE_MODE
    --source_format=CSV 'gs://mybucket/*.csv' > mytable_def

bq mk
    --table
    --external_table_definition=mytable_def='gs://mybucket/*.csv'
    --max_staleness=0-0 0 4:0:0
    myproject:mydataset.mybiglaketable
    Region:STRING,Quarter:STRING,Total_sales:INTEGER
```

如要使用結構定義自動偵測功能，請在 `mkdef` 指令中設定 `--autodetect=true` 標記，並省略結構定義：

```
bq mkdef \
    --connection_id=myconnection \
    --metadata_cache_mode=CACHE_MODE \
    --source_format=CSV --autodetect=true \
    gs://mybucket/*.csv > mytable_def

bq mk \
    --table \
    --external_table_definition=mytable_def=gs://mybucket/*.csv \
    --max_staleness=0-0 0 4:0:0 \
    myproject:mydataset.myexternaltable
```

**選項 2：內嵌表格定義**

您可以直接將資料表定義傳遞至 [`bq mk` 指令](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_mk)，不必建立資料表定義檔。使用 `@connection` 裝飾器，在 [`--external_table_definition`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#external_table_definition_flag) 旗標結尾指定要使用的連線。

```
bq mk --table \
  --external_table_definition=@SOURCE_FORMAT=BUCKET_PATH@projects/PROJECT_ID/locations/REGION/connections/CONNECTION_ID \
  DATASET_NAME.TABLE_NAME \
  SCHEMA
```

更改下列內容：

* `SOURCE_FORMAT`：外部資料來源的格式

  例如 `CSV`。
* `BUCKET_PATH`：包含資料表的資料的 Cloud Storage bucket 路徑，格式為 `gs://bucket_name/[folder_name/]file_pattern`。

  如要在 `file_pattern` 中選取 bucket 中的多個檔案，請在 `file_pattern` 中指定一個星號 (`*`) 萬用字元。例如：`gs://mybucket/file00*.parquet`。詳情請參閱「[Cloud Storage URI 的萬用字元支援](https://docs.cloud.google.com/bigquery/docs/external-data-cloud-storage?hl=zh-tw#wildcard-support)」。

  如要為 `uris` 選項指定多個值區，請提供多個路徑。

  以下範例顯示有效的 `uris` 值：

  + `gs://bucket/path1/myfile.csv`
  + `gs://bucket/path1/*.parquet`
  + `gs://bucket/path1/file1*`、`gs://bucket1/path1/*`

  指定以多個檔案為目標的 `uris` 值時，所有檔案都必須共用相容的結構定義。

  如要進一步瞭解如何在 BigQuery 中使用 Cloud Storage URI，請參閱「[Cloud Storage 資源路徑](https://docs.cloud.google.com/bigquery/docs/external-data-cloud-storage?hl=zh-tw#google-cloud-storage-uri)」。
* `PROJECT_ID`：要在其中建立資料表的專案名稱，例如 `myproject`
* `REGION`：包含連線的區域，`us`
* `CONNECTION_ID`：連線 ID，例如 `myconnection`

  在 Google Cloud 控制台中[查看連線詳細資料](https://docs.cloud.google.com/bigquery/docs/working-with-connections?hl=zh-tw#view-connections)時，連線 ID 是「連線 ID」中顯示的完整連線 ID 最後一個區段的值，例如 `projects/myproject/locations/connection_location/connections/myconnection`。

  如要使用[預設連線](https://docs.cloud.google.com/bigquery/docs/default-connections?hl=zh-tw)，請指定 `DEFAULT`，而非包含 PROJECT\_ID.REGION.CONNECTION\_ID 的連線字串。
* `DATASET_NAME`：要在其中建立 BigLake 資料集的資料集名稱
* `TABLE_NAME`：BigLake 資料表名稱
* `SCHEMA`：BigLake 資料表的結構定義

範例：

```
bq mk --table \
    --external_table_definition=@CSV=gs://mybucket/*.parquet@projects/myproject/locations/us/connections/myconnection \
    --max_staleness=0-0 0 4:0:0 \
    myproject:mydataset.myexternaltable \
    Region:STRING,Quarter:STRING,Total_sales:INTEGER
```

### API

呼叫 [`tables.insert` 方法](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables/insert?hl=zh-tw) API 方法，並在您傳入的 [`Table` 資源](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables?hl=zh-tw#Table)中建立 [`ExternalDataConfiguration`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables?hl=zh-tw#externaldataconfiguration)。

指定 `schema` 屬性，或將 `autodetect` 屬性設為 `true`，為支援的資料來源啟用結構定義自動偵測功能。

指定 `connectionId` 屬性，找出要用於連線至 Cloud Storage 的連線。

### Terraform

這個範例會根據未經分割的資料建立 BigLake 資料表。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
# This creates a bucket in the US region named "my-bucket" with a pseudorandom suffix.
resource "random_id" "default" {
  byte_length = 8
}
resource "google_storage_bucket" "default" {
  name                        = "my-bucket-${random_id.default.hex}"
  location                    = "US"
  force_destroy               = true
  uniform_bucket_level_access = true
}

# This queries the provider for project information.
data "google_project" "project" {}

# This creates a connection in the US region named "my-connection".
# This connection is used to access the bucket.
resource "google_bigquery_connection" "default" {
  connection_id = "my-connection"
  location      = "US"
  cloud_resource {}
}

# This grants the previous connection IAM role access to the bucket.
resource "google_project_iam_member" "default" {
  role    = "roles/storage.objectViewer"
  project = data.google_project.project.id
  member  = "serviceAccount:${google_bigquery_connection.default.cloud_resource[0].service_account_id}"
}

# This makes the script wait for seven minutes before proceeding.
# This lets IAM permissions propagate.
resource "time_sleep" "default" {
  create_duration = "7m"

  depends_on = [google_project_iam_member.default]
}

# This defines a Google BigQuery dataset with
# default expiration times for partitions and tables, a
# description, a location, and a maximum time travel.
resource "google_bigquery_dataset" "default" {
  dataset_id                      = "my_dataset"
  default_partition_expiration_ms = 2592000000  # 30 days
  default_table_expiration_ms     = 31536000000 # 365 days
  description                     = "My dataset description"
  location                        = "US"
  max_time_travel_hours           = 96 # 4 days

  # This defines a map of labels for the bucket resource,
  # including the labels "billing_group" and "pii".
  labels = {
    billing_group = "accounting",
    pii           = "sensitive"
  }
}


# This creates a BigQuery Table with automatic metadata caching.
resource "google_bigquery_table" "default" {
  dataset_id = google_bigquery_dataset.default.dataset_id
  table_id   = "my_table"
  schema = jsonencode([
    { "name" : "country", "type" : "STRING" },
    { "name" : "product", "type" : "STRING" },
    { "name" : "price", "type" : "INT64" }
  ])
  external_data_configuration {
    # This defines an external data configuration for the BigQuery table
    # that reads Parquet data from the publish directory of the default
    # Google Cloud Storage bucket.
    autodetect    = false
    source_format = "PARQUET"
    connection_id = google_bigquery_connection.default.name
    source_uris   = ["gs://${google_storage_bucket.default.name}/data/*"]
    # This enables automatic metadata refresh.
    metadata_cache_mode = "AUTOMATIC"
  }

  # This sets the maximum staleness of the metadata cache to 10 hours.
  max_staleness = "0-0 0 10:0:0"

  depends_on = [time_sleep.default]
}
```

如要在 Google Cloud 專案中套用 Terraform 設定，請完成下列各節的步驟。

## 準備 Cloud Shell

1. 啟動 [Cloud Shell](https://shell.cloud.google.com/?hl=zh-tw)。
2. 設定要套用 Terraform 設定的預設 Google Cloud 專案。

   每項專案只需要執行一次這個指令，且可以在任何目錄中執行。

   ```
   export GOOGLE_CLOUD_PROJECT=PROJECT_ID
   ```

   如果您在 Terraform 設定檔中設定明確值，環境變數就會遭到覆寫。

## 準備目錄

每個 Terraform 設定檔都必須有自己的目錄 (也稱為*根模組*)。

1. 在 [Cloud Shell](https://shell.cloud.google.com/?hl=zh-tw) 中建立目錄，並在該目錄中建立新檔案。檔案名稱的副檔名必須是 `.tf`，例如 `main.tf`。在本教學課程中，這個檔案稱為 `main.tf`。

   ```
   mkdir DIRECTORY && cd DIRECTORY && touch main.tf
   ```
2. 如果您正在學習教學課程，可以複製每個章節或步驟中的程式碼範例。

   將程式碼範例複製到新建立的 `main.tf`。

   視需要從 GitHub 複製程式碼。如果 Terraform 代码片段是端對端解決方案的一部分，建議您使用這個方法。
3. 查看並修改範例參數，套用至您的環境。
4. 儲存變更。
5. 初始化 Terraform。每個目錄只需執行一次這項操作。

   ```
   terraform init
   ```

   如要使用最新版 Google 供應商，請加入 `-upgrade` 選項：

   ```
   terraform init -upgrade
   ```

## 套用變更

1. 檢查設定，確認 Terraform 即將建立或更新的資源符合您的預期：

   ```
   terraform plan
   ```

   視需要修正設定。
2. 執行下列指令，並在提示中輸入 `yes`，套用 Terraform 設定：

   ```
   terraform apply
   ```

   等待 Terraform 顯示「Apply complete!」訊息。
3. [開啟 Google Cloud 專案](https://console.cloud.google.com/?hl=zh-tw)即可查看結果。在 Google Cloud 控制台中，前往 UI 中的資源，確認 Terraform 已建立或更新這些資源。

**注意：**Terraform 範例通常會假設 Google Cloud 專案已啟用必要的 API。

BigLake 支援自動偵測結構定義。不過，如果您未提供結構定義，且上個步驟中未將存取權授予服務帳戶，當您嘗試自動偵測結構定義時，這些步驟會失敗，並顯示存取遭拒的訊息。

## 在 Apache Hive 分區資料上建立 BigLake 資料表

您可以在 Cloud Storage 中，為 Hive 分區資料建立 BigLake 資料表。建立外部分區資料表後，您就無法變更分區鍵。如要變更分割區鍵，您必須重新建立資料表。

如要根據 Cloud Storage 中的 Hive 分區資料建立 BigLake 資料表，請選取下列任一選項：

### 控制台

1. 前往「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。

   如果沒有看到左側窗格，請按一下 last\_page「Expand left pane」(展開左側窗格)，開啟窗格。
3. 在「Explorer」窗格中展開專案，按一下「Datasets」(資料集)，然後按一下資料集。
4. 按一下 [Create table] (建立資料表)。「建立資料表」窗格隨即開啟。
5. 在「來源」部分，指定下列詳細資料：

   1. 在「Create table from」(使用下列資料建立資料表) 部分，選取「Google Cloud Storage」。
   2. 使用[萬用字元](https://docs.cloud.google.com/bigquery/docs/batch-loading-data?hl=zh-tw#load-wildcards)提供資料夾路徑。例如：`my_bucket/my_files*`。資料夾的位置必須與要建立、附加或覆寫的資料表所在的資料集位置相同。
   3. 從「檔案格式」清單中選取檔案類型。
   4. 選取「來源資料分割」核取方塊，然後指定下列詳細資料：

      1. 在「選取來源 URI 前置字串」中，輸入 URI 前置字串。例如：`gs://my_bucket/my_files`。
      2. 選用：如要對這個資料表的所有查詢強制使用分區篩選器，請選取「需要分區篩選器」核取方塊。
         使用分區篩選器可以降低成本並提升效能。詳情請參閱[在查詢中對分區鍵套用述詞篩選器](https://docs.cloud.google.com/bigquery/docs/hive-partitioned-queries-gcs?hl=zh-tw#requiring_predicate_filters_on_partition_keys_in_queries)。
      3. 在「分割區推論模式」部分，選取下列其中一個選項：

         * **自動推論類型**：將分區結構定義偵測模式設為 `AUTO`。
         * **將所有資料欄視為字串**：將分區結構定義偵測模式設為 `STRINGS`。
         * **提供自己的結構定義**：將分區結構定義偵測模式設為 `CUSTOM`，然後手動輸入分區鍵的結構定義資訊。詳情請參閱「[提供自訂分區索引鍵結構定義](https://docs.cloud.google.com/bigquery/docs/hive-partitioned-loads-gcs?hl=zh-tw#custom_partition_key_schema)」。
6. 在「目的地」部分，指定下列詳細資料：

   1. 在「Project」(專案) 部分，選取要建立資料表的專案。
   2. 在「Dataset」(資料集) 部分，選取要建立資料表的資料集。
   3. 在「Table」(資料表) 中，輸入要建立的資料表名稱。
   4. 在「Table type」(資料表類型) 中，選取「External table」(外部資料表)。
   5. 選取「使用 Cloud 資源連線建立 BigLake 資料表」核取方塊。
   6. 在「連線 ID」部分，選取您先前建立的連線。
7. 在「Schema」(結構定義) 區段中，選取「Auto detect」(自動偵測) 選項，啟用[結構定義自動偵測](https://docs.cloud.google.com/bigquery/docs/schema-detect?hl=zh-tw)功能。
8. 如要忽略含有與結構定義不符之額外資料欄值的資料列，請展開「進階選項」部分，然後選取「不明的值」。
9. 點選「建立資料表」。

### SQL

使用 [`CREATE EXTERNAL TABLE` DDL 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#create_external_table_statement)：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列陳述式：

   ```
   CREATE EXTERNAL TABLE `PROJECT_ID.DATASET.EXTERNAL_TABLE_NAME`
   WITH PARTITION COLUMNS
   (
     PARTITION_COLUMN PARTITION_COLUMN_TYPE,
   )
   WITH CONNECTION {`PROJECT_ID.REGION.CONNECTION_ID` | DEFAULT}
   OPTIONS (
     hive_partition_uri_prefix = "HIVE_PARTITION_URI_PREFIX",
     uris=['FILE_PATH'],
     max_staleness = STALENESS_INTERVAL,
     metadata_cache_mode = 'CACHE_MODE',
     format ="TABLE_FORMAT"
   );
   ```

   請替換下列項目：

   * `PROJECT_ID`：要在其中建立資料表的專案名稱，例如 `myproject`
   * `DATASET`：您要在其中建立資料表的 BigQuery 資料集名稱，例如 `mydataset`
   * `EXTERNAL_TABLE_NAME`：要建立的資料表名稱，例如 `mytable`
   * `PARTITION_COLUMN`：分區資料欄的名稱
   * `PARTITION_COLUMN_TYPE`：分區資料欄的類型
   * `REGION`：包含連線的區域，例如 `us`
   * `CONNECTION_ID`：連線 ID，例如 `myconnection`

     在 Google Cloud 控制台中[查看連線詳細資料](https://docs.cloud.google.com/bigquery/docs/working-with-connections?hl=zh-tw#view-connections)時，連線 ID 是「連線 ID」中顯示的完整連線 ID 最後一個部分的值，例如 `projects/myproject/locations/connection_location/connections/myconnection`。

     如要使用[預設連線](https://docs.cloud.google.com/bigquery/docs/default-connections?hl=zh-tw)，請指定 `DEFAULT`，而不是包含 PROJECT\_ID.REGION.CONNECTION\_ID 的連線字串。
   * `HIVE_PARTITION_URI_PREFIX`：Hive 分割 URI 前置字串，例如 `gs://mybucket/`
   * `FILE_PATH`：要建立的外部資料表資料來源路徑，例如 `gs://mybucket/*.parquet`
   * `STALENESS_INTERVAL`：指定對 BigLake 資料表執行的作業是否使用快取中繼資料，以及作業必須使用多新的快取中繼資料。如要進一步瞭解中繼資料快取注意事項，請參閱「[中繼資料快取，提升效能](https://docs.cloud.google.com/bigquery/docs/biglake-intro?hl=zh-tw#metadata_caching_for_performance)」。

     如要停用中繼資料快取功能，請指定 0。這是目前的預設做法。

     如要啟用中繼資料快取功能，請指定介於 30 分鐘至 7 天之間的[間隔常值](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/lexical?hl=zh-tw#interval_literals)。舉例來說，如要指定 4 小時的過時間隔，請輸入 `INTERVAL 4 HOUR`。如果資料表在過去 4 小時內重新整理過，針對該資料表執行的作業就會使用快取中繼資料。如果快取中繼資料的建立時間較早，作業就會改為從 Cloud Storage 擷取中繼資料。
   * `CACHE_MODE`：指定中繼資料快取是否自動或手動重新整理。如要進一步瞭解中繼資料快取注意事項，請參閱「[中繼資料快取，提升效能](https://docs.cloud.google.com/bigquery/docs/biglake-intro?hl=zh-tw#metadata_caching_for_performance)」。

     設為 `AUTOMATIC`，中繼資料快取就會以系統定義的時間間隔 (通常介於 30 到 60 分鐘之間) 重新整理。

     如要依您決定的時間表重新整理中繼資料快取，請設為 `MANUAL`。在這種情況下，您可以呼叫 [`BQ.REFRESH_EXTERNAL_METADATA_CACHE` 系統程序](https://docs.cloud.google.com/bigquery/docs/reference/system-procedures?hl=zh-tw#bqrefresh_external_metadata_cache)來重新整理快取。

     如果 `STALENESS_INTERVAL` 設為大於 0 的值，您就必須設定 `CACHE_MODE`。
   * `TABLE_FORMAT`：要建立的資料表格式，例如 `PARQUET`
3. 按一下「執行」play\_circle。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

**範例**

下列範例會根據分區資料建立 BigLake 資料表，其中：

* 系統會自動偵測結構定義。
* 資料表的中繼資料快取過時間隔為 1 天。
* 中繼資料快取會自動重新整理。

```
CREATE EXTERNAL TABLE `my_dataset.my_table`
WITH PARTITION COLUMNS
(
  sku STRING,
)
WITH CONNECTION `us.my-connection`
OPTIONS(
  hive_partition_uri_prefix = "gs://mybucket/products",
  uris = ['gs://mybucket/products/*'],
  max_staleness = INTERVAL 1 DAY,
  metadata_cache_mode = 'AUTOMATIC'
);
```

下列範例會根據分區資料建立 BigLake 資料表，其中：

* 已指定結構定義。
* 資料表的中繼資料快取過時間隔為 8 小時。
* 中繼資料快取必須手動重新整理。

```
CREATE EXTERNAL TABLE `my_dataset.my_table`
(
  ProductId INTEGER,
  ProductName STRING,
  ProductType STRING
)
WITH PARTITION COLUMNS
(
  sku STRING,
)
WITH CONNECTION `us.my-connection`
OPTIONS(
  hive_partition_uri_prefix = "gs://mybucket/products",
  uris = ['gs://mybucket/products/*'],
  max_staleness = INTERVAL 8 HOUR,
  metadata_cache_mode = 'MANUAL'
);
```

### bq

首先，請使用 [`bq mkdef`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_mkdef) 指令建立資料表定義檔：

```
bq mkdef \
--source_format=SOURCE_FORMAT \
--connection_id=REGION.CONNECTION_ID \
--hive_partitioning_mode=PARTITIONING_MODE \
--hive_partitioning_source_uri_prefix=GCS_URI_SHARED_PREFIX \
--require_hive_partition_filter=BOOLEAN \
--metadata_cache_mode=CACHE_MODE \
 GCS_URIS > DEFINITION_FILE
```

更改下列內容：

* `SOURCE_FORMAT`：外部資料來源的格式。例如：`CSV`。
* `REGION`：包含連線的區域，例如 `us`。
* `CONNECTION_ID`：連線 ID，例如 `myconnection`。

  在 Google Cloud 控制台中[查看連線詳細資料](https://docs.cloud.google.com/bigquery/docs/working-with-connections?hl=zh-tw#view-connections)時，連線 ID 是「連線 ID」中顯示的完整連線 ID 最後一個區段的值，例如 `projects/myproject/locations/connection_location/connections/myconnection`。

  如要使用[預設連線](https://docs.cloud.google.com/bigquery/docs/default-connections?hl=zh-tw)，請指定 `DEFAULT`，而非包含 PROJECT\_ID.REGION.CONNECTION\_ID 的連線字串。
* `PARTITIONING_MODE`：Hive 分區模式。請使用下列其中一個值：

  + `AUTO`：自動偵測索引鍵名稱和類型。
  + `STRINGS`：自動將鍵名轉換為字串。
  + `CUSTOM`：在來源 URI 前置字串中編碼索引鍵結構定義。
* `GCS_URI_SHARED_PREFIX`：來源 URI 前置字串。
* `BOOLEAN`：指定是否要在查詢時要求述詞篩選器。這個標記是選用的，預設值為 `false`。
* `CACHE_MODE`：指定中繼資料快取是否自動或手動重新整理。如果您也打算在後續的 `bq mk` 指令中使用 `--max_staleness` 標記來啟用中繼資料快取，才需要加入這個標記。如要進一步瞭解中繼資料快取注意事項，請參閱「[中繼資料快取，提升效能](https://docs.cloud.google.com/bigquery/docs/biglake-intro?hl=zh-tw#metadata_caching_for_performance)」。

  設為 `AUTOMATIC`，中繼資料快取就會以系統定義的時間間隔 (通常介於 30 到 60 分鐘之間) 重新整理。

  如要依您決定的時間表重新整理中繼資料快取，請設為 `MANUAL`。在這種情況下，您可以呼叫 [`BQ.REFRESH_EXTERNAL_METADATA_CACHE` 系統程序](https://docs.cloud.google.com/bigquery/docs/reference/system-procedures?hl=zh-tw#bqrefresh_external_metadata_cache)來重新整理快取。

  如果 `STALENESS_INTERVAL` 設為大於 0 的值，就必須設定 `CACHE_MODE`。
* `GCS_URIS`：Cloud Storage 資料夾的路徑，使用萬用字元格式。
* `DEFINITION_FILE`：本機電腦上[資料表定義檔](https://docs.cloud.google.com/bigquery/external-table-definition?hl=zh-tw)的路徑。

如果 `PARTITIONING_MODE` 為 `CUSTOM`，請在來源 URI 前置字串中加入分區索引鍵結構定義，格式如下：

```
--hive_partitioning_source_uri_prefix=GCS_URI_SHARED_PREFIX/{KEY1:TYPE1}/{KEY2:TYPE2}/...
```

建立資料表定義檔後，請使用 [`bq mk`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#mk-table) 指令建立 BigLake 資料表：

```
bq mk --external_table_definition=DEFINITION_FILE \
--max_staleness=STALENESS_INTERVAL \
DATASET_NAME.TABLE_NAME \
SCHEMA
```

更改下列內容：

* `DEFINITION_FILE`：資料表定義檔的路徑。
* `STALENESS_INTERVAL`：指定對 BigLake 資料表執行的作業是否使用快取中繼資料，以及快取中繼資料必須有多新，作業才能使用。如要使用此旗標，您必須在先前的 `bq mkdef` 指令中，為 `--metadata_cache_mode` 旗標指定值。如要進一步瞭解中繼資料快取注意事項，請參閱「[中繼資料快取，提升效能](https://docs.cloud.google.com/bigquery/docs/biglake-intro?hl=zh-tw#metadata_caching_for_performance)」。

  如要停用中繼資料快取功能，請指定 0。這是目前的預設做法。

  如要啟用中繼資料快取，請使用[`INTERVAL` 資料類型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#interval_type)文件所述的 `Y-M D H:M:S` 格式，指定 30 分鐘到 7 天之間的時間間隔值。舉例來說，如要指定 4 小時的過時間隔，請輸入 `0-0 0 4:0:0`。如果資料表在過去 4 小時內重新整理過，針對該資料表執行的作業就會使用快取中繼資料。如果快取中繼資料的建立時間較早，作業就會改為從 Cloud Storage 擷取中繼資料。
* `DATASET_NAME`：包含資料表的資料集名稱。
* `TABLE_NAME`：您要建立的資料表名稱。
* `SCHEMA`：指定 [JSON 結構定義檔](https://docs.cloud.google.com/bigquery/docs/schemas?hl=zh-tw#specifying_a_json_schema_file)的路徑，或以 `field:data_type,field:data_type,...` 形式指定結構定義。如要使用結構定義自動偵測功能，請省略這個引數。

**範例**

下列範例使用 `AUTO` Hive 分區模式，並將中繼資料快取設為 12 小時的過時間隔，且會自動重新整理：

```
bq mkdef --source_format=CSV \
  --connection_id=us.my-connection \
  --hive_partitioning_mode=AUTO \
  --hive_partitioning_source_uri_prefix=gs://myBucket/myTable \
  --metadata_cache_mode=AUTOMATIC \
  gs://myBucket/myTable/* > mytable_def

bq mk --external_table_definition=mytable_def \
  --max_staleness=0-0 0 12:0:0 \
  mydataset.mytable \
  Region:STRING,Quarter:STRING,Total_sales:INTEGER
```

以下範例使用 `STRING` Hive 分割模式：

```
bq mkdef --source_format=CSV \
  --connection_id=us.my-connection \
  --hive_partitioning_mode=STRING \
  --hive_partitioning_source_uri_prefix=gs://myBucket/myTable \
  gs://myBucket/myTable/* > mytable_def

bq mk --external_table_definition=mytable_def \
  mydataset.mytable \
  Region:STRING,Quarter:STRING,Total_sales:INTEGER
```

以下範例使用 `CUSTOM` Hive 分割模式：

```
bq mkdef --source_format=CSV \
  --connection_id=us.my-connection \
  --hive_partitioning_mode=CUSTOM \
  --hive_partitioning_source_uri_prefix=gs://myBucket/myTable/{dt:DATE}/{val:STRING} \
  gs://myBucket/myTable/* > mytable_def

bq mk --external_table_definition=mytable_def \
  mydataset.mytable \
  Region:STRING,Quarter:STRING,Total_sales:INTEGER
```

### API

如要使用 BigQuery API 設定 Hive 分區，請在建立[資料表定義檔](https://docs.cloud.google.com/bigquery/external-table-definition?hl=zh-tw)時，將 [`hivePartitioningOptions`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables?hl=zh-tw#hivepartitioningoptions) 物件納入 [`ExternalDataConfiguration`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables?hl=zh-tw#externaldataconfiguration) 物件。如要建立 BigLake 資料表，您也必須為 `connectionId` 欄位指定值。

如果將 `hivePartitioningOptions.mode` 欄位設為 `CUSTOM`，則必須在 `hivePartitioningOptions.sourceUriPrefix` 欄位中編碼分區索引鍵結構定義，如下所示：`gs://BUCKET/PATH_TO_TABLE/{KEY1:TYPE1}/{KEY2:TYPE2}/...`

如要在查詢時強制使用述詞篩選器，請將 `hivePartitioningOptions.requirePartitionFilter` 欄位設為 `true`。

### Terraform

這個範例會根據分區資料建立 BigLake 資料表。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
# This creates a bucket in the US region named "my-bucket" with a pseudorandom
# suffix.
resource "random_id" "default" {
  byte_length = 8
}
resource "google_storage_bucket" "default" {
  name                        = "my-bucket-${random_id.default.hex}"
  location                    = "US"
  force_destroy               = true
  uniform_bucket_level_access = true
}

resource "google_storage_bucket_object" "default" {
  # This creates a fake message to create partition locations on the table.
  # Otherwise, the table deployment fails.
  name    = "publish/dt=2000-01-01/hr=00/min=00/fake_message.json"
  content = "{\"column1\": \"XXX\"}"
  bucket  = google_storage_bucket.default.name
}

# This queries the provider for project information.
data "google_project" "default" {}

# This creates a connection in the US region named "my-connection".
# This connection is used to access the bucket.
resource "google_bigquery_connection" "default" {
  connection_id = "my-connection"
  location      = "US"
  cloud_resource {}
}

# This grants the previous connection IAM role access to the bucket.
resource "google_project_iam_member" "default" {
  role    = "roles/storage.objectViewer"
  project = data.google_project.default.id
  member  = "serviceAccount:${google_bigquery_connection.default.cloud_resource[0].service_account_id}"
}

# This makes the script wait for seven minutes before proceeding. This lets IAM
# permissions propagate.
resource "time_sleep" "default" {
  create_duration = "7m"

  depends_on = [google_project_iam_member.default]
}

# This defines a Google BigQuery dataset with default expiration times for
# partitions and tables, a description, a location, and a maximum time travel.
resource "google_bigquery_dataset" "default" {
  dataset_id                      = "my_dataset"
  default_partition_expiration_ms = 2592000000  # 30 days
  default_table_expiration_ms     = 31536000000 # 365 days
  description                     = "My dataset description"
  location                        = "US"
  max_time_travel_hours           = 96 # 4 days

  # This defines a map of labels for the bucket resource,
  # including the labels "billing_group" and "pii".
  labels = {
    billing_group = "accounting",
    pii           = "sensitive"
  }
}

# This creates a BigQuery table with partitioning and automatic metadata
# caching.
resource "google_bigquery_table" "default" {
  dataset_id = google_bigquery_dataset.default.dataset_id
  table_id   = "my_table"
  schema     = jsonencode([{ "name" : "column1", "type" : "STRING", "mode" : "NULLABLE" }])
  external_data_configuration {
    # This defines an external data configuration for the BigQuery table
    # that reads Parquet data from the publish directory of the default
    # Google Cloud Storage bucket.
    autodetect    = false
    source_format = "PARQUET"
    connection_id = google_bigquery_connection.default.name
    source_uris   = ["gs://${google_storage_bucket.default.name}/publish/*"]
    # This configures Hive partitioning for the BigQuery table,
    # partitioning the data by date and time.
    hive_partitioning_options {
      mode                     = "CUSTOM"
      source_uri_prefix        = "gs://${google_storage_bucket.default.name}/publish/{dt:STRING}/{hr:STRING}/{min:STRING}"
      require_partition_filter = false
    }
    # This enables automatic metadata refresh.
    metadata_cache_mode = "AUTOMATIC"
  }


  # This sets the maximum staleness of the metadata cache to 10 hours.
  max_staleness = "0-0 0 10:0:0"

  depends_on = [
    time_sleep.default,
    google_storage_bucket_object.default
  ]
}
```

如要在 Google Cloud 專案中套用 Terraform 設定，請完成下列各節的步驟。

## 準備 Cloud Shell

1. 啟動 [Cloud Shell](https://shell.cloud.google.com/?hl=zh-tw)。
2. 設定要套用 Terraform 設定的預設 Google Cloud 專案。

   每項專案只需要執行一次這個指令，且可以在任何目錄中執行。

   ```
   export GOOGLE_CLOUD_PROJECT=PROJECT_ID
   ```

   如果您在 Terraform 設定檔中設定明確值，環境變數就會遭到覆寫。

## 準備目錄

每個 Terraform 設定檔都必須有自己的目錄 (也稱為*根模組*)。

1. 在 [Cloud Shell](https://shell.cloud.google.com/?hl=zh-tw) 中建立目錄，並在該目錄中建立新檔案。檔案名稱的副檔名必須是 `.tf`，例如 `main.tf`。在本教學課程中，這個檔案稱為 `main.tf`。

   ```
   mkdir DIRECTORY && cd DIRECTORY && touch main.tf
   ```
2. 如果您正在學習教學課程，可以複製每個章節或步驟中的程式碼範例。

   將程式碼範例複製到新建立的 `main.tf`。

   視需要從 GitHub 複製程式碼。如果 Terraform 代码片段是端對端解決方案的一部分，建議您使用這個方法。
3. 查看並修改範例參數，套用至您的環境。
4. 儲存變更。
5. 初始化 Terraform。每個目錄只需執行一次這項操作。

   ```
   terraform init
   ```

   如要使用最新版 Google 供應商，請加入 `-upgrade` 選項：

   ```
   terraform init -upgrade
   ```

## 套用變更

1. 檢查設定，確認 Terraform 即將建立或更新的資源符合您的預期：

   ```
   terraform plan
   ```

   視需要修正設定。
2. 執行下列指令，並在提示中輸入 `yes`，套用 Terraform 設定：

   ```
   terraform apply
   ```

   等待 Terraform 顯示「Apply complete!」訊息。
3. [開啟 Google Cloud 專案](https://console.cloud.google.com/?hl=zh-tw)即可查看結果。在 Google Cloud 控制台中，前往 UI 中的資源，確認 Terraform 已建立或更新這些資源。

**注意：**Terraform 範例通常會假設 Google Cloud 專案已啟用必要的 API。

## 設定存取控管政策

您可以透過多種方法控管 BigLake 資料表的存取權：

* 如需設定資料欄層級安全防護機制的指引，請參閱[資料欄層級安全防護機制指南](https://docs.cloud.google.com/bigquery/docs/column-level-security?hl=zh-tw)。
* 如需設定資料遮蓋的指示，請參閱[資料遮蓋指南](https://docs.cloud.google.com/bigquery/docs/column-data-masking?hl=zh-tw)。
* 如需設定資料列層級安全防護機制的指引，請參閱[資料列層級的安全性指南](https://docs.cloud.google.com/bigquery/docs/managing-row-level-security?hl=zh-tw)。

舉例來說，假設您要限制資料集 `mydataset` 中資料表 `mytable` 的資料列存取權：

```
+---------+---------+-------+
| country | product | price |
+---------+---------+-------+
| US      | phone   |   100 |
| JP      | tablet  |   300 |
| UK      | laptop  |   200 |
+---------+---------+-------+
```

您可以為 Kim (`kim@example.com`) 建立資料列層級的篩選器，限制他們只能存取 `country` 等於 `US` 的資料列。

```
CREATE ROW ACCESS POLICY only_us_filter
ON mydataset.mytable
GRANT TO ('user:kim@example.com')
FILTER USING (country = 'US');
```

接著，Kim 執行下列查詢：

```
SELECT * FROM projectid.mydataset.mytable;
```

輸出結果只會顯示 `country` 等於 `US` 的資料列：

```
+---------+---------+-------+
| country | product | price |
+---------+---------+-------+
| US      | phone   |   100 |
+---------+---------+-------+
```

## 查詢 BigLake 資料表

詳情請參閱[查詢 BigLake 資料表中的 Cloud Storage 資料](https://docs.cloud.google.com/bigquery/docs/query-cloud-storage-using-biglake?hl=zh-tw)。

## 更新 BigLake 資料表

您可以視需要更新 BigLake 資料表，例如變更[中繼資料快取](https://docs.cloud.google.com/bigquery/docs/biglake-intro?hl=zh-tw#metadata_caching_for_performance)。如要取得資料表詳細資料 (例如來源格式和來源 URI)，請參閱「[取得資料表資訊](https://docs.cloud.google.com/bigquery/docs/tables?hl=zh-tw#get_table_information)」。

您也可以使用相同程序，將以 Cloud Storage 為基礎的外部資料表連結至連線，藉此升級為 BigLake 資料表。詳情請參閱[將外部資料表升級為 BigLake 資料表](https://docs.cloud.google.com/bigquery/docs/external-data-cloud-storage?hl=zh-tw#upgrade-external-tables-to-biglake-tables)。

如要更新 BigLake 資料表，請選取下列其中一個選項：

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

     設為 `AUTOMATIC`，中繼資料快取就會以系統定義的時間間隔 (通常介於 30 到 60 分鐘之間) 重新整理。

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

**範例**

以下範例會更新 `mytable`，只要快取中繼資料在過去 4.5 小時內重新整理過，就會使用該資料，並自動重新整理快取中繼資料：

```
bq update --project_id=myproject --max_staleness='0-0 0 4:30:0' \
--external_table_definition=enable_metadata.json mydataset.mytable
```

其中 `enable_metadata.json` 包含下列內容：
`json
{
"metadataCacheMode": "AUTOMATIC"
}`

## 稽核記錄

如要瞭解 BigQuery 中的記錄，請參閱「[BigQuery 監控簡介](https://docs.cloud.google.com/bigquery/docs/monitoring?hl=zh-tw)」。如要進一步瞭解 Google Cloud中的記錄，請參閱 [Cloud Logging](https://docs.cloud.google.com/logging/docs?hl=zh-tw)。

## 後續步驟

* 進一步瞭解 [BigLake](https://docs.cloud.google.com/bigquery/docs/biglake-intro?hl=zh-tw)。
* 瞭解 [Cloud Storage](https://docs.cloud.google.com/storage/docs/introduction?hl=zh-tw)。
* 瞭解如何[查詢 Amazon Web Services (AWS) 資料](https://docs.cloud.google.com/bigquery/docs/omni-aws-introduction?hl=zh-tw)。
* 瞭解如何[查詢 Microsoft Azure 資料](https://docs.cloud.google.com/bigquery/docs/omni-azure-introduction?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-09 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-09 (世界標準時間)。"],[],[]]