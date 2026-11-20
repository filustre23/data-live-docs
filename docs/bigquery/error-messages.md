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

本文說明使用 BigQuery 時，可能會遇到的用戶端、Proxy、連線能力和 Google Cloud 控制台錯誤訊息。

* 如要瞭解 BigQuery API 傳回的 HTTP 狀態碼和 API 錯誤訊息，請參閱「[BigQuery API 的 HTTP 狀態和錯誤代碼](https://docs.cloud.google.com/bigquery/docs/errors?hl=zh-tw)」。
* 如要進一步瞭解查詢錯誤，請參閱「[排解查詢錯誤](https://docs.cloud.google.com/bigquery/docs/troubleshoot-queries?hl=zh-tw)」。
* 如要進一步瞭解存取控管和驗證錯誤，請參閱「[排解存取控管問題](https://docs.cloud.google.com/bigquery/docs/troubleshoot-access-control?hl=zh-tw)」。
* 如要進一步瞭解串流資料即時插入錯誤，請參閱「[排解串流資料即時插入問題](https://docs.cloud.google.com/bigquery/docs/write-api-rest?hl=zh-tw#troubleshooting)」。
* 如要進一步瞭解用戶端程式庫錯誤和物件，請參閱「[BigQuery API 用戶端程式庫](https://docs.cloud.google.com/bigquery/docs/reference/libraries?hl=zh-tw)」。

## 錯誤表格

如果您使用 [bq 指令列工具](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw)檢查工作狀態，系統預設不會傳回錯誤物件。如要查看錯誤物件和對應的 `reason` 屬性，請使用 `--format=prettyjson` 旗標，例如 `bq --format=prettyjson show -j <var>JOB_ID</var>`。如要查看 bq 工具的詳細記錄，請使用 `--apilog=stdout`。如要進一步瞭解如何排解 bq 工具問題，請參閱「[排解 CLI 指令問題](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#troubleshooting-bq)」。

下表列出 BigQuery API 未直接傳回的用戶端和 Proxy 錯誤訊息：

| 錯誤訊息 | HTTP 代碼 | 說明 | 疑難排解 |
| --- | --- | --- | --- |
| attributeError | 400 | 使用者程式碼參照了不存在的物件屬性。 | 請確認您使用的物件具有您嘗試存取的屬性。如要進一步瞭解這項錯誤，請參閱「[AttributeError](https://docs.python.org/3/library/exceptions.html#AttributeError)」。 |
| proxyAuthenticationRequired | 407 | 用戶端要求缺少 Proxy 伺服器的有效驗證憑證。詳情請參閱「[407 Proxy Authentication Required](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/407)」。 | 疑難排解步驟會因環境而異。如果您在 Java 中作業時收到這則錯誤訊息，請確認您已設定 `jdk.http.auth.tunneling.disabledSchemes=` 和 `jdk.http.auth.proxying.disabledSchemes=` 屬性，且等號後方沒有任何值。 |

## 連線錯誤訊息

下表列出使用用戶端程式庫或從程式碼呼叫 BigQuery API 時，可能因間歇性連線問題而看到的錯誤訊息：

| 錯誤訊息 | 用戶端程式庫或 API | 疑難排解 |
| --- | --- | --- |
| com.google.cloud.bigquery.BigQueryException: Read timed out | Java | 設定較大的逾時值。 |
| Connection has been shutdown: javax.net.ssl.SSLException: java.net.SocketException: Connection reset at com.google.cloud.bigquery.spi.v2.HttpBigQueryRpc.translate(HttpBigQueryRpc.java:115) | Java | 請實作重試機制，並設定較長的逾時值。 |
| javax.net.ssl.SSLHandshakeException: Remote host terminated the handshake | Java | 請實作重試機制，並設定較長的逾時值。 |
| BrokenPipeError: [Errno 32] Broken pipe | Python | 實作重試機制。如要進一步瞭解這項錯誤，請參閱「[BrokenPipeError](https://docs.python.org/3/library/exceptions.html#BrokenPipeError)」。 |
| 連線已中斷。RemoteDisconnected('Remote end closed connection without response' | Python | 設定較大的逾時值。 |
| SSLEOFError (EOF occurred in violation of protocol) | Python | 要求酬載超過允許的傳輸大小，因此在產生 HTTP 413 (`ENTITY_TOO_LARGE`) 錯誤前遭到拒絕。縮減要求大小。 |
| TaskCanceledException：工作已取消 | .NET 程式庫 | 提高用戶端的逾時值。 |
| google.api\_core.exceptions.PreconditionFailed: 412 PATCH | Python | [HTTP 更新要求](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables/update?hl=zh-tw)失敗，因為 HTTP 標頭中的 ETag 已過時，或基礎資料表或資料集資源在物件例項化後遭到修改。請確認 ETag 為最新版本，並視需要重新建立用戶端物件。 |
| 無法建立新連線：[Errno 110] 連線逾時 | 用戶端程式庫 | 從 BigQuery 串流或讀取資料時，用戶端連線意外終止或達到檔案結尾 (EOF)。實作[重試機制](https://docs.cloud.google.com/monitoring/api/troubleshooting?hl=zh-tw#retry)，並設定較長的逾時值。 |
| socks.ProxyConnectionError: Error connecting to HTTP proxy `IP_ADDRESS:8080: [Errno 110] Connection timed out` | 用戶端程式庫 | 排解 Proxy 狀態和設定問題。實作[重試機制](https://docs.cloud.google.com/monitoring/api/troubleshooting?hl=zh-tw#retry)，並設定較長的逾時值。 |
| 從傳輸串流收到非預期的 EOF 或 0 個位元組 | 用戶端程式庫 | 實作[重試機制](https://docs.cloud.google.com/monitoring/api/troubleshooting?hl=zh-tw#retry)，並設定較長的逾時值。 |

## Google Cloud 則控制台錯誤訊息

下表列出您在 Google Cloud 控制台操作時可能看到的錯誤訊息。

| 錯誤訊息 | 說明 | 疑難排解 |
| --- | --- | --- |
| 伺服器傳回不明錯誤回應。 | 如果 Google Cloud 控制台收到來自伺服器的不明錯誤，就會顯示這項錯誤。舉例來說，當您點選資料集或其他類型的連結，但無法顯示頁面時，就會出現這項錯誤。 | 切換至瀏覽器的無痕或私密模式，然後重複執行導致錯誤的操作。如果無痕模式下沒有發生錯誤，則錯誤可能是由瀏覽器擴充功能 (例如廣告攔截器) 造成。在非無痕模式下停用瀏覽器擴充功能，看看是否能解決問題。 |




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-11-20 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-11-20 (世界標準時間)。"],[],[]]