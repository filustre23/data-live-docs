* [Home](https://docs.cloud.google.com/?hl=zh-cn)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-cn)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-cn)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-cn)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-cn)

发送反馈



使用集合让一切井井有条

根据您的偏好保存内容并对其进行分类。

# 查询 Bigtable 数据

本文档介绍了如何使用 BigQuery 查询存储在 [Bigtable 外部表](https://docs.cloud.google.com/bigquery/docs/create-bigtable-external-table?hl=zh-cn)中的数据。如需了解如何直接从 Bigtable 查询数据，请参阅 [GoogleSQL for Bigtable 概览](https://docs.cloud.google.com/bigtable/docs/googlesql-overview?hl=zh-cn)。

[Bigtable](https://docs.cloud.google.com/bigtable/docs?hl=zh-cn) 是 Google 推出的一种稀疏填充的 NoSQL 数据库，可以扩展到数十亿行和数千列，支持存储 PB 级的数据。如需了解 Bigtable 数据模型，请参阅[存储模型](https://docs.cloud.google.com/bigtable/docs/overview?hl=zh-cn#storage-model)。

## 查询永久外部表

在开始之前，您或组织的管理员必须先创建一个供您使用的外部表。如需了解详情和所需权限，请参阅[创建 BigQuery 外部表](https://docs.cloud.google.com/bigquery/docs/create-bigtable-external-table?hl=zh-cn)。

### 所需的角色

如需查询 Bigtable 外部表，请确保您具有以下角色。

* BigQuery Data Viewer (`roles/bigquery.dataViewer`)
* BigQuery User (`roles/bigquery.user`)
* Bigtable Reader (`roles/bigtable.reader`)

根据您的权限，您可以自行授予这些角色给自己，或者让管理员授予给您。如需详细了解如何授予角色，请参阅[查看可针对资源授予的角色](https://docs.cloud.google.com/iam/docs/viewing-grantable-roles?hl=zh-cn)。

如需查看查询外部表所需的确切 BigQuery 权限，请展开**所需权限**部分：

#### 所需权限

* `bigquery.jobs.create`
* `bigquery.readsessions.create`（仅当您[使用 BigQuery Storage Write API 流式传输数据](https://docs.cloud.google.com/bigquery/docs/write-api-streaming?hl=zh-cn)时才需要）
* `bigquery.tables.get`
* `bigquery.tables.getData`

您也可以使用[自定义角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-cn)或其他[预定义角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-cn#predefined)来获取这些权限。

### 查询表

您可以对永久外部 Bigtable 表运行查询，就像对[标准 BigQuery 表](https://docs.cloud.google.com/bigquery/docs/tables-intro?hl=zh-cn#standard-tables)运行查询一样，但需遵守外部数据源的[限制](https://docs.cloud.google.com/bigquery/docs/external-tables?hl=zh-cn#limitations)。如需了解详情，请参阅[运行交互式查询和批量查询](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-cn)。

## 查询临时外部表

使用临时表查询外部数据源适用于对外部数据进行一次性临时查询，或执行提取、转换和加载 (ETL) 过程。

要在不创建永久表的情况下查询外部数据源，请为临时表提供表定义，然后在命令或调用中使用该表定义来查询临时表。您可以通过以下任一方式提供表定义：

* [表定义文件](https://docs.cloud.google.com/bigquery/external-table-definition?hl=zh-cn)
* 内嵌架构定义
* [JSON 架构文件](https://docs.cloud.google.com/bigquery/docs/schemas?hl=zh-cn#specifying_a_json_schema_file)

系统会使用表定义文件或提供的架构来创建临时外部表，然后对临时外部表运行查询。

使用临时外部表时，并不会在您的某个 BigQuery 数据集中创建表。由于该表不会永久存储在数据集内，因此无法与他人共享。

使用临时外部表而不是永久外部表存在一些限制，包括以下限制：

* 您必须具有 Bigtable Admin (`roles/bigtable.admin`) 角色。
* 此方法不允许您使用 Google Cloud 控制台来推理 Bigtable 表的架构并自动创建表定义。您必须自行创建表定义。

### 所需的角色

如需查询 Bigtable 临时外部表，请确保您具有以下角色：

* BigQuery Data Viewer (`roles/bigquery.dataViewer`)
* BigQuery User (`roles/bigquery.user`)
* Bigtable 管理员 (`roles/bigtable.admin`)

根据您的权限，您可以自行授予这些角色给自己，或者让管理员授予给您。如需详细了解如何授予角色，请参阅[查看可针对资源授予的角色](https://docs.cloud.google.com/iam/docs/viewing-grantable-roles?hl=zh-cn)。

如需查看查询外部表所需的确切 BigQuery 权限，请展开**所需权限**部分：

#### 所需权限

* `bigquery.jobs.create`
* `bigquery.readsessions.create`（仅当您[使用 BigQuery Storage Write API 流式传输数据](https://docs.cloud.google.com/bigquery/docs/write-api-streaming?hl=zh-cn)时才需要）
* `bigquery.tables.get`
* `bigquery.tables.getData`

您也可以使用[自定义角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-cn)或其他[预定义角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-cn#predefined)来获取这些权限。

### 创建和查询表

如需使用临时外部表查询 Bigtable 数据，您需要执行以下操作：

* 创建[表定义文件](https://docs.cloud.google.com/bigquery/docs/external-table-definition?hl=zh-cn#tabledef-bigtable)
* 提交查询和表定义文件

bq 命令行工具和 API 支持创建和查询临时外部表。

### bq

如需使用表定义文件查询临时表，请输入带 `--external_table_definition` 标志的 `bq query` 命令。

（可选）提供 `--location` 标志并将其值设置为您的[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-cn)。

```
bq --location=LOCATION query \
--use_legacy_sql=false \
--external_table_definition=TABLE::DEFINITION_FILE \
'QUERY'
```

替换以下内容：

* `LOCATION`：您所在[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-cn)的名称。`--location` 是可选标志。
* `TABLE`：您要创建的临时表的名称。
* `DEFINITION_FILE`：本地机器上[表定义文件](https://docs.cloud.google.com/bigquery/docs/external-table-definition?hl=zh-cn#tabledef-bigtable)的路径。
* `QUERY`：您要提交到临时表的查询。

例如，以下命令使用名为 `follows_def` 的表定义文件创建并查询名为 `follows` 的临时表。

```
bq query \
--use_legacy_sql=false \
--external_table_definition=follows::/tmp/follows_def \
'SELECT
  COUNT(rowkey)
 FROM
   follows'
```

### API

* 创建查询。如需了解如何创建查询作业，请参阅[查询数据](https://docs.cloud.google.com/bigquery/querying-data?hl=zh-cn)。
* （可选）在[作业资源](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-cn)的 `jobReference` 部分的 `location` 属性中指定您的位置。
* 为[表资源](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables?hl=zh-cn#externaldataconfiguration)设置 `ExternalDataConfiguration` 以指定外部数据源属性。

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
import com.google.cloud.bigquery.TableResult;
import com.google.common.collect.ImmutableList;
import org.apache.commons.codec.binary.Base64;

// Sample to queries an external bigtable data source using a temporary table
public class QueryExternalBigtableTemp {

  public static void main(String[] args) {
    // TODO(developer): Replace these variables before running the sample.
    String projectId = "MY_PROJECT_ID";
    String bigtableInstanceId = "MY_INSTANCE_ID";
    String bigtableTableName = "MY_BIGTABLE_NAME";
    String bigqueryTableName = "MY_TABLE_NAME";
    String sourceUri =
        String.format(
            "https://googleapis.com/bigtable/projects/%s/instances/%s/tables/%s",
            projectId, bigtableInstanceId, bigtableTableName);
    String query = String.format("SELECT * FROM %s ", bigqueryTableName);
    queryExternalBigtableTemp(bigqueryTableName, sourceUri, query);
  }

  public static void queryExternalBigtableTemp(String tableName, String sourceUri, String query) {
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

      // Configure the external data source and query job.
      ExternalTableDefinition externalTable =
          ExternalTableDefinition.newBuilder(sourceUri, options).build();
      QueryJobConfiguration queryConfig =
          QueryJobConfiguration.newBuilder(query)
              .addTableDefinition(tableName, externalTable)
              .build();

      // Example query
      TableResult results = bigquery.query(queryConfig);

      results
          .iterateAll()
          .forEach(row -> row.forEach(val -> System.out.printf("%s,", val.toString())));

      System.out.println("Query on external temporary table performed successfully.");
    } catch (BigQueryException | InterruptedException e) {
      System.out.println("Query not performed \n" + e.toString());
    }
  }
}
```

## 性能考虑因素

针对 Bigtable 外部数据源进行的查询的性能取决于三个因素：

* 行数
* 读取的数据量
* 并行化程度

BigQuery 会尝试仅读取查询中引用的列族，从而尽可能减少读取数据量。并行化程度取决于您在 Bigtable 集群中拥有的节点数量以及您在自己的表中的拆分次数。

请注意，Bigtable 会根据负载自动合并拆分。如果读取该表的频率较低，则随着时间的推移，拆分次数会减少，查询性能会逐渐降低。如需了解详情，请参阅 [BigQuery 如何随时间推移优化数据](https://docs.cloud.google.com/bigtable/docs/performance?hl=zh-cn#optimization)。

### 计算

**预览版**

此产品或功能 受[服务专用条款](https://docs.cloud.google.com/terms/service-terms?hl=zh-cn#1)的约束。
非正式版产品和功能“按原样”提供，可能只能获得有限的支持。
如需了解详情，请参阅[发布阶段说明](https://cloud.google.com/products/?hl=zh-cn#product-launch-stages)。

从 BigQuery 查询 Bigtable 数据时，您可以选择以下计算选项：

* 集群节点，这是默认设置。
* [Data Boost](https://docs.cloud.google.com/bigtable/docs/data-boost-overview?hl=zh-cn)（预览版），一种无服务器计算选项，可让您隔离分析流量，而不会影响集群节点所处理的应用服务流量。

如需使用 Data Boost，您或您的管理员必须创建一个定义文件，用于在 Bigtable URI 中指定 Data Boost 应用配置文件。如需了解详情，请参阅[创建 Bigtable 外部表](https://docs.cloud.google.com/bigquery/docs/create-bigtable-external-table?hl=zh-cn)。

如果您不使用 Data Boost，请注意，通过 BigQuery 查询 Bigtable 会消耗 Bigtable CPU 周期。当使用预配的节点进行计算时，BigQuery 的 CPU 消耗可能会影响其他并发请求（例如实时用户流量处理）的延迟时间和吞吐量。例如，Bigtable 上的高 CPU 使用率会影响长尾查询，并增加第 99 百分位的延迟时间。

因此，您应该监控 Bigtable 的 CPU 使用率，以验证此数据是否处于 Google Cloud 控制台内 Bigtable 监控信息中心所注明的推荐范围内。通过增加实例的节点数量，您将能够处理 BigQuery 流量以及来自其他并发请求的流量。

## 查询过滤器

在查询外部表时，您可以添加查询过滤条件来减少 BigQuery 资源用量。

### 行键过滤条件

采用行键相等性过滤条件的查询仅读取该特定行。例如，在 GoogleSQL 语法中：

```
SELECT
  COUNT(follows.column.name)
FROM
  `dataset.table`
WHERE
  rowkey = "alice";
```

系统也支持 `rowkey > '1'` 和 `rowkey < '8'` 等范围过滤器，但只有在使用 `readRowkeyAsString` 选项以字符串形式读取 rowkey 时才能提供此支持。

**注意：**如果将 `readRowkeyAsString` 设置为 `true`，则系统会读取 rowkey 列族，并将其转换为字符串。否则，系统会使用 BYTES 类型值读取这些内容。

### 按列族和限定符进行过滤

您还可以选择特定的列族或列族中的特定限定符。如需按列族进行过滤，请选择列族名称，结果中将仅包含所选列族。在以下示例中，`user_info` 表示一个列族：

```
    SELECT
      rowkey AS user_id,
      user_info
    FROM
      project.dataset.table;
```

如需按特定限定符进行过滤，您必须先在外部表定义的 `"columns"` 中声明这些限定符：

```
CREATE OR REPLACE EXTERNAL TABLE project.dataset.table
  OPTIONS (
    format = 'CLOUD_BIGTABLE',
    uris = ['https://googleapis.com/bigtable/projects/…/instances/…/tables/…'],
    bigtable_options = '''{
  "columnFamilies": [
    {
      "familyId": "user_info",
      "columns": [
        {
          "qualifierString": "name"
        },
        {
          "qualifierString": "email"
        },
        {
          "qualifierString": "registered_at"
        }
      ]
    },
    {
      "familyId": "session_data"
    }
  ],
  "readRowkeyAsString": true,
  "timestampSuffix": "_ts"
}'''
  );
```

创建外部表后，使用 `SELECT` 语句查询特定限定符。这样可确保 BigQuery 将过滤条件下推到 Bigtable，并且在从 BigQuery 运行 `SELECT` 语句时仅加载指定的限定符，而不是整个列族的数据。这样可以减少 BigQuery 资源消耗。

```
    SELECT
      rowkey AS user_id,
      user_info.email.cell[SAFE_OFFSET(0)].value as email
    FROM
      project.dataset.table;
```




发送反馈

如未另行说明，那么本页面中的内容已根据[知识共享署名 4.0 许可](https://creativecommons.org/licenses/by/4.0/)获得了许可，并且代码示例已根据 [Apache 2.0 许可](https://www.apache.org/licenses/LICENSE-2.0)获得了许可。有关详情，请参阅 [Google 开发者网站政策](https://developers.google.com/site-policies?hl=zh-cn)。Java 是 Oracle 和/或其关联公司的注册商标。

最后更新时间 (UTC)：2026-03-17。




需要向我们提供更多信息？

[[["易于理解","easyToUnderstand","thumb-up"],["解决了我的问题","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["很难理解","hardToUnderstand","thumb-down"],["信息或示例代码不正确","incorrectInformationOrSampleCode","thumb-down"],["没有我需要的信息/示例","missingTheInformationSamplesINeed","thumb-down"],["翻译问题","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["最后更新时间 (UTC)：2026-03-17。"],[],[]]