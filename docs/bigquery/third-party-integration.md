Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 分析和商業智慧工具簡介

您可以將數據分析和商業智慧 (BI) 工具與 BigQuery 整合，從資料倉儲中發掘可做為行動依據的洞察資料。多項工具可與 BigQuery 搭配使用，讓您建立互動式資訊主頁、自訂資料應用程式，或執行程式輔助分析，而不必移動資料集。

## 連結試算表

[連結試算表](https://docs.cloud.google.com/bigquery/docs/connected-sheets?hl=zh-tw)可讓您從 [Google 試算表](https://www.google.com/sheets/about/?hl=zh-tw)存取、分析、共用並以圖表呈現數十億列的 BigQuery 資料。連結試算表介面可簡化與非技術專案利害關係人的協作流程、不需額外匯出資料、簡化報表製作，並提供強大的存取控管功能。

如要進一步瞭解如何搭配使用連結試算表與 BigQuery，請參閱「[使用連結試算表](https://docs.cloud.google.com/bigquery/docs/connected-sheets?hl=zh-tw)」。

## Looker

[Looker](https://docs.cloud.google.com/bigquery/docs/looker?hl=zh-tw) 是 Google 的企業平台，用於資料視覺化和商業智慧。適用於進階資料分析、預測分析和自訂資料應用程式。也能連結其他公有雲中的交易資料庫。

如要進一步瞭解如何搭配使用 Looker 和 BigQuery，請參閱「[使用 BigQuery BI Engine 和 Looker 分析資料](https://docs.cloud.google.com/bigquery/docs/looker?hl=zh-tw)」。

## 數據分析

[數據分析](https://docs.cloud.google.com/bigquery/docs/visualize-looker-studio?hl=zh-tw)是 Google 的資料視覺化和商業智慧工具。這項工具可直接從 Google Cloud 控制台連結至 BigQuery，適合用來建立圖表、報表和資訊主頁。

如要進一步瞭解如何搭配使用數據分析和 BigQuery，請參閱「[使用數據分析分析資料](https://docs.cloud.google.com/bigquery/docs/visualize-looker-studio?hl=zh-tw)」。

## 程式輔助分析工具

[程式輔助分析工具](https://docs.cloud.google.com/bigquery/docs/programmatic-analysis?hl=zh-tw)可執行程式碼，分析 BigQuery 中管理的資料。雖然 SQL 是強大的查詢語言，但 Python、Java 或 R 通常能以更簡化、更具表達力的方式執行資料分析。這類工具包括 Jupyter Notebooks 和 Apache Zeppelin 等開放原始碼網頁式應用程式。[Vertex AI Workbench](https://docs.cloud.google.com/gemini-enterprise-agent-platform/notebooks/workbench/introduction?hl=zh-tw) 是 Google 工具，提供 JupyterLab 筆記本環境，可用於程式輔助分析。

## 第三方工具

您也可以使用多種熱門第三方工具 (例如 [Tableau](https://help.tableau.com/current/pro/desktop/en-us/examples_googlebigquery.htm) 和 [Microsoft Power BI](https://docs.microsoft.com/en-us/power-bi/connect-data/desktop-connect-bigquery)) 連線至 BigQuery。

BigQuery Ready 計畫提供[經過驗證的合作夥伴解決方案完整清單](https://docs.cloud.google.com/bigquery/docs/bigquery-ready-partners?hl=zh-tw)。

如需解決方案相關協助，建議您與 [Google Cloud Ready - BigQuery 合作夥伴](https://console.cloud.google.com/bigquery/partner-center?hl=zh-tw)聯絡。如果 BigQuery 運作正常，Cloud Customer Care 不會支援第三方軟體。

### 網路連線

所有部署在具有外部 IP 位址的主機和服務上的商業智慧和資料分析解決方案，都可以透過網際網路，使用公開的 [BigQuery REST API](https://docs.cloud.google.com/bigquery/docs/reference/rest?hl=zh-tw) 和 RPC 型 [BigQuery Storage API](https://docs.cloud.google.com/bigquery/docs/reference/storage?hl=zh-tw) 存取 BigQuery。

部署在只有內部 IP 位址的 [Compute Engine](https://docs.cloud.google.com/compute?hl=zh-tw) VM 執行個體上的第三方 BI 和資料分析解決方案，可以使用[Private Google Access](https://docs.cloud.google.com/vpc/docs/private-google-access?hl=zh-tw)存取 Google API 和服務，例如 BigQuery。如要為 Private Google Access 啟用子網路並查看相關規定，請參閱「[設定 Private Google Access](https://docs.cloud.google.com/vpc/docs/configure-private-google-access?hl=zh-tw)」。

如要部署在內部部署主機上的第三方 BI 和資料分析解決方案，可藉由[內部部署主機的私人 Google 存取權](https://docs.cloud.google.com/vpc/docs/private-google-access-hybrid?hl=zh-tw)，以使用 Google API 和 BigQuery 等服務。這項服務會透過 [Cloud VPN](https://docs.cloud.google.com/network-connectivity/docs/vpn?hl=zh-tw) 或 [Cloud Interconnect](https://docs.cloud.google.com/network-connectivity/docs/interconnect?hl=zh-tw)，在資料中心與 Google Cloud之間建立私人連線。地端部署主機不需要外部 IP 位址，而是使用內部 [RFC 1918](https://tools.ietf.org/html/rfc1918) IP 位址。如要為地端部署主機啟用 Private Google Access，您必須在地端部署和虛擬私有雲網路中設定 DNS、防火牆規則和路由。如要進一步瞭解地端部署主機的 Private Google Access，請參閱「[為地端部署主機設定 Private Google Access](https://docs.cloud.google.com/vpc/docs/configure-private-google-access-hybrid?hl=zh-tw)」。

如果您自行管理第三方 BI 解決方案的執行個體，建議將其部署在 [Compute Engine](https://docs.cloud.google.com/compute?hl=zh-tw) 上，盡可能縮短執行個體與 BigQuery 之間的延遲時間。

如果商業智慧解決方案支援，建議您盡可能在報表或資訊主頁查詢中設定篩選器。此步驟將篩選器以 `WHERE` 子句推送至 BigQuery。雖然設定這些篩選器不會減少 BigQuery 須掃描的資料量，卻能減少透過網路返回的資料量。

如要進一步瞭解網路和查詢最佳化，請參閱「[最佳化工作負載](https://docs.cloud.google.com/bigquery/docs/admin-intro?hl=zh-tw#optimize_workloads)」和「[查詢效能最佳化簡介](https://docs.cloud.google.com/bigquery/docs/best-practices-performance-overview?hl=zh-tw)」。

### ODBC 和 JDBC 驅動程式

如果第三方解決方案和自訂應用程式未與 [BigQuery API](https://docs.cloud.google.com/bigquery/docs/reference/libraries-overview?hl=zh-tw) 整合，[Magnitude Simba](https://www.magnitude.com/products/data-connectivity) 會提供 [ODBC](https://wikipedia.org/wiki/Open_Database_Connectivity) 和 [JDBC](https://wikipedia.org/wiki/Java_Database_Connectivity) 驅動程式，協助您搭配現有工具使用 BigQuery。

### 驗證

BigQuery API 使用 [OAuth 2.0](https://tools.ietf.org/html/rfc6749) 存取權杖驗證要求。OAuth 2.0 存取憑證是一組字串，可向 API 授予暫時存取權。[Google 的 OAuth 2.0 伺服器](https://developers.google.com/identity/protocols/OAuth2WebServer?hl=zh-tw#obtainingaccesstokens)會為所有 Google API 授予存取權杖。存取憑證有一個相關聯的[範圍](https://tools.ietf.org/html/rfc6749#section-3.3)，並會受到這個範圍的限制。如需與 BigQuery API 相關聯的範圍，請參閱完整的 [Google API 範圍清單](https://developers.google.com/identity/protocols/googlescopes?hl=zh-tw#bigqueryv2)。

提供原生 BigQuery 整合功能的解決方案，可使用 [OAuth 2.0 通訊協定](https://developers.google.com/identity/protocols/OAuth2?hl=zh-tw)或客戶提供的[服務帳戶私密金鑰](https://docs.cloud.google.com/iam/docs/creating-managing-service-account-keys?hl=zh-tw)，自動產生 BigQuery 的存取權杖。同樣地，依賴 Simba ODBC/JDBC 驅動程式的解決方案也可以取得 [Google 使用者帳戶](https://www.simba.com/products/BigQuery/doc/ODBC_InstallGuide/mac/content/odbc/bq/configuring/authenticating/useraccount.htm)或 [Google 服務帳戶](https://www.simba.com/products/BigQuery/doc/ODBC_InstallGuide/mac/content/odbc/bq/configuring/authenticating/serviceaccount.htm)的存取權杖。

## 後續步驟

* 瞭解如何[使用連結試算表](https://docs.cloud.google.com/bigquery/docs/connected-sheets?hl=zh-tw)。
* 瞭解如何[在數據分析中以圖表呈現資料](https://docs.cloud.google.com/bigquery/docs/visualize-looker-studio?hl=zh-tw)。
* 瞭解如何[使用 Looker](https://docs.cloud.google.com/bigquery/docs/looker?hl=zh-tw)。
* 瞭解如何[使用 ODBC 和 JDBC 驅動程式](https://docs.cloud.google.com/bigquery/docs/reference/odbc-jdbc-drivers?hl=zh-tw)。
* 瞭解如何[使用程式輔助分析工具](https://docs.cloud.google.com/bigquery/docs/programmatic-analysis?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-11-12 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-11-12 (世界標準時間)。"],[],[]]