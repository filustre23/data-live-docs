Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 建立 materialized view

**注意：** 如果預留項目是以特定 BigQuery 版本建立，可能無法使用這項功能。如要進一步瞭解各版本啟用的功能，請參閱「[BigQuery 版本簡介](https://docs.cloud.google.com/bigquery/docs/editions-intro?hl=zh-tw)」。

本文說明如何在 BigQuery 建立 materialized view。閱讀本文前，請先熟悉[具體化檢視表簡介](https://docs.cloud.google.com/bigquery/docs/materialized-views-intro?hl=zh-tw)。

## 事前準備

授予 Identity and Access Management (IAM) 角色，讓使用者具備必要權限，可執行本文件中的各項工作。

### 所需權限

如要建立 materialized view，您必須具備 `bigquery.tables.create` IAM 權限。

下列各項預先定義的 IAM 角色，都包含建立 materialized view 所需的權限：

* `bigquery.dataEditor`
* `bigquery.dataOwner`
* `bigquery.admin`

如要進一步瞭解 BigQuery Identity and Access Management (IAM)，請參閱「[使用 IAM 控管存取權](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)」。

## 建立 materialized view

如要建立 materialized view，請選取下列其中一個選項：

### SQL

使用 [`CREATE MATERIALIZED VIEW` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#create_materialized_view_statement)。以下範例會為每個產品 ID 的點擊次數建立 materialized view：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列陳述式：

   ```
   CREATE MATERIALIZED VIEW PROJECT_ID.DATASET.MATERIALIZED_VIEW_NAME AS (
     QUERY_EXPRESSION
   );
   ```

   替換下列內容：

   * `PROJECT_ID`：要建立 materialized view 的專案名稱，例如 `myproject`。
   * `DATASET`：要建立 materialized view 的 BigQuery 資料集名稱，例如 `mydataset`。如要透過 Amazon Simple Storage Service (Amazon S3) BigLake 資料表 ([預先發布版](https://cloud.google.com/products?hl=zh-tw#product-launch-stages)) 建立 materialized view，請確認資料集位於[支援的區域](https://docs.cloud.google.com/bigquery/docs/omni-introduction?hl=zh-tw#locations)。
   * `MATERIALIZED_VIEW_NAME`：要建立的 materialized view 名稱，例如 `my_mv`。
   * `QUERY_EXPRESSION`：定義 materialized view 的 GoogleSQL 查詢運算式，例如 `SELECT product_id, SUM(clicks) AS sum_clicks FROM
     mydataset.my_source_table`。
3. 按一下「play\_circle 執行」。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

**範例**

以下範例會為每個產品 ID 的點擊次數建立 materialized view：

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

使用 [`google_bigquery_table`](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/bigquery_table) 資源。

**注意：** 如要使用 Terraform 建立 BigQuery 物件，必須啟用 [Cloud Resource Manager API](https://docs.cloud.google.com/resource-manager/reference/rest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

以下範例說明如何建立名為 `my_materialized_view` 的檢視表：

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

   每個專案只需執行這個指令一次，而且可以在任何目錄中執行。

   ```
   export GOOGLE_CLOUD_PROJECT=PROJECT_ID
   ```

   如果您在 Terraform 設定檔中設定明確的值，環境變數就會遭到覆寫。

## 準備目錄

每個 Terraform 設定檔都必須有自己的目錄 (也稱為*根模組*)。

1. 在 [Cloud Shell](https://shell.cloud.google.com/?hl=zh-tw) 中建立目錄，並在該目錄中建立新檔案。檔案名稱必須有 `.tf` 副檔名，例如 `main.tf`。在本教學課程中，這個檔案稱為 `main.tf`。

   ```
   mkdir DIRECTORY && cd DIRECTORY && touch main.tf
   ```
2. 如果您正在按照教學課程操作，可以複製每個章節或步驟中的程式碼範例。

   將程式碼範例複製到新建立的 `main.tf`。

   您也可以從 GitHub 複製程式碼。如果 Terraform 程式碼片段是端對端解決方案的一部分，建議您採用這種做法。
3. 請查看並修改範例參數，以便套用至您的環境。
4. 儲存變更。
5. 初始化 Terraform。每個目錄只需執行一次這項操作。

   ```
   terraform init
   ```

   如要使用最新版 Google 供應商，請視需要加入 `-upgrade` 選項：

   ```
   terraform init -upgrade
   ```

## 套用變更

1. 查看設定，確認 Terraform 要建立或更新的資源符合預期：

   ```
   terraform plan
   ```

   視需要修正設定。
2. 執行下列指令，並在提示中輸入 `yes`，套用 Terraform 設定：

   ```
   terraform apply
   ```

   等待 Terraform 顯示「Apply complete!」訊息。
3. [開啟 Google Cloud 專案](https://console.cloud.google.com/?hl=zh-tw)即可查看結果。在 Google Cloud 控制台的使用者介面中，前往資源頁面，確認 Terraform 已建立或更新資源。

**注意：**Terraform 範例通常會假設 Google Cloud 專案已啟用必要的 API。

### API

呼叫 [`tables.insert` 方法](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables/insert?hl=zh-tw)，並傳入已定義 `materializedView` 欄位的 [`Table` 資源](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables?hl=zh-tw#Table)：

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

替換下列內容：

* `PROJECT_ID`：要建立 materialized view 的專案名稱，例如 `myproject`。
* `DATASET`：要建立 materialized view 的 BigQuery 資料集名稱，例如 `mydataset`。如要透過 Amazon Simple Storage Service (Amazon S3) BigLake 資料表 ([預先發布版](https://cloud.google.com/products?hl=zh-tw#product-launch-stages)) 建立 materialized view，請確認資料集位於[支援的區域](https://docs.cloud.google.com/bigquery/docs/omni-introduction?hl=zh-tw#locations)。
* `MATERIALIZED_VIEW_NAME`：要建立的 materialized view 名稱，例如 `my_mv`。
* `QUERY_EXPRESSION`：定義 materialized view 的 GoogleSQL 查詢運算式，例如 `SELECT product_id, SUM(clicks) AS sum_clicks FROM
  mydataset.my_source_table`。

**範例**

以下範例會為每個產品 ID 的點擊次數建立 materialized view：

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

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Java 設定操作說明進行操作。詳情請參閱 [BigQuery Java API 參考文件](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/overview?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

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

materialized view 建立成功後，會顯示在 Google Cloud 控制台 BigQuery 的「Explorer」窗格中。以下範例顯示 materialized view 結構定義：

除非您停用[自動重新整理](https://docs.cloud.google.com/bigquery/docs/materialized-views-manage?hl=zh-tw#automatic-refresh)功能，否則 BigQuery 會啟動 materialized view 的非同步完整重新整理。查詢會快速完成，但初始重新整理作業可能會繼續執行。

**注意：** 每個基礎資料表在同一個專案中最多只能有 100 個 materialized view，在同一個組織中最多只能有 500 個 materialized view。

## 存取控管

您可以在[資料集層級](https://docs.cloud.google.com/bigquery/docs/dataset-access-controls?hl=zh-tw)、[檢視表層級](https://docs.cloud.google.com/bigquery/docs/authorized-views?hl=zh-tw)或[資料欄層級](https://docs.cloud.google.com/bigquery/docs/column-level-security-intro?hl=zh-tw)授予 materialized view 的存取權。您也可以在 [IAM 資源階層](https://docs.cloud.google.com/iam/docs/resource-hierarchy-access-control?hl=zh-tw)中設定較高層級的存取權。

如要查詢 materialized view，您必須具備該檢視表及其基礎資料表的存取權。如要共用 materialized view，您可以授予基礎資料表的權限，或將 materialized view 設為授權 view。詳情請參閱「[授權檢視表](https://docs.cloud.google.com/bigquery/docs/authorized-views?hl=zh-tw)」。

### 存取控管限制

* 如果使用者查詢 materialized view 時，包含因資料欄層級安全性而無法存取的基礎資料表資料欄，查詢就會失敗，並顯示 `Access Denied` 訊息。
* 如果使用者查詢 materialized view，但對 materialized view 基礎資料表中的所有資料列沒有完整存取權，BigQuery 就會對基礎資料表執行查詢，而不是讀取 materialized view 資料。這可確保查詢遵循所有存取控管限制。查詢含有遮蓋資料欄的資料表時，也適用這項限制。

## materialized view 查詢支援

materialized view 採用受限的 SQL 語法。查詢必須採用下列模式：

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

增量 materialized view 有下列限制。

### 匯總需求條件

materialized view 查詢中的匯總必須是輸出內容。不支援依據匯總值進行運算、篩選或彙整。舉例來說，系統不支援透過下列查詢建立檢視表，因為這會產生從匯總 `COUNT(*) / 10 as cnt` 計算的值。

```
SELECT TIMESTAMP_TRUNC(ts, HOUR) AS ts_hour, COUNT(*) / 10 AS cnt
FROM mydataset.mytable
GROUP BY ts_hour;
```

系統僅支援下列匯總函式：

* `ANY_VALUE` (但不超過 `STRUCT`)
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
* `MAX_BY` (但不超過 `STRUCT`)
* `MIN_BY` (但不超過 `STRUCT`)
* `SUM`

### 不支援的 SQL 功能

materialized view 不支援下列 SQL 功能：

* `UNION ALL` ([science預先發布版支援](#left-union))
* `LEFT OUTER JOIN` ([science 預先發布版支援](#left-union))
* `RIGHT/FULL OUTER JOIN`。
* Self-join，也就是在同一個資料表上多次使用 `JOIN`。
* [Window 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/window-function-calls?hl=zh-tw)。
* `ARRAY` 個子查詢。
* 非確定性函式，例如 `RAND()`、`CURRENT_DATE()`、`SESSION_USER()` 或 `CURRENT_TIME()`。
* [使用者定義函式 (UDF)](https://docs.cloud.google.com/bigquery/docs/user-defined-functions?hl=zh-tw)。
* `TABLESAMPLE`。
* `FOR SYSTEM_TIME AS OF`。
* [生成式 AI 函式](https://docs.cloud.google.com/bigquery/docs/generative-ai-overview?hl=zh-tw)。

#### `LEFT OUTER JOIN`和`UNION ALL`支援

**預覽**

這項功能適用《[服務專屬條款](https://docs.cloud.google.com/terms/service-terms?hl=zh-tw#1)》中「一般服務條款」一節的《正式發布前產品條款》。正式發布前功能是依「原樣」提供，支援服務可能受限。
詳情請參閱[推出階段說明](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages)。

如要針對這項功能提供意見或尋求支援，請傳送電子郵件至 [bq-mv-help@google.com](mailto:bq-mv-help@google.com)。

增量 materialized view 支援 `LEFT OUTER JOIN` 和 `UNION ALL`。含有 `LEFT OUTER JOIN` 和 `UNION ALL` 陳述式的 materialized view，與其他增量 materialized view 有相同的限制。此外，如果 materialized view 含有 union all 或 left outer join，則不支援[智慧微調](https://docs.cloud.google.com/bigquery/docs/materialized-views-use?hl=zh-tw#smart_tuning)。對於使用 `UNION ALL` 的分區增量 materialized view，所有基礎資料表都必須採用相同的分區到期日 (TTL) 設定，才能維持[分區相符](https://docs.cloud.google.com/bigquery/docs/materialized-views-use?hl=zh-tw#partition_alignment)。如果基礎資料表的分區到期日不同，則會導致增量重新整理失敗。

##### 範例

下列範例會建立含有 `LEFT JOIN` 的匯總增量 materialized view。當資料附加至左側資料表時，這個檢視表會增量更新。

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

下列範例會建立含有 `UNION ALL` 的匯總增量 materialized view。當資料附加至其中一個或兩個資料表時，這個檢視表會增量更新。如要進一步瞭解增量更新，請參閱「[增量更新](https://docs.cloud.google.com/bigquery/docs/materialized-views-use?hl=zh-tw#incremental_updates)」。

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

materialized view 支援 `WITH` 子句和一般資料表運算式。含有 `WITH` 子句的 materialized view 仍須遵循不含 `WITH` 子句的 materialized view 模式和限制。

#### 範例

以下範例顯示使用 `WITH` 子句的 materialized view：

```
WITH tmp AS (
  SELECT TIMESTAMP_TRUNC(ts, HOUR) AS ts_hour, *
  FROM mydataset.mytable
)
SELECT ts_hour, COUNT(*) AS cnt
FROM tmp
GROUP BY ts_hour;
```

以下範例顯示使用 `WITH` 子句的 materialized view，但由於含有兩個 `GROUP BY` 子句，因此不受支援：

```
WITH tmp AS (
  SELECT city, COUNT(*) AS population
  FROM mydataset.mytable
  GROUP BY city
)
SELECT population, COUNT(*) AS cnt
GROUP BY population;
```

### BigLake 資料表的 materialized view

如要[根據 BigLake 資料表建立 materialized view](https://docs.cloud.google.com/bigquery/docs/materialized-views-intro?hl=zh-tw#biglake)，BigLake 資料表必須[啟用 Cloud Storage 資料的中繼資料快取](https://docs.cloud.google.com/bigquery/docs/biglake-intro?hl=zh-tw#metadata_caching_for_performance)，且 materialized view 的 [`max_staleness`](#max_staleness) 選項值必須大於基礎資料表。BigLake 資料表的 materialized view 支援與其他 materialized view [相同的查詢組合](https://docs.cloud.google.com/bigquery/docs/materialized-views-create?hl=zh-tw#query_limitations)。

#### 範例

使用 BigLake 基礎資料表建立匯總檢視表：

```
CREATE MATERIALIZED VIEW sample_dataset.sample_mv
    OPTIONS (max_staleness=INTERVAL "0:30:0" HOUR TO SECOND)
AS SELECT COUNT(*) cnt
FROM dataset.biglake_base_table;
```

如要進一步瞭解 BigLake 資料表具體化檢視表的限制，請參閱「[BigLake 資料表的具體化檢視表](https://docs.cloud.google.com/bigquery/docs/materialized-views-intro?hl=zh-tw#biglake)」。

### Apache Iceberg 外部資料表的 materialized view

您可以在 materialized view 中參照大型 Iceberg 資料表，不必將資料遷移至 BigQuery 代管儲存空間。

#### 依據 Iceberg 資料表建立 materialized view

下列範例會根據分區基礎 Iceberg 資料表，建立分區相符的 materialized view：

```
CREATE MATERIALIZED VIEW mydataset.myicebergmv
  PARTITION BY DATE_TRUNC(birth_month, MONTH)
AS
  SELECT * FROM mydataset.myicebergtable;
```

基礎 Iceberg 資料表 `myicebergtable` 必須具備[分區規格](https://iceberg.apache.org/spec/#partition-specs)，如下所示：

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

除了標準 Iceberg 資料表的[限制](https://docs.cloud.google.com/bigquery/docs/iceberg-external-tables?hl=zh-tw#limitations)外，Iceberg 資料表的 materialized view 還有下列限制：

* 您可以建立與基礎資料表分區相符的 materialized view。不過，materialized view 僅支援以時間為基礎的[分區轉換](https://iceberg.apache.org/spec/#partition-transforms)，例如 `YEAR`、`MONTH`、`DAY` 和 `HOUR`。
* materialized view 分區的精細程度，不得高於基礎資料表分區的精細程度。舉例來說，如果您使用 `birth_date` 資料欄每年分區基礎資料表，則不支援使用 `PARTITION BY DATE_TRUNC(birth_date, MONTH)` 建立 materialized view。
* 如果基礎 Iceberg 資料表有超過 4,000 個分區發生變更，則 materialized view 重新整理後會完全失效，即使已分區也一樣。
* 支援[分區演變](https://iceberg.apache.org/spec/#partition-evolution)。不過，如果變更基礎資料表的分區欄，但未重新建立 materialized view，可能會導致完全失效，且無法透過重新整理 materialized view 來修正。
* 基礎資料表中至少須有一個快照。
* Iceberg 資料表必須是 BigLake 資料表，例如已授權的外部資料表。
* 如果 Iceberg 資料表的 `metadata.json` 檔案損毀，materialized view 查詢可能會失敗。
* 如果已啟用 [VPC Service Controls](https://docs.cloud.google.com/vpc-service-controls/docs/overview?hl=zh-tw)，則必須將授權外部資料表的服務帳戶新增至輸入規則，否則 VPC Service Controls 會封鎖 materialized view 的自動背景重新整理。

Iceberg 資料表的 `metadata.json` 檔案必須符合下列規格。如果沒有這些規格，查詢會掃描基礎資料表，無法使用具體化結果。

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

## 分區 materialized view

分區資料表上的 materialized view 可以分區。對 materialized view 進行分區，與對一般資料表進行分區類似，當查詢經常存取分區子集時，這種做法可帶來好處。此外，如果基礎資料表中的資料遭到修改或刪除，對 materialized view 進行分區可改善檢視表的行為。詳情請參閱「[分區相符](https://docs.cloud.google.com/bigquery/docs/materialized-views-use?hl=zh-tw#partition_alignment)」。

如果基礎資料表已分區，您可以在同一個分區資料欄上，對 materialized view 進行分區。如果是以時間為依據的分區，精細程度必須相符 (每小時、每日、每月或每年)。如果是整數範圍分區，範圍規格必須完全相符。您無法在非分區基礎資料表上，對 materialized view 進行分區。

如果基礎資料表是依擷取時間分區，則 materialized view 可以依基礎資料表的 `_PARTITIONDATE` 欄分組，並依該欄分區。如果您在建立 materialized view 時未明確指定分區，則 materialized view 不會分區。

如果基礎資料表已分區，建議您也將 materialized view 分區，以降低[重新整理工作維護](https://docs.cloud.google.com/bigquery/docs/materialized-views-manage?hl=zh-tw)費用和查詢費用。

### 分區有效期限

無法為 materialized view 設定分區到期時間。materialized view 會隱含繼承基礎資料表的分區到期時間。materialized view 分區會與基礎資料表分區對齊，因此會同步到期。

**注意：** 如果非分區 materialized view 是以設有分區到期時間的資料表為基礎，則分區到期時，該檢視表會失效，必須完整重新整理。因此，您應對 materialized view 進行分區，以免產生額外的重新整理和查詢費用。

#### 範例 1

在本例中，基礎資料表會依 `transaction_time` 資料欄分區，並採用每日分區。materialized view 會依相同資料欄分區，並依 `employee_id` 資料欄分群。

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

在這個範例中，基礎資料表是按擷取時間進行分區，並採用每日分區。materialized view 會選取擷取時間，並將其命名為 `date` 資料欄。materialized view 會依 `date` 資料欄分組，並依同一資料欄分區。

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

在本例中，基礎資料表會依名為 `transaction_time` 的 `TIMESTAMP` 資料欄分區，並按日分區。materialized view 定義名為 `transaction_hour` 的資料欄，並使用 [`TIMESTAMP_TRUNC`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/timestamp_functions?hl=zh-tw#timestamp_trunc) 函式將值截斷至最接近的小時。materialized view 會依 `transaction_hour` 分組，並依該資料欄分區。

注意事項：

* 套用至分區資料欄的截斷函式，精細程度至少須與基礎資料表的分區相同。舉例來說，如果基礎資料表使用每日分區，則截斷函式無法使用 `MONTH` 或 `YEAR` 精細程度。
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

## 叢集 materialized view

您可以依據輸出資料欄，將 materialized view 分群，但須遵守 BigQuery [分群資料表限制](https://docs.cloud.google.com/bigquery/docs/clustered-tables?hl=zh-tw#limitations)。匯總輸出欄無法做為叢集欄。在 materialized view 中新增分群資料欄，可提升包含這些資料欄篩選條件的查詢效能。

### 參考邏輯檢視表

**預覽**

這項功能適用《[服務專屬條款](https://docs.cloud.google.com/terms/service-terms?hl=zh-tw#1)》中「一般服務條款」一節的《正式發布前產品條款》。正式發布前功能是依「原樣」提供，支援服務可能受限。
詳情請參閱[推出階段說明](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages)。

如要針對這項功能提供意見或尋求支援，請傳送電子郵件至 [bq-mv-help@google.com](mailto:bq-mv-help@google.com)。

materialized view 查詢可以參照邏輯 view，但須遵守下列限制：

* [適用 materialized view 限制](https://docs.cloud.google.com/bigquery/docs/materialized-views-intro?hl=zh-tw#limitations)。
* 如果邏輯檢視表有所變更，materialized view 就會失效，必須完整重新整理。
* 不支援[智慧微調](https://docs.cloud.google.com/bigquery/docs/materialized-views-use?hl=zh-tw#smart_tuning)。

## 建立 materialized view 的最佳做法

建立 materialized view 時，建議您考量下列最佳做法。

### 要建立哪些 materialized view

建立 materialized view 時，請確保 materialized view 定義反映了基礎資料表的查詢模式。materialized view 適用於廣泛的查詢，而非單一特定查詢模式。

舉例來說，假設使用者經常依 `user_id` 或 `department` 資料欄篩選資料表，您可以依這些資料欄分組，並視需要依這些資料欄分群，而不是在 materialized view 中新增 `user_id = 123` 等篩選器。

另一個例子是，您可以使用確定性日期篩選器，依特定日期 (例如 `WHERE order_date = '2019-10-01'`) 或日期範圍 (例如 `WHERE order_date BETWEEN '2019-10-01' AND '2019-10-31'`) 篩選。在 materialized view 中新增日期範圍篩選器，涵蓋查詢中的預期日期範圍：

```
CREATE MATERIALIZED VIEW ...
  ...
  WHERE date > '2019-01-01'
  GROUP BY date
```

### materialized view 中的彙整

下列建議適用於含有 `JOIN` 陳述式的 materialized view。

#### 將最常變更的資料表放在最前面

請確保最大或最常變更的資料表，是檢視表查詢中第一個或最左側參照的資料表。如果查詢中的第一個或最左側資料表附加了資料，則具有 join 的 materialized view 支援增量查詢和重新整理，但對其他資料表的變更會完全使檢視快取失效。在星狀或雪花狀結構定義中，第一個或最左側的資料表通常應為事實資料表。

#### 避免依叢集鍵進行彙整

如果資料經過大量匯總，或原始 join 查詢費用高昂，則最適合使用含有 join 的 materialized view。對於選擇性查詢，BigQuery 通常已能有效執行 join，不需要 materialized view。舉例來說，請參考下列 materialized view 定義。

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

假設 `store_sales` 是在 `ss_store_sk` 上分群，而您經常執行類似下列的查詢：

```
SELECT
  SUM(ss_net_paid)
FROM dataset.store_sales
INNER JOIN dataset.store
ON ss_store_sk = s_store_sk
WHERE s_country = 'Germany';
```

materialized view 的效率可能不如原始查詢。為獲得最佳結果，請使用一組具代表性的查詢進行實驗，並比較使用和不使用 materialized view 的結果。

## 使用 `max_staleness` 選項的 materialized view

`max_staleness` materialized view 選項可協助您在處理大型、經常變更的資料集時，以可控的成本持續獲得高查詢效能。使用 `max_staleness` 參數，您可以設定查詢結果資料過時的可接受時間間隔，藉此降低查詢成本和延遲時間。如果資訊主頁和報表不需要完全最新的查詢結果，這種行為就很有用。

### 資料過時

當您查詢已設定 `max_staleness` 選項的 materialized view 時，BigQuery 會根據 `max_staleness` 值和上次重新整理的時間傳回結果。

如果上次重新整理是在 `max_staleness` 間隔內進行，BigQuery 會直接從 materialized view 傳回資料，而不會讀取基礎資料表。舉例來說，如果 `max_staleness` 間隔為 4 小時，而上次重新整理是在 2 小時前，就會發生這種情況。

如果上次重新整理的時間超出 `max_staleness` 間隔，BigQuery 會從 materialized view 讀取資料，並與上次重新整理後對基礎資料表所做的變更合併，然後傳回合併結果。這項合併結果可能仍會過時，最長可達 `max_staleness` 間隔。舉例來說，如果 `max_staleness` 間隔為 4 小時，而上次重新整理是在 7 小時前，就會發生這種情況。

### 「用 `max_staleness` 生成」選項

選取下列選項之一：

### SQL

如要建立具有 `max_staleness` 選項的 materialized view，請在建立 materialized view 時，在 DDL 陳述式中加入 `OPTIONS` 子句：

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
   * my\_dataset 是專案中的資料集 ID。
   * my\_mv\_table 是您要建立的 materialized view ID。
   * my\_base\_table 是資料集中資料表的 ID，做為 materialized view 的基礎資料表。
   * 按一下「play\_circle 執行」。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

### API

呼叫 [`tables.insert`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables/insert?hl=zh-tw) 方法，並在 API 要求中定義 `materializedView` 資源。`materializedView` 資源包含 `query` 欄位。例如：

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
* my\_dataset 是專案中的資料集 ID。
* my\_mv\_table 是您要建立的 materialized view ID。
* my\_base\_table 是資料集中資料表的 ID，做為 materialized view 的基礎資料表。
* `product_id` 是基礎資料表中的資料欄。
* `clicks` 是基礎資料表中的資料欄。
* `sum_clicks` 是您要建立的 materialized view 中的資料欄。

### 套用 `max_staleness` 選項

您可以使用 `ALTER
MATERIALIZED VIEW` 陳述式，將這項參數套用至現有的 materialized view。例如：

```
ALTER MATERIALIZED VIEW project-id.my_dataset.my_mv_table
SET OPTIONS (enable_refresh = true, refresh_interval_minutes = 120,
  max_staleness = INTERVAL "8:0:0" HOUR TO SECOND);
```

### 使用`max_staleness`查詢

您可以使用 `max_staleness` 選項查詢 materialized view，就像查詢任何其他 materialized view、邏輯檢視表或資料表一樣。

例如：

```
SELECT * FROM  project-id.my_dataset.my_mv_table
```

如果資料未超過 `max_staleness` 參數，這項查詢會傳回上次重新整理的資料。如果 materialized view 未在 `max_staleness` 間隔內重新整理，BigQuery 會將最新可用重新整理作業的結果與基礎資料表變更合併，傳回 `max_staleness` 間隔內的結果。

#### 資料串流和`max_staleness`結果

如果您使用 `max_staleness` 選項將資料串流至 materialized view 的基礎資料表，materialized view 的查詢可能會排除在過時時間間隔開始前，串流至其資料表的記錄。因此，如果 materialized view 包含多個資料表的資料和 `max_staleness` 選項，可能無法代表這些資料表的時間點快照。

#### 串流資料和時間旅行限制

雖然 BigQuery 資料集的預設[時間回溯期](https://docs.cloud.google.com/bigquery/docs/time-travel?hl=zh-tw)為 7 天，但**串流儲存空間緩衝區**只會保留 3 天的資料。這會對 materialized view 造成下列限制：

* **查詢失敗：**如果 materialized view 使用 `max_staleness` 選項，且超過 3 天未重新整理，對該檢視表執行的查詢會失敗，並顯示錯誤訊息 `Streaming data from <materialized_view_name> is temporarily
  unavailable`。
* **原因：**查詢重寫程序嘗試從串流儲存空間緩衝區讀取增量變更 (差異)，因此發生失敗。如果所需資料超過 3 天的保留期限，系統就無法擷取增量重寫所需的差異。

為避免發生這些錯誤，請確保[重新整理政策](https://docs.cloud.google.com/bigquery/docs/materialized-views-manage?hl=zh-tw#automatic-refresh)至少每 3 天更新一次 materialized view。

### 智慧微調和 `max_staleness` 選項

無論 `max_staleness` 選項為何，智慧微調功能都會自動重寫查詢，盡可能使用 materialized view，即使查詢未參照 materialized view 也一樣。materialized view 的 `max_staleness` 選項不會影響重寫查詢的結果。`max_staleness` 選項只會影響直接查詢 materialized view 的查詢。

### 管理過時和重新整理頻率

請根據需求設定 `max_staleness`。為避免從基礎資料表讀取資料，請設定重新整理間隔，讓重新整理作業在過時時間間隔內進行。您可以將平均重新整理執行時間加上成長幅度。

舉例來說，如果重新整理 materialized view 需要一小時，且您希望保留一小時的緩衝時間，則應將重新整理間隔設為兩小時。這項設定可確保重新整理作業在報表最長四小時的過時時間內完成。

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

## 非增量 materialized view

非漸進式 materialized view 支援大多數 SQL 查詢，包括 `OUTER
JOIN`、`UNION` 和 `HAVING` 子句，以及數據分析函式。如要判斷查詢是否使用 materialized view，請透過[模擬測試](https://docs.cloud.google.com/bigquery/docs/materialized-views-intro?hl=zh-tw#interaction)查看預估費用。在可接受資料過時的情況下 (例如批次資料處理或報表)，非增量 materialized view 可提升查詢效能並降低成本。使用 `max_staleness` 選項，即可建構任意、複雜的 materialized view，系統會自動維護這些檢視表，並內建過時限制。

### 使用非增量 materialized view

您可以使用 `allow_non_incremental_definition` 選項，建立非增量 materialized view。這個選項必須與 `max_staleness` 選項搭配使用。為確保定期重新整理 materialized view，您也應設定[重新整理政策](https://docs.cloud.google.com/bigquery/docs/materialized-views-manage?hl=zh-tw#enable_and_disable_automatic_refresh)。如果沒有重新整理政策，您就必須手動重新整理 materialized view。

materialized view 一律代表 `max_staleness` 間隔內基礎資料表的狀態。如果上次重新整理的時間過久，無法代表 `max_staleness` 間隔內的基礎資料表，查詢就會讀取基礎資料表。如要進一步瞭解可能對效能造成的影響，請參閱「[資料過時](#data_staleness)」。

### 用 `allow_non_incremental_definition` 生成

如要使用 `allow_non_incremental_definition` 選項建立 materialized view，請按照下列步驟操作。建立 materialized view 後，您就無法修改 `allow_non_incremental_definition` 選項。舉例來說，您無法將 `true` 值變更為 `false`，也無法從 materialized view 移除 `allow_non_incremental_definition` 選項。

### SQL

建立 materialized view 時，請在 DDL 陳述式中新增 `OPTIONS` 子句：

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

   更改下列內容：

   * my\_project 是您的專案 ID。
   * my\_dataset 是專案中的資料集 ID。
   * my\_mv\_table 是您要建立的 materialized view ID。
   * my\_dataset.store 和 my\_dataset.store\_sales 是資料集中資料表的 ID，可做為 materialized view 的基礎資料表。
3. 按一下「play\_circle 執行」。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

### API

呼叫 [`tables.insert`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables/insert?hl=zh-tw) 方法，並在 API 要求中定義 `materializedView` 資源。`materializedView` 資源包含 `query` 欄位。例如：

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
* my\_dataset 是專案中的資料集 ID。
* my\_mv\_table 是您要建立的 materialized view ID。
* my\_dataset.store 和 my\_dataset.store\_sales 是資料集中資料表的 ID，做為 materialized view 的基礎資料表。

### 建立 Spanner 外部資料集的 materialized view

繼續操作前，請務必使用 [`CLOUD_RESOURCE` 連線](https://docs.cloud.google.com/bigquery/docs/spanner-external-datasets?hl=zh-tw#use_a_cloud_resource_connection)建立基礎 Spanner 外部資料集。

您可以使用 `allow_non_incremental_definition` 選項，建立參照 [Spanner 外部資料集資料表](https://docs.cloud.google.com/bigquery/docs/spanner-external-datasets?hl=zh-tw)的非漸進式 materialized view。以下範例使用基礎 Spanner 外部資料集資料表：

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

### 使用`allow_non_incremental_definition`查詢

您可以查詢非增量 materialized view，就像查詢任何其他 materialized view、邏輯檢視表或資料表一樣。

例如：

```
SELECT * FROM  my_project.my_dataset.my_mv_table
```

如果資料的時間不超過 `max_staleness` 參數，這項查詢會傳回上次重新整理的資料。如要進一步瞭解資料過時和更新間隔，請參閱「[資料過時](#data_staleness)」一節。

### 非增量 materialized view 的特定限制

下列限制僅適用於具有 `allow_non_incremental_definition` 選項的 materialized view。除了支援的查詢語法限制外，所有[materialized view 限制](https://docs.cloud.google.com/bigquery/docs/materialized-views-intro?hl=zh-tw#limitations)仍適用。

* 智慧微調功能不適用於包含 `allow_non_incremental_definition` 選項的 materialized view。如要使用 `allow_non_incremental_definition` 選項，唯一能發揮 materialized view 效益的方法，就是直接查詢。
* 不含 `allow_non_incremental_definition` 選項的 materialized view，可以遞增重新整理部分資料。如果 materialized view 含有 `allow_non_incremental_definition` 選項，則必須完整重新整理。
* 如果 materialized view 設有 `max_staleness` 選項，系統會在執行查詢時，驗證是否存在資料欄層級安全性限制。詳情請參閱「[資料欄層級存取控管](https://docs.cloud.google.com/bigquery/docs/column-level-security-intro?hl=zh-tw#time-travel)」
* 對於 Spanner 外部資料集資料表的 materialized view，如果非增量 materialized view 的上次重新整理時間超出 `max_staleness` 間隔，則查詢會讀取基礎 Spanner 外部資料集資料表，即使基礎資料表未變更也一樣。舉例來說，如果 `max_staleness` 間隔為 4 小時，且上次重新整理時間為 7 小時前，則查詢會讀取基礎 Spanner 外部資料集資料表。

## 後續步驟

* [管理 materialized view](https://docs.cloud.google.com/bigquery/docs/materialized-views-manage?hl=zh-tw)。
* [使用 materialized view](https://docs.cloud.google.com/bigquery/docs/materialized-views-use?hl=zh-tw)。
* [疑難排解 materialized view 問題](https://docs.cloud.google.com/bigquery/docs/materialized-views-troubleshoot?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-10-16 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-10-16 (世界標準時間)。"],[],[]]