Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [參考資料](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 使用虛擬私有雲網路遷移 Amazon Redshift 資料

本文說明如何使用 VPC，將資料從 Amazon Redshift 遷移至 BigQuery。

如果您在 AWS 中有私有 Amazon Redshift 執行個體，可以建立[虛擬私有雲網路 (VPC 網路)](https://docs.cloud.google.com/vpc/docs/overview?hl=zh-tw)，並將其連線至 Amazon Redshift VPC 網路，藉此將資料遷移至 BigQuery。資料遷移流程如下：

1. 在要用於轉移的專案中建立虛擬私有雲網路。虛擬私有雲網路不得為[Shared VPC](https://docs.cloud.google.com/vpc/docs/shared-vpc?hl=zh-tw)網路。
2. 設定[虛擬私人網路 (VPN)](https://docs.cloud.google.com/network-connectivity/docs/vpn/concepts/overview?hl=zh-tw)，並連結專案虛擬私有雲網路和 Amazon Redshift 虛擬私有雲網路。
3. 設定轉移作業時，請指定專案虛擬私有雲網路和保留的 IP 範圍。
4. BigQuery 資料移轉服務會建立租戶專案，並附加至您用於移轉的專案。
5. BigQuery 資料移轉服務會使用您指定的保留 IP 範圍，在租戶專案中建立具有一個子網路的虛擬私有雲網路。
6. BigQuery 資料移轉服務會在您的專案虛擬私有雲網路與租戶專案虛擬私有雲網路之間，建立[虛擬私有雲對等互連](https://docs.cloud.google.com/vpc/docs/vpc-peering?hl=zh-tw)。
7. BigQuery 資料移轉服務遷移作業會在租戶專案中執行。
   並觸發從 Amazon Redshift 到 Amazon S3 值區中暫存區的上傳作業。卸載速度取決於叢集設定。
8. BigQuery 資料移轉服務會將資料從 Amazon S3 值區移轉至 BigQuery。

**注意：** BigQuery 與 Amazon Redshift 之間的通訊，是透過對等互連虛擬私有雲網路之間的 VPN 進行。不過，從 Amazon S3 到 BigQuery 的資料移動作業是透過公用網際網路進行。

如要透過公開 IP 從 Amazon Redshift 執行個體移轉資料，請按照[這些操作說明](https://docs.cloud.google.com/bigquery/docs/migration/redshift?hl=zh-tw)將 Amazon Redshift 資料遷移至 BigQuery。

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
- Enable the BigQuery and BigQuery Data Transfer Service APIs.

  **Roles required to enable APIs**

  To enable APIs, you need the Service Usage Admin IAM
  role (`roles/serviceusage.serviceUsageAdmin`), which
  contains the `serviceusage.services.enable` permission. [Learn how to grant
  roles](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw).

  [Enable the APIs](https://console.cloud.google.com/flows/enableapi?apiid=bigquery.googleapis.com%2Cbigquerydatatransfer.googleapis.com&hl=zh-tw)

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
- Enable the BigQuery and BigQuery Data Transfer Service APIs.

  **Roles required to enable APIs**

  To enable APIs, you need the Service Usage Admin IAM
  role (`roles/serviceusage.serviceUsageAdmin`), which
  contains the `serviceusage.services.enable` permission. [Learn how to grant
  roles](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw).

  [Enable the APIs](https://console.cloud.google.com/flows/enableapi?apiid=bigquery.googleapis.com%2Cbigquerydatatransfer.googleapis.com&hl=zh-tw)

### 設定必要權限

建立 Amazon Redshift 移轉作業前，請按照下列步驟操作：

1. 確認建立移轉作業的人員在 BigQuery 中具有以下必要的身分與存取權管理 (IAM) 權限：

   * `bigquery.transfers.update` 權限，以建立移轉作業
   * 目標資料集的 `bigquery.datasets.update` 權限

   `role/bigquery.admin` 這個預先定義的 IAM 角色具備 `bigquery.transfers.update` 和 `bigquery.datasets.update` 權限。如要進一步瞭解 BigQuery 資料移轉服務中的 IAM 角色，請參閱[存取控管](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)。
2. 參閱 Amazon S3 的說明文件，以確保您已設定啟用移轉所需的任何權限。Amazon S3 來源資料至少必須套用 AWS 代管政策 [`AmazonS3ReadOnlyAccess`](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_manage.html#attach-managed-policy-console)。
3. 授予適當的[身分與存取權管理權限](https://docs.cloud.google.com/iam/docs/roles-permissions?hl=zh-tw)，讓設定轉移作業的使用者可以建立及刪除虛擬私有雲網路對等互連。這項服務會使用個人的 Google Cloud 使用者憑證建立虛擬私有雲對等互連連線。

   * 建立 VPC 對等互連的權限：`compute.networks.addPeering`
   * 刪除虛擬私有雲對等互連的權限：`compute.networks.removePeering`

   根據預設，`roles/project.owner`、`roles/project.editor` 和 `roles/compute.networkAdmin` 預先定義的 IAM 角色都具備 `compute.networks.addPeering` 和 `compute.networks.removePeering` 權限。

### 建立資料集

[建立 BigQuery 資料集](https://docs.cloud.google.com/bigquery/docs/datasets?hl=zh-tw)來儲存您的資料。您無須建立任何資料表。

### 授予 Amazon Redshift 叢集的存取權

[設定安全性群組規則](https://docs.aws.amazon.com/vpc/latest/userguide/working-with-security-group-rules.html)，將私有 Amazon Redshift 叢集的下列 IP 範圍新增至許可清單。在後續步驟中，您設定轉移作業時，會在這個虛擬私有雲網路中定義私人 IP 範圍。

### 授予 Amazon S3 值區的存取權

您必須具備 Amazon S3 值區，做為將 Amazon Redshift 資料移轉至 BigQuery 的暫存區域。如需詳細操作說明，請參閱 [Amazon 說明文件](https://aws.amazon.com/premiumsupport/knowledge-center/create-access-key/)。

1. 建議您建立專用的 Amazon IAM 使用者，並授予該使用者 Amazon Redshift 的唯讀權限，以及 Amazon S3 的讀取與寫入權限。如要完成這個步驟，可以套用下列政策：
2. 建立 Amazon [IAM 使用者存取金鑰組](https://docs.aws.amazon.com/general/latest/gr/aws-sec-cred-types.html)。

### 使用獨立遷移佇列設定工作負載控制

您可以視需要[定義用於遷移目的的 Amazon Redshift 佇列](https://docs.aws.amazon.com/redshift/latest/dg/cm-c-modifying-wlm-configuration.html)，以限制及分離用於遷移作業的資源。您可以使用最大並行查詢次數來設定這個遷移佇列。然後，您可以在某個[遷移使用者群組](https://docs.aws.amazon.com/redshift/latest/dg/r_CREATE_GROUP.html)與佇列之間建立關聯，並在設定遷移作業以移轉資料到 BigQuery 時使用這些憑證。移轉服務只具備遷移佇列的存取權。

### 收集轉移資訊

收集使用 BigQuery 資料移轉服務設定遷移作業所需的資訊：

* 在 Amazon Redshift 中取得虛擬私有雲和保留的 IP 範圍。

* 請按照[這些操作說明](https://docs.aws.amazon.com/redshift/latest/mgmt/configure-jdbc-connection.html#obtain-jdbc-url) 取得 JDBC 網址。
* 取得具備適當權限的 Amazon Redshift 資料庫使用者名稱和密碼。
* 按照「[授予 Amazon S3 值區的存取權](#grant_access_to_your_amazon_s3_bucket)」一文中的操作說明，取得 AWS 存取金鑰組。
* 取得要用於移轉作業的 Amazon S3 值區 URI。
  建議您為這個 bucket 設定[生命週期](https://docs.aws.amazon.com/AmazonS3/latest/user-guide/create-lifecycle.html)政策，避免產生不必要的費用。建議的到期時間為 24 小時，以便有足夠的時間將所有資料移轉到 BigQuery。

### 評估資料

在資料移轉過程中，BigQuery 資料移轉服務會將 Amazon Redshift 的資料以 CSV 檔案的形式寫入 Cloud Storage。如果這些檔案含有 ASCII 0 字元，就無法載入至 BigQuery。建議您評估資料，判斷這是否會造成問題。如果是，您可以將資料匯出至 Amazon S3 做為 Parquet 檔案，然後使用 BigQuery 資料移轉服務匯入這些檔案，藉此解決問題。詳情請參閱「[Amazon S3 移轉作業總覽](https://docs.cloud.google.com/bigquery/docs/s3-transfer-intro?hl=zh-tw)」。

### 設定虛擬私有雲網路和 VPN

1. 請確認您具備啟用 VPC 對等互連的權限。詳情請參閱「[設定必要權限](#set_required_permissions)」。
2. 請按照[本指南中的操作說明](https://docs.cloud.google.com/network-connectivity/docs/vpn/tutorials/create-ha-vpn-connections-google-cloud-aws?hl=zh-tw)，設定 Google Cloud 虛擬私有雲網路、在Google Cloud 專案的虛擬私有雲網路與 Amazon Redshift 虛擬私有雲網路之間設定 VPN，並啟用虛擬私有雲對等互連。

   **注意：** 這項服務會使用 VPC 網路名稱做為 VPC 對等互連連線名稱，因此請確保沒有任何現有的 VPC 對等互連連線已使用該名稱。
3. 設定 Amazon Redshift，允許連線至 VPN。詳情請參閱 [Amazon Redshift 叢集安全群組](https://docs.aws.amazon.com/redshift/latest/mgmt/working-with-security-groups.html)。
4. 前往 Google Cloud 控制台的「VPC networks」(虛擬私有雲網路)  頁面，確認Google Cloud 專案中的虛擬私有雲網路已透過 VPN 連線至 Amazon Redshift。 Google Cloud

   [前往「VPC networks」(虛擬私有雲網路)](https://console.cloud.google.com/networking/networks/list?hl=zh-tw)

   主控台頁面會列出所有虛擬私有雲網路。

### 將預留 IP 做為自訂路徑通告

在轉移設定中提供預留 IP 位址範圍時，您必須先[將 IP 範圍新增為現有 Cloud Router 或 BGP 工作階段通告的自訂路徑](https://docs.cloud.google.com/network-connectivity/docs/router/how-to/advertising-custom-ip?hl=zh-tw)。

## 設定 Amazon Redshift 移轉作業

請按照下列操作說明設定 Amazon Redshift 移轉作業：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 按一下「資料移轉」。
3. 按一下「建立轉移作業」。
4. 在「Source type」(來源類型) 區段中，從「Source」(來源) 清單選取「Migration: Amazon Redshift」(遷移：Amazon Redshift)。
5. 在「Transfer config name」(轉移設定名稱) 區段中，於「Display name」(顯示名稱) 欄位輸入移轉作業的名稱，例如 `My migration`。顯示名稱可以是任何容易辨識的值，方便您日後在必要時進行修改。
6. 在「Destination settings」(目的地設定) 部分，從「Dataset」(資料集) 清單中選擇[您建立的資料集](#create_a_dataset)。
7. 在「Data source details」(資料來源詳細資料) 部分執行下列操作：

   1. 在「JDBC connection url for Amazon Redshift」(Amazon Redshift 的 JDBC 連線網址) 部分，提供 [JDBC 網址](#jdbc_url)以存取 Amazon Redshift 叢集。
   2. 在「Username of your database」(資料庫的使用者名稱) 部分，輸入您要遷移的 Amazon Redshift 資料庫使用者名稱。
   3. 在「Password of your database」(資料庫密碼) 部分，輸入資料庫密碼。

      **注意：** 提供 Amazon 憑證，即表示您瞭解 BigQuery 資料移轉服務是您的代理程式，僅用於存取移轉資料。
   4. 在「Access key ID」(存取金鑰 ID) 和「Secret access key」(存取密鑰) 部分，輸入您在[授予 S3 值區的存取權](#grant_access_to_your_S3_bucket)步驟所取得的存取金鑰組。
   5. 在「Amazon S3 URI」部分，輸入將做為暫存區使用的 [S3 值區的 URI](#s3_uri)。
   6. 在「Amazon Redshift Schema」(Amazon Redshift 結構定義) 部分，輸入您正在遷移的 Amazon Redshift 結構定義。
   7. 在「Table name patterns」(資料表名稱格式) 部分，指定符合結構定義中資料表名稱的名稱或格式。您可以使用規則運算式，在下列表單中指定格式：`<table1Regex>;<table2Regex>`。此格式必須遵循 Java 規則運算式語法。例如：

      * `lineitem;ordertb` 會比對名為 `lineitem` 和 `ordertb` 的資料表。
      * `.*` 會比對所有資料表。

      將這個欄位留白，用以遷移所有來自指定結構定義的資料表。

      **注意：** 針對非常大型的資料表，我們建議一次移轉一個資料表。[每個載入工作的 BigQuery 載入配額為 15 TB](#quotas_and_limits)。
   8. 如要設定 **VPC 和保留的 IP 範圍**，請指定虛擬私有雲網路名稱，以及要在租戶專案虛擬私有雲網路中使用的私人 IP 位址範圍。以 CIDR 區塊表示法指定 IP 位址範圍。

      * IP 位址必須先通告為自訂路徑。詳情請參閱「[通告保留的 IP 做為自訂路由](#advertise-routes)」。
      * 格式為 `VPC_network_name:CIDR`，例如：`my_vpc:10.251.1.0/24`。
      * 請使用 CIDR 標記法中的標準非公開虛擬私有雲網路位址範圍，開頭為 `10.x.x.x`。
      * IP 範圍必須包含超過 10 個 IP 位址。
      * 這個 IP 範圍不得與專案虛擬私有雲網路或 Amazon Redshift 虛擬私有雲網路中的任何子網路重疊。
      * 如果為同一個 Amazon Redshift 執行個體設定多項轉移作業，請務必在每項作業中使用相同的 `VPC_network_name:CIDR` 值，這樣多項轉移作業就能重複使用相同的遷移基礎架構。**注意：** 設定完成後，這個 CIDR 區塊的值就無法變更。
8. 選用：在「Notification options」(通知選項) 專區，執行下列操作：

   1. 按一下啟用電子郵件通知的切換開關。啟用這個選項之後，若移轉失敗，移轉作業管理員就會收到電子郵件通知。
   2. 在「Select a Pub/Sub topic」(選取 Pub/Sub 主題) 選取[主題](https://docs.cloud.google.com/pubsub/docs/overview?hl=zh-tw#types)名稱，或是點選「Create a topic」(建立主題)。這個選項會針對移轉作業設定 Pub/Sub 執行[通知](https://docs.cloud.google.com/bigquery/docs/transfer-run-notifications?hl=zh-tw)。
9. 按一下 [儲存]。
10. Google Cloud 控制台會顯示移轉設定的所有詳細資料，包括此移轉作業的「Resource name」(資源名稱)。

## 配額與限制

使用虛擬私有雲網路遷移 Amazon Redshift 私人執行個體時，遷移代理程式會在單一租戶基礎架構上執行。由於運算資源有限，最多只能同時執行 5 個轉移作業。

每個資料表之每個載入工作的 BigQuery 載入配額皆為 15 TB。Amazon Redshift 會在內部壓縮資料表資料，因此匯出的資料表大小將大於 Amazon Redshift 回報的資料表大小。如果您計畫遷移大於 15 TB 的資料表，請先與 [Cloud Customer Care](https://docs.cloud.google.com/bigquery/docs/getting-support?hl=zh-tw) 聯絡。

使用這項服務可能必須支付其他產品 (非 Google) 的使用費用。詳情請參閱 [Amazon Redshift](https://aws.amazon.com/redshift/pricing/) 和 [Amazon S3](https://aws.amazon.com/s3/pricing/) 定價頁面。

由於 [Amazon S3 的一致性模型](https://docs.cloud.google.com/bigquery/docs/s3-transfer-intro?hl=zh-tw#consistency_considerations)，您可以在移轉到 BigQuery 時不納入部分檔案。

## 後續步驟

* 瞭解標準 [Amazon Redshift 遷移作業](https://docs.cloud.google.com/bigquery/docs/migration/redshift?hl=zh-tw)。
* 進一步瞭解 [BigQuery 資料移轉服務](https://docs.cloud.google.com/bigquery/docs/dts-introduction?hl=zh-tw)。
* 使用[批次 SQL 轉譯](https://docs.cloud.google.com/bigquery/docs/batch-sql-translator?hl=zh-tw)功能遷移 SQL 程式碼。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-08 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-08 (世界標準時間)。"],[],[]]