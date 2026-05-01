* [Home](https://docs.cloud.google.com/?hl=zh-cn)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-cn)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-cn)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-cn)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-cn)

发送反馈



使用集合让一切井井有条

根据您的偏好保存内容并对其进行分类。

# 表采样

**预览版**

此产品或功能 受[服务专用条款](https://docs.cloud.google.com/terms/service-terms?hl=zh-cn#1)的约束。
非正式版产品和功能“按原样”提供，可能只能获得有限的支持。
如需了解详情，请参阅[发布阶段说明](https://cloud.google.com/products/?hl=zh-cn#product-launch-stages)。

利用表采样，您可以查询大型 BigQuery 表中的数据子集。采样会返回各种记录，同时避免了与扫描和处理整个表相关的费用。

## 使用表采样

如需在查询中使用表采样，请添加 [`TABLESAMPLE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-cn#tablesample_operator) 子句。例如，以下查询选择表大约 10％ 的表数据：

```
SELECT * FROM dataset.my_table TABLESAMPLE SYSTEM (10 PERCENT)
```

与 `LIMIT` 子句不同，`TABLESAMPLE` 从表中随机返回数据子集。此外，BigQuery 不会缓存包含 `TABLESAMPLE` 子句的查询的结果，因此查询可能每次返回不同的结果。

您可将 `TABLESAMPLE` 子句与其他选择条件结合使用。以下示例演示了表的 50% 示例，然后应用 `WHERE` 子句：

```
SELECT *
FROM dataset.my_table TABLESAMPLE SYSTEM (50 PERCENT)
WHERE customer_id = 1
```

下一个示例将 `TABLESAMPLE` 子句与 `JOIN` 子句组合：

```
SELECT *
FROM dataset.table1 T1 TABLESAMPLE SYSTEM (10 PERCENT)
JOIN dataset.table2 T2 TABLESAMPLE SYSTEM (20 PERCENT) USING (customer_id)
```

对于较小的表，如果联接两个样本且所有采样行都不符合联接条件，则您可能会收到空结果。

您可以将百分比指定为[查询参数](https://docs.cloud.google.com/bigquery/docs/parameterized-queries?hl=zh-cn)。以下示例展示了如何使用 bq 命令行工具将百分比传递给查询：

```
bq query --use_legacy_sql=false --parameter=percent:INT64:29 \
    'SELECT * FROM `dataset.my_table` TABLESAMPLE SYSTEM (@percent PERCENT)`
```

BigQuery 表整理成数据块。`TABLESAMPLE` 子句的工作原理：从表中随机选择一定百分比的数据块，并读取所选块中的所有行。采样粒度受数据块数量的限制。

如果表或表分区的大小超过 1 GB，则 BigQuery 通常会将表或表分区拆分为多个块。较小的表可能包含单个数据块。在这种情况下，`TABLESAMPLE` 子句读取整个表。如果采样百分比大于零，且表不为空，则表采样始终会返回一些结果。

块的大小可能不同，因此采样行的确切比例可能有所不同。如果要对个别行而不是数据块进行采样，您可以改用 `WHERE rand() < K` 子句。但是，此方法要求 BigQuery 扫描整个表。为了节省费用但仍从行层级采样获益，您可以结合使用这两种方法。

以下示例从存储空间中读取大约 20% 的数据块，然后随机选择这些块中的 10% 的行：

```
SELECT * FROM dataset.my_table TABLESAMPLE SYSTEM (20 PERCENT)
WHERE rand() < 0.1
```

## 外部表

您可以将 `TABLESAMPLE` 子句与将数据存储在文件集中的外部表搭配使用。BigQuery 会对表引用的外部文件的子集进行采样。对于某些文件格式，BigQuery 可以将各个文件拆分为块以进行采样。一些外部数据（例如 Google 表格中的数据）只包含作为一个数据块采样的单个文件。

## 从写入优化的存储空间进行采样

如果您将表采样与[流式插入](https://docs.cloud.google.com/bigquery/docs/streaming-data-into-bigquery?hl=zh-cn)功能搭配使用，则 BigQuery 会对写入优化的存储空间中的数据进行采样。在某些情况下，写入优化的存储空间中的所有数据会表示为单个块。发生这种情况时，写入优化的存储空间中的所有数据要么都显示在结果中，要么全部都不显示。

## 分区表和聚簇表

分区和聚簇会生成块，其中特定块中的所有行具有相同的分区键或具有闭合值的聚簇属性。因此，与非分区表、非聚簇表的样本集相比，这些表的样本集更容易出现偏差。

## 限制

* 采样表只能在查询语句中出现一次。此限制包括视图定义中引用的表。
* 不支持从视图采样数据。
* 不支持对子查询或表值函数调用的结果进行采样。
* 不支持从数组扫描中采样，例如调用 `UNNEST` 运算符的结果。
* 不支持在 `IN` 子查询中进行采样。
* 不支持从应用了行级安全性的表进行采样。

## 表采样价格

如果使用[按需结算](https://cloud.google.com/bigquery/pricing?hl=zh-cn#on_demand_pricing)，则需要为读取的采样数据付费。BigQuery 不会缓存包含 `TABLESAMPLE` 子句的查询的结果，因此每次执行都会从存储空间中读取数据。




发送反馈

如未另行说明，那么本页面中的内容已根据[知识共享署名 4.0 许可](https://creativecommons.org/licenses/by/4.0/)获得了许可，并且代码示例已根据 [Apache 2.0 许可](https://www.apache.org/licenses/LICENSE-2.0)获得了许可。有关详情，请参阅 [Google 开发者网站政策](https://developers.google.com/site-policies?hl=zh-cn)。Java 是 Oracle 和/或其关联公司的注册商标。

最后更新时间 (UTC)：2026-03-18。




需要向我们提供更多信息？

[[["易于理解","easyToUnderstand","thumb-up"],["解决了我的问题","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["很难理解","hardToUnderstand","thumb-down"],["信息或示例代码不正确","incorrectInformationOrSampleCode","thumb-down"],["没有我需要的信息/示例","missingTheInformationSamplesINeed","thumb-down"],["翻译问题","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["最后更新时间 (UTC)：2026-03-18。"],[],[]]