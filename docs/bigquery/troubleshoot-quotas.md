Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 疑難排解配額與限制錯誤

BigQuery 設有各種[配額和限制](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)，會限制不同要求和作業的頻率和數量。這些限制不僅能保護基礎架構，還能防範客戶意外使用。本文說明如何診斷及緩解因配額和限制而產生的特定錯誤。

部分錯誤訊息會指出可提高的配額或限制，其他錯誤訊息則會指出無法提高的配額或限制。達到硬性限制時，您必須為工作負載實施暫時或永久的解決方法或最佳做法。即使配額或限制可以提高，也建議您這麼做。

本文會根據這些類別整理錯誤訊息和解決方案，並在後續的「總覽」一節說明如何解讀錯誤訊息，以及如何針對問題套用正確的解決方案。

如果本文未列出您遇到的錯誤訊息，請參閱[錯誤訊息清單](https://docs.cloud.google.com/bigquery/docs/error-messages?hl=zh-tw)，其中包含更多一般錯誤資訊。

## 總覽

如果 BigQuery 作業因超出配額而失敗，API 會傳回 HTTP `403 Forbidden` 狀態碼。回應主體會提供更多資訊，說明已達到的配額。回應主體看起來會與下列內容類似：

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

* **`rateLimitExceeded`。**這個值代表短期限制。如要解決這些限制問題，請在幾秒後重試操作。在重試之間使用*指數輪詢*。也就是說，每次重試之間的延遲時間會以指數方式增加。
* **`quotaExceeded`：**這個值代表長期限制。如果您達到長期配額上限，則至少應等待 10 分鐘，然後再重試作業。如果您持續達到其中一項長期配額限制，則應分析您的工作負載，以便找出緩解問題的方法。將工作負載最佳化或要求增加配額都有可能緩解問題。

**注意事項：**部分配額會以每日配額表示。例如，[每個資料表的載入工作](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#load_jobs)數量設有每日配額。不過，這些配額會在 24 小時內逐步補充，因此達到上限後，您
不必等待整整 24 小時。

如有 `quotaExceeded` 錯誤，請查看錯誤訊息，瞭解哪些配額已超過上限。接著，分析工作負載，看看是否能避免達到配額。

在某些情況下，您可以[聯絡 BigQuery 支援團隊](https://docs.cloud.google.com/bigquery/docs/getting-support?hl=zh-tw)或[聯絡 Google Cloud 銷售人員](https://cloud.google.com/contact?hl=zh-tw)來提高配額，但建議您先嘗試本文中的建議。

## 診斷

如要診斷問題，請按照下列步驟操作：

* 使用 [`INFORMATION_SCHEMA` 檢視畫面](https://docs.cloud.google.com/bigquery/docs/information-schema-tables?hl=zh-tw)和[區域限定詞](https://docs.cloud.google.com/bigquery/docs/information-schema-intro?hl=zh-tw#region_qualifier)，分析根本問題。這些檢視表包含 BigQuery 資源的中繼資料，包括工作、預留項目和串流資料即時插入。

  舉例來說，下列查詢會使用 [`INFORMATION_SCHEMA.JOBS`](https://docs.cloud.google.com/bigquery/docs/information-schema-jobs?hl=zh-tw) 檢視表，列出過去一天內所有與配額相關的錯誤：

  ```
  SELECT
  job_id,
  creation_time,
  error_result
  FROM  `region-REGION_NAME`.INFORMATION_SCHEMA.JOBS
  WHERE creation_time > TIMESTAMP_SUB(CURRENT_TIMESTAMP, INTERVAL 1 DAY) AND
      error_result.reason IN ('rateLimitExceeded', 'quotaExceeded')
  ```

  將 `REGION_NAME` 替換為專案的區域。前面必須加上 `region-`。例如，如果是 `US` 多區域，請使用 `region-us`。
* 在 Cloud 稽核記錄中查看錯誤。

  舉例來說，使用[Logs Explorer](https://docs.cloud.google.com/logging/docs/view/logs-explorer-summary?hl=zh-tw)時，下列查詢會傳回訊息字串中含有 `Quota exceeded` 或 `limit` 的錯誤：

  ```
  resource.type = ("bigquery_project" OR "bigquery_dataset")
  protoPayload.status.code ="7"
  protoPayload.status.message: ("Quota exceeded" OR "limit")
  ```

  在本例中，狀態碼 `7` 表示 [`PERMISSION_DENIED`](https://docs.cloud.google.com/tasks/docs/reference/rpc/google.rpc?hl=zh-tw#code)，對應至 HTTP `403` 狀態碼。

  如需其他 Cloud 稽核記錄查詢範例，請參閱「[BigQuery 查詢](https://docs.cloud.google.com/logging/docs/view/query-library-preview?hl=zh-tw#bigquery-filters)」。

## 排解可提高的配額或限制

您可以提高下列配額和限制，但建議先嘗試任何建議的解決方法或最佳做法。

### 專案超過免費查詢位元組掃描配額

在免費使用層級執行查詢時，如果帳戶達到每月查詢上限，BigQuery 就會傳回這項錯誤。如要進一步瞭解查詢定價，請參閱「[免費使用層級](https://cloud.google.com/bigquery/pricing?hl=zh-tw#free-usage-tier)」。

**錯誤訊息**

```
Your project exceeded quota for free query bytes scanned
```

#### 解析度

如要繼續使用 BigQuery，請[將帳戶升級為 Cloud Billing 付費帳戶](https://docs.cloud.google.com/free/docs/gcp-free-tier?hl=zh-tw#how-to-upgrade)。

### 串流資料即時插入配額錯誤

本節提供疑難排解提示，協助您解決將資料串流至 BigQuery 時發生的配額錯誤。

在特定區域，如果您未填入各列的 `insertId` 欄位，串流資料即時插入作業的配額會較高。如要進一步瞭解串流資料即時插入的配額，請參閱「[串流資料即時插入](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#streaming_inserts)」。BigQuery 串流的配額相關錯誤取決於 `insertId` 是否存在。

**錯誤訊息**

如果 `insertId` 欄位為空白，則可能會發生下列配額錯誤：

| 配額限制 | 錯誤訊息 |
| --- | --- |
| 每項專案每秒位元組數 | 在區域 REGION 中專案 PROJECT\_ID gaia\_id 為 GAIA\_ID 的實體超過每秒插入位元組數的配額。 |

如果在 `insertId` 欄位填入資料，則可能會發生下列配額錯誤：

| 配額限制 | 錯誤訊息 |
| --- | --- |
| 每項專案每秒資料列數量 | 您在 REGION 的專案 PROJECT\_ID 超過每秒串流資料插入資料列的配額。 |
| 每個資料表每秒資料列數量 | 您的資料表「TABLE\_ID」已超過每秒串流資料即時插入資料列的配額。 |
| 每個資料表每秒位元組數 | 資料表「TABLE\_ID」已超過每秒串流資料即時插入位元組數的配額。 |

`insertId` 欄位的用途是簡化插入的資料列。如果同一個 `insertId` 的多個插入項目均於幾分鐘之內抵達，則 BigQuery 會寫入單一版本的記錄。但是，我們無法保證系統會自動刪除重複的內容。為了達到最大的串流總處理量，建議您不要加入 `insertId`，改成[手動刪除重複內容](https://docs.cloud.google.com/bigquery/docs/streaming-data-into-bigquery?hl=zh-tw#manually_removing_duplicates)。詳情請參閱[確保資料一致性](https://docs.cloud.google.com/bigquery/docs/streaming-data-into-bigquery?hl=zh-tw#dataconsistency)一文。

遇到這項錯誤時，請[診斷問題](#ts-streaming-insert-quota-diagnose)，然後[按照建議步驟](#ts-streaming-insert-quota-resolution)解決問題。

#### 診斷

使用 [`STREAMING_TIMELINE_BY_*`](https://docs.cloud.google.com/bigquery/docs/information-schema-streaming?hl=zh-tw) 檢視表來分析串流流量。這些檢視表會以一分鐘為間隔，匯總串流統計資料，並依 `error_code` 分組。如果 `error_code` 等於 `RATE_LIMIT_EXCEEDED` 或 `QUOTA_EXCEEDED`，結果中會顯示配額錯誤。

根據已達到的特定配額上限查看 `total_rows` 或 `total_input_bytes`。如果錯誤是資料表層級配額，請依 `table_id` 篩選。

舉例來說，下列查詢會顯示每分鐘擷取的位元組總數，以及配額錯誤總數：

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

* 如果您使用 `insertId` 欄位進行簡化，且專案位於支援較高串流配額的區域，建議您移除 `insertId` 欄位。這項解決方案可能需要額外步驟，才能手動簡化資料。詳情請參閱[手動移除重複內容](https://docs.cloud.google.com/bigquery/docs/streaming-data-into-bigquery?hl=zh-tw#manually_removing_duplicates)。
* 如果您並非使用 `insertId`，或是無法加以移除，請監控 24 小時內的串流流量，並分析配額錯誤：

  + 如果看到的大多是 `RATE_LIMIT_EXCEEDED` 錯誤，而非 `QUOTA_EXCEEDED` 錯誤，且整體流量低於配額的 80%，則錯誤可能代表暫時性尖峰。如要解決這類錯誤，請重試作業，並在重試之間採用指數輪詢策略。
  + 如果您使用 Dataflow 工作插入資料，建議使用載入工作，而非串流資料即時插入。詳情請參閱「[設定插入方法](https://beam.apache.org/documentation/io/built-in/google-bigquery/#setting-the-insertion-method)」。如果您使用 Dataflow 搭配自訂 I/O 連接器，建議改用內建 I/O 連接器。詳情請參閱「[自訂 I/O 模式](https://beam.apache.org/documentation/patterns/custom-io/)」。
  + 如果看到 `QUOTA_EXCEEDED` 錯誤，或整體流量持續超過配額的 80%，請提交提高配額的要求。詳情請參閱「[要求調整配額](https://docs.cloud.google.com/docs/quotas/help/request_increase?hl=zh-tw)」。
  + 您也可以考慮將串流資料即時插入作業，改為使用較新的 [Storage Write API](https://docs.cloud.google.com/bigquery/docs/write-api?hl=zh-tw)，這項 API 的處理量較高、價格較低，且提供許多實用功能。

如要進一步瞭解串流資料即時插入，請參閱「[將資料串流至 BigQuery](https://docs.cloud.google.com/bigquery/docs/streaming-data-into-bigquery?hl=zh-tw)」。

### 串流資料表建立頻率限制錯誤

如果串流管道 (`tabledata.insertAll`) 自動建立新資料表 (例如使用[範本資料表](https://docs.cloud.google.com/bigquery/docs/write-api-rest?hl=zh-tw#template-tables)搭配 `templateSuffix` 或動態目的地資料表) 的速度，超過每項專案的[串流資料表建立頻率限制](https://docs.cloud.google.com/bigquery/docs/write-api-rest?hl=zh-tw#template_table_details)，BigQuery 會傳回下列錯誤：

**錯誤訊息**

```
Exceeded rate limits: Your Project: PROJECT_ID exceeded quota for
Streaming Table Creation Rate. For more information, see
https://docs.cloud.google.com/bigquery/troubleshooting-errors
```

#### 解析度

如要解決這項錯誤，請執行下列操作：

* **預先建立目的地資料表。**如果管道會動態產生許多 shard 或快速輪替的資料表，請執行 DDL 指令碼或使用 [`tables.insert`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables/insert?hl=zh-tw) API 預先建立資料表，而不是在插入期間依賴串流 API 建立資料表。詳情請參閱「[範本表格詳細資料](https://docs.cloud.google.com/bigquery/docs/write-api-rest?hl=zh-tw#template_table_details)」。

### 包含遠端函式的並行查詢數量上限

如果含有遠端函式的並行查詢數量超過限制，BigQuery 就會傳回這項錯誤。

如要進一步瞭解遠端函式限制，請參閱「[遠端函式](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#remote_function_limits)」。

**錯誤訊息**

```
Exceeded rate limits: too many concurrent queries with remote functions for
this project
```

這項限制可以提高。請先嘗試解決方法和最佳做法。

#### 診斷

如要查看包含[遠端函式](https://docs.cloud.google.com/bigquery/docs/remote-functions?hl=zh-tw)的並行查詢限制，請參閱「[遠端函式限制](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#remote_function_limits)」。

#### 解析度

* 使用遠端函式時，請遵循[遠端函式的最佳做法](https://docs.cloud.google.com/bigquery/docs/remote-functions?hl=zh-tw#best_practices_for_remote_functions)。
* 如要提高配額，請與[支援團隊](https://docs.cloud.google.com/bigquery/docs/getting-support?hl=zh-tw)或[銷售團隊](https://cloud.google.com/contact?hl=zh-tw)聯絡。審查及處理要求可能需要幾天時間。建議您在要求中說明優先順序、用途和專案 ID。

### `CREATE MODEL` 陳述式數量上限

這項錯誤表示您已超出 `CREATE MODEL` 陳述式的配額。

**錯誤訊息**

```
Quota exceeded: Your project exceeded quota for CREATE MODEL queries per
 project.
```

#### 解析度

如果超過 `CREATE MODEL` 陳述式的[配額](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#create_model_statements)，請傳送電子郵件至 [bqml-feedback@google.com](mailto:bqml-feedback@google.com)，要求提高配額。

### 每項專案每日複製工作數量上限配額錯誤

如果專案中執行的複製工作數量超過每日上限，BigQuery 就會傳回這項錯誤。如要進一步瞭解每日複製工作的限制，請參閱「[複製工作](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#copy_jobs)」。

**錯誤訊息**

```
Your project exceeded quota for copies per project
```

#### 診斷

如要收集更多資料，瞭解複製工作的來源，可以嘗試下列做法：

* 如果複製工作位於單一或少數區域，您可以嘗試查詢特定區域的 [`INFORMATION_SCHEMA.JOBS`](https://docs.cloud.google.com/bigquery/docs/information-schema-jobs?hl=zh-tw) 資料表。例如：

  ```
  SELECT
  creation_time, job_id, user_email, destination_table.project_id, destination_table.dataset_id, destination_table.table_id
  FROM `PROJECT_ID`.`region-REGION_NAME`.INFORMATION_SCHEMA.JOBS
  WHERE
  creation_time BETWEEN TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 2 DAY) AND CURRENT_TIMESTAMP()
  AND job_type = "COPY"
  order by creation_time DESC
  ```

  您也可以根據感興趣的日期範圍調整時間間隔。
* 如要查看所有區域中的所有複製工作，請在 Cloud Logging 中使用下列篩選器：

  ```
  resource.type="bigquery_resource"
  protoPayload.methodName="jobservice.insert"
  protoPayload.serviceData.jobInsertRequest.resource.jobConfiguration.tableCopy:*
  ```

#### 解析度

* 如果頻繁複製作業的目的是建立資料快照，建議改用[資料表快照](https://docs.cloud.google.com/bigquery/docs/table-snapshots-intro?hl=zh-tw)。資料表快照是複製完整資料表的替代方案，成本較低且速度更快。
* 如要提高配額，請與[支援團隊](https://docs.cloud.google.com/bigquery/docs/getting-support?hl=zh-tw)或[銷售團隊](https://cloud.google.com/contact?hl=zh-tw)聯絡。審查及處理要求可能需要幾天時間。建議您在要求中說明優先順序、用途和專案 ID。

### 超出每日擷取位元組配額錯誤

如果擷取作業超出專案預設的每日 50 TiB 上限，BigQuery 就會傳回這項錯誤。如要進一步瞭解擷取工作的限制，請參閱「[擷取工作](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#export_jobs)」。

**錯誤訊息**

```
Your usage exceeded quota for ExtractBytesPerDay
```

#### 診斷

如果匯出的資料表大於 50 TiB，匯出作業會因[超過擷取限制](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#export_jobs)而失敗。如要[匯出特定資料表分區的資料表資料](https://docs.cloud.google.com/bigquery/docs/partitioned-tables?hl=zh-tw#export_table_data)，可以使用[分區修飾符](https://docs.cloud.google.com/bigquery/docs/partitioned-tables?hl=zh-tw#partition_decorators)，找出要匯出的分區。

如要收集最近幾天的匯出資料用量，可以嘗試下列做法：

* [查看專案配額](https://docs.cloud.google.com/docs/quotas/view-manage?hl=zh-tw#view_project_quotas)：使用 `Name: Extract bytes per day` 或 `Metric: bigquery.googleapis.com/quota/extract/bytes` 等篩選條件，並搭配「顯示用量」圖表，查看幾天內的用量趨勢。
* 或者，您也可以查詢 [`INFORMATION_SCHEMA.JOBS_BY_PROJECT`](https://docs.cloud.google.com/bigquery/docs/information-schema-jobs?hl=zh-tw)，查看幾天內的擷取位元組總數。舉例來說，下列查詢會傳回過去七天內 `EXTRACT` 工作每日處理的總位元組數。

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
* 接著，您可以找出耗用位元組數超出預期的特定工作，進一步縮小結果範圍。以下範例會傳回過去七天內，處理超過 100 GB 的前 100 個 `EXTRACT` 工作。

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

您也可以使用[工作探索工具](https://docs.cloud.google.com/bigquery/docs/admin-jobs-explorer?hl=zh-tw)，並搭配 `Bytes processed more than` 等篩選器，篩選出指定時間範圍內處理量較高的工作。

#### 解析度

如要解決這項配額錯誤，其中一種方法是建立運算單元[預留項目](https://docs.cloud.google.com/bigquery/docs/reservations-intro?hl=zh-tw#reservations)，並將專案[指派](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#assignments)至具有 `PIPELINE` 工作類型的預留項目。這種方法會使用專屬預留項目，而非免費的共用運算單元集區，因此可以略過限制檢查。如有需要，您可以刪除預留項目，以便日後使用共用運算單元集區。

如要瞭解如何匯出*超過* 50 TiB 的資料，請參閱「[擷取工作](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#export_jobs)」中的附註部分。

### 每個專案每秒位元組數或要求數上限 (`tabledata.list`) 配額錯誤

如果錯誤訊息中提及的專案編號，達到每秒可透過專案中 `tabledata.list` API 呼叫讀取的資料大小上限或要求數量上限 (QPS)，BigQuery 就會傳回這項錯誤。詳情請參閱「[每分鐘最多 `tabledata.list` 個位元組](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#tabledata_list_bytes_per_minute)」。

**錯誤訊息**

```
Your project:[project number] exceeded quota for tabledata.list bytes per second per project
```

```
Exceeded rate limits: Your project:[project number] exceeded quota for tabledata.list qps per project
```

#### 解析度

如要解決這項錯誤，請執行下列操作：

* 一般來說，建議您盡量不要超過這個上限。例如，在較長的時間內分散要求，並加入延遲。如果錯誤不常發生，只要實作指數輪詢重試機制，即可解決這個問題。
* 如果您使用 `tabledata.list` 逐列或以小幅增量讀取資料，請增加批次大小 (例如使用 `maxResults`)，以便透過較少的 HTTP 要求擷取較大的區塊。
* 如果用途需要快速且頻繁地從資料表讀取大量資料，建議使用 [BigQuery Storage Read API](https://docs.cloud.google.com/bigquery/docs/reference/storage?hl=zh-tw)，而非 `tabledata.list` API。
* 如果上述建議無法解決問題，您可以按照下列步驟，在Google Cloud 控制台 API 資訊主頁中申請提高配額：

  1. 前往 [Google Cloud 控制台 API 資訊主頁](https://console.cloud.google.com/apis/dashboard?hl=zh-tw)。
  2. 在資訊主頁中，篩選配額：`Tabledata list bytes per minute (default quota)`。
  3. 選取配額，然後按照「[申請調整配額](https://docs.cloud.google.com/docs/quotas/help/request_increase?hl=zh-tw)」一節的指示操作。

  審查及處理要求可能需要幾天時間。

### API 要求數量上限錯誤

當您達到每位使用者對 BigQuery API 的 API 要求數量頻率限制 (例如服務帳戶的 [`tables.get` 方法](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables/get?hl=zh-tw)呼叫，或不同使用者電子郵件的 [`jobs.insert` 方法](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs/insert?hl=zh-tw)呼叫)，或使用者超過 `INFORMATION_SCHEMA` 查詢的頻率限制時，BigQuery 會傳回這項錯誤。

大多數 BigQuery API 核心方法，每位使用者每種方法最多可提出 100 項 API 要求，但部分核心方法的頻率限制可能不同，例如：

* [`jobs.get` 方法](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs/get?hl=zh-tw)的限制為每位使用者每秒 1000 個 API 要求。
* [`projects.list` 方法](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/projects/list?hl=zh-tw)和 [`tables.insert` 方法](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables/insert?hl=zh-tw)的限制皆為每位使用者每秒 10 個要求。

此外，BigQuery API 頻率限制[不適用於](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#streaming_inserts)串流資料即時插入。

如要進一步瞭解個別頻率限制，請參閱「[**每位使用者每種方法每秒的 API 要求數量上限**頻率限制](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#api_request_quotas)」。

**錯誤訊息**

```
Exceeded rate limits: too many api requests per user per method for this
user_method. For more information, see
https://cloud.google.com/bigquery/docs/troubleshoot-quotas
```

```
Exceeded rate limits: too many rate INFORMATION_SCHEMA queries per user for
this user. For more information, see
https://cloud.google.com/bigquery/docs/troubleshoot-quotas
```

```
Exceeded rate limits: Your user exceeded quota for rate INFORMATION_SCHEMA
queries per user
```

```
Quota exceeded: Your user_method exceeded quota for concurrent api requests
per user per method.
```

遇到這項錯誤時，請[診斷](#ts-maximum-api-request-limit-diagnose)問題，然後[按照建議步驟](#ts-maximum-api-request-limit-resolution)解決問題。

如果錯誤原因為 `apiLimitExceeded`，請參閱「[API 頻率和中繼資料評估限制錯誤](#ts-api-limit-rate-and-metadata)」；如果是資料集副本錯誤，請參閱「[跨區域資料集副本建立限制錯誤](#ts-dataset-replica-limit)」。

#### 診斷

如果您尚未找出達到這項頻率限制的方法，請按照下列步驟操作：

**服務帳戶**

1. [前往託管服務帳戶的專案](https://console.cloud.google.com/projectselector2/home/dashboard?hl=zh-tw)。
2. 在 Google Cloud 控制台，前往「API Dashboard」(API 資訊主頁)。

   如要瞭解如何查看 API 的詳細使用資訊，請參閱「[使用 API 資訊主頁](https://docs.cloud.google.com/apis/docs/monitoring?hl=zh-tw#using_the_api_dashboard)」。
3. 在 API 資訊主頁中，選取「BigQuery API」。
4. 如要查看更詳細的使用資訊，請選取「Metrics」(指標)，然後執行下列操作：

   1. 在「選取圖表」部分，選取「依 API 方法劃分的流量」。
   2. 依服務帳戶的憑證篩選圖表。在您發現錯誤的日期範圍內，某個方法可能會出現尖峰。

**API 呼叫**

部分 API 呼叫會在 Cloud Logging 的 BigQuery 稽核記錄中記錄錯誤。如要找出達到上限的方法，請按照下列步驟操作：

1. 在 Google Cloud 控制台中，前往 Google Cloud 導覽選單 menu，然後依序選取「Logging」>「Logs Explorer」，查看專案：

   [前往「Logs Explorer」](https://console.cloud.google.com/logs/query?hl=zh-tw)
2. 執行下列查詢來篩選記錄：

   ```
    resource.type="bigquery_resource"
    protoPayload.authenticationInfo.principalEmail="<user email or service account>"
    ("too many api requests per user per method" OR "too many rate INFORMATION_SCHEMA queries per user")
    In the log entry, you can find the method name under the property protoPayload.methodName.
   ```

   詳情請參閱「[BigQuery 稽核記錄總覽](https://docs.cloud.google.com/bigquery/docs/reference/auditlogs?hl=zh-tw)」。

#### 解析度

如要解決這項配額錯誤，請按照下列步驟操作：

* 減少 API 要求數量，或在多個 API 要求之間加入延遲時間，讓要求數量不超過這項限制。
* 如果只是偶爾超過上限，可以對這項特定錯誤實作指數輪詢重試機制。
* 請避免直接從即時商業智慧資訊主頁或高頻率工作流程輪詢 `INFORMATION_SCHEMA` 檢視表。如果工作流程需要頻繁存取工作記錄或中繼資料，請排定定期查詢，將 `INFORMATION_SCHEMA` 輸出內容具體化為標準 BigQuery 資料表，並將應用程式或資訊主頁指向該具體化資料表。如需執行多個 `INFORMATION_SCHEMA` 查詢，請分批執行，不要同時執行。
* 如果您經常插入資料，建議使用 [BigQuery Storage Write API (gRPC)](https://docs.cloud.google.com/bigquery/docs/write-api-streaming?hl=zh-tw)。使用這個 API 串流資料時，不受 BigQuery API 配額限制。
* 使用 Dataflow 搭配 [BigQuery I/O 連接器](https://beam.apache.org/documentation/io/built-in/google-bigquery/)將資料載入 BigQuery 時，[`tables.get` 方法](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables/get?hl=zh-tw)可能會發生這項錯誤。請按照下列步驟解決這個問題：

  + 將目的地資料表的建立處置設為 `CREATE_NEVER`。詳情請參閱「[建立處置](https://beam.apache.org/documentation/io/built-in/google-bigquery/#create-disposition)」。
  + 使用 Apache Beam SDK 2.24.0 以上版本。在舊版 SDK 中，`CREATE_IF_NEEDED` 處置會呼叫 `tables.get` 方法，檢查資料表是否存在。
  + 如需更多配額，請參閱「[申請提高配額](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#requesting_a_quota_increase)」。提高配額的要求可能需要幾天才能處理完畢。為提供更多資訊，建議您在要求中加入工作優先順序、執行查詢的使用者，以及受影響的方法。

### API 頻率和中繼資料評估限制錯誤

如果要求超出 API 頻率限制，或並行中繼資料和存取權評估限制，BigQuery 會傳回 HTTP `403 Forbidden` 錯誤，原因為 `apiLimitExceeded`。

**錯誤訊息**

* `Quota exceeded for the project...`
* `API limit exceeded: Quota exceeded for quota metric 'Read requests'...`

#### 診斷

這個錯誤可能在下列情況發生：

* **大量並行 API 要求。**應用程式提交大量並行 API 呼叫 (例如 `jobs.insert`、`tables.get` 或快速工作狀態輪詢)，超出 BigQuery API 要求限制。
* **BigLake metastore 並行。**對由 BigLake Metastore 支援的外部資料表執行查詢，會產生大量並行中繼資料讀取要求。
* **複雜的 IAM 或資料列層級安全性評估。**並行查詢參照大量資料集、資料表或資料列層級安全性 (RLS) 政策，導致後端存取權評估限制用盡。

如果錯誤訊息為 `Quota exceeded: Your user_method exceeded quota for
concurrent api requests per user per method`，請參閱「[API 要求數量上限錯誤](#ts-maximum-api-request-limit)」。

#### 解析度

如要解決這項錯誤，請執行下列操作：

* **以部分指數輪詢方式重試。**請設定用戶端應用程式或指令碼，使用截斷指數輪詢重試失敗的要求。
* **批次處理及整合 API 作業。**載入或查詢資料時，請使用較少、較大的批次，而非發出高頻率的單列或每表 API 呼叫，並減少 `jobs.get` 輪詢呼叫的頻率。
* **簡化 IAM 和安全性設定。**建議您使用 Google 群組和資料集層級的 IAM 角色繫結，而非大量精細的個別資料表 IAM 繫結，或重疊的資料列層級安全性政策，以減少存取權檢查負擔。
* **在 Google Cloud 控制台查看配額用量。**查看「[Quotas & System Limits](https://docs.cloud.google.com/docs/quotas/view-manage?hl=zh-tw#viewing_your_quota_console)」(配額與系統限制) 頁面，確認是否已達到可調整的 BigQuery 或 BigLake API 配額。如果持續需要更多容量，請要求調整配額。

### 每個專案在各區域的 Python UDF 映像檔儲存空間位元組數上限

在每個專案的各個區域中，使用中的 Python UDF 所用儲存容器映像檔總大小不得超過 `10 GiB`。建立或更新 Python UDF 時，系統會強制執行這項限制。如果總大小超過區域限制，要求會立即失敗，並傳回下列錯誤。

**錯誤訊息**

`Resources exceeded during query execution: Quota exceeded: Your project:
PROJECT_ID exceeded quota for Python UDF image storage usage per
region per project.`

#### 解析度

如要解決這項錯誤，請執行下列操作：

1. 要求提高上限：前往[**「Quotas & System Limits」(配額與系統限制)** 頁面](https://docs.cloud.google.com/docs/quotas/view-manage?hl=zh-tw#viewing_your_quota_console)，搜尋 `Python UDF image storage bytes per project per region` 限制，然後要求提高上限。
2. 最佳化儲存空間：使用 `DROP FUNCTION` 陳述式刪除未使用的 Python UDF，釋出空間。刪除 UDF 後，其映像檔大小就不會再計入配額。您可以使用 API 的 [`RoutineBuildStatus`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/routines?hl=zh-tw#routinebuildstatus) 找出圖片大小。如要進一步瞭解如何查看建構狀態，請參閱「[容器建構狀態](https://docs.cloud.google.com/bigquery/docs/user-defined-functions-python?hl=zh-tw#container_build_status)」。

### 並行 Python UDF 數量上限

每項專案最多只能同時執行 10 個 Python UDF。如果執行超過 10 個，就會收到下列錯誤。

**錯誤訊息**

`Exceeded rate limits: too many concurrent queries with Python UDFs in this
project. Your project:
PROJECT_ID exceeded quota for maximum concurrent Python UDFs per
project.`

如要查看所有 Python UDF 配額，請參閱「配額與限制」參考資料中的「[常式](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#udf_limits)」一節。

#### 解析度

如要解決這項錯誤，請與[支援團隊](https://docs.cloud.google.com/bigquery/docs/getting-support?hl=zh-tw)或[銷售團隊](https://cloud.google.com/contact?hl=zh-tw)聯絡，要求提高配額。審查及處理要求可能需要幾天時間。建議您在要求中說明優先順序、用途和專案 ID。

### Python UDF 執行頻率限制或容量錯誤

如果叫用 Python UDF 的查詢超過 UDF 的頻率限制或容器擴充容量上限，就會發生這項錯誤。這個問題通常發生在下列情況：

* 查詢會以高度平行處理的方式處理大量資料。
* 每個容器執行個體都設為處理少量並行要求。
* 個別 UDF 叫用需要很長時間才能完成。

**錯誤訊息**

`Resources exceeded during query execution: Python user-defined function
execution exceeded rate limits or capacity. Check
https://docs.cloud.google.com/bigquery/docs/troubleshoot-quotas for more
details.`

#### 解析度

如要解決這項錯誤，請嘗試下列做法：

* **調整容器限制**：在 Cloud Monitoring 中查看 [Python UDF 指標](https://docs.cloud.google.com/bigquery/docs/user-defined-functions-python?hl=zh-tw#view_python_udf_metrics)，檢查 CPU 使用率、記憶體使用率和並行要求。如果 `container_request_concurrency` 設為較低的值，請調高這個值，讓每個容器執行個體能同時處理更多要求。如果 `container_cpu` 設為小於 `1.0` 個 vCPU，且未明確指定 `container_request_concurrency` 值，則並行數量在執行階段會預設為 `1`。詳情請參閱「[設定 Python UDF 的容器限制](https://docs.cloud.google.com/bigquery/docs/user-defined-functions-python?hl=zh-tw#configure-container-limits)」。
* **最佳化 UDF 執行和查詢結構**：請遵循 [Python UDF 最佳做法](https://docs.cloud.google.com/bigquery/docs/user-defined-functions-python?hl=zh-tw#best_practices)，縮短執行時間和每項查詢的要求量。例如，在叫用 UDF 前先篩選資料、保持輸入資料列酬載較小，以及建構查詢以支援批次處理。
* **要求增加容量**：如果最佳化 UDF 後仍發生錯誤，請與[支援團隊](https://docs.cloud.google.com/bigquery/docs/getting-support?hl=zh-tw)或[銷售人員](https://cloud.google.com/contact?hl=zh-tw)聯絡，要求提高容器擴充限制。請在要求中附上優先順序、用途和專案 ID。

### 自訂每日查詢配額錯誤

當專案或使用者達到管理員設定的自訂每日查詢用量配額 (`QueryUsagePerDay` 或 `QueryUsagePerUserPerDay`) 時，BigQuery 會傳回這項錯誤 (`reason: quotaExceeded`)。如要進一步瞭解自訂查詢配額的運作方式，請參閱「[自訂配額](https://docs.cloud.google.com/bigquery/docs/custom-quotas?hl=zh-tw)」。

**錯誤訊息**

* `Custom quota exceeded: Your usage exceeded the custom quota for
  QueryUsagePerDay, which is set by your administrator.`
* `Custom quota exceeded: Your usage exceeded the custom quota for
  QueryUsagePerUserPerDay, which is set by your administrator.`

#### 診斷

如果查詢用量比預期更快達到自訂每日配額，請檢查下列常見原因：

* **每日重設時間和時區調整。**自訂每日查詢配額會在太平洋時間 (美國和加拿大) 午夜重設。如果當地時區與太平洋時間不同，在當地時區前一個日曆日執行的查詢，可能仍會落在目前的 24 小時太平洋時間配額範圍內。
* **BigQuery ML 陳述式的正規化用量。** Google Cloud 控制台的「Quotas & System Limits」(配額與系統限制) 頁面會回報正規化查詢用量，這可能高於`INFORMATION_SCHEMA.JOBS`中的計費位元組。某些 BigQuery ML 作業 (例如建立邏輯迴歸模型) 的計費費率較高，詳情請參閱「[BigQuery ML 定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#bqml)」。舉例來說，如果某項作業的定價是標準隨選費率的 50 倍，則在 `INFORMATION_SCHEMA.JOBS` 中回報 1 TiB `total_bytes_billed` 的 `CREATE MODEL` 工作，會計為 50 TiB 的查詢用量，計入自訂每日配額。詳情請參閱「[設定或修改自訂配額](https://docs.cloud.google.com/bigquery/docs/custom-quotas?hl=zh-tw#set-custom-quotas)」。

如要找出在太平洋時間當天，哪些工作和使用者耗用最多計費位元組，請查詢 [`INFORMATION_SCHEMA.JOBS_BY_PROJECT`](https://docs.cloud.google.com/bigquery/docs/information-schema-jobs?hl=zh-tw) 檢視表：

```
SELECT
  user_email,
  job_id,
  statement_type,
  creation_time,
  total_bytes_billed / POWER(1024, 4) AS tib_billed
FROM
  `region-REGION_NAME`.INFORMATION_SCHEMA.JOBS_BY_PROJECT
WHERE
  creation_time >= TIMESTAMP(
    CURRENT_DATE('America/Los_Angeles'), 'America/Los_Angeles')
  AND job_type = 'QUERY'
ORDER BY
  tib_billed DESC
LIMIT 50;
```

將 `REGION_NAME` 替換為資料集區域 (例如 `us` 或 `eu`)。

`statement_type` 為 `CREATE_MODEL` 的工作可能會以高於 `tib_billed` 顯示的比率計入配額。

#### 解析度

如要解決或減少自訂每日查詢配額錯誤，請按照下列步驟操作：

* **最佳化高用量查詢，減少掃描的位元組數。**例如，篩選分區和分群欄、只選取所需欄 (而非使用 `SELECT *`)，以及使用[模擬測試](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#dry-run)預覽執行查詢前處理的位元組。詳情請參閱「[減少處理的資料](https://docs.cloud.google.com/bigquery/docs/best-practices-performance-compute?hl=zh-tw#reduce-data-processed)」。
* **從其他計費專案執行查詢。**如果資料集與另一個 Google Cloud 專案共用，且該專案可存取基礎資料表，而且沒有自訂每日配額或有剩餘配額，您就可以從該替代專案提交查詢工作。
* **提高自訂每日配額。**如果工作負載的每日查詢量增加，請要求 Google Cloud 管理員或配額管理員 (`roles/servicemanagement.quotaAdmin`) 前往「配額與系統限制」頁面，提高「每日查詢用量」或「每位使用者每日查詢用量」限制。如需操作說明，請參閱「[設定或修改自訂配額](https://docs.cloud.google.com/bigquery/docs/custom-quotas?hl=zh-tw#set-custom-quotas)」。

## 排解無法提高配額或限制的問題

您無法提高下列配額或限制，但可以採用建議的解決方法或最佳做法來減輕影響。

### 超過資料表快照數量上限

如果 BigQuery 資料表在 24 小時內超過允許的資料表快照數量上限，就會發生這項錯誤。這是資料表層級的限制，也就是說，這項限制適用於專案中的每個資料表。

如要進一步瞭解每日資料表作業限制，請參閱「[標準資料表](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#standard_tables)」。

這項限制[無法提高](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#table_snapshots)。

**錯誤訊息**

```
Your table exceeded quota for SNAPSHOT operations per table
```

#### 解析度

如要解決這項錯誤，請考慮採取下列行動：

* 在 24 小時內，減少對受影響資料表執行的快照作業數量。
* 如果無法降低快照頻率，請與 [Cloud Customer Care](https://docs.cloud.google.com/bigquery/docs/getting-support?hl=zh-tw) 或客戶技術顧問聯絡。

### 待處理工作錯誤數量上限

這項限制[無法提高](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#pending_jobs)。

**錯誤訊息**

```
Quota exceeded: concurrent number of jobs that can be in the pending state
```

#### 解析度

這項配額無法提高。

如要解決這項錯誤，請執行下列操作：

* **降低提交頻率。**降低向 BigQuery 提交工作的頻率，並使用[截斷指數輪詢](https://cloud.google.com/monitoring/api/troubleshooting?hl=zh-tw#exponential-retry)重試失敗的工作提交。
* **限制並行作業，並批次處理較小的作業。**請避免同時提交大量工作，以免累積在 `PENDING` 狀態。請改為將較小的載入、複製或 DML 作業合併成數量較少的大型工作。
* **檢查執行中和待處理的工作。**查詢 [`INFORMATION_SCHEMA.JOBS` 檢視表](https://docs.cloud.google.com/bigquery/docs/information-schema-jobs?hl=zh-tw)，找出含有 `state IN ('PENDING', 'RUNNING')` 的工作，即可識別提交待處理工作的使用者、服務帳戶或管道。

### 查詢佇列限制錯誤

如果專案排入佇列的互動式或批次查詢數量超過[佇列限制](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#queued_interactive_queries)，就可能發生這項錯誤。

**錯誤訊息**

```
Quota exceeded: Your project and region exceeded quota for max number of jobs
that can be queued per project.
```

#### 解析度

這項限制[無法提高](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#jobs)。如要解決這項錯誤，請參閱下列一般指南。如要執行大量互動式查詢，請參閱「[避免大量互動式查詢的限制](#interactive-query-queue-resolution)」。

* **暫停工作。**如果發現某個程序或管道導致查詢增加，請暫停該程序或管道。
* **分散執行時間。**將負載分散到更長的時間範圍。如果報表解決方案需要執行多項查詢，請嘗試在查詢開始時加入一些隨機性。例如，請勿同時啟動所有報表。
* **最佳化查詢和資料模型。**通常，您可以重寫查詢，提高執行效率。

  舉例來說，如果查詢包含*通用資料表運算式 (CTE)* (`WITH` 子句)，且在查詢中多次參照，則這項運算會執行多次。建議將 CTE 執行的計算結果保留在臨時資料表中，然後在查詢中參照。

  多個彙整也可能導致效率不彰。在這種情況下，建議您考慮使用[巢狀和重複資料欄](https://docs.cloud.google.com/bigquery/docs/nested-repeated?hl=zh-tw)。使用這項功能通常可以改善資料的局部性、免除部分彙整作業，並整體減少資源消耗和查詢執行時間。

  最佳化查詢可降低費用，因此使用以運算資源為基礎的定價模式時，您可以使用運算單元執行更多查詢。詳情請參閱「[最佳化查詢效能簡介](https://docs.cloud.google.com/bigquery/docs/best-practices-performance-overview?hl=zh-tw)」。
* **最佳化查詢模型。**BigQuery 並非關聯式資料庫。不適合處理無限量的小型查詢。執行大量小型查詢會快速耗盡配額。這類查詢的執行效率不如小型資料庫產品。BigQuery 是大型資料倉儲，這也是其主要用途。最適合對大量資料執行分析查詢。

  請參考下列清單中的建議，將查詢模型最佳化，避免達到查詢佇列上限。

  + **保存資料 (儲存的資料表)。**在 BigQuery 中預先處理資料，並將資料儲存在其他資料表中。舉例來說，如果您使用不同的 `WHERE` 條件執行許多類似、需要大量運算的查詢，系統就不會快取這些查詢的結果。這類查詢每次執行時也會耗用資源。您可以預先計算資料並儲存在資料表中，藉此提升這類查詢的效能，並縮短處理時間。資料表中預先運算的資料可透過 `SELECT` 查詢。這項作業通常可在 ETL 程序中的擷取期間完成，或使用[排定查詢](https://docs.cloud.google.com/bigquery/docs/scheduling-queries?hl=zh-tw)或[materialized view](https://docs.cloud.google.com/bigquery/docs/materialized-views-intro?hl=zh-tw) 完成。
  + **使用模擬測試模式。**在[模擬測試模式](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#dry-run)中執行查詢，估算讀取的位元組數，但不會實際處理查詢。
  + **預覽資料表資料。**如要實驗或探索資料，而非執行查詢，請使用 BigQuery 的[資料表預覽功能](https://docs.cloud.google.com/bigquery/docs/best-practices-costs?hl=zh-tw#preview-data)預覽資料表資料。
  + **使用[快取查詢結果](https://docs.cloud.google.com/bigquery/docs/cached-results?hl=zh-tw)。**
    所有查詢結果 (包括互動式和批次查詢) 都會快取在暫存資料表中，快取時間約為 24 小時，但有部分[例外狀況](https://docs.cloud.google.com/bigquery/docs/cached-results?hl=zh-tw#cache-exceptions)。雖然執行快取查詢仍會計入並行查詢限制，但使用快取結果的查詢速度明顯快於不使用快取結果的查詢，因為 BigQuery 不需要計算結果集。
  + **使用 BigQuery BI Engine。**如果您在使用商業智慧 (BI) 工具建立資訊主頁，並查詢 BigQuery 中的資料時遇到這項錯誤，建議您使用 [BigQuery BI Engine](https://docs.cloud.google.com/bigquery/docs/bi-engine-intro?hl=zh-tw)。使用 BigQuery BI Engine 是這類用途的最佳選擇。
* **使用批次優先順序的工作。**您可以排入佇列的[批次查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#batch)數量，多於互動式查詢。
* **分配查詢。**根據查詢性質和業務需求，在不同專案之間分配及分配負載。
* **增加預留項目中的運算單元。**[增加運算單元](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#estimate-slots)，或在工作負載需求較高時，從隨選 (按查詢付費模式) [切換](https://docs.cloud.google.com/bigquery/docs/reservations-intro?hl=zh-tw#choosing_a_model)至預留項目 (以運算能力計費模式)。
* **調整預留項目的並行目標。**如果您使用預留項目，可以[設定預留項目的並行目標上限](https://docs.cloud.google.com/bigquery/docs/query-queues?hl=zh-tw#set_the_maximum_concurrency_target)，控制可同時執行的查詢數量，超過這個數量後，其他查詢就會排入佇列。

##### 避免大量互動式查詢的限制

執行大量互動式查詢時，可能會達到排入佇列的互動式查詢數量[上限](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#query_jobs)。這項上限無法提高。

如果您執行大量互動式查詢，尤其是在涉及 Cloud Run functions 等自動觸發條件的情境中，請先[監控](https://docs.cloud.google.com/bigquery/docs/admin-jobs-explorer?hl=zh-tw)導致錯誤的 Cloud Run 函式行為並停止該函式，然後採用下列其中一項建議策略，避免達到這項限制：

* [增加預留項目中的運算單元](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#estimate-slots)。如果工作負載需求量很大，請從隨選 (按查詢付費模式) [切換](https://docs.cloud.google.com/bigquery/docs/reservations-intro?hl=zh-tw#choosing_a_model)至預留項目 (以容量為基礎的模式)。
* 將工作負載分散到互動式查詢。
* 由於可排入佇列的批次查詢數量多於互動式查詢，因此請使用[批次優先順序工作](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#batch)，而非互動式查詢。

### 重組大小限制錯誤

如果專案超過重組作業可用的磁碟和記憶體大小上限，BigQuery 就會傳回這項錯誤。

這項配額會依預留項目計算，並依預留項目的專案劃分。Cloud Customer Care 無法修改配額。如要進一步瞭解用量，請查詢 [`INFORMATION_SCHEMA.JOBS_TIMELINE` 檢視表](https://docs.cloud.google.com/bigquery/docs/information-schema-jobs-timeline?hl=zh-tw#schema)。

如果使用[隨選](https://cloud.google.com/bigquery/pricing?hl=zh-tw#on_demand_pricing)定價模式，則[最多只能使用 2,000 個運算單元](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#query_jobs)。如要增加運算單元數量，必須改用[依運算資源計費](https://cloud.google.com/bigquery/pricing?hl=zh-tw#capacity_compute_analysis_pricing)的定價模式。

**錯誤訊息**

您收到下列其中一則錯誤訊息：

```
Quota exceeded: Your project exceeded quota for total shuffle size limit.
```

```
Resources exceeded: Your project or organization exceeded the maximum
  disk and memory limit available for shuffle operations. Consider provisioning
  more slots, reducing query concurrency, or using more efficient logic in this
  job.
```

#### 解析度

如要解決這項錯誤，請執行下列操作：

* [增加預留項目](https://docs.cloud.google.com/bigquery/docs/reservations-tasks?hl=zh-tw#update_reservations)。
* [最佳化查詢](https://docs.cloud.google.com/bigquery/docs/best-practices-performance-overview?hl=zh-tw)。
* 減少查詢並行或具體化中繼結果，降低對資源的依賴。詳情請參閱「[查詢佇列](https://docs.cloud.google.com/bigquery/docs/query-queues?hl=zh-tw)」和「[建立 materialized view](https://docs.cloud.google.com/bigquery/docs/materialized-views-create?hl=zh-tw)」。
* [查看詳細步驟](https://docs.cloud.google.com/bigquery/docs/query-insights?hl=zh-tw#insufficient_shuffle_quota)，瞭解如何緩解重組配額不足的問題。

### 資料欄分區資料表的分區修改次數配額錯誤

如果資料欄分區資料表達到每日允許的分區修改次數配額，BigQuery 就會傳回這項錯誤。分區修改作業包括所有[載入工作](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#load_jobs)、[複製工作](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#copy_jobs)和[查詢工作](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#query_jobs)，這些工作會附加或覆寫目的地分區。

如要查看「**每個資料欄分區資料表每天的分區修改次數**」限制值，請參閱「[分區資料表](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#partitioned_tables)」。

**錯誤訊息**

```
Quota exceeded: Your table exceeded quota for
Number of partition modifications to a column partitioned table
```

#### 解析度

這項配額無法提高。如要解決這項配額錯誤，請按照下列步驟操作：

* 變更資料表的分區，讓每個分區有更多資料，以減少分區總數。例如，從[按日分區變更為按月分區](https://docs.cloud.google.com/bigquery/docs/partitioned-tables?hl=zh-tw#select_daily_hourly_monthly_or_yearly_partitioning)，或變更[資料表分區方式](https://docs.cloud.google.com/bigquery/docs/partitioned-tables?hl=zh-tw)。
* 使用[分群](https://docs.cloud.google.com/bigquery/docs/clustered-tables?hl=zh-tw#when_to_use_clustering)而非分區。
* 如果您經常從 Cloud Storage 儲存的多個小型檔案載入資料，且每個檔案都使用一項工作，請將多項載入工作合併為單一工作。您可以使用以半形逗號分隔的清單 (例如 `gs://my_path/file_1,gs://my_path/file_2`) 或萬用字元 (例如 `gs://my_path/*`)，從多個 Cloud Storage URI 載入資料。

  詳情請參閱「[批次載入資料](https://docs.cloud.google.com/bigquery/docs/batch-loading-data?hl=zh-tw#permissions-load-data-from-cloud-storage)」。
* 舉例來說，如果您使用載入、選取或複製工作，將單一資料列附加至資料表，建議您將多項工作批次處理成一項工作。BigQuery 做為關聯式資料庫時，效能不佳。最佳做法是避免頻繁執行單列附加動作。
* 如要快速附加資料，建議使用 [BigQuery Storage Write API (gRPC)](https://docs.cloud.google.com/bigquery/docs/write-api?hl=zh-tw)。建議用於高效能資料擷取。BigQuery Storage Write API (gRPC) 具備強大的功能，包括「僅傳送一次」語意。如要瞭解限制和配額，請參閱「[Storage Write API](https://cloud.google.com/bigquery/quotas?hl=zh-tw#write-api-limits)」；如要瞭解使用這個 API 的費用，請參閱「[BigQuery 資料擷取定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#data_ingestion_pricing)」。
* 如要監控資料表上修改的分區數量，請使用 [`INFORMATION_SCHEMA` 檢視表](https://docs.cloud.google.com/bigquery/docs/information-schema-jobs?hl=zh-tw#partitions-modified-by)。
* 如要瞭解如何最佳化資料表載入工作，避免達到配額限制，請參閱「[最佳化載入工作](https://docs.cloud.google.com/bigquery/docs/optimize-load-jobs?hl=zh-tw)」。

### 資料表中繼資料更新作業頻率上限錯誤

如果資料表達到標準或分區資料表每資料表的中繼資料更新作業頻率上限，BigQuery 就會傳回這項錯誤。資料表作業包括所有[載入工作](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#load_jobs)、[複製工作](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#copy_jobs)和[查詢工作](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#query_jobs)的總和，這些工作會附加或覆寫目的地資料表，或使用 [DML](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/dml-syntax?hl=zh-tw) `DELETE`、`INSERT`、`MERGE`、`TRUNCATE TABLE` 或 `UPDATE` 將資料寫入資料表。

如要查看「**每個資料表的中繼資料更新作業頻率上限**」限制的值，請參閱「[標準資料表](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#standard_tables)」。

**錯誤訊息**

```
Exceeded rate limits: too many table update operations for this table. For
more information, see
https://cloud.google.com/bigquery/docs/troubleshoot-quotas
```

```
Exceeded rate limits: too many partitioned table update operations for this
table. For more information, see
https://cloud.google.com/bigquery/docs/troubleshoot-quotas
```

遇到這項錯誤時，請[診斷](#ts-maximum-update-table-metadata-limit-diagnose)問題，然後[按照建議步驟](#ts-maximum-update-table-metadata-limit-resolution)解決。

#### 診斷

中繼資料資料表更新可能來自修改資料表中繼資料的 *API 呼叫*，或修改資料表內容的*工作*。如果您尚未找出資料表大部分中繼資料更新作業的來源，請按照下列步驟操作：

* [識別 API 呼叫](#identify-api-calls)。
* [找出所需的工作](#identify-jobs)。

##### 找出 API 呼叫

1. 前往 Google Cloud 導覽
   menu選單，然後
   依序選取**「Logging」(記錄)>「Logs Explorer」(記錄檔探索工具)**：

   [前往「Logs Explorer」](https://console.cloud.google.com/logs/query?hl=zh-tw)
2. 執行下列查詢，篩選記錄檔來查看資料表作業：

   ```
   resource.type="bigquery_dataset"
   protoPayload.resourceName="projects/my-project-id/datasets/my_dataset/tables/my_table"
   (protoPayload.methodName="google.cloud.bigquery.v2.TableService.PatchTable" OR
   protoPayload.methodName="google.cloud.bigquery.v2.TableService.UpdateTable" OR
   protoPayload.methodName="google.cloud.bigquery.v2.TableService.InsertTable")
   ```

##### 找出所需的工作

下列查詢會傳回一份工作清單，列出過去一天內修改專案中受影響資料表的工作。如果您預期組織中有多項專案會寫入資料表，請將 `JOBS_BY_PROJECT` 替換為 `JOBS_BY_ORGANIZATION`。

```
SELECT
 job_id,
 user_email,
 query
FROM  `region-REGION_NAME`.INFORMATION_SCHEMA.JOBS_BY_PROJECT
WHERE creation_time > TIMESTAMP_SUB(CURRENT_TIMESTAMP, INTERVAL 1 DAY)
AND destination_table.project_id = "my-project-id"
AND destination_table.dataset_id = "my_dataset"
AND destination_table.table_id = "my_table"
```

詳情請參閱「[BigQuery 稽核記錄總覽](https://docs.cloud.google.com/bigquery/docs/reference/auditlogs?hl=zh-tw)」。

#### 解析度

這項配額無法提高。如要解決這項配額錯誤，請按照下列步驟操作：

* 降低資料表中繼資料的更新頻率。
* 在工作或資料表作業之間加入延遲時間，確保更新率不超過限制，並以截斷指數輪詢重試失敗的作業。
* 將連續的 DDL 陳述式 (例如多個 `ALTER TABLE` 陳述式) 合併為單一 [`CREATE OR REPLACE TABLE` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#create_table_statement)，或將結構定義變更批次處理為單一資料表中繼資料更新，而非執行連續的中繼資料更新指令。
* 如要插入或修改資料，建議使用 DML 作業。DML 作業不受「**每個資料表的中繼資料更新作業頻率上限**」限制。

  DML 作業有其他[限制](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#data-manipulation-language-statements)和配額。詳情請參閱「[使用 data manipulation language (DML)](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-manipulation-language?hl=zh-tw)」。
* 如果您經常從 Cloud Storage 儲存的多個小型檔案載入資料，且每個檔案都使用一項工作，請將多項載入工作合併為單一工作。您可以使用以半形逗號分隔的清單 (例如 `gs://my_path/file_1,gs://my_path/file_2`) 或萬用字元 (例如 `gs://my_path/*`)，從多個 Cloud Storage URI 載入資料。

  詳情請參閱「[批次載入資料](https://docs.cloud.google.com/bigquery/docs/batch-loading-data?hl=zh-tw#permissions-load-data-from-cloud-storage)」。
* 舉例來說，如果您使用載入、選取或複製工作，將單一資料列附加至資料表，建議您將多項工作批次處理成一項工作。BigQuery 做為關聯式資料庫時，效能不佳。最佳做法是避免頻繁執行單列附加動作。
* 如要快速附加資料，建議使用 [BigQuery Storage Write API (gRPC)](https://docs.cloud.google.com/bigquery/docs/write-api?hl=zh-tw)。建議用於高效能資料擷取。BigQuery Storage Write API (gRPC) 具備強大的功能，包括「僅傳送一次」語意。如要瞭解限制和配額，請參閱「[Storage Write API](https://cloud.google.com/bigquery/quotas?hl=zh-tw#write-api-limits)」；如要瞭解使用這個 API 的費用，請參閱「[BigQuery 資料擷取定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#data_ingestion_pricing)」。
* 如要監控資料表上修改的分區數量，請使用 [`INFORMATION_SCHEMA` 檢視表](https://docs.cloud.google.com/bigquery/docs/information-schema-jobs?hl=zh-tw#partitions-modified-by)。
* 如要瞭解如何最佳化資料表載入工作，避免達到配額限制，請參閱「[最佳化載入工作](https://docs.cloud.google.com/bigquery/docs/optimize-load-jobs?hl=zh-tw)」。

### 資料表和資料集中繼資料並行讀取次數上限錯誤

如果同時有太多查詢讀取同一個資料表，或同時查詢已淘汰的舊版資料集中繼資料表 (`__TABLES__` 或 `__TABLES_SUMMARY__`)，BigQuery 就會傳回這項錯誤。

**錯誤訊息**

* `Exceeded rate limits: too many concurrent reads on a table for this table.
  For more information, see
  https://cloud.google.com/bigquery/docs/troubleshoot-quotas`
* `Exceeded rate limits: too many concurrent dataset meta table reads per
  dataset for this dataset. For more information, see
  https://cloud.google.com/bigquery/docs/troubleshoot-quotas`
* `Exceeded rate limits: too many concurrent dataset meta table reads per
  project for this project. For more information, see
  https://cloud.google.com/bigquery/docs/troubleshoot-quotas`

#### 解析度

如要解決這項錯誤，請執行下列操作：

* **限制並行讀取並新增抖動。**如果自動調度管理工具 (例如 Apache Airflow 或 dbt) 同時對同一個資料表啟動多項平行查詢，請設定並行限制，或新增隨機啟動延遲 (抖動)。
* **啟用[快取查詢結果](https://docs.cloud.google.com/bigquery/docs/cached-results?hl=zh-tw)。**對同一個資料表重複執行相同的讀取查詢時，使用快取結果。
* **以指數輪詢方式重試。**使用截斷指數輪詢重試失敗的查詢。
* **分配高度並行的讀取工作負載。**如果資料表必須同時服務大量並行讀取器，請建立[materialized view](https://docs.cloud.google.com/bigquery/docs/materialized-views-intro?hl=zh-tw)來服務不同的查詢、維護個別資料表副本來分配讀取負載，或[分區](https://docs.cloud.google.com/bigquery/docs/partitioned-tables?hl=zh-tw)和[分群](https://docs.cloud.google.com/bigquery/docs/clustered-tables?hl=zh-tw)資料表，讓不同的查詢讀取不同的分區或叢集，藉此分配負載。
* **將舊版 `__TABLES__` 和 `__TABLES_SUMMARY__` 檢視畫面替換為 `INFORMATION_SCHEMA` 檢視畫面。**如果遇到 `concurrent dataset meta
  table reads` 錯誤，請將查詢從已淘汰的 `__TABLES__` 和 `__TABLES_SUMMARY__` 檢視表遷移至 [`INFORMATION_SCHEMA.TABLES`](https://docs.cloud.google.com/bigquery/docs/information-schema-tables?hl=zh-tw) 或 [`INFORMATION_SCHEMA.PARTITIONS`](https://docs.cloud.google.com/bigquery/docs/information-schema-partitions?hl=zh-tw)。

### 工作建立頻率限制錯誤

如果工作負載在專案和區域中建立新工作的速度，超過每項專案區域工作建立頻率限制，BigQuery 就會傳回這項錯誤，包括使用 [`jobCreationMode: JOB_CREATION_OPTIONAL`](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#optional-job-creation) 的查詢改為建立標準 BigQuery 工作時。

**錯誤訊息**

* `Exceeded rate limits: too many creating jobs for this project_and_region.
  For more information, see
  https://cloud.google.com/bigquery/docs/troubleshoot-quotas`
* `Exceeded rate limits: Your project_and_region exceeded quota for creating
  jobs. For more information, see
  https://cloud.google.com/bigquery/troubleshooting-errors`

#### 解析度

如要解決這項錯誤，請執行下列操作：

* **以指數輪詢方式重試。**在用戶端應用程式中擷取 HTTP `403` `rateLimitExceeded` 錯誤，並使用截斷指數輪詢重試提交工作。
* **合併個別 DML 陳述式。**請勿同時提交多個獨立的單一陳述式 DML 工作，而是將這些工作分組為[多陳述式查詢](https://docs.cloud.google.com/bigquery/docs/multi-statement-queries?hl=zh-tw)。
* **檢查及最佳化 `JOB_CREATION_OPTIONAL` 備用查詢。**如果工作負載使用 `JOB_CREATION_OPTIONAL`，請查詢 [`job_creation_reason.code` (位於 `INFORMATION_SCHEMA.JOBS`)](https://docs.cloud.google.com/bigquery/docs/information-schema-jobs?hl=zh-tw#optional-job-creation)，找出查詢改為建立工作的原因 (例如 `LARGE_RESULTS` 或 `LONG_RUNNING`)，並最佳化這些查詢，以傳回較小的結果集或加快執行速度。或者，如果工作負載一律需要建立完整工作，請將 [`jobCreationMode`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs/query?hl=zh-tw#JobCreationMode) 設為 `JOB_CREATION_REQUIRED` (預設值)，並調整工作提交速率。
* **減少運算單元爭用情形，或提高預留容量。**如果預留項目中執行的查詢因運算單元爭用而改用 `LONG_RUNNING`，請平均分配查詢並行作業，或[增加預留項目大小](https://docs.cloud.google.com/bigquery/docs/reservations-tasks?hl=zh-tw#update_reservations)。

### 資料表匯入或查詢附加配額錯誤

如果資料表達到標準資料表每日作業上限，BigQuery 就會傳回這則錯誤訊息。資料表作業包括所有[載入工作](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#load_jobs)、[複製工作](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#copy_jobs)和[查詢工作](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#query_jobs)的總和，這些工作會附加或覆寫目的地資料表。

如要查看「每日資料表作業」限制的值，請參閱「[標準資料表](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#standard_tables)」。

**錯誤訊息**

```
Your table exceeded quota for imports or query appends per table
```

遇到這項錯誤時，請[診斷](#ts-table-import-quota-diagnose)問題，然後[按照建議步驟](#ts-table-import-quota-resolution)解決。

#### 診斷

如果您尚未找出大多數資料表作業的來源，請按照下列步驟操作：

1. 記下失敗的查詢、載入或複製工作寫入的專案、資料集和資料表。
2. 使用 `INFORMATION_SCHEMA.JOBS_BY_*` 資料表，進一步瞭解修改資料表的工作。

   下列範例使用 `JOBS_BY_PROJECT`，找出過去 24 小時內每小時的工作數量 (按工作類型分組)。如果預期有多個專案會寫入資料表，請將 `JOBS_BY_PROJECT` 替換為 `JOBS_BY_ORGANIZATION`。

   ```
   SELECT
   TIMESTAMP_TRUNC(creation_time, HOUR),
   job_type,
   count(1)
   FROM `region-REGION_NAME`.INFORMATION_SCHEMA.JOBS_BY_PROJECT
   WHERE creation_time > TIMESTAMP_SUB(CURRENT_TIMESTAMP, INTERVAL 1 DAY)
   AND destination_table.project_id = "my-project-id"
   AND destination_table.dataset_id = "my_dataset"
   AND destination_table.table_id = "my_table"
   GROUP BY 1, 2
   ORDER BY 1 DESC
   ```

#### 解析度

這項配額無法提高。如要解決這項配額錯誤，請按照下列步驟操作：

* 如果您經常從 Cloud Storage 儲存的多個小型檔案載入資料，且每個檔案都使用一項工作，請將多項載入工作合併為單一工作。您可以使用以半形逗號分隔的清單 (例如 `gs://my_path/file_1,gs://my_path/file_2`) 或萬用字元 (例如 `gs://my_path/*`)，從多個 Cloud Storage URI 載入資料。

  詳情請參閱「[批次載入資料](https://docs.cloud.google.com/bigquery/docs/batch-loading-data?hl=zh-tw#permissions-load-data-from-cloud-storage)」。
* 舉例來說，如果您使用載入、選取或複製工作，將單一資料列附加至資料表，建議您將多項工作批次處理成一項工作。BigQuery 做為關聯式資料庫時，效能不佳。最佳做法是避免頻繁執行單列附加動作。
* 如要快速附加資料，建議使用 [BigQuery Storage Write API (gRPC)](https://docs.cloud.google.com/bigquery/docs/write-api?hl=zh-tw)。建議用於高效能資料擷取。BigQuery Storage Write API (gRPC) 具備強大的功能，包括「僅傳送一次」語意。如要瞭解限制和配額，請參閱「[Storage Write API](https://cloud.google.com/bigquery/quotas?hl=zh-tw#write-api-limits)」；如要瞭解使用這個 API 的費用，請參閱「[BigQuery 資料擷取定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#data_ingestion_pricing)」。
* 如要監控資料表上修改的分區數量，請使用 [`INFORMATION_SCHEMA` 檢視表](https://docs.cloud.google.com/bigquery/docs/information-schema-jobs?hl=zh-tw#partitions-modified-by)。
* 如要瞭解如何最佳化資料表載入工作，避免達到配額限制，請參閱「[最佳化載入工作](https://docs.cloud.google.com/bigquery/docs/optimize-load-jobs?hl=zh-tw)」。

### 「每個資料集的授權檢視表」配額指標和「2500」限制已超出配額。

如果資料集的存取控制清單超過授權資源的合併限制，BigQuery 就會傳回這則錯誤訊息。

**錯誤訊息**

```
Quota exceeded for quota metric 'Authorized Views per dataset' and limit '2500'.
```

#### 解析度

資料集的存取控制清單最多可有 2,500 項授權資源，包括[授權檢視表](https://docs.cloud.google.com/bigquery/docs/authorized-views?hl=zh-tw)、[授權資料集](https://docs.cloud.google.com/bigquery/docs/authorized-datasets?hl=zh-tw)和[授權函式](https://docs.cloud.google.com/bigquery/docs/authorized-functions?hl=zh-tw)。
如果授權檢視表數量過多而超過這項限制，建議您將檢視表分組為授權資料集。
最佳做法是在設計新的 BigQuery 架構 (尤其是多租戶架構) 時，將相關檢視表分組到授權資料集。

### 資料表有太多未執行的 DML 陳述式

錯誤字串：`Resources exceeded during query execution: Too many DML
statements outstanding against table
PROJECT_ID:DATASET.TABLE, limit is 20.`

這項錯誤表示[並行變動 DML 陳述式](https://docs.cloud.google.com/bigquery/docs/data-manipulation-language?hl=zh-tw#update_delete_merge_dml_concurrency) (`UPDATE`、`DELETE` 和 `MERGE`) 的數量，加上在 `PENDING` 狀態下針對單一資料表排入佇列的 `TRUNCATE TABLE` 陳述式，已超過 20 個[data manipulation language (DML) 配額限制](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#data-manipulation-language-statements)。`INSERT` 陳述式會使用獨立佇列，上限為 100。

#### 解析度

* 查詢 [`INFORMATION_SCHEMA.JOBS` 檢視表](https://docs.cloud.google.com/bigquery/docs/troubleshoot-queries?hl=zh-tw#too_many_DML)，找出 `RUNNING` 和 `PENDING` 工作，以及 `statement_type IN ('UPDATE', 'DELETE',
  'MERGE', 'TRUNCATE_TABLE')`，找出填滿資料表 DML 佇列的工作。
* 將多個較小的變動 DML 作業分組為較少、較大的工作，例如將個別的 `UPDATE` 陳述式合併為單一 `UPDATE ...
  SET column = CASE WHEN ... END` 陳述式，或將頻繁更新暫存在個別資料表中，並使用單一 `MERGE` 陳述式定期套用至目標資料表。請參閱「[避免使用更新或插入單一資料列的 DML 陳述式](https://docs.cloud.google.com/bigquery/docs/best-practices-performance-compute?hl=zh-tw#avoid-dml-update-single-rows)」和「[DML 陳述式過多](https://docs.cloud.google.com/bigquery/docs/troubleshoot-queries?hl=zh-tw#too_many_DML)」。
* 將目標資料表分區或分群，提高 DML 執行速度，加快佇列工作的處理速度。詳情請參閱「[DML 陳述式的最佳做法](https://docs.cloud.google.com/bigquery/docs/data-manipulation-language?hl=zh-tw#best_practices)」。

### 載入 CSV 檔案配額錯誤

如果您使用 `bq load` 指令搭配 [`--allow_quoted_newlines` 旗標](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#flags_and_arguments_9)載入大型 CSV 檔案，可能會遇到這項錯誤。

**錯誤訊息**

```
Input CSV files are not splittable and at least one of the files is larger than
the maximum allowed size. Size is: ...
```

#### 解析度

如要解決這項配額錯誤，請按照下列步驟操作：

* 將 `--allow_quoted_newlines` 旗標設為 `false`。
* 將 CSV 檔案分割成多個小於 4 GB 的檔案。

如要進一步瞭解將資料載入 BigQuery 時適用的限制，請參閱「[載入工作](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#load_jobs)」。

### 跨區域資料集副本建立限制錯誤

設定[跨區域資料集複製](https://docs.cloud.google.com/bigquery/docs/data-replication?hl=zh-tw) (`ALTER SCHEMA ... ADD REPLICA`) 時，如果超出滾動時間範圍內可為區域新增的資料集副本數量上限，BigQuery 就會傳回這項錯誤 (`reason: apiLimitExceeded`)。

**錯誤訊息**

```
API limit exceeded: Cannot add more than LIMIT replicas for a region within WINDOW day(s)
```

#### 診斷

如果自動化指令碼或基礎架構即程式碼 (IaC) 工具在迴圈中重複建立及捨棄資料集副本 (`ADD REPLICA` 和 `DROP REPLICA`)，就常會發生這項錯誤。

#### 解析度

如要解決這項錯誤，請執行下列操作：

* **稽核自動化和基礎架構即程式碼指令碼。**檢查所有管理資料集副本的 Terraform、部署指令碼或排定工作，確保這些項目不會在每次執行時重複捨棄及重新建立副本。
* **等待滾動週期結束。**請等到錯誤訊息中指定的滾動天數時間範圍結束後，再對該區域執行 `ALTER SCHEMA ... ADD
  REPLICA`。

### 使用者超出並行 `project.lists` 要求配額

如果 Microsoft Power BI 工作透過 Simba ODBC 驅動程式或 DataHub 與 BigQuery 通訊，但因超出 `project.list` API 限制而失敗，就會發生這項錯誤。如要解決這個問題，請採用本節所述的短期或長期解決方法。

**錯誤訊息**

```
Your user exceeded quota for concurrent project.lists requests
```

#### 診斷

當 Power BI 報表重新整理，且 Simba 驅動程式與特定 BigQuery 專案建立連線時，Power BI 的連線和探索階段會發生這項錯誤。

#### 短期解決方案

如要短期內解決這個問題，請採用下列解決方法 (依效果由高至低排序)。視您是使用 Simba 驅動程式或 DataHub 連線至 BigQuery，實施第三或第四項修正。

如需長期修正，請參閱「[長期解決方案](#long-term-resolution)」。

1. **錯開報表重新整理時間**。如果無法修改 DSN，請減少同時要求的數量，以緩解配額問題。不要讓所有報表同時重新整理 (例如上午 9:00)，而是將排程錯開幾分鐘 (例如上午 9:01、9:03 和 9:05)。這種做法可分散 API 呼叫，降低達到並行限制的可能性。
2. **在 Power BI 中實作重試機制**。這種被動策略有助於報表從暫時性失敗中復原。Power BI 內建重試邏輯，可在資料重新整理失敗時自動重試。雖然這種做法無法避免配額錯誤，但可讓管道更具彈性，在 API 呼叫的初始高峰過後，讓報表在後續嘗試中成功。如要實施這項修正，請按照下列步驟操作：

   1. 在 Power BI 服務中，前往資料集的「設定」。
   2. 展開「排定重新整理」部分。在「Retry」(重試) 下方，設定 Power BI 自動重新執行失敗的重新整理作業。
3. **如果是舊版 Simba 驅動程式，請在 ODBC 連線中指定專案 ID**。這項操作可防止驅動程式執行 `projects.list` 探索呼叫。而是直接連線至指定專案，避免不必要的 API 呼叫，並解決配額問題。

   如果未指定專案，較新的驅動程式會立即失敗，並顯示類似 `Unable to establish connection with data source. Missing settings: {[Catalog]}` 的訊息。

   如要修正這個問題，請按照下列步驟操作：

   1. 在執行 Power BI Gateway 或 Power BI Desktop 的機器上，開啟「ODBC Data Sources (64-bit)」應用程式。
   2. 在 BigQuery 的 Simba ODBC 驅動程式主要設定畫面中，在「Catalog (Project)」(目錄 (專案)) 欄位中填入特定 Google Cloud 專案 ID，例如 `my-gcp-project-id`。
4. **如果是舊版 DataHub，請在 DataHub 擷取設定中指定專案 ID**。如果您使用的是 DataHub 而非 Simba 驅動程式，請套用這項修正。與 Simba 類似，較新版本的 DataHub 需要您指定專案 ID，否則無法連線至 BigQuery。

   為避免超出 DataHub 限制，請修改 DataHub 擷取設定，提供要掃描的明確專案 ID 清單。這可防止 DataHub 設定找到服務帳戶可查看的所有專案。

   在 BigQuery 來源 recipe 檔案 (通常是 YAML 檔案) 中，使用 `project_ids` 設定列舉要擷取的專案。接著，使用新設定重新部署 DataHub 擷取配方。請參閱以下範例和 DataHub 提供的[這個較長範例](https://github.com/datahub-project/datahub/blob/master/metadata-ingestion/examples/recipes/bigquery_to_datahub.dhub.yaml)。

   以下是 DataHub 設定程式碼片段範例：

   ```
     source:
     type: "bigquery"
     config:
       # Instead of relying on discovery, explicitly list the projects.
       # This avoids the problematic projects.list() API call.
       project_ids:
       -  "YOUR_PRODUCTION_PROJECT_ID"
       -  "YOUR_ANALYTICS_PROJECT_ID"
       -  "ANOTHER_BQ_PROJECT"
   ```

#### 長期解決方案

如要長期解決這個錯誤訊息，最佳做法是為每個函式建立獨立的專屬Google Cloud 服務帳戶。例如，為所有 Power BI 報表建立服務帳戶，並為 DataHub 擷取作業建立服務帳戶。

這項最佳做法可將 API 用量隔離到不同的配額 bucket，並防止 DataHub 中的高負載工作導致 Power BI 中的重要業務報表失敗。

請按照下列各節的行動計畫，解決 Power BI 和 DataHub 的長期配額錯誤。

##### 第 1 階段：準備

1. 通知 Power BI 閘道和 DataHub 設定的擁有者，您將進行協調變更，解決持續發生的工作失敗問題。
2. 在 Google Cloud 控制台中，[建立](https://docs.cloud.google.com/iam/docs/service-accounts-create?hl=zh-tw)兩個新的服務帳戶，例如 `sa-powerbi-gateway@...` 和 `sa-datahub-ingestion@...`。
3. 為 Power BI 和 DataHub 服務帳戶[建立](https://docs.cloud.google.com/iam/docs/keys-create-delete?hl=zh-tw)服務帳戶金鑰。
4. [授予](https://docs.cloud.google.com/iam/docs/manage-access-service-accounts?hl=zh-tw)每個新服務帳戶最小權限，方法是指派下列 Identity and Access Management 角色，讓帳戶能在相關 Identity and Access Management (IAM) 中執行工作。避免指派過於廣泛的角色，例如 **ProjectEditor**。

###### 必要的角色

Power BI 的服務帳戶會執行查詢，並從資料表讀取資料。在每個包含 Power BI 必須存取資料的 Google Cloud 專案中，將下列角色授予服務帳戶。如要進一步瞭解這些角色，請參閱「[BigQuery 角色](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery-roles)」。

* [**BigQuery 資料檢視者**](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.dataViewer)：提供資料集、資料表和檢視表的唯讀存取權。
* [**BigQuery 工作使用者**](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.jobUser)：提供執行工作 (包括查詢) 的權限，這是 Power BI 執行要求所不可或缺的權限。

DataHub 擷取作業的服務帳戶只需要讀取中繼資料，例如資料表名稱、結構定義和說明，不需要讀取資料表中的資料。在專案層級，為 DataHub 掃描的每個專案授予下列角色。如要進一步瞭解這些角色，請參閱「[BigQuery 的 IAM 角色](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw)」。

[**BigQuery 中繼資料檢視者**](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.metadataViewer)：這個角色專門用於讀取中繼資料。可列出資料集和資料表，並查看其中繼資料，但無法存取基礎資料。

##### 階段 2：協調推出

在低使用期間，Power BI 管理員會執行下列步驟，更新閘道機器上的 ODBC DSN 設定：

1. 變更驗證方式，改用先前步驟中建立的新 `sa-powerbi-gateway@...` 服務帳戶金鑰。
2. 如果尚未執行短期修正，請在 ODBC 驅動程式的「Catalog (Project)」(目錄 (專案)) 欄位中輸入 Google Cloud專案 ID。
3. 請 DataHub 擁有者更新 BigQuery 來源設定 YAML 檔案。
4. 指向先前步驟中建立的新 `sa-datahub-ingestion@...` 服務帳戶金鑰。
5. 如果尚未執行短期修正，請使用 `project_ids` 參數明確列出要掃描的專案。
6. 使用新設定重新部署 DataHub 擷取配方。

##### 階段 3：驗證與監控

為驗證及監控修正效果，Power BI 和 DataHub 管理員會執行下列步驟：

1. 手動觸發幾份重要 Power BI 報表的重新整理作業，並在 DataHub 中執行新的擷取作業。確認這些工作順利完成，未發生配額錯誤。
2. 為確保不再發生 `Quota exceeded: Your user exceeded quota for concurrent
   project.lists requests` 錯誤，請監控應用程式記錄或商業智慧工具執行記錄。
3. 選用：確認相關聯服務帳戶的 `projects.list` API 呼叫總量或相關 `403` 錯誤是否減少：

   1. 在 Google Cloud 控制台中，前往 BigQuery API 的「API/Service Details」(API/服務詳細資料) 頁面

      [前往「APIs & Services」(API 和服務) 頁面](https://console.cloud.google.com/apis/api/bigquery.googleapis.com/metrics?hl=zh-tw)
   2. 查看「Metrics」(指標) 分頁中的資訊主頁，確認呼叫量和相關 403 錯誤是否減少。

管理員應該會看到這項特定 API 呼叫的使用量大幅且永久下降，確認修正成功。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-10-24 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-10-24 (世界標準時間)。"],[],[]]