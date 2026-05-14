Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 舊版容量承諾使用價格方案

**注意：** 只有許可清單中的客戶可以使用舊版預訂，包括存取固定費率帳單或特定承諾期。如要確認您是否能使用這些舊版功能，請與管理員聯絡。固定費率計費模式會定義運算資源的計費方式，但固定費率預訂和承諾方案的功能與 Enterprise 版的配額相同。

BigQuery 提供下列運算資源承諾方案：

* [彈性運算單元使用承諾](#flex_slots)
* [每月承諾使用合約](#monthly-commitments)
* [年度承諾](#annual-commitments)

最小的使用承諾大小為 100 個運算單元，且使用承諾以 100 個運算單元為增量單位，上限為[運算單元配額](https://docs.cloud.google.com/bigquery/docs/slots?hl=zh-tw#slot_quotas_and_limits)。
可建立的約定數量沒有上限。從您成功購買使用承諾的時刻起，系統就會開始計費。如要瞭解 BigQuery 費用，請參閱 [BigQuery 定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw)。

**注意：** 採用以量計價方案的客戶通常享有 2,000 個以上的運算單元可進行查詢處理。配置 100 個運算單元可能會導致查詢效能降低。

如要進一步瞭解容量承諾和預留項目，請參閱「[預留項目簡介](https://docs.cloud.google.com/bigquery/docs/reservations-intro?hl=zh-tw)」。

購買與 [BigQuery 版本](https://docs.cloud.google.com/bigquery/docs/editions-intro?hl=zh-tw)相關聯的運算單元時，可選擇是否購買容量承諾使用合約，但購買這類合約可節省費用。

### 彈性運算單元承諾使用方案

彈性運算單元是購買 BigQuery 容量的一種方式，最短購買時間為 **60 秒**。購買彈性運算單元承諾後，您可以在承諾生效 60 秒後刪除承諾。這項服務會以秒為單位計費。您可以將彈性時段承諾方案轉換為[月](#monthly-commitments)或[年](#annual-commitments)承諾方案。

舉例來說，如果您在下午 6 點購買使用承諾，系統會立即開始計費。您可以在承諾開始後的 60 秒內刪除承諾 (即下午 6 點 01 分)，這會產生 60 秒的計費用量。系統會針對承諾的有效時間以秒計費。

## 每月承諾使用方案

**注意：** 我們已在 2023 年 8 月停止支援月約方案，並將月約方案轉換為年約方案或基本位置。如要進一步瞭解承諾和續約，請參閱「[Slot 承諾](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#slot_commitments)」一文。

## 年約方案

如果採用年約方案，您須支付指定數量配額的一年費用，之後則以秒計費。方案到期後，您可以隨時刪除承諾，或繼續根據續約方案的條件付款。

續約方案是指年約到期後生效的容量使用承諾方案。

### 續訂年約方案

購買年約方案或將其他方案轉換為年約方案時，您會選擇續約方案。您可以在年約到期前隨時變更續約方案。

如果採用固定費率容量模式，您可以在方案到期前變更續約方案，選擇下列其中一種做法：

* **無。**365 天後，方案就會到期且不會續訂。系統會移除該項目。
* **每月。**365 天後，承諾期會改為每月承諾。系統會按月費率收費，您可以在 30 天後刪除承諾。
* **Flex。**365 天後，您的承諾會轉換為彈性時段承諾。系統會按照彈性運算單元費率收費，且您隨時可以刪除承諾。
* **按年**。365 天後，承諾將續約一年。

**注意：** 自 2023 年 7 月 5 日起，BigQuery 客戶將無法再購買固定費率年約、固定費率月約和彈性配額承諾。詳情請參閱 [BigQuery 計價方式](https://cloud.google.com/bigquery/pricing?hl=zh-tw#flat-rate_compute_analysis_pricing)。

如果不是採用固定費率運算能力模式，如要瞭解如何購買及續約承諾使用合約，請參閱「[建立運算能力承諾使用合約](https://docs.cloud.google.com/bigquery/docs/reservations-commitments?hl=zh-tw#create_a_capacity_commitment)」。

舉例來說，假設您在 2019 年 10 月 5 日下午 6 點購買年約，系統會立即開始計費。承諾到期或續約時間為 2020 年 10 月 4 日下午 6 點後 (2020 年為閏年)。

* 如果選擇續約為月約方案，使用承諾會在 2020 年 10 月 4 日下午 6 點轉換為月約方案。系統會按照月費率向您收費，且月費續訂方案生效後 30 天內，您無法刪除使用承諾。
* 如果您選擇續約彈性配額使用承諾，則您的使用承諾會在 2020 年 10 月 4 日下午 6 點轉換為彈性配額使用承諾。系統會以彈性運算單元費率計費，您可以在 60 秒後刪除承諾。
* 如果您選擇每年續約，則您的使用承諾會在 2020 年 10 月 4 日下午 6 點整續約一年。

### 過期的承諾使用合約

如果採用固定費率使用承諾，除非指定續約方案，否則承諾到期後就會移除。為確保您不會失去任何容量，系統會將額外運算單元移至名為 `system-created-Enterprise` 的系統建立保留項目基準。承諾到期後，帳單會包含以下三部分：

1. 剩餘承諾。
2. 剩餘承諾使用合約未涵蓋的基準運算單元。
3. 自動調度資源功能管理的調度資源運算單元。

以下情境說明承諾到期後會發生什麼情況：

#### 情境 1：承諾用量等於基準用量總計

您有一個即將到期的承諾 (100 個運算單元)，以及一個保留項目 (100 個基準運算單元)。

系統會移除 100 個配額，並根據 100 個配額的基準費用向您收費。

#### 情境 2：承諾用量大於總基準用量

您有一個即將到期的承諾，內含 200 個運算單元，以及一個含有 100 個基準運算單元的預留項目。

系統會移除 200 個時段，並建立 `system-created-Enterprise`，其中包含 100 個基本時段。系統會根據 200 個基準運算單元的總數向您收費。

#### 情境 3：使用每年固定費率續約方案的承諾

您有一項年約固定費率承諾，內含 100 個時段，並採用年約固定費率續訂方案，即將到期。

這 100 個名額會移至 Enterprise 年約方案，並採用年約續訂方案。

## 刪除承諾使用合約

建立承諾產品之後，只能在承諾產品到期後刪除。

如要刪除年約方案，請將續約方案設為彈性運算單元。年約到期並續約為彈性運算單元使用承諾後，您就可以刪除年約。

如需如何刪除承諾使用設定的操作說明，請參閱「[承諾使用期限](https://docs.cloud.google.com/bigquery/docs/reservations-commitments?hl=zh-tw#commitment_expiration)」一文。

如果您意外購買了承諾產品或錯誤設定了承諾產品，請與 [Cloud 帳單支援團隊](https://docs.cloud.google.com/support/billing?hl=zh-tw)聯絡取得協助。

## 後續步驟

* 瞭解[預訂、限制、配額和價格](https://docs.cloud.google.com/bigquery/docs/reservations-intro?hl=zh-tw)。
* 瞭解[時段](https://docs.cloud.google.com/bigquery/docs/slots?hl=zh-tw)。
* 瞭解如何[購買及管理運算單元容量](https://docs.cloud.google.com/bigquery/docs/reservations-commitments?hl=zh-tw)。
* 瞭解 [BigQuery 版本](https://docs.cloud.google.com/bigquery/docs/editions-intro?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-14 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-14 (世界標準時間)。"],[],[]]