Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 瞭解可靠性

BigQuery 會自動處理區域內的機器和可用區故障，盡可能減少干擾，讓您順利執行分析工作負載。如要提升韌性，您可以設定跨區域災難復原、還原已刪除或損毀的資料，以及實作用戶端錯誤重試機制，滿足可靠性需求。

這些功能可支援擷取及分析大量資料的工作負載，並維持一致的效能，包括異常偵測、透過[串流擷取](https://docs.cloud.google.com/bigquery/docs/streaming-data-into-bigquery?hl=zh-tw)進行即時分析，以及使用 [BigQuery ML](https://docs.cloud.google.com/bigquery/docs/bqml-introduction?hl=zh-tw) 進行預測分析。如需這些解決方案的詳細範例，請參閱「[BigQuery 參考模式](https://docs.cloud.google.com/bigquery/docs/reference-patterns?hl=zh-tw)」。

## BigQuery 的可靠性面向

如要判斷 BigQuery 是否符合工作負載需求，可以從五個關鍵面向評估其可靠性：可用性、耐用性、資料一致性、效能一致性和資料復原。

### 可用性

可用性定義了您從 BigQuery 讀取資料或將資料寫入 BigQuery 的能力。BigQuery 的設計可讓讀取和寫入作業具備高可用性，並提供 [99.99% 的運作時間服務水準協議](https://cloud.google.com/bigquery/sla?hl=zh-tw)。這兩項作業都涉及兩個元件：

* BigQuery 服務
* 執行特定查詢所需的運算資源

服務的可靠性取決於您用來擷取資料的特定 BigQuery API。運算資源的可用性取決於執行查詢時可用的容量。如要進一步瞭解 BigQuery 的基本運算單位和[運算單元資源經濟](https://docs.cloud.google.com/bigquery/docs/slots?hl=zh-tw#slot_resource_economy)，請參閱「[瞭解運算單元](https://docs.cloud.google.com/bigquery/docs/slots?hl=zh-tw)」。

### 耐用性

耐用性是指可成功讀取的資料比例，定義請參閱「*網站可靠性工作手冊*」的「[導入服務等級目標](https://sre.google/workbook/implementing-slos/?hl=zh-tw)」一章。為提供高耐用性，BigQuery 會自動將資料的備援副本，儲存在所選位置的兩個可用區。

### 資料一致性

資料一致性定義了資料寫入或修改後，查詢資料的方式和時機。資料一致性的其中一個面向，是確保資料擷取採用「僅限一次」語意。詳情請參閱「[重試失敗的工作插入作業](#retry_failed_job_insertions)」。

### 成效一致性

一般來說，效能可以從兩個維度來表示。「延遲時間」是指查詢等長時間資料擷取作業的執行時間。「*Throughput*」(處理量) 是指 BigQuery 在特定時間內可處理的資料量。BigQuery 採用多租戶、可水平擴充的設計，因此處理量可擴充至任意資料大小。延遲時間和處理量的相對重要性取決於您的特定用途。

### 資料復原

您可以使用下列指標，評估服務中斷後復原資料的能力：

* *復原時間目標* (RTO)：事件發生後，資料無法使用的最長時間。
* *復原點目標* (RPO)：貴組織可容許遺失的事件前資料收集量上限。

如果可用區或區域發生多日或破壞性中斷，這些考量因素就特別重要，不過這種情況不太可能發生。

## 擬定災難復原計畫

在本節中，「災難規劃」涵蓋的故障範圍從單一機器遺失到整個區域的災難性遺失。BigQuery 會自動處理單一機器和可用區故障，但如果工作負載需要，您必須設計架構來復原區域故障。規劃災難復原時，必須瞭解自動復原的範圍，以及您需要負責的部分。

BigQuery 提供 [99.99% 的運作時間服務水準協議](https://cloud.google.com/bigquery/sla?hl=zh-tw)。BigQuery 的區域架構可將資料寫入兩個不同的可用區，並佈建備援運算容量，確保資料可用性。BigQuery 服務水準協議適用於區域 (例如 `us-central1`) 和多區域 (例如 `US`)。

### 自動處理失敗

BigQuery 是區域性服務，因此會自動處理個別機器或整個可用區遺失的問題。BigQuery 會為您抽象化底層可用區基礎架構。

#### 機器遺失

以 Google 的營運規模來說，機器故障是每天都會發生的事。BigQuery 可自動處理機器故障，不會影響所在可用區。

BigQuery 會將每項查詢拆分為多個小型工作，並平行分派至多部機器。如果機器故障或效能降低，BigQuery 會自動將受影響的工作重新調度至其他機器。這種做法對於降低尾端延遲至關重要。

BigQuery 會使用 [Reed-Solomon](https://en.wikipedia.org/wiki/Binary_Reed%E2%80%93Solomon_encoding) 編碼，持久儲存資料的可用區副本，並在另一個可用區中儲存至少一個額外的可用區副本。如果多部機器故障導致可用區副本遺失，BigQuery 會偵測到遺失，並建立新的可用區副本來還原備援。

#### 失去可用區

為符合 99.99% 的運作時間服務水準協議，BigQuery 會自動為資料和運算運算單元提供可用區備援。由於單一可用區的運算可用性無法單獨滿足這項服務水準協議，BigQuery 會在可用區發生嚴重中斷後的一分鐘內，自動將新查詢轉送至其他可用區。執行中的查詢可能需要較長時間才能完成，而新發出的查詢則會在另一個可用區正常完成。

即使某個可用區長時間無法使用，也不會遺失資料，因為 BigQuery 會同步將資料寫入兩個可用區。因此，即使某個可用區服務中斷，您的服務也不會受到影響。

### 故障類型

失敗分為兩種：軟失敗和硬失敗。

*軟性故障*是指硬體未損毀，但運作不正常。例如停電、網路失聯或機器當機。BigQuery 的設計可防止在軟故障期間遺失資料。

「硬體故障」是指硬體損毀導致的運作故障，例如洪水、地震或颶風造成的損害。BigQuery 能否在硬體故障期間防止資料遺失，取決於故障影響的是單一可用區還是整個區域。

### 位置備援和故障行為

建立 BigQuery 資料集時，您要選取資料儲存位置。這個位置可能是下列其中一種：

* 區域：特定地理位置，例如愛荷華州 (`us-central1`) 或蒙特婁 (`northamerica-northeast1`)。
* 多區域：包含兩個以上地理位置的大型地理區域，例如美國 (`US`) 或歐洲 (`EU`)。

無論是哪一種情況，BigQuery 都會自動將資料副本儲存在所選位置單一區域內的兩個不同 Google Cloud
[可用區](https://docs.cloud.google.com/docs/geography-and-regions?hl=zh-tw#regions_and_zones)。

除了儲存空間備援，BigQuery 也會在多個可用區中維護備援運算容量。BigQuery 結合多個可用區的備援儲存空間和運算資源，提供高可用性和耐用性。

**注意：** 選取多區域位置不會提供跨區域複製或區域備援功能。BigQuery 會將資料儲存在多區域位置中的單一區域。

如果發生機器層級故障，BigQuery 會繼續執行，延遲時間不超過幾毫秒，且所有目前執行的查詢都會繼續處理。在軟性或硬性可用區故障期間，不會發生資料遺失，但您可能需要重新提交目前執行的查詢。BigQuery 會在幾分鐘內自動緩解軟性可用區故障，例如停電、變壓器故障或網路分區。

軟性區域故障 (例如整個區域失去網路連線) 會導致可用性中斷，直到區域恢復上線為止，但不會導致資料遺失。如果發生嚴重的區域性故障，例如整個區域遭到災害破壞，可能會導致儲存在該區域的資料遺失。BigQuery 不會自動在其他地理區域提供資料備份或副本。您可以使用[跨區域資料集複製](https://docs.cloud.google.com/bigquery/docs/data-replication?hl=zh-tw)或[代管災難復原](https://docs.cloud.google.com/bigquery/docs/managed-disaster-recovery?hl=zh-tw)功能，提高對區域性硬體故障的復原能力。

如要進一步瞭解 BigQuery 資料集位置，請參閱「[位置考量事項](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw#data-locations)」。

### 情境：區域遺失

如果實體區域遭到破壞，BigQuery 不會提供耐用性或可用性。這項限制適用於單一區域和多區域，因此您必須預先規劃，才能在區域服務中斷期間維持耐用性和可用性。如果 BigQuery 的 99.99% 服務水準協議無法滿足您在區域暫時中斷期間的可用性需求，請考慮跨區域設定備援可用性。

為避免區域損毀時遺失資料，請將資料備份到其他地理位置。舉例來說，您可以使用[跨區域資料集複製](https://docs.cloud.google.com/bigquery/docs/data-replication?hl=zh-tw)功能，持續將資料複製到不同地理區域。

如果您使用 BigQuery 多區域，請勿將資料備份到該多區域地理範圍內的單一區域。舉例來說，如果您從 `US` 多區域備份資料，請避免選擇重疊的區域 (例如 `us-central1`)，因為在發生災害時，可能會發生相關聯的故障。如要進一步瞭解多區域的地理範圍，請參閱「[多區域](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw#multi-regions)」。

為避免長時間無法使用，請在兩個地理位置不同的 BigQuery 位置複製資料並佈建運算單元。您可以使用[代管災難復原](https://docs.cloud.google.com/bigquery/docs/managed-disaster-recovery?hl=zh-tw)功能，在次要區域自動佈建運算單元，並控管工作負載從一個區域容錯移轉至另一個區域。

### 情境：意外刪除或資料損毀

BigQuery 採用[多版本並行控制](https://en.wikipedia.org/wiki/Multiversion_concurrency_control)架構，因此支援[時光旅行](https://docs.cloud.google.com/bigquery/docs/time-travel?hl=zh-tw)功能。透過時間旅行功能，您可以查詢過去 7 天內任何時間點的資料。這項功能可讓您還原 7 天內誤刪、修改或損毀的資料。時間旅行也適用於已刪除的資料表

BigQuery 也可讓您建立[資料表快照](https://docs.cloud.google.com/bigquery/docs/table-snapshots-intro?hl=zh-tw)，在同一區域內備份資料，保留時間可超過 7 天的時間旅行時間範圍。建立快照是僅限中繼資料的操作，不會產生額外的儲存空間費用。雖然資料表快照有助於防止意外刪除，但不會提高資料耐用性。

### 即時分析的災難復原

如果是[即時分析管道](#real-time_analytics)，會持續將串流端點記錄擷取至 BigQuery，因此必須持續複製資料並在次要區域佈建運算單元，才能防範區域長時間無法使用的情況。不過，當擷取架構使用 Pub/Sub 和 Dataflow 做為[資料載入方法](https://docs.cloud.google.com/bigquery/docs/loading-data?hl=zh-tw#methods)之一時，該架構已能彈性因應 BigQuery 暫時無法使用的情況，因此這種高層級的備援可能不值得您付出成本。

舉例來說，假設您設定夜間擷取工作，將 BigQuery 資料從 `us-east4` 匯出至 `us-central1` 的 Cloud Storage Archive Storage。如果 `us-east4` 發生災難性資料遺失，這項匯出作業可提供持久的備份。在這項設定中，復原點目標 (RPO) 為 24 小時，因為最新備份可能最多為 24 小時前。復原時間目標 (RTO) 可能需要幾天，因為您必須將資料從 Cloud Storage 備份還原至 `us-central1` 的 BigQuery。如果您在與備份不同的區域佈建 BigQuery，則必須先將資料移轉至該區域。除非您事先在復原區域購買備援運算單元，否則視您要求的數量而定，佈建所需的 BigQuery 容量可能需要額外時間。

### 批次資料處理的災難復原

如果是[批次資料處理工作負載](#batch_data_processing)，您必須在固定期限前向監管機構提交業務關鍵每日報表，因此通常值得花費成本，執行整個處理管道的兩個獨立執行個體，以實作備援。使用兩個不同的區域 (例如 `us-west1` 和 `us-east4`) 可提供地理位置分隔和兩個獨立的故障域，以防區域長時間無法使用或永久遺失。

如果必須只傳送一次報表，則需要在兩個管道都成功完成時，協調輸出內容。其中一種方法是選取最先完成的管道結果，例如在完成時將通知發布至 Pub/Sub 主題。或者，您也可以讓第二個管道覆寫結果，並在 Cloud Storage 中使用物件版本管理功能。如果較晚完成的管道寫入損毀的資料，您可以從 Cloud Storage 還原第一個管道寫入的版本。

## 錯誤處理

以下各節說明處理影響可靠性錯誤的最佳做法。

### 重試失敗的 API 要求

當用戶端應用程式、用戶端程式庫或合作夥伴工具向 BigQuery 發出 API 要求時，請使用[截斷指數輪詢](https://en.wikipedia.org/wiki/Exponential_backoff)。如果用戶端收到系統錯誤或配額錯誤，就會使用這項重試策略，以隨機且遞增的等待間隔重試要求，直到達到重試次數上限。

使用部分指數輪詢，可讓應用程式更具彈性，能更妥善地處理暫時性錯誤。即使在正常運作條件下，每 10,000 個要求中仍可能有一個失敗，詳情請參閱 BigQuery 的 [99.99% 可用性服務水準協議](https://cloud.google.com/bigquery/sla?hl=zh-tw)。在異常情況下，這項錯誤率可能會增加，但如果錯誤是隨機分布，則指數輪詢可以緩解大部分的失敗。

如果要求持續失敗並顯示 `5xx` 錯誤，請與 Cloud Customer Care 聯絡，並在設定[客服案件優先順序](https://docs.cloud.google.com/support/docs/customer-care-procedures?hl=zh-tw#support_case_priority)時，清楚說明對業務的影響，以便支援團隊準確分類問題。相反地，如果要求持續失敗並傳回 `4xx` 錯誤，您可以修改應用程式來解決問題。詳情請參閱錯誤訊息。

### 指數輪詢邏輯範例

指數輪詢邏輯會重試查詢或要求，並在重試之間增加等待時間，直到達到最大輪詢時間。下列步驟說明用戶端如何實作截斷指數輪詢：

1. 向 BigQuery 提出要求。
2. 如果要求失敗，請等待 `1 + random_number_milliseconds` 秒，然後重試要求。
3. 如果要求失敗，請等待 `2 + random_number_milliseconds` 秒，然後重試要求。
4. 如果要求失敗，請等待 `4 + random_number_milliseconds` 秒，然後重試要求。
5. 重複這個模式，每次重試時將基本等待時間加倍，最多重試 `maximum_backoff` 次。
6. 繼續等待及重試，直到重試次數達上限，但等待時間不超過 `maximum_backoff`。

請留意下列退避計算細節：

* 等待時間為 `min(((2^n)+random_number_milliseconds), maximum_backoff)`，其中 `n` 會在每次疊代 (要求) 時遞增 1。
* `random_number_milliseconds` 是小於或等於 1,000 的隨機毫秒數。這種隨機化做法有助於避免許多用戶端碰巧同步並同時重試，導致要求同步傳送。每次重試要求後，重新計算 `random_number_milliseconds`。
* 輪詢間隔上限 (`maximum_backoff`) 通常為 32 或 64 秒。`maximum_backoff` 的適當值取決於您的用途。

達到輪詢時間上限後，用戶端可以繼續重試。此時重試就不需要繼續增加輪詢時間。舉例來說，如果用戶端使用的最大輪詢時間為 64 秒，則在用戶端達到這個值後，可以繼續每 64 秒重試一次。為避免無限重試迴圈，請設定重試次數上限，讓用戶端在達到設定的限制後停止重試。

重試之間的等待時間和重試次數取決於您的用途和網路狀況。

### 重試失敗的工作插入作業

如果應用程式需要「僅限一次」插入語意，請考量工作 [`WriteDisposition`](https://docs.cloud.google.com/bigquery/docs/reference/auditlogs/rest/Shared.Types/BigQueryAuditMetadata.WriteDisposition?hl=zh-tw) 如何處理資料表中的現有資料 (失敗、覆寫或附加)。

如果使用 `WRITE_EMPTY` 或 `WRITE_TRUNCATE` 處置，您可以重試任何失敗的工作插入或執行作業，藉此達成最多一次語意，因為 BigQuery 會以原子方式將工作擷取的所有資料列寫入資料表。

使用 `WRITE_APPEND` 處置方式時，請指定自訂工作 ID，以免重試時附加重複資料。BigQuery 會拒絕任何重複使用先前工作 ID 的工作建立要求，因此指定工作 ID 可為該 ID 提供最多一次的語意。接著，您可以在使用新的可預測工作 ID 重試之前，確認所有先前的嘗試都失敗，藉此實現「僅限一次」語意。

如果暫時性網路問題導致用戶端無法收到工作插入確認，則使用相同工作 ID 重試會失敗，並傳回 `status=ALREADY_EXISTS` (`code=409` 和 `reason="duplicate"`)。請呼叫 `jobs.get` 擷取現有工作的狀態，並判斷是否要使用新的工作 ID 建立新工作。

## 用途和可靠性需求

BigQuery 可做為各種架構的重要元件。視您部署的用途和架構而定，您可能需要滿足不同的可用性、效能和可靠性需求。以下各節將探討兩種常見的架構及其可靠性需求。

### 即時分析

第一個範例是事件資料處理管道。在這個架構中，Pub/Sub 會從端點擷取記錄事件，而串流 Dataflow 管道會使用 [BigQuery Storage Write API](https://docs.cloud.google.com/bigquery/docs/write-api?hl=zh-tw) 處理資料並寫入 BigQuery。接著，分析人員會對資料執行臨時查詢，重新建立事件序列，並透過近乎即時的資訊主頁以視覺化方式呈現資料，偵測趨勢和模式。

由於這項工作負載需要高度端對端資料更新間隔，因此低擷取*延遲時間*至關重要。資料寫入 BigQuery 後，*可靠性*取決於兩個因素：使用者能否以*一致*、可預測的延遲時間執行臨時查詢，以及使用資料的資訊主頁是否反映最新資訊。

### 批次資料處理

第二個例子是金融服務業法規遵循的批次處理架構。其中一項主要要求是，必須在每晚固定截止時間前，向監管機構提交每日報表。只要產生報表的夜間批次處理作業在這個期限前完成，就符合效能要求。

管道會將資料載入 BigQuery，並與其他資料來源彙整，用於製作資訊主頁、分析及產生 PDF 報表。準時且正確地提交這些報表，是重要的業務需求。因此，您必須確保資料擷取過程的*可靠性*，並在*一致*的時間範圍內產生準確的報表，以符合法規期限。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-10-28 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-10-28 (世界標準時間)。"],[],[]]