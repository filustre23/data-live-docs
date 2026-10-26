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

BigQuery 資料移轉服務提供的 Snowflake 連接器可讓您安排及管理自動移轉工作，使用公開 IP 許可清單將資料從 Snowflake 遷移至 BigQuery。

## 總覽

Snowflake 連接器會與 Google Kubernetes Engine 中的遷移代理程式互動，並觸發從 Snowflake 到 Cloud Storage bucket 內暫存區的載入作業。

* 如果是 Amazon Web Services (AWS)、Azure 或 Google Cloud託管的 Snowflake 帳戶，資料會先暫存在 Cloud Storage bucket，再透過 BigQuery 資料移轉服務移轉至 BigQuery。

下圖說明從託管於 Amazon Web Services (AWS) 或 Azure 的 Snowflake 帳戶，或 Google Cloud託管的 Snowflake 帳戶公開移轉資料。

## 限制

使用 Snowflake 連接器移轉資料時，須遵守下列限制：

* Snowflake 連接器僅支援從單一 Snowflake 資料庫和結構定義中的資料表移轉資料。如要從具有多個 Snowflake 資料庫或結構定義的資料表移轉，可以分別設定各項移轉工作。
* 從 Snowflake 載入資料到 Amazon S3 bucket、Azure Blob Storage 容器或 Cloud Storage bucket 的速度，取決於您為這項移轉作業選擇的 Snowflake 倉儲。
* BigQuery 會將 Snowflake 的資料以 Parquet 檔案格式寫入 Cloud Storage。Parquet 檔案不支援 [`TIMESTAMP_TZ` 和 `TIMESTAMP_LTZ`](https://community.snowflake.com/s/article/How-To-Unload-Timestamp-data-in-a-Parquet-file) 資料類型。如果資料包含這些類型，可以將資料匯出至 Amazon S3 做為 CSV 檔案，然後將 CSV 檔案匯入 BigQuery。詳情請參閱「[Amazon S3 資料移轉簡介](https://docs.cloud.google.com/bigquery/docs/s3-transfer-intro?hl=zh-tw)」。

## 事前準備

設定 Snowflake 移轉作業前，請務必完成本節列出的所有步驟。以下列出所有必要步驟。

1. [準備 Google Cloud 專案](#preparing-gcp-project)
2. [必要的 BigQuery 角色](#required-roles)
3. [準備暫存 bucket](#preparing-staging-bucket)
4. [建立具備必要權限的 Snowflake 使用者](#create-snowflake-user)
5. [新增網路政策](#add_network_policies)
6. 選用：[結構定義偵測和對應](#schema_detection_and_mapping)
7. [評估 Snowflake 是否有不支援的資料類型](#limitations)
8. 選用：[啟用增量移轉](#enable_incremental_transfers)
9. 選用：[啟用私人連線](#enable_private_connectivity)
10. [收集轉移資訊](#gather_transfer_information)
11. 如果您打算指定客戶自行管理的加密金鑰 (CMEK)，請確認[服務帳戶具備加密和解密權限](https://docs.cloud.google.com/bigquery/docs/customer-managed-encryption?hl=zh-tw#grant_permission)，且您擁有使用 CMEK 所需的 [Cloud KMS 金鑰資源 ID](https://docs.cloud.google.com/bigquery/docs/customer-managed-encryption?hl=zh-tw#key_resource_id)。如要瞭解 CMEK 如何與移轉作業搭配運作，請參閱「[指定移轉作業加密金鑰](#CMEK)」。

### 準備 Google Cloud 專案

請按照下列步驟建立及設定 Google Cloud 專案，以便轉移 Snowflake：

1. [建立 Google Cloud 專案](https://docs.cloud.google.com/resource-manager/docs/creating-managing-projects?hl=zh-tw)或選取現有專案。

   **注意：** 如果您不打算保留在 Snowflake 移轉作業期間建立的資源，請建立新的 Google Cloud 專案，不要選取現有專案。完成 Snowflake 移轉作業後，即可刪除專案。
2. 確認您已完成[啟用 BigQuery 資料移轉服務](https://docs.cloud.google.com/bigquery/docs/enable-transfer-service?hl=zh-tw)的所有必要動作。
3. [建立 BigQuery 資料集](https://docs.cloud.google.com/bigquery/docs/datasets?hl=zh-tw)來儲存資料。您不需要建立任何資料表。

### 必要的 BigQuery 角色

如要取得建立 BigQuery 資料移轉服務資料移轉作業所需的權限，請要求管理員授予您專案的 [BigQuery 管理員](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.admin)  (`roles/bigquery.admin`) IAM 角色。如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

這個預先定義的角色具備建立 BigQuery 資料移轉服務資料移轉作業所需的權限。如要查看確切的必要權限，請展開「Required permissions」(必要權限) 部分：

#### 所需權限

您必須具備下列權限，才能建立 BigQuery 資料移轉服務資料移轉作業：

* BigQuery 資料移轉服務權限：
  + `bigquery.transfers.update`
  + `bigquery.transfers.get`
* BigQuery 權限：
  + `bigquery.datasets.get`
  + `bigquery.datasets.getIamPolicy`
  + `bigquery.datasets.update`
  + `bigquery.datasets.setIamPolicy`
  + `bigquery.jobs.create`

您或許還可透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)取得這些權限。

詳情請參閱「[授予 `bigquery.admin` 存取權](https://docs.cloud.google.com/bigquery/docs/enable-transfer-service?hl=zh-tw#grant_bigqueryadmin_access)」。

**注意：** 為方便您在建立移轉作業時選取服務帳戶和 Cloud Storage bucket URI，建議您將 `iam.serviceAccounts.list` 和 `storage.buckets.list` 權限授予建立移轉設定的使用者。

### 準備暫存 bucket

如要準備 Snowflake 資料移轉作業，請建立暫存 bucket，然後設定允許 Snowflake 寫入。您必須先將 Snowflake 資料暫存於 Cloud Storage bucket，才能載入 BigQuery。

1. [建立 Cloud Storage bucket](https://docs.cloud.google.com/storage/docs/creating-buckets?hl=zh-tw)。
2. [建立及設定 Snowflake 儲存空間整合物件](https://docs.snowflake.com/en/user-guide/data-load-gcs-config)，允許 Snowflake 將資料寫入 Cloud Storage bucket 做為外部暫存區。
3. 執行 [`DESCRIBE INTEGRATION` 指令](https://docs.snowflake.com/en/user-guide/data-load-gcs-config#step-2-retrieve-the-cloud-storage-service-account-for-your-snowflake-account)時，Cloud Storage 服務帳戶會列在 `STORAGE_GCP_SERVICE_ACCOUNT` 欄位下方。將 Cloud Storage bucket 的下列權限授予 Cloud Storage 服務帳戶：
   * `storage.objects.create`
   * `storage.objects.delete`
   * `storage.objects.get`
   * `storage.objects.list`
4. 如要允許存取暫存 bucket，請使用下列指令，將 `roles/storage.objectViewer` 角色授予 [DTS 服務代理](https://docs.cloud.google.com/bigquery/docs/enable-transfer-service?hl=zh-tw#service_agent)：

   ```
   gcloud storage buckets add-iam-policy-binding gs://STAGING_BUCKET_NAME \
     --member=serviceAccount:service-PROJECT_NUMBER@gcp-sa-bigquerydatatransfer.iam.gserviceaccount.com \
     --role=roles/storage.objectViewer
   ```

如要進行 Snowflake 私人資料移轉，請[建立暫存 bucket 並設定私人連線](https://docs.cloud.google.com/bigquery/docs/migration/snowflake-private-connectivity?hl=zh-tw#prepare_staging_bucket)。

### 建立具備必要權限的 Snowflake 使用者

在 Snowflake 移轉期間，Snowflake 連接器會使用 JDBC 連線，連線至您的 Snowflake 帳戶。您必須建立新的 Snowflake 使用者，並指派自訂角色，只授予執行資料移轉所需的權限：

```
  // Create and configure new role, MIGRATION_ROLE
  GRANT USAGE
    ON WAREHOUSE WAREHOUSE_NAME
    TO ROLE MIGRATION_ROLE;

  GRANT USAGE
    ON DATABASE DATABASE_NAME
    TO ROLE MIGRATION_ROLE;

  GRANT USAGE
    ON SCHEMA DATABASE_NAME.SCHEMA_NAME
    TO ROLE MIGRATION_ROLE;

  // You can modify this to give select permissions for all tables in a schema
  GRANT SELECT
    ON TABLE DATABASE_NAME.SCHEMA_NAME.TABLE_NAME
    TO ROLE MIGRATION_ROLE;

  GRANT USAGE
    ON INTEGRATION STORAGE_INTEGRATION_OBJECT_NAME
    TO ROLE MIGRATION_ROLE;
```

更改下列內容：

* `MIGRATION_ROLE`：要建立的自訂角色名稱
* `WAREHOUSE_NAME`：資料倉儲的名稱
* `DATABASE_NAME`：Snowflake 資料庫名稱
* `SCHEMA_NAME`：Snowflake 結構定義的名稱
* `TABLE_NAME`：這項資料移轉作業包含的 Snowflake 名稱
* `STORAGE_INTEGRATION_OBJECT_NAME`：Snowflake 儲存空間整合物件的名稱。

#### 產生用於驗證的金鑰組

由於 [Snowflake 已淘汰單一要素密碼登入機制](https://docs.snowflake.com/en/user-guide/security-mfa-rollout)，建議您使用金鑰組進行驗證。

如要設定金鑰組，請產生加密或未加密的 RSA 金鑰組，然後將公開金鑰指派給 Snowflake 使用者。詳情請參閱「[設定金鑰組驗證](https://docs.snowflake.com/en/user-guide/key-pair-auth#configuring-key-pair-authentication)」。

#### 允許卸載至內嵌外部位置

Snowflake 連接器會在移轉期間，將資料轉存至內嵌外部位置。如果 Snowflake 帳戶限制將資料卸載至內嵌位置，移轉作業就會失敗。

如要允許將資料卸載至內嵌位置，請在 Snowflake 帳戶中執行下列 SQL 指令。您必須具備 Snowflake 的 `ACCOUNTADMIN` 角色，才能執行這項指令。

```
ALTER ACCOUNT SET PREVENT_UNLOAD_TO_INLINE_URL = false;
```

### 新增網路政策

如果是公開連線，Snowflake 帳戶預設允許使用資料庫憑證進行公開連線。不過，您可能設定了網路規則或政策，導致 Snowflake 連接器無法連線至帳戶。在這種情況下，您必須將必要的 IP 位址加入許可清單。詳情請參閱「[設定 Snowflake 移轉作業的網路政策](https://docs.cloud.google.com/bigquery/docs/migration/snowflake-network-policies?hl=zh-tw)」。

### 結構定義偵測和對應

如要定義結構定義，您可以使用 BigQuery 資料移轉服務，在將資料從 Snowflake 移轉至 BigQuery 時，自動偵測結構定義和資料類型對應。或者，您也可以使用翻譯引擎，手動定義結構定義和資料類型。

詳情請參閱「[Snowflake 的結構定義偵測和對應](https://docs.cloud.google.com/bigquery/docs/migration/snowflake-transfer-schema?hl=zh-tw)」。

### 啟用增量移轉

如要設定 Snowflake 累加式資料移轉作業，請參閱「[設定 Snowflake 累加式移轉作業](https://docs.cloud.google.com/bigquery/docs/migration/snowflake-incremental?hl=zh-tw)」。

### 啟用私人連線

如要建立私人 Snowflake 資料移轉作業，請[為私人連線設定網路](https://docs.cloud.google.com/bigquery/docs/migration/snowflake-private-connectivity?hl=zh-tw)。

### 收集轉移資訊

收集使用 BigQuery 資料移轉服務設定遷移作業所需的資訊：

* Snowflake 帳戶 ID，也就是 Snowflake 帳戶網址的前置字串。例如 `ACCOUNT_IDENTIFIER.snowflakecomputing.com`。
* 使用者名稱和相關聯的私密金鑰，須具備 Snowflake 資料庫的適當權限。只要具備[執行資料移轉所需的權限](#create-snowflake-user)即可。
* 用於移轉作業的[暫存 bucket URI](#preparing-staging-bucket)。建議您為這個 bucket 設定生命週期政策，以免產生不必要的費用。
* Cloud Storage bucket 的 URI，用於儲存[從翻譯引擎取得的結構定義對應檔](https://docs.cloud.google.com/bigquery/docs/migration/snowflake-transfer-schema?hl=zh-tw)。

## 設定 Snowflake 移轉作業

選取下列選項之一：

### 控制台

1. 前往 Google Cloud 控制台的「資料移轉」頁面。

   [前往「資料移轉」](https://console.cloud.google.com/bigquery/transfers?hl=zh-tw)
2. 按一下「add 建立移轉作業」。
3. 在「Source type」(來源類型) 部分，從「Source」(來源) 清單選取「Snowflake Migration」(Snowflake 遷移)。
4. 在「Transfer config name」(移轉設定名稱) 部分，於「Display name」(顯示名稱) 欄位輸入移轉作業名稱，例如 `My migration`。顯示名稱可以是任何值，只要日後需要修改時能識別移轉作業即可。
5. 在「Destination settings」(目的地設定) 部分，從「Dataset」(資料集) 清單中選擇[您建立的資料集](#preparing-gcp-project)。
6. 在「Snowflake Credentials」(Snowflake 憑證) 部分，執行下列操作：

   1. 在「Account Identifier」(帳戶 ID) 部分，輸入 Snowflake 帳戶的專屬 ID，也就是組織名稱和帳戶名稱的組合。ID 是 Snowflake 帳戶網址的前置字元，而非完整網址。例如：`ACCOUNT_IDENTIFIER.snowflakecomputing.com`。
   2. 在「Username」(使用者名稱) 部分，輸入 Snowflake 使用者的使用者名稱，系統會使用該使用者的憑證和授權存取資料庫，以便移轉 Snowflake 資料表。建議您使用[為這項移轉作業建立的使用者](#create-snowflake-user)。
   3. 在「Authentication Mechanism」(驗證機制) 部分，選取 Snowflake 使用者驗證方式：

      ### PASSWORD

      * 在「Password」(密碼) 部分，輸入 Snowflake 使用者的密碼。

      ### KEY\_PAIR

      * 在「Private Key」(私密金鑰)，輸入與[和 Snowflake 使用者相關聯的公開金鑰](#create-snowflake-user)連結的私密金鑰。
      * 如果私密金鑰是以通關密語加密，請選取「Is Private Key Encrypted」(私密金鑰是否加密)。
      * 在「Private Key Passphrase」(私密金鑰通關密語) 部分，輸入加密私密金鑰的通關密語。如果選取「Is Private Key Encrypted」(私密金鑰是否加密)，就必須填寫這個欄位。詳情請參閱「[產生用於驗證的金鑰組](#generate_key_pair_for_authentication)」。
   * 在「Warehouse」(倉儲) 中，輸入用於執行這項資料移轉作業的[倉儲](https://docs.snowflake.com/en/user-guide/warehouses-tasks)。
   * 在「Snowflake Database」(Snowflake 資料庫) 部分，輸入 Snowflake 資料庫的名稱，該資料庫包含這項資料移轉作業中的資料表。
   * 在「Snowflake Schema」部分，輸入 Snowflake 結構定義的名稱，該結構定義包含這項資料移轉作業中的資料表。
7. 在「Storage Configuration」(儲存空間設定) 部分，執行下列操作：

   1. 在「Storage integration object name」(儲存空間整合物件名稱)，輸入 Snowflake 儲存空間整合物件的名稱。
   2. 選用：在「Max file size」(檔案大小上限) 部分，指定從 Snowflake 卸載至暫存位置的各個檔案大小上限 (以 MB 為單位)。
   3. 在「Cloud Provider」(雲端服務供應商) 部分，根據託管 Snowflake 帳戶的雲端服務供應商，選取 `AWS`、`AZURE` 或 `GCP`。

      * 在「GCS URI」中，輸入要用作暫存 bucket 的 [Cloud Storage bucket URI](#preparing-staging-bucket)。
8. 在「Service Account」(服務帳戶) 部分，執行下列操作：

   1. 在「Service Account」(服務帳戶) 部分，輸入要與這項資料移轉作業搭配使用的服務帳戶。服務帳戶應與建立移轉設定和目的地資料集的Google Cloud 專案相同。服務帳戶必須具備 `storage.objects.list` 和 `storage.objects.get` [必要權限](https://docs.cloud.google.com/bigquery/docs/migration/snowflake-transfer-schema?hl=zh-tw#required_service_account_permissions)。
9. 在「Schema Configuration」(結構定義設定) 部分，執行下列操作：

   1. 在「Ingestion type」(擷取類型) 部分，選取「Full」(完整) 或「Incremental」(增量)。詳情請參閱「[設定增量移轉作業](https://docs.cloud.google.com/bigquery/docs/migration/snowflake-incremental?hl=zh-tw#configure_incremental_transfers)」。
   2. 在「Table name patterns」(資料表名稱模式)，輸入名稱或與結構定義中資料表名稱相符的模式，指定要移轉的資料表。您可以使用規則運算式指定模式，例如 `table1_regex;table2_regex`。模式應遵循 Java 規則運算式語法。例如：
      * `lineitem;ordertb` 會比對名為 `lineitem` 和 `ordertb` 的資料表。
      * `.*` 會比對所有資料表。
   3. 選用：如要指定自訂翻譯輸出路徑，請選取「Use BigQuery Translation Engine Output」欄位。
   4. 選用：在「Translation output GCS path」(轉譯輸出內容 GCS 路徑)，指定 Cloud Storage 資料夾的路徑，其中包含[轉譯引擎的結構定義對應檔案](https://docs.cloud.google.com/bigquery/docs/migration/snowflake-transfer-schema?hl=zh-tw)。您可以留空，讓 Snowflake 連接器自動偵測結構定義。
      * 路徑應採用 `translation_target_base_uri/metadata/config/db/schema/` 格式，且結尾必須是 `/`。
   5. 選用：在「Custom schema file path」(自訂結構定義檔案路徑) 部分，指定自訂結構定義檔案的 Cloud Storage 路徑。
   6. 選用：在「Map zero scale Snowflake NUMBER to BigQuery INT64」(將零小數位數 Snowflake NUMBER 對應至 BigQuery INT64) 部分，如要將 Snowflake `NUMBER(p, 0)` 類型對應至 BigQuery `INT64`，請選取這個欄位。
10. 在「Network Connectivity」(網路連線) 部分，執行下列操作：

    1. 如要建立[私人資料移轉](https://docs.cloud.google.com/bigquery/docs/migration/snowflake-private-connectivity?hl=zh-tw)，請在「Use Private Network」(使用私人網路) 部分選取「True」(是)。
    2. 如果是建立私人連線，請在「PSC Service Attachment」(PSC 服務連結) 輸入服務連結 URI。詳情請參閱「[建立私人 Snowflake 移轉設定](https://docs.cloud.google.com/bigquery/docs/migration/snowflake-private-connectivity?hl=zh-tw#create-transfer-config)」。
    3. 如果是**私人網路服務**，且您要建立私人資料移轉作業，請輸入 Service Directory 自我連結。詳情請參閱「[建立私人 Snowflake 移轉設定](https://docs.cloud.google.com/bigquery/docs/migration/snowflake-private-connectivity?hl=zh-tw#create-transfer-config)」。
11. 選用：在「Notification options」(通知選項) 專區，執行下列操作：

    1. 按一下啟用電子郵件通知的切換開關。啟用這個選項之後，若移轉失敗，移轉作業管理員就會收到電子郵件通知。
    2. 在「Select a Pub/Sub topic」(選取 Pub/Sub 主題) 選取[主題](https://docs.cloud.google.com/pubsub/docs/overview?hl=zh-tw#types)名稱，或是點選「Create a topic」(建立主題)。這個選項會設定移轉作業的 Pub/Sub 執行[通知](https://docs.cloud.google.com/bigquery/docs/transfer-run-notifications?hl=zh-tw)。
12. 如果使用 [CMEK](https://docs.cloud.google.com/bigquery/docs/customer-managed-encryption?hl=zh-tw)，請在「Advanced options」(進階選項) 部分選取「Customer-managed key」(客戶管理的金鑰)。畫面隨即會列出可用的 CMEK 供您選擇。如要瞭解 CMEK 如何與 BigQuery 資料移轉服務搭配運作，請參閱[指定移轉作業加密金鑰](#CMEK)的相關說明。
13. 按一下 [儲存]。
14. Google Cloud 控制台會顯示所有移轉設定詳細資料，包括這項移轉作業的「Resource name」(資源名稱)。

### bq

輸入 `bq mk` 指令並加上移轉建立作業旗標 `--transfer_config`。還需加上以下旗標：

* `--project_id`
* `--data_source`
* `--target_dataset`
* `--display_name`
* `--params`

```
bq mk \
    --transfer_config \
    --project_id=PROJECT_ID \
    --data_source=DATA_SOURCE \
    --target_dataset=DATASET \
    --display_name=NAME \
    --service_account_name=SERVICE_ACCOUNT \
    --params='PARAMETERS'
```

更改下列內容：

* `PROJECT_ID`：您的 Google Cloud 專案 ID。如未指定 `--project_id`，系統會使用預設專案。
* `DATA_SOURCE`