Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見

# 使用遞迴式 CTE 透過集合功能整理內容 你可以依據偏好儲存及分類內容。

在 GoogleSQL for BigQuery 中，`WITH` 子句包含一或多個通用資料表運算式 (CTE)，您可以在查詢運算式中參照這些運算式。CTE 可以是[非遞迴](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw#simple_cte)、[遞迴](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw#recursive_cte)或兩者兼具。[`RECURSIVE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw#recursive_keyword) 關鍵字會在 `WITH` 子句 (`WITH RECURSIVE`) 中啟用遞迴。

遞迴 CTE 可以參照自身、前一個 CTE 或後續 CTE。非遞迴 CTE 只能參照前面的 CTE，無法參照自身。遞迴 CTE 會持續執行，直到找不到新結果為止，而非遞迴 CTE 則只會執行一次。因此，遞迴 CTE 通常用於查詢階層式資料和圖形資料。

舉例來說，假設有一個圖表，其中每一列代表一個可連結至其他節點的節點。如要從特定起始節點找出所有可連線節點的可轉移閉包，但不知道躍點數上限，您需要在查詢中使用遞迴 CTE (`WITH RECURSIVE`)。遞迴查詢會從起始節點的基本案例開始，每個步驟都會計算新的未見節點，這些節點可從目前為止看到的所有節點連線到上一個步驟。找不到新節點時，查詢就會結束。

不過，遞迴 CTE 可能會耗用大量運算資源，因此使用前請詳閱本指南和 GoogleSQL 參考文件的 [`WITH` 子句](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw#with_clause)一節。

## 建立遞迴 CTE

如要在 GoogleSQL 中建立遞迴 CTE，請使用 [`WITH RECURSIVE` 子句](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw#with_clause)，如以下範例所示：

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

遞迴 CTE 包含基本詞彙、聯集運算子和遞迴詞彙。基本詞彙會執行遞迴聯集運算的第一個疊代。遞迴詞彙會執行剩餘的反覆運算，且必須包含一個對遞迴 CTE 的自我參照。只有遞迴詞彙可以包含自我參照。

在上述範例中，遞迴 CTE 包含下列元件：

* 遞迴 CTE 名稱：`CTE_1`
* 基本條款：`SELECT 1 AS iteration`
* 聯集運算子：`UNION ALL`
* 遞迴詞：`SELECT iteration + 1 AS iteration FROM CTE_1 WHERE
  iteration < 3`

如要進一步瞭解遞迴 CTE 語法、規則和範例，請參閱 GoogleSQL 參考文件中的 [`WITH` 子句](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw#with_clause)。

## 探索有向無環圖 (DAG) 的可達性

您可以使用遞迴查詢，探索有向無環圖 (DAG) 中的可連性。下列查詢會找出圖表 `GraphData` 中可從節點 `5` 連接的所有節點：

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

遞迴 CTE 可能會導致無限遞迴，也就是遞迴詞彙持續執行，但未達到終止條件。為終止無限遞迴，系統會強制限制每個遞迴 CTE 的疊代次數。BigQuery 的疊代次數上限為 500 次。遞迴 CTE 達到疊代次數上限後，CTE 執行作業會中止並顯示錯誤。

之所以有這項限制，是因為遞迴 CTE 的運算可能耗費大量資源，而執行具有大量疊代的 CTE 會耗用大量系統資源，且需要更長的時間才能完成。

達到疊代限制的查詢通常缺少適當的終止條件，因此會建立無限迴圈，或在不適當的情境中使用遞迴 CTE。

如果遇到遞迴疊代限制錯誤，請參閱本節的建議。

### 檢查是否有無限遞迴

為避免無限遞迴，請確保遞迴詞彙在執行特定次數的疊代後，能夠產生空白結果。

如要檢查無限遞迴，其中一種方法是將遞迴 CTE 轉換為 `TEMP TABLE`，並針對前 `100` 次疊代使用 `REPEAT` 迴圈，如下所示：

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
* `base_expression`：遞迴 CTE 的基本詞彙。
* `recursive_expression`：遞迴 CTE 的遞迴詞。
* `termination_condition_expression`：遞迴 CTE 的終止運算式。

舉例來說，請考慮下列名為 `TestCTE` 的遞迴 CTE：

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

因此，下列程式碼會測試 `TestCTE` 是否有無限遞迴：

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

上述範例會產生下列結果，其中包含疊代 ID 和該疊代期間產生的資料列數量：

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

如果資料列數量一律大於零 (如本例所示)，則範例可能會有無限遞迴。

### 確認遞迴 CTE 的適當用法

確認您在適當的情境中使用遞迴 CTE。遞迴 CTE 是設計用來查詢階層式資料和圖形資料，因此運算成本可能很高。如果您不是查詢這兩種資料，請考慮其他替代方案，例如使用 [`LOOP` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/procedural-language?hl=zh-tw#loop)搭配非遞迴 CTE。

### 將遞迴 CTE 分割成多個遞迴 CTE

如果您認為遞迴 CTE 需要超過允許的疊代次數上限，可以將遞迴 CTE 拆分為多個遞迴 CTE。

您可以使用類似下方的查詢結構，分割遞迴 CTE：

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
* `recursive_expression`：目前 CTE 的遞迴詞彙運算式。

舉例來說，下列程式碼會將一個 CTE 分割成三個不同的 CTE：

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

在上述範例中，500 次疊代會替換為 10 次疊代，以便更快查看查詢結果。查詢會產生 30 個資料列，但每個遞迴 CTE 只會疊代 10 次。輸出內容如下所示：

```
/*-----------+
 | iteration |
 +-----------+
 | 2         |
 | ...       |
 | 30        |
 +-----------*/
```

您可以對先前的查詢進行更多次疊代測試。

### 使用迴圈，而非遞迴 CTE

為避免疊代次數限制，建議使用迴圈，而非遞迴 CTE。您可以使用多種迴圈陳述式建立迴圈，例如 `LOOP`、`REPEAT` 或 `WHILE`。詳情請參閱「[迴圈](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/procedural-language?hl=zh-tw#loops)」。

### 變更遞迴限制

如果您認為下列因素適用，請與客戶服務聯絡，提高遞迴限制：

* 您有正當理由讓遞迴 CTE 執行超過 500 次疊代。
* 您可以接受較長的執行時間。

請注意，提高遞迴限制可能會有潛在風險：

* CTE 可能會失敗，並顯示其他錯誤訊息，例如記憶體超出上限或逾時。
* 如果專案採用的是隨選計價模式，CTE 可能仍會發生計費級別錯誤，直到您改用以運算資源為準的計價模式為止。
* 如果遞迴 CTE 的疊代次數過多，會耗用大量資源。這可能會影響在相同預留項目中執行的其他查詢，因為這些查詢會爭用共用資源。

## 定價

如果您使用[隨選計費](https://cloud.google.com/bigquery/pricing?hl=zh-tw#on_demand_pricing)，BigQuery 會根據執行含有遞迴 CTE 的查詢時處理的位元組數收費。

詳情請參閱「[查詢大小計算](https://docs.cloud.google.com/bigquery/docs/estimate-costs?hl=zh-tw#query_size_calculation)」。

## 配額

如要瞭解遞迴 CTE 配額和限制，請參閱「[配額和限制](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#recursive-ctes-limits)」。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-10-29 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-10-29 (世界標準時間)。"],[],[]]