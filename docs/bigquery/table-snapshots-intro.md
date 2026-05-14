Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 資料表快照簡介

本文將簡介 BigQuery 資料表快照。這是一系列文件的第一篇，說明如何使用 BigQuery 資料表快照，包括如何建立、還原、更新、取得相關資訊及查詢資料表快照。這組文件適用於熟悉 [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw) 和 BigQuery [資料表](https://docs.cloud.google.com/bigquery/docs/tables-intro?hl=zh-tw)的使用者。

## 資料表快照

BigQuery 資料表快照會保留特定時間點的資料表內容 (稱為「基準資料表」)。您可以儲存目前資料表的快照，也可以建立過去七天內任一時間點的資料表快照。資料表快照可以設定到期時間；自建立資料表快照起，經過設定的時間後，BigQuery 就會刪除該快照。您可以查詢資料表快照，就像查詢標準資料表一樣。資料表快照為唯讀，但您可以從資料表快照建立 (*還原*) 標準資料表，然後修改還原的資料表。

使用表格快照的好處包括：

* **保留記錄超過七天。**使用 BigQuery [Time Travel](https://docs.cloud.google.com/bigquery/docs/time-travel?hl=zh-tw) 時，您只能存取七天前或更近的資料表資料。資料表快照可無限期保留特定時間點的資料表資料。
* **盡量降低儲存空間成本。**BigQuery 只會儲存快照與基礎資料表之間不同的位元組，因此資料表快照的儲存空間用量通常會比資料表的完整副本少。

如需資料表的可變動輕量副本，請考慮使用[資料表副本](https://docs.cloud.google.com/bigquery/docs/table-clones-intro?hl=zh-tw)。

## 資料表快照的存取權控管

資料表快照的存取權控管方式與資料表類似。
詳情請參閱「[使用 IAM 控管資源存取權](https://docs.cloud.google.com/bigquery/docs/control-access-to-resources-iam?hl=zh-tw)」。

## 查詢資料表快照

查詢資料表快照的資料時，方法與查詢其他類型的 BigQuery 資料表相同。詳情請參閱「[查詢 BigQuery 資料](https://docs.cloud.google.com/bigquery/docs/query-overview?hl=zh-tw)」。

## 儲存空間費用

資料表快照會產生[儲存空間費用](https://cloud.google.com/bigquery/pricing?hl=zh-tw#storage)，但 BigQuery 只會針對資料表快照中尚未向其他資料表收費的資料收費：

* 建立資料表快照時，一開始不會產生資料表快照的儲存空間費用。
* 如果建立資料表快照後，基礎資料表新增了資料，您就不必支付資料表快照中該資料的儲存空間費用。
* 建立快照時，快照的儲存空間類型會與來源資料的儲存空間類型相同。舉例來說，如果您為分類為動態儲存空間的表格建立快照，該快照的儲存空間類型就是動態。同樣地，如果基礎資料表分類為長期儲存，快照的儲存類型就是長期儲存。
* 如果基礎資料表中的資料經過變更或刪除，且該資料也存在於資料表快照中，系統會收取下列費用：

  + 系統會針對已變更或刪除資料的資料表快照儲存空間計費。
  + 如果系統將基本資料表視為實體儲存空間計費，則不會向基本資料表收取時空旅行和安全防護費用。刪除快照後，系統會收取時空旅行和安全模式的費用。
  + 如果有多個快照包含變更或刪除的資料，系統只會針對最舊快照使用的儲存空間收費。
* 在同一區域內複製資料表快照或複製資料表，或是從一個區域或多個區域複製到另一個區域時，系統會建立資料表的完整副本。這會產生額外的[儲存空間費用](https://cloud.google.com/bigquery/pricing?hl=zh-tw)。

下圖顯示基本資料表和資料表快照儲存空間費用的差異：

**注意：**

* 由於 BigQuery 儲存空間是以資料欄為基礎，因此對基礎資料表中的資料進行小幅變更，可能會導致資料表快照的儲存空間費用大幅增加。
* 如果對基本資料表進行某些變更，系統可能會針對資料表的資料表快照收取全額儲存空間費用。舉例來說，如果您修改具有[叢集](https://docs.cloud.google.com/bigquery/docs/manage-clustered-tables?hl=zh-tw#modifying-cluster-spec)的基本資料表，可能會導致系統自動重新叢集。由於重新叢集化作業可能會重新編寫基本資料表的儲存區塊，因此基本資料表的儲存空間不再與快照的儲存空間相同。這可能會導致系統針對基礎資料表最舊的快照，收取修改後分區的完整儲存空間費用。
* 分區有助於降低表格快照的儲存費用。一般來說，BigQuery 只會複製分區內經過修改的資料，而不是整個資料表快照。

詳情請參閱 [BigQuery 儲存空間定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#storage)一文。

## 限制

* 資料表快照必須與其基本資料表位於相同[區域](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)，且屬於相同[機構](https://docs.cloud.google.com/resource-manager/docs/creating-managing-organization?hl=zh-tw)。如果選取不同區域的資料集，BigQuery 會在該區域的目標資料集中建立資料表副本。
* 資料表快照為唯讀，您無法更新資料表快照中的資料，除非您從快照建立標準資料表，然後更新資料。您只能更新資料表快照的中繼資料，例如說明、到期日和存取政策。
* 由於[時空旅行](https://docs.cloud.google.com/bigquery/docs/time-travel?hl=zh-tw)有七天的限制，您只能擷取七天前或最近的資料表快照。
* 您無法對檢視區塊或具體化檢視區塊建立快照。
* 您無法對[外部資料表](https://docs.cloud.google.com/bigquery/docs/external-tables?hl=zh-tw)建立快照。
* 建立資料表快照時，無法覆寫現有資料表或資料表快照。
* 如果資料表在[寫入最佳化儲存空間 (串流緩衝區)](https://docs.cloud.google.com/bigquery/docs/streaming-data-into-bigquery?hl=zh-tw#dataavailability) 中有資料，則建立快照時不會納入這些資料。
* 如果您為含有[時空旅行](https://docs.cloud.google.com/bigquery/docs/time-travel?hl=zh-tw)資料的資料表建立快照，時空旅行中的資料不會納入資料表快照。
* 如果為已設定[分區到期時間](https://docs.cloud.google.com/bigquery/docs/managing-partitioned-tables?hl=zh-tw#partition-expiration)的分區資料表建立快照，快照不會保留分區到期時間資訊。快照資料表會改用目的地資料集的預設分區到期時間。如要保留分區到期資訊，請改為[複製資料表](https://docs.cloud.google.com/bigquery/docs/managing-tables?hl=zh-tw#copy-table)。

## 配額與限制

如要瞭解資料表快照適用的配額和限制，請參閱「[資料表快照配額和限制](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#table_snapshots)」。

## 後續步驟

* [建立資料表快照](https://docs.cloud.google.com/bigquery/docs/table-snapshots-create?hl=zh-tw)。
* [還原資料表快照](https://docs.cloud.google.com/bigquery/docs/table-snapshots-restore?hl=zh-tw)。
* [更新資料表快照的說明、到期日或存取政策](https://docs.cloud.google.com/bigquery/docs/table-snapshots-update?hl=zh-tw)。
* [使用服務帳戶執行排程查詢，每月建立資料表的快照](https://docs.cloud.google.com/bigquery/docs/table-snapshots-scheduled?hl=zh-tw)。
* [在資料集層級自動建立快照](https://github.com/GoogleCloudPlatform/bigquery-utils/tree/master/tools/cloud_functions/bq_table_snapshots)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-14 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-14 (世界標準時間)。"],[],[]]