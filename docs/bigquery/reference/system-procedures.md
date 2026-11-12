Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

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

您可以視需要指定[工作階段 ID](https://docs.cloud.google.com/bigquery/docs/sessions?hl=zh-tw#get-id)，以便在系統程序並非從該工作階段呼叫時，終止工作階段。

詳情請參閱「[終止工作階段](https://docs.cloud.google.com/bigquery/docs/sessions?hl=zh-tw#terminate-session)」。

## BQ.JOBS.CANCEL

**語法**

```
CALL BQ.JOBS.CANCEL(job);
```

**說明**

取消正在執行的工作。

以 `'[project_id.]job_id'` 格式的字串指定工作。如果您從與工作不同的專案執行這項系統程序，則必須提供專案 ID。您必須在工作所在位置執行程序。

詳情請參閱「[取消工作](https://docs.cloud.google.com/bigquery/docs/managing-jobs?hl=zh-tw#cancel_jobs)」。

## BQ.CANCEL\_INDEX\_ALTERATION

**預覽**

這項功能適用《[服務專屬條款](https://docs.cloud.google.com/terms/service-terms?hl=zh-tw#1)》中「一般服務條款」一節的《正式發布前產品條款》。正式發布前功能是依「原樣」提供，支援服務可能受限。
詳情請參閱[推出階段說明](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages)。

**語法**

```
CALL BQ.CANCEL_INDEX_ALTERATION(table_name, index_name);
```

**說明**

取消使用者發起的[搜尋索引變更](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#alter_search_index_statement)或[向量索引重建](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#alter_vector_index_rebuild_statement)。

以字串形式指定資料表名稱，格式為 `'[project_id.]dataset.table'`，並以字串形式指定索引名稱。如果您從與資料表不同的專案執行這項系統程序，則必須加入專案 ID。

您必須在索引資料表所在的位置執行這項程序。如要設定查詢位置，請參閱「[指定位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw#specify_locations)」。

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

重新整理 BigLake 資料表或物件資料表的中繼資料快取。如果對中繼資料快取模式設為 `AUTOMATIC` 的資料表執行這項程序，程序會失敗。

如要執行這項系統程序，您必須具備 `bigquery.tables.update` 和 `bigquery.tables.updateData` 權限。

請以 `'[project_id.]dataset.table'` 格式的字串指定資料表名稱。如果您從與資料表不同的專案執行這項系統程序，則必須加入專案 ID。

如果是 BigLake 資料表，您可以選擇在 Cloud Storage 中，以 `'gs://table_data_directory/subdirectory/.../'` 格式指定資料表資料目錄的一或多個子目錄。如要讓選擇性重新整理功能正常運作，Cloud Storage 路徑參數必須包含特定路徑或萬用字元。詳情請參閱「[Cloud Storage URI 的萬用字元支援](https://docs.cloud.google.com/bigquery/docs/external-data-cloud-storage?hl=zh-tw#wildcard-support)」。這樣一來，您只需重新整理這些子目錄中的資料表中繼資料，避免不必要的中繼資料處理作業。

**範例**

如要重新整理資料表的所有中繼資料，請按照下列步驟操作：

```
CALL BQ.REFRESH_EXTERNAL_METADATA_CACHE('myproject.test_db.test_table')
```

如要選擇性重新整理 BigLake 資料表的中繼資料，請按照下列步驟操作：

```
CALL BQ.REFRESH_EXTERNAL_METADATA_CACHE('myproject.test_db.test_table', ['gs://source/uri/sub/path/d1/*', 'gs://source/uri/sub/path/d2/*'])
```

**限制**

* 如果資料表是由連結資料集透過外部資料集參照，則不支援中繼資料快取重新整理功能。
* 中繼資料快取重新整理不應在[多重陳述式交易](https://docs.cloud.google.com/bigquery/docs/transactions?hl=zh-tw)中使用。

## BQ.REFRESH\_MATERIALIZED\_VIEW

**語法**

```
CALL BQ.REFRESH_MATERIALIZED_VIEW(view_name);
```

**說明**

重新整理 materialized view。

以 `'[project_id.]dataset.table'` 格式的字串指定 materialized view 的名稱。如果從與 materialized view 不同的專案執行這項系統程序，則必須加入專案 ID。

詳情請參閱「[手動重新整理](https://docs.cloud.google.com/bigquery/docs/materialized-views?hl=zh-tw#manual_refresh)」。

## BQ.SHOW\_GRAPH\_EXPAND\_SCHEMA

**語法**

```
CALL BQ.SHOW_GRAPH_EXPAND_SCHEMA(
  graph_name
  [, start_node [, flatten_results] ]
  , output_schema);
```

**說明**

在 `graph_name` 上呼叫 [`GRAPH_EXPAND` TVF](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/graph-sql-queries?hl=zh-tw#graph_expand)，並以傳回的資料表結構定義填入您提供的 `output_schema` 變數。

`GRAPH_EXPAND` TVF 傳回的每個資料欄都會在圖表中顯示為屬性。輸出內容包含各欄的名稱、類型和模式。如果屬性有定義說明或同義詞，這些資訊會顯示在資料欄的 `description` 欄位中。如果屬性定義了[測量指標](https://docs.cloud.google.com/bigquery/docs/graph-measures?hl=zh-tw)，輸出內容就會包含該欄位的 `"is_measure":true`。

* `graph_name`：`STRING`，包含[圖表](https://docs.cloud.google.com/bigquery/docs/graph-overview?hl=zh-tw)名稱，格式為 `'[project_id.]dataset.graph'`。
* `start_node`：選用的 `STRING`，指定周遊的起始節點名稱。如果圖表有多個根節點資料表，則必須提供這個引數。
* `flatten_results`：選用的 `BOOL` 值，表示如何建構輸出結構定義：
  + `TRUE`：將所有節點和邊緣屬性扁平化，成為 `<element>_<property>` 格式的頂層資料欄。預設值為 `TRUE`。
  + `FALSE`：將根節點屬性傳回為不含前置字元的頂層資料欄，並將彙整的鄰近資料表傳回為 `STRUCT` 資料欄。

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

上次更新時間：2026-11-11 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-11-11 (世界標準時間)。"],[],[]]