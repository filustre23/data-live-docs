Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 資源階層結構簡介

BigQuery 資源與其他Google Cloud 服務一樣，都是階層式結構。瞭解這個階層結構，有助於您建構 BigQuery 資源，以便管理工作負載、控管權限、分配配額、指派預留運算單元，以及追蹤帳單。

## 資源階層結構

BigQuery 沿用[Google Cloud 資源階層](https://docs.cloud.google.com/resource-manager/docs/cloud-platform-resource-hierarchy?hl=zh-tw)，並新增 BigQuery 專屬的分組機制，稱為「資料集」。本節將說明這個階層的元素。

### 組織

[機構資源](https://docs.cloud.google.com/resource-manager/docs/cloud-platform-resource-hierarchy?hl=zh-tw#organizations)代表機構 (例如公司)，是Google Cloud 資源階層中的根節點。

您不一定要有組織資源才能開始使用 BigQuery，但建議您建立一個。使用組織資源可讓管理員集中控管 BigQuery 資源，而非由個別使用者控管他們建立的資源。

### 資料夾

資料夾是專案之上的額外分組機制。資料夾中的專案和資料夾會自動沿用上層資料夾的存取權政策。資料夾可用來為公司內的不同法人、部門和團隊建立模型。

這裡討論的資料夾是[Google Cloud 資源階層](https://docs.cloud.google.com/resource-manager/docs/cloud-platform-resource-hierarchy?hl=zh-tw)的一部分。請勿與 [BigQuery 資料夾](https://docs.cloud.google.com/bigquery/docs/code-asset-folders?hl=zh-tw)混淆，後者用於整理程式碼資產。

### 專案

每個 BigQuery 資料集都與一項專案相關聯。您必須建立至少一個專案，才能使用 Google Cloud。專案是建立、啟用及使用所有 Google Cloud 服務的基本要件。詳情請參閱「[資源階層](https://docs.cloud.google.com/resource-manager/docs/cloud-platform-resource-hierarchy?hl=zh-tw)」。一個專案可以包含多個資料集，且不同位置的資料集可以存在於同一個專案中。

對 BigQuery 資料執行作業 (例如執行查詢或將資料擷取至資料表) 時，系統會建立[工作](https://docs.cloud.google.com/bigquery/docs/managing-jobs?hl=zh-tw)。工作一律與專案相關聯，但不一定要在包含資料的專案中執行。事實上，工作可能會參照多個專案中資料集的資料表。查詢工作、載入工作或擷取工作一律會在與其參照的資料表相同的位置執行。

每項專案都附加了 [Cloud Billing 帳戶](https://docs.cloud.google.com/billing/docs/concepts?hl=zh-tw#billing_account)。專案產生的費用會計入該帳戶。如果採用[隨選計價模式](https://cloud.google.com/bigquery/pricing?hl=zh-tw#on_demand_pricing)，查詢費用會計入執行查詢的專案。如果您採用[依運算資源計價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#capacity_compute_analysis_pricing)模式，預留的運算單元費用會計入購買運算單元的管理專案。儲存空間費用會向資料集所在的專案收取。

### 資料集

資料集是邏輯容器，可用於整理及控管 BigQuery 資源的存取權。資料集類似於其他資料庫系統中的結構定義。

您建立的大多數 BigQuery 資源 (包括資料表、檢視表、函式和程序) 都是在資料集內建立。連線和工作是例外狀況，這些與專案相關聯，而非資料集。

資料集有[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)。建立資料表時，資料表資料會儲存在資料集的位置。為正式環境資料建立資料表前，請先考量[位置需求](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw#data-locations)。資料集建立後，即無法變更位置。

## 資源階層結構範例

下圖為資源階層範例。在這個範例中，組織在資料夾內有一個專案。該專案與一個帳單帳戶相關聯，並包含三個資料集。

## 注意事項

選擇如何組織 BigQuery 資源時，請考量下列幾點：

* **配額。**許多 BigQuery [配額](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)都是在專案層級套用。少數則適用於資料集層級。涉及運算資源 (例如查詢和載入工作) 的專案層級配額，會計入建立工作的專案，而非儲存專案。
* **帳單**：如要讓組織中的不同部門使用不同的 Cloud Billing 帳戶，請為各團隊建立不同的專案。在組織層級建立 Cloud Billing 帳戶，並將專案與帳戶建立關聯。
* **運算單元預留項目。**預留[運算單元](https://docs.cloud.google.com/bigquery/docs/slots?hl=zh-tw)的範圍限定為組織資源。購買預留運算單元容量後，您可以將運算單元集區指派給組織中的任何專案或資料夾，或將運算單元指派給整個組織資源。專案會從上層資料夾或組織繼承運算單元預留項目。預留運算單元會與[管理專案](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#admin-project)建立關聯，用於管理運算單元。詳情請參閱「[使用預留項目管理工作負載](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw)」。
* **權限。**請考量權限階層對組織中需要存取資料的人員有何影響。舉例來說，如果您想讓整個團隊存取特定資料，可以將資料儲存在單一專案中，簡化存取權管理。

  資料表和其他實體會繼承其上層資料集的權限。資料集會從資源階層 (專案、資料夾、組織) 中的上層實體繼承權限。如要對資源執行作業，使用者必須具備該資源的相關權限，以及建立 BigQuery 工作的權限。建立工作的權限與用於該工作的專案相關聯。

## 模式

本節介紹兩種常見的 BigQuery 資源組織模式。

* **中央資料湖泊和部門資料市集**。組織會建立統一的儲存空間專案，用來存放原始資料。組織內的部門會建立自己的資料市集專案，以便進行分析。
* **部門資料湖泊，中央資料倉儲**。每個部門都會建立及管理自己的儲存空間專案，用於存放該部門的原始資料。接著，組織會建立中央資料倉儲專案，用於分析。

這兩種方法各有優缺點。許多組織會結合這兩種模式的元素。

### 中央資料湖泊、部門資料市集

在這個模式中，您會建立統合儲存空間專案，用來存放組織的原始資料。資料擷取管道也可以在這個專案中執行。統一儲存空間專案可做為貴組織的資料湖泊。

每個部門都有專屬專案，用於查詢資料、儲存查詢結果及建立檢視表。這些部門層級專案會做為資料市集。這些費用會與部門的帳單帳戶建立關聯。

這種結構的優點包括：

* 集中式資料工程團隊可以在單一位置管理擷取管道。
* 原始資料與部門層級專案隔離。
* 如果採用隨選定價模式，執行查詢的費用會計入執行查詢的部門。
* 您可以根據各部門預計的運算需求，為其指派運算單元。
* 各部門的專案層級配額彼此獨立。

使用這個結構時，通常會用到下列權限：

* 中央資料工程團隊獲派儲存空間專案的 BigQuery 資料編輯者和 BigQuery 工作使用者角色。這樣一來，他們就能在儲存空間專案中擷取及編輯資料。
* 部門分析師會獲得中央資料湖泊專案中特定資料集的 BigQuery 資料檢視者角色。這樣一來，他們就能查詢資料，但無法更新或刪除原始資料。
* 部門分析師也具備部門資料市集專案的 BigQuery 資料編輯者角色和工作使用者角色。這樣一來，他們就能在專案中建立及更新資料表，並執行查詢工作，以便轉換及匯總資料，供部門使用。

詳情請參閱「[基本角色和權限](https://docs.cloud.google.com/bigquery/docs/access-control-basic-roles?hl=zh-tw)」。

### 部門資料湖泊，中央資料倉儲

在這個模式中，每個部門都會建立及管理自己的儲存空間專案，用於存放該部門的原始資料。中央*資料倉儲*專案會儲存原始資料的匯總或轉換。

分析師可以從資料倉儲專案查詢及讀取匯總資料。資料倉儲專案也提供商業智慧 (BI) 工具的存取層。

這種結構的優點包括：

* 為每個部門使用獨立專案，可簡化部門層級的資料存取權管理。
* 中央數據分析團隊有一個專案，專門用來執行數據分析工作，方便監控查詢。
* 使用者可以透過集中式商業智慧工具存取資料，該工具與原始資料保持隔離。
* 您可以將運算單元指派給資料倉儲專案，處理分析師和外部工具的所有查詢。

使用這個結構時，通常會用到下列權限：

* 資料工程師會獲得其部門資料市集的 BigQuery 資料編輯者和 BigQuery 工作使用者角色。這些角色可讓他們擷取資料並轉換至資料市集。
* 分析師在資料倉儲專案中，會獲得 BigQuery 資料編輯者和 BigQuery 工作使用者角色。這些角色可讓他們在資料倉儲中建立匯總檢視表，並執行查詢工作。
* 將 BigQuery 連結至 BI 工具的服務帳戶，會獲得特定資料集的 BigQuery 資料檢視者角色，這些資料集可存放資料湖泊中的原始資料，或資料倉儲專案中的轉換資料。

詳情請參閱「[基本角色和權限](https://docs.cloud.google.com/bigquery/docs/access-control-basic-roles?hl=zh-tw)」。

您也可以使用[授權檢視表](https://docs.cloud.google.com/bigquery/docs/authorized-views?hl=zh-tw)和[授權使用者定義函式](https://docs.cloud.google.com/bigquery/docs/user-defined-functions?hl=zh-tw#authorize_routines) (UDF) 等安全防護功能，向特定使用者提供匯總資料，而不授予他們查看資料市集專案中原始資料的權限。

這種專案結構可能會導致資料倉儲專案中出現許多並行查詢。因此，您可能會達到[並行查詢限制](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#query_jobs)。如果採用這種結構，建議提高專案的配額限制。此外，您也可以考慮使用以運算資源為基礎的計費模式，購買運算單元集區來執行查詢。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-10-28 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-10-28 (世界標準時間)。"],[],[]]