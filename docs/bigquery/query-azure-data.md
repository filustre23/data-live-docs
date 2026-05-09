Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 查詢 Blob 儲存體資料

本文說明如何查詢儲存在 [Azure Blob 儲存體 BigLake 資料表](https://docs.cloud.google.com/bigquery/docs/omni-azure-create-external-table?hl=zh-tw)中的資料。

## 事前準備

確認您有 [Blob Storage BigLake 資料表](https://docs.cloud.google.com/bigquery/docs/omni-azure-create-external-table?hl=zh-tw)。

### 必要的角色

如要查詢 Blob 儲存空間 BigLake 資料表，請確保 BigQuery API 的呼叫端具有下列角色：

* BigQuery 連線使用者 (`roles/bigquery.connectionUser`)
* BigQuery 資料檢視者 (`roles/bigquery.dataViewer`)
* BigQuery 使用者 (`roles/bigquery.user`)

呼叫者可以是您的帳戶或 [Blob 儲存空間連線服務帳戶](https://docs.cloud.google.com/bigquery/docs/omni-azure-create-connection?hl=zh-tw#create_an_azure_connection)。視權限而定，您可以將這些角色授予自己，或請系統管理員授予您這些角色。如要進一步瞭解如何授予角色，請參閱「[查看可針對資源授予的角色](https://docs.cloud.google.com/iam/docs/viewing-grantable-roles?hl=zh-tw)」。

如要查看查詢 Blob Storage BigLake 表格的確切必要權限，請展開「Required permissions」(必要權限) 部分：

#### 所需權限

* `bigquery.connections.use`
* `bigquery.jobs.create`
* `bigquery.readsessions.create` (只有在[使用 BigQuery Storage Read API 讀取資料](https://docs.cloud.google.com/bigquery/docs/reference/storage?hl=zh-tw)時才需要)
* `bigquery.tables.get`
* `bigquery.tables.getData`

您或許還可透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)取得這些權限。

## 查詢 Blob 儲存空間 BigLake 資料表

建立 Blob Storage BigLake 資料表後，您就可以[使用 GoogleSQL 語法查詢資料表](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw)，就像查詢標準 BigQuery 資料表一樣。

[快取的查詢結果](https://docs.cloud.google.com/bigquery/docs/cached-results?hl=zh-tw)會儲存在 BigQuery 暫存資料表中。如要查詢臨時 BigLake 資料表，請參閱「[查詢臨時 BigLake 資料表](#query-temp-biglake-table)」。如要進一步瞭解 BigQuery Omni 的限制和配額，請參閱[限制](https://docs.cloud.google.com/bigquery/docs/omni-introduction?hl=zh-tw#limitations)和[配額](https://docs.cloud.google.com/bigquery/docs/omni-introduction?hl=zh-tw#quotas_and_limits)。

在 BigQuery Omni 區域建立預留項目時，請使用 Enterprise 版。如要瞭解如何使用版本建立預留項目，請參閱「[建立預留項目](https://docs.cloud.google.com/bigquery/docs/reservations-tasks?hl=zh-tw#create_reservations)」。

對 Blob 儲存空間 BigLake 資料表執行查詢：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列陳述式：

   ```
   SELECT * FROM DATASET_NAME.TABLE_NAME;
   ```

   更改下列內容：

   * `DATASET_NAME`：您建立的資料集名稱
   * `TABLE_NAME`：您建立的 BigLake 資料表名稱
   * 按一下「執行」play\_circle。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

## 查詢臨時資料表

BigQuery 會建立臨時資料表來儲存查詢結果。如要從暫時性資料表擷取查詢結果，可以使用 Google Cloud 控制台或 [BigQuery API](https://docs.cloud.google.com/bigquery/docs/reliability-read?hl=zh-tw#read_with_api)。

選取下列選項之一：

### 控制台

[查詢參照外部雲端資料的 BigLake 資料表](#query-biglake-table)時，您可以在 Google Cloud 控制台中查看查詢結果。

### API

如要使用 API 查詢 BigLake 資料表，請按照下列步驟操作：

1. 建立[職缺物件](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw)。
2. 呼叫 [`jobs.insert` 方法](https://docs.cloud.google.com/bigquery/docs/reference/v2/jobs/insert?hl=zh-tw)，以非同步方式執行查詢，或呼叫 [`jobs.query` 方法](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs/query?hl=zh-tw)，以同步方式執行查詢，並傳入 `Job` 物件。
3. 傳遞指定的工作參考資料，並透過 [`tabledata.list`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tabledata/list?hl=zh-tw) 方法傳遞查詢結果的指定資料表參考資料，即可使用 [`jobs.getQueryResults`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs/getQueryResults?hl=zh-tw) 讀取資料列。

## 查詢 `_FILE_NAME` 虛擬資料欄

以外部資料來源為基礎的資料表可提供名為 `_FILE_NAME` 的虛擬資料欄。這個資料欄含有該列所屬檔案的完整路徑。此資料欄僅適用於參照儲存在 **Cloud Storage**、**Google 雲端硬碟**、**Amazon S3** 和 **Azure Blob 儲存體**中的外部資料的資料表。

系統會保留 `_FILE_NAME` 資料欄名稱，這表示您無法在任何資料表中使用該名稱建立資料欄。如要選取 `_FILE_NAME` 的值，您必須使用別名。下方範例查詢示範如何透過指派別名 `fn` 給虛擬資料欄的方式來選取 `_FILE_NAME`。

```
  bq query \
  --project_id=PROJECT_ID \
  --use_legacy_sql=false \
  'SELECT
     name,
     _FILE_NAME AS fn
   FROM
     `DATASET.TABLE_NAME`
   WHERE
     name contains "Alex"'
```

更改下列內容：

* `PROJECT_ID` 是有效的專案 ID (如果您使用 Cloud Shell，或是在 Google Cloud CLI 中設定預設專案，則此為選用標記)
* `DATASET` 是儲存永久外部資料表的資料集名稱
* `TABLE_NAME` 是永久外部資料表的名稱

如果查詢在 `_FILE_NAME` 虛擬資料欄上設有篩選述詞，BigQuery 會嘗試略過不符合篩選條件的檔案。使用 `_FILE_NAME` 虛擬資料欄建構查詢述詞時，請套用與[使用虛擬資料欄查詢擷取時間分區資料表](https://docs.cloud.google.com/bigquery/docs/querying-partitioned-tables?hl=zh-tw#query_an_ingestion-time_partitioned_table)類似的建議。

## 後續步驟

* 瞭解如何[在 BigQuery 中使用 SQL](https://docs.cloud.google.com/bigquery/docs/introduction-sql?hl=zh-tw)。
* 瞭解 [BigQuery Omni](https://docs.cloud.google.com/bigquery/docs/omni-introduction?hl=zh-tw)。
* 瞭解 [BigQuery 配額](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-08 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-08 (世界標準時間)。"],[],[]]