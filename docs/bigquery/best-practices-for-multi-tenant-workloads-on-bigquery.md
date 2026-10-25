Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [資源](https://docs.cloud.google.com/bigquery/docs/release-notes?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 在 BigQuery 執行多租戶工作負載的最佳做法

本文提供多租戶資料平台和企業資料市集常用模式的技術和最佳做法。

商業企業、軟體即服務 (SaaS) 供應商和政府組織，通常必須跨地理和管理界線，安全地託管內部和第三方資料。[BigQuery](https://docs.cloud.google.com/bigquery?hl=zh-tw) 是一項強大的工具，可持續滿足多租戶平台的需求，處理數百萬 TB 的資料，以及不同業務單位中數十萬名資料消費者的需求。本文適用於在 BigQuery 上部署多租戶平台，並想瞭解可用的[存取控管](https://docs.cloud.google.com/bigquery/docs/data-governance?hl=zh-tw)和[效能管理功能](https://docs.cloud.google.com/bigquery/docs/best-practices-performance-overview?hl=zh-tw)的組織。

多租戶平台建構工具通常需要平衡下列考量：

* **資料隔離**：實施嚴格控管，防止資料在租戶之間外洩。
* **效能穩定**：設定及分配 [BigQuery 預留項目](https://docs.cloud.google.com/bigquery/docs/reservations-intro?hl=zh-tw)，確保各租戶的效能穩定。
* **資源管理**：規劃配額和限制的影響。
* **地理分布**：將資料存放在指定和必要的[地理位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw#multi-regions)。如有法規遵循相關疑慮，請參閱 Google Cloud的[法規遵循服務](https://cloud.google.com/security/compliance/offerings?hl=zh-tw)。
* **稽核與安全性**：保護租戶資料，避免不當存取和竊取。
* **成本管理**：確保託管各租戶的 BigQuery 費用一致。
* **作業複雜度**：盡可能減少託管新租戶所需的系統變異量。

## 採用共用租戶基礎架構的 SaaS 供應商

代管第三方資料的 SaaS 供應商必須確保整個客戶群的可靠性和隔離性。這些客戶可能多達數萬人，且客戶資料可能透過共用服務基礎架構存取。部分 SaaS 供應商也會維護經過清理的中央資料儲存庫，對所有租戶進行分析。

每個租戶一個資料集的設計，有助於減輕組織在擴充至數千個租戶時遇到的下列問題：

* **管理複雜度**：每位客戶的新專案和雲端資源總數
* **端對端延遲時間**：資料儲存庫對租戶和跨客戶數據分析解決方案的最新程度
* **效能預期**：確保租戶效能維持在可接受的範圍內

### 為每個租戶設定資料集

在專門儲存客戶資料的專案中，每位客戶的資料會以 BigQuery 資料集分隔。在主機組織中，您可以使用第二個專案，對合併的客戶資料部署數據分析和機器學習。接著，您可以設定資料處理引擎 [Dataflow](https://docs.cloud.google.com/dataflow?hl=zh-tw)，將傳入的資料雙重寫入內部和租戶專用資料表。Dataflow 設定會使用完整寫入的資料表，而非授權檢視表。使用完整寫入的資料表，可統一處理地理分布，並在租戶數量增加時，避免達到[授權檢視表限制](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#view_limits)。

BigQuery 將儲存空間和[運算](https://docs.cloud.google.com/bigquery/docs/slots?hl=zh-tw)分開，因此與叢集式資料倉儲相比，您只需設定較少的專案，即可處理服務層級和資料隔離等問題。如果不需要為租戶設定額外的[專屬雲端](#saas-dedicated)資源，建議您考慮為每個租戶設定專屬資料集的預設設定。下圖顯示根據這項建議設計的專案設定範例：

**圖 1.**隨著租戶數量增加，固定數量的專案會處理資料和處理需求。

圖 1 中的專案設定包含下列專案：

* **資料管道專案**：接收、處理及發布租戶資料的核心基礎架構元件，全部封裝至單一專案。
* **合併租戶資料專案**：核心資料專案，為每位客戶維護資料集。租戶資料應透過運算層專案存取。
* **內部開發專案**：代表自行管理資源的專案，分析團隊會使用這些資源評估租戶資料及建構新功能。
* **使用者應用程式專案**：這類專案包含的資源，旨在與使用者互動。建議您使用租戶範圍的服務帳戶存取租戶資料集，並使用穩固且安全的[建構管道](https://docs.cloud.google.com/kubernetes-engine/docs/tutorials/gitops-cloud-build?hl=zh-tw)部署應用程式。
* **預留項目運算層級專案**：將租戶查詢活動對應至 BigQuery 預留項目的專案。

### 共用預留項目

這種方法的預留項目仰賴 BigQuery 預留項目內建的[公平排程](https://docs.cloud.google.com/bigquery/docs/slots?hl=zh-tw#fair_scheduling_in_bigquery)演算法。每個運算層預留項目都會指派給單一專案。租戶查詢會使用各運算層級專案可用的公平排程運算單元，而任何層級未使用的運算單元，都會自動在其他層級重複使用。如果租戶有特定的時間要求，您可以使用專案預留項目組合，專門提供確切數量的運算單元。

### 設定 VPC Service Controls perimeter

在這種設定中，建議您使用 VPC Service Controls perimeter，防止租戶資料集意外在 Google Cloud 組織外部公開，並防止組織內未經授權的資料彙整。

#### Perimeter

在這種設定中，建議您建立下列[service perimeter](https://docs.cloud.google.com/vpc-service-controls/docs/create-service-perimeters?hl=zh-tw)：

* **資料管道**：資料管道專案周圍的 perimeter 應強制執行所有不需要接收租戶資料的服務。
* **租戶資料**：租戶資料集專案和租戶 BigQuery 運算專案周圍的 perimeter。強制執行所有服務，防止機構外部人員存取。
* **內部應用程式**：強制執行所有服務，並使用[存取層級](https://docs.cloud.google.com/vpc-service-controls/docs/use-access-levels?hl=zh-tw#using_access_levels)，將資源存取權授予部門團隊。
* **外部應用程式**：SaaS 應用程式的 perimeter。強制執行應用程式運作時不需要的所有服務。

#### Perimeter bridge

在這種設定中，建議您建立下列[perimeter bridge](https://docs.cloud.google.com/vpc-service-controls/docs/create-perimeter-bridges?hl=zh-tw)：

* **資料管道和租戶資料**：允許管道將資料寫入租戶資料集。
* **資料管道和內部應用程式**：允許管道將資料寫入跨客戶資料集。
* **外部應用程式和租戶資料**：允許對外應用程式查詢租戶資料。
* **外部應用程式和內部應用程式**：允許對外應用程式使用內部應用程式開發及部署的模型處理資料。

### 具備專屬租戶基礎架構的 SaaS 供應商

在更複雜的情境中，SaaS 供應商可能會為每個租戶部署專屬的運算基礎架構。在這種情況下，專用基礎架構會負責處理 BigQuery 內租戶資料的要求。

專屬租戶基礎架構設計可解決為每個租戶部署基礎架構時，與 BigQuery 相關的下列常見問題：

* **帳單責任歸屬**：追蹤與各個已上線租戶相關的基礎架構費用。
* **端對端延遲時間**：租戶和跨客戶數據分析解決方案的資料儲存庫最新程度。
* **效能預期**：確保租戶效能維持在可接受的範圍內。

#### 將資料集與專用資源放在同一位置

部署專用租戶基礎架構時，建議您為租戶專屬專案建立上層[資料夾](https://docs.cloud.google.com/resource-manager/docs/cloud-platform-resource-hierarchy?hl=zh-tw#folders)。接著，將租戶的 BigQuery 資料集與專案中的專屬資源放在同一位置，並由這些資源代表租戶存取資料。為盡量縮短租戶資料的端對端延遲時間，Dataflow 管道會直接將資料插入租戶資料集。

這項設計會處理上游資料處理和發布作業，類似於上述共用基礎架構設計。不過，租戶資料和存取租戶資料的應用程式會歸入租戶專屬專案 (並可選擇歸入租戶專用資料夾)，以簡化計費和資源管理。下圖顯示根據這項建議設計的專案設定範例：

**圖 2**：資料管道專案會處理來自多個其他專案的單一租戶資料。

圖 2 的專案設定包含下列專案：

* **資料管道專案**：接收、處理及發布租戶資料的核心基礎架構元件，全部封裝至單一專案。
* **專用租戶專案**：包含單一租戶專用所有雲端資源的專案，包括 BigQuery 資料集。建議您使用 [Identity and Access Management (IAM)](https://docs.cloud.google.com/iam?hl=zh-tw)，大幅限制可存取客戶資料集的帳戶和服務帳戶範圍。
* **內部數據分析專案**：代表數據分析團隊用來評估租戶資料及建構新功能的自我管理資源。
* **外部網路專案**：處理租戶要求並轉送至專屬後端的專案。

#### 共用預留項目

這種方法的預留項目仰賴 BigQuery 預留項目內建的公平排程演算法。在這個設定中，運算層預留項目會指派給使用該層的每個租戶專案。如果租戶有特定的時間需求，您可以建立專屬預留項目，為租戶專案提供精確的運算單元數量。

#### 使用 IAM 控制項並停用金鑰建立功能

VPC Service Controls perimeter 可能不適用於這種情況。專案相關[限制](https://docs.cloud.google.com/vpc-service-controls/quotas?hl=zh-tw#limits)會防止組織在與租戶專案互動的專案周圍使用 perimeter 邊界。建議您改用嚴格的 IAM 控制項，並[停用金鑰建立功能](https://docs.cloud.google.com/resource-manager/docs/organization-policy/restricting-service-accounts?hl=zh-tw#disable_service_account_key_creation)，防止未經授權的外部存取。

## 由中央授權的資料市集

資料市集是常見的設計主題，核心數據分析資料會儲存在中央存放區，子集則會依業務範圍共用。資料市集通常有數十或數百個租戶，代表要考量的業務範圍。

BigQuery 的資料市集設計可滿足下列需求：

* **安全資料協作**：透過技術控管機制共用資料，盡可能減少團隊間不當存取。
* **集中式資料治理**：確保用於重要業務報表的核心資料資產經過標準化和驗證。
* **業務單位成本歸因**：追蹤及調整業務單位的運算用量。

### 使用集中管理的存放區

在這種設計中，核心資料會擷取至集中管理的存放區。授權檢視表、[授權 user-defined function (UDF)](https://docs.cloud.google.com/bigquery/docs/user-defined-functions?hl=zh-tw#authorize_routines) 和資料欄政策通常會搭配使用，以便與業務範圍共用資料，同時防止機密資料意外散布。

租戶專案中的團隊可以根據帳戶權限，存取集中管理的資料集。團隊會使用分配給自己專案的運算單元，建立報表和衍生資料集。核心資料團隊使用授權檢視表，完整控管資料市集資產的存取控管。在這種設定下，建議您避免在核心資料專案呈現的物件上，建立多層檢視表。下圖顯示根據這項建議設計的專案設定範例：

**圖 3**：核心資料專案會維護集中式資料市集，可供整個組織存取。

圖 3 中的專案設定包含下列專案：

* **核心資料專案**：管理核心資料和資料市集檢視表存取權的控管範圍。您會在這個專案的資料集內維護授權檢視表，並根據群組成員資格，將授權檢視表授予數據分析團隊。
* **[擷取、轉換、載入 (ETL)](https://wikipedia.org/wiki/Extract,_transform,_load) 基礎架構**：用於將上游資料來源處理成核心資料的基礎架構。視管理分隔需求而定，您可以選擇將 ETL 基礎架構部署為獨立專案，或做為核心資料專案的一部分。
* **數據分析團隊專案**：資料市集的使用者會使用這些專案，並透過自己佈建的基礎架構存取權，處理資料市集內的資料。數據分析團隊專案應能建構衍生資料集，供本機使用。

### 採用兩層式預留項目設計

使用資料市集時，建議您採用兩層式設計。在雙層設計中，您會為[組織資源](https://docs.cloud.google.com/resource-manager/docs/cloud-platform-resource-hierarchy?hl=zh-tw#organizations)指派少量運算單元的預留項目，以涵蓋一般用量。如果團隊有更多需求，請在專案或資料夾層級指派預留項目。

### 設定 VPC Service Controls perimeter

在這種設定中，建議您使用 VPC Service Controls perimeter，防止 BigQuery 資料集意外公開至Google Cloud 組織外部。

#### Perimeter

在這種設定中，建議您建立下列 service perimeter：

* **核心資料**：保護資料倉儲和資料市集資料集的 perimeter。
* **資料管道**：ETL 基礎架構專案的 perimeter。如果資料管道需要向 Google Cloud組織外部發出要求，建議您將這個 perimeter 與核心資料 perimeter 分開。
* **Analytics**：這個 perimeter 用於建構及部署貴組織內部的數據分析資產。這個 perimeter 的存取權政策應比與其橋接的核心資料 perimeter 更寬鬆。

#### Perimeter bridge

在這種設定中，建議您建立下列 perimeter bridge：

* **資料管道和核心資料**：允許資料管道寫入核心資料專案。
* **核心資料和數據分析**：允許數據分析專案中的使用者查詢授權檢視表。

### 複製多區域設定的資料集

由於 BigQuery 不允許跨區域查詢，因此當資料市集必須存在於多個區域時，您無法使用授權檢視表區隔資料。不過，您可以使用 [BigQuery 資料移轉服務](https://docs.cloud.google.com/bigquery/docs/dts-introduction?hl=zh-tw)，將相關資料集複製到其他區域。在這種情況下，您可以在 Data Catalog 中，為資料落地所在的每個額外區域建立資料欄政策。下圖顯示多區域設定：

**圖 4**：多區域設定會使用 BigQuery 資料移轉服務，跨區域複製資料集。

圖 4 的專案設定包含下列專案。

* **核心資料專案**：管理核心資料和資料市集檢視表存取權的控管範圍。資料會複製並維護至區域資料集，可供全球團隊使用。
* **ETL 基礎架構**：用於將上游資料來源處理成核心資料的基礎架構。視管理區隔需求而定，您可以選擇將 ETL 基礎架構部署為獨立專案，或做為核心資料專案的一部分。
* **數據分析團隊專案**：資料市集的消費者會使用這些專案，並使用自己佈建的基礎架構，處理資料市集區域資料集內的資料。數據分析團隊專案應能建立衍生資料集，供本機使用。

[BigQuery 資料移轉服務](https://docs.cloud.google.com/bigquery/docs/dts-introduction?hl=zh-tw)是額外的排程元件，有一些限制。內建服務排程器的最短間隔時間為 15 分鐘，且必須複製來源資料集中的所有資料表。您無法在 BigQuery 資料移轉服務排程器中嵌入其他指令碼，建立區域專屬資料子集。

如果貴組織需要更多彈性，可以選擇下列選項：

* **Managed Service for Apache Airflow 工作**：您可以排定 [Managed Service for Apache Airflow](https://docs.cloud.google.com/composer?hl=zh-tw) 工作，發出建立區域子集的 ETL 工作，然後透過[用戶端 API](https://docs.cloud.google.com/bigquery/docs/reference/libraries?hl=zh-tw) 觸發 BigQuery 資料移轉服務。如果貴機構可以接受額外延遲，建議採用這個選項。
* **ETL 基礎架構**：ETL 基礎架構 (例如 Dataflow) 可將區域子集雙重寫入目標區域。如果貴組織要求區域之間的資料延遲時間降到最低，建議您選擇這個選項。

## 分散式權限的資料市集

如需依系統擁有者、業務範圍或地理位置區分管理權限，請使用分散式授權。

與標準資料市集相比，去中心化資料市集有下列不同的考量：

* **安全資料協作**：透過技術控管機制共用資料，盡可能減少團隊間不當存取。
* **資料可探索性**：團隊必須能夠探索及要求存取資料集。
* **資料來源**：在沒有中央管理團隊的情況下，團隊必須能夠信任分析產品的資料來源。

### 委派核心資料管理

這種設計與傳統的資料市集方法不同，因為去中心化授權會將核心資料管理決策委派給組織的元件子群組。使用分散式授權時，您可以透過 [Cloud Key Management Service (Cloud KMS)](https://docs.cloud.google.com/security-key-management?hl=zh-tw)、資料欄政策、VPC Service Controls 和預留項目，集中控管安全性和 BigQuery 容量。因此，您可避免自行管理的倉儲中常見的資料蔓延問題。下圖顯示使用分散式授權的架構：

**圖 5.** 核心管理專案有助於確保安全性一致，同時個別群組可維護其資料作業。

圖 5 的專案設定包含下列專案：

* **核心管理專案**：負責跨組織管理事宜的專案。在這個專案中，您會建立 Cloud KMS 金鑰環和 Data Catalog 欄政策等安全性資源。這項專案會做為 BigQuery [預留項目管理專案](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#admin-project)，在整個組織內共用運算單元。
* **組織單位資料專案**：在更廣泛的組織中，自行管理資料市集的擁有者。核心管理專案會管理組織單位資料專案的受限範圍。
* **數據分析團隊專案**：資料市集消費者使用的專案。這些專案會使用自己佈建的基礎架構和運算單元，存取及處理資料市集中的資料。

### 採用兩層式預留項目設計

建議分散式資料市集採用與標準資料市集[相同的兩層式設計](#data-marts-central-reservation)。在這個設定中，您會為[組織資源](https://docs.cloud.google.com/resource-manager/docs/cloud-platform-resource-hierarchy?hl=zh-tw#organizations)指派少量運算單元的預留項目，以因應一般用量。如果團隊有更多需求，請在專案或資料夾層級指派預留項目。

### 使用 Data Catalog

Data Catalog 提供全組織探索、中繼資料標記和資料欄政策設定。Knowledge Catalog 探索功能會自動為貴組織的所有新 BigQuery 資料表建立[中繼資料項目](https://docs.cloud.google.com/knowledge-catalog/docs/catalog-overview?hl=zh-tw)。Knowledge Catalog 的功能也有助於資料治理管理員快速識別新的資料資產，並套用適當的控管措施。

### 設定 VPC Service Controls perimeter

在這種設定中，建議您使用 VPC Service Controls 範圍，防止 BigQuery 資料集意外公開至Google Cloud 組織外部。

#### Perimeter

在這種設定中，建議您建立下列 service perimeter：

* **核心資料**：保護資料倉儲和資料市集資料集的 perimeter。這個 perimeter 應包含所有組織單位專案和資料治理專案。
* **Analytics**：這個 perimeter 用於在組織內部建構及部署數據分析資產。這個 perimeter 的存取政策應比與其橋接的核心資料 perimeter 更寬鬆。

#### Perimeter bridge

在這種設定中，建議您建立下列 perimeter bridge：

* **核心資料和數據分析**：允許數據分析專案中的使用者查詢授權檢視表。

## 多組織資料共用

設計資料市集時，必須特別考量多組織共用。這種資料共用設計適用於想與其他實體安全共用資料集的組織，且該實體擁有自己的 Google 組織。

多組織資料共用功能可解決資料共用者的下列問題：

* **共用機密性**：只有預定對象可以存取共用資料。
* **防止不當存取**：只有預定存取的資源才能從外部存取。
* **運算分離**：外部方會依據他們發起的查詢付費。

**注意：** 在某些情況下，來自外部組織的查詢可能會意外失敗。[Cloud Customer Care](https://cloud.google.com/support-hub/?hl=zh-tw) 可協助您變更設定，解決問題。

### 保護內部專案，避免共用資料專案

多組織資料共用設計著重於保護組織的內部專案，不受共用資料專案中的活動影響。共用資料集專案可做為緩衝區，禁止存取機密的內部資料處理作業，同時提供對外共用資料的功能。

從外部專案發出的查詢會使用叫用專案的運算資源。如果所有查詢的資料集都位於同一個 Google Cloud區域，這些查詢就能彙整不同組織的資料。下圖顯示在多機構專案設定中，資料集的共用方式：

**圖 6**：外部組織查詢共用專案中多個資料集的資料。

圖 6 中的專案設定包含下列專案：

* **組織內部專案**：包含機密內部資料的專案。內部專案可以將經過清理的資料複製到共用資料專案的資料集，藉此對外共用資料。內部專案應擁有負責更新共用資料的服務帳戶。
* **共用資料專案**：包含從內部專案複製的經過清理資訊。使用外部使用者[群組](https://docs.cloud.google.com/iam/docs/groups-in-cloud-console?hl=zh-tw)管理外部人員的存取權。在這種情況下，您會以管理員身分管理群組成員資格，並授予外部帳戶檢視者權限，讓他們可以透過這些群組存取資料集。

### 設定 VPC Service Controls perimeter

在這種設定下，建議您使用 VPC Service Controls 範圍，對外共用資料，並防止 BigQuery 資料集意外在內部專案外公開。

#### Perimeter

在這種設定中，建議您建立下列 service perimeter：

* **內部資料**：保護核心資料資產的 perimeter。VPC Service Controls 會強制執行 BigQuery 存取權。
* **對外共用資料**：這個 perimeter 託管的資料集可與外部組織共用。這個 perimeter 會停用 BigQuery 存取權強制執行功能。

#### Perimeter bridge

在這種設定中，建議您建立下列 perimeter bridge：

* **內部到外部資料**：perimeter 橋接允許受保護程度較高的內部資料專案，將資料輸出至外部資料共用專案。

## 多租戶系統的其他考量

本節將深入探討特殊情況，您可以與上述最佳做法一併考量。

### Google Cloud 資源限制和配額

* 服務帳戶的軟性配額限制為每項專案 100 個服務帳戶。如果專案維護租戶服務帳戶，您可以透過 [Google Cloud 控制台](https://console.cloud.google.com/iam-admin/quotas?hl=zh-tw)申請配額。
* BigQuery 的預設並行查詢數量為每個發出查詢的專案 100 個 (存放資料集的專案沒有這類限制)。如要提高這項軟性配額，請與業務代表聯絡。
* VPC Service Controls 限制整個組織的 service perimeter 內最多只能有 10,000 個專案。如果每個租戶專案設計的擴充程度很高，建議改用每個租戶資料集設計。
* VPC Service Controls 限制每個組織最多可有 100 個 perimeter，包括 bridge。

### 使用授權檢視表或具體化子集資料表

如要管理租戶對大型事實資料表子集的存取權，您可以使用租戶專屬的授權檢視表，或建立租戶專屬的子集資料表。下表比較這些方法：

| 功能 | 授權檢視表 | 子集資料表 |
| --- | --- | --- |
| 支援的租戶數量 | 每個資料集的授權資源數量上限為 [2,500 個](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#dataset_limits)。 | 授權資源包括授權檢視表、授權資料集和授權函式。專案中的資料集數量或資料集中的資料表數量沒有限制。 |
| 分區與分群 | 授權檢視表必須與基礎資料表共用相同的分區和叢集配置。  為提升租戶區隔的效能，建議您依據租戶 ID 建立父項資料表的叢集。 | 您可以根據租戶的需求，對子集資料表進行分區和分群。 |
| 區域規劃 | 授權檢視表不得跨區域，且必須位於基礎資料表的 Google Cloud 區域。區域化會影響地理位置偏遠的租戶。 | 子集資料表可以位於最適合租戶的區域。可能需要支付額外[費用](https://docs.cloud.google.com/bigquery/docs/copying-datasets?hl=zh-tw#pricing)。 |
| 資料欄政策強制執行 | 套用至基礎資料表的資料欄政策會套用至所有授權檢視表，無論這些檢視表的權限為何。 | 每個子集資料表都必須套用資料欄政策，政策才會生效。 |
| 資料存取記錄 | 資料存取記錄會反映在基礎資料表的記錄中。 | 系統會分別記錄每個子集資料表的存取活動。 |
| 轉換彈性 | 授權檢視表可讓您立即重新設計租戶存取的物件。 | 如要變更子集資料表，必須進行複雜的結構定義變更。 |

### 控管機密資料

為防止未經授權存取資料，BigQuery 提供多項標準 IAM 權限以外的額外功能。

#### 用戶端提供的加密金鑰

用戶端資料加密涵蓋代管機構代表租戶儲存及處理資料，但無法存取部分資料內容的情況。舉例來說，代管機構可能無法存取視為機密的個人或裝置資料。

建議資料傳送者使用開放原始碼 [Tink 程式庫](https://github.com/google/tink)中的 AEAD 加密金鑰，加密機密資料。Tink 程式庫 AEAD 加密金鑰與 [BigQuery AEAD 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/aead_encryption_functions?hl=zh-tw)相容。接著，租戶可以透過[授權 UDF](https://docs.cloud.google.com/bigquery/docs/user-defined-functions?hl=zh-tw#authorize_routines) 存取金鑰內容，或將金鑰內容做為[查詢參數](https://docs.cloud.google.com/bigquery/docs/parameterized-queries?hl=zh-tw#bq)傳遞至 BigQuery，藉此解密資料，而主辦機構無法記錄金鑰。

#### 資料欄存取政策

在多租戶資料市集中，資料欄政策通常用於防止機密內容意外在協作團隊之間外洩。在資料市集情境中，授權檢視表是團隊之間共用資料的首選機制。授權檢視表無法授予受保護資料欄的存取權。

如果將政策設為強制執行存取控管，未獲授予政策[精細讀取者](https://docs.cloud.google.com/bigquery/docs/column-level-security?hl=zh-tw#fine_grained_reader)角色的使用者就無法存取。即使未強制執行政策，政策也會記錄所有使用者對分類資料欄的存取。

#### Sensitive Data Protection

[Sensitive Data Protection](https://docs.cloud.google.com/sensitive-data-protection?hl=zh-tw) 提供 API 和掃描公用程式，可協助您找出並減少儲存在 BigQuery 或 [Cloud Storage](https://docs.cloud.google.com/storage?hl=zh-tw) 資料集中的機密內容。在多租戶情境中，組織經常使用 DLP API (Sensitive Data Protection 的一部分) 來識別機密資料，並視需要將其權杖化，然後再儲存。

### 運算單元預留項目管理

在多租戶系統中，預留項目管理功能有助於在租戶擴充時控管成本，並確保每個租戶都能享有保證效能。

如要管理預留項目，建議您建立單一預留項目管理專案。在同一個管理專案中購買的運算單元承諾使用合約，可由該管理專案產生的所有[預留項目](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#admin-project)共用。使用運算單元承諾使用合約的專案，一次只能指派給一個預留項目。[源自專案](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs/insert?hl=zh-tw#path-parameters)的所有查詢，會根據可用資源共用運算單元。

為確保達成租戶服務水準目標 (SLO)，您可以透過 Cloud Logging 和 BigQuery [資訊架構](https://docs.cloud.google.com/bigquery/docs/information-schema-jobs?hl=zh-tw)[監控](https://docs.cloud.google.com/bigquery/docs/reservations-monitoring?hl=zh-tw)預留項目。如果組織在分析師活動或優先工作期間較為忙碌，可以使用[彈性運算單元](https://cloud.google.com/bigquery/pricing?hl=zh-tw#flex-slots-pricing)分配額外運算資源。

#### 預留項目做為租戶運算層

SaaS 供應商通常有數十到數千個租戶，因此會將有限數量的 BigQuery 預留項目設為共用資源。

如果您是共用租戶基礎架構的 SaaS 供應商，建議您將每個預留項目專用於單一專案，並將租戶分組，共用該專案進行 BigQuery 運算。這種設計可減少管理數千個額外專案和預留項目的負擔，同時讓組織分配必要的最低[運算單元容量](https://docs.cloud.google.com/bigquery/docs/reference/reservations/rest/v1/projects.locations.reservations?hl=zh-tw)，滿足預留項目的預期效能需求。

如果 [ELT 資料處理](https://wikipedia.org/wiki/Extract,_transform,_load#Vs._ELT)時效性是首要考量，建議您分配預留項目來處理。如要避免使用可能用於臨時工作負載的額外運算單元，請將預留項目設為[忽略閒置運算單元](https://docs.cloud.google.com/bigquery/docs/slots?hl=zh-tw#idle_slots)。

以下範例說明如何將預留項目設為租戶運算級別：

* **資料處理**：2, 000 個運算單元，忽略閒置。這項預留項目已設為符合資料處理服務等級目標。
* **內部專案**：1, 000 個運算單元，允許閒置。這項預留項目會套用至用於內部數據分析的專案。如果資料處理或運算層有剩餘的運算單元，系統會重複使用這些運算單元。
* **低運算層級**：2, 000 個運算單元，忽略閒置。這項預留項目會套用至資源不足的租戶。與高層級不同，這個預留項目會忽略閒置的運算單元。
* **高運算層級**：3, 000 個運算單元，允許閒置。這項預留項目適用於獲得大量資源的租戶。為加快查詢速度，系統會自動套用其他預留項目的閒置運算單元。

如果租戶在專屬基礎架構上運作，建議您將指定資料夾或專案指派給適當的共用預留項目。

#### 每個團隊的預留項目數量

在資料市集設定中與團隊合作時，建議您為每個需要額外運算資源的團隊建立預留項目。接著將該預留項目指派給包含團隊專案的上層資料夾。該團隊的所有新專案都會使用相同資源分配中的[公平排程](https://docs.cloud.google.com/bigquery/docs/slots?hl=zh-tw#fair_scheduling_in_bigquery)運算單元。

以下範例說明如何為各團隊設定預留項目：

* **組織層級預留項目**：500 個運算單元，允許閒置。這項預留項目會指派給頂層機構，並將運算單元提供給任何 BigQuery 使用者，前提是他們使用的專案沒有專屬預留項目
* **資料處理**：1, 000 個運算單元，忽略閒置。這項預留項目已設為符合最低資料處理服務等級目標。
* **核心資料管理**：500 個運算單元，允許閒置。這項預留項目會套用至用於內部管理的專案。如果資料處理或運算層有剩餘運算單元，系統會重複使用。
* **Analytics 處理預留項目**：500 個運算單元，允許閒置。這是提供給數據分析團隊的專屬預留項目。

### 多區域託管規定

多區域託管需求通常是為了減少消費者的資料延遲，或符合法規要求。

Google Cloud 中的專案視為全域專案，可在任何區域佈建資源。BigQuery 將資料集、資料欄政策和運算單元承諾使用合約視為區域性資源。運算單元只能存取本機區域中的資料集，資料欄政策也只能套用至本機資料集內的資料表。如要使用依用量計費的定價模式，您必須在每個含有資料集的區域購買運算單元。

如需遵守法規要求的指引，請洽詢業務代表。

## 後續步驟

* 瞭解 [IAM 最佳做法](https://docs.cloud.google.com/iam/docs/recommender-best-practices?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-10-24 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-10-24 (世界標準時間)。"],[],[]]