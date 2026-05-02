* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 針對查詢效能最佳化儲存空間

本頁提供最佳做法，協助您為 BigQuery 儲存空間進行最佳化調整，以提升查詢效能。您也可以[降低儲存空間成本](https://docs.cloud.google.com/bigquery/docs/best-practices-costs?hl=zh-tw#control-storage-cost)。雖然這些最佳做法主要著重於使用 BigQuery 儲存空間的資料表，但也可以套用至外部資料表。

BigQuery 會以資料欄格式儲存資料。以資料列為導向的資料庫是針對匯總大量記錄資料的分析工作負載進行最佳化。由於資料列通常比資料欄有更多重複資料，因此您可以利用這項特性，透過長度編碼等技術進一步壓縮資料。如要進一步瞭解 BigQuery 儲存資料的方式，請參閱「[BigQuery 儲存空間總覽](https://docs.cloud.google.com/bigquery/docs/storage_overview?hl=zh-tw)」。最佳化 BigQuery 儲存空間可提升[查詢效能](https://docs.cloud.google.com/bigquery/docs/best-practices-performance-compute?hl=zh-tw)並[控管費用](https://docs.cloud.google.com/bigquery/docs/best-practices-costs?hl=zh-tw)。

BigQuery 會提供資源的儲存空間用量詳細資料。如要查看資料表儲存空間中繼資料，請查詢下列 `INFORMATION_SCHEMA` 檢視畫面：

* [`INFORMATION_SCHEMA.TABLE_STORAGE`](https://docs.cloud.google.com/bigquery/docs/information-schema-table-storage?hl=zh-tw)
* [`INFORMATION_SCHEMA.TABLE_STORAGE_BY_ORGANIZATION`](https://docs.cloud.google.com/bigquery/docs/information-schema-table-storage-by-organization?hl=zh-tw)
* [`INFORMATION_SCHEMA.TABLE_STORAGE_USAGE_TIMELINE`](https://docs.cloud.google.com/bigquery/docs/information-schema-table-storage-usage?hl=zh-tw)
* [`INFORMATION_SCHEMA.TABLE_STORAGE_USAGE_TIMELINE_BY_ORGANIZATION`](https://docs.cloud.google.com/bigquery/docs/information-schema-table-storage-usage-by-organization?hl=zh-tw)

## 叢集資料表資料

**最佳做法：**建立叢集資料表。

如要為查詢最佳化儲存空間，請先將資料表資料分群。您可以將常用的資料欄分組，藉此減少查詢掃描的資料總量。如要瞭解如何建立叢集，請參閱「[建立及使用叢集資料表](https://docs.cloud.google.com/bigquery/docs/creating-clustered-tables?hl=zh-tw)」。

## 分區資料表資料

**最佳做法：**使用分區將大型資料表分割。

透過分區，您可以依據一組定義的資料欄特性 (例如整數資料欄、時間單位資料欄或擷取時間) 分組及排序資料。分區可減少查詢讀取的位元組數，進而提高查詢效能並控制成本。

如要進一步瞭解分區，請參閱「[分區資料表簡介](https://docs.cloud.google.com/bigquery/docs/partitioned-tables?hl=zh-tw)」。

## 使用資料表和分區到期時間設定

**最佳做法：**如要最佳化儲存空間，請為[資料集](https://docs.cloud.google.com/bigquery/docs/updating-datasets?hl=zh-tw#table-expiration)、[資料表](https://docs.cloud.google.com/bigquery/docs/managing-tables?hl=zh-tw#updating_a_tables_expiration_time)和[分區資料表](https://docs.cloud.google.com/bigquery/docs/managing-partitioned-tables?hl=zh-tw#partition-expiration)設定預設到期時間。

您可以為資料集當中新建立的資料表設定預設資料表到期時間，藉此控管儲存空間費用並為儲存空間進行最佳化處理。資料表到期後，系統會刪除該資料表及其內含的所有資料。如果您在建立資料集時設定了這項屬性，則在到期時間過後，資料集中建立的任何資料表都會遭到刪除。如果您在建立資料集後設定這項屬性，系統只會在到期時間過後刪除新資料表。

舉例來說，如果您將預設資料表到期時間設為七天，系統就會在一週後自動刪除較舊的資料。

如果您只需要存取近期資料，這個選項就可以派上用場。如果您要嘗試使用資料，但不需要保留資料，這也是實用的方法。

如果您的資料表是按日期分區，則各分區都會套用資料集的預設資料表到期時間。您也可以使用 bq 指令列工具的 `time_partitioning_expiration` 旗標或 API 中的 `expirationMs` 配置設定來控管分區到期時間。分區到期時，系統會刪除分區中的資料，但不會刪除分區資料表，即使資料表為空白也一樣。

舉例來說，下列指令會設定分區在三天後過期：

```
bq mk \
--time_partitioning_type=DAY \
--time_partitioning_expiration=259200 \
project_id:dataset.table
```

## 匯總長期資料

**最佳做法：**請確認是否需要長期儲存資料列層級資料，如果不需要，請只長期儲存匯總資料。

在許多情況下，交易或資料列層級資料中包含的詳細資料在短期內很實用，但長期而言參照的次數較少。在這種情況下，您可以建立匯總查詢來計算及儲存與此資料相關聯的指標，然後使用資料表或分區到期時間，有系統地移除資料列層級資料。這樣一來，您就能降低儲存空間費用，同時保留可用於長期消費的指標。

## 後續步驟

* 瞭解如何[降低成本](https://docs.cloud.google.com/bigquery/docs/best-practices-costs?hl=zh-tw)。
* 瞭解如何[最佳化查詢](https://docs.cloud.google.com/bigquery/docs/best-practices-performance-compute?hl=zh-tw)。
* 瞭解如何[最佳化函式](https://docs.cloud.google.com/bigquery/docs/best-practices-performance-functions?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-02 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-02 (世界標準時間)。"],[],[]]