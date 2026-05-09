Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# BigQuery Storage Write API 最佳做法

本文提供使用 BigQuery Storage Write API 的最佳做法。閱讀本文前，請先參閱「[BigQuery Storage Write API 總覽](https://docs.cloud.google.com/bigquery/docs/write-api?hl=zh-tw#overview)」。

## 限制串流建立速率

建立串流前，請先考慮是否可以使用[預設串流](https://docs.cloud.google.com/bigquery/docs/write-api?hl=zh-tw#default_stream)。在串流情境中，預設串流的配額限制較少，且比使用應用程式建立的串流更具擴充性。如果您使用應用程式建立的串流，請務必先充分利用每個串流的最大處理量，再建立其他串流。舉例來說，請使用[非同步寫入作業](#do_not_block_on_appendrows_calls)。

如果是應用程式建立的串流，請避免以高頻率呼叫 `CreateWriteStream`。一般來說，如果每秒超過 40 到 50 次呼叫，API 呼叫的延遲時間會大幅增加 (超過 25 秒)。請確保應用程式可接受冷啟動，並逐步增加串流數量，同時限制 `CreateWriteStream` 呼叫的速率。您也可以設定較長的期限，等待呼叫完成，以免因 `DeadlineExceeded` 錯誤而失敗。此外，`CreateWriteStream` 呼叫的最高速率也有長期[配額](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#createwritestream)。建立串流是耗用大量資源的程序，因此減少串流建立率並充分利用現有串流，是避免超出這項限制的最佳做法。

## 連線集區管理

`AppendRows` 方法會建立串流的雙向連線。您可以在預設串流上開啟多個連線，但只能在應用程式建立的串流上開啟單一有效連線。

使用預設串流時，您可以透過 Storage Write API 多工處理，使用共用連線寫入多個目的地資料表。多工處理集區連線，可提高處理量和資源使用率。如果工作流程有超過 20 個並行連線，建議使用多路複用。Java 和 Go 支援多路複用。如需 Java 實作詳細資料，請參閱「[使用多路複用](https://docs.cloud.google.com/bigquery/docs/write-api-streaming?hl=zh-tw#use_multiplexing)」。如需 Go 實作詳細資料，請參閱「[連線共用 (多工處理)](https://pkg.go.dev/cloud.google.com/go/bigquery/storage/managedwriter#hdr-Connection_Sharing__Multiplexing_)」。如果您使用[至少一次語意 Beam 連接器](https://beam.apache.org/documentation/io/built-in/google-bigquery/#at-least-once-semantics)，可以透過 [UseStorageApiConnectionPool](https://beam.apache.org/releases/javadoc/current/org/apache/beam/sdk/io/gcp/bigquery/BigQueryOptions.html#setUseStorageApiConnectionPool-java.lang.Boolean-) 啟用多路複用。Managed Service for Apache Spark 連接器預設會啟用多路複用。

為獲得最佳效能，請盡可能使用單一連線寫入大量資料。請勿只使用一個連線進行單一寫入作業，也不要為許多小型寫入作業開啟及關閉串流。

每個專案可同時開啟的[並行連線](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#concurrent_connections)數量有配額限制。超過上限後，對 `AppendRows` 的呼叫就會失敗。
不過，您可以提高並行連線的配額，因此通常不會成為擴充的限制因素。

每次呼叫 `AppendRows` 時，都會建立新的資料寫入器物件。因此，使用應用程式建立的串流時，連線數量會對應至已建立的串流數量。一般而言，單一連線至少支援 1MBps 的總處理量。上限取決於多項因素，例如網路頻寬、資料結構定義和伺服器負載，但可能超過 10 MBps。

此外，[每項專案的總處理量](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#writeapi_throughput)也有配額。這代表透過 Storage Write API 服務的所有連線每秒流動的位元組數。如果專案超出這項配額，可以[要求調整配額](https://docs.cloud.google.com/docs/quotas/help/request_increase?hl=zh-tw)。通常這會涉及以相同比例提高相關配額，例如並行連線配額。

## 管理串流偏移，實現「僅限一次」語意

Storage Write API 只允許寫入目前串流的結尾，而這個結尾會隨著資料附加而移動。串流中的目前位置會指定為從串流開頭算起的偏移值。

寫入應用程式建立的串流時，您可以指定串流偏移，以實現僅一次寫入語意。

指定位移時，寫入作業會是等冪作業，因此可安全地因網路錯誤或伺服器無回應而重試。處理下列與位移相關的錯誤：

* `ALREADY_EXISTS` (`StorageErrorCode.OFFSET_ALREADY_EXISTS`)：資料列已寫入。您可以放心忽略這項錯誤。
* `OUT_OF_RANGE` (`StorageErrorCode.OFFSET_OUT_OF_RANGE`)：先前的寫入作業失敗。從上次成功寫入的位置重試。

請注意，如果設定的偏移值有誤，也可能發生這些錯誤，因此請務必謹慎管理偏移值。

使用串流偏移前，請先考量是否需要僅一次語意。舉例來說，如果上游資料管道僅保證至少寫入一次，或您可以在擷取資料後輕鬆偵測重複項目，則可能不需要精確寫入一次。在這種情況下，建議使用預設串流，不必追蹤資料列位移。

## 不要封鎖 `AppendRows` 通話

`AppendRows` 方法為非同步。您可以傳送一系列寫入作業，而不必個別封鎖每個寫入作業的回應。雙向連線上的回應訊息會按照要求加入佇列的順序傳送。如要達到最高總處理量，請呼叫 `AppendRows`，不要封鎖等待回應。

## 處理結構定義更新

在資料串流情境中，資料表結構定義通常是在串流管道外部管理。結構定義通常會隨著時間演進，例如新增可為空值的欄位。健全的管道必須處理頻外結構定義更新。

Storage Write API 支援的表格結構定義如下：

* 第一個寫入要求包含結構定義。
* 您會以二進位通訊協定緩衝區的形式傳送每個資料列。BigQuery 會將資料對應至結構定義。
* 您可以省略可為空值的欄位，但不能加入目前結構定義中沒有的欄位。如果您傳送含有額外欄位的資料列，Storage Write API 會傳回含有 `StorageErrorCode.SCHEMA_MISMATCH_EXTRA_FIELD` 的 [`StorageError`](https://docs.cloud.google.com/bigquery/docs/reference/storage/rpc/google.cloud.bigquery.storage.v1?hl=zh-tw#google.cloud.bigquery.storage.v1.StorageError)，並顯示 `StorageErrorCode.SCHEMA_MISMATCH_EXTRA_FIELD`。

如要在酬載中傳送新欄位，請先更新 BigQuery 中的資料表結構定義。儲存空間寫入 API 會在短時間內 (約幾分鐘) 偵測到結構定義變更。Storage Write API 偵測到結構定義變更時，[`AppendRowsResponse`](https://docs.cloud.google.com/bigquery/docs/reference/storage/rpc/google.cloud.bigquery.storage.v1?hl=zh-tw#google.cloud.bigquery.storage.v1.AppendRowsResponse) 回應訊息會包含 `TableSchema` 物件，說明新的結構定義。

如要使用更新後的結構定義傳送資料，請關閉現有連線，並使用新結構定義開啟新連線。

**Java 用戶端**。Java 用戶端程式庫透過 [`JsonStreamWriter`](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquerystorage/latest/com.google.cloud.bigquery.storage.v1.JsonStreamWriter?hl=zh-tw) 類別，提供一些額外的結構定義更新功能。架構更新後，`JsonStreamWriter` 會自動重新連線至更新後的架構。您不需要明確關閉並重新開啟連線。
如要透過程式輔助檢查結構定義變更，請在 `append` 方法完成後呼叫 [`AppendRowsResponse.hasUpdatedSchema`](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquerystorage/latest/com.google.cloud.bigquery.storage.v1.AppendRowsResponse?hl=zh-tw#com_google_cloud_bigquery_storage_v1_AppendRowsResponse_getUpdatedSchema__)。

**注意：** 用戶端程式庫不會立即顯示結構定義更新，但會在幾分鐘內偵測到更新。

您也可以設定 `JsonStreamWriter`，忽略輸入資料中的不明欄位。如要設定這項行為，請呼叫 [`setIgnoreUnknownFields`](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquerystorage/latest/com.google.cloud.bigquery.storage.v1.JsonStreamWriter.Builder?hl=zh-tw#com_google_cloud_bigquery_storage_v1_JsonStreamWriter_Builder_setIgnoreUnknownFields_boolean_)。使用舊版 [`tabledata.insertAll`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tabledata/insertAll?hl=zh-tw) API 時，這項行為與 `ignoreUnknownValues` 選項類似。不過，這可能會導致資料意外遺失，因為系統會自動捨棄不明欄位。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-09 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-09 (世界標準時間)。"],[],[]]