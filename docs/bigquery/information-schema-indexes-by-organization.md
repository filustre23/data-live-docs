Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [參考資料](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# SEARCH\_INDEXES\_BY\_ORGANIZATION 檢視畫面

[BigQuery 搜尋索引](https://docs.cloud.google.com/bigquery/docs/search-intro?hl=zh-tw)提供免費索引管理服務，直到貴機構在特定區域達到[限制](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#index_limits)為止。您可以透過 `INFORMATION_SCHEMA.SEARCH_INDEXES_BY_ORGANIZATION` 檢視表，瞭解目前的使用量，以及專案和資料表的使用量明細。`INFORMATION_SCHEMA.SEARCH_INDEXES_BY_ORGANIZATION` 檢視表會針對與目前專案相關聯的整個機構，為每個搜尋索引各列出一個相對應的資料列。

**注意：** `INFORMATION_SCHEMA.SEARCH_INDEXES_BY_ORGANIZATION` 檢視畫面中的資料並非即時更新，可能會延遲幾秒到幾分鐘。

## 所需權限

如要查詢 `INFORMATION_SCHEMA.SEARCH_INDEXES_BY_ORGANIZATION` 檢視畫面，您必須具備貴機構的下列 Identity and Access Management (IAM) 權限：

* `bigquery.tables.get`
* `bigquery.tables.list`

下列每個預先定義的 IAM 角色都包含上述權限：

* `roles/bigquery.admin`
* `roles/bigquery.dataViewer`
* `roles/bigquery.dataEditor`
* `roles/bigquery.metadataViewer`

只有已定義[Google Cloud 機構](https://docs.cloud.google.com/resource-manager/docs/cloud-platform-resource-hierarchy?hl=zh-tw#organizations)的使用者才能使用這個結構定義檢視畫面。

如要進一步瞭解 BigQuery 權限，請參閱「[使用 IAM 控管存取權](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)」。

## 結構定義

`INFORMATION_SCHEMA.SEARCH_INDEXES_BY_ORGANIZATION` 檢視表具有下列結構定義：

| 資料欄名稱 | 資料類型 | 值 |
| --- | --- | --- |
| `project_id` | `STRING` | 資料集所屬專案的名稱。 |
| `project_number` | `STRING` | 包含資料集的專案編號。 |
| `index_catalog` | `STRING` | 資料集所屬專案的名稱。 |
| `index_schema` | `STRING` | 包含索引的資料集名稱。 |
| `table_name` | `STRING` | 建立索引的基礎資料表名稱。 |
| `index_name` | `STRING` | 搜尋索引的名稱。 |
| `index_status` | `STRING` | 索引狀態可能是下列其中一種：   * `ACTIVE`：索引可用或正在建立中。 * `PENDING DISABLEMENT`：索引基本資料表的總大小超出貴機構的[限制](https://cloud.google.com/bigquery/quotas?hl=zh-tw#index_limits)，索引已排入刪除佇列。處於這個狀態時，索引可用於搜尋查詢，且系統會向您收取搜尋索引儲存空間費用。 * `TEMPORARILY DISABLED`：索引基礎資料表的總大小超過貴機構的[限制](https://cloud.google.com/bigquery/quotas?hl=zh-tw#index_limits)，或是索引基礎資料表小於 10 GB。處於這個狀態時，搜尋查詢不會使用索引，您也不必支付搜尋索引儲存空間費用。 * `PERMANENTLY DISABLED`：基礎資料表發生不相容的結構定義變更，例如將索引資料欄的類型從 `STRING` 變更為 `INT64`。 |
| `index_status_details` | `RECORD` | 記錄包含下列欄位：   * `throttle_status`：指出搜尋索引的節流狀態，可能值如下：   + `UNTHROTTLED`：索引可用。   + `BASE_TABLE_TOO_SMALL`：基礎資料表大小小於 10 GB。無論您是否為索引管理工作使用自己的預留項目，都適用這項限制。在這種情況下，索引會暫時停用，搜尋查詢也不會使用索引。   + `BASE_TABLE_TOO_LARGE`：基本資料表大小超過貴機構的[限制](https://cloud.google.com/bigquery/quotas?hl=zh-tw#index_limits)。   + `ORGANIZATION_LIMIT_EXCEEDED`：貴機構中已建立索引的基礎資料表總大小超過貴機構的[限制](https://cloud.google.com/bigquery/quotas?hl=zh-tw#index_limits)。 * `message`：說明索引狀態的詳細訊息。 |
| `use_background_reservation` | `BOOL` | 指出索引維護作業是否使用 `BACKGROUND` 預訂。如果索引維護作業使用限制，這項屬性會設為 `FALSE`。 |

為確保穩定性，建議您在資訊結構定義查詢中明確列出資料欄，而非使用萬用字元 (`SELECT *`)。明確列出資料欄可避免基礎結構定義變更時，查詢中斷。

## 範圍和語法

對這個檢視表執行的查詢必須包含[區域限定詞](https://docs.cloud.google.com/bigquery/docs/information-schema-intro?hl=zh-tw#syntax)。下表說明這個檢視畫面的區域範圍：

| 檢視表名稱 | 資源範圍 | 區域範圍 |
| --- | --- | --- |
| `` [`PROJECT_ID`.]`region-REGION`.INFORMATION_SCHEMA.SEARCH_INDEXES_BY_ORGANIZATION `` | 包含指定專案的機構 | `REGION` |

更改下列內容：

* 選用：`PROJECT_ID`：您的專案 ID。Google Cloud 如未指定，系統會使用預設專案。
* `REGION`：專案的[區域](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)。例如：`` `myproject`.`region-us`.INFORMATION_SCHEMA.SEARCH_INDEXES_BY_ORGANIZATION ``。

  **注意：**您必須使用[區域限定詞](https://docs.cloud.google.com/bigquery/docs/information-schema-intro?hl=zh-tw#region_qualifier)查詢 `INFORMATION_SCHEMA` 檢視畫面。查詢執行位置必須與`INFORMATION_SCHEMA`檢視區塊的區域相符。

## 索引節流

如果索引受到節流，其資料表大小不會計入機構的限制。如果基本資料表大小低於 10 GB 或超過貴機構的[限制](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#index_limits)，就會發生節流。索引受到節流時，管理工作會暫停，導致索引過時，最終暫時停用。因此，搜尋查詢無法使用索引。

您可以設定快訊，在超過特定門檻時收到通知，這與[為排程查詢設定快訊](https://docs.cloud.google.com/bigquery/docs/create-alert-scheduled-query?hl=zh-tw)類似。舉例來說，您可以設定在表格大小超過配額限制的 70% 時觸發快訊，以便及時採取行動。

## 範例

本節包含 `INFORMATION_SCHEMA.SEARCH_INDEXES_BY_ORGANIZATION` 檢視區塊的查詢範例。

#### 查看特定區域的用量是否超出限制

以下範例說明如果整個機構在美國多重區域使用共用時段，且索引基本資料表總大小超過 100 TB，會發生什麼情況：

```
WITH
 indexed_base_table_size AS (
 SELECT
   SUM(base_table.total_logical_bytes) AS total_logical_bytes
 FROM
   `region-us`.INFORMATION_SCHEMA.SEARCH_INDEXES_BY_ORGANIZATION AS search_index
 JOIN
   `region-us`.INFORMATION_SCHEMA.TABLE_STORAGE_BY_ORGANIZATION AS base_table
 ON
   (search_index.table_name = base_table.table_name
     AND search_index.project_id = base_table.project_id
     AND search_index.index_schema = base_table.table_schema)
 WHERE
   TRUE
   -- Excludes search indexes that are permanently disabled.
   AND search_index.index_status != 'PERMANENTLY DISABLED'
   -- Excludes BASE_TABLE_TOO_SMALL search indexes whose base table size is
   -- less than 10 GB. These tables don't count toward the limit.
   AND search_index.index_status_details.throttle_status != 'BASE_TABLE_TOO_SMALL'
   -- Excludes search indexes whose project has BACKGROUND reservation purchased
   -- for search indexes.
   AND search_index.use_background_reservation = false
 -- Outputs the total indexed base table size if it exceeds 100 TB,
 -- otherwise, doesn't return any output.
)
SELECT * FROM indexed_base_table_size
WHERE total_logical_bytes >= 109951162777600 -- 100 TB
```

結果大致如下：

```
+---------------------+
| total_logical_bytes |
+---------------------+
|     109951162777601 |
+---------------------+
```

#### 找出區域中各專案的索引基本資料表總大小

以下範例會列出美國多區域中每個專案的詳細資料，包括已建立索引的基本資料表總大小：

```
SELECT
 search_index.project_id,
 search_index.use_background_reservation,
 SUM(base_table.total_logical_bytes) AS total_logical_bytes
FROM
 `region-us`.INFORMATION_SCHEMA.SEARCH_INDEXES_BY_ORGANIZATION AS search_index
JOIN
 `region-us`.INFORMATION_SCHEMA.TABLE_STORAGE_BY_ORGANIZATION AS base_table
ON
 (search_index.table_name = base_table.table_name
   AND search_index.project_id = base_table.project_id
   AND search_index.index_schema = base_table.table_schema)
WHERE
 TRUE
  -- Excludes search indexes that are permanently disabled.
  AND search_index.index_status != 'PERMANENTLY DISABLED'
  -- Excludes BASE_TABLE_TOO_SMALL search indexes whose base table size is
  -- less than 10 GB. These tables don't count toward limit.
 AND search_index.index_status_details.throttle_status != 'BASE_TABLE_TOO_SMALL'
GROUP BY search_index.project_id, search_index.use_background_reservation
```

結果大致如下：

```
+---------------------+----------------------------+---------------------+
|     project_id      | use_background_reservation | total_logical_bytes |
+---------------------+----------------------------+---------------------+
| projecta            |     true                   |     971329178274633 |
+---------------------+----------------------------+---------------------+
| projectb            |     false                  |     834638211024843 |
+---------------------+----------------------------+---------------------+
| projectc            |     false                  |     562910385625126 |
+---------------------+----------------------------+---------------------+
```

#### 找出受到節流的搜尋索引

以下範例會傳回機構和區域內所有受到節流的搜尋索引：

```
SELECT project_id, index_schema, table_name, index_name
FROM
 `region-us`.INFORMATION_SCHEMA.SEARCH_INDEXES_BY_ORGANIZATION
WHERE
 -- Excludes search indexes that are permanently disabled.
 index_status != 'PERMANENTLY DISABLED'
 AND index_status_details.throttle_status IN ('ORGANIZATION_LIMIT_EXCEEDED', 'BASE_TABLE_TOO_LARGE')
```

結果大致如下：

```
+--------------------+--------------------+---------------+----------------+
|     project_id     |    index_schema    |  table_name   |   index_name   |
+--------------------+--------------------+---------------+----------------+
|     projecta       |     dataset_us     |   table1      |    index1      |
|     projectb       |     dataset_us     |   table1      |    index1      |
+--------------------+--------------------+---------------+----------------+
```




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-16 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-16 (世界標準時間)。"],[],[]]