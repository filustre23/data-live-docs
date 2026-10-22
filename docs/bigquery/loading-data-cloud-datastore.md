Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 從 Datastore 匯出作業載入資料

BigQuery 可讓您將 Cloud Storage bucket 中的 [Datastore](https://docs.cloud.google.com/datastore?hl=zh-tw) 實體載入 BigQuery 資料表，以便進行分析。使用 Datastore 代管匯入和匯出服務匯出實體後，您可以載入所有實體資料，或選取要匯入的特定屬性。

如要將 Datastore 匯出作業載入 BigQuery，您必須在[匯出指令](https://docs.cloud.google.com/datastore/docs/export-import-entities?hl=zh-tw#exporting_entities)中指定實體篩選器。如要進一步瞭解如何建立及排定匯出作業，請參閱「[匯出及匯入實體](https://docs.cloud.google.com/datastore/docs/export-import-entities?hl=zh-tw)」和「[排定匯出作業](https://docs.cloud.google.com/datastore/docs/schedule-export?hl=zh-tw)」。如要直接查詢匯出檔案，而不將檔案載入 BigQuery，請參閱「[外部資料來源](https://docs.cloud.google.com/bigquery/external-data-sources?hl=zh-tw)」。

## 限制

當您在 BigQuery 中載入 Datastore 匯出檔案中的資料時，請注意下列幾點限制：

* 指定 Datastore 匯出檔案時，您無法在 Cloud Storage URI 中使用萬用字元。
* 從 Datastore 匯出檔案載入資料時，您只能指定一個 Cloud Storage URI。
* 您無法在已定義結構定義的現有資料表中附加 Datastore 匯出資料。
* 如要正確載入 Datastore 匯出作業，匯出資料中的實體必須共用一致的結構定義，且不重複的屬性名稱不得超過 10,000 個。
* 假如不指定實體篩選器，匯出的資料就無法載入 BigQuery。匯出要求的實體篩選器中必須包含一或多個種類名稱。
* Datastore 匯出檔案的欄位大小上限為 64 KB。載入 Datastore 匯出檔案時，大於 64 KB 的所有欄位會遭截斷。

## 事前準備

授予 Identity and Access Management (IAM) 角色，讓使用者具備必要權限，可執行本文件中的各項工作。

### 所需權限

如要將資料載入 BigQuery，您必須具備 IAM 權限，才能執行載入工作，並將資料載入 BigQuery 資料表和分區。如果您是從 Cloud Storage 載入資料，也需要 IAM 權限，才能存取含有資料的 bucket。

#### 將資料載入 BigQuery 的權限

如要將資料載入新的 BigQuery 資料表或分區，或附加或覆寫現有資料表或分區，您必須具備下列 IAM 權限：

* `bigquery.tables.create`
* `bigquery.tables.updateData`
* `bigquery.tables.update`
* `bigquery.jobs.create`

下列各項預先定義的 IAM 角色，都包含將資料載入 BigQuery 資料表或分區所需的權限：

* `roles/bigquery.dataEditor`
* `roles/bigquery.dataOwner`
* `roles/bigquery.admin` (包含 `bigquery.jobs.create` 權限)
* `bigquery.user` (包含 `bigquery.jobs.create` 權限)
* `bigquery.jobUser` (包含 `bigquery.jobs.create` 權限)

此外，如果您具備 `bigquery.datasets.create` 權限，則可在建立的資料集中，使用載入工作建立及更新資料表。

如要進一步瞭解 BigQuery 的 IAM 角色和權限，請參閱「[預先定義的角色和權限](https://docs.cloud.google.com/bigquery/access-control?hl=zh-tw)」。

### 從 Cloud Storage 載入資料的權限

如要取得從 Cloud Storage bucket 載入資料所需的權限，請要求管理員授予您 bucket 的[儲存空間管理員](https://docs.cloud.google.com/iam/docs/roles-permissions/storage?hl=zh-tw#storage.admin)  (`roles/storage.admin`) IAM 角色。如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

這個預先定義的角色具備從 Cloud Storage bucket 載入資料所需的權限。如要查看確切的必要權限，請展開「Required permissions」(必要權限) 部分：

#### 所需權限

您必須具備下列權限，才能從 Cloud Storage bucket 載入資料：

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
3. 在「Explorer」窗格中展開專案，點選「資料集」，然後選取資料集。
4. 在「資料集資訊」部分，點選 add\_box「建立資料表」。
5. 在「建立資料表」窗格中，指定下列詳細資料：

1. 在「Source」(來源) 部分，從「Create table from」(建立資料表來源) 清單中選取「Google Cloud Storage」。接著，按照下列步驟操作：
   1. 從 Cloud Storage bucket 選取檔案，或輸入 [Cloud Storage URI](https://docs.cloud.google.com/bigquery/docs/batch-loading-data?hl=zh-tw#gcs-uri)。您無法在 Google Cloud 控制台中加入多個 URI，但可以使用[萬用字元](https://docs.cloud.google.com/bigquery/docs/batch-loading-data?hl=zh-tw#load-wildcards)。Cloud Storage bucket 必須與資料集位於相同位置，且該資料集包含您要建立、附加或覆寫的資料表。  
       Datastore 匯出檔案的 URI 結尾必須是 `KIND_NAME.export_metadata` 或 `export[NUM].export_metadata`。舉例來說，在 `default_namespace_kind_Book.export_metadata` 中，`Book` 是種類名稱，`default_namespace_kind_Book` 則是 Datastore 產生的檔案名稱。
   2. 在「File format」(檔案格式) 部分，選取「Cloud Datastore Backup」(Cloud Datastore 備份)。
2. 在「Destination」(目的地) 部分，指定下列詳細資料：
   1. 在「Dataset」(資料集) 部分，選取要在其中建立資料表的資料集。
   2. 在「Table」(資料表) 欄位中，輸入要建立的資料表名稱。
   3. 確認「資料表類型」欄位設為「原生資料表」。
3. 在「Schema」(結構定義) 區段中，無需採取任何行動。系統會推論 Datastore 匯出作業的結構定義。
4. 選用：指定**分區和叢集設定**。詳情請參閱「[建立分區資料表](https://docs.cloud.google.com/bigquery/docs/creating-partitioned-tables?hl=zh-tw)」和「[建立及使用分群資料表](https://docs.cloud.google.com/bigquery/docs/creating-clustered-tables?hl=zh-tw)」。
5. 按一下「進階選項」，然後執行下列操作：
   * 讓「Write preference」(寫入偏好設定) 的 [Write if empty] (空白時寫入) 選項維持在已選取狀態。這個選項會建立新資料表，並將資料載入其中。
   * 如要忽略資料列中未出現在資料表結構定義的值，請選取「Unknown values」(不明的值)。
   * 在「Encryption」(加密) 部分，按一下「Customer-managed key」(客戶自行管理的金鑰)，即可使用 [Cloud Key Management Service 金鑰](https://docs.cloud.google.com/bigquery/docs/customer-managed-encryption?hl=zh-tw)。如果保留 **Google-managed key** 設定，BigQuery 會[加密靜態資料](https://docs.cloud.google.com/docs/security/encryption/default-encryption?hl=zh-tw)。
   如要瞭解可用選項，請參閱「[資料儲存庫選項](https://docs.cloud.google.com/bigquery/docs/loading-data-cloud-datastore?hl=zh-tw#cloud_datastore_options)」。
6. 點選「建立資料表」。

### bq

使用 `bq load` 指令，並將 `source_format` 設為 `DATASTORE_BACKUP`。加上 `--location` 旗標，並將該旗標值設為您的[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)。

```
bq --location=LOCATION load \
--source_format=FORMAT \
DATASET.TABLE \
PATH_TO_SOURCE
```

更改下列內容：

* `LOCATION`：您的位置。`--location` 是選用旗標。舉例來說，如果您在東京地區使用 BigQuery，就可以將旗標的值設為 `asia-northeast1`。您可以使用 [.bigqueryrc 檔案](https://docs.cloud.google.com/bigquery/docs/bq-command-line-tool?hl=zh-tw#setting_default_values_for_command-line_flags)設定位置的預設值。
* `FORMAT`: `DATASTORE_BACKUP`.
* `DATASET`：資料集，其中包含您要載入資料的資料表。
* `TABLE`：要載入資料的資料表。如果資料表不存在，系統會建立資料表。
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
3. [來源 URI](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#JobConfigurationLoad.FIELDS.source_uris) 必須完整，格式為 gs://[BUCKET]/[OBJECT]。檔案 (物件) 名稱的結尾必須是 `[KIND_NAME].export_metadata`。您只能為 Datastore 匯出檔案指定一個 URI，且不得使用萬用字元。
4. 將 [`JobConfigurationLoad.sourceFormat` 屬性](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#JobConfigurationLoad.FIELDS.source_format)設為 `DATASTORE_BACKUP`，指定資料格式。

## 將 Datastore 資料附加或覆寫至資料表

將 Datastore 匯出資料載入 BigQuery 時，您可以建立新資料表來儲存資料，也可以覆寫現有資料表。但無法將 Datastore 匯出資料附加至現有資料表。

如果您嘗試將 Datastore 匯出資料附加至現有資料表，就會發生以下錯誤：`Cannot append a datastore backup to a table
that already has a schema. Try using the WRITE_TRUNCATE write disposition to
replace the existing table`。

如要使用 Datastore 匯出資料覆寫現有資料表，請按照下列步驟操作：

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往 BigQuery](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中展開專案，點選「資料集」，然後選取資料集。
4. 在「資料集資訊」部分，點選 add\_box「建立資料表」。
5. 在「建立資料表」窗格中，指定下列詳細資料：

1. 在「Source」(來源) 部分，從「Create table from」(建立資料表來源) 清單中選取「Google Cloud Storage」。接著，按照下列步驟操作：
   1. 從 Cloud Storage bucket 選取檔案，或輸入 [Cloud Storage URI](https://docs.cloud.google.com/bigquery/docs/batch-loading-data?hl=zh-tw#gcs-uri)。您無法在 Google Cloud 控制台中加入多個 URI，但可以使用[萬用字元](https://docs.cloud.google.com/bigquery/docs/batch-loading-data?hl=zh-tw#load-wildcards)。Cloud Storage bucket 必須與資料集位於相同位置，且該資料集包含您要建立、附加或覆寫的資料表。  
       Datastore 匯出檔案的 URI 結尾必須是 `KIND_NAME.export_metadata` 或 `export[NUM].export_metadata`。舉例來說，在 `default_namespace_kind_Book.export_metadata` 中，`Book` 是種類名稱，`default_namespace_kind_Book` 則是 Datastore 產生的檔案名稱。
   2. 在「File format」(檔案格式) 部分，選取「Cloud Datastore Backup」(Cloud Datastore 備份)。
**注意：**附加或覆寫資料表時，可以修改資料表的結構定義。如要進一步瞭解載入作業期間支援的結構定義變更，請參閱「[修改資料表結構定義](https://docs.cloud.google.com/bigquery/docs/managing-table-schemas?hl=zh-tw)」。2. 在「Destination」(目的地) 部分，指定下列詳細資料：
   1. 在「Dataset」(資料集) 部分，選取要在其中建立資料表的資料集。
   2. 在「Table」(資料表) 欄位中，輸入要建立的資料表名稱。
   3. 確認「資料表類型」欄位設為「原生資料表」。
3. 在「Schema」(結構定義) 區段中，無需採取任何行動。系統會推論 Datastore 匯出作業的結構定義。
**注意：**附加或覆寫資料表時，可以修改資料表的結構定義。如要進一步瞭解載入作業期間支援的結構定義變更，請參閱「[修改資料表結構定義](https://docs.cloud.google.com/bigquery/docs/managing-table-schemas?hl=zh-tw)」。4. 選用：指定**分區和叢集設定**。詳情請參閱「[建立分區資料表](https://docs.cloud.google.com/bigquery/docs/creating-partitioned-tables?hl=zh-tw)」和「[建立及使用分群資料表](https://docs.cloud.google.com/bigquery/docs/creating-clustered-tables?hl=zh-tw)」。您無法透過附加或覆寫資料表，將資料表轉換為分區或分群資料表。 Google Cloud 控制台不支援在載入工作中附加或覆寫分區或分群資料表。
5. 按一下「進階選項」，然後執行下列操作：
   * 在「Write preference」(寫入偏好設定) 部分，選擇「Append to table」(附加至資料表) 或「Overwrite table」(覆寫資料表)。
   * 如要忽略資料列中未出現在資料表結構定義的值，請選取「Unknown values」(不明的值)。
   * 在「Encryption」(加密) 部分，按一下「Customer-managed key」(客戶自行管理的金鑰)，即可使用 [Cloud Key Management Service 金鑰](https://docs.cloud.google.com/bigquery/docs/customer-managed-encryption?hl=zh-tw)。如果保留 **Google-managed key** 設定，BigQuery 會[加密靜態資料](https://docs.cloud.google.com/docs/security/encryption/default-encryption?hl=zh-tw)。
   如要瞭解可用選項，請參閱「[資料儲存庫選項](https://docs.cloud.google.com/bigquery/docs/loading-data-cloud-datastore?hl=zh-tw#cloud_datastore_options)」。
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
* `DATASET`：資料集，其中包含您要載入資料的資料表。
* `TABLE`：要覆寫的資料表。
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
3. [來源 URI](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#JobConfigurationLoad.FIELDS.source_uris) 必須完整，格式為 gs://[BUCKET]/[OBJECT]。檔案 (物件) 名稱的結尾必須是 `[KIND_NAME].export_metadata`。您只能為 Datastore 匯出檔案指定一個 URI，且不得使用萬用字元。
4. 將 [`JobConfigurationLoad.sourceFormat` 屬性](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#JobConfigurationLoad.FIELDS.source_format)設為 `DATASTORE_BACKUP`，指定資料格式。
5. 將 [`JobConfigurationLoad.writeDisposition` 屬性](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#JobConfigurationLoad.FIELDS.write_disposition)設為 `WRITE_TRUNCATE`，指定寫入配置。

## Datastore 選項

您可以透過在 API 中設定 [`projectionFields` 屬性](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#JobConfigurationLoad.FIELDS.projection_fields)，或在 bq 指令列工具中使用 `--projection_fields` 旗標，控制 BigQuery 載入哪些屬性，以及如何剖析 Datastore 匯出資料：

| 主控台選項 | bq 工具旗標 | BigQuery API 屬性 | 說明 |
| --- | --- | --- | --- |
| 無法使用 | `--projection_fields` | [projectionFields](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#JobConfigurationLoad.FIELDS.projection_fields) | 逗號分隔的清單，用來指定要從 Datastore 匯出檔案載入至 BigQuery 的實體屬性。屬性名稱區分大小寫，且必須是頂層屬性。如果不指定屬性，BigQuery 會載入所有屬性。如果系統在 Datastore 匯出資料中找不到任一指定屬性，工作結果中就會出現無效錯誤。預設值為 ''。 |

## 資料類型轉換

BigQuery 會將 Datastore 匯出檔案中每個實體的資料轉換為 BigQuery [資料類型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw)。下表說明不同資料類型的轉換對應關係。

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
| 文字字串 | `STRING` (已截斷至 64 KB) |

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

上次更新時間：2026-10-21 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-10-21 (世界標準時間)。"],[],[]]