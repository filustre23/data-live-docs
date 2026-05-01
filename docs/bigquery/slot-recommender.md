* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 查看版本運算單元建議

BigQuery 運算單元建議工具會為[版本](https://docs.cloud.google.com/bigquery/docs/editions-intro?hl=zh-tw)或隨選工作負載建立建議。建議工具會分析查詢工作的歷來運算單元用量，並計算版本承諾運算單元和[自動調度資源](https://docs.cloud.google.com/bigquery/docs/slots-autoscaling-intro?hl=zh-tw)運算單元的最佳成本設定，同時維持類似的效能。運算單元建議工具也會建議可提升效能的最大預留大小。

運算單元建議工具適用於預留運算單元和以量計價的計費方式：

* 在預訂帳單方面，您可以取得 Enterprise 或 Enterprise Plus 版本工作負載的成本最佳化建議，以及預訂項目的效能建議。
* 如果是隨選計費，您可以將一或多個專案轉換為 Enterprise 版，取得整個機構、特定專案或一組專案的隨選工作負載成本最佳化建議。

如要進一步瞭解建議工具服務，請參閱「[建議工具總覽](https://docs.cloud.google.com/recommender/docs/overview?hl=zh-tw)」。

## 成本最佳化建議

運算單元建議工具會根據過去 30 天的運算單元用量，預估自動調度用量。如要進一步瞭解自動調度資源功能，請參閱「[自動調度資源簡介](https://docs.cloud.google.com/bigquery/docs/slots-autoscaling-intro?hl=zh-tw)」。建議工具可以產生多個約期選項，並計算每個選項的總費用。建議工具也可以使用自訂價格，建議總費用最低的選項。建議的承諾和自動調整運算單元數量，是為了涵蓋整個 30 天觀察期內 P99 的運算單元用量。

位置建議工具會針對不同價格類型提供建議，包括隨用隨付 (無承諾)、1 年和 3 年承諾。並根據自訂價格顯示各選項的每月費用。

最佳化建議包含下列詳細資料：

* 基準承諾使用運算單元：為達到最佳成本效益，且不影響效能的承諾使用運算單元數量。選取「查看最佳承諾」，即可在上方的使用情形圖表中查看最佳承諾。
* 基準承諾使用每月費用：最佳承諾使用方案的每月費用，是根據自訂版本承諾使用價格計算。一個月定義為 730 小時。
* 自動調度運算單元：一次使用的自動調度運算單元數量上限。這代表自動調度資源涵蓋的最佳承諾運算單元以外的額外運算單元。這個值不含承諾或基準時段。
* 自動調度資源的預期使用率：自動調度資源運算單元的預期每月使用率，計算方式為預期使用的自動調度資源運算單元除以自動調度資源運算單元上限。
* 自動調度資源每月費用：使用預期自動調度資源運算單元數量的每月費用，以自訂自動調度資源價格計算。
* 每月總費用：每月總費用，包括承諾每月費用和自動調度資源每月費用。

### 套用建議的最佳做法

**注意：** 我們提供的建議是根據歷來資料而定，實際結果可能因工作負載的具體特徵而異。

1. 請確保版本中所有預留項目的基準運算單元總數，小於或等於承諾運算單元數。確保自動調度運算單元可因應任何超過承諾運算單元的用量。如果基準運算單元超出承諾使用運算單元，系統會針對額外的基準運算單元向您收費。
2. 系統會選擇設定中的自動調度資源功能，確保可用容量符合歷史尖峰用量。確保效能不受影響。您也可以將自動調度資源的空位數調低於上限，藉此提高自動調度資源的使用率。不過請注意，如果運算單元用量無法完全涵蓋，可能會影響查詢效能。
3. 如果工作負載出現尖峰，暫時超出最大容量，建議的時段可能會過高。在這種情況下，如果您對目前的成效水準感到滿意，可以考慮維持目前的設定。

即使有時超出設定上限，您也可能會看到 `Slot Estimator doesn't have any recommendations
that would be more effective than your current settings` 訊息。這是因為 BigQuery 有時會暫時超額佈建運算單元，藉此提升查詢速度，且不會產生額外費用。時段建議工具的目標是維持您近期的成效，包括這些爆量情況。如果這個 P99 用量高於目前上限，任何等於或低於目前設定的建議都不符合這些成效等級，因此系統不會建議變更。

### 所需權限

如要查看成本最佳化承諾方案配額建議，您需要下列身分與存取權管理 (IAM) 權限：

* `recommender.bigqueryCapacityCommitmentsRecommendations.get`
* `recommender.bigqueryCapacityCommitmentsRecommendations.list`

下列預先定義的 IAM 角色都包含這些權限：

* `BigQuery Resource Admin`
* `BigQuery Slot Recommender Viewer`
* `BigQuery Slot Recommender Admin`

如要查看版本工作負載的建議，您必須擁有管理專案的列出權限。

如要查看隨選工作負載的專案層級建議，您必須具備專案層級的上述權限。

如要查看一組專案中隨選工作負載的成本最佳化建議，您必須具備機構層級的先前列出權限，以及 `bigquery.jobs.listExecutionMetadata` 或 `bigquery.jobs.listAll` 權限。

如要查看隨選工作負載的機構層級建議，您必須具備機構層級的先前列出權限。您也需要 `resourcemanager.organizations.get` 權限。`Organization
Viewer` IAM 角色具備這項權限。

在建議設定中，您會看到「基準承諾使用合約配額」和「每月總費用」等資料列，但每月費用詳細資料的值會隱藏。如要查看隱藏值，您還需要下列權限：

* `billing.accounts.getPricing`

下列預先定義的 IAM 角色都包含這些權限：

* `Billing Account Viewer`
* `Billing Account Administrator`

如要處理版本工作負載，您必須在與管理員專案相關聯的帳單帳戶中，擁有先前列出的權限。如要查看專案層級的隨選工作負載，您需要與專案相關聯的帳單帳戶權限，如要查看機構層級的建議，則需要機構層級的權限。

如要進一步瞭解 BigQuery 中的 IAM 角色，請參閱[預先定義的角色與權限](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)一文。

## 提升成效的建議

選取特定預留項目工作負載時，運算單元建議工具會建議可提升工作效能的預留項目大小上限。接著，運算單元估算器會分析[運算單元模擬](https://docs.cloud.google.com/bigquery/docs/slot-estimator?hl=zh-tw#model_slot_performance)資料，找出可將工作效能提升至少 5% 的最大預留項目大小，並計算出最低增量值。如果目前的預訂大小上限符合您過去的需求，系統就不會提供建議。

**注意：** 建議是根據歷來資料提供。工作效能可能會因實際使用情形而異。

如要套用最佳化建議，請按一下「套用」，系統會將您重新導向至可更新預訂的頁面。

## 事前準備

如要查看建議，請先[啟用 Recommender API](https://docs.cloud.google.com/recommender/docs/enabling?hl=zh-tw)。如要在Google Cloud 控制台中查看建議，您也必須[啟用 Reservations API](https://docs.cloud.google.com/bigquery/docs/reservations-commitments?hl=zh-tw#enabling-reservations-api)。

### 所需權限

如要取得預訂成效改善建議，運算單元建議工具需要您在管理專案中具備下列 IAM 權限：

* `bigquery.reservations.list`
* `bigquery.reservationAssignments.list`
* `bigquery.capacityCommitments.list`

如要將建議的更新套用至預留項目，您也必須在管理專案中具備下列 IAM 權限：

* `bigquery.reservations.update`

如要進一步瞭解 BigQuery 中的 IAM 角色，請參閱[預先定義的角色與權限](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)一文。

## 定價

這項建議工具會顯示在[版位預估工具](https://docs.cloud.google.com/bigquery/docs/slot-estimator?hl=zh-tw)的環境中。您可以免費使用建議。

## 查看運算單元建議

如要使用 Google Cloud 控制台查看建議的配額，請執行下列步驟。

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 如要取得版本工作負載建議，請選取管理員專案。如要取得隨選工作負載建議，請選取機構內符合預先定義需求的任何專案。
3. 如果是隨選工作負載，只要具備機構層級的權限，就能在側邊面板選項中選取任何個別專案或整個機構，查看特定範圍的建議。
4. 在導覽選單中，按一下「容量管理」。
5. 按一下「運算單元估算工具」分頁標籤。
6. 在「來源」窗格中，選取隨選工作負載或版本 (Enterprise 或 Enterprise Plus) 工作負載。

   * 如果您選取版本工作負載，詳細建議會顯示在歷來用量圖表下方。
   * 如果選取隨選工作負載，機構管理員就能在機構層級和專案層級之間切換 (適用於一或多個專案)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-04-30 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-04-30 (世界標準時間)。"],[],[]]