Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 建立具體化檢視表

**注意：** 使用以特定 BigQuery 版本建立的預留項目時，這項功能可能無法使用。如要進一步瞭解各版本啟用的功能，請參閱「[BigQuery 版本簡介](https://docs.cloud.google.com/bigquery/docs/editions-intro?hl=zh-tw)」。

本文說明如何在 BigQuery 中建立具體化檢視表。閱讀本文前，請先熟悉[具體化檢視區塊簡介](https://docs.cloud.google.com/bigquery/docs/materialized-views-intro?hl=zh-tw)。

## 事前準備

授予身分與存取權管理 (IAM) 角色，讓使用者取得執行本文各項工作所需的權限。

### 所需權限

如要建立具體化檢視區塊，您需要 `bigquery.tables.create` IAM 權限。

下列每個預先定義的 IAM 角色都包含建立 materialized view 所需的權限：

* `bigquery.dataEditor`
* `bigquery.dataOwner`
* `bigquery.admin`

如要進一步瞭解 BigQuery Identity and Access Management (IAM)，請參閱「[使用 IAM 控管存取權](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)」。

## 建立具體化檢視表

如要建立具體化檢視區塊，請選取下列任一選項：

### SQL

使用 [`CREATE MATERIALIZED VIEW` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#create_materialized_view_statement)。下列範例會為每個產品 ID 的點擊次數建立具體化檢視表：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列陳述式：

   ```
   CREATE MATERIALIZED VIEW PROJECT_ID.DATASET.MATERIALIZED_VIEW_NAME AS (
     QUERY_EXPRESSION
   );
   ```

   請替換下列項目：

   * `PROJECT_ID`：要在其中建立具體化檢視的專案名稱，例如 `myproject`。
   * `DATASET`：您要在其中建立具體化檢視的 BigQuery 資料集名稱，例如 `mydataset`。如果您要透過 Amazon Simple Storage Service (Amazon S3) BigLake 資料表 ([預先發布版](https://cloud.google.com/products?hl=zh-tw#product-launch-stages)) 建立具體化檢視表，請確保資料集位於[支援的區域](https://docs.cloud.google.com/bigquery/docs/omni-introduction?hl=zh-tw#locations)。
   * `MATERIALIZED_VIEW_NAME`：要建立的具體化檢視表名稱，例如 `my_mv`。
   * `QUERY_EXPRESSION`：定義具體化檢視表的 GoogleSQL 查詢運算式，例如 `SELECT product_id, SUM(clicks) AS sum_clicks FROM
     mydataset.my_source_table`。
3. 按一下「執行」play\_circle。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

**範例**

下列範例會為每個產品 ID 的點擊次數建立具體化檢視表：

```
CREATE MATERIALIZED VIEW myproject.mydataset.my_mv_table AS (
  SELECT
    product_id,
    SUM(clicks) AS sum_clicks
  FROM
    myproject.mydataset.my_base_table
  GROUP BY
    product_id
);
```

### Terraform

請使用 [`google_bigquery_table`](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/bigquery_table) 資源。

**注意：** 如要使用 Terraform 建立 BigQuery 物件，必須啟用 [Cloud Resource Manager API](https://docs.cloud.google.com/resource-manager/reference/rest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

下列範例會建立名為 `my_materialized_view` 的檢視區塊：

```
resource "google_bigquery_dataset" "default" {
  dataset_id                      = "mydataset"
  default_partition_expiration_ms = 2592000000  # 30 days
  default_table_expiration_ms     = 31536000000 # 365 days
  description                     = "dataset description"
  location                        = "US"
  max_time_travel_hours           = 96 # 4 days

  labels = {
    billing_group = "accounting",
    pii           = "sensitive"
  }
}

resource "google_bigquery_table" "default" {
  dataset_id = google_bigquery_dataset.default.dataset_id
  table_id   = "my_materialized_view"

  materialized_view {
    query                            = "SELECT ID, description, date_created FROM `myproject.orders.items`"
    enable_refresh                   = "true"
    refresh_interval_ms              = 172800000 # 2 days
    allow_non_incremental_definition = "false"
  }

}
```

如要在 Google Cloud 專案中套用 Terraform 設定，請完成下列各節的步驟。

## 準備 Cloud Shell

1. 啟動 [Cloud Shell](https://shell.cloud.google.com/?hl=zh-tw)。
2. 設定要套用 Terraform 設定的預設 Google Cloud 專案。

   您只需要為每項專案執行一次這個指令，且可以在任何目錄中執行。

   ```
   export GOOGLE_CLOUD_PROJECT=PROJECT_ID
   ```

   如果您在 Terraform 設定檔中設定明確值，環境變數就會遭到覆寫。

## 準備目錄

每個 Terraform 設定檔都必須有自己的目錄 (也稱為*根模組*)。

1. 在 [Cloud Shell](https://shell.cloud.google.com/?hl=zh-tw) 中建立目錄，並在該目錄中建立新檔案。檔案名稱的副檔名必須是 `.tf`，例如 `main.tf`。在本教學課程中，這個檔案稱為 `main.tf`。

   ```
   mkdir DIRECTORY && cd DIRECTORY && touch main.tf
   ```
2. 如果您正在學習教學課程，可以複製每個章節或步驟中的程式碼範例。

   將程式碼範例複製到新建立的 `main.tf`。

   視需要從 GitHub 複製程式碼。如果 Terraform 代码片段是端對端解決方案的一部分，建議您使用這個方法。
3. 查看並修改範例參數，套用至您的環境。
4. 儲存變更。
5. 初始化 Terraform。每個目錄只需執行一次這項操作。

   ```
   terraform init
   ```

   如要使用最新版 Google 供應商，請加入 `-upgrade` 選項：

   ```
   terraform init -upgrade
   ```

## 套用變更

1. 查看設定，確認 Terraform 即將建立或更新的資源符合您的預期：

   ```
   terraform plan
   ```

   視需要修正設定。
2. 執行下列指令，並在提示中輸入 `yes`，套用 Terraform 設定：

   ```
   terraform apply
   ```

   等待 Terraform 顯示「Apply complete!」訊息。
3. [開啟 Google Cloud 專案](https://console.cloud.google.com/?hl=zh-tw)即可查看結果。在 Google Cloud 控制台中，前往 UI 中的資源，確認 Terraform 已建立或更新這些資源。

**注意：**Terraform 範例通常會假設 Google Cloud 專案已啟用必要的 API。

### API

呼叫 [`tables.insert` 方法](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables/insert?hl=zh-tw)，然後傳入已定義 `materializedView` 欄位的 [`Table` 資源](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables?hl=zh-tw#Table)：

```
{
  "kind": "bigquery#table",
  "tableReference": {
    "projectId": "PROJECT_ID",
    "datasetId": "DATASET",
    "tableId": "MATERIALIZED_VIEW_NAME"
  },
  "materializedView": {
    "query": "QUERY_EXPRESSION"
  }
}
```

請替換下列項目：

* `PROJECT_ID`：要在其中建立具體化檢視的專案名稱，例如 `myproject`。
* `DATASET`：您要在其中建立具體化檢視的 BigQuery 資料集名稱，例如 `mydataset`。如果您要透過 Amazon Simple Storage Service (Amazon S3) BigLake 資料表 ([預先發布版](https://cloud.google.com/products?hl=zh-tw#product-launch-stages)) 建立具體化檢視表，請確保資料集位於[支援的區域](https://docs.cloud.google.com/bigquery/docs/omni-introduction?hl=zh-tw#locations)。
* `MATERIALIZED_VIEW_NAME`：要建立的具體化檢視表名稱，例如 `my_mv`。
* `QUERY_EXPRESSION`：定義具體化檢視表的 GoogleSQL 查詢運算式，例如 `SELECT product_id, SUM(clicks) AS sum_clicks FROM
  mydataset.my_source_table`。

**範例**

下列範例會為每個產品 ID 的點擊次數建立具體化檢視表：

```
{
  "kind": "bigquery#table",
  "tableReference": {
    "projectId": "myproject",
    "datasetId": "mydataset",
    "tableId": "my_mv"
  },
  "materializedView": {
    "query": "select product_id,sum(clicks) as
                sum_clicks from myproject.mydataset.my_source_table
                group by 1"
  }
}
```

### Java

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Java 設定說明操作。詳情請參閱 [BigQuery Java API 參考說明文件](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/overview?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import com.google.cloud.bigquery.BigQuery;
import com.google.cloud.bigquery.BigQueryException;
import com.google.cloud.bigquery.BigQueryOptions;
import com.google.cloud.bigquery.MaterializedViewDefinition;
import com.google.cloud.bigquery.TableId;
import com.google.cloud.bigquery.TableInfo;

// Sample to create materialized view
public class CreateMaterializedView {

  public static void main(String[] args) {
    // TODO(developer): Replace these variables before running the sample.
    String datasetName = "MY_DATASET_NAME";
    String tableName = "MY_TABLE_NAME";
    String materializedViewName = "MY_MATERIALIZED_VIEW_NAME";
    String query =
        String.format(
            "SELECT MAX(TimestampField) AS TimestampField, StringField, "
                + "MAX(BooleanField) AS BooleanField "
                + "FROM %s.%s GROUP BY StringField",
            datasetName, tableName);
    createMaterializedView(datasetName, materializedViewName, query);
  }

  public static void createMaterializedView(
      String datasetName, String materializedViewName, String query) {
    try {
      // Initialize client that will be used to send requests. This client only needs to be created
      // once, and can be reused for multiple requests.
      BigQuery bigquery = BigQueryOptions.getDefaultInstance().getService();

      TableId tableId = TableId.of(datasetName, materializedViewName);

      MaterializedViewDefinition materializedViewDefinition =
          MaterializedViewDefinition.newBuilder(query).build();

      bigquery.create(TableInfo.of(tableId, materializedViewDefinition));
      System.out.println("Materialized view created successfully");
    } catch (BigQueryException e) {
      System.out.println("Materialized view was not created. \n" + e.toString());
    }
  }
}
```

成功建立具體化檢視區塊後，該檢視區塊會顯示在 Google Cloud 控制台的 BigQuery「探索工具」窗格中。以下範例顯示具體化檢視區塊結構定義：

除非停用[自動重新整理](https://docs.cloud.google.com/bigquery/docs/materialized-views-manage?hl=zh-tw#automatic-refresh)，否則 BigQuery 會對具體化檢視區塊啟動非同步完整重新整理。查詢很快就會完成，但初始重新整理作業可能會繼續執行。

**注意：** 每個基本資料表在同一個專案中最多只能有 100 個具體化檢視區塊，在同一個機構中則最多只能有 500 個具體化檢視區塊。

## 存取控管

您可以在[資料集層級](https://docs.cloud.google.com/bigquery/docs/dataset-access-controls?hl=zh-tw)、[檢視層級](https://docs.cloud.google.com/bigquery/docs/authorized-views?hl=zh-tw)或[資料欄層級](https://docs.cloud.google.com/bigquery/docs/column-level-security-intro?hl=zh-tw)授予具體化檢視的存取權。您也可以在 [IAM 資源階層](https://docs.cloud.google.com/iam/docs/resource-hierarchy-access-control?hl=zh-tw)中，於較高層級設定存取權。

查詢具體化檢視表時，必須具備該檢視表及其基本資料表的存取權。如要分享 materialized view，您可以授予基礎資料表的權限，或將 materialized view 設定為授權 view。詳情請參閱「[授權檢視表](https://docs.cloud.google.com/bigquery/docs/authorized-views?hl=zh-tw)」。

### 存取控管限制

* 如果使用者查詢具體化檢視表時，包含因資料欄層級安全性而無法存取的基礎資料表資料欄，查詢就會失敗，並顯示 `Access Denied` 訊息。
* 如果使用者查詢具體化檢視表，但沒有權限完整存取具體化檢視表基礎資料表中的所有資料列，BigQuery 就會對基礎資料表執行查詢，而不是讀取具體化檢視表資料。這可確保查詢遵守所有存取控管限制。查詢含有資料遮蓋欄的資料表時，也適用這項限制。

## 支援查詢具體化檢視表

具體化檢視表使用受限的 SQL 語法。查詢必須採用以下格式：

```
[ WITH cte [, …]]
SELECT  [{ ALL | DISTINCT }]
  expression [ [ AS ] alias ] [, ...]
FROM from_item [, ...]
[ WHERE bool_expression ]
[ GROUP BY expression [, ...] ]

from_item:
    {
      table_name [ as_alias ]
      | { join_operation | ( join_operation ) }
      | field_path
      | unnest_operator
      | cte_name [ as_alias ]
    }

as_alias:
    [ AS ] alias
```

## 查詢限制

遞增式具體化檢視區有下列限制。

### 匯總需求條件

materialized view 查詢中的匯總必須是輸出內容。系統不支援根據匯總值進行運算、篩選或聯結。舉例來說，系統不支援從下列查詢建立檢視區塊，因為這會產生從匯總計算的值 `COUNT(*) / 10 as cnt`。

```
SELECT TIMESTAMP_TRUNC(ts, HOUR) AS ts_hour, COUNT(*) / 10 AS cnt
FROM mydataset.mytable
GROUP BY ts_hour;
```

系統僅支援下列匯總函式：

* `ANY_VALUE` (但不得超過 `STRUCT`)
* `APPROX_COUNT_DISTINCT`
* `ARRAY_AGG` (但不得超過 `ARRAY` 或 `STRUCT`)
* `AVG`
* `BIT_AND`
* `BIT_OR`
* `BIT_XOR`
* `COUNT`
* `COUNTIF`
* `HLL_COUNT.INIT`
* `LOGICAL_AND`
* `LOGICAL_OR`
* `MAX`
* `MIN`
* `MAX_BY` (但不得超過 `STRUCT`)
* `MIN_BY` (但不得超過 `STRUCT`)
* `SUM`

### 不支援的 SQL 功能

具體化檢視表不支援下列 SQL 功能：

* `UNION ALL`。([支援 science 預先發布版](#left-union))
* `LEFT OUTER JOIN` ([支援 science 預先發布版](#left-union))
* `RIGHT/FULL OUTER JOIN`。
* 自我彙整，也就是多次使用同一個資料表上的 `JOIN`。
* [視窗函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/window-function-calls?hl=zh-tw)。
* `ARRAY` 子查詢。
* 非確定性函式，例如 `RAND()`、`CURRENT_DATE()`、`SESSION_USER()` 或 `CURRENT_TIME()`。
* [使用者定義的函式 (UDF)](https://docs.cloud.google.com/bigquery/docs/user-defined-functions?hl=zh-tw)。
* `TABLESAMPLE`。
* `FOR SYSTEM_TIME AS OF`。
* [生成式 AI 功能](https://docs.cloud.google.com/bigquery/docs/generative-ai-overview?hl=zh-tw)。

#### `LEFT OUTER JOIN` 和 `UNION ALL` 支援

**預覽**

這項功能適用《[服務專屬條款](https://docs.cloud.google.com/terms/service-terms?hl=zh-tw#1)》中「一般服務條款」一節的《正式發布前產品條款》。正式發布前功能是依「原樣」提供，支援服務可能受限。
詳情請參閱[推出階段說明](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages)。

如要尋求支援或提供意見回饋，請傳送電子郵件至 [bq-mv-help@google.com](mailto:bq-mv-help@google.com)。

遞增式具體化檢視表支援 `LEFT OUTER JOIN` 和 `UNION ALL`。
使用 `LEFT OUTER JOIN` 和 `UNION ALL` 陳述式的具體化檢視表，與其他遞增式具體化檢視表有相同的限制。此外，如果具體化檢視表包含 union all 或 left outer join，系統就不支援[智慧微調](https://docs.cloud.google.com/bigquery/docs/materialized-views-use?hl=zh-tw#smart_tuning)。

##### 範例

下列範例會建立具有 `LEFT JOIN` 的匯總遞增具體化檢視。當資料附加至左側表格時，這個檢視畫面會逐步更新。

```
CREATE MATERIALIZED VIEW dataset.mv
AS (
  SELECT
    s_store_sk,
    s_country,
    s_zip,
    SUM(ss_net_paid) AS sum_sales,
  FROM dataset.store_sales
  LEFT JOIN dataset.store
    ON ss_store_sk = s_store_sk
  GROUP BY 1, 2, 3
);
```

下列範例會建立具有 `UNION ALL` 的匯總遞增具體化檢視。當資料附加至任一或兩個資料表時，這個檢視畫面會逐步更新。如要進一步瞭解增量更新，請參閱「[增量更新](https://docs.cloud.google.com/bigquery/docs/materialized-views-use?hl=zh-tw#incremental_updates)」。

```
CREATE MATERIALIZED VIEW dataset.mv PARTITION BY DATE(ts_hour)
AS (
  SELECT
    SELECT TIMESTAMP_TRUNC(ts, HOUR) AS ts_hour, SUM(sales) sum_sales
  FROM
    (SELECT ts, sales from dataset.table1 UNION ALL
     SELECT ts, sales from dataset.table2)
  GROUP BY 1
);
```

### `WITH` 子句和一般資料表運算式 (CTE)

具體化檢視區塊支援 `WITH` 子句和一般資料表運算式。
含有 `WITH` 子句的具體化檢視表仍須遵循不含 `WITH` 子句的具體化檢視表模式和限制。

#### 範例

以下範例顯示使用 `WITH` 子句的具體化檢視表：

```
WITH tmp AS (
  SELECT TIMESTAMP_TRUNC(ts, HOUR) AS ts_hour, *
  FROM mydataset.mytable
)
SELECT ts_hour, COUNT(*) AS cnt
FROM tmp
GROUP BY ts_hour;
```

以下範例顯示使用 `WITH` 子句的具體化檢視，由於包含兩個 `GROUP BY` 子句，因此不支援：

```
WITH tmp AS (
  SELECT city, COUNT(*) AS population
  FROM mydataset.mytable
  GROUP BY city
)
SELECT population, COUNT(*) AS cnt
GROUP BY population;
```

### BigLake 資料表的具體化檢視表

如要[透過 BigLake 資料表建立具體化檢視表](https://docs.cloud.google.com/bigquery/docs/materialized-views-intro?hl=zh-tw#biglake)，BigLake 資料表必須[啟用中繼資料快取](https://docs.cloud.google.com/bigquery/docs/biglake-intro?hl=zh-tw#metadata_caching_for_performance)，並透過 Cloud Storage 資料建立具體化檢視表，且[`max_staleness`](#max_staleness) 選項值必須大於基本資料表。BigLake 資料表的具體化檢視表支援[與其他具體化檢視表相同的查詢集](https://docs.cloud.google.com/bigquery/docs/materialized-views-create?hl=zh-tw#query_limitations)。

#### 範例

使用 BigLake 基礎資料表建立匯總檢視區：

```
CREATE MATERIALIZED VIEW sample_dataset.sample_mv
    OPTIONS (max_staleness=INTERVAL "0:30:0" HOUR TO SECOND)
AS SELECT COUNT(*) cnt
FROM dataset.biglake_base_table;
```

如要進一步瞭解 BigLake 資料表具體化檢視表的限制，請參閱「[BigLake 資料表的具體化檢視表](https://docs.cloud.google.com/bigquery/docs/materialized-views-intro?hl=zh-tw#biglake)」。

### Apache Iceberg 外部資料表的具體化檢視表

您可以在具體化檢視區塊中參照大型 Iceberg 資料表，而不必將資料遷移至 BigQuery 代管儲存空間。

#### 在 Iceberg 資料表上建立具體化檢視表

下列範例會在分區基礎 Iceberg 資料表上建立與分區對齊的具體化檢視：

```
CREATE MATERIALIZED VIEW mydataset.myicebergmv
  PARTITION BY DATE_TRUNC(birth_month, MONTH)
AS
  SELECT * FROM mydataset.myicebergtable;
```

基礎 Iceberg 資料表 `myicebergtable` 必須具有[分區規格](https://iceberg.apache.org/spec/#partition-specs)，如下所示：

```
  "partition-specs" : [ {
    "spec-id" : 0,
    "fields" : [ {
    "name" : "birth_month",
    "transform" : "month",
    "source-id" : 3,
    "field-id" : 1000
    } ]
  } ]
```

#### 限制

除了標準 Iceberg 資料表的[限制](https://docs.cloud.google.com/bigquery/docs/iceberg-external-tables?hl=zh-tw#limitations)外，Iceberg 資料表上的具體化檢視區有下列限制：

* 您可以建立與基礎資料表分區對齊的具體化檢視表。不過，materialized view 僅支援以時間為準的[分割轉換](https://iceberg.apache.org/spec/#partition-transforms)，例如 `YEAR`、`MONTH`、`DAY` 和 `HOUR`。
* 具體化檢視表分區的精細程度不得高於基礎資料表分區的精細程度。舉例來說，如果您使用 `birth_date` 資料欄，每年為基礎資料表建立分區，系統就不支援使用 `PARTITION BY DATE_TRUNC(birth_date, MONTH)` 建立具體化檢視表。
* 如果基礎 Iceberg 資料表在超過 4000 個分割區中都有變更，即使具體化檢視區已分割，系統仍會在重新整理時完全失效。
* 支援[分區演進](https://iceberg.apache.org/spec/#partition-evolution)。不過，如果變更基礎資料表的分區資料欄，但未重新建立具體化檢視，可能會導致完全失效，且無法透過重新整理具體化檢視修正。
* 基本表格中必須至少有一個快照。
* Iceberg 資料表必須是 BigLake 資料表，例如已授權的外部資料表。
* 如果 Iceberg 資料表的 `metadata.json` 檔案已損毀，查詢具體化檢視可能會失敗。
* 如果啟用 [VPC Service Controls](https://docs.cloud.google.com/vpc-service-controls/docs/overview?hl=zh-tw)，您必須將授權外部資料表的服務帳戶新增至連入規則，否則 VPC Service Controls 會封鎖具體化檢視表的自動背景重新整理作業。

Iceberg 資料表的 `metadata.json` 檔案必須符合下列規格。如果沒有這些規格，查詢就會掃描基本資料表，而無法使用具體化結果。

* 在[資料表中繼資料](https://iceberg.apache.org/spec/#table-metadata)中：

  + `current-snapshot-id`
  + `current-schema-id`
  + `snapshots`
  + `snapshot-log`
* 在[快照](https://iceberg.apache.org/spec/#snapshots)中：

  + `parent-snapshot-id` (如有)
  + `schema-id`
  + `operation` (在「`summary`」欄位中)
* [分區](https://iceberg.apache.org/spec/#partitioning) (適用於分區 materialized view)

## 已分割的具體化檢視表

分區資料表上的具體化檢視表可以分區。materialized view 分區與一般資料表分區類似，如果查詢經常存取部分分區，就能帶來好處。此外，如果基礎資料表中的資料經過修改或刪除，實體化檢視分區也會改善檢視區隔的行為。詳情請參閱[磁碟分割區對齊](https://docs.cloud.google.com/bigquery/docs/materialized-views-use?hl=zh-tw#partition_alignment)。

如果基本資料表已分區，您就可以在相同的分區資料欄上對 materialized view 分區。如果是以時間為準的分區，精細程度必須一致 (每小時、每天、每月或每年)。如果是整數範圍分區，範圍規格必須完全相符。您無法在非分區基礎資料表上建立具體化檢視表分區。

如果基礎資料表是依擷取時間分區，則具體化檢視可以依基礎資料表的 `_PARTITIONDATE` 資料欄分組依據，也可以依該資料欄分區。如果您在建立 materialized view 時未明確指定分區，則 materialized view 就不會分區。

如果基本資料表已分區，建議您也將具體化檢視區分區，以降低[重新整理作業維護](https://docs.cloud.google.com/bigquery/docs/materialized-views-manage?hl=zh-tw)成本和查詢成本。

### 分區有效期限

無法為具體化檢視表設定分區到期時間。具體化檢視表會隱含地從基礎資料表繼承分區到期時間。具體化檢視區塊會與基礎資料表分區對齊，因此會同步過期。

**注意：** 如果非分區具體化檢視區是以設有分區到期時間的資料表為基礎，則分區到期時，該檢視區會失效，必須完整重新整理。因此，您應對 materialized view 區隔，以免產生額外的重新整理和查詢費用。

#### 範例 1

在本範例中，基礎資料表會依 `transaction_time` 資料欄分區，且每天都會分區。materialized view 會依相同資料欄分區，並依 `employee_id` 資料欄叢集。

```
CREATE TABLE my_project.my_dataset.my_base_table(
  employee_id INT64,
  transaction_time TIMESTAMP)
  PARTITION BY DATE(transaction_time)
  OPTIONS (partition_expiration_days = 2);

CREATE MATERIALIZED VIEW my_project.my_dataset.my_mv_table
  PARTITION BY DATE(transaction_time)
  CLUSTER BY employee_id
AS (
  SELECT
    employee_id,
    transaction_time,
    COUNT(employee_id) AS cnt
  FROM
    my_dataset.my_base_table
  GROUP BY
    employee_id, transaction_time
);
```

#### 範例 2

在本例中，基礎資料表是依擷取時間分區，且每天都有分區。materialized view 會選取擷取時間，並將其做為名為 `date` 的資料欄。具體化檢視會依 `date` 資料欄分組，並依相同資料欄分區。

```
CREATE MATERIALIZED VIEW my_project.my_dataset.my_mv_table
  PARTITION BY date
  CLUSTER BY employee_id
AS (
  SELECT
    employee_id,
    _PARTITIONDATE AS date,
    COUNT(1) AS count
  FROM
    my_dataset.my_base_table
  GROUP BY
    employee_id,
    date
);
```

#### 範例 3

在本範例中，基礎資料表會依據名為 `transaction_time` 的 `TIMESTAMP` 資料欄分區，並以每日分區。materialized view 會使用 [`TIMESTAMP_TRUNC`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/timestamp_functions?hl=zh-tw#timestamp_trunc) 函式，將值截斷至最接近的小時，藉此定義名為 `transaction_hour` 的資料欄。這個具體化檢視區塊會依 `transaction_hour` 分組，並依此分區。

注意事項：

* 套用至分區資料欄的截斷函式，必須至少與基本資料表的分區一樣精細。舉例來說，如果基本資料表使用每日分割區，截斷函式就無法使用 `MONTH` 或 `YEAR` 粒度。
* 在 materialized view 的分區規格中，精細程度必須與基礎資料表相符。

```
CREATE TABLE my_project.my_dataset.my_base_table (
  employee_id INT64,
  transaction_time TIMESTAMP)
  PARTITION BY DATE(transaction_time);

CREATE MATERIALIZED VIEW my_project.my_dataset.my_mv_table
  PARTITION BY DATE(transaction_hour)
AS (
  SELECT
    employee_id,
    TIMESTAMP_TRUNC(transaction_time, HOUR) AS transaction_hour,
    COUNT(employee_id) AS cnt
  FROM
    my_dataset.my_base_table
  GROUP BY
    employee_id,
    transaction_hour
);
```

## 叢集具體化檢視表

您可以依輸出資料欄叢集化具體化檢視，但須遵守 BigQuery [分群資料表限制](https://docs.cloud.google.com/bigquery/docs/clustered-tables?hl=zh-tw#limitations)。匯總輸出資料欄無法做為分群資料欄。在具體化檢視區塊中加入叢集資料欄，可提升查詢效能，包括對這些資料欄套用篩選條件的查詢。

### 參考邏輯 view

**預覽**

這項功能適用《[服務專屬條款](https://docs.cloud.google.com/terms/service-terms?hl=zh-tw#1)》中「一般服務條款」一節的《正式發布前產品條款》。正式發布前功能是依「原樣」提供，支援服務可能受限。
詳情請參閱[推出階段說明](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages)。

如要尋求支援或對這項功能提供意見回饋，請傳送電子郵件至 [bq-mv-help@google.com](mailto:bq-mv-help@google.com)。

materialized view 查詢可以參照邏輯檢視表，但須遵守下列限制：

* [具體化檢視表有相關限制](https://docs.cloud.google.com/bigquery/docs/materialized-views-intro?hl=zh-tw#limitations)。
* 如果邏輯檢視區塊變更，具體化檢視區塊就會失效，且必須完全重新整理。
* 不支援[智慧微調](https://docs.cloud.google.com/bigquery/docs/materialized-views-use?hl=zh-tw#smart_tuning)。

## 建立具體化檢視表的最佳做法

建立具體化檢視區塊時，請考慮下列最佳做法。

### 要建立哪些具體化檢視表

建立具體化檢視表時，請確保具體化檢視表定義反映對基礎資料表的查詢模式。如果具體化檢視區可服務廣泛的查詢集，而非僅限於特定查詢模式，則效果更佳。

舉例來說，假設使用者經常依 `user_id` 或 `department` 欄篩選資料表，您可以依這些資料欄分組依據，並選擇性地依這些資料欄叢集，而不必在具體化檢視畫面中新增 `user_id = 123` 等篩選器。

舉例來說，您可以使用確定性日期篩選器，指定特定日期 (例如 `WHERE order_date = '2019-10-01'`) 或日期範圍 (例如 `WHERE order_date BETWEEN '2019-10-01' AND '2019-10-31'`)。在 materialized view 中新增日期範圍篩選器，涵蓋查詢中的預期日期範圍：

```
CREATE MATERIALIZED VIEW ...
  ...
  WHERE date > '2019-01-01'
  GROUP BY date
```

### 具體化檢視表中的聯結

下列建議適用於含有 `JOIN` 陳述式的具體化檢視區塊。

#### 將最常變更的表格放在第一位

請確保檢視查詢中參照的第一個或最左側的資料表，是最大或最常變更的資料表。如果查詢中的第一個或最左側的表格附加了資料，則支援使用聯結的具體化檢視區塊會支援增量查詢和重新整理，但其他表格的變更會完全使檢視區塊快取失效。在星狀或雪花結構定義中，第一個或最左側的資料表通常應為事實資料表。

#### 避免在叢集鍵上進行聯結

如果資料經過大量匯總，或原始聯結查詢的成本很高，最適合使用含聯結的具體化檢視區塊。如果是選擇性查詢，BigQuery 通常已能有效執行聯結，因此不需要具體化檢視區塊。舉例來說，請考量下列具體化檢視區塊定義。

```
CREATE MATERIALIZED VIEW dataset.mv
  CLUSTER BY s_market_id
AS (
  SELECT
    s_market_id,
    s_country,
    SUM(ss_net_paid) AS sum_sales,
    COUNT(*) AS cnt_sales
  FROM dataset.store_sales
  INNER JOIN dataset.store
    ON ss_store_sk = s_store_sk
  GROUP BY s_market_id, s_country
);
```

假設 `store_sales` 是叢集在 `ss_store_sk` 上，且您經常執行下列查詢：

```
SELECT
  SUM(ss_net_paid)
FROM dataset.store_sales
INNER JOIN dataset.store
ON ss_store_sk = s_store_sk
WHERE s_country = 'Germany';
```

materialized view 的效率可能不如原始查詢。為獲得最佳成果，請使用具代表性的查詢組合進行實驗，並比較使用和未使用 materialized view 的結果。

## 使用 `max_staleness` 選項的具體化檢視表

處理大型且經常變更的資料集時，`max_staleness` materialized view 選項可協助您維持高查詢效能，同時控管費用。您可以透過 `max_staleness` 參數設定時間間隔，允許查詢結果的資料過時，藉此降低查詢成本和延遲時間。如果資訊主頁和報表不需要完全最新的查詢結果，這種做法就很有用。

### 資料過時

使用 `max_staleness` 選項集查詢具體化檢視表時，BigQuery 會根據 `max_staleness` 值和上次重新整理的時間傳回結果。

如果上次重新整理發生在 `max_staleness` 間隔內，BigQuery 會直接從具體化檢視傳回資料，而不讀取基本資料表。舉例來說，如果您的間隔為 4 小時，而上次重新整理是在 2 小時前，就會發生這種情況。`max_staleness`

如果上次重新整理的時間不在 `max_staleness` 間隔內，BigQuery 會從具體化檢視區塊讀取資料，並與上次重新整理後對基本資料表所做的變更合併，然後傳回合併結果。這個綜合結果可能仍會過時，最多會延遲 `max_staleness`間隔。舉例來說，如果 `max_staleness` 間隔為 4 小時，但上次重新整理發生在 7 小時前，就會套用這項規則。

### 使用「用 `max_staleness` 生成」選項

選取下列選項之一：

### SQL

如要使用 `max_staleness` 選項建立具體化檢視表，請在建立具體化檢視表時，將 `OPTIONS` 子句新增至 DDL 陳述式：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列陳述式：

   ```
   CREATE MATERIALIZED VIEW  project-id.my_dataset.my_mv_table
     OPTIONS (enable_refresh = true, refresh_interval_minutes = 60,
       max_staleness = INTERVAL "4:0:0" HOUR TO SECOND)
   AS SELECT
     employee_id,
     DATE(transaction_time),
     COUNT(1) AS count
   FROM my_dataset.my_base_table
   GROUP BY 1, 2;
   ```

   更改下列內容：

   * project-id 是您的專案 ID。
   * my\_dataset 是專案中資料集的 ID。
   * my\_mv\_table 是您要建立的 materialized view ID。
   * my\_base\_table 是資料集中的資料表 ID，可做為具體化檢視表的基礎資料表。
   * 按一下「執行」play\_circle。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

### API

在 API 要求中，使用已定義的 `materializedView` 資源呼叫 [`tables.insert`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables/insert?hl=zh-tw) 方法。`materializedView` 資源包含 `query` 欄位。例如：

```
{
  "kind": "bigquery#table",
  "tableReference": {
    "projectId": "project-id",
    "datasetId": "my_dataset",
    "tableId": "my_mv_table"
  },
  "materializedView": {
    "query": "select product_id,sum(clicks) as
                sum_clicks from project-id.my_dataset.my_base_table
                group by 1"
  }
  "maxStaleness": "4:0:0"
}
```

更改下列內容：

* project-id 是您的專案 ID。
* my\_dataset 是專案中資料集的 ID。
* my\_mv\_table 是您要建立的 materialized view ID。
* my\_base\_table 是資料集中的資料表 ID，可做為具體化檢視表的基礎資料表。
* `product_id` 是基本資料表中的資料欄。
* `clicks` 是基本資料表中的資料欄。
* `sum_clicks` 是您要建立的具體化檢視表中的資料欄。

### 套用 `max_staleness` 選項

您可以使用 `ALTER
MATERIALIZED VIEW` 陳述式，將這個參數套用至現有的具體化檢視區塊。例如：

```
ALTER MATERIALIZED VIEW project-id.my_dataset.my_mv_table
SET OPTIONS (enable_refresh = true, refresh_interval_minutes = 120,
  max_staleness = INTERVAL "8:0:0" HOUR TO SECOND);
```

### 使用「`max_staleness`」查詢

您可以透過 `max_staleness` 選項查詢實體化檢視區塊，就像查詢任何其他實體化檢視區塊、邏輯檢視區塊或資料表一樣。

例如：

```
SELECT * FROM  project-id.my_dataset.my_mv_table
```

如果資料不超過 `max_staleness` 參數的指定時間，這項查詢就會傳回上次重新整理的資料。如果 materialized view 在 `max_staleness` 間隔內未重新整理，BigQuery 會合併最新可用的重新整理結果與基本資料表變更，在 `max_staleness` 間隔內傳回結果。

#### 資料串流和 `max_staleness` 結果

如果使用 `max_staleness` 選項將資料串流至具體化檢視表的基礎資料表，具體化檢視表的查詢可能會排除在過時間隔開始前串流至資料表的記錄。因此，包含多個資料表資料和 `max_staleness` 選項的具體化檢視，可能無法代表這些資料表的某個時間點快照。

#### 串流資料和時間旅行限制

BigQuery 資料集的預設[時間回溯視窗](https://docs.cloud.google.com/bigquery/docs/time-travel?hl=zh-tw)為 7 天，但**串流儲存緩衝區**只會保留資料 3 天。這會對具體化檢視區塊造成下列限制：

* **查詢失敗：**如果具體化檢視使用 `max_staleness` 選項，且超過 3 天未重新整理，針對該檢視的查詢就會失敗，並顯示 `Streaming data from <materialized_view_name> is temporarily
  unavailable` 錯誤訊息。
* **原因：**查詢重寫程序嘗試從串流儲存空間緩衝區讀取增量變更 (差異) 時發生失敗。如果所需資料的保留期限超過 3 天，系統就無法擷取增量重寫所需的差異。

為避免發生這些錯誤，請確保[重新整理政策](https://docs.cloud.google.com/bigquery/docs/materialized-views-manage?hl=zh-tw#automatic-refresh)至少每 3 天更新一次 materialized view。

### 智慧微調和 `max_staleness` 選項

無論 `max_staleness` 選項為何，智慧型微調功能都會盡可能自動重新編寫查詢，以使用具體化檢視表，即使查詢未參照具體化檢視表也一樣。實體化檢視區的 `max_staleness` 選項不會影響重新編寫的查詢結果。`max_staleness` 選項只會影響直接查詢具體化檢視區塊的查詢。

### 管理過時和重新整理頻率

請根據需求設定 `max_staleness`。為避免從基本資料表讀取資料，請設定更新間隔，讓更新作業在過時間隔內完成。您可以將平均重新整理執行階段加上成長幅度。

舉例來說，如果重新整理具體化檢視需要一小時，且您希望有一小時的成長緩衝時間，則應將重新整理間隔設為兩小時。這項設定可確保報表在四小時的資料過時上限內重新整理。

```
CREATE MATERIALIZED VIEW project-id.my_dataset.my_mv_table
OPTIONS (enable_refresh = true, refresh_interval_minutes = 120, max_staleness =
INTERVAL "4:0:0" HOUR TO SECOND)
AS SELECT
  employee_id,
  DATE(transaction_time),
  COUNT(1) AS cnt
FROM my_dataset.my_base_table
GROUP BY 1, 2;
```

## 非累加式具體化檢視表

非增量具體化檢視表支援大多數 SQL 查詢，包括 `OUTER
JOIN`、`UNION` 和 `HAVING` 子句，以及分析函式。如要判斷查詢是否使用 materialized view，請使用[模擬測試](https://docs.cloud.google.com/bigquery/docs/materialized-views-intro?hl=zh-tw#interaction)檢查費用估算值。如果可以接受資料過時，例如用於批次資料處理或報表，非增量具體化檢視區塊可提升查詢效能並降低成本。您可以使用 `max_staleness` 選項建構任意複雜的具體化檢視區塊，這些檢視區塊會自動維護，並內建過時保證。

### 使用非累加式具體化檢視表

您可以使用 `allow_non_incremental_definition` 選項建立非遞增式具體化檢視表。這個選項必須搭配 `max_staleness` 選項使用。為確保實體化檢視區塊定期重新整理，您也應設定[重新整理政策](https://docs.cloud.google.com/bigquery/docs/materialized-views-manage?hl=zh-tw#enable_and_disable_automatic_refresh)。
如果沒有重新整理政策，您必須手動重新整理具體化檢視。

materialized view 一律代表 `max_staleness` 間隔內基本資料表的狀態。如果上次重新整理的時間太久，且無法代表 `max_staleness` 間隔內的基礎資料表，查詢就會讀取基礎資料表。如要進一步瞭解可能對效能造成的影響，請參閱「[資料過時](#data_staleness)」。

### 用 `allow_non_incremental_definition` 生成

如要使用 `allow_non_incremental_definition` 選項建立具體化檢視，請按照下列步驟操作。建立具體化檢視區塊後，您就無法修改 `allow_non_incremental_definition` 選項。舉例來說，您無法將 `true` 的值變更為 `false`，也無法從具體化檢視中移除 `allow_non_incremental_definition` 選項。

### SQL

建立具體化檢視表時，請在 DDL 陳述式中加入 `OPTIONS` 子句：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列陳述式：

   ```
   CREATE MATERIALIZED VIEW my_project.my_dataset.my_mv_table
   OPTIONS (
     enable_refresh = true, refresh_interval_minutes = 60,
     max_staleness = INTERVAL "4" HOUR,
       allow_non_incremental_definition = true)
   AS SELECT
     s_store_sk,
     SUM(ss_net_paid) AS sum_sales,
     APPROX_QUANTILES(ss_net_paid, 2)[safe_offset(1)] median
   FROM my_project.my_dataset.store
   LEFT OUTER JOIN my_project.my_dataset.store_sales
     ON ss_store_sk = s_store_sk
   GROUP BY s_store_sk
   HAVING median < 40 OR median is NULL ;
   ```

   請替換下列項目：

   * my\_project 是您的專案 ID。
   * my\_dataset 是專案中資料集的 ID。
   * my\_mv\_table 是您要建立的具體化檢視 ID。
   * my\_dataset.store 和
     my\_dataset.store\_sales 是資料集中資料表的 ID，這些資料表會做為具體化檢視的基礎資料表。
3. 按一下「執行」play\_circle。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

### API

在 API 要求中，使用已定義的 `materializedView` 資源呼叫 [`tables.insert`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables/insert?hl=zh-tw) 方法。`materializedView` 資源包含 `query` 欄位。例如：

```
{
  "kind": "bigquery#table",
  "tableReference": {
    "projectId": "my_project",
    "datasetId": "my_dataset",
    "tableId": "my_mv_table"
  },
  "materializedView": {
    "query": "`SELECT`
        s_store_sk,
        SUM(ss_net_paid) AS sum_sales,
        APPROX_QUANTILES(ss_net_paid, 2)[safe_offset(1)] median
      FROM my_project.my_dataset.store
      LEFT OUTER JOIN my_project.my_dataset.store_sales
        ON ss_store_sk = s_store_sk
      GROUP BY s_store_sk
      HAVING median < 40 OR median is NULL`",
    "allowNonIncrementalDefinition": true
  }
  "maxStaleness": "4:0:0"
}
```

更改下列內容：

* my\_project 是您的專案 ID。
* my\_dataset 是專案中資料集的 ID。
* my\_mv\_table 是您要建立的 materialized view ID。
* my\_dataset.store 和 my\_dataset.store\_sales 是資料集中的資料表 ID，做為具體化檢視的基礎資料表。

### 透過 Spanner 外部資料集建立具體化檢視表

繼續操作前，請先使用[`CLOUD_RESOURCE`連線](https://docs.cloud.google.com/bigquery/docs/spanner-external-datasets?hl=zh-tw#use_a_cloud_resource_connection)建立基礎 Spanner 外部資料集。

您可以使用 `allow_non_incremental_definition` 選項，建立參照 [Spanner 外部資料集資料表](https://docs.cloud.google.com/bigquery/docs/spanner-external-datasets?hl=zh-tw)的非遞增具體化檢視區塊。以下範例使用基礎 Spanner 外部資料集資料表：

```
/*
  You must create the spanner_external_dataset with a CLOUD_RESOURCE connection.
*/
CREATE MATERIALIZED VIEW sample_dataset.sample_spanner_mv
  OPTIONS (
      enable_refresh = true, refresh_interval_minutes = 60,
      max_staleness = INTERVAL "24" HOUR,
        allow_non_incremental_definition = true)
AS
  SELECT COUNT(*) cnt FROM spanner_external_dataset.spanner_table;
```

### 使用「`allow_non_incremental_definition`」查詢

您可以查詢非增量具體化檢視表，就像查詢任何其他具體化檢視表、邏輯檢視表或資料表一樣。

例如：

```
SELECT * FROM  my_project.my_dataset.my_mv_table
```

如果資料時間不早於 `max_staleness` 參數，這項查詢就會傳回上次重新整理的資料。如要進一步瞭解資料的過時程度和新舊程度，請參閱[資料過時程度](#data_staleness)。

### 非增量具體化檢視表的專屬限制

下列限制僅適用於使用 `allow_non_incremental_definition` 選項的具體化檢視區塊。除了支援的查詢語法限制外，所有[具體化檢視限制](https://docs.cloud.google.com/bigquery/docs/materialized-views-intro?hl=zh-tw#limitations)仍適用。

* 如果具體化檢視表包含 `allow_non_incremental_definition` 選項，系統不會套用智慧微調功能。如要透過 `allow_non_incremental_definition` 選項使用具體化檢視區塊，唯一方法是直接查詢這些檢視區塊。
* 不含 `allow_non_incremental_definition` 選項的具體化檢視表可以遞增方式重新整理部分資料。使用 `allow_non_incremental_definition` 選項的具體化檢視區塊必須完整重新整理。
* 使用 `max_staleness` 選項具體化的檢視畫面會在查詢執行期間，驗證資料欄層級安全限制是否存在。如要進一步瞭解這項功能，請參閱[資料欄層級存取控管](https://docs.cloud.google.com/bigquery/docs/column-level-security-intro?hl=zh-tw#time-travel)
* 對於 Spanner 外部資料集資料表的具體化檢視表，如果非增量具體化檢視表的上次重新整理時間不在 `max_staleness` 間隔內，即使基礎資料表未變更，查詢也會讀取基礎 Spanner 外部資料集資料表。舉例來說，如果 `max_staleness` 間隔為 4 小時，且上次重新整理發生在 7 小時前，則查詢會讀取基礎 Spanner 外部資料集資料表。

## 後續步驟

* [管理具體化檢視表](https://docs.cloud.google.com/bigquery/docs/materialized-views-manage?hl=zh-tw)。
* [使用具體化檢視表](https://docs.cloud.google.com/bigquery/docs/materialized-views-use?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-12 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-12 (世界標準時間)。"],[],[]]