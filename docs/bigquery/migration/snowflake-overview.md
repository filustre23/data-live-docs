* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 從 Snowflake 遷移至 BigQuery：總覽

本文說明如何將資料從 Snowflake 遷移至 BigQuery。

如需從其他資料倉儲遷移至 BigQuery 的一般架構，請參閱「[總覽：將資料倉儲遷移至 BigQuery](https://docs.cloud.google.com/bigquery/docs/migration/migration-overview?hl=zh-tw)」。

## 從 Snowflake 遷移至 BigQuery 的簡介

如果是 Snowflake 遷移作業，建議您設定對現有作業影響最小的遷移架構。以下範例顯示的架構可讓您重複使用現有工具和程序，同時將其他工作負載卸載至 BigQuery。

您也可以根據舊版驗證報表和資訊主頁。詳情請參閱「[將資料倉儲遷移至 BigQuery：驗證](https://docs.cloud.google.com/bigquery/docs/migration/migration-overview?hl=zh-tw#7_verify_and_validate)」。

## 遷移個別工作負載

規劃 Snowflake 遷移作業時，建議您依序個別遷移下列工作負載：

### 遷移結構定義

首先，請將 Snowflake 環境中的必要結構定義複製到 BigQuery。建議使用 BigQuery 遷移服務[遷移結構定義](https://docs.cloud.google.com/bigquery/docs/migration/schema-data-overview?hl=zh-tw)。BigQuery 遷移服務支援各種資料模型設計模式，例如[星狀結構定義](https://wikipedia.org/wiki/Star_schema)或[雪花狀結構定義](https://wikipedia.org/wiki/Snowflake_schema)，因此您不必為新的結構定義更新上游資料管道。BigQuery 遷移服務也提供自動結構定義遷移功能，包括結構定義擷取和翻譯功能，可簡化遷移程序。

### 遷移 SQL 查詢

如要遷移 SQL 查詢，BigQuery 遷移服務提供各種 SQL 翻譯功能，可自動將 Snowflake SQL 查詢轉換為 GoogleSQL SQL，例如[批次 SQL 翻譯器](https://docs.cloud.google.com/bigquery/docs/batch-sql-translator?hl=zh-tw) (可大量翻譯查詢)、[互動式 SQL 翻譯器](https://docs.cloud.google.com/bigquery/docs/interactive-sql-translator?hl=zh-tw) (可翻譯個別查詢) 和 [SQL 翻譯 API](https://docs.cloud.google.com/bigquery/docs/api-sql-translator?hl=zh-tw)。這些翻譯服務也包含 Gemini 強化功能，可進一步簡化 SQL 查詢遷移程序。

翻譯 SQL 查詢時，請仔細檢查翻譯後的查詢，確認資料型別和表格結構處理正確。為此，我們建議建立各種情境和資料的測試案例。接著在 BigQuery 中執行這些測試案例，比較結果與原始 Snowflake 結果。如有任何差異，請分析並修正轉換後的查詢。

### 遷移資料

您可以透過多種方式設定資料遷移管道，將資料轉移至 BigQuery。一般來說，這些管道遵循的模式相同：

1. **從來源擷取資料：**將擷取的檔案從來源複製到內部部署環境的暫存儲存空間。詳情請參閱[將資料倉儲遷移至 BigQuery：擷取來源資料](https://docs.cloud.google.com/bigquery/docs/migration/schema-data-overview?hl=zh-tw#extract_the_existing_schema_and_data_into_files)。
2. **將資料轉移到暫存 Cloud Storage 值區：**從來源擷取資料後，請將資料轉移到 Cloud Storage 中的臨時值區。根據轉移的資料量和可用的網路頻寬，您[有幾種選項](https://docs.cloud.google.com/bigquery/docs/migration/schema-data-overview?hl=zh-tw#migrating_data_and_schema_from_on-premises_to_bigquery)。

   請務必確認 BigQuery 資料集、外部資料來源或 Cloud Storage 值區位於相同區域。
3. **將資料從 Cloud Storage 值區載入 BigQuery：**資料現在位於 Cloud Storage 值區中。將資料上傳至 BigQuery 的方式有幾種。這些選項取決於資料的轉換量。或者，您也可以按照 ELT 方法，在 BigQuery 中轉換資料。

   從 JSON、Avro 或 CSV 檔案大量匯入資料時，BigQuery 會自動偵測結構定義，因此您不需要預先定義。如要詳細瞭解 EDW 工作負載的結構定義遷移程序，請參閱「[結構定義和資料遷移程序](https://docs.cloud.google.com/bigquery/docs/migration/schema-data-overview?hl=zh-tw#schema_and_data_migration_process)」。

如需支援 Snowflake 資料遷移的工具清單，請參閱「[遷移工具](#migration_tools)」。

如需設定 Snowflake 資料遷移管道的端對端範例，請參閱「[Snowflake 遷移管道範例](#pipeline-examples)」。

### 最佳化結構定義和查詢

結構定義遷移完成後，您可以測試成效，並根據結果進行最佳化。舉例來說，您可以導入分區功能，提高資料的管理和查詢效率。您可以依擷取時間、時間戳記或整數範圍將資料表分區，藉此提高查詢效能並控管費用。詳情請參閱[分區資料表簡介](https://docs.cloud.google.com/bigquery/docs/partitioned-tables?hl=zh-tw)一文。

叢集資料表是另一種結構定義最佳化方式。您可以建立資料表叢集，根據資料表結構定義中的內容整理資料表資料，進而提升使用篩選子句的查詢或匯總資料的查詢效能。詳情請參閱[叢集資料表簡介](https://docs.cloud.google.com/bigquery/docs/clustered-tables?hl=zh-tw)。

## 支援的資料類型、屬性和檔案格式

Snowflake 和 BigQuery 支援大部分相同的資料類型，但有時會使用不同的名稱。如需 Snowflake 和 BigQuery 支援的完整資料類型清單，請參閱「[資料類型](https://docs.cloud.google.com/bigquery/docs/migration/snowflake-sql?hl=zh-tw#data-types)」。您也可以使用 SQL 翻譯工具 (例如[互動式 SQL 翻譯器](https://docs.cloud.google.com/bigquery/docs/interactive-sql-translator?hl=zh-tw)、[SQL 翻譯 API](https://docs.cloud.google.com/bigquery/docs/api-sql-translator?hl=zh-tw) 或[批次 SQL 翻譯器](https://docs.cloud.google.com/bigquery/docs/batch-sql-translator?hl=zh-tw))，將不同的 SQL 方言翻譯成 GoogleSQL。

如要進一步瞭解 BigQuery 支援的資料類型，請參閱「[GoogleSQL 資料類型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw)」。

Snowflake 可以匯出下列檔案格式的資料。您可以將下列格式的資料直接載入 BigQuery：

* [從 Cloud Storage 載入 CSV 資料](https://docs.cloud.google.com/bigquery/docs/loading-data-cloud-storage-csv?hl=zh-tw)。
* [從 Cloud Storage 載入 Parquet 資料](https://docs.cloud.google.com/bigquery/docs/loading-data-cloud-storage-parquet?hl=zh-tw)。
* [從 Cloud Storage 載入 JSON 資料](https://docs.cloud.google.com/bigquery/docs/loading-data-cloud-storage-json?hl=zh-tw)。
* [查詢 Apache Iceberg 中的資料](https://docs.cloud.google.com/bigquery/docs/iceberg-tables?hl=zh-tw)。

## 遷移工具

下表列出可將資料從 Snowflake 遷移至 BigQuery 的工具。如需瞭解如何在 Snowflake 遷移管道中一併使用這些工具，請參閱 [Snowflake 遷移管道範例](#pipeline-examples)。

* **[`COPY INTO <location>` 指令](https://docs.snowflake.com/en/sql-reference/sql/copy-into-location.html)：**
  在 Snowflake 中使用這項指令，將資料從 Snowflake 資料表直接擷取至指定的 Cloud Storage bucket。如需端對端範例，請參閱 GitHub 上的「[Snowflake to BigQuery (snowflake2bq)](https://github.com/GoogleCloudPlatform/professional-services/tree/master/tools/snowflake2bq)」。
* **[Apache Sqoop](https://sqoop.apache.org/)：**
  如要將資料從 Snowflake 擷取至 HDFS 或 Cloud Storage，請使用 Sqoop 和 Snowflake 的 JDBC 驅動程式提交 Hadoop 工作。Sqoop 會在 [Dataproc](https://docs.cloud.google.com/dataproc/docs?hl=zh-tw) 環境中執行。
* **[Snowflake JDBC](https://docs.snowflake.com/en/user-guide/jdbc.html)：**
  搭配支援 JDBC 的大多數用戶端工具或應用程式使用這個驅動程式。

您可以使用下列一般工具，將資料從 Snowflake 遷移至 BigQuery：

* **[Snowflake 連接器的 BigQuery 資料移轉服務](https://docs.cloud.google.com/bigquery/docs/migration/snowflake-transfer?hl=zh-tw)** [搶先版](https://cloud.google.com/products?hl=zh-tw#product-launch-stages)：
  自動將 Cloud Storage 資料批次移轉至 BigQuery。
* **[Google Cloud CLI](https://docs.cloud.google.com/sdk/gcloud/reference/storage?hl=zh-tw)：**
  使用這個指令列工具，將下載的 Snowflake 檔案複製到 Cloud Storage。
* **[bq 指令列工具](https://docs.cloud.google.com/bigquery/docs/bq-command-line-tool?hl=zh-tw)：**使用這個指令列工具與 BigQuery 互動。
  常見用途包括建立 BigQuery 資料表結構定義、將 Cloud Storage 資料載入資料表，以及執行查詢。
* **[Cloud Storage 用戶端程式庫](https://docs.cloud.google.com/storage/docs/reference/libraries?hl=zh-tw)：**
  使用自訂工具 (採用 Cloud Storage 用戶端程式庫)，將下載的 Snowflake 檔案複製到 Cloud Storage。
* **[BigQuery 用戶端程式庫](https://docs.cloud.google.com/bigquery/docs/reference/libraries?hl=zh-tw)：**
  使用以 BigQuery 用戶端程式庫為基礎建構的自訂工具，與 BigQuery 互動。
* **[BigQuery 查詢排程器](https://docs.cloud.google.com/bigquery/docs/scheduling-queries?hl=zh-tw)：**
  使用這項內建的 BigQuery 功能，排定週期性 SQL 查詢。
* **[Cloud Composer](https://docs.cloud.google.com/composer/docs?hl=zh-tw)：**
  使用這個全代管的 Apache Airflow 環境，自動化調度管理 BigQuery 載入作業和轉換。

如要進一步瞭解如何將資料載入 BigQuery，請參閱[將資料載入 BigQuery](https://docs.cloud.google.com/bigquery/docs/migration/schema-data-overview?hl=zh-tw#loading_the_data_into_bigquery)。

## Snowflake 遷移管道範例

以下各節提供範例，說明如何使用三種不同的程序 (ELT、ETL 和合作夥伴工具)，將資料從 Snowflake 遷移至 BigQuery。

### 擷取、載入及轉換

您可以透過下列兩種方式設定擷取、載入及轉換 (ELT) 程序：

* 使用管道從 Snowflake 擷取資料，並將資料載入至 BigQuery
* 使用其他 Google Cloud 產品從 Snowflake 擷取資料。

#### 使用管道從 Snowflake 擷取資料

如要[從 Snowflake 擷取資料](https://docs.snowflake.com/en/user-guide/data-unload-gcs.html)並直接載入 Cloud Storage，請使用 [snowflake2bq](https://github.com/GoogleCloudPlatform/professional-services/tree/main/tools/snowflake2bq) 工具。

然後，您可以使用下列其中一種工具，將資料從 Cloud Storage 載入至 BigQuery：

* [Cloud Storage 連接器的 BigQuery 資料移轉服務](https://docs.cloud.google.com/bigquery/docs/cloud-storage-transfer-overview?hl=zh-tw)
* 使用 bq 指令列工具的 [`LOAD` 指令](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_load)
* BigQuery API 用戶端程式庫

#### 從 Snowflake 擷取資料的其他工具

您也可以使用下列工具從 Snowflake 擷取資料：

* Dataflow
  + [JDBC 到 BigQuery 範本](https://docs.cloud.google.com/dataflow/docs/guides/templates/provided/jdbc-to-bigquery?hl=zh-tw)
  + [SnowflakeIO 連接器](https://beam.apache.org/documentation/io/built-in/snowflake/)
* [Cloud Data Fusion](https://docs.cloud.google.com/data-fusion/docs?hl=zh-tw)
  + [JDBC 驅動程式](https://docs.cloud.google.com/data-fusion/docs/how-to/using-jdbc-drivers?hl=zh-tw)
* Dataproc
  + [Apache Spark BigQuery 連接器](https://docs.cloud.google.com/dataproc/docs/tutorials/bigquery-connector-spark-example?hl=zh-tw)
  + [Apache Spark 的 Snowflake 連接器](https://docs.snowflake.com/en/user-guide/spark-connector.html)
  + [Hadoop BigQuery 連接器](https://docs.cloud.google.com/dataproc/docs/concepts/connectors/bigquery?hl=zh-tw)
  + 使用 Snowflake 和 Sqoop 的 JDBC 驅動程式，將資料從 Snowflake 擷取至 Cloud Storage：
    - [在 Dataproc 中使用 Apache Sqoop 遷移資料](https://medium.com/google-cloud/moving-data-with-apache-sqoop-in-google-cloud-dataproc-4056b8fa2600)

#### 其他將資料載入 BigQuery 的工具

您也可以使用下列工具將資料載入 BigQuery：

* Dataflow
  + [從 Cloud Storage 讀取](https://beam.apache.org/documentation/programming-guide/#pipeline-io-reading-data)
  + [寫入 BigQuery](https://beam.apache.org/documentation/io/built-in/google-bigquery/#writing-to-bigquery)
  + [Cloud Storage Text 到 BigQuery 範本](https://docs.cloud.google.com/dataflow/docs/guides/templates/provided/cloud-storage-to-bigquery?hl=zh-tw)
* Cloud Data Fusion
  + [建立目標廣告活動管道](https://docs.cloud.google.com/data-fusion/docs/tutorials/targeting-campaign-pipeline?hl=zh-tw)
* Dataproc
  + [搭配 Spark 使用 Cloud Storage 連接器](https://docs.cloud.google.com/dataproc/docs/tutorials/gcs-connector-spark-tutorial?hl=zh-tw)
  + [Spark BigQuery 連接器](https://docs.cloud.google.com/dataproc/docs/tutorials/bigquery-connector-spark-example?hl=zh-tw)
  + [Hadoop Cloud Storage 連接器](https://docs.cloud.google.com/dataproc/docs/concepts/connectors/cloud-storage?hl=zh-tw)
  + [Hadoop BigQuery 連接器](https://docs.cloud.google.com/dataproc/docs/concepts/connectors/bigquery?hl=zh-tw)
* [Dataprep by Trifacta](https://docs.trifacta.com/Dataprep/en/product-overview.html)
  + [從 Cloud Storage 讀取](https://docs.trifacta.com/Dataprep/en/platform/connections/connection-types/google-cloud-storage-access.html##)
  + [寫入 BigQuery](https://docs.trifacta.com/Dataprep/en/platform/connections/connection-types/bigquery-connections.html##)

### 擷取、轉換及載入

如要在將資料載入 BigQuery 前轉換資料，請考慮使用下列工具：

* Dataflow
  + 複製 [JDBC 到 BigQuery 範本](https://docs.cloud.google.com/dataflow/docs/guides/templates/provided/jdbc-to-bigquery?hl=zh-tw)程式碼，並修改範本以新增 [Apache Beam 轉換](https://beam.apache.org/documentation/programming-guide/#transforms)。
* Cloud Data Fusion
  + 建立可重複使用的管道，並使用 [CDAP 外掛程式](https://cdap.io/resources/plugins/)轉換資料。
* Dataproc
  + 使用 [Spark SQL](https://spark.apache.org/docs/latest/sql-programming-guide.html) 或任何支援的 Spark 語言 (例如 Scala、Java、Python 或 R) 中的自訂程式碼轉換資料。

### 合作夥伴適用的遷移工具

有多家供應商專門提供企業資料倉儲遷移服務。如需主要合作夥伴及其提供的解決方案清單，請參閱 [BigQuery 合作夥伴](https://docs.cloud.google.com/bigquery/docs/bigquery-ready-partners?hl=zh-tw)。

## Snowflake 匯出教學課程

下列教學課程說明如何使用 `COPY INTO <location>` Snowflake 指令，將範例資料從 Snowflake 匯出至 BigQuery。如需詳細的逐步程序 (包括程式碼範例)，請參閱[Google Cloud 專業服務的 Snowflake 至 BigQuery 工具](https://github.com/GoogleCloudPlatform/professional-services/tree/master/tools/snowflake2bq)

### 準備匯出

如要準備匯出 Snowflake 資料，請按照下列步驟將 Snowflake 資料擷取至 Cloud Storage 或 Amazon Simple Storage Service (Amazon S3) 值區：

### Cloud Storage

本教學課程會準備 `PARQUET` 格式的檔案。

1. 使用 Snowflake SQL 陳述式建立[具名檔案格式規格](https://docs.snowflake.com/en/user-guide/data-unload-prepare.html#creating-a-named-file-format)。

   ```
   create or replace file format NAMED_FILE_FORMAT
       type = 'PARQUET'
   ```

   將 `NAMED_FILE_FORMAT` 替換為檔案格式的名稱。例如：`my_parquet_unload_format`。
2. 使用 [`CREATE STORAGE INTEGRATION`](https://docs.snowflake.com/en/sql-reference/sql/create-storage-integration) 指令建立整合項目。

   ```
   create storage integration INTEGRATION_NAME
       type = external_stage
       storage_provider = gcs
       enabled = true
       storage_allowed_locations = ('BUCKET_NAME')
   ```

   更改下列內容：

   * `INTEGRATION_NAME`：儲存空間整合的名稱。例如：`gcs_int`
   * `BUCKET_NAME`：Cloud Storage bucket 的路徑。例如：`gcs://mybucket/extract/`
3. 使用 [`DESCRIBE INTEGRATION`](https://docs.snowflake.com/en/sql-reference/sql/desc-integration.html) 指令[擷取 Snowflake 的 Cloud Storage 服務帳戶](https://docs.snowflake.com/en/user-guide/data-load-gcs-config.html#step-2-retrieve-the-cloud-storage-service-account-for-your-snowflake-account)。

   ```
   desc storage integration INTEGRATION_NAME;
   ```

   輸出結果會與下列內容相似：

   ```
   +-----------------------------+---------------+-----------------------------------------------------------------------------+------------------+
   | property                    | property_type | property_value                                                              | property_default |
   +-----------------------------+---------------+-----------------------------------------------------------------------------+------------------|
   | ENABLED                     | Boolean       | true                                                                        | false            |
   | STORAGE_ALLOWED_LOCATIONS   | List          | gcs://mybucket1/path1/,gcs://mybucket2/path2/                               | []               |
   | STORAGE_BLOCKED_LOCATIONS   | List          | gcs://mybucket1/path1/sensitivedata/,gcs://mybucket2/path2/sensitivedata/   | []               |
   | STORAGE_GCP_SERVICE_ACCOUNT | String        | service-account-id@iam.gserviceaccount.com                 |                  |
   +-----------------------------+---------------+-----------------------------------------------------------------------------+------------------+
   ```
4. 授予列為 `STORAGE_GCP_SERVICE_ACCOUNT` 的服務帳戶讀取和寫入權限，存取儲存空間整合指令中指定的值區。在本範例中，請授予 `service-account-id@` 服務帳戶 `<var>UNLOAD_BUCKET</var>` bucket 的讀取和寫入權限。
5. 建立外部 Cloud Storage 階段，參照先前建立的整合。

   ```
   create or replace stage STAGE_NAME
       url='UNLOAD_BUCKET'
       storage_integration = INTEGRATION_NAME
       file_format = NAMED_FILE_FORMAT;
   ```

   更改下列內容：

   * `STAGE_NAME`：Cloud Storage 階段物件的名稱。
     例如：`my_ext_unload_stage`

### Amazon S3

下列範例說明如何[將資料從 Snowflake 資料表移至 Amazon S3 值區](https://docs.snowflake.com/en/user-guide/data-unload-s3.html)：

1. 在 Snowflake 中，[設定儲存空間整合物件](https://docs.snowflake.com/en/user-guide/data-load-s3-config.html#option-1-configuring-a-snowflake-storage-integration)，允許 Snowflake 寫入外部 Cloud Storage 階段中參照的 Amazon S3 值區。

   這個步驟包括[設定 Amazon S3 值區的存取權限](https://docs.snowflake.com/en/user-guide/data-load-s3-config.html#step-1-configure-access-permissions-for-the-s3-bucket)、[建立 Amazon Web Services (AWS) IAM 角色](https://docs.snowflake.com/en/user-guide/data-load-s3-config.html#step-2-create-the-iam-role-in-aws)，以及使用 `CREATE STORAGE INTEGRATION` 指令在 Snowflake 中建立儲存空間整合：

   ```
   create storage integration INTEGRATION_NAME
   type = external_stage
   storage_provider = s3
   enabled = true
   storage_aws_role_arn = 'arn:aws:iam::001234567890:role/myrole'
   storage_allowed_locations = ('BUCKET_NAME')
   ```

   更改下列內容：

   * `INTEGRATION_NAME`：儲存空間整合的名稱。例如：`s3_int`
   * `BUCKET_NAME`：要載入檔案的 Amazon S3 儲存空間路徑。例如：`s3://unload/files/`
2. 使用 [`DESCRIBE INTEGRATION`](https://docs.snowflake.com/en/sql-reference/sql/desc-integration.html) 指令[擷取 AWS IAM 使用者](https://docs.snowflake.com/en/user-guide/data-load-s3-config-storage-integration.html#step-4-retrieve-the-aws-iam-user-for-your-snowflake-account)。

   ```
   desc integration INTEGRATION_NAME;
   ```

   輸出結果會與下列內容相似：

   ```
   +---------------------------+---------------+================================================================================+------------------+
   | property                  | property_type | property_value                                                                 | property_default |
   +---------------------------+---------------+================================================================================+------------------|
   | ENABLED                   | Boolean       | true                                                                           | false            |
   | STORAGE_ALLOWED_LOCATIONS | List          | s3://mybucket1/mypath1/,s3://mybucket2/mypath2/                                | []               |
   | STORAGE_BLOCKED_LOCATIONS | List          | s3://mybucket1/mypath1/sensitivedata/,s3://mybucket2/mypath2/sensitivedata/    | []               |
   | STORAGE_AWS_IAM_USER_ARN  | String        | arn:aws:iam::123456789001:user/abc1-b-self1234                                 |                  |
   | STORAGE_AWS_ROLE_ARN      | String        | arn:aws:iam::001234567890:role/myrole                                          |                  |
   | STORAGE_AWS_EXTERNAL_ID   | String        | MYACCOUNT_SFCRole=                                                   |                  |
   +---------------------------+---------------+================================================================================+------------------+
   ```
3. 建立具備結構定義 `CREATE STAGE` 權限和儲存空間整合 `USAGE` 權限的角色：

   ```
       CREATE role ROLE_NAME;  
       GRANT CREATE STAGE ON SCHEMA public TO ROLE ROLE_NAME;
       GRANT USAGE ON INTEGRATION s3_int TO ROLE ROLE_NAME;
   ```

   將 `ROLE_NAME` 替換為角色的名稱。例如：`myrole`。
4. 授予 AWS IAM 使用者存取 Amazon S3 值區的權限，並使用 `CREATE STAGE` 指令[建立外部階段](https://docs.snowflake.com/en/user-guide/data-load-s3-create-stage)：

   ```
       USE SCHEMA mydb.public;

       create or replace stage STAGE_NAME
           url='BUCKET_NAME'
           storage_integration = INTEGRATION_NAMEt
           file_format = NAMED_FILE_FORMAT;
   ```

   更改下列內容：

   * `STAGE_NAME`：Cloud Storage 階段物件的名稱。
     例如：`my_ext_unload_stage`

### 匯出 Snowflake 資料

準備好資料後，即可將資料移至 Google Cloud。
使用 `COPY INTO` 指令，指定外部階段物件 `STAGE_NAME`，將資料從 Snowflake 資料庫資料表複製到 Cloud Storage 或 Amazon S3 值區。

```
    copy into @STAGE_NAME/d1
    from TABLE_NAME;
```

將 `TABLE_NAME` 替換為 Snowflake 資料庫資料表的名稱。

執行這項指令後，資料表資料會複製到與 Cloud Storage 或 Amazon S3 值區連結的暫存物件。檔案包含 `d1` 前置字串。

### 其他匯出方法

如要使用 Azure Blob 儲存體匯出資料，請按照「[卸載至 Microsoft Azure](https://docs.snowflake.com/en/user-guide/data-unload-azure.html)」一文中的詳細步驟操作。然後使用 [Storage 移轉服務](https://docs.cloud.google.com/storage-transfer/docs/create-manage-transfer-program?hl=zh-tw)，將匯出的檔案移轉至 Cloud Storage。

## 定價

規劃 Snowflake 遷移作業時，請考量在 BigQuery 中轉移資料、儲存資料及使用服務的成本。詳情請參閱「[定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw)」。

將資料移出 Snowflake 或 AWS 時，可能會產生輸出費用。跨區域移轉資料或跨不同雲端供應商移轉資料時，也可能產生額外費用。

## 後續步驟

* 遷移後[成效和最佳化](https://docs.cloud.google.com/bigquery/docs/admin-intro?hl=zh-tw#optimize_workloads) 。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-02-05 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-02-05 (世界標準時間)。"],[],[]]