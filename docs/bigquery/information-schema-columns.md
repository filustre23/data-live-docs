Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [參考資料](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 「COLUMNS」檢視畫面

`INFORMATION_SCHEMA.COLUMNS` 檢視表會針對資料表中的每個資料欄 (欄位)，分別列出一個相對應的資料列。

## 所需權限

如要查詢 `INFORMATION_SCHEMA.COLUMNS` 檢視畫面，您必須具備下列 Identity and Access Management (IAM) 權限：

* `bigquery.tables.get`
* `bigquery.tables.list`

下列每個預先定義的 IAM 角色都包含上述權限：

* `roles/bigquery.admin`
* `roles/bigquery.dataViewer`
* `roles/bigquery.dataEditor`
* `roles/bigquery.metadataViewer`

如要進一步瞭解 BigQuery 權限，請參閱「[使用 IAM 控管存取權](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)」。

## 結構定義

當您查詢 `INFORMATION_SCHEMA.COLUMNS` 檢視表時，系統會在查詢結果中，針對資料集中的每個資料欄 (欄位)，分別列出一個相對應的資料列。

`INFORMATION_SCHEMA.COLUMNS` 檢視表具有下列結構定義：

| 資料欄名稱 | 資料類型 | 值 |
| --- | --- | --- |
| `table_catalog` | `STRING` | 資料集所屬專案的專案 ID。 |
| `table_schema` | `STRING` | 資料表所屬資料集的名稱 (又稱為 `datasetId`)。 |
| `table_name` | `STRING` | 資料表或檢視表的名稱 (又稱為 `tableId`)。 |
| `column_name` | `STRING` | 資料欄的名稱。 |
| `ordinal_position` | `INT64` | 資料表中資料欄的 1 索引偏移；如果是虛擬資料欄 (例如 \_PARTITIONTIME 或 \_PARTITIONDATE)，則值為 `NULL`。 |
| `is_nullable` | `STRING` | `YES` 或 `NO`，視資料欄的模式是否允許使用 `NULL` 值而定。 |
| `data_type` | `STRING` | 資料欄的 GoogleSQL [資料類型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw)。 |
| `is_generated` | `STRING` | 如果資料欄是[自動產生的嵌入資料欄](https://docs.cloud.google.com/bigquery/docs/autonomous-embedding-generation?hl=zh-tw)，值為 `ALWAYS`；否則值為 `NEVER`。 |
| `generation_expression` | `STRING` | 如果資料欄是自動產生的嵌入資料欄，這個值就是用於定義資料欄的生成運算式；否則這個值為 `NULL`。 |
| `is_stored` | `STRING` | 如果資料欄是自動產生的嵌入資料欄，值為 `YES`；否則值為 `NULL`。 |
| `is_hidden` | `STRING` | `YES` 或 `NO`，視資料欄是否為虛擬資料欄 (例如 \_PARTITIONTIME 或 \_PARTITIONDATE) 而定。 |
| `is_updatable` | `STRING` | 此值一律為 `NULL`。 |
| `is_system_defined` | `STRING` | `YES` 或 `NO`，視資料欄是否為虛擬資料欄 (例如 \_PARTITIONTIME 或 \_PARTITIONDATE) 而定。 |
| `is_partitioning_column` | `STRING` | `YES` 或 `NO`，視資料欄是否為[分區資料欄](https://docs.cloud.google.com/bigquery/docs/partitioned-tables?hl=zh-tw)而定。 |
| `clustering_ordinal_position` | `INT64` | 在資料表的叢集資料欄中，資料欄的 1 索引偏移。如果資料表不是叢集資料表，則此值為 `NULL`。 |
| `collation_name` | `STRING` | [排序規則規格](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/collation-concepts?hl=zh-tw)的名稱 (如有)，否則為 `NULL`。   如果傳入 `STRING` 或 `ARRAY<STRING>`，則會傳回排序規則規格 (如有)，否則會傳回 `NULL`。 |
| `column_default` | `STRING` | 如果資料欄存在，則為該資料欄的[預設值](https://docs.cloud.google.com/bigquery/docs/default-values?hl=zh-tw)；否則值為 `NULL`。 |
| `rounding_mode` | `STRING` | 如果欄位類型是參數化 `NUMERIC` 或 `BIGNUMERIC`，則寫入欄位的值會使用此捨入模式；否則值為 `NULL`。 |
| `data_policies.name` | `STRING` | 附加至資料欄的資料政策清單，用於控管存取權和遮蓋。這個欄位為 ([預先發布版](https://cloud.google.com/products?hl=zh-tw#product-launch-stages))。 |
| `policy_tags` | `ARRAY<STRING>` | 附加至資料欄的政策標記清單。 |

為確保穩定性，建議您在資訊結構定義查詢中明確列出資料欄，而非使用萬用字元 (`SELECT *`)。明確列出資料欄可避免基礎結構定義變更時，查詢中斷。

## 範圍和語法

對這個檢視表執行的查詢必須包含資料集或區域限定詞。如果是含有資料集限定符的查詢，您必須具備該資料集的權限。如要查詢含有區域限定符的資料，您必須具備專案權限。詳情請參閱「[語法](https://docs.cloud.google.com/bigquery/docs/information-schema-intro?hl=zh-tw#syntax)」。下表說明這個檢視畫面的區域和資源範圍：

| 檢視表名稱 | 資源範圍 | 區域範圍 |
| --- | --- | --- |
| `` [PROJECT_ID.]`region-REGION`.INFORMATION_SCHEMA.COLUMNS `` | 專案層級 | `REGION` |
| `[PROJECT_ID.]DATASET_ID.INFORMATION_SCHEMA.COLUMNS` | 資料集層級 | 資料集位置 |

取代下列項目：

* 選用：`PROJECT_ID`：您的 Google Cloud 專案 ID。如未指定，系統會使用預設專案。
* `REGION`：任何[資料集區域名稱](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)。
  例如：`` `region-us` ``。
* `DATASET_ID`：資料集 ID。詳情請參閱「[資料集限定符](https://docs.cloud.google.com/bigquery/docs/information-schema-intro?hl=zh-tw#dataset_qualifier)」。**注意：**您必須使用[區域限定詞](https://docs.cloud.google.com/bigquery/docs/information-schema-intro?hl=zh-tw#region_qualifier)查詢 `INFORMATION_SCHEMA` 檢視畫面。查詢執行位置必須與 `INFORMATION_SCHEMA` 檢視區塊的區域相符。

## 範例

以下範例會從 [`census_bureau_usa`](https://console.cloud.google.com/bigquery?p=bigquery-public-data&%3Bd=census_bureau_usa&%3Bpage=dataset&hl=zh-tw) 資料集中的 `population_by_zip_2010` 資料表，擷取 `INFORMATION_SCHEMA.COLUMNS` 檢視表的中繼資料。這個資料集是 BigQuery [公開資料集方案](https://cloud.google.com/public-datasets/?hl=zh-tw)的一部分。

由於您要查詢的資料表位於另一個專案 (`bigquery-public-data`) 中，因此您應使用以下格式將專案 ID 新增至資料集：`` `project_id`.dataset.INFORMATION_SCHEMA.view ``；例如 `` `bigquery-public-data`.census_bureau_usa.INFORMATION_SCHEMA.TABLES ``。

查詢結果會排除下列資料欄：

* `IS_UPDATABLE`

**注意：** `INFORMATION_SCHEMA` 檢視表名稱會區分大小寫。

```
  SELECT
    * EXCEPT(is_updatable)
  FROM
    `bigquery-public-data`.census_bureau_usa.INFORMATION_SCHEMA.COLUMNS
  WHERE
    table_name = 'population_by_zip_2010';
```

結果大致如下。為了方便閱讀，部分資料欄已從結果中排除。

```
+------------------------+-------------+------------------+-------------+-----------+-----------+-------------------+------------------------+-----------------------------+-------------+
|       table_name       | column_name | ordinal_position | is_nullable | data_type | is_hidden | is_system_defined | is_partitioning_column | clustering_ordinal_position | policy_tags |
+------------------------+-------------+------------------+-------------+-----------+-----------+-------------------+------------------------+-----------------------------+-------------+
| population_by_zip_2010 | zipcode     |                1 | NO          | STRING    | NO        | NO                | NO                     |                        NULL | 0 rows      |
| population_by_zip_2010 | geo_id      |                2 | YES         | STRING    | NO        | NO                | NO                     |                        NULL | 0 rows      |
| population_by_zip_2010 | minimum_age |                3 | YES         | INT64     | NO        | NO                | NO                     |                        NULL | 0 rows      |
| population_by_zip_2010 | maximum_age |                4 | YES         | INT64     | NO        | NO                | NO                     |                        NULL | 0 rows      |
| population_by_zip_2010 | gender      |                5 | YES         | STRING    | NO        | NO                | NO                     |                        NULL | 0 rows      |
| population_by_zip_2010 | population  |                6 | YES         | INT64     | NO        | NO                | NO                     |                        NULL | 0 rows      |
+------------------------+-------------+------------------+-------------+-----------+-----------+-------------------+------------------------+-----------------------------+-------------+
```




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-09 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-09 (世界標準時間)。"],[],[]]