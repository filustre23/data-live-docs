Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [參考資料](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 排定 Snowflake 移轉作業

BigQuery 資料移轉服務提供的 Snowflake 連接器可讓您排定及管理自動移轉工作，使用公開 IP 許可清單將資料從 Snowflake 遷移至 BigQuery。

## 總覽

Snowflake 連接器會與 Google Kubernetes Engine 中的遷移代理程式互動，並觸發從 Snowflake 到 Cloud Storage bucket 內暫存區的載入作業。

* 如果是 Amazon Web Services (AWS)、Azure 或 Google Cloud託管的 Snowflake 帳戶，資料會先暫存在 Cloud Storage bucket，再透過 BigQuery 資料移轉服務移轉至 BigQuery。

下圖說明從託管於 Amazon Web Services (AWS) 或 Azure 的 Snowflake 帳戶，或 Google Cloud託管的 Snowflake 帳戶公開移轉資料。

## 限制

使用 Snowflake 連接器移轉資料時，須遵守下列限制：

* Snowflake 連接器僅支援從單一 Snowflake 資料庫和結構定義中的資料表移轉資料。如要從具有多個 Snowflake 資料庫或結構定義的資料表移轉，可以分別設定各項移轉工作。
* 將資料從 Snowflake 載入 Amazon S3 bucket、Azure Blob Storage 容器或 Cloud Storage bucket 的速度，取決於您為這項移轉作業選擇的 Snowflake 倉儲。
* BigQuery 會將 Snowflake 的資料以 Parquet 檔案格式寫入 Cloud Storage。Parquet 檔案不支援 [`TIMESTAMP_TZ` 和 `TIMESTAMP_LTZ`](https://community.snowflake.com/s/article/How-To-Unload-Timestamp-data-in-a-Parquet-file) 資料類型。如果資料包含這些類型，可以將資料匯出至 Amazon S3 為 CSV 檔案，然後將 CSV 檔案匯入 BigQuery。詳情請參閱「[Amazon S3 資料移轉簡介](https://docs.cloud.google.com/bigquery/docs/s3-transfer-intro?hl=zh-tw)」。

## 事前準備

以下各節說明設定 Snowflake 移轉作業的必要步驟。

### 準備 Google Cloud 專案

請按照下列步驟，建立及設定 Google Cloud 專案，以便移轉 Snowflake：

1. [建立 Google Cloud 專案](https://docs.cloud.google.com/resource-manager/docs/creating-managing-projects?hl=zh-tw)或選取現有專案。

   **注意：**如果您不打算保留在這項 Snowflake 移轉作業中建立的資源，請建立新的 Google Cloud 專案，不要選取現有專案。完成 Snowflake 移轉作業後，即可刪除專案。
2. 確認您已完成[啟用 BigQuery 資料移轉服務](https://docs.cloud.google.com/bigquery/docs/enable-transfer-service?hl=zh-tw)的所有必要動作。
3. [建立 BigQuery 資料集](https://docs.cloud.google.com/bigquery/docs/datasets?hl=zh-tw)來儲存資料。您不需要建立任何資料表。

### 取得必要的 IAM 角色

如要建立及管理 Snowflake 資料移轉作業，所有必要的使用者和服務帳戶都必須具備下表所述的角色：

| 身分 | 角色 | 目標資源 |
| --- | --- | --- |
| 使用者帳戶 | `roles/bigquery.user` | Google Cloud 專案 |
| 使用者帳戶 | `roles/bigquery.dataOwner` | 目的地 BigQuery 資料集 |
| 使用者帳戶 | `roles/iam.serviceAccountUser` | 專屬服務帳戶 |
| 專屬服務帳戶 | `roles/storage.objectViewer` | 暫存 Cloud Storage bucket，以及包含結構定義對應檔案的一或多個 bucket |
| BigQuery 資料移轉服務服務代理 | `roles/storage.objectViewer` | Cloud Storage 暫存 bucket |
| BigQuery 資料移轉服務服務代理 | `roles/bigquery.dataEditor` | 目的地 BigQuery 資料集 |
| BigQuery 資料移轉服務服務代理 | `roles/iam.serviceAccountTokenCreator` | 專屬服務帳戶 (如果您使用[跨專案服務帳戶](https://docs.cloud.google.com/bigquery/docs/enable-transfer-service?hl=zh-tw#cross-project_service_account_authorization)) |
| Snowflake Google Cloud 服務帳戶 | `roles/storage.objectUser` | Cloud Storage 暫存 bucket |
| Snowflake Google Cloud 服務帳戶 | `roles/storage.bucketViewer` | Cloud Storage 暫存 bucket |

以下各節將詳細說明各身分所需的角色和權限。

#### 取得使用者帳戶權限

如要取得建立及管理移轉設定，以及使用使用者帳戶執行工作的權限，請要求管理員授予您下列 IAM 角色：

* 建立及管理移轉設定，並執行工作：專案的 [BigQuery 使用者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.user) (`roles/bigquery.user`)
* 管理及授予目的地資料集的存取權：目的地 BigQuery 資料集的 [BigQuery 資料擁有者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.dataOwner) (`roles/bigquery.dataOwner`)
* 使用專屬服務帳戶建立或更新移轉設定：專屬服務帳戶的[服務帳戶使用者](https://docs.cloud.google.com/iam/docs/roles-permissions/iam?hl=zh-tw#iam.serviceAccountUser) (`roles/iam.serviceAccountUser`)

如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

這些預先定義的角色具備所需權限，可建立及管理移轉設定，並透過使用者帳戶執行工作。如要查看確切的必要權限，請展開「Required permissions」(必要權限) 部分：

#### 所需權限

您必須具備下列權限，才能建立及管理移轉設定，以及透過使用者帳戶執行工作：

* `bigquery.transfers.get`
* `bigquery.transfers.update`
* `bigquery.datasets.get`
* `bigquery.datasets.getIamPolicy`
* `bigquery.datasets.update`
* `bigquery.jobs.create`
* `bigquery.datasets.setIamPolicy`
* `iam.serviceAccounts.actAs`

您或許還可透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)取得這些權限。

#### 取得專屬服務帳戶權限

為確保專用服務帳戶具備必要權限，可在移轉作業執行期間，使用服務帳戶讀取翻譯中繼資料、自訂結構定義或暫存檔案，請要求管理員將 Cloud Storage 暫存 bucket 和包含結構定義對應檔案的 bucket，授予專用服務帳戶 [Storage 物件檢視者](https://docs.cloud.google.com/iam/docs/roles-permissions/storage?hl=zh-tw#storage.objectViewer) (`roles/storage.objectViewer`) IAM 角色。

**重要事項：**請務必將這個角色授予專屬服務帳戶，*而非*您的使用者帳戶。如果未將角色授予正確的主體，可能會發生權限錯誤。

#### 取得 BigQuery 資料移轉服務服務代理權限

為確保 BigQuery 資料移轉服務服務代理具備必要權限，可使用服務代理執行移轉作業，請要求管理員將下列 IAM 角色授予 BigQuery 資料移轉服務服務代理：

**重要事項：**您必須將這些角色授予 BigQuery 資料移轉服務代理，*而非*您的使用者帳戶。如果未將角色授予正確的主體，可能會發生權限錯誤。

* 在移轉作業執行期間讀取未載入的資料檔案：Cloud Storage 暫存 bucket 的 [Storage 物件檢視者](https://docs.cloud.google.com/iam/docs/roles-permissions/storage?hl=zh-tw#storage.objectViewer) (`roles/storage.objectViewer`)
* 將移轉的資料寫入目的地資料表：目的地 BigQuery 資料集的 [BigQuery 資料編輯者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.dataEditor) (`roles/bigquery.dataEditor`)
* 授權使用跨專案服務帳戶的移轉作業：跨專案專用服務帳戶的[服務帳戶權杖建立者](https://docs.cloud.google.com/iam/docs/roles-permissions/iam?hl=zh-tw#iam.serviceAccountTokenCreator) (`roles/iam.serviceAccountTokenCreator`)

如果專用服務帳戶與啟用 BigQuery 資料移轉服務的專案位於相同位置，Google 會自動授予必要的 `iam.serviceAccounts.getAccessToken` 權限。只有在專用服務帳戶位於不同專案時，才需要手動授予服務帳戶權杖建立者角色 (`roles/iam.serviceAccountTokenCreator`)。詳情請參閱「[跨專案服務帳戶授權](https://docs.cloud.google.com/bigquery/docs/enable-transfer-service?hl=zh-tw#cross-project_service_account_authorization)」。

#### 取得 Snowflake Google Cloud 服務帳戶權限

為確保 Snowflake Google Cloud 服務帳戶具備必要權限，可在暫存 bucket 中寫入及管理卸載的資料檔案，請要求管理員在 Cloud Storage 暫存 bucket 中，將下列 IAM 角色授予 Snowflake Google Cloud 服務帳戶：

**重要事項：**請務必將這些角色授予 Snowflake Google Cloud 服務帳戶，*而非*您的使用者帳戶。如果未將角色授予正確的主體，可能會發生權限錯誤。

* [Storage 物件使用者](https://docs.cloud.google.com/iam/docs/roles-permissions/storage?hl=zh-tw#storage.objectUser) (`roles/storage.objectUser`)
* [Storage bucket 檢視者](https://docs.cloud.google.com/iam/docs/roles-permissions/storage?hl=zh-tw#storage.bucketViewer) (`roles/storage.bucketViewer`)

這些預先定義的角色具備在暫存 bucket 中寫入及管理卸載資料檔案所需的權限。如要查看確切的必要權限，請展開「Required permissions」(必要權限) 部分：

#### 所需權限

您必須具備下列權限，才能在暫存 bucket 中寫入及管理卸載的資料檔案：

* `storage.buckets.get`
* `storage.objects.get`
* `storage.objects.create`
* `storage.objects.delete`
* `storage.objects.list`

### 準備暫存 bucket

如要準備 Snowflake 資料移轉作業，請建立暫存 bucket，並設定允許 Snowflake 寫入。您必須先將 Snowflake 資料暫存至 Cloud Storage bucket，才能載入 BigQuery。暫存 bucket 不得啟用階層命名空間功能。

如要建立及設定暫存 bucket，請按照下列步驟操作：

1. [建立 Cloud Storage bucket](https://docs.cloud.google.com/storage/docs/creating-buckets?hl=zh-tw)。
2. [建立及設定 Snowflake 儲存空間整合物件](https://docs.snowflake.com/en/user-guide/data-load-gcs-config)，允許 Snowflake 將資料寫入 Cloud Storage bucket 做為外部暫存區。

   ```
   CREATE STORAGE INTEGRATION STORAGE_INTEGRATION_NAME
   TYPE = EXTERNAL_STAGE
   STORAGE_PROVIDER = 'GCS'
   ENABLED = TRUE
   STORAGE_ALLOWED_LOCATIONS = ('gcs://STAGING_BUCKET_NAME/');

   -- Describe integration to retrieve Snowflake Google Cloud service account
   DESCRIBE INTEGRATION STORAGE_INTEGRATION_NAME;
   ```

   更改下列內容：

   * `STORAGE_INTEGRATION_NAME`：新儲存空間整合物件的名稱。
   * `STAGING_BUCKET_NAME`：您建立的 Cloud Storage bucket 名稱。
3. 執行 [`DESCRIBE INTEGRATION` 指令](https://docs.snowflake.com/en/user-guide/data-load-gcs-config#step-2-retrieve-the-cloud-storage-service-account-for-your-snowflake-account)時，Cloud Storage 服務帳戶會列在 `STORAGE_GCP_SERVICE_ACCOUNT` 欄位下方。將 Cloud Storage bucket 的下列權限授予 Cloud Storage 服務帳戶：

   * `storage.buckets.get`
   * `storage.objects.create`
   * `storage.objects.delete`
   * `storage.objects.get`
   * `storage.objects.list`
4. 如要允許存取暫存 bucket，請將 `roles/storage.objectViewer` 角色授予 [BigQuery 資料移轉服務代理](https://docs.cloud.google.com/bigquery/docs/enable-transfer-service?hl=zh-tw#service_agent)：

   ```
   gcloud storage buckets add-iam-policy-binding gs://STAGING_BUCKET_NAME \
       --member=serviceAccount:service-PROJECT_NUMBER@gcp-sa-bigquerydatatransfer.iam.gserviceaccount.com \
       --role=roles/storage.objectViewer
   ```

如要進行 Snowflake 私人資料移轉，請[建立暫存 bucket 並設定私人連線](https://docs.cloud.google.com/bigquery/docs/migration/snowflake-private-connectivity?hl=zh-tw#prepare_staging_bucket)。

如果 Google Cloud 貴組織使用 `constraints/iam.allowedPolicyMemberDomains` 限制強制執行網域限制共用，則將暫存 bucket 的 IAM 角色授予 `STORAGE_GCP_SERVICE_ACCOUNT` 服務帳戶會失敗，因為該服務帳戶屬於 Snowflake 的外部組織。

您無法從服務帳戶電子郵件地址衍生 Snowflake 的 Google Workspace 客戶 ID。透過下列任一方式取得客戶 ID：

* 如果您的 Snowflake 帳戶託管於 Google Cloud，請在 Snowflake 中以 `ACCOUNTADMIN` 角色執行 `SELECT SYSTEM$GET_SNOWFLAKE_PLATFORM_INFO();`，並在輸出內容中找出 `snowflake-customer-directory-id` 值。
* 如果您的 Snowflake 帳戶託管於 AWS 或 Azure，請與 Snowflake 支援團隊聯絡，索取 `STORAGE_GCP_SERVICE_ACCOUNT` 服務帳戶的 Google Workspace 客戶 ID。

如要將 Snowflake 的客戶 ID 新增至專案的許可清單，請更新組織政策：

```
gcloud resource-manager org-policies allow \
    iam.allowedPolicyMemberDomains EXTERNAL_CUSTOMER_ID \
    --project=PROJECT_ID
```

更改下列內容：

* `EXTERNAL_CUSTOMER_ID`：Snowflake 的 Google Workspace 客戶 ID。
* `PROJECT_ID`： Google Cloud 專案 ID，用於存放暫存 bucket。

詳情請參閱「[使用網域限制共用功能限制身分](https://docs.cloud.google.com/organization-policy/restrict-domains?hl=zh-tw#predefined-constraint)」。

### 建立具備必要權限的 Snowflake 使用者

在 Snowflake 移轉期間，Snowflake 連接器會使用 JDBC 連線連至 Snowflake 帳戶。您必須建立新的 Snowflake 使用者，並指派自訂角色，只授予執行資料移轉所需的權限。

下表列出名為 `MIGRATION_ROLE` 的自訂角色所需的角色和權限：

| 身分 | 角色或權限 | 目標資源 | 目的 |
| --- | --- | --- | --- |
| 遷移使用者 | `MIGRATION_ROLE` | Snowflake 帳戶 | 使用 RSA 金鑰組進行驗證，並執行遷移作業。 |
| 遷移角色 | `USAGE` | Snowflake 倉儲 | 提供執行查詢所需的運算能力。 |
|  | `USAGE` | Snowflake 資料庫和結構定義 | 存取包含來源資料表的資料庫和結構定義。 |
|  | `SELECT` | 來源資料表 | 讀取資料表中繼資料，並擷取要移轉的資料。 |
|  | `USAGE` | 儲存空間整合 | 授權將資料卸載至外部 Cloud Storage 暫存 bucket。 |

如要建立及設定自訂角色和遷移使用者，請在 Snowflake 帳戶中執行下列 SQL 指令：

1. 建立自訂角色 `MIGRATION_ROLE`：

   ```
   CREATE ROLE MIGRATION_ROLE;
   ```

   將 `MIGRATION_ROLE` 替換為您要建立的自訂角色名稱。
2. 授予自訂角色必要權限：

   ```
   GRANT USAGE ON WAREHOUSE WAREHOUSE_NAME
   ```