Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# AlloyDB 聯合查詢

資料分析師可以透過 [聯合查詢](https://docs.cloud.google.com/bigquery/docs/federated-queries-intro?hl=zh-tw)，從 BigQuery 查詢 AlloyDB for PostgreSQL 資料。

BigQuery AlloyDB 連結讓 BigQuery 能夠即時查詢儲存於 AlloyDB 中的資料，而且無須複製或移動資料。

## 事前準備

* 確認 BigQuery 管理員已建立 [AlloyDB 連線](https://docs.cloud.google.com/bigquery/docs/connect-to-alloydb?hl=zh-tw#create-alloydb-connection)，並[與您共用](https://docs.cloud.google.com/bigquery/docs/connect-to-alloydb?hl=zh-tw#share_connections)。
* 如要取得查詢 AlloyDB 執行個體所需的權限，請要求管理員授予您專案的 [BigQuery 連線使用者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.connectionUser)  (`roles/bigquery.connectionUser`) IAM 角色。如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

  您或許也能透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)，取得必要權限。

## 查詢資料

如要從 GoogleSQL 查詢傳送聯合查詢至 AlloyDB，請使用 [`EXTERNAL_QUERY` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/federated_query_functions?hl=zh-tw#external_query)。

假設您在 BigQuery 中儲存客戶資料表，同時在 AlloyDB 中儲存銷售資料表，並希望透過單次查詢彙整這兩個資料表。以下範例會對名為 `orders` 的 AlloyDB 資料表執行聯合查詢，並將結果與名為 `mydataset.customers` 的 BigQuery 資料表彙整。

查詢範例包括 3 個部分：

1. 在 AlloyDB 資料庫中執行外部查詢 `SELECT customer_id, MIN(order_date) AS
   first_order_date FROM orders GROUP BY customer_id`，透過 `EXTERNAL_QUERY` 函式取得每位顧客的第一筆訂單日期。
2. 依據 `customer_id` 彙整外部查詢結果資料表與 BigQuery 中的客戶資料表。
3. 在最終結果集中，選取客戶資訊和第一筆訂單日期。

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

## 查看 AlloyDB 資料表結構定義

您可以使用 `EXTERNAL_QUERY` 函式查詢 `information_schema` 資料表，藉此存取資料庫中繼資料。舉例來說，您可以列出資料庫中的所有資料表，或查看資料表結構定義。詳情請參閱 [PostgreSQL information\_schema 資料表](https://www.postgresql.org/docs/9.1/information-schema.html)。

```
-- List all tables in a database.
SELECT * FROM EXTERNAL_QUERY("region.connection_id",
"select * from information_schema.tables;");
```

```
-- List all columns in a table.
SELECT * FROM EXTERNAL_QUERY("region.connection_id",
"select * from information_schema.columns where table_name='x';");
```

## 追蹤 BigQuery 聯合查詢

對 AlloyDB 執行聯合查詢時，BigQuery 會在查詢中加入類似下列內容的註解：

```
/* Federated query from BigQuery. Project ID: PROJECT_ID, BigQuery Job ID: JOB_ID. */
```

如果您監控查詢用量的記錄，下列註解有助於識別來自 BigQuery 的查詢。

1. 前往「Logs Explorer」頁面。

   [前往 Logs Explorer](https://console.cloud.google.com/logs/query?hl=zh-tw)
2. 在「Query」(查詢) 分頁中，輸入下列查詢：

   ```
   resource.type="alloydb.googleapis.com/Instance"
   textPayload=~"Federated query from BigQuery"
   ```
3. 點選「執行查詢」

   如果 BigQuery 聯邦查詢有可用記錄，**查詢結果**中會顯示類似下列的記錄清單。

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

   如要進一步瞭解 Cloud Logging，請參閱 [Cloud Logging](https://docs.cloud.google.com/logging/docs/view/logs-explorer-interface?hl=zh-tw)。

## 疑難排解

本節說明將聯合查詢傳送至 AlloyDB 時可能發生的錯誤，並提供可能的疑難排解方法。

**問題：**無法連線至資料庫伺服器，並顯示以下錯誤：
`Invalid table-valued function EXTERNAL_QUERY Connect to PostgreSQL server failed: server closed the connection unexpectedly. This probably means the server terminated abnormally before or while processing the request.`

**解決方法：**請確認您在[連線至 AlloyDB](https://docs.cloud.google.com/bigquery/docs/connect-to-alloydb?hl=zh-tw#create-alloydb-connection) 時使用有效憑證，並遵循所有必要條件。檢查在建立 AlloyDB 連線時自動建立的服務帳戶，是否具有 AlloyDB 用戶端 (`roles/alloydb.client`) 角色。詳情請參閱「[授予服務帳戶存取權](https://docs.cloud.google.com/bigquery/docs/connect-to-alloydb?hl=zh-tw#access-alloydb)」。

## 後續步驟

* 瞭解[聯合查詢](https://docs.cloud.google.com/bigquery/docs/federated-queries-intro?hl=zh-tw)。
* 瞭解 [PostgreSQL 到 BigQuery 的資料類型對應關係](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/federated_query_functions?hl=zh-tw#postgresql_mapping)。
* 瞭解[不支援的資料類型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/federated_query_functions?hl=zh-tw#unsupported_data_types)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-05 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-05 (世界標準時間)。"],[],[]]