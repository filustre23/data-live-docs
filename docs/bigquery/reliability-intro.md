Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 瞭解可靠性

本文將說明 BigQuery 的可靠性功能，例如可用性、耐久性、資料一致性、效能一致性、資料復原，並回顧錯誤處理注意事項。

這份簡介將協助您瞭解三項主要考量：

* 判斷 BigQuery 是否適合您的工作。
* 瞭解 BigQuery 可靠性的各個層面。
* 針對特定用途找出具體的可靠性需求。

## 選取 BigQuery

[BigQuery](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw) 是全代管的企業資料倉儲，可儲存及分析大量資料集。這項服務提供一致的效能，可讓您擷取、儲存、讀取及查詢 MB 到 PB 規模的資料，不必管理任何基礎架構。BigQuery 效能強大，因此非常適合用於各種解決方案。其中有些已詳細記錄為[參考模式](https://docs.cloud.google.com/bigquery/docs/reference-patterns?hl=zh-tw)。

一般來說，BigQuery 非常適合用於大量資料擷取和分析的工作負載。具體來說，這項服務可有效部署於即時和預測資料分析 (搭配[串流擷取](https://docs.cloud.google.com/bigquery/docs/streaming-data-into-bigquery?hl=zh-tw)和 [BigQuery ML](https://docs.cloud.google.com/bigquery/docs/bqml-introduction?hl=zh-tw))、異常偵測等用途，以及其他需要分析大量資料並確保效能可預測的用途。不過，如果您要尋找支援線上交易處理 (OLTP) 樣式應用程式的資料庫，建議考慮其他 Google Cloud 服務，例如 [Spanner](https://docs.cloud.google.com/spanner?hl=zh-tw)、[Cloud SQL](https://docs.cloud.google.com/sql?hl=zh-tw) 或 [Bigtable](https://docs.cloud.google.com/bigtable?hl=zh-tw)，這些服務可能更適合這類用途。

## BigQuery 的可靠性層面

### 可用性

可用性是指使用者從 BigQuery 讀取或寫入資料的能力。BigQuery 的設計宗旨是確保這兩項服務的高可用性，並提供 99.99% 的[服務水準協議](https://cloud.google.com/bigquery/sla?hl=zh-tw)。這兩項作業都涉及兩個元件：

* BigQuery 服務
* 執行特定查詢所需的運算資源

服務的可靠性取決於用於擷取資料的特定 BigQuery API。運算資源的可用性取決於使用者執行查詢時的可用容量。如要進一步瞭解 BigQuery 的基本運算單位，以及由此產生的[運算單元資源經濟](https://docs.cloud.google.com/bigquery/docs/slots?hl=zh-tw#slot_resource_economy)，請參閱「[瞭解運算單元](https://docs.cloud.google.com/bigquery/docs/slots?hl=zh-tw)」。

### 耐用性

如要瞭解耐久性，請參閱 SRE 工作手冊的「[實作 SLO](https://sre.google/workbook/implementing-slos/?hl=zh-tw)」一章，其中將耐久性定義為「可成功讀取的資料比例」。

### 資料一致性

一致性是指使用者對資料的期望，也就是資料寫入或修改後，查詢方式應如何。資料一致性的一項重點，是確保資料擷取作業的「僅一次」語意。詳情請參閱「[重試插入失敗的工作](#retry_failed_job_insertions)」。

### 效能一致性

一般來說，效能可從兩個維度來看。*延遲時間*是衡量查詢等長時間資料擷取作業執行時間的指標。*處理量*是用來衡量 BigQuery 在特定時間內可處理多少資料。由於 BigQuery 採用多租戶、可水平擴充的設計，因此處理量可擴充至任意資料大小。延遲時間和處理量的相對重要性取決於特定用途。

### 資料復原

如要評估系統在服務中斷後復原資料的能力，可以採取以下兩種方式：

* *復原時間目標* (RTO)。事件發生後，資料可能無法使用的時間長度。
* *復原點目標* (RPO)。可接受遺失多少事件發生前收集的資料。

萬一可用區或區域發生多日或破壞性服務中斷，這些考量事項就特別重要。

## 擬定災難復原計畫

雖然「災害」一詞可能會讓人聯想到天災，但本節的範圍涵蓋從單一機器故障，到區域發生災難性損失等特定故障。前者是 BigQuery 自動處理的日常事件，後者則可能需要客戶設計架構來處理。瞭解災難規劃在何種範圍內會轉移至客戶責任，這點非常重要。

BigQuery 提供業界領先的[99.99% 運作時間服務水準協議](https://cloud.google.com/bigquery/sla?hl=zh-tw)。BigQuery 的區域架構會在兩個不同區域寫入資料，並提供備援運算容量，因此能確保資料可用性。請務必注意，BigQuery 的服務等級協議 (SLA) 適用於區域 (例如 us-central1) 和多區域 (例如 US)。

### 自動處理情境

由於 BigQuery 是區域服務，因此 BigQuery 必須自動處理機器或整個可用區的損失。BigQuery 是以區域為基礎建構，但使用者不會察覺這點。

#### 機器遺失

Google 的營運規模龐大，每天都會發生機器故障。BigQuery 的設計可自動處理機器故障，不會對所含區域造成任何影響。  
在幕後，查詢執行作業會拆分為多項小型工作，可平行分派至多部機器。如果機器效能突然下降或降低，系統會自動將工作重新指派給其他機器。這種做法對於縮短尾延遲時間至關重要。

BigQuery 會使用 [Reed-Solomon](https://en.wikipedia.org/wiki/Binary_Reed%E2%80%93Solomon_encoding) 編碼，有效率地長期儲存資料的區域副本。即使發生極為罕見的狀況，導致多部機器故障而遺失區域副本，資料也會以相同方式儲存在至少一個其他可用區。在這種情況下，BigQuery 會偵測到問題，並建立新的區域資料副本，以還原備援。

#### 可用區中斷

任何指定區域的運算資源可用性不足，無法達到 BigQuery 99.99% 的運作時間服務水準協議。因此，BigQuery 會自動為資料和運算單元提供區域備援。雖然區域中斷的情況不常見，但確實會發生。不過，BigQuery 自動化功能會在嚴重中斷後的一分鐘內，將新查詢路徑導向其他可用區。已在處理中的查詢可能不會立即恢復，但新發出的查詢會。這會導致進行中的查詢需要很長時間才能完成，但新發出的查詢則會快速完成。

即使某個可用區長時間無法使用，BigQuery 也會將資料同步寫入兩個可用區，因此不會發生資料遺失的情況。因此即使發生區域損失，客戶也不會遇到服務中斷問題。

### 故障類型

故障類型分為兩種：軟體故障和硬體故障。

「軟體故障」是指硬體未損壞的操作性缺陷。例如：電源中斷、網路分區或機器當機。一般來說，BigQuery 不會因軟體故障而遺失資料。

「硬體故障」是硬體損壞的操作性缺陷。硬體故障比軟體故障更為嚴重。硬體故障的例子包括水災、恐怖攻擊、地震和颶風造成的損壞。

### 可用性和耐用性

建立 BigQuery 資料集時，請選取資料的儲存位置。這個位置可以是下列其中一種：

* 地區：特定地理位置，例如愛荷華州 (`us-central1`) 或蒙特婁 (`northamerica-northeast1`)。
* 多地區：包含兩個以上地理位置的大型地理區域，例如美國 (`US`) 或歐洲 ()。`EU`

無論是哪種情況，BigQuery 都會自動將資料副本儲存在所選位置的單一區域內，兩個不同的 Google Cloud [可用區](https://docs.cloud.google.com/docs/geography-and-regions?hl=zh-tw#regions_and_zones)。

除了儲存空間備援外，BigQuery 也會在多個區域維護備援運算容量。BigQuery 結合多個可用區的備援儲存空間和運算資源，提供高可用性和高耐用性。

**注意：** 選取多區域位置不會提供跨區域複製或區域備援。資料會儲存在地理位置內的單一區域。

如果發生機器層級故障，BigQuery 將繼續運作，且幾乎不會出現延遲情況，所有目前執行的查詢都會繼續處理。無論是軟體或硬體故障，都不會造成資料遺失。不過，目前執行的查詢可能會失敗，需要重新提交。因停電、變壓器損壞或網路分區等導致的軟體故障，已經過充分測試，且系統會在幾分鐘內自動解決問題。

輕微的地區性故障 (例如整個區域的網路連線中斷) 不會導致資料遺失，但在該區域重新上線前，您將無法使用該區域。如果發生嚴重的地區性故障，例如，災難破壞了整個地區，則該地區中儲存的資料可能會遺失。BigQuery 不會自動在其他地理區域提供資料備份或副本。您可以透過[跨區域資料集複製](https://docs.cloud.google.com/bigquery/docs/data-replication?hl=zh-tw)或[代管災難復原](https://docs.cloud.google.com/bigquery/docs/managed-disaster-recovery?hl=zh-tw)，提升系統在區域發生嚴重故障時的復原能力。

如要進一步瞭解 BigQuery 資料集位置，請參閱「[位置注意事項](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw#data-locations)」一文。

### 情境：區域遺失

在極不可能發生的實體區域損失事件中，BigQuery 不提供耐久性或可用性。這項規則適用於地區和多地區。因此，在這種情況下維持耐久性和可用性需要客戶規劃。如果發生暫時性中斷 (例如網路中斷)，且您認為 BigQuery 的 99.99% 服務水準協議不足以因應，則應考慮採用備援可用性。

為避免區域性破壞性損失造成資料遺失，您需要將資料備份到其他地理位置。舉例來說，您可以使用[跨區域資料集複製](https://docs.cloud.google.com/bigquery/docs/data-replication?hl=zh-tw)功能，持續將資料複製到地理位置不同的區域。

如果是 BigQuery 多地區，請避免備份至多地區範圍內的地區。如要瞭解多區域的範圍，請參閱 [BigQuery 位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw#multi-regions)。舉例來說，如果您要從美國多區域備份資料，請避免選擇重疊的區域 (例如 us-central1)，以免發生災害時出現相關聯的故障。

為避免長時間無法使用，您必須在兩個地理位置不同的 BigQuery 位置複製資料並佈建配額。您可以使用[受管理災難復原](https://docs.cloud.google.com/bigquery/docs/managed-disaster-recovery?hl=zh-tw)，在次要區域中自動佈建運算單元，並控管工作負載從一個區域到另一個區域的容錯移轉。

### 情境：意外刪除或資料毀損

由於 BigQuery 採用[多版本並行控制](https://en.wikipedia.org/wiki/Multiversion_concurrency_control)架構，因此支援[時空旅行](https://docs.cloud.google.com/bigquery/docs/time-travel?hl=zh-tw)。這項功能可讓您查詢過去七天內任何時間點的資料。這樣一來，您就能在 7 天內自行還原任何遭誤刪、修改或損毀的資料。即使是已刪除的資料表，也能使用時間旅行功能。

BigQuery 也支援[建立資料表快照](https://docs.cloud.google.com/bigquery/docs/table-snapshots-intro?hl=zh-tw)。這項功能可讓您在同一區域內明確備份資料，備份時間長度超過 7 天的時間旅行視窗。快照純粹是中繼資料作業，不會產生額外的儲存空間位元組。雖然這項功能可防止資料遭誤刪，但無法提高資料的耐用性。

### 用途：即時分析

在這個使用案例中，端點記錄檔的資料會持續串流至 BigQuery。如要避免整個區域長時間無法使用 BigQuery，必須持續複製資料，並在其他區域佈建時段。由於架構可透過[擷取路徑中的 Pub/Sub 和 Dataflow](https://docs.cloud.google.com/bigquery/docs/loading-data?hl=zh-tw#methods)，避免 BigQuery 無法使用，因此這種高層級的備援機制可能不符成本效益。

假設使用者已在 us-east4 中設定 BigQuery 資料，並使用擷取工作，每晚將資料匯出至 us-central1 中 Archive Storage 儲存空間級別下的 Cloud Storage。萬一 us-east4 發生災難性資料遺失，這項功能可提供耐用的備份。在這種情況下，復原點目標 (RPO) 為 24 小時，因為最舊的匯出備份資料可能已存在 24 小時。復原時間目標 (RTO) 可能需要數天，因為資料必須從 Cloud Storage 備份還原至 us-central1 的 BigQuery。如果 BigQuery 佈建的區域與備份位置不同，資料必須先移轉至該區域。另請注意，除非您事先在復原區域購買備援運算單元，否則視要求數量而定，可能需要額外時間才能取得所需的 BigQuery 容量。

### 使用案例：批次資料處理

在這個使用案例中，每天都要在固定期限前完成報告並傳送給監管機構，對業務至關重要。執行整個處理管道的兩個獨立執行個體來實作備援機制，可能值得付出這筆費用。使用兩個不同的區域 (例如 us-west1 和 us-east4) 可提供地理隔離，並在區域長時間無法使用，甚至是區域永久遺失這種不太可能發生的情況下，提供兩個獨立的故障網域。

假設我們需要準確傳送一次報表，就必須協調兩個管道預期的成功完成案例。合理的策略是直接選取管道中第一個完成的結果，例如在成功完成時通知 Pub/Sub 主題。或者，覆寫結果並重新為 Cloud Storage 物件建立版本。如果稍後完成的管道寫入的資料已損毀，您可以從 Cloud Storage 還原由先完成的管道寫入的版本，藉此復原資料。

## 處理錯誤

以下是解決影響穩定性錯誤的最佳做法。

### 重試失敗的 API 要求

BigQuery 用戶端 (包括用戶端程式庫和合作夥伴工具) 發出 API 要求時，應使用[截斷指數輪詢](https://en.wikipedia.org/wiki/Exponential_backoff)。也就是說，如果用戶端收到系統錯誤或配額錯誤，應重試要求最多幾次，但輪詢間隔應隨機增加。

採用這種重試方法後，應用程式在發生錯誤時會更加穩定可靠。即使在正常運作條件下，您仍可預期每 10, 000 筆要求中，約有 1 筆會失敗，如 BigQuery 的[可用性服務水準協議 (99.99%)](https://cloud.google.com/bigquery/sla?hl=zh-tw) 所述。在異常情況下，這個錯誤率可能會提高，但如果錯誤是隨機分布，指數輪詢策略可以減輕所有情況，最嚴重的情況除外。

如果要求持續失敗並出現 5XX 錯誤，請向 Google Cloud 支援團隊提報。請務必[清楚說明失敗對業務的影響](https://docs.cloud.google.com/support/docs/procedures?hl=zh-tw#support_case_priority)，以便正確分類問題。另一方面，如果要求持續失敗並出現 4XX 錯誤，則應可透過變更應用程式來解決問題。詳情請參閱錯誤訊息。

### 指數輪詢邏輯範例

指數輪詢邏輯會重試查詢或要求，並將每次重試之間的等待時間逐漸增加至最大輪詢時間，例如：

1. 向 BigQuery 發出要求。
2. 如果要求失敗，請等待 1 + random\_number\_milliseconds 秒後再重試要求。
3. 如果要求失敗，請等待 2 + random\_number\_milliseconds 秒後再重試要求。
4. 如果要求失敗，請等待 4 + random\_number\_milliseconds 秒後再重試要求。
5. 依此類推，時間上限為 (`maximum_backoff`)。
6. 繼續等待和重試，直到重試次數達上限，但不再增加每次重試之間的等待時間。

注意事項：

* 等待時間為 `min(((2^n)+random_number_milliseconds), maximum_backoff)`，`n` 會在每次疊代 (要求) 時增加 1。
* `random_number_milliseconds` 是小於或等於 1000 的隨機毫秒數。這種隨機化做法有助於避免多個用戶端同步處理並同時重試，導致同步傳送每一波要求。`random_number_milliseconds` 的值會在每次重試要求後重新計算。
* 輪詢間隔上限 (`maximum_backoff`) 通常為 32 或 64 秒。`maximum_backoff` 的適當值視用途而異。

用戶端達到輪詢持續時間上限後，仍可繼續重試。
但接下來的重試工作就不需繼續增加輪詢時間。舉例來說，如果用戶端使用的輪詢時間上限是 64 秒，達到這個值之後，用戶端就可以維持在每 64 秒重試一次的頻率。到了特定時間點後，用戶端應停止無限重試。

重試之間的等待時間和重試次數，應視用途及您的網路狀況而定。

### 重試插入失敗的工作

如果應用程式需要「只插入一次」的語意，插入作業時請注意其他事項。如何達成「最多一次」語意，取決於您指定的 [WriteDisposition](https://docs.cloud.google.com/bigquery/docs/reference/auditlogs/rest/Shared.Types/BigQueryAuditMetadata.WriteDisposition?hl=zh-tw)。寫入處置會告知 BigQuery 在資料表中遇到現有資料時應採取的動作：失敗、覆寫或附加。

如果處置方式為 `WRITE_EMPTY` 或 `WRITE_TRUNCATE`，只要重試任何失敗的工作插入或執行作業，即可達成此目的。這是因為工作擷取的所有資料列都會以不可分割的方式寫入資料表。

如果處置為 `WRITE_APPEND`，用戶端必須指定工作 ID，避免重試時再次附加相同資料。這是因為 BigQuery 會拒絕嘗試使用先前工作 ID 的工作建立要求。這樣一來，任何指定工作 ID 都會達到「最多一次」的語意。確認 BigQuery 中所有先前的嘗試都失敗後，您可以使用新的可預測工作 ID 重試，即可實現「只執行一次」的目標。

在某些情況下，由於暫時性問題或網路中斷，API 用戶端或 HTTP 用戶端可能無法收到工作已插入的確認訊息。重試插入時，該要求會失敗並傳回 `status=ALREADY_EXISTS` (`code=409` 和 `reason="duplicate"`)。現有工作狀態可透過呼叫 `jobs.get` 擷取。現有工作狀態為 `retrieved` 後，呼叫端可以判斷是否應建立具有新工作 ID 的新工作。

## 應用實例和穩定性需求

BigQuery 可能是各種架構的重要元件。視用途和部署的架構而定，可能需要滿足各種可用性、效能或其他可靠性需求。在本指南中，我們將選取兩個主要用途和架構，並詳細說明。

### 即時分析

第一個範例是事件資料處理管道。在本範例中，系統會使用 Pub/Sub 擷取端點的記錄事件。接著，串流 Dataflow 管道會先對資料執行一些作業，再使用 [Storage Write API](https://docs.cloud.google.com/bigquery/docs/write-api?hl=zh-tw) 將資料寫入 BigQuery。這些資料可用於臨時查詢，例如重現可能導致特定端點結果的事件序列，也可用於提供近乎即時的資訊主頁，以便透過視覺化方式偵測資料中的趨勢和模式。

這個範例需要考量可靠性的多個面向。由於端對端資料更新間隔的要求相當高，因此擷取程序的**延遲時間**至關重要。資料寫入 BigQuery 後，**可靠性**是指使用者能以**一致**且可預測的延遲時間發出臨時查詢，並確保使用資料的資訊主頁反映絕對最新的可用資訊。

### 批次資料處理

第二個例子是批次處理架構，以金融服務業的法規遵循為基礎。其中一項重要需求是每天在固定夜間截止時間前，向監管機構提交報告。只要生成報表的夜間批次程序能在這個期限前完成，就視為速度夠快。

資料必須在 BigQuery 中提供，並與其他資料來源合併，才能製作資訊主頁、進行分析，並最終產生 PDF 報表。準時且正確地交付這些報表，是重要的業務需求。因此，確保資料擷取**可靠**，並在**一致**的時間範圍內正確產生報表，以符合所需期限，是至關重要的環節。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-14 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-14 (世界標準時間)。"],[],[]]