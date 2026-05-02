* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 為 Delta Lake 建立 BigLake 外部資料表

BigLake 可讓您存取 Delta Lake 資料表，並提供更精細的存取控管機制。[Delta Lake](https://docs.databricks.com/en/delta/index.html) 是由 Databricks 開發的開放原始碼表格資料儲存格式，支援 PB 級資料表。

BigQuery 支援 Delta Lake 資料表的下列功能：

* **存取權委派**：透過存取權委派，查詢外部資料儲存區中的結構化資料。存取權委派功能可將 Delta Lake 資料表的存取權，與基礎資料儲存空間的存取權分開。
* **精細的存取控管**：在資料表層級強制執行精細的安全防護機制，包括[列層級](https://docs.cloud.google.com/bigquery/docs/row-level-security-intro?hl=zh-tw)和[欄層級](https://docs.cloud.google.com/bigquery/docs/column-level-security-intro?hl=zh-tw)安全防護機制。如果是以 Cloud Storage 為基礎的 Delta Lake 資料表，您也可以使用[動態資料遮蓋](https://docs.cloud.google.com/bigquery/docs/column-data-masking?hl=zh-tw)。
* **結構定義演變**：系統會自動偵測 Delta Lake 資料表中的結構定義變更。結構定義的變更會反映在 BigQuery 資料表中。

將 Delta Lake 資料表設定為 [BigLake 資料表](https://docs.cloud.google.com/bigquery/docs/biglake-intro?hl=zh-tw)時，也支援所有 BigLake 功能。

## 事前準備

1. 在 Google Cloud 控制台的專案選擇器頁面中，選取或建立 Google Cloud 專案。

   **選取或建立專案所需的角色**

   * **選取專案**：選取專案時，不需要具備特定 IAM 角色，只要您已獲授角色，即可選取任何專案。
   * **建立專案**：如要建立專案，您需要具備專案建立者角色 (`roles/resourcemanager.projectCreator`)，其中包含 `resourcemanager.projects.create` 權限。[瞭解如何授予角色](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)。
   **注意**：如果您不打算保留在這項程序中建立的資源，請建立新專案，而不要選取現有專案。完成這些步驟後，您就可以刪除專案，並移除與該專案相關聯的所有資源。

   [前往專案選取器](https://console.cloud.google.com/projectselector2/home/dashboard?hl=zh-tw)
2. [確認專案已啟用計費功能 Google Cloud](https://docs.cloud.google.com/billing/docs/how-to/verify-billing-enabled?hl=zh-tw#confirm_billing_is_enabled_on_a_project) 。
3. 啟用 BigQuery Connection 和 BigQuery Reservation API。

   **啟用 API 時所需的角色**

   如要啟用 API，您需要服務使用情形管理員 IAM 角色 (`roles/serviceusage.serviceUsageAdmin`)，其中包含 `serviceusage.services.enable` 權限。[瞭解如何授予角色](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)。

   [啟用 API](https://console.cloud.google.com/flows/enableapi?apiid=bigqueryconnection%2Cbigqueryreservation&%3Bredirect=https%3A%2F%2Fconsole.cloud.google.com&hl=zh-tw)
4. 在 Google Cloud 控制台中啟用 Cloud Shell。

   [啟用 Cloud Shell](https://console.cloud.google.com/?cloudshell=true&hl=zh-tw)
5. 確認您有 BigQuery [資料集](https://docs.cloud.google.com/bigquery/docs/datasets?hl=zh-tw)。
6. 確認 Google Cloud SDK 版本為 366.0.0 以上：

   ```
   gcloud version
   ```

   視需要[更新 Google Cloud SDK](https://docs.cloud.google.com/sdk/docs/quickstart?hl=zh-tw)。
7. 根據外部資料來源建立 [Cloud 資源連線](https://docs.cloud.google.com/bigquery/docs/create-cloud-resource-connection?hl=zh-tw#create-cloud-resource-connection)，並授予該連線 [Cloud Storage 存取權](https://docs.cloud.google.com/bigquery/docs/create-cloud-resource-connection?hl=zh-tw#access-storage)。如果沒有建立連線的適當權限，請 BigQuery 管理員建立連線並與您共用。

### 必要的角色

如要建立 Delta Lake 資料表，您必須具備下列權限：

* `bigquery.tables.create`
* `bigquery.connections.delegate`

BigQuery 管理員 (`roles/bigquery.admin`) 預先定義的身分與存取權管理角色包含這些權限。

如果您不是這個角色的主體，請要求管理員授予這些權限，或為您建立 Delta Lake 資料表。

此外，如要允許 BigQuery 使用者查詢資料表，與連線相關聯的服務帳戶必須具備下列權限和存取權：

* BigQuery 檢視者 (`roles/bigquery.viewer`) 角色
* BigQuery Connection 使用者 (`roles/bigquery.connectionUser`) 角色
* 存取包含該資料的 Cloud Storage bucket

如要進一步瞭解 BigQuery 中的 Identity and Access Management 角色和權限，請參閱[預先定義的角色和權限](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)一文。

## 使用 Delta Lake 建立資料表

如要建立 Delta Lake 資料表，請按照下列步驟操作。

### SQL

使用 [`CREATE EXTERNAL TABLE` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#create_external_table_statement)建立 Delta Lake 資料表：

```
CREATE EXTERNAL TABLE `PROJECT_ID.DATASET.DELTALAKE_TABLE_NAME`
WITH CONNECTION `PROJECT_ID.REGION.CONNECTION_ID`
OPTIONS (
  format ="DELTA_LAKE",
  uris=['DELTA_TABLE_GCS_BASE_PATH']);
```

替換下列值：

* PROJECT\_ID：您要在其中建立 Delta Lake 資料表的專案 ID
* DATASET：要包含 Delta Lake 資料表的 BigQuery 資料集
* DELTALAKE\_TABLE\_NAME：Delta Lake 資料表的名稱
* REGION：包含要建立 Delta Lake 資料表之連線的區域，例如 `us`
* CONNECTION\_ID：連線 ID，例如 `myconnection`

  在 Google Cloud 控制台中[查看連線詳細資料](https://docs.cloud.google.com/bigquery/docs/working-with-connections?hl=zh-tw#view-connections)時，連線 ID 是「連線 ID」中顯示的完整連線 ID 最後一個區段的值，例如 `projects/myproject/locations/connection_location/connections/myconnection`。
* DELTA\_TABLE\_GCS\_BASE\_PATH：Delta Lake 資料表前置字元

### bq

在指令列環境中，使用 [`bq mk`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_mk) 指令建立 Delta Lake 資料表：

```
bq mk --table --external_table_definition=DEFINITION_FILE PROJECT_ID:DATASET.DELTALAKE_TABLE_NAME
```

替換下列值：

* DEFINITION\_FILE：資料表定義檔的路徑
* PROJECT\_ID：您要在其中建立 Delta Lake 資料表的專案 ID
* DATASET：要包含 Delta Lake 資料表的 BigQuery 資料集
* DELTALAKE\_TABLE\_NAME：Delta Lake 資料表的名稱

### REST

使用 [BigQuery API](https://docs.cloud.google.com/bigquery/docs/reference/rest?hl=zh-tw) 呼叫 `tables.insert` API 方法，建立 Delta Lake 資料表：

```
REQUEST='{
  "autodetect": true,
  "externalDataConfiguration": {
  "sourceFormat": "DELTA_LAKE",
  "connectionId": "PROJECT_ID.REGION.CONNECTION_ID",
  "sourceUris": [
    "DELTA_TABLE_GCS_BASE_PATH"
  ],
 },
"tableReference": {
"tableId": "DELTALAKE_TABLE_NAME"
}
}'

echo $REQUEST | curl -X POST -d @- -H "Content-Type: application/json" -H "Authorization: Bearer $(gcloud auth print-access-token)" https://bigquery.googleapis.com/bigquery/v2/projects/PROJECT_ID/datasets/DATASET/tables?autodetect_schema=true
```

替換下列值：

* PROJECT\_ID：您要在其中建立 Delta Lake 資料表的專案 ID
* REGION：包含要建立 Delta Lake 資料表之連線的區域，例如 `us`
* CONNECTION\_ID：連線 ID，例如 `myconnection`

  在 Google Cloud 控制台中[查看連線詳細資料](https://docs.cloud.google.com/bigquery/docs/working-with-connections?hl=zh-tw#view-connections)時，連線 ID 是「連線 ID」中顯示的完整連線 ID 最後一個區段的值，例如 `projects/myproject/locations/connection_location/connections/myconnection`。
* DELTA\_TABLE\_GCS\_BASE\_PATH：Delta Lake 資料表前置字元
* DELTALAKE\_TABLE\_NAME：Delta Lake 資料表的名稱
* DATASET：要包含 Delta Lake 資料表的 BigQuery 資料集

建立 Delta Lake 資料表時，Delta Lake 前置字元會做為資料表的 URI。舉例來說，如果資料表在值區 `gs://bucket/warehouse/basictable/_delta_log` 中有記錄，則資料表 URI 為 `gs://bucket/warehouse/basictable`。在 Delta Lake 資料表上執行查詢時，BigQuery 會讀取前置字元下的資料，找出資料表的目前版本，然後計算資料表的中繼資料和檔案。

雖然您可以在沒有連線的情況下建立 Delta Lake 外部資料表，但基於下列原因，我們不建議這麼做：

* 使用者嘗試存取 Cloud Storage 中的檔案時，可能會遇到 `ACCESS_DENIED` 錯誤。
* 精細的存取控管等功能僅適用於 Delta Lake BigLake 資料表。

## 更新 Delta Lake 資料表

如要更新 (重新整理) Delta Lake 資料表的結構定義，請按照下列步驟操作。

### bq

在指令列環境中，使用 [`bq update`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_update) 指令更新 (重新整理) Delta Lake 資料表的結構定義：

```
bq update --autodetect_schema PROJECT_ID:DATASET.DELTALAKE_TABLE_NAME
```

替換下列值：

* PROJECT\_ID：您要在其中建立 Delta Lake 資料表的專案 ID
* DATASET：要包含 Delta Lake 資料表的 BigQuery 資料集
* DELTALAKE\_TABLE\_NAME：Delta Lake 資料表的名稱

### REST

使用 [BigQuery API](https://docs.cloud.google.com/bigquery/docs/reference/rest?hl=zh-tw) 呼叫 `tables.patch` API 方法，更新 Delta Lake 資料表：

```
REQUEST='{
  "externalDataConfiguration": {
    "sourceFormat": "DELTA_LAKE",
    "sourceUris": [
      "DELTA_TABLE_GCS_BASE_PATH"
    ],
    "connectionId": "PROJECT_ID.REGION.CONNECTION_ID",
    "autodetect": true
  }
}'
echo $REQUEST |curl -X PATCH -d @- -H "Content-Type: application/json" -H "Authorization: Bearer $(gcloud auth print-access-token)" https://bigquery.googleapis.com/bigquery/v2/projects/PROJECT_ID/datasets/DATASET/tables/DELTALAKE_TABLE_NAME?autodetect_schema=true
```

替換下列值：

* DELTA\_TABLE\_GCS\_BASE\_PATH：Delta Lake 資料表前置字元
* PROJECT\_ID：您要在其中建立 Delta Lake 資料表的專案 ID
* REGION：包含要建立 Delta Lake 資料表之連線的區域，例如 `us`
* CONNECTION\_ID：連線 ID，例如 `myconnection`

  在 Google Cloud 控制台中[查看連線詳細資料](https://docs.cloud.google.com/bigquery/docs/working-with-connections?hl=zh-tw#view-connections)時，連線 ID 是「連線 ID」中顯示的完整連線 ID 最後一個區段的值，例如 `projects/myproject/locations/connection_location/connections/myconnection`。
* DELTALAKE\_TABLE\_NAME：Delta Lake 資料表的名稱
* DATASET：要包含 Delta Lake 資料表的 BigQuery 資料集

## 查詢 Delta Lake 資料表

建立 Delta Lake BigLake 資料表後，您就可以[使用 GoogleSQL 語法查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw)，與標準 BigQuery 資料表相同。例如：

```
SELECT field1, field2 FROM mydataset.my_cloud_storage_table;
```

詳情請參閱[查詢 BigLake 資料表中的 Cloud Storage 資料](https://docs.cloud.google.com/bigquery/docs/query-cloud-storage-using-biglake?hl=zh-tw#query-biglake-table-bigquery)。

與服務帳戶相關聯的[外部連線](https://docs.cloud.google.com/bigquery/docs/connections-api-intro?hl=zh-tw)可用於連線至資料存放區。由於服務帳戶會從資料存放區擷取資料，因此使用者只需要存取 Delta Lake 表格。

## 資料對應

BigQuery 會將 Delta Lake 資料類型轉換為 BigQuery 資料類型，如下表所示：

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

## 限制

Delta Lake 資料表有 [BigLake 資料表限制](https://docs.cloud.google.com/bigquery/docs/biglake-intro?hl=zh-tw#limitations)，以及下列限制：

* 支援 Delta Lake [讀取器版本](https://github.com/delta-io/delta/blob/master/PROTOCOL.md#reader-version-requirements) 3，其中包含相對路徑刪除向量和資料欄對應。
* 不支援 Delta Lake V2 檢查點。
* 您必須在最後一個記錄項目檔中列出讀取器版本。舉例來說，新資料表必須包含 `00000..0.json`。
* 系統不支援變更資料擷取 (CDC) 作業。系統會忽略所有現有的 CDC 作業。
* 系統會自動偵測結構定義。系統不支援使用 BigQuery 修改結構定義。
* 資料表資料欄名稱必須遵守 BigQuery 的[資料欄名稱限制](https://docs.cloud.google.com/bigquery/docs/schemas?hl=zh-tw#column_names)。
* 不支援具體化檢視表。
* Delta Lake 不支援 Read API。
* Delta Lake BigLake 資料表不支援 `timestamp_ntz` 資料類型。

## 疑難排解

本節提供 Delta Lake BigLake 資料表的相關說明。如需排解 BigQuery 查詢問題的一般說明，請參閱「[排解查詢問題](https://docs.cloud.google.com/bigquery/docs/troubleshoot-queries?hl=zh-tw)」。

### 查詢逾時和資源錯誤

檢查 Delta Lake 表格的記錄目錄 (`gs://bucket/warehouse/basictable/_delta_log`)，並尋找版本號碼大於先前[檢查點](https://github.com/delta-io/delta/blob/master/PROTOCOL.md#checkpoints)的 JSON 檔案。您可以列出目錄或檢查 [\_delta\_log/\_last\_checkpoint 檔案](https://github.com/delta-io/delta/blob/master/PROTOCOL.md#last-checkpoint-file)，取得版本號碼。如果 JSON 檔案大於 10 MiB，可能會導致資料表擴充速度變慢，進而引發逾時和資源問題。如要解決這個問題，請使用下列指令建立新的檢查點，讓查詢作業略過讀取 JSON 檔案：

```
  spark.sql("ALTER TABLE delta.`gs://bucket/mydeltatabledir` SET TBLPROPERTIES ('delta.checkpointInterval' = '1')");
```

使用者接著可以使用相同指令，將檢查點間隔重設為預設值 10，或設為可避免檢查點之間 JSON 檔案超過 50 MB 的值。

### 欄名稱無效

確認 Delta Lake 資料表已啟用欄位對應。[Reader 2 以上版本](https://github.com/delta-io/delta/blob/master/PROTOCOL.md#reader-version-requirements)支援欄位對應。如果是 Reader 第 1 版，請使用下列指令，將「delta.columnMapping.mode」設為「name」：

```
spark.sql("ALTER TABLE delta.`gs://bucket/mydeltatabledir` SET TBLPROPERTIES ('delta.columnMapping.mode' = 'name', 'delta.minReaderVersion' = '3', 'delta.minWriterVersion' = '7')");
```

如果無效的資料欄名稱符合[彈性資料欄名稱限制](https://docs.cloud.google.com/bigquery/docs/schemas?hl=zh-tw#flexible-column-names)，請與 [Cloud Customer Care](https://docs.cloud.google.com/bigquery/docs/getting-support?hl=zh-tw) 團隊聯絡，或寄信至 [biglake-help@google.com](mailto:biglake-help@google.com)。

### 存取遭拒錯誤

如要診斷 Delta Lake BigLake 資料表的問題，請檢查下列項目：

* 請確認您使用的是 Delta Lake BigLake 資料表[(含連線)](#create-tables)。
* 使用者具備[必要權限](#iam-permissions)。

## 效能

如要提升查詢效能，請嘗試下列步驟：

* 使用 [Delta Lake 公用程式](https://docs.databricks.com/en/delta/best-practices.html)壓縮基礎資料檔案，並移除多餘的檔案，例如資料和中繼資料。
* 確認 `delta.checkpoint.writeStatsAsStruct` 已設為 `true`。
* 請確認述詞子句中常用的變數位於分區資料欄。

如果資料集很大 (超過 100 TB)，可能需要額外的設定和功能。如果上述步驟無法解決問題，請考慮聯絡[客戶服務](https://docs.cloud.google.com/bigquery/docs/getting-support?hl=zh-tw)或 [biglake-help@google.com](mailto:biglake-help@google.com)，尤其是資料集大於 100 TB 時。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-02 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-02 (世界標準時間)。"],[],[]]