Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 設定 Cloud SQL 執行個體存取權

本文將詳細說明如何設定虛擬私有雲對等互連、安裝 Cloud SQL Proxy，以及跨不同 Google Cloud 專案連線至內部 Cloud SQL IP 位址。這項設定可確保 Cloud SQL 執行個體與下列連接器之間的通訊安全且有效率：

* [BigQuery 資料移轉服務 MySQL 連接器](https://docs.cloud.google.com/bigquery/docs/mysql-transfer?hl=zh-tw)
* [BigQuery 資料移轉服務 PostgreSQL 連接器](https://docs.cloud.google.com/bigquery/docs/postgresql-transfer?hl=zh-tw)。

本文件也將說明如何在 BigQuery 資料移轉服務連接器專案中建立網路附件。

## 事前準備

請確認你已備妥下列項目：

* 存取使用 BigQuery 資料移轉服務連接器的 Google Cloud 專案，以及另一個使用 Cloud SQL 執行個體的 Google Cloud 專案。
* Google Cloud 專案中現有的 MySQL 或 PostgreSQL 資料庫。
* [建立 VPC](https://docs.cloud.google.com/vpc/docs/create-modify-vpc-networks?hl=zh-tw)、[建立防火牆規則](https://docs.cloud.google.com/network-connectivity/docs/vpn/how-to/configuring-firewall-rules?hl=zh-tw)及安裝軟體的適當權限。
* [虛擬機器 (VM) 執行個體](https://docs.cloud.google.com/compute/docs/instances/create-start-instance?hl=zh-tw)。

## 設定虛擬私有雲對等互連

如要設定 VPC 對等連線，您必須從 BigQuery 資料移轉服務連接器專案建立 VPC 對等連線，在 Cloud SQL 資料庫專案中建立 VPC 對等連線至 BigQuery 資料移轉服務專案，並設定路由和防火牆規則。

### 透過 BigQuery 資料移轉服務連接器專案建立 VPC 對等連線

1. 在 Google Cloud 控制台中，前往 BigQuery 資料移轉服務連接器專案的「VPC network peering」頁面。

   [前往「VPC Network Peering」(虛擬私有雲網路對等互連)](https://console.cloud.google.com/networking/peering/list?hl=zh-tw)
2. 按一下 add「建立對接連線」。
3. 在「Name」欄位中，輸入對等互連設定的名稱。
4. 在「Your VPC network」(您的 VPC 網路) 中，選取您要在 BigQuery 資料移轉服務連接器專案中對等互連的 VPC 網路。
5. 在「對等互連虛擬私有雲網路」中，選取「在其他專案中」選項。
6. 在「Project ID」中，輸入 Cloud SQL 專案的專案 ID。
7. 在「虛擬私有雲端網路名稱」中，輸入 Cloud SQL 專案中的虛擬私有雲端網路名稱。
8. 按一下 [建立]。

### 在 Cloud SQL 資料庫專案中建立 VPC 對等互連

如要在 Cloud SQL 資料庫專案中建立 VPC 對等連線，以連線至 BigQuery 資料移轉服務專案，請按照下列步驟操作：

1. 在 Google Cloud 控制台中，前往 BigQuery 資料移轉服務連接器專案的「VPC Network Peering」頁面。

   [前往「VPC Network Peering」(虛擬私有雲網路對等互連)](https://console.cloud.google.com/networking/peering/list?hl=zh-tw)
2. 按一下 add「建立對接連線」。
3. 在「Name」欄位中，輸入對等互連設定的名稱。
4. 選取您要在 Cloud SQL 資料庫專案中建立對等互連的 VPC 網路。
5. 在「Peer project ID」中，輸入 BigQuery 資料移轉服務專案的專案 ID。
6. 針對「對等互連虛擬私有雲網路」，請在 BigQuery 資料移轉服務連接器專案中輸入虛擬私有雲網路的名稱。
7. 按一下 [建立]。

### 設定路徑和防火牆規則

如果您先前在設定對等連線時未選取匯入/匯出路徑，請按照下列步驟操作：

1. 前往 BigQuery 資料移轉服務連接器專案的「**路由**」頁面。

   [前往「Routes」(路徑)](https://console.cloud.google.com/networking/routes/list?hl=zh-tw)
2. 確認路徑是否存在，以便在已建立夥伴關係的虛擬私有雲環境之間傳輸流量。
3. 前往「防火牆政策」頁面。

   [前往「防火牆政策」](https://console.cloud.google.com/networking/firewalls/list?hl=zh-tw)
4. 建立防火牆規則，允許在對等網路之間的必要通訊埠 (例如 MySQL 的 3306 通訊埠和 PostgreSQL 的 5432 通訊埠) 上傳輸流量。
5. 將 BigQuery 資料移轉服務連接器專案所需的自訂防火牆規則，新增至 Cloud SQL 資料庫代管專案。
6. 如同先前步驟所述，使用 Cloud SQL 執行個體為專案設定路徑和防火牆規則。

## 設定 Cloud SQL Proxy

1. 使用 SSH 連線至 BigQuery 資料移轉服務連接器專案中的虛擬機器 (VM) 執行個體。
2. 在終端下載 Cloud SQL Proxy：

   ```
   wget https://dl.google.com/cloudsql/cloud_sql_proxy.linux.amd64 -O cloud_sql_proxy
   ```
3. 更新下載檔案的權限：

   ```
   chmod +x cloud_sql_proxy
   ```
4. 執行 Cloud SQL Proxy：

   ```
   ./cloud_sql_proxy -instances=NAME=tcp:3306 or 5432 &
   ```

   將 `NAME` 改成 Cloud SQL 執行個體連線的名稱。

## 連線至 Cloud SQL 內部 IP 位址

1. 使用 Cloud SQL 執行個體的內部 IP 位址進行連線。
2. 設定應用程式或工具以連線至內部 IP 位址，並指定適當的憑證和資料庫詳細資料。

從其他 Google Cloud 專案連線時，請使用先前部署的 Proxy VM 的內部 IP 位址。這個解決方案可解決轉介對等連線問題。

## 建立網路連結

如要在 BigQuery 資料移轉服務連接器專案中建立網路附件，請按照下列步驟操作：

1. 在 Google Cloud 控制台中，前往「Network attachments」頁面。

   [前往「網路附件」](https://console.cloud.google.com/net-services/psc/list/networkAttachments?hl=zh-tw)
2. 依序按一下 add「建立網路連結」。
3. 提供網路連結的名稱。
4. 選取適當的 VPC 網路。
5. 在「Region」中，指定 BigQuery 資料移轉服務連接器所在的區域。
6. 在「Subnetwork」(子網路) 中，選取與設定相符的適當選項。
7. 按一下「Create network attachment」(建立網路連結)。

## 測試連線

1. 確認含有 Cloud SQL Proxy 的 VM 能否連線至 Cloud SQL 執行個體：

   ```
   mysql -u USERNAME -p -h IP_ADDRESS
   ```

   更改下列內容：

   * `USERNAME`：資料庫使用者的使用者名稱
   * `IP_ADDRESS`：Cloud SQL 執行個體的 IP 位址
2. 請確認 BigQuery 資料移轉服務連接器專案中的應用程式可以使用內部 IP 連線至 Cloud SQL 執行個體。

## 疑難排解

如果在設定網路時遇到問題，請按照下列步驟操作：

* 請確認已建立 VPC 對等互連，且路徑設定正確無誤。
* 確認防火牆規則允許在必要通訊埠上傳輸流量。
* 檢查 Cloud SQL Proxy 記錄是否有錯誤，並確認其是否正常執行。
* 確認網路附件已正確設定及連線。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-06 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-06 (世界標準時間)。"],[],[]]