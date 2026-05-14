Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 函式的最佳做法

本文說明如何最佳化使用 SQL 函式的查詢。

## 最佳化字串比較

**最佳做法：**盡可能使用 `LIKE`，而非 `REGEXP_CONTAINS`。

在 BigQuery 中，您可以使用 [`REGEXP_CONTAINS`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/string_functions?hl=zh-tw#regexp_contains) 函式或 [`LIKE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/operators?hl=zh-tw#comparison_operators) 運算子比較字串。`REGEXP_CONTAINS`提供更多功能，但執行時間較慢。使用 `LIKE` 而不是 `REGEXP_CONTAINS` 會更快，特別是當您不需要 `REGEXP_CONTAINS` 提供的完整規則運算式功能時，例如萬用字元比對。

請參考下列 `REGEXP_CONTAINS` 函式用法：

```
SELECT
  dim1
FROM
  `dataset.table1`
WHERE
  REGEXP_CONTAINS(dim1, '.*test.*');
```

您可以按照下列方式最佳化這項查詢：

```
SELECT
  dim1
FROM
  `dataset.table`
WHERE
  dim1 LIKE '%test%';
```

## 最佳化匯總函式

**最佳做法：**如果您的應用實例支援的話，請使用近似匯總函式。

如果您使用的 SQL 匯總函式有對應的近似函式，近似函式可加快查詢執行速度。舉例來說，請使用 [`APPROX_COUNT_DISTINCT`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/approximate_aggregate_functions?hl=zh-tw#approx_count_distinct)，而非 [`COUNT(DISTINCT)`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/aggregate_functions?hl=zh-tw#count)。詳情請參閱[近似匯總函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/approximate_aggregate_functions?hl=zh-tw)。

您也可以使用 `HyperLogLog++` 函式來計算近似值 (包括自訂近似匯總)。詳情請參閱 GoogleSQL 參考資料中的 [HyperLogLog++ 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/hll_functions?hl=zh-tw)。

請參考下列 `COUNT` 函式用法：

```
SELECT
  dim1,
  COUNT(DISTINCT dim2)
FROM
  `dataset.table`
GROUP BY 1;
```

您可以按照下列方式最佳化這項查詢：

```
SELECT
  dim1,
  APPROX_COUNT_DISTINCT(dim2)
FROM
  `dataset.table`
GROUP BY 1;
```

### 最佳化分位數函式

**最佳做法：**盡可能使用 `APPROX_QUANTILE`，而非 `NTILE`。

如果單一分割區中有太多要 `ORDER BY` 的元素，導致資料量增加，執行含有 [`NTILE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/numbering_functions?hl=zh-tw#ntile) 函式的查詢可能會失敗，並顯示 [`Resources exceeded`](https://docs.cloud.google.com/bigquery/troubleshooting-errors?hl=zh-tw#resourcesExceeded) 錯誤。分析視窗未經過分區，因此 `NTILE` 運算需要由單一工作者/運算單元處理表格中所有資料列的`ORDER BY`。

請改用 [`APPROX_QUANTILES`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/approximate_aggregate_functions?hl=zh-tw#approx_quantiles)。這項函式可讓查詢更有效率地執行，因為不需要資料表中所有列的 `ORDER BY`。

請參考下列 `NTILE` 函式用法：

```
SELECT
  individual_id,
  NTILE(nbuckets) OVER (ORDER BY sales desc) AS sales_third
FROM
  `dataset.table`;
```

您可以按照下列方式最佳化這項查詢：

```
WITH QuantInfo AS (
  SELECT
    o, qval
  FROM UNNEST((
     SELECT APPROX_QUANTILES(sales, nbuckets)
     FROM `dataset.table`
    )) AS qval
  WITH offset o
  WHERE o > 0
)
SELECT
  individual_id,
  (SELECT
     (nbuckets + 1) - MIN(o)
   FROM QuantInfo
   WHERE sales <= QuantInfo.qval
  ) AS sales_third
FROM `dataset.table`;
```

最佳化版本會提供與原始查詢類似但不完全相同的結果，因為 `APPROX_QUANTILES`：

1. 提供近似匯總。
2. 以不同方式放置餘數值 (資料列數除以值區後的餘數)。

## 最佳化 UDF

**最佳做法：**使用 SQL UDF 進行簡單計算，因為查詢最佳化工具可以對 SQL UDF 定義套用最佳化。如果 SQL UDF 無法支援複雜的計算，請使用 JavaScript UDF。

呼叫 JavaScript UDF 時，需要例項化子程序。
直接啟動這項程序並執行 UDF 會影響查詢成效。如果可行，請改用[原生 (SQL) UDF](https://docs.cloud.google.com/bigquery/docs/user-defined-functions?hl=zh-tw#sql-udf-structure)。

### 永久性 UDF

建議您在集中式 BigQuery 資料集中建立持續性使用者定義 SQL 和 JavaScript 函式，以便在查詢和邏輯檢視區塊中叫用，而不是每次都在程式碼中建立及呼叫 UDF。在共用資料集中建立全機構的商業邏輯程式庫，有助於提升效能並減少資源用量。

以下範例說明如何在查詢中叫用暫時性 UDF：

```
CREATE TEMP FUNCTION addFourAndDivide(x INT64, y INT64) AS ((x + 4) / y);

WITH numbers AS
  (SELECT 1 as val
  UNION ALL
  SELECT 3 as val
  UNION ALL
  SELECT 4 as val
  UNION ALL
  SELECT 5 as val)
SELECT val, addFourAndDivide(val, 2) AS result
FROM numbers;
```

您可以將暫時性 UDF 換成永久性 UDF，藉此最佳化這項查詢：

```
WITH numbers AS
  (SELECT 1 as val
  UNION ALL
  SELECT 3 as val
  UNION ALL
  SELECT 4 as val
  UNION ALL
  SELECT 5 as val)
SELECT val, `your_project.your_dataset.addFourAndDivide`(val, 2) AS result
FROM numbers;
```

## 最佳化 AI 成本

**最佳做法：**如果您的用途支援，請在大型資料集上執行 `AI.IF` 或 `AI.CLASSIFY` 時使用最佳化模式。

如果您使用受管理 AI 函式處理的資料列超過幾千列，可以啟用最佳化模式，自動訓練輕量型精簡模型。這可大幅減少 LLM 權杖用量和查詢延遲時間。詳情請參閱「[針對大規模資料最佳化 AI 函式](https://docs.cloud.google.com/bigquery/docs/optimize-ai-functions?hl=zh-tw)」。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-14 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-14 (世界標準時間)。"],[],[]]