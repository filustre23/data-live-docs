Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 根據記錄進行最佳化

本指南說明如何啟用、停用及分析查詢的記錄式最佳化功能。

## 關於根據記錄進行最佳化

以記錄為準的最佳化功能會使用類似查詢已完成執行的資訊，套用額外的最佳化設定，進一步提升查詢效能，例如消耗的時段時間和查詢延遲。舉例來說，套用以記錄為準的最佳化功能時，第一次執行查詢可能需要 60 秒，但如果系統識別出以記錄為準的最佳化功能，第二次執行查詢可能只需要 30 秒。這個程序會持續進行，直到沒有其他最佳化項目可新增為止。

以下舉例說明如何透過 BigQuery 進行歷史記錄最佳化：

| 執行次數 | 查詢耗用的運算單元時間 | 附註 |
| --- | --- | --- |
| 1 | 60 | 原始執行作業。 |
| 2 | 30 | 首次套用以記錄為依據的最佳化設定。 |
| 3 | 20 | 套用第二個以記錄為依據的最佳化設定。 |
| 4 | 21 | 沒有其他可套用的記錄最佳化設定。 |
| 5 | 19 | 沒有其他可套用的記錄最佳化設定。 |
| 6 | 20 | 沒有其他可套用的記錄最佳化設定。 |

只有在確信可提升查詢成效時，系統才會套用以記錄為依據的最佳化設定。此外，如果最佳化作業無法大幅提升查詢效能，系統就會撤銷該最佳化作業，且日後不會再用於該查詢的執行作業。

## 角色和權限

* 如要啟用或停用以記錄為準的最佳化功能，您必須具備建立 BigQuery 預設設定的必要權限，然後使用 `ALTER PROJECT` 陳述式啟用以記錄為準的最佳化功能。啟用以記錄為準的最佳化功能後，無論是哪位使用者建立的工作，該專案中的所有工作都會採用這項功能。如要進一步瞭解預設設定所需的角色和權限，請參閱「[預設設定所需的角色](https://docs.cloud.google.com/bigquery/docs/default-configuration?hl=zh-tw#required_permissions)」一文。如要啟用以記錄為準的最佳化功能，請參閱「[啟用以記錄為準的最佳化功能](#enable-history-based-optimization)」。
* 如要使用 `INFORMATION_SCHEMA.JOBS` 檢視畫面查看作業的歷史記錄最佳化，您必須具備必要角色。詳情請參閱「[查看 `INFORMATION_SCHEMA.JOBS` 檢視畫面所需的角色](https://docs.cloud.google.com/bigquery/docs/information-schema-jobs?hl=zh-tw#required_role)」。

## 啟用以記錄為準的最佳化功能

系統預設會啟用以記錄為依據的最佳化功能。如果專案或機構已停用以記錄為準的最佳化功能，您可以在 [`ALTER PROJECT`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#alter_project_set_options_statement) 或 [`ALTER ORGANIZATION`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#alter_organization_set_options_statement) 陳述式中加入 `default_query_optimizer_options = 'adaptive=on'` 參數，手動重新啟用以記錄為準的最佳化功能。例如：

```
ALTER PROJECT PROJECT_NAME
SET OPTIONS (
  `region-LOCATION.default_query_optimizer_options` = 'adaptive=on'
);
```

更改下列內容：

* `PROJECT_NAME`：專案名稱
* `LOCATION`：作業應嘗試使用以記錄為準的最佳化功能的位置

**注意：** 啟用以記錄為準的最佳化功能後，如果看到以下警示訊息，請放心忽略。只要有任何 `ALTER PROJECT` 或 `ALTER ORGANIZATION` 陳述式成功執行，就會顯示這則訊息：
`ALTER PROJECT succeeded. Please make sure no existing queries depend on the
old defaults (such as the default time zone) or else these queries will be
broken.`

## 停用以記錄為準的最佳化功能

如要在專案中停用以記錄為準的最佳化功能，請在 [`ALTER PROJECT`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#alter_project_set_options_statement) 或 [`ALTER ORGANIZATION`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#alter_organization_set_options_statement) 陳述式中加入 `default_query_optimizer_options = 'adaptive=off'` 參數。例如：

```
ALTER PROJECT PROJECT_NAME
SET OPTIONS (
  `region-LOCATION.default_query_optimizer_options` = 'adaptive=off'
);
```

更改下列內容：

* `PROJECT_NAME`：專案名稱
* `LOCATION`：工作不應嘗試使用以記錄為依據的最佳化功能的位置

**注意：** 停用以記錄為準的最佳化功能後，如果看到以下警示訊息，請放心忽略。只要有任何 `ALTER PROJECT` 或 `ALTER ORGANIZATION` 陳述式成功執行，就會顯示這則訊息：
`ALTER PROJECT succeeded. Please make sure no existing queries depend on the
old defaults (such as the default time zone) or else these queries will be
broken.`

## 查看作業的歷史記錄最佳化項目

如要查看作業的歷史記錄最佳化結果，可以使用 SQL 查詢或 REST API 方法呼叫。

### SQL

您可以使用查詢，取得作業的歷史記錄最佳化結果。
查詢必須包含 [`INFORMATION_SCHEMA.JOBS_BY_PROJECT`](https://docs.cloud.google.com/bigquery/docs/information-schema-jobs?hl=zh-tw#schema) 和 `query_info.optimization_details` 資料欄名稱。

在下列範例中，系統會傳回名為 `sample_job` 的工作最佳化詳細資料。如果沒有套用任何以記錄為依據的最佳化設定，系統會為 `optimization_details` 產生 `NULL`：

```
SELECT
  job_id,
  query_info.optimization_details
FROM `PROJECT_NAME.region-LOCATION`.INFORMATION_SCHEMA.JOBS_BY_PROJECT
WHERE job_id = 'sample_job'
LIMIT 1;
```

結果類似下方：

```
-- The JSON in optimization_details has been formatted for readability.
/*------------+-----------------------------------------------------------------*
 | job_id     | optimization_details                                            |
 +------------+-----------------------------------------------------------------+
 | sample_job | {                                                               |
 |            |   "optimizations": [                                            |
 |            |     {                                                           |
 |            |       "semi_join_reduction": "web_sales.web_date,RIGHT"         |
 |            |     },                                                          |
 |            |     {                                                           |
 |            |       "semi_join_reduction": "catalog_sales.catalog_date,RIGHT" |
 |            |     },                                                          |
 |            |     {                                                           |
 |            |       "semi_join_reduction": "store_sales.store_date,RIGHT"     |
 |            |     },
 |            |     {                                                           |
 |            |       "join_commutation": "web_returns.web_item"                |
 |            |     },
 |            |     {                                                           |
 |            |       "parallelism_adjustment": "applied"                       |
 |            |     },
 |            |   ]                                                             |
 |            | }                                                               |
 *------------+-----------------------------------------------------------------*/
```

### API

如要取得工作的最佳化詳細資料，可以呼叫 [`jobs.get` 方法](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs/get?hl=zh-tw)。

在下列範例中，`jobs.get` 方法會在完整回應中傳回最佳化詳細資料 ([`optimizationDetails`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#queryinfo))：

```
{
  "jobReference": {
    "projectId": "myProject",
    "jobId": "sample_job"
  }
}
```

結果類似下方：

```
-- The unrelated parts in the full response have been removed.
{
  "jobReference": {
    "projectId": "myProject",
    "jobId": "sample_job",
    "location": "US"
  },
  "statistics": {
    "query": {
      "queryInfo": {
        "optimizationDetails": {
          "optimizations": [
            {
              "semi_join_reduction": "web_sales.web_date,RIGHT"
            },
            {
              "semi_join_reduction": "catalog_sales.catalog_date,RIGHT"
            },
            {
              "semi_join_reduction": "store_sales.store_date,RIGHT"
            },
            {
              "join_commutation": "web_returns.web_item"
            },
            {
              "parallelism_adjustment": "applied"
            }
          ]
        }
      }
    }
  }
}
```

## 預估根據記錄進行最佳化的影響

如要估算根據記錄進行最佳化的影響，可以使用下列 SQL 查詢範例，找出預估執行時間改善幅度最大的專案查詢。

```
  WITH
    jobs AS (
      SELECT
        *,
        query_info.query_hashes.normalized_literals AS query_hash,
        TIMESTAMP_DIFF(end_time, start_time, MILLISECOND) AS elapsed_ms,
        IFNULL(
          ARRAY_LENGTH(JSON_QUERY_ARRAY(query_info.optimization_details.optimizations)) > 0,
          FALSE)
          AS has_history_based_optimization,
      FROM region-LOCATION.INFORMATION_SCHEMA.JOBS_BY_PROJECT
      WHERE EXTRACT(DATE FROM creation_time) > DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)
    ),
    most_recent_jobs_without_history_based_optimizations AS (
      SELECT *
      FROM jobs
      WHERE NOT has_history_based_optimization
      QUALIFY ROW_NUMBER() OVER (PARTITION BY query_hash ORDER BY end_time DESC) = 1
    )
  SELECT
    job.job_id,
    100 * SAFE_DIVIDE(
      original_job.elapsed_ms - job.elapsed_ms,
      original_job.elapsed_ms) AS percent_execution_time_saved,
    job.elapsed_ms AS new_elapsed_ms,
    original_job.elapsed_ms AS original_elapsed_ms,
  FROM jobs AS job
  INNER JOIN most_recent_jobs_without_history_based_optimizations AS original_job
    USING (query_hash)
  WHERE
    job.has_history_based_optimization
    AND original_job.end_time < job.start_time
  ORDER BY percent_execution_time_saved DESC
  LIMIT 10;
```

如果套用以記錄為準的最佳化，上述查詢的結果會類似於下列內容：

```
  /*--------------+------------------------------+------------------+-----------------------*
   |    job_id    | percent_execution_time_saved | new_execution_ms | original_execution_ms |
   +--------------+------------------------------+------------------+-----------------------+
   | sample_job1  |           67.806850186245114 |             7087 |                 22014 |
   | sample_job2  |           66.485800412501987 |            10562 |                 31515 |
   | sample_job3  |           63.285605271764254 |            97668 |                266021 |
   | sample_job4  |           61.134141726887904 |           923384 |               2375823 |
   | sample_job5  |           55.381272089713754 |          1060062 |               2375823 |
   | sample_job6  |           45.396943168036479 |          2324071 |               4256302 |
   | sample_job7  |           38.227031526376024 |            17811 |                 28833 |
   | sample_job8  |           33.826608962725111 |            66360 |                100282 |
   | sample_job9  |           32.087813758311604 |            44020 |                 64819 |
   | sample_job10 |           28.356416319483539 |            19088 |                 26643 |
   *--------------+------------------------------+------------------+-----------------------*/
```

這項查詢的結果僅為根據記錄進行最佳化的影響預估值。影響查詢效能的因素有很多，包括但不限於可用時段、資料隨時間的變化、檢視區塊或 UDF 定義，以及查詢參數值的差異。

如果這項範例查詢的結果為空白，表示沒有任何工作使用過以記錄為準的最佳化功能，或是所有查詢都是在 30 天前完成最佳化。

這項查詢可套用至其他查詢效能指標，例如 `total_slot_ms` 和 `total_bytes_billed`。詳情請參閱 [`INFORMATION_SCHEMA.JOBS`](https://docs.cloud.google.com/bigquery/docs/information-schema-jobs?hl=zh-tw#schema) 的結構定義。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-16 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-16 (世界標準時間)。"],[],[]]