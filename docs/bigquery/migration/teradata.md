* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [參考資料](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 從 Teradata 遷移結構定義和資料

只要搭配使用 BigQuery 資料移轉服務與特別的遷移代理程式，您就能將 Teradata 地端部署資料倉儲執行個體中的資料複製到 BigQuery。本文將逐步說明如何使用 BigQuery 資料移轉服務，從 Teradata 遷移資料。

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
- Enable the BigQuery, BigQuery Data Transfer Service, Cloud Storage, and Pub/Sub APIs.

  **Roles required to enable APIs**

  To enable APIs, you need the Service Usage Admin IAM
  role (`roles/serviceusage.serviceUsageAdmin`), which
  contains the `serviceusage.services.enable` permission. [Learn how to grant
  roles](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw).

  [Enable the APIs](https://console.cloud.google.com/flows/enableapi?apiid=bigquery.googleapis.com%2Cbigquerydatatransfer.googleapis.com%2Cstorage-component.googleapis.com%2Cpubsub.googleapis.com&hl=zh-tw)
- Create a service account:

  1. Ensure that you have the Create Service Accounts IAM role
     (`roles/iam.serviceAccountCreator`) and the Project IAM Admin role
     (`roles/resourcemanager.projectIamAdmin`). [Learn how to grant
     roles](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw).
  2. In the Google Cloud console, go to the **Create service account** page.

     [Go to Create service account](https://console.cloud.google.com/projectselector/iam-admin/serviceaccounts/create?supportedpurview=project&hl=zh-tw)
  3. Select your project.
  4. In the **Service account name** field, enter a name. The Google Cloud console fills
     in the **Service account ID** field based on this name.

     In the **Service account description** field, enter a description. For example,
     `Service account for quickstart`.
  5. Click **Create and continue**.
  6. Grant the following roles to the service account:
     **roles/bigquery.user, roles/storage.objectAdmin, roles/iam.serviceAccountTokenCreator**.

     To grant a role, find the **Select a role** list, then select the role.

     To grant additional roles, click add **Add another
     role** and add each additional role.

     **Note**: The **Role** field affects which resources the service account can access in your
     project. You can revoke these roles or grant additional roles later.
  7. Click **Continue**.
  8. Click **Done** to finish creating the service account.

     Do not close your browser window. You will use it in the next step.
- Create a service account key:

  1. In the Google Cloud console, click the email address for the service account that you
     created.
  2. Click **Keys**.
  3. Click **Add key**, and then click **Create new key**.
  4. Click **Create**. A JSON key file is downloaded to your computer.
  5. Click **Close**.

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
- Enable the BigQuery, BigQuery Data Transfer Service, Cloud Storage, and Pub/Sub APIs.

  **Roles required to enable APIs**

  To enable APIs, you need the Service Usage Admin IAM
  role (`roles/serviceusage.serviceUsageAdmin`), which
  contains the `serviceusage.services.enable` permission. [Learn how to grant
  roles](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw).

  [Enable the APIs](https://console.cloud.google.com/flows/enableapi?apiid=bigquery.googleapis.com%2Cbigquerydatatransfer.googleapis.com%2Cstorage-component.googleapis.com%2Cpubsub.googleapis.com&hl=zh-tw)
- Create a service account:

  1. Ensure that you have the Create Service Accounts IAM role
     (`roles/iam.serviceAccountCreator`) and the Project IAM Admin role
     (`roles/resourcemanager.projectIamAdmin`). [Learn how to grant
     roles](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw).
  2. In the Google Cloud console, go to the **Create service account** page.

     [Go to Create service account](https://console.cloud.google.com/projectselector/iam-admin/serviceaccounts/create?supportedpurview=project&hl=zh-tw)
  3. Select your project.
  4. In the **Service account name** field, enter a name. The Google Cloud console fills
     in the **Service account ID** field based on this name.

     In the **Service account description** field, enter a description. For example,
     `Service account for quickstart`.
  5. Click **Create and continue**.
  6. Grant the following roles to the service account:
     **roles/bigquery.user, roles/storage.objectAdmin, roles/iam.serviceAccountTokenCreator**.

     To grant a role, find the **Select a role** list, then select the role.

     To grant additional roles, click add **Add another
     role** and add each additional role.

     **Note**: The **Role** field affects which resources the service account can access in your
     project. You can revoke these roles or grant additional roles later.
  7. Click **Continue**.
  8. Click **Done** to finish creating the service account.

     Do not close your browser window. You will use it in the next step.
- Create a service account key:

  1. In the Google Cloud console, click the email address for the service account that you
     created.
  2. Click **Keys**.
  3. Click **Add key**, and then click **Create new key**.
  4. Click **Create**. A JSON key file is downloaded to your computer.
  5. Click **Close**.


如未妥善管理服務帳戶金鑰，可能會產生安全性風險，您有責任保護私密金鑰的安全，並執行「[管理服務帳戶金鑰的最佳做法](https://docs.cloud.google.com/iam/docs/best-practices-for-managing-service-account-keys?hl=zh-tw)」一文所述的其他作業。假如無法建立服務帳戶金鑰，可能是因為貴組織已停用這項功能。詳情請參閱[這篇文章](https://docs.cloud.google.com/resource-manager/docs/secure-by-default-organizations?hl=zh-tw)。

如果您是從外部來源取得服務帳戶金鑰，必須先驗證金鑰，才能使用。詳情請參閱「[外部來源憑證的安全規定](https://docs.cloud.google.com/docs/authentication/external/externally-sourced-credentials?hl=zh-tw)」一節。

### 設定必要權限

請確認建立移轉作業的主體在包含移轉作業的專案中，具有下列角色：

* 記錄檢視者 (`roles/logging.viewer`)
* Storage 管理員 (`roles/storage.admin`)，或是授予下列權限的[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)：
  + `storage.objects.create`
  + `storage.objects.get`
  + `storage.objects.list`
* BigQuery 管理員 (`roles/bigquery.admin`)，或授予下列權限的自訂角色：
  + `bigquery.datasets.create`
  + `bigquery.jobs.create`
  + `bigquery.jobs.get`
  + `bigquery.jobs.listAll`
  + `bigquery.tables.get`
  + `bigquery.transfers.get`
  + `bigquery.transfers.update`

### 建立資料集

[建立 BigQuery 資料集](https://docs.cloud.google.com/bigquery/docs/datasets?hl=zh-tw)來儲存您的資料。您無須建立任何資料表。

### 建立 Cloud Storage 值區

[建立 Cloud Storage bucket](https://docs.cloud.google.com/storage/docs/creating-buckets?hl=zh-tw)，在移轉工作期間暫存資料。

### 準備本機環境

請完成本節中的工作，為轉移工作準備本機環境。

#### 本機需求條件

* 遷移代理程式會使用 JDBC 連線和 API 與 Teradata 執行個體互動。 Google Cloud 確認網路存取權未遭防火牆封鎖。
* 確認已安裝 Java Runtime Environment 8 以上版本。
* 請確認您選擇的擷取方法有足夠的儲存空間，詳情請參閱「[擷取方法](https://docs.cloud.google.com/bigquery/docs/migration/teradata-overview?hl=zh-tw#extraction_method)」。
* 如果您決定使用 Teradata Parallel Transporter (TPT) 擷取功能，請確認已安裝 [`tbuild`](https://docs.teradata.com/r/Teradata-Parallel-Transporter-Reference/July-2017/Teradata-PT-Utility-Commands/Command-Syntax/tbuild) 公用程式。如要進一步瞭解如何選擇擷取方法，請參閱「[擷取方法](https://docs.cloud.google.com/bigquery/docs/migration/teradata-overview?hl=zh-tw#extraction_method)」。

#### Teradata 連線詳細資料

* 請確認您擁有 Teradata 使用者的使用者名稱和密碼，且該使用者有權讀取系統資料表和要遷移的資料表。

  系統會透過提示擷取使用者名稱和密碼，且只會儲存在 RAM 中。您也可以選擇在後續步驟中，為使用者名稱或密碼建立憑證檔案。使用憑證檔案時，請採取適當步驟來控管對本機檔案系統中儲存憑證檔案的資料夾的存取權，因為憑證檔案未經過加密。
* 請務必知道要連線至 Teradata 執行個體的主機名稱和通訊埠編號。

  系統不支援 LDAP 等驗證模式。

#### 下載 JDBC 驅動程式

從 Teradata [下載](https://downloads.teradata.com/download/connectivity/jdbc-driver) `terajdbc4.jar` JDBC 驅動程式檔案，並儲存到可連線至資料倉儲的電腦。

#### 設定 `GOOGLE_APPLICATION_CREDENTIALS` 變數

[將環境變數 `GOOGLE_APPLICATION_CREDENTIALS`](https://docs.cloud.google.com/docs/authentication/set-up-adc-local-dev-environment?hl=zh-tw#local-key) 設定為您在「[事前準備](#before_you_begin)」一節中下載的服務帳戶金鑰。

### 更新 VPC Service Controls 輸出規則

在 VPC Service Controls 邊界中，將 BigQuery 資料移轉服務代管 Google Cloud 專案 (專案編號：990232121269) 新增至[輸出規則](https://docs.cloud.google.com/vpc-service-controls/docs/ingress-egress-rules?hl=zh-tw#egress_rules_reference)。

在內部部署執行的代理程式與 BigQuery 資料移轉服務之間的通訊管道，是將 Pub/Sub 訊息發布至每個移轉主題。BigQuery 資料移轉服務需要將指令傳送給代理程式，才能擷取資料；代理程式則需要將訊息發布回 BigQuery 資料移轉服務，才能更新狀態並傳回資料擷取回應。

### 建立自訂結構定義檔案

如要使用[自訂結構定義檔](https://docs.cloud.google.com/bigquery/docs/migration/teradata-overview?hl=zh-tw#custom_schema_file)，而非自動偵測結構定義，請手動建立結構定義檔，或在[初始化代理程式](#initialize_the_migration_agent)時，讓遷移代理程式為您建立。

如果您手動建立結構定義檔，並打算使用 Google Cloud 控制台建立轉移作業，請將結構定義檔上傳至 Cloud Storage bucket，並確定該 bucket 位於要進行轉移作業的專案中。

### 下載遷移代理程式

[將遷移代理程式下載](https://storage.googleapis.com/data_transfer_agent/latest/mirroring-agent.jar)到可連線至資料倉儲的機器。將遷移代理程式 JAR 檔案移至與 Teradata JDBC 驅動程式 JAR 檔案相同的目錄。

### 設定存取模組的憑證檔案

如果您使用 [Teradata Parallel Transporter (TPT) 公用程式的 Cloud Storage 存取模組](https://docs.cloud.google.com/bigquery/docs/migration/teradata-overview?hl=zh-tw#extraction_method)進行擷取作業，則必須提供憑證檔案。

建立憑證檔案前，您必須[建立服務帳戶金鑰](https://docs.cloud.google.com/iam/docs/keys-create-delete?hl=zh-tw#creating)。從下載的服務帳戶金鑰檔案中，取得下列資訊：

* `client_email`
* `private_key`：複製 `-----BEGIN PRIVATE KEY-----` 和 `-----END PRIVATE KEY-----` 之間的所有字元，包括所有 `/n` 字元，但不含外圍的雙引號。

取得必要資訊後，請建立憑證檔案。以下是憑證檔案範例，預設位置為 `$HOME/.gcs/credentials`：

```
[default]
gcs_access_key_id = ACCESS_ID
gcs_secret_access_key = ACCESS_KEY
```

更改下列內容：

* `ACCESS_ID`：存取金鑰 ID，或服務帳戶金鑰檔案中的 `client_email` 值。
* `ACCESS_KEY`：私密存取金鑰，或服務帳戶金鑰檔案中的 `private_key` 值。

**注意：** [設定轉移作業](#set_up_a_transfer)時，您可以使用 `gcs-module-config-dir` 參數修改憑證檔案的位置。

## 設定轉移作業

使用 BigQuery 資料移轉服務建立移轉作業。

如要自動建立自訂結構定義檔案，請使用遷移代理程式設定轉移作業。

您無法使用 bq 指令列工具建立隨選移轉作業，必須改用 Google Cloud 控制台或 BigQuery 資料移轉服務 API。

如果您要建立週期性移轉作業，強烈建議您指定結構定義檔案，這樣後續移轉作業的資料載入 BigQuery 時，才能正確進行資料分割。如果沒有結構定義檔案，BigQuery 資料移轉服務會從要移轉的來源資料推斷資料表結構定義，但所有有關分割、叢集、主鍵和變更追蹤的資訊都會遺失。此外，後續轉移作業會略過初始轉移作業中已轉移的表格。如要進一步瞭解如何建立結構定義檔案，請參閱「[自訂結構定義檔案](https://docs.cloud.google.com/bigquery/docs/migration/teradata-overview?hl=zh-tw#custom_schema_file)」。

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往 BigQuery 頁面](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 按一下「資料移轉」。
3. 按一下 [Create Transfer] (建立移轉作業)。
4. 在「來源類型」部分，執行下列操作：

   * 選擇「遷移：Teradata」。
   * 在「Transfer config name」(轉移設定名稱) 部分，輸入移轉作業的顯示名稱，例如 `My Migration`。顯示名稱可以是任意值，日後需要修改移轉作業時能夠據此識別。
   * 選用：在「Schedule options」(排程選項) 中，您可以保留預設值「Daily」(每日) (以建立時間為準)，或選擇其他時間，進行週期性增量轉移。如果只要移轉一次，請選擇「隨選」。
   * 在「Destination settings」(目的地設定) 中，選擇適當的資料集。
5. 接著在「Data source details」(資料來源詳細資料) 部分，輸入 Teradata 移轉作業的特定詳細資料。

   * 在「資料庫類型」部分，選擇「Teradata」。
   * 在「Cloud Storage bucket」，瀏覽用來暫存移轉資料的 Cloud Storage bucket 名稱。請勿輸入前置字串 `gs://`，只要輸入 bucket 名稱即可。
   * 在「Database name」(資料庫名稱) 中，輸入 Teradata 來源資料庫的名稱。
   * 在「Table name patterns」(資料表名稱格式) 部分，輸入符合來源資料庫中資料表名稱的格式。您可以使用規則運算式指定模式。例如：

     + `sales|expenses` 會比對名為 `sales` 和 `expenses` 的資料表。
     + `.*` 會比對所有資料表。**注意：** 如要瞭解 Teradata 轉移作業的規則運算式語法，請參閱 [re2 程式庫](https://github.com/google/re2/wiki/Syntax)。
   * 在「服務帳戶電子郵件」部分，輸入與遷移代理程式所用服務帳戶憑證相關聯的電子郵件地址。
   * 選用：在「結構定義檔路徑」中，輸入自訂結構定義檔的路徑和檔案名稱。如要進一步瞭解如何建立自訂結構定義檔案，請參閱「[自訂結構定義檔案](https://docs.cloud.google.com/bigquery/docs/migration/teradata-overview?hl=zh-tw#custom_schema_file)」。您可以將這個欄位留空，讓 BigQuery [自動偵測來源資料表結構定義](https://docs.cloud.google.com/bigquery/docs/migration/teradata-overview?hl=zh-tw#default_schema_detection)。
   * 選用：在「翻譯輸出根目錄」部分，輸入 BigQuery 翻譯引擎提供的結構定義對應檔案路徑和檔案名稱。如要進一步瞭解如何產生結構定義對應檔案，請參閱「[使用翻譯引擎輸出內容進行結構定義](https://docs.cloud.google.com/bigquery/docs/migration/teradata-overview?hl=zh-tw#using_translation_engine_output_for_schema)」([預覽版](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages))。您可以將這個欄位留空，讓 BigQuery [自動偵測來源資料表結構定義](https://docs.cloud.google.com/bigquery/docs/migration/teradata-overview?hl=zh-tw#default_schema_detection)。
   * 選用：如要「啟用直接卸載至 GCS」，請選取核取方塊，啟用 [Cloud Storage 的存取模組](https://docs.cloud.google.com/bigquery/docs/migration/teradata-overview?hl=zh-tw#extraction_method)。
6. 在「Service Account」(服務帳戶) 選單，選取與貴機構Google Cloud 專案相關聯的[服務帳戶](https://docs.cloud.google.com/iam/docs/service-account-overview?hl=zh-tw)。您可以將服務帳戶與移轉作業建立關聯，這樣就不需要使用者憑證。如要進一步瞭解如何搭配使用服務帳戶與資料移轉作業，請參閱[使用服務帳戶](https://docs.cloud.google.com/bigquery/docs/use-service-accounts?hl=zh-tw)的相關說明。

   * 如果使用[聯合身分](https://docs.cloud.google.com/iam/docs/workforce-identity-federation?hl=zh-tw)登入，您必須擁有服務帳戶才能建立移轉作業。如果是以 [Google 帳戶](https://docs.cloud.google.com/iam/docs/principals-overview?hl=zh-tw#google-account)登入，則不一定要透過服務帳戶建立移轉作業。
   * 服務帳戶必須具備[必要權限](#set_required_permissions)。
7. 選用：在「Notification options」(通知選項) 專區，執行下列操作：

   * 如果希望移轉作業管理員在移轉作業失敗時收到電子郵件通知，請點選「電子郵件通知」切換按鈕。
   * 點選「Pub/Sub notifications」(Pub/Sub 通知) 切換按鈕，即可設定移轉作業的 Pub/Sub 執行[通知](https://docs.cloud.google.com/bigquery/docs/transfer-run-notifications?hl=zh-tw)。在「Select a Pub/Sub topic」(選取 Pub/Sub 主題)，選擇[主題](https://docs.cloud.google.com/pubsub/docs/overview?hl=zh-tw#types)名稱，或點選「Create a topic」(建立主題)。
8. 按一下 [儲存]。
9. 在「Transfer details」(移轉作業詳細資料) 頁面中，按一下「Configuration」(設定) 分頁標籤。
10. 請記下這項轉移作業的資源名稱，因為您需要這個名稱才能執行遷移代理程式。

### bq

使用 bq 工具建立 Cloud Storage 移轉作業時，系統會將移轉設定設為每 24 小時執行一次。如要進行隨選移轉，請使用 Google Cloud 控制台或 BigQuery 資料移轉服務 API。

您無法使用 bq 工具設定通知。

輸入 [`bq mk`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#mk-transfer-config) 指令並加上移轉建立作業旗標 `--transfer_config`。還需加上以下旗標：

* `--data_source`
* `--display_name`
* `--target_dataset`
* `--params`

```
bq mk \
--transfer_config \
--project_id=project ID \
--target_dataset=dataset \
--display_name=name \
--service_account_name=service_account \
--params='parameters' \
--data_source=data source
```

其中：

* project ID 是您的專案 ID。如未提供 `--project_id` 指定特定專案，系統會使用預設專案。
* dataset 是您要指定給移轉設定的資料集 (`--target_dataset`)。
* name 是移轉設定的顯示名稱 (`--display_name`)。移轉作業的顯示名稱可以是任意值，日後需要修改移轉作業時，能夠據此識別即可。
* service\_account 是用於驗證移轉作業的服務帳戶名稱。服務帳戶應由用於建立轉移作業的 `project_id` 所擁有，且應具備所有列出的[必要權限](#set_required_permissions)。
* parameters 含有已建立移轉設定的 JSON 格式參數 (`--params`)。例如 `--params='{"param":"param_value"}'`。
  + 如要遷移 Teradata，請使用下列參數：
    - `bucket` 是 Cloud Storage bucket，在遷移期間會做為暫存區。
    - `database_type` 是 Teradata。
    - `agent_service_account` 是與您建立的服務帳戶相關聯的電子郵件地址。
    - `database_name` 是 Teradata 中的來源資料庫名稱。
    - `table_name_patterns` 是用來比對來源資料庫中資料表名稱的模式。您可以使用規則運算式指定模式。此模式必須遵循 Java 規則運算式語法。例如：
      * `sales|expenses` 會比對名為 `sales` 和 `expenses` 的資料表。
      * `.*` 會比對所有資料表。
    - `is_direct_gcs_unload_enabled` 是布林值旗標，可啟用直接卸載至 Cloud Storage 的功能。
* data\_source 是資料來源 (`--data_source`)：`on_premises`。

舉例來說，下列指令會使用 Cloud Storage bucket `mybucket` 和目標資料集 `mydataset`，建立名為 `My Transfer` 的 Teradata 移轉作業。這項轉移作業會遷移 Teradata 資料倉儲 `mydatabase` 中的所有資料表，以及選用的結構定義檔案 `myschemafile.json`。

```
bq mk \
--transfer_config \
--project_id=123456789876 \
--target_dataset=MyDataset \
--display_name='My Migration' \
--params='{"bucket": "mybucket", "database_type": "Teradata",
"database_name":"mydatabase", "table_name_patterns": ".*",
"agent_service_account":"myemail@mydomain.com", "schema_file_path":
"gs://mybucket/myschemafile.json", "is_direct_gcs_unload_enabled": true}' \
--data_source=on_premises
```

執行指令後，您會收到如下的訊息：

`[URL omitted] Please copy and paste the above URL into your web browser and
follow the instructions to retrieve an authentication code.`

請按照指示進行操作，並在指令列中貼上驗證碼。

### API

請使用 [`projects.locations.transferConfigs.create`](https://docs.cloud.google.com/bigquery/docs/reference/datatransfer/rest/v1/projects.locations.transferConfigs/create?hl=zh-tw) 方法，並提供 [`TransferConfig`](https://docs.cloud.google.com/bigquery/docs/reference/datatransfer/rest/v1/projects.locations.transferConfigs?hl=zh-tw#TransferConfig) 資源的執行個體。

### Java

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Java 設定說明操作。詳情請參閱 [BigQuery Java API 參考說明文件](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/overview?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import com.google.api.gax.rpc.ApiException;
import com.google.cloud.bigquery.datatransfer.v1.CreateTransferConfigRequest;
import com.google.cloud.bigquery.datatransfer.v1.DataTransferServiceClient;
import com.google.cloud.bigquery.datatransfer.v1.ProjectName;
import com.google.cloud.bigquery.datatransfer.v1.TransferConfig;
import com.google.protobuf.Struct;
import com.google.protobuf.Value;
import java.io.IOException;
import java.util.HashMap;
import java.util.Map;

// Sample to create a teradata transfer config.
public class CreateTeradataTransfer {

  public static void main(String[] args) throws IOException {
    // TODO(developer): Replace these variables before running the sample.
    final String projectId = "MY_PROJECT_ID";
    String datasetId = "MY_DATASET_ID";
    String databaseType = "Teradata";
    String bucket = "cloud-sample-data";
    String databaseName = "MY_DATABASE_NAME";
    String tableNamePatterns = "*";
    String serviceAccount = "MY_SERVICE_ACCOUNT";
    String schemaFilePath = "/your-schema-path";
    Map<String, Value> params = new HashMap<>();
    params.put("database_type", Value.newBuilder().setStringValue(databaseType).build());
    params.put("bucket", Value.newBuilder().setStringValue(bucket).build());
    params.put("database_name", Value.newBuilder().setStringValue(databaseName).build());
    params.put("table_name_patterns", Value.newBuilder().setStringValue(tableNamePatterns).build());
    params.put("agent_service_account", Value.newBuilder().setStringValue(serviceAccount).build());
    params.put("schema_file_path",
```