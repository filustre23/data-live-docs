Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 設定 Cloud SQL 執行個體存取權

BigQuery 資料移轉服務可讓您透過內部 IP 位址，從不同 Google Cloud 專案的私人 Cloud SQL 執行個體移轉資料。如要為 [BigQuery 資料移轉服務 MySQL 連接器](https://docs.cloud.google.com/bigquery/docs/mysql-transfer?hl=zh-tw)或 [BigQuery 資料移轉服務 PostgreSQL 連接器](https://docs.cloud.google.com/bigquery/docs/postgresql-transfer?hl=zh-tw)建立這項私人連線，請設定虛擬私有雲對接、Cloud SQL Proxy 和網路連結。

## 架構總覽

如要將資料從某項專案中的私人 Cloud SQL 執行個體，移轉至另一項專案中的 BigQuery，BigQuery 資料移轉服務需要連接器網路，才能橋接私人網路連線。

虛擬私有雲網路對等互連僅支援直接對接網路之間的通訊，不會轉送其他連線的流量。因此，透過 Private Service Connect 網路連結進入虛擬私有雲網路的流量，無法跨越對等互連連線，到達對等互連的 Cloud SQL 網路。如要建立這項連線，連接器網路中的 Compute Engine VM 會執行 Cloud SQL Auth Proxy。Proxy 會終止來自網路連結的連入連線，並透過對等互連網路，與 Cloud SQL 執行個體建立經過驗證的連線。

下圖說明 BigQuery 資料移轉服務與私人 Cloud SQL 執行個體之間的網路元件和資料路徑：

## 事前準備

請確認您已備妥下列項目：

* 具備 BigQuery 資料移轉服務連接器的 Google Cloud 專案，以及具備 Cloud SQL 執行個體的另一個 Google Cloud 專案。
* Google Cloud 專案中現有的 MySQL 或 PostgreSQL 資料庫。
* [建立虛擬私有雲](https://docs.cloud.google.com/vpc/docs/create-modify-vpc-networks?hl=zh-tw)、[建立防火牆規則](https://docs.cloud.google.com/network-connectivity/docs/vpn/how-to/configuring-firewall-rules?hl=zh-tw)和安裝軟體的適當權限。
* [虛擬機器 (VM) 執行個體](https://docs.cloud.google.com/compute/docs/instances/create-start-instance?hl=zh-tw)。

## 設定虛擬私有雲對接

如要設定虛擬私有雲對接，您必須從 BigQuery 資料移轉服務連接器專案建立虛擬私有雲對接、在 Cloud SQL 資料庫專案中建立虛擬私有雲對接至 BigQuery 資料移轉服務專案，並設定路由和防火牆規則。

### 從 BigQuery 資料移轉服務連接器專案建立虛擬私有雲對接

1. 在 Google Cloud 控制台中，前往 BigQuery 資料移轉服務連接器專案的「VPC network peering」(虛擬私有雲網路對接) 頁面。

   [前往「VPC Network Peering」(虛擬私有雲網路對接)](https://console.cloud.google.com/networking/vpc-connectivity/peering?hl=zh-tw)
2. 按一下「add 建立對接連線」。
3. 在「Name」(名稱) 欄位中，輸入對接設定的名稱。
4. 在「您的虛擬私有雲網路」部分，選取要在 BigQuery 資料移轉服務連接器專案中對接的虛擬私有雲網路。
5. 在「對接虛擬私有雲網路」部分，選取「在其他專案中」選項。
6. 在「Project ID」(專案 ID) 中，輸入 Cloud SQL 專案的專案 ID。
7. 在「VPC network name」(虛擬私有雲網路名稱) 中，輸入 Cloud SQL 專案中的虛擬私有雲網路名稱。
8. 點選「建立」。

### 在 Cloud SQL 資料庫專案中建立虛擬私有雲對接

如要在 Cloud SQL 資料庫專案中，建立與 BigQuery 資料移轉服務專案的虛擬私有雲對接，請按照下列步驟操作：

1. 在 Google Cloud 控制台中，前往 BigQuery 資料移轉服務連接器專案的「VPC Network Peering」(虛擬私有雲網路對等互連) 頁面。

   [前往「VPC Network Peering」(虛擬私有雲網路對接)](https://console.cloud.google.com/networking/vpc-connectivity/peering?hl=zh-tw)
2. 按一下「add 建立對接連線」。
3. 在「Name」(名稱) 欄位中，輸入對接設定的名稱。
4. 在 Cloud SQL 資料庫專案中，選取要對接的虛擬私有雲網路。
5. 在「Peer project ID」(對等互連專案 ID) 部分，輸入 BigQuery 資料移轉服務專案的專案 ID。
6. 在「Peered VPC network」(對接的虛擬私有雲網路) 部分，輸入 BigQuery 資料移轉服務連接器專案中的虛擬私有雲網路名稱。
7. 點選「建立」。

### 設定路徑和防火牆規則

如果先前設定對等互連連線時，未選取匯入/匯出路徑，請按照下列步驟操作：

1. 前往 BigQuery 資料移轉服務連接器專案的「Routes」(路徑) 頁面。

   [前往「Routes」(路徑)](https://console.cloud.google.com/networking/routes/list?hl=zh-tw)
2. 確認路徑存在，允許對等互連虛擬私有雲環境之間的流量。
3. 前往「Firewall policies」(防火牆政策) 頁面。

   [前往「Firewall policies」(防火牆政策)](https://console.cloud.google.com/networking/firewalls/list?hl=zh-tw)
4. 建立防火牆規則，允許對等互連網路之間必要通訊埠的流量 (例如 MySQL 的通訊埠 3306 和 PostgreSQL 的通訊埠 5432)。
5. 將 BigQuery 資料移轉服務連接器專案所需的自訂防火牆規則，新增至 Cloud SQL 資料庫託管專案。
6. 按照先前步驟，為含有 Cloud SQL 執行個體的專案設定路由和防火牆規則。

## 設定 Cloud SQL Proxy

1. 使用 SSH 連線至 BigQuery 資料移轉服務連接器專案中的虛擬機器 (VM) 執行個體。
2. 在終端機中下載 Cloud SQL Proxy：

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

   將 `NAME` 替換為 Cloud SQL 執行個體連線名稱。

## 連線至內部 Cloud SQL IP 位址

1. 使用 Cloud SQL 執行個體的內部 IP 位址建立連線。
2. 設定應用程式或工具，連線至內部 IP 位址，並指定適當的憑證和資料庫詳細資料。

從其他 Google Cloud 專案連線時，請使用先前部署的 Proxy VM 內部 IP 位址。這項解決方案可解決傳遞對等互連問題。

## 建立網路連結

如要在 BigQuery 資料移轉服務連接器專案中建立網路連結，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「Network attachments」(網路連結) 頁面。

   [前往「Network attachments」(網路連結)](https://console.cloud.google.com/net-services/psc/list/networkAttachments?hl=zh-tw)
2. 按一下「add 建立網路連結」。
3. 輸入網路連結的名稱。
4. 選取適當的虛擬私有雲網路。
5. 在「Region」(區域) 部分，指定 BigQuery 資料移轉服務連接器所在的區域。
6. 在「Subnetwork」(子網路) 中，選取符合設定的適當選項。
7. 按一下「Create network attachment」(建立網路連結)。

## 測試連線

1. 確認具備 Cloud SQL Proxy 的 VM 可連線至 Cloud SQL 執行個體：

   ```
   mysql -u USERNAME -p -h IP_ADDRESS
   ```

   更改下列內容：

   * `USERNAME`：資料庫使用者的使用者名稱
   * `IP_ADDRESS`：Cloud SQL 執行個體的 IP 位址
2. 確認 BigQuery 資料移轉服務連接器專案中的應用程式，可以使用內部 IP 連線至 Cloud SQL 執行個體。

## 疑難排解

如果無法順利設定網路，請按照下列步驟操作：

* 請確認已建立虛擬私有雲對接，且路徑設定正確。
* 確認防火牆規則允許所需通訊埠的流量。
* 檢查 Cloud SQL Proxy 記錄檔是否有錯誤，並確認其運作正常。
* 請確認網路連結設定正確且已連線。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-10-22 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-10-22 (世界標準時間)。"],[],[]]