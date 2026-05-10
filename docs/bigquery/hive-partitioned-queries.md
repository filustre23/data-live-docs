Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# Hive 分區資料的外部資料表

您可以使用 BigQuery 外部資料表，查詢下列資料儲存庫中的已分割資料：

* [Cloud Storage](https://docs.cloud.google.com/bigquery/docs/create-cloud-storage-table-biglake?hl=zh-tw#create-biglake-partitioned-data)
* [Amazon Simple Storage Service (Amazon S3)](https://docs.cloud.google.com/bigquery/docs/omni-aws-create-external-table?hl=zh-tw#create-biglake-table-partitioned)
* [Azure Blob 儲存體](https://docs.cloud.google.com/bigquery/docs/omni-azure-create-external-table?hl=zh-tw#create-biglake-table-partitioned)

外部分區資料必須使用[預設 Hive 分區配置](#supported_data_layouts)，且採用下列其中一種格式：

* Avro
* CSV
* JSON
* ORC
* Parquet

如要查詢外部分區資料，您必須建立 [BigLake 資料表](https://docs.cloud.google.com/bigquery/docs/create-cloud-storage-table-biglake?hl=zh-tw)或[外部資料表](https://docs.cloud.google.com/bigquery/docs/external-data-cloud-storage?hl=zh-tw#create-external-table-partitioned)。建議使用 BigLake 資料表，因為這類資料表可讓您在資料表層級強制執行精細的安全防護機制。如要瞭解 BigLake 和外部資料表，請參閱「[BigLake 資料表簡介](https://docs.cloud.google.com/bigquery/docs/biglake-intro?hl=zh-tw)」
和「[外部資料表簡介](https://docs.cloud.google.com/bigquery/docs/external-tables?hl=zh-tw)」。

在[資料表定義檔](https://docs.cloud.google.com/bigquery/docs/external-table-definition?hl=zh-tw#create_a_definition_file_for_hive-partitioned_data)中設定相關選項即可支援 Hive 分區。如需查詢代管分區資料表的操作說明，請參閱[分區資料表簡介](https://docs.cloud.google.com/bigquery/docs/partitioned-tables?hl=zh-tw)。

## 分區結構定義

以下各節說明 [預設的 Hive 分區配置](#supported_data_layouts)，以及 BigQuery 支援的[結構定義偵測模式](#detection_modes)。

為避免讀取不必要的檔案並提升效能，您可以在查詢中[使用分區索引鍵的述詞篩選器](#partition_pruning)。

### 支援的資料配置

查詢 Cloud Storage 中的資料時，Hive 分區索引鍵會顯示為一般資料欄。資料必須符合預設 Hive 分區配置。舉例來說，下列檔案均符合預設配置，鍵/值組合會以目錄型式排列並採用等號 (=) 做為分隔符，而且分區索引鍵的順序一律相同：

```
gs://my_bucket/my_table/dt=2019-10-31/lang=en/my_filename
gs://my_bucket/my_table/dt=2018-10-31/lang=fr/my_filename
```

在本範例中，常見的來源 URI 前置字串為 `gs://my_bucket/my_table`。

### 不支援的資料配置

如果分區索引鍵名稱未編碼入目錄路徑中，系統將無法偵測分區結構定義。舉例來說，分區索引鍵名稱未編碼入下列路徑：

```
gs://my_bucket/my_table/2019-10-31/en/my_filename
```

如果檔案的結構定義順序不一致，系統也無法進行偵測作業。舉例來說，下列兩個檔案採用反向分區索引鍵編碼：

```
gs://my_bucket/my_table/dt=2019-10-31/lang=en/my_filename
gs://my_bucket/my_table/lang=fr/dt=2018-10-31/my_filename
```

### 偵測模式

BigQuery 支援三種 Hive 分區結構定義偵測模式：

* `AUTO`：系統會自動偵測索引鍵名稱與類型。系統可偵測下列類型：

  + [STRING](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#string_type)
  + [INTEGER](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#integer_types)
  + [DATE](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#date_type)

    例如 `/date=2018-10-18/`。
  + [TIMESTAMP](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#timestamp_type)

    例如 `/time=2018-10-18 16:00:00+00/`。
* `STRINGS`：系統會自動將索引鍵名稱轉換為 `STRING` 類型。
* `CUSTOM`：分區索引鍵結構定義會編碼入來源 URI 前置字串。

#### 自訂分區索引鍵結構定義

如要使用 `CUSTOM` 結構定義，必須在來源 URI 前置字串欄位中指定結構定義。使用 `CUSTOM` 結構定義可指定每個分區索引鍵的類型。這些值必須有效地剖析為指定類型，否則查詢作業會失敗。

舉例來說，如果將 `source_uri_prefix` 旗標設為 `gs://my_bucket/my_table/{dt:DATE}/{val:STRING}`，BigQuery 會將 `val` 視為 STRING、將 `dt` 視為 DATE，並將 `gs://my_bucket/my_table` 做為相符檔案的來源 URI 前置字串。

### 分區修剪

BigQuery 會盡可能利用分區索引鍵上的查詢述詞修剪分區。這樣 BigQuery 就能避免讀取不必要的檔案，進而提升效能。

### 查詢中分區鍵的述詞篩選條件

建立外部分區資料表時，只要啟用 [HivePartitioningOptions](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables?hl=zh-tw#hivepartitioningoptions) 下的 `requirePartitionFilter` 選項，即可要求使用分區鍵的述詞篩選器。

啟用此選項後，如嘗試在未指定 `WHERE` 子句的情況下查詢外部分區資料表，將會產生下列錯誤：`Cannot query over table <table_name> without a filter over column(s)
<partition key names> that can be used for partition elimination`。

**注意：**必須至少有一個述詞只參照一或多個分割區鍵，篩選器才符合分割區排除資格。舉例來說，如果檔案中的資料表具有分區鍵 `val` 和資料欄 `f`，下列兩個 `WHERE` 子句都符合需求：
  
    `WHERE val = "key"`
  
    `WHERE val = "key" AND f = "column"`

不過，`WHERE (val = "key" OR f = "column")` 不夠。

## 限制

* 建構 Hive 分區支援時，我們會假設所有 URI 都有一個通用來源 URI 前置字串，字串結尾處緊接在分區編碼之前，如下所示：`gs://BUCKET/PATH_TO_TABLE/`。
* 假設 Hive 分區資料表的目錄結構具有相同的分區索引鍵、索引鍵的顯示順序相同，且每個資料表最多包含十個分區索引鍵。
* 資料必須符合[預設 Hive 分區配置](#supported_data_layouts)。
* Hive 分區索引鍵不得與基礎檔案中的資料欄重疊。
* 僅支援 [GoogleSQL](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw)。
* 查詢儲存在 Cloud Storage 中外部資料來源的所有[限制](https://docs.cloud.google.com/bigquery/external-data-sources?hl=zh-tw#external_data_source_limitations)均適用。

## 後續步驟

* 瞭解[分區資料表](https://docs.cloud.google.com/bigquery/docs/partitioned-tables?hl=zh-tw)。
* 瞭解如何[在 BigQuery 中使用 SQL](https://docs.cloud.google.com/bigquery/docs/introduction-sql?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-09 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-09 (世界標準時間)。"],[],[]]