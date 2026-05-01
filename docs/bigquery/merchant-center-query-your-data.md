* [Home](https://docs.cloud.google.com/?hl=zh-cn)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-cn)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-cn)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-cn)
* [参考文档](https://docs.cloud.google.com/bigquery/quotas?hl=zh-cn)

发送反馈



使用集合让一切井井有条

根据您的偏好保存内容并对其进行分类。

# 查询 Google Merchant Center 转移作业数据

**预览版**

此产品 受[服务专用条款](https://docs.cloud.google.com/terms/service-terms?hl=zh-cn#1)的约束。 非正式版产品“按原样”提供，且可能仅提供有限支持。
如需了解详情，请参阅[发布阶段说明](https://cloud.google.com/products/?hl=zh-cn#product-launch-stages)。

当数据转移到 BigQuery 时，这些数据会写入注入时间分区表。如需了解详情，请参阅[分区表简介](https://docs.cloud.google.com/bigquery/docs/partitioned-tables?hl=zh-cn)。

查询 Google Merchant Center 表时，必须在查询中使用 `_PARTITIONTIME` 或 `_PARTITIONDATE` 伪列。
如需了解详情，请参阅[查询分区表](https://docs.cloud.google.com/bigquery/docs/querying-partitioned-tables?hl=zh-cn)。

`Products_` 表包含嵌套和重复的字段。如需了解如何处理嵌套和重复的数据，请参阅 GoogleSQL 文档中的[重复字段处理的差异](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/migrating-from-legacy-sql?hl=zh-cn#differences_in_repeated_field_handling)。

## Google Merchant Center 示例查询

您可以使用以下 Google Merchant Center 示例查询来分析转移的数据。您还可以在 [Looker 数据洞察](https://www.google.com/analytics/data-studio/?hl=zh-cn)等可视化工具中使用查询。

在以下每个查询中，将 dataset 替换为您的数据集名称。将 merchant\_id 替换为您的商家 ID。如果您使用的是 MCA，请将 merchant\_id 替换为您的 MCA ID。

### 产品和产品问题统计信息

以下示例 SQL 查询按天提供商品数、问题商品数和问题数。

```
SELECT
  _PARTITIONDATE AS date,
  COUNT(*) AS num_products,
  COUNTIF(ARRAY_LENGTH(issues) > 0) AS num_products_with_issues,
  SUM(ARRAY_LENGTH(issues)) AS num_issues
FROM
  dataset.Products_merchant_id
WHERE
  _PARTITIONDATE >= 'YYYY-MM-DD'
GROUP BY
  date
ORDER BY
  date DESC
```

### 未获批准在购物广告中展示的商品

以下示例 SQL 查询提供了未获批准在购物广告中展示的商品数量（按国家/地区分隔）。未获批准的原因可能是目标页面被[排除](https://support.google.com/merchants/answer/6324486?hl=zh-cn)或商品存在问题。

```
SELECT
  _PARTITIONDATE AS date,
  disapproved_country,
  COUNT(*) AS num_products
FROM
  dataset.Products_merchant_id,
  UNNEST(destinations) AS destination,
  UNNEST(disapproved_countries) AS disapproved_country
WHERE
  _PARTITIONDATE >= 'YYYY-MM-DD'
GROUP BY
  date, disapproved_country
ORDER BY
  date DESC
```

### 存在未获批准问题的商品

以下示例 SQL 查询会检索存在未获批准问题的商品数量（按国家/地区分隔）。

```
SELECT
  _PARTITIONDATE AS date,
  applicable_country,
  COUNT(DISTINCT CONCAT(CAST(merchant_id AS STRING), ':', product_id))
      AS num_distinct_products
FROM
  dataset.Products_merchant_id,
  UNNEST(issues) AS issue,
  UNNEST(issue.applicable_countries) as applicable_country
WHERE
  _PARTITIONDATE >= 'YYYY-MM-DD' AND
  issue.servability = 'disapproved'
GROUP BY
  date, applicable_country
ORDER BY
  date DESC
```

**注意**：此查询使用 `merchant_id` 和 `product_id` 构建唯一键。
仅当您拥有 MCA 账号时，才需要如此构建唯一键。使用 MCA 账号时，可能会有多个子账号发生 `product_id` 冲突。




发送反馈

如未另行说明，那么本页面中的内容已根据[知识共享署名 4.0 许可](https://creativecommons.org/licenses/by/4.0/)获得了许可，并且代码示例已根据 [Apache 2.0 许可](https://www.apache.org/licenses/LICENSE-2.0)获得了许可。有关详情，请参阅 [Google 开发者网站政策](https://developers.google.com/site-policies?hl=zh-cn)。Java 是 Oracle 和/或其关联公司的注册商标。

最后更新时间 (UTC)：2026-03-17。




需要向我们提供更多信息？

[[["易于理解","easyToUnderstand","thumb-up"],["解决了我的问题","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["很难理解","hardToUnderstand","thumb-down"],["信息或示例代码不正确","incorrectInformationOrSampleCode","thumb-down"],["没有我需要的信息/示例","missingTheInformationSamplesINeed","thumb-down"],["翻译问题","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["最后更新时间 (UTC)：2026-03-17。"],[],[]]