Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# Apache Iceberg 資料表

*由 BigQuery 管理的 Apache Iceberg 資料表* (舊稱「BigQuery 中的 Apache Iceberg 專用 BigLake 資料表」) 是在 Google Cloud上建構開放格式 lakehouse 的基礎。代管 Iceberg 資料表與標準 BigQuery 資料表一樣，提供全代管體驗，但資料會儲存在客戶擁有的儲存空間 bucket 中。受管理 Iceberg 資料表支援開放式 Apache Iceberg 資料表格式，可與單一資料副本上的開放原始碼和第三方運算引擎互通。

代管 Iceberg 資料表支援下列功能：

* 使用 GoogleSQL 資料操縱語言 (DML) 進行*資料表變異*。
* 透過 Spark、Dataflow 和其他引擎等連接器，使用 [BigQuery Storage Write API](https://docs.cloud.google.com/bigquery/docs/write-api?hl=zh-tw) *統一處理批次和高處理量串流*。
* *匯出 Apache Iceberg V2 快照，並在每個資料表變動時自動重新整理*，以便使用 Spark 等開放原始碼和第三方查詢引擎直接查詢。
* *結構定義演變*：可新增、捨棄及重新命名資料欄，以符合您的需求。您也可以使用這項功能[變更現有資料欄的資料類型](https://docs.cloud.google.com/bigquery/docs/managing-table-schemas?hl=zh-tw#change_a_columns_data_type)和[資料欄模式](https://docs.cloud.google.com/bigquery/docs/managing-table-schemas?hl=zh-tw#change_a_columns_mode)。
  詳情請參閱[類型轉換規則](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/conversion_rules?hl=zh-tw)。
* *自動儲存空間最佳化*，包括調整檔案大小、自動叢集、垃圾回收和中繼資料最佳化。
* [*時間旅行*](https://docs.cloud.google.com/bigquery/docs/time-travel?hl=zh-tw)：在 BigQuery 中存取歷來資料。
* [*資料欄層級安全防護*](https://docs.cloud.google.com/bigquery/docs/column-level-security-intro?hl=zh-tw)和[*資料遮蓋*](https://docs.cloud.google.com/bigquery/docs/column-data-masking-intro?hl=zh-tw)。
* [*多陳述式交易*](#use_multi-statement_transactions) (在預覽版中)。
* [*資料表分區*](#use_partitioning) (預先發布版)。
* [*在 Dataform 工作流程中建立資料表*](https://docs.cloud.google.com/dataform/docs/create-tables?hl=zh-tw#create-iceberg-table)。

## 架構

代管 Iceberg 資料表可將 BigQuery 資源管理功能，帶到您自有雲端 bucket 中的資料表，您可以在這些資料表上使用 BigQuery 和開放原始碼運算引擎，不必將資料移出您控管的 bucket。您必須先設定 Cloud Storage bucket，才能開始使用受管理 Iceberg 表格。

受管理 Iceberg 資料表會使用 [*Lakehouse 執行階段目錄*](https://docs.cloud.google.com/bigquery/docs/about-blms?hl=zh-tw)，做為所有 Apache Iceberg 資料的統一執行階段目錄。Lakehouse 執行階段目錄提供單一資料來源，可管理多個引擎的中繼資料，並支援引擎互通性。

使用 Apache Iceberg 資料表對儲存空間的影響如下：

* BigQuery 會根據寫入要求和背景儲存空間最佳化作業 (例如 DML 陳述式和串流)，在值區中建立新的資料檔案。
* 系統會自動壓縮及叢集處理 bucket 中的資料檔案。[時間旅行視窗](https://docs.cloud.google.com/bigquery/docs/time-travel?hl=zh-tw)過期後，資料檔案會遭到垃圾收集。不過，如果刪除資料表，相關聯的資料檔案就不會進行垃圾收集。詳情請參閱「[儲存空間最佳化](#storage_optimization)」。

建立 Apache Iceberg 資料表的方式與[建立 BigQuery 資料表](https://docs.cloud.google.com/bigquery/docs/tables?hl=zh-tw)類似。由於資料湖泊會在 Cloud Storage 中以開放格式儲存資料，因此您必須執行下列操作：

* 使用 `WITH CONNECTION` 指定[雲端資源連結](https://docs.cloud.google.com/bigquery/docs/create-cloud-resource-connection?hl=zh-tw)，設定 BigQuery 存取 Cloud Storage 的連線憑證。
* 使用 `file_format =
  PARQUET` 陳述式，將資料儲存的檔案格式指定為 `PARQUET`。
* 使用 `table_format = ICEBERG` 陳述式，將開放原始碼中繼資料表格式指定為 `ICEBERG`。

## 最佳做法

**警告：** 在 BigQuery 外部修改受管理 Iceberg 資料表的資料檔案，可能會導致查詢失敗或資料遺失。此外，如果刪除包含受管理 Iceberg 資料表的 Cloud Storage 值區，或是讓連線服務帳戶無法存取這些資料表，可能會導致資料遺失。為避免發生這種情況，請使用 BigQuery 更新或修改代管 Iceberg 資料表。

直接在 BigQuery 外部變更或新增儲存空間中的檔案，可能會導致資料遺失或發生無法復原的錯誤。下表說明可能的情況：

| **作業** | **後果** | **預防方法** |
| --- | --- | --- |
| 在 BigQuery 以外的位置，將新檔案新增至值區。 | **資料遺失：**BigQuery 不會追蹤在 BigQuery 外部新增的檔案或物件。背景垃圾回收程序會刪除未追蹤的檔案。 | 只能透過 BigQuery 新增資料。這樣 BigQuery 就能追蹤檔案，並防止檔案遭到垃圾收集。  為避免意外新增資料和資料遺失，我們也建議限制外部工具對含有代管 Iceberg 表格的 bucket 寫入資料。 |
| 在非空白前置字元中建立新的 Apache Iceberg 資料表。 | **資料遺失：**BigQuery 不會追蹤現有資料，因此這些檔案會視為未追蹤，並由背景垃圾回收程序刪除。 | 請只在空白前置字元中建立新的受管理 Iceberg 資料表。 |
| 修改或取代 Apache Iceberg 資料表資料檔案。 | **資料遺失：**如果外部修改或取代資料表，一致性檢查就會失敗，導致資料表無法讀取。針對資料表執行的查詢會失敗。  此時無法自行復原。如要尋求資料復原協助，請與[支援團隊](https://docs.cloud.google.com/bigquery/docs/getting-support?hl=zh-tw)聯絡。 | 只能透過 BigQuery 修改資料。這樣 BigQuery 就能追蹤檔案，並防止檔案遭到垃圾收集。  為避免意外新增資料和資料遺失，我們也建議限制外部工具對含有代管 Iceberg 表格的 bucket 寫入資料。 |
| 在相同或重疊的 URI 上建立兩個代管 Iceberg 資料表。 | **資料遺失：**BigQuery 不會橋接受管理 Iceberg 資料表的相同 URI 執行個體。每個資料表的背景垃圾回收程序都會將對向資料表的檔案視為未追蹤，並刪除這些檔案，導致資料遺失。 | 每個 Apache Iceberg 資料表都必須使用專屬 URI。 |

### Cloud Storage 值區設定最佳做法

Cloud Storage 儲存空間儲存桶的設定及其與 BigQuery 的連線，會直接影響受管理 Iceberg 資料表的效能、費用、資料完整性、安全性及管理。以下是設定這項功能的最佳做法：

* 選取名稱時，請務必清楚指出該值區僅適用於代管的 Iceberg 資料表。
* 選擇與 BigQuery 資料集位於相同區域的[單一區域 Cloud Storage 值區](https://docs.cloud.google.com/storage/docs/locations?hl=zh-tw#available-locations)。這項協調作業可避免資料移轉費用，進而提升效能並降低成本。
* 根據預設，Cloud Storage 會將資料儲存在 Standard Storage 儲存空間級別中，這類別可提供充足的效能。如要盡量降低資料儲存成本，可以啟用 [Autoclass](https://docs.cloud.google.com/storage/docs/autoclass?hl=zh-tw)，讓系統自動管理[儲存空間級別](https://docs.cloud.google.com/storage/docs/storage-classes?hl=zh-tw)轉換。自動調整級別功能會從 Standard Storage 開始，將未存取的物件移至存取頻率較低的級別，藉此降低儲存空間費用。再次讀取物件時，物件會移回 Standard 類別。
* 啟用[統一值區層級存取權](https://docs.cloud.google.com/storage/docs/uniform-bucket-level-access?hl=zh-tw)和[禁止公開存取](https://docs.cloud.google.com/storage/docs/public-access-prevention?hl=zh-tw)。
* 確認已將[必要角色](#required-roles)指派給正確的使用者和服務帳戶。
* 為避免 Cloud Storage bucket 中的 Apache Iceberg 資料遭到意外刪除或毀損，請限制貴機構中大多數使用者的寫入和刪除權限。如要這麼做，請設定[值區權限政策](https://docs.cloud.google.com/storage/docs/access-control/using-iam-permissions?hl=zh-tw)，並加入條件，拒絕所有使用者 (您指定的除外) 的 `PUT` 和 `DELETE` 要求。
* 套用[Google 代管](https://docs.cloud.google.com/storage/docs/encryption/default-keys?hl=zh-tw)或[客戶自行管理](https://docs.cloud.google.com/storage/docs/encryption/customer-managed-keys?hl=zh-tw)的加密金鑰，進一步保護私密資料。
* 啟用[稽核記錄](https://docs.cloud.google.com/storage/docs/audit-logging?hl=zh-tw#settings)，確保作業透明度、進行疑難排解，以及監控資料存取權。
* 保留預設的[虛刪除政策](https://docs.cloud.google.com/storage/docs/soft-delete?hl=zh-tw) (保留 7 天)，防止物件遭到意外刪除。不過，如果發現 Apache Iceberg 資料已遭刪除，請與[支援團隊](https://docs.cloud.google.com/bigquery/docs/getting-support?hl=zh-tw)聯絡，而非手動還原物件，因為 BigQuery 中繼資料不會追蹤在 BigQuery 外部新增或修改的物件。
* 系統會自動啟用適應性檔案大小、自動叢集和垃圾回收功能，協助您盡可能提高檔案效能和成本效益。
* 請避免使用下列 Cloud Storage 功能，因為這些功能不支援受管理 Iceberg 表格：

  + [階層式命名空間](https://docs.cloud.google.com/storage/docs/hns-overview?hl=zh-tw)
  + [物件存取控制清單 (ACL)](https://docs.cloud.google.com/storage/docs/access-control/lists?hl=zh-tw)
  + [客戶提供的加密金鑰](https://docs.cloud.google.com/storage/docs/encryption/customer-supplied-keys?hl=zh-tw)
  + [物件版本管理](https://docs.cloud.google.com/storage/docs/object-versioning?hl=zh-tw)
  + [物件鎖定](https://docs.cloud.google.com/storage/docs/using-object-lock?hl=zh-tw)
  + [bucket 鎖定功能](https://docs.cloud.google.com/storage/docs/bucket-lock?hl=zh-tw)
  + 使用 BigQuery API 或 bq CLI 還原已軟刪除的物件

如要實作這些最佳做法，請使用下列指令建立值區：

```
gcloud storage buckets create gs://BUCKET_NAME \
    --project=PROJECT_ID \
    --location=LOCATION \
    --enable-autoclass \
    --public-access-prevention \
    --uniform-bucket-level-access
```

更改下列內容：

* `BUCKET_NAME`：新 bucket 的名稱
* `PROJECT_ID`：專案 ID
* `LOCATION`：新值區的[位置](https://docs.cloud.google.com/storage/docs/locations?hl=zh-tw)

## Apache Iceberg 資料表工作流程

下列各節說明如何建立、載入、管理及查詢受管理資料表。

### 事前準備

建立及使用受管理 Iceberg 資料表前，請務必先[設定 Cloud 資源連結](https://docs.cloud.google.com/bigquery/docs/create-cloud-resource-connection?hl=zh-tw)至儲存空間值區。連線必須具備儲存空間 bucket 的寫入權限，如「[必要角色](#required-roles)」一節所述。如要進一步瞭解連線所需的角色和權限，請參閱「[管理連線](https://docs.cloud.google.com/bigquery/docs/working-with-connections?hl=zh-tw)」。

### 必要的角色

如要取得讓 BigQuery 管理專案中資料表所需的權限，請要求管理員授予您下列 IAM 角色：

* 如要建立代管 Iceberg 資料表，請按照下列步驟操作：
  + 專案的 [BigQuery 資料擁有者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.dataOwner)  (`roles/bigquery.dataOwner`)
  + 專案的 [BigQuery 連線管理員](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.connectionAdmin)  (`roles/bigquery.connectionAdmin`)
* 如要查詢代管的 Iceberg 資料表：
  + [BigQuery 資料檢視者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.dataViewer)  (`roles/bigquery.dataViewer`)
    專案
  + [BigQuery 使用者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.user)  (`roles/bigquery.user`)
    專案
* 將下列角色授予連線服務帳戶，以便讀取及寫入 Cloud Storage 中的資料：
  + [Storage 物件使用者](https://docs.cloud.google.com/iam/docs/roles-permissions/storage?hl=zh-tw#storage.objectUser)  (`roles/storage.objectUser`)
    (值區)
  + 值區的「Storage 舊版值區讀取者」 (`roles/storage.legacyBucketReader`)

如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

這些預先定義的角色具備讓 BigQuery 管理專案中資料表所需的權限。如要查看確切的必要權限，請展開「Required permissions」(必要權限) 部分：

#### 所需權限

如要讓 BigQuery 管理專案中的資料表，您必須具備下列權限：

* 全部：
  + 專案的  `bigquery.connections.delegate`
  + 專案的 `bigquery.jobs.create`
  + 專案的 `bigquery.readsessions.create`
  + 專案的 `bigquery.tables.create`
  + 專案的 `bigquery.tables.get`
  + 專案的  `bigquery.tables.getData`
  + `storage.buckets.get`
    在 bucket 上
  + `storage.objects.create`
    在 bucket 上
  + `storage.objects.delete`
    在 bucket 上
  + `storage.objects.get`
    在 bucket 上
  + `storage.objects.list`
    在 bucket 上

您或許還可透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)取得這些權限。

### 建立代管 Iceberg 資料表

如要建立 Apache Iceberg 資料表，請選取下列其中一種方法：

### SQL

```
CREATE TABLE [PROJECT_ID.]DATASET_ID.TABLE_NAME (
COLUMN DATA_TYPE[, ...]
)
CLUSTER BY CLUSTER_COLUMN_LIST
WITH CONNECTION {CONNECTION_NAME | DEFAULT}
OPTIONS (
file_format = 'PARQUET',
table_format = 'ICEBERG',
storage_uri = 'STORAGE_URI');
```

更改下列內容：

* PROJECT\_ID：包含資料集的專案。如果未定義，指令會採用預設專案。
* DATASET\_ID：現有資料集。
* TABLE\_NAME：您要建立的資料表名稱。
* DATA\_TYPE：資料欄所含資訊的資料類型。
* CLUSTER\_COLUMN\_LIST (選用)：以半形逗號分隔的清單，最多包含四個資料欄。必須是頂層的非重複資料欄。
* CONNECTION\_NAME：連線名稱。例如：`myproject.us.myconnection`。

如要使用[預設連線](https://docs.cloud.google.com/bigquery/docs/default-connections?hl=zh-tw)，請指定 `DEFAULT`，而不是包含 PROJECT\_ID.REGION.CONNECTION\_ID 的連線字串。

* STORAGE\_URI：完整合格的 [Cloud Storage URI](https://docs.cloud.google.com/bigquery/docs/batch-loading-data?hl=zh-tw#gcs-uri)。例如：`gs://mybucket/table`。

### bq

```
bq --project_id=PROJECT_ID mk \
    --table \
    --file_format=PARQUET \
    --table_format=ICEBERG \
    --connection_id=CONNECTION_NAME \
    --storage_uri=STORAGE_URI \
    --schema=COLUMN_NAME:DATA_TYPE[, ...] \
    --clustering_fields=CLUSTER_COLUMN_LIST \
    DATASET_ID.MANAGED_TABLE_NAME
```

更改下列內容：

* PROJECT\_ID：包含資料集的專案。如果未定義，指令會採用預設專案。
* CONNECTION\_NAME：連線名稱。例如：`myproject.us.myconnection`。
* STORAGE\_URI：完整合格的 [Cloud Storage URI](https://docs.cloud.google.com/bigquery/docs/batch-loading-data?hl=zh-tw#gcs-uri)。例如：`gs://mybucket/table`。
* COLUMN\_NAME：資料欄名稱。
* DATA\_TYPE：資料欄所含資訊的資料類型。
* CLUSTER\_COLUMN\_LIST (選用)：以半形逗號分隔的清單，最多包含四個資料欄。必須是頂層的非重複資料欄。
* DATASET\_ID：現有資料集的 ID。
* MANAGED\_TABLE\_NAME：您要建立的資料表名稱。

### API

使用已定義的[資料表資源](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables?hl=zh-tw)呼叫 [`tables.insert`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables/insert?hl=zh-tw) 方法，類似於下列範例：

```
{
"tableReference": {
  "tableId": "TABLE_NAME"
},
"biglakeConfiguration": {
  "connectionId": "CONNECTION_NAME",
  "fileFormat": "PARQUET",
  "tableFormat": "ICEBERG",
  "storageUri": "STORAGE_URI"
},
"schema": {
  "fields": [
    {
      "name": "COLUMN_NAME",
      "type": "DATA_TYPE"
    }
    [, ...]
  ]
}
}
```

更改下列內容：

* TABLE\_NAME：您要建立的資料表名稱。
* CONNECTION\_NAME：連線名稱。例如：`myproject.us.myconnection`。
* STORAGE\_URI：完整合格的 [Cloud Storage URI](https://docs.cloud.google.com/bigquery/docs/batch-loading-data?hl=zh-tw#gcs-uri)。您也可以使用[萬用字元](https://docs.cloud.google.com/bigquery/docs/batch-loading-data?hl=zh-tw#load-wildcards)。例如：`gs://mybucket/table`。
* COLUMN\_NAME：資料欄名稱。
* DATA\_TYPE：資料欄所含資訊的資料類型。

### 將資料匯入受管理 Iceberg 資料表

以下各節說明如何將各種資料表格式的資料匯入代管 Iceberg 資料表。

#### 從平面檔案標準載入資料

代管 Iceberg 資料表會使用 BigQuery 載入工作，將外部檔案載入代管 Iceberg 資料表。如果您有現有的 Apache Iceberg 表格，請按照 [`bq load` CLI 指南](https://docs.cloud.google.com/bigquery/docs/hive-partitioned-loads-gcs?hl=zh-tw#bq)或 [`LOAD` SQL 指南](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/other-statements?hl=zh-tw#load_a_file_that_is_externally_partitioned)載入外部資料。載入資料後，新的 Parquet 檔案會寫入 STORAGE\_URI`/data` 資料夾。

如果使用先前的操作說明，但沒有現有的 Apache Iceberg 資料表，系統會改為建立 BigQuery 資料表。

如需將批次資料載入受管理資料表的工具專屬範例，請參閱下列內容：

### SQL

```
LOAD DATA INTO MANAGED_TABLE_NAME
FROM FILES (
uris=['STORAGE_URI'],
format='FILE_FORMAT');
```

更改下列內容：

* MANAGED\_TABLE\_NAME：現有 Apache Iceberg 資料表的名稱。
* STORAGE\_URI：完整的 [Cloud Storage URI](https://docs.cloud.google.com/bigquery/docs/batch-loading-data?hl=zh-tw#gcs-uri)，或是以逗號分隔的 URI 清單。您也可以使用[萬用字元](https://docs.cloud.google.com/bigquery/docs/batch-loading-data?hl=zh-tw#load-wildcards)。例如：`gs://mybucket/table`。
* FILE\_FORMAT：來源資料表格式。如要瞭解支援的格式，請參閱[`load_option_list`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/load-statements?hl=zh-tw#load_option_list)的`format`列。

### bq

```
bq load \
  --source_format=FILE_FORMAT \
  MANAGED_TABLE \
  STORAGE_URI
```

更改下列內容：

* FILE\_FORMAT：來源資料表格式。如要瞭解支援的格式，請參閱 [`load_option_list`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/load-statements?hl=zh-tw#load_option_list) 的 `format` 列。
  + MANAGED\_TABLE\_NAME：現有 Apache Iceberg 資料表的名稱。
* STORAGE\_URI：完整的 [Cloud Storage URI](https://docs.cloud.google.com/bigquery/docs/batch-loading-data?hl=zh-tw#gcs-uri)，或是以逗號分隔的 URI 清單。您也可以使用[萬用字元](https://docs.cloud.google.com/bigquery/docs/batch-loading-data?hl=zh-tw#load-wildcards)。例如：`gs://mybucket/table`。

#### 從 Apache Hive 分區檔案標準載入

您可以使用標準 BigQuery 載入工作，將 Apache Hive 分割檔案載入 Managed Iceberg 資料表。詳情請參閱「[載入外部分區資料](https://docs.cloud.google.com/bigquery/docs/hive-partitioned-loads-gcs?hl=zh-tw)」。

#### 從 Pub/Sub 載入串流資料

您可以使用 [Pub/Sub BigQuery 訂閱項目](https://docs.cloud.google.com/pubsub/docs/subscription-properties?hl=zh-tw#bigquery)，將串流資料載入代管 Iceberg 資料表。

### 從受管理 Iceberg 資料表匯出資料

以下各節說明如何將受管理 Iceberg 資料表中的資料匯出為各種資料表格式。

#### 將資料匯出為平面格式

如要將 Apache Iceberg 資料表匯出為平面格式，請使用 [`EXPORT DATA` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/other-statements?hl=zh-tw#export_data_statement)，並選取目的地格式。詳情請參閱[匯出資料](https://docs.cloud.google.com/bigquery/docs/exporting-data?hl=zh-tw#sql)。

### 建立 Apache Iceberg 資料表的中繼資料快照

如要建立 Apache Iceberg 資料表的中繼資料快照，請按照下列步驟操作：

1. 使用 [`EXPORT TABLE
   METADATA`](https://docs.cloud.google.com/bigquery/docs/exporting-data?hl=zh-tw#export_table_metadata) SQL 陳述式，將中繼資料匯出為 Apache Iceberg V2 格式。
2. 選用：排定 Apache Iceberg 中繼資料快照重新整理作業。如要根據設定的時間間隔重新整理 Apache Iceberg 中繼資料快照，請使用[排程查詢](https://docs.cloud.google.com/bigquery/docs/scheduling-queries?hl=zh-tw)。
3. 選用：為專案啟用中繼資料自動重新整理功能，在每次資料表變動時，自動更新 Apache Iceberg 資料表的中繼資料快照。如要啟用中繼資料自動重新整理功能，請來信至 [bigquery-tables-for-apache-iceberg-help@google.com](mailto:bigquery-tables-for-apache-iceberg-help@google.com)。每次重新整理作業都會產生[`EXPORT METADATA`費用](#queries_and_jobs)。

下列範例使用 DDL 陳述式 `EXPORT TABLE METADATA FROM
mydataset.test`，建立名為 `My Scheduled Snapshot
Refresh Query` 的排程查詢。DDL 陳述式每 24 小時執行一次。

```
bq query \
    --use_legacy_sql=false \
    --display_name='My Scheduled Snapshot Refresh Query' \
    --schedule='every 24 hours' \
    'EXPORT TABLE METADATA FROM mydataset.test'
```

### 查看 Apache Iceberg 資料表的中繼資料快照

重新整理 Apache Iceberg 資料表的中繼資料快照後，您可以在原始建立 Apache Iceberg 資料表的 [Cloud Storage URI](https://docs.cloud.google.com/bigquery/docs/batch-loading-data?hl=zh-tw#gcs-uri) 中找到快照。`/data` 資料夾包含 Parquet 檔案資料分片，`/metadata` 資料夾則包含 Apache Iceberg 資料表的中繼資料快照。

```
SELECT
  table_name,
  REGEXP_EXTRACT(ddl, r"storage_uri\s*=\s*\"([^\"]+)\"") AS storage_uri
FROM
  `mydataset`.INFORMATION_SCHEMA.TABLES;
```

請注意，`mydataset` 和 `table_name` 是實際資料集和資料表的預留位置。

### 使用 Spark 讀取代管 Iceberg 資料表

下列範例會設定環境，以便搭配使用 Spark SQL 和 Spark，然後執行查詢，從指定的 Apache Iceberg 資料表擷取資料。

```
spark-sql \
  --packages org.apache.iceberg:iceberg-spark-runtime-ICEBERG_VERSION_NUMBER \
  --conf spark.sql.catalog.CATALOG_NAME=org.apache.iceberg.spark.SparkCatalog \
  --conf spark.sql.catalog.CATALOG_NAME.type=hadoop \
  --conf spark.sql.catalog.CATALOG_NAME.warehouse='BUCKET_PATH' \

# Query the table
SELECT * FROM CATALOG_NAME.FOLDER_NAME;
```

更改下列內容：

* ICEBERG\_VERSION\_NUMBER：目前版本的 Apache Iceberg Spark 執行階段。從 [Apache Iceberg 版本](https://iceberg.apache.org/releases/)下載最新版本。
* CATALOG\_NAME：用於參照 Apache Iceberg 資料表的目錄。
* BUCKET\_PATH：包含資料表檔案的 bucket 路徑。
  例如：`gs://mybucket/`。
* FOLDER\_NAME：包含資料表檔案的資料夾。例如：`myfolder`。

### 修改代管的 Iceberg 資料表

如要修改 Apache Iceberg 資料表，請按照「[修改資料表結構定義](https://docs.cloud.google.com/bigquery/docs/managing-table-schemas?hl=zh-tw)」一文中的步驟操作。

### 使用多陳述式交易

**預覽**

這項產品或功能適用《[服務專屬條款](https://docs.cloud.google.com/terms/service-terms?hl=zh-tw#1)》中「一般服務條款」一節的《正式發布前產品條款》。正式發布前的產品和功能是按照「原樣」提供，支援範圍可能有限。
詳情請參閱[推出階段說明](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages)。

**注意：** 如要提供意見回饋或提出與這項預先發布版功能相關的問題，請傳送電子郵件至 [biglake-help@google.com](mailto:biglake-help@google.com)。

如要存取代管型 Iceberg 資料表的多陳述式交易，請填寫[註冊表單](https://docs.google.com/forms/d/1lQMsrT_jj_bi_aJbcb65dOc8LJTf0Wjb9AZs9EQXkCg?hl=zh-tw)。

### 使用分區

**預覽**

這項產品或功能適用《[服務專屬條款](https://docs.cloud.google.com/terms/service-terms?hl=zh-tw#1)》中「一般服務條款」一節的《正式發布前產品條款》。正式發布前的產品和功能是按照「原樣」提供，支援範圍可能有限。
詳情請參閱[推出階段說明](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages)。

**注意：** 如要提供意見回饋或提出與這項預先發布版功能相關的問題，請傳送電子郵件至 [biglake-help@google.com](mailto:biglake-help@google.com)。

如要存取 Apache Iceberg 資料表的[分區](https://docs.cloud.google.com/bigquery/docs/partitioned-tables?hl=zh-tw)功能，請填寫[申請表單](https://forms.gle/AJTG3idhjZ6RLLV98)。

您可以指定分區資料欄來區隔資料表，藉此將資料表分區。系統支援下列受管理 Iceberg 資料表的欄類型：

* `DATE`
* `DATETIME`
* `TIMESTAMP`

依據 `DATE`、`DATETIME` 或 `TIMESTAMP` 資料欄分區的資料表稱為[時間單位資料欄分區](https://docs.cloud.google.com/bigquery/docs/partitioned-tables?hl=zh-tw#date_timestamp_partitioned_tables)。您可以選擇分區的[時間間隔為小時、日、月或年](https://docs.cloud.google.com/bigquery/docs/partitioned-tables?hl=zh-tw#select_daily_hourly_monthly_or_yearly_partitioning)。

代管 Iceberg 資料表也支援[叢集](https://docs.cloud.google.com/bigquery/docs/clustered-tables?hl=zh-tw)，以及[合併叢集和分區資料表](https://docs.cloud.google.com/bigquery/docs/clustered-tables?hl=zh-tw#combine-clustered-partitioned-tables)。

#### 分區限制

* 適用所有 [BigQuery 分區資料表限制](https://docs.cloud.google.com/bigquery/docs/partitioned-tables?hl=zh-tw#limitations)。
* 不支援 `DATE`、`DATETIME` 或 `TIMESTAMP` 以外的分區資料欄類型。
* 不支援分區到期。
* 不支援[分區演進](https://iceberg.apache.org/docs/1.5.1/evolution/#partition-evolution)。

#### 建立分區 Apache Iceberg 資料表

如要建立已分割的 Apache Iceberg 資料表，請按照[建立標準 Apache Iceberg 資料表](#create-iceberg-tables)的指示操作，並根據您的環境加入下列其中一項：

* [`PARTITION BY` 子句](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#partition_expression)
* [`--time_partitioning_field` 和 `--time_partitioning_type` 標記](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#mk-table)
* [`timePartitioning` 屬性](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables?hl=zh-tw#timepartitioning)

#### 修改及查詢分區代管 Iceberg 資料表

分區代管 Iceberg 資料表的 BigQuery 資料操縱語言 (DML) 陳述式和查詢，與標準 Apache Iceberg 資料表相同。BigQuery 會自動將工作範圍限定在正確的分區，類似於 [Apache Iceberg 隱藏式分區](https://iceberg.apache.org/docs/latest/partitioning/#icebergs-hidden-partitioning)。此外，您新增至資料表的任何新資料都會自動進行分割。

您也可以使用其他引擎查詢分區代管 Iceberg 資料表，方式與標準代管 Iceberg 資料表相同。建議[啟用中繼資料快照](https://docs.cloud.google.com/bigquery/docs/iceberg-tables?hl=zh-tw#create-iceberg-table-snapshots)，以獲得最佳體驗。

為提升安全性，受管理 Iceberg 資料表的分區資訊會與資料路徑分離，並完全由中繼資料層管理。

## 定價

Apache Iceberg 資料表定價包括儲存空間、儲存空間最佳化，以及查詢和工作。

### 儲存空間

代管 Iceberg 資料表會將所有資料儲存在 [Cloud Storage](https://docs.cloud.google.com/storage?hl=zh-tw)。系統會針對所有儲存的資料收費，包括歷史資料表資料。您可能也需要支付 Cloud Storage [資料處理](https://cloud.google.com/storage/pricing?hl=zh-tw#process-pricing)和[移轉費用](https://cloud.google.com/storage/pricing?hl=zh-tw#network-buckets)。透過 BigQuery 或 BigQuery Storage API 處理的作業，可能免除部分 Cloud Storage 作業費用。不會收取 BigQuery 專屬的儲存費用。詳情請參閱 [Cloud Storage 定價](https://cloud.google.com/storage/pricing?hl=zh-tw)。

### 儲存空間最佳化

代管 Iceberg 資料表會自動管理資料表，包括壓縮、分群、垃圾回收，以及產生/重新整理 BigQuery 中繼資料，以提升查詢效能並降低儲存空間成本。資料表管理功能的運算資源用量會以資料運算單元 (DCU) 為單位，按秒累加計費。詳情請參閱「[Apache Iceberg 資料表定價](https://cloud.google.com/products/biglake/pricing?hl=zh-tw)」。

透過 Storage Write API 串流資料時進行的資料匯出作業，會計入 Storage Write API 價格，不會以背景維護作業計費。詳情請參閱「[資料擷取定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#data_ingestion_pricing)」。

如要查看這些背景作業的記錄和運算用量，請查詢 [`INFORMATION_SCHEMA.JOBS`](https://docs.cloud.google.com/bigquery/docs/information-schema-jobs?hl=zh-tw) 檢視畫面。如需查詢範例，請參閱下列內容：

* [儲存空間最佳化工作](https://docs.cloud.google.com/bigquery/docs/information-schema-jobs?hl=zh-tw#get-iceberg-storage-optimization-jobs)
* [`EXPORT TABLE METADATA` 項工作](https://docs.cloud.google.com/bigquery/docs/information-schema-jobs?hl=zh-tw#get-iceberg-export-table-metadata-jobs)

### 查詢和工作

與 BigQuery 資料表類似，如果您使用 [BigQuery 隨選定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#on_demand_pricing)，系統會根據查詢和讀取的位元組 (每 TiB) 收費；如果您使用 [BigQuery 容量運算定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#capacity_compute_analysis_pricing)，系統會根據運算單元消耗量 (每運算單元時數) 收費。

BigQuery 定價也適用於 [BigQuery Storage Read API](https://cloud.google.com/bigquery/pricing?hl=zh-tw#data_extraction_pricing) 和 [Storage Write API](https://cloud.google.com/bigquery/pricing?hl=zh-tw#data_ingestion_pricing)。

載入和匯出作業 (例如 `EXPORT METADATA`) 會使用 [Enterprise 版隨用隨付方案的配額](https://cloud.google.com/bigquery/pricing?hl=zh-tw#enterprise-edition-slots)。這與 BigQuery 資料表不同，因為這些作業不會產生費用。如果 `PIPELINE` 保留項目提供 Enterprise 或 Enterprise Plus 配額，載入和匯出作業會優先使用這些保留項目配額。

## 限制

代管 Iceberg 資料表有下列限制：

* 代管 Iceberg 資料表不支援[重新命名作業](https://docs.cloud.google.com/bigquery/docs/managing-tables?hl=zh-tw#renaming-table)或 [`ALTER TABLE
  RENAME TO` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#alter_table_rename_to_statement)。
  + 受管理 Iceberg 資料表不支援[資料表副本](https://docs.cloud.google.com/bigquery/docs/managing-tables?hl=zh-tw#copy-table)或 [`CREATE TABLE
    COPY` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#create_table_copy)。
    - 代管 Iceberg 資料表不支援[資料表複製](https://docs.cloud.google.com/bigquery/docs/table-clones-intro?hl=zh-tw)或 [`CREATE TABLE CLONE` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#create_table_clone_statement)。
      * 受管理 Iceberg 資料表不支援[資料表快照](https://docs.cloud.google.com/bigquery/docs/table-snapshots-intro?hl=zh-tw)或 [`CREATE
        SNAPSHOT TABLE` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#create_snapshot_table_statement)。
        + 受管理 Iceberg 資料表不支援下列資料表結構定義：
* 結構定義空白
  + 結構定義包含 `BIGNUMERIC`、`INTERVAL`、`JSON`、`RANGE` 或 `GEOGRAPHY` 資料類型。
  + 具有[欄位對照](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#collatable_data_types)的結構定義。
    - 結構定義，其中包含[預設值
      運算式](https://docs.cloud.google.com/bigquery/docs/default-values?hl=zh-tw)。
* 受管理 Iceberg 資料表不支援下列結構定義演變情況：
  + `NUMERIC`至 `FLOAT` 型別強制轉換
  + `INT`至 `FLOAT` 型別強制轉換
  + 使用 SQL DDL 陳述式，在現有的 `RECORD` 資料欄中新增巢狀欄位
* 透過控制台或 API 查詢時，受管理 Iceberg 資料表會顯示 0 位元組的儲存空間大小。
* 代管 Iceberg 資料表不支援[具體化檢視區塊](https://docs.cloud.google.com/bigquery/docs/materialized-views-intro?hl=zh-tw)。
* 受管理 Iceberg 資料表不支援[授權檢視區塊](https://docs.cloud.google.com/bigquery/docs/authorized-views?hl=zh-tw)，但支援[資料欄層級存取權控管](https://docs.cloud.google.com/bigquery/docs/column-level-security-intro?hl=zh-tw)。
* 受管理 Iceberg 資料表不支援[變更資料擷取 (CDC)](https://docs.cloud.google.com/bigquery/docs/change-data-capture?hl=zh-tw) 更新。
* 代管 Iceberg 資料表不支援[代管災難復原](https://docs.cloud.google.com/bigquery/docs/managed-disaster-recovery?hl=zh-tw)
* 代管 Iceberg 資料表不支援[資料列層級安全防護機制](https://docs.cloud.google.com/bigquery/docs/row-level-security-intro?hl=zh-tw)。
* 代管 Iceberg 資料表不支援[安全防護期](https://docs.cloud.google.com/bigquery/docs/time-travel?hl=zh-tw#fail-safe)。
* 代管 Iceberg 資料表不支援擷取工作。
* `INFORMATION_SCHEMA.TABLE_STORAGE` 檢視畫面不包含 Apache Iceberg 資料表。
* 系統不支援將代管 Iceberg 資料表做為查詢結果目的地。您可以改用 [`CREATE
  TABLE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#create_table_statement) 陳述式搭配 `AS query_statement` 引數，將資料表建立為查詢結果目的地。
* `CREATE OR REPLACE` 不支援以 Apache Iceberg 資料表取代標準資料表，也不支援以標準資料表取代代管的 Iceberg 資料表。
* [批次載入](https://docs.cloud.google.com/bigquery/docs/batch-loading-data?hl=zh-tw)和 [`LOAD DATA` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/load-statements?hl=zh-tw)僅支援將資料附加至現有的代管 Iceberg 資料表。
* [批次載入](https://docs.cloud.google.com/bigquery/docs/batch-loading-data?hl=zh-tw)和 [`LOAD
  DATA` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/load-statements?hl=zh-tw)不支援結構定義更新。
* `TRUNCATE TABLE` 不支援代管 Iceberg 資料表。您可以採用以下兩種替代方式：
  + [`CREATE OR REPLACE
    TABLE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#create_table_statement)，並使用相同的資料表建立選項。
  + `DELETE FROM` table `WHERE` true
* [`APPENDS` 資料表值函式 (TVF)](https://docs.cloud.google.com/bigquery/docs/change-history?hl=zh-tw) 不支援代管 Iceberg 資料表。
* Apache Iceberg 中繼資料可能不包含過去 90 分鐘內，透過 Storage Write API 串流至 BigQuery 的資料。
* 使用 `tabledata.list` 依記錄分頁存取資料時，不支援 Apache Iceberg 資料表。
* 每個 Apache Iceberg 資料表只能執行一個並行的變動 DML 陳述式 (`UPDATE`、`DELETE` 和 `MERGE`)。其他變動 DML 陳述式會排入佇列。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-05 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-05 (世界標準時間)。"],[],[]]