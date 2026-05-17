Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見

# 使用遞迴式 CTE 透過集合功能整理內容 你可以依據偏好儲存及分類內容。

在 BigQuery 的 GoogleSQL 中，`WITH` 子句包含一或多個通用資料表運算式 (CTE)，您可以在查詢運算式中參照這些運算式。CTE 可以是[非遞迴](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw#simple_cte)、[遞迴](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw#recursive_cte)或兩者皆是。[`RECURSIVE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw#recursive_keyword) 關鍵字會在 `WITH` 子句 (`WITH RECURSIVE`) 中啟用遞迴。

遞迴 CTE 可以參照自身、前一個 CTE 或後續 CTE。非遞迴 CTE 只能參照先前的 CTE，不能參照自身。遞迴 CTE 會持續執行，直到找不到新結果為止，而非遞迴 CTE 則只會執行一次。因此，遞迴 CTE 通常用於查詢階層式資料和圖形資料。

舉例來說，假設有一個圖表，其中每一列代表一個節點，可連結至其他節點。如要找出特定開始節點中所有可連線節點的遞移封閉，但不知道最大躍點數，您需要在查詢中使用遞迴 CTE (`WITH RECURSIVE`)。遞迴查詢會從開始節點的基本情況開始，每個步驟都會計算從先前步驟中所有節點可連線的新節點。找不到新節點時，查詢就會結束。

不過，遞迴 CTE 的運算成本可能很高，因此使用前請先參閱本指南和 GoogleSQL 參考文件 的[`WITH` 子句](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw#with_clause)部分。

## 建立遞迴 CTE

如要在 GoogleSQL 中建立遞迴 CTE，請使用 [`WITH RECURSIVE` 子句](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw#with_clause)，如下列範例所示：

```
WITH RECURSIVE
  CTE_1 AS (
    (SELECT 1 AS iteration UNION ALL SELECT 1 AS iteration)
    UNION ALL
    SELECT iteration + 1 AS iteration FROM CTE_1 WHERE iteration < 3
  )
SELECT iteration FROM CTE_1
ORDER BY 1 ASC
```

上述範例會產生下列結果：

```
/*-----------+
 | iteration |
 +-----------+
 | 1         |
 | 1         |
 | 2         |
 | 2         |
 | 3         |
 | 3         |
 +-----------*/
```

遞迴 CTE 包含基本項、聯集運算子和遞迴項。
基礎字詞會執行遞迴聯集作業的第一個疊代。遞迴項會執行其餘反覆運算，且必須包含對遞迴 CTE 的一個自我參照。只有遞迴項可以包含自我參照。

在上述範例中，遞迴 CTE 包含下列元件：

* 遞迴 CTE 名稱：`CTE_1`
* 基本字詞：`SELECT 1 AS iteration`
* 聯集運算子：`UNION ALL`
* 遞迴項：`SELECT iteration + 1 AS iteration FROM CTE_1 WHERE
  iteration < 3`

如要進一步瞭解遞迴 CTE 語法、規則和範例，請參閱 GoogleSQL 參考文件中的 [`WITH` 子句](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw#with_clause)。

## 探索有向無環圖 (DAG) 中的可達性

您可以使用遞迴查詢，探索有向無環圖 (DAG) 中的可到達性。下列查詢會在名為 `GraphData` 的圖表中，找出可從節點 `5` 抵達的所有節點：

```
WITH RECURSIVE
  GraphData AS (
    --    1          5
    --   / \        / \
    --  2 - 3      6   7
    --      |       \ /
    --      4        8
    SELECT 1 AS from_node, 2 AS to_node UNION ALL
    SELECT 1, 3 UNION ALL
    SELECT 2, 3 UNION ALL
    SELECT 3, 4 UNION ALL
    SELECT 5, 6 UNION ALL
    SELECT 5, 7 UNION ALL
    SELECT 6, 8 UNION ALL
    SELECT 7, 8
  ),
  R AS (
    (SELECT 5 AS node)
    UNION ALL
    (
      SELECT GraphData.to_node AS node
      FROM R
      INNER JOIN GraphData
        ON (R.node = GraphData.from_node)
    )
  )
SELECT DISTINCT node FROM R ORDER BY node;
```

上述範例會產生下列結果：

```
/*------+
 | node |
 +------+
 | 5    |
 | 6    |
 | 7    |
 | 8    |
 +------*/
```

## 排解疊代限制錯誤

遞迴 CTE 可能會導致無限遞迴，也就是遞迴項持續執行，但未達到終止條件。為終止無限遞迴，系統會對每個遞迴 CTE 強制執行疊代次數限制。如果是 BigQuery，疊代次數上限為 500 次。遞迴 CTE 達到疊代次數上限後，CTE 執行作業就會因錯誤而中止。

由於遞迴 CTE 的運算成本可能很高，因此設有這項限制。如果 CTE 的疊代次數過多，就會耗用大量系統資源，且需要很長時間才能完成。

達到疊代限制的查詢通常缺少適當的終止條件，因此會建立無限迴圈，或是在不適當的情況下使用遞迴 CTE。

如果遇到遞迴疊代限制錯誤，請參閱本節的建議。

### 檢查無限遞迴

為避免無限遞迴，請確保遞迴項在執行一定次數的疊代後，能夠產生空白結果。

如要檢查無限遞迴，方法之一是將遞迴 CTE 轉換為 `TEMP TABLE`，並在第一次 `100` 疊代時使用 `REPEAT` 迴圈，如下所示：

```
DECLARE current_iteration INT64 DEFAULT 0;

CREATE TEMP TABLE recursive_cte_name AS
SELECT base_expression, current_iteration AS iteration;

REPEAT
  SET current_iteration = current_iteration + 1;
  INSERT INTO recursive_cte_name
    SELECT recursive_expression, current_iteration
    FROM recursive_cte_name
    WHERE termination_condition_expression
      AND iteration = current_iteration - 1
      AND current_iteration < 100;
  UNTIL NOT EXISTS(SELECT * FROM recursive_cte_name WHERE iteration = current_iteration)
END REPEAT;
```

替換下列值：

* `recursive_cte_name`：要偵錯的遞迴 CTE。
* `base_expression`：遞迴 CTE 的基本條件。
* `recursive_expression`：遞迴 CTE 的遞迴項。
* `termination_condition_expression`：遞迴 CTE 的終止運算式。

舉例來說，請思考下列名為 `TestCTE` 的遞迴 CTE：

```
WITH RECURSIVE
  TestCTE AS (
    SELECT 1 AS n
    UNION ALL
    SELECT n + 3 FROM TestCTE WHERE MOD(n, 6) != 0
  )
```

本範例使用下列值：

* `recursive_cte_name`：`TestCTE`
* `base_expression`：`SELECT 1`
* `recursive_expression`：`n + 3`
* `termination_condition_expression`：`MOD(n, 6) != 0`

因此，下列程式碼會測試 `TestCTE` 是否出現無限遞迴：

```
DECLARE current_iteration INT64 DEFAULT 0;

CREATE TEMP TABLE TestCTE AS
SELECT 1 AS n, current_iteration AS iteration;

REPEAT
SET current_iteration = current_iteration + 1;

INSERT INTO TestCTE
SELECT n + 3, current_iteration
FROM TestCTE
WHERE
  MOD(n, 6) != 0
  AND iteration = current_iteration - 1
  AND current_iteration < 10;

UNTIL
  NOT EXISTS(SELECT * FROM TestCTE WHERE iteration = current_iteration)
    END REPEAT;

-- Print the number of rows produced by each iteration

SELECT iteration, COUNT(1) AS num_rows
FROM TestCTE
GROUP BY iteration
ORDER BY iteration;

-- Examine the actual result produced for a specific iteration

SELECT * FROM TestCTE WHERE iteration = 2;
```

上述範例會產生下列結果，包括疊代 ID 和該疊代期間產生的資料列數：

```
/*-----------+----------+
 | iteration | num_rows |
 +-----------+----------+
 | 0         | 1        |
 | 1         | 1        |
 | 2         | 1        |
 | 3         | 1        |
 | 4         | 1        |
 | 5         | 1        |
 | 6         | 1        |
 | 7         | 1        |
 | 8         | 1        |
 | 9         | 1        |
 | 10        | 1        |
 +-----------+----------*/
```

以下是疊代 `2` 期間產生的實際結果：

```
/*----------+-----------+
 | n        | iteration |
 +----------+-----------+
 | 7        | 2         |
 +----------+-----------*/
```

如果資料列數一律大於零 (本例中確實如此)，則樣本很可能具有無限遞迴。

### 確認遞迴 CTE 的適當用法

確認您在適當情境中使用遞迴 CTE。
遞迴 CTE 的設計目的是查詢階層式資料和圖形資料，因此運算成本可能很高。如果您並未查詢這兩種資料，建議改用其他方法，例如搭配非遞迴 CTE 使用 [`LOOP` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/procedural-language?hl=zh-tw#loop)。

### 將遞迴 CTE 分割為多個遞迴 CTE

如果遞迴 CTE 需要的疊代次數超過上限，或許可以將遞迴 CTE 分解為多個遞迴 CTE。

您可以透過類似下列查詢結構的查詢，分割遞迴 CTE：

```
WITH RECURSIVE
  CTE_1 AS (
    SELECT base_expression
    UNION ALL
    SELECT recursive_expression FROM CTE_1 WHERE iteration < 500
  ),
  CTE_2 AS (
    SELECT * FROM CTE_1 WHERE iteration = 500
    UNION ALL
    SELECT recursive_expression FROM CTE_2 WHERE iteration < 500 * 2
  ),
  CTE_3 AS (
    SELECT * FROM CTE_2 WHERE iteration = 500 * 2
    UNION ALL
    SELECT recursive_expression FROM CTE_3 WHERE iteration < 500 * 3
  ),
  [, ...]
SELECT * FROM CTE_1
UNION ALL SELECT * FROM CTE_2 WHERE iteration > 500
UNION ALL SELECT * FROM CTE_3 WHERE iteration > 500 * 2
[...]
```

替換下列值：

* `base_expression`：目前 CTE 的基本字詞運算式。
* `recursive_expression`：目前 CTE 的遞迴項運算式。

舉例來說，下列程式碼會將 CTE 分割成三個不同的 CTE：

```
WITH RECURSIVE
  CTE_1 AS (
    SELECT 1 AS iteration
    UNION ALL
    SELECT iteration + 1 AS iteration FROM CTE_1 WHERE iteration < 10
  ),
  CTE_2 AS (
    SELECT * FROM CTE_1 WHERE iteration = 10
    UNION ALL
    SELECT iteration + 1 AS iteration FROM CTE_2 WHERE iteration < 10 * 2
  ),
  CTE_3 AS (
    SELECT * FROM CTE_2 WHERE iteration = 10 * 2
    UNION ALL
    SELECT iteration + 1 AS iteration FROM CTE_3 WHERE iteration < 10 * 3
  )
SELECT iteration FROM CTE_1
UNION ALL
SELECT iteration FROM CTE_2 WHERE iteration > 10
UNION ALL
SELECT iteration FROM CTE_3 WHERE iteration > 20
ORDER BY 1 ASC
```

在上述範例中，我們將 500 次疊代替換為 10 次疊代，以便更快查看查詢結果。這項查詢會產生 30 個資料列，但每個遞迴 CTE 只會疊代 10 次。輸出內容如下所示：

```
/*-----------+
 | iteration |
 +-----------+
 | 2         |
 | ...       |
 | 30        |
 +-----------*/
```

您可以在更大的疊代中測試先前的查詢。

### 請使用迴圈，而非遞迴 CTE

為避免達到疊代次數上限，請考慮使用迴圈，而非遞迴 CTE。
您可以使用多種迴圈陳述式建立迴圈，例如 `LOOP`、`REPEAT` 或 `WHILE`。詳情請參閱「[迴圈](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/procedural-language?hl=zh-tw#loops)」。

### 變更遞迴限制

如果您認為適用下列因素，請與客戶服務團隊聯絡，以提高遞迴限制：

* 遞迴 CTE 有充分的理由執行超過 500 次疊代。
* 您可接受執行時間較長。

請注意，提高遞迴限制可能會有以下風險：

* 您的 CTE 可能會失敗，並顯示其他錯誤訊息，例如超出記憶體或逾時。
* 如果專案使用隨選價格模式，您可能仍會收到帳單層級錯誤，導致 CTE 失敗，直到切換至以容量為準的價格模式為止。
* 如果遞迴 CTE 的疊代次數過多，就會耗用大量資源。這可能會影響在相同預訂中執行的其他查詢，因為這些查詢會爭用共用資源。

## 定價

如果您採用[以量計價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#on_demand_pricing)方案，BigQuery 會根據執行遞迴 CTE 查詢時處理的位元組數計費。

詳情請參閱[查詢大小計算方式](https://docs.cloud.google.com/bigquery/docs/estimate-costs?hl=zh-tw#query_size_calculation)。

## 配額

如要瞭解遞迴 CTE 配額和限制，請參閱「[配額與限制](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#recursive-ctes-limits)」。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-16 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-16 (世界標準時間)。"],[],[]]