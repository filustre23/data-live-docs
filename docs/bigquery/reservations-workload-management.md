Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 瞭解預留項目

本頁面說明如何使用時段預留，管理 BigQuery 工作負載。

## 運算單元保留項目

在 BigQuery 中，[運算單元](https://docs.cloud.google.com/bigquery/docs/slots?hl=zh-tw)會分配到稱為「預留」的集區。您可以透過預留項目管理容量，並以符合貴機構需求的方式隔離工作負載。舉例來說，您可以為實際工作環境工作負載建立名為 `prod` 的預留項目，並為測試建立名為 `test` 的預留項目，這樣測試作業就不會與實際工作環境作業爭用資源。或者，您也可以為機構中的不同部門建立預訂，以分配運算費用。

管理員也可以根據指派的預留項目，設定運算單元處理量。舉例來說，如果您有生產層級、對時間敏感的工作負載，請建立預留項目，並提供足夠的基準運算單元。基準運算單元一律可用，可確保預留項目始終有足夠的容量。不過，如果您使用自動調整規模的預留項目，預留項目中的容量不一定會預留。使用[自動調度資源預留容量](https://docs.cloud.google.com/bigquery/docs/slots-autoscaling-intro?hl=zh-tw)時，系統會根據需求自動調度容量。自動調度資源預訂項目預設會以秒計費，最少為一分鐘。您可以選擇在預訂層級啟用 [BigQuery 彈性調度](https://docs.cloud.google.com/bigquery/docs/slots?hl=zh-tw#fluid-scaling)，以依秒計費，且沒有最短時間限制。此外，[閒置運算單元](https://docs.cloud.google.com/bigquery/docs/slots?hl=zh-tw#idle_slots)可供多個預留項目共用。

## 指派的預留項目

如要在預留項目中使用已分配的配額，您必須將預留項目*指派*給一或多個專案、資料夾或機構。專案中的作業執行時，會使用指派給該專案的預留項目配額。資源可以從[Google Cloud 資源階層](https://docs.cloud.google.com/resource-manager/docs/cloud-platform-resource-hierarchy?hl=zh-tw)中的上層資源繼承指派作業。如果專案未指派給預留項目，則會繼承上層資料夾或機構的指派作業 (如有)。

專案會使用資源階層中最具體的單一指派保留項目。資料夾指派作業會覆寫機構指派作業，專案指派作業則會覆寫資料夾指派作業。

如果專案沒有指派或沿用的預訂方案，工作就會採用以量計價方案。如要進一步瞭解資源階層，請參閱[整理 BigQuery 資源](https://docs.cloud.google.com/bigquery/docs/resource-hierarchy?hl=zh-tw)。

資源可以指派給 `None`，代表沒有指派作業。指派給 `None` 的專案一律會採用依用量計價方式。`None` 指派作業的常見用途是將機構指派給保留項目，然後使用 `None` 將特定專案或資料夾排除在該保留項目之外。詳情請參閱「[將專案指派給 `None`](https://docs.cloud.google.com/bigquery/docs/reservations-assignments?hl=zh-tw#assign-project-to-none)」。

建立指派項目時，請指定該指派項目的工作類型：

* `QUERY`：將此預留項目用於非連續查詢作業，包括 SQL、DDL、DML 和 BigQuery ML (內建模型) 查詢。
* `BACKGROUND_CHANGE_DATA_CAPTURE`：選擇[使用自己的預留資源](https://docs.cloud.google.com/bigquery/docs/search-index?hl=zh-tw#use_your_own_reservation)來執行 [BigQuery CDC 擷取](https://docs.cloud.google.com/bigquery/docs/change-data-capture?hl=zh-tw)背景工作時，請使用這項預留資源。`BACKGROUND_CHANGE_DATA_CAPTURE` 預留資源不適用於標準版。
* `BACKGROUND_COLUMN_METADATA_INDEX`：選擇[使用自己的預留量](https://docs.cloud.google.com/bigquery/docs/search-index?hl=zh-tw#use_your_own_reservation)來執行 [BigLake 中繼資料快取](https://docs.cloud.google.com/bigquery/docs/metadata-caching?hl=zh-tw)背景工作時，請使用這項預留量。使用 Datastream 的背景套用作業將來源資料庫複製到 BigQuery 時，也請使用這項預留空間。標準版不提供`BACKGROUND_COLUMN_METADATA_INDEX`預訂功能。
* `BACKGROUND_SEARCH_INDEX_REFRESH`：選擇[使用自己的預留項目](https://docs.cloud.google.com/bigquery/docs/search-index?hl=zh-tw#use_your_own_reservation)來執行 [BigQuery 搜尋](https://docs.cloud.google.com/bigquery/docs/search-intro?hl=zh-tw)索引管理背景工作時，請使用這個預留項目。標準版不提供`BACKGROUND_SEARCH_INDEX_REFRESH`預訂功能。
* `BACKGROUND`：選擇[使用自己的預留量](https://docs.cloud.google.com/bigquery/docs/search-index?hl=zh-tw#use_your_own_reservation)，透過 Datastream 的背景套用作業將來源資料庫複製到 BigQuery 時，請使用這項預留量。如果沒有更具體的預留量可供 `BACKGROUND_CHANGE_DATA_CAPTURE`、`BACKGROUND_COLUMN_METADATA_INDEX` 和 `BACKGROUND_SEARCH_INDEX_REFRESH` 所述工作類型使用，系統也會將這項預留量做為備援。標準版不提供 `BACKGROUND` 預留量。
* `CONTINUOUS`：請使用這項預留位置執行[持續查詢](https://docs.cloud.google.com/bigquery/docs/continuous-queries-introduction?hl=zh-tw)工作。
* `ML_EXTERNAL`：將此預留項目用於使用 BigQuery 外部服務的 BigQuery ML 查詢。[`CREATE MODEL`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create?hl=zh-tw)詳情請參閱「[將運算單元指派給 BigQuery ML 工作負載](https://docs.cloud.google.com/bigquery/docs/reservations-assignments?hl=zh-tw#assign-ml-workload)」。標準版不提供 `ML_EXTERNAL` 預訂功能。
* `PIPELINE`：使用這項預留項目執行載入和擷取工作。

  根據預設，載入和擷取工作[免費](https://cloud.google.com/bigquery/pricing?hl=zh-tw#free)，且使用共用運算單元集區。BigQuery 不保證這個共用集區的可用容量或您所看到的總處理量。如果您載入大量資料，工作可能會等待運算單元可用。

  載入和擷取工作指派給保留項目後，就無法再使用免費集區。您應[監控資源用量和工作](https://docs.cloud.google.com/bigquery/docs/admin-resource-charts?hl=zh-tw)，確保保留項目有足夠容量，可滿足所需的工作持續時間。

您無法將個別運算單元分配給特定指派項目。BigQuery 排程器會使用預留項目處理工作的運算單元分配作業。如要進一步瞭解運算單元的使用方式，請參閱 [BigQuery 中的公平排程](https://docs.cloud.google.com/bigquery/docs/slots?hl=zh-tw#fair_scheduling_in_bigquery)。

### 彈性指派預留項目

BigQuery 可讓您在執行階段指定查詢應執行的預留項目，進一步控管資源分配，避免建立不必要的專案。您可以使用 [CLI](https://docs.cloud.google.com/bigquery/docs/reservations-assignments?hl=zh-tw#bq_3)、[UI](https://docs.cloud.google.com/bigquery/docs/reservations-assignments?hl=zh-tw#console_2)、[SQL](https://docs.cloud.google.com/bigquery/docs/reservations-assignments?hl=zh-tw#sql_3) 或 [API](https://docs.cloud.google.com/bigquery/docs/reservations-assignments?hl=zh-tw#api)，在執行階段指定預留項目，覆寫專案、資料夾或組織的預設預留項目指派。指派的預留項目必須與您執行的查詢位於相同區域。所有[版本](https://docs.cloud.google.com/bigquery/docs/editions-intro?hl=zh-tw)都支援這些指派。

您必須[有預訂的存取權](#securable)，才能在執行查詢時使用預訂。

如果預設指派的預訂版本為 Enterprise Plus，則只能使用 Enterprise Plus 預訂覆寫。

如要彈性指派預留項目，請[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)並指定預留項目。

### 結合預留項目與隨需帳單

您可以在一個地區使用以量計價模式，在另一個地區使用隨選計價模式。根據預設，所有專案都會採用隨選計價模式。在一個地區內，您可以將專案、資料夾或機構指派給預留項目，選擇採用以量計價模式。舉例來說，如果您在美國多區域購買運算單元承諾使用，並將機構指派給預設的預留項目，機構在美國多區域就會採用以量計價模式，但在所有其他地區仍會採用隨選計價模式。

在一個區域內，您可以明確指派專案給預留項目，藉此結合以量計價和隨選計費。未指派給預留項目的專案會繼續採用隨選計費。您也可以指派預留項目 ID `none`，明確指派專案使用隨選計費。如果您將資料夾或機構指派給預留項目，但希望該資料夾或機構中的部分專案使用隨選計費，這項功能就非常實用。詳情請參閱「[指派專案給『無』](https://docs.cloud.google.com/bigquery/docs/reservations-assignments?hl=zh-tw#assign-project-to-none)」。

採用以量計價的專案會使用與已承諾容量不同的容量。這類專案不會影響已承諾容量的可用性。如果您查詢串流緩衝區中的資料，系統不會針對以量計價作業從串流緩衝區處理的位元組收費，但預留空間中執行的作業會使用配額處理這些位元組。

## 指定管理專案

建立承諾和預留項目時，這些項目會與 Google Cloud 專案建立關聯。
這個專案會管理 BigQuery 保留項目資源，也會設為這些資源的主要帳單來源。這個專案不必與存放 BigQuery 工作或資料集的專案相同。

最佳做法是為預留項目資源建立專屬專案。這個專案稱為「管理」專案，因為它會集中管理承諾的帳單和管理作業。請為這個專案提供描述性名稱，例如 `bq-COMPANY_NAME-admin`。然後建立一或多個獨立專案，用於存放 BigQuery 工作。

只有與管理專案位於相同[機構資源](https://docs.cloud.google.com/resource-manager/docs/creating-managing-organization?hl=zh-tw)的專案，才能指派給預留項目。如果管理專案不屬於任何機構，則只有該專案可以使用運算單元。

系統會向管理專案收取已承諾的配額費用。使用運算單元的專案會產生儲存空間費用，但不會產生運算單元費用。您可以購買多種方案 (例如年約和三年約)，並將配額放入同一個管理專案。

**注意：** 建立預訂或承諾後，就無法將其移至其他管理專案。

最佳做法是限制管理專案的數量，這樣有助於簡化帳單管理和配額分配。建議您盡可能為機構的所有預訂項目使用一個管理專案。複雜的機構可能需要額外的管理專案，才能滿足管理或帳單需求。

### 使用多個管理專案

在某些情況下，您可能會想建立多個管理專案：

* 將多個預訂和承諾的費用分攤到不同機構單位。
* 將一或多個空位承諾對應至不同預訂組合。

不同管理專案的預留項目不會共用閒置運算單元處理量。

在 BigQuery Google Cloud 控制台的「容量管理」頁面中，您只能查看所選管理專案的預留項目和承諾。

## 調整運算單元預留資源大小

BigQuery 的架構會隨著資源量增加而呈線性成長。視工作負載而定，容量增加可能會帶來更多效能。不過，增加容量也會提高費用。因此，要購買的最佳運算單元數量取決於您的效能、總處理量和公用程式需求。

您可以實驗基準和自動調度資源的配額，找出最佳的配額設定。舉例來說，您可以先以 500 個基準配額測試工作負載，然後依序測試 1,000 個、1,500 個和 2,000 個，並觀察對效能的影響。

如果測試效能的區域有閒置運算單元，預留項目可能會以比預期少的運算單元達到效能。這是因為預留項目使用閒置運算單元來滿足工作負載的運算單元需求。如果其他預訂項目的工作負載變更導致閒置運算單元減少，工作負載效能可能會降低。因此，對於生產層級的時限工作負載，請確保預留項目在運算單元容量方面可自給自足。這樣一來，閒置時段的變更就不會直接影響工作成效。

分配運算單元並執行工作負載至少七天後，您可以使用[運算單元估算工具](https://docs.cloud.google.com/bigquery/docs/slot-estimator?hl=zh-tw)分析成效，並模擬增減運算單元的效果。

您也可以檢查專案目前的運算單元用量，以及您希望支付的每月費用。隨選工作負載的軟性運算單元上限為 2,000 個，但請務必使用 [`INFORMATION_SCHEMA.JOBS*` 檢視畫面](https://docs.cloud.google.com/bigquery/docs/information-schema-jobs?hl=zh-tw)、Cloud Logging、Jobs API 或 BigQuery 稽核記錄，檢查專案實際使用的運算單元數量。詳情請參閱「[監控預留項目](https://docs.cloud.google.com/bigquery/docs/reservations-monitoring?hl=zh-tw)」。

## 使用預留項目管理工作負載

您可以建立額外的保留項目，並將專案指派給這些保留項目，藉此使用 BigQuery 保留項目在工作負載、團隊或部門之間分配容量。保留項目是獨立的資源集區，可讓您在機構中特定區域的閒置容量中獲益。

舉例來說，您可能有 1,000 個運算單元的承諾總容量和 3 種工作負載類型：資料科學、ELT 和 BI。

* 您可以建立具有 500 個運算單元的 `ds` 保留項目，並將所有相關 Google Cloud 專案指派給該 `ds` 保留項目。
* 您可以建立具有 300 個運算單元的 `elt` 保留項目，並將用於 ELT 工作負載的專案指派給該 `elt` 保留項目。
* 您可以建立具有 200 個運算單元的 `bi` 保留項目，並將連結至您的 BI 工具的專案指派給該 `bi` 保留項目。

您可以選擇為個別團隊或部門建立保留項目，而不是在多個工作負載類型之間劃分容量。透過自動調度資源，您可以在多個預訂項目中隔離工作負載，提供更彈性且精細的工作負載管理。

### 管理不同地區的預訂

預訂是區域資源。在一個地區購買的運算單元和建立的保留項目不能在任何其他地區使用。專案、資料夾和機構都可以指派給一個地區內的保留項目，並在另一個地區內隨選執行。如要管理其他區域的預留項目，請在 BigQuery「容量管理」頁面中變更區域：

1. 在 BigQuery 控制台中，按一下「保留項目」。
2. 按一下「位置」選擇工具，然後選取要管理預訂的地區。
3. 選取區域後，您可以購買運算單元、建立預留項目，以及將專案指派給預留項目。

### 管理複雜機構的預訂

預留項目是機構範圍內的資源。建立預留項目後，您可以將容量指派給同一機構內的任何專案。大多數 BigQuery 使用者會為預留項目和承諾使用單一管理專案。這個管理專案會與 Cloud Billing 帳戶建立關聯，容量費用會計入該帳戶。 Google Cloud

不過，如果貴機構結構複雜，有多個部門各自管理帳單，您可能需要使用多個管理專案。請注意，[閒置配額](https://docs.cloud.google.com/bigquery/docs/slots?hl=zh-tw#idle_slots)只能在同一個管理專案中建立的預訂之間共用。您應瞭解預訂和管理專案的[配額和限制](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#reservations)。

如果您使用多個 Google Cloud 機構，則必須為每個機構建立至少一個管理專案，然後在相關管理專案中管理每個機構的預訂和承諾。您無法跨機構共用容量。

**注意：** [變更連結至專案的 Cloud Billing 帳戶](https://docs.cloud.google.com/billing/docs/how-to/modify-project?hl=zh-tw#change_the_billing_account_for_a_project)，不會造成現有約定和預訂項目停機。配額會連結至專案或機構，與 Cloud Billing 帳戶無關。

### 加強控管預訂

BigQuery 的預留項目可進一步控管預留項目的使用方式，並提供額外的安全性功能。您可以定義政策，指定哪些使用者或群組可以存取及使用特定預訂項目。確保機密資料和工作負載受到隔離和保護。預訂管理員可以精確控管哪些使用者或服務帳戶 (主體) 獲授權使用特定預訂。如要這麼做，請使用套用至管理專案 (管理預留項目的專案) 的 IAM 條件。

舉例來說，您可以建立 IAM 條件，將 `reservations.use` 權限授予特定使用者群組，適用於名稱開頭為特定前置字元的所有預訂項目。方便您管理相關預訂的存取權。

如要覆寫工作的預設預訂項目，或在專案已指派預訂項目時強制工作隨選執行，使用者必須具備 `reservations.use` 權限。`roles/bigquery.resourceAdmin` 和 `roles/bigquery.resourceEditor` 角色提供這項權限。您可以授予個別使用者、群組或服務帳戶存取權。您也可以根據預訂項目屬性 (例如名稱) 定義政策，因為 IAM 條件支援以屬性為準的存取控管。

如要授予預留項目的 IAM 條件，請參閱「[控管預留項目的存取權](https://docs.cloud.google.com/bigquery/docs/reservations-tasks?hl=zh-tw#control_access_to_reservations)」。

## 運算單元承諾使用合約

*運算單元承諾使用合約*是指在特定時間內購買運算單元。您可以購買運算單元，每次購買數量須為 50 個，最多可購買[區域運算單元配額](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#reservations)。容量承諾使用合約為選用項目，但可為穩定狀態的工作負載節省費用。運算單元承諾使用合約可用於支付預留項目的基準運算單元費用。任何未使用的運算單元容量，都會以閒置運算單元的形式，在其他預留項目之間共用。運算單元承諾使用合約不適用於自動調整運算單元。如要確保承諾使用的運算單元享有折扣價，請確認運算單元承諾使用合約足以支付基準運算單元費用。您可以建立的承諾使用合約數量沒有限制。承諾使用合約購買成功後，系統就會開始收費。如需目前的價格資訊，請參閱[容量承諾使用合約價格](https://cloud.google.com/bigquery/pricing?hl=zh-tw#capacity_compute_analysis_pricing)。

* **年約方案**：購買 365 天的合約。365 天後，您可以選擇續約或改用其他類型的合約方案。
* **承諾使用三年**。購買三年期承諾使用合約。3 年 (1,095 天) 後，您可以選擇續約或改用其他類型的約期方案。

使用承諾期結束後，系統會根據[所選續約方案](#renew-commitments)續約。

年約或三年約方案會按月收費，但您必須承諾在整個承諾期內支付費用，無法按月取消。帳單報表每天都會更新用量，您隨時可以查看。

運算單元承諾視可用容量而定。嘗試購買運算單元承諾時，我們不保證能成功購買。不過，一旦您成功購買承諾，系統就會提供足夠的運算能力，直到承諾到期為止。

如果您在建立預留項目之前購買運算單元承諾，系統會自動建立名為 `default` 的預留項目，方便您使用。`default` 預留項目沒有特殊行為。您可以視需要建立其他預留項目，或使用預設預留項目。

建議您為預留項目指派非零的基準，以獲得最可預測的效能和初始容量。雖然您可以設定預留項目，將基準運算單元設為零，並設定最大容量，打算使用自動調度資源功能，但這種做法的成效完全取決於自動調度資源功能是否已正確啟用，以及是否主動取得運算單元。如果這類零基準預留項目的自動調度資源功能無法有效運作，系統就會改為完全依據可用的閒置運算單元容量，但這樣無法保證效能，且可能導致查詢速度不穩定或變慢。

### 續訂承諾使用合約

購買合約時，請選取續約方案。您隨時可以變更合約的續約方案，直到合約到期為止。可用的續訂方案如下：

* **無。**承諾期結束後，系統會移除承諾，但保留項目不受影響。
* **按年**。承諾期結束後，承諾會再續約一年。
* **三年**。承諾期限結束後，承諾會自動續約三年。

如要瞭解如何購買及續訂承諾，請參閱「[建立容量承諾](https://docs.cloud.google.com/bigquery/docs/reservations-commitments?hl=zh-tw#create_a_capacity_commitment)」。

舉例來說，如果您在 2019 年 10 月 5 日下午 6 點購買年約方案，系統會立即開始計費。您可以在 2020 年 10 月 4 日下午 6 點後刪除或續約使用承諾 (請注意，2020 年是閏年)。您可以在 2020 年 10 月 4 日下午 6 點前變更續約方案，方法如下：

* 如果您選擇續約年約，則您的使用承諾會在 2020 年 10 月 4 日下午 6 點整後續約一年。
* 如果您選擇續約三年期方案，則您的使用承諾會在 2020 年 10 月 4 日下午 6 點整續約三年。

**注意：**承諾期限到期後，續約程序最多可能需要約一小時才能完成。舉例來說，如果使用承諾在 2020 年 10 月 4 日下午 6 點到期，系統會在 2020 年 10 月 4 日下午 6 點到 7 點之間，顯示續約的使用承諾記錄。由於建立的約定用量生效時間為下午 6 點，因此在資料更新期間不會產生隨選費用。

### 承諾到期

承諾方案一經建立即無法刪除。
如要刪除年約或三年約，請將續訂方案設為 `NONE`。
承諾到期後，系統會自動刪除。如要進一步瞭解承諾到期日，請參閱「[承諾到期日](https://docs.cloud.google.com/bigquery/docs/reservations-commitments?hl=zh-tw#commitment_expiration)」。

如果您意外購買承諾方案，或在設定承諾方案時發生錯誤，請向 [Cloud Customer Care 團隊](https://cloud.google.com/support-hub?hl=zh-tw)尋求協助。

## 預訂限制

* 一個機構的預訂項目無法與其他機構共用。
* 您必須為每個機構使用單獨的預訂項目和單獨的管理專案。
* 每個機構在單一位置最多可有 10 個管理專案，且這些專案都含有有效預留項目。
* 機構之間或單一機構內的不同管理專案之間，無法共用閒置容量。
* 閒置容量無法在不同區域之間共用。
* 承諾和預訂是[區域資源](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw#specify_locations)。在某個區域或多區域購買的承諾，無法用於其他區域或多區域的預訂，即使單一區域位置與多區域位置位於同一地點也一樣。舉例來說，您無法將在 `EU` 多區域購買的承諾用於 `europe-west4` 的預訂。
* 承諾和預訂無法從一個區域或多區域移至另一個區域。
* 在某個管理專案中購買的承諾無法移至其他管理專案。
* 使用某個[版本](https://docs.cloud.google.com/bigquery/docs/editions-intro?hl=zh-tw)購買的承諾無法用於其他版本的預留項目。
* 不同[版本](https://docs.cloud.google.com/bigquery/docs/editions-intro?hl=zh-tw)的預留項目不會共用閒置運算單元。
* [自動調度資源的空位](https://docs.cloud.google.com/bigquery/docs/slots-autoscaling-intro?hl=zh-tw)不再需要時會縮減，因此無法共用。

## 預訂可預測性

如要使用預留項目預測功能，請先啟用[預留項目公平性](https://docs.cloud.google.com/bigquery/docs/slots?hl=zh-tw#fairness)。

預留項目預測功能可讓您設定預留項目中使用的運算單元絕對上限。BigQuery 提供基準運算單元、閒置運算單元和自動調度資源運算單元，做為潛在的運算能力資源。建立設有大小上限的預留項目時，請根據過去的工作負載，確認基準運算單元數量，並適當設定自動調度資源和閒置運算單元。

如要啟用預留項目預測功能，您必須在預留項目中設定運算單元數量上限和調度模式的值。運算單元數量上限必須是正數，且大於指派給預留項目的基準運算單元數量。如要進一步瞭解如何使用預留項目預測功能，請參閱「[建立具有專屬運算單元的預留項目](https://docs.cloud.google.com/bigquery/docs/reservations-tasks?hl=zh-tw#create_a_reservation_with_dedicated_slots)」。
在預留項目中設定運算單元數量上限值時，您無法設定 `autoscale_max_slots` 的值。

`ignore_idle_slots` 的值必須與縮放模式一致。如果縮放模式為 `ALL_SLOTS` 或 `IDLE_SLOTS_ONLY`，`ignore_idle_slots` 必須為 false。如果縮放模式為 `AUTOSCALE_ONLY`，`ignore_idle_slots` 必須為 true。

您可以設定預留項目，只使用下列容量資源組合，且不得超過定義上限：

* **基準運算單元 + 閒置運算單元**：預留項目的運算單元容量大於零，且調度模式為 `IDLE_SLOTS_ONLY`。預留項目會消耗設定的基準運算單元數量和可用閒置運算單元，但不會超過運算單元數量上限。如果沒有足夠的閒置運算單元，預留項目可能無法達到上限。
* **基準運算單元 + 閒置運算單元 + 自動調度資源運算單元**：預留項目的運算單元容量大於零，且調度模式為 `ALL_SLOTS`。預留項目會先耗用設定的基準運算單元數量，接著是所有可用的閒置運算單元，最後是自動調度資源運算單元。
* **基準運算單元 + 自動調度資源運算單元**：預留運算單元數量大於零，且調度模式為 `AUTOSCALE_ONLY`。預留項目會先耗用設定的基準運算單元，接著是自動調度運算單元。
* **閒置運算單元 + 自動調度資源運算單元**：預留項目的運算單元容量為零，且調度模式為 `ALL_SLOTS`。預留項目會先耗用所有可用的閒置運算單元，然後再耗用自動調度資源運算單元。
* **閒置運算單元**：預留項目的運算單元容量為零，且資源調度模式為 `IDLE_SLOTS_ONLY`。預留項目會耗用所有可用的閒置運算單元，但不會超過設定上限。如果閒置運算單元不足，預留項目可能無法達到上限。

下圖顯示可用的不同設定選項：

在圖表中，五個設定選項顯示 BigQuery 如何耗用運算單元，直到達到設定上限為止。前三個選項包含基準時段，其他選項則未設定基準時段。

### 限制

預留項目的預測功能有下列限制：

* 除非選擇 `AUTOSCALE_ONLY` 選項，否則預訂預測功能僅適用於 Enterprise 和 Enterprise Plus 版本。
* 預留項目預測功能會盡可能提供準確資訊，但整體用量仍可能超過設定上限。

### 後續步驟

* 如要進一步瞭解如何使用預訂預測功能，請參閱「[建立具有專屬時段的預訂](https://docs.cloud.google.com/bigquery/docs/reservations-tasks?hl=zh-tw#create_a_reservation_with_dedicated_slots)」。

## 預留項目群組

如要使用預留項目群組，請先啟用[預留項目公平性](https://docs.cloud.google.com/bigquery/docs/slots?hl=zh-tw#fairness)。

預留項目群組可讓您管理多個預留項目的屬性，類似於資料集整理資料表的方式。

如果預留項目屬於同一個預留項目群組，會先共用閒置運算單元，然後才開放機構使用：

### 與預留項目群組共用閒置運算單元

閒置運算單元會平均分配給未分組的預留項目和預留項目群組，然後再平均分配給預留項目群組。

在以下範例中，有三個預留項目和 1,200 個閒置時段。如果沒有預留項目群組，每個預留項目會平均分配到 400 個閒置運算單元。如果將預留項目 1 和 2 分組，閒置時段的分配情形就會改變。系統會先將閒置運算單元平均分配給預留項目群組和預留項目 3 (兩者各 600 個閒置運算單元)。接著，預留項目群組的 600 個閒置運算單元會平均分配給預留項目 1 和 2。

### 限制

預留群組有下列限制：

* 共用預留項目群組的預留項目必須屬於相同專案和區域。
* 專案必須啟用[以預留項目為基礎的公平性機制](https://docs.cloud.google.com/bigquery/docs/slots?hl=zh-tw#fairness)。
* 群組中的預留項目必須使用相同的[版本](https://docs.cloud.google.com/bigquery/docs/editions-intro?hl=zh-tw)。
* 您無法在同一個群組中，混用有和沒有[受管理災難復原](https://docs.cloud.google.com/bigquery/docs/managed-disaster-recovery?hl=zh-tw)設定的預訂。群組中的所有預訂都必須設定災難復原，或全部都必須停用。
* 如果為群組中的預留項目啟用災難復原功能，所有預留項目都必須使用相同的區域配對做為主要和次要位置。

如要進一步瞭解如何使用預訂群組，請參閱「[使用預訂群組優先處理閒置時段](https://docs.cloud.google.com/bigquery/docs/reservations-tasks?hl=zh-tw#prioritize_idle_slots_with_reservation_groups)」。

## 排解預訂問題

本節旨在協助排解與預留位置互動時遇到的常見問題，例如判斷預留位置未用於 BigQuery 工作的可能原因、找出不明預留位置，或解決新增時段時的問題。

### 無法在預訂大小中新增更多運算單元

如果在嘗試為預訂新增更多空位時遇到 `Failed to allocate slots for reservation in the current system state` 或 `Failed to update reservation: Failed to allocate slots for reservation` 等錯誤，通常是暫時性問題。如要解決，請按照下列步驟操作：

* 請減少預訂的座位數後重試
* 如果減少配額後仍無法完成作業，請等待 15 分鐘再重試

如果多次重試並等待 30 分鐘後，仍收到相同錯誤訊息，請[與 BigQuery 支援團隊聯絡](https://docs.cloud.google.com/bigquery/docs/getting-support?hl=zh-tw)。

### 配額不足，無法完成這項要求

如果錯誤訊息顯示 `There is insufficient quota to complete this request`，表示要求超出專案配額上限。

如要解決這項錯誤，請採取下列任一做法：

1. 在預留項目中新增較少的運算單元，以免超過配額限制。
2. 在相應區域申請提高配額。請參閱「[申請提高配額](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#requesting_a_quota_increase)」。

### BigQuery 未使用預留項目執行工作

在多種情況下，工作可能會使用隨選資源或免費共用運算單元集區執行，而不是使用您建立的預留項目。

#### 查詢和預訂位於不同地區

預訂是區域資源。查詢會在與查詢中參照的任何資料表相同的位置執行。

如果資料表位置與預留項目位置不符，查詢會使用共用運算單元集區執行，不會使用預留項目。

#### 查詢 BigQuery Omni 資料表

查詢 BigQuery Omni 資料表時，請務必在與資料表相同的區域中建立預留項目，而非在共置區域中建立。如果您在同區的 BigQuery 區域建立預留項目，查詢會依需求執行。

#### 已建立預留項目，但未指派專案

如要使用購買的運算單元，請建立指派作業，將專案指派給特定預留項目。請確認專案有[預留項目的對應指派作業](https://docs.cloud.google.com/bigquery/docs/reservations-assignments?hl=zh-tw)。

#### 工作類型不符

建立指派作業時，請務必選取正確的[工作類型](#assignments)，否則工作會使用共用運算單元集區執行。

舉例來說，如果選取 `PIPELINE` 做為工作類型，所有查詢工作都會依需求執行。將指派類型變更為 `QUERY`，即可使用預留項目執行查詢工作。

#### 多陳述式查詢

如果您執行多個陳述式查詢，即使子項工作是在保留項目下執行，父項工作物件也不會與保留項目建立關聯。

如要確認工作是否實際使用保留項目，請查看子項工作的中繼資料。

#### 擷取快取結果

查詢工作擷取快取結果時，由於系統不會執行實際的運算，而是直接從臨時表擷取結果，因此保留欄位會是空白。

#### 變更資料擷取列修改作業

如果您有[變更資料擷取 (CDC) 資料表](https://docs.cloud.google.com/bigquery/docs/change-data-capture?hl=zh-tw)，BigQuery 會在 `max_staleness` 間隔內套用待處理的資料列修改內容，並以 `BACKGROUND` 指派類型做為背景工作。如果沒有 `BACKGROUND` 指派作業，系統會採用隨選方案計價。建議為專案建立 `BACKGROUND` 指派項目，以免產生高昂的隨需費用。您可以在工作 ID 中找出 `queueworker_cdc_background_merge_coalesce` 子字串，藉此識別這些工作。

#### 使用外部服務的 BigQuery ML 模型類型

如果系統在專案中找不到工作類型為 `ML_EXTERNAL` 的保留項目指派作業，查詢作業就會以以量計價模式執行。`QUERY` 工作類型指派作業只能用於非外部模型或矩陣因式分解模型的 BigQuery ML 模型。如要瞭解詳情，請參閱「[保留項目指派作業](https://docs.cloud.google.com/bigquery/docs/reservations-assignments?hl=zh-tw#assign-ml-workload)」說明文件。

### 專案中無法辨識的預留項目

BigQuery 擁有保留項目，代表用於 BigQuery 中特定作業的免費共用運算單元集區：

#### `default-pipeline`

根據預設，在 BigQuery 中批次載入或匯出資料時，會使用共用的免費運算單元集區。檢查這些載入或擷取工作時，系統會將使用的預留項目列為 `default-pipeline`。

使用共用運算單元集區無須支付費用。如要確保效能穩定且可預測，請考慮購買`PIPELINE`預留資源。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-06-12 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-06-12 (世界標準時間)。"],[],[]]