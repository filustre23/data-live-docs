Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [參考資料](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 「TABLES」檢視畫面

`INFORMATION_SCHEMA.TABLES` 檢視表會針對資料集中的每個資料表或檢視表，分別列出一個相對應的資料列。`TABLES` 和 `TABLE_OPTIONS` 檢視表也包含檢視表的高階資訊。如需詳細資訊，請查詢 [`INFORMATION_SCHEMA.VIEWS`](https://docs.cloud.google.com/bigquery/docs/information-schema-views?hl=zh-tw) 檢視區塊。

## 所需權限

如要查詢 `INFORMATION_SCHEMA.TABLES` 檢視畫面，您必須具備下列 Identity and Access Management (IAM) 權限：

* `bigquery.tables.get`
* `bigquery.tables.list`
* `bigquery.routines.get`
* `bigquery.routines.list`

下列每個預先定義的 IAM 角色都包含上述權限：

* `roles/bigquery.admin`
* `roles/bigquery.dataViewer`
* `roles/bigquery.metadataViewer`

如要進一步瞭解 BigQuery 權限，請參閱「[使用 IAM 控管存取權](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)」。

## 結構定義

查詢 `INFORMATION_SCHEMA.TABLES` 檢視表時，查詢結果會為資料集中的每個資料表或檢視表包含一個資料列。如要取得檢視區塊的詳細資訊，請改為查詢 [`INFORMATION_SCHEMA.VIEWS` 檢視區塊](https://docs.cloud.google.com/bigquery/docs/information-schema-views?hl=zh-tw)。

`INFORMATION_SCHEMA.TABLES` 檢視表具有下列結構定義：

| 資料欄名稱 | 資料類型 | 值 |
| --- | --- | --- |
| `table_catalog` | `STRING` | 資料集所屬專案的專案 ID。 |
| `table_schema` | `STRING` | 資料表或檢視表所屬資料集的名稱。也稱為「`datasetId`」。 |
| `table_name` | `STRING` | 資料表或檢視表的名稱。也稱為「`tableId`」。 |
| `table_type` | `STRING` | 資料表類型，可能是下列其中一個值：   * `BASE TABLE`：標準[資料表](https://docs.cloud.google.com/bigquery/docs/tables-intro?hl=zh-tw) * `CLONE`：[資料表副本](https://docs.cloud.google.com/bigquery/docs/table-clones-intro?hl=zh-tw) * `SNAPSHOT`：[資料表快照](https://docs.cloud.google.com/bigquery/docs/table-snapshots-intro?hl=zh-tw) * `VIEW`：A   [檢視表](https://docs.cloud.google.com/bigquery/docs/views-intro?hl=zh-tw) * `MATERIALIZED VIEW`：[具體化檢視表](https://docs.cloud.google.com/bigquery/docs/materialized-views-intro?hl=zh-tw)或[具體化檢視表副本](https://docs.cloud.google.com/bigquery/docs/load-data-using-cross-cloud-transfer?hl=zh-tw#materialized_view_replicas) * `EXTERNAL`：參照[外部資料來源](https://docs.cloud.google.com/bigquery/external-data-sources?hl=zh-tw)的資料表 |
| `managed_table_type` | `STRING` | 這一欄目前為預先發布版。受管理資料表類型，可以是下列其中一種：   * `NATIVE`：標準[資料表](https://docs.cloud.google.com/bigquery/docs/tables-intro?hl=zh-tw) * `BIGLAKE`：[Apache Iceberg 代管資料表](https://docs.cloud.google.com/bigquery/docs/iceberg-tables?hl=zh-tw) |
| `is_insertable_into` | `STRING` | `YES` 或 `NO`，視資料表是否支援 [DML INSERT](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/dml-syntax?hl=zh-tw#insert_statement) 陳述式而定 |
| `is_fine_grained_mutations_enabled` | `STRING` | `YES` 或 `NO`，視資料表是否啟用[細微 DML 突變](https://docs.cloud.google.com/bigquery/docs/data-manipulation-language?hl=zh-tw#enable_fine-grained_dml)而定 |
| `is_typed` | `STRING` | 此值一律為 `NO` |
| `is_change_history_enabled` | `STRING` | `YES` 或 `NO`，視[變更記錄](https://docs.cloud.google.com/bigquery/docs/change-history?hl=zh-tw)是否已啟用而定 |
| `creation_time` | `TIMESTAMP` | 資料表的建立時間 |
| `base_table_catalog` | `STRING` | 如果是[資料表本機副本](https://docs.cloud.google.com/bigquery/docs/table-clones-intro?hl=zh-tw)和[資料表快照](https://docs.cloud.google.com/bigquery/docs/table-snapshots-intro?hl=zh-tw)，則為基本資料表的專案。僅適用於 `table_type` 設為 `CLONE` 或 `SNAPSHOT` 的資料表。 |
| `base_table_schema` | `STRING` | 如果是[資料表副本](https://docs.cloud.google.com/bigquery/docs/table-clones-intro?hl=zh-tw)和[資料表快照](https://docs.cloud.google.com/bigquery/docs/table-snapshots-intro?hl=zh-tw)，則為基礎資料表的資料集。僅適用於 `table_type` 設為 `CLONE` 或 `SNAPSHOT` 的資料表。 |
| `base_table_name` | `STRING` | 如果是[資料表副本](https://docs.cloud.google.com/bigquery/docs/table-clones-intro?hl=zh-tw)和[資料表快照](https://docs.cloud.google.com/bigquery/docs/table-snapshots-intro?hl=zh-tw)，則為基礎資料表的名稱。僅適用於 `table_type` 設為 `CLONE` 或 `SNAPSHOT` 的資料表。 |
| `snapshot_time_ms` | `TIMESTAMP` | 如果是[資料表本機副本](https://docs.cloud.google.com/bigquery/docs/table-clones-intro?hl=zh-tw)和[資料表快照](https://docs.cloud.google.com/bigquery/docs/table-snapshots-intro?hl=zh-tw)，則為在基本資料表上執行[本機副本](https://docs.cloud.google.com/bigquery/docs/table-clones-create?hl=zh-tw)或[快照](https://docs.cloud.google.com/bigquery/docs/table-snapshots-create?hl=zh-tw)作業，以建立這個資料表的時間。如果使用[時空旅行](https://docs.cloud.google.com/bigquery/docs/time-travel?hl=zh-tw)，這個欄位會包含時空旅行時間戳記。否則，`snapshot_time_ms` 欄位與 `creation_time` 欄位相同。僅適用於 `table_type` 設為 `CLONE` 或 `SNAPSHOT` 的資料表。 |
| `replica_source_catalog` | `STRING` | 如果是 [materialized view 副本](https://docs.cloud.google.com/bigquery/docs/load-data-using-cross-cloud-transfer?hl=zh-tw#materialized_view_replicas)，則為基礎 materialized view 的專案。 |
| `replica_source_schema` | `STRING` | 如果是[具體化檢視表副本](https://docs.cloud.google.com/bigquery/docs/load-data-using-cross-cloud-transfer?hl=zh-tw#materialized_view_replicas)，則為基礎具體化檢視表的資料集。 |
| `replica_source_name` | `STRING` | 如果是[具體化檢視表副本](https://docs.cloud.google.com/bigquery/docs/load-data-using-cross-cloud-transfer?hl=zh-tw#materialized_view_replicas)，則為基礎具體化檢視表的名稱。 |
| `replication_status` | `STRING` | 如果是[具體化檢視表副本](https://docs.cloud.google.com/bigquery/docs/load-data-using-cross-cloud-transfer?hl=zh-tw#materialized_view_replicas)，則為從基礎具體化檢視表複製到具體化檢視表副本的狀態，可能為下列其中一種：   * `REPLICATION_STATUS_UNSPECIFIED` * `ACTIVE`：複製作業正在進行，沒有發生任何錯誤 * `SOURCE_DELETED`：來源具體化檢視表已刪除 * `PERMISSION_DENIED`：來源具體化檢視表尚未在資料集上[獲得授權](https://docs.cloud.google.com/bigquery/docs/authorized-views?hl=zh-tw)，而該資料集包含來源 Amazon S3 BigLake 資料表，這些資料表用於建立具體化檢視表的查詢。 * `UNSUPPORTED_CONFIGURATION`：副本的[必要條件](https://docs.cloud.google.com/bigquery/docs/load-data-using-cross-cloud-transfer?hl=zh-tw#create)有問題，但來源 materialized view 授權除外。 |
| `replication_error` | `STRING` | 如果 `replication_status` 表示[具體化檢視區塊副本](https://docs.cloud.google.com/bigquery/docs/load-data-using-cross-cloud-transfer?hl=zh-tw#materialized_view_replicas)有複寫問題，`replication_error` 會提供問題的詳細資料。 |
| `ddl` | `STRING` | 可用於重新建立資料表的 [DDL 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw)，例如 `CREATE TABLE` 或 `CREATE VIEW` |
| `default_collation_name` | `STRING` | 預設[排序規格](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/collation-concepts?hl=zh-tw)的名稱 (如有)，否則為 `NULL`。 |
| `sync_status` | `JSON` | [跨區域複製](https://docs.cloud.google.com/bigquery/docs/data-replication?hl=zh-tw)和[災難復原](https://docs.cloud.google.com/bigquery/docs/managed-disaster-recovery?hl=zh-tw)資料集的主要和次要副本之間的同步狀態。如果副本是主要副本，或資料集未使用複製功能，則傳回 `NULL`。 |
| `upsert_stream_apply_watermark` | `TIMESTAMP` | 如果資料表使用變更資料擷取 (CDC)，則為上次套用資料列修改的時間。詳情請參閱「[監控資料表 upsert 作業進度](https://docs.cloud.google.com/bigquery/docs/change-data-capture?hl=zh-tw#monitor_table_upsert_operation_progress)」。 |

為確保穩定性，建議您在資訊結構定義查詢中明確列出資料欄，而非使用萬用字元 (`SELECT *`)。明確列出資料欄可避免基礎結構定義變更時，查詢中斷。

## 範圍和語法

對這個檢視表執行的查詢必須包含資料集或區域限定詞。如果是含有資料集限定符的查詢，您必須具備該資料集的權限。如要查詢含有區域限定符的資料，您必須具備專案權限。
詳情請參閱「[語法](https://docs.cloud.google.com/bigquery/docs/information-schema-intro?hl=zh-tw#syntax)」。下表說明這個檢視畫面的區域和資源範圍：

| 檢視表名稱 | 資源範圍 | 區域範圍 |
| --- | --- | --- |
| `` [PROJECT_ID.]`region-REGION`.INFORMATION_SCHEMA.TABLES `` | 專案層級 | `REGION` |
| `[PROJECT_ID.]DATASET_ID.INFORMATION_SCHEMA.TABLES` | 資料集層級 | 資料集位置 |

取代下列項目：

* 選用：`PROJECT_ID`：專案 ID。 Google Cloud 如未指定，系統會使用預設專案。
* `REGION`：任何[資料集區域名稱](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)。
  例如：`` `region-us` ``。
* `DATASET_ID`：資料集的 ID。詳情請參閱「[資料集限定符](https://docs.cloud.google.com/bigquery/docs/information-schema-intro?hl=zh-tw#dataset_qualifier)」。**注意：**您必須使用[區域限定詞](https://docs.cloud.google.com/bigquery/docs/information-schema-intro?hl=zh-tw#region_qualifier)查詢 `INFORMATION_SCHEMA` 檢視畫面。查詢執行位置必須與 `INFORMATION_SCHEMA` 檢視區塊的區域相符。

**範例**

```
-- Returns metadata for tables in a single dataset.
SELECT * FROM myDataset.INFORMATION_SCHEMA.TABLES;
```

## 範例

##### 範例 1：

以下範例會擷取名為 `mydataset` 的資料集中所有資料表的資料表中繼資料。系統傳回的是預設專案中 `mydataset` 內所有類型的資料表中繼資料。

`mydataset` 包含下列資料表：

* `mytable1`：標準的 BigQuery 資料表
* `myview1`：BigQuery 檢視表

如要對預設專案以外的專案執行查詢，請使用以下格式將專案 ID 新增至資料集：`` `project_id`.dataset.INFORMATION_SCHEMA.view ``；例如 `` `myproject`.mydataset.INFORMATION_SCHEMA.TABLES ``。

**注意：** `INFORMATION_SCHEMA` 檢視表名稱會區分大小寫。

```
SELECT
  table_catalog, table_schema, table_name, table_type,
  is_insertable_into, creation_time, ddl
FROM
  mydataset.INFORMATION_SCHEMA.TABLES;
```

結果大致如下。為了方便閱讀，部分資料欄已從結果中排除。

```
+----------------+---------------+----------------+------------+--------------------+---------------------+---------------------------------------------+
| table_catalog  | table_schema  |   table_name   | table_type | is_insertable_into |    creation_time    |                     ddl                     |
+----------------+---------------+----------------+------------+--------------------+---------------------+---------------------------------------------+
| myproject      | mydataset     | mytable1       | BASE TABLE | YES                | 2018-10-29 20:34:44 | CREATE TABLE `myproject.mydataset.mytable1` |
|                |               |                |            |                    |                     | (                                           |
|                |               |                |            |                    |                     |   id INT64                                  |
|                |               |                |            |                    |                     | );                                          |
| myproject      | mydataset     | myview1        | VIEW       | NO                 | 2018-12-29 00:19:20 | CREATE VIEW `myproject.mydataset.myview1`   |
|                |               |                |            |                    |                     | AS SELECT 100 as id;                        |
+----------------+---------------+----------------+------------+--------------------+---------------------+---------------------------------------------+
```

##### 範例 2：

以下範例會從 `INFORMATION_SCHEMA.TABLES` 檢視表，擷取 `CLONE` 或 `SNAPSHOT` 類型所有資料表的資料表中繼資料。系統傳回的是預設專案中 `mydataset` 內的資料表中繼資料。

如要對預設專案以外的專案執行查詢，請使用以下格式將專案 ID 新增至資料集：`` `project_id`.dataset.INFORMATION_SCHEMA.view ``；例如 `` `myproject`.mydataset.INFORMATION_SCHEMA.TABLES ``。

```
  SELECT
    table_name, table_type, base_table_catalog,
    base_table_schema, base_table_name, snapshot_time_ms
  FROM
    mydataset.INFORMATION_SCHEMA.TABLES
  WHERE
    table_type = 'CLONE'
  OR
    table_type = 'SNAPSHOT';
```

結果大致如下。為了方便閱讀，部分資料欄已從結果中排除。

```
  +--------------+------------+--------------------+-------------------+-----------------+---------------------+
  | table_name   | table_type | base_table_catalog | base_table_schema | base_table_name | snapshot_time_ms    |
  +--------------+------------+--------------------+-------------------+-----------------+---------------------+
  | items_clone  | CLONE      | myproject          | mydataset         | items           | 2018-10-31 22:40:05 |
  | orders_bk    | SNAPSHOT   | myproject          | mydataset         | orders          | 2018-11-01 08:22:39 |
  +--------------+------------+--------------------+-------------------+-----------------+---------------------+
```

##### 範例 3：

以下範例會從 [`census_bureau_usa`](https://console.cloud.google.com/bigquery?p=bigquery-public-data&%3Bd=census_bureau_usa&%3Bpage=dataset&hl=zh-tw) 資料集中的 `population_by_zip_2010` 資料表，擷取 `INFORMATION_SCHEMA.TABLES` 檢視表的 `table_name` 和 `ddl` 資料欄。這個資料集是 BigQuery [公開資料集方案](https://docs.cloud.google.com/bigquery/public-data?hl=zh-tw)的一部分。

由於您要查詢的資料表位於另一個專案中，因此您應使用下列格式將專案 ID 新增至資料集：`` `project_id`.dataset.INFORMATION_SCHEMA.view ``。在本範例中，這個值為 `` `bigquery-public-data`.census_bureau_usa.INFORMATION_SCHEMA.TABLES ``。

```
SELECT
  table_name, ddl
FROM
  `bigquery-public-data`.census_bureau_usa.INFORMATION_SCHEMA.TABLES
WHERE
  table_name = 'population_by_zip_2010';
```

結果大致如下：

```
+------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
|       table_name       |                                                                                                            ddl                                                                                                             |
+------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| population_by_zip_2010 | CREATE TABLE `bigquery-public-data.census_bureau_usa.population_by_zip_2010`                                                                                                                                               |
|                        | (                                                                                                                                                                                                                          |
|                        |   geo_id STRING OPTIONS(description="Geo code"),                                                                                                                                                                           |
|                        |   zipcode STRING NOT NULL OPTIONS(description="Five digit ZIP Code Tabulation Area Census Code"),                                                                                                                          |
|                        |   population INT64 OPTIONS(description="The total count of the population for this segment."),                                                                                                                             |
|                        |   minimum_age INT64 OPTIONS(description="The minimum age in the age range. If null, this indicates the row as a total for male, female, or overall population."),                                                          |
|                        |   maximum_age INT64 OPTIONS(description="The maximum age in the age range. If null, this indicates the row as having no maximum (such as 85 and over) or the row is a total of the male, female, or overall population."), |
|                        |   gender STRING OPTIONS(description="male or female. If empty, the row is a total population summary.")                                                                                                                    |
|                        | )                                                                                                                                                                                                                          |
|                        | OPTIONS(                                                                                                                                                                                                                   |
|                        |   labels=[("freebqcovid", "")]                                                                                                                                                                                             |
|                        | );                                                                                                                                                                                                                         |
+------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
```




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-09 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-09 (世界標準時間)。"],[],[]]