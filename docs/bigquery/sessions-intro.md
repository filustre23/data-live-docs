Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 工作階段簡介

BigQuery 工作階段可讓您擷取 SQL 活動，並在多個查詢之間維持狀態。在工作階段中，您可以定義臨時資料表、臨時函式和變數，並在以互動方式建構查詢或執行多陳述式交易時重複使用。

多個工作階段可以同時處於啟用狀態，BigQuery 會在工作階段結束後，將每個工作階段的記錄儲存最多 20 天。使用工作階段前，請務必熟悉 [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw) 和 [GoogleSQL](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw)。

## 用途

工作階段的常見用途包括：

* **維護暫時性工作階段資料。**定義變數和臨時資料表一次，即可在整個工作階段中使用。
* **依工作階段查詢歷史記錄。**如要追蹤工作階段中特定時間發生的行為，可以查看工作階段期間的變更記錄。
* **建立多陳述式交易，涵蓋多個查詢。**在工作階段中，您可以開始交易、進行變更及查看暫時結果，再決定要提交或復原。您可以在工作階段中透過多個查詢完成這項操作。如果不使用工作階段，則必須在單一查詢中完成多陳述式交易。

## 定價

* 使用工作階段不會產生額外費用。
* 如果專案採用隨選定價模式，對 `INFORMATION_SCHEMA` 執行查詢會產生費用。詳情請參閱 [`INFORMATION_SCHEMA` 定價](https://docs.cloud.google.com/bigquery/docs/information-schema-intro?hl=zh-tw#pricing)。
* 在工作階段中建立暫存資料表會產生費用。儲存費用取決於資料表中儲存的資料量。如要瞭解儲存空間定價，請參閱「[儲存空間定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#storage)」。

## 限制

* 工作階段中的每項查詢都會在工作階段建立的位置執行。如果未指定位置，或無法從建立工作階段的查詢推斷位置，系統會在[預設位置](https://docs.cloud.google.com/bigquery/docs/default-configuration?hl=zh-tw#global-settings)建立工作階段。
* 閒置 24 小時後，工作階段會自動終止。
* 工作階段會在建立 7 天後自動終止。
* 工作階段變數的大小上限為 1 MB，工作階段中使用的所有變數大小上限為 10 MB。
* 工作階段內不得同時執行多項查詢。

## 角色和權限

本節說明對工作階段執行動作時，所需的 [Identity and Access Management (IAM) 權限](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bq-permissions)和 [IAM 角色](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery)。

| 動作 | 所需權限 | 預設角色 |
| --- | --- | --- |
| 建立新的工作階段。 使用您建立的現有工作階段。 | `bigquery.jobs.create` | `bigquery.user`  `bigquery.Jobuser`  `bigquery.admin` |
| 終止您建立的工作階段。 | `bigquery.jobs.create` | `bigquery.user`  `bigquery.Jobuser`  `bigquery.admin` |
| 終止其他使用者建立的工作階段。 | `bigquery.jobs.create`  `bigquery.jobs.update` | `bigquery.admin` |
| 查看專案中的工作階段清單。 這份清單包含您在專案中使用 `INFORMATION_SCHEMA.JOBS_BY_USER` 建立的工作階段 ID。 | `bigquery.jobs.list` | `bigquery.user`  `bigquery.Jobuser`  `bigquery.admin` |
| 查看專案中所有使用者的所有工作階段。 這份清單包含在專案中以 `INFORMATION_SCHEMA.JOBS` 建立的所有工作階段 ID。 | `bigquery.jobs.listAll` | `bigquery.admin` |
| 使用 `INFORMATION_SCHEMA.SESSIONS_BY_USER`，查看目前使用者在目前專案中建立的工作階段中繼資料。 | `bigquery.jobs.list` | `bigquery.user`  `bigquery.Jobuser`  `bigquery.admin` |
| 使用 `INFORMATION_SCHEMA.SESSIONS_BY_PROJECT` 查看目前專案中所有工作階段的中繼資料。 | `bigquery.jobs.listAll` | `bigquery.admin` |

## 後續步驟

* 進一步瞭解如何[在工作階段中編寫查詢](https://docs.cloud.google.com/bigquery/docs/sessions-write-queries?hl=zh-tw)。
* 進一步瞭解如何[使用工作階段](https://docs.cloud.google.com/bigquery/docs/sessions?hl=zh-tw)，包括如何建立、使用、終止及列出工作階段。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-11-08 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-11-08 (世界標準時間)。"],[],[]]