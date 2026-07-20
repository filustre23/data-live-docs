Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [參考資料](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# API 上傳作業

媒體上傳功能可讓 BigQuery API 將資料儲存至雲端，以供伺服器使用。使用者可能想上傳的資料種類包括相片、影片、PDF 檔案、ZIP 檔案，或是任何其他類型的資料。

## 上傳選項

BigQuery API 可讓您上傳特定類型的二進位資料或媒體。您可以針對支援媒體上傳作業的任何方法，在相關參照頁面上指定可上傳的資料特性：

* 「Maximum upload file size」：您可以使用這個方法儲存的資料量上限。
* 「Accepted media MIME types」：您可以使用這個方法儲存的二進位資料類型。

您可以透過下列任何一種方式提出上傳要求。請利用 `uploadType` 要求參數，指定您要使用的方法。

* [多部分上傳作業](#multipart)：`uploadType=multipart`。適合為較小型的檔案和中繼資料進行快速的傳輸作業；可在單一要求中，將檔案與描述該檔案的中繼資料一起傳輸完畢。
* [支援續傳的上傳作業](#resumable)：`uploadType=resumable`。可靠的傳輸作業，對於較大型的檔案特別重要。透過這個方法，您可以使用工作階段啟動要求，其中可以選擇是否包含中繼資料。對於大多數的應用程式而言，這是不錯的策略，因為這也適用於較小型的檔案，您只需要為每次上傳作業額外支付一次 HTTP 要求的費用即可。

當您上傳媒體時，會使用特殊的 URI。事實上，支援媒體上傳作業的方法都有兩個 URI 端點：

* **/upload URI，適用於媒體**。上傳端點的格式，就是標準資源 URI 加上「/upload」前置字串。傳輸媒體資料本身時，請使用這個 URI。

  範例：`POST /upload/bigquery/v2/projects/projectId/jobs`
* **標準資源 URI，適用於中繼資料。**如果資源包含任何資料欄位，這些欄位會用來儲存描述已上傳檔案的中繼資料。建立或更新中繼資料值時，可以使用這個 URI。

  示例：
  `POST /bigquery/v2/projects/projectId/jobs`

### 多部分上傳作業

如果您有要隨資料一起上傳的中繼資料，可以提出單一 `multipart/related` 要求。如果您要傳送的資料小到足以在連線失敗時再完整上傳一次，這就是個不錯的選擇。

如要使用多部分上傳作業，請向方法的 **/upload** URI 發出 `POST` 要求，並新增查詢參數 `uploadType=multipart`，例如：

```
POST https://www.googleapis.com/upload/bigquery/v2/projects/projectId/jobs?uploadType=multipart
```

提出多部分上傳要求時，要使用的頂層 HTTP 標頭包括：

* `Content-Type`：請設定成 multipart/related，並加入要用來辨識各個要求部分的邊界字串。
* `Content-Length`：請設定成要求主體中的位元組總數。要求中的媒體部分，必須小於針對這個方法指定的檔案大小上限。

要求主體的格式為 `multipart/related` 內容類型 [[RFC2387](https://datatracker.ietf.org/doc/html/rfc2387)]，其中包含兩個部分。這些部分是靠邊界字串來辨識的，而緊接在最後一個邊界字串後面會有兩個連字號。

多部分要求的每個部分都需要一個額外的 `Content-Type` 標頭：

1. **中繼資料部分：**必須是要求的第一個部分，且 `Content-Type` 必須符合系統接受的其中一種中繼資料格式。
2. **媒體部分：**必須是要求的第二個部分，且 `Content-Type` 必須符合該方法可接受的其中一種媒體 MIME 類型。

如要瞭解每個方法的可接受媒體 MIME 類型清單，以及上傳檔案的大小限制，請參閱 API [參考資料](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs/insert?hl=zh-tw)。

**注意：**如果您只需要建立或更新中繼資料部分，不會上傳相關聯的資料，您只要把 `POST` 或 `PUT` 要求傳送給標準資源端點即可：`https://www.googleapis.com/bigquery/v2/projects/projectId/jobs`

#### 範例：多部分上傳作業

以下範例顯示 BigQuery API 的多部分上傳要求。

```
POST /upload/bigquery/v2/projects/projectId/jobs?uploadType=multipart HTTP/1.1
Host: www.googleapis.com
Authorization: Bearer your_auth_token
Content-Type: multipart/related; boundary=foo_bar_baz
Content-Length: number_of_bytes_in_entire_request_body

--foo_bar_baz
Content-Type: application/json; charset=UTF-8

{
  "configuration": {
    "load": {
      "sourceFormat": "NEWLINE_DELIMITED_JSON",
      "schema": {
        "fields": [
          {"name": "f1", "type": "STRING"},
          {"name": "f2", "type": "INTEGER"}
        ]
      },
      "destinationTable": {
        "projectId": "projectId",
        "datasetId": "datasetId",
        "tableId": "tableId"
      }
    }
  }
}


--foo_bar_baz
Content-Type: */*

CSV, JSON, AVRO, PARQUET, or ORC data
--foo_bar_baz--
```

如果要求成功，伺服器會傳回 HTTP `200 OK` 狀態碼，以及所有中繼資料：

```
HTTP/1.1 200
Content-Type: application/json

{
  "configuration": {
    "load": {
      "sourceFormat": "NEWLINE_DELIMITED_JSON",
      "schema": {
        "fields": [
          {"name": "f1", "type": "STRING"},
          {"name": "f2", "type": "INTEGER"}
        ]
      },
      "destinationTable": {
        "projectId": "projectId",
        "datasetId": "datasetId",
        "tableId": "tableId"
      }
    }
  }
}
```

### 支援續傳的上傳作業

如要更可靠地上傳資料檔案，您可以使用支援續傳的上傳通訊協定。這個通訊協定可讓您在通訊問題導致上傳作業的資料傳輸過程中斷之後，能夠繼續執行上傳作業。如果您要傳輸大型檔案，而且發生網路中斷或其他傳輸問題的可能性很高 (例如從行動裝置用戶端應用程式上傳時)，這種方法就特別有用。這方法也能在網路發生問題時降低頻寬用量，因為您不需要從頭開始上傳大型檔案。

使用支援續傳的上傳作業的步驟包括：

1. [啟動可續傳工作階段](#start-resumable)。對包含中繼資料 (如果有的話) 的上傳 URI 提出初始要求。
2. [儲存可續傳工作階段 URI](#save-session-uri)。儲存在初始要求回應中傳回的工作階段 URI；您會在這個工作階段的剩餘要求中用到它。
3. [上傳檔案](#upload-resumable)。將媒體檔案傳送到可續傳工作階段 URI。

此外，使用可續傳上傳功能的應用程式，必須擁有[繼續執行中斷的上傳作業](#resume-upload)小節中的程式碼。如果上傳作業中斷，請找出已成功接收多少資料，然後從那一點開始續傳。

**注意：**上傳 URI 會在一週後失效。

#### 步驟 1：啟動可續傳的工作階段

如要啟動可續傳上傳作業，請向方法的 **/upload** URI 發出 `POST` 要求，並新增查詢參數 `uploadType=resumable`，例如：

```
POST https://www.googleapis.com/upload/bigquery/v2/projects/projectId/jobs?uploadType=resumable
```

這個初始要求的主體會是空白的，或是只包含中繼資料；您將在後續的要求中，傳輸您要上傳的檔案中的實際內容。

請將下列 HTTP 標頭與初始要求搭配使用：

* `X-Upload-Content-Type`：請設定為要在後續要求中傳輸的上傳資料媒體 MIME 類型。
* `X-Upload-Content-Length`：請設定為要在後續要求中傳輸的上傳資料位元組數。如果您在提出該要求時不知道這個位元組數，可以省略這個標頭。
* 如果要提供中繼資料，請使用 `Content-Type`。請根據中繼資料的資料類型來設定。
* `Content-Length`：請設定為您在該初始要求主體中提供的位元組數。如果您要使用[區塊傳輸編碼](https://datatracker.ietf.org/doc/html/rfc7230#section-4.1)，就不需要這個標頭。

如要瞭解每個方法的可接受媒體 MIME 類型清單，以及上傳檔案的大小限制，請參閱 API [參考資料](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs/insert?hl=zh-tw)。

##### 範例：可續傳工作階段啟動要求

以下範例顯示，如何針對 BigQuery API 啟動可續傳的工作階段。

```
POST /upload/bigquery/v2/projects/projectId/jobs?uploadType=resumable HTTP/1.1
Host: www.googleapis.com
Authorization: Bearer your_auth_token
Content-Length: 38
Content-Type: application/json; charset=UTF-8
X-Upload-Content-Type: */*
X-Upload-Content-Length: 2000000

{
  "configuration": {
    "load": {
      "sourceFormat": "NEWLINE_DELIMITED_JSON",
      "schema": {
        "fields": [
          {"name": "f1", "type": "STRING"},
          {"name": "f2", "type": "INTEGER"}
        ]
      },
      "destinationTable": {
        "projectId": "projectId",
        "datasetId": "datasetId",
        "tableId": "tableId"
      }
    }
  }
}
```

**注意：**針對不含中繼資料的初始可續傳更新要求，請將要求主體留白，並將 `Content-Length` 標頭設定為 `0`。

下一節將說明如何處理回應。

#### 步驟 2：儲存可續傳的工作階段 URI

如果工作階段啟動要求成功，API 伺服器就會傳回包含 `200 OK` HTTP 狀態碼的回應。此外，API 伺服器還提供會指定可續傳工作階段 URI 的 `Location` 標頭。如以下範例所示，`Location` 標頭包含 `upload_id` 查詢參數，可提供這個工作階段所用的唯一上傳 ID。

##### 範例：可續傳工作階段啟動作業的回應

以下是步驟 1 中要求的回應：

```
HTTP/1.1 200 OK
Location: https://www.googleapis.com/upload/bigquery/v2/projects/projectId/jobs?uploadType=resumable&upload_id=xa298sd_sdlkj2
Content-Length: 0
```

如以上回應範例所示，`Location` 標頭的值，就是您將做為 HTTP 端點的工作階段 URI，且這個 HTTP 端點將用於執行實際檔案上傳作業或查詢上傳狀態。

請複製並儲存工作階段 URI，好讓您能夠在後續的要求中使用。

#### 步驟 3：上傳檔案

如要上傳檔案，請傳送 `PUT` 要求給您在上一個步驟中取得的上傳 URI。上傳要求的格式如下：

```
PUT session_uri
```

當您在提出可續傳檔案上傳要求時，要使用的 HTTP 標頭包含 `Content-Length`。請把它設定為您要在這個要求中上傳的位元組數，這通常就是上傳檔案的大小。

##### 範例：可續傳檔案上傳要求

以下是要在目前的範例中，上傳完整的 2,000,000 位元組 CSV、JSON、AVRO 或 PARQUET 檔案的可續傳要求。

```
PUT https://www.googleapis.com/upload/bigquery/v2/projects/projectId/jobs?uploadType=resumable&upload_id=xa298sd_sdlkj2 HTTP/1.1
Content-Length: 2000000
Content-Type: */*

bytes 0-1999999
```

如果要求成功，伺服器會傳回包含 `HTTP 201 Created` 的回應，加上與這個資源相關聯的所有中繼資料。如果可續傳工作階段的初始要求曾經是 `PUT`，如要更新現有資源，成功的回應就會是 `200 OK`，加上與這個資源相關聯的所有中繼資料。

如果上傳要求中斷，或是您從伺服器收到 `HTTP 503 Service Unavailable` 或任何其他的 `5xx` 回應，請依照[繼續執行中斷的上傳作業](#resume-upload)小節所述的程序進行。

---

##### 將檔案以區塊的形式上傳

透過可續傳的上傳作業，您可將檔案切割為片段，然後傳送一系列要求來依序上傳每個片段。這不是大家偏好的方式，因為您必須承擔與額外的要求相關聯的效能成本，而這通常是沒有必要的。然而，您可能需要使用切割成區塊的方式，減少要在任何單一要求中傳輸的資料量。當個別的要求有固定的時間限制時，這方式就很有用，對於 Google App Engine 要求的某些類別而言也是如此。這方式也能讓您做些其他的事，例如讓預設不支援顯示上傳進度的舊版瀏覽器顯示上傳進度。

###### 展開以顯示更多資訊

如果您要以區塊的形式上傳資料，您還需要 `Content-Range` 標頭，以及完整檔案上傳作業所需的 `Content-Length` 標頭：

* `Content-Length`：請設定為區塊大小，或是更少的位元組，因為最後一個要求的資料傳輸量就可能會小於區塊大小。
* [`Content-Range`](https://datatracker.ietf.org/doc/html/rfc7233#section-4.2)：請設定來顯示您要上傳檔案中的哪些位元組。舉例來說，`Content-Range: bytes 0-524287/2000000` 代表您要提供 2,000,000 位元組檔案中的前 524,288 個位元組 (256 x 1024 x 2)。

區塊大小限制：所有區塊的大小都必須是 256 KB 的倍數 (256 x 1024 位元組)，但會完成上傳作業的最後一個區塊除外。如果您要以區塊的形式上傳檔案，請務必要讓區塊大一點，以保持上傳效率。

##### 範例：可續傳區塊分割檔案上傳要求

傳送前 524,288 個位元組的要求可能會像是：

```
PUT {session_uri} HTTP/1.1
Host: www.googleapis.com
Content-Length: 524288
Content-Type: */*
Content-Range: bytes 0-524287/2000000

bytes 0-524288
```

如果要求成功，伺服器會傳回包含 `308 Resume Incomplete` 的回應，加上能辨識當下已儲存的位元組總數的 `Range` 標頭：

```
HTTP/1.1 308 Resume Incomplete
Content-Length: 0
Range: bytes=0-524287
```

請使用在 `Range` 標頭中傳回的上限值，決定下一個區塊要從哪裡開始。請繼續對檔案的每個區塊執行 `PUT`，直到整個檔案上傳完畢為止。

如果有任何區塊的 `PUT` 要求中斷，或是您從伺服器收到 HTTP `503 Service Unavailable` 或任何其他的 `5xx` 回應，請依照[繼續執行中斷的上傳作業](#resume-upload)小節所述的程序進行，但請勿上傳檔案的剩餘部分，而是要直接從那一點繼續上傳區塊。

**重要注意事項：**

* 請務必使用回應中的 `Range` 標頭，決定下一個區塊要從哪裡開始；請勿假設伺服器已收到在前一個要求中傳送的所有位元組。
* 每個上傳 URI 的生命都是有限的，最終都會過期 (如果沒有使用的話，大約會在一天內過期)。因此，我們強烈建議您在取得上傳 URI 之後，盡快開始可續傳上傳作業，還要在上傳作業中斷之後盡快繼傳。
* 如果您傳送的要求包含過期的上傳工作階段 ID，伺服器會傳回 `404 Not Found` 狀態碼。當上傳工作階段發生無法復原的錯誤時，伺服器會傳回 `410 Gone` 狀態碼。在這種情況下，您必須開始新的可續傳上傳作業、取得新的上傳 URI，然後利用新的端點從頭開始上傳。

當整個檔案上傳完畢時，伺服器會傳回包含 `HTTP 201 Created` 的回應，加上與這個資源相關聯的所有中繼資料。如果這個要求已更新現有的實體，而非建立新的實體，已完成上傳作業的 HTTP 回應碼就會是 `200 OK`。

---

#### 繼續執行中斷的上傳作業

如果上傳要求在您收到回應之前就終止了，或是您收到伺服器傳回的 HTTP `503 Service Unavailable` 回應，您就必須繼續執行中斷的上傳作業。現在說明一下操作方式：

1. **要求狀態：**請向上傳 URI 提出空白的 `PUT` 要求，以便查詢上傳作業目前的狀態。針對這個要求，HTTP 標頭應該包含會指出目前在檔案中位置不明的 `Content-Range`。舉例來說，如果檔案的總長度是 2,000,000，請將 `Content-Range` 設定為 `*/2000000`。如果您不知道檔案的完整大小，請將 `Content-Range` 設定為 `*/*`。

   **附註：**您可以在不同區塊的上傳作業之間提出狀態要求，而不是只能在上傳中斷時提出要求。舉例來說，當您要讓舊版瀏覽器顯示上傳進度時，這功能就很有用。
2. **取得已上傳的位元組數：**請處理狀態查詢的回應。伺服器會在自己的回應中使用 `Range` 標頭，指出當下已接收到哪些位元組。舉例來說，如果 `Range` 標頭是 `0-299999`，代表伺服器已接收到檔案的前 300,000 個位元組。
3. **上傳剩餘的資料：**最後，既然您已經知道要從哪裡繼續提出要求，請傳送剩餘的資料或目前的區塊。請注意，無論如何，您都必須要把剩餘的資料當做單獨的區塊來處理，因此您必須在繼續執行上傳作業時傳送 `Content-Range` 標頭。

##### 範例：繼續執行中斷的上傳作業

1) 要求上傳狀態。

以下要求使用 `Content-Range` 標頭，指出目前在 2,000,000 位元組檔案中的位置不明。

```
PUT {session_uri} HTTP/1.1
Content-Length: 0
Content-Range: bytes */2000000
```

2) 從回應擷取當下已經上傳的位元組數。

伺服器的回應會使用 `Range` 標頭，指出伺服器當下已經收到檔案的前 43 個位元組。請使用在 `Range` 標頭中的上限值，決定要從哪裡繼續上傳。

```
HTTP/1.1 308 Resume Incomplete
Content-Length: 0
Range: 0-42
```

**注意：**如果上傳作業已經完成，狀態回應可能會是 `201 Created` 或 `200 OK`。如果連線在所有位元組都已上傳之後，但在用戶端收到伺服器的回應之前中斷，就可能發生這種情況。

3) 從上次離開的位置續傳上傳作業。

以下要求透過傳送檔案的剩餘位元組 (從位元組 43 開始) 續傳上傳作業。

```
PUT {session_uri} HTTP/1.1
Content-Length: 1999957
Content-Range: bytes 43-1999999/2000000

bytes 43-1999999
```

## 最佳做法

當您要上傳媒體時，瞭解幾個與錯誤處理相關的最佳做法是很有用的。

* 請繼續或重新執行因連線中斷或因任何 `5xx` 錯誤導致失敗的上傳作業，這些錯誤包括：
  + `500 Internal Server Error`
  + `502 Bad Gateway`
  + `503 Service Unavailable`
  + `504 Gateway Timeout`
* 如果您在繼續或重試上傳要求時，收到任何 `5xx` 伺服器錯誤，請使用[指數輪詢](#exp-backoff)策略。如果伺服器超載，就可能發生這些錯誤。在發生大量要求或存在繁重網路流量期間，指數輪詢可協助減輕這一類問題。
* 其他類型的要求不應透過指數輪詢處理，但您仍可重試其中一些要求。重試這些要求時，請限制重試的次數。舉例來說，您的程式碼可能會限制為在最多重試十次之後，才會回報錯誤。
* 如要處理在執行可續傳上傳作業時收到的 `404 Not Found` 和 `410 Gone` 錯誤，請從頭開始執行整個上傳作業。

### 指數輪詢

指數輪詢是網路應用程式的標準錯誤處理策略，用戶端可透過這種策略，以逐漸增加的次數定期重試失敗的要求。如果大量要求或繁重的網路流量導致伺服器傳回錯誤，指數輪詢就是處理這類錯誤的一種不錯的策略。相反地，處理與網路流量或回應時間相關的錯誤 (例如授權憑證無效或找不到檔案的錯誤) 並不是很有意義的策略。

在正確的使用之下，指數輪詢可以提升頻寬使用的效率，減少取得成功回應所需的要求數，並最大化並行環境中的要求總處理量。

實作簡單指數輪詢的流程如下：

1. 對 API 提出要求。
2. 收到指出您應該要重試要求的 `HTTP 503` 回應。
3. 等待 1 秒鐘 + random\_number\_milliseconds 毫秒，然後重試要求。
4. 收到指出您應該要重試要求的 `HTTP 503` 回應。
5. 等待 2 秒鐘 + random\_number\_milliseconds 毫秒，然後重試要求。
6. 收到指出您應該要重試要求的 `HTTP 503` 回應。
7. 等待 4 秒鐘 + random\_number\_milliseconds 毫秒，然後重試要求。
8. 收到指出您應該要重試要求的 `HTTP 503` 回應。
9. 等待 8 秒鐘 + random\_number\_milliseconds 毫秒，然後重試要求。
10. 收到指出您應該要重試要求的 `HTTP 503` 回應。
11. 等待 16 秒鐘 + random\_number\_milliseconds 毫秒，然後重試要求。
12. 停止。報告或記錄錯誤。

在以上流程中，random\_number\_milliseconds 是小於或等於 1000 的隨機毫秒數。這是必要的，因為使用較小的隨機延遲有助於更平均地分散負載，並避免對伺服器產生衝擊的可能性。必須在每次等待之後重新定義 random\_number\_milliseconds 的值。

**注意：**等待時間一律是 (2 ^ n) + random\_number\_milliseconds，其中 n 是一開始定義為 0 的單調遞增整數。對於每個疊代 (每次要求)，整數 n 會遞增 1。

演算法已設定為會在 n 等於 5 時終止。這個上限可以防止用戶端一直重試下去，導致要求在總延遲時間達到約 32 秒之後，才會被視為「無法復原的錯誤」。您可以把重試次數的上限設高一點，尤其是在大型上傳作業執行的過程中；但請確保要把重試延遲時間的上限設定在合理的地方，例如短於一分鐘。

### API 用戶端程式庫指南

* [.NET](https://developers.google.com/api-client-library/dotnet/guide/media_upload?hl=zh-tw)
* [Java](https://developers.google.com/api-client-library/java/google-api-java-client/media-upload?hl=zh-tw)
* [PHP](https://github.com/googleapis/google-api-php-client/blob/master/docs/media.md)
* [Python](https://github.com/googleapis/google-api-python-client/blob/master/docs/media.md)
* [Ruby](https://github.com/googleapis/google-api-ruby-client/blob/master/docs/usage-guide.md#media)




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-04-21 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-04-21 (世界標準時間)。"],[],[]]