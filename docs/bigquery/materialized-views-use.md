Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 使用 materialized view

在 BigQuery 中查詢 materialized view，能以較低的延遲時間和運算成本，擷取最新資料。您可以使用自動智慧微調和直接查詢，將這些檢視表整合至現有工作流程。

閱讀本文前，請先熟悉[具體化檢視表簡介](https://docs.cloud.google.com/bigquery/docs/materialized-views-intro?hl=zh-tw)和[建立具體化檢視表](https://docs.cloud.google.com/bigquery/docs/materialized-views-create?hl=zh-tw)。

## 查詢 materialized view

您可以直接查詢 materialized view，就像查詢一般資料表或標準檢視表一樣。對 materialized view 執行的查詢，一律與對檢視表基礎資料表執行的查詢一致，即使這些資料表在上次重新整理 materialized view 後有所變更也一樣。查詢不會自動觸發具體化檢視表重新整理。

**注意：**如果未先刪除 materialized view 就刪除基礎資料表，系統會無法查詢 materialized view。重新建立基礎資料表後，必須重新建立 materialized view，才能再次查詢。

### 必要的角色

如要取得查詢 materialized view 所需的權限，請要求管理員針對 materialized view 的基礎資料表和 materialized view 本身，授予您 [BigQuery 資料檢視者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.dataViewer) (`roles/bigquery.dataViewer`) IAM 角色。如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

這個預先定義的角色具備查詢 materialized view 所需的權限。如要查看確切的必要權限，請展開「Required permissions」(必要權限) 部分：

#### 所需權限

必須具備下列權限，才能查詢 materialized view：

* `bigquery.tables.get`
* `bigquery.tables.getData`

您或許還可透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)取得這些權限。

查詢必須具備這些權限，才能使用[智慧微調](#smart_tuning)功能。

如要進一步瞭解 BigQuery 中的 IAM 角色，請參閱「[IAM 簡介](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)」。

### 增量更新

BigQuery 會將快取檢視表的資料與新資料合併，提供一致的查詢結果，同時仍使用 materialized view，這時就會進行增量更新。如果是單一資料表 materialized view，只要基礎資料表自上次重新整理後未變更，或僅新增資料，就能執行這項操作。如果是 `JOIN` 檢視表，只有 `JOIN` 左側的資料表可以附加資料。如果 `JOIN` 右側的其中一個資料表有所變更，則無法對檢視表進行增量更新。

如果基礎資料表自上次重新整理後有更新或刪除，或 `JOIN` 右側的 materialized view 基礎資料表有變更，BigQuery 就不會使用增量更新，而是自動還原為原始查詢。如要進一步瞭解 join 和 materialized view，請參閱「[join](https://docs.cloud.google.com/bigquery/docs/materialized-views-create?hl=zh-tw#joins)」。以下是可能導致更新或刪除的 Google Cloud 控制台、bq 指令列工具和 API 動作範例：

* data manipulation language (DML) `UPDATE`、`MERGE` 或 `DELETE` 陳述式
* 截斷
* 分區有效期限

下列中繼資料作業也會導致 materialized view 無法增量更新：

* 變更分區到期時間
* 更新或捨棄資料欄

如果無法對 materialized view 進行增量更新，則在自動或手動重新整理檢視表之前，查詢不會使用其快取資料。如要進一步瞭解工作為何未使用 materialized view 資料，請參閱「[瞭解 materialized view 遭拒的原因](https://docs.cloud.google.com/bigquery/docs/materialized-views-use?hl=zh-tw#understand-rejected)」。此外，如果基礎資料表累積的未處理變更時間範圍超過資料表的[時光旅行間隔](https://docs.cloud.google.com/bigquery/docs/time-travel?hl=zh-tw#configure_the_time_travel_window)，則無法對 materialized view 進行增量更新。

## 分區相符

如果 materialized view 已分區，BigQuery 會確保其分區與基礎資料表的分區資料欄分區一致。「對齊」是指基礎資料表特定分區的資料，會提供給 materialized view 的相同分區。舉例來說，基礎資料表分區 `20220101` 的資料列只會影響 materialized view 的分區 `20220101`。

如果對 materialized view 進行分區，則會針對每個分區獨立執行「[增量更新](#incremental_updates)」一節所述的行為。舉例來說，如果刪除基礎資料表某個分區中的資料，BigQuery 仍可使用 materialized view 的其他分區，不必完整重新整理整個 materialized view。

使用內部彙整的 materialized view 只能與其中一個基礎資料表對齊。如果其中一個未對齊的基礎資料表發生變更，整個檢視表都會受到影響。

對於使用 `UNION ALL` 的分區增量 materialized view，所有基礎資料表都必須採用相同的分區到期日 (TTL) 設定，才能維持分區相符。

## 智慧微調

BigQuery 會自動重寫查詢，盡可能使用 materialized view。自動重寫功能可提升查詢效能並降低成本，且不會變更查詢結果。查詢不會自動觸發具體化重新整理。如要使用智慧微調功能重寫查詢，materialized view 必須符合下列條件：

* 與其中一個基礎資料表或執行查詢的專案屬於同一個專案。
* 使用與查詢相同的一組基礎資料表。
* 包含所有讀取的資料欄。
* 包含所有讀取的資料列。

智慧微調不支援下列項目：

* [參照邏輯檢視表](https://docs.cloud.google.com/bigquery/docs/materialized-views-create?hl=zh-tw#reference_logical_views)的 materialized view。
* 使用 [union all 或左外部彙整](https://docs.cloud.google.com/bigquery/docs/materialized-views-create?hl=zh-tw#left-union)的 materialized view。
* [非漸進式 materialized view](https://docs.cloud.google.com/bigquery/docs/materialized-views-create?hl=zh-tw#limitations_specific_to_non-incremental_materialized_views)。
* 參照[已啟用變更資料擷取](https://docs.cloud.google.com/bigquery/docs/change-data-capture?hl=zh-tw)資料表的 materialized view。

### 智慧微調範例

請參考以下 materialized view 查詢範例：

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

以下範例說明查詢，以及為何這些查詢會或不會使用這個檢視表自動重寫：

| 查詢 | 要重寫嗎？ | 原因 |
| --- | --- | --- |
| SELECT  **SUM(net\_paid) AS sum\_paid**,  SUM(net\_profit) AS sum\_profit  FROM dataset.store\_sales  WHERE  CAST(sold\_datetime AS DATE) >= '2021-01-01' AND  promo\_id IS NOT NULL | 否 | 檢視表必須包含所有讀取的資料欄。檢視表不含「SUM(net\_paid)」。 |
| SELECT SUM(net\_profit) AS sum\_profit  FROM dataset.store\_sales  WHERE  CAST(sold\_datetime AS DATE) >= '2021-01-01' AND  promo\_id IS NOT NULL | 是 |  |
| SELECT SUM(net\_profit) AS sum\_profit  FROM dataset.store\_sales  WHERE  CAST(sold\_datetime AS DATE) >= '2021-01-01' AND  promo\_id IS NOT NULL AND  **customer\_id = 12345** | 否 | 檢視表必須包含所有讀取的資料欄。檢視畫面不含「customer」。 |
| SELECT SUM(net\_profit) AS sum\_profit  FROM dataset.store\_sales  WHERE  **sold\_datetime**= '2021-01-01' AND  promo\_id IS NOT NULL | 否 | 檢視表必須包含所有讀取的資料欄。「sold\_datetime」不是輸出內容 (但「CAST(sold\_datetime AS DATE)」是)。 |
| SELECT SUM(net\_profit) AS sum\_profit  FROM dataset.store\_sales  WHERE  CAST(sold\_datetime AS DATE) >= '2021-01-01' AND  promo\_id IS NOT NULL AND  store\_id = 12345 | 是 |  |
| SELECT SUM(net\_profit) AS sum\_profit  FROM dataset.store\_sales  WHERE  CAST(sold\_datetime AS DATE) >= '2021-01-01' AND  **promo\_id = 12345** | 否 | 檢視表必須包含所有讀取的資料列。「promo\_id」不是輸出內容，因此無法對檢視表套用更嚴格的篩選器。 |
| SELECT SUM(net\_profit) AS sum\_profit  FROM dataset.store\_sales  WHERE **CAST(sold\_datetime AS DATE) >= '2020-01-01'** | 否 | 檢視表必須包含所有讀取的資料列。檢視表篩選器會篩選 2021 年及之後的日期，但查詢會讀取 2020 年的日期。 |
| SELECT SUM(net\_profit) AS sum\_profit  FROM dataset.store\_sales  WHERE  CAST(sold\_datetime AS DATE) >= '2022-01-01' AND  promo\_id IS NOT NULL | 是 |  |

### 瞭解查詢是否經過重寫

如要瞭解查詢是否經過智慧微調重寫，改用 materialized view，請檢查[查詢計畫](https://docs.cloud.google.com/bigquery/docs/query-plan-explanation?hl=zh-tw)。如果查詢經過重寫，查詢計畫會包含 `READ my_materialized_view` 步驟，其中 `my_materialized_view` 是所用 materialized view 的名稱。如要瞭解查詢為何未使用 materialized view，請參閱「[瞭解 materialized view 遭拒的原因](#understand-rejected)」。

### 瞭解 materialized view 遭拒的原因

如果您已停用 materialized view 的自動重新整理功能，且資料表有未處理的變更，則查詢速度可能會在幾天內加快，但隨後會開始還原為原始查詢，導致處理速度變慢。如要充分運用 materialized view，請啟用自動重新整理功能，或定期手動重新整理，並監控 materialized view 重新整理工作，確認工作成功。

如要瞭解 materialized view 遭拒的原因，請根據您使用的查詢類型，按照下列步驟操作：

* 直接查詢 materialized view
* [智慧微調](#smart_tuning)可能會選擇使用 materialized view 的間接查詢

以下各節提供相關步驟，協助您瞭解 materialized view 遭拒的原因。

#### 直接查詢 materialized view

在某些情況下，直接查詢 materialized view 可能不會使用快取資料。下列步驟可協助您瞭解未使用 materialized view 資料的原因：

1. 按照「[監控 materialized view 使用情形](https://docs.cloud.google.com/bigquery/docs/materialized-views-monitor?hl=zh-tw#monitor_materialized_view_usage)」中的步驟操作，並在查詢的 [`materialized_view_statistics` 欄位](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#MaterializedViewStatistics)中找出目標 materialized view。
2. 如果統計資料中含有 `chosen`，且其值為 `TRUE`，則查詢會使用 materialized view。
3. 查看「`rejected_reason`」欄位，瞭解後續步驟。在多數情況下，您可以[手動重新整理](https://docs.cloud.google.com/bigquery/docs/materialized-views-manage?hl=zh-tw#manual-refresh) materialized view，或等待下次[自動重新整理](https://docs.cloud.google.com/bigquery/docs/materialized-views-manage?hl=zh-tw#automatic-refresh)。

#### 使用智慧微調功能查詢

1. 按照「[監控 materialized view 使用情形](https://docs.cloud.google.com/bigquery/docs/materialized-views-monitor?hl=zh-tw#monitor_materialized_view_usage)」中的步驟操作，並在查詢的 [`materialized_view_statistics`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#MaterializedViewStatistics) 中找出目標 materialized view。
2. 請查看`rejected_reason`，瞭解後續步驟。舉例來說，如果 `rejected_reason` 值為 `COST`，表示智慧微調功能已找出更有效率的資料來源，可降低成本並提升效能。
3. 如果沒有 materialized view，請嘗試直接查詢 materialized view，並按照「[直接查詢 materialized view](#direct_query_of_materialized_views)」中的步驟操作。
4. 如果直接查詢未使用 materialized view，則表示 materialized view 的形狀與查詢不符。如要進一步瞭解智慧微調，以及如何使用 materialized view 重寫查詢，請參閱「[智慧微調範例](https://docs.cloud.google.com/bigquery/docs/materialized-views-use?hl=zh-tw#smart_tuning_examples)」。

## 常見問題

### 何時該使用排程查詢，何時該使用 materialized view？

[排定查詢](https://docs.cloud.google.com/bigquery/docs/scheduling-queries?hl=zh-tw)可讓您輕鬆定期執行任意複雜的計算。每次執行查詢時，系統都會完整執行，不會利用先前的結果，您也必須支付查詢的完整運算費用。如果您不需要最新資料，而且較不在意資料過時，則適合使用排定查詢。

如果需要查詢最新資料，並重複運用先前的運算結果，盡可能減少延遲情形與費用，則最適合使用 materialized view。您可以將 materialized view 做為*虛擬索引*，加快對基礎資料表的查詢，而不必更新任何現有工作流程。[`--max_staleness`
選項](https://docs.cloud.google.com/bigquery/docs/materialized-views-create?hl=zh-tw#max_staleness)
可讓您定義 materialized view 可接受的過時程度，在處理經常變動的大型資料集時，以可控的成本持續提供高效能。

一般來說，只要可能且不執行任意複雜的計算，請使用 materialized view。

### 對 materialized view 執行某些查詢時，速度會比對手動 materialized view 資料表執行相同查詢時慢。為什麼會這樣？

一般來說，對 materialized view 執行查詢的效能，不一定會與對等效 materialized 資料表執行查詢的效能相同。這是因為 materialized view 一律會傳回最新結果，且必須考量自上次重新整理檢視表以來，基礎資料表的變更。

試想以下情境：

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

例如，以下查詢：

```
  SELECT * FROM my_dataset.my_mv LIMIT 10
```

的執行速度通常比這項查詢慢得多：

```
  SELECT * FROM my_dataset.my_materialized_table LIMIT 10
```

為了提供一致的最新結果，BigQuery 必須查詢基礎資料表中的新資料列，並將其合併至 materialized view，然後再套用「LIMIT 10」述詞。因此，即使 materialized view 是最新版本，速度仍會變慢。

另一方面，對 materialized view 進行匯總的速度，通常與對 materialized 資料表執行查詢的速度一樣快。例如：

```
  SELECT SUM(total_paid) FROM my_dataset.my_mv WHERE date > '2020-12-01'
```

應該要像這樣快速：

```
  SELECT SUM(total_paid) FROM my_dataset.my_materialized_table WHERE date > '2020-12-01'
```




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-11-16 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-11-16 (世界標準時間)。"],[],[]]