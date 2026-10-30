Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 瞭解預留項目

本頁面說明如何使用預留運算單元管理 BigQuery 工作負載。

## 運算單元保留項目

在 BigQuery 中，[運算單元](https://docs.cloud.google.com/bigquery/docs/slots?hl=zh-tw)會分配到稱為「預留項目」的集區。預留項目可讓您以適合貴組織的方式管理容量及隔離工作負載。舉例來說，您可以為正式環境工作負載建立名為 `prod` 的預留項目，並為測試建立名為 `test` 的獨立預留項目，這樣測試工作就不會與正式環境工作爭奪資源。或者，您也可以為組織中的不同部門建立預留項目，以便分配運算成本。

管理員也可以根據指派給預留項目的工作負載，設定運算單元容量。舉例來說，如果您有正式環境等級、具時效性的工作負載，請建立具有足夠基準運算單元的預留項目。

分配後，基準運算單元會持續提供給預留項目，但能否增加基準運算單元，取決於目前的系統容量。相較之下，使用自動調度資源預留項目時，BigQuery 不會預先保留基準和預留項目大小上限之間的容量。BigQuery 會根據您的需求和系統可用性，自動調整這項容量。自動調度資源預留項目預設以秒計費，至少會產生一分鐘的基本費用。您可以在預留項目層級選擇加入 [BigQuery 流暢擴充](https://docs.cloud.google.com/bigquery/docs/slots?hl=zh-tw#fluid-scaling)，按秒計費，且沒有最短使用時間限制。此外，[閒置運算單元](https://docs.cloud.google.com/bigquery/docs/slots?hl=zh-tw#idle_slots)可供多個預留項目共用。

## 預留項目指派作業

如要使用預留項目中分配到的運算單元，您必須將其*指派*給一或多個專案、資料夾或組織。專案中的工作執行時，會使用指派預留項目的運算單元。資源可以從[Google Cloud 資源階層](https://docs.cloud.google.com/resource-manager/docs/cloud-platform-resource-hierarchy?hl=zh-tw)中的父項繼承指派項目。如果專案未指派給預留項目，則會沿用上層資料夾或組織的指派項目 (如有)。

專案會使用資源階層中最明確的單一預留項目。資料夾指派作業會覆寫組織指派作業，專案指派作業則會覆寫資料夾指派作業。

如果專案沒有指派或繼承的預留項目，則工作會採用隨選計價模式。如要進一步瞭解如何整理 BigQuery 資源，請參閱「[資源階層簡介](https://docs.cloud.google.com/bigquery/docs/resource-hierarchy?hl=zh-tw)」。

資源可以指派給 `None`，代表沒有指派項目。指派給 `None` 的專案一律採用隨選計價方案。`None` 指派作業的常見用途是將組織指派給預留項目，然後使用 `None` 將特定專案或資料夾從該預留項目中排除。詳情請參閱「[將專案指派給 `None`](https://docs.cloud.google.com/bigquery/docs/reservations-assignments?hl=zh-tw#assign-project-to-none)」。

建立指派作業時，您必須指定該指派作業的工作類型：

* `QUERY`：將這項預留項目用於非持續查詢工作，包括 SQL、DDL、DML 和 BigQuery ML (內建模型) 查詢。
* `AUTOMATIC_MATERIALIZED_VIEW_REFRESH`：將這個預留項目用於[自動具體化檢視表重新整理](https://docs.cloud.google.com/bigquery/docs/materialized-views-manage?hl=zh-tw#automatic-refresh)工作。
* `BACKGROUND_CHANGE_DATA_CAPTURE`：選擇[使用自己的預留項目](https://docs.cloud.google.com/bigquery/docs/search-index?hl=zh-tw#use_your_own_reservation)執行 [BigQuery CDC 擷取](https://docs.cloud.google.com/bigquery/docs/change-data-capture?hl=zh-tw)背景工作時，請使用這個預留項目。Standard 版本不提供`BACKGROUND_CHANGE_DATA_CAPTURE`預留項目。
* `BACKGROUND_COLUMN_METADATA_INDEX`：選擇[使用自己的預留項目](https://docs.cloud.google.com/bigquery/docs/search-index?hl=zh-tw#use_your_own_reservation)執行 [BigLake 中繼資料快取](https://docs.cloud.google.com/bigquery/docs/metadata-caching-external-tables?hl=zh-tw)背景工作時，請使用這個預留項目。使用 Datastream 的背景套用作業，將來源資料庫複製到 BigQuery 時，也請使用這項預留項目。Standard 版本不提供`BACKGROUND_COLUMN_METADATA_INDEX`預留項目。
* `BACKGROUND_SEARCH_INDEX_REFRESH`：選擇[使用自己的預留項目](https://docs.cloud.google.com/bigquery/docs/search-index?hl=zh-tw#use_your_own_reservation)執行 [BigQuery 搜尋](https://docs.cloud.google.com/bigquery/docs/search-intro?hl=zh-tw)索引管理背景工作時，請使用這個預留項目。Standard 版本不提供`BACKGROUND_SEARCH_INDEX_REFRESH`預留項目。
* `BACKGROUND`：選擇[使用自己的預留項目](https://docs.cloud.google.com/bigquery/docs/search-index?hl=zh-tw#use_your_own_reservation)，透過 Datastream 的背景套用作業，將來源資料庫複製到 BigQuery 時，請使用這個預留項目。如果沒有更明確的預留項目，這項預留項目也會做為備用，用於 `BACKGROUND_CHANGE_DATA_CAPTURE`、`BACKGROUND_COLUMN_METADATA_INDEX` 和 `BACKGROUND_SEARCH_INDEX_REFRESH` 描述的工作。Standard 版本不提供`BACKGROUND`預留項目。
* `CONTINUOUS`：將這個預留項目用於[持續查詢](https://docs.cloud.google.com/bigquery/docs/continuous-queries-introduction?hl=zh-tw)工作。
* `ML_EXTERNAL`：將這項預留項目用於 BigQuery ML [`CREATE MODEL`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create?hl=zh-tw) 查詢，這些查詢會使用 BigQuery 外部的服務。詳情請參閱「[將運算單元指派給 BigQuery ML 工作負載](https://docs.cloud.google.com/bigquery/docs/reservations-assignments?hl=zh-tw#assign-ml-workload)」。Standard 版本不提供 `ML_EXTERNAL` 預留項目。
* `PIPELINE`：將這項預留項目用於載入和擷取工作。

  根據預設，載入和擷取工作為[免費](https://cloud.google.com/bigquery/pricing?hl=zh-tw#free)，並使用共用的運算單元集區。BigQuery 不保證這個共用集區的容量可用性，也不保證您看到的處理量。如果您要載入大量資料，工作可能會等待運算單元釋出。

  將載入和擷取工作指派給預留項目後，這些工作就無法再存取免費集區。請[監控資源使用率和工作](https://docs.cloud.google.com/bigquery/docs/admin-resource-charts?hl=zh-tw)，確保預留項目有足夠的容量，可在所需的工作時間內完成。

您無法將個別運算單元分配給特定作業。BigQuery 排程器會使用預留項目，為工作分配運算單元。如要進一步瞭解運算單元的使用方式，請參閱「[BigQuery 中的公平排程](https://docs.cloud.google.com/bigquery/docs/slots?hl=zh-tw#fair_scheduling_in_bigquery)」。

### 彈性指派預留項目

BigQuery 可讓您指定查詢在執行階段應使用的預留項目。這樣一來，您就能進一步控管資源分配，避免建立不必要的專案。您可以在執行階段使用 [CLI](https://docs.cloud.google.com/bigquery/docs/reservations-assignments?hl=zh-tw#bq_3)、[UI](https://docs.cloud.google.com/bigquery/docs/reservations-assignments?hl=zh-tw#console_2)、[SQL](https://docs.cloud.google.com/bigquery/docs/reservations-assignments?hl=zh-tw#sql_3) 或 [API](https://docs.cloud.google.com/bigquery/docs/reservations-assignments?hl=zh-tw#api) 指定預留項目，覆寫專案、資料夾或組織的預設預留項目指派。指派的預留項目必須與您執行的查詢位於相同區域。所有[版本](https://docs.cloud.google.com/bigquery/docs/editions-intro?hl=zh-tw)都支援這些指派作業。

您必須[具備預留項目的存取權](#securable)，才能在執行查詢時使用預留項目。

如果預設指派的預留項目版本為 Enterprise Plus，則只能由 Enterprise Plus 預留項目覆寫。

如要彈性指派預留項目，請[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)並指定預留項目。

### 結合預留項目與隨選計費模式

您可以在某個區域使用依運算能力計費模式，在另一個區域使用隨選模式。根據預設，所有專案都採用隨選計費模式。在區域內，您可以將專案、資料夾或組織指派給預留項目，選擇採用依用量計費模式。舉例來說，如果您在美國多區域購買運算單元承諾使用合約，並將組織指派給預設預留項目，則組織在美國多區域會採用依運算能力計費模式，但在所有其他區域仍會採用隨選計費模式。

在區域內，您可以明確將專案指派給預留項目，藉此結合依運算能力計費和隨選計費模式。未指派預留項目的專案會繼續採用隨選計費模式。您也可以指派預留項目 ID `none`，明確指派專案使用隨選計費模式。如果您將資料夾或組織指派給預留項目，但希望該資料夾或組織中的某些專案使用隨選計費模式，這項功能就非常實用。詳情請參閱「[將專案指派給『無』](https://docs.cloud.google.com/bigquery/docs/reservations-assignments?hl=zh-tw#assign-project-to-none)」。

採用隨選計費模式的專案，其容量與承諾使用容量分開計算。這些專案不會影響承諾使用資源的可用性。如果您查詢串流緩衝區中的資料，系統不會針對從串流緩衝區處理的位元組，向隨選工作收取費用，但預留項目中執行的工作會使用運算單元處理這些位元組。

## 指定管理專案

建立承諾使用合約和預留項目時，這些項目會與 Google Cloud 專案建立關聯。這個專案會管理 BigQuery 預留項目資源，也是這些資源的主要計費來源。這個專案不一定要與存放 BigQuery 工作或資料集的專案相同。

建議您為預留資源建立專屬專案。這項專案稱為「管理」專案，因為它會集中管理承諾使用合約的計費和管理作業。為這項專案提供描述性名稱，例如 `bq-COMPANY_NAME-admin`。然後建立一或多個獨立專案，用於存放 BigQuery 工作。

只有與管理專案位於相同[組織資源](https://docs.cloud.google.com/resource-manager/docs/creating-managing-organization?hl=zh-tw)中的專案，才能指派給預留項目。如果管理專案不屬於任何組織，則只有該專案可以使用運算單元。

系統會針對管理專案收取承諾使用運算單元的費用。使用運算單元的專案會產生儲存空間費用，但不會產生運算單元費用。您可以購買多種方案 (例如年約和三年約)，並將運算單元放入同一個管理專案。

**注意：** 建立預留項目或承諾使用合約後，就無法移至其他管理專案。

建議您限制管理專案的數量。這有助於簡化帳單管理和運算單元分配作業。建議您盡可能為貴組織的所有預留項目建立一個管理專案。複雜的組織可能需要額外的管理專案，才能滿足管理或計費需求。

### 使用多個管理專案

在某些情況下，您可能需要建立多個管理專案：

* 將多個預留項目和承諾使用合約的費用，分到不同的組織單位。
* 將一或多個運算單元承諾使用合約對應至不同的預留項目組合。

閒置運算單元容量不會在不同管理專案的預留項目之間共用。

在 BigQuery Google Cloud 控制台的「Workload management」(工作負載管理) 頁面中，您只能查看所選管理專案的預留項目和承諾使用合約。

## 專案上限和排程政策

**預覽**

這項功能適用《[服務專屬條款](https://docs.cloud.google.com/terms/service-terms?hl=zh-tw#1)》中「一般服務條款」一節的《正式發布前產品條款》。正式發布前功能是依「原樣」提供，支援服務可能受限。
詳情請參閱[推出階段說明](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages)。

如要尋求支援或針對這項功能提供意見回饋，請傳送電子郵件至 [bigquery-wlm-feedback@google.com](mailto:bigquery-wlm-feedback@google.com)。

專案上限 (也稱為排程政策) 可讓您為使用預留項目的專案設定用量和並行限制，自訂預設的[公平排程](https://docs.cloud.google.com/bigquery/docs/slots?hl=zh-tw#fair_scheduling_in_bigquery)行為。這些限制可防止專案耗用過多運算單元，即使專案在公平排程下有資格獲得更多容量。

您可以在預留項目層級設定專案上限，做為預設限制。除非遭到覆寫，否則這些限制會套用至使用該預留項目的所有專案。或者，您也可以將專案上限設為個別專案的[專案專屬覆寫](https://docs.cloud.google.com/bigquery/docs/reservations-assignments?hl=zh-tw#scheduling-policy-assignments)。

支援的專案數量上限類型如下：

* **運算單元數量上限：**限制預留項目中，指派對象專案執行查詢時的運算單元用量。最小值為 100。
  這並非嚴格限制，而是約略上限。
* **並行數量上限：**限制預留項目中，指派對象專案可同時執行的查詢數量。

  並行上限僅在查詢准入時套用，不會導致執行中的查詢取消。如果將並行上限調降至低於目前執行中的查詢數量，新查詢會排入佇列，直到有足夠的執行中查詢完成為止。

變更這些設定時，請注意下列限制：

* 變更最多需要一分鐘才會生效。
* 修改每項專案的運算單元數量上限覆寫設定後，必須啟動新查詢才會生效。

如要進一步瞭解如何設定這些政策，請參閱「[管理工作負載指派作業](https://docs.cloud.google.com/bigquery/docs/reservations-assignments?hl=zh-tw)」和「[管理工作負載預留項目](https://docs.cloud.google.com/bigquery/docs/reservations-tasks?hl=zh-tw)」。

## 預留運算單元數量

BigQuery 的架構會隨著資源量增加而呈線性成長。視工作負載而定，容量增加可能會帶來更多效能。不過，增加容量也會提高費用。因此，請根據您對效能、處理量和公用程式的需求，選擇最佳的運算單元購買數量。

新增基準運算單元或提高自動調度資源上限時，BigQuery 排程器會為個別查詢指派更多運算單元，盡可能提高平行處理能力。雖然這會縮短查詢執行時間，但並行 worker 負擔可能會導致查詢耗用的總運算單元時間 (`total_slot_ms`) 增加。

您可以嘗試使用基準和自動調度資源運算單元，找出最佳的運算單元設定。舉例來說，您可以先使用 500 個基準運算單元測試工作負載，接著再使用 1,000、1,500 和 2,000 個基準運算單元，並觀察對效能的影響。

如果測試效能的區域有可用的閒置運算單元，預留項目可能會以低於預期的運算單元數量達到效能。這是因為預留項目使用閒置運算單元來滿足工作負載的運算單元需求。如果其他預留項目的工作負載變更，導致閒置運算單元可用性降低，工作負載效能可能會下降。因此，對於正式環境層級、有時間限制的工作負載，請確保預留項目在運算單元容量方面能自給自足。這可避免閒置運算單元的變更直接影響工作效能。

分配運算單元並執行工作負載至少七天後，您可以使用[運算單元估算工具](https://docs.cloud.google.com/bigquery/docs/slot-estimator?hl=zh-tw)分析效能，並模擬新增或減少運算單元的影響。

您也可以查看專案目前的運算單元用量，以及選擇要支付的月費。隨選工作負載的運算單元上限為 2,000 個，但請務必使用 [`INFORMATION_SCHEMA.JOBS*` 檢視表](https://docs.cloud.google.com/bigquery/docs/information-schema-jobs?hl=zh-tw)、Cloud Logging、Jobs API 或 BigQuery 稽核記錄，檢查專案實際使用的運算單元數量。詳情請參閱「[監控預留項目](https://docs.cloud.google.com/bigquery/docs/reservations-monitoring?hl=zh-tw)」。

## 使用預留項目管理工作負載

您可以使用 BigQuery 預留項目，建立額外的預留項目並將專案指派給這些預留項目，藉此在工作負載、團隊或部門之間分配容量。預留項目是獨立的資源集區，可讓您充分運用貴組織在特定區域的閒置容量。

舉例來說，假設您承諾使用的總容量為 1,000 個運算單元，且有三種工作負載類型：資料科學、ELT 和 BI。

* 您可以建立具有 500 個運算單元的`ds`預留項目，並將所有相關 Google Cloud 專案指派給`ds`預留項目。
* 您可以建立具有 300 個運算單元的 `elt` 保留項目，並將用於 ELT 工作負載的專案指派給該 `elt` 保留項目。
* 您可以建立具有 200 個運算單元的 `bi` 保留項目，並將連結至您的 BI 工具的專案指派給該 `bi` 保留項目。

除了依工作負載類型劃分運算資源，您也可以選擇為個別團隊或部門建立預留項目。有了自動調度資源功能，您就能在多個預留項目之間隔離工作負載，更靈活、更精細地管理工作負載。

### 管理不同區域的預留項目

預留項目是區域性資源。在一個地區購買的運算單元和建立的保留項目不能在任何其他地區使用。專案、資料夾和組織可以指派給某個區域的預留項目，並在另一個區域中隨選執行。如要管理其他區域的預留項目，請在 BigQuery 的「Workload management」(工作負載管理) 頁面變更區域：

1. 在 BigQuery 控制台中，點選「預留項目」。
2. 按一下「Location」(位置) 挑選器，然後選取要管理預留項目的區域。
3. 選取區域後，您可以購買運算單元、建立預留項目，以及將專案指派給預留項目。

### 管理複雜組織中的預留項目

預留項目是組織範圍的資源。建立預留項目時，您可以將運算資源指派給同一 Google Cloud組織中的任何專案。大多數 BigQuery 使用者會使用單一管理專案，處理預留項目和承諾使用合約。這個管理專案與 Cloud Billing 帳戶相關聯，該帳戶會依容量計費。

不過，如果您的組織較為複雜，有多個部門自行管理帳單，則建議使用多個管理專案。請注意，[閒置運算單元](https://docs.cloud.google.com/bigquery/docs/slots?hl=zh-tw#idle_slots)只能在相同管理專案中建立的預留項目之間共用。請留意預留項目和管理專案的[配額與限制](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#reservations)。

如果您使用多個 Google Cloud 組織，則必須為每個組織建立至少一個管理專案，然後在相關聯的管理專案中，管理各個組織的預留項目和承諾使用合約。無法跨組織共用容量。

**注意：** [變更連結至專案的 Cloud Billing 帳戶](https://docs.cloud.google.com/billing/docs/how-to/modify-project?hl=zh-tw#change_the_billing_account_for_a_project)，不會導致現有承諾使用合約和預留項目停機。運算單元會連結至專案或組織，且與 Cloud Billing 帳戶無關。

### 管理預留項目的進階控制項

BigQuery 的預留項目可讓您進一步控管預留項目的使用方式，並提供額外的安全防護功能。您可以定義政策，指定哪些使用者或群組可以存取及使用特定預留項目。這可確保機密資料和工作負載受到隔離和保護。預留項目管理員可以精確控管哪些使用者或服務帳戶 (主體) 有權使用特定預留項目。方法是將 IAM 條件套用至管理專案 (管理預留項目的專案)。

舉例來說，您可以建立 IAM 條件，將 `reservations.use` 權限授予特定使用者群組，讓他們能存取名稱開頭為特定前置字串的所有預留項目。這樣就能管理一組相關預留項目的存取權。

使用者必須具備 `reservations.use` 權限，才能覆寫工作的預設預留項目，或在專案已有預留項目指派作業時，強制工作依隨選方式執行。`roles/bigquery.resourceAdmin` 和 `roles/bigquery.resourceEditor` 角色提供這項權限。您可以將存取權授予個別使用者、群組或服務帳戶。您也可以根據預留項目屬性 (例如名稱) 定義政策，因為 IAM 條件支援屬性式存取控管。

如要授予預留項目的 IAM 條件，請參閱「[控管預留項目的存取權](https://docs.cloud.google.com/bigquery/docs/reservations-tasks?hl=zh-tw#control_access_to_reservations)」。

## 運算單元承諾使用合約

「運算單元承諾使用合約」是指在指定時間範圍內購買運算單元。購買運算單元時，每次可增加 50 個，最多可達[區域運算單元配額](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#reservations)。容量承諾使用合約為選用項目，但可為穩定狀態的工作負載節省成本。運算單元承諾使用合約用於支付預留項目的基準運算單元費用。任何未使用的運算單元容量，都會做為閒置運算單元，與其他預留項目共用。運算單元承諾使用合約不適用於自動調度資源運算單元。為確保您能以折扣費率使用承諾的運算單元，請確認承諾的運算單元數量足以涵蓋基準運算單元。可建立的使用承諾數量沒有限制。從您成功購買承諾使用合約的那一刻起，系統就會開始收費。如要瞭解目前的定價資訊，請參閱「[容量承諾使用合約定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#capacity_compute_analysis_pricing)」。

* **年約制承諾使用合約**。您購買了 365 天的承諾使用合約。365 天後，您可以選擇續約或轉換為其他類型的承諾使用合約方案。
* **承諾使用三年**。您購買了三年承諾使用合約。3 年 (1,095 天) 後，您可以選擇續約或轉換為其他類型的約期授權方案。

承諾期結束後，系統會根據[所選續約方案](#renew-commitments)續約。

年約或三年約方案是按月計費，但財務承諾涵蓋整個承諾期，無法按月取消。帳單報表中的用量資料每天都會更新，您隨時可以查看。

運算單元承諾使用合約會受可用容量影響。嘗試購買運算單元承諾使用合約時，不保證一定能成功。不過，成功購買承諾使用合約後，您就能使用該容量，直到合約到期為止。

如果您在建立預留項目之前購買運算單元承諾使用合約，系統會自動建立名為 `default` 的預留項目，方便您使用。`default` 預留項目沒有特殊行為。您可以視需要建立其他預留項目，或使用預設預留項目。

建議您為預留項目指派非零基準，以獲得最可預測的效能和初始容量。雖然您可以設定基準運算單元為零的預留項目，並設定容量上限，以便使用自動調度資源功能，但這種做法的效果完全取決於是否正確啟用自動調度資源，以及是否主動取得運算單元。如果自動調度資源功能無法有效運作，這類零基準預留項目會改為僅依賴可用的閒置運算單元容量，這無法保證效能，且可能導致查詢速度不穩定或降低。

### 續約

購買合約時，您需要選取續約方案。在承諾使用合約到期前，您隨時可以變更續約方案。可用的續約方案如下：

* **無。**承諾期結束後，承諾使用合約就會移除。預留項目不受影響。
* **按年。**承諾期結束後，承諾會再續約一年。
* **三年。**承諾期結束後，承諾使用合約會再續約三年。

**警告：** 取消或允許運算單元承諾使用合約到期，並不會刪除或取消佈建相關聯的預留項目或指派作業。凡是設有基準運算單元的預留項目，都會繼續按照[即付即用費率](https://cloud.google.com/bigquery/pricing?hl=zh-tw#on_demand_pricing)產生基準運算單元時數費用。如要停止基準運算單元時數費用，並改回隨選計費，您必須在Google Cloud 控制台手動[刪除所有預留項目](https://docs.cloud.google.com/bigquery/docs/reservations-tasks?hl=zh-tw#delete_reservations)，並[刪除所有預留項目指派作業](https://docs.cloud.google.com/bigquery/docs/reservations-assignments?hl=zh-tw)。

如要瞭解如何購買及續約承諾使用合約，請參閱「[建立運算資源承諾使用合約](https://docs.cloud.google.com/bigquery/docs/reservations-commitments?hl=zh-tw#create_a_capacity_commitment)」。

舉例來說，如果您在 2019 年 10 月 5 日下午 6:00 購買年約方案，系統會立即開始計費。您可以在 2020 年 10 月 4 日下午 6:00 後刪除或續約承諾使用合約，請注意 2020 年是閏年。您可以在 2020 年 10 月 4 日下午 6:00 前變更續訂方案，方法如下：

* 如果您選擇續約年約，則在 2020 年 10 月 4 日下午 6:00，您的合約會續約一年。
* 如果您選擇續約三年承諾使用合約，則在 2020 年 10 月 4 日下午 6:00，您的承諾使用合約會續約三年。

**注意：**承諾使用合約到期後，續約程序最多可能需要約一小時。舉例來說，如果承諾使用合約在 2020 年 10 月 4 日下午 6:00 到期，續約記錄會在 2020 年 10 月 4 日下午 6:00 到 7:00 之間顯示在系統中。由於建立的承諾使用合約生效時間為下午 6:00，因此在這段資料更新期間內，不會產生任何隨選費用。

### 承諾使用合約到期

承諾使用合約一經建立即無法刪除。如要刪除年約或三年約方案，請將續約方案設為 `NONE`。使用承諾到期後，系統會自動刪除。如要進一步瞭解承諾使用合約到期，請參閱「[承諾使用合約到期](https://docs.cloud.google.com/bigquery/docs/reservations-commitments?hl=zh-tw#commitment_expiration)」。

如果您不小心購買承諾使用合約，或是在設定承諾使用合約時發生錯誤，請向 [Cloud Customer Care](https://cloud.google.com/support-hub?hl=zh-tw) 尋求協助。

## 預留項目限制

* 某個組織的預留項目無法與其他組織共用。
* 您必須為每個組織使用不同的預留項目和管理專案。
* 每個組織在單一位置最多可有 10 個管理專案，且這些專案須有有效的預留項目。
* 閒置運算資源無法在組織之間共用，也無法在單一組織內的不同管理專案之間共用。
* 閒置運算能力無法跨區域共用。
* 承諾使用合約和預留項目是[區域性資源](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw#specify_locations)。在某個區域或多區域購買的使用承諾，無法用於其他區域或多區域的預留項目，即使單一區域位置與多區域位置位於同一地點也一樣。舉例來說，您無法將在 `EU` 多區域購買的使用承諾用於 `europe-west4` 的預留項目。
* 承諾使用合約和預留項目無法從某個區域或多區域移至其他區域。
* 在某個管理專案中購買的使用承諾，無法移至其他管理專案。
* 以某個[版本](https://docs.cloud.google.com/bigquery/docs/editions-intro?hl=zh-tw)購買的使用承諾，無法用於其他版本的預留項目。
* 不同[版本](https://docs.cloud.google.com/bigquery/docs/editions-intro?hl=zh-tw)的預留項目不會共用閒置運算單元。
* [自動調度資源的運算單元](https://docs.cloud.google.com/bigquery/docs/slots?hl=zh-tw#slot-autoscaling)無法共用，因為不再需要時會縮減。

## 預留項目的可預測性

如要使用預留項目可預測性，請先啟用[預留項目公平性](https://docs.cloud.google.com/bigquery/docs/slots?hl=zh-tw#fairness)。

預留項目可預測性可讓您設定預留項目使用的運算單元絕對數量上限。BigQuery 提供基準運算單元、閒置運算單元和自動調度資源運算單元，做為潛在容量資源。建立預留項目並設定大小上限時，請根據過去的工作負載，確認基準運算單元數量，以及自動調度資源和閒置運算單元的適當設定。

如要啟用預留項目可預測性，您必須設定預留項目的運算單元數量上限和調度資源模式。運算單元數量上限必須為正數，且大於指派給預留項目的基準運算單元數量。如要進一步瞭解如何使用預留項目可預測性，請參閱「[建立具有專屬運算單元的預留項目](https://docs.cloud.google.com/bigquery/docs/reservations-tasks?hl=zh-tw#create_a_reservation_with_dedicated_slots)」。在預留項目設定運算單元數量上限時，無法設定 `autoscale_max_slots` 的值。

`ignore_idle_slots` 的值必須與調度資源模式一致。如果縮放模式為 `ALL_SLOTS` 或 `IDLE_SLOTS_ONLY`，`ignore_idle_slots` 必須為 false。如果縮放模式為 `AUTOSCALE_ONLY`，`ignore_idle_slots` 必須為 true。

您可以設定預留項目，只使用下列容量資源組合，最多不超過定義的上限：

* **基準運算單元 + 閒置運算單元**：預留項目運算單元數量大於零，且資源調度模式為 `IDLE_SLOTS_ONLY`。預留項目會使用設定的基準數量和可用的閒置運算單元，最多不超過運算單元數量上限。如果沒有足夠的閒置運算單元，預留項目可能無法達到上限。
* **基準運算單元 + 閒置運算單元 + 自動調度資源運算單元**：預留項目運算單元容量大於零，且調度資源模式為 `ALL_SLOTS`。預留項目會先使用設定的基準運算單元數量，接著使用所有可用的閒置運算單元，最後才會使用自動調度資源運算單元。
* **基準運算單元 + 自動調度資源運算單元**：預留項目運算單元容量大於零，且調度模式為 `AUTOSCALE_ONLY`。預留項目會先使用設定的基準運算單元，再使用自動調度資源運算單元。
* **閒置運算單元 + 自動調度資源運算單元**：預留項目運算單元容量為零，且調度模式為 `ALL_SLOTS`。預留項目會先使用所有可用的閒置運算單元，接著才會使用自動調度資源運算單元。
* **閒置運算單元**：預留項目運算單元容量為零，且調度資源模式為 `IDLE_SLOTS_ONLY`。預留項目會使用所有可用的閒置運算單元，但不會超過設定的上限。如果可用的閒置運算單元不足，預留項目可能無法達到上限。

下圖顯示可用的不同設定選項：

圖中顯示五種設定選項，說明 BigQuery 如何使用運算單元，直到達到設定的上限。前三個選項包含基準運算單元，其他選項則未設定基準運算單元。

### 限制

預留項目可預測性有下列限制：

* 除非選擇`AUTOSCALE_ONLY`選項，否則只有 Enterprise 和 Enterprise Plus 版本提供預留項目可預測性。
* 預留項目的可預測性會盡可能達到最佳。整體用量仍可能超過設定的上限。

### 後續步驟

* 如要進一步瞭解如何使用預留項目可預測性，請參閱「[建立具有專屬運算單元的預留項目](https://docs.cloud.google.com/bigquery/docs/reservations-tasks?hl=zh-tw#create_a_reservation_with_dedicated_slots)」。

## 預留項目群組

如要使用預留項目群組，請先啟用[預留項目公平性](https://docs.cloud.google.com/bigquery/docs/slots?hl=zh-tw#fairness)。

預留項目群組可讓您管理多個預留項目的屬性，就像資料集整理資料表一樣。

預留項目會先與同一個預留項目群組中的其他預留項目共用閒置運算單元，然後才開放給組織使用：

### 與預留項目群組共用閒置運算單元

閒置運算單元會先平均分配給未分組的預留項目和預留項目群組，再平均分配給預留項目群組。

在以下範例中，有三個預留項目和 1,200 個閒置運算單元。如果沒有預留項目群組，每個預留項目會平均分配到 400 個閒置運算單元。將預留項目 1 和 2 分組後，閒置運算單元的分配方式會改變。閒置運算單元會先平均分配給預留項目群組和預留項目 3 (兩者各 600 個閒置運算單元)。接著，預留項目群組的 600 個閒置運算單元會平均分配給預留項目 1 和 2。

### 限制

預留項目群組有下列限制：

* 共用預留項目群組的預留項目必須屬於相同專案和區域。
* 專案必須啟用[以預留項目為基礎的公平性機制](https://docs.cloud.google.com/bigquery/docs/slots?hl=zh-tw#fairness)。
* 群組中的預留項目必須使用相同的[版本](https://docs.cloud.google.com/bigquery/docs/editions-intro?hl=zh-tw)。
* 在同一個群組中，您無法混用有[代管災難復原](https://docs.cloud.google.com/bigquery/docs/managed-disaster-recovery?hl=zh-tw)設定和沒有這類設定的預留項目。群組中的所有預留項目都必須設定災難復原功能，或全部停用。
* 如果群組中的預留項目已啟用災難復原功能，則所有預留項目的主要和次要位置都必須使用同一組區域。

如要進一步瞭解如何使用預留項目群組，請參閱「[使用預留項目群組排定閒置運算單元的優先順序](https://docs.cloud.google.com/bigquery/docs/reservations-tasks?hl=zh-tw#prioritize_idle_slots_with_reservation_groups)」。

## 排解預訂問題

請參考下列資訊，排解預留項目的常見問題，例如新增運算單元時發生錯誤、預留項目未用於 BigQuery 工作，或無法辨識預留項目。

### 無法增加預留項目大小

嘗試在預留項目中新增更多運算單元時，如果遇到 `Failed to allocate slots for reservation in the
current system state` 或 `Failed to update reservation: Failed to allocate slots
for reservation` 等錯誤，通常是暫時性問題。如要緩解問題，請按照下列步驟操作：

* 請減少運算單元數量，然後重試。
* 如果嘗試使用較少的運算單元失敗，請等待 15 分鐘，然後重試作業。

如果重試多次並等待 30 分鐘後，仍收到相同錯誤，請[與 Cloud Customer Care 聯絡](https://docs.cloud.google.com/bigquery/docs/getting-support?hl=zh-tw)。

### 配額不足，無法完成這項要求

如果錯誤訊息顯示 `There is insufficient quota to complete this
request`，表示要求超出專案設定的配額限制。

如要解決這個錯誤，請執行下列任一操作：

* 在預留項目中新增較少的運算單元，確保要求不會超出配額限制。
* 請在對應區域申請提高配額。詳情請參閱「[要求提高配額](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#requesting_a_quota_increase)」。

### BigQuery 未使用預留項目執行工作

在多種情況下，工作可能會使用[隨選計價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#on_demand_pricing)或免費共用運算單元集區，而非您建立的預留項目。

#### 查詢和預留項目位於不同區域

預留項目是區域性資源。查詢會在與查詢中參照的任何資料表相同的位置執行。

如果資料表的位置與預留項目不符，查詢就不會使用預留項目，而是按照隨選定價執行 (或符合資格的批次載入和匯出工作，則使用免費共用運算單元集區)。

#### 查詢 BigQuery Omni 資料表

查詢 BigQuery Omni 資料表時，請務必在資料表所在的區域建立預留項目，而非共置區域。如果您在共置的 BigQuery 區域建立預留項目，系統會按照隨選定價模式執行查詢。

#### 預留項目已建立，但專案未指派給該項目

如要使用預留項目中的運算單元，您必須建立指派作業，將專案、資料夾或組織指派給特定預留項目。確認專案有[對應的預留項目指派作業](https://docs.cloud.google.com/bigquery/docs/reservations-assignments?hl=zh-tw)。

#### 工作類型不符

建立工作時，請務必選取正確的[工作類型](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#assignments)，否則工作不會使用預留項目。

舉例來說，如果選取 `PIPELINE` 做為工作類型，所有查詢工作都會以隨選計價模式執行。將指派類型變更為 `QUERY`，即可使用預留項目執行查詢工作。

#### 多陳述式查詢

如果您執行多重陳述式查詢，即使子項工作是在預留項目下執行，父項工作物件也不會有相關聯的預留項目。

如要確認工作是否確實使用預留項目，請查看子工作的中繼資料。

#### 正在擷取快取結果

查詢工作擷取快取結果時，預留項目欄位會留空，因為 BigQuery 不會執行任何運算，而是直接從臨時資料表擷取結果。

#### 變更資料擷取資料列修改作業

如果您有[變更資料擷取 (CDC) 資料表](https://docs.cloud.google.com/bigquery/docs/change-data-capture?hl=zh-tw)，BigQuery 會在 `max_staleness` 間隔內，以使用 `BACKGROUND` 指派類型的背景工作，套用待處理的資料列修改。如果沒有 `BACKGROUND` 指派作業，這些工作會採用隨選定價。建議您為專案建立`BACKGROUND`指派作業，以免產生非預期的隨選費用。您可以透過工作 ID 中的 `queueworker_cdc_background_merge_coalesce` 子字串，識別這些工作。

#### 使用外部服務的 BigQuery ML 模型類型

如果專案中找不到 `ML_EXTERNAL` 工作類型的預留項目指派作業，系統會依據隨選定價模式執行外部模型建立工作。`QUERY` 工作類型指派作業適用於標準 BigQuery ML 模型和矩陣分解模型 (需要 Enterprise 或 Enterprise Plus 版本預留項目)，而外部模型則需要 `ML_EXTERNAL` 指派作業。詳情請參閱「[將運算單元指派給 BigQuery 工作負載](https://docs.cloud.google.com/bigquery/docs/reservations-assignments?hl=zh-tw#assign-ml-workload)」。

### 在專案中發現無法辨識的預留項目

BigQuery 擁有預留項目，代表 BigQuery 中特定作業的免費共用運算單元集區。

#### `default-pipeline`

根據預設，在 BigQuery 中批次載入或批次匯出資料時，會使用免費的共用運算單元集區。檢查這些載入或擷取工作時，預留項目欄位會顯示 `default-pipeline`。

使用共用運算單元集區不會產生費用。如要獲得穩定、可預測的效能，建議您購買 `PIPELINE` 預留項目。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-10-29 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-10-29 (世界標準時間)。"],[],[]]