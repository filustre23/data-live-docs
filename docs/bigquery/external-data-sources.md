Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 外部資料來源簡介

外部資料來源可讓您直接從 BigQuery 查詢資料，即使資料並未儲存在 BigQuery 儲存空間中也一樣。例如，您可以分析其他 Google Cloud 資料庫、Cloud Storage 檔案或其他雲端產品中的資料，而不必先遷移資料。

本文概略說明查詢外部資料的方法，包括 BigLake 資料表、物件資料表、外部資料表和聯合查詢，並說明常見用途。

## 用途

外部資料來源的用途包括：

* 對於擷取-載入-轉換 (ELT) 工作負載，使用 `CREATE TABLE ... AS SELECT` 查詢，即可一次載入並清理資料，然後將清理後的結果寫入 BigQuery 儲存空間。
* 彙整 BigQuery 資料表與外部資料來源中變動頻繁的資料。直接查詢外部資料來源，您就不需要在每次資料變更時，重新將資料載入至 BigQuery 儲存空間。

## 外部資料來源資料表

外部資料來源資料表與標準 BigQuery 資料表類似，都會將中繼資料和結構定義儲存在 BigQuery 儲存空間中。但資料位於外部來源。

外部資料來源資料表包含在資料集內，管理方式與標準 BigQuery 資料表相同。例如，您可以[查看資料表的屬性](https://docs.cloud.google.com/bigquery/docs/tables?hl=zh-tw#get_information_about_tables)、[設定存取控管](https://docs.cloud.google.com/bigquery/docs/table-access-controls?hl=zh-tw)等。您可以查詢這些資料表，在多數情況下，您也可以將這些資料表與其他資料表彙整。

外部資料來源資料表有三種：

* BigLake 資料表
* 物件資料表
* 外部資料表

### BigLake 資料表

BigLake 資料表可讓您透過存取權委派功能，查詢外部資料儲存庫中的結構化資料。存取權委派功能會將 BigLake 資料表的存取權，與基礎資料儲存庫的存取權分開。與服務帳戶相關聯的[外部連線](https://docs.cloud.google.com/bigquery/docs/connections-api-intro?hl=zh-tw)，用於連線至資料儲存庫。由於服務帳戶會處理從資料儲存庫擷取資料的作業，因此您只需授予使用者 BigLake 資料表的存取權。這可讓您在資料表層級強制執行精細的安全防護機制，包括[資料列層級](https://docs.cloud.google.com/bigquery/docs/row-level-security-intro?hl=zh-tw)和[資料欄層級](https://docs.cloud.google.com/bigquery/docs/column-level-security-intro?hl=zh-tw)安全性。如果是以 Cloud Storage 為基礎的 BigLake 資料表，您也可以使用[動態資料遮蓋](https://docs.cloud.google.com/bigquery/docs/column-data-masking?hl=zh-tw)。如要進一步瞭解如何使用 BigLake 資料表搭配 Amazon S3 或 Blob 儲存體資料的多雲端分析解決方案，請參閱「[BigQuery Omni](https://docs.cloud.google.com/bigquery/docs/omni-introduction?hl=zh-tw)」。

詳情請參閱「[BigLake 資料表簡介](https://docs.cloud.google.com/bigquery/docs/biglake-intro?hl=zh-tw)」。

### 物件資料表

物件資料表可讓您分析 Cloud Storage 中的非結構化資料。您可以使用遠端函式執行分析，或透過 BigQuery ML 執行推論，然後將這些作業的結果與 BigQuery 中的其他結構化資料彙整。

與 BigLake 資料表一樣，物件資料表也使用存取權委派功能，將物件資料表的存取權與 Cloud Storage 物件的存取權分開。與服務帳戶相關聯的[外部連線](https://docs.cloud.google.com/bigquery/docs/working-with-connections?hl=zh-tw)會用於連線至 Cloud Storage，因此您只需授予使用者物件資料表的存取權。這可讓您強制執行[資料列層級](https://docs.cloud.google.com/bigquery/docs/row-level-security-intro?hl=zh-tw)安全性，並管理使用者可存取的物件。

詳情請參閱「[物件資料表簡介](https://docs.cloud.google.com/bigquery/docs/object-table-introduction?hl=zh-tw)」。

### 外部資料表

外部資料表可讓您查詢外部資料儲存庫中的結構化資料。如要查詢外部資料表，您必須具備外部資料表和外部資料來源的權限。例如，如要查詢使用 Cloud Storage 資料來源的外部資料表，您必須具備下列權限：

* `bigquery.tables.getData`
* `bigquery.jobs.create`
* `storage.buckets.get`
* `storage.objects.get`

詳情請參閱「[外部資料表簡介](https://docs.cloud.google.com/bigquery/docs/external-tables?hl=zh-tw)」。

## 聯合查詢

聯合查詢可讓您將查詢陳述式傳送至 AlloyDB、Spanner 或 Cloud SQL 資料庫，並以臨時資料表的形式傳回結果。聯合查詢會使用 BigQuery Connection API，與 AlloyDB、Spanner 或 Cloud SQL 建立連線。在查詢中，您可以使用 `EXTERNAL_QUERY` 函式，透過該資料庫的 SQL 方言將查詢陳述式傳送至外部資料庫。結果會轉換為 GoogleSQL 資料類型。

詳情請參閱「[聯合查詢簡介](https://docs.cloud.google.com/bigquery/docs/federated-queries-intro?hl=zh-tw)」。

## 外部資料來源功能比較

下表比較外部資料來源的行為：

|  | **BigLake 資料表** | **物件資料表** | **外部資料表** | **聯合查詢** |
| --- | --- | --- | --- | --- |
| **使用存取權委派功能** | 是，透過服務帳戶 | 是，透過服務帳戶 | 否 | 是，透過資料庫使用者帳戶 (僅限 Cloud SQL) |
| **可根據多個來源 URI** | 是 | 是 | 是 (僅限 Cloud Storage) | 不適用 |
| **資料列對應** | 資料列代表檔案內容 | 資料列代表檔案中繼資料 | 資料列代表檔案內容 | 不適用 |
| **可透過連接器由其他資料處理工具存取** | 是 (僅限 Cloud Storage) | 否 | 是 | 不適用 |
| **可與其他 BigQuery 資料表彙整** | 是 (僅限 Cloud Storage) | 是 | 是 | 是 |
| **可做為臨時資料表存取** | 是 (僅限 Cloud Storage) | 否 | 是 | 是 |
| **與 Amazon S3 搭配使用** | [是](https://docs.cloud.google.com/bigquery/docs/omni-aws-introduction?hl=zh-tw) | 否 | 否 | 否 |
| **與 Azure Storage 搭配使用** | [是](https://docs.cloud.google.com/bigquery/docs/omni-azure-introduction?hl=zh-tw) | 否 | 否 | 否 |
| **與 Bigtable 搭配使用** | 否 | 否 | [是](https://docs.cloud.google.com/bigquery/docs/external-data-bigtable?hl=zh-tw) | 否 |
| **與 Spanner 搭配使用** | 否 | 否 | 否 | [是](https://docs.cloud.google.com/bigquery/docs/spanner-federated-queries?hl=zh-tw) |
| **與 Cloud SQL 搭配使用** | 否 | 否 | 否 | [是](https://docs.cloud.google.com/bigquery/docs/cloud-sql-federated-queries?hl=zh-tw) |
| **支援 Google 雲端硬碟** | 否 | 否 | [是](https://docs.cloud.google.com/bigquery/docs/external-data-drive?hl=zh-tw) | 否 |
| **與 Cloud Storage 搭配使用** | [是](https://docs.cloud.google.com/bigquery/docs/query-cloud-storage-using-biglake?hl=zh-tw) | [是](https://docs.cloud.google.com/bigquery/docs/object-tables?hl=zh-tw) | [是](https://docs.cloud.google.com/bigquery/docs/external-data-cloud-storage?hl=zh-tw) | 否 |

## 後續步驟

* 進一步瞭解 [BigLake 資料表](https://docs.cloud.google.com/bigquery/docs/biglake-intro?hl=zh-tw)。
* 進一步瞭解[物件資料表](https://docs.cloud.google.com/bigquery/docs/object-table-introduction?hl=zh-tw)
* 進一步瞭解[外部資料表](https://docs.cloud.google.com/bigquery/docs/external-tables?hl=zh-tw)。
* 進一步瞭解[聯合查詢](https://docs.cloud.google.com/bigquery/docs/federated-queries-intro?hl=zh-tw)。
* 瞭解 [BigQuery 定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#on_demand_pricing)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-10-24 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-10-24 (世界標準時間)。"],[],[]]