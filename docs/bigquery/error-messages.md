Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [資源](https://docs.cloud.google.com/bigquery/docs/release-notes?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 錯誤訊息

本文說明使用 BigQuery 時可能會遇到的錯誤訊息，包括 HTTP 錯誤代碼和建議的疑難排解步驟。

如要進一步瞭解查詢錯誤，請參閱「[排解查詢錯誤](https://docs.cloud.google.com/bigquery/docs/troubleshoot-queries?hl=zh-tw)」。

如要進一步瞭解串流資料插入錯誤，請參閱「[排解串流資料插入疑難](https://docs.cloud.google.com/bigquery/docs/streaming-data-into-bigquery?hl=zh-tw#troubleshooting)」。

## 錯誤表格

BigQuery API 的回應包含 HTTP 錯誤代碼，以及回應內文中的錯誤物件。錯誤物件通常是下列其中一種：

* [`errors` 物件](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#jobstatus)，其中包含 [`ErrorProto` 物件陣列](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables?hl=zh-tw#errorproto)。
* [`errorResults` 物件](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#jobstatus)，其中包含單一 [`ErrorProto` 物件](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables?hl=zh-tw#errorproto)。

下表中的「錯誤訊息」欄與 `ErrorProto` 物件中的 `reason` 屬性對應。

下表不會列出所有可能的 HTTP 錯誤或其他網路錯誤。因此，請勿假設 BigQuery 的每個錯誤回應中都有錯誤物件。此外，如果您使用 BigQuery API 適用的 Cloud 用戶端程式庫，可能會收到不同的錯誤或錯誤物件。詳情請參閱 [BigQuery API 用戶端程式庫](https://docs.cloud.google.com/bigquery/docs/reference/libraries?hl=zh-tw)。

如果您收到的 HTTP 回應代碼沒有出現在下表中，代表 HTTP 要求發生問題，或是產生符合預期的結果。`5xx` 範圍內的回應代碼表示伺服器端錯誤。如果收到 `5xx` 回應代碼，請稍後重試要求。在某些情況下，中繼伺服器 (例如 Proxy) 可能會傳回 `5xx` 回應代碼。檢查回應主體和回應標頭，瞭解錯誤的詳細資料。如需完整的 HTTP 回應代碼清單，請參閱 [HTTP 回應代碼](https://en.wikipedia.org/wiki/HTTP_response_codes)。

使用 [bq 指令列工具](https://docs.cloud.google.com/bigquery/bq-command-line-tool?hl=zh-tw)查看工作狀態時，系統預設不會傳回錯誤物件。如要查看錯誤物件，以及與下表相對應的 `reason` 屬性，請使用 `--format=prettyjson` 旗標。例如：`bq --format=prettyjson show -j
*<job id>*`。如要查看 bq 工具的詳細記錄，請使用 `--apilog=stdout`。如要進一步瞭解如何排解 bq 工具問題，請參閱「[偵錯](https://docs.cloud.google.com/bigquery/docs/bq-command-line-tool?hl=zh-tw#debugging)」一文。

| 錯誤訊息 | HTTP 代碼 | 說明 | 疑難排解 |
| --- | --- | --- | --- |
| accessDenied | 403 | 當您嘗試存取您沒有存取權限的資源 (例如[資料集](https://docs.cloud.google.com/bigquery/docs/datasets?hl=zh-tw)、[資料表](https://docs.cloud.google.com/bigquery/docs/tables?hl=zh-tw)、[檢視區塊](https://docs.cloud.google.com/bigquery/docs/views-intro?hl=zh-tw)或[工作](https://docs.cloud.google.com/bigquery/docs/managing-jobs?hl=zh-tw)) 時，系統就會傳回這個錯誤。如果您嘗試修改唯讀物件，也會傳回這個錯誤。 | 請與資源擁有者聯絡，並[要求使用者存取資源](https://docs.cloud.google.com/bigquery/access-control?hl=zh-tw)。該使用者是由錯誤稽核記錄中的 `principalEmail` 值所識別。 |
| attributeError | 400 | 如果使用者程式碼有問題，呼叫了不存在的特定物件屬性，就會傳回這個錯誤。 | 請確認您要使用的物件具有您嘗試存取的屬性。如要進一步瞭解這項錯誤，請參閱「[AttributeError](https://docs.python.org/3/library/exceptions.html#AttributeError)」。 |
| backendError | 500、502、503 或 504 | 這個錯誤表示服務目前無法使用。這可能是由許多暫時性問題所造成，包括：   * **服務需求暴增**：需求突然暴增 (例如使用量尖峰時段)，可能會導致負載卸除，以保護所有 BigQuery 使用者的服務品質。為避免系統負載過重，BigQuery 可能會針對一小部分要求傳回 500 或 503 錯誤。 * **網路問題**：BigQuery 的分散式特性表示資料通常會在系統中的不同元件或機器之間傳輸。各種間歇性網路連線問題都可能導致 BigQuery 傳回 5xx 錯誤，包括 SSL 交握失敗，或是使用者與Google Cloud之間的網路基礎架構問題。 * **資源耗盡**：BigQuery 設有各種內部資源限制，可避免單一使用者或單一工作耗用過多資源，進而影響整體服務效能。BigQuery 會實作負載卸除，以解決資源耗盡問題。 * **後端錯誤**：在極少數情況下，BigQuery 元件發生內部問題時，可能會導致系統傳回 500 或 503 錯誤給用戶端。 | 5xx 錯誤是服務端問題，用戶端無法修正或控制。在用戶端，為減輕 5xx 錯誤的影響，您需要使用[部分指數輪詢](https://cloud.google.com/monitoring/api/troubleshooting?hl=zh-tw#exponential-retry)重試要求。如要進一步瞭解指數輪詢，請參閱「[指數輪詢](https://en.wikipedia.org/wiki/Exponential_backoff)」。不過，排解這個錯誤時要注意兩個特殊案例：`jobs.get` 呼叫和 `jobs.insert` 呼叫。  **`jobs.get` 呼叫**   * 如果您在輪詢 `jobs.get` 時收到 503 錯誤，請稍候片刻，然後再輪詢一次。 * 如果工作完成，但出現含 `backendError` 的錯誤物件，表示工作失敗。您可以安全地重新執行工作，不必擔心資料一致性的問題。   **`jobs.insert` 呼叫**  如果您在執行 `jobs.insert` 呼叫時收到這則錯誤訊息，我們無法得知工作是否已成功執行。在這種情況下，您必須重新執行工作。  如果重試無效且問題仍未解決，請[計算要求失敗率](#calculate-rate-of-failing-requests)，然後[與支援團隊聯絡](https://cloud.google.com/support?hl=zh-tw)。  此外，如果發現特定 BigQuery 要求持續失敗並傳回 5xx 錯誤，即使在多次重新啟動工作流程時使用指數輪詢重試，也應將此問題回報給[支援團隊](https://cloud.google.com/support?hl=zh-tw)，以便從 BigQuery 端排解問題，無論整體計算的錯誤率為何。請務必清楚說明[業務影響](https://cloud.google.com/support/docs/customer-care-procedures?hl=zh-tw#support_case_priority)，以便正確分類問題。 |
| badRequest | 400 | 如果資料表中的某些資料列最近才透過串流傳輸，可能無法用於 DML 作業 (`DELETE`、`UPDATE`、`MERGE`)，通常會持續幾分鐘，但極少數情況下，最多可能達 90 分鐘，這時就會發生 `'UPDATE or DELETE statement over table project.dataset.table would affect rows in the streaming buffer, which is not supported'` 錯誤。詳情請參閱「[串流資料可用性](https://docs.cloud.google.com/bigquery/docs/streaming-data-into-bigquery?hl=zh-tw#dataavailability)」和「[DML 限制](https://docs.cloud.google.com/bigquery/docs/data-manipulation-language?hl=zh-tw#dml-limitations)」。 | 請稍候幾分鐘再試一次，或篩選對帳單，只處理串流緩衝區以外的舊資料。如要查看資料是否可用於資料表 DML 作業，請檢查[`tables.get`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables/get?hl=zh-tw)回應的[streamingBuffer 區段](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables?hl=zh-tw#streamingbuffer)。如果沒有 streamingBuffer 區段，則資料表資料可用於 DML 作業。您也可以使用 `streamingBuffer.oldestEntryTime` 欄位，識別串流緩衝區中的記錄存續時間。  或者，您也可以考慮使用[BigQuery Storage Write API](https://docs.cloud.google.com/bigquery/docs/write-api?hl=zh-tw#use_data_manipulation_language_dml_with_recently_streamed_data) 串流資料，這個 API 沒有這項限制。 |
| billingNotEnabled | 403 | 當專案的計費功能沒有啟用時，系統就會傳回這個錯誤。 | 在[Google Cloud 控制台](https://console.cloud.google.com/?hl=zh-tw)中啟用專案的計費功能。 |
| billingTierLimitExceeded | 400 | 如果隨選工作的 `statistics.query.billingTier` 值超過 100，系統就會傳回這個錯誤。如果以量計價查詢使用的 CPU 資源，相較於掃描的資料量過多，就會發生這種情況。如需檢查工作詳細資料的操作說明，請參閱「[管理工作](https://docs.cloud.google.com/bigquery/docs/managing-jobs?hl=zh-tw#view-job)」。 | 這個錯誤最常是因為執行效率不彰的交叉聯結所致，可能是明確或隱含的交叉聯結，例如聯結條件不精確。這類查詢會耗用大量資源，因此不適合採用以量計價，而且通常無法順利擴充。您可以最佳化查詢，或改用[以運算資源 (運算單元) 為基礎](https://docs.cloud.google.com/bigquery/docs/reservations-intro?hl=zh-tw)的計價模式，解決這項錯誤。如要瞭解如何最佳化查詢，請參閱「[避免 SQL 反模式](https://docs.cloud.google.com/bigquery/docs/best-practices-performance-patterns?hl=zh-tw)」。 |
| 已封鎖 | 403 | 當 BigQuery 暫時將您嘗試執行的作業加入拒絕清單時 (通常是為了避免服務中斷)，就會傳回這個錯誤。 | 如需更多資訊，請[與支援團隊聯絡](https://cloud.google.com/support?hl=zh-tw)。 |
| duplicate | 409 | 當您嘗試建立已經存在的工作、資料集或資料表時，系統就會傳回這個錯誤。如果工作的 `writeDisposition` 屬性設為 `WRITE_EMPTY`，且工作所存取的目的地資料表已存在，也會傳回這個錯誤。 | 將您嘗試建立的資源重新命名，或變更工作中的 `writeDisposition` 值。詳情請參閱「[作業已存在](https://docs.cloud.google.com/bigquery/docs/troubleshoot-queries?hl=zh-tw#job_already_exists)」錯誤的疑難排解方式。 |
| internalError | 500 | 當 BigQuery 發生內部錯誤時，系統就會傳回這個錯誤。 | 請根據 [BigQuery 服務水準協議](https://cloud.google.com/bigquery/sla?hl=zh-tw)所述的退避要求等待一段時間，然後再試一次。如果這個問題一再發生，請[與支援小組聯絡](https://cloud.google.com/support?hl=zh-tw)，或是使用 BigQuery 問題追蹤工具[回報錯誤](https://issuetracker.google.com/issues/new?component=187149&template=0&hl=zh-tw)。您也可以使用[預訂](https://docs.cloud.google.com/bigquery/docs/reservations-intro?hl=zh-tw)功能，減少發生這類錯誤的頻率。 |
| 無效 | 400 | 出現無效查詢以外的任何無效輸入種類時 (例如空白的必填欄位，或無效的資料表結構定義)，系統就會傳回這個錯誤。查詢無效時，系統會傳回 `invalidQuery` 錯誤。 |  |
| invalidQuery | 400 | 當您嘗試執行無效的查詢時，系統就會傳回這個錯誤。 | 請檢查查詢，看看有無語法錯誤。如需如何建立有效查詢的說明和範例，請參閱[查詢參考資料](https://docs.cloud.google.com/bigquery/query-reference?hl=zh-tw)。 |
| invalidUser | 400 | 當您嘗試使用無效的使用者憑證排定查詢時，系統就會傳回這個錯誤。 | 如「[排定查詢時間](https://docs.cloud.google.com/bigquery/docs/scheduling-queries?hl=zh-tw#update_scheduled_query_credentials)」一文所述，重新整理使用者憑證。 |
| jobBackendError | 400 | 如果作業已順利建立，但因發生內部錯誤而失敗，系統就會傳回這個錯誤。您可能會在 `jobs.query` 或 `jobs.getQueryResults` 中看到這項錯誤。 | 使用新的 `jobId` 重試工作。如果錯誤持續發生，請與支援團隊聯絡。 |
| jobInternalError | 400 | 如果作業已順利建立，但因發生內部錯誤而失敗，系統就會傳回這個錯誤。您可能會在 `jobs.query` 或 `jobs.getQueryResults` 中看到這項錯誤。 | 使用新的 `jobId` 重試工作。如果錯誤持續發生，請與支援團隊聯絡。 |
| jobRateLimitExceeded | 400 | 如果作業已順利建立，但因 [rateLimitExceeded](#rateLimitExceeded) 錯誤而失敗，系統就會傳回這項錯誤。您可能會在 `jobs.query` 或 `jobs.getQueryResults` 中看到這項錯誤。 | 使用「指數輪詢」降低要求率，然後使用新的 `jobId` 重試工作。 |
| notFound | 404 | 當您參照的資源 (資料集、資料表或工作) 不存在，或要求中的位置與資源位置不符 (例如工作執行的位置) 時，系統就會傳回這個錯誤。如果使用[資料表修飾符](https://docs.cloud.google.com/bigquery/docs/table-decorators?hl=zh-tw)參照最近曾做為[串流目的地](https://docs.cloud.google.com/bigquery/docs/streaming-data-into-bigquery?hl=zh-tw)的已刪除資料表，也會發生這個錯誤。 | 請修正資源名稱、正確指定位置，或是在串流結束至少 6 小時之後，再查詢已刪除的資料表。 |
| notImplemented | 501 | 當您嘗試存取沒有導入的功能時，系統就會傳回這個錯誤。 | 如需更多資訊，請[與支援團隊聯絡](https://cloud.google.com/support?hl=zh-tw)。 |
| proxyAuthenticationRequired | 407 | 當要求缺少 Proxy 伺服器的有效驗證憑證時，用戶端環境和 Proxy 伺服器之間會傳回這項錯誤。詳情請參閱「[407 需要 Proxy 驗證](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/407)」。 | 疑難排解方式會因環境而異。如果在 Java 中作業時收到這項錯誤，請確認您已設定 `jdk.http.auth.tunneling.disabledSchemes=` 和 `jdk.http.auth.proxying.disabledSchemes=` 屬性，且等號後方沒有值。 |
| quotaExceeded | 403 | 如果您的專案超出 [BigQuery 配額](https://docs.cloud.google.com/bigquery/quota-policy?hl=zh-tw)或[自訂配額](https://docs.cloud.google.com/bigquery/docs/custom-quotas?hl=zh-tw)，或是您沒有設定計費功能，且專案超出[查詢的免費方案配額](https://cloud.google.com/bigquery/pricing?hl=zh-tw#free-tier)時，系統就會傳回這個錯誤。 | 請查看錯誤物件的 `message` 屬性，以便進一步瞭解專案超出了哪個配額。如要重設或調高 BigQuery 配額，請[與支援小組聯絡](https://cloud.google.com/support?hl=zh-tw)。如要修改自訂配額，請前往「配額」頁面提交要求。如果您是在使用 BigQuery 沙箱時收到這個錯誤，可以[從沙箱升級](https://docs.cloud.google.com/bigquery/docs/sandbox?hl=zh-tw#upgrade)。  詳情請參閱「[排解 BigQuery 配額錯誤](https://docs.cloud.google.com/bigquery/docs/troubleshoot-quotas?hl=zh-tw)」。 |
| rateLimitExceeded | 403 | 如果專案在短時間內傳送太多要求，超出短期頻率限制，系統就會傳回這個錯誤。舉例來說，請參閱「[查詢作業的使用頻率限制](https://docs.cloud.google.com/bigquery/quota-policy?hl=zh-tw#query_jobs)」和「[API 請求的使用頻率限制](https://docs.cloud.google.com/bigquery/quota-policy?hl=zh-tw#api_requests)」。 | 降低要求頻率。  如果您確定專案並未超出上述的任何限制，請[與支援小組聯絡](https://cloud.google.com/support?hl=zh-tw)。  詳情請參閱「[排解 BigQuery 配額錯誤](https://docs.cloud.google.com/bigquery/docs/troubleshoot-quotas?hl=zh-tw)」。 |
| resourceInUse | 400 | 當您嘗試刪除含有資料表的資料集或目前正在執行的工作時，就會傳回這個錯誤。 | 請在刪除資料集之前先清空資料夾，或是等待工作執行完畢之後再來刪除工作。 |
| resourcesExceeded | 400 | 當工作使用的資源過多時，系統就會傳回這個錯誤。 | 如果工作使用的資源過多，系統就會傳回這個錯誤。如需疑難排解資訊，請參閱「[排解資源超出限制的錯誤](https://docs.cloud.google.com/bigquery/docs/troubleshoot-queries?hl=zh-tw#ts-resources-exceeded)」。 |
| responseTooLarge | 403 | 當查詢的結果超出[回應大小上限](https://docs.cloud.google.com/bigquery/quota-policy?hl=zh-tw#query_jobs)時，系統就會傳回這個錯誤。某些查詢會分成好幾個階段來執行，只要有任何一個階段傳回的回應大小超出上限，即使最終的結果並沒有超過大小上限，系統也會傳回這個錯誤。當查詢使用 `ORDER BY` 子句時，系統通常會傳回這個錯誤。 | 請新增 `LIMIT` 子句 (可能會有幫助)，或是移除 `ORDER BY` 子句。如要確保查詢能夠傳回較大的結果，請將 `allowLargeResults` 屬性設定為 `true`，並指定目的地資料表。詳情請參閱「[寫入大型查詢結果](https://docs.cloud.google.com/bigquery/docs/writing-results?hl=zh-tw#large-results)」。 |
| 已停止 | 200 | 工作遭到取消時會傳回這個狀態碼。 |  |
| tableUnavailable | 400 | 特定 BigQuery 資料表所含的資料是由其他 Google 產品團隊負責管理。這個錯誤代表其中一個資料表是無法使用的。 | 當您收到這個錯誤訊息時，請重新提出要求 (請參閱 [internalError](#internalError) 的疑難排解建議)，或是與授予您資料存取權的 Google 產品小組聯絡。 |
| 逾時 | 400 | 工作逾時 | 建議減少作業執行的工作量，以便在設定的限制內完成。詳情請參閱「[排解配額和限制錯誤](https://docs.cloud.google.com/bigquery/docs/troubleshoot-quotas?hl=zh-tw)」。 |

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

### 計算要求失敗率和正常運作時間

大多數的 500 和 503 錯誤都能透過指數輪詢重試解決。如果 500 和 503 錯誤仍持續發生，您可以計算整體要求失敗率和相應的運作時間，並與 [BigQuery 服務水準協議 (SLA)](https://cloud.google.com/bigquery/sla?hl=zh-tw) 比較，判斷服務是否正常運作。

如要計算過去 30 天的整體要求失敗率，請將特定 API 呼叫或方法在過去 30 天內的要求失敗次數，除以該 API 呼叫或方法在過去 30 天內的要求總次數。將這個值乘以 100，即可得出 30 天內要求失敗的平均百分比。

舉例來說，您可以查詢 [Cloud Logging 資料](https://docs.cloud.google.com/logging/docs/view/logging-query-language?hl=zh-tw)，取得 `jobs.insert` 要求的總數和失敗的 `jobs.insert` 要求數，然後進行計算。您也可以從 [API 資訊主頁](https://docs.cloud.google.com/apis/docs/monitoring?hl=zh-tw#using_the_api_dashboard)取得錯誤率值，或使用 [Cloud Monitoring](https://docs.cloud.google.com/apis/docs/monitoring?hl=zh-tw#using) 中的 Metrics Explorer 取得。這些選項不會納入用戶端與 BigQuery 之間發生的網路或路由問題相關資料，因此我們也建議使用用戶端記錄和回報系統，更準確地計算失敗率。

首先，請從 100% 減去整體要求失敗率。如果這個值大於或等於 BigQuery 服務水準協議 (SLA) 中所述的值，則正常運作時間也符合 BigQuery 服務水準協議。不過，如果這個值低於服務等級協議 (SLA) 中所述的值，請手動計算正常運作時間。

如要計算正常運作時間，您必須知道服務停機的分鐘數。服務停機是指錯誤率超過 10% 的一分鐘時段，計算方式依據服務等級協議定義。如要計算正常運作時間，請取過去 30 天的總分鐘數，然後扣除服務停機的總分鐘數。將剩餘時間除以過去 30 天的總分鐘數，然後將這個值乘以 100，即可得出 30 天的正常運作時間百分比。如要進一步瞭解與服務水準協議 (SLA) 相關的定義和計算方式，請參閱 [BigQuery 服務水準協議 (SLA)](https://cloud.google.com/bigquery/sla?hl=zh-tw)

如果您的每月正常運作時間百分比大於或等於 BigQuery 服務水準協議中描述的值，則錯誤最可能是由暫時性問題所致，因此您可以繼續使用[指數輪詢](https://docs.cloud.google.com/monitoring/api/troubleshooting?hl=zh-tw#exponential-retry)重試。

如果正常運作時間低於服務水準協議中顯示的值，請[與支援團隊聯絡](https://docs.cloud.google.com/support?hl=zh-tw)尋求協助，並分享觀察到的整體錯誤率和正常運作時間計算結果。

## 驗證錯誤

根據 [OAuth2 規格](https://tools.ietf.org/html/rfc6749#section-5.2)的定義，OAuth 權杖產生系統所擲回的錯誤，會傳回以下 JSON 物件。

`{"error" : "_description_string_"}`

這個錯誤會與「HTTP `400` 錯誤的要求」錯誤或「HTTP`401` 未授權」錯誤一起出現。`_description_string_` 是 OAuth2 規格所定義的其中一個錯誤代碼。例如：

`{"error":"invalid_client"}`

### 查看錯誤

您可以使用[記錄檢視器](https://docs.cloud.google.com/logging/docs/view/logs-explorer-interface?hl=zh-tw)，查看特定工作、使用者或其他範圍的驗證錯誤。以下是記錄探索器篩選器範例，可用於查看驗證錯誤：

* 在「政策遭拒」稽核記錄中，搜尋權限問題導致失敗的工作：

  ```
  resource.type="bigquery_resource"
  protoPayload.status.message=~"Access Denied"
  logName="projects/PROJECT_ID/logs/cloudaudit.googleapis.com%2Fdata_access"
  ```

  將 `PROJECT_ID` 替換為含有資源的專案 ID。
* 搜尋用於驗證的特定使用者或服務帳戶：

  ```
  resource.type="bigquery_resource"
  protoPayload.authenticationInfo.principalEmail="EMAIL"
  ```

  將 `EMAIL` 替換為使用者或服務帳戶的電子郵件地址。
* 在管理員活動稽核記錄中，搜尋身分與存取權管理政策異動：

  ```
  protoPayload.methodName=~"SetIamPolicy"
  logName="projects/PROJECT_ID/logs/cloudaudit.googleapis.com%2Factivity"
  ```
* 在「資料存取」稽核記錄中，搜尋特定 BigQuery 資料集的變更：

  ```
  resource.type="bigquery_resource"
  protoPayload.resourceName="projects/PROJECT_ID/datasets/DATASET_ID"
  logName=projects/PROJECT_ID/logs/cloudaudit.googleapis.com%2Fdata_access
  ```

  將 `DATASET_ID` 替換為含有資源的資料集 ID。

## 連線錯誤訊息

下表列出使用用戶端程式庫或從程式碼呼叫 BigQuery API 時，可能因連線問題而看到的錯誤訊息：

| 錯誤訊息 | 用戶端程式庫或 API | 疑難排解 |
| --- | --- | --- |
| com.google.cloud.bigquery.BigQueryException：讀取逾時 | Java | 設定較大的逾時值。 |
| Connection has been shutdown: javax.net.ssl.SSLException: java.net.SocketException: Connection reset at com.google.cloud.bigquery.spi.v2.HttpBigQueryRpc.translate(HttpBigQueryRpc.java:115) | Java | 實作重試機制，並設定較大的逾時值。 |
| javax.net.ssl.SSLHandshakeException：遠端主機終止交握 | Java | 實作重試機制，並設定較大的逾時值。 |
| BrokenPipeError: [Errno 32] Broken pipe | Python | 實作重試機制。如要進一步瞭解這項錯誤，請參閱「[BrokenPipeError](https://docs.python.org/3/library/exceptions.html#BrokenPipeError)」。 |
| 連線已中止。RemoteDisconnected('Remote end closed connection without response' | Python | 設定較大的逾時值。 |
| SSLEOFError (違反通訊協定而發生 EOF) | Python | 系統會傳回這個錯誤，而不是 413 (`ENTITY_TOO_LARGE`) HTTP 錯誤。縮減要求大小。 |
| TaskCanceledException：工作已取消 | .NET 程式庫 | 在用戶端增加逾時值。 |
| google.api\_core.exceptions.PreconditionFailed: 412 PATCH | Python | 使用 [HTTP 要求](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables/update?hl=zh-tw)更新資料表資源時，系統會傳回這個錯誤。請確認 HTTP 標頭中的 ETag 並未過時。如要執行資料表或資料集層級的作業，請確認資源自上次例項化後未曾變更，並視需要重新建立物件。 |
| 無法建立新連線：[Errno 110] Connection timed out | 用戶端程式庫 | 從 BigQuery 串流或讀取資料時，如果這項要求已到達檔案結尾 (EOF)，系統就會傳回這個錯誤。實作[重試機制](https://cloud.google.com/monitoring/api/troubleshooting?hl=zh-tw#exponential-retry)，並設定較大的逾時值。 |
| socks.ProxyConnectionError: Error connecting to HTTP proxy :8080: [Errno 110] Connection timed out | 用戶端程式庫 | 排解 Proxy 狀態和設定問題。實作[重試機制](https://cloud.google.com/monitoring/api/troubleshooting?hl=zh-tw#exponential-retry)，並設定較大的逾時值。 |
| 從傳輸串流收到非預期的 EOF 或 0 位元組 | 用戶端程式庫 | 實作[重試機制](https://cloud.google.com/monitoring/api/troubleshooting?hl=zh-tw#exponential-retry)，並設定較大的逾時值。 |

## Google Cloud 控制台錯誤訊息

下表列出在Google Cloud 控制台中作業時可能看到的錯誤訊息。

| 錯誤訊息 | 說明 | 疑難排解 |
| --- | --- | --- |
| 伺服器傳回不明的錯誤回應。 | 如果 Google Cloud 控制台從伺服器收到不明錯誤，就會顯示這個錯誤。舉例來說，當您點選資料集或其他類型的連結，但系統無法顯示該頁面時，就會發生這種情況。 | 切換至瀏覽器的無痕或私密模式，然後重複導致錯誤的動作。如果無痕模式沒有錯誤，可能是因為瀏覽器擴充功能 (例如廣告封鎖程式) 導致錯誤。在非無痕模式下停用瀏覽器擴充功能，看看是否能解決問題。 |




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-09 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-09 (世界標準時間)。"],[],[]]