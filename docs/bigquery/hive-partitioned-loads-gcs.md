* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 載入外部分區資料

BigQuery 可以使用 Hive 分區配置，載入儲存在 Cloud Storage 中的資料。*Hive 分區*是指外部資料會整理成多個檔案，並採用命名慣例將檔案分成不同分區。詳情請參閱「[支援的資料版面配置](#supported_data_layouts)」。

根據預設，資料載入 BigQuery 後不會分區，除非您明確建立[分區資料表](https://docs.cloud.google.com/bigquery/docs/partitioned-tables?hl=zh-tw)。

## 載入 Hive 分區資料

如要載入 Hive 分區資料，請選擇下列任一選項：

### 主控台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往 BigQuery](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的「Explorer」explore。
3. 在「Explorer」窗格中展開專案，按一下「Datasets」(資料集)，然後選取資料集。
4. 依序點選 more\_vert「動作」和「建立資料表」。系統會開啟「建立資料表」窗格。
5. 在「來源」部分，指定下列詳細資料：

1. 在「Create table from」(使用下列資料建立資料表) 部分，選取「Google Cloud Storage」。
2. 在「Select file from Cloud Storage bucket」(從 Cloud Storage 值區選取檔案)  中，使用[萬用字元](https://docs.cloud.google.com/bigquery/docs/batch-loading-data?hl=zh-tw#load-wildcards)輸入 Cloud Storage 資料夾的路徑。例如 `my_bucket/my_files*`。Cloud Storage 值區的位置必須與要建立、附加或覆寫的表格所在的資料集位置相同。
3. 從「檔案格式」清單中選取檔案類型。
4. 選取「Source data partitioning」(來源資料分割) 核取方塊，然後在「Select Source URI Prefix」(選取來源 URI 前置字串) 中輸入 Cloud Storage URI 前置字串。例如：`gs://my_bucket/my_files`。
5. 在「Partition inference mode」(分割區推論模式) 部分中，選取下列其中一個選項：
   * **自動推論類型**：將分區結構定義偵測模式設為 `AUTO`。
   * **將所有資料欄視為字串**：將分區結構定義偵測模式設為 `STRINGS`。
   * **提供我自己的**：將分區結構定義偵測模式設為 `CUSTOM`，然後手動輸入分區鍵的結構定義資訊。詳情請參閱「[提供自訂分區索引鍵結構定義](https://docs.cloud.google.com/bigquery/docs/hive-partitioned-loads-gcs?hl=zh-tw#custom_partition_key_schema)」。
6. 選用：如要要求所有查詢都必須使用這個資料表的分區篩選器，請選取「Require partition filter」(需要分區篩選器) 核取方塊。使用分區篩選器可以降低成本並提升效能。詳情請參閱[在查詢中對分區鍵套用述詞篩選器](https://docs.cloud.google.com/bigquery/docs/hive-partitioned-queries-gcs?hl=zh-tw#requiring_predicate_filters_on_partition_keys_in_queries)。

6. 在「目的地」部分，指定下列詳細資料：
   1. 在「Project」(專案) 部分，選取要在其中建立資料表的專案。
   2. 在「Dataset」(資料集) 部分，選取要建立資料表的資料集。
   3. 在「Table」(資料表) 中，輸入要建立的資料表名稱。
   4. 在「Table type」(資料表類型) 選取「Native table」(原生資料表)。
7. 在「Schema」(結構定義) 區段中，輸入[結構定義](https://docs.cloud.google.com/bigquery/docs/schemas?hl=zh-tw)。
8. 如要啟用結構定義[自動偵測](https://docs.cloud.google.com/bigquery/docs/schema-detect?hl=zh-tw)功能，請選取「Auto detect」(自動偵測)。
9. 如要忽略含有與結構定義不符之額外資料欄值的資料列，請展開「進階選項」部分，然後選取「不明的值」。
10. 點選「建立資料表」。

### SQL

如要建立外部分區資料表，請使用 [`LOAD DATA` 陳述式的 `WITH PARTITION COLUMNS` 子句](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/load-statements?hl=zh-tw#load_data_statement)，指定分區結構定義詳細資料。

如需範例，請參閱「[載入外部分區檔案](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/load-statements?hl=zh-tw#load_a_file_that_is_externally_partitioned)」。

### bq

使用自動偵測分區索引鍵類型功能載入 Hive 分區資料：

```
bq load --source_format=ORC --hive_partitioning_mode=AUTO \
--hive_partitioning_source_uri_prefix=gcs_uri_shared_prefix \
dataset.table gcs_uris
```

使用字串類型分區索引鍵偵測功能載入 Hive 分區資料：

```
bq load --source_format=CSV --autodetect \
--hive_partitioning_mode=STRINGS \
--hive_partitioning_source_uri_prefix=gcs_uri_shared_prefix \
dataset.table gcs_uris
```

使用透過 `source\_uri\_prefix` 欄位編碼的自訂分區索引鍵結構定義，載入 Hive 分區資料：

```
bq load --source_format=JSON --hive_partitioning_mode=CUSTOM \
--hive_partitioning_source_uri_prefix=gcs_uri_shared_prefix/partition_key_schema \
dataset.table gcs_uris file_schema
```

分區索引鍵結構定義會編碼入緊鄰來源 URI 前置字串後方的位置。請使用以下格式指定 `--hive_partitioning_source_uri_prefix`：

```
--hive_partitioning_source_uri_prefix=gcs_uri_shared_prefix/{key1:TYPE1}/{key2:TYPE2}/{key3:TYPE3}
```

### API

在 [`JobConfigurationLoad`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#jobconfigurationload) 上設定 [`HivePartitioningOptions`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables?hl=zh-tw#hivepartitioningoptions)，即可支援 Hive 分區。

**注意：** 如果 `hivePartitioningOptions.mode` 設為 `CUSTOM`，您必須在 `hivePartitioningOptions.sourceUriPrefix` 欄位中編碼分區索引鍵結構定義，如下所示：`gs://BUCKET/PATH_TO_TABLE/{KEY1:TYPE1}/{KEY2:TYPE2}/...`

## 執行增量載入

以下列資料配置為例：

```
gs://my_bucket/my_table/dt=2019-10-31/val=1/file1
gs://my_bucket/my_table/dt=2018-10-31/val=2/file2
gs://my_bucket/my_table/dt=2017-10-31/val=3/file3
gs://my_bucket/my_table/dt=2016-10-31/val=4/file4
```

如要僅載入 2019 年 10 月 31 日的資料，請執行下列操作：

* 將「Hive 分區模式」設為 `AUTO`、`STRINGS` 或 `CUSTOM`。
* 如為 `AUTO` 或 `STRINGS` Hive 分區模式，請將來源 URI 前置字串設為 `gs://my_bucket/my_table/`。如為 CUSTOM 分區模式，請提供 `gs://my_bucket/my_table/{dt:DATE}/{val:INTEGER}`。
* 使用 URI `gs://my_bucket/my_table/dt=2019-10-31/*`。
* 資料載入時會包含 `dt` 和 `val` 資料欄，分別具有 `2019-10-31` 和 `1` 值。

如要僅載入特定檔案的資料，請按照下列步驟操作：

* 將「Hive 分區模式」設為 `AUTO`、`STRINGS` 或 `CUSTOM`。
* 如為 `AUTO` 或 `STRINGS` Hive 分區模式，請將來源 URI 前置字串設為 `gs://my_bucket/my_table/`。如為 `CUSTOM`，請提供 `gs://my_bucket/my_table/{dt:DATE}/{val:INTEGER}`。
* 使用 URI `gs://my_bucket/my_table/dt=2017-10-31/val=3/file3,gs://my_bucket/my_table/dt=2016-10-31/val=4/file4`。
* 資料已從兩個檔案載入，且 `dt` 和 `val` 資料欄已填入。

## 分區結構定義

以下各節說明 [預設 Hive 分割配置](#supported_data_layouts)，以及 BigQuery 支援的[結構定義偵測模式](#detection_modes)。

### 支援的資料配置

查詢 Cloud Storage 中的資料時，Hive 分區索引鍵會顯示為一般資料欄。資料必須符合預設 Hive 分區配置。舉例來說，下列檔案均符合預設配置，鍵/值組合會以目錄型式排列並採用等號 (=) 做為分隔符，而且分區索引鍵的順序一律相同：

```
gs://my_bucket/my_table/dt=2019-10-31/lang=en/my_filename
gs://my_bucket/my_table/dt=2018-10-31/lang=fr/my_filename
```

在本例中，常見的來源 URI 前置字串為 `gs://my_bucket/my_table`。

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

## 限制

* 建構 Hive 分區支援時，我們會假設所有 URI 都有一個通用來源 URI 前置字串，字串結尾處緊接在分區編碼之前，如下所示：`gs://BUCKET/PATH_TO_TABLE/`。
* 假設 Hive 分區資料表的目錄結構具有相同的分區索引鍵、索引鍵的顯示順序相同，且每個資料表最多包含十個分區索引鍵。
* 資料必須符合[預設 Hive 分區配置](#supported_data_layouts)。
* Hive 分區索引鍵不得與基礎檔案中的資料欄重疊。
* 僅支援 [GoogleSQL](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw)。
* 適用於所有[從 Cloud Storage 載入的限制](https://docs.cloud.google.com/bigquery/docs/batch-loading-data?hl=zh-tw#limitations)。

## 後續步驟

* 瞭解[分區資料表](https://docs.cloud.google.com/bigquery/docs/partitioned-tables?hl=zh-tw)。
* 瞭解如何[在 BigQuery 中使用 SQL](https://docs.cloud.google.com/bigquery/docs/introduction-sql?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-02 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-02 (世界標準時間)。"],[],[]]