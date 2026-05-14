Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 監控 BI Engine

[BigQuery BI Engine](https://docs.cloud.google.com/bigquery/docs/bi-engine-intro?hl=zh-tw) 會使用記憶體快取和更快的執行速度，加速處理 BI 情境的 BigQuery。您可以使用 [INFORMATION\_SCHEMA](https://docs.cloud.google.com/bigquery/docs/information-schema-jobs?hl=zh-tw) 和 [Cloud Monitoring 指標](https://docs.cloud.google.com/bigquery/docs/monitoring?hl=zh-tw)監控加速詳細資料。

## Cloud Monitoring

您可以使用 Cloud Monitoring 監控 BigQuery BI Engine，並設定相關快訊。如要瞭解如何建立 BI Engine 指標的資訊主頁，請參閱「[建立圖表](https://docs.cloud.google.com/monitoring/charts?hl=zh-tw)」。

BigQuery BI Engine 提供下列指標：

| 資源 | 指標 | 詳細資料 |
| --- | --- | --- |
| BigQuery 專案 | 預留容量總計 (位元組) | 分配給單一 Google Cloud 專案的總容量 |
| BigQuery 專案 | 已使用的預留位元組數 | 單一 Google Cloud 專案使用的總容量 |
| BigQuery 專案 | BI Engine 快取位元組數最多的資料表 | 每個資料表的快取用量。這項指標會顯示各區域報表用量前 *N* 名的資料表。 |

## BI Engine 的查詢統計資料

本節說明如何找出查詢統計資料，以利監控、診斷及排解 BI Engine 使用問題。

### BI Engine 加速模式

啟用 BI Engine 加速功能後，查詢可以下列四種模式執行：

|  |  |
| --- | --- |
| ``` BI_ENGINE_DISABLED ``` | BI Engine 已停用加速功能。 `biEngineReasons` 會指定更詳細的原因。查詢是使用 BigQuery 執行引擎執行的。 |
| ``` PARTIAL_INPUT ``` | 查詢輸入的部分內容已使用 BI Engine 加速處理。如「[查詢最佳化和加速](https://docs.cloud.google.com/bigquery/docs/bi-engine-query?hl=zh-tw#query_optimization_and_acceleration)」一文所述，查詢計畫通常會細分為多個輸入階段。BI Engine 支援一般類型的子查詢模式，通常用於資訊主頁。如果查詢包含多個輸入階段，但只有少數階段屬於支援的用途，BI Engine 會使用一般 BigQuery 引擎執行不支援的階段，不會加速處理。在這種情況下，BI Engine 會傳回 `PARTIAL` 加速代碼，並使用 `biEngineReasons` 填入未加速其他輸入階段的原因。 |
| ```  FULL_INPUT ``` | 查詢的所有輸入階段都使用 BI Engine 加速處理。快取資料會在查詢中重複使用，且讀取資料後立即進行的運算作業會加速。 |
| ```  FULL_QUERY ``` | 整個查詢都使用 BI Engine 加速。 |

### 查看 BigQuery API 工作統計資料

您可以透過 BigQuery API 取得 BI Engine 的詳細統計資料。

如要擷取與 BI Engine 加速查詢相關聯的統計資料，請執行下列 bq 指令列工具指令：

```
bq show --format=prettyjson -j job_id
```

如果專案已啟用 BI Engine 加速功能，輸出內容會產生新的欄位 `biEngineStatistics`。以下是工作報告範例：

```
 "statistics": {
    "creationTime": "1602175128902",
    "endTime": "1602175130700",
    "query": {
      "biEngineStatistics": {
        "biEngineMode": "DISABLED",
        "biEngineReasons": [
          {
            "code": "UNSUPPORTED_SQL_TEXT",
            "message": "Detected unsupported join type"
          }
        ]
      },
```

如要進一步瞭解 `BiEngineStatistics` 欄位，請參閱[工作參考資料](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#bienginestatistics)。

### BigQuery 資訊結構定義統計資料

BI Engine 加速統計資料會納入 [BigQuery `INFORMATION_SCHEMA`](https://docs.cloud.google.com/bigquery/docs/information-schema-intro?hl=zh-tw) 檢視畫面，做為 `INFORMATION_SCHEMA.JOBS_BY_*` 檢視畫面的一部分，位於 [`bi_engine_statistics`](https://docs.cloud.google.com/bigquery/docs/information-schema-jobs?hl=zh-tw#schema) 欄中。舉例來說，這項查詢會傳回過去 24 小時內所有目前專案工作的 `bi_engine_statistics`：

```
SELECT
  creation_time,
  job_id,
  bi_engine_statistics
FROM
  `region-us`.INFORMATION_SCHEMA.JOBS_BY_PROJECT
WHERE
  creation_time >
     TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 1 DAY)
  AND job_type = "QUERY"
```

請使用以下格式，在 `INFORMATION_SCHEMA` 檢視畫面中，為 `project-id`、`region` 和 `views` 指定[地域性](https://docs.cloud.google.com/bigquery/docs/information-schema-views?hl=zh-tw#scope_and_syntax)：

```
`PROJECT_ID`.`region-REGION_NAME`.INFORMATION_SCHEMA.VIEW
```

**記錄運算單元指標：**雖然系統會回報 BI Engine 的運算單元指標，但加速的 BI Engine 輸入階段不會計入運算單元保留項目。詳情請參閱[定價](https://docs.cloud.google.com/bigquery/pricing?hl=zh-tw#bi-engine-pricing)頁面。

### 查看數據分析資訊結構定義詳細資料

您可以查看 [`INFORMATION_SCHEMA.JOBS` 檢視畫面](https://docs.cloud.google.com/bigquery/docs/information-schema-jobs?hl=zh-tw)，追蹤 BigQuery 使用的 Google 數據分析報表和資料來源。BigQuery 中的每個數據分析查詢都會建立含有 `report_id` 和 `datasource_id` 標籤的項目。開啟報表或資料來源頁面時，這些 ID 會顯示在數據分析網址的結尾。舉例來說，網址為 `https://lookerstudio.google.com/navigation/reporting/my-report-id-123` 的報表，其報表 ID 為 `"my-report-id-123"`。

下列範例說明如何查看報表和資料來源：

#### 找出每個數據分析 BigQuery 工作的報表和資料來源網址

```
-- Standard labels used by Data Studio.
DECLARE requestor_key STRING DEFAULT 'requestor';
DECLARE requestor_value STRING DEFAULT 'looker_studio';

CREATE TEMP FUNCTION GetLabel(labels ANY TYPE, label_key STRING)
AS (
  (SELECT l.value FROM UNNEST(labels) l WHERE l.key = label_key)
);

CREATE TEMP FUNCTION GetDatasourceUrl(labels ANY TYPE)
AS (
  CONCAT("https://lookerstudio.google.com/datasources/", GetLabel(labels, 'looker_studio_datasource_id'))
);

CREATE TEMP FUNCTION GetReportUrl(labels ANY TYPE)
AS (
  CONCAT("https://lookerstudio.google.com/reporting/", GetLabel(labels, 'looker_studio_report_id'))
);

SELECT
  job_id,
  GetDatasourceUrl(labels) AS datasource_url,
  GetReportUrl(labels) AS report_url,
FROM
  `region-us`.INFORMATION_SCHEMA.JOBS jobs
WHERE
  creation_time > TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 7 DAY)
  AND GetLabel(labels, requestor_key) = requestor_value
LIMIT
  100;
```

#### 查看使用報表和資料來源產生的工作

```
-- Specify report and data source id, which can be found at the end of Data Studio URLs.
DECLARE user_report_id STRING DEFAULT '*report id here*';
DECLARE user_datasource_id STRING DEFAULT '*datasource id here*';

-- Data Studio labels for BigQuery.
DECLARE requestor_key STRING DEFAULT 'requestor';
DECLARE requestor_value STRING DEFAULT 'looker_studio';
DECLARE datasource_key STRING DEFAULT 'looker_studio_datasource_id';
DECLARE report_key STRING DEFAULT 'looker_studio_report_id';

CREATE TEMP FUNCTION GetLabel(labels ANY TYPE, label_key STRING)
AS (
  (SELECT l.value FROM UNNEST(labels) l WHERE l.key = label_key)
);

SELECT
  creation_time,
  job_id,
FROM
  `region-us`.INFORMATION_SCHEMA.JOBS jobs
WHERE
  creation_time > TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 7 DAY)
  AND GetLabel(labels, requestor_key) = requestor_value
  AND GetLabel(labels, datasource_key) = user_datasource_id
  AND GetLabel(labels, report_key) = user_report_id
ORDER BY 1
LIMIT 100;
```

## Cloud Logging

BI Engine 加速是 BigQuery 工作處理程序的一部分。如要檢查特定專案的 BigQuery 工作，請查看 [Cloud Logging](https://console.cloud.google.com/logs/query?hl=zh-tw) 頁面，並使用 `protoPayload.serviceName="bigquery.googleapis.com"` 做為酬載。

## 後續步驟

* 進一步瞭解 [Cloud Monitoring](https://docs.cloud.google.com/monitoring/docs?hl=zh-tw)
* 進一步瞭解 Monitoring [圖表](https://docs.cloud.google.com/monitoring/charts?hl=zh-tw)。
* 進一步瞭解 Monitoring [快訊](https://docs.cloud.google.com/monitoring/alerts?hl=zh-tw)。
* 進一步瞭解 [Cloud Logging](https://docs.cloud.google.com/logging/docs?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-14 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-14 (世界標準時間)。"],[],[]]