Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [參考資料](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 從 Apache Hive 遷移結構定義和資料

本文說明如何將資料、安全性設定和管道從 Apache Hive 遷移至 BigQuery。

您也可以使用[批次 SQL 翻譯](https://docs.cloud.google.com/bigquery/docs/batch-sql-translator?hl=zh-tw)大量遷移 SQL 指令碼，或使用[互動式 SQL 翻譯](https://docs.cloud.google.com/bigquery/docs/interactive-sql-translator?hl=zh-tw)翻譯臨時查詢。這兩項 SQL 轉譯服務都完整支援 Apache HiveQL。如要翻譯 Databricks SQL 或 Apache Spark SQL 工作負載，請參閱「[Databricks 和 Apache Spark SQL 翻譯參考資料](https://docs.cloud.google.com/bigquery/docs/migration/databricks-sql?hl=zh-tw)」。

## 準備遷移

下列各節說明如何收集資料表統計資料、中繼資料和安全性設定的相關資訊，協助您將資料倉儲從 Apache Hive 遷移至 BigQuery。

### 收集來源資料表資訊

收集來源 Hive 資料表的相關資訊，例如資料列數、資料欄數、資料欄資料類型、大小、資料輸入格式和位置。這項資訊在遷移程序中非常實用，也可用於驗證資料遷移。如果資料庫 `corp` 中有名為 `employees` 的 Hive 資料表，請使用下列指令收集資料表資訊：

```
# Find the number of rows in the table
hive> SELECT COUNT(*) FROM corp.employees;

# Output all the columns and their data types
hive> DESCRIBE corp.employees;

# Output the input format and location of the table
hive> SHOW CREATE TABLE corp.employees;
Output:
…
STORED AS INPUTFORMAT
  'org.apache.hadoop.hive.ql.io.avro.AvroContainerInputFormat'
OUTPUTFORMAT
  'org.apache.hadoop.hive.ql.io.avro.AvroContainerOutputFormat'
LOCATION
  'hdfs://demo_cluster/user/hive/warehouse/corp/employees'
TBLPROPERTIES (
…

# Get the total size of the table data in bytes
shell> hdfs dfs -du -s TABLE_LOCATION
```

### 來源資料表格式轉換

Hive 支援的部分格式無法直接擷取至 BigQuery。

Hive 支援以以下格式儲存資料：

* 文字檔
* RC 檔案
* 序列檔案
* Avro 檔案
* ORC 檔案
* Parquet 檔案

BigQuery 支援從 Cloud Storage 載入下列任一檔案格式的資料：

* CSV
* JSON (以換行符號分隔)
* Avro
* ORC
* Parquet

BigQuery 可直接載入 Avro、ORC 和 Parquet 格式的資料檔案，不需要結構定義檔案。如果文字檔案的格式不是 CSV 或 JSON (以換行符號分隔)，您可以將資料複製到 Avro 格式的 Hive 資料表，也可以將資料表結構定義轉換為 BigQuery [JSON 結構定義](https://docs.cloud.google.com/bigquery/docs/schemas?hl=zh-tw)，以便在擷取時提供。

### 收集 Hive 存取控管設定

Hive 和 BigQuery 的存取控管機制不同。收集所有 Hive 存取控管設定，例如角色、群組、成員和授予的權限。在 BigQuery 中，以資料集為單位規劃安全性模型，並導入精細的 ACL。舉例來說，Hive 使用者可以對應至 [Google 帳戶](https://docs.cloud.google.com/iam/docs/principals-overview?hl=zh-tw#google-account)，HDFS 群組則可以對應至 [Google 群組](https://docs.cloud.google.com/iam/docs/overview?hl=zh-tw#google_group)。您可以在資料集層級設定存取權。使用下列指令，收集 Hive 中的存取控管設定：

```
# List all the users
> hdfs dfs -ls /user/ | cut -d/ -f3

# Show all the groups that a specific user belongs to
> hdfs groups user_name

# List all the roles
hive> SHOW ROLES;

# Show all the roles assigned to a specific group
hive> SHOW ROLE GRANT GROUP group_name

# Show all the grants for a specific role
hive> SHOW GRANT ROLE role_name;

# Show all the grants for a specific role on a specific object
hive> SHOW GRANT ROLE role_name on object_type object_name;
```

在 Hive 中，如果您具備必要權限，可以直接存取資料表背後的 HDFS 檔案。在標準 BigQuery 資料表中，資料載入資料表後，會儲存在 BigQuery 儲存空間。您可以使用 BigQuery Storage Read API 讀取資料，但所有 IAM、資料列和資料欄層級的安全性仍會強制執行。如果您使用 BigQuery 外部資料表查詢 Cloud Storage 中的資料，Cloud Storage 的存取權也由 IAM 控管。

您可以建立 [BigLake 資料表](https://docs.cloud.google.com/bigquery/docs/biglake-quickstart?hl=zh-tw)，以便使用[連接器](https://docs.cloud.google.com/bigquery/docs/biglake-quickstart?hl=zh-tw#query-biglake-table-using-connectors)，透過 Apache Spark、Trino 或 Hive 查詢資料。BigQuery Storage API 會針對 Cloud Storage 或 BigQuery 中的所有 BigLake 資料表，強制執行資料列和資料欄層級的控管政策。

## 資料遷移

將 Hive 資料從地端部署或其他雲端式來源叢集遷移至 BigQuery，需要執行兩個步驟：

1. 將資料從來源叢集複製到 Cloud Storage
2. 將 Cloud Storage 中的資料載入 BigQuery

以下各節將說明如何遷移 Hive 資料、驗證遷移的資料，以及處理持續擷取資料的遷移作業。範例是針對非 ACID 資料表編寫。

### 分區資料欄資料

在 Hive 中，分區資料表中的資料會儲存在目錄結構中。資料表的每個分區都與分區資料欄的特定值相關聯。資料檔案本身不含分區資料欄的任何資料。使用 `SHOW PARTITIONS` 指令，列出分區資料表中的不同分區。

以下範例顯示來源 Hive 資料表在 `joining_date` 和 `department` 資料欄上進行分區。這個資料表下的資料檔案不含與這兩個資料欄相關的任何資料。

```
hive> SHOW PARTITIONS corp.employees_partitioned
joining_date="2018-10-01"/department="HR"
joining_date="2018-10-01"/department="Analyst"
joining_date="2018-11-01"/department="HR"
```

如要複製這些資料欄，其中一種方法是在載入 BigQuery 之前，將分區資料表轉換為非分區資料表：

1. 建立非分區資料表，結構定義與分區資料表類似。
2. 從來源分區資料表將資料載入未分區資料表。
3. 將暫存未分區資料表下的這些資料檔案複製到 Cloud Storage。
4. 使用 `bq load` 指令將資料載入 BigQuery，並提供 `TIMESTAMP` 或 `DATE` 類型分區資料欄的名稱 (如有)，做為 `time_partitioning_field` 引數。

### 將資料複製到 Cloud Storage

資料遷移的第一步是將資料複製到 Cloud Storage。使用 [Hadoop DistCp](https://hadoop.apache.org/docs/current/hadoop-distcp/DistCp.html)，將資料從地端部署或其他雲端叢集複製到 Cloud Storage。將資料儲存在 bucket 中，該 bucket 須與您要在 BigQuery 儲存資料的資料集位於相同區域或多區域。舉例來說，如果您想使用東京區域的現有 BigQuery 資料集做為目的地，就必須選擇東京的 Cloud Storage 區域 bucket 來存放資料。

選取 Cloud Storage bucket 位置後，您可以使用下列指令，列出 `employees` Hive 資料表位置的所有資料檔案：

```
> hdfs dfs -ls hdfs://demo_cluster/user/hive/warehouse/corp/employees
hdfs://demo_cluster/user/hive/warehouse/corp/employees/000000_0
hdfs://demo_cluster/user/hive/warehouse/corp/employees/000001_0
hdfs://demo_cluster/user/hive/warehouse/corp/employees/000002_0
```

將上述所有檔案複製到 Cloud Storage：

```
> hadoop distcp
hdfs://demo_cluster/user/hive/warehouse/corp/employees
gs://hive_data/corp/employees
```

請注意，系統會根據[資料儲存空間定價](https://cloud.google.com/storage/pricing?hl=zh-tw#storage-pricing)，向您收取在 Cloud Storage 儲存資料的費用。

暫存目錄可能包含為查詢工作建立的中繼檔案。執行 `bq load` 指令前，請務必刪除這類目錄。

### 正在載入資料

BigQuery 支援從 Cloud Storage [批次載入多種格式的資料](https://docs.cloud.google.com/bigquery/docs/batch-loading-data?hl=zh-tw)。建立載入工作前，請確認要載入資料的 BigQuery [資料集](https://docs.cloud.google.com/bigquery/docs/datasets?hl=zh-tw)已存在。

下列指令會顯示從 Hive 複製的非 ACID 資料表資料：

```
> gcloud storage ls gs://hive_data/corp/employees/
gs://hive-migration/corp/employees/
gs://hive-migration/corp/employees/000000_0
gs://hive-migration/corp/employees/000001_0
gs://hive-migration/corp/employees/000002_0
```

如要將 Hive 資料載入 BigQuery，請使用 [`bq load` 指令](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_load)。您可以在網址中使用萬用字元 \*，從共用相同物件前置字元的多個檔案載入資料。例如，使用下列指令載入所有共用前置字串 `gs://hive_data/corp/employees/` 的檔案：

```
bq load --source_format=AVRO corp.employees gs://hive_data/corp/employees/*
```

由於工作可能需要很長時間才能完成，您可以將 `--sync` 旗標設為 `False`，以非同步方式執行工作。執行 `bq load` 指令會輸出所建立載入工作的 ID，因此您可以使用這個指令輪詢工作狀態。這類資料包括工作類型、工作狀態，以及執行工作的使用者等詳細資料。

使用各項載入工作的 工作 ID 輪詢工作狀態，並檢查是否有任何工作因錯誤而失敗。如果發生失敗，BigQuery 會在將資料載入資料表時，採用「全部或全無」的做法。您可以嘗試解決錯誤，並安全地重新建立其他載入工作。詳情請參閱「[排解錯誤](https://docs.cloud.google.com/bigquery/troubleshooting-errors?hl=zh-tw)」。

請確認每個資料表和專案都有足夠的載入工作[配額](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#load_jobs)。如果超過配額，載入工作就會失敗，並顯示 `quotaExceeded` 錯誤。

請注意，從 Cloud Storage 將資料載入 BigQuery 的載入作業不會產生費用。資料載入 BigQuery 後，須按照 BigQuery 的[儲存空間定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#storage)付費。載入工作順利完成後，您可以刪除 Cloud Storage 中剩餘的檔案，以免因儲存多餘資料而產生費用。

### 驗證

成功載入資料後，您可以比較 [Hive](#collect_source_table_information) 和 BigQuery 資料表中的資料列數量，驗證遷移的資料。查看[資料表資訊](https://docs.cloud.google.com/bigquery/docs/tables?hl=zh-tw#get_information_about_tables)，取得 BigQuery 資料表的詳細資料，例如資料列數、資料欄數、分區欄位或叢集欄位。如需額外驗證，建議您試用[資料驗證工具](https://github.com/GoogleCloudPlatform/professional-services-data-validator)。

### 連續擷取

如果您持續將資料擷取至 Hive 資料表，請先執行初始遷移，然後僅將增量資料變更遷移至 BigQuery。通常會建立重複執行的指令碼，尋找並載入新資料。方法有很多種，以下各節將說明其中一種。

您可以在 [Cloud SQL](https://docs.cloud.google.com/sql/docs/mysql?hl=zh-tw) 資料庫資料表 (在下列各節中稱為追蹤資料表) 中追蹤遷移進度。在第一次執行遷移作業時，將進度儲存在追蹤資料表中。在後續的遷移作業中，請使用追蹤資料表資訊，偵測是否有任何額外資料已擷取，且可遷移至 BigQuery。

選取 `INT64`、`TIMESTAMP` 或 `DATE` 類型的 ID 欄，以區分增量資料。這稱為增量資料欄。

下表是未分區資料表的範例，其增量資料欄使用 `TIMESTAMP` 類型：

```
+-----------------------------+-----------+-----------+-----------+-----------+
| timestamp_identifier        | column_2  | column_3  | column_4  | column_5  |
+-----------------------------+-----------+-----------+-----------+-----------+
| 2018-10-10 21\:56\:41       |           |           |           |           |
| 2018-10-11 03\:13\:25       |           |           |           |           |
| 2018-10-11 08\:25\:32       |           |           |           |           |
| 2018-10-12 05\:02\:16       |           |           |           |           |
| 2018-10-12 15\:21\:45       |           |           |           |           |
+-----------------------------+-----------+-----------+-----------+-----------+
```

下表是依 `DATE` 已指定類型和格式的欄 `partition_column` 分區的資料表示例。每個分區都有一個整數類型的遞增資料欄 `int_identifier`。

```
+---------------------+---------------------+----------+----------+-----------+
| partition_column    | int_identifier      | column_3 | column_4 | column_5  |
+---------------------+---------------------+----------+----------+-----------+
| 2018-10-01          | 1                   |          |          |           |
| 2018-10-01          | 2                   |          |          |           |
| ...                 | ...                 |          |          |           |
| 2018-10-01          | 1000                |          |          |           |
| 2018-11-01          | 1                   |          |          |           |
| 2018-11-01          | 2                   |          |          |           |
| ...                 | ...                 |          |          |           |
| 2018-11-01          | 2000                |          |          |           |
+---------------------+---------------------+----------+----------+-----------+
```

以下各節將說明如何根據 Hive 資料是否已分區，以及是否具有遞增資料欄，來遷移 Hive 資料。

#### 沒有漸進式資料欄的非分區資料表

假設 Hive 中沒有檔案壓縮，Hive 會在擷取新資料時建立新的資料檔案。在第一次執行期間，將檔案清單儲存在追蹤資料表中，並將這些檔案複製到 Cloud Storage，然後載入 BigQuery，完成 Hive 資料表的初始遷移。

```
> hdfs dfs -ls hdfs://demo_cluster/user/hive/warehouse/corp/employees
Found 3 items
hdfs://demo_cluster/user/hive/warehouse/corp/employees/000000_0
hdfs://demo_cluster/user/hive/warehouse/corp/employees/000001_0
hdfs://demo_cluster/user/hive/warehouse/corp/employees/000002_0
```

初始遷移作業完成後，部分資料會擷取至 Hive。您只需要將這些增量資料遷移至 BigQuery。在後續的遷移作業中，再次列出資料檔案，並與追蹤資料表中的資訊進行比較，偵測尚未遷移的新資料檔案。

```
> hdfs dfs -ls hdfs://demo_cluster/user/hive/warehouse/corp/employees
Found 5 items
hdfs://demo_cluster/user/hive/warehouse/corp/employees/000000_0
hdfs://demo_cluster/user/hive/warehouse/corp/employees/000001_0
hdfs://demo_cluster/user/hive/warehouse/corp/employees/000002_0
hdfs://demo_cluster/user/hive/warehouse/corp/employees/000003_0
hdfs://demo_cluster/user/hive/warehouse/corp/employees/000004_0
```

在這個範例中，資料表位置有兩個新檔案。將這些新資料檔案複製到 Cloud Storage，並載入現有的 BigQuery 資料表，即可遷移資料。

#### 含有漸進式資料欄的非分區資料表

在這種情況下，您可以使用遞增資料欄的最大值，判斷是否新增了任何資料。執行初始遷移作業時，請查詢 Hive 資料表，擷取遞增資料欄的最大值，並將其儲存在追蹤資料表中：

```
hive> SELECT MAX(timestamp_identifier) FROM corp.employees;
2018-12-31 22:15:04
```

在後續的遷移作業中，再次重複執行相同的查詢，擷取增量資料欄目前的最大值，並與追蹤資料表中的前一個最大值進行比較，檢查是否存在增量資料：

```
hive> SELECT MAX(timestamp_identifier) FROM corp.employees;
2019-01-04 07:21:16
```

如果目前的最大值大於先前的值，表示增量資料已擷取至 Hive 資料表，如範例所示。如要遷移增量資料，請建立暫存資料表，並僅將增量資料載入其中。

```
hive> CREATE TABLE stage_employees LIKE corp.employees;
hive> INSERT INTO TABLE stage_employees SELECT * FROM corp.employees WHERE timestamp_identifier>"2018-12-31 22:15:04" and timestamp_identifier<="2019-01-04 07:21:16"
```

列出 HDFS 資料檔案、將檔案複製到 Cloud Storage，然後載入現有的 BigQuery 資料表，藉此遷移暫存資料表。

#### 沒有漸進式資料欄的分區資料表

將資料擷取至分區資料表時，可能會建立新的分區、將增量資料附加至現有分區，或同時執行這兩項操作。在這種情況下，您可以找出更新的分區，但由於沒有可區分的增量資料欄，因此無法輕易找出新增至這些現有分區的資料。另一個選項是建立及維護 HDFS 快照，但快照會造成 Hive 效能問題，因此通常會停用。

首次遷移資料表時，請執行 `SHOW PARTITIONS` 指令，並將不同分區的資訊儲存在追蹤資料表中。

```
hive> SHOW PARTITIONS corp.employees
partition_column=2018-10-01
partition_column=
```