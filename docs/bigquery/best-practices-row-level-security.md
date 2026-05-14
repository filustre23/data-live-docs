Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# BigQuery 資料列層級安全防護的最佳做法

本文將說明使用[資料列層級安全性](https://docs.cloud.google.com/bigquery/docs/row-level-security-intro?hl=zh-tw)的最佳做法。

閱讀本文前，請先參閱「[BigQuery 資料列層級安全防護機制簡介](https://docs.cloud.google.com/bigquery/docs/row-level-security-intro?hl=zh-tw)」和「[使用資料列層級安全防護機制](https://docs.cloud.google.com/bigquery/docs/managing-row-level-security?hl=zh-tw)」，瞭解資料列層級安全防護機制。

## 設計資料列存取政策時的注意事項

在資料表上設定資料列存取政策時，您至少需要兩項資料列存取政策：

* 授予資料表存取權的政策。第一個資料列存取權政策應授予使用者和群組存取權，讓他們能完整存取資料表中的資料，以進行資料維護或支援。舉例來說，BigQuery 管理員和使用 DML 陳述式轉換資料表資料的服務帳戶。
* 第二項政策會根據商業邏輯使用篩選器，並授予特定群組。

如要進一步瞭解如何設定資料列存取權政策，請參閱「[建立或更新資料列層級存取權政策](https://docs.cloud.google.com/bigquery/docs/managing-row-level-security?hl=zh-tw#create_or_update_a_row-level_access_policy)」。

## 測試具有資料列存取政策的服務帳戶

您可以使用服務帳戶模擬功能，測試系統如何套用資料列存取政策。如要使用服務帳戶測試資料列存取權政策，請按照下列步驟操作：

1. [建立服務帳戶](https://docs.cloud.google.com/iam/docs/service-account-overview?hl=zh-tw#locations)。
2. [更新資料列存取政策](https://docs.cloud.google.com/bigquery/docs/managing-row-level-security?hl=zh-tw#create-policy)，授予服務帳戶存取權。或者，將服務帳戶新增至 Google 群組，並透過資料列存取權政策授予存取權。
3. 使用[服務帳戶模擬](https://docs.cloud.google.com/iam/docs/service-account-impersonation?hl=zh-tw)功能，驗證列存取權政策是否正常運作。

## 限制使用者權限，防範側通道攻擊

**最佳做法：**請勿將敏感權限授予只應查看篩選資料的使用者。

側通道攻擊是一種安全攻擊，根據從系統本身取得的資訊發動。如果攻擊者擁有的權限超出必要範圍，就能發動旁路攻擊，並透過**觀察**或**搜尋**帳單、記錄或系統訊息，取得私密資料。

為減少這類機會，BigQuery 會隱藏針對具有資料列層級安全防護機制的資料表執行的所有查詢，當中包含的敏感統計資料。這些敏感統計資料包括處理的位元組數和分割區數、計費的位元組數，以及查詢計畫階段。

*建議管理員不要將下列權限授予只應查看篩選後資料的使用者，以免他們存取敏感資料。*

| **權限** | **機密資料** |
| --- | --- |
| 專案擁有者 | 專案擁有者只能在稽核記錄中查看處理的位元組數和相關資料。您無法從工作詳細資料查看帳單中繼資料。沒有特定權限或角色可授予檢視者存取這項帳單中繼資料的權限。 |
| BigQuery 資料編輯者、擁有者或檢視者角色 | 查看查詢的錯誤訊息。 |
| Cloud Billing 檢視者權限 | 查看 BigQuery 帳單。 |

**範例**

* 透過重複**觀察**查詢資料表時的查詢時間，使用者可以推斷出受列層級存取政策保護的資料列值。這類攻擊需要針對分割或叢集資料欄中的一系列鍵值，進行多次重複嘗試。即使觀察或測量查詢時間時存在固有雜訊，攻擊者仍可透過重複嘗試，取得可靠的估計值。*如果對這個保護層級有疑慮，建議您改用不同的資料表，隔離具有不同存取控管規定的資料列。*
* 攻擊者可以監控查詢工作超出限制 (例如計費位元組上限或自訂費用控制項) 時發生的錯誤，**搜尋**查詢處理的位元組。不過，這類攻擊需要大量查詢。
* 透過重複查詢並**觀察** Cloud Billing 中的 BigQuery 帳單金額，使用者可以推斷出受資料列層級存取政策保護的資料列值。這類攻擊需要針對分割或叢集資料欄中的一系列鍵值，進行多次重複嘗試。*如果您對這類保護措施很敏感，建議限制查詢的帳單資料存取權。*

*此外，我們也建議管理員監控 Cloud 稽核記錄(/bigquery/docs/reference/auditlogs)，查看含有資料列層級安全性的資料表是否有可疑活動，例如意外新增、修改及刪除資料列層級存取政策。*

## 限制使用者權限，避免資料遭到竄改

**最佳做法：**請勿將資料表寫入權限授予只應查看篩選資料的使用者。

具備資料表寫入權限的使用者可以透過 [`bq load` 指令](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_load)或 BigQuery Storage Write API，將資料插入資料表。這可能會導致具有寫入權限的使用者變更其他使用者的查詢結果。

*建議管理員為資料表寫入存取權和列層級存取政策建立個別的 Google 群組。如果使用者只能查看經過篩選的資料表結果，就不應具備經過篩選的資料表寫入權限。*

## 重新建立資料列層級存取政策時，避免發生非預期的存取行為

**最佳做法：**如果資料表只有一項資料列層級存取權政策，請勿使用 `CREATE OR REPLACE` 指令重新建立該政策。請先使用資料表存取權控制選項移除資料表的所有存取權，視需要重新建立政策，然後重新啟用存取權。

首次在資料表上新增資料列存取權政策時，系統會立即開始篩選查詢結果中的資料。移除資料表的最後一項資料列層級存取權政策時，即使您只打算重新建立資料列層級存取權政策，也可能會不慎授予未經過濾的存取權給超出預期的對象。

*建議管理員按照下列準則，在資料表上重新建立最後一個資料列層級存取權政策時，特別留意：*

1. 首先，使用[資料表存取權控制項](https://docs.cloud.google.com/bigquery/docs/control-access-to-resources-iam?hl=zh-tw)移除資料表的所有存取權。
2. 移除所有資料列層級的存取權政策。
3. 重新建立資料列層級存取政策。
4. 重新啟用資料表的存取權。

或者，您也可以先在資料表上建立新的資料列層級存取權政策，
然後刪除不再需要的舊政策。

## 僅在機構內使用資料列層級安全性，而非跨機構使用

**最佳做法：**僅在貴機構內使用資料列層級安全性。

請勿跨機構使用資料列層級安全性功能，以免透過側通道攻擊造成資料外洩，並維持對機密資料存取權的更高控管權。

如果是子查詢資料列層級存取權政策，請在機構或專案中建立及搜尋資料表。這樣一來，受讓人必須在政策中的目標和參照資料表上擁有 `bigquery.tables.getData` 權限，以及任何相關的[資料欄層級安全性](https://docs.cloud.google.com/bigquery/docs/column-level-security-intro?hl=zh-tw)權限，因此可提升安全性並簡化 ACL 設定。

*建議您僅在機構內的安全限制 (例如在機構/企業/公司內共用資料) 使用資料列層級安全功能，而非用於跨機構或公開安全。*

**範例**

在貴機構外部，您對資料存取權的控管程度較低。
在貴機構中，您可以控管哪些使用者有權存取資料表查詢的帳單資訊，這些資料表設有資料列層級的存取權政策。帳單資訊是[旁路攻擊](#limit-side-channel-attacks)的媒介。

## 透過列層級存取權政策管理 `Filtered Data Viewer` 角色

**最佳做法：** `bigquery.filteredDataViewer` 是透過資料列層級存取權政策授予的系統管理角色。只能透過列層級存取權政策管理角色。請勿透過 Identity and Access Management (IAM) 套用角色。

[建立資料列層級存取權政策](https://docs.cloud.google.com/bigquery/docs/managing-row-level-security?hl=zh-tw#create-policy)時，系統會自動將 `bigquery.filteredDataViewer` 角色授予政策中的主體。您只能[使用 DDL 陳述式](https://docs.cloud.google.com/bigquery/docs/managing-row-level-security?hl=zh-tw#examples)，在存取政策中新增或移除主體。

`bigquery.filteredDataViewer` 角色*不得*透過 [IAM](https://docs.cloud.google.com/bigquery/access-control?hl=zh-tw) 授予較高層級的資源，例如資料表、資料集或專案。以這種方式授予角色後，使用者就能查看該範圍內*所有*資料列層級存取權政策定義的資料列，無論預期限制為何。雖然資料列層級存取權政策篩選條件的聯集可能無法涵蓋整個資料表，但這種做法會造成重大安全風險，並破壞資料列層級安全性的目的。

建議您只透過資料列層級存取權政策管理 `bigquery.filteredDataViewer` 角色。這個方法可確保主體隱含且正確地獲得 `bigquery.filteredDataViewer` 角色，並遵守各項政策定義的篩選條件述詞。

## 篩選分區資料欄對效能的影響

**最佳做法：**盡量避免建立以叢集和分區資料欄為篩選條件的資料列存取權政策。

資料列層級存取權政策篩選器不會參與[分區和叢集資料表的查詢修剪作業](https://docs.cloud.google.com/bigquery/docs/using-row-level-security-with-features?hl=zh-tw#partitioned_and_clustered_tables)。

如果資料列層級存取權政策指定了分區資料欄，查詢就無法享有查詢修剪的效能優勢。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-14 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-14 (世界標準時間)。"],[],[]]