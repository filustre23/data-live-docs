Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 多陳述式交易

BigQuery 支援在單一查詢中執行多陳述式交易，或在使用工作階段時跨多個查詢執行。多陳述式交易可讓您執行變動作業，例如在一或多個資料表中插入或刪除資料列，並以不可分割的方式提交或復原變更。

多陳述式交易的用途包括：

* 在多個資料表上執行 DML 異動，並視為單一交易。資料表可以跨越多個資料集或專案。
* 根據中繼運算，在多個階段對單一資料表執行異動。

交易可保證 [ACID](https://en.wikipedia.org/wiki/ACID) 屬性，並支援快照隔離。在交易期間，所有讀取作業都會傳回交易中參照資料表的一致快照。如果交易中的陳述式修改了資料表，則同一交易中的後續陳述式會顯示這些變更。

**注意：** 如果基礎資料來源在交易期間發生變更，則無法保證交易中從外部資料來源讀取的資料會保持一致。

## 交易範圍

交易必須包含在單一 SQL 查詢中，除非是在 [`Session mode`](https://docs.cloud.google.com/bigquery/docs/sessions-intro?hl=zh-tw) 中。查詢可以包含多個交易，但不得巢狀。您可以在工作階段中，對多個查詢執行[多陳述式交易](https://docs.cloud.google.com/bigquery/docs/sessions-write-queries?hl=zh-tw#multi_transactions)。

如要啟動交易，請使用 [`BEGIN TRANSACTION`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/procedural-language?hl=zh-tw#begin_transaction) 陳述式。發生下列任一情況時，交易就會結束：

* 查詢會執行 [`COMMIT TRANSACTION`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/procedural-language?hl=zh-tw#commit_transaction) 陳述式。這個陳述式會自動提交交易內的所有變更。
* 查詢會執行 [`ROLLBACK TRANSACTION`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/procedural-language?hl=zh-tw#rollback_transaction) 陳述式。這個陳述式會捨棄交易內的所有變更。
* 查詢會在到達這兩個陳述式之前結束。在這種情況下，BigQuery 會自動復原交易。

如果交易期間發生錯誤，且查詢有[例外狀況處理常式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/procedural-language?hl=zh-tw#beginexceptionend)，BigQuery 會將控制權轉移給例外狀況處理常式。在例外狀況區塊中，您可以選擇要修訂或復原交易。

如果工作階段模式已停用，且交易期間發生錯誤，但沒有例外狀況處理常式，則查詢會失敗，BigQuery 會自動復原交易。

啟用工作階段模式且沒有例外狀況處理常式時，交易會保持有效狀態，直到工作階段終止或明確復原為止。無論工作階段模式為何，建議您新增例外狀況處理常式，確保交易能盡快正確復原，避免不必要地保留鎖定和資源。

以下範例顯示復原交易的例外狀況處理常式：

```
BEGIN

  BEGIN TRANSACTION;
  INSERT INTO mydataset.NewArrivals
    VALUES ('top load washer', 100, 'warehouse #1');
  -- Trigger an error.
  SELECT 1/0;
  COMMIT TRANSACTION;

EXCEPTION WHEN ERROR THEN
  -- Roll back the transaction inside the exception handler.
  SELECT @@error.message;
  ROLLBACK TRANSACTION;
END;
```

## 交易支援的陳述式

交易支援下列陳述式類型：

* 查詢陳述式：`SELECT`
* DML 陳述式：`INSERT`、`UPDATE`、`DELETE`、`MERGE` 和 `TRUNCATE TABLE`
* 臨時實體的 DDL 陳述式：

  + `CREATE TEMP TABLE`
  + `CREATE TEMP FUNCTION`
  + 臨時資料表上的 `DROP TABLE`
  + `DROP FUNCTION` 臨時函式

交易中不支援建立或捨棄永久實體 (例如資料集、資料表和函式) 的 DDL 陳述式。

### 交易中的日期/時間函式

在交易中，下列日期/時間函式具有特殊行為：

* [`CURRENT_TIMESTAMP`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/timestamp_functions?hl=zh-tw#current_timestamp)、[`CURRENT_DATE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/date_functions?hl=zh-tw#current_date) 和 [`CURRENT_TIME`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/time_functions?hl=zh-tw#current_time) 函式會傳回交易開始的時間戳記。
* 您無法使用 [`FOR SYSTEM_TIME AS OF`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw#for_system_time_as_of) 子句讀取交易開始時間戳記之後的資料表。否則會傳回錯誤。

## 交易範例

這個範例假設有兩個名為 `Inventory` 和 `NewArrivals` 的資料表，建立方式如下：

```
CREATE OR REPLACE TABLE mydataset.Inventory
(
 product string,
 quantity int64,
 supply_constrained bool
);

CREATE OR REPLACE TABLE mydataset.NewArrivals
(
 product string,
 quantity int64,
 warehouse string
);

INSERT mydataset.Inventory (product, quantity)
VALUES('top load washer', 10),
     ('front load washer', 20),
     ('dryer', 30),
     ('refrigerator', 10),
     ('microwave', 20),
     ('dishwasher', 30);

INSERT mydataset.NewArrivals (product, quantity, warehouse)
VALUES('top load washer', 100, 'warehouse #1'),
     ('dryer', 200, 'warehouse #2'),
     ('oven', 300, 'warehouse #1');
```

`Inventory` 資料表包含目前庫存的資訊，`NewArrivals` 則包含新到貨商品的資訊。

下列交易會以新到貨品更新 `Inventory`，並從 `NewArrivals` 刪除對應的記錄。假設所有陳述式都順利完成，兩個資料表中的變更會以單一交易的形式自動修訂。

```
BEGIN TRANSACTION;

-- Create a temporary table that holds new arrivals from 'warehouse #1'.
CREATE TEMP TABLE tmp
  AS SELECT * FROM mydataset.NewArrivals WHERE warehouse = 'warehouse #1';

-- Delete the matching records from the NewArravals table.
DELETE mydataset.NewArrivals WHERE warehouse = 'warehouse #1';

-- Merge the records from the temporary table into the Inventory table.
MERGE mydataset.Inventory AS I
USING tmp AS T
ON I.product = T.product
WHEN NOT MATCHED THEN
 INSERT(product, quantity, supply_constrained)
 VALUES(product, quantity, false)
WHEN MATCHED THEN
 UPDATE SET quantity = I.quantity + T.quantity;

-- Drop the temporary table and commit the transaction.
DROP TABLE tmp;

COMMIT TRANSACTION;
```

## 交易並行

如果交易會變更 (更新或刪除) 資料表中的資料列，則其他會變更相同資料表中資料列的交易或 DML 陳述式就無法同時執行。系統會取消衝突的交易。在交易外執行的衝突 DML 陳述式會排入佇列，稍後再執行，但須遵守[佇列限制](https://docs.cloud.google.com/bigquery/docs/data-manipulation-language?hl=zh-tw#update_delete_merge_dml_concurrency)。

讀取或附加新資料列的作業可以與交易同時執行。舉例來說，當交易在資料表中變更資料時，可以同時對該資料表執行下列任一作業：

* `SELECT` 個陳述式
* BigQuery Storage Read API 讀取作業
* BigQuery BI Engine 的查詢
* `INSERT` 個陳述式
* 使用 `WRITE_APPEND` 處置方式附加資料列的載入工作
* 串流寫入

如果交易只讀取資料表或將新資料列附加至資料表，則可在該資料表上同時執行任何作業。

## 查看交易資訊

BigQuery 會為每筆多陳述式交易指派交易 ID。交易 ID 會附加至交易中執行的每項查詢。如要查看工作的交易 ID，請查詢 [`INFORMATION_SCHEMA.JOBS*`](https://docs.cloud.google.com/bigquery/docs/information-schema-jobs?hl=zh-tw) 檢視表的 `transaction_id` 欄。

執行多陳述式交易時，BigQuery 會為交易中的每個陳述式建立子工作。對於特定交易，與該交易相關聯的每個子項工作都具有相同的 `transaction_id` 值。

以下範例說明如何查看交易資訊。

### 找出所有已提交或復原的交易

下列查詢會傳回所有成功提交的交易。

```
SELECT transaction_id, parent_job_id, query
FROM `region-us`.INFORMATION_SCHEMA.JOBS_BY_PROJECT
WHERE statement_type = "COMMIT_TRANSACTION" AND error_result IS NULL;
```

下列查詢會傳回所有成功復原的交易。

```
SELECT
  transaction_id, parent_job_id, query
FROM `region-us`.INFORMATION_SCHEMA.JOBS_BY_PROJECT
WHERE statement_type = "ROLLBACK_TRANSACTION" AND error_result IS NULL;
```

### 查看交易的開始和結束時間

下列查詢會傳回指定交易 ID 的開始和結束時間。

```
SELECT transaction_id, start_time, end_time, statement_type
FROM `region-us`.INFORMATION_SCHEMA.JOBS_BY_USER
WHERE transaction_id = "TRANSACTION_ID"
AND statement_type IN
  ("BEGIN_TRANSACTION", "COMMIT_TRANSACTION", "ROLLBACK_TRANSACTION")
ORDER BY start_time;
```

### 找出執行工作的交易

下列查詢會取得與指定工作 ID 相關聯的交易。如果工作並非在多陳述式交易中執行，則會傳回 `NULL`。

```
SELECT transaction_id
FROM `region-us`.INFORMATION_SCHEMA.JOBS_BY_PROJECT
WHERE job_id = 'JOB_ID';
```

### 找出交易中目前執行的工作

下列查詢會傳回目前在指定交易中執行的工作相關資訊 (如有)。

```
SELECT job_id, query, start_time, total_slot_ms
FROM `region-us`.INFORMATION_SCHEMA.JOBS_BY_PROJECT
WHERE transaction_id = 'TRANSACTION_ID' AND state = RUNNING;
```

### 找出影響資料表的有效交易

下列查詢會傳回影響指定資料表的有效交易。如果交易是以多重陳述式查詢的一部分執行 (例如在[預存程序](https://docs.cloud.google.com/bigquery/docs/procedures?hl=zh-tw)中)，則每筆進行中的交易也會傳回父項工作 ID。如果交易是在工作階段中執行，則也會傳回工作階段資訊。

```
WITH running_transactions AS (
  SELECT DISTINCT transaction_id
  FROM
    `region-us`.INFORMATION_SCHEMA.JOBS_BY_PROJECT
  EXCEPT DISTINCT
  SELECT transaction_id
  FROM
    `region-us`.INFORMATION_SCHEMA.JOBS_BY_PROJECT
  WHERE
    statement_type = 'COMMIT_TRANSACTION'
    OR statement_type = 'ROLLBACK_TRANSACTION'
)
SELECT
  jobs.transaction_id, parent_job_id, session_info, query
FROM
  `region-us`.INFORMATION_SCHEMA.JOBS_BY_PROJECT AS jobs, running_transactions
WHERE
  destination_table = ("PROJECT_NAME", "DATASET_NAME", "TABLE_NAME")
  AND jobs.transaction_id = running_transactions.transaction_id;
```

### 找出在多陳述式交易中執行的有效交易

下列查詢會傳回特定工作的有效交易，並以執行多陳述式交易的工作 ID 指定。

```
SELECT DISTINCT transaction_id
FROM
  `region-us`.INFORMATION_SCHEMA.JOBS_BY_PROJECT
WHERE
  parent_job_id = "JOB_ID"
EXCEPT DISTINCT
SELECT transaction_id
FROM
  `region-us`.INFORMATION_SCHEMA.JOBS_BY_PROJECT
WHERE
  parent_job_id = "JOB_ID"
  AND (statement_type = 'COMMIT_TRANSACTION'
       OR statement_type = 'ROLLBACK_TRANSACTION');
```

## 限制

* 交易無法使用會影響永久實體的 DDL 陳述式。
* 在交易中，[materialized view](https://docs.cloud.google.com/bigquery/docs/materialized-views-intro?hl=zh-tw) 會解讀為邏輯檢視表。您仍可在交易中查詢 materialized view，但與對等的邏輯檢視表相比，效能不會提升，成本也不會降低。
* 如果多陳述式交易失敗，系統會觸發復原作業，復原所有待變更項目，並防止重試。
* 一筆交易最多可變更 100 個資料表中的資料，且最多可執行 100,000 次分區修改。
* [BI Engine](https://docs.cloud.google.com/bigquery/docs/bi-engine-intro?hl=zh-tw) 不會加速交易中的查詢。
* 無法使用[系統程序](https://docs.cloud.google.com/bigquery/docs/reference/system-procedures?hl=zh-tw#bqrefresh_external_metadata_cache)在交易中重新整理外部資料來源的中繼資料。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-10-16 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-10-16 (世界標準時間)。"],[],[]]