Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# BigQuery 監控功能簡介

BigQuery 監控功能可讓您追蹤各項工作負載的資源用量、工作執行情形和作業健康狀態，找出瓶頸並維持可靠性。

如要在雲端執行可靠的應用程式，監控和記錄功能至關重要。BigQuery 工作負載也不例外，尤其是工作負載量大或對業務至關重要時。

監控來源會因取樣頻率和匯總層級而異。舉例來說，資訊結構定義檢視表提供的精細程度通常高於 Cloud Monitoring 指標。因此，指標圖表可能會暫時與資訊結構定義資料不一致，直到匯總作業消除差異為止。設計監控策略時，請根據需求評估延遲時間、精確度和準確度。

## 指標

指標是定期收集的數值，可用於分析。指標可用於：

* 建立圖表和資訊主頁。
* 針對需要人工介入的情況或情境觸發警示。
* 分析歷來成效。

以 BigQuery 來說，可用的指標包括執行中的工作數量、查詢期間掃描的位元組數，以及查詢時間的分佈情形。查詢成功後，系統才會提供查詢指標，最多可能需要七分鐘才會回報。系統不會回報失敗查詢的指標。如需可用指標的完整清單 (包括取樣率、瀏覽權限和限制)，請參閱 [Google Cloud 指標](https://docs.cloud.google.com/monitoring/api/metrics_gcp?hl=zh-tw)下的 [`bigquery`](https://docs.cloud.google.com/monitoring/api/metrics_gcp_a_b?hl=zh-tw#gcp-bigquery)。

使用 [Cloud Monitoring](https://docs.cloud.google.com/monitoring/docs?hl=zh-tw) 查看 BigQuery 指標，並建立圖表和快訊。每項指標都有資源類型 (`bigquery_dataset`、`bigquery_project` 或 `global`) 和一組標籤。您可以使用標籤，將各項指標分組或篩選。

舉例來說，如要以圖表呈現執行中的互動式查詢數量，請使用下列 PromQL 陳述式，依 `priority` 等於 `interactive` 進行篩選：

```
{"bigquery.googleapis.com/query/count", monitored_resource="global", priority="interactive"}
```

下一個範例會取得執行中的載入工作數量，並以 10 分鐘為間隔分組：

```
avg_over_time({"bigquery.googleapis.com/job/num_in_flight",
  monitored_resource="bigquery_project",
  job_type="load"
}[10m])
```

詳情請參閱「[建立 BigQuery 圖表和快訊](https://docs.cloud.google.com/bigquery/docs/monitoring-dashboard?hl=zh-tw)」。

## 記錄

記錄是因應特定事件或動作而產生的文字記錄。BigQuery 會為建立或刪除資料表、購買運算單元或執行載入工作等動作建立記錄項目。如要進一步瞭解 Google Cloud中的記錄功能，請參閱「[Cloud Logging](https://docs.cloud.google.com/logging/docs?hl=zh-tw)」。

記錄檔是僅附加的記錄項目集合。舉例來說，您可以將自己的記錄項目寫入名為 `projects/PROJECT_ID/logs/my-test-log` 的記錄。許多Google Cloud 服務 (包括 BigQuery) 都會建立一種稱為「稽核記錄」的記錄。這些記錄會列出：

* 管理活動，例如建立或修改資源。
* 資料存取，例如從資源讀取使用者提供的資料。
* 由 Google 系統 (而非使用者動作) 產生的系統事件。

稽核記錄會以結構化 JSON 格式寫入。Google Cloud 記錄項目的基本資料類型是 [`LogEntry`](https://docs.cloud.google.com/logging/docs/reference/v2/rest/v2/LogEntry?hl=zh-tw) 結構。這個結構包含記錄名稱、產生記錄項目的資源、時間戳記 (世界標準時間) 和其他基本資訊。

記錄事件的詳細資料包含在名為「*payload*」的子欄位中。如果是稽核記錄，酬載欄位名稱為 `protoPayload`。這個欄位的值是 [`AuditLog`](https://docs.cloud.google.com/logging/docs/reference/audit/auditlog/rest/Shared.Types/AuditLog?hl=zh-tw) 結構，由 `protoPayload.@type` 欄位的值表示，設為 `type.googleapis.com/google.cloud.audit.AuditLog`。

對於資料集、資料表和工作的作業，BigQuery 會以兩種不同格式寫入稽核記錄，但兩者都共用 `AuditLog` 基本類型。

舊格式：

* `resource.type` 欄位為 `bigquery_resource`。
* 作業的詳細資料會寫入 `protoPayload.serviceData` 欄位。這個欄位的值是 [`AuditData`](https://docs.cloud.google.com/bigquery/docs/reference/auditlogs/rest/Shared.Types/AuditData?hl=zh-tw) 結構。

新格式：

* `resource.type` 欄位為 `bigquery_project` 或 `bigquery_dataset`。`bigquery_project` 資源包含工作相關記錄項目，`bigquery_dataset` 資源則包含儲存空間相關記錄項目。
* 作業的詳細資料會寫入 `protoPayload.metadata` 欄位。這個欄位的值是 [`BigQueryAuditMetadata`](https://docs.cloud.google.com/bigquery/docs/reference/auditlogs/rest/Shared.Types/BigQueryAuditMetadata?hl=zh-tw) 結構。

建議您使用新格式的記錄。詳情請參閱[稽核記錄遷移指南](https://docs.cloud.google.com/bigquery/docs/reference/auditlogs/migration?hl=zh-tw)。

以下是顯示失敗作業的記錄項目簡短範例：

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

如果是 BigQuery Reservations 的作業，`protoPayload` 是 [`AuditLog`](https://docs.cloud.google.com/logging/docs/reference/audit/auditlog/rest/Shared.Types/AuditLog?hl=zh-tw) 結構，而 `protoPayload.request` 和 `protoPayload.response` 欄位則包含更多資訊。您可以在 [BigQuery Reservation API](https://docs.cloud.google.com/bigquery/docs/reference/reservations/rpc?hl=zh-tw) 中找到欄位定義。詳情請參閱「[監控 BigQuery 預留項目](https://docs.cloud.google.com/bigquery/docs/reservations-monitoring?hl=zh-tw)」。

## BigQuery 資訊結構定義檢視表

[資訊結構定義檢視表](https://docs.cloud.google.com/bigquery/docs/information-schema-intro?hl=zh-tw)是 BigQuery 的另一項洞察資訊來源，可與指標和記錄搭配使用。

這些檢視表包含工作、資料集、資料表和其他 BigQuery 實體的中繼資料。舉例來說，您可以取得即時中繼資料，瞭解在指定時間範圍內執行的 BigQuery 工作，然後依專案、使用者、參照的資料表和其他維度，將結果分組或篩選。

您可以使用這項資訊，對 BigQuery 工作負載執行更詳細的分析，並回答下列問題：

* 在過去 7 天內，特定專案所有查詢的平均運算單元使用率為何？
* 哪些使用者為特定專案提交了批次載入工作？
* 過去 30 分鐘內發生了哪些串流錯誤 (依錯誤代碼分組)？

特別是[工作中繼資料](https://docs.cloud.google.com/bigquery/docs/information-schema-jobs?hl=zh-tw)、[串流中繼資料](https://docs.cloud.google.com/bigquery/docs/information-schema-streaming?hl=zh-tw)和[預留項目中繼資料](https://docs.cloud.google.com/bigquery/docs/information-schema-reservations?hl=zh-tw)，可讓您深入瞭解 BigQuery 工作負載的效能。

您可以在 [GitHub 上找到資訊結構定義查詢範例](https://github.com/GoogleCloudPlatform/bigquery-utils/tree/master/dashboards/system_tables)，其中顯示組織的運算單元和預留項目使用率、工作執行情形和工作錯誤。舉例來說，下列查詢會提供待處理或執行中的查詢清單。這些查詢會依據在 `us` 區域建立後經過的時間長度排序：

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

除了自行編寫查詢，您也可以在 Google Cloud 控制台使用 BigQuery 監控工具：

* **[監控健康狀態、資源使用率和工作](https://docs.cloud.google.com/bigquery/docs/admin-resource-charts?hl=zh-tw)**。
  查看作業健康狀態資訊主頁和 BigQuery 管理員資源圖表，追蹤整個組織和預留項目的運算單元用量、工作並行數量和工作執行時間。
* **[監控工作](https://docs.cloud.google.com/bigquery/docs/admin-jobs-explorer?hl=zh-tw)。**搜尋、篩選及分組整個組織的個別查詢執行作業，檢查查詢執行圖、找出主要運算單元使用者，以及排解有問題的工作。

## 遙測地圖

下表將 BigQuery 功能和資源對應至其作業監控遙測、受稽核的 API 服務和資源，以及稽核記錄參考文件。您可以使用這項功能，找出疑難排解、最佳化效能、控管成本、稽核用量及維持法規遵循所需的遙測資料。

許多 Google Cloud 服務會將作業工作記錄寫入 [Cloud Logging](https://docs.cloud.google.com/logging/docs?hl=zh-tw)，但 BigQuery 會將作業工作遙測資料寫入[資訊結構定義檢視表](https://docs.cloud.google.com/bigquery/docs/information-schema-intro?hl=zh-tw)，例如 [`INFORMATION_SCHEMA.JOBS`](https://docs.cloud.google.com/bigquery/docs/information-schema-jobs?hl=zh-tw)。這些檢視表會擷取查詢執行階段、運算單元用量、計費位元組數，以及所有提交的工作，包括進行中和失敗的工作。

BigQuery 主要使用 Logging 發出 [Cloud 稽核記錄](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw)，記錄管理和資料存取活動。稽核這項活動時，您可以判斷誰在何時何地存取資源或資料。

系統不會針對每項工作中斷或失敗事件發出稽核記錄。舉例來說，失敗的工作不會產生 `TableDataRead` 或 `TableDataChange` 事件，而 `jobCompletedEvent` 只會記錄成功完成的工作。如要進一步瞭解不會產生稽核記錄的情境，請參閱 [BigQuery 稽核記錄總覽](https://docs.cloud.google.com/bigquery/docs/reference/auditlogs?hl=zh-tw)中的「[資料存取](https://docs.cloud.google.com/bigquery/docs/reference/auditlogs?hl=zh-tw#data_access)」一節。

在下表中，`INFORMATION_SCHEMA` 檢視畫面名稱中的星號 (`*`) 表示特定範圍的檢視畫面變體，例如 `_BY_PROJECT`、`_BY_USER`、`_BY_FOLDER` 和 `_BY_ORGANIZATION`。

| 功能或資源 | 作業監控 | Cloud 稽核記錄 |
| --- | --- | --- |
| 查詢和工作 | **資訊結構定義檢視表：**   * [`JOBS*`](https://docs.cloud.google.com/bigquery/docs/information-schema-jobs?hl=zh-tw)：即時和歷來工作執行、運算單元毫秒、計費位元組、執行階段，以及所有提交的工作 (無論完成狀態為何) * [`JOBS_TIMELINE*`](https://docs.cloud.google.com/bigquery/docs/information-schema-jobs-timeline?hl=zh-tw)：每個時間片段的工作狀態和運算單元用量   **控制台：**   * Google Cloud 控制台中的[工作探索工具](https://docs.cloud.google.com/bigquery/docs/admin-jobs-explorer?hl=zh-tw) * [管理資源圖表](https://docs.cloud.google.com/bigquery/docs/admin-resource-charts?hl=zh-tw)   **指標：**[Cloud Monitoring 指標](https://docs.cloud.google.com/monitoring/api/metrics_gcp_a_b?hl=zh-tw#gcp-bigquery)，例如 `query/count`、`query/execution_times` 和 `job/num_in_flight`。 | **API 服務：**`bigquery.googleapis.com`。  **已稽核的資源：**`JobService` 中的工作 (受監控資源：`bigquery_project`)。  **稽核記錄：**使用 [`BigQueryAuditMetadata`](https://docs.cloud.google.com/bigquery/docs/reference/auditlogs/rest/Shared.Types/BigQueryAuditMetadata?hl=zh-tw) (`JobInsertion` 和 `JobChange` 事件) 的資料存取記錄，記錄提交或取消工作的使用者、工作狀態、陳述式類型，以及參照的資料表或檢視表。請參閱「[BigQuery 稽核記錄總覽](https://docs.cloud.google.com/bigquery/docs/reference/auditlogs?hl=zh-tw#data_access)」。 |
| 資料表和檢視表 | **資訊結構定義檢視表：**   * [`TABLES`](https://docs.cloud.google.com/bigquery/docs/information-schema-tables?hl=zh-tw)：資料表中繼資料 * [`VIEWS`](https://docs.cloud.google.com/bigquery/docs/information-schema-views?hl=zh-tw)：檢視定義和中繼資料 * [`TABLE_STORAGE*`](https://docs.cloud.google.com/bigquery/docs/information-schema-table-storage?hl=zh-tw)：邏輯和實體位元組，以及儲存空間計費 * [`PARTITIONS`](https://docs.cloud.google.com/bigquery/docs/information-schema-partitions?hl=zh-tw)：分區資料列數和儲存空間大小 * [`STREAMING_TIMELINE*`](https://docs.cloud.google.com/bigquery/docs/information-schema-streaming?hl=zh-tw)：串流資料即時插入處理量和錯誤 * [`WRITE_API_TIMELINE*`](https://docs.cloud.google.com/bigquery/docs/information-schema-write-api?hl=zh-tw)：寫入串流處理量和錯誤   **指標：**[Monitoring 指標](https://docs.cloud.google.com/monitoring/api/metrics_gcp_a_b?hl=zh-tw#gcp-bigquery)，例如 `storage/stored_bytes` 和 `storage/table_count`。 | **API 服務：**`bigquery.googleapis.com` 和 `bigquerystorage.googleapis.com`。BigQuery Storage API 的資料存取記錄會使用 `bigquery.googleapis.com`，而政策遭拒記錄則會使用 `bigquerystorage.googleapis.com`。  **稽核的資源：**`TableService` 和 `TableDataService` 中的資料表、檢視表和 materialized view；以及 `BigQueryRead` 和 `BigQueryWrite` 中的儲存空間讀取工作階段和寫入串流 (受監控資源：`bigquery_dataset` 和 `bigquery_table`)。  **稽核記錄：**使用 `BigQueryAuditMetadata` 的資料存取記錄 (`TableDataRead` 和 `TableDataChange` 事件，用於資料表讀取、修改、參照欄位、來源工作，以及 BigQuery Storage API 串流讀取和寫入)，以及 `TableCreation`、`TableChange` 和 `TableDeletion` 事件的管理員活動、資料存取和系統事件記錄，包括資料表 Identity and Access Management (IAM) 政策變更和資料表到期。請參閱「[BigQuery 稽核記錄總覽](https://docs.cloud.google.com/bigquery/docs/reference/auditlogs?hl=zh-tw)」。 |
| 資料集 | **資訊結構定義檢視表：**   * [`SCHEMATA`](https://docs.cloud.google.com/bigquery/docs/information-schema-datasets-schemata?hl=zh-tw)：資料集中繼資料和預設到期時間 * [`SCHEMATA_OPTIONS`](https://docs.cloud.google.com/bigquery/docs/information-schema-datasets-schemata-options?hl=zh-tw)：資料集選項和標籤 * [`SCHEMATA_REPLICAS`](https://docs.cloud.google.com/bigquery/docs/information-schema-schemata-replicas?hl=zh-tw)：跨區域複製功能狀態 | **API 服務：**`bigquery.googleapis.com`。  **受稽核資源：**`DatasetService` 和 `IAMPolicy` 中的資料集、資料集 IAM 政策和資料集 ACL (受監控資源：`bigquery_dataset`)。  **稽核記錄：**使用 `BigQueryAuditMetadata` (`DatasetCreation`、`DatasetChange` 和 `DatasetDeletion` 事件) 的管理員活動和資料存取記錄，包括 `bindingDeltas` 中的資料集 IAM 政策變更，以及 `accessChanges` 中的 ACL 更新。請參閱「[BigQuery 稽核記錄總覽](https://docs.cloud.google.com/bigquery/docs/reference/auditlogs?hl=zh-tw)」。 |
| 運算單元和預留項目 | **資訊結構定義檢視表：**   * [`RESERVATIONS*`](https://docs.cloud.google.com/bigquery/docs/information-schema-reservations?hl=zh-tw)：目前的預留項目設定 * [`RESERVATIONS_TIMELINE*`](https://docs.cloud.google.com/bigquery/docs/information-schema-reservation-timeline?hl=zh-tw)：每分鐘預留中繼資料和自動調度資源詳細資料 * [`ASSIGNMENTS*`](https://docs.cloud.google.com/bigquery/docs/information-schema-assignments?hl=zh-tw)：專案、資料夾和組織指派作業 * [`CAPACITY_COMMITMENTS*`](https://docs.cloud.google.com/bigquery/docs/information-schema-capacity-commitments?hl=zh-tw)：運算單元容量承諾使用合約   **控制台：**   * Google Cloud 控制台中的[管理資源圖表](https://docs.cloud.google.com/bigquery/docs/admin-resource-charts?hl=zh-tw) * [運算單元估算器](https://docs.cloud.google.com/bigquery/docs/slot-estimator?hl=zh-tw)   **指標：**[Monitoring 指標](https://docs.cloud.google.com/bigquery/docs/reservations-monitoring?hl=zh-tw)，例如 `slots/allocated` 和 `slots/total_available`。 | **API 服務：**BigQuery Reservation API 的 `bigqueryreservation.googleapis.com`。  **稽核的資源：**`ReservationService` 中的預留項目、容量承諾和預留項目指派作業 (受監控資源：`bigquery_project`)。  **稽核記錄：**管理員活動和資料存取記錄，用於建立、修改、刪除及列出預留項目、容量承諾使用合約，以及專案或資料夾指派作業。請參閱「[BigQuery Reservation API 稽核記錄](https://docs.cloud.google.com/bigquery/docs/reference/auditlogs/index-reservation?hl=zh-tw)」。 |
| 資料欄層級安全防護機制和資料遮蓋 | **資訊結構定義檢視表：**   * [`COLUMN_FIELD_PATHS`](https://docs.cloud.google.com/bigquery/docs/information-schema-column-field-paths?hl=zh-tw)：巢狀資料欄路徑、政策標記和資料政策指派 * [`COLUMNS`](https://docs.cloud.google.com/bigquery/docs/information-schema-columns?hl=zh-tw)：資料欄結構定義和資料類型 | **API 服務：**`datacatalog.googleapis.com` (用於 Data Catalog 政策標記)、`bigquerydatapolicy.googleapis.com` (用於 BigQuery Data Policy API) 和 `bigquery.googleapis.com`。  **稽核的資源：**`PolicyTagManager` 中的分類和政策標記、`DataPolicyService` 中的資料政策，以及已加上政策標記的資料表資料欄 (受監控資源：`audited_resource` 和 `bigquery_dataset`)。  **稽核記錄：**管理員活動和資料存取記錄，用於分類和政策標記管理，以及 IAM 政策變更 ([稽核政策標記](https://docs.cloud.google.com/bigquery/docs/auditing-policy-tags?hl=zh-tw))；資料政策管理和被授權人更新 ([BigQuery 資料政策稽核記錄](https://docs.cloud.google.com/bigquery/docs/column-data-masking-audit-logging?hl=zh-tw))；以及受保護資料欄讀取作業的 `TableDataRead.fields` 記錄 ([BigQuery 稽核記錄總覽](https://docs.cloud.google.com/bigquery/docs/reference/auditlogs?hl=zh-tw))。 |
| 常式，包括 UDF 和預存程序 | **資訊結構定義檢視表：**   * [`ROUTINES`](https://docs.cloud.google.com/bigquery/docs/information-schema-routines?hl=zh-tw)：常式定義和中繼資料 * [`ROUTINE_OPTIONS`](https://docs.cloud.google.com/bigquery/docs/information-schema-routine-options?hl=zh-tw)：日常安排選項 * [`PARAMETERS`](https://docs.cloud.google.com/bigquery/docs/information-schema-parameters?hl=zh-tw)：常式輸入和輸出參數 * [`JOBS*`](https://docs.cloud.google.com/bigquery/docs/information-schema-jobs?hl=zh-tw)：常式執行工作 | **API 服務：**`bigquery.googleapis.com`。  **稽核的資源：**`RoutineService` 中的使用者定義函式 (UDF)、資料表函式和預存程序 (受監控資源：`bigquery_dataset` 和 `bigquery_project`)。  **稽核記錄：**使用 `BigQueryAuditMetadata` 的管理員活動和資料存取記錄 (`RoutineCreation`、`RoutineChange` 和 `RoutineDeletion` 事件)，以及預存程序執行的子工作事件。請參閱「[BigQuery 稽核記錄總覽](https://docs.cloud.google.com/bigquery/docs/reference/auditlogs?hl=zh-tw)」。 |
| 外部連線 | **資訊結構定義檢視表：**   * [`OBJECT_PRIVILEGES`](https://docs.cloud.google.com/bigquery/docs/information-schema-object-privileges?hl=zh-tw)：連線權限 * [`JOBS*`](https://docs.cloud.google.com/bigquery/docs/information-schema-jobs?hl=zh-tw)：使用連線的聯合查詢和遠端函式工作 | **API 服務：**BigQuery Connection API 的 `bigqueryconnection.googleapis.com`。  **稽核的資源：**`ConnectionService` 中的連線和連線 IAM 政策 (受監控資源：`audited_resource`)。  **稽核記錄：**管理員活動和資料存取記錄，用於連線建立、憑證更新、刪除、列出和 IAM 政策變更。請參閱「[BigQuery Connection API 稽核記錄](https://docs.cloud.google.com/bigquery/docs/reference/auditlogs/index-connection?hl=zh-tw)」。 |
| BigQuery sharing | **資訊結構定義檢視表：**   * [`SHARED_DATASET_USAGE`](https://docs.cloud.google.com/bigquery/docs/information-schema-shared-dataset-usage?hl=zh-tw)：訂閱者對共用資料集資料表的使用情形 * [`SCHEMATA_LINKS`](https://docs.cloud.google.com/bigquery/docs/information-schema-datasets-schemata-links?hl=zh-tw)：連結的資料集和共用資源   **資訊主頁：**[共用使用情形指標資訊主頁](https://docs.cloud.google.com/bigquery/docs/analytics-hub-monitor-listings?hl=zh-tw)。 | **API 服務：**`analyticshub.googleapis.com`。  **稽核的資源：**`AnalyticsHubService` 中的資料交換、清單、訂閱項目，以及交換或清單 IAM 政策 (受監控資源：`audited_resource`)。  **稽核記錄：**管理員活動和資料存取記錄，用於資料交換和建立、更新、刪除、IAM 政策變更和訂閱者作業。請參閱「[共用稽核記錄](https://docs.cloud.google.com/bigquery/docs/analytics-hub-audit-logging?hl=zh-tw)」。 |
| BigQuery 資料移轉服務 | **指標和記錄：**   * [監控移轉指標](https://docs.cloud.google.com/bigquery/docs/dts-monitor?hl=zh-tw) * Logging 中的作業移轉執行作業記錄，位於 `resource.type="bigquery_dts_config"` | **API 服務：**BigQuery 資料移轉服務 API 的 `bigquerydatatransfer.googleapis.com`。  **稽核的資源：**`DataTransferService` 中的移轉設定、移轉執行作業和資料來源 (受監控資源：`audited_resource`)。  **稽核記錄：**管理員活動和資料存取記錄，用於建立、更新、刪除、列出及啟動移轉設定和執行作業。請參閱「[BigQuery 資料移轉服務稽核記錄](https://docs.cloud.google.com/bigquery/docs/audit-logging?hl=zh-tw)」。 |
| BigLake 目錄和資料表 | **資訊結構定義檢視表：**   * [`TABLES`](https://docs.cloud.google.com/bigquery/docs/information-schema-tables?hl=zh-tw)：資料表中繼資料 * [`JOBS*`](https://docs.cloud.google.com/bigquery/docs/information-schema-jobs?hl=zh-tw)：外部物件儲存庫查詢統計資料 (`metadata_cache_statistics` 和 `object_storage_stats`) | **API 服務：**`biglake.googleapis.com` 和 `bigquery.googleapis.com`。  **稽核的資源：**`MetastoreService` 和 `HiveMetastoreService` 中的 metastore 目錄、資料庫、資料表和分區，以及 `IcebergCatalogService` 中的 Apache Iceberg 目錄、命名空間和資料表 (受監控資源：`audited_resource` 和 `bigquery_dataset`)。  **稽核記錄：**目錄、資料庫、命名空間、資料表、分區和目錄 IAM 政策作業的管理員活動和資料存取記錄。請參閱「[BigLake 稽核記錄](https://docs.cloud.google.com/bigquery/docs/biglake-audit-logging?hl=zh-tw)」。 |
| BigQuery 遷移服務 | **狀態和報表：**   * Google Cloud 控制台中的[批次 SQL 轉譯](https://docs.cloud.google.com/bigquery/docs/batch-sql-translator?hl=zh-tw)工作狀態 * BigQuery Migration API 中的工作流程和子工作狀態 * Cloud Storage 中的翻譯摘要報表 | **API 服務：**`bigquerymigration.googleapis.com` (適用於 BigQuery Migration API)。  **稽核的資源：**`MigrationService` 和 `SqlTranslationService` 中的遷移工作流程、遷移子工作和 SQL 轉譯要求 (受監控資源：`audited_resource`)。  **稽核記錄：**資料存取記錄，用於建立、啟動、列出、查看及刪除遷移工作流程和子工作，以及轉譯 SQL 查詢。請參閱「[BigQuery Migration Service 稽核記錄](https://docs.cloud.google.com/bigquery/docs/reference/auditlogs/audit-logging-bq-migration?hl=zh-tw)」。 |

## 後續步驟

* 瞭解如何[使用工作探索工具監控及篩選工作](https://docs.cloud.google.com/bigquery/docs/admin-jobs-explorer?hl=zh-tw)。
* 瞭解如何[監控健康狀態和資源使用率](https://docs.cloud.google.com/bigquery/docs/admin-resource-charts?hl=zh-tw)。
* 瞭解如何[建立 BigQuery 圖表和快訊](https://docs.cloud.google.com/bigquery/docs/monitoring-dashboard?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-11-05 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-11-05 (世界標準時間)。"],[],[]]