Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 監控房源

本文說明如何在 BigQuery sharing (舊稱 Analytics Hub) 中監控項目。資料供應商可以追蹤房源的使用量指標。如要取得共用資料的使用情況指標，有以下兩種方法：

* [使用 BigQuery sharing](#use-analytics-hub)。你可以使用「分享」查看房源的使用指標資訊主頁。這個資訊主頁包含每日訂閱數、每日執行的工作數、每個機構的訂閱者人數，以及每個資料表的工作頻率。您可以查詢 `INFORMATION_SCHEMA.SHARED_DATASET_USAGE` 檢視表，擷取共用資料的用量指標。
* [使用 `INFORMATION_SCHEMA` 檢視畫面](#use-information-schema)。您可以查詢 `INFORMATION_SCHEMA.SHARED_DATASET_USAGE` 檢視畫面，追蹤訂閱者使用資料集的方式。

## 使用分享功能

如要使用「分享」功能取得共用資料的用量指標，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「Sharing (Analytics Hub)」頁面。

   [前往「共用」(Analytics Hub)](https://console.cloud.google.com/bigquery/analytics-hub?hl=zh-tw)
2. 按一下含有資源的[資料交換](https://docs.cloud.google.com/bigquery/docs/analytics-hub-introduction?hl=zh-tw#data_exchanges)名稱，即可查看使用指標。
3. 按一下「用量指標」，然後執行下列操作：

   1. 從「房源」選單中選取房源。
   2. 設定時間範圍。

這個頁面會顯示下列用量指標：

* **訂閱總數**：所選商品目前的訂閱數。最多可查看 60 天的總訂閱數。
* **訂閱總人數**：所選應用程式的所有訂閱方案不重複訂閱人數。最多可查看 60 天內的總訂閱人數。
* **執行的工作總數**：在所選項目各個資料表上執行的不重複工作數。
* **掃描的位元組總數**：從所選項目所有資料表掃描的位元組總數。
* **每日訂閱次數**：這張圖表會追蹤指定時間範圍內，所選房源的訂閱次數。最多可查看 60 天的每日訂閱資料。
* **每個機構的訂閱者人數**：列出機構和訂閱者人數，這些訂閱者會使用您選取的項目。
* **每日執行的工作**：這張圖表會顯示所選項目消耗的工作數。
* **資料表的工作頻率**：在所選商家資訊中存取資料表的頻率。

**注意：** 您也可以使用 [BigQuery sharing subscriber APIs](https://docs.cloud.google.com/bigquery/docs/reference/analytics-hub/rest/v1/projects.locations.subscriptions/list?hl=zh-tw) 擷取「總訂閱數」、「總訂閱者人數」和「每日訂閱數」欄位。

## 使用 `INFORMATION_SCHEMA` 檢視畫面

資料供應商可以查詢 [`INFORMATION_SCHEMA.SHARED_DATASET_USAGE` 檢視區塊](https://docs.cloud.google.com/bigquery/docs/information-schema-shared-dataset-usage?hl=zh-tw)，追蹤訂閱者使用資料集的情形。請確認您具備查詢這個檢視畫面的必要角色。

如要對預設專案以外的 Google Cloud 專案執行查詢，請使用下列格式：

```
PROJECT_ID.region-REGION_NAME.INFORMATION_SCHEMA.SHARED_DATASET_USAGE
```

更改下列內容：

* `PROJECT_ID`： Google Cloud 專案 ID
* `REGION_NAME`：BigQuery 資料集
  區域名稱

例如 `myproject.region-us.INFORMATION_SCHEMA.SHARED_DATASET_USAGE`。

下列範例說明如何查詢 `INFORMATION_SCHEMA` 檢視區塊，查看使用量指標。

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

## 後續步驟

* 瞭解如何[管理 BigQuery sharing 清單](https://docs.cloud.google.com/bigquery/docs/analytics-hub-manage-listings?hl=zh-tw)。
* 瞭解 [BigQuery 計價方式](https://cloud.google.com/bigquery/pricing?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-06 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-06 (世界標準時間)。"],[],[]]