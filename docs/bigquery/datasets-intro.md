* [Home](https://docs.cloud.google.com/?hl=zh-cn)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-cn)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-cn)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-cn)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-cn)

发送反馈



使用集合让一切井井有条

根据您的偏好保存内容并对其进行分类。

# 数据集简介

此页面简要介绍 BigQuery 中的数据集。

## 数据集

数据集包含在特定[项目](https://docs.cloud.google.com/docs/overview?hl=zh-cn#projects)中，数据集是用来组织和控制[表](https://docs.cloud.google.com/bigquery/docs/tables?hl=zh-cn)和[视图](https://docs.cloud.google.com/bigquery/docs/views?hl=zh-cn)访问权限的顶级容器。表或视图必须属于数据集，因此需要创建至少一个数据集，才能[将数据加载到 BigQuery](https://docs.cloud.google.com/bigquery/loading-data-into-bigquery?hl=zh-cn) 中。
使用 GoogleSQL 时，请使用 `projectname.datasetname` 格式来完全限定数据集名称；使用 bq 命令行工具时，请使用 `projectname:datasetname` 格式来完全限定数据集名称。

## 位置

您在创建数据集时会指定一个位置用于存储 BigQuery 数据。如需查看 BigQuery 数据集位置的列表，请参阅 [BigQuery 位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-cn)。创建数据集后，该位置无法更改，但您可以[将数据集复制到其他位置](https://docs.cloud.google.com/bigquery/docs/copying-datasets?hl=zh-cn)，也可以手动[将数据集移动到其他位置（在其他位置重新创建数据集）](https://docs.cloud.google.com/bigquery/docs/managing-datasets?hl=zh-cn#recreate-dataset)。

BigQuery 在包含待查询表的数据集所在的位置处理查询。BigQuery根据[服务专用条款](https://cloud.google.com/terms/service-terms?hl=zh-cn)将您的数据存储在选定位置。

## 数据保留

数据集将[时间旅行](https://docs.cloud.google.com/bigquery/docs/time-travel?hl=zh-cn#time_travel)与[故障安全期](https://docs.cloud.google.com/bigquery/docs/time-travel?hl=zh-cn#fail-safe)结合使用，以将已删除和修改的数据保留一小段时间，以防您需要恢复数据。如需了解详情，请参阅[使用时间旅行和故障安全功能保留数据](https://docs.cloud.google.com/bigquery/docs/time-travel?hl=zh-cn)。

## 存储空间结算模式

您可以按逻辑字节数或物理（压缩）字节数或者两者的组合来为 BigQuery 数据存储空间付费。您选择的存储结算模式决定了[存储价格](https://cloud.google.com/bigquery/pricing?hl=zh-cn#storage)。您选择的存储空间结算模式不会影响 BigQuery 性能。无论您选择哪种结算模式，您的数据都会以物理字节的形式存储。

您可以在数据集级层设置存储结算模式。如果您在创建数据集时未指定存储结算模式，则系统默认为使用逻辑存储结算。不过，您可以在创建数据集后[更改数据集的存储结算模式](https://docs.cloud.google.com/bigquery/docs/updating-datasets?hl=zh-cn#update_storage_billing_models)。如果您更改了数据集的存储结算模式，则必须等待 14 天才能再次更改存储结算模式。

更改数据集的结算模式后，更改需要 24 小时才能生效。 更改数据集的结算模式时，长期存储中的任何表或表分区都不会重置为活跃存储。
更改数据集的结算模式不会影响查询性能和查询延迟时间。

数据集使用[时间旅行](https://docs.cloud.google.com/bigquery/docs/time-travel?hl=zh-cn#time_travel)和[故障安全](https://docs.cloud.google.com/bigquery/docs/time-travel?hl=zh-cn#fail-safe)存储进行数据保留。如果您使用物理存储空间结算模式，系统会按活跃存储空间费率单独收取时间旅行和故障安全存储空间费用；但如果您使用逻辑存储空间结算模式，系统会将这两项费用计入基本费率中。您可以修改为数据集使用的时间旅行窗口，以在物理存储空间费用和数据保留之间实现平衡。您无法修改故障安全窗口。如需详细了解数据集数据保留，请参阅[使用时间旅行和故障安全功能保留数据](https://docs.cloud.google.com/bigquery/docs/time-travel?hl=zh-cn)。如需详细了解如何预测存储费用，请参阅[预测存储结算](https://docs.cloud.google.com/bigquery/docs/information-schema-table-storage?hl=zh-cn#forecast_storage_billing)。

如果组织的任何现有旧版[固定费率槽承诺](https://docs.cloud.google.com/bigquery/docs/reservations-commitments-legacy?hl=zh-cn)位于数据集所在的区域，则无法将数据集加入物理存储空间结算。这不适用于通过 [BigQuery 版本](https://docs.cloud.google.com/bigquery/docs/editions-intro?hl=zh-cn)购买的承诺。

## 外部数据集

除了 BigQuery 数据集之外，您还可以创建外部数据集，即指向外部数据源的链接：

* [Spanner 外部数据集](https://docs.cloud.google.com/bigquery/docs/spanner-external-datasets?hl=zh-cn)
* [AWS Glue 联合数据集](https://docs.cloud.google.com/bigquery/docs/glue-federated-datasets?hl=zh-cn)

外部数据集也称为联合数据集；这两个术语可互换使用。

创建后，外部数据集将包含引用的外部数据源中的表。这些表中的数据不会复制到 BigQuery 中，而是在每次使用时进行查询。如需了解详情，请参阅 [Spanner 联合查询](https://docs.cloud.google.com/bigquery/docs/spanner-federated-queries?hl=zh-cn)。

## 限制

BigQuery 数据集有以下限制：

* [数据集位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-cn)只能在创建时设置。创建数据集后，就无法再更改其位置。
* 查询中引用的所有表必须存储在位于同一位置的数据集中。
* 外部数据集不支持表到期、副本、时间旅行、默认排序规则、默认舍入模式，或用于启用或停用不区分大小写的表名称的选项。
* [复制表](https://docs.cloud.google.com/bigquery/docs/managing-tables?hl=zh-cn#copy-table)时，包含源表和目标表的数据集必须位于同一位置。
* 各个项目的数据集名称不得重复。
* 如果您更改了数据集的[存储空间结算模式](#dataset_storage_billing_models)，则必须等待 14 天才能再次更改存储空间结算模式。
* 如果您的任何现有旧版[固定费率槽承诺](https://docs.cloud.google.com/bigquery/docs/reservations-commitments-legacy?hl=zh-cn)位于数据集所在的区域，则无法将数据集加入物理存储空间结算。

## 配额

要详细了解数据集配额和限制，请参阅[配额和限制](https://docs.cloud.google.com/bigquery/quotas?hl=zh-cn#dataset_limits)。

## 价格

您无需为创建、更新或删除数据集付费。

要详细了解 BigQuery 价格，请参阅[价格](https://cloud.google.com/bigquery/pricing?hl=zh-cn)。

## 安全性

如需控制对 BigQuery 中数据集的访问权限，请参阅[控制对数据集的访问权限](https://docs.cloud.google.com/bigquery/docs/control-access-to-resources-iam?hl=zh-cn)。
如需了解数据加密，请参阅[静态加密](https://docs.cloud.google.com/bigquery/docs/encryption-at-rest?hl=zh-cn)。

## 后续步骤

* 如需详细了解如何创建数据集，请参阅[创建数据集](https://docs.cloud.google.com/bigquery/docs/datasets?hl=zh-cn)。
* 如需详细了解如何向数据集分配访问权限控制，请参阅[控制数据集访问权限](https://docs.cloud.google.com/bigquery/docs/dataset-access-controls?hl=zh-cn)。




发送反馈

如未另行说明，那么本页面中的内容已根据[知识共享署名 4.0 许可](https://creativecommons.org/licenses/by/4.0/)获得了许可，并且代码示例已根据 [Apache 2.0 许可](https://www.apache.org/licenses/LICENSE-2.0)获得了许可。有关详情，请参阅 [Google 开发者网站政策](https://developers.google.com/site-policies?hl=zh-cn)。Java 是 Oracle 和/或其关联公司的注册商标。

最后更新时间 (UTC)：2026-03-16。




需要向我们提供更多信息？

[[["易于理解","easyToUnderstand","thumb-up"],["解决了我的问题","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["很难理解","hardToUnderstand","thumb-down"],["信息或示例代码不正确","incorrectInformationOrSampleCode","thumb-down"],["没有我需要的信息/示例","missingTheInformationSamplesINeed","thumb-down"],["翻译问题","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["最后更新时间 (UTC)：2026-03-16。"],[],[]]