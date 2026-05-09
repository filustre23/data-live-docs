Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 透過跨雲端作業載入資料

BigQuery 管理員或分析師可以將 Amazon Simple Storage Service (Amazon S3) 值區或 Azure Blob 儲存空間中的資料載入 [BigQuery 資料表](https://docs.cloud.google.com/bigquery/docs/tables-intro?hl=zh-tw#standard-tables)。您可以將移轉的資料與Google Cloud 區域中的資料合併，也可以運用 [BigQuery ML](https://docs.cloud.google.com/bigquery/docs/bqml-introduction?hl=zh-tw) 等 BigQuery 功能。您也可以建立特定外部來源的具體化檢視表副本，讓該資料可在 BigQuery 中使用。

您可以透過下列方式將資料移轉至 BigQuery：

* 使用 [`LOAD DATA` 陳述式](#load-data)，將 Amazon S3 和 Azure Blob 儲存體中檔案的資料移轉至 BigQuery 資料表。
* 使用 [`CREATE TABLE AS SELECT` 陳述式](#filter-data)，先篩選 Amazon S3 或 Blob 儲存空間中的檔案資料，再將結果移轉至 BigQuery 資料表。如要將資料附加至目的地資料表，請使用 [`INSERT INTO SELECT` 陳述式](#filter-data)。資料操作會套用至參照 [Amazon S3](https://docs.cloud.google.com/bigquery/docs/omni-aws-create-external-table?hl=zh-tw) 或 [Blob 儲存空間](https://docs.cloud.google.com/bigquery/docs/omni-azure-create-external-table?hl=zh-tw)資料的外部資料表。
* 在 BigQuery 資料集中建立外部 Amazon S3、Apache Iceberg 或 Salesforce Data Cloud 資料的[具體化檢視](#materialized_view_replicas)副本，讓資料可在 BigQuery 本機使用。

**注意：** 如要定期將大型檔案從 Amazon Simple Storage Service (Amazon S3) 值區或 Azure Blob 儲存空間移轉至 BigQuery 資料表，請使用 [BigQuery 資料移轉服務](https://docs.cloud.google.com/bigquery/docs/dts-introduction?hl=zh-tw)。如要在將資料移轉至 BigQuery 資料表之前讀取及處理資料，請使用 [`CREATE TABLE AS SELECT` 陳述式](#filter-data)。

## 配額與限制

如要瞭解配額和限制，請參閱[查詢工作配額和限制](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#query_jobs)。

## 事前準備

如要授予 Google Cloud 讀取權限，以便載入或篩選其他雲端中的資料，請管理員建立[連線](https://docs.cloud.google.com/bigquery/docs/connections-api-intro?hl=zh-tw)並與您共用。如要瞭解如何建立連線，請參閱「[連結至 Amazon S3](https://docs.cloud.google.com/bigquery/docs/omni-aws-create-connection?hl=zh-tw)」或「[Blob 儲存體](https://docs.cloud.google.com/bigquery/docs/omni-azure-create-connection?hl=zh-tw)」。

### 必要角色

如要取得使用跨雲端移轉功能載入資料所需的權限，請要求系統管理員授予您資料集的「[BigQuery 資料編輯者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.dataEditor) 」(`roles/bigquery.dataEditor`) IAM 角色。如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

這個預先定義的角色具備使用跨雲端轉移功能載入資料所需的權限。如要查看確切的必要權限，請展開「Required permissions」(必要權限) 部分：

#### 所需權限

如要使用跨雲端轉移功能載入資料，必須具備下列權限：

* `bigquery.tables.create`
* `bigquery.tables.get`
* `bigquery.tables.updateData`
* `bigquery.tables.update`
* `bigquery.jobs.create`
* `bigquery.connections.use`

您或許還可透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)取得這些權限。

如要進一步瞭解 BigQuery 中的 IAM 角色，請參閱 [BigQuery IAM 角色和權限](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)。

## 定價

系統會根據[`LOAD`陳述式](#load-data)，向您收取跨雲端傳輸的位元組費用。如要瞭解定價資訊，請參閱 [BigQuery Omni 定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#bqomni)中的「Omni Cross Cloud 資料移轉」一節。

系統會根據 [`CREATE TABLE AS SELECT` 陳述式](#filter-data)或 [`INSERT INTO SELECT` 陳述式](#filter-data)，針對跨雲端傳輸的位元組和[運算容量](https://cloud.google.com/bigquery/pricing?hl=zh-tw#capacity_compute_analysis_pricing)向您收費。

`LOAD` 和 `CREATE TABLE AS SELECT` 陳述式都需要 BigQuery Omni 區域中的時段，才能掃描 Amazon S3 和 Blob 儲存體檔案並載入。詳情請參閱 [BigQuery Omni 定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#bqomni)。

如果是外部資料來源的具體化檢視表副本，費用也可能包括[具體化檢視表定價](https://docs.cloud.google.com/bigquery/docs/materialized-views-intro?hl=zh-tw#materialized_views_pricing)。

## 載入和篩選選項的最佳做法

* 避免載入多個小於 5 MB 的檔案。
  請改為為檔案建立外部資料表，然後將查詢結果匯出至 [Amazon S3](https://docs.cloud.google.com/bigquery/docs/omni-aws-create-external-table?hl=zh-tw) 或 [Blob 儲存體](https://docs.cloud.google.com/bigquery/docs/omni-azure-create-external-table?hl=zh-tw)，即可建立較大的檔案。這個方法有助於縮短資料轉移時間。
如要瞭解查詢結果大小上限，請參閱「[BigQuery Omni 查詢結果大小上限](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#max_result_size_query_omni)」。* 如果來源資料位於 gzip 壓縮檔中，請在建立外部資料表時，將 [`external_table_options.compression`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#external_table_option_list) 選項設為 `GZIP`。

## 載入資料

您可以使用 [`LOAD DATA [INTO|OVERWRITE]` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/load-statements?hl=zh-tw)將資料載入 BigQuery。

### 限制

* 連線和目的地資料集必須屬於相同專案。系統不支援載入跨專案的資料。
* `LOAD DATA` 僅在將資料從 Amazon Simple Storage Service (Amazon S3) 或 Azure Blob 儲存體移轉至同區 BigQuery 時支援。詳情請參閱「[位置](https://docs.cloud.google.com/bigquery/docs/omni-introduction?hl=zh-tw#locations)」。
  + 您可以將資料從任何 `US` 區域轉移至 `US` 多區域。您也可以從任何`EU`區域轉移至`EU`多區域。

### 範例

#### 範例 1

以下範例會從 Amazon S3 值區將名為 `sample.parquet` 的 Parquet 檔案載入 `test_parquet` 資料表，並自動偵測結構定義：

```
LOAD DATA INTO mydataset.testparquet
  FROM FILES (
    uris = ['s3://test-bucket/sample.parquet'],
    format = 'PARQUET'
  )
  WITH CONNECTION `aws-us-east-1.test-connection`
```

#### 範例 2

以下範例會將 Blob 儲存空間中前置字元為 `sampled*` 的 CSV 檔案，載入至 `test_csv` 資料表，並依時間預先定義資料欄分割：

```
LOAD DATA INTO mydataset.test_csv (Number INT64, Name STRING, Time DATE)
  PARTITION BY Time
  FROM FILES (
    format = 'CSV', uris = ['azure://test.blob.core.windows.net/container/sampled*'],
    skip_leading_rows=1
  )
  WITH CONNECTION `azure-eastus2.test-connection`
```

#### 範例 3

以下範例會使用名為 `sample.parquet` 的檔案資料，覆寫現有資料表 `test_parquet`，並自動偵測結構定義：

```
LOAD DATA OVERWRITE mydataset.testparquet
  FROM FILES (
    uris = ['s3://test-bucket/sample.parquet'],
    format = 'PARQUET'
  )
  WITH CONNECTION `aws-us-east-1.test-connection`
```

## 篩選資料

您可以使用 [`CREATE TABLE AS SELECT` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#create_table_statement)和 [`INSERT INTO SELECT` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/dml-syntax?hl=zh-tw#insert_statement)，在將資料移轉至 BigQuery 前進行篩選。

### 限制

* 如果 `SELECT` 查詢的結果超過 60 GiB 的邏輯位元組，查詢就會失敗。系統不會建立資料表，也不會轉移資料。如要瞭解如何減少掃描的資料量，請參閱「[減少查詢處理的資料量](https://docs.cloud.google.com/bigquery/docs/best-practices-performance-communication?hl=zh-tw)」。
* 系統不支援臨時資料表。
* 不支援轉移[知名二進位 (WKB)](https://docs.cloud.google.com/bigquery/docs/geospatial-data?hl=zh-tw) 地理空間資料格式。
* `INSERT INTO SELECT` 陳述式不支援將資料轉移至分群資料表。
* 在 `INSERT INTO SELECT` 陳述式中，如果目的地資料表與 `SELECT` 查詢中的來源資料表相同，則 `INSERT INTO SELECT` 陳述式不會修改目的地資料表中的任何資料列。由於 BigQuery 無法跨區域讀取資料，因此不會修改目的地資料表。
* 只有在從 Amazon S3 或 Blob 儲存體將資料移轉至共置的 BigQuery 區域時，才支援 `CREATE TABLE AS SELECT` 和 `INSERT INTO SELECT`。詳情請參閱「[位置](https://docs.cloud.google.com/bigquery/docs/omni-introduction?hl=zh-tw#locations)」。

  + 您可以將資料從任何 `US` 區域轉移至 `US` 多區域。您也可以從任何`EU`區域轉移至`EU`多區域。

### 範例

#### 範例 1

假設您有名為 `myawsdataset.orders` 的 BigLake 資料表，參照 [Amazon S3](https://docs.cloud.google.com/bigquery/docs/omni-aws-create-external-table?hl=zh-tw) 中的資料。您想將該資料表中的資料轉移至美國多區域的 BigQuery 資料表 `myotherdataset.shipments`。

首先，顯示 `myawsdataset.orders` 資料表的相關資訊：

```
    bq show myawsdataset.orders;
```

輸出結果會與下列內容相似：

```
  Last modified             Schema              Type     Total URIs   Expiration
----------------- -------------------------- ---------- ------------ -----------
  31 Oct 17:40:28   |- l_orderkey: integer     EXTERNAL   1
                    |- l_partkey: integer
                    |- l_suppkey: integer
                    |- l_linenumber: integer
                    |- l_returnflag: string
                    |- l_linestatus: string
                    |- l_commitdate: date
```

接著，顯示 `myotherdataset.shipments` 資料表的相關資訊：

```
  bq show myotherdataset.shipments
```

輸出結果大致如下。系統會省略某些資料欄，以便簡化輸出結果。

```
  Last modified             Schema             Total Rows   Total Bytes   Expiration   Time Partitioning   Clustered Fields   Total Logical
 ----------------- --------------------------- ------------ ------------- ------------ ------------------- ------------------ ---------------
  31 Oct 17:34:31   |- l_orderkey: integer      3086653      210767042                                                         210767042
                    |- l_partkey: integer
                    |- l_suppkey: integer
                    |- l_commitdate: date
                    |- l_shipdate: date
                    |- l_receiptdate: date
                    |- l_shipinstruct: string
                    |- l_shipmode: string
```

現在，您可以使用 `CREATE TABLE AS SELECT` 陳述式，將資料選擇性載入美國多區域的 `myotherdataset.orders` 表格：

```
CREATE OR REPLACE TABLE
  myotherdataset.orders
  PARTITION BY DATE_TRUNC(l_commitdate, YEAR) AS
SELECT
  *
FROM
  myawsdataset.orders
WHERE
  EXTRACT(YEAR FROM l_commitdate) = 1992;
```

**注意：** 如果收到 `ResourceExhausted` 錯誤訊息，請稍後再試。如果問題仍未解決，請[聯絡支援團隊](https://docs.cloud.google.com/bigquery/docs/getting-support?hl=zh-tw)。

然後，您可以使用新建立的資料表執行聯結作業：

```
SELECT
  orders.l_orderkey,
  orders.l_orderkey,
  orders.l_suppkey,
  orders.l_commitdate,
  orders.l_returnflag,
  shipments.l_shipmode,
  shipments.l_shipinstruct
FROM
  myotherdataset.shipments
JOIN
  `myotherdataset.orders` as orders
ON
  orders.l_orderkey = shipments.l_orderkey
AND orders.l_partkey = shipments.l_partkey
AND orders.l_suppkey = shipments.l_suppkey
WHERE orders.l_returnflag = 'R'; -- 'R' means refunded.
```

有新資料時，請使用 `INSERT INTO SELECT` 陳述式，將 1993 年的資料附加到目的地資料表：

```
INSERT INTO
   myotherdataset.orders
 SELECT
   *
 FROM
   myawsdataset.orders
 WHERE
   EXTRACT(YEAR FROM l_commitdate) = 1993;
```

#### 範例 2

以下範例會將資料插入擷取時間分區資料表：

```
CREATE TABLE
 mydataset.orders(id String, numeric_id INT64)
PARTITION BY _PARTITIONDATE;
```

建立分區資料表後，您可以將資料插入擷取時間分區資料表：

```
INSERT INTO
 mydataset.orders(
   _PARTITIONTIME,
   id,
   numeric_id)
SELECT
 TIMESTAMP("2023-01-01"),
 id,
 numeric_id,
FROM
 mydataset.ordersof23
WHERE
 numeric_id > 4000000;
```

## materialized view 副本

實體化檢視區塊副本是外部 Amazon Simple Storage Service (Amazon S3)、Apache Iceberg 或 Salesforce Data Cloud 資料的副本，位於 BigQuery 資料集中，因此資料可在 BigQuery 中本機使用。這有助於避免資料輸出費用，並提升查詢效能。BigQuery 可讓您[在啟用 BigLake 中繼資料快取的資料表上建立具體化檢視表](https://docs.cloud.google.com/bigquery/docs/omni-introduction?hl=zh-tw#cache-enabled_tables_with_materialized_views)，並透過 Amazon Simple Storage Service (Amazon S3)、Apache Iceberg 或 Salesforce Data Cloud 資料建立。

實體化檢視區塊副本可讓您在查詢中使用 Amazon S3、Iceberg 或 Data Cloud 實體化檢視區塊資料，同時避免資料輸出成本並提升查詢效能。具體化檢視副本會將 Amazon S3、Iceberg 或 Data Cloud 資料複製到[支援的 BigQuery 區域](#supported_regions)的資料集，讓資料可在 BigQuery 中本機使用。

### 事前準備

- 登入 Google Cloud 帳戶。如果您是 Google Cloud新手，歡迎[建立帳戶](https://console.cloud.google.com/freetrial?hl=zh-tw)，親自評估產品在實際工作環境中的成效。新客戶還能獲得價值 $300 美元的免費抵免額，可用於執行、測試及部署工作負載。
- In the Google Cloud console, on the project selector page,
  select or create a Google Cloud project.

  **Roles required to select or create a project**

  * **Select a project**: Selecting a project doesn't require a specific
    IAM role—you can select any project that you've been
    granted a role on.
  * **Create a project**: To create a project, you need the Project Creator role
    (`roles/resourcemanager.projectCreator`), which contains the
    `resourcemanager.projects.create` permission. [Learn how to grant
    roles](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw).
  **Note**: If you don't plan to keep the
  resources that you create in this procedure, create a project instead of
  selecting an existing project. After you finish these steps, you can
  delete the project, removing all resources associated with the project.

  [Go to project selector](https://console.cloud.google.com/projectselector2/home/dashboard?hl=zh-tw)
- [Verify that billing is enabled for your Google Cloud project](https://docs.cloud.google.com/billing/docs/how-to/verify-billing-enabled?hl=zh-tw#confirm_billing_is_enabled_on_a_project).

- In the Google Cloud console, on the project selector page,
  select or create a Google Cloud project.

  **Roles required to select or create a project**

  * **Select a project**: Selecting a project doesn't require a specific
    IAM role—you can select any project that you've been
    granted a role on.
  * **Create a project**: To create a project, you need the Project Creator role
    (`roles/resourcemanager.projectCreator`), which contains the
    `resourcemanager.projects.create` permission. [Learn how to grant
    roles](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw).
  **Note**: If you don't plan to keep the
  resources that you create in this procedure, create a project instead of
  selecting an existing project. After you finish these steps, you can
  delete the project, removing all resources associated with the project.

  [Go to project selector](https://console.cloud.google.com/projectselector2/home/dashboard?hl=zh-tw)
- [Verify that billing is enabled for your Google Cloud project](https://docs.cloud.google.com/billing/docs/how-to/verify-billing-enabled?hl=zh-tw#confirm_billing_is_enabled_on_a_project).

1. 確認您具備[必要的 Identity and Access Management (IAM) 權限](#required_permissions)，可執行本節中的工作。

#### 必要的角色

如要取得執行本節工作所需的權限，請要求管理員授予您「[BigQuery 管理員](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.admin) 」(`roles/bigquery.admin`) IAM 角色。如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

這個預先定義的角色具備執行本節工作所需的權限。如要查看確切的必要權限，請展開「Required permissions」(必要權限) 部分：

#### 所需權限

如要執行本節中的工作，必須具備下列權限：

* `bigquery.tables.create`
* `bigquery.tables.get`
* `bigquery.tables.getData`
* `bigquery.tables.replicateData`
* `bigquery.jobs.create`

您或許還可透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)取得這些權限。

如要進一步瞭解 BigQuery IAM，請參閱「[BigQuery IAM 角色和權限](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)」。

### 準備 materialized view 副本的資料集

建立具體化檢視區塊副本前，請先完成下列工作：

1. 在[支援 Amazon S3 的區域](https://docs.cloud.google.com/bigquery/docs/omni-introduction?hl=zh-tw#locations)[建立資料集](https://docs.cloud.google.com/bigquery/docs/datasets?hl=zh-tw)
2. 在您於上一個步驟中建立的資料集中，建立來源資料表。來源表格可以是下列任一表格類型：
   * [Amazon S3 BigLake 資料表](https://docs.cloud.google.com/bigquery/docs/omni-aws-create-external-table?hl=zh-tw)，已啟用[中繼資料快取](https://docs.cloud.google.com/bigquery/docs/metadata-caching?hl=zh-tw)，且未使用 Iceberg 檔案格式。
   * [Apache Iceberg 外部資料表](https://docs.cloud.google.com/bigquery/docs/iceberg-external-tables?hl=zh-tw)。
   * [Data Cloud 資料表](https://docs.cloud.google.com/bigquery/docs/salesforce-quickstart?hl=zh-tw)。

### 建立 materialized view 副本

選取下列選項之一：

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。

   如果沒有看到左側窗格，請按一下 last\_page「Expand left pane」(展開左側窗格)，開啟窗格。
3. 在「Explorer」窗格中，前往要建立具體化檢視副本的專案和資料集，然後依序點選 more\_vert「動作」>「建立資料表」。
4. 在「Create table」(建立資料表) 對話方塊的「Source」(來源) 區段中，執行下列操作：

   1. 在「Create table from」(使用下列資料建立資料表) 部分，選取「Existing table/view」(現有資料表/檢視區塊)。
   2. 在「Project」(專案) 部分，輸入來源資料表或檢視區塊所在的專案。
   3. 在「Dataset」(資料集) 部分，輸入來源資料表或檢視表所在的資料集。
   4. 在「View」(檢視畫面) 中，輸入要複製的來源資料表或檢視畫面。如果選擇檢視表，則必須是[授權檢視表](https://docs.cloud.google.com/bigquery/docs/authorized-views?hl=zh-tw)；否則，用於產生該檢視表的所有資料表都必須位於檢視表的資料集中。
5. 選用：在「本機 materialized view 過時程度上限」中，輸入本機 materialized view 的 [`max_staleness` 值](https://docs.cloud.google.com/bigquery/docs/materialized-views-create?hl=zh-tw#max_staleness)。
6. 在「Create table」(建立資料表) 對話方塊的「Destination」(目的地) 區段中，執行下列操作：

   1. 在「Project」(專案) 部分，輸入要建立 materialized view 副本的專案。
   2. 在 **Dataset** (資料集) 部分，輸入要建立具體化檢視表副本的資料集。
   3. 在「**副本 materialized view 名稱**」部分，輸入副本的名稱。
7. 選用：為具體化檢視副本指定**標記**和**進階選項**。如果沒有為「本機具體化檢視資料集」指定資料集，系統會在與來源資料相同的專案和區域中，自動建立名為 `bq_auto_generated_local_mv_dataset` 的資料集。如未指定**本機具體化檢視表名稱**，系統會自動在與來源資料相同的專案和區域中建立名稱，並加上 `bq_auto_generated_local_mv_` 前置字串。
8. 點選「建立資料表」。

系統會建立新的本機具體化檢視區塊 (如果未指定)，並在來源資料集中授權。然後在目的地資料集中建立 materialized view 副本。

### SQL

1. 在您建立的資料集中，對基礎資料表[建立具體化檢視](https://docs.cloud.google.com/bigquery/docs/materialized-views-create?hl=zh-tw)。您也可以在 Amazon S3 區域中的不同資料集中建立具體化檢視區塊。
2. [授權具體化檢視表](https://docs.cloud.google.com/bigquery/docs/authorized-views?hl=zh-tw)存取資料集，這些資料集包含用於建立具體化檢視表的查詢中的來源資料表。
3. 如果已為來源資料表設定手動重新整理中繼資料快取，請執行 [`BQ.REFRESH_EXTERNAL_METADATA_CACHE` 系統程序](https://docs.cloud.google.com/bigquery/docs/reference/system-procedures?hl=zh-tw#bqrefresh_external_metadata_cache)，重新整理中繼資料快取。
4. 執行 [`BQ.REFRESH_MATERIALIZED_VIEW` 系統程序](https://docs.cloud.google.com/bigquery/docs/reference/system-procedures?hl=zh-tw#bqrefresh_materialized_view)，重新整理 materialized view。
5. 使用 [`CREATE MATERIALIZED VIEW AS REPLICA OF` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#create_materialized_view_as_replica_of_statement)建立 materialized view 副本：

   ```
   CREATE MATERIALIZED VIEW PROJECT_ID.BQ_DATASET.REPLICA_NAME
   OPTIONS(replication_interval_seconds=REPLICATION_INTERVAL)
   AS REPLICA OF PROJECT_ID.S3_DATASET.MATERIALIZED_VIEW_NAME;
   ```

   請替換下列項目：

   * `PROJECT_ID`：要在其中建立 materialized view 副本的專案名稱，例如 `myproject`。
   * `BQ_DATASET`：您要在其中建立具體化檢視表副本的 BigQuery 資料集名稱，例如 `bq_dataset`。資料集必須位於 BigQuery [區域](https://docs.cloud.google.com/bigquery/docs/omni-introduction?hl=zh-tw#locations)，且該區域會對應至來源具體化檢視區的區域。
   * `REPLICA_NAME`：要建立的具體化檢視副本名稱，例如 `my_mv_replica`。
   * `REPLICATION_INTERVAL`：指定將來源 materialized view 資料複製到備用資源的頻率 (以秒為單位)。值必須介於 60 至 3,600 之間，預設值為 300 (5 分鐘)。
   * `S3_DATASET`：包含來源具體化檢視的資料集名稱，例如 `s3_dataset`。
   * `MATERIALIZED_VIEW_NAME`：要複製的 materialized view 名稱，例如 `my_mv`。

   下列範例會在 `bq_dataset` 中建立名為 `mv_replica` 的具體化檢視表副本：

   ```
   CREATE MATERIALIZED VIEW `myproject.bq_dataset.mv_replica`
   OPTIONS(
   replication_interval_seconds=600
   )
   AS REPLICA OF `myproject.s3_dataset.my_s3_mv`
   ```

建立 materialized view 副本後，複製程序會輪詢來源 materialized view 的變更，並將資料複製到 materialized view 副本，按照您在 `replication_interval_seconds` 或 `max_staleness` 選項中指定的間隔時間重新整理資料。如果在第一個補充作業完成前查詢副本，會收到 `backfill in progress` 錯誤。第一次複製完成後，您就可以查詢具體化檢視表副本中的資料。

### 資料更新間隔

建立 materialized view 副本後，複製程序會輪詢來源 materialized view 的變更，並將資料複製到 materialized view 副本。資料會按照您在 [`CREATE MATERIALIZED VIEW AS REPLICA OF` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#create_materialized_view_as_replica_of_statement)的 `replication_interval_seconds` 選項中指定的間隔複製。

除了複製間隔外，來源具體化檢視的重新整理頻率，以及具體化檢視使用的 Amazon S3、Iceberg 或 Data Cloud 資料表的中繼資料快取重新整理頻率，也會影響具體化檢視副本資料的新鮮度。

您可以使用 Google Cloud 控制台，檢查 materialized view 副本和所依據資源的資料更新間隔：

* 如要查看具體化檢視表副本的新鮮度，請查看具體化檢視表副本「詳細資料」窗格中的「上次修改時間」欄位。
* 如要查看具體化檢視區塊的來源時效，請查看具體化檢視區塊「詳細資料」窗格中的「上次修改時間」欄位。
* 如要查看來源 Amazon S3、Iceberg 或 Data Cloud 資料表的中繼資料快取更新間隔，請查看具體化檢視表「詳細資料」窗格中的「最大陳舊度」欄位。

### 支援的 materialized view 副本區域

建立具體化檢視副本時，請使用下表中的位置對應：

| **來源 materialized view 的位置** | **materialized view 副本的位置** |
| --- | --- |
| `aws-us-east-1` | `US` [多區域](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw#multi-regions)、 或下列任一[區域](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw#regions)：  * `northamerica-northeast1` * `northamerica-northeast2` * `us-central1` * `us-east1` * `us-east4` * `us-east5` * `us-south1` * `us-west1` * `us-west2` * `us-west3` * `us-west4` |
| `aws-us-west-2` | `US` [多區域](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw#multi-regions)、 或下列任一[區域](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw#regions)：  * `northamerica-northeast1` * `northamerica-northeast2` * `us-central1` * `us-east1` * `us-east4` * `us-east5` * `us-south1` * `us-west1` * `us-west2` * `us-west3` * `us-west4` |
| `aws-eu-west-1` | `EU` [多區域](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw#multi-regions)、 或下列任一[區域](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw#regions)：  * `europe-central2` * `europe-north1` * `europe-southwest1` * `europe-west1` * `europe-west2` * `europe-west3` * `europe-west4` * `europe-west6` * `europe-west8` * `europe-west9` * `europe-west10` |
| `aws-ap-northeast-2` | 下列任一[區域](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw#regions)：  * `asia-east1` * `asia-east2` * `asia-northeast1` * `asia-northeast2` * `asia-northeast3` * `asia-south1` * `asia-south2` * `asia-southeast1` |
| `aws-ap-southeast-2` | 下列任一[區域](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw#regions)：  * `australia-southeast1` * `australia-southeast2` |

### materialized view 副本的限制

* 如果 materialized view 是以使用[資料列層級安全防護機制](https://docs.cloud.google.com/bigquery/docs/row-level-security-intro?hl=zh-tw)或[資料欄層級安全防護機制](https://docs.cloud.google.com/bigquery/docs/column-level-security-intro?hl=zh-tw)的資料表為基礎，就無法建立 materialized view 副本。
* 您無法將[客戶自行管理的加密金鑰 (CMEK)](https://docs.cloud.google.com/bigquery/docs/customer-managed-encryption?hl=zh-tw) 用於來源具體化檢視或具體化檢視副本。
* 您只能為以使用[中繼資料快取](https://docs.cloud.google.com/bigquery/docs/metadata-caching?hl=zh-tw)的任何資料表為依據的具體化檢視表，建立具體化檢視表副本。
* 您只能為特定來源具體化檢視建立一個副本。
* 您只能為[授權的具體化檢視表](https://docs.cloud.google.com/bigquery/docs/authorized-views?hl=zh-tw)建立副本。

### 具體化檢視表副本定價

使用具體化檢視表副本會產生運算、傳出資料移轉和儲存空間費用。

## 後續步驟

* 瞭解 [BigQuery ML](https://docs.cloud.google.com/bigquery/docs/bqml-introduction?hl=zh-tw)。
* 瞭解 [BigQuery Omni](https://docs.cloud.google.com/bigquery/docs/omni-introduction?hl=zh-tw)。
* 瞭解如何[執行查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw)。
* 瞭解如何[為 BigQuery Omni 設定 VPC Service Controls](https://docs.cloud.google.com/bigquery/docs/omni-vpc-sc?hl=zh-tw)。
* 瞭解如何排定及管理從 [Amazon S3 到 BigQuery](https://docs.cloud.google.com/bigquery/docs/s3-transfer-intro?hl=zh-tw)，以及從 [Blob Storage 到 BigQuery](https://docs.cloud.google.com/bigquery/docs/blob-storage-transfer-intro?hl=zh-tw) 的週期性載入工作。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-08 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-08 (世界標準時間)。"],[],[]]