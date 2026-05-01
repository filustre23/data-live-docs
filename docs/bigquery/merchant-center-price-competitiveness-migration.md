* [Home](https://docs.cloud.google.com/?hl=zh-cn)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-cn)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-cn)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-cn)
* [参考文档](https://docs.cloud.google.com/bigquery/quotas?hl=zh-cn)

发送反馈



使用集合让一切井井有条

根据您的偏好保存内容并对其进行分类。

# 迁移价格竞争力报告

**预览版**

此产品 受[服务专用条款](https://docs.cloud.google.com/terms/service-terms?hl=zh-cn#1)的约束。 非正式版产品“按原样”提供，且可能仅提供有限支持。
如需了解详情，请参阅[发布阶段说明](https://cloud.google.com/products/?hl=zh-cn#product-launch-stages)。

**注意**：如需获得有关使用 BigQuery Data Transfer Service 执行 Google Merchant Center 转移作业方面的支持，或提供相关反馈，请联系 [gmc-transfer-preview@google.com](mailto:gmc-transfer-preview@google.com)。

本文档可帮助您从将于 2025 年 9 月 1 日弃用的[价格基准](https://docs.cloud.google.com/bigquery/docs/merchant-center-price-benchmarks-schema?hl=zh-cn)报告迁移到新的[价格竞争力](https://docs.cloud.google.com/bigquery/docs/merchant-center-price-competitiveness-schema?hl=zh-cn)报告。

新版价格竞争力报告提供以下信息：

* 与旧版报告保持同等水平，并提高了与其他类似的 Google 产品（例如 Content API for Shopping 的 [`PriceCompetitivenessProductView` 字段](https://developers.google.com/shopping-content/guides/reports/fields?hl=zh-cn#pricecompetitivenessproductview)）的一致性。
* 有关商家价格数据的[其他分析洞见](#compare_price_benchmarks_and_price_competitiveness_table_schemas)。

## 比较价格基准表架构和价格竞争力表架构

下表可帮助您确定 [`Products_PriceBenchmarks` 表](https://docs.cloud.google.com/bigquery/docs/merchant-center-price-benchmarks-schema?hl=zh-cn#schema)中在 [`PriceCompetitiveness_` 表](https://docs.cloud.google.com/bigquery/docs/merchant-center-price-competitiveness-schema?hl=zh-cn#schema)中有等效替代项的字段：

| 价格基准（旧版） | 价格竞争力（新版） |
| --- | --- |
| `product_id` | `id` |
| `merchant_id` | `merchant_id` |
| `aggregator_id` | `aggregator_id` |
| `country_of_sale` | `report_country_code` |
| `price_benchmark_value` | `benchmark_price.amount_micros` |
| `price_benchmark_currency` | `benchmark_price.currency_code` |
| `price_benchmark_timestamp` | `_PARTITIONDATE` 或 `_PARTITIONTIME` |

此外，`PriceCompetitiveness_` 表还包含有关商品目录的其他数据，例如商品名、品牌、商品类型和类别，以及商家商品目录中的商品价格。借助此数据，您可以有效地将基准价格与自己的价格进行比较和分析。

新版 [`PriceCompetitiveness_` 表](https://docs.cloud.google.com/bigquery/docs/merchant-center-price-competitiveness-schema?hl=zh-cn#schema)中提供了以下额外字段：

| 字段 | 说明 |
| --- | --- |
| `title` | 商品的名称。 |
| `brand` | 商品的品牌。 |
| `offer_id` | 商家提供的[商品 ID](https://support.google.com/merchants/answer/6324405?hl=zh-cn)。 |
| `price` | 商品的价格。 |
| `price.amount_micros` | 商品的价格，以微单位表示（1 表示为 1,000,000）。 |
| `price.currency_code` | 商品的价格采用的币种。 |
| `product_type_l1` | 商品的[商品类型属性](https://support.google.com/merchants/answer/6324406?hl=zh-cn)。 |
| `product_type_l2` | 商品的[商品类型属性](https://support.google.com/merchants/answer/6324406?hl=zh-cn)。 |
| `product_type_l3` | 商品的[商品类型属性](https://support.google.com/merchants/answer/6324406?hl=zh-cn)。 |
| `product_type_l4` | 商品的[商品类型属性](https://support.google.com/merchants/answer/6324406?hl=zh-cn)。 |
| `product_type_l5` | 商品的[商品类型属性](https://support.google.com/merchants/answer/6324406?hl=zh-cn)。 |
| `category_l1` | 商品的 [Google 商品类别](https://support.google.com/merchants/answer/6324436?hl=zh-cn)。 |
| `category_l2` | 商品的 [Google 商品类别](https://support.google.com/merchants/answer/6324436?hl=zh-cn)。 |
| `category_l3` | 商品的 [Google 商品类别](https://support.google.com/merchants/answer/6324436?hl=zh-cn)。 |
| `category_l4` | 商品的 [Google 商品类别](https://support.google.com/merchants/answer/6324436?hl=zh-cn)。 |
| `category_l5` | 商品的 [Google 商品类别](https://support.google.com/merchants/answer/6324436?hl=zh-cn)。 |

价格竞争力和价格基准不支持回填。当您请求转移数据时，它们始终会返回当前可用的数据。

## 示例查询

本部分重点介绍了用于检索价格竞争力数据的示例查询中的变化。

### 示例 1：检索每个国家/地区的商品价格基准

以下查询会返回每个国家/地区的商品价格基准列表。请注意，商品在不同国家/地区的基准可能会有所不同。

#### 使用 `Products_PriceBenchmarks` 表（旧版）

```
SELECT
  DATE(price_benchmark_timestamp) AS date,
  product_id,
  merchant_id,
  aggregator_id,
  country_of_sale,
  price_benchmark_value,
  price_benchmark_currency
FROM
  `DATASET.Products_PriceBenchmarks_MERCHANT_ID`
WHERE
  _PARTITIONDATE >= 'DATE';
```

#### 使用 `PriceCompetitiveness` 表格（新版）

```
SELECT
  _PARTITIONDATE AS date,
  id,
  merchant_id,
  aggregator_id,
  report_country_code,
  benchmark_price.amount_micros,
  benchmark_price.currency_code
FROM
  `DATASET.PriceCompetitiveness_MERCHANT_ID`
WHERE
  _PARTITIONDATE >= 'DATE';
```

### 示例 2：检索商品和关联的基准

以下查询会检索商品及其关联的基准。

#### 联接 `Products` 和 `PriceBenchmarks` 表（旧版）

```
WITH products AS (
  SELECT
    _PARTITIONDATE AS date,
    *
  FROM
    `DATASET.Products_MERCHANT_ID`
  WHERE
    _PARTITIONDATE >= 'DATE'
), benchmarks AS (
  SELECT
    _PARTITIONDATE AS date,
    *
  FROM
    `DATASET.Products_PriceBenchmarks_MERCHANT_ID`
  WHERE
    _PARTITIONDATE >= 'DATE'
)
SELECT
  products.date,
  products.product_id,
  products.merchant_id,
  products.aggregator_id,
  products.price,
  benchmarks.price_benchmark_value,
  benchmarks.price_benchmark_currency,
  benchmarks.country_of_sale
FROM
  products
INNER JOIN
  benchmarks
ON products.product_id = benchmarks.product_id
  AND products.merchant_id = benchmarks.merchant_id
  AND products.date = benchmarks.date;
```

#### 使用 `PriceCompetitiveness` 表格（新版）

```
SELECT
  _PARTITIONDATE AS date,
  id AS product_id,
  merchant_id,
  aggregator_id,
  price.amount_micros,
  price.currency_code,
  benchmark_price.amount_micros,
  benchmark_price.currency_code,
  report_country_code AS country_of_sale
FROM
  `DATASET.PriceCompetitiveness_MERCHANT_ID`
WHERE
  _PARTITIONDATE >= 'DATE';
```

在这些查询中，替换以下内容：

* `DATASET`：您的数据集的名称。
* `MERCHANT_ID`：商家账号 ID
* `DATE`：日期，格式为 `YYYY-MM-DD`

## 后续步骤

* 如需详细了解新的价格竞争力报告，请参阅 [Google Merchant Center 价格竞争力表](https://docs.cloud.google.com/bigquery/docs/merchant-center-price-competitiveness-schema?hl=zh-cn)。




发送反馈

如未另行说明，那么本页面中的内容已根据[知识共享署名 4.0 许可](https://creativecommons.org/licenses/by/4.0/)获得了许可，并且代码示例已根据 [Apache 2.0 许可](https://www.apache.org/licenses/LICENSE-2.0)获得了许可。有关详情，请参阅 [Google 开发者网站政策](https://developers.google.com/site-policies?hl=zh-cn)。Java 是 Oracle 和/或其关联公司的注册商标。

最后更新时间 (UTC)：2026-03-17。




需要向我们提供更多信息？

[[["易于理解","easyToUnderstand","thumb-up"],["解决了我的问题","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["很难理解","hardToUnderstand","thumb-down"],["信息或示例代码不正确","incorrectInformationOrSampleCode","thumb-down"],["没有我需要的信息/示例","missingTheInformationSamplesINeed","thumb-down"],["翻译问题","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["最后更新时间 (UTC)：2026-03-17。"],[],[]]