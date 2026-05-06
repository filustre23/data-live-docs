Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 從 Firestore 匯出檔案載入資料

BigQuery 支援從使用 Firestore [代管的匯入與匯出服務](https://docs.cloud.google.com/firestore/docs/manage-data/export-import?hl=zh-tw)建立的 [Firestore](https://docs.cloud.google.com/firestore?hl=zh-tw) 匯出檔案來載入資料。
代管的匯入與匯出服務會將 Firestore 文件匯出至 Cloud Storage 值區，之後您可以將匯出的資料載入到 BigQuery 表格中。

**注意：** 並非所有 Firestore 匯出內容都能載入。請參閱 BigQuery [限制](#limitations)，建立可載入 BigQuery 資料表的 Firestore 匯出檔案。

## 限制

當您在 BigQuery 中載入 Firestore 匯出檔案中的資料時，請注意下列幾點限制：

* 您的資料集必須與包含匯出檔案的 Cloud Storage 值區位於相同位置。
* 您只能指定一個 Cloud Storage URI，且無法使用 URI 萬用字元。
* Firestore 匯出資料中的文件必須有一致的結構定義，且其中不重複的欄位名稱數量未逾 10,000 個，這樣才能順利載入匯出資料。
* 您可以建立新資料表來儲存資料，也可以覆寫現有資料表，但無法在現有資料表中附加 Firestore 匯出資料。
* 您的[匯出指令](https://docs.cloud.google.com/firestore/docs/manage-data/export-import?hl=zh-tw#export_data)必須指定 `collection-ids` 篩選器。未指定集合 ID 篩選器的匯出資料無法載入 BigQuery。

## 事前準備

授予身分與存取權管理 (IAM) 角色，讓使用者擁有執行本文件各項工作所需的權限。

### 所需權限

如要將資料載入 BigQuery，您需要具備執行載入工作，以及將資料載入 BigQuery 資料表和分區的 IAM 權限。如要從 Cloud Storage 載入資料，您也需要 IAM 權限，才能存取包含資料的值區。

#### 將資料載入 BigQuery 的權限

如要將資料載入新的 BigQuery 資料表或分區，或是附加或覆寫現有的資料表或分區，您需要下列 IAM 權限：

* `bigquery.tables.create`
* `bigquery.tables.updateData`
* `bigquery.tables.update`
* `bigquery.jobs.create`

以下每個預先定義的 IAM 角色都包含將資料載入 BigQuery 資料表或分區所需的權限：

* `roles/bigquery.dataEditor`
* `roles/bigquery.dataOwner`
* `roles/bigquery.admin` (包括 `bigquery.jobs.create` 權限)
* `bigquery.user` (包括 `bigquery.jobs.create` 權限)
* `bigquery.jobUser` (包括 `bigquery.jobs.create` 權限)

此外，如果您具備 `bigquery.datasets.create` 權限，就能在您建立的資料集中，使用載入工作建立及更新資料表。

如要進一步瞭解 BigQuery 中的 IAM 角色和權限，請參閱[預先定義的角色與權限](https://docs.cloud.google.com/bigquery/access-control?hl=zh-tw)一文。

### 從 Cloud Storage 載入資料的權限

如要取得從 Cloud Storage bucket 載入資料所需的權限，請要求管理員授予您 bucket 的「[Storage 管理員](https://docs.cloud.google.com/iam/docs/roles-permissions/storage?hl=zh-tw#storage.admin) 」(`roles/storage.admin`) IAM 角色。如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

這個預先定義的角色具備從 Cloud Storage 值區載入資料所需的權限。如要查看確切的必要權限，請展開「Required permissions」(必要權限) 部分：

#### 所需權限

如要從 Cloud Storage 值區載入資料，您必須具備下列權限：

* `storage.buckets.get`
* `storage.objects.get`
* `storage.objects.list (required if you are using a URI wildcard)`

您或許還可透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)取得這些權限。

## 載入 Firestore 匯出服務資料

您可以使用 Google Cloud 控制台、[bq 指令列工具](https://docs.cloud.google.com/bigquery/docs/bq-command-line-tool?hl=zh-tw)或 [API](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2?hl=zh-tw)，從 Firestore 匯出中繼資料檔案載入資料。

Google Cloud 控制台和 bq 指令列工具中有時會使用 Datastore 術語，不過下列程序與 Firestore 匯出檔案仍會相容。Firestore 與 Datastore 共用一種匯出格式。

**注意：** 使用 bq 指令列工具 中的 [--projection\_fields 旗標](#cloud_firestore_options)，或在 `load` 工作設定 中設定 `projectionFields` 屬性，即可載入特定欄位。

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往 BigQuery](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中展開專案，按一下「Datasets」(資料集)，然後選取資料集。
4. 在「資料集資訊」部分，按一下 add\_box「建立資料表」。
5. 在「建立資料表」窗格中，指定下列詳細資料：

1. 在「來源」部分中，從「建立資料表來源」清單中選取「Google Cloud Storage」。
   接著，按照下列步驟操作：
   1. 從 Cloud Storage bucket 選取檔案，或輸入 [Cloud Storage URI](https://docs.cloud.google.com/bigquery/docs/batch-loading-data?hl=zh-tw#gcs-uri)。
      您無法在 Google Cloud 控制台中加入多個 URI，但支援使用[萬用字元](https://docs.cloud.google.com/bigquery/docs/batch-loading-data?hl=zh-tw#load-wildcards)。Cloud Storage 值區的位置必須與包含您要建立、附加或覆寫之資料表的資料集位置相同。  
       Firestore 匯出檔案的 URI 結尾必須為 `KIND_COLLECTION_ID.export_metadata`。舉例來說，在 `default_namespace_kind_Book.export_metadata` 中，`Book` 是集合 ID，而 `default_namespace_kind_Book` 是 Firestore 產生的檔案名稱。如果 URI 未以 `KIND_COLLECTION_ID.export_metadata` 結尾，您會收到以下錯誤訊息：**does not contain valid backup metadata. (錯誤代碼：invalid)。**

      **注意：**請勿使用以 `overall_export_metadata` 結尾的檔案。BigQuery 無法使用這個檔案。
   2. 在「File format」(檔案格式) 部分中，選取「Cloud Datastore Backup」(Cloud Datastore 備份)。Firestore 和 Datastore 共用匯出格式。
2. 在「目的地」部分，指定下列詳細資料：
   1. 在「Dataset」(資料集) 部分，選取要建立資料表的資料集。
   2. 在「Table」(資料表) 欄位中，輸入要建立的資料表名稱。
   3. 確認「資料表類型」欄位已設為「原生資料表」。
3. 在「Schema」(結構定義) 區段中，無需採取任何行動。系統會推測 Firestore 匯出檔案的結構定義。
4. 選用：指定「分區與叢集設定」。詳情請參閱「[建立分區資料表](https://docs.cloud.google.com/bigquery/docs/creating-partitioned-tables?hl=zh-tw)」和「[建立及使用叢集資料表](https://docs.cloud.google.com/bigquery/docs/creating-clustered-tables?hl=zh-tw)」。
5. 按一下「進階選項」，然後執行下列操作：
   * 讓「Write preference」(寫入偏好設定) 的 [Write if empty] (空白時寫入) 選項維持在已選取狀態。這個選項能建立新的資料表，並將您的資料載入其中。
   * 如要忽略不在資料表結構定義中的資料列值，請選取「Unknown values」(不明的值)。
   * 針對 **Encryption**，請按一下 **Customer-managed key**，以使用 [Cloud Key Management Service key](https://docs.cloud.google.com/bigquery/docs/customer-managed-encryption?hl=zh-tw)。如果您保留 **Google-managed key** 設定，BigQuery 會[加密靜態資料](https://docs.cloud.google.com/docs/security/encryption/default-encryption?hl=zh-tw)。
6. 點選「建立資料表」。

### bq

在 `source_format` 設為 `DATASTORE_BACKUP` 的情況下使用 [`bq load`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_load) 指令。加上 `--location` 標記，並該標記值設為您的[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)。如要覆寫現有資料表，請加上 `--replace` 標記。

如果只要載入特定欄位，請使用 [--projection\_fields 旗標](#cloud_firestore_options)。

```
bq --location=LOCATION load \
--source_format=FORMAT \
DATASET.TABLE \
PATH_TO_SOURCE
```

更改下列內容：

* `LOCATION`：您的位置。`--location` 是選用旗標。
* `FORMAT`：`DATASTORE_BACKUP`。
  [Datastore Backup] (Datastore 備份) 是 Firestore 的所需選項。Firestore 與 Datastore 共用一種匯出格式。
* `DATASET`：特定資料集，該資料集包含您要在當中載入資料的資料表。
* `TABLE`：您要在當中載入資料的資料表。如果該資料表不存在，系統就會建立新資料表。
* `PATH_TO_SOURCE`：[Cloud Storage URI](https://docs.cloud.google.com/bigquery/docs/batch-loading-data?hl=zh-tw#gcs-uri)。

舉例來說，下列指令會在名為 `book_data` 的資料表中載入 `gs://mybucket/20180228T1256/default_namespace/kind_Book/default_namespace_kind_Book.export_metadata` Firestore 匯出檔案。`mybucket` 和 `mydataset` 是在 `US` 多地區位置建立的。

```
bq --location=US load \
--source_format=DATASTORE_BACKUP \
mydataset.book_data \
gs://mybucket/20180228T1256/default_namespace/kind_Book/default_namespace_kind_Book.export_metadata
```

### API

設定下列屬性，以便使用 [API](https://docs.cloud.google.com/bigquery/docs/reference/v2?hl=zh-tw) 載入 Firestore 匯出資料。

1. 建立 `load` 工作設定指向 Cloud Storage 中的來源資料。
2. 在[工作資源](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs?hl=zh-tw)的 `jobReference` 區段中，在 `location` 屬性指定您的[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)。
3. 在載入工作設定中，`sourceUris` 屬性必須完整且符合下列格式：`gs://BUCKET/OBJECT`。檔案 (物件) 名稱的結尾必須是 `KIND_NAME.export_metadata`。您只能針對 Firestore 匯出檔案指定一個 URI，且不得使用萬用字元。
4. 在載入工作設定中，將 `sourceFormat` 屬性設為 `DATASTORE_BACKUP` 以指定資料格式。[Datastore Backup] (Datastore 備份) 是 Firestore 的所需選項。Firestore 與 Datastore 使用相同的匯出格式。
5. 如要僅載入特定欄位，請設定 `projectionFields` 屬性。
6. 如果您要覆寫現有資料表，請將 `writeDisposition` 屬性設為 `WRITE_TRUNCATE` 以指定寫入配置。

### Python

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Python 設定說明操作。詳情請參閱 [BigQuery Python API 參考說明文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
# TODO(developer): Set table_id to the ID of the table to create.
table_id = "your-project.your_dataset.your_table_name"

# TODO(developer): Set uri to the path of the kind export metadata
uri = (
    "gs://cloud-samples-data/bigquery/us-states"
    "/2021-07-02T16:04:48_70344/all_namespaces/kind_us-states"
    "/all_namespaces_kind_us-states.export_metadata"
)

# TODO(developer): Set projection_fields to a list of document properties
#                  to import. Leave unset or set to `None` for all fields.
projection_fields = ["name", "post_abbr"]

from google.cloud import bigquery

# Construct a BigQuery client object.
client = bigquery.Client()

job_config = bigquery.LoadJobConfig(
    source_format=bigquery.SourceFormat.DATASTORE_BACKUP,
    projection_fields=projection_fields,
)

load_job = client.load_table_from_uri(
    uri, table_id, job_config=job_config
)  # Make an API request.

load_job.result()  # Waits for the job to complete.

destination_table = client.get_table(table_id)
print("Loaded {} rows.".format(destination_table.num_rows))
```

**注意：**如果您想略過載入程序，可以將匯出檔案設為外部資料來源，直接查詢匯出檔案。詳情請參閱[外部資料來源](https://docs.cloud.google.com/bigquery/external-data-sources?hl=zh-tw)一文。

## Firestore 選項

如要變更 BigQuery 剖析 Firestore 匯出資料的方式，請指定下列選項：

| Google Cloud 控制台選項 | `bq` 標記 | BigQuery API 屬性 | 說明 |
| --- | --- | --- | --- |
| 無法使用 | `--projection_fields` | `projectionFields` ([Java](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/com.google.cloud.bigquery.DatastoreBackupOptions.Builder?hl=zh-tw#com_google_cloud_bigquery_DatastoreBackupOptions_Builder_setProjectionFields_java_util_List_java_lang_String__)、[Python](https://docs.cloud.google.com/python/docs/reference/bigquery/latest/google.cloud.bigquery.job.LoadJobConfig?hl=zh-tw#google_cloud_bigquery_job_LoadJobConfig_projection_fields)) | (選用) 逗號分隔的清單，用來指定要從 Firestore 匯出檔案載入的文件欄位。根據預設，BigQuery 會載入所有欄位。欄位名稱區分大小寫，且必須存在於匯出檔案中。您無法在 `map.foo` 等對應欄位內指定欄位路徑。 |

## 資料類型轉換

BigQuery 會將 Firestore 匯出檔案中各個文件的資料，轉換成 BigQuery 的[資料類型](https://docs.cloud.google.com/bigquery/docs/schemas?hl=zh-tw#standard_sql_data_types)。下表說明支援的資料類型之間的轉換對應關係。

| Firestore 資料類型 | BigQuery 資料類型 |
| --- | --- |
| 陣列 | RECORD |
| 布林值 | BOOLEAN |
| 參考資料 | RECORD |
| 日期和時間 | TIMESTAMP |
| 對應 | RECORD |
| 浮點數 | FLOAT |
| 地理點 | RECORD     ``` [{"lat","FLOAT"},  {"long","FLOAT"}] ``` |
| 整數 | INTEGER |
| 字串 | STRING (截斷至 64 KB) |

## Firestore 金鑰屬性

Firestore 中每個文件都有專屬金鑰，當中包含文件 ID 和文件路徑等資訊。
BigQuery 會為金鑰建立 `RECORD` 資料類型 (也稱為 [`STRUCT`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#struct_type))，並透過巢狀欄位整理不同類型的資訊，如下表所示。

| 金鑰屬性 | 說明 | BigQuery 資料類型 |
| --- | --- | --- |
| `__key__.app` | Firestore 應用程式名稱。 | STRING |
| `__key__.id` | 文件的 ID；如有設定 `__key__.name`，則為 `null`。 | INTEGER |
| `__key__.kind` | 文件的集合 ID。 | STRING |
| `__key__.name` | 文件的名稱；如有設定 `__key__.id`，則為 `null`。 | STRING |
| `__key__.namespace` | Firestore 不支援自訂命名空間。預設命名空間會以空白字串表示。 | 字串 |
| `__key__.path` | 文件的路徑：文件的序列與根集合的集合配對。例如 `"Country", "USA", "PostalCode", 10011, "Route", 1234`。 | STRING |




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-05 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-05 (世界標準時間)。"],[],[]]