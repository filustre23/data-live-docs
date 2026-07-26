* [Home](https://docs.cloud.google.com/?hl=zh-cn)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-cn)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-cn)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-cn)
* [参考文档](https://docs.cloud.google.com/bigquery/quotas?hl=zh-cn)

发送反馈



使用集合让一切井井有条

根据您的偏好保存内容并对其进行分类。

# 迁移畅销商品报告

**预览版**

此产品 受[服务专用条款](https://docs.cloud.google.com/terms/service-terms?hl=zh-cn#1)的约束。 非正式版产品“按原样”提供，且可能仅提供有限支持。
如需了解详情，请参阅[发布阶段说明](https://cloud.google.com/products/?hl=zh-cn#product-launch-stages)。

**注意：**如需获得有关使用 BigQuery Data Transfer Service 执行 Google Merchant Center 转移作业方面的支持，或提供相关反馈，请联系 [gmc-transfer-preview@google.com](mailto:gmc-transfer-preview@google.com)。

本文档可帮助您从旧版畅销商品报告迁移到[新版](https://docs.cloud.google.com/bigquery/docs/merchant-center-best-sellers-schema?hl=zh-cn)。导出 [`BestSellers_TopBrands_`](https://docs.cloud.google.com/bigquery/docs/merchant-center-top-brands-schema?hl=zh-cn)、[`BestSellers_TopProducts_`](https://docs.cloud.google.com/bigquery/docs/merchant-center-top-products-schema?hl=zh-cn) 和 [`BestSellers_TopProducts_Inventory_`](https://docs.cloud.google.com/bigquery/docs/merchant-center-product-inventory-schema?hl=zh-cn) 表的旧版报告将于 2025 年 9 月 1 日弃用。

新版畅销商品报告提供以下功能：

* 与旧版报告保持一致，并改进了与其他类似 Google 产品（例如 Content API for Shopping 中的 [BestSellersBrandView](https://developers.google.com/shopping-content/guides/reports/fields?hl=zh-cn#bestsellersbrandview) 和 [BestSellerProductClusterView](https://developers.google.com/shopping-content/guides/reports/fields?hl=zh-cn#bestsellersproductclusterview) 字段）的一致性。
* [Google Merchant Center Analytics](https://support.google.com/merchants/answer/13299535?hl=zh-cn) 中有关热门商品的其他分析洞见。
* 延长了回填功能（从 14 天延长到 2 年）。

## 旧版报告和新版报告导出的表

下表比较了旧版报告和新版报告导出的表：

| 旧版报告 | 新报告 |
| --- | --- |
| `BestSellers_TopBrands` | `BestSellersBrandWeekly`和`BestSellersBrandMonthly`之间 |
| `BestSellers_TopProducts` | `BestSellersProductClusterWeekly`和`BestSellersProductClusterMonthly`之间 |
| `BestSellers_TopProducts_Inventory` | `BestSellersEntityProductMapping` |

旧版报告包含畅销商品数据在未指定的时段内的单一汇总。新版报告会提供此数据在请求时的最新每周和每月汇总。

### 比较 `BestSellers_TopBrands` 与 `BestSellersBrandWeekly` 和 `BestSellersBrandMonthly`

下表可帮助您确定 [`BestSellers_TopBrands` 表](https://docs.cloud.google.com/bigquery/docs/merchant-center-top-brands-schema?hl=zh-cn#schema)中在 [`BestSellersBrandWeekly`](https://docs.cloud.google.com/bigquery/docs/merchant-center-best-sellers-schema?hl=zh-cn#best-sellers-brand) 和 [`BestSellersBrandMonthly`](https://docs.cloud.google.com/bigquery/docs/merchant-center-best-sellers-schema?hl=zh-cn#best-sellers-brand) 表中有等效替代项的字段。旧版表中的某些字段没有替代项。

| `BestSellers_TopBrands`（旧版） | `BestSellersBrandWeekly` 和 `BestSellersBrandMonthly`（新版） |
| --- | --- |
| `rank_timestamp` | `_PARTITIONDATE`和`_PARTITIONTIME`之间 |
| `brand` | `brand` |
| `google_brand_id` |  |
| `ranking_category` | `category_id` |
| `ranking_category_path.locale` |  |
| `ranking_category_path.name` |  |
| `ranking_country` | `country_code` |
| `rank_id` |  |
| `rank` | `rank` |
| `previous_rank` | `previous_rank` |
| `relative_demand.bucket` | `relative_demand` |
| `relative_demand.min` |  |
| `relative_demand.max` |  |
| `previous_relative_demand.bucket` | `previous_relative_demand` |
| `previous_relative_demand.min` |  |
| `previous_relative_demand.max` |  |
|  | `relative_demand_change` |

### 比较 `BestSellers_TopProducts` 与 `BestSellersProductClusterWeekly` 和 `BestSellersProductClusterMonthly`

下表可帮助您确定 [`BestSellers_TopProducts` 表](https://docs.cloud.google.com/bigquery/docs/merchant-center-top-products-schema?hl=zh-cn#schema)中在 [`BestSellersProductClusterWeekly`](https://docs.cloud.google.com/bigquery/docs/merchant-center-best-sellers-schema?hl=zh-cn#best-sellers-product-cluster) 和 [`BestSellersProductClusterMonthly`](https://docs.cloud.google.com/bigquery/docs/merchant-center-best-sellers-schema?hl=zh-cn#best-sellers-product-cluster) 表中有等效替代项的字段。旧版表中的某些字段没有替代项。

| `BestSellers_TopProducts`（旧版） | `BestSellersProductClusterWeekly` 和 `BestSellersProductClusterMonthly`（新版） |
| --- | --- |
| `rank_timestamp` | `_PARTITIONDATE`和`_PARTITIONTIME`之间 |
| `rank_id` | `entity_id` |
| `rank` | `rank` |
| `previous_rank` | `previous_rank` |
| `ranking_country` | `country_code` |
| `ranking_category` | `report_category_id` |
| `ranking_category_path.locale` |  |
| `ranking_category_path.name` |  |
| `relative_demand.bucket` | `relative_demand` |
| `relative_demand.min` |  |
| `relative_demand.max` |  |
| `previous_relative_demand.bucket` | `previous_relative_demand` |
| `previous_relative_demand.min` |  |
| `previous_relative_demand.max` |  |
|  | `relative_demand_change` |
| `product_title.locale` |  |
| `product_title.name` | `title`（单个标题，而不是每个语言区域的数组） |
| `gtins` | `variant_gtins` |
| `google_brand_id` |  |
| `brand` | `brand` |
| `google_product_category` |  |
|  | `category_l1`、`category_l2`、`category_l3`、`category_l4`、`category_l5` |
| `google_product_category_path.locale` |  |
| `google_product_category_path.name` |  |
| `price_range.min` | `price_range.min_amount_micros` |
| `price_range.max` | `price_range.max_amount_micros` |
| `price_range.currency` | `price_range.currency_code` |
|  | `product_inventory_status` |
|  | `brand_inventory_status` |

### 畅销商品数据的商品目录映射

在旧版畅销商品报告中，畅销商品数据会使用 [`TopProducts` 表](https://docs.cloud.google.com/bigquery/docs/merchant-center-top-products-schema?hl=zh-cn#schema)中的 `rank_id` 列，映射到[新生成的表](https://docs.cloud.google.com/bigquery/docs/merchant-center-product-inventory-schema?hl=zh-cn#schema)中的商家商品目录数据。

在新版畅销商品报告中，`entity_id` 列会导出到 `BestSellersProductCluster` 表中，并映射到 [`BestSellersEntityProductMapping`](https://docs.cloud.google.com/bigquery/docs/merchant-center-best-sellers-schema?hl=zh-cn#best-sellers-mapping) 表中商家商品目录中的所有商品 ID。

| `BestSellers_TopProductsInventory`（旧版） | `BestSellersEntityProductMapping`（新版） |
| --- | --- |
| `rank_id`（在 `BestSellers_TopProducts` 中） | `entity_id`（在 `BestSellersProductClustersWeekly` 和 `BestSellersProductClustersMonthly` 表中） |
| `product_id` | `product_id` |
| `merchant_id` |  |
| `aggregator_id` |  |

## 示例查询

本部分重点介绍用于检索畅销商品数据的查询示例中的变化。

### 示例 1：检索给定类别和国家/地区的热门商品

以下查询会返回给定类别和国家/地区的热门商品。

#### 使用 `BestSellers_TopProducts` 表（旧版）

```
SELECT
  rank,
  previous_rank,
  relative_demand.bucket,
  (SELECT name FROM top_products.product_title WHERE locale = 'en-US') AS product_title,
  brand,
  price_range,
  google_product_category
FROM
  `DATASET.BestSellers_TopProducts_MERCHANT_ID` AS top_products
WHERE
  _PARTITIONDATE = 'DATE' AND
  ranking_category = 267 /*Smartphones*/ AND
  ranking_country = 'US'
ORDER BY
  rank;
```

#### 使用 `BestSellersProductClusterWeekly` 或 `BestSellersProductClusterMonthly` 表（新版）

```
SELECT
  rank,
  previous_rank,
  relative_demand,
  title AS product_title,
  brand,
  price_range,
  category_l1,
  category_l2
FROM
  `DATASET.BestSellersProductClusterWeekly_MERCHANT_ID` AS top_products
WHERE
  _PARTITIONDATE = 'DATE' AND
  report_category_id = 267 /*Smartphones*/ AND
  country_code = 'US'
ORDER BY
  rank;
```

### 示例 2：检索商品目录中的热门商品

以下查询会返回商品目录中的热门商品列表。

#### 使用 `BestSellers_TopProducts` 表（旧版）

```
WITH latest_top_products AS
(
  SELECT
    *
  FROM
    `DATASET.BestSellers_TopProducts_MERCHANT_ID`
  WHERE
    _PARTITIONDATE = 'DATE'
),
latest_top_products_inventory AS
(
  SELECT
    *
  FROM
    `DATASET.BestSellers_TopProducts_Inventory_MERCHANT_ID`
  WHERE
    _PARTITIONDATE = 'DATE'
)
SELECT
  top_products.rank,
  inventory.product_id,
  (SELECT ANY_VALUE(name) FROM top_products.product_title) AS product_title,
  top_products.brand,
  top_products.gtins
FROM
  latest_top_products AS top_products
INNER JOIN
  latest_top_products_inventory AS inventory
USING (rank_id);
```

#### 使用 `BestSellersProductClusterWeekly` 或 `BestSellersProductClusterMonthly` 表（新版）

```
WITH latest_top_products AS
(
  SELECT
    *
  FROM
    `DATASET.BestSellersProductClusterWeekly_MERCHANT_ID`
  WHERE
    _PARTITIONDATE = 'DATE'
),
latest_top_products_inventory AS
(
  SELECT
    *
  FROM
    `DATASET.BestSellersEntityProductMapping_MERCHANT_ID`
  WHERE
    _PARTITIONDATE = 'DATE'
)
SELECT
  top_products.rank,
  inventory.product_id,
  top_products.title AS product_title,
  top_products.brand,
  top_products.variant_gtins
FROM
  latest_top_products AS top_products
INNER JOIN
  latest_top_products_inventory AS inventory
USING (entity_id);
```

此外，如果您想了解商品目录中畅销商品或品牌的数量，可以使用 `product_inventory_status` 或 `brand_inventory_status` 列对 `BestSellerProductClusterWeekly` 或 `BestSellerProductClusterMonthly` 表运行查询。请参阅以下查询示例：

```
SELECT
  *
FROM
  `DATASET.BestSellersProductClusterMonthly_MERCHANT_ID`
WHERE
  _PARTITIONDATE = 'DATE' AND
  product_inventory_status != 'NOT_IN_INVENTORY'
ORDER BY
  rank;
```

### 示例 3：检索给定类别和国家/地区的热门品牌

以下查询会返回给定类别和国家/地区的热门品牌列表。

#### 使用 `BestSellers_TopBrands` 表（旧版）

```
SELECT
  rank,
  previous_rank,
  brand
FROM
  `DATASET.BestSellers_TopBrands_MERCHANT_ID`
WHERE
  _PARTITIONDATE = 'DATE' AND
  ranking_category = 267 /*Smartphones*/ AND
  ranking_country = 'US'
ORDER BY
  rank;
```

#### 使用 `BestSellersTopBrandsWeekly` 或 `BestSellersTopBrandsMonthly` 表（新版）

```
SELECT
  rank,
  previous_rank,
  brand
FROM
  `DATASET.BestSellersTopBrandsWeekly_MERCHANT_ID`
WHERE
  _PARTITIONDATE = 'DATE' AND
  report_category_id = 267 /*Smartphones*/ AND
  country_code = 'US'
ORDER BY
  rank;
```

### 示例 4：检索商品目录中热门品牌的商品

以下查询会返回商品目录中热门品牌的商品列表。

#### 使用 `BestSellers_TopBrands` 表（旧版）

```
WITH latest_top_brands AS
  (
    SELECT
      *
    FROM
      `DATASET.BestSellers_TopBrands_MERCHANT_ID`
    WHERE
      _PARTITIONDATE = 'DATE'
  ),
  latest_products AS
  (
    SELECT
      product.*,
      product_category_id
    FROM
      `DATASET.Products_MERCHANT_ID` AS product,
      UNNEST(product.google_product_category_ids) AS product_category_id,
      UNNEST(destinations) AS destination,
      UNNEST(destination.approved_countries) AS approved_country
    WHERE
      _PARTITIONDATE = 'DATE'
  )
SELECT
  top_brands.brand,
  (SELECT name FROM top_brands.ranking_category_path
  WHERE locale = 'en-US') AS ranking_category,
  top_brands.ranking_country,
  top_brands.rank,
  products.product_id,
  products.title
FROM
  latest_top_brands AS top_brands
INNER JOIN
  latest_products AS products
ON top_brands.google_brand_id = products.google_brand_id AND
   top_brands.ranking_category = product_category_id AND
   top_brands.ranking_country = products.approved_country;
```

#### 使用 `BestSellersTopBrandsWeekly` 或 `BestSellersTopBrandsMonthly` 表（新版）

```
WITH latest_top_brands AS
  (
    SELECT
      *
    FROM
      `DATASET.BestSellersBrandMonthly_MERCHANT_ID`
    WHERE
      _PARTITIONDATE = 'DATE'
  ),
  latest_products AS
  (
    SELECT
      product.*,
      product_category_id
    FROM
      `DATASET.Products_MERCHANT_ID` AS product,
      UNNEST(product.google_product_category_ids) AS product_category_id,
      UNNEST(destinations) AS destination,
      UNNEST(destination.approved_countries) AS approved_country
    WHERE
      _PARTITIONDATE = 'DATE'
  )
SELECT
  top_brands.brand,
  –- The full category name is not supported in the new BestSellersTopBrands tables.
  –- (SELECT name FROM top_brands.ranking_category_path
  –- WHERE locale = 'en-US') AS ranking_category,
  top_brands.category_id,
  top_brands.rank,
  products.product_id,
  products.title
FROM
  latest_top_brands AS top_brands
INNER JOIN
  latest_products AS products
ON top_brands.brand = products.brand AND
   top_brands.category_id = product_category_id AND
   top_brands.country_code = products.approved_country;
```

在这些查询中，替换以下内容：

* `DATASET`：您的数据集的名称。
* `MERCHANT_ID`：商家账号 ID
* `DATE`：日期，格式为 `YYYY-MM-DD`

## 后续步骤

* 如需详细了解新版畅销商品报告，请参阅 [Google Merchant Center 畅销商品表](https://docs.cloud.google.com/bigquery/docs/merchant-center-best-sellers-schema?hl=zh-cn)。




发送反馈

如未另行说明，那么本页面中的内容已根据[知识共享署名 4.0 许可](https://creativecommons.org/licenses/by/4.0/)获得了许可，并且代码示例已根据 [Apache 2.0 许可](https://www.apache.org/licenses/LICENSE-2.0)获得了许可。有关详情，请参阅 [Google 开发者网站政策](https://developers.google.com/site-policies?hl=zh-cn)。Java 是 Oracle 和/或其关联公司的注册商标。

最后更新时间 (UTC)：2026-03-17。




需要向我们提供更多信息？

[[["易于理解","easyToUnderstand","thumb-up"],["解决了我的问题","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["很难理解","hardToUnderstand","thumb-down"],["信息或示例代码不正确","incorrectInformationOrSampleCode","thumb-down"],["没有我需要的信息/示例","missingTheInformationSamplesINeed","thumb-down"],["翻译问题","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["最后更新时间 (UTC)：2026-03-17。"],[],[]]