Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 建立自訂查詢配額

本文說明如何設定或修改自訂查詢配額，以控管費用。如要瞭解 BigQuery 分析師如何估算及控管費用，請參閱「[估算及控管費用](https://docs.cloud.google.com/bigquery/docs/best-practices-costs?hl=zh-tw)」。

如果您同時擁有多個 BigQuery 專案和使用者，則可以提出自訂配額要求並指定每日處理的資料量上限，藉此達到管控成本的目的。系統會在太平洋時間凌晨 12 點重設每日配額。

自訂配額會主動發揮作用，因此如果配額為 10 TB，您就無法執行資料量為 11 TB 的查詢作業。為處理的資料量建立自訂配額之後，您就能掌控專案層級或使用者層級的費用。

如要設定自訂成本控制項，請更新下列一或兩項查詢配額：

* `QueryUsagePerDay`：專案層級的自訂配額會限制同一專案中所有使用者的匯總用量。
* `QueryUsagePerUserPerDay`：使用者層級的自訂配額會分別套用至專案中的所有使用者和[服務帳戶](https://docs.cloud.google.com/docs/authentication?hl=zh-tw#user_accounts_and_service_accounts)。無論每位使用者的限制為何，專案中所有使用者的總用量絕不會超過每日查詢用量限制。

**注意：** 您無法為個別使用者或服務帳戶指派自訂配額。

`QueryUsagePerDay` 配額的預設限制為每項專案每天處理 200 Tebibytes (TiB) 的資料。`QueryUsagePerUserPerDay` 的預設限制為無限制。如要查看目前的限制，請參閱[配額頁面](https://console.cloud.google.com/iam-admin/quotas?metric=bigquery.googleapis.com%2Fquota%2Fquery%2Fusage&hl=zh-tw)。你隨時可以[變更限制](#set-custom-quotas)，自訂覆寫會取代預設限制。

查詢用量配額僅適用於[隨選查詢定價模式](https://cloud.google.com/bigquery/pricing?hl=zh-tw#on_demand_pricing)。

如要進一步瞭解可設定的 BigQuery 配額，請參閱「[配額與限制](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)」。

## 必要角色

如要取得變更配額所需的權限，請要求管理員授予您專案的配額管理員 (`role/servicemanagement.quotaAdmin`) IAM 角色。如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和機構的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

這個預先定義的角色具備  `serviceusage.quotas.update` 權限，可變更配額。

您或許還可透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)取得這項權限。

## 設定或修改自訂配額

您可以為 Google Cloud 控制台「配額與系統限制」頁面顯示的任何配額，設定自訂配額或修改現有配額。要求調降配額時，變更會在幾分鐘內生效。如果您要求提高配額，系統會進行核准程序，這可能需要較長時間。詳情請參閱「[要求調整配額](https://docs.cloud.google.com/docs/quotas/help/request_increase?hl=zh-tw)」。

**附註：**自訂配額為約略值。自訂配額功能提供額外的防護機制，可預防費用超額，但無法嚴格限制系統的資料處理量，因此在某些情況下，BigQuery 可能會執行超過配額的查詢作業。如要確保價格一致性，建議使用[預訂](https://docs.cloud.google.com/bigquery/docs/reservations-intro?hl=zh-tw)。

如要設定或更新自訂費用控管機制，例如限制每天可處理的 BigQuery 資料量，請按照下列步驟操作：

1. 在 Google Cloud 控制台，依序開啟「IAM 與管理」>「配額與系統限制」頁面：

   [前往「配額與系統限制」](https://console.cloud.google.com/iam-admin/quotas?hl=zh-tw)
2. 在「篩選器」搜尋框中使用「服務」篩選器，篩選出 BigQuery API。
3. 選取要調整的配額。舉例來說，如要限制專案和使用者層級的每日查詢資料量，請選取「每日查詢次數」和「每人每天查詢次數」。你可能需要捲動清單才能找到這些項目。選取配額後，工具列會隨即顯示。
4. 按一下工具列中的「編輯」edit。
   「Quota changes」(配額變更) 對話方塊隨即開啟。
5. 如果選取「無限制」，請取消選取。
6. 在「New value」(新值) 欄位輸入所需的配額值 (以 TiB 為單位)。
7. 按一下 [完成]。
8. 按一下 [提交要求]。

如要進一步瞭解如何查看及管理配額，請參閱「[查看及管理配額](https://docs.cloud.google.com/docs/quotas/view-manage?hl=zh-tw)」。

**注意：** 查詢用量是累計的計費位元組數。如果部分查詢的收費費率高於一般[以量計價方案](https://cloud.google.com/bigquery/pricing?hl=zh-tw#on_demand_pricing)，則「配額與系統限制」頁面上的查詢用量值，可能與從[`INFORMATION_SCHEMA.JOBS`檢視畫面](https://docs.cloud.google.com/bigquery/docs/information-schema-jobs?hl=zh-tw)取得的相同期間計費位元組數不符。舉例來說，一般查詢的以量計價價格可能為每 TiB X 美元，但建立邏輯迴歸模型等其他查詢作業的價格可能為每 TiB 50X 美元，是正常價格的 50 倍。在這個情況下，`INFORMATION_SCHEMA.JOBS` 檢視畫面可能會傳回 100 GiB 的計費位元組，但「配額和系統限制」頁面顯示的查詢用量會是 5 TiB，是前者的 50 倍，因為查詢用量值會根據一般隨選價格進行標準化。

## 傳回的錯誤訊息

設定自訂配額之後，如果您超過該上限，BigQuery 就會傳回錯誤訊息：

* 如果您超過專案層級的自訂配額，BigQuery 會傳回 [`usageQuotaExceeded`](https://docs.cloud.google.com/bigquery/troubleshooting-errors?hl=zh-tw#quotaExceeded) 錯誤：

  ```
  Custom quota exceeded: Your usage exceeded the custom quota for
  QueryUsagePerDay, which is set by your administrator. For more information,
  see https://cloud.google.com/bigquery/cost-controls
  ```
* 如果使用者超過使用者層級的自訂配額，BigQuery 會傳回 [`usageQuotaExceeded`](https://docs.cloud.google.com/bigquery/troubleshooting-errors?hl=zh-tw#quotaExceeded) 錯誤，但訊息內容不同：

  ```
  Custom quota exceeded: Your usage exceeded the custom quota for
  QueryUsagePerUserPerDay, which is set by your administrator. For more
  information, see https://cloud.google.com/bigquery/cost-controls
  ```

您可以透過其他專案執行查詢作業，不過前提是該項專案可存取您的資料集，並且沒有設定自訂配額或尚未超過配額上限。

## 範例

假設您已為包含 10 名使用者的專案設定下列自訂配額，且其中一名使用者為服務帳戶：

* 專案層級：每日 50 TB
* 使用者層級：每日 10 TB

專案層級的自訂配額會限制同一專案中所有使用者的匯總用量。使用者層級的自訂配額會分別套用至單一專案中的每個使用者或[服務帳戶](https://docs.cloud.google.com/docs/authentication?hl=zh-tw#user_accounts_and_service_accounts)。

下表說明 10 位使用者在單日內執行完所需查詢後的剩餘配額。

| 用量 | 剩餘配額 |
| --- | --- |
| 10 位使用者的查詢量各為 4 TB | **專案層級**：剩餘 10 TB。  **使用者層級**：每位使用者各剩餘 6 TB，但總計最多只能再使用 10 TB。 |
| 服務帳戶使用了另外的 6 TB 查詢量 | **專案層級**：剩餘 4 TB。  **使用者層級**：服務帳戶無法繼續使用 BigQuery。其他使用者各剩餘 6 TB，但總計最多只能再使用 4 TB。 |
| 1 名使用者使用了另外的 4 TB 查詢量 | **專案層級**：剩餘 0 TB。  **使用者層級**：每位使用者剩餘的 TB 數各不相同。不過由於已超出專案層級的配額上限，因此所有使用者均不得使用 BigQuery。 |

由於已無剩餘配額，該項專案中的每位使用者都無法繼續使用 BigQuery。

## 後續步驟

* 瞭解 [BigQuery 定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw)。
* 瞭解如何[估算及控管費用](https://docs.cloud.google.com/bigquery/docs/best-practices-costs?hl=zh-tw)。
* 瞭解如何分析 [BigQuery 稽核記錄](https://docs.cloud.google.com/bigquery/docs/introduction-audit-workloads?hl=zh-tw)，監控查詢費用和 BigQuery 用量。
* 如要瞭解帳單、快訊和資料視覺化，請參閱下列主題：

  + [建立、編輯或刪除預算和預算快訊](https://docs.cloud.google.com/billing/docs/how-to/budgets?hl=zh-tw)
  + [將 Cloud Billing 資料匯出至 BigQuery](https://docs.cloud.google.com/billing/docs/how-to/export-data-bigquery?hl=zh-tw)
  + [透過數據分析以圖表呈現您的費用](https://docs.cloud.google.com/billing/docs/how-to/visualize-data?hl=zh-tw)




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-05 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-05 (世界標準時間)。"],[],[]]