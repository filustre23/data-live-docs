Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 在工作階段中撰寫查詢

本文說明如何在 BigQuery 工作階段中編寫查詢。
本文適用於已大致瞭解 BigQuery [工作階段](https://docs.cloud.google.com/bigquery/docs/sessions-intro?hl=zh-tw)，且知道如何[在工作階段中執行查詢](https://docs.cloud.google.com/bigquery/docs/sessions?hl=zh-tw#run-queries)的使用者。

工作階段會儲存狀態。在工作階段中建立的狀態會保留下來，並可在整個工作階段中使用。因此，如果您在一個查詢項目中建立臨時資料表，就能在工作階段的其餘時間，於其他查詢項目中使用該臨時資料表。

工作階段支援[工作階段變數](#session_variables)、[工作階段系統變數](#session_system_variables)、[多陳述式查詢](#session_scripting)和[多陳述式交易](#multi_transactions)。

完成這些步驟之前，請確認您具備在工作階段中作業的必要[權限](https://docs.cloud.google.com/bigquery/docs/sessions-intro?hl=zh-tw#roles_and_permissions)。

## 在工作階段中使用系統變數

您可以使用下列[系統變數](https://docs.cloud.google.com/bigquery/docs/reference/system-variables?hl=zh-tw)設定或擷取工作階段層級資料：

* `@@dataset_id`：目前專案中預設資料集的 ID。您可以一併設定及使用系統變數 `@@dataset_project_id` 和 `@@dataset_id`。
* `@@dataset_project_id`：查詢中使用的資料集所屬預設專案的 ID。如果未設定這個系統變數，或將其設為 `NULL`，系統會使用查詢執行專案。系統變數 `@@dataset_project_id` 和 `@@dataset_id` 可以一併設定及使用。
* `@@query_label`：要指派給工作階段的[工作標籤](https://docs.cloud.google.com/bigquery/docs/adding-labels?hl=zh-tw#job-label)。標籤可供整個工作階段使用，而不僅限於工作階段中的特定查詢。
* `@@session_id`：目前工作階段的 ID。
* `@@time_zone`：受時區影響的 SQL 函式中，如未指定時區做為引數，就會使用這個預設時區。

這些系統變數可在工作階段期間隨時使用，且適用於剩餘的工作階段。您不會定義這些變數，但可以使用 [`SET`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/procedural-language?hl=zh-tw#set) 陳述式指派新值。

工作階段中[變數](https://docs.cloud.google.com/bigquery/docs/multi-statement-queries?hl=zh-tw#variables)的大小上限為 1 MB，而工作階段中所有變數的總和上限為 10 MB。

## 為工作階段指派標籤

您可以[將工作標籤指派給工作階段](https://docs.cloud.google.com/bigquery/docs/adding-labels?hl=zh-tw#adding-label-to-session)。
這樣一來，工作階段中所有後續查詢都會指派給該標籤。
標籤可在工作階段期間的任何時間使用，並適用於剩餘的工作階段。您指派的工作標籤會顯示在[稽核記錄](https://docs.cloud.google.com/bigquery/docs/reference/auditlogs?hl=zh-tw)中。

## 在工作階段中使用變數

您可以使用[變數](https://docs.cloud.google.com/bigquery/docs/multi-statement-queries?hl=zh-tw#variables)建立、設定及擷取工作階段層級資料。您可以在工作階段期間隨時使用變數，且變數適用於工作階段的其餘時間。

* 如要建立工作階段範圍變數，請在 [`BEGIN...END`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/procedural-language?hl=zh-tw#begin) 區塊外使用 [`DECLARE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/procedural-language?hl=zh-tw#declare) 陳述式。
* 如要在建立工作階段範圍變數後進行設定，請使用 [`SET`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/procedural-language?hl=zh-tw#set) 陳述式。
* 在 `BEGIN...END` 區塊內宣告的變數並非工作階段範圍變數。
* 工作階段範圍變數可在 `BEGIN...END` 區塊內參照。
* 您可以在 `BEGIN...END` 區塊內設定工作階段範圍變數。

工作階段中變數的大小上限為 1 MB，而工作階段中所有變數的總和上限為 10 MB。

## 在工作階段中使用臨時資料表

暫時性資料表可讓您將中繼結果儲存至資料表。臨時資料表會在工作階段層級顯示，因此您不需要在資料集中儲存或維護臨時資料表。工作階段終止後，系統會自動刪除該檔案。工作階段處於有效狀態時，系統會針對臨時資料表的儲存空間向您收費。詳情請參閱「[在多重陳述式查詢中使用暫時性資料表](https://docs.cloud.google.com/bigquery/docs/multi-statement-queries?hl=zh-tw#temporary_tables)」。

## 在工作階段中使用暫時性函式

[暫時函式](https://docs.cloud.google.com/bigquery/docs/user-defined-functions?hl=zh-tw)或[暫時匯總函式](https://docs.cloud.google.com/bigquery/docs/user-defined-aggregates?hl=zh-tw#create-temp-sql-udaf)會顯示在工作階段層級，因此不需要儲存或維護資料集。工作階段終止後，系統會自動刪除。

## 在工作階段中使用多陳述式查詢

您可以在工作階段中使用 [GoogleSQL 多重陳述式查詢](https://docs.cloud.google.com/bigquery/docs/multi-statement-queries?hl=zh-tw#write_a_multi_statement_query)。每個指令碼都可以包含臨時資料表和系統變數。指令碼可存取工作階段變數和臨時資料表。指令碼中宣告的所有頂層變數也都是工作階段變數。

## 在工作階段中執行多查詢多陳述式交易

您可以在工作階段中，透過多個查詢執行多陳述式交易。
例如：

下列查詢會啟動交易。

```
BEGIN TRANSACTION
```

在交易中，下列查詢會建立名為 `Flights` 的臨時資料表，然後傳回這個資料表中的資料。查詢中包含兩項陳述式。

```
CREATE TEMP TABLE Flights(total INT64)  AS SELECT * FROM UNNEST([10,23,3,14,55]) AS a;

SELECT * FROM Flights;
```

下列查詢會提交交易。

```
COMMIT
```

您可以找出影響 `Flights` 資料表的有效交易：

```
WITH running_transactions AS (
  SELECT DISTINCT transaction_id
  FROM
    `region-us`.INFORMATION_SCHEMA.JOBS_BY_PROJECT
    WHERE creation_time > TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 7 DAY)
    EXCEPT DISTINCT
    SELECT transaction_id FROM `region-us`.INFORMATION_SCHEMA.JOBS_BY_PROJECT
    WHERE
      creation_time > TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 7 DAY)
      AND statement_type = "COMMIT_TRANSACTION"
      OR statement_type = "ROLLBACK_TRANSACTION"
)
SELECT
  jobs.transaction_id AS transaction_id,
  project_id,
  user_email,
  session_info.session_id,
  query
FROM `region-us`.INFORMATION_SCHEMA.JOBS_BY_PROJECT AS jobs, running_transactions
  WHERE
  creation_time > TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 7 DAY)
  AND destination_table = ("Flights")
  AND jobs.transaction_id = running_transactions.transaction_id;
```

如要取消進行中的交易，且您具備 `bigquery.admin` 角色，可以[發出復原陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/procedural-language?hl=zh-tw#rollback_transaction)，方法是在 Cloud Shell 中使用與交易相關聯的會期 ID，或是透過 API 呼叫。[執行查詢](https://docs.cloud.google.com/bigquery/docs/sessions?hl=zh-tw#run-queries)時，如果使用與交易相關聯的工作階段 ID，結果中就會顯示工作階段 ID。

## 範例階段

以下是 Google Cloud 控制台中的工作階段工作流程範例：

1. 在 Google Cloud 控制台中，開啟新的編輯器分頁，然後[建立工作階段](https://docs.cloud.google.com/bigquery/docs/sessions?hl=zh-tw#create-session)。
2. 在編輯器分頁中，新增下列查詢：

   ```
   CREATE TEMP TABLE Flights(total INT64)  AS SELECT * FROM UNNEST([10,23,3,14,55]) AS a;
   SELECT * FROM Flights;
   ```
3. 執行查詢。系統會建立名為 `Flights` 的臨時資料表，並傳回所有資料。

   ```
   +-------+
   | total |
   +-------+
   |    55 |
   |    23 |
   |     3 |
   |    14 |
   |    10 |
   +-------+
   ```
4. 刪除編輯器分頁中的內容，然後新增下列查詢：

   ```
   SELECT * FROM Flights LIMIT 2;
   ```
5. 執行查詢。系統會傳回兩筆記錄的結果。即使您刪除了先前的查詢，查詢資訊仍會儲存在目前的工作階段中。

   ```
   +-------+
   | total |
   +-------+
   |    55 |
   |    23 |
   +-------+
   ```
6. 刪除編輯器分頁中的內容，然後新增下列查詢：

   ```
   DECLARE x INT64 DEFAULT 10;

   SELECT total * x AS total_a FROM Flights LIMIT 2;

   BEGIN
     SET x = 100;
     SELECT total * x AS total_b FROM Flights LIMIT 2;
   END;

   SELECT total * x AS total_c FROM Flights LIMIT 2;
   ```
7. 執行查詢。工作階段範圍變數 `x` 用於限制 `Flights` 資料表傳回的結果數。請仔細觀察，當這個變數在 `BEGIN...END` 陳述式外宣告、在 `BEGIN...END` 陳述式內設定，然後再次在 `BEGIN...END` 陳述式外參照時，範圍會如何影響這個變數。

   ```
   +---------+
   | total_a |
   +---------+
   |     550 |
   |     230 |
   +---------+

   +---------+
   | total_b |
   +---------+
   |    5500 |
   |    2300 |
   +---------+

   +---------+
   | total_c |
   +---------+
   |    5500 |
   |    2300 |
   +---------+
   ```
8. 刪除編輯器分頁中的內容，然後新增下列查詢：

   ```
   SELECT STRING(TIMESTAMP "2008-12-20 15:30:00+00", @@time_zone) AS default_time_zone;

   SET @@time_zone = "America/Los_Angeles";

   SELECT STRING(TIMESTAMP "2008-12-20 15:30:00+00", @@time_zone) AS new_time_zone;
   ```
9. 執行查詢。工作階段範圍的系統變數 `@@time_zone` 用於將時區指派給時間戳記。第一個陳述式會傳回預設時區 (在本例中為 `UTC`) 的時間戳記。下一個陳述式會將 `@@time_zone` 指派給新值。第三個陳述式會傳回具有新時區的時間戳記。

   ```
   +-------------------------------+
   | default_time_zone             |
   +-------------------------------+
   | 2008-12-20 15:30:00+00        |
   +-------------------------------+

   +-------------------------------+
   | new_time_zone                 |
   +-------------------------------+
   | 2008-12-20 07:30:00-08        |
   +-------------------------------+
   ```

## 後續步驟

* 進一步瞭解如何[處理工作階段](https://docs.cloud.google.com/bigquery/docs/sessions?hl=zh-tw)，包括如何建立、使用、終止及列出工作階段。
* 進一步瞭解 GoogleSQL 中的[多重陳述式查詢](https://docs.cloud.google.com/bigquery/docs/multi-statement-queries?hl=zh-tw)。
* 進一步瞭解 GoogleSQL 中的[多重陳述式交易](https://docs.cloud.google.com/bigquery/docs/transactions?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-14 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-14 (世界標準時間)。"],[],[]]