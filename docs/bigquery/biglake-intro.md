Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# BigLake 外部資料表簡介

本文將概述 BigLake，並假設您熟悉資料庫表格和 Identity and Access Management (IAM)。如要查詢[支援的資料儲存庫](#supported-data-stores)中儲存的資料，請先建立 BigLake 資料表，然後使用 GoogleSQL 語法查詢：

* [建立 Cloud Storage BigLake 資料表](https://docs.cloud.google.com/bigquery/docs/create-cloud-storage-table-biglake?hl=zh-tw)，然後[查詢](https://docs.cloud.google.com/bigquery/docs/query-cloud-storage-using-biglake?hl=zh-tw)。
* [建立 Amazon S3 BigLake 資料表](https://docs.cloud.google.com/bigquery/docs/omni-aws-create-external-table?hl=zh-tw)，然後[查詢](https://docs.cloud.google.com/bigquery/docs/omni-aws-introduction?hl=zh-tw)。
* [建立 Azure Blob 儲存體 BigLake 資料表](https://docs.cloud.google.com/bigquery/docs/omni-azure-create-external-table?hl=zh-tw)，然後[查詢](https://docs.cloud.google.com/bigquery/docs/omni-aws-introduction?hl=zh-tw)。

您也可以將外部資料表升級為 BigLake。詳情請參閱「[將外部資料表升級為 BigLake](https://docs.cloud.google.com/bigquery/docs/external-data-cloud-storage?hl=zh-tw#upgrade-external-tables-to-biglake-tables)」。

您可以使用 BigLake 資料表，透過存取權委派功能，查詢外部資料儲存庫中的結構化資料。存取權委派功能可將 BigLake 資料表的存取權，與基礎資料儲存庫的存取權分開。系統會使用與服務帳戶相關聯的[外部連線](https://docs.cloud.google.com/bigquery/docs/connections-api-intro?hl=zh-tw)，連線至資料儲存庫。由於服務帳戶會負責從資料儲存庫擷取資料，您只需要授予使用者 BigLake 資料表的存取權。這項功能可讓您在資料表層級強制執行精細的安全性，包括[資料列層級](https://docs.cloud.google.com/bigquery/docs/row-level-security-intro?hl=zh-tw)和[資料欄層級](https://docs.cloud.google.com/bigquery/docs/column-level-security-intro?hl=zh-tw)安全性。如果是以 Cloud Storage 為基礎的 BigLake 資料表，您也可以使用[動態資料遮蓋](https://docs.cloud.google.com/bigquery/docs/column-data-masking?hl=zh-tw)。如要進一步瞭解如何使用 BigLake 資料表和 Amazon S3 或 Blob 儲存體資料，打造多雲端數據分析解決方案，請參閱 [BigQuery Omni](https://docs.cloud.google.com/bigquery/docs/omni-introduction?hl=zh-tw)。

## 支援的資料儲存庫

您可以在下列資料儲存庫中使用 BigLake 資料表：

* 使用 [BigQuery Omni](https://docs.cloud.google.com/bigquery/docs/omni-introduction?hl=zh-tw) 存取 [Amazon S3](https://docs.cloud.google.com/bigquery/docs/omni-aws-introduction?hl=zh-tw)
* 使用 [BigQuery Omni](https://docs.cloud.google.com/bigquery/docs/omni-introduction?hl=zh-tw) 存取 [Blob 儲存體](https://docs.cloud.google.com/bigquery/docs/omni-azure-introduction?hl=zh-tw)
* [Cloud Storage](https://docs.cloud.google.com/bigquery/docs/query-cloud-storage-using-biglake?hl=zh-tw)

## 支援臨時資料表

以 Cloud Storage 為基礎的 BigLake 資料表可以是臨時或永久資料表。以 Amazon S3 或 Blob 儲存空間為基礎的 BigLake 資料表必須是永久資料表。

## 多個來源檔案

您可以根據多個外部資料來源建立 BigLake 資料表，前提是這些資料來源具有相同結構定義。

## 跨雲端聯結

透過跨雲端聯結，您可以執行查詢，涵蓋 Google Cloud 和 BigQuery Omni 地區。您可以使用 [GoogleSQL `JOIN` 作業](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw#join_types)，分析 AWS、Azure、公開資料集和其他 Google Cloud 服務等各種儲存解決方案中的資料。跨雲端聯結
可免除在執行查詢前複製跨來源資料的需要。

您可以在 `SELECT` 陳述式中參照 BigLake 資料表，就像參照標準 BigQuery 資料表一樣，包括在[資料操縱語言 (DML)](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/dml-syntax?hl=zh-tw) 和[資料定義語言 (DDL)](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw) 陳述式中，使用子查詢擷取資料。您可以在同一個查詢中使用來自不同雲端的 BigLake 資料表和 BigQuery 資料表。所有 BigQuery 資料表都必須位於同一個地區。

### 跨雲端加入所需的權限

如要取得執行跨雲端聯結所需的權限，請要求系統管理員在執行聯結的專案中，授予您下列 IAM 角色：

* [BigQuery 資料檢視者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.dataViewer)  (`roles/bigquery.dataViewer`)
* [BigQuery 工作使用者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.jobUser)  (`roles/bigquery.jobUser`)

如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

這些預先定義的角色具備執行跨雲端聯結所需的權限。如要查看確切的必要權限，請展開「Required permissions」(必要權限) 部分：

#### 所需權限

如要執行跨雲端聯播，必須具備下列權限：

* `bigquery.jobs.create`
* `bigquery.tables.getData`

您或許還可透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)取得這些權限。

### 跨雲端聯結費用

執行跨雲端聯結作業時，BigQuery 會將查詢剖析為本機和遠端部分。系統會將本機部分視為 BigQuery 地區的標準查詢。遠端部分會轉換為 BigQuery Omni 區域中參照的 BigLake 資料表上的 `CREATE TABLE AS SELECT` (CTAS) 作業，這會在 BigQuery 區域中建立臨時資料表。BigQuery 接著會使用這個臨時資料表執行跨雲端聯結，並在八小時後自動刪除該資料表。

您必須支付參照 BigLake 表格中資料的資料移轉費用。不過，BigQuery 只會傳輸查詢中參照的 BigLake 資料表資料欄和資料列，而非整個資料表，因此有助於降低這些成本。建議您指定盡可能範圍較窄的資料欄篩選器，進一步降低傳輸成本。CTAS 工作會顯示在工作記錄中，並顯示轉移的位元組數等資訊。即使主要查詢工作失敗，成功轉移的資料仍會產生費用。詳情請參閱 [BigQuery Omni 定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#bqomni)。

以以下查詢為例：

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

這個範例有兩項轉移作業：一項來自員工資料表 (附有層級篩選器)，另一項來自現職員工資料表。移轉完成後，系統會在 BigQuery 區域執行聯結。如果其中一項移轉作業失敗，另一項成功，系統仍會針對成功移轉的作業收取資料移轉費用。

### 跨雲端聯結限制

* BigQuery[免費方案](https://cloud.google.com/bigquery/pricing?hl=zh-tw#free-tier)和 [BigQuery 沙箱](https://docs.cloud.google.com/bigquery/docs/sandbox?hl=zh-tw)不支援跨雲端聯結。
* 如果查詢包含 `JOIN` 陳述式，匯總作業可能不會下推至 BigQuery Omni 區域。
* 每個暫時性資料表只會用於單一跨雲端查詢，即使重複執行相同的查詢多次，也不會重複使用。
* 每筆轉移作業的大小上限為 60 GB。具體來說，如果您對 BigLake 資料表套用篩選器並載入結果，結果大小必須小於 60 GB。如有需要，您可以[申請調整配額](https://docs.cloud.google.com/docs/quotas/help/request_increase?hl=zh-tw)。掃描的位元組沒有限制。
* 跨雲端聯結查詢會採用查詢速率的內部配額。如果查詢率超過配額，您可能會收到 `All our servers are busy processing data transferred between regions` 錯誤。在大多數情況下，重新嘗試查詢即可解決問題。如要提高內部配額，以支援更高的查詢率，請與支援團隊聯絡。
* 只有[與對應 BigQuery Omni 區域位於同一位置的 BigQuery 區域](https://docs.cloud.google.com/bigquery/docs/omni-introduction?hl=zh-tw#locations)，以及 `US` 和 `EU` 多區域，才支援跨雲端聯結。在 `US` 或 `EU` 多區域執行的跨雲端聯結，只能存取美國或歐盟 BigQuery Omni 區域的資料。
* 如果跨雲端聯結查詢參照 BigQuery Omni 地區的 10 個以上資料集，可能會失敗並顯示 `Not found: Dataset <BigQuery dataset> was not found in
  location <BigQuery Omni region>` 錯誤。為避免這個問題，建議您在執行參照超過 10 個資料集的跨雲端聯結時，[明確指定位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw#specify_locations)。請注意，如果您明確指定 BigQuery 區域，且查詢只包含 BigLake 資料表，則查詢會以跨雲端查詢的形式執行，並產生資料移轉費用。
* 您無法使用跨雲端聯結[查詢 `_FILE_NAME` 虛擬資料欄](https://docs.cloud.google.com/bigquery/docs/query-aws-data?hl=zh-tw#query_the_file_name_pseudo-column)。
* 在 `WHERE` 子句中參照 BigLake 資料表的資料欄時，無法使用 `INTERVAL` 或 `RANGE` 常值。
* 跨雲端聯結工作不會回報從其他雲端處理及轉移的位元組數。這項資訊會顯示在跨雲端查詢執行作業建立的子 CTAS 工作中。
* 參照 BigQuery Omni 資料表或檢視區塊的[授權檢視區塊](https://docs.cloud.google.com/bigquery/docs/authorized-views?hl=zh-tw)和[授權常式](https://docs.cloud.google.com/bigquery/docs/authorized-routines?hl=zh-tw)，僅支援 BigQuery Omni 區域。
* 如果跨雲端查詢參照 `STRUCT` 或 `JSON` 資料欄，系統不會對任何遠端子查詢套用下推作業。為提升效能，建議在 BigQuery Omni 區域中建立檢視區塊，篩選 `STRUCT` 和 `JSON` 資料欄，並只傳回必要欄位做為個別資料欄。
* 跨雲端聯結不支援[排序規則](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/collation-concepts?hl=zh-tw)。
* 跨雲端聯結不支援使用 `ORDER BY` 子句聯結 Omni 檢視區塊。

### 跨雲端聯結範例

下列查詢會將 BigQuery 地區中的 `orders` 資料表，與 BigQuery Omni 地區中的 `lineitem` 資料表聯結：

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

這項查詢分為本機和遠端部分。系統會先將下列查詢傳送至 BigQuery Omni 區域執行。結果是 BigQuery 地區中的暫時資料表。您可以在工作記錄中查看這項子項 CTAS 工作及其相關中繼資料。

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

建立臨時表後，`JOIN` 作業會完成，並執行下列查詢：

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

再舉一例，請看下列跨雲端聯結：

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

在這項查詢中，`LIMIT` 子句不會下推至 BigQuery Omni 區域。`FURNITURE` 市場區隔的所有客戶會先移轉至 BigQuery 區域，然後套用 10 個的限制。

## 連接器

您可以使用 BigQuery 連接器，透過其他資料處理工具存取 BigLake 資料表中的資料 (以 Cloud Storage 為基礎)。舉例來說，您可以透過 [Apache Spark](https://github.com/GoogleCloudDataproc/spark-bigquery-connector)、[Apache Hive](https://github.com/GoogleCloudDataproc/hive-bigquery-connector)、[TensorFlow](https://www.tensorflow.org/?hl=zh-tw)、[Trino](https://trino.io/docs/current/connector/bigquery.html) 或 [Presto](https://prestodb.io/docs/current/connector/bigquery.html) 存取 BigLake 資料表中的資料。BigQuery Storage API 會對 BigLake 資料表的所有資料存取權 (包括透過連接器存取) 強制執行列層級和欄層級管理政策。

舉例來說，下圖說明 [BigQuery Storage API](https://docs.cloud.google.com/bigquery/docs/reference/storage?hl=zh-tw) 如何讓使用者透過 Apache Spark 等開放原始碼查詢引擎，存取自己有權限存取的資料：

如要進一步瞭解 BigQuery 支援的連接器，請參閱「[BigQuery 連接器](https://docs.cloud.google.com/dataproc/docs/concepts/connectors/bigquery?hl=zh-tw)」。

## 物件儲存空間中的 BigLake 資料表

對於資料湖泊管理員，BigLake 可讓您在資料表而非檔案上設定存取權控管機制，在設定使用者存取資料湖泊中的資料時，提供更精細的選項。

由於 BigLake 資料表可簡化存取控管，因此建議使用 BigLake 資料表，建立及維護與外部物件儲存空間的連線。

如果不需要控管，或是要臨時探索及操控資料，可以使用[外部資料表](https://docs.cloud.google.com/bigquery/docs/external-tables?hl=zh-tw)。

## 限制

* 所有[外部資料表限制](https://docs.cloud.google.com/bigquery/docs/external-tables?hl=zh-tw#limitations)均適用於 BigLake 資料表。
* 物件儲存空間中的 BigLake 資料表與 BigQuery 資料表一樣，詳情請參閱「[配額](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#external_tables)」。
* BigLake 不支援來自「[Managed Service for Apache Spark 個人叢集驗證](https://docs.cloud.google.com/dataproc/docs/concepts/iam/personal-auth?hl=zh-tw)」的範圍縮減憑證。如要使用啟用個人叢集驗證功能的叢集，請使用空白的[憑證存取權界線](https://cloud.google.com/dataproc/docs/concepts/iam/personal-auth?hl=zh-tw#create_a_cluster_and_enable_an_interactive_session)搭配 `--access-boundary=<(echo -n "{}")` 旗標，插入您的憑證。舉例來說，下列指令會在名為 `myproject` 的專案中，為名為 `mycluster` 的叢集啟用憑證傳播工作階段：

  ```
  gcloud dataproc clusters enable-personal-auth-session \
      --region=us \
      --project=myproject \
      --access-boundary=<(echo -n "{}") \
      mycluster
  ```



  **注意：**使用空白的憑證存取邊界，會移除一層防護機制，避免透過 Managed Service for Apache Spark 叢集遭竊的憑證發動攻擊。如果沒有縮減範圍，遭竊憑證的影響範圍會更大。

  或者，您也可以停用個人叢集驗證，並使用 [Managed Service for Apache Spark 虛擬機器 (VM) 服務帳戶](https://docs.cloud.google.com/dataproc/docs/concepts/configuring-clusters/service-accounts?hl=zh-tw)做為使用者群組的 Proxy。
* BigLake 資料表為唯讀，您無法使用 DML 陳述式或其他方法修改 BigLake 資料表。
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

  + 您只能搭配使用 [快取中繼資料](https://docs.cloud.google.com/bigquery/docs/biglake-intro?hl=zh-tw#metadata_caching_for_performance)與使用 Avro、ORC、Parquet、JSON 和 CSV 格式的 BigLake 資料表。
  + 如果您在 Amazon S3 中建立、更新或刪除檔案，查詢檔案時，系統不會傳回更新後的資料，直到下次重新整理中繼資料快取為止。這可能會導致非預期的結果。舉例來說，如果您刪除檔案並寫入新檔案，查詢結果可能會排除舊檔案和新檔案，具體情況取決於快取中繼資料上次更新的時間。
  + 如果 BigLake 資料表參照 Amazon S3 或 Blob Storage 資料，則不支援搭配快取中繼資料使用客戶自行管理的加密金鑰 (CMEK)。

## 安全性模型

管理及使用 BigLake 表格時，通常會涉及下列機構角色：

* **資料湖泊管理員**：這類管理員通常會管理 Cloud Storage 值區和物件的身分與存取權管理 (IAM) 政策。
* **資料倉儲管理員**。這類管理員通常會建立、刪除及更新資料表。
* **資料分析師**：分析師通常會讀取資料及執行查詢。

資料湖泊管理員負責建立連線，並與資料倉儲管理員共用連線。資料倉儲管理員則會建立資料表、設定適當的存取權控管機制，並與資料分析師共用資料表。

**注意：**資料分析師**不應**具備下列權限：

* 直接從 Cloud Storage 讀取物件 (請參閱[儲存空間物件檢視者 IAM 角色](https://docs.cloud.google.com/storage/docs/access-control/iam-roles?hl=zh-tw))，讓資料分析師規避資料倉儲管理員設定的存取控管。
* 將資料表繫結至連線 (例如 BigQuery 連線管理員)。

  否則，資料分析師可以建立沒有任何存取權控管的新資料表，藉此規避資料倉儲管理員設定的控管機制。

## 中繼資料快取功能可提升效能

您可以使用快取中繼資料，提升某些 BigLake 資料表的查詢效能。如果您要處理大量檔案，或是資料已進行 Hive 分割，中繼資料快取功能就特別實用。下列類型的 BigLake 資料表支援中繼資料快取：

* Amazon S3 BigLake 資料表
* Cloud Storage BigLake 資料表

BigQuery 使用 CMETA 做為分散式中繼資料系統，有效處理大型資料表。CMETA 提供資料欄和區塊層級的精細中繼資料，可透過系統資料表存取。這個系統會最佳化資料存取和處理程序，進而提升查詢效能。為進一步提升大型資料表的查詢效能，BigQuery 會維護中繼資料快取。CMETA 重新整理作業會讓這個快取保持在最新狀態。

中繼資料包括檔案名稱、分區資訊，以及來自檔案的實體中繼資料，例如列數。你可以選擇是否在資料表上啟用中繼資料快取功能。如果查詢的檔案數量龐大，且包含 Apache Hive 分區篩選器，中繼資料快取功能就能發揮最大效益。

如果未啟用中繼資料快取，查詢資料表時必須讀取外部資料來源，才能取得物件中繼資料。讀取這項資料會增加查詢延遲時間；從外部資料來源列出數百萬個檔案可能需要幾分鐘。啟用中繼資料快取功能後，查詢作業就能避免列出外部資料來源中的檔案，並更快地分割及修剪檔案。

中繼資料快取也會與 Cloud Storage 物件版本管理功能整合。快取填入或重新整理時，會根據當時 Cloud Storage 物件的即時版本擷取中繼資料。因此，即使 Cloud Storage 中有較新的使用中版本，啟用中繼資料快取的查詢作業仍會讀取與特定快取物件版本相應的資料。如要存取 Cloud Storage 中任何後續更新的物件版本資料，必須重新整理中繼資料快取。

有兩個屬性可控制這項功能：

* **最大過時程度**：指定查詢何時使用快取中繼資料。
* 「中繼資料快取模式」會指定中繼資料的收集方式。

啟用中繼資料快取時，您可以指定可接受的資料表作業中繼資料過時間隔上限。舉例來說，如果指定間隔為 1 小時，則對資料表執行的作業會使用快取中繼資料 (如果該資料在過去 1 小時內已重新整理)。如果快取中繼資料的舊於該時間，作業會改為從資料存放區 (Amazon S3 或 Cloud Storage) 擷取中繼資料。過時間隔可指定的範圍為 30 分鐘至 7 天。

為 BigLake 或物件資料表啟用中繼資料快取時，BigQuery 會觸發中繼資料產生重新整理工作。你可以選擇自動或手動重新整理快取：

* 如果是自動重新整理，系統會以定義的間隔重新整理快取，通常是 30 到 60 分鐘。如果資料存放區中的檔案是以隨機間隔新增、刪除或修改，建議自動重新整理快取。如要控管重新整理時間，例如在擷取、轉換及載入作業結束時觸發重新整理，請使用手動重新整理。
* 如要手動重新整理，請執行 [`BQ.REFRESH_EXTERNAL_METADATA_CACHE` 系統程序](https://docs.cloud.google.com/bigquery/docs/reference/system-procedures?hl=zh-tw#bqrefresh_external_metadata_cache)，按照符合您需求的排程重新整理中繼資料快取。如果是 BigLake 資料表，您可以提供資料表資料目錄的子目錄，選擇性地重新整理中繼資料。這樣一來，您就能避免處理不必要的中繼資料。如果資料存放區中的檔案是以已知間隔新增、刪除或修改 (例如管道的輸出內容)，手動重新整理快取是不錯的做法。

  如果您同時發出多個手動重新整理要求，只有一個會成功。

如果未重新整理，中繼資料快取會在 7 天後過期。

手動和自動重新整理快取時，都會以 [`INTERACTIVE`](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw) 查詢優先順序執行。

### 使用 `BACKGROUND` 預留項目

如果選擇使用自動重新整理功能，建議您建立[預訂](https://docs.cloud.google.com/bigquery/docs/reservations-intro?hl=zh-tw)，然後為執行中繼資料快取重新整理工作的專案，建立[工作類型為 `BACKGROUND` 的指派](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#assignments)。使用`BACKGROUND`預留項目時，重新整理作業會使用專屬資源集區，避免與使用者查詢競爭，並防止作業因資源不足而可能失敗。

使用共用運算單元集區不會產生額外費用，但改用`BACKGROUND`預留資源可分配專屬資源集區，提供更穩定的效能，並提升 BigQuery 中的重新整理作業可靠性及整體查詢效率。

設定陳舊間隔和中繼資料快取模式值之前，請先考量這些值之間的互動方式。請見以下範例：

* 如果您要手動重新整理資料表的中繼資料快取，並將過時間隔設為 2 天，則必須每 2 天或更短的時間執行 `BQ.REFRESH_EXTERNAL_METADATA_CACHE` 系統程序，才能讓針對資料表執行的作業使用快取中繼資料。
* 如果您自動重新整理資料表的中繼資料快取，並將過時間隔設為 30 分鐘，則如果中繼資料快取重新整理作業耗時較長 (通常為 30 到 60 分鐘)，您對資料表執行的部分作業可能會從資料儲存庫讀取資料。

如要查詢中繼資料重新整理作業的相關資訊，請查詢 [`INFORMATION_SCHEMA.JOBS` 檢視區塊](https://docs.cloud.google.com/bigquery/docs/information-schema-jobs?hl=zh-tw)，如下列範例所示：

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

### 具體化檢視表搭配啟用快取的資料表

您可以[透過啟用 BigLake 中繼資料快取功能的資料表使用具體化檢視表](https://docs.cloud.google.com/bigquery/docs/materialized-views-intro?hl=zh-tw#biglake)，在查詢儲存在 Cloud Storage 或 Amazon Simple Storage Service (Amazon S3) 中的結構化資料時，提升效能和效率。這些具體化檢視區塊的功能與 BigQuery 管理的儲存空間資料表上的具體化檢視區塊類似，包括[自動重新整理](https://docs.cloud.google.com/bigquery/docs/materialized-views-manage?hl=zh-tw#automatic-refresh)和[智慧微調](https://docs.cloud.google.com/bigquery/docs/materialized-views-use?hl=zh-tw#smart_tuning)等優點。

## 整合

您可以透過許多其他 BigQuery 功能和 gcloud CLI 服務存取 BigLake 資料表，包括下列服務 (以醒目顯示)。

### BigQuery sharing (舊稱 Analytics Hub)

BigLake 資料表與共用功能相容。含有 BigLake 資料表的資料集可以發布為[共用項目](https://docs.cloud.google.com/bigquery/docs/analytics-hub-introduction?hl=zh-tw#listings)。共用訂閱者可以訂閱這些資訊，在專案中佈建唯讀資料集 (稱為[*連結資料集*](https://docs.cloud.google.com/bigquery/docs/analytics-hub-introduction?hl=zh-tw#linked_datasets))。訂閱者可以查詢連結資料集中的所有資料表，包括所有 BigLake 資料表。詳情請參閱「[查看及訂閱房源資訊](https://docs.cloud.google.com/bigquery/docs/analytics-hub-view-subscribe-listings?hl=zh-tw)」。

### BigQuery ML

您可以使用 [BigQuery ML](https://docs.cloud.google.com/bigquery/docs/bqml-introduction?hl=zh-tw)，在 Cloud Storage 中的 BigLake 上訓練及執行模型。

### Sensitive Data Protection

[Sensitive Data Protection](https://docs.cloud.google.com/sensitive-data-protection/docs?hl=zh-tw) 會掃描 BigLake 資料表，找出並分類機密資料。如果偵測到機密資料，Sensitive Data Protection 去識別化轉換可以[遮蓋、刪除或隱藏](https://docs.cloud.google.com/bigquery/docs/scan-with-dlp?hl=zh-tw)該資料。

## 費用

BigLake 資料表有以下相關費用：

* 查詢資料表。
* [重新整理中繼資料快取](#metadata_caching_for_performance)。

如果您有[運算單元預留](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw)，查詢外部資料表時不會產生費用。而是會耗用這些查詢的配額。

下表說明定價模式如何影響這些費用的適用方式：

|  | **以量計價** | **Standard、Enterprise 和 Enterprise Plus 版本** |
| --- | --- | --- |
| 查詢 | 系統會[根據使用者查詢處理的位元組數](https://cloud.google.com/bigquery/pricing?hl=zh-tw#on_demand_pricing)向您收費。 | 查詢期間會耗用[保留項目指派中[運算單元](https://cloud.google.com/bigquery/pricing?hl=zh-tw#capacity_compute_analysis_pricing)的`QUERY`工作類型](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#assignments)。 |
| 手動重新整理中繼資料快取。 | 系統會[針對重新整理快取所處理的位元組向您收費](https://cloud.google.com/bigquery/pricing?hl=zh-tw#on_demand_pricing)。 | 快取重新整理期間會耗用[指派給`QUERY`工作類型](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#assignments)的[運算單元](https://cloud.google.com/bigquery/pricing?hl=zh-tw#capacity_compute_analysis_pricing)。 |
| 自動重新整理中繼資料快取。 | 系統會[針對重新整理快取所處理的位元組向您收費](https://cloud.google.com/bigquery/pricing?hl=zh-tw#on_demand_pricing)。 | 快取重新整理期間會耗用[指派給`BACKGROUND`工作類型](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#assignments)的[運算單元](https://cloud.google.com/bigquery/pricing?hl=zh-tw#capacity_compute_analysis_pricing)。    如果沒有可用的 `BACKGROUND` 預留項目來重新整理中繼資料快取，且您使用的是 Enterprise 或 Enterprise Plus 版本，BigQuery 會自動改用 `QUERY` 預留項目中的運算單元。 |

系統也會依據各產品的價格規定，針對 [Cloud Storage](https://cloud.google.com/storage/pricing?hl=zh-tw)、[Amazon S3](https://aws.amazon.com/s3/pricing/) 和 [Azure Blob Storage](https://azure.microsoft.com/pricing/details/storage/blobs/) 的儲存空間和資料存取權向您收費。

BigQuery 與 Cloud Storage 互動時，可能會產生下列 Cloud Storage 費用：

* 儲存資料的資料儲存費用。
* 存取 [Nearline](https://docs.cloud.google.com/storage/docs/storage-classes?hl=zh-tw#nearline)、[Coldline](https://docs.cloud.google.com/storage/docs/storage-classes?hl=zh-tw#coldline) 和 [Archive](https://docs.cloud.google.com/storage/docs/storage-classes?hl=zh-tw#archive) 儲存空間級別中的資料時，會產生資料擷取費用。對這些儲存空間類別查詢資料表或重新整理中繼資料快取時，請務必謹慎操作，因為費用可能相當高昂。
* 跨區域讀取資料時的網路用量費用，例如 BigQuery 資料集和 Cloud Storage bucket 位於不同區域時。
* 資料處理費用。不過，如果是 BigQuery 代表您發出的 API 呼叫 (例如列出或取得資源)，則不會收取費用。

## 後續步驟

* 瞭解如何[將外部資料表升級為 BigLake 資料表](https://docs.cloud.google.com/bigquery/docs/external-data-cloud-storage?hl=zh-tw#upgrade-external-tables-to-biglake-tables)。
* 瞭解如何[建立 Cloud Storage BigLake 資料表](https://docs.cloud.google.com/bigquery/docs/create-cloud-storage-table-biglake?hl=zh-tw)。
* 瞭解如何[建立 Amazon S3 BigLake 資料表](https://docs.cloud.google.com/bigquery/docs/omni-aws-create-external-table?hl=zh-tw)。
* 瞭解如何[建立 Blob 儲存體 BigLake 資料表](https://docs.cloud.google.com/bigquery/docs/omni-azure-create-external-table?hl=zh-tw)。
* 瞭解如何[使用 Knowledge Catalog 建立資料品質檢查](https://docs.cloud.google.com/bigquery/docs/dataplex-shared-introduction?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-06 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-06 (世界標準時間)。"],[],[]]