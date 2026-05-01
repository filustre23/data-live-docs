* [Home](https://docs.cloud.google.com/?hl=zh-cn)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-cn)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-cn)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-cn)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-cn)

发送反馈



使用集合让一切井井有条

根据您的偏好保存内容并对其进行分类。

# 连接简介

借助 BigQuery，您可以创建外部连接来查询存储在 BigQuery 之外的 Google Cloud 服务（如 Cloud Storage 或 Spanner）或第三方来源（如 Amazon Web Services [AWS] 或 Microsoft Azure）中的数据。这些外部连接使用 BigQuery Connection API。

例如，假设您在 Cloud SQL 中存储有关客户订单的详细信息，在 BigQuery 中存储有关销售的数据，并且您希望在单个查询中联接这两个表。您可以使用 BigQuery Connection API 创建与外部数据库的 Cloud SQL 连接。通过连接，您永远不会以[明文](https://simple.wikipedia.org/wiki/Cleartext)形式发送数据库凭据。

连接会经过加密并安全地存储在 BigQuery 连接服务中。您可以通过向用户授予 BigQuery 连接 Identity and Access Management (IAM) 角色，[为用户提供连接访问权限](https://docs.cloud.google.com/bigquery/docs/working-with-connections?hl=zh-cn#share-connections)。

## 连接类型

BigQuery 会为以下外部数据源提供不同的连接类型：

* Amazon Simple Storage Service (Amazon S3)
* Apache Spark
* Azure Blob Storage
* Google Cloud 资源，例如 Vertex AI 远程模型、远程函数和 BigLake
* Spanner
* Cloud SQL
* AlloyDB for PostgreSQL
* SAP Datasphere

**注意**：您无需连接即可查询 [Bigtable](https://docs.cloud.google.com/bigquery/docs/external-data-bigtable?hl=zh-cn) 和 [Google 云端硬盘](https://docs.cloud.google.com/bigquery/docs/external-data-drive?hl=zh-cn)中的数据。

### Amazon S3 连接

如需使用 BigQuery Omni 创建 Amazon S3 连接，请参阅[连接到 Amazon S3](https://docs.cloud.google.com/bigquery/docs/omni-aws-create-connection?hl=zh-cn)。

建立 Amazon S3 连接后，您可以执行以下操作：

* [在 Amazon S3 上创建外部表](https://docs.cloud.google.com/bigquery/docs/omni-aws-create-external-table?hl=zh-cn)
* [查询 Amazon S3 数据](https://docs.cloud.google.com/bigquery/docs/query-aws-data?hl=zh-cn)
* [将结果导出到 Amazon S3](https://docs.cloud.google.com/bigquery/docs/omni-aws-export-results-to-s3?hl=zh-cn)
* [基于 AWS Glue 数据库创建数据集](https://docs.cloud.google.com/bigquery/docs/glue-federated-datasets?hl=zh-cn)。

### Spark 连接

[Spark 的存储过程](https://docs.cloud.google.com/bigquery/docs/spark-procedures?hl=zh-cn)可让您使用 BigQuery 运行以 Python 编写的存储过程。[Spark 连接](https://docs.cloud.google.com/bigquery/docs/connect-to-spark?hl=zh-cn)可让您连接到 Apache Spark 无服务器并运行 Spark 的存储过程。

如需创建此连接，请参阅[创建连接](https://docs.cloud.google.com/bigquery/docs/connect-to-spark?hl=zh-cn#create-spark-connection)。

### Blob Storage 连接

如需使用 BigQuery Omni 创建 Blob Storage 连接，请参阅[连接到 Blob Storage](https://docs.cloud.google.com/bigquery/docs/omni-azure-create-connection?hl=zh-cn)。

建立 Blob Storage 连接后，您可以执行以下操作：

* [基于 Blob Storage 创建外部表](https://docs.cloud.google.com/bigquery/docs/omni-azure-create-external-table?hl=zh-cn)
* [查询 Blob Storage 数据](https://docs.cloud.google.com/bigquery/docs/query-azure-data?hl=zh-cn)
* [将结果导出到 Blob Storage](https://docs.cloud.google.com/bigquery/docs/omni-azure-export-results-to-azure-storage?hl=zh-cn)

### Google Cloud 资源连接

Google Cloud 资源连接是一种用于授权访问其他 Google Cloud资源（例如 Vertex AI 远程模型、远程函数和 BigLake）的连接。如需详细了解如何设置 Google Cloud 资源连接，请参阅[创建和设置 Cloud 资源连接](https://docs.cloud.google.com/bigquery/docs/create-cloud-resource-connection?hl=zh-cn)。

建立 Google Cloud 资源连接后，您可以使用该连接创建以下 BigQuery 对象：

* **远程模型**。如需了解详情，请参阅[用于创建基于 LLM 的远程模型的 CREATE MODEL 语句](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model?hl=zh-cn)、[用于创建基于云 AI 服务的远程模型的 CREATE MODEL 语句](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model-service?hl=zh-cn)，以及[用于创建基于 Vertex AI 托管模型的远程模型的 CREATE MODEL 语句](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model-https?hl=zh-cn)。
* **远程函数**。BigQuery [远程函数](https://docs.cloud.google.com/bigquery/docs/remote-functions?hl=zh-cn)可让您在 Cloud Run functions 或 Cloud Run 中使用任何支持的语言实现函数。借助远程函数连接，您可以连接 Cloud Run functions 或 Cloud Run 并运行这些函数。如需创建 BigQuery 远程函数连接，请参阅[创建连接](https://docs.cloud.google.com/bigquery/docs/remote-functions?hl=zh-cn#create_a_connection)。
* **BigLake 表**。BigLake 连接可将 [BigLake 表](https://docs.cloud.google.com/bigquery/docs/biglake-intro?hl=zh-cn)连接到外部数据源，同时为 Cloud Storage 中的结构化和非结构化数据保留精细的 BigQuery 访问权限控制和安全性。
* **对象表**。如需了解详情，请参阅[对象表简介](https://docs.cloud.google.com/bigquery/docs/object-table-introduction?hl=zh-cn)。

### Spanner 连接

如需创建 Spanner 连接，请参阅[连接到 Spanner](https://docs.cloud.google.com/bigquery/docs/connect-to-spanner?hl=zh-cn)。

建立 Spanner 连接后，您就可以运行[联合查询](https://docs.cloud.google.com/bigquery/docs/federated-queries-intro?hl=zh-cn)了。

### Cloud SQL 连接

如需创建 Cloud SQL 连接，请参阅[连接到 Cloud SQL](https://docs.cloud.google.com/bigquery/docs/connect-to-sql?hl=zh-cn)。

建立 Cloud SQL 连接后，您就可以运行[联合查询](https://docs.cloud.google.com/bigquery/docs/federated-queries-intro?hl=zh-cn)了。

### AlloyDB 连接

如需创建 AlloyDB 连接，请参阅[连接到 AlloyDB for PostgreSQL](https://docs.cloud.google.com/bigquery/docs/connect-to-alloydb?hl=zh-cn)。

建立 AlloyDB 连接后，您就可以运行[联合查询](https://docs.cloud.google.com/bigquery/docs/federated-queries-intro?hl=zh-cn)了。

### SAP Datasphere 连接

**预览版**

此产品或功能 受[服务专用条款](https://docs.cloud.google.com/terms/service-terms?hl=zh-cn#1)的约束。
非正式版产品和功能“按原样”提供，可能只能获得有限的支持。
如需了解详情，请参阅[发布阶段说明](https://cloud.google.com/products/?hl=zh-cn#product-launch-stages)。

如需创建 SAP Datasphere 连接，请参阅[连接到 SAP Datasphere](https://docs.cloud.google.com/bigquery/docs/connect-to-sap-datasphere?hl=zh-cn)。

建立 SAP Datasphere 连接后，您就可以运行[联合查询](https://docs.cloud.google.com/bigquery/docs/federated-queries-intro?hl=zh-cn)了。

## 审核日志

BigQuery 会记录有关连接的使用情况和管理请求。如需了解详情，请参阅 [BigQuery 审核日志概览](https://docs.cloud.google.com/bigquery/docs/reference/auditlogs?hl=zh-cn)。

## 后续步骤

* 了解如何[管理连接](https://docs.cloud.google.com/bigquery/docs/working-with-connections?hl=zh-cn)。
* 详细了解项目的[默认连接](https://docs.cloud.google.com/bigquery/docs/default-connections?hl=zh-cn)。
* 了解如何[使用远程函数分析对象表](https://docs.cloud.google.com/bigquery/docs/object-table-remote-function?hl=zh-cn)。
* 了解如何查询存储的数据：
  + [查询存储在 Amazon S3 中的数据](https://docs.cloud.google.com/bigquery/docs/omni-aws-create-external-table?hl=zh-cn)。
  + [查询存储在 Blob Storage 中的数据](https://docs.cloud.google.com/bigquery/docs/omni-azure-create-external-table?hl=zh-cn)。
  + [查询存储在 Cloud Storage 中的结构化数据](https://docs.cloud.google.com/bigquery/docs/query-cloud-storage-using-biglake?hl=zh-cn#query-biglake-table-bigquery)。
  + [查询存储在 Cloud Storage 中的非结构化数据](https://docs.cloud.google.com/bigquery/docs/object-tables?hl=zh-cn)。
  + [查询存储在 Spanner 中的数据](https://docs.cloud.google.com/bigquery/docs/spanner-federated-queries?hl=zh-cn)。
  + [查询存储在 Cloud SQL 中的数据](https://docs.cloud.google.com/bigquery/docs/cloud-sql-federated-queries?hl=zh-cn)。
  + [查询存储在 AlloyDB 中的数据](https://docs.cloud.google.com/bigquery/docs/alloydb-federated-queries?hl=zh-cn)。
  + [使用远程函数查询数据](https://docs.cloud.google.com/bigquery/docs/remote-functions?hl=zh-cn#create_a_remote_function)。
  + [使用远程函数查询非结构化数据](https://docs.cloud.google.com/bigquery/docs/object-table-remote-function?hl=zh-cn)。
  + [使用 Apache Spark 的存储过程查询数据](https://docs.cloud.google.com/bigquery/docs/spark-procedures?hl=zh-cn)。
* 了解[外部表](https://docs.cloud.google.com/bigquery/docs/external-tables?hl=zh-cn)。




发送反馈

如未另行说明，那么本页面中的内容已根据[知识共享署名 4.0 许可](https://creativecommons.org/licenses/by/4.0/)获得了许可，并且代码示例已根据 [Apache 2.0 许可](https://www.apache.org/licenses/LICENSE-2.0)获得了许可。有关详情，请参阅 [Google 开发者网站政策](https://developers.google.com/site-policies?hl=zh-cn)。Java 是 Oracle 和/或其关联公司的注册商标。

最后更新时间 (UTC)：2026-03-17。




需要向我们提供更多信息？

[[["易于理解","easyToUnderstand","thumb-up"],["解决了我的问题","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["很难理解","hardToUnderstand","thumb-down"],["信息或示例代码不正确","incorrectInformationOrSampleCode","thumb-down"],["没有我需要的信息/示例","missingTheInformationSamplesINeed","thumb-down"],["翻译问题","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["最后更新时间 (UTC)：2026-03-17。"],[],[]]