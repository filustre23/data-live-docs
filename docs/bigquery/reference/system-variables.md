* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [參考資料](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 系統變數參考資料

BigQuery 支援下列系統變數，可用於[多重陳述式查詢](https://docs.cloud.google.com/bigquery/docs/multi-statement-queries?hl=zh-tw)或[工作階段](https://docs.cloud.google.com/bigquery/docs/sessions-intro?hl=zh-tw)中。
您可以在查詢執行期間設定或擷取資訊，做法與使用者定義的[程序語言變數](https://docs.cloud.google.com/bigquery/docs/multi-statement-queries?hl=zh-tw#variables)類似。

| 名稱 | 類型 | 讀取及寫入或唯讀 | 說明 |
| --- | --- | --- | --- |
| `@@current_job_id` | `STRING` | 唯讀 | 目前正在執行的工作 ID。如果是多陳述式查詢，這項函式會傳回負責目前陳述式的工作，而非整個多陳述式查詢。 |
| `@@dataset_id` | `STRING` | 讀取及寫入 | 目前專案中預設資料集的 ID。如果查詢中未指定專案的資料集，系統就會使用這個 ID。您可以使用 `SET` 陳述式，將 `@@dataset_id` 指派給目前專案中的另一個資料集 ID。系統變數 `@@dataset_project_id` 和 `@@dataset_id` 可以一併設定及使用。 |
| `@@dataset_project_id` | `STRING` | 讀取及寫入 | 如果查詢中使用的資料集未指定專案，系統會使用這個預設專案的 ID。如未設定 `@@dataset_project_id`，或設為 `NULL`，系統會使用查詢執行專案 (`@@project_id`)。您可以使用 `SET` 陳述式，將 `@@dataset_project_id` 指派給其他專案 ID。系統變數 `@@dataset_project_id` 和 `@@dataset_id` 可以一併設定及使用。 |
| `@@last_job_id` | `STRING` | 唯讀 | 目前多重陳述式查詢中最近執行的工作 ID，不包括目前的工作。如果多重陳述式查詢包含 `CALL` 陳述式，這項工作可能源自其他程序。 |
| `@@location` | `STRING` | 讀取及寫入 | 執行查詢的位置。`@@location` 只能設為具有[有效位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw#supported_locations)的字串常值。`SET @@location` 陳述式必須是查詢中的第一個陳述式。如果查詢的`@@location`與其他[位置設定](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw#specify_locations)不符，就會發生錯誤。如要改善設定 `@@location` 的查詢延遲時間，可以使用[選用的工作建立模式](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#optional-job-creation)。您可以在 [SQL UDF](https://docs.cloud.google.com/bigquery/docs/user-defined-functions?hl=zh-tw#sql-udf-structure) 和[資料表函式](https://docs.cloud.google.com/bigquery/docs/table-functions?hl=zh-tw)中使用 `@@location` 系統變數。 |
| `@@project_id` | `STRING` | 唯讀 | 用於執行目前查詢的專案 ID。在程序環境中，`@@project_id` 是指執行多重陳述式查詢的專案，而非擁有程序的專案。 |
| `@@query_label` | `STRING` | 讀取及寫入 | 要與目前多重陳述式查詢或工作階段中的查詢工作建立關聯的查詢標籤。如果在查詢中設定，指令碼或工作階段中的所有後續查詢工作都會有這個標籤。 如果未在查詢中設定，這個系統變數的值為 `NULL`。如要查看如何設定這個系統變數的範例，請參閱「[將工作階段中的工作與標籤建立關聯](https://docs.cloud.google.com/bigquery/docs/adding-labels?hl=zh-tw#adding-label-to-session)」。 |
| `@@reservation` | `STRING` | 讀取及寫入 | 可讓您指定或覆寫用於執行下列陳述式的預留項目。 格式必須為： `projects/project_id/locations/location/reservations/reservation_id`。 如要強制查詢使用隨選計費，請將這個變數設為 `'none'`。專案或機構必須將 `reservation_override_mode` 設為 `ALLOW_ANY_OVERRIDE`，才能啟用這項功能。  預訂位置必須與執行查詢的位置相符。如果 `@@reservation` 為 `NULL`，系統會根據符合查詢屬性的[指派設定](https://docs.cloud.google.com/bigquery/docs/reservations-assignments?hl=zh-tw)，自動偵測保留項目。 |
| `@@row_count` | `INT64` | 唯讀 | 如果用於多重陳述式查詢，且前一個陳述式是 DML，則指定因該 DML 陳述式而插入、修改或刪除的資料列數。如果前一個陳述式是 `MERGE` 陳述式，`@@row_count` 代表插入、修改及刪除的資料列總數。如果不在多重陳述式查詢中，這個值為 `NULL`。 |
| `@@script.bytes_billed` | `INT64` | 唯讀 | 目前執行的多重陳述式查詢工作至今已計費的位元組總數。如果不在工作中，這個值為 `NULL`。 |
| `@@script.bytes_processed` | `INT64` | 唯讀 | 目前執行的多重陳述式查詢工作至今處理的總位元組數。如果不在工作中，這個值為 `NULL`。 |
| `@@script.creation_time` | `TIMESTAMP` | 唯讀 | 目前執行的多重陳述式查詢工作建立時間。如果不在工作中，這個值為 `NULL`。 |
| `@@script.job_id` | `STRING` | 唯讀 | 目前執行的多重陳述式查詢作業工作 ID。如果不在工作中，這個值為 `NULL`。 |
| `@@script.num_child_jobs` | `INT64` | 唯讀 | 目前已完成的子項工作數量。如果不在工作中，這個值為 `NULL`。 |
| `@@script.slot_ms` | `INT64` | 唯讀 | 指令碼目前使用的時段毫秒數。 如果不在工作中，這個值為 `NULL`。 |
| `@@session_id` | `STRING` | 唯讀 | 與目前查詢相關聯的工作階段 ID。您可以在 [SQL 使用者定義函式](https://docs.cloud.google.com/bigquery/docs/user-defined-functions?hl=zh-tw#sql-udf-structure)、[資料表函式](https://docs.cloud.google.com/bigquery/docs/table-functions?hl=zh-tw)和[邏輯檢視區塊](https://docs.cloud.google.com/bigquery/docs/views?hl=zh-tw)中使用 `@@session_id` 系統變數。系統不支援在具體化檢視表中使用這個系統變數。 |
| `@@time_zone` | `STRING` | 讀取及寫入 | 受時區影響的 SQL 函式中，如未指定時區做為引數，就會使用這個預設時區。`@@time_zone` 可以使用 `SET` 陳述式修改為任何有效的時區名稱。每個指令碼的開頭，`@@time_zone` 都會以「UTC」開頭。 |

為確保回溯相容性，`OPTIONS` 或 `FOR SYSTEM TIME AS OF` 子句中使用的運算式預設為 `America/Los_Angeles` 時區，而所有其他日期/時間運算式則預設為 `UTC` 時區。如果多重陳述式查詢中已設定 `@@time_zone`，所選時區會套用至所有日期/時間運算式，包括 `OPTIONS` 和 `FOR SYSTEM TIME AS OF` 子句。

除了先前顯示的系統變數外，您也可以在執行多重陳述式查詢時使用 `EXCEPTION` 系統變數。如要進一步瞭解 `EXCEPTION` 系統變數，請參閱程序語言陳述式 [BEGIN...EXCEPTION](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/procedural-language?hl=zh-tw#beginexceptionend)。

## 範例

您無法建立系統變數，但可以覆寫部分變數的預設值：

```
SET @@dataset_project_id = 'MyProject';
```

下列查詢會傳回預設時區：

```
SELECT @@time_zone AS default_time_zone;
```

```
+-------------------+
| default_time_zone |
+-------------------+
| UTC               |
+-------------------+
```

您可以在 DDL 和 DML 查詢中使用系統變數。
舉例來說，以下是建立及更新資料表時使用系統變數 `@@time_zone` 的幾種方式：

```
BEGIN
  CREATE TEMP TABLE MyTempTable
  AS SELECT @@time_zone AS default_time_zone;
END;
```

```
CREATE OR REPLACE TABLE MyDataset.MyTable(default_time_zone STRING)
  OPTIONS (description = @@time_zone);
```

```
UPDATE MyDataset.MyTable
SET default_time_zone = @@time_zone
WHERE TRUE;
```

在 DDL 和 DML 查詢中，有些位置無法使用系統變數。舉例來說，您無法將系統變數做為專案名稱、資料集或表格名稱。在資料表路徑中加入 `@@dataset_id` 系統變數時，下列查詢會產生錯誤：

```
BEGIN
  CREATE TEMP TABLE @@dataset_id.MyTempTable (id STRING);
END;
```

如要查看如何在多陳述式查詢中使用系統變數的更多範例，請參閱「[設定變數](https://docs.cloud.google.com/bigquery/docs/multi-statement-queries?hl=zh-tw#set_system_variable)」。

如需在工作階段中使用系統變數的範例，請參閱[範例工作階段](https://docs.cloud.google.com/bigquery/docs/sessions-write-queries?hl=zh-tw#session_system_variables)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-04-21 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-04-21 (世界標準時間)。"],[],[]]