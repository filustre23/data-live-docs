Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# Cloud SQL 聯合查詢

BigQuery 的[聯合查詢](https://docs.cloud.google.com/bigquery/docs/federated-queries-intro?hl=zh-tw)功能可讓您即時查詢 Cloud SQL 中的資料，不必複製或移動資料。查詢聯合功能支援 MySQL 適用的 Cloud SQL 和 PostgreSQL 適用的 Cloud SQL 執行個體。

或者，您也可以使用 Cloud Data Fusion 或 [Datastream](https://docs.cloud.google.com/datastream/docs/overview?hl=zh-tw)，將資料複製到 BigQuery。如要進一步瞭解如何使用 Cloud Data Fusion，請參閱「[將資料從 MySQL 複製到 BigQuery](https://docs.cloud.google.com/data-fusion/docs/tutorials/replicating-data/mysql-to-bigquery?hl=zh-tw)」。

## 事前準備

如要對 Cloud SQL 中的資料執行聯合查詢，請按照下列步驟操作：

1. 確認 BigQuery 管理員已[建立 Cloud SQL 連線](https://docs.cloud.google.com/bigquery/docs/connect-to-sql?hl=zh-tw#create-sql-connection)，並[與您共用連線](https://docs.cloud.google.com/bigquery/docs/connect-to-sql?hl=zh-tw#share_connections)。
2. 確認 BigQuery 連線服務代理已具備 Cloud SQL 用戶端 (`roles/cloudsql.client`) 角色。詳情請參閱「[授予服務代理存取權](https://docs.cloud.google.com/bigquery/docs/connect-to-sql?hl=zh-tw#access-sql)」。
3. 如果 Cloud SQL 執行個體使用私人 IP 位址，請確認建立執行個體時已啟用私人路徑。詳情請參閱「[連線至 Cloud SQL](https://docs.cloud.google.com/bigquery/docs/connect-to-sql?hl=zh-tw)」和「[設定私人 IP](https://docs.cloud.google.com/sql/docs/mysql/configure-private-ip?hl=zh-tw)」。

### 必要的角色

如要取得查詢 Cloud SQL 執行個體所需的權限，請要求管理員授予您專案的 [BigQuery 連線使用者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.connectionUser)  (`roles/bigquery.connectionUser`) IAM 角色。如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

您或許也能透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)，取得必要權限。

## 查詢資料

如要透過 GoogleSQL 查詢將聯合查詢傳送至 Cloud SQL，請使用 [`EXTERNAL_QUERY` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/federated_query_functions?hl=zh-tw#external_query)。

### 連線 ID 格式

`EXTERNAL_QUERY` 函式的第一個引數是連線 ID。您可以使用下列其中一種格式指定連線 ID：

* **Shorts**：`[LOCATION.]CONNECTION_ID` (例如 `'us.my-connection'` 或 `'my-connection'`)
* **完整格式**：`projects/PROJECT_ID/locations/LOCATION/connections/CONNECTION_ID`
* **易記路徑格式**：`PROJECT_ID.LOCATION.CONNECTION_ID` (例如 `'my-project.us.my-connection'`)

在多項專案的共用檢視表中執行查詢時，請一律使用完整連線 ID，以免連至錯誤的專案。

### 執行聯合查詢

假設您在 BigQuery 中儲存客戶資料表，在 Cloud SQL 中儲存訂單資料表，並想透過單一查詢彙整這兩個資料表。下列範例會對名為 `orders` 的 Cloud SQL 資料表執行聯合查詢，並將結果與名為 `mydataset.customers` 的 BigQuery 資料表彙整。

選取下列其中一個選項，執行聯合查詢：

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入查詢：

   ```
   SELECT c.customer_id, c.name, rq.first_order_date
   FROM mydataset.customers AS c
   LEFT OUTER JOIN EXTERNAL_QUERY(
     'us.CONNECTION_ID',
     '''SELECT customer_id, MIN(order_date) AS first_order_date
     FROM orders
     GROUP BY customer_id''') AS rq ON rq.customer_id = c.customer_id
   GROUP BY c.customer_id, c.name, rq.first_order_date;
   ```

   將 `CONNECTION_ID` 替換為 BigQuery 連線 ID。
3. 按一下「play\_circle 執行」。

   查詢結果會顯示在「Query results」(查詢結果) 窗格中。

### bq

2. 在 Google Cloud 控制台啟用 Cloud Shell。

   [啟用 Cloud Shell](https://console.cloud.google.com/?cloudshell=true&hl=zh-tw)

   Google Cloud 控制台底部會開啟 [Cloud Shell](https://docs.cloud.google.com/shell/docs/how-cloud-shell-works?hl=zh-tw) 工作階段，並顯示指令列提示。Cloud Shell 是已安裝 Google Cloud CLI 的殼層環境，並已設定適用於您目前專案的值。工作階段可能要幾秒鐘的時間才能初始化。
3. 執行 [`bq query`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_query) 指令並加上 `--use_legacy_sql=false` 旗標：

   ```
   bq query \
       --use_legacy_sql=false \
       'SELECT c.customer_id, c.name, rq.first_order_date
       FROM mydataset.customers AS c
       LEFT OUTER JOIN EXTERNAL_QUERY(
         "us.CONNECTION_ID",
         """SELECT customer_id, MIN(order_date) AS first_order_date
         FROM orders
         GROUP BY customer_id""") AS rq ON rq.customer_id = c.customer_id
       GROUP BY c.customer_id, c.name, rq.first_order_date;'
   ```

   將 `CONNECTION_ID` 替換為 BigQuery 連線 ID。

查詢範例包括 3 個部分：

1. 在營運 Cloud SQL 資料庫中執行外部查詢 `SELECT customer_id, MIN(order_date) AS first_order_date FROM orders GROUP BY customer_id`，透過 `EXTERNAL_QUERY()` 函式取得每位顧客的第一筆訂單日期。
2. 依 `customer_id` 將外部查詢結果資料表與 BigQuery 中的客戶資料表彙整。
3. 選取顧客個人資訊和首筆訂單日期。

## 查看 Cloud SQL 資料表結構定義

您可以使用 `EXTERNAL_QUERY()` 函式查詢 `INFORMATION_SCHEMA` 檢視表，
存取資料庫中繼資料，例如列出資料庫中的所有資料表，或顯示
資料表結構定義。下列 `INFORMATION_SCHEMA` 查詢範例適用於 MySQL 和 PostgreSQL。詳情請參閱 [MySQL information\_schema 資料表](https://dev.mysql.com/doc/refman/8.4/en/information-schema-introduction.html)和 [PostgreSQL information\_schema 資料表](https://www.postgresql.org/docs/current/information-schema.html)。

```
-- List all tables in a database.
SELECT * FROM EXTERNAL_QUERY("CONNECTION_ID",
"SELECT * FROM information_schema.tables;");
```

```
-- List all columns in a table.
SELECT * FROM EXTERNAL_QUERY("CONNECTION_ID",
"SELECT * FROM information_schema.columns WHERE table_name='x';");
```

將 `CONNECTION_ID` 替換為 BigQuery 連線 ID。

## 追蹤 BigQuery 聯合查詢

對 Cloud SQL 執行聯合查詢時，BigQuery 會在查詢中加入類似下列內容的註解：

```
/* Federated query from BigQuery. Project ID: PROJECT_ID, BigQuery Job ID: JOB_ID. */
```

如果您監控 MySQL 或 PostgreSQL 資料庫的查詢用量記錄，這項註解可協助您找出源自 BigQuery 的查詢。

1. 前往 Google Cloud 控制台的「Logs Explorer」頁面。

   [前往 Logs Explorer](https://console.cloud.google.com/logs/query?hl=zh-tw)
2. 在「查詢」分頁中，輸入下列查詢：

   ```
   resource.type="cloudsql_database"
   textPayload=~"Federated query from BigQuery"
   ```
3. 點選「執行查詢」。

   如果有可用於 BigQuery 聯合查詢的記錄，「Query results」(查詢結果) 中會顯示類似下方的記錄清單：

   ```
   YYYY-MM-DD hh:mm:ss.millis UTC [3210064]: [4-1]
   db=DATABASE, user=USER_ACCOUNT
   STATEMENT: SELECT 1 FROM (SELECT FROM company_name_table) t;
   /* Federated query from BigQuery.
   Project ID: PROJECT_ID, BigQuery Job ID: JOB_ID
   */

   YYYY-MM-DD hh:mm:ss.millis UTC [3210532]: [2-1]
   db=DATABASE, user=USER_ACCOUNT
   STATEMENT: SELECT "company_id", "company type_id" FROM
   (SELECT FROM company_name_table) t;
   /* Federated query from BigQuery.
   Project ID: PROJECT_ID, BigQuery Job ID: JOB_ID
   */
   ```

## 連線詳細資料

下表列出 Cloud SQL 連線屬性：

| 屬性名稱 | 值 | 說明 |
| --- | --- | --- |
| `name` | 字串 | 連線資源名稱，格式為：`projects/PROJECT_ID/locations/LOCATION/connections/CONNECTION_ID`。 |
| `location` | 字串 | 連線位置必須與 Cloud SQL 執行個體位置相符，或是相應管轄區的多區域。舉例來說，`us-east4` 中的 Cloud SQL 執行個體可以使用 `US`，而 `europe-north1` 中的 Cloud SQL 執行個體可以使用 `EU`。只有在這個位置執行的 BigQuery 查詢，才能使用這個連線。 |
| `friendlyName` | 字串 | 連線的顯示名稱，方便使用者辨識。 |
| `description` | 字串 | 連線說明。 |
| `cloudSql.type` | 字串 | 可以是 `POSTGRES` 或 `MYSQL`。 |
| `cloudSql.instanceId` | 字串 | [Cloud SQL 執行個體](https://docs.cloud.google.com/sql/docs/mysql/instance-settings?hl=zh-tw#instance-id-2ndgen)的名稱，格式通常為 `PROJECT_ID:LOCATION:INSTANCE_ID`。您可以在「Cloud SQL 執行個體」頁面找到執行個體 ID。 |
| `cloudSql.database` | 字串 | 要連線的 Cloud SQL 資料庫。 |
| `cloudSql.serviceAccountId` | 字串 | 設定為存取 Cloud SQL 資料庫的服務帳戶。 |

下表列出 Cloud SQL 執行個體憑證的屬性：

| 屬性名稱 | 值 | 說明 |
| --- | --- | --- |
| `username` | 字串 | 資料庫使用者名稱。 |
| `password` | 字串 | 資料庫密碼。 |

## 查詢效能和最佳做法

如要最佳化聯合查詢的效能，並避免對 Cloud SQL 執行個體造成不必要的負載，請考慮下列最佳做法：

* **在外部查詢中提早篩選**：在 `EXTERNAL_QUERY` SQL 陳述式中套用 `WHERE` 篩選器和 `GROUP BY` 匯總，而不是在外部 BigQuery 查詢中篩選。在 Cloud SQL 中執行篩選器，可減少透過網路傳輸至 BigQuery 的資料量。
* **刪減資料欄**：在 `EXTERNAL_QUERY` 陳述式中只選取需要的特定資料欄，而非使用 `SELECT *`。這會減少網路傳輸量和查詢執行時間。
* **使用唯讀副本**：如要將分析查詢工作負載與主要正式資料庫隔離，請建立 [Cloud SQL 唯讀副本](https://docs.cloud.google.com/sql/docs/mysql/replication?hl=zh-tw#read-replicas)，並設定 BigQuery 連線來查詢副本。
* **將資料集和執行個體放在相同位置**：為盡可能縮短延遲時間，請將 BigQuery 資料集和連線放在 Cloud SQL 執行個體所在的區域，或對應的多區域 (例如 `US` 或 `EU`)。詳情請參閱「[支援的區域](https://docs.cloud.google.com/bigquery/docs/federated-queries-intro?hl=zh-tw#supported_region_alloy_sql)」。

## 疑難排解

本節說明如何排解將聯合查詢傳送至 Cloud SQL 時可能遇到的問題。

### 無法連線至資料庫伺服器

查詢 MySQL 資料庫時，可能會遇到下列錯誤：

```
Invalid table-valued function EXTERNAL_QUERY Failed to connect to MySQL database. Error: MysqlErrorCode(2013): Lost connection to MySQL server during query.
```

查詢 PostgreSQL 資料庫時，可能會遇到下列錯誤：

```
Invalid table-valued function EXTERNAL_QUERY Connect to PostgreSQL server failed: server closed the connection unexpectedly This probably means the server terminated abnormally before or while processing the request.
```

**解析度**

如要解決這個問題，請確認下列必要條件：

1. [建立 Cloud SQL 連線](https://docs.cloud.google.com/bigquery/docs/connect-to-sql?hl=zh-tw)時，請務必使用有效的憑證，並按照所有設定步驟操作。
2. 確認 BigQuery 連線服務代理已具備 Cloud SQL 用戶端 (`roles/cloudsql.client`) 角色。服務代理電子郵件地址的格式如下：

   ```
   service-PROJECT_NUMBER@gcp-sa-bigqueryconnection.iam.gserviceaccount.com
   ```

   如需詳細操作說明，請參閱「[授予服務代理存取權](https://docs.cloud.google.com/bigquery/docs/connect-to-sql?hl=zh-tw#access-sql)」。
3. 如果 Cloud SQL 執行個體使用私人 IP 位址，請確認您在[建立 Cloud SQL 執行個體](https://docs.cloud.google.com/sql/docs/postgres/create-instance?hl=zh-tw)時，已啟用私人路徑。啟用私人路徑後，BigQuery 就能透過私人連線存取 Cloud SQL 中的資料並執行查詢。

### 驗證外掛程式導致無法連線至 MySQL 資料庫

對 MySQL 執行個體執行聯合查詢時，可能會遇到下列錯誤：

```
Invalid table-valued function EXTERNAL_QUERY Failed to connect to MySQL database. Error: MysqlErrorCode(2059): Authentication plugin 'caching_sha2_password' cannot be loaded: /usr/lib/plugin/caching_sha2_password.so: cannot open shared object file: No such file or directory at [1:15]
```

**解析度**

如果資料庫使用者帳戶設定了 [caching\_sha2\_password 驗證](https://dev.mysql.com/doc/refman/8.4/en/native-pluggable-authentication.html)，就會發生這項錯誤，因為聯合查詢不支援這種驗證方式。

如果 Cloud SQL 執行個體執行的是 MySQL 8.0 以下版本，您可以變更 BigQuery 使用者帳戶的驗證外掛程式。在 Cloud SQL 執行個體上執行下列指令：

```
ALTER USER 'USERNAME'@'%' IDENTIFIED WITH mysql_native_password BY 'PASSWORD';
```

更改下列內容：

* `USERNAME`：BigQuery 用來連線至 MySQL 適用的 Cloud SQL 執行個體的資料庫使用者帳戶。
* `PASSWORD`：資料庫使用者帳戶的密碼。

如果 Cloud SQL 執行個體執行 MySQL 8.4 版，`mysql_native_password` 外掛程式已淘汰。不建議將現有資料庫從 8.4 降級至 8.0，用於正式環境工作負載。

只要在升級前未變更使用者驗證外掛程式，將執行個體從舊版升級至 MySQL 8.4，就不會影響現有的資料庫連線。只有使用 `mysql_native_password` 建立的使用者才能用於聯合查詢，因此傳送至 MySQL 8.4 的查詢必須使用升級前建立的使用者帳戶。

## 限制

Cloud SQL 的聯合查詢有下列限制：

* **唯讀查詢**：聯合查詢為唯讀。外部查詢必須是 `SELECT` 陳述式，不支援資料定義語言 (DDL) 和 data manipulation language (DML) 陳述式。
* **查詢效能**：聯合查詢的速度不如查詢 BigQuery 儲存空間。BigQuery 必須等待 Cloud SQL 執行外部查詢，並透過網路傳輸結果集。
* **區域限制**：BigQuery 查詢處理位置必須與 Cloud SQL 執行個體位置相符或相容。詳情請參閱「[支援的地區](https://docs.cloud.google.com/bigquery/docs/federated-queries-intro?hl=zh-tw#supported_region_alloy_sql)」。
* **不支援的資料類型**：如果外部查詢傳回 BigQuery 不支援的資料類型，查詢就會失敗。您可以在外部查詢中，將不支援的資料類型轉換為支援的資料類型。詳情請參閱「[資料類型對應](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/federated_query_functions?hl=zh-tw#mysql_mapping)」。
* **連線數量上限**：聯合查詢最多可參照 10 個不重複連線。
* **驗證外掛程式限制**：MySQL `caching_sha2_password` 外掛程式不支援聯合查詢。詳情請參閱「[疑難排解](#mysql_auth_plugin)」。

## 後續步驟

* 瞭解[聯合查詢](https://docs.cloud.google.com/bigquery/docs/federated-queries-intro?hl=zh-tw)。
* 瞭解 [MySQL 至 BigQuery 資料類型對應](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/federated_query_functions?hl=zh-tw#mysql_mapping)。
* 瞭解[從 PostgreSQL 到 BigQuery 的資料類型對應](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/federated_query_functions?hl=zh-tw#postgresql_mapping)。
* 瞭解[不支援的資料類型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/federated_query_functions?hl=zh-tw#unsupported_data_types)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-10-29 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-10-29 (世界標準時間)。"],[],[]]