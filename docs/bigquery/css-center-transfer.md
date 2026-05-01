* [Home](https://docs.cloud.google.com/?hl=zh-cn)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-cn)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-cn)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-cn)
* [参考文档](https://docs.cloud.google.com/bigquery/quotas?hl=zh-cn)

发送反馈



使用集合让一切井井有条

根据您的偏好保存内容并对其进行分类。

# 将 CSS Center 数据加载到 BigQuery 中

**预览版**

此产品 受[服务专用条款](https://docs.cloud.google.com/terms/service-terms?hl=zh-cn#1)的约束。 非正式版产品“按原样”提供，且可能仅提供有限支持。
如需了解详情，请参阅[发布阶段说明](https://cloud.google.com/products/?hl=zh-cn#product-launch-stages)。

**注意**：如需获得有关使用 BigQuery Data Transfer Service 执行 Comparison Shopping Service (CSS) Center 转移作业的支持或提供相关反馈，请联系 [gmc-transfer-preview@google.com](mailto:gmc-transfer-preview@google.com)。

您可以使用适用于 CSS Center 的 BigQuery Data Transfer Service 连接器将数据从 CSS Center 加载到 BigQuery。借助 BigQuery Data Transfer Service，您可以安排周期性转移作业，以将 CSS Center 中的最新数据添加到 BigQuery 中。

## 支持的报告

适用于 CSS Center 的 BigQuery Data Transfer Service 支持来自关联 Merchant Center 账号的[商品和商品问题报告](https://docs.cloud.google.com/bigquery/docs/merchant-center-transfer?hl=zh-cn#products_and_product_issues)的以下数据。

### 商品和商品问题

此报告包含与您的 CSS Center 关联的商家上传到其 Merchant Center 账号的数据。此报告还包括 Google 检测到的商家商品的商品级别问题。如需了解如何将此数据加载到 BigQuery，请参阅 [CSS Center 商品表架构](https://docs.cloud.google.com/bigquery/docs/css-center-products-schema?hl=zh-cn)。

## 从 CSS Center 转移作业注入数据

当您将数据从 CSS Center 转移到 BigQuery 时，数据会加载到按日期分区的 BigQuery 表中。数据加载到的表分区对应于数据源中的日期。如果您在同一日期安排多次转移，BigQuery Data Transfer Service 会使用最新数据覆盖该特定日期对应的分区。同一天的多个转移作业或正在运行的回填不会导致重复数据，其他日期的分区不受影响。

## 限制

某些报告可能有自己的限制条件，例如对于历史数据回填支持不同的时间长度。商品和商品问题报告不支持回填。

BigQuery 中的商品和商品问题数据不代表与您 CSS Center 账号关联的 Merchant Center 账号的实时视图。BigQuery 中的商品和商品问题数据的延迟时间最长可达一小时。

为 CSS Center 账号导出的数据仅包含已同意与关联 CSS 共享其信息的商家的相关信息。如需了解详情，请参阅 [CSS 如何访问您的 Merchant Center 账号](https://support.google.com/merchants/answer/13438603?hl=zh-cn)。

### CSS Center 数据访问权限和授权

CSS Center 的用户只能根据 Merchant Center 账号向该用户提供的访问权限级别来访问 Merchant Center 账号中的信息。因此，CSS Center 转移作业仅包含 CSS Center 用户有权访问的商家数据。如需了解详情，请参阅 [CSS 如何访问您的 Merchant Center 账号](https://support.google.com/merchants/answer/13438603?hl=zh-cn)。

您可以通过[在 CSS Center 中将用户的访问权限配置为 CSS 管理员](https://support.google.com/css-center/answer/9773473?hl=zh-cn)，来配置 CSS 用户的访问权限。

## 查询数据

在数据转移到 BigQuery 后，系统会将其写入[注入时间分区表](https://docs.cloud.google.com/bigquery/docs/partitioned-tables?hl=zh-cn)。

查询 CSS Center 表时，必须在查询中使用 `_PARTITIONTIME` 或 `_PARTITIONDATE` 伪列。如需了解详情，请参阅[查询分区表](https://docs.cloud.google.com/bigquery/docs/querying-partitioned-tables?hl=zh-cn)。

`Products_` 表包含嵌套和重复的字段。如需了解如何处理嵌套数据和重复数据，请参阅[重复字段处理方面的差异](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/migrating-from-legacy-sql?hl=zh-cn#differences_in_repeated_field_handling)。

## CSS Center 示例查询

您可以使用以下 CSS Center 示例查询来分析转移的数据。您还可以在 [Looker 数据洞察](https://www.google.com/analytics/data-studio/?hl=zh-cn)等可视化工具中使用查询。

在以下每个查询中，将 dataset 替换为您的数据集名称。将 css\_id 替换为您的 CSS 网域 ID。

### 商品和商品问题示例查询

以下查询会分析商品和商品问题报告中的数据。

#### 商品和商品问题统计信息

以下示例 SQL 查询按天提供商品数、问题商品数和问题数。

```
SELECT
  _PARTITIONDATE AS date,
  COUNT(*) AS num_products,
  COUNTIF(ARRAY_LENGTH(item_issues) > 0) AS num_products_with_issues,
  SUM(ARRAY_LENGTH(item_issues)) AS num_issues
FROM
  dataset.Products_css_id
WHERE
  _PARTITIONDATE >= 'YYYY-MM-DD'
GROUP BY
  date
ORDER BY
  date DESC;
```

#### 未获批准的商品

以下示例 SQL 查询提供了未获批准进行展示的商品数量（按区域和报告上下文分隔）。未获批准的原因可能是报告上下文被[排除在外](https://support.google.com/merchants/answer/6324486?hl=zh-cn)或商品存在问题。

```
SELECT
  _PARTITIONDATE AS date,
  statuses.region as disapproved_region,
  reporting_context_status.reporting_context as reporting_context,
  COUNT(*) AS num_products
FROM
  dataset.Products_css_id,
  UNNEST(reporting_context_statuses) AS reporting_context_status,
  UNNEST(reporting_context_status.region_and_status) AS statuses
WHERE
  _PARTITIONDATE >= 'YYYY-MM-DD' AND statuses.status = 'DISAPPROVED'
GROUP BY
  date, disapproved_region, reporting_context
ORDER BY
  date DESC;
```

#### 存在未获批准问题的商品

以下示例 SQL 查询会检索存在未获批准问题的商品数量（按区域分隔）。

```
SELECT
  _PARTITIONDATE AS date,
  disapproved_region,
  COUNT(DISTINCT CONCAT(CAST(css_id AS STRING), ':', product_id))
      AS num_distinct_products
FROM
  dataset.Products_css_id,
  UNNEST(item_issues) AS issue,
  UNNEST(issue.severity.severity_per_reporting_context) as severity_per_rc,
  UNNEST(severity_per_rc.disapproved_regions) as disapproved_region
WHERE
  _PARTITIONDATE >= 'YYYY-MM-DD'
GROUP BY
  date, disapproved_region
ORDER BY
  date DESC;
```




发送反馈

如未另行说明，那么本页面中的内容已根据[知识共享署名 4.0 许可](https://creativecommons.org/licenses/by/4.0/)获得了许可，并且代码示例已根据 [Apache 2.0 许可](https://www.apache.org/licenses/LICENSE-2.0)获得了许可。有关详情，请参阅 [Google 开发者网站政策](https://developers.google.com/site-policies?hl=zh-cn)。Java 是 Oracle 和/或其关联公司的注册商标。

最后更新时间 (UTC)：2026-03-18。




需要向我们提供更多信息？

[[["易于理解","easyToUnderstand","thumb-up"],["解决了我的问题","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["很难理解","hardToUnderstand","thumb-down"],["信息或示例代码不正确","incorrectInformationOrSampleCode","thumb-down"],["没有我需要的信息/示例","missingTheInformationSamplesINeed","thumb-down"],["翻译问题","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["最后更新时间 (UTC)：2026-03-18。"],[],[]]