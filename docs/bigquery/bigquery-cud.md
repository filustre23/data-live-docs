Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [資源](https://docs.cloud.google.com/bigquery/docs/release-notes?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 承諾使用折扣

**重要事項：**本頁說明 BigQuery 隨用隨付容量的承諾用量折扣。如要瞭解其他 Google Cloud CUD，請參閱「[承諾使用折扣](https://docs.cloud.google.com/billing/docs/resources/multiprice-cuds?hl=zh-tw)」。

本頁面說明以支出為準的承諾使用折扣 (CUD) 如何與 BigQuery 搭配使用。

BigQuery 支援兩種不同的承諾：

* [容量承諾](https://cloud.google.com/bigquery/pricing?hl=zh-tw#capacity_compute_analysis_pricing)：承諾在管理專案中購買特定數量的版位和版本。
* 根據支出而定的承諾，詳情請參閱本頁。

## BigQuery 支出型 CUD

以支出為基礎的 BigQuery CUD 可提供折扣價，以換取您承諾在特定區域使用 BigQuery 容量。

* **10% 折扣**：只要承諾訂閱 1 年，即可享有這項優惠。在合約期間，您需支付 BigQuery CUD 1 年期價格 (計費模式 ID：DD83-D9A3-79AF)，做為每小時的承諾支出金額。
* **20% 折扣**：承諾使用 3 年即可享有此折扣。在合約期間，您需支付 BigQuery CUD 3 年期價格 (計費模式 ID 4D8D-49A7-C5B1)，做為每小時的承諾支出金額。

BigQuery 依支出計算的 CUD 非常適合每小時支出可預測的工作負載。您承諾在一年或三年的期限內，每小時支出一定金額。做為回報，您可享有 BigQuery SKU 的折扣費率，適用於承諾用量涵蓋的用量。

您可以透過任何 Cloud Billing 帳戶購買依支出計算的 CUD，適用折扣會套用至 Cloud Billing 帳戶支付費用的專案中，所有符合條件的用量。購買 BigQuery 依支出計算的 CUD 時，即使適用用量的價格變動，您在整個承諾使用合約期間支付的承諾使用費用仍會維持不變。系統會按月收取承諾費用。如果超量，系統會依即付即用費率計費。

**注意**：本文討論部分依支出計算的承諾使用折扣 (CUD)，這些折扣已自動遷移至新的計費模式，也就是使用折扣而非抵免額。 Google Cloud 控制台的「帳單總覽」頁面會顯示通知，指出遷移日期。如要進一步瞭解這些改善措施、受影響的 CUD，以及您需要採取的行動，請參閱「[依支出計算的 CUD](https://docs.cloud.google.com/docs/cuds-multiprice?hl=zh-tw)」。

決定購買依支出計算的 CUD 時，請注意下列事項：

* 區域：您可為個別區域購買依支出計算的 CUD。如果您在多個區域中執行作業，請在每個區域分別計算及購買以支出為準的 CUD。
* 專案：判斷每個專案每小時的隨用隨付運算單元用量是否一致。
* BigQuery 功能：以消費金額為準的 CUD 適用於所有 BigQuery PAYG SKU。

## BigQuery 支出型 CUD 使用類型

系統會自動將以支出為準的 CUD 套用至區域內的 BigQuery 執行個體總用量，讓您享有低廉且可預測的費用，不必手動變更或更新任何項目。這項彈性機制有助於您在承諾使用量內達到高使用率，節省時間和金錢。BigQuery 支出型 CUD 適用於所有 BigQuery 隨用隨付方案的使用量。BigQuery 支出型 CUD 適用於所有支援的運算容量類型，包括：

* BigQuery 版本
* Composer 3 (也稱為 Apache Airflow 適用的 BigQuery 引擎)
* Knowledge Catalog
* BigQuery 服務
* Managed Service for Apache Spark (舊稱 *Dataproc Serverless*)

如需適用 SKU 的完整清單，請參閱「[可使用 BigQuery CUD 的 SKU](https://docs.cloud.google.com/skus/sku-groups/bigquery-cud-eligible-skus?hl=zh-tw)」。

## 購買 BigQuery 支出型 CUD

購買 CUD 後，您就無法取消承諾。請確認承諾使用容量的大小和期限，符合您歷來和預期的 BigQuery 容量最低支出。詳情請參閱「[取消承諾](https://docs.cloud.google.com/docs/cuds-spend-based?hl=zh-tw#canceling_commitments)」。

如要為 Cloud Billing 帳戶購買或管理 BigQuery 預先承諾用量折扣，請按照「[購買以支出為準的承諾](https://docs.cloud.google.com/docs/cuds-spend-based?hl=zh-tw#purchasing)」一文中的操作說明進行。

## 計算依支出計算的 CUD 折扣

以下範例說明如何使用以支出為準的 CUD，計算 BigQuery 的使用費用。

重要注意事項：

* BigQuery 依支出計算的 CUD 僅適用於先前列出的功能，且僅限即付即用容量。
* BigQuery 支出型 CUD 不適用於儲存空間或以量計價。
* BigQuery 依支出計算的 CUD 適用於特定區域的所有即付即用運算單元 SKU。
* BigQuery 依支出計算的 CUD，是以每小時折扣承諾的金額 (以美元為單位) 計算。

在要購買 CUD 的區域計算 BigQuery PAYG 的每小時費率時，請先考量是否能為您省下費用。如果用量超過承諾量，系統會按照標準即付即用價格收費。

舉例來說，假設您在 `us-central1` 區域執行 BigQuery 工作負載，並使用 Enterprise 版的運算單元時數。

請前往 [BigQuery 定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw)頁面，瞭解三年期方案的每小時費用，例如每運算單元小時 $0.036 美元 (可享 8 折優惠)。這就是承諾價格，您承諾在 `us-central1` 的所有專案中，三年內每小時的 BigQuery 支出金額。如果超量，系統會依即付即用費率計費。

在自動帳戶遷移前的舊版 CUD 計畫中，承諾金額是隨選價格。詳情請參閱「[依支出計算的 CUD](https://docs.cloud.google.com/docs/cuds-multiprice?hl=zh-tw)」。

無論實際用量為何，您每年都必須支付最低 $0.036 美元 / 每小時的費用。承諾使用後，即使您決定在承諾使用期間停止或減少每小時用量，仍須支付該金額。

## 定價

BigQuery 提供一年期 10% 的折扣，以及三年期 20% 的折扣，折扣金額以承諾支出為準。如需價格資訊，請洽詢業務代表。

如要進一步瞭解 BigQuery 支出型 CUD 的定價，請參閱 [BigQuery 定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw)。所有區域和多區域均適用上述折扣。

## 後續步驟

* 請參閱「[承諾使用折扣](https://docs.cloud.google.com/docs/cuds-spend-based?hl=zh-tw)」，瞭解如何購買按照支出計算的承諾使用合約。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-06 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-06 (世界標準時間)。"],[],[]]