Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [參考資料](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 排定 Snowflake 轉移作業

BigQuery 資料移轉服務提供的 Snowflake 連接器可讓您排定及管理自動移轉工作，使用公開 IP 允許清單將資料從 Snowflake 移轉至 BigQuery。

## 總覽

Snowflake 連接器會與 Google Kubernetes Engine 中的遷移代理程式相互通訊，並觸發從 Snowflake 傳輸至暫存區的載入作業，而暫存區與 Snowflake 位於同一雲端服務供應商。

* 如果是 Amazon Web Services (AWS) 代管的 Snowflake 帳戶，資料會先暫存在 Amazon S3 值區，然後透過 BigQuery 資料移轉服務移轉至 BigQuery。
* 如果是Google Cloud代管的 Snowflake 帳戶，資料會先暫存在 Cloud Storage 值區，然後透過 BigQuery 資料移轉服務移轉至 BigQuery。
* 如果是 Azure 代管的 Snowflake 帳戶，資料會先暫存在 Azure Blob 儲存體容器中，然後透過 BigQuery 資料移轉服務移轉至 BigQuery。

下圖比較從其他雲端服務供應商代管的 Snowflake 帳戶，以及 Google Cloud代管的 Snowflake 帳戶傳輸資料的差異。

## 限制

使用 Snowflake 連接器進行資料轉移時，須遵守下列限制：

* Snowflake 連接器僅支援從單一 Snowflake 資料庫和結構定義中的資料表轉移資料。如要從具有多個 Snowflake 資料庫或結構定義的資料表轉移資料，可以分別設定每項轉移工作。
* 從 Snowflake 將資料載入 Amazon S3 值區、Azure Blob 儲存體容器或 Cloud Storage 值區的速度，取決於您為這項轉移作業選擇的 Snowflake 倉庫。
* BigQuery 會將 Snowflake 中的資料以 Parquet 檔案的形式寫入 Cloud Storage。Parquet 檔案不支援 [`TIMESTAMP_TZ` 和 `TIMESTAMP_LTZ`](https://community.snowflake.com/s/article/How-To-Unload-Timestamp-data-in-a-Parquet-file) 資料類型。如果資料包含這些類型，您可以將資料匯出至 Amazon S3 做為 CSV 檔案，然後將 CSV 檔案匯入 BigQuery。詳情請參閱 [Amazon S3 移轉作業總覽](https://docs.cloud.google.com/bigquery/docs/s3-transfer-intro?hl=zh-tw)。

## 事前準備

設定 Snowflake 轉移作業前，請務必完成本節列出的所有步驟。以下列出所有必要步驟。

1. [準備 Google Cloud 專案](#preparing-gcp-project)
2. [必要 BigQuery 角色](#required-roles)
3. [準備暫存 bucket](#preparing-staging-bucket)
4. [建立具備必要權限的 Snowflake 使用者](#create-snowflake-user)
5. [新增網路政策](#add_network_policies)
6. 選用：[結構定義偵測和對應](#schema_detection_and_mapping)
7. [評估 Snowflake 是否有任何不支援的資料類型](#limitations)
8. 選用：[啟用增量轉移](#enable_incremental_transfers)
9. 選用步驟：[啟用私人連線](#enable_private_connectivity)
10. [收集轉移資訊](#gather_transfer_information)
11. 如果您打算指定客戶自行管理的加密金鑰 (CMEK)，請確保[服務帳戶具有加密和解密權限](https://docs.cloud.google.com/bigquery/docs/customer-managed-encryption?hl=zh-tw#grant_permission)，且您擁有使用 CMEK 時所需的 [Cloud KMS 金鑰資源 ID](https://docs.cloud.google.com/bigquery/docs/customer-managed-encryption?hl=zh-tw#key_resource_id)。如要瞭解 CMEK 如何與移轉作業搭配運作，請參閱「[指定移轉作業加密金鑰](#CMEK)」。

### 準備 Google Cloud 專案

請按照下列步驟，建立及設定 Snowflake 轉移專案： Google Cloud

1. [建立 Google Cloud 專案](https://docs.cloud.google.com/resource-manager/docs/creating-managing-projects?hl=zh-tw)或選取現有專案。

   **注意：** 如果您不打算保留在這次 Snowflake 轉移作業中建立的資源，請建立新的 Google Cloud 專案，不要選取現有專案。完成 Snowflake 轉移作業後，即可刪除專案。
2. 確認您已完成[啟用 BigQuery 資料移轉服務](https://docs.cloud.google.com/bigquery/docs/enable-transfer-service?hl=zh-tw)的一切必要動作。
3. [建立 BigQuery 資料集](https://docs.cloud.google.com/bigquery/docs/datasets?hl=zh-tw)來儲存資料。您無須建立任何資料表。

### 必要的 BigQuery 角色

如要取得建立 BigQuery 資料移轉服務資料移轉作業所需的權限，請要求系統管理員在專案中授予您 [BigQuery 管理員](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.admin)  (`roles/bigquery.admin`) IAM 角色。如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

這個預先定義的角色具備建立 BigQuery 資料移轉服務資料移轉作業所需的權限。如要查看確切的必要權限，請展開「Required permissions」(必要權限) 部分：

#### 所需權限

如要建立 BigQuery 資料移轉服務資料移轉作業，您必須具備下列權限：

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

**注意：** 為方便在建立移轉作業時選取服務帳戶和 Cloud Storage 值區 URI，建議您對建立移轉設定的使用者授予 `iam.serviceAccounts.list` 和 `storage.buckets.list` 權限。

### 準備暫存 bucket

如要完成 Snowflake 資料移轉，您必須建立暫存 bucket，然後設定該 bucket，允許 Snowflake 寫入資料。

選取下列選項之一：

### AWS

**AWS 代管 Snowflake 帳戶的暫存值區**

如果是 AWS 代管的 Snowflake 帳戶，請建立 Amazon S3 值區來暫存 Snowflake 資料，再將資料載入 BigQuery。

1. [建立 Amazon S3 bucket](https://docs.aws.amazon.com/AmazonS3/latest/userguide/create-bucket-overview.html)。
2. [建立及設定 Snowflake 儲存空間整合物件](https://docs.snowflake.com/en/user-guide/data-load-s3-config-storage-integration)，允許 Snowflake 將資料寫入 Amazon S3 值區，做為外部階段。

如要允許 Amazon S3 bucket 的讀取權限，
您也必須執行下列操作：

1. 建立專用的 [Amazon IAM 使用者](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users.html)，並授予 [AmazonS3ReadOnlyAccess](https://docs.aws.amazon.com/aws-managed-policy/latest/reference/AmazonS3ReadOnlyAccess.html) 政策。
2. 為 IAM 使用者[建立 Amazon 存取金鑰組](https://docs.aws.amazon.com/keyspaces/latest/devguide/create.keypair.html)。

### Azure

**Azure 託管 Snowflake 帳戶的暫存 Azure Blob 儲存體容器**

如果是 Azure 託管的 Snowflake 帳戶，請建立 Azure Blob 儲存體容器，暫存 Snowflake 資料，然後再載入 BigQuery。

1. [建立 Azure 儲存體帳戶](https://learn.microsoft.com/en-us/azure/storage/common/storage-account-create)，並在其中建立[儲存體容器](https://learn.microsoft.com/en-us/azure/storage/blobs/blob-containers-portal#create-a-container)。
2. [建立及設定 Snowflake 儲存空間整合物件](https://docs.snowflake.com/en/user-guide/data-load-azure-config#option-1-configuring-a-snowflake-storage-integration)，允許 Snowflake 將資料寫入 Azure 儲存空間容器，做為外部階段。請注意，由於我們不會使用「步驟 3：建立外部階段」，因此可以略過。

如要允許讀取 Azure 容器，請[為該容器產生 SAS 權杖](https://learn.microsoft.com/en-us/azure/ai-services/translator/document-translation/how-to-guides/create-sas-tokens?tabs=Containers#create-sas-tokens-in-the-azure-portal)。

### Google Cloud

**Google Cloud代管 Snowflake 帳戶的暫存 bucket**

如果是 Google Cloud代管的 Snowflake 帳戶，請建立 Cloud Storage bucket，暫存 Snowflake 資料，再載入 BigQuery。

1. [建立 Cloud Storage bucket](https://docs.cloud.google.com/storage/docs/creating-buckets?hl=zh-tw)。
2. [建立及設定 Snowflake 儲存空間整合物件](https://docs.snowflake.com/en/user-guide/data-load-gcs-config)，允許 Snowflake 將資料寫入 Cloud Storage bucket 做為外部階段。
3. 如要允許存取暫存 bucket，請使用下列指令，將 `roles/storage.objectViewer` 角色授予 [DTS 服務代理](https://docs.cloud.google.com/bigquery/docs/enable-transfer-service?hl=zh-tw#service_agent)：

   ```
   gcloud storage buckets add-iam-policy-binding gs://STAGING_BUCKET_NAME \
     --member=serviceAccount:service-PROJECT_NUMBER@gcp-sa-bigquerydatatransfer.iam.gserviceaccount.com \
     --role=roles/storage.objectViewer
   ```

### 建立具備必要權限的 Snowflake 使用者

在 Snowflake 轉移期間，Snowflake 連接器會使用 JDBC 連線連至 Snowflake 帳戶。您必須建立新的 Snowflake 使用者，並指派自訂角色，該角色只能具備執行資料移轉所需的權限：

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
    ON STORAGE_INTEGRATION_OBJECT_NAME
    TO ROLE MIGRATION_ROLE;
```

更改下列內容：

* `MIGRATION_ROLE`：要建立的自訂角色名稱
* `WAREHOUSE_NAME`：資料倉儲名稱
* `DATABASE_NAME`：Snowflake 資料庫名稱
* `SCHEMA_NAME`：Snowflake 結構定義的名稱
* `TABLE_NAME`：此資料移轉中包含的 Snowflake 名稱
* `STORAGE_INTEGRATION_OBJECT_NAME`：Snowflake 儲存空間整合物件的名稱。

#### 產生用於驗證的金鑰組

由於 [Snowflake 已淘汰單一因素密碼登入功能](https://docs.snowflake.com/en/user-guide/security-mfa-rollout)，建議您使用金鑰組進行驗證。

您可以產生加密或未加密的 RSA 金鑰組，然後將公開金鑰指派給 Snowflake 使用者，藉此設定金鑰組。詳情請參閱「[設定金鑰配對驗證](https://docs.snowflake.com/en/user-guide/key-pair-auth#configuring-key-pair-authentication)」。

### 新增聯播網政策

如要使用公開連線，Snowflake 帳戶預設允許透過資料庫憑證進行公開連線。不過，您可能已設定網路規則或政策，導致 Snowflake 連接器無法連線至帳戶。在這種情況下，您必須將必要的 IP 位址加入許可清單。詳情請參閱「[設定 Snowflake 轉移作業的網路政策](https://docs.cloud.google.com/bigquery/docs/migration/snowflake-network-policies?hl=zh-tw)」。

### 偵測及對應結構定義

如要定義結構定義，您可以使用 BigQuery 資料移轉服務，在將資料從 Snowflake 移轉至 BigQuery 時，自動偵測結構定義和資料類型對應。或者，您也可以使用翻譯引擎手動定義架構和資料類型。

詳情請參閱「[Snowflake 的結構定義偵測和對應](https://docs.cloud.google.com/bigquery/docs/migration/snowflake-transfer-schema?hl=zh-tw)」。

### 啟用遞增式轉移

如要設定 Snowflake 資料的增量移轉，請參閱[設定 Snowflake 的增量移轉](https://docs.cloud.google.com/bigquery/docs/migration/snowflake-incremental?hl=zh-tw)。

### 啟用私人連線

如要建立私人的 Snowflake 資料移轉作業，請務必[設定網路以進行私人連線](https://docs.cloud.google.com/bigquery/docs/migration/snowflake-private-connectivity?hl=zh-tw)。

### 收集轉移資訊

收集使用 BigQuery 資料移轉服務設定遷移作業所需的資訊：

* 您的 Snowflake 帳戶 ID，也就是 Snowflake 帳戶網址中的前置碼。例如 `ACCOUNT_IDENTIFIER.snowflakecomputing.com`。
* 使用者名稱和相關聯的私密金鑰，須具備 Snowflake 資料庫的適當權限。只要具備[執行資料移轉作業的必要權限](#create-snowflake-user)即可。
* 要用於轉移作業的暫存值區 URI：
  + 如果是 AWS 代管的 Snowflake 帳戶，則必須提供 [Amazon S3 bucket URI](#preparing-s3-bucket) 和存取憑證。
  + 如果是 Azure 託管的 Snowflake，則需要 [Azure Blob 儲存體帳戶和容器](#preparing-azure-container)。
  + 如果是Google Cloud代管的 Snowflake 帳戶，則必須提供 [Cloud Storage 值區 URI](#preparing-gcs-bucket)。建議您為這個值區設定生命週期政策，避免產生不必要的費用。
* Cloud Storage 值區的 URI，您已在其中儲存[從翻譯引擎取得的結構定義對應檔](https://docs.cloud.google.com/bigquery/docs/migration/snowflake-transfer-schema?hl=zh-tw)。

## 設定 Snowflake 轉移作業

選取下列選項之一：

### 控制台

1. 前往 Google Cloud 控制台的「資料移轉」頁面。

   [前往「資料轉移」頁面](https://console.cloud.google.com/bigquery/transfers?hl=zh-tw)
2. 按一下 add「建立轉移作業」。
3. 在「來源類型」部分，從「來源」清單中選取「Snowflake 遷移」。
4. 在「Transfer config name」(轉移設定名稱) 區段中，於「Display name」(顯示名稱) 欄位輸入移轉作業的名稱，例如 `My migration`。顯示名稱可以是任意值，日後需要修改移轉作業時，能夠據此識別即可。
5. 在「Destination settings」(目的地設定) 部分，從「Dataset」(資料集) 清單中選擇[您建立的資料集](#preparing-gcp-project)。
6. 在「Snowflake Credentials」(Snowflake 憑證) 部分，執行下列操作：

   1. 在「帳戶 ID」中，輸入 Snowflake 帳戶的專屬 ID，也就是機構名稱和帳戶名稱的組合。這個 ID 是 Snowflake 帳戶網址的前置字元，而非完整網址。例如：`ACCOUNT_IDENTIFIER.snowflakecomputing.com`。
   2. 在「Username」(使用者名稱) 中，輸入 Snowflake 使用者名稱。系統會使用該使用者的憑證和授權，存取資料庫以轉移 Snowflake 資料表。建議您[使用為這項轉移作業建立的使用者](#create-snowflake-user)。
   3. 在「Authentication Mechanism」部分，選取 Snowflake 使用者驗證方法：

      ### 密碼

      * 在「Password」(密碼) 中輸入 Snowflake 使用者的密碼。

      ### KEY\_PAIR

      * 在「Private Key」(私密金鑰)，輸入與[與 Snowflake 使用者相關聯的公開金鑰](#create-snowflake-user)連結的私密金鑰。
      * 如要使用通關密語加密私密金鑰，請選取「Is Private Key Encrypted」(私密金鑰是否已加密) 欄位。
      * 在「Private Key Passphrase」(私密金鑰通關密語) 部分，輸入加密私密金鑰的通關密語。如果您已選取「私密金鑰是否經過加密」，就必須填寫這個欄位。
        詳情請參閱「[產生金鑰組以進行驗證](#generate_key_pair_for_authentication)」。
   * 在「Warehouse」中，輸入用於執行這項資料移轉作業的[倉庫](https://docs.snowflake.com/en/user-guide/warehouses-tasks)。
   * 在「Snowflake Database」(Snowflake 資料庫) 中，輸入包含此資料移轉所含資料表的 Snowflake 資料庫名稱。
   * 在「Snowflake Schema」(Snowflake 結構定義) 中，輸入包含此資料移轉作業所含資料表的 Snowflake 結構定義名稱。
7. 在「儲存空間設定」部分，執行下列操作：

   1. 在「Storage integration object name」(儲存空間整合物件名稱) 中，輸入 Snowflake 儲存空間整合物件的名稱。
   2. 選用：在「檔案大小上限」中，指定從 Snowflake 卸載至暫存位置的每個檔案大小上限 (以 MB 為單位)。
   3. 在「Cloud Provider」(雲端服務供應商) 部分，根據代管 Snowflake 帳戶的雲端服務供應商，選取 `AWS`、`AZURE` 或 `GCP`。

      ### AWS

      * 在「Amazon S3 URI」部分，輸入將做為暫存區使用的 [Amazon S3 值區的 URI](#preparing-s3-bucket)。
      * 在「Access key ID」(存取金鑰 ID) 和「Secret access key」(存取密鑰) 部分，輸入[存取金鑰組](#snowflake_key_pair)。

      ### Azure

      * 在「Azure storage account name」(Azure 儲存體帳戶名稱)和「The container in the Azure storage account」(Azure 儲存體帳戶中的容器)，輸入[要用做暫存區的 Azure Blob 儲存體帳戶和容器名稱](#preparing-azure-container)。
      * 在「SAS Token」(SAS 權杖)  部分，輸入[為容器產生的 SAS 權杖](#azure_sas_token)。

      ### Google Cloud

      * 在「GCS URI」部分，輸入將做為暫存區使用的 [Cloud Storage URI](#preparing-gcs-bucket)。
8. 在「服務帳戶」部分執行下列操作：

   1. 在「服務帳戶」中，輸入要用於這項資料移轉作業的服務帳戶。服務帳戶應屬於移轉設定和目的地資料集建立所在的Google Cloud 專案。服務帳戶必須具備 `storage.objects.list` 和 `storage.objects.get` [必要權限](https://docs.cloud.google.com/bigquery/docs/migration/snowflake-transfer-schema?hl=zh-tw#required_service_account_permissions)。
9. 在「結構定義設定」部分，執行下列操作：

   1. 在「Ingestion type」(擷取類型) 部分，選取「Full」(完整) 或「Incremental」(增量)。詳情請參閱「[設定累加式轉移作業](https://docs.cloud.google.com/bigquery/docs/migration/snowflake-incremental?hl=zh-tw#configure_incremental_transfers)」。
   2. 在「Table name patterns」(資料表名稱格式) 部分，輸入符合結構定義中資料表名稱的名稱或格式，指定要移轉的資料表。您可以使用規則運算式指定模式，例如 `table1_regex;table2_regex`。此格式必須遵循 Java 規則運算式語法。例如：
      * `lineitem;ordertb` 會比對名為 `lineitem` 和 `ordertb` 的資料表。
      * `.*` 會比對所有資料表。
   3. 選用：如要「使用 BigQuery Translation Engine 輸出」，請選取這個欄位，指定自訂的翻譯輸出路徑。
   4. 選用：在「翻譯輸出 GCS 路徑」中，指定 Cloud Storage 資料夾的路徑，該資料夾包含[翻譯引擎的結構對應檔案](https://docs.cloud.google.com/bigquery/docs/migration/snowflake-transfer-schema?hl=zh-tw)。您可以將此欄位留空，讓 Snowflake 連接器自動偵測結構定義。
      * 路徑應採用 `translation_target_base_uri/metadata/config/db/schema/` 格式，且結尾必須為 `/`。
   5. 選用：在「自訂架構檔案路徑」中，指定自訂架構檔案的 Cloud Storage 路徑。
   6. 選用：如要將零比例的 Snowflake NUMBER 對應至 BigQuery INT64，請選取這個欄位，將 Snowflake `NUMBER(p, 0)` 型別對應至 BigQuery `INT64`。
10. 在「網路連線」部分，執行下列操作：

    1. 如要**使用私人網路**，請在建立[私人資料轉移](https://docs.cloud.google.com/bigquery/docs/migration/snowflake-private-connectivity?hl=zh-tw)時選取「True」。
    2. 如果是 **PSC 服務連結**，請輸入服務連結 URI (如要建立私人連線)。詳情請參閱「[建立私有 Snowflake 轉移設定](https://docs.cloud.google.com/bigquery/docs/migration/snowflake-private-connectivity?hl=zh-tw#create-transfer-config)」。
    3. 如果是 **Private Network Service**，請輸入服務目錄的自我連結，建立私人資料移轉作業。詳情請參閱「[建立私有 Snowflake 轉移設定](https://docs.cloud.google.com/bigquery/docs/migration/snowflake-private-connectivity?hl=zh-tw#create-transfer-config)」。
11. 選用：在「Notification options」(通知選項) 專區，執行下列操作：

    1. 按一下啟用電子郵件通知的切換開關。啟用這個選項之後，若移轉失敗，移轉作業管理員就會收到電子郵件通知。
    2. 在「Select a Pub/Sub topic」(選取 Pub/Sub 主題) 選取[主題](https://docs.cloud.google.com/pubsub/docs/overview?hl=zh-tw#types)名稱，或是點選「Create a topic」(建立主題)。這個選項會針對移轉作業設定 Pub/Sub 執行[通知](https://docs.cloud.google.com/bigquery/docs/transfer-run-notifications?hl=zh-tw)。
12. 如果使用 [CMEK](https://docs.cloud.google.com/bigquery/docs/customer-managed-encryption?hl=zh-tw)，請在「Advanced options」(進階選項) 部分選取「Customer-managed key」(客戶管理的金鑰)。畫面隨即會列出可用的 CMEK 供您選擇。如要瞭解 CMEK 如何與 BigQuery 資料移轉服務搭配運作，請參閱[指定移轉作業加密金鑰](#CMEK)的相關說明。
13. 按一下 [儲存]。
14. Google Cloud 控制台會顯示移轉設定的所有詳細資料，包括此移轉作業的「Resource name」(資源名稱)。

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
    --project_id=project_id \
    --data_source=data_source \
    --target_dataset=dataset \
    --display_name=name \
    --service_account_name=service_account \
    --params='parameters'
```

更改下列內容：

* project\_id：您的 Google Cloud 專案 ID。如果未指定 `--project_id`，系統會使用預設專案。
* data\_source：資料來源 `snowflake_migration`。
* dataset：移轉設定的 BigQuery 目標資料集。
* name：移轉設定的顯示名稱。移轉作業名稱可以是任意值，日後需要修改移轉作業時，能夠據此識別即可。
* service\_account：(選用) 用於驗證轉移作業的服務帳戶名稱。服務帳戶應由用於建立移轉作業的 `project_id` 擁有，且應具備所有[必要角色](#required-roles)。
* parameters：已建立移轉設定的 JSON 格式參數。例如：`--params='{"param":"param_value"}'`。

您可以為 Snowflake 轉移設定下列參數：

* `account_identifier`：指定 Snowflake 帳戶的專屬 ID，也就是機構名稱和帳戶名稱的組合。這個 ID 是 Snowflake 帳戶網址的前置字元，而非完整網址。例如：`account_identifier.snowflakecomputing.com`。
* `username`：指定 Snowflake 使用者的使用者名稱，系統會使用該使用者的憑證和授權存取資料庫，以轉移 Snowflake 資料表。
* `auth_mechanism`：指定 Snowflake 使用者驗證方法。
  支援的值為 `PASSWORD` 和 `KEY_PAIR`。詳情請參閱「[產生驗證用的金鑰組](#generate_key_pair_for_authentication)」。
* `password`：指定 Snowflake 使用者的密碼。如果您在 `auth_mechanism` 欄位中指定 `PASSWORD`，則此欄位為必填欄位。
* `private_key`：指定與[與 Snowflake 使用者相關聯的公開金鑰](#create-snowflake-user)連結的私密金鑰。如果您在 `auth_mechanism` 欄位中指定 `KEY_PAIR`，則此欄位為必填欄位。
* `is_private_key_encrypted`：如果私密金鑰是以通關密語加密，請指定 `true`。
* `private_key_passphrase`：指定加密私密金鑰的通關密語。如果您在 `auth_mechanism` 欄位中指定 `KEY_PAIR`，並在 `is_private_key_encrypted` 欄位中指定 `true`，則此為必填欄位。
* `warehouse`：指定用於執行這項資料移轉作業的[倉庫](https://docs.snowflake.com/en/user-guide/warehouses-tasks)。
* `service_account`：指定要用於這項資料移轉作業的服務帳戶。服務帳戶應屬於建立移轉設定和目的地資料集的相同 Google Cloud 專案。服務帳戶必須具備 `storage.objects.list` 和 `storage.objects.get` [必要權限](https://docs.cloud.google.com/bigquery/docs/migration/snowflake-transfer-schema?hl=zh-tw#required_service_account_permissions)。
* `database`：指定包含此資料轉移作業所用資料表的 Snowflake 資料庫名稱。
* `schema`：指定包含此資料移轉所含資料表的 Snowflake 結構定義名稱。
* `table_name_patterns`：輸入名稱或符合結構定義中資料表名稱的格式，指定要轉移的資料表。您可以使用規則運算式指定模式，例如 `table1_regex;table2_regex`。此格式必須遵循 Java 規則運算式語法。例如，假設使用者要求系統
  將文字從英文翻譯成法文

  + `lineitem;ordertb` 會比對名為 `lineitem` 和 `ordertb` 的資料表。
  + `.*` 會比對所有資料表。

    您也可以將這個欄位留白，用以遷移所有來自指定結構定義的資料表。
* `ingestion_mode`：指定轉移的擷取模式。支援的值為 `FULL` 和 `INCREMENTAL`。詳情請參閱「[設定增量轉移](https://docs.cloud.google.com/bigquery/docs/migration/snowflake-incremental?hl=zh-tw#configure_incremental_transfers)」。
* `translation_output_gcs_path`：(選用) 指定 Cloud Storage 資料夾的路徑，該資料夾包含[翻譯引擎的結構定義對應檔案](https://docs.cloud.google.com/bigquery/docs/migration/snowflake-transfer-schema?hl=zh-tw)。您可以將此欄位留空，讓 Snowflake 連接器自動偵測結構定義。

  + 路徑應採用 `gs://translation_target_base_uri/metadata/config/db/schema/` 格式，且結尾必須為 `/`。
* `storage_integration_object_name`：指定 Snowflake 儲存空間整合物件的名稱。
* `cloud_provider`：輸入 `AWS`、`AZURE` 或 `GCP`，視代管 Snowflake 帳戶的雲端服務供應商而定。
* `staging_s3_uri`：輸入將做為暫存區使用的 [S3 值區 URI](#preparing-s3-bucket)。只有在 `cloud_provider` 為 `AWS` 時才需要。
* `aws_access_key_id`：輸入[存取金鑰組](#snowflake_key_pair)。只有在 `cloud_provider` 為 `AWS` 時才需要。
* `aws_secret_access_key`：輸入[存取金鑰組](#snowflake_key_pair)。只有在 `cloud_provider` 為 `AWS` 時才需要。
* `azure_storage_account`：輸入要用做暫存區的[儲存空間帳戶名稱](#preparing-azure-container)。只有在 `cloud_provider` 為 `AZURE` 時才需要。
* `staging_azure_container`：輸入[Azure Blob 儲存體中的容器](#preparing-azure-container)，做為暫存區。只有在 `cloud_provider` 為 `AZURE` 時才需要。
* `azure_sas_token`：輸入 [SAS 權杖](#azure_sas_token)。只有在 `cloud_provider` 為 `AZURE` 時才需要。
* `staging_gcs_uri`：輸入要用做暫存區的 [Cloud Storage URI](#preparing-gcs-bucket)。只有在 `cloud_provider` 為 `GCP` 時才需要。
* `use_private_network`：如要建立[私人資料轉移](https://docs.cloud.google.com/bigquery/docs/migration/snowflake-private-connectivity?hl=zh-tw)，請設為 `TRUE`。
* `service_attachment`：如要建立私人資料移轉作業，請指定服務連結 URI。詳情請參閱「[建立私人 Snowflake 轉移設定](https://docs.cloud.google.com/bigquery/docs/migration/snowflake-private-connectivity?hl=zh-tw#create-transfer-config)」。
* `private_network_service`：如果您要建立私人資料移轉作業，請指定 NLB 服務的自我連結。詳情請參閱「[建立私有 Snowflake 轉移設定](https://docs.cloud.google.com/bigquery/docs/migration/snowflake-private-connectivity?hl=zh-tw#create-transfer-config)」。

舉例來說，如果是 AWS 代管的 Snowflake 帳戶，下列指令會建立名為 `Snowflake transfer config` 的 Snowflake 移轉作業，其中目標資料集的名稱為 `your_bq_dataset`，專案的 ID 為 `your_project_id`。

```
  PARAMS='{
  "account_identifier": "your_account_identifier",
  "auth_mechanism": "KEY_PAIR",
  "aws_access_key_id": "your_access_key_id",
  "aws_secret_access_key": "your_aws_secret_access_key",
  "cloud_provider": "AWS",
  "database": "your_sf_database",
  "ingestion_mode": "INCREMENTAL",
  "private_key": "-----BEGIN PRIVATE KEY----- privatekey\nseparatedwith\nnewlinecharacters=-----END PRIVATE KEY-----",
  "schema": "your_snowflake_schema",
  "service_account": "your_service_account",
  "storage_integration_object_name": "your_storage_integration_object",
  "staging_s3_uri": "s3://your/s3/bucket/uri",
  "table_name_patterns": ".*",
  "translation_output_gcs_path": "gs://sf_test_translation/output/metadata/config/database_name/schema_name/",
  "username": "your_sf_username",
  "warehouse": "your_warehouse"
}'

bq mk --transfer_config \
    --project_id=your_project_id \
    --target_dataset=your_bq_dataset \
    --display_name='snowflake transfer config' \
    --params="$PARAMS" \
    --data_source=snowflake_migration
```

**注意：** 您無法使用指令列工具設定通知。

### API

請使用 [`projects.locations.transferConfigs.create`](https://docs.cloud.google.com/bigquery/docs/reference/datatransfer/rest/v1/projects.locations.transferConfigs/create?hl=zh-tw) 方法，並提供 [`TransferConfig`](https://docs.cloud.google.com/bigquery/docs/reference/datatransfer/rest/v1/projects.locations.transferConfigs?hl=zh-tw#TransferConfig) 資源的執行個體。

如果為同一個 Snowflake 資料表建立多次移轉作業，或多次執行相同的移轉設定，現有 BigQuery 目的地資料表中的資料就會遭到覆寫。

## 指定轉移作業的加密金鑰

您可以指定[客戶自行管理的加密金鑰 (CMEK)](https://docs.cloud.google.com/kms/docs/cmek?hl=zh-tw)，加密轉移作業的資料。您可以使用 CMEK 支援從 [Snowflake](https://docs.cloud.google.com/bigquery/docs/migration/snowflake-migration-intro?hl=zh-tw) 轉移資料。

指定移轉作業的 CMEK 後，BigQuery 資料移轉服務會將 CMEK 套用至所有已擷取資料的中間磁碟快取，確保整個資料移轉工作流程符合 CMEK 規定。

如果轉移作業最初並非使用 CMEK 建立，您就無法更新現有轉移作業來新增 CMEK。舉例來說，您無法將原本預設加密的目的地資料表，變更為使用 CMEK 加密。反之，您也無法將 CMEK 加密的目的地資料表變更為其他類型的加密。

如果移轉設定最初是使用 CMEK 加密功能建立，您可以更新移轉的 CMEK。更新移轉作業設定的 CMEK 時，BigQuery 資料移轉服務會在下次執行移轉作業時，將 CMEK 傳播至目的地資料表。屆時，BigQuery 資料移轉服務會在移轉作業執行期間，以新的 CMEK 取代任何過時的 CMEK。詳情請參閱「[更新轉移作業](https://docs.cloud.google.com/bigquery/docs/working-with-transfers?hl=zh-tw#update_a_transfer)」。

您也可以使用[專案預設金鑰](https://docs.cloud.google.com/bigquery/docs/customer-managed-encryption?hl=zh-tw#project_default_key)。
使用移轉作業指定專案預設金鑰時，BigQuery 資料移轉服務會將專案預設金鑰做為任何新移轉作業設定的預設金鑰。

**注意：** 如果是 Snowflake 移轉作業，CMEK 加密會處理 BigQuery 目的地資料表中的資料加密，以及移轉程序中使用的中繼 Cloud Storage 租戶 bucket 資料加密，適用於 Amazon S3 或 Azure Blob Storage 上的 Snowflake。

## 配額與限制

根據預設，每個資料表之每個載入工作的 BigQuery 載入配額皆為 15 TB。Snowflake 會在內部壓縮資料表資料，因此匯出的資料表大小會大於 Snowflake 回報的資料表大小。

如要縮短大型資料表的載入時間，請為預留項目指派指定[`PIPELINE`工作類型](https://docs.cloud.google.com/bigquery/docs/migration/snowflake-transfer?hl=zh-tw#quotas_and_limits)。

由於 [Amazon S3 的一致性模型](https://docs.cloud.google.com/bigquery/docs/s3-transfer-intro?hl=zh-tw#consistency_considerations)，您可以在移轉到 BigQuery 時不納入部分檔案。

## 提升資料移轉效能

您可以查看[資料移轉記錄](https://docs.cloud.google.com/bigquery/docs/dts-monitor?hl=zh-tw)，監控資料移轉作業的效能。為提升資料移轉效能，建議您執行下列最佳化步驟：

* 將 Snowflake 執行個體、暫存值區和 BigQuery 資料集放在同一區域
* 您可以透過下列方式提升資料表卸載速度：
  + 增加 Snowflake 虛擬倉庫的大小，特別是在傳輸大型 Snowflake 表格 (1 TiB 以上) 時。
  + 調整轉移設定中的 `MAX_FILE_SIZE` 選項。
    - 檔案越小，傳輸速度就越快，但如果檔案太小，可能會導致檔案數量過多。
* 如要提升資料表載入速度，請增加 `PIPELINE` 和 `QUERY` 工作類型的 BigQuery 運算單元預留項目數量。
* 進行完整轉移時，請避免在目的地 BigQuery 資料表上進行叢集和分割。
* 以 Upsert 模式進行增量轉移時，請考慮在主鍵資料欄上進行叢集化和分區，以提升轉移效能。
  + 不過，請避免在非主鍵資料欄上進行分區和分割，以免合併作業速度變慢。

## 定價

如要瞭解 BigQuery 資料移轉服務定價，請參閱[定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#data-transfer-service-pricing)頁面。

* 如果 Snowflake 倉庫和 Amazon S3 值區位於不同區域，執行 Snowflake 資料移轉作業時，Snowflake 會收取輸出費用。如果 Snowflake 倉儲和 Amazon S3 值區位於同一區域，則 Snowflake 資料移轉不會產生輸出費用。
* 從 AWS 移轉資料至 Google Cloud時，須支付跨雲端輸出費用。

## 後續步驟

* 進一步瞭解 [BigQuery 資料移轉服務](https://docs.cloud.google.com/bigquery/docs/transfer-service-overview?hl=zh-tw)。
* 使用[批次 SQL 轉譯](https://docs.cloud.google.com/bigquery/docs/batch-sql-translator?hl=zh-tw)功能遷移 SQL 程式碼。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-14 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-14 (世界標準時間)。"],[],[]]