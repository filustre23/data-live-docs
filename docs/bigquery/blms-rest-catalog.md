自 2026 年 4 月 20 日起，BigLake 现在称为 Lakehouse for Apache Iceberg。BigLake metastore 现已更名为 Lakehouse 运行时目录。Lakehouse API、客户端库、CLI 命令和 IAM 名称保持不变，仍引用 BigLake。

Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-cn)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-cn)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-cn)
* [Lakehouse](https://docs.cloud.google.com/lakehouse/docs?hl=zh-cn)

发送反馈

# 设置 Lakehouse Iceberg REST 目录端点 使用集合让一切井井有条 根据您的偏好保存内容并对其进行分类。

对于新目录，我们建议在 *Lakehouse 运行时目录*中使用 *Apache Iceberg REST 目录端点*。此端点基于开源 *Apache Iceberg REST Catalog API* 提供全代管式式标准化接口。

此端点充当单一可信来源，可在查询引擎之间实现无缝互操作性。它允许 Apache Spark 等引擎发现、读取和管理您的 Google Cloud Lakehouse 表。

如果您使用兼容的 OSS 或第三方引擎来访问 Cloud Storage 中的数据，并且需要与其他引擎（包括 BigQuery）实现互操作性，则此方法是不错的选择。它支持[凭据自动售卖](#create_a_catalog)等功能，可实现精细的访问权限控制，还支持[跨区域复制和灾难恢复](https://docs.cloud.google.com/lakehouse/docs/about-managed-disaster-recovery?hl=zh-cn)。

相比之下，[*适用于 BigQuery 的自定义 Apache Iceberg 目录*端点](https://docs.cloud.google.com/lakehouse/docs/configure-lakehouse-catalog-iceberg-1-10?hl=zh-cn)是较早的集成。虽然现有工作流可以继续使用它，但 REST 目录可提供更标准化且功能更丰富的体验。

## 准备工作

在继续操作之前，请先熟悉 [Lakehouse 运行时目录](https://docs.cloud.google.com/lakehouse/docs/about-lakehouse-catalogs?hl=zh-cn)和 [Iceberg REST 目录端点概览](https://docs.cloud.google.com/lakehouse/docs/understand-catalog-types?hl=zh-cn)。

如果您有现有的版本 1 (V1) Apache Iceberg 表，则必须先升级这些表，然后才能将它们与 Apache Iceberg REST 目录端点搭配使用。如需了解详情，请参阅[将 Iceberg V1 表升级到 V2](https://docs.cloud.google.com/lakehouse/docs/update-tables?hl=zh-cn)。

1. [验证是否已为您的 Google Cloud 项目启用结算功能](https://docs.cloud.google.com/billing/docs/how-to/verify-billing-enabled?hl=zh-cn#confirm_billing_is_enabled_on_a_project)。
2. 启用 BigLake API。

   **启用 API 所需的角色**

   如需启用 API，您需要拥有 `serviceusage.services.enable` 权限。如果您创建了项目，则可能已经通过 Owner 角色 (`roles/owner`) 获得了此权限。否则，您可以通过 Service Usage Admin 角色 (`roles/serviceusage.serviceUsageAdmin`) 获得此权限。[了解如何授予角色](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-cn)。

   [启用 API](https://console.cloud.google.com/apis/enableflow?apiid=biglake.googleapis.com&hl=zh-cn)

### 所需的角色

如需获得在 Lakehouse 运行时目录中使用 Apache Iceberg REST 目录端点所需的权限，请让管理员为您授予以下 IAM 角色：

* 执行管理任务，例如管理目录用户访问权限、存储访问权限和目录的凭证自动售卖模式：
  + 针对项目的 [BigLake Admin](https://docs.cloud.google.com/iam/docs/roles-permissions/biglake?hl=zh-cn#biglake.admin)  (`roles/biglake.admin`) 角色
  + 针对所有关联的 Cloud Storage 存储分区的 [Storage Admin](https://docs.cloud.google.com/iam/docs/roles-permissions/storage?hl=zh-cn#storage.admin)  (`roles/storage.admin`) 角色。
* 在 Lakehouse 目录中注册表：项目的 [BigLake Admin](https://docs.cloud.google.com/iam/docs/roles-permissions/biglake?hl=zh-cn#biglake.admin)  (`roles/biglake.admin`) 角色。
* 在凭据自动售卖模式下读取表数据：
  项目的 [BigLake Viewer](https://docs.cloud.google.com/iam/docs/roles-permissions/biglake?hl=zh-cn#biglake.viewer)  (`roles/biglake.viewer`) 角色。如果您使用 Managed Service for Apache Spark、Managed Service for Apache Spark 或 Dataflow 等查询引擎读取表数据，请向您用于在该引擎中运行作业的服务账号授予此角色。
* 以凭据自动售卖模式写入表数据：项目的 [BigLake Editor](https://docs.cloud.google.com/iam/docs/roles-permissions/biglake?hl=zh-cn#biglake.editor)  (`roles/biglake.editor`) 角色。如果您使用 Managed Service for Apache Spark、Managed Service for Apache Spark 或 Dataflow 等查询引擎来写入表数据，请向您用于在该引擎中运行作业的服务账号授予此角色。
* 在凭据贩售模式下使用自动预配的 Lakehouse 运行时目录服务账号：
  所有关联的 Cloud Storage 存储分区上的 [Storage Object User](https://docs.cloud.google.com/iam/docs/roles-permissions/storage?hl=zh-cn#storage.objectUser)  (`roles/storage.objectUser`)。创建目录后，请向目录的自动预配 Lakehouse 运行时目录服务账号明确授予所有关联存储分区的 Storage Object User 角色 (`roles/storage.objectUser`)。
* 在非凭证自动售卖模式下读取目录资源和表数据：
  + 项目的 [BigLake Viewer](https://docs.cloud.google.com/iam/docs/roles-permissions/biglake?hl=zh-cn#biglake.viewer)  (`roles/biglake.viewer`) 角色
  + [Storage Object Viewer](https://docs.cloud.google.com/iam/docs/roles-permissions/storage?hl=zh-cn#storage.objectViewer)  (`roles/storage.objectViewer`) 角色，适用于所有关联的 Cloud Storage 存储分区。
* 在非凭证自动售卖模式下管理目录资源和写入表数据：
  + 项目的 [BigLake Editor](https://docs.cloud.google.com/iam/docs/roles-permissions/biglake?hl=zh-cn#biglake.editor)  (`roles/biglake.editor`) 角色
  + 针对所有关联的 Cloud Storage 存储分区的 [Storage Object User](https://docs.cloud.google.com/iam/docs/roles-permissions/storage?hl=zh-cn#storage.objectUser)  (`roles/storage.objectUser`) 角色。

如需详细了解如何授予角色，请参阅[管理对项目、文件夹和组织的访问权限](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-cn)。

您也可以通过[自定义角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-cn)或其他[预定义角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-cn#predefined)来获取所需的权限。

## 限制

Apache Iceberg REST 目录端点受以下限制：

**一般限制**

* 支持 Apache Iceberg V2 表（正式版）和 V3 表（预览版）。不支持 Iceberg V1 表。在使用 Apache Iceberg REST 目录端点处理现有 V1 表之前，您必须将这些表升级到受支持的版本。
* 使用凭据贩售模式时，如果查询引擎允许您为目录连接设置 `io-impl` 属性，则必须将其设置为 `org.apache.iceberg.gcp.gcs.GCSFileIO`。
* 目前，凭据贩售模式不支持[分层命名空间](https://docs.cloud.google.com/storage/docs/hns-overview?hl=zh-cn)存储分区。

**表格限制**

* 您无法使用 BigQuery 数据定义语言 (DDL) 或数据操纵语言 (DML) 语句在 Apache Iceberg REST 目录端点中创建或修改表。您可以使用 BigQuery API（通过 bq 命令行工具或客户端库）修改这些表，但这样做可能会导致更改与外部引擎不兼容。
* 通过 Apache Iceberg REST 目录端点管理的表不支持精细访问权限控制 (FGAC)，例如行级和列级安全性。
* 禁止将 Iceberg 表属性 `write.data.path` 或 `write.metadata.path` 设置为非默认值。
* 表路径必须嵌套在父命名空间路径（例如 `gs://{namespace_path}/.../{table_name}`）内。为防止冲突并提高安全性，系统会自动在生成的位置附加随机字符串后缀（例如 `gs://{namespace_path}/{table_name}/{random_suffix}`）。

**数据限制**

* 仅支持 Parquet 文件。如需详细了解 BigQuery 如何处理 Parquet 文件，请参阅[从 Cloud Storage 加载 Parquet 数据](https://docs.cloud.google.com/bigquery/docs/loading-data-cloud-storage-parquet?hl=zh-cn)。
* Iceberg `metadata.json` 文件大小上限为 1MB。如需申请提高此限制，请与您的 Google 客户支持团队联系。

**查询限制**

* 在 BigQuery 中，无法使用五部分名称标识符查询 Apache Iceberg 元数据表（例如 `.snapshots` 或 `.files`）；您可以使用 Spark 查询这些表。

## 注意事项

创建目录时，请考虑以下配置。

#### 存储桶类型

您可以选择创建单存储桶目录或多存储桶目录。

* **多存储桶 (`bl://`) 目录（推荐）**：此配置可让您的目录关联多个存储桶，并让您独立于任何存储桶名称来命名目录。
* **单存储桶 (`gs://`)**：此配置会将目录限制为单个存储桶，并将目录名称锁定为存储桶名称。不建议用于新项目。

#### 凭据模式（范围）

您可以创建使用最终用户凭据或[凭据贩售模式](https://docs.cloud.google.com/lakehouse/docs/understand-catalog-types?hl=zh-cn#storage-single-bucket)的目录。

* **最终用户凭据**：目录会将访问它的最终用户的身份传递给 Cloud Storage 以进行授权检查。
* **凭据自动售卖模式**：一种存储访问权限委托机制，可让 Lakehouse 运行时目录管理员直接控制 Lakehouse 运行时目录资源的权限，从而无需目录用户直接访问 Cloud Storage 存储分区。借助此功能，Google Cloud 的*Lakehouse*管理员可以向用户授予对特定数据文件的权限。

  自动预配的 Lakehouse 运行时目录服务账号需要对所有关联的 Cloud Storage 存储分区具有明确的 Storage Object User 角色 (`roles/storage.objectUser`)。默认情况下，它没有任何访问权限。
  如果没有此角色，出售的凭据将没有足够的范围来执行存储写入操作。如果您使用 `gcloud` 或 Terraform 等工具，则必须手动授予此角色。

  自动配置的目录服务账号的创建是[最终一致的](https://wikipedia.org/wiki/Eventual_consistency)。
  这意味着服务账号需要一段时间才能在整个系统中生效。如果您尝试在创建服务账号后立即向其授予角色，则请求可能会失败。如需了解访问权限更改传播的平均时间，请参阅[访问权限更改传播](https://docs.cloud.google.com/iam/docs/access-change-propagation?hl=zh-cn)。

#### 位置

在创建目录之前，请先熟悉[位置要求](https://docs.cloud.google.com/lakehouse/docs/understand-catalog-types?hl=zh-cn#bucket_and_catalog_regions)。

* 创建命名空间时，系统会自动使用与目录相同的区域。
* 如果您的目录使用多区域存储桶，并且您想将其与 BigQuery 多区域（`US` 或 `EU`）搭配使用，则必须删除并重新创建目录，以指定主要位置。

## 设置 Iceberg REST Catalog 端点

在设置目录之前，建议您先阅读 [Apache Iceberg REST 目录端点概览](https://docs.cloud.google.com/lakehouse/docs/understand-catalog-types?hl=zh-cn)，了解其资源层次结构、目录类型和命名结构。

在 Lakehouse 运行时目录中使用 Apache Iceberg REST 目录端点时，一般需要遵循以下步骤：

1. 选择目录类型 - [多存储桶 (`bl://`)](https://docs.cloud.google.com/lakehouse/docs/understand-catalog-types?hl=zh-cn#storage-multiple-buckets) 目录（推荐）或[单存储桶 (`gs://`)](https://docs.cloud.google.com/lakehouse/docs/understand-catalog-types?hl=zh-cn#storage-single-bucket) 目录。
2. 创建指向仓库位置的目录。
3. 将客户端应用配置为使用 Apache Iceberg REST 目录端点。
4. 创建命名空间或架构来整理表。
5. 使用配置的客户端创建和查询表。

### 创建目录

请按照以下步骤根据您的首选凭据模式和存储桶类型创建目录。

### 控制台

**创建多存储桶 (`bl://`) 目录（推荐）**

通过此配置，您的目录可以关联多个存储桶，并且您可以独立于任何存储桶名称来命名目录。

1. 在 Google Cloud 控制台中打开 **Lakehouse** 页面。

   [前往 Lakehouse](https://console.cloud.google.com/biglake?hl=zh-cn)
2. 点击**创建目录**。
3. 对于**目录类型**，选择 **Iceberg Rest 目录**。
4. 对于 **Lakehouse 目录存储桶选项**，选择**多存储桶目录**。
5. 对于**默认目录 Cloud Storage 路径**，请输入或浏览要与目录搭配使用的 Cloud Storage 路径。
6. 在**目录 ID** 字段中，输入目录的自定义名称。
7. 对于**主要位置**，选择一个位置。位置必须靠近主存储桶的区域。
8. 点击**继续**。
9. 在**数据路径**这一步中，根据需要添加其他 Cloud Storage 路径。
10. 点击**继续**。
11. 对于**身份验证方法**，请选择**最终用户凭证**或**凭证分发模式**。
12. 点击**创建**。

    系统会创建您的目录，并打开**目录详情**页面。
13. 如果您选择了**凭据自动售卖模式**，请执行以下额外步骤：

    1. 在**身份验证方法**下，点击**设置存储桶权限**。
    2. 在对话框中，点击**确认**。

#### 创建单存储桶 (`gs://`) 目录

**注意**：强烈建议新项目不要使用单存储桶配置。此配置会将目录限制为单个存储桶，并将目录名称锁定为存储桶名称。

1. 对于**目录类型**，选择 **Iceberg Rest 目录**。
2. 对于 **Lakehouse 目录存储桶选项**，选择**单个存储桶目录**。
3. 对于**默认目录 Cloud Storage 路径**，请输入或浏览要与目录搭配使用的 Cloud Storage 路径。
   （对于单存储桶 (`gs://`) 目录，每个存储桶只能有一个目录，且目录名称与存储桶名称一致）。
4. 点击**继续**。
5. 对于**身份验证方法**，请选择**最终用户凭证**或**凭证分发模式**。
6. 点击**创建**。
7. 如果您选择了**凭据自动售卖模式**，请执行以下额外步骤：
   1. 在**身份验证方法**下，点击**设置存储桶权限**。
   2. 在对话框中，点击**确认**。

### gcloud

**创建多存储桶 (`bl://`) 目录（推荐）**

通过此配置，您的目录可以关联多个存储桶，并且您可以独立于任何存储桶名称来命名目录。

如需创建多存储桶 (`bl://`) 目录（推荐），请运行 [`gcloud biglake iceberg catalogs create`](https://docs.cloud.google.com/sdk/gcloud/reference/biglake/iceberg/catalogs/create?hl=zh-cn) 命令。

```
gcloud biglake iceberg catalogs create \
    CATALOG_NAME \
    --project PROJECT_ID \
    --catalog-type biglake \
    --default-location DEFAULT_LOCATION \
    --credential-mode CREDENTIAL_MODE \
    [--restricted-locations RESTRICTED_LOCATIONS] \
    [--primary-location LOCATION]
```

替换以下内容：

* `CATALOG_NAME`：目录的名称。对于多存储桶 (`bl://`) 目录（推荐），这是您的自定义目录名称。对于单存储桶 (`gs://`) 目录，此值与 REST 目录使用的 Cloud Storage 存储桶 ID 相匹配。
* `PROJECT_ID`： Google Cloud项目 ID。
* `DEFAULT_LOCATION`：指定目录的默认存储位置。您可以指定存储桶 (`gs://my-bucket`) 或子路径 (`gs://my-bucket/path`)。目录中的所有命名空间和表都必须位于指定路径下。例如，如果您指定 `gs://my-bucket/path`，则无法在 `gs://my-bucket/another/path` 下创建命名空间或表。
* `CREDENTIAL_MODE`：身份验证方法。使用 `end-user` 获取*最终用户凭证*，或使用 `vended-credentials` 获取*凭证分发模式*。

  **注意**：如果您使用*凭据自动售卖模式*，则必须向目录的自动预配 Lakehouse 运行时目录服务账号明确授予所有关联存储分区的*存储对象用户*角色 (`roles/storage.objectUser`)。
* `RESTRICTED_LOCATIONS`：（可选）以英文逗号分隔的其他允许的存储位置列表，格式为 `gs://my-bucket-1/...,gs://my-bucket-2/...`。如果您指定了路径（例如 `gs://my-bucket/path`），则相应存储桶中的任何命名空间或表都必须位于该路径下。默认位置和受限位置的所有已配置的 Cloud Storage 位置都必须位于同一地理区域组或管辖区（例如美国、欧洲、加拿大或亚洲）。例如，您不能将美国境内的存储桶与欧洲境内的存储桶混用。如需查看受支持位置的列表，请参阅 [Lakehouse 位置](https://docs.cloud.google.com/lakehouse/docs/locations?hl=zh-cn)。

  **警告**：请避免配置与其他目录重叠的路径，以防止未经授权的凭据泄露。如需了解详情，请参阅[跨多个存储分区的存储](https://docs.cloud.google.com/lakehouse/docs/understand-catalog-types?hl=zh-cn#storage-multiple-buckets)。
* `LOCATION`：（可选）目录的主区域，用于确保与 BigQuery 的互操作性。对于美国区域（例如 `US` 或 `us-central1`）或欧盟区域（例如 `EU` 或 `europe-west4`）中的 Cloud Storage 存储分区，请分别指定 `US` 或 `EU`，以确保目录可供相应 BigQuery 多区域位置查询。如需了解详情，请参阅[存储分区和目录区域](https://docs.cloud.google.com/lakehouse/docs/understand-catalog-types?hl=zh-cn#bucket_and_catalog_regions)。

#### 创建单存储桶 (`gs://`) 目录

**注意**：强烈建议新项目不要使用单存储桶配置。此配置会将目录限制为单个存储桶，并将目录名称锁定为存储桶名称。

如需创建单存储桶 (`gs://`) 目录，请运行以下命令：

```
gcloud biglake iceberg catalogs create \
    CATALOG_NAME \
    --project PROJECT_ID \
    --catalog-type gcs-bucket \
    --credential-mode CREDENTIAL_MODE
```

替换以下内容：

* `CATALOG_NAME`：目录的名称。对于多存储桶 (`bl://`) 目录（推荐），这是您的自定义目录名称。对于单存储桶 (`gs://`) 目录，此值与 REST 目录使用的 Cloud Storage 存储桶 ID 相匹配。
* `PROJECT_ID`：您的 Google Cloud项目 ID。
* `CREDENTIAL_MODE`：身份验证方法。使用 `end-user` 获取*最终用户凭证*，或使用 `vended-credentials` 获取*凭证分发模式*。

### 配置客户端应用

创建目录后，请配置客户端应用以使用该目录。这些示例展示了如何配置凭据自动售卖功能（有或没有）。

### 集群

使用简化的配置属性（推荐）或手动指定属性，在 Compute Engine 集群上创建 Managed Service for Apache Spark。

#### 使用属性简化配置（推荐）

创建具有目录资源的集群：

```
gcloud dataproc clusters create CLUSTER_NAME \
  --enable-component-gateway \
  --project=PROJECT_ID \
  --region=REGION \
  --optional-components=ICEBERG \
  --image-version=DATAPROC_VERSION \
  --properties="dataproc.lakehouse.catalog.CATALOG_NAME=projects/PROJECT_ID/catalogs/CATALOG_ID"
```

替换以下内容：

* `CLUSTER_NAME`：集群的名称。
* `PROJECT_ID`：您的 Google Cloud 项目 ID。
* `REGION`：Managed Service for Apache Spark 集群区域。
* `DATAPROC_VERSION`：Managed Service for Apache Spark 映像版本，例如 `2.3`。
* `CATALOG_NAME`：本地 Spark 目录的名称（例如 `my_catalog`）。它可以与 `CATALOG_ID` 相同。
* `CATALOG_ID`：您创建的目录的 ID。

**注意**： 您可以在 `--properties` 标志中配置多个目录，只需用英文逗号分隔即可。例如：
`--properties="dataproc.lakehouse.catalog.CATALOG_NAME_1=projects/PROJECT_ID_1/catalogs/CATALOG_ID_1,dataproc.lakehouse.catalog.CATALOG_NAME_2=projects/PROJECT_ID_2/catalogs/CATALOG_ID_2"`

在 PySpark 应用文件中，创建 `SparkSession`，但不指定目录配置：

```
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("APP_NAME").getOrCreate()
```

#### 手动配置

如果您不使用简化的配置属性，请按照上述说明创建集群，但不要使用 `--properties` 标志。然后，手动配置 `SparkSession`：

```
import pyspark
from pyspark.context import SparkContext
from pyspark.sql import SparkSession

catalog_name = "CATALOG_NAME"
spark = SparkSession.builder.appName("APP_NAME") \
  .config('spark.sql.defaultCatalog', 'CATALOG_NAME') \
  .config(f'spark.sql.catalog.{catalog_name}', 'org.apache.iceberg.spark.SparkCatalog') \
  .config(f'spark.sql.catalog.{catalog_name}.type', 'rest') \
  .config(f'spark.sql.catalog.{catalog_name}.uri', 'https://biglake.googleapis.com/iceberg/REST_API_VERSION/restcatalog') \
  .config(f'spark.sql.catalog.{catalog_name}.warehouse', 'WAREHOUSE_PATH') \
  .config(f'spark.sql.catalog.{catalog_name}.header.x-goog-user-project', 'PROJECT_ID') \
  .config(f'spark.sql.catalog.{catalog_name}.rest.auth.type', 'org.apache.iceberg.gcp.auth.GoogleAuthManager') \
  .config(f'spark.sql.catalog.{catalog_name}.io-impl', 'org.apache.iceberg.gcp.gcs.GCSFileIO') \
  .config('spark.sql.extensions', 'org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions') \
  .getOrCreate()
```

替换以下内容：

* `CATALOG_NAME`：本地 Spark 目录的名称（例如 `my_catalog`）。
* `APP_NAME`：Spark 会话的名称。
* `REST_API_VERSION`：对于稳定的 API 版本，设置为 `v1`。
* `WAREHOUSE_PATH`：仓库的路径。对于 BigLake 目录，请使用 `bl://projects/PROJECT_ID/catalogs/CATALOG_ID`。
  对于 Cloud Storage 存储桶目录，请使用 `gs://CLOUD_STORAGE_BUCKET_NAME`。
* `PROJECT_ID`：使用 Apache Iceberg REST 目录端点所产生的费用将计入该项目，该项目可能与拥有 Cloud Storage 存储桶的项目不同。如需详细了解使用 REST API 时的项目配置，请参阅[系统参数](https://docs.cloud.google.com/apis/docs/system-parameters?hl=zh-cn)。

### 通过凭证分发进行配置

如需使用凭据自动售卖，您必须使用[处于凭据自动售卖模式的目录](#create_a_catalog)，并向 Iceberg REST 目录请求添加 `X-Iceberg-Access-Delegation` 标头，其值为 `vended-credentials`，方法是在 `SparkSession` build 中添加以下行：

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
  .config('spark.sql.defaultCatalog', 'CATALOG_NAME') \
  .config(f'spark.sql.catalog.{catalog_name}', 'org.apache.iceberg.spark.SparkCatalog') \
  .config(f'spark.sql.catalog.{catalog_name}.type', 'rest') \
  .config(f'spark.sql.catalog.{catalog_name}.uri', 'https://biglake.googleapis.com/iceberg/REST_API_VERSION/restcatalog') \
  .config(f'spark.sql.catalog.{catalog_name}.warehouse', 'WAREHOUSE_PATH') \
  .config(f'spark.sql.catalog.{catalog_name}.header.x-goog-user-project', 'PROJECT_ID') \
  .config(f'spark.sql.catalog.{catalog_name}.rest.auth.type', 'org.apache.iceberg.gcp.auth.GoogleAuthManager') \
  .config(f'spark.sql.catalog.{catalog_name}.io-impl', 'org.apache.iceberg.gcp.gcs.GCSFileIO') \
  .config(f'spark.sql.catalog.{catalog_name}.header.X-Iceberg-Access-Delegation','vended-credentials') \
  .config('spark.sql.extensions', 'org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions') \
  .getOrCreate()
```

如需了解详情，请参阅 Apache Iceberg 文档的 [`RESTCatalog`](https://py.iceberg.apache.org/configuration/#headers-in-rest-catalog) 部分中的“标头”。

Managed Service for Apache Spark 集群在以下版本中支持 Apache Iceberg 的 Google 授权流程：

* Managed Service for Apache Spark on Compute Engine 2.2 映像版本 2.2.65 及更高版本。
* Compute Engine 2.3 上的 Managed Service for Apache Spark 映像版本 2.3.11 及更高版本。

### 无服务器

使用简化的配置属性（推荐）或手动指定属性，向 Managed Service for Apache Spark 提交 [PySpark 批量工作负载](https://docs.cloud.google.com/dataproc-serverless/docs/quickstarts/spark-batch?hl=zh-cn#submit_a_spark_batch_workload)。

#### 使用属性简化配置（推荐）

提交包含目录资源的批量作业：

```
gcloud dataproc batches submit pyspark PYSPARK_FILE \
    --project=PROJECT_ID \
    --region=REGION \
    --version=RUNTIME_VERSION \
    --properties="dataproc.lakehouse.catalog.CATALOG_NAME=projects/PROJECT_ID/catalogs/CATALOG_ID"
```

替换以下内容：

* `PYSPARK_FILE`：PySpark 应用文件的 `gs://` Cloud Storage 路径。
* `PROJECT_ID`：您的 Google Cloud 项目 ID。
* `REGION`：Managed Service for Apache Spark 批量工作负载的区域。
* `RUNTIME_VERSION`：Managed Service for Apache Spark 运行时版本，例如 `2.3`。
* `CATALOG_NAME`：本地 Spark 目录的名称（例如 `my_catalog`）。它可以与 `CATALOG_ID` 相同。
* `CATALOG_ID`：您创建的目录的 ID。

**注意**： 您可以在 `--properties` 标志中配置多个目录，只需用英文逗号分隔即可。例如：
`--properties="dataproc.lakehouse.catalog.CATALOG_NAME_1=projects/PROJECT_ID_1/catalogs/CATALOG_ID_1,dataproc.lakehouse.catalog.CATALOG_NAME_2=projects/PROJECT_ID_2/catalogs/CATALOG_ID_2"`

在 PySpark 应用文件中，创建 `SparkSession`，但不指定目录配置：

```
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("APP_NAME").getOrCreate()
```

#### 手动配置

如果您不使用简化的配置属性，则必须手动指定目录配置：

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
    spark.sql.catalog.CATALOG_NAME.header.x-goog-user-project=PROJECT_ID,\
    spark.sql.catalog.CATALOG_NAME.rest.auth.type=org.apache.iceberg.gcp.auth.GoogleAuthManager,\
    spark.sql.catalog.CATALOG_NAME.io-impl=org.apache.iceberg.gcp.gcs.GCSFileIO,\
    spark.sql.extensions=org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions"
```

替换以下内容：

* `PYSPARK_FILE`：PySpark 应用文件的 `gs://` Cloud Storage 路径。
* `REGION`：Managed Service for Apache Spark 批量工作负载的区域。
* `RUNTIME_VERSION`：Managed Service for Apache Spark 运行时版本，例如 `2.3`。
* `CATALOG_NAME`：本地 Spark 目录的名称（例如 `my_catalog`）。
* `REST_API_VERSION`：对于稳定的 API 版本，设置为 `v1`。
* `WAREHOUSE_PATH`：仓库的路径。对于 BigLake 目录，请使用 `bl://projects/PROJECT_ID/catalogs/CATALOG_ID`。
  对于 Cloud Storage 存储桶目录，请使用 `gs://CLOUD_STORAGE_BUCKET_NAME`。
* `PROJECT_ID`：使用 Apache Iceberg REST 目录端点所产生的费用将计入该项目，该项目可能与拥有 Cloud Storage 存储桶的项目不同。如需详细了解使用 REST API 时的项目配置，请参阅[系统参数](https://docs.cloud.google.com/apis/docs/system-parameters?hl=zh-cn)。

### 通过凭证分发进行配置

如需使用凭据自动售卖，您必须使用[处于凭据自动售卖模式的目录](#create_a_catalog)，并将 `X-Iceberg-Access-Delegation` 标头添加到 Apache Iceberg REST Catalog 端点请求，其值为 `vended-credentials`，方法是在 Managed Service for Apache Spark 配置中添加以下行：

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
    spark.sql.catalog.CATALOG_NAME.warehouse=WAREHOUSE_PATH,\
    spark.sql.catalog.CATALOG_NAME.header.x-goog-user-project=PROJECT_ID,\
    spark.sql.catalog.CATALOG_NAME.rest.auth.type=org.apache.iceberg.gcp.auth.GoogleAuthManager,\
    spark.sql.catalog.CATALOG_NAME.io-impl=org.apache.iceberg.gcp.gcs.GCSFileIO,\
    spark.sql.catalog.CATALOG_NAME.header.X-Iceberg-Access-Delegation=vended-credentials,\"
    spark.sql.extensions=org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions
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
* `CATALOG_NAME`：使用 Apache Iceberg REST Catalog 端点的 Trino Catalog 的名称。
* `REST_API_VERSION`：对于稳定的 API 版本，设置为 `v1`。
* `WAREHOUSE_PATH`：仓库的路径。对于 BigLake 目录，请使用 `bl://projects/PROJECT_ID/catalogs/CATALOG_ID`。
  对于 Cloud Storage 存储桶目录，请使用 `gs://CLOUD_STORAGE_BUCKET_NAME`。
* `PROJECT_ID`：用于 Lakehouse 运行时目录的 Google Cloud 项目 ID。

创建集群后，连接到主虚拟机实例，然后使用 Trino CLI：

```
trino --catalog=CATALOG_NAME
```

Managed Service for Apache Spark Trino 在以下版本中支持 Apache Iceberg 的 Google 授权流程：

* Managed Service for Apache Spark on Compute Engine 2.2 运行时版本 2.2.65 及更高版本
* Managed Service for Apache Spark on Compute Engine 2.3 运行时版本 2.3.11 及更高版本
* 不支持 Compute Engine 3.0 上的 Managed Service for Apache Spark。

### 通过凭证分发进行配置

凭据贩售仅在 Trino 版本 481 及更高版本中受支持。

### Apache Iceberg 1.10 或更高版本

开源 Apache Iceberg 1.10 及更高版本内置了对 `GoogleAuthManager` 中 Google 授权流的支持。以下示例展示了如何配置 Spark 以使用 Apache Iceberg REST Catalog 端点。

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

* `CATALOG_NAME`：本地 Spark 目录的名称（例如 `my_catalog`）。
* `APP_NAME`：Spark 会话的名称。
* `REST_API_VERSION`：对于稳定的 API 版本，设置为 `v1`。
* `WAREHOUSE_PATH`：仓库的路径。对于 BigLake 目录，请使用 `bl://projects/PROJECT_ID/catalogs/CATALOG_ID`。
  对于 Cloud Storage 存储桶目录，请使用 `gs://CLOUD_STORAGE_BUCKET_NAME`。
* `PROJECT_ID`：使用 Apache Iceberg REST 目录端点所产生的费用将计入该项目，该项目可能与拥有 Cloud Storage 存储桶的项目不同。如需详细了解使用 REST API 时的项目配置，请参阅[系统参数](https://docs.cloud.google.com/apis/docs/system-parameters?hl=zh-cn)。

### 通过凭证分发进行配置

上述示例未使用凭据自动售卖功能。如需使用凭据自动售卖，您必须使用[处于凭据自动售卖模式的目录](#create_a_catalog)，并将 `X-Iceberg-Access-Delegation` 标头添加到 Apache Iceberg REST Catalog 端点请求，其值为 `vended-credentials`，方法是将以下行添加到 `SparkSession` 构建器：

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
  .config(f'spark.sql.catalog.{catalog_name}.warehouse', 'WAREHOUSE_PATH') \
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

* `CATALOG_NAME`：本地 Spark 目录的名称（例如 `my_catalog`）。
* `APP_NAME`：Spark 会话的名称。
* `REST_API_VERSION`：对于稳定的 API 版本，设置为 `v1`。
* `WAREHOUSE_PATH`：仓库的路径。对于 BigLake 目录，请使用 `bl://projects/PROJECT_ID/catalogs/CATALOG_ID`。
  对于 Cloud Storage 存储桶目录，请使用 `gs://CLOUD_STORAGE_BUCKET_NAME`。
* `PROJECT_ID`：使用 Apache Iceberg REST 目录端点所产生的费用将计入该项目，该项目可能与拥有 Cloud Storage 存储桶的项目不同。如需详细了解使用 REST API 时的项目配置，请参阅[系统参数](https://docs.cloud.google.com/apis/docs/system-parameters?hl=zh-cn)。
* `TOKEN`：您的身份验证令牌，有效期为一小时，例如使用 `gcloud auth application-default print-access-token` 生成的令牌。

### 通过凭证分发进行配置

上述示例未使用凭据自动售卖功能。如需使用凭据自动售卖，您必须使用[处于凭据自动售卖模式的目录](#create_a_catalog)，并将 `X-Iceberg-Access-Delegation` 标头添加到 Apache Iceberg REST Catalog 端点请求，其值为 `vended-credentials`，方法是将以下行添加到 `SparkSession` 构建器：

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
  .config(f'spark.sql.catalog.{catalog_name}.warehouse', 'WAREHOUSE_PATH') \
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

### 控制台

1. 在 Google Cloud 控制台中，前往 **Lakehouse**。

   [前往 Lakehouse](https://console.cloud.google.com/biglake?hl=zh-cn)
2. 选择现有目录，如果没有，则创建一个目录。
3. 在菜单栏中，点击 **+ 创建命名空间**。
4. 对于**命名空间名称**，为您的命名空间输入一个唯一的名称。
5. 对于**位置**，指定要与您的命名空间关联的路径：

   * **多存储桶 (`bl://`)**（推荐）：您可以设置任何自定义位置，只要该位置位于目录允许的位置（`default_location` 或 `restricted_locations`）下即可。如果您未指定位置，系统会在目录的默认位置（例如 `gs://{path-to-default-location}/{namespace_name}`）下创建命名空间。
   * **单存储桶 (`gs://`)**：命名空间位置会自动从目录的单个存储桶继承。
6. 点击**创建**。

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

* `CATALOG_NAME`：使用 Apache Iceberg REST Catalog 端点的 Trino Catalog 的名称。
* `SCHEMA_NAME`：架构的名称。

## 升级目录

如果您有现有的单存储桶 (`gs://`) 目录，可以将其升级为多存储桶 (`bl://`) 目录类型（推荐）。升级后，您可以关联多个存储分区并配置受限位置，同时保留原始目录名称。

如需升级目录，请参阅[更新目录](https://docs.cloud.google.com/lakehouse/docs/update-catalog?hl=zh-cn)。

## 后续步骤

* 了解如何[在 Google Cloud 控制台中管理目录](https://docs.cloud.google.com/lakehouse/docs/lakehouse-console?hl=zh-cn)。
* 了解 [Lakehouse REST 目录表（适用于 Apache Iceberg）](https://docs.cloud.google.com/lakehouse/docs/lakehouse-iceberg-tables?hl=zh-cn)。




发送反馈

如未另行说明，那么本页面中的内容已根据[知识共享署名 4.0 许可](https://creativecommons.org/licenses/by/4.0/)获得了许可，并且代码示例已根据 [Apache 2.0 许可](https://www.apache.org/licenses/LICENSE-2.0)获得了许可。有关详情，请参阅 [Google 开发者网站政策](https://developers.google.com/site-policies?hl=zh-cn)。Java 是 Oracle 和/或其关联公司的注册商标。

最后更新时间 (UTC)：2026-07-18。




需要向我们提供更多信息？

[[["易于理解","easyToUnderstand","thumb-up"],["解决了我的问题","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["很难理解","hardToUnderstand","thumb-down"],["信息或示例代码不正确","incorrectInformationOrSampleCode","thumb-down"],["没有我需要的信息/示例","missingTheInformationSamplesINeed","thumb-down"],["翻译问题","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["最后更新时间 (UTC)：2026-07-18。"],[],[]]