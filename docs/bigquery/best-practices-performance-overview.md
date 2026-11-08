Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 最佳化查詢效能簡介

在 BigQuery 最佳化查詢，可縮短執行時間、減少資源消耗，並盡可能降低成本和查詢失敗率。一般來說，查詢時需要完成的工作越少，執行速度就越快，消耗的運算和儲存資源也越少。

## 查詢效能

評估 BigQuery 的查詢效能時，須考量多項因素：

* [輸入資料和資料來源 (I/O)](https://docs.cloud.google.com/bigquery/docs/best-practices-performance-compute?hl=zh-tw#reduce-data-processed)：查詢作業會讀取多少位元組數？
* [(隨機排列) 節點間的通訊](https://docs.cloud.google.com/bigquery/docs/best-practices-performance-compute?hl=zh-tw#reduce-data-processed)：查詢作業會傳送多少位元組數到下一個階段？查詢作業會傳送多少位元組數到每一個運算單元？
* [計算](https://docs.cloud.google.com/bigquery/docs/best-practices-performance-compute?hl=zh-tw#optimize-query-operations)：查詢需要使用多少 CPU 工作負載？
* [輸出 (實質關聯性)](https://docs.cloud.google.com/bigquery/docs/best-practices-performance-compute?hl=zh-tw#reduce-query-output)：查詢作業會寫入多少位元組數？
* [容量和並行](#capacity-and-concurrency)：有多少可用運算單元，以及有多少其他查詢同時執行？
* [查詢模式](https://docs.cloud.google.com/bigquery/docs/best-practices-performance-patterns?hl=zh-tw)：查詢是否遵循 SQL 最佳做法？

如要評估特定查詢，或確認是否發生資源爭用情形，您可以使用 [Cloud Monitoring](https://docs.cloud.google.com/bigquery/docs/monitoring?hl=zh-tw) 或 [BigQuery 管理資源圖表](https://docs.cloud.google.com/bigquery/docs/admin-resource-charts?hl=zh-tw)，監控 BigQuery 工作在一段時間內的資源消耗情形。您也可以使用 Gemini Cloud Assist [分析工作](https://docs.cloud.google.com/bigquery/docs/use-cloud-assist?hl=zh-tw#analyze_jobs)。如果發現查詢速度緩慢或耗用大量資源，可以著重於最佳化該查詢的效能。

部分查詢模式 (尤其是商業智慧工具產生的模式) 可透過 [BigQuery BI Engine](https://docs.cloud.google.com/bigquery/docs/bi-engine-intro?hl=zh-tw) 加速。BI Engine 是一項快速的記憶體內分析服務，可智慧快取最常使用的資料，加快 BigQuery 中的許多 SQL 查詢。BI Engine 內建於 BigQuery，因此通常不必修改查詢，就能提升效能。

與任何系統一樣，最佳化效能有時也需要進行取捨。
舉例來說，對非 SQL 專家的人而言，使用進階 SQL 語法有時可能會增加複雜性，並降低他們對查詢的理解。
如果花時間對非關鍵工作負載進行微幅最佳化，也可能會分散資源，無法為應用程式建構新功能，或找出更重要的最佳化項目。為盡可能提高投資報酬率，建議您著重於最佳化對資料分析管道最重要的工作負載。

## 容量和並行最佳化

BigQuery 提供兩種查詢計價模式：[隨選](https://cloud.google.com/bigquery/pricing?hl=zh-tw#on_demand_pricing)計價和[依運算能力計價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#capacity_compute_analysis_pricing)。隨選模式提供共用運算資源集區，費用取決於您執行的每個查詢所處理的資料量。

如果您想預算固定的每月支出，或需要比隨選模式更多的容量，建議採用[容量型](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw)模式。使用以運算資源為基礎的定價模式時，您會分配專屬的查詢處理資源，並以[運算單元](https://docs.cloud.google.com/bigquery/docs/slots?hl=zh-tw)為單位計算。所有處理位元組的費用都包含在依用量計費的價格中。除了固定的[運算單元承諾使用合約](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#slot_commitments)，您也可以使用[自動調度運算單元](https://docs.cloud.google.com/bigquery/docs/slots-autoscaling-intro?hl=zh-tw)，根據查詢工作負載動態調整容量。

對相同資料重複執行查詢時，效能可能會有所不同，而且使用隨選運算單元的查詢，其效能差異通常大於使用預留運算單元的查詢。

在 SQL 查詢處理期間，BigQuery 會將執行查詢各階段所需的運算能力細分為運算單元。BigQuery 會自動判斷可同時執行的查詢數量，如下所示：

* 隨選模式：專案中的可用運算單元數量
* 以運算資源為準的模型：預留項目中的可用運算單元數量

如果查詢所需的運算單元數量超過可用數量，就會[排入佇列](https://docs.cloud.google.com/bigquery/docs/query-queues?hl=zh-tw)，直到有可用的處理資源為止。查詢開始執行後，BigQuery 會根據階段大小、複雜程度和可用運算單元數量，計算每個查詢階段使用的運算單元數量。BigQuery 採用稱為「公平排程」的技術，確保每項查詢都有足夠的容量可執行。

存取更多運算單元不一定能加快查詢速度。不過，如果運算單元集區較大，則可提升大型或複雜查詢的效能，以及高並行工作負載的效能。修改運算單元預留項目或自動調度資源限制來增加容量時，BigQuery 的排程器可能會為個別查詢分配更多運算單元，盡可能提高平行處理能力並縮短延遲時間。由於同時運作的運算單元增加，查詢耗用的總運算單元時間 (`total_slot_ms`) 也可能增加。這代表預期的成本和效能權衡：查詢執行速度更快，但會耗用更多運算單元時間。

如要提高查詢效能，可以[修改預留運算單元](https://docs.cloud.google.com/bigquery/docs/reservations-tasks?hl=zh-tw)，或提高[運算單元自動調度資源](https://docs.cloud.google.com/bigquery/docs/slots-autoscaling-intro?hl=zh-tw)的上限。您也可以使用 Gemini Cloud Assist，[透過自然語言提示管理預留項目和容量](https://docs.cloud.google.com/bigquery/docs/use-cloud-assist?hl=zh-tw#administer_bigquery)。

## 查詢計畫和執行圖

每次執行查詢時，BigQuery 都會產生[查詢計畫](https://docs.cloud.google.com/bigquery/query-plan-explanation?hl=zh-tw)。瞭解這項計畫是有效最佳化查詢的關鍵。查詢計畫包含執行統計資料，例如讀取的位元組數和消耗的運算單元時間。查詢計畫也包含不同執行階段的詳細資料，可協助您診斷及改善查詢效能。[查詢執行圖](https://docs.cloud.google.com/bigquery/docs/query-insights?hl=zh-tw)提供圖形介面，可查看查詢計畫及診斷查詢效能問題。

您也可以使用 [`jobs.get` API 方法](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs/get?hl=zh-tw)或 [`INFORMATION_SCHEMA.JOBS` 檢視表](https://docs.cloud.google.com/bigquery/docs/information-schema-jobs?hl=zh-tw)，擷取查詢計畫和時間軸資訊。[BigQuery Visualizer](https://github.com/GoogleCloudPlatform/professional-services/tree/master/tools/bq-visualizer) 是一種開放原始碼工具，可直觀呈現 BigQuery 工作中執行階段的流程，並使用這項資訊。

BigQuery 執行查詢工作時，會將宣告式 SQL 陳述式轉換為執行圖。這個圖會再細分成一連串的查詢階段，而這些階段本身是由更精細的執行步驟集所組成。BigQuery 使用大量分散式平行架構來執行這些查詢。BigQuery 的階段則是模擬許多潛在工作站可能平行執行的工作單元。各階段之間是使用[快速的分散式重組基礎架構](https://cloud.google.com/blog/products/gcp/in-memory-query-execution-in-google-bigquery?hl=zh-tw)通訊。

如要估算查詢在運算方面的費用有多高，可查看查詢使用的總運算單元秒數。運算單元秒數越低越好，因為這表示有更多資源可供同一專案中同時執行的其他查詢使用。

查詢執行圖可協助您瞭解 BigQuery 如何執行查詢，以及特定階段是否占據大部分資源。例如，`JOIN` 階段產生的輸出資料列比輸入資料列多很多，可能表示可以在查詢中更早進行篩選。
然而，服務的代管性質限制了部分詳細資料是否可以直接操作。如需改善查詢執行和效能的最佳做法和技術，請參閱「[最佳化查詢運算](https://docs.cloud.google.com/bigquery/docs/best-practices-performance-compute?hl=zh-tw)」。

## 後續步驟

* 瞭解如何使用 [BigQuery 稽核記錄](https://docs.cloud.google.com/bigquery/docs/reference/auditlogs?hl=zh-tw)排解查詢執行問題。
* 瞭解 BigQuery 的其他[費用控管技術](https://docs.cloud.google.com/bigquery/docs/controlling-costs?hl=zh-tw)。
* 使用 [`INFORMATION_SCHEMA.JOBS` 檢視表](https://docs.cloud.google.com/bigquery/docs/information-schema-jobs?hl=zh-tw)，查看 BigQuery 工作的近乎即時中繼資料。
* 瞭解如何使用 [BigQuery 系統資料表報表](https://github.com/GoogleCloudPlatform/bigquery-utils/tree/master/dashboards/system_tables)監控 BigQuery 用量。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-11-04 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-11-04 (世界標準時間)。"],[],[]]