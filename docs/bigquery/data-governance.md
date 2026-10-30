Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# BigQuery 資料治理簡介

BigQuery 內建管理功能，可讓您在整個資料生命週期中探索、管理、監控及控管資料和 AI 資產。資料團隊可以整理資料集、充實中繼資料、追蹤品質，並強制執行法規遵循政策，同時安全地大規模共用資產。

這些功能由 [Knowledge Catalog](https://docs.cloud.google.com/knowledge-catalog/docs/catalog-overview?hl=zh-tw) 提供，這是一個全天候運作的通用內容比對引擎，可使用整個資料資產的技術中繼資料和業務語意，為下游應用程式和資料分析師建立自我學習脈絡圖。

## 資料探索

BigQuery 會在 Google Cloud中探索整個組織的資料，無論資料位於 BigQuery、Spanner、Cloud SQL、Pub/Sub 還是 Cloud Storage。中繼資料會自動擷取並儲存在 Knowledge Catalog。舉例來說，您可以從 Cloud Storage 擷取結構化和非結構化資料的中繼資料，並自動大規模建立可供查詢的 BigLake 資料表。這樣一來，您就能使用開放原始碼引擎執行分析，不必複製資料。

您也可以使用自訂連接器，從第三方資料來源擷取中繼資料並建立目錄。

BigQuery 提供下列資料探索功能：

* **搜尋。**搜尋專案和組織中的資料和 AI 資源。在 Google Cloud 控制台的 BigQuery 中，使用[語意搜尋](https://docs.cloud.google.com/bigquery/docs/search-resources?hl=zh-tw) ([預先發布版](https://cloud.google.com/products?hl=zh-tw#product-launch-stages)) 功能，以日常用語搜尋資源。您也可以在 Knowledge Catalog 使用[關鍵字搜尋](https://docs.cloud.google.com/knowledge-catalog/docs/search-assets?hl=zh-tw)功能尋找資源。
* **[自動探索 Cloud Storage 資料](https://docs.cloud.google.com/bigquery/docs/automatic-discovery?hl=zh-tw)。**掃描 Cloud Storage bucket 中的資料，擷取中繼資料並編入目錄。自動探索功能會為結構化和非結構化資料建立資料表。
* **[中繼資料匯入](https://docs.cloud.google.com/knowledge-catalog/docs/managed-connectivity-overview?hl=zh-tw)。**從第三方系統大量匯入中繼資料至 Knowledge Catalog。您可以建構自訂連接器，從資料來源擷取資料，然後執行代管連線能力管道，自動調度中繼資料匯入工作流程。
* **[中繼資料匯出](https://docs.cloud.google.com/knowledge-catalog/docs/export-metadata?hl=zh-tw)。**從 Knowledge Catalog 大規模匯出中繼資料。您可以使用 BigQuery 分析匯出的中繼資料，或將中繼資料整合至自訂應用程式或程式輔助處理工作流程。

## 收錄和資料監管

為提升資料的發現度和可用性，資料監管者和管理員可以使用 BigQuery 查看、更新及分析中繼資料。BigQuery 的資料管理和監管功能可確保資料準確、一致，並符合組織政策。

BigQuery 提供下列資料管理功能：

* **[組織詞彙](https://docs.cloud.google.com/knowledge-catalog/docs/create-glossary?hl=zh-tw)**：在詞彙表中定義貴機構的術語，可改善上下文、協作和搜尋功能。找出這些字詞的資料監管員，並將字詞附加到資料資產欄位。
* **[資料洞察](https://docs.cloud.google.com/bigquery/docs/data-insights?hl=zh-tw)。**
  Gemini 會使用中繼資料，生成有關資料表的自然語言問題，以及回答問題的 SQL 查詢。這些資料洞察資訊可協助您發掘模式、評估資料品質，以及執行統計分析。
* **[資料剖析](https://docs.cloud.google.com/bigquery/docs/data-profile-scan?hl=zh-tw)。**找出 BigQuery 資料表中資料欄的常見統計特徵，更有效地解讀及分析資料。
* **[資料品質](https://docs.cloud.google.com/bigquery/docs/data-quality-scan?hl=zh-tw)。**定義及執行 BigQuery 和 Cloud Storage 資料表的資料品質檢查，並在 BigQuery 環境中套用定期和持續的資料控制項。
* **[資料歷程](https://docs.cloud.google.com/knowledge-catalog/docs/about-data-lineage?hl=zh-tw)。**追蹤資料在系統中的移動情形，包括來源、傳遞目的地和套用的轉換作業。BigQuery 支援資料表和資料欄層級的資料歷程。

### 彙整和資料監管的後續步驟

下表列出後續步驟，可協助您進一步瞭解資料收錄和資料監管功能：

| 工作經驗 | 學習路徑 |
| --- | --- |
| 新雲端使用者 | * 執行[資料剖析掃描](https://docs.cloud.google.com/bigquery/docs/data-profile-scan?hl=zh-tw)，取得資料洞察資訊，包括資料的限制或平均值。 |
| 經驗豐富的雲端使用者 | * 在 BigQuery 專案中啟用[資料歷程](https://docs.cloud.google.com/knowledge-catalog/docs/about-data-lineage?hl=zh-tw#auto-lineage-bq-support)，即可自動記錄 BigQuery 作業 (例如載入、複製和資料修改) 的歷程資訊。    **注意**：您可以[設定資料歷程擷取](https://docs.cloud.google.com/knowledge-catalog/docs/use-lineage?hl=zh-tw#control-ingestion)，啟用或停用 BigQuery 的自動歷程擷取功能。 * 設定週期性[資料品質掃描](https://docs.cloud.google.com/bigquery/docs/data-quality-scan?hl=zh-tw)，使用[預先定義的掃描規則](https://docs.cloud.google.com/knowledge-catalog/docs/auto-data-quality-overview?hl=zh-tw#predefined-rules)，在可能發生資料問題時發出警示。 * 為資料品質掃描作業設定[自訂資料品質規則](https://docs.cloud.google.com/knowledge-catalog/docs/auto-data-quality-overview?hl=zh-tw#supported-custom-sql-rule-types)，以便根據特定需求調整掃描作業。 |

## 安全性和存取控管

資料存取權管理是指定義、強制執行及監控規則和政策，控管誰能存取資料。存取權管理可確保只有獲得授權的人員才能存取資料。

BigQuery 提供下列安全性和存取控管功能：

* **[Identity and Access Management (IAM)](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)。**IAM 可讓您控管誰能存取 BigQuery 資源，例如專案、資料集、資料表和檢視表。您可以將 IAM 角色授予使用者、群組和服務帳戶。這些角色會定義他們可以對您的資源執行哪些操作。
* **[資料欄層級存取控管](https://docs.cloud.google.com/bigquery/docs/column-level-security-intro?hl=zh-tw)**和**[資料列層級存取控管](https://docs.cloud.google.com/bigquery/docs/row-level-security-intro?hl=zh-tw)**。資料欄和資料列層級的存取控管機制，可讓您根據使用者屬性或資料值，限制資料表中特定資料欄和資料列的存取權。這項控制項可讓您實施精細的存取權，協助保護機密資料，防範未經授權的存取。
* **[資料移轉管理](https://docs.cloud.google.com/bigquery/docs/vpc-sc?hl=zh-tw)。**
  VPC Service Controls 可讓您為 Google Cloud資源建立 perimeter，並根據組織政策控管這些資源的存取權。
* **[稽核記錄](https://docs.cloud.google.com/bigquery/docs/introduction-audit-workloads?hl=zh-tw)。**稽核記錄會詳細記錄貴組織的使用者活動和系統事件。這類記錄有助於強制執行資料治理政策，並找出潛在的安全風險。
* **[資料遮蓋](https://docs.cloud.google.com/bigquery/docs/column-data-masking-intro?hl=zh-tw)。**資料遮罩功能可遮蓋資料表中的機密資料，同時允許授權使用者存取周圍資料。資料遮蓋功能也能遮蓋符合機密資料模式的資料，防止資料不慎外洩。
* **[加密](https://docs.cloud.google.com/bigquery/docs/encryption-at-rest?hl=zh-tw)。**
  BigQuery 會自動加密所有靜態和傳輸中的資料，同時允許您自訂加密設定，以符合特定需求。

### 安全性和存取控管的後續步驟

下表列出後續步驟，您可以採取這些步驟，進一步瞭解存取控管功能：

| 工作經驗 | 學習路徑 |
| --- | --- |
| 新雲端使用者 | * 查看 BigQuery 的[預先定義角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)，並思考如何根據[最小權限原則](https://wikipedia.org/wiki/Principle_of_least_privilege)指派這些角色。 * 瞭解 Google 預設如何加密[靜態](https://docs.cloud.google.com/docs/security/encryption/default-encryption?hl=zh-tw)和[傳輸中](https://docs.cloud.google.com/docs/security/encryption-in-transit?hl=zh-tw)的資料。 |
| 經驗豐富的雲端使用者 | * 如要更靈活、更精細地管理權限，建議您根據需求[建立自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)。 * 新增[資料列](https://docs.cloud.google.com/bigquery/docs/row-level-security-intro?hl=zh-tw)和[資料欄控制項](https://docs.cloud.google.com/bigquery/docs/column-level-security-intro?hl=zh-tw)，協助控管資料表中特定資料列和資料欄的存取權。 * [設定 VPC Service Controls](https://docs.cloud.google.com/vpc-service-controls/docs/set-up-service-perimeter-verify-access?hl=zh-tw)，為 Google Cloud資源建立存取範圍。 * 在資料表中新增[資料欄層級資料遮蓋](https://docs.cloud.google.com/bigquery/docs/column-data-masking?hl=zh-tw)功能，即可在貴機構中分享資訊，而不洩漏機密資料。 * 使用 [Sensitive Data Protection](https://docs.cloud.google.com/sensitive-data-protection/docs/data-profiles?hl=zh-tw) 掃描資料，找出機密和高風險資訊，例如個人識別資訊 (PII)、財務資料和健康資訊。 |

## 共用資料和深入分析

BigQuery 可讓您在組織內外大規模共用資料和洞察資訊。並透過內建的資料交換平台，建立強大的安全性和隱私權架構。透過 [BigQuery 共用](https://docs.cloud.google.com/bigquery/docs/analytics-hub-introduction?hl=zh-tw)功能，您可以探索、存取及使用由多種資料供應商收錄的資料庫。

BigQuery 提供下列共用功能：

* **[不只分享資料](https://docs.cloud.google.com/bigquery/docs/analytics-hub-introduction?hl=zh-tw)。**您可以共用各種資料和 AI 資產，例如 BigQuery 資料集、資料表、檢視表、Pub/Sub 主題的即時串流、SQL 預存程序和 BigQuery ML 模型。
* **[存取 Google 資料集](https://cloud.google.com/datasets?hl=zh-tw)。**運用 Google 搜尋趨勢、DeepMind WeatherNext 模型、Google Maps Platform、Google Earth Engine 等 Google 資料集，強化數據分析和機器學習計畫。
* **[整合資料治理原則](https://docs.cloud.google.com/bigquery/docs/analytics-hub-grant-roles?hl=zh-tw)。**資料擁有者可控管自己的資料，並定義及設定規則或政策，限制存取和使用。
* **[即時、零複製的資料共用](https://docs.cloud.google.com/bigquery/docs/analytics-hub-introduction?hl=zh-tw#architecture)**。資料會就地共用，不需整合、移動或複製，確保分析結果是根據最新資訊。建立的連結資料集會即時指向共用資產。
* **[強化安全防護機制](https://docs.cloud.google.com/bigquery/docs/analytics-hub-vpc-sc-rules?hl=zh-tw)。**您可以使用存取控管機制，減少過度佈建存取權，包括內建的 VPC Service Controls 支援。
* **[透過供應商使用指標提高能見度](https://docs.cloud.google.com/bigquery/docs/analytics-hub-monitor-listings?hl=zh-tw)。**資料發布者可以查看及監控共用資產的使用情形，例如執行的工作數量、掃描的總位元組數，以及各組織的訂閱者。
* **[使用資料無塵室協作處理機密資料](https://docs.cloud.google.com/bigquery/docs/data-clean-rooms?hl=zh-tw)。**資料無塵室提供安全性強化的環境，讓多方不必移動或揭露基礎資料，也能共用、彙整及分析資料資產。
* **[以 BigQuery 為基礎](https://docs.cloud.google.com/bigquery/docs/analytics-hub-introduction?hl=zh-tw)**：您可以運用 BigQuery 的擴充性和強大處理能力，進行大規模協作。

### 分享的後續步驟

下表列出後續步驟，可協助您進一步瞭解共用功能：

| 工作經驗 | 學習路徑 |
| --- | --- |
| 新雲端使用者 | * 瞭解如何建立及管理[交換作業](https://docs.cloud.google.com/bigquery/docs/analytics-hub-manage-exchanges?hl=zh-tw)和[清單](https://docs.cloud.google.com/bigquery/docs/analytics-hub-manage-listings?hl=zh-tw)，開始在組織內外共用資料。 |
| 經驗豐富的雲端使用者 | * 透過 [Pub/Sub 主題](https://docs.cloud.google.com/bigquery/docs/analytics-hub-stream-sharing?hl=zh-tw)分享即時串流資料。 * 透過[資料無塵室](https://docs.cloud.google.com/bigquery/docs/data-clean-rooms?hl=zh-tw)共用及協作處理機密資料。 * 為共用資產設定 [VPC Service Controls](https://docs.cloud.google.com/bigquery/docs/analytics-hub-vpc-sc-rules?hl=zh-tw)，進一步防範資料竊取。 * 在 Google Cloud Marketplace [商業化](https://docs.cloud.google.com/bigquery/docs/analytics-hub-cloud-marketplace?hl=zh-tw)及銷售資產 |

## 後續步驟

* 瞭解 [Google 的驗證機制](https://docs.cloud.google.com/docs/authentication?hl=zh-tw)。
* 瞭解 [Google Cloud的資料刪除](https://docs.cloud.google.com/docs/security/deletion?hl=zh-tw)。
* 進一步瞭解 [IAM 最佳做法](https://docs.cloud.google.com/iam/docs/using-iam-securely?hl=zh-tw)。
* 瞭解 [Google Cloud的資源階層結構](https://docs.cloud.google.com/resource-manager/docs/cloud-platform-resource-hierarchy?hl=zh-tw)。
* 瞭解  [Google Cloud的 IAM](https://docs.cloud.google.com/iam/docs/overview?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-10-29 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-10-29 (世界標準時間)。"],[],[]]