* [Home](https://docs.cloud.google.com/?hl=zh-cn)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-cn)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-cn)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-cn)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-cn)

发送反馈



使用集合让一切井井有条

根据您的偏好保存内容并对其进行分类。

# 恢复已删除的数据集

**预览版**

此功能 受[服务专用条款](https://docs.cloud.google.com/terms/service-terms?hl=zh-cn#1)的约束。 非正式版功能“按原样”提供，且可能仅提供有限支持。
如需了解详情，请参阅[发布阶段说明](https://cloud.google.com/products/?hl=zh-cn#product-launch-stages)。

**注意：**如需提供反馈或提出与此预览版相关的问题，请联系 [bq-dataset-undelete-feedback@google.com](mailto:bq-dataset-undelete-feedback@google.com)。

本文档介绍了如何在 BigQuery 中恢复（或恢复删除）已删除的数据集。

您可以恢复数据集，以将其恢复到删除时的状态。您只能恢复处于[时间旅行窗口](https://docs.cloud.google.com/bigquery/docs/time-travel?hl=zh-cn#time_travel)内的数据集。这种恢复包括数据集中包含的所有对象、数据集属性和安全设置。对于未恢复的资源，请参阅[限制](#limitations)。

**注意：**您只能恢复给定数据集 ID 的最新数据集。如果您删除了某个数据集，然后创建了具有相同 ID 的新数据集，则无法恢复删除的原始数据集。不过，您或许仍然可以[从已删除的数据集中恢复特定表](https://docs.cloud.google.com/bigquery/docs/managing-datasets?hl=zh-cn#restore-delete-tables)。

如需了解如何恢复已删除的表或快照，请参阅以下资源：

* [恢复已删除的表](https://docs.cloud.google.com/bigquery/docs/restore-deleted-tables?hl=zh-cn)
* [恢复表快照](https://docs.cloud.google.com/bigquery/docs/table-snapshots-restore?hl=zh-cn)

## 限制

以下是与恢复数据集相关的限制列表：

* 恢复的数据集可能会引用不再存在的安全主体。
* 执行此操作时，系统不会恢复关联数据集中对已删除数据集的引用。订阅方必须重新订阅才能手动恢复链接。
* 执行此操作时，系统不会恢复业务标记。
* 您必须[手动刷新物化视图](https://docs.cloud.google.com/bigquery/docs/materialized-views-manage?hl=zh-cn#manual-refresh)并向[授权视图](https://docs.cloud.google.com/bigquery/docs/authorized-views?hl=zh-cn#manage_users_or_groups_for_authorized_views)、[授权数据集](https://docs.cloud.google.com/bigquery/docs/authorized-datasets?hl=zh-cn#authorize_a_dataset)和[授权例程](https://docs.cloud.google.com/bigquery/docs/authorized-routines?hl=zh-cn#authorize_routines)重新授权。
* 您无法直接恢复逻辑视图。不过，您可以恢复删除数据集或重新创建视图，以恢复逻辑视图。如需详细了解这些解决方法，请参阅[恢复视图](https://docs.cloud.google.com/bigquery/docs/managing-views?hl=zh-cn#restore_a_view)。
* [已启用 BigQuery CDC 的表](https://docs.cloud.google.com/bigquery/docs/change-data-capture?hl=zh-cn)在作为恢复删除的数据集的一部分恢复时，不会恢复后台应用作业。
* 恢复的数据集最长可能需要 24 小时才会显示在 BigQuery 搜索结果中。

  删除授权资源（视图、数据集和例程）后，最长可能需要 24 小时才能删除授权。因此，如果您在删除后 24 小时内恢复包含授权资源的数据集，则可能不需要重新授权。最佳实践是始终在恢复资源后验证授权。

## 准备工作

确保您拥有必要的 Identity and Access Management (IAM) 权限，以恢复已删除的数据集。

### 所需的角色

如需获得恢复已删除数据集所需的权限，请让您的管理员为您授予项目的 [BigQuery User](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-cn#bigquery.user) (`roles/bigquery.user`) IAM 角色。如需详细了解如何授予角色，请参阅[管理对项目、文件夹和组织的访问权限](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-cn)。

此预定义角色包含恢复已删除数据集所需的权限。如需查看所需的确切权限，请展开**所需权限**部分：

#### 所需权限

您必须具备以下权限才能恢复已删除数据集：

* 针对项目的  `bigquery.datasets.create` 权限
* 针对数据集的 `bigquery.datasets.get` 权限

您也可以使用[自定义角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-cn)或其他[预定义角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-cn#predefined)来获取这些权限。

## 恢复数据集

如需恢复数据集，请选择以下选项之一：

### SQL

使用 [`UNDROP SCHEMA` 数据定义语言 (DDL) 语句](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-cn#undrop_schema_statement)：

1. 在 Google Cloud 控制台中，前往 **BigQuery** 页面。

   [转到 BigQuery](https://console.cloud.google.com/bigquery?hl=zh-cn)
2. 在查询编辑器中，输入以下语句：

   ```
   UNDROP SCHEMA DATASET_ID;
   ```

   将 `DATASET_ID` 替换为您要执行恢复删除操作的数据集。
3. [指定您要执行恢复删除操作的数据集的位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-cn#specify_locations)。 如需指定 SQL 语句的位置部分，请使用 `location` 选项

   ```
   UNDROP SCHEMA DATASET_ID OPTIONS (location=location);
   ```
4. 点击 play\_circle **运行**。

如需详细了解如何运行查询，请参阅[运行交互式查询](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-cn#queries)。

### API

调用 [`datasets.undelete` 方法](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/datasets/undelete?hl=zh-cn)。

**注意**：如果您的项目中有两个同名的已删除数据集位于两个不同的区域中，则使用 BigQuery API 恢复删除的数据集只会对随机选择的一个数据集执行恢复删除操作，除非指定了位置。

恢复数据集时，可能会出现以下错误：

* `ALREADY_EXISTS`：您尝试在其中执行恢复操作的区域中已存在同名的数据集。您无法使用恢复删除来覆盖或合并数据集。
* `NOT_FOUND`：您尝试恢复的数据集已超过其时间旅行窗口、从未存在，或者您未[指定正确的数据集位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-cn#specify_locations)。
* `ACCESS_DENIED`：您没有对此数据集执行恢复删除操作所需的[权限](#before-you-begin)。

  ## 后续步骤
* 如需了解如何查询某个时间点的数据，请参阅[访问历史数据](https://docs.cloud.google.com/bigquery/docs/access-historical-data?hl=zh-cn)。
* 如需了解数据保留，请参阅[使用时间旅行和故障安全功能保留数据](https://docs.cloud.google.com/bigquery/docs/time-travel?hl=zh-cn)。
* 如需了解如何删除数据集，请参阅[管理数据集](https://docs.cloud.google.com/bigquery/docs/managing-datasets?hl=zh-cn)。




发送反馈

如未另行说明，那么本页面中的内容已根据[知识共享署名 4.0 许可](https://creativecommons.org/licenses/by/4.0/)获得了许可，并且代码示例已根据 [Apache 2.0 许可](https://www.apache.org/licenses/LICENSE-2.0)获得了许可。有关详情，请参阅 [Google 开发者网站政策](https://developers.google.com/site-policies?hl=zh-cn)。Java 是 Oracle 和/或其关联公司的注册商标。

最后更新时间 (UTC)：2026-02-10。




需要向我们提供更多信息？

[[["易于理解","easyToUnderstand","thumb-up"],["解决了我的问题","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["很难理解","hardToUnderstand","thumb-down"],["信息或示例代码不正确","incorrectInformationOrSampleCode","thumb-down"],["没有我需要的信息/示例","missingTheInformationSamplesINeed","thumb-down"],["翻译问题","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["最后更新时间 (UTC)：2026-02-10。"],[],[]]