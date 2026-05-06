Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# BigQuery Migration Service 簡介

本文將概述 BigQuery 遷移服務。

BigQuery Migration Service 是一套全方位解決方案，可將資料倉儲遷移至 BigQuery。這項服務提供多項功能，可協助您完成遷移作業的每個階段，包括評估和規劃、[各種 SQL 方言](https://docs.cloud.google.com/bigquery/docs/interactive-sql-translator?hl=zh-tw#supported_sql_dialects)的 SQL 轉譯、資料移轉和資料驗證。這些服務可協助您加快遷移作業、降低風險，並縮短創造價值所需的時間。

BigQuery Migration Service 包含下列功能：

* **BigQuery 遷移評估**：執行 [BigQuery 遷移評估](https://docs.cloud.google.com/bigquery/docs/migration-assessment?hl=zh-tw)，評估及規劃資料倉儲遷移作業。
* **SQL 翻譯服務**：這項服務可自動將 SQL 查詢轉換為 GoogleSQL，包括 Gemini 強化版 SQL 自訂功能。您可以透過[批次 SQL 翻譯器](https://docs.cloud.google.com/bigquery/docs/batch-sql-translator?hl=zh-tw)大量遷移 SQL 指令碼，也可以使用[互動式 SQL 翻譯器](https://docs.cloud.google.com/bigquery/docs/interactive-sql-translator?hl=zh-tw)翻譯個別查詢。您也可以使用 [SQL 翻譯 API](https://docs.cloud.google.com/bigquery/docs/api-sql-translator?hl=zh-tw)，將工作負載遷移至 BigQuery。
* **BigQuery 資料移轉服務**：設定資料移轉作業，將資料從資料來源載入 BigQuery。詳情請參閱「[什麼是 BigQuery 資料移轉服務？](https://docs.cloud.google.com/bigquery/docs/dts-introduction?hl=zh-tw)」一文。

您也可以使用下列開放原始碼工具，協助完成遷移程序：

* **資料遷移工具**：使用[資料遷移工具](https://github.com/GoogleCloudPlatform/data-migration-tool)，自動將資料倉儲遷移至 BigQuery。這項工具會使用 BigQuery 資料移轉服務、BigQuery 翻譯服務和資料驗證工具，轉移資料、翻譯及驗證 DDL、DML 和 SQL 查詢。
* **資料驗證工具**：將資料遷移至 BigQuery 後，請執行[資料驗證工具](https://github.com/GoogleCloudPlatform/professional-services-data-validator)，確認來源和目的地資料表相符。
* **BigQuery 權限對應工具**：使用[權限對應工具](https://github.com/GoogleCloudPlatform/professional-services-bigquery-permission-mapper)，自動建立及維護使用者可修改的權限對應。您可以使用權限對應工具分析及調解重複的權限和使用者群組，同時產生錯誤報告。這項工具會輸出 JSON 和 Terraform 指令碼，用於建立 BigQuery 群組、使用者和繫結。
* **Managed Service for Apache Airflow 範本**：使用 [Managed Service for Apache Airflow 範本](https://github.com/GoogleCloudPlatform/professional-services-composer-templates)，簡化建立新 Airflow DAG 的程序，或將現有的自動化調度管理工作從地端部署遷移至雲端。
* **Cloud Foundation Fabric**：查看 [Terraform 範例和模組，適用於Google Cloud](https://github.com/GoogleCloudPlatform/cloud-foundation-fabric)，包括全機構適用的到達區域藍圖、網路模式和產品功能的參考藍圖，以及可調整的模組庫。

## 配額

配額和限制適用於工作數量和檔案大小。如要進一步瞭解移轉服務配額和限制，請參閱[配額和限制](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#migration-api-limits)。

## 定價

使用 BigQuery Migration API 無須付費。不過，輸入和輸出檔案所用的儲存空間仍須支付一般費用。詳情請參閱[儲存空間價格](https://cloud.google.com/bigquery/pricing?hl=zh-tw#storage)。

此外，您可以使用 [Google Cloud Migration Center 的成本估算功能](https://docs.cloud.google.com/migration-center/docs/migration-center-overview?hl=zh-tw)，產生遷移至 BigQuery 的資料倉儲設定執行成本估算。詳情請參閱「[開始估算費用](https://docs.cloud.google.com/migration-center/docs/estimate/start-estimation?hl=zh-tw)」和「[指定資料倉儲需求](https://docs.cloud.google.com/migration-center/docs/estimate/specify-datawarehouse-requirements?hl=zh-tw)」。

## 後續步驟

* 如要進一步瞭解如何使用 BigQuery Migration Service MCP 伺服器，請參閱「[瞭解如何使用 BigQuery Migration Service MCP 伺服器](https://docs.cloud.google.com/bigquery/docs/use-bigquery-migration-mcp?hl=zh-tw)」。
* 如要進一步瞭解批次 SQL 翻譯器，請參閱[批次 SQL 翻譯器](https://docs.cloud.google.com/bigquery/docs/batch-sql-translator?hl=zh-tw)。
* 如要進一步瞭解如何使用互動式 SQL 翻譯器，請參閱[互動式 SQL 翻譯器](https://docs.cloud.google.com/bigquery/docs/interactive-sql-translator?hl=zh-tw)。
* 如要進一步瞭解 BigQuery 遷移評估，請參閱「[BigQuery 遷移評估](https://docs.cloud.google.com/bigquery/docs/migration-assessment?hl=zh-tw)」一文。
* 瞭解[資料驗證工具](https://github.com/GoogleCloudPlatform/professional-services-data-validator#data-validation-tool)。
* 如要瞭解 BigQuery Migration Service 的配額和限制，請參閱「[配額和限制](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#migration-api-limits)」。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-06 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-06 (世界標準時間)。"],[],[]]