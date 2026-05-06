Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# BigQuery 稽核記錄簡介

記錄是指系統在回應特定事件或動作時產生的文字記錄。舉例來說，BigQuery 會針對建立或刪除資料表、購買運算單元或執行載入工作等動作建立記錄項目。

Google Cloud 也會寫入記錄，包括稽核記錄，提供與您使用 Google Cloud 服務相關的作業問題洞察資料。如要進一步瞭解 Google Cloud 如何處理記錄，請參閱 [Cloud Logging](https://docs.cloud.google.com/logging/docs?hl=zh-tw) 說明文件和 [Cloud 稽核記錄總覽](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw)。

## 稽核記錄與 `INFORMATION_SCHEMA` 檢視畫面

Google Cloud 專案的稽核記錄僅涵蓋直接隸屬於 Google Cloud 專案的資源。資料夾、機構和帳單帳戶等其他 Google Cloud 資源則各有其專屬的稽核記錄。

稽核記錄可協助您瞭解 Google Cloud 資源中有關「人事時地」的問題。稽核記錄是使用者系統活動和存取模式的確切資訊來源，應是稽核或安全性問題的主要來源。

BigQuery 中的 [`INFORMATION_SCHEMA`](https://docs.cloud.google.com/bigquery/docs/information-schema-intro?hl=zh-tw) 檢視表是另一個可用來取得洞察資訊的來源，可與指標和記錄搭配使用。這些檢視畫面包含工作、資料集、資料表和其他 BigQuery 實體的中繼資料。舉例來說，您可以取得即時中繼資料，瞭解在指定時間內執行哪些 BigQuery 工作。接著，您可以依專案、使用者、參照的資料表和其他維度來分組或篩選結果。

`INFORMATION_SCHEMA` 檢視畫面會提供資訊，協助您更詳細地分析 BigQuery 工作負載，例如：

* 指定專案過去七天內所有查詢的平均運算單元使用率為何？
* 過去 30 分鐘內發生的串流錯誤為何？請依錯誤代碼分組。

BigQuery 稽核記錄包含 API 呼叫的記錄項目，但不會說明 API 呼叫的影響。部分 API 呼叫會建立工作 (例如查詢和載入)，而 `INFORMATION_SCHEMA` 檢視畫面會擷取這些工作的資訊。舉例來說，您可以在 `INFORMATION_SCHEMA` 檢視畫面中查看特定查詢所使用的時間和時段，但稽核記錄中則沒有這類資訊。

如要深入瞭解 BigQuery 工作負載的效能，請參閱[工作中繼資料](https://docs.cloud.google.com/bigquery/docs/information-schema-jobs?hl=zh-tw)、[串流中繼資料](https://docs.cloud.google.com/bigquery/docs/information-schema-streaming?hl=zh-tw)和[預留中繼資料](https://docs.cloud.google.com/bigquery/docs/information-schema-reservations?hl=zh-tw)。

如要進一步瞭解 Google Cloud 服務寫入的稽核記錄類型，請參閱「[稽核記錄類型](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw#types)」。

## 稽核記錄格式

Google Cloud 服務會以結構化 JSON 格式寫入稽核記錄。 Google Cloud 記錄項目的基本資料類型為 [`LogEntry`](https://docs.cloud.google.com/logging/docs/reference/v2/rest/v2/LogEntry?hl=zh-tw) 結構。這個結構體包含記錄名稱、產生記錄項目的資源、時間戳記 (世界標準時間) 和其他基本資訊。

記錄會在稱為「酬載欄位」的子欄位中，加入記錄事件的詳細資料。稽核記錄的酬載欄位名稱為 `protoPayload`。這個欄位的類型 (`protoPayload.@type`) 已設為 `type.googleapis.com/google.cloud.audit.AuditLog`，表示該欄位使用 [`AuditLog`](https://docs.cloud.google.com/logging/docs/reference/audit/auditlog/rest/Shared.Types/AuditLog?hl=zh-tw) 記錄檔結構。

針對資料集、資料表和工作執行的作業，BigQuery 會以兩種不同的格式寫入稽核記錄，但兩種格式都共用 `AuditLog` 基本類型。

舊版格式包含下列欄位和值：

* `resource.type` 欄位的值為 `bigquery_resource`。
* BigQuery 會在 `protoPayload.serviceData` 欄位中寫入作業詳細資料。這個欄位的值會使用 [`AuditData`](https://docs.cloud.google.com/bigquery/docs/reference/auditlogs/rest/Shared.Types/AuditData?hl=zh-tw) 記錄結構。

新格式包含下列欄位和值：

* `resource.type` 欄位的值為 `bigquery_project` 或 `bigquery_dataset`。`bigquery_project` 資源含有工作記錄項目，而 `bigquery_dataset` 資源則含有儲存空間記錄項目。
* BigQuery 會在 `protoPayload.metadata` 欄位中寫入作業詳細資料。這個欄位的值會使用 [`BigQueryAuditMetadata`](https://docs.cloud.google.com/bigquery/docs/reference/auditlogs/rest/Shared.Types/BigQueryAuditMetadata?hl=zh-tw) 結構。

建議您使用較新的格式使用記錄。詳情請參閱「[稽核記錄遷移指南](https://docs.cloud.google.com/bigquery/docs/reference/auditlogs/migration?hl=zh-tw)」。

以下是記錄項目的簡略範例，其中顯示失敗的作業：

```
{
  "protoPayload": {
    "@type": "type.googleapis.com/google.cloud.audit.AuditLog",
    "status": {
      "code": 5,
      "message": "Not found: Dataset myproject:mydataset was not found in location US"
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
  "logName": "projects/myproject/logs/cloudaudit.googleapis.com%2Fdata_access",
  ...
}
```

針對 BigQuery 預留作業，`protoPayload` 欄位會使用 `AuditLog` 結構，而 `protoPayload.request` 和 `protoPayload.response` 欄位則包含更多資訊。您可以在 [BigQuery Reservation API](https://docs.cloud.google.com/bigquery/docs/reference/reservations/rpc?hl=zh-tw) 中找到欄位定義。詳情請參閱「[監控 BigQuery 預留空間](https://docs.cloud.google.com/bigquery/docs/reservations-monitoring?hl=zh-tw)」。

如要進一步瞭解稽核記錄格式，請參閱「[瞭解稽核記錄](https://docs.cloud.google.com/logging/docs/audit/understanding-audit-logs?hl=zh-tw)」。

## 限制

記錄訊息的大小上限為 100,000 位元組。詳情請參閱「[截斷的記錄項目](https://docs.cloud.google.com/bigquery/docs/reference/auditlogs?hl=zh-tw#truncated_log_entry)」。

## 瀏覽權限和存取權控管

BigQuery 稽核記錄可能包含使用者認為機密的資訊，例如 SQL 文字、結構定義，以及資料表和資料集等資源的 ID。如要進一步瞭解如何管理這類資訊的存取權，請參閱 Cloud Logging 的[存取權控管說明文件](https://docs.cloud.google.com/logging/docs/access-control?hl=zh-tw)。

## 後續步驟

* 如要瞭解如何使用 Cloud Logging 稽核與政策標記相關的活動，請參閱「[稽核政策標記](https://docs.cloud.google.com/bigquery/docs/auditing-policy-tags?hl=zh-tw)」。
* 如要瞭解如何使用 BigQuery 分析記錄的活動，請參閱「[BigQuery 稽核記錄總覽](https://docs.cloud.google.com/bigquery/docs/reference/auditlogs?hl=zh-tw)」。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-02 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-02 (世界標準時間)。"],[],[]]