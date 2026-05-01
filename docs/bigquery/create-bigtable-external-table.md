* [Home](https://docs.cloud.google.com/?hl=zh-cn)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-cn)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-cn)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-cn)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-cn)

发送反馈



使用集合让一切井井有条

根据您的偏好保存内容并对其进行分类。

# 创建 Bigtable 外部表

本页面介绍如何创建 BigQuery 永久外部表，该表可用于查询存储在 Bigtable 中的数据。您可以在所有 [Bigtable 位置](https://docs.cloud.google.com/bigtable/docs/locations?hl=zh-cn)查询 Bigtable 中的数据。

## 准备工作

在创建外部表之前，请收集一些信息并确保您有权创建该表。

### 所需的角色

如需创建用于查询 Bigtable 数据的外部表，您必须是包含源表的实例的 Bigtable Admin (`roles/bigtable.admin`) 角色中的主账号。

您还需要 `bigquery.tables.create` BigQuery Identity and Access Management (IAM) 权限。

以下每个预定义的 Identity and Access Management 角色都具有此权限：

* BigQuery Data Editor (`roles/bigquery.dataEditor`)
* BigQuery Data Owner (`roles/bigquery.dataOwner`)
* BigQuery Admin (`roles/bigquery.admin`)

如果您不是这些角色中的主账号，请让您的管理员授予您访问权限或为您创建外部表。

如需详细了解 BigQuery 中的 Identity and Access Management 角色和权限，请参阅[预定义的角色和权限](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-cn)。如需查看有关 Bigtable 权限的信息，请参阅[使用 Identity and Access Management 进行访问权限控制](https://docs.cloud.google.com/bigtable/docs/access-control?hl=zh-cn)。如需查看查询外部表所需的角色，请参阅[查询 Bigtable 数据](https://docs.cloud.google.com/bigquery/docs/external-data-bigtable?hl=zh-cn)。

### 创建或标识数据集

创建外部表之前，必须先[创建数据集](https://docs.cloud.google.com/bigquery/docs/datasets?hl=zh-cn)来存放该外部表。您也可以使用现有数据集。

### 规划计算用量

**预览版**

此产品或功能 受[服务专用条款](https://docs.cloud.google.com/terms/service-terms?hl=zh-cn#1)的约束。
非正式版产品和功能“按原样”提供，可能只能获得有限的支持。
如需了解详情，请参阅[发布阶段说明](https://cloud.google.com/products/?hl=zh-cn#product-launch-stages)。

确定在查询数据时要使用的计算类型。您可以在[应用配置文件设置](#app-profile)中指定要使用 Data Boost，或者要路由到专用集群。

#### Data Boost

为避免影响应用处理流量，您可以在使用 BigQuery 外部表读取 Bigtable 数据时使用 Data Boost 无服务器计算。如需使用 Data Boost，您必须使用 Data Boost 应用配置文件，并在编写 Bigtable URI 时添加应用配置文件 ID。如需详细了解 Data Boost，请参阅 [Bigtable Data Boost 概览](https://docs.cloud.google.com/bigtable/docs/data-boost-overview?hl=zh-cn)。

#### 预配的节点

如果您不使用 Data Boost，则集群节点用于计算。

如果您不使用 Data Boost，并且计划经常查询为生产应用提供服务的相同数据，我们建议您在 Bigtable 实例中指定一个集群以仅用于 BigQuery 分析。这会将流量与用于应用读取和写入的集群隔离开。如需详细了解复制以及如何创建具有多个集群的实例，请参阅[复制简介](https://docs.cloud.google.com/bigtable/docs/replication-overview?hl=zh-cn)。

### 确定或创建应用配置文件

在创建外部表之前，请确定 BigQuery 应使用哪个 Bigtable 应用配置文件来读取数据。我们建议您使用指定仅用于 BigQuery 的应用配置文件。应用配置文件可以是标准应用配置文件，也可以是 Data Boost 应用配置文件，具体取决于您要使用哪种计算类型来查询数据。

如果您的 Bigtable 实例中有一个专用于 BigQuery 访问的集群，请将应用配置文件配置为使用单集群路由到该集群。

如需使用 Data Boost 无服务器计算，请创建 Data Boost 应用配置文件。如需使用集群节点进行计算，请创建标准应用配置文件。如需了解 Bigtable 应用配置文件的运作方式，请参阅[应用配置文件简介](https://docs.cloud.google.com/bigtable/docs/app-profiles?hl=zh-cn)。如需了解如何创建新的应用配置文件，请参阅[创建和配置应用配置文件](https://docs.cloud.google.com/bigtable/docs/configuring-app-profiles?hl=zh-cn)。

### 检索 Bigtable URI

如需为 Bigtable 数据源创建外部表，您必须提供 Bigtable URI。如需检索 Bigtable URI，请执行以下操作：

1. 在控制台中打开 Bigtable 页面。

   [打开 Bigtable](https://console.cloud.google.com/bigtable?hl=zh-cn)
2. 检索有关 Bigtable 数据源的如下详细信息：

   * 您的项目 ID。
   * 您的 Bigtable 实例 ID。
   * 您计划使用的 Bigtable 应用配置文件的 ID。
     这可以是标准应用配置文件，也可以是 Data Boost 应用配置文件，具体取决于您要使用的[计算类型](#compute)。如果您未指定应用配置文件 ID，则系统会使用默认应用配置文件。
   * 您的 Bigtable 表的名称。
3. 使用以下格式撰写 Bigtable URI，各变量含义如下：

   * PROJECT\_ID 是包含您的 Bigtable 实例的项目
   * INSTANCE\_ID 是 Bigtable 实例 ID
   * APP\_PROFILE（可选）是您要使用的应用配置文件的标识符
   * TABLE\_NAME 是您要查询的表的名称

   `https://googleapis.com/bigtable/projects/PROJECT_ID/instances/INSTANCE_ID[/appProfiles/APP_PROFILE]/tables/TABLE_NAME`

**注意**：您只能指定一个 Bigtable URI，并且此 URI 必须是指向一个 Bigtable 表的完整、有效的 HTTPS 网址。Bigtable 外部数据源不支持通配符。

## 创建永久外部表

在 BigQuery 中创建链接到 Bigtable 数据源的永久外部表时，您可以通过以下两个选项指定外部表的格式：

* 如果您使用的是 API 或 bq 命令行工具，则需要创建[表定义文件](https://docs.cloud.google.com/bigquery/docs/external-table-definition?hl=zh-cn)，以定义外部表的架构和元数据。
* 如果您使用的是 SQL，则需要使用 `CREATE EXTERNAL TABLE` 语句的 `uri` 选项指定要从中拉取数据的 Bigtable 表，并使用 `bigtable_options` 选项指定表架构。

外部表数据不会存储在 BigQuery 表中。由于该表是永久表，因此您可以使用数据集级层的[访问权限控制](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-cn)与其他同样有权访问底层 Bigtable 数据源的人员共享该表。

如需创建永久表，请选择以下方法之一。

### SQL

您可以通过运行 [`CREATE EXTERNAL TABLE` DDL 语句](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-cn#create_external_table_statement)创建永久外部表。您必须在语句选项中明确指定表架构。

1. 在 Google Cloud 控制台中，前往 **BigQuery** 页面。

   [转到 BigQuery](https://console.cloud.google.com/bigquery?hl=zh-cn)
2. 在查询编辑器中，输入以下语句：

   ```
   CREATE EXTERNAL TABLE DATASET.NEW_TABLE
   OPTIONS (
     format = 'CLOUD_BIGTABLE',
     uris = ['URI'],
     bigtable_options = BIGTABLE_OPTIONS );
   ```

   请替换以下内容：

   * `DATASET`：要在其中创建 Bigtable 外部表的数据集。
   * `NEW_TABLE`：Bigtable 外部表的名称。
   * `URI`：要用作数据源的 Bigtable 表的 URI。此 URI 必须遵循[检索 Bigtable URI](#bigtable-uri) 中所述的格式。
   * `BIGTABLE_OPTIONS`：Bigtable 表的架构（采用 JSON 格式）。如需查看 Bigtable 表定义选项列表，请参阅 REST API 参考文档中的 `BigtableOptions`。
3. 点击 play\_circle **运行**。

如需详细了解如何运行查询，请参阅[运行交互式查询](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-cn#queries)。

用于创建 Bigtable 外部表的语句如下所示：

```
CREATE EXTERNAL TABLE mydataset.BigtableTable
OPTIONS (
  format = 'CLOUD_BIGTABLE',
  uris = ['https://googleapis.com/bigtable/projects/myproject/instances/myBigtableInstance/appProfiles/myAppProfile/tables/table1'],
  bigtable_options =
    """
    {
      columnFamilies: [
        {
          "familyId": "familyId1",
          "type": "INTEGER",
          "encoding": "BINARY"
        }
      ],
      readRowkeyAsString: true
    }
    """
);
```

### bq

您可以在 bq 命令行工具中使用 [`bq mk` 命令](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-cn#bq_mk)创建表。使用 bq 命令行工具创建链接到外部数据源的表时，您可以使用[表定义文件](https://docs.cloud.google.com/bigquery/docs/external-table-definition?hl=zh-cn#tabledef-bigtable)来标识表的架构。

1. 使用 `bq mk` 命令创建永久表。

   ```
   bq mk \
   --external_table_definition=DEFINITION_FILE \
   DATASET.TABLE
   ```

   请替换以下内容：

   * `DEFINITION_FILE`：本地机器上[表定义文件](https://docs.cloud.google.com/bigquery/docs/external-table-definition?hl=zh-cn#tabledef-bigtable)的路径。
   * `DATASET`：包含该表的数据集的名称。
   * `TABLE`：您要创建的表的名称。

### API

使用 [`tables.insert`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables/insert?hl=zh-cn) API 方法，并在传入的 [`Table` 资源](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables?hl=zh-cn#Table)中创建一个 [`ExternalDataConfiguration`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables?hl=zh-cn#externaldataconfiguration)。

对于 `Table` 资源中的 `sourceUris` 属性，请仅指定一个 [Bigtable URI](#bigtable-uri)；并且该 URI 必须是有效的 HTTPS 网址。

对于 `sourceFormat` 属性，请指定 `"BIGTABLE"`。

### Java

试用此示例之前，请按照 [BigQuery 快速入门：使用客户端库](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-cn)中的 Java 设置说明进行操作。
如需了解详情，请参阅 [BigQuery Java API 参考文档](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/overview?hl=zh-cn)。

如需向 BigQuery 进行身份验证，请设置应用默认凭证。如需了解详情，请参阅[为客户端库设置身份验证](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-cn#client-libs)。

```
import com.google.cloud.bigquery.BigQuery;
import com.google.cloud.bigquery.BigQueryException;
import com.google.cloud.bigquery.BigQueryOptions;
import com.google.cloud.bigquery.BigtableColumn;
import com.google.cloud.bigquery.BigtableColumnFamily;
import com.google.cloud.bigquery.BigtableOptions;
import com.google.cloud.bigquery.ExternalTableDefinition;
import com.google.cloud.bigquery.QueryJobConfiguration;
import com.google.cloud.bigquery.TableId;
import com.google.cloud.bigquery.TableInfo;
import com.google.cloud.bigquery.TableResult;
import com.google.common.collect.ImmutableList;
import org.apache.commons.codec.binary.Base64;

// Sample to queries an external bigtable data source using a permanent table
public class QueryExternalBigtablePerm {

  public static void main(String[] args) {
    // TODO(developer): Replace these variables before running the sample.
    String projectId = "MY_PROJECT_ID";
    String bigtableInstanceId = "MY_INSTANCE_ID";
    String bigtableTableName = "MY_BIGTABLE_NAME";
    String bigqueryDatasetName = "MY_DATASET_NAME";
    String bigqueryTableName = "MY_TABLE_NAME";
    String sourceUri =
        String.format(
            "https://googleapis.com/bigtable/projects/%s/instances/%s/tables/%s",
            projectId, bigtableInstanceId, bigtableTableName);
    String query = String.format("SELECT * FROM %s ", bigqueryTableName);
    queryExternalBigtablePerm(bigqueryDatasetName, bigqueryTableName, sourceUri, query);
  }

  public static void queryExternalBigtablePerm(
      String datasetName, String tableName, String sourceUri, String query) {
    try {
      // Initialize client that will be used to send requests. This client only needs to be created
      // once, and can be reused for multiple requests.
      BigQuery bigquery = BigQueryOptions.getDefaultInstance().getService();

      BigtableColumnFamily.Builder statsSummary = BigtableColumnFamily.newBuilder();

      // Configuring Columns
      BigtableColumn connectedCell =
          BigtableColumn.newBuilder()
              .setQualifierEncoded(Base64.encodeBase64String("connected_cell".getBytes()))
              .setFieldName("connected_cell")
              .setType("STRING")
              .setEncoding("TEXT")
              .build();
      BigtableColumn connectedWifi =
          BigtableColumn.newBuilder()
              .setQualifierEncoded(Base64.encodeBase64String("connected_wifi".getBytes()))
              .setFieldName("connected_wifi")
              .setType("STRING")
              .setEncoding("TEXT")
              .build();
      BigtableColumn osBuild =
          BigtableColumn.newBuilder()
              .setQualifierEncoded(Base64.encodeBase64String("os_build".getBytes()))
              .setFieldName("os_build")
              .setType("STRING")
              .setEncoding("TEXT")
              .build();

      // Configuring column family and columns
      statsSummary
          .setColumns(ImmutableList.of(connectedCell, connectedWifi, osBuild))
          .setFamilyID("stats_summary")
          .setOnlyReadLatest(true)
          .setEncoding("TEXT")
          .setType("STRING")
          .build();

      // Configuring BigtableOptions is optional.
      BigtableOptions options =
          BigtableOptions.newBuilder()
              .setIgnoreUnspecifiedColumnFamilies(true)
              .setReadRowkeyAsString(true)
              .setColumnFamilies(ImmutableList.of(statsSummary.build()))
              .build();

      TableId tableId = TableId.of(datasetName, tableName);
      // Create a permanent table linked to the Bigtable table
      ExternalTableDefinition externalTable =
          ExternalTableDefinition.newBuilder(sourceUri, options).build();
      bigquery.create(TableInfo.of(tableId, externalTable));

      // Example query
      TableResult results = bigquery.query(QueryJobConfiguration.of(query));

      results
          .iterateAll()
          .forEach(row -> row.forEach(val -> System.out.printf("%s,", val.toString())));

      System.out.println("Query on external permanent table performed successfully.");
    } catch (BigQueryException | InterruptedException e) {
      System.out.println("Query not performed \n" + e.toString());
    }
  }
}
```

## 查询外部表

如需了解详情，请参阅[查询 Bigtable 数据](https://docs.cloud.google.com/bigquery/docs/external-data-bigtable?hl=zh-cn)。

## 生成的架构

默认情况下，BigQuery 将列族中的值作为列数组公开，并在其中包含以不同时间戳写入的值数组。该架构保留了 Bigtable 中数据的自然布局，但 SQL 查询可能难度较大。可能的解决方案是将列提升为父级列族中的子字段，并且只读取每个单元格中的最新值。这会以标量值的形式表示默认架构中的两个数组。

### 示例

您要存储某个虚构社交网络的用户个人资料。一个数据模型可能是一个 `profile` 列族，其中包含对应于 `gender`、`age` 和 `email` 的各列：

```
rowkey | profile:gender| profile:age| profile:email
-------| --------------| -----------| -------------
alice  | female        | 30         | alice@gmail.com
```

使用默认架构时，用于计算 30 岁以上男性用户数量的 GoogleSQL 查询如下：

```
SELECT
  COUNT(1)
FROM
  `dataset.table`
OMIT
  RECORD IF NOT SOME(profile.column.name = "gender"
    AND profile.column.cell.value = "male")
  OR NOT SOME(profile.column.name = "age"
    AND INTEGER(profile.column.cell.value) > 30)
```

如果将 `gender` 和 `age` 作为子字段公开提供，则查询数据会较为容易。为了将这些字段作为子字段公开提供，可以在定义表时将 `gender` 和 `age` 作为 `profile` 列族中的命名列列出。您还可以指示 BigQuery 公开此列族中的最新值，因为通常只有最新值（并且可能是唯一值）才是有用的。

将列作为子字段公开提供之后，用于计算 30 岁以上男性用户数量的 GoogleSQL 查询如下：

```
SELECT
  COUNT(1)
FROM
  `dataset.table`
WHERE
  profile.gender.cell.value="male"
  AND profile.age.cell.value > 30
```

请注意如何将 `gender` 和 `age` 直接作为字段引用。此设置的 JSON 配置如下：

```
  "bigtableOptions": {
    "readRowkeyAsString": "true",
    "columnFamilies": [
      {
          "familyId": "profile",
          "onlyReadLatest": "true",
          "columns": [
              {
                  "qualifierString": "gender",
                  "type": "STRING"
              },
              {
                  "qualifierString": "age",
                  "type": "INTEGER"
              }
          ]
      }
    ]
  }
```

## 值编码

Bigtable 将数据存储为与数据编码无关的原始字节。但字节值在 SQL 查询分析中的用途有限。Bigtable 提供两种基本类型的标量解码：文本和 HBase 二进制。

文本格式假定所有值均存储为字母数字文本字符串。例如，整数 768 将存储为字符串“768”。二进制编码假定使用 HBase 的 [`Bytes.toBytes`](https://hbase.apache.org/devapidocs/org/apache/hadoop/hbase/util/Bytes.html) 方法类对数据进行编码，并应用适当的解码方法。

## 支持的区域和地区

您可以在支持 Bigtable 的所有可用区中进行 Bigtable 数据查询。您可以在[此处](https://docs.cloud.google.com/bigtable/docs/locations?hl=zh-cn)找到可用区列表。对于多集群实例，BigQuery 会根据 Bigtable [应用配置文件](https://docs.cloud.google.com/bigtable/docs/app-profiles?hl=zh-cn)设置路由流量。

## 限制

* 您无法在基于 Bigtable SQL 的对象（例如视图和连续物化视图）上创建外部表。
* 如需详细了解适用于外部表的限制，请参阅[外部表限制](https://docs.cloud.google.com/bigquery/docs/external-tables?hl=zh-cn#limitations)。

## Compute Engine 实例的范围

创建 Compute Engine 实例时，您可以为该实例指定一个范围列表。这些范围用于控制该实例对 Google Cloud产品（包括 Bigtable）的访问权限。虚拟机上运行的应用使用服务账号来调用 Google Cloud API。

如果您将某个 Compute Engine 实例设置为以[服务账号](https://docs.cloud.google.com/compute/docs/access/create-enable-service-accounts-for-instances?hl=zh-cn)身份运行，并且该服务账号访问一个链接到 Bigtable 数据源的外部表，则您必须为该实例添加 Bigtable 只读数据访问权限范围 (`https://www.googleapis.com/auth/bigtable.data.readonly`)。如需了解详情，请参阅[为 Bigtable 创建 Compute Engine 实例](https://docs.cloud.google.com/bigtable/docs/creating-compute-instance?hl=zh-cn)。

如需了解如何将范围应用于 Compute Engine 实例，请参阅[更改实例的服务账号和访问权限范围](https://docs.cloud.google.com/compute/docs/access/create-enable-service-accounts-for-instances?hl=zh-cn#changeserviceaccountandscopes)。如需详细了解 Compute Engine 服务账号，请参阅[服务账号](https://docs.cloud.google.com/compute/docs/access/service-accounts?hl=zh-cn)。

## 后续步骤

* [详细了解 Bigtable 架构设计](https://docs.cloud.google.com/bigtable/docs/schema-design?hl=zh-cn)。
* [查看外部数据源简介](https://docs.cloud.google.com/bigquery/docs/external-data-sources?hl=zh-cn)。




发送反馈

如未另行说明，那么本页面中的内容已根据[知识共享署名 4.0 许可](https://creativecommons.org/licenses/by/4.0/)获得了许可，并且代码示例已根据 [Apache 2.0 许可](https://www.apache.org/licenses/LICENSE-2.0)获得了许可。有关详情，请参阅 [Google 开发者网站政策](https://developers.google.com/site-policies?hl=zh-cn)。Java 是 Oracle 和/或其关联公司的注册商标。

最后更新时间 (UTC)：2026-02-24。




需要向我们提供更多信息？

[[["易于理解","easyToUnderstand","thumb-up"],["解决了我的问题","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["很难理解","hardToUnderstand","thumb-down"],["信息或示例代码不正确","incorrectInformationOrSampleCode","thumb-down"],["没有我需要的信息/示例","missingTheInformationSamplesINeed","thumb-down"],["翻译问题","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["最后更新时间 (UTC)：2026-02-24。"],[],[]]