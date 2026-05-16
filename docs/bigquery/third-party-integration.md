Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 與第三方工具相互整合

本文說明您可能需要採取的初始設定步驟，以管理 BigQuery 與第三方商業智慧 (BI) 解決方案之間的連結。如需解決方案方面的協助，建議與 [Google Cloud Ready - BigQuery 合作夥伴](https://console.cloud.google.com/bigquery/partner-center?hl=zh-tw)聯絡。如果 Cloud Customer Care 判斷 BigQuery 運作正常，就不會支援第三方軟體。

### 網路連線

所有部署在主機和外部 IP 位址服務的 BI 和資料分析解決方案，都可以透過 [BigQuery REST API](https://docs.cloud.google.com/bigquery/docs/reference/rest?hl=zh-tw) 以及以 RPC 為基礎的 [BigQuery Storage API](https://docs.cloud.google.com/bigquery/docs/reference/storage?hl=zh-tw) 在網際網路上公開存取 BigQuery。

僅以內部 IP 位址 (無外部 IP 位址) 部署在 [Compute Engine](https://docs.cloud.google.com/compute?hl=zh-tw) VM 執行個體上的第三方商業智慧 (BI) 和資料分析解決方案可以使用 [Private Google Access](https://docs.cloud.google.com/vpc/docs/private-google-access?hl=zh-tw)來存取 Google API 和 BigQuery 之類的服務。您可以根據不同的子網路來決定是否啟用該子網路的私人 Google 存取權；這是虛擬私人雲端網路中的子網路設定。如要啟用子網路的私人 Google 存取權以及查看需求條件，請參閱[設定私人 Google 存取權](https://docs.cloud.google.com/vpc/docs/configure-private-google-access?hl=zh-tw)。

如要部署在內部部署主機上的第三方商業智慧 (BI) 和資料分析解決方案，可藉由[內部部署主機的 Private Google Access](https://docs.cloud.google.com/vpc/docs/private-google-access-hybrid?hl=zh-tw)，以使用 Google API 和 BigQuery 等服務。這項服務會透過 [Cloud VPN](https://docs.cloud.google.com/network-connectivity/docs/vpn?hl=zh-tw) 或 [Cloud Interconnect](https://docs.cloud.google.com/network-connectivity/docs/interconnect?hl=zh-tw) 建立從您的資料中心到 Google Cloud的私人連線。地端部署主機不需要外部 IP 位址；而是使用內部 [RFC 1918](https://tools.ietf.org/html/rfc1918) IP 位址。如要啟用內部部署主機的私人 Google 存取權，您必須在內部部署與虛擬私人雲端網路中設定 DNS、防火牆規則與路徑。如要進一步瞭解地端部署主機的 Private Google Access，請參閱[為地端部署主機設定 Private Google Access](https://docs.cloud.google.com/vpc/docs/configure-private-google-access-hybrid?hl=zh-tw)。

如果您選擇管理自己的第三方 BI 解決方案執行個體，建議您在 [Compute Engine](https://docs.cloud.google.com/compute?hl=zh-tw) 上部署這個解決方案，以便利用 Google 的中樞網路，並儘量減少執行個體與 BigQuery 之間的延遲。

如果您的 BI 解決方案可支援，請盡可能考慮在報告或資訊主頁的查詢中設定篩選器。此步驟將篩選器以 `WHERE` 子句推送至 BigQuery。雖然設定這些篩選器不會減少 BigQuery 須掃描的資料量，卻能減少透過網路返回的資料量。

如要進一步瞭解網路和查詢最佳化的資訊，請參閱「[將資料倉儲遷移至 BigQuery：效能最佳化](https://docs.cloud.google.com/architecture/dw2bq/dw-bq-performance-optimization?hl=zh-tw)」和「[最佳化查詢效能簡介](https://docs.cloud.google.com/bigquery/docs/best-practices-performance-overview?hl=zh-tw)」。

### API 和 ODBC/JDBC 整合

Google 的商業智慧 (BI) 和資料分析產品，例如：[數據分析](https://docs.cloud.google.com/looker-studio?hl=zh-tw)、[Looker](https://docs.cloud.google.com/looker?hl=zh-tw)、[Managed Service for Apache Spark](https://docs.cloud.google.com/dataproc?hl=zh-tw) 和 [Vertex AI Workbench 執行個體](https://docs.cloud.google.com/vertex-ai/docs/workbench/instances/introduction?hl=zh-tw)，以及第三方解決方案，例如 [Tableau](https://www.tableau.com/)，可使用 [BigQuery API](https://docs.cloud.google.com/bigquery/docs/reference/libraries-overview?hl=zh-tw) 直接與 BigQuery 整合。

對於其他第三方解決方案和自訂應用程式，Google 與 [Magnitude Simba](https://www.magnitude.com/products/data-connectivity) 合作，提供 [ODBC](https://wikipedia.org/wiki/Open_Database_Connectivity) 和 [JDBC](https://wikipedia.org/wiki/Java_Database_Connectivity) 驅動程式。這些驅動程式主要旨在協助您透過未與 [BigQuery API](https://docs.cloud.google.com/bigquery/docs/reference/libraries-overview?hl=zh-tw) 整合的現有工具和基礎架構，運用 BigQuery 的強大功能。

詳情請參閱 Google Cloud 關於 [BigQuery 的 ODBC 和 JDBC 驅動程式](https://docs.cloud.google.com/bigquery/docs/reference/odbc-jdbc-drivers?hl=zh-tw)的說明文件。

### 驗證

BigQuery API 會使用 [OAuth 2.0](https://tools.ietf.org/html/rfc6749) 存取權杖來驗證要求。OAuth 2.0 存取憑證是一組字串，可向 API 授予暫時存取權。[Google 的 OAuth 2.0 伺服器](https://developers.google.com/identity/protocols/OAuth2WebServer?hl=zh-tw#obtainingaccesstokens)會授予所有 Google API 的存取憑證。存取憑證有一個相關聯的[範圍](https://tools.ietf.org/html/rfc6749#section-3.3)，並會受到這個範圍的限制。如需與 BigQuery API 相關聯的範圍，請參閱完整的 [Google API 範圍清單](https://developers.google.com/identity/protocols/googlescopes?hl=zh-tw#bigqueryv2)。

提供原生 BigQuery 整合的 BI 和資料分析解決方案可以藉由使用 [OAuth 2.0 通訊協定](https://developers.google.com/identity/protocols/OAuth2?hl=zh-tw)或由客戶提供的[服務帳戶私密金鑰](https://docs.cloud.google.com/iam/docs/creating-managing-service-account-keys?hl=zh-tw)自動產生 BigQuery 存取權杖。同樣地，使用 Simba ODBC/JDBC 驅動程式的解決方案也可以取得 [Google 使用者帳戶](https://www.simba.com/products/BigQuery/doc/ODBC_InstallGuide/mac/content/odbc/bq/configuring/authenticating/useraccount.htm)或 [Google 服務帳戶](https://www.simba.com/products/BigQuery/doc/ODBC_InstallGuide/mac/content/odbc/bq/configuring/authenticating/serviceaccount.htm)的存取權杖。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-16 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-16 (世界標準時間)。"],[],[]]