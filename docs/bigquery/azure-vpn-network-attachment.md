Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 設定 Azure-Google Cloud VPN 網路附件

本文件提供高層級指南，說明如何在 Google Cloud 與 Microsoft Azure 之間建立 VPN 連線。該文件也提供有關在 Google Cloud中建立網路連結的指示。

## 事前準備

請確認你已備妥下列項目：

* 具備 Azure 和 Google Cloud 帳戶的適當權限。
* Azure 和Google Cloud中的現有 VPC。

## 在 Google Cloud上設定網路

Google Cloud 上的設定需要建立虛擬私有雲網路、客戶閘道和 VPN 連線。

### 建立虛擬私有雲網路

1. 在 Google Cloud 控制台中，前往「VPC Networks」(虛擬私有雲網路) 頁面。

   [前往「VPC networks」(虛擬私有雲網路)](https://console.cloud.google.com/networking/networks/list?hl=zh-tw)
2. 按一下 add「建立虛擬私有雲網路」。
3. 提供網路名稱。
4. 視需要設定子網路。
5. 按一下 [建立]。

詳情請參閱「[建立及管理虛擬私有雲網路](https://docs.cloud.google.com/vpc/docs/create-modify-vpc-networks?hl=zh-tw)」。

### 建立 VPN 閘道

**注意：** 下列步驟說明如何建立[傳統版 VPN](https://docs.cloud.google.com/network-connectivity/docs/vpn/concepts/overview?hl=zh-tw#classic-vpn)。如果高可用性 (HA) VPN 適合您的用途，您可以改為建立這類 VPN。如需更多資訊，請參閱「[建立連結至對接 VPN 閘道的高可用性 VPN 閘道](https://docs.cloud.google.com/network-connectivity/docs/vpn/how-to/creating-ha-vpn?hl=zh-tw)」。

1. 在 Google Cloud 控制台中，前往「Cloud VPN gateways」頁面。

   [前往 Cloud VPN 閘道](https://console.cloud.google.com/hybrid/vpn?tab=gateways&hl=zh-tw)
2. 按一下「建立 VPN 閘道」。
3. 選取「傳統版 VPN」選項按鈕。
4. 提供 VPN 閘道名稱。
5. 選取要用來建立 VPN 閘道和通道的現有 VPC 網路。
6. 選取地區。
7. 在「IP address」(IP 位址) 部分，建立或選擇現有地區[外部 IP 位址](https://docs.cloud.google.com/compute/docs/ip-addresses?hl=zh-tw#reservedaddress)。
8. 提供通道名稱。
9. 針對「遠端對等互連 IP 位址」，請輸入 Azure VPN 閘道的公開 IP 位址。
10. 指定 **IKE 版本**和 **IKE 預先共用金鑰**的選項。
11. 視需要指定轉送選項，將流量導向 Azure IP 範圍。
12. 按一下 [建立]。

詳情請參閱「[建立閘道和通道](https://docs.cloud.google.com/network-connectivity/docs/vpn/how-to/creating-static-vpns?hl=zh-tw#create_a_gateway_and_tunnel)」。

## 在 Azure 上設定網路

1. 建立虛擬網路。如需詳細操作說明，請參閱 Azure 說明文件中的[快速入門：使用 Azure 入口網站建立虛擬網路](https://learn.microsoft.com/en-us/azure/virtual-network/quick-create-portal)和[建立虛擬網路](https://learn.microsoft.com/en-us/azure/vpn-gateway/tutorial-site-to-site-portal#CreatVNet)。
2. 建立 VPN，並將其路由至您在本文件「[建立虛擬私有雲網路](#create-vpc-network)」一節中建立的虛擬網路。如需詳細操作說明，請參閱「[教學課程：使用 Azure 入口網站建立及管理 VPN 閘道](https://learn.microsoft.com/en-us/azure/vpn-gateway/tutorial-create-gateway-portal)」和 Azure 說明文件中的「[建立 VPN 閘道](https://learn.microsoft.com/en-us/azure/vpn-gateway/tutorial-site-to-site-portal#VNetGateway)」。
3. 使用Google Cloud VPN 閘道的公開 IP 位址和Google Cloud 網路的位址空間，建立本機網路閘道。如需詳細操作說明，請參閱 Azure 說明文件中的「[建立本機網路閘道](https://learn.microsoft.com/en-us/azure/vpn-gateway/tutorial-site-to-site-portal#LocalNetworkGateway)」。
4. 使用您建立的本機網路閘道建立站對站 VPN 連線。如需詳細操作說明，請參閱 Azure 說明文件中的「[建立 VPN 連線](https://learn.microsoft.com/en-us/azure/vpn-gateway/tutorial-site-to-site-portal#CreateConnection)」。

## 建立 Google Cloud 網路連結

如要將網路連結至 Private Service Connect，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「Private Service Connect」頁面。

   [前往 Private Service Connect](https://console.cloud.google.com/net-services/psc/list?hl=zh-tw)
2. 選取要附加至網路的資源。
3. 按一下 [編輯]。
4. 在「Network attachments」(網路附件) 分頁中，選取您在本文件「Create the VPC network」(建立虛擬私有雲網路) 一節中建立的網路。
5. 按一下 [儲存]。

詳情請參閱「[建立網路連結](https://docs.cloud.google.com/vpc/docs/create-manage-network-attachments?hl=zh-tw#create-network-attachments)」。

## 確認網路連線

請確認 Google Cloud 中的 VM 可連上 Azure 中的 VM，且 Azure 中的 VM 可連上 Google Cloud中的 VM。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-06 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-06 (世界標準時間)。"],[],[]]