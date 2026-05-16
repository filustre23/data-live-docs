自 2026 年 4 月 20 日起，BigLake 现在称为 Lakehouse for Apache Iceberg。BigLake metastore 现已更名为 Lakehouse 运行时目录。Lakehouse API、客户端库、CLI 命令和 IAM 名称保持不变，仍引用 BigLake。

Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-cn)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-cn)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-cn)
* [Lakehouse](https://docs.cloud.google.com/lakehouse/docs?hl=zh-cn)
* [指南](https://docs.cloud.google.com/lakehouse/docs/introduction?hl=zh-cn)

发送反馈

# 设置 Lakehouse Iceberg REST 目录 使用集合让一切井井有条 根据您的偏好保存内容并对其进行分类。

对于新工作流，我们建议使用 *Lakehouse 运行时目录*中的 *Apache Iceberg REST Catalog* 端点。

此端点充当单一可信来源，可在各个查询引擎之间实现无缝互操作。它使 Apache Spark 等引擎能够一致地发现、读取和管理 Google Cloud Lakehouse 表。

如果您使用开源引擎访问 Cloud Storage 中的数据，并且需要与其他引擎（包括 BigQuery）实现互操作性，那么此方法是不错的选择。它支持[凭据自动售卖](#create_a_catalog)等功能，可实现精细的访问权限控制，还支持[跨区域复制和灾难恢复](https://docs.cloud.google.com/lakehouse/docs/about-managed-disaster-recovery?hl=zh-cn)。

相比之下，[*适用于 BigQuery 的自定义 Apache Iceberg 目录*端点](https://docs.cloud.google.com/lakehouse/docs/configure-lakehouse-catalog-iceberg-1-10?hl=zh-cn)是较早的集成。虽然现有工作流可以继续使用它，但 REST 目录提供了更标准化且功能更丰富的体验。

## 准备工作

在继续操作之前，请先熟悉 [Lakehouse 运行时目录](https://docs.cloud.google.com/lakehouse/docs/about-lakehouse-catalogs?hl=zh-cn)和 [Iceberg REST 目录端点概览](https://docs.cloud.google.com/lakehouse/docs/understand-catalog-types?hl=zh-cn)。

1. [验证是否已为您的 Google Cloud 项目启用结算功能](https://docs.cloud.google.com/billing/docs/how-to/verify-billing-enabled?hl=zh-cn#confirm_billing_is_enabled_on_a_project)。
2. 启用 BigLake API。

   **启用 API 所需的角色**

   如需启用 API，您需要拥有 Service Usage Admin IAM 角色 (`roles/serviceusage.serviceUsageAdmin`)，该角色包含 `serviceusage.services.enable` 权限。[了解如何授予角色](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-cn)。

   [启用 API](https://console.cloud.google.com/flows/enableapi?apiid=biglake.googleapis.com&hl=zh-cn)

### 所需的角色

如需获得在 Lakehouse 运行时目录中使用 Apache Iceberg REST 目录端点所需的权限，请让管理员为您授予以下 IAM 角色：

* 执行管理任务，例如管理目录用户访问权限、存储访问权限和目录的凭证自动售卖模式：
  + 针对项目的 [BigLake Admin](https://docs.cloud.google.com/iam/docs/roles-permissions/biglake?hl=zh-cn#biglake.admin)  (`roles/biglake.admin`) 角色
  + 针对 Cloud Storage 存储桶的 [Storage Admin](https://docs.cloud.google.com/iam/docs/roles-permissions/storage?hl=zh-cn#storage.admin)  (`roles/storage.admin`)　角色
* 在凭据自动售卖模式下读取表数据：
  项目的 [BigLake Viewer](https://docs.cloud.google.com/iam/docs/roles-permissions/biglake?hl=zh-cn#biglake.viewer)  (`roles/biglake.viewer`) 角色。如果您使用 Managed Service for Apache Spark、Managed Service for Apache Spark 或 Dataflow 等查询引擎读取表数据，请向您用于在该引擎中运行作业的服务账号授予此角色。
* 以凭据自动售卖模式写入表数据：项目的 [BigLake Editor](https://docs.cloud.google.com/iam/docs/roles-permissions/biglake?hl=zh-cn#biglake.editor)  (`roles/biglake.editor`) 角色。如果您使用 Managed Service for Apache Spark、Managed Service for Apache Spark 或 Dataflow 等查询引擎来写入表数据，请向您用于在该引擎中运行作业的服务账号授予此角色。
* 在凭据贩卖模式下使用自动预配的 Lakehouse 运行时目录服务账号：目标 Cloud Storage 存储桶上的 [Storage Object User](https://docs.cloud.google.com/iam/docs/roles-permissions/storage?hl=zh-cn#storage.objectUser)  (`roles/storage.objectUser`)。创建目录后，请向目录的自动预配 Lakehouse 运行时目录服务账号明确授予存储桶的 Storage Object User 角色 (`roles/storage.objectUser`)。
* 在非凭证自动售卖模式下读取目录资源和表数据：
  + 项目的 [BigLake Viewer](https://docs.cloud.google.com/iam/docs/roles-permissions/biglake?hl=zh-cn#biglake.viewer)  (`roles/biglake.viewer`) 角色
  + 针对 Cloud Storage 存储桶的 [Storage Object Viewer](https://docs.cloud.google.com/iam/docs/roles-permissions/storage?hl=zh-cn#storage.objectViewer)  (`roles/storage.objectViewer`) 角色
* 在非凭证自动售卖模式下管理目录资源和写入表数据：
  + 项目的 [BigLake Editor](https://docs.cloud.google.com/iam/docs/roles-permissions/biglake?hl=zh-cn#biglake.editor)  (`roles/biglake.editor`) 角色
  + 针对 Cloud Storage 存储桶的 [Storage Object User](https://docs.cloud.google.com/iam/docs/roles-permissions/storage?hl=zh-cn#storage.objectUser)  (`roles/storage.objectUser`) 角色
* 使用 BigQuery 目录联合执行数据操纵语言 (DML) 操作：
  + 项目的 [BigQuery Data Editor](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-cn#bigquery.dataEditor)  (`roles/bigquery.dataEditor`) 角色
  + 针对 Cloud Storage 存储桶的 [Storage Admin](https://docs.cloud.google.com/iam/docs/roles-permissions/storage?hl=zh-cn#storage.admin)  (`roles/storage.admin`) 角色。如果您使用 Managed Service for Apache Spark 等查询引擎执行 DML 操作，请向您用于在该引擎中运行作业的服务账号授予这些角色。

如需详细了解如何授予角色，请参阅[管理对项目、文件夹和组织的访问权限](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-cn)。

您也可以通过[自定义角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-cn)或其他[预定义角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-cn#predefined)来获取所需的权限。

## 限制

Apache Iceberg REST Catalog 端点受以下限制：

**一般限制**

* 只有在使用 Compute Engine 2.3 映像版本 2.3.16 及更高版本的 Managed Service for Apache Spark 时，Trino 才支持 BigQuery 目录联合。
* 使用凭证分发模式时，您必须将 `io-impl` 属性设置为 `org.apache.iceberg.gcp.gcs.GCSFileIO`。默认值 `org.apache.iceberg.hadoop.HadoopFileIO` 不受支持。

**表格限制**

* 通过 Apache Iceberg REST Catalog 端点管理的表不支持精细访问权限控制 (FGAC)，例如行级和列级安全性。

**数据限制**

* 仅支持 Parquet 文件。如需详细了解 BigQuery 如何处理 Parquet 文件，请参阅[从 Cloud Storage 加载 Parquet 数据](https://docs.cloud.google.com/bigquery/docs/loading-data-cloud-storage-parquet?hl=zh-cn)。
* Iceberg `metadata.json` 文件大小上限为 1MB。如需申请提高此限制，请与您的 Google 客户支持团队联系。

**查询限制**

* 无法在 BigQuery 中创建由 Apache Iceberg REST 目录端点管理的 Apache Iceberg 表的视图。
* 在 BigQuery 中，无法使用五部分名称标识符查询 Apache Iceberg 元数据表（例如 `.snapshots` 或 `.files`）；您可以使用 Spark 查询这些表。

## 设置 Iceberg REST Catalog 端点

在设置目录之前，建议您先阅读 [Apache Iceberg REST 目录端点概览](https://docs.cloud.google.com/lakehouse/docs/understand-catalog-types?hl=zh-cn)，了解其资源层次结构、目录类型和命名结构。

在 Lakehouse 运行时目录中使用 Apache Iceberg REST 目录端点时，一般需要遵循以下步骤：

1. 根据 [Iceberg REST 目录端点概览](https://docs.cloud.google.com/lakehouse/docs/understand-catalog-types?hl=zh-cn)，选择目录数据仓库位置（Cloud Storage 或 BigQuery）。
2. 如果您使用的是 Cloud Storage `gs://` 数据仓库，请创建一个指向数据仓库位置的目录。
3. 将客户端应用配置为使用 Apache Iceberg REST Catalog 端点。
4. 创建命名空间或架构来整理表。
5. 使用配置的客户端创建和查询表。

### 创建目录

您可以创建使用最终用户凭据或凭据贩售模式的目录。

* 借助最终用户凭据，目录会将访问它的最终用户的身份传递给 Cloud Storage 以进行授权检查。
* 凭据贩卖是一种存储访问权限委托机制，可让 Lakehouse 运行时目录管理员直接控制 Lakehouse 运行时目录资源的权限，从而无需目录用户直接访问 Cloud Storage 存储分区。借助此功能，Google Cloud 的 *Lakehouse* 管理员可以向用户授予对特定数据文件的权限。

**注意事项**

在创建目录之前，请先熟悉[位置要求](https://docs.cloud.google.com/lakehouse/docs/understand-catalog-types?hl=zh-cn#bucket_and_catalog_regions)。

* 创建命名空间时，系统会自动使用与目录相同的区域。
* 如果您的目录使用多区域存储桶，并且您想将其与 BigQuery 多区域（`US` 或 `EU`）搭配使用，则必须删除并重新创建目录，以指定主要位置。

### 最终用户凭据

### 控制台

1. 在 Google Cloud 控制台中打开 **Lakehouse** 页面。

   [前往 Lakehouse](https://console.cloud.google.com/biglake?hl=zh-cn)
2. 点击**创建目录**。
3. 在**选择 Cloud Storage 存储桶**字段中，输入要与目录搭配使用的 Cloud Storage 存储桶的名称。或者，点击**浏览**以选择现有存储桶或创建新存储桶。每个 Cloud Storage 存储桶只能有一个目录。
4. 对于**身份验证方法**，选择**最终用户凭据**。
5. 点击**创建**。

### gcloud

使用 [`gcloud biglake iceberg catalogs create` 命令](https://docs.cloud.google.com/sdk/gcloud/reference/biglake/iceberg/catalogs/create?hl=zh-cn)。

```
gcloud biglake iceberg catalogs create \
    CATALOG_NAME \
    --project PROJECT_ID \
    --catalog-type gcs-bucket \
    --credential-mode end-user \
    [--primary-location LOCATION]
```

替换以下内容：

* `CATALOG_NAME`：目录的名称。对于 [Apache Iceberg 的受管 Lakehouse REST 目录表](https://docs.cloud.google.com/lakehouse/docs/lakehouse-iceberg-tables?hl=zh-cn)，此名称通常与 REST 目录使用的 Cloud Storage 存储桶 ID 匹配，例如，如果您的存储桶为 `gs://bucket-id`，则目录名称可能为 `bucket-id`。从 [BigQuery 查询这些表](#query-tables)时，此名称也用作目录标识符。
* `PROJECT_ID`：您的 Google Cloud 项目 ID。
* `LOCATION`：（可选）目录的主区域，用于确保与 BigQuery 的互操作性。
  对于美国区域（例如 `US` 或 `us-central1`）或欧盟区域（例如 `EU` 或 `europe-west4`）中的 Cloud Storage 存储分区，请分别指定 `US` 或 `EU`，以确保目录可供相应 BigQuery 多区域位置查询。如需了解详情，请参阅[存储分区和目录区域](https://docs.cloud.google.com/lakehouse/docs/understand-catalog-types?hl=zh-cn#bucket_and_catalog_regions)。

### 凭证分发模式

目录管理员可以在创建或更新目录时启用凭据自动发放功能。作为目录用户，您可以在[配置 Apache Iceberg REST 目录端点](#configure-catalog)时指定访问权限委托，从而指示 Apache Iceberg REST 目录端点返回降级后的存储凭据。

自动预配的 Lakehouse 运行时目录服务账号需要对目标 Cloud Storage 存储桶具有明确的 Storage Object User 角色 (`roles/storage.objectUser`)。默认情况下，该角色仅具有查看者访问权限。
如果没有此角色，出售的凭据将没有足够的范围来执行存储写入操作。如果您使用 `gcloud` 或 Terraform 等工具，则必须手动授予此角色。

### 控制台

1. 在 Google Cloud 控制台中，打开 **Lakehouse** 页面。

   [前往 Lakehouse](https://console.cloud.google.com/biglake?hl=zh-cn)
2. 点击 add\_box
   **创建目录**。系统会打开**创建目录**页面。
3. 在**选择 Cloud Storage 存储桶**部分，输入要与目录搭配使用的 Cloud Storage 存储桶的名称。或者，点击**浏览**，从现有存储分区列表中选择一个存储分区或创建一个新存储分区。每个 Cloud Storage 存储桶只能有一个目录。
4. 对于**身份验证方法**，请选择**凭证分发模式**。
5. 点击**创建**。

   系统会创建您的目录，并打开**目录详情**页面。
6. 在**身份验证方法**下，点击**设置存储桶权限**。
7. 在对话框中，点击**确认**。

   这会验证您的目录的服务账号是否对您的存储桶具有 Storage Object Admin 角色。

### gcloud

使用 [`gcloud biglake iceberg catalogs create` 命令](https://docs.cloud.google.com/sdk/gcloud/reference/biglake/iceberg/catalogs/create?hl=zh-cn)。

```
gcloud biglake iceberg catalogs create \
    CATALOG_NAME \
    --project PROJECT_ID \
    --catalog-type gcs-bucket \
    --credential-mode vended-credentials \
    [--primary-location LOCATION]
```

替换以下内容：

* `CATALOG_NAME`：目录的名称。此名称通常与 Lakehouse Iceberg REST 目录使用的 Cloud Storage 存储桶 ID 相匹配，例如，如果您的存储桶为 `gs://bucket-id`，则目录名称可能为 `bucket-id`。从 BigQuery [查询这些表](#query-tables)时，此名称还用作目录标识符。
* `PROJECT_ID`：您的 Google Cloud 项目 ID。
* `LOCATION`：（可选）目录的主区域，用于确保与 BigQuery 的互操作性。对于美国区域（例如 `US` 或 `us-central1`）或欧盟区域（例如 `EU` 或 `europe-west4`）中的 Cloud Storage 存储分区，请分别指定 `US` 或 `EU`，以确保可以从相应的 BigQuery 多区域访问和查询目录。如需了解详情，请参阅[存储分区和目录区域](https://docs.cloud.google.com/lakehouse/docs/understand-catalog-types?hl=zh-cn#bucket_and_catalog_regions)。

  创建目录后，请向目录自动预配的 Lakehouse 运行时目录服务账号明确授予存储桶的 **Storage Object User** 角色 (`roles/storage.objectUser`)。

### 配置客户端应用

创建目录后，请配置客户端应用以使用该目录。这些示例展示了如何配置凭据自动售卖功能（有或没有）。

### 集群

如需在 Managed Service for Apache Spark 上将 Spark 与 Apache Iceberg REST Catalog 端点搭配使用，您可以使用属性来简化配置，也可以手动配置会话。

#### 使用属性简化配置（推荐）

创建具有目录属性的集群：

```
gcloud dataproc clusters create CLUSTER_NAME \
    --enable-component-gateway \
    --project=PROJECT_ID \
    --region=REGION \
    --optional-components=ICEBERG \
    --image-version=DATAPROC_VERSION \
    --properties="dataproc:dataproc.lakehouse.catalog.CATALOG_NAME=projects/PROJECT_ID/catalogs/CATALOG_ID"
```

替换以下内容：

* `CLUSTER_NAME`：集群的名称。
* `PROJECT_ID`：您的 Google Cloud 项目 ID。
* `REGION`：Managed Service for Apache Spark 集群区域。
* `DATAPROC_VERSION`：Managed Service for Apache Spark 映像版本，例如 `2.2`。
* `CATALOG_NAME`：要在 Spark 中使用的 Lakehouse Catalog 的名称。它可以与 CATALOG\_ID 相同。
* `CATALOG_ID`：您创建的 Lakehouse 目录的 ID。

**注意**： 您可以在 `--properties` 标志中配置多个目录，只需用英文逗号分隔即可。例如：`--properties="dataproc:dataproc.lakehouse.catalog.CATALOG_NAME_1=projects/PROJECT_ID_1/catalogs/CATALOG_ID_1,dataproc:dataproc.lakehouse.catalog.CATALOG_NAME_2=projects/PROJECT_ID_2/catalogs/CATALOG_ID_2"`

然后，创建一个不指定手动目录参数的 Spark 会话：

```
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("APP_NAME").getOrCreate()
```

#### 手动配置

如果您不使用集群属性，请按照上述说明创建集群（不使用 `--properties` 标志），然后手动配置 Spark 会话：

```
import pyspark
from pyspark.context import SparkContext
from pyspark.sql import SparkSession

catalog_name = "CATALOG_NAME"
spark = SparkSession.builder.appName("APP_NAME") \
  .config(f'spark.sql.catalog.{catalog_name}', 'org.apache.iceberg.spark.SparkCatalog') \
  .config(f'spark.sql.catalog.{catalog_name}.type', 'rest') \
  .config(f'spark.sql.catalog.{catalog_name}.uri', 'https://biglake.googleapis.com/iceberg/REST_API_VERSION/restcatalog') \
  .config(f'spark.sql.catalog.{catalog_name}.warehouse', 'WAREHOUSE_PATH') \
  .config(f'spark.sql.catalog.{catalog_name}.header.x-goog-user-project', 'PROJECT_ID') \
  .config(f'spark.sql.catalog.{catalog_name}.rest.auth.type', 'org.apache.iceberg.gcp.auth.GoogleAuthManager') \
  .config(f'spark.sql.catalog.{catalog_name}.io-impl', 'org.apache.iceberg.gcp.gcs.GCSFileIO') \
  .config('spark.sql.extensions', 'org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions') \
  .config('spark.sql.defaultCatalog', 'CATALOG_NAME') \
  .getOrCreate()
```

替换以下内容：

* `CATALOG_NAME`：Apache Iceberg REST 目录端点的名称。
* `APP_NAME`：Spark 会话的名称。
* `REST_API_VERSION`：对于稳定的 API 版本，设置为 `v1`。如果需要解决数据沿袭生成方面的[已知问题](https://docs.cloud.google.com/dataproc/docs/guides/create-lakehouse?hl=zh-cn#lineage-known-issue)，请设置为 `v1beta`。
* `WAREHOUSE_PATH`：数据仓库的路径。
  使用 `gs://CLOUD_STORAGE_BUCKET_NAME`。如需使用 [BigQuery 目录联合](https://docs.cloud.google.com/lakehouse/docs/understand-catalog-types?hl=zh-cn#catalog-federation)，请参阅[将目录联合与 BigQuery 搭配使用](#federation)。
* `PROJECT_ID`：使用 Apache Iceberg REST Catalog 端点所产生的费用将计入该项目，该项目可能与拥有 Cloud Storage 存储桶的项目不同。如需详细了解使用 REST API 时的项目配置，请参阅[系统参数](https://docs.cloud.google.com/apis/docs/system-parameters?hl=zh-cn)。

### 通过凭证分发进行配置

如需使用凭据自动售卖，您必须使用[处于凭据自动售卖模式的目录](#create_a_catalog)，并通过向 `SparkSession` build 添加以下行，向 Iceberg REST 目录请求添加值为 `vended-credentials` 的 `X-Iceberg-Access-Delegation` 标头：

```
.config(f'spark.sql.catalog.{catalog_name}.header.X-Iceberg-Access-Delegation','vended-credentials')
```

#### 包含凭证分发的示例

以下示例使用凭据自动售卖功能配置查询引擎：

```
import pyspark
from pyspark.context import SparkContext
from pyspark.sql import SparkSession

catalog_name = "CATALOG_NAME"
spark = SparkSession.builder.appName("APP_NAME") \
  .config(f'spark.sql.catalog.{catalog_name}', 'org.apache.iceberg.spark.SparkCatalog') \
  .config(f'spark.sql.catalog.{catalog_name}.type', 'rest') \
  .config(f'spark.sql.catalog.{catalog_name}.uri', 'https://biglake.googleapis.com/iceberg/REST_API_VERSION/restcatalog') \
  .config(f'spark.sql.catalog.{catalog_name}.warehouse', 'gs://CLOUD_STORAGE_BUCKET_NAME') \
  .config(f'spark.sql.catalog.{catalog_name}.header.x-goog-user-project', 'PROJECT_ID') \
  .config(f'spark.sql.catalog.{catalog_name}.rest.auth.type', 'org.apache.iceberg.gcp.auth.GoogleAuthManager') \
  .config(f'spark.sql.catalog.{catalog_name}.io-impl', 'org.apache.iceberg.gcp.gcs.GCSFileIO') \
  .config(f'spark.sql.catalog.{catalog_name}.header.X-Iceberg-Access-Delegation','vended-credentials') \
  .config('spark.sql.extensions', 'org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions') \
  .config('spark.sql.defaultCatalog', 'CATALOG_NAME') \
  .getOrCreate()
```

如需了解详情，请参阅 Apache Iceberg 文档的 [`RESTCatalog`](https://py.iceberg.apache.org/configuration/#headers-in-rest-catalog) 部分中的“标头”。

Managed Service for Apache Spark 集群在以下版本中支持 Apache Iceberg 的 Google 授权流程：

* Managed Service for Apache Spark on Compute Engine 2.2 映像版本 2.2.65 及更高版本。
* Compute Engine 2.3 上的 Managed Service for Apache Spark 映像版本 2.3.11 及更高版本。

### 无服务器

使用属性（推荐）或通过指定所有参数，向 Managed Service for Apache Spark 提交 [PySpark 批量工作负载](https://docs.cloud.google.com/dataproc-serverless/docs/quickstarts/spark-batch?hl=zh-cn#submit_a_spark_batch_workload)，以简化配置。

#### 使用属性简化配置（推荐）

提交具有目录资源的批量作业：

```
gcloud dataproc batches submit pyspark PYSPARK_FILE \
    --project=PROJECT_ID \
    --region=REGION \
    --version=RUNTIME_VERSION \
    --properties="dataproc:dataproc.lakehouse.catalog.CATALOG_NAME=projects/PROJECT_ID/catalogs/CATALOG_ID"
```

**注意**： 您可以在 `--properties` 标志中配置多个目录，只需用英文逗号分隔即可。例如：`--properties="dataproc:dataproc.lakehouse.catalog.CATALOG_NAME_1=projects/PROJECT_ID_1/catalogs/CATALOG_ID_1,dataproc:dataproc.lakehouse.catalog.CATALOG_NAME_2=projects/PROJECT_ID_2/catalogs/CATALOG_ID_2"`

#### 手动配置

如果您希望手动指定所有属性，请使用以下配置：

```
gcloud dataproc batches submit pyspark PYSPARK_FILE \
    --project=PROJECT_ID \
    --region=REGION \
    --version=RUNTIME_VERSION \
    --properties="\
    spark.sql.defaultCatalog=CATALOG_NAME,\
    spark.sql.catalog.CATALOG_NAME=org.apache.iceberg.spark.SparkCatalog,\
    spark.sql.catalog.CATALOG_NAME.type=rest,\
    spark.sql.catalog.CATALOG_NAME.uri=https://biglake.googleapis.com/iceberg/REST_API_VERSION/restcatalog,\
    spark.sql.catalog.CATALOG_NAME.warehouse=WAREHOUSE_PATH,\
    spark.sql.catalog.CATALOG_NAME.io-impl=org.apache.iceberg.gcp.gcs.GCSFileIO,\
    spark.sql.catalog.CATALOG_NAME.header.x-goog-user-project=PROJECT_ID,\
    spark.sql.catalog.CATALOG_NAME.rest.auth.type=org.apache.iceberg.gcp.auth.GoogleAuthManager,\
    spark.sql.extensions=org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions"
```

替换以下内容：

* `PYSPARK_FILE`：PySpark 应用文件的 `gs://` Cloud Storage 路径。
* `PROJECT_ID`：您的 Google Cloud 项目 ID。
* `REGION`：Managed Service for Apache Spark 批量工作负载的区域。
* `RUNTIME_VERSION`：Managed Service for Apache Spark 运行时版本，例如 `2.2`。
* `CATALOG_NAME`：Apache Iceberg REST 目录端点的名称。
* `REST_API_VERSION`：对于稳定的 API 版本，设置为 `v1`。如果需要解决数据沿袭生成方面的[已知问题](https://docs.cloud.google.com/dataproc/docs/guides/create-lakehouse?hl=zh-cn#lineage-known-issue)，请设置为 `v1beta`。
* `WAREHOUSE_PATH`：数据仓库的路径。
  使用 `gs://CLOUD_STORAGE_BUCKET_NAME`。如需使用 [BigQuery 目录联合](https://docs.cloud.google.com/lakehouse/docs/understand-catalog-types?hl=zh-cn#catalog-federation)，请参阅[将目录联合与 BigQuery 搭配使用](#federation)。

### 通过凭证分发进行配置

如需使用凭据自动售卖，您必须使用[处于凭据自动售卖模式的目录](#create_a_catalog)，并将 `X-Iceberg-Access-Delegation` 标头添加到 Apache Iceberg REST Catalog 端点请求中，其值为 `vended-credentials`，方法是在 Managed Service for Apache Spark 配置中添加以下行：

```
.config(f'spark.sql.catalog.{catalog_name}.header.X-Iceberg-Access-Delegation','vended-credentials')
```

#### 包含凭证分发的示例

以下示例使用凭据自动售卖功能配置查询引擎：

```
gcloud dataproc batches submit pyspark PYSPARK_FILE \
    --project=PROJECT_ID \
    --region=REGION \
    --version=RUNTIME_VERSION \
    --properties="\
    spark.sql.defaultCatalog=CATALOG_NAME,\
    spark.sql.catalog.CATALOG_NAME=org.apache.iceberg.spark.SparkCatalog,\
    spark.sql.catalog.CATALOG_NAME.type=rest,\
    spark.sql.catalog.CATALOG_NAME.uri=https://biglake.googleapis.com/iceberg/REST_API_VERSION/restcatalog,\
    spark.sql.catalog.CATALOG_NAME.warehouse=gs://CLOUD_STORAGE_BUCKET_NAME,\
    spark.sql.catalog.CATALOG_NAME.header.x-goog-user-project=PROJECT_ID,\
    spark.sql.catalog.CATALOG_NAME.rest.auth.type=org.apache.iceberg.gcp.auth.GoogleAuthManager,\
    spark.sql.extensions=org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions,\
    spark.sql.catalog.CATALOG_NAME.gcs.oauth2.refresh-credentials-endpoint=https://oauth2.googleapis.com/token, \
    spark.sql.catalog.CATALOG_NAME.header.X-Iceberg-Access-Delegation=vended-credentials"
```

如需了解详情，请参阅 Apache Iceberg 文档的 [`RESTCatalog`](https://py.iceberg.apache.org/configuration/#headers-in-rest-catalog) 部分中的“标头”。

Managed Service for Apache Spark 在以下运行时版本中支持 Apache Iceberg 的 Google 授权流程：

* Managed Service for Apache Spark 2.2 运行时 2.2.60 及更高版本
* Managed Service for Apache Spark 2.3 运行时 2.3.10 及更高版本

### Trino

如需将 Trino 与 Apache Iceberg REST 目录端点搭配使用，请创建包含 Trino 组件的 Managed Service for Apache Spark 集群，并使用 `gcloud dataproc clusters create --properties` 标志配置目录属性。以下示例创建了一个名为 `CATALOG_NAME` 的 Trino 目录：

```
gcloud dataproc clusters create CLUSTER_NAME \
    --enable-component-gateway \
    --region=REGION \
    --image-version=DATAPROC_VERSION \
    --network=NETWORK_ID \
    --optional-components=TRINO \
    --properties="\
    trino-catalog:CATALOG_NAME.connector.name=iceberg,\
    trino-catalog:CATALOG_NAME.iceberg.catalog.type=rest,\
    trino-catalog:CATALOG_NAME.iceberg.rest-catalog.uri=https://biglake.googleapis.com/iceberg/REST_API_VERSION/restcatalog,\
    trino-catalog:CATALOG_NAME.iceberg.rest-catalog.warehouse=WAREHOUSE_PATH,\
    trino-catalog:CATALOG_NAME.iceberg.rest-catalog.biglake.project-id=PROJECT_ID,\
    trino-catalog:CATALOG_NAME.iceberg.rest-catalog.rest.auth.type=org.apache.iceberg.gcp.auth.GoogleAuthManager"
```

替换以下内容：

* `CLUSTER_NAME`：集群的名称。
* `REGION`：Managed Service for Apache Spark 集群区域。
* `DATAPROC_VERSION`：Managed Service for Apache Spark 映像版本，例如 `2.2`。
* `NETWORK_ID`：集群网络 ID。如需了解详情，请参阅 [Managed Service for Apache Spark 集群网络配置](https://docs.cloud.google.com/dataproc/docs/concepts/configuring-clusters/network?hl=zh-cn)。
* `CATALOG_NAME`：使用 Apache Iceberg REST Catalog 端点的 Trino 目录的名称。
* `REST_API_VERSION`：对于稳定的 API 版本，设置为 `v1`。如果需要解决数据沿袭生成方面的[已知问题](https://docs.cloud.google.com/dataproc/docs/guides/create-lakehouse?hl=zh-cn#lineage-known-issue)，请设置为 `v1beta`。
* `WAREHOUSE_PATH`：数据仓库的路径。
  请使用 `gs://CLOUD_STORAGE_BUCKET_NAME`。
* `PROJECT_ID`：用于 Lakehouse 运行时目录的 Google Cloud 项目 ID。

创建集群后，连接到主虚拟机实例，然后使用 Trino CLI：

```
trino --catalog=CATALOG_NAME
```

Managed Service for Apache Spark Trino 在以下版本中支持 Apache Iceberg 的 Google 授权流：

* Managed Service for Apache Spark on Compute Engine 2.2 运行时版本 2.2.65 及更高版本
* Managed Service for Apache Spark on Compute Engine 2.3 运行时版本 2.3.11 及更高版本
* 不支持 Compute Engine 3.0 上的 Managed Service for Apache Spark。

### 通过凭证分发进行配置

Managed Service for Apache Spark Trino 不支持凭据自动售卖。

### Apache Iceberg 1.10 或更高版本

开源 Apache Iceberg 1.10 及更高版本内置了对 `GoogleAuthManager` 中 Google 授权流的支持。以下示例展示了如何配置 Spark 以使用 Lakehouse 运行时目录 Apache Iceberg REST Catalog 端点。

```
import pyspark
from pyspark.context import SparkContext
from pyspark.sql import SparkSession

catalog_name = "CATALOG_NAME"
spark = SparkSession.builder.appName("APP_NAME") \
  .config(f'spark.sql.catalog.{catalog_name}', 'org.apache.iceberg.spark.SparkCatalog') \
  .config(f'spark.sql.catalog.{catalog_name}.type', 'rest') \
  .config(f'spark.sql.catalog.{catalog_name}.uri', 'https://biglake.googleapis.com/iceberg/REST_API_VERSION/restcatalog') \
  .config(f'spark.sql.catalog.{catalog_name}.warehouse', 'WAREHOUSE_PATH') \
  .config(f'spark.sql.catalog.{catalog_name}.header.x-goog-user-project', 'PROJECT_ID') \
  .config(f'spark.sql.catalog.{catalog_name}.rest.auth.type', 'org.apache.iceberg.gcp.auth.GoogleAuthManager') \
  .config(f'spark.sql.catalog.{catalog_name}.io-impl', 'org.apache.iceberg.gcp.gcs.GCSFileIO') \
  .config('spark.sql.extensions', 'org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions') \
  .config('spark.sql.defaultCatalog', 'CATALOG_NAME') \
  .getOrCreate()
```

替换以下内容：

* `CATALOG_NAME`：Apache Iceberg REST 目录端点的名称。
* `APP_NAME`：Spark 会话的名称。
* `REST_API_VERSION`：对于稳定的 API 版本，设置为 `v1`。如果需要解决数据沿袭生成方面的[已知问题](https://docs.cloud.google.com/dataproc/docs/guides/create-lakehouse?hl=zh-cn#lineage-known-issue)，请设置为 `v1beta`。
* `WAREHOUSE_PATH`：数据仓库的路径。
  使用 `gs://CLOUD_STORAGE_BUCKET_NAME`。如需使用 [BigQuery 目录联合](https://docs.cloud.google.com/lakehouse/docs/understand-catalog-types?hl=zh-cn#catalog-federation)，请参阅[将目录联合与 BigQuery 搭配使用](#federation)。
* `PROJECT_ID`：使用 Apache Iceberg REST Catalog 端点所产生的费用将计入该项目，该项目可能与拥有 Cloud Storage 存储桶的项目不同。如需详细了解使用 REST API 时的项目配置，请参阅[系统参数](https://docs.cloud.google.com/apis/docs/system-parameters?hl=zh-cn)。

### 通过凭证分发进行配置

上述示例未使用凭据自动售卖功能。如需使用凭据自动售卖，您必须使用[处于凭据自动售卖模式的目录](#create_a_catalog)，并将 `X-Iceberg-Access-Delegation` 标头添加到 Apache Iceberg REST 目录端点请求，其值为 `vended-credentials`，方法是将以下行添加到 `SparkSession` 构建器：

```
.config(f'spark.sql.catalog.{catalog_name}.header.X-Iceberg-Access-Delegation','vended-credentials')
```

#### 包含凭证分发的示例

以下示例使用凭据自动售卖功能配置查询引擎：

```
import pyspark
from pyspark.context import SparkContext
from pyspark.sql import SparkSession

catalog_name = "CATALOG_NAME"
spark = SparkSession.builder.appName("APP_NAME") \
  .config(f'spark.sql.catalog.{catalog_name}', 'org.apache.iceberg.spark.SparkCatalog') \
  .config(f'spark.sql.catalog.{catalog_name}.type', 'rest') \
  .config(f'spark.sql.catalog.{catalog_name}.uri', 'https://biglake.googleapis.com/iceberg/REST_API_VERSION/restcatalog') \
  .config(f'spark.sql.catalog.{catalog_name}.warehouse', 'gs://CLOUD_STORAGE_BUCKET_NAME') \
  .config(f'spark.sql.catalog.{catalog_name}.header.x-goog-user-project', 'PROJECT_ID') \
  .config(f'spark.sql.catalog.{catalog_name}.rest.auth.type', 'org.apache.iceberg.gcp.auth.GoogleAuthManager') \
  .config(f'spark.sql.catalog.{catalog_name}.io-impl', 'org.apache.iceberg.gcp.gcs.GCSFileIO') \
  .config(f'spark.sql.catalog.{catalog_name}.header.X-Iceberg-Access-Delegation','vended-credentials') \
  .config('spark.sql.extensions', 'org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions') \
  .config('spark.sql.defaultCatalog', 'CATALOG_NAME') \
  .getOrCreate()
```

如需了解详情，请参阅 Apache Iceberg 文档的 [`RESTCatalog`](https://py.iceberg.apache.org/configuration/#headers-in-rest-catalog) 部分中的“标头”。

### 之前的 Apache Iceberg 版本

对于 1.10 之前的开源 Apache Iceberg 版本，您可以通过配置具有以下内容的会话来配置标准 OAuth 身份验证：

```
import pyspark
from pyspark.context import SparkContext
from pyspark.sql import SparkSession

catalog_name = "CATALOG_NAME"
spark = SparkSession.builder.appName("APP_NAME") \
  .config('spark.jars.packages', 'org.apache.iceberg:iceberg-spark-runtime-3.5_2.12:1.9.1,org.apache.iceberg:iceberg-gcp-bundle:1.9.1') \
  .config(f'spark.sql.catalog.{catalog_name}', 'org.apache.iceberg.spark.SparkCatalog') \
  .config(f'spark.sql.catalog.{catalog_name}.type', 'rest') \
  .config(f'spark.sql.catalog.{catalog_name}.uri', 'https://biglake.googleapis.com/iceberg/REST_API_VERSION/restcatalog') \
  .config(f'spark.sql.catalog.{catalog_name}.warehouse', 'WAREHOUSE_PATH') \
  .config(f'spark.sql.catalog.{catalog_name}.header.x-goog-user-project', 'PROJECT_ID') \
  .config(f"spark.sql.catalog.{catalog_name}.token", "TOKEN") \
  .config(f"spark.sql.catalog.{catalog_name}.oauth2-server-uri", "https://oauth2.googleapis.com/token") \
  .config(f'spark.sql.catalog.{catalog_name}.io-impl', 'org.apache.iceberg.gcp.gcs.GCSFileIO') \
  .config('spark.sql.extensions', 'org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions') \
  .config('spark.sql.defaultCatalog', 'CATALOG_NAME') \
  .getOrCreate()
```

替换以下内容：

* `CATALOG_NAME`：Apache Iceberg REST 目录端点的名称。
* `APP_NAME`：Spark 会话的名称。
* `REST_API_VERSION`：对于稳定的 API 版本，设置为 `v1`。如果需要解决数据沿袭生成方面的[已知问题](https://docs.cloud.google.com/dataproc/docs/guides/create-lakehouse?hl=zh-cn#lineage-known-issue)，请设置为 `v1beta`。
* `WAREHOUSE_PATH`：数据仓库的路径。
  使用 `gs://CLOUD_STORAGE_BUCKET_NAME`。如需使用 [BigQuery 目录联合](https://docs.cloud.google.com/lakehouse/docs/understand-catalog-types?hl=zh-cn#catalog-federation)，请参阅[将目录联合与 BigQuery 搭配使用](#federation)。
* `PROJECT_ID`：使用 Apache Iceberg REST Catalog 端点所产生的费用将计入该项目，该项目可能与拥有 Cloud Storage 存储桶的项目不同。如需详细了解使用 REST API 时的项目配置，请参阅[系统参数](https://docs.cloud.google.com/apis/docs/system-parameters?hl=zh-cn)。
* `TOKEN`：您的身份验证令牌，有效期为一小时，例如使用 `gcloud auth application-default print-access-token` 生成的令牌。

### 通过凭证分发进行配置

上述示例未使用凭据自动售卖功能。如需使用凭据自动售卖，您必须使用[处于凭据自动售卖模式的目录](#create_a_catalog)，并将 `X-Iceberg-Access-Delegation` 标头添加到 Apache Iceberg REST 目录端点请求，其值为 `vended-credentials`，方法是将以下行添加到 `SparkSession` 构建器：

```
.config(f'spark.sql.catalog.{catalog_name}.header.X-Iceberg-Access-Delegation','vended-credentials')
```

#### 包含凭证分发的示例

以下示例使用凭据自动售卖功能配置查询引擎：

```
import pyspark
from pyspark.context import SparkContext
from pyspark.sql import SparkSession

catalog_name = "CATALOG_NAME"
spark = SparkSession.builder.appName("APP_NAME") \
  .config(f'spark.sql.catalog.{catalog_name}', 'org.apache.iceberg.spark.SparkCatalog') \
  .config(f'spark.sql.catalog.{catalog_name}.type', 'rest') \
  .config(f'spark.sql.catalog.{catalog_name}.uri', 'https://biglake.googleapis.com/iceberg/REST_API_VERSION/restcatalog') \
  .config(f'spark.sql.catalog.{catalog_name}.warehouse', 'gs://CLOUD_STORAGE_BUCKET_NAME') \
  .config(f'spark.sql.catalog.{catalog_name}.header.x-goog-user-project', 'PROJECT_ID') \
  .config(f"spark.sql.catalog.{catalog_name}.token", "TOKEN") \
  .config(f"spark.sql.catalog.{catalog_name}.oauth2-server-uri", "https://oauth2.googleapis.com/token") \
  .config(f'spark.sql.catalog.{catalog_name}.io-impl', 'org.apache.iceberg.gcp.gcs.GCSFileIO') \
  .config(f'spark.sql.catalog.{catalog_name}.header.X-Iceberg-Access-Delegation','vended-credentials') \
  .config('spark.sql.extensions', 'org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions') \
  .config('spark.sql.defaultCatalog', 'CATALOG_NAME') \
  .getOrCreate()
```

如需了解详情，请参阅 Apache Iceberg 文档的 [`RESTCatalog`](https://py.iceberg.apache.org/configuration/#headers-in-rest-catalog) 部分中的“标头”。

### 创建命名空间或架构

配置客户端后，请创建命名空间或架构来整理表。创建命名空间或架构的语法因查询引擎而异。以下示例展示了如何使用 Spark 和 Trino 创建它们。

**注意**： 如果您使用的是凭据自动售卖，请勿在其他命名空间或架构中创建命名空间或架构，因为这样做可能会授予用户对非预期资源的访问权限。

### Spark

#### Cloud Storage 数据仓库

```
spark.sql("CREATE NAMESPACE IF NOT EXISTS NAMESPACE_NAME;")
spark.sql("USE NAMESPACE_NAME;")
```

将 `NAMESPACE_NAME` 替换为您的命名空间的名称。

### Trino

#### Cloud Storage 数据仓库

```
CREATE SCHEMA IF NOT EXISTS  CATALOG_NAME.SCHEMA_NAME;
USE CATALOG_NAME.SCHEMA_NAME;
```

替换以下内容：

* `CATALOG_NAME`：使用 Apache Iceberg REST Catalog 端点的 Trino 目录的名称。
* `SCHEMA_NAME`：架构的名称。

## 在 BigQuery 中查询表

您在 BigQuery 中通过 Apache Iceberg REST 目录端点创建的表的查询方式取决于您使用的是 [Cloud Storage 存储桶数据仓库还是 BigQuery 联合查询](https://docs.cloud.google.com/lakehouse/docs/understand-catalog-types?hl=zh-cn#catalog-federation)。

* **Cloud Storage 存储桶仓库**：如果您使用 `gs://` 仓库路径配置了客户端，请使用四部分名称 (P.C.N.T) `project.catalog.namespace.table` 从 BigQuery 查询表。
  如需详细了解 P.C.N.T 结构，请参阅 [Iceberg REST 目录概念](https://docs.cloud.google.com/lakehouse/docs/understand-catalog-types?hl=zh-cn)。
  `catalog` 组件是 Lakehouse 运行时目录资源目录的名称。如需详细了解如何查询表，请参阅[查询表](https://docs.cloud.google.com/lakehouse/docs/lakehouse-iceberg-tables?hl=zh-cn#query_a_table)。
* **BigQuery 联邦**：如果您使用 `bq://` 仓库路径配置了客户端，则您创建的表会在 BigQuery 中显示，并且可以使用标准 BigQuery SQL 直接查询：

  ```
  SELECT * FROM `NAMESPACE_NAME.TABLE_NAME`;
  ```

  替换以下内容：

  + `NAMESPACE_NAME`：您的命名空间名称。
  + `TABLE_NAME`：表格的名称。

## 将目录联合与 BigQuery 配合使用

如需了解目录联合，请参阅 [Iceberg REST 目录概念](https://docs.cloud.google.com/lakehouse/docs/understand-catalog-types?hl=zh-cn)。如需启用联邦，请在[配置客户端应用](#configure-catalog)中的客户端配置示例中，将客户端配置为 `WAREHOUSE_PATH` 字段中的 `bq://projects/PROJECT_ID` 仓库格式。您还可以选择添加 BigQuery 位置，以使用 `bq://projects/PROJECT_ID/locations/LOCATION` 格式将未来的请求限制为单个位置。

由于这些资源由 BigQuery 管理，因此您必须拥有适用的[必需权限](https://docs.cloud.google.com/bigquery/docs/iceberg-tables?hl=zh-cn#required-roles)。

为联合配置客户端后，您可以为联合表创建命名空间。

### Spark

如需使用 BigQuery 目录联合，请添加 `LOCATION` 和 `DBPROPERTIES` 子句：

```
spark.sql("CREATE NAMESPACE IF NOT EXISTS NAMESPACE_NAME LOCATION 'gs://BUCKET_NAME/NAMESPACE_NAME' WITH DBPROPERTIES ('gcp-region' = 'LOCATION');")
spark.sql("USE NAMESPACE_NAME;")
```

替换以下内容：

* `NAMESPACE_NAME`：命名空间的名称。
* `BUCKET_NAME`：您在目录中使用的 Cloud Storage 存储桶。
* `LOCATION`：一个 [BigQuery 位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-cn)。默认值为 `US` 多区域。

### Trino

如需使用 BigQuery 目录联合，请添加 `LOCATION` 和 `gcp-region` 属性：

```
CREATE SCHEMA IF NOT EXISTS  CATALOG_NAME.SCHEMA_NAME WITH ( LOCATION = 'gs://BUCKET_NAME/SCHEMA_NAME', "gcp-region" = 'LOCATION');
USE CATALOG_NAME.SCHEMA_NAME;
```

替换以下内容：

* `CATALOG_NAME`：使用 Apache Iceberg REST Catalog 端点的 Trino 目录的名称。
* `SCHEMA_NAME`：架构的名称。
* `BUCKET_NAME`：您在目录中使用的 Cloud Storage 存储桶。
* `LOCATION`：一个 [BigQuery 位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-cn)。默认值为 `US` 多区域。

## 后续步骤

* 了解如何[查询表以及如何将目录联合与 BigQuery 结合使用](https://docs.cloud.google.com/lakehouse/docs/use-catalog-federation?hl=zh-cn)。
* 了解如何[在 Google Cloud 控制台中管理目录](https://docs.cloud.google.com/lakehouse/docs/lakehouse-console?hl=zh-cn)。
* 了解[适用于 Apache Iceberg 的 Lakehouse REST 目录表](https://docs.cloud.google.com/lakehouse/docs/lakehouse-iceberg-tables?hl=zh-cn)。




发送反馈

如未另行说明，那么本页面中的内容已根据[知识共享署名 4.0 许可](https://creativecommons.org/licenses/by/4.0/)获得了许可，并且代码示例已根据 [Apache 2.0 许可](https://www.apache.org/licenses/LICENSE-2.0)获得了许可。有关详情，请参阅 [Google 开发者网站政策](https://developers.google.com/site-policies?hl=zh-cn)。Java 是 Oracle 和/或其关联公司的注册商标。

最后更新时间 (UTC)：2026-05-16。




需要向我们提供更多信息？

[[["易于理解","easyToUnderstand","thumb-up"],["解决了我的问题","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["很难理解","hardToUnderstand","thumb-down"],["信息或示例代码不正确","incorrectInformationOrSampleCode","thumb-down"],["没有我需要的信息/示例","missingTheInformationSamplesINeed","thumb-down"],["翻译问题","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["最后更新时间 (UTC)：2026-05-16。"],[],[]]