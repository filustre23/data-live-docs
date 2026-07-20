* [Home](https://docs.cloud.google.com/?hl=zh-cn)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-cn)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-cn)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-cn)
* [参考文档](https://docs.cloud.google.com/bigquery/quotas?hl=zh-cn)

发送反馈



使用集合让一切井井有条

根据您的偏好保存内容并对其进行分类。

# SEARCH\_INDEX\_COLUMN\_OPTIONS 视图

**预览版**

此产品或功能 受[服务专用条款](https://docs.cloud.google.com/terms/service-terms?hl=zh-cn#1)的约束。
非正式版产品和功能“按原样”提供，可能只能获得有限的支持。
如需了解详情，请参阅[发布阶段说明](https://cloud.google.com/products/?hl=zh-cn#product-launch-stages)。

`INFORMATION_SCHEMA.SEARCH_INDEX_COLUMN_OPTIONS` 视图中的每一行对应数据集中各表的搜索索引列中设置的每个选项。

## 所需权限

如需查看[搜索索引](https://docs.cloud.google.com/bigquery/docs/search-index?hl=zh-cn)元数据，您需要对具有相应索引的表拥有 `bigquery.tables.get` 或 `bigquery.tables.list` Identity and Access Management (IAM) 权限。以下每个预定义的 IAM 角色都至少包含以下权限之一：

* `roles/bigquery.admin`
* `roles/bigquery.dataEditor`
* `roles/bigquery.dataOwner`
* `roles/bigquery.dataViewer`
* `roles/bigquery.metadataViewer`
* `roles/bigquery.user`

如需详细了解 BigQuery 权限，请参阅[使用 IAM 进行访问权限控制](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-cn)。

## 架构

当您查询 `INFORMATION_SCHEMA.SEARCH_INDEX_COLUMN_OPTIONS` 视图时，数据集中各表的搜索索引列上设置的每个选项都会有一行对应的查询结果。

`INFORMATION_SCHEMA.SEARCH_INDEX_COLUMN_OPTIONS` 视图具有如下架构：

| 列名 | 数据类型 | 值 |
| --- | --- | --- |
| `index_catalog` | `STRING` | 包含数据集的项目的名称。 |
| `index_schema` | `STRING` | 包含索引的数据集的名称。 |
| `table_name` | `STRING` | 在其中创建索引的基表的名称。 |
| `index_name` | `STRING` | 索引的名称。 |
| `index_column_name` | `STRING` | 设置了相应选项的已编入索引的列的名称。 |
| `option_name` | `STRING` | 列上指定的选项的名称。 |
| `option_type` | `STRING` | 相应选项的类型。 |
| `option_value` | `STRING` | 选项的值。 |

为了确保稳定性，我们建议您在信息架构查询中明确列出列，而不是使用通配符 (`SELECT *`)。明确列出列可防止底层架构发生更改时查询中断。

## 范围和语法

针对此视图的查询必须具有[数据集限定符](https://docs.cloud.google.com/bigquery/docs/information-schema-intro?hl=zh-cn#syntax)。下表说明了此视图的区域范围：

| 视图名称 | 资源范围 | 区域范围 |
| --- | --- | --- |
| `[PROJECT_ID.]DATASET_ID.INFORMATION_SCHEMA.SEARCH_INDEX_COLUMN_OPTIONS` | 数据集级 | 数据集位置 |

请替换以下内容：

* 可选：`PROJECT_ID`：您的 Google Cloud 项目的 ID。如果未指定，则使用默认项目。
* `DATASET_ID`：您的数据集的 ID。如需了解详情，请参阅[数据集限定符](https://docs.cloud.google.com/bigquery/docs/information-schema-intro?hl=zh-cn#dataset_qualifier)。

**示例**

```
-- Returns metadata for search index column options in a single dataset.
SELECT * FROM myDataset.INFORMATION_SCHEMA.SEARCH_INDEX_COLUMN_OPTIONS;
```

## 示例

以下示例将默认索引列粒度设置为 `COLUMN`，并分别将 `col2` 和 `col3` 的粒度设置为 `GLOBAL` 和 `COLUMN`。在此示例中，列 `col2` 和 `col3` 会显示在结果中，因为其粒度是明确设置的。系统未显示列 `col1` 的粒度，因为该列使用的是默认粒度。

```
CREATE SEARCH INDEX index1 ON `mydataset.table1` (
  ALL COLUMNS WITH COLUMN OPTIONS (
    col2 OPTIONS(index_granularity = 'GLOBAL'),
    col3 OPTIONS(index_granularity = 'COLUMN')
  )
)
OPTIONS(
  default_index_column_granularity = 'COLUMN'
);

SELECT
  index_column_name, option_name, option_type, option_value
FROM
  mydataset.INFORMATION_SCHEMA.SEARCH_INDEX_COLUMN_OPTIONS
WHERE
  index_schema = 'mydataset' AND index_name = 'index1' AND table_name = 'table1';
```

结果类似于以下内容：

```
+-------------------+-------------------+---------------+--------------+
| index_column_name |  option_name      | option_type   | option_value |
+-------------------+-------------------+---------------+--------------+
| col2              | index_granularity | STRING        | GLOBAL       |
| col3              | index_granularity | STRING        | COLUMN       |
+-------------------+-------------------+---------------+--------------+
```

以下等效示例未使用 `ALL COLUMNS`，而是将默认索引列粒度设置为 `COLUMN`，并将两个列的粒度分别单独设置为 `GLOBAL` 和 `COLUMN`：

```
CREATE SEARCH INDEX index1 ON `mydataset.table1` (
  col1,
  col2 OPTIONS(index_granularity = 'GLOBAL'),
  col3 OPTIONS(index_granularity = 'COLUMN')
)
OPTIONS(
  default_index_column_granularity = 'COLUMN'
);

SELECT
  index_column_name, option_name, option_type, option_value
FROM
  mydataset.INFORMATION_SCHEMA.SEARCH_INDEX_COLUMN_OPTIONS
WHERE
  index_schema = 'mydataset' AND index_name = 'index1' AND table_name = 'table1';
```

结果类似于以下内容：

```
+-------------------+-------------------+---------------+--------------+
| index_column_name |  option_name      | option_type   | option_value |
+-------------------+-------------------+---------------+--------------+
| col2              | index_granularity | STRING        | GLOBAL       |
| col3              | index_granularity | STRING        | COLUMN       |
+-------------------+-------------------+---------------+--------------+
```




发送反馈

如未另行说明，那么本页面中的内容已根据[知识共享署名 4.0 许可](https://creativecommons.org/licenses/by/4.0/)获得了许可，并且代码示例已根据 [Apache 2.0 许可](https://www.apache.org/licenses/LICENSE-2.0)获得了许可。有关详情，请参阅 [Google 开发者网站政策](https://developers.google.com/site-policies?hl=zh-cn)。Java 是 Oracle 和/或其关联公司的注册商标。

最后更新时间 (UTC)：2026-03-18。




需要向我们提供更多信息？

[[["易于理解","easyToUnderstand","thumb-up"],["解决了我的问题","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["很难理解","hardToUnderstand","thumb-down"],["信息或示例代码不正确","incorrectInformationOrSampleCode","thumb-down"],["没有我需要的信息/示例","missingTheInformationSamplesINeed","thumb-down"],["翻译问题","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["最后更新时间 (UTC)：2026-03-18。"],[],[]]