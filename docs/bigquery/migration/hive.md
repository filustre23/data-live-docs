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

您也可以使用[批次 SQL 翻譯](https://docs.cloud.google.com/bigquery/docs/batch-sql-translator?hl=zh-tw)大量遷移 SQL 指令碼，或使用[互動式 SQL 翻譯](https://docs.cloud.google.com/bigquery/docs/interactive-sql-translator?hl=zh-tw)翻譯臨時查詢。SQL 翻譯服務全面支援 Apache HiveQL。

## 為遷移作業做好準備

以下各節說明如何收集資料表統計資料、中繼資料和安全性設定的相關資訊，協助您將資料倉儲從 Apache Hive 遷移至 BigQuery。

### 收集來源資料表資訊

收集來源 Hive 資料表的相關資訊，例如列數、欄數、欄資料類型、大小、資料輸入格式和位置。這項資訊在遷移程序中非常實用，也有助於驗證資料遷移作業。如果您在名為 `corp` 的資料庫中有名為 `employees` 的 Hive 資料表，請使用下列指令收集資料表資訊：

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

### 轉換來源資料表格式

Hive 支援的部分格式無法直接擷取至 BigQuery。

Hive 支援以下列格式儲存資料：

* 文字檔
* RC 檔案
* 序列檔案
* Avro 檔案
* ORC 檔案
* Parquet 檔案

BigQuery 支援從 Cloud Storage 載入下列檔案格式的資料：

* CSV
* JSON (以換行符號分隔)
* Avro
* ORC
* Parquet

BigQuery 可以直接載入 Avro、ORC 和 Parquet 格式的資料檔案，不需要結構定義檔。如果文字檔案不是 CSV 或 JSON (以換行符號分隔) 格式，您可以將資料複製到 Avro 格式的 Hive 資料表，也可以將資料表結構定義轉換為 BigQuery [JSON 結構定義](https://docs.cloud.google.com/bigquery/docs/schemas?hl=zh-tw)，以便在擷取時提供。

### 收集 Hive 存取控管設定

Hive 和 BigQuery 的存取控管機制不同。收集所有 Hive 存取權控管設定，例如角色、群組、成員，以及授予的權限。在 BigQuery 中，針對每個資料集繪製安全防護模型，並實作精細的存取控制清單。舉例來說，Hive 使用者可以對應至 [Google 帳戶](https://docs.cloud.google.com/iam/docs/principals-overview?hl=zh-tw#google-account)，而 HDFS 群組可以對應至 [Google 群組](https://docs.cloud.google.com/iam/docs/overview?hl=zh-tw#google_group)。您可以在資料集層級設定存取權。使用下列指令，在 Hive 中收集存取控管設定：

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

在 Hive 中，只要具備必要權限，即可直接存取資料表背後的 HDFS 檔案。在標準 BigQuery 資料表中，資料載入資料表後，就會儲存在 BigQuery 儲存空間。您可以使用 BigQuery Storage Read API 讀取資料，但系統仍會強制執行所有 IAM、資料列和資料欄層級的安全措施。如果您使用 BigQuery 外部資料表查詢 Cloud Storage 中的資料，存取 Cloud Storage 的權限也由 IAM 控制。

您可以建立 [BigLake 資料表](https://docs.cloud.google.com/bigquery/docs/biglake-quickstart?hl=zh-tw)，使用[連接器](https://docs.cloud.google.com/bigquery/docs/biglake-quickstart?hl=zh-tw#query-biglake-table-using-connectors)以 Apache Spark、Trino 或 Hive 查詢資料。BigQuery Storage API 會針對 Cloud Storage 或 BigQuery 中的所有 BigLake 資料表，強制執行列層級和欄層級的治理政策。

## 資料遷移

將 Hive 資料從地端部署或其他雲端來源叢集遷移至 BigQuery 的步驟如下：

1. 將資料從來源叢集複製到 Cloud Storage
2. 將資料從 Cloud Storage 載入 BigQuery

以下各節將說明如何遷移 Hive 資料、驗證遷移的資料，以及處理持續擷取的資料遷移作業。這些範例是為非 ACID 資料表編寫。

### 分割資料欄資料

在 Hive 中，分區資料表中的資料會儲存在目錄結構中。資料表中的每個分區都與特定分區資料欄值相關聯。資料檔案本身不含任何分割欄的資料。使用 `SHOW PARTITIONS` 指令列出分區資料表中的不同分區。

以下範例顯示來源 Hive 資料表是依據 `joining_date` 和 `department` 資料欄分區。這個資料表下的資料檔案不含與這兩欄相關的任何資料。

```
hive> SHOW PARTITIONS corp.employees_partitioned
joining_date="2018-10-01"/department="HR"
joining_date="2018-10-01"/department="Analyst"
joining_date="2018-11-01"/department="HR"
```

如要複製這些資料欄，其中一種方法是先將分區資料表轉換為非分區資料表，再載入至 BigQuery：

1. 建立結構定義與分區資料表類似的非分區資料表。
2. 從來源分區資料表將資料載入非分區資料表。
3. 將暫存非分區資料表下的這些資料檔案複製到 Cloud Storage。
4. 使用 `bq load` 指令將資料載入 BigQuery，並提供 `TIMESTAMP` 或 `DATE` 類型分區資料欄的名稱 (如有)，做為 `time_partitioning_field` 引數。

### 將資料複製到 Cloud Storage

資料遷移的第一步是將資料複製到 Cloud Storage。
使用 [Hadoop DistCp](https://hadoop.apache.org/docs/current/hadoop-distcp/DistCp.html) 將資料從地端部署或其他雲端叢集複製到 Cloud Storage。將資料儲存在與資料集相同的區域或多區域值區中，然後將資料儲存在 BigQuery 中。舉例來說，如果您想使用位於東京區域的現有 BigQuery 資料集做為目的地，就必須選擇東京的 Cloud Storage 單一區域 bucket 來存放資料。

選取 Cloud Storage bucket 位置後，您可以使用下列指令列出 `employees` Hive 資料表位置的所有資料檔案：

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

請注意，您必須依據[資料儲存定價](https://cloud.google.com/storage/pricing?hl=zh-tw#storage-pricing)，支付在 Cloud Storage 中儲存資料的費用。

暫存目錄可能包含為查詢工作建立的中繼檔案。執行 `bq load` 指令前，請務必刪除所有這類目錄。

### 正在載入資料

BigQuery 支援從 Cloud Storage [批次載入資料](https://docs.cloud.google.com/bigquery/docs/batch-loading-data?hl=zh-tw)，格式不限。建立載入工作前，請先確認要載入資料的 BigQuery[資料集](https://docs.cloud.google.com/bigquery/docs/datasets?hl=zh-tw)存在。

下列指令會顯示從 Hive 複製的非 ACID 資料表資料：

```
> gcloud storage ls gs://hive_data/corp/employees/
gs://hive-migration/corp/employees/
gs://hive-migration/corp/employees/000000_0
gs://hive-migration/corp/employees/000001_0
gs://hive-migration/corp/employees/000002_0
```

如要將 Hive 資料載入 BigQuery，請使用 [`bq load` 指令](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_load)。您可以在網址中使用萬用字元 \*，從共用物件前置字元的多個檔案載入資料。舉例來說，使用下列指令載入共用 `gs://hive_data/corp/employees/` 前置字串的所有檔案：

```
bq load --source_format=AVRO corp.employees gs://hive_data/corp/employees/*
```

由於工作可能需要長時間才能完成，您可以將 `--sync` 旗標設為 `False`，以非同步執行工作。執行 `bq load` 指令會輸出所建立載入工作的工作 ID，因此您可以使用此指令輪詢工作狀態。這項資料包括工作類型、工作狀態，以及執行該工作的使用者等詳細資料。

使用各自的工作 ID 輪詢每個載入工作狀態，並檢查是否有任何工作因錯誤而失敗。如果發生失敗情況，BigQuery 會在將資料載入資料表時，採用「全有或全無」方法。您可以嘗試解決錯誤，然後安全地重新建立其他載入工作。詳情請參閱「[排解錯誤](https://docs.cloud.google.com/bigquery/troubleshooting-errors?hl=zh-tw)」。

請確認您有足夠的載入工作[配額](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#load_jobs) (以資料表和專案為單位)。如果超出配額，載入工作就會失敗，並傳回 `quotaExceeded` 錯誤。

請注意，從 Cloud Storage 將資料載入 BigQuery 時，您不必支付載入作業的費用。資料載入至 BigQuery 後，將適用 BigQuery 的[儲存空間定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#storage)。載入工作順利完成後，您可以刪除 Cloud Storage 中剩餘的檔案，避免因儲存多餘資料而產生費用。

### 驗證

成功載入資料後，您可以比較 [Hive 和 BigQuery 資料表中的資料列數](#collect_source_table_information)，驗證遷移的資料。查看[資料表資訊](https://docs.cloud.google.com/bigquery/docs/tables?hl=zh-tw#get_information_about_tables)，取得 BigQuery 資料表的詳細資料，例如資料列數、資料欄數、分區欄位或叢集欄位。如要進行額外驗證，請考慮使用[資料驗證工具](https://github.com/GoogleCloudPlatform/professional-services-data-validator)。

### 連續擷取

如果持續將資料擷取至 Hive 資料表，請先執行初始遷移作業，然後只將遞增資料變更內容遷移至 BigQuery。您通常會建立重複執行的指令碼，以便尋找及載入新資料。方法有很多種，以下各節將說明其中一種做法。

您可以在 [Cloud SQL](https://docs.cloud.google.com/sql/docs/mysql?hl=zh-tw) 資料庫資料表中追蹤遷移進度，以下各節會將該資料表稱為追蹤資料表。第一次執行遷移作業時，請將進度儲存在追蹤表格中。在後續執行遷移作業時，請使用追蹤資料表資訊，偵測是否有任何額外資料已擷取，並可遷移至 BigQuery。

選取 `INT64`、`TIMESTAMP` 或 `DATE` 類型的 ID 欄，以區分增量資料。這稱為遞增資料欄。

下表是沒有分區的資料表範例，其漸進式資料欄使用 `TIMESTAMP` 型別：

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

下表是依據 `DATE` 型別資料欄 `partition_column` 分區的資料表範例。每個分區都有整數型別的遞增資料欄 `int_identifier`。

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

以下各節將說明如何遷移 Hive 資料，並根據資料是否經過分區，以及是否包含遞增資料欄，提供不同的遷移方式。

#### 沒有遞增資料欄的非分區資料表

假設 Hive 中沒有檔案壓縮作業，Hive 會在擷取新資料時建立新的資料檔案。第一次執行時，請將檔案清單儲存在追蹤資料表中，然後將這些檔案複製到 Cloud Storage 並載入 BigQuery，完成 Hive 資料表的初始遷移作業。

```
> hdfs dfs -ls hdfs://demo_cluster/user/hive/warehouse/corp/employees
Found 3 items
hdfs://demo_cluster/user/hive/warehouse/corp/employees/000000_0
hdfs://demo_cluster/user/hive/warehouse/corp/employees/000001_0
hdfs://demo_cluster/user/hive/warehouse/corp/employees/000002_0
```

完成初始遷移後，部分資料會擷取至 Hive。您只需要將這項增量資料遷移至 BigQuery。在後續的遷移作業中，請再次列出資料檔案，並與追蹤表格中的資訊進行比較，找出尚未遷移的新資料檔案。

```
> hdfs dfs -ls hdfs://demo_cluster/user/hive/warehouse/corp/employees
Found 5 items
hdfs://demo_cluster/user/hive/warehouse/corp/employees/000000_0
hdfs://demo_cluster/user/hive/warehouse/corp/employees/000001_0
hdfs://demo_cluster/user/hive/warehouse/corp/employees/000002_0
hdfs://demo_cluster/user/hive/warehouse/corp/employees/000003_0
hdfs://demo_cluster/user/hive/warehouse/corp/employees/000004_0
```

在本例中，表格位置有兩個新檔案。如要遷移資料，請將這些新資料檔案複製到 Cloud Storage，然後載入現有的 BigQuery 資料表。

#### 具有漸進式資料欄的非分區資料表

在這種情況下，您可以使用遞增資料欄的最大值，判斷是否新增任何資料。執行初始遷移作業時，請查詢 Hive 資料表，擷取遞增資料欄的最大值，並將該值儲存在追蹤資料表中：

```
hive> SELECT MAX(timestamp_identifier) FROM corp.employees;
2018-12-31 22:15:04
```

在後續的遷移作業中，請再次重複相同的查詢，擷取遞增資料欄的目前最大值，並與追蹤資料表中的先前最大值進行比較，檢查是否有遞增資料：

```
hive> SELECT MAX(timestamp_identifier) FROM corp.employees;
2019-01-04 07:21:16
```

如果目前最大值大於先前最大值，表示增量資料已如範例所示，擷取至 Hive 資料表。如要遷移累加資料，請建立暫存資料表，並只將累加資料載入其中。

```
hive> CREATE TABLE stage_employees LIKE corp.employees;
hive> INSERT INTO TABLE stage_employees SELECT * FROM corp.employees WHERE timestamp_identifier>"2018-12-31 22:15:04" and timestamp_identifier<="2019-01-04 07:21:16"
```

列出 HDFS 資料檔案、將檔案複製到 Cloud Storage，然後載入現有的 BigQuery 資料表，即可遷移暫存資料表。

#### 沒有漸進式資料欄的分區資料表

將資料擷取至分區資料表時，可能會建立新分區、將遞增資料附加至現有分區，或同時執行這兩項作業。在這種情況下，您可以找出更新的分區，但由於沒有可供區別的遞增資料欄，因此無法輕易找出這些現有分區新增的資料。另一個選項是擷取及維護 HDFS 快照，但擷取快照會造成 Hive 效能問題，因此通常會停用這項功能。

首次遷移資料表時，請執行 `SHOW PARTITIONS` 指令，並將不同分區的相關資訊儲存在追蹤資料表中。

```
hive> SHOW PARTITIONS corp.employees
partition_column=2018-10-01
partition_column=2018-11-01
```

下列輸出內容顯示資料表 `employees` 有兩個分區。下表提供簡化版的追蹤表，說明如何儲存這項資訊。

| **partition\_information** | **file\_path** | **gcs\_copy\_status** | **gcs\_file\_path** | **bq\_job\_id** | **...** |
| --- | --- | --- | --- | --- | --- |
| partition\_column =2018-10-01 |  |  |  |  |  |
| partition\_column =2018-11-01 |  |  |  |  |  |

在後續的遷移作業中，再次執行 `SHOW PARTITIONS` 指令，列出所有分區，並與追蹤資料表中的分區資訊進行比較，檢查是否有任何尚未遷移的新分區。

```
hive> SHOW PARTITIONS corp.employees
partition_column=2018-10-01
partition_column=2018-11-01
partition_column=2018-12-01
partition_column=2019-01-01
```

如果系統識別出任何新分區 (如範例所示)，請建立暫存資料表，並只將新分區從來源資料表載入其中。將檔案複製到 Cloud Storage，然後載入現有的 BigQuery 資料表，即可遷移暫存資料表。

#### 具有累加資料欄的分區資料表

在此情境中，Hive 資料表會進行分區，且每個分區中都有遞增資料欄。系統會根據這個資料欄的值，持續擷取遞增資料。如上一節所述，您可以在這裡遷移新分區，也可以遷移已擷取至現有分區的累加資料。

首次遷移資料表時，請將每個分區的遞增資料欄最小值和最大值，連同追蹤資料表中的資料表分區資訊一併儲存。

```
hive> SHOW PARTITIONS corp.employees
partition_column=2018-10-01
partition_column=2018-11-01

hive> SELECT MIN(int_identifier),MAX(int_identifier) FROM corp.employees WHERE partition_column="2018-10-01";
1 1000

hive> SELECT MIN(int_identifier),MAX(int_identifier) FROM corp.employees
```