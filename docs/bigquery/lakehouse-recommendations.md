自 2026 年 4 月 20 日起，BigLake 已改名為 Lakehouse。BigLake Metastore 現在稱為 Lakehouse 執行階段目錄。湖倉 API、用戶端程式庫、CLI 指令和 IAM 名稱維持不變，仍會參照 BigLake。

Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [Lakehouse](https://docs.cloud.google.com/lakehouse/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/lakehouse/docs/introduction?hl=zh-tw)

提供意見

# 什麼是無邊界湖倉？ 透過集合功能整理內容 你可以依據偏好儲存及分類內容。

*無邊界湖倉*可讓您結合 Apache Iceberg 開放資料表格式與代管儲存空間，在Google Cloud 上建構開放式資料湖倉。這種架構將儲存空間與運算資源分離，為數據分析和 AI 工作負載提供統一的基礎。

為管理開放式資料表中繼資料，Lakehouse 採用 [*Lakehouse 執行階段目錄*](https://docs.cloud.google.com/lakehouse/docs/about-lakehouse-catalogs?hl=zh-tw)，這項無伺服器中繼資料服務可集中探索，並消除跨存放區同步處理。這項設計可讓多個引擎 (包括 Managed Service for Apache Spark、Apache Flink、Apache Hive、Trino 和 BigQuery) 直接存取單一事實來源，不需複製資料。

## 主要優點

* **無伺服器架構：**Google Cloud 的 Lakehouse 可免除伺服器或叢集管理工具需求，降低營運負擔，並根據需求自動調度資源。針對運算工作負載，無伺服器批次和互動式工作階段可消除工作之間的資源爭用，並自動維護基礎架構。
* **讀寫互通性：**開放原始碼引擎和 BigQuery 可讀寫相同的 Apache Iceberg 資料表 (BigQuery 寫入功能為[預先發布版](https://cloud.google.com/products?hl=zh-tw#product-launch-stages))，而選用的[資料表管理](https://docs.cloud.google.com/lakehouse/docs/table-options?hl=zh-tw#enable-table-management) ([預先發布版](https://cloud.google.com/products?hl=zh-tw#product-launch-stages)) 可自動執行壓縮、快照到期和垃圾收集。
* **整合式資料管理和治理：**與 [Knowledge Catalog](https://docs.cloud.google.com/knowledge-catalog/docs/introduction?hl=zh-tw) 整合，可集中定義及強制執行多個引擎的治理政策，並提供語意搜尋、資料歷程和品質檢查功能。
* **儲存空間擴充功能：**Google Cloud 的 Lakehouse 擴充 Cloud Storage 管理功能，納入 Autoclass 分級和客戶自行管理的加密金鑰 (CMEK) 等功能。
* **全代管體驗：**Google Cloud 的 Lakehouse 與 BigQuery 整合，提供全代管的數據分析和 AI 體驗。
* **高可用性和災難復原：**Google Cloud 的 Lakehouse 提供跨區域複製和災難復原 ([預先發布版](https://docs.cloud.google.com/lakehouse/docs/about-managed-disaster-recovery?hl=zh-tw)) 選項，可支援資料的高可用性。

## 用途

* **開放式湖倉：**使用 Cloud Storage 做為儲存層，並透過 Google Cloud 的 Lakehouse 管理及控管 Apache Iceberg 資料。
* **整合分析和交易：**直接在 AlloyDB for PostgreSQL ([預先發布版](https://docs.cloud.google.com/alloydb/docs/access-real-time-data-overview?hl=zh-tw)) 中存取分析 Apache Iceberg 資料表，將分析資料與交易工作負載結合。
* **統一存取：**讓不同引擎 (Apache Spark、Apache Flink、BigQuery) 與具有一致中繼資料的相同 Apache Iceberg 資料表互動。
* **跨雲端數據分析和 AI：**[存取 Databricks Unity Catalog、AWS Glue Data Catalog、Snowflake Horizon Catalog、Workday Data Lake 和 SAP Business Data Cloud (SAP BDC) 中的跨雲端資料](https://docs.cloud.google.com/lakehouse/docs/about-cross-cloud-data-access?hl=zh-tw)。聯合目錄會同步處理這些供應商的中繼資料，讓您使用 BigQuery 或開放原始碼引擎查詢資料，無須遷移。
* **探索公開資料集：**透過 Apache Iceberg REST 目錄端點查詢[公開資料集](https://docs.cloud.google.com/lakehouse/docs/public-datasets?hl=zh-tw)，不必管理基礎架構。
* **Hive metastore：**使用 [Apache Hive 目錄端點](https://docs.cloud.google.com/lakehouse/docs/about-spark-hive-metastore?hl=zh-tw)，將 Apache Spark 和 Apache Hive 等開放原始碼引擎連結至 Lakehouse 執行階段目錄。這樣一來，您就不必維護自行託管的 Hive metastore (HMS)，可省去作業負擔，同時直接在 BigQuery 中共用資料及查詢資料表。
* **Metastore 現代化：**[將中繼資料從 Dataproc Metastore](https://docs.cloud.google.com/lakehouse/docs/migrate-dataproc-metastore?hl=zh-tw) 或其他外部 metastore 遷移至 Lakehouse 執行階段目錄，不需複製資料檔案。

## 介面和工具

您可以使用下列工具，與 Google Cloud 的 Lakehouse 資源互動：

* **Google Cloud 控制台**：使用控制台建立目錄、查看目錄屬性、查看稽核記錄，以及設定權限。
* **BigQuery SQL：**使用 GoogleSQL 查詢 Lakehouse 執行階段目錄中的 Apache Iceberg 資料表和外部資料表，並使用 DDL 和 DML ([預先發布版](https://cloud.google.com/products?hl=zh-tw#product-launch-stages)) 建立及修改 Lakehouse 執行階段目錄中的 Apache Iceberg 資料表。
* **Google Cloud CLI、REST API 和 Terraform：**透過程式輔助方式建立及管理目錄、命名空間、資料表和存取權政策。
* **開放原始碼引擎：**使用 Apache Spark、Apache Flink、Trino 和 Apache Hive 等引擎，搭配 Lakehouse 執行階段目錄讀取及寫入資料。
* **IDE 和筆記本：**使用互動式 Apache Spark 筆記本和 IDE 擴充功能 (例如 VS Code 的 Data Agent Kit (DAK) 擴充功能)，直接在開發環境中驗證 Google Cloud、以互動方式編寫程式碼，以及管理筆記本工作階段。
* **自動化調度管理和 MLOps 工具：**使用 Managed Service for Apache Airflow (原為 Cloud Composer) 和 Vertex AI 中的 Kubeflow Pipelines，將無伺服器批次管道和目錄作業與自動化調度管理工作流程整合。
* **Apache Iceberg REST Catalog API：**使用 Apache Iceberg REST 目錄端點，透過與開放式 Apache Iceberg REST 規格相容的工具與服務互動。
* **支援 Apache Iceberg 資料表：**支援 Apache Iceberg V2 資料表 (正式發布版) 和 V3 資料表 (預先發布版)。不支援 Iceberg V1 資料表。

## 後續步驟

* 瞭解 [Google Cloud 無邊界湖倉](https://docs.cloud.google.com/lakehouse/docs/lakehouse-basics?hl=zh-tw)的架構。
* 請參閱「[重要概念](https://docs.cloud.google.com/lakehouse/docs/key-concepts?hl=zh-tw)」一節，瞭解相關術語。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-11-09 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-11-09 (世界標準時間)。"],[],[]]