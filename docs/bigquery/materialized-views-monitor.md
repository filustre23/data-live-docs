Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 監控具體化檢視表

您可以使用資訊結構定義和記錄監控等工具，監控[具體化檢視區塊](https://docs.cloud.google.com/bigquery/docs/materialized-views-intro?hl=zh-tw)。

如要建立具體化檢視表清單，請參閱「[列出具體化檢視表](https://docs.cloud.google.com/bigquery/docs/materialized-views-manage?hl=zh-tw#list)」。

## 具體化檢視表資訊結構定義檢視畫面

如要探索具體化檢視表，請查詢 [`INFORMATION_SCHEMA.TABLES`view](https://docs.cloud.google.com/bigquery/docs/information-schema-tables?hl=zh-tw)。如要擷取具體化檢視區塊的屬性，請查詢 [`INFORMATION_SCHEMA.TABLE_OPTIONS` 檢視區塊](https://docs.cloud.google.com/bigquery/docs/information-schema-table-options?hl=zh-tw)。

具體化檢視區塊不會列在 [`INFORMATION_SCHEMA.VIEWS` 檢視區塊](https://docs.cloud.google.com/bigquery/docs/information-schema-views?hl=zh-tw)資料表中。

## 監控自動重新整理

本節說明如何查看[具體化檢視區塊的重新整理詳細資料](https://docs.cloud.google.com/bigquery/docs/materialized-views-manage?hl=zh-tw#refresh)。

### 查看上次重新整理狀態

如要擷取具體化檢視表的目前狀態，請呼叫 [`tables.get` 方法](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables/get?hl=zh-tw)，或查詢 [`INFORMATION_SCHEMA.MATERIALIZED_VIEWS` 檢視表](https://docs.cloud.google.com/bigquery/docs/information-schema-materialized-views?hl=zh-tw)。

例如：

```
SELECT
  table_name, last_refresh_time, refresh_watermark, last_refresh_status
FROM
  `DATASET`.INFORMATION_SCHEMA.MATERIALIZED_VIEWS;
```

如果 `last_refresh_status` 的值不是 `NULL`，表示上次自動重新整理作業失敗。手動重新整理要求不會顯示在這裡。變更基礎資料表可能會導致具體化檢視定義失效，進而導致自動重新整理期間發生錯誤。詳情請參閱「[增量更新](https://docs.cloud.google.com/bigquery/docs/materialized-views-use?hl=zh-tw#incremental_updates)」。舉例來說，如果從基本資料表捨棄實體化檢視參照的資料欄，`last_refresh_status` 欄位會傳回 `invalidQuery` 錯誤。詳情請參閱「[錯誤訊息](https://docs.cloud.google.com/bigquery/docs/error-messages?hl=zh-tw)」。

### 列出自動重新整理工作

如要列出具體化檢視區塊自動重新整理工作，請呼叫 [`jobs.list` 方法](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs/list?hl=zh-tw)。如要擷取工作詳細資料，請呼叫 [`jobs.get` 方法](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs/get?hl=zh-tw)。您也可以查詢 [`INFORMATION_SCHEMA.JOBS_BY_*` 檢視畫面](https://docs.cloud.google.com/bigquery/docs/information-schema-jobs?hl=zh-tw)，擷取工作詳細資料。自動重新整理工作包含`materialized_view_refresh`前置字元 (位於[工作 ID](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#FIELDS.id) 內)，且由 BigQuery 管理員帳戶啟動。

例如：

```
SELECT
  job_id, total_slot_ms, total_bytes_processed,
  materialized_view_statistics.materialized_view[SAFE_OFFSET(0)].rejected_reason
  AS full_refresh_reason
FROM
  `region-us.INFORMATION_SCHEMA.JOBS_BY_PROJECT`
WHERE
  job_id LIKE '%materialized_view_refresh_%'
LIMIT 10;
```

如要監控重新整理工作的費用，並視需要調整自動重新整理間隔，請查看 `total_bytes_processed` 和 `total_slot_ms` 欄位。

舉例來說，如果基礎資料表的擷取率相對較小，則較不常重新整理檢視區塊是合理的做法。如果基礎資料變更快速，建議提高重新整理頻率。

如果基礎資料表會在預先定義的時間點擷取資料 (例如使用夜間擷取、轉換和載入 (ETL) 管道)，請考慮控管具體化檢視區塊維護時間表，方法如下：

1. [停用自動重新整理功能](https://docs.cloud.google.com/bigquery/docs/materialized-views-manage?hl=zh-tw#automatic-refresh)。
2. [手動重新整理](https://docs.cloud.google.com/bigquery/docs/materialized-views-manage?hl=zh-tw#manual-refresh)，可做為 ETL 管道的一部分，或是在一天中的特定時段設定排程查詢。

資料表截斷、分區截斷、分區到期，以及對基本資料表執行的 `UPDATE`、`DELETE` 和 `MERGE` 資料操縱語言 (DML) 陳述式，都可能導致具體化檢視區失效。如果 materialized view 已分割，系統會使修改過的分區失效；否則，整個 materialized view 都會失效。因此，您可能需要批次處理 DML 陳述式，並在查詢結束時手動重新整理。

如要進一步瞭解具體化檢視表的定價，請參閱[具體化檢視表定價](https://docs.cloud.google.com/bigquery/docs/materialized-views-intro?hl=zh-tw#materialized_views_pricing)。

### 監控具體化檢視表重新整理失敗的情況

您可以建立自動化程序，監控具體化檢視區塊的重新整理作業是否失敗，並使用 [Cloud Logging](https://docs.cloud.google.com/logging/docs/overview?hl=zh-tw) 中的 [BigQuery 稽核記錄](https://docs.cloud.google.com/bigquery/docs/reference/auditlogs?hl=zh-tw)傳送快訊。BigQuery 會為具體化檢視表重新整理工作建立記錄項目，包括失敗的項目。您可以使用 Google Cloud 控制台的[記錄檔探索工具](https://docs.cloud.google.com/logging/docs/view/logs-explorer-interface?hl=zh-tw)，擷取、查看及分析記錄項目。這些項目會儲存在[記錄檔 bucket](https://docs.cloud.google.com/logging/docs/store-log-entries?hl=zh-tw) 中，這是 Cloud Logging 用來儲存記錄檔資料的容器。

如要建立指標和快訊，請按照下列步驟操作：

### 控制台

請按照下列步驟建立記錄指標，在 10 分鐘間隔內有超過三個具體化檢視區塊重新整理失敗時，傳送快訊。

**建立記錄指標**

1. 如要設定記錄檔探索工具，請按照「[查看及分析記錄檔](https://docs.cloud.google.com/logging/docs/view/logs-explorer-interface?hl=zh-tw#getting_started)」一文的說明操作。
2. 在記錄檔探索工具中，確認「顯示查詢」設定已開啟。

   使用 Google Cloud 控制台時，專案範圍是您在 Google Cloud 控制台專案挑選器中選取的單一專案。如要瞭解如何新增其他專案，請參閱「[將專案新增至指標範圍](https://docs.cloud.google.com/monitoring/settings/multiple-projects?hl=zh-tw#add-monitored-project)」。
3. 在「查詢」窗格中，貼上下列查詢，擷取目前專案記錄範圍內所有失敗的自動具體化檢視表重新整理作業：

   ```
   severity: "ERROR"
   protoPayload.metadata.jobChange.after: "DONE"
   protoPayload.metadata.jobChange.job.jobConfig.queryConfig.query =~ "CALL BQ.REFRESH_MATERIALIZED_VIEW\('.*'\)"
   protoPayload.resourceName =~ ".*materialized_view_refresh_[\w]"
   ```
4. 點選「執行查詢」
5. 點選「動作」，然後選取「建立指標」。
6. 如要根據錯誤數量建立快訊，請選取「計數器」做為指標類型，然後輸入指標的「記錄指標名稱」和「說明」。「單位」欄位可以留空。
7. 如要在「篩選器選取」部分定義指標篩選器，請套用下列設定：

   * 使用「選取專案或記錄檔 bucket」選單，選擇指標的計數範圍。可以選擇 Google Cloud 專案中的記錄項目，或是僅限特定記錄檔 bucket 中的記錄項目。
   * 使用[記錄查詢語言](https://docs.cloud.google.com/logging/docs/view/logging-query-language?hl=zh-tw)建立篩選器，只收集您要在指標中計數的記錄項目。您也可以使用規則運算式建立指標的篩選器。
   * 如要查看符合篩選條件的記錄項目，請按一下「預覽記錄」。
8. 按一下「新增標籤」。
9. 輸入專屬的**標籤名稱**和**說明**，方便您識別指標。將「標籤類型」保留為預設的「字串」。
10. 在「Field name」(欄位名稱) 中輸入下列字串：

    ```
    protoPayload.metadata.jobChange.job.jobConfig.queryConfig.query
    ```
11. 在「規則運算式」部分輸入下列字串：

    ```
    CALL BQ.REFRESH_MATERIALIZED_VIEW\('(.*)'\)
    ```
12. 依序點選「完成」和「建立指標」。

如要進一步瞭解計數器指標，請參閱「[設定計數器指標](https://docs.cloud.google.com/logging/docs/logs-based-metrics/counter-metrics?hl=zh-tw)」。

**建立快訊**

請完成下列步驟，建立快訊政策來指定條件，並在十分鐘內有三項具體化檢視區塊重新整理作業失敗時傳送電子郵件。設定快訊政策時，這個選項可提供更多彈性。如果直接建立記錄指標，系統會在記錄檔中出現具體化檢視重新整理失敗錯誤時，傳送快訊。

1. 前往 Google Cloud 控制台的「記錄指標」頁面。

   [前往「記錄指標」](https://console.cloud.google.com/logs/metrics?hl=zh-tw)
2. 在使用者定義的記錄指標旁，點選 more\_vert「更多動作」>「運用指標建立警告」。
3. 在「選取指標」中，選取您先前為「記錄指標名稱」指定的指標名稱。
4. 在「新增篩選器」中，根據「規則運算式」欄位中定義的具體化檢視區塊命名慣例，為快訊新增篩選條件。

   如果多個團隊使用同一個專案，但邏輯上是依具體化檢視區塊命名慣例劃分，且您需要為這些團隊定義個別的通知管道，這個步驟就很有用。如要進一步瞭解快訊條件，請參閱「使用 Metrics Explorer 時選取指標」一文中的「[篩選圖表資料](https://docs.cloud.google.com/monitoring/charts/metrics-selector?hl=zh-tw#filter-option)」。
5. 在「轉換資料」專區的「Rolling window」(滾動視窗) 設定中，指定大於 10 分鐘的值，確保系統會計算符合篩選條件的多個記錄項目，然後點選「下一步」。
6. 指定「門檻值」，例如 `3`，並視需要設定「警報觸發條件」和「門檻位置」欄位。按一下「下一步」。
7. 選擇接收快訊的通知管道。
8. 點選「建立政策」。

如果具體化檢視的重新整理失敗次數超過門檻，系統就會透過通知管道發出警示。

### Terraform

您可以使用 Terraform 建立自訂指標、快訊政策、通知管道和記錄範圍。下列 Terraform 範例會使用查詢，監控並記錄每個失敗的具體化檢視畫面重新整理作業。

```
resource "google_logging_metric" "failed_mv_refresh_metric" {
project = var.project_id
name    = var.logging_metric_name
filter = trimspace(<<EOT
  severity="ERROR"
  AND protoPayload.metadata.jobChange.after="DONE"
  AND protoPayload.metadata.jobChange.job.jobConfig.queryConfig.query=~"CALL BQ.REFRESH_MATERIALIZED_VIEW\('.*'\)"
  AND protoPayload.resourceName=~".*materialized_view_refresh_[\\w]"
  EOT
  )
metric_descriptor {
  metric_kind  = "DELTA"
  value_type   = "INT64"
  unit         = "1"
  display_name = "Failed Materialized View Refresh Count"

  labels {
    key          = "materialized_view_name"
    value_type   = "STRING"
    description  = "The name of the materialized view that failed to refresh."
  }
}
label_extractors = {
  "materialized_view_name" = "REGEXP_EXTRACT(protoPayload.metadata.jobChange.job.jobConfig.queryConfig.query, \"CALL BQ\\.REFRESH_MATERIALIZED_VIEW\\('(.*)'\\)\")"
}
}
```

下列範例會建立快訊，當失敗的具體化檢視表重新整理作業數量超過門檻時，系統就會傳送電子郵件。

```
resource "google_monitoring_alert_policy" "failed_mv_refresh_alert" {
project      = var.project_id
display_name = var.alert_policy_display_name
combiner     = "OR"

conditions {
  display_name = "Condition: Materialized View Refresh Failure Count Exceeds Threshold"

  condition_threshold {
    filter = "metric.type=\"logging.googleapis.com/user/${google_logging_metric.failed_mv_refresh_metric.name}\" AND resource.type=\"bigquery_project\""

    duration = "${var.alert_duration_seconds}s"

    comparison = "COMPARISON_GT"

    threshold_value = var.alert_threshold_count

    aggregations {
      alignment_period   = "${var.alert_rolling_window_seconds}s"
      per_series_aligner = "ALIGN_DELTA"
      cross_series_reducer = "REDUCE_SUM"
      group_by_fields        = []
    }

    trigger {
      count = 1
    }
  }
}

notification_channels = [
  google_monitoring_notification_channel.email_channel.id,
]
}
```

如需其他範例，請參閱下列文章：

* [google\_logging\_metric](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/logging_metric)
* [google\_monitoring\_alert\_policy](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/monitoring_alert_policy)
* [google\_monitoring\_notification\_channel](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/monitoring_notification_channel)
* [google\_logging\_log\_scope](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/logging_log_scope)

如要進一步瞭解計數器指標，請參閱「[記錄指標總覽](https://docs.cloud.google.com/logging/docs/logs-based-metrics?hl=zh-tw)」的說明。

## 監控具體化檢視表用量

如要查看查詢作業的具體化檢視區塊用量，您可以呼叫 [`jobs.get` 方法](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs/get?hl=zh-tw)或查詢 [`INFORMATION_SCHEMA.JOBS_BY_*` 檢視區塊](https://docs.cloud.google.com/bigquery/docs/information-schema-jobs?hl=zh-tw)，然後查看 `materialized_view_statistics` 欄位，其中提供查詢使用具體化檢視區塊的詳細資料，包括：

* 是否使用具體化檢視表。
* 如果未使用具體化檢視區塊，則會顯示[遭拒原因](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#rejectedreason)。

例如：

```
SELECT
  job_id, materialized_view_statistics
FROM
  region-US.INFORMATION_SCHEMA.JOBS_BY_PROJECT
WHERE
  job_id = '<my-query-job-id>';
```

如要查看具體化檢視表的用量趨勢，請查詢 [`INFORMATION_SCHEMA.JOBS_BY_*` 檢視區塊](https://docs.cloud.google.com/bigquery/docs/information-schema-jobs?hl=zh-tw)。

舉例來說，下列查詢會傳回使用目標具體化檢視區塊的近期查詢工作摘要：

```
SELECT
  mv.table_reference.dataset_id,
  mv.table_reference.table_id,
  MAX(job.creation_time) latest_job_time,
  COUNT(job_id) job_count
FROM
  region-US.INFORMATION_SCHEMA.JOBS_BY_PROJECT job,
  UNNEST(materialized_view_statistics.materialized_view) mv
WHERE
  job.creation_time > TIMESTAMP_SUB(CURRENT_TIMESTAMP, INTERVAL 7 DAY)
  AND mv.table_reference.dataset_id = 'MY_DATASET'
  AND mv.table_reference.table_id = 'MY_MATERIALIZED_VIEW'
  AND mv.chosen = TRUE
GROUP BY 1, 2;
```

## 使用具體化檢視表排解查詢速度緩慢的問題

如果查詢使用具體化檢視表，但執行速度不如預期，請採取下列做法：

1. 確認查詢是否確實使用預期的具體化檢視表。如需詳細操作說明，請參閱「[監控具體化檢視區塊用量](#monitor_materialized_view_usage)」。
2. [檢查具體化檢視區塊的新鮮度](#view_last_refresh_status)。
3. 請檢查具體化檢視區塊定義和參照的資料，並考慮[採用適當技巧，盡量提高具體化檢視區塊的使用效率](https://docs.cloud.google.com/bigquery/docs/materialized-views-create?hl=zh-tw#best_practices_when_creating_materialized_views)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-09 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-09 (世界標準時間)。"],[],[]]