Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 設定 AWS VPN 和網路連結

您可以透過 VPN 和網路連結，在 Amazon Web Services (AWS) 和 Google Cloud之間建立可靠且安全性更高的連線。只要在兩個雲端環境中設定閘道、通道和路由，即可在部署的資料庫和執行個體之間導向流量。

## 事前準備

請確認您已備妥下列項目：

* 具備適當權限，可存取 AWS 和 Google Cloud 帳戶。
* AWS 和 Google Cloud中現有的[虛擬私有雲](https://docs.cloud.google.com/vpc/docs/overview?hl=zh-tw)。

## 在 AWS 設定網路

1. 建立虛擬私人閘道，並連結至部署資料庫的虛擬私有雲。如需詳細操作說明，請參閱 AWS 說明文件中的「[建立 AWS Direct Connect 虛擬私有閘道](https://docs.aws.amazon.com/directconnect/latest/UserGuide/create-virtual-private-gateway.html)」。
2. 使用 Google CloudVPN 閘道的公開 IP 位址建立客戶閘道。如需詳細操作說明，請參閱 AWS 說明文件中的「[建立客戶閘道](https://docs.aws.amazon.com/vpn/latest/s2svpn/SetUpVPNConnections.html#vpn-create-cgw)」。
3. 使用先前建立的虛擬私人閘道和客戶閘道，建立 VPN 連線。如需詳細操作說明，請參閱 AWS 說明文件中的「[Get started with AWS Client VPN](https://docs.aws.amazon.com/vpn/latest/clientvpn-admin/cvpn-getting-started.html)」(開始使用 AWS Client VPN) 和「[How do I establish an encrypted connection over an AWS Direct Connect connection?](https://repost.aws/knowledge-center/create-vpn-direct-connect)」(如何透過 AWS Direct Connect 連線建立加密連線？)。
4. 新增路徑，使用 VPN 連線將流量導向 Google Cloud IP 範圍。如需詳細操作說明，請參閱 AWS 說明文件中的「[設定路由表](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Route_Tables.html)」和「[設定路由](https://docs.aws.amazon.com/vpn/latest/s2svpn/SetUpVPNConnections.html#vpn-configure-route-tables)」。

## 在 Google Cloud上設定網路

在 Google Cloud 上設定時，必須建立 VPN 閘道和 VPN 通道、設定路由，以及建立 Google Cloud網路連結。

### 建立 VPN 閘道

**注意：** 下列步驟說明如何建立[傳統版 VPN](https://docs.cloud.google.com/network-connectivity/docs/vpn/concepts/overview?hl=zh-tw#classic-vpn)。如果符合您的用途，也可以改為建立高可用性 (HA) VPN。詳情請參閱「[建立連結至對接 VPN 閘道的高可用性 VPN 閘道](https://docs.cloud.google.com/network-connectivity/docs/vpn/how-to/creating-ha-vpn?hl=zh-tw)」。

1. 前往 Google Cloud 控制台的「Cloud VPN gateways」(Cloud VPN 閘道) 頁面。

   [前往「Cloud VPN gateways」(Cloud VPN 閘道) 頁面](https://console.cloud.google.com/hybrid/vpn?tab=gateways&hl=zh-tw)
2. 按一下「建立 VPN 閘道」。
3. 選取「傳統版 VPN」選項按鈕。
4. 提供 VPN 閘道名稱。
5. 選取現有的虛擬私有雲網路，在當中建立 VPN 閘道和通道。
6. 選取地區。
7. 在「IP address」(IP 位址) 部分，建立或選擇現有的區域[外部 IP 位址](https://docs.cloud.google.com/compute/docs/ip-addresses?hl=zh-tw#reservedaddress)。
8. 提供通道名稱。
9. 在「Remote peer IP address」(遠端對等互連 IP 位址) 中，輸入 AWS VPN 閘道公開 IP 位址。
10. 指定「IKE version」(IKE 版本) 和「IKE pre-shared key」(IKE 預先共用金鑰) 的選項。
11. 視需要指定轉送選項，將流量導向 AWS IP 範圍。
12. 點選「建立」。

詳情請參閱「[建立閘道和通道](https://docs.cloud.google.com/network-connectivity/docs/vpn/how-to/creating-static-vpns?hl=zh-tw#create_a_gateway_and_tunnel)」。

### 建立網路連結

1. 前往 Google Cloud 控制台的「Network attachments」(網路連結) 頁面。

   [前往「Network attachments」(網路連結)](https://console.cloud.google.com/net-services/psc/list/networkAttachments?hl=zh-tw)
2. 按一下「add 建立網路連結」。
3. 輸入網路連結的名稱。
4. 在「Network」(網路) 部分，選取適當的虛擬私有雲網路。
5. 在「Region」(區域)，選擇 VPN 閘道的位置。
6. 在「子網路」部分，選取先前建立的 VPN 通道。
7. 按一下「Create network attachment」(建立網路連結)。

詳情請參閱「[建立網路連結](https://docs.cloud.google.com/vpc/docs/create-manage-network-attachments?hl=zh-tw#create-network-attachments)」。

## 測試 VPN 連線

1. 在 AWS 和 Google Cloud
   虛擬私有雲環境中部署執行個體。
2. 如要驗證連線能力，請嘗試透過 VPN 連線或對執行個體進行連線偵測 (ping)。
3. 確認安全性群組和防火牆規則允許流量通過 VPN。

## 疑難排解

如果設定網路連結時遇到問題，請按照下列步驟操作：

* 確認 VPN 連線在 AWS 控制台和 Google Cloud 控制台中都正常運作。
* 查看 VPN 記錄，瞭解是否有錯誤或封包遺失。
* 確認 AWS 和Google Cloud 中的轉送表格設定正確。
* 確認 AWS 安全性群組和 Google Cloud 防火牆規則中，都已開啟必要通訊埠。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-10-29 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-10-29 (世界標準時間)。"],[],[]]