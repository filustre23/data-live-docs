Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 使用網路連結設定連線

BigQuery 支援聯合查詢，可讓您將查詢陳述式傳送至外部資料庫，並以臨時資料表的形式取得結果。聯合查詢會使用 BigQuery Connection API 建立連線。本文將說明如何提高這個連線的安全性。

由於連線會直接連至資料庫，因此您必須允許 Google Cloud 的流量連至資料庫引擎。為提高安全性，您應只允許來自 BigQuery 查詢的流量。您可以透過下列兩種方式限制流量：

* 定義 BigQuery 連線使用的靜態 IP 位址，並將其新增至外部資料來源的防火牆規則。
* 在 BigQuery 和內部基礎架構之間建立 VPN，並用於查詢。

這兩種技術都支援使用[網路附件](https://docs.cloud.google.com/vpc/docs/create-manage-network-attachments?hl=zh-tw)。

## 事前準備

授予身分與存取權管理 (IAM) 角色，讓使用者取得執行本文各項工作所需的權限。

### 必要的角色

如要取得設定與網路連結連線所需的權限，請要求管理員授予您專案的[Compute 管理員](https://docs.cloud.google.com/iam/docs/roles-permissions/compute?hl=zh-tw#compute.admin)  (`roles/compute.admin`) IAM 角色。如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

這個預先定義的角色具備設定與網路附件連線所需的權限。如要查看確切的必要權限，請展開「Required permissions」(必要權限) 部分：

#### 所需權限

如要設定與網路附件的連線，您必須具備下列權限：

* `compute.networkAttachments.get`
* `compute.networkAttachments.update`

您或許還可透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)取得這些權限。

如要進一步瞭解 BigQuery 中的 IAM 角色和權限，請參閱 [BigQuery IAM 角色和權限](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)。

## 限制

使用網路附件的連線會受到下列限制：

* 網路附件僅支援 [SAP Datasphere 連線](https://docs.cloud.google.com/bigquery/docs/sap-datasphere-federated-queries?hl=zh-tw)。
* 如果是標準區域，網路附件必須與連線位於相同區域。如要連線至 `US` 多區域，網路連結必須位於 `us-central1` 區域。如要建立 `EU` 多區域連線，網路附件必須位於 `europe-west4` 區域。
* 建立網路附件後，就無法進行任何變更。如要以新方式設定任何項目，請重新建立網路連結。
* 除非生產者 (BigQuery) 刪除已分配的資源，否則無法刪除網路附件。如要啟動刪除程序，請[與 BigQuery 支援團隊聯絡](https://docs.cloud.google.com/bigquery/docs/support?hl=zh-tw)。

## 建立網路連結

建立查詢聯盟的連線時，您可以使用選用的網路連結參數，指向提供網路連線的網路連結，從該網路建立資料庫連線。您可以定義靜態 IP 位址或建立 VPN，藉此建立網路連結。無論選擇哪種做法，請按照下列步驟操作：

1. 如果沒有，請[建立虛擬私有雲網路和子網路](https://docs.cloud.google.com/vpc/docs/create-modify-vpc-networks?hl=zh-tw#create-custom-network)。
2. 如要透過定義靜態 IP 位址來建立網路連結，請[使用您建立的網路、區域和子網路，建立具有靜態 IP 位址的 Cloud NAT 閘道](https://docs.cloud.google.com/nat/docs/set-up-manage-network-address-translation?hl=zh-tw#create-nat-gateway)。如要透過建立 VPN 來建立網路附件，請[建立連線至私人網路的 VPN](https://docs.cloud.google.com/network-connectivity/docs/vpn?hl=zh-tw)。
3. 使用您建立的網路、區域和子網路[建立網路連結](https://docs.cloud.google.com/vpc/docs/create-manage-network-attachments?hl=zh-tw#create-manual-accept)。
4. 選用：視貴機構的安全性政策而定，您可能需要 Google Cloud 設定防火牆，[建立防火牆規則](https://docs.cloud.google.com/firewall/docs/using-firewalls?hl=zh-tw#creating_firewall_rules)，並使用下列設定允許輸出：

   * 將「Targets」(目標) 設為「All instances in the network」(網路中的所有執行個體)。
   * 將「Destination IPv4 ranges」(目的地 IPv4 範圍) 設為整個 IP 位址範圍。
   * 將「指定的通訊協定和通訊埠」設為資料庫使用的通訊埠。
5. 設定內部防火牆，允許來自您建立的靜態 IP 位址的輸入流量。這項程序會因資料來源而異。
6. [建立連線](https://docs.cloud.google.com/bigquery/docs/connections-api-intro?hl=zh-tw)，並加入您建立的網路連結名稱。
7. 執行任何[聯合查詢](https://docs.cloud.google.com/bigquery/docs/federated-queries-intro?hl=zh-tw)，將專案與網路連結同步處理。

連線現在已設定網路附件，您可以執行聯邦查詢。

## 定價

* 適用標準[聯合查詢定價](https://docs.cloud.google.com/bigquery/docs/federated-queries-intro?hl=zh-tw#pricing)。
* 使用 VPC 時，須遵守[虛擬私有雲定價](https://cloud.google.com/vpc/pricing?hl=zh-tw)。
* 使用 Cloud VPN 時，須遵守 [Cloud VPN 定價](https://docs.cloud.google.com/network-connectivity/docs/vpn/pricing?hl=zh-tw)。
* 使用 Cloud NAT 須遵守 [Cloud NAT 定價](https://cloud.google.com/nat/pricing?hl=zh-tw)。

## 後續步驟

* 瞭解不同[連線類型](https://docs.cloud.google.com/bigquery/docs/connections-api-intro?hl=zh-tw)。
* 瞭解如何[管理連線](https://docs.cloud.google.com/bigquery/docs/working-with-connections?hl=zh-tw)。
* 瞭解[聯合查詢](https://docs.cloud.google.com/bigquery/docs/federated-queries-intro?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-09 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-09 (世界標準時間)。"],[],[]]