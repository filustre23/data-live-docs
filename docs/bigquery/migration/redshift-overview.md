* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [參考資料](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 從 Amazon Redshift 遷移至 BigQuery：總覽

本文提供從 Amazon Redshift 遷移至 BigQuery 的指南，著重於下列主題：

* 遷移策略
* 查詢最佳化和資料模型化的最佳做法
* 疑難排解提示
* 使用者採用指南

本文件的目標如下：

* 為從 Amazon Redshift 遷移至 BigQuery 的機構提供高階指引，包括協助您重新思考現有的資料管道，充分發揮 BigQuery 的效益。
* 協助您比較 BigQuery 和 Amazon Redshift 的架構，以便在遷移期間決定如何實作現有功能。我們的目標是向您展示貴機構透過 BigQuery 取得的新功能，而不是將功能一對一對應至 Amazon Redshift。

本文適用於企業架構師、資料庫管理員、應用程式開發人員和 IT 安全專家。本文假設您已熟悉 Amazon Redshift。

您也可以使用[批次 SQL 翻譯](https://docs.cloud.google.com/bigquery/docs/batch-sql-translator?hl=zh-tw)大量遷移 SQL 指令碼，或使用[互動式 SQL 翻譯](https://docs.cloud.google.com/bigquery/docs/interactive-sql-translator?hl=zh-tw)翻譯臨時查詢。兩項 SQL 轉換服務都完整支援 Amazon Redshift SQL。

## 遷移前置工作

為確保資料倉儲遷移作業順利完成，請在專案時間軸的早期階段，就開始規劃遷移策略。這種做法可讓您評估適合自己需求的 Google Cloud 功能。

### 處理能力規劃

BigQuery 會使用「運算單元」來評估數據分析處理量。BigQuery 運算單元是 Google 專有的運算能力單位，用來執行 SQL 查詢。BigQuery 會在查詢執行時持續計算所需的運算單元數量，但會根據[公平調度器](https://docs.cloud.google.com/bigquery/docs/slots?hl=zh-tw#fair_scheduling_in_bigquery)將運算單元分配給查詢。

為 BigQuery 運算單元規劃容量時，您可以選擇下列計價模式：

* [以量計價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#on_demand_pricing)：
  在以量計價模式中，BigQuery 會按照處理的位元組數 (資料大小) 收取費用，因此您只需為執行的查詢付費。
  如要進一步瞭解 BigQuery 如何判斷資料量，請參閱「[資料量的計算方式](https://cloud.google.com/bigquery/pricing?hl=zh-tw#data)」。由於運算單元決定了基礎運算容量，因此您可以根據所需的運算單元數量支付 BigQuery 用量費用 (而非根據處理的位元組數)。根據預設，所有Google Cloud 專案的運算單元上限為 2,000 個。BigQuery 可能會透過爆發功能提供高於這項限制的運算單元數量，藉此加快查詢速度，但爆發功能不保證能提供額外運算單元。
* [以運算資源為基礎的計價模式](https://cloud.google.com/bigquery/pricing?hl=zh-tw#capacity_compute_analysis_pricing)：
  採用以運算資源為基礎的計價模式時，您會購買 BigQuery 運算單元[保留項目](https://docs.cloud.google.com/bigquery/docs/reservations-intro?hl=zh-tw) (最少 100 個)，而不必根據查詢處理的位元組數付費。對於企業資料倉儲工作負載，我們建議採用以容量計價模式，這類工作負載通常會同時執行許多報表和擷取、載入、轉換 (ELT) 查詢，且用量可預測。

為協助估算運算單元，建議您[使用 Cloud Monitoring 設定 BigQuery 監控](https://docs.cloud.google.com/bigquery/docs/monitoring?hl=zh-tw)，並[使用 BigQuery 分析稽核記錄](https://docs.cloud.google.com/bigquery/audit-logs?hl=zh-tw)。您可以使用 [Data Studio](https://lookerstudio.google.com/?hl=zh-tw) (這是 Data Studio 資訊主頁的[開放原始碼範例](https://github.com/GoogleCloudPlatform/professional-services/tree/master/examples/bigquery-audit-log)) 或 [Looker](https://looker.com/)，將 BigQuery 的稽核記錄資料視覺化，特別是查詢和專案的運算單元用量。您也可以使用 BigQuery 的系統資料表資料，監控工作和預留容量的時段用量 (這是[開放原始碼的數據分析資訊主頁範例](https://github.com/GoogleCloudPlatform/bigquery-utils/tree/master/dashboards/system_tables))。定期監控及分析使用配額，有助於預估貴機構在 Google Cloud成長時所需的總配額。

舉例來說，假設您一開始保留 4,000 個 BigQuery [運算單元](https://docs.cloud.google.com/bigquery/docs/slots?hl=zh-tw)，同時執行 100 個中等複雜度的查詢。如果您發現查詢的執行計畫等待時間過長，且資訊主頁顯示的運算單元使用率偏高，可能表示您需要額外的 BigQuery 運算單元，才能支援工作負載。如要透過一年或三年期承諾自行購買運算單元，請使用Google Cloud 主控台或 bq 指令列工具，[開始使用 BigQuery 預留量](https://docs.cloud.google.com/bigquery/docs/reservations-get-started?hl=zh-tw)。如要進一步瞭解工作負載管理、查詢執行和 BigQuery 架構，請參閱「[遷移至Google Cloud：深入瞭解](#migration-in-depth)」。

### Google Cloud的安全防護

以下各節說明常見的 Amazon Redshift 安全控管機制，以及如何確保資料倉儲在Google Cloud 環境中受到保護。

#### 身分與存取權管理

在 Amazon Redshift 中設定存取權控管機制時，需要編寫 Amazon Redshift API 權限政策，並將這些政策附加至 [Identity and Access Management (IAM)](https://docs.cloud.google.com/iam?hl=zh-tw) 身分。Amazon Redshift API 權限提供叢集層級的存取權，但無法提供比叢集更精細的存取層級。如要更精細地存取資料表或檢視等資源，可以使用 Amazon Redshift 資料庫中的使用者帳戶。

BigQuery 使用 IAM 管理資源存取權，精細程度更勝以往。BigQuery 提供的資源類型包括機構、專案、資料集、資料表、資料欄和檢視區塊。在 IAM 政策階層中，資料集是專案的子項資源。資料表會繼承所屬資料集的權限。

如要授予資源的存取權，請將一或多個 IAM 角色指派給使用者、群組或服務帳戶。機構和專案角色會影響執行工作或管理專案的能力，而資料集角色則會影響存取或修改專案內資料的能力。

IAM 提供下列類型的角色：

* [預先定義的角色](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)，可因應常見的用途和存取控管模式。
* [自訂角色](https://docs.cloud.google.com/iam/docs/understanding-custom-roles?hl=zh-tw)：根據使用者指定的權限清單，提供精細的存取權限。

在 IAM 中，BigQuery 提供[資料表層級的存取權控管](https://docs.cloud.google.com/bigquery/docs/control-access-to-resources-iam?hl=zh-tw)。資料表層級權限可以決定要允許哪些使用者、群組和服務帳戶存取資料表或檢視表。您可以授予使用者特定資料表或檢視區塊的存取權，而不必授予完整資料集的存取權。如要更精細地控管存取權，您也可以考慮實作下列一或多個安全機制：

* [資料欄層級存取控管](https://docs.cloud.google.com/bigquery/docs/column-level-security-intro?hl=zh-tw)：透過政策標記或依據類型的資料分類方式，對機密資料欄提供精細的存取權限。
* [資料欄層級的動態資料遮蓋](https://docs.cloud.google.com/bigquery/docs/column-data-masking-intro?hl=zh-tw)：可針對使用者群組選擇性地遮蓋資料欄資料，但這些使用者還是能正常使用該資料欄。
* [資料列層級安全防護機制](https://docs.cloud.google.com/bigquery/docs/row-level-security-intro?hl=zh-tw)：可根據符合資格的使用者條件篩選資料，並啟用資料表中特定資料列的存取權。

#### 全磁碟加密

除了身分與存取權管理，資料加密技術還可為資料提供進一步的安全保障，如果資料暴露，已加密資料也無法讀取。

在 Amazon Redshift 中，系統預設不會啟用靜態資料和傳輸中的資料的加密功能。啟動叢集時，必須[明確啟用](https://docs.aws.amazon.com/redshift/latest/mgmt/changing-cluster-encryption.html)靜態資料加密功能，或是修改現有叢集，改用 AWS Key Management Service 加密功能。您也必須[明確啟用](https://docs.aws.amazon.com/redshift/latest/mgmt/security-encryption-in-transit.html)傳輸中的資料加密功能。

無論來源或任何其他條件為何，BigQuery 預設都會加密所有[靜態](https://docs.cloud.google.com/docs/security/encryption/default-encryption?hl=zh-tw)和[傳輸中](https://docs.cloud.google.com/docs/security/encryption-in-transit?hl=zh-tw)的資料，且無法關閉這項功能。如果您想在 [Cloud Key Management Service](https://docs.cloud.google.com/kms/docs?hl=zh-tw) 中控管及管理金鑰加密金鑰，BigQuery 也支援[客戶管理的加密金鑰 (CMEK)](https://docs.cloud.google.com/bigquery/docs/customer-managed-encryption?hl=zh-tw)。

如要進一步瞭解 Google Cloud中的加密功能，請參閱[靜態資料加密](https://docs.cloud.google.com/docs/security/encryption/default-encryption?hl=zh-tw)和[傳輸中資料加密](https://docs.cloud.google.com/docs/security/encryption-in-transit?hl=zh-tw)白皮書。

對於[傳輸中的資料 Google Cloud](https://docs.cloud.google.com/docs/security/encryption-in-transit?hl=zh-tw)，當資料移出 [Google 控制或第三方代表 Google 控制的實體界線](https://docs.cloud.google.com/docs/security/encryption-in-transit?hl=zh-tw#physical_boundaries_of_a_network)外時，系統會加密及驗證資料。在這些界線內，傳輸中的資料通常會經過驗證，但不一定會加密。

#### 資料遺失防護

法規遵循規定可能會限制可儲存在Google Cloud的資料。您可以使用 [Sensitive Data Protection](https://docs.cloud.google.com/sensitive-data-protection/docs?hl=zh-tw) [掃描 BigQuery 資料表](https://docs.cloud.google.com/bigquery/docs/scan-with-dlp?hl=zh-tw)，偵測及分類機密資料。如果偵測到機密資料，Sensitive Data Protection 去識別化轉換可以[遮蓋、刪除或隱藏](https://docs.cloud.google.com/bigquery/docs/scan-with-dlp?hl=zh-tw)該資料。

## 遷移至 Google Cloud：基本概念

本節將說明如何使用工具和管道，協助您完成遷移作業。

### 遷移工具

BigQuery 資料移轉服務提供自動化工具，可直接將結構定義和資料從 Amazon Redshift 遷移至 BigQuery。下表列出其他工具，可協助您從 Amazon Redshift 遷移至 BigQuery：

| **工具** | **Purpose** |
| --- | --- |
| [BigQuery 資料移轉服務](https://docs.cloud.google.com/bigquery/docs/dts-introduction?hl=zh-tw) | 使用這項全代管服務，自動將 Amazon Redshift 資料批次移轉至 BigQuery。 |
| [Storage 移轉服務](https://docs.cloud.google.com/storage/transfer?hl=zh-tw) | 使用這項全代管服務，快速將 Amazon S3 資料匯入 Cloud Storage，並設定重複的資料移轉時間表。 |
| `gcloud` | 使用這個指令列工具，將 Amazon S3 檔案複製到 Cloud Storage。 |
| [bq 指令列工具](https://docs.cloud.google.com/bigquery/bq-command-line-tool?hl=zh-tw) | 使用這個指令列工具與 BigQuery 互動。常見的互動包括建立 BigQuery 資料表結構定義、將 Cloud Storage 資料載入資料表，以及執行查詢。 |
| [Cloud Storage 用戶端程式庫](https://docs.cloud.google.com/storage/docs/reference/libraries?hl=zh-tw) | 使用以 Cloud Storage 用戶端程式庫為基礎建構的自訂工具，將 Amazon S3 檔案複製到 Cloud Storage。 |
| [BigQuery 用戶端程式庫](https://docs.cloud.google.com/bigquery/docs/reference/libraries?hl=zh-tw) | 使用以 BigQuery 用戶端程式庫為基礎建構的自訂工具，與 BigQuery 互動。 |
| [BigQuery 查詢排程器](https://docs.cloud.google.com/bigquery/docs/scheduling-queries?hl=zh-tw) | 使用這項 BigQuery 內建功能，排定週期性 SQL 查詢。 |
| [Managed Service for Apache Airflow](https://docs.cloud.google.com/composer?hl=zh-tw) | 使用這個全代管的 Apache Airflow 環境，調度轉換作業和 BigQuery 載入工作。 |
| [Apache Sqoop](https://sqoop.apache.org/) | 使用 Sqoop 和 Amazon Redshift 的 JDBC 驅動程式提交 Hadoop 工作，將資料從 Amazon Redshift 擷取至 HDFS 或 Cloud Storage。Sqoop 會在 Managed Service for Apache Spark 環境中執行。 |

如要進一步瞭解如何使用 BigQuery 資料移轉服務，請參閱「[從 Amazon Redshift 遷移結構定義和資料](https://docs.cloud.google.com/bigquery/docs/migration/redshift?hl=zh-tw)」。

### 使用管道進行遷移

從 Amazon Redshift 遷移至 BigQuery 的資料遷移作業，可根據可用的遷移工具採取不同路徑。本節列出的模式並非完整清單，但可讓您瞭解遷移資料時可用的各種資料管道模式。

如要進一步瞭解如何使用管道將資料遷移至 BigQuery，請參閱「[遷移資料管道](https://docs.cloud.google.com/bigquery/docs/migration/pipelines?hl=zh-tw)」。

#### 擷取及載入 (EL)

您可以使用 BigQuery 資料移轉服務，全面自動化 EL 管道，該服務可自動將資料表結構定義和資料從 Amazon Redshift 叢集複製到 BigQuery。如要進一步控管資料管道步驟，請使用下列各節所述的選項建立管道。

##### 使用 Amazon Redshift 檔案擷取內容

1. [將 Amazon Redshift 資料匯出至 Amazon S3](https://docs.aws.amazon.com/redshift/latest/dg/t_Unloading_tables.html)。
2. 使用下列任一選項，將資料從 Amazon S3 複製到 Cloud Storage：

   * [Storage 移轉服務](https://docs.cloud.google.com/storage/transfer?hl=zh-tw) (建議)
   * [gcloud CLI](https://docs.cloud.google.com/sdk/gcloud/reference/storage?hl=zh-tw)
   * [Cloud Storage 用戶端程式庫](https://docs.cloud.google.com/storage/docs/reference/libraries?hl=zh-tw)
3. 使用下列任一選項，將 Cloud Storage 資料載入 BigQuery：

   * [BigQuery 資料移轉服務](https://docs.cloud.google.com/bigquery/docs/cloud-storage-transfer-overview?hl=zh-tw)
   * [bq 指令列工具](https://docs.cloud.google.com/bigquery/bq-command-line-tool?hl=zh-tw)
   * [BigQuery 用戶端程式庫](https://docs.cloud.google.com/bigquery/docs/reference/libraries?hl=zh-tw)

##### 使用 Amazon Redshift JDBC 連線

使用下列任一 Google Cloud 產品，透過 [Amazon Redshift JDBC 驅動程式](https://docs.aws.amazon.com/redshift/latest/mgmt/configure-jdbc-connection.html#download-jdbc-driver)匯出 Amazon Redshift 資料：

* [Dataflow](https://docs.cloud.google.com/dataflow/docs?hl=zh-tw)

  + Google 提供的範本：
    [JDBC 到 BigQuery](https://docs.cloud.google.com/dataflow/docs/guides/templates/provided-batch?hl=zh-tw#java-database-connectivity-jdbc-to-bigquery)
* [Cloud Data Fusion](https://docs.cloud.google.com/data-fusion/docs?hl=zh-tw)

  + [使用 JDBC 驅動程式](https://docs.cloud.google.com/data-fusion/docs/how-to/using-jdbc-drivers?hl=zh-tw)
* [Managed Service for Apache Spark](https://docs.cloud.google.com/dataproc/docs?hl=zh-tw)

  + [透過 JDBC 和 Apache Spark 連線至 Amazon Redshift](https://docs.databricks.com/spark/latest/data-sources/aws/amazon-redshift.html)

    - [Apache Spark 範例](https://spark.apache.org/docs/latest/sql-data-sources-jdbc.html)
  + [使用 Apache Spark 寫入 BigQuery](https://docs.cloud.google.com/dataproc/docs/tutorials/bigquery-connector-spark-example?hl=zh-tw#reading_and_writing_data_from_bigquery)
  + [Hadoop BigQuery 連接器](https://docs.cloud.google.com/dataproc/docs/concepts/connectors/bigquery?hl=zh-tw)
  + 使用 Sqoop 和 [Amazon Redshift JDBC 驅動程式](https://docs.aws.amazon.com/redshift/latest/mgmt/configure-jdbc-connection.html#download-jdbc-driver)，將資料從 Amazon Redshift 擷取到 Cloud Storage

    - [Managed Service for Apache Spark 上的 Sqoop 範例](https://medium.com/google-cloud/moving-data-with-apache-sqoop-in-google-cloud-dataproc-4056b8fa2600)

#### 擷取、轉換及載入 (ETL)

如要在將資料載入 BigQuery 前進行轉換，請按照「[擷取和載入 (EL)](#extract_and_load_el)」一節所述的管道建議操作，並新增一個步驟，在載入 BigQuery 前轉換資料。

##### 使用 Amazon Redshift 檔案擷取內容

1. [將 Amazon Redshift 資料匯出至 Amazon S3](https://docs.aws.amazon.com/redshift/latest/dg/t_Unloading_tables.html)。
2. 使用下列任一選項，將資料從 Amazon S3 複製到 Cloud Storage：

   * [Storage 移轉服務](https://docs.cloud.google.com/storage/transfer?hl=zh-tw) (建議)
   * [gcloud CLI](https://docs.cloud.google.com/sdk/gcloud/reference/storage?hl=zh-tw)
   * [Cloud Storage 用戶端程式庫](https://docs.cloud.google.com/storage/docs/reference/libraries?hl=zh-tw)
3. 使用下列任一方法轉換資料，然後載入 BigQuery：

   * [Managed Service for Apache Spark](https://docs.cloud.google.com/dataproc/docs?hl=zh-tw)

     + [使用 Apache Spark 從 Cloud Storage 讀取資料](https://docs.cloud.google.com/dataproc/docs/tutorials/gcs-connector-spark-tutorial?hl=zh-tw#prepare_the_spark_wordcount_job)
     + [使用 Apache Spark 寫入 BigQuery](https://docs.cloud.google.com/dataproc/docs/tutorials/bigquery-connector-spark-example?hl=zh-tw#reading_and_writing_data_from_bigquery)
     + [Hadoop Cloud Storage 連接器](https://docs.cloud.google.com/dataproc/docs/concepts/connectors/cloud-storage?hl=zh-tw)
     + [Hadoop BigQuery 連接器](https://docs.cloud.google.com/dataproc/docs/concepts/connectors/bigquery?hl=zh-tw)
   * [Dataflow](https://docs.cloud.google.com/dataflow/docs?hl=zh-tw)

     + [從 Cloud Storage 讀取](https://beam.apache.org/documentation/programming-guide/#pipeline-io-reading-data)
     + [寫入 BigQuery](https://beam.apache.org/documentation/io/built-in/google-bigquery/#writing-to-a-table)
     + Google 提供的範本：
       [Cloud Storage Text 到 BigQuery](https://docs.cloud.google.com/dataflow/docs/guides/templates/provided-batch?hl=zh-tw#gcstexttobigquery)
   * [Cloud Data Fusion](https://docs.cloud.google.com/data-fusion/docs?hl=zh-tw)

     + [從 Cloud Storage 讀取](https://docs.cloud.google.com/data-fusion/docs/tutorials/targeting-campaign-pipeline?hl=zh-tw#load_the_customer_data)
     + [寫入 BigQuery](https://docs.cloud.google.com/data-fusion/docs/tutorials/targeting-campaign-pipeline?hl=zh-tw#store_the_output_to)
   * [Dataprep by Trifacta](https://docs.trifacta.com/Dataprep/en/product-overview.html)

     + [從 Cloud Storage 讀取](https://docs.trifacta.com/Dataprep/en/platform/connections/connection-types/google-cloud-storage-access.html)
     + [寫入 BigQuery](https://docs.trifacta.com/Dataprep/en/platform/connections/connection-types/bigquery-connections.html)

##### 使用 Amazon Redshift JDBC 連線

使用「擷取和載入 (EL)」一節中說明的任何產品，並新增額外步驟，在載入至 BigQuery 之前轉換資料。修改管道，導入一或多個步驟，在將資料寫入 BigQuery 前先轉換資料。

* [Dataflow](https://docs.cloud.google.com/dataflow/docs?hl=zh-tw)

  + 複製 [JDBC 到 BigQuery](https://docs.cloud.google.com/dataflow/docs/guides/templates/provided-batch?hl=zh-tw#java-database-connectivity-jdbc-to-bigquery) 範本程式碼，並修改範本以新增 [Apache Beam 轉換](https://beam.apache.org/documentation/programming-guide/#transforms)。
* [Cloud Data Fusion](https://docs.cloud.google.com/data-fusion/docs?hl=zh-tw)

  + 使用任何 [CDAP 外掛程式](https://cdap.io/resources/plugins/)轉換資料。
* [Managed Service for Apache Spark](https://docs.cloud.google.com/dataproc/docs?hl=zh-tw)

  + 使用 [Spark SQL](https://spark.apache.org/docs/latest/sql-programming-guide.html) 或以任何支援的 Spark 語言 ([Scala](https://spark.apache.org/docs/latest/api/scala/index.html#org.apache.spark.package)、[Java](https://spark.apache.org/docs/latest/api/java/index.html)、[Python](https://spark.apache.org/docs/latest/api/python/index.html) 或 [R](https://spark.apache.org/docs/latest/api/R/index.html)) 編寫的自訂程式碼轉換資料。

#### 擷取、載入及轉換 (ELT)

您可以使用 BigQuery 本身轉換資料，也可以使用任何「擷取和載入 (EL)」選項，將資料載入暫存資料表。接著，使用 SQL 查詢轉換這個暫存資料表中的資料，並將輸出內容寫入最終的正式環境資料表。

#### 變更資料擷取 (CDC)

[變更資料擷取](https://wikipedia.org/wiki/Change_data_capture)
是用來追蹤資料變更的其中一個軟體設計模式，通常用於資料倉儲系統，這是因為資料倉儲系統是用來整理資料，並追蹤不同來源系統隨著時間經過而產生的資料變更。

### 資料遷移合作夥伴工具

擷取、轉換及載入 (ETL) 領域有多家供應商。如需主要合作夥伴及其提供的解決方案清單，請參閱 [BigQuery 合作夥伴網站](https://docs.cloud.google.com/bigquery/docs/bigquery-ready-partners?hl=zh-tw)。

## 遷移至 Google Cloud：深入瞭解

請參閱本節，進一步瞭解資料倉儲架構、結構定義和 SQL 方言對遷移作業的影響。

### 架構比較

BigQuery 和 Amazon Redshift 都是以大規模平行處理 (MPP) 架構為基礎。查詢會分散到多個伺服器，以加快執行速度。就系統架構而言，Amazon Redshift 和 BigQuery 的主要差異在於資料的儲存方式和查詢的執行方式。在 BigQuery 中，底層硬體和設定會經過抽象化處理；儲存空間和運算資源可讓資料倉儲成長，不需要您介入。

#### 運算、記憶體和儲存空間

在 Amazon Redshift 中，CPU、記憶體和磁碟儲存空間會透過[運算節點](https://docs.aws.amazon.com/redshift/latest/dg/c_high_level_system_architecture.html)連結在一起，如 [Amazon Redshift 說明文件中的這張圖](https://docs.aws.amazon.com/redshift/latest/dg/c_high_level_system_architecture.html)所示。叢集效能和儲存空間容量取決於運算節點的類型和數量，這兩者都必須設定。如要變更運算或儲存空間，您必須透過程序調整叢集大小 ([幾小時內，或最多兩天以上](https://docs.aws.amazon.com/redshift/latest/mgmt/managing-cluster-operations.html))，建立全新叢集並複製資料。Amazon Redshift 也提供具備代管儲存空間的 RA3 節點，可協助您分離運算和儲存空間。RA3 類別中最大的節點，每個節點的受管理儲存空間上限為 64 TB。

BigQuery 從一開始就將運算、記憶體和儲存空間分開處理，而非綁在一起。

BigQuery 運算資源是以[運算單元](https://docs.cloud.google.com/bigquery/docs/slots?hl=zh-tw)為單位，這是執行查詢所需的運算能力單位。Google 會管理封裝插槽的整個基礎架構，因此您只需要為 BigQuery 工作負載選擇適當的插槽數量。請參閱[容量規劃](#capacity_planning)，協助決定資料倉儲要購買多少個時段。BigQuery 記憶體是由[遠端分散式服務](https://cloud.google.com/blog/products/gcp/in-memory-query-execution-in-google-bigquery?hl=zh-tw)提供，並透過 Google 的 Petabit 網路連線至運算單元，所有作業都由 Google 管理。

BigQuery 和 Amazon Redshift 都使用欄式儲存空間，但 BigQuery 使用的欄式儲存空間[變化和進展](https://cloud.google.com/blog/products/gcp/inside-capacitor-bigquerys-next-generation-columnar-storage-format?hl=zh-tw)。在編碼資料欄時，系統會保存各種資料統計資料，並在稍後查詢執行期間使用這些資料，編譯最佳計畫及選擇最有效率的執行階段演算法。BigQuery 會將資料儲存在 [Google 的分散式檔案系統](https://cloud.google.com/files/storage_architecture_and_challenges.pdf?hl=zh-tw)中，並自動壓縮、加密、複製及散布資料。而且完全不會影響查詢可用的運算能力。將儲存空間與運算資源分開，可讓您順暢擴充儲存空間，最多可達數十 PB，且不需要額外的高價運算資源。此外，運算與儲存空間分離還有許多其他[優點](https://cloud.google.com/blog/products/gcp/separation-of-compute-and-state-in-google-bigquery-and-cloud-dataflow-and-why-it-matters?hl=zh-tw)。

#### 向上或向下擴充

儲存空間或運算資源受限時，您必須修改叢集中的節點數量或類型，才能調整 Amazon Redshift 叢集的大小。

[調整 Amazon Redshift 叢集大小](https://docs.aws.amazon.com/redshift/latest/mgmt/managing-cluster-operations.html)時，有兩種做法：

* **傳統調整大小**：Amazon Redshift 會建立叢集並複製資料，如果資料量很大，這個程序可能需要幾小時，甚至兩天以上的時間。
* **彈性調整大小**：如果只變更節點數量，系統會暫時停止查詢，並盡可能保持連線開啟。在調整大小作業期間，叢集處於唯讀狀態。彈性調整大小通常需要 10 到 15 分鐘，但可能不適用於所有設定。

由於 BigQuery 是平台即服務 (PaaS)，您只需考慮要為貴機構預留多少 BigQuery 運算單元。您可以在保留項目中預留 BigQuery 運算單元，然後將專案指派給這些保留項目。如要瞭解如何設定這些預留項目，請參閱「[容量規劃](#capacity_planning)」。

#### 查詢執行

BigQuery 的執行引擎與 Amazon Redshift 類似，都會將查詢分解為多個步驟 (查詢計畫)，然後執行這些步驟 (盡可能並行執行)，最後重新組合結果。Amazon Redshift 會產生靜態查詢計畫，但 BigQuery 不會，因為 BigQuery 會在查詢執行時動態最佳化查詢計畫。BigQuery 會使用遠端記憶體服務重組資料，而 Amazon Redshift 則會使用本機運算節點記憶體重組資料。如要進一步瞭解 BigQuery 如何儲存查詢計畫各階段的中繼資料，請參閱「[Google BigQuery 中的記憶體內查詢執行](https://cloud.google.com/blog/products/gcp/in-memory-query-execution-in-google-bigquery?hl=zh-tw)」。

#### BigQuery 中的工作負載管理

BigQuery 提供下列工作負載管理 (WLM) 控制項：

* [互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)：盡快執行查詢 (預設設定)。
* [批次查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#batch)：系統會代表您將查詢排入佇列，等到 BigQuery 共用資源集區中出現閒置資源，就會開始進行查詢。
* 透過[以容量為準的定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#capacity_compute_analysis_pricing)[預留運算單元](https://docs.cloud.google.com/bigquery/docs/reservations-intro?hl=zh-tw)。您不必為查詢支付隨需費用，而是可以[動態建立及管理](https://docs.cloud.google.com/bigquery/docs/reservations-tasks?hl=zh-tw#create_a_reservation_with_dedicated_slots)運算單元儲存區 (稱為[預留項目](https://docs.cloud.google.com/bigquery/docs/reservations-intro?hl=zh-tw#reservations))，並[指派](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#assignments)專案、資料夾或機構給這些預留項目。您可以購買 BigQuery [運算單元使用承諾](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw#slot_commitments) (最少 100 個)，並選擇彈性、月約或年約，盡量降低成本。根據預設，在預留項目中執行的查詢會自動使用其他預留項目中閒置的[運算單元](https://docs.cloud.google.com/bigquery/docs/slots?hl=zh-tw#idle_slots)。

  如下圖所示，假設您購買了 1,000 個運算單元的承諾使用容量總計，並在三種工作負載類型之間共用：資料科學、ELT 和商業智慧 (BI)。如要支援這些工作負載，您可以建立下列預訂：

  + 您可以建立具有 500 個運算單元的 **ds** 保留項目，並將所有Google Cloud 資料科學專案指派給該保留項目。
  + 您可以建立具有 300 個運算單元的 **elt** 保留項目，並將用於 ELT 工作負載的專案指派給該保留項目。
  + 您可以建立具有 200 個運算單元的 **bi** 保留項目，並將連結至 BI 工具的專案指派給該保留項目。

  這項設定如下圖所示：

  您可以選擇將預訂項目指派給個別團隊或部門，而不是將預訂項目分配給貴機構的工作負載 (例如生產和測試)，具體取決於您的用途。

  詳情請參閱[使用預留項目進行工作負載管理](https://docs.cloud.google.com/bigquery/docs/reservations-intro?hl=zh-tw)。

#### Amazon Redshift 中的工作負載管理

Amazon Redshift 提供兩種工作負載管理 (WLM) 方式：

* [自動](https://docs.aws.amazon.com/redshift/latest/dg/automatic-wlm.html)：
  使用自動 WLM 時，Amazon Redshift 會管理查詢並行和記憶體分配。最多可使用服務類別 ID 100 至 107 建立八個佇列。自動 WLM 會判斷查詢所需的資源量，並根據工作負載調整並行數量。詳情請參閱「[查詢優先順序](https://docs.aws.amazon.com/redshift/latest/dg/query-priority.html)」。
* [手動](https://docs.aws.amazon.com/redshift/latest/dg/cm-c-defining-query-queues.html)：
  相較之下，手動 WLM 需要您指定查詢並行和記憶體配置的值。手動 WLM 的預設值是五個查詢的並行，記憶體會平均分配給這五個查詢。

啟用[並行擴充](https://docs.aws.amazon.com/redshift/latest/dg/concurrency-scaling.html)功能後，Amazon Redshift 會在您需要處理增加的並行讀取查詢時，自動新增額外的叢集容量。並行擴充功能有特定的區域和查詢考量。詳情請參閱「[並行調度候選項目](https://docs.aws.amazon.com/redshift/latest/dg/concurrency-scaling.html)」。

### 資料集和資料表設定

BigQuery 提供多種方式來設定資料和資料表，例如分區、叢集和資料本地性。這些設定有助於維護大型資料表，並減少查詢的整體資料負載和回應時間，進而提高資料工作負載的運作效率。

#### 分區

分區資料表會劃分為多個區段 (稱為分區)，管理和查詢資料時更加方便。使用者通常會將大型資料表分成許多較小的分區，每個分區包含一天的資料。查詢特定日期範圍時，分區管理是決定 BigQuery 效能和費用的主要因素，因為這有助於 BigQuery 減少每次查詢掃描的資料量。

BigQuery 中的資料表分區有三種類型：

* [依擷取時間分區的資料表](https://docs.cloud.google.com/bigquery/docs/creating-partitioned-tables?hl=zh-tw)：根據資料擷取時間分區的資料表。
* [依資料欄分區的資料表](https://docs.cloud.google.com/bigquery/docs/partitioned-tables?hl=zh-tw#date_timestamp_partitioned_tables)：根據 `TIMESTAMP` 或 `DATE` 資料欄分區的資料表。
* [依整數範圍分區的資料表](https://docs.cloud.google.com/bigquery/docs/creating-integer-range-partitions?hl=zh-tw)：根據整數資料欄分區的資料表。

以資料欄為基礎的時間分區資料表，可免除維護分區意識的需求，且與繫結資料欄的現有資料篩選作業無關。系統會根據資料值，將寫入以資料欄為基礎的時間分區資料表的資料，自動傳送到適當的分區。同樣地，對分區資料欄表示篩選器的查詢可以減少掃描的整體資料量，進而提升效能，並降低隨選查詢的查詢費用。

BigQuery 的資料欄分區與 Amazon Redshift 的資料欄分區類似，但動機略有不同。Amazon Redshift 會使用以資料欄為準的索引鍵分配方式，盡量將相關資料儲存在同一個運算節點中，最終盡量減少聯結和匯總期間發生的資料重組。BigQuery 會分開處理儲存和運算作業，因此會利用以資料欄為準的分區功能，盡量減少[運算單元](https://docs.cloud.google.com/bigquery/docs/slots?hl=zh-tw)從磁碟讀取的資料量。

當運算單元從磁碟讀取資料後，BigQuery 就能自動判斷更合適的資料 sharding，並使用 BigQuery 的記憶體內重組服務快速重新分割資料。

詳情請參閱[分區資料表簡介](https://docs.cloud.google.com/bigquery/docs/partitioned-tables?hl=zh-tw)一文。

#### 叢集和排序鍵

Amazon Redshift 支援將資料表欄指定為[複合](https://docs.aws.amazon.com/redshift/latest/dg/t_Sorting_data.html#t_Sorting_data-compound)或[交錯](https://docs.aws.amazon.com/redshift/latest/dg/t_Sorting_data.html#t_Sorting_data-interleaved)排序鍵。在 BigQuery 中，您可以透過[叢集](https://docs.cloud.google.com/bigquery/docs/clustered-tables?hl=zh-tw)資料表，指定複合排序鍵。BigQuery 叢集資料表會根據資料表結構定義中最多四個資料欄的內容自動排序資料，因此能提升查詢效能。系統會按照您指定的資料欄，將相關資料歸入同一個位置。您指定的分群資料欄順序非常重要，因為這會決定資料的排序方式。

叢集處理可以提升某幾種查詢的效能，例如使用篩選子句的查詢，以及匯總資料的查詢。當查詢工作或載入工作將資料寫入分群資料表時，BigQuery 會使用分群資料欄裡的值自動排序資料。將資料分到 BigQuery 儲存空間中的多個區塊。當提交的查詢含有根據叢集化資料欄篩選資料的子句時，BigQuery 會使用排序過的區塊，不會掃描不需要的資料。

同樣地，當您所提交的查詢會根據叢集處理資料欄中的值匯總資料時，由於排序過的區塊會將含有相似值的資料列並置於相同位置，所以效能也會提升。

在下列情況下使用分群：

* 複合排序鍵是在 Amazon Redshift 資料表中設定。
* 您會在查詢中，對特定資料欄設定篩選或匯總。

同時使用叢集和分區處理時，可依據日期、時間戳記或整數資料欄將資料分區，然後依據另一組資料欄進行叢集處理 (最多四個叢集資料欄)。在此情況下，各分區中的資料是根據分群資料欄的值來分群。

在 Amazon Redshift 的資料表中指定排序鍵時，Amazon Redshift 會根據系統負載，使用您自己的叢集運算容量自動啟動排序作業。如果您想盡快完整排序資料表資料 (例如在載入大量資料後)，甚至可能需要手動執行 [`VACUUM`](https://docs.aws.amazon.com/redshift/latest/dg/r_VACUUM_command.html) 指令。BigQuery 會[自動處理](https://docs.cloud.google.com/bigquery/docs/clustered-tables?hl=zh-tw#automatic_reclustering)這項排序作業，且不會使用您分配的 BigQuery 運算單元，因此不會影響任何查詢的效能。

如要進一步瞭解如何使用叢集資料表，請參閱「[叢集資料表簡介](https://docs.cloud.google.com/bigquery/docs/clustered-tables?hl=zh-tw)」。

#### 發布金鑰

Amazon Redshift 會使用分布索引鍵，最佳化資料區塊的位置，以執行查詢。BigQuery 不會使用分配鍵，因為系統會在查詢執行期間，自動判斷並新增查詢計畫中的階段，以改善資料在所有查詢工作站之間的分布狀況。

#### 外部來源

如果您使用 [Amazon Redshift Spectrum](https://docs.aws.amazon.com/redshift/latest/dg/c-using-spectrum.html) 查詢 Amazon S3 上的資料，也可以使用 BigQuery 的外部資料來源功能，[直接查詢 Cloud Storage 檔案中的資料](https://docs.cloud.google.com/bigquery/external-data-cloud-storage?hl=zh-tw)。

除了查詢 Cloud Storage 中的資料，BigQuery 也提供[聯合查詢函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/federated_query_functions?hl=zh-tw)，可[直接查詢](https://docs.cloud.google.com/bigquery/external-data-sources?hl=zh-tw)下列產品中的資料：

* [Cloud SQL](https://docs.cloud.google.com/bigquery/docs/cloud-sql-federated-queries?hl=zh-tw)
  (全代管 MySQL 或 PostgreSQL)
* [Bigtable](https://docs.cloud.google.com/bigquery/external-data-bigtable?hl=zh-tw)
  (全代管 NoSQL)
* [Google 雲端硬碟](https://docs.cloud.google.com/bigquery/external-data-drive?hl=zh-tw)
  (CSV、JSON、Avro、試算表)

#### 資料位置

您可以在地區和多地區位置建立 BigQuery 資料集，但 Amazon Redshift 僅提供地區位置。BigQuery 會根據要求中參考的資料集，決定載入、查詢或擷取工作的執行位置。如需處理地區和多地區資料集的訣竅，請參閱 BigQuery 位置注意事項。

### BigQuery 中的資料類型對應

Amazon Redshift 資料類型與 BigQuery 資料類型不同。如要進一步瞭解 BigQuery 資料類型，請參閱[官方說明文件](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw)。

BigQuery 也支援下列資料類型，這些類型沒有直接對應的 Amazon Redshift 類似項目：

* [`ARRAY`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#array_type)
* [`BYTES`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#bytes_type)
* [`GEOGRAPHY`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#geography_type)
* [`TIME`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#time_type)
* [`STRUCT`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#struct_type)

### SQL 比較

[GoogleSQL](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql?hl=zh-tw)
支援 SQL 2011 標準，並具備查詢巢狀和重複資料的擴充功能。Amazon Redshift SQL 是以 PostgreSQL 為基礎，但有幾項差異，詳情請參閱 [Amazon Redshift 說明文件](https://docs.aws.amazon.com/redshift/latest/dg/c_redshift-and-postgres-sql.html)。如要詳細比較 Amazon Redshift 和 GoogleSQL 的語法和函式，請參閱 [Amazon Redshift SQL 轉換指南](https://docs.cloud.google.com/bigquery/docs/migration/redshift-sql?hl=zh-tw)。

您可以使用[批次 SQL 翻譯器](https://docs.cloud.google.com/bigquery/docs/batch-sql-translator?hl=zh-tw)，將目前平台中的指令碼和其他 SQL 程式碼轉換為 BigQuery 格式。

## 遷移後

由於您遷移的指令碼並非專為 BigQuery 設計，因此可以選擇實作相關技術，以最佳化 BigQuery 查詢效能。詳情請參閱「[最佳化查詢效能簡介](https://docs.cloud.google.com/bigquery/docs/best-practices-performance-overview?hl=zh-tw)」。

## 後續步驟

* 取得[從 Amazon Redshift 遷移結構定義和資料](https://docs.cloud.google.com/bigquery/docs/migration/redshift?hl=zh-tw)的逐步操作說明。
* 取得[使用虛擬私有雲端執行 Amazon Redshift 遷移至 BigQuery](https://docs.cloud.google.com/bigquery/docs/migration/redshift-vpc?hl=zh-tw) 的逐步操作說明。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-02 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-02 (世界標準時間)。"],[],[]]