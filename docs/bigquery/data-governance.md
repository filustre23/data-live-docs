Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# BigQuery 資料治理簡介

BigQuery 內建管理功能，可簡化資料和 AI 資產的探索、管理、監控、控管及使用方式。

管理員、資料管理員、資料治理經理和資料管理員可以使用 BigQuery 的治理功能執行下列操作：

* 探索資料。
* 彙整資料。
* 收集及豐富中繼資料。
* 管理資料品質。
* 確保資料使用方式符合組織政策。
* 大規模安全地共用資料。

BigQuery 治理功能採用[Knowledge Catalog](https://docs.cloud.google.com/dataplex/docs/catalog-overview?hl=zh-tw)技術，可集中管理貴機構的所有資料資產。Knowledge Catalog 包含所有資料的業務、技術和作業中繼資料。這項服務會運用人工智慧和機器學習技術，協助您發掘中繼資料中的關係和語意。

Lakehouse 執行階段目錄可讓您使用多個資料處理引擎，透過單一結構定義查詢單一資料副本，不必重複資料。可用的資料處理引擎包括 BigQuery、Apache Spark、Apache Flink 和 Apache Hive。資料可儲存在 BigQuery 儲存空間資料表、Apache Iceberg 管理的資料表，或 BigLake 外部資料表等位置。

BigQuery 支援端對端資料生命週期，從資料探索到資料使用皆可支援。Knowledge Catalog 也提供控管功能。

## 資料探索

BigQuery 會在整個機構中探索資料 Google Cloud，無論資料位於 BigQuery、Spanner、Cloud SQL、Pub/Sub 或 Cloud Storage，系統會自動擷取中繼資料，並儲存在 Knowledge Catalog 中。舉例來說，您可以從 Cloud Storage 擷取結構化和非結構化資料的中繼資料，並自動大規模建立可供查詢的 BigLake 資料表。這樣您就能使用開放原始碼引擎執行分析，而不必複製資料。

您也可以使用自訂連接器，從第三方資料來源擷取及分類中繼資料。

BigQuery 提供下列資料探索功能：

* **搜尋**。搜尋專案和機構中的資料和 AI 資源。在 Google Cloud 控制台的 BigQuery 中，使用[語意搜尋](https://docs.cloud.google.com/bigquery/docs/search-resources?hl=zh-tw) ([預覽版](https://cloud.google.com/products?hl=zh-tw#product-launch-stages)) 以日常用語搜尋資源。或者，在 Knowledge Catalog 中使用[關鍵字搜尋](https://docs.cloud.google.com/dataplex/docs/search-assets?hl=zh-tw)功能尋找資源。
* **[自動探索 Cloud Storage 資料](https://docs.cloud.google.com/bigquery/docs/automatic-discovery?hl=zh-tw)。**掃描 Cloud Storage bucket 中的資料，擷取中繼資料並編製目錄。自動探索功能會為結構化和非結構化資料建立資料表。
* **[中繼資料匯入](https://docs.cloud.google.com/dataplex/docs/managed-connectivity-overview?hl=zh-tw)：**從第三方系統大規模匯入中繼資料至 Knowledge Catalog。您可以建立自訂連接器，從資料來源擷取資料，然後執行受管理連線管道，協調中繼資料匯入工作流程。
* **[中繼資料匯出](https://docs.cloud.google.com/dataplex/docs/export-metadata?hl=zh-tw)。**從 Knowledge Catalog 大量匯出中繼資料。您可以透過 BigQuery 分析匯出的中繼資料，或將中繼資料整合至自訂應用程式或程式輔助處理工作流程。

## 收錄和資料監管

為提升資料的探索和可用性，資料管理員和管理員可以使用 BigQuery 檢閱、更新及分析中繼資料。BigQuery 資料管理和管理功能可協助您確保資料準確無誤、一致性，並符合貴機構的政策。

BigQuery 提供下列資料管理和控管功能：

* **[組織詞彙](https://docs.cloud.google.com/dataplex/docs/create-glossary?hl=zh-tw)：**在詞彙表中定義貴機構的術語，提升背景資訊、協作和搜尋效果。找出字詞的資料監管員，並將字詞附加到資料資產欄位。
* **[資料洞察](https://docs.cloud.google.com/bigquery/docs/data-insights?hl=zh-tw)。**
  Gemini 會使用中繼資料生成有關資料表的自然語言問題，以及回答這些問題的 SQL 查詢。這些資料洞察資訊有助於發掘模式、評估資料品質，以及執行統計分析。
* **[資料剖析](https://docs.cloud.google.com/bigquery/docs/data-profile-scan?hl=zh-tw)。**找出 BigQuery 資料表中資料欄的常見統計特徵，更有效地解讀及分析資料。
* **[資料品質](https://docs.cloud.google.com/bigquery/docs/data-quality-scan?hl=zh-tw)：**定義及執行 BigQuery 和 Cloud Storage 中資料表的資料品質檢查，並在 BigQuery 環境中套用定期和持續的資料控管措施。
* **[資料歷程](https://docs.cloud.google.com/dataplex/docs/about-data-lineage?hl=zh-tw)。**追蹤資料在系統中的移動情形，包括來源、傳遞目的地和套用的轉換作業。BigQuery 支援資料表和資料欄層級的資料歷程。

### 彙整和資料監管後續步驟

下表列出後續步驟，可協助您進一步瞭解策展和資料監管功能：

| 工作經驗 | 學習路徑 |
| --- | --- |
| 新雲端使用者 | * 執行[資料剖析掃描](https://docs.cloud.google.com/bigquery/docs/data-profile-scan?hl=zh-tw)，深入瞭解資料，包括資料的限制或平均值。 |
| 經驗豐富的雲端使用者 | * 在 BigQuery 專案中啟用[資料沿襲](https://docs.cloud.google.com/dataplex/docs/about-data-lineage?hl=zh-tw#auto-lineage-bq-support)，即可自動記錄 BigQuery 作業 (例如載入、複製和資料修改) 的沿襲資訊。 * 設定定期[資料品質掃描](https://docs.cloud.google.com/bigquery/docs/data-quality-scan?hl=zh-tw)，使用[預先定義的掃描規則](https://docs.cloud.google.com/dataplex/docs/auto-data-quality-overview?hl=zh-tw#predefined-rules)，在發生可能的資料問題時收到快訊。 * 為資料品質掃描作業設定[自訂資料品質規則](https://docs.cloud.google.com/dataplex/docs/auto-data-quality-overview?hl=zh-tw#supported-custom-sql-rule-types)，讓掃描作業符合特定需求。 |

## 安全性和存取控管

資料存取權管理是指定義、強制執行及監控資料存取規則和政策的程序，可控管資料存取權。存取權管理可確保只有獲得授權的使用者才能存取資料。

BigQuery 提供下列安全性和存取權控管功能：

* **[身分與存取權管理 (IAM)](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)。**透過 IAM，您可以控管哪些人有權存取 BigQuery 資源，例如專案、資料集、資料表和檢視區塊。您可以將 IAM 角色授予使用者、群組和服務帳戶。這些角色會定義使用者可對資源執行的操作。
* **[資料欄層級存取權控管](https://docs.cloud.google.com/bigquery/docs/column-level-security-intro?hl=zh-tw)**和**[資料列層級存取權控管](https://docs.cloud.google.com/bigquery/docs/row-level-security-intro?hl=zh-tw)。**透過資料欄和資料列層級的存取權控管機制，您可以根據使用者屬性或資料值，限制特定資料欄和資料列的存取權。這項控管機制可讓您實施精細的存取權，協助保護私密資料免於未經授權的存取。
* **[資料移轉管理](https://docs.cloud.google.com/bigquery/docs/vpc-sc?hl=zh-tw)**。
  VPC Service Controls 可讓您在資源周圍建立 perimeter，並根據貴機構的政策控管這些資源的存取權。 Google Cloud
* **[稽核記錄](https://docs.cloud.google.com/bigquery/docs/introduction-audit-workloads?hl=zh-tw)：**稽核記錄會詳細記錄貴機構中的使用者活動和系統事件。這些記錄檔有助於落實資料治理政策，並找出潛在的安全風險。
* **[資料遮蓋](https://docs.cloud.google.com/bigquery/docs/column-data-masking-intro?hl=zh-tw)。**資料遮蓋功能可讓您遮蓋資料表中的機密資料，但仍允許授權使用者存取周圍的資料。資料遮蓋功能也能遮蓋符合機密資料模式的資料，避免資料意外揭露。
* **[加密](https://docs.cloud.google.com/bigquery/docs/encryption-at-rest?hl=zh-tw)。**
  BigQuery 會自動加密所有待用和傳輸中的資料，同時讓您自訂加密設定，以符合特定需求。

### 安全性和存取控管的後續步驟

下表列出後續步驟，協助您進一步瞭解存取控管功能：

| 工作經驗 | 學習路徑 |
| --- | --- |
| 新雲端使用者 | * 請參閱 BigQuery 中的[預先定義角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)，並根據[最小權限原則](https://wikipedia.org/wiki/Principle_of_least_privilege)，考慮如何指派這些角色。 * 瞭解 Google 如何預設加密[靜態資料](https://docs.cloud.google.com/docs/security/encryption/default-encryption?hl=zh-tw)和[傳輸中的資料](https://docs.cloud.google.com/docs/security/encryption-in-transit?hl=zh-tw)。 |
| 經驗豐富的雲端使用者 | * 如要更靈活且精細地管理權限，建議[建立符合需求的自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)。 * 新增[列](https://docs.cloud.google.com/bigquery/docs/row-level-security-intro?hl=zh-tw)和[欄控制項](https://docs.cloud.google.com/bigquery/docs/column-level-security-intro?hl=zh-tw)，控管表格中特定列和欄的存取權。 * 透過 Google Cloud[設定 VPC Service Controls](https://docs.cloud.google.com/vpc-service-controls/docs/set-up-service-perimeter-verify-access?hl=zh-tw)，為資源建立存取範圍。 * 在表格中新增[資料欄層級的資料遮蓋](https://docs.cloud.google.com/bigquery/docs/column-data-masking?hl=zh-tw)，透過貴機構分享資訊，同時隱藏機密資料。 * 使用 [Sensitive Data Protection](https://docs.cloud.google.com/sensitive-data-protection/docs/data-profiles?hl=zh-tw) 掃描資料，找出機密和高風險資訊，例如個人識別資訊 (PII)、財務資料和健康資訊。 |

## 共用資料和洞察

BigQuery 可讓您在機構內和跨機構大規模共用資料和洞察資訊。內建資料交換平台，提供強大的安全和隱私權架構。透過 [BigQuery sharing](https://docs.cloud.google.com/bigquery/docs/analytics-hub-introduction?hl=zh-tw)，您可以探索、存取及使用由各種資料供應商提供的資料庫。

BigQuery 提供下列共用功能：

* **[分享的不只是資料](https://docs.cloud.google.com/bigquery/docs/analytics-hub-introduction?hl=zh-tw)：**您可以共用各種資料和 AI 資產，例如 BigQuery 資料集、資料表、檢視區塊、透過 Pub/Sub 主題傳送的即時串流、SQL 預存程序，以及 BigQuery ML 模型。
* **[存取 Google 資料集](https://cloud.google.com/datasets?hl=zh-tw)。**運用 Google 搜尋趨勢、DeepMind WeatherNext 模型、Google 地圖平台、Google Earth Engine 等 Google 資料集，提升您的數據分析和機器學習成效。
* **[整合資料治理原則](https://docs.cloud.google.com/bigquery/docs/analytics-hub-grant-roles?hl=zh-tw)。**資料擁有者可保留資料控制權，並定義及設定規則或政策，限制存取和使用權。
* **[即時分享資料，無需複製](https://docs.cloud.google.com/bigquery/docs/analytics-hub-introduction?hl=zh-tw#linked_resources)。**資料會直接共用，不需整合、移動或複製資料，確保分析結果是以最新資訊為依據。建立的連結資料集是共用資產的即時指標。
* **[提升安全防護機制](https://docs.cloud.google.com/bigquery/docs/analytics-hub-vpc-sc-rules?hl=zh-tw)**。您可以透過存取權控管機制減少過度佈建的存取權，包括內建的 VPC Service Controls 支援。
* **[透過供應商用量指標提高曝光率](https://docs.cloud.google.com/bigquery/docs/analytics-hub-monitor-listings?hl=zh-tw)。**資料發布者可以查看及監控共用資產的使用情形，例如執行的工作數、掃描的總位元組數，以及每個機構的訂閱者。
* **[透過資料無塵室協作處理機密資料](https://docs.cloud.google.com/bigquery/docs/data-clean-rooms?hl=zh-tw)。**資料無塵室提供安全強化環境，讓多方不必移動或揭露基礎資料，也能共用、彙整及分析資料資產。
* **[以 BigQuery 為基礎](https://docs.cloud.google.com/bigquery/docs/analytics-hub-introduction?hl=zh-tw)。**您可以運用 BigQuery 的擴充性和大規模處理功能，進行大規模協作。

### 分享的後續步驟

下表列出後續步驟，可協助您進一步瞭解分享功能：

| 工作經驗 | 學習路徑 |
| --- | --- |
| 新雲端使用者 | * 瞭解如何建立及管理[交易所](https://docs.cloud.google.com/bigquery/docs/analytics-hub-manage-exchanges?hl=zh-tw)和[房源](https://docs.cloud.google.com/bigquery/docs/analytics-hub-manage-listings?hl=zh-tw)，開始在機構內外分享。 |
| 經驗豐富的雲端使用者 | * 透過 [Pub/Sub 主題](https://docs.cloud.google.com/bigquery/docs/analytics-hub-stream-sharing?hl=zh-tw)分享即時串流資料。 * 透過[資料無塵室](https://docs.cloud.google.com/bigquery/docs/data-clean-rooms?hl=zh-tw)共用及協作處理機密資料。 * 如要進一步防範資料竊取，請在共用資產周圍設定 [VPC Service Controls](https://docs.cloud.google.com/bigquery/docs/analytics-hub-vpc-sc-rules?hl=zh-tw)。 * [在 Google Cloud Marketplace 中銷售資產](https://docs.cloud.google.com/bigquery/docs/analytics-hub-cloud-marketplace?hl=zh-tw) |

## 後續步驟

* 瞭解 Google 的[驗證機制](https://docs.cloud.google.com/docs/authentication?hl=zh-tw)。
* 瞭解[如何刪除 Google Cloud的資料](https://docs.cloud.google.com/docs/security/deletion?hl=zh-tw)。
* 進一步瞭解 [IAM 最佳做法](https://docs.cloud.google.com/iam/docs/using-iam-securely?hl=zh-tw)。
* 瞭解  [Google Cloud](https://docs.cloud.google.com/resource-manager/docs/cloud-platform-resource-hierarchy?hl=zh-tw) 的資源階層。
* 瞭解  [Google Cloud](https://docs.cloud.google.com/iam/docs/overview?hl=zh-tw) 上的 IAM。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-06 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-06 (世界標準時間)。"],[],[]]