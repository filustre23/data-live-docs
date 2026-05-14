Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# BigQuery 資料移轉服務稽核記錄

本文說明 BigQuery 資料移轉服務的稽核記錄。 Google Cloud 服務會產生稽核記錄，記錄資源中的管理和存取活動。 Google Cloud 如要進一步瞭解 Cloud 稽核記錄，請參閱下列文章：

* [稽核記錄類型](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#types)
* [稽核記錄項目結構](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#audit_log_entry_structure)
* [儲存及轉送稽核記錄](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#storing_and_routing_audit_logs)
* [Cloud Logging 定價摘要](https://docs.cloud.google.com/stackdriver/pricing?hl=zh-tw#logs-pricing-summary)
* [啟用資料存取稽核記錄](https://docs.cloud.google.com/logging/docs/audit/configure-data-access?hl=zh-tw)

## 服務名稱

BigQuery 資料移轉服務稽核記錄會使用服務名稱 `bigquerydatatransfer.googleapis.com`。篩選這項服務：

```
    protoPayload.serviceName="bigquerydatatransfer.googleapis.com"
```

## 依權限類型劃分的方法

每個 IAM 權限都有 `type` 屬性，其值為列舉，可以是下列四個值之一：`ADMIN_READ`、`ADMIN_WRITE`、`DATA_READ` 或 `DATA_WRITE`。呼叫方法時，BigQuery 資料移轉服務會產生稽核記錄，記錄的類別取決於執行方法所需權限的 `type` 屬性。如果方法需要 IAM 權限，且 `type` 屬性值為 `DATA_READ`、`DATA_WRITE` 或 `ADMIN_READ`，就會產生「資料存取」稽核記錄。需要 IAM 權限且 `type` 屬性值為 `ADMIN_WRITE` 的方法，會產生[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)稽核記錄。

下列清單中標示 (LRO) 的 API 方法，都是長時間執行的作業 (LRO)。這些方法通常會產生兩筆稽核記錄項目：一筆是在作業開始時產生，另一筆則是在作業結束時產生。詳情請參閱[長時間執行的作業的稽核記錄](https://docs.cloud.google.com/logging/docs/audit/understanding-audit-logs?hl=zh-tw#lro)。

| 權限類型 | 方法 |
| --- | --- |
| `ADMIN_READ` | `google.cloud.bigquery.datatransfer.v1.DataTransferService.CheckValidCreds` `google.cloud.bigquery.datatransfer.v1.DataTransferService.GetDataSource` `google.cloud.bigquery.datatransfer.v1.DataTransferService.GetTransferConfig` `google.cloud.bigquery.datatransfer.v1.DataTransferService.GetTransferRun` `google.cloud.bigquery.datatransfer.v1.DataTransferService.ListDataSources` `google.cloud.bigquery.datatransfer.v1.DataTransferService.ListTransferConfigs` `google.cloud.bigquery.datatransfer.v1.DataTransferService.ListTransferLogs` `google.cloud.bigquery.datatransfer.v1.DataTransferService.ListTransferRuns` `google.cloud.location.Locations.GetLocation` `google.cloud.location.Locations.ListLocations` |
| `ADMIN_WRITE` | `google.cloud.bigquery.datatransfer.v1.DataTransferService.CreateTransferConfig` `google.cloud.bigquery.datatransfer.v1.DataTransferService.DeleteTransferConfig` `google.cloud.bigquery.datatransfer.v1.DataTransferService.DeleteTransferRun` `google.cloud.bigquery.datatransfer.v1.DataTransferService.EnrollDataSources` `google.cloud.bigquery.datatransfer.v1.DataTransferService.ScheduleTransferRuns` `google.cloud.bigquery.datatransfer.v1.DataTransferService.StartManualTransferRuns` `google.cloud.bigquery.datatransfer.v1.DataTransferService.UnenrollDataSources` `google.cloud.bigquery.datatransfer.v1.DataTransferService.UpdateTransferConfig` |

## API 介面稽核記錄

如要瞭解系統如何評估每種方法的權限，請參閱 BigQuery 資料移轉服務的 Identity and Access Management 說明文件。

### `google.cloud.bigquery.datatransfer.v1.DataTransferService`

下列稽核記錄與屬於 `google.cloud.bigquery.datatransfer.v1.DataTransferService` 的方法相關聯。

#### `CheckValidCreds`

* **方法**：`google.cloud.bigquery.datatransfer.v1.DataTransferService.CheckValidCreds`
* **稽核記錄類型**：[資料存取](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#data-access)
* **權限**：
  + `bigquery.transfers.get - ADMIN_READ`
* **方法是長時間執行的作業或串流作業**：
  否。
* **篩選這個方法**：`protoPayload.methodName="google.cloud.bigquery.datatransfer.v1.DataTransferService.CheckValidCreds"`

#### `CreateTransferConfig`

* **方法**：`google.cloud.bigquery.datatransfer.v1.DataTransferService.CreateTransferConfig`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `bigquery.transfers.update - ADMIN_WRITE`
* **方法是長時間執行的作業或串流作業**：
  否。
* **篩選這個方法**：`protoPayload.methodName="google.cloud.bigquery.datatransfer.v1.DataTransferService.CreateTransferConfig"`

#### `DeleteTransferConfig`

* **方法**：`google.cloud.bigquery.datatransfer.v1.DataTransferService.DeleteTransferConfig`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `bigquery.transfers.update - ADMIN_WRITE`
* **方法是長時間執行的作業或串流作業**：
  否。
* **篩選這個方法**：`protoPayload.methodName="google.cloud.bigquery.datatransfer.v1.DataTransferService.DeleteTransferConfig"`

#### `DeleteTransferRun`

* **方法**：`google.cloud.bigquery.datatransfer.v1.DataTransferService.DeleteTransferRun`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `bigquery.transfers.update - ADMIN_WRITE`
* **方法是長時間執行的作業或串流作業**：
  否。
* **篩選這個方法**：`protoPayload.methodName="google.cloud.bigquery.datatransfer.v1.DataTransferService.DeleteTransferRun"`

#### `EnrollDataSources`

* **方法**：`google.cloud.bigquery.datatransfer.v1.DataTransferService.EnrollDataSources`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `resourcemanager.projects.update - ADMIN_WRITE`
* **方法是長時間執行的作業或串流作業**：
  否。
* **篩選這個方法**：`protoPayload.methodName="google.cloud.bigquery.datatransfer.v1.DataTransferService.EnrollDataSources"`

#### `GetDataSource`

* **方法**：`google.cloud.bigquery.datatransfer.v1.DataTransferService.GetDataSource`
* **稽核記錄類型**：[資料存取](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#data-access)
* **權限**：
  + `bigquery.transfers.get - ADMIN_READ`
* **方法是長時間執行的作業或串流作業**：
  否。
* **篩選這個方法**：`protoPayload.methodName="google.cloud.bigquery.datatransfer.v1.DataTransferService.GetDataSource"`

#### `GetTransferConfig`

* **方法**：`google.cloud.bigquery.datatransfer.v1.DataTransferService.GetTransferConfig`
* **稽核記錄類型**：[資料存取](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#data-access)
* **權限**：
  + `bigquery.transfers.get - ADMIN_READ`
* **方法是長時間執行的作業或串流作業**：
  否。
* **篩選這個方法**：`protoPayload.methodName="google.cloud.bigquery.datatransfer.v1.DataTransferService.GetTransferConfig"`

#### `GetTransferRun`

* **方法**：`google.cloud.bigquery.datatransfer.v1.DataTransferService.GetTransferRun`
* **稽核記錄類型**：[資料存取](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#data-access)
* **權限**：
  + `bigquery.transfers.get - ADMIN_READ`
* **方法是長時間執行的作業或串流作業**：
  否。
* **篩選這個方法**：`protoPayload.methodName="google.cloud.bigquery.datatransfer.v1.DataTransferService.GetTransferRun"`

#### `ListDataSources`

* **方法**：`google.cloud.bigquery.datatransfer.v1.DataTransferService.ListDataSources`
* **稽核記錄類型**：[資料存取](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#data-access)
* **權限**：
  + `bigquery.transfers.get - ADMIN_READ`
* **方法是長時間執行的作業或串流作業**：
  否。
* **篩選這個方法**：`protoPayload.methodName="google.cloud.bigquery.datatransfer.v1.DataTransferService.ListDataSources"`

#### `ListTransferConfigs`

* **方法**：`google.cloud.bigquery.datatransfer.v1.DataTransferService.ListTransferConfigs`
* **稽核記錄類型**：[資料存取](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#data-access)
* **權限**：
  + `bigquery.transfers.get - ADMIN_READ`
* **方法是長時間執行的作業或串流作業**：
  否。
* **篩選這個方法**：`protoPayload.methodName="google.cloud.bigquery.datatransfer.v1.DataTransferService.ListTransferConfigs"`

#### `ListTransferLogs`

* **方法**：`google.cloud.bigquery.datatransfer.v1.DataTransferService.ListTransferLogs`
* **稽核記錄類型**：[資料存取](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#data-access)
* **權限**：
  + `bigquery.transfers.get - ADMIN_READ`
* **方法是長時間執行的作業或串流作業**：
  否。
* **篩選這個方法**：`protoPayload.methodName="google.cloud.bigquery.datatransfer.v1.DataTransferService.ListTransferLogs"`

#### `ListTransferRuns`

* **方法**：`google.cloud.bigquery.datatransfer.v1.DataTransferService.ListTransferRuns`
* **稽核記錄類型**：[資料存取](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#data-access)
* **權限**：
  + `bigquery.transfers.get - ADMIN_READ`
* **方法是長時間執行的作業或串流作業**：
  否。
* **篩選這個方法**：`protoPayload.methodName="google.cloud.bigquery.datatransfer.v1.DataTransferService.ListTransferRuns"`

#### `ScheduleTransferRuns`

* **方法**：`google.cloud.bigquery.datatransfer.v1.DataTransferService.ScheduleTransferRuns`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `bigquery.transfers.update - ADMIN_WRITE`
* **方法是長時間執行的作業或串流作業**：
  否。
* **篩選這個方法**：`protoPayload.methodName="google.cloud.bigquery.datatransfer.v1.DataTransferService.ScheduleTransferRuns"`

#### `StartManualTransferRuns`

* **方法**：`google.cloud.bigquery.datatransfer.v1.DataTransferService.StartManualTransferRuns`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `bigquery.transfers.update - ADMIN_WRITE`
* **方法是長時間執行的作業或串流作業**：
  否。
* **篩選這個方法**：`protoPayload.methodName="google.cloud.bigquery.datatransfer.v1.DataTransferService.StartManualTransferRuns"`

#### `UnenrollDataSources`

* **方法**：`google.cloud.bigquery.datatransfer.v1.DataTransferService.UnenrollDataSources`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `resourcemanager.projects.update - ADMIN_WRITE`
* **方法是長時間執行的作業或串流作業**：
  否。
* **篩選這個方法**：`protoPayload.methodName="google.cloud.bigquery.datatransfer.v1.DataTransferService.UnenrollDataSources"`

#### `UpdateTransferConfig`

* **方法**：`google.cloud.bigquery.datatransfer.v1.DataTransferService.UpdateTransferConfig`
* **稽核記錄類型**：[管理員活動](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#admin-activity)
* **權限**：
  + `bigquery.transfers.update - ADMIN_WRITE`
* **方法是長時間執行的作業或串流作業**：
  否。
* **篩選這個方法**：`protoPayload.methodName="google.cloud.bigquery.datatransfer.v1.DataTransferService.UpdateTransferConfig"`

### `google.cloud.location.Locations`

下列稽核記錄與屬於 `google.cloud.location.Locations` 的方法相關聯。

#### `GetLocation`

* **方法**：`google.cloud.location.Locations.GetLocation`
* **稽核記錄類型**：[資料存取](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#data-access)
* **權限**：
  + `bigquery.transfers.get - ADMIN_READ`
* **方法是長時間執行的作業或串流作業**：
  否。
* **篩選這個方法**：`protoPayload.methodName="google.cloud.location.Locations.GetLocation"`

#### `ListLocations`

* **方法**：`google.cloud.location.Locations.ListLocations`
* **稽核記錄類型**：[資料存取](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#data-access)
* **權限**：
  + `bigquery.transfers.get - ADMIN_READ`
* **方法是長時間執行的作業或串流作業**：
  否。
* **篩選這個方法**：`protoPayload.methodName="google.cloud.location.Locations.ListLocations"`




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-14 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-14 (世界標準時間)。"],[],[]]