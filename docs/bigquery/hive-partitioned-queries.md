Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 管理外部 Hive 分區資料

Hive 分區支援功能可讓您使用 BigLake 資料表或 BigQuery 外部資料表，查詢 Cloud Storage、Amazon Simple Storage Service (Amazon S3) 和 Azure Blob Storage 中的外部資料。當查詢依分區索引鍵篩選時，BigQuery 可以剪除分區並讀取較少資料。

本文說明支援的 Hive 分區版面配置和格式、分區剪除和限制。建議使用 BigLake 資料表，因為這類資料表可讓您在資料表層級強制執行精細的安全防護機制。

## 支援的資料儲存庫和格式

您可以使用 BigQuery 外部資料表，查詢下列資料儲存庫中的分區資料：

* [Cloud Storage](https://docs.cloud.google.com/bigquery/docs/create-cloud-storage-table-biglake?hl=zh-tw#create-biglake-partitioned-data)
* [Amazon Simple Storage Service (Amazon S3)](https://docs.cloud.google.com/bigquery/docs/omni-aws-create-external-table?hl=zh-tw#create-biglake-table-partitioned)
* [Azure Blob 儲存體](https://docs.cloud.google.com/bigquery/docs/omni-azure-create-external-table?hl=zh-tw#create-biglake-table-partitioned)

外部分區資料必須使用[預設 Hive 分區版面配置](#supported_data_layouts)，並採用下列其中一種格式：

* Avro
* CSV
* JSON
* ORC
* Parquet

如要查詢外部分區資料，您必須建立 [BigLake 資料表](https://docs.cloud.google.com/bigquery/docs/create-cloud-storage-table-biglake?hl=zh-tw)或[外部資料表](https://docs.cloud.google.com/bigquery/docs/external-data-cloud-storage?hl=zh-tw#create-external-table-partitioned)。如要瞭解 BigLake 和外部資料表，請參閱「[BigLake 資料表簡介](https://docs.cloud.google.com/bigquery/docs/biglake-intro?hl=zh-tw)」和「[外部資料表簡介](https://docs.cloud.google.com/bigquery/docs/external-tables?hl=zh-tw)」。

如要啟用 Hive 分區支援，請在[資料表定義檔案](https://docs.cloud.google.com/bigquery/docs/external-table-definition?hl=zh-tw#create_a_definition_file_for_hive-partitioned_data)中設定適當選項。如需查詢代管分區資料表的操作說明，請參閱「[分區資料表簡介](https://docs.cloud.google.com/bigquery/docs/partitioned-tables?hl=zh-tw)」。

## 分區結構定義

以下各節將說明 BigQuery 支援的[預設 Hive 分區版面配置](#supported_data_layouts)和[結構定義偵測模式](#detection_modes)。

為避免讀取不必要的檔案並提升效能，您可以在[查詢中對分區索引鍵使用述詞篩選器](#partition_pruning)。

### 支援的資料配置

從 Cloud Storage 查詢資料時，Hive 分區索引鍵會顯示為一般資料欄。資料必須採用預設的 Hive 分區版面配置。舉例來說，下列檔案採用預設版面配置，鍵/值組合設為目錄，並以等號 (=) 做為分隔符號，且分區鍵一律按照相同順序排列：

```
gs://my_bucket/my_table/dt=2019-10-31/lang=en/my_filename
gs://my_bucket/my_table/dt=2018-10-31/lang=fr/my_filename
```

在本範例中，共同來源 URI 前置字串為 `gs://my_bucket/my_table`。

### 不支援的資料配置

如果分區索引鍵名稱未在目錄路徑中編碼，分區結構定義偵測就會失敗。舉例來說，分區索引鍵名稱未編碼入下列路徑：

```
gs://my_bucket/my_table/2019-10-31/en/my_filename
```

如果檔案的結構定義順序不一致，系統也無法進行偵測作業。舉例來說，請考慮下列兩個檔案，其中包含反向分區鍵編碼：

```
gs://my_bucket/my_table/dt=2019-10-31/lang=en/my_filename
gs://my_bucket/my_table/lang=fr/dt=2018-10-31/my_filename
```

### 偵測模式

BigQuery 支援三種 Hive 分區結構定義偵測模式：

* `AUTO`：系統會自動偵測鍵名和類型。可偵測的類型如下：

  + [STRING](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#string_type)
  + [INTEGER](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#integer_types)
  + [DATE](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#date_type)

    例如 `/date=2018-10-18/`。
  + [TIMESTAMP](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#timestamp_type)

    例如 `/time=2018-10-18 16:00:00+00/`。
* `STRINGS`：鍵名會自動轉換為 `STRING` 類型。
* `CUSTOM`：分區索引鍵結構定義會按照來源 URI 前置字串中指定的方式編碼。

#### 自訂分區索引鍵結構定義

如要使用 `CUSTOM` 結構定義，您必須在來源 URI 前置字串欄位中指定結構定義。使用 `CUSTOM` 結構定義，即可指定每個分區索引鍵的類型。這些值必須能有效剖析為指定類型，否則查詢會失敗。

舉例來說，如果將 `source_uri_prefix` 旗標設為 `gs://my_bucket/my_table/{dt:DATE}/{val:STRING}`，BigQuery 會將 `val` 視為 STRING，將 `dt` 視為 DATE，並使用 `gs://my_bucket/my_table` 做為相符檔案的來源 URI 前置字串。

### 分區修剪

BigQuery 會盡可能使用分區索引鍵上的查詢述詞，來剪除分區。這樣一來，BigQuery 就不會讀取不必要的檔案，有助於提升效能。

### 查詢中分區鍵的述詞篩選器

建立外部資料分割資料表時，您可以啟用 [HivePartitioningOptions](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables?hl=zh-tw#hivepartitioningoptions) 下方的 `requirePartitionFilter` 選項，要求在資料分割索引鍵上使用述詞篩選器。

啟用這個選項後，如果嘗試查詢外部資料表，但未指定 `WHERE` 子句，就會產生下列錯誤：`Cannot query over table <table_name> without a filter over column(s)
<partition key names> that can be used for partition elimination`。

**注意：**必須至少有一個述詞只參照一或多個分區鍵，篩選器才符合分區排除條件。舉例來說，如果資料表在檔案中具有分區索引鍵 `val` 和資料欄 `f`，則下列兩個 `WHERE` 子句都符合要求：
  
    `WHERE val = "key"`
  
    `WHERE val = "key" AND f = "column"`

不過，`WHERE (val = "key" OR f = "column")` 仍不足以解決問題。

## 限制

* Hive 分區支援功能假設所有 URI 都有共同的來源 URI 前置字串，且該前置字串會在分區編碼之前結束，如下所示：`gs://BUCKET/PATH_TO_TABLE/`。
* Hive 分區資料表的目錄結構應具有相同的分區鍵，且分區鍵的順序相同，每個資料表最多可有十個分區鍵。
* 資料必須採用[預設 Hive 分區版面配置](#supported_data_layouts)。
* Hive 分區鍵和基礎檔案中的資料欄不得重疊。
* 僅支援 [GoogleSQL](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw)。
* 查詢儲存在 Cloud Storage 中外部資料來源的所有[限制](https://docs.cloud.google.com/bigquery/external-data-sources?hl=zh-tw#external_data_source_limitations)均適用。

## 後續步驟

* 瞭解[分區資料表](https://docs.cloud.google.com/bigquery/docs/partitioned-tables?hl=zh-tw)。
* 瞭解如何[在 BigQuery 中使用 SQL](https://docs.cloud.google.com/bigquery/docs/introduction-sql?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-10-22 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-10-22 (世界標準時間)。"],[],[]]