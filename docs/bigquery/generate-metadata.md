Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 生成翻譯和評估的中繼資料

**預覽**

這項產品適用《[服務專屬條款](https://docs.cloud.google.com/terms/service-terms?hl=zh-tw#1)》中「一般服務條款」一節的《正式發布前產品條款》。正式發布前的產品是按照「原樣」提供，支援範圍可能有限。詳情請參閱[推出階段說明](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages)。

本文說明如何使用 `dwh-migration-dumper` 指令列擷取工具建立中繼資料和查詢記錄檔。中繼資料檔案會說明來源系統中的 SQL 物件。

BigQuery 遷移服務會使用這項資訊，將來源系統方言的 SQL 指令碼翻譯成 GoogleSQL，並提升翻譯品質。

BigQuery 遷移評估會使用中繼資料檔案和查詢記錄檔分析現有資料倉儲，協助評估將資料倉儲遷移至 BigQuery 的工作量。

## 總覽

您可以使用 `dwh-migration-dumper` 工具，從要遷移至 BigQuery 的資料庫平台擷取中繼資料資訊。雖然翻譯時不一定要使用擷取工具，但 BigQuery 遷移評估需要使用這項工具，因此我們強烈建議您在所有遷移作業中使用這項工具。

詳情請參閱「[建立中繼資料檔案](https://docs.cloud.google.com/bigquery/docs/batch-sql-translator?hl=zh-tw#create_metadata_files)」。

您可以使用 `dwh-migration-dumper` 工具，從下列資料庫平台擷取中繼資料：

* Teradata
* Amazon Redshift
* Apache Hive
* Apache Impala
* Apache Spark
* Azure Synapse
* Greenplum
* SQL Server
* IBM Netezza
* Oracle
* PostgreSQL
* Snowflake
* Trino 或 PrestoSQL
* Vertica
* BigQuery

您也可以從大多數資料庫中擷取查詢記錄。

`dwh-migration-dumper` 工具會查詢系統資料表，收集與使用者和系統資料庫相關的資料定義語言 (DDL) 陳述式。不會查詢使用者資料庫的內容。這項工具會將系統資料表中的中繼資料資訊儲存為 CSV 檔案，然後將這些檔案壓縮成單一封裝檔。然後，在您上傳翻譯或評估用的來源檔案時，將這個 ZIP 檔案上傳至 Cloud Storage。

使用查詢記錄選項時，`dwh-migration-dumper` 工具會查詢系統資料表，找出與使用者和系統資料庫相關的 DDL 陳述式和查詢記錄。這些檔案會以 CSV 或 YAML 格式儲存至子目錄，然後封裝成 ZIP 檔案。系統絕不會查詢使用者資料庫的內容。目前 BigQuery 遷移評估需要個別的 CSV、YAML 和文字檔案 (查詢記錄)，因此請從查詢記錄 ZIP 檔案解壓縮所有檔案，並上傳以進行評估。

`dwh-migration-dumper` 工具可在 Windows、macOS 和 Linux 上執行。

`dwh-migration-dumper` 工具是依據 [Apache 2 授權](https://github.com/google/dwh-migration-tools/blob/main/LICENSE)提供。

如果您選擇不使用 `dwh-migration-dumper` 工具進行轉譯，可以手動提供中繼資料檔案，方法是將來源系統中 SQL 物件的資料定義語言 (DDL) 陳述式收集到個別文字檔中。

使用 BigQuery 遷移評估工具進行遷移評估時，必須提供使用該工具擷取的中繼資料和查詢記錄。

## 法規遵循規定

我們提供已編譯的 `dwh-migration-dumper` 工具二進位檔，方便您使用。如要稽核工具，確保符合法規遵循規定，可以查看[`dwh-migration-dumper` 工具 GitHub 存放區](https://github.com/google/dwh-migration-tools/tree/main/dumper)的原始碼，並編譯自己的二進位檔。

## 必要條件

### 安裝 Java

您打算執行 `dwh-migration-dumper` 工具的伺服器必須安裝 Java 8 以上版本。如果沒有，請從 [Java 下載頁面](https://www.java.com/download/)下載並安裝 Java。

### 所需權限

您指定用來將 `dwh-migration-dumper` 工具連結至來源系統的使用者帳戶，必須具備從該系統讀取中繼資料的權限。確認這個帳戶具有適當的角色成員資格，可查詢平台可用的中繼資料資源。舉例來說，`INFORMATION_SCHEMA` 是多個平台通用的中繼資料資源。

## 安裝 `dwh-migration-dumper` 工具

如要安裝 `dwh-migration-dumper` 工具，請按照下列步驟操作：

1. 在要執行 `dwh-migration-dumper` 工具的機器上，從 [`dwh-migration-dumper` 工具 GitHub 存放區](https://github.com/google/dwh-migration-tools/releases/latest)下載 zip 檔案。
2. 如要驗證 `dwh-migration-dumper` 工具的 ZIP 檔案，請下載 [`SHA256SUMS.txt` 檔案](https://github.com/google/dwh-migration-tools/releases/latest/download/SHA256SUMS.txt)，然後執行下列指令：

   ### Bash

   ```
   sha256sum --check SHA256SUMS.txt
   ```

   如果驗證失敗，請參閱「[疑難排解](#corrupted_zip_file)」。

   ### Windows PowerShell

   ```
   (Get-FileHash RELEASE_ZIP_FILENAME).Hash -eq ((Get-Content SHA256SUMS.txt) -Split " ")[0]
   ```

   將 `RELEASE_ZIP_FILENAME` 替換為 `dwh-migration-dumper` 指令列擷取工具版本的已下載 zip 檔案名稱，例如 `dwh-migration-tools-v1.0.52.zip`。

   `True` 結果會確認總和檢查碼驗證是否成功。

   `False` 結果表示驗證錯誤。請確認檢查碼和 zip 檔案是從相同發布版本下載，並放在相同目錄中。
3. 將 ZIP 檔案解壓縮，解壓縮 ZIP 檔案後建立的資料夾中，`/bin` 子目錄內會包含解壓縮工具二進位檔。
4. 更新 `PATH` 環境變數，加入擷取工具的安裝路徑。

## 執行 `dwh-migration-dumper` 工具

`dwh-migration-dumper` 工具使用下列格式：

```
dwh-migration-dumper [FLAGS]
```

執行 `dwh-migration-dumper` 工具會在工作目錄中建立名為 `dwh-migration-<source platform>-metadata.zip` 的輸出檔案，例如 `dwh-migration-teradata-metadata.zip`。

**提示：** 使用 Windows PowerShell 時，請以雙引號括住標記，例如 `dwh-migration-dumper "-Dteradata-logs.utility-logs-table=historicdb.ArchivedUtilityLogs"`。

請按照下列操作說明，為來源平台執行 `dwh-migration-dumper` 工具。

### Teradata

如要允許 `dwh-migration-dumper` 工具連線至 Teradata，請從 Teradata 的[下載頁面](https://downloads.teradata.com/download/connectivity/jdbc-driver)下載 JDBC 驅動程式。

下表說明使用擷取工具擷取 Teradata 中繼資料和查詢記錄時，常用的旗標。如要瞭解所有支援的旗標，請參閱[通用旗標](#global_flags)。

| **名稱** | **預設值** | **說明** | **必要** |
| --- | --- | --- | --- |
| `--assessment` |  | 產生資料庫記錄或擷取中繼資料時，開啟評估模式。 使用 `dwh-migration-dumper` 工具擷取中繼資料時，該工具會產生 BigQuery 遷移評估所需的統計資料。用於查詢記錄時，這個指令會擷取額外資料欄，以評估 BigQuery 遷移作業。 | 用於執行評估時必須提供，用於翻譯時則不必。 |
| `--connector` |  | 要使用的連接器名稱，在此情況下，中繼資料為 **teradata**，查詢記錄則為 **teradata-logs**。 | 是 |
| `--database` |  | 以半形逗號分隔的資料庫清單，視 Teradata 伺服器設定而定，資料庫名稱可能區分大小寫。  如果這個旗標與 `teradata` 連接器一併使用，`dwh-migration-dumper` 工具會依據提供的資料庫清單，篩選中繼資料表和檢視區塊。例外狀況是 `DatabasesV` 和 `RoleMembersV` 檢視畫面，`dwh-migration-dumper` 工具會從這些檢視畫面中擷取資料庫和使用者，不會依資料庫名稱篩選。  這個旗標無法與 `teradata-logs` 連接器搭配使用。系統一律會擷取所有資料庫的查詢記錄。 | 否 |
| `--driver` |  | 要用於這個連線的驅動程式 JAR 檔案的絕對或相對路徑。您可以指定多個驅動程式 JAR 檔案，並以半形逗號分隔。 | 是 |
| `--host` | localhost | 資料庫伺服器的主機名稱或 IP 位址。 | 否 |
| `--password` |  | 資料庫連線要使用的密碼。 | 如未指定，擷取工具會使用安全提示要求這項資訊。 |
| `--port` | 1025 | 資料庫伺服器的通訊埠。 | 否 |
| `--user` |  | 資料庫連線要使用的使用者名稱。 | 是 |
| `--query-log-alternates` |  | 僅適用於 `teradata-logs` 連接器。  如要從其他位置擷取查詢記錄，建議改用 `-Dteradata-logs.query-logs-table` 和 `-Dteradata-logs.sql-logs-table` 標記。  根據預設，查詢記錄會從 `dbc.DBQLogTbl` 和 `dbc.DBQLSQLTbl` 資料表擷取。如果您使用 `--assessment` 旗標，系統會從檢視區塊 `dbc.QryLogV` 和資料表 `dbc.DBQLSQLTbl` 擷取查詢記錄。如要從其他位置擷取查詢記錄，可以使用 `--query-log-alternates` 旗標指定資料表或檢視的完整名稱。第一個參數會參照 `dbc.DBQLogTbl` 資料表的替代項目，第二個參數則會參照 `dbc.DBQLSQLTbl` 資料表的替代項目。這兩個參數都必須提供。   如果兩個資料表都有 `DATE` 類型的索引欄，可以使用 `-Dteradata-logs.log-date-column` 旗標提升擷取效能。  範例： `--query-log-alternates historicdb.ArchivedQryLogV,historicdb.ArchivedDBQLSqlTbl` | 否 |
| `-Dteradata.tmode` |  | 連線的交易模式。支援的值如下：   * `ANSI`：ANSI 模式。這是預設模式 (如未指定旗標) * `TERA`：Teradata 交易模式 (BTET) * `DEFAULT`：使用資料庫伺服器上設定的預設交易模式 * `NONE`：未設定連線模式   範例 (Bash)：  `-Dteradata.tmode=TERA`  範例 (Windows PowerShell)：  `"-Dteradata.tmode=TERA"` | 否 |
| `-Dteradata-logs.log-date-column` |  | 僅適用於 `teradata-logs` 連接器。  如要提升由 `-Dteradata-logs.query-logs-table` 和 `-Dteradata-logs.sql-logs-table` 旗標指定的聯結資料表效能，可以在 `JOIN` 條件中加入 `DATE` 類型的額外資料欄。這個資料欄必須在兩個資料表中定義，且必須是分區主索引的一部分。  範例 (Bash)：  `-Dteradata-logs.log-date-column=ArchiveLogDate`  範例 (Windows PowerShell)：  `"-Dteradata-logs.log-date-column=ArchiveLogDate"` | 否 |
| `-Dteradata-logs.query-logs-table` |  | 僅適用於 `teradata-logs` 連接器。  根據預設，查詢記錄會從 `dbc.DBQLogTbl` 表格擷取。如果您使用 `--assessment` 旗標，系統會從檢視區塊 `dbc.QryLogV` 擷取查詢記錄。如要從其他位置擷取查詢記錄，可以使用這個標記指定資料表或檢視的完整名稱。  請參閱 `-Dteradata-logs.log-date-column` 旗標，瞭解如何提升擷取效能。  範例 (Bash)：  `-Dteradata-logs.query-logs-table=historicdb.ArchivedQryLogV`  範例 (Windows PowerShell)：  `"-Dteradata-logs.query-logs-table=historicdb.ArchivedQryLogV"` | 否 |
| `-Dteradata-logs.sql-logs-table` |  | 僅適用於 `teradata-logs` 連接器。  根據預設，系統會從 `dbc.DBQLSqlTbl` 資料表擷取含有 SQL 文字的查詢記錄。如需從替代位置擷取這些檔案，您可以使用這個標記指定表格或檢視的完整名稱。  請參閱 `-Dteradata-logs.log-date-column` 旗標，瞭解如何提升擷取效能。  範例 (Bash)：  `-Dteradata-logs.sql-logs-table=historicdb.ArchivedDBQLSqlTbl`  範例 (Windows PowerShell)：  `"-Dteradata-logs.sql-logs-table=historicdb.ArchivedDBQLSqlTbl"` | 否 |
| `-Dteradata-logs.utility-logs-table` |  | 僅適用於 `teradata-logs` 連接器。  根據預設，公用程式記錄檔會從表格中擷取 `dbc.DBQLUtilityTbl`。如要從其他位置擷取公用程式記錄，可以使用 `-Dteradata-logs.utility-logs-table` 標記指定資料表的完整名稱。  範例 (Bash)：  `-Dteradata-logs.utility-logs-table=historicdb.ArchivedUtilityLogs`  範例 (Windows PowerShell)：  `"-Dteradata-logs.utility-logs-table=historicdb.ArchivedUtilityLogs"` | 否 |
| `-Dteradata-logs.res-usage-scpu-table` |  | 僅適用於 `teradata-logs` 連接器。  根據預設，SCPU 資源用量記錄會從 `dbc.ResUsageScpu` 資料表擷取。如要從其他位置擷取這些項目，可以使用 `-Dteradata-logs.res-usage-scpu-table` 標記指定資料表的完整名稱。  範例 (Bash)：  `-Dteradata-logs.res-usage-scpu-table=historicdb.ArchivedResUsageScpu`  範例 (Windows PowerShell)：  `"-Dteradata-logs.res-usage-scpu-table=historicdb.ArchivedResUsageScpu"` | 否 |
| `-Dteradata-logs.res-usage-spma-table` |  | 僅適用於 `teradata-logs` 連接器。  根據預設，系統會從 `dbc.ResUsageSpma` 表格中擷取 SPMA 資源用量記錄。如要從其他位置擷取這些記錄，可以使用 `-Dteradata-logs.res-usage-spma-table` 標記指定資料表的完整名稱。  範例 (Bash)：  `-Dteradata-logs.res-usage-spma-table=historicdb.ArchivedResUsageSpma`  範例 (Windows PowerShell)：  `"-Dteradata-logs.res-usage-spma-table=historicdb.ArchivedResUsageSpma"` | 否 |
| `--query-log-start` |  | 要擷取查詢記錄的開始時間 (含此時間)。系統會將值截斷至小時。這個旗標僅適用於 **teradata-logs** 連接器。  範例：`--query-log-start "2023-01-01 14:00:00"` | 否 |
| `--query-log-end` |  | 要擷取查詢記錄的結束時間 (不含)。系統會將值截斷至小時。這個旗標僅適用於 **teradata-logs** 連接器。  範例：`--query-log-end "2023-01-15 22:00:00"` | 否 |
| `-Dteradata.metadata.tablesizev.max-rows` |  | 僅適用於 `teradata` 連接器。  限制從檢視畫面擷取的資料列數量 `TableSizeV`。 資料列會依 `DatabaseName`、`AccountName` 和 `TableName` 欄分組，然後依永久空間大小 (運算式 `SUM(CurrentPerm)`) 遞減排序。接著，系統會擷取指定數量的資料列。  範例 (Bash)：  `-Dteradata.metadata.tablesizev.max-rows=100000`  範例 (Windows PowerShell)：  `"-Dteradata.metadata.tablesizev.max-rows=100000"` | 否 |
| `-Dteradata.metadata.diskspacev.max-rows` |  | 僅適用於 `teradata` 連接器。  限制從檢視畫面擷取的資料列數量 `DiskSpaceV`。 資料列會依永久空間大小 (`CurrentPerm` 欄) 遞減排序，然後擷取指定數量的資料列。  範例 (Bash)：  `-Dteradata.metadata.diskspacev.max-rows=100000`  範例 (Windows PowerShell)：  `"-Dteradata.metadata.diskspacev.max-rows=100000"` | 否 |
| `-Dteradata.metadata.databasesv.users.max-rows` |  | 僅適用於 `teradata` 連接器。  限制代表使用者的資料列數量 (`DBKind='U'`)，這些資料列是從檢視畫面 `DatabasesV` 擷取而來。系統會先依 `PermSpace` 欄以遞減順序排序資料列，然後擷取指定數量的資料列。  範例 (Bash)：  `-Dteradata.metadata.databasesv.users.max-rows=100000`  範例 (Windows PowerShell)：  `"-Dteradata.metadata.databasesv.users.max-rows=100000"` | 否 |
| `-Dteradata.metadata.databasesv.dbs.max-rows` |  | 僅適用於 `teradata` 連接器。  限制代表資料庫的資料列數 (`DBKind='D'`)，這些資料列是從檢視區塊 `DatabasesV` 擷取而來。系統會先依 `PermSpace` 欄以遞減順序排序資料列，然後擷取指定數量的資料列。  範例 (Bash)：  `-Dteradata.metadata.databasesv.dbs.max-rows=100000`  範例 (Windows PowerShell)：  `"-Dteradata.metadata.databasesv.dbs.max-rows=100000"` | 否 |
| `-Dteradata.metadata.max-text-length` |  | 僅適用於 `teradata` 連接器。  從 `TableTextV` 檢視畫面擷取資料時，文字欄的長度上限。如果文字超過定義的上限，系統會將其分割為多列。允許的範圍：介於 5000 到 32000 (含)。  範例 (Bash)：  `-Dteradata.metadata.max-text-length=10000`  範例 (Windows PowerShell)：  `"-Dteradata.metadata.max-text-length=10000"` | 否 |
| `-Dteradata-logs.max-sql-length` |  | 僅適用於 `teradata-logs` 連接器。  `DBQLSqlTbl.SqlTextInfo` 欄的長度上限。 如果查詢文字超過定義的上限，系統會將其分成多列。允許的範圍：介於 5000 到 31000 (含)。  範例 (Bash)：  `-Dteradata-logs.max-sql-length=10000`  範例 (Windows PowerShell)：  `"-Dteradata-logs.max-sql-length=10000"` | 否 |

#### 範例

以下範例說明如何擷取本機主機上兩個 Teradata 資料庫的中繼資料：

```
dwh-migration-dumper \
  --connector teradata \
  --user user \
  --password password \
  --database database1,database2 \
  --driver path/terajdbc4.jar
```

以下範例說明如何擷取本機主機上「評估」的查詢記錄以進行驗證：

```
dwh-migration-dumper \
  --connector teradata-logs \
  --assessment \
  --user user \
  --password password \
  --driver path/terajdbc4.jar
```

#### `dwh-migration-dumper` 工具擷取的資料表和檢視表

使用 `teradata` 連接器時，系統會擷取下列資料表和檢視畫面：

* `DBC.ColumnsV`
* `DBC.DatabasesV`
* `DBC.DBCInfo`
* `DBC.FunctionsV`
* `DBC.IndicesV`
* `DBC.PartitioningConstraintsV`
* `DBC.TablesV`
* `DBC.TableTextV`

使用 `teradata` 連接器和 `--assessment` 旗標時，系統會擷取下列其他資料表和檢視畫面：

* `DBC.All_RI_ChildrenV`
* `DBC.All_RI_ParentsV`
* `DBC.AllTempTablesVX`
* `DBC.DiskSpaceV`
* `DBC.RoleMembersV`
* `DBC.StatsV`
* `DBC.TableSizeV`

使用 `teradata-logs` 連接器時，系統會擷取下列資料表和檢視畫面：

* `DBC.DBQLogTbl` (如果使用 `--assessment` 旗標，則會變更為 `DBC.QryLogV`)
* `DBC.DBQLSqlTbl`

使用 `teradata-logs` 連接器和 `--assessment` 旗標時，系統會擷取下列其他資料表和檢視畫面：

* `DBC.DBQLUtilityTbl`
* `DBC.ResUsageScpu`
* `DBC.ResUsageSpma`

### Redshift

您可以使用下列任一 Amazon Redshift 驗證和授權機制搭配擷取工具：

* 使用者名稱和密碼。
* AWS Identity and Access Management (IAM) 存取金鑰 ID 和私密金鑰。
* AWS IAM 設定檔名稱。

如要使用使用者名稱和密碼進行驗證，請使用 Amazon Redshift 預設的 PostgreSQL JDBC 驅動程式。如要使用 AWS IAM 進行驗證，請使用 Amazon Redshift JDBC 驅動程式，您可以從[下載頁面](https://docs.aws.amazon.com/redshift/latest/mgmt/jdbc20-download-driver.html)下載。

下表說明使用 `dwh-migration-dumper` 工具擷取 Amazon Redshift 中繼資料和查詢記錄時，常用的旗標。如要瞭解所有支援的旗標，請參閱「[全域旗標](#global_flags)」。

| **名稱** | **預設值** | **說明** | **必要** |
| --- | --- | --- | --- |
| `--assessment` |  | 產生資料庫記錄或擷取中繼資料時，開啟評估模式。 用於中繼資料擷取時，會產生 BigQuery 遷移評估所需的必要中繼資料統計資料。用於擷取查詢記錄時，會產生 BigQuery 遷移評估的查詢指標統計資料。 | 以評估模式執行時為必要項目，翻譯時則不需提供。 |
| `--connector` |  | 要使用的連接器名稱，在此案例中為中繼資料的 **redshift** 或查詢記錄的 **redshift-raw-logs**。 | 是 |
| `--database` | 如未指定，Amazon Redshift 會使用 `--user` 值做為預設資料庫名稱。 | 要連線的資料庫名稱。 | 否 |
| `--driver` | 如未指定，Amazon Redshift 會使用預設的 PostgreSQL JDBC 驅動程式。 | 要用於這個連線的驅動程式 JAR 檔案絕對或相對路徑。您可以指定多個驅動程式 JAR 檔案，並以半形逗號分隔。 | 否 |
| `--host` | localhost | 資料庫伺服器的主機名稱或 IP 位址。 | 否 |
| `--iam-accesskeyid` |  | 用於驗證的 AWS IAM 存取金鑰 ID。存取金鑰是由字元組成的字串，如下所示：`AKIAIOSFODNN7EXAMPLE`。  與 `--iam-secretaccesskey` 旗標搭配使用。指定 `--iam-profile` 或 `--password` 旗標時，請勿使用這個旗標。 | 您不必明確提供驗證資訊，但必須透過下列任一方法提供：   * 搭配 `--iam-secretaccesskey` 旗標使用這個旗標。 * 使用 `--iam-profile` 旗標。 * 同時使用 `--password` 和 `--user` 旗標。 |
| `--iam-profile` |  | 用於驗證的 AWS IAM 設定檔。您可以檢查 `$HOME/.aws/credentials` 檔案或執行 `aws configure list-profiles`，擷取要使用的設定檔值。  請勿將此標記與 `--iam-accesskeyid`、`--iam-secretaccesskey` 或 `--password` 標記搭配使用。 | 您不必明確提供驗證資訊，但必須透過下列任一方法提供：   * 使用這個旗標。 * 一併使用 `--iam-accesskeyid` 和 `--iam-secretaccesskey` 旗標。 * 同時使用 `--password` 和 `--user` 旗標。 |
| `--iam-secretaccesskey` |  | 用於驗證的 AWS IAM 私密存取金鑰。存取金鑰是由字元組成的字串，如下所示：`wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY`。  與 `--iam-accesskeyid` 旗標搭配使用。請勿將此旗標與 `--iam-profile` 或 `--password` 旗標搭配使用。 | 您不必明確提供驗證資訊，但必須透過下列任一方法提供：   * 搭配 `--iam-accesskeyid` 旗標使用這個旗標。 * 使用 `--iam-profile` 旗標。 * 同時使用 `--password` 和 `--user` 旗標。 |
| `--password` |  | 資料庫連線要使用的密碼。 請勿將此標記與 `--iam-accesskeyid`、`--iam-secretaccesskey` 或 `--iam-profile` 標記搭配使用。 | 您不必明確提供驗證資訊，但必須透過下列任一方法提供：   * 搭配 `--user` 旗標使用這個旗標。 * 一併使用 `--iam-accesskeyid` 和 `--iam-secretaccesskey` 旗標。 * 使用 `--password` 旗標。 |
| `--port` | 5439 | 資料庫伺服器的通訊埠。 | 否 |
| `--user` |  | 資料庫連線要使用的使用者名稱。 | 是 |
| `--query-log-start` |  | 要擷取查詢記錄的開始時間 (含此時間)。系統會將值截斷至小時。這個旗標僅適用於 **redshift-raw-logs** 連接器。  範例：`--query-log-start "2023-01-01 14:00:00"` | 否 |
| `--query-log-end` |  | 要擷取查詢記錄的結束時間 (不含)。系統會將值截斷至小時。這個旗標僅適用於 **redshift-raw-logs** 連接器。  範例：`--query-log-end "2023-01-15 22:00:00"` | 否 |

#### 範例

以下範例說明如何使用 AWS IAM 金鑰進行驗證，從指定主機上的 Amazon Redshift 資料庫擷取中繼資料：

```
dwh-migration-dumper \
  --connector redshift \
  --database database \
  --driver path/redshift-jdbc42-version.jar \
  --host host.region.redshift.amazonaws.com \
  --iam-accesskeyid access_key_ID \
  --iam-secretaccesskey secret_access-key \
  --user user
```

以下範例說明如何使用使用者名稱和密碼進行驗證，從預設主機上的 Amazon Redshift 資料庫擷取中繼資料：

```
dwh-migration-dumper \
  --connector redshift \
  --database database \
  --password password \
  --user user
```

以下範例說明如何使用 AWS IAM 設定檔進行驗證，從指定主機上的 Amazon Redshift 資料庫擷取中繼資料：

```
dwh-migration-dumper \
  --connector redshift \
  --database database \
  --driver path/redshift-jdbc42-version.jar \
  --host host.region.redshift.amazonaws.com \
  --iam-profile profile \
  --user user \
  --assessment
```

以下範例說明如何使用 AWS IAM 設定檔進行驗證，從指定主機上的 Amazon Redshift 資料庫中，擷取評估的查詢記錄：

```
dwh-migration-dumper \
  --connector redshift-raw-logs \
  --database database \
  --driver path/redshift-jdbc42-version.jar \
  --host 123.456.789.012 \
  --iam-profile profile \
  --user user \
  --assessment
```

#### `dwh-migration-dumper` 工具擷取的資料表和檢視表

使用 `redshift` 連接器時，系統會擷取下列資料表和檢視畫面：

* `SVV_COLUMNS`
* `SVV_EXTERNAL_COLUMNS`
* `SVV_EXTERNAL_DATABASES`
* `SVV_EXTERNAL_PARTITIONS`
* `SVV_EXTERNAL_SCHEMAS`
* `SVV_EXTERNAL_TABLES`
* `SVV_TABLES`
* `SVV_TABLE_INFO`
* `INFORMATION_SCHEMA.COLUMNS`
* `PG_CAST`
* `PG_DATABASE`
* `PG_LANGUAGE`
* `PG_LIBRARY`
* `PG_NAMESPACE`
* `PG_OPERATOR`
* `PG_PROC`
* `PG_TABLE_DEF`
* `PG_TABLES`
* `PG_TYPE`
* `PG_VIEWS`

使用 `redshift` 連接器和 `--assessment` 旗標時，系統會擷取下列其他資料表和檢視畫面：

* `SVV_DISKUSAGE`
* `STV_MV_INFO`
* `STV_WLM_SERVICE_CLASS_CONFIG`
* `STV_WLM_SERVICE_CLASS_STATE`

使用 `redshift-raw-logs` 連接器時，系統會擷取下列資料表和檢視畫面：

* `STL_DDLTEXT`
* `STL_QUERY`
* `STL_QUERYTEXT`
* `PG_USER`

使用 `redshift-raw-logs` 連接器和 `--assessment` 旗標時，系統會擷取下列其他資料表和檢視畫面：

* `STL_QUERY_METRICS`
* `SVL_QUERY_QUEUE_INFO`
* `STL_WLM_QUERY`

如要瞭解 Redshift 中的系統檢視畫面和資料表，請參閱 [Redshift 系統檢視畫面](https://docs.aws.amazon.com/redshift/latest/dg/c_intro_system_views.html)和 [Redshift 系統目錄資料表](https://docs.aws.amazon.com/redshift/latest/dg/c_intro_catalog_views.html)。

### Hive/Impala/Spark 或 Trino/PrestoSQL

`dwh-migration-dumper` 工具僅支援透過 Kerberos 驗證 Apache Hive Metastore。因此，請勿使用 `--user` 和 `--password` 標記，而是使用 `--hive-kerberos-url` 標記提供 Kerberos 驗證詳細資料。

下表說明使用擷取工具擷取 Apache Hive、Impala、Spark、Presto 或 Trino 中繼資料時，常用的標記。如需所有支援的旗標，請參閱[全域旗標](#global_flags)。

| **名稱** | **預設值** | **說明** | **必要** |
| --- | --- | --- | --- |
| `--assessment` |  | 在擷取中繼資料時開啟評估模式。 使用 `dwh-migration-dumper` 工具擷取中繼資料時，該工具會產生 BigQuery 遷移評估所需的必要中繼資料統計資料。 | 這是評估作業的必填項目。Not required for translation. |
| `--connector` |  | 要使用的連接器名稱，在本例中為 **hiveql**。 | 是 |
| `--hive-metastore-dump-partition-metadata` | true | 導致 `dwh-migration-dumper` 工具擷取分割區中繼資料。如果生產環境中繼存放區的分區數量龐大，您可能會想將這個旗標設為 `false`，因為這會影響 Thrift 用戶端效能。這項做法可提升擷取工具的效能，但會導致 BigQuery 端的分割區最佳化作業有些許損失。  請勿將這個旗標與 `--assessment` 旗標搭配使用，否則不會有任何效果。 | 否 |
| `--hive-metastore-version` | 2.3.6 | 執行 `dwh-migration-dumper` 工具時，系統會根據這個旗標的值，選取適當的 [Thrift](https://thrift.apache.org/) 規格，用於與 Apache Hive 伺服器通訊。如果擷取工具沒有適當的 Thrift 規格，就會使用 2.3.6 版的用戶端，並向 `stdout` 發出警告。如果發生這種情況，請[聯絡支援團隊](https://cloud.google.com/support-hub?hl=zh-tw)，並提供您要求的 Apache Hive 版本號碼。 | 否 |
| `--host` | localhost | 資料庫伺服器的主機名稱或 IP 位址。 | 否 |
| `--port` | 9083 | 資料庫伺服器的通訊埠。 | 否 |
| `--hive-kerberos-url` |  | 用於驗證的 Kerberos 主體和主機。 | 如果叢集已啟用 Kerberos 驗證，則必須設定此屬性。 |
| `-Dhiveql.rpc.protection` |  | RPC 保護設定層級。這會決定叢集與 `dwh-migration-dumper` 工具之間，簡易驗證和安全防護層 (SASL) 連線的保護品質 (QOP)。  必須等於叢集上 `/etc/hadoop/conf/core-site.xml` 檔案內的 `hadoop.rpc.protection` 參數值，且為下列其中一個值：   * `authentication` * `integrity` * `privacy`   範例 (Bash)：  `-Dhiveql.rpc.protection=privacy`  範例 (Windows PowerShell)：  `"-Dhiveql.rpc.protection=privacy"` | 如果叢集已啟用 Kerberos 驗證，則必須設定此屬性。 |

#### 範例

以下範例說明如何擷取指定主機上 Hive 2.3.7 資料庫的中繼資料，且不需驗證，並使用替代通訊埠進行連線：

```
dwh-migration-dumper \
  --connector hiveql \
  --hive-metastore-version 2.3.7 \
  --host host \
  --port port
```

如要使用 Kerberos 驗證，請以具備 Hive metastore 讀取權限的使用者身分登入，並產生 Kerberos 票證。然後，使用下列指令產生中繼資料 ZIP 檔案：

```
JAVA_OPTS="-Djavax.security.auth.useSubjectCredsOnly=false" \
  dwh-migration-dumper \
  --connector hiveql \
  --host host \
  --port port \
  --hive-kerberos-url principal/kerberos_host
```

### Azure Synapse 或 Microsoft SQL Server

如要讓「`dwh-migration-dumper`」工具連線至 Azure Synapse 或 Microsoft SQL Server，請從 Microsoft 的[下載頁面](https://docs.microsoft.com/en-us/sql/connect/jdbc/microsoft-jdbc-driver-for-sql-server?view=sql-server-ver15)下載 JDBC 驅動程式。

下表說明使用擷取工具擷取 Azure Synapse 或 Microsoft SQL Server 中繼資料時，常用的旗標。如需所有支援的旗標，請參閱[全域旗標](#global_flags)。

| **名稱** | **預設值** | **說明** | **必要** |
| --- | --- | --- | --- |
| `--connector` |  | 要使用的連接器名稱，在本例中為 **sqlserver**。 | 是 |
| `--database` |  | 要連線的資料庫名稱。 | 是 |
| `--driver` |  | 要用於這個連線的驅動程式 JAR 檔案絕對或相對路徑。您可以指定多個驅動程式 JAR 檔案，並以半形逗號分隔。 | 是 |
| `--host` | localhost | 資料庫伺服器的主機名稱或 IP 位址。 | 否 |
| `--password` |  | 資料庫連線要使用的密碼。 | 是 |
| `--port` | 1433 | 資料庫伺服器的通訊埠。 | 否 |
| `--user` |  | 資料庫連線要使用的使用者名稱。 | 是 |

#### 範例

以下範例說明如何從指定主機上的 Azure Synapse 資料庫擷取中繼資料：

```
dwh-migration-dumper \
  --connector sqlserver \
  --database database \
  --driver path/mssql-jdbc.jar \
  --host server_name.sql.azuresynapse.net \
  --password password \
  --user user
```

### Greenplum

如要允許 `dwh-migration-dumper` 工具連線至 Greenplum，請從 VMware Greenplum 的[下載頁面](https://docs.vmware.com/en/VMware-Greenplum/7/greenplum-database/datadirect-datadirect_jdbc.html)下載 JDBC 驅動程式。

下表說明使用擷取工具擷取 Greenplum 中繼資料時，常用的旗標。如要瞭解所有支援的旗標，請參閱[通用旗標](#global_flags)。

| **名稱** | **預設值** | **說明** | **必要** |
| --- | --- | --- | --- |
| `--connector` |  | 要使用的連接器名稱，在本例中為 **greenplum**。 | 是 |
| `--database` |  | 要連線的資料庫名稱。 | 是 |
| `--driver` |  | 要用於這個連線的驅動程式 JAR 檔案絕對或相對路徑。您可以指定多個驅動程式 JAR 檔案，並以半形逗號分隔。 | 是 |
| `--host` | localhost | 資料庫伺服器的主機名稱或 IP 位址。 | 否 |
| `--password` |  | 資料庫連線要使用的密碼。 | 如未指定，擷取工具會使用安全提示要求這項資訊。 |
| `--port` | 5432 | 資料庫伺服器的通訊埠。 | 否 |
| `--user` |  | 資料庫連線要使用的使用者名稱。 | 是 |

#### 範例

以下範例說明如何擷取指定主機上 Greenplum 資料庫的中繼資料：

```
dwh-migration-dumper \
  --connector greenplum \
  --database database \
  --driver path/greenplum.jar \
  --host host \
  --password password \
  --user user \
```

### Netezza

如要允許 `dwh-migration-dumper` 工具連線至 IBM Netezza，您必須取得 JDBC 驅動程式。通常可以從 IBM Netezza 裝置主機的 `/nz/kit/sbin`
目錄取得驅動程式。如果找不到，請向系統管理員尋求協助，或參閱 IBM Netezza 說明文件中的「[安裝及設定 JDBC](https://www.ibm.com/docs/en/psfa/latest?topic=configuration-installing-configuring-jdbc)」。

下表說明使用擷取工具擷取 IBM Netezza 中繼資料時，常用的旗標。如要瞭解所有支援的旗標，請參閱[通用旗標](#global_flags)。

| **名稱** | **預設值** | **說明** | **必要** |
| --- | --- | --- | --- |
| `--connector` |  | 要使用的連接器名稱，在本例中為 **netezza**。 | 是 |
| `--database` |  | 以半形逗號分隔的資料庫清單，列出要擷取的資料庫。 | 是 |
| `--driver` |  | 要用於這個連線的驅動程式 JAR 檔案絕對或相對路徑。您可以指定多個驅動程式 JAR 檔案，並以半形逗號分隔。 | 是 |
| `--host` | localhost | 資料庫伺服器的主機名稱或 IP 位址。 | 否 |
| `--password` |  | 資料庫連線要使用的密碼。 | 是 |
| `--port` | 5480 | 資料庫伺服器的通訊埠。 | 否 |
| `--user` |  | 資料庫連線要使用的使用者名稱。 | 是 |

#### 範例

以下範例說明如何擷取指定主機上兩個 IBM Netezza 資料庫的中繼資料：

```
dwh-migration-dumper \
  --connector netezza \
  --database database1,database2 \
  --driver path/nzjdbc.jar \
  --host host \
  --password password \
  --user user
```

### PostgreSQL

如要允許 `dwh-migration-dumper` 工具連線至 PostgreSQL，請從 PostgreSQL 的[下載頁面](https://jdbc.postgresql.org/)下載 JDBC 驅動程式。

下表說明使用擷取工具擷取 PostgreSQL 中繼資料時，常用的旗標。如要瞭解所有支援的旗標，請參閱[通用旗標](#global_flags)。

| **名稱** | **預設值** | **說明** | **必要** |
| --- | --- | --- | --- |
| `--connector` |  | 要使用的連接器名稱，在本例中為 **postgresql**。 | 是 |
| `--database` |  | 要連線的資料庫名稱。 | 是 |
| `--driver` |  | 要用於這個連線的驅動程式 JAR 檔案絕對或相對路徑。您可以指定多個驅動程式 JAR 檔案，並以半形逗號分隔。 | 是 |
| `--host` | localhost | 資料庫伺服器的主機名稱或 IP 位址。 | 否 |
| `--password` |  | 資料庫連線要使用的密碼。 | 如未指定，擷取工具會使用安全提示要求這項資訊。 |
| `--port` | 5432 | 資料庫伺服器的通訊埠。 | 否 |
| `--user` |  | 資料庫連線要使用的使用者名稱。 | 是 |

#### 範例

以下範例說明如何擷取指定主機上 PostgreSQL 資料庫的中繼資料：

```
dwh-migration-dumper \
  --connector postgresql \
  --database database \
  --driver path/postgresql-version.jar \
  --host host \
  --password password \
  --user user
```

### Oracle

如要允許 `dwh-migration-dumper` 工具連線至 Oracle，請從 Oracle 的[下載頁面](https://www.oracle.com/database/technologies/appdev/jdbc-downloads.html)下載 JDBC 驅動程式。

下表說明使用擷取工具擷取 Oracle 中繼資料時，常用的旗標。如要瞭解所有支援的旗標，請參閱[通用旗標](#global_flags)。

| **名稱** | **預設值** | **說明** | **必要** |
| --- | --- | --- | --- |
| `--connector` |  | 要使用的連接器名稱，在本例中為 **oracle**。 | 是 |
| `--driver` |  | 要用於這個連線的驅動程式 JAR 檔案絕對或相對路徑。您可以指定多個驅動程式 JAR 檔案，並以半形逗號分隔。 | 是 |
| `--host` | localhost | 資料庫伺服器的主機名稱或 IP 位址。 | 否 |
| `--oracle-service` |  | 連線要使用的 Oracle 服務名稱。 | 不一定，但您必須指定這個旗標或 `--oracle-sid` 旗標。 |
| `--oracle-sid` |  | 連線要使用的 Oracle 系統 ID (SID)。 | 不一定，但您必須指定這個旗標或 `--oracle-service` 旗標。 |
| `--password` |  | 資料庫連線要使用的密碼。 | 如未指定，擷取工具會使用安全提示要求這項資訊。 |
| `--port` | 1521 | 資料庫伺服器的通訊埠。 | 否 |
| `--user` |  | 資料庫連線要使用的使用者名稱。  您指定的使用者必須具備 `SELECT_CATALOG_ROLE` 角色，才能擷取中繼資料。如要查看使用者是否具備必要角色，請對 Oracle 資料庫執行 `select granted_role from user_role_privs;` 查詢。 | 是 |

#### 範例

以下範例說明如何使用 Oracle 服務連線，從指定主機上的 Oracle 資料庫擷取中繼資料：

```
dwh-migration-dumper \
  --connector oracle \
  --driver path/ojdbc8.jar \
  --host host \
  --oracle-service service_name \
  --password password \
  --user user
```

### Snowflake

下表說明使用 `dwh-migration-dumper` 工具擷取 Snowflake 中繼資料時，常用的旗標。如要瞭解所有支援的旗標，請參閱[通用旗標](#global_flags)。

| **名稱** | **預設值** | **說明** | **必要** |
| --- | --- | --- | --- |
| `--assessment` |  | 產生資料庫記錄或擷取中繼資料時，開啟評估模式。使用 `dwh-migration-dumper` 工具擷取中繼資料時，該工具會產生 BigQuery 遷移評估所需的統計資料。用於查詢記錄時，這項工具會擷取額外資料欄，以評估 BigQuery 遷移作業。 | 僅供評估。 |
| `--connector` |  | 要使用的連接器名稱，在本例中為 **snowflake**。 | 是 |
| `--database` |  | 要擷取的資料庫名稱。  一次只能從 Snowflake 擷取一個資料庫的資料。評估模式不允許使用這個標記。 | 僅供翻譯。 |
| `--host` | localhost | 資料庫伺服器的主機名稱或 IP 位址。 | 否 |
| `--private-key-file` |  | 用於驗證的 RSA 私密金鑰路徑。建議使用以金鑰配對為基礎進行驗證的[`SERVICE`](https://docs.snowflake.com/en/user-guide/admin-user-management#types-of-users)使用者。這樣一來，您就能安全存取 Snowflake 資料平台，不必產生多重驗證權杖。 | 否，如果未提供，擷取工具會使用以密碼為基礎的驗證。 |
| `--private-key-password` |  | 建立 RSA 私密金鑰時使用的密碼。 | 否，只有在私密金鑰經過加密時才需要。 |
| `--password` |  | 資料庫連線要使用的密碼。 | 如未指定，擷取工具會使用安全提示要求這項資訊。不過，建議改用金鑰配對驗證。 |
| `--query-log-start` |  | 要擷取查詢記錄的開始時間 (含此時間)。系統會將值截斷至小時。這個旗標僅適用於 `snowflake-logs` 連接器。  範例：`--query-log-start "2023-01-01 14:00:00"` | 否 |
| `--query-log-end` |  | 要擷取查詢記錄的結束時間 (不含)。系統會將值截斷至小時。這個旗標僅適用於 `snowflake-logs` 連接器。  範例：`--query-log-end "2023-01-15 22:00:00"` | 否 |
| `--role` |  | 用於授權的 Snowflake 角色。只有在大型安裝作業中，需要從 `SNOWFLAKE.ACCOUNT_USAGE` 結構定義而非 `INFORMATION_SCHEMA` 取得中繼資料時，才需要指定此項目。詳情請參閱「[使用大型 Snowflake 執行個體](#large-instance)」。 | 否 |
| `--user` |  | 資料庫連線要使用的使用者名稱。 | 是 |
| `--warehouse` |  | 用於處理中繼資料查詢的 Snowflake 倉儲。 | 是 |

#### 範例

以下範例說明如何擷取評估的中繼資料：

```
dwh-migration-dumper \
  --connector snowflake \
  --assessment \
  --host "account.snowflakecomputing.com" \
  --role role \
  --user user \
  --private-key-file private-key-file \
  --private-key-password private-key-password \
  --warehouse warehouse
```

以下範例說明如何擷取本機主機上一般大小的 Snowflake 資料庫中繼資料：

```
dwh-migration-dumper \
  --connector snowflake \
  --database database \
  --user user \
  --private-key-file private-key-file \
  --private-key-password private-key-password \
  --warehouse warehouse
```

下列範例說明如何擷取指定主機上大型 Snowflake 資料庫的中繼資料：

```
dwh-migration-dumper \
  --connector snowflake \
  --database database \
  --host "account.snowflakecomputing.com" \
  --role role \
  --user user \
  --private-key-file private-key-file \
  --private-key-password private-key-password \
  --warehouse warehouse
```

或者，您也可以使用下列範例，透過密碼驗證擷取中繼資料：

```
dwh-migration-dumper \
  --connector snowflake \
  --database database \
  --host "account.snowflakecomputing.com" \
  --password password \
  --user user \
  --warehouse warehouse
```

#### 使用大型 Snowflake 執行個體

`dwh-migration-dumper` 工具會從 Snowflake `INFORMATION_SCHEMA` 讀取中繼資料。不過，從 `INFORMATION_SCHEMA` 擷取的資料量有上限。如果執行擷取工具時收到 `SnowflakeSQLException:
Information schema query returned too much data` 錯誤，請按照下列步驟操作，改為從 `SNOWFLAKE.ACCOUNT_USAGE` 結構定義讀取中繼資料：

1. 在 Snowflake 網頁介面中開啟「Shares」選項。
2. 從「`SNOWFLAKE.ACCOUNT_USAGE`」共用資料夾建立資料庫：

   ```
   -- CREATE DATABASE database FROM SHARE SNOWFLAKE.ACCOUNT_USAGE;
   ```
3. 建立角色：

   ```
   CREATE ROLE role;
   ```
4. 將新資料庫的 `IMPORTED` 權限授予角色：

   ```
   GRANT IMPORTED PRIVILEGES ON DATABASE database TO ROLE role;
   ```
5. 將角色授予要用來執行 `dwh-migration-dumper` 工具的使用者：

   ```
   GRANT ROLE role TO USER user;
   ```

### Vertica

如要允許 `dwh-migration-dumper` 工具連線至 Vertica，請從[下載頁面](https://www.vertica.com/download/vertica/client-drivers/)下載 JDBC 驅動程式。

下表說明使用擷取工具擷取 Vertica 中繼資料時，常用的旗標。如要瞭解所有支援的旗標，請參閱[通用旗標](#global_flags)。

| **名稱** | **預設值** | **說明** | **必要** |
| --- | --- | --- | --- |
| `--connector` |  | 要使用的連接器名稱，在本例中為 **vertica**。 | 是 |
| `--database` |  | 要連線的資料庫名稱。 | 是 |
| `--driver` |  | 要用於這個連線的驅動程式 JAR 檔案絕對或相對路徑。您可以指定多個驅動程式 JAR 檔案，並以半形逗號分隔。 | 是 |
| `--host` | localhost | 資料庫伺服器的主機名稱或 IP 位址。 | 否 |
| `--password` |  | 資料庫連線要使用的密碼。 | 是 |
| `--port` | 5433 | 資料庫伺服器的通訊埠。 | 否 |
| `--user` |  | 資料庫連線要使用的使用者名稱。 | 是 |

#### 範例

以下範例說明如何從本機主機上的 Vertica 資料庫擷取中繼資料：

```
dwh-migration-dumper \
  --driver path/vertica-jdbc.jar \
  --connector vertica \
  --database database
  --user user
  --password password
```

### BigQuery

下表說明使用擷取工具擷取 BigQuery 中繼資料時，常用的旗標。如要瞭解所有支援的旗標，請參閱[通用旗標](#global_flags)。

| **名稱** | **預設值** | **說明** | **必要** |
| --- | --- | --- | --- |
| `--connector` |  | 要使用的連接器名稱，在本例中為 **bigquery**。 | 是 |
| `--database` |  | 要從中擷取中繼資料和查詢記錄的專案清單，並以半形逗號分隔。 | 是 |
| `--schema` |  | 要從中擷取中繼資料和查詢記錄的資料集清單，以半形逗號分隔。 | 是 |

#### 範例

以下範例說明如何從本機主機上的 Vertica 資料庫擷取中繼資料：

```
dwh-migration-dumper \
  --connector bigquery \
  --database PROJECT1, PROJECT2
  --schema DATASET1, DATASET2
```

## 通用標記

下表說明可搭配任何支援來源平台使用的旗標。

| **名稱** | **說明** |
| --- | --- |
| `--connector` | 來源系統的連接器名稱。 |
| `--database` | 實際使用情形依來源系統而異。 |
| `--driver` | 連線至來源系統時要使用的驅動程式 JAR 檔案絕對或相對路徑。您可以指定多個驅動程式 JAR 檔案，並以半形逗號分隔。 |
| `--dry-run`或`-n` | 顯示擷取工具會執行的動作，但不實際執行。 |
| `--help` | 顯示指令列說明。 |
| `--host` | 要連線的資料庫伺服器主機名稱或 IP 位址。 |
| `--jdbcDriverClass` | (選用) 覆寫廠商指定的 JDBC 驅動程式類別名稱。 如果您有自訂 JDBC 用戶端，請使用這個選項。 |
| `--output` | 輸出 ZIP 檔案的路徑。例如：`dir1/dir2/teradata-metadata.zip`。如未指定路徑，輸出檔案會建立在工作目錄中。如果您指定目錄路徑，系統會在指定目錄中建立預設的 zip 檔案名稱。如果目錄不存在，系統會建立該目錄。 如要使用 Cloud Storage，請採用下列格式：  `gs://<BUCKET>/<PATH>`。  如要使用 Google Cloud 憑證進行驗證，請參閱「[進行驗證以使用用戶端程式庫](https://docs.cloud.google.com/docs/authentication/client-libraries?hl=zh-tw)」一文。 |
| `--password` | 資料庫連線要使用的密碼。 |
| `--port` | 資料庫伺服器的通訊埠。 |
| `--save-response-file` | 將指令列標記儲存至 JSON 檔案，方便重複使用。這個檔案名為 `dumper-response-file.json`，會在工作目錄中建立。如要使用回應檔案，請在執行擷取工具時，提供以 `@` 為前置字元的檔案路徑，例如 `dwh-migration-dumper @path/to/dumper-response-file.json`。 |
| `--schema` | 以半形逗號分隔的要擷取結構定義清單。  Oracle 不會區分[結構定義](https://docs.oracle.com/cd/B19306_01/server.102/b14196/schema.htm#CFHHBEGH)和建立結構定義的資料庫使用者，因此您可以使用結構定義名稱或使用者名稱搭配 `--schema` 旗標。例如：`--schema schema1,user2,schema3`。 |
| `--thread-pool-size` | 設定執行緒集區大小，這會影響連線集區大小。 執行 `dwh-migration-dumper` 工具的伺服器核心數，就是執行緒集區的預設大小。  如果擷取工具速度緩慢，或需要更多資源，可以增加使用的執行緒數量。如果跡象顯示伺服器上的其他程序需要更多頻寬，您可以減少使用的執行緒數量。 |
| `--url` | 用於資料庫連線的網址，而非 JDBC 驅動程式產生的 URI。  在大多數情況下，產生的 URI 應已足夠。只有在需要使用來源平台專屬的 JDBC 連線設定，且該設定尚未由這個表格列出的其中一個旗標設定時，才需要覆寫產生的 URI。 |
| `--user` | 資料庫連線要使用的使用者名稱。 |
| `--version` | 顯示產品版本。 |
| `--telemetry` | 收集有關執行作業效能特徵的深入分析資料，例如持續時間、執行次數和資源用量。這項功能預設為啟用。如要停用遙測功能，請將這個旗標設為 `false`。 |

## 疑難排解

本節說明 `dwh-migration-dumper` 工具的一些常見問題和疑難排解技巧。

### 「記憶體不足」錯誤

`dwh-migration-dumper` 工具終端機輸出中的 `java.lang.OutOfMemoryError` 錯誤，通常與處理擷取資料的記憶體不足有關。如要解決這個問題，請增加可用記憶體或減少處理執行緒數量。

您可以匯出 `JAVA_OPTS` 環境變數，藉此增加記憶體上限：

### Linux

```
export JAVA_OPTS="-Xmx4G"
```

### Windows

```
set JAVA_OPTS="-Xmx4G"
```

您可以加入 `--thread-pool-size` 旗標，減少處理執行緒數量 (預設為 32)。這個選項僅支援 `hiveql` 和 `redshift*` 連接器。

```
dwh-migration-dumper --thread-pool-size=1
```

### 處理 `WARN...Task failed` 錯誤

有時您可能會在 `WARN [main]
o.c.a.d.MetadataDumper [MetadataDumper.java:107] Task failed: …` 工具終端機輸出中看到 `dwh-migration-dumper` 錯誤。擷取工具會向來源系統提交多個查詢，並將每個查詢的輸出內容寫入各自的檔案。如果看到這個問題，表示其中一個查詢失敗。不過，如果其中一項查詢失敗，不會影響其他查詢的執行。如果看到多個錯誤，請查看問題詳細資料，看看是否需要修正任何內容，才能正常執行查詢。`WARN`舉例來說，如果您在執行擷取工具時指定的資料庫使用者沒有讀取所有中繼資料的權限，請使用具備正確權限的使用者重試。

### ZIP 檔案已毀損

如要驗證 `dwh-migration-dumper` 工具的 ZIP 檔案，請下載 [`SHA256SUMS.txt` 檔案](https://github.com/google/dwh-migration-tools/releases/latest/download/SHA256SUMS.txt)，然後執行下列指令：

### Bash

```
sha256sum --check SHA256SUMS.txt
```

`OK` 結果會確認總和檢查碼驗證是否成功。其他訊息表示驗證錯誤：

* `FAILED: computed checksum did NOT match`：ZIP 檔案已毀損，必須重新下載。
* `FAILED: listed file could not be read`：找不到 ZIP 檔案版本。請確認檢查碼和 ZIP 檔案是從相同發布版本下載，並放在相同目錄中。

### Windows PowerShell

```
(Get-FileHash RELEASE_ZIP_FILENAME).Hash -eq ((Get-Content SHA256SUMS.txt) -Split " ")[0]
```

將 `RELEASE_ZIP_FILENAME` 替換為 `dwh-migration-dumper` 指令列擷取工具版本的已下載 zip 檔案名稱，例如 `dwh-migration-tools-v1.0.52.zip`。

`True` 結果會確認總和檢查碼驗證是否成功。

`False` 結果表示驗證錯誤。請確認檢查碼和 zip 檔案是從相同發布版本下載，並放在相同目錄中。

### Teradata 查詢記錄擷取作業緩慢

如要提升由 `-Dteradata-logs.query-logs-table` 和 `-Dteradata-logs.sql-logs-table` 旗標指定的聯結資料表效能，可以在 `JOIN` 條件中加入 `DATE` 類型的額外資料欄。這個資料欄必須在兩個資料表中定義，且必須是分區主索引的一部分。如要加入這個資料欄，請使用 `-Dteradata-logs.log-date-column` 旗標。

範例：

### Bash

```
dwh-migration-dumper \
  -Dteradata-logs.query-logs-table=historicdb.ArchivedQryLogV \
  -Dteradata-logs.sql-logs-table=historicdb.ArchivedDBQLSqlTbl \
  -Dteradata-logs.log-date-column=ArchiveLogDate
```

### Windows PowerShell

```
dwh-migration-dumper `
  "-Dteradata-logs.query-logs-table=historicdb.ArchivedQryLogV" `
  "-Dteradata-logs.sql-logs-table=historicdb.ArchivedDBQLSqlTbl" `
  "-Dteradata-logs.log-date-column=ArchiveLogDate"
```

### 超過 Teradata 列大小限制

Teradata 15 的資料列大小上限為 64 KB。如果超過上限，傾印工具會失敗，並顯示以下訊息：
`none
[Error 9804] [SQLState HY000] Response Row size or Constant Row size overflow`

如要解決這項錯誤，請將列數上限延長至 1 MB，或將列分割成多列：

* 安裝並啟用 1MB Perm 和 Response Rows 功能，以及目前的 TTU 軟體。詳情請參閱「[Teradata Database Message 9804](https://docs.teradata.com/r/Teradata-VantageCloud-Lake-Analytics-Database-Messages/Database-Messages/9804)」。
* 使用 `-Dteradata.metadata.max-text-length` 和 `-Dteradata-logs.max-sql-length` 旗標，將長查詢文字分成多列。

下列指令顯示如何使用 `-Dteradata.metadata.max-text-length` 旗標，將長查詢文字分割成多列，每列最多 10000 個半形字元：

### Bash

```
dwh-migration-dumper \
  --connector teradata \
  -Dteradata.metadata.max-text-length=10000
```

### Windows PowerShell

```
dwh-migration-dumper `
  --connector teradata `
  "-Dteradata.metadata.max-text-length=10000"
```

下列指令顯示如何使用 `-Dteradata-logs.max-sql-length` 旗標，將長查詢文字分割成多列，每列最多 10000 個半形字元：

### Bash

```
dwh-migration-dumper \
  --connector teradata-logs \
  -Dteradata-logs.max-sql-length=10000
```

### Windows PowerShell

```
dwh-migration-dumper `
  --connector teradata-logs `
  "-Dteradata-logs.max-sql-length=10000"
```

### Oracle 連線問題

在密碼或主機名稱無效等常見情況下，`dwh-migration-dumper` 工具會顯示有意義的錯誤訊息，說明根本問題。不過在某些情況下，Oracle 伺服器傳回的錯誤訊息可能是一般訊息，難以調查。

其中一個問題是 `IO Error: Got minus one from a read call`。這項錯誤表示已建立與 Oracle 伺服器的連線，但伺服器拒絕接受用戶端並關閉連線。如果伺服器只接受 `TCPS` 連線，通常就會發生這個問題。根據預設，`dwh-migration-dumper` 工具會使用 `TCP` 協定。如要解決這個問題，請覆寫 Oracle JDBC 連線網址。

您可以提供 `url` 旗標，解決這個問題，格式如下：`jdbc:oracle:thin:@tcps://{HOST_NAME}:{PORT}/{ORACLE_SERVICE}`。`oracle-service``host``port`Oracle 伺服器通常使用的 `TCPS` 通訊埠號碼為 `2484`。

傾印器指令範例：

```
  dwh-migration-dumper \
    --connector oracle-stats \
    --url "jdbc:oracle:thin:@tcps://host:port/oracle_service" \
    --assessment \
    --driver "jdbc_driver_path" \
    --user "user" \
    --password
```

除了將連線通訊協定變更為 TCPS 之外，您可能還需要提供驗證 Oracle 伺服器憑證所需的 trustStore SSL 設定。如果缺少 SSL 設定，系統會顯示 `Unable to find valid
certification path` 錯誤訊息。如要解決這個問題，請設定 JAVA\_OPTS 環境變數：

```
  set JAVA_OPTS=-Djavax.net.ssl.trustStore="jks_file_location" -Djavax.net.ssl.trustStoreType=JKS -Djavax.net.ssl.trustStorePassword="password"
```

視 Oracle 伺服器設定而定，您可能也需要提供 keyStore 設定。如要進一步瞭解設定選項，請參閱「[SSL With Oracle JDBC Driver](https://www.oracle.com/docs/tech/wp-oracle-jdbc-thin-ssl.pdf)」。

## 後續步驟

執行 `dwh-migration-dumper` 工具後，請[將輸出內容上傳](https://docs.cloud.google.com/bigquery/docs/batch-sql-translator?hl=zh-tw#upload-files)至 Cloud Storage，並附上用於翻譯的來源檔案。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-06 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-06 (世界標準時間)。"],[],[]]