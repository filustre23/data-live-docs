Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [參考資料](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# TABLE\_STORAGE 檢視表

`INFORMATION_SCHEMA.TABLE_STORAGE` 檢視畫面會提供資料表和 materialized view 的儲存空間用量目前快照。查詢 `INFORMATION_SCHEMA.TABLE_STORAGE` 檢視表時，查詢結果會針對目前專案的每個資料表或 materialized view 顯示一列。

`INFORMATION_SCHEMA.TABLE_STORAGE` 檢視畫面中的資料不會即時保留，更新通常會延遲幾秒到幾分鐘。如果儲存空間異動僅由分區或資料表到期造成，或由資料集時間旅行時間範圍的修改造成，可能需要最多一天的時間，才會反映在 `INFORMATION_SCHEMA.TABLE_STORAGE` 檢視表中。如果刪除的資料集包含超過 1,000 個資料表，則在刪除資料集的[時間旅行期間](https://docs.cloud.google.com/bigquery/docs/time-travel?hl=zh-tw#time_travel)結束前，這個檢視表不會反映變更。

資料表儲存空間檢視畫面可讓您輕鬆查看目前的儲存空間用量，並提供詳細資料，說明儲存空間使用的是邏輯未壓縮位元組、實體壓縮位元組，還是時間旅行位元組。這項資訊可協助您規劃未來成長，以及瞭解資料表的更新模式。

## `*_BYTES` 欄中的資料

資料表儲存空間檢視表中的 `*_BYTES` 欄包含儲存空間位元組用量資訊。這項資訊是根據您在 materialized view 和下列資料表類型的儲存空間用量決定：

* 透過「[建立及使用資料表](https://docs.cloud.google.com/bigquery/docs/tables?hl=zh-tw)」一文所述的任何方法建立的永久資料表。
* 在[工作階段](https://docs.cloud.google.com/bigquery/docs/sessions-write-queries?hl=zh-tw#use_temporary_tables_in_sessions)中建立的暫存資料表。這些資料表會放入資料集，並產生類似「\_c018003e063d09570001ef33ae401fad6ab92a6a」的名稱。
* 在[多重陳述式查詢](https://docs.cloud.google.com/bigquery/docs/multi-statement-queries?hl=zh-tw#temporary_tables) (「指令碼」) 中建立的臨時資料表。這些資料表會放入資料集，並產生「\_script72280c173c88442c3a7200183a50eeeaa4073719」等名稱。

儲存在[查詢結果快取](https://docs.cloud.google.com/bigquery/docs/writing-results?hl=zh-tw#temporary_and_permanent_tables)中的資料不會向您收費，因此不會計入 `*_BYTES` 欄值。

複製項目和快照會將 `*_BYTES` 資料欄值顯示為完整資料表，而非基礎資料表所用儲存空間的差異，因此會高估。帳單會正確反映這項儲存空間用量差異。如要進一步瞭解複製和快照儲存及計費的差異位元組，請參閱 [`TABLE_STORAGE_USAGE_TIMELINE` 檢視畫面](https://docs.cloud.google.com/bigquery/docs/information-schema-table-storage-usage?hl=zh-tw)。

## 預測儲存空間費用

如要預測資料集的每月儲存空間帳單費用，您可以使用這個檢視表中的 `logical` 或 `physical *_BYTES` 資料欄，具體取決於資料集使用的[資料集儲存空間帳單模式](https://docs.cloud.google.com/bigquery/docs/datasets-intro?hl=zh-tw#dataset_storage_billing_models)。請注意，這只是粗略預測，精確的帳單金額會根據 BigQuery 儲存空間計費基礎架構的使用量計算，並顯示在 Cloud Billing 中。

如果資料集採用邏輯計費模式，您可以按照下列方式預估每月儲存空間費用：

((`ACTIVE_LOGICAL_BYTES` 值 / `POW`(1024, 3)) \* 使用中的邏輯位元組定價) +
((`LONG_TERM_LOGICAL_BYTES` 值 / `POW`(1024, 3)) \* 長期邏輯位元組定價)

資料表的 `ACTIVE_LOGICAL_BYTES` 值反映該資料表目前使用的有效位元組。

如果資料集採用實體計費模式，您可以按照下列方式預測儲存空間費用：

((`ACTIVE_PHYSICAL_BYTES + FAIL_SAFE_PHYSICAL_BYTES` 值 / `POW`(1024, 3)) \* 作用中實體位元組定價) +
((`LONG_TERM_PHYSICAL_BYTES` 值 / `POW`(1024, 3)) \* 長期實體位元組定價)

資料表的 `ACTIVE_PHYSICAL_BYTES` 值反映該資料表目前使用的有效位元組，加上該資料表時間旅行所用的位元組。

如要單獨查看資料表的有效位元組，請從 `ACTIVE_PHYSICAL_BYTES` 值中減去 `TIME_TRAVEL_PHYSICAL_BYTES` 值。

詳情請參閱「[儲存空間定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#storage)」。

**注意：** 檢視表名稱 `INFORMATION_SCHEMA.TABLE_STORAGE` 和 `INFORMATION_SCHEMA.TABLE_STORAGE_BY_PROJECT` 是同義詞，可以交替使用。

## 瞭解位元組值與計費單位

`INFORMATION_SCHEMA.TABLE_STORAGE` 檢視表中的 `*_BYTES` 欄會以位元組為單位，提供目前儲存空間用量的數據匯報。這會顯示當下儲存的資料量。

不過，Cloud Billing 報表顯示的 BigQuery 儲存空間費用，並非僅根據這個即時大小計算。而是根據一段時間內儲存的資料量計算。標準計費單位為 GiB-月或 TiB-月。

舉例來說，無論當月有 28 天或 31 天，只要儲存 1 GiB 滿一個日曆月，用量就會是 1 GiB 月。同樣地，如果資料只儲存一個月中的部分天數，則會按比例計算費用。在 31 天的月份中，儲存 31 GiB 一天約為 1 GiB-月，而在 28 天的月份中，儲存 28 GiB 一天也約為 1 GiB-月。

雖然 `INFORMATION_SCHEMA.TABLE_STORAGE` 中的位元組值是預估潛在費用的重要輸入內容，但實際帳單反映的是 `(bytes stored * duration stored)` 的連續計算結果。這個檢視畫面中的值不會直接與帳單報表中的明細項目相符，因為帳單報表中的明細項目是帳單週期內的匯總資料。

如要全面瞭解儲存空間費用的計算方式，請參閱「[儲存空間定價](https://docs.cloud.google.com/bigquery/pricing?hl=zh-tw#storage-pricing)」頁面。

## 必要的角色

如要取得查詢 `INFORMATION_SCHEMA.TABLE_STORAGE` 檢視表所需的權限，請要求管理員授予您專案的 [BigQuery 中繼資料檢視者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.metadataViewer)  (`roles/bigquery.metadataViewer`) IAM 角色。如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

這個預先定義的角色具備查詢 `INFORMATION_SCHEMA.TABLE_STORAGE` 檢視表所需的權限。如要查看確切的必要權限，請展開「Required permissions」(必要權限) 部分：

#### 所需權限

必須具備下列權限，才能查詢 `INFORMATION_SCHEMA.TABLE_STORAGE` 檢視表：

* `bigquery.tables.get`
* `bigquery.tables.list`

您或許還可透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)取得這些權限。

## 結構定義

`INFORMATION_SCHEMA.TABLE_STORAGE` 檢視表具有下列結構定義：

| 資料欄名稱 | 資料類型 | 值 |
| --- | --- | --- |
| `project_id` | `STRING` | 資料集所屬專案的 ID。 |
| `project_number` | `INT64` | 資料集所屬專案的編號。 |
| `table_catalog` | `STRING` | 資料集所屬專案的 ID。 |
| `table_schema` | `STRING` | 包含資料表或 materialized view 的資料集名稱，也稱為 `datasetId`。 |
| `table_name` | `STRING` | 資料表或 materialized view 的名稱，也稱為 `tableId`。 |
| `creation_time` | `TIMESTAMP` | 資料表的建立時間。 |
| `total_rows` | `INT64` | 資料表或 materialized view 中的資料列總數。 |
| `total_partitions` | `INT64` | 資料表或 materialized view 中的分區數量。未分區資料表會傳回 0。 |
| `total_logical_bytes` | `INT64` | 資料表或 materialized view 中的邏輯 (未壓縮) 位元組總數。 |
| `active_logical_bytes` | `INT64` | 未滿 90 天的邏輯 (未壓縮) 位元組數。 |
| `long_term_logical_bytes` | `INT64` | 超過 90 天的邏輯 (未壓縮) 位元組數。 |
| `current_physical_bytes` | `INT64` | 資料表目前所有分區的實體位元組總數。 |
| `total_physical_bytes` | `INT64` | 用於儲存空間的實體 (壓縮) 位元組總數，包括使用中、長期和時間旅行 (已刪除或變更的資料) 位元組。不含安全防護 (時間旅行期間過後保留的已刪除或變更資料) 位元組。 |
| `active_physical_bytes` | `INT64` | 90 天內的實體 (壓縮) 位元組數，包括時間旅行 (已刪除或變更的資料) 位元組。 |
| `long_term_physical_bytes` | `INT64` | 超過 90 天的實體 (壓縮) 位元組數。 |
| `time_travel_physical_bytes` | `INT64` | 時光旅行儲存空間 (已刪除或變更的資料) 使用的實體 (壓縮) 位元組數。 |
| `storage_last_modified_time` | `TIMESTAMP` | 資料寫入資料表的最近時間。如果沒有任何資料，則會傳回 `NULL`。 |
| `deleted` | `BOOLEAN` | 指出資料表是否已刪除。 |
| `table_type` | `STRING` | 資料表類型。例如 `BASE TABLE`。 |
| `managed_table_type` | `STRING` | 這一欄目前為預先發布版。資料表的代管類型。例如 `NATIVE` 或 `BIGLAKE`。 |
| `fail_safe_physical_bytes` | `INT64` | 安全防護儲存空間 (已刪除或變更的資料) 使用的實體 (壓縮) 位元組數。 |
| `last_metadata_index_refresh_time` | `TIMESTAMP` | 資料表上次重新整理中繼資料索引的時間。 |
| `table_deletion_reason` | `STRING` | 如果 `deleted` 欄位為 true，則為資料表刪除原因。可能的值如下：  * `TABLE_EXPIRATION:` 個資料表已在設定的到期時間後刪除 * 使用者已刪除`DATASET_DELETION:`資料集 * 使用者刪除了 `USER_DELETED:` 個表格 |
| `table_deletion_time` | `TIMESTAMP` | 資料表的刪除時間。 |

為確保穩定性，建議您在資訊結構定義查詢中明確列出資料欄，而非使用萬用字元 (`SELECT *`)。明確列出資料欄可避免查詢因基礎結構定義變更而中斷。

## 範圍和語法

對這個檢視表執行的查詢必須包含[區域限定詞](https://docs.cloud.google.com/bigquery/docs/information-schema-intro?hl=zh-tw#syntax)。下表說明這個檢視畫面的區域範圍：

| 檢視表名稱 | 資源範圍 | 區域範圍 |
| --- | --- | --- |
| `` [`PROJECT_ID`.]`region-REGION`.INFORMATION_SCHEMA.TABLE_STORAGE[_BY_PROJECT] `` | 專案層級 | `REGION` |

請更改下列內容：

* 選用：`PROJECT_ID`： Google Cloud 專案的 ID。如未指定，則會使用預設專案。
* `REGION`：任何[資料集區域名稱](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)。例如：`` `region-us` ``。**注意：**您必須使用[區域限定詞](https://docs.cloud.google.com/bigquery/docs/information-schema-intro?hl=zh-tw#region_qualifier)，才能查詢 `INFORMATION_SCHEMA` 檢視表。查詢執行位置必須與 `INFORMATION_SCHEMA` 檢視表的區域相符。

以下範例說明如何傳回指定專案和區域中資料表的儲存空間資訊：

```
SELECT * FROM `myProject`.`region-REGION`.INFORMATION_SCHEMA.TABLE_STORAGE;
```

以下範例說明如何傳回目前專案中指定區域的資料表儲存空間資訊：

```
SELECT * FROM `region-REGION`.INFORMATION_SCHEMA.TABLE_STORAGE_BY_PROJECT;
```

## 範例

##### 範例 1：

以下範例顯示目前專案計費的邏輯位元組總數。

```
SELECT
  SUM(total_logical_bytes) AS total_logical_bytes
FROM
  `region-REGION`.INFORMATION_SCHEMA.TABLE_STORAGE;
```

結果大致如下：

```
+---------------------+
| total_logical_bytes |
+---------------------+
| 971329178274633     |
+---------------------+
```

##### 範例 2：

以下範例顯示目前專案在資料集層級的不同儲存空間位元組(以 GiB 為單位)。

```
SELECT
  table_schema AS dataset_name,
  -- Logical
  SUM(total_logical_bytes) / power(1024, 3) AS total_logical_gib,
  SUM(active_logical_bytes) / power(1024, 3) AS active_logical_gib,
  SUM(long_term_logical_bytes) / power(1024, 3) AS long_term_logical_gib,
  -- Physical
  SUM(total_physical_bytes) / power(1024, 3) AS total_physical_gib,
  SUM(active_physical_bytes) / power(1024, 3) AS active_physical_gib,
  SUM(active_physical_bytes - time_travel_physical_bytes) / power(1024, 3) AS active_no_tt_physical_gib,
  SUM(long_term_physical_bytes) / power(1024, 3) AS long_term_physical_gib,
  SUM(time_travel_physical_bytes) / power(1024, 3) AS time_travel_physical_gib,
  SUM(fail_safe_physical_bytes) / power(1024, 3) AS fail_safe_physical_gib
FROM
  `region-REGION`.INFORMATION_SCHEMA.TABLE_STORAGE
WHERE
  table_type ='BASE TABLE'
GROUP BY
  table_schema
ORDER BY
  dataset_name
```

##### 範例 3：

以下範例說明如何預測未來 30 天內，邏輯和實體計費模式之