Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 建立物件資料表

本文說明如何建立[物件資料表](https://docs.cloud.google.com/bigquery/docs/object-table-introduction?hl=zh-tw)，讓 BigQuery 存取 Cloud Storage 中的非結構化資料。

如要建立物件表格，請完成下列工作：

1. 建立[資料集](https://docs.cloud.google.com/bigquery/docs/datasets-intro?hl=zh-tw)，內含物件資料表。
2. 建立「連線」，從 Cloud Storage 讀取物件資訊。
3. 將「Storage 物件檢視者」角色 (`roles/storage.objectViewer`) 授予與連線相關聯的服務帳戶。
4. 使用 [`CREATE EXTERNAL TABLE` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#create_external_table_statement)建立物件資料表，並將其與連線建立關聯。

## 事前準備

- 登入 Google Cloud 帳戶。如果您是 Google Cloud新手，歡迎[建立帳戶](https://console.cloud.google.com/freetrial?hl=zh-tw)，親自評估產品在實際工作環境中的成效。新客戶還能獲得價值 $300 美元的免費抵免額，可用於執行、測試及部署工作負載。
- In the Google Cloud console, on the project selector page,
  select or create a Google Cloud project.

  **Roles required to select or create a project**

  * **Select a project**: Selecting a project doesn't require a specific
    IAM role—you can select any project that you've been
    granted a role on.
  * **Create a project**: To create a project, you need the Project Creator role
    (`roles/resourcemanager.projectCreator`), which contains the
    `resourcemanager.projects.create` permission. [Learn how to grant
    roles](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw).
  **Note**: If you don't plan to keep the
  resources that you create in this procedure, create a project instead of
  selecting an existing project. After you finish these steps, you can
  delete the project, removing all resources associated with the project.

  [Go to project selector](https://console.cloud.google.com/projectselector2/home/dashboard?hl=zh-tw)
- [Verify that billing is enabled for your Google Cloud project](https://docs.cloud.google.com/billing/docs/how-to/verify-billing-enabled?hl=zh-tw#confirm_billing_is_enabled_on_a_project).
- Enable the BigQuery and BigQuery Connection API APIs.

  **Roles required to enable APIs**

  To enable APIs, you need the Service Usage Admin IAM
  role (`roles/serviceusage.serviceUsageAdmin`), which
  contains the `serviceusage.services.enable` permission. [Learn how to grant
  roles](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw).

  [Enable the APIs](https://console.cloud.google.com/apis/enableflow?apiid=bigquery.googleapis.com%2Cbigqueryconnection.googleapis.com&hl=zh-tw)

- In the Google Cloud console, on the project selector page,
  select or create a Google Cloud project.

  **Roles required to select or create a project**

  * **Select a project**: Selecting a project doesn't require a specific
    IAM role—you can select any project that you've been
    granted a role on.
  * **Create a project**: To create a project, you need the Project Creator role
    (`roles/resourcemanager.projectCreator`), which contains the
    `resourcemanager.projects.create` permission. [Learn how to grant
    roles](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw).
  **Note**: If you don't plan to keep the
  resources that you create in this procedure, create a project instead of
  selecting an existing project. After you finish these steps, you can
  delete the project, removing all resources associated with the project.

  [Go to project selector](https://console.cloud.google.com/projectselector2/home/dashboard?hl=zh-tw)
- [Verify that billing is enabled for your Google Cloud project](https://docs.cloud.google.com/billing/docs/how-to/verify-billing-enabled?hl=zh-tw#confirm_billing_is_enabled_on_a_project).
- Enable the BigQuery and BigQuery Connection API APIs.

  **Roles required to enable APIs**

  To enable APIs, you need the Service Usage Admin IAM
  role (`roles/serviceusage.serviceUsageAdmin`), which
  contains the `serviceusage.services.enable` permission. [Learn how to grant
  roles](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw).

  [Enable the APIs](https://console.cloud.google.com/apis/enableflow?apiid=bigquery.googleapis.com%2Cbigqueryconnection.googleapis.com&hl=zh-tw)

## 必要的角色

如要建立物件表格，您必須具備專案的下列角色：

* 如要建立資料集和資料表，您必須具備 BigQuery 資料編輯者 (`roles/bigquery.dataEditor`) 角色。
* 如要建立連線，您必須具備 BigQuery 連線管理員 (`roles/bigquery.connectionAdmin`) 角色。
* 如要將角色授予連線的服務帳戶，您必須具備專案 IAM 管理員 (`roles/resourcemanager.projectIamAdmin`) 角色。

如要[查詢物件資料表](#query-object-tables)，您必須具備專案的下列角色：

* BigQuery 資料檢視者 (`roles/bigquery.dataViewer`) 角色
* BigQuery Connection 使用者 (`roles/bigquery.connectionUser`) 角色

如要查看確切的必要權限，請展開「Required permissions」(必要權限) 部分：

#### 所需權限

* `bigquery.datasets.create`
* `bigquery.tables.create`
* `bigquery.tables.update`
* `bigquery.connections.create`
* `bigquery.connections.get`
* `bigquery.connections.list`
* `bigquery.connections.update`
* `bigquery.connections.use`
* `bigquery.connections.delete`
* `bigquery.connections.delegate`
* `storage.bucket.*`
* `storage.object.*`
* `bigquery.jobs.create`
* `bigquery.tables.get`
* `bigquery.tables.getData`
* `bigquery.readsessions.create`

您或許還可透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)取得這些權限。

**注意：**僅查詢資料的使用者**不應**具備下列權限：

* 可直接從 Cloud Storage 讀取物件，這項權限由「Storage 物件檢視者」角色授予。
* 將資料表繫結至連線的權限，由 BigQuery 連線管理員角色授予。

否則，使用者可以建立沒有任何存取權控管機制的新物件資料表，規避資料倉儲管理員設定的控管機制。

## 建立資料集

建立 BigQuery 資料集，內含物件資料表：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。

   如果沒有看到左側窗格，請按一下 last\_page「Expand left pane」(展開左側窗格)，開啟窗格。
3. 在「Explorer」窗格中，按一下專案名稱。
4. 依序點按 more\_vert「View actions」(查看動作) >「Create dataset」(建立資料集)。
5. 在「建立資料集」頁面中，執行下列操作：

   1. 在「Dataset ID」(資料集 ID) 部分，輸入資料集的名稱。
   2. 在「位置類型」部分，選取「區域」或「多區域」。

      * 如果選取「區域」，請從「區域」清單中選取位置。
      * 如果選取「多區域」，請從「多區域」清單中選取「美國」或「歐洲」。
   3. 點選「建立資料集」。

## 建立連線

如果已設定預設連線，或您具備 BigQuery 管理員角色，可以略過這個步驟。

為物件資料表建立要使用的[Cloud 資源連結](https://docs.cloud.google.com/bigquery/docs/create-cloud-resource-connection?hl=zh-tw)，並取得連線的服務帳戶。

1. 前往「BigQuery」頁面

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中，點選「新增資料」add。

   「新增資料」對話方塊隨即開啟。
4. 在「依條件篩選」窗格的「資料來源類型」部分，選取「商用應用程式」。

   或者，您也可以在「Search for data sources」(搜尋資料來源) 欄位中輸入 `Vertex AI`。
5. 在「精選資料來源」部分，點選「Vertex AI」。
6. 按一下「Vertex AI Models: BigQuery Federation」解決方案資訊卡。
7. 在「連線類型」清單中，選取「Vertex AI 遠端模型、遠端函式、BigLake 和 Spanner (Cloud 資源)」。
8. 在「連線 ID」欄位中，輸入連線名稱。
9. 在「位置類型」部分，選取「區域」或「多區域」。

   * 如果選取「區域」，請從「區域」清單中選取位置。
   * 如果選取「多區域」，請從「多區域」清單中選取「美國」或「歐洲」。
10. 點選「建立連線」。
11. 點選「前往連線」。
12. 在「連線資訊」窗格中，複製服務帳戶 ID，以供後續步驟使用。

### 授予服務帳戶存取權

為連線的服務帳戶授予「Storage 物件檢視者」角色：

### 控制台

1. 前往「IAM & Admin」(IAM 與管理) 頁面。

   [前往「IAM & Admin」(IAM 與管理)](https://console.cloud.google.com/project/_/iam-admin?hl=zh-tw)
2. 按一下「新增」person\_add。

   「新增主體」對話方塊隨即開啟。
3. 在「新增主體」欄位，輸入先前複製的服務帳戶 ID。
4. 在「Select a role」(請選擇角色) 欄位中，依序選取「Cloud Storage」和「Storage Object Viewer」(Storage 物件檢視者)。
5. 按一下 [儲存]。

### gcloud

使用 [`gcloud projects add-iam-policy-binding`](https://docs.cloud.google.com/sdk/gcloud/reference/projects/add-iam-policy-binding?hl=zh-tw) 指令。

```
gcloud projects add-iam-policy-binding 'PROJECT_NUMBER' --member='serviceAccount:MEMBER' --role='roles/storage.objectViewer' --condition=None
```

請替換下列項目：

* `PROJECT_NUMBER`：要授予角色的專案編號。
* `MEMBER`：您先前複製的服務帳戶 ID。

## 建立物件資料表

如要建立物件資料表，請按照下列步驟操作：

### SQL

使用 [`CREATE EXTERNAL TABLE` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#create_external_table_statement)。

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列陳述式：

   ```
   CREATE EXTERNAL TABLE `PROJECT_ID.DATASET_ID.TABLE_NAME`
   WITH CONNECTION {`PROJECT_ID.REGION.CONNECTION_ID`| DEFAULT}
   OPTIONS(
     object_metadata = 'SIMPLE',
     uris = ['BUCKET_PATH'[,...]],
     max_staleness = STALENESS_INTERVAL,
     metadata_cache_mode = 'CACHE_MODE');
   ```

   請替換下列項目：

   * `PROJECT_ID`：您的專案 ID。
   * `DATASET_ID`：要包含物件表格的資料集 ID。
   * `TABLE_NAME`：物件資料表的名稱。
   * `REGION`：包含連線的[區域或多區域](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw#supported_locations)。
   * `CONNECTION_ID`：要用於這個物件資料表的[Cloud 資源連結](https://docs.cloud.google.com/bigquery/docs/connections-api-intro?hl=zh-tw) ID。連線會決定用來從 Cloud Storage 讀取資料的服務帳戶。

     在 Google Cloud 控制台中[查看連線詳細資料](https://docs.cloud.google.com/bigquery/docs/working-with-connections?hl=zh-tw#view-connections)時，連線 ID 是「連線 ID」中顯示的完整連線 ID 最後一個區段的值，例如 `projects/myproject/locations/connection_location/connections/myconnection`。

     如要使用[預設連線](https://docs.cloud.google.com/bigquery/docs/default-connections?hl=zh-tw)，請指定 `DEFAULT`，而不是包含 PROJECT\_ID.REGION.CONNECTION\_ID 的連線字串。
   * `BUCKET_PATH`：Cloud Storage bucket 的路徑，其中包含物件表格代表的物件，格式為 `['gs://bucket_name/[folder_name/]*']`。

     您可以在每個路徑中使用一個星號 (`*`) 萬用字元，限制物件表格中包含的物件。舉例來說，如果 bucket 包含多種非結構化資料，您可以只指定 `['gs://bucket_name/*.pdf']`，為 PDF 物件建立物件資料表。詳情請參閱「[Cloud Storage URI 的萬用字元支援](https://docs.cloud.google.com/bigquery/docs/external-data-cloud-storage?hl=zh-tw#wildcard-support)」。

     您可以提供多個路徑，為 `uris` 選項指定多個值區，例如 `['gs://mybucket1/*', 'gs://mybucket2/folder5/*']`。

     如要進一步瞭解如何在 BigQuery 中使用 Cloud Storage URI，請參閱「[Cloud Storage 資源路徑](https://docs.cloud.google.com/bigquery/docs/external-data-cloud-storage?hl=zh-tw#google-cloud-storage-uri)」。
   * `STALENESS_INTERVAL`：指定針對物件資料表執行的作業是否使用快取中繼資料，以及作業必須使用多新的快取中繼資料。如要進一步瞭解中繼資料快取注意事項，請參閱「[中繼資料快取，提升效能](https://docs.cloud.google.com/bigquery/docs/object-table-introduction?hl=zh-tw#metadata_caching_for_performance)」。

     如要停用中繼資料快取功能，請指定 0。這是目前的預設做法。

     如要啟用中繼資料快取功能，請指定介於 30 分鐘至 7 天之間的[間隔常值](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/lexical?hl=zh-tw#interval_literals)。舉例來說，如要指定 4 小時的過時間隔，請輸入 `INTERVAL 4 HOUR`。如果資料表在過去 4 小時內重新整理過，針對資料表執行的作業就會使用快取中繼資料。如果快取中繼資料的建立時間早於該時間，作業會改為從 Cloud Storage 擷取中繼資料。
   * `CACHE_MODE`：指定中繼資料快取是否自動或手動重新整理。如要進一步瞭解中繼資料快取注意事項，請參閱「[中繼資料快取，提升效能](https://docs.cloud.google.com/bigquery/docs/object-table-introduction?hl=zh-tw#metadata_caching_for_performance)」。

     設為 `AUTOMATIC`，中繼資料快取就會以系統定義的時間間隔 (通常為 30 到 60 分鐘) 重新整理。

     如要依您決定的時間表重新整理中繼資料快取，請設為 `MANUAL`。在這種情況下，您可以呼叫 [`BQ.REFRESH_EXTERNAL_METADATA_CACHE` 系統程序](https://docs.cloud.google.com/bigquery/docs/reference/system-procedures?hl=zh-tw#bqrefresh_external_metadata_cache)來重新整理快取。

     如果 `STALENESS_INTERVAL` 設為大於 0 的值，您就必須設定 `CACHE_MODE`。
3. 按一下「執行」play\_circle。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

**範例**

下列範例會建立物件資料表，並將中繼資料快取過時間隔設為 1 天：

```
CREATE EXTERNAL TABLE `my_dataset.object_table`
WITH CONNECTION `us.my-connection`
OPTIONS(
  object_metadata = 'SIMPLE',
  uris = ['gs://mybucket/*'],
  max_staleness = INTERVAL 1 DAY,
  metadata_cache_mode = 'AUTOMATIC'
);
```

下列範例會針對三個 Cloud Storage 值區中的物件建立物件資料表：

```
CREATE EXTERNAL TABLE `my_dataset.object_table`
WITH CONNECTION `us.my-connection`
OPTIONS(
  object_metadata = 'SIMPLE',
  uris = ['gs://bucket1/*','gs://bucket2/folder1/*','gs://bucket3/*']
);
```

下列範例會針對 Cloud Storage bucket 中的 PDF 物件建立物件資料表：

```
CREATE EXTERNAL TABLE `my_dataset.object_table`
WITH CONNECTION `us.my-connection`
OPTIONS(
  object_metadata = 'SIMPLE',
  uris = ['gs://bucket1/*.pdf']
);
```

### bq

使用 [`bq mk`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#mk-table) 指令。

```
bq mk --table \
--external_table_definition=BUCKET_PATH@REGION.CONNECTION_ID \
--object_metadata=SIMPLE \
--max_staleness=STALENESS_INTERVAL \
--metadata_cache_mode=CACHE_MODE \
PROJECT_ID:DATASET_ID.TABLE_NAME
```

請替換下列項目：

* `PROJECT_ID`：您的專案 ID。
* `DATASET_ID`：要包含物件表格的資料集 ID。
* `TABLE_NAME`：物件資料表的名稱。
* `REGION`：包含連線的[區域或多區域](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw#supported_locations)。
* `CONNECTION_ID`：要用於這個外部資料表的[Cloud 資源連結](https://docs.cloud.google.com/bigquery/docs/working-with-connections?hl=zh-tw) ID。連線會決定用來從 Cloud Storage 讀取資料的服務帳戶。

  在 Google Cloud 控制台中[查看連線詳細資料](https://docs.cloud.google.com/bigquery/docs/working-with-connections?hl=zh-tw#view-connections)時，連線 ID 是「連線 ID」中顯示的完整連線 ID 最後一個部分的值，例如 `projects/myproject/locations/connection_location/connections/myconnection`。
* `BUCKET_PATH`：Cloud Storage bucket 的路徑，其中包含物件表格代表的物件，格式為 `gs://bucket_name/[folder_name/]*`。

  您可以在每個路徑中使用一個星號 (`*`) 萬用字元，限制物件表格中包含的物件。舉例來說，如果 bucket 包含多種非結構化資料，您可以只指定 `gs://bucket_name/*.pdf`，為 PDF 物件建立物件資料表。詳情請參閱「[Cloud Storage URI 的萬用字元支援](https://docs.cloud.google.com/bigquery/docs/external-data-cloud-storage?hl=zh-tw#wildcard-support)」。

  您可以提供多個路徑，為 `uris` 選項指定多個值區，例如 `gs://mybucket1/*,gs://mybucket2/folder5/*`。

  如要進一步瞭解如何在 BigQuery 中使用 Cloud Storage URI，請參閱「[Cloud Storage 資源路徑](https://docs.cloud.google.com/bigquery/docs/external-data-cloud-storage?hl=zh-tw#google-cloud-storage-uri)」。
* `STALENESS_INTERVAL`：指定針對物件資料表執行的作業是否使用快取中繼資料，以及作業必須使用多新的快取中繼資料。如要進一步瞭解中繼資料快取注意事項，請參閱「[中繼資料快取，提升效能](https://docs.cloud.google.com/bigquery/docs/object-table-introduction?hl=zh-tw#metadata_caching_for_performance)」。

  如要停用中繼資料快取功能，請指定 0。這是目前的預設做法。

  如要啟用中繼資料快取，請使用[`INTERVAL` 資料類型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#interval_type)文件所述的 `Y-M D H:M:S` 格式，指定 30 分鐘到 7 天之間的時間間隔值。舉例來說，如要指定 4 小時的過時間隔，請輸入 `0-0 0 4:0:0`。如果資料表在過去 4 小時內重新整理過，針對該資料表執行的作業就會使用快取中繼資料。如果快取中繼資料的建立時間早於該時間，作業會改為從 Cloud Storage 擷取中繼資料。
* `CACHE_MODE`：指定中繼資料快取是否自動或手動重新整理。如要進一步瞭解中繼資料快取注意事項，請參閱「[中繼資料快取，提升效能](https://docs.cloud.google.com/bigquery/docs/object-table-introduction?hl=zh-tw#metadata_caching_for_performance)」。

  設為 `AUTOMATIC`，中繼資料快取就會以系統定義的時間間隔 (通常為 30 到 60 分鐘) 重新整理。

  如要依您決定的時間表重新整理中繼資料快取，請設為 `MANUAL`。在這種情況下，您可以呼叫 [`BQ.REFRESH_EXTERNAL_METADATA_CACHE` 系統程序](https://docs.cloud.google.com/bigquery/docs/reference/system-procedures?hl=zh-tw#bqrefresh_external_metadata_cache)來重新整理快取。

  如果 `STALENESS_INTERVAL` 設為大於 0 的值，您就必須設定 `CACHE_MODE`。

**範例**

下列範例會建立物件資料表，並將中繼資料快取過時間隔設為 1 天：

```
bq mk --table \
--external_table_definition=gs://mybucket/*@us.my-connection \
--object_metadata=SIMPLE \
--max_staleness=0-0 1 0:0:0 \
--metadata_cache_mode=AUTOMATIC \
my_dataset.object_table
```

下列範例會針對三個 Cloud Storage 值區中的物件建立物件資料表：

```
bq mk --table \
--external_table_definition=gs://bucket1/*,gs://bucket2/folder1/*,gs://bucket3/*@us.my-connection \
--object_metadata=SIMPLE \
my_dataset.object_table
```

下列範例會針對 Cloud Storage bucket 中的 PDF 物件建立物件資料表：

```
bq mk --table \
--external_table_definition=gs://bucket1/*.pdf@us.my-connection \
--object_metadata=SIMPLE \
my_dataset.object_table
```

### API

呼叫 [`tables.insert` 方法](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables/insert?hl=zh-tw)。在您傳入的 [`Table` 資源中，納入 [`ExternalDataConfiguration` 物件](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables?hl=zh-tw#ExternalDataConfiguration)，並將 `objectMetadata` 欄位設為 `SIMPLE`。](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables?hl=zh-tw#resource:-table)

以下範例說明如何使用 `curl` 呼叫這個方法：

```
ACCESS_TOKEN=$(gcloud auth print-access-token) curl \
-H "Authorization: Bearer ${ACCESS_TOKEN}" \
-H "Content-Type: application/json" \
-X POST \
-d '{"tableReference": {"projectId": "my_project", "datasetId": "my_dataset", "tableId": "object_table_name"}, "externalDataConfiguration": {"objectMetadata": "SIMPLE", "sourceUris": ["gs://mybucket/*"]}}' \
https://www.googleapis.com/bigquery/v2/projects/my_project/datasets/my_dataset/tables
```

### Terraform

這個範例會建立物件資料表，並啟用中繼資料快取功能，但採用手動重新整理。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

為物件資料表指定的索引鍵欄位為 [`google_bigquery_table.external_data_configuration.object_metadata`](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/bigquery_table.html#object_metadata)、[`google_bigquery_table.external_data_configuration.metadata_cache_mode`](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/bigquery_table.html#metadata_cache_mode) 和 [`google_bigquery_table.max_staleness`](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/bigquery_table.html#max_staleness)。如要進一步瞭解各項資源，請參閱 [Terraform BigQuery 說明文件](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/bigquery_table.html)。

```
# This queries the provider for project information.
data "google_project" "default" {}

# This creates a connection in the US region named "my-connection-id".
# This connection is used to access the bucket.
resource "google_bigquery_connection" "default" {
  connection_id = "my-connection-id"
  location      = "US"
  cloud_resource {}
}

# This grants the previous connection IAM role access to the bucket.
resource "google_project_iam_member" "default" {
  role    = "roles/storage.objectViewer"
  project = data.google_project.default.project_id
  member  = "serviceAccount:${google_bigquery_connection.default.cloud_resource[0].service_account_id}"
}

# This defines a Google BigQuery dataset.
resource "google_bigquery_dataset" "default" {
  dataset_id = "my_dataset_id"
}

# This creates a bucket in the US region named "my-bucket" with a pseudorandom suffix.
resource "random_id" "bucket_name_suffix" {
  byte_length = 8
}
resource "google_storage_bucket" "default" {
  name                        = "my-bucket-${random_id.bucket_name_suffix.hex}"
  location                    = "US"
  force_destroy               = true
  uniform_bucket_level_access = true
}

# This defines a BigQuery object table with manual metadata caching.
resource "google_bigquery_table" "default" {
  table_id   = "my-table-id"
  dataset_id = google_bigquery_dataset.default.dataset_id
  external_data_configuration {
    connection_id = google_bigquery_connection.default.name
    autodetect    = false
    # `object_metadata is` required for object tables. For more information, see
    # https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/bigquery_table#object_metadata
    object_metadata = "SIMPLE"
    # This defines the source for the prior object table.
    source_uris = [
      "gs://${google_storage_bucket.default.name}/*",
    ]

    metadata_cache_mode = "MANUAL"
  }

  # This ensures that the connection can access the bucket
  # before Terraform creates a table.
  depends_on = [
    google_project_iam_member.default
  ]
}
```

如要在 Google Cloud 專案中套用 Terraform 設定，請完成下列各節的步驟。

## 準備 Cloud Shell

1. 啟動 [Cloud Shell](https://shell.cloud.google.com/?hl=zh-tw)。
2. 設定要套用 Terraform 設定的預設 Google Cloud 專案。

   您只需要為每項專案執行一次這個指令，且可以在任何目錄中執行。

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

1. 查看設定，確認 Terraform 即將建立或更新的資源符合您的預期：

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

## 查詢物件資料表

您可以像查詢其他 BigQuery 資料表一樣查詢物件資料表，例如：

```
SELECT *
FROM mydataset.myobjecttable;
```

查詢物件資料表會傳回基礎物件的中繼資料。詳情請參閱[物件資料表結構定義](https://docs.cloud.google.com/bigquery/docs/object-table-introduction?hl=zh-tw#object_table_schema)。

## 後續步驟

* 瞭解如何[對圖片物件資料表執行推論](https://docs.cloud.google.com/bigquery/docs/object-table-inference?hl=zh-tw)。
* 瞭解如何[使用遠端函式分析物件資料表](https://docs.cloud.google.com/bigquery/docs/object-table-remote-function?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-16 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-16 (世界標準時間)。"],[],[]]