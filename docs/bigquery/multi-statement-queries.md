Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 使用多陳述式查詢

*多重陳述式查詢*是一組 SQL 陳述式，可按照共用狀態的序列執行。

本文說明如何在 BigQuery 中使用多重陳述式查詢，例如如何編寫多重陳述式查詢、在多重陳述式查詢中使用暫時性資料表、在多重陳述式查詢中參照變數，以及偵錯多重陳述式查詢。

多重陳述式查詢通常用於[預存程序](https://docs.cloud.google.com/bigquery/docs/procedures?hl=zh-tw)，並支援[程序語言陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/procedural-language?hl=zh-tw)，可讓您定義變數及實作控制流程等作業。多重陳述式查詢可包含具有副作用的 DDL 和 DML 陳述式，例如建立或修改資料表或資料表資料。

## 撰寫、執行及儲存多重陳述式查詢

多重陳述式查詢包含一或多個以半形分號分隔的 SQL 陳述式。多重陳述式查詢可使用任何有效的 SQL 陳述式。多重陳述式查詢也可以包含[程序語言陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/procedural-language?hl=zh-tw)，讓您使用變數或透過 SQL 陳述式實作控制流程。

### 撰寫多重陳述式查詢

您可以在 BigQuery 中撰寫多個陳述式查詢。下列多重陳述式查詢會宣告變數，並在 [`IF`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/procedural-language?hl=zh-tw#if) 陳述式中使用該變數：

```
DECLARE day INT64;
SET day = (SELECT EXTRACT(DAYOFWEEK from CURRENT_DATE));
if day = 1 or day = 7 THEN
  SELECT 'Weekend';
ELSE
  SELECT 'Weekday';
END IF
```

BigQuery 會將任何含有多個陳述式的請求解讀為多重陳述式查詢，除非該陳述式完全由 `CREATE TEMP FUNCTION` 陳述式組成，且後面接著單一 `SELECT` 陳述式。舉例來說，下列查詢不屬於多重陳述式查詢：

```
CREATE TEMP FUNCTION Add(x INT64, y INT64) AS (x + y);
SELECT Add(3, 4);
```

### 執行多陳述式查詢

您可以執行多重陳述式查詢，方式與執行任何其他查詢相同，例如在 Google Cloud 控制台中或使用 bq 指令列工具。

### 模擬測試多陳述式查詢

如要估算多重陳述式查詢讀取的位元組數，請考慮執行[模擬測試](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#dry-run)。如果查詢只包含 `SELECT` 陳述式，對多重陳述式查詢執行模擬測試時，結果最為準確。

模擬執行會特別處理下列查詢和陳述式類型：

* `CALL` 陳述式：模擬測試會驗證所呼叫的程序是否存在，以及是否具有與所提供引數相符的簽章。系統不會驗證所呼叫程序中的內容，以及 `CALL` 陳述式後的所有陳述式。
* [DDL 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw)：
  模擬測試會驗證第一個 DDL 陳述式，然後停止。後續所有陳述式都會略過。不支援模擬測試 `CREATE TEMP TABLE` 陳述式。
* [DML 陳述式](https://docs.cloud.google.com/bigquery/docs/data-manipulation-language?hl=zh-tw)：模擬測試會驗證 DML 陳述式，然後繼續驗證後續陳述式。在這種情況下，位元組估算值會以原始表格大小為準，不會將 DML 陳述式的結果納入考量。
* `EXECUTE IMMEDIATE` 陳述式：模擬測試會驗證查詢運算式，但不會評估動態查詢本身。系統會略過 `EXECUTE IMMEDIATE` 陳述式後的所有陳述式。
* 在分區篩選器中使用變數的查詢：試算會驗證初始查詢和後續陳述式。不過，模擬執行無法計算分區篩選器中變數的執行階段值。這會影響讀取的位元組數估算值。
* 在 `FOR SYSTEM TIME AS OF` 子句的時間戳記運算式中使用變數的查詢：試算表會使用資料表的目前內容，並忽略 `FOR SYSTEM TIME AS OF` 子句。如果目前資料表與先前疊代版本的大小不同，這會影響讀取的位元組估計值。
* `FOR`、`IF` 和 `WHILE` 控制陳述式：模擬測試會立即停止。條件運算式、控制陳述式主體和所有後續陳述式都不會經過驗證。

系統會盡力執行試運轉，但基礎程序可能會變更。模擬測試須符合下列規定：

* 成功完成模擬執行的查詢可能無法順利執行。
  舉例來說，查詢可能會在執行階段失敗，但模擬測試不會偵測到這些原因。
* 成功執行的查詢可能無法順利完成模擬測試。
  舉例來說，查詢可能會因執行時發現的原因，導致模擬測試失敗。
* 成功執行的模擬測試不保證日後也能順利執行。舉例來說，如果對模擬執行實作項目進行變更，可能會偵測到先前未偵測到的查詢錯誤。

### 儲存多重陳述式查詢

如要儲存多個陳述式查詢，請參閱「[使用已儲存的查詢](https://docs.cloud.google.com/bigquery/docs/work-with-saved-queries?hl=zh-tw)」。

## 在多陳述式查詢中使用變數

多重陳述式查詢可包含[使用者建立的變數](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/procedural-language?hl=zh-tw#declare)和[系統變數](https://docs.cloud.google.com/bigquery/docs/reference/system-variables?hl=zh-tw)。

* 您可以宣告使用者建立的變數、為變數指派值，並在整個查詢中參照這些變數。
* 您可以在查詢中參照系統變數，並為部分變數指派值，但與使用者定義變數不同，您不需要宣告系統變數。系統變數是 BigQuery 內建的變數。

### 宣告使用者建立的變數

您必須在多重陳述式查詢的開頭，或 [`BEGIN`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/procedural-language?hl=zh-tw#begin) 區塊的開頭，宣告使用者建立的變數。在多重陳述式查詢開頭宣告的變數，適用於整個查詢。在 `BEGIN` 區塊中宣告的變數，其範圍為該區塊。在對應的 `END` 陳述式之後，這些變數就會超出範圍。變數的大小上限為 1 MB，而多重陳述式查詢中使用的所有變數的總和上限為 10 MB。

您可以使用下列程序陳述式宣告變數：
[`DECLARE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/procedural-language?hl=zh-tw#declare)

```
DECLARE x INT64;

BEGIN
DECLARE y INT64;
-- Here you can reference x and y
END;

-- Here you can reference x, but not y
```

### 設定使用者建立的變數

宣告使用者建立的變數後，您可以使用 [`SET`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/procedural-language?hl=zh-tw#set) 程序陳述式為變數指派值，如下所示：

```
DECLARE x INT64 DEFAULT 0;
SET x = 10;
```

### 設定系統變數

您無法建立系統變數，但可以覆寫部分變數的預設值，做法如下：

```
SET @@dataset_project_id = 'MyProject';
```

您也可以在多個陳述式查詢中設定及隱含使用系統變數。舉例來說，在下列查詢中，每次要建立新資料表時，都必須加入專案：

```
BEGIN
  CREATE TABLE MyProject.MyDataset.MyTempTableA (id STRING);
  CREATE TABLE MyProject.MyDataset.MyTempTableB (id STRING);
END;
```

如果不想多次將專案新增至資料表路徑，可以在多重陳述式查詢中，將資料集專案 ID `MyProject` 指派給 `@@dataset_project_id` 系統變數。這項指派作業會將 `MyProject` 設為其餘查詢的預設專案。

```
SET @@dataset_project_id = 'MyProject';

BEGIN
  CREATE TABLE MyDataset.MyTempTableA (id STRING);
  CREATE TABLE MyDataset.MyTempTableB (id STRING);
END;
```

同樣地，您可以設定 `@@dataset_id` 系統變數，為查詢指派預設資料集。例如：

```
SET @@dataset_project_id = 'MyProject';
SET @@dataset_id = 'MyDataset';

BEGIN
  CREATE TABLE MyTempTableA (id STRING);
  CREATE TABLE MyTempTableB (id STRING);
END;
```

您也可以在多重陳述式查詢的許多部分，明確參照 `@@dataset_id` 等系統變數。詳情請參閱[系統變數範例](https://docs.cloud.google.com/bigquery/docs/reference/system-variables?hl=zh-tw#examples)。

### 參照使用者建立的變數

宣告及設定使用者建立的變數後，您可以在多重陳述式查詢中參照該變數。如果變數和資料欄的名稱相同，系統會優先採用資料欄。

這會傳回 `column x` + `column x`：

```
DECLARE x INT64 DEFAULT 0;
SET x = 10;

WITH Numbers AS (SELECT 50 AS x)
SELECT (x+x) AS result FROM Numbers;
```

```
+--------+
| result |
+--------+
| 100    |
+--------+
```

這會傳回 `column y` + `variable x`：

```
DECLARE x INT64 DEFAULT 0;
SET x = 10;

WITH Numbers AS (SELECT 50 AS y)
SELECT (y+x) AS result FROM Numbers;
```

```
+--------+
| result |
+--------+
| 60     |
+--------+
```

## 在多重陳述式查詢中使用暫存資料表

暫存資料表可讓您將中繼結果儲存至資料表。臨時資料表由 BigQuery 管理，因此您不必在資料集中儲存或維護這些資料表。系統會根據臨時資料表的儲存空間計費。

您可以在多重陳述式查詢中建立及參照臨時資料表。臨時資料表使用完畢後，您可以手動刪除，盡量減少儲存空間費用，也可以等待 BigQuery 在 24 小時後刪除。

### 建立臨時資料表

您可以使用 [`CREATE TABLE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#create_table_statement) 陳述式，為多重陳述式查詢建立暫時性資料表。下列範例會建立臨時資料表來儲存查詢結果，然後在子查詢中使用該臨時資料表：

```
-- Find the top 100 names from the year 2017.
CREATE TEMP TABLE top_names(name STRING)
AS
 SELECT name
 FROM `bigquery-public-data`.usa_names.usa_1910_current
 WHERE year = 2017
 ORDER BY number DESC LIMIT 100
;
-- Which names appear as words in Shakespeare's plays?
SELECT
 name AS shakespeare_name
FROM top_names
WHERE name IN (
 SELECT word
 FROM `bigquery-public-data`.samples.shakespeare
);
```

除了使用 `TEMP` 或 `TEMPORARY` 以外，語法與 `CREATE TABLE` 語法完全相同。

建立臨時資料表時，請勿在資料表名稱中使用專案或資料集限定符。系統會在特殊資料集中自動建立資料表。

### 參照臨時資料表

在目前的多重陳述式查詢期間，您可以依名稱參照臨時資料表。包括多重陳述式查詢中程序建立的臨時資料表。您無法共用臨時資料表。臨時資料表位於隱藏的 `_script%` 資料集中，名稱是隨機產生。如要瞭解如何列出隱藏的資料集，請參閱[列出資料集](https://docs.cloud.google.com/bigquery/docs/listing-datasets?hl=zh-tw#bq)一文。

### 刪除臨時資料表

您可以使用 [`DROP TABLE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#drop_table_statement) 陳述式，在多重陳述式查詢完成前明確刪除臨時資料表：

```
CREATE TEMP TABLE table1(x INT64);
SELECT * FROM table1;  -- Succeeds
DROP TABLE table1;
SELECT * FROM table1;  -- Results in an error
```

多重陳述式查詢完成後，臨時資料表最多會存在 24 小時。

### 查看暫時性資料表資料

建立臨時資料表後，您可以查看資料表的結構和其中的任何資料。如要查看資料表結構和資料，請按照下列步驟操作：

1. 在 Google Cloud 控制台開啟「BigQuery」**BigQuery**頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。

   如果沒有看到左側窗格，請按一下「展開左側窗格」圖示 last\_page 開啟窗格。
3. 在「Explorer」窗格中，按一下「Job history」。
4. 在「Personal history」(個人記錄) 或「Project history」(專案記錄) 分頁中，按一下建立暫存資料表的查詢。
5. 在「目標資料表」列中，按一下「暫時性資料表」。

   **注意：** 多重陳述式查詢中使用的暫時性資料表名稱不會保留。在 Google Cloud 控制台中，該服務會隨機命名。

### 使用 `_SESSION` 限定臨時資料表

當臨時資料表與預設資料集一起使用時，非限定的資料表名稱指的是臨時資料表 (如果有的話)，或是預設資料集中的資料表。例外情況是 `CREATE TABLE` 陳述式，在這種陳述式中，只有在 `TEMP` 或 `TEMPORARY` 關鍵字存在時，系統才會將目標資料表視為臨時資料表。

舉例來說，請看下列多重陳述式查詢：

```
-- Create table t1 in the default dataset
CREATE TABLE t1 (x INT64);

-- Create temporary table t1.
CREATE TEMP TABLE t1 (x INT64);

-- This statement selects from the temporary table.
SELECT * FROM t1;

-- Drop the temporary table
DROP TABLE t1;

-- Now that the temporary table is dropped, this statement selects from the
-- table in the default dataset.
SELECT * FROM t1;
```

您可以使用 `_SESSION` 來限定資料表名稱，藉此明確指出您所指的臨時資料表：

```
-- Create a temp table
CREATE TEMP TABLE t1 (x INT64);

-- Create a temp table using the `_SESSION` qualifier
CREATE TEMP TABLE _SESSION.t2 (x INT64);

-- Select from a temporary table using the `_SESSION` qualifier
SELECT * FROM _SESSION.t1;
```

如果使用 `_SESSION` 限定詞的查詢其臨時資料表不存在，多重陳述式查詢會擲回錯誤訊息，指出該資料表不存在。舉例來說，如果沒有名為 `t3` 的臨時資料表，即使預設資料集中有名為 `t3` 的資料表存在，多重陳述式查詢也會擲回錯誤。

您不能使用 `_SESSION` 來建立非臨時的資料表：

```
CREATE TABLE _SESSION.t4 (x INT64);  -- Fails
```

## 收集多重陳述式查詢工作的相關資訊

多重陳述式查詢作業包含已執行的多重陳述式查詢相關資訊。您可以使用工作資料執行一些常見工作，包括傳回使用多重陳述式查詢執行的最後一個陳述式，或是傳回使用多重陳述式查詢執行的所有陳述式。

### 傳回上次執行的陳述式

[`jobs.getQueryResults`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs/getQueryResults?hl=zh-tw) 方法會傳回多重陳述式查詢中，最後一個執行的陳述式查詢結果。如果沒有執行任何陳述式，系統就不會傳回任何結果。

### 傳回所有執行的陳述式

如要取得多重陳述式查詢中所有陳述式的結果，請[列舉子工作](#enumerate_child_jobs_of_a_multi-statement_query)，並對每個子工作呼叫 [`jobs.getQueryResults`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs/getQueryResults?hl=zh-tw)。

### 列舉子項工作

多重陳述式查詢會使用 [`jobs.insert`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs/insert?hl=zh-tw) 在 BigQuery 中執行，與任何其他查詢類似，只是多重陳述式查詢會指定為查詢文字。執行多重陳述式查詢時，系統會為多重陳述式查詢中的每個陳述式建立額外的工作，也就是子項工作。您可以呼叫 [`jobs.list`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs/list?hl=zh-tw)，並將多重陳述式查詢工作 ID 做為 `parentJobId` 參數傳入，列舉多重陳述式查詢的子項工作。

## 偵錯多陳述式查詢

以下是偵錯多重陳述式查詢的訣竅：

* 使用 [`ASSERT`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/debugging-statements?hl=zh-tw#assert) 陳述式，確認布林值條件為 true。
* 使用 [`BEGIN...EXCEPTION...END`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/procedural-language?hl=zh-tw#beginexceptionend) 擷取錯誤，並顯示錯誤訊息和堆疊追蹤。
* 使用 `SELECT FORMAT("....")` 顯示中間結果。
* 在 Google Cloud 控制台中執行多重陳述式查詢時，您可以查看多重陳述式查詢中每個陳述式的輸出內容。執行多重陳述式查詢時，bq 指令列工具的 `bq query` 指令也會顯示每個步驟的結果。
* 在 Google Cloud 控制台中，您可以在查詢編輯器內選取個別陳述式並執行。

## 權限

系統會在執行時檢查存取資料表、模型或其他資源的權限。如果陳述式未執行或運算式未評估，BigQuery 就不會檢查執行多重陳述式查詢的使用者是否具有存取權，可存取該查詢參照的任何資源。

在多陳述式查詢中，系統會分別驗證每個運算式或陳述式的權限。例如：

```
SELECT * FROM dataset_with_access.table1;
SELECT * FROM dataset_without_access.table2;
```

如果執行查詢的使用者有 `table1` 的存取權，但沒有 `table2` 的存取權，則第一個查詢會成功，第二個查詢會失敗。多重陳述式查詢工作本身也會失敗。

## 安全限制

在多重陳述式查詢中，您可以使用[動態 SQL](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/procedural-language?hl=zh-tw#execute_immediate) 在執行階段建構 SQL 陳述式。這項功能很方便，但可能遭到濫用。舉例來說，執行下列查詢可能會造成 [SQL 注入](https://en.wikipedia.org/wiki/SQL_injection)安全威脅，因為系統可能無法正確篩選資料表參數，導致使用者存取非預期的資料表並執行查詢。

```
-- Risky query vulnerable to SQL injection attack.
EXECUTE IMMEDIATE CONCAT('SELECT * FROM SensitiveTable WHERE id = ', @id);
```

為避免資料表中的機密資料外洩，或執行 `DROP TABLE` 等指令來刪除資料表中的資料，BigQuery 的動態程序陳述式支援多種安全措施，可減少 SQL 注入攻擊的風險，包括：

* `EXECUTE IMMEDIATE` 陳述式不允許其查詢 (以查詢參數和變數擴充) 嵌入多個 SQL 陳述式。
* 下列指令無法動態執行：`BEGIN`/`END`、`CALL`、`CASE`、`IF`、`LOOP`、`WHILE` 和 `EXECUTE IMMEDIATE`。

## 設定欄位限制

下列[工作設定查詢欄位](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#JobConfigurationQuery)無法為多重陳述式查詢設定：

* `clustering`
* `create_disposition`
* `destination_table`
* `destination_encryption_configuration`
* `range_partitioning`
* `schema_update_options`
* `time_partitioning`
* `user_defined_function_resources`
* `write_disposition`

## 定價

多重陳述式查詢的價格包括查詢費用 (使用[以量計價模式](https://cloud.google.com/bigquery/pricing?hl=zh-tw#on_demand_pricing)時) 和[暫時資料表](#temporary_tables)的儲存空間費用。使用[預留項目](https://docs.cloud.google.com/bigquery/docs/reservations-intro?hl=zh-tw)時，查詢用量會計入預留項目費用。

### 以量計價查詢大小計算

如果您採用以量計價方案，BigQuery 會根據執行多重陳述式查詢期間處理的位元組數，收取多重陳述式查詢的費用。

如要估算多重陳述式查詢可能處理的位元組數，可以執行[模擬測試](#dryrun_multi_statement_queries)。

**注意：** 系統通常無法確認多重陳述式查詢在執行之前所掃描的位元組數。為避免產生非預期的查詢費用，建議使用[以容量為準的定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#capacity_compute_analysis_pricing)。此外，您也可以使用 BigQuery [沙箱](https://docs.cloud.google.com/bigquery/docs/sandbox?hl=zh-tw)免費執行有限的查詢。

下列價格適用於這些多重陳述式查詢：

* `DECLARE`：`DEFAULT` 運算式中參照的任何資料表所掃描的總位元組數。沒有資料表參照的 `DECLARE` 陳述式不會產生費用。
* `SET`：運算式中參照的任何資料表所掃描的總位元組數。沒有資料表參照的 `SET` 陳述式不會產生費用。
* `IF`：條件運算式中參照的任何資料表所掃描的總位元組數。沒有資料表參照的 `IF` 條件運算式不會產生費用。`IF` 區塊內任何未執行的陳述式也不會產生費用。
* `WHILE`：條件運算式中參照的任何資料表所掃描的總位元組數。條件運算式中沒有資料表參照的 `WHILE` 陳述式不會產生費用。`WHILE` 區塊內任何未執行的陳述式也不會產生費用。
* `CONTINUE` 或 `ITERATE`：沒有相關費用。
* `BREAK` 或 `LEAVE`：沒有相關費用。
* `BEGIN` 或 `END`：沒有相關費用。

如果多重陳述式查詢失敗，陳述式啟動後直到失敗的期間仍會計費。失敗的陳述式則不會產生任何費用。

舉例來說，在下列範例程式碼中，每個陳述式前都有註解，說明各個陳述式會產生的費用 (如有)：

```
-- No cost, since no tables are referenced.
DECLARE x DATE DEFAULT CURRENT_DATE();
-- Incurs the cost of scanning string_col from dataset.table.
DECLARE y STRING DEFAULT (SELECT MAX(string_col) FROM dataset.table);
-- Incurs the cost of copying the data from dataset.big_table.  Once the
-- table is created, you are not charged for storage while the rest of the
-- multi-statement query runs.
CREATE TEMP TABLE t AS SELECT * FROM dataset.big_table;
-- Incurs the cost of scanning column1 from temporary table t.
SELECT column1 FROM t;
-- No cost, since y = 'foo' doesn't reference a table.
IF y = 'foo' THEN
  -- Incurs the cost of scanning all columns from dataset.other_table, if
  -- y was equal to 'foo', or otherwise no cost since it is not executed.
  SELECT * FROM dataset.other_table;
ELSE
  -- Incurs the cost of scanning all columns from dataset.different_table, if
  -- y was not equal to 'foo', or otherwise no cost since it is not executed.
  UPDATE dataset.different_table
  SET col = 10
  WHERE true;
END IF;
-- Incurs the cost of scanning date_col from dataset.table for each
-- iteration of the loop.
WHILE x < (SELECT MIN(date_col) FROM dataset.table) DO
  -- No cost, since the expression does not reference any tables.
  SET x = DATE_ADD(x, INTERVAL 1 DAY);
  -- No cost, since the expression does not reference any tables.
  IF true THEN
    -- LEAVE has no associated cost.
    LEAVE;
  END IF;
  -- Never executed, since the IF branch is always taken, so does not incur
  -- a cost.
  SELECT * FROM dataset.big_table;
END WHILE;
```

詳情請參閱[查詢大小計算方式](https://docs.cloud.google.com/bigquery/docs/estimate-costs?hl=zh-tw#query_size_calculation)。

### 儲存空間定價

系統會針對多重陳述式查詢建立的[臨時資料表](#temporary_tables)收費。您可以使用 [`TABLE_STORAGE`](https://docs.cloud.google.com/bigquery/docs/information-schema-table-storage?hl=zh-tw) 或 [`TABLE_STORAGE_USAGE_TIMELINE`](https://docs.cloud.google.com/bigquery/docs/information-schema-table-storage-usage?hl=zh-tw) 檢視畫面，查看這些臨時資料表使用的儲存空間。臨時資料表位於隱藏的 `_script%` 資料集中，名稱是隨機產生。

## 配額

如要瞭解多重陳述式查詢配額，請參閱「[配額與限制](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#multi_statement_query_limits)」。

### 查看多重陳述式查詢的數量

您可以使用 [`INFORMATION_SCHEMA.JOBS_BY_PROJECT` 檢視畫面](https://docs.cloud.google.com/bigquery/docs/information-schema-jobs?hl=zh-tw)，查看多重陳述式查詢的數量。以下範例使用 `INFORMATION_SCHEMA.JOBS_BY_PROJECT` 檢視表，顯示前一天的多重陳述式查詢數量：

```
SELECT
  COUNT(*)
FROM
  `region-us`.INFORMATION_SCHEMA.JOBS_BY_PROJECT
WHERE
  creation_time BETWEEN TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 1 DAY) AND CURRENT_TIMESTAMP()
AND job_type = "QUERY"
AND state = 'RUNNING'
AND statement_type = 'SCRIPT'
```

如要進一步瞭解如何查詢多重陳述式查詢，請參閱[多重陳述式查詢工作](https://docs.cloud.google.com/bigquery/docs/information-schema-jobs?hl=zh-tw#multi-statement_query_jobs)。`INFORMATION_SCHEMA.JOBS`




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-02 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-02 (世界標準時間)。"],[],[]]