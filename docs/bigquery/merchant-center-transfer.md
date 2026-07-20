* [Home](https://docs.cloud.google.com/?hl=zh-cn)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-cn)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-cn)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-cn)
* [参考文档](https://docs.cloud.google.com/bigquery/quotas?hl=zh-cn)

发送反馈



使用集合让一切井井有条

根据您的偏好保存内容并对其进行分类。

# 将 Google Merchant Center 数据加载到 BigQuery 中

**预览版**

此产品 受[服务专用条款](https://docs.cloud.google.com/terms/service-terms?hl=zh-cn#1)的约束。 非正式版产品“按原样”提供，且可能仅提供有限支持。
如需了解详情，请参阅[发布阶段说明](https://cloud.google.com/products/?hl=zh-cn#product-launch-stages)。

**注意：**如需获得有关使用 BigQuery Data Transfer Service 执行 Google Merchant Center 转移作业方面的支持，或提供相关反馈，请联系 [gmc-transfer-preview@google.com](mailto:gmc-transfer-preview@google.com)。

您可以使用 BigQuery Data Transfer Service for Google Merchant Center 连接器将数据从 Google Merchant Center 加载到 BigQuery。借助 BigQuery Data Transfer Service，您可以安排周期性转移作业，将最新数据从 Google Merchant Center 添加到 BigQuery。

## 支持的报告

适用于 Google Merchant Center 的 BigQuery Data Transfer Service 支持以下数据：

### 商品和商品问题

商品和商品问题报告包括通过 Feed 或使用 Content API for Shopping 向 Google Merchant Center 提供的商品数据。此报告还包括 Google 检测到的商品项级别问题。您可以在 [Google Merchant Center](https://merchants.google.com/?hl=zh-cn) 中或通过查询 [Content API for Shopping](https://developers.google.com/shopping-content/v2/reference/v2.1/?hl=zh-cn) 来查看商品和商品问题数据。如需了解如何将此数据加载到 BigQuery，请参阅 Google Merchant Center [商品表架构](https://docs.cloud.google.com/bigquery/docs/merchant-center-products-schema?hl=zh-cn)。

### 地区商品目录

地区商品目录报告包括有关商品的地区性库存状况和价格替换的更多商品数据。如需了解如何将此数据加载到 BigQuery 中，请参阅 Google Merchant Center [地区商品目录表架构](https://docs.cloud.google.com/bigquery/docs/merchant-center-regional-inventories-schema?hl=zh-cn)。

### 本地商品目录

本地商品目录包括有关商品的本地商品目录的更多商品数据。此报告包含有关本地价格、库存状况、数量、自提和店内商品位置的数据。如需了解如何将此数据加载到 BigQuery 中，请参阅 Google Merchant Center [本地商品目录表架构](https://docs.cloud.google.com/bigquery/docs/merchant-center-local-inventories-schema?hl=zh-cn)。

### 性能

效果报告可提供对广告和非付费商品详情中的效果数据的精细细分。如需了解如何将此数据加载到 BigQuery 中，请参阅 Google Merchant Center [效果表架构](https://docs.cloud.google.com/bigquery/docs/merchant-center-performance-schema?hl=zh-cn)。

### 畅销商品

畅销商品报告提供的数据与 Google Merchant Center 界面中的数据相同，并支持回填至多 2 年前的国家/地区或类别的数据。其中包括关于购物广告和非付费商品详情中最受欢迎的商品和品牌的数据，以及您的商品目录中是否有这些商品和品牌。此报告基于 Google Merchant Center 提供的[畅销商品报告](https://support.google.com/merchants/answer/9488679?hl=zh-cn)。如需了解如何将此数据加载到 BigQuery 中，请参阅 Google Merchant Center [畅销商品表架构](https://docs.cloud.google.com/bigquery/docs/merchant-center-best-sellers-schema?hl=zh-cn)。

### 价格竞争力

价格竞争力报告（以前称为价格基准报告）包括商品级别属性和价格基准数据，它基于通过 Google Merchant Center 提供的[价格竞争力报告](https://support.google.com/merchants/answer/9626903?hl=zh-cn)中的定义。如需了解如何将此数据加载到 BigQuery 中，请参阅 Google Merchant Center [价格竞争力表架构](https://docs.cloud.google.com/bigquery/docs/merchant-center-price-competitiveness-schema?hl=zh-cn)。

### 价格分析

使用价格分析报告查看商品的建议售价，以及更新商品价格后的效果预测。使用价格分析报告可以帮助您更有效地为商品定价。如需详细了解如何使用此报告中的数据，请参阅[使用价格分析报告改善商品定价](https://support.google.com/merchants/answer/11916926?hl=zh-cn)。如需了解如何将此数据加载到 BigQuery 中，请参阅 Google Merchant Center [价格分析表架构](https://docs.cloud.google.com/bigquery/docs/merchant-center-price-insights-schema?hl=zh-cn)。

### 产品定位

请在设置转移作业时启用产品定位报告，以便在将 Google 购物中的数据加载到 BigQuery 时公开广告定位信息。如需了解如何将数据加载到 BigQuery 中，请参阅 Google Merchant Center [产品定位表架构](https://docs.cloud.google.com/bigquery/docs/merchant-center-product-targeting-schema?hl=zh-cn)。

## 报告选项

适用于 Google Merchant Center 的 BigQuery Data Transfer Service 支持以下报告选项：

| 报告选项 | 支持 |
| --- | --- |
| 时间表 | 可配置为每天、每周、每月或自定义。默认情况下，创建转移作业时，此项设置为每天。转移作业之间的最短间隔为 6 小时。 |

## 数据注入

当您将数据从 Google Merchant Center 转移到 BigQuery 时，数据会加载到按日期分区的 BigQuery 表中。数据加载到的表分区对应于数据源中的日期。如果您在同一日期安排多次转移，BigQuery Data Transfer Service 会使用最新数据覆盖该特定日期对应的分区。同一天的多个转移作业或正在运行的回填不会导致重复数据，其他日期的分区不受影响。

## 多客户账号 (MCA) 支持

建议具有多个商家 ID 的现有客户配置父级[多客户账号 (MCA)](https://support.google.com/merchants/answer/188487?hl=zh-cn)。
通过配置 MCA，您可以创建单个转移作业来覆盖您所有的商家 ID。

与使用单个商家 ID 相比，使用 Google Merchant Center MCA 具有多项优势：

* 您无需再管理多个转移作业，即可为多个商家 ID 转移报告数据。
* 由于所有商家 ID 的数据都存储在同一个表中，编写涉及多个商家 ID 的查询变得容易得多。
* 使用 MCA 可以缓解潜在的 BigQuery 加载作业配额问题，因为您的所有商家 ID 数据都将加载到同一作业中。

使用 MCA 的一项可能的缺点是后续查询费用有可能较高。由于您的所有数据都存储在同一个表中，检索单个商家 ID 数据的查询仍然必须扫描整个表。

**注意**：BigQuery Data Transfer Service 会拉取所有列出的商家 ID 的报告。如果某特定日期 Google 购物中没有商品，则您可能无法查看 BigQuery 表中的商家 ID。

如果使用的是 MCA，则 MCA ID 将在 `aggregator_id` 下列出，各子账号将在 `merchant_id` 下列出。对于不使用 MCA 的账号，`aggregator_id` 将设置为 `null`。

## 限制

某些报告可能有自己的限制条件，例如对于历史数据回填支持不同的时间长度。以下部分介绍每个报告的限制。

**历史数据回填支持**

各个报告对历史数据回填的支持不一定相同。下面列出了各个报告对历史数据回填的支持级别。

* 商品和商品问题 - 14 天
* 本地商品目录 - 14 天
* 地区商品目录 - 14 天
* 表现 - 2 年
* 畅销商品 - 2 年
* 价格竞争力 - 不支持回填
* 价格分析 - 不支持回填

**自动回填转移作业运行**

效果报告中的“今天”数据可能会有延迟。因此，在请求导出数据时，数据可能会更新至过去 3 天，以便进行修正。

为了支持此功能，每当在任何报告上触发转移作业时，系统都会针对 `today - 1` 和 `today - 2` 创建两次转移作业运行。这些转移作业运行仅影响效果表；其他表不受影响。

自动回填功能无法停用。




发送反馈

如未另行说明，那么本页面中的内容已根据[知识共享署名 4.0 许可](https://creativecommons.org/licenses/by/4.0/)获得了许可，并且代码示例已根据 [Apache 2.0 许可](https://www.apache.org/licenses/LICENSE-2.0)获得了许可。有关详情，请参阅 [Google 开发者网站政策](https://developers.google.com/site-policies?hl=zh-cn)。Java 是 Oracle 和/或其关联公司的注册商标。

最后更新时间 (UTC)：2026-03-10。




需要向我们提供更多信息？

[[["易于理解","easyToUnderstand","thumb-up"],["解决了我的问题","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["很难理解","hardToUnderstand","thumb-down"],["信息或示例代码不正确","incorrectInformationOrSampleCode","thumb-down"],["没有我需要的信息/示例","missingTheInformationSamplesINeed","thumb-down"],["翻译问题","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["最后更新时间 (UTC)：2026-03-10。"],[],[]]