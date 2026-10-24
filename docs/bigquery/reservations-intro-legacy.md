Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 舊版預留項目簡介

**注意：** 舊版預留項目 (包括固定費率計費或特定承諾使用合約長度) 僅適用於許可清單中的客戶。如要確認您是否能存取這些舊版功能，請與管理員聯絡。固定費率計費模式會定義運算資源的計費方式，但固定費率預留項目和承諾使用合約會做為 Enterprise 版運算單元。

BigQuery 預留項目可讓您從[隨選計價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#on_demand_pricing)切換至[依運算資源計價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#capacity_compute_analysis_pricing)。採用運算資源定價模式時，您需要支付專屬或自動調度資源的查詢處理運算資源費用，而非個別查詢的費用。

您可以透過預留項目，將查詢容量 (以[運算單元](https://docs.cloud.google.com/bigquery/docs/slots?hl=zh-tw)為單位) 分配給不同的工作負載或機構的不同部分。

使用 [BigQuery 版本](https://docs.cloud.google.com/bigquery/docs/editions-intro?hl=zh-tw)的預留項目時，不一定要建立[運算資源承諾使用合約](https://docs.cloud.google.com/bigquery/docs/reservations-details?hl=zh-tw)，但可以節省穩定狀態工作負載的費用。

**注意：** [舊版固定費率承諾使用合約](#commitments)可使用的功能，與 [Enterprise 版本](https://docs.cloud.google.com/bigquery/docs/editions-intro?hl=zh-tw)承諾使用合約相同。所有舊版固定費率承諾使用合約的運算計價模式值都會標示為 `flat-rate`，版本值則標示為 `Enterprise`。

## 總覽

BigQuery 提供兩種運算 (分析) 計價模式：

* **[隨選定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#on_demand_pricing)**：您只需為查詢掃描的資料付費。每個專案都有固定的[查詢處理能力](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#max_concurrent_slots_on-demand)，費用則取決於每項查詢處理的位元組數。
* **[以運算資源為基礎的計價模式](https://cloud.google.com/bigquery/pricing?hl=zh-tw#capacity_compute_analysis_pricing)**：您需要為專用或自動調度資源的查詢處理運算資源付費，運算資源是以[運算單元](https://docs.cloud.google.com/bigquery/docs/slots?hl=zh-tw)為單位，並以一段時間為計算基準。多個查詢會共用相同的運算單元容量。

根據預設，系統會按照以量計價的模式向您收費。使用預留項目，即可切換至以運算資源為基礎的定價模式、使用[運算單元自動調度資源](https://docs.cloud.google.com/bigquery/docs/slots-autoscaling-intro?hl=zh-tw)功能，以及購買折扣[運算資源承諾使用合約](https://docs.cloud.google.com/bigquery/docs/reservations-details?hl=zh-tw)。如果採用以容量為基礎的模式，則不會針對處理的位元組收費。

您可以結合兩種計費模式。舉例來說，您可以採用隨選計價模式執行某些工作負載，並採用以運算資源為基礎的計價模式執行其他工作負載。由於計費模式是依專案指定，因此您必須使用多個專案來執行查詢工作。

## 預留項目的優點

使用 BigQuery 預留項目的優點包括：

* **可預測性**。依據運算資源計費的模式，費用可預測且一致。您可以預先指定費用預算上限，也可以利用運算單元承諾使用合約，以折扣費率取得專屬的持續運算資源。
* **高度彈性**。您可以選擇要為工作負載分配多少專屬運算資源，或讓 BigQuery 根據工作負載需求自動調度資源。系統會根據您使用的運算單元計費，基本計費單位為一秒。
* **工作負載管理。**每個工作負載都有指定的 BigQuery 運算資源集區可供使用。同時，如果工作負載未用盡所有專屬運算單元，任何未使用的運算單元都會自動與其他工作負載共用。
* **集中購買：**您可以為整個組織購買及分配運算單元。您不必為每個使用 BigQuery 的專案購買運算單元。

## 預留項目

BigQuery 容量是以[*運算單元*](https://docs.cloud.google.com/bigquery/docs/slots?hl=zh-tw)為單位，代表查詢使用的虛擬 CPU。一般來說，如果佈建更多運算單元，就能執行更多並行查詢，複雜查詢的執行速度也會更快。

運算單元會分配到稱為「預留項目」的集區。預留項目可讓您以適合特定組織的方式分配運算單元。

舉例來說，您可以為正式環境工作負載建立名為 `prod` 的預留項目，並為測試建立名為 `test` 的獨立預留項目。這樣一來，測試工作就不會與正式環境工作負載爭奪所需資源。或者，您也可以為組織中的不同部門建立預留項目。

預留項目可包含一律分配的「基準」運算單元，以及根據工作負載需求[動態新增或移除](https://docs.cloud.google.com/bigquery/docs/slots-autoscaling-intro?hl=zh-tw)的「自動調度」運算單元。

如果您在建立預留項目之前購買運算單元承諾使用合約，系統會自動建立名為 `default` 的預留項目。`default` 預留項目沒有特別之處，只是為了方便而建立。您可以決定是否需要額外預留項目，或只使用預設預留項目。

如要使用分配的運算單元，您必須將一或多個專案「指派」至預留項目，詳情請參閱下一節。

預留項目是指定運算單元分配的最低層級。[預留項目中的運算單元分配](#slot_allocation_within_reservations)由 BigQuery 排程器處理。

## 作業

如要使用分配的運算單元，您必須將一或多個專案、資料夾或組織指派給預留項目。資源階層中的每個層級都會沿用上層的指派項目。換句話說，如果專案或資料夾未指派，則該專案或資料夾會繼承上層資料夾或組織 (如有) 的指派。如要進一步瞭解如何整理 BigQuery 資源，請參閱「[資源階層簡介](https://docs.cloud.google.com/bigquery/docs/resource-hierarchy?hl=zh-tw)」。

如果工作是從指派給預留項目的專案啟動，就會使用該預留項目的運算單元。如果專案未指派給預留項目 (無論是直接指派，或繼承自上層資料夾或組織)，該專案中的工作會採用隨選計價。

`None` 指派項目代表沒有指派項目。指派給 `None` 的專案採用隨選定價。`None` 指派作業的常見用途是將組織指派給預留項目，並將部分專案或資料夾指派給 `None`，藉此從該預留項目中排除這些專案或資料夾。詳情請參閱「[將專案指派給『無』](https://docs.cloud.google.com/bigquery/docs/reservations-assignments?hl=zh-tw#assign-project-to-none)」。

建立指派作業時，您必須指定該指派作業的工作類型：

* `QUERY`：將這項預留項目用於查詢工作，包括 SQL、DDL、DML 和 BigQuery ML 查詢。
* `PIPELINE`：將這項預留項目用於載入和擷取工作。

  根據預設，載入和擷取工作為[免費](https://cloud.google.com/bigquery/pricing?hl=zh-tw#free)，並使用共用的運算單元集區。BigQuery 不保證這個共用集區的可用運算資源或您看到的處理量。如果您要載入大量資料，工作可能會等待運算單元釋出。在這種情況下，建議您購買專屬運算單元，並將管道工作指派給這些運算單元。建議您建立額外的專屬預留項目，並停用閒置運算單元共用功能。

  將載入工作指派給預留項目後，這些工作就無法再存取免費集區。監控效能，確保工作有足夠的容量。否則，成效實際上可能比使用免費集區更差。
* `BACKGROUND`：選擇[使用自己的預留項目](https://docs.cloud.google.com/bigquery/docs/search-index?hl=zh-tw#use_your_own_reservation)，執行 [BigQuery 搜尋](https://docs.cloud.google.com/bigquery/docs/search-intro?hl=zh-tw)索引管理工作，或 [BigQuery 變更資料擷取 (CDC) 擷取](https://docs.cloud.google.com/bigquery/docs/change-data-capture?hl=zh-tw)背景工作時，請使用這個預留項目。使用 Datastream 的背景套用作業，將來源資料庫複製到 BigQuery 時，也請使用這項預留項目。Standard 版本不提供`BACKGROUND`預留項目。
* `ML_EXTERNAL`：將這個預留項目用於使用 BigQuery 外部服務的 BigQuery ML 查詢。詳情請參閱「[將運算單元指派給 BigQuery ML 工作負載](https://docs.cloud.google.com/bigquery/docs/reservations-assignments?hl=zh-tw#assign-ml-workload)」。Standard 版本不提供`ML_EXTERNAL`預留項目。

您無法將運算單元分配給特定作業。BigQuery 排程器會處理預留項目中指派作業的運算單元分配。

## 承諾使用合約

*承諾使用容量*是指購買固定數量的 BigQuery 運算容量，並承諾使用一段時間。使用[版本](https://docs.cloud.google.com/bigquery/docs/editions-intro?hl=zh-tw)建立預留項目時，不一定要承諾使用運算資源，但可節省穩定狀態工作負載的成本。

BigQuery 提供多種承諾使用合約方案供您選擇。主要差異在於費用和最低承諾使用時間。如需目前的定價資訊，請參閱[容量承諾使用合約定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#capacity_compute_analysis_pricing)。

* **年約制承諾使用合約**。您購買了 365 天的承諾使用合約。365 天後，您可以選擇續約或轉換為其他類型的承諾使用合約方案。
* **每月承諾使用合約**。您購買了至少 30 天的承諾使用合約。30 天後，您隨時可以刪除方案。
* **彈性運算單元**：您購買了 60 秒的承諾使用合約。60 秒後即可隨時刪除。在購買長期承諾使用合約前，彈性運算單元是測試工作負載在固定費率計費模式下效能的好方法。此外，這類執行個體也適合用於處理週期性或季節性需求，或報稅季等高負載事件。

無論選擇哪種方案，承諾使用期結束後，運算單元都不會到期。您會保留運算單元，並在刪除前持續支付費用。也可以在最低期限後變更方案類型。

運算單元數量取決於可用容量。嘗試購買運算單元承諾使用合約時，不保證一定能成功。不過，成功購買承諾使用合約後，在您刪除合約之前，容量都會受到保障。

如要進一步瞭解這些方案，請參閱「[承諾使用方案](https://docs.cloud.google.com/bigquery/docs/reservations-details?hl=zh-tw#commitment-plans)」。

## 預留項目中的運算單元分配

BigQuery 會使用稱為「公平排程」的演算法，在單一預留項目中分配運算單元容量。

BigQuery 排程器會強制執行以下規則：在預留項目中，執行查詢的專案會平均分配運算單元，然後在特定專案的工作中，也會平均分配運算單元。排程器最終會提供公平性。在短時間內，某些工作可能會分配到不合比例的運算單元，但排程器最終會修正這個問題。排程器的目標是在過度積極驅逐執行中的工作 (導致浪費運算單元時間) 和過於寬鬆 (導致長時間執行的工作占用過多運算單元時間) 之間找到平衡點。

如果重要工作持續需要比排程器提供的運算單元更多的運算單元，請考慮建立額外的預留項目，並指定保證的運算單元數量，然後將工作指派給該預留項目。詳情請參閱「[工作負載管理](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw)」。

## 閒置的運算單元

在任何時間點，部分運算單元可能處於閒置狀態。這些實用資源包括：

* 未分配給任何預留項目的運算單元承諾使用合約。
* 已分配給預留項目基準，但目前未使用的運算單元。

根據預設，在預留項目中執行的查詢會自動使用相同管理專案中其他預留項目的閒置運算單元。也就是說，只要有容量，工作就能隨時執行。閒置運算資源可立即先占，並視需要返回原先指派的預留項目，無論需要資源的查詢優先順序為何。系統會自動即時執行這項作業。

如要停用這項功能，並強制預留項目僅使用佈建給它的運算單元，請將 `ignore_idle_slots` 設為 `true`。如果預留項目的 `ignore_idle_slots` 設為 `true`，就不會收到閒置運算單元。

不同[版本](https://docs.cloud.google.com/bigquery/docs/editions-intro?hl=zh-tw)的預留項目之間無法共用閒置運算單元。您只能共用基準運算單元或承諾使用運算單元。[自動調度資源運算單元](https://docs.cloud.google.com/bigquery/docs/slots-autoscaling-intro?hl=zh-tw)可能暫時可用，但由於可能會縮減，因此無法共用。

只要 `ignore_idle_slots` 為 false，預留項目的運算單元數量就可以是 `0`，且仍可存取未使用的運算單元。如果只使用 `default` 預留項目，建議採用這種設定方式。接著，您可以[將專案或資料夾指派](https://docs.cloud.google.com/bigquery/docs/reservations-assignments?hl=zh-tw#assign_my_prod_project_to_prod_reservation)給該預留項目，該項目只會使用閒置運算單元。

`ML_EXTERNAL` 類型的指派作業是上述行為的例外狀況。BigQuery ML 外部模型建立工作使用的運算單元無法先占，也就是說，如果預留項目同時具有 ml\_external 和查詢指派類型，則只有在 `ML_EXTERNAL` 工作未占用運算單元時，其他查詢工作才能使用這些運算單元。此外，這些工作不會使用其他預留項目的閒置運算單元。

## 限制

* 您購買的保留項目無法與其他機構共用。
* 您必須為每個機構建立單獨的保留項目和單獨的管理專案。
* 每個組織在單一位置最多可有 10 個管理專案，且這些專案須有有效承諾使用合約。
* 閒置運算資源無法在組織之間共用，也無法在單一組織內的不同管理專案之間共用。
* 承諾使用合約屬於區域性資源。在某個區域或多區域購買的承諾使用合約，無法用於其他區域或多區域。承諾使用合約無法在區域之間，或區域與多區域之間移動。
* 在某個管理專案中購買的使用承諾，無法移至其他管理專案。
* 以某個[版本](https://docs.cloud.google.com/bigquery/docs/editions-intro?hl=zh-tw)購買的承諾使用合約，無法用於其他版本的預留項目。
* 不同[版本](https://docs.cloud.google.com/bigquery/docs/editions-intro?hl=zh-tw)的預留項目之間不會共用閒置運算單元。
* [自動調度資源運算單元](https://docs.cloud.google.com/bigquery/docs/slots-autoscaling-intro?hl=zh-tw)無法共用，因為系統會在不再需要時縮減資源。

## 配額

運算單元配額是指您在某個位置可購買的運算單元數量上限。配額不會產生費用，只有預留項目和承諾使用合約會產生費用。詳情請參閱「[預留項目配額和限制](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#reservation-api-limits)」。如要瞭解如何提高運算單元配額，請參閱「[申請提高配額](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#requesting_a_quota_increase)」。

## 定價

如要瞭解預留項目的定價，請參閱「[固定費率定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#flat-rate_pricing)」。

## 後續步驟

* 如要開始使用 BigQuery 預留項目，請參閱「[開始使用預留項目](https://docs.cloud.google.com/bigquery/docs/reservations-get-started?hl=zh-tw)」
* 如要瞭解預留項目的隨選計費方式，請參閱「[合併使用預留項目與隨選計費](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#combine_reservations_with_on-demand_billing)」。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-10-22 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-10-22 (世界標準時間)。"],[],[]]