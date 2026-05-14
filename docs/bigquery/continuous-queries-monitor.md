Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 監控持續查詢

您可以使用下列 BigQuery 工具，監控 BigQuery[持續查詢](https://docs.cloud.google.com/bigquery/docs/continuous-queries-introduction?hl=zh-tw)：

* [`INFORMATION_SCHEMA` 觀看次數](https://docs.cloud.google.com/bigquery/docs/information-schema-intro?hl=zh-tw)
* [查詢執行圖表](https://docs.cloud.google.com/bigquery/docs/query-insights?hl=zh-tw#view_query_performance_insights)
* [工作記錄](https://docs.cloud.google.com/bigquery/docs/managing-jobs?hl=zh-tw#view-job)
* [行政工作探索工具](https://docs.cloud.google.com/bigquery/docs/admin-jobs-explorer?hl=zh-tw)

由於 BigQuery 持續查詢的執行時間較長，通常在 SQL 查詢完成時產生的指標可能會缺漏或不準確。

## 使用 `INFORMATION_SCHEMA` 檢視畫面

您可以使用多個 `INFORMATION_SCHEMA` 檢視畫面，監控持續查詢和持續查詢預留項目。

**注意：** `JOBS* INFORMATION_SCHEMA` 檢視畫面只會保留執行中持續查詢的資料兩天。

### 查看工作詳細資料

您可以使用 [`JOBS`](https://docs.cloud.google.com/bigquery/docs/information-schema-jobs?hl=zh-tw) 檢視表取得持續查詢工作的中繼資料。

下列查詢會傳回所有有效持續查詢的中繼資料。中繼資料包含輸出浮水印時間戳記，代表持續查詢成功處理資料的時間點。

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中執行下列查詢：

   ```
   SELECT
     start_time,
     job_id,
     user_email,
     query,
     state,
     reservation_id,
     continuous_query_info.output_watermark
   FROM `PROJECT_ID.region-REGION.INFORMATION_SCHEMA.JOBS`
   WHERE
     creation_time > TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 7 day)
     AND continuous IS TRUE
     AND state = "RUNNING"
   ORDER BY
     start_time DESC
   ```

   更改下列內容：

   * `PROJECT_ID`：專案 ID。
   * `REGION`：任何[資料集區域名稱](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)。
     例如：`region-us`。

### 查看預留項目指派作業詳細資料

您可以使用 [`ASSIGNMENTS`](https://docs.cloud.google.com/bigquery/docs/information-schema-assignments?hl=zh-tw) 和 [`RESERVATIONS`](https://docs.cloud.google.com/bigquery/docs/information-schema-reservations?hl=zh-tw) 檢視畫面，取得持續查詢預留指派詳細資料。

傳回連續查詢的保留項目指派詳細資料：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中執行下列查詢：

   ```
   SELECT
     reservation.reservation_name,
     reservation.slot_capacity
   FROM
     `ADMIN_PROJECT_ID.region-LOCATION.INFORMATION_SCHEMA.ASSIGNMENTS`
       AS assignment
   INNER JOIN
     `ADMIN_PROJECT_ID.region-LOCATION.INFORMATION_SCHEMA.RESERVATIONS`
       AS reservation
     ON (assignment.reservation_name = reservation.reservation_name)
   WHERE
     assignment.assignee_id = 'PROJECT_ID'
     AND job_type = 'CONTINUOUS';
   ```

   更改下列內容：

   * `ADMIN_PROJECT_ID`：擁有預留資源的[管理專案](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#admin-project) ID。
   * `LOCATION`：預訂地點。
   * `PROJECT_ID`：指派給預留項目的專案 ID。系統只會傳回在這個專案中執行的持續查詢相關資訊。

### 查看運算單元消耗量資訊

您可以使用 [`ASSIGNMENTS`](https://docs.cloud.google.com/bigquery/docs/information-schema-assignments?hl=zh-tw)、[`RESERVATIONS`](https://docs.cloud.google.com/bigquery/docs/information-schema-reservations?hl=zh-tw) 和 [`JOBS_TIMELINE`](https://docs.cloud.google.com/bigquery/docs/information-schema-jobs-timeline?hl=zh-tw) 檢視畫面，取得持續查詢的查詢配額消耗資訊。

傳回持續查詢的時段消耗量資訊：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中執行下列查詢：

   ```
   SELECT
     jobs.period_start,
     reservation.reservation_name,
     reservation.slot_capacity,
     SUM(jobs.period_slot_ms) / 1000 AS consumed_total_slots
   FROM
     `ADMIN_PROJECT_ID.region-LOCATION.INFORMATION_SCHEMA.ASSIGNMENTS`
       AS assignment
   INNER JOIN
     `ADMIN_PROJECT_ID.region-LOCATION.INFORMATION_SCHEMA.RESERVATIONS`
       AS reservation
     ON (assignment.reservation_name = reservation.reservation_name)
   INNER JOIN
     `PROJECT_ID.region-LOCATION.INFORMATION_SCHEMA.JOBS_TIMELINE` AS jobs
     ON (
       UPPER(CONCAT('ADMIN_PROJECT_ID:LOCATION.', assignment.reservation_name))
       = UPPER(jobs.reservation_id))
   WHERE
     assignment.assignee_id = 'PROJECT_ID'
     AND assignment.job_type = 'CONTINUOUS'
     AND jobs.period_start
       BETWEEN TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 1 DAY)
       AND CURRENT_TIMESTAMP()
   GROUP BY 1, 2, 3
   ORDER BY jobs.period_start DESC;
   ```

   更改下列內容：

   * `ADMIN_PROJECT_ID`：擁有預留資源的[管理專案](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#admin-project) ID。
   * `LOCATION`：預訂地點。
   * `PROJECT_ID`：指派給預留項目的專案 ID。系統只會傳回在這個專案中執行的持續查詢相關資訊。

您也可以使用其他工具 (例如 [Metrics Explorer](https://docs.cloud.google.com/monitoring/charts/metrics-explorer?hl=zh-tw) 和[管理資源圖表](https://docs.cloud.google.com/bigquery/docs/admin-resource-charts?hl=zh-tw#view-resource-utilization)) 監控持續查詢預留量。
詳情請參閱「[監控 BigQuery 預留項目](https://docs.cloud.google.com/bigquery/docs/reservations-monitoring?hl=zh-tw)」。

## 使用查詢執行圖表

您可以透過[查詢執行圖](https://docs.cloud.google.com/bigquery/docs/query-insights?hl=zh-tw#view_query_performance_insights)，取得持續查詢的效能深入分析和一般統計資料。詳情請參閱「[查看查詢效能深入分析](https://docs.cloud.google.com/bigquery/docs/query-insights?hl=zh-tw#view_query_performance_insights)」。

## 查看工作記錄

您可以在個人工作記錄或專案工作記錄中，查看持續查詢工作的詳細資料。詳情請參閱「[查看工作詳細資料](https://docs.cloud.google.com/bigquery/docs/managing-jobs?hl=zh-tw#view-job)」。

請注意，工作記錄清單會依工作開始時間排序，因此已執行一段時間的連續查詢可能不會出現在清單開頭。

## 使用管理工作探索工具

在管理工作探索器中[篩選工作](https://docs.cloud.google.com/bigquery/docs/admin-jobs-explorer?hl=zh-tw#filter-jobs)，將「工作類別」篩選器設為「持續查詢」，即可顯示持續查詢。

## 使用 Cloud Monitoring

您可以使用 Cloud Monitoring 查看 BigQuery 持續查詢的專屬指標。詳情請參閱「[建立資訊主頁、圖表和快訊](https://docs.cloud.google.com/bigquery/docs/monitoring-dashboard?hl=zh-tw)」，並瞭解[可供視覺化的指標](https://docs.cloud.google.com/bigquery/docs/monitoring-dashboard?hl=zh-tw#metrics)。

## 查詢失敗時發出快訊

建議您建立快訊，在持續查詢失敗時收到通知，不必定期檢查。其中一種做法是建立自訂的 [Cloud Logging 記錄指標](https://docs.cloud.google.com/logging/docs/logs-based-metrics/counter-metrics?hl=zh-tw)，並為作業設定篩選器，然後根據該指標建立 [Cloud Monitoring 警告政策](https://docs.cloud.google.com/monitoring/alerts/using-alerting-ui?hl=zh-tw)：

1. 建立持續查詢時，請使用[自訂工作 ID 前置字元](https://docs.cloud.google.com/bigquery/docs/continuous-queries?hl=zh-tw#custom-job-id)。多個連續查詢可以共用相同的前置字元。
   舉例來說，您可以使用 `prod-` 前置字串表示生產查詢。
2. 前往 Google Cloud 控制台的「記錄指標」頁面。

   [前往「記錄指標」](https://console.cloud.google.com/logs/metrics?hl=zh-tw)
3. 按一下「建立指標」，「建立記錄指標」面板隨即顯示。
4. 在「Metric type」(指標類型) 部分，選取「Counter」(計數器)。
5. 在「詳細資料」部分，為指標命名。例如：`CUSTOM_JOB_ID_PREFIX-metric`。
6. 在「選取篩選條件」部分，在「建立篩選器」編輯器中輸入下列內容：

   ```
   resource.type = "bigquery_project"
   protoPayload.resourceName : "projects/PROJECT_ID/jobs/CUSTOM_JOB_ID_PREFIX"
   severity = ERROR
   ```

   更改下列內容：

   * `PROJECT_ID`：專案名稱。
   * `CUSTOM_JOB_ID_PREFIX`：您為持續查詢設定的[自訂工作 ID 前置字元](https://docs.cloud.google.com/bigquery/docs/continuous-queries?hl=zh-tw#custom-job-id)名稱。
7. 點選「建立指標」。
8. 在導覽選單中，按一下「以記錄為準的指標」。您剛建立的指標會顯示在使用者定義指標清單中。
9. 在指標的資料列中，依序點選 more\_vert「更多動作」和「運用指標建立快訊」。
10. 點選「下一步」。您不需要變更「政策設定模式」頁面的預設設定。
11. 點選「下一步」。您不需要變更「Configure alert trigger」(設定快訊觸發條件) 頁面的預設設定。
12. 選取通知管道，然後輸入快訊政策的名稱。
13. 點選「建立政策」。

您可以執行持續查詢，並使用所選的自訂工作 ID 前置字元，然後取消查詢，藉此測試快訊。警報可能需要幾分鐘才會傳送到通知管道。

## 重試失敗的查詢

重試失敗的持續查詢，有助於避免持續管道長時間停機，或需要人為介入才能重新啟動的情況。重試失敗的持續查詢時，請注意下列重要事項：

* 是否可容許重新處理先前查詢處理的部分資料 (查詢失敗前)。
* 如何處理限制重試次數或使用指數輪詢。

以下是自動重試查詢的其中一種可能方法：

1. 根據符合下列條件的納入篩選器建立 [Cloud Logging 接收器](https://docs.cloud.google.com/logging/docs/export/configure_export_v2?hl=zh-tw#creating_sink)，將記錄轉送至 Pub/Sub 主題：

   ```
   resource.type = "bigquery_project"
   protoPayload.resourceName : "projects/PROJECT_ID/jobs/CUSTOM_JOB_ID_PREFIX"
   severity = ERROR
   ```

   更改下列內容：

   * `PROJECT_ID`：專案名稱。
   * `CUSTOM_JOB_ID_PREFIX`：您為持續查詢設定的[自訂工作 ID 前置字元](https://docs.cloud.google.com/bigquery/docs/continuous-queries?hl=zh-tw#custom-job-id)名稱。
2. 建立 [Cloud Run 函式](https://docs.cloud.google.com/functions/docs/calling?hl=zh-tw)，在 Pub/Sub 收到符合篩選條件的記錄時觸發。

   Cloud Run 函式可以接受 Pub/Sub 訊息中的資料酬載，並嘗試使用與失敗查詢相同的 SQL 語法，啟動新的持續查詢，但會從先前工作停止後不久開始。

舉例來說，您可以使用類似下列的函式：

### Python

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Python 設定說明操作。詳情請參閱 [BigQuery Python API 參考說明文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import base64
import json
import logging
import re
import uuid

import google.auth
import google.auth.transport.requests
import requests


def retry_continuous_query(event, context):
    logging.info("Cloud Function started.")

    if "data" not in event:
        logging.info("No data in Pub/Sub message.")
        return

    try:
        # Decode and parse the Pub/Sub message data
        log_entry = json.loads(base64.b64decode(event["data"]).decode("utf-8"))

        # Extract the SQL query and other necessary data
        proto_payload = log_entry.get("protoPayload", {})
        metadata = proto_payload.get("metadata", {})
        job_change = metadata.get("jobChange", {})
        job = job_change.get("job", {})
        job_config = job.get("jobConfig", {})
        query_config = job_config.get("queryConfig", {})
        sql_query = query_config.get("query")
        job_stats = job.get("jobStats", {})
        end_timestamp = job_stats.get("endTime")
        failed_job_id = job.get("jobName")

        # Check if required fields are missing
        if not all([sql_query, failed_job_id, end_timestamp]):
            logging.error("Required fields missing from log entry.")
            return

        logging.info(f"Retrying failed job: {failed_job_id}")

        # Adjust the timestamp in the SQL query
        timestamp_match = re.search(
            r"\s*TIMESTAMP\(('.*?')\)(\s*\+ INTERVAL 1 MICROSECOND)?", sql_query
        )

        if timestamp_match:
            original_timestamp = timestamp_match.group(1)
            new_timestamp = f"'{end_timestamp}'"
            sql_query = sql_query.replace(original_timestamp, new_timestamp)
        elif "CURRENT_TIMESTAMP() - INTERVAL 10 MINUTE" in sql_query:
            new_timestamp = f"TIMESTAMP('{end_timestamp}') + INTERVAL 1 MICROSECOND"
            sql_query = sql_query.replace(
                "CURRENT_TIMESTAMP() - INTERVAL 10 MINUTE", new_timestamp
            )

        # Get access token
        credentials, project = google.auth.default(
            scopes=["https://www.googleapis.com/auth/cloud-platform"]
        )
        request = google.auth.transport.requests.Request()
        credentials.refresh(request)
        access_token = credentials.token

        # API endpoint
        url = f"https://bigquery.googleapis.com/bigquery/v2/projects/{project}/jobs"

        # Request headers
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }

        # Generate a random UUID
        random_suffix = str(uuid.uuid4())[:8]  # Take the first 8 characters of the UUID

        # Combine the prefix and random suffix
        job_id = f"CUSTOM_JOB_ID_PREFIX{random_suffix}"

        # Request payload
        data = {
            "configuration": {
                "query": {
                    "query": sql_query,
                    "useLegacySql": False,
                    "continuous": True,
                    "connectionProperties": [
                        {"key": "service_account", "value": "SERVICE_ACCOUNT"}
                    ],
                    # ... other query parameters ...
                },
                "labels": {"bqux_job_id_prefix": "CUSTOM_JOB_ID_PREFIX"},
            },
            "jobReference": {
                "projectId": project,
                "jobId": job_id,  # Use the generated job ID here
            },
        }

        # Make the API request
        response = requests.post(url, headers=headers, json=data)

        # Handle the response
        if response.status_code == 200:
            logging.info("Query job successfully created.")
        else:
            logging.error(f"Error creating query job: {response.text}")

    except Exception as e:
        logging.error(
            f"Error processing log entry or retrying query: {e}", exc_info=True
        )

    logging.info("Cloud Function finished.")
```

## 後續步驟

* 瞭解如何建立及執行[連續查詢](https://docs.cloud.google.com/bigquery/docs/continuous-queries?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-14 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-14 (世界標準時間)。"],[],[]]