Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 聯合查詢簡介

本頁面將介紹如何使用聯合查詢，並提供從 BigQuery 查詢 Spanner、AlloyDB 和 Cloud SQL 資料的指南。

聯合查詢可讓您將查詢陳述式傳送至 AlloyDB、Spanner 或 Cloud SQL 資料庫，並以臨時資料表的形式傳回結果。聯合查詢會使用 BigQuery Connection API，與 AlloyDB、Spanner 或 Cloud SQL 建立連線。在查詢中，您可以使用 `EXTERNAL_QUERY` 函式，以該資料庫的 SQL 方言，將查詢陳述式傳送至外部資料庫。結果會轉換為 GoogleSQL 資料類型。

## 支援的資料儲存庫

您可以在下列資料儲存庫中使用聯合查詢：

* [Spanner](https://docs.cloud.google.com/bigquery/docs/spanner-federated-queries?hl=zh-tw)
* [Cloud SQL](https://docs.cloud.google.com/bigquery/docs/cloud-sql-federated-queries?hl=zh-tw)
* [AlloyDB](https://docs.cloud.google.com/bigquery/docs/alloydb-federated-queries?hl=zh-tw)
* [SAP Datasphere](https://docs.cloud.google.com/bigquery/docs/sap-datasphere-federated-queries?hl=zh-tw) ([預先發布版](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages))

## 工作流程

* 找出包含要查詢資料來源的 Google Cloud 專案。
* `bigquery.admin` 使用者在 BigQuery 中建立連線資源。
* 管理員使用者將[使用連線資源的權限授予](https://docs.cloud.google.com/bigquery/docs/working-with-connections?hl=zh-tw#share-connections)使用者 B。
  + 如果管理員和使用者 B 是同一人，則無須授予權限。
* 使用者 B 使用新的 [`EXTERNAL_QUERY`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/federated_query_functions?hl=zh-tw#external_query) SQL 函式在 BigQuery 中編寫查詢。

**注意事項：** 相較於讀取 BigQuery 儲存空間中資料的查詢，聯合式查詢的執行效能可能較差。

## 聯合查詢的替代方案：外部資料表和資料集

如要查詢 Bigtable、Spanner、Cloud Storage、Google 雲端硬碟和 Salesforce Data Cloud 等營運資料庫，也可以使用外部資料表和資料集。您可以使用外部資料集和資料表查看資料表及其結構定義，並查詢資料，不必使用 [`EXTERNAL_QUERY`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/federated_query_functions?hl=zh-tw#external_query) SQL 函式。您不必將資料帶回 BigQuery，而且可以使用 BigQuery 語法，不必以 SQL 的特定 SQL 資料庫方言撰寫程式碼。

## 支援的地區

如需支援的地點清單，請參閱以下章節：

### AlloyDB 和 Cloud SQL

只有同時支援外部資料來源和 BigQuery 的地區，才能使用聯合查詢。

* [Cloud SQL 執行個體位置](https://docs.cloud.google.com/sql/docs/mysql/locations?hl=zh-tw)。
* [AlloyDB 地點](https://docs.cloud.google.com/alloydb/docs/locations?hl=zh-tw)。
* [BigQuery 資料集位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)。

您可以根據下列規則建立連線，並跨區域執行聯合查詢：

**單一地區**

BigQuery 單一地區只能查詢相同地區中的資源。

舉例來說，如果資料集位於 `us-east4`，您可以查詢位於 `us-east4` 的 Cloud SQL 執行個體或 AlloyDB 執行個體。[查詢處理位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw#specify_locations)是 BigQuery 單一區域。

**多地區**

BigQuery 的多地區可以查詢相同大型地理區域 (美國、歐盟) 中的任何資料來源地區。Cloud SQL 執行個體不支援[多區域位置](https://docs.cloud.google.com/sql/docs/mysql/locations?hl=zh-tw)，因為這些位置僅用於備份。

* 在 BigQuery US 多地區執行的查詢，可以查詢美國地理區域中的任何單一地區，例如 `us-central1`、`us-east4` 或 `us-west2`。

  **注意：** 不支援從美國多區域的 BigQuery 資料集，查詢位於 `southamerica-east1` 的外部資料來源。
* 在 BigQuery EU 多地區執行的查詢，可以查詢歐盟[成員國](https://europa.eu/european-union/about-eu/countries_en)的任何單一地區，例如 `europe-north1` 或 `europe-west3`。
* 查詢的執行位置必須與連線資源的位置相同。舉例來說，從美國多區域執行的查詢必須使用位於美國多區域的連線。

  **注意：** 源自多區域的查詢無法再參照單一區域中的連線。如果連線受到影響，請在與查詢相同的多區域中重新建立連線。

查詢效能取決於資料集與外部資料來源之間的鄰近程度。舉例來說，在美國多區域的資料集和 `us-central1` 中的 Cloud SQL 執行個體之間進行聯合查詢時，速度很快。不過，如果您在美國多區域和 `us-east4` 的 Cloud SQL 執行個體之間執行相同的查詢，效能可能會降低。

[查詢處理位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw#specify_locations)是多地區位置，即 `US` 或 `EU`。

### Spanner

[Spanner 支援區域和多區域設定](https://docs.cloud.google.com/spanner/docs/instance-configurations?hl=zh-tw)。BigQuery 單一地區/多地區可以查詢任何支援的 Spanner 地區中的 Spanner 執行個體。詳情請參閱[跨區域查詢](https://docs.cloud.google.com/bigquery/docs/spanner-federated-queries?hl=zh-tw#cross_region_queries)。

## 資料類型對應關係

執行聯合查詢時，外部資料來源中的資料會轉換為 GoogleSQL 類型。詳情請參閱「[Cloud SQL 聯合式查詢](https://docs.cloud.google.com/bigquery/docs/cloud-sql-federated-queries?hl=zh-tw)」。

## 配額與限制

* **跨區域聯合查詢**。如果 [BigQuery 查詢處理位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw#specify_locations)和外部資料來源位置不同，就會視為跨區域查詢。每個專案每日可執行高達 1 TB 的跨地區查詢。以下是跨區域查詢的範例。
  + Cloud SQL 執行個體位於 `us-west1`，而 BigQuery 連線則位於美國多區域位置。BigQuery 查詢處理位置為 `US`。
* **Quota**。使用者應控制外部資料來源 (例如 Cloud SQL 或 AlloyDB) 中的查詢配額，聯合式查詢沒有額外的配額設定。如要確實隔離工作負載，建議您僅查詢資料庫唯讀備用資源。
* **允許的計費位元組上限**。這個欄位不支援聯合式查詢。系統無法事先估算實際執行聯合式查詢之後會產生費用的位元組數。
* **連線數量**。聯合查詢最多可以建立 10 個不重複的連線。
* **Cloud SQL [MySQL](https://docs.cloud.google.com/sql/docs/mysql/quotas?hl=zh-tw) 和
  [PostgreSQL](https://docs.cloud.google.com/sql/docs/postgres/quotas?hl=zh-tw)**。須遵守配額和限制。

## 限制

聯合查詢必須遵循以下限制：

* **效能**。聯合查詢的執行速度可能低於僅查詢 BigQuery 儲存空間。BigQuery 必須等待來源資料庫執行外部查詢，並暫時將資料從外部資料來源移至 BigQuery。此外，來源資料庫可能不適合用於較為複雜的分析查詢。

  查詢效能也會因資料集與外部資料來源的距離而異。詳情請參閱「[支援的區域](https://docs.cloud.google.com/bigquery/docs/federated-queries-intro?hl=zh-tw#supported_regions)」。
* **聯合查詢是唯讀查詢**。在來源資料庫中執行的外部查詢必須為唯讀。因此不支援 DML 或 DDL 陳述式。
* **不支援的資料類型**。如果外部查詢含有 BigQuery 不支援的資料類型，查詢作業就會立即失敗。您可以將不支援的資料類型轉換為支援的其他資料類型。
* **客戶自行管理的加密金鑰 (CMEK)**。您必須分別為 BigQuery 和外部資料來源設定 CMEK。如果您將來源資料庫設為使用 CMEK，但 BigQuery 未使用，則包含聯合查詢結果的暫時資料表會以 Google-owned and Google-managed encryption key加密。

## 定價

* 如果您採用以量計價模式，透過 BigQuery 執行聯合查詢時，系統會針對外部查詢傳回的位元組數向您收費。詳情請參閱「[以量計價的分析定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#on_demand_pricing)」。
* 如果您使用 BigQuery 版本，系統會根據您使用的運算單元數量收費。詳情請參閱「[容量運算定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#capacity_compute_analysis_pricing)」。

## SQL 下推

聯合查詢會受到稱為 SQL 下推的最佳化技術影響。這類函式會將篩選等作業委派給外部資料來源，而不是在 BigQuery 中執行，因此可提升查詢效能。減少從外部資料來源移轉的資料量，可縮短查詢執行時間並降低成本。SQL 下推包括資料欄修剪 (`SELECT` 子句) 和篩選器下推 (`WHERE` 子句)。

使用 `EXTERNAL_QUERY` 函式時，SQL 下推作業會重寫原始查詢。在下列範例中，`EXTERNAL_QUERY` 函式用於與 Cloud SQL 資料庫通訊：

```
SELECT COUNT(*)
FROM (
  SELECT * FROM EXTERNAL_QUERY("CONNECTION_ID", "select * from operations_table")
  )
WHERE a = 'Y' AND b NOT IN ('COMPLETE','CANCELLED');
```

將 `CONNECTION_ID` 替換為 BigQuery 連線的 ID。

如果沒有 SQL 下推，系統會將下列查詢傳送至 Cloud SQL：

```
SELECT *
FROM operations_table
```

執行這項查詢時，即使只需要部分資料列和資料欄，系統仍會將整個資料表傳回 BigQuery。

使用 SQL 下推功能時，系統會將下列查詢傳送至 Cloud SQL：

```
SELECT `a`, `b`
FROM (
  SELECT * FROM operations_table) t
WHERE ((`a` = 'Y') AND (NOT `b` IN ('COMPLETE', 'CANCELLED')))
```

執行這項查詢時，系統只會將兩個資料欄和符合篩選條件的資料列傳回 BigQuery。

使用[Spanner 外部資料集](https://docs.cloud.google.com/bigquery/docs/spanner-external-datasets?hl=zh-tw)執行聯合查詢時，也會套用 SQL 下推。

您可以在[查詢計畫](https://docs.cloud.google.com/bigquery/docs/query-plan-explanation?hl=zh-tw#explanation_for_federated_queries)中檢查已套用的下推 (如有)。

### 限制

SQL 下推作業有各種限制，視外部資料來源和查詢資料的方式而異。

#### 使用 `EXTERNAL_QUERY` 時的查詢同盟限制

* SQL 下推僅適用於 `SELECT * FROM T` 形式的聯合查詢。
* 僅支援資料欄修剪和篩選條件下推。具體來說，系統不支援運算、聯結、限制、排序依據和彙整下推。
* 如要進行篩選器下推，常值必須是下列其中一種型別：`BOOL`、`INT64`、`FLOAT64`、`STRING`、`DATE`、`DATETIME`、`TIMESTAMP`。不支援結構體常值。
* 只有 BigQuery 和目標資料庫都支援的函式，才會套用 SQL 函式下推。
* SQL 下推僅支援 AlloyDB、Cloud SQL 和 Spanner。
* SAP Datasphere 不支援 SQL 下推。

#### 使用 Spanner 外部資料集時，查詢聯盟的限制

* 系統支援資料欄修剪、篩選、計算和部分匯總下推。具體來說，系統不支援聯結、限制和排序依據下推。
* 如要篩選條件下推，常值必須是下列其中一種型別：`BOOL`、`INT64`、`FLOAT64`、`STRING`、`DATE`、`DATETIME`、`TIMESTAMP`、`BYTE` 或陣列。不支援結構體常值。
* 只有 BigQuery 和 Spanner 都支援的函式，才會套用 SQL 函式下推。

### 各資料來源支援的函式

下表列出各資料來源支援的 SQL 函式。SAP Datasphere 不支援任何函式。

#### Cloud SQL MySQL

* **邏輯運算子：** `AND`、`OR`、`NOT`。
* **比較運算子：** `=`、`>`、`>=`、`<`、`<=`、`<>`、`IN`、`BETWEEN`、`IS NULL`。
* **算術運算子：** `+`、`-`、`*` (僅適用於 `INT64` 和 `FLOAT64`)。

#### Cloud SQL PostgreSQL 和 AlloyDB

* **邏輯運算子：** `AND`、`OR`、`NOT`。
* **比較運算子：** `=`、`>`、`>=`、`<`、`<=`、`<>`、`IN`、`BETWEEN`、`IS NULL`。
* **算術運算子：** `+`、`-`、`*`、`/` (僅適用於 `INT64`、`FLOAT64` 和 `DATE` 類型，但 `DATE` 減法除外)。

#### Spanner - PostgreSQL 方言

* **邏輯運算子：** `AND`、`OR`、`NOT`。
* **比較運算子：** `=`、`>`、`>=`、`<`、`<=`、`<>`、`IN`、`BETWEEN`、`IS NULL`。
* **算術運算子：** `+`、`-`、`*`、`/` (僅適用於 `INT64`、`FLOAT64`、`NUMERIC`)。
* 使用[外部資料集](https://docs.cloud.google.com/bigquery/docs/spanner-external-datasets?hl=zh-tw)時，請注意以下事項：

  + **運算**下推
  + **部分匯總**下推
  + **字串**函式
  + **數學**函式
  + **Cast**函式
  + **陣列**函式
* 執行查詢時，請預期會使用 GoogleSQL 語意，而非 PostgreSQL 語意。例如：

  + 預設會先按遞增順序排序 `NULL` 值，這與 PostgreSQL 不同，後者預設會將這些值排在最後。
  + 從 Spanner 讀取的 PostgreSQL `NUMERIC` 值會根據[從 Spanner 到 BigQuery 的類型對應](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/federated_query_functions?hl=zh-tw#spanner-mapping)處理。舉例來說，如果數值資料欄含有 `1.1234567891` 值，下列查詢會傳回 0 列：

    ```
    SELECT * FROM EXTERNAL_QUERY("CONNECTION_ID", "SELECT * from
    operations_table where numeric_col = 1.123456789")
    ```

    但根據 GoogleSQL 語意，下列陳述式會傳回 1 個資料列：

    ```
    SELECT * from operations_table where numeric_col = 1.123456789
    ```
  + JSON 物件正規化作業的行為不同。在 Spanner 中，鍵會依嚴格的字典順序排序 `JSON`，但在 PostgreSQL 中 `PG JSONB`，鍵會先依鍵長排序，然後依字典順序排序，鍵長相同的鍵則會依字典順序排序。

#### Spanner - GoogleSQL 方言

* **邏輯運算子：** `AND`、`OR`、`NOT`。
* **比較運算子：** `=`、`>`、`>=`、`<`、`<=`、`<>`、`IN`、`BETWEEN`、`IS NULL`。
* **算術運算子：** `+`、`-`、`*`、`/` (僅適用於 `INT64`、`FLOAT64`、`NUMERIC`)。
* **安全算術運算子：** `SAFE_ADD`、`SAFE_SUBTRACT`、`SAFE_MULTIPLY`、`SAFE_DIVIDE` (僅適用於 `INT64`、`FLOAT64`、`NUMERIC`)。
* 使用[外部資料集](https://docs.cloud.google.com/bigquery/docs/spanner-external-datasets?hl=zh-tw)時，請注意以下事項：
  + **運算**下推，
  + **Partial Aggregate** 下推，
  + **字串**函式，
  + **數學**函式
  + **Cast** 函式，
  + **陣列**函式。

## 處理外部資料來源中的對照順序

外部資料來源的資料欄可能設有排序規則集 (例如不區分大小寫)。執行聯合查詢時，遠端資料庫會考量已設定的排序規則。

請參考以下範例，其中外部資料來源的 `flag` 欄包含不區分大小寫的對照：

```
SELECT * FROM EXTERNAL_QUERY("CONNECTION_ID", "select * from operations_table where flag = 'Y'")
```

將 `CONNECTION_ID` 替換為 BigQuery 連線的 ID。

由於查詢是在外部資料來源上執行，因此上述查詢會傳回 `flag` 為 `y` 或 `Y` 的資料列。

不過，如果是與 Cloud SQL、SAP Datasphere 或 AlloyDB 資料來源的查詢聯合，如果您在主要查詢中新增篩選器，查詢會在 BigQuery 端執行，並使用預設的對照順序。請參閱以下查詢：

```
SELECT * FROM
  (
    SELECT * FROM EXTERNAL_QUERY("CONNECTION_ID", "select * from operations_table")
  )
WHERE flag = 'Y'
```

由於 BigQuery 預設會區分大小寫的[排序規則](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/collation-concepts?hl=zh-tw)，因此上述查詢只會傳回標記為 `Y` 的資料列，並篩除標記為 `y` 的資料列。如要讓 `WHERE` 子句不區分大小寫，請在查詢中指定排序規則：

```
SELECT * FROM
  (
    SELECT * FROM EXTERNAL_QUERY("CONNECTION_ID", "select * from operations_table")
  )
WHERE COLLATE(flag, 'und:ci') = 'Y'
```

## 後續步驟

* 瞭解如何[查詢 Spanner 資料](https://docs.cloud.google.com/bigquery/docs/spanner-federated-queries?hl=zh-tw)。
* 瞭解如何[建立 Spanner 外部資料集](https://docs.cloud.google.com/bigquery/docs/spanner-external-datasets?hl=zh-tw)。
* 瞭解如何[查詢 Cloud SQL 資料](https://docs.cloud.google.com/bigquery/docs/cloud-sql-federated-queries?hl=zh-tw)。
* 瞭解如何[查詢 AlloyDB 資料](https://docs.cloud.google.com/bigquery/docs/alloydb-federated-queries?hl=zh-tw)。
* 瞭解如何[查詢 SAP Datasphere 資料](https://docs.cloud.google.com/bigquery/docs/sap-datasphere-federated-queries?hl=zh-tw)




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-16 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-16 (世界標準時間)。"],[],[]]