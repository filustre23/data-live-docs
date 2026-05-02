* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# Cloud SQL 聯合式查詢

資料分析師可以使用[聯合查詢](https://docs.cloud.google.com/bigquery/docs/federated-queries-intro?hl=zh-tw)，從 BigQuery 查詢 Cloud SQL 中的資料。

BigQuery Cloud SQL 連結讓 BigQuery 能夠即時查詢儲存於 Cloud SQL 中的資料，而且無須複製或移動資料。查詢聯合功能支援 Cloud SQL 中的 MySQL (第 2 代) 和 PostgreSQL 執行個體。

或者，您也可以使用 Cloud Data Fusion 或 [Datastream](https://docs.cloud.google.com/datastream/docs/overview?hl=zh-tw)，將資料複製到 BigQuery。如要進一步瞭解如何使用 Cloud Data Fusion，請參閱[將資料從 MySQL 複製到 BigQuery](https://docs.cloud.google.com/data-fusion/docs/tutorials/replicating-data/mysql-to-bigquery?hl=zh-tw)。

## 事前準備

* 確認 BigQuery 管理員已建立 [Cloud SQL 連線](https://docs.cloud.google.com/bigquery/docs/connect-to-sql?hl=zh-tw#create-sql-connection)，並[與您共用](https://docs.cloud.google.com/bigquery/docs/connect-to-sql?hl=zh-tw#share_connections)該連線。
* 如要取得查詢 Cloud SQL 執行個體所需的權限，請要求管理員授予您專案的 [BigQuery Connection User](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.connectionUser)  (`roles/bigquery.connectionUser`) IAM 角色。如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

  您或許也能透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)，取得必要權限。

## 查詢資料

如要從 GoogleSQL 查詢將聯合查詢傳送至 Cloud SQL，請使用 [`EXTERNAL_QUERY` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/federated_query_functions?hl=zh-tw#external_query)。

假設您在 BigQuery 中儲存客戶資料表，同時在 Cloud SQL 中儲存銷售資料表，並希望透過單次查詢彙整這兩個資料表。下列範例會對名為 `orders` 的 Cloud SQL 資料表執行聯合查詢，並將結果與名為 `mydataset.customers` 的 BigQuery 資料表聯結。

```
SELECT c.customer_id, c.name, rq.first_order_date
FROM mydataset.customers AS c
LEFT OUTER JOIN EXTERNAL_QUERY(
  'us.connection_id',
  '''SELECT customer_id, MIN(order_date) AS first_order_date
  FROM orders
  GROUP BY customer_id''') AS rq ON rq.customer_id = c.customer_id
GROUP BY c.customer_id, c.name, rq.first_order_date;
```

查詢範例包括 3 個部分：

1. 透過 `EXTERNAL_QUERY()` 函式在作業 PostgreSQL 資料庫中執行外部查詢 `SELECT customer_id, MIN(order_date) AS
   first_order_date FROM orders GROUP BY customer_id`，藉此取得每位客戶第一筆訂單的日期。
2. 依據 `customer_id` 彙整外部查詢結果資料表與 BigQuery 中的客戶資料表。
3. 選擇顧客資訊和第一筆訂單日期。

## 查看 Cloud SQL 資料表結構定義

您可以使用 `EXTERNAL_QUERY()` 函式來查詢 information\_schema 資料表，藉此存取資料庫中繼資料。舉例來說，您可以列出資料庫中的所有資料表，或查看資料表結構定義。下列 information\_schema 查詢範例可以在 MySQL 和 PostgreSQL 中運作。您可以從 [MySQL information\_schema 資料表](https://dev.mysql.com/doc/refman/8.0/en/information-schema-introduction.html)和 [PostgreSQL information\_schema 資料表](https://www.postgresql.org/docs/9.1/information-schema.html)中查看更多資訊。

```
-- List all tables in a database.
SELECT * FROM EXTERNAL_QUERY("connection_id",
"select * from information_schema.tables;");
```

```
-- List all columns in a table.
SELECT * FROM EXTERNAL_QUERY("connection_id",
"select * from information_schema.columns where table_name='x';");
```

## 連線詳細資料

下表列出 Cloud SQL 連線屬性：

| 屬性名稱 | 值 | 說明 |
| --- | --- | --- |
| `name` | 字串 | 連線資源的名稱，格式為 project\_id.location\_id.connection\_id。 |
| `location` | 字串 | 連線位置，必須與 Cloud SQL 執行個體位置相符，或是對應管轄區的多區域。舉例來說，`us-east4` 中的 Cloud SQL 執行個體可以使用 `US`，而 `europe-north1` 中的 Cloud SQL 執行個體可以使用 `EU`。只有在這個位置執行的 BigQuery 查詢才能使用這個連線。 |
| `friendlyName` | 字串 | 連線的好記顯示名稱。 |
| `description` | 字串 | 連線的說明。 |
| `cloudSql.type` | 字串 | 可以是「POSTGRES」或「MYSQL」。 |
| `cloudSql.instanceId` | 字串 | [Cloud SQL 執行個體](https://docs.cloud.google.com/sql/docs/mysql/instance-settings?hl=zh-tw#instance-id-2ndgen)的名稱通常採用以下格式：  `Project-id:location-id:instance-id`  。您可以在 [Cloud SQL 執行個體](https://console.cloud.google.com/sql/instances?hl=zh-tw)詳細資料頁面中找到執行個體 ID。 |
| `cloudSql.database` | 字串 | 您要連結的 Cloud SQL 資料庫。 |
| `cloudSql.serviceAccountId` | 字串 | 設定為存取 Cloud SQL 資料庫的服務帳戶。 |

下表列出 Cloud SQL 執行個體憑證的屬性：

| 屬性名稱 | 值 | 說明 |
| --- | --- | --- |
| `username` | 字串 | 資料庫使用者名稱 |
| `password` | 字串 | 資料庫密碼 |

## 追蹤 BigQuery 聯合查詢

對 Cloud SQL 執行聯合查詢時，BigQuery 會在查詢中加入類似下列內容的註解：

```
/* Federated query from BigQuery. Project ID: PROJECT_ID, BigQuery Job ID: JOB_ID. */
```

如果您要監控 MySQL 或 PostgreSQL 資料庫的查詢使用記錄，下列註解有助於識別來自 BigQuery 的查詢。

1. 前往「Logs Explorer」頁面。

   [前往 Logs Explorer](https://console.cloud.google.com/logs/query?hl=zh-tw)
2. 在「Query」(查詢) 分頁中，輸入下列查詢：

   ```
   resource.type="cloudsql_database"
   textPayload=~"Federated query from BigQuery"
   ```
3. 點選「執行查詢」

   如果 BigQuery 聯邦查詢有可用記錄，**查詢結果**會顯示類似下列的記錄清單：

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

## 疑難排解

本節說明如何排解將聯合查詢傳送至 Cloud SQL 時可能遇到的問題。

**問題：**無法連線至資料庫伺服器。查詢 MySQL 資料庫時，可能會遇到下列錯誤：

`Invalid table-valued function EXTERNAL_QUERY Failed to connect to MySQL database. Error: MysqlErrorCode(2013): Lost connection to MySQL server during query.`

或者，如果您查詢的是 PostgreSQL 資料庫，可能會遇到下列錯誤：

`Invalid table-valued function EXTERNAL_QUERY Connect to PostgreSQL server failed: server closed the connection unexpectedly This probably means the server terminated abnormally before or while processing the request.`
:   **解決方法：**請確認您已使用有效憑證，並遵循所有必要條件，建立 [Cloud SQL 連線](https://docs.cloud.google.com/bigquery/docs/connect-to-sql?hl=zh-tw)。檢查在建立 Cloud SQL 連線時自動建立的服務帳戶，是否具備 Cloud SQL 用戶端 (`roles/cloudsql.client`) 角色。服務帳戶的格式如下：
    `service-PROJECT_NUMBER@gcp-sa-bigqueryconnection.iam.gserviceaccount.com`。
    如需詳細操作說明，請參閱[授予服務帳戶存取權](https://docs.cloud.google.com/bigquery/docs/connect-to-sql?hl=zh-tw#access-sql)。

    如果 Cloud SQL 執行個體使用私人 IP 位址，請務必在[建立 Cloud SQL 執行個體](https://docs.cloud.google.com/sql/docs/postgres/create-instance?hl=zh-tw)時啟用私人路徑。這樣一來，BigQuery 就能透過私人連線存取 Cloud SQL 中的資料，並對這些資料執行查詢。

**問題：**無法連線至 MySQL 資料庫。對 Cloud SQL 資料執行聯合查詢時，可能會遇到下列錯誤：

`Invalid table-valued function EXTERNAL_QUERY Failed to connect to MySQL database. Error: MysqlErrorCode(2059): Authentication plugin 'caching_sha2_password' cannot be loaded: /usr/lib/plugin/caching_sha2_password.so: cannot open shared object file: No such file or directory at [1:15]`
:   **解決方法：**

    如果資料庫使用者採用[caching\_sha2\_password 驗證](https://dev.mysql.com/doc/refman/8.4/en/native-pluggable-authentication.html)，就會發生這個錯誤，因為聯合查詢不支援這項驗證方式。

    如果您使用執行 MySQL 8.0 版或更早版本的 Cloud SQL 執行個體，可以變更從 BigQuery 連線的使用者驗證外掛程式。如要變更驗證外掛程式，請在 Cloud SQL 執行個體上執行下列指令：

    ```
    ALTER USER 'USERNAME'@'%' IDENTIFIED WITH mysql_native_password BY 'PASSWORD';
    ```

    更改下列內容：

    * ：BigQuery 用於驗證及連線至 MySQL 適用的 Cloud SQL 執行個體的資料庫使用者帳戶。`USERNAME`
    * `PASSWORD`：資料庫使用者的密碼。

    如果您使用執行 MySQL 8.4 版的 Cloud SQL 執行個體，由於 `mysql_native_password`外掛程式已遭 8.4 版淘汰，因此無法使用任何解決方法。我們不建議將現有資料庫從 8.4 降級至 8.0，做為正式環境工作負載的解決方案。

    如果 Cloud SQL 執行個體執行的 MySQL 版本低於 8.4，升級至 8.4 版不會影響現有的資料庫連線，前提是您在升級前未變更使用者的驗證外掛程式。

    只有透過 `mysql_native_password` 外掛程式建立的使用者 (通常是在升級至 8.4 版前建立的使用者) 才能用於同盟查詢，因此即使 MySQL 執行個體升級至 8.4 版，您仍應使用連線設定，透過 MySQL 8.4 版之前的資料庫使用者，將同盟查詢傳送至 MySQL。

## 限制

* 聯盟查詢不支援 MySQL `caching_sha2_password` 外掛程式。因此，使用這個外掛程式對 MySQL 8.0 和 8.4 執行的聯邦查詢會失敗。詳情請參閱「[疑難排解](https://docs.cloud.google.com/bigquery/docs/cloud-sql-federated-queries?hl=zh-tw#troubleshooting)」。

## 後續步驟

* 瞭解[聯合查詢](https://docs.cloud.google.com/bigquery/docs/federated-queries-intro?hl=zh-tw)。
* 瞭解 [MySQL 到 BigQuery 的資料類型對應關係](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/federated_query_functions?hl=zh-tw#mysql_mapping)。
* 瞭解 [PostgreSQL 到 BigQuery 的資料類型對應關係](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/federated_query_functions?hl=zh-tw#postgresql_mapping)。
* 瞭解[不支援的資料類型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/federated_query_functions?hl=zh-tw#unsupported_data_types)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-02 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-02 (世界標準時間)。"],[],[]]