Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [參考資料](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 從 Oracle 遷移至 BigQuery

本文件提供從 Oracle 遷移至 BigQuery 的概略指南。說明基本的架構差異，並建議如何從在 Oracle RDBMS (包括 Exadata) 上執行的資料倉儲和資料市集遷移至 BigQuery。本文提供的詳細資料也適用於 Exadata、ExaCC 和 Oracle Autonomous Data Warehouse，因為這些服務使用相容的 Oracle 軟體。

本文適用於企業架構師、資料庫管理員、應用程式開發人員和 IT 資安專業人員，協助他們從 Oracle 遷移至 BigQuery，並解決遷移過程中的技術難題。

您也可以使用[批次 SQL 翻譯](https://docs.cloud.google.com/bigquery/docs/batch-sql-translator?hl=zh-tw)大量遷移 SQL 指令碼，或使用[互動式 SQL 翻譯](https://docs.cloud.google.com/bigquery/docs/interactive-sql-translator?hl=zh-tw)翻譯臨時查詢。這兩項工具都支援 Oracle SQL、PL/SQL 和 Exadata ([預先發布版](https://cloud.google.com/products?hl=zh-tw#product-launch-stages))。

## 遷移前

為確保資料倉儲遷移作業順利完成，請在專案時間軸初期開始規劃遷移策略。如要瞭解如何有系統地規劃遷移工作，請參閱「[遷移內容和方式：遷移架構](https://docs.cloud.google.com/bigquery/docs/migration/migration-overview?hl=zh-tw#what_and_how_to_migrate_the_migration_framework)」。

### BigQuery 運算資源規劃

在幕後，BigQuery 的數據分析處理量是以運算單元為單位。BigQuery 運算單元是 Google 專屬的運算能力單位，用於執行 SQL 查詢。

BigQuery 會在查詢執行時持續計算查詢所需的運算單元數量，但會根據[公平排程器](https://docs.cloud.google.com/bigquery/docs/slots?hl=zh-tw#fair_scheduling_in_bigquery)將運算單元分配給查詢。

規劃 BigQuery 運算單元容量時，您可以選擇下列計價模式：

* [隨選定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#on_demand_pricing)：在隨選定價模式中，BigQuery 會按照實際處理的位元組數 (資料大小) 收取費用，因此您只需為執行的查詢付費。如要進一步瞭解 BigQuery 如何判斷資料大小，請參閱「[資料大小計算](https://cloud.google.com/bigquery/pricing?hl=zh-tw#data)」。由於運算單元決定了基礎運算能力，您可以根據所需的運算單元數量 (而非處理的位元組數) 支付 BigQuery 使用費用。根據預設， Google Cloud 專案最多只能有 2,000 個運算單元。
* [以運算資源為基礎的定價模式](https://cloud.google.com/bigquery/pricing?hl=zh-tw#capacity_compute_analysis_pricing)：採用以運算資源為基礎的定價模式時，您需要購買 BigQuery 運算單元[預留項目](https://docs.cloud.google.com/bigquery/docs/reservations-intro?hl=zh-tw) (至少 100 個)，而非依據查詢處理的位元組數付費。對於企業資料倉儲工作負載，我們建議採用依運算資源計價的模式，因為這類工作負載通常會有多個並行報表和擷取、載入、轉換 (ELT) 查詢，且用量可預測。

為協助您估算運算單元，建議您[使用 Cloud Monitoring 設定 BigQuery 監控功能](https://docs.cloud.google.com/bigquery/docs/monitoring?hl=zh-tw)，並[使用 BigQuery 分析稽核記錄](https://docs.cloud.google.com/bigquery/audit-logs?hl=zh-tw)。許多客戶會使用[數據分析](https://datastudio.google.com/?hl=zh-tw) (例如，請參閱[數據分析資訊主頁](https://datastudio.google.com/c/u/0/reporting/1kwNFt05J8_GCju5TBH1v4IlBmmAU74Nu/page/nSaN?hl=zh-tw)的[開放原始碼範例](https://github.com/GoogleCloudPlatform/professional-services/tree/master/examples/bigquery-audit-log))、[Looker](https://looker.com/) 或 [Tableau](https://www.tableau.com/) 做為前端，以視覺化方式呈現 BigQuery 稽核記錄資料，特別是各項查詢和專案的運算單元用量。您也可以運用 BigQuery 系統資料表資料，監控各項工作和預留項目的運算單元使用率。如需範例，請參閱 [數據分析 資訊主頁](https://datastudio.google.com/s/kGZzZJWkeyA?hl=zh-tw)的[開放原始碼範例](https://github.com/GoogleCloudPlatform/bigquery-utils/tree/master/dashboards/system_tables)。

定期監控及分析運算單元使用率，有助於預估貴組織在 Google Cloud成長時所需的運算單元總數。

舉例來說，假設您一開始預留 [4,000 個 BigQuery 運算單元](https://docs.cloud.google.com/bigquery/docs/slots?hl=zh-tw)，同時執行 100 項中等複雜度的查詢。如果發現查詢執行計畫的等待時間過長，且資訊主頁顯示運算單元使用率偏高，可能代表需要更多 BigQuery 運算單元來支援工作負載。如要透過一年或三年承諾使用合約自行購買運算單元，可以使用 Google Cloud 控制台或 bq 指令列工具[開始使用 BigQuery 預留項目](https://docs.cloud.google.com/bigquery/docs/reservations-get-started?hl=zh-tw)。

如果對目前的方案和上述選項有任何疑問，請與[業務代表](https://cloud.google.com/contact?hl=zh-tw)聯絡。

### Google Cloud的安全性

以下各節將說明常見的 Oracle 安全控管機制，以及如何確保資料倉儲在 Google Cloud環境中受到保護。

#### 身分與存取權管理 (IAM)

Oracle 提供[使用者、權限、角色和設定檔](https://docs.oracle.com/cd/B19306_01/network.102/b14266/admusers.htm#DBSEG10000)，用於管理資源存取權。

BigQuery 使用 [IAM](https://docs.cloud.google.com/iam?hl=zh-tw) 管理資源存取權，並提供資源和動作的集中式[存取權管理](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)。BigQuery 提供的資源類型包括組織、專案、資料集、資料表和檢視表。在 IAM 政策階層中，資料集是專案的子資源。資料表會繼承所屬資料集的權限。

如要授予資源存取權，請將一或多個角色指派給使用者、群組或服務帳戶。組織和專案角色會影響執行工作或管理專案的能力，而資料集角色則會影響存取或修改專案內資料的能力。

IAM 提供下列類型的角色：

* [預先定義的角色](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)旨在支援常見用途和存取控管模式。預先定義的角色由 Google Cloud管理，可提供特定服務的精細存取權。
* [基本角色](https://docs.cloud.google.com/bigquery/docs/access-control-basic-roles?hl=zh-tw)包括擁有者、編輯者和檢視者角色。

  **注意：** BigQuery 的資料集層級基本角色在 IAM 推出前就已存在。建議您盡量減少使用基本角色。在正式環境中，除非沒有其他替代方案，否則請勿授予基本角色，請改用[預先定義的 IAM](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw) 角色。
* [自訂角色](https://docs.cloud.google.com/iam/docs/understanding-custom-roles?hl=zh-tw)：根據使用者指定的權限清單，提供精細的存取權限。

如果同時為使用者指派預先定義角色和基本角色，則授予的權限會是各個角色權限的聯集。

#### 資料列層級安全性

[Oracle Label Security (OLS)](https://docs.oracle.com/database/121/TDPSG/GUID-72D524FF-5A86-495A-9D12-14CB13819D42.htm#TDPSG94446) 可限制逐列存取資料。資料列層級安全性的典型用途，是限制銷售人員只能存取自己管理的帳戶。實作資料列層級安全性，即可精細控管存取權。

如要在 BigQuery 中實現資料列層級安全性，您可以使用[授權檢視表](https://docs.cloud.google.com/bigquery/docs/authorized-views?hl=zh-tw)和[資料列層級存取權政策](https://docs.cloud.google.com/bigquery/docs/managing-row-level-security?hl=zh-tw)。如要進一步瞭解如何設計及實施這些政策，請參閱「[BigQuery 資料列層級安全防護機制簡介](https://docs.cloud.google.com/bigquery/docs/row-level-security-intro?hl=zh-tw)」。

#### 全磁碟加密

Oracle 提供[透明資料加密 (TDE)](https://docs.oracle.com/cd/E11882_01/network.112/e40393/asotrans.htm#ASOAG600) 和[網路加密](https://docs.oracle.com/database/121/DBSEG/asoconfg.htm#DBSEG020)，用於加密靜態和傳輸中的資料。TDE 需要 Advanced Security 選項，該選項需另外授權。

無論來源或其他條件為何，BigQuery 預設會加密所有[靜態](https://docs.cloud.google.com/docs/security/encryption/default-encryption?hl=zh-tw)和[傳輸中](https://docs.cloud.google.com/docs/security/encryption-in-transit?hl=zh-tw)的資料，且無法關閉這項功能。BigQuery 也支援[客戶自行管理的加密金鑰](https://docs.cloud.google.com/bigquery/docs/customer-managed-encryption?hl=zh-tw) (CMEK)，方便使用者在 [Cloud Key Management Service](https://docs.cloud.google.com/kms/docs?hl=zh-tw) 中控管及管理金鑰加密金鑰。如要進一步瞭解 Google Cloud的加密功能，請參閱「[預設靜態資料加密](https://docs.cloud.google.com/docs/security/encryption/default-encryption?hl=zh-tw)」和「[傳輸中資料加密](https://docs.cloud.google.com/docs/security/encryption-in-transit?hl=zh-tw)」。

#### 資料遮蓋和遮蓋

Oracle 在 Real Application Testing 中使用[資料遮蓋](https://docs.oracle.com/cd/E11882_01/server.112/e41481/tdm_data_masking.htm#RATUG04000)和[資料遮蓋](https://docs.oracle.com/cd/E11882_01/network.112/e40393/redaction.htm#ASOAG594)，可讓您遮蓋 (遮蓋) 應用程式發出的查詢傳回的資料。

BigQuery 支援資料欄層級的[動態資料遮蓋](https://docs.cloud.google.com/bigquery/docs/column-data-masking-intro?hl=zh-tw)功能。您能針對不同使用者群組，選擇性地遮蓋特定資料欄的資料，但這些使用者還是能正常使用該資料欄。

您可以使用 [Sensitive Data Protection](https://docs.cloud.google.com/sensitive-data-protection/docs?hl=zh-tw)，在 BigQuery 中識別及遮蓋具敏感性的個人識別資訊 (PII)。

### BigQuery 與 Oracle 比較

本節說明 BigQuery 和 Oracle 之間的主要差異。這些重點可協助您找出遷移障礙，並規劃必要的變更。

#### 系統架構

Oracle 和 BigQuery 的主要差異之一，在於 BigQuery 是無伺服器雲端 EDW，具有獨立的儲存和運算層，可根據查詢需求擴充。BigQuery 採用無伺服器架構，因此您不必受限於硬體決策，而是可以透過預留項目，為查詢和使用者要求更多資源。BigQuery 也不需要設定基礎軟體和基礎架構，例如作業系統 (OS)、網路系統和儲存系統，包括資源調度及高可用性。BigQuery 會處理擴充、管理和管理作業。下圖說明 BigQuery 儲存空間階層。

瞭解基礎儲存空間和查詢處理架構，例如儲存空間 (Colossus) 與查詢執行 (Dremel) 之間的分隔，以及Google Cloud 如何分配資源 (Borg)，有助於瞭解行為差異，並最佳化查詢效能和成本效益。詳情請參閱 [BigQuery](https://cloud.google.com/blog/products/data-analytics/new-blog-series-bigquery-explained-overview?hl=zh-tw)、[Oracle](https://www.oracle.com/webfolder/technetwork/tutorials/architecture-diagrams/18/technical-architecture/database-technical-architecture.html) 和 [Exadata](https://www.oracle.com/technetwork/database/exadata/exadata-x7-2-ds-3908482.pdf) 的參考系統架構。

#### 資料和儲存空間架構

資料和儲存空間結構是所有資料分析系統的重要部分，因為這會影響查詢效能、成本、擴充性和效率。

BigQuery 會[將資料儲存和運算作業分開](https://cloud.google.com/blog/products/gcp/separation-of-storage-and-compute-in-bigquery?hl=zh-tw)，並將資料儲存在 Colossus 中，資料會經過壓縮，並以名為 [Capacitor](https://cloud.google.com/blog/products/gcp/inside-capacitor-bigquerys-next-generation-columnar-storage-format?hl=zh-tw) 的欄式格式儲存。

BigQuery 使用 Capacitor，直接對壓縮資料執行作業，不需解壓縮。如上圖所示，BigQuery 提供[資料集](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/datasets?hl=zh-tw)做為最高層級的抽象層，用於管理資料表的存取權。[結構定義](https://docs.cloud.google.com/bigquery/docs/schemas?hl=zh-tw)和[標籤](https://docs.cloud.google.com/bigquery/docs/adding-using-labels?hl=zh-tw)可用於進一步整理資料表。BigQuery 提供[分區](https://docs.cloud.google.com/bigquery/docs/partitioned-tables?hl=zh-tw)功能，可提升查詢效能、降低成本，並管理資訊生命週期。儲存空間資源會在使用當下分配，並在您移除資料或捨棄資料表時取消分配。

Oracle 會使用 [Oracle 區塊格式](https://docs.oracle.com/cd/B28359_01/server.111/b28318/logical.htm#CNCPT004)，以資料列格式儲存資料，並以區段形式整理。結構定義 (由使用者擁有) 用於整理資料表和其他資料庫物件。自 Oracle 12c 起，[多租戶](https://www.oracle.com/technetwork/database/multitenant/learn-more/multitenantwp18c-4396158.pdf)架構可用於在一個資料庫執行個體中建立可插式資料庫，進一步隔離資料。[分區](https://www.oracle.com/technetwork/database/options/partitioning/partitioning-wp-12c-1896137.pdf)可用於提升查詢效能和資訊生命週期作業。Oracle 為獨立和 [Real Application Clusters (RAC)](https://www.oracle.com/technetwork/database/options/clustering/rac-twp-overview-5303704.pdf) 資料庫提供多種[儲存選項](https://docs.oracle.com/database/121/CNCPT/physical.htm#CNCPT88986)，例如 ASM、OS 檔案系統和叢集檔案系統。

Exadata 在儲存體單元伺服器中提供最佳化的儲存體基礎架構，並允許 Oracle 伺服器利用 [ASM](https://docs.oracle.com/cd/E11882_01/server.112/e18951/asmcon.htm#OSTMG036) 以透明的方式存取這項資料。Exadata 提供[混合分欄壓縮 (HCC)](https://www.oracle.com/technetwork/database/exadata/ehcc-twp-131254.pdf) 選項，讓使用者壓縮資料表和分區。

Oracle 需要預先佈建儲存空間容量、仔細調整大小，以及在區段、資料檔案和資料表空間上設定自動遞增。

#### 查詢執行和效能

BigQuery 會在查詢層級管理效能和資源調度，盡可能提高成本效益。BigQuery 採用多種最佳化技術，例如：

* [在記憶體中執行查詢](https://cloud.google.com/blog/products/gcp/in-memory-query-execution-in-google-bigquery?hl=zh-tw)
* 以 [Dremel](http://static.googleusercontent.com/media/research.google.com/en//pubs/archive/36632.pdf) 執行引擎為基礎的多層級樹狀架構
* Capacitor 內建自動儲存空間最佳化功能
* [Jupiter](https://cloudplatform.googleblog.com/2015/06/A-Look-Inside-Googles-Data-Center-Networks.html) 的每秒總對分頻寬為 1 PB
* [自動調度資源管理](https://cloud.google.com/blog/products/gcp/understanding-bigquerys-rapid-scaling-and-simple-pricing?hl=zh-tw)，提供快速的 PB 規模查詢

BigQuery 會在載入資料時收集資料欄統計資料，並提供診斷[查詢計畫](https://docs.cloud.google.com/bigquery/query-plan-explanation?hl=zh-tw)和[時間](https://docs.cloud.google.com/bigquery/query-plan-explanation?hl=zh-tw)資訊。查詢資源會根據查詢類型及複雜度分配。每筆查詢都會使用一些[運算單元](https://docs.cloud.google.com/bigquery/docs/slots?hl=zh-tw)，這些運算單元是由一定數量的 CPU 與 RAM 組成。

Oracle 提供資料[統計資料](https://docs.oracle.com/cd/B19306_01/server.102/b14211/stats.htm#g49431)收集工作。資料庫[最佳化工具](https://docs.oracle.com/cd/B10501_01/server.920/a96533/optimops.htm)會使用統計資料，提供最佳[執行計畫](https://docs.oracle.com/database/121/TGSQL/tgsql_genplan.htm#TGSQL271)。[索引](https://docs.oracle.com/cd/E11882_01/server.112/e40540/indexiot.htm#CNCPT721)可能需要用於快速資料列查詢和彙整作業。Oracle 也提供[記憶體內資料欄儲存庫](https://www.oracle.com/a/tech/docs/twp-oracle-database-in-memory-19c.pdf)，用於記憶體內數據分析。Exadata 提供多項效能改善功能，例如儲存格智慧掃描、儲存體索引、快閃快取，以及儲存體伺服器與資料庫伺服器之間的 InfiniBand 連線。[Real Application Clusters (RAC)](https://www.oracle.com/technetwork/database/options/clustering/rac-twp-overview-5303704.pdf) 可用於實現伺服器高可用性，並使用相同的基礎儲存空間，擴充資料庫 CPU 密集型應用程式。

如要使用 Oracle 最佳化查詢效能，必須仔細考量這些選項和資料庫參數。Oracle 提供多項工具，例如 Active Session History (ASH)、Automatic Database Diagnostic Monitor (ADDM)、Automatic Workload Repository (AWR) 報表、SQL 監控和 Tuning Advisor，以及 Undo 和 Memory Tuning [Advisor](https://docs.oracle.com/database/121/ADMQS/GUID-8DE70F1D-E161-45D2-BE01-E9972883BCEC.htm#ADMQS1031)，可用於調整效能。

#### 靈活的數據分析

在 BigQuery 中，您可以啟用不同的專案、使用者和群組，查詢不同專案中的資料集。查詢執行作業區隔可讓自主團隊在專案中工作，而不會影響其他使用者和專案，方法是將運算單元配額和查詢計費與其他專案和託管資料集的專案區隔開來。

#### 高可用性、備份和災難復原

Oracle 提供 [Data Guard](https://www.oracle.com/database/data-guard/) 做為災難復原和資料庫複製解決方案。您可以設定 [Real Application Clusters (RAC)](https://www.oracle.com/database/technologies/rac.html)，確保伺服器可用性。您可以設定[復原管理員 (RMAN)](https://www.oracle.com/database/technologies/high-availability/rman.html) 備份，用於備份資料庫和封存記錄，以及執行還原和復原作業。[Flashback 資料庫](https://docs.oracle.com/html/E10643_07/rcmsynta023.htm)功能可用於資料庫閃回，將資料庫倒轉至特定時間點。復原資料表空間會保留資料表快照。您可以根據先前執行的 DML/DDL 作業和[復原保留](https://docs.oracle.com/cd/B28359_01/server.111/b28310/undo002.htm#ADMIN10180)設定，使用閃回查詢和「[as of](https://docs.oracle.com/cd/E11882_01/appdev.112/e41502/adfns_flashback.htm#ADFNS01003)」查詢子句查詢舊快照。在 Oracle 中，資料庫的完整性應在資料表空間內管理，而資料表空間取決於系統中繼資料、復原和對應的資料表空間，因為同步一致對 Oracle 備份很重要，且復原程序應包含完整的原始資料。如果不需要在 Oracle 中使用時間點復原功能，您可以在資料表結構定義層級排定匯出作業。

BigQuery 是全代管服務，與傳統資料庫系統的不同之處在於，BigQuery 具備完整的備份功能。您不必考慮伺服器、儲存空間故障、系統錯誤和實體資料損毀等問題。BigQuery 會根據[資料集位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)，在不同資料中心複製資料，盡可能提高可靠性和可用性。BigQuery 多區域功能會跨不同區域複製資料，並防範區域內單一可用區無法使用的情況。BigQuery 單一區域功能會在同一區域內的不同可用區複製資料。

BigQuery 可讓您查詢最多七天前的資料表歷來快照，並使用[時間回溯](https://docs.cloud.google.com/bigquery/docs/time-travel?hl=zh-tw)功能在兩天內還原已刪除的資料表。您可以使用[快照語法](https://docs.cloud.google.com/bigquery/docs/restore-deleted-tables?hl=zh-tw) (`dataset.table@timestamp`) 複製已刪除的資料表 (以便還原)。您也可以從 BigQuery 資料表[匯出](https://docs.cloud.google.com/bigquery/docs/exporting-data?hl=zh-tw)資料，以滿足其他備份需求，例如從意外的使用者操作中復原。現有資料倉儲 (DWH) 系統採用的備份策略和排程，可用於備份。

批次作業和快照技術可讓您為 BigQuery 採用不同的備份策略，因此不必頻繁匯出未變更的資料表和分區。載入或 ETL 作業完成後，只要匯出分區或資料表的一個備份即可。如要降低備份成本，您可以將匯出檔案儲存在 Cloud Storage [Nearline Storage 或 Coldline Storage](https://docs.cloud.google.com/storage/docs/storage-classes?hl=zh-tw) 中，並定義[生命週期政策](https://docs.cloud.google.com/storage/docs/lifecycle?hl=zh-tw)，在經過一段時間後刪除檔案，具體取決於資料保留需求。

#### 快取

BigQuery 提供每位使用者[快取](https://docs.cloud.google.com/bigquery/docs/cached-results?hl=zh-tw)，如果資料未變更，查詢結果會快取約 24 小時。如果結果是從快取擷取，查詢就不會產生費用。

Oracle 提供多種資料和查詢結果快取，例如[緩衝區快取](https://docs.oracle.com/database/121/TGDBA/tune_buffer_cache.htm#TGDBA294)、[結果快取](https://docs.oracle.com/database/121/TGDBA/tune_result_cache.htm#TGDBA616)、[Exadata Flash 快取](http://www.oracle.com/us/solutions/exadata-smart-flash-cache-366203.pdf)和記憶體內資料欄儲存庫。

#### 連線

BigQuery 會處理連線管理，您不需要進行任何伺服器端設定。BigQuery 提供 [JDBC 和 ODBC](https://docs.cloud.google.com/bigquery/partners/simba-drivers?hl=zh-tw) 驅動程式。您可以使用 [Google Cloud 控制台](https://docs.cloud.google.com/bigquery/docs/bigquery-web-ui?hl=zh-tw)或 `bq command-line tool` 進行互動式查詢。您可以使用 [REST API](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2?hl=zh-tw) 和[用戶端程式庫](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)，透過程式與 BigQuery 互動。您可以將 [Google 試算表直接連結](https://cloud.google.com/blog/products/g-suite/connecting-bigquery-and-google-sheets-to-help-with-hefty-data-analysis?hl=zh-tw)至 BigQuery，並使用 [ODBC 和 JDBC 驅動程式](https://docs.cloud.google.com/bigquery/docs/reference/odbc-jdbc-drivers?hl=zh-tw)連結至 Excel。如需電腦版用戶端，可以使用 [DBeaver](https://dbeaver.io/) 等免費工具。

Oracle 提供[監聽器](https://docs.oracle.com/database/121/NETAG/listenercfg.htm#NETAG010)、[服務](https://docs.oracle.com/html/E25494_01/create007.htm)、服務處理常式、多項設定和調整[參數](https://docs.oracle.com/cd/B28359_01/network.111/b28317/listener.htm#NETRF293)，以及[共用和專屬伺服器](https://docs.oracle.com/cd/B28359_01/server.111/b28310/manproc001.htm#ADMIN11166)，用於處理資料庫[連線](https://docs.oracle.com/database/121/NETAG/concepts.htm#NETAG002)。Oracle 提供 [JDBC](https://docs.oracle.com/cd/E11882_01/appdev.112/e13995/oracle/jdbc/OracleDriver.html)、[JDBC Thin](https://docs.oracle.com/cd/B28359_01/java.111/b31224/jdbcthin.htm)、[ODBC](https://docs.oracle.com/database/121/ADFNS/adfns_odbc.htm#ADFNS1112) 驅動程式、[Oracle Client](https://docs.oracle.com/cd/E11882_01/install.112/e47959/install.htm#NTCLI1280) 和 [TNS](https://docs.oracle.com/cd/B28359_01/network.111/b28317/tnsnames.htm#NETRF007) 連線。[RAC 設定](https://docs.oracle.com/database/121/RILIN/undrstnd.htm#RILIN006)需要掃描監聽器、掃描 IP 位址和掃描名稱。

#### 價格和授權

Oracle 會根據資料庫版本和[資料庫選項](https://docs.oracle.com/en/database/oracle/oracle-database/12.2/dblic/Licensing-Information.html#GUID-B6113390-9586-46D7-9008-DCC9EDA45AB4) (例如 RAC、多租戶、Active Data Guard、分區、記憶體內、Real Application Testing、GoldenGate、Spatial and Graph) 的核心數量，收取[授權](https://www.oracle.com/assets/technology-price-list-070617.pdf)和支援費用。

BigQuery 提供彈性的[定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw)方案，依據儲存空間、查詢和串流資料即時插入用量計費。BigQuery 提供[依用量計費](https://cloud.google.com/bigquery/pricing?hl=zh-tw#capacity_compute_analysis_pricing)模式，適合需要預測特定區域費用和運算單元容量的客戶。用於串流資料即時插入和載入作業的運算單元，不會計入專案運算單元容量。如要決定要為資料倉儲購買多少運算單元，請參閱「[BigQuery 容量規劃](#capacity_planning)」。

BigQuery 也會自動將儲存超過 90 天未修改資料的儲存費用[減半](https://cloud.google.com/blog/products/gcp/google-bigquery-cuts-historical-data-storage-cost-in-half-and-accelerates-many-queries-by-10x?hl=zh-tw)。

#### 加上標籤中

BigQuery 資料集、資料表和檢視表可使用鍵/值組合[加上標籤](https://docs.cloud.google.com/bigquery/docs/adding-using-labels?hl=zh-tw)。標籤可用來區分儲存空間費用和內部交易退單。

#### 監控與稽核記錄

Oracle 提供不同層級和種類的[資料庫稽核](https://docs.oracle.com/cd/E11882_01/server.112/e10575/tdpsg_auditing.htm#TDPSG50000)選項、[稽核資料庫](https://www.oracle.com/database/technologies/security/audit-vault-firewall.html)和[資料庫防火牆功能](https://www.oracle.com/database/technologies/security/audit-vault-firewall.html)，這些功能需另外授權。Oracle 提供 [Enterprise Manager](https://www.oracle.com/technetwork/oem/enterprise-manager/overview/index.html) 監控資料庫。

BigQuery 的資料存取記錄和稽核記錄均使用 [Cloud 稽核記錄](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw)，且預設為啟用。資料存取記錄會保留 30 天，其他系統事件和管理員活動記錄則會保留 400 天。如需更長的保留期限，可以按照「 [Google Cloud中的安全性記錄檔分析](https://docs.cloud.google.com/solutions/design-patterns-for-exporting-stackdriver-logging?hl=zh-tw)」一文所述，將記錄[匯出](https://docs.cloud.google.com/solutions/design-patterns-for-exporting-stackdriver-logging?hl=zh-tw)至 BigQuery、Cloud Storage 或 Pub/Sub。如需與現有事件監控工具整合，可以使用 Pub/Sub 匯出，並在現有工具上進行自訂開發，以便從 Pub/Sub 讀取記錄。

稽核記錄包含所有 API 呼叫、查詢陳述式和工作狀態。您可以使用 [Cloud Monitoring](https://docs.cloud.google.com/bigquery/docs/monitoring?hl=zh-tw) 監控運算單元分配情形、查詢和儲存的掃描位元組數，以及其他 BigQuery [指標](https://docs.cloud.google.com/bigquery/docs/monitoring?hl=zh-tw#metrics)。BigQuery [查詢計畫和時間軸](https://docs.cloud.google.com/bigquery/query-plan-explanation?hl=zh-tw)可用於分析查詢階段和效能。

您可以使用[錯誤訊息表格](https://docs.cloud.google.com/bigquery/troubleshooting-errors?hl=zh-tw)，排解查詢工作和 API 錯誤。如要區分每項查詢或工作的運算單元分配，可以使用這項[公用程式](https://github.com/GoogleCloudPlatform/professional-services/tree/master/examples/bigquery-cross-project-slot-monitoring)，這對採用用量計價模式，且有多個專案分散在多個團隊的客戶來說非常實用。

#### 維護、升級和版本

BigQuery 是全代管服務，您不需要進行任何維護或升級。BigQuery 不提供不同版本。升級作業會持續進行，不需要停機，也不會影響系統效能。詳情請參閱[版本資訊](https://docs.cloud.google.com/bigquery/docs/release-notes?hl=zh-tw)。

Oracle 和 Exadata 需要您執行資料庫和基礎架構層級的修補、升級和維護作業。Oracle 有許多版本，且預計每年都會發布新的主要版本。雖然新版本回溯相容，但查詢效能、情境和功能可能會有所變動。

有些應用程式可能需要特定版本，例如 10g、[11g](https://docs.oracle.com/cd/B28359_01/server.111/b28279/chapter1.htm#NEWFTCH1) 或 [12c](https://docs.oracle.com/database/121/NEWFT/chapter12102.htm#NEWFT003)。進行重大資料庫升級時，