Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [參考資料](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 舊版 SQL 中的使用者定義函式

本文件詳述，如何在舊版 SQL 查詢語法中使用 JavaScript 使用者定義函式。建議在 BigQuery 中使用[GoogleSQL 語法](https://docs.cloud.google.com/bigquery/docs/user-defined-functions?hl=zh-tw)，建立使用者定義函式。詳情請參閱[舊版 SQL 功能適用情形](https://docs.cloud.google.com/bigquery/docs/legacy-sql-feature-availability?hl=zh-tw)。

BigQuery 的舊版 SQL 支援以 JavaScript 編寫的使用者定義函式 (UDF)。UDF 與 MapReduce 中的「Map」函式類似，也就是把單一資料列當做輸入內容，然後產生至少零個資料列來做為輸出內容。輸出內容的結構定義可能會和輸入內容的不同。

如要瞭解 GoogleSQL 中的使用者定義函式，請參閱[GoogleSQL 的使用者定義函式](https://docs.cloud.google.com/bigquery/sql-reference/user-defined-functions?hl=zh-tw)。

## UDF 範例

```
// UDF definition
function urlDecode(row, emit) {
  emit({title: decodeHelper(row.title),
        requests: row.num_requests});
}

// Helper function with error handling
function decodeHelper(s) {
  try {
    return decodeURI(s);
  } catch (ex) {
    return s;
  }
}

// UDF registration
bigquery.defineFunction(
  'urlDecode',  // Name used to call the function from SQL

  ['title', 'num_requests'],  // Input column names

  // JSON representation of the output schema
  [{name: 'title', type: 'string'},
   {name: 'requests', type: 'integer'}],

  urlDecode  // The function reference
);
```

[返回頁首](#top)

## UDF 結構

```
function name(row, emit) {
  emit(<output data>);
}
```

BigQuery UDF 會在資料表的個別列或 subselect 查詢結果上執行。UDF 有兩種形式參數：

* `row`：輸入列。
* `emit`：BigQuery 用來收集輸出資料的掛鉤。`emit`emit 函式採用一種參數，也就是代表輸出資料中單一資料列的 JavaScript 物件。您可以多次呼叫 `emit` 函式 (例如在迴圈中)，以便輸出多列資料。

以下程式碼範例顯示基本 UDF。

```
function urlDecode(row, emit) {
  emit({title: decodeURI(row.title),
        requests: row.num_requests});
}
```

### 註冊 UDF

您必須為自己的函式註冊名稱，好讓您可以從 BigQuery SQL 叫用該函式。您註冊的名稱不需要與該函式在 JavaScript 中使用的名稱相同。

```
bigquery.defineFunction(
  '<UDF name>',  // Name used to call the function from SQL

  ['<col1>', '<col2>'],  // Input column names

  // JSON representation of the output schema
  [<output schema>],

  // UDF definition or reference
  <UDF definition or reference>
);
```

#### 輸入資料欄

輸入資料欄名稱必須符合輸入資料表或子查詢中資料欄的名稱 (或別名，如果適用)。

對於屬於記錄的輸入資料欄，您必須在輸入資料欄清單中指定要從該記錄存取的分葉欄位。

舉例來說，如果您有一筆記錄儲存了某人的姓名和年齡：

```
person RECORD REPEATED
  name STRING OPTIONAL
  age INTEGER OPTIONAL
```

姓名和年齡的輸入指定碼會是：

```
['person.name', 'person.age']
```

如果您在使用 `['person']` 時沒有搭配姓名或年齡，就會產生錯誤。

產生的輸出內容會與結構定義相符；您會得到 JavaScript 物件陣列，其中每個物件都有「name」和「age」屬性。例如：

```
[ {name: 'alice', age: 23}, {name: 'bob', age: 64}, ... ]
```

#### 輸出內容的結構定義

您必須將 UDF 所產生記錄的結構定義或結構，以 JSON 表示法提供給 BigQuery。結構定義可以包含[任何受支援的 BigQuery 資料類型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw)，包括巢狀結構記錄。支援的類型指定碼如下：

* 布林值
* 浮動值
* 整數
* 記錄
* 字串
* 時間戳記

以下程式碼範例顯示輸出結構定義中的記錄語法。每個輸出欄位都需要 `name` 和 `type` 屬性。巢狀結構欄位也必須包含 `fields` 屬性。

```
[{name: 'foo_bar', type: 'record', fields:
  [{name: 'a', type: 'string'},
   {name: 'b', type: 'integer'},
   {name: 'c', type: 'boolean'}]
}]
```

每個欄位都能包含選用的 `mode` 屬性，且該屬性支援下列的值：

* nullable：預設值，可以省略。
* required：如果指定此值，則指定的欄位必須設為某個值。
* repeated：如果指定這個值，則指定的欄位必須是陣列。

傳遞到 `emit()` 函式的資料列，必須與輸出結構定義的資料類型相符。如果您在 emit 函式中忽略了輸出結構定義中的某些欄位，這些欄位會以空值輸出。

#### UDF 定義或參照

如有需要，您可以直接在 `bigquery.defineFunction` 中定義 UDF。例如：

```
bigquery.defineFunction(
  'urlDecode',  // Name used to call the function from SQL

  ['title', 'num_requests'],  // Input column names

  // JSON representation of the output schema
  [{name: 'title', type: 'string'},
   {name: 'requests', type: 'integer'}],

  // The UDF
  function(row, emit) {
    emit({title: decodeURI(row.title),
          requests: row.num_requests});
  }
);
```

否則，您可以個別定義 UDF，然後在 `bigquery.defineFunction` 中傳遞該函式的參照。例如：

```
// The UDF
function urlDecode(row, emit) {
  emit({title: decodeURI(row.title),
        requests: row.num_requests});
}

// UDF registration
bigquery.defineFunction(
  'urlDecode',  // Name used to call the function from SQL

  ['title', 'num_requests'],  // Input column names

  // JSON representation of the output schema
  [{name: 'title', type: 'string'},
   {name: 'requests', type: 'integer'}],

  urlDecode  // The function reference
);
```

#### 處理錯誤

如果系統在處理 UDF 的過程中擲回例外狀況或錯誤，整個查詢作業將會失敗。您可以使用 try-catch 區塊來處理錯誤。例如：

```
// The UDF
function urlDecode(row, emit) {
  emit({title: decodeHelper(row.title),
        requests: row.num_requests});
}

// Helper function with error handling
function decodeHelper(s) {
  try {
    return decodeURI(s);
  } catch (ex) {
    return s;
  }
}

// UDF registration
bigquery.defineFunction(
  'urlDecode',  // Name used to call the function from SQL

  ['title', 'num_requests'],  // Input column names

  // JSON representation of the output schema
  [{name: 'title', type: 'string'},
   {name: 'requests', type: 'integer'}],

  urlDecode  // The function reference
);
```



## 使用 UDF 執行查詢

您可以使用 [bq 指令列工具](#command-line)或 [BigQuery API](#api)，在舊版 SQL 中使用 UDF。[Google Cloud 控制台](https://docs.cloud.google.com/bigquery/docs/bigquery-web-ui?hl=zh-tw)不支援舊版 SQL 中的 UDF。

### 使用 bq 指令列工具

如要執行含有一或多個 UDF 的查詢，請在 Google Cloud CLI 的 bq 指令列工具中指定 `--udf_resource` 標記。該旗標的值可以是 Cloud Storage (`gs://...`) URI，或是本機檔案的路徑。如要指定多個 UDF 資源檔，請重複使用這個旗標。

使用以下語法來利用 UDF 執行查詢：

```
bq query --udf_resource=<file_path_or_URI> <sql_query>
```

以下範例執行的查詢會使用儲存在本機檔案的 UDF，以及同樣也是儲存在本機檔案中的 SQL 查詢。

#### 建立 UDF

您可以把 UDF 儲存在 Cloud Storage，或是儲存為本機文字檔。舉例來說，如要儲存下列 `urlDecode` UDF，請建立名為 `urldecode.js` 的檔案，並把下列 JavaScript 程式碼貼到該檔案中，然後儲存檔案。

```
// UDF definition
function urlDecode(row, emit) {
  emit({title: decodeHelper(row.title),
        requests: row.num_requests});
}

// Helper function with error handling
function decodeHelper(s) {
  try {
    return decodeURI(s);
  } catch (ex) {
    return s;
  }
}

// UDF registration
bigquery.defineFunction(
  'urlDecode',  // Name used to call the function from SQL

  ['title', 'num_requests'],  // Input column names

  // JSON representation of the output schema
  [{name: 'title', type: 'string'},
   {name: 'requests', type: 'integer'}],

  urlDecode  // The function reference
);
```

#### 建立查詢

您也可以把查詢儲存在檔案中，好讓指令列不會變得太冗長。舉例來說，您可以建立名稱為 `query.sql` 的本機檔案，然後將下列 BigQuery 陳述式貼到該檔案中。

```
#legacySQL
SELECT requests, title
```