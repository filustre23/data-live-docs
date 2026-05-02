* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 載入、轉換及匯出資料簡介

本文說明如何使用擷取、載入及轉換 (ELT) 或擷取、轉換及載入 (ETL) 程序，在 BigQuery 中載入及轉換資料。本文也會說明如何從 BigQuery 匯出資料，以便在其他系統中套用洞察資料，這稱為*反向 ETL*。

## 決定使用 ELT 或 ETL

載入 BigQuery 前後轉換資料是很常見的做法。基本決策是先轉換資料再載入 BigQuery (擷取、轉換與載入或 ETL 方法)，還是將原始資料載入 BigQuery，然後使用 BigQuery 執行轉換 (擷取、載入與轉換或 ELT 方法)。

下圖顯示將資料整合至 BigQuery 的各種選項，包括使用 ELT 或 ETL。

一般來說，我們建議大多數客戶採用 ELT 方法。ELT 工作流程會將複雜的資料整合程序分成兩個可管理的部分：擷取和載入，然後轉換。使用者可以選擇符合需求的各種資料載入方法。將資料載入 BigQuery 後，熟悉 SQL 的使用者就能使用 Dataform 等工具開發轉換管道。

以下各節將詳細說明各個工作流程。

## 載入及轉換資料

載入 BigQuery 前後轉換資料是很常見的做法。以下各節將說明資料整合的兩種常見方法：ETL 和 ELT。

### ELT 資料整合方法

採用擷取、載入及轉換 (ELT) 方法時，您會分兩個步驟執行資料整合：

* 擷取及載入資料
* 轉換資料

舉例來說，您可以從 JSON 檔案來源擷取資料，然後載入至 BigQuery 資料表。接著，您可以使用管道將欄位擷取並轉換至目標資料表。

ELT 方法可透過下列方式簡化資料整合工作流程：

* 不再需要其他資料處理工具
* 將複雜的資料整合程序分成兩個可管理的步驟
* 充分運用 BigQuery 的功能，大規模準備、轉換及最佳化資料

#### 擷取及載入資料

在 ELT 資料整合方法中，您會從資料來源擷取資料，並使用任何支援的[載入或存取外部資料方法](https://docs.cloud.google.com/bigquery/docs/loading-data?hl=zh-tw#methods)，將資料載入 BigQuery。

#### 在 BigQuery 中轉換資料

將資料載入 BigQuery 後，您可以使用下列工具準備及轉換資料：

* 如要共同建構、測試、記錄及排定進階 SQL 資料轉換管道，請使用 [Dataform](https://docs.cloud.google.com/dataform/docs?hl=zh-tw)。
* 如要執行較小的資料轉換工作流程 (例如 SQL 程式碼、Python 筆記本或資料準備作業)，請使用 [BigQuery 管道](https://docs.cloud.google.com/bigquery/docs/pipelines-introduction?hl=zh-tw)。
* 如要清理資料以利分析，請使用 AI 輔助的[資料準備](https://docs.cloud.google.com/bigquery/docs/data-prep-introduction?hl=zh-tw)功能。

這些工具都由 [Dataform API](https://docs.cloud.google.com/dataform/reference/rest?hl=zh-tw) 支援。

詳情請參閱「[轉換簡介](https://docs.cloud.google.com/bigquery/docs/transform-intro?hl=zh-tw)」。

### ETL 資料整合方法

在擷取、轉換、載入 (ETL) 方法中，您會先擷取及轉換資料，再將資料傳送至 BigQuery。如果您已建立資料轉換程序，或是想減少 BigQuery 中的資源用量，這個方法就非常實用。

[Cloud Data Fusion](https://docs.cloud.google.com/data-fusion/docs/concepts/overview?hl=zh-tw) 可協助您簡化 ETL 程序。BigQuery 也與[第三方合作夥伴合作，將資料轉換並載入至 BigQuery](https://docs.cloud.google.com/bigquery/docs/bigquery-ready-partners?hl=zh-tw#etl-data-integration)。

## 正在匯出資料

在 BigQuery 中處理及分析資料後，您可以匯出結果，並套用至其他系統。BigQuery 支援下列匯出作業：

* 將查詢結果匯出至本機檔案、Google 雲端硬碟或 Google 試算表
* 將資料表或查詢結果匯出至 Cloud Storage、Bigtable、Spanner、AlloyDB for PostgreSQL 和 Pub/Sub

這個程序稱為反向 ETL。

詳情請參閱 [BigQuery 資料匯出簡介](https://docs.cloud.google.com/bigquery/docs/export-intro?hl=zh-tw)。

## 後續步驟

* 進一步瞭解如何[在 BigQuery 中載入資料](https://docs.cloud.google.com/bigquery/docs/loading-data?hl=zh-tw)。
* 進一步瞭解如何[在 BigQuery 中轉換資料](https://docs.cloud.google.com/bigquery/docs/transform-intro?hl=zh-tw)。
* 進一步瞭解如何[在 BigQuery 中匯出資料](https://docs.cloud.google.com/bigquery/docs/export-intro?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-02 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-02 (世界標準時間)。"],[],[]]