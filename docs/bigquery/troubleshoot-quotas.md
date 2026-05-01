* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [參考資料](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 排解配額和限制錯誤

BigQuery 有各式各樣的[配額與限制](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)，可限制不同要求和作業的頻率和數量。配額的用途是保護基礎架構，並避免客戶產生超出預期的用量。本文說明如何診斷及減輕配額和限制造成的特定錯誤。

部分錯誤訊息會指出可提高的配額或限制，其他錯誤訊息則會指出無法提高的配額或限制。達到硬性限制表示您需要為工作負載導入暫時或永久的替代方案，或是最佳做法。即使配額或限制可以提高，也建議您這麼做。

本文會根據這些類別整理錯誤訊息和解決方案，而本文稍後的「總覽」一節會說明如何解讀錯誤訊息，並針對問題套用正確的解決方案。

如果這份文件未列出您的錯誤訊息，請參閱[錯誤訊息清單](https://docs.cloud.google.com/bigquery/docs/error-messages?hl=zh-tw)，其中提供更多一般錯誤資訊。

## 總覽

如果 BigQuery 作業因超出配額而失敗，API 會傳回 HTTP `403 Forbidden` 狀態碼。回應主體會進一步說明已達到的配額。回應主體看起來會與下列內容類似：

```
{
  "code" : 403,
  "errors" : [ {
    "domain" : "global",
    "message" : "Quota exceeded: ...",
    "reason" : "quotaExceeded"
  } ],
  "message" : "Quota exceeded: ..."
}
```

酬載中的 `message` 欄位會說明超出的限制。例如，`message` 欄位可能會顯示 `Exceeded rate limits: too many table
update operations for this table`。

一般來說，配額限制會被分為兩個類別，如回應酬載中的 `reason` 欄位所示。

* **`rateLimitExceeded`。**這個值表示短期限制。如要解決這些限制問題，請稍待幾秒再重試作業。在兩次重試之間使用「指數輪詢」。也就是說，每次重試之間的延遲時間會呈指數增加。
* **`quotaExceeded`。**這個值表示長期限制。如果您達到長期配額上限，則至少應等待 10 分鐘，然後再重試作業。如果您持續達到其中一項長期配額限制，則應分析您的工作負載，以便找出緩解問題的方法。將工作負載最佳化或要求增加配額都有可能緩解問題。

**注意事項：**部分配額會以每日配額表示。例如，[每個資料表的載入工作](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#load_jobs)數量設有每日配額。不過，系統會在 24 小時內以漸進的方式補充這些配額，因此您在達到上限後無須等候整整 24 小時。

如有 `quotaExceeded` 錯誤，請查看錯誤訊息，瞭解哪些配額已超過上限。接著分析工作負載，確認是否可以避免達到配額上限。

在某些情況下，您可以[與 BigQuery 支援團隊聯絡](https://docs.cloud.google.com/bigquery/docs/getting-support?hl=zh-tw)或[聯絡 Google Cloud 銷售人員](https://cloud.google.com/contact?hl=zh-tw)，並申請提高配額，但我們建議您先嘗試本文中的建議。

## 診斷

如要診斷問題，請按照下列步驟操作：

* 使用 [`INFORMATION_SCHEMA` 檢視表](https://docs.cloud.google.com/bigquery/docs/information-schema-tables?hl=zh-tw)和[區域限定符](https://docs.cloud.google.com/bigquery/docs/information-schema-intro?hl=zh-tw#region_qualifier)，分析基本問題。這些檢視表含有 BigQuery 資源的中繼資料，包括工作、預留項目和串流資料插入。

  舉例來說，以下查詢會使用 [`INFORMATION_SCHEMA.JOBS`](https://docs.cloud.google.com/bigquery/docs/information-schema-jobs?hl=zh-tw) 檢視表列出過去一天內所有配額相關錯誤：

  ```
  SELECT
  job_id,
  creation_time,
  error_result
  FROM  `region-REGION_NAME`.INFORMATION_SCHEMA.JOBS
  WHERE creation_time > TIMESTAMP_SUB(CURRENT_TIMESTAMP, INTERVAL 1 DAY) AND
      error_result.reason IN ('rateLimitExceeded', 'quotaExceeded')
  ```

  將 `REGION_NAME` 替換為專案的區域。前面必須加上 `region-`。舉例來說，如果是 `US` 多區域，請使用 `region-us`。
* 查看 Cloud 稽核記錄中的錯誤。

  舉例來說，使用 [Logs Explorer](https://docs.cloud.google.com/logging/docs/view/logs-explorer-summary?hl=zh-tw) 時，以下查詢會在訊息字串中找出 `Quota exceeded` 或 `limit` 的錯誤：

  ```
  resource.type = ("bigquery_project" OR "bigquery_dataset")
  protoPayload.status.code ="7"
  protoPayload.status.message: ("Quota exceeded" OR "limit")
  ```

  在本例中，狀態碼 `7` 表示 [`PERMISSION_DENIED`](https://docs.cloud.google.com/tasks/docs/reference/rpc/google.rpc?hl=zh-tw#code)，這對應到 HTTP `403` 狀態碼。

  如需其他 Cloud 稽核記錄查詢範例，請參閱 [BigQuery 查詢](https://docs.cloud.google.com/logging/docs/view/query-library-preview?hl=zh-tw#bigquery-filters)。

## 解決可提高的配額或限制

您可以提高下列配額和限制，但建議先嘗試任何建議的解決方法或最佳做法。

### 專案掃描的免費查詢位元組數超出配額

在免費用量方案中執行查詢時，如果帳戶達到每月查詢上限，BigQuery 就會傳回這個錯誤。如要進一步瞭解查詢定價，請參閱[免費用量層級](https://cloud.google.com/bigquery/pricing?hl=zh-tw#free-usage-tier)。

**錯誤訊息**

```
Your project exceeded quota for free query bytes scanned
```

#### 解析度

如要繼續使用 BigQuery，請[將帳戶升級為 Cloud Billing 付費帳戶](https://docs.cloud.google.com/free/docs/gcp-free-tier?hl=zh-tw#how-to-upgrade)。

### 串流資料插入配額錯誤

本節提供相關提示，協助您排解以串流方式將資料傳入 BigQuery 時發生的配額錯誤。

在特定區域中，如果您並未在每個資料列的 `insertId` 欄位中填入資料，則串流資料插入會含有較高的配額。如要進一步瞭解串流資料插入的配額，請參閱[串流資料插入](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#streaming_inserts)。BigQuery 串流的配額相關錯誤取決於 `insertId` 是否存在。

**錯誤訊息**

如果 `insertId` 欄位為空白，則可能會發生下列配額錯誤：

| 配額限制 | 錯誤訊息 |
| --- | --- |
| 每項專案每秒位元組數 | 在區域 REGION 中專案 PROJECT\_ID gaia\_id 為 GAIA\_ID 的實體超過每秒插入位元組數的配額。 |

如果在 `insertId` 欄位填入資料，則可能會發生下列配額錯誤：

| 配額限制 | 錯誤訊息 |
| --- | --- |
| 每項專案每秒資料列數量 | 您在 REGION 的專案 PROJECT\_ID 超過每秒串流資料插入資料列的配額。 |
| 每個資料表每秒資料列數量 | 您的資料表 TABLE\_ID 超過每秒串流資料插入資料列的配額。 |
| 每個資料表每秒位元組數 | 您的資料表 TABLE\_ID 超出每秒串流資料插入位元組數的配額。 |

`insertId` 欄位的用途是簡化插入的資料列。如果同一個 `insertId` 的多個插入項目均於幾分鐘之內抵達，則 BigQuery 會寫入單一版本的記錄。但是，我們無法保證系統會自動刪除重複的內容。為了達到最大的串流總處理量，建議您不要加入 `insertId`，改成[手動刪除重複內容](https://docs.cloud.google.com/bigquery/docs/streaming-data-into-bigquery?hl=zh-tw#manually_removing_duplicates)。詳情請參閱[確保資料一致性](https://docs.cloud.google.com/bigquery/docs/streaming-data-into-bigquery?hl=zh-tw#dataconsistency)一文。

如果遇到這項錯誤，請[診斷問題](#ts-streaming-insert-quota-diagnose)，然後[按照建議步驟](#ts-streaming-insert-quota-resolution)解決問題。

#### 診斷

使用 [`STREAMING_TIMELINE_BY_*`](https://docs.cloud.google.com/bigquery/docs/information-schema-streaming?hl=zh-tw) 檢視表來分析串流流量。這些檢視表會每隔一分鐘匯總串流統計資料，並依 `error_code` 分類。結果中會顯示配額錯誤，且 `error_code` 等於 `RATE_LIMIT_EXCEEDED` 或 `QUOTA_EXCEEDED`。

根據已達到的特定配額上限查看 `total_rows` 或 `total_input_bytes`。如果錯誤是資料表層級的配額，請依 `table_id` 進行篩選。

舉例來說，下列查詢顯示每分鐘擷取的位元組總數和配額錯誤總數：

```
SELECT
 start_timestamp,
 error_code,
 SUM(total_input_bytes) as sum_input_bytes,
 SUM(IF(error_code IN ('QUOTA_EXCEEDED', 'RATE_LIMIT_EXCEEDED'),
     total_requests, 0)) AS quota_error
FROM
 `region-REGION_NAME`.INFORMATION_SCHEMA.STREAMING_TIMELINE_BY_PROJECT
WHERE
  start_timestamp > TIMESTAMP_SUB(CURRENT_TIMESTAMP, INTERVAL 1 DAY)
GROUP BY
 start_timestamp,
 error_code
ORDER BY 1 DESC
```

#### 解析度

如要解決這項配額錯誤，請按照下列步驟操作：

* 如果您使用 `insertId` 欄位來刪除重複的內容，而您的專案位於支援較高串流配額的區域，則建議移除 `insertId` 欄位。這個解決方案可能需要執行一些其他步驟，以手動方式刪除重複的資料內容。詳情請參閱[手動移除重複內容](https://docs.cloud.google.com/bigquery/docs/streaming-data-into-bigquery?hl=zh-tw#manually_removing_duplicates)。
* 如果您並非使用 `insertId`，或是無法加以移除，請監控 24 小時內的串流流量，並分析配額錯誤：

  + 如果您看到的大多是 `RATE_LIMIT_EXCEEDED` 錯誤而不是 `QUOTA_EXCEEDED` 錯誤，而您的整體流量低於配額的 80%，則這些錯誤可能表示流量暫時暴增。您可以在每次重試之間使用指數輪詢重試作業，以處理這些錯誤。
  + 如果您使用 Dataflow 工作插入資料，請考慮使用載入工作，而非串流插入。詳情請參閱「[設定插入方法](https://beam.apache.org/documentation/io/built-in/google-bigquery/#setting-the-insertion-method)」。如果您使用 Dataflow 和自訂 I/O 連接器，請考慮改用內建 I/O 連接器。詳情請參閱「[自訂 I/O 模式](https://beam.apache.org/documentation/patterns/custom-io/)」。
  + 如果您看到 `QUOTA_EXCEEDED` 錯誤，或整體流量持續超過配額的 80%，請提交增加配額的要求。詳情請參閱「[要求調整配額](https://docs.cloud.google.com/docs/quotas/help/request_increase?hl=zh-tw)」。
  + 您也可以考慮使用較新的 [Storage Write API](https://docs.cloud.google.com/bigquery/docs/write-api?hl=zh-tw) 取代串流插入，因為這項 API 的輸送量較高、價格較低，而且提供許多實用功能。

如要進一步瞭解串流資料插入，請參閱[以串流方式將資料傳入 BigQuery](https://docs.cloud.google.com/bigquery/docs/streaming-data-into-bigquery?hl=zh-tw) 一文。

### 包含遠端函式的並行查詢數量上限

如果含有遠端函式的並行查詢數量超過上限，BigQuery 就會傳回這項錯誤。

如要進一步瞭解遠端函式限制，請參閱「[遠端函式](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#remote_function_limits)」。

**錯誤訊息**

```
Exceeded rate limits: too many concurrent queries with remote functions for
this project
```

這項上限可以提高。請先嘗試解決方法和最佳做法。

#### 診斷

如要瞭解含有[遠端函式](https://docs.cloud.google.com/bigquery/docs/remote-functions?hl=zh-tw)的並行查詢限制，請參閱「[遠端函式限制](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#remote_function_limits)」。

#### 解析度

* 使用遠端函式時，請遵循[遠端函式的最佳做法](https://docs.cloud.google.com/bigquery/docs/remote-functions?hl=zh-tw#best_practices_for_remote_functions)。
* 如要要求增加配額，請與[支援團隊](https://docs.cloud.google.com/bigquery/docs/getting-support?hl=zh-tw)或[銷售人員](https://cloud.google.com/contact?hl=zh-tw)聯絡。審查及處理要求可能需要幾天的時間。建議在要求中說明優先順序、用途和專案 ID。

### `CREATE MODEL` 陳述式數量上限

這項錯誤表示您已超出 `CREATE MODEL` 陳述式的配額。

**錯誤訊息**

```
Quota exceeded: Your project exceeded quota for CREATE MODEL queries per
 project.
```

#### 解析度

如果超出 `CREATE MODEL` 陳述式的[配額](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#create_model_statements)，請傳送電子郵件至 [bqml-feedback@google.com](mailto:bqml-feedback@google.com)，要求增加配額。

### 每個專案每日的複製工作數量上限配額錯誤

如果專案中執行的複製工作數超過每日上限，BigQuery 就會傳回這項錯誤。如要進一步瞭解每日複製作業的限制，請參閱[複製作業](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#copy_jobs)。

**錯誤訊息**

```
Your project exceeded quota for copies per project
```

#### 診斷

如要收集更多有關複製作業來源的資料，可以嘗試下列做法：

* 如果複製作業位於單一或少數幾個區域，您可以嘗試查詢特定區域的 [`INFORMATION_SCHEMA.JOBS`](https://docs.cloud.google.com/bigquery/docs/information-schema-jobs?hl=zh-tw) 資料表。例如：

  ```
  SELECT
  creation_time, job_id, user_email, destination_table.project_id, destination_table.dataset_id, destination_table.table_id
  FROM `PROJECT_ID`.`region-REGION_NAME`.INFORMATION_SCHEMA.JOBS
  WHERE
  creation_time BETWEEN TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 2 DAY) AND CURRENT_TIMESTAMP()
  AND job_type = "COPY"
  order by creation_time DESC
  ```

  您也可以根據想查看的時間範圍調整時間間隔。
* 如要查看所有地區的所有複製工作，請在 Cloud Logging 中使用下列篩選條件：

  ```
  resource.type="bigquery_resource"
  protoPayload.methodName="jobservice.insert"
  protoPayload.serviceData.jobInsertRequest.resource.jobConfiguration.tableCopy:*
  ```

#### 解析度

* 如果頻繁複製作業的目的是建立資料快照，建議改用[資料表快照](https://docs.cloud.google.com/bigquery/docs/table-snapshots-intro?hl=zh-tw)。相較於複製完整表格，表格快照的費用較低，速度也較快。
* 如要要求增加配額，請與[支援團隊](https://docs.cloud.google.com/bigquery/docs/getting-support?hl=zh-tw)或[銷售人員](https://cloud.google.com/contact?hl=zh-tw)聯絡。審查及處理要求可能需要幾天的時間。建議在要求中說明優先順序、用途和專案 ID。

### 超出每日擷取位元組配額錯誤

如果專案的擷取作業超出預設的 50 TiB 每日上限，BigQuery 就會傳回這項錯誤。如要進一步瞭解擷取工作限制，請參閱「[擷取工作](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#export_jobs)」。

**錯誤訊息**

```
Your usage exceeded quota for ExtractBytesPerDay
```

#### 診斷

如果匯出的資料表超過 50 TiB，匯出作業會失敗，因為[超過擷取限制](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#export_jobs)。如要[匯出特定資料表分區的資料表資料](https://docs.cloud.google.com/bigquery/docs/partitioned-tables?hl=zh-tw#export_table_data)，可以使用[分區修飾符](https://docs.cloud.google.com/bigquery/docs/partitioned-tables?hl=zh-tw#partition_decorators)來識別要匯出的分區。

如要收集最近幾天的匯出資料用量，可以嘗試下列做法：

* [查看專案配額](https://docs.cloud.google.com/docs/quotas/view-manage?hl=zh-tw#view_project_quotas)：使用 `Name: Extract bytes per day` 或 `Metric: bigquery.googleapis.com/quota/extract/bytes` 等篩選條件，並顯示用量圖表，即可查看幾天內的用量趨勢。
* 或者，您也可以查詢 [`INFORMATION_SCHEMA.JOBS_BY_PROJECT`](https://docs.cloud.google.com/bigquery/docs/information-schema-jobs?hl=zh-tw)，查看幾天內的總擷取位元組。舉例來說，下列查詢會傳回過去七天內，`EXTRACT` 工作每天處理的位元組總數。

  ```
  SELECT
  TIMESTAMP_TRUNC(creation_time, DAY) AS day,
  SUM ( total_bytes_processed ) / POW(1024, 3) AS total_gibibytes_processed
  FROM
  `region-REGION_NAME`.INFORMATION_SCHEMA.JOBS_BY_PROJECT
  WHERE
  creation_time BETWEEN TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 7 DAY) AND CURRENT_TIMESTAMP()
  AND job_type = "EXTRACT"
  GROUP BY 1
  ORDER BY 2 DESC
  ```
* 然後找出耗用位元組數超出預期的特定工作，進一步縮小搜尋結果範圍。以下範例會傳回前 100 個 `EXTRACT` 工作，這些工作在過去七天內處理的資料量超過 100 GB。

  ```
  SELECT
  creation_time,
  job_id,
  total_bytes_processed/POW(1024, 3) AS total_gigabytes_processed
  FROM
  `region-REGION_NAME`.INFORMATION_SCHEMA.JOBS_BY_PROJECT
  WHERE
  creation_time BETWEEN TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 7 DAY) AND CURRENT_TIMESTAMP()
  AND job_type="EXTRACT"
  AND total_bytes_processed > (POW(1024, 3) * 100)
  ORDER BY
  total_bytes_processed DESC
  LIMIT 100
  ```

您也可以使用[工作探索器](https://docs.cloud.google.com/bigquery/docs/admin-jobs-explorer?hl=zh-tw)，並搭配 `Bytes processed more than` 等篩選器，篩選出特定時間範圍內的高處理量工作。

#### 解析度

如要解決這項配額錯誤，其中一種方法是建立運算單元[預留項目](https://docs.cloud.google.com/bigquery/docs/reservations-intro?hl=zh-tw#reservations)，然後將專案[指派](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#assignments)給具有 `PIPELINE` 工作類型的預留項目。由於這個方法使用專屬預訂，而非免費的共用運算單元集區，因此可以略過限制檢查。如有需要，您可以刪除預留項目，以便日後使用共用運算單元集區。

如要瞭解如何匯出超過 50 TiB 的資料，請參閱「[擷取工作](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#export_jobs)」的附註部分。

### 每個專案配額錯誤的每秒 `tabledata.list` 位元組數上限

當錯誤訊息中提及的專案號碼達到每秒可透過專案中的 `tabledata.list` API 呼叫讀取的資料大小上限時，BigQuery 就會傳回這項錯誤。詳情請參閱「[每分鐘最多 `tabledata.list` 位元組](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#tabledata_list_bytes_per_minute)」。

**錯誤訊息**

```
Your project:[project number] exceeded quota for tabledata.list bytes per second per project
```

#### 解析度

如要解決這項錯誤，請按照下列步驟操作：

* 一般來說，我們建議盡量不要超過這個上限。舉例來說，您可以延長要求間隔時間，如果錯誤不常發生，實作指數輪詢重試即可解決這個問題。
* 如果用途是從資料表快速且頻繁地讀取大量資料，建議使用 [BigQuery Storage Read API](https://docs.cloud.google.com/bigquery/docs/reference/storage?hl=zh-tw)，而非 `tabledata.list` API。
* 如果上述建議無法解決問題，請按照下列步驟，透過Google Cloud 主控台 API 資訊主頁申請增加配額：

  1. 前往[Google Cloud 控制台 API 資訊主頁](https://console.cloud.google.com/apis/dashboard?hl=zh-tw)。
  2. 在資訊主頁中，篩選配額：`Tabledata list bytes per minute (default quota)`。
  3. 選取配額，然後按照「[要求調整配額](https://docs.cloud.google.com/docs/quotas/help/request_increase?hl=zh-tw)」一文中的說明操作。

  審查及處理要求可能需要幾天的時間。

### API 要求數量上限錯誤

當您達到每個使用者每種方法對 BigQuery API 的 API 要求數量速率限制時，BigQuery 會傳回這項錯誤。舉例來說，服務帳戶的 [`tables.get` 方法](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables/get?hl=zh-tw)呼叫，或不同使用者電子郵件的 [`jobs.insert` 方法](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs/insert?hl=zh-tw)呼叫，都可能達到速率限制。

大多數 BigQuery API 核心方法每位使用者每個方法最多可提出 100 項 API 要求，但部分核心方法的速率限制可能不同，例如：

* [`jobs.get` 方法](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs/get?hl=zh-tw)每位使用者每秒最多可發出 1000 個 API 要求。
* [`projects.list` 方法](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/projects/list?hl=zh-tw)和 [`tables.insert` 方法](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables/insert?hl=zh-tw)每位使用者每秒最多只能提出 10 個要求。

此外，BigQuery API 速率限制[不適用](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#streaming_inserts)於串流插入作業。

如要進一步瞭解個別使用頻率限制，請參閱「[**每位使用者每種方法每秒的 API 要求數上限**」使用頻率限制](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#api_request_quotas)。

**錯誤訊息**

```
Quota exceeded: Your user_method exceeded quota for concurrent api requests
per user per method.
```

如果遇到這項錯誤，請[診斷](#ts-maximum-api-request-limit-diagnose)問題，然後[按照建議步驟](#ts-maximum-api-request-limit-resolution)解決問題。

#### 診斷

如果尚未找出達到此速率限制的方法，請執行下列操作：

**服務帳戶**

1. [前往代管服務帳戶的專案](https://console.cloud.google.com/projectselector2/home/dashboard?hl=zh-tw)。
2. 前往 Google Cloud 控制台的「API Dashboard」(API 資訊主頁)。

   如需查看 API 詳細用量資訊的操作說明，請參閱「[使用 API 資訊主頁](https://docs.cloud.google.com/apis/docs/monitoring?hl=zh-tw#using_the_api_dashboard)」。
3. 在 API 資訊主頁中，選取「BigQuery API」。
4. 如要查看更詳細的使用情況資訊，請選取「指標」，然後執行下列步驟：

   1. 在「選取圖表」中，選取「依 API 方法劃分的流量」。
   2. 依服務帳戶的憑證篩選圖表。在發現錯誤的時間範圍內，您可能會看到某個方法的尖峰。

**API 呼叫**

部分 API 呼叫會在 Cloud Logging 的 BigQuery 稽核記錄中記錄錯誤。如要找出達到上限的方法，請按照下列步驟操作：

1. 在 Google Cloud 控制台中，前往 Google Cloud 導覽選單 menu，然後依序選取專案的「Logging」>「Logs Explorer」：

   [前往 Logs Explorer](https://console.cloud.google.com/logs/query?hl=zh-tw)
2. 執行下列查詢來篩選記錄：

   ```
    resource.type="bigquery_resource"
    protoPayload.authenticationInfo.principalEmail="<user email or service account>"
    "Too many API requests per user per method for this user_method"
    In the log entry, you can find the method name under the property protoPayload.method_name.
   ```

   詳情請參閱 [BigQuery 稽核記錄總覽](https://docs.cloud.google.com/bigquery/docs/reference/auditlogs?hl=zh-tw)。

#### 解析度

如要解決這項配額錯誤，請按照下列步驟操作：

* 減少 API 要求數量，或在多個 API 要求之間加入延遲，確保要求數量不超過上限。
* 如果只是偶爾超出限制，您可以針對這項特定錯誤實作重試作業，並採用指數輪詢。
* 如果經常插入資料，建議使用 [BigQuery Storage Write API](https://docs.cloud.google.com/bigquery/docs/write-api-streaming?hl=zh-tw)。使用這個 API 串流資料時，不會受到 BigQuery API 配額影響。
* 使用 Dataflow 和 [BigQuery I/O 連接器](https://beam.apache.org/documentation/io/built-in/google-bigquery/)將資料載入 BigQuery 時，您可能會遇到 [`tables.get` 方法的這項錯誤](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables/get?hl=zh-tw)。如要解決這個問題，請按照下列步驟操作：

  + 將目的地資料表的建立處理方式設為 `CREATE_NEVER`。詳情請參閱「[建立處置方式](https://beam.apache.org/documentation/io/built-in/google-bigquery/#create-disposition)」。
  + 使用 Apache Beam SDK 2.24.0 以上版本。在舊版 SDK 中，`CREATE_IF_NEEDED` 處置會呼叫 `tables.get` 方法，檢查資料表是否存在。
  + 如需額外配額，請參閱「[要求增加配額](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#requesting_a_quota_increase)」。申請增加配額可能需要幾天才能處理完畢。為提供更多要求相關資訊，建議您在要求中加入工作優先順序、執行查詢的使用者，以及受影響的方法。

### 每個專案在每個區域的 Python UDF 映像檔儲存空間位元組數上限

有效 Python UDF 使用的所有已儲存容器映像檔總大小，不得超過每個專案在每個區域的 `10 GiB`。建立或更新 Python UDF 時，系統會強制執行這項限制。如果總大小超過區域限制，要求會立即失敗，並傳回下列錯誤。

**錯誤訊息**

`Resources exceeded during query execution: Quota exceeded: Your project:
PROJECT_ID exceeded quota for Python UDF image storage usage per
region per project.`

#### 解析度

如要解決這項錯誤，請按照下列步驟操作：

1. 要求提高上限：前往「[配額與系統限制」頁面](https://docs.cloud.google.com/docs/quotas/view-manage?hl=zh-tw#viewing_your_quota_console)，搜尋 `Python UDF image storage bytes per project per region` 限制，然後要求提高上限。
2. 最佳化儲存空間：使用 `DROP FUNCTION`
   陳述式刪除未使用的 Python UDF，釋出空間。刪除 UDF 後，其圖片大小就不會再計入配額。您可以使用 `Routine.GetBuildStatus` API 找出圖片大小。

## 解決無法提高的配額或限制

您無法提高下列配額或限制，但可以套用建議的解決方法或最佳做法來減輕影響。

### 查詢佇列限制錯誤

如果專案排入佇列的互動式或批次查詢數量超出[佇列限制](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#queued_interactive_queries)，就可能會發生這個錯誤。

**錯誤訊息**

```
Quota exceeded: Your project and region exceeded quota for max number of jobs
that can be queued per project.
```

#### 解析度

這項上限[無法提高](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#jobs)。如要解決這項錯誤，請參閱下列一般指引。如要瞭解如何避免大量互動式查詢受到限制，請參閱[這篇文章](#interactive-query-queue-resolution)。

* **暫停工作。**如果發現某個程序或管道導致查詢次數增加，請暫停該程序或管道。
* **分配執行時間。**在較長的時間範圍內分配負載。
  如果報表解決方案需要執行許多查詢，請嘗試在查詢開始時導入一些隨機性。舉例來說，請勿同時開始所有報表。
* **最佳化查詢和資料模型。**通常可以重寫查詢，提高執行效率。

  舉例來說，如果查詢包含*一般資料表運算式 (CTE)* (即 `WITH` 子句)，且查詢中有多個位置參照該運算式，則這項計算會執行多次。最好將 CTE 執行的計算結果保留在臨時資料表中，然後在查詢中參照該資料表。

  多次聯結也可能導致效率不彰。在這種情況下，您可能需要考慮使用[巢狀和重複的資料欄](https://docs.cloud.google.com/bigquery/docs/nested-repeated?hl=zh-tw)。使用這項功能通常可改善資料的區域性、免除部分聯結需求，並整體減少資源耗用量和查詢執行時間。

  最佳化查詢可降低費用，因此採用以運算量為準的計價模式時，您就能使用運算單元執行更多查詢。詳情請參閱「[簡介：最佳化查詢效能](https://docs.cloud.google.com/bigquery/docs/best-practices-performance-overview?hl=zh-tw)」。
* **最佳化查詢模型。**BigQuery 並非關聯資料庫。不適合處理無限多的小型查詢。執行大量小型查詢會迅速耗盡配額。這類查詢的執行效率不如小型資料庫產品。BigQuery 是大型資料倉儲，主要用途就是儲存大量資料。最適合對大量資料執行分析查詢。

  請參考下列建議，盡量避免查詢模型達到查詢佇列限制。

  + **保存資料 (儲存的資料表)。**在 BigQuery 中預先處理資料，並將資料儲存在其他資料表中。舉例來說，如果您使用不同的 `WHERE` 條件執行許多類似的運算密集型查詢，系統就不會快取結果。這類查詢每次執行時也會耗用資源。您可以預先計算資料並儲存在資料表中，藉此提升這類查詢的效能，並縮短處理時間。您可以使用 `SELECT` 查詢資料表中的預先計算資料。通常可以在 ETL 程序中的擷取階段完成，也可以使用[排程查詢](https://docs.cloud.google.com/bigquery/docs/scheduling-queries?hl=zh-tw)或[具體化檢視區塊](https://docs.cloud.google.com/bigquery/docs/materialized-views-intro?hl=zh-tw)。
  + **使用模擬測試模式**。以[模擬測試模式](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#dry-run)執行查詢，估算讀取的位元組數，但不會實際處理查詢。
  + **預覽資料表資料。**如要試用或探索資料，而非執行查詢，請使用 BigQuery 的[資料表預覽功能](https://docs.cloud.google.com/bigquery/docs/best-practices-costs?hl=zh-tw#preview-data)預覽資料表資料。
  + **使用[快取查詢結果](https://docs.cloud.google.com/bigquery/docs/cached-results?hl=zh-tw)。**
    所有查詢結果 (包括互動式與批次查詢) 皆會以快取方式存放在暫時性資料表中約 24 小時，但也有一些[例外狀況](https://docs.cloud.google.com/bigquery/docs/cached-results?hl=zh-tw#cache-exceptions)。
    執行快取查詢仍會計入並行查詢限制，但使用快取結果的查詢作業因為 BigQuery 不需計算結果集，執行速度會比未使用快取結果的查詢作業快上許多。
  + **使用 BigQuery BI Engine。**如果您在使用商業智慧 (BI) 工具建立資訊主頁時遇到這個錯誤，且該資訊主頁會查詢 BigQuery 中的資料，建議您使用 [BigQuery BI Engine](https://docs.cloud.google.com/bigquery/docs/bi-engine-intro?hl=zh-tw)。使用 BigQuery BI Engine 是這個用途的最佳選擇。
* **使用批次優先順序的工作。**您可以將比互動式查詢更多的[批次查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#batch)加入佇列。
* **分發查詢。**根據查詢性質和業務需求，在不同專案之間分配及散布負載。
* **增加預訂的運算單元。**[增加運算單元](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#estimate-slots)，或在工作負載需求量高時，從隨選 (依查詢付費模式) [改用](https://docs.cloud.google.com/bigquery/docs/reservations-intro?hl=zh-tw#choosing_a_model)預留 (以容量為準的模式)。

##### 避免大量互動式查詢受到限制

執行大量互動式查詢時，這些查詢可能會達到佇列中互動式查詢數量的[上限](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#query_jobs)。這項上限無法提高。

如果執行大量互動式查詢，特別是在涉及自動觸發程序 (例如 Cloud Run 函式) 的情況下，請先[監控](https://docs.cloud.google.com/bigquery/docs/admin-jobs-explorer?hl=zh-tw)並停止導致錯誤的 Cloud Run 函式，然後採用下列其中一種建議策略，避免超出這項限制：

* [增加預訂的運算單元](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#estimate-slots)。如果工作負載需求量高，請從隨選 (依查詢付費模式)[切換](https://docs.cloud.google.com/bigquery/docs/reservations-intro?hl=zh-tw#choosing_a_model)至預留 (以容量為準的模式)。
* 在互動式查詢之間分散工作負載。
* 因為批次查詢的佇列長度比互動式查詢長，請使用[批次優先順序工作](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#batch)，而非互動式查詢。

### 隨機播放大小限制錯誤

如果專案超出可供重組作業使用的磁碟和記憶體大小上限，BigQuery 就會傳回這項錯誤。

這項配額是以預訂為單位計算，並根據預訂項目在專案間分配。Cloud Customer Care 無法修改配額。如要進一步瞭解用量，請查詢 [`INFORMATION_SCHEMA.JOBS_TIMELINE` 檢視畫面](https://docs.cloud.google.com/bigquery/docs/information-schema-jobs-timeline?hl=zh-tw#schema)。

**錯誤訊息**

您收到下列其中一則錯誤訊息：

* ```
  Quota exceeded: Your project exceeded quota for total shuffle size limit.
  ```
* ```
  Resources exceeded: Your project or organization exceeded the maximum
  disk and memory limit available for shuffle operations. Consider provisioning
  more slots, reducing query concurrency, or using more efficient logic in this
  job.
  ```

#### 解析度

如要解決這項錯誤，請按照下列步驟操作：

* [增加預訂量](https://docs.cloud.google.com/bigquery/docs/reservations-tasks?hl=zh-tw#update_reservations)。
* [最佳化查詢](https://docs.cloud.google.com/bigquery/docs/best-practices-performance-overview?hl=zh-tw)。
* 減少查詢並行數或具體化中間結果，以減少對資源的依賴。詳情請參閱「[查詢佇列](https://docs.cloud.google.com/bigquery/docs/query-queues?hl=zh-tw)」和「[建立具體化檢視區塊](https://docs.cloud.google.com/bigquery/docs/materialized-views-create?hl=zh-tw)」。
* [查看詳細步驟](https://docs.cloud.google.com/bigquery/docs/query-insights?hl=zh-tw#insufficient_shuffle_quota)，瞭解如何緩解隨機播放配額不足的問題。

### 依資料欄分區的資料表分區修改次數配額錯誤

當資料欄分區資料表達到每日允許的分區修改次數配額時，BigQuery 就會傳回這項錯誤。分區修改次數包括所有[載入工作](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#load_jobs)、[複製工作](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#copy_jobs)和[查詢工作](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#query_jobs)，這些工作會將資料附加至目的地分區或覆寫目的地分區。

如要查看「每個資料欄分區資料表每日可修改分區的次數上限」值，請參閱「[分區資料表](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#partitioned_tables)」一文。

**錯誤訊息**

```
Quota exceeded: Your table exceeded quota for
Number of partition modifications to a column partitioned table
```

#### 解析度

這項配額無法提高。如要解決這項配額錯誤，請按照下列步驟操作：

* 變更資料表的分區，讓每個分區包含更多資料，以減少分區總數。舉例來說，您可以[將分區依天改為依月](https://docs.cloud.google.com/bigquery/docs/partitioned-tables?hl=zh-tw#select_daily_hourly_monthly_or_yearly_partitioning)，或是[變更資料表的分區方式](https://docs.cloud.google.com/bigquery/docs/partitioned-tables?hl=zh-tw)。
* 請改用[叢集](https://docs.cloud.google.com/bigquery/docs/clustered-tables?hl=zh-tw#when_to_use_clustering)，而非分區。
* 如果您經常從儲存在 Cloud Storage 中的多個小型檔案載入資料，且每個檔案都使用一個工作，請將多個載入工作合併為單一工作。您可以透過以逗號分隔的清單 (例如 `gs://my_path/file_1,gs://my_path/file_2`)，