* [Home](https://docs.cloud.google.com/?hl=zh-cn)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-cn)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-cn)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-cn)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-cn)

发送反馈



使用集合让一切井井有条

根据您的偏好保存内容并对其进行分类。

# 在表架构中指定 ObjectRef 列

**预览版**

此功能 受[服务专用条款](https://docs.cloud.google.com/terms/service-terms?hl=zh-cn#1)的约束。 非正式版功能“按原样”提供，且可能仅提供有限支持。
如需了解详情，请参阅[发布阶段说明](https://cloud.google.com/products/?hl=zh-cn#product-launch-stages)。

**注意**：如需就此功能提供反馈或请求支持，请发送邮件至 [bq-objectref-feedback@google.com](mailto:bq-objectref-feedback@google.com)

本文档介绍了如何定义 BigQuery 标准表架构，使其包含可存储 `ObjectRef` 值的列。

`ObjectRef` 值提供 Cloud Storage 中对象的元数据和连接信息。当您需要将非结构化数据集成到标准表中时，使用 `ObjectRef` 值。例如，在商品表中，您可以通过添加包含 `ObjectRef` 值的列，将商品图片与其余商品信息存储在同一行中。您可以将 `ObjectRef` 值存储在采用 [`ObjectRef` 格式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/objectref_functions?hl=zh-cn#objectref)（即 `STRUCT<uri STRING, version STRING, authorizer STRING, details JSON>`）的 `STRUCT` 列中。

如需详细了解如何处理多模态数据，请参阅[分析多模态数据](https://docs.cloud.google.com/bigquery/docs/analyze-multimodal-data?hl=zh-cn)。
如需查看有关如何处理 `ObjectRef` 数据的教程，请参阅[使用 SQL 分析多模态数据](https://docs.cloud.google.com/bigquery/docs/multimodal-data-sql-tutorial?hl=zh-cn)。
如需了解如何在 Python 中处理多模态数据，请参阅[使用 BigQuery DataFrames 在 Python 中分析多模态数据](https://docs.cloud.google.com/bigquery/docs/multimodal-data-dataframes-tutorial?hl=zh-cn)。

**注意**：本文档中的示例使用 [`CREATE OR REPLACE TABLE` 语句](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-cn#create_table_statement)通过一次操作创建并填充 `ObjectRef` 列，但您也可以使用 [`ALTER TABLE ADD COLUMN` 语句](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-cn#alter_table_add_column_statement)将 `STRUCT` 列添加到现有表中，然后使用 [`UPDATE` 语句](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/dml-syntax?hl=zh-cn#update_statement)通过单独的操作填充该列。

## 前提条件

如需在标准表中填充和更新 `ObjectRef` 值，该表必须具有 `STRING` 列，其中包含相关 Cloud Storage 对象的 URI 信息。

您必须拥有一个 Cloud Storage 存储桶，其中包含目标标准表的 URI 数据中标识的相同对象。如果您想使用[对象表](https://docs.cloud.google.com/bigquery/docs/object-table-introduction?hl=zh-cn)[维护标准表中的 `ObjectRef` 值](#maintaining_objectref_values)，则还必须有一个对象表来表示相应存储桶中的对象。

## 维护 `ObjectRef` 值

您可以使用对象表在标准表中填充和更新 `ObjectRef` 值。如果您在预览版的许可名单中，那么您创建的任何对象表都会有一个 `ref` 列，其中包含给定对象的 `ObjectRef` 值。您可以使用对象 URI 将标准表与对象表联接，以填充和更新 `ObjectRef` 值。我们建议使用此方法以实现可伸缩性，因为它避免了从 Cloud Storage 检索对象元数据的需要。

如果您不想创建对象表，可以使用 [`OBJ.FETCH_METADATA`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/objectref_functions?hl=zh-cn#objfetch_metadata) 和 [`OBJ.MAKE_REF`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/objectref_functions?hl=zh-cn#objmake_ref) 函数通过直接从 Cloud Storage 中提取对象元数据来填充和更新 `ObjectRef` 值。这种方法的可伸缩性可能较差，因为它需要从 Cloud Storage 检索对象元数据。

## 创建 `ObjectRef` 列

如需在标准表中创建并填充 `ObjectRef` 列，请选择以下选项之一：

### 对象表

基于对象表 `ref` 列中的数据创建并填充 `ObjectRef` 列：

1. 在 Google Cloud 控制台中，前往 **BigQuery** 页面。

   [转到 BigQuery](https://console.cloud.google.com/bigquery?hl=zh-cn)
2. 在查询编辑器中，输入以下语句：

   ```
   CREATE OR REPLACE TABLE PROJECT_ID.DATASET_ID.TABLE_NAME
   AS
   SELECT TABLE_NAME.*, OBJECT_TABLE.ref AS objectrefcolumn
   FROM DATASET_ID.TABLE_NAME
   INNER JOIN DATASET_ID.OBJECT_TABLE
   ON OBJECT_TABLE.uri = TABLE_NAME.uri;
   ```

   请替换以下内容：

   * `PROJECT_ID`：您的项目 ID。如果您要在当前项目中创建表，则可以跳过此参数。
   * `DATASET_ID`：您要创建的数据集的 ID。
   * `TABLE_NAME`：您要重新创建的标准表的名称。
   * `OBJECT_TABLE`：包含要集成到标准表中的对象数据的对象表的名称。
3. 点击 play\_circle **运行**。

如需详细了解如何运行查询，请参阅[运行交互式查询](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-cn#queries)。

### SQL 函数的可组合性

根据 `OBJ.FETCH_METADATA` 和 `OBJ.MAKE_REF` 函数的输出创建并填充 `ObjectRef` 列：

1. 在 Google Cloud 控制台中，前往 **BigQuery** 页面。

   [转到 BigQuery](https://console.cloud.google.com/bigquery?hl=zh-cn)
2. 在查询编辑器中，输入以下语句：

   ```
   CREATE OR REPLACE TABLE PROJECT_ID.DATASET_ID.TABLE_NAME
   AS
   SELECT TABLE_NAME.*,
   OBJ.FETCH_METADATA(OBJ.MAKE_REF(uri, 'CONNECTION_ID')) AS objectrefcolumn
   FROM DATASET_ID.TABLE_NAME;
   ```

   请替换以下内容：

   * `PROJECT_ID`：您的项目 ID。如果您要在当前项目中创建表，则可以跳过此参数。
   * `DATASET_ID`：您要创建的数据集的 ID。
   * `TABLE_NAME`：您要重新创建的标准表的名称。
   * `CONNECTION_ID`：一个 `STRING` 值，其中包含服务可用于访问 Cloud Storage 中对象的[云资源连接](https://docs.cloud.google.com/bigquery/docs/create-cloud-resource-connection?hl=zh-cn)，格式为 `location.connection_id`。例如，`us-west1.myconnection`。您可以通过在 Google Cloud 控制台中[查看连接详细信息](https://docs.cloud.google.com/bigquery/docs/working-with-connections?hl=zh-cn#view-connections)并复制**连接 ID** 中显示的完全限定连接 ID 的最后一部分中的值，来获取连接 ID。例如，`projects/myproject/locations/connection_location/connections/myconnection`。

     您必须将 Storage Object User (`roles/storage.objectUser`) 角色授予您使用它来访问对象的任何 Cloud Storage 存储桶上的连接服务账号。

     连接必须与您调用函数的查询位于同一项目和区域中。
3. 点击 play\_circle **运行**。

如需详细了解如何运行查询，请参阅[运行交互式查询](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-cn#queries)。

## 创建 `ARRAY<ObjectRef>` 列

您可以创建一个 `ARRAY<STRUCT<uri STRING, version STRING, authorizer STRING, details JSON>>` 列来包含 `ObjectRef` 值数组。例如，您可以将视频分块为单独的图片，然后将这些图片存储为 `ObjectRef` 值的数组。

您可以使用 [`ARRAY_AGG` 函数](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/aggregate_functions?hl=zh-cn#array_agg)来聚合 `ObjectRef` 值的数组，包括在必要时使用 `ORDER BY` 子句保留对象顺序。您可以使用 [`UNNEST` 运算符](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-cn#unnest_operator)将 `ObjectRef` 值数组解析为单个 `ObjectRef` 值，包括在必要时使用 `WITH OFFSET` 子句保留对象顺序。您可以使用对象元数据（例如 URI 路径和对象文件名）将表示对象块的 `ObjectRef` 值映射到表示原始对象的 `ObjectRef` 值。

如需查看如何使用 `ObjectRef` 值数组的示例，请参阅[使用 SQL 分析多模态数据](https://docs.cloud.google.com/bigquery/docs/multimodal-data-sql-tutorial?hl=zh-cn)教程的[使用 `ARRAY<ObjectRef>` 值处理有序的多模态数据](https://docs.cloud.google.com/bigquery/docs/multimodal-data-sql-tutorial?hl=zh-cn#process_ordered_multimodal_data_using_arrays_of_objectref_values)部分。

## 更新 `ObjectRef` 列

如需更新标准表中的 `ObjectRef` 列，请选择以下选项之一：

### 对象表

使用对象表 `ref` 列中的数据更新 `ObjectRef` 列：

1. 在 Google Cloud 控制台中，前往 **BigQuery** 页面。

   [转到 BigQuery](https://console.cloud.google.com/bigquery?hl=zh-cn)
2. 在查询编辑器中，输入以下语句：

   ```
   UPDATE PROJECT_ID.DATASET_ID.TABLE_NAME
   SET objectrefcolumn = (SELECT ref FROM DATASET_ID.OBJECT_TABLE WHERE OBJECT_TABLE.uri = TABLE_NAME.uri)
   WHERE uri != "";
   ```

   请替换以下内容：

   * `PROJECT_ID`：您的项目 ID。如果您要在当前项目中创建表，则可以跳过此参数。
   * `DATASET_ID`：您要创建的数据集的 ID。
   * `TABLE_NAME`：您要重新创建的标准表的名称。
   * `OBJECT_TABLE`：包含与标准表 `ObjectRef` 列相同的对象数据的对象表的名称。
3. 点击 play\_circle **运行**。

如需详细了解如何运行查询，请参阅[运行交互式查询](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-cn#queries)。

### SQL 函数的可组合性

使用 `OBJ.FETCH_METADATA` 和 `OBJ.MAKE_REF` 函数的输出更新 `ObjectRef` 列：

1. 在 Google Cloud 控制台中，前往 **BigQuery** 页面。

   [转到 BigQuery](https://console.cloud.google.com/bigquery?hl=zh-cn)
2. 在查询编辑器中，输入以下语句：

   ```
   UPDATE PROJECT_ID.DATASET_ID.TABLE_NAME
   SET objectrefcolumn = (SELECT OBJ.FETCH_METADATA(OBJ.MAKE_REF(uri, 'CONNECTION_ID')))
   WHERE uri != "";
   ```

   请替换以下内容：

   * `PROJECT_ID`：您的项目 ID。如果您要在当前项目中创建表，则可以跳过此参数。
   * `DATASET_ID`：您要创建的数据集的 ID。
   * `TABLE_NAME`：您要重新创建的标准表的名称。
   * `CONNECTION_ID`：一个 `STRING` 值，其中包含服务可用于访问 Cloud Storage 中对象的[云资源连接](https://docs.cloud.google.com/bigquery/docs/create-cloud-resource-connection?hl=zh-cn)，格式为 `location.connection_id`。例如，`us-west1.myconnection`。您可以通过在 Google Cloud 控制台中[查看连接详细信息](https://docs.cloud.google.com/bigquery/docs/working-with-connections?hl=zh-cn#view-connections)并复制**连接 ID** 中显示的完全限定连接 ID 的最后一部分中的值，来获取连接 ID。例如，`projects/myproject/locations/connection_location/connections/myconnection`。

     您必须将 Storage Object User (`roles/storage.objectUser`) 角色授予您使用它来访问对象的任何 Cloud Storage 存储桶上的连接服务账号。

     连接必须与您调用函数的查询位于同一项目和区域中。
3. 点击 play\_circle **运行**。

如需详细了解如何运行查询，请参阅[运行交互式查询](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-cn#queries)。

## 后续步骤

* [分析多模态数据](https://docs.cloud.google.com/bigquery/docs/analyze-multimodal-data?hl=zh-cn)。
* [使用 SQL 分析多模态数据](https://docs.cloud.google.com/bigquery/docs/multimodal-data-sql-tutorial?hl=zh-cn)。
* [使用 BigQuery DataFrames 在 Python 中分析多模态数据](https://docs.cloud.google.com/bigquery/docs/multimodal-data-dataframes-tutorial?hl=zh-cn)




发送反馈

如未另行说明，那么本页面中的内容已根据[知识共享署名 4.0 许可](https://creativecommons.org/licenses/by/4.0/)获得了许可，并且代码示例已根据 [Apache 2.0 许可](https://www.apache.org/licenses/LICENSE-2.0)获得了许可。有关详情，请参阅 [Google 开发者网站政策](https://developers.google.com/site-policies?hl=zh-cn)。Java 是 Oracle 和/或其关联公司的注册商标。

最后更新时间 (UTC)：2026-03-18。




需要向我们提供更多信息？

[[["易于理解","easyToUnderstand","thumb-up"],["解决了我的问题","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["很难理解","hardToUnderstand","thumb-down"],["信息或示例代码不正确","incorrectInformationOrSampleCode","thumb-down"],["没有我需要的信息/示例","missingTheInformationSamplesINeed","thumb-down"],["翻译问题","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["最后更新时间 (UTC)：2026-03-18。"],[],[]]