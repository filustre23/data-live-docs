Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 資料表本機副本簡介

本文提供 BigQuery 中資料表副本的總覽。這份指南適用於熟悉 [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw) 和 BigQuery [資料表](https://docs.cloud.google.com/bigquery/docs/tables-intro?hl=zh-tw)的使用者。

*資料表副本*是另一個資料表 (稱為*基本資料表*) 的輕量型可寫入副本。系統只會針對與基礎資料表不同的資料表副本儲存空間收費，因此一開始建立資料表副本時不會產生儲存空間費用。除了儲存空間的計費模式，以及基礎資料表的一些額外中繼資料外，資料表複製與標準資料表類似，您可以查詢、複製、刪除等等。

表格副本的常見用途包括：

* 建立正式版資料表的副本，用於開發和測試。
* 為使用者建立沙箱，讓他們產生自己的分析資料和資料操作，不必實際複製所有正式環境資料。系統只會針對變更的資料收費。

建立資料表副本後，副本會獨立於基本資料表。對基本資料表或資料表本機副本所做的任何變更，都不會反映在另一個資料表中。

如果您需要資料表的唯讀輕量副本，建議使用[資料表快照](https://docs.cloud.google.com/bigquery/docs/table-snapshots-intro?hl=zh-tw)。

## 資料表副本中繼資料

資料表複製與標準資料表的中繼資料相同，但會加上以下資訊：

* 專案、資料集和資料表名稱，以及資料表副本的基礎資料表。
* 資料表複製作業的時間。如果使用[時間旅行](https://docs.cloud.google.com/bigquery/docs/time-travel?hl=zh-tw)建立資料表副本，則這是時間旅行時間戳記。

詳情請參閱 [INFORMATION\_SCHEMA.TABLES](https://docs.cloud.google.com/bigquery/docs/information-schema-tables?hl=zh-tw)。

## 資料表複製作業

一般來說，您使用資料表副本的方式與[標準資料表](https://docs.cloud.google.com/bigquery/docs/managing-tables?hl=zh-tw)相同，包括下列作業：

* 查詢
* 存取權控管
* 取得中繼資料
* 分區與分群
* 使用結構定義
* 刪除中

不過，建立資料表副本的方式與建立標準資料表不同。詳情請參閱「[建立資料表副本](https://docs.cloud.google.com/bigquery/docs/table-clones-create?hl=zh-tw)」。

## 儲存空間費用

[儲存空間費用](https://cloud.google.com/bigquery/pricing?hl=zh-tw#storage)適用於資料表副本，但 BigQuery 只會針對資料表副本中尚未向其他資料表收費的資料收費：

* 建立資料表本機副本時，一開始不會產生儲存空間費用。
* 如果在資料表副本中新增或變更資料，系統會針對新增或更新的資料收取儲存空間費用。
* 複製資料表時，副本的儲存空間類型與來源資料的儲存空間類型相同。舉例來說，如果您複製分類為有效儲存空間的資料表，複製的資料表也會是有效儲存空間。同樣地，如果基礎資料表歸類為長期儲存空間，複製的資料表也會是長期儲存空間。
* 如果資料表副本中的資料遭到刪除，您就不必支付已刪除資料的儲存空間費用。
* 如果基本資料表中的資料也存在於資料表本機副本，且資料經過變更或刪除，則您需要為變更或刪除的資料支付資料表本機副本的儲存空間費用。如果有多個副本包含變更或刪除的資料，系統只會針對最舊副本使用的儲存空間收費。
* 如果在建立資料表副本後，資料已新增至基礎資料表，則您不必為資料表副本中的資料儲存空間付費，但基礎資料表會收取相關費用。

下圖顯示基礎資料表和資料表副本的儲存空間費用差異：


**注意：**

* 由於 BigQuery 儲存空間是以資料欄為基礎，因此對基礎資料表中的資料進行小幅變更，可能會導致資料表副本的儲存空間費用大幅增加。
* 如果對基本資料表進行某些變更，您可能需要為資料表的本機副本支付全額儲存空間費用。舉例來說，如果您修改具有[叢集](https://docs.cloud.google.com/bigquery/docs/manage-clustered-tables?hl=zh-tw#modifying-cluster-spec)的基本資料表，可能會導致系統自動重新叢集。由於重新叢集化作業可能會重新編寫基礎資料表的儲存區塊，基礎資料表的儲存空間不再與其複本的儲存空間相同。這會導致系統向最舊的基礎資料表副本收取修改後分區的完整儲存空間費用。
* 分區有助於降低資料表副本的儲存空間費用。一般來說，BigQuery 只會複製分區中經過修改的資料，而不是複製整個資料表。

詳情請參閱 [BigQuery 儲存空間定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#storage)一文。

## 限制

* 您可以在同一專案的不同資料集之間複製資料表，也可以在不同專案的資料集之間複製資料表。不過，資料表副本的目的地資料集必須與要複製的資料表位於同一個[地區](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)，且屬於同一個[機構](https://docs.cloud.google.com/resource-manager/docs/creating-managing-organization?hl=zh-tw)。例如，您無法將位於歐盟資料集的資料表複製到位於美國的資料集。
* 您無法建立資料表資料的副本，因為該資料表的時間比資料集[時間旅行](https://docs.cloud.google.com/bigquery/docs/time-travel?hl=zh-tw)視窗的持續時間更早。
* 您無法複製「檢視」或「具體化檢視」。
* 您無法建立[外部資料表](https://docs.cloud.google.com/bigquery/docs/external-tables?hl=zh-tw)的副本。
* 如果您複製的資料表含有寫入最佳化儲存空間中的資料 ([最近串流資料列的串流緩衝區](https://docs.cloud.google.com/bigquery/docs/streaming-data-into-bigquery?hl=zh-tw#dataavailability))，則資料表副本不會包含寫入最佳化儲存空間中的資料。
* 如果複製的資料表含有[時空旅行](https://docs.cloud.google.com/bigquery/docs/time-travel?hl=zh-tw)資料，複製的資料表不會包含時空旅行資料。
* 在「探索」窗格中，無法區分資料表副本和標準資料表。不過，您可以[查看資料表詳細資料](https://docs.cloud.google.com/bigquery/docs/tables?hl=zh-tw#get_table_information_using_information_schema)，判斷資料表是否為標準資料表副本。資料表副本詳細資料有「Base Table Info」(基礎資料表資訊) 區段，標準資料表則沒有。
* 您無法使用複製作業將資料附加至現有資料表。舉例來說，您無法在同一個 [`bq cp`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_cp) 指令中使用 `--append_table=true` 和 `--append_table=true` 和 `--clone=true` 旗標設定。如要在複製資料表時附加資料，請改用複製作業。
* 建立資料表副本時，名稱必須遵守與建立資料表時相同的[命名規則](https://docs.cloud.google.com/bigquery/docs/tables?hl=zh-tw#table_naming)。
* 建立資料表副本時，必須遵守 BigQuery 複製工作的[限制](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#copy_jobs)。
* BigQuery 建立資料表副本所需的時間可能會因執行次數而有顯著差異，因為基礎儲存空間是動態管理。

## 配額與限制

資料表副本的配額和限制與標準資料表相同。詳情請參閱[表格配額與限制](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#table_limits)。此外，還設有[資料表複製限制](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#table_clones)。

## 後續步驟

* [建立資料表副本](https://docs.cloud.google.com/bigquery/docs/table-clones-create?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-09 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-09 (世界標準時間)。"],[],[]]