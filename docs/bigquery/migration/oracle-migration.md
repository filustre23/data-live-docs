Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [參考資料](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 從 Oracle 遷移至 BigQuery

本文件提供從 Oracle 遷移至 BigQuery 的概略指南。本文說明基本架構差異，並建議從 Oracle RDBMS (包括 Exadata) 執行的資料倉儲和資料市集遷移至 BigQuery 的方法。本文提供的詳細資料也適用於 Exadata、ExaCC 和 Oracle Autonomous Data Warehouse，因為這些服務使用的 Oracle 軟體相容。

本文適用於企業架構師、資料庫管理員、應用程式開發人員和 IT 安全專業人員，協助他們從 Oracle 遷移至 BigQuery，並解決遷移過程中的技術難題。

您也可以使用[批次 SQL 翻譯](https://docs.cloud.google.com/bigquery/docs/batch-sql-translator?hl=zh-tw)大量遷移 SQL 指令碼，或使用[互動式 SQL 翻譯](https://docs.cloud.google.com/bigquery/docs/interactive-sql-translator?hl=zh-tw)翻譯臨時查詢。這兩項工具的[預先發布版](https://cloud.google.com/products?hl=zh-tw#product-launch-stages)都支援 Oracle SQL、PL/SQL 和 Exadata。

## 遷移前

為確保資料倉儲遷移作業順利完成，請在專案時間軸的早期，開始規劃遷移策略。如要瞭解如何有系統地規劃遷移作業，請參閱「[遷移的內容和方式：遷移作業架構](https://docs.cloud.google.com/bigquery/docs/migration/migration-overview?hl=zh-tw#what_and_how_to_migrate_the_migration_framework)」。

### BigQuery 容量規劃

在幕後，BigQuery 中的數據分析處理量是以「運算單元」為單位計算。BigQuery 運算單元是 Google 專有的運算能力單位，用來執行 SQL 查詢。

BigQuery 會在查詢執行時持續計算所需的運算單元數量，但會根據[公平調度器](https://docs.cloud.google.com/bigquery/docs/slots?hl=zh-tw#fair_scheduling_in_bigquery)將運算單元分配給查詢。

為 BigQuery 運算單元規劃容量時，您可以選擇下列計價模式：

* [以量計價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#on_demand_pricing)：在以量計價模式中，BigQuery 會按照實際處理的位元組數 (資料大小) 收取費用，因此您只需為執行的查詢付費。如要進一步瞭解 BigQuery 如何判斷資料量，請參閱「[資料量的計算方式](https://cloud.google.com/bigquery/pricing?hl=zh-tw#data)」一文。由於運算單元決定了基礎運算容量，因此您可以根據所需的運算單元數量支付 BigQuery 使用費用 (而非根據處理的位元組數)。根據預設， Google Cloud 專案最多只能有 2,000 個時段。
* [以運算資源為基礎的計價模式](https://cloud.google.com/bigquery/pricing?hl=zh-tw#capacity_compute_analysis_pricing)：
  採用以運算資源為基礎的計價模式時，您會購買 BigQuery 運算單元[保留項目](https://docs.cloud.google.com/bigquery/docs/reservations-intro?hl=zh-tw) (最少 100 個)，而不必根據查詢處理的位元組數付費。對於企業資料倉儲工作負載，我們建議採用以容量計價模式，這類工作負載通常會同時執行許多報表和擷取、載入、轉換 (ELT) 查詢，且用量可預測。

為協助估算配額，建議您使用 [Cloud Monitoring 設定 BigQuery 監控](https://docs.cloud.google.com/bigquery/docs/monitoring?hl=zh-tw)，並[使用 BigQuery 分析稽核記錄](https://docs.cloud.google.com/bigquery/audit-logs?hl=zh-tw)。許多客戶使用 [Data Studio](https://datastudio.google.com/?hl=zh-tw) (例如，請參閱 [Data Studio 資訊主頁的[開放原始碼範例](https://datastudio.google.com/c/u/0/reporting/1kwNFt05J8_GCju5TBH1v4IlBmmAU74Nu/page/nSaN?hl=zh-tw))、[Looker](https://looker.com/) 或 [Tableau](https://www.tableau.com/) 做為前端，以視覺化方式呈現 BigQuery 稽核記錄資料，特別是查詢和專案的時段用量。](https://github.com/GoogleCloudPlatform/professional-services/tree/master/examples/bigquery-audit-log)您也可以運用 BigQuery 系統資料表資料，監控工作和預訂的時段用量。如需範例，請參閱[開放原始碼範例](https://github.com/GoogleCloudPlatform/bigquery-utils/tree/master/dashboards/system_tables)的[數據分析資訊主頁](https://datastudio.google.com/s/kGZzZJWkeyA?hl=zh-tw)。

定期監控及分析時段使用情況，有助於估算貴機構在 Google Cloud成長時所需的總時段數。

舉例來說，假設您一開始保留 [4,000 個 BigQuery 運算單元](https://docs.cloud.google.com/bigquery/docs/slots?hl=zh-tw)，同時執行 100 個中等複雜度的查詢。如果您發現查詢的執行計畫中等待時間較長，且資訊主頁顯示運算單元使用率偏高，可能表示您需要額外的 BigQuery 運算單元，才能支援工作負載。如要透過一年或三年期承諾自行購買運算單元，請使用 Google Cloud 控制台或 bq 指令列工具，[開始使用 BigQuery 預留](https://docs.cloud.google.com/bigquery/docs/reservations-get-started?hl=zh-tw)。

如有任何關於目前方案和上述選項的問題，請與[業務代表](https://cloud.google.com/contact?hl=zh-tw)聯絡。

### Google Cloud的安全防護

以下各節說明常見的 Oracle 安全性控制項，以及如何確保資料倉儲在 Google Cloud環境中受到保護。

#### 身分與存取權管理 (IAM)

Oracle 提供[使用者、權限、角色和設定檔](https://docs.oracle.com/cd/B19306_01/network.102/b14266/admusers.htm#DBSEG10000)，可管理資源存取權。

BigQuery 使用 [IAM](https://docs.cloud.google.com/iam?hl=zh-tw) 管理資源存取權，並提供資源和動作的集中式[存取權管理](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)。BigQuery 提供的資源類型包括機構、專案、資料集、資料表和檢視區塊。在 IAM 政策階層中，資料集是專案的子項資源。資料表會繼承所屬資料集的權限。

如要授予資源的存取權，請將一或多個角色指派給使用者、群組或服務帳戶。機構和專案角色會影響執行工作或管理專案的能力，而資料集角色則會影響存取或修改專案內資料的能力。

IAM 提供下列類型的角色：

* [預先定義角色](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)的用意在於支援常見的用途和存取權控管模式。預先定義的角色提供特定服務的精細存取權，並由 Google Cloud管理。
* [基本角色](https://docs.cloud.google.com/bigquery/docs/access-control-basic-roles?hl=zh-tw)包括「擁有者」、「編輯者」和「檢視者」角色。

  **注意：** BigQuery 的資料集層級基本角色在 IAM 推出前就已經存在。建議您盡量減少使用基本角色。在正式環境中，除非沒有其他替代方案，否則請勿授予基本角色，請改用[預先定義的 IAM](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw) 角色。
* [自訂角色](https://docs.cloud.google.com/iam/docs/understanding-custom-roles?hl=zh-tw)：根據使用者指定的權限清單，提供精細的存取權限。

當您同時把預先定義角色和基本角色指派給某個使用者時，您授予的權限就是這兩個角色權限的聯集。

#### 資料列層級安全性

[Oracle Label Security (OLS)](https://docs.oracle.com/database/121/TDPSG/GUID-72D524FF-5A86-495A-9D12-14CB13819D42.htm#TDPSG94446) 可逐列限制資料存取權。行層級安全性的典型用途是限制銷售人員只能存取自己管理的帳戶。實作資料列層級安全防護機制後，您就能獲得精細的存取控管機制。

如要在 BigQuery 中實現資料列層級安全防護機制，可以使用[授權檢視畫面](https://docs.cloud.google.com/bigquery/docs/authorized-views?hl=zh-tw)和[資料列層級存取權政策](https://docs.cloud.google.com/bigquery/docs/managing-row-level-security?hl=zh-tw)。如要進一步瞭解如何設計及導入這些政策，請參閱「[BigQuery 資料列層級安全防護機制簡介](https://docs.cloud.google.com/bigquery/docs/row-level-security-intro?hl=zh-tw)」。

#### 全磁碟加密

Oracle 提供[資料庫透明加密 (TDE)](https://docs.oracle.com/cd/E11882_01/network.112/e40393/asotrans.htm#ASOAG600) 和[網路加密](https://docs.oracle.com/database/121/DBSEG/asoconfg.htm#DBSEG020)，可加密靜態資料和傳輸中的資料。TDE 需要另外授權的進階安全性選項。

無論資料來源或任何其他條件為何，BigQuery 預設都會加密所有[靜態](https://docs.cloud.google.com/docs/security/encryption/default-encryption?hl=zh-tw)和[傳輸中](https://docs.cloud.google.com/docs/security/encryption-in-transit?hl=zh-tw)的資料，且無法關閉這項功能。BigQuery 也支援[客戶管理的加密金鑰](https://docs.cloud.google.com/bigquery/docs/customer-managed-encryption?hl=zh-tw) (CMEK)，方便使用者在 [Cloud Key Management Service](https://docs.cloud.google.com/kms/docs?hl=zh-tw) 中控管及管理金鑰加密金鑰。如要進一步瞭解靜態資料加密，請參閱「[預設靜態資料加密](https://docs.cloud.google.com/docs/security/encryption/default-encryption?hl=zh-tw)」和「[傳輸中資料加密](https://docs.cloud.google.com/docs/security/encryption-in-transit?hl=zh-tw)」。 Google Cloud

#### 資料遮蓋和遮蓋

Oracle 會在 Real Application Testing 中使用[資料遮蓋](https://docs.oracle.com/cd/E11882_01/server.112/e41481/tdm_data_masking.htm#RATUG04000)，並使用[資料遮蓋](https://docs.oracle.com/cd/E11882_01/network.112/e40393/redaction.htm#ASOAG594)，讓您遮蓋 (遮蓋) 應用程式發出的查詢所傳回的資料。

BigQuery 支援資料欄層級的[動態資料遮蓋](https://docs.cloud.google.com/bigquery/docs/column-data-masking-intro?hl=zh-tw)。您可以針對使用者群組，選擇性地掩蓋特定資料欄的資料，但這些使用者還是能正常使用該資料欄。

您可以使用 [Sensitive Data Protection](https://docs.cloud.google.com/sensitive-data-protection/docs?hl=zh-tw) 識別及遮蓋 BigQuery 中的機密個人識別資訊 (PII)。

### BigQuery 與 Oracle 比較

本節說明 BigQuery 和 Oracle 的主要差異。這些重點有助於找出遷移障礙，並規劃必要的變更。

#### 系統架構

Oracle 和 BigQuery 的主要差異之一，在於 BigQuery 是無伺服器雲端 EDW，具有獨立的儲存空間和運算層，可根據查詢需求調度資源。由於 BigQuery 無伺服器服務的性質，您不會受到硬體決策的限制，而是可以透過預留項目，為查詢和使用者要求更多資源。BigQuery 也不需要設定底層軟體和基礎架構，例如作業系統 (OS)、網路系統和儲存系統，包括擴充和高可用性。BigQuery 會負責處理擴充性、管理和管理作業。下圖說明 BigQuery 儲存空間階層。

瞭解基礎儲存空間和查詢處理架構，例如儲存空間 (Colossus) 和查詢執行 (Dremel) 之間的區隔，以及Google Cloud 如何分配資源 (Borg)，有助於瞭解行為差異，並盡可能提高查詢效能和成本效益。詳情請參閱 [BigQuery](https://cloud.google.com/blog/products/data-analytics/new-blog-series-bigquery-explained-overview?hl=zh-tw)、[Oracle](https://www.oracle.com/webfolder/technetwork/tutorials/architecture-diagrams/18/technical-architecture/database-technical-architecture.html) 和 [Exadata](https://www.oracle.com/technetwork/database/exadata/exadata-x7-2-ds-3908482.pdf) 的參考系統架構。

#### 資料和儲存空間架構

資料和儲存空間結構是任何資料分析系統的重要部分，因為這會影響查詢效能、成本、可擴充性和效率。

BigQuery [會將資料儲存和運算作業分離](https://cloud.google.com/blog/products/gcp/separation-of-storage-and-compute-in-bigquery?hl=zh-tw)，並將資料儲存在 Colossus 中，資料會經過壓縮，並以名為 [Capacitor](https://cloud.google.com/blog/products/gcp/inside-capacitor-bigquerys-next-generation-columnar-storage-format?hl=zh-tw) 的資料欄格式儲存。

BigQuery 會使用 Capacitor 直接處理壓縮資料，不必解壓縮。如上圖所示，BigQuery 提供[資料集](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/datasets?hl=zh-tw)做為最高層級的抽象概念，用於整理資料表的存取權。您可以使用[結構定義](https://docs.cloud.google.com/bigquery/docs/schemas?hl=zh-tw)和[標籤](https://docs.cloud.google.com/bigquery/docs/adding-using-labels?hl=zh-tw)進一步整理表格。BigQuery 提供[分區](https://docs.cloud.google.com/bigquery/docs/partitioned-tables?hl=zh-tw)功能，可提升查詢效能、降低成本，以及管理資訊生命週期。儲存空間資源會在耗用時分配，並在移除資料或捨棄資料表時取消分配。

Oracle 會以資料列格式儲存資料，並使用以區段整理的 [Oracle 區塊格式](https://docs.oracle.com/cd/B28359_01/server.111/b28318/logical.htm#CNCPT004)。結構定義 (由使用者擁有) 用於整理資料表和其他資料庫物件。自 Oracle 12c 起，[多租戶](https://www.oracle.com/technetwork/database/multitenant/learn-more/multitenantwp18c-4396158.pdf)可用於在一個資料庫執行個體中建立可插拔資料庫，進一步隔離。[分區](https://www.oracle.com/technetwork/database/options/partitioning/partitioning-wp-12c-1896137.pdf)可用於提升查詢效能和資訊生命週期作業。Oracle 為獨立和[Real Application Clusters (RAC)](https://www.oracle.com/technetwork/database/options/clustering/rac-twp-overview-5303704.pdf) 資料庫提供多種[儲存空間選項](https://docs.oracle.com/database/121/CNCPT/physical.htm#CNCPT88986)，例如 ASM、OS 檔案系統和叢集檔案系統。

Exadata 會在儲存空間單元伺服器中提供最佳化儲存空間基礎架構，並允許 Oracle 伺服器使用 [ASM](https://docs.oracle.com/cd/E11882_01/server.112/e18951/asmcon.htm#OSTMG036) 透明地存取這項資料。Exadata 提供[混合分欄壓縮 (HCC)](https://www.oracle.com/technetwork/database/exadata/ehcc-twp-131254.pdf) 選項，方便使用者壓縮資料表和分割區。

Oracle 需要預先佈建儲存空間容量，並仔細調整區隔、資料檔案和表空間的大小，以及設定自動遞增。

#### 查詢執行和效能

BigQuery 會在查詢層級管理效能和調整規模，以盡可能提高效能，BigQuery 會進行許多最佳化，例如：

* [記憶體內查詢執行](https://cloud.google.com/blog/products/gcp/in-memory-query-execution-in-google-bigquery?hl=zh-tw)
* 以 [Dremel](http://static.googleusercontent.com/media/research.google.com/en//pubs/archive/36632.pdf) 執行引擎為基礎的多層樹狀結構架構
* Capacitor 內建自動儲存空間最佳化功能
* 每秒總對分頻寬 1 PB，搭配 [Jupiter](https://cloudplatform.googleblog.com/2015/06/A-Look-Inside-Googles-Data-Center-Networks.html)
* [自動調度資源管理](https://cloud.google.com/blog/products/gcp/understanding-bigquerys-rapid-scaling-and-simple-pricing?hl=zh-tw)
  提供 PB 級的快速查詢

BigQuery 會在載入資料時收集資料欄統計資料，並提供診斷[查詢計畫](https://docs.cloud.google.com/bigquery/query-plan-explanation?hl=zh-tw)和[時間點](https://docs.cloud.google.com/bigquery/query-plan-explanation?hl=zh-tw)資訊。查詢資源會根據查詢類型及複雜度分配。每個查詢都會使用一些[運算單元](https://docs.cloud.google.com/bigquery/docs/slots?hl=zh-tw)，這些運算單元是由一定數量的 CPU 與 RAM 組成。

Oracle 提供資料[統計資料](https://docs.oracle.com/cd/B19306_01/server.102/b14211/stats.htm#g49431)收集工作。資料庫[最佳化工具](https://docs.oracle.com/cd/B10501_01/server.920/a96533/optimops.htm)會使用統計資料提供最佳[執行計畫](https://docs.oracle.com/database/121/TGSQL/tgsql_genplan.htm#TGSQL271)。如要快速查詢資料列和執行聯結作業，可能需要[索引](https://docs.oracle.com/cd/E11882_01/server.112/e40540/indexiot.htm#CNCPT721)。Oracle 也提供[記憶體內資料欄儲存空間](https://www.oracle.com/a/tech/docs/twp-oracle-database-in-memory-19c.pdf)，用於記憶體內分析。Exadata 提供多項效能改善功能，例如儲存格智慧掃描、儲存空間索引、快閃快取，以及儲存伺服器和資料庫伺服器之間的 InfiniBand 連線。[Real Application Clusters (RAC)](https://www.oracle.com/technetwork/database/options/clustering/rac-twp-overview-5303704.pdf) 可用於實現伺服器高可用性，並使用相同的基礎儲存空間，擴充資料庫 CPU 密集型應用程式。

如要使用 Oracle 最佳化查詢效能，必須仔細考量這些選項和資料庫參數。Oracle 提供多種工具，例如「Active Session History」(ASH)、「Automatic Database Diagnostic Monitor」(ADDM)、「Automatic Workload Repository」(AWR) 報表、SQL 監控和 Tuning Advisor，以及 Undo 和 Memory Tuning [Advisors](https://docs.oracle.com/database/121/ADMQS/GUID-8DE70F1D-E161-45D2-BE01-E9972883BCEC.htm#ADMQS1031)，可供您調整效能。

#### 敏捷分析

在 BigQuery 中，您可以允許不同專案、使用者和群組查詢不同專案中的資料集。查詢執行作業分離後，自主團隊就能在專案中工作，不會影響其他使用者和專案，因為系統會將配額和查詢帳單與其他專案和代管資料集的專案分開。

#### 高可用性、備份和災難復原

Oracle 提供 [Data Guard](https://www.oracle.com/database/data-guard/) 做為災難復原和資料庫複製解決方案。[Real Application Clusters (RAC)](https://www.oracle.com/database/technologies/rac.html)
可設定伺服器可用性。
[復原管理員 (RMAN)](https://www.oracle.com/database/technologies/high-availability/rman.html)
備份可設定為資料庫和歸檔記錄備份，也可用於還原和復原作業。[資料庫回溯](https://docs.oracle.com/html/E10643_07/rcmsynta023.htm)功能可用於資料庫回溯，將資料庫倒轉至特定時間點。復原資料表空間保留表格快照。視先前執行的 DML/DDL 作業和[復原保留](https://docs.oracle.com/cd/B28359_01/server.111/b28310/undo002.htm#ADMIN10180)設定而定，您可以使用回溯查詢和「[as of](https://docs.oracle.com/cd/E11882_01/appdev.112/e41502/adfns_flashback.htm#ADFNS01003)」查詢子句，查詢舊的快照。在 Oracle 中，資料庫的完整性應在依附於系統中繼資料、復原和相應表空間的表空間內管理，因為 Oracle 備份需要同步一致，且復原程序應包含完整的主要資料。如果 Oracle 不需要時間點復原功能，您可以在資料表結構定義層級排定匯出作業。

BigQuery 是全代管服務，與傳統資料庫系統不同，具備完整的備份功能。您不必擔心伺服器、儲存空間故障、系統錯誤和實體資料損毀。BigQuery 會根據[資料集位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)，在不同資料中心複製資料，盡可能提高可靠性和可用性。BigQuery 多區域功能會跨不同區域複製資料，並防範區域內單一可用區無法使用的情況。BigQuery 單一區域功能會在同一區域內的不同可用區複製資料。

BigQuery 支援[時間回溯](https://docs.cloud.google.com/bigquery/docs/time-travel?hl=zh-tw)，可查詢最多七天前的資料表快照，並在兩天內還原已刪除的資料表。您可以使用[快照語法](https://docs.cloud.google.com/bigquery/docs/restore-deleted-tables?hl=zh-tw) (`dataset.table@timestamp`) 複製已刪除的資料表 (以便還原)。如需額外備份，例如從使用者誤操作中復原，可以從 BigQuery 資料表[匯出](https://docs.cloud.google.com/bigquery/docs/exporting-data?hl=zh-tw)資料。您可以使用現有資料倉儲 (DWH) 系統的備份策略和時間表。

批次作業和快照技術可為 BigQuery 提供不同的備份策略，因此您不需要經常匯出未變更的資料表和分區。載入或 ETL 作業完成後，匯出一個分割區或資料表備份即可。如要降低備份成本，您可以將匯出檔案儲存在 Cloud Storage [Nearline Storage 或 Coldline Storage](https://docs.cloud.google.com/storage/docs/storage-classes?hl=zh-tw)，並根據資料保留規定定義[生命週期政策](https://docs.cloud.google.com/storage/docs/lifecycle?hl=zh-tw)，在一段時間後刪除檔案。

#### 快取

BigQuery 提供使用者專屬[快取](https://docs.cloud.google.com/bigquery/docs/cached-results?hl=zh-tw)，如果資料沒有變更，查詢結果會快取約 24 小時。如果結果是從快取擷取，查詢費用為零。

Oracle 提供多種資料和查詢結果快取，例如[緩衝區快取](https://docs.oracle.com/database/121/TGDBA/tune_buffer_cache.htm#TGDBA294)、[結果快取](https://docs.oracle.com/database/121/TGDBA/tune_result_cache.htm#TGDBA616)、[Exadata Flash Cache](http://www.oracle.com/us/solutions/exadata-smart-flash-cache-366203.pdf) 和記憶體內資料欄儲存空間。

#### 連線

BigQuery 會處理連線管理作業，您不需要進行任何伺服器端設定。BigQuery 提供 [JDBC 和 ODBC](https://docs.cloud.google.com/bigquery/partners/simba-drivers?hl=zh-tw) 驅動程式。您可以使用 [Google Cloud 控制台](https://docs.cloud.google.com/bigquery/docs/bigquery-web-ui?hl=zh-tw)或 `bq command-line tool` 進行互動式查詢。您可以使用 [REST API](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2?hl=zh-tw) 和[用戶端程式庫](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)，以程式輔助方式與 BigQuery 互動。您可以[直接將 Google 試算表連結至 BigQuery](https://cloud.google.com/blog/products/g-suite/connecting-bigquery-and-google-sheets-to-help-with-hefty-data-analysis?hl=zh-tw)，並使用 [ODBC 和 JDBC 驅動程式](https://docs.cloud.google.com/bigquery/docs/reference/odbc-jdbc-drivers?hl=zh-tw)連結至 Excel。如要使用電腦版用戶端，可以選擇 [DBeaver](https://dbeaver.io/) 等免費工具。

Oracle 提供[接聽程式](https://docs.oracle.com/database/121/NETAG/listenercfg.htm#NETAG010)、[服務](https://docs.oracle.com/html/E25494_01/create007.htm)、服務處理常式、多個設定和調整[參數](https://docs.oracle.com/cd/B28359_01/network.111/b28317/listener.htm#NETRF293)，以及[共用和專用伺服器](https://docs.oracle.com/cd/B28359_01/server.111/b28310/manproc001.htm#ADMIN11166)，用來處理資料庫[連線](https://docs.oracle.com/database/121/NETAG/concepts.htm#NETAG002)。Oracle 提供 [JDBC](https://docs.oracle.com/cd/E11882_01/appdev.112/e13995/oracle/jdbc/OracleDriver.html)、[JDBC Thin](https://docs.oracle.com/cd/B28359_01/java.111/b31224/jdbcthin.htm)、[ODBC](https://docs.oracle.com/database/121/ADFNS/adfns_odbc.htm#ADFNS1112) 驅動程式、[Oracle Client](https://docs.oracle.com/cd/E11882_01/install.112/e47959/install.htm#NTCLI1280) 和 [TNS](https://docs.oracle.com/cd/B28359_01/network.111/b28317/tnsnames.htm#NETRF007) 連線。[RAC 設定](https://docs.oracle.com/database/121/RILIN/undrstnd.htm#RILIN006)需要掃描接聽程式、掃描 IP 位址和掃描名稱。

#### 價格和授權

Oracle 會根據資料庫版本和[資料庫選項](https://docs.oracle.com/en/database/oracle/oracle-database/12.2/dblic/Licensing-Information.html#GUID-B6113390-9586-46D7-9008-DCC9EDA45AB4) (例如 RAC、多租戶、Active Data Guard、分區、記憶體內建、Real Application Testing、GoldenGate，以及 Spatial and Graph) 的核心數量，收取[授權](https://www.oracle.com/assets/technology-price-list-070617.pdf)和支援費用。

BigQuery 提供彈性的[計價](https://cloud.google.com/bigquery/pricing?hl=zh-tw)選項，費用取決於儲存空間、查詢和串流插入的用量。如果客戶需要特定區域的預估費用和運算單元容量，BigQuery 提供[以容量為準的計價方式](https://cloud.google.com/bigquery/pricing?hl=zh-tw#capacity_compute_analysis_pricing)。用於串流插入和載入的運算單元不會計入專案運算單元容量。如要決定為資料倉儲購買多少運算單元，請參閱 [BigQuery 容量規劃](#capacity_planning)。

此外，如果資料超過 90 天未經修改，BigQuery 也會自動[減半](https://cloud.google.com/blog/products/gcp/google-bigquery-cuts-historical-data-storage-cost-in-half-and-accelerates-many-queries-by-10x?hl=zh-tw)儲存空間費用。

#### 標籤

BigQuery 資料集、資料表和檢視區塊可以[加上標籤](https://docs.cloud.google.com/bigquery/docs/adding-using-labels?hl=zh-tw)，並以鍵值組表示。標籤可用於區分儲存空間成本和內部退款。

#### 監控與稽核記錄

Oracle 提供不同層級和類型的[資料庫稽核](https://docs.oracle.com/cd/E11882_01/server.112/e10575/tdpsg_auditing.htm#TDPSG50000)選項，以及[稽核保管庫](https://www.oracle.com/database/technologies/security/audit-vault-firewall.html)和[資料庫防火牆功能](https://www.oracle.com/database/technologies/security/audit-vault-firewall.html)，這些功能需另外取得授權。Oracle 提供 [Enterprise Manager](https://www.oracle.com/technetwork/oem/enterprise-manager/overview/index.html)，用於監控資料庫。

對於 BigQuery，[Cloud 稽核記錄](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw)會同時用於資料存取記錄和稽核記錄，且預設為啟用。資料存取記錄會保留 30 天，其他系統事件和管理員活動記錄則會保留 400 天。如要保留更長時間，您可以按照「[安全性記錄分析 Google Cloud」一文的說明，將記錄匯出至 BigQuery、Cloud Storage 或 Pub/Sub。](https://docs.cloud.google.com/solutions/design-patterns-for-exporting-stackdriver-logging?hl=zh-tw)如需與現有事件監控工具整合，可以使用 Pub/Sub 匯出資料，並在現有工具上進行自訂開發，從 Pub/Sub 讀取記錄。

稽核記錄包含所有 API 呼叫、查詢陳述式和工作狀態。您可以使用 [Cloud Monitoring](https://docs.cloud.google.com/bigquery/docs/monitoring?hl=zh-tw) 監控運算單元分配情形、查詢和儲存的位元組數，以及其他 BigQuery [指標](https://docs.cloud.google.com/bigquery/docs/monitoring?hl=zh-tw#metrics)。BigQuery [查詢計畫和時間軸](https://docs.cloud.google.com/bigquery/query-plan-explanation?hl=zh-tw)可用於分析查詢階段和效能。

您可以參考[錯誤訊息表](https://docs.cloud.google.com/bigquery/troubleshooting-errors?hl=zh-tw)，排解查詢工作和 API 錯誤。如要區分每個查詢或作業的時段分配情形，可以使用這個[公用程式](https://github.com/GoogleCloudPlatform/professional-services/tree/master/examples/bigquery-cross-project-slot-monitoring)，這對採用以容量為準的定價，且有多個專案分散在多個團隊的客戶來說很有幫助。

#### 維護、升級和版本

BigQuery 是全代管服務，您不必進行任何維護或升級作業。BigQuery 不提供不同版本。升級作業會持續進行，不會造成停機或降低系統效能。詳情請參閱「[版本資訊](https://docs.cloud.google.com/bigquery/docs/release-notes?hl=zh-tw)」。

Oracle 和 Exadata 要求您執行資料庫和基礎架構層級的修補、升級和維護作業。Oracle 有許多版本，且每年都會發布新的主要版本。雖然新版本具備回溯相容性，但查詢效能、內容和功能可能會有所變更。

有些應用程式可能需要特定版本，例如 10g、[11g](https://docs.oracle.com/cd/B28359_01/server.111/b28279/chapter1.htm#NEWFTCH1) 或 [12c](https://docs.oracle.com/database/121/NEWFT/chapter12102.htm#NEWFT003)。進行重大資料庫升級時，需要審慎規劃和測試。從不同版本遷移時，查詢子句和資料庫物件可能會有不同的技術轉換需求。

#### 工作負載

Oracle Exadata 支援混合工作負載，包括 OLTP 工作負載。BigQuery 專為分析而設計，不適合處理 OLTP 工作負載。使用相同 Oracle 的 OLTP 工作負載應在Google Cloud中遷移至 Cloud SQL、Spanner 或 Firestore。Oracle 提供其他選項，例如 Advanced Analytics 和 Spatial and Graph。這些工作負載可能需要重新編寫，才能遷移至 BigQuery。詳情請參閱「[遷移 Oracle 選項](#migrating-oracle-database-options)」。

#### 參數和設定

Oracle 提供並要求在[作業系統](https://docs.oracle.com/en/database/oracle/oracle-database/12.2/cwlin/configuring-kernel-parameters-for-linux.html#GUID-6127884D-FB27-45FA-9498-B2540632CBD5)、[資料庫](https://docs.oracle.com/cd/B28359_01/server.111/b28320/dynviews_2085.htm#REFRN30176)、[RAC](https://docs.oracle.com/database/121/RACAD/GUID-59DEC066-5743-4EDE-9A02-E8896005F658.htm#RACAD017)、[ASM](https://docs.oracle.com/en/database/oracle/oracle-database/12.2/ostmg/init-params-asm-instance.html#GUID-E31FC459-3208-4390-9A27-2FB626520EC4) 和[接聽程式](https://docs.oracle.com/cd/B19306_01/network.102/b14213/listener.htm)層級設定及調整許多參數，以因應不同的工作負載和應用程式。BigQuery 是全代管服務，您不需要設定任何初始化參數。

#### 限制與配額

Oracle 會根據基礎架構、硬體容量、參數、軟體版本和授權，設定硬性與軟性限制。BigQuery 對特定動作和物件設有[配額與限制](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)。

#### BigQuery 佈建

BigQuery 是平台即服務 (PaaS)，也是雲端大規模平行處理資料倉儲。Google 會管理後端，因此容量可隨時擴充或縮減，使用者不必介入。因此，不同於許多 RDBMS 系統，您不需要在使用 BigQuery 之前佈建資源。BigQuery 會根據您的使用模式，以動態方式分配儲存空間及查詢資源。儲存空間資源會在耗用時分配，並在移除資料或捨棄資料表時取消分配。查詢資源會根據查詢類型及複雜度分配。每項查詢都會使用運算單元。系統會使用最終公平性排程器，因此某些查詢可能會在短時間內分配到較多的運算單元數量，但排程器最終仍會修正這個問題。

以傳統 VM 術語來說，BigQuery 提供以下兩項服務的同等功能：

* 以秒計費
* 以秒為單位的資源調度

為完成這項工作，BigQuery 會執行下列操作：

* 部署大量資源，避免需要快速擴充。
* 使用多租戶資源，一次分配大量區塊，時間以秒為單位。
* 透過規模經濟，有效率地為使用者分配資源。
* 只會針對您執行的工作收費，而非部署的資源，因此您只需支付使用的資源費用。

如要進一步瞭解定價，請參閱「[瞭解 BigQuery 的快速擴充功能和簡單定價](https://cloud.google.com/blog/products/gcp/understanding-bigquerys-rapid-scaling-and-simple-pricing?hl=zh-tw)」。

## 結構定義遷移

如要將資料從 Oracle 遷移至 BigQuery，您必須瞭解 Oracle 資料類型和 BigQuery 對應關係。

### Oracle 資料類型和 BigQuery 對應項目

Oracle 資料類型與 BigQuery 資料類型不同。如要進一步瞭解 BigQuery 資料類型，請參閱官方[說明文件](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw)。

如要詳細比較 Oracle 和 BigQuery 資料類型，請參閱 [Oracle SQL 翻譯指南](https://docs.cloud.google.com/bigquery/docs/migration/oracle-sql?hl=zh-tw)。

### 索引

在許多分析工作負載中，會使用直欄式資料表，而非列儲存區。這可大幅增加以資料欄為基礎的作業，並免除批次分析的索引使用。BigQuery 也會以直欄格式儲存資料，因此不需要索引。如果分析工作負載只需要一小組以列為基礎的存取權，[Bigtable](https://docs.cloud.google.com/bigtable/docs/overview?hl=zh-tw#top_of_page) 可能是更好的替代方案。如果工作負載需要處理交易，且具有嚴格的關聯一致性，[Spanner](https://docs.cloud.google.com/spanner/docs/overview?hl=zh-tw) 或 [Cloud SQL](https://docs.cloud.google.com/sql/docs?hl=zh-tw) 可能是更好的替代方案。

總而言之，BigQuery 不需要索引，也不會提供索引，您可以使用[分區](https://docs.cloud.google.com/bigquery/docs/partitioned-tables?hl=zh-tw)或[分群](https://docs.cloud.google.com/bigquery/docs/clustered-tables?hl=zh-tw)。如要進一步瞭解如何在 BigQuery 中調整及提升查詢效能，請參閱「[最佳化查詢效能簡介](https://docs.cloud.google.com/bigquery/docs/best-practices-performance-overview?hl=zh-tw)」。

### 瀏覽次數

與 Oracle 類似，BigQuery 允許建立自訂檢視區塊。不過，[BigQuery 中的檢視表](https://docs.cloud.google.com/bigquery/docs/views-intro?hl=zh-tw)不支援 DML 陳述式。

### 具體化檢視表

Materialized view 通常用於改善「寫入一次，讀取多次」類型的報表和工作負載的報表顯示時間。

Oracle 提供 materialized view，只要建立及維護資料表來保存查詢結果資料集，即可提高檢視效能。在 Oracle 中，具體化檢視表有兩種重新整理方式：提交時和隨選。

BigQuery 也提供[具體化檢視表功能](https://docs.cloud.google.com/bigquery/docs/materialized-views-intro?hl=zh-tw)。BigQuery 會運用具體化檢視表的預先運算結果，並盡可能只讀取基礎資料表的差異變更，以運算最新結果。

數據分析或其他現代化商業智慧 (BI) 工具的快取功能也能提升效能，並免除重新執行相同查詢的需要，進而節省費用。

### 資料表分區

資料表分區廣泛用於 Oracle 資料倉儲。與 Oracle 不同，BigQuery 不支援階層式分區。

BigQuery 實作了三種[資料表分區](https://docs.cloud.google.com/bigquery/docs/partitioned-tables?hl=zh-tw)，可讓查詢根據分區欄指定述詞篩選條件，以減少掃描的資料量。

* [依擷取時間分區的資料表](https://docs.cloud.google.com/bigquery/docs/creating-partitioned-tables?hl=zh-tw)：根據資料的擷取時間分區的資料表。
* [依資料欄分區的資料表](https://docs.cloud.google.com/bigquery/docs/partitioned-tables?hl=zh-tw#date_timestamp_partitioned_tables)：根據 `TIMESTAMP` 或 `DATE` 資料欄分區的資料表。
* [依整數範圍分區的資料表](https://docs.cloud.google.com/bigquery/docs/creating-integer-range-partitions?hl=zh-tw)：根據整數資料欄分區的資料表。

如要進一步瞭解 BigQuery 中分區資料表的限制和配額，請參閱[分區資料表簡介](https://docs.cloud.google.com/bigquery/docs/partitioned-tables?hl=zh-tw)。

如果 BigQuery 限制會影響遷移資料庫的功能，請考慮使用[sharding](https://docs.cloud.google.com/bigquery/docs/partitioned-tables?hl=zh-tw#dt_partition_shard)，而非分割。

此外，BigQuery 不支援 `EXCHANGE PARTITION`、`SPLIT PARTITION`，也不支援將非分區資料表轉換為分區資料表。

### 分群

叢集有助於有效整理及擷取儲存在多個資料欄中的資料，這些資料通常會一起存取。不過，Oracle 和 BigQuery 的叢集功能最適合在不同情況下使用。在 BigQuery 中，如果資料表通常會使用特定資料欄進行篩選和匯總，請使用[叢集](https://docs.cloud.google.com/bigquery/docs/clustered-tables?hl=zh-tw)。從 Oracle 遷移[清單分區](https://docs.oracle.com/database/121/VLDBG/GUID-7221F7EC-4AFB-412F-8A4F-766CBE24CAE0.htm)或[索引組織](https://docs.oracle.com/cd/B28359_01/server.111/b28310/tables012.htm#ADMIN01506)資料表時，可以考慮使用叢集。

### 臨時資料表

Oracle ETL 管道經常使用暫時資料表。臨時資料表會在使用者工作階段期間保留資料，工作階段結束時，系統會自動刪除這類資料。

BigQuery 會使用臨時資料表，擷取未寫入永久資料表的查詢結果。查詢完成後，暫時性資料表最多會保留 24 小時。這些資料表會建立在特殊資料集中，並隨機命名。您也可以建立臨時資料表供自己使用。詳情請參閱[暫時性資料表](https://docs.cloud.google.com/bigquery/docs/multi-statement-queries?hl=zh-tw#temporary_tables)。

### 外部資料表

與 Oracle 類似，BigQuery 可讓您查詢[外部資料來源](https://docs.cloud.google.com/bigquery/external-data-sources?hl=zh-tw)。BigQuery 支援直接從外部資料來源查詢資料，包括：

* Amazon Simple Storage Service (Amazon S3)
* Azure Blob 儲存體
* Bigtable
* Spanner
* Cloud SQL
* Cloud Storage
* Google 雲端硬碟

### 建立資料模型

星狀或雪花資料模型可有效率地儲存分析資料，且通常用於 Oracle Exadata 上的資料倉儲。

反正規化資料表可避免耗費資源的聯結作業，而且在大多數情況下，BigQuery 的分析效能會更好。BigQuery 也支援星狀和雪花資料模型。如要進一步瞭解 BigQuery 資料倉儲設計，請參閱[設計結構定義](https://docs.cloud.google.com/solutions/bigquery-data-warehouse?hl=zh-tw#designing_schema)。

#### 列格式與欄格式，以及伺服器限制與無伺服器

Oracle 使用資料列格式，將資料表資料列儲存在資料區塊中，因此系統會根據特定資料欄的篩選和匯總作業，在區塊中擷取不必要的資料欄，以供分析查詢使用。

Oracle 採用「一切共用」架構，並將記憶體和儲存空間等固定硬體資源指派給伺服器。這兩大力量是許多資料模型技術的基礎，這些技術不斷演進，以提升儲存效率和分析查詢效能。星狀和雪花結構定義，以及資料保險庫建模就是其中幾種。

BigQuery 採用資料欄格式儲存資料，且沒有固定的儲存空間和記憶體限制。這個架構可讓您根據讀取作業和業務需求，進一步非正規化及設計結構定義，進而降低複雜度，並提升彈性、擴充性和效能。

#### 去標準化

關聯式資料庫正規化的主要目標之一是減少資料冗餘。雖然這個模型最適合使用列格式的關聯式資料庫，但資料去正規化更適合用於直欄式資料庫。如要進一步瞭解資料反正規化的優點，以及 BigQuery 中的其他查詢最佳化策略，請參閱「[反正規化](https://docs.cloud.google.com/bigquery/docs/migration/schema-data-overview?hl=zh-tw#denormalization)」一文。

#### 簡化現有結構定義的技巧

BigQuery 技術結合了資料欄資料存取和處理、記憶體內儲存空間，以及分散式處理，可提供優質的查詢效能。

設計 BigQuery DWH 結構定義時，以扁平資料表結構建立事實資料表 (將所有維度資料表整合到事實資料表中的單一記錄)，比使用多個 DWH 維度資料表更能有效利用儲存空間。除了減少儲存空間用量，在 BigQuery 中使用扁平資料表也能減少 `JOIN` 用量。下圖說明如何攤平結構定義。

#### 扁平化星形結構定義的範例

圖 1 顯示虛構的銷售管理資料庫，內含四個資料表：

* 訂單/銷售表格 (事實表格)
* 員工表格
* 門市表格
* 顧客表格

銷售資料表的主鍵是 `OrderNum`，其中也包含其他三個資料表的外鍵。

圖 1：星形結構定義中的銷售資料範例

#### 範例資料

**訂單/事實資料表內容**

| OrderNum | CustomerID | SalesPersonID | 金額 | Location |
| --- | --- | --- | --- | --- |
| O-1 | 1234 | 12 | 234.22 | 18 |
| O-2 | 4567 | 1 | 192.10 | 27 |
| O-3 |  | 12 | 14.66 | 18 |
| O-4 | 4567 | 4 | 182.00 | 26 |

**員工表格內容**

| SalesPersonID | FName | LName | title |
| --- | --- | --- | --- |
| 1 | Alex | Smith | 銷售助理 |
| 4 | Lisa | 陳 | 銷售助理 |
| 12 | John | 陳 | 銷售助理 |

**客戶資料表內容**

| CustomerID | FName | LName |
| --- | --- | --- |
| 1234 | Amanda | Lee |
| 4567 | Matt | Ryan |

**位置表格內容**

| Location | 城市 | 州 | 郵遞區號 |
| --- | --- | --- | --- |
| 18 | 布朗克斯 | NY | 10452 |
| 26 | 山景城 | CA | 90210 |
| 27 | 芝加哥 | IL | 60613 |

#### 使用 `LEFT OUTER JOIN` 將資料扁平化的查詢

```
#standardSQL
INSERT INTO flattened
SELECT
  orders.ordernum,
  orders.customerID,
  customer.fname,
  customer.lname,
  orders.salespersonID,
  employee.fname,
  employee.lname,
  employee.title,
  orders.amount,
  orders.location,
  location.city,
  location.state,
  location.zipcode
FROM orders
LEFT OUTER JOIN customer
  ON customer.customerID = orders.customerID
LEFT OUTER JOIN employee
  ON employee.salespersonID = orders.salespersonID
LEFT OUTER JOIN location
  ON location.locationID = orders.locationID
```

**注意：** BigQuery 會從左到右 (上到下) 處理 `JOIN`。在鏈結中盡早放置可減少記錄數量的 `JOIN`，有助於縮短回應時間，進而提升查詢效率。

#### 扁平化資料的輸出內容

| OrderNum | CustomerID | FName | LName | SalesPersonID | FName | LName | 金額 | 位置 | 城市 | 州 | 郵遞區號 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| O-1 | 1234 | Amanda | Lee | 12 | John | Doe | 234.22 | 18 | 布朗克斯 | NY | 10452 |
| O-2 | 4567 | Matt | Ryan | 1 | Alex | Smith | 192.10 | 27 | 芝加哥 | IL | 60613 |
| O-3 |  |  |  | 12 | John | Doe | 14.66 | 18 | 布朗克斯 | NY | 10452 |
| O-4 | 4567 | Matt | Ryan | 4 | Lisa | Doe | 182.00 | 26 | 山岳 查看 | CA | 90210 |

#### 巢狀和重複欄位

如要從關聯式結構定義設計及建立 DWH 結構定義 (例如包含維度和事實資料表的星形和雪花狀結構定義)，BigQuery 提供巢狀和重複欄位功能。因此，您可保留關聯式標準化 (或部分標準化) DWH 結構定義中的關係，且不會影響效能。詳情請參閱「[效能最佳做法](https://docs.cloud.google.com/bigquery/docs/best-practices-performance-input?hl=zh-tw#denormalize_data_whenever_possible)」。

如要進一步瞭解如何實作巢狀和重複欄位，請查看 `CUSTOMERS` 資料表和 `ORDER`/`SALES` 資料表的簡單關係結構定義。這兩個資料表各代表一個實體，而關係是使用主鍵和外鍵等索引鍵定義，做為資料表之間的連結，同時使用 `JOIN` 查詢。BigQuery 巢狀和重複欄位可讓您在單一資料表中，保留實體之間的相同關係。如要實作這項功能，請提供所有顧客資料，並為每位顧客巢狀顯示訂單資料。詳情請參閱[指定巢狀和重複的欄位](https://docs.cloud.google.com/bigquery/docs/nested-repeated?hl=zh-tw)。

如要將扁平結構轉換為巢狀或重複結構定義，請依下列方式將欄位設為巢狀：

* `CustomerID`、`FName`、`LName` 巢狀結構，並納入名為 `Customer` 的新欄位。
* `SalesPersonID`、`FName`、`LName` 巢狀結構，並納入名為「`Salesperson`」的新欄位。
* `LocationID`、`city`、`state`、`zip code` 巢狀結構，並納入名為 `Location` 的新欄位。

`OrderNum` 和 `amount` 欄位不會巢狀化，因為它們代表不重複的元素。

您希望架構夠彈性，讓每個訂單都能有多位顧客：主要和次要。顧客欄位標示為重複。圖 2 顯示產生的結構定義，說明巢狀和重複的欄位。

圖 2：巢狀結構的邏輯表示法

在某些情況下，使用巢狀和重複欄位進行去標準化並無法提升效能。如要進一步瞭解限制，請參閱[在資料表結構定義中指定巢狀與重複的資料欄](https://docs.cloud.google.com/bigquery/docs/nested-repeated?hl=zh-tw)。

#### 替代鍵

通常會使用資料表中的不重複索引鍵來識別資料列。Oracle 通常會使用序列來建立這些金鑰。在 BigQuery 中，您可以使用 `row_number` 和 `partition by` 函式建立替代鍵。詳情請參閱「[BigQuery and surrogate keys: a practical approach](https://cloud.google.com/blog/products/data-analytics/bigquery-and-surrogate-keys-practical-approach?hl=zh-tw)」(BigQuery 和替代鍵：實用方法)。

#### 追蹤變更和記錄

規劃 BigQuery DWH 遷移作業時，請考量緩慢變更的維度 (SCD) 概念。一般來說，SCD 一詞是指在維度資料表中進行變更 (DML 作業) 的程序。

傳統資料倉儲會基於多種原因，使用[不同類型](https://en.wikipedia.org/wiki/Slowly_changing_dimension)來處理資料變更，並在緩慢變動維度中保留歷來資料。如先前所述，這些型別用法是因應硬體限制和效率需求而生。由於儲存空間比運算便宜許多，而且可無限擴充，因此如果資料備援和重複可加快 BigQuery 的查詢速度，建議您採用這種做法。您可以使用[資料快照技術](https://medium.com/%40maximebeauchemin/functional-data-engineering-a-modern-paradigm-for-batch-data-processing-2327ec32c42a)，將所有資料載入新的每日分區。

#### 角色專屬和使用者專屬檢視畫面

如果使用者屬於不同團隊，且只需要查看所需的記錄和結果，請使用角色專屬和使用者專屬的檢視畫面。

BigQuery 支援[column-](https://docs.cloud.google.com/bigquery/docs/column-level-security-intro?hl=zh-tw)和[資料列層級安全防護機制](https://docs.cloud.google.com/bigquery/docs/row-level-security-intro?hl=zh-tw)。資料欄層級安全防護機制透過政策標記或依據類型的資料分類方式，對機密資料欄提供精細的存取權限。資料列層級安全防護機制：可根據符合資格的使用者條件篩選資料，並允許存取資料表中的特定資料列。

## 資料遷移

本節將說明如何從 Oracle 遷移資料至 BigQuery，包括初始載入、變更資料擷取 (CDC)，以及 ETL/ELT 工具和方法。

### 遷移活動

建議您先找出適合遷移的用途，然後分階段執行遷移作業。您可以使用多種工具和服務，將資料從 Oracle 遷移至 Google Cloud。這份清單並未詳列所有項目，但可讓您瞭解遷移作業的規模和範圍。

* **從 Oracle 匯出資料：**詳情請參閱[初始載入](#initial_load)和[從 Oracle 到 BigQuery 的 CDC 和串流擷取](#cdc-streaming-oracle-bigquery)。[ETL 工具](#etl-elt-migration)可用於初始載入。
* **資料暫存 (在 Cloud Storage 中)：**建議您將從 Oracle 匯出的資料暫存於 Cloud Storage。Cloud Storage 的設計宗旨是快速且彈性地擷取結構化或非結構化資料。
* **ETL 程序：**詳情請參閱「[ETL/ELT 遷移](#etl-elt-migration)」。
* **直接將資料載入 BigQuery：**您可以透過 Dataflow 或即時串流，直接從 Cloud Storage 將資料載入 BigQuery。需要轉換資料時，請使用 Dataflow。

### 初始載入

視資料大小和網路頻寬而定，將現有 Oracle 資料倉儲的初始資料遷移至 BigQuery，可能與增量 ETL/ELT 管道不同。如果資料大小為幾 TB，可以使用相同的 ETL/ELT 管道。

如果資料量最多只有幾 TB，傾印資料並使用 `gcloud storage` 進行轉移，會比使用 [JdbcIO](https://beam.apache.org/releases/javadoc/current/org/apache/beam/sdk/io/jdbc/JdbcIO.html) 類似的程式輔助資料庫擷取方法有效率得多，因為程式輔助方法可能需要更精細的效能調整。如果資料大小超過幾 TB，且資料儲存在雲端或線上儲存空間 (例如 Amazon Simple Storage Service (Amazon S3))，建議使用 [BigQuery 資料移轉服務](https://docs.cloud.google.com/bigquery/docs/dts-introduction?hl=zh-tw)。對於大規模移轉作業 (尤其是網路頻寬受限的移轉作業)，[Transfer Appliance](https://docs.cloud.google.com/transfer-appliance?hl=zh-tw) 是實用的選項。

#### 初始載入的限制

規劃資料遷移作業時，請注意下列事項：

* **Oracle DWH 資料大小：**結構定義的來源大小對所選資料移轉方法有重大影響，尤其是在資料量龐大 (TB 以上) 時。如果資料量相對較小，資料轉移程序可以簡化。處理大規模資料會使整體程序更加複雜。
* **停機時間：**決定是否要停機，是將資料遷移至 BigQuery 的重要環節。為減少停機時間，您可以大量載入穩定的歷來資料，並使用 CDC 解決方案，趕上轉移程序期間發生的變更。
* **價格：**在某些情況下，您可能需要第三方整合工具 (例如 ETL 或複製工具)，這類工具需要額外授權。

#### 初始資料移轉 (批次)

使用批次方法進行資料移轉表示資料會以單一程序匯出 (例如將 Oracle DWH 結構定義資料匯出至 CSV、Avro 或 Parquet 檔案，或匯入 Cloud Storage 以在 BigQuery 上建立資料集)。您可以使用 [ETL/ELT 遷移作業](#etl-elt-migration)中說明的所有 ETL 工具和概念，進行初始載入。

如果不想使用 ETL/ELT 工具進行初始載入，可以編寫自訂指令碼，將資料匯出至檔案 (CSV、Avro 或 Parquet)，然後使用 `gcloud storage`、BigQuery 資料移轉服務或 Transfer Appliance，將資料上傳至 Cloud Storage。如要進一步瞭解如何調整大型資料移轉作業和移轉選項的效能，請參閱[轉移大型資料集](https://docs.cloud.google.com/solutions/transferring-big-data-sets-to-gcp?hl=zh-tw)。然後將資料從 Cloud Storage 載入 [BigQuery](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)。

Cloud Storage 非常適合處理資料的初始登陸。
Cloud Storage 是高可用性且耐用的物件儲存服務，檔案數量沒有限制，而且只會收取您使用的儲存空間費用。這項服務經過最佳化，可與 BigQuery 和 Dataflow 等其他 Google Cloud 服務搭配使用。

### 透過 CDC 和串流擷取功能，將資料從 Oracle 移至 BigQuery

您可以透過多種方式擷取 Oracle 中的變更資料，每個選項都有取捨之處，主要在於對來源系統的效能影響、開發和設定需求，以及定價和授權。

#### 以記錄為基礎的 CDC

Oracle 建議使用 Oracle GoldenGate 擷取重做記錄，並使用 [GoldenGate for Big Data](https://docs.oracle.com/en/middleware/goldengate/big-data/12.3.2.1/gadbd/using-bigquery-handler.html#GUID-4568CD10-5495-4DB0-8E75-10F40451A8A7) 將記錄串流到 BigQuery。GoldenGate 需採用 CPU 授權。如要瞭解價格，請參閱 [Oracle Technology Global Price List](https://www.oracle.com/assets/technology-price-list-070617.pdf)。如果可以使用 Oracle GoldenGate for B