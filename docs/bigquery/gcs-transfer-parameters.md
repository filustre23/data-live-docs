Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [參考資料](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# Cloud Storage 移轉作業中的執行階段參數

在 Cloud Storage、Azure Blob 儲存空間或 Amazon Simple Storage Service (Amazon S3) 中設定資料移轉作業時，您可以將 URI (或資料路徑) 和目的地資料表轉換為參數。參數化可讓您從依日期排序的值區載入資料。這些參數稱為「執行階段參數」，以便和查詢參數做區別。

在轉移作業中使用執行階段參數，即可達成以下事項：

* 指定將目的地資料表加以分區的方式
* 擷取符合特定日期的檔案

## 可用的執行階段參數

設定 Cloud Storage、Blob 儲存體或 Amazon S3 移轉作業時，您可以使用執行階段參數，指定目的地資料表的分區方式。

| **參數** | **範本類型** | **值** |
| --- | --- | --- |
| `run_time` | 格式化的時間戳記 | 採用世界標準時間，依排程而定。`run_time` 用以表示定期移轉作業的預定執行時間。舉例來說，如果移轉作業設為「每 24 小時」執行一次，就算實際執行時間可能略有不同，但兩次連續查詢之間的 `run_time` 差異都會是 24 小時整。  請參閱 [TransferRun.runTime](https://docs.cloud.google.com/bigquery/docs/reference/datatransfer/rest/v1/projects.locations.transferConfigs.runs?hl=zh-tw) |
| `run_date` | 日期字串 | `run_time` 參數的日期，採用以下格式：`%Y%m%d`；例如 *20180101*。這個格式與擷取時間分區資料表相容。 |

## 範本系統

透過範本語法，Cloud Storage、Blob 儲存體和 Amazon S3 移轉作業支援在目的地資料表名稱中使用執行階段參數。

#### 參數範本語法

範本語法支援基本字串範本和時區設定。參數會以下列格式參照：

* `{run_date}`
* `{run_time[+\-offset]|"time_format"}`

| **參數** | **Purpose** |
| --- | --- |
| `run_date` | 這個參數會由格式為 `YYYYMMDD` 的日期取代。 |
| `run_time` | 這個參數支援下列屬性： `offset` 時區設定，依小時 (h)、分鐘 (m)、秒鐘 (s) 的順序表示。 不支援天 (d)。 可使用小數，例如：`1.5h`。  `time_format` 格式設定字串。最常見的格式參數是年 (%Y)、月 (%m)、日 (%d)。 就分區資料表而言，YYYYMMDD 是必要的後置字串，相當於「%Y%m%d」。  進一步瞭解 [datetime 元素的格式設定](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/functions-and-operators?hl=zh-tw#supported-format-elements-for-datetime)。 |

**使用須知：**

* run\_time、offset 和 time\_format 之間不得有空格字元。
* 如果字串要包含大括號，可以按以下方式加以逸出：`'\{' and '\}'`。
* 如果 time\_format 要包含引號或分隔號，例如 `"YYYY|MM|DD"`，可以在格式字串按以下方式加以逸出：`'\"'` 或 `'\|'`。

#### 參數範本範例

以下範例說明如何以不同的時間格式指定目的地資料表名稱，以及如何設定執行時間時區。

| **執行時間 (世界標準時間)** | **範本參數** | **輸出目的地資料表名稱** |
| --- | --- | --- |
| 2018-02-15 00:00:00 | `mytable` | `mytable` |
| 2018-02-15 00:00:00 | `mytable_{run_time|"%Y%m%d"}` | `mytable_20180215` |
| 2018-02-15 00:00:00 | `mytable_{run_time+25h|"%Y%m%d"}` | `mytable_20180216` |
| 2018-02-15 00:00:00 | `mytable_{run_time-1h|"%Y%m%d"}` | `mytable_20180214` |
| 2018-02-15 00:00:00 | `mytable_{run_time+1.5h|"%Y%m%d%H"}` 或 `mytable_{run_time+90m|"%Y%m%d%H"}` | `mytable_2018021501` |
| 2018-02-15 00:00:00 | `{run_time+97s|"%Y%m%d"}_mytable_{run_time+97s|"%H%M%S"}` | `20180215_mytable_000137` |

**注意：**使用日期或時間參數建立資料表時，如果資料表名稱結尾為日期格式 (例如 `YYYYMMDD`)，BigQuery 會[將這些資料表歸為一組](https://docs.cloud.google.com/bigquery/docs/querying-wildcard-tables?hl=zh-tw)。在 Google Cloud 控制台中，這些分組資料表可能會顯示類似 `mytable_(1)` 的名稱，代表分片資料表的集合。

## 分區選項

BigQuery 中的分區資料表有兩種類型：

* **依擷取時間分區的資料表。**
  Cloud Storage、Blob 儲存空間和 Amazon S3 移轉作業的擷取時間即是移轉作業的執行時間。
* **依資料欄分區的資料表。**資料欄類型必須是 [`TIMESTAMP`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#timestamp_type) 或 [`DATE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#date_type) 資料欄。

如果目的地資料表是依資料欄分區，請在建立目的地資料表和指定結構定義時，設定用來分區的資料欄。如要瞭解如何建立以資料欄分區的資料表，請參閱[建立和使用分區資料表](https://docs.cloud.google.com/bigquery/docs/creating-column-partitions?hl=zh-tw)。

**注意：** 分割資料表時無法指定分鐘數。

### 分區範例

* 無分區的資料表
  + 目的地資料表：`mytable`
* [擷取時間分區資料表](https://docs.cloud.google.com/bigquery/docs/partitioned-tables?hl=zh-tw#ingestion_time)
  + 目的地資料表：`mytable$YYYYMMDD`
  + 請注意，你無法指定分鐘數。
* [資料欄分區資料表](https://docs.cloud.google.com/bigquery/docs/partitioned-tables?hl=zh-tw#date_timestamp_partitioned_tables)
  + 目的地資料表：`mytable`
  + 建立資料表的結構定義時，請將分區資料欄指定為 `TIMESTAMP` 或 `DATE` 資料欄。

## 使用參數的注意事項

* 如果您將資料分區時，是以當地時區為準，則需要使用[範例語法](#templating_system)中的時區機制，手動計算當地時區與世界標準時間的時差。
* 參數中無法指定分鐘數。
* 您可以在 URI 或資料路徑中使用萬用字元，並搭配目的地資料表名稱的參數。

## 執行階段參數範例

下列範例說明如何結合萬用字元和參數，以因應常見用途。假設資料表名稱為 `mytable`，且所有範例的 `run_time` 都是 `2018-02-15 00:00:00` (UTC)。

### 將資料轉移至非分區資料表

此使用案例適用於將新檔案從 Cloud Storage、Blob 儲存體或 Amazon S3 值區載入非分區資料表時。此範例會在 URI 或資料路徑中使用萬用字元，並透過臨時的重新整理移轉作業來擷取新檔案。

| **資料來源** | **來源 URI 或資料路徑** | **目的地資料表名稱** |
| --- | --- | --- |
| Cloud Storage | `gs://bucket/*.csv` | `mytable` |
| Amazon S3 | `s3://bucket/*.csv` | `mytable` |
| blob 儲存空間 | `*.csv` | `mytable` |

### 將包含所有資料的快照載入依擷取時間分區的資料表

在這種情況下，指定的 URI 或資料路徑內所有資料均會移轉至以今日日期分區的資料表。在重新整理移轉作業中，此設定會擷取最近一次載入作業完成後新增的檔案，並將檔案加入特定的分區。

| **資料來源** | **來源 URI 或資料路徑** | **已參數化目的地資料表名稱** | **已評估目的地資料表名稱** |
| --- | --- | --- | --- |
| Cloud Storage | `gs://bucket/*.csv` | `mytable${run_time|"%Y%m%d"}` | `mytable$20180215` |
| Amazon S3 | `s3://bucket/*.csv` | `mytable${run_time|"%Y%m%d"}` | `mytable$20180215` |
| blob 儲存空間 | `*.csv` | `mytable${run_time|"%Y%m%d"}` | `mytable$20180215` |

此使用案例會將今天的資料移轉至以今天日期分區的資料表。如果重新整理移轉作業會擷取符合特定日期的新增檔案，並將資料載入至對應的分區，則同樣適用這個使用案例。

| **資料來源** | **參數化 URI 或資料路徑** | **已參數化目的地資料表名稱** | **已評估的 URI 或資料路徑** | **已評估目的地資料表名稱** |
| --- | --- | --- | --- | --- |
| Cloud Storage | `gs://bucket/events-{run_time|"%Y%m%d"}/*.csv` | `mytable${run_time|"%Y%m%d"}` | `gs://bucket/events-20180215/*.csv` | `mytable$20180215` |
| Amazon S3 | `s3://bucket/events-{run_time|"%Y%m%d"}/*.csv` | `mytable${run_time|"%Y%m%d"}` | `s3://bucket/events-20180215/*.csv` | `mytable$20180215` |
| blob 儲存空間 | `events-{run_time|"%Y%m%d"}/*.csv` | `mytable${run_time|"%Y%m%d"}` | `events-20180215/*.csv` | `mytable$20180215` |

## 後續步驟

* 瞭解如何[設定 Cloud Storage 移轉作業](https://docs.cloud.google.com/bigquery/docs/cloud-storage-transfer?hl=zh-tw)。
* 進一步瞭解 [BigQuery 資料移轉服務](https://docs.cloud.google.com/bigquery/docs/dts-introduction?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-16 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-16 (世界標準時間)。"],[],[]]