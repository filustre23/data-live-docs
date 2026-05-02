* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [參考資料](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 從 Teradata 遷移至 BigQuery：簡介

本文將說明從 Teradata 遷移至 BigQuery 的原因、比較兩者的功能，並提供 BigQuery 遷移作業的步驟大綱。

## 從 Teradata 遷移至 BigQuery 的理由

Teradata 是管理及分析大量資料的早期創新者。不過，隨著雲端運算需求演進，您可能需要更現代化的資料分析解決方案。

如果您先前使用 Teradata，請考慮遷移至 BigQuery，原因如下：

* 克服舊版平台限制
  + Teradata 的傳統架構通常難以滿足現代分析的需求，特別是針對各種工作負載，需要無限並行和持續高效能的需求。BigQuery 的無伺服器架構旨在以最少的工作量處理這些需求。
* 採用雲端原生策略
  + 許多機構正策略性地從地端部署基礎架構遷移至雲端。因此，您必須捨棄 Teradata 等傳統的硬體綁定解決方案，改用 BigQuery 這類全代管、可擴充的隨選服務，以減少營運管理負擔。
* 整合現代資料來源和數據分析
  + 企業的重要資料越來越多都儲存在雲端來源。BigQuery 原生整合至 Google Cloud 生態系統，可順暢存取這些來源，並執行進階分析、機器學習和即時資料處理作業，不受 Teradata 基礎架構限制。
* 最佳化成本和擴充性
  + Teradata 通常需要複雜且成本高昂的擴充程序。BigQuery 提供儲存空間和運算資源的透明自動調整資源配置，因此您不必手動重新設定，且總持有成本通常會更低，也更容易預估。

## 功能比較

下表比較 Teradata 的功能和概念，以及 BigQuery 的對等功能：

| Teradata 概念 | BigQuery 對等項目 | 說明 |
| --- | --- | --- |
| Teradata (地端部署、雲端、混合式) | BigQuery (整合式 AI 資料平台)。相較於傳統資料倉儲，BigQuery 提供大量額外功能。 | BigQuery 是 Google Cloud上的全代管雲端原生資料倉儲，Teradata 提供地端部署、雲端和混合式選項。BigQuery 是無伺服器服務，可透過 [BQ Omni](https://docs.cloud.google.com/bigquery/docs/omni-introduction?hl=zh-tw) 在所有雲端使用。 |
| Teradata 工具 (Teradata Studio、BTEQ) | Google Cloud 控制台、BigQuery Studio、bq 指令列工具 | 兩者都提供介面，可管理資料倉儲及與之互動。BigQuery Studio 是以網頁為基礎，並與 Google Cloud 整合，可撰寫 SQL、Python 和 Apache Spark。 |
| 資料庫/結構定義 | 資料集 | 在 Teradata 中，資料庫和結構定義用於整理資料表和檢視表，類似於 BigQuery 資料集。不過，管理和使用方式可能有所不同。 |
| 資料表 | 資料表 | 這兩個平台都使用資料表，以資料列和資料欄的形式儲存資料。 |
| 查看 | 查看 | 這兩個平台中的檢視表功能類似，都能根據查詢建立虛擬資料表。 |
| 主鍵 | 主鍵 (GoogleSQL 中未強制執行) | BigQuery 支援 GoogleSQL 中未強制執行的[主鍵](https://docs.cloud.google.com/bigquery/docs/primary-foreign-keys?hl=zh-tw)。這些指標主要用於協助查詢最佳化。 |
| 外鍵 | 外鍵 (在 GoogleSQL 中不會強制執行) | BigQuery 支援 GoogleSQL 中未強制執行的[外部鍵](https://docs.cloud.google.com/bigquery/docs/primary-foreign-keys?hl=zh-tw)。這些指標主要用於協助查詢最佳化。 |
| 索引 | 叢集、搜尋索引、向量索引 (自動或受管理) | Teradata 允許明確建立索引。    建議您[在 BigQuery 中進行分群](https://docs.cloud.google.com/bigquery/docs/clustered-tables?hl=zh-tw)。雖然叢集不等於資料庫索引，但有助於在磁碟上依序儲存資料，因此當分群資料欄做為述詞使用時，有助於最佳化資料擷取作業。  BigQuery 支援[搜尋索引](https://docs.cloud.google.com/bigquery/docs/search-index?hl=zh-tw)和[向量索引](https://docs.cloud.google.com/bigquery/docs/vector-index?hl=zh-tw)。 |
| 分區 | 分區 | 這兩個平台都支援資料表分區，可提高大型資料表的查詢效能。    BigQuery 僅支援按日期和整數分區。如果是字串，請改用叢集。 |
| 資源分配 (視硬體和授權而定) | 預訂 (以容量為準)、以量計價 (以分析為準) | BigQuery 提供彈性的計費模式。預留項目可為使用自動調度資源的持續性及臨時工作負載提供可預測的費用，而以量計價則著重於依查詢掃描的位元組數收費。 |
| BTEQ、SQL Assistant 和其他用戶端工具 | BigQuery Studio、bq 指令列工具、API | BigQuery 提供各種介面來執行查詢，包括網頁式編輯器、指令列工具，以及用於程式輔助存取的 API。 |
| 查詢記錄/記錄 | 查詢記錄、`INFORMATION_SCHEMA.JOBS` | BigQuery 會保留已執行查詢的記錄，方便您查看過去的查詢、分析效能及排解問題。`INFORMATION_SCHEMA.JOBS` 會保留過去 6 個月內提交的所有工作記錄。 |
| 安全防護功能 (存取控管、加密) | 安全防護功能 (IAM、ACL、加密) | 兩者都能提供強大的安全防護。BigQuery 使用 Google Cloud IAM 進行精細的存取權控管。 |
| 網路控制項 (防火牆、VPN) | VPC Service Controls、Private Google Access | BigQuery 會與 VPC Service Controls 整合，限制特定網路對 BigQuery 資源的存取權。您可以使用 Private Google Access 存取 BigQuery，不必使用公開 IP。 |
| 使用者和角色管理 | 身分與存取權管理 (IAM) | BigQuery 使用 IAM 進行精細的存取權控管。您可以在專案、資料集和資料表層級，將特定權限授予使用者和服務帳戶。 |
| 物件的授權和角色 | 資料集和資料表的存取控制清單 (ACL) | 您可以在 BigQuery 中定義資料集和資料表的 ACL，精細控管存取權。 |
| 靜態資料加密和傳輸中資料的加密機制 | 靜態資料加密和傳輸中的資料都會經過加密防護，客戶也能使用客戶自行管理的加密金鑰 (CMEK)，金鑰可託管於外部 EKM 系統。 | BigQuery 預設會加密資料。您也可以管理自己的加密金鑰，進一步控管加密作業。 |
| 資料治理與法規遵循功能 | 資料治理政策、資料遺失防護 (DLP) | BigQuery 支援資料治理政策和 DLP，可協助您強制執行資料安全性及法規遵循要求。 |
| Teradata 載入公用程式 (例如 FastLoad、MultiLoad)、bteq | BigQuery 資料移轉服務、bq 指令列工具、API | BigQuery 提供多種資料載入方法。Teradata 具有專用的載入公用程式。BigQuery 強調資料擷取的擴充性和速度。 |
| Teradata 匯出公用程式 (bteq) | bq 指令列工具、API、匯出至 Cloud Storage | BigQuery 可將資料匯出至各種目的地。Teradata 有自己的匯出工具。BigQuery 與 Cloud Storage 的整合是主要優勢。    BigQuery Storage Read API 可讓任何外部運算功能大量讀取資料。 |
| 外部資料表 | 外部資料表 | 兩者都支援查詢外部儲存空間中的資料。BigQuery 可與 Cloud Storage、Spanner、Bigtable、Cloud SQL、AWS S3、Azure Blob 儲存體和 Google 雲端硬碟完美整合。 |
| 具體化檢視表 | 具體化檢視表 | 兩者都提供具體化檢視表，可提升查詢效能。    BigQuery 提供智慧調整具體化檢視區塊，這些檢視區塊一律會傳回目前的資料，而且即使查詢參照的是基本資料表，也會自動將查詢重新編寫至具體化檢視區塊。 |
| 使用者定義函式 (UDF) | 使用者定義函式 (UDF) (SQL、JavaScript) | BigQuery 支援 SQL 和 JavaScript 中的 UDF。 |
| Teradata 排程器、其他排程工具 | 排程查詢、Managed Service for Apache Airflow、Cloud Functions、BigQuery 管道 | BigQuery 可與 Google Cloud 排程服務和其他外部排程工具整合。 |
| 觀景點 | BigQuery 管理功能，可監控、執行健康狀態檢查、探索工作及管理容量。 | BigQuery 提供以 UI 為基礎的全方位管理工具箱，內含多個窗格，可監控作業健康狀態和資源用量。 |
| 備份與還原 | 資料集複製、時空旅行和安全防護、資料表快照和複製、單一區域與多區域儲存空間、跨區域備份和復原。 | BigQuery 提供快照和時空旅行功能，可復原資料。時間回溯功能可讓您存取特定時間範圍內的歷來資料。BigQuery 也提供資料集複製、單區域和多區域儲存空間，以及跨區域備份和復原選項。 |
| 地理空間函式 | 地理空間函式 | 這兩個平台都支援地理空間資料和函式。 |

## 開始使用

以下各節將摘要說明從 Teradata 遷移至 BigQuery 的程序：

### 執行遷移評估

在從 Teradata 遷移至 BigQuery 的過程中，建議您先執行 [BigQuery 遷移評估工具](https://docs.cloud.google.com/bigquery/docs/migration-assessment?hl=zh-tw)，評估將資料倉儲從 Teradata 遷移至 BigQuery 的可行性和潛在效益。這項工具提供結構化方法，協助您瞭解目前的 Teradata 環境，並預估順利遷移所需的作業量。

執行 BigQuery 遷移評估工具後，會產生評估報告，其中包含下列章節：

* 現有系統報表：現有 Teradata 系統和用量的快照，包括資料庫、結構定義、資料表數量，以及總大小 (以 TB 為單位)。此外，這項工具也會依大小列出結構定義，並指出可能導致資源使用率偏低的因素，例如沒有寫入作業或讀取次數很少的資料表。
* BigQuery 穩定狀態轉換建議：顯示遷移後 BigQuery 的系統樣貌。包括如何最佳化 BigQuery 工作負載，以及避免浪費資源的建議。
* 遷移計畫：提供遷移作業本身的相關資訊。舉例來說，從現有系統遷移至 BigQuery 穩定狀態。這個部分會顯示自動翻譯的查詢數量，以及將每個資料表移至 BigQuery 的預估時間。

如要進一步瞭解遷移評估結果，請參閱「[查看數據分析報表](https://docs.cloud.google.com/bigquery/docs/migration-assessment?hl=zh-tw#review_the_data_studio_report)」。

### 從 Teradata 遷移結構定義和資料

查看遷移評估結果後，您可以[準備 BigQuery 以進行遷移](https://docs.cloud.google.com/bigquery/docs/migration/teradata?hl=zh-tw#before_you_begin)，然後[設定資料移轉作業](https://docs.cloud.google.com/bigquery/docs/migration/teradata?hl=zh-tw#set_up_a_transfer)，開始遷移 Teradata 資料。

如要進一步瞭解 Teradata 遷移程序，請參閱「[從 Teradata 遷移結構定義和資料](https://docs.cloud.google.com/bigquery/docs/migration/teradata?hl=zh-tw)」。

### 驗證遷移作業

將 Teradata 資料遷移至 BigQuery 後，請執行資料驗證工具 (DVT)，對新遷移的 BigQuery 資料執行資料驗證。DVT 會驗證各種函式，從資料表層級到資料列層級，確認遷移的資料是否正常運作。如要進一步瞭解 DVT，請參閱「[企業資料倉儲遷移：認識資料驗證工具](https://cloud.google.com/blog/products/databases/automate-data-validation-with-dvt?hl=zh-tw)」。

您可以在 [DVT 公開 GitHub 存放區](https://github.com/GoogleCloudPlatform/professional-services-data-validator)中存取 DVT。

## 後續步驟

* 試著[測試遷移](https://docs.cloud.google.com/bigquery/docs/migration/teradata-tutorial?hl=zh-tw) Teradata 至 BigQuery。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-02 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-02 (世界標準時間)。"],[],[]]