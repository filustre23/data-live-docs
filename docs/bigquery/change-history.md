* [Home](https://docs.cloud.google.com/?hl=zh-cn)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-cn)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-cn)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-cn)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-cn)

发送反馈



使用集合让一切井井有条

根据您的偏好保存内容并对其进行分类。

# 使用更改历史记录

**预览版**

此产品或功能 受[服务专用条款](https://docs.cloud.google.com/terms/service-terms?hl=zh-cn#1)的约束。
非正式版产品和功能“按原样”提供，可能只能获得有限的支持。
如需了解详情，请参阅[发布阶段说明](https://cloud.google.com/products/?hl=zh-cn#product-launch-stages)。

**注意：**如需在预览版期间获得支持，请联系 [bq-change-history-feedback@google.com](mailto:bq-change-history-feedback@google.com)。

通过 BigQuery 更改历史记录，您可以跟踪 BigQuery 表的更改历史记录。 您可以使用 GoogleSQL [函数](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/table-functions-built-in?hl=zh-cn)查看指定时间范围内所做的特定类型的更改，以便处理对表所做的增量更改。了解对表进行了哪些更改可帮助您在 BigQuery 外部执行逐步维护表副本等操作，同时避免费用高昂的副本。

## 所需权限

如需查看某个表的更改历史记录，您需要拥有该表的 `bigquery.tables.getData` 权限。以下预定义的 Identity and Access Management (IAM) 角色包含此权限：

* `roles/bigquery.dataViewer`
* `roles/bigquery.dataEditor`
* `roles/bigquery.dataOwner`
* `roles/bigquery.admin`

如果表具有或以前具有[行级访问权限政策](https://docs.cloud.google.com/bigquery/docs/row-level-security-intro?hl=zh-cn)，则只有表管理员可以访问表的历史数据。表需要 `bigquery.rowAccessPolicies.overrideTimeTravelRestrictions` 权限，它包含在预定义的 `roles/bigquery.admin` IAM 角色中。

如果表具有列级安全性，则您只能查看您有权访问的列的更改历史记录。

## 更改历史记录函数

您可以使用以下函数来了解表的更改历史记录：

* [`APPENDS`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/time-series-functions?hl=zh-cn#appends)：返回给定时间范围内附加到表的所有行。

  以下操作会将行添加到 `APPENDS` 更改历史记录中：

  + [`CREATE TABLE` DDL 语句](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-cn#create_table_statement)
  + [`INSERT` DML 语句](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/dml-syntax?hl=zh-cn#insert_statement)
  + [作为 `MERGE` DML 语句的一部分附加的数据](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/dml-syntax?hl=zh-cn#merge_statement)
  + [加载数据](https://docs.cloud.google.com/bigquery/docs/loading-data?hl=zh-cn)到 BigQuery 中
  + [流式提取](https://docs.cloud.google.com/bigquery/docs/write-api?hl=zh-cn)
* [`CHANGES`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/time-series-functions?hl=zh-cn#changes)：返回给定时间范围内表中所有已更改的行。如需对表使用 `CHANGES` 函数，您必须将表的 [`enable_change_history` 选项](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-cn#table_option_list)设置为 `TRUE`。

  以下操作会将行添加到 `CHANGES` 更改历史记录中：

  + [`CREATE TABLE` DDL 语句](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-cn#create_table_statement)
  + [`INSERT` DML 语句](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/dml-syntax?hl=zh-cn#insert_statement)
  + [作为 `MERGE` DML 语句的一部分附加或更改的数据](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/dml-syntax?hl=zh-cn#merge_statement)
  + [`UPDATE` DML 语句](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/dml-syntax?hl=zh-cn#update_statement)
  + [`DELETE` DML 语句](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/dml-syntax?hl=zh-cn#delete_statement)
  + [加载数据](https://docs.cloud.google.com/bigquery/docs/loading-data?hl=zh-cn)到 BigQuery 中
  + [流式提取](https://docs.cloud.google.com/bigquery/docs/write-api?hl=zh-cn)
  + [`TRUNCATE TABLE` DML 语句](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/dml-syntax?hl=zh-cn#truncate_table_statement)
  + 配置了 `writeDisposition` 为 `WRITE_TRUNCATE` 的[作业](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-cn)
  + 单独的[表分区删除](https://docs.cloud.google.com/bigquery/docs/managing-partitioned-tables?hl=zh-cn#delete_a_partition)

## 价格和费用

调用更改历史记录函数会产生 [BigQuery 计算费用](https://cloud.google.com/bigquery/pricing?hl=zh-cn#analysis_pricing_models)。
`APPENDS` 和 `CHANGES` 函数都需要处理写入指定时间范围内的表中的所有数据。此处理适用于所有写入操作，包括附加和变更操作。
将表的 [`enable_change_history` 选项](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-cn#table_option_list)设置为 `FALSE` 不会减少 `APPENDS` 处理的数据量。

如果您将表的 [`enable_change_history` 选项](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-cn#table_option_list)设置为 `TRUE` 以使用 `CHANGES` 函数，则 BigQuery 会存储表更改元数据。存储的这些元数据会产生额外的 [BigQuery 存储费用](https://cloud.google.com/bigquery/pricing?hl=zh-cn#storage)和 [BigQuery 计算费用](https://cloud.google.com/bigquery/pricing?hl=zh-cn#analysis_pricing_models)。
账单金额取决于对表所做的更改的数量和类型，通常很小。包含许多更改操作（尤其是大量删除操作）的表最有可能产生明显的费用。




发送反馈

如未另行说明，那么本页面中的内容已根据[知识共享署名 4.0 许可](https://creativecommons.org/licenses/by/4.0/)获得了许可，并且代码示例已根据 [Apache 2.0 许可](https://www.apache.org/licenses/LICENSE-2.0)获得了许可。有关详情，请参阅 [Google 开发者网站政策](https://developers.google.com/site-policies?hl=zh-cn)。Java 是 Oracle 和/或其关联公司的注册商标。

最后更新时间 (UTC)：2026-02-12。




需要向我们提供更多信息？

[[["易于理解","easyToUnderstand","thumb-up"],["解决了我的问题","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["很难理解","hardToUnderstand","thumb-down"],["信息或示例代码不正确","incorrectInformationOrSampleCode","thumb-down"],["没有我需要的信息/示例","missingTheInformationSamplesINeed","thumb-down"],["翻译问题","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["最后更新时间 (UTC)：2026-02-12。"],[],[]]