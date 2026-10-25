Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [參考資料](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 從 Teradata 遷移至 BigQuery：簡介

本文說明從 Teradata 遷移至 BigQuery 的原因、比較 Teradata 和 BigQuery 的功能，並概述開始遷移至 BigQuery 的步驟。

## 從 Teradata 遷移至 BigQuery 的原因

Teradata 是管理及分析大量資料的早期創新者。不過，隨著雲端運算需求演變，您可能需要更現代化的資料分析解決方案。

如果您先前使用過 Teradata，建議您基於下列原因遷移至 BigQuery：

* 克服舊版平台限制
  + Teradata 的傳統架構往往難以滿足現代數據分析的需求，尤其是各種工作負載對無限並行和穩定高效能的需求。BigQuery 的無伺服器架構旨在以最少的心力處理這些需求。
* 採用雲端原生策略
  + 許多組織正有策略地從地端部署基礎架構遷移至雲端。這項轉變需要捨棄 Teradata 等傳統、受硬體限制的解決方案，改用 BigQuery 等全代管、可擴充且隨選的服務，以減少營運負擔。
* 整合現代資料來源和數據分析
  + 企業的重要資料越來越常儲存在雲端來源。BigQuery 與 Google Cloud 生態系統原生整合，可順暢存取這些來源，並提供進階數據分析、機器學習和即時資料處理功能，不受 Teradata 的基礎架構限制。
* 最佳化成本和擴充性
  + Teradata 的擴充程序通常複雜且昂貴。BigQuery 可獨立且自動調整儲存和運算資源，不需手動重新設定，因此總持有成本更可預測，通常也更低。

## 功能比較

下表比較 Teradata 的功能和概念與 BigQuery 的對應功能：

| Teradata 概念 | BigQuery 對等項目 | 說明 |
| --- | --- | --- |
| Teradata (地端部署、雲端、混合式) | BigQuery (整合式 AI 資料平台)。相較於傳統資料倉儲，BigQuery 提供大量額外功能。 | BigQuery 是 Google Cloud上的全代管雲端原生資料倉儲。Teradata 提供地端部署、雲端和混合式選項。BigQuery 是無伺服器服務，並以 [BQ Omni](https://docs.cloud.google.com/bigquery/docs/omni-introduction?hl=zh-tw) 的形式在所有雲端上提供。 |
| Teradata 工具 (Teradata Studio、BTEQ) | Google Cloud 控制台、BigQuery Studio、bq 指令列工具 | 兩者都提供管理及與資料倉儲互動的介面。BigQuery Studio 是網頁式服務，與 Google Cloud 整合，可讓您編寫 SQL、Python 和 Apache Spark。 |
| 資料庫/結構定義 | 資料集 | 在 Teradata 中，資料庫和結構定義用於整理資料表和檢視表，類似於 BigQuery 資料集。不過，管理和使用方式可能有所不同。 |
| 資料表 | 資料表 | 這兩個平台都使用資料表，以列和欄的形式儲存資料。 |
| 查看 | 查看 | 兩者的檢視表功能類似，都能根據查詢建立虛擬資料表。 |
| 主鍵 | 主鍵 (在 GoogleSQL 中未強制執行) | BigQuery 支援 GoogleSQL 中未強制執行的[主鍵](https://docs.cloud.google.com/bigquery/docs/primary-foreign-keys?hl=zh-tw)。這些主要用於協助查詢最佳化。 |
| 外鍵 | 外鍵 (在 GoogleSQL 中不強制執行) | BigQuery 支援 GoogleSQL 中未強制執行的[外鍵](https://docs.cloud.google.com/bigquery/docs/primary-foreign-keys?hl=zh-tw)。這些主要用於協助查詢最佳化。 |
| 索引 | 分群、搜尋索引、向量索引 (自動或代管) | Teradata 允許明確建立索引。    建議您[在 BigQuery 中分群](https://docs.cloud.google.com/bigquery/docs/clustered-tables?hl=zh-tw)。雖然叢集與資料庫索引不同，但可協助將資料依序儲存在磁碟上，並在叢集資料欄做為述詞時，協助最佳化資料擷取作業。   BigQuery 支援[搜尋索引](https://docs.cloud.google.com/bigquery/docs/search-index?hl=zh-tw)和[向量索引](https://docs.cloud.google.com/bigquery/docs/vector-index?hl=zh-tw)。 |
| 分區 | 分區 | 兩者都支援資料表分區，可提升大型資料表的查詢效能。    BigQuery 僅支援依日期和整數進行分區。如果是字串，請改用分群。 |
| 資源分配 (依據硬體和授權) | 預留項目 (以運算資源為基礎)、以量計價 (分析定價) | BigQuery 提供彈性的計價模式。預留項目可為使用自動調度資源的一致和臨時工作負載提供可預測的費用，而隨選定價模式則著重於每次查詢的位元組掃描費用。 |
| BTEQ、SQL Assistant、其他用戶端工具 | BigQuery Studio、bq 指令列工具、API | BigQuery 提供多種執行查詢的介面，包括網頁式編輯器、指令列工具，以及用於程式輔助存取的 API。 |
| 查詢記錄/歷史記錄 | 查詢記錄，`INFORMATION_SCHEMA.JOBS` | BigQuery 會保留已執行查詢的記錄，方便您查看過去的查詢、分析效能及排解問題。`INFORMATION_SCHEMA.JOBS` 會保留過去 6 個月內提交的所有工作記錄。 |
| 安全防護功能 (存取控管、加密) | 安全防護功能 (IAM、ACL、加密) | 兩者都提供強大的安全防護。BigQuery 使用 Google Cloud IAM 進行精細的存取控管。 |
| 網路控制項 (防火牆、VPN) | VPC Service Controls、Private Google Access | BigQuery 與 VPC Service Controls 整合，可限制特定網路存取 BigQuery 資源。有了 Private Google Access，您不必使用公開 IP 就能存取 BigQuery。 |
| 使用者和角色管理 | 身分與存取權管理 (IAM) | BigQuery 使用 IAM 進行精細的存取控管。您可以在專案、資料集和資料表層級，向使用者和服務帳戶授予特定權限。 |
| 物件的授權和角色 | 資料集和資料表的存取控管清單 (ACL) | BigQuery 可讓您定義資料集和資料表的 ACL，精細控管存取權。 |
| 靜態資料加密和傳輸中資料的加密機制 | 靜態資料加密和傳輸中資料加密、客戶自行管理的加密金鑰 (CMEK)，金鑰可託管於外部 EKM 系統。 | BigQuery 預設會加密資料。您也可以自行管理加密金鑰，進一步控管資料。 |
| 資料治理和法規遵循功能 | 資料治理政策、資料遺失防護 (DLP) | BigQuery 支援資料治理政策和資料遺失防護，協助您強制執行資料安全性和法規遵循規定。 |
| Teradata 載入公用程式 (例如 FastLoad、MultiLoad)、bteq | BigQuery 資料移轉服務、bq 指令列工具、API | BigQuery 提供多種資料載入方法。Teradata 具有專門的載入公用程式。BigQuery 著重於資料擷取的擴充性和速度。 |
| Teradata 匯出公用程式、bteq | bq 指令列工具、API、匯出至 Cloud Storage | BigQuery 可將資料匯出至多個目的地。Teradata 有專屬的匯出工具。BigQuery 與 Cloud Storage 整合是一大優勢。    BigQuery Storage Read API 可讓任何外部運算服務大量讀取資料。 |
| 外部資料表 | 外部資料表 | 兩者都支援查詢外部儲存空間中的資料。BigQuery 與 Cloud Storage、Spanner、Bigtable、Cloud SQL、AWS S3、Azure Blob Storage、Google 雲端硬碟完美整合。 |
| materialized view | materialized view | 兩者都提供 materialized view，可提升查詢效能。    BigQuery 提供智慧微調 materialized view，一律會傳回最新資料，即使查詢參照基礎資料表，也會自動將查詢重寫為 materialized view。 |
| User-defined function (UDF) | 使用者定義函式 (UDF) (SQL、JavaScript) | BigQuery 支援 SQL 和 JavaScript UDF。 |
| Teradata 排程器、其他排程工具 | 排定查詢、Managed Service for Apache Airflow、Cloud Functions、BigQuery 管道 | BigQuery 與 Google Cloud 排程服務和其他外部排程工具整合。 |
| 觀景點 | BigQuery 管理功能，可用於監控、健康狀態檢查、探索工作和管理容量。 | BigQuery 提供以 UI 為基礎的全方位管理工具箱，內含多個窗格，可用於監控作業健康狀態和資源使用率。 |
| 備份與還原 | 資料集複製、時間旅行和故障安全、資料表快照和複製、單一區域和多區域儲存空間、跨區域備份和復原。 | BigQuery 提供快照和時光旅行功能，可用於復原資料。時間旅行功能可讓您存取特定時間範圍內的歷來資料。BigQuery 也提供資料集複製、區域和多區域儲存空間，以及跨區域備份和復原選項。 |
| 地理空間函式 | 地理空間函式 | 這兩個平台都支援地理空間資料和函式。 |

## 開始使用

下列各節會概略說明從 Teradata 遷移至 BigQuery 的程序：

### 執行遷移評估

從 Teradata 遷移至 BigQuery 時，建議您先執行 [BigQuery 遷移評估工具](https://docs.cloud.google.com/bigquery/docs/migration-assessment?hl=zh-tw)，評估將資料倉儲從 Teradata 遷移至 BigQuery 的可行性和潛在效益。這項工具提供結構化方法，可協助您瞭解目前的 Teradata 環境，並預估順利遷移所需的工作。

執行 BigQuery 遷移評估工具後，會產生評估報告，其中包含下列部分：

* 現有系統報表：現有 Teradata 系統和用量的數據匯報，包括資料庫、結構定義、資料表的數量，以及總大小 (以 TB 為單位)。此外，這項工具也會依大小列出結構定義，並指出可能未充分利用資源的情況，例如沒有寫入作業或讀取作業很少的資料表。
* BigQuery 穩定狀態轉換建議：顯示遷移後系統在 BigQuery 的樣貌。其中包含最佳化 BigQuery 工作負載和避免浪費的建議。
* 遷移計畫：提供遷移作業本身的相關資訊。例如從現有系統轉換至 BigQuery 穩定狀態。這個部分包含自動翻譯的查詢數量，以及將各個資料表移至 BigQuery 的預計時間。

如要進一步瞭解遷移評估結果，請參閱「[查看數據分析報表](https://docs.cloud.google.com/bigquery/docs/migration-assessment?hl=zh-tw#review_the_data_studio_report)」。

### 從 Teradata 遷移結構定義和資料

查看遷移評估結果後，您可以[為 BigQuery 做好遷移準備](https://docs.cloud.google.com/bigquery/docs/migration/teradata?hl=zh-tw#before_you_begin)，然後[設定資料移轉工作](https://docs.cloud.google.com/bigquery/docs/migration/teradata?hl=zh-tw#set_up_a_transfer)，開始遷移 Teradata。

如要進一步瞭解 Teradata 遷移程序，請參閱「[從 Teradata 遷移結構定義和資料](https://docs.cloud.google.com/bigquery/docs/migration/teradata?hl=zh-tw)」。

### 驗證遷移作業

將 Teradata 資料遷移至 BigQuery 後，請執行 Data Validation Tool (DVT)，對新遷移的 BigQuery 資料執行資料驗證。DVT 會驗證從資料表層級到資料列層級的各種函式，確認遷移的資料能正常運作。如要進一步瞭解 DVT，請參閱「[企業資料倉儲遷移：認識資料驗證工具](https://cloud.google.com/blog/products/databases/automate-data-validation-with-dvt?hl=zh-tw)」。

您可以前往 [DVT 公開 GitHub 存放區](https://github.com/GoogleCloudPlatform/professional-services-data-validator)存取 DVT。

## 後續步驟

* 嘗試[測試遷移](https://docs.cloud.google.com/bigquery/docs/migration/teradata-tutorial?hl=zh-tw)，將 Teradata 遷移至 BigQuery。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-10-24 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-10-24 (世界標準時間)。"],[],[]]