Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# BigQuery Storage Write API (gRPC) 最佳做法

您可以調整應用程式建立串流、集區連線和批次要求的方式，透過 BigQuery Storage Write API (gRPC) 最大化寫入處理量，並避免配額瓶頸。謹慎處理偏移和結構定義更新，也有助於在資料表結構定義演變時，保持擷取管道的彈性。如需基礎串流概念，請參閱「[BigQuery Storage Write API (gRPC) 總覽](https://docs.cloud.google.com/bigquery/docs/write-api?hl=zh-tw#overview)」。

## 限制串流建立頻率

建立串流前，請先考量是否可以使用[預設串流](https://docs.cloud.google.com/bigquery/docs/write-api?hl=zh-tw#default_stream)。在串流情境中，預設串流的配額限制較少，且擴充性優於應用程式建立的串流。如果您使用應用程式建立的串流，請務必先充分利用每個串流的最大處理量，再建立其他串流。例如，使用[非同步寫入](#do_not_block_on_appendrows_calls)。

如果是應用程式建立的串流，請避免頻繁呼叫 `CreateWriteStream`。一般來說，如果每秒呼叫次數超過 40 到 50 次，API 呼叫的延遲時間會大幅增加 (>25 秒)。請確認應用程式可以接受冷啟動，並逐步增加串流數量，以及限制 `CreateWriteStream` 呼叫的頻率。您也可以設定較長的期限，等待呼叫完成，以免發生 `DeadlineExceeded` 錯誤。`CreateWriteStream` 呼叫的最大速率也有長期[配額](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#createwritestream)。建立串流會耗用大量資源，因此降低串流建立速率並充分利用現有串流，是避免超過這項限制的最佳方式。

## 連線集區管理

`AppendRows` 方法會建立與串流的雙向連線。您可以在預設串流上開啟多個連線，但在應用程式建立的串流上，只能開啟一個有效連線。

使用預設串流時，您可以透過 Storage Write API (gRPC) 多工處理，使用共用連線寫入多個目的地資料表。多工處理會集結連線，提高處理量和資源使用率。如果工作流程有超過 20 個並行連線，建議使用多工處理。多工處理適用於 Java 和 Go。如需 Java 實作詳細資料，請參閱「[使用多工處理](https://docs.cloud.google.com/bigquery/docs/write-api-streaming?hl=zh-tw#use_multiplexing)」。如要瞭解 Go 實作詳情，請參閱「[連線共用 (多工處理)](https://pkg.go.dev/cloud.google.com/go/bigquery/storage/managedwriter#hdr-Connection_Sharing__Multiplexing_)」。如果您使用[至少一次語意的 Beam 連接器](https://beam.apache.org/documentation/io/built-in/google-bigquery/#at-least-once-semantics)，可以透過 [UseStorageApiConnectionPool](https://beam.apache.org/releases/javadoc/current/org/apache/beam/sdk/io/gcp/bigquery/BigQueryOptions.html#setUseStorageApiConnectionPool-java.lang.Boolean-) 啟用多工處理。Managed Service for Apache Spark 連接器預設會啟用多工處理功能。

為達到最佳效能，請盡可能使用單一連線寫入多筆資料。請勿只為單一寫入作業使用一個連線，或為許多小型寫入作業開啟及關閉串流。

每個專案可同時開啟的[並行連線](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#concurrent_connections)數量有配額限制。超過上限時，對 `AppendRows` 的呼叫會失敗。不過，並行連線的配額可以提高，通常不會成為擴充的限制因素。

每次呼叫 `AppendRows` 都會建立新的資料寫入器物件。因此，使用應用程式建立的串流時，連線數量會對應到已建立的串流數量。一般來說，單一連線至少支援 1 MBps 的處理量。上限取決於多項因素，例如網路頻寬、資料架構和伺服器負載，但可能超過 10 MBps。

[每項專案的總處理量](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#writeapi_throughput)也有配額限制。這代表透過 Storage Write API (gRPC) 服務傳輸的所有連線每秒位元組數。如果專案超過這項配額，您可以[要求調整配額](https://docs.cloud.google.com/docs/quotas/help/request_increase?hl=zh-tw)。通常這涉及以相同比例提高伴隨配額，例如並行連線配額。

## 管理串流偏移，實現僅一次語意

Storage Write API (gRPC) 僅允許寫入串流目前的結尾，該結尾會隨著資料附加而移動。串流中的目前位置會指定為從串流開頭算起的偏移量。

寫入應用程式建立的串流時，您可以指定串流偏移量，達到僅一次寫入語意。

指定偏移量後，寫入作業會具有冪等性，因此在發生網路錯誤或伺服器無回應時，可以安全地重試。處理下列與偏移量相關的錯誤：

* `ALREADY_EXISTS` (`StorageErrorCode.OFFSET_ALREADY_EXISTS`)：資料列已寫入。您可以放心忽略這項錯誤。
* `OUT_OF_RANGE` (`StorageErrorCode.OFFSET_OUT_OF_RANGE`)：先前的寫入作業失敗。從上次成功寫入的位置重試。

請注意，如果設定錯誤的偏移值，也可能發生這些錯誤，因此您必須謹慎管理偏移。

使用串流偏移前，請先考量是否需要僅一次語意。舉例來說，如果上游資料管道僅保證至少寫入一次，或者您可以在資料擷取後輕鬆偵測重複項目，則可能不需要僅寫入一次。在這種情況下，建議您使用預設串流，這樣就不必追蹤資料列偏移。

## 不要封鎖 `AppendRows` 呼叫

`AppendRows` 方法為非同步性質。您可以傳送一系列寫入作業，而不必個別封鎖每個寫入作業的回應。雙向連線上的回應訊息會按照要求排入佇列的順序抵達。如要達到最高處理量，請呼叫 `AppendRows`，不要封鎖等待回應。

## 偏好較大的要求

每項傳送的要求都會在用戶端和伺服器端產生處理負擔。為提高效率，請盡可能傳送大型要求 (大於 1 MB)。

## 處理結構定義更新

在資料串流情境中，資料表結構定義通常是在串流管道外管理。結構定義通常會隨著時間演變，例如新增可為空值的欄位。穩健的管道必須能處理頻外結構定義更新。

Storage Write API (gRPC) 支援下列資料表結構定義：

* 第一個寫入要求包含結構定義。
* 您會以二進位通訊協定緩衝區的形式傳送每個資料列。BigQuery 會將資料對應至結構定義。
* 您可以省略可為空值的欄位，但不能加入目前結構定義中沒有的欄位。如果傳送的資料列含有額外欄位，Storage Write API (gRPC) 會傳回 [`StorageError`](https://docs.cloud.google.com/bigquery/docs/reference/storage/rpc/google.cloud.bigquery.storage.v1?hl=zh-tw#google.cloud.bigquery.storage.v1.StorageError) 和 `StorageErrorCode.SCHEMA_MISMATCH_EXTRA_FIELD`。

如要在酬載中傳送新欄位，請先更新 BigQuery 中的資料表結構定義。Storage Write API (gRPC) 會在短時間內 (幾分鐘內) 偵測到結構定義變更。Storage Write API (gRPC) 偵測到結構定義變更時，[`AppendRowsResponse`](https://docs.cloud.google.com/bigquery/docs/reference/storage/rpc/google.cloud.bigquery.storage.v1?hl=zh-tw#google.cloud.bigquery.storage.v1.AppendRowsResponse) 回應訊息會包含描述新結構定義的 `TableSchema` 物件。

如要使用更新後的結構定義傳送資料，您必須關閉現有連線，並使用新的結構定義開啟新連線。

**Java 用戶端**。Java 用戶端程式庫透過 [`JsonStreamWriter`](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquerystorage/latest/com.google.cloud.bigquery.storage.v1.JsonStreamWriter?hl=zh-tw) 類別，提供一些額外的結構定義更新功能。結構定義更新後，`JsonStreamWriter` 會自動重新連結至更新後的結構定義。您不需要明確關閉並重新開啟連線。如要透過程式輔助檢查結構定義變更，請在 `append` 方法完成後呼叫 [`AppendRowsResponse.hasUpdatedSchema`](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquerystorage/latest/com.google.cloud.bigquery.storage.v1.AppendRowsResponse?hl=zh-tw#com_google_cloud_bigquery_storage_v1_AppendRowsResponse_getUpdatedSchema__)。

**注意：** 用戶端程式庫不會立即顯示結構定義更新，但會在幾分鐘內偵測到。

您也可以設定 `JsonStreamWriter`，忽略輸入資料中的未知欄位。如要設定這項行為，請呼叫 [`setIgnoreUnknownFields`](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquerystorage/latest/com.google.cloud.bigquery.storage.v1.JsonStreamWriter.Builder?hl=zh-tw#com_google_cloud_bigquery_storage_v1_JsonStreamWriter_Builder_setIgnoreUnknownFields_boolean_)。這項行為與使用 [BigQuery Storage Write API (REST)](https://docs.cloud.google.com/bigquery/docs/streaming-data-into-bigquery?hl=zh-tw) 時的 `ignoreUnknownValues` 選項類似。不過，由於系統會自動捨棄不明欄位，因此可能會導致資料意外遺失。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-10-30 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-10-30 (世界標準時間)。"],[],[]]