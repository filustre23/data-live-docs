* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 工作階段簡介

本指南說明如何啟用、建立及追蹤 BigQuery 工作階段中的變更。本文適用於熟悉 [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw) 和 [GoogleSQL](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw) 的使用者。

您可以在 BigQuery 工作階段中擷取 SQL 活動。您可以在整個工作階段中使用臨時資料表、臨時函式和變數，以互動方式建構一或多個查詢。你可以同時進行多個工作階段，並儲存每個工作階段的記錄。工作階段終止後，您最多可以在 20 天內查看工作階段記錄。

工作階段的常見用途包括：

* **維護暫時性工作階段資料。**定義變數和臨時資料表一次，即可在整個工作階段中使用。
* **依工作階段查詢記錄。**如要追蹤工作階段期間特定時間發生的行為，可以查看工作階段期間的變更記錄。
* **透過多個查詢建立多陳述式交易。**在工作階段中，您可以開始交易、進行變更，並查看暫時結果，然後再決定要提交或回溯。您可以在工作階段中透過多個查詢執行這項操作。如果您未使用工作階段，則必須在單一查詢中完成多重陳述式交易。

## 定價

* 使用工作階段不會產生額外費用。
* 對於使用以量計價方案的專案，對 `INFORMATION_SCHEMA` 執行查詢時，會產生費用。詳情請參閱[`INFORMATION_SCHEMA`定價](https://docs.cloud.google.com/bigquery/docs/information-schema-intro?hl=zh-tw#pricing)。
* 您在工作階段中建立的臨時資料表會計費。儲存空間費用取決於資料表中儲存的資料量。如需儲存空間價格的相關資訊，請參閱[儲存空間定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#storage)一文。

## 限制

* 工作階段中的每項查詢都會在工作階段建立的位置執行。如果未指定位置，或無法從建立工作階段的查詢推斷位置，工作階段會在[預設位置](https://docs.cloud.google.com/bigquery/docs/default-configuration?hl=zh-tw#global-settings)建立。
* 如果閒置 24 小時，工作階段就會自動終止。
* 工作階段會在建立 7 天後自動終止。
* 工作階段變數的大小上限為 1 MB，而工作階段中使用的所有變數的總和上限為 10 MB。
* 工作階段內不得進行並行查詢。

## 角色和權限

本節說明執行工作階段動作所需的 [Identity and Access Management (IAM) 權限](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bq-permissions)和 [IAM 角色](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery)。

| 動作 | 所需權限 | 預設角色 |
| --- | --- | --- |
| 建立新工作階段。 使用您建立的現有工作階段。 | `bigquery.jobs.create` | `bigquery.user`  `bigquery.Jobuser`  `bigquery.admin` |
| 終止你建立的工作階段。 | `bigquery.jobs.create` | `bigquery.user`  `bigquery.Jobuser`  `bigquery.admin` |
| 終止其他使用者建立的工作階段。 | `bigquery.jobs.create`  `bigquery.jobs.update` | `bigquery.admin` |
| 查看專案中的工作階段清單。 這份清單包含您在專案中透過 `INFORMATION_SCHEMA.JOBS_BY_USER` 建立的 ID。 | `bigquery.jobs.list` | `bigquery.user`  `bigquery.Jobuser`  `bigquery.admin` |
| 查看專案中所有使用者的所有工作階段。 這份清單包含專案中以 `INFORMATION_SCHEMA.JOBS` 建立的所有工作階段 ID。 | `bigquery.jobs.listAll` | `bigquery.admin` |
| 查看目前專案中，由目前使用者建立的工作階段的中繼資料 (使用 `INFORMATION_SCHEMA.SESSIONS_BY_USER`)。 | `bigquery.jobs.list` | `bigquery.user`  `bigquery.Jobuser`  `bigquery.admin` |
| 使用 `INFORMATION_SCHEMA.SESSIONS_BY_PROJECT` 查看目前專案中所有工作階段的中繼資料。 | `bigquery.jobs.listAll` | `bigquery.admin` |

## 後續步驟

* 進一步瞭解如何[在工作階段中撰寫查詢](https://docs.cloud.google.com/bigquery/docs/sessions-write-queries?hl=zh-tw)。
* 進一步瞭解如何[處理工作階段](https://docs.cloud.google.com/bigquery/docs/sessions?hl=zh-tw)，包括如何建立、使用、終止及列出工作階段。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-04-30 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-04-30 (世界標準時間)。"],[],[]]