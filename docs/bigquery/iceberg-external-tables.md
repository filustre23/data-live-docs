Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 建立 Apache Iceberg 外部資料表

透過 Apache Iceberg 外部資料表，您可以使用更精細的存取控管機制，以唯讀格式存取 [Apache Iceberg](https://iceberg.apache.org/docs/latest/) 資料表。

Iceberg 是開放原始碼資料表格式，支援 PB 級資料表。Iceberg 開放規格可讓您在物件儲存空間中儲存的單一資料副本上，執行多個查詢引擎。Apache Iceberg 外部資料表 (以下簡稱「Iceberg 外部資料表」) 支援 [Iceberg 第 2 版](https://iceberg.apache.org/spec/#version-2-row-level-deletes)，包括讀取時合併。支援 [Iceberg 第 3 版](https://iceberg.apache.org/spec/#version-3-extended-types-and-capabilities) (包括二進位刪除向量) 的功能為[預先發布版](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages)。如要提供意見回饋或提出與這項預先發布版功能相關的問題，請傳送電子郵件至 [biglake-help@google.com](mailto:biglake-help@google.com)。

BigQuery 管理員可以強制執行列層級和欄層級的存取控管，包括資料表上的資料遮蓋。如要瞭解如何設定資料表層級的存取控管機制，請參閱「[設定存取控管政策](#set-access-control)」。當您使用 BigQuery Storage API 做為 Managed Service for Apache Spark 和 Serverless Spark 中資料表的資料來源時，系統也會強制執行資料表存取政策。

您可以透過下列方式建立 Iceberg 外部資料表：

* **[使用 Lakehouse 執行階段目錄 (建議做法，適用於 Google Cloud)。](https://docs.cloud.google.com/biglake/docs/about-blms?hl=zh-tw)**
  Lakehouse 執行階段目錄是可擴充的統合式無伺服器代管 metastore，可將儲存於 Google Cloud 的湖倉資料連結至多個執行階段，包括開放原始碼引擎 (例如 Apache Spark) 和 BigQuery。
* **[使用 AWS Glue Data Catalog (建議 AWS 使用者)](https://docs.cloud.google.com/bigquery/docs/glue-federated-datasets?hl=zh-tw)。**建議使用 AWS Glue，因為這是集中式中繼資料存放區，您可以在其中定義儲存在各種 AWS 服務中的資料結構和位置，並提供自動結構定義探索和與 AWS 數據分析工具整合等功能。
* **[使用 Iceberg JSON 中繼資料檔案](#create-using-metadata-file) (建議用於 Azure)。**
  如果您使用 Iceberg JSON 中繼資料檔案，則每當有任何表格更新時，都必須手動更新最新的中繼資料檔案。您可以使用 Apache Spark 的 BigQuery 預存程序，建立參照 Iceberg 中繼資料檔案的 Iceberg 外部資料表。

如需限制的完整清單，請參閱「[限制](#limitations)」一節。

## 事前準備

啟用 BigQuery Connection 和 BigQuery Reservation API。

**啟用 API 時所需的角色**

如要啟用 API，您需要服務使用情形管理員 IAM 角色 (`roles/serviceusage.serviceUsageAdmin`)，其中包含 `serviceusage.services.enable` 權限。[瞭解如何授予角色](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)。

[啟用 API](https://console.cloud.google.com/flows/enableapi?apiid=bigqueryconnection.googleapis.com%2C%5Cnbigqueryreservation.googleapis.com&%3Bredirect=https%3A%2F%2Fconsole.cloud.google.com&hl=zh-tw)

* 如果您在 BigQuery 中使用 Spark 預存程序建立 Iceberg 外部資料表，請務必按照下列步驟操作：

  1. [建立 Spark 連線](https://docs.cloud.google.com/bigquery/docs/connect-to-spark?hl=zh-tw#create-spark-connection)。
  2. [為該連線設定存取控管機制](https://docs.cloud.google.com/bigquery/docs/connect-to-spark?hl=zh-tw#grant-access)。
* 如要在 Cloud Storage 中儲存 Iceberg 外部資料表的中繼資料和資料檔案，請[建立 Cloud Storage bucket](https://docs.cloud.google.com/storage/docs/creating-buckets?hl=zh-tw)。您必須連線至 Cloud Storage bucket，才能存取中繼資料檔案。請按照以下步驟操作：

  1. [建立 Cloud 資源連結](https://docs.cloud.google.com/bigquery/docs/create-cloud-resource-connection?hl=zh-tw#create-cloud-resource-connection)。
  2. [設定該連結的存取權](https://docs.cloud.google.com/bigquery/docs/create-cloud-resource-connection?hl=zh-tw#access-storage)。

### 必要的角色

如要取得建立 Iceberg 外部資料表所需的權限，請要求管理員在專案中授予您下列 IAM 角色：

* [BigQuery 管理員](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.admin)  (`roles/bigquery.admin`)
* [Storage 物件管理員](https://docs.cloud.google.com/iam/docs/roles-permissions/storage?hl=zh-tw#storage.objectAdmin)  (`roles/storage.objectAdmin`)

如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

這些預先定義的角色具備建立 Iceberg 外部資料表所需的權限。如要查看確切的必要權限，請展開「Required permissions」(必要權限) 部分：

#### 所需權限

如要建立 Iceberg 外部資料表，必須具備下列權限：

* `bigquery.tables.create`
* `bigquery.connections.delegate`
* `bigquery.jobs.create`

您或許還可透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)取得這些權限。

## 使用 Lakehouse 執行階段目錄建立資料表

建議使用 [Lakehouse 執行階段目錄](https://docs.cloud.google.com/biglake/docs/about-blms?hl=zh-tw)建立 Iceberg 外部資料表。

## 使用中繼資料檔案建立資料表

您可以使用 [JSON 中繼資料檔案](https://iceberg.apache.org/spec/#table-metadata)建立 Iceberg 外部資料表。不過，我們不建議使用這種方法，因為您必須手動[更新 JSON 中繼資料檔案的 URI](#update-table-metadata)，才能讓 Iceberg 外部資料表保持最新狀態。如果 URI 未保持最新狀態，BigQuery 中的查詢可能會失敗，或提供與直接使用 Iceberg 目錄的其他查詢引擎不同的結果。

使用 [Spark 建立 Iceberg 資料表](https://docs.cloud.google.com/dataproc-metastore/docs/apache-iceberg?hl=zh-tw#iceberg-table-with-spark)時，系統會在您指定的 Cloud Storage 值區中建立 Iceberg 資料表的中繼資料檔案。

選取下列選項之一：

### SQL

使用 [`CREATE EXTERNAL TABLE` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#create_external_table_statement)。以下範例會建立名為 `myexternal-table` 的 Iceberg 外部資料表：

```
  CREATE EXTERNAL TABLE myexternal-table
  WITH CONNECTION `myproject.us.myconnection`
  OPTIONS (
         format = 'ICEBERG',
         uris = ["gs://mybucket/mydata/mytable/metadata/iceberg.metadata.json"]
   )
```

將 `uris` 值替換為特定資料表快照的最新 [JSON 中繼資料檔案](https://iceberg.apache.org/spec/#table-metadata)。

您可以設定 `require_partition_filter` 旗標，啟用「必須使用分區篩選器」。

### bq

在指令列環境中，使用 [`bq mk --table` 指令](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#mk-table)和 `@connection` 修飾符，在 `--external_table_definition` 參數結尾指定要使用的連線。
如要啟用必要分區篩選器，請使用 `--require_partition_filter`。

```
bq mk   

    --table   

    --external_table_definition=TABLE_FORMAT=URI@projects/CONNECTION_PROJECT_ID/locations/CONNECTION_REGION/connections/CONNECTION_ID   

    PROJECT_ID:DATASET.EXTERNAL_TABLE
```

更改下列內容：

* `TABLE_FORMAT`：要建立的資料表格式

  在本例中為 `ICEBERG`。
* `URI`：特定資料表快照的最新 [JSON 中繼資料檔案](https://iceberg.apache.org/spec/#table-metadata)。

  例如 `gs://mybucket/mydata/mytable/metadata/iceberg.metadata.json`。

  URI 也可以指向外部雲端位置，例如 Amazon S3 或 Azure Blob 儲存體。

  + AWS 範例：`s3://mybucket/iceberg/metadata/1234.metadata.json`。
  + Azure 範例：`azure://mystorageaccount.blob.core.windows.net/mycontainer/iceberg/metadata/1234.metadata.json`。
* `CONNECTION_PROJECT_ID`：包含[連線](https://docs.cloud.google.com/bigquery/docs/connect-to-spark?hl=zh-tw)的專案，用於建立 Iceberg 外部資料表，例如 `myproject`
* `CONNECTION_REGION`：包含要建立 Iceberg 外部資料表連線的區域，例如 `us`
* `CONNECTION_ID`：資料表連線 ID，例如 `myconnection`

  在 Google Cloud 控制台中[查看連線詳細資料](https://docs.cloud.google.com/bigquery/docs/working-with-connections?hl=zh-tw#view-connections)時，連線 ID 是「連線 ID」中顯示的完整連線 ID 最後一個部分的值，例如：`projects/myproject/locations/connection_location/connections/myconnection`
* `DATASET`：您要在其中建立資料表的 BigQuery 資料集名稱

  例如 `mydataset`。
* `EXTERNAL_TABLE`：要建立的資料表名稱

  例如 `mytable`。

### 可更新資料表中繼資料

如果您使用 JSON 中繼資料檔案建立 Iceberg 外部資料表，請將資料表定義更新為最新的資料表中繼資料。如要更新結構定義或中繼資料檔案，請選取下列任一選項：

### bq

1. 建立資料表定義檔：

   ```
   bq mkdef --source_format=ICEBERG \
   "URI" > TABLE_DEFINITION_FILE
   ```
2. 使用 [`bq update` 指令](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_update)並加上 `--autodetect_schema` 旗標：

   ```
   bq update --autodetect_schema --external_table_definition=TABLE_DEFINITION_FILE
   PROJECT_ID:DATASET.TABLE
   ```

   更改下列內容：

   * `URI`：您的 Cloud Storage URI，其中包含最新的 [JSON 中繼資料檔案](https://iceberg.apache.org/spec/#table-metadata)

     例如 `gs://mybucket/us/iceberg/mytable/metadata/1234.metadata.json`。
   * `TABLE_DEFINITION_FILE`：包含資料表結構定義的檔案名稱
   * `PROJECT_ID`：包含要更新資料表的專案 ID
   * `DATASET`：包含要更新資料表的資料集
   * `TABLE`：要更新的資料表

### API

使用 [`tables.patch` 方法](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables/patch?hl=zh-tw)，並將 `autodetect_schema` 屬性設為 `true`：

```
PATCH https://bigquery.googleapis.com/bigquery/v2/projects/PROJECT_ID/datasets/DATASET/tables/TABLE?autodetect_schema=true
```

更改下列內容：

* `PROJECT_ID`：包含要更新資料表的專案 ID
* `DATASET`：包含要更新資料表的資料集
* `TABLE`：要更新的資料表

在要求主體中，為下列欄位指定更新的值：

```
{
     "externalDataConfiguration": {
      "sourceFormat": "ICEBERG",
      "sourceUris": [
        "URI"
      ]
    },
    "schema": null
  }'
```

將 `URI` 替換為最新的 Iceberg 中繼資料檔案。例如：`gs://mybucket/us/iceberg/mytable/metadata/1234.metadata.json`。

## 設定存取控管政策

您可以透過[資料欄層級安全防護機制](https://docs.cloud.google.com/bigquery/docs/column-level-security?hl=zh-tw)、[資料列層級安全防護機制](https://docs.cloud.google.com/bigquery/docs/managing-row-level-security?hl=zh-tw)和[資料遮蓋](https://docs.cloud.google.com/bigquery/docs/column-data-masking?hl=zh-tw)，控管 Iceberg 外部資料表的存取權。

## 查詢 Iceberg 外部資料表

詳情請參閱「[查詢 Iceberg 資料](https://docs.cloud.google.com/bigquery/docs/query-iceberg-data?hl=zh-tw)」。

### 查詢歷來資料

您可以使用 [`FOR SYSTEM_TIME AS OF` 子句](https://docs.cloud.google.com/bigquery/docs/access-historical-data?hl=zh-tw#query_data_at_a_point_in_time)，存取 Iceberg 中繼資料中保留的 Iceberg 外部資料表快照。

任何外部資料表都不支援[時空旅行和容錯資料保留時間範圍](https://docs.cloud.google.com/bigquery/docs/time-travel?hl=zh-tw)。

## 資料對應

BigQuery 會將 Iceberg 資料類型轉換為 BigQuery 資料類型，如下表所示：

| **Iceberg 資料類型** | **BigQuery 資料類型** |
| --- | --- |
| `boolean` | `BOOL` |
| `int` | `INT64` |
| `long` | `INT64` |
| `float` | `FLOAT64` |
| `double` | `FLOAT64` |
| `Decimal(P/S)` | `NUMERIC or BIG_NUMERIC depending on precision` |
| `date` | `DATE` |
| `time` | `TIME` |
| `timestamp` | `DATETIME` |
| `timestamptz` | `TIMESTAMP` |
| `string` | `STRING` |
| `uuid` | `BYTES` |
| `fixed(L)` | `BYTES` |
| `binary` | `BYTES` |
| `list<Type>` | `ARRAY<Type>` |
| `struct` | `STRUCT` |
| `map<KeyType, ValueType>` | `ARRAY<Struct<key KeyType, value ValueType>>` |

## 限制

除了[外部資料表限制](https://docs.cloud.google.com/bigquery/docs/biglake-intro?hl=zh-tw#limitations)外，Iceberg 外部資料表還有下列限制：

* 系統不支援使用 VPC Service Controls 的查詢，因此會產生 `NO_MATCHING_ACCESS_LEVEL` 等錯誤。
* 使用讀取時合併的資料表有下列限制：

  + 每個資料檔案最多可與 10,000 個刪除檔案建立關聯。
  + 每個資料檔案最多可套用 10 萬次等值刪除作業。
  + 如要規避這些限制，請經常壓縮刪除的檔案、在 Iceberg 資料表上建立檢視區塊，避免經常變動的分區，或使用位置刪除而非等值刪除。
* BigQuery 支援使用所有 [Iceberg 分區轉換函式](https://iceberg.apache.org/spec/#partition-transforms)修剪資訊清單。如要瞭解如何修剪分區，請參閱「[查詢分區資料表](https://docs.cloud.google.com/bigquery/docs/querying-partitioned-tables?hl=zh-tw)」。參照 Iceberg 外部資料表的查詢，必須在與分區資料欄比較的述詞中包含常值。
* 系統僅支援 Apache Parquet 資料檔案。
* 系統不支援下列 [Iceberg 3 版](https://iceberg.apache.org/spec/#version-3-extended-types-and-capabilities)功能：

  + 新資料類型：奈秒時間戳記(時區)、不明、變體、幾何、地理位置
  + 初始預設值
  + 表格加密金鑰

## 讀取時合併的費用

以量計價的讀取時合併資料費用，是下列資料掃描量的總和：

* 資料檔案中讀取的所有邏輯位元組 (包括標示為依位置刪除和等值刪除的資料列)。
* 載入等號刪除、位置刪除和刪除向量檔案時讀取的邏輯位元組，用於尋找資料檔案中已刪除的資料列。

## 必須使用分區篩選器

您可以為 Iceberg 資料表啟用「require partition filter」(需要分區篩選器) 選項，要求使用述詞篩選器。啟用此選項後，如嘗試查詢資料表，但未指定與每個資訊清單檔案一致的 `WHERE` 子句，系統會產生下列錯誤：

```
Cannot query over table project_id.dataset.table without a
filter that can be used for partition elimination.
```

每個資訊清單檔案至少需要一個適合用於分區排除的述詞。

建立 Iceberg 資料表時，可以透過下列方式啟用 `require_partition_filter`：

### SQL

使用 [`CREATE EXTERNAL TABLE` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#create_external_table_statement)。下列範例會建立名為 `TABLE` 的 Iceberg 外部資料表，並啟用必要的分區篩選器：

```
  CREATE EXTERNAL TABLE TABLE
  WITH CONNECTION `PROJECT_ID.REGION.CONNECTION_ID`
  OPTIONS (
         format = 'ICEBERG',
         uris = [URI],
         require_partition_filter = true
   )
```

更改下列內容：

* `TABLE`：要建立的資料表名稱。
* `PROJECT_ID`：包含要建立資料表的專案 ID。
* `REGION`：要建立 Iceberg 資料表的[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)。
* `CONNECTION_ID`：[連線 ID](https://docs.cloud.google.com/bigquery/docs/working-with-connections?hl=zh-tw#view-connections)。例如：`myconnection`。
* `URI`：包含最新 [JSON 中繼資料檔案](https://iceberg.apache.org/spec/#table-metadata)的 Cloud Storage URI。

  例如 `gs://mybucket/us/iceberg/mytable/metadata/1234.metadata.json`。

  URI 也可以指向外部雲端位置，例如 Amazon S3 或 Azure Blob 儲存體。

  + AWS 範例：`s3://mybucket/iceberg/metadata/1234.metadata.json`。
  + Azure 範例：`azure://mystorageaccount.blob.core.windows.net/mycontainer/iceberg/metadata/1234.metadata.json`。

### bq

使用 `@connection` 裝飾器搭配 [`bq mk --table` 指令](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#mk-table)，在 `--external_table_definition` 參數結尾指定要使用的連線。
使用 `--require_partition_filter` 啟用必要分區篩選器。
下列範例會建立名為 `TABLE` 的 Iceberg 外部資料表，並啟用必要分區篩選器：

```
bq mk \
    --table \
    --external_table_definition=ICEBERG=URI@projects/CONNECTION_PROJECT_ID/locations/CONNECTION_REGION/connections/CONNECTION_ID \
    PROJECT_ID:DATASET.EXTERNAL_TABLE \
    --require_partition_filter
```

更改下列內容：

* `URI`：特定資料表快照的最新 [JSON 中繼資料檔案](https://iceberg.apache.org/spec/#table-metadata)

  例如 `gs://mybucket/mydata/mytable/metadata/iceberg.metadata.json`。

  URI 也可以指向外部雲端位置，例如 Amazon S3 或 Azure Blob 儲存體。

  + AWS 範例：`s3://mybucket/iceberg/metadata/1234.metadata.json`。
  + Azure 範例：`azure://mystorageaccount.blob.core.windows.net/mycontainer/iceberg/metadata/1234.metadata.json`。
* `CONNECTION_PROJECT_ID`：包含要建立 Iceberg 外部資料表的[連線](https://docs.cloud.google.com/bigquery/docs/connect-to-spark?hl=zh-tw)的專案，例如 `myproject`
* `CONNECTION_REGION`：包含要建立 Iceberg 外部資料表之連線的[區域](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)。例如：`us`。
* `CONNECTION_ID`：[連線 ID](https://docs.cloud.google.com/bigquery/docs/working-with-connections?hl=zh-tw#view-connections)。例如：`myconnection`。

  在 Google Cloud 控制台中[查看連線詳細資料](https://docs.cloud.google.com/bigquery/docs/working-with-connections?hl=zh-tw#view-connections)時，連線 ID 是「連線 ID」中顯示的完整連線 ID 最後一個部分的值，例如：`projects/myproject/locations/connection_location/connections/myconnection`
* `DATASET`：BigQuery 的名稱

  包含要更新資料表的資料集。例如 `mydataset`。
* `EXTERNAL_TABLE`：要建立的資料表名稱

  例如 `mytable`。

您也可以更新 Iceberg 資料表，啟用必要分區篩選器。

如果您在建立分區資料表時未啟用「需要分區篩選器」選項，可以更新該資料表以新增選項。

### bq

使用 `bq update` 指令並加上 `--require_partition_filter` 旗標。

例如：

如要在預設專案中更新 `mydataset` 中的 `mypartitionedtable`，請輸入：

```
bq update --require_partition_filter PROJECT_ID:DATASET.TABLE
```

## 後續步驟

* 瞭解 [Spark 的預存程序](https://docs.cloud.google.com/bigquery/docs/spark-procedures?hl=zh-tw)。
* 瞭解[存取控管政策](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)。
* 瞭解如何[在 BigQuery 中執行查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw)。
* 瞭解 [BigQuery 支援的陳述式和 SQL 方言](https://docs.cloud.google.com/bigquery/docs/introduction-sql?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-09 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-09 (世界標準時間)。"],[],[]]