* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [資源](https://docs.cloud.google.com/bigquery/docs/release-notes?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 在 BigQuery 上處理多租戶工作負載的最佳做法

本文提供多租戶資料平台和企業資料市集常用模式的技術和最佳做法。

商業企業、軟體即服務 (SaaS) 供應商和政府機構通常必須跨越地理和行政界線，安全地託管內部和第三方資料。[BigQuery](https://docs.cloud.google.com/bigquery?hl=zh-tw) 是功能強大的工具，可持續滿足多租戶平台的需求，處理來自不同業務部門的 EB 級資料，並供數十萬名資料消費者使用。本文適用於在 BigQuery 上部署多租戶平台的機構，以及想瞭解可用的[存取權控管](https://docs.cloud.google.com/bigquery/docs/data-governance?hl=zh-tw)和[效能管理功能](https://docs.cloud.google.com/bigquery/docs/best-practices-performance-overview?hl=zh-tw)的機構。

多租戶平台建構人員通常需要兼顧下列考量事項：

* **資料隔離**：實施嚴格的控管措施，防止資料在不同房客之間外洩。
* **效能穩定**：設定及分配 [BigQuery 保留項目](https://docs.cloud.google.com/bigquery/docs/reservations-intro?hl=zh-tw)，確保所有租戶的效能穩定。
* **資源管理**：規劃配額和限制的影響。
* **地理分布**：在指定和必要的[地理位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw#multi-regions)尋找資料。如要瞭解法規遵循相關問題，請參閱 Google Cloud的[法規遵循服務](https://cloud.google.com/security/compliance/offerings?hl=zh-tw)。
* **稽核與安全性**：保護租戶資料，避免遭到不當存取和外洩。
* **費用管理**：確保每個租戶的 BigQuery 費用一致。
* **作業複雜度**：盡量減少代管新房客所需的系統變異量。

## 提供共用租戶基礎架構的軟體即服務 (SaaS) 供應商

代管第三方資料的 SaaS 供應商必須確保所有客戶的可靠性和隔離性。這類客戶可能多達數萬人，且客戶資料可能透過共用服務基礎架構存取。部分 SaaS 供應商也會維護經過清理的中央資料儲存庫，以便對整個租戶機群進行數據分析。

每個房客都有專屬的資料集，有助於減輕機構在擴充至數千名房客時，會遇到的下列問題：

* **管理作業複雜度**：以每位客戶為單位，計算新專案和雲端資源的總數
* **端對端延遲時間**：資料存放區的最新狀態，適用於租戶和跨客戶分析解決方案
* **效能預期**：確保租戶效能維持在可接受的範圍內

### 為每個租戶設定資料集

在專門用於儲存客戶資料的專案中，每位客戶的資料都會以 BigQuery 資料集分隔。在主機機構中，您可以使用第二個專案，對合併的客戶資料部署分析和機器學習。接著，您可以將資料處理引擎 [Dataflow](https://docs.cloud.google.com/dataflow?hl=zh-tw) 設定為將傳入資料雙重寫入內部和租戶專屬資料表。Dataflow 設定會使用完整寫入的資料表，而非授權檢視區塊。使用完整編寫的資料表，可統一處理地理分布，並避免在租戶數量擴增時達到[授權檢視限制](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#view_limits)。

BigQuery 將儲存空間和[運算資源](https://docs.cloud.google.com/bigquery/docs/slots?hl=zh-tw)分隔，因此與叢集式倉儲相比，您只需設定較少的專案，即可處理服務層級和資料隔離等問題。如果不需要使用額外的[專屬雲端](#saas-dedicated)資源設定租戶，建議您考慮為每個租戶設定專屬資料集的預設設定。下圖顯示根據這項建議設計的範例專案設定：

**圖 1.** 隨著租戶數量增加，處理資料和處理需求時，專案數量維持不變。

圖 1 中的專案設定包含下列專案：

* **資料管道專案**：接收、處理及發布租戶資料的核心基礎架構元件，全都會封裝到單一專案中。
* **合併租戶資料專案**：核心資料專案，負責維護每個客戶的資料集。租戶資料應透過運算層級專案存取。
* **內部開發專案**：代表分析團隊用來評估租戶資料和建構新功能的自我管理資源。
* **使用者應用程式專案**：內含專為與使用者互動而設計的資源。建議您使用租戶範圍的服務帳戶存取租戶資料集，並使用穩固安全的[建構管道](https://docs.cloud.google.com/kubernetes-engine/docs/tutorials/gitops-cloud-build?hl=zh-tw)部署應用程式。
* **預留項目運算層級專案**：將租戶查詢活動對應至 BigQuery 預留項目的專案。

### 分享預訂資訊

這種方法中的預留項目會採用 BigQuery 預留項目內建的[公平排程](https://docs.cloud.google.com/bigquery/docs/slots?hl=zh-tw#fair_scheduling_in_bigquery)演算法。每個運算層級預訂項目都會指派給單一專案。租戶查詢會使用每個運算層級專案可用的公平調度資源運算單元，而任何層級未使用的資源運算單元會自動在其他層級重複使用。如果租戶有特定時間需求，您可以使用專案/預訂配對，專門提供確切數量的運算單元。

### 設定 VPC Service Controls 範圍

在這種設定中，我們建議使用 VPC Service Controls 服務範圍，防止租戶資料集意外暴露在貴機構 Google Cloud 外部，並防止機構內未經授權的資料彙整。

#### 範圍

在這種設定中，建議您建立下列[服務安全防護範圍](https://docs.cloud.google.com/vpc-service-controls/docs/create-service-perimeters?hl=zh-tw)：

* **資料管道**：資料管道專案周圍的範圍應強制執行所有不需要接收租戶資料的服務。
* **租戶資料**：租戶資料集專案和租戶 BigQuery 計算專案周圍的 Perimeter。強制所有服務禁止機構外部存取。
* **內部應用程式**：強制執行所有服務，並使用[存取層級](https://docs.cloud.google.com/vpc-service-controls/docs/use-access-levels?hl=zh-tw#using_access_levels)，將資源存取權授予部門團隊。
* **外部應用程式**：軟體即服務 (SaaS) 應用程式周圍的 perimeter。強制停用應用程式運作不需要的所有服務。

#### 重疊範圍

在這種設定中，建議您建立下列[周邊橋接器](https://docs.cloud.google.com/vpc-service-controls/docs/create-perimeter-bridges?hl=zh-tw)：

* **資料管道和租戶資料**：允許管道將資料寫入租戶資料集。
* **資料管道和內部應用程式**：允許管道將資料寫入跨客戶資料集。
* **外部應用程式和租戶資料**：允許面向外部的應用程式查詢租戶資料。
* **外部應用程式和內部應用程式**：允許外部應用程式使用內部應用程式開發及部署的模型處理資料。

### 提供專屬租戶基礎架構的 SaaS 供應商

在更複雜的情境中，SaaS 供應商可能會為每個租戶部署專屬的運算基礎架構。在此情境中，專屬基礎架構負責處理 BigQuery 內租戶資料的要求。

專屬租戶基礎架構設計可解決下列常見問題，也就是為每個租戶部署基礎架構時，與 BigQuery 相關的常見問題：

* **帳單責任**：追蹤與每個已加入的租戶相關的基礎架構費用。
* **端對端延遲時間**：資料存放區的最新程度，適用於租戶和跨客戶分析解決方案。
* **效能預期**：確保租戶效能維持在可接受的限制內。

#### 將資料集與專用資源共置

部署專屬租戶基礎架構時，建議您為租戶專屬專案建立父項[資料夾](https://docs.cloud.google.com/resource-manager/docs/cloud-platform-resource-hierarchy?hl=zh-tw#folders)。然後，在專案中將租戶的 BigQuery 資料集與專用資源共置，代表租戶存取該資料。為盡量縮短租戶資料的端對端延遲時間，Dataflow 管道會直接將資料插入租戶資料集。

這個設計會處理上游資料處理和發布作業，與先前的共用基礎架構設計類似。不過，租戶資料和存取租戶資料的應用程式會整理到租戶專屬專案 (也可以整理到租戶專用資料夾)，以簡化帳單和資源管理作業。下圖顯示根據這項建議設計的範例專案設定：

**圖 2**：資料管道專案會處理來自其他多個專案的單一租戶資料。

圖 2 中的專案設定包含下列專案：

* **資料管道專案**：接收、處理及發布租戶資料的核心基礎架構元件，全都封裝在單一專案中。
* **專屬租戶專案**：包含所有專屬於單一租戶的雲端資源，包括 BigQuery 資料集。建議您使用 [Identity and Access Management (IAM)](https://docs.cloud.google.com/iam?hl=zh-tw)，大幅限制可存取客戶資料集的帳戶和服務帳戶範圍。
* **內部分析專案**：代表分析團隊用來評估租戶資料和建構新功能的自我管理資源。
* **外部網路專案**：負責處理租戶要求並將其路由至專屬後端的專案。

#### 分享預訂資訊

這個方法中的預留項目會採用 BigQuery 預留項目內建的公平排程演算法。在此設定中，系統會將運算層級預留項目指派給使用該層級的每個租戶專案。如果租戶有特定時間要求，您可以建立專屬預留項目，為租戶專案提供精確數量的運算單元。

#### 使用 IAM 控制項並停用金鑰建立功能

VPC Service Controls 範圍可能不適合這個情境。專案相關[限制](https://docs.cloud.google.com/vpc-service-controls/quotas?hl=zh-tw#limits)可防止機構在與租戶專案互動的專案周圍使用範圍界線。建議您改用嚴格的 IAM 控制項，並[停用金鑰建立功能](https://docs.cloud.google.com/resource-manager/docs/organization-policy/restricting-service-accounts?hl=zh-tw#disable_service_account_key_creation)，防範不當的外部存取行為。

## 由中央機構管理的資料市集

資料市集是常見的設計主題，核心數據分析資料會儲存在中央存放區，子集則會依業務範圍共用。資料市集通常有數十或數百個租戶，代表要考量的業務範圍。

BigQuery 中的資料市集設計可滿足下列需求：

* **安全地共用資料**：透過技術控管機制共用資料，盡量減少團隊間的不當存取。
* **集中式資料治理**：確保用於重要商務報表的核心資料資產經過標準化和驗證。
* **業務單位成本歸因**：追蹤及調整各業務單位的運算用量。

### 使用集中管理的存放區

在這個設計中，核心資料會擷取到集中管理的存放區。授權檢視區塊、[授權使用者定義函式 (UDF)](https://docs.cloud.google.com/bigquery/docs/user-defined-functions?hl=zh-tw#authorize_routines) 和資料欄政策通常會一併使用，以便與業務線共用資料，同時防止機密資料意外散布。

租戶專案中的團隊可以根據帳戶權限，存取集中管理的資料集。團隊會使用分配給自己專案的配額，建構報表和衍生資料集。核心資料團隊會使用授權檢視表，完全掌控資料市集資產的存取權控管。在這種設定中，建議您避免在核心資料專案呈現的物件上建構多層檢視區塊。下圖顯示根據這項建議設計的專案設定範例：

**圖 3**：核心資料專案會維護集中式資料市集，供整個機構存取。

圖 3 中的專案設定包含下列專案：

* **核心資料專案**：管理核心資料和資料市集檢視畫面存取權的治理範圍。您可以在這個專案的資料集中維護授權檢視區塊，並根據群組成員資格，將授權檢視區塊授予數據分析團隊。
* **[擷取、轉換、載入 (ETL)](https://wikipedia.org/wiki/Extract,_transform,_load) 基礎架構**：將上游資料來源處理為核心資料的基礎架構。視管理區隔需求而定，您可以選擇將 ETL 基礎架構部署為獨立專案，或部署為核心資料專案的一部分。
* **Analytics 團隊專案**：資料市集的消費者會使用這些專案，並透過自行佈建的基礎架構存取權，處理資料市集中的資料。分析團隊專案應能建構衍生資料集供當地使用。

### 使用雙層預留項目設計

使用資料市集時，建議採用雙層設計。在雙層設計中，您會為[機構資源](https://docs.cloud.google.com/resource-manager/docs/cloud-platform-resource-hierarchy?hl=zh-tw#organizations)指派運算單元數量較少的預留項目，以涵蓋一般用途。如果團隊有更多需求，請在專案或資料夾層級指派保留項目。

### 設定 VPC Service Controls 範圍

在此設定中，我們建議使用 VPC Service Controls 邊界，防止 BigQuery 資料集意外暴露在Google Cloud 機構外部。

#### 範圍

在這個設定中，建議您建立下列服務周邊：

* **核心資料**：保護資料倉儲和資料市集資料集的周邊。
* **資料管道**：ETL 基礎架構專案的周邊。如果資料管道需要向貴機構 Google Cloud以外的位置提出要求，建議您將這個周邊範圍與核心資料周邊範圍分開。
* **Analytics**：用於建構及部署機構內部資料分析資產的周邊。這個 perimeter 的存取權政策預期會比與其橋接的核心資料 perimeter 更寬鬆。

#### 重疊範圍

在這個設定中，建議您建立下列周邊橋接器：

* **資料管道和核心資料**：允許資料管道寫入核心資料專案。
* **核心資料和分析**：允許分析專案中的使用者查詢授權檢視區塊。

### 複製多區域設定的資料集

由於 BigQuery 不允許跨區域查詢，因此當資料市集必須存在於多個區域時，您無法使用授權檢視區隔資料的策略。不過，您可以使用 [BigQuery 資料移轉服務](https://docs.cloud.google.com/bigquery/docs/dts-introduction?hl=zh-tw)，將相關資料集複製到其他區域。在這種情況下，您會在資料目錄中為資料所在的每個額外區域建立資料欄政策。下圖顯示多區域設定：

**圖 4**：多區域設定會使用 BigQuery 資料移轉服務，跨區域複製資料集。

圖 4 中的專案設定包含下列專案。

* **核心資料專案**：管理核心資料和資料市集檢視畫面存取權的治理範圍。資料會複製到區域資料集並維護，供全球團隊使用。
* **ETL 基礎架構**：處理上游資料來源並轉換為核心資料的基礎架構。視管理區隔需求而定，您可以選擇將 ETL 基礎架構部署為獨立專案，或部署為核心資料專案的一部分。
* **資料分析團隊專案**：資料市集的消費者會使用這些專案，並運用自行佈建的基礎架構，處理資料市集區域資料集中的資料。分析團隊專案應能建構衍生資料集供本機使用。

[BigQuery 資料移轉服務](https://docs.cloud.google.com/bigquery/docs/dts-introduction?hl=zh-tw)是額外的排程元件，但有一些限制。內建服務排程器的間隔時間最短為 15 分鐘，且必須複製來源資料集中的所有資料表。您無法在 BigQuery 資料移轉服務排程器中嵌入其他指令碼，建立特定區域的資料子集。

如果貴機構需要更多彈性，可以選擇下列方案：

* **Managed Service for Apache Airflow 工作**：您可以排定 [Managed Service for Apache Airflow](https://docs.cloud.google.com/composer?hl=zh-tw) 工作，發出 ETL 工作來建立區域子集，然後透過[用戶端 API](https://docs.cloud.google.com/bigquery/docs/reference/libraries?hl=zh-tw) 觸發 BigQuery 資料移轉服務。如果貴機構可以支援額外延遲，建議使用這個選項。
* **ETL 基礎架構**：ETL 基礎架構 (例如 Dataflow) 可將區域子集雙重寫入目標區域。如果貴機構要求地區間的資料延遲時間越短越好，建議選用這個選項。

## 權責分散的資料市集

如果需要依系統擁有者、業務線或地理位置進行管理區隔，請使用分散式授權。

與標準資料市集相比，去中心化資料市集有下列不同疑慮：

* **安全地共用資料**：透過技術控管機制共用資料，盡量減少團隊間的不當存取。
* **資料探索**：團隊必須能夠探索及要求存取資料集。
* **資料出處**：如果沒有中央管理團隊，各團隊必須能夠信任傳送至分析產品的資料來源。

### 委派核心資料管理權

這種設計與傳統資料市集方法不同，因為分散式授權會將核心資料管理決策委派給機構的元件子群組。使用去中心化授權時，您可以透過 [Cloud Key Management Service (Cloud KMS)](https://docs.cloud.google.com/security-key-management?hl=zh-tw)、資料欄政策、VPC Service Controls 和預留項目，集中控管安全性與 BigQuery 容量。因此，您可以避免自行管理的倉儲常見的資料蔓延問題。下圖顯示使用去中心化授權的架構：

**圖 5.** 核心控管專案有助於確保安全一致性，而各個群組則可維護資料作業。

圖 5 中的專案設定包含下列專案：

* **核心控管專案**：負責處理跨機構管理問題的專案。您可以在這個專案中建立安全防護資源，例如 Cloud KMS 金鑰環和資料目錄欄政策。這個專案會做為 BigQuery [保留項目管理專案](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#admin-project)，在整個機構中分享運算單元。
* **組織單位資料專案**：廣泛機構內自行管理的資料市集擁有者。核心管理專案會管理組織單位資料專案的受限範圍。
* **Analytics 團隊專案**：資料市集消費者使用的專案。這些專案會使用自行佈建的基礎架構和配額，存取及處理資料市集中的資料。

### 使用雙層預留項目設計

建議您分散式資料市集採用與標準資料市集[相同的雙層設計](#data-marts-central-reservation)。在這個設定中，您會為[機構資源](https://docs.cloud.google.com/resource-manager/docs/cloud-platform-resource-hierarchy?hl=zh-tw#organizations)指派預訂項目，其中包含少量配額，可滿足一般用途。如果團隊有更多需求，請在專案或資料夾層級指派保留項目。

### 使用資料目錄

資料目錄提供全機構的探索功能、中繼資料標記和資料欄政策設定。知識目錄探索功能會自動為機構中所有新的 BigQuery 資料表建立[中繼資料項目](https://docs.cloud.google.com/dataplex/docs/catalog-overview?hl=zh-tw)。知識目錄的功能也能協助資料治理管理員快速找出新的資料資產，並套用適當的控管措施。

### 設定 VPC Service Controls 範圍

在此設定中，我們建議使用 VPC Service Controls 邊界，防止 BigQuery 資料集意外暴露在Google Cloud 機構外部。

#### 範圍

在這個設定中，建議您建立下列服務周邊：

* **核心資料**：保護資料倉儲和資料市集資料集的周邊。這個安全防護範圍應包含所有組織單位專案和資料治理專案。
* **Analytics**：用於建構及部署機構內部分析資產的周邊。這個周邊的存取政策預計會比與其橋接的核心資料周邊更寬鬆。

#### 重疊範圍

在這個設定中，建議您建立下列周邊橋接器：

* **核心資料和分析**：允許分析專案中的使用者查詢授權檢視區塊。

## 多機構資料共用

多機構共用是資料市集設計的特殊考量。如果機構想與擁有專屬 Google 機構的其他實體安全共用資料集，就適合採用這種資料共用設計。

多機構資料共用功能可解決資料共用者下列疑慮：

* **分享機密性**：只有預期對象可以存取分享的資料。
* **防止不當存取**：只有預定要存取的資源才能從外部存取。
* **運算資源分離**：外部人士發起的查詢會產生費用。

**注意：** 在某些情況下，來自外部機構的查詢可能會意外失敗。[Cloud Customer Care](https://cloud.google.com/support-hub/?hl=zh-tw) 團隊可以協助您啟動設定變更，以修正問題。

### 保護內部專案，避免受到共用資料專案影響

多機構資料共用設計的重點，在於保護機構的內部專案，避免受到共用資料專案活動的影響。共用資料集專案可做為緩衝區，禁止存取機密的內部資料處理作業，同時提供對外共用資料的功能。

從外部專案啟動的查詢會使用叫用專案的運算資源。如果所有查詢的資料集都位於相同 Google Cloud區域，這些查詢就能合併不同機構的資料。下圖顯示如何在多機構專案設定中共用資料集：

**圖 6**：外部機構查詢共用專案中多個資料集的資料。

圖 6 中的專案設定包含下列專案：

* **機構內部專案**：含有機密內部資料的專案。內部專案可將經過清除的資料複製到共用資料專案的資料集中，藉此對外共用資料。內部專案應擁有負責更新共用資料的服務帳戶。
* **共用資料專案**：包含從內部專案複製的經過清除的資訊。使用外部使用者[群組](https://docs.cloud.google.com/iam/docs/groups-in-cloud-console?hl=zh-tw)管理外部人士的存取權。在這種情況下，您會以管理功能身分管理群組成員，並授予外部帳戶檢視者權限，讓他們透過這些群組存取資料集。

### 設定 VPC Service Controls 範圍

在這種設定中，我們建議 VPC Service Controls perimeter 外部共用資料，並防止 BigQuery 資料集意外暴露在內部專案外部。

#### 範圍

在這個設定中，建議您建立下列服務周邊：

* **內部資料**：保護核心資料資產的範圍。VPC Service Controls 會強制執行 BigQuery 存取權。
* **對外共用資料**：用於存放可與外部機構共用資料集的 perimeter。這個安全防護範圍會停用 BigQuery 存取權的強制執行。

#### 重疊範圍

在這種設定中，建議您建立下列周邊橋接器：

* **內部資料到外部資料**：perimeter bridge 可讓受保護程度較高的內部資料專案，將資料輸出至外部資料共用專案。

## 多租戶系統的其他注意事項

本節將深入探討特殊情況，供您參考並搭配上述最佳做法使用。

### Google Cloud 資源限制和配額

* 每個專案的服務帳戶軟性配額上限為 100 個。如要為維護租戶服務帳戶的專案申請配額，請透過 [Google Cloud 控制台](https://console.cloud.google.com/iam-admin/quotas?hl=zh-tw)操作。
* BigQuery 並行作業預設為每個發出查詢的專案 100 個查詢 (擁有資料集的專案沒有這類限制)。如要提高這項軟性配額，請與業務代表聯絡。
* VPC Service Controls 限制整個機構的服務範圍內最多只能有 10,000 個專案。如果每個房客的專案設計規模很大，建議改用每個房客的資料集設計。
* 每個機構的 VPC Service Controls 範圍 (包括重疊範圍) 數量上限為 100 個。

### 使用授權檢視或具體化子集資料表

如要管理租戶對大型事實資料表子集的存取權，可以使用租戶專屬的授權檢視區塊，或建立租戶專屬的子集資料表。下表比較了這些方法：

| 功能 | 授權檢視表 | 子集資料表 |
| --- | --- | --- |
| 支援的租戶數量 | 每個資料集最多只能有 [2500 個授權資源](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#dataset_limits)。 | 授權資源包括授權檢視表、授權資料集和授權函式。專案中的資料集數量或資料集中的資料表數量沒有限制。 |
| 分區與分群 | 授權檢視區必須共用基礎資料表的一般分區和叢集配置。  為提升租戶區隔的效能，建議您根據租戶 ID 將父項資料表叢集化。 | 您可以根據租戶需求，對子集資料表進行分區和叢集處理。 |
| 區域規劃 | 授權檢視區塊無法跨地區，且必須位於基本資料表的 Google Cloud 地區。區域化會影響地理位置偏遠的租戶。 | 子集資料表可以位於最適合租戶的區域。可能需要支付額外[費用](https://docs.cloud.google.com/bigquery/docs/copying-datasets?hl=zh-tw#pricing)。 |
| 資料欄政策強制執行 | 套用至基本資料表的資料欄政策，會套用至所有授權檢視畫面，無論這些檢視畫面的權限為何。 | 每個子集資料表都必須套用資料欄政策，政策才會生效。 |
| 資料存取記錄 | 資料存取記錄會反映在基本資料表的記錄中。 | 系統會分別記錄每個子集資料表的存取權。 |
| 轉換彈性 | 透過授權檢視區塊，您可以立即重新設計租戶存取的物件。 | 如要變更子集資料表，必須進行複雜的結構定義變更。 |

### 控管機密資料

為防止未經授權存取資料，BigQuery 除了標準 IAM 權限外，還提供多項額外功能。

#### 客戶提供的加密金鑰

如果代管機構代表租戶儲存及處理資料，但無法存取部分資料內容，就適用用戶端資料加密。舉例來說，主辦機構可能無法存取視為私密的個人或裝置資料。

我們建議資料傳送者使用開放原始碼 [Tink 程式庫](https://github.com/google/tink)的 AEAD 加密金鑰，加密機密資料。Tink 程式庫 AEAD 加密金鑰與 [BigQuery AEAD 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/aead_encryption_functions?hl=zh-tw)相容。租戶接著可以透過[授權 UDF](https://docs.cloud.google.com/bigquery/docs/user-defined-functions?hl=zh-tw#authorize_routines) 存取金鑰資料，或將金鑰資料做為[查詢參數](https://docs.cloud.google.com/bigquery/docs/parameterized-queries?hl=zh-tw#bq)傳遞至 BigQuery，藉此解密資料，主機機構無法記錄金鑰。

#### 資料欄存取政策

在多租戶資料市集，通常會使用資料欄政策，防止協作團隊之間意外洩漏敏感內容。在資料市集情境中，授權檢視表是團隊之間分享資料的首選機制。授權檢視畫面無法授予受保護資料欄的存取權。

如果將政策設為強制執行存取控管，系統會禁止未獲授與政策[細部讀取者](https://docs.cloud.google.com/bigquery/docs/column-level-security?hl=zh-tw#fine_grained_reader)角色的使用者存取。即使未強制執行政策，政策也會記錄使用者對分類欄的所有存取權。

#### Sensitive Data Protection

[Sensitive Data Protection](https://docs.cloud.google.com/sensitive-data-protection?hl=zh-tw) 提供 API 和掃描公用程式，可協助您找出並防範儲存在 BigQuery 或 [Cloud Storage](https://docs.cloud.google.com/storage?hl=zh-tw) 資料集中的機密內容。在多租戶情境中，機構通常會使用 DLP API (Sensitive Data Protection 的一部分) 識別機密資料，並視需要將其權杖化，再進行儲存。

### 管理運算單元預留項目

在多租戶系統中管理預訂，有助於在租戶擴大規模時控管成本，並確保每個租戶的效能。

如要管理預留項目，建議您建立單一預留項目管理專案。在同一個管理專案中購買的運算單元承諾，可供源自該管理專案的所有[預留項目](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#admin-project)共用。使用運算單元承諾的專案一次只能指派給一個預留項目。[專案發出的所有查詢](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs/insert?hl=zh-tw#path-parameters)會根據可用資源共用運算單元。

為確保符合租戶服務水準目標 (SLO)，您可以透過 Cloud Logging 和 BigQuery [資訊結構定義](https://docs.cloud.google.com/bigquery/docs/information-schema-jobs?hl=zh-tw)[監控](https://docs.cloud.google.com/bigquery/docs/reservations-monitoring?hl=zh-tw)預留項目。如果機構在分析師活動或優先工作期間遇到忙碌期，可以使用[彈性配額](https://cloud.google.com/bigquery/pricing?hl=zh-tw#flex-slots-pricing)分配額外容量。

#### 預留項目做為租戶運算層級

SaaS 供應商通常會設定有限數量的 BigQuery 預留項目做為共用資源，這些供應商擁有數十到數千個租戶。

如果您是共用租戶基礎架構的 SaaS 供應商，建議您為每個專案指派專屬的預留項目，並將租戶分組，共用該專案的 BigQuery 運算資源。這個設計可減少數千個額外專案和預訂的管理負擔，同時讓機構分配最低[時段容量](https://docs.cloud.google.com/bigquery/docs/reference/reservations/rest/v1/projects.locations.reservations?hl=zh-tw)，以滿足預訂的預期效能需求。

如果[ELT 資料處理](https://wikipedia.org/wiki/Extract,_transform,_load#Vs._ELT)的即時性是首要考量，建議您分配預留項目來處理。如要避免使用可用於臨時工作負載的額外運算單元，請將預留項目設為[忽略閒置運算單元](https://docs.cloud.google.com/bigquery/docs/slots?hl=zh-tw#idle_slots)。

以下範例說明如何將預留項目設定為租戶運算層級：

* **資料處理**：2000 個時段，忽略閒置時段。這項預留空間已設定為符合資料處理服務等級目標。
* **內部專案**：1000 個時段，允許閒置。這項預留容量會套用至用於內部分析的專案。如果資料處理或運算層級有剩餘的配額，系統會重複使用這些配額。
* **低運算層級**：2000 個位置，忽略閒置狀態。這項預訂會套用至資源不足的房客。與高優先順序層級不同，這個預留項目會忽略閒置的運算單元。
* **高運算層級**：3000 個位置，允許閒置。這項預留項目會套用至資源用量高的租戶。為加快查詢速度，系統會自動套用其他預留項目的閒置運算單元。

如果房客在專屬基礎架構上運作，建議您將指定資料夾或專案指派給適當的共用預留項目。

#### 每個團隊的預留項目

在資料市集環境中與團隊合作時，建議您為每個需要額外運算資源的團隊建立預留項目。然後將該保留項目指派給包含團隊專案的父項資料夾。該團隊的所有新專案都會使用相同資源分配的[公平排程](https://docs.cloud.google.com/bigquery/docs/slots?hl=zh-tw#fair_scheduling_in_bigquery)時段。

以下範例說明如何為每個團隊設定預訂：

* **機構層級預留**：500 個配額，允許閒置。這項預留項目會指派給頂層機構，並為未使用專屬預留項目的 BigQuery 使用者提供運算單元
* **資料處理**：1000 個時段，忽略閒置時段。這項預留容量已設定為符合最低資料處理 SLO。
* **核心資料管理**：500 個配額，允許閒置。這項預留項目會套用至用於內部管理的專案。如果資料處理或運算層級有剩餘的配額，系統會重複使用這些配額。
* **Analytics 處理保留項目**：500 個運算單元，允許閒置。這是專門提供給分析團隊的預留項目。

### 多區域代管規定

通常是為了減少消費者資料延遲，或是為了符合法規要求，才需要多區域主機代管。

Google Cloud 中的專案視為全域專案，可在任何區域佈建資源。BigQuery 會將資料集、資料欄政策和運算單元承諾視為區域性資源。配額只能存取本機區域中的資料集，且只能將資料欄政策套用至本機資料集中的資料表。如要使用以容量為準的定價，您必須在包含資料集的每個區域購買運算單元。

如需遵守法規的相關指引，請洽詢業務代表。

## 後續步驟

* 瞭解 [IAM 最佳做法](https://docs.cloud.google.com/iam/docs/recommender-best-practices?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-02 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-02 (世界標準時間)。"],[],[]]