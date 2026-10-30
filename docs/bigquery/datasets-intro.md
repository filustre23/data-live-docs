Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 資料集簡介

BigQuery 資料集可用來整理資料表和檢視表，並控管存取權。您也可以使用資料集指定儲存位置、管理保留政策，以及連結至外部資料來源。

## 資料集

資料集包含在特定[專案](https://docs.cloud.google.com/docs/overview?hl=zh-tw#projects)中，是用來整理及控管[資料表](https://docs.cloud.google.com/bigquery/docs/tables?hl=zh-tw)與[檢視表](https://docs.cloud.google.com/bigquery/docs/views?hl=zh-tw)存取權的頂層容器。資料表或檢視表必須屬於某個資料集，因此您需要建立至少一個資料集，才能[將資料載入 BigQuery](https://docs.cloud.google.com/bigquery/loading-data-into-bigquery?hl=zh-tw)。使用 GoogleSQL 時，請採用 `projectname.datasetname` 格式來指定完整的資料集名稱；使用 bq 指令列工具時，請採用 `projectname:datasetname` 格式來指定完整的資料集名稱。

## 位置

您可以在建立資料集時指定 BigQuery 資料的儲存位置。如需 BigQuery 資料集位置清單，請參閱「[BigQuery 位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)」。BigQuery 會依據《[服務專屬條款](https://cloud.google.com/terms/service-terms?hl=zh-tw)》將資料儲存在所選位置。舉例來說，如果您選擇 `EU` 或位於歐盟的區域做為資料集位置，核心 BigQuery 客戶資料就會存放在歐盟。

資料集建立後，位置即無法變更，
但您可以[將資料集複製到其他位置](https://docs.cloud.google.com/bigquery/docs/managing-datasets?hl=zh-tw#copy-datasets)，
或手動[將資料集移動 (重新建立) 至其他位置](https://docs.cloud.google.com/bigquery/docs/managing-datasets?hl=zh-tw#recreate-dataset)。

如果您未[明確指定位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw#specify_locations)，系統會以下列其中一種方式決定位置：

* 要求中參照的資料集位置。舉例來說，如果查詢參照了儲存在 `asia-northeast1` 區域的資料集中的資料表或檢視表，查詢工作就會在 `asia-northeast1` 執行。
* 要求中參照的連線指定區域。
* 目的地資料表的位置。

如果未明確指定位置，且無法從要求中的資源判斷，則會使用預設位置。如未設定預設位置，工作會在 `US` 多區域執行。

## 資料保留

資料集會搭配使用[時間旅行](https://docs.cloud.google.com/bigquery/docs/time-travel?hl=zh-tw#time_travel)和[安全防護期](https://docs.cloud.google.com/bigquery/docs/time-travel?hl=zh-tw#fail-safe)，在短時間內保留已刪除和修改的資料，以便您在需要時復原資料。詳情請參閱「[透過時間旅行和安全防護機制保留資料](https://docs.cloud.google.com/bigquery/docs/time-travel?hl=zh-tw)」。

## 儲存空間計費模式

BigQuery 提供兩種儲存空間計費模式：**邏輯** (未壓縮) 和**實體** (壓縮)。

變更儲存空間計費模式只會變更計量設定，不涉及資料遷移、檔案格式轉換或任何基礎架構變更。資料一律會以相同的壓縮實體格式儲存。變更這項設定不會影響查詢效能、延遲時間，或與其他應用程式 (例如 Looker) 的整合。

所選模式只會決定系統如何根據[儲存空間定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#storage)，衡量儲存位元組並計價：

* **邏輯計費：**根據未壓縮的資料大小計費。這是預設模型。
* **實體計費：**根據磁碟資料的壓縮大小計費。

無論選擇哪種計費模式，資料都會以實體位元組的形式儲存。

您可以在資料集層級設定儲存空間計費模式。如果您在建立資料集時未指定儲存空間計費模式，系統會預設使用邏輯儲存空間計費模式。不過，您可以在建立資料集後[變更其儲存空間計費模式](https://docs.cloud.google.com/bigquery/docs/updating-datasets?hl=zh-tw#update_storage_billing_models)。變更資料集的儲存空間計費模式後，必須等待 14 天才能再次變更。

變更資料集的計費模式後，變更會在 24 小時後生效。變更資料集的計費模式時，長期儲存空間中的任何資料表或資料表分區都不會重設為使用中儲存空間。變更資料集的計費模式不會影響查詢效能和查詢延遲時間。

資料集會使用[時間旅行](https://docs.cloud.google.com/bigquery/docs/time-travel?hl=zh-tw#time_travel)和[安全防護](https://docs.cloud.google.com/bigquery/docs/time-travel?hl=zh-tw#fail-safe)儲存空間來保留資料。如果採用實體儲存空間計費模式，系統會按照使用中儲存空間費率，另外收取時間旅行和防故障儲存空間的費用。如果採用邏輯儲存空間計費模式，則會按照基本費率收取費用。您可以修改資料集的時間回溯時間範圍，在實體儲存空間費用和資料保留之間取得平衡。您無法修改安全防護時間範圍。如要進一步瞭解資料集資料保留，請參閱「[使用時間旅行和防故障功能保留資料](https://docs.cloud.google.com/bigquery/docs/time-travel?hl=zh-tw)」。如要進一步瞭解如何預測儲存空間費用，請參閱「[預測儲存空間費用](https://docs.cloud.google.com/bigquery/docs/information-schema-table-storage?hl=zh-tw#forecast_storage_billing)」。

如果貴組織在資料集所在區域有任何現有的舊版[固定費率運算單元承諾使用合約](https://docs.cloud.google.com/bigquery/docs/reservations-commitments-legacy?hl=zh-tw)，就無法將資料集註冊至實體儲存空間計費模式。這項規定不適用於透過 [BigQuery 版本](https://docs.cloud.google.com/bigquery/docs/editions-intro?hl=zh-tw)購買的承諾使用合約。

## 外部資料集

除了 BigQuery 資料集，您也可以建立外部資料集，也就是外部資料來源的連結：

* [Spanner 外部資料集](https://docs.cloud.google.com/bigquery/docs/spanner-external-datasets?hl=zh-tw)
* [AWS Glue 聯合資料集](https://docs.cloud.google.com/bigquery/docs/glue-federated-datasets?hl=zh-tw)

*外部資料集*也稱為*聯合資料集*，這兩個詞彙可交替使用。

建立後，外部資料集會包含參照外部資料來源的資料表。這些資料表中的資料不會複製到 BigQuery，但每次使用時都會查詢。詳情請參閱「[Spanner 聯合查詢](https://docs.cloud.google.com/bigquery/docs/spanner-federated-queries?hl=zh-tw)」。

## 限制

BigQuery 資料集有下列限制：

* [資料集位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)只能在建立時設定。資料集建立後即無法變更位置。
* 查詢中參照的所有資料表，都必須儲存在相同位置的資料集中。
* 外部資料集不支援資料表到期、副本、時間旅行、預設定序、預設捨入模式，或啟用/停用不區分大小寫資料表名稱的選項。
* [複製資料表](https://docs.cloud.google.com/bigquery/docs/managing-tables?hl=zh-tw#copy-table)時，包含來源資料表和目的地資料表的資料集必須位於相同位置。
* 每個專案的資料集名稱皆不得重複。
* 變更資料集的[儲存空間計費模式](#dataset_storage_billing_models)後，必須等待 14 天才能再次變更。
* 如果資料集所在區域有任何舊版[固定費率運算單元承諾使用合約](https://docs.cloud.google.com/bigquery/docs/reservations-commitments-legacy?hl=zh-tw)，就無法將資料集註冊至實體儲存空間計費模式。

## 配額

如要進一步瞭解資料集配額和限制，請參閱[配額和限制](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#dataset_limits)。

## 定價

您不需為建立、更新或刪除資料集付費。

若要深入瞭解 BigQuery 價格，請參閱[價格](https://cloud.google.com/bigquery/pricing?hl=zh-tw)。

## 安全性

如要控管 BigQuery 資料集的存取權，請參閱「[控管資料集的存取權](https://docs.cloud.google.com/bigquery/docs/control-access-to-resources-iam?hl=zh-tw)」。如要瞭解資料加密，請參閱「[靜態資料加密](https://docs.cloud.google.com/bigquery/docs/encryption-at-rest?hl=zh-tw)」。

## 後續步驟

* 參閱[建立資料集](https://docs.cloud.google.com/bigquery/docs/datasets?hl=zh-tw)一文，進一步瞭解如何建立資料集。
* 如要進一步瞭解如何為資料集指派存取控管機制，請參閱「[使用資料集存取控管機制](https://docs.cloud.google.com/bigquery/docs/control-access-to-resources-iam?hl=zh-tw#work_with_dataset_access_controls)」。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-10-29 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-10-29 (世界標準時間)。"],[],[]]