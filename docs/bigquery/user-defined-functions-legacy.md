Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

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
FROM
  urlDecode(
    SELECT
      title, sum(requests) AS num_requests
    FROM
      [my-project:wikipedia.pagecounts_201504]
    WHERE language = 'fr'
    GROUP EACH BY title
  )
WHERE title LIKE '%ç%'
ORDER BY requests DESC
LIMIT 100
```

當您儲存檔案之後，就可以在指令列參照這個檔案。

#### 執行查詢

當您分別在不同的檔案中定義 UDF 和查詢之後，就可以在指令列中參照這些檔案。舉例來說，以下指令會執行您以 `query.sql` 檔名儲存的查詢，並參照您之前建立的 UDF。

```
$ bq query --udf_resource=urldecode.js "$(cat query.sql)"
```

### 使用 BigQuery API

#### configuration.query

使用 UDF 的查詢，必須包含要在查詢中使用的 [`userDefinedFunctionResources`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables?hl=zh-tw#userdefinedfunctionresource) 元素，而這個元素會提供程式碼或程式碼資源所在位置。該元素提供的程式碼，必須包含查詢所參照的所有 UDF 的註冊函式叫用。

#### 程式碼資源

查詢設定可以包含 JavaScript 程式碼 blob，以及儲存在 Cloud Storage 中 JavaScript 來源檔的參照。

系統會在 `userDefinedFunctionResource` 元素的 [`inlineCode`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables?hl=zh-tw#UserDefinedFunctionResource.FIELDS.inline_code) 區段中，填入內嵌 JavaScript 程式碼 blob。不過，如要在多個查詢中重複使用或參照程式碼，您應該將該程式碼保存在 Cloud Storage，並當成外部資源來參照。

如要參照 Cloud Storage 中的 JavaScript 來源檔，請將 `userDefinedFunctionResource` 元素的 [`resourceURI`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables?hl=zh-tw#UserDefinedFunctionResource.FIELDS.resource_uri) 區段設定成該檔案的 `gs://` URI。

查詢設定可包含多個 `userDefinedFunctionResource` 元素，每個元素都可以含有 `inlineCode` 或 `resourceUri` 區段。

#### 範例

以下 JSON 範例說明參照兩個 UDF 資源的查詢要求，其中一個資源是內嵌程式碼的 blob，另一個則是要從 Cloud Storage 讀取的 `lib.js` 檔案。在本範例中，`myFunc` 和 `myFunc` 的註冊叫用是由 `lib.js` 提供的。

```
{
  "configuration": {
    "query": {
      "userDefinedFunctionResources": [
        {
          "inlineCode": "var someCode = 'here';"
        },
        {
          "resourceUri": "gs://some-bucket/js/lib.js"
        }
      ],
      "query": "select a from myFunc(T);"
    }
  }
}
```

[返回頁首](#top)

## 最佳做法

#### 開發您的 UDF

您可以使用[我們的 UDF 測試工具](https://github.com/GoogleCloudPlatform/bigquery-udf-test-tool)來測試 UDF 並進行偵錯，BigQuery 不會為此向您收費。

#### 預先篩選您的輸入內容

如果輸入內容在傳遞到 UDF 之前，能夠輕易地進行篩選，您查詢的執行速度可能會更快，費用也可能會更便宜。

在[執行查詢](https://docs.cloud.google.com/bigquery/user-defined-functions?hl=zh-tw#queryui)小節的範例中，系統將子查詢當做輸入內容傳遞到 `urlDecode`，而不是傳遞整個資料表。資料表可能有多達數十億列，如果我們針對整份資料表執行 UDF，JavaScript 架構必須處理的資料列數量，會是針對篩選後的子查詢執行 UDF 時所需處理的資料列數量的數倍。

#### 避免永久的可變動狀態

請勿在不同的 UDF 呼叫之間儲存或存取可變動的狀態。以下程式碼範例將說明這個情境：

```
// myCode.js
var numRows = 0;

function dontDoThis(r, emit) {
  emit({rowCount: ++numRows});
}

// The query.
SELECT max(rowCount) FROM dontDoThis(t);
```

上述範例不會如預期般運作，因為 BigQuery 會將查詢分割到許多節點。每個節點都有獨立的 JavaScript 處理環境，而這環境會累積不同的 `numRows` 值。

#### 有效率地使用記憶體

JavaScript 處理環境限制了每個查詢可用的記憶體。累積太多本機狀態的 UDF 查詢可能會因記憶體耗盡而失敗。

#### 展開 select 查詢

您必須明確列出要從 UDF 中選取的資料欄。系統並不支援 `SELECT * FROM <UDF name>(...)`。

如要檢查輸入列資料的結構，請使用 `JSON.stringify()` 來發出字串輸出欄：

```
bigquery.defineFunction(
  'examineInputFormat',
  ['some', 'input', 'columns'],
  [{name: 'input', type: 'string'}],
  function(r, emit) {
    emit({input: JSON.stringify(r)});
  }
);
```

[返回頁首](#top)

## 限制

* 處理單一資料列時，您的 UDF 輸出的資料量應該約在 5 MB 以內。
* 每個使用者僅限同時在特定專案中執行約 6 個 UDF 查詢。如果您收到的錯誤說明您已超出[並行查詢限制](https://docs.cloud.google.com/bigquery/quota-policy?hl=zh-tw#queries)，請稍待片刻，然後再試一次。
* UDF 可能會逾時，造成查詢無法完成。逾時可能只有短短 5 分鐘，但可能因多種因素而異，包括您的函式佔用多少使用者 CPU 作業時間，以及 JS 函式的輸入和輸出有多大。
* 查詢工作最多可以有 50 個 UDF 資源 (內嵌程式碼 blob 或外部檔案)。
* 每個內嵌程式碼 blob 的大小上限為 32 KB。如要使用更大的程式碼資源，請將程式碼儲存在 Cloud Storage，然後將它當成外部資源來參照。
* 每個外部程式碼資源的大小上限為 1 MB。
* 所有外部程式碼資源的累積大小上限為 5 MB。

[返回頁首](#top)

## 限制

* 系統不支援 `Window`、`Document` 和 `Node` 等 DOM 物件，以及需要使用這些物件的函式。
* 系統不支援必須使用原生程式碼的 JavaScript 函式。
* JavaScript 中的位元作業僅處理最重要的 32 位元。
* 叫用使用者定義函式的查詢由於具有非確定性本質，因此無法使用快取結果。

[返回頁首](#top)




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-06 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-06 (世界標準時間)。"],[],[]]