* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 使用具體化檢視表

本文提供具體化檢視表的相關資訊，以及如何使用這類檢視表。閱讀本文前，請先熟悉「[具體化檢視區塊簡介](https://docs.cloud.google.com/bigquery/docs/materialized-views-intro?hl=zh-tw)」和「[建立具體化檢視區塊](https://docs.cloud.google.com/bigquery/docs/materialized-views-create?hl=zh-tw)」。

## 查詢具體化檢視表

您可以直接查詢具體化檢視表，方法與查詢一般資料表或標準檢視表相同。即使檢視表的基本資料表在上次重新整理具體化檢視表後有所變更，針對具體化檢視表執行的查詢，一律會與針對檢視表基本資料表執行的查詢保持一致。查詢不會自動觸發具體化重新整理。

**注意：** 如果未先刪除具體化檢視表就刪除基礎資料表，對具體化檢視表的查詢就會失敗。重新建立基礎資料表後，您必須重新建立具體化檢視，才能再次查詢。

### 必要的角色

如要取得查詢具體化檢視表所需的權限，請要求管理員授予您具體化檢視表和基礎資料表的「BigQuery 資料檢視者」 (`roles/bigquery.dataViewer`) 身分與存取權管理角色。如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和機構的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

這個預先定義的角色具備查詢具體化檢視區塊所需的權限。如要查看確切的必要權限，請展開「必要權限」部分：

#### 所需權限

如要查詢具體化檢視區塊，必須具備下列權限：

* `bigquery.tables.get`
* `bigquery.tables.getData`

您或許還可透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)取得這些權限。

查詢必須具備這些權限，才能使用[智慧微調](#smart_tuning)功能。

如要進一步瞭解 BigQuery 中的 IAM 角色，請參閱 [IAM 簡介](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)。

### 分批更新

當 BigQuery 將快取檢視的資料與新資料合併，以提供一致的查詢結果，同時仍使用具體化檢視時，就會發生增量更新。如果是單一資料表的具體化檢視表，只要基礎資料表自上次重新整理後未變更，或只新增資料，即可執行這項作業。如果是 `JOIN` 檢視畫面，只有 `JOIN` 左側的資料表可以附加資料。如果 `JOIN` 右側的其中一個表格已變更，則無法以遞增方式更新檢視畫面。

如果基礎資料表在上次重新整理後有更新或刪除作業，或實體化檢視區塊右側 `JOIN` 的基礎資料表已變更，BigQuery 就不會使用增量更新，而是自動還原為原始查詢。如要進一步瞭解聯結和具體化檢視區塊，請參閱「[聯結](https://docs.cloud.google.com/bigquery/docs/materialized-views-create?hl=zh-tw#joins)」。以下是可能導致更新或刪除的 Google Cloud 主控台、bq 指令列工具和 API 動作範例：

* 資料操縱語言 (DML) `UPDATE`、`MERGE` 或 `DELETE` 陳述式
* 截斷
* 分區有效期限

下列中繼資料作業也會導致具體化檢視區塊無法以遞增方式更新：

* 變更分區到期時間
* 更新或捨棄資料欄

如果具體化檢視表無法以漸進方式更新，查詢就不會使用其快取資料，直到檢視表自動或手動重新整理為止。如要瞭解作業為何未使用具體化檢視表資料，請參閱「[瞭解具體化檢視表遭拒的原因](https://docs.cloud.google.com/bigquery/docs/materialized-views-use?hl=zh-tw#understand-rejected)」。此外，如果基礎資料表累積的未處理變更時間範圍大於資料表的[時間旅行間隔](https://docs.cloud.google.com/bigquery/docs/time-travel?hl=zh-tw#configure_the_time_travel_window)，則無法以遞增方式更新具體化檢視區塊。

## 分區對齊

如果具體化檢視區分區，BigQuery 會確保其分區與基礎資料表分區欄的分區對齊。*對齊*是指基礎資料表特定分區的資料，會對應到具體化檢視表中的相同分區。舉例來說，基底資料表分區 `20220101` 中的資料列只會影響具體化檢視分區 `20220101`。

如果具體化檢視區隔化，則每個區隔都會獨立發生「[增量更新](#incremental_updates)」一節所述的行為。舉例來說，如果刪除基礎資料表某個分區中的資料，BigQuery 仍可使用具體化檢視表的其他分區，而不必完整重新整理整個具體化檢視表。

使用內部彙整功能的具體化檢視表只能與其中一個基本資料表對齊。如果其中一個未對齊的基礎資料表發生變化，整個檢視區塊都會受到影響。

## 智慧微調

BigQuery 會盡可能自動重新編寫查詢，以使用具體化檢視區塊。自動重寫功能可提升查詢效能並降低成本，同時維持查詢結果不變。查詢不會自動觸發具體化重新整理。如要使用智慧微調功能重新編寫查詢，具體化檢視區塊必須符合下列條件：

* 與其中一個基礎資料表或查詢執行的專案屬於同一專案。
* 使用與查詢相同的基本資料表集。
* 納入所有要讀取的資料欄。
* 包含所有讀取的資料列。

智慧微調功能不支援下列項目：

* [參照邏輯檢視表](https://docs.cloud.google.com/bigquery/docs/materialized-views-create?hl=zh-tw#reference_logical_views)的具體化檢視表。
* 使用 [UNION ALL 或左外部彙整](https://docs.cloud.google.com/bigquery/docs/materialized-views-create?hl=zh-tw#left-union)的具體化檢視表。
* [非遞增式具體化檢視表](https://docs.cloud.google.com/bigquery/docs/materialized-views-create?hl=zh-tw#limitations_specific_to_non-incremental_materialized_views)。
* 參照[已啟用變更資料擷取](https://docs.cloud.google.com/bigquery/docs/change-data-capture?hl=zh-tw)的資料表具體化檢視區。

### 智慧微調範例

請參考以下具體化檢視查詢範例：

```
SELECT
  store_id,
  CAST(sold_datetime AS DATE) AS sold_date
  SUM(net_profit) AS sum_profit
FROM dataset.store_sales
WHERE
  CAST(sold_datetime AS DATE) >= '2021-01-01' AND
  promo_id IS NOT NULL
GROUP BY 1, 2
```

下列範例顯示查詢，以及這些查詢是否會使用這個檢視區塊自動重新編寫：

| 查詢 | 要改寫嗎？ | 原因 |
| --- | --- | --- |
| SELECT  **SUM(net\_paid) AS sum\_paid**,  SUM(net\_profit) AS sum\_profit  FROM dataset.store\_sales  WHERE  CAST(sold\_datetime AS DATE) >= '2021-01-01' AND  promo\_id IS NOT NULL | 否 | 檢視畫面必須包含所有讀取的資料欄。檢視畫面不含「SUM(net\_paid)」。 |
| SELECT SUM(net\_profit) AS sum\_profit  FROM dataset.store\_sales  WHERE  CAST(sold\_datetime AS DATE) >= '2021-01-01' AND  promo\_id IS NOT NULL | 是 |  |
| SELECT SUM(net\_profit) AS sum\_profit  FROM dataset.store\_sales  WHERE  CAST(sold\_datetime AS DATE) >= '2021-01-01' AND  promo\_id IS NOT NULL AND  **customer\_id = 12345** | 否 | 檢視畫面必須包含所有讀取的資料欄。檢視畫面不含「customer」。 |
| SELECT SUM(net\_profit) AS sum\_profit  FROM dataset.store\_sales  WHERE  **sold\_datetime**= '2021-01-01' AND  promo\_id IS NOT NULL | 否 | 檢視畫面必須包含所有讀取的資料欄。「sold\_datetime」不是輸出內容 (但「CAST(sold\_datetime AS DATE)」是)。 |
| SELECT SUM(net\_profit) AS sum\_profit  FROM dataset.store\_sales  WHERE  CAST(sold\_datetime AS DATE) >= '2021-01-01' AND  promo\_id IS NOT NULL AND  store\_id = 12345 | 是 |  |
| SELECT SUM(net\_profit) AS sum\_profit  FROM dataset.store\_sales  WHERE  CAST(sold\_datetime AS DATE) >= '2021-01-01' AND  **promo\_id = 12345** | 否 | 檢視畫面必須包含所有讀取的資料列。「promo\_id」不是輸出內容，因此無法對檢視畫面套用限制較嚴格的篩選器。 |
| SELECT SUM(net\_profit) AS sum\_profit  FROM dataset.store\_sales  WHERE **CAST(sold\_datetime AS DATE) >= '2020-01-01'** | 否 | 檢視畫面必須包含所有讀取的資料列。資料檢視篩選器適用於 2021 年 (含) 以後的日期，但查詢讀取的日期是 2020 年。 |
| SELECT SUM(net\_profit) AS sum\_profit  FROM dataset.store\_sales  WHERE  CAST(sold\_datetime AS DATE) >= '2022-01-01' AND  promo\_id IS NOT NULL | 是 |  |

### 瞭解查詢是否經過改寫

如要瞭解智慧調整功能是否已重新編寫查詢，以使用具體化檢視區塊，請檢查[查詢計畫](https://docs.cloud.google.com/bigquery/docs/query-plan-explanation?hl=zh-tw)。如果查詢經過重寫，查詢計畫會包含 `READ my_materialized_view` 步驟，其中 `my_materialized_view` 是所用具體化檢視表的名稱。如要瞭解查詢未採用具體化檢視表的原因，請參閱「[瞭解具體化檢視表遭拒的原因](#understand-rejected)」。

### 瞭解具體化檢視表遭拒的原因

如果您已停用具體化檢視區塊的自動重新整理功能，且資料表有未處理的變更，查詢速度可能會在幾天內變快，但之後會開始還原為原始查詢，導致處理速度變慢。如要使用具體化檢視區塊，請啟用自動重新整理功能，或定期手動重新整理，並監控具體化檢視區塊重新整理作業，確認作業成功。

如要瞭解具體化檢視區塊遭拒的原因，請按照您使用的查詢類型執行下列步驟：

* 直接查詢具體化檢視表
* 間接查詢，[智慧型微調](#smart_tuning)可能會選擇使用具體化檢視表

以下各節提供步驟，協助您瞭解實體化檢視區塊遭到拒絕的原因。

#### 直接查詢具體化檢視表

在特定情況下，直接查詢具體化檢視區塊可能不會使用快取資料。請按照下列步驟，瞭解系統未採用具體化檢視區塊資料的原因：

1. 請按照「[監控具體化檢視表使用情形](https://docs.cloud.google.com/bigquery/docs/materialized-views-monitor?hl=zh-tw#monitor_materialized_view_usage)」一文中的步驟操作，並在查詢的 [`materialized_view_statistics` 欄位中找出目標具體化檢視表](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#MaterializedViewStatistics)。
2. 如果統計資料中存在 `chosen`，且值為 `TRUE`，則查詢會使用具體化檢視區塊。
3. 查看「`rejected_reason`」欄位，瞭解後續步驟。在大多數情況下，您可以[手動重新整理](https://docs.cloud.google.com/bigquery/docs/materialized-views-manage?hl=zh-tw#manual-refresh)具體化檢視區塊，或等待下一次[自動重新整理](https://docs.cloud.google.com/bigquery/docs/materialized-views-manage?hl=zh-tw#automatic-refresh)。

#### 使用智慧微調功能查詢

1. 請按照「[監控具體化檢視區塊使用情形](https://docs.cloud.google.com/bigquery/docs/materialized-views-monitor?hl=zh-tw#monitor_materialized_view_usage)」中的步驟操作，並在查詢的 [`materialized_view_statistics`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#MaterializedViewStatistics) 中找出目標具體化檢視區塊。
2. 請參閱`rejected_reason`，瞭解後續步驟。舉例來說，如果 `rejected_reason` 值為 `COST`，表示智慧調整功能已找出更有效率的費用和成效資料來源。
3. 如果沒有具體化檢視表，請嘗試直接查詢具體化檢視表，並按照「[直接查詢具體化檢視表](#direct_query_of_materialized_views)」一節中的步驟操作。
4. 如果直接查詢未使用具體化檢視表，則具體化檢視表的形狀與查詢不符。如要進一步瞭解智慧微調，以及如何使用具體化檢視區塊重新編寫查詢，請參閱[智慧微調範例](https://docs.cloud.google.com/bigquery/docs/materialized-views-use?hl=zh-tw#smart_tuning_examples)。

## 常見問題

### 排程查詢與具體化檢視表的使用時機

[排程查詢](https://docs.cloud.google.com/bigquery/docs/scheduling-queries?hl=zh-tw)可讓您定期執行任意複雜的計算，每次執行查詢時，系統都會完整執行，不會沿用先前的結果，且您須支付查詢的完整運算費用。如果您不需要最新資料，而且較不在意資料過時，排程查詢就是理想選擇。

如果您需要查詢最新資料，並重複運用先前的運算結果，盡可能減少延遲情形與費用，具體化檢視表就是最佳選擇。您可以將具體化檢視表做為*虛擬索引*，加快查詢基礎資料表的速度，且不必更新任何現有工作流程。[`--max_staleness`
選項](https://docs.cloud.google.com/bigquery/docs/materialized-views-create?hl=zh-tw#max_staleness)
可讓您定義具體化檢視區塊可接受的陳舊程度，在處理大型且經常變更的資料集時，以受控的成本提供一致的高效能。

一般而言，只要可能且您並未執行任意複雜的計算，請使用具體化檢視區塊。

### 針對具體化檢視表執行的部分查詢，速度會比針對手動具體化資料表執行的相同查詢慢。為什麼會這樣？

一般來說，對具體化檢視表執行的查詢，效能不一定比對等具體化資料表執行的查詢好。這是因為具體化檢視區塊一律會傳回最新結果，且必須考量自上次檢視區塊重新整理後，基礎資料表發生的變更。

請參考下列情境：

```
CREATE MATERIALIZED VIEW my_dataset.my_mv AS
SELECT date, customer_id, region, SUM(net_paid) as total_paid
FROM my_dataset.sales
GROUP BY 1, 2, 3;

CREATE TABLE my_dataset.my_materialized_table AS
SELECT date, customer_id, region, SUM(net_paid) as total_paid
FROM my_dataset.sales
GROUP BY 1, 2, 3;
```

舉例來說，這項查詢：

```
  SELECT * FROM my_dataset.my_mv LIMIT 10
```

通常比這個查詢慢得多：

```
  SELECT * FROM my_dataset.my_materialized_table LIMIT 10
```

為了提供持續更新的結果，BigQuery 必須查詢基礎資料表中的新資料列，並將這些資料列合併至具體化檢視區塊，然後再套用「LIMIT 10」述詞。
因此，即使具體化檢視區塊完全是最新狀態，速度仍會很慢。

另一方面，對具體化檢視表執行的匯總作業通常與對具體化資料表執行的查詢一樣快速。例如：

```
  SELECT SUM(total_paid) FROM my_dataset.my_mv WHERE date > '2020-12-01'
```

應盡快完成，如下所示：

```
  SELECT SUM(total_paid) FROM my_dataset.my_materialized_table WHERE date > '2020-12-01'
```




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-02 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-02 (世界標準時間)。"],[],[]]