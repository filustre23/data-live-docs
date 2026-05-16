自 2026 年 4 月 20 日起，BigLake 將改名為 Lakehouse for Apache Iceberg。BigLake metastore 現在稱為 Lakehouse 執行階段目錄。湖倉 API、用戶端程式庫、CLI 指令和 IAM 名稱維持不變，仍會參照 BigLake。

Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [Lakehouse](https://docs.cloud.google.com/lakehouse/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/lakehouse/docs/introduction?hl=zh-tw)

提供意見

# 什麼是 Lakehouse for Apache Iceberg？ 透過集合功能整理內容 你可以依據偏好儲存及分類內容。

*Lakehouse for Apache Iceberg* 是一種高效能儲存引擎，專為建構開放式資料湖倉而設計。透過整合 Apache Iceberg 開放資料表格式與 Google Cloud上的全代管企業級儲存空間，提供進階數據分析和 AI 的統一介面。

Google Cloud 的*Lakehouse*可將儲存空間與運算資源區隔開來，確保分析和交易系統之間順暢互通。這個架構可讓多個引擎 (包括 Apache Spark、Apache Flink、Apache Hive、Trino 和 BigQuery) 存取單一的事實來源，消除資料重複問題，並確保洞察資料一致。

## 主要優點

* **無伺服器架構：**Google Cloud 的 Lakehouse 可免除伺服器或叢集管理作業，減少作業負擔，並根據需求自動調度資源。
* **統一資料管理和治理：**與 [Knowledge Catalog](https://docs.cloud.google.com/dataplex/docs/introduction?hl=zh-tw) 整合，確保在多個引擎中集中定義及強制執行治理政策，並提供語意搜尋、資料歷程和品質檢查功能。
* **儲存空間擴充功能：**Google Cloud 的 Lakehouse 擴充了 Cloud Storage 管理功能，納入自動調整級別分層和客戶自行管理的加密金鑰 (CMEK) 等功能。
* **全代管體驗：**與 BigQuery 整合後，Google Cloud 的 Lakehouse 會使用高輸送量串流和即時中繼資料管理，提供全代管串流、數據分析和 AI 體驗。
* **高可用性和災難復原：**Google Cloud 的 Lakehouse 提供跨區域複製和災難復原 ([搶先版](https://docs.cloud.google.com/lakehouse/docs/about-managed-disaster-recovery?hl=zh-tw)) 選項，支援資料高可用性。

## 用途

* **開放式湖倉：**將 Cloud Storage 做為儲存層，並透過 Google Cloud 的 Lakehouse 介面管理及控管 Apache Iceberg 資料。
* **分析和交易整合：**直接在 AlloyDB for PostgreSQL ([預先發布版](https://docs.cloud.google.com/alloydb/docs/bigquery-view-alloydb-overview?hl=zh-tw)) 中存取分析 Apache Iceberg 資料表，將分析資料與交易工作負載合併。
* **統一存取：**讓不同引擎 (Apache Spark、Apache Flink、BigQuery) 與相同的 Apache Iceberg 資料表互動，並使用一致的中繼資料。
* **跨雲端分析和 AI：**使用 Cross-cloud Lakehouse ([搶先版](https://docs.cloud.google.com/lakehouse/docs/about-cross-cloud-lakehouse?hl=zh-tw)) 直接從 Google Cloud 查詢其他雲端供應商的資料，不必遷移資料。
* **探索公開資料集：**使用 Apache Iceberg REST 目錄端點輕鬆查詢高品質公開資料集，不必管理基礎架構。

## 目錄介面

*Lakehouse 執行階段目錄*是單一中繼資料服務，提供多個介面 (端點)，可連結 Cloud Storage 和 BigQuery 中的資料。

* **Apache Iceberg REST 目錄端點：**提供標準 [REST 介面](https://iceberg.apache.org/rest-catalog-spec/)，可廣泛相容於 Apache Spark、Apache Flink 和 Trino 等開放原始碼引擎。建議您使用這個介面處理新的工作負載，並提供完整的讀取/寫入互通性。

  **提示：** 請參閱快速入門指南「[使用 Lakehouse 執行階段目錄搭配 Apache Spark 和 BigQuery，並透過 Apache Iceberg REST 目錄端點](https://docs.cloud.google.com/lakehouse/docs/use-lakehouse-metastore-iceberg-rest-catalog?hl=zh-tw)」。
* **BigQuery 端點的自訂 Apache Iceberg 目錄：**可讓引擎直接與 BigQuery 目錄互通。這個介面主要用於 *BigQuery 管理的 Apache Iceberg 資料表*，以及遷移至 Google Cloud 的 Lakehouse 架構的現有工作負載。

## 介面和工具

您可以使用下列工具與 Google Cloud 的 Lakehouse 資源互動：

* **Google Cloud 控制台**：使用控制台建立目錄、查看目錄屬性、查看稽核記錄，以及設定權限。
* **BigQuery SQL：**使用標準 SQL DDL (資料定義語言) 建立及管理與 Lakehouse 執行階段目錄整合的 Apache Iceberg 資料表和外部資料表。
* **開放原始碼引擎：**搭配使用 Apache Spark、Apache Flink 和 Apache Hive 等引擎與 Lakehouse 執行階段目錄，即可讀取及寫入資料。
* **Lakehouse 執行階段目錄 API：**使用 Apache Iceberg REST 目錄端點，透過與開放式 Apache Iceberg REST 規格相容的工具與服務互動。

## 後續步驟

* 瞭解 [Google Cloud 的 Lakehouse](https://docs.cloud.google.com/lakehouse/docs/lakehouse-basics?hl=zh-tw) 架構。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-16 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-16 (世界標準時間)。"],[],[]]