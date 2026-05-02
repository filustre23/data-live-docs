* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# BigQuery 實體解析架構簡介

本文說明 BigQuery 實體解析架構的架構。實體解析功能會比對共用資料中的記錄，即使沒有通用 ID，也能比對成功，或是使用 Google Cloud 合作夥伴的身分識別服務擴增共用資料。

這份文件適用於實體解析服務使用者和身分識別提供者。如需實作詳細資料，請參閱「[在 BigQuery 中設定及使用實體解析](https://docs.cloud.google.com/bigquery/docs/entity-resolution-setup?hl=zh-tw)」。

您可以在將資料提供給[資料無塵室](https://docs.cloud.google.com/bigquery/docs/data-clean-rooms?hl=zh-tw)之前，使用 BigQuery 實體解析功能準備資料。實體解析功能適用於以量計價和容量計費模式，以及所有 BigQuery 版本。

## 優點

實體解析功能可為使用者帶來下列好處：

* 就地解決實體問題，無須支付資料移轉費用。訂閱者或Google Cloud 合作夥伴會將您的資料與身分識別資料表比對，並將比對結果寫入您專案中的資料集。 Google Cloud
* 避免管理擷取、轉換及載入 (ETL) 工作。

實體解析可為身分識別資訊提供者帶來下列好處：

* 在 [Google Cloud Marketplace](https://docs.cloud.google.com/marketplace/docs/partners/integrated-saas?hl=zh-tw) 上，以代管軟體即服務 (SaaS) 產品的形式提供實體解析服務。
* 使用專屬身分識別圖表和比對邏輯，但不會向使用者揭露。

## 架構

BigQuery 會使用遠端函式呼叫實作實體解析，在身分識別提供者的環境中啟動實體解析程序。系統不會在過程中複製或轉移資料。
下圖和說明描述了實體解析工作流程：

1. 使用者授予身分提供者的服務帳戶輸入資料集的讀取權限，以及輸出資料集的寫入權限。
2. 使用者會呼叫遠端函式，將輸入資料與供應商的身分識別圖表資料比對。遠端函式會將相符的參數傳遞給供應商。
3. 供應商的服務帳戶會讀取及處理輸入資料集。
4. 供應商的服務帳戶會將實體解析結果寫入使用者的輸出資料集。

以下各節說明使用者元件和供應商專案。

### 使用者元件

使用者端元件包括：

* **遠端函式呼叫**：呼叫由身分識別提供者定義及實作的程序。這項呼叫會啟動實體解析程序。
* **輸入資料集**：包含要比對資料的來源資料集。視需要，資料集可以包含具有額外參數的中繼資料表。供應商會指定輸入資料集的結構定義需求。
* **輸出資料集**：供應商將比對結果儲存為輸出資料表的目標資料集。供應商可以視需要將包含實體解析工作詳細資料的工作狀態表寫入這個資料集。輸出資料集可以與輸入資料集相同。

### 識別資訊提供者元件

識別資訊提供者元件包括：

* **控制平面**：包含[BigQuery 遠端函式](https://docs.cloud.google.com/bigquery/docs/remote-functions?hl=zh-tw)，可協調比對程序。這項函式可以實作為 [Cloud Run](https://docs.cloud.google.com/run/docs/overview/what-is-cloud-run?hl=zh-tw) 工作或 [Cloud Run 函式](https://docs.cloud.google.com/functions/docs/concepts/overview?hl=zh-tw)。控制層也可能包含其他服務，例如驗證和授權。
* **資料平面**：包含身分識別圖表資料集，以及實作供應商比對邏輯的預存程序。預存程序可以實作為 [SQL 預存程序](https://docs.cloud.google.com/bigquery/docs/procedures?hl=zh-tw)或 [Apache Spark 預存程序](https://docs.cloud.google.com/bigquery/docs/spark-procedures?hl=zh-tw)。身分識別圖表資料集包含與使用者資料比對的資料表。

**注意：** 身分圖表也可以儲存在某些外部資料庫。

## 後續步驟

* 瞭解如何[設定及使用實體解析](https://docs.cloud.google.com/bigquery/docs/entity-resolution-setup?hl=zh-tw)。
* 瞭解[遠端函式](https://docs.cloud.google.com/bigquery/docs/remote-functions?hl=zh-tw)。
* 瞭解[預存程序](https://docs.cloud.google.com/bigquery/docs/procedures?hl=zh-tw)。
* 瞭解[資料無塵室](https://docs.cloud.google.com/bigquery/docs/data-clean-rooms?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-02 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-02 (世界標準時間)。"],[],[]]