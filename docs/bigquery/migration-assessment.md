Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 遷移評估

BigQuery 遷移評估功能可讓您規劃及查看現有資料倉儲遷移至 BigQuery 的作業。您可以執行 BigQuery 遷移評估作業，產生報表來評估在 BigQuery 儲存資料的費用、瞭解 BigQuery 如何最佳化現有工作負載來節省成本，並準備遷移計畫，概述將資料倉儲遷移至 BigQuery 所需的時間和精力。

本文說明如何使用 BigQuery 遷移評估，以及查看評估結果的不同方式。本文件適用於熟悉 [Google Cloud 控制台](https://docs.cloud.google.com/bigquery/docs/bigquery-web-ui?hl=zh-tw)和[批次 SQL 轉譯器](https://docs.cloud.google.com/bigquery/docs/batch-sql-translator?hl=zh-tw)的使用者。

## 事前準備

如要準備及執行 BigQuery 遷移評估作業，請按照下列步驟操作：

1. [建立 Cloud Storage bucket](https://docs.cloud.google.com/storage/docs/creating-buckets?hl=zh-tw)。

   **注意：** [請使用 `--pap` 旗標](https://docs.cloud.google.com/sdk/gcloud/reference/storage/buckets/create?hl=zh-tw#FLAGS)，防止 Cloud Storage bucket 資料公開存取。
2. 從資料倉儲[擷取中繼資料和查詢記錄](#extract-metadata-logs)。
3. [將中繼資料和查詢記錄上傳](#upload)至 Cloud Storage bucket。
4. [執行遷移評估](#run-migration-assessment)。
5. [查看數據分析報表](#review_the_data_studio_report)。
6. 選用：[查詢評估結果](#query_assessment_output)，找出詳細或特定的評估資訊。

## 從資料倉儲擷取中繼資料和查詢記錄

您必須同時提供中繼資料和查詢記錄，才能準備評估作業和建議。

如要擷取執行評估所需的中繼資料和查詢記錄，請選取資料倉儲：

### Databricks

**預覽**

這項功能適用《[服務專屬條款](https://docs.cloud.google.com/terms/service-terms?hl=zh-tw#1)》中「一般服務條款」一節的《正式發布前產品條款》。正式發布前功能是依「原樣」提供，支援服務可能受限。
詳情請參閱[推出階段說明](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages)。

如要針對這項功能提供意見或尋求支援，請傳送電子郵件至 [bq-edw-migration-support@google.com](mailto:bq-edw-migration-support@google.com)。

如要擷取 Databricks 評估作業的中繼資料，請先在 Databricks 環境中下載並執行擷取工具。

擷取工具是筆記本，可產生 ZIP 封存檔，其中包含代表多個 Databricks 檢視表的檔案。檢視表包含評估所需的資料。

## 下載擷取工具

Google Cloud 控制台的「Assessment」(評估) 專區會提供筆記本的下載連結。這些檔案會以 ZIP 封存檔的形式提供，其中包含下列內容：

* 擷取筆記本
* 筆記本在擷取程序中執行的公用程式 Python 指令碼。

## 匯入及設定擷取工具

**注意：** 這個步驟需要完整的下載封存檔，因為擷取 Notebook 必須依賴其他檔案，才能完成必要的擷取工作。

1. 使用 Databricks 使用者介面[匯入](https://docs.databricks.com/aws/en/notebooks/notebook-export-import)上一個步驟中的 ZIP 檔案。
2. 匯入後，請開啟擷取筆記本，並完成標示為「Configuration」的所有步驟。

Notebook 的驗證是設定步驟的一部分。筆記本支援兩種 Databricks 驗證方式：

* [服務主體](https://docs.databricks.com/aws/en/admin/users-groups/service-principals)
* [個人存取權杖 (PAT)](https://docs.databricks.com/aws/en/dev-tools/auth/pat)

您必須使用其中一種方法，才能繼續進行下一節。Databricks 認為 PAT 選項已過時，因此建議您盡可能使用服務主體，而非 PAT。

## 取得評估資料

完成所有設定步驟後，即可執行筆記本。擷取筆記本啟用後，請使用「Run all」(全部執行) 選項執行筆記本。

如果系統非常龐大，執行筆記本可能需要一天的時間。以約有 50,000 個資料表的典型系統來說，擷取作業不到一小時即可完成。

## 選用：監控擷取筆記本進度

擷取筆記本會提供記錄，其中包含進度和錯誤資訊，可用於監控。特定 Notebook 執行的最新記錄訊息，包含正在擷取的內容資訊。

由於筆記本執行作業不會在第一個錯誤發生時停止，因此請按照下列兩個步驟查看錯誤：

1. 擷取完成後，請查看摘要，瞭解錯誤計數或其他錯誤指標，例如找到的資料少於預期。如果結果可以接受，則可略過下一個步驟。
2. 複製記錄輸出內容，並儲存至文字檔。

## 完成擷取程序

筆記本完成擷取程序後，您可以點選筆記本最後一個部分的下載按鈕，下載結果。

### Snowflake

### 需求條件

您必須符合下列規定，才能從 Snowflake 擷取中繼資料和查詢記錄：

* 可連線至 Snowflake 執行個體的機器。
* 一個 Google Cloud 帳戶，並具備用於儲存資料的 Cloud Storage bucket。
* 用於儲存結果的空白 BigQuery 資料集。或者，您也可以在使用 Google Cloud 控制台 UI 建立評估工作時，建立 BigQuery 資料集。
* 對資料庫 `Snowflake` 具有 `IMPORTED PRIVILEGES` 存取權的 Snowflake 使用者。建議您建立 [`SERVICE`](https://docs.snowflake.com/en/user-guide/admin-user-management#types-of-users) 使用者，並採用金鑰組驗證機制。這樣一來，您就能安全存取 Snowflake 資料平台，不必產生多重驗證權杖。
  + 如要建立新的服務使用者，請按照[官方 Snowflake 指南](https://docs.snowflake.com/en/user-guide/key-pair-auth#configuring-key-pair-authentication)操作。您必須產生 RSA 金鑰組，並將公開金鑰指派給 Snowflake 使用者。
  + 服務使用者應具備 `ACCOUNTADMIN` 角色，或由帳戶管理員[授予具備資料庫 `Snowflake` `IMPORTED PRIVILEGES` 權限的角色](https://docs.snowflake.com/en/sql-reference/account-usage#enabling-snowflake-database-usage-for-other-roles)。
  + 除了金鑰組驗證，您也可以使用密碼驗證。不過，自 2025 年 8 月起，Snowflake 會對所有使用密碼的使用者強制執行多重驗證。因此，使用我們的擷取工具時，您必須核准多重驗證推播通知。

### 執行 `dwh-migration-dumper` 工具

下載 [`dwh-migration-dumper` 指令列擷取工具](https://github.com/google/dwh-migration-tools/releases/latest)。

下載 [`SHA256SUMS.txt` 檔案](https://github.com/google/dwh-migration-tools/releases/latest/download/SHA256SUMS.txt)，然後執行下列指令，確認 ZIP 檔案正確無誤：

### Bash

```
sha256sum --check SHA256SUMS.txt
```

### Windows PowerShell

```
(Get-FileHash RELEASE_ZIP_FILENAME).Hash -eq ((Get-Content SHA256SUMS.txt) -Split " ")[0]
```

將 `RELEASE_ZIP_FILENAME` 替換為下載的 `dwh-migration-dumper` 指令列擷取工具版本 ZIP 檔案名稱，例如 `dwh-migration-tools-v1.0.52.zip`

`True` 結果確認核對和驗證成功。

`False` 結果表示驗證錯誤。請確認核對和與 ZIP 檔案是從同一個發布版本下載，並放在同一個目錄中。

如要進一步瞭解如何使用 `dwh-migration-dumper` 工具，請參閱[產生中繼資料](https://docs.cloud.google.com/bigquery/docs/generate-metadata?hl=zh-tw)頁面。

使用 `dwh-migration-dumper` 工具，從 Snowflake 資料倉儲中擷取記錄和中繼資料，並儲存為兩個 ZIP 檔案。在可存取來源資料倉儲的機器上執行下列指令，即可產生檔案。

產生中繼資料 ZIP 檔案：

```
dwh-migration-dumper \
  --connector snowflake \
  --host HOST_NAME \
  --user USER_NAME \
  --role ROLE_NAME \
  --warehouse WAREHOUSE \
  --assessment \
  --private-key-file PRIVATE_KEY_PATH \
  --private-key-password PRIVATE_KEY_PASSWORD
```

產生包含查詢記錄的 ZIP 檔案：

```
dwh-migration-dumper \
  --connector snowflake-logs \
  --host HOST_NAME \
  --user USER_NAME \
  --role ROLE_NAME \
  --warehouse WAREHOUSE \
  --query-log-start STARTING_DATE \
  --query-log-end ENDING_DATE \
  --assessment \
  --private-key-file PRIVATE_KEY_PATH \
  --private-key-password PRIVATE_KEY_PASSWORD
```

更改下列內容：

* `HOST_NAME`：Snowflake 執行個體的主機名稱。
* `USER_NAME`：用於資料庫連線的使用者名稱，使用者必須具備[需求條件一節](#requirements-snowflake)詳述的存取權限。
* `PRIVATE_KEY_PATH`：用於驗證的 RSA 私密金鑰路徑。
* `PRIVATE_KEY_PASSWORD`：(選用) 建立 RSA 私密金鑰時使用的密碼。只有在私密金鑰經過加密時，才需要提供這個值。
* `ROLE_NAME`：(選用，但強烈建議) 執行 `dwh-migration-dumper` 工具時的使用者角色，例如 `ACCOUNTADMIN`。如果預設角色具備足夠權限，則可不指定角色，但指定角色可確保工作階段能存取 `SNOWFLAKE.ACCOUNT_USAGE` 結構定義。
* `WAREHOUSE`：用於執行轉儲作業的倉儲。如果您有多個虛擬倉儲，可以指定任何倉儲來執行這項查詢。執行這項查詢時，如果具備[需求條件一節](#requirements-snowflake)詳述的存取權限，系統就會擷取這個帳戶中的所有倉儲構件。
* `STARTING_DATE`：(選用) 用於指出查詢記錄日期範圍的開始日期，格式為 `YYYY-MM-DD`。
* `ENDING_DATE`：(選用) 用於指定查詢記錄日期範圍的結束日期，格式為 `YYYY-MM-DD`。

您也可以產生多個 ZIP 檔案，其中包含不重疊期間的查詢記錄，並提供所有檔案進行評估。

### Hadoop / Cloudera

**預覽**

這項功能適用《[服務專屬條款](https://docs.cloud.google.com/terms/service-terms?hl=zh-tw#1)》中「一般服務條款」一節的《正式發布前產品條款》。正式發布前功能是依「原樣」提供，支援服務可能受限。
詳情請參閱[推出階段說明](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages)。

如要針對這項功能提供意見或尋求支援，請傳送電子郵件至 [bq-edw-migration-support@google.com](mailto:bq-edw-migration-support@google.com)。

**注意：** 從 Cloudera Manager 擷取中繼資料時，會擷取叢集層級的使用率，以及 Apache Hadoop YARN 和 Apache Spark 工作負載，但不會擷取 Apache Hive 資料表結構定義或 SQL 查詢記錄。如果 Cloudera 叢集執行 Hive 工作負載，您也必須完成中繼資料和查詢記錄擷取步驟。詳情請參閱「[在 Cloudera 叢集中使用 Hive](#use-hive-cloudera)」。

### 需求條件

您必須具備下列條件，才能從 Cloudera 擷取中繼資料：

* 可連線至 Cloudera Manager API 的機器。
* 一個 Google Cloud 帳戶，並具備用於儲存資料的 Cloud Storage bucket。
* 用於儲存結果的空白 BigQuery 資料集。或者，您也可以在建立評估工作時建立 BigQuery 資料集。

### 執行 `dwh-migration-dumper` 工具

1. 下載 [`dwh-migration-dumper` 指令列擷取工具](https://github.com/google/dwh-migration-tools/releases/latest)。
2. 下載 [`SHA256SUMS.txt` 檔案](https://github.com/google/dwh-migration-tools/releases/latest/download/SHA256SUMS.txt)。
3. 在指令列環境中，確認 ZIP 檔案正確無誤：

   ```
     sha256sum --check SHA256SUMS.txt
   ```

   如要進一步瞭解如何使用 `dwh-migration-dumper` 工具，請參閱「[產生翻譯和評估作業的中繼資料](https://docs.cloud.google.com/bigquery/docs/generate-metadata?hl=zh-tw)」。
4. 使用 `dwh-migration-dumper` 工具，將中繼資料和效能統計資料擷取至 ZIP 檔案：

   ```
   dwh-migration-dumper \
       --connector cloudera-manager \
       --user USER_NAME \
       --password PASSWORD \
       --url URL_PATH \
       --yarn-application-types "APP_TYPES" \
       --spark-history-service-names "SPARK_HISTORY_SERVICE_NAMES" \
       --pagination-page-size PAGE_SIZE \
       --start-date START_DATE \
       --end-date END_DATE \
       --assessment
   ```

   更改下列內容：

   * `USER_NAME`：要連線至 Cloudera Manager 執行個體的使用者名稱。
   * `PASSWORD`：Cloudera Manager 執行個體的密碼。
   * `URL_PATH`：Cloudera Manager API 的網址路徑，例如 `https://localhost:7183/api/v55/`。
   * `APP_TYPES` (選用)：從叢集傾印的 YARN 應用程式類型，以半形逗號分隔。預設值為 `MAPREDUCE,SPARK,Oozie Launcher`。
   * `SPARK_HISTORY_SERVICE_NAMES` (選用)：Spark 記錄伺服器的服務名稱清單 (以半形逗號分隔)，用於透過 Apache Knox 查詢 Spark 事件記錄，以擷取應用程式中繼資料。如未提供，預設值為 `sparkhistory,spark3history`。
   * `PAGE_SIZE` (選用)：每個 Cloudera 回應的記錄數量。預設值為 `1000`。
   * `START_DATE` (選用)：歷史記錄轉儲的開始日期，採用 ISO 8601 格式，例如 `2025-05-29`。預設值為目前日期前 90 天。
   * `END_DATE` (選用)：歷史記錄轉儲的結束日期，採用 ISO 8601 格式，例如 `2025-05-30`。預設值為目前日期。

#### 擷取 HDFS 儲存空間中繼資料

您也可以在可存取 HDFS NameNode 的節點上，執行 `dwh-migration-dumper` 工具和 `hdfs` 連接器，分析 Apache Hadoop 分散式檔案系統 (HDFS) 的儲存空間用量、目錄結構和檔案權限。

```
dwh-migration-dumper \
    --connector hdfs \
    --host HDFS_NAMENODE_HOST \
    --port 8020 \
    --kerberos-auth-for-hadoop \
    --hadoop-core-site-xml CORE_SITE_XML_PATH \
    --hadoop-hdfs-site-xml HDFS_SITE_XML_PATH \
    --assessment
```

更改下列內容：

* `HDFS_NAMENODE_HOST`：使用中 HDFS NameNode 的主機名稱或 IP 位址。預設通訊埠為 `8020`。
* `CORE_SITE_XML_PATH`：叢集 `core-site.xml` 檔案的路徑。例如：`/etc/hadoop/conf/core-site.xml`。
* `HDFS_SITE_XML_PATH`：叢集 `hdfs-site.xml` 檔案的路徑。例如：`/etc/hadoop/conf/hdfs-site.xml`。

將產生的 `dwh-migration-hdfs-*.zip` 檔案上傳至 Cloudera Manager 中繼資料 ZIP 檔案所在的 Cloud Storage bucket。

#### 在 Cloudera 叢集使用 Oozie

如果您在 Cloudera 叢集中使用 Oozie，可以使用 Oozie 連接器傾印 Oozie 工作記錄。您可以搭配使用 Oozie 與 Kerberos 驗證或基本驗證。

如要進行 Kerberos 驗證，請執行下列指令：

```
kinit
dwh-migration-dumper \
    --connector oozie \
    --url URL_PATH \
    --assessment
```

更改下列內容：

* `URL_PATH` (選用)：Oozie 伺服器網址路徑。如未指定網址路徑，系統會從 `OOZIE_URL` 環境變數擷取。

如要進行基本驗證，請執行下列指令：

```
dwh-migration-dumper \
    --connector oozie \
    --user USER_NAME \
    --password PASSWORD \
    --url URL_PATH \
    --assessment
```

更改下列內容：

* `USER_NAME`：Oozie 使用者的名稱。
* `PASSWORD`：使用者密碼。
* `URL_PATH` (選用)：Oozie 伺服器網址路徑。如未指定網址路徑，系統會從 `OOZIE_URL` 環境變數擷取。

#### 在 Cloudera 叢集中使用 Airflow

如果您在 Cloudera 叢集中使用 Airflow，可以使用 Airflow 連接器傾印 DAG 記錄：

```
dwh-migration-dumper \
    --connector airflow \
    --user USER_NAME \
    --password PASSWORD \
    --url URL \
    --driver "DRIVER_PATH" \
    --start-date START_DATE \
    --end-date END_DATE \
    --assessment
```

更改下列內容：

* `USER_NAME`：Airflow 使用者名稱
* `PASSWORD`：使用者密碼
* `URL`：Airflow 資料庫的 JDBC 字串
* `DRIVER_PATH`：JDBC 驅動程式的路徑
* `START_DATE` (選用)：歷史記錄轉儲的開始日期，採用 ISO 8601 格式
* `END_DATE` (選用)：歷史記錄轉儲的結束日期，採用 ISO 8601 格式

#### 在 Cloudera 叢集中使用 Hive

如果 Cloudera 叢集執行 Hive 工作負載，請完成「Hive」分頁中的步驟，擷取 Hive metastore 結構定義 (`--connector hiveql`) 和查詢記錄 (`hadoop-migration-assessment` 記錄掛鉤)。

### Teradata

### 需求條件

* 連線至來源 Teradata 資料倉儲的機器。遷移評估支援 Teradata 15 以上版本，且僅支援地端部署版本的 Teradata VantageCore。不支援 Teradata VantageCloud。
* 具備 Cloud Storage bucket 的 Google Cloud 帳戶，用於儲存資料
* 用於儲存結果的空白 BigQuery 資料集
* 資料集的讀取的權限，以便查看結果
* 建議：使用擷取工具存取系統資料表時，具備來源資料庫的管理員層級存取權

#### 需求：啟用記錄功能

`dwh-migration-dumper` 工具會擷取三種記錄：查詢記錄、公用程式記錄和資源用量記錄。您必須啟用下列類型的記錄，才能查看更詳盡的深入分析：

* **查詢記錄：**從檢視表 `dbc.QryLogV` 和資料表 `dbc.DBQLSqlTbl` 擷取。[指定 `WITH SQL` 選項](https://docs.teradata.com/r/Enterprise_IntelliFlex_VMware/Database-Administration/Tracking-Query-Behavior-with-Database-Query-Logging-Operational-DBAs/SQL-Statements-to-Control-Logging/WITH-Logging-Options)，啟用記錄功能。
* **公用程式記錄：**從 `dbc.DBQLUtilityTbl` 資料表擷取。[指定 `WITH UTILITYINFO` 選項](https://docs.teradata.com/r/Enterprise_IntelliFlex_VMware/Database-Administration/Tracking-Query-Behavior-with-Database-Query-Logging-Operational-DBAs/SQL-Statements-to-Control-Logging/WITH-Logging-Options)，啟用記錄功能。
* **資源用量記錄：**從 `dbc.ResUsageScpu` 和 `dbc.ResUsageSpma` 資料表擷取。為這兩個資料表[啟用 RSS 記錄功能](https://docs.teradata.com/r/Enterprise_IntelliFlex_VMware/Resource-Usage-Macros-and-Tables/Resource-Usage-and-Procedures/Enabling-RSS-Logging)。

### 執行 `dwh-migration-dumper` 工具

下載 [`dwh-migration-dumper` 工具](https://github.com/google/dwh-migration-tools/releases/latest)。

下載 [`SHA256SUMS.txt` 檔案](https://github.com/google/dwh-migration-tools/releases/latest/download/SHA256SUMS.txt)，然後執行下列指令，確認 ZIP 檔案正確無誤：

### Bash

```
sha256sum --check SHA256SUMS.txt
```

### Windows PowerShell

```
(Get-FileHash RELEASE_ZIP_FILENAME).Hash -eq ((Get-Content SHA256SUMS.txt) -Split " ")[0]
```

將 `RELEASE_ZIP_FILENAME` 替換為下載的 `dwh-migration-dumper` 指令列擷取工具版本 ZIP 檔案名稱，例如 `dwh-migration-tools-v1.0.52.zip`

`True` 結果確認核對和驗證成功。

`False` 結果表示驗證錯誤。請確認核對和與 ZIP 檔案是從同一個發布版本下載，並放在同一個目錄中。

如要進一步瞭解如何設定及使用擷取工具，請參閱「[產生翻譯和評估所需的中繼資料](https://docs.cloud.google.com/bigquery/docs/generate-metadata?hl=zh-tw)」。

使用擷取工具，從 Teradata 資料倉儲中擷取記錄和中繼資料，並儲存為兩個 ZIP 檔案。在可存取來源資料倉儲的機器上執行下列指令，即可產生檔案。

產生中繼資料 ZIP 檔案：

```
dwh-migration-dumper \
  --connector teradata \
  --database DATABASES \
  --driver path/terajdbc4.jar \
  --host HOST \
  --assessment \
  --user USER \
  --password PASSWORD
```

**注意：**`teradata` 連接器可視需要使用 `--database` 旗標。如果省略，系統會擷取所有資料庫的中繼資料。這個旗標僅適用於 `teradata` 連接器，無法與 `teradata-logs` 搭配使用。

產生包含查詢記錄的 ZIP 檔案：

```
dwh-migration-dumper \
  --connector teradata-logs \
  --driver path/terajdbc4.jar \
  --host HOST \
  --assessment \
  --user USER \
  --password PASSWORD
```

**注意：**使用 `teradata-logs` 連接器擷取查詢記錄時，不會使用 `--database` 旗標。系統一律會擷取所有資料庫的查詢記錄。

更改下列內容：

* `PATH`：這個連線所用驅動程式 JAR 檔案的絕對或相對路徑
* `VERSION`：驅動程式版本
* `HOST`：主機位址
* `USER`：用於資料庫連線的使用者名稱
* `DATABASES`：(選用) 以半形逗號分隔的資料庫名稱清單，用於擷取資料。如未提供，系統會擷取所有資料庫。
* `PASSWORD`：(選用) 資料庫連線使用的密碼。如果留空，系統會提示使用者輸入密碼。

根據預設，系統會從檢視表 `dbc.QryLogV` 和資料表 `dbc.DBQLSqlTbl` 擷取查詢記錄。如要從其他位置擷取查詢記錄，可以使用 `-Dteradata-logs.query-logs-table` 和 `-Dteradata-logs.sql-logs-table` 旗標指定資料表或檢視表的名稱。

**提示：** 如要提升 `-Dteradata-logs.query-logs-table` 和 `-Dteradata-logs.sql-logs-table` 旗標指定資料表的彙整效能，您可以在 `JOIN` 條件中加入 `DATE` 類型的額外資料欄。這個資料欄必須在兩個資料表中定義，且必須是分區主索引的一部分。如要加入這個資料欄，請使用 `-Dteradata-logs.log-date-column` 旗標。

根據預設，公用程式記錄會從資料表 `dbc.DBQLUtilityTbl` 擷取。如要從其他位置擷取公用程式記錄，可以使用 `-Dteradata-logs.utility-logs-table` 旗標指定資料表名稱。

根據預設，系統會從 `dbc.ResUsageScpu` 和 `dbc.ResUsageSpma` 資料表擷取資源使用記錄。如要從其他位置擷取資源用量記錄，可以使用 `-Dteradata-logs.res-usage-scpu-table` 和 `-Dteradata-logs.res-usage-spma-table` 旗標指定資料表名稱。

例如：

### Bash

```
dwh-migration-dumper \
  --connector teradata-logs \
  --driver path/terajdbc4.jar \
  --host HOST \
  --assessment \
  --user USER \
  --password PASSWORD \
  -Dteradata-logs.query-logs-table=pdcrdata.QryLogV_hst \
  -Dteradata-logs.sql-logs-table=pdcrdata.DBQLSqlTbl_hst \
  -Dteradata-logs.log-date-column=LogDate \
  -Dteradata-logs.utility-logs-table=pdcrdata.DBQLUtilityTbl_hst \
  -Dteradata-logs.res-usage-scpu-table=pdcrdata.ResUsageScpu_hst \
  -Dteradata-logs.res-usage-spma-table=pdcrdata.ResUsageSpma_hst
```

### Windows PowerShell

```
dwh-migration-dumper `
  --connector teradata-logs `
  --driver path\terajdbc4.jar `
  --host HOST `
  --assessment `
  --user USER `
  --password PASSWORD `
  "-Dteradata-logs.query-logs-table=pdcrdata.QryLogV_hst" `
  "-Dteradata-logs.sql-logs-table=pdcrdata.DBQLSqlTbl_hst" `
  "-Dteradata-logs.log-date-column=LogDate" `
  "-Dteradata-logs.utility-logs-table=pdcrdata.DBQLUtilityTbl_hst" `
  "-Dteradata-logs.res-usage-scpu-table=pdcrdata.ResUsageScpu_hst" `
  "-Dteradata-logs.res-usage-spma-table=pdcrdata.ResUsageSpma_hst"
```

根據預設，`dwh-migration-dumper` 工具會擷取過去七天的查詢記錄。Google 建議您提供至少兩週的查詢記錄，以便查看更詳盡的深入分析。您可以使用 `--query-log-start` 和 `--query-log-end` 旗標指定自訂時間範圍。例如：

```
dwh-migration-dumper \
  --connector teradata-logs \
  --driver path/terajdbc4.jar \
  --host HOST \
  --assessment \
  --user USER \
  --password PASSWORD \
  --query-log-start "2023-01-01 00:00:00" \
  --query-log-end "2023-01-15 00:00:00"
```

您也可以產生多個 ZIP 檔案，其中包含不同時期的查詢記錄，並提供所有檔案進行評估。

### Redshift

### 需求條件

* 連線至來源 Amazon Redshift 資料倉儲的機器
* 具備 Cloud Storage bucket 的 Google Cloud 帳戶，用於儲存資料
* 用於儲存結果的空白 BigQuery 資料集
* 資料集的讀取的權限，以便查看結果
* 建議：使用擷取工具存取系統資料表時，請以超級使用者身分存取資料庫

### 執行 `dwh-migration-dumper` 工具

下載 [`dwh-migration-dumper` 指令列擷取工具](https://github.com/google/dwh-migration-tools/releases/latest)。

下載 [`SHA256SUMS.txt` 檔案](https://github.com/google/dwh-migration-tools/releases/latest/download/SHA256SUMS.txt)，然後執行下列指令，確認 ZIP 檔案正確無誤：

### Bash

```
sha256sum --check SHA256SUMS.txt
```

### Windows PowerShell

```
(Get-FileHash RELEASE_ZIP_FILENAME).Hash -eq ((Get-Content SHA256SUMS.txt) -Split " ")[0]
```

將 `RELEASE_ZIP_FILENAME` 替換為下載的 `dwh-migration-dumper` 指令列擷取工具版本 ZIP 檔案名稱，例如 `dwh-migration-tools-v1.0.52.zip`

`True` 結果確認核對和驗證成功。

`False` 結果表示驗證錯誤。請確認核對和與 ZIP 檔案是從同一個發布版本下載，並放在同一個目錄中。

如要進一步瞭解如何使用 `dwh-migration-dumper` 工具，請參閱[產生中繼資料](https://docs.cloud.google.com/bigquery/docs/generate-metadata?hl=zh-tw)頁面。

使用 `dwh-migration-dumper` 工具，從 Amazon Redshift 資料倉儲擷取記錄和中繼資料，並儲存為兩個 ZIP 檔案。在可存取來源資料倉儲的機器上執行下列指令，即可產生檔案。

產生中繼資料 ZIP 檔案：

```
dwh-migration-dumper \
  --connector redshift \
  --database DATABASE \
  --driver PATH/redshift-jdbc42-VERSION.jar \
  --host host.region.redshift.amazonaws.com \
  --assessment \
  --user USER \
  --iam-profile IAM_PROFILE_NAME
```

產生包含查詢記錄的 ZIP 檔案：

```
dwh-migration-dumper \
  --connector redshift-raw-logs \
  --database DATABASE \
  --driver PATH/redshift-jdbc42-VERSION.jar \
  --host host.region.redshift.amazonaws.com \
  --assessment \
  --user USER \
  --iam-profile IAM_PROFILE_NAME
```

更改下列內容：

* `DATABASE`：要連線的資料庫名稱
* `PATH`：這個連線所用驅動程式 JAR 檔案的絕對或相對路徑
* `VERSION`：驅動程式版本
* `USER`：用於資料庫連線的使用者名稱
* `IAM_PROFILE_NAME`：[Amazon Redshift IAM 設定檔名稱](https://docs.aws.amazon.com/redshift/latest/mgmt/connecting-with-authentication-profiles.html)。Amazon Redshift 驗證和 AWS API 存取權的必要資訊。如要取得 Amazon Redshift 叢集的說明，請使用 AWS API。

根據預設，Amazon Redshift 會儲存三到五天的查詢記錄。

根據預設，`dwh-migration-dumper` 工具會擷取過去七天的查詢記錄。

Google 建議您提供至少兩週的查詢記錄，以便查看更詳盡的深入分析。您可能需要在兩週內執行擷取工具幾次，才能取得最佳結果。您可以使用 `--query-log-start` 和 `--query-log-end` 旗標指定自訂範圍。例如：

```
dwh-migration-dumper \
  --connector redshift-raw-logs \
  --database DATABASE \
  --driver PATH/redshift-jdbc42-VERSION.jar \
  --host host.region.redshift.amazonaws.com \
  --assessment \
  --user USER \
  --iam-profile IAM_PROFILE_NAME \
  --query-log-start "2023-01-01 00:00:00" \
  --query-log-end "2023-01-02 00:00:00"
```

您也可以產生多個 ZIP 檔案，其中包含不同時期的查詢記錄，並提供所有檔案進行評估。

**注意：** 舊版 `dwh-migration-dumper` 工具偏好使用 `--password` 選項，而非 `--iam-profile`。這個選項仍可使用，但已淘汰，可能會導致報表出現一些落差。

### Redshift Serverless

**預先發布版：** Amazon Redshift Serverless 適用的 BigQuery Migration Assessment 處於[預先發布版](https://cloud.google.com/products?hl=zh-tw#product-launch-stages)階段。如要使用這項功能，您必須加入許可清單。如要申請存取權，請填寫[申請表](https://docs.google.com/forms/d/e/1FAIpQLScr8inhgfdAFg5phMFjs9TQRTDuucmQ3vACzKgtRGmjmqlzdA/viewform?hl=zh-tw)，或傳送電子郵件至 [bq-edw-migration-support@google.com](mailto:bq-edw-migration-support@google.com)。

### 需求條件

* 一部機器，已連結至來源 Amazon Redshift Serverless 資料倉儲
* 具備 Cloud Storage bucket 的 Google Cloud 帳戶，用於儲存資料
* 用於儲存結果的空白 BigQuery 資料集
* 資料集的讀取的權限，以便查看結果
* 建議：使用擷取工具存取系統資料表時，請以超級使用者身分存取資料庫

### 執行 `dwh-migration-dumper` 工具

下載 [`dwh-migration-dumper` 指令列擷取工具](https://github.com/google/dwh-migration-tools/releases/latest)。

如要進一步瞭解如何使用 `dwh-migration-dumper` 工具，請參閱「[產生中繼資料](https://docs.cloud.google.com/bigquery/docs/generate-metadata?hl=zh-tw)」頁面。

使用 `dwh-migration-dumper` 工具，從 Amazon Redshift Serverless 命名空間擷取用量記錄和中繼資料，並儲存為兩個 ZIP 檔案。在可存取來源資料倉儲的機器上執行下列指令，即可產生檔案。

產生中繼資料 ZIP 檔案：

```
dwh-migration-dumper \
  --connector redshift \
  --database DATABASE \
  --driver PATH/redshift-jdbc42-VERSION.jar \
  --host host.region.redshift-serverless.amazonaws.com \
  --assessment \
  --user USER \
  --iam-profile IAM_PROFILE_NAME
```

產生包含查詢記錄的 ZIP 檔案：

```
dwh-migration-dumper \
  --connector redshift-serverless-logs \
  --database DATABASE \
  --driver PATH/redshift-jdbc42-VERSION.jar \
  --host host.region.redshift-serverless.amazonaws.com \
  --assessment \
  --user USER \
  --iam-profile IAM_PROFILE_NAME
```

更改下列內容：

* `DATABASE`：要連線的資料庫名稱
* `PATH`：這個連線所用驅動程式 JAR 檔案的絕對或相對路徑
* `VERSION`：驅動程式版本
* `USER`：用於資料庫連線的使用者名稱
* `IAM_PROFILE_NAME`：[Amazon Redshift IAM 設定檔名稱](https://docs.aws.amazon.com/redshift/latest/mgmt/connecting-with-authentication-profiles.html)。Amazon Redshift 驗證和 AWS API 存取權的必要資訊。如要取得 Amazon Redshift 叢集的說明，請使用 AWS API。

Amazon Redshift Serverless 會將用量記錄保留七天。如果需要更廣的範圍，Google 建議您在較長的時間內多次擷取資料。

### Oracle / Oracle Exadata

**預覽**

這項功能適用《[服務專屬條款](https://docs.cloud.google.com/terms/service-terms?hl=zh-tw#1)》中「一般服務條款」一節的《正式發布前產品條款》。正式發布前功能是依「原樣」提供，支援服務可能受限。
詳情請參閱[推出階段說明](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages)。

如要針對這項功能提供意見或尋求支援，請傳送電子郵件至 [bq-edw-migration-support@google.com](mailto:bq-edw-migration-support@google.com)。

### 需求條件

您必須符合下列規定，才能從 Oracle 和 Oracle Exadata 擷取中繼資料和查詢記錄：

* Oracle 資料庫必須是 11g R1 以上版本。
* 可連線至 Oracle 執行個體的機器。
* Java 8 以上版本。
* 一個 Google Cloud 帳戶，並具備用於儲存資料的 Cloud Storage bucket。
* 用於儲存結果的空白 BigQuery 資料集。或者，您也可以在使用 Google Cloud 控制台 UI 建立評估工作時，建立 BigQuery 資料集。
* 具備 SYSDBA 權限的 Oracle 一般使用者。

### 執行 `dwh-migration-dumper` 工具

下載 [`dwh-migration-dumper` 指令列擷取工具](https://github.com/google/dwh-migration-tools/releases/latest)。

下載 [`SHA256SUMS.txt` 檔案](https://github.com/google/dwh-migration-tools/releases/latest/download/SHA256SUMS.txt)，然後執行下列指令，確認 ZIP 檔案正確無誤：

```
sha256sum --check SHA256SUMS.txt
```

如要進一步瞭解如何使用 `dwh-migration-dumper` 工具，請參閱[產生中繼資料](https://docs.cloud.google.com/bigquery/docs/generate-metadata?hl=zh-tw)頁面。

使用 `dwh-migration-dumper` 工具，將中繼資料和效能統計資料擷取至 ZIP 檔案。根據預設，系統會從需要 Oracle Tuning and Diagnostics Pack 的 Oracle AWR 擷取統計資料。如果無法取得這項資料，`dwh-migration-dumper` 會改用 STATSPACK。`oracle-stats` 連接器也支援 Oracle Exadata。

如果是多租戶資料庫，則必須在根容器中執行 `dwh-migration-dumper` 工具。在其中一個可插式資料庫中執行，會導致缺少其他可插式資料庫的效能統計資料和中繼資料。

產生中繼資料 ZIP 檔案：

```
dwh-migration-dumper \
  --connector oracle-stats \
  --host HOST_NAME \
  --port PORT \
  --oracle-service SERVICE_NAME \
  --assessment \
  --driver JDBC_DRIVER_PATH \
  --user USER_NAME \
  --password
```

更改下列內容：

* `HOST_NAME`：Oracle 執行個體的主機名稱。
* `PORT`：連線通訊埠編號。預設值為 1521。
* `SERVICE_NAME`：連線要使用的 Oracle 服務名稱。
* `JDBC_DRIVER_PATH`：驅動程式 JAR 檔案的絕對或相對路徑。您可以從 [Oracle JDBC 驅動程式下載](https://www.oracle.com/pl/database/technologies/appdev/jdbc-downloads.html)頁面下載這個檔案。請選取與資料庫版本相容的驅動程式版本。
* `USER_NAME`：用於連線至 Oracle 執行個體的使用者名稱。使用者必須具備[需求條件一節](#requirements-oracle)詳述的存取權限。

### Apache Hive

**預覽**

這項功能適用《[服務專屬條款](https://docs.cloud.google.com/terms/service-terms?hl=zh-tw#1)》中「一般服務條款」一節的《正式發布前產品條款》。正式發布前功能是依「原樣」提供，支援服務可能受限。
詳情請參閱[推出階段說明](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages)。

### 需求條件

* 連至來源 Apache Hive 資料倉儲的機器 (BigQuery 遷移評估支援 Tez 和 MapReduce 上的 Hive，以及 2.2 至 3.1 之間的 Apache Hive 版本，含 2.2 和 3.1)
* 具備 Cloud Storage bucket 的 Google Cloud 帳戶，用於儲存資料
* 用於儲存結果的空白 BigQuery 資料集
* 資料集的讀取的權限，以便查看結果
* 來源 Apache Hive 資料倉儲的存取權，以便設定查詢記錄擷取作業
* 最新的資料表、分區和資料欄統計資料

BigQuery 遷移評估作業會使用資料表、分區和資料欄統計資料，進一步瞭解 Apache Hive 資料倉儲，並提供詳盡的深入分析。如果來源 Apache Hive 資料倉儲中的 `hive.stats.autogather` 設定設為 `false`，建議您先啟用這項設定或手動更新統計資料，再執行 `dwh-migration-dumper` 工具。

### 執行 `dwh-migration-dumper` 工具

下載 [`dwh-migration-dumper` 指令列擷取工具](https://github.com/google/dwh-migration-tools/releases/latest)。

下載 [`SHA256SUMS.txt` 檔案](https://github.com/google/dwh-migration-tools/releases/latest/download/SHA256SUMS.txt)，然後執行下列指令，確認 ZIP 檔案正確無誤：

### Bash

```
sha256sum --check SHA256SUMS.txt
```

### Windows PowerShell

```
(Get-FileHash RELEASE_ZIP_FILENAME).Hash -eq ((Get-Content SHA256SUMS.txt) -Split " ")[0]
```

將 `RELEASE_ZIP_FILENAME` 替換為下載的 `dwh-migration-dumper` 指令列擷取工具版本 ZIP 檔案名稱，例如 `dwh-migration-tools-v1.0.52.zip`

`True` 結果確認核對和驗證成功。

`False` 結果表示驗證錯誤。請確認核對和與 ZIP 檔案是從同一個發布版本下載，並放在同一個目錄中。

如要進一步瞭解如何使用 `dwh-migration-dumper` 工具，請參閱「[產生翻譯和評估作業的中繼資料](https://docs.cloud.google.com/bigquery/docs/generate-metadata?hl=zh-tw)」。

使用 `dwh-migration-dumper` 工具，從 Hive 資料倉儲產生中繼資料，並儲存為 ZIP 檔案。

#### 不需驗證

如要產生中繼資料 ZIP 檔案，請在可存取來源資料倉儲的機器上執行下列指令：

```
dwh-migration-dumper \
  --connector hiveql \
  --database DATABASE \
  --host hive.cluster.host \
  --port 9083 \
  --assessment
```

#### 使用 Kerberos 驗證

如要向 metastore 進行驗證，請以有權存取 Apache Hive metastore 的使用者身分登入，並產生 Kerberos 票證。接著，使用下列指令產生中繼資料 ZIP 檔案：

```
JAVA_OPTS="-Djavax.security.auth.useSubjectCredsOnly=false" \
  dwh-migration-dumper \
  --connector hiveql \
  --database DATABASE \
  --host hive.cluster.host \
  --port 9083 \
  --hive-kerberos-url PRINCIPAL/HOST \
  -Dhiveql.rpc.protection=hadoop.rpc.protection \
  --assessment
```

更改下列內容：

* `DATABASE` (選用)：要擷取的資料庫名稱清單 (以半形逗號分隔)，例如 `--database db1,db2`。您可以省略 `--database` 旗標，擷取叢集中的所有資料庫。擷取整個叢集目錄，可確保擷取所有資料表和跨資料庫依附元件，讓您執行更全面的遷移評估。
* `PRINCIPAL`：票證核發對象的 Kerberos 主體
* `HOST`：票證核發對象的 Kerberos 主機名稱
* `hadoop.rpc.protection`：簡易驗證和安全防護層 (SASL) 設定層級的保護品質 (QOP)，等於 `/etc/hadoop/conf/core-site.xml` 檔案中 `hadoop.rpc.protection` 參數的值，且為下列其中一個值：
  + `authentication`
  + `integrity`
  + `privacy`

### 使用 `hadoop-migration-assessment` 記錄掛鉤擷取查詢記錄

`hadoop-migration-assessment` 記錄掛鉤 (`MigrationAssessmentLoggingHook`) 會在查詢即時執行時攔截並記錄查詢。不會擷取安裝記錄掛鉤前執行的歷史查詢。

* 如要進行初始測試或產生報表，建議您執行記錄掛鉤數小時，確認 `.avro` 檔案已在設定的基本目錄中產生，例如 `hdfs://tmp/logs/` 或 `/tmp/logs/hive/`。
* 如要評估正式環境遷移作業，建議您執行記錄掛鉤一到兩週，擷取完整的業務週期 (包括每週或月底批次工作)，以便準確瞭解工作負載並行、查詢頻率和運算規模。

如要擷取查詢記錄，請按照下列步驟操作：

1. [上傳 `hadoop-migration-assessment` 記錄掛鉤](#upload-hadoop-hive-hook)。
2. [設定記錄掛鉤屬性](#configure-properties)。
3. [驗證記錄掛鉤](#verify-hive-hook)。

#### 上傳 `hadoop-migration-assessment` 記錄掛鉤

1. 下載 [`hadoop-migration-assessment` 查詢記錄擷取記錄掛鉤](https://github.com/google/hadoop-migration-assessment-tools/releases/latest)，其中包含 Hive 記錄掛鉤 JAR 檔案。
2. 解壓縮 JAR 檔案。

   如需稽核工具，確保符合法規遵循要求，請查看 [`hadoop-migration-assessment` 記錄掛鉤 GitHub 存放區](https://github.com/google/hadoop-migration-assessment-tools)中的原始碼，並自行編譯二進位檔。
3. 將 JAR 檔案複製到所有要啟用查詢記錄的叢集上的輔助程式庫資料夾。視供應商而定，您需要在叢集設定中找到輔助程式庫資料夾，並將 JAR 檔案轉移至 Hive 叢集上的輔助程式庫資料夾。
4. 設定 `hadoop-migration-assessment` 記錄掛鉤的設定屬性。視 Hadoop 供應商而定，您可能需要使用 UI 控制台編輯叢集設定。請修改 `/etc/hive/conf/hive-site.xml` 檔案，或使用設定管理員套用設定。

#### 設定屬性

如果下列設定鍵已有其他值，請使用半形逗號 (`,`) 附加設定。如要設定 `hadoop-migration-assessment` 記錄掛鉤，必須進行下列設定：

* `hive.exec.failure.hooks`：`com.google.cloud.bigquery.dwhassessment.hooks.MigrationAssessmentLoggingHook`
* `hive.exec.post.hooks`：`com.google.cloud.bigquery.dwhassessment.hooks.MigrationAssessmentLoggingHook`
* `hive.exec.pre.hooks`：`com.google.cloud.bigquery.dwhassessment.hooks.MigrationAssessmentLoggingHook`
* `hive.aux.jars.path`：加入記錄掛鉤 JAR 檔案的路徑，例如 `file:///HiveMigrationAssessmentQueryLogsHooks_deploy.jar`。
* `dwhassessment.hook.base-directory`：查詢記錄輸出資料夾的路徑。例如：`hdfs://tmp/logs/`。
* 您也可以視需要進行下列設定：

  + `dwhassessment.hook.queue.capacity`：查詢事件記錄執行緒的佇列容量。預設值為 `64`。
  + `dwhassessment.hook.rollover-interval`：必須執行檔案輪替的頻率。例如：`600s`。預設值為 3600 秒 (1 小時)。
  + `dwhassessment.hook.rollover-eligibility-check-interval`：在背景觸發檔案換用資格檢查的頻率。例如，`600s`。預設值為 600 秒 (10 分鐘)。

**重要事項：** 如要套用設定變更，請務必重新啟動 Hive 服務。

#### 驗證記錄掛鉤

重新啟動 `hive-server2` 程序後，請執行測試查詢並分析偵錯記錄檔。您會看到以下訊息：

```
Logger successfully started, waiting for query events. Log directory is '[dwhassessment.hook.base-directory value]'; rollover interval is '60' minutes;
rollover eligibility check is '10' minutes
```

記錄掛鉤會在設定的資料夾中，建立依日期分區的子資料夾。`dwhassessment.hook.rollover-interval` 間隔或 `hive-server2` 程序終止後，含有查詢事件的 Avro 檔案會顯示在該資料夾中。您可以在偵錯記錄檔中尋找類似訊息，查看變換作業的狀態：

```
Updated rollover time for logger ID 'my_logger_id' to '2023-12-25T10:15:30'
```

```
Performed rollover check for logger ID 'my_logger_id'. Expected rollover time
is '2023-12-25T10:15:30'
```

系統會按照指定的時間間隔或在日期變更時進行換約。日期變更時，記錄掛鉤也會為該日期建立新的子資料夾。

您也可以產生包含不同 Hive 叢集查詢記錄的資料夾，並將這些資料夾全部提供給單一評估作業。

### Informatica

**預覽**

這項功能適用《[服務專屬條款](https://docs.cloud.google.com/terms/service-terms?hl=zh-tw#1)》中「一般服務條款」一節的《正式發布前產品條款》。正式發布前功能是依「原樣」提供，支援服務可能受限。
詳情請參閱[推出階段說明](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages)。

如要針對這項功能提供意見或尋求支援，請傳送電子郵件至 [bq-edw-migration-support@google.com](mailto:bq-edw-migration-support@google.com)。

### 需求條件

* 可存取 Informatica PowerCenter Repository Manager 用戶端
* 一個 Google Cloud 帳戶，並具備用於儲存資料的 Cloud Storage bucket。
* 用於儲存結果的空白 BigQuery 資料集。或者，您也可以使用 Google Cloud 控制台建立評估工作，同時建立 BigQuery 資料集。

#### 規定：匯出物件檔案

您可以使用 Informatica PowerCenter Repository Manager GUI 匯出物件檔案。詳情請參閱「[匯出物件的步驟](https://docs.informatica.com/data-integration/powercenter/10-5-8/repository-guide/exporting-and-importing-objects/steps-to-export-objects.html)」

或者，您也可以執行 `pmrep` 指令，按照下列步驟匯出物件檔案：

1. 執行 [`pmrep connect`](https://docs.informatica.com/data-integration/common-content-for-data-integration/10-5-6/command-reference/pmrep-command-reference/connect.html) 指令，連線至存放區：

```
  pmrep connect -r `REPOSITORY_NAME` -d `DOMAIN_NAME` -n `USERNAME` -x `PASSWORD`
```

更改下列內容：

* `REPOSITORY_NAME`：要連線的存放區名稱
* `DOMAIN_NAME`：存放區的網域名稱
* `USERNAME`：用於連線至存放區的使用者名稱
* `PASSWORD`：使用者名稱的密碼

1. 連線至存放區後，請使用 [`pmrep objectexport`](https://docs.informatica.com/data-integration/common-content-for-data-integration/10-5-6/command-reference/pmrep-command-reference/objectexport.html) 指令匯出所需物件：

```
  pmrep objectexport -n `OBJECT_NAME` -o `OBJECT_TYPE` -f `FOLDER_NAME` -u `OUTPUT_FILE_NAME.xml`
```

更改下列內容：

* `OBJECT_NAME`：要匯出的特定物件名稱
* `OBJECT_TYPE`：指定物件的物件類型
* `FOLDER_NAME`：資料夾名稱，內含要匯出的物件
* `OUTPUT_FILE_NAME`：包含物件資訊的 XML 檔案名稱

## 將中繼資料和查詢記錄上傳至 Cloud Storage

從資料倉儲擷取中繼資料和查詢記錄後，您可以將檔案上傳至 Cloud Storage bucket，繼續進行遷移評估。

### Databricks

**預覽**

這項功能適用《[服務專屬條款](https://docs.cloud.google.com/terms/service-terms?hl=zh-tw#1)》中「一般服務條款」一節的《正式發布前產品條款》。正式發布前功能是依「原樣」提供，支援服務可能受限。
詳情請參閱[推出階段說明](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages)。

如要針對這項功能提供意見或尋求支援，請傳送電子郵件至 [bq-edw-migration-support@google.com](mailto:bq-edw-migration-support@google.com)。

將 ZIP 檔案上傳至 Cloud Storage bucket。如要進一步瞭解如何建立 bucket 及將檔案上傳至 Cloud Storage，請參閱「[建立 bucket](https://docs.cloud.google.com/storage/docs/creating-buckets?hl=zh-tw)」和「[從檔案系統上傳物件](https://docs.cloud.google.com/storage/docs/uploading-objects?hl=zh-tw)」。

### Snowflake

將中繼資料和含有查詢記錄與使用記錄的 ZIP 檔案上傳至 Cloud Storage bucket。將這些檔案上傳至 Cloud Storage 時，必須符合下列規定：

* 中繼資料 ZIP 檔案中所有檔案解壓縮後的總大小必須小於 50 GB。
* 中繼資料 ZIP 檔案和含有查詢記錄的 ZIP 檔案必須上傳至 Cloud Storage 資料夾。如果您有多個 ZIP 檔案，且內含不重疊的查詢記錄，則可全部上傳。
* 所有檔案都必須上傳至同一個 Cloud Storage 資料夾。
* 您必須上傳所有中繼資料和查詢記錄 ZIP 檔案，且檔案必須與 `dwh-migration-dumper` 工具輸出的檔案完全相同。請勿擷取、合併或以其他方式修改。
* 所有查詢記錄檔案解壓縮後的總大小必須小於 5 TB。
* 確認遷移評估作業選取的位置與 [Cloud Storage bucket 位於相同位置](https://docs.cloud.google.com/storage/docs/locations?hl=zh-tw)。

如要進一步瞭解如何建立 bucket 及將檔案上傳至 Cloud Storage，請參閱「[建立 bucket](https://docs.cloud.google.com/storage/docs/creating-buckets?hl=zh-tw)」和「[從檔案系統上傳物件](https://docs.cloud.google.com/storage/docs/uploading-objects?hl=zh-tw)」。

### Hadoop / Cloudera

**預覽**

這項功能適用《[服務專屬條款](https://docs.cloud.google.com/terms/service-terms?hl=zh-tw#1)》中「一般服務條款」一節的《正式發布前產品條款》。正式發布前功能是依「原樣」提供，支援服務可能受限。
詳情請參閱[推出階段說明](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages)。

如要針對這項功能提供意見或尋求支援，請傳送電子郵件至 [bq-edw-migration-support@google.com](mailto:bq-edw-migration-support@google.com)。

將包含中繼資料和效能統計資料的 ZIP 檔案上傳至 Cloud Storage bucket。根據預設，ZIP 檔案的名稱為 `dwh-migration-cloudera-manager-RUN_DATE.zip` (例如 `dwh-migration-cloudera-manager-20250312T145808.zip`)，但您可以使用 `--output` 旗標自訂名稱。

* ZIP 檔案中所有檔案解壓縮後的總大小上限為 50 GB。
* 如果是 Hadoop 和 Cloudera，遷移評估工具一次只能接受一個 ZIP 檔案。指定的 Cloud Storage bucket 路徑只能包含一個 ZIP 檔案。
* 確認遷移評估作業選取的位置與 [Cloud Storage bucket 位於相同位置](https://docs.cloud.google.com/storage/docs/locations?hl=zh-tw)。

如要進一步瞭解如何建立 bucket 及將檔案上傳至 Cloud Storage，請參閱「[建立 bucket](https://docs.cloud.google.com/storage/docs/creating-buckets?hl=zh-tw)」和「[從檔案系統上傳物件](https://docs.cloud.google.com/storage/docs/uploading-objects?hl=zh-tw)」。

### Teradata

將中繼資料和一或多個含有查詢記錄的 ZIP 檔案上傳至 Cloud Storage bucket。

所有包含查詢記錄的 ZIP 檔案中的項目會分為下列幾種：

* 查詢前置字串為 `query_history_` 的記錄檔。
* 前置字串為 `utility_logs_`、`dbc.ResUsageScpu_` 和 `dbc.ResUsageSpma_` 的時間序列檔案。

將這些檔案上傳至 Cloud Storage 時，必須符合下列規定：

* 所有查詢記錄檔案的未壓縮總大小上限為 5 TB。所有時間序列檔案的未壓縮總大小上限為 1 TB。
* ZIP 檔案中所有檔案解壓縮後的總大小上限為 50 GB。
* 如果查詢記錄封存在其他資料庫，請使用 `-Dteradata-logs.query-logs-table` 和 `-Dteradata-logs.sql-logs-table` 旗標指定資料表或檢視表的名稱。詳情請參閱「[從資料倉儲擷取中繼資料和查詢記錄](https://docs.cloud.google.com/bigquery/docs/migration-assessment?hl=zh-tw#teradata)」。
* 確認遷移評估作業選取的位置與 [Cloud Storage bucket 位於相同位置](https://docs.cloud.google.com/storage/docs/locations?hl=zh-tw)。

如要進一步瞭解如何建立 bucket 及將檔案上傳至 Cloud Storage，請參閱「[建立 bucket](https://docs.cloud.google.com/storage/docs/creating-buckets?hl=zh-tw)」和「[從檔案系統上傳物件](https://docs.cloud.google.com/storage/docs/uploading-objects?hl=zh-tw)」。

### Redshift

將中繼資料和一或多個含有查詢記錄的 ZIP 檔案上傳至 Cloud Storage bucket。

所有包含查詢記錄的 ZIP 檔案中的項目會分為下列幾種：

* 查詢前置字串為 `querytext_` 和 `ddltext_` 的記錄檔。
* 前置字串為 `query_queue_info_`、`wlm_query_` 和 `querymetrics_` 的時間序列檔案。

將這些檔案上傳至 Cloud Storage 時，必須符合下列規定：

* 所有查詢記錄檔案的未壓縮總大小上限為 5 TB。所有時間序列檔案的未壓縮總大小上限為 1 TB。
* ZIP 檔案中所有檔案解壓縮後的總大小上限為 50 GB。
* 確認遷移評估作業選取的位置與 [Cloud Storage bucket 位於相同位置](https://docs.cloud.google.com/storage/docs/locations?hl=zh-tw)。

如要進一步瞭解如何建立 bucket 及將檔案上傳至 Cloud Storage，請參閱「[建立 bucket](https://docs.cloud.google.com/storage/docs/creating-buckets?hl=zh-tw)」和「[從檔案系統上傳物件](https://docs.cloud.google.com/storage/docs/uploading-objects?hl=zh-tw)」。

### Redshift Serverless

**預先發布版：** Amazon Redshift Serverless 適用的 BigQuery Migration Assessment 處於[預先發布版](https://cloud.google.com/products?hl=zh-tw#product-launch-stages)階段。如要使用這項功能，您必須加入許可清單。如要申請存取權，請填寫[申請表](https://docs.google.com/forms/d/e/1FAIpQLScr8inhgfdAFg5phMFjs9TQRTDuucmQ3vACzKgtRGmjmqlzdA/viewform?hl=zh-tw)，或傳送電子郵件至 [bq-edw-migration-support@google.com](mailto:bq-edw-migration-support@google.com)。

將中繼資料和一或多個含有查詢記錄的 ZIP 檔案上傳至 Cloud Storage bucket。如要進一步瞭解如何建立 bucket 及將檔案上傳至 Cloud Storage，請參閱「[建立 bucket](https://docs.cloud.google.com/storage/docs/creating-buckets?hl=zh-tw)」和「[從檔案系統上傳物件](https://docs.cloud.google.com/storage/docs/uploading-objects?hl=zh-tw)」。

### Oracle / Oracle Exadata

**預覽**

這項功能適用《[服務專屬條款](https://docs.cloud.google.com/terms/service-terms?hl=zh-tw#1)》中「一般服務條款」一節的《正式發布前產品條款》。正式發布前功能是依「原樣」提供，支援服務可能受限。
詳情請參閱[推出階段說明](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages)。

如要針對這項功能提供意見或尋求支援，請傳送電子郵件至 [bq-edw-migration-support@google.com](mailto:bq-edw-migration-support@google.com)。

將包含中繼資料和效能統計資料的 ZIP 檔案上傳至 Cloud Storage bucket。ZIP 檔案的預設名稱為 `dwh-migration-oracle-stats.zip`，但您可以在 `--output` 旗標中指定自訂名稱。將這些檔案上傳至 Cloud Storage 時，必須符合下列規定：

* ZIP 檔案中所有檔案解壓縮後的總大小上限為 50 GB。
* 如果是 Oracle 和 Oracle Exadata，遷移評估工具一次只能接受一個 ZIP 檔案。Cloud Storage bucket 的指定路徑一次只能接受一個 ZIP 檔案。
* 確認遷移評估作業選取的位置與 [Cloud Storage bucket 位於相同位置](https://docs.cloud.google.com/storage/docs/locations?hl=zh-tw)。

如要進一步瞭解如何建立 bucket 及將檔案上傳至 Cloud Storage，請參閱「[建立 bucket](https://docs.cloud.google.com/storage/docs/creating-buckets?hl=zh-tw)」和「[從檔案系統上傳物件](https://docs.cloud.google.com/storage/docs/uploading-objects?hl=zh-tw)」。

### Apache Hive

**預覽**

這項功能適用《[服務專屬條款](https://docs.cloud.google.com/terms/service-terms?hl=zh-tw#1)》中「一般服務條款」一節的《正式發布前產品條款》。正式發布前功能是依「原樣」提供，支援服務可能受限。
詳情請參閱[推出階段說明](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages)。

將中繼資料和資料夾 (內含一或多個 Hive 叢集的查詢記錄) 上傳至 Cloud Storage bucket。如要進一步瞭解如何建立 bucket 及將檔案上傳至 Cloud Storage，請參閱「[建立 bucket](https://docs.cloud.google.com/storage/docs/creating-buckets?hl=zh-tw)」和「[從檔案系統上傳物件](https://docs.cloud.google.com/storage/docs/uploading-objects?hl=zh-tw)」。

中繼資料 ZIP 檔案中所有檔案解壓縮後的總大小上限為 50 GB。

您可以使用 [Cloud Storage 連接器](https://docs.cloud.google.com/dataproc/docs/concepts/connectors/cloud-storage?hl=zh-tw#non-clusters)，將查詢記錄直接複製到 Cloud Storage 資料夾。包含查詢記錄子資料夾的資料夾，必須上傳至中繼資料 ZIP 檔案上傳到的同一個 Cloud Storage 資料夾。

查詢記錄資料夾包含前置字串為 `dwhassessment_` 的查詢記錄檔案。所有查詢記錄檔案的未壓縮總大小上限為 5 TB。

### Informatica

**預覽**

這項功能適用《[服務專屬條款](https://docs.cloud.google.com/terms/service-terms?hl=zh-tw#1)》中「一般服務條款」一節的《正式發布前產品條款》。正式發布前功能是依「原樣」提供，支援服務可能受限。
詳情請參閱[推出階段說明](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages)。

如要針對這項功能提供意見或尋求支援，請傳送電子郵件至 [bq-edw-migration-support@google.com](mailto:bq-edw-migration-support@google.com)。

將含有 Informatica XML 存放區物件的 ZIP 檔案上傳至 Cloud Storage bucket。這個 ZIP 檔案也必須包含 `compilerworks-metadata.yaml` 檔案，其中包含下列內容：

```
  product:
    arguments: "ConnectorArguments{connector=informatica, assessment=true}"
```

ZIP 檔案中所有檔案解壓縮後的總大小上限為 50 GB。

如要進一步瞭解如何建立 bucket 及將檔案上傳至 Cloud Storage，請參閱「[建立 bucket](https://docs.cloud.google.com/storage/docs/creating-buckets?hl=zh-tw)」和「[從檔案系統上傳物件](https://docs.cloud.google.com/storage/docs/uploading-objects?hl=zh-tw)」。

## 執行 BigQuery 遷移評估

請按照下列步驟執行 BigQuery 遷移評估。這些步驟假設您已按照上一節所述，將中繼資料檔案上傳至 Cloud Storage bucket。

### 所需權限

如要啟用 BigQuery Migration Service，您必須具備下列 Identity and Access Management (IAM) 權限：

* `resourcemanager.projects.get`
* `resourcemanager.projects.update`
* `serviceusage.services.enable`
* `serviceusage.services.get`

如要存取及使用 BigQuery 遷移服務，您必須具備下列專案權限：

* `bigquerymigration.workflows.create`
* `bigquerymigration.workflows.get`
* `bigquerymigration.workflows.list`
* `bigquerymigration.workflows.delete`
* `bigquerymigration.subtasks.get`
* `bigquerymigration.subtasks.list`

**注意：** 您只能使用 Google Cloud CLI 設定具有 `bigquerymigration.*` 前置字元的權限和角色。如要瞭解如何設定及使用 Google Cloud CLI，請參閱「[gcloud CLI 工具總覽](https://docs.cloud.google.com/sdk/gcloud?hl=zh-tw)」。

如要執行 BigQuery 遷移服務，您需要下列額外權限。

* 輸入和輸出檔案的 Cloud Storage bucket 存取權限：

  + 來源 Cloud Storage bucket 的 `storage.objects.get`
  + 來源 Cloud Storage bucket 的 `storage.objects.list`
  + 目的地 Cloud Storage bucket 的 `storage.objects.create`
  + 目的地 Cloud Storage bucket 的 `storage.objects.delete`
  + 目的地 Cloud Storage bucket 的 `storage.objects.update`
  + `storage.buckets.get`
  + `storage.buckets.list`
* 具備讀取及更新 BigQuery 資料集的權限，以便 BigQuery 遷移服務寫入結果：

  + `bigquery.datasets.update`
  + `bigquery.datasets.get`
  + `bigquery.datasets.create`
  + `bigquery.datasets.delete`
  + `bigquery.jobs.create`
  + `bigquery.jobs.delete`
  + `bigquery.jobs.list`
  + `bigquery.jobs.update`
  + `bigquery.tables.create`
  + `bigquery.tables.get`
  + `bigquery.tables.getData`
  + `bigquery.tables.list`
  + `bigquery.tables.updateData`

如要與使用者共用數據分析報表，您必須授予下列角色：

* `roles/bigquery.dataViewer`
* `roles/bigquery.jobUser`

以下範例說明如何將必要角色授予要共用報表的使用者：

```
gcloud projects add-iam-policy-binding \
  PROJECT \
  --member=user:REPORT_VIEWER_EMAIL \
  --role=roles/bigquery.dataViewer

gcloud projects add-iam-policy-binding \
  PROJECT \
  --member=user:REPORT_VIEWER_EMAIL \
  --role=roles/bigquery.jobUser
```

更改下列內容：

* `PROJECT`：使用者所在的專案
* `REPORT_VIEWER_EMAIL`：報表分享對象的電子郵件地址

### 建立評估專案

建議您建立及設定新專案，以便執行遷移評估。您可以使用下列指令碼建立新的 Google Cloud 專案，並指派執行評估作業所需的所有權限和角色：

```
#!/bin/bash

# --- Configuration ---
# Replace with your desired project ID, the email of the user that runs
# the assessment, and your organization ID.
export PROJECT_ID="PROJECT_ID"
export ASSESSMENT_RUNNER_EMAIL="RUNNER_EMAIL"
export ORGANIZATION_ID="ORGANIZATION_ID"


# --- Project Creation ---
echo "Creating project: $PROJECT_ID"
gcloud projects create $PROJECT_ID --organization=$ORGANIZATION_ID

# Set the new project as the default for subsequent gcloud commands
gcloud config set project $PROJECT_ID

# --- IAM Role Creation ---
echo "Creating custom role 'BQMSrole' in project $PROJECT_ID"
gcloud iam roles create BQMSrole \
  --project=$PROJECT_ID \
  --title=BQMSrole \
  --permissions=bigquerymigration.subtasks.get,bigquerymigration.subtasks.list,bigquerymigration.workflows.create,bigquerymigration.workflows.get,bigquerymigration.workflows.list,bigquerymigration.workflows.delete,resourcemanager.projects.update,resourcemanager.projects.get,serviceusage.services.enable,serviceusage.services.get,storage.objects.get,storage.objects.list,storage.objects.create,storage.objects.delete,storage.objects.update,bigquery.datasets.get,bigquery.datasets.update,bigquery.datasets.create,bigquery.datasets.delete,bigquery.tables.get,bigquery.tables.create,bigquery.tables.updateData,bigquery.tables.getData,bigquery.tables.list,bigquery.jobs.create,bigquery.jobs.update,bigquery.jobs.list,bigquery.jobs.delete,storage.buckets.list,storage.buckets.get

# --- IAM Policy Binding for Assessment Runner ---
echo "Granting IAM roles to the assessment runner: $ASSESSMENT_RUNNER_EMAIL"

# Grant the custom BQMSrole to the assessment runner user
gcloud projects add-iam-policy-binding \
  $PROJECT_ID \
  --member=user:$ASSESSMENT_RUNNER_EMAIL \
  --role=projects/$PROJECT_ID/roles/BQMSrole

# Grant the BigQuery Data Viewer role to the assessment runner user
gcloud projects add-iam-policy-binding \
  $PROJECT_ID \
  --member=user:$ASSESSMENT_RUNNER_EMAIL \
  --role=roles/bigquery.dataViewer

# Grant the BigQuery Job User role to the assessment runner user
gcloud projects add-iam-policy-binding \
  $PROJECT_ID \
  --member=user:$ASSESSMENT_RUNNER_EMAIL \
  --role=roles/bigquery.jobUser

echo "Project $PROJECT_ID created and configured for BigQuery Migration Assessment."
echo "Assessment Runner: $ASSESSMENT_RUNNER_EMAIL"
```

更改下列內容：

* `PROJECT_ID`：新專案 ID 的名稱
* `RUNNER_EMAIL`：執行遷移評估作業的使用者電子郵件地址
* `ORGANIZATION_ID`：組織 ID。例如：`123456789012`

### 支援的地區

所有 BigQuery 位置都支援 BigQuery 遷移評估功能。如需 BigQuery 位置清單，請參閱「[支援的位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw#supported_locations)」。

### 事前準備

執行評估前，您必須啟用 BigQuery Migration API，並建立 BigQuery 資料集來儲存評估結果。

#### 啟用 BigQuery Migration API

按照下列步驟啟用 BigQuery Migration API：

1. 前往 Google Cloud 控制台的「BigQuery Migration API」頁面。

   [前往 BigQuery Migration API](https://console.cloud.google.com/apis/api/bigquerymigration.googleapis.com/overview?hl=zh-tw)
2. 按一下「啟用」。

#### 建立評估結果資料集

BigQuery 遷移評估會將評估結果寫入 BigQuery 中的資料表。開始之前，請先[建立資料集](https://docs.cloud.google.com/bigquery/docs/datasets?hl=zh-tw)來存放這些資料表。共用數據分析報表時，您也必須授予使用者讀取這個資料集的權限。詳情請參閱「[向使用者提供報表](#share_the_data_studio_report)」。

**注意：** 資料集應與 Cloud Storage bucket 位於相同區域，其中包含從來源資料庫擷取的中繼資料和記錄檔。不過，如果 Cloud Storage bucket 位於多區域，則資料集必須位於該多區域內的任何區域。

### 執行遷移評估

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在導覽選單的「`Migration`」下方，點選「服務」。
3. 按一下「Start Assessment」。
4. 填寫評估設定對話方塊。

   1. 在「Display name」(顯示名稱) 中輸入名稱，可包含英文字母、數字或底線。這個名稱僅供顯示之用，不一定要是專屬名稱。
   2. 在「Assessment data source」(評估資料來源)，選擇資料倉儲。
   3. 在「Path to input files」(輸入檔案的路徑) 中，輸入包含擷取檔案的 Cloud Storage bucket 路徑。
   4. 如要選擇評估結果的儲存方式，請採取下列任一做法：

      * 請勾選「Automatically create the new BigQuery dataset」(自動建立新的 BigQuery 資料集) 核取方塊，讓系統自動建立 BigQuery 資料集。系統會自動產生資料集名稱。
      * 取消勾選「Automatically create the new BigQuery dataset」(自動建立新的 BigQuery 資料集) 核取方塊，然後使用 `projectId.datasetId` 格式選擇現有的空白 BigQuery 資料集，或建立新的資料集名稱。在這個選項中，您可以選擇 BigQuery 資料集名稱。**重要事項：** Cloud Storage bucket 和 BigQuery 資料集必須位於相同多區域，或該多區域內的位置。如要進一步瞭解位置限制，請參閱「[位置考量事項](https://docs.cloud.google.com/bigquery/docs/batch-loading-data?hl=zh-tw#data-locations)」。

   **選項 1** - 自動產生 BigQuery 資料集 (預設)

   **方法 2** - 手動建立 BigQuery 資料集：
5. 點選「建立」。您可以在評估工作清單中查看工作狀態。

   評估作業執行期間，您可以查看進度，並在狀態圖示的工具提示中查看預估完成時間。
6. 評估作業執行期間，您可以點選評估工作清單中的「View report」(查看報表) 連結，在數據分析中查看含有部分資料的評估報表。評估作業執行期間，「View report」(查看報表) 連結可能需要一些時間才會顯示。報表會在新分頁中開啟。

   系統處理完新資料後，就會更新報表。重新整理報表分頁，或再次點選「查看報表」，即可查看更新後的報表。
7. 評估完成後，按一下「View report」(查看報表)，即可在數據分析中查看完整的評估報告。報表會在新分頁中開啟。

### API

使用定義的[工作流程](https://docs.cloud.google.com/bigquery/docs/reference/migration/rest/v2alpha/projects.locations.workflows?hl=zh-tw)呼叫 [`create`](https://docs.cloud.google.com/bigquery/docs/reference/migration/rest/v2alpha/projects.locations.workflows/create?hl=zh-tw) 方法。

接著，呼叫 [`start`](https://docs.cloud.google.com/bigquery/docs/reference/migration/rest/v2alpha/projects.locations.workflows/start?hl=zh-tw) 方法，啟動評估工作流程。

評估作業會在您先前建立的 BigQuery 資料集中建立資料表。您可以查詢這些資料表，取得現有資料倉儲中使用的資料表和查詢相關資訊。如要瞭解翻譯的輸出檔案，請參閱「[批次 SQL 翻譯器](https://docs.cloud.google.com/bigquery/docs/batch-sql-translator?hl=zh-tw#explore_the_translation_output)」。

#### 可分享的匯總評估結果

**預覽**

這項功能適用《[服務專屬條款](https://docs.cloud.google.com/terms/service-terms?hl=zh-tw#1)》中「一般服務條款」一節的《正式發布前產品條款》。正式發布前功能是依「原樣」提供，支援服務可能受限。
詳情請參閱[推出階段說明](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages)。

如果是 Amazon Redshift、Teradata 和 Snowflake 評估作業，除了先前建立的 BigQuery 資料集外，工作流程還會建立另一個名稱相同且加上 `_shareableRedactedAggregate` 尾碼的輕量資料集。這個資料集包含從輸出資料集衍生的高度匯總資料，不含任何個人識別資訊 (PII)。

如要尋找、檢查資料集，並安全地與其他使用者共用，請參閱「[查詢遷移評估輸出表格](#query_assessment_output)」。

這項功能預設為開啟，但您可以透過[公開 API](https://docs.cloud.google.com/bigquery/docs/reference/migration/rest/v2alpha/projects.locations.workflows/create?hl=zh-tw) 選擇不使用。

### 評估作業詳細資料

如要查看評估詳細資料頁面，請按一下評估工作清單中的顯示名稱。

評估詳細資料頁面包含「Configuration」(設定) 分頁標籤，可讓您查看評估工作的詳細資訊，以及「Errors」(錯誤) 分頁標籤，可讓您查看評估處理期間發生的任何錯誤。

查看「設定」分頁，瞭解評估作業的屬性。

查看「Errors」(錯誤) 分頁，瞭解評估處理期間發生的錯誤。

## 查看及分享數據分析報表

評估任務完成後，您可以建立並分享結果的數據分析報表。

### 查看報告

按一下個別評量工作旁邊的「查看報告」連結。數據分析報表會在新分頁中以預覽模式開啟。您可以使用預覽模式查看報表內容，再進一步分享。

報表大致如下：

如要查看報表包含哪些檢視表，請選取資料倉儲：

### Snowflake

這份報告包含不同部分，可單獨或合併使用。下圖將這些部分整理成三個常見的使用者目標，協助您評估遷移需求：

### 「遷移重點」檢視畫面

「Migration Highlights」(遷移重點) 專區包含下列檢視畫面：

Snowflake 與 BigQuery 計費模式
:   列出不同層級/版本的定價。此外，我們也提供圖表，說明 BigQuery 自動調度資源功能如何比 Snowflake 節省更多成本。

總持有成本
:   互動式表格，可讓使用者定義：BigQuery 版本、承諾使用合約、基準運算單元承諾使用合約、使用中儲存空間百分比，以及載入或變更的資料百分比。有助於更準確地估算自訂案例的費用。

自動翻譯重點
:   匯總翻譯比率，依使用者或資料庫分組，並以遞增或遞減排序。此外，也包含自動翻譯失敗時最常見的錯誤訊息。

### 現有系統檢視

「Existing System」(現有系統) 區段包含下列檢視畫面：

系統總覽
:   「System Overview」(系統總覽) 檢視畫面會顯示現有系統中重要元件在指定時間範圍內的大致資料量指標。評估的時間軸取決於 BigQuery 遷移評估分析的記錄。這個檢視畫面可讓您快速瞭解來源資料倉儲的使用率，以便規劃遷移作業。

虛擬倉儲總覽
:   顯示各倉儲的 Snowflake 費用，以及期間內以節點為基礎的重新調整。

資料表磁碟區
:   「資料表數量」檢視畫面會提供 BigQuery 遷移評估作業找到的最大資料表和資料庫統計資料。由於大型資料表可能需要較長時間才能從來源資料倉儲系統擷取，因此這個檢視表有助於規劃遷移作業和排序。

資料表用量
:   「資料表用量」檢視畫面會提供統計資料，說明來源資料倉儲系統中哪些資料表的使用量較高。頻繁使用的資料表可協助您瞭解哪些資料表可能有多個依附元件，並在遷移過程中需要額外規劃。

查詢
:   「查詢」檢視畫面會細分執行的 SQL 陳述式類型，並提供使用統計資料。您可以透過「查詢類型和時間」直方圖，找出系統使用率較低的時間，以及一天中適合轉移資料的最佳時段。您也可以使用這個檢視畫面，找出經常執行的查詢，以及叫用這些執行的使用者。

資料庫
:   「資料庫」檢視畫面會提供來源資料倉儲系統中定義的大小、資料表、檢視表和程序指標。這個檢視畫面可讓您深入分析需要遷移的物件數量。

### BigQuery 穩定狀態檢視表

「BigQuery steady state」(BigQuery 穩定狀態) 區段包含下列檢視畫面：

未使用的資料表
:   「Tables With No Usage」(未使用的資料表) 檢視畫面會顯示在分析的記錄期間，BigQuery 遷移評估作業找不到任何用量的資料表。這可以指出哪些資料表可能不需要在遷移期間轉移至 BigQuery，或在 BigQuery 中儲存資料的成本可能較低。您必須驗證未使用的資料表清單，因為這些資料表可能在分析的記錄期間之外有使用情形，例如每季或每半年才使用一次的資料表。

沒有寫入作業的資料表
:   「Tables With No Writes」(沒有寫入作業的資料表) 檢視畫面會顯示在分析的記錄期間，BigQuery 遷移評估作業找不到任何更新的資料表。這可能表示在 BigQuery 儲存資料的費用較低。

### 遷移計畫檢視畫面

報表的「Migration Plan」(遷移計畫) 區段包含下列檢視畫面：

SQL 翻譯
:   「SQL Translation」(SQL 翻譯) 檢視畫面會列出 BigQuery 遷移評估自動轉換且不需手動介入的查詢數量和詳細資料。如果提供中繼資料，自動 SQL 轉譯通常能達到高轉譯率。這個檢視畫面可互動，能分析常見查詢和翻譯方式。

SQL 翻譯離線作業
:   「Offline Effort」檢視畫面會擷取需要手動介入的區域，包括特定 UDF，以及資料表或資料欄可能違反詞彙結構和語法的問題。

SQL 警告 - 待審查
:   「待審查警告」檢視畫面會擷取大部分已翻譯，但需要人工檢查的區域。

BigQuery 保留關鍵字
:   「BigQuery Reserved Keywords」(BigQuery 保留關鍵字) 檢視畫面會顯示偵測到的關鍵字使用情形，這些關鍵字在 GoogleSQL 語言中具有特殊意義，除非以反引號 (`` ` ``) 字元括住，否則無法做為 ID 使用。

資料庫和資料表耦合
:   「資料庫耦合」檢視畫面會概略顯示在單一查詢中一併存取的資料庫和
    資料表。這個檢視畫面會顯示經常參照的資料表和資料庫，以及可用於遷移規劃的項目。

表格更新時間表
:   「Table Updates Schedule」(表格更新時間表) 檢視畫面會顯示表格更新的時間和頻率，協助您規劃移動表格的方式和時間。

### 概念驗證檢視畫面

**PoC** (概念驗證) 部分包含下列檢視畫面：

概念驗證：展示 BigQuery 穩定狀態的節省效益
:   包括最常見的查詢、讀取最多資料的查詢、最慢的查詢，以及受上述查詢影響的資料表。

示範 BigQuery 遷移計畫的概念驗證
:   展示 BigQuery 如何翻譯最複雜的查詢，以及受影響的資料表。

### Teradata

這份報告分為三個部分，開頭是摘要重點頁面。該頁面包含下列章節：

* **現有系統。**這個部分是現有 Teradata 系統和用量的數據匯報，包括資料庫、結構定義、資料表的數量，以及總大小 (以 TB 為單位)。此外，這份報表也會依大小列出結構定義，並指出可能未充分利用資源的情況 (沒有寫入或讀取次數偏低的資料表)。
* **BigQuery 穩定狀態轉換 (建議)。**本節說明遷移後，系統在 BigQuery 中的樣貌。其中包含在 BigQuery 最佳化工作負載 (並避免浪費) 的建議。
* **遷移計畫。**本節提供遷移作業本身的相關資訊，例如從現有系統遷移至 BigQuery 穩定狀態。這個部分會顯示自動翻譯的查詢數量，以及將各個資料表移至 BigQuery 的預估時間。

各部分的詳細資料如下：

**現有系統**

* **運算與查詢**
  + CPU 使用率：
    - 每小時平均 CPU 使用率的熱視圖 (整體系統資源使用率檢視畫面)
    - 依小時和日期劃分的查詢，以及 CPU 使用率
    - 按類型 (讀取/寫入) 顯示的查詢，以及 CPU 使用率
    - CPU 使用率
    - 每小時 CPU 使用率、每小時平均查詢效能和每小時平均應用程式效能的疊加圖
  + 查詢直方圖 (依類型和查詢時間長度劃分)
  + 應用程式詳細資料檢視畫面 (應用程式、使用者、不重複查詢、報表與 ETL 細目)
* **儲存空間總覽**
  + 依資料量、檢視次數和存取率列出的資料庫
  + 表格：使用者、查詢、寫入和臨時表格建立作業的存取率
* **應用程式**：存取率和 IP 位址

**BigQuery 穩態轉換 (建議)**

* 彙整索引轉換為 materialized view
* 根據中繼資料和用量，建議分群和分區
* 低延遲查詢，適合使用 BigQuery BI Engine
* 設定預設值的資料欄，使用資料欄說明功能儲存預設值
* Teradata 中的不重複索引 (用於防止資料表中的資料列含有非不重複索引鍵) 會使用暫存資料表和 `MERGE` 陳述式，只將不重複記錄插入目標資料表，然後捨棄重複項目
* 其餘查詢和結構定義則照原樣翻譯

**遷移計畫**

* 自動翻譯查詢的詳細檢視畫面
  + 查詢總數，可依使用者、應用程式、受影響的資料表、查詢的資料表和查詢類型篩選
  + 將模式相似的查詢分組並一起顯示，讓使用者能依查詢類型瞭解翻譯原則
* 需要人工介入的查詢
  + 違反 BigQuery 詞彙結構的查詢
  + user-defined function 和程序
  + BigQuery 保留關鍵字
* 依寫入和讀取作業排定資料表 (以便分組移動)
* 使用 BigQuery 資料移轉服務遷移資料：各資料表的預估遷移時間

「Existing System」(現有系統) 區段包含下列檢視畫面：

系統總覽
:   「System Overview」(系統總覽) 檢視畫面會顯示現有系統中重要元件在指定時間範圍內的大致數量指標。評估的時間範圍取決於 BigQuery 遷移評估分析的記錄。這個檢視畫面可讓您快速瞭解來源資料倉儲的使用率，以便規劃遷移作業。

資料表磁碟區
:   「資料表數量」檢視畫面會提供 BigQuery 遷移評估作業找到的最大資料表和資料庫統計資料。由於大型資料表可能需要較長時間才能從來源資料倉儲系統擷取，因此這個檢視表有助於規劃遷移作業和排序。

資料表用量
:   「資料表用量」檢視畫面會提供統計資料，說明來源資料倉儲系統中哪些資料表的使用量較高。
透過頻繁使用的資料表，您可以瞭解哪些資料表可能有多個依附元件，並在遷移過程中需要額外規劃。

應用程式
:   「應用程式使用情形」和「應用程式模式」檢視畫面會提供記錄處理期間找到的應用程式統計資料。使用者可以透過這些檢視畫面，瞭解特定應用程式在一段時間內的使用情形，以及對資源用量的影響。在遷移期間，請務必以視覺化方式呈現資料的擷取和使用情形，進一步瞭解資料倉儲的依附元件，並分析一併移動各種依附應用程式的影響。IP 位址資料表有助於找出透過 JDBC 連線使用資料倉儲的確切應用程式。

查詢
:   「查詢」檢視畫面會細分執行的 SQL 陳述式類型，並提供使用統計資料。您可以透過「查詢類型和時間」直方圖，找出系統使用率較低的時間，以及一天中最適合轉移資料的時段。您也可以使用這個檢視畫面，找出經常執行的查詢，以及叫用這些執行的使用者。

資料庫
:   「資料庫」檢視畫面會提供來源資料倉儲系統中定義的大小、資料表、檢視表和程序指標。這個檢視畫面可讓您深入分析需要遷移的物件數量。

資料庫耦合
:   「資料庫耦合」檢視畫面會概略顯示在單一查詢中一併存取的資料庫和
    資料表。這個檢視畫面會顯示經常參照的資料表和資料庫，以及可用於遷移規劃的內容。

「BigQuery steady state」(BigQuery 穩定狀態) 區段包含下列檢視畫面：

未使用的資料表
:   「Tables With No Usage」(未使用的資料表) 檢視畫面會顯示 BigQuery 遷移評估作業在分析的記錄期間內，找不到任何用量的資料表。如果沒有使用，可能表示您不需要在遷移期間將該資料表轉移至 BigQuery，或者在 BigQuery 中儲存資料的費用可能較低。您應驗證未使用資料表的清單，因為這些資料表可能在記錄期間以外的時間使用，例如每三或六個月才使用一次的資料表。

沒有寫入作業的資料表
:   「Tables With No Writes」(沒有寫入作業的資料表) 檢視畫面會顯示在分析的記錄期間，BigQuery 遷移評估作業找不到任何更新的資料表。如果沒有寫入作業，可能表示您可以在 BigQuery 中降低儲存費用。

低延遲查詢
:   「低延遲查詢」檢視畫面會根據分析的記錄資料，顯示查詢執行時間的分佈情形。如果查詢時間長度分布圖表顯示大量執行時間 < 1 秒的查詢，建議啟用 BigQuery BI Engine，加快 BI 和其他低延遲工作負載。

materialized view
:   Materialized view 會提供進一步的最佳化建議，協助您提升 BigQuery 效能。

分群和分區
:   「分區和分群」檢視畫面會顯示適合分區、分群或兩者皆適用的資料表。
:   系統會分析來源資料倉儲結構定義 (例如來源資料表中的分區和主鍵)，並找出最接近的 BigQuery 對等項目，以達到類似的最佳化特性，進而提供中繼資料建議。
:   系統會分析來源查詢記錄，提供工作負載建議。系統會分析工作負載，尤其是分析查詢記錄中的 `WHERE` 或 `JOIN` 子句，然後決定建議。

分群建議
:   「分區」檢視畫面會根據分區限制定義，顯示分區數量可能超過 10,000 個的資料表。這類資料表通常適合用於 BigQuery 分群，可進行精細的資料表分區。

不重複限制
:   「Unique Constraints」(不重複限制) 檢視畫面會顯示 `SET` 資料表，以及來源資料倉儲中定義的不重複索引。在 BigQuery 中，建議使用暫存資料表和 `MERGE` 陳述式，只將不重複的記錄插入目標資料表。請根據這個檢視畫面的內容，判斷在遷移期間，可能需要調整哪些資料表的 ETL。

預設值 / 檢查限制
:   這個檢視表會顯示使用檢查限制設定預設資料欄值的資料表。在 BigQuery 中，請參閱「[指定預設資料欄值](https://docs.cloud.google.com/bigquery/docs/default-values?hl=zh-tw)」。

報表的「Migration path」(遷移路徑) 區段包含下列檢視畫面：

SQL 翻譯
:   「SQL Translation」(SQL 翻譯) 檢視畫面會列出 BigQuery 遷移評估自動轉換且不需手動介入的查詢數量和詳細資料。如果提供中繼資料，自動 SQL 轉譯通常能達到高轉譯率。這個檢視畫面可互動，能分析常見查詢和翻譯方式。

離線作業
:   「Offline Effort」檢視畫面會擷取需要手動介入的區域，包括特定 UDF，以及資料表或資料欄可能違反詞彙結構和語法的問題。

BigQuery 保留關鍵字
:   「BigQuery Reserved Keywords」(BigQuery 保留關鍵字) 檢視畫面會顯示偵測到的關鍵字使用情形，這些關鍵字在 GoogleSQL 語言中具有特殊意義，除非以反引號 (`` ` ``) 字元括住，否則無法做為 ID 使用。

表格更新時間表
:   「Table Updates Schedule」(表格更新時間表) 檢視畫面會顯示表格的更新時間和頻率，協助您規劃移動表格的方式和時間。

將資料遷移至 BigQuery
:   「Data Migration to BigQuery」(資料遷移至 BigQuery) 檢視畫面會列出遷移路徑，以及使用 BigQuery 資料移轉服務遷移資料的預計時間。詳情請參閱 [Teradata 適用的 BigQuery 資料移轉服務指南](https://docs.cloud.google.com/bigquery/docs/migration/teradata?hl=zh-tw)。

「Appendix」(附錄) 區段包含下列檢視畫面：

區分大小寫
:   「Case Sensitivity」(區分大小寫) 檢視畫面會顯示來源資料倉儲中，設為執行不區分大小寫比較的資料表。根據預設，BigQuery 中的字串比較會區分大小寫。詳情請參閱「[Collation](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/collation-concepts?hl=zh-tw)」。

### Redshift

遷移重點
:   「遷移重點」檢視畫面提供報告三個部分的內容提要：

1. 「Existing System」(現有系統) 面板會提供資料庫、結構定義、資料表的數量，以及現有 Redshift 系統的總大小。並依大小和潛在次佳資源使用率列出結構定義。您可以根據這項資訊，移除、分區或分群資料表，藉此最佳化資料。
2. 「BigQuery Steady State」(BigQuery 穩定狀態) 面板會提供資料遷移至 BigQuery 後的樣貌資訊，包括可使用 BigQuery 遷移服務自動翻譯的查詢數量。這個部分也會根據您的年度資料擷取率，顯示在 BigQuery 中儲存資料的費用，以及資料表、佈建和空間的最佳化建議。
3. 「Migration Path」(遷移路徑) 面板會提供遷移作業本身的相關資訊。其中會顯示每個資料表的預計遷移時間、資料列數和大小。

「Existing System」(現有系統) 區段包含下列檢視畫面：

依類型和排程查詢
:   「Queries by Type and Schedule」(依類型和排程分類的查詢) 檢視畫面會將查詢分為 ETL/寫入和報表/匯總。查看查詢組合隨時間的變化，有助於瞭解現有的使用模式，並找出可能影響成本和效能的突發狀況和過度佈建。

查詢佇列
:   「查詢佇列」檢視畫面提供系統負載的其他詳細資料，包括查詢量、組合，以及因佇列而產生的任何效能影響，例如資源不足。

查詢和 WLM 資源調度
:   「查詢和 WLM 資源調度」檢視畫面會將並行資源調度視為額外費用和設定複雜度。這張圖表會顯示 Redshift 系統如何根據您指定的規則轉送查詢，以及排入佇列、並行調度資源和遭撤除的查詢對效能造成的影響。

排入佇列和等待
:   「佇列和等待」檢視畫面可讓您深入瞭解查詢的佇列和等待時間。

WLM 類別和效能
:   「WLM Classes and Performance」(WLM 類別和效能) 檢視表提供選用方法，可將規則對應至 BigQuery。不過，建議您讓 BigQuery 自動轉送查詢。

查詢和資料表數量深入分析
:   「查詢和資料表數量深入分析」檢視畫面會依大小、頻率和熱門使用者列出查詢。這有助於您分類系統負載來源，並規劃如何遷移工作負載。

資料庫和結構定義
:   「資料庫和結構定義」檢視畫面會提供來源資料倉儲系統中定義的大小、資料表、檢視表和程序指標。這有助於瞭解需要遷移的物件數量。

資料表磁碟區
:   「資料表數量」檢視畫面會提供最大資料表和資料庫的統計資料，顯示這些資料表和資料庫的存取方式。由於大型資料表可能需要較長時間才能從來源資料倉儲系統擷取，因此這個檢視畫面可協助您規劃遷移作業和排序。

資料表用量
:   「資料表用量」檢視畫面會提供統計資料，說明來源資料倉儲系統中哪些資料表的使用量較高。您可以透過頻繁使用的資料表，瞭解哪些資料表可能有多項依附元件，並在遷移過程中進行額外規劃。

進出口商
:   「匯入者與匯出者」檢視畫面會提供資料匯入 (使用 `COPY` 查詢) 和資料匯出 (使用 `UNLOAD` 查詢) 涉及的資料和使用者資訊。這個檢視畫面有助於找出與擷取和匯出相關的中繼層和程序。

叢集使用率
:   「叢集使用率」檢視畫面提供所有可用叢集的一般資訊，並顯示各叢集的 CPU 使用率。這個檢視畫面可協助您瞭解系統容量預留。

「BigQuery steady state」(BigQuery 穩定狀態) 區段包含下列檢視畫面：

分群與分區
:   「分區和分群」檢視畫面會顯示適合分區、分群或兩者皆適用的資料表。

    中繼資料建議是透過分析來源資料倉儲結構定義 (例如來源資料表中的排序鍵和分布鍵)，並找出最接近的 BigQuery 對等項目，以達到類似的最佳化特性。

    系統會分析來源查詢記錄，提供工作負載建議。系統會分析工作負載，尤其是分析查詢記錄中的 `WHERE` 或 `JOIN` 子句，然後決定建議。

    頁面底部會顯示翻譯後的建立資料表陳述式，並提供所有最佳化建議。所有翻譯後的 DDL 陳述式也可以從資料集擷取。翻譯後的 DDL 陳述式會儲存在
    `SchemaConversion` 資料表的 `CreateTableDDL` 欄中。

    報表只會針對大於 1 GB 的資料表提供建議，因為小型資料表無法從分群和分區中受益。不過，所有資料表 (包括小於 1 GB 的資料表) 的 DDL 都可在 `SchemaConversion` 資料表中取得。

未使用的資料表
:   「Tables With No Usage」(未使用的資料表) 檢視畫面會顯示 BigQuery 遷移評估在分析記錄期間未發現任何用量的資料表。如果資料表未經使用，可能代表您在遷移期間不需要將該資料表移轉至 BigQuery，或是在 BigQuery 中儲存資料的費用可能較低 (以[長期儲存](https://cloud.google.com/bigquery/pricing?hl=zh-tw#storage)計費)。建議您驗證未使用的資料表清單，因為這些資料表可能在記錄期間以外的時間使用，例如每三或六個月才使用一次的資料表。

沒有寫入作業的資料表
:   「Tables With No Writes」(無寫入作業的資料表) 檢視畫面會顯示在分析記錄期間，BigQuery 遷移評估未發現任何更新的資料表。如果沒有寫入作業，表示您或許可以降低 BigQuery 的儲存費用 (計費項目為[長期儲存](https://cloud.google.com/bigquery/pricing?hl=zh-tw#storage))。

BigQuery BI Engine 和 materialized view
:   BigQuery BI Engine 和 materialized view 會提供進一步的最佳化建議，提升 BigQuery 效能。

「Migration path」(遷移路徑) 區段包含下列檢視畫面：

SQL 翻譯
:   「SQL Translation」(SQL 翻譯) 檢視畫面會列出 BigQuery 遷移評估自動轉換且不需手動介入的查詢數量和詳細資料。如果提供中繼資料，自動 SQL 翻譯通常能達到高翻譯率。

SQL 翻譯離線作業
:   「SQL Translation Offline Effort」檢視畫面會擷取需要手動介入的區域，包括特定 UDF 和可能翻譯不明確的查詢。

支援 Alter Table Append
:   「Alter Table Append Support」檢視畫面會顯示常見 Redshift SQL 建構的詳細資料，這些建構沒有直接對應的 BigQuery 建構。

複製指令支援
:   「Copy Command Support」(複製指令支援) 檢視畫面會顯示常見 Redshift SQL 建構的詳細資料，這些建構沒有直接對應的 BigQuery 建構。

SQL 警告
:   「SQL Warnings」(SQL 警告) 檢視畫面會擷取已成功翻譯但需要審查的部分。

違反詞彙結構和語法
:   「Lexical Structure & Syntax Violations」(詞彙結構和語法違規) 檢視畫面會顯示違反 BigQuery 語法的資料欄、資料表、函式和程序名稱。

BigQuery 保留關鍵字
:   「BigQuery Reserved Keywords」(BigQuery 保留關鍵字) 檢視畫面會顯示偵測到的關鍵字使用情形，這些關鍵字在 GoogleSQL 語言中具有特殊意義，除非以反引號 (`` ` ``) 字元括住，否則無法做為 ID 使用。

結構定義耦合
:   「結構定義耦合」檢視畫面會提供資料庫、結構定義和資料表的高階檢視畫面，這些資料庫、結構定義和資料表會在單一查詢中一併存取。這個檢視畫面會顯示經常參照的資料表、結構定義和資料庫，以及可用於遷移規劃的項目。

表格更新時間表
:   「Table Updates Schedule」(表格更新時間表) 檢視畫面會顯示表格的更新時間和頻率，協助您規劃移動表格的方式和時間。

表格比例
:   「資料表規模」檢視畫面會列出資料欄最多的資料表。

將資料遷移至 BigQuery
:   「Data Migration to BigQuery」(資料遷移至 BigQuery) 檢視畫面會列出遷移路徑，以及使用 BigQuery Migration Service 資料移轉服務遷移資料的預估時間。詳情請參閱 [Redshift 的 BigQuery 資料移轉服務指南](https://docs.cloud.google.com/bigquery/docs/migration/redshift?hl=zh-tw)。

評估作業執行摘要
:   評估執行摘要包含報表完整性、進行中評估的進度，以及已處理檔案和錯誤的狀態。

    報表完整度是指成功處理的資料百分比，建議在評估報表中顯示有意義的洞察資料。如果報表缺少特定部分的資料，這項資訊會列在「Assessment Modules」(評估模組) 表格的「Report Completeness」(報表完整性) 指標下方。

    **進度**指標會顯示目前已處理的資料百分比，以及處理所有資料的預估剩餘時間。處理完成後，系統不會顯示進度指標。

### Redshift Serverless

**預先發布版：** Amazon Redshift Serverless 適用的 BigQuery Migration Assessment 處於[預先發布版](https://cloud.google.com/products?hl=zh-tw#product-launch-stages)階段。如要使用這項功能，您必須加入許可清單。如要申請存取權，請填寫[申請表](https://docs.google.com/forms/d/e/1FAIpQLScr8inhgfdAFg5phMFjs9TQRTDuucmQ3vACzKgtRGmjmqlzdA/viewform?hl=zh-tw)，或傳送電子郵件至 [bq-edw-migration-support@google.com](mailto:bq-edw-migration-support@google.com)。

遷移重點
:   這個報表頁面會顯示現有 Amazon Redshift Serverless 資料庫的摘要，包括資料表的大小和數量。此外，這份報告也會提供年度合約價值 (ACV) 的高階預估值，也就是 BigQuery 的運算和儲存費用。「遷移重點」檢視畫面提供報表三個部分的內容提要。

「Existing System」(現有系統) 區段包含下列檢視畫面：

資料庫和結構定義
:   提供各資料庫、結構定義或資料表的總儲存空間大小 (以 GB 為單位)。

外部資料庫和結構定義
:   提供每個外部資料庫、結構定義或資料表的總儲存空間大小 (以 GB 為單位) 細目。

系統使用率
:   提供過往系統使用率的一般資訊。這個檢視畫面會顯示 RPU (Amazon Redshift 處理單位) 的歷來用量和每日儲存空間用量。這個檢視畫面可協助您瞭解系統容量預留量。

「BigQuery Steady State」(BigQuery 穩定狀態) 專區提供遷移後 BigQuery 資料的相關資訊，包括可使用 BigQuery 遷移服務自動翻譯的查詢數量。這個部分也會根據您的年度資料擷取率，顯示在 BigQuery 儲存資料的費用，以及資料表、佈建和空間的最佳化建議。「穩定狀態」部分包含下列檢視畫面：

Amazon Redshift Serverless 與 BigQuery 定價
:   比較 Amazon Redshift Serverless 和 BigQuery 的定價模式，協助您瞭解遷移至 BigQuery 後的優點和潛在成本節省效益。

BigQuery 運算費用 (TCO)
:   可估算 BigQuery 的運算費用。計算機有四個手動輸入項目：BigQuery 版本、區域、承諾期和基準。根據預設，計算機會提供最佳、符合成本效益的基本承諾使用合約，您可以手動覆寫。

總持有成本
:   可讓您預估年度合約價值 (ACV)，也就是 BigQuery 的運算和儲存費用。您也可以使用計算機計算儲存費用，這項費用會因使用中儲存空間和長期儲存空間而異，具體取決於分析時間範圍內的資料表修改情況。詳情請參閱「[儲存空間定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#storage)」。

「Appendix」部分包含以下檢視畫面：

評估內容提要
:   提供評估執行作業詳細資料，包括已處理的檔案清單、錯誤和報表完整性。您可以使用這個頁面調查報表中缺少的資料，並進一步瞭解報表的完整性。

### Oracle / Oracle Exadata

**預覽**

這項功能適用《[服務專屬條款](https://docs.cloud.google.com/terms/service-terms?hl=zh-tw#1)》中「一般服務條款」一節的《正式發布前產品條款》。正式發布前功能是依「原樣」提供，支援服務可能受限。
詳情請參閱[推出階段說明](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages)。

如要針對這項功能提供意見或尋求支援，請傳送電子郵件至 [bq-edw-migration-support@google.com](mailto:bq-edw-migration-support@google.com)。

### 遷移重點

「Migration Highlights」(遷移重點) 專區包含下列檢視畫面：

* 現有系統：現有 Oracle 系統和用量的快照，包括資料庫、結構定義、資料表的數量，以及總大小 (以 GB 為單位)。此外，這項服務也會提供各資料庫的工作負載分類摘要，協助您判斷 BigQuery 是否為合適的遷移目標。
* 相容性：提供遷移作業本身的相關資訊。針對每個分析的資料庫，這份報告會顯示預計遷移時間，以及可透過 Google 提供的工具自動遷移的資料庫物件數量。
* BigQuery 穩定狀態：包含遷移至 BigQuery 後的資料樣貌資訊，包括根據年度資料擷取率和運算費用估算值，在 BigQuery 儲存資料的費用。此外，這項功能也會提供洞察資料，指出哪些資料表未充分利用。

### 現有系統

「Existing System」(現有系統) 區段包含下列檢視畫面：

* 工作負載特性：根據分析的成效指標，說明每個資料庫的工作負載類型。每個資料庫都會分類為 OLAP、混合或 OLTP。這項資訊可協助您決定要將哪些資料庫遷移至 BigQuery。
* 資料庫和結構定義：提供每個資料庫、結構定義或資料表的總儲存空間大小 (以 GB 為單位)。此外，您也可以使用這個檢視表，找出 materialized view 和外部資料表。
* 資料庫功能和連結：顯示資料庫中使用的 Oracle 功能清單，以及遷移後可使用的 BigQuery 同等功能或服務。此外，您也可以探索資料庫連結，進一步瞭解資料庫之間的連結。
* 資料庫連線：提供使用者或應用程式啟動的資料庫工作階段深入分析。分析這項資料，有助於找出遷移期間可能需要額外處理的外部應用程式。
* 查詢類型：提供執行的 SQL 陳述式類型明細，以及使用情形統計資料。您可以查看查詢執行或查詢 CPU 作業時間的每小時直方圖，找出系統使用率較低的時間，以及一天中適合移轉資料的最佳時段。
* PL/SQL 原始碼：提供 PL/SQL 物件 (例如函式或程序) 的深入分析，以及每個資料庫和結構定義的大小。此外，您也可以透過每小時執行次數直方圖，找出 PL/SQL 執行次數最多的尖峰時段。
* 系統使用率：提供過往系統使用率的一般資訊。這個檢視畫面會顯示每小時的 CPU 用量和每日儲存空間消耗量。這個檢視畫面有助於瞭解系統容量預留。

### BigQuery 穩定狀態

「BigQuery Steady State」(BigQuery 穩定狀態) 區段包含下列檢視表：

* Exadata 與 BigQuery 定價：提供 Exadata 和 BigQuery 定價模式的一般比較，協助您瞭解遷移至 BigQuery 後的優點和潛在成本節省。
* BigQuery 資料庫讀取/寫入：提供資料庫實體磁碟作業的深入分析。分析這項資料，有助於找出將資料從 Oracle 遷移至 BigQuery 的最佳時機。
* BigQuery 運算費用：可讓您估算 BigQuery 的運算費用。計算器有四個手動輸入項目：「BigQuery Edition」(BigQuery 版本)、「Region」(區域)、「Commitment period」(承諾期) 和「Baseline」(基準)。根據預設，計算機會提供最佳且符合成本效益的基準承諾使用合約，您可以手動覆寫。「Annual Autoscaling Slot Hours」(年度自動調度運算單元時數) 值會提供承諾使用量以外的運算單元時數。這個值是根據系統使用率計算得出。本頁結尾處提供基準、自動調度資源和使用率之間關係的視覺化說明。每項預估值都會顯示可能數量和預估範圍。
* 總持有成本 (TCO)：可預估年度合約價值 (ACV)，也就是 BigQuery 的運算和儲存成本。您也可以使用這項工具計算儲存費用。您也可以使用計算機計算儲存費用，*使用中儲存空間*和*長期儲存空間*的費用會有所不同，具體取決於分析時間範圍內的資料表修改情況。如要進一步瞭解儲存空間定價，請參閱「[儲存空間定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#storage)」。
* 使用率偏低的資料表：根據分析時間範圍內的用量指標，提供未使用和唯讀資料表的相關資訊。如果沒有使用，可能表示您不需要在遷移期間將資料表轉移至 BigQuery，或者在 BigQuery 中儲存資料的費用可能較低 (以長期儲存計費)。建議您驗證未使用的資料表清單，確認這些資料表在分析時間範圍外是否有人使用。

### 遷移提示

「Migration Hints」(遷移提示) 專區包含下列檢視畫面：

* 資料庫物件相容性：提供資料庫物件與 BigQuery 的相容性總覽，包括可使用 Google 提供的工具自動遷移的物件數量，或需要手動操作的物件數量。系統會針對每個資料庫、結構定義和資料庫物件類型顯示這項資訊。
* 資料庫物件遷移工作：顯示每個資料庫、結構定義或資料庫物件類型的預估遷移工作時數。此外，也會根據遷移作業，顯示小型、中型和大型物件的百分比。
* 資料庫結構定義遷移作業：提供所有偵測到的資料庫物件類型、數量、與 BigQuery 的相容性，以及預估遷移作業所需時數。
* 資料庫結構定義遷移作業詳細資料：提供資料庫結構定義遷移作業的深入深入分析，包括每個單一物件的資訊。

### 概念驗證檢視畫面

「Proof of Concept views」(概念驗證檢視畫面) 專區包含下列檢視畫面：

* 概念驗證遷移：顯示建議的資料庫清單，這些資料庫的遷移難度最低，適合做為初始遷移的候選項目。此外，這份報告也會顯示熱門查詢，協助您透過概念驗證，展示 BigQuery 節省時間和成本的成效，以及這項服務的價值。

### 附錄

「Appendix」(附錄) 區段包含下列檢視畫面：

* 評估執行摘要：提供評估執行詳細資料，包括已處理的檔案清單、錯誤和報表完整性。您可以使用這個頁面調查報表中缺少的資料，進一步瞭解報表的整體完整性。

### Apache Hive

這份報告由三個部分組成，前言為摘要重點頁面，包含下列部分：

* **現有系統 - Apache Hive。**這個部分包含現有 Apache Hive 系統和用量的快照，包括資料庫、資料表的數量、總大小 (以 GB 為單位)，以及處理的查詢記錄數量。這個部分也會依大小列出資料庫，並指出可能未充分利用資源 (沒有寫入或讀取次數極少的資料表) 和佈建。這個部分包含下列詳細資料：

  + **運算和查詢**
    - CPU 使用率：
      * 依小時和日期劃分的查詢，以及 CPU 使用率
      * 依類型查詢 (讀取/寫入)
      * 佇列和應用程式
      * 每小時 CPU 使用率、每小時平均查詢效能和每小時平均應用程式效能的疊加圖
    - 查詢直方圖 (依類型和查詢時間長度劃分)
    - 排隊和等待頁面
    - 佇列詳細檢視畫面 (佇列、使用者、不重複查詢、報表與 ETL 細目，依指標分類)
  + **儲存空間總覽**
    - 依資料量、檢視次數和存取率列出的資料庫
    - 表格：使用者、查詢、寫入和臨時表格建立作業的存取率
  + **佇列和應用程式**：存取率和用戶端 IP 位址
* **BigQuery 穩定狀態。**本節說明遷移後，系統在 BigQuery 中的樣貌。其中包含在 BigQuery 最佳化工作負載 (並避免浪費) 的建議。這個部分包含下列詳細資料：

  + 系統判定可做為 materialized view 的資料表。
  + 根據中繼資料和使用情形，建議分群和分區。
  + 系統會找出適合使用 BigQuery BI Engine 的低延遲查詢。
  + 沒有讀取或寫入用量的資料表。
  + 資料偏斜的分區資料表。
* **遷移計畫。**本節提供遷移作業本身的相關資訊。例如從現有系統轉換至 BigQuery 穩定狀態。這個部分包含為每個資料表識別的儲存目標、識別為重要的遷移資料表，以及自動翻譯的查詢數量。這個部分包含下列詳細資料：

  + 自動翻譯查詢的詳細檢視畫面
    - 查詢總數，可依使用者、應用程式、受影響的資料表、查詢的資料表和查詢類型篩選。
    - 查詢值區會將類似的模式分組，讓使用者能依查詢類型查看翻譯原則。
  + 需要人工介入的查詢
    - 違反 BigQuery 詞彙結構的查詢
    - user-defined function 和程序
    - BigQuery 保留關鍵字
  + 需要審查的查詢
  + 依寫入和讀取作業排定資料表 (以便分組移動)
  + 已找出外部和代管資料表的儲存目標

「Existing System - Hive」(現有系統 - Hive) 區段包含下列檢視畫面：

系統總覽
:   這個檢視畫面會顯示現有系統中重要元件在指定時間範圍內的高階數量指標。評估的時間範圍取決於 BigQuery 遷移評估分析的記錄。這個檢視畫面可讓您快速瞭解來源資料倉儲的使用率，以便規劃遷移作業。

資料表磁碟區
:   這個檢視畫面會顯示 BigQuery 遷移評估作業找到的最大資料表和資料庫統計資料。由於大型資料表可能需要較長時間才能從來源資料倉儲系統擷取，因此這個檢視表有助於規劃遷移作業和排序。

資料表用量
:   這個檢視畫面會提供統計資料，說明來源資料倉儲系統中哪些資料表的使用率較高。
透過頻繁使用的資料表，您可以瞭解哪些資料表可能有多個依附元件，並在遷移過程中需要額外規劃。

佇列使用率
:   這個檢視畫面會提供處理記錄時，所發現的 YARN 佇列用量統計資料。使用者可以透過這些檢視畫面，瞭解特定佇列和應用程式在一段時間內的使用情形，以及對資源用量的影響。這些檢視畫面也有助於找出並排定要遷移的工作負載。在遷移期間，請務必以視覺化方式呈現資料的擷取和使用情形，進一步瞭解資料倉儲的依附元件，並分析一併移動各種依附應用程式的影響。IP 位址資料表有助於找出透過 JDBC 連線使用資料倉儲的確切應用程式。

佇列指標
:   這個檢視畫面會細分處理記錄時，在 YARN 佇列中找到的不同指標。使用者可以透過這個檢視畫面，瞭解特定佇列的使用模式，以及對遷移作業的影響。您也可以透過這個檢視表，找出查詢中存取的資料表與執行查詢的佇列之間的關聯。

排入佇列和等待
:   這個檢視畫面可讓您深入瞭解來源資料倉儲中的查詢排入佇列時間。排隊時間代表因佈建不足而導致效能降低，而額外佈建則需要增加硬體和維護成本。

查詢
:   這個檢視畫面會細分執行的 SQL 陳述式類型，並提供使用統計資料。您可以透過「查詢類型和時間」直方圖，找出系統使用率較低的時間，以及一天中最適合轉移資料的時段。您也可以透過這個檢視畫面，找出最常用的 Hive 執行引擎和經常執行的查詢，以及使用者詳細資料。

資料庫
:   這個檢視畫面會提供來源資料倉儲系統中定義的大小、資料表、檢視表和程序指標。這個檢視畫面可讓您深入分析需要遷移的物件數量。

資料庫和資料表耦合
:   這個檢視畫面會概略顯示在單一查詢中一併存取的資料庫和資料表。這個檢視畫面會顯示經常參照的資料表和資料庫，以及可用於遷移規劃的內容。

「BigQuery Steady State」(BigQuery 穩定狀態) 區段包含下列檢視畫面：

未使用的資料表
:   「Tables With No Usage」(未使用的資料表) 檢視畫面會顯示 BigQuery 遷移評估作業在分析的記錄期間內，找不到任何用量的資料表。如果沒有使用，可能表示您不需要在遷移期間將該資料表轉移至 BigQuery，或者在 BigQuery 中儲存資料的費用可能較低。您必須驗證未使用的資料表清單，因為這些資料表可能在記錄期間以外的時間使用，例如每三或六個月才使用一次的資料表。

沒有寫入作業的資料表
:   「Tables With No Writes」(沒有寫入作業的資料表) 檢視畫面會顯示在分析的記錄期間，BigQuery 遷移評估作業找不到任何更新的資料表。如果沒有寫入作業，可能表示您可以在 BigQuery 中降低儲存費用。

分群和分區建議
:   這個檢視畫面會顯示適合分區、分群或兩者皆適用的資料表。
:   系統會分析來源資料倉儲結構定義 (例如來源資料表中的分區和主鍵)，並找出最接近的 BigQuery 對等項目，以達到類似的最佳化特性，進而提供中繼資料建議。
:   系統會分析來源查詢記錄，提供工作負載建議。系統會分析工作負載，尤其是分析查詢記錄中的 `WHERE` 或 `JOIN` 子句，然後決定建議。

分區已轉換為叢集
:   這個檢視畫面會根據分區限制定義，顯示分區數量超過 10,000 個的資料表。這類資料表通常適合用於 BigQuery 分群，可進行精細的資料表分區。

偏斜分區
:   「Skewed Partitions」(偏斜分區) 檢視畫面會根據中繼資料分析顯示資料表，並在一或多個分區中顯示資料偏斜。這些資料表適合變更結構定義，因為偏斜分區的查詢效能可能不佳。

BI Engine 和 materialized view
:   「低延遲查詢和 materialized view」檢視畫面會根據分析的記錄資料，顯示查詢執行時間的分佈情形，並提供進一步的最佳化建議，提升 BigQuery 的效能。如果查詢時間長度分布圖表顯示大量查詢的執行時間少於 1 秒，建議啟用 BI Engine，加速 BI 和其他低延遲工作負載。

報表的「Migration Plan」(遷移計畫) 區段包含下列檢視畫面：

SQL 翻譯
:   「SQL Translation」(SQL 翻譯) 檢視畫面會列出 BigQuery 遷移評估自動轉換且不需手動介入的查詢數量和詳細資料。如果提供中繼資料，自動 SQL 轉譯通常能達到高轉譯率。這個檢視畫面可互動，能分析常見查詢和翻譯方式。

SQL 翻譯離線作業
:   「Offline Effort」檢視畫面會擷取需要手動介入的區域，包括特定 UDF，以及資料表或資料欄可能違反詞彙結構和語法的問題。

SQL 警告
:   「SQL Warnings」(SQL 警告) 檢視畫面會擷取已成功翻譯但需要審查的部分。

BigQuery 保留關鍵字
:   「BigQuery Reserved Keywords」(BigQuery 保留關鍵字) 檢視畫面會顯示偵測到的關鍵字使用情形，這些關鍵字在 GoogleSQL 語言中具有特殊意義。除非以反引號 (`` ` ``) 字元括住，否則這些關鍵字無法做為 ID 使用。

表格更新時間表
:   「Table Updates Schedule」(表格更新時間表) 檢視畫面會顯示表格的更新時間和頻率，協助您規劃移動表格的方式和時間。

BigLake 外部資料表
:   「BigLake 外部資料表」檢視畫面會列出已識別為遷移至 BigLake (而非 BigQuery) 的目標資料表。

報表的「Appendix」(附錄) 部分包含下列檢視畫面：

SQL 翻譯離線作業詳細分析
:   「Detailed Offline Effort Analysis」(詳細離線工作分析) 檢視畫面可提供額外洞察資訊，指出需要手動介入的 SQL 區域。

詳細 SQL 警告分析
:   「Detailed Warnings Analysis」(詳細警告分析) 分析檢視表會提供額外深入分析，指出已成功翻譯但需要審查的 SQL 區域。

### 分享報告

數據分析報表是遷移評估的前端資訊主頁。這項功能取決於基礎資料集的存取權限。如要共用報表，收件者必須有權存取數據分析報表本身，以及包含評估結果的 BigQuery 資料集。

從 Google Cloud 控制台開啟報表時，您會以預覽模式查看報表。如要建立報表並與其他使用者共用，請按照下列步驟操作：

1. 點選「Edit and share」。數據分析會提示您將新建立的數據分析連接器附加至新報表。
2. 點選「加入報表」。報表會收到個別報表 ID，您可以使用該 ID 存取報表。
3. 如要與其他使用者共用數據分析報表，請按照「[與檢視者和編輯者共用報表](https://support.google.com/looker-studio/answer/7459147?hl=zh-tw)」一文中的步驟操作。
4. 授予使用者權限，允許他們查看用於執行評估工作的 BigQuery 資料集。詳情請參閱「[授予資料集存取權](https://docs.cloud.google.com/bigquery/docs/migration-assessment?hl=zh-tw#required_permissions)」。

## 查詢遷移評估輸出資料表

雖然數據分析報表是查看評估結果最方便的方式，但您也可以在 BigQuery 資料集中[查看及查詢基礎資料](https://docs.cloud.google.com/bigquery/docs/bigquery-web-ui?hl=zh-tw#open-ui)。

### 查詢範例

以下範例會取得不重複查詢總數、翻譯失敗的查詢數量，以及翻譯失敗的不重複查詢百分比。

```
  SELECT
    QueryCount.v AS QueryCount,
    ErrorCount.v as ErrorCount,
    (ErrorCount.v * 100) / QueryCount.v AS FailurePercentage
  FROM
  (
    SELECT
     COUNT(*) AS v
    FROM
      `your_project.your_dataset.TranslationErrors`
    WHERE Severity = "ERROR"
  ) AS ErrorCount,
  (
    SELECT
      COUNT(DISTINCT(QueryHash)) AS v
    FROM
      `your_project.your_dataset.Queries`
  ) AS QueryCount;
```

### 與其他專案中的使用者共用資料集

檢查資料集後，如要與專案外的使用者共用，可以[使用 BigQuery sharing (舊稱 Analytics Hub) 的發布者工作流程](https://docs.cloud.google.com/bigquery/docs/analytics-hub-introduction?hl=zh-tw#publisher_workflow)。

**注意：** 管理[資料交換](https://docs.cloud.google.com/bigquery/docs/analytics-hub-manage-exchanges?hl=zh-tw)或共用中的資訊清單，不會產生額外費用。

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往 BigQuery](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 按一下資料集即可查看詳細資料。
3. 依序點選「person\_add 共用」「發布為清單」。
4. 在隨即開啟的對話方塊中，按照提示建立商店資訊。

   如果您已有資料交換，請略過步驟 5。
5. [建立資料交換作業並設定權限](https://docs.cloud.google.com/bigquery/docs/analytics-hub-manage-exchanges?hl=zh-tw#create-exchange)。如要允許使用者查看這個交換作業中的清單，請將他們新增至「Subscribers」(訂閱者) 清單。
6. 輸入商店資訊詳細資料。

   「Display name」(顯示名稱) 是這個產品資訊的名稱，為必填欄位；其他欄位則為選填。
7. 按一下「發布」。

   建立私人產品資訊。
8. 在清單中，選取「Actions」下方的「More actions」more\_vert。
9. 按一下「複製分享連結」。

   您可以將連結提供給有權訂閱資料交換或清單的使用者。

## 疑難排解

以下各節將說明將資料倉儲遷移至 BigQuery 時的常見問題和疑難排解技術。

### `dwh-migration-dumper` 項工具錯誤

如要排解中繼資料或查詢記錄擷取期間，`dwh-migration-dumper` 工具終端機輸出內容中發生的錯誤和警告，請參閱「[產生中繼資料疑難排解](https://docs.cloud.google.com/bigquery/docs/generate-metadata?hl=zh-tw#troubleshooting)」。

### Hive 遷移錯誤

以下各節說明從 Hive 遷移資料倉儲至 BigQuery 時，可能遇到的常見問題。

`hadoop-migration-assessment` 查詢記錄擷取記錄掛鉤會將偵錯記錄訊息寫入 `hive-server2` 記錄。如果遇到任何問題，請查看記錄掛鉤偵錯記錄檔，其中包含 `MigrationAssessmentLoggingHook` 字串。

#### 處理 `ClassNotFoundException` 錯誤

如果 `hive-server2` 程序在查詢編譯期間找不到 `com.google.cloud.bigquery.dwhassessment.hooks.MigrationAssessmentLoggingHook`，就會發生這項錯誤。

請確認您已將記錄掛鉤 JAR 檔案新增至 Hive 叢集上的 `auxlib` 資料夾，或在 `hive.aux.jars.path` 屬性中指定 JAR 檔案的完整路徑，例如 `file://AUXLIB_PATH/HiveMigrationAssessmentQueryLogsHooks_deploy.jar`。

如果錯誤持續發生，請按照下列步驟操作：

* **驗證 Cloudera (CDP 或 CDH) 上的 JAR 位置：**在 Cloudera 環境中，輔助 JAR 屬性 (`hive.aux.jars.path`) 可能無法穩定載入根查詢編譯類別載入器。如要解決這個問題，請將記錄掛鉤 JAR 檔案直接複製到所有 HiveServer2 主機上的核心 Hive 程式庫目錄，例如 `/opt/cloudera/parcels/CDH/lib/hive/lib/`。
* **驗證設定範圍：**如果您使用 Cloudera Manager，請務必將記錄掛鉤設定屬性 (例如 `hive.exec.pre.hooks`、`hive.exec.post.hooks`、`hive.exec.failure.hooks` 和 `dwhassessment.hook.base-directory`) 放在執行中的執行引擎設定程式碼片段中。舉例來說，如果叢集使用 Tez 執行，請將 XML 屬性新增至 `hive-site.xml` 的 Hive on Tez 進階設定程式碼片段 (安全閥) 欄位，或新增至服務層級的 Hive 安全閥，而非獨立的 HiveServer2 設定程式碼片段。儲存變更後，請重新啟動 Hive 服務，包括 HiveServer2 和 Hive Metastore 角色。

#### 子資料夾未顯示在設定的資料夾中

這可能是因為設定錯誤，或記錄掛鉤初始化期間發生問題。

在 `hive-server2` 偵錯記錄中搜尋下列記錄掛鉤訊息：

```
Unable to initialize logger, logging disabled
```

```
Log dir configuration key 'dwhassessment.hook.base-directory' is not set,
logging disabled.
```

```
Error while trying to set permission
```

查看問題詳情，看看是否有需要修正的地方。

#### 資料夾中未顯示檔案

這個問題可能是事件處理期間或寫入檔案時發生問題所致。

在 `hive-server2` 偵錯記錄中搜尋下列記錄掛鉤訊息：

```
Failed to close writer for file
```

```
Got exception while processing event
```

```
Error writing record for query
```

查看問題詳情，看看是否有需要修正的地方。

#### 遺漏部分查詢事件

這個問題可能是記錄掛鉤執行緒佇列溢位所致。

在 `hive-server2` 偵錯記錄檔中搜尋下列記錄掛鉤訊息：

```
Writer queue is full. Ignoring event
```

如果看到這則訊息，建議您提高 `dwhassessment.hook.queue.capacity` 參數。

## 後續步驟

如要進一步瞭解 `dwh-migration-dumper` 工具，請參閱 [dwh-migration-tools](https://github.com/google/dwh-migration-tools)。

您也可以進一步瞭解資料倉儲遷移作業的下列步驟：

* [遷移作業總覽](https://docs.cloud.google.com/bigquery/docs/migration/migration-overview?hl=zh-tw)
* [結構定義與資料移轉總覽](https://docs.cloud.google.com/bigquery/docs/migration/schema-data-overview?hl=zh-tw)
* [資料管道](https://docs.cloud.google.com/bigquery/docs/migration/pipelines?hl=zh-tw)
* [批次 SQL 翻譯](https://docs.cloud.google.com/bigquery/docs/batch-sql-translator?hl=zh-tw)
* [互動式 SQL 翻譯](https://docs.cloud.google.com/bigquery/docs/interactive-sql-translator?hl=zh-tw)
* [資料安全性與管理](https://docs.cloud.google.com/bigquery/docs/data-governance?hl=zh-tw)
* [資料驗證工具](https://github.com/GoogleCloudPlatform/professional-services-data-validator#data-validation-tool)




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-10-20 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-10-20 (世界標準時間)。"],[],[]]