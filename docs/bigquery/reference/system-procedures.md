Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [參考資料](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 系統程序參考資料

BigQuery 支援下列系統程序，使用方式與使用者建立的[預存程序](https://docs.cloud.google.com/bigquery/docs/procedures?hl=zh-tw)類似。

## BQ.ABORT\_SESSION

**語法**

```
CALL BQ.ABORT_SESSION([session_id]);
```

**說明**

終止目前的工作階段。

您可以選擇指定[工作階段 ID](https://docs.cloud.google.com/bigquery/docs/sessions?hl=zh-tw#get-id)，如果系統程序不是從該工作階段呼叫，您就能終止工作階段。

詳情請參閱「[終止工作階段](https://docs.cloud.google.com/bigquery/docs/sessions?hl=zh-tw#terminate-session)」。

## BQ.JOBS.CANCEL

**語法**

```
CALL BQ.JOBS.CANCEL(job);
```

**說明**

取消正在執行的工作。

以 `'[project_id.]job_id'` 格式將工作指定為字串。如果您從與工作不同的專案執行這項系統程序，則必須加入專案 ID。您必須在與工作相同的位置執行程序。

詳情請參閱「[取消工作](https://docs.cloud.google.com/bigquery/docs/managing-jobs?hl=zh-tw#cancel_jobs)」。

## BQ.CANCEL\_INDEX\_ALTERATION

**語法**

```
CALL BQ.CANCEL_INDEX_ALTERATION(table_name, index_name);
```

**說明**

取消使用者啟動的[向量索引重建作業](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#alter_vector_index_rebuild_statement)。

以字串形式指定資料表名稱，格式為 `'[project_id.]dataset.table'`，並以字串形式指定索引名稱。如果您從與資料表不同的專案執行這項系統程序，則必須加入專案 ID。

您必須在與索引資料表相同的位置執行這項程序。如要設定查詢位置，請參閱「[指定位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw#specify_locations)」。

**範例**

```
CALL BQ.CANCEL_INDEX_ALTERATION('my_project.my_dataset.indexed_table', 'my_index');
```

## BQ.REFRESH\_EXTERNAL\_METADATA\_CACHE

**語法**

```
CALL BQ.REFRESH_EXTERNAL_METADATA_CACHE(table_name [, [subdirectory_uri, …]]);
```

**說明**

重新整理 Google Cloud Lakehouse 資料表或物件資料表的中繼資料快取。
如果對中繼資料快取模式設為 `AUTOMATIC` 的資料表執行這項程序，就會失敗。

如要執行這項系統程序，您需要 `bigquery.tables.update` 和 `bigquery.tables.updateData` 權限。

以字串形式指定資料表名稱，格式為 `'[project_id.]dataset.table'`。如果您從與資料表不同的專案執行這項系統程序，則必須加入專案 ID。

如果是 Lakehouse 資料表，您可以選擇在 Cloud Storage 中，以 `'gs://table_data_directory/subdirectory/.../'` 格式指定資料表資料目錄的一或多個子目錄。這樣一來，您就能只重新整理這些子目錄中的資料表中繼資料，避免不必要的中繼資料處理作業。

**範例**

如要重新整理資料表的所有中繼資料，請按照下列步驟操作：

```
CALL BQ.REFRESH_EXTERNAL_METADATA_CACHE('myproject.test_db.test_table')
```

如要選擇性重新整理 Lakehouse 資料表的中繼資料，請按照下列步驟操作：

```
CALL BQ.REFRESH_EXTERNAL_METADATA_CACHE('myproject.test_db.test_table', ['gs://source/uri/sub/path/d1/*', 'gs://source/uri/sub/path/d2/*'])
```

**限制**

* 如果連結資料集參照外部資料集中的資料表，則不支援重新整理中繼資料快取。
* 中繼資料快取重新整理不應在[多重陳述式交易](https://docs.cloud.google.com/bigquery/docs/transactions?hl=zh-tw)中使用。

## BQ.REFRESH\_MATERIALIZED\_VIEW

**語法**

```
CALL BQ.REFRESH_MATERIALIZED_VIEW(view_name);
```

**說明**

重新整理具體化檢視表。

以字串形式指定 materialized view 的名稱，格式為 `'[project_id.]dataset.table'`。如果您從具體化檢視以外的專案執行這項系統程序，則必須加入專案 ID。

詳情請參閱「[手動重新整理](https://docs.cloud.google.com/bigquery/docs/materialized-views?hl=zh-tw#manual_refresh)」。

## BQ.SHOW\_GRAPH\_EXPAND\_SCHEMA

**語法**

```
CALL BQ.SHOW_GRAPH_EXPAND_SCHEMA(graph_name, output_schema);
```

**說明**

使用透過在 `graph_name` 上呼叫 [`GRAPH_EXPAND` TVF](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/graph-sql-queries?hl=zh-tw#graph_expand)傳回的資料表結構定義，填入您提供的 `output_schema` 變數。

以字串形式指定[圖表](https://docs.cloud.google.com/bigquery/docs/graph-overview?hl=zh-tw)名稱，格式為 `'[project_id.]dataset.graph'`。TVF 傳回的每個資料欄都會在圖表中顯示為屬性。`GRAPH_EXPAND`輸出內容包含每個資料欄的名稱、類型和模式。如果屬性有定義說明或同義字，這些內容會顯示在資料欄的 `description` 欄位中。如果屬性定義了指標，輸出內容就會包含該欄位的 `"is_measure":true`。

**範例**

```
DECLARE schema STRING;
CALL BQ.SHOW_GRAPH_EXPAND_SCHEMA('my_project.my_dataset.my_graph', schema);
SELECT schema;
```

輸出看起來類似以下內容：

```
{
  "fields":[
    {
      "name":"Department_dept_name",
      "type":"STRING",
      "mode":"NULLABLE",
      "description":
        "{\"description\":\"The name of the academic department\",
          \"synonyms\":[\"division\"]}"
    },
    {
      "name":"Department_budget",
      "type":"FLOAT",
      "mode":"NULLABLE"
    },
    {
      "name":"Department_total_budget",
      "type":"FLOAT",
      "mode":"NULLABLE",
      "is_measure":true
    }
  ]
}
```




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-04-22 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-04-22 (世界標準時間)。"],[],[]]