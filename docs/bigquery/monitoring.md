Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# BigQuery 監控簡介

如要在雲端中執行可靠的應用程式，監控和記錄功能至關重要。BigQuery 工作負載也不例外，尤其是大量或對公司業務十分重要的工作負載。本文將概略介紹可供 BigQuery 使用的監控資料。

監控和記錄來源可能因取樣或匯總頻率而異。舉例來說，資訊結構定義資料的精細程度可能高於 Cloud Monitoring 指標資料。

因此，細微程度較低的指標圖表，可能會與可比較的資訊架構統計資料有所出入。匯總作業通常會消除差異。設計監控解決方案時，請根據需求評估指標的請求回應時間、精確度和準確度。

## 指標

指標是定期收集的數值，可用於分析。指標可用於：

* 建立圖表和資訊主頁。
* 針對需要人為介入的情況觸發快訊。
* 分析歷來成效。

以 BigQuery 來說，可用的指標包括執行中的工作數、查詢期間掃描的位元組數，以及查詢時間的分布情形。查詢成功後，查詢的指標才會顯示，且最多可能需要七分鐘才會回報。系統不會回報失敗查詢的指標。如要查看可用指標的完整清單，包括取樣率、可見度和限制，請參閱「[Google Cloud 指標](https://docs.cloud.google.com/monitoring/api/metrics_gcp?hl=zh-tw)」下的「[`bigquery`](https://docs.cloud.google.com/monitoring/api/metrics_gcp_a_b?hl=zh-tw#gcp-bigquery)」。

使用 [Cloud Monitoring](https://docs.cloud.google.com/monitoring/docs?hl=zh-tw) 查看 BigQuery 指標，並建立圖表和快訊。每項指標都有資源類型 (`bigquery_dataset`、`bigquery_project` 或 `global`) 和一組標籤。您可以使用標籤，依據標籤分組或篩選各項指標。

舉例來說，如要繪製進行中互動式查詢的數量圖表，請使用下列 PromQL 陳述式，依 `priority` 等於 `interactive` 進行篩選：

```
{"bigquery.googleapis.com/query/count", monitored_resource="global", priority="interactive"}
```

下一個範例會取得進行中的載入工作數量，並以 10 分鐘為間隔分組：

```
avg_over_time({"bigquery.googleapis.com/job/num_in_flight",
  monitored_resource="bigquery_project",
  job_type="load"
}[10m])
```

詳情請參閱「[建立 BigQuery 的圖表和快訊](https://docs.cloud.google.com/bigquery/docs/monitoring-dashboard?hl=zh-tw)」。

## 記錄

記錄是因應特定事件或動作而產生的文字記錄。BigQuery 會為建立或刪除資料表、購買運算單元或執行載入工作等動作建立記錄檔項目。如要進一步瞭解記錄功能，請參閱 [Cloud Logging](https://docs.cloud.google.com/logging/docs?hl=zh-tw)。 Google Cloud

記錄是僅附加的記錄項目集合。舉例來說，您可以將自己的記錄項目寫入名為 `projects/PROJECT_ID/logs/my-test-log` 的記錄。許多服務 (包括 BigQuery) 都會建立一種稱為[稽核記錄](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw)的記錄。Google Cloud 這些記錄檔會記錄：

* 管理活動，例如建立或修改資源。
* 資料存取權，例如從資源讀取使用者提供的資料。
* 由 Google 系統產生，而非由使用者動作觸發的系統事件。

稽核記錄會以結構化 JSON 格式編寫。Google Cloud 記錄項目的基本資料類型是 [`LogEntry`](https://docs.cloud.google.com/logging/docs/reference/v2/rest/v2/LogEntry?hl=zh-tw) 結構。這個結構包含記錄名稱、產生記錄項目的資源、時間戳記 (世界標準時間) 和其他基本資訊。

記錄事件的詳細資料會包含在名為「payload」的子欄位中。如果是稽核記錄，酬載欄位會命名為 `protoPayload`。這個欄位的值是 [`AuditLog`](https://docs.cloud.google.com/logging/docs/reference/audit/auditlog/rest/Shared.Types/AuditLog?hl=zh-tw) 結構，由 `protoPayload.@type` 欄位的值 (設為 `type.googleapis.com/google.cloud.audit.AuditLog`) 指出。

針對資料集、資料表和作業，BigQuery 會以兩種不同格式寫入稽核記錄，但兩者都共用 `AuditLog` 基本類型。

舊版格式：

* `resource.type` 欄位為 `bigquery_resource`。
* 作業詳細資料會寫入 `protoPayload.serviceData` 欄位。這個欄位的值是 [`AuditData`](https://docs.cloud.google.com/bigquery/docs/reference/auditlogs/rest/Shared.Types/AuditData?hl=zh-tw) 結構。

新版格式：

* `resource.type` 欄位為 `bigquery_project` 或 `bigquery_dataset`。
  `bigquery_project` 資源包含與工作相關的記錄項目，`bigquery_dataset` 資源則包含與儲存空間相關的記錄項目。
* 作業詳細資料會寫入 `protoPayload.metadata` 欄位。這個欄位的值是 [`BigQueryAuditMetadata`](https://docs.cloud.google.com/bigquery/docs/reference/auditlogs/rest/Shared.Types/BigQueryAuditMetadata?hl=zh-tw) 結構。

建議您使用新版格式的記錄。詳情請參閱「[稽核記錄遷移指南](https://docs.cloud.google.com/bigquery/docs/reference/auditlogs/migration?hl=zh-tw)」。

以下是顯示作業失敗的記錄項目簡短範例：

```
{
  "protoPayload": {
    "@type": "type.googleapis.com/google.cloud.audit.AuditLog",
    "status": {
      "code": 5,
      "message": "Not found: Dataset my-project:my-dataset was not found in location US"
    },
    "authenticationInfo": { ... },
    "requestMetadata":  { ... },
    "serviceName": "bigquery.googleapis.com",
    "methodName": "google.cloud.bigquery.v2.JobService.InsertJob",
    "metadata": {
  },
  "resource": {
    "type": "bigquery_project",
    "labels": { .. },
  },
  "severity": "ERROR",
  "logName": "projects/my-project/logs/cloudaudit.googleapis.com%2Fdata_access",
  ...
}
```

如要對 BigQuery 預留項目執行作業，`protoPayload` 是 [`AuditLog`](https://docs.cloud.google.com/logging/docs/reference/audit/auditlog/rest/Shared.Types/AuditLog?hl=zh-tw) `protoPayload.request` 和 `protoPayload.response` 欄位中的結構，內含更多資訊。您可以在 [BigQuery Reservation API](https://docs.cloud.google.com/bigquery/docs/reference/reservations/rpc?hl=zh-tw) 中找到欄位定義。詳情請參閱「[監控 BigQuery 預留項目](https://docs.cloud.google.com/bigquery/docs/reservations-monitoring?hl=zh-tw)」。

## BigQuery `INFORMATION_SCHEMA` 檢視畫面

[`INFORMATION_SCHEMA`](https://docs.cloud.google.com/bigquery/docs/information-schema-intro?hl=zh-tw) 檢視畫面是 BigQuery 的另一項洞察資訊來源，可與指標和記錄搭配使用。

這些檢視區塊包含工作、資料集、資料表和其他 BigQuery 實體的相關中繼資料。舉例來說，您可以取得指定時間範圍內執行的 BigQuery 工作相關即時中繼資料，然後依專案、使用者、參照的資料表和其他維度，將結果分組或篩選。

您可以運用這項資訊，對 BigQuery 工作負載進行更詳細的分析，並回答下列問題：

* 在過去 7 天內，特定專案的所有查詢平均運算單元用量是多少？
* 哪些使用者為特定專案提交了批次載入工作？
* 過去 30 分鐘內發生哪些串流錯誤 (依錯誤代碼分組)？

特別是查看[工作的中繼資料](https://docs.cloud.google.com/bigquery/docs/information-schema-jobs?hl=zh-tw)、[串流中繼資料](https://docs.cloud.google.com/bigquery/docs/information-schema-streaming?hl=zh-tw)和[預留位置中繼資料](https://docs.cloud.google.com/bigquery/docs/information-schema-reservations?hl=zh-tw)，深入瞭解 BigQuery 工作負載的效能。

您可以在 [GitHub`INFORMATION_SCHEMA`](https://github.com/GoogleCloudPlatform/bigquery-utils/tree/master/dashboards/system_tables) 上找到查詢範例，瞭解機構的運算單元和預留運算單元用量、工作執行情況和工作錯誤。舉例來說，下列查詢會提供待處理或正在執行的查詢清單。這些查詢會依據在 `us` 區域建立的時間長度排序：

```
SELECT
    creation_time,
    project_id,
    user_email,
    job_id,
    job_type,
    priority,
    state,
    TIMESTAMP_DIFF(CURRENT_TIMESTAMP(), start_time,second) as running_time_sec
 FROM
   `region-us`.INFORMATION_SCHEMA.JOBS_BY_PROJECT
 WHERE
    creation_time BETWEEN TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 1 DAY) AND CURRENT_TIMESTAMP()
    AND state != "DONE"
ORDER BY
    running_time_sec DESC
```

詳情請參閱「[使用這些資訊主頁排解 BigQuery 效能問題](https://cloud.google.com/blog/products/data-analytics/troubleshoot-bigquery-performance-with-these-dashboards?hl=zh-tw)」。

除了自行編寫查詢，您還可以在 Google Cloud 控制台使用 BigQuery 監控工具：

* **[監控健康狀態和資源使用情形](https://docs.cloud.google.com/bigquery/docs/admin-resource-charts?hl=zh-tw)。**
  查看運作健康狀態資訊主頁和資源圖表，追蹤機構和預留項目中一段時間內的時段使用情形、容量和工作並行數。
* **[監控作業](https://docs.cloud.google.com/bigquery/docs/admin-jobs-explorer?hl=zh-tw)。**在整個機構中搜尋、篩選及分組個別查詢執行作業，檢查查詢執行圖表、找出頂尖的時段消費者，並排解有問題的工作。

## 後續步驟

* 瞭解如何[使用工作探索工具監控及篩選工作](https://docs.cloud.google.com/bigquery/docs/admin-jobs-explorer?hl=zh-tw)。
* 瞭解如何[監控健康狀態和資源使用率](https://docs.cloud.google.com/bigquery/docs/admin-resource-charts?hl=zh-tw)。
* 瞭解如何[為 BigQuery 建立圖表和快訊](https://docs.cloud.google.com/bigquery/docs/monitoring-dashboard?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-10-19 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-10-19 (世界標準時間)。"],[],[]]