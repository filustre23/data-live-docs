Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

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

您可以使用 BigQuery 資料移轉服務，將資料從 Amazon Redshift 資料倉儲複製到 BigQuery。這項服務會與 GKE 中的遷移代理程式互動，並觸發卸載作業，將資料從 Amazon Redshift 移至 Amazon S3 bucket 中的暫存區。接著，BigQuery 資料移轉服務會將資料從 Amazon S3 bucket 移轉至 BigQuery。

下圖顯示遷移期間 Amazon Redshift 資料倉儲與 BigQuery 之間的整體資料流動情況。

如要使用私人 IP 位址，透過虛擬私有雲 (VPC) 從 Amazon Redshift 執行個體移轉資料，請參閱「[使用虛擬私有雲移轉 Amazon Redshift 資料](https://docs.cloud.google.com/bigquery/docs/migration/redshift-vpc?hl=zh-tw)」。

## 事前準備

- 登入 Google Cloud 帳戶。如果您未曾使用過 Google Cloud，歡迎[建立帳戶](https://console.cloud.google.com/freetrial?hl=zh-tw)，親自體驗實際使用我們產品的成效。新客戶還能獲得價值 $300 美元的免費抵免額，用於執行、測試及部署工作負載。
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
- Enable the BigQuery and BigQuery Data Transfer Service APIs, if any are not already enabled.

  **Roles required to enable APIs**

  To enable APIs, you need the `serviceusage.services.enable` permission. If you
  created the project, then you likely already have this permission through the
  Owner role (`roles/owner`). Otherwise, you can get this permission through the
  Service Usage Admin role (`roles/serviceusage.serviceUsageAdmin`).
  [Learn how to grant roles](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw).

  [Enable the APIs](https://console.cloud.google.com/apis/enableflow?apiid=bigquery.googleapis.com%2Cbigquerydatatransfer.googleapis.com&hl=zh-tw)

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
- Enable the BigQuery and BigQuery Data Transfer Service APIs, if any are not already enabled.

  **Roles required to enable APIs**

  To enable APIs, you need the `serviceusage.services.enable` permission. If you
  created the project, then you likely already have this permission through the
  Owner role (`roles/owner`). Otherwise, you can get this permission through the
  Service Usage Admin role (`roles/serviceusage.serviceUsageAdmin`).
  [Learn how to grant roles](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw).

  [Enable the APIs](https://console.cloud.google.com/apis/enableflow?apiid=bigquery.googleapis.com%2Cbigquerydatatransfer.googleapis.com&hl=zh-tw)

### 設定必要權限

建立 Amazon Redshift 移轉作業前，請先完成下列事項：

1. 請確認建立移轉作業的主體，在包含移轉工作的專案中具備下列權限：

   * 用於建立移轉作業的 `bigquery.transfers.update` 權限
   * 目標資料集的 `bigquery.datasets.get` 和 `bigquery.datasets.update` 權限

   `roles/bigquery.admin` 預先定義的 Identity and Access Management (IAM) 角色包含 `bigquery.transfers.update`、`bigquery.datasets.update` 和 `bigquery.datasets.get` 權限。如要進一步瞭解 BigQuery 資料移轉服務中的 IAM 角色，請參閱「[存取控管](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)」。
2. 參閱 Amazon S3 的說明文件，以確保您已設定啟用移轉所需的任何權限。Amazon S3 來源資料至少必須套用 AWS 代管政策 [`AmazonS3ReadOnlyAccess`](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_manage.html#attach-managed-policy-console)。

### 建立資料集

[建立 BigQuery 資料集](https://docs.cloud.google.com/bigquery/docs/datasets?hl=zh-tw)來儲存您的資料。您不需要建立任何資料表。

### 授予 Amazon Redshift 叢集的存取權

如要允許來自 Amazon Redshift 叢集的連線，請設定傳入安全性群組規則，允許透過 TCP 在叢集使用的通訊埠上傳入連線。根據預設，Amazon Redshift 會使用通訊埠 `5439`。如要查看或驗證叢集的通訊埠，請在 Amazon Redshift 控制台中查看叢集屬性的「Endpoint」(端點) 欄位。

[設定安全性群組規則](https://docs.aws.amazon.com/vpc/latest/userguide/working-with-security-group-rules.html)，將下列 Google 擁有的 IP 範圍新增至叢集安全性群組的輸入規則。您可以新增與資料集位置對應的 IP 位址，也可以新增下表中的所有 IP 位址。這些 Google 擁有的 IP 位址會保留給 Amazon Redshift 資料遷移作業使用。

**注意：**BigQuery 和 Amazon Redshift 之間的通訊是透過下列 Google 擁有的 IP 位址進行。不過，從 Amazon S3 到 BigQuery 的資料移動作業是透過公開網際網路進行。

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
|  | 特拉維夫 | `me-west1` | 34.165.184.115  34.165.110.74  34.165.174.16  34.165.28.235  34.165.170.172  34.165.187.98  34.165.85.64  34.165.245.97 |
| **非洲** | | | |
|  | 約翰尼斯堡 | `africa-south1` | 34.35.11.24  34.35.10.66  34.35.8.32  34.35.3.248  34.35.2.113  34.35.5.61  34.35.7.53  34.35.3.17 |

#### 多地區位置

| 多地區說明 | 多地區名稱 | IP 位址 |
| --- | --- | --- |
| 歐盟[成員國](https://europa.eu/european-union/about-eu/countries_en)境內的資料中心1 | `EU` | 34.76.156.158  34.76.156.172  34.76.136.146  34.76.1.29  34.76.156.232  34.76.156.81  34.76.156.246  34.76.102.206  34.76.129.246  34.76.121.168 |
| 美國資料中心 | `US` | 35.185.196.212  35.197.102.120   35.185.224.10  35.185.228.170  35.197.5.235  35.185.206.139  35.197.67.234  35.197.38.65  35.185.202.229  35.185.200.120 |

1 位於 `EU` 多區域的資料不會儲存在 `europe-west2` (倫敦) 或 `europe-west6` (蘇黎世) 資料中心。

### 授予 Amazon S3 值區的存取權

您必須擁有 Amazon S3 bucket，才能做為暫存區，將 Amazon Redshift 資料移轉至 BigQuery。如需詳細操作說明，請參閱 [Amazon 說明文件](https://aws.amazon.com/premiumsupport/knowledge-center/create-access-key/)。

1. 建議您建立專屬的 AWS IAM 使用者，並僅授予該使用者 Amazon Redshift 的讀取權限，以及 Amazon S3 的讀取和寫入權限。如要完成這個步驟，您可以套用下列政策：
2. 建立 AWS [IAM 使用者存取金鑰組](https://docs.aws.amazon.com/general/latest/gr/aws-sec-cred-types.html)。

### 使用獨立遷移佇列設定工作負載控制

您也可以[定義用於遷移的 Amazon Redshift 佇列](https://docs.aws.amazon.com/redshift/latest/dg/cm-c-modifying-wlm-configuration.html)，限制及分隔用於遷移的資源。您可以設定這個遷移佇列的並行查詢數量上限。接著，您可以將特定[遷移使用者群組](https://docs.aws.amazon.com/redshift/latest/dg/r_CREATE_GROUP.html)與佇列建立關聯，並在設定遷移作業時使用這些憑證，將資料移轉至 BigQuery。Transfer Service 只能存取遷移佇列。

### 收集轉移資訊

收集使用 BigQuery 資料移轉服務設定遷移作業所需的資訊：

* 請按照[這些操作說明](https://docs.aws.amazon.com/redshift/latest/mgmt/configure-jdbc-connection.html#obtain-jdbc-url)取得 JDBC 網址。
* 取得