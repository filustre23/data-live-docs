Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 錯誤訊息

本文說明使用 BigQuery 時可能遇到的錯誤訊息，包括 HTTP 錯誤代碼和建議的疑難排解步驟。

如要進一步瞭解查詢錯誤，請參閱「[排解查詢錯誤](https://docs.cloud.google.com/bigquery/docs/troubleshoot-queries?hl=zh-tw)」。

如要進一步瞭解串流資料即時插入錯誤，請參閱「[排解串流資料即時插入問題](https://docs.cloud.google.com/bigquery/docs/streaming-data-into-bigquery?hl=zh-tw#troubleshooting)」。

## 錯誤表格

BigQuery API 的回應包含 HTTP 錯誤代碼，以及回應主體中的錯誤物件。錯誤物件通常是下列其中一種：

* [`errors` 物件](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#jobstatus)，其中包含 [`ErrorProto` 物件](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/ErrorProto?hl=zh-tw)陣列。
* [`errorResults` 物件](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#jobstatus)，其中包含單一 [`ErrorProto` 物件](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/ErrorProto?hl=zh-tw)。

下表中的「錯誤訊息」欄會對應至 `ErrorProto` 物件中的 `reason` 屬性。

表格並未列出所有可能的 HTTP 錯誤或其他網路錯誤。
因此，請勿假設 BigQuery 的每個錯誤回應中都有錯誤物件。此外，如果您使用 BigQuery API 的 Cloud 用戶端程式庫，可能會收到不同的錯誤或錯誤物件。詳情請參閱「[BigQuery API 用戶端程式庫](https://docs.cloud.google.com/bigquery/docs/reference/libraries?hl=zh-tw)」。

如果您收到的 HTTP 回應代碼未列在下表中，則表示 HTTP 要求有問題或預期結果。`5xx` 範圍內的回應代碼表示伺服器端錯誤。如果收到 `5xx` 回應代碼，請稍後再重試要求。在某些情況下，`5xx` 回應代碼可能會由 Proxy 等中介伺服器傳回。請查看回應主體和回應標頭，瞭解錯誤詳情。如需 HTTP 回應代碼的完整清單，請參閱「[HTTP 回應代碼](https://en.wikipedia.org/wiki/HTTP_response_codes)」。

如果您使用 [bq 指令列工具](https://docs.cloud.google.com/bigquery/bq-command-line-tool?hl=zh-tw)檢查工作狀態，系統預設不會傳回錯誤物件。如要查看錯誤物件和對應至下表的 `reason` 屬性，請使用 `--format=prettyjson` 旗標。例如：`bq --format=prettyjson show -j
*<job id>*`。如要查看 bq 工具的詳細記錄，請使用 `--apilog=stdout`。如要進一步瞭解如何排解 bq 工具的問題，請參閱「[偵錯](https://docs.cloud.google.com/bigquery/docs/bq-command-line-tool?hl=zh-tw#debugging)」。

| 錯誤訊息 | HTTP 代碼 | 說明 | 疑難排解 |
| --- | --- | --- | --- |
| accessDenied | 403 | 如果您嘗試存取沒有權限的資源，例如[資料集](https://docs.cloud.google.com/bigquery/docs/datasets?hl=zh-tw)、[資料表](https://docs.cloud.google.com/bigquery/docs/tables?hl=zh-tw)、[檢視表](https://docs.cloud.google.com/bigquery/docs/views-intro?hl=zh-tw)或[工作](https://docs.cloud.google.com/bigquery/docs/managing-jobs?hl=zh-tw)，就會傳回這項錯誤。如果您嘗試修改唯讀物件，也會傳回這個錯誤。 | 請與資源擁有者聯絡，並[要求資源存取權](https://docs.cloud.google.com/bigquery/access-control?hl=zh-tw)，授予錯誤稽核記錄中 `principalEmail` 值所識別的使用者。 |
| attributeError | 400 | 如果使用者程式碼發生問題，呼叫了不存在的特定物件屬性，就會傳回這項錯誤。 | 請確認您使用的物件具有您嘗試存取的屬性。如要進一步瞭解這項錯誤，請參閱「[AttributeError](https://docs.python.org/3/library/exceptions.html#AttributeError)」。 |
| backendError | 500、502、503 或 504 | 這項錯誤表示服務目前無法使用。這可能是由多種暫時性問題造成，包括：   * **服務需求激增**：需求突然激增 (例如尖峰使用時段)，可能會導致負載降低，以保護所有 BigQuery 使用者的服務品質。為避免系統不堪負荷，BigQuery 可能會針對一小部分要求傳回 500 或 503 錯誤。 * **網路問題**：BigQuery 採用分散式架構，因此資料經常在系統中的不同元件或機器之間傳輸。各種間歇性網路連線問題都可能導致 BigQuery 傳回 5xx 錯誤，包括 SSL 握手失敗，或使用者與Google Cloud之間的其他網路基礎架構問題。 * **資源耗盡**：BigQuery 設有多項內部資源限制，可防止單一使用者或單一工作耗用過多資源，進而保護整體服務效能。BigQuery 會實施卸載機制，解決資源耗盡的問題。 * **後端錯誤**：在極少數情況下，其中一個 BigQuery 元件發生內部問題，可能會導致系統向用戶端傳回 500 或 503 錯誤。 | 5xx 錯誤是服務端問題，用戶端無法修正或控制。在用戶端，為了減輕 5xx 錯誤的影響，您需要使用[截斷指數輪詢](https://docs.cloud.google.com/monitoring/api/troubleshooting?hl=zh-tw#exponential-retry)重試要求。如要進一步瞭解指數輪詢，請參閱「[指數輪詢](https://en.wikipedia.org/wiki/Exponential_backoff)」。不過，排解這項錯誤時有兩種特殊情況：`jobs.get` 呼叫和 `jobs.insert` 呼叫。  **`jobs.get` 通來電**   * 如果輪詢 `jobs.get` 時收到 503 錯誤，請稍候幾秒再重新輪詢。 * 如果工作完成，但包含含有 `backendError` 的錯誤物件，則表示工作失敗。您可以放心重試工作，不必擔心資料一致性問題。   **`jobs.insert` 呼叫**  如果在發出 `jobs.insert` 呼叫時收到這項錯誤，表示無法確定工作是否成功。在這種情況下，您必須重試工作。  如果重試無效且問題持續發生，您可以[計算失敗要求的比率](#calculate-rate-of-failing-requests)，並[聯絡支援團隊](https://cloud.google.com/support?hl=zh-tw)。  此外，如果發現對 BigQuery 的特定要求持續失敗並傳回 5xx 錯誤，即使多次嘗試重新啟動工作流程，並使用指數輪詢重試，仍無法解決問題，請向[支援團隊](https://cloud.google.com/support?hl=zh-tw)提報，從 BigQuery 端排解問題，無論整體計算出的錯誤率為何。請務必清楚說明[業務影響](https://docs.cloud.google.com/support/docs/customer-care-procedures?hl=zh-tw#support_case_priority)，以便正確分類問題。 |
| badRequest | 400 | 如果資料表中最近串流的部分資料列無法用於 DML 作業 (`DELETE`、`UPDATE`、`MERGE`)，就可能發生 `'UPDATE or DELETE statement over table project.dataset.table would affect rows in the streaming buffer, which is not supported'` 錯誤，通常會持續幾分鐘，但在極少數情況下，最長可能達 90 分鐘。詳情請參閱「[串流資料可用性](https://docs.cloud.google.com/bigquery/docs/streaming-data-into-bigquery?hl=zh-tw#dataavailability)」和「[DML 限制](https://docs.cloud.google.com/bigquery/docs/data-manipulation-language?hl=zh-tw#dml-limitations)」。 | 請稍候幾分鐘再試一次，或篩選陳述式，只對串流緩衝區外的舊資料執行操作。如要查看資料表 DML 作業是否有可用資料，請檢查 [`tables.get` 回應](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables/get?hl=zh-tw)的 [streamingBuffer 區段](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables?hl=zh-tw#streamingbuffer)。如果沒有 streamingBuffer 區段，則資料表資料可用於 DML 作業。您也可以使用 `streamingBuffer.oldestEntryTime` 欄位，找出串流緩衝區中記錄的保留時間。  或者，您也可以考慮使用 [BigQuery Storage Write API (gRPC)](https://docs.cloud.google.com/bigquery/docs/write-api?hl=zh-tw#use_data_manipulation_language_dml_with_recently_streamed_data) 串流資料，這項 API 沒有這項限制。 |
| billingNotEnabled | 403 | 當專案的計費功能沒有啟用時，系統就會傳回這個錯誤。 | 在[Google Cloud 控制台](https://console.cloud.google.com/?hl=zh-tw)中啟用專案的計費功能。 |
| billingTierLimitExceeded | 400 | 如果隨選工作的 `statistics.query.billingTier` 值超過 100，系統就會傳回這項錯誤。如果隨選查詢使用的 CPU 資源，相對於掃描的資料量過多，就會發生這種情況。如需檢查工作詳細資料的操作說明，請參閱「[管理工作](https://docs.cloud.google.com/bigquery/docs/managing-jobs?hl=zh-tw#view-job)」。 | 這項錯誤通常是因為明確或隱含執行效率不佳的 cross join，例如 join 條件不精確。這類查詢會消耗大量資源，通常無法妥善擴充，因此不適用於隨選定價。如要解決這項錯誤，您可以最佳化查詢，或改用[以運算資源 (運算單元) 為基礎](https://docs.cloud.google.com/bigquery/docs/reservations-intro?hl=zh-tw)的計價模式。如要瞭解如何最佳化查詢，請參閱「[避免 SQL 反模式](https://docs.cloud.google.com/bigquery/docs/best-practices-performance-patterns?hl=zh-tw)」。 |
| 已封鎖 | 403 | 如果 BigQuery 暫時拒絕您嘗試執行的作業 (通常是為了避免服務中斷)，就會傳回這項錯誤。 | 如需瞭解詳情，請[與支援團隊聯絡](https://cloud.google.com/support?hl=zh-tw)。 |
| duplicate | 409 | 嘗試建立已存在的工作、資料集或資料表時，系統會傳回這項錯誤。如果工作的 `writeDisposition` 屬性設為 `WRITE_EMPTY`，且工作存取的目的地資料表已存在，系統也會傳回這項錯誤。 | 請重新命名要建立的資源，或變更工作中的 `writeDisposition` 值。詳情請參閱如何排解[工作已存在](https://docs.cloud.google.com/bigquery/docs/troubleshoot-queries?hl=zh-tw#job_already_exists)錯誤。 |
| internalError | 500 | 如果 BigQuery 發生內部錯誤，就會傳回這項錯誤。 | 請按照 [BigQuery 服務水準協議](https://cloud.google.com/bigquery/sla?hl=zh-tw)所述的輪詢要求等待，然後再試一次。如果錯誤持續發生，請[聯絡支援團隊](https://cloud.google.com/support?hl=zh-tw)，或使用 BigQuery Issue Tracker [提交錯誤](https://issuetracker.google.com/issues/new?component=187149&template=0&hl=zh-tw)。您也可以使用[預留項目](https://docs.cloud.google.com/bigquery/docs/reservations-intro?hl=zh-tw)，降低這項錯誤的發生頻率。 |
| 無效 | 400 | 如果輸入內容無效 (查詢無效除外)，例如缺少必要欄位或資料表結構定義無效，就會傳回這項錯誤。無效的查詢會傳回 `invalidQuery` 錯誤。 |  |
| invalidQuery | 400 | 當您嘗試執行無效的查詢時，系統就會傳回這個錯誤。 | 檢查查詢是否有語法錯誤。[查詢參考資料](https://docs.cloud.google.com/bigquery/query-reference?hl=zh-tw)包含說明和範例，介紹如何建構有效的查詢。 |
| invalidUser | 400 | 如果您嘗試使用無效的使用者憑證排定查詢，就會傳回這項錯誤。 | 按照「[排定查詢](https://docs.cloud.google.com/bigquery/docs/scheduling-queries?hl=zh-tw#update_scheduled_query_credentials)」一文所述，重新整理使用者憑證。 |
| jobBackendError | 400 | 如果工作建立成功，但因內部錯誤而失敗，就會傳回這項錯誤。您可能會在 `jobs.query` 或 `jobs.getQueryResults` 中看到這項錯誤。 | 請使用新的 `jobId` 重試工作。如果錯誤持續發生，請與支援團隊聯絡。 |
| jobInternalError | 400 | 如果工作建立成功，但因內部錯誤而失敗，就會傳回這項錯誤。您可能會在 `jobs.query` 或 `jobs.getQueryResults` 中看到這項錯誤。 | 請使用新的 `jobId` 重試工作。如果錯誤持續發生，請與支援團隊聯絡。 |
| jobRateLimitExceeded | 400 | 如果工作建立成功，但因 [rateLimitExceeded](#rateLimitExceeded) 錯誤而失敗，就會傳回這項錯誤。您可能會在 `jobs.query` 或 `jobs.getQueryResults` 中看到這項錯誤。 | 請使用[指數輪詢](https://docs.cloud.google.com/monitoring/api/troubleshooting?hl=zh-tw#exponential-retry)降低要求率，然後使用新的 `jobId` 重試工作。 |
| notFound | 404 | 如果參照的資源 (資料集、資料表或工作) 不存在，或要求中的位置與資源位置不符 (例如工作執行位置)，就會傳回這項錯誤。使用[表格修飾符](https://docs.cloud.google.com/bigquery/docs/table-decorators?hl=zh-tw)參照最近[串流至](https://docs.cloud.google.com/bigquery/docs/streaming-data-into-bigquery?hl=zh-tw)的已刪除表格時，也可能發生這種情況。 | 請修正資源名稱、正確指定位置，或在串流後等待至少 6 小時，再查詢已刪除的資料表。 |
| notImplemented | 501 | 嘗試存取未實作的功能時，系統會傳回這項工作錯誤。 | 如需瞭解詳情，請[與支援團隊聯絡](https://cloud.google.com/support?hl=zh-tw)。 |
| proxyAuthenticationRequired | 407 | 如果要求缺少 Proxy 伺服器的有效驗證憑證，系統會在用戶端環境和 Proxy 伺服器之間傳回這項錯誤。詳情請參閱「[407 Proxy Authentication Required](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/407)」。 | 疑難排解方式會因環境而異。如果您在 Java 中作業時收到這則錯誤訊息，請確認您已設定 `jdk.http.auth.tunneling.disabledSchemes=` 和 `jdk.http.auth.proxying.disabledSchemes=` 屬性，且等號後方沒有任何值。 |
| quotaExceeded | 403 | 如果專案超出 [BigQuery 配額](https://docs.cloud.google.com/bigquery/quota-policy?hl=zh-tw)、[自訂配額](https://docs.cloud.google.com/bigquery/docs/custom-quotas?hl=zh-tw)，或您尚未設定帳單，且已超出[查詢免費方案](https://cloud.google.com/bigquery/pricing?hl=zh-tw#free-tier)，就會傳回這項錯誤。 | 查看錯誤物件的 `message` 屬性，進一步瞭解超出哪項配額。如要重設或提高 BigQuery 配額，請[與支援團隊聯絡](https://cloud.google.com/support?hl=zh-tw)。如要修改自訂配額，請在「[Quotas](https://console.cloud.google.com/iam-admin/quotas?hl=zh-tw)」(配額) 頁面提交要求。如果您在使用 BigQuery 沙箱時收到這項錯誤，可以[從沙箱升級](https://docs.cloud.google.com/bigquery/docs/sandbox?hl=zh-tw#upgrade)。  詳情請參閱「[排解 BigQuery 配額錯誤](https://docs.cloud.google.com/bigquery/docs/troubleshoot-quotas?hl=zh-tw)」。 |
| rateLimitExceeded | 403、429 | 如果專案在短時間內傳送過多要求，超出短期頻率限制，就會傳回這項錯誤。例如，請參閱[查詢工作的頻率限制](https://docs.cloud.google.com/bigquery/quota-policy?hl=zh-tw#query_jobs)和 [API 要求的頻率限制](https://docs.cloud.google.com/bigquery/quota-policy?hl=zh-tw#api_requests)。 | 降低要求比率。  如果您認為專案並未超過上述任一限制，請[聯絡支援團隊](https://cloud.google.com/support?hl=zh-tw)。  詳情請參閱「[排解 BigQuery 配額錯誤](https://docs.cloud.google.com/bigquery/docs/troubleshoot-quotas?hl=zh-tw)」。 |
| resourceInUse | 400 | 如果嘗試刪除含有資料表的資料集，或刪除目前正在執行的工作，就會傳回這項錯誤。 | 請先清空資料集再嘗試刪除，或等待工作完成後再刪除。 |
| resourcesExceeded | 400 | 如果工作使用的資源過多，系統就會傳回這項錯誤。 | 如果工作使用的資源過多，系統就會傳回這項錯誤。如需疑難排解資訊，請參閱「[排解資源超出錯誤](https://docs.cloud.google.com/bigquery/docs/troubleshoot-queries?hl=zh-tw#ts-resources-exceeded)」。 |
| responseTooLarge | 403 | 如果查詢結果大於[回應大小上限](https://docs.cloud.google.com/bigquery/quota-policy?hl=zh-tw#query_jobs)，系統就會傳回這項錯誤。有些查詢會分多個階段執行，如果任何階段傳回的回應大小過大，即使最終結果小於上限，也會傳回這項錯誤。如果查詢使用 `ORDER BY` 子句，通常會傳回這項錯誤。 | 有時新增 `LIMIT` 子句或移除 `ORDER BY` 子句可能會有幫助。如要確保能傳回大型結果，請將 `allowLargeResults` 屬性設為 `true`，並指定目的地資料表。詳情請參閱「[寫入大型查詢結果](https://docs.cloud.google.com/bigquery/docs/writing-results?hl=zh-tw#large-results)」。 |
| 已停止 | 200 | 工作遭到取消時會傳回這個狀態碼。 |  |
| tableUnavailable | 400 | 某些 BigQuery 資料表是由其他 Google 產品團隊管理的資料支援。這項錯誤表示其中一個資料表無法使用。 | 如果看到這則錯誤訊息，您可以重試要求 (請參閱 [internalError](#internalError) 疑難排解建議)，或與授予您資料存取權的 Google 產品團隊聯絡。 |
| 逾時 | 400 | 工作逾時 | 建議您減少作業執行的工作量，以便在設定的限制內完成。詳情請參閱「[排解配額和限制錯誤](https://docs.cloud.google.com/bigquery/docs/troubleshoot-quotas?hl=zh-tw)」。 |

### 錯誤回應範例

```
GET https://bigquery.googleapis.com/bigquery/v2/projects/12345/datasets/foo
Response:
[404]
{
  "error": {
  "errors": [
  {
    "domain": "global",
    "reason": "notFound",
    "message": "Not Found: Dataset myproject:foo"
  }],
  "code": 404,
  "message": "Not Found: Dataset myproject:foo"
  }
}
```

### 計算失敗要求率和運作時間

大多數 500 和 503 錯誤都能透過指數輪詢重試解決。如果 500 和 503 錯誤仍持續發生，您可以計算失敗要求的整體比率和對應的運作時間，並與 [BigQuery 服務水準協議 (SLA)](https://cloud.google.com/bigquery/sla?hl=zh-tw) 比較，判斷服務是否正常運作。

如要計算過去 30 天內要求失敗的整體比率，請將過去 30 天內特定 API 呼叫或方法的失敗要求數，除以過去 30 天內該 API 呼叫或方法的總要求數。將這個值乘以 100，即可得出 30 天內失敗要求的平均百分比。

舉例來說，您可以查詢 [Cloud Logging 資料](https://docs.cloud.google.com/logging/docs/view/logging-query-language?hl=zh-tw)，取得 `jobs.insert` 要求總數和失敗的 `jobs.insert` 要求數量，然後執行計算。您也可以從 [API 資訊主頁](https://docs.cloud.google.com/apis/docs/monitoring?hl=zh-tw#using_the_api_dashboard)或使用 [Cloud Monitoring](https://docs.cloud.google.com/apis/docs/monitoring?hl=zh-tw#using) 中的 Metrics Explorer 取得錯誤率值。這些選項不包含用戶端與 BigQuery 之間發生的網路或轉送問題相關資料，因此我們也建議使用用戶端記錄和回報系統，以便更精確地計算失敗率。

首先，用 100% 減去失敗要求的整體比率。如果這個值大於或等於 BigQuery 服務水準協議中規定的值，則運作時間也符合 BigQuery 服務水準協議。不過，如果這個值小於服務水準協議中說明的值，請手動計算運作時間。

如要計算正常運作時間，您必須知道視為服務停機時間的分鐘數。服務停機時間是指根據服務水準協議定義，錯誤率超過 10% 的一分鐘時間。如要計算正常運作時間，請將過去 30 天的總分鐘數減去服務停機的總分鐘數，將剩餘時間除以過去 30 天的總分鐘數，再將這個值乘以 100，即可得出 30 天內的正常運作時間百分比。如要進一步瞭解與服務水準協議相關的定義和計算方式，請參閱「[BigQuery 服務水準協議 (SLA)](https://cloud.google.com/bigquery/sla?hl=zh-tw)」。

如果每月正常運作時間百分比大於或等於 BigQuery 服務水準協議中規定的值，則錯誤很可能是由暫時性問題引起，因此您可以繼續使用[指數輪詢](https://docs.cloud.google.com/monitoring/api/troubleshooting?hl=zh-tw#exponential-retry)重試。

如果正常運作時間低於服務水準協議中顯示的值，請[與支援團隊聯絡](https://docs.cloud.google.com/support?hl=zh-tw)尋求協助，並提供觀察到的整體錯誤率和正常運作時間計算結果。

## 驗證錯誤

OAuth 權杖產生系統擲回的錯誤會傳回下列 JSON 物件，如 [OAuth 2.0 規格](https://tools.ietf.org/html/rfc6749#section-5.2)所定義。

`{"error" : "_description_string_"}`

這項錯誤會伴隨 HTTP `400` 錯誤要求，或 HTTP `401` 未授權錯誤。`_description_string_` 是 OAuth 2.0 規格定義的其中一個錯誤代碼。例如：

`{"error":"invalid_client"}`

### 查看錯誤

您可以使用[Logs Explorer](https://docs.cloud.google.com/logging/docs/view/logs-explorer-interface?hl=zh-tw)，查看特定工作、使用者或其他範圍的驗證錯誤。以下是 Logs Explorer 篩選器的範例，可用於查看驗證錯誤：

* 在政策遭拒稽核記錄中，搜尋因權限問題而失敗的工作：

  ```
  resource.type="bigquery_resource"
  protoPayload.status.message=~"Access Denied"
  logName="projects/PROJECT_ID/logs/cloudaudit.googleapis.com%2Fdata_access"
  ```

  將 `PROJECT_ID` 替換為資源所在專案的 ID。
* 搜尋用於驗證的特定使用者或服務帳戶：

  ```
  resource.type="bigquery_resource"
  protoPayload.authenticationInfo.principalEmail="EMAIL"
  ```

  將 `EMAIL` 替換為使用者或服務帳戶的電子郵件地址。
* 在管理員活動稽核記錄中，搜尋 Identity and Access Management 政策變更：

  ```
  protoPayload.methodName=~"SetIamPolicy"
  logName="projects/PROJECT_ID/logs/cloudaudit.googleapis.com%2Factivity"
  ```
* 在資料存取稽核記錄中，搜尋特定 BigQuery 資料集的變更：

  ```
  resource.type="bigquery_resource"
  protoPayload.resourceName="projects/PROJECT_ID/datasets/DATASET_ID"
  logName=projects/PROJECT_ID/logs/cloudaudit.googleapis.com%2Fdata_access
  ```

  將 `DATASET_ID` 替換為包含資源的資料集 ID。

## 連線錯誤訊息

下表列出使用用戶端程式庫或從程式碼呼叫 BigQuery API 時，可能因間歇性連線問題而看到的錯誤訊息：

| 錯誤訊息 | 用戶端程式庫或 API | 疑難排解 |
| --- | --- | --- |
| com.google.cloud.bigquery.BigQueryException: Read timed out | Java | 設定較大的逾時值。 |
| Connection has been shutdown: javax.net.ssl.SSLException: java.net.SocketException: Connection reset at com.google.cloud.bigquery.spi.v2.HttpBigQueryRpc.translate(HttpBigQueryRpc.java:115) | Java | 請導入重試機制，並設定較長的逾時值。 |
| javax.net.ssl.SSLHandshakeException: Remote host terminated the handshake | Java | 請導入重試機制，並設定較長的逾時值。 |
| BrokenPipeError: [Errno 32] Broken pipe | Python | 實作重試機制。如要進一步瞭解這項錯誤，請參閱 [BrokenPipeError](https://docs.python.org/3/library/exceptions.html#BrokenPipeError)。 |
| 連線已中斷。RemoteDisconnected('Remote end closed connection without response' | Python | 設定較大的逾時值。 |
| SSLEOFError (EOF occurred in violation of protocol) | Python | 系統會傳回這項錯誤，而非 413 (`ENTITY_TOO_LARGE`) HTTP 錯誤。縮減要求大小。 |
| TaskCanceledException：工作已取消 | .NET 程式庫 | 提高用戶端逾時值。 |
| google.api\_core.exceptions.PreconditionFailed: 412 PATCH | Python | 嘗試使用 [HTTP 要求](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables/update?hl=zh-tw)更新資料表資源時，會傳回這項錯誤。請確認 HTTP 標頭中的 ETag 並未過時。如果是資料表或資料集層級作業，請確認資源自上次例項化後未曾變更，並視需要重新建立物件。 |
| 無法建立新連線：[Errno 110] 連線逾時 | 用戶端程式庫 | 從 BigQuery 串流或讀取資料時，如果要求已達到檔案結尾 (EOF)，就會傳回這項錯誤。實作[重試機制](https://docs.cloud.google.com/monitoring/api/troubleshooting?hl=zh-tw#exponential-retry)，並設定較長的逾時值。 |
| socks.ProxyConnectionError: Error connecting to HTTP proxy :8080: [Errno 110] Connection timed out | 用戶端程式庫 | 排解 Proxy 狀態和設定問題。實作[重試機制](https://docs.cloud.google.com/monitoring/api/troubleshooting?hl=zh-tw#exponential-retry)，並設定較長的逾時值。 |
| 從傳輸串流收到非預期的 EOF 或 0 個位元組 | 用戶端程式庫 | 實作[重試機制](https://docs.cloud.google.com/monitoring/api/troubleshooting?hl=zh-tw#exponential-retry)，並設定較長的逾時值。 |

## Google Cloud 則控制台錯誤訊息

下表列出在Google Cloud 控制台操作時可能看到的錯誤訊息。

| 錯誤訊息 | 說明 | 疑難排解 |
| --- | --- | --- |
| 伺服器傳回不明錯誤回應。 | 如果 Google Cloud 控制台收到來自伺服器的不明錯誤，就會顯示這則錯誤訊息。舉例來說，當您點選資料集或其他類型的連結，但頁面無法顯示時，就會看到這則訊息。 | 切換至瀏覽器的無痕或私密模式，然後重複執行導致錯誤的操作。如果無痕模式下沒有發生錯誤，則錯誤可能是由瀏覽器擴充功能 (例如廣告攔截器) 造成。在非無痕模式下停用瀏覽器擴充功能，看看是否能解決問題。 |




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-10-29 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-10-29 (世界標準時間)。"],[],[]]