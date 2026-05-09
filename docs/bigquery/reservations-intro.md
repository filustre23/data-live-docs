Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 工作負載管理簡介

透過 BigQuery 工作負載管理，您可以分配及管理可用於資料分析和處理的運算資源，並指定這些資源的計費方式。

## 工作負載管理模型

BigQuery 提供兩種工作負載管理模式。採用*以量計價*時，您只需為查詢或處理資料時所處理的位元組數付費。*以容量為準*的計費方式可讓您為工作負載分配處理容量，並視需要自動調高或調低容量。

您隨時可以在以量計價和容量計費模式之間切換。
你也可以[結合這兩種模式](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#combine_reservations_with_on-demand_billing)。

## 選擇模型

選擇工作負載管理模型時，請考量下列事項：

|  | **以量計價** | **以容量為準** |
| --- | --- | --- |
| **用量模式** | 查詢掃描或處理的資料 | 專屬運算單元或自動調度運算單元 |
| **計量單位** | TiB | 運算單元小時 |
| **容量下限** | 每項專案最多 2,000 個運算單元 | 每個預留項目 50 個運算單元 |
| **容量上限** | 每項專案最多 2,000 個運算單元 | 每個預訂最多可設定區域配額 |
| **費用控管** | (選用) 設定專案層級或使用者層級配額 (硬性上限) | 為每個預訂設定以空位數表示的預算 |
| **設定** | 不需要設定 | 建立運算單元預留項目並指派給專案 |
| **版本支援** | 固定特徵集 | 提供 3 種版本 |
| **容量折扣** | 僅限即付即用 | 穩態工作負載的選用型時段承諾 |
| **可預測性** | 用量和帳單視情況而定 | 透過基準和承諾用量預估帳單費用 |
| **集中採購** | 依專案計費 | 集中分配運算單元並結算費用，不必為每個專案分別處理 |
| **工作彈性** | 隨選容量 (每項查詢至少 10 MiB) | 基準或自動調度資源的運算單元 (至少 1 分鐘) |

## 工作

每當您[載入](https://docs.cloud.google.com/bigquery/docs/loading-data?hl=zh-tw)、[匯出](https://docs.cloud.google.com/bigquery/exporting-data-from-bigquery?hl=zh-tw)、[查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw)或[複製資料](https://docs.cloud.google.com/bigquery/docs/managing-tables?hl=zh-tw#copy-table)時，BigQuery 會自動建立、排定及執行工作，追蹤工作進度。

因為工作可能需要長時間才能完成，所以會非同步執行，而且可以輪詢其狀態。執行時間較短的動作 (如列出資源或取得中繼資料) 不會以工作形式管理。

如要進一步瞭解工作，請參閱「[管理工作](https://docs.cloud.google.com/bigquery/docs/managing-jobs?hl=zh-tw)」。

## 運算單元

BigQuery 運算單元是 BigQuery 用來執行 SQL 查詢或其他[工作類型](https://docs.cloud.google.com/bigquery/docs/managing-jobs?hl=zh-tw)的*虛擬運算單元*。執行查詢時，BigQuery 會自動判斷查詢使用的運算單元數量。使用的運算單元數量取決於處理的資料量、查詢的複雜程度，以及可用的運算單元數量。

如要進一步瞭解運算單元及其用途，請參閱「[瞭解運算單元](https://docs.cloud.google.com/bigquery/docs/slots?hl=zh-tw)」。

## 預留項目

在以容量為準的計費模式中，系統會將運算單元分配到稱為「預留項目」的集區。保留項目可讓您以適合貴機構的方式指派運算單元。舉例來說，您可以為實際工作環境工作負載建立名為 `prod` 的保留項目，並為測試建立名為 `test` 的獨立保留項目，這樣測試工作就不會與實際工作環境工作負載爭用容量。或者，您也可以為機構內的不同部門建立預約。

如要進一步瞭解預留項目，請參閱[使用預留項目進行工作負載管理](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw)。

## BI Engine

BI Engine 是一種快速的記憶體內分析服務，可智慧快取最常使用的資料，藉此加快 BigQuery 中許多 SQL 查詢的速度。BI Engine 可加速處理來自任何來源的 SQL 查詢 (包括資料視覺化工具編寫的查詢)，並管理快取資料表，持續進行最佳化。

[BI Engine 保留項目](https://docs.cloud.google.com/bigquery/docs/bi-engine-reserve-capacity?hl=zh-tw)會以 GiB 的記憶體大小分配，並與時段保留項目分開管理。

如要進一步瞭解 BI Engine，請參閱「[BI Engine 簡介](https://docs.cloud.google.com/bigquery/docs/bi-engine-intro?hl=zh-tw)」。

## 後續步驟

* [瞭解運算單元](https://docs.cloud.google.com/bigquery/docs/slots?hl=zh-tw)
* [瞭解預留項目](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw)
* 瞭解[隨選定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#on_demand_pricing)
* 瞭解[以容量為準的定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#capacity_compute_analysis_pricing)
* [估算及控管費用](https://docs.cloud.google.com/bigquery/docs/best-practices-costs?hl=zh-tw)
* [建立自訂費用控管機制](https://docs.cloud.google.com/bigquery/docs/custom-quotas?hl=zh-tw)




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-08 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-08 (世界標準時間)。"],[],[]]