Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 資料匯出簡介

本文說明從 BigQuery 匯出資料的各種方式。

如要進一步瞭解資料整合，請參閱[載入、轉換及匯出資料簡介](https://docs.cloud.google.com/bigquery/docs/load-transform-export-intro?hl=zh-tw)。

## 匯出查詢結果

您可以將查詢結果匯出至本機檔案 (CSV 或 JSON 檔案)、Google 雲端硬碟或 Google 試算表。詳情請參閱「[將查詢結果匯出至檔案](https://docs.cloud.google.com/bigquery/docs/export-file?hl=zh-tw)」。

## 匯出資料表

您可以匯出下列資料格式的 BigQuery 資料表：

| 資料格式 | 支援的壓縮類型 | 支援的匯出方法 |
| --- | --- | --- |
| CSV | GZIP | [匯出至 Cloud Storage](https://docs.cloud.google.com/bigquery/docs/exporting-data?hl=zh-tw) |
| JSON | GZIP | [匯出至 Cloud Storage](https://docs.cloud.google.com/bigquery/docs/exporting-data?hl=zh-tw)  [使用 Dataflow 從 BigQuery 讀取資料](https://docs.cloud.google.com/dataflow/docs/guides/read-from-bigquery?hl=zh-tw) |
| Avro | DEFLATE、SNAPPY | [匯出至 Cloud Storage](https://docs.cloud.google.com/bigquery/docs/exporting-data?hl=zh-tw)  [使用 Dataflow 從 BigQuery 讀取資料](https://docs.cloud.google.com/dataflow/docs/guides/read-from-bigquery?hl=zh-tw) |
| Parquet | GZIP、SNAPPY、ZSTD | [匯出至 Cloud Storage](https://docs.cloud.google.com/bigquery/docs/exporting-data?hl=zh-tw) |

處理需要物件類型安全性的巢狀資料結構，或需要更廣泛的語言支援時，您也可以[將 BigQuery 資料表匯出為 Protobuf 資料欄](https://docs.cloud.google.com/bigquery/docs/protobuf-export?hl=zh-tw)。

### 匯出大型資料表注意事項

從 BigQuery 匯出大量資料時，請注意下列事項：

* **資料量和格式**：
  + 計算要匯出的資料量。視資料大小、格式、方法和地理位置而定，匯出作業可能會產生大量費用。部分資源以每 GiB 為單位計費，其他則以每 TiB 為單位計費。
  + 選擇與分析工具和資料結構相容的格式。
    舉例來說，CSV 無法處理巢狀或重複欄位。檢查資料類型相容性。
  + 建議您使用壓縮格式，縮減大小並降低費用。
* **匯出費用**：
  + 部分匯出方法提供免費額度，其他方法則一律會產生費用。
    詳情請參閱[資料擷取定價](https://docs.cloud.google.com/bigquery/pricing?hl=zh-tw#data-extraction-pricing)。
  + 如果 BigQuery 資料表和目的地 (例如 Cloud Storage bucket) 位於不同位置，可能會產生費用。
* **配額**：部分匯出方法設有每日上限。詳情請參閱「[擷取作業](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#export_jobs)」。
* **多個檔案**：大型匯出檔案會分割成多個檔案。請考慮如何管理這些下游檔案。
* **自動化**：如要定期匯出資料，請使用 [BigQuery 排程查詢](https://docs.cloud.google.com/bigquery/docs/scheduling-queries?hl=zh-tw)或 [Dataflow](https://docs.cloud.google.com/dataflow/docs/overview?hl=zh-tw)。
* **保留政策**：決定目標資料集中的保留期限，並實作生命週期規則，盡量降低儲存空間費用。
* **安全性和存取控管**：實作適當的 IAM 權限和加密。

考量這些因素時，建議您對資料子集執行測試匯出作業，評估成本、檔案大小、計數和時間。您可以在 `EXPORT DATA` SQL 陳述式中使用 `WHERE` 子句，限制匯出測試。

## 匯出 BigQuery 程式碼資產

您可以下載 [BigQuery Studio](https://docs.cloud.google.com/bigquery/docs/query-overview?hl=zh-tw#bigquery-studio) 程式碼資產，例如[已儲存的查詢](https://docs.cloud.google.com/bigquery/docs/saved-queries-introduction?hl=zh-tw)或[筆記本](https://docs.cloud.google.com/bigquery/docs/programmatic-analysis?hl=zh-tw)，在本機保留資產副本。如要進一步瞭解如何下載 BigQuery 程式碼資產，請參閱下列文章：

* [下載已儲存的查詢](https://docs.cloud.google.com/bigquery/docs/manage-saved-queries?hl=zh-tw#download_saved_queries)
* [下載筆記本](https://docs.cloud.google.com/bigquery/docs/manage-notebooks?hl=zh-tw#download_a_notebook)

## 使用反向 ETL 匯出

您可以設定反向 ETL (RETL) 工作流程，將資料從 BigQuery 移至下列資料庫：

* [匯出至 Bigtable](https://docs.cloud.google.com/bigquery/docs/export-to-bigtable?hl=zh-tw)
* [匯出至 Spanner](https://docs.cloud.google.com/bigquery/docs/export-to-spanner?hl=zh-tw)
* [匯出至 Pub/Sub](https://docs.cloud.google.com/bigquery/docs/export-to-pubsub?hl=zh-tw)
* [匯出至 AlloyDB](https://docs.cloud.google.com/bigquery/docs/export-to-alloydb?hl=zh-tw) ([預先發布版](https://cloud.google.com/products?hl=zh-tw#product-launch-stages))

## 後續步驟

* 瞭解[擷取工作的配額](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#export_jobs)。
* 瞭解 [BigQuery 儲存空間定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#storage)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-10-15 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-10-15 (世界標準時間)。"],[],[]]