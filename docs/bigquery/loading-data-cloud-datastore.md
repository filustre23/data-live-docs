* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 從 Datastore 匯出檔案載入資料

對於使用 Datastore 代管的匯入與匯出服務建立的 [Datastore](https://docs.cloud.google.com/datastore?hl=zh-tw) 匯出檔案，BigQuery 支援從這類檔案載入資料的功能。您可以使用代管匯入和匯出服務，將 Datastore 實體匯出至 Cloud Storage 值區。然後在 BigQuery 中以資料表的形式載入匯出檔案。

如要瞭解如何建立 Datastore 匯出檔案，請參閱 Datastore 說明文件中的[匯出與匯入實體](https://docs.cloud.google.com/datastore/docs/export-import-entities?hl=zh-tw)一文。關於如何排定匯出時程，請參閱[排定匯出時程](https://docs.cloud.google.com/datastore/docs/schedule-export?hl=zh-tw)一文。

**附註：**如要將 Datastore 匯出檔案載入 BigQuery，您必須在[匯出指令](https://docs.cloud.google.com/datastore/docs/export-import-entities?hl=zh-tw#exporting_entities)中指定實體篩選器。
假如不指定實體篩選器，匯出的資料就無法載入 BigQuery。

您可以在 API 中設定 [`projectionFields` 屬性](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#JobConfigurationLoad.FIELDS.projection_fields)，或是在 bq 指令列工具中使用 `--projection_fields` 旗標，來控制 BigQuery 要載入的屬性。

如果您想略過載入程序，可以將匯出檔案設為外部資料來源，直接查詢匯出檔案。詳情請參閱[外部資料來源](https://docs.cloud.google.com/bigquery/external-data-sources?hl=zh-tw)。

將資料從 Cloud Storage 載入 BigQuery 資料表時，該資料表所屬的資料集必須位於和 Cloud Storage 值區相同的地區或多地區。

## 限制

當您在 BigQuery 中載入 Datastore 匯出檔案中的資料時，請注意下列幾點限制：

* 指定 Datastore 匯出檔案時，您無法在 Cloud Storage URI 中使用萬用字元。
* 從 Datastore 匯出檔案載入資料時，您只能指定一個 Cloud Storage URI。
* 您無法在已定義結構定義的現有資料表中附加 Datastore 匯出資料。
* Datastore 匯出資料中的實體必須有一致的結構定義，且其中不重複的屬性名稱數量未逾 10,000 個，這樣才能順利載入匯出資料。
* 假如不指定實體篩選器，匯出的資料就無法載入 BigQuery。匯出要求的實體篩選器中必須包含一或多個種類名稱。
* Datastore 匯出檔案的欄位大小上限為 64 KB。載入 Datastore 匯出檔案時，大於 64 KB 的所有欄位會遭截斷。

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

## 載入 Datastore 匯出服務資料

如何從 Datastore 匯出中繼資料檔案載入資料：

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
      您無法在 Google Cloud 控制台中加入多個 URI，但支援使用[萬用字元](https://docs.cloud.google.com/bigquery/docs/batch-loading-data?hl=zh-tw#load-wildcards)。Cloud Storage 值區的位置必須與要建立、附加或覆寫的表格所在的資料集位置相同。
        
       Datastore 匯出檔案的 URI 結尾必須為 `KIND_NAME.export_metadata` 或 `export[NUM].export_metadata`。舉例來說，在 `default_namespace_kind_Book.export_metadata` 中，`Book` 是種類名稱，而 `default_namespace_kind_Book` 是 Datastore 產生的檔案名稱。
   2. 在「File format」(檔案格式) 部分，選取「Cloud Datastore Backup」(Cloud Datastore 備份)。
2. 在「目的地」部分，指定下列詳細資料：
   1. 在「Dataset」(資料集) 部分，選取要建立資料表的資料集。
   2. 在「Table」(資料表) 欄位中，輸入要建立的資料表名稱。
   3. 確認「資料表類型」欄位已設為「原生資料表」。
3. 在「Schema」(結構定義) 區段中，無需採取任何行動。系統會推測 Datastore 匯出檔案的結構定義。
4. 選用：指定「分區與叢集設定」。詳情請參閱「[建立分區資料表](https://docs.cloud.google.com/bigquery/docs/creating-partitioned-tables?hl=zh-tw)」和「[建立及使用叢集資料表](https://docs.cloud.google.com/bigquery/docs/creating-clustered-tables?hl=zh-tw)」。
5. 按一下「進階選項」，然後執行下列操作：
   * 讓「Write preference」(寫入偏好設定) 的 [Write if empty] (空白時寫入) 選項維持在已選取狀態。這個選項能建立新的資料表，並將您的資料載入其中。
   * 如要忽略不在資料表結構定義中的資料列值，請選取「Unknown values」(不明的值)。
   * 針對「Encryption」(加密)，請按一下「Customer-managed key」(客戶管理的金鑰)，以使用 [Cloud Key Management Service 金鑰](https://docs.cloud.google.com/bigquery/docs/customer-managed-encryption?hl=zh-tw)。如果您保留 **Google-managed key** 設定，BigQuery 會[加密靜態資料](https://docs.cloud.google.com/docs/security/encryption/default-encryption?hl=zh-tw)。
   如要瞭解可用的選項，請參閱「[Datastore 選項](https://docs.cloud.google.com/bigquery/docs/loading-data-cloud-datastore?hl=zh-tw#cloud_datastore_options)」。
6. 點選「建立資料表」。

### bq

在 `source_format` 設為 `DATASTORE_BACKUP` 的情況下使用 `bq load` 指令。加上 `--location` 旗標，並將該旗標值設為您的[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)。

```
bq --location=LOCATION load \
--source_format=FORMAT \
DATASET.TABLE \
PATH_TO_SOURCE
```

更改下列內容：

* `LOCATION`：您的位置。`--location` 是選用旗標。舉例來說，如果您在東京地區使用 BigQuery，就可以將旗標的值設為 `asia-northeast1`。您可以使用 [.bigqueryrc 檔案](https://docs.cloud.google.com/bigquery/docs/bq-command-line-tool?hl=zh-tw#setting_default_values_for_command-line_flags)設定位置的預設值。
* `FORMAT`: `DATASTORE_BACKUP`.
* `DATASET`：包含您要載入資料的資料表。
* `TABLE`：您要在當中載入資料的資料表。如果該資料表不存在，系統就會建立新資料表。
* `PATH_TO_SOURCE`：[Cloud Storage URI](https://docs.cloud.google.com/bigquery/docs/batch-loading-data?hl=zh-tw#gcs-uri)。

舉例來說，下列指令會在名為 `book_data` 的資料表中載入 `gs://mybucket/20180228T1256/default_namespace/kind_Book/default_namespace_kind_Book.export_metadata` Datastore 匯出檔案。`mybucket` 和 `mydataset` 是在 `US` 多地區位置建立的。

```
bq --location=US load \
--source_format=DATASTORE_BACKUP \
mydataset.book_data \
gs://mybucket/20180228T1256/default_namespace/kind_Book/default_namespace_kind_Book.export_metadata
```

### API

設定下列屬性，以便使用 [API](https://docs.cloud.google.com/bigquery/docs/reference/v2?hl=zh-tw) 載入 Datastore 匯出資料。

1. 建立指向 Cloud Storage 中來源資料的[載入工作](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#jobconfigurationload)。
2. 在[工作資源](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs?hl=zh-tw)的 `jobReference` 區段中，在 `location` 屬性指定您的[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)。
3. [來源 URI](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#JobConfigurationLoad.FIELDS.source_uris) 必須完整且符合下列格式：gs://[BUCKET]/[OBJECT]。檔案 (物件) 名稱的結尾必須是 `[KIND_NAME].export_metadata`。您只能為 Datastore 匯出檔案指定一個 URI，且不得使用萬用字元。
4. 將 [`JobConfigurationLoad.sourceFormat` 屬性設為 `DATASTORE_BACKUP`，以指定資料格式。](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#JobConfigurationLoad.FIELDS.source_format)

## 將 Datastore 資料附加或覆寫至資料表

將 Datastore 匯出資料載入 BigQuery 時，您可以建立新資料表來儲存資料，也可以覆寫現有資料表。但無法將 Datastore 匯出資料附加至現有資料表。

如果您嘗試將 Datastore 匯出資料附加至現有資料表，就會發生以下錯誤：`Cannot append a datastore backup to a table
that already has a schema. Try using the WRITE_TRUNCATE write disposition to
replace the existing table`。

如何使用 Datastore 匯出資料覆寫現有資料表：

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
      您無法在 Google Cloud 控制台中加入多個 URI，但支援使用[萬用字元](https://docs.cloud.google.com/bigquery/docs/batch-loading-data?hl=zh-tw#load-wildcards)。Cloud Storage 值區的位置必須與要建立、附加或覆寫的表格所在的資料集位置相同。
        
       Datastore 匯出檔案的 URI 結尾必須為 `KIND_NAME.export_metadata` 或 `export[NUM].export_metadata`。舉例來說，在 `default_namespace_kind_Book.export_metadata` 中，`Book` 是種類名稱，而 `default_namespace_kind_Book` 是 Datastore 產生的檔案名稱。
   2. 在「File format」(檔案格式) 部分，選取「Cloud Datastore Backup」(Cloud Datastore 備份)。
**注意：**您可以在附加或覆寫資料表時修改資料表的結構定義。如要進一步瞭解載入作業期間支援的結構定義變更，請參閱「[修改資料表結構定義](https://docs.cloud.google.com/bigquery/docs/managing-table-schemas?hl=zh-tw)」一文。
2. 在「目的地」部分，指定下列詳細資料：
   1. 在「Dataset」(資料集) 部分，選取要建立資料表的資料集。
   2. 在「Table」(資料表) 欄位中，輸入要建立的資料表名稱。
   3. 確認「資料表類型」欄位已設為「原生資料表」。
3. 在「Schema」(結構定義) 區段中，無需採取任何行動。系統會推測 Datastore 匯出檔案的結構定義。
**注意：**您可以在附加或覆寫資料表時修改資料表的結構定義。如要進一步瞭解載入作業期間支援的結構定義變更，請參閱[修改資料表結構定義](https://docs.cloud.google.com/bigquery/docs/managing-table-schemas?hl=zh-tw)。4. 選用：指定「分區與叢集設定」。詳情請參閱「[建立分區資料表](https://docs.cloud.google.com/bigquery/docs/creating-partitioned-tables?hl=zh-tw)」和「[建立及使用叢集資料表](https://docs.cloud.google.com/bigquery/docs/creating-clustered-tables?hl=zh-tw)」。您無法藉由附加或覆寫的方式，將資料表轉換為分區資料表或叢集資料表。 Google Cloud 控制台不支援在載入工作中，對分區或叢集資料表執行附加或覆寫作業。
5. 按一下「進階選項」，然後執行下列操作：
   * 針對「Write preference」(寫入偏好設定)，請選擇「Append to table」(附加到資料表中) 或「Overwrite table」(覆寫資料表)。
   * 如要忽略不在資料表結構定義中的資料列值，請選取「Unknown values」(不明的值)。
   * 針對「Encryption」(加密)，請按一下「Customer-managed key」(客戶管理的金鑰)，以使用 [Cloud Key Management Service 金鑰](https://docs.cloud.google.com/bigquery/docs/customer-managed-encryption?hl=zh-tw)。如果您保留 **Google-managed key** 設定，BigQuery 會[加密靜態資料](https://docs.cloud.google.com/docs/security/encryption/default-encryption?hl=zh-tw)。
   如要瞭解可用的選項，請參閱「[Datastore 選項](https://docs.cloud.google.com/bigquery/docs/loading-data-cloud-datastore?hl=zh-tw#cloud_datastore_options)」。
6. 點選「建立資料表」。

### bq

請使用 `bq load` 指令搭配 `--replace` 旗標，並將 `source_format` 設為 `DATASTORE_BACKUP`。加上 `--location` 旗標，並將該旗標值設為您的[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)。

```
bq --location=LOCATION load \
--source_format=FORMAT \
--replace \
DATASET.TABLE \
PATH_TO_SOURCE
```

更改下列內容：

* `LOCATION`：您的位置。`--location` 是選用旗標。舉例來說，如果您在東京地區使用 BigQuery，就可以將旗標的值設為 `asia-northeast1`。您可以使用 [.bigqueryrc 檔案](https://docs.cloud.google.com/bigquery/docs/bq-command-line-tool?hl=zh-tw#setting_default_values_for_command-line_flags)設定位置的預設值。
* `FORMAT`: `DATASTORE_BACKUP`.
* `DATASET`：包含您要載入資料的資料表所屬的資料集。
* `TABLE`：您要覆寫的資料表。
* `PATH_TO_SOURCE`：[Cloud Storage URI](https://docs.cloud.google.com/bigquery/docs/batch-loading-data?hl=zh-tw#gcs-uri)。

舉例來說，下列指令會在名為 `book_data` 的資料表中載入 `gs://mybucket/20180228T1256/default_namespace/kind_Book/default_namespace_kind_Book.export_metadata` Datastore 匯出檔案。

```
bq load --source_format=DATASTORE_BACKUP \
--replace \
mydataset.book_data \
gs://mybucket/20180228T1256/default_namespace/kind_Book/default_namespace_kind_Book.export_metadata
```

### API

設定下列屬性，以便使用 [API](https://docs.cloud.google.com/bigquery/docs/reference/v2?hl=zh-tw) 載入資料。

1. 建立指向 Cloud Storage 中來源資料的[載入工作](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#jobconfigurationload)。
2. 在[工作資源](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs?hl=zh-tw)的 `jobReference` 區段中，在 `location` 屬性指定您的[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)。
3. [來源 URI](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#JobConfigurationLoad.FIELDS.source_uris) 必須完整且符合下列格式：gs://[BUCKET]/[OBJECT]。檔案 (物件) 名稱的結尾必須是 `[KIND_NAME].export_metadata`。您只能為 Datastore 匯出檔案指定一個 URI，且不得使用萬用字元。
4. 將 [`JobConfigurationLoad.sourceFormat` 屬性設為 `DATASTORE_BACKUP`，以指定資料格式。](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#JobConfigurationLoad.FIELDS.source_format)
5. 將 [`JobConfigurationLoad.writeDisposition` 屬性](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#JobConfigurationLoad.FIELDS.write_disposition)設為 `WRITE_TRUNCATE`，藉此指定寫入配置。

## Datastore 選項

如要變更 BigQuery 剖析 Datastore 匯出資料的方式，請指定下列選項：

| 主控台選項 | bq 工具標記 | BigQuery API 屬性 | 說明 |
| --- | --- | --- | --- |
| 無法使用 | `--projection_fields` | [projectionFields](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#JobConfigurationLoad.FIELDS.projection_fields) | 逗號分隔的清單，用來指定要從 Datastore 匯出檔案載入至 BigQuery 的實體屬性。屬性名稱有大小寫之分，且必須為頂層屬性。如果不指定屬性，BigQuery 會載入所有屬性。如果系統在 Datastore 匯出資料中找不到任一指定屬性，工作結果中就會出現無效錯誤。預設值為 ''。 |

## 資料類型轉換

BigQuery 會將 Datastore 匯出檔案中各個實體的資料，轉換成 BigQuery 的[資料類型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw)。下表說明不同資料類型的轉換對應關係。

| Datastore 資料類型 | BigQuery 資料類型 |
| --- | --- |
| 陣列 | `ARRAY` |
| Blob | `BYTES` |
| 布林值 | `BOOLEAN` |
| 日期與時間 | `TIMESTAMP` |
| 嵌入實體 | `RECORD` |
| 浮點數 | `FLOAT` |
| 地理點 | `RECORD`     ``` [{"lat","DOUBLE"},  {"long","DOUBLE"}] ``` |
| 整數 | `INTEGER` |
| 鍵 | `RECORD` |
| 空值 | `STRING` |
| 文字字串 | `STRING` (截斷至 64 KB) |

## Datastore 金鑰屬性

Datastore 中每個實體都有專屬金鑰，當中包含命名空間和路徑等資訊。BigQuery 會為每個金鑰建立 `RECORD` 類型的資料，並透過巢狀欄位整理不同類型的資訊 (如下表所示)。

| 金鑰屬性 | 說明 | BigQuery 資料類型 |
| --- | --- | --- |
| `__key__.app` | Datastore 應用程式名稱。 | STRING |
| `__key__.id` | 實體的 ID，或設定 `__key__.name` 時則為 `null`。 | INTEGER |
| `__key__.kind` | 實體的種類。 | STRING |
| `__key__.name` | 實體的名稱，或設定 `__key__.id` 時則為 `null`。 | STRING |
| `__key__.namespace` | 如果 Datastore 應用程式使用自訂命名空間，這個屬性就是實體的命名空間。如果未使用自訂命名空間，則會以空白字串代表預設命名空間。 | STRING |
| `__key__.path` | 經過整併的[實體祖系路徑](https://docs.cloud.google.com/appengine/docs/java/datastore/entities?hl=zh-tw#Java_Ancestor_paths)，其中包含一系列根實體和實體本身等項目的種類-識別碼組合，例如：`"Country", "USA", "PostalCode", 10011, "Route", 1234`。 | STRING |




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-04-30 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-04-30 (世界標準時間)。"],[],[]]