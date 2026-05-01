* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 在 BigQuery Studio 筆記本中執行 PySpark 程式碼

本文說明如何在 BigQuery Python 筆記本中執行 PySpark 程式碼。

## 事前準備

請建立 Google Cloud 專案和 Cloud Storage [bucket](https://docs.cloud.google.com/storage/docs/xml-api/put-bucket-create?hl=zh-tw)。

1. **設定專案**

   - 登入 Google Cloud 帳戶。如果您是 Google Cloud新手，歡迎[建立帳戶](https://console.cloud.google.com/freetrial?hl=zh-tw)，親自評估產品在實際工作環境中的成效。新客戶還能獲得價值 $300 美元的免費抵免額，可用於執行、測試及部署工作負載。
   - In the Google Cloud console, on the project selector page,
     select or create a Google Cloud project.

     **Roles required to select or create a project**

     * **Select a project**: Selecting a project doesn't require a specific
       IAM role—you can select any project that you've been
       granted a role on.
     * **Create a project**: To create a project, you need the Project Creator role
       (`roles/resourcemanager.projectCreator`), which contains the
       `resourcemanager.projects.create` permission. [Learn how to grant
       roles](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw).
     **Note**: If you don't plan to keep the
     resources that you create in this procedure, create a project instead of
     selecting an existing project. After you finish these steps, you can
     delete the project, removing all resources associated with the project.

     [Go to project selector](https://console.cloud.google.com/projectselector2/home/dashboard?hl=zh-tw)
   - Enable the Managed Service for Apache Spark, BigQuery, and Cloud Storage APIs.

     **Roles required to enable APIs**

     To enable APIs, you need the Service Usage Admin IAM
     role (`roles/serviceusage.serviceUsageAdmin`), which
     contains the `serviceusage.services.enable` permission. [Learn how to grant
     roles](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw).

     [Enable the APIs](https://console.cloud.google.com/flows/enableapi?apiid=dataproc.googleapis.com%2Cbigquery.googleapis.com%2Cstorage-component.googleapis.com&hl=zh-tw)

   - In the Google Cloud console, on the project selector page,
     select or create a Google Cloud project.

     **Roles required to select or create a project**

     * **Select a project**: Selecting a project doesn't require a specific
       IAM role—you can select any project that you've been
       granted a role on.
     * **Create a project**: To create a project, you need the Project Creator role
       (`roles/resourcemanager.projectCreator`), which contains the
       `resourcemanager.projects.create` permission. [Learn how to grant
       roles](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw).
     **Note**: If you don't plan to keep the
     resources that you create in this procedure, create a project instead of
     selecting an existing project. After you finish these steps, you can
     delete the project, removing all resources associated with the project.

     [Go to project selector](https://console.cloud.google.com/projectselector2/home/dashboard?hl=zh-tw)
   - Enable the Managed Service for Apache Spark, BigQuery, and Cloud Storage APIs.

     **Roles required to enable APIs**

     To enable APIs, you need the Service Usage Admin IAM
     role (`roles/serviceusage.serviceUsageAdmin`), which
     contains the `serviceusage.services.enable` permission. [Learn how to grant
     roles](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw).

     [Enable the APIs](https://console.cloud.google.com/flows/enableapi?apiid=dataproc.googleapis.com%2Cbigquery.googleapis.com%2Cstorage-component.googleapis.com&hl=zh-tw)
2. 如果沒有可用的 Cloud Storage 值區，請在專案中**[建立一個](https://docs.cloud.google.com/storage/docs/creating-buckets?hl=zh-tw)**。
3. **設定筆記本**

   * 筆記本憑證：根據預設，筆記本工作階段會使用您的[使用者憑證](https://docs.cloud.google.com/docs/authentication?hl=zh-tw#user-accounts)。或者，也可以使用[工作階段服務帳戶](https://docs.cloud.google.com/docs/authentication?hl=zh-tw#service-accounts)憑證。
     + 使用者憑證：您的使用者帳戶必須具備下列 Identity and Access Management 角色：
       - [Managed Service for Apache Spark 編輯者 (`roles/dataproc.editor` 角色)](https://docs.cloud.google.com/iam/docs/roles-permissions/dataproc?hl=zh-tw#dataproc.editor)
       - [BigQuery Studio 使用者 (`roles/bigquery.studioUser` 角色)](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.studioUser)
       - [工作階段服務帳戶的服務帳戶使用者 (roles/iam.serviceAccountUser) 角色](https://docs.cloud.google.com/iam/docs/service-account-permissions?hl=zh-tw#user-role)。這個角色包含模擬服務帳戶所需的 `iam.serviceAccounts.actAs` 權限。
     + 服務帳戶憑證：如要為筆記本工作階段指定服務帳戶憑證，而非使用者憑證，[工作階段服務帳戶](https://docs.cloud.google.com/dataproc-serverless/docs/concepts/service-account?hl=zh-tw)必須具備下列角色：
       - [Dataproc Worker (`roles/dataproc.worker` 角色)](https://docs.cloud.google.com/iam/docs/roles-permissions/dataproc?hl=zh-tw#dataproc.worker)
   * 筆記本執行階段：除非您選取其他執行階段，否則筆記本會使用預設的 Vertex AI 執行階段。如要定義自己的執行階段，請在 Google Cloud 控制台的「執行階段」[頁面](https://console.cloud.google.com/vertex-ai/colab/runtimes?hl=zh-tw)建立執行階段。**注意**，使用 [NumPy 程式庫](https://numpy.org/)時，請在筆記本執行階段使用 Spark 3.5 支援的 NumPy 1.26 版。

## 定價

如需價格資訊，請參閱 BigQuery [Notebook 執行階段價格](https://cloud.google.com/bigquery/pricing?hl=zh-tw#external_services)。

## 開啟 BigQuery Studio Python 筆記本

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在詳細資料窗格的分頁列中，按一下「+」符號旁的箭頭，然後按一下「記事本」。arrow\_drop\_down

## 在 BigQuery Studio 筆記本中建立 Spark 工作階段

您可以使用 BigQuery Studio Python 筆記本建立 [Spark Connect](https://spark.apache.org/docs/latest/spark-connect-overview.html) 互動式工作階段。每個 BigQuery Studio 筆記本只能有一個相關聯的有效 Spark 工作階段。

您可以在 BigQuery Studio Python 筆記本中，透過下列方式建立 Spark 工作階段：

* 在筆記本中設定及建立單一工作階段。
* 在[**互動式工作階段範本**](https://docs.cloud.google.com/dataproc-serverless/docs/guides/create-serverless-sessions-templates?hl=zh-tw#create-dataproc-serverless-session-template)中設定 Spark 工作階段，然後使用範本在 Notebook 中設定及建立工作階段。BigQuery 提供 `Query using Spark` 功能，可協助您開始編寫範本化工作階段的程式碼，如「範本化 Spark 工作階段」分頁標籤所述。

### 單次

如要在新筆記本中建立 Spark 工作階段，請按照下列步驟操作：

1. 在編輯器窗格的分頁列中，按一下「+」符號旁的arrow\_drop\_down下拉式箭頭，然後按一下「筆記本」。
2. 在筆記本儲存格中複製並執行下列程式碼，即可設定及建立基本 Spark 工作階段。

```
from google.cloud.dataproc_spark_connect import DataprocSparkSession
from google.cloud.dataproc_v1 import Session

import pyspark.sql.functions as f

session = Session()

# Create the Spark session.
spark = (
   DataprocSparkSession.builder
     .appName("APP_NAME")
     .dataprocSessionConfig(session)
     .getOrCreate()
)
```

更改下列內容：

* APP\_NAME：工作階段的選用名稱。
* **選用工作階段設定：**您可以新增 Managed Service for Apache Spark API
  [`Session`](https://docs.cloud.google.com/dataproc-serverless/docs/reference/rest/v1/projects.locations.sessions?hl=zh-tw#Session)
  設定，自訂工作階段。以下舉幾個例子說明：
  + [`RuntimeConfig`](https://docs.cloud.google.com/dataproc-serverless/docs/reference/rest/v1/RuntimeConfig?hl=zh-tw)：

    - `session.runtime_config.properties={spark.property.key1:VALUE_1,...,spark.property.keyN:VALUE_N}`
    - `session.runtime_config.container_image = path/to/container/image`
  + [`EnvironmentConfig`](https://docs.cloud.google.com/dataproc-serverless/docs/reference/rest/v1/EnvironmentConfig?hl=zh-tw#ExecutionConfig)：

    - session.environment\_config.execution\_config.subnetwork\_uri = "SUBNET\_NAME"
    - `session.environment_config.execution_config.ttl = {"seconds": VALUE}`
    - `session.environment_config.execution_config.service_account = SERVICE_ACCOUNT`

### 範本 Spark 工作階段

您可以在筆記本儲存格中輸入並執行程式碼，根據現有的[工作階段範本](https://docs.cloud.google.com/dataproc-serverless/docs/guides/create-serverless-sessions-templates?hl=zh-tw#create-dataproc-serverless-session-template)建立 Spark 工作階段。您在筆記本程式碼中提供的任何 `session` 設定，都會覆寫在工作階段範本中設定的相同設定。

如要快速上手，請使用`Query using Spark`範本預先填入 Spark 工作階段範本程式碼：

1. 在編輯器窗格的分頁列中，按一下「+」符號旁的arrow\_drop\_down下拉式箭頭，然後點選「筆記本」。
2. 在「從範本開始」下方，按一下「使用 Spark 查詢」，然後點選「使用範本」，將程式碼插入筆記本。
3. 請按照「[附註](#notes)」一節的說明指定變數。
4. 您可以刪除插入筆記本中的任何其他程式碼範例儲存格。

```
from google.cloud.dataproc_spark_connect import DataprocSparkSession
from google.cloud.dataproc_v1 import Session
session = Session()
project_id = "PROJECT_ID"
location = "LOCATION"
# Configure the session with an existing session template.
session_template = "SESSION_TEMPLATE"
session.session_template = f"projects/{project_id}/locations/{location}/sessionTemplates/{session_template}"
# Create the Spark session.
spark = (
   DataprocSparkSession.builder
     .appName("APP_NAME")
     .dataprocSessionConfig(session)
     .getOrCreate()
)
```

請替換下列項目：

* PROJECT\_ID：專案 ID，列於[Google Cloud 控制台資訊主頁](https://console.cloud.google.com/home/dashboard?hl=zh-tw)的「專案資訊」部分。
* LOCATION：筆記本工作階段執行的 [Compute Engine 區域](https://docs.cloud.google.com/compute/docs/regions-zones?hl=zh-tw#available)。如未提供，系統會使用建立筆記本的 VM 區域。
* SESSION\_TEMPLATE：現有[互動式工作階段範本](https://docs.cloud.google.com/dataproc-serverless/docs/guides/create-serverless-sessions-templates?hl=zh-tw#create-dataproc-serverless-session-template)的名稱。系統會從範本取得工作階段設定。
  範本也必須指定下列設定：

  + 執行階段版本 [`2.3`+](https://docs.cloud.google.com/dataproc-serverless/docs/concepts/versions/spark-runtime-2.3?hl=zh-tw)
  + 筆記本類型：`Spark Connect`

    範例：
* APP\_NAME：工作階段的選用名稱。

## 在 BigQuery Studio 筆記本中撰寫及執行 PySpark 程式碼

在筆記本中建立 Spark 工作階段後，即可使用該工作階段在筆記本中執行 Spark 筆記本程式碼。

**支援 Spark Connect PySpark API：**Spark Connect 筆記本工作階段支援大部分的 [PySpark API](https://spark.apache.org/docs/latest/api/python/reference/index.html)，包括 [DataFrame](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/dataframe.html)、[Functions](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/functions.html) 和 [Column](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/column.html)，但不支援 [SparkContext](https://spark.apache.org/docs/latest/api/python/reference/api/pyspark.SparkContext.html) 和 [RDD](https://spark.apache.org/docs/latest/api/python/reference/api/pyspark.RDD.html) 等其他 PySpark API。詳情請參閱「[Spark 3.5 支援的項目](https://spark.apache.org/docs/latest/spark-connect-overview.html#what-is-supported)」。

**提示：** 您可以查看 [Spark SQL API 參考資料](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/index.html)，瞭解 Spark Connect 是否支援某個 API。支援的 API 說明文件會顯示「支援 Spark Connect」訊息：

**Spark Connect 筆記本直接寫入**：BigQuery Studio 筆記本中的 Spark 工作階段會預先設定 [Spark BigQuery 連接器](https://docs.cloud.google.com/dataproc/docs/tutorials/bigquery-connector-spark-example?hl=zh-tw)，以便直接寫入資料。DIRECT 寫入方法會使用 [BigQuery Storage Write API](https://docs.cloud.google.com/bigquery/docs/write-api?hl=zh-tw)，將資料直接寫入 BigQuery；INDIRECT 寫入方法 (Managed Service for Apache Spark 批次作業的預設方法) 會將資料寫入中繼 Cloud Storage 值區，然後將資料寫入 BigQuery (如要進一步瞭解 INDIRECT 寫入，請參閱「[在 BigQuery 間讀寫資料](https://docs.cloud.google.com/dataproc/docs/tutorials/bigquery-connector-spark-example?hl=zh-tw#read-and-write-data-from-and-to-bigquery)」)。

**Managed Service for Apache Spark 專屬 API：**Managed Service for Apache Spark 擴充了 `addArtifacts` 方法，可簡化動態將 `PyPI` 套件新增至 Spark 工作階段的程序。您可以採用 [`version-scheme`](https://packaging.python.org/en/latest/specifications/version-specifiers/#examples-of-compliant-version-schemes) 格式指定清單 (類似於 `pip install`)。這會指示 Spark Connect 伺服器在所有叢集節點上安裝套件及其依附元件，讓工作站可將這些套件用於 UDF。

以下範例會在叢集上安裝指定的 `textdistance` 版本和最新相容的 `random2` 程式庫，讓使用 `textdistance` 和 `random2` 的 UDF 在工作節點上執行。

```
spark.addArtifacts("textdistance==4.6.1", "random2", pypi=True)
```

**筆記本程式碼說明：**在 BigQuery Studio 筆記本中，將指標懸停在類別或方法名稱上時，系統會提供程式碼說明；輸入程式碼時，系統會提供程式碼自動完成說明。

在下列範例中，輸入 `DataprocSparkSession` 並將指標懸停在這個類別名稱上，會顯示程式碼自動完成和說明文件輔助功能。


**提示：** 如要瞭解如何[使用 `DataprocSparkSession.builder` 方法](https://github.com/GoogleCloudDataproc/dataproc-spark-connect-python?tab=readme-ov-file#builder-configuration)設定 Spark Connect 工作階段，請參閱 GitHub 上的 [Dataproc Spark Connect Client](https://github.com/GoogleCloudDataproc/dataproc-spark-connect-python)。

### BigQuery Studio 筆記本 PySpark 範例

本節提供 BigQuery Studio Python 筆記本範例，其中包含 PySpark 程式碼，可執行下列工作：

* 對莎士比亞公開資料集執行字數統計。
* 建立 Iceberg 資料表，並將中繼資料儲存在 [Lakehouse 執行階段目錄](https://docs.cloud.google.com/bigquery/docs/about-blms?hl=zh-tw)中。

### Wordcount

下列 PySpark 範例會建立 Spark 工作階段，然後計算公開 `bigquery-public-data.samples.shakespeare` 資料集中出現的字詞。

```
# Basic wordcount example
from google.cloud.dataproc_spark_connect import DataprocSparkSession
from google.cloud.dataproc_v1 import Session
import pyspark.sql.functions as f
session = Session()

# Create the Spark session.
spark = (
   DataprocSparkSession.builder
     .appName("APP_NAME")
     .dataprocSessionConfig(session)
     .getOrCreate()
)
# Run a wordcount on the public Shakespeare dataset.
df = spark.read.format("bigquery").option("table", "bigquery-public-data.samples.shakespeare").load()
words_df = df.select(f.explode(f.split(f.col("word"), " ")).alias("word"))
word_counts_df = words_df.filter(f.col("word") != "").groupBy("word").agg(f.count("*").alias("count")).orderBy("word")
word_counts_df.show()
```

更改下列內容：

* APP\_NAME：工作階段的選用名稱。

**輸出內容：**

儲存格輸出內容會列出字數統計輸出內容的範例。如要在 Google Cloud 控制台中查看工作階段詳細資料，請按一下「Interactive Session Detail View」(互動式工作階段詳細資料檢視畫面) 連結。如要監控 Spark 工作階段，請在工作階段詳細資料頁面中按一下「View Spark UI」(查看 Spark UI)。



```
Interactive Session Detail View: LINK
+------------+-----+
|        word|count|
+------------+-----+
|           '|   42|
|       ''All|    1|
|     ''Among|    1|
|       ''And|    1|
|       ''But|    1|
|    ''Gamut'|    1|
|       ''How|    1|
|        ''Lo|    1|
|      ''Look|    1|
|        ''My|    1|
|       ''Now|    1|
|         ''O|    1|
|      ''Od's|    1|
|       ''The|    1|
|       ''Tis|    4|
|      ''When|    1|
|       ''tis|    1|
|      ''twas|    1|
|          'A|   10|
|'ARTEMIDORUS|    1|
+------------+-----+
only showing top 20 rows
```

### Iceberg 資料表

## 執行 PySpark 程式碼，使用 Lakehouse 執行階段目錄中繼資料建立 Iceberg 資料表

下列範例程式碼會建立 `sample_iceberg_table`，並將資料表的中繼資料儲存在 Lakehouse 執行階段目錄中，然後查詢資料表。

```
from google.cloud.dataproc_spark_connect import DataprocSparkSession
from google.cloud.dataproc_v1 import Session
# Create the Dataproc Serverless session.
session = Session()
# Set the session configuration for BigLake Metastore with the Iceberg environment.
project_id = "PROJECT_ID"
region = "REGION"
subnet_name = "SUBNET_NAME"
location = "LOCATION"
session.environment_config.execution_config.subnetwork_uri = f"{subnet_name}"
warehouse_dir = "gs://BUCKET/WAREHOUSE_DIRECTORY"
catalog = "CATALOG"
namespace = "NAMESPACE"
session.runtime_config.properties[f"spark.sql.catalog.{catalog}"] = "org.apache.iceberg.spark.SparkCatalog"
session.runtime_config.properties[f"spark.sql.catalog.{catalog}.catalog-impl"] = "org.apache.iceberg.gcp.bigquery.BigQueryMetastoreCatalog"
session.runtime_config.properties[f"spark.sql.catalog.{catalog}.gcp_project"] = f"{project_id}"
session.runtime_config.properties[f"spark.sql.catalog.{catalog}.gcp_location"] = f"{location}"
session.runtime_config.properties[f"spark.sql.catalog.{catalog}.warehouse"] = f"{warehouse_dir}"
# Create the Spark Connect session.
spark = (
   DataprocSparkSession.builder
     .appName("APP_NAME")
     .dataprocSessionConfig(session)
     .getOrCreate()
)
# Create the namespace in BigQuery.
spark.sql(f"USE `{catalog}`;")
spark.sql(f"CREATE NAMESPACE IF NOT EXISTS `{namespace}`;")
spark.sql(f"USE `{namespace}`;")
# Create the Iceberg table.
spark.sql("DROP TABLE IF EXISTS `sample_iceberg_table`");
spark.sql("CREATE TABLE sample_iceberg_table (id int, data string) USING ICEBERG;")
spark.sql("DESCRIBE sample_iceberg_table;")
# Insert table data and query the table.
spark.sql("INSERT INTO sample_iceberg_table VALUES (1, \"first row\");")
# Alter table, then query and display table data and schema.
spark.sql("ALTER TABLE sample_iceberg_table ADD COLUMNS (newDoubleCol double);")
spark.sql("DESCRIBE sample_iceberg_table;")
df = spark.sql("SELECT * FROM sample_iceberg_table")
df.show()
df.printSchema()
```

注意：

* PROJECT\_ID：專案 ID，列於[Google Cloud 控制台資訊主頁](https://console.cloud.google.com/home/dashboard?hl=zh-tw)的「專案資訊」部分。
* REGION 和 SUBNET\_NAME：指定 [Compute Engine 區域](https://docs.cloud.google.com/compute/docs/regions-zones?hl=zh-tw#available)，以及工作階段區域中的子網路名稱。Managed Service for Apache Spark 會在指定的子網路上啟用[Private Google Access (PGA)](https://docs.cloud.google.com/vpc/docs/private-google-access?hl=zh-tw)。
* LOCATION：預設值為 `BigQuery_metastore_config.location` 和 `spark.sql.catalog.{catalog}.gcp_location`，但您可以選擇任何`US`[支援的 BigQuery 位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw#supported_locations)。
* BUCKET 和 WAREHOUSE\_DIRECTORY：用於 Iceberg 倉儲目錄的 Cloud Storage 值區和資料夾。
* CATALOG 和 NAMESPACE：Iceberg 目錄名稱和命名空間會合併，用於識別 Iceberg 資料表 (`catalog.namespace.table_name`)。
* APP\_NAME：工作階段的選用名稱。

儲存格輸出內容會列出 `sample_iceberg_table`，並顯示 Google Cloud 控制台的「互動式工作階段詳細資料」頁面連結。您可以在工作階段詳細資料頁面點選「View Spark UI」(查看 Spark UI)，監控 Spark 工作階段。



```
Interactive Session Detail View: LINK
+---+---------+------------+
| id|     data|newDoubleCol|
+---+---------+------------+
|  1|first row|        NULL|
+---+---------+------------+

root
 |-- id: integer (nullable = true)
 |-- data: string (nullable = true)
 |-- newDoubleCol: double (nullable = true)
```

### 在 BigQuery 中查看資料表詳細資料

請按照下列步驟，在 BigQuery 中查看 Iceberg 資料表詳細資料：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在專案資源窗格中，按一下專案，然後按一下命名空間，列出 `sample_iceberg_table` 資料表。按一下「詳細資料」資料表，即可查看「開啟目錄資料表設定」資訊。

   輸入和輸出格式是 Iceberg 使用的標準 Hadoop `InputFormat` 和 `OutputFormat` 類別格式。

### 其他範例

從 Pandas DataFrame (`df`) 建立 Spark `DataFrame` (`sdf`)。

```
sdf = spark.createDataFrame(df)
sdf.show()
```

在 Spark `DataFrames` 上執行匯總作業。

```
from pyspark.sql import functions as f

sdf.groupby("segment").agg(
   f.mean("total_spend_per_user").alias("avg_order_value"),
   f.approx_count_distinct("user_id").alias("unique_customers")
).show()
```

使用 [Spark-BigQuery](https://docs.cloud.google.com/dataproc/docs/tutorials/bigquery-connector-spark-example?hl=zh-tw) 連接器從 BigQuery 讀取資料。

```
spark.conf.set("viewsEnabled","true")
spark.conf.set("materializationDataset","my-bigquery-dataset")

sdf = spark.read.format('bigquery') \
 .load(query)
```

### 使用 Gemini Code Assist 撰寫 Spark 程式碼

**預覽**

這項產品或功能適用《[服務專屬條款](https://docs.cloud.google.com/terms/service-terms?hl=zh-tw#1)》中「一般服務條款」一節的《正式發布前產品條款》。正式發布前的產品和功能是按照「原樣」提供，支援範圍可能有限。
詳情請參閱[推出階段說明](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages)。

您可以問問 Gemini Code Assist，請它在筆記本中生成 PySpark 程式碼。Gemini Code Assist 會擷取並使用相關的 BigQuery 和 Dataproc Metastore 資料表及其結構定義，生成程式碼回覆。

如要在筆記本中生成 Gemini Code Assist 程式碼，請按照下列步驟操作：

1. 點選工具列中的「+ Code」，插入新的程式碼儲存格。
   新的程式碼儲存格會顯示 `Start coding or generate with AI`。
   點選「生成」。
2. 在「生成」編輯器中輸入自然語言提示，然後按一下 `enter`。**請務必在提示中加入 `spark` 或 `pyspark` 關鍵字。**

   提示範例：

   ```
   create a spark dataframe from order_items and filter to orders created in 2024
   ```

   輸出內容範例：

   ```
   spark.read.format("bigquery").option("table", "sqlgen-testing.pysparkeval_ecommerce.order_items").load().filter("year(created_at) = 2024").createOrReplaceTempView("order_items")
   df = spark.sql("SELECT * FROM order_items")
   ```

### 使用 Gemini Code Assist 生成程式碼的提示

* 為了讓 Gemini Code Assist 擷取相關的資料表和結構定義，請為 Dataproc Metastore 執行個體啟用 [Data Catalog 同步處理功能](https://docs.cloud.google.com/dataproc-metastore/docs/data-catalog-sync?hl=zh-tw)。
* 請確保使用者帳戶可以存取 Data Catalog 的查詢資料表，做法是指派 [`DataCatalog.Viewer` 角色](https://docs.cloud.google.com/iam/docs/roles-permissions/datacatalog?hl=zh-tw#datacatalog.viewer)。

## 結束 Spark 工作階段

如要在 BigQuery Studio 筆記本中停止 Spark Connect 工作階段，可以採取下列任一動作：

* 在筆記本儲存格中執行 `spark.stop()`。
* 終止筆記本中的執行階段：
  1. 按一下執行階段選取器，然後按一下「管理工作階段」。
  2. 在「Active sessions」(有效工作階段) 對話方塊中，按一下終止圖示，然後點選「Terminate」(終止)。

## 協調 BigQuery Studio 筆記本程式碼

您可以透過下列方式協調 BigQuery Studio 筆記本程式碼：

* 從 Google Cloud 控制台排定筆記本程式碼 (適用[筆記本定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#external_services))。
* 以批次工作負載形式執行筆記本程式碼 (適用 [Managed Service for Apache Spark 定價](https://cloud.google.com/dataproc-serverless/pricing?hl=zh-tw))。

### 透過 Google Cloud 控制台排定筆記本程式碼執行時間

您可以透過下列方式排定筆記本程式碼的執行時間：

* [排定筆記本執行時間](https://docs.cloud.google.com/bigquery/docs/orchestrate-notebooks?hl=zh-tw)。
* 如果筆記本程式碼執行作業是工作流程的一部分，請將筆記本排定為[管道](https://docs.cloud.google.com/bigquery/docs/orchestrate-workflows?hl=zh-tw)的一部分。

### 以批次工作負載的形式執行筆記本程式碼

請完成下列步驟，以批次工作負載的形式執行 BigQuery Studio 筆記本程式碼。

1. 在本機終端機或 [Cloud Shell](https://console.cloud.google.com/?cloudshell=true&hl=zh-tw) 中，將筆記本程式碼下載到檔案。

   建議您下載到 Cloud Shell 並在其中作業，因為 Cloud Shell 已預先安裝[文字編輯器和其他工具](https://docs.cloud.google.com/shell/docs/how-cloud-shell-works?hl=zh-tw#tools)，並提供內建的 [Python 支援](https://docs.cloud.google.com/shell/docs/how-cloud-shell-works?hl=zh-tw#language_support)。
   1. 在 Google Cloud 控制台的「BigQuery Studio」[頁面](https://console.cloud.google.com/bigquery?hl=zh-tw)上，開啟「Explorer」窗格中的筆記本。
   2. 如要展開選單列，請依序點選 keyboard\_arrow\_down **切換標題顯示設定**。
   3. 依序點選「File」**>「Download」**，然後點選「Download.py」。
2. 生成 `requirements.txt`。

   1. 在儲存 `.py` 檔案的目錄中安裝 `pipreqs`。

      ```
      pip install pipreqs
      ```
   2. 執行 `pipreqs` 即可生成 `requirements.txt`。

      ```
      pipreqs filename.py
      ```
   3. 使用 [Google Cloud CLI](https://docs.cloud.google.com/sdk/gcloud?hl=zh-tw) 將本機 `requirements.txt` 檔案複製到 Cloud Storage 中的 bucket。

      ```
      gcloud storage cp requirements.txt gs://BUCKET/
      ```
3. 編輯下載的 `.py` 檔案，更新 Spark 工作階段程式碼。

   1. 移除或註解排除任何殼層指令碼指令。
   2. 移除設定 Spark 工作階段的程式碼，然後將設定參數指定為批次工作負載提交參數。(請參閱「[提交 Spark 批次工作負載](https://docs.cloud.google.com/dataproc-serverless/docs/quickstarts/spark-batch?hl=zh-tw#submit_a_spark_batch_workload)」)。

      範例：

      * 從程式碼中移除下列工作階段子網路設定行：

        ```
        session.environment_config.execution_config.subnetwork_uri = "{subnet_name}"
        ```
      * [執行批次工作負載](#run-the-batch-workload)時，請使用 `--subnet` 旗標指定子網路。

        ```
        gcloud dataproc batches submit pyspark \
        --subnet=SUBNET_NAME
        ```
   3. 使用簡單的工作階段建立程式碼片段。

      * 簡化前下載的筆記本程式碼範例。

        ```
        from google.cloud.dataproc_spark_connect import DataprocSparkSession
        from google.cloud.dataproc_v1 import Session

        session = Session()
        spark = DataprocSparkSession \
            .builder \
            .appName("CustomSparkSession")
            .dataprocSessionConfig(session) \
            .getOrCreate()
        ```
      * 簡化後的批次工作負載程式碼。

        ```
        from pyspark.sql import SparkSession

        spark = SparkSession \
        .builder \
        .getOrCreate()
        ```
4. 執行批次工作負載。

   1. 如需操作說明，請參閱「[提交 Spark 批次工作負載](https://docs.cloud.google.com/dataproc-serverless/docs/quickstarts/spark-batch?hl=zh-tw#submit_a_spark_batch_workload)」。

      * 請務必加入 --deps-bucket 標記，指向包含 `requirements.txt` 檔案的 Cloud Storage bucket。

        範例：

      ```
      gcloud dataproc batches submit pyspark FILENAME.py \
          --region=REGION \
          --deps-bucket=BUCKET \
          --version=2.3
      ```

      注意：

      * FILENAME：下載並編輯的筆記本程式碼檔案名稱。
      * REGION：叢集所在的 Compute Engine [區域](https://docs.cloud.google.com/compute/docs/regions-zones?hl=zh-tw#available)。
      * BUCKET：包含 `requirements.txt` 檔案的 Cloud Storage bucket 名稱。
      * `--version`：選取 [Spark 執行階段 2.3 版](https://docs.cloud.google.com/dataproc-serverless/docs/concepts/versions/spark-runtime-2.3?hl=zh-tw)，執行批次工作負載。
5. 提交程式碼。

   1. 測試批次工作負載程式碼後，您可以使用 `git` 用戶端 (例如 GitHub、GitLab 或 Bitbucket) 將 `.ipynb` 或 `.py` 檔案提交至存放區，做為 CI/CD pipeline 的一部分。
6. 使用 Managed Service for Apache Airflow 安排批次工作負載。

   1. 如需操作說明，請參閱「[使用 Managed Airflow 執行 Managed Service for Apache Spark 工作負載](https://docs.cloud.google.com/composer/docs/composer-2/run-dataproc-workloads?hl=zh-tw)」。

## 排解筆記本錯誤

如果含有 Spark 程式碼的儲存格發生失敗，您可以按一下儲存格輸出內容中的「互動式工作階段詳細資料檢視畫面」連結，排解錯誤 (請參閱「[字數統計和 Iceberg 表格範例](#dataproc_serverless_bq_notebook-Wordcount)」)。

如果遇到 Notebook 程式碼錯誤，通常只要前往 **Spark UI** 中的最後一個 Spark 工作，就能取得額外資訊，協助您偵錯失敗的工作。

### 已知問題和解決方案

**錯誤**：使用 Python 版本 `3.10` 建立的 [Notebook 執行階段](https://console.cloud.google.com/vertex-ai/colab/runtimes?hl=zh-tw)，嘗試連線至 Spark 工作階段時可能會導致 `PYTHON_VERSION_MISMATCH` 錯誤。

**解決方案**：使用 Python 版本 `3.11` 重新建立執行階段。

## 後續步驟

* YouTube 影片示範：[善用與 BigQuery 整合的 Apache Spark 強大功能](https://www.youtube.com/watch?v=DIZn6Nuur7k&hl=zh-tw)。
* [將 Lakehouse 執行階段目錄與 Managed Service for Apache Spark 搭配使用](https://docs.cloud.google.com/bigquery/docs/bqms-use-dataproc?hl=zh-tw)
* [將 Lakehouse 執行階段目錄與 Managed Service for Apache Spark 搭配使用](https://docs.cloud.google.com/bigquery/docs/bqms-use-dataproc-serverless?hl=zh-tw)




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-04-30 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-04-30 (世界標準時間)。"],[],[]]