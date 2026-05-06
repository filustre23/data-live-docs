Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 最佳化查詢效能簡介

本文提供最佳化技巧總覽，可提升 BigQuery 的查詢效能。一般來說，查詢時需要完成的工作越少，成效就會越好。執行速度更快，耗用的資源更少，因此可降低成本並減少失敗次數。

## 查詢效能

評估 BigQuery 中的查詢效能時，需要考慮多項因素：

* [輸入資料和資料來源 (I/O)](https://docs.cloud.google.com/bigquery/docs/best-practices-performance-compute?hl=zh-tw#reduce-data-processed)：查詢作業會讀取多少位元組數？
* [(隨機排列) 節點間的通訊](https://docs.cloud.google.com/bigquery/docs/best-practices-performance-compute?hl=zh-tw#reduce-data-processed)：查詢作業會傳送多少位元組數到下一個階段？查詢作業會傳送多少位元組數到每一個運算單元？
* [計算](https://docs.cloud.google.com/bigquery/docs/best-practices-performance-compute?hl=zh-tw#optimize-query-operations)：查詢需要使用多少 CPU 工作負載？
* [輸出 (實質關聯性)](https://docs.cloud.google.com/bigquery/docs/best-practices-performance-compute?hl=zh-tw#reduce-query-output)：查詢作業會寫入多少位元組數？
* [容量和並行](#capacity-and-concurrency)：有多少可用運算單元，以及有多少其他查詢同時執行？
* [查詢模式](https://docs.cloud.google.com/bigquery/docs/best-practices-performance-patterns?hl=zh-tw)：查詢是否遵循 SQL 最佳做法？

如要評估特定查詢或資源爭用情形，可以使用 [Cloud Monitoring](https://docs.cloud.google.com/bigquery/docs/monitoring?hl=zh-tw) 或 [BigQuery 管理資源圖表](https://docs.cloud.google.com/bigquery/docs/admin-resource-charts?hl=zh-tw)，監控 BigQuery 工作長期資源使用情形。您也可以使用 Gemini Cloud Assist [分析工作](https://docs.cloud.google.com/bigquery/docs/use-cloud-assist?hl=zh-tw#analyze_jobs)。如發現有速度緩慢或資源密集型的查詢，可以將效能最佳化集中在該查詢上。

部分查詢模式 (尤其是商業智慧工具產生的模式) 可使用 [BigQuery BI Engine](https://docs.cloud.google.com/bigquery/docs/bi-engine-query?hl=zh-tw) 加速。BI Engine 是一種快速的記憶體內分析服務，可智慧快取最常使用的資料，藉此加快 BigQuery 中許多 SQL 查詢的速度。BI Engine 內建於 BigQuery，因此您通常不需要修改查詢，就能獲得更出色的效能。

與任何系統一樣，最佳化效能有時也需要進行取捨。
舉例來說，對非 SQL 專家的人而言，使用進階 SQL 語法有時可能會增加複雜性，並降低他們對查詢的理解。
將時間花費在對非關鍵工作負載進行微最佳化，也可能占用可用在為應用程式建構新功能或找出更重要最佳化的資源。為協助您獲得最高投資報酬率，我們建議您將最佳化心力集中在對資料分析管道最重要的工作負載上。

## 針對容量和並行進行最佳化

BigQuery 針對查詢提供了兩種計費模式：[以量計價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#on_demand_pricing)與[以容量計價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#capacity_compute_analysis_pricing)。以量計價模式提供共用的容量集區，費用取決於您執行的每個查詢所處理的資料量。

如果您想規劃每月支出預算，或需要的容量超出以量計價模式的上限，建議採用[容量計價](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw)模式。採用以容量為準的計價方式時，您會分配以[運算單元](https://docs.cloud.google.com/bigquery/docs/slots?hl=zh-tw)為計算單位的查詢處理專用容量。系統處理所有位元組所產生的費用，都會包含在以容量為準的價格中。除了固定的[運算單元承諾](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#slot_commitments)，您也可以使用[自動調度運算單元](https://docs.cloud.google.com/bigquery/docs/slots-autoscaling-intro?hl=zh-tw)，根據查詢工作負載提供動態容量。

對相同資料重複執行的查詢效能可能會有所不同，而且使用隨選時段的查詢，效能差異通常會比使用時段預訂的查詢更大。

在處理 SQL 查詢時，BigQuery 會將執行查詢各階段所需的運算能力細分為運算單元。BigQuery 會自動決定可同時執行的查詢數量，方式如下：

* 以量計價模型：專案可用的運算單元數量
* 以容量為準的模型：預留項目可用的運算單元數量

如果查詢要求的運算單元數量高於可用數量，系統會將查詢[排入佇列](https://docs.cloud.google.com/bigquery/docs/query-queues?hl=zh-tw)，直到處理資源可用為止。查詢開始執行後，BigQuery 會根據階段大小和複雜度，以及可用運算單元數量，計算每個查詢階段使用的運算單元數量。BigQuery 會使用「公平排程」技術，確保每項查詢都有足夠的容量可供執行。

使用更多運算單元不一定能加快查詢速度。但若運算單元集區較大，也許可以為大型或非常複雜的查詢提升效能，也能提升高度並行工作負載的效能。如要提升查詢效能，可以[修改時段預訂](https://docs.cloud.google.com/bigquery/docs/reservations-tasks?hl=zh-tw)，或為[時段自動調度資源](https://docs.cloud.google.com/bigquery/docs/slots-autoscaling-intro?hl=zh-tw)設定較高的限制。

## 查詢計畫和執行圖表

每次執行查詢時，BigQuery 都會產生[查詢計畫](https://docs.cloud.google.com/bigquery/query-plan-explanation?hl=zh-tw)。瞭解這項計畫對於有效最佳化查詢至關重要。查詢計畫包含執行統計資料，例如讀取的位元組數和耗用的時段時間。查詢計畫也包含執行作業各階段的詳細資料，可協助您診斷及提升查詢效能。[查詢執行圖](https://docs.cloud.google.com/bigquery/docs/query-insights?hl=zh-tw)提供圖形介面，可查看查詢計畫及診斷查詢效能問題。

您也可以使用 [`jobs.get` API 方法](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs/get?hl=zh-tw)或 [`INFORMATION_SCHEMA.JOBS` 檢視](https://docs.cloud.google.com/bigquery/docs/information-schema-jobs?hl=zh-tw)，擷取查詢計畫和時間軸資訊。[BigQuery Visualizer](https://github.com/GoogleCloudPlatform/professional-services/tree/master/tools/bq-visualizer) 會使用這項資訊。BigQuery Visualizer 是一個開放原始碼工具，能以視覺方式呈現 BigQuery 工作中的執行階段流程。

BigQuery 執行查詢工作時，會將 SQL 宣告陳述式轉換成執行圖。這個圖會再細分成一連串的查詢階段，而這些階段本身是由更精細的執行步驟集所組成。BigQuery 使用大量分散式平行架構來執行這些查詢。BigQuery 的階段則是模擬許多潛在工作站可能平行執行的工作單元。各階段之間是使用[快速的分散式重組基礎架構](https://cloud.google.com/blog/products/gcp/in-memory-query-execution-in-google-bigquery?hl=zh-tw)通訊。

如要估算查詢在運算方面的費用有多高，可查看查詢使用的總運算單元秒數。運算單元秒數越低越好，因為這表示有更多資源可供同一專案中同時執行的其他查詢使用。

查詢執行圖可協助您瞭解 BigQuery 執行查詢的方式，以及是否有特定階段霸占資源使用量。例如，`JOIN` 階段產生的輸出資料列比輸入資料列多很多，可能表示可以在查詢中更早進行篩選。
然而，服務的代管性質限制了部分詳細資料是否可以直接操作。如要瞭解改善查詢執行和效能的最佳做法和技術，請參閱「[最佳化查詢運算](https://docs.cloud.google.com/bigquery/docs/best-practices-performance-compute?hl=zh-tw)」。

## 後續步驟

* 瞭解如何使用 [BigQuery 稽核記錄](https://docs.cloud.google.com/bigquery/docs/reference/auditlogs?hl=zh-tw)排解查詢執行問題。
* 瞭解其他 [BigQuery 費用控管技巧](https://docs.cloud.google.com/bigquery/docs/controlling-costs?hl=zh-tw)。
* 使用 [`INFORMATION_SCHEMA.JOBS` 檢視畫面](https://docs.cloud.google.com/bigquery/docs/information-schema-jobs?hl=zh-tw)，查看 BigQuery 工作近乎即時的中繼資料。
* 瞭解如何使用 [BigQuery 系統資料表報表](https://github.com/GoogleCloudPlatform/bigquery-utils/tree/master/dashboards/system_tables)監控 BigQuery 用量。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-06 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-06 (世界標準時間)。"],[],[]]