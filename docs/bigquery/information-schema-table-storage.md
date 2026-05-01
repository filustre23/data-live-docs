* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [參考資料](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# TABLE\_STORAGE 檢視畫面

`INFORMATION_SCHEMA.TABLE_STORAGE` 檢視畫面會顯示資料表和具體化檢視畫面的目前儲存空間用量快照。查詢 `INFORMATION_SCHEMA.TABLE_STORAGE` 檢視表時，查詢結果會針對目前專案中的每個資料表或具體化檢視表，各列出一個相對應的資料列。

`INFORMATION_SCHEMA.TABLE_STORAGE` 檢視畫面中的資料不會即時更新，通常會延遲幾秒到幾分鐘。如果儲存空間變更僅是因為分區或資料表到期，
或是因為修改資料集時間旅行視窗，則可能需要最多一天，才會反映在 `INFORMATION_SCHEMA.TABLE_STORAGE` 檢視畫面中。
如果資料集包含超過 1,000 個資料表，且您刪除了該資料集，則只有在刪除資料集的[時空旅行視窗](https://docs.cloud.google.com/bigquery/docs/time-travel?hl=zh-tw#time_travel)結束後，這個檢視畫面才會反映變更。

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

**注意：** 檢視區塊名稱 `INFORMATION_SCHEMA.TABLE_STORAGE` 和 `INFORMATION_SCHEMA.TABLE_STORAGE_BY_PROJECT` 是同義詞，可以互換使用。

## 瞭解位元組值與計費單位的差異

`*_BYTES` 檢視畫面中的 `INFORMATION_SCHEMA.TABLE_STORAGE` 資料欄會以位元組為單位，顯示目前的儲存空間用量快照。這項指標會顯示您當時儲存的資料量。

不過，如 Cloud Billing 報表所示，BigQuery 儲存空間的帳單費用並非僅以這個即時大小為準。而是根據一段時間內儲存的資料量計算。標準計費單位為 GiB 月或 TiB 月。

舉例來說，無論當月有 28 到 31 天，只要儲存 1 GiB 滿一個月，用量就是 1 GiB-month。同樣地，如果只儲存部分月份的資料，費用也會按比例計算。在 31 天的月份中，儲存 31 GiB 一天約為 1 GiB-month；在 28 天的月份中，儲存 28 GiB 一天也約為 1 GiB-month。

雖然 `INFORMATION_SCHEMA.TABLE_STORAGE` 中的位元組值是估算潛在費用的重要輸入內容，但實際帳單會反映 `(bytes stored * duration stored)` 的持續計算結果。這個檢視畫面中的值不會直接與帳單報表中的委刊項相符，因為帳單報表中的值是帳單週期的匯總資料。

如要進一步瞭解儲存空間費用的計算方式，請參閱[儲存空間定價](https://docs.cloud.google.com/bigquery/pricing?hl=zh-tw#storage-pricing)頁面。

## 必要的角色

如要取得查詢 `INFORMATION_SCHEMA.TABLE_STORAGE` 檢視畫面所需的權限，請要求系統管理員授予您專案的「[BigQuery 中繼資料檢視者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.metadataViewer) 」(`roles/bigquery.metadataViewer`) IAM 角色。如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和機構的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

這個預先定義的角色具備查詢 `INFORMATION_SCHEMA.TABLE_STORAGE` 檢視畫面所需的權限。如要查看確切的必要權限，請展開「Required permissions」(必要權限) 部分：

#### 所需權限

如要查詢 `INFORMATION_SCHEMA.TABLE_STORAGE` 檢視畫面，必須具備下列權限：

* `bigquery.tables.get`
* `bigquery.tables.list`

您或許還可透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)取得這些權限。

## 結構定義

`INFORMATION_SCHEMA.TABLE_STORAGE` 檢視表具有下列結構定義：

| 資料欄名稱 | 資料類型 | 值 |
| --- | --- | --- |
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
| `` [`PROJECT_ID`.]`region-REGION`.INFORMATION_SCHEMA.TABLE_STORAGE[_BY_PROJECT] `` | 專案層級 | `REGION` |

取代下列項目：

* 選用：`PROJECT_ID`：專案 ID。 Google Cloud 如未指定，系統會使用預設專案。
* `REGION`：任何[資料集區域名稱](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)。
  例如：`` `region-us` ``。**注意：**您必須使用[區域限定詞](https://docs.cloud.google.com/bigquery/docs/information-schema-intro?hl=zh-tw#region_qualifier)查詢 `INFORMATION_SCHEMA` 檢視畫面。查詢執行位置必須與`INFORMATION_SCHEMA`檢視區塊的區域相符。

以下範例說明如何傳回指定專案和區域中資料表的儲存空間資訊：

```
SELECT * FROM `myProject`.`region-REGION`.INFORMATION_SCHEMA.TABLE_STORAGE;
```

以下範例說明如何傳回指定區域中，目前專案內資料表的儲存空間資訊：

```
SELECT * FROM `region-REGION`.INFORMATION_SCHEMA.TABLE_STORAGE_BY_PROJECT;
```

## 範例

##### 範例 1：

以下範例顯示目前專案的邏輯位元組總計費用。

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

以下範例顯示目前專案中，資料集層級的不同儲存空間位元組(以 GiB 為單位)。

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

以下範例說明如何預測未來 30 天內，每個資料集在邏輯和實體帳單模型之間的價格差異。這個範例假設查詢執行後 30 天內的儲存空間用量維持不變。請注意，預測僅限於基本資料表，不包括資料集內的所有其他類型資料表。

這項查詢的價格變數所用價格適用於 `us-central1` 區域。如要為其他區域執行這項查詢，請適當更新價格變數。如需價格資訊，請參閱「[儲存空間價格](https://cloud.google.com/bigquery/pricing?hl=zh-tw#storage)」。

1. 在 Google Cloud 控制台中開啟 BigQuery 頁面。

   [前往 BigQuery 頁面](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在「Query editor」(查詢編輯器) 方塊中輸入下列 GoogleSQL 查詢。
   `INFORMATION_SCHEMA` 需要使用 GoogleSQL 語法。GoogleSQL 是 Google Cloud 控制台的預設語法。

   ```
   DECLARE active_logical_gib_price FLOAT64 DEFAULT 0.02;
   DECLARE long_term_logical_gib_price FLOAT64 DEFAULT 0.01;
   DECLARE active_physical_gib_price FLOAT64 DEFAULT 0.04;
   DECLARE long_term_physical_gib_price FLOAT64 DEFAULT 0.02;

   WITH
    storage_sizes AS (
      SELECT
        table_schema AS dataset_name,
        -- Logical
        SUM(IF(deleted=false, active_logical_bytes, 0)) / power(1024, 3) AS active_logical_gib,
        SUM(IF(deleted=false, long_term_logical_bytes, 0)) / power(1024, 3) AS long_term_logical_gib,
        -- Physical
        SUM(active_physical_bytes) / power(1024, 3) AS active_physical_gib,
        SUM(active_physical_bytes - time_travel_physical_bytes) / power(1024, 3) AS active_no_tt_physical_gib,
        SUM(long_term_physical_bytes) / power(1024, 3) AS long_term_physical_gib,
        -- Restorable previously deleted physical
        SUM(time_travel_physical_bytes) / power(1024, 3) AS time_travel_physical_gib,
        SUM(fail_safe_physical_bytes) / power(1024, 3) AS fail_safe_physical_gib,
      FROM
        `region-REGION`.INFORMATION_SCHEMA.TABLE_STORAGE_BY_PROJECT
      WHERE total_physical_bytes + fail_safe_physical_bytes > 0
        -- Base the forecast on base tables only for highest precision results
        AND table_type  = 'BASE TABLE'
        GROUP BY 1
    )
   SELECT
     dataset_name,
     -- Logical
     ROUND(active_logical_gib, 2) AS active_logical_gib,
     ROUND(long_term_logical_gib, 2) AS long_term_logical_gib,
     -- Physical
     ROUND(active_physical_gib, 2) AS active_physical_gib,
     ROUND(long_term_physical_gib, 2) AS long_term_physical_gib,
     ROUND(time_travel_physical_gib, 2) AS time_travel_physical_gib,
     ROUND(fail_safe_physical_gib, 2) AS fail_safe_physical_gib,
     -- Compression ratio
     ROUND(SAFE_DIVIDE(active_logical_gib, active_no_tt_physical_gib), 2) AS active_compression_ratio,
     ROUND(SAFE_DIVIDE(long_term_logical_gib, long_term_physical_gib), 2) AS long_term_compression_ratio,
     -- Forecast costs logical
     ROUND(active_logical_gib * active_logical_gib_price, 2) AS forecast_active_logical_cost,
     ROUND(long_term_logical_gib * long_term_logical_gib_price, 2) AS forecast_long_term_logical_cost,
     -- Forecast costs physical
     ROUND((active_no_tt_physical_gib + time_travel_physical_gib + fail_safe_physical_gib) * active_physical_gib_price, 2) AS forecast_active_physical_cost,
     ROUND(long_term_physical_gib * long_term_physical_gib_price, 2) AS forecast_long_term_physical_cost,
     -- Forecast costs total
     ROUND(((active_logical_gib * active_logical_gib_price) + (long_term_logical_gib * long_term_logical_gib_price)) -
        (((active_no_tt_physical_gib + time_travel_physical_gib + fail_safe_physical_gib) * active_physical_gib_price) + (long_term_physical_gib * long_term_physical_gib_price)), 2) AS forecast_total_cost_difference
   FROM
     storage_sizes
   ORDER BY
     (forecast_active_logical_cost + forecast_active_physical_cost) DESC;
   ```

   **注意：** `INFORMATION_SCHEMA` 檢視表名稱會區分大小寫。
3. 按一下「執行」。

結果大致如下：

```
+--------------+--------------------+-----------------------+---------------------+------------------------+--------------------------+-----------------------------+------------------------------+----------------------------------+-------------------------------+----------------------------------+--------------------------------+
| dataset_name | active_logical_gib | long_term_logical_gib | active_physical_gib | long_term_physical_gib | active_compression_ratio | long_term_compression_ratio | forecast_active_logical_cost | forecaset_long_term_logical_cost | forecast_active_physical_cost | forecast_long_term_physical_cost | forecast_total_cost_difference |
+--------------+--------------------+-----------------------+---------------------+------------------------+--------------------------+-----------------------------+------------------------------+----------------------------------+-------------------------------+----------------------------------+--------------------------------+
| dataset1     |               10.0 |                  10.0 |                 1.0 |                    1.0 |                     10.0 |                        10.0 |                          0.2 |                              0.1 |                          0.04 |                             0.02 |                           0.24 |
```

## 疑難排解

如要啟用這個檢視畫面，請在專案或機構中將 `enable_info_schema_storage` 的值設為 `TRUE`。如要進一步瞭解如何管理設定，請參閱「[管理設定](https://docs.cloud.google.com/bigquery/docs/default-configuration?hl=zh-tw)」。

如果尚未設定，您會看到下列錯誤訊息：

```
INFORMATION_SCHEMA.TABLE_STORAGE hasn't been enabled for project <myproject>.
Consider using one of the following SQL statements to enable data collection:
ALTER PROJECT `<myproject>`
SET OPTIONS (`region-<region>.enable_info_schema_storage` = TRUE)

Or to enable for the entire organization:
ALTER ORGANIZATION
SET OPTIONS (`region-<region>.enable_info_schema_storage` = TRUE)

After enabling, please allow around 1 day for the complete historical data to
become available.
```

執行錯誤訊息中說明的 SQL 陳述式，啟用檢視畫面。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-04-30 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-04-30 (世界標準時間)。"],[],[]]