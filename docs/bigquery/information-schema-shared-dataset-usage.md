* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [參考資料](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# INFORMATION\_SCHEMA.SHARED\_DATASET\_USAGE 檢視區塊

`INFORMATION_SCHEMA.SHARED_DATASET_USAGE` 檢視畫面包含共用資料集資料表用量的近乎即時中繼資料。如要開始跨機構共用資料，請參閱「[BigQuery sharing (舊稱 Analytics Hub)](https://docs.cloud.google.com/bigquery/docs/analytics-hub-introduction?hl=zh-tw)」。

## 必要的角色

如要取得查詢 `INFORMATION_SCHEMA.SHARED_DATASET_USAGE` 檢視畫面所需的權限，請要求系統管理員授予您來源專案的「[BigQuery 資料擁有者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.dataOwner) 」(`roles/bigquery.dataOwner`) IAM 角色。如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和機構的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

這個預先定義的角色具備  `bigquery.datasets.listSharedDatasetUsage` 權限，可查詢 `INFORMATION_SCHEMA.SHARED_DATASET_USAGE` 檢視畫面。

您或許還可透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)取得這項權限。

## 結構定義

基礎資料依 `job_start_time` 資料欄分區，並依 `project_id` 和 `dataset_id` 分群。

`INFORMATION_SCHEMA.SHARED_DATASET_USAGE` 具有下列結構定義：

| **資料欄名稱** | **資料類型** | **值** |
| --- | --- | --- |
| `project_id` | `STRING` | **(*叢集資料欄*)** 包含共用資料集的專案 ID。 |
| `dataset_id` | `STRING` | **(*叢集資料欄*)** 共用資料集的 ID。 |
| `table_id` | `STRING` | 所存取資料表的 ID。 |
| `data_exchange_id` | `STRING` | 資料交換的資源路徑。 |
| `listing_id` | `STRING` | 房源的資源路徑。 |
| `job_start_time` | `TIMESTAMP` | **(*分區資料欄*)** 這項工作的開始時間。 |
| `job_end_time` | `TIMESTAMP` | 這項工作的結束時間。 |
| `job_id` | `STRING` | 工作 ID。例如 **bquxjob\_1234**。 |
| `job_project_number` | `INTEGER` | 這項工作所屬的專案編號。 |
| `job_location` | `STRING` | 工作地點。 |
| `linked_project_number` | `INTEGER` | 訂閱者專案的專案編號。 |
| `linked_dataset_id` | `STRING` | 訂閱者資料集的連結資料集 ID。 |
| `subscriber_org_number` | `INTEGER` | 執行工作的機構編號。這是訂閱者的機構號碼。如果專案沒有機構，這個欄位會空白。 |
| `subscriber_org_display_name` | `STRING` | 使用者容易理解的字串，是指工作執行的機構。這是訂閱者的機構號碼。如果專案沒有機構，這個欄位會空白。 |
| `job_principal_subject` | `STRING` | 對連結資料集執行作業和查詢的使用者主體 ID (使用者電子郵件 ID、服務帳戶、群組電子郵件 ID、網域)。 |
| `num_rows_processed` | `INTEGER` | 查詢資源參照的基礎資料表所處理的總列數。 |
| `total_bytes_processed` | `INTEGER` | 查詢的資源所參照的基礎資料表處理的位元組總數。 |
| `shared_resource_id` | `STRING` | 所查詢資源 (資料表、檢視區塊或常式) 的 ID。 |
| `shared_resource_type` | `STRING` | 查詢資源的類型。例如：`TABLE`、`EXTERNAL_TABLE`、`VIEW`、`MATERIALIZED_VIEW`、`TABLE_VALUED_FUNCTION` 或 `SCALAR_FUNCTION`。 |
| `referenced_tables` | `RECORD REPEATED` | 包含基本資料表的 `project_id`、`dataset_id`、`table_id` 和 `processed_bytes` 欄位。 |

為確保穩定性，建議您在資訊結構定義查詢中明確列出資料欄，而非使用萬用字元 (`SELECT *`)。明確列出資料欄可避免基礎結構定義變更時，查詢中斷。

## 資料保留

`INFORMATION_SCHEMA.SHARED_DATASET_USAGE` 檢視畫面會顯示執行中的工作，以及過去 180 天的工作記錄。

## 範圍和語法

對這個檢視表執行的查詢必須包含[區域限定詞](https://docs.cloud.google.com/bigquery/docs/information-schema-intro?hl=zh-tw#syntax)。如未指定區域限定符，系統會從美國地區擷取中繼資料。下表說明這個檢視畫面的區域範圍：

| 檢視表名稱 | 資源範圍 | 區域範圍 |
| --- | --- | --- |
| `[PROJECT_ID.]INFORMATION_SCHEMA.SHARED_DATASET_USAGE` | 專案層級 | 美國區域 |
| `` [PROJECT_ID.]`region-REGION`.INFORMATION_SCHEMA.SHARED_DATASET_USAGE `` | 專案層級 | `REGION` |

取代下列項目：

* 選用：`PROJECT_ID`：專案 ID。 Google Cloud 如未指定，系統會使用預設專案。
* `REGION`：任何[資料集區域名稱](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)。
  例如：`` `region-us` ``。**注意：**您必須使用[區域限定詞](https://docs.cloud.google.com/bigquery/docs/information-schema-intro?hl=zh-tw#region_qualifier)查詢 `INFORMATION_SCHEMA` 檢視畫面。查詢執行位置必須與`INFORMATION_SCHEMA`檢視區塊的區域相符。

## 範例

如要對預設專案以外的專案執行查詢，請使用以下格式新增專案 ID：

`PROJECT_ID.region-REGION_NAME.INFORMATION_SCHEMA.SHARED_DATASET_USAGE`

例如 `myproject.region-us.INFORMATION_SCHEMA.SHARED_DATASET_USAGE`。

### 取得所有共用資料表上執行的工作總數

以下範例會計算專案中[訂閱者](https://docs.cloud.google.com/bigquery/docs/analytics-hub-view-subscribe-listings?hl=zh-tw)執行的工作總數：

```
SELECT
  COUNT(DISTINCT job_id) AS num_jobs
FROM
  `region-us`.INFORMATION_SCHEMA.SHARED_DATASET_USAGE
```

結果大致如下：

```
+------------+
| num_jobs   |
+------------+
| 1000       |
+------------+
```

如要檢查訂閱者執行的工作總數，請使用 `WHERE` 子句：

* 如果是資料集，請使用 `WHERE dataset_id = "..."`。
* 表格請使用 `WHERE dataset_id = "..." AND table_id = "..."`。

### 根據處理的列數取得最常使用的資料表

下列查詢會根據訂閱者處理的資料列數，計算最常使用的資料表。

```
SELECT
  dataset_id,
  table_id,
  SUM(num_rows_processed) AS usage_rows
FROM
  `region-us`.INFORMATION_SCHEMA.SHARED_DATASET_USAGE
GROUP BY
  1,
  2
ORDER BY
  3 DESC
LIMIT
  1
```

輸出結果會與下列內容相似：

```
+---------------+-------------+----------------+
| dataset_id    | table_id      | usage_rows     |
+---------------+-------------+----------------+
| mydataset     | mytable     | 15             |
+---------------+-------------+----------------+
```

### 找出最常使用資料表的機構

下列查詢會根據資料表處理的位元組數，計算出最常使用的訂閱者。您也可以將 `num_rows_processed` 資料欄做為指標。

```
SELECT
  subscriber_org_number,
  ANY_VALUE(subscriber_org_display_name) AS subscriber_org_display_name,
  SUM(total_bytes_processed) AS usage_bytes
FROM
  `region-us`.INFORMATION_SCHEMA.SHARED_DATASET_USAGE
GROUP BY
  1
```

輸出結果會與下列內容相似：

```
+--------------------------+--------------------------------+----------------+
|subscriber_org_number     | subscriber_org_display_name    | usage_bytes    |
+-----------------------------------------------------------+----------------+
| 12345                    | myorganization                 | 15             |
+--------------------------+--------------------------------+----------------+
```

如果訂閱者沒有機構，可以使用 `job_project_number`，
而非 `subscriber_org_number`。

### 取得資料交換的使用情況指標

如果[資料交換庫](https://docs.cloud.google.com/bigquery/docs/analytics-hub-introduction?hl=zh-tw#data_exchanges)和來源資料集位於不同專案，請按照下列步驟查看資料交換庫的使用情況指標：

1. 找出資料交換庫的所有[刊登資訊](https://docs.cloud.google.com/bigquery/docs/analytics-hub-introduction?hl=zh-tw#listings)。
2. 擷取附加至房源資訊的來源資料集。
3. 如要查看資料交換庫的用量指標，請使用下列查詢：

```
SELECT
  *
FROM
  source_project_1.`region-us`.INFORMATION_SCHEMA.SHARED_DATASET_USAGE
WHERE
  dataset_id='source_dataset_id'
AND data_exchange_id="projects/4/locations/us/dataExchanges/x1"
UNION ALL
SELECT
  *
FROM
  source_project_2.`region-us`.INFORMATION_SCHEMA.SHARED_DATASET_USAGE
WHERE
  dataset_id='source_dataset_id'
AND data_exchange_id="projects/4/locations/us/dataExchanges/x1"
```

### 取得共用檢視畫面的用量指標

下列查詢會顯示專案中所有共用檢視區塊的用量指標：

```
SELECT
  project_id,
  dataset_id,
  table_id,
  num_rows_processed,
  total_bytes_processed,
  shared_resource_id,
  shared_resource_type,
  referenced_tables
FROM `myproject`.`region-us`.INFORMATION_SCHEMA.SHARED_DATASET_USAGE
WHERE shared_resource_type = 'VIEW'
```

輸出結果會與下列內容相似：

```
+---------------------+----------------+----------+--------------------+-----------------------+--------------------+----------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
|     project_id      |   dataset_id   | table_id | num_rows_processed | total_bytes_processed | shared_resource_id | shared_resource_type |                                                                                                              referenced_tables                                                                                                              |
+---------------------+----------------+----------+--------------------+-----------------------+--------------------+----------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
|     myproject       | source_dataset | view1    |                  6 |                    38 | view1              | VIEW                 | [{"project_id":"myproject","dataset_id":"source_dataset","table_id":"test_table","processed_bytes":"21"},
{"project_id":"bq-dataexchange-exp","dataset_id":"other_dataset","table_id":"other_table","processed_bytes":"17"}]                 |

+---------------------+----------------+----------+--------------------+-----------------------+--------------------+----------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
```

### 取得共用資料表值函式的用量指標

下列查詢會顯示專案中所有共用資料表值函式的用量指標：

```
SELECT
  project_id,
  dataset_id,
  table_id,
  num_rows_processed,
  total_bytes_processed,
  shared_resource_id,
  shared_resource_type,
  referenced_tables
FROM `myproject`.`region-us`.INFORMATION_SCHEMA.SHARED_DATASET_USAGE
WHERE shared_resource_type = 'TABLE_VALUED_FUNCTION'
```

輸出結果會與下列內容相似：

```
+---------------------+----------------+----------+--------------------+-----------------------+--------------------+-----------------------+---------------------------------------------------------------------------------------------------------------------+
|     project_id      |   dataset_id   | table_id | num_rows_processed | total_bytes_processed | shared_resource_id | shared_resource_type  |                                                  referenced_tables                                                  |
+---------------------+----------------+----------+--------------------+-----------------------+--------------------+-----------------------+---------------------------------------------------------------------------------------------------------------------+
|     myproject       | source_dataset |          |                  3 |                    45 | provider_exp       | TABLE_VALUED_FUNCTION | [{"project_id":"myproject","dataset_id":"source_dataset","table_id":"test_table","processed_bytes":"45"}]           |
+---------------------+----------------+----------+--------------------+-----------------------+--------------------+-----------------------+---------------------------------------------------------------------------------------------------------------------+
```




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-02 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-02 (世界標準時間)。"],[],[]]