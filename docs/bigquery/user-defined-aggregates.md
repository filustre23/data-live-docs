Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 使用者定義的匯總函式

本文說明如何在 BigQuery 中建立、呼叫及刪除使用者定義的匯總函式 (UDAF)。

您可以使用含有程式碼的運算式，透過 UDAF 建立匯總函式。UDAF 可接受輸入資料欄、一次對一組資料列執行計算，然後將計算結果以單一值的形式傳回。

## 建立 SQL UDAF

本節說明在 BigQuery 中建立永久或暫時 SQL UDAF 的各種方法。

### 建立永久性 SQL UDAF

您可以建立永久性 SQL UDAF，也就是在多個查詢中重複使用 UDAF。如果擁有者之間共用持續性 UDAF，則可安全地呼叫這些 UDAF。UDAF 無法變更資料、與外部系統通訊，或將記錄傳送至 Google Cloud Observability 或類似應用程式。

如要建立永久性 UDAF，請使用[`CREATE AGGREGATE FUNCTION` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#sql-create-udaf-function)，但不要使用 `TEMP` 或 `TEMPORARY` 關鍵字。您必須在函式路徑中加入資料集。

舉例來說，下列查詢會建立名為 `ScaledAverage` 的永久性 UDAF：

```
CREATE AGGREGATE FUNCTION myproject.mydataset.ScaledAverage(
  dividend FLOAT64,
  divisor FLOAT64)
RETURNS FLOAT64
AS (
  AVG(dividend / divisor)
);
```

### 建立暫時性 SQL UDAF

您可以建立暫時性 SQL UDAF，也就是說，UDAF 只存在於單一查詢、指令碼、工作階段或程序的範圍內。

如要建立暫時性 UDAF，請使用 [`CREATE AGGREGATE FUNCTION` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#sql-create-udaf-function)，並搭配 `TEMP` 或 `TEMPORARY` 關鍵字。

舉例來說，下列查詢會建立名為 `ScaledAverage` 的臨時 UDAF：

```
CREATE TEMP AGGREGATE FUNCTION ScaledAverage(
  dividend FLOAT64,
  divisor FLOAT64)
RETURNS FLOAT64
AS (
  AVG(dividend / divisor)
);
```

### 使用匯總和非匯總參數

您可以建立同時具有匯總和非匯總參數的 SQL UDAF。

UDAF 通常會匯總[群組](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw#group_by_clause)中所有資料列的函式參數。不過，您可以使用 `NOT AGGREGATE` 關鍵字，將函式參數指定為非匯總。

非匯總函式參數是純量函式參數，群組中所有資料列的值都相同。有效的非匯總函式參數必須是常值。在 UDAF 定義中，匯總函式參數只能做為匯總函式呼叫的函式引數。對非聚合函式參數的參照可出現在 UDAF 定義中的任何位置。

舉例來說，下列函式包含名為 `dividend` 的匯總參數，以及名為 `divisor` 的非匯總參數：

```
-- Create the function.
CREATE TEMP AGGREGATE FUNCTION ScaledSum(
  dividend FLOAT64,
  divisor FLOAT64 NOT AGGREGATE)
RETURNS FLOAT64
AS (
  SUM(dividend) / divisor
);
```

### 在函式主體中使用預設專案

在 SQL UDAF 的主體中，凡是參照 BigQuery 實體 (例如資料表或檢視區塊)，都必須包含專案 ID，除非實體位於包含 UDAF 的專案中。

舉例來說，請看以下陳述：

```
CREATE AGGREGATE FUNCTION project1.dataset_a.ScaledAverage(
  dividend FLOAT64,
  divisor FLOAT64)
RETURNS FLOAT64
AS (
  ( SELECT AVG(dividend / divisor) FROM dataset_a.my_table )
);
```

如果您在 `project1` 專案中執行上述陳述式，該陳述式會成功，因為 `project1` 中存在 `my_table`。不過，如果您從其他專案執行上述陳述式，該陳述式就會失敗。如要修正錯誤，請在表格參照中加入專案 ID：

```
CREATE AGGREGATE FUNCTION project1.dataset_a.ScaledAverage(
  dividend FLOAT64,
  divisor FLOAT64)
RETURNS FLOAT64
AS (
  ( SELECT AVG(dividend / divisor) FROM project1.dataset_a.my_table )
);
```

您也可以參照其他專案或資料集中的實體，不必與建立函式的專案或資料集相同：

```
CREATE AGGREGATE FUNCTION project1.dataset_a.ScaledAverage(
  dividend FLOAT64,
  divisor FLOAT64)
RETURNS FLOAT64
AS (
  ( SELECT AVG(dividend / divisor) FROM project2.dataset_c.my_table )
);
```

## 建立 JavaScript UDAF

本節說明在 BigQuery 中建立 JavaScript UDAF 的各種方式。建立 JavaScript UDAF 時，請遵守下列幾項規則：

* JavaScript UDAF 的主體必須是代表 JavaScript 程式碼的引號字串文字。如要進一步瞭解可使用的不同類型引號字串文字，請參閱「[引號文字格式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/lexical?hl=zh-tw#quoted_literals)」。
* 系統只允許特定類型的編碼。詳情請參閱「[JavaScript UDAF 中允許的 SQL 類型編碼](#javascript-type-encodings)」。
* JavaScript 函式主體必須包含四個 JavaScript 函式，用於初始化、彙整、合併及完成 JavaScript UDAF 的結果 (`initialState`、`aggregate`、`merge` 和 `finalize`)。詳情請參閱[必要的 JavaScript 彙整函式](#required-javascript-aggregate-functions)。
* `initialState` 函式傳回的任何值，或在呼叫 `aggregate` 或 `merge` 函式後留在 `state` 引數中的任何值，都必須可序列化。如要處理無法序列化的匯總資料 (例如函式或符號欄位)，請務必使用內含的 `serialize` 和 `deserialize` 函式。詳情請參閱「[在 JavaScript UDAF 中序列化及還原序列化資料](#serialize-javascript-udaf)」。

### 建立永久性 JavaScript UDAF

您可以建立永久性 JavaScript UDAF，也就是在多個查詢中重複使用 UDAF。如果擁有者之間共用持續性 UDAF，則可安全地呼叫這些 UDAF。UDAF 無法變更資料、與外部系統通訊，或將記錄傳送至 Google Cloud Observability 或類似應用程式。

如要建立永久性 UDAF，請使用[`CREATE AGGREGATE FUNCTION` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#javascript-create-udaf-function)，但不要使用 `TEMP` 或 `TEMPORARY` 關鍵字。您必須在函式路徑中加入資料集。

下列查詢會建立名為 `SumPositive` 的永久性 JavaScript UDAF：

```
CREATE OR REPLACE AGGREGATE FUNCTION my_project.my_dataset.SumPositive(x FLOAT64)
RETURNS FLOAT64
LANGUAGE js
AS r'''

  export function initialState() {
    return {sum: 0}
  }
  export function aggregate(state, x) {
    if (x > 0) {
      state.sum += x;
    }
  }
  export function merge(state, partialState) {
    state.sum += partialState.sum;
  }
  export function finalize(state) {
    return state.sum;
  }

''';

-- Call the JavaScript UDAF.
WITH numbers AS (
  SELECT * FROM UNNEST([1.0, -1.0, 3.0, -3.0, 5.0, -5.0]) AS x)
SELECT my_project.my_dataset.SumPositive(x) AS sum FROM numbers;

/*-----*
 | sum |
 +-----+
 | 9.0 |
 *-----*/
```

### 建立暫時性 JavaScript UDAF

您可以建立暫時性 JavaScript UDAF，也就是說，UDAF 只存在於單一查詢、指令碼、工作階段或程序的範圍內。

如要建立暫時性 UDAF，請使用 [`CREATE AGGREGATE FUNCTION` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#javascript-create-udaf-function)，並搭配 `TEMP` 或 `TEMPORARY` 關鍵字。

下列查詢會建立名為 `SumPositive` 的暫時性 JavaScript UDAF：

```
CREATE TEMP AGGREGATE FUNCTION SumPositive(x FLOAT64)
RETURNS FLOAT64
LANGUAGE js
AS r'''

  export function initialState() {
    return {sum: 0}
  }
  export function aggregate(state, x) {
    if (x > 0) {
      state.sum += x;
    }
  }
  export function merge(state, partialState) {
    state.sum += partialState.sum;
  }
  export function finalize(state) {
    return state.sum;
  }

''';

-- Call the JavaScript UDAF.
WITH numbers AS (
  SELECT * FROM UNNEST([1.0, -1.0, 3.0, -3.0, 5.0, -5.0]) AS x)
SELECT SumPositive(x) AS sum FROM numbers;

/*-----*
 | sum |
 +-----+
 | 9.0 |
 *-----*/
```

### 在 JavaScript UDAF 中加入非匯總參數

您可以建立同時具有匯總和非匯總參數的 JavaScript UDAF。

UDAF 通常會匯總[群組](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw#group_by_clause)中所有資料列的函式參數。不過，您可以使用 `NOT AGGREGATE` 關鍵字，將函式參數指定為非匯總。

非匯總函式參數是純量函式參數，群組中所有資料列的值都相同。有效的非匯總函式參數必須是常值。在 UDAF 定義中，匯總函式參數只能做為匯總函式呼叫的函式引數。對非聚合函式參數的參照可出現在 UDAF 定義中的任何位置。

在下列範例中，JavaScript UDAF 包含名為 `s` 的匯總參數，以及名為 `delimiter` 的非匯總參數：

```
CREATE TEMP AGGREGATE FUNCTION JsStringAgg(
  s STRING,
  delimiter STRING NOT AGGREGATE)
RETURNS STRING
LANGUAGE js
AS r'''

  export function initialState() {
    return {strings: []}
  }
  export function aggregate(state, s) {
    state.strings.push(s);
  }
  export function merge(state, partialState) {
    state.strings = state.strings.concat(partialState.strings);
  }
  export function finalize(state, delimiter) {
    return state.strings.join(delimiter);
  }

''';

-- Call the JavaScript UDAF.
WITH strings AS (
  SELECT * FROM UNNEST(["aaa", "bbb", "ccc", "ddd"]) AS values)
SELECT JsStringAgg(values, '.') AS result FROM strings;

/*-----------------*
 | result          |
 +-----------------+
 | aaa.bbb.ccc.ddd |
 *-----------------*/
```

### 在 JavaScript UDAF 中序列化及還原序列化資料

BigQuery 必須序列化 `initialState` 函式傳回的任何物件，或在呼叫 `aggregate` 或 `merge` 函式後，留在 `state` 引數中的物件。如果物件的所有欄位都屬於下列其中一種，BigQuery 就支援序列化物件：

* JavaScript 原始值 (例如：`2`、`"abc"`、`null`、`undefined`)。
* BigQuery 支援序列化所有欄位值的 JavaScript 物件。
* BigQuery 支援序列化所有元素的 JavaScript 陣列。

下列傳回值可序列化：

```
export function initialState() {
  return {a: "", b: 3, c: null, d: {x: 23} }
}
```

```
export function initialState() {
  return {value: 2.3};
}
```

下列傳回值無法序列化：

```
export function initialState() {
  return {
    value: function() {return 6;}
  }
}
```

```
export function initialState() {
  return 2.3;
}
```

如要使用無法序列化的匯總狀態，JavaScript UDAF 必須包含 `serialize` 和 `deserialize` 函式。`serialize` 函式會將聚合狀態轉換為可序列化的物件；`deserialize` 函式則會將可序列化的物件轉換回聚合狀態。

在下列範例中，外部程式庫會使用介面計算總和：

```
export class SumAggregator {
 constructor() {
   this.sum = 0;
 }
 update(value) {
   this.sum += value;
 }
 getSum() {
   return this.sum;
 }
}
```

由於類別內有函式，因此 `SumAggregator` 類別物件無法進行 BigQuery 序列化，導致下列查詢無法執行。

```
CREATE TEMP AGGREGATE FUNCTION F(x FLOAT64)
RETURNS FLOAT64
LANGUAGE js
AS r'''

  class SumAggregator {
   constructor() {
     this.sum = 0;
   }

   update(value) {
     this.sum += value;
   }

   getSum() {
     return this.sum;
   }
  }

  export function initialState() {
   return new SumAggregator();
  }

  export function aggregate(agg, value) {
   agg.update(value);
  }

  export function merge(agg1, agg2) {
   agg1.update(agg2.getSum());
  }

  export function finalize(agg) {
   return agg.getSum();
  }

''';

--Error: getSum is not a function
SELECT F(x) AS results FROM UNNEST([1,2,3,4]) AS x;
```

如果您將 `serialize` 和 `deserialize` 函式新增至上述查詢，查詢就會執行，因為 `SumAggregator` 類別物件會轉換為可供 BigQuery 序列化的物件，然後再轉換回 `SumAggregator` 類別物件。

```
CREATE TEMP AGGREGATE FUNCTION F(x FLOAT64)
RETURNS FLOAT64
LANGUAGE js
AS r'''

  class SumAggregator {
   constructor() {
     this.sum = 0;
   }

   update(value) {
     this.sum += value;
   }

   getSum() {
     return this.sum;
   }
  }

  export function initialState() {
   return new SumAggregator();
  }

  export function aggregate(agg, value) {
   agg.update(value);
  }

  export function merge(agg1, agg2) {
   agg1.update(agg2.getSum());
  }

  export function finalize(agg) {
   return agg.getSum();
  }

  export function serialize(agg) {
   return {sum: agg.getSum()};
  }

  export function deserialize(serialized) {
   var agg = new SumAggregator();
   agg.update(serialized.sum);
   return agg;
  }

''';

SELECT F(x) AS results FROM UNNEST([1,2,3,4]) AS x;

/*-----------------*
 | results         |
 +-----------------+
 | 10.0            |
 *-----------------*/
```

如要進一步瞭解序列化函式，請參閱[選用的 JavaScript 序列化函式](#javascript-serialization-functions)。

### 在 JavaScript UDAF 中加入全域變數和自訂函式

JavaScript 函式主體可以包含自訂 JavaScript 程式碼，例如 JavaScript 全域變數和自訂函式。

JavaScript 載入 BigQuery 時，系統會執行全域變數，然後再執行 `initialState` 函式。如果您需要執行一次性的初始化作業，且不應針對每個匯總群組重複執行，則全域變數可能很有用，就像 `initialState`、`aggregate`、`merge` 和 `finalize` 函式的情況一樣。

請勿使用全域變數儲存匯總狀態。請改為將匯總狀態限制為傳遞至匯出函式的物件。請只使用全域變數，快取不屬於任何特定匯總作業的昂貴作業。

在下列查詢中，`SumOfPrimes` 函式會計算總和，但只有質數會納入計算。在 JavaScript 函式主體中，有兩個全域變數 `primes` 和 `maxTested`，會先初始化。此外，還有一個名為 `isPrime` 的自訂函式，可檢查數字是否為質數。

```
CREATE TEMP AGGREGATE FUNCTION SumOfPrimes(x INT64)
RETURNS INT64
LANGUAGE js
AS r'''

  var primes = new Set([2]);
  var maxTested = 2;

  function isPrime(n) {
    if (primes.has(n)) {
      return true;
    }
    if (n <= maxTested) {
      return false;
    }
    for (var k = 2; k < n; ++k) {
      if (!isPrime(k)) {
        continue;
      }
      if ((n % k) == 0) {
        maxTested = n;
        return false;
      }
    }
    maxTested = n;
    primes.add(n);
    return true;
  }

  export function initialState() {
    return {sum: 0};
  }

  export function aggregate(state, x) {
    x = Number(x);
    if (isPrime(x)) {
      state.sum += x;
    }
  }

  export function merge(state, partialState) {
    state.sum += partialState.sum;
  }

  export function finalize(state) {
    return state.sum;
  }

''';

-- Call the JavaScript UDAF.
WITH numbers AS (
  SELECT * FROM UNNEST([10, 11, 13, 17, 19, 20]) AS x)
SELECT SumOfPrimes(x) AS sum FROM numbers;

/*-----*
 | sum |
 +-----+
 | 60  |
 *-----*/
```

### 加入 JavaScript 程式庫

您可以使用 `OPTIONS` 子句中的 `library` 選項，擴充 JavaScript UDAF。這個選項可讓您為 JavaScript UDAF 指定外部程式碼資料庫，然後使用 `import` 宣告匯入這些程式庫。

在下列範例中，`bar.js` 中的程式碼可供 JavaScript UDAF 函式主體中的任何程式碼使用：

```
CREATE TEMP AGGREGATE FUNCTION JsAggFn(x FLOAT64)
RETURNS FLOAT64
LANGUAGE js
OPTIONS (library = ['gs://foo/bar.js'])
AS r'''

  import doInterestingStuff from 'bar.js';

  export function initialState() {
    return ...
  }
  export function aggregate(state, x) {
    var result = doInterestingStuff(x);
    ...
  }
  export function merge(state, partial_state) {
    ...
  }
  export function finalize(state) {
    return ...;
  }

''';
```

### 必要的 JavaScript 結構

與 JavaScript UDF 不同，JavaScript UDF 的函式主體是自由形式的 JavaScript，會針對每個資料列執行，而 JavaScript UDAF 的函式主體是 JavaScript 模組，內含一些內建的匯出函式，會在匯總程序的各個階段叫用。部分內建函式為必要函式，其餘則為選用函式。您也可以新增 JavaScript 函式。

#### 必要的 JavaScript 匯總函式

您可以加入 JavaScript 函式，但 JavaScript 函式主體必須包含下列可匯出的 JavaScript 函式：

* `initialState([nonAggregateParam])`：傳回 JavaScript 物件，代表尚未匯總任何資料列的匯總狀態。
* `aggregate(state, aggregateParam[, ...][, nonAggregateParam])`：匯總一列資料，更新狀態以儲存匯總結果。不會傳回值。
* `merge(state, partialState, [nonAggregateParam])`：將匯總狀態 `partialState` 合併至匯總狀態 `state`。當引擎平行彙整不同部分的資料，且需要合併結果時，就會使用這個函式。不會傳回值。
* `finalize(finalState, [nonAggregateParam])`：根據最終匯總狀態 `finalState`，傳回匯總函式的最終結果。

如要進一步瞭解必要函式，請參閱「[JavaScript UDAF 中的必要函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#javascript-interface-functions-udaf)」。

#### 選用的 JavaScript 序列化函式

如要使用無法序列化的匯總狀態，JavaScript UDAF 必須提供 `serialize` 和 `deserialize` 函式。`serialize` 函式會將匯總狀態轉換為可序列化為 BigQuery 的物件；`deserialize` 函式則會將可序列化為 BigQuery 的物件轉換回匯總狀態。

* `serialize(state)`：傳回可序列化的物件，其中包含匯總狀態的資訊，可透過 `deserialize` 函式還原序列化。
* `deserialize(serializedState)`：將 `serializedState` (先前由 `serialize` 函式序列化) 還原序列化為可傳遞至 `serialize`、`aggregate`、`merge` 或 `finalize` 函式的匯總狀態。

如要進一步瞭解內建的 JavaScript 序列化函式，請參閱「[JavaScript UDAF 的序列化函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#javascript-serialization-functions-udaf)」。

如要瞭解如何使用 JavaScript UDAF 序列化及還原序列化資料，請參閱「[在 JavaScript UDAF 中序列化及還原序列化資料](#serialize-javascript-udaf)」。

### JavaScript UDAF 中允許的 SQL 類型編碼

在 JavaScript UDAF 中，下列支援的 [GoogleSQL 資料類型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw)會以如下方式表示 [JavaScript 資料類型](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects)：

| GoogleSQL  資料類型 | JavaScript  資料類型 | 附註 |
| --- | --- | --- |
| `ARRAY` | `Array` | 不支援陣列的陣列。如要突破這項限制，請使用 `Array<Object<Array>>` (JavaScript) 和 `ARRAY<STRUCT<ARRAY>>` (GoogleSQL) 資料類型。 |
| `BIGNUMERIC` | `Number` 或 `String` | 與 `NUMERIC` 相同。 |
| `BOOL` | `Boolean` |  |
| `BYTES` | `Uint8Array` |  |
| `DATE` | `Date` |  |
| `FLOAT64` | `Number` |  |
| `INT64` | `BigInt` |  |
| `JSON` | 各種類型 | GoogleSQL `JSON` 資料類型可以轉換為 JavaScript `Object`、`Array` 或其他 GoogleSQL 支援的 JavaScript 資料類型。 |
| `NUMERIC` | `Number` 或 `String` | 如果 `NUMERIC` 值能夠以 [IEEE 754 浮點](https://en.wikipedia.org/wiki/Floating-point_arithmetic#IEEE_754:_floating_point_in_modern_computers)值準確表示 (範圍 `[-253, 253]`)，且沒有任何小數部分，則可以當成 `Number` 資料類型加以編碼，否則會編碼為 `String` 資料類型。 |
| `STRING` | `String` |  |
| `STRUCT` | `Object` | 每個 `STRUCT` 欄位都是 `Object` 資料類型中的具名屬性。系統不支援未命名的 `STRUCT` 欄位。 |
| `TIMESTAMP` | `Date` | `Date` 包含微秒欄位，其中含有 `TIMESTAMP` 的微秒部分。 |

**注意：** JavaScript UDAF 的 SQL 編碼與 JavaScript UDF 的不同。

## 呼叫 UDAF

本節說明在 BigQuery 中建立持續性或暫時性 UDAF 後，可以呼叫該 UDAF 的各種方式。

**注意：** JavaScript UDAF 呼叫不支援 `ORDER BY` 子句。

### 呼叫永久 UDAF

呼叫永久 UDAF 的方式與呼叫內建匯總函式相同。詳情請參閱「[匯總函式呼叫](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/aggregate-function-calls?hl=zh-tw)」。您必須在函式路徑中加入資料集。

在下列範例中，查詢會呼叫名為 `WeightedAverage` 的永久 UDAF：

```
SELECT my_project.my_dataset.WeightedAverage(item, weight, 2) AS weighted_average
FROM (
  SELECT 1 AS item, 2.45 AS weight UNION ALL
  SELECT 3 AS item, 0.11 AS weight UNION ALL
  SELECT 5 AS item, 7.02 AS weight
);
```

系統會產生下表結果：

```
/*------------------*
 | weighted_average |
 +------------------+
 | 4.5              |
 *------------------*/
```

### 呼叫臨時 UDAF

呼叫暫時性 UDAF 的方式與呼叫內建匯總函式相同。詳情請參閱「[匯總函式呼叫](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/aggregate-function-calls?hl=zh-tw)」。

臨時函式必須包含在含有 UDAF 函式呼叫的[多重陳述式查詢](https://docs.cloud.google.com/bigquery/docs/multi-statement-queries?hl=zh-tw)或[程序](https://docs.cloud.google.com/bigquery/docs/procedures?hl=zh-tw)中。

在以下範例中，查詢會呼叫名為 `WeightedAverage` 的暫時性 UDAF：

```
CREATE TEMP AGGREGATE FUNCTION WeightedAverage(...)

-- Temporary UDAF function call
SELECT WeightedAverage(item, weight, 2) AS weighted_average
FROM (
  SELECT 1 AS item, 2.45 AS weight UNION ALL
  SELECT 3 AS item, 0.11 AS weight UNION ALL
  SELECT 5 AS item, 7.02 AS weight
);
```

系統會產生下表結果：

```
/*------------------*
 | weighted_average |
 +------------------+
 | 4.5              |
 *------------------*/
```

### 忽略或納入含有 `NULL` 值的資料列

使用 `IGNORE NULLS` 引數呼叫 JavaScript UDAF 時，BigQuery 會自動略過任何匯總引數評估為 `NULL` 的資料列。這類資料列會完全排除在匯總作業之外，且不會傳遞至 JavaScript `aggregate` 函式。提供 `RESPECT NULLS` 引數時，系統會停用 `NULL` 篩選，並將每個資料列傳遞至 JavaScript UDAF，不論 `NULL` 值為何。

如果未提供 `IGNORE NULLS` 和 `RESPECT NULLS` 引數，預設引數為 `IGNORE NULLS`。

以下範例說明預設的 `NULL` 行為、`IGNORE NULLS` 行為和 `RESPECT NULLS` 行為：

```
CREATE TEMP AGGREGATE FUNCTION SumPositive(x FLOAT64)
RETURNS FLOAT64
LANGUAGE js
AS r'''

  export function initialState() {
    return {sum: 0}
  }
  export function aggregate(state, x) {
    if (x == null) {
      // Use 1000 instead of 0 as placeholder for null so
      // that NULL values passed are visible in the result.
      state.sum += 1000;
      return;
    }
    if (x > 0) {
      state.sum += x;
    }
  }
  export function merge(state, partialState) {
    state.sum += partialState.sum;
  }
  export function finalize(state) {
    return state.sum;
  }

''';

-- Call the JavaScript UDAF.
WITH numbers AS (
  SELECT * FROM UNNEST([1.0, 2.0, NULL]) AS x)
SELECT
  SumPositive(x) AS sum,
  SumPositive(x IGNORE NULLS) AS sum_ignore_nulls,
  SumPositive(x RESPECT NULLS) AS sum_respect_nulls
FROM numbers;

/*-----+------------------+-------------------*
 | sum | sum_ignore_nulls | sum_respect_nulls |
 +-----+------------------+-------------------+
 | 3.0 | 3.0              | 1003.0            |
 *-----+------------------+-------------------*/
```

## 刪除 UDAF

本節說明在 BigQuery 中建立永久或暫時 UDAF 後，可以透過哪些方式刪除。

### 刪除永久 UDAF

如要刪除永久性 UDAF，請使用 [`DROP FUNCTION` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#drop_function_statement)。您必須在函式路徑中加入資料集。

在下列範例中，查詢會刪除名為 `WeightedAverage` 的永久性 UDAF：

```
DROP FUNCTION IF EXISTS my_project.my_dataset.WeightedAverage;
```

### 刪除暫時性 UDAF

如要刪除暫時性 UDAF，請使用 [`DROP FUNCTION` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#drop_function_statement)。

在下列範例中，查詢會刪除名為 `WeightedAverage` 的暫時性 UDAF：

```
DROP FUNCTION IF EXISTS WeightedAverage;
```

暫時性 UDAF 會在查詢完成時立即失效。除非您想從[多重陳述式查詢](https://docs.cloud.google.com/bigquery/docs/multi-statement-queries?hl=zh-tw)或[程序](https://docs.cloud.google.com/bigquery/docs/procedures?hl=zh-tw)中提早移除 UDAF，否則不需要刪除。

## 列出 UDAF

UDAF 是一種常式。如要列出資料集中的所有常式，請參閱「[列出常式](https://docs.cloud.google.com/bigquery/docs/routines?hl=zh-tw#list_routines)」。

## 效能提示

如要提升查詢效能，請考慮下列事項：

* 預先篩選您的輸入內容。以 JavaScript 處理資料的成本高於 SQL，因此最好先盡可能在 SQL 中篩選輸入內容。

  下列查詢的效率較低，因為它會在 UDAF 呼叫中使用 `x > 0` 篩選輸入內容：

  ```
  SELECT JsFunc(x) FROM t;
  ```

  下列查詢會先使用 `WHERE x > 0` 預先篩選輸入內容，再呼叫 UDAF，因此效率更高：

  ```
  SELECT JsFunc(x) FROM t WHERE x > 0;
  ```
* 盡量使用內建匯總函式，而非 JavaScript。以 JavaScript 重新實作內建匯總函式，會比呼叫執行相同作業的內建匯總函式慢。

  下列查詢實作了 UDAF，因此效率較低：

  ```
  SELECT SumSquare(x) FROM t;
  ```

  下列查詢的效率較高，因為它會實作內建函式，產生與先前查詢相同的結果：

  ```
  SELECT SUM(x*x) FROM t;
  ```
* JavaScript UDAF 適用於較複雜的匯總作業，這類作業無法透過內建函式表示。
* 有效率地使用記憶體。JavaScript 處理環境限制了每個查詢可用的記憶體。如果 JavaScript UDAF 查詢累積過多本機狀態，可能會因記憶體耗盡而失敗。請特別注意盡量縮小匯總狀態物件的大小，並避免匯總狀態累積大量資料列。

  下列查詢效率不彰，因為當處理的資料列數量變多時，`aggregate` 函式會使用無上限的記憶體。

  ```
  export function initialState() {
    return {rows: []};
  }
  export function aggregate(state, x) {
    state.rows.push(x);
  }
  ...
  ```
* 盡可能使用分區資料表。與非分區資料表相比，查詢分區資料表時，JavaScript UDAF 通常會更有效率地執行，因為分區資料表儲存資料時會分成許多較小的檔案，因此可實現更高的平行處理能力。

## 限制

* UDAF 適用與 UDF 相同的限制。詳情請參閱「[UDF 限制](https://docs.cloud.google.com/bigquery/docs/user-defined-functions?hl=zh-tw#limitations)」。
* 只有常值、查詢參數和指令碼變數可以做為 UDAF 的非匯總引數傳入。
* JavaScript UDAF 函式呼叫不支援使用 `ORDER BY` 子句。

  ```
  SELECT MyUdaf(x ORDER BY y) FROM t; -- Error: ORDER BY is unsupported.
  ```

## 定價

系統會按照標準的 [BigQuery 定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw)模式，針對 UDAF 收取費用。

## 配額與限制

UDAF 適用的配額和限制與 UDF 相同。如要瞭解 UDF 配額，請參閱「[配額與限制](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#udf_limits)」。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-16 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-16 (世界標準時間)。"],[],[]]