Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# BigQuery 實體解析架構簡介

BigQuery 實體解析功能可讓您比對共用資料集中的記錄，即使這些資料集缺少通用 ID 也能比對。您也可以使用 Google Cloud 合作夥伴的身分識別提供者，透過其他屬性擴充共用資料。舉例來說，您可以連結不同資料集中的顧客記錄，建立統一的顧客個人資料、偵測金融詐欺或分析供應鏈。

將資料提供給[資料無塵室](https://docs.cloud.google.com/bigquery/docs/data-clean-rooms?hl=zh-tw)前，您可以先使用實體解析功能準備及比對記錄。實體解析功能適用於所有 BigQuery 版本，並支援以量計價和容量計費模式。如要進一步瞭解如何實作，請參閱「[在 BigQuery 中設定及使用實體解析](https://docs.cloud.google.com/bigquery/docs/entity-resolution-setup?hl=zh-tw)」。

## 實體解析的優點

實體解析可為使用者和身分識別提供者帶來營運和資料共用的優勢。

### 使用者優勢

在 BigQuery 中解析實體後，您可享有下列使用者福利：

* **就地解析**：您可以在原地解析實體，不必支付資料傳輸費用。身分識別提供者會將您的資料與身分識別圖譜比對，並將實體解析結果寫入您 Google Cloud 專案中的資料集。
* **簡化作業**：您不必管理擷取、轉換和載入 (ETL) 管道或自訂資料複製工作流程。

### 識別資訊提供者優點

在 BigQuery 中提供身分識別服務時，您可享有下列身分識別提供者優勢：

* **Marketplace 整合**：您可以在 [Google Cloud Marketplace](https://docs.cloud.google.com/marketplace/docs/partners/integrated-saas?hl=zh-tw) 上，以代管軟體即服務 (SaaS) 產品的形式提供實體解析服務。
* **智慧財產權保護**：您可以使用專屬的身分圖表和比對邏輯，但不會向使用者揭露這些內容。這項架構有助於保護您的智慧財產。

## 實體解析架構

BigQuery 會呼叫遠端函式，在身分識別提供者的環境中執行比對程序，藉此實作實體解析。BigQuery 不會在過程中複製或移動資料。

下圖說明使用者 Google Cloud 專案與身分提供者 Google Cloud 專案之間的實體解析工作流程：

實體解析工作流程包含下列步驟：

1. 您授予身分識別提供者的服務帳戶輸入資料集的讀取權限，以及輸出資料集的寫入權限。
2. 您會呼叫遠端函式，將輸入資料與身分識別供應商的身分識別圖表資料進行比對。遠端函式會將相符參數傳遞至身分識別提供者。
3. 身分識別資訊提供者的服務帳戶會讀取及處理輸入資料集。
4. 身分識別提供者的服務帳戶會將實體解析結果寫入輸出資料集。

如要執行這項工作流程，實體解析作業必須仰賴您環境和身分識別提供者環境中的元件。

### 使用者元件

您的 Google Cloud 專案包含下列使用者元件：

* **遠端函式呼叫**：執行身分識別提供者定義及實作程序的呼叫。這項呼叫會啟動實體解析程序。
* **輸入資料集**：包含您要比對資料的來源資料集。輸入資料集可以視需要包含中繼資料表，並提供額外參數。識別資訊提供者會指定輸入資料集的結構定義需求。
* **輸出資料集**：身分識別提供者會將比對結果寫入這個目的地資料集，做為輸出資料表。身分識別提供者也可以選擇將工作詳細資料寫入這個資料集的工作狀態表。輸出資料集可以與輸入資料集相同。

### 識別資訊提供者元件

身分識別提供者的環境包含下列元件：

* **控制層**：包含[BigQuery 遠端函式](https://docs.cloud.google.com/bigquery/docs/remote-functions?hl=zh-tw)，可協調比對程序。身分識別提供者可以將這項函式實作為 [Cloud Run](https://docs.cloud.google.com/run/docs/overview/what-is-cloud-run?hl=zh-tw) 工作或 [Cloud Run 函式](https://docs.cloud.google.com/functions/docs/concepts/overview?hl=zh-tw)。控制平面也可以包含驗證和授權服務。
* **資料平面**：包含身分識別圖表資料集和執行比對邏輯的預存程序。身分圖表是已知實體 ID 和屬性的參考資料庫。身分識別提供者可以將預存程序實作為 [SQL 預存程序](https://docs.cloud.google.com/bigquery/docs/procedures?hl=zh-tw)或 [Apache Spark 預存程序](https://docs.cloud.google.com/bigquery/docs/spark-procedures?hl=zh-tw)。身分圖表資料集包含身分提供者用來比對您資料的資料表。

## 注意事項

規劃實體解析部署作業時，請考量下列因素：

* **與身分識別提供者協調**：執行比對作業前，您必須與支援的身分識別提供者協調，取得他們的服務帳戶憑證和遠端函式簽章。
* **外部資料庫**：身分識別提供者通常會在 BigQuery 中代管身分識別圖表，但也可以將身分識別圖表儲存在外部資料庫中。

## 後續步驟

* 瞭解如何[設定及使用實體解析](https://docs.cloud.google.com/bigquery/docs/entity-resolution-setup?hl=zh-tw)。
* 瞭解如何[使用遠端函式](https://docs.cloud.google.com/bigquery/docs/remote-functions?hl=zh-tw)。
* 瞭解如何[使用 SQL 預存程序](https://docs.cloud.google.com/bigquery/docs/procedures?hl=zh-tw)。
* 瞭解如何[透過資料無塵室共用機密資料](https://docs.cloud.google.com/bigquery/docs/data-clean-rooms?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-10-20 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-10-20 (世界標準時間)。"],[],[]]