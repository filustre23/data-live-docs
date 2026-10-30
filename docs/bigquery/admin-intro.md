Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# BigQuery 管理簡介

BigQuery 管理功能可讓您設定、保護及監控整個組織的資料資源和運算工作負載。您可以使用這些功能分配運算能力、提升查詢效能、控管成本，以及強制執行存取權政策。

如要直接在 Google Cloud 控制台導覽 BigQuery 資料管理功能，請按一下「Take the tour」(導覽)。

[開始導覽](https://console.cloud.google.com/?walkthrough_id=bigquery--ui-tour-data-admin&hl=zh-tw)

## 工具

BigQuery 提供多個介面，可用於執行管理工作。通常，特定工作可以透過多種工具完成，您可以選擇最適合自己的工具。舉例來說，您可以使用Google Cloud 控制台中的「Explorer」窗格、`bq mk --table` 指令或 `CREATE TABLE` SQL 陳述式建立資料表。

* **Google Cloud 控制台。** Google Cloud 控制台有多個頁面專門用於 BigQuery 管理。詳情請參閱「[使用 Google Cloud 控制台](https://docs.cloud.google.com/bigquery/docs/bigquery-web-ui?hl=zh-tw)」。
* **SQL 陳述式**。Google Cloud 控制台的 BigQuery 頁面提供查詢編輯器，您可以使用 DDL 和 DCL 陳述式執行管理工作。詳情請參閱「[資料定義語言 (DDL)](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw)」和「[資料控制語言 (DCL)](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-control-language?hl=zh-tw)」。

  您可以使用預存程序，自動執行使用 SQL 陳述式的管理工作。詳情請參閱「[使用預存程序](https://docs.cloud.google.com/bigquery/docs/procedures?hl=zh-tw)」。
* **`bq` 指令。**bq 指令列工具可讓您使用 `bq` 指令執行多項管理工作。您可以使用 bq 指令列工具執行 Google Cloud 控制台不支援的工作、在查詢或 API 方法中編碼前先設計功能原型，或在指令列介面中工作。詳情請參閱「[使用 bq 指令列工具](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw)」。

## 管理資源

BigQuery 資源包括組織、資料夾、專案、資料集和資料表。本節說明如何管理貴組織的資源。

如要瞭解如何整理 BigQuery 資源，請參閱「[資源階層簡介](https://docs.cloud.google.com/bigquery/docs/resource-hierarchy?hl=zh-tw)」。具體來說，您可以建立組織資源，以便在組織層級執行某些工作，例如設定存取控管。

### 管理資料集

資料集是資料表的容器。您可以在資料集中建立資料表，然後以群組形式管理。舉例來說，您可以設定資料集的預設資料表到期時間，除非您覆寫這項設定，否則該設定會套用至資料集內的所有資料表。您可以複製資料集，藉此複製一組資料表，並在資料集層級控管資料表的存取權。

如要進一步瞭解資料集管理，請參閱下列文件：

* 如要進一步瞭解如何建立、複製、移動及更新資料集，請參閱「[資料集簡介](https://docs.cloud.google.com/bigquery/docs/datasets-intro?hl=zh-tw)」。
* 如要進一步瞭解資料集層級的存取控管，請參閱「[使用資料集存取控管](https://docs.cloud.google.com/bigquery/docs/control-access-to-resources-iam?hl=zh-tw#work_with_dataset_access_controls)」和「[授權資料集](https://docs.cloud.google.com/bigquery/docs/authorized-datasets?hl=zh-tw)」。

### 管理資料表

在 BigQuery 中，資料會儲存在資料表，方便您查詢。您可以建立資料表、從各種來源和格式將資料載入資料表、根據特定資料欄或擷取時間將資料表分區、將資料表分群、更新資料表屬性，以及匯出資料表資料。

如要進一步瞭解資料表管理，請參閱下列文件：

* 如要進一步瞭解如何將資料載入 BigQuery 資料表，請參閱「[載入資料表簡介](https://docs.cloud.google.com/bigquery/docs/loading-data?hl=zh-tw)」。
* 如要進一步瞭解如何管理資料表及匯出資料表資料，請參閱「[資料表簡介](https://docs.cloud.google.com/bigquery/docs/tables-intro?hl=zh-tw)」。
* 如要進一步瞭解資料表分區和分群，請參閱「[分區資料表簡介](https://docs.cloud.google.com/bigquery/docs/partitioned-tables?hl=zh-tw)」和「[分群資料表簡介](https://docs.cloud.google.com/bigquery/docs/clustered-tables?hl=zh-tw)」。

### 標籤資源

您可以在資料集、資料表和檢視表中加入標籤，協助您整理 BigQuery 資源。標籤是您可以附加至資源的鍵/值組合。為資源加上標籤後，即可根據標籤值搜尋資源。舉例來說，您可以新增 `dept:sales`、`dept:marketing` 或 `dept:analytics` 等標籤，依部門將資料集分組。然後使用標籤[依部門細分帳單費用](https://docs.cloud.google.com/billing/docs/how-to/bq-examples?hl=zh-tw)。

詳情請參閱「[標籤簡介](https://docs.cloud.google.com/bigquery/docs/labels-intro?hl=zh-tw)」。

### 取得資源資訊

您可以查詢 `INFORMATION_SCHEMA` 檢視表，取得 BigQuery 資源的相關資訊。BigQuery 會為每種資源類型提供[檢視表](https://docs.cloud.google.com/bigquery/docs/views-intro?hl=zh-tw)。例如，`INFORMATION_SCHEMA.TABLES` 檢視表包含資料表的相關資訊。

以下列舉幾個例子，說明您可以透過查詢 `INFORMATION_SCHEMA` 檢視表取得哪些資訊：

* 查看資料表的建立時間。
* 取得資料表中各資料欄的名稱和資料類型。
* 找出專案中執行的所有工作。
* 取得從基礎資料表建立的資料表快照清單。
* 針對資料集、資料表、檢視表或常式，取得可用於建立資源的 DDL 陳述式。
* 取得用於建立資料表的選項 (例如資料表到期時間)。
* 找出資料表的分區和分群資料欄。
* 取得專案指派的預留項目和運算單元容量。

詳情請參閱「[BigQuery `INFORMATION_SCHEMA` 簡介](https://docs.cloud.google.com/bigquery/docs/information-schema-intro?hl=zh-tw)」。

### 複製資料

您可能基於各種原因需要建立資料副本，例如避免人為錯誤，或保留資料以供日後比較。BigQuery 提供多種選項，可複製特定時間點的資料表資料。

* **時間回溯。**您可能需要存取資料表在過去一週內某個時間點的狀態，例如資料因人為錯誤而損毀時。BigQuery 會保留資料表的歷來資料七天。您可以使用時光旅行功能，存取資料表近期的歷來資料。

  詳情請參閱「[使用時間旅行功能存取歷來資料](https://docs.cloud.google.com/bigquery/docs/time-travel?hl=zh-tw)」。
* **資料表快照。**如要存取一週前的資料表狀態，建議定期建立[資料表快照](https://docs.cloud.google.com/bigquery/docs/table-snapshots-intro?hl=zh-tw)。資料表快照是輕量級的唯讀副本，可讓您無限期保留資料表的狀態。舉例來說，您可以使用資料表快照，比較資料表目前的資料與年初的資料，但無法使用時間旅行功能。您只需支付基礎資料表和資料表快照之間差異資料的儲存費用。

  詳情請參閱「[資料表快照簡介](https://docs.cloud.google.com/bigquery/docs/table-snapshots-intro?hl=zh-tw)」。
* **資料表本機副本**如要建立輕量、可寫入的資料表副本，可以使用資料表複製。您只需支付基礎資料表和資料表複製版本之間差異資料的儲存費用。舉例來說，您可以在測試環境中建立資料表複製，以便使用正式環境資料的副本進行實驗，而不會影響正式環境資料，也不必支付完整資料表副本的儲存費用。

  詳情請參閱「[資料表複製版本簡介](https://docs.cloud.google.com/bigquery/docs/table-clones-intro?hl=zh-tw)」。

### 追蹤資料歷程

資料歷程是 [Knowledge Catalog](https://docs.cloud.google.com/knowledge-catalog/docs/introduction?hl=zh-tw) 的功能，可以追蹤資料在系統的移動情形，包括來源、傳遞目的地和採用的轉換作業。如要進一步瞭解資料歷程如何協助您追蹤專案中的資料移動，請參閱 Knowledge Catalog 的「[關於資料歷程](https://docs.cloud.google.com/knowledge-catalog/docs/about-data-lineage?hl=zh-tw)」。

### 保護資源

BigQuery 安全性是以 [Google Cloud Identity and Access Management](https://docs.cloud.google.com/iam/docs?hl=zh-tw) 為基礎。BigQuery 可讓您在多個層級控管資源存取權，包括機構、資料夾、專案、資料集、資料表、資料表資料欄和資料表資料列。

如要瞭解如何控管 BigQuery 資源的存取權，請參閱「[資料安全性與管理總覽](https://docs.cloud.google.com/bigquery/docs/data-governance?hl=zh-tw)」。

## 管理工作負載

BigQuery 會代表使用者執行許多工作，包括擷取、查詢和匯出資料。每項工作都是由 BigQuery *工作*完成。本節說明如何監控及管理組織的工作。

### 管理工作機會

工作是 BigQuery 代表使用者執行的動作，用於載入、匯出、查詢或複製資料。當使用者透過[Google Cloud 控制台](https://docs.cloud.google.com/bigquery/docs/bigquery-web-ui?hl=zh-tw)、[bq 指令列工具](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw)、[SQL 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/lexical?hl=zh-tw)或 [API 呼叫](https://docs.cloud.google.com/bigquery/docs/running-jobs?hl=zh-tw)啟動其中一項工作時，BigQuery 會自動建立工作來執行該工作。

BigQuery 管理員可以監控、管理及排解組織的工作，確保工作順利執行。

詳情請參閱「[管理工作](https://docs.cloud.google.com/bigquery/docs/managing-jobs?hl=zh-tw)」。

### 管理保留項目

BigQuery 執行查詢時，會使用稱為「*運算單元*」的運算單位。BigQuery 會依據查詢的規模和複雜程度，計算執行每項查詢所需的運算單元數量。

BigQuery 針對執行查詢的運算單元，提供兩種計費模式：

* **隨選計費。**查詢會使用共用的運算單元集區，費用則依查詢處理的位元組數計算。如要進一步瞭解隨選計費限制，請參閱「[查詢工作](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#query_jobs)」。
* **依容量計費。**您可以將預留項目或運算資源承諾使用合約指派給版本，每個版本都有專屬的功能集和價格點，可提供最適合您的工作環境。

這些定價模式適用於各項專案，因此您可以讓部分專案使用隨選計費，部分專案使用依容量計費。

如果採用隨選計價模式，當月[免費額度](https://cloud.google.com/bigquery/pricing?hl=zh-tw#free-tier)用完後，系統會根據每項查詢處理的位元組數收費。處理量受限於預先定義的運算單元配額，由專案中執行的查詢共用。

採用 BigQuery 版本計費模式時，您可透過自動調度資源預留項目，以及選用但費用較低的運算資源承諾使用合約，為組織分配運算單元。每個版本的運算單元都有各自的價格點，並提供專屬功能。如要進一步瞭解 BigQuery 版本和相關功能，請參閱「[BigQuery 版本簡介](https://docs.cloud.google.com/bigquery/docs/editions-intro?hl=zh-tw)」。

如要進一步瞭解如何管理處理查詢的運算能力，請參閱下列文件：

* 如要瞭解運算單元，以及隨選計費和以運算資源為基礎的計費模式之間的取捨，請參閱「[預留項目簡介](https://docs.cloud.google.com/bigquery/docs/reservations-intro?hl=zh-tw)」。
* 如要瞭解依據運算能力計費的不同選項 (按月或按年承諾使用合約)，請參閱「[管理工作負載承諾使用合約](https://docs.cloud.google.com/bigquery/docs/reservations-commitments?hl=zh-tw)」。
* 如要建立以容量為基礎的運算單元集區 (稱為「運算單元預留項目」)，請參閱「[使用運算單元預留項目](https://docs.cloud.google.com/bigquery/docs/reservations-tasks?hl=zh-tw)」。
* 如要將運算單元預留項目分配給特定專案，請參閱「[使用預留項目指派作業](https://docs.cloud.google.com/bigquery/docs/reservations-assignments?hl=zh-tw)」。
* 如要預估應分配給工作負載的運算單元數量，請參閱「[預估運算單元容量需求](https://docs.cloud.google.com/bigquery/docs/slot-estimator?hl=zh-tw)」。

## 監控資源

Google Cloud 提供監控及稽核資源的功能，包括 BigQuery 資源。本節說明適用於 BigQuery 的Google Cloud 監控和稽核功能。

詳情請參閱「[BigQuery 監控簡介](https://docs.cloud.google.com/bigquery/docs/monitoring?hl=zh-tw)」。

### Cloud Monitoring 資訊主頁

Cloud Monitoring 提供監控 BigQuery 的資訊主頁。您可以使用這個資訊主頁，查看 BigQuery 事件、資料集、資料表、專案、查詢時間和運算單元使用率的相關資訊。

詳情請參閱「[查看 Monitoring 資訊主頁](https://docs.cloud.google.com/bigquery/docs/monitoring-dashboard?hl=zh-tw#view-dashboards)」。

### 管理圖表和快訊

您可以使用 Cloud Monitoring，根據指定的資源、指標和任何匯總建立自訂圖表。

詳情請參閱「[資訊主頁和圖表](https://docs.cloud.google.com/monitoring/dashboards?hl=zh-tw)」。

您也可以建立警告政策，在觸發設定的警告時通知您。舉例來說，您可以建立快訊，在查詢執行時間超過指定限制時，傳送電子郵件到指定電子郵件地址。

詳情請參閱「[建立快訊](https://docs.cloud.google.com/bigquery/docs/monitoring-dashboard?hl=zh-tw#create-alert)」。

### 監控保留項目

您可以在Google Cloud 控制台的「Workload management」(工作負載管理) 頁面監控運算單元用量。您可以查看運算資源承諾使用合約，以及運算單元預留項目的指派位置。您也可以使用**運算單元估算工具** ([預先發布版](https://cloud.google.com/products?hl=zh-tw#section-22))，根據歷來成效指標，預估組織的容量需求。

詳情請參閱「[監控 BigQuery 預留項目](https://docs.cloud.google.com/bigquery/docs/reservations-monitoring?hl=zh-tw)」。

### 配額

Google Cloud 會限制資源的使用，包括 BigQuery 資源，以確保共用資源的公平使用，並防止成本失控。您可以查看設有[配額](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)的 BigQuery 資源用量，並視需要透過 Google Cloud 控制台[要求提高配額](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#requesting_a_quota_increase)。

詳情請參閱「[BigQuery 配額與限制](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)」。

### 稽核記錄

Cloud 稽核記錄會保存 Google Cloud 事件的記錄，包括 BigQuery 事件。您可以使用**Logs Explorer**，查詢與 BigQuery 工作、資料集、移轉作業等相關事件的記錄。「**Logs Dashboard**」(記錄資訊主頁) 會顯示近期錯誤的相關資訊，您可以使用**記錄指標**計算符合特定篩選條件的記錄項目數量。

詳情請參閱 [Google Cloud 記錄說明文件](https://docs.cloud.google.com/logging/docs?hl=zh-tw)。

## 最佳化工作負載

您可以最佳化 BigQuery 設定，控管儲存空間和查詢處理費用。

* 如需管理 BigQuery 儲存空間費用的協助，請參閱「[最佳化 BigQuery 儲存空間](https://docs.cloud.google.com/bigquery/docs/best-practices-storage?hl=zh-tw)」。
* 如需管理 BigQuery 處理費用的協助，請參閱「[在 BigQuery 控管費用](https://docs.cloud.google.com/bigquery/docs/best-practices-costs?hl=zh-tw)」。
* 如需最佳化 BigQuery 查詢的協助，請參閱「[最佳化查詢效能簡介](https://docs.cloud.google.com/bigquery/docs/best-practices-performance-overview?hl=zh-tw)」。
* 如需 BigQuery 費用的一般資訊，請參閱「[BigQuery 定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw)」 和「[BigQuery 帳單問題](https://docs.cloud.google.com/bigquery/docs/billing-questions?hl=zh-tw)」。

## 可靠性指南

本文將說明 BigQuery 的可靠性，包括可用性、耐用性、資料一致性、效能一致性和資料復原，並探討錯誤處理的注意事項。如要進一步瞭解可靠性和災難規劃，請參閱「[瞭解可靠性](https://docs.cloud.google.com/bigquery/docs/reliability-intro?hl=zh-tw)」。

## 疑難排解

除了本文所述用於監控及管理組織 BigQuery 系統的功能外，您也可以使用下列資源，排解可能發生的問題：

* [BigQuery 錯誤訊息](https://docs.cloud.google.com/bigquery/docs/error-messages?hl=zh-tw)
* [BigQuery 計費問題](https://docs.cloud.google.com/bigquery/docs/billing-questions?hl=zh-tw)
* [排解配額錯誤](https://docs.cloud.google.com/bigquery/docs/troubleshoot-quotas?hl=zh-tw)

如需其他協助，請參閱「[取得支援](https://docs.cloud.google.com/bigquery/docs/getting-support?hl=zh-tw)」。

## 後續步驟

* [BigQuery 管理員參考指南：重點回顧](https://cloud.google.com/blog/topics/developers-practitioners/bigquery-admin-reference-guide-recap?hl=zh-tw)




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-10-29 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-10-29 (世界標準時間)。"],[],[]]