Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 基本角色和權限

BigQuery 支援將 IAM [基本角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#basic)用於專案層級存取權。

**注意：** 請避免使用基本角色。這些角色早於 IAM，且授予的存取權過多且不平均。請改用[預先定義的 IAM](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw) 角色。

## 專案的基本角色

根據預設，將存取權授予專案的同時，也會將存取權授予該專案中的資料集。您可以覆寫每個資料集的預設存取權。下表說明基本 IAM 角色成員可獲得的存取權。

| 基本角色 | 功能 |
| --- | --- |
| `Viewer` | * 可以在專案中啟動工作。不同的工作類型可能還需要其他資料集角色。 * 可以列出和取得所有工作，並更新角色在專案中啟動的工作。 * 如果您在含有任何檢視者的專案中建立資料集，則 BigQuery 會將新資料集中預先定義的 [bigquery.dataViewer](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.dataViewer) 角色授予那些使用者。 |
| `Editor` | * 和 `Viewer` 擁有相同權限，另外：   + 可在專案內中建立新資料集   + 如果您在含有任何編輯者的專案中建立資料集，則 BigQuery 會將新資料集中預先定義的 [bigquery.dataEditor](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.dataEditor) 角色授予那些使用者。 |
| `Owner` | * 和 `Editor` 擁有相同權限，另外：   + 可撤銷或變更任何專案角色   + 列出專案內的所有資料集   + 可刪除專案中的任何資料集   + 可列出和取得在專案中執行的所有工作，包括其他專案使用者執行的工作。   + 如果您建立資料集，BigQuery 會將新資料集中預先定義的 [bigquery.dataOwner](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.dataOwner) 角色授予所有專案擁有者。  **例外狀況：**使用者執行查詢時，系統會建立[匿名資料集](https://docs.cloud.google.com/bigquery/docs/cached-results?hl=zh-tw#how_cached_results_are_stored)，以儲存快取結果資料表。只有執行該項查詢的使用者具有匿名資料集時的 `OWNER` 存取權。  請勿將`OWNER`基本角色與 [BigQuery 管理員](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.admin) (`roles/bigquery.admin`) IAM 角色混淆。BigQuery 管理員提供許多權限，這些權限並未授予`OWNER`基本角色。如果您要授予 BigQuery 專案層級存取權，請使用 IAM 角色，而非基本角色。 |

您可透過[Google Cloud 控制台](https://console.cloud.google.com/?hl=zh-tw)授予或撤銷專案的基本角色。建立專案時，系統會將 `Owner` 角色授予建立該專案的使用者。

如要進一步瞭解如何授予或撤銷專案角色的存取權，請參閱 IAM 說明文件中的[授予、變更及撤銷資源的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)一文。

## 資料集的基本角色

以下是適用於資料集層級的基本角色。

| 資料集角色 | 功能 |
| --- | --- |
| `READER` | * 可以讀取、查詢、複製或匯出資料集裡的資料表。可以讀取資料集裡的處理常式   + 可以對資料集呼叫 [get](https://docs.cloud.google.com/bigquery/docs/reference/v2/datasets/get?hl=zh-tw)   + 可以對資料集裡的資料表呼叫 [get](https://docs.cloud.google.com/bigquery/docs/reference/v2/tables/get?hl=zh-tw) 和 [list](https://docs.cloud.google.com/bigquery/docs/reference/v2/tables/list?hl=zh-tw)   + 可以對資料集裡的處理常式呼叫 [get](https://docs.cloud.google.com/bigquery/docs/reference/v2/routines/get?hl=zh-tw) 和 [list](https://docs.cloud.google.com/bigquery/docs/reference/v2/routines/list?hl=zh-tw)   + 可以對資料集裡資料表的資料呼叫 [list](https://docs.cloud.google.com/bigquery/docs/reference/v2/tabledata/list?hl=zh-tw)  預先定義的 IAM [BigQuery 資料檢視者](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.dataViewer)`roles/bigquery.dataViewer` 角色會對應至 BigQuery 基本角色 `READER`。在資料集層級將 BigQuery 資料檢視者授予主體時，主體會獲得資料集的 `READER`存取權。 |
| `WRITER` | * 和 `READER` 擁有相同權限，另外：   + 可以在資料集裡編輯或附加資料     - 可以對資料表呼叫 [insert](https://docs.cloud.google.com/bigquery/docs/reference/v2/tables/insert?hl=zh-tw)、[insertAll](https://docs.cloud.google.com/bigquery/docs/reference/v2/tabledata/insertAll?hl=zh-tw)、[update](https://docs.cloud.google.com/bigquery/docs/reference/v2/tables/update?hl=zh-tw) 或 [delete](https://docs.cloud.google.com/bigquery/docs/reference/v2/tables/delete?hl=zh-tw)     - 可以將資料集裡的資料表做為載入、複製或查詢工作的目的地     - 可以對處理常式呼叫 [insert](https://docs.cloud.google.com/bigquery/docs/reference/v2/routines/insert?hl=zh-tw)、[update](https://docs.cloud.google.com/bigquery/docs/reference/v2/routines/update?hl=zh-tw) 或 [delete](https://docs.cloud.google.com/bigquery/docs/reference/v2/routines/delete?hl=zh-tw)  預先定義的 IAM [BigQuery 資料編輯者](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.dataEditor)`roles/bigquery.dataEditor` 角色會對應至 `WRITER` BigQuery 基本角色。在資料集層級將 BigQuery 資料編輯者授予主體時，主體會獲得資料集的 `WRITER` 存取權。 |
| `OWNER` | * 和 `WRITER` 擁有相同權限，另外：   + 可以對資料集呼叫 [update](https://docs.cloud.google.com/bigquery/docs/reference/v2/datasets/update?hl=zh-tw)   + 可以對資料集呼叫 [delete](https://docs.cloud.google.com/bigquery/docs/reference/v2/datasets/delete?hl=zh-tw)   資料集必須至少包含一個具備 `OWNER` 角色的實體。擁有 `OWNER` 角色的使用者無法移除自己的 `OWNER` 角色。 預先定義的 IAM [BigQuery 資料擁有者](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.dataOwner) (`roles/bigquery.dataOwner`) 角色會對應至 `OWNER` BigQuery 基本角色。在資料集層級將 BigQuery 資料擁有者角色授予主體時，主體會獲得資料集的 `OWNER` 存取權。 |

如要進一步瞭解如何在資料集層級指派角色，請參閱[控管資料集存取權](https://docs.cloud.google.com/bigquery/docs/dataset-access-controls?hl=zh-tw)。

建立新資料集時，BigQuery 會在下列實體中新增預設資料集存取權。您在資料集建立時指定的角色會覆寫預設值。

| 實體 | 資料集角色 |
| --- | --- |
| 擁有專案 `Viewer` 存取權的所有使用者 | `READER` |
| 擁有專案 `Editor` 存取權的所有使用者 | `WRITER` |
| 擁有專案 `Owner` 存取權的所有使用者，  以及資料集建立者 | `OWNER`  **例外狀況：**使用者執行查詢時，系統會建立[匿名資料集](https://docs.cloud.google.com/bigquery/docs/cached-results?hl=zh-tw#how_cached_results_are_stored)，以儲存快取結果資料表。只有執行該項查詢的使用者具有匿名資料集時的 `OWNER` 存取權。 |




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-16 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-16 (世界標準時間)。"],[],[]]