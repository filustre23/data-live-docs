Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 探索 Cloud Storage 資料並匯入目錄

本文說明如何使用 Knowledge Catalog 自動探索功能。這項 BigQuery 功能可掃描 Cloud Storage 值區中的資料，然後擷取中繼資料並建立目錄。在探索掃描作業中，自動探索功能會為結構化資料建立 BigLake 或外部資料表，並為非結構化資料建立物件資料表。這個集中式資料表可簡化 AI 輔助的資料洞察、資料安全性和治理。

如要自動探索 Cloud Storage 資料，請建立並執行探索掃描作業。

自動探索也稱為獨立探索。

## 探索掃描總覽

探索掃描會執行下列動作：

* 掃描 Cloud Storage bucket 或路徑中的資料。
* 將結構化和半結構化資料分組到資料表中。
* 收集中繼資料，例如資料表名稱、結構定義和分區定義。
* 使用結構定義和分割區定義，在 BigQuery 中建立及更新 [BigLake 外部](https://docs.cloud.google.com/bigquery/docs/biglake-intro?hl=zh-tw)、
  [非 BigLake 外部](https://docs.cloud.google.com/bigquery/docs/external-tables?hl=zh-tw)、
  或 [BigLake 物件](https://docs.cloud.google.com/bigquery/docs/object-table-introduction?hl=zh-tw)
  資料表。

如果是圖片和影片等非結構化資料，探索掃描會偵測並註冊共用相同資料檔案格式的檔案群組。檔案必須位於包含相同檔案格式的資料夾中。舉例來說，`gs://images/group1` 只能包含 GIF 圖片，`gs://images/group2` 只能包含 JPEG 圖片，探索掃描才能偵測及註冊兩個 BigLake 物件資料表。

如果是 Avro 等結構化資料，探索掃描會將檔案群組註冊為 BigLake 外部資料表，且只會偵測位於含有相同資料格式和相容結構定義的資料夾中的檔案。

探索掃描支援下列格式：

**結構化和半結構化**

* Parquet
* Avro
* ORC
* JSON (僅限[以換行符號分隔的格式](https://github.com/ndjson/ndjson-spec))
* CSV (但不得為含有註解列的 CSV 檔案)

[**非結構化**](https://docs.cloud.google.com/bigquery/docs/object-table-introduction?hl=zh-tw#supported_object_files)

* 圖片 (例如 JPEG、PNG 和 BMP)
* 文件 (例如 PDF、投影片簡報和文字報表)
* 音訊或視訊 (例如 WAV、MP3 和 MP4)

**注意：** 探索掃描不支援 Apache Iceberg 和 Delta Lake 資料表格式。

探索掃描支援下列壓縮格式：

**結構化和半結構化資料**

* 下列格式的內部壓縮：

  | 壓縮 | 副檔名範例 | 支援的格式 |
  | --- | --- | --- |
  | gzip | `.gz.parquet` | Parquet |
  | LZ4 | `.lz4.parquet` | Parquet |
  | Snappy | `.snappy.parquet` | Parquet、ORC、Avro |
  | LZO | `.lzo.parquet` | Parquet、ORC |
* JSON 和 CSV 檔案的外部壓縮：

  + gzip
  + bzip2

**非結構化資料**

如果是物件資料表，壓縮作業主要透過 [Cloud Storage 物件中繼資料](https://docs.cloud.google.com/storage/docs/metadata?hl=zh-tw)管理，而非 BigQuery 內部設定。

* 標準中繼資料壓縮：如果檔案使用標準的 .gz 或 .bz2 副檔名，BigQuery 會自動辨識以 gzip 和 bzip2 壓縮的檔案。
* Content-Encoding：您可以在 Cloud Storage 中使用 [Content-Encoding gzip](https://docs.cloud.google.com/storage/docs/metadata?hl=zh-tw#content-encoding) 中繼資料，提供壓縮檔案，同時保留原始內容類型。
* 媒體內部壓縮：系統原生支援本質上經過壓縮的格式 (例如圖片的 JPEG、音訊的 MP3、影片的 MP4)。

如要瞭解探索掃描支援的資料表數量上限，請參閱「[配額與限制](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#dataplex-discovery)」。

探索到的資料表會以 BigLake 外部資料表、BigLake 物件資料表或外部資料表的形式，在 BigQuery 中註冊。這樣一來，他們就能在 BigQuery 中分析資料。BigLake 資料表和物件資料表的中繼資料快取功能也會啟用。所有 BigLake 資料表都會自動擷取至 Knowledge Catalog，供您搜尋及探索。

## 事前準備

啟用 Dataplex API。

**啟用 API 時所需的角色**

如要啟用 API，您需要服務使用情形管理員 IAM 角色 (`roles/serviceusage.serviceUsageAdmin`)，其中包含 `serviceusage.services.enable` 權限。[瞭解如何授予角色](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)。

[啟用 API](https://console.cloud.google.com/flows/enableapi?apiid=dataplex.googleapis.com&hl=zh-tw)

**注意：** 下一節列出的角色適用於標準探索掃描。如要使用非結構化資料語意推論功能，從檔案中擷取 AI 輔助洞察資料，您也必須套用「[使用非結構化資料的資料洞察](https://docs.cloud.google.com/dataplex/docs/use-data-insights-unstructured-data?hl=zh-tw#roles-permissions)」一文列出的其他角色。

### Knowledge Catalog 服務帳戶的必要角色

開始前，請先在專案中將 IAM 權限指派給 Knowledge Catalog 服務帳戶。

```
  service-PROJECT_NUMBER@gcp-sa-dataplex.iam.gserviceaccount.com
```

將 `PROJECT_NUMBER` 替換為已啟用 Dataplex API 的專案。

為確保 Dataplex 服務帳戶具備必要權限，能建立及執行探索掃描，請要求系統管理員將下列 IAM 角色授予 Dataplex 服務帳戶：

**重要事項：**您必須將這些角色授予 Dataplex 服務帳戶，*而非*使用者帳戶。如果未將角色授予正確的主體，可能會導致權限錯誤。

* [Dataplex Discovery 服務代理](https://docs.cloud.google.com/iam/docs/roles-permissions/dataplex?hl=zh-tw#dataplex.discoveryServiceAgent)  (`roles/dataplex.discoveryServiceAgent`)
  儲存空間 bucket
* 使用者專案的 [Dataplex Discovery 發布服務代理](https://docs.cloud.google.com/iam/docs/roles-permissions/dataplex?hl=zh-tw#dataplex.discoveryPublishingServiceAgent)  (`roles/dataplex.discoveryPublishingServiceAgent`)
* 建立 BigLake 資料表：
  BigQuery 連線上的 [Dataplex Discovery BigLake 發布服務代理](https://docs.cloud.google.com/iam/docs/roles-permissions/dataplex?hl=zh-tw#dataplex.discoveryBigLakePublishingServiceAgent)  (`roles/dataplex.discoveryBigLakePublishingServiceAgent`)

如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

這些預先定義的角色具備建立及執行探索掃描作業所需的權限。如要查看確切的必要權限，請展開「Required permissions」(必要權限) 部分：

#### 所需權限

如要建立及執行探索掃描作業，必須具備下列權限：

* `bigquery.datasets.create`
  資料來源專案
* `storage.buckets.get`
  資料來源 bucket
* `storage.objects.get`
  資料來源 bucket
* `storage.objects.list`
  資料來源 bucket
* `bigquery.datasets.get`
  資料來源專案
* 提供連線：
  + `bigquery.connections.delegate`
    在 BigQuery 連線上
  + `bigquery.connections.use`
    在 BigQuery 連線上

管理員或許還可透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)，授予 Dataplex 服務帳戶這些權限。

### BigQuery 連線服務帳戶的必要角色

為確保 BigQuery Connection 服務帳戶具備建立探索掃描的必要權限，請要求系統管理員在 Cloud Storage bucket 上，將 [Dataplex Discovery 服務代理](https://docs.cloud.google.com/iam/docs/roles-permissions/dataplex?hl=zh-tw#dataplex.discoveryServiceAgent)  (`roles/dataplex.discoveryServiceAgent`) IAM 角色授予 BigQuery Connection 服務帳戶。

**重要事項：**您必須將這個角色授予 BigQuery 連線服務帳戶，*而非*使用者帳戶。如果未將角色授予正確的主體，可能會導致權限錯誤。
如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和機構的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

這個預先定義的角色具備建立探索掃描作業所需的權限。如要查看確切的必要權限，請展開「Required permissions」(必要權限) 部分：

#### 所需權限

如要建立探索掃描作業，必須具備下列權限：

* `bigquery.datasets.create`
  資料來源專案
* `storage.buckets.get`
  資料來源 bucket
* `storage.objects.get`
  資料來源 bucket
* `storage.objects.list`
  資料來源 bucket
* `bigquery.datasets.get`
  資料來源專案
* 提供連線：
  + `bigquery.connections.delegate`
    在 BigQuery 連線上
  + `bigquery.connections.use`
    在 BigQuery 連線上

管理員或許還可透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)，將這些權限授予 BigQuery 連線服務帳戶。

### 終端使用者必須具備的角色

如要取得建立及管理資料探索掃描作業所需的權限，請要求管理員授予您 Cloud Storage bucket 的下列 IAM 角色：

* 具備 DataScan 資源的完整存取權限：
  Dataplex DataScan 管理員 (`roles/dataplex.dataScanAdmin`) - 您的專案
* 具備 DataScan 資源的寫入權限：
  Dataplex DataScan 編輯者 (`roles/dataplex.dataScanEditor`) - 您的專案
* 具備 DataScan 資源的讀取權限，結果除外：
  Dataplex DataScan 檢視者 (`roles/dataplex.dataScanViewer`) - 您的專案
* 具備 DataScan 資源的讀取權限，包含結果：
  Dataplex DataScan 資料檢視者 (`roles/dataplex.dataScanDataViewer`) - 您的專案

如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

這些預先定義的角色具備建立及管理資料探索掃描作業所需的權限。如要查看確切的必要權限，請展開「Required permissions」(必要權限) 部分：

#### 所需權限

如要建立及管理資料探索掃描作業，您必須具備下列權限：

* 建立 DataScan：
  `dataplex.datascans.create`
  在專案中
* 刪除 DataScan：
  `dataplex.datascans.delete`
  在專案或 DataScan 資源上
* 查看 DataScan 詳細資料 (不含結果)：
  `dataplex.datascans.get`
  投影機上的 DataScan 資源
* 查看 DataScan 詳細資料，包括結果：
  `dataplex.datascans.getData`
  在專案或 DataScan 資源中
* 列出 DataScan：
  `dataplex.datascans.list`
  專案或 DataScan 資源
* 執行 DataScan：
  `dataplex.datascans.run`
  在專案或 DataScan 資源上
* 更新 DataScan 的說明：
  `dataplex.datascans.update`
  在投影機上投影 DataScan 資源
* 查看 DataScan 的 IAM 權限：
  `dataplex.datascans.getIamPolicy`
  在專案或 DataScan 資源上
* 在 DataScan 上設定 IAM 權限：
  `dataplex.datascans.setIamPolicy`
  在專案或 DataScan 資源上

您或許還可透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)取得這些權限。

## 建立探索掃描作業

如要探索資料，請建立並執行探索掃描作業。您可以設定掃描時間表，也可以視需要執行掃描。

探索掃描作業執行時，會在 BigQuery 中建立與掃描的 Cloud Storage bucket 相對應的新資料集。BigQuery 資料集名稱與 Cloud Storage 值區名稱相同。儲存空間名稱中的無效字元會替換為底線。如果資料集名稱無法使用，系統會附加後置字元 (例如 `_discovered_001`)。資料集包含探索掃描建立的 BigLake 外部資料表或非 BigLake 外部資料表，以供進一步分析。

### 控制台

1. 前往 Google Cloud 控制台的「Metadata curation」(中繼資料管理) 頁面。

   [前往「中繼資料彙整」頁面](https://console.cloud.google.com/bigquery/governance/metadata-curation/cloud-storage-discovery?hl=zh-tw)
2. 在「Cloud Storage discovery」(Cloud Storage 探索) 分頁中，按一下「Create」(建立)。
3. 在「建立探索掃描」窗格中，設定要掃描的資料詳細資料。
4. 輸入掃描名稱。
5. 在「掃描 ID」欄位中，輸入符合 [Google Cloud資源命名慣例的專屬 ID。 Google Cloud](https://docs.cloud.google.com/compute/docs/naming-resources?hl=zh-tw#resource-name-format)如未提供 ID，探索掃描作業會產生掃描 ID。
6. 選用：提供掃描說明。
7. 如要指定包含待掃描檔案的 Cloud Storage bucket，請在「Bucket」欄位中瀏覽並選取該 bucket。
8. 選用：提供[檔案篩選的 glob 模式清單](https://en.wikipedia.org/wiki/Glob_(programming))，定義要納入或排除在探索掃描範圍內的資料。

   * **包含**：如果只應掃描部分資料，請提供與要納入的物件相符的 glob 模式清單。
   * **排除**：提供與要排除的物件相符的 glob 模式清單。

   舉例來說，如要從探索掃描中排除 `gs://test_bucket/foo/..`，請輸入 `**/foo/**` 做為排除路徑。引號會導致錯誤。請務必輸入 `**/foo/**`，而非 `"**/foo/**"`。

   如果同時提供納入模式和排除模式，系統會先套用排除模式。
9. 在「非結構化資料選項」部分，選取「啟用語意推論」。

   如要在 Knowledge Catalog 中查看非結構化資料的資料洞察，就必須選取這個選項。詳情請參閱「[關於非結構化資料的資料洞察](https://docs.cloud.google.com/dataplex/docs/data-insights-unstructured-data?hl=zh-tw)」。
10. 選用步驟：在「專案」中，選取包含探索掃描所建立 BigLake 外部或非 BigLake 外部資料表的 BigQuery 資料集專案。如未提供，系統會在包含 Cloud Storage bucket 的專案中建立資料集。
11. 在「位置類型」中，選取「區域」或「多區域」(視可用選項而定)，建立 BigQuery 發布資料集。
12. 如要從掃描的資料建立 BigLake 資料表，請在「連線 ID」欄位中提供 Google Cloud 資源連線 ID。詳情請參閱 [Google Cloud BigQuery 中的資源連線](https://docs.cloud.google.com/bigquery/docs/connections-api-intro?hl=zh-tw#cloud-resource-connections)。

    您可以在與 BigQuery 資料集位置相同的位置建立新的連線 ID，[與 Cloud Storage 值區位置相容](https://docs.cloud.google.com/bigquery/docs/external-tables?hl=zh-tw#storage-location-considerations)。

    如未提供資源連線 ID，探索掃描會建立[非 BigLake 外部資料表](https://docs.cloud.google.com/bigquery/docs/external-data-sources?hl=zh-tw#non-biglake-tables)。如要瞭解這些外部資料表類型的差異，以及探索服務可能選擇其中一種的原因，請參閱[行為差異比較](https://docs.cloud.google.com/bigquery/docs/external-data-sources?hl=zh-tw#external_data_source_feature_comparison)。
13. 在「探索頻率」部分，設定探索掃描的執行時間：

    * **重複**：掃描作業會依預先定義的時間表執行。提供掃描開始時間、掃描天數和頻率 (例如每小時)。
    * **隨選**：掃描作業會視需要執行。
14. 選用：在「JSON 或 CSV 規格」部分，指定掃描作業應如何處理 JSON 和 CSV 檔案。按一下「JSON 或 CSV 規格」。

    1. 如要設定 JSON 選項，請選取「啟用 JSON 剖析選項」。
       * **停用型別推斷**：探索掃描作業是否應在掃描資料時推斷資料型別。如果停用 JSON 資料的型別推斷功能，所有資料欄都會註冊為原始型別，例如字串、數字或布林值。
       * **編碼格式**：資料的字元編碼，例如 UTF-8、US-ASCII 或 ISO-8859-1。如未指定值，系統會預設使用 UTF-8。
    2. 如要設定 CSV 選項，請勾選「啟用 CSV 剖析選項」。
       * **停用型別推斷**：探索掃描作業是否應在掃描資料時推斷資料型別。如果停用 CSV 資料的型別推斷功能，所有資料欄都會註冊為字串。
       * **標題列**：標題列數，可以是 `0` 或 `1`。
         如果指定值 `0`，探索掃描會推斷標題，並從檔案中擷取資料欄名稱。預設值為 `0`。
       * **資料欄分隔符號字元**：用來分隔值的字元。請提供單一字元，即 `\r` (回車) 或 `\n` (換行)。預設值為半形逗號 (`,`)。
       * **編碼格式**：資料的字元編碼，例如 `UTF-8`、`US-ASCII` 或 `ISO-8859-1`。如未指定值，系統會預設使用 UTF-8。
15. 按一下「建立」 (排定掃描時間)、「立即執行」 (隨選掃描) 或「建立並執行」 (一次性掃描)。

    系統會按照您設定的時間表執行排定的掃描作業。

    建立隨選掃描作業時，系統會先執行一次掃描，您也可以隨時執行掃描。探索掃描作業可能需要幾分鐘才能完成。

    系統會自動執行一次性掃描，當探索掃描達到定義的存留時間 (TTL) 門檻時，系統會自動刪除掃描結果。存留時間值會決定探索掃描在執行後維持有效狀態的時間長度。存留時間值可以介於 0 秒 (立即刪除) 至 365 天。如果探索掃描未指定 TTL，系統會在 24 小時後自動刪除。

### gcloud

如要建立探索掃描，請使用 [`gcloud dataplex datascans create data-discovery`](https://docs.cloud.google.com/sdk/gcloud/reference/dataplex/datascans/create/data-discovery?hl=zh-tw) 指令。

```
gcloud dataplex datascans create data-discovery --location=LOCATION
--data-source-resource=BUCKET_PATH
```

更改下列內容：

* `LOCATION`：您要建立探索掃描的位置
* `BUCKET_PATH`：要掃描的 bucket 的 Cloud Storage 路徑

### REST

如要建立探索掃描作業，請使用 [`dataScans.create` 方法](https://docs.cloud.google.com/dataplex/docs/reference/rest/v1/projects.locations.dataScans/create?hl=zh-tw)。

## 查詢已發布的 BigLake 資料表

執行探索掃描後，BigLake 資料表會發布至 BigQuery 中的新資料集。接著，您就能在 BigQuery 中使用 SQL 分析資料表，或在 Managed Service for Apache Spark 中使用 Apache Spark 或 HiveQL 分析資料表。

### SQL

您可以在 BigQuery 中查看或查詢資料表。如要進一步瞭解如何在 BigQuery 中執行查詢，請參閱「[執行查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw)」。

### Apache Spark

如要在 Managed Service for Apache Spark 無伺服器工作上，使用 Spark SQL 查詢 BigLake 資料表，請按照下列步驟操作：

1. 建立類似下列範例指令碼的 PySpark 指令碼：

   ```
   from pyspark.sql import SparkSession
   session = (
     SparkSession.builder.appName("testing")
       .config("viewsEnabled","true")
       .config("materializationDataset", "DATASET_ID")
       .config("spark.hive.metastore.bigquery.project.id", "PROJECT_ID")
       .config("spark.hive.metastore.client.factory.class", "com.google.cloud.bigquery.metastore.client.BigQueryMetastoreClientFactory")
       .enableHiveSupport()
       .getOrCreate()
   )

   session.sql("show databases").show()
   session.sql("use TABLE_NAME").show()
   session.sql("show tables").show()

   sql = "SELECT * FROM DATASET_ID.TABLE_ID LIMIT 10"
   df = session.read.format("bigquery").option("dataset", "DATASET_ID").load(sql)
   df.show()
   ```

   更改下列內容：

   * `DATASET_ID`：使用者具有建立權限的資料集 ID
   * `PROJECT_ID`：BigLake 資料表所在專案的 ID
   * `TABLE_NAME`：BigLake 資料表名稱
   * `TABLE_ID`：BigLake 資料表的 ID
2. [提交批次工作](https://docs.cloud.google.com/dataproc-serverless/docs/quickstarts/spark-batch?hl=zh-tw#submit_a_spark_batch_workload)。

## 管理已發布的 BigLake 資料表

探索掃描作業會在 BigQuery 中建立及管理已發布的 BigLake 資料表。根據預設，每次執行排定或隨選掃描時，探索掃描都會處理新資料探索、結構定義推論和結構定義演變。如要指出中繼資料是由掃描作業管理，掃描作業會發布標籤設為 `discovery-managed` 的資料表 `metadata-managed-mode`。

如要自行管理結構定義和其他中繼資料 (例如 CSV 或 JSON 選項)，請將 `metadata-managed-mode` 標籤設為 `user_managed`。這樣下次執行探索掃描時，結構定義就不會變更。如果探索掃描推斷的結構定義不正確，或與特定資料表的預期結構定義不同，這個方法就非常實用。將 `metadata-managed-mode` 標籤設為 `user_managed`，即可降低費用。

如要更新標籤，可以[編輯標籤鍵的值](https://docs.cloud.google.com/bigquery/docs/updating-labels?hl=zh-tw#updating_a_table_or_view_label)，將 `metadata-managed-mode` 變更為 `user_managed`，而非 `discovery-managed`。在這種情況下，只要資料表附加 `user_managed` 標籤，探索掃描作業就不會更新資料表的結構定義。

**注意：** 即使資料表是由探索掃描管理，您仍可套用存取權政策，例如[欄層級安全防護機制](https://docs.cloud.google.com/bigquery/docs/column-level-security-intro?hl=zh-tw)和[資料列層級安全防護機制](https://docs.cloud.google.com/bigquery/docs/row-level-security-intro?hl=zh-tw)。

### 更新已發布的 BigLake 資料表

如果使用預設設定，透過探索掃描作業發布 BigLake 資料表，系統會在每次以排定頻率執行探索掃描作業時，自動更新結構定義和其他中繼資料。

如要更新已發布的 BigLake 資料表，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」頁面](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. [更新一或多個資料表屬性](https://docs.cloud.google.com/bigquery/docs/managing-tables?hl=zh-tw#updating_table_properties)。
3. 點選左側窗格中的 explore「Explorer」。

   如果沒有看到左側窗格，請按一下 last\_page「Expand left pane」(展開左側窗格)，開啟窗格。
4. 在「Explorer」窗格中展開專案，按一下「Datasets」(資料集)，然後選取資料集。
5. 依序點選「總覽」**>「表格」**，然後選取所需表格。
6. 在「詳細資料」分頁的「標籤」部分，確認 **metadata-managed-mode** 標籤已設為 **user\_managed**。如果設為其他值，請按照下列步驟操作：

   1. 按一下「編輯詳細資料」edit。
   2. 在「metadata-managed-mode」鍵旁邊的「value」欄位中，輸入 `user_managed`。

**注意：** 更新結構定義的資料表會用於 SQL 和 Spark 查詢。下次執行探索掃描時，資料表的中繼資料不會變更。

### 刪除已發布的 BigLake 資料表

如要刪除已發布的 BigLake 表格，請按照下列步驟操作：

1. [刪除 Cloud Storage bucket 中資料表的資料檔案](https://docs.cloud.google.com/storage/docs/deleting-objects?hl=zh-tw)。
2. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」頁面](https://console.cloud.google.com/bigquery?hl=zh-tw)
3. 點選左側窗格中的 explore「Explorer」。
4. 在「Explorer」窗格中展開專案，按一下「Datasets」(資料集)，然後選取資料集。
5. 依序點選「總覽」**>「表格」**，然後選取所需表格。
6. 在「詳細資料」窗格的「標籤」部分，確認「metadata-managed-mode」標籤未設為 `user_managed`。如果設為 `user_managed`，請按照下列步驟操作：

   1. 按一下「編輯詳細資料」圖示 edit。
   2. 在「metadata-managed-mode」鍵旁邊的「value」欄位中，輸入 `discovery-managed`。

      **注意：** 如果 **metadata-managed-mode** 標籤設為 `user_managed`，探索掃描不會覆寫資料表的中繼資料，因此資料表不會遭到刪除。
7. 按一下「執行」。探索掃描作業會視需求執行。

探索掃描作業執行完畢後，BigLake 資料表會在 BigQuery 中刪除，且無法透過 Spark 列出或查詢。

## 依需求執行探索掃描

如要視需要執行探索掃描，請選取下列其中一個選項。

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」頁面](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在導覽選單中，依序點選「治理」**>**「中繼資料管理」。
3. 在「Cloud Storage discovery」窗格中，按一下要執行的探索掃描。
4. 按一下「立即執行」。

### gcloud

如要執行探索掃描，請使用 [`gcloud dataplex datascans run` 指令](https://docs.cloud.google.com/sdk/gcloud/reference/dataplex/datascans/run?hl=zh-tw)：

```
gcloud dataplex datascans run DATASCAN \
  --location=LOCATION
```

請替換下列變數：

* `LOCATION`：建立探索掃描的 Google Cloud 區域。
* `DATASCAN`：探索掃描的名稱。

### REST

如要視需要執行探索掃描，請使用 Dataplex API 中的 [`dataScans.run` 方法](https://docs.cloud.google.com/dataplex/docs/reference/rest/v1/projects.locations.dataScans/run?hl=zh-tw)。

## 列出探索掃描作業

如要列出探索掃描結果，請選取下列其中一個選項。

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」頁面](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在導覽選單中，依序點選「治理」**>**「中繼資料管理」。
3. 「Cloud Storage 探索」窗格會列出專案中建立的探索掃描作業。

### gcloud

```
gcloud dataplex datascans list --location=LOCATION --project=PROJECT_ID
```

更改下列內容：

* `LOCATION`：專案位置
* `PROJECT_ID`：您的 Google Cloud 專案 ID

### REST

如要擷取專案中的探索掃描清單，請使用 Dataplex API 中的 [`dataScans.list` 方法](https://docs.cloud.google.com/dataplex/docs/reference/rest/v1/projects.locations.dataScans/list?hl=zh-tw)。

## 查看探索掃描作業

如要查看探索掃描結果，請選取下列其中一個選項。

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」頁面](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在導覽選單中，依序點選「治理」**>**「中繼資料管理」。
3. 在「Cloud Storage discovery」(Cloud Storage 探索) 窗格中，按一下要查看詳細資料的探索掃描。

   * 「掃描詳細資料」部分會顯示探索掃描的詳細資料。
   * 「掃描狀態」部分會顯示最新掃描工作的探索結果。

### gcloud

```
gcloud dataplex datascans jobs describe JOB \
    --location=LOCATION \
    --datascan=DATASCAN \
    --view=FULL
```

更改下列內容：

* `JOB`：探索掃描作業的作業 ID。
* `LOCATION`：建立探索掃描的 Google Cloud 區域。
* `DATASCAN`：工作所屬的探索掃描名稱。
* `--view=FULL`：查看探索掃描作業結果。

### REST

如要查看資料探索掃描結果，請使用 Dataplex API 中的 [`dataScans.get` 方法](https://docs.cloud.google.com/dataplex/docs/reference/rest/v1/projects.locations.dataScans/get?hl=zh-tw)。

### 查看歷來探索掃描結果

如要查看歷來探索掃描結果，請選取下列其中一個選項。

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」頁面](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在導覽選單中，依序點選「治理」**>**「中繼資料管理」。
3. 在「Cloud Storage discovery」(Cloud Storage 探索) 窗格中，按一下要查看詳細資料的探索掃描。
4. 按一下「掃描記錄」窗格。「掃描記錄」窗格會提供過去工作的相關資訊，包括每個工作掃描的記錄數量、每個工作的狀態，以及工作執行時間。
5. 如要查看工作的詳細資訊，請按一下「工作 ID」欄中的工作。

### gcloud

```
gcloud dataplex datascans jobs list \
    --location=LOCATION \
    --datascan=DATASCAN
```

更改下列內容：

* `LOCATION`：建立探索掃描的 Google Cloud 區域。
* `DATASCAN`：工作所屬的探索掃描名稱。

### REST

如要查看探索掃描的所有工作，請使用 Dataplex API 中的 [`dataScans.job/list` 方法](https://docs.cloud.google.com/dataplex/docs/reference/rest/v1/projects.locations.dataScans.jobs/list?hl=zh-tw)。

## 更新探索掃描作業

如要變更探索掃描作業的時間表 (例如從隨選變更為定期)，請更新探索掃描作業。

**注意：** 系統不支援更新一次性探索掃描作業。

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」頁面](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在導覽選單中，依序點選「治理」**>**「中繼資料管理」。
3. 在「Cloud Storage 探索」窗格中，找出要更新的探索掃描作業，然後依序點選「動作」**>「編輯」**。
4. 編輯值。
5. 按一下 [儲存]。

### gcloud

如要更新探索掃描，請使用 [`gcloud dataplex datascans update data-discovery`](https://docs.cloud.google.com/sdk/gcloud/reference/dataplex/datascans/update/data-discovery?hl=zh-tw) 指令。

```
gcloud dataplex datascans update data-discovery SCAN_ID --location=LOCATION --description=DESCRIPTION
```

更改下列內容：

* `SCAN_ID`：要更新的探索掃描 ID
* `LOCATION`：建立探索掃描的 Google Cloud 區域
* `DESCRIPTION`：探索掃描的新說明

### REST

如要更新探索掃描，請使用 Dataplex API 中的 [`dataScans.patch` 方法](https://docs.cloud.google.com/dataplex/docs/reference/rest/v1/projects.locations.dataScans/patch?hl=zh-tw)。

## 刪除探索掃描作業

如要刪除探索掃描作業，請選取下列其中一個選項。

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」頁面](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在導覽選單中，依序點選「治理」**>**「中繼資料管理」。
3. 在「Cloud Storage discovery」(Cloud Storage 探索) **窗格中，找出要刪除的探索掃描作業，然後依序點選「Actions」(動作) >「Delete」(刪除)**。
4. 點選「刪除」。

### gcloud

```
gcloud dataplex datascans delete SCAN_ID --location=LOCATION --async
```

更改下列內容：

* `SCAN_ID`：要刪除的探索掃描 ID。
* `LOCATION`：建立探索掃描的 Google Cloud 區域。

### REST

如要刪除探索掃描，請使用 Dataplex API 中的 [`dataScans.delete` 方法](https://docs.cloud.google.com/dataplex/docs/reference/rest/v1/projects.locations.dataScans/delete?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-14 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-14 (世界標準時間)。"],[],[]]