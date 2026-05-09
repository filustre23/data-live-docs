Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 在 BigQuery 中使用政策標記的最佳做法

本頁面說明在 BigQuery 中使用政策標記的最佳做法。使用政策標記定義資料的存取權，適用於[資料欄層級存取控管](https://docs.cloud.google.com/bigquery/docs/column-level-security-intro?hl=zh-tw)或[動態資料遮蓋](https://docs.cloud.google.com/bigquery/docs/column-data-masking-intro?hl=zh-tw)。

如要瞭解如何為資料欄設定政策標記，請參閱「[為資料欄設定政策標記](https://docs.cloud.google.com/bigquery/docs/column-level-security?hl=zh-tw#set_policy)」。

## 建構資料類別的階層

建立符合業務需求的資料類別階層。

首先，請考量機構處理的資料類型。通常組織管理少量資料類別。舉例來說，機構組織可能會有下列資料類別：

* PII 資料
* 財務資料
* 查看客戶訂單記錄

您可以使用政策標記，將單一資料類別套用至多個資料欄。您應善用這個抽象層級，只使用少數政策標記，就能有效管理多個資料欄。

其次，請考慮是否有需要不同資料類別存取權的群組。舉例來說，某個群組需要存取業務機密資料，例如收益和顧客記錄。另一個群組需要存取電話號碼和地址等個人識別資料 (PII)。

請注意，您可以在樹狀結構中將政策標記分組。有時建立包含所有其他政策標記的根政策標記，會很有幫助。

下圖為分類範例。這個階層會將所有資料類型分組，歸入三個頂層政策標記：**高**、**中**和**低**。

每個頂層政策標記都包含葉節點政策標記。舉例來說，「高」政策標記包含「信用卡」、「政府核發的身分證件」和「生物特徵辨識」政策標記。**中**和**低**也同樣有葉子政策標記。

這種結構有以下幾個優點：

* 您可以一次授予整個政策標記群組的存取權。舉例來說，您可以在「低」層級授予「Data Catalog 精細讀取者」角色。
* 您可以將政策標記從一個層級移至另一個層級。舉例來說，您可以將「地址」從「低」層級移至「中」層級，進一步限制存取權，不必重新分類所有「地址」欄。

  **注意：** 您只能透過 Data Catalog `PolicyTagManager.UpdatePolicyTag` 方法移動政策標記。
* 有了這項精細的存取權，您只需控管少數資料分類政策標記，就能管理多個資料欄的存取權。

如要進一步瞭解 BigQuery 中的政策標記，請參閱：

* [資料欄層級存取控管機制簡介](https://docs.cloud.google.com/bigquery/docs/column-level-security-intro?hl=zh-tw)
* [透過資料欄層級存取控管機制限制存取權](https://docs.cloud.google.com/bigquery/docs/column-level-security?hl=zh-tw)
* [動態資料遮蓋簡介](https://docs.cloud.google.com/bigquery/docs/column-data-masking-intro?hl=zh-tw)
* [依使用者角色遮蓋資料欄](https://docs.cloud.google.com/bigquery/docs/column-data-masking?hl=zh-tw)




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-08 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-08 (世界標準時間)。"],[],[]]