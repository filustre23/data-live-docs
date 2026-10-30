Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 使用多陳述式查詢

在 BigQuery 中，多陳述式查詢可讓您依序執行一組 SQL 陳述式，並共用狀態。您可以將標準 SQL 與[程序語言陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/procedural-language?hl=zh-tw)結合，在單一要求中定義變數、實作控制流程，以及執行複雜的資料定義語言 (DDL) 和 data manipulation language (DML) 作業。多重陳述式查詢通常用於[預存程序](https://docs.cloud.google.com/bigquery/docs/procedures?hl=zh-tw)。

## 編寫、執行及儲存多陳述式查詢

多陳述式查詢包含一或多個 SQL 陳述式，並以分號分隔。任何有效的 SQL 陳述式都可用於多陳述式查詢。多陳述式查詢也可以包含[程序語言陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/procedural-language?hl=zh-tw)，讓您使用變數或透過 SQL 陳述式實作控制流程。

### 編寫多陳述式查詢

您可以在 BigQuery 中編寫多陳述式查詢。下列多陳述式查詢會宣告變數，並在 [`IF`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/procedural-language?hl=zh-tw#if) 陳述式中使用該變數：

```
DECLARE day INT64;
SET day = (SELECT EXTRACT(DAYOFWEEK from CURRENT_DATE));
if day = 1 or day = 7 THEN
  SELECT 'Weekend';
ELSE
  SELECT 'Weekday';
END IF
```

BigQuery 會將任何包含多個陳述式的要求解讀為多陳述式查詢，除非陳述式完全由 `CREATE TEMP FUNCTION` 陳述式組成，後面接著單一 `SELECT` 陳述式。舉例來說，下列查詢不屬於多重陳述式查詢：

```
CREATE TEMP FUNCTION Add(x INT64, y INT64) AS (x + y);
SELECT Add(3, 4);
```

### 執行多陳述式查詢

您可以像執行其他查詢一樣執行多陳述式查詢，例如在 Google Cloud 控制台或使用 bq 指令列工具。

### 查看多陳述式查詢結果

在 BigQuery Studio 執行多陳述式查詢時，「Query results」(查詢結果) 窗格會以階層式執行記錄樹狀結構，顯示各陳述式的結果。多重陳述式查詢執行作業會顯示為記錄樹狀結構中的父項節點，而多重陳述式查詢中的每個個別陳述式 (子項工作) 則會顯示為子節點。您可以點選個別子節點，查看多重陳述式查詢中該部分傳回的特定資料，不必離開編輯器。

### 模擬測試多陳述式查詢

如要估算多陳述式查詢讀取的位元組數，請考慮執行[模擬測試](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#dry-run)。如果多陳述式查詢只包含 `SELECT` 陳述式，模擬測試結果最準確。

模擬測試會對下列查詢和陳述式類型進行特殊處理：

* `CALL` 陳述式：模擬測試會驗證呼叫的程序是否存在，且簽章與提供的引數相符。系統不會驗證呼叫程序和 `CALL` 陳述式後方所有陳述式的內容。
* [DDL 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw)：模擬測試會驗證第一個 DDL 陳述式，然後停止。系統會略過所有後續陳述式。不支援 `CREATE TEMP TABLE` 陳述式的模擬測試。
* [DML 陳述式](https://docs.cloud.google.com/bigquery/docs/data-manipulation-language?hl=zh-tw)：模擬測試會驗證 DML 陳述式，然後繼續驗證後續陳述式。在這種情況下，系統會根據原始資料表大小估算位元組，不會考量 DML 陳述式的結果。
* `EXECUTE IMMEDIATE` 陳述式：模擬測試會驗證查詢運算式，但不會評估動態查詢本身。系統會略過 `EXECUTE IMMEDIATE` 陳述式後的所有陳述式。
* 在分區篩選器中使用變數的查詢：模擬測試會驗證初始查詢和後續陳述式。不過，模擬測試無法計算分區篩選器中變數的執行階段值。這會影響讀取的位元組預估值。
* 在 `FOR SYSTEM TIME AS OF` 子句的時間戳記運算式中使用變數的查詢：模擬測試會使用資料表的目前內容，並忽略 `FOR SYSTEM TIME AS OF` 子句。如果目前資料表與先前疊代資料表的大小不同，就會影響讀取的位元組預估值。
* `FOR`、`IF` 和 `WHILE` 控制陳述式：模擬測試會立即停止。條件運算式、控制陳述式的主體和所有後續陳述式都不會經過驗證。

系統會盡力執行模擬測試，基礎程序可能會有變動。模擬測試須遵守下列規定：

* 即使查詢成功完成模擬測試，也可能無法順利執行。例如，查詢可能會在執行階段失敗，原因可能是模擬測試未偵測到。
* 成功執行的查詢不一定能順利完成模擬測試。例如，查詢可能因執行時發現的原因而無法模擬測試。
* 今天成功執行的模擬測試不保證日後一律能執行。例如，模擬測試實作方式的變更可能會偵測到先前未偵測到的查詢錯誤。

### 儲存多重陳述式查詢

如要儲存多重陳述式查詢，請參閱「[使用已儲存的查詢](https://docs.cloud.google.com/bigquery/docs/work-with-saved-queries?hl=zh-tw)」。

## 在多陳述式查詢中使用變數

多陳述式查詢可以包含[使用者建立的變數](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/procedural-language?hl=zh-tw#declare)和[系統變數](https://docs.cloud.google.com/bigquery/docs/reference/system-variables?hl=zh-tw)。

* 您可以宣告使用者建立的變數、為變數指派值，並在整個查詢中參照這些變數。
* 您可以在查詢中參照系統變數，並為部分變數指派值，但與使用者定義變數不同，您不必宣告系統變數。系統變數內建於 BigQuery。

### 宣告使用者建立的變數

您必須在多重陳述式查詢或 [`BEGIN`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/procedural-language?hl=zh-tw#begin) 區塊的開頭，宣告使用者建立的變數。在多重陳述式查詢開頭宣告的變數，其範圍涵蓋整個查詢。在 `BEGIN` 區塊內宣告的變數，其範圍僅限於該區塊。在對應的 `END` 陳述式之後，這些變數就會超出範圍。變數的大小上限為 1 MB，多陳述式查詢中使用的所有變數大小上限為 10 MB。

您可以使用 [`DECLARE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/procedural-language?hl=zh-tw#declare) 程序陳述式宣告變數，如下所示：

```
DECLARE x INT64;

BEGIN
DECLARE y INT64;
-- Here you can reference x and y
END;

-- Here you can reference x, but not y
```

### 設定使用者建立的變數

宣告使用者建立的變數後，您可以使用 [`SET`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/procedural-language?hl=zh-tw#set) 程序陳述式為其指派值，如下所示：

```
DECLARE x INT64 DEFAULT 0;
SET x = 10;
```

### 設定系統變數

您無法建立系統變數，但可以覆寫部分變數的預設值，如下所示：

```
SET @@dataset_project_id = 'MyProject';
```

您也可以在多陳述式查詢中設定及隱含使用系統變數。舉例來說，在下列查詢中，每次要建立新資料表時，都必須加入專案：

```
BEGIN
  CREATE TABLE MyProject.MyDataset.MyTempTableA (id STRING);
  CREATE TABLE MyProject.MyDataset.MyTempTableB (id STRING);
END;
```

如果不想多次將專案新增至資料表路徑，可以在多重陳述式查詢中，將資料集專案 ID `MyProject` 指派給 `@@dataset_project_id` 系統變數。這項指派作業會將 `MyProject` 設為查詢其餘部分的預設專案。

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

您也可以在多陳述式查詢的多個部分中，明確參照 `@@dataset_id` 等系統變數。詳情請參閱[系統變數範例](https://docs.cloud.google.com/bigquery/docs/reference/system-variables?hl=zh-tw#examples)。

### 參照使用者建立的變數

宣告並設定使用者建立的變數後，您可以在多陳述式查詢中參照該變數。如果變數和資料欄名稱相同，則以資料欄為準。

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

## 在多陳述式查詢中使用暫存資料表

臨時資料表可讓您將中繼結果儲存至資料表。臨時資料表由 BigQuery 管理，因此您不需要在資料集中儲存或維護這些資料表。系統會根據臨時資料表的儲存空間計費。

您可以在多重陳述式查詢中建立及參照臨時資料表。臨時資料表使用完畢後，您可以手動刪除，盡可能降低儲存費用，或等待 BigQuery 在 24 小時後刪除。

### 建立暫時資料表

您可以使用 [`CREATE TABLE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#create_table_statement) 陳述式，為多陳述式查詢建立臨時資料表。以下範例會建立臨時資料表來儲存查詢結果，然後在子查詢中使用該臨時資料表：

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

建立臨時資料表時，請勿在資料表名稱中使用專案或資料集限定詞。系統會在特殊資料集中自動建立資料表。

### 參照臨時資料表

在目前的多重陳述式查詢期間，您可以依名稱參照臨時資料表。包括多重陳述式查詢中，由程序建立的臨時資料表。您無法共用臨時資料表。臨時資料表位於隱藏的 `_script%` 資料集中，名稱為隨機產生。[列出資料集](https://docs.cloud.google.com/bigquery/docs/listing-datasets?hl=zh-tw#bq)一文說明如何列出隱藏的資料集。

### 刪除臨時資料表

您可以使用 [`DROP TABLE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#drop_table_statement) 陳述式，在多陳述式查詢完成前明確刪除臨時資料表：

```
CREATE TEMP TABLE table1(x INT64);
SELECT * FROM table1;  -- Succeeds
DROP TABLE table1;
SELECT * FROM table1;  -- Results in an error
```

多重陳述式查詢完成後，臨時資料表最多會存在 24 小時。

### 查看臨時資料表資料

建立臨時資料表後，您可以查看資料表的結構和其中的任何資料。如要查看資料表結構和資料，請按照下列步驟操作：

1. 在 Google Cloud 控制台開啟「BigQuery」**BigQuery**頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。

   如果沒有看到左側窗格，請按一下 last\_page「Expand left pane」(展開左側窗格)，開啟窗格。
3. 在「Explorer」窗格中，點選「工作記錄」。
4. 在「Personal history」(個人記錄) 或「Project history」(專案記錄) 分頁中，按一下建立暫存資料表的查詢。
5. 在「Destination table」(目的地資料表) 列中，按一下「Temporary table」(臨時資料表)。

   **注意：** 多陳述式查詢中使用的臨時資料表名稱不會保留。在 Google Cloud 控制台中，這個服務帳戶會隨機命名。

### 使用 `_SESSION` 限定臨時資料表

如果臨時資料表與預設資料集搭配使用，不完整的資料表名稱會參照臨時資料表 (如有)，或預設資料集中的資料表。`CREATE TABLE` 陳述式是例外狀況，只有在出現 `TEMP` 或 `TEMPORARY` 關鍵字時，目標資料表才會視為暫存資料表。

以下列多陳述式查詢為例：

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

如果您使用 `_SESSION` 限定詞查詢不存在的臨時資料表，多重陳述式查詢會擲回錯誤，指出資料表不存在。舉例來說，如果沒有名為 `t3` 的臨時資料表，即使預設資料集中有名為 `t3` 的資料表，多重陳述式查詢也會擲回錯誤。

您不能使用 `_SESSION` 來建立非臨時的資料表：

```
CREATE TABLE _SESSION.t4 (x INT64);  -- Fails
```

## 收集多陳述式查詢工作的相關資訊

多陳述式查詢工作包含已執行的多陳述式查詢相關資訊。您可以使用工作資料執行一些常見工作，包括傳回使用多陳述式查詢執行的最後一個陳述式，或傳回使用多陳述式查詢執行的所有陳述式。

### 傳回上次執行的陳述式

[`jobs.getQueryResults`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs/getQueryResults?hl=zh-tw) 方法會傳回多陳述式查詢中最後一個陳述式的查詢結果。如果未執行任何陳述式，系統就不會傳回任何結果。

### 傳回所有已執行的陳述式

如要取得多陳述式查詢中所有陳述式的結果，請[列舉子工作](#enumerate_child_jobs_of_a_multi-statement_query)，並對每個子工作呼叫 [`jobs.getQueryResults`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs/getQueryResults?hl=zh-tw)。

### 列舉子項工作

多陳述式查詢會使用 [`jobs.insert`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs/insert?hl=zh-tw) 在 BigQuery 中執行，與其他查詢類似，多陳述式查詢會指定為查詢文字。執行多陳述式查詢時，系統會為多陳述式查詢中的每個陳述式建立額外工作，稱為子工作。您可以呼叫 [`jobs.list`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs/list?hl=zh-tw)，並傳入多陳述式查詢工作 ID 做為 `parentJobId` 參數，列舉多陳述式查詢的子項工作。

子項工作也會產生自己的稽核記錄項目。`TableDataRead` 和 `TableDataChange` 等資料存取事件會記錄在執行陳述式的子項工作，而非父項工作。詳情請參閱「[BigQuery 稽核記錄總覽](https://docs.cloud.google.com/bigquery/docs/reference/auditlogs?hl=zh-tw#data_access)」。

## 對多陳述式查詢進行偵錯

以下是偵錯多陳述式查詢的一些提示：

* 使用 [`ASSERT`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/debugging-statements?hl=zh-tw#assert) 陳述式，斷言布林值條件為 true。
* 使用 [`BEGIN...EXCEPTION...END`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/procedural-language?hl=zh-tw#beginexceptionend) 擷取錯誤，並顯示錯誤訊息和堆疊追蹤。
* 使用 `SELECT FORMAT("....")` 顯示中間結果。
* 在 Google Cloud 控制台執行多陳述式查詢時，您可以查看多陳述式查詢中各個陳述式的輸出內容。執行多陳述式查詢時，bq 指令列工具的 `bq query` 指令也會顯示每個步驟的結果。
* 在 Google Cloud 控制台，您可以在查詢編輯器中選取個別陳述式並執行。

## 權限

系統會在執行時檢查資料表、模型或其他資源的存取權限。如果未執行陳述式，或未評估運算式，BigQuery 就不會檢查執行多陳述式查詢的使用者，是否能存取查詢參照的任何資源。

在多陳述式查詢中，系統會分別驗證每個運算式或陳述式的權限。例如：

```
SELECT * FROM dataset_with_access.table1;
SELECT * FROM dataset_without_access.table2;
```

如果執行查詢的使用者有權存取 `table1`，但無權存取 `table2`，則第一個查詢會成功，第二個查詢會失敗。多陳述式查詢工作本身也會失敗。

## 安全性限制

在多陳述式查詢中，您可以使用[動態 SQL](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/procedural-language?hl=zh-tw#execute_immediate) 在執行階段建構 SQL 陳述式。這雖然方便，但也可能帶來新的濫用機會。舉例來說，執行下列查詢可能會造成 [SQL 注入](https://en.wikipedia.org/wiki/SQL_injection)安全威脅，因為資料表參數可能未正確篩選，導致非預期的資料表遭到存取及執行。

```
-- Risky query vulnerable to SQL injection attack.
EXECUTE IMMEDIATE CONCAT('SELECT * FROM SensitiveTable WHERE id = ', @id);
```

為避免資料表中的機密資料外洩，或執行 `DROP TABLE` 等指令刪除資料表中的資料，BigQuery 的動態程序陳述式支援多項安全措施，可減少 SQL 注入式攻擊的風險，包括：

* `EXECUTE IMMEDIATE` 陳述式不允許其查詢 (以查詢參數和變數展開) 嵌入多個 SQL 陳述式。
* 下列指令無法動態執行：`BEGIN`/`END`、`CALL`、`CASE`、`IF`、`LOOP`、`WHILE` 和 `EXECUTE IMMEDIATE`。

## 設定欄位限制

多重陳述式查詢無法設定下列[工作設定查詢欄位](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#JobConfigurationQuery)：

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

多重陳述式查詢的定價包含查詢費用 (使用[隨選計費模式](https://cloud.google.com/bigquery/pricing?hl=zh-tw#on_demand_pricing)時) 和[臨時資料表](#temporary_tables)的儲存空間費用。如果您使用[預留項目](https://docs.cloud.google.com/bigquery/docs/reservations-intro?hl=zh-tw)，查詢用量會計入預留項目費用。

### 隨選查詢大小計算

如果您採用隨選計費模式，BigQuery 會根據執行多重陳述式查詢期間處理的位元組數，收取多重陳述式查詢費用。

如要估算多重陳述式查詢可能處理的位元組數，可以執行[模擬測試](#dryrun_multi_statement_queries)。

**注意：** 多重陳述式查詢掃描的位元組數，通常在執行前無法得知。為避免產生非預期的查詢費用，建議您使用[以運算資源為基礎的計價模式](https://cloud.google.com/bigquery/pricing?hl=zh-tw#capacity_compute_analysis_pricing)。或者，您也可以使用 BigQuery [沙箱](https://docs.cloud.google.com/bigquery/docs/sandbox?hl=zh-tw)，享有有限的免費查詢執行服務。

這類多重陳述式查詢的定價如下：

* `DECLARE`：`DEFAULT` 運算式中參照的任何資料表所掃描的總位元組數。不含資料表參照的 `DECLARE` 陳述式不會產生費用。
* `SET`：運算式中參照的任何資料表所掃描的總位元組數。不含資料表參照的 `SET` 陳述式不會產生費用。
* `IF`：條件運算式中參照的任何資料表所掃描的總位元組數。不含資料表參照的 `IF` 條件運算式不會產生費用。`IF` 區塊中未執行的陳述式不會產生費用。
* `WHILE`：條件運算式中參照的任何資料表所掃描的總位元組數。如果 `WHILE` 陳述式的條件運算式中沒有資料表參照，就不會產生費用。`WHILE` 區塊中未執行的陳述式不會產生費用。
* `CONTINUE` 或 `ITERATE`：沒有相關費用。
* `BREAK` 或 `LEAVE`：沒有相關費用。
* `BEGIN` 或 `END`：沒有相關費用。

如果多重陳述式查詢失敗，系統仍會收取失敗前所有陳述式的費用。失敗的陳述式則不會產生任何費用。

舉例來說，下列程式碼範例在每個陳述式前都加上註解，說明每個陳述式產生的費用 (如有)：

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

詳情請參閱「[查詢大小計算](https://docs.cloud.google.com/bigquery/docs/estimate-costs?hl=zh-tw#query_size_calculation)」。

### 儲存空間定價

系統會針對多陳述式查詢建立的[臨時資料表](#temporary_tables)收費。您可以使用 [`TABLE_STORAGE`](https://docs.cloud.google.com/bigquery/docs/information-schema-table-storage?hl=zh-tw) 或 [`TABLE_STORAGE_USAGE_TIMELINE`](https://docs.cloud.google.com/bigquery/docs/information-schema-table-storage-usage?hl=zh-tw) 檢視表，查看這些臨時資料表使用的儲存空間。臨時資料表位於隱藏的 `_script%` 資料集中，名稱為隨機產生。

## 配額

如要瞭解多重陳述式查詢配額，請參閱「[配額與限制](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#multi_statement_query_limits)」。

### 查看多重陳述式查詢數量

您可以使用 [`INFORMATION_SCHEMA.JOBS_BY_PROJECT` 檢視表](https://docs.cloud.google.com/bigquery/docs/information-schema-jobs?hl=zh-tw)，查看執行中的多重陳述式查詢數量。以下範例使用 `INFORMATION_SCHEMA.JOBS_BY_PROJECT` 檢視表，顯示前一天的多重陳述式查詢數量：

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

如要進一步瞭解如何查詢 `INFORMATION_SCHEMA.JOBS` 以執行多重陳述式查詢，請參閱「[多重陳述式查詢工作](https://docs.cloud.google.com/bigquery/docs/information-schema-jobs?hl=zh-tw#multi-statement_query_jobs)」。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-10-29 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-10-29 (世界標準時間)。"],[],[]]