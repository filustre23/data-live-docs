* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [參考資料](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 從 Amazon Redshift 遷移結構定義和資料

本文說明如何使用公開 IP 位址，將資料從 Amazon Redshift 遷移至 BigQuery。

您可以使用 BigQuery 資料移轉服務，將 Amazon Redshift 資料倉儲中的資料複製到 BigQuery。這項服務會與 GKE 中的遷移代理程式相互通訊，並觸發從 Amazon Redshift 傳輸至 Amazon S3 值區暫存區的卸載作業。接著，BigQuery 資料移轉服務就會將資料從 Amazon S3 值區移轉到 BigQuery。

下圖顯示遷移期間 Amazon Redshift 資料倉儲與 BigQuery 之間的整體資料流動情況。

如要透過虛擬私有雲 (VPC) 使用私有 IP 位址，從 Amazon Redshift 執行個體移轉資料，請參閱「[使用虛擬私有雲 (VPC) 遷移 Amazon Redshift 資料](https://docs.cloud.google.com/bigquery/docs/migration/redshift-vpc?hl=zh-tw)」。

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

建立 Amazon Redshift 移轉作業之前：

1. 請確認建立移轉作業的主體在包含移轉工作的專案中，具有下列權限：

   * 用於建立移轉作業的 `bigquery.transfers.update` 權限
   * 目標資料集的 `bigquery.datasets.get` 和 `bigquery.datasets.update` 權限

   `roles/bigquery.admin` 這個預先定義的 Identity and Access Management (IAM) 角色具備 `bigquery.transfers.update`、`bigquery.datasets.update` 和 `bigquery.datasets.get` 權限。如要進一步瞭解 BigQuery 資料移轉服務中的 IAM 角色，請參閱[存取權控管](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)。
2. 參閱 Amazon S3 的說明文件，以確保您已設定啟用移轉所需的任何權限。Amazon S3 來源資料至少必須套用 AWS 代管政策 [`AmazonS3ReadOnlyAccess`](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_manage.html#attach-managed-policy-console)。

### 建立資料集

[建立 BigQuery 資料集](https://docs.cloud.google.com/bigquery/docs/datasets?hl=zh-tw)來儲存您的資料。您無須建立任何資料表。

### 授予 Amazon Redshift 叢集的存取權

[設定安全群組規則](https://docs.aws.amazon.com/vpc/latest/userguide/working-with-security-group-rules.html)，將私有 Amazon Redshift 叢集的下列 IP 範圍新增至許可清單。您可以將與資料集位置相對應的 IP 位址加入許可清單，也可以將下表中的所有 IP 位址加入許可清單。這些 Google 擁有的 IP 位址會保留給 Amazon Redshift 資料遷移作業使用。

**注意：** BigQuery 與 Amazon Redshift 之間的通訊會透過下列 Google 擁有的 IP 位址進行。不過，從 Amazon S3 移轉至 BigQuery 的資料會透過公用網際網路傳輸。

#### 地區位置

|  | 地區說明 | 區域名稱 | IP 位址 |
| --- | --- | --- | --- |
| **美洲** | | | |
|  | 俄亥俄州哥倫布 | `us-east5` | 34.162.72.184  34.162.173.185  34.162.205.205  34.162.81.45  34.162.182.149  34.162.59.92  34.162.157.190  34.162.191.145 |
|  | 達拉斯 | `us-south1` | 34.174.172.89  34.174.40.67  34.174.5.11  34.174.96.109  34.174.148.99  34.174.176.19  34.174.253.135  34.174.129.163 |
|  | 愛荷華州 | `us-central1` | 34.121.70.114  34.71.81.17  34.122.223.84  34.121.145.212  35.232.1.105  35.202.145.227  35.226.82.216  35.225.241.102 |
|  | 拉斯維加斯 | `us-west4` | 34.125.53.201  34.125.69.174  34.125.159.85  34.125.152.1  34.125.195.166  34.125.50.249  34.125.68.55  34.125.91.116 |
|  | 洛杉磯 | `us-west2` | 35.236.59.167  34.94.132.139  34.94.207.21  34.94.81.187  34.94.88.122  35.235.101.187  34.94.238.66  34.94.195.77 |
|  | 墨西哥 | `northamerica-south1` | 34.51.6.35  34.51.7.113  34.51.12.83  34.51.10.94  34.51.11.219  34.51.11.52  34.51.2.114  34.51.15.251 |
|  | 蒙特婁 | `northamerica-northeast1` | 34.95.20.253  35.203.31.219  34.95.22.233  34.95.27.99  35.203.12.23  35.203.39.46  35.203.116.49  35.203.104.223 |
|  | 北維吉尼亞州 | `us-east4` | 35.245.95.250  35.245.126.228  35.236.225.172  35.245.86.140  35.199.31.35  35.199.19.115  35.230.167.48  35.245.128.132  35.245.111.126  35.236.209.21 |
|  | 奧勒岡州 | `us-west1` | 35.197.117.207  35.199.178.12  35.197.86.233  34.82.155.140  35.247.28.48  35.247.31.246  35.247.106.13  34.105.85.54 |
|  | 鹽湖城 | `us-west3` | 34.106.37.58  34.106.85.113  34.106.28.153  34.106.64.121  34.106.246.131  34.106.56.150  34.106.41.31  34.106.182.92 |
|  | 聖保羅 | `southamerica-east1` | 35.199.88.228  34.95.169.140  35.198.53.30  34.95.144.215  35.247.250.120  35.247.255.158  34.95.231.121  35.198.8.157 |
|  | 聖地亞哥 | `southamerica-west1` | 34.176.188.48  34.176.38.192  34.176.205.134  34.176.102.161  34.176.197.198  34.176.223.236  34.176.47.188  34.176.14.80 |
|  | 南卡羅來納州 | `us-east1` | 35.196.207.183  35.237.231.98  104.196.102.222  35.231.13.201  34.75.129.215  34.75.127.9  35.229.36.137  35.237.91.139 |
|  | 多倫多 | `northamerica-northeast2` | 34.124.116.108  34.124.116.107  34.124.116.102  34.124.116.80  34.124.116.72  34.124.116.85  34.124.116.20  34.124.116.68 |
| **歐洲** | | | |
|  | 比利時 | `europe-west1` | 35.240.36.149  35.205.171.56  34.76.234.4  35.205.38.234  34.77.237.73  35.195.107.238  35.195.52.87  34.76.102.189 |
|  | 柏林 | `europe-west10` | 34.32.28.80  34.32.31.206  34.32.19.49  34.32.33.71  34.32.15.174  34.32.23.7  34.32.1.208  34.32.8.3 |
|  | 芬蘭 | `europe-north1` | 35.228.35.94  35.228.183.156  35.228.211.18  35.228.146.84  35.228.103.114  35.228.53.184  35.228.203.85  35.228.183.138 |
|  | 法蘭克福 | `europe-west3` | 35.246.153.144  35.198.80.78  35.246.181.106  35.246.211.135  34.89.165.108  35.198.68.187  35.242.223.6  34.89.137.180 |
|  | 倫敦 | `europe-west2` | 35.189.119.113  35.189.101.107  35.189.69.131  35.197.205.93  35.189.121.178  35.189.121.41  35.189.85.30  35.197.195.192 |
|  | 馬德里 | `europe-southwest1` | 34.175.99.115  34.175.186.237  34.175.39.130  34.175.135.49  34.175.1.49  34.175.95.94  34.175.102.118  34.175.166.114 |
|  | 米蘭 | `europe-west8` | 34.154.183.149  34.154.40.104  34.154.59.51  34.154.86.2  34.154.182.20  34.154.127.144  34.154.201.251  34.154.0.104 |
|  | 荷蘭 | `europe-west4` | 35.204.237.173  35.204.18.163  34.91.86.224  34.90.184.136  34.91.115.67  34.90.218.6  34.91.147.143  34.91.253.1 |
|  | 巴黎 | `europe-west9` | 34.163.76.229  34.163.153.68  34.155.181.30  34.155.85.234  34.155.230.192  34.155.175.220  34.163.68.177  34.163.157.151 |
|  | 斯德哥爾摩 | `europe-north2` | 34.51.133.48  34.51.136.177  34.51.128.140  34.51.141.252  34.51.139.127  34.51.142.55  34.51.134.218  34.51.138.9 |
|  | 杜林 | `europe-west12` | 34.17.15.186  34.17.44.123  34.17.41.160  34.17.47.82  34.17.43.109  34.17.38.236  34.17.34.223  34.17.16.47 |
|  | 華沙 | `europe-central2` | 34.118.72.8  34.118.45.245  34.118.69.169  34.116.244.189  34.116.170.150  34.118.97.148  34.116.148.164  34.116.168.127 |
|  | 蘇黎世 | `europe-west6` | 34.65.205.160  34.65.121.140  34.65.196.143  34.65.9.133  34.65.156.193  34.65.216.124  34.65.233.83  34.65.168.250 |
| **亞太地區** | | | |
|  | 曼谷 | `asia-southeast3` | 34.15.142.80  34.15.131.78  34.15.141.141  34.15.143.6  34.15.142.166  34.15.138.0  34.15.135.129  34.15.139.45 |
|  | 德里 | `asia-south2` | 34.126.212.96  34.126.212.85  34.126.208.224  34.126.212.94  34.126.208.226  34.126.212.232  34.126.212.93  34.126.212.206 |
|  | 香港 | `asia-east2` | 34.92.245.180  35.241.116.105  35.220.240.216  35.220.188.244  34.92.196.78  34.92.165.209  35.220.193.228  34.96.153.178 |
|  | 雅加達 | `asia-southeast2` | 34.101.79.105  34.101.129.32  34.101.244.197  34.101.100.180  34.101.109.205  34.101.185.189  34.101.179.27  34.101.197.251 |
|  | 墨爾本 | `australia-southeast2` | 34.126.196.95  34.126.196.106  34.126.196.126  34.126.196.96  34.126.196.112  34.126.196.99  34.126.196.76  34.126.196.68 |
|  | 孟買 | `asia-south1` | 34.93.67.112  35.244.0.1  35.200.245.13  35.200.203.161  34.93.209.130  34.93.120.224  35.244.10.12  35.200.186.100 |
|  | 大阪 | `asia-northeast2` | 34.97.94.51  34.97.118.176  34.97.63.76  34.97.159.156  34.97.113.218  34.97.4.108  34.97.119.140  34.97.30.191 |
|  | 首爾 | `asia-northeast3` | 34.64.152.215  34.64.140.241  34.64.133.199  34.64.174.192  34.64.145.219  34.64.136.56  34.64.247.158  34.64.135.220 |
|  | 新加坡 | `asia-southeast1` | 34.87.12.235  34.87.63.5  34.87.91.51  35.198.197.191  35.240.253.175  35.247.165.193  35.247.181.82  35.247.189.103 |
|  | 雪梨 | `australia-southeast1` | 35.189.33.150  35.189.38.5  35.189.29.88  35.189.22.179  35.189.20.163  35.189.29.83  35.189.31.141  35.189.14.219 |
|  | 台灣 | `asia-east1` | 35.221.201.20  35.194.177.253  34.80.17.79  34.80.178.20  34.80.174.198  35.201.132.11  35.201.223.177  35.229.251.28  35.185.155.147  35.194.232.172 |
|  | 東京 | `asia-northeast1` | 34.85.11.246  34.85.30.58  34.85.8.125  34.85.38.59  34.85.31.67  34.85.36.143  34.85.32.222  34.85.18.128  34.85.23.202  34.85.35.192 |
| **中東地區** | | | |
|  | 達曼 | `me-central2` | 34.166.20.177  34.166.10.104  34.166.21.128  34.166.19.184  34.166.20.83  34.166.18.138  34.166.18.48  34.166.23.171 |
|  | 杜哈 | `me-central1` | 34.18.48.121  34.18.25.208  34.18.38.183  34.18.33.25  34.18.21.203  34.18.21.80  34.18.36.126  34.18.23.252 |
|  | 特拉維夫市 | `me-west1` | 34.165.184.115  34.165.110.74  34.165.174.16  34.165.28.235  34.165.170.172  34.165.187.98  34.165.85.64  34.165.245.97 |
| **非洲** | | | |
|  | 約翰尼斯堡 | `africa-south1` | 34.35.11.24  34.35.10.66  34.35.8.32  34.35.3.248  34.35.2.113  34.35.5.61  34.35.7.53  34.35.3.17 |

#### 多地區位置

| 多地區說明 | 多地區名稱 | IP 位址 |
| --- | --- | --- |
| 歐盟1[成員國](https://europa.eu/european-union/about-eu/countries_en)境內的資料中心 | `EU` | 34.76.156.158  34.76.156.172  34.76.136.146  34.76.1.29  34.76.156.232  34.76.156.81  34.76.156.246  34.76.102.206  34.76.129.246  34.76.121.168 |
| 美國資料中心 | `US` | 35.185.196.212  35.197.102.120   35.185.224.10  35.185.228.170  35.197.5.235  35.185.206.139  35.197.67.234  35.197.38.65  35.185.202.229  35.185.200.120 |

1 位於 `EU` 多地區的資料，不會存放在 `europe-west2` (倫敦) 或 `europe-west6` (蘇黎世) 資料中心。

### 授予 Amazon S3 值區的存取權

您必須具備 Amazon S3 值區，做為將 Amazon Redshift 資料移轉至 BigQuery 的暫存區域。如需詳細操作說明，請參閱 [Amazon 說明文件](https://aws.amazon.com/premiumsupport/knowledge-center/create-access-key/)。

1. 建議您建立專用的 Amazon IAM 使用者，並授予該使用者 Amazon Redshift 的唯讀權限，以及 Amazon S3 的讀取與寫入權限。如要完成這個步驟，可以套用下列政策：
2. 建立 Amazon [IAM 使用者存取金鑰組](https://docs.aws.amazon.com/general/latest/gr/aws-sec-cred-types.html)。

### 使用獨立遷移佇列設定工作負載控制

您可以視需要[定義用於遷移目的的 Amazon Redshift 佇列](https://docs.aws.amazon.com/redshift/latest/dg/cm-c-modifying-wlm-configuration.html)，以限制及分離用於遷移作業的資源。您可以使用最大並行查詢次數來設定這個遷移佇列。然後，您可以在某個[遷移使用者群組](https://docs.aws.amazon.com/redshift/latest/dg/r_CREATE_GROUP.html)與佇列之間建立關聯，並在設定遷移作業以移轉資料到 BigQuery 時使用這些憑證。移轉服務只具備遷移佇列的存取權。

### 收集轉移資訊

收集使用 BigQuery 資料移轉服務設定遷移作業所需的資訊：

* 請按照[這些操作說明](https://docs.aws.amazon.com/redshift/latest/mgmt/configure-jdbc-connection.html#obtain-jdbc-url) 取得 JDBC 網址。
* 取得具備適當權限的 Amazon Redshift 資料庫使用者名稱和密碼。
* 按照「[授予 Amazon S3 值區的存取權](#grant_access_to_your_amazon_s3_bucket)」一文中的操作說明，取得 AWS 存取金鑰組。
* 取得要用於移轉作業的 Amazon S3 值區 URI。
  建議您為這個 bucket 設定[生命週期](https://docs.aws.amazon.com/AmazonS3/latest/user-guide/create-lifecycle.html)政策，避免產生不必要的費用。建議的到期時間為 24 小時，以便有足夠的時間將所有資料移轉到 BigQuery。

### 評估資料

在資料移轉過程中，BigQuery 資料移轉服務會將 Amazon Redshift 的資料寫入 Cloud Storage，做為 CSV 檔案。如果這些檔案含有 ASCII 0 字元，就無法載入至 BigQuery。建議您評估資料，判斷這是否會造成問題。如果是，您可以將資料匯出至 Amazon S3 做為 Parquet 檔案，然後使用 BigQuery 資料移轉服務匯入這些檔案，藉此解決問題。詳情請參閱「[Amazon S3 移轉作業總覽](https://docs.cloud.google.com/bigquery/docs/s3-transfer-intro?hl=zh-tw)」。

## 設定 Amazon Redshift 轉移作業

選取下列選項之一：

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往 BigQuery](https://console.cloud.google.com/bigquery?hl=zh-tw)
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
   5. 在 **Amazon S3 URI** 部分，輸入將做為暫存區使用的 [S3 值區的 URI](#s3_uri)。
   6. 在「Amazon Redshift Schema」(Amazon Redshift 結構定義) 部分，輸入您正在遷移的 Amazon Redshift 結構定義。
   7. 在「Table name patterns」(資料表名稱格式) 部分，指定符合結構定義中資料表名稱的名稱或格式。您可以使用規則運算式，在下列表單中指定格式：`<table1Regex>;<table2Regex>`。此格式必須遵循 Java 規則運算式語法。例如：

      * `lineitem;ordertb` 會比對名為 `lineitem` 和 `ordertb` 的資料表。
      * `.*` 會比對所有資料表。

      將這個欄位留白，用以遷移所有來自指定結構定義的資料表。

      **注意：** 針對非常大型的資料表，我們建議一次移轉一個資料表。[每個載入工作的 BigQuery 載入配額為 15 TB](#quotas_and_limits)。
   8. 將「VPC and the reserved IP range」(虛擬私有雲和保留的 IP 範圍) 欄位留空。
8. 在「Service Account」(服務帳戶) 選單，選取與貴機構Google Cloud 專案相關聯的[服務帳戶](https://docs.cloud.google.com/iam/docs/service-account-overview?hl=zh-tw)。您可以將服務帳戶與移轉作業建立關聯，這樣就不需要使用者憑證。如要進一步瞭解如何搭配使用服務帳戶與資料移轉作業，請參閱[使用服務帳戶](https://docs.cloud.google.com/bigquery/docs/use-service-accounts?hl=zh-tw)的相關說明。

   * 如果使用[聯合身分](https://docs.cloud.google.com/iam/docs/workforce-identity-federation?hl=zh-tw)登入，您必須擁有服務帳戶才能建立移轉作業。如果是以 [Google 帳戶](https://docs.cloud.google.com/iam/docs/principals-overview?hl=zh-tw#google-account)登入，則不一定要透過服務帳戶建立移轉作業。
   * 服務帳戶必須具備[必要權限](#set_required_permissions)。
9. 選用：在「Notification options」(通知選項) 專區，執行下列操作：

   1. 按一下啟用電子郵件通知的切換開關。啟用這個選項之後，若移轉失敗，移轉作業管理員就會收到電子郵件通知。
   2. 在「Select a Pub/Sub topic」(選取 Pub/Sub 主題) 選取[主題](https://docs.cloud.google.com/pubsub/docs/overview?hl=zh-tw#types)名稱，或是點選「Create a topic」(建立主題)。這個選項會針對移轉作業設定 Pub/Sub 執行[通知](https://docs.cloud.google.com/bigquery/docs/transfer-run-notifications?hl=zh-tw)。
10. 按一下 [儲存]。
11. Google Cloud 控制台會顯示移轉設定的所有詳細資料，包括此移轉作業的「Resource name」(資源名稱)。

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

其中：

* project\_id 是您的 Google Cloud 專案 ID。如果未指定 `--project_id`，系統會使用預設專案。
* data\_source 是資料來源：`redshift`。
* dataset 是移轉作業設定的 BigQuery 目標資料集。
* name 是移轉設定的顯示名稱。移轉作業名稱可以是任意值，日後需要修改移轉作業時，能夠據此識別即可。
* service\_account：用於驗證轉移作業的服務帳戶名稱。服務帳戶應由用於建立轉移作業的 `project_id` 擁有，且應具備所有[必要權限](#set_required_permissions)。
* parameters 含有已建立移轉設定的 JSON 格式參數，例如：`--params='{"param":"param_value"}'`。

Amazon Redshift 移轉設定所需的參數如下：

* `jdbc_url`：JDBC 連線網址可用來找出 Amazon Redshift 叢集的位置。
* `database_username`：用來存取資料庫以卸載指定資料表的使用者名稱。
* `database_password`：與使用者名稱搭配使用的密碼，可存取資料庫以卸載指定資料表。
* `access_key_id`：簽署向 AWS 發出要求的存取金鑰 ID。
* `secret_access_key`：與存取金鑰 ID 搭配使用的存取密鑰，密鑰可簽署向 AWS 發出的要求。
* `s3_bucket`：以「s3://」開頭的 Amazon S3 URI，並且可指定用於暫存檔案的前置字串。
* `redshift_schema`：包含所有要遷移之資料表的 Amazon Redshift 結構定義。
* `table_name_patterns`：以分號 (;) 分隔的資料表名稱格式。資料表格式是要遷移之資料表的規則運算式。如未提供，則系統會遷移資料庫結構定義下的所有資料表。

舉例來說，下列指令會建立名為 `My Transfer` 的 Amazon Redshift 移轉作業，其中目標資料集的名稱為 `mydataset`，專案的 ID 為 `google.com:myproject`。

```
bq mk \
    --transfer_config \
    --project_id=myproject \
    --data_source=redshift \
    --target_dataset=mydataset \
    --display_name='My Transfer' \
    --params='{"jdbc_url":"jdbc:postgresql://test-example-instance.sample.us-west-1.redshift.amazonaws.com:5439/dbname","database_username":"my_username","database_password":"1234567890","access_key_id":"A1B2C3D4E5F6G7H8I9J0","secret_access_key":"1234567890123456789012345678901234567890","s3_bucket":"s3://bucket/prefix","redshift_schema":"public","table_name_patterns":"table_name"}'
```

**注意：** 您無法使用指令列工具設定通知。

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

// Sample to create redshift transfer config
public class CreateRedshiftTransfer {

  public static void main(String[] args) throws IOException {
    // TODO(developer): Replace these variables before running the sample.
    final String projectId = "MY_PROJECT_ID";
    String datasetId = "MY_DATASET_ID";
    String datasetRegion = "US";
    String jdbcUrl = "MY_JDBC_URL_CONNECTION_REDSHIFT";
    String dbUserName = "MY_USERNAME";
    String dbPassword = "MY_PASSWORD";
    String accessKeyId = "MY_AWS_ACCESS_KEY_ID";
    String secretAccessId = "MY_AWS_SECRET_ACCESS_ID";
    String s3Bucket = "MY_S3_BUCKET_URI";
    String redShiftSchema = "MY_REDSHIFT_SCHEMA";
    String tableNamePatterns = "*";
    String vpcAndReserveIpRange = "MY_VPC_AND_IP_RANGE";
    Map<String, Value> params = new HashMap<>();
    params.put("jdbc_url", Value.newBuilder().setStringValue(jdbcUrl).build());
    params.put("database_username", Value.newBuilder().setStringValue(dbUserName).build());
    params.put("database_password", Value.newBuilder().setStringValue(dbPassword).build());
    params.put("access_key_id",
```