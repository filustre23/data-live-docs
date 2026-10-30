Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [參考資料](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 系統變數參考資料

BigQuery 支援下列系統變數，可用於[多陳述式查詢](https://docs.cloud.google.com/bigquery/docs/multi-statement-queries?hl=zh-tw)或[工作階段](https://docs.cloud.google.com/bigquery/docs/sessions-intro?hl=zh-tw)。您可以使用系統變數，在查詢執行期間設定或擷取資訊，類似於使用者定義的[程序語言變數](https://docs.cloud.google.com/bigquery/docs/multi-statement-queries?hl=zh-tw#variables)。

| 名稱 | 類型 | 讀取及寫入或唯讀 | 說明 |
| --- | --- | --- | --- |
| `@@current_job_id` | `STRING` | 唯讀 | 目前執行中工作的 ID。在多陳述式查詢中，這會傳回負責目前陳述式的工作，而非整個多陳述式查詢。 |
| `@@dataset_id` | `STRING` | 讀取及寫入 | 目前專案中預設資料集的 ID。如果查詢中的專案未指定資料集，系統就會使用這個 ID。您可以使用 `SET` 陳述式，將 `@@dataset_id` 指派給目前專案中的其他資料集 ID。系統變數 `@@dataset_project_id` 和 `@@dataset_id` 可以一併設定及使用。 |
| `@@dataset_project_id` | `STRING` | 讀取及寫入 | 如果查詢中使用的資料集未指定專案，系統會使用預設專案的 ID。如果未設定 `@@dataset_project_id`，或設為 `NULL`，則會使用執行查詢的專案 (`@@project_id`)。您可以使用 `SET` 陳述式，將 `@@dataset_project_id` 指派給其他專案 ID。系統變數 `@@dataset_project_id` 和 `@@dataset_id` 可以一併設定及使用。 |
| `@@last_job_id` | `STRING` | 唯讀 | 在目前的多重陳述式查詢中，最近執行的工作 ID (不含目前的工作)。如果多重陳述式查詢包含 `CALL` 陳述式，這項工作可能源自其他程序。 |
| `@@location` | `STRING` | 讀取及寫入 | 執行查詢的位置。`@@location` 只能設為包含[有效位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw#supported_locations)的字串常值。`SET @@location` 陳述式必須是查詢中的第一個陳述式。如果 `@@location` 與查詢的其他[位置資訊設定](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw#specify_locations)不符，就會發生錯誤。您可以使用[選用的工作建立模式](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#optional-job-creation)，改善設定 `@@location` 的查詢延遲時間。您可以在 [SQL UDF](https://docs.cloud.google.com/bigquery/docs/user-defined-functions?hl=zh-tw#sql-udf-structure) 和[資料表函式](https://docs.cloud.google.com/bigquery/docs/table-functions?hl=zh-tw)中使用 `@@location` 系統變數。 |
| `@@max_staleness_override` | `INTERVAL` | 讀取及寫入 | 覆寫目前多重陳述式查詢或工作階段中，所有適用實體的過時時間間隔上限。適用的實體包括在目前多重陳述式查詢或工作階段中查詢的[串流資料表](https://docs.cloud.google.com/bigquery/docs/write-api-grpc?hl=zh-tw#query-streamed-data-max-staleness)、[變更資料擷取 (CDC) 資料表](https://docs.cloud.google.com/bigquery/docs/change-data-capture?hl=zh-tw#query-max-staleness)和[materialized view](https://docs.cloud.google.com/bigquery/docs/materialized-views-create?hl=zh-tw#max_staleness)。 根據預設，每次執行查詢時，BigQuery 都會傳回最新結果，或遵循實體設定的 `max_staleness` 選項。您可以使用 `@@max_staleness_override` 動態自訂過時行為，而不必變更資料表或檢視表設定：   * **縮短查詢延遲時間並降低費用：**如要容許過時資料，請將 `@@max_staleness_override` 設為非負間隔，例如 `INTERVAL 10 MINUTE`。 * **確保結果完全符合最新狀態：**如要強制在查詢執行時套用待處理的修改或重新整理，請將 `@@max_staleness_override` 設為 `INTERVAL 0 SECOND`。 * **清除覆寫：**如要還原為實體層級 `max_staleness` 設定，請將 `@@max_staleness_override` 設為 `NULL`。 |
| `@@project_id` | `STRING` | 唯讀 | 用於執行目前查詢的專案 ID。在程序中，`@@project_id` 是指執行多重陳述式查詢的專案，而非擁有程序的專案。 |
| `@@query_label` | `STRING` | 讀取及寫入 | 要與目前多重陳述式查詢或工作階段中的查詢工作建立關聯的查詢標籤。如果是在查詢中設定，指令碼或工作階段中所有後續的查詢工作都會有這個標籤。如未在查詢中設定，這個系統變數的值為 `NULL`。如需設定這個系統變數的範例，請參閱「[將工作階段中的工作與標籤建立關聯](https://docs.cloud.google.com/bigquery/docs/adding-labels?hl=zh-tw#adding-label-to-session)」。 |
| `@@reservation` | `STRING` | 讀取及寫入 | 可讓您指定或覆寫要用於執行下列陳述式的預留項目。 必須採用下列格式：`projects/project_id/locations/location/reservations/reservation_id`。 設為 `'none'` 時，系統會強制查詢使用隨選計費模式。這項操作需要將專案或組織的 `reservation_override_mode` 設為 `ALLOW_ANY_OVERRIDE`。您可以使用 [`ALTER PROJECT SET OPTIONS`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#alter_project_set_options_statement) 或 [`ALTER ORGANIZATION SET OPTIONS`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#alter_organization_set_options_statement) 陳述式設定這個值。如有任何問題，請[尋求支援](https://docs.cloud.google.com/bigquery/docs/getting-support?hl=zh-tw)。  預留項目的位置必須與查詢執行位置相符。如果 `@@reservation` 為 `NULL`，系統會根據與查詢屬性相符的[指派設定](https://docs.cloud.google.com/bigquery/docs/reservations-assignments?hl=zh-tw)，自動偵測預留項目。 |
| `@@row_count` | `INT64` | 唯讀 | 如果用於多陳述式查詢，且前一個陳述式為 DML，則會指定該 DML 陳述式插入、修改或刪除的資料列數量。如果前一個陳述式是 `MERGE` 陳述式，`@@row_count` 代表插入、修改和刪除的資料列總數。如果不是多重陳述式查詢，這個值會是 `NULL`。 |
| `@@script.bytes_billed` | `INT64` | 唯讀 | 目前執行的多重陳述式查詢工作中，目前為止計費的總位元組數。如果不在工作中，這個值為 `NULL`。 |
| `@@script.bytes_processed` | `INT64` | 唯讀 | 目前執行的多重陳述式查詢工作中，至今處理的總位元組數。如果不在工作中，這個值會是 `NULL`。 |
| `@@script.creation_time` | `TIMESTAMP` | 唯讀 | 目前執行的多重陳述式查詢工作建立時間。如果不在工作中，這個值會是 `NULL`。 |
| `@@script.job_id` | `STRING` | 唯讀 | 目前執行的多重陳述式查詢工作 ID。如果不在工作中，則此值為 `NULL`。 |
| `@@script.num_child_jobs` | `INT64` | 唯讀 | 目前已完成的子項工作數量。如果不在工作中，這個值會是 `NULL`。 |
| `@@script.slot_ms` | `INT64` | 唯讀 | 指令碼目前使用的運算單元毫秒數。 如果不在工作中，這個值會是 `NULL`。 |
| `@@session_id` | `STRING` | 唯讀 | 與目前查詢相關聯的工作階段 ID。您可以在 [SQL user-defined function](https://docs.cloud.google.com/bigquery/docs/user-defined-functions?hl=zh-tw#sql-udf-structure)、[資料表函式](https://docs.cloud.google.com/bigquery/docs/table-functions?hl=zh-tw)和[邏輯檢視表](https://docs.cloud.google.com/bigquery/docs/views?hl=zh-tw)中使用 `@@session_id` 系統變數。materialized view 不支援使用這個系統變數。 |
| `@@time_zone` | `STRING` | 讀取及寫入 | 受時區影響的 SQL 函式中，如未指定時區做為引數，就會使用這個預設時區。您可以使用 `SET` 陳述式，將 `@@time_zone` 修改為任何有效的時區名稱。在每個指令碼的開頭，`@@time_zone` 會以「UTC」開始。 |

為確保回溯相容性，`OPTIONS` 或 `FOR SYSTEM TIME AS OF` 子句中使用的運算式預設為 `America/Los_Angeles` 時區，而所有其他日期/時間運算式則預設為 `UTC` 時區。如果在多陳述式查詢中已預先設定 `@@time_zone`，則所選時區會套用至所有日期/時間運算式，包括 `OPTIONS` 和 `FOR SYSTEM TIME AS OF` 子句。

除了先前顯示的系統變數外，您也可以在執行多陳述式查詢時使用 `EXCEPTION` 系統變數。如要進一步瞭解 `EXCEPTION` 系統變數，請參閱程序語言陳述式 [BEGIN...EXCEPTION](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/procedural-language?hl=zh-tw#beginexceptionend)。

## 範例

您無法建立系統變數，但可以覆寫部分變數的預設值：

```
SET @@dataset_project_id = 'MyProject';
```

以下範例會將工作階段中後續查詢的最大過時時間間隔覆寫為 10 分鐘：

```
SET @@max_staleness_override = INTERVAL 10 MINUTE;
```

如要強制查詢傳回最新結果，並在查詢執行時套用待處理的修改，請按照下列步驟操作：

```
SET @@max_staleness_override = INTERVAL 0 SECOND;
```

如要將過時覆寫值重設回資料表層級設定，請將 `@@max_staleness_override` 設為 `NULL`：

```
SET @@max_staleness_override = NULL;
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

系統變數可與 DDL 和 DML 查詢搭配使用。舉例來說，在建立及更新資料表時，可以透過下列幾種方式使用系統變數 `@@time_zone`：

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

在某些情況下，系統變數無法用於 DDL 和 DML 查詢。例如，您無法將系統變數用作專案名稱、資料集或資料表名稱。如果在資料表路徑中加入 `@@dataset_id` 系統變數，下列查詢會產生錯誤：

```
BEGIN
  CREATE TEMP TABLE @@dataset_id.MyTempTable (id STRING);
END;
```

如要進一步瞭解如何在多陳述式查詢中使用系統變數，請參閱「[設定變數](https://docs.cloud.google.com/bigquery/docs/multi-statement-queries?hl=zh-tw#set_system_variable)」。

如需在工作階段中使用系統變數的範例，請參閱「[工作階段範例](https://docs.cloud.google.com/bigquery/docs/sessions-write-queries?hl=zh-tw#session_system_variables)」。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-10-29 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-10-29 (世界標準時間)。"],[],[]]