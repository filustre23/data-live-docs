Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# BigQuery 管理簡介

本文將介紹 BigQuery 管理工作，以及協助您完成這些工作的 BigQuery 功能。

BigQuery 管理員通常會執行下列類型的工作：

* 管理專案、資料集和資料表等資源。
* 保護資源，僅限必要主體存取。
* 管理工作負載，例如作業、查詢和運算容量 (預留)。
* 監控資源，包括配額、工作和運算用量。
* 盡可能提高工作負載的效能，同時控管成本。
* 排解錯誤訊息、帳單問題和配額。

本文將概述 BigQuery 提供的功能，協助您完成這些工作。

如要直接在 Google Cloud 控制台中導覽 BigQuery 資料管理功能，請按一下「Take the tour」(參加導覽)。

[觀看導覽](https://console.cloud.google.com/?walkthrough_id=bigquery--ui-tour-data-admin&hl=zh-tw)

## 工具

BigQuery 提供多種介面，可用於執行管理工作。通常特定工作可使用多種工具完成，因此你可以選擇最適合自己的工具。舉例來說，您可以使用Google Cloud 控制台的「探索」窗格、`bq mk --table` 指令或 `CREATE TABLE` SQL 陳述式建立資料表。

* **Google Cloud console.** Google Cloud 控制台提供多個專用於 BigQuery 管理的頁面。詳情請參閱「[使用 Google Cloud 控制台](https://docs.cloud.google.com/bigquery/docs/bigquery-web-ui?hl=zh-tw)」一文。
* **SQL 陳述式**。Google Cloud 控制台的 BigQuery 頁面提供查詢編輯器，您可以使用 DDL 和 DCL 陳述式執行管理工作。詳情請參閱「[資料定義語言 (DDL)](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw)」和「[資料控制語言 (DCL)](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-control-language?hl=zh-tw)」。

  您可以使用預存程序，自動執行使用 SQL 陳述式的管理工作。詳情請參閱「[使用預存程序](https://docs.cloud.google.com/bigquery/docs/procedures?hl=zh-tw)」。
* **`bq`指令。**您可以使用 bq 指令列工具，透過 `bq` 指令執行許多管理工作。您可以使用 bq 指令列工具執行 Google Cloud 控制台不支援的工作，在查詢或 API 方法中編碼功能前，先製作功能原型，或在指令列介面中工作。詳情請參閱「[使用 bq 指令列工具](https://docs.cloud.google.com/bigquery/docs/bq-command-line-tool?hl=zh-tw)」。

## 管理資源

BigQuery 資源包括機構、資料夾、專案、資料集和資料表。本節說明如何管理機構的資源。

如要瞭解 BigQuery 資源階層，請參閱「[整理 BigQuery 資源](https://docs.cloud.google.com/bigquery/docs/resource-hierarchy?hl=zh-tw)」。具體來說，您可以建立機構資源，在機構層級執行設定存取權控管等工作。

### 管理資料集

資料集是資料表的容器，您可以在資料集中建立資料表，然後以群組形式管理這些資料表。舉例來說，您可以設定資料集的預設資料表到期時間，這項設定會套用至資料集中的所有資料表，除非您覆寫這項設定。您可以複製資料集來複製一組資料表，並在資料集層級控管資料表存取權。

如要進一步瞭解資料集管理，請參閱下列文件：

* 如要進一步瞭解如何建立、複製、移動及更新資料集，請參閱「[資料集簡介](https://docs.cloud.google.com/bigquery/docs/datasets-intro?hl=zh-tw)」。
* 如要進一步瞭解資料集層級的存取控管，請參閱「[控管資料集存取權](https://docs.cloud.google.com/bigquery/docs/dataset-access-controls?hl=zh-tw)」和「[授權資料集](https://docs.cloud.google.com/bigquery/docs/authorized-datasets?hl=zh-tw)」。

### 管理資料表

BigQuery 會將資料儲存在資料表中，方便您查詢。您可以建立資料表、從各種來源以各種格式將資料載入資料表、依特定資料欄或擷取時間將資料表分區、叢集資料表、更新資料表屬性，以及匯出資料表資料。

如要進一步瞭解表格管理，請參閱下列文件：

* 如要進一步瞭解如何將資料載入 BigQuery 資料表，請參閱「[載入資料表簡介](https://docs.cloud.google.com/bigquery/docs/loading-data?hl=zh-tw)」。
* 如要進一步瞭解如何管理資料表及匯出資料表資料，請參閱[資料表簡介](https://docs.cloud.google.com/bigquery/docs/tables-intro?hl=zh-tw)。
* 如要進一步瞭解如何分區及叢集資料表，請參閱[分區資料表簡介](https://docs.cloud.google.com/bigquery/docs/partitioned-tables?hl=zh-tw)和[叢集資料表簡介](https://docs.cloud.google.com/bigquery/docs/clustered-tables?hl=zh-tw)。

### 為資源加上標籤

您可以在資料集、資料表和檢視表中加入標籤，協助您整理 BigQuery 資源。標籤是您可以附加至資源的鍵/值組合。為資源加上標籤後，您就可以根據標籤值搜尋資源。舉例來說，您可以新增 `dept:sales`、`dept:marketing` 或 `dept:analytics` 等標籤，依部門將資料集分組。然後使用標籤，依部門[細分帳單費用](https://docs.cloud.google.com/billing/docs/how-to/bq-examples?hl=zh-tw)。

詳情請參閱「[標籤簡介](https://docs.cloud.google.com/bigquery/docs/labels-intro?hl=zh-tw)」。

### 取得資源資訊

您可以查詢 `INFORMATION_SCHEMA` 檢視區塊，取得 BigQuery 資源的相關資訊。BigQuery 會為每個資源類型提供[檢視畫面](https://docs.cloud.google.com/bigquery/docs/views-intro?hl=zh-tw)。舉例來說，`INFORMATION_SCHEMA.TABLES` 檢視畫面包含資料表的相關資訊。

以下列舉幾個可透過查詢 `INFORMATION_SCHEMA` 檢視畫面取得的資訊：

* 查看資料表的建立時間。
* 取得資料表中每個資料欄的名稱和資料類型。
* 找出專案中執行的所有工作。
* 取得從基礎資料表建立的資料表快照清單。
* 針對資料集、資料表、檢視區塊或常式，取得可用於建立資源的 DDL 陳述式。
* 取得用於建立資料表的選項 (例如資料表到期時間)。
* 找出資料表的分區和叢集資料欄。
* 取得專案的指派預留項目及其運算單元容量。

詳情請參閱 [BigQuery 簡介](https://docs.cloud.google.com/bigquery/docs/information-schema-intro?hl=zh-tw)。`INFORMATION_SCHEMA`

### 複製資料

您可能基於各種原因需要建立資料副本，例如避免人為錯誤，或保留資料以供日後比較。BigQuery 提供多種選項，可從特定時間點複製資料表資料。

* **時間回溯。**您可能需要存取過去一週內某個時間點的資料表狀態，例如資料因人為錯誤而損毀。BigQuery 會將資料表的歷來資料保留七天。您可以使用時空旅行功能，存取表格的近期歷來資料。

  詳情請參閱「[使用時間旅行功能存取歷來資料](https://docs.cloud.google.com/bigquery/docs/time-travel?hl=zh-tw)」。
* **資料表快照。**
  如要存取資料表在過去一週前的狀態，請考慮定期建立[資料表快照](https://docs.cloud.google.com/bigquery/docs/table-snapshots-intro?hl=zh-tw)。資料表快照是輕量型的唯讀副本，可無限期保留資料表狀態。舉例來說，您可以使用資料表快照比較資料表目前的資料與年初的資料，但這無法透過時空旅行功能達成。您只需支付基本資料表與資料表快照之間差異資料的儲存費用。

  詳情請參閱「[資料表快照簡介](https://docs.cloud.google.com/bigquery/docs/table-snapshots-intro?hl=zh-tw)」。
* **資料表本機副本**。
  如要建立資料表的輕量型可寫入副本，可以使用資料表副本。您只需支付基本資料表與資料表副本之間差異資料的儲存空間費用。舉例來說，您可以在測試環境中建立資料表副本，以便使用正式環境資料副本進行實驗，不會影響正式環境資料，也不必支付完整資料表副本的儲存空間費用。

  詳情請參閱[資料表副本簡介](https://docs.cloud.google.com/bigquery/docs/table-clones-intro?hl=zh-tw)。

### 追蹤資料歷程

資料歷程是 [Knowledge Catalog](https://docs.cloud.google.com/dataplex/docs/introduction?hl=zh-tw) 的功能，可追蹤資料在系統中的移動情形，包括來源、傳遞目的地和採用的轉換作業。如要進一步瞭解資料歷程如何協助您追蹤專案中的資料移動情形，請參閱 Knowledge Catalog 的「[關於資料歷程](https://docs.cloud.google.com/dataplex/docs/about-data-lineage?hl=zh-tw)」一文。

### 安全資源

BigQuery 安全防護機制以[Google Cloud 身分與存取權管理](https://docs.cloud.google.com/iam/docs?hl=zh-tw)為基礎。BigQuery 可讓您在多個層級控管資源存取權，包括機構、資料夾、專案、資料集、資料表、資料表欄和資料表列的存取權。

如要瞭解如何控管 BigQuery 資源的存取權，請參閱「[資料安全性與治理總覽](https://docs.cloud.google.com/bigquery/docs/data-governance?hl=zh-tw)」。

## 管理工作負載

BigQuery 會代表使用者執行許多工作，包括擷取、查詢及匯出資料。每項工作都是由 BigQuery *工作*完成。本節說明如何監控及管理貴機構的工作。

### 管理工作機會

「工作」是指 BigQuery 代表使用者執行的動作，包括載入、匯出、查詢或複製資料。使用者透過 [Google Cloud 主控台](https://docs.cloud.google.com/bigquery/docs/bigquery-web-ui?hl=zh-tw)、[bq 指令列工具](https://docs.cloud.google.com/bigquery/docs/bq-command-line-tool?hl=zh-tw)、[SQL 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/lexical?hl=zh-tw)或 [API 呼叫](https://docs.cloud.google.com/bigquery/docs/running-jobs?hl=zh-tw)啟動其中一項工作時，BigQuery 會自動建立工作來執行該工作。

BigQuery 管理員可以監控、管理及排解機構的作業問題，確保作業順利執行。

詳情請參閱「[管理工作](https://docs.cloud.google.com/bigquery/docs/managing-jobs?hl=zh-tw)」。

### 管理保留項目

BigQuery 執行查詢時，會使用稱為「*運算單元*」的運算單位。BigQuery 會根據查詢的大小和複雜度，計算執行各項查詢所需的運算單元數量。

BigQuery 提供兩種計費模式，可針對執行查詢的運算單元收費：

* **以量計價。**您的查詢會使用共用的運算單元集區，系統會根據查詢處理的位元組數向您收費。如要進一步瞭解隨選帳單限制，請參閱「[查詢工作](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#query_jobs)」。
* **根據容量計費**：您可以為版本指派預留項目或承諾使用，每個版本都有自己的特徵集和價位，可為您提供最佳工作環境。

這些計費模式適用於各個專案，因此您可以讓部分專案採用以量計價，部分專案採用以容量計費。

採用以量計價模式時，每月[免費用量](https://cloud.google.com/bigquery/pricing?hl=zh-tw#free-tier)用完後，系統會根據各項查詢處理作業的位元組數向您收費。總處理量會受到預先定義的運算單元配額限制，且專案中執行的查詢會共用配額。

採用 BigQuery 版本計費時，您可以透過自動調度資源預留項目，以及選用但較便宜的容量承諾使用，為機構分配運算單元。每個版本的席位都有各自的價格，並提供專屬功能。如要進一步瞭解 BigQuery 版本和相關功能，請參閱「[BigQuery 版本簡介](https://docs.cloud.google.com/bigquery/docs/editions-intro?hl=zh-tw)」。

如要進一步瞭解如何管理運算容量來處理查詢，請參閱下列文件：

* 如要瞭解配額，以及隨選帳單和以容量為準帳單之間的取捨，請參閱「[預訂簡介](https://docs.cloud.google.com/bigquery/docs/reservations-intro?hl=zh-tw)」。
* 如要瞭解以容量為準的計費方式 (月約或年約) 的不同選項，請參閱[配額承諾](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#slot_commitments)。
* 如要建立以容量為準的運算單元集區 (稱為「運算單元保留」)，請參閱「[使用運算單元保留功能](https://docs.cloud.google.com/bigquery/docs/reservations-tasks?hl=zh-tw)」。
* 如要將運算單元預留項目分配給特定專案，請參閱「[處理預留項目指派作業](https://docs.cloud.google.com/bigquery/docs/reservations-assignments?hl=zh-tw)」。
* 如要估算要為工作負載分配的適當運算單元數量，請參閱「[估算運算單元容量需求](https://docs.cloud.google.com/bigquery/docs/slot-estimator?hl=zh-tw)」。

## 監控資源

Google Cloud 針對您的資源 (包含 BigQuery 資源) 提供監控與稽核功能。本節說明適用於 BigQuery 的Google Cloud 監控和稽核功能。

詳情請參閱「[BigQuery 監控簡介](https://docs.cloud.google.com/bigquery/docs/monitoring?hl=zh-tw)」。

### Cloud Monitoring 資訊主頁

Cloud Monitoring 提供資訊主頁，可監控 BigQuery。
您可以使用這個資訊主頁查看 BigQuery 事件、資料集、資料表、專案、查詢時間和時段用量等資訊。

詳情請參閱「[查看 Monitoring 資訊主頁](https://docs.cloud.google.com/bigquery/docs/monitoring-dashboard?hl=zh-tw#view-dashboards)」。

### 管理圖表和快訊

您可以根據指定的資源、指標和任何彙整方式，使用 Cloud Monitoring 建立自訂圖表。

詳情請參閱「[資訊主頁和圖表](https://docs.cloud.google.com/monitoring/dashboards?hl=zh-tw)」。

您也可以建立快訊政策，在設定的快訊觸發時收到通知。舉例來說，您可以建立警告，在查詢的執行時間超過指定上限時，傳送電子郵件到指定電子郵件地址。

詳情請參閱「[建立快訊](https://docs.cloud.google.com/bigquery/docs/monitoring-dashboard?hl=zh-tw#create-alert)」。

### 監控保留項目

您可以在Google Cloud 控制台的「容量管理」頁面中，監控運算單元用量。您可以查看容量承諾，以及運算單元預留位置的指派位置。您也可以使用**運算單元估算工具** ([預先發布版](https://cloud.google.com/products?hl=zh-tw#section-22))，根據歷來成效指標估算貴機構的容量需求。

詳情請參閱「[監控 BigQuery 預留項目](https://docs.cloud.google.com/bigquery/docs/reservations-monitoring?hl=zh-tw)」。

### 配額

Google Cloud 會限制資源用量 (包括 BigQuery 資源)，確保共用資源的用量公平，並避免您產生過高的費用。您可以使用 Google Cloud 控制台查看有[配額](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)的 BigQuery 資源用量，並視需要[申請更多配額](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#requesting_a_quota_increase)。

詳情請參閱「[BigQuery 配額與限制](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)」。

### 稽核記錄

Cloud 稽核記錄會記錄 Google Cloud 事件，包括 BigQuery 事件。您可以使用**Logs Explorer**查詢與 BigQuery 工作、資料集、移轉作業等相關事件的記錄。**記錄資訊主頁**會顯示近期錯誤的相關資訊，您也可以使用**記錄指標**，計算符合特定篩選條件的記錄項目數量。

詳情請參閱[Google Cloud 記錄說明文件](https://docs.cloud.google.com/logging/docs?hl=zh-tw)。

## 最佳化工作負載

您可以將 BigQuery 設定最佳化，控管儲存空間和查詢處理費用。

* 如需管理 BigQuery 儲存空間費用的協助，請參閱「[盡可能降低 BigQuery 的儲存費用](https://docs.cloud.google.com/bigquery/docs/best-practices-storage?hl=zh-tw)」。
* 如需管理 BigQuery 處理費用的協助，請參閱「[控管 BigQuery 費用](https://docs.cloud.google.com/bigquery/docs/best-practices-costs?hl=zh-tw)」。
* 如需最佳化 BigQuery 查詢的協助，請參閱「[最佳化查詢效能簡介](https://docs.cloud.google.com/bigquery/docs/best-practices-performance-overview?hl=zh-tw)」。
* 如要瞭解 BigQuery 費用的一般資訊，請參閱「[BigQuery 定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw)」 和「[BigQuery 帳單問題](https://docs.cloud.google.com/bigquery/docs/billing-questions?hl=zh-tw)」。

## 可靠性指引

本文將說明 BigQuery 的可靠性，包括可用性、耐久性、資料一致性、效能一致性，以及 BigQuery 中的資料復原，並回顧錯誤處理考量。如要進一步瞭解可靠性和災害規劃，請參閱「[瞭解可靠性](https://docs.cloud.google.com/bigquery/docs/reliability-intro?hl=zh-tw)」。

## 疑難排解

除了本文所述的監控與管理貴機構 BigQuery 系統功能外，您也可以參考下列資源，排解可能發生的問題：

* [BigQuery 錯誤訊息](https://docs.cloud.google.com/bigquery/docs/error-messages?hl=zh-tw)
* [BigQuery 帳單問題](https://docs.cloud.google.com/bigquery/docs/billing-questions?hl=zh-tw)
* [排解配額錯誤](https://docs.cloud.google.com/bigquery/docs/troubleshoot-quotas?hl=zh-tw)

如需其他協助，請參閱「[取得支援](https://docs.cloud.google.com/bigquery/docs/getting-support?hl=zh-tw)」。

## 後續步驟

* 如要觀看 BigQuery 管理相關主題的系列影片，請參閱 [BigQuery 管理參考指南：回顧](https://cloud.google.com/blog/topics/developers-practitioners/bigquery-admin-reference-guide-recap?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-02 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-02 (世界標準時間)。"],[],[]]