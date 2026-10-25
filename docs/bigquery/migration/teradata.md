Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

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
- Enable the BigQuery, BigQuery Data Transfer Service, Cloud Storage, and Pub/Sub APIs, if any are not already enabled.

  **Roles required to enable APIs**

  To enable APIs, you need the `serviceusage.services.enable` permission. If you
  created the project, then you likely already have this permission through the
  Owner role (`roles/owner`). Otherwise, you can get this permission through the
  Service Usage Admin role (`roles/serviceusage.serviceUsageAdmin`).
  [Learn how to grant roles](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw).

  [Enable the APIs](https://console.cloud.google.com/apis/enableflow?apiid=bigquery.googleapis.com%2Cbigquerydatatransfer.googleapis.com%2Cstorage-component.googleapis.com%2Cpubsub.googleapis.com&hl=zh-tw)
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
- Enable the BigQuery, BigQuery Data Transfer Service, Cloud Storage, and Pub/Sub APIs, if any are not already enabled.

  **Roles required to enable APIs**

  To enable APIs, you need the `serviceusage.services.enable` permission. If you
  created the project, then you likely already have this permission through the
  Owner role (`roles/owner`). Otherwise, you can get this permission through the
  Service Usage Admin role (`roles/serviceusage.serviceUsageAdmin`).
  [Learn how to grant roles](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw).

  [Enable the APIs](https://console.cloud.google.com/apis/enableflow?apiid=bigquery.googleapis.com%2Cbigquerydatatransfer.googleapis.com%2Cstorage-component.googleapis.com%2Cpubsub.googleapis.com&hl=zh-tw)
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
* Storage 管理員 (`roles/storage.admin`)，或授予下列權限的[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)：
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

### 建立 Cloud Storage bucket

[建立 Cloud Storage bucket](https://docs.cloud.google.com/storage/docs/creating-buckets?hl=zh-tw)，在移轉工作期間暫存資料。

### 準備本機環境

完成本節中的工作，為轉移作業準備本機環境。

#### 本機需求條件

* 遷移代理程式會使用 JDBC 連線和 Google Cloud API 連接 Teradata 執行個體。確認網路存取權未遭防火牆封鎖。
* 如要使用 1.18.0 以上版本的遷移代理，請安裝 Java Runtime Environment (JRE) 21 以上版本。較舊版本的遷移代理程式需要 JRE 8 以上版本。
* 請確認您選擇的擷取方法有足夠的儲存空間，詳情請參閱「[擷取方法](https://docs.cloud.google.com/bigquery/docs/migration/teradata-overview?hl=zh-tw#extraction_method)」。
* 如果您決定使用 Teradata Parallel Transporter (TPT) 擷取功能，請確認已安裝 [`tbuild`](https://docs.teradata.com/r/Teradata-Parallel-Transporter-Reference/July-2017/Teradata-PT-Utility-Commands/Command-Syntax/tbuild) 公用程式。如要進一步瞭解如何選擇擷取方法，請參閱「[擷取方法](https://docs.cloud.google.com/bigquery/docs/migration/teradata-overview?hl=zh-tw#extraction_method)」。

#### Teradata 連線詳細資料

* 請確認您擁有 Teradata 使用者的使用者名稱和密碼，且該使用者有權讀取系統資料表和要遷移的資料表。

  系統會透過提示擷取使用者名稱和密碼，並只儲存在 RAM 中。您也可以選擇在後續步驟中，為使用者名稱或密碼建立憑證檔案。使用憑證檔案時，請採取適當步驟來控管對本機檔案系統中儲存憑證檔案的資料夾的存取權，因為憑證檔案未經過加密。
* 請務必知道要連線至 Teradata 執行個體的主機名稱和通訊埠編號。

  系統不支援 LDAP 等驗證模式。

#### 下載 JDBC 驅動程式

從 Teradata [下載](https://downloads.teradata.com/download/connectivity/jdbc-driver) `terajdbc4.jar` JDBC 驅動程式檔案，並儲存到可連線至資料倉儲的電腦。

#### 設定 `GOOGLE_APPLICATION_CREDENTIALS` 變數

[將環境變數 `GOOGLE_APPLICATION_CREDENTIALS`](https://docs.cloud.google.com/docs/authentication/set-up-adc-local-dev-environment?hl=zh-tw#local-key) 設定為您在「[事前準備](#before_you_begin)」一節中下載的服務帳戶金鑰。

### 更新 VPC Service Controls 輸出規則

將與您所在區域對應的 BigQuery 資料移轉服務代管 Google Cloud 專案，新增至 VPC Service Controls 範圍的[輸出規則](https://docs.cloud.google.com/vpc-service-controls/docs/ingress-egress-rules?hl=zh-tw#egress_rules_reference)。

下表列出用於資料移轉的區域位置專案編號。新增與資料集位置對應的專案編號。

#### 多地區位置

| 多地區說明 | 多地區名稱 | 專案編號 |
| --- | --- | --- |
| 歐盟成員國境內的資料中心 | `eu` | 17253722542  272853474138  420718595790  929473878322  990232121269 |
| 美國資料中心 | `us` | 1005756709729  140222280645  247872939591  312976397333  521896999118  525821192359  892499355189  949134172629  990232121269 |

#### 地區位置

| 區域說明 | 區域名稱 | 專案編號 |
| --- | --- | --- |
| **美洲** | | |
| 蒙特婁 | `northamerica-northeast1` | 603911341430  644379120249  665941355665  743643531530  990232121269 |
| 多倫多 | `northamerica-northeast2` | 181203883014  569023246094  814935732186  833015518790  990232121269 |
| 墨西哥 | `northamerica-south1` | 439376105624  737643102222  746316165749  863053761002  990232121269 |
| 聖保羅 | `southamerica-east1` | 133435938206  376122552368  485381725001  796391836836  990232121269 |
| 聖地亞哥 | `southamerica-west1` | 1087357303029  348543783783  659924941015  862900136725  990232121269 |
| 愛荷華州 | `us-central1` | 298453567688  788415223852  850878823175  986263347210  990232121269 |
| 南卡羅來納州 | `us-east1` | 1055108947046  1084124504460  335013112247  724101498857  990232121269 |
| 北維吉尼亞州 | `us-east4` | 1029854080039  517474920593  970314007431  98298633330  990232121269 |
| 俄亥俄州哥倫布 | `us-east5` | 1018267783826  386306739011  420397636038  778968775575  990232121269 |
| 達拉斯 | `us-south1` | 1000457898916  1047122215716  241710172671  955278753983  990232121269 |
| 奧勒岡州 | `us-west1` | 232019391832  341405773774  376906440760  477215631937  990232121269 |
| 洛杉磯 | `us-west2` | 1082081077124  593499865061  796558996990  812061960238  990232121269 |
| 鹽湖城 | `us-west3` | 34769458069  488393466740  870087576864  878441810105  990232121269 |
| 拉斯維加斯 | `us-west4` | 219770299440  421529192039  516260452158  653925368482  990232121269 |
| **歐洲** | | |
| 華沙 | `europe-central2` | 408105394529  556626738827  613447812609  875068591969  990232121269 |
| 芬蘭 | `europe-north1` | 1049140453480  148002628360  610856287987  657186468367  990232121269 |
| 斯德哥爾摩 | `europe-north2` | 264708615094  275871864623  353052212156  915614473443  990232121269 |
| 馬德里 | `europe-southwest1` | 1035291313153  1048466610864  16585749286  684773867031  990232121269 |
| 比利時 | `europe-west1` | 311010690362  337985836396  348525528820  874692481832  990232121269 |
| 柏林 | `europe-west10` | 1014021387408  1021109191575  1076988971454  965306537493  990232121269 |
| 杜林 | `europe-west12` | 624998300135  664251133452  672417986210  702529954322  990232121269 |
| 倫敦 | `europe-west2` | 1013046052024  424062913611  625972158490  707263280432  990232121269 |
| 法蘭克福 | `europe-west3` | 1087781646048  143240061766  312688138599  715827071311  990232121269 |
| 荷蘭 | `europe-west4` | 110044889848  398757511504  557234723212  769143166592  990232121269 |
| 蘇黎世 | `europe-west6` | 163551586425  378713015688  416925392034  669890417706  990232121269 |
| 米蘭 | `europe-west8` | 103481800693  1082157965924  23655501621  555661886352  990232121269 |
| 巴黎 | `europe-west9` | 1085882338778  176207547936  221990904254  670920836007  990232121269 |
| **亞太地區** | | |
| 台灣 | `asia-east1` | 21873972082  271898158674  389278959284  922460772707  990232121269 |
| 香港 | `asia-east2` | 263483805684  773980783174  865347783058  90665746791  990232121269 |
| 東京 | `asia-northeast1` | 415417931028  53965067050  953665196151  983967577764  990232121269 |
| 大阪 | `asia-northeast2` | 205726704771  478186599828  57312416489  861476638029  990232121269 |
| 首爾 | `asia-northeast3` | 320159292295  548035635347  791473645597  935702892639  990232121269 |
| 孟買 | `asia-south1` | 13592990997  229940966341  68960523189  901420668689  990232121269 |
| 德里 | `asia-south2` | 496191507005  54806403576  741779061357  809478923584  990232121269 |
| 新加坡 | `asia-southeast1` | 541653567103  60558171982  753901882843  944188302893  990232121269 |
| 雅加達 | `asia-southeast2` | 1074047252998  17464964742  271871433529  427023413305  990232121269 |
| 曼谷 | `asia-southeast3` | 1020436856624  355273974477  603543103680  777922772431  990232121269 |
| 雪梨 | `australia-southeast1` | 163046745040  591848239128  623326425100  814418810594  990232121269 |
| 墨爾本 | `australia-southeast2` | 1062391852597  441829466914  714897033691  748594785463  990232121269 |
| **中東地區** | | |
| 杜哈 | `me-central1` | 260539430499  380691191456  707684919235  799708208022  990232121269 |
| 達曼 | `me-central2` | 1067269861014  364585730608  702115426609  932431265647  990232121269 |
| 特拉維夫 | `me-west1` | 356023739839  748664533815  869899828196  940471234508  990232121269 |
| **非洲** | | |
| 約翰尼斯堡 | `africa-south1` | 3664 |