Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# BigLake 資料表簡介

BigLake 資料表可讓您透過存取權委派功能，查詢 Cloud Storage、Amazon S3 和 Blob Storage 中的結構化資料。與服務帳戶相關聯的連線會擷取資料，因此您只需授予使用者 BigLake 資料表的存取權，不必授予基礎資料儲存庫的存取權。這種設計可讓您強制執行精細的安全防護措施，包括資料列層級和資料欄層級安全性。

本文提供 BigLake 資料表的總覽，並假設您熟悉資料庫資料表和 Identity and Access Management (IAM)。

## 支援的資料儲存庫

BigLake 資料表可與下列資料儲存庫搭配使用：

* 使用 [BigQuery Omni](https://docs.cloud.google.com/bigquery/docs/omni-introduction?hl=zh-tw) 存取 [Amazon S3](https://docs.cloud.google.com/bigquery/docs/omni-aws-introduction?hl=zh-tw)
* 使用 [BigQuery Omni](https://docs.cloud.google.com/bigquery/docs/omni-introduction?hl=zh-tw) 存取 [Blob Storage](https://docs.cloud.google.com/bigquery/docs/omni-azure-introduction?hl=zh-tw)
* [Cloud Storage](https://docs.cloud.google.com/bigquery/docs/query-cloud-storage-using-biglake?hl=zh-tw)

如要查詢儲存在這些資料儲存庫中的資料，您必須先建立 BigLake 資料表，然後使用 GoogleSQL 語法查詢：

* [建立 Cloud Storage BigLake 資料表](https://docs.cloud.google.com/bigquery/docs/create-cloud-storage-table-biglake?hl=zh-tw)，然後[查詢](https://docs.cloud.google.com/bigquery/docs/query-cloud-storage-using-biglake?hl=zh-tw)。
* [建立 Amazon S3 BigLake 資料表](https://docs.cloud.google.com/bigquery/docs/omni-aws-create-external-table?hl=zh-tw)，然後[執行查詢](https://docs.cloud.google.com/bigquery/docs/omni-aws-introduction?hl=zh-tw)。
* [建立 Azure Blob 儲存體 BigLake 資料表](https://docs.cloud.google.com/bigquery/docs/omni-azure-create-external-table?hl=zh-tw)，然後[查詢](https://docs.cloud.google.com/bigquery/docs/omni-aws-introduction?hl=zh-tw)。

您也可以將外部資料表升級為 BigLake。詳情請參閱「[將外部資料表升級為 BigLake](https://docs.cloud.google.com/bigquery/docs/external-data-cloud-storage?hl=zh-tw#upgrade-external-tables-to-biglake-tables)」。

BigLake 資料表可讓您透過存取權委派功能，查詢外部資料儲存庫中的結構化資料。存取權委派功能會將 BigLake 資料表的存取權，與基礎資料儲存庫的存取權分開。與服務帳戶相關聯的[外部連線](https://docs.cloud.google.com/bigquery/docs/connections-api-intro?hl=zh-tw)，用於連線至資料儲存庫。由於服務帳戶會處理從資料儲存庫擷取資料的作業，因此您只需授予使用者 BigLake 資料表的存取權。這可讓您在資料表層級強制執行精細的安全防護機制，包括[資料列層級](https://docs.cloud.google.com/bigquery/docs/row-level-security-intro?hl=zh-tw)和[資料欄層級](https://docs.cloud.google.com/bigquery/docs/column-level-security-intro?hl=zh-tw)安全性。如果是以 Cloud Storage 為基礎的 BigLake 資料表，您也可以使用[動態資料遮蓋](https://docs.cloud.google.com/bigquery/docs/column-data-masking?hl=zh-tw)。如要進一步瞭解如何使用 BigLake 資料表搭配 Amazon S3 或 Blob 儲存體資料的多雲端分析解決方案，請參閱「[BigQuery Omni](https://docs.cloud.google.com/bigquery/docs/omni-introduction?hl=zh-tw)」。

## 支援的資料儲存庫

BigLake 資料表可與下列資料儲存庫搭配使用：

* 使用 [BigQuery Omni](https://docs.cloud.google.com/bigquery/docs/omni-introduction?hl=zh-tw) 存取 [Amazon S3](https://docs.cloud.google.com/bigquery/docs/omni-aws-introduction?hl=zh-tw)
* 使用 [BigQuery Omni](https://docs.cloud.google.com/bigquery/docs/omni-introduction?hl=zh-tw) 存取 [Blob Storage](https://docs.cloud.google.com/bigquery/docs/omni-azure-introduction?hl=zh-tw)
* [Cloud Storage](https://docs.cloud.google.com/bigquery/docs/query-cloud-storage-using-biglake?hl=zh-tw)

## 臨時資料表支援

以 Cloud Storage 為基礎的 BigLake 資料表可以是臨時或永久資料表。以 Amazon S3 或 Blob 儲存體為基礎的 BigLake 資料表必須是永久資料表。

## 多個來源檔案

您可以根據多個外部資料來源建立 BigLake 資料表，前提是這些資料來源具有相同的結構定義。

## BigQuery Omni 彙整

BigQuery Omni 彙整功能可讓您執行跨Google Cloud 和 BigQuery Omni 區域的查詢。您可以使用 [GoogleSQL `JOIN` 作業](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw#join_types)，分析多種不同儲存空間解決方案中的資料，例如 AWS、Azure、公開資料集和其他 Google Cloud 服務。BigQuery Omni 彙整功能可讓您在執行查詢前，不必跨來源複製資料。

您可以在 `SELECT` 陳述式的任何位置參照 BigLake 資料表，就像參照標準 BigQuery 資料表一樣，包括使用子查詢擷取資料的[data manipulation language (DML)](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/dml-syntax?hl=zh-tw) 和[資料定義語言 (DDL)](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw) 陳述式。您可以在同一查詢中使用來自不同雲端的 BigLake 資料表和 BigQuery 資料表。所有 BigQuery 資料表都必須位於相同區域。

### BigQuery Omni join 必要權限

如要取得執行 BigQuery Omni join 所需的權限，請要求管理員在執行 join 的專案中，授予您下列 IAM 角色：

* [BigQuery 資料檢視者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.dataViewer)  (`roles/bigquery.dataViewer`)
* [BigQuery 工作使用者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.jobUser)  (`roles/bigquery.jobUser`)

如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

這些預先定義的角色具備執行 BigQuery Omni join 所需的權限。如要查看確切的必要權限，請展開「Required permissions」(必要權限) 部分：

#### 所需權限

必須具備下列權限，才能執行 BigQuery Omni join：

* `bigquery.jobs.create`
* `bigquery.tables.getData`

您或許還可透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)取得這些權限。

### BigQuery Omni join 費用

執行 BigQuery Omni 彙整作業時，BigQuery 會將查詢剖析為本機和遠端部分。本機部分會視為 BigQuery 區域中的標準查詢。遠端部分會轉換為 `CREATE TABLE AS SELECT` (CTAS) 作業，在 BigQuery Omni 區域中參照的 BigLake 資料表上執行，在 BigQuery 區域中建立臨時資料表。接著，BigQuery 會使用這個臨時資料表執行 BigQuery Omni 彙整作業，並在八小時後自動刪除資料表。

您需要支付參照 BigLake 資料表的資料移轉費用。不過，BigQuery 只會移轉 BigLake 資料表中查詢參照的資料欄和資料列，而非整個資料表，因此有助於降低這些費用。建議您盡可能指定範圍較小的資料欄篩選器，進一步降低移轉費用。CTAS 工作會顯示在工作記錄中，並顯示轉移的位元組數等資訊。即使主要查詢工作失敗，成功轉移仍會產生費用。詳情請參閱「[BigQuery Omni 定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#bqomni)」。

請參考以下查詢範例：

```
SELECT *
FROM bigquery_dataset.bigquery_table AS clients
WHERE clients.sales_rep IN (
  SELECT id
  FROM aws_dataset.aws_table1 AS employees
  INNER JOIN aws_dataset.aws_table2 AS active_employees
    ON employees.id = active_employees.id
  WHERE employees.level > 3
);
```

這個範例有兩項移轉作業：一項來自員工資料表 (含層級篩選器)，另一項來自在職員工資料表。移轉作業完成後，系統會在 BigQuery 區域執行彙整作業。如果其中一項移轉作業失敗，另一項成功，則成功的移轉作業仍會收取資料移轉費用。

### BigQuery Omni join 限制

* BigQuery [免費方案](https://cloud.google.com/bigquery/pricing?hl=zh-tw#free-tier)和 [BigQuery 沙箱](https://docs.cloud.google.com/bigquery/docs/sandbox?hl=zh-tw)不支援 BigQuery Omni 彙整。
* 如果查詢包含 `JOIN` 陳述式，匯總可能不會下推至 BigQuery Omni 區域。
* 每個臨時資料表僅用於單一 BigQuery Omni 查詢，即使多次重複相同查詢，也不會重複使用。
* 每次轉移的大小上限為 60 GB。具體來說，如果您對 BigLake 資料表套用篩選器並載入結果，結果必須小於 60 GB。如要提高配額，請[聯絡支援團隊](https://docs.cloud.google.com/bigquery/docs/getting-support?hl=zh-tw)。掃描的位元組數量沒有限制。
* BigQuery Omni 彙整查詢會對查詢速率採用內部配額。如果查詢率超過配額，您可能會收到 `All our servers are busy processing data transferred between regions` 錯誤。在多數情況下，重試查詢應可解決問題。如要提高內部配額，以便支援更高的查詢率，請與支援團隊聯絡。
* BigQuery Omni 彙整作業僅支援[共置 BigQuery 區域](https://docs.cloud.google.com/bigquery/docs/omni-introduction?hl=zh-tw#locations)及其對應的 BigQuery Omni 區域，以及 `US` 和 `EU` 多區域。在 `US` 或 `EU` 多區域中執行的 BigQuery Omni 彙整作業，只能分別存取美國或歐盟 BigQuery Omni 區域中的資料。
* 如果 BigQuery Omni 彙整查詢參照 10 個以上 BigQuery Omni 區域的資料集，可能會失敗並顯示錯誤 `Not found: Dataset <BigQuery dataset> was not found in
  location <BigQuery Omni region>`。為避免這個問題，建議您在執行參照超過 10 個資料集的 BigQuery Omni 彙整作業時，[明確指定位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw#specify_locations)。請注意，如果您明確指定 BigQuery 區域，且查詢僅包含 BigLake 資料表，則查詢會以 BigQuery Omni 查詢的形式執行，並產生資料移轉費用。
* 您無法使用 BigQuery Omni 彙整[查詢 `_FILE_NAME` 虛擬資料欄](https://docs.cloud.google.com/bigquery/docs/query-aws-data?hl=zh-tw#query_the_file_name_pseudo-column)。
* 在 `WHERE` 子句中參照 BigLake 資料表的資料欄時，無法使用 `INTERVAL` 或 `RANGE` 常值。
* BigQuery Omni join 工作不會回報從其他雲端處理及移轉的位元組數。這項資訊可在執行 BigQuery Omni 查詢時建立的子 CTAS 工作中找到。
* 參照 BigQuery Omni 資料表或檢視表的[授權檢視表](https://docs.cloud.google.com/bigquery/docs/authorized-views?hl=zh-tw)和[授權常式](https://docs.cloud.google.com/bigquery/docs/authorized-routines?hl=zh-tw)，僅適用於 BigQuery Omni 區域。
* 如果 BigQuery Omni 查詢參照 `STRUCT` 資料欄，則不會對任何遠端子查詢套用下推。為達到最佳效能，建議您在 BigQuery Omni 區域建立檢視表，將 `STRUCT` 資料欄中的必要欄位拆解成個別資料欄。
* BigQuery Omni 彙整不支援[定序](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/collation-concepts?hl=zh-tw)。
* BigQuery Omni 彙整不支援使用 `ORDER BY` 子句彙整 BigQuery Omni 檢視表。

### BigQuery Omni join 範例

下列查詢會將 BigQuery 區域中的 `orders` 資料表，與 BigQuery Omni 區域中的 `lineitem` 資料表彙整：

```
SELECT
  l_shipmode,
  o_orderpriority,
  count(l_linenumber) AS num_lineitems
FROM bigquery_dataset.orders
JOIN aws_dataset.lineitem
  ON orders.o_orderkey = lineitem.l_orderkey
WHERE
  l_shipmode IN ('AIR', 'REG AIR')
  AND l_commitdate < l_receiptdate
  AND l_shipdate < l_commitdate
  AND l_receiptdate >= DATE '1997-01-01'
  AND l_receiptdate < DATE '1997-02-01'
GROUP BY l_shipmode, o_orderpriority
ORDER BY l_shipmode, o_orderpriority;
```

這項查詢會分成地端和遠端兩部分。下列查詢會先傳送至 BigQuery Omni 區域執行。結果會是 BigQuery 區域中的臨時資料表。您可以在工作記錄中查看這個子 CTAS 工作及其中繼資料。

```
CREATE OR REPLACE TABLE temp_table
AS (
  SELECT
    l_shipmode,
    l_linenumber,
    l_orderkey
  FROM aws_dataset.lineitem
  WHERE
    l_shipmode IN ('AIR', 'REG AIR')
    AND l_commitdate < l_receiptdate
    AND l_shipdate < l_commitdate
    AND l_receiptdate >= DATE '1997-01-01'
    AND l_receiptdate < DATE '1997-02-01'
);
```

建立臨時資料表後，`JOIN` 作業會完成，並執行下列查詢：

```
SELECT
  l_shipmode,
  o_orderpriority,
  count(l_linenumber) AS num_lineitems
FROM bigquery_dataset.orders
JOIN temp_table
  ON orders.o_orderkey = lineitem.l_orderkey
GROUP BY l_shipmode, o_orderpriority
ORDER BY l_shipmode, o_orderpriority;
```

再舉一個例子，請考慮下列 BigQuery Omni 彙整：

```
SELECT c_mktsegment, c_name
FROM bigquery_dataset.customer
WHERE c_mktsegment = 'BUILDING'
UNION ALL
SELECT c_mktsegment, c_name
FROM aws_dataset.customer
WHERE c_mktsegment = 'FURNITURE'
LIMIT 10;
```

在這項查詢中，`LIMIT` 子句不會下推至 BigQuery Omni 區域。`FURNITURE` 市場區隔中的所有客戶會先轉移至 BigQuery 區域，然後套用 10 的限制。

## 連接器

您可以使用 BigQuery 連接器，從其他資料處理工具存取 Cloud Storage 中的 BigLake 資料表。舉例來說，您可以從 [Apache Spark](https://github.com/GoogleCloudDataproc/spark-bigquery-connector)、[Apache Hive](https://github.com/GoogleCloudDataproc/hive-bigquery-connector)、[TensorFlow](https://www.tensorflow.org/?hl=zh-tw)、[Trino](https://trino.io/docs/current/connector/bigquery.html) 或 [Presto](https://prestodb.io/docs/current/connector/bigquery.html) 存取 BigLake 資料表中的資料。BigQuery Storage API 會對 BigLake 資料表的所有資料存取活動 (包括透過連接器進行的活動)，強制執行資料列和資料欄層級的控管政策。

舉例來說，下圖說明 [BigQuery Storage API](https://docs.cloud.google.com/bigquery/docs/reference/storage?hl=zh-tw) 如何讓使用者透過 Apache Spark 等開放原始碼查詢引擎，存取自己有權限存取的資料：

如要進一步瞭解 BigQuery 支援的連接器，請參閱「[BigQuery 連接器](https://docs.cloud.google.com/dataproc/docs/concepts/connectors/bigquery?hl=zh-tw)」。

## 物件儲存庫中的 BigLake 資料表

資料湖泊管理員可透過 BigLake 設定資料表的存取控管機制，而非檔案，因此在設定使用者對資料湖泊中資料的存取權時，可提供更精細的選項。

BigLake 資料表可簡化存取控管，因此建議您使用 BigLake 資料表，建立及維護與外部物件儲存庫的連線。

如果不需要管理，或需要臨時探索及操控資料，可以使用[外部資料表](https://docs.cloud.google.com/bigquery/docs/external-tables?hl=zh-tw)。

## 限制

* [外部資料表的所有限制](https://docs.cloud.google.com/bigquery/docs/external-tables?hl=zh-tw#limitations)都適用於 BigLake 資料表。
* 物件儲存庫中的 BigLake 資料表與 BigQuery 資料表受相同限制。詳情請參閱「[配額](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#external_tables)」。
* BigLake 不支援 [Managed Service for Apache Spark 個人叢集驗證](https://docs.cloud.google.com/dataproc/docs/concepts/iam/personal-auth?hl=zh-tw)中範圍縮小的憑證。如要使用啟用個人叢集驗證功能的叢集，請透過空白的[憑證存取權邊界](https://docs.cloud.google.com/managed-spark/docs/concepts/iam/personal-auth?hl=zh-tw#create_a_cluster_and_enable_an_interactive_session)和 `--access-boundary=<(echo -n "{}")` 旗標插入憑證。舉例來說，下列指令會在名為 `myproject` 的專案中，為名為 `mycluster` 的叢集啟用憑證傳播工作階段：

  ```
  gcloud dataproc clusters enable-personal-auth-session \
      --region=us \
      --project=myproject \
      --access-boundary=<(echo -n "{}") \
      mycluster
  ```



  **注意：**如果使用空白的憑證存取權邊界，就少了一層防護，無法抵禦透過 Managed Service for Apache Spark 叢集竊取憑證的攻擊。如果未縮減範圍，遭竊憑證的影響範圍會更大。

  或者，您也可以停用個人叢集驗證，並使用 [Managed Service for Apache Spark 虛擬機器 (VM) 服務帳戶](https://docs.cloud.google.com/dataproc/docs/concepts/configuring-clusters/service-accounts?hl=zh-tw)做為使用者群組的 Proxy。
* BigLake 資料表為唯讀。您無法使用 DML 陳述式或其他方法修改 BigLake 資料表。
* BigLake 資料表支援下列格式：

  + Avro
  + CSV
  + [Delta Lake](https://docs.cloud.google.com/bigquery/docs/create-delta-lake-table?hl=zh-tw)
  + Iceberg
  + JSON
  + ORC
  + Parquet
* 您無法將[快取中繼資料](https://docs.cloud.google.com/bigquery/docs/biglake-intro?hl=zh-tw#metadata_caching_for_performance)與 [Apache Iceberg 外部資料表](https://docs.cloud.google.com/bigquery/docs/iceberg-external-tables?hl=zh-tw)搭配使用；BigQuery 已使用 Iceberg 在資訊清單檔案中擷取的中繼資料。
* [BigQuery Storage API](https://docs.cloud.google.com/bigquery/docs/reference/storage?hl=zh-tw) 不適用於其他雲端環境，例如 AWS 和 Azure。
* 如果使用[快取中繼資料](https://docs.cloud.google.com/bigquery/docs/biglake-intro?hl=zh-tw#metadata_caching_for_performance)，則適用下列限制：

  + [快取中繼資料](https://docs.cloud.google.com/bigquery/docs/biglake-intro?hl=zh-tw#metadata_caching_for_performance)只能用於採用 Avro、ORC、Parquet、JSON 和 CSV 格式的 BigLake 資料表。
  + 如果您在 Amazon S3 中建立、更新或刪除檔案，則查詢檔案時不會傳回更新後的資料，直到下次重新整理中繼資料快取為止。這可能會導致非預期的結果。
    舉例來說，如果您刪除檔案並寫入新檔案，查詢結果可能會排除舊檔案和新檔案，具體取決於快取中繼資料上次更新的時間。
  + 如果 BigLake 資料表參照 Amazon S3 或 Blob 儲存體資料，則不支援搭配使用客戶自行管理的加密金鑰 (CMEK) 和快取中繼資料。

## 安全性模型

BigLake 資料表可讓您透過存取權委派功能，查詢外部資料儲存庫中的結構化資料。存取權委派功能會將 BigLake 資料表的存取權，與基礎資料儲存庫的存取權分開。與服務帳戶相關聯的[外部連線](https://docs.cloud.google.com/bigquery/docs/connections-api-intro?hl=zh-tw)，用於連線至資料儲存庫。由於服務帳戶會處理從資料儲存庫擷取資料的作業，因此您只需授予使用者 BigLake 資料表的存取權。這可讓您在資料表層級強制執行精細的安全防護機制，包括[資料列層級](https://docs.cloud.google.com/bigquery/docs/row-level-security-intro?hl=zh-tw)和[資料欄層級](https://docs.cloud.google.com/bigquery/docs/column-level-security-intro?hl=zh-tw)安全性。如果是以 Cloud Storage 為基礎的 BigLake 資料表，您也可以使用[動態資料遮蓋](https://docs.cloud.google.com/bigquery/docs/column-data-masking?hl=zh-tw)。如要進一步瞭解如何使用 BigLake 資料表搭配 Amazon S3 或 Blob 儲存體資料的多雲端分析解決方案，請參閱「[BigQuery Omni](https://docs.cloud.google.com/bigquery/docs/omni-introduction?hl=zh-tw)」。

管理及使用 BigLake 資料表時，通常會涉及下列組織角色：

* **資料湖泊管理員**：這類管理員通常會管理 Cloud Storage bucket 和物件的身分與存取權管理 (IAM) 政策。
* **資料倉儲管理員：**這類管理員通常會建立、刪除及更新資料表。
* **資料分析師：**分析人員通常會讀取資料及執行查詢。

資料湖泊管理員負責建立連線，並與資料倉儲管理員共用。資料倉儲管理員則會建立資料表、設定適當的存取控管機制，並與資料分析師共用資料表。

**注意：**資料分析師**不應**具備下列權限：

* 直接從 Cloud Storage 讀取物件的能力 (請參閱 [Storage 物件檢視者 IAM 角色](https://docs.cloud.google.com/storage/docs/access-control/iam-roles?hl=zh-tw))，可讓資料分析師規避資料倉儲管理員設定的存取控管機制。
* 可將資料表繫結至連線 (例如 BigQuery 連線管理員)。

  否則，資料分析師可以建立沒有任何存取控管機制的新資料表，進而規避資料倉儲管理員設定的控管機制。

## 中繼資料快取，提升效能

您可以使用快取中繼資料，提升某些類型 BigLake 資料表的查詢效能。如果您要處理大量檔案，或資料已進行 Hive 分區，中繼資料快取功能就特別實用。下列類型的 BigLake 資料表支援中繼資料快取：

* Amazon S3 BigLake 資料表
* Cloud Storage BigLake 資料表

BigQuery 使用 CMETA 做為分散式中繼資料系統，有效率地處理大型資料表。CMETA 提供資料欄和區塊層級的精細中繼資料，可透過系統資料表存取。這個系統會最佳化資料存取和處理作業，進而提升查詢效能。為進一步提升大型資料表的查詢效能，BigQuery 會維護中繼資料快取。CMETA 重新整理工作會讓這個快取保持在最新狀態。

中繼資料包括檔案名稱、分區資訊，以及檔案的實體中繼資料，例如資料列數。您可以選擇是否要啟用資料表的中繼資料快取功能。含有大量檔案和 Apache Hive 分區篩選器的查詢，最能發揮中繼資料快取的效益。

如未啟用中繼資料快取功能，資料表查詢就必須讀取外部資料來源，才能取得物件中繼資料。讀取這類資料會增加查詢延遲時間；從外部資料來源列出數百萬個檔案可能需要幾分鐘的時間。啟用中繼資料快取功能後，查詢作業就不必列出外部資料來源中的檔案，而且能更快分區及剪除檔案。

中繼資料快取也與 Cloud Storage 物件版本管理功能整合。填入或重新整理快取時，系統會根據當時 Cloud Storage 物件的使用中版本擷取中繼資料。因此，啟用中繼資料快取的查詢會讀取與特定快取物件版本對應的資料，即使 Cloud Storage 中有較新的版本也一樣。如要存取 Cloud Storage 中後續更新的物件版本資料，必須重新整理中繼資料快取。

有兩個屬性可控制這項功能：

* **最大過時時間**指定查詢使用快取中繼資料的時間。
* **中繼資料快取模式**會指定中繼資料的收集方式。

啟用中繼資料快取功能後，您可以指定資料表作業可接受的中繼資料過時時間間隔上限。舉例來說，如果您指定 1 小時的間隔，則資料表作業會使用過去一小時內重新整理的快取中繼資料。如果快取的中繼資料超過這個時間，作業就會改為從資料儲存庫 (Amazon S3 或 Cloud Storage) 擷取中繼資料。您可以指定 30 分鐘至 7 天的過時間隔。

為 BigLake 或物件資料表啟用中繼資料快取時，BigQuery 會觸發中繼資料生成重新整理工作。您可以選擇自動或手動重新整理快取：

* 如果是自動重新整理，快取會按照系統定義的時間間隔重新整理，通常介於 30 到 60 分鐘之間。如果資料儲存庫中的檔案會不定期新增、刪除或修改，自動重新整理快取是不錯的做法。如需控制重新整理的時間點 (例如在擷取、轉換和載入工作結束時觸發重新整理)，請使用手動重新整理。
* 如要手動重新整理，請執行 [`BQ.REFRESH_EXTERNAL_METADATA_CACHE` 系統程序](https://docs.cloud.google.com/bigquery/docs/reference/system-procedures?hl=zh-tw#bqrefresh_external_metadata_cache)，按照符合需求的時間表重新整理中繼資料快取。如果是 BigLake 資料表，您可以提供資料表資料目錄的子目錄，選擇性重新整理中繼資料。這樣一來，您就能避免不必要的中繼資料處理。如果資料儲存庫中的檔案會以已知間隔新增、刪除或修改 (例如做為管道的輸出內容)，手動重新整理快取是不錯的做法。

  如果同時發出多個手動重新整理要求，只有一個會成功。

如果未重新整理，中繼資料快取會在 7 天後過期。

手動和自動快取重新整理都會以 [`INTERACTIVE`](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw) 查詢優先順序執行。

### 使用 `BACKGROUND` 預留項目

如果您選擇使用自動重新整理功能，建議您建立[預留項目](https://docs.cloud.google.com/bigquery/docs/reservations-intro?hl=zh-tw)，然後為執行中繼資料快取重新整理工作的專案建立[具有 `BACKGROUND` 工作類型的指派作業](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#assignments)。使用 `BACKGROUND` 預留項目時，重新整理工作會使用專屬資源集區，因此不會與使用者查詢競爭資源，也不會因資源不足而失敗。

雖然使用共用運算單元集區不會產生額外費用，但改用 `BACKGROUND` 預留項目可分配專屬資源集區，提供更穩定的效能，並提高 BigQuery 重新整理工作的可靠性和整體查詢效率。

設定過時時間間隔和中繼資料快取模式值之前，請先考量兩者之間的互動方式。請見以下範例：

* 如果您手動重新整理資料表的中繼資料快取，並將過時時間間隔設為 2 天，則必須每 2 天 (或更短時間) 執行一次 `BQ.REFRESH_EXTERNAL_METADATA_CACHE` 系統程序，才能對資料表執行作業，使用快取的中繼資料。
* 如果您自動重新整理資料表的中繼資料快取，並將過時時間間隔設為 30 分鐘，則對資料表執行的部分作業可能會從資料儲存庫讀取，前提是中繼資料快取重新整理作業所需的時間超過一般的 30 到 60 分鐘。

如要查看中繼資料重新整理工作的相關資訊，請查詢 [`INFORMATION_SCHEMA.JOBS` 檢視表](https://docs.cloud.google.com/bigquery/docs/information-schema-jobs?hl=zh-tw)，如下例所示：

```
SELECT *
FROM `region-us.INFORMATION_SCHEMA.JOBS_BY_PROJECT`
WHERE job_id LIKE '%metadata_cache_refresh%'
AND creation_time > TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 6 HOUR)
ORDER BY start_time DESC
LIMIT 10;
```

如果是以 Parquet 檔案為基礎的 Cloud Storage BigLake 資料表，系統會在重新整理中繼資料快取時收集[資料表統計資料](https://docs.cloud.google.com/bigquery/docs/metadata-caching?hl=zh-tw#table_statistics)，並用於改善查詢計畫。

詳情請參閱「[中繼資料快取](https://docs.cloud.google.com/bigquery/docs/metadata-caching?hl=zh-tw)」。

如要進一步瞭解如何設定中繼資料快取選項，請參閱「[建立 Amazon S3 BigLake 資料表](https://docs.cloud.google.com/bigquery/docs/omni-aws-create-external-table?hl=zh-tw)」或「[建立 Cloud Storage BigLake 資料表](https://docs.cloud.google.com/bigquery/docs/create-cloud-storage-table-biglake?hl=zh-tw)」。

### 啟用快取且含 materialized view 的資料表

您可以[在已啟用 BigLake 中繼資料快取的資料表上使用 materialized view](https://docs.cloud.google.com/bigquery/docs/materialized-views-intro?hl=zh-tw#biglake)，提高查詢 Cloud Storage 或 Amazon Simple Storage Service (Amazon S3) 中結構化資料的效能和效率。這些 materialized view 的運作方式與 BigQuery 代管儲存空間資料表的 materialized view 相同，包括[自動重新整理](https://docs.cloud.google.com/bigquery/docs/materialized-views-manage?hl=zh-tw#automatic-refresh)和[智慧微調](https://docs.cloud.google.com/bigquery/docs/materialized-views-use?hl=zh-tw#smart_tuning)等優點。

## 整合

您可以透過許多其他 BigQuery 功能和 gcloud CLI 服務存取 BigLake 資料表，包括下列重點服務。

### BigQuery sharing (舊稱 Analytics Hub)

BigLake 資料表與共用功能相容。含有 BigLake 資料表的資料集可發布為[共用項目](https://docs.cloud.google.com/bigquery/docs/analytics-hub-introduction?hl=zh-tw#listings)。共用訂閱者可以訂閱這些清單，在專案中佈建唯讀資料集，稱為[*連結資料集*](https://docs.cloud.google.com/bigquery/docs/analytics-hub-introduction?hl=zh-tw#linked_datasets)。訂閱者可以查詢連結資料集中的所有資料表，包括所有 BigLake 資料表。詳情請參閱「[查看及訂閱產品資訊](https://docs.cloud.google.com/bigquery/docs/analytics-hub-view-subscribe-listings?hl=zh-tw)」。

### BigQuery ML

您可以使用 [BigQuery ML](https://docs.cloud.google.com/bigquery/docs/bqml-introduction?hl=zh-tw)，在 Cloud Storage 的 BigLake 中訓練及執行模型。

### Sensitive Data Protection

[Sensitive Data Protection](https://docs.cloud.google.com/sensitive-data-protection/docs?hl=zh-tw) 會掃描 BigLake 資料表，找出機密資料並分類。如果偵測到機密資料，Sensitive Data Protection 去識別化轉換功能可以[遮蓋、刪除或模糊處理](https://docs.cloud.google.com/bigquery/docs/scan-with-dlp?hl=zh-tw)該資料。

## 費用

BigLake 資料表的費用與下列項目有關：

* 查詢資料表。
* [重新整理中繼資料快取](#metadata_caching_for_performance)。

如果您有[預留運算單元](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw)，則查詢外部資料表時不會產生費用。而是會耗用運算單元。

下表說明定價模式如何影響這些費用的套用方式：

|  | **隨選定價** | **Standard、Enterprise 和 Enterprise Plus 版本** |
| --- | --- | --- |
| 查詢 | 系統會根據使用者查詢[處理的位元組數計費](https://cloud.google.com/bigquery/pricing?hl=zh-tw#on_demand_pricing)。 | [預留項目指派作業中`QUERY`工作類型](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#assignments)的[運算單元](https://cloud.google.com/bigquery/pricing?hl=zh-tw#capacity_compute_analysis_pricing)會在查詢期間耗用。 |
| 手動重新整理中繼資料快取。 | 系統會[根據重新整理快取時處理的位元組數向您收費](https://cloud.google.com/bigquery/pricing?hl=zh-tw#on_demand_pricing)。 | [預留項目指派作業中`QUERY`工作類型的[運算單元](https://cloud.google.com/bigquery/pricing?hl=zh-tw#capacity_compute_analysis_pricing)](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#assignments)，會在快取重新整理期間耗用。 |
| 自動重新整理中繼資料快取。 | 系統會[根據重新整理快取時處理的位元組數向您收費](https://cloud.google.com/bigquery/pricing?hl=zh-tw#on_demand_pricing)。 | [預留項目指派作業中`BACKGROUND`工作類型的[運算單元](https://cloud.google.com/bigquery/pricing?hl=zh-tw#capacity_compute_analysis_pricing)](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#assignments)，會在快取重新整理期間耗用。    如果沒有可用的 `BACKGROUND` 預留項目來重新整理中繼資料快取，且您使用的是 Enterprise 或 Enterprise Plus 版本，BigQuery 會自動改用 `QUERY` 預留項目中的運算單元。 |

此外，[Cloud Storage](https://cloud.google.com/storage/pricing?hl=zh-tw)、[Amazon S3](https://aws.amazon.com/s3/pricing/) 和 [Azure Blob Storage](https://azure.microsoft.com/pricing/details/storage/blobs/) 也會根據各產品的定價指南，向您收取儲存空間和資料存取費用。

BigQuery 與 Cloud Storage 互動時，可能會產生下列 Cloud Storage 費用：

* 資料儲存費用，依儲存的資料量計算。
* 存取 [Nearline](https://docs.cloud.google.com/storage/docs/storage-classes?hl=zh-tw#nearline)、[Coldline](https://docs.cloud.google.com/storage/docs/storage-classes?hl=zh-tw#coldline) 和 [Archive](https://docs.cloud.google.com/storage/docs/storage-classes?hl=zh-tw#archive) 儲存空間級別中的資料時，會產生資料擷取費用。對這些儲存空間級別查詢資料表或重新整理中繼資料快取時，請務必謹慎，因為費用可能相當高昂。
* 跨區域讀取資料的網路用量費用，例如 BigQuery 資料集和 Cloud Storage bucket 位於不同區域時。
* 資料處理費用。不過，BigQuery 代表您發出的 API 呼叫 (例如列出或取得資源) 不會產生費用。

## 後續步驟

* 瞭解如何[將外部資料表升級為 BigLake 資料表](https://docs.cloud.google.com/bigquery/docs/external-data-cloud-storage?hl=zh-tw#upgrade-external-tables-to-biglake-tables)。
* 瞭解如何[建立 Cloud Storage BigLake 資料表](https://docs.cloud.google.com/bigquery/docs/create-cloud-storage-table-biglake?hl=zh-tw)。
* 瞭解如何[建立 Amazon S3 BigLake 資料表](https://docs.cloud.google.com/bigquery/docs/omni-aws-create-external-table?hl=zh-tw)。
* 瞭解如何[建立 Blob 儲存體 BigLake 資料表](https://docs.cloud.google.com/bigquery/docs/omni-azure-create-external-table?hl=zh-tw)。
* 瞭解如何[使用 Knowledge Catalog 建立資料品質檢查](https://docs.cloud.google.com/bigquery/docs/dataplex-shared-introduction?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-10-22 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-10-22 (世界標準時間)。"],[],[]]