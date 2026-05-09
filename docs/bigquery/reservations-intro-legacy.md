Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 舊版預訂簡介

**注意：** 只有許可清單中的客戶可以使用舊版預訂，包括存取固定費率帳單或特定承諾期。如要確認您是否能使用這些舊版功能，請與管理員聯絡。固定費率計費模式會定義運算資源的計費方式，但固定費率預訂和承諾方案的功能與 Enterprise 版的配額相同。

BigQuery 預訂可讓您從[以量計價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#on_demand_pricing)切換為[以容量計價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#capacity_compute_analysis_pricing)。採用以容量為準的定價時，您支付的是專屬或自動調度的查詢處理容量費用，而不是個別查詢的費用。

您可以透過保留項目，將以[運算單元](https://docs.cloud.google.com/bigquery/docs/slots?hl=zh-tw)為單位的查詢容量，分配給不同的工作負載或機構的不同部門。

使用採用 [BigQuery 版本](https://docs.cloud.google.com/bigquery/docs/editions-intro?hl=zh-tw)的預留項目時，您可以選擇是否要建立[容量承諾](https://docs.cloud.google.com/bigquery/docs/reservations-details?hl=zh-tw)，但如果工作負載穩定，建立容量承諾可節省費用。

**注意：** [舊版固定費率合約](#commitments)與 [Enterprise 版](https://docs.cloud.google.com/bigquery/docs/editions-intro?hl=zh-tw)合約享有相同功能。所有舊版固定費率方案都會標示為`flat-rate`，代表運算定價模式值，`Enterprise` 則代表版本值。

## 總覽

BigQuery 提供兩種運算 (分析) 計費模式：

* **[以量計價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#on_demand_pricing)**：
  您只需為查詢所掃描過的資料付費。您有固定的專案[查詢處理容量](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#max_concurrent_slots_on-demand)，費用則取決於每個查詢處理的位元組數。
* **[以運算資源為基礎的計價模式](https://cloud.google.com/bigquery/pricing?hl=zh-tw#capacity_compute_analysis_pricing)**：
  您支付一段時間內專用或自動調度的查詢處理作業容量費用，計算單位為[運算單元](https://docs.cloud.google.com/bigquery/docs/slots?hl=zh-tw)。多個查詢共用相同的運算單元容量。

根據預設，系統會按照以量計價的模式向您收費。使用預訂功能時，您可以切換為以容量為準的計價模式，並使用[運算單元自動調度資源](https://docs.cloud.google.com/bigquery/docs/slots-autoscaling-intro?hl=zh-tw)功能，以及購買享有折扣的[容量承諾](https://docs.cloud.google.com/bigquery/docs/reservations-details?hl=zh-tw)。如果採用容量計費模式，處理的位元組就不會額外產生費用。

您可以同時採用這兩種計費模式。舉例來說，您可能會以以量計價模式執行部分工作負載，並以容量計價模式執行其他工作負載。由於帳單模型是依專案指定，因此您需要為查詢工作使用多個專案。

## 預留項目的優點

使用 BigQuery 預留項目有以下好處：

* **可預測性**。容量計價模式的費用均相同，不會有意料之外的支出。您可以預先指定最高費用預算，也可以善用運算單元承諾，以折扣價取得專屬的持續運算資源。
* **彈性**：您可以選擇要為工作負載分配多少專屬容量，也可以讓 BigQuery 根據工作負載需求自動調度容量。系統會以至少一秒為單位，向您收取所用運算單元的費用。
* **工作負載管理。**每個工作負載都有可供使用的指定 BigQuery 運算資源集區。同時，如果工作負載未使用所有專屬運算單元，系統會自動將未使用的運算單元分配給其他工作負載。
* **集中購買：**可以替整個機構購買及分配運算單元，不需要為每個使用 BigQuery 的專案購買運算單元。

## 預留項目

BigQuery 容量以[*運算單元*](https://docs.cloud.google.com/bigquery/docs/slots?hl=zh-tw)為單位，代表查詢使用的虛擬 CPU。一般來說，如果佈建更多運算單元，就能執行更多並行查詢，複雜查詢的執行速度也會更快。

運算單元會分配到稱為「預留」的集區。預留功能可讓您以適合貴機構的方式分配時段。

舉例來說，您可以為實際工作環境工作負載建立名為 `prod` 的保留項目，並為測試建立名為 `test` 的保留項目。這樣一來，測試作業就不會與正式環境工作負載爭用資源。或者，您也可以為貴機構的不同部門建立預約。

預留項目可包含一律會分配的*基準*運算單元，以及*自動調度*的運算單元，後者會[根據工作負載需求動態新增或移除](https://docs.cloud.google.com/bigquery/docs/slots-autoscaling-intro?hl=zh-tw)。

如果您在建立預留項目之前購買運算單元承諾，系統會自動建立名為 `default` 的預留項目。這個預訂項目沒有特別之處，只是為了方便而建立。`default`您可以決定是否需要額外預留項目，或只使用預設預留項目。

如要使用您分配的配額，必須將一或多個專案*指派*給預留項目，詳情請見下一節。

預留項目是指定運算單元分配量的最低層級。[保留項目內的運算單元分配](#slot_allocation_within_reservations)由 BigQuery 排程器處理。

## 作業

如要使用您分配的配額，必須將一或多個專案、資料夾或機構指派給保留項目。資源階層中的每個層級都會沿用上層的指派項目。換句話說，如果專案或資料夾未獲指派，則該專案或資料夾會繼承上層資料夾或機構的指派項目 (如有)。如要進一步瞭解資源階層，請參閱「[整理 BigQuery 資源](https://docs.cloud.google.com/bigquery/docs/resource-hierarchy?hl=zh-tw)」。

如果專案已指派給保留項目，從該專案啟動工作時，工作會使用該保留項目的運算單元。如果專案未指派給保留項目 (直接指派，或從上層資料夾或機構繼承)，該專案中的工作就會採用以量計價模式。

`None` 指派作業代表沒有指派作業。指派給`None`的專案會採用以量計價方案。`None` 指派作業的常見用途是將機構指派給保留項目，並將部分專案或資料夾指派給 `None`，藉此排除在該保留項目之外。詳情請參閱「[將專案指派為『無』](https://docs.cloud.google.com/bigquery/docs/reservations-assignments?hl=zh-tw#assign-project-to-none)」。

建立指派項目時，請指定該指派項目的工作類型：

* `QUERY`：將此預留項目用於查詢工作，包括 SQL、DDL、DML 和 BigQuery ML 查詢。
* `PIPELINE`：使用這項預留空間進行載入和擷取作業。

  根據預設，載入和擷取工作是[免費](https://cloud.google.com/bigquery/pricing?hl=zh-tw#free)的，且會使用共用運算單元集區。BigQuery 不保證這個共用集區的可用容量或您所看到的總處理量。如果您要載入大量資料，工作可能會等待可用的時段。在這種情況下，您可能需要購買專屬運算單元，並將管道工作指派給這些運算單元。建議您建立額外的專屬保留項目，並停用閒置運算單元共用功能。

  載入工作指派給保留項目後，就無法再使用免費集區。監控效能，確保工作有足夠的容量。
  否則，效能可能會比使用免費集區更差。
* `BACKGROUND`：選擇[使用自己的預留空間](https://docs.cloud.google.com/bigquery/docs/search-index?hl=zh-tw#use_your_own_reservation)來執行 [BigQuery 搜尋](https://docs.cloud.google.com/bigquery/docs/search-intro?hl=zh-tw)索引管理工作，或 [BigQuery 變更資料擷取 (CDC) 擷取](https://docs.cloud.google.com/bigquery/docs/change-data-capture?hl=zh-tw)背景工作時，請使用這項預留空間。使用 Datastream 的背景套用作業將來源資料庫複製到 BigQuery 時，也請使用這項預留量。`BACKGROUND`
  Standard 版不支援預留項目。
* `ML_EXTERNAL`：將此預留項目用於使用 BigQuery 外部服務的 BigQuery ML 查詢。詳情請參閱[將運算單元指派給 BigQuery ML 工作負載](https://docs.cloud.google.com/bigquery/docs/reservations-assignments?hl=zh-tw#assign-ml-workload)。`ML_EXTERNAL`
  Standard 版不支援預留項目。

您無法將運算單元分配給特定作業。BigQuery 排程器會處理保留項目中指派項目的運算單元分配作業。

## 承諾使用合約

*容量使用承諾*是指購買固定量的 BigQuery 運算容量，但有最短承諾使用期。使用[版本](https://docs.cloud.google.com/bigquery/docs/editions-intro?hl=zh-tw)建立的預留項目可選擇是否要使用運算資源承諾，但如果工作負載處於穩定狀態，使用運算資源承諾可節省成本。

BigQuery 提供多種約期方案供您選擇。主要差異在於費用和最短約期。如要查看目前定價資訊，請參閱[容量承諾定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#capacity_compute_analysis_pricing)。

* **一年期承諾使用合約**。您購買 365 天的承諾方案。365 天後，您可以選擇續約或改用其他類型的約期方案。
* **每月承諾使用合約**。購買至少 30 天的承諾使用合約。30 天後，你隨時可以刪除方案。
* **彈性運算單元**。您購買 60 秒的承諾。你可以在 60 秒後隨時刪除這類資料。購買長期使用承諾前，您可以先使用彈性運算單元，測試工作負載在固定費率計費模式下的效能。此外，這類執行個體也適用於處理週期性或季節性需求，或是稅季等高負載事件。

無論選取哪個方案，預約名額都不會在約期結束時失效。只要您未刪除這些配額，系統就會持續向您收費。最低期限過後，你也可以變更方案類型。

運算單元取決於運算能力可用性，當您嘗試購買運算單元使用承諾時，我們不保證能成功購買。不過，在您成功購買使用承諾之後，系統就會保證提供足夠的運算能力，直到您刪除使用承諾為止。

如要進一步瞭解這些方案，請參閱[合約方案](https://docs.cloud.google.com/bigquery/docs/reservations-details?hl=zh-tw#commitment-plans)。

## 預留項目中的運算單元分配

BigQuery 會使用稱為「公平排程」的演算法，在單一保留項目中分配運算單元容量。

BigQuery 排程器會強制將運算單元平均分配給保留項目中執行查詢的專案，然後再分配給指定專案中的工作。排程器會提供最終公平性。即使某些工作可能會在短時間內分配到不成比例的運算單元數量，排程器最終仍會修正這個問題。排程器的目標是找出中間值，避免過於嚴格的作業 (清空執行中的工作會浪費運算單元時間) 和過於寬鬆的作業 (長時間執行作業的工作會佔用不成比例的運算單元時間)。

如果重要工作持續需要比排程器分配的運算單元數量更多，請考慮建立額外的保留項目，並保證運算單元數量，然後將工作指派給該保留項目。詳情請參閱「[工作負載管理](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw)」。

## 閒置的運算單元

在任何時間，部分運算單元可能處於閒置狀態。這些實用資源包括：

* 未分配給任何預留項目的運算單元使用承諾。
* 已分配給預留項目基準，但目前未使用的運算單元。

根據預設，在保留項目中執行的查詢會自動使用同一個管理專案中其他保留項目的閒置運算單元。也就是說，只要有容量，工作隨時都能執行。無論需要資源的查詢優先順序為何，閒置容量都會立即搶占回原始指派的預留項目。系統會即時自動執行這項操作。

如要停用這項功能，並強制保留項目只使用佈建給該項目的運算單元，請將 `ignore_idle_slots` 設為 `true`。如果預留項目將 `ignore_idle_slots` 設為 `true`，就不會收到閒置運算單元。

不同[版本](https://docs.cloud.google.com/bigquery/docs/editions-intro?hl=zh-tw)的預留項目無法共用閒置運算單元。你只能分享基準運算單元或已承諾運算單元。[自動調度資源的時段](https://docs.cloud.google.com/bigquery/docs/slots-autoscaling-intro?hl=zh-tw)可能暫時可用，但由於系統可能會縮減資源，因此無法共用。

只要 `ignore_idle_slots` 設為 False，保留項目就可以有 `0` 個運算單元，並存取未使用的運算單元。如果只使用`default`預訂功能，建議採用這種設定方式。然後[將專案或資料夾指派](https://docs.cloud.google.com/bigquery/docs/reservations-assignments?hl=zh-tw#assign_my_prod_project_to_prod_reservation)給該保留項目，這樣專案或資料夾就只會使用閒置運算單元。

`ML_EXTERNAL` 類型的指派作業是上述行為的例外狀況。BigQuery ML 外部模型建立工作使用的運算單元無法搶占；也就是說，如果保留項目同時指派了 ml\_external 和 query 類型，只有在 `ML_EXTERNAL` 工作未占用運算單元時，其他查詢工作才能使用這些運算單元。此外，這些工作不會使用其他預留項目的閒置運算單元。

## 限制

* 您購買的保留項目無法與其他機構共用。
* 您必須為每個機構建立單獨的保留項目和單獨的管理專案。
* 每個機構在單一位置最多可有 10 個管理專案，且這些專案都具有有效合約。
* 機構之間或單一機構內的不同管理專案之間，無法共用閒置容量。
* 承諾是地區性資源。在某個地區或多地區購買的使用承諾，無法用於其他地區或多地區。使用承諾無法在區域之間移動，也無法在區域和多區域之間移動。
* 在某個管理專案中購買的承諾無法移至其他管理專案。
* 以某個[版本](https://docs.cloud.google.com/bigquery/docs/editions-intro?hl=zh-tw)購買的使用承諾，無法用於其他版本的預訂。
* 不同[版本](https://docs.cloud.google.com/bigquery/docs/editions-intro?hl=zh-tw)的預訂項目不會共用閒置運算單元。
* [自動調度資源的時段](https://docs.cloud.google.com/bigquery/docs/slots-autoscaling-intro?hl=zh-tw)無法共用，因為系統會在不再需要時縮減資源。

## 配額

運算單元配額是指您在某個地點可購買的運算單元數量上限。您不需支付配額費用，只需支付預訂和承諾費用。詳情請參閱[預訂配額和限制](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#reservation-api-limits)。如要瞭解如何提高運算單元配額，請參閱「[申請提高配額](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#requesting_a_quota_increase)」一文。

## 定價

如要瞭解保留項目的定價資訊，請參閱[固定費率定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#flat-rate_pricing)。

## 後續步驟

* 如要開始使用 BigQuery 保留項目，請參閱「[開始使用保留項目](https://docs.cloud.google.com/bigquery/docs/reservations-get-started?hl=zh-tw)」
* 如要瞭解預留項目的隨需帳單，請參閱「[合併使用保留項目與隨需帳單](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#combine_reservations_with_on-demand_billing)」。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-09 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-09 (世界標準時間)。"],[],[]]