Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [參考資料](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# TABLE\_STORAGE\_BY\_FOLDER 檢視畫面

`INFORMATION_SCHEMA.TABLE_STORAGE_BY_FOLDER` 檢視表會為目前專案上層資料夾中的每個資料表或具體化檢視表 (包括子資料夾)，各包含一個資料列。

這個表格不會維護即時資料，可能會有幾秒到幾分鐘的延遲。如果儲存空間變更是由於分區或資料表到期，或是修改資料集時間回溯期所致，最多可能需要一天才會顯示在 `INFORMATION_SCHEMA.TABLE_STORAGE` 檢視畫面中。如果刪除含有超過 1,000 個資料表的資料集，系統不會立即反映這項變更，直到刪除資料集的[時間旅行視窗](https://docs.cloud.google.com/bigquery/docs/time-travel?hl=zh-tw#time_travel)結束為止。

透過表格儲存空間檢視畫面，您可以輕鬆觀察目前的儲存空間使用量，並詳細瞭解儲存空間是使用邏輯未壓縮位元組、實體壓縮位元組還是時空旅行位元組。這項資訊可協助您規劃未來的成長，並瞭解表格的更新模式。

## `*_BYTES` 欄中包含的資料

表格儲存空間檢視畫面中的 `*_BYTES` 欄位包含儲存空間位元組用量資訊。系統會根據具體化檢視區塊和下列類型的資料表儲存空間用量，判斷這項資訊：

* 透過「[建立及使用資料表](https://docs.cloud.google.com/bigquery/docs/tables?hl=zh-tw)」一文所述的任何方法建立的永久資料表。
* 在[工作階段](https://docs.cloud.google.com/bigquery/docs/sessions-write-queries?hl=zh-tw#use_temporary_tables_in_sessions)中建立的暫時資料表。這些資料表會放入名稱類似「\_c018003e063d09570001ef33ae401fad6ab92a6a」的資料集。
* 在[多重陳述式查詢](https://docs.cloud.google.com/bigquery/docs/multi-statement-queries?hl=zh-tw#temporary_tables) (「指令碼」) 中建立的臨時資料表。這些資料表會放入名稱類似「\_\_script72280c173c88442c3a7200183a50eeeaa4073719」的資料集。

系統不會向您收取[查詢結果快取](https://docs.cloud.google.com/bigquery/docs/writing-results?hl=zh-tw#temporary_and_permanent_tables)中儲存的資料費用，因此不會將這類資料納入 `*_BYTES` 欄值。

複製和快照會顯示 `*_BYTES` 資料欄值，就像是完整的資料表，而不是顯示與基本資料表所用儲存空間的差異，因此會高估。帳單會正確計算儲存空間用量差異。如要進一步瞭解複製和快照儲存及計費的差異位元組，請參閱[`TABLE_STORAGE_USAGE_TIMELINE`
檢視畫面](https://docs.cloud.google.com/bigquery/docs/information-schema-table-storage-usage?hl=zh-tw)。

## 預測儲存空間帳單

如要預測資料集的每月儲存空間費用，您可以使用這個檢視畫面中的 `logical` 或 `physical *_BYTES` 欄，具體取決於資料集使用的[資料集儲存空間計費模式](https://docs.cloud.google.com/bigquery/docs/datasets-intro?hl=zh-tw#dataset_storage_billing_models)。請注意，這只是粗略的預測，實際帳單金額是根據 BigQuery 儲存空間帳單基礎架構的用量計算，並顯示在 Cloud Billing 中。

如果資料集使用邏輯帳單模型，您可以按照下列方式預估每月儲存空間費用：

((`ACTIVE_LOGICAL_BYTES` 值 / `POW`(1024, 3)) \* 使用中的邏輯位元組價格) +
((`LONG_TERM_LOGICAL_BYTES` 值 / `POW`(1024, 3)) \* 長期邏輯位元組價格)

資料表的 `ACTIVE_LOGICAL_BYTES` 值會反映該資料表目前使用的有效位元組。

如果資料集採用實體計費模式，您可以按照下列方式預測儲存空間費用：

((`ACTIVE_PHYSICAL_BYTES + FAIL_SAFE_PHYSICAL_BYTES` 值 / `POW`(1024, 3)) \* 作用中實體位元組價格) +
((`LONG_TERM_PHYSICAL_BYTES` 值 / `POW`(1024, 3)) \* 長期實體位元組價格)

資料表的 `ACTIVE_PHYSICAL_BYTES` 值反映該資料表目前使用的有效位元組，以及該資料表用於時空旅行的位元組。

如要查看表格的有效位元組，請從 `ACTIVE_PHYSICAL_BYTES` 值減去 `TIME_TRAVEL_PHYSICAL_BYTES` 值。

詳情請參閱「[儲存空間定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#storage)」。

## 所需權限

如要查詢 `INFORMATION_SCHEMA.TABLE_STORAGE_BY_FOLDER` 檢視畫面，您必須具備專案父項資料夾的下列 Identity and Access Management (IAM) 權限：

* `bigquery.tables.get`
* `bigquery.tables.list`

下列每個預先定義的 IAM 角色都包含上述權限：

* `roles/bigquery.admin`
* `roles/bigquery.dataViewer`
* `roles/bigquery.dataEditor`
* `roles/bigquery.metadataViewer`

如要進一步瞭解 BigQuery 權限，請參閱 [BigQuery IAM 角色和權限](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)。

## 結構定義

`INFORMATION_SCHEMA.TABLE_STORAGE_BY_FOLDER` 檢視表具有下列結構定義：

| 資料欄名稱 | 資料類型 | 值 |
| --- | --- | --- |
| `folder_numbers` | `REPEATED INTEGER` | 含有專案的資料夾 ID 編號，從直接含有專案的資料夾開始，接著是含有子資料夾的資料夾，依此類推。舉例來說，如果 `folder_numbers` 是 `[1, 2, 3]`，則資料夾 `1` 會立即包含專案，資料夾 `2` 包含 `1`，而資料夾 `3` 包含 `2`。這個欄位只會在 `TABLE_STORAGE_BY_FOLDER` 中填入資料。 |
| `project_id` | `STRING` | 資料集所屬專案的專案 ID。 |
| `project_number` | `INT64` | 資料集所屬專案的專案編號。 |
| `table_catalog` | `STRING` | 資料集所屬專案的專案 ID。 |
| `table_schema` | `STRING` | 包含資料表或具體化檢視的資料集名稱，又稱為 `datasetId`。 |
| `table_name` | `STRING` | 資料表或具體化檢視表的名稱，又稱為 `tableId`。 |
| `creation_time` | `TIMESTAMP` | 資料表的建立時間。 |
| `total_rows` | `INT64` | 資料表或具體化檢視中的資料列總數。 |
| `total_partitions` | `INT64` | 資料表或具體化檢視中的分區數。未分區資料表會傳回 0。 |
| `total_logical_bytes` | `INT64` | 資料表或具體化檢視區塊中的邏輯 (未壓縮) 位元組總數。 |
| `active_logical_bytes` | `INT64` | 未滿 90 天的邏輯 (未壓縮) 位元組數。 |
| `long_term_logical_bytes` | `INT64` | 超過 90 天的邏輯 (未壓縮) 位元組數。 |
| `current_physical_bytes` | `INT64` | 目前儲存的資料表在所有分區中的實際位元組總數。 |
| `total_physical_bytes` | `INT64` | 儲存空間使用的實體 (壓縮) 位元組總數，包括使用中、長期和時空旅行 (已刪除或變更的資料) 位元組。不包括安全防護 (時間回溯期後保留的已刪除或變更資料) 位元組。 |
| `active_physical_bytes` | `INT64` | 90 天內實體 (壓縮) 位元組數，包括時間旅行 (已刪除或變更的資料) 位元組。 |
| `long_term_physical_bytes` | `INT64` | 超過 90 天的實體 (壓縮) 位元組數。 |
| `time_travel_physical_bytes` | `INT64` | 時空旅行儲存空間 (已刪除或變更的資料) 使用的實體 (壓縮) 位元組數。 |
| `storage_last_modified_time` | `TIMESTAMP` | 資料最近一次寫入資料表的時間。如果沒有任何資料，則傳回 `NULL`。 |
| `deleted` | `BOOLEAN` | 指出資料表是否已刪除。 |
| `table_type` | `STRING` | 資料表類型。例如 `BASE TABLE`。 |
| `managed_table_type` | `STRING` | 這一欄目前為預先發布版。資料表的受管理類型。例如 `NATIVE` 或 `BIGLAKE`。 |
| `fail_safe_physical_bytes` | `INT64` | 安全儲存空間 (已刪除或變更的資料) 使用的實體 (壓縮) 位元組數。 |
| `last_metadata_index_refresh_time` | `TIMESTAMP` | 資料表上次重新整理中繼資料索引的時間。 |
| `table_deletion_reason` | `STRING` | 如果 `deleted` 欄位為 true，則為資料表刪除原因。可能的值如下：  * 資料表在設定的到期時間後遭到刪除`TABLE_EXPIRATION:` * 使用者已刪除資料集`DATASET_DELETION:` * 使用者已刪除 `USER_DELETED:` 個表格 |
| `table_deletion_time` | `TIMESTAMP` | 資料表的刪除時間。 |

為確保穩定性，建議您在資訊結構定義查詢中明確列出資料欄，而非使用萬用字元 (`SELECT *`)。明確列出資料欄可避免基礎結構定義變更時，查詢中斷。

## 範圍和語法

對這個檢視表執行的查詢必須包含[區域限定詞](https://docs.cloud.google.com/bigquery/docs/information-schema-intro?hl=zh-tw#syntax)。下表說明這個檢視畫面的區域範圍：

| 檢視表名稱 | 資源範圍 | 區域範圍 |
| --- | --- | --- |
| `` [`PROJECT_ID`.]`region-REGION`.INFORMATION_SCHEMA.TABLE_STORAGE_BY_FOLDER `` | 包含指定專案的資料夾 | `REGION` |

取代下列項目：

* 選用：`PROJECT_ID`：專案 ID。 Google Cloud 如未指定，系統會使用預設專案。
* `REGION`：任何[資料集區域名稱](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)。
  例如：`` `region-us` ``。**注意：**您必須使用[區域限定詞](https://docs.cloud.google.com/bigquery/docs/information-schema-intro?hl=zh-tw#region_qualifier)查詢 `INFORMATION_SCHEMA` 檢視畫面。查詢執行位置必須與`INFORMATION_SCHEMA`檢視區塊的區域相符。

如要擷取指定專案父項資料夾中資料表的儲存空間資訊，請執行下列查詢：

```
SELECT * FROM `myProject`.`region-REGION`.INFORMATION_SCHEMA.TABLE_STORAGE_BY_FOLDER;
```

## 範例

下列查詢會顯示資料夾中哪些專案使用的儲存空間最多：

```
SELECT
  project_id,
  SUM(total_logical_bytes) AS total_logical_bytes
FROM
  `region-REGION`.INFORMATION_SCHEMA.TABLE_STORAGE_BY_FOLDER
GROUP BY
  project_id
ORDER BY
  total_logical_bytes DESC;
```

結果大致如下：

```
+---------------------+---------------------+
|     project_id      | total_logical_bytes |
+---------------------+---------------------+
| projecta            |     971329178274633 |
+---------------------+---------------------+
| projectb            |     834638211024843 |
+---------------------+---------------------+
| projectc            |     562910385625126 |
+---------------------+---------------------+
```




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-16 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-16 (世界標準時間)。"],[],[]]