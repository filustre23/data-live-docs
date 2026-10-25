Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 載入外部分區資料

BigQuery 可讓您從使用 Apache Hive 分區版面配置的 Cloud Storage 載入資料，並將分區鍵納入資料表的資料欄。*Hive 分區*是指將外部資料整理成多個檔案，並採用命名慣例，將檔案分成不同分區。

根據預設，除非您明確建立[分區資料表](https://docs.cloud.google.com/bigquery/docs/partitioned-tables?hl=zh-tw)，否則資料載入 BigQuery 後不會分區。詳情請參閱「[支援的資料版面配置](https://docs.cloud.google.com/bigquery/docs/hive-partitioned-loads-gcs?hl=zh-tw#supported_data_layouts)」。

## 載入 Hive 分區資料

如要載入 Hive 分區資料，請選擇下列其中一個選項：

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往 BigQuery](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中展開專案，點選「資料集」，然後選取資料集。
4. 按一下 more\_vert「Actions」(動作)，然後點選「Create table」(建立資料表)。「建立資料表」窗格隨即開啟。
5. 在「Source」(來源) 部分，指定下列詳細資料：

1. 在「建立資料表來源」部分，選取「Google Cloud Storage」。
2. 在「Select file from Cloud Storage bucket」(從 Cloud Storage bucket 選取檔案) 部分，使用[萬用字元](https://docs.cloud.google.com/bigquery/docs/batch-loading-data?hl=zh-tw#load-wildcards)輸入 Cloud Storage 資料夾的路徑。例如：`my_bucket/my_files*`。Cloud Storage bucket 必須與資料集位於相同位置，而該資料集包含您要建立、附加或覆寫的資料表。
3. 從「File format」(檔案格式) 清單中選取檔案類型。
4. 勾選「Source data partitioning」(來源資料分區) 核取方塊，然後在「Select Source URI Prefix」(選取來源 URI 前置字元) 中輸入 Cloud Storage URI 前置字元。例如：`gs://my_bucket/my_files`。
5. 在「Partition inference mode」(分區推論模式) 部分，選取下列其中一個選項：
   * **自動推論類型**：將分區結構定義偵測模式設為 `AUTO`。
   * **將所有資料欄視為字串**：將分區架構偵測模式設為 `STRINGS`。
   * 「Provide my own」(自行提供)：將分區結構定義偵測模式設為 `CUSTOM`，並手動輸入分區索引鍵的結構定義資訊。詳情請參閱「[提供自訂分區索引鍵結構定義](https://docs.cloud.google.com/bigquery/docs/hive-partitioned-loads-gcs?hl=zh-tw#custom_partition_key_schema)」。
6. 選用：如要對這個資料表的所有查詢要求分區篩選器，請勾選「Require partition filter」(必須使用分區篩選器) 核取方塊。規定必須使用分區篩選器，或許可以降低費用及提高成效。詳情請參閱「[在查詢中要求對分區索引鍵使用述詞篩選器](https://docs.cloud.google.com/bigquery/docs/hive-partitioned-queries-gcs?hl=zh-tw#requiring_predicate_filters_on_partition_keys_in_queries)」。

6. 在「Destination」(目的地) 部分，指定下列詳細資料：
   1. 在「Project」(專案) 部分，選取要建立資料表的專案。
   2. 在「Dataset」(資料集) 部分，選取要建立資料表的資料集。
   3. 在「Table」(資料表) 中，輸入要建立的資料表名稱。
   4. 在「Table type」(資料表類型) 部分，選取「Native table」(原生資料表)。
7. 在「Schema」(結構定義) 部分，輸入[結構定義](https://docs.cloud.google.com/bigquery/docs/schemas?hl=zh-tw)。
8. 如要啟用結構定義[自動偵測](https://docs.cloud.google.com/bigquery/docs/schema-detect?hl=zh-tw)功能，請選取「自動偵測」。
9. 如要忽略含有與結構定義不符的多餘資料欄值的資料列，請展開「Advanced options」(進階選項) 區段，然後選取「Unknown values」(不明的值)。
10. 點選「建立資料表」。

### SQL

如要建立外部資料分割資料表，請使用 [`LOAD DATA` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/load-statements?hl=zh-tw#load_data_statement)的 `WITH PARTITION COLUMNS` 子句，指定資料分割結構定義詳細資料。

如需範例，請參閱「[載入外部分區檔案](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/load-statements?hl=zh-tw#load_a_file_that_is_externally_partitioned)」。

### bq

使用自動偵測分區索引鍵類型功能，載入 Hive 分區資料：

```
bq load --source_format=ORC --hive_partitioning_mode=AUTO \
--hive_partitioning_source_uri_prefix=gcs_uri_shared_prefix \
dataset.table gcs_uris
```

使用字串類型的分區索引鍵偵測功能，載入 Hive 分區資料：

```
bq load --source_format=CSV --autodetect \
--hive_partitioning_mode=STRINGS \
--hive_partitioning_source_uri_prefix=gcs_uri_shared_prefix \
dataset.table gcs_uris
```

使用以 `source\_uri\_prefix` 欄位編碼的自訂分區索引鍵架構，載入 Hive 分區資料：

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

只要在 [`JobConfigurationLoad`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#jobconfigurationload) 上設定 [`HivePartitioningOptions`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables?hl=zh-tw#hivepartitioningoptions)，即可支援 Hive 分區。

**注意：** 如果 `hivePartitioningOptions.mode` 設為 `CUSTOM`，您必須在 `hivePartitioningOptions.sourceUriPrefix` 欄位中編碼分區索引鍵結構定義，如下所示：
`gs://BUCKET/PATH_TO_TABLE/{KEY1:TYPE1}/{KEY2:TYPE2}/...`

## 執行增量載入

以下列資料配置為例：

```
gs://my_bucket/my_table/dt=2019-10-31/val=1/file1
gs://my_bucket/my_table/dt=2018-10-31/val=2/file2
gs://my_bucket/my_table/dt=2017-10-31/val=3/file3
gs://my_bucket/my_table/dt=2016-10-31/val=4/file4
```

如要僅載入 2019-10-31 的資料，請按照下列步驟操作：

* 將「Hive partitioning mode」(Hive 分區模式) 設為 `AUTO`、`STRINGS` 或 `CUSTOM`。
* 將 `AUTO` 或 `STRINGS` Hive 分區模式的來源 URI 前置字串設為 `gs://my_bucket/my_table/`。如果是 CUSTOM，請提供 `gs://my_bucket/my_table/{dt:DATE}/{val:INTEGER}`。
* 使用 URI `gs://my_bucket/my_table/dt=2019-10-31/*`。
* 資料載入時會包含 `dt` 和 `val` 資料欄，分別具有 `2019-10-31` 和 `1` 值。

如要僅載入特定檔案中的資料，請按照下列步驟操作：

* 將「Hive partitioning mode」(Hive 分區模式) 設為 `AUTO`、`STRINGS` 或 `CUSTOM`。
* 將 `AUTO` 或 `STRINGS` Hive 分區模式的來源 URI 前置字串設為 `gs://my_bucket/my_table/`。如果是 `CUSTOM`，請提供 `gs://my_bucket/my_table/{dt:DATE}/{val:INTEGER}`。
* 使用 URI `gs://my_bucket/my_table/dt=2017-10-31/val=3/file3,gs://my_bucket/my_table/dt=2016-10-31/val=4/file4`。
* 資料已從兩個檔案載入，且 `dt` 和 `val` 資料欄已填入。

## 分區結構定義

以下各節將說明 BigQuery 支援的[預設 Hive 分區版面配置](#supported_data_layouts)和[結構定義偵測模式](#detection_modes)。

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

## 限制

* Hive 分區支援功能假設所有 URI 都有共同的來源 URI 前置字串，且該前置字串會在分區編碼之前結束，如下所示：`gs://BUCKET/PATH_TO_TABLE/`。
* Hive 分區資料表的目錄結構應具有相同的分區鍵，且分區鍵的順序相同，每個資料表最多可有十個分區鍵。
* 資料必須採用[預設 Hive 分區版面配置](#supported_data_layouts)。
* Hive 分區鍵和基礎檔案中的資料欄不得重疊。
* 僅支援 [GoogleSQL](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw)。
* 適用於所有[從 Cloud Storage 載入的限制](https://docs.cloud.google.com/bigquery/docs/batch-loading-data?hl=zh-tw#limitations)。

## 後續步驟

* 瞭解[分區資料表](https://docs.cloud.google.com/bigquery/docs/partitioned-tables?hl=zh-tw)。
* 瞭解如何[在 BigQuery 中使用 SQL](https://docs.cloud.google.com/bigquery/docs/introduction-sql?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-10-24 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-10-24 (世界標準時間)。"],[],[]]