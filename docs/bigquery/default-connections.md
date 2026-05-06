Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 預設連線總覽

為簡化工作流程，您可以在 BigQuery 中設定預設的[Cloud 資源連結](https://docs.cloud.google.com/bigquery/docs/create-cloud-resource-connection?hl=zh-tw)，用於建立外部資料表和 BigQuery ML 遠端模型。管理員設定預設連線後，使用者在建立資源時即可參照該連線，不必指定連線詳細資料。

BigQuery 支援下列資源中的預設連線：

* [Cloud Storage BigLake 資料表](https://docs.cloud.google.com/bigquery/docs/create-cloud-storage-table-biglake?hl=zh-tw)
* [物件資料表](https://docs.cloud.google.com/bigquery/docs/object-tables?hl=zh-tw)
* [Apache Iceberg 代管資料表](https://docs.cloud.google.com/bigquery/docs/iceberg-tables?hl=zh-tw#create-iceberg-tables)
* [遠端模型](https://docs.cloud.google.com/bigquery/docs/bqml-introduction?hl=zh-tw#remote_models)

如要使用預設連線，請在下列 SQL 子句中指定 `DEFAULT` 關鍵字：

* [`CREATE EXTERNAL TABLE` 陳述式的 `WITH CONNECTION` 子句](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#create_external_table_statement)
* 遠端模型的 [`CREATE MODEL` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model?hl=zh-tw)的 `REMOTE WITH CONNECTION` 子句

## 事前準備

啟用 BigQuery Connection API。

**啟用 API 時所需的角色**

如要啟用 API，您需要服務使用情形管理員 IAM 角色 (`roles/serviceusage.serviceUsageAdmin`)，其中包含 `serviceusage.services.enable` 權限。[瞭解如何授予角色](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)。

[啟用 API](https://console.cloud.google.com/flows/enableapi?apiid=bigqueryconnection.googleapis.com&hl=zh-tw)

### 必要角色和權限

如要使用預設連線，請使用下列 Identity and Access Management (IAM) 角色：

* 使用預設連線：專案的 BigQuery 連線使用者 (`roles/bigquery.connectionUser`)
* 設定預設連線：專案中的 BigQuery 管理員 (`roles/bigquery.admin`)
* 如有必要，請將權限授予預設連線的服務帳戶：

  + 如果使用預設連線建立外部資料表：外部資料表使用的任何 Cloud Storage bucket 上的 Storage Admin (`roles/storage.admin`)。
  + 如果使用預設連線建立遠端模型：在包含 Vertex AI 端點的專案中，擔任專案 IAM 管理員 (`roles/resourcemanager.projectIamAdmin`)。對於下列類型的遠端模型，這是目前的專案：

    - 透過 Cloud AI 服務使用的遠端模型。
    - 透過指定模型名稱做為端點建立的 Google 或合作夥伴模型。

    如果是所有其他遠端模型，這個專案會包含目標模型部署到的 Vertex AI 端點。

    如果您使用遠端模型分析物件資料表中的非結構化資料，且物件資料表使用的 Cloud Storage bucket 與 Vertex AI 端點位於不同專案，您也必須在物件資料表使用的 Cloud Storage bucket 中擁有 Storage 管理員 (`roles/storage.admin`) 角色。

  如果您是管理員，要設定連線做為預設連線，或是使用者要使用尚未授予適當服務帳戶角色的預設連線，才需要這些角色。詳情請參閱「[設定預設連線](https://docs.cloud.google.com/bigquery/docs/default-connections?hl=zh-tw#configure_the_default_connection)」。

這些預先定義的角色具備執行本文所述工作所需的權限。如要查看確切的必要權限，請展開「Required permissions」(必要權限) 部分：

#### 所需權限

* 使用預設連線：`bigquery.connections.use`
* 建立連線：`bigquery.connections.*`
* 設定預設連線：`bigquery.config.*`
* 為用於建立外部資料表的預設連線設定服務帳戶權限：`storage.buckets.getIamPolicy` 和 `storage.buckets.setIamPolicy`
* 為用於建立遠端模型的預設連線設定服務帳戶權限：
  + `resourcemanager.projects.getIamPolicy` 和
    `resourcemanager.projects.setIamPolicy`
  + 如果預設連線搭配遠端模型使用，處理來自物件資料表的非結構化資料，則 `storage.buckets.getIamPolicy` 和 `storage.buckets.setIamPolicy`

您或許還可透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)取得這些權限。

## 設定預設連線

如要首次設定預設連線，請使用下列其中一種方法：

* 建立連線、將適當的角色授予連線的服務帳戶，然後將連線設為預設連線。

  建立及設定預設連線的使用者需要 BigQuery 管理員角色，以及適當的 Storage 管理員或專案 IAM 管理員角色。預設連線使用者需要 BigQuery 連線使用者角色。
* 建立連線，然後設為預設連線。使用預設連線時，服務會[將適當的角色授予](#permissions-provisioning)預設連線的服務帳戶。

  建立及設定預設連線的使用者必須具備 BigQuery 管理員角色。預設連線使用者需要 BigQuery 連線使用者角色，以及適用的 Storage 管理員或專案 IAM 管理員角色。
* 在支援的陳述式中指定 `DEFAULT` 關鍵字。服務會建立連線、將適當的角色授予連線的服務帳戶，然後將連線設為預設連線。

  預設連線使用者需要 BigQuery 管理員角色，以及適用的 Storage 管理員或專案 IAM 管理員角色。
* 如果缺少預設連線，BigQuery 會建立具有下列屬性的新連線：

  + **區域：**與資料集相同的區域。
  + **名稱：**`__default_cloudresource_connection__`
  + **類型：** `CLOUD_RESOURCE`

**重要事項：** 使用預設連線可能會授予使用者額外權限。舉例來說，如果管理員使用預設連線建立物件資料表，系統會為預設連線的服務帳戶，在適當的 Cloud Storage bucket 上授予 Storage Legacy Bucket Reader 和 Storage Legacy Object Reader 角色。獲准使用連線的使用者，也能透過這些角色獲得的權限存取該 Cloud Storage 值區。

## 為專案設定預設連線

使用 [`ALTER PROJECT SET OPTIONS` DDL 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#alter_project_set_options_statement)，為專案設定預設的 Cloud 資源連結。

以下範例會為專案設定預設連線：

```
  ALTER PROJECT PROJECT_ID
  SET OPTIONS (
    `region-REGION.default_cloud_resource_connection_id` = CONNECTION_ID);
```

更改下列內容：

* `PROJECT_ID`：您要設定預設連線的專案 ID。
* `REGION`：連線的區域。
* `CONNECTION_ID`：要用做資料表和模型預設值的連線 ID 或名稱。請只指定連線 ID 或名稱，並排除附加至名稱或 ID 的專案 ID 和區域前置字元。

如要進一步瞭解如何為專案設定預設連線，請參閱「[管理預設設定](https://docs.cloud.google.com/bigquery/docs/default-configuration?hl=zh-tw)」。

## 預設連線的權限佈建

使用預設連線建立外部資料表或遠端模型時，如果預設連線的服務帳戶尚未具備適當角色，Google Cloud 會將這些角色授予該服務帳戶。如果沒有外部資料表或遠端模型所用 Cloud Storage 或 Vertex AI 資源的管理權限，這項動作就會失敗。

預設連線的服務帳戶會取得下列角色：

| 資料表或模型類型 | 遠端資源 | 指派給連線服務帳戶的角色 |
| --- | --- | --- |
| [Cloud Storage BigLake 資料表](https://docs.cloud.google.com/bigquery/docs/create-cloud-storage-table-biglake?hl=zh-tw) | Cloud Storage | `roles/storage.legacyBucketReader`  `roles/storage.legacyObjectReader` |
| [物件資料表](https://docs.cloud.google.com/bigquery/docs/object-tables?hl=zh-tw) | Cloud Storage | `roles/storage.legacyBucketReader`  `roles/storage.legacyObjectReader` |
| [Iceberg 代管資料表](https://docs.cloud.google.com/bigquery/docs/iceberg-tables?hl=zh-tw#create-iceberg-tables) | Cloud Storage | `roles/storage.legacyBucketWriter`  `roles/storage.legacyObjectOwner` |
| [BigQuery ML 遠端模型與 Vertex AI 模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model-https?hl=zh-tw) | Google 自有模型 | `roles/aiplatform.user` |
| 可從 Model Garden 部署至端點 |
| 使用者模型 |
| 經過微調的模型 | `roles/aiplatform.serviceAgent` |
| [透過 Cloud AI 服務使用 BigQuery ML 遠端模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model-service?hl=zh-tw) | 文件處理器 | `roles/documentai.apiUser` |
| 語音辨識器 | `roles/speech.serviceAgent` |
| Cloud NLP | `roles/serviceusage.serviceUsageConsumer` |
| Cloud Vision | `roles/serviceusage.serviceUsageConsumer` |
| Cloud Translation | `roles/cloudtranslate.user` |

## 使用 `CONNECTION DEFAULT` 建立外部資料表

以下範例說明如何在 BigQuery 中指定 `WITH CONNECTION DEFAULT` 來建立外部資料表。

### 範例：建立 Cloud Storage BigLake 資料表

下列 SQL 運算式會使用預設連線，建立 [Cloud Storage BigLake 資料表](https://docs.cloud.google.com/bigquery/docs/create-cloud-storage-table-biglake?hl=zh-tw)：

```
CREATE EXTERNAL TABLE PROJECT_ID.DATASET.EXTERNAL_TABLE_NAME
WITH CONNECTION DEFAULT
OPTIONS (
  format = 'TABLE_FORMAT',
  uris = ['BUCKET_PATH']);
```

### 範例：使用預設連線建立物件資料表

下列 SQL 運算式會建立具有預設連線的[物件資料表](https://docs.cloud.google.com/bigquery/docs/object-tables?hl=zh-tw)：

```
CREATE EXTERNAL TABLE PROJECT_ID.DATASET.EXTERNAL_TABLE_NAME
WITH CONNECTION DEFAULT
OPTIONS (
  object_metadata = 'SIMPLE'
  uris = ['BUCKET_PATH']);
```

### 範例：使用預設連線建立 Iceberg 代管資料表

下列 SQL 運算式會使用預設連線建立 [Iceberg 受管理資料表](https://docs.cloud.google.com/bigquery/docs/iceberg-tables?hl=zh-tw#create-iceberg-tables)：

```
CREATE TABLE `myproject.tpch_clustered.nation` (
  n_nationkey integer,
  n_name string,
  n_regionkey integer,
  n_comment string)
CLUSTER BY n_nationkey
WITH CONNECTION DEFAULT
OPTIONS (
  file_format = 'PARQUET',
  table_format = 'ICEBERG',
  storage_uri = 'gs://mybucket/warehouse/nation');
```

## 使用 `REMOTE WITH CONNECTION DEFAULT` 建立遠端模型

以下範例說明如何在 BigQuery 中指定 `REMOTE WITH CONNECTION DEFAULT`，藉此建立遠端模型。

### 範例：透過 Vertex AI 模型建立遠端模型

下列 SQL 運算式會建立具有預設連線的[遠端模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model?hl=zh-tw)：

```
CREATE OR REPLACE MODEL `mydataset.flash_model`
  REMOTE WITH CONNECTION DEFAULT
  OPTIONS(ENDPOINT = 'gemini-2.0-flash');
```

### 範例：透過 Cloud AI 服務建立遠端模型

下列 SQL 運算式會[透過 Cloud AI 服務建立遠端模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model-service?hl=zh-tw)，並使用預設連線：

```
CREATE MODEL `project_id.mydataset.mymodel`
REMOTE WITH CONNECTION DEFAULT
 OPTIONS(REMOTE_SERVICE_TYPE = 'CLOUD_AI_VISION_V1')
```

### 範例：使用 HTTPS 端點建立遠端模型

下列 SQL 運算式會[建立具有 HTTPS 端點和預設連線的遠端模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model-https?hl=zh-tw)：

```
CREATE MODEL `project_id.mydataset.mymodel`
 INPUT(f1 INT64, f2 FLOAT64, f3 STRING, f4 ARRAY)
 OUTPUT(out1 INT64, out2 INT64)
 REMOTE WITH CONNECTION DEFAULT
 OPTIONS(ENDPOINT = 'https://us-central1-aiplatform.googleapis.com/v1/projects/myproject/locations/us-central1/endpoints/1234')
```

## 後續步驟

* 瞭解 BigQuery 的[預設設定](https://docs.cloud.google.com/bigquery/docs/default-configuration?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-06 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-06 (世界標準時間)。"],[],[]]