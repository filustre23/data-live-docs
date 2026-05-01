* [Home](https://docs.cloud.google.com/?hl=zh-cn)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-cn)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-cn)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-cn)
* [参考文档](https://docs.cloud.google.com/bigquery/quotas?hl=zh-cn)

发送反馈



使用集合让一切井井有条

根据您的偏好保存内容并对其进行分类。

# PARTITIONS 视图

**预览版**

此产品或功能 受[服务专用条款](https://docs.cloud.google.com/terms/service-terms?hl=zh-cn#1)的约束。
非正式版产品和功能“按原样”提供，可能只能获得有限的支持。
如需了解详情，请参阅[发布阶段说明](https://cloud.google.com/products/?hl=zh-cn#product-launch-stages)。

`INFORMATION_SCHEMA.PARTITIONS` 视图包含每个分区对应的一行。

最多可以在 1000 个表中查询 `INFORMATION_SCHEMA.PARTITIONS` 视图。如需在项目级获取有关分区的数据，您可以将查询拆分为多个查询，然后将结果联接起来。如果超出此限制，您可能会遇到如下所示的错误。如需缩小结果范围，您可以在 `WHERE` 语句中使用过滤条件，例如 `table_name = 'mytable'` 和 `total_logical_bytes IS NOT NULL`。

```
INFORMATION_SCHEMA.PARTITIONS query attempted to read too many tables. Please add more restrictive filters.
```

## 所需权限

如需查询 `INFORMATION_SCHEMA.PARTITIONS` 视图，您需要拥有以下 Identity and Access Management (IAM) 权限：

* `bigquery.tables.get`
* `bigquery.tables.list`

以下每个预定义的 IAM 角色均可提供上述权限：

* `roles/bigquery.admin`
* `roles/bigquery.dataEditor`
* `roles/bigquery.dataViewer`

如需详细了解 BigQuery 权限，请参阅[使用 IAM 进行访问权限控制](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-cn)。

## 架构

当您查询 `INFORMATION_SCHEMA.PARTITIONS` 视图时，每个分区一般都会有一行对应的查询结果。例外情况是，[`__UNPARTITIONED__` 分区](https://docs.cloud.google.com/bigquery/docs/querying-partitioned-tables?hl=zh-cn#query_data_in_the_streaming_buffer)中同时包含长期存储层数据和活跃存储层数据。在这种情况下，该视图会为 `__UNPARTITIONED__` 分区返回两行，每行对应一个存储层级。

`INFORMATION_SCHEMA.PARTITIONS` 视图具有如下架构：

| 列名 | 数据类型 | 值 |
| --- | --- | --- |
| `table_catalog` | `STRING` | 包含表的项目的 ID。 |
| `table_schema` | `STRING` | 包含表的数据集的名称，也称为 `datasetId`。 |
| `table_name` | `STRING` | 表的名称，也称为 `tableId`。 |
| `partition_id` | `STRING` | 单个分区的 ID。对于未分区的表，该值为 `NULL`。如果分区表包含在分区列中具有 `NULL` 值的行，则值为 `__NULL__`。 |
| `total_rows` | `INTEGER` | 分区中的总行数。 |
| `total_logical_bytes` | `INTEGER` | 分区中的逻辑字节总数。 |
| `total_billable_bytes` | `INTEGER` | 分区中的可计费字节总数。如果存储空间的结算基于物理（压缩）字节数，则此值将与 `TOTAL_LOGICAL_BYTES` 数值不匹配。 |
| `last_modified_time` | `TIMESTAMP` | 数据最近一次写入分区的时间。用于计算分区是否符合长期存储的条件。 90 天后，该分区会自动从活跃存储空间转换为长期存储空间。如需了解详情，请参阅 [BigQuery 存储价格](https://cloud.google.com/bigquery/pricing?hl=zh-cn#storage)。 在分区中插入、加载、流式传输或修改数据时，此字段会更新。涉及记录删除的修改可能不会反映出来。 |
| `storage_tier` | `STRING` | 分区的存储层级：   * `ACTIVE`：分区按[活跃存储空间](https://cloud.google.com/bigquery/pricing?hl=zh-cn#storage)计费 * `LONG_TERM`：分区按[长期存储空间](https://cloud.google.com/bigquery/pricing?hl=zh-cn#storage)计费 |

为了确保稳定性，我们建议您在信息架构查询中明确列出列，而不是使用通配符 (`SELECT *`)。明确列出列可防止底层架构发生更改时查询中断。

## 范围和语法

针对此视图的查询必须包括数据集限定符。对于包含数据集限定符的查询，您必须拥有数据集的权限。如需了解详情，请参阅[语法](https://docs.cloud.google.com/bigquery/docs/information-schema-intro?hl=zh-cn#syntax)。下表说明了此视图的区域和资源范围：

| 视图名称 | 资源范围 | 区域范围 |
| --- | --- | --- |
| `[PROJECT_ID.]DATASET_ID.INFORMATION_SCHEMA.PARTITIONS` | 数据集级 | 数据集位置 |

请替换以下内容：

* 可选：`PROJECT_ID`：您的 Google Cloud 项目的 ID。如果未指定，则使用默认项目。
* `DATASET_ID`：您的数据集的 ID。如需了解详情，请参阅[数据集限定符](https://docs.cloud.google.com/bigquery/docs/information-schema-intro?hl=zh-cn#dataset_qualifier)。

## 示例

**示例 1**

以下示例计算了名为 `mydataset` 的数据集中所有表的每个存储层使用的逻辑字节数：

```
SELECT
  storage_tier,
  SUM(total_logical_bytes) AS logical_bytes
FROM
  `mydataset.INFORMATION_SCHEMA.PARTITIONS`
GROUP BY
  storage_tier;
```

**注意：**`INFORMATION_SCHEMA` 视图名称区分大小写。

结果类似于以下内容：

```
+--------------+----------------+
| storage_tier | logical_bytes  |
+--------------+----------------+
| LONG_TERM    |  1311495144879 |
| ACTIVE       |    66757629240 |
+--------------+----------------+
```

**示例 2**

以下示例会创建一个列，该列会从 `partition_id` 字段中提取分区类型，并在表级别汇总公共 `bigquery-public-data.covid19_usafacts` 数据集的分区信息：

```
SELECT
  table_name,
  CASE
    WHEN regexp_contains(partition_id, '^[0-9]{4}$') THEN 'YEAR'
    WHEN regexp_contains(partition_id, '^[0-9]{6}$') THEN 'MONTH'
    WHEN regexp_contains(partition_id, '^[0-9]{8}$') THEN 'DAY'
    WHEN regexp_contains(partition_id, '^[0-9]{10}$') THEN 'HOUR'
    END AS partition_type,
  min(partition_id) AS earliest_partition,
  max(partition_id) AS latest_partition_id,
  COUNT(partition_id) AS partition_count,
  sum(total_logical_bytes) AS sum_total_logical_bytes,
  max(last_modified_time) AS max_last_updated_time
FROM `bigquery-public-data.covid19_usafacts.INFORMATION_SCHEMA.PARTITIONS`
GROUP BY 1, 2;
```

结果类似于以下内容：

```
+-----------------+----------------+--------------------+---------------------+-----------------+-------------------------+--------------------------------+
| table_name      | partition_type | earliest_partition | latest_partition_id | partition_count | sum_total_logical_bytes | max_last_updated_time          |
+--------------+-------------------+--------------------+---------------------+-----------------+-------------------------+--------------------------------+
| confirmed_cases | DAY            | 20221204           | 20221213            | 10              | 26847302                | 2022-12-13 00:09:25.604000 UTC |
| deaths          | DAY            | 20221204           | 20221213            | 10              | 26847302                | 2022-12-13 00:09:24.709000 UTC |
| summary         | DAY            | 20221204           | 20221213            | 10              | 241285338               | 2022-12-13 00:09:27.496000 UTC |
+-----------------+----------------+--------------------+---------------------+-----------------+-------------------------+--------------------------------+
```




发送反馈

如未另行说明，那么本页面中的内容已根据[知识共享署名 4.0 许可](https://creativecommons.org/licenses/by/4.0/)获得了许可，并且代码示例已根据 [Apache 2.0 许可](https://www.apache.org/licenses/LICENSE-2.0)获得了许可。有关详情，请参阅 [Google 开发者网站政策](https://developers.google.com/site-policies?hl=zh-cn)。Java 是 Oracle 和/或其关联公司的注册商标。

最后更新时间 (UTC)：2026-03-10。




需要向我们提供更多信息？

[[["易于理解","easyToUnderstand","thumb-up"],["解决了我的问题","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["很难理解","hardToUnderstand","thumb-down"],["信息或示例代码不正确","incorrectInformationOrSampleCode","thumb-down"],["没有我需要的信息/示例","missingTheInformationSamplesINeed","thumb-down"],["翻译问题","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["最后更新时间 (UTC)：2026-03-10。"],[],[]]