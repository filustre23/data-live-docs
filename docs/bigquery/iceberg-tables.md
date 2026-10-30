Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# Apache Iceberg 代管資料表

BigQuery 中的 Apache Iceberg 代管資料表可讓您在 Google Cloud上建構開放格式的湖倉。這類資料表提供與標準 BigQuery 資料表相同的全代管體驗，但資料會儲存在您擁有的儲存空間 bucket。

Iceberg 代管資料表採用開放式 Iceberg 資料表格式，因此開放原始碼和第三方運算引擎可使用單一資料副本。

## 功能與特色

Iceberg 代管資料表支援下列功能：

* 使用 GoogleSQL data manipulation language (DML) *變動資料表*。
* 透過 Spark、Dataflow 和其他引擎等連接器，使用 [BigQuery Storage Write API (gRPC)](https://docs.cloud.google.com/bigquery/docs/write-api?hl=zh-tw) *整合批次和高處理量串流*。
* *匯出 Iceberg V2 快照，並在每次資料表變更時自動重新整理*，以便使用 Spark 等開放原始碼和第三方查詢引擎直接查詢。
* *結構定義演變*：可依需求新增、刪除及重新命名資料欄。這項功能也可讓您變更現有資料欄的[資料類型](https://docs.cloud.google.com/bigquery/docs/managing-table-schemas?hl=zh-tw#change_a_columns_data_type)和[模式](https://docs.cloud.google.com/bigquery/docs/managing-table-schemas?hl=zh-tw#change_a_columns_mode)。詳情請參閱「[轉換規則](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/conversion_rules?hl=zh-tw)」。
* *自動儲存空間最佳化*，包括自動調整檔案大小、自動分群、垃圾回收和中繼資料最佳化。
* [*時間旅行*](https://docs.cloud.google.com/bigquery/docs/time-travel?hl=zh-tw)：在 BigQuery 中存取歷來資料。
* [*資料欄層級安全防護機制*](https://docs.cloud.google.com/bigquery/docs/column-level-security-intro?hl=zh-tw)、[*資料列層級安全防護機制*](https://docs.cloud.google.com/bigquery/docs/row-level-security-intro?hl=zh-tw)和[*資料遮蓋*](https://docs.cloud.google.com/bigquery/docs/column-data-masking-intro?hl=zh-tw)。
* [*多陳述式交易*](#use_multi-statement_transactions)。
* [*資料表分區*](#use_partitioning)。
* [*在 Dataform 工作流程中建立資料表*](https://docs.cloud.google.com/dataform/docs/create-tables?hl=zh-tw#create-iceberg-table)。
* [*BigQuery 進階執行階段*](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#advanced-runtime)。
* 使用 [*BigQuery Storage Write API (gRPC)*](https://docs.cloud.google.com/bigquery/docs/write-api-grpc?hl=zh-tw) 串流。

## 架構

Iceberg 代管資料表可讓您在自己的雲端 bucket 中，輕鬆管理 BigQuery 資源。您可以在這些資料表上使用 BigQuery 和開放原始碼運算引擎，不必將資料移出您控管的 bucket。您必須先設定 Cloud Storage bucket，才能開始使用 Iceberg 代管資料表。

使用 Iceberg 代管資料表會對 bucket 造成下列影響：

* BigQuery 會在 bucket 中建立新的資料檔案，以回應寫入要求和背景儲存空間最佳化作業，例如 DML 陳述式和串流。
* 系統會對 bucket 中的資料檔案執行自動壓縮和分群。[時間旅行視窗](https://docs.cloud.google.com/bigquery/docs/time-travel?hl=zh-tw)到期後，資料檔案會進行垃圾收集。不過，如果資料表遭到刪除，系統不會對相關聯的資料檔案進行垃圾收集。詳情請參閱「[儲存空間最佳化](#storage_optimization)」。

建立 Iceberg 代管資料表的方式與[建立 BigQuery 資料表](https://docs.cloud.google.com/bigquery/docs/tables?hl=zh-tw)類似。由於資料是以開放格式儲存在 Cloud Storage，因此您必須執行下列操作：

* 指定 [Cloud 資源連結](https://docs.cloud.google.com/bigquery/docs/create-cloud-resource-connection?hl=zh-tw)，並使用 `WITH CONNECTION` 設定 BigQuery 存取 Cloud Storage 的連線憑證。
* 使用 `file_format =
  PARQUET` 陳述式，將資料儲存庫的檔案格式指定為 `PARQUET`。
* 使用 `table_format = ICEBERG` 陳述式，將開放原始碼中繼資料資料表格式指定為 `ICEBERG`。

## 最佳做法

**警告：** 在 BigQuery 外部修改 Iceberg 代管資料表的資料檔案，可能會導致查詢失敗或資料遺失。此外，如果刪除含有 Iceberg 代管資料表的 Cloud Storage bucket，或讓連線服務帳戶無法存取這些資料表，可能會導致資料遺失。為避免這種情況，請使用 BigQuery 更新或修改 Iceberg 代管資料表。

直接在 BigQuery 以外的地方變更或新增檔案至 bucket，可能會導致資料遺失或發生無法復原的錯誤。下表說明可能的情況：

| **作業** | **後果** | **預防** |
| --- | --- | --- |
| 在 BigQuery 外部，將新檔案新增至 bucket。 | **資料遺失：**BigQuery 不會追蹤在 BigQuery 外部新增的檔案或物件。未追蹤的檔案會由背景垃圾收集程序刪除。 | 只能透過 BigQuery 新增資料。這樣一來，BigQuery 就能追蹤檔案，並防止檔案遭到垃圾收集。  為避免意外新增和資料遺失，建議您限制外部工具對含有 Iceberg 代管資料表的 bucket 寫入權限。 |
| 在非空白前置字元中建立新的 Iceberg 代管資料表。 | **資料遺失：**BigQuery 不會追蹤現有資料，因此這些檔案會視為未追蹤，並由背景垃圾收集程序刪除。 | 請只在空白前置字串中建立新的 Iceberg 代管資料表。 |
| 修改或取代 Iceberg 代管資料表的資料檔案。 | **資料遺失：**如果外部修改或替換，資料表會無法通過一致性檢查，且無法讀取。對資料表執行的查詢會失敗。  您無法自行復原。請聯絡[支援團隊](https://docs.cloud.google.com/bigquery/docs/getting-support?hl=zh-tw)，取得資料復原協助。 | 只能透過 BigQuery 修改資料。這樣一來，BigQuery 就能追蹤檔案，並防止檔案遭到垃圾收集。  為避免意外新增和資料遺失，建議您限制外部工具對含有 Iceberg 代管資料表的 bucket 寫入權限。 |
| 在相同或重疊的 URI 上建立兩個 Iceberg 代管資料表。 | **資料遺失：**BigQuery 不會橋接 Iceberg 代管資料表的相同 URI 執行個體。每個資料表的背景垃圾收集程序會將對應資料表的檔案視為未追蹤，並將其刪除，導致資料遺失。 | 為每個 Iceberg 代管資料表使用專屬 URI。 |

### Cloud Storage bucket 設定最佳做法

Cloud Storage bucket 的設定及其與 BigQuery 的連線，會直接影響 Iceberg 代管資料表的效能、成本、資料完整性、安全性和控管。以下是這項設定的最佳做法：

* 請選取能清楚指出 bucket 僅用於 Iceberg 代管資料表的名稱。
* 選擇與 BigQuery 資料集位於相同區域的[單一區域 Cloud Storage bucket](https://docs.cloud.google.com/storage/docs/locations?hl=zh-tw#available-locations)。這種協調方式可避免資料移轉費用，進而提升效能並降低成本。
* 根據預設，Cloud Storage 會將資料儲存在 Standard Storage 儲存空間級別，提供足夠的效能。如要盡可能降低資料儲存費用，可以啟用 [Autoclass](https://docs.cloud.google.com/storage/docs/autoclass?hl=zh-tw)，自動管理[儲存空間級別](https://docs.cloud.google.com/storage/docs/storage-classes?hl=zh-tw)轉換。Autoclass 會從 Standard Storage 儲存空間級別開始，將未存取的物件逐步移至較冷的級別，以降低儲存費用。再次讀取物件時，物件會移回 Standard 級別。
* 啟用[統一 bucket 層級存取權](https://docs.cloud.google.com/storage/docs/uniform-bucket-level-access?hl=zh-tw)和[禁止公開存取](https://docs.cloud.google.com/storage/docs/public-access-prevention?hl=zh-tw)。
* 確認[必要角色](#required-roles)已指派給正確的使用者和服務帳戶。
* 為避免 Cloud Storage bucket 中的資料意外刪除或損毀，請限制貴組織中多數使用者的寫入和刪除權限。方法是設定[值區權限政策](https://docs.cloud.google.com/storage/docs/access-control/using-iam-permissions?hl=zh-tw)，並加入條件，拒絕所有使用者的 `PUT` 和 `DELETE` 要求，但您指定的使用者除外。
* 套用 [Google 代管](https://docs.cloud.google.com/storage/docs/encryption/default-keys?hl=zh-tw)或[客戶自行管理](https://docs.cloud.google.com/storage/docs/encryption/customer-managed-keys?hl=zh-tw)的加密金鑰，進一步保護機密資料。
* 啟用[稽核記錄](https://docs.cloud.google.com/storage/docs/audit-logging?hl=zh-tw#settings)，確保作業透明度、排解問題及監控資料存取。
* 保留預設的[虛刪除政策](https://docs.cloud.google.com/storage/docs/soft-delete?hl=zh-tw) (保留 7 天)，防止意外刪除。不過，如果您發現資料遭到刪除，請與[支援團隊](https://docs.cloud.google.com/bigquery/docs/getting-support?hl=zh-tw)聯絡，不要手動還原物件，因為在 BigQuery 外部新增或修改的物件不會由 BigQuery 中繼資料追蹤。
* 系統會自動啟用自動調整檔案大小、自動分群和垃圾收集功能，協助您最佳化檔案效能和成本。
* 請避免使用下列 Cloud Storage 功能，因為 Iceberg 代管資料表不支援這些功能：

  + [物件存取控管清單 (ACL)](https://docs.cloud.google.com/storage/docs/access-control/lists?hl=zh-tw)
  + [客戶提供的加密金鑰](https://docs.cloud.google.com/storage/docs/encryption/customer-supplied-keys?hl=zh-tw)
  + [物件版本管理](https://docs.cloud.google.com/storage/docs/object-versioning?hl=zh-tw)
  + [物件鎖定](https://docs.cloud.google.com/storage/docs/using-object-lock?hl=zh-tw)
  + [bucket 鎖定](https://docs.cloud.google.com/storage/docs/bucket-lock?hl=zh-tw)
  + 使用 BigQuery API 或 bq CLI 還原虛刪除的物件

您可以使用下列指令建立 bucket，藉此實作這些最佳做法：

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
* `LOCATION`：新 bucket 的[位置](https://docs.cloud.google.com/storage/docs/locations?hl=zh-tw)

## Iceberg 代管資料表工作流程

以下各節說明如何建立、載入、管理及查詢 Iceberg 代管資料表。

### 事前準備

建立及使用 Iceberg 代管資料表前，請務必設定[Cloud 資源連結](https://docs.cloud.google.com/bigquery/docs/create-cloud-resource-connection?hl=zh-tw)，連至儲存空間 bucket。連線必須具備儲存空間 bucket 的寫入權限，如以下「[必要角色](#required-roles)」一節所述。如要進一步瞭解連線所需的角色和權限，請參閱「[管理連線](https://docs.cloud.google.com/bigquery/docs/working-with-connections?hl=zh-tw)」。

### 必要的角色

如要取得所需權限，讓 BigQuery 管理專案中的資料表，請要求管理員授予您下列 IAM 角色：

* 如要建立 Iceberg 代管資料表，請按照下列步驟操作：
  + 專案的 [BigQuery 資料擁有者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.dataOwner)  (`roles/bigquery.dataOwner`)
  + 專案的 [BigQuery 連線管理員](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.connectionAdmin)  (`roles/bigquery.connectionAdmin`)
* 如要查詢 Iceberg 代管資料表，請按照下列步驟操作：
  + 專案的 [BigQuery 資料檢視者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.dataViewer)  (`roles/bigquery.dataViewer`)
  + 專案的 [BigQuery 使用者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.user)  (`roles/bigquery.user`)
* 將下列角色授予連線服務帳戶，以便讀取及寫入 Cloud Storage 中的資料：
  + 值區的 [Storage 物件使用者](https://docs.cloud.google.com/iam/docs/roles-permissions/storage?hl=zh-tw#storage.objectUser)  (`roles/storage.objectUser`)
  + 值區的 [Storage 舊版值區讀取者](https://docs.cloud.google.com/iam/docs/roles-permissions/storage?hl=zh-tw#storage.legacyBucketReader)  (`roles/storage.legacyBucketReader`)

如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

這些預先定義的角色具備所需權限，可讓 BigQuery 管理專案中的資料表。如要查看確切的必要權限，請展開「Required permissions」(必要權限) 部分：

#### 所需權限

必須具備下列權限，BigQuery 才能管理專案中的資料表：

* 全部：
  + 專案的 `bigquery.connections.delegate`
  + 專案的 `bigquery.jobs.create`
  + 專案的 `bigquery.readsessions.create`
  + 專案的 `bigquery.tables.create`
  + 專案的 `bigquery.tables.get`
  + 專案的 `bigquery.tables.getData`
  + bucket 上的 `storage.buckets.get`
  + bucket 上的 `storage.objects.create`
  + bucket 上的 `storage.objects.delete`
  + bucket 上的 `storage.objects.get`
  + bucket 上的 `storage.objects.list`

您或許還可透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)取得這些權限。

### 建立 Iceberg 代管資料表

如要建立 Iceberg 代管資料表，請選取下列其中一種方法：

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

* PROJECT\_ID：包含資料集的專案。如未定義，指令會假設使用預設專案。
* DATASET\_ID：現有資料集。
* TABLE\_NAME：要建立的資料表名稱。
* DATA\_TYPE：資料欄所含資訊的資料類型。
* CLUSTER\_COLUMN\_LIST (選用)：以半形逗號分隔的清單，最多可包含四個資料欄。必須是頂層、非重複的資料欄。
* CONNECTION\_NAME：連線名稱。例如：`myproject.us.myconnection`。如要使用[預設連線](https://docs.cloud.google.com/bigquery/docs/default-connections?hl=zh-tw)，請指定 `DEFAULT`，而非連線名稱。
* STORAGE\_URI：完整的 [Cloud Storage URI](https://docs.cloud.google.com/bigquery/docs/batch-loading-data?hl=zh-tw#gcs-uri)。例如：`gs://mybucket/table`。

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

* PROJECT\_ID：包含資料集的專案。如未定義，指令會假設使用預設專案。
* CONNECTION\_NAME：連線名稱。例如：`myproject.us.myconnection`。
* STORAGE\_URI：完整的 [Cloud Storage URI](https://docs.cloud.google.com/bigquery/docs/batch-loading-data?hl=zh-tw#gcs-uri)。例如：`gs://mybucket/table`。
* COLUMN\_NAME：資料欄名稱。
* DATA\_TYPE：資料欄所含資訊的資料類型。
* CLUSTER\_COLUMN\_LIST (選用)：以半形逗號分隔的清單，最多可包含四個資料欄。必須是頂層、非重複的資料欄。
* DATASET\_ID：現有資料集的 ID。
* MANAGED\_TABLE\_NAME：要建立的資料表名稱。

### API

使用定義的[資料表資源](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables?hl=zh-tw)呼叫 [`tables.insert`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables/insert?hl=zh-tw) 方法，如下所示：

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

* TABLE\_NAME：要建立的資料表名稱。
* CONNECTION\_NAME：連線名稱。例如：`myproject.us.myconnection`。
* STORAGE\_URI：完整的 [Cloud Storage URI](https://docs.cloud.google.com/bigquery/docs/batch-loading-data?hl=zh-tw#gcs-uri)。也支援[萬用字元](https://docs.cloud.google.com/bigquery/docs/batch-loading-data?hl=zh-tw#load-wildcards)。例如：`gs://mybucket/table`。
* COLUMN\_NAME：資料欄名稱。
* DATA\_TYPE：資料欄所含資訊的資料類型。

### 將資料匯入 Iceberg 代管資料表

以下各節說明如何將各種資料表格式的資料，匯入 Iceberg 代管資料表。

#### 從平面檔載入標準資料

Iceberg 代管資料表會使用 BigQuery 載入工作，將外部檔案載入 Iceberg 代管資料表。如果您已有 Iceberg 代管資料表，請按照 [`bq load` CLI 指南](https://docs.cloud.google.com/bigquery/docs/hive-partitioned-loads-gcs?hl=zh-tw#bq)或 [`LOAD` SQL 指南](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/other-statements?hl=zh-tw#load_a_file_that_is_externally_partitioned)載入外部資料。載入資料後，新的 Parquet 檔案會寫入 STORAGE\_URI`/data` 資料夾。

如果按照上述操作說明執行，但沒有現成的 Iceberg 代管資料表，系統會改為建立 BigQuery 資料表。

請參閱下列範例，瞭解如何使用特定工具，將批次資料載入 Iceberg 代管資料表：

### SQL

```
LOAD DATA INTO MANAGED_TABLE_NAME
FROM FILES (
uris=['STORAGE_URI'],
format='FILE_FORMAT');
```

更改下列內容：

* MANAGED\_TABLE\_NAME：現有 Iceberg 代管資料表的名稱。
* STORAGE\_URI：完整 [Cloud Storage URI](https://docs.cloud.google.com/bigquery/docs/batch-loading-data?hl=zh-tw#gcs-uri)，或以半形逗號分隔的 URI 清單。也支援[萬用字元](https://docs.cloud.google.com/bigquery/docs/batch-loading-data?hl=zh-tw#load-wildcards)。例如：`gs://mybucket/table`。
* FILE\_FORMAT：來源資料表格式。如要瞭解支援的格式，請參閱 [`load_option_list`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/load-statements?hl=zh-tw#load_option_list) 的 `format` 列。

### bq

```
bq load \
  --source_format=FILE_FORMAT \
  MANAGED_TABLE \
  STORAGE_URI
```

更改下列內容：

* FILE\_FORMAT：來源資料表格式。如要瞭解支援的格式，請參閱 [`load_option_list`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/load-statements?hl=zh-tw#load_option_list) 的 `format` 列。
* MANAGED\_TABLE\_NAME：現有 Iceberg 代管資料表的名稱。
* STORAGE\_URI：完整 [Cloud Storage URI](https://docs.cloud.google.com/bigquery/docs/batch-loading-data?hl=zh-tw#gcs-uri)，或以半形逗號分隔的 URI 清單。也支援[萬用字元](https://docs.cloud.google.com/bigquery/docs/batch-loading-data?hl=zh-tw#load-wildcards)。例如：`gs://mybucket/table`。

#### 從 Apache Hive 分區檔案標準載入

您可以使用標準 BigQuery 載入工作，將 Hive 分區檔案載入 Iceberg 代管資料表。詳情請參閱「[載入外部分區資料](https://docs.cloud.google.com/bigquery/docs/hive-partitioned-loads-gcs?hl=zh-tw)」。

#### 從 Pub/Sub 載入串流資料

您可以使用 [Pub/Sub BigQuery 訂閱項目](https://docs.cloud.google.com/pubsub/docs/subscription-properties?hl=zh-tw#bigquery)，將串流資料載入 Iceberg 代管資料表。

#### 使用持續查詢載入串流資料

您可以使用 [BigQuery 持續查詢](https://docs.cloud.google.com/bigquery/docs/continuous-queries-introduction?hl=zh-tw)搭配 `INSERT` DML 陳述式，持續處理串流資料，並從 BigQuery 寫入 Iceberg 代管資料表。這樣一來，您就能在開放格式的湖倉中，即時執行反向 ETL、資料充實和篩選作業。

執行持續查詢前，請確認目標 Iceberg 代管資料表存在，且使用者或服務帳戶具備資料表、其 Google Cloud 資源連線和基礎 Cloud Storage bucket 的必要權限。

如需設定操作說明和 SQL 範例，請參閱「[將資料寫入 BigQuery 或 Apache Iceberg 代管資料表](https://docs.cloud.google.com/bigquery/docs/continuous-queries?hl=zh-tw#write-bigquery)」。

### 從 Iceberg 代管資料表匯出資料

以下各節說明如何將 Iceberg 代管資料表中的資料，匯出為各種資料表格式。

#### 將資料匯出為平面格式

如要將 Iceberg 代管資料表匯出為平面格式，請使用 [`EXPORT DATA` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/other-statements?hl=zh-tw#export_data_statement)，並選取目的地格式。詳情請參閱「[匯出資料](https://docs.cloud.google.com/bigquery/docs/exporting-data?hl=zh-tw#sql)」。

### 建立 Iceberg 代管資料表中繼資料快照

如要建立 Iceberg 代管資料表中繼資料快照，請按照下列步驟操作：

1. 使用 [`EXPORT TABLE
   METADATA`](https://docs.cloud.google.com/bigquery/docs/exporting-data?hl=zh-tw#export_table_metadata) SQL 陳述式，將中繼資料匯出為 Iceberg V2 格式。
2. 選用：排定 Iceberg 中繼資料快照重新整理作業。如要根據設定的時間間隔重新整理 Iceberg 中繼資料快照，請使用[排定的查詢](https://docs.cloud.google.com/bigquery/docs/scheduling-queries?hl=zh-tw)。
3. 選用：為專案啟用中繼資料自動重新整理功能，在每次資料表變動時，自動更新 Iceberg 資料表中繼資料快照。如要啟用中繼資料自動重新整理功能，請與 [bigquery-tables-for-apache-iceberg-help@google.com](mailto:bigquery-tables-for-apache-iceberg-help@google.com) 聯絡。每次重新整理作業都會產生 [`EXPORT METADATA` 費用](#queries_and_jobs)。

下列範例使用 DDL 陳述式 `EXPORT TABLE METADATA FROM
mydataset.test` 建立名為 `My Scheduled Snapshot
Refresh Query` 的排定查詢。DDL 陳述式每 24 小時執行一次。

```
bq query \
    --use_legacy_sql=false \
    --display_name='My Scheduled Snapshot Refresh Query' \
    --schedule='every 24 hours' \
    'EXPORT TABLE METADATA FROM mydataset.test'
```

### 查看 Iceberg 代管資料表中繼資料快照

重新整理 Iceberg 代管資料表中繼資料快照後，您可以在原本建立 Iceberg 代管資料表的 [Cloud Storage URI](https://docs.cloud.google.com/bigquery/docs/batch-loading-data?hl=zh-tw#gcs-uri) 中找到該快照。`/data` 資料夾包含 Parquet 檔案資料 shard，`/metadata` 資料夾則包含 Iceberg 代管資料表中繼資料快照。

```
SELECT
  table_name,
  REGEXP_EXTRACT(ddl, r"storage_uri\s*=\s*\"([^\"]+)\"") AS storage_uri
FROM
  `mydataset`.INFORMATION_SCHEMA.TABLES;
```

請注意，`mydataset` 和 `table_name` 是實際資料集和資料表的預留位置。

### 使用 Spark 讀取 Iceberg 代管資料表

下列範例會設定環境，以便搭配使用 Spark SQL 和 Spark，然後執行查詢，從指定的 Iceberg 代管資料表擷取資料。

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

* ICEBERG\_VERSION\_NUMBER：目前的執行階段版本。請前往 [Iceberg 版本](https://iceberg.apache.org/releases/)下載最新版本。
* CATALOG\_NAME：：參照
  Iceberg 代管資料表的目錄。
* BUCKET\_PATH：：資料表檔案所在 bucket 的路徑。
  例如：`gs://mybucket/`。
* FOLDER\_NAME：包含資料表檔案的資料夾。例如：`myfolder`。

### 修改 Iceberg 代管資料表

如要修改 Iceberg 代管資料表，請按照「[修改資料表結構定義](https://docs.cloud.google.com/bigquery/docs/managing-table-schemas?hl=zh-tw)」中的步驟操作。

### 使用多陳述式交易

您可以對 Iceberg 代管資料表使用[多陳述式交易](https://docs.cloud.google.com/bigquery/docs/transactions?hl=zh-tw)，方法與標準 BigQuery 資料表相同。多重陳述式交易通常用於同時對多個資料表執行異動，或對單一資料表執行多個階段的異動。多陳述式交易可保證 ACID 屬性，並支援快照隔離。

適用標準[多陳述式交易限制](https://docs.cloud.google.com/bigquery/docs/transactions?hl=zh-tw#limitations)。

### 使用分區

您可以對 Iceberg 代管資料表使用[資料表分區](https://docs.cloud.google.com/bigquery/docs/partitioned-tables?hl=zh-tw)，方法與標準 BigQuery 資料表類似。您可以指定分區資料欄來區隔資料表。Iceberg 代管資料表支援下列資料欄類型：

* `DATE`
* `DATETIME`
* `TIMESTAMP`

依 `DATE`、`DATETIME` 或 `TIMESTAMP` 資料欄將資料表分區，稱為「時間單位資料欄分區」。您可以選擇分區的[精細程度為小時、日、月或年](https://docs.cloud.google.com/bigquery/docs/partitioned-tables?hl=zh-tw#select_daily_hourly_monthly_or_yearly_partitioning)。

Iceberg 代管資料表也支援[分群](https://docs.cloud.google.com/bigquery/docs/clustered-tables?hl=zh-tw)，以及[合併分群和分區資料表](https://docs.cloud.google.com/bigquery/docs/clustered-tables?hl=zh-tw#combine-clustered-partitioned-tables)。

#### 分區限制

* 所有 [BigQuery 分區資料表限制](https://docs.cloud.google.com/bigquery/docs/partitioned-tables?hl=zh-tw#limitations)皆適用。
* 不支援 `DATE`、`DATETIME` 或 `TIMESTAMP` 以外的分區資料欄類型。
* 不支援[分區演進](https://iceberg.apache.org/docs/1.5.1/evolution/#partition-evolution)。

#### 建立分區 Iceberg 代管資料表

如要建立分區 Iceberg 代管資料表，請按照操作說明[建立標準 Iceberg 代管資料表](#create-iceberg-tables)，並依據環境加入下列其中一項：

* [`PARTITION BY` 子句](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#partition_expression)
* [`--time_partitioning_field` 和 `--time_partitioning_type` 旗標](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#mk-table)
* [`timePartitioning` 屬性](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables?hl=zh-tw#timepartitioning)

您可以按照與標準 BigQuery 資料表相同的方式，設定及更新[分區到期時間](https://docs.cloud.google.com/bigquery/docs/managing-partitioned-tables?hl=zh-tw#partition-expiration)。過期的分區會在時間回溯期結束後，由垃圾收集機制處理。如果將資料新增至已過期的分區，資料會立即過期。

#### 修改及查詢分區 Iceberg 代管資料表

分區 Iceberg 代管資料表的 BigQuery 資料操縱語言 (DML) 陳述式和查詢，與標準 Iceberg 代管資料表相同。BigQuery 會自動將工作範圍限定在正確的分區，類似於 [Iceberg 隱藏分區](https://iceberg.apache.org/docs/latest/partitioning/#icebergs-hidden-partitioning)。此外，您新增至資料表的任何新資料都會自動分區。

您也可以使用其他引擎查詢分區 Iceberg 代管資料表，方法與標準 Iceberg 代管資料表相同。建議[啟用中繼資料快照](https://docs.cloud.google.com/bigquery/docs/iceberg-tables?hl=zh-tw#create-iceberg-table-snapshots)，以獲得最佳體驗。

為強化安全性，Iceberg 代管資料表的分區資訊會與資料路徑分離，並完全由中繼資料層管理。

## 定價

Iceberg 代管資料表的定價包含儲存空間、儲存空間最佳化、查詢和工作。

### 儲存空間

Iceberg 代管資料表會將所有資料儲存在 [Cloud Storage](https://docs.cloud.google.com/storage?hl=zh-tw)。系統會根據所有儲存的資料 (包括歷來資料表資料) 向您收費。您可能也需要支付 Cloud Storage [資料處理](https://cloud.google.com/storage/pricing?hl=zh-tw#process-pricing)和[移轉費用](https://cloud.google.com/storage/pricing?hl=zh-tw#network-buckets)。如果作業是透過 BigQuery 或 BigQuery Storage API 處理，則可能免除部分 Cloud Storage 作業費用。BigQuery 不會收取專屬的儲存費用。詳情請參閱「[Cloud Storage 定價](https://cloud.google.com/storage/pricing?hl=zh-tw)」。

### 儲存空間最佳化

Iceberg 代管資料表會自動執行資料表管理作業，包括壓縮、分群、垃圾回收，以及 BigQuery 中繼資料生成/重新整理，以最佳化查詢效能並降低儲存成本。資料表管理的運算資源用量，會以資料運算單元 (DCU) 為單位，按秒累計計費。詳情請參閱「[Iceberg 代管資料表定價](https://cloud.google.com/products/biglake/pricing?hl=zh-tw)」。

透過 Storage Write API 串流時執行的資料匯出作業，會計入 Storage Write API 定價，不會視為背景維護作業收費。詳情請參閱「[資料擷取定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#data_ingestion_pricing)」。

如要查看這些背景作業的記錄和運算用量，請查詢 [`INFORMATION_SCHEMA.JOBS`](https://docs.cloud.google.com/bigquery/docs/information-schema-jobs?hl=zh-tw) 檢視表。如需查詢範例，請參閱下列內容：

* [儲存空間最佳化工作](https://docs.cloud.google.com/bigquery/docs/information-schema-jobs?hl=zh-tw#get-iceberg-storage-optimization-jobs)
* [`EXPORT TABLE METADATA` 項工作](https://docs.cloud.google.com/bigquery/docs/information-schema-jobs?hl=zh-tw#get-iceberg-export-table-metadata-jobs)

### 查詢和工作

與 BigQuery 資料表類似，如果您使用 [BigQuery 隨選定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#on_demand_pricing)，則須支付查詢和讀取位元組 (每 TiB) 的費用；如果使用 [BigQuery 運算資源定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#capacity_compute_analysis_pricing)，則須支付運算單元消耗量 (每運算單元時數) 的費用。

BigQuery 定價也適用於 [BigQuery Storage Read API](https://cloud.google.com/bigquery/pricing?hl=zh-tw#data_extraction_pricing) 和 [Storage Write API](https://cloud.google.com/bigquery/pricing?hl=zh-tw#data_ingestion_pricing)。

載入和匯出作業 (例如 `EXPORT METADATA`) 會使用[企業版即付即用運算單元](https://cloud.google.com/bigquery/pricing?hl=zh-tw#enterprise-edition-slots)。這與 BigQuery 資料表不同，後者不會對這些作業收費。如果 `PIPELINE` 預留項目有 Enterprise 或 Enterprise Plus 運算單元，載入和匯出作業會優先使用這些預留項目運算單元。

## 限制

Iceberg 代管資料表有下列限制：

* Iceberg 代管資料表不支援[重新命名作業](https://docs.cloud.google.com/bigquery/docs/managing-tables?hl=zh-tw#renaming-table)或 [`ALTER TABLE RENAME TO` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#alter_table_rename_to_statement)。
* Iceberg 代管資料表不支援[資料表複製](https://docs.cloud.google.com/bigquery/docs/managing-tables?hl=zh-tw#copy-table)或 [`CREATE TABLE COPY` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#create_table_copy)。
* Iceberg 代管資料表不支援[資料表複製](https://docs.cloud.google.com/bigquery/docs/table-clones-intro?hl=zh-tw)或 [`CREATE TABLE CLONE` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#create_table_clone_statement)。
* Iceberg 代管資料表不支援[資料表快照](https://docs.cloud.google.com/bigquery/docs/table-snapshots-intro?hl=zh-tw)或 [`CREATE SNAPSHOT TABLE` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#create_snapshot_table_statement)。
* Iceberg 代管資料表不支援下列資料表結構定義：
  + 結構定義空白
  + 包含 `BIGNUMERIC`、`INTERVAL`、`JSON`、`RANGE` 或 `GEOGRAPHY` 資料類型的結構定義。
  + 含有[欄位定序](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#collatable_data_types)的結構定義。
  + 含有[預設值運算式](https://docs.cloud.google.com/bigquery/docs/default-values?hl=zh-tw)的結構定義。
* Iceberg 代管資料表不支援下列結構定義演進案例：
  + `NUMERIC` 到 `FLOAT` 類型強制轉型
  + `INT` 到 `FLOAT` 類型強制轉型
  + 使用 SQL DDL 陳述式，將新的巢狀欄位新增至現有的 `RECORD` 資料欄
* 透過控制台或 API 查詢時，Iceberg 代管資料表會顯示 0 位元組的儲存空間大小。
* Iceberg 代管資料表不支援 [materialized view](https://docs.cloud.google.com/bigquery/docs/materialized-views-intro?hl=zh-tw)。
* Iceberg 代管資料表不支援[授權檢視表](https://docs.cloud.google.com/bigquery/docs/authorized-views?hl=zh-tw)，但支援[資料欄層級存取控管](https://docs.cloud.google.com/bigquery/docs/column-level-security-intro?hl=zh-tw)和[資料列層級安全性](https://docs.cloud.google.com/bigquery/docs/row-level-security-intro?hl=zh-tw)。
* Iceberg 代管資料表不支援[代管災難復原](https://docs.cloud.google.com/bigquery/docs/managed-disaster-recovery?hl=zh-tw)
* Iceberg 代管資料表不支援[安全防護期](https://docs.cloud.google.com/bigquery/docs/time-travel?hl=zh-tw#fail-safe)。
* Iceberg 代管資料表不支援擷取工作。
* `INFORMATION_SCHEMA.TABLE_STORAGE` 檢視表不含 Iceberg 代管資料表。
* Iceberg 代管資料表不支援做為查詢結果目的地。您可以改用 [`CREATE
  TABLE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#create_table_statement) 陳述式和 `AS query_statement` 引數，建立資料表做為查詢結果目的地。
* `CREATE OR REPLACE` 不支援將標準資料表替換為 Iceberg 代管資料表，或將 Iceberg 代管資料表替換為標準資料表。
* [批次載入](https://docs.cloud.google.com/bigquery/docs/batch-loading-data?hl=zh-tw)和 [`LOAD DATA` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/load-statements?hl=zh-tw)僅支援將資料附加至現有的 Iceberg 代管資料表。
* [批次載入](https://docs.cloud.google.com/bigquery/docs/batch-loading-data?hl=zh-tw)和 [`LOAD
  DATA` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/load-statements?hl=zh-tw)不支援結構定義更新。
* `TRUNCATE TABLE`不支援 Iceberg 代管資料表。有兩種替代方案：
  + [`CREATE OR REPLACE
    TABLE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#create_table_statement)，並使用相同的資料表建立選項。
  + `DELETE FROM` table `WHERE` true
* [`APPENDS` 資料表值函式 (TVF)](https://docs.cloud.google.com/bigquery/docs/change-history?hl=zh-tw) 不支援 Iceberg 代管資料表。
* Iceberg 中繼資料可能不含過去 90 分鐘內，由 Storage Write API 串流至 BigQuery 的資料。
* 使用 BigQuery Storage Write API (gRPC) 將資料串流至 Iceberg 代管資料表時，資料表的 `lastModifiedTime` 可能不會立即更新，且可能過時。BigLake 狀態中的中繼資料匯出時間戳記，反映的是產生 Iceberg 中繼資料時使用的讀取快照時間，而非資料表的 `lastModifiedTime`。
* 使用 `tabledata.list` 的記錄式分頁存取不支援 Iceberg 代管資料表。
* 每個 Iceberg 代管資料表只能同時執行一個變動 DML 陳述式 (`UPDATE`、`DELETE` 和 `MERGE`)。其他變更 DML 陳述式會排入佇列。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-10-29 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-10-29 (世界標準時間)。"],[],[]]