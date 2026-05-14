Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# Azure Blob 儲存體的外部資料表

本文說明如何建立 Azure Blob 儲存體 BigLake 資料表。[BigLake 資料表](https://docs.cloud.google.com/bigquery/docs/biglake-intro?hl=zh-tw)可讓您使用存取權委派功能，查詢 Blob 儲存空間中的資料。存取權委派功能可將 BigLake 資料表的存取權，與基礎資料儲存空間的存取權分開。

如要瞭解 BigQuery 與 Blob 儲存空間之間的資料流程，請參閱[查詢資料時的資料流程](https://docs.cloud.google.com/bigquery/docs/omni-introduction?hl=zh-tw#query-data)。

## 事前準備

確認你已[連線至 Blob 儲存體，可存取其中的資料](https://docs.cloud.google.com/bigquery/docs/omni-azure-create-connection?hl=zh-tw)。

### 必要的角色

如要取得建立外部資料表所需的權限，請要求管理員授予您資料集的「[BigQuery 管理員](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.admin) 」(`roles/bigquery.admin`) IAM 角色。如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

這個預先定義的角色具備建立外部資料表所需的權限。如要查看確切的必要權限，請展開「Required permissions」(必要權限) 部分：

#### 所需權限

如要建立外部資料表，必須具備下列權限：

* `bigquery.tables.create`
* `bigquery.connections.delegate`

您或許還可透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)取得這些權限。

## 建立資料集

建立外部資料表前，您必須先在[支援的區域](https://docs.cloud.google.com/bigquery/docs/omni-introduction?hl=zh-tw#locations)中建立資料集。選取下列其中一個選項：

### 控制台

1. 前往「BigQuery」頁面

   [前往 BigQuery](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中，選取要建立資料集的專案。
4. 依序點選 more\_vert「View actions」(查看動作) 和「Create dataset」(建立資料集)。
5. 在「建立資料集」頁面中，指定下列詳細資料：

1. 針對「Dataset ID」(資料集 ID)，輸入唯一的資料集[名稱](https://docs.cloud.google.com/bigquery/docs/datasets?hl=zh-tw#dataset-naming)。
2. 針對「Data location」(資料位置)，選擇[支援的地區](https://docs.cloud.google.com/bigquery/docs/omni-introduction?hl=zh-tw#locations)。
3. 選用：如要自動刪除資料表，請勾選「Enable table expiration」(啟用資料表到期時間) 核取方塊，並以天為單位設定「Default maximum table age」(預設資料表存在時間上限)。資料表到期時，系統不會刪除 Azure 中的資料。
4. 如要使用[預設定序](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/collation-concepts?hl=zh-tw)，請展開「進階選項」部分，然後選取「啟用預設定序」選項。
5. 點選「建立資料集」。

### SQL

使用 [`CREATE SCHEMA` DDL 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#create_schema_statement)。以下範例會在
`azure-eastus2` 地區建立資料集：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列陳述式：

   ```
   CREATE SCHEMA mydataset
   OPTIONS (
     location = 'azure-eastus2');
   ```
3. 按一下「執行」play\_circle。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

### bq

在指令列環境中，使用 [`bq mk` 指令建立資料集：](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#mk-dataset)

```
bq --location=LOCATION mk \
    --dataset \
PROJECT_ID:DATASET_NAME
```

`--project_id` 參數會覆寫預設專案。

更改下列內容：

* `LOCATION`：資料集位置

  如要瞭解支援的地區，請參閱「[位置](https://docs.cloud.google.com/bigquery/docs/omni-introduction?hl=zh-tw#locations)」一文。建立資料集後，就無法變更位置。您可以使用 [`.bigqueryrc` 檔案](https://docs.cloud.google.com/bigquery/docs/bq-command-line-tool?hl=zh-tw#setting_default_values_for_command-line_flags)設定位置的預設值。
* `PROJECT_ID`：專案 ID
* `DATASET_NAME`：要建立的資料集名稱

  如要在非預設專案中建立資料集，請採用下列格式將專案 ID 新增至資料集：`PROJECT_ID:DATASET_NAME`。

## 在未分區的資料上建立 BigLake 資料表

選取下列選項之一：

### 控制台

1. 前往「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。

   如果沒有看到左側窗格，請按一下 last\_page「Expand left pane」(展開左側窗格)，開啟窗格。
3. 在「Explorer」窗格中展開專案，按一下「Datasets」(資料集)，然後選取資料集。
4. 在「資料集資訊」部分，按一下 add\_box「建立資料表」。
5. 在「Create table」(建立資料表) 頁面的「Source」(來源) 區段中，執行下列操作：

   1. 在「Create table from」(使用下列資料建立資料表) 部分，選取「Azure Blob Storage」(Azure Blob 儲存體)。
   2. 在「選取 Azure Blob 儲存體路徑」中，使用下列格式輸入 Blob 儲存體路徑：
      `azure://AZURE_STORAGE_ACCOUNT_NAME.blob.core.windows.net/CONTAINER_NAME/FILE_PATH`

      更改下列內容：

      * `AZURE_STORAGE_ACCOUNT_NAME`：Blob 儲存體帳戶的名稱。帳戶的地區應與資料集的地區相同。
      * `CONTAINER_NAME`：Blob 儲存體容器的名稱。
      * `FILE_PATH`：指向 Blob 儲存空間資料的資料路徑。舉例來說，如果是單一 CSV 檔案，`FILE_PATH` 可以是 `myfile.csv`。
   3. 在「File format」(檔案格式) 部分選取 Azure 中的資料格式。支援的格式包括 **AVRO**、**CSV**、**DELTA\_LAKE**、**ICEBERG**、**JSONL**、**ORC** 和 **PARQUET**。
6. 在「目的地」部分，執行下列操作：

   1. 在「Dataset」(資料集) 中選擇適當的資料集。
   2. 在「Table」(資料表) 欄位中，輸入資料表名稱。
   3. 確認「Table type」(資料表類型) 已設為 [External table] (外部資料表)。
   4. 在「Connection ID」(連線 ID) 專區中，從下拉式選單選擇適當的連線 ID。如要瞭解連線，請參閱「[連線至 Blob 儲存體](https://docs.cloud.google.com/bigquery/docs/omni-azure-create-connection?hl=zh-tw)」一文。
7. 在「Schema」(結構定義) 區段中，您可以啟用[結構定義自動偵測](https://docs.cloud.google.com/bigquery/docs/schema-detect?hl=zh-tw)功能，也可以在有來源檔案時手動指定結構定義。如果沒有來源檔案，就必須手動指定結構定義。

   * 如要啟用結構定義自動偵測功能，請選取「自動偵測」選項。
   * 如要手動指定結構定義，請取消勾選「自動偵測」選項。啟用「以文字形式編輯」，然後以 [JSON 陣列](https://docs.cloud.google.com/bigquery/docs/schemas?hl=zh-tw#specifying_a_json_schema_file)的形式輸入資料表結構定義。
8. 點選「建立資料表」。

**注意：** 如果是 Avro、Parquet 和 ORC 檔案格式，您不必指定資料表結構定義，因為 BigQuery Omni 會從來源檔案自動偵測資料表結構定義。如果是 CSV、JSON 和 Google 試算表檔案格式，請勾選「自動偵測」，以自動偵測結構定義。

### SQL

如要建立 BigLake 資料表，請使用 [`CREATE EXTERNAL TABLE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#create_external_table_statement) 陳述式和 `WITH CONNECTION` 子句：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列陳述式：

   ```
   CREATE EXTERNAL TABLE DATASET_NAME.TABLE_NAME
   WITH CONNECTION `AZURE_LOCATION.CONNECTION_NAME`
     OPTIONS (
       format = 'DATA_FORMAT',
       uris = ['azure://AZURE_STORAGE_ACCOUNT_NAME.blob.core.windows.net/CONTAINER_NAME/FILE_PATH']);
   ```

   請替換下列項目：

   * `DATASET_NAME`：您建立的資料集名稱
   * `TABLE_NAME`：您要為這個資料表指定的名稱
   * `AZURE_LOCATION`：Azure 位置，例如 `azure-eastus2` Google Cloud
   * `CONNECTION_NAME`：您建立的連線名稱
   * `DATA_FORMAT`：任何支援的 [BigQuery 聯合格式](https://docs.cloud.google.com/bigquery/external-data-sources?hl=zh-tw)，例如 `AVRO`、`CSV`、`DELTA_LAKE` 或 `ICEBERG` ([預覽版](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages))
   * `AZURE_STORAGE_ACCOUNT_NAME`：Blob 儲存空間帳戶的名稱
   * `CONTAINER_NAME`：Blob 儲存體容器的名稱
   * `FILE_PATH`：指向 Blob 儲存體資料的資料路徑
3. 按一下「執行」play\_circle。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

範例：

```
CREATE EXTERNAL TABLE absdataset.abstable
WITH CONNECTION `azure-eastus2.abs-read-conn`
  OPTIONS (
    format = 'CSV', uris = ['azure://account_name.blob.core.windows.net/container/path/file.csv']);
```

### bq

建立[資料表定義檔](https://docs.cloud.google.com/bigquery/external-table-definition?hl=zh-tw)：

```
bq mkdef  \
    --source_format=DATA_FORMAT \
    --connection_id=AZURE_LOCATION.CONNECTION_NAME \
    "azure://AZURE_STORAGE_ACCOUNT_NAME.blob.core.windows.net/CONTAINER_NAME/FILE_PATH" > table_def
```

更改下列內容：

* `DATA_FORMAT`：任何支援的 [BigQuery 聯合格式](https://docs.cloud.google.com/bigquery/external-data-sources?hl=zh-tw)，例如 `AVRO`、`CSV`、`ICEBERG` 或 `PARQUET`
* `AZURE_LOCATION`：Azure 位置，例如 `azure-eastus2` Google Cloud
* `CONNECTION_NAME`：您建立的連線名稱
* `AZURE_STORAGE_ACCOUNT_NAME`：Blob 儲存空間帳戶的名稱
* `CONTAINER_NAME`：Blob 儲存體容器的名稱
* `FILE_PATH`：指向 Blob 儲存體資料的資料路徑

接著，建立 BigLake 資料表：

```
bq mk --external_table_definition=table_def DATASET_NAME.TABLE_NAME
```

更改下列內容：

* `DATASET_NAME`：您建立的資料集名稱
* `TABLE_NAME`：您要為這個資料表指定的名稱

舉例來說，下列指令會建立新的 BigLake 資料表 `my_dataset.my_table`，該資料表可查詢儲存在路徑 `azure://account_name.blob.core.windows.net/container/path` 的 Blob 儲存體資料，且在位置 `azure-eastus2` 中有讀取連線：

```
bq mkdef \
    --source_format=AVRO \
    --connection_id=azure-eastus2.read-conn \
    "azure://account_name.blob.core.windows.net/container/path" > table_def

bq mk \
    --external_table_definition=table_def my_dataset.my_table
```

**注意：** 如要覆寫預設專案，請使用 `--project_id=PROJECT_ID` 參數。將 `PROJECT_ID` 替換為 Google Cloud 專案 ID。

### API

呼叫 [`tables.insert` 方法](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables/insert?hl=zh-tw) API 方法，並在您傳入的 [`Table` 資源](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables?hl=zh-tw#Table)中建立 [`ExternalDataConfiguration`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables?hl=zh-tw#externaldataconfiguration)。

指定 `schema` 屬性，或將 `autodetect` 屬性設為 `true`，為支援的資料來源啟用結構定義自動偵測功能。

指定 `connectionId` 屬性，找出要用於連線至 Blob 儲存體的連線。

## 根據分區資料建立 BigLake 資料表

您可以在 Blob Storage 中，為 Hive 分區資料建立 BigLake 資料表。建立外部分區資料表後，您就無法變更分區鍵。如要變更分割區鍵，您必須重新建立資料表。

如要根據 Hive 分區資料建立 BigLake 資料表，請選取下列任一選項：

### 控制台

1. 前往「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。

   如果沒有看到左側窗格，請按一下 last\_page「Expand left pane」(展開左側窗格)，開啟窗格。
3. 在「Explorer」窗格中展開專案，按一下「Datasets」(資料集)，然後選取資料集。
4. 按一下 [Create table] (建立資料表)。「建立資料表」窗格隨即開啟。
5. 在「來源」部分，指定下列詳細資料：

   1. 在「Create table from」(建立資料表來源) 部分，選取下列任一選項：

      * **Amazon S3**
      * **Azure Blob 儲存體**
   2. 使用[萬用字元](https://docs.cloud.google.com/bigquery/docs/batch-loading-data?hl=zh-tw#load-wildcards)提供資料夾路徑。例如：

      * Amazon S3：`s3://mybucket/*`
      * Blob 儲存空間：`azure://mystorageaccount.blob.core.windows.net/mycontainer/*`

      資料夾的位置必須與要建立、附加或覆寫的資料表所在的資料集位置相同。
   3. 從「檔案格式」清單中選取檔案類型。
   4. 選取「來源資料分割」核取方塊，然後指定下列詳細資料：

      1. 在「選取來源 URI 前置字串」中，輸入 URI 前置字串。例如：`s3://mybucket/my_files`。
      2. 選用：如要對這個資料表的所有查詢強制使用分區篩選器，請選取「需要分區篩選器」核取方塊。
         使用分區篩選器可以降低成本並提升效能。詳情請參閱[在查詢中對分區鍵套用述詞篩選器](https://docs.cloud.google.com/bigquery/docs/hive-partitioned-queries-gcs?hl=zh-tw#requiring_predicate_filters_on_partition_keys_in_queries)。
      3. 在「Partition inference mode」(分割區推論模式) 部分，選取下列其中一個選項：

         * **自動推論類型**：將分區結構定義偵測模式設為 `AUTO`。
         * **將所有資料欄視為字串**：將分區結構定義偵測模式設為 `STRINGS`。
         * **提供自己的結構定義**：將分區結構定義偵測模式設為 `CUSTOM`，然後手動輸入分區鍵的結構定義資訊。詳情請參閱「[自訂分區索引鍵結構定義](https://docs.cloud.google.com/bigquery/docs/hive-partitioned-loads-gcs?hl=zh-tw#custom_partition_key_schema)」。
6. 在「目的地」部分，指定下列詳細資料：

   1. 在「Project」(專案) 部分，選取要建立資料表的專案。
   2. 在「Dataset」(資料集) 部分，選取要建立資料表的資料集。
   3. 在「Table」(資料表) 中，輸入要建立的資料表名稱。
   4. 確認「Table type」(資料表類型) 已選取「External table」(外部資料表)。
   5. 在「連線 ID」部分，選取您先前建立的連線。
7. 在「Schema」(結構定義) 區段中，您可以啟用[結構定義自動偵測](https://docs.cloud.google.com/bigquery/docs/schema-detect?hl=zh-tw)功能，也可以在有來源檔案時手動指定結構定義。如果沒有來源檔案，就必須手動指定結構定義。

   * 如要啟用結構定義自動偵測功能，請選取「自動偵測」選項。
   * 如要手動指定結構定義，請取消勾選「自動偵測」選項。啟用「以文字形式編輯」，然後以 [JSON 陣列](https://docs.cloud.google.com/bigquery/docs/schemas?hl=zh-tw#specifying_a_json_schema_file)的形式輸入資料表結構定義。
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
   WITH CONNECTION `PROJECT_ID.REGION.CONNECTION_ID`
   OPTIONS (
     hive_partition_uri_prefix = "HIVE_PARTITION_URI_PREFIX",
     uris=['FILE_PATH'],
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
   * `CONNECTION_ID`：連線名稱，例如 `myconnection`
   * `HIVE_PARTITION_URI_PREFIX`：Hive 分區 URI 前置字串，例如：
     + `s3://mybucket/`
     + `azure://mystorageaccount.blob.core.windows.net/mycontainer/`
   * `FILE_PATH`：您要建立的外部資料表資料來源路徑，例如：
     + `s3://mybucket/*.parquet`
     + `azure://mystorageaccount.blob.core.windows.net/mycontainer/*.parquet`
   * `TABLE_FORMAT`：要建立的資料表格式，例如 `PARQUET`
3. 按一下「執行」play\_circle。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

**範例**

下列範例會根據 Amazon S3 中的分區資料建立 BigLake 資料表。結構定義由系統自動偵測。

```
CREATE EXTERNAL TABLE `my_dataset.my_table`
WITH PARTITION COLUMNS
(
  sku STRING,
)
WITH CONNECTION `us.my-connection`
OPTIONS(
  hive_partition_uri_prefix = "s3://mybucket/products",
  uris = ['s3://mybucket/products/*']
);
```

下列範例會在 Blob 儲存空間中的分區資料上建立 BigLake 資料表。已指定結構定義。

```
CREATE EXTERNAL TABLE `my_dataset.my_table`
(
  ProductId INTEGER,
  ProductName, STRING,
  ProductType, STRING
)
WITH PARTITION COLUMNS
(
  sku STRING,
)
WITH CONNECTION `us.my-connection`
OPTIONS(
  hive_partition_uri_prefix = "azure://mystorageaccount.blob.core.windows.net/mycontainer/products",
  uris = ['azure://mystorageaccount.blob.core.windows.net/mycontainer/*']
);
```

### bq

首先，請使用 [`bq mkdef`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_mkdef) 指令建立資料表定義檔：

```
bq mkdef \
--source_format=SOURCE_FORMAT \
--connection_id=REGION.CONNECTION_ID \
--hive_partitioning_mode=PARTITIONING_MODE \
--hive_partitioning_source_uri_prefix=URI_SHARED_PREFIX \
--require_hive_partition_filter=BOOLEAN \
 URIS > DEFINITION_FILE
```

更改下列內容：

* `SOURCE_FORMAT`：外部資料來源的格式。例如：`CSV`。
* `REGION`：包含連線的區域，例如 `us`。
* `CONNECTION_ID`：連線名稱，例如 `myconnection`。
* `PARTITIONING_MODE`：Hive 分區模式。請使用下列其中一個值：
  + `AUTO`：自動偵測索引鍵名稱和類型。
  + `STRINGS`：自動將鍵名轉換為字串。
  + `CUSTOM`：在來源 URI 前置字串中編碼索引鍵結構定義。
* `URI_SHARED_PREFIX`：來源 URI 前置字串。
* `BOOLEAN`：指定是否要在查詢時要求述詞篩選器。這個標記是選用的，預設值為 `false`。
* `URIS`：Amazon S3 或 Blob Storage 資料夾的路徑，使用萬用字元格式。
* `DEFINITION_FILE`：本機電腦上[資料表定義檔](https://docs.cloud.google.com/bigquery/external-table-definition?hl=zh-tw)的路徑。

如果 `PARTITIONING_MODE` 為 `CUSTOM`，請在來源 URI 前置字串中加入分區索引鍵結構定義，格式如下：

```
--hive_partitioning_source_uri_prefix=GCS_URI_SHARED_PREFIX/{KEY1:TYPE1}/{KEY2:TYPE2}/...
```

建立資料表定義檔後，請使用 [`bq mk`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#mk-table) 指令建立 BigLake 資料表：

```
bq mk --external_table_definition=DEFINITION_FILE \
DATASET_NAME.TABLE_NAME \
SCHEMA
```

更改下列內容：

* `DEFINITION_FILE`：資料表定義檔的路徑。
* `DATASET_NAME`：包含資料表的資料集名稱。
* `TABLE_NAME`：您要建立的資料表名稱。
* `SCHEMA`：指定 [JSON 結構定義檔](https://docs.cloud.google.com/bigquery/docs/schemas?hl=zh-tw#specifying_a_json_schema_file)的路徑，或以 `field:data_type,field:data_type,...` 形式指定結構定義。如要使用結構定義自動偵測功能，請省略這個引數。

**範例**

以下範例使用 Amazon S3 資料的 `AUTO` Hive 分割模式：

```
bq mkdef --source_format=CSV \
  --connection_id=us.my-connection \
  --hive_partitioning_mode=AUTO \
  --hive_partitioning_source_uri_prefix=s3://mybucket/myTable \
  --metadata_cache_mode=AUTOMATIC \
  s3://mybucket/* > mytable_def

bq mk --external_table_definition=mytable_def \
  mydataset.mytable \
  Region:STRING,Quarter:STRING,Total_sales:INTEGER
```

以下範例使用 Amazon S3 資料的 `STRING` Hive 分割模式：

```
bq mkdef --source_format=CSV \
  --connection_id=us.my-connection \
  --hive_partitioning_mode=STRING \
  --hive_partitioning_source_uri_prefix=s3://mybucket/myTable \
  s3://mybucket/myTable/* > mytable_def

bq mk --external_table_definition=mytable_def \
  mydataset.mytable \
  Region:STRING,Quarter:STRING,Total_sales:INTEGER
```

以下範例使用 `CUSTOM` Hive 分區模式處理 Blob 儲存空間資料：

```
bq mkdef --source_format=CSV \
  --connection_id=us.my-connection \
  --hive_partitioning_mode=CUSTOM \
  --hive_partitioning_source_uri_prefix=azure://mystorageaccount.blob.core.windows.net/mycontainer/{dt:DATE}/{val:STRING} \
  azure://mystorageaccount.blob.core.windows.net/mycontainer/* > mytable_def

bq mk --external_table_definition=mytable_def \
  mydataset.mytable \
  Region:STRING,Quarter:STRING,Total_sales:INTEGER
```

### API

如要使用 BigQuery API 設定 Hive 分區，請在建立[資料表定義檔](https://docs.cloud.google.com/bigquery/external-table-definition?hl=zh-tw)時，將 [`hivePartitioningOptions`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables?hl=zh-tw#hivepartitioningoptions) 物件納入 [`ExternalDataConfiguration`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables?hl=zh-tw#externaldataconfiguration) 物件。如要建立 BigLake 資料表，您也必須為 `connectionId` 欄位指定值。

如果將 `hivePartitioningOptions.mode` 欄位設為 `CUSTOM`，則必須在 `hivePartitioningOptions.sourceUriPrefix` 欄位中編碼分區索引鍵結構定義，如下所示：`s3://BUCKET/PATH_TO_TABLE/{KEY1:TYPE1}/{KEY2:TYPE2}/...`

如要在查詢時強制使用述詞篩選器，請將 `hivePartitioningOptions.requirePartitionFilter` 欄位設為 `true`。

## Delta Lake 資料表

Delta Lake 是開放原始碼資料表格式，支援 PB 級資料表。Delta Lake 資料表可做為臨時和永久資料表查詢，並支援做為 [BigLake 資料表](https://docs.cloud.google.com/bigquery/docs/biglake-intro?hl=zh-tw)。

### 結構定義同步

Delta Lake 會將標準結構定義做為中繼資料的一部分。您無法使用 JSON 中繼資料檔案更新結構定義。如要更新結構定義，請按照下列步驟操作：

1. 使用 [`bq update` 指令](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_update)並加上 `--autodetect_schema` 旗標：

   ```
   bq update --autodetect_schema
   PROJECT_ID:DATASET.TABLE
   ```

   更改下列內容：

   * `PROJECT_ID`：包含要更新資料表的專案 ID
   * `DATASET`：包含要更新資料表的資料集
   * `TABLE`：要更新的資料表

### 類型轉換

BigQuery 會將 Delta Lake 資料類型轉換為下列 BigQuery 資料類型：

| **Delta Lake 類型** | **BigQuery 類型** |
| --- | --- |
| `boolean` | `BOOL` |
| `byte` | `INT64` |
| `int` | `INT64` |
| `long` | `INT64` |
| `float` | `FLOAT64` |
| `double` | `FLOAT64` |
| `Decimal(P/S)` | 視精確度而定，為 `NUMERIC` 或 `BIG_NUMERIC` |
| `date` | `DATE` |
| `time` | `TIME` |
| `timestamp (not partition column)` | `TIMESTAMP` |
| `timestamp (partition column)` | `DATETIME` |
| `string` | `STRING` |
| `binary` | `BYTES` |
| `array<Type>` | `ARRAY<Type>` |
| `struct` | `STRUCT` |
| `map<KeyType, ValueType>` | `ARRAY<Struct<key KeyType, value ValueType>>` |

### 限制

Delta Lake 資料表有以下限制：

* [外部資料表限制](https://docs.cloud.google.com/bigquery/docs/external-tables?hl=zh-tw#limitations)適用於 Delta Lake 資料表。
* Delta Lake 資料表僅支援 BigQuery Omni，且有相關[限制](https://docs.cloud.google.com/bigquery/docs/omni-introduction?hl=zh-tw#limitations)。
* 您無法使用新的 JSON 中繼資料檔案更新資料表。您必須使用自動偵測結構定義資料表更新作業。詳情請參閱「[結構定義同步](#schema_synchronization)」。
* BigLake 安全性功能僅在透過 BigQuery 服務存取時，保護 Delta Lake 資料表。

### 建立 Delta Lake 資料表

下列範例使用 [`CREATE EXTERNAL
TABLE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#create_external_table_statement) 陳述式和 Delta Lake 格式，建立外部資料表：

```
CREATE [OR REPLACE] EXTERNAL TABLE table_name
WITH CONNECTION connection_name
OPTIONS (
         format = 'DELTA_LAKE',
         uris = ["parent_directory"]
       );
```

更改下列內容：

* table\_name：資料表名稱。
* connection\_name：連線名稱。連線必須識別 [Amazon S3](https://docs.cloud.google.com/bigquery/docs/omni-aws-create-connection?hl=zh-tw) 或 [Blob 儲存體](https://docs.cloud.google.com/bigquery/docs/omni-azure-create-connection?hl=zh-tw)來源。
* parent\_directory：父項目錄的 URI。

### 使用 Delta Lake 進行跨雲端轉移

以下範例使用 [`LOAD DATA`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/other-statements?hl=zh-tw#load_data_statement) 陳述式，將資料載入適當的資料表：

```
LOAD DATA [INTO | OVERWRITE] table_name
FROM FILES (
        format = 'DELTA_LAKE',
        uris = ["parent_directory"]
)
WITH CONNECTION connection_name;
```

如需跨雲端資料移轉的更多範例，請參閱[使用跨雲端作業載入資料](https://docs.cloud.google.com/bigquery/docs/load-data-using-cross-cloud-transfer?hl=zh-tw#load-data)。

## 查詢 BigLake 資料表

詳情請參閱「[查詢 Blob 儲存體資料](https://docs.cloud.google.com/bigquery/docs/query-azure-data?hl=zh-tw)」。

## 使用 `INFORMATION_SCHEMA` 查看資源中繼資料

**預覽**

這項功能適用《[服務專屬條款](https://docs.cloud.google.com/terms/service-terms?hl=zh-tw#1)》中「一般服務條款」一節的《正式發布前產品條款》。正式發布前功能是依「原樣」提供，支援服務可能受限。
詳情請參閱[推出階段說明](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages)。

您可以使用 [`INFORMATION_SCHEMA`](https://docs.cloud.google.com/bigquery/docs/information-schema-intro?hl=zh-tw) 檢視表查看資源中繼資料。查詢 [`JOBS_BY_*`](https://docs.cloud.google.com/bigquery/docs/information-schema-jobs?hl=zh-tw)、[`JOBS_TIMELINE_BY_*`](https://docs.cloud.google.com/bigquery/docs/information-schema-jobs-timeline?hl=zh-tw) 和 [`RESERVATION*`](https://docs.cloud.google.com/bigquery/docs/information-schema-reservations?hl=zh-tw) 檢視區塊時，必須[指定與資料表所在區域位於同一位置的查詢處理位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw#specify_locations)。如要瞭解 BigQuery Omni 位置，請參閱「[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw#omni-loc)」。對於所有其他系統資料表，指定查詢工作位置是*選用*項目。

如要瞭解 BigQuery Omni 支援的系統資料表，請參閱[限制](https://docs.cloud.google.com/bigquery/docs/omni-introduction?hl=zh-tw#limitations)。

如要查詢 `JOBS_*` 和 `RESERVATION*` 系統資料表，請選取下列其中一種方法來指定處理位置：

### 控制台

1. 前往「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 如果沒有看到「編輯器」分頁，請按一下 add\_box「撰寫新查詢」。
3. 依序點選「更多」>「查詢設定」。系統隨即會開啟「查詢設定」對話方塊。
4. 在「查詢設定」對話方塊中，依序選取「其他設定」>「資料位置」，然後選取與 BigQuery Omni 區域共置的 [BigQuery 區域](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw#omni-loc)。舉例來說，如果 BigQuery Omni 區域是 `aws-us-east-1`，請指定 `us-east4`。
5. 選取其餘欄位，然後按一下「儲存」。

### bq

使用 `--location` 旗標，將作業的處理位置設為與 BigQuery Omni 區域共置的 [BigQuery 區域](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw#omni-loc)。舉例來說，如果 BigQuery Omni 區域是 `aws-us-east-1`，請指定 `us-east4`。

**範例**

```
bq query --use_legacy_sql=false --location=us-east4 \
"SELECT * FROM region-azure-eastus2.INFORMATION_SCHEMA.JOBS limit 10;"
```

### API

如果您是[透過程式執行工作](https://docs.cloud.google.com/bigquery/docs/running-jobs?hl=zh-tw)，請將位置引數設為與 BigQuery Omni 區域共置的 [BigQuery 區域](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw#omni-loc)。舉例來說，如果 BigQuery Omni 區域是 `aws-us-east-1`，請指定 `us-east4`。

## VPC Service Controls

您可以透過 VPC Service Controls perimeter，限制 BigQuery Omni 對外部雲端服務的存取權，做為額外的防禦層。舉例來說，VPC Service Controls 範圍可限制從 BigQuery Omni 資料表匯出資料，只能匯出至特定 Amazon S3 值區或 Blob 儲存體容器。

如要進一步瞭解 VPC Service Controls，請參閱「[VPC Service Controls 總覽](https://docs.cloud.google.com/vpc-service-controls/docs/overview?hl=zh-tw)」。

### 必要權限

確認您具備設定服務範圍的必要權限。如要查看設定 VPC Service Controls 時須具備的 IAM 角色清單，請參閱 VPC Service Controls 說明文件中的「[使用 IAM 控管存取權](https://docs.cloud.google.com/vpc-service-controls/docs/access-control?hl=zh-tw)」。

### 使用 Google Cloud 控制台設定 VPC Service Controls

1. 在 Google Cloud 控制台導覽選單中，依序按一下「Security」(安全性) 和「VPC Service Controls」。

   [前往 VPC Service Controls](https://console.cloud.google.com/security/service-perimeter?hl=zh-tw)
2. 如要為 BigQuery Omni 設定 VPC Service Controls，請按照「[建立服務範圍](https://docs.cloud.google.com/vpc-service-controls/docs/create-service-perimeters?hl=zh-tw#create_a_service_perimeter)」指南中的步驟操作，並在「輸出規則」窗格中執行下列步驟：

   1. 在「Egress rules」(輸出規則) 面板中，按一下「Add rule」(新增規則)。
   2. 在「From attributes of the API client」(API 用戶端的屬性) 部分，從「Identity」(身分) 清單中選取一個選項。
   3. 選取「外部資源的 TO 屬性」。
   4. 如要新增外部資源，請按一下「新增外部資源」。
   5. 在「新增外部資源」對話方塊中，為「外部資源名稱」輸入有效的資源名稱。例如：

      * Amazon Simple Storage Service (Amazon S3)：`s3://BUCKET_NAME`

        將 BUCKET\_NAME 替換為 Amazon S3 值區名稱。
      * Azure Blob 儲存體：`azure://myaccount.blob.core.windows.net/CONTAINER_NAME`

        將 CONTAINER NAME 替換為 Blob 儲存體容器名稱。

      如需輸出規則屬性清單，請參閱「[輸出規則參考資料](https://docs.cloud.google.com/vpc-service-controls/docs/ingress-egress-rules?hl=zh-tw#egress_rules_reference)」。
   6. 選取要在外部資源上允許的方法：

      1. 如要允許所有方法，請在「方法」清單中選取「所有方法」。
      2. 如要允許特定方法，請選取「選取的方法」，按一下「選取方法」，然後選取要在外部資源上允許的方法。
   7. 按一下「建立範圍」。

### 使用 gcloud CLI 設定 VPC Service Controls

如要使用 gcloud CLI 設定 VPC Service Controls，請按照下列步驟操作：

1. [設定預設存取權政策](#set-default-policy)。
2. [建立輸出政策輸入檔案](#create-egress-file)。
3. [新增輸出政策](#add-egress-policy)。

#### 設定預設存取權政策

存取權政策是適用全機構的容器，可存放存取層級和服務範圍。如要瞭解如何設定預設存取權政策或取得存取權政策名稱，請參閱「[管理存取權政策](https://docs.cloud.google.com/access-context-manager/docs/manage-access-policy?hl=zh-tw#set-default)」。

#### 建立輸出政策輸入檔案

輸出規則區塊會定義允許從 perimeter 內部存取該 perimeter 外部資源的權限。如果是外部資源，`externalResources` 屬性會定義允許從 VPC Service Controls perimeter 內存取的外部資源路徑。

可以使用 JSON 檔案或 YAML 檔案設定輸出規則。下列範例使用 `.yaml` 格式：

```
- egressTo:
    operations:
    - serviceName: bigquery.googleapis.com
      methodSelectors:
      - method: "*"
      *OR*
      - permission: "externalResource.read"
    externalResources:
      - EXTERNAL_RESOURCE_PATH
  egressFrom:
    identityType: IDENTITY_TYPE
    *OR*
    identities:
    - serviceAccount:SERVICE_ACCOUNT
```

* `egressTo`：列出 perimeter 外指定專案中 Google Cloud 資源允許的服務作業。
* `operations`：列出可存取的服務和動作/方法，滿足 `from` 區塊條件的用戶端可供存取。
* `serviceName`：設定 BigQuery Omni 的 `bigquery.googleapis.com`。
* `methodSelectors`：列出滿足 `from` 條件的用戶端可存取的方法。如要瞭解可限制的服務方法和權限，請參閱「[支援的服務方法限制](https://docs.cloud.google.com/vpc-service-controls/docs/supported-method-restrictions?hl=zh-tw)」。
* `method`：有效的服務方法，或 `\"*\"`，允許所有 `serviceName` 方法。
* `permission`：有效的服務權限，例如 `\"*\"`、`externalResource.read` 或 `externalResource.write`。對於需要這項權限的作業，系統允許存取 perimeter 外部的資源。
* `externalResources`：列出 perimeter 內部的用戶端可存取的外部資源。請將 EXTERNAL\_RESOURCE\_PATH 替換為有效的 Amazon S3 值區 (例如 `s3://bucket_name`)，或 Blob 儲存體容器路徑 (例如 `azure://myaccount.blob.core.windows.net/container_name`)。
* `egressFrom`：列出 perimeter 內指定專案中 Google Cloud資源允許的服務作業。
* `identityType` 或 `identities`：定義可存取 perimeter 外部指定資源的身分類型。將 IDENTITY\_TYPE 替換為下列其中一個有效值：

  + `ANY_IDENTITY`：允許所有身分。
  + `ANY_USER_ACCOUNT`：允許所有使用者。
  + `ANY_SERVICE_ACCOUNT`：允許所有服務帳戶
* `identities`：列出可存取 perimeter 外部指定資源的服務帳戶。
* `serviceAccount` (選用)：將 SERVICE\_ACCOUNT 替換為可存取 perimeter 外部指定資源的服務帳戶。

#### 範例

以下範例政策允許從 perimeter 內部向 AWS 中的 `s3://mybucket` Amazon S3 位置執行輸出作業。

```
- egressTo:
    operations:
    - serviceName: bigquery.googleapis.com
      methodSelectors:
      - method: "*"
    externalResources:
      - s3://mybucket
      - s3://mybucket2
  egressFrom:
    identityType: ANY_IDENTITY
```

以下範例允許對 Blob 儲存體容器執行輸出作業：

```
- egressTo:
    operations:
    - serviceName: bigquery.googleapis.com
      methodSelectors:
      - method: "*"
    externalResources:
      - azure://myaccount.blob.core.windows.net/mycontainer
  egressFrom:
    identityType: ANY_IDENTITY
```

如要進一步瞭解輸出政策，請參閱「[輸出規則參考資料](https://docs.cloud.google.com/vpc-service-controls/docs/ingress-egress-rules?hl=zh-tw#egress-rules-reference)」。

#### 新增輸出政策

如要在建立新服務範圍時新增輸出政策，請使用 [`gcloud access-context-manager perimeters create` 指令](https://docs.cloud.google.com/sdk/gcloud/reference/access-context-manager/perimeters/create?hl=zh-tw)。舉例來說，下列指令會建立名為 `omniPerimeter` 的新 perimeter，其中包含專案編號為 `12345` 的專案、限制 BigQuery API，並新增 `egress.yaml` 檔案中定義的輸出政策：

```
gcloud access-context-manager perimeters create omniPerimeter \
    --title="Omni Perimeter" \
    --resources=projects/12345 \
    --restricted-services=bigquery.googleapis.com \
    --egress-policies=egress.yaml
```

如要將輸出政策新增至現有服務範圍，請使用 [`gcloud access-context-manager perimeters update` 指令](https://docs.cloud.google.com/sdk/gcloud/reference/access-context-manager/perimeters/update?hl=zh-tw)。舉例來說，下列指令會將 `egress.yaml` 檔案中定義的輸出政策，新增至名為 `omniPerimeter` 的現有 service perimeter：

```
gcloud access-context-manager perimeters update omniPerimeter
    --set-egress-policies=egress.yaml
```

### 驗證 perimeter

如要驗證範圍，請使用 [`gcloud access-context-manager perimeters describe` 指令](https://docs.cloud.google.com/sdk/gcloud/reference/access-context-manager/perimeters/describe?hl=zh-tw)：

```
gcloud access-context-manager perimeters describe PERIMETER_NAME
```

將 PERIMETER\_NAME 替換為 perimeter 名稱。

舉例來說，下列指令會說明 perimeter `omniPerimeter`：

```
gcloud access-context-manager perimeters describe omniPerimeter
```

詳情請參閱「[管理 service perimeter](https://docs.cloud.google.com/vpc-service-controls/docs/manage-service-perimeters?hl=zh-tw#list-and-describe)」。

## 允許 BigQuery Omni 虛擬私有雲存取 Blob 儲存體

BigQuery 管理員可以建立網路規則，授予 BigQuery Omni 存取 Blob 儲存體資源的權限。確保只有授權的 BigQuery Omni VPC 才能與 Blob 儲存體互動，進一步提升資料安全性。

### 為 BigQuery Omni VPC 套用網路規則

如要套用網路規則，請使用 Azure PowerShell 或 Terraform：

### Azure PowerShell

執行下列指令，將網路規則新增至儲存空間帳戶，並將擷取的 BigQuery Omni 子網路 ID 指定為 `VirtualNetworkResourceId`。

```
  Add-AzStorageAccountNetworkRule`
   -ResourceGroupName "RESOURCE_GROUP_NAME"`
   -Name "STORAGE_ACCOUNT_NAME"`
   -VirtualNetworkResourceId "SUBNET_ID1","SUBNET_ID2"
```

更改下列內容：

* `RESOURCE_GROUP_NAME`：資源群組名稱。
* `STORAGE_ACCOUNT_NAME`：儲存空間帳戶名稱。
* `SUBNET_ID1`,`SUBNET_ID1`：
  子網路 ID。您可以在本頁的表格中找到這項資訊。

### Terraform

在 Terraform 設定檔中新增下列內容：

```
  resource "azurerm_storage_account_network_rules" "example" {
    storage_account_name       = "STORAGE_ACCOUNT_NAME"
    resource_group_name        = "RESOURCE_GROUP_NAME"
    default_action             = "Allow"
    bypass                     = ["Logging", "Metrics", "AzureServices"]
    virtual_network_subnet_ids = ["SUBNET_ID1","SUBNET_ID2"]
  }
```

更改下列內容：

* `STORAGE_ACCOUNT_NAME`：儲存空間帳戶名稱。
* `RESOURCE_GROUP_NAME`：資源群組名稱。
* `SUBNET_ID1`,`SUBNET_ID1`：
  子網路 ID。您可以在本頁的表格中找到這項資訊。

### BigQuery Omni VPC 資源 ID

| **區域** | **子網路 ID** |
| --- | --- |
| azure-eastus2 | /subscriptions/95f30708-58d1-48ba-beac-d71870c3b2f5/resourceGroups/bqe-prod-eastus2-resource-group/providers/Microsoft.Network/virtualNetworks/bqe-prod-eastus2-network/subnets/azure-prod-eastus21-yurduaaaaa-private /subscriptions/95f30708-58d1-48ba-beac-d71870c3b2f5/resourceGroups/bqe-prod-eastus2-resource-group/providers/Microsoft.Network/virtualNetworks/bqe-prod-eastus2-network/subnets/azure-prod-eastus22-yurduaaaab-private |

## 限制

如要查看適用於 Amazon S3 和 Blob 儲存體的 BigLake 資料表限制完整清單，請參閱「[限制](https://docs.cloud.google.com/bigquery/docs/omni-introduction?hl=zh-tw#limitations)」。

## 後續步驟

* 瞭解 [BigQuery Omni](https://docs.cloud.google.com/bigquery/docs/omni-introduction?hl=zh-tw)。
* 瞭解 [BigLake 資料表](https://docs.cloud.google.com/bigquery/docs/biglake-intro?hl=zh-tw)。
* 瞭解如何[將查詢結果匯出至 Blob 儲存體](https://docs.cloud.google.com/bigquery/docs/omni-azure-export-results-to-azure-storage?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-14 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-14 (世界標準時間)。"],[],[]]