* [Home](https://docs.cloud.google.com/?hl=zh-cn)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-cn)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-cn)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-cn)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-cn)

发送反馈



使用集合让一切井井有条

根据您的偏好保存内容并对其进行分类。

# 搜索资源

**预览版**

此功能 受[服务专用条款](https://docs.cloud.google.com/terms/service-terms?hl=zh-cn#1)的约束。 非正式版功能“按原样”提供，且可能仅提供有限支持。
如需了解详情，请参阅[发布阶段说明](https://cloud.google.com/products/?hl=zh-cn#product-launch-stages)。

如需了解如何访问此版本，请参阅[访问申请页面](https://docs.google.com/forms/d/e/1FAIpQLSfeucdQXFDYl88JsxPCylt-iU0KxuQMN6VZRalS1vM4ZD0U0Q/viewform?hl=zh-cn)。

使用 Dataplex Universal Catalog 搜索功能查找 BigQuery 中的 Google Cloud 资源，例如 BigQuery 数据集和表。

Dataplex Universal Catalog 搜索支持自然语言搜索查询（也称为语义搜索查询），让您可以使用日常用语搜索资源。

与关键字搜索类似，自然语言搜索通过分析组织中资源的关联元数据，从而更侧重于资源发现。搜索会考虑描述资源的各种元数据，包括您创建的元数据。

自然语言搜索更注重提高召回率，而非精确率。

如需详细了解如何在 BigQuery 中搜索表数据，请参阅 [BigQuery 中的搜索功能简介](https://docs.cloud.google.com/bigquery/docs/search-intro?hl=zh-cn)。

## 注册预览版

如需注册预览版，您的 Google 客户代表必须通过填写[报名表单](https://docs.google.com/forms/d/e/1FAIpQLSfeucdQXFDYl88JsxPCylt-iU0KxuQMN6VZRalS1vM4ZD0U0Q/viewform?hl=zh-cn)提交申请。您提交表单后，BigQuery 团队会与您联系，告知您后续步骤。

## 准备工作

在 BigQuery 中使用自然语言搜索功能搜索Google Cloud 资源之前，请完成本部分中的任务。

### 所需的角色

如需搜索资源，您需要在用于搜索的项目中至少拥有以下一个 [Dataplex Universal Catalog IAM 角色](https://docs.cloud.google.com/dataplex/docs/iam-roles?hl=zh-cn#predefined-roles)：Dataplex Catalog Admin、Dataplex Catalog Editor 或 Dataplex Catalog Viewer。搜索结果的权限检查独立于所选项目。

BigQuery 中的搜索结果会根据您对底层资源的 IAM 权限进行限定。如需在 BigQuery 中搜索资源，您必须拥有访问相应资源的权限。如需了解详情，请参阅本文档的[搜索范围](#search-scope)部分。

例如，如需搜索 BigQuery 数据集、表、视图和模型，您需要拥有访问这些资源的相应权限。如需了解详情，请参阅 [BigQuery 权限](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-cn#bq-permissions)。以下列表介绍了所需的最低权限：

* 如需搜索表，您需要拥有该表的 `bigquery.tables.get` 权限。
* 如需搜索数据集，您需要拥有该数据集的 `bigquery.datasets.get` 权限。

[BigQuery Metadata Viewer 角色](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-cn#bigquery.metadataViewer) (`roles/bigquery.metadataViewer`) 同时包含 `bigquery.tables.get` 和 `bigquery.datasets.get` 权限，可让您搜索任何 BigQuery 资源。

如需详细了解如何授予角色，请参阅[管理访问权限](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-cn)。

您也可以通过[自定义角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-cn)或其他[预定义角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-cn#predefined)来获取所需的权限。

### 启用 API

如需使用搜索功能，请确保已启用 Dataplex API。对于所有使用 BigQuery 的新 Google Cloud 项目，Dataplex API 均[默认处于启用状态](https://docs.cloud.google.com/bigquery/docs/service-dependencies?hl=zh-cn)。如果您的项目中未启用 Dataplex API，请参阅[启用 Dataplex Universal Catalog](https://docs.cloud.google.com/dataplex/docs/enable-api?hl=zh-cn)。

## 搜索资源

1. 在 Google Cloud 控制台中，前往 BigQuery **搜索**页面。

   [转到搜索](https://console.cloud.google.com/bigquery/search?hl=zh-cn)
2. 在搜索字段中，用自然语言输入查询内容，然后按 `Enter` 键。以下是一些示例查询：

   * `Show me the datasets that contain taxi information`
   * `Find data on vaccine distribution across different countries`
   * `Get tables with historical temperature data for major world cities`
   * `Search for hurricane tracking and storm activity datasets`
   * `Population data by country`
3. 如需过滤搜索结果，请点击**过滤条件**。您可以使用以下过滤条件：

   * **范围**：在整个组织（默认）、当前项目或仅在已加星标的资源中进行搜索。如需了解详情，请参阅本文档的[搜索范围](#search-scope)部分。
   * **系统**：资源所属的 Google Cloud 服务，例如 BigQuery。Dataplex Universal Catalog 系统包含[条目组](https://docs.cloud.google.com/dataplex/docs/ingest-custom-sources?hl=zh-cn#entry-groups)。
   * **项目**：要搜索的项目。
   * **类型**：资源类型，例如 BigQuery 连接、Cloud Storage 存储桶或数据库。根据资源类型的不同，您还可以按子类型（例如连接类型或 SQL 方言）进行过滤。
   * **选择位置**：要搜索的位置。
   * **选择数据集**：此选项会将搜索结果限制为属于所选 BigQuery 数据集的 BigQuery 资源。在**输入文本以进行过滤**字段中，输入数据集的名称。
   * **注解**：与您要搜索的资源相关联的 Dataplex Universal Catalog [方面类型](https://docs.cloud.google.com/dataplex/docs/enrich-entries-metadata?hl=zh-cn#aspect-types)。如需按方面值过滤，请点击**按注解值过滤**，然后选择相应值。

   如需移除过滤条件，请点击要移除的特定过滤条件旁边的 clear **清除**。或者，如需移除所有过滤条件，请点击**清除过滤条件**。

   如需详细了解过滤条件的评估方式，请参阅本文档的[过滤条件](#filters)部分。
4. 可选：如需查看有关资源的更多信息，请在搜索结果中点击资源名称。

   这会在分屏窗格中打开资源摘要。执行以下任意操作：

   * 如需在资源所属的服务中打开该资源，请点击相应资源的**在 PRODUCT\_NAME 中打开**。例如，如需在 BigQuery Studio 中打开 BigQuery 数据集，请点击**在 Studio 中打开**。可用的选项取决于资源。
   * 如需查看与资源关联的 Dataplex Universal Catalog 元数据，请点击相应资源的**在 Dataplex Catalog 中打开**。
   * 如果您有想要收藏的重要搜索结果，可以为其加星标。点击相应资源的 star\_border **加星标**。您可以在 BigQuery Studio 中查看已加星标的资源。
   * 如需关闭分屏窗格中的资源摘要，请点击 close **关闭**。

## 过滤条件

借助过滤条件，您可以缩小搜索结果的范围。

如果您在多个部分中提供过滤条件，系统会使用 `AND` 逻辑运算符评估这些过滤条件。搜索结果包含与所选每个部分中至少一个条件相匹配的资源。例如，如果您选择 BigQuery 系统和 `dataset` 资源类型，则搜索结果会包含 BigQuery 数据集，但不会包含 Vertex AI 数据集。

如果您在单个部分中选择多个过滤条件，系统会使用 `OR` 逻辑运算符来评估这些过滤条件。例如，如果您选择 `dataset` 资源类型和 `table` 资源类型，则搜索结果会同时包含数据集和表。

## 搜索范围

对于属于 Google Cloud 组织的项目，搜索范围将限定在该组织内。

搜索结果会考虑您对资源的权限。例如，如果您拥有某个资源的 BigQuery 元数据读取权限，则该资源会显示在您的搜索结果中。如果您有权访问某个 BigQuery 表，但无权访问该表所属的数据集，则该表仍会按预期方式显示在搜索结果中。

**注意：**如果更改会影响大量资源或主账号，则权限传播到搜索可能会延迟。

搜索结果仅包含与执行搜索的项目属于同一 VPC Service Controls 边界的资源。使用 Google Cloud 控制台时，这是在控制台中选择的项目。

## 后续步骤

* 了解如何[在 BigQuery Studio 中分析数据](https://docs.cloud.google.com/bigquery/docs/query-overview?hl=zh-cn#bigquery-studio)。
* 了解如何[在 Dataplex Universal Catalog 中使用关键字搜索](https://docs.cloud.google.com/dataplex/docs/search-assets?hl=zh-cn)。




发送反馈

如未另行说明，那么本页面中的内容已根据[知识共享署名 4.0 许可](https://creativecommons.org/licenses/by/4.0/)获得了许可，并且代码示例已根据 [Apache 2.0 许可](https://www.apache.org/licenses/LICENSE-2.0)获得了许可。有关详情，请参阅 [Google 开发者网站政策](https://developers.google.com/site-policies?hl=zh-cn)。Java 是 Oracle 和/或其关联公司的注册商标。

最后更新时间 (UTC)：2026-01-24。




需要向我们提供更多信息？

[[["易于理解","easyToUnderstand","thumb-up"],["解决了我的问题","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["很难理解","hardToUnderstand","thumb-down"],["信息或示例代码不正确","incorrectInformationOrSampleCode","thumb-down"],["没有我需要的信息/示例","missingTheInformationSamplesINeed","thumb-down"],["翻译问题","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["最后更新时间 (UTC)：2026-01-24。"],[],[]]