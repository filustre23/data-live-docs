* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [參考資料](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 從 IBM Netezza 遷移

本文提供從 IBM Netezza 遷移至 BigQuery 的高階指南。本文說明 Netezza 和 BigQuery 之間的基本架構差異，以及 BigQuery 提供的額外功能。此外，這份指南也說明如何重新思考現有的資料模型，以及擷取、轉換和載入 (ETL) 程序，以充分發揮 BigQuery 的優勢。

本文適用於企業架構師、資料庫管理員、應用程式開發人員和 IT 安全專業人員，協助他們從 Netezza 遷移至 BigQuery，並解決遷移過程中的技術難題。本文將詳細說明遷移程序的下列階段：

* 正在匯出資料
* 擷取資料
* 善用第三方工具

您也可以使用[批次 SQL 翻譯](https://docs.cloud.google.com/bigquery/docs/batch-sql-translator?hl=zh-tw)大量遷移 SQL 指令碼，或使用[互動式 SQL 翻譯](https://docs.cloud.google.com/bigquery/docs/interactive-sql-translator?hl=zh-tw)翻譯臨時查詢。這兩項工具的[預先發布](https://cloud.google.com/products?hl=zh-tw#product-launch-stages)版本都支援 Netezza SQL/NZPLSQL。

## 架構比較

Netezza 是一套功能強大的系統，可協助您儲存及分析大量資料。不過，Netezza 這類系統需要投入大量資金，才能取得硬體、維護和授權。由於節點管理、每個來源的資料量和封存成本等問題，這類資料庫難以擴充。使用 Netezza 時，儲存空間和處理容量會受到硬體設備限制。達到最高用量後，擴充設備容量的程序會很複雜，有時甚至無法擴充。

使用 BigQuery 時，您不必管理基礎架構，也不需要資料庫管理員。BigQuery 是全代管的無伺服器資料倉儲，規模可達 PB 級，能在數十秒內掃描數十億個資料列，且不需要索引。由於 BigQuery 共用 Google 的基礎架構，因此可以平行處理每個查詢，並在數萬部伺服器上同時執行。下列核心技術是 BigQuery 的獨到之處：

* **資料欄儲存空間。**資料是以資料欄而非資料列的形式儲存，因此可達到極高的壓縮比和掃描處理量。
* **靈樹架構。**查詢會傳送至數千部電腦，並在幾秒內匯總結果。

### Netezza 架構

Netezza 是硬體加速裝置，隨附軟體資料抽象層。資料抽象層會管理設備中的資料分配情形，並在基礎 CPU 和 FPGA 之間分配資料處理作業，藉此最佳化查詢。

Netezza TwinFin 和 Striper 型號已於 2019 年 6 月停止支援。

下圖說明 Netezza 中的資料抽象層：

下圖顯示下列資料抽象層：

* **磁碟外殼。**設備內安裝磁碟的實體空間。
* **磁碟**。磁碟機殼內的實體硬碟會儲存資料庫和資料表。
* **資料切片。**儲存在磁碟上的資料邏輯表示法。
  資料會使用分配鍵分配到各個資料切片。您可以使用 `nzds` 指令監控資料切片的狀態。
* **資料分割區。**由特定[程式碼片段處理單元 (SPU)](https://www.ibm.com/support/knowledgecenter/en/SSULQD_7.2.1/com.ibm.nz.adm.doc/r_sysadm_nz_hardware_components.html) 管理的資料切片邏輯表示法。每個 SPU 都擁有一個或多個資料分割區，其中包含 SPU 在查詢期間負責處理的使用者資料。

所有系統元件都透過網路結構互連。Netezza 設備會根據 IP 位址執行自訂通訊協定。

### BigQuery 架構

BigQuery 是全代管的企業資料倉儲，內建機器學習、地理空間分析和商業智慧等功能，有助於管理及分析資料。詳情請參閱「[BigQuery 總覽](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)」一文。

BigQuery 會處理儲存空間和運算作業，提供耐久的資料儲存空間，並針對分析查詢提供高效能的回應。詳情請參閱「[BigQuery 說明](https://cloud.google.com/blog/products/data-analytics/new-blog-series-bigquery-explained-overview?hl=zh-tw)」一文。

如要瞭解 BigQuery 定價，請參閱「[瞭解 BigQuery 的快速擴充和簡單定價](https://cloud.google.com/blog/products/gcp/understanding-bigquerys-rapid-scaling-and-simple-pricing?hl=zh-tw)」一文。

## 遷移前

為確保資料倉儲遷移作業順利完成，請在專案時間軸的早期，開始規劃遷移策略。如要瞭解如何有系統地規劃遷移作業，請參閱「[遷移的內容和方式：遷移作業架構](https://docs.cloud.google.com/bigquery/docs/migration/migration-overview?hl=zh-tw#what_and_how_to_migrate_the_migration_framework)」。

### BigQuery 容量規劃

BigQuery 中的 Analytics 處理量是以「運算單元」為單位。BigQuery 運算單元是 Google 的專屬運算單位，代表執行 SQL 查詢所需的運算、RAM 和網路輸送量。BigQuery 會依據查詢的大小和複雜程度，自動計算各項查詢所需的運算單元數量。

如要在 BigQuery 中執行查詢，請選取下列其中一種計費模式：

* **[隨選](https://cloud.google.com/bigquery/pricing?hl=zh-tw#on_demand_pricing)。**預設定價模式，系統會根據各項查詢處理作業的位元組數向您收費。
* **[以容量為準的價格](https://cloud.google.com/bigquery/pricing?hl=zh-tw#capacity_compute_analysis_pricing)。**您必須購買運算單元，也就是虛擬 CPU。購買運算單元時，您必須購買可用於執行查詢的專用處理容量。運算單元的使用承諾方案如下：
  + **按年**。承諾至少使用 365 天。
  + **三年。**承諾至少使用 365\*3 天。

BigQuery 運算單元與 Netezza SPU 有些相似之處，例如 CPU、記憶體和資料處理，但兩者並非相同的測量單位。Netezza SPU 會固定對應至基礎硬體元件，而 BigQuery 運算單元則代表用於執行查詢的虛擬 CPU。為協助估算配額，建議您[使用 Cloud Monitoring 設定 BigQuery 監控](https://docs.cloud.google.com/bigquery/docs/monitoring?hl=zh-tw)，並[使用 BigQuery 分析稽核記錄](https://docs.cloud.google.com/bigquery/audit-logs?hl=zh-tw)。如要將 BigQuery 運算單元使用率視覺化，您也可以使用 [數據分析](https://datastudio.google.com/c/?hl=zh-tw) 或 [Looker](https://docs.cloud.google.com/looker?hl=zh-tw) 等工具。定期監控及分析使用配額，有助於估算貴機構在 Google Cloud成長時所需的配額總數。

舉例來說，假設您一開始保留 2,000 個 BigQuery [運算單元](https://docs.cloud.google.com/bigquery/docs/slots?hl=zh-tw)，同時執行 50 個中等複雜度的查詢。如果查詢持續執行超過數小時，且資訊主頁顯示運算單元使用率偏高，則查詢可能未經過最佳化，或是您可能需要額外的 BigQuery 運算單元，才能支援工作負載。如要自行購買運算單元，並簽訂一年或三年期承諾，請使用 Google Cloud 控制台或 bq 指令列工具[建立 BigQuery 預留](https://docs.cloud.google.com/bigquery/docs/reservations-get-started?hl=zh-tw)。如果您是透過簽署離線協議的方式購買容量方案，您的方案內容可能會不同於此處所述的詳細資料。

如要瞭解如何控管 BigQuery 的儲存空間和查詢處理費用，請參閱「[最佳化工作負載](https://docs.cloud.google.com/bigquery/docs/admin-intro?hl=zh-tw#optimize_workloads)」。

### Google Cloud的安全防護

以下各節將說明常見的 Netezza 安全控管措施，以及如何協助保護環境中的資料倉儲。 Google Cloud

#### 身分與存取權管理

Netezza 資料庫包含一組完全整合的系統[存取控管功能](https://www.ibm.com/support/knowledgecenter/en/SSULQD_7.2.1/com.ibm.nz.adm.doc/c_sysadm_nz_db_users_and_groups.html)，可讓使用者存取授權資源。

存取 Netezza 的權限是透過網路控管，方法是管理可登入作業系統的 Linux 使用者帳戶。Netezza 資料庫、物件和工作存取權，是透過 Netezza 資料庫使用者帳戶管理，這些帳戶可與系統建立 SQL 連線。

BigQuery 使用 Google 的[身分與存取權管理 (IAM)](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw) 服務，管理資源的存取權。BigQuery 提供的資源類型包括機構、專案、資料集、資料表和檢視表。在 IAM 政策階層中，資料集是專案的子項資源。資料表會繼承所屬資料集的權限。

如要授予資源的存取權，請將一或多個角色指派給使用者、群組或服務帳戶。機構和專案角色可控管執行作業或管理專案的存取權，而資料集角色則可控管專案內資料的檢視或修改權限。

IAM 提供下列類型的角色：

* **[預先定義的角色](https://docs.cloud.google.com/iam/docs/choose-predefined-roles?hl=zh-tw)。**支援常見用途和存取控管模式。
* **[基本角色](https://docs.cloud.google.com/bigquery/docs/access-control-primitive-roles?hl=zh-tw)。**包括「擁有者」、「編輯者」和「檢視者」角色。基本角色提供特定服務的精細存取權，並由 Google Cloud管理。
* **[自訂角色](https://docs.cloud.google.com/iam/docs/understanding-custom-roles?hl=zh-tw)**。根據使用者指定的權限清單，提供精細的存取權限。

當您同時把預先定義角色和基本角色指派給某個使用者時，您授予的權限就是這兩個角色權限的聯集。

#### 資料列層級安全性

多層級安全防護是一種抽象安全模型，Netezza 會使用這個模型定義規則，控管使用者對[資料列安全防護表 (RST)](https://www.ibm.com/support/knowledgecenter/en/SSULQD_7.2.1/com.ibm.nz.adv.doc/c_advsec_mls_and_row_secure_tables.html) 的存取權。資料列安全表格是指資料庫表格，其中資料列附有安全標籤，可篩除沒有適當權限的使用者。查詢傳回的結果會因查詢使用者的權限而異。

如要在 BigQuery 中實現資料列層級安全防護機制，可以使用[授權檢視畫面](https://docs.cloud.google.com/bigquery/docs/authorized-views?hl=zh-tw)和[資料列層級存取權政策](https://docs.cloud.google.com/bigquery/docs/managing-row-level-security?hl=zh-tw)。如要進一步瞭解如何設計及導入這些政策，請參閱「[BigQuery 資料列層級安全防護機制簡介](https://docs.cloud.google.com/bigquery/docs/row-level-security-intro?hl=zh-tw)」。

#### 資料加密

Netezza 設備使用[自我加密硬碟 (SED)](https://www.ibm.com/support/knowledgecenter/en/SSULQD_7.2.1/com.ibm.nz.adm.doc/c_sysadm_sed_drives.html)，可提升安全性，並保護儲存在設備中的資料。SED 會在資料寫入磁碟時加密。每個磁碟都有出廠時設定並儲存在磁碟中的磁碟加密金鑰 (DEK)。磁碟會使用 DEK 加密寫入的資料，並在從磁碟讀取資料時解密。磁碟的運作方式，以及加密和解密程序，對讀取及寫入資料的使用者而言都是透明的。這個預設加密和解密模式稱為「安全清除模式」。

在安全清除模式下，您不需要驗證金鑰或密碼，即可解密及讀取資料。如果磁碟必須重新用途或因支援或保固原因退回，SED 可提供改良功能，簡化並快速安全地清除資料。

Netezza 使用對稱式加密；如果您的資料經過欄位層級加密，可以使用下列解密函式讀取及匯出資料：

```
varchar = decrypt(varchar text, varchar key [, int algorithm [, varchar IV]]);
nvarchar = decrypt(nvarchar text, nvarchar key [, int algorithm[, varchar IV]]);
```

BigQuery 儲存的所有資料都會經過靜態加密。如果您想自行控管加密作業，可以針對 BigQuery 使用客戶代管的加密金鑰 (CMEK)。使用 CMEK 時，您可以在 [Cloud Key Management Service](https://docs.cloud.google.com/kms/docs?hl=zh-tw) 中控制及管理用來保護您資料的金鑰加密金鑰，而不是由 Google 管理。詳情請參閱「[靜態資料加密](https://docs.cloud.google.com/bigquery/docs/encryption-at-rest?hl=zh-tw)」。

### 成效基準

如要在整個遷移過程中追蹤進度和改善情況，請務必為目前的 Netezza 環境建立基準效能。如要建立基準，請選取一組代表性查詢，這些查詢是從使用中的應用程式 (例如 Tableau 或 Cognos) 擷取而來。

| **環境** | **Netezza** | **BigQuery** |
| --- | --- | --- |
| 資料大小 | *size* TB | - |
| 查詢 1：*name* (完整資料表掃描) | *mm:ss.ms* | - |
| 查詢 2：*name* | *mm:ss.ms* | - |
| 查詢 3：*name* | *mm:ss.ms* | - |
| 總計 | *mm:ss.ms* | - |

### 基礎專案設定

佈建儲存空間資源以遷移資料前，請先完成專案設定。

* 如要在專案層級設定專案並啟用 IAM，請參閱 [Google Cloud Well-Architected Framework](https://docs.cloud.google.com/architecture/framework?hl=zh-tw)。
* 如要設計基礎資源，讓雲端部署作業符合企業需求，請參閱「 [Google Cloud中的登陸區設計](https://docs.cloud.google.com/architecture/landing-zones?hl=zh-tw)」。
* 如要瞭解將地端部署資料倉儲遷移至 BigQuery 時所需的資料治理和控管機制，請參閱「[資料安全性與資料治理總覽](https://docs.cloud.google.com/bigquery/docs/data-governance?hl=zh-tw)」。

### 網路連線

地端部署資料中心 (Netezza 執行個體所在位置) 與 Google Cloud環境之間必須有可靠且安全的網路連線。如要瞭解如何協助確保連線安全，請參閱「[BigQuery 資料治理簡介](https://docs.cloud.google.com/bigquery/docs/data-governance?hl=zh-tw)」。上傳資料擷取內容時，網路頻寬可能會成為限制因素。如要瞭解如何滿足資料移轉需求，請參閱「[增加網路頻寬](https://docs.cloud.google.com/architecture/migration-to-google-cloud-transferring-your-large-datasets?hl=zh-tw#increasing_network_bandwidth)」。

### 支援的資料類型和屬性

Netezza 資料類型與 BigQuery 資料類型不同。如要進一步瞭解 BigQuery 資料類型，請參閱「[資料類型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw)」。如需 Netezza 和 BigQuery 資料類型之間的詳細比較，請參閱 [IBM Netezza SQL 翻譯指南](https://docs.cloud.google.com/bigquery/docs/migration/netezza-sql?hl=zh-tw)。

### SQL 比較

Netezza 資料 SQL 包含 DDL、DML 和 Netezza 專用的資料控制語言 (DCL)，與 GoogleSQL 不同。[GoogleSQL](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql?hl=zh-tw) 與 SQL 2011 標準相容，並具備查詢巢狀和重複資料的擴充功能。如果您使用 BigQuery 舊版 SQL，請參閱[舊版 SQL 函式和運算子](https://docs.cloud.google.com/bigquery/query-reference?hl=zh-tw)。如要詳細比較 Netezza SQL 和 BigQuery SQL 及函式，請參閱 [IBM Netezza SQL 翻譯指南](https://docs.cloud.google.com/bigquery/docs/migration/netezza-sql?hl=zh-tw)。

如要協助遷移 SQL 程式碼，請使用[批次 SQL 翻譯](https://docs.cloud.google.com/bigquery/docs/batch-sql-translator?hl=zh-tw)大量遷移 SQL 程式碼，或使用[互動式 SQL 翻譯](https://docs.cloud.google.com/bigquery/docs/interactive-sql-translator?hl=zh-tw)翻譯臨時查詢。

### 函式比較

請務必瞭解 Netezza 函式如何對應至 BigQuery 函式。舉例來說，Netezza `Months_Between` 函式會輸出十進位數，而 BigQuery `DateDiff` 函式則會輸出整數。因此，您必須使用[自訂 UDF 函式](#replacing_months_between)輸出正確的資料類型。如要詳細比較 Netezza SQL 和 GoogleSQL 函式，請參閱 [IBM Netezza SQL 翻譯指南](https://docs.cloud.google.com/bigquery/docs/migration/netezza-sql?hl=zh-tw)。

## 資料遷移

如要將資料從 Netezza 遷移至 BigQuery，請先從 Netezza 匯出資料，然後在 Google Cloud上傳輸及暫存資料，最後將資料載入 BigQuery。本節將概略說明資料遷移程序。如要詳細瞭解資料遷移程序，請參閱「[結構定義和資料遷移程序](https://docs.cloud.google.com/bigquery/docs/migration/schema-data-overview?hl=zh-tw#schema_and_data_migration_process)」。如需 Netezza 和 BigQuery 支援的資料類型詳細比較，請參閱 [IBM Netezza SQL 翻譯指南](https://docs.cloud.google.com/bigquery/docs/migration/netezza-sql?hl=zh-tw)。

### 從 Netezza 匯出資料

如要從 Netezza 資料庫表格匯出資料，建議您匯出至 CSV 格式的外部表格。詳情請參閱「[將資料卸載至遠端用戶端系統](https://www.ibm.com/docs/en/psfa/7.2.1?topic=tables-unloading-data-remote-client-system)」。您也可以使用 JDBC/ODBC 連接器，透過 Informatica 等第三方系統 (或自訂 ETL) 讀取資料，產生 CSV 檔案。

Netezza 僅支援匯出每個資料表的未壓縮平面檔案 (CSV)。不過，如果匯出大型資料表，未壓縮的 CSV 檔案可能會非常大。如有可能，請考慮將 CSV 轉換為可辨識結構定義的格式，例如 Parquet、Avro 或 ORC，這樣匯出的檔案會較小，可靠性也較高。如果只有 CSV 格式可用，建議您先壓縮匯出檔案，縮減檔案大小，再上傳至 Google Cloud。縮減檔案大小有助於加快上傳速度，並提高傳輸可靠性。如果將檔案轉移至 Cloud Storage，您可以在 [`gcloud storage cp` 指令](https://docs.cloud.google.com/sdk/gcloud/reference/storage/cp?hl=zh-tw)中使用 `--gzip-local` 旗標，在檔案上傳前壓縮檔案。

### 資料移轉和暫存

匯出資料後，必須將資料轉移並暫存到Google Cloud。根據轉移的資料量和可用的網路頻寬，您可以選擇以下移轉選項：詳情請參閱「[結構定義與資料移轉總覽](https://docs.cloud.google.com/bigquery/docs/migration/schema-data-overview?hl=zh-tw)」。

使用 Google Cloud CLI 時，您可以自動化並平行處理檔案轉移至 Cloud Storage 的作業。為加快載入 BigQuery 的速度，請將檔案大小限制為 4 TB (未壓縮)。不過，您必須事先匯出結構定義。這是使用分區和分群功能，將 BigQuery 最佳化的好機會。

使用 [`gcloud storage bucket create`](https://docs.cloud.google.com/sdk/gcloud/reference/storage/buckets/create?hl=zh-tw) 建立暫存值區，儲存匯出的資料，並使用 [`gcloud storage cp`](https://docs.cloud.google.com/sdk/gcloud/reference/storage/cp?hl=zh-tw) 將資料匯出檔案傳輸至 Cloud Storage 值區。

gcloud CLI 會自動執行複製作業，並結合多執行緒和多重處理。

### 將資料載入 BigQuery

資料在 Google Cloud中暫存後，您可以選擇幾種方式將資料載入 BigQuery。詳情請參閱「[將結構定義和資料載入 BigQuery](https://docs.cloud.google.com/bigquery/docs/migration/schema-data-overview?hl=zh-tw#loading_the_data_into_bigquery)」。

### 合作夥伴工具和支援

您可以在遷移過程中取得合作夥伴支援。如要協助遷移 SQL 程式碼，請使用[批次 SQL 轉譯](https://docs.cloud.google.com/bigquery/docs/batch-sql-translator?hl=zh-tw)大量遷移 SQL 程式碼。

許多 Google Cloud 合作夥伴也提供資料倉儲遷移服務。如需合作夥伴及其提供的解決方案清單，請參閱「[與具備 BigQuery 專業知識的夥伴合作](https://docs.cloud.google.com/bigquery?hl=zh-tw#partners-and-integration)」。

## 遷移後

資料遷移完成後，您就可以開始最佳化Google Cloud 的使用方式，解決業務需求。例如使用Google Cloud的探索和視覺化工具，為業務利害關係人取得洞察資料、[改善成效不佳的查詢](https://docs.cloud.google.com/bigquery/docs/best-practices-performance-overview?hl=zh-tw)，或是開發有助於使用者採用的程式。

### 透過網際網路連線至 BigQuery API

下圖顯示外部應用程式如何使用 API 連線至 BigQuery：

下圖顯示下列步驟：

1. 在 Google Cloud中，系統會建立具備 IAM 權限的服務帳戶。服務帳戶金鑰會以 JSON 格式產生，並複製到前端伺服器 (例如 MicroStrategy)。
2. 前端會讀取金鑰，並透過 HTTPS 向 Google API 要求 OAuth 權杖。
3. 前端接著會將 BigQuery 要求連同權杖傳送至 BigQuery。

詳情請參閱「[授權 API 要求](https://docs.cloud.google.com/bigquery/docs/authorization?hl=zh-tw)」。

### 針對 BigQuery 進行最佳化

GoogleSQL 支援 SQL 2011 標準，並具備擴充功能，可查詢[巢狀和重複資料](https://docs.cloud.google.com/bigquery/docs/arrays?hl=zh-tw#querying_nested_arrays)。[最佳化 BigQuery 查詢](https://docs.cloud.google.com/bigquery/docs/best-practices-performance-overview?hl=zh-tw)是提升效能和縮短回應時間的關鍵。

#### 在 BigQuery 中以 UDF 取代 Months\_Between 函式

Netezza 會將一個月的天數視為 31 天。下列自訂 UDF 會以接近準確度重新建立 Netezza 函式，您可以從查詢中呼叫該函式：

```
CREATE TEMP FUNCTION months_between(date_1 DATE, date_2 DATE)
AS (
  CASE
    WHEN date_1 = date_2
      THEN 0
    WHEN EXTRACT(DAY FROM DATE_ADD(date_1, INTERVAL 1 DAY)) = 1
      AND EXTRACT(DAY FROM DATE_ADD(date_2, INTERVAL 1 DAY)) = 1
      THEN date_diff(date_1,date_2, MONTH)
    WHEN EXTRACT(DAY FROM date_1) = 1
      AND EXTRACT(DAY FROM DATE_ADD(date_2, INTERVAL 1 DAY)) = 1
      THEN date_diff(DATE_ADD(date_1, INTERVAL -1 DAY), date_2, MONTH) + 1/31
    ELSE date_diff(date_1, date_2, MONTH) - 1 + ((EXTRACT(DAY FROM date_1) + (31 - EXTRACT(DAY FROM date_2))) / 31)
    END
);
```

#### 遷移 Netezza 預存程序

如果您在 ETL 工作負載中使用 Netezza 儲存程序建構事實資料表，就必須將這些儲存程序遷移至與 BigQuery 相容的 SQL 查詢。Netezza 會使用 NZPLSQL 指令碼語言處理預存程序。NZPLSQL 是以 Postgres PL/pgSQL 語言為基礎。詳情請參閱 [IBM Netezza SQL 翻譯指南](https://docs.cloud.google.com/bigquery/docs/migration/netezza-sql?hl=zh-tw)。

#### 自訂 UDF，模擬 Netezza ASCII

下列 BigQuery 自訂 UDF 可修正資料欄中的編碼錯誤：

```
CREATE TEMP FUNCTION ascii(X STRING)
AS (TO_CODE_POINTS(x)[ OFFSET (0)]);
```

## 後續步驟

* 瞭解如何[最佳化工作負載](https://docs.cloud.google.com/bigquery/docs/admin-intro?hl=zh-tw#optimize_workloads)，全面提升效能並降低成本。
* 瞭解如何[在 BigQuery 中最佳化儲存空間](https://docs.cloud.google.com/bigquery/docs/best-practices-storage?hl=zh-tw)。
* 請參閱 [IBM Netezza SQL 翻譯指南](https://docs.cloud.google.com/bigquery/docs/migration/netezza-sql?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-04-29 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-04-29 (世界標準時間)。"],[],[]]