* [Home](https://docs.cloud.google.com/?hl=zh-cn)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-cn)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-cn)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-cn)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-cn)

发送反馈



使用集合让一切井井有条

根据您的偏好保存内容并对其进行分类。

# 数据转换简介

本文档介绍了在 BigQuery 表中转换数据的不同方式。

如需详细了解数据集成，请参阅[加载、转换和导出数据简介](https://docs.cloud.google.com/bigquery/docs/load-transform-export-intro?hl=zh-cn)。

## 转换数据的方法

您可以通过以下方式转换 BigQuery 中的数据：

* 使用[数据操纵语言 (DML)](#transform-with-dml) 转换 BigQuery 表中的数据。
* 使用[物化视图](#transform-with-mvs)自动缓存查询结果，以提高性能和效率。
* 使用[持续查询](#transform-with-continuous-queries)实时分析传入的数据，并将输出行持续插入 BigQuery 表中，或导出到 Pub/Sub 或 Bigtable。
* 使用 [BigQuery 流水线](#transform-with-bq-pipelines)或 [Dataform](#transform-with-dataform) 在 BigQuery 中开发、测试、安排流水线并进行版本控制。
* 使用[数据准备](#data-preparation)功能，该功能可提供具备上下文感知能力的 AI 生成转换建议，帮助您清理数据以便进行分析。数据准备由 [Dataform API](https://docs.cloud.google.com/dataform/reference/rest?hl=zh-cn) 提供支持。

下表显示了每种转换方法的不同特征。

| 转换方法 | 转换目标 | 定义方法 | 转换频率 |
| --- | --- | --- | --- |
| [数据操纵语言 (DML)](#transform-with-dml) | [表（就地）](https://docs.cloud.google.com/bigquery/docs/tables-intro?hl=zh-cn) | [SQL DML](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/dml-syntax?hl=zh-cn) | 用户发起的或预定的 |
| [具体化视图](#transform-with-mvs) | [物化视图](https://docs.cloud.google.com/bigquery/docs/materialized-views-intro?hl=zh-cn) | [SQL 查询](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-cn) | 自动或手动刷新 |
| [持续查询](#transform-with-continuous-queries) | [表](https://docs.cloud.google.com/bigquery/docs/tables-intro?hl=zh-cn)、[Pub/Sub 主题](https://docs.cloud.google.com/bigquery/docs/continuous-queries?hl=zh-cn#pubsub-example)、[Bigtable 表](https://docs.cloud.google.com/bigquery/docs/continuous-queries?hl=zh-cn#bigtable-example) | [包含 EXPORT DATA 的 SQL 查询](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/export-statements?hl=zh-cn#export_data_statement) | 连续 |
| [Dataform](#transform-with-dataform) | [表格](https://docs.cloud.google.com/bigquery/docs/tables-intro?hl=zh-cn) | [Dataform 核心 (SQLX)](https://docs.cloud.google.com/dataform/docs/overview?hl=zh-cn#dataform-core) | 预定（流水线） |
| [BigQuery 流水线](#transform-with-bq-pipelines) | [表格](https://docs.cloud.google.com/bigquery/docs/tables-intro?hl=zh-cn) | [BigQuery 流水线](https://docs.cloud.google.com/bigquery/docs/pipelines-introduction?hl=zh-cn) | 预定（流水线） |
| [数据准备](#data-preparation) | [表格](https://docs.cloud.google.com/bigquery/docs/tables-intro?hl=zh-cn) | [可视化编辑器](https://docs.cloud.google.com/bigquery/docs/data-prep-get-suggestions?hl=zh-cn#open-data-prep-editor) | 预定 |

您还可以[查看 BigQuery 表格的更改历史记录](https://docs.cloud.google.com/bigquery/docs/change-history?hl=zh-cn)，以检查在指定时间范围内对表进行的转换。

### 使用 DML 转换数据

您可以使用[数据操纵语言 (DML)](https://docs.cloud.google.com/bigquery/docs/data-manipulation-language?hl=zh-cn) 来转换 BigQuery 表中的数据。DML 语句是 GoogleSQL 查询，这些查询可以操控现有的表数据以添加或删除行、修改现有行中的数据，或者将数据与其他表中的值合并。[分区表](https://docs.cloud.google.com/bigquery/docs/using-dml-with-partitioned-tables?hl=zh-cn)也支持 DML 转换。

您可以并发运行多个 DML 语句，其中 BigQuery 会将多个 DML 语句排成队列依次转换数据。
BigQuery 根据转换类型来管理[并发 DML 语句的运行方式](https://docs.cloud.google.com/bigquery/docs/data-manipulation-language?hl=zh-cn#concurrent_jobs)。

### 使用物化视图转换数据

[物化视图](https://docs.cloud.google.com/bigquery/docs/materialized-views-intro?hl=zh-cn)是预计算视图，可定期缓存 SQL 查询结果以提高性能和效率。BigQuery 利用来自物化视图的预计算结果，并尽可能只从基表中读取更改以计算最新结果。

当基表发生变化时，系统会在后台预计算物化视图。基表中的任何增量数据更改都会自动添加到物化视图，无需用户执行任何操作。

### 使用持续查询转换数据

**预览版**

此功能 受[服务专用条款](https://docs.cloud.google.com/terms/service-terms?hl=zh-cn#1)的约束。 非正式版功能“按原样”提供，且可能仅提供有限支持。
如需了解详情，请参阅[发布阶段说明](https://cloud.google.com/products/?hl=zh-cn#product-launch-stages)。

[持续查询](https://docs.cloud.google.com/bigquery/docs/continuous-queries-introduction?hl=zh-cn)是持续运行的 SQL 语句。借助持续查询，您可以实时分析 BigQuery 中的传入数据。您可以将持续查询生成的输出行插入 BigQuery 表中，也可以将其导出到 Pub/Sub 或 Bigtable。

### 使用 Dataform 转换数据

借助 Dataform，您可以在数据集成的提取、加载和转换 (ELT) 流程中管理数据转换。从源系统中提取原始数据并将其加载到 BigQuery 后，您可以使用 Dataform 将其转换为整理、测试和记录的表套件。在 DML 中，您采用命令式方式，告知 BigQuery 如何转换数据，而在 Dataform 中，您可以编写声明式语句，让 Dataform 确定实现该状态所需的转换。

在 Dataform 中，您可以开发、测试[数据转换的 SQL 工作流](https://docs.cloud.google.com/dataform/docs/sql-workflows?hl=zh-cn)并进行版本控制，从数据源声明到输出表、视图或具体化视图。您可以使用 Dataform 核心或纯 JavaScript 开发 SQL 工作流。
[Dataform 核心](https://docs.cloud.google.com/dataform/docs/overview?hl=zh-cn#dataform-core)是一种开源元语言，使用 SQLX 和 JavaScript 扩展 SQL。您可以使用 Dataform Core 管理依赖项，设置自动化数据质量测试，以及在代码中记录表或列说明。

Dataform 将您的 SQL 工作流代码存储在[仓库](https://docs.cloud.google.com/dataform/docs/create-repository?hl=zh-cn)中，并使用 Git 跟踪文件更改。借助 Dataform 中的开发工作区，您可以处理仓库的内容，而不会影响同一仓库中其他人员的工作。您可以将 Dataform 仓库连接到第三方 Git 提供商，包括 Azure DevOps Services、Bitbucket、GitHub 和 GitLab。

您可以使用 Dataform 版本配置和工作流配置运行或安排 SQL 工作流。
或者，您也可以使用 Cloud Composer 或 Workflows 和 Cloud Scheduler 来安排执行。在执行期间，Dataform 会根据 SQL 工作流中的对象依赖项在 BigQuery 中执行 SQL 查询。执行后，您可以使用定义的表和视图在 BigQuery 中进行分析。

如需详细了解如何在 Dataform 中创建数据转换 SQL 工作流，请参阅 [Dataform 概览](https://docs.cloud.google.com/dataform/docs/overview?hl=zh-cn)和 [Dataform 功能](https://docs.cloud.google.com/dataform/docs/overview?hl=zh-cn#features)。

### 使用 BigQuery 流水线转换数据

BigQuery 流水线由 Dataform 提供支持，可让您在提取、加载、转换 (ELT) 或提取、转换、加载 (ETL) 流程中创建和管理数据转换。

您可以在 BigQuery Studio 中以直观的方式创建和管理 BigQuery 流水线。

如需详细了解如何创建 BigQuery 流水线，请参阅[创建流水线](https://docs.cloud.google.com/bigquery/docs/create-pipelines?hl=zh-cn)。

### 在 BigQuery 中准备数据

为了减少数据准备工作量，BigQuery 可让您根据 Gemini 生成的转换建议来清理数据。BigQuery 中的数据准备可提供以下帮助：

* 应用转换和数据质量规则
* 标准化和丰富数据
* 自动化架构映射

您可以在预览数据中验证结果，然后再对所有数据执行更改。

如需了解详情，请参阅 [BigQuery 数据准备简介](https://docs.cloud.google.com/bigquery/docs/data-prep-introduction?hl=zh-cn)。

## 后续步骤

* 如需详细了解 DML，请参阅[使用数据操纵语言 (DML) 转换数据](https://docs.cloud.google.com/bigquery/docs/data-manipulation-language?hl=zh-cn)。
* 如需详细了解 Dataform，请参阅 [Dataform 概览](https://docs.cloud.google.com/dataform/docs/overview?hl=zh-cn)。




发送反馈

如未另行说明，那么本页面中的内容已根据[知识共享署名 4.0 许可](https://creativecommons.org/licenses/by/4.0/)获得了许可，并且代码示例已根据 [Apache 2.0 许可](https://www.apache.org/licenses/LICENSE-2.0)获得了许可。有关详情，请参阅 [Google 开发者网站政策](https://developers.google.com/site-policies?hl=zh-cn)。Java 是 Oracle 和/或其关联公司的注册商标。

最后更新时间 (UTC)：2026-03-17。




需要向我们提供更多信息？

[[["易于理解","easyToUnderstand","thumb-up"],["解决了我的问题","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["很难理解","hardToUnderstand","thumb-down"],["信息或示例代码不正确","incorrectInformationOrSampleCode","thumb-down"],["没有我需要的信息/示例","missingTheInformationSamplesINeed","thumb-down"],["翻译问题","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["最后更新时间 (UTC)：2026-03-17。"],[],[]]