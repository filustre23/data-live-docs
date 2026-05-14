Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 資料載入簡介

本文說明如何將資料載入 BigQuery。資料整合的兩種常見方法是擷取、載入及轉換 (ELT)，或是擷取、轉換及載入 (ETL) 資料。

如要瞭解 ELT 和 ETL 方法的總覽，請參閱[載入、轉換及匯出資料簡介](https://docs.cloud.google.com/bigquery/docs/load-transform-export-intro?hl=zh-tw)。

## 載入或存取外部資料的方法

在 BigQuery 頁面的「新增資料」[對話方塊](https://docs.cloud.google.com/bigquery/docs/bigquery-web-ui?hl=zh-tw#studio-overview)中，您可以查看所有可用的方法，將資料載入 BigQuery 或存取 BigQuery 中的資料。根據用途和資料來源，選擇下列其中一個選項：

| 載入方法 | 說明 |
| --- | --- |
| **批次載入** | 這個方法適合從各種來源批次載入大量資料。   如要從 Cloud Storage 和其他支援的資料來源批次或增量載入資料，建議使用 [BigQuery 資料移轉服務](https://docs.cloud.google.com/bigquery/docs/dts-introduction?hl=zh-tw)。   使用 BigQuery 資料移轉服務，您可以排定載入工作，自動將資料載入管道移至 BigQuery。您可以安排一次性或批次資料移轉作業，並設定定期執行間隔 (例如每日或每月)。為確保 BigQuery 資料一律為最新狀態，您可以監控及記錄移轉作業。   如要查看 BigQuery 資料移轉服務支援的資料來源清單，請參閱「[支援的資料來源](https://docs.cloud.google.com/bigquery/docs/dts-introduction?hl=zh-tw#supported_data_sources)」。 |
| **串流負荷** | 這個方法可從訊息傳遞系統近乎即時載入資料。   如要將資料串流至 BigQuery，您可以在 [Pub/Sub](https://docs.cloud.google.com/pubsub/docs/overview?hl=zh-tw) 中使用 BigQuery 訂閱項目。Pub/Sub 可處理高處理量資料，並載入 BigQuery。支援即時資料串流，可在資料產生時載入。詳情請參閱「[BigQuery 訂閱項目](https://docs.cloud.google.com/pubsub/docs/bigquery?hl=zh-tw)」。 |
| **變更資料擷取 (CDC)** | 這個方法可將資料從資料庫複製到 BigQuery，且近乎即時。   [Datastream](https://docs.cloud.google.com/datastream/docs/overview?hl=zh-tw) 可將資料從資料庫串流至 BigQuery 資料，並以近乎即時的方式複製資料。Datastream 會運用 CDC 功能，追蹤及複製資料來源的資料列層級變更。   如需 Datastream 支援的資料來源清單，請參閱「[來源](https://docs.cloud.google.com/datastream/docs/sources?hl=zh-tw)」。 |
| **與外部資料來源聯盟** | 這個方法可存取外部資料，不必將資料載入 BigQuery。   BigQuery 支援透過 Cloud Storage 和聯合查詢，存取特定[外部資料來源](https://docs.cloud.google.com/bigquery/docs/external-data-sources?hl=zh-tw)。這個方法的優點是，您不必先載入資料，再轉換資料以供後續使用。您可以對外部資料執行 `SELECT` 陳述式，進行轉換。 |

您也可以使用下列程式輔助方法載入資料：

| 載入方法 | 說明 |
| --- | --- |
| **批次載入** | 您可以建立載入工作，[從 Cloud Storage 或本機檔案載入資料](https://docs.cloud.google.com/bigquery/docs/batch-loading-data?hl=zh-tw)。   如果來源資料不常變更，或您不需要持續更新的結果，載入工作就是將資料載入 BigQuery 的經濟實惠方式，且不會耗用大量資源。    載入的資料可以是 Avro、CSV、JSON、ORC 或 Parquet 格式。如要建立載入工作，您也可以使用 [`LOAD DATA`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/load-statements?hl=zh-tw) SQL 陳述式。   熱門的開放原始碼系統 (例如 [Spark](https://docs.cloud.google.com/dataproc/docs/tutorials/bigquery-connector-spark-example?hl=zh-tw)) 和各種 [ETL 合作夥伴](https://docs.cloud.google.com/bigquery/docs/bigquery-ready-partners?hl=zh-tw#etl-data-integration)，也支援將資料批次載入 BigQuery。   如要最佳化資料表批次載入作業，避免達到每日載入上限，請參閱「[最佳化載入工作](https://docs.cloud.google.com/bigquery/docs/optimize-load-jobs?hl=zh-tw)」。 |
| **串流負荷** | 如需支援自訂串流資料來源，或在將資料以高輸送量串流至 BigQuery 前預先處理資料，請使用 [Dataflow](https://docs.cloud.google.com/dataflow/docs?hl=zh-tw)。   如要進一步瞭解如何從 Dataflow 載入至 BigQuery，請參閱「[從 Dataflow 寫入至 BigQuery](https://docs.cloud.google.com/dataflow/docs/guides/write-to-bigquery?hl=zh-tw)」。   您也可以直接使用 [BigQuery Storage Write API](https://docs.cloud.google.com/bigquery/docs/write-api?hl=zh-tw)。   如要最佳化資料表串流，避免達到每日載入上限，請參閱「[最佳化載入工作](https://docs.cloud.google.com/bigquery/docs/optimize-load-jobs?hl=zh-tw)」。 |

[Cloud Data Fusion](https://docs.cloud.google.com/data-fusion/docs/concepts/overview?hl=zh-tw) 可協助您簡化 ETL 程序。BigQuery 也與[第三方合作夥伴合作，將資料轉換並載入至 BigQuery](https://docs.cloud.google.com/bigquery/docs/bigquery-ready-partners?hl=zh-tw#etl-data-integration)。

BigQuery 可讓您建立外部連線，查詢儲存在 BigQuery 以外的資料，例如 Cloud Storage 或 Spanner 等 Google Cloud 服務，或是 Amazon Web Services (AWS) 或 Microsoft Azure 等第三方來源。這些外部連結會使用 BigQuery Connection API。詳情請參閱「[連線簡介](https://docs.cloud.google.com/bigquery/docs/connections-api-intro?hl=zh-tw)」。

## 其他取得資料的方式

您可以對資料執行查詢，不必自行將資料載入 BigQuery。以下各節說明一些替代方案。

以下列出部分替代方案：

### 查詢公開資料

公開資料集是儲存在 BigQuery 中並與大眾共用的資料集。詳情請參閱 [BigQuery 公開資料集](https://docs.cloud.google.com/bigquery/public-data?hl=zh-tw)。

### 對共用資料執行查詢

如要查詢他人與您共用的 BigQuery 資料集，請參閱「[BigQuery sharing (舊稱 Analytics Hub) 簡介](https://docs.cloud.google.com/bigquery/docs/analytics-hub-introduction?hl=zh-tw)」。「共用」是資料交換平台，可進行資料共用。

### 使用記錄資料執行查詢

您可以在記錄檔上執行查詢，不必建立額外的載入工作：

* **Cloud Logging** 可讓您[將記錄檔轉送至 BigQuery 目的地](https://docs.cloud.google.com/logging/docs/export/configure_export?hl=zh-tw)。
* **可觀測性分析**可讓您[執行查詢來分析記錄檔資料](https://docs.cloud.google.com/logging/docs/log-analytics?hl=zh-tw#analytics)。

## 後續步驟

* 瞭解如何使用 Gemini 版 BigQuery[準備資料](https://docs.cloud.google.com/bigquery/docs/data-prep-introduction?hl=zh-tw)。
* 進一步瞭解如何使用 [Dataform](https://docs.cloud.google.com/dataform/docs/overview?hl=zh-tw) 轉換資料。
* 如要進一步瞭解如何監控載入工作，請參閱[管理工作探索器](https://docs.cloud.google.com/bigquery/docs/admin-jobs-explorer?hl=zh-tw)和 [BigQuery 指標](https://docs.cloud.google.com/monitoring/api/metrics_gcp_a_b?hl=zh-tw#gcp-bigquery)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-14 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-14 (世界標準時間)。"],[],[]]