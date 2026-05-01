* [Home](https://docs.cloud.google.com/?hl=zh-cn)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-cn)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-cn)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-cn)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-cn)

发送反馈



使用集合让一切井井有条

根据您的偏好保存内容并对其进行分类。

# 管理搜索索引

搜索索引是一种数据结构，旨在使用 [`SEARCH` 函数](https://docs.cloud.google.com/bigquery/docs/search?hl=zh-cn)实现非常高效的搜索。 搜索索引还可以优化某些使用[受支持的函数和运算符](https://docs.cloud.google.com/bigquery/docs/search?hl=zh-cn#operator_and_function_optimization)的查询。

就像您在书籍后面找到的索引一样，字符串数据列的搜索索引就像一个辅助表，其中一列包含唯一字词，另一列表示出现这些字词的数据所在的位置。

## 创建搜索索引

如需创建搜索索引，请使用 [`CREATE SEARCH INDEX`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-cn#create_search_index_statement) DDL 语句。如需指定要编入索引的原初数据类型，请参阅[创建搜索索引并指定列和数据类型](https://docs.cloud.google.com/bigquery/docs/search-index?hl=zh-cn#create_a_search_index_and_specify_the_columns_and_data_types)。如果您未指定任何数据类型，则 BigQuery 默认会将以下类型且包含 `STRING` 数据的列编入索引：

* `STRING`
* `ARRAY<STRING>`
* `STRUCT`，至少包含一个类型为 `STRING` 或 `ARRAY<STRING>` 的嵌套字段
* `JSON`

创建搜索索引时，您可以指定要使用的[文本分析器](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/text-analysis?hl=zh-cn)的类型。文本分析器可控制如何对数据进行词法单元化处理以供索引和搜索功能使用。默认值为 `LOG_ANALYZER`。此分析器非常适合机器生成的日志，并具有针对可观测性数据中常见令牌的特殊规则，例如 IP 地址或电子邮件地址。在预处理完您希望完全匹配的数据后，请使用 `NO_OP_ANALYZER`。
`PATTERN_ANALYZER` 使用正则表达式从文本中提取词元。

### 创建使用默认文本分析器的搜索索引

在以下示例中，搜索索引是在 `simple_table` 的 `a` 和 `c` 列上创建的，并默认使用 `LOG_ANALYZER` 文本分析器：

```
CREATE TABLE dataset.simple_table(a STRING, b INT64, c JSON);

CREATE SEARCH INDEX my_index
ON dataset.simple_table(a, c);
```

### 在所有列上创建使用 `NO_OP_ANALYZER` 分析器的搜索索引

如果在 `ALL COLUMNS` 上创建搜索索引，则表中的所有 `STRING` 或 `JSON` 数据都会编入索引。 如果表不包含此类数据（比方说，如果所有列包含整数），则索引创建操作将会失败。如果您指定要编入索引的 `STRUCT` 列，则所有嵌套的子字段都会编入索引。

在以下示例中，搜索索引是在 `a`、`c.e` 和 `c.f.g` 上创建的，并使用 `NO_OP_ANALYZER` 文本分析器：

```
CREATE TABLE dataset.my_table(
  a STRING,
  b INT64,
  c STRUCT <d INT64,
            e ARRAY<STRING>,
            f STRUCT<g STRING, h INT64>>) AS
SELECT 'hello' AS a, 10 AS b, (20, ['x', 'y'], ('z', 30)) AS c;

CREATE SEARCH INDEX my_index
ON dataset.my_table(ALL COLUMNS)
OPTIONS (analyzer = 'NO_OP_ANALYZER');
```

由于搜索索引是在 `ALL COLUMNS` 上创建的，因此如果添加到表中的任何列包含 `STRING` 数据，则会将这些列编入索引。

### 创建搜索索引并指定列和数据类型

创建搜索索引时，您可以指定要使用的数据类型。数据类型用于控制列类型以及要编入索引的 `JSON` 和 `STRUCT` 列的子字段。要编入索引的默认数据类型为 `STRING`。如需创建包含更多数据类型（例如数字类型）的搜索索引，请使用 `CREATE SEARCH INDEX` 语句并包含 [`data_types`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-cn#index_option_list) 选项。

在以下示例中，系统会在名为 `simple_table` 的表的 `a`、`b`、`c` 和 `d` 列上创建搜索索引。支持的数据类型包括 `STRING`、`INT64` 和 `TIMESTAMP`。

```
CREATE TABLE dataset.simple_table(a STRING, b INT64, c JSON, d TIMESTAMP);

CREATE SEARCH INDEX my_index
ON dataset.simple_table(a, b, c, d)
OPTIONS ( data_types = ['STRING', 'INT64', 'TIMESTAMP']);
```

### 在所有列上创建搜索索引并指定数据类型

如果您在 `ALL COLUMNS` 上创建搜索索引并指定 `data_types` 选项，则系统会将任何与指定数据类型之一匹配的列编入索引。对于 `JSON` 和 `STRUCT` 列，系统会将任何与指定数据类型之一匹配的嵌套子字段编入索引。

在以下示例中，系统会在 `ALL COLUMNS` 上创建搜索索引并指定数据类型。名为 `my_table` 的表的列 `a`、`b`、`c`、`d.e`、`d.f`、`d.g.h`、`d.g.i` 会编入索引：

```
CREATE TABLE dataset.my_table(
  a STRING,
  b INT64,
  c TIMESTAMP,
  d STRUCT <e INT64,
            f ARRAY<STRING>,
            g STRUCT<h STRING, i INT64>>)
AS (
  SELECT
    'hello' AS a,
    10 AS b,
    TIMESTAMP('2008-12-25 15:30:00 UTC') AS c,
    (20, ['x', 'y'], ('z', 30)) AS d;
)

CREATE SEARCH INDEX my_index
ON dataset.my_table(ALL COLUMNS)
OPTIONS ( data_types = ['STRING', 'INT64', 'TIMESTAMP']);
```

由于搜索索引是在 `ALL COLUMNS` 上创建的，因此如果添加到表中的任何列与任何指定的数据类型匹配，则系统会自动将这些列编入索引。

### 以列粒度编入索引

**预览版**

此产品或功能 受[服务专用条款](https://docs.cloud.google.com/terms/service-terms?hl=zh-cn#1)的约束。
非正式版产品和功能“按原样”提供，可能只能获得有限的支持。
如需了解详情，请参阅[发布阶段说明](https://cloud.google.com/products/?hl=zh-cn#product-launch-stages)。

**注意：**如需在预览版期间获得支持，请联系 [bq-search@googlegroups.com](mailto:bq-search@googlegroups.com)。

创建搜索索引时，您可以为已编入索引的列指定列粒度。借助列粒度，BigQuery 可以在搜索索引中存储额外的列信息，从而优化某些类型的搜索查询。如需为已编入索引的列设置列粒度，请在运行 [`CREATE SEARCH INDEX` 语句](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-cn#create_search_index_statement)时，在 `index_column_option_list` 中使用 `index_granularity` 选项。

在内部，BigQuery 表整理为文件的形式。创建索引时，BigQuery 会创建从令牌到包含这些令牌的文件的映射。当您运行搜索查询时，BigQuery 会扫描包含该令牌的所有文件。如果搜索令牌很少出现在您要搜索的列中，但在其他列中很常见，则这种方法可能效率不高。

例如，假设您有以下包含招聘信息的表：

```
CREATE TABLE my_dataset.job_postings (job_id INT64, company_name STRING, job_description STRING);
```

“技能”一词可能经常出现在 `job_description` 列中，但很少出现在 `company_name` 列中。假设您运行以下查询：

```
SELECT * FROM my_dataset.job_postings WHERE SEARCH(company_name, 'skills');
```

如果您在列 `company_name` 和 `job_description` 上创建了搜索索引，但未指定列粒度，则 BigQuery 会扫描“技能”一词出现在 `job_description` 或 `company_name` 列中的每个文件。
为了提高此查询的性能，您可以将 `company_name` 的列粒度设置为 `COLUMN`：

```
CREATE SEARCH INDEX my_index
ON my_dataset.job_postings (
  company_name OPTIONS(index_granularity = 'COLUMN'),
  job_description);
```

现在，当您运行查询时，BigQuery 只会扫描“技能”一词出现在 `company_name` 列中的文件。

如需查看有关已编入索引的表列上设置了哪些选项的信息，请查询 [`INFORMATION_SCHEMA.SEARCH_INDEX_COLUMN_OPTIONS` 视图](https://docs.cloud.google.com/bigquery/docs/information-schema-index-column-options?hl=zh-cn)。

您可以按列粒度编入索引的列数存在限制。如需了解详情，请参阅[配额和限制](https://docs.cloud.google.com/bigquery/quotas?hl=zh-cn#indexed_granular_columns)。

## 了解索引刷新

搜索索引由 BigQuery 完全管理，并在表发生变化时自动刷新。在以下情况下，可能会发生索引完全刷新：

* [分区到期时间](https://docs.cloud.google.com/bigquery/docs/managing-partitioned-tables?hl=zh-cn#update_the_partition_expiration)已更新。
* 由于[表架构更改](https://docs.cloud.google.com/bigquery/docs/managing-table-schemas?hl=zh-cn)，索引列会更新。
* 由于缺少用于增量刷新的 `BACKGROUND` 预留槽，索引已过时。为防止过时，您可以使用[自动扩缩](https://docs.cloud.google.com/bigquery/docs/slots-autoscaling-intro?hl=zh-cn)并监控工作负载，以确定最佳基准和预留大小上限。

如果每个行中已编入索引的列数据都进行了更新（例如在回填操作期间），则需要更新整个索引，这相当于完全刷新。我们建议您缓慢执行回填，例如按分区逐个执行，以最大限度地减少潜在的负面影响。

如果您对基表进行任何架构更改，导致无法对已明确编入索引的列编入索引，则该索引会被永久停用。

如果您删除表中仅编入索引的列或重命名表本身，则搜索索引会自动予以删除。

搜索索引专为大型表而设计。如果您在小于 10GB 的表上创建搜索索引，则系统不会填充该索引。同样，如果从编入索引的表中删除数据导致表大小低于 10GB，则系统会暂时停用索引。在这种情况下，搜索查询不使用索引，并且 [`IndexUnusedReason` 代码](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-cn#indexunusedreason)为 `BASE_TABLE_TOO_SMALL`。无论您是否将自己的预留用于索引管理作业，都会发生这种情况。当编入索引的表大小超过 10GB 时，系统会自动填充其索引。在填充并激活搜索索引之前，您不需要支付存储费用。使用 [`SEARCH` 函数](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/search_functions?hl=zh-cn)的查询始终会返回正确的结果，即使某些数据尚未编入索引也是如此。

## 获取有关搜索索引的信息

可以通过查询 `INFORMATION_SCHEMA` 来验证搜索索引是否存在以及是否就绪。有三个视图包含有关搜索索引的元数据。

* [`INFORMATION_SCHEMA.SEARCH_INDEXES` 视图](https://docs.cloud.google.com/bigquery/docs/information-schema-indexes?hl=zh-cn)包含在数据集上创建的每个搜索索引的相关信息。
* [`INFORMATION_SCHEMA.SEARCH_INDEX_COLUMNS` 视图](https://docs.cloud.google.com/bigquery/docs/information-schema-index-columns?hl=zh-cn)包含数据集的每个表中已编入索引的列的相关信息。
* [`INFORMATION_SCHEMA.SEARCH_INDEXES_BY_ORGANIZATION` 视图](https://docs.cloud.google.com/bigquery/docs/information-schema-indexes-by-organization?hl=zh-cn)包含与当前项目关联的整个组织的搜索索引的相关信息。

### `INFORMATION_SCHEMA.SEARCH_INDEXES` 视图示例

本部分包含 `INFORMATION_SCHEMA.SEARCH_INDEXES` 视图的示例查询。

以下示例展示了项目 `my_project` 的数据集 `my_dataset` 中表的所有活跃搜索索引。该示例包括索引名称、用于创建索引的 DDL 语句、索引覆盖率及其文本分析器。如果编入索引的基表小于 10GB，则系统不会填充其索引，在这种情况下，`coverage_percentage` 为 0。

```
SELECT table_name, index_name, ddl, coverage_percentage, analyzer
FROM my_project.my_dataset.INFORMATION_SCHEMA.SEARCH_INDEXES
WHERE index_status = 'ACTIVE';
```

结果应如下所示：

```
+-------------+-------------+--------------------------------------------------------------------------------------+---------------------+----------------+
| table_name  | index_name  | ddl                                                                                  | coverage_percentage | analyzer       |
+-------------+-------------+--------------------------------------------------------------------------------------+---------------------+----------------+
| small_table | names_index | CREATE SEARCH INDEX `names_index` ON `my_project.my_dataset.small_table`(names)      | 0                   | NO_OP_ANALYZER |
| large_table | logs_index  | CREATE SEARCH INDEX `logs_index` ON `my_project.my_dataset.large_table`(ALL COLUMNS) | 100                 | LOG_ANALYZER   |
+-------------+-------------+--------------------------------------------------------------------------------------+---------------------+----------------+
```

### `INFORMATION_SCHEMA.SEARCH_INDEX_COLUMNS` 视图示例

本部分包含 `INFORMATION_SCHEMA.SEARCH_INDEX_COLUMNS` 视图的示例查询。

以下示例针对 `my_table` 的所有列创建搜索索引。

```
CREATE TABLE dataset.my_table(
  a STRING,
  b INT64,
  c STRUCT <d INT64,
            e ARRAY<STRING>,
            f STRUCT<g STRING, h INT64>>) AS
SELECT 'hello' AS a, 10 AS b, (20, ['x', 'y'], ('z', 30)) AS c;

CREATE SEARCH INDEX my_index
ON dataset.my_table(ALL COLUMNS);
```

以下查询会提取将哪些字段编入索引的信息。`index_field_path` 指示将列的哪个字段编入索引。这与 `index_column_name` 不同，后者仅在 `STRUCT` 的情况下提供编入索引的字段的完整路径。在此示例中，`c` 列包含 `ARRAY<STRING>` 字段 `e` 和另一个名为 `f` 的 `STRUCT`（包含 `STRING` 字段 `g`），每个网址都编入索引。

```
SELECT table_name, index_name, index_column_name, index_field_path
FROM my_project.dataset.INFORMATION_SCHEMA.SEARCH_INDEX_COLUMNS
```

结果类似于以下内容：

```
+------------+------------+-------------------+------------------+
| table_name | index_name | index_column_name | index_field_path |
+------------+------------+-------------------+------------------+
| my_table   | my_index   | a                 | a                |
| my_table   | my_index   | c                 | c.e              |
| my_table   | my_index   | c                 | c.f.g            |
+------------+------------+-------------------+------------------+
```

以下查询将 `INFORMATION_SCHEMA.SEARCH_INDEX_COUMNS` 视图与 `INFORMATION_SCHEMA.SEARCH_INDEXES` 和 `INFORMATION_SCHEMA.COLUMNS` 视图联接，以包含每列的搜索索引状态和数据类型：

```
SELECT
  index_columns_view.index_catalog AS project_name,
  index_columns_view.index_SCHEMA AS dataset_name,
  indexes_view.TABLE_NAME AS table_name,
  indexes_view.INDEX_NAME AS index_name,
  indexes_view.INDEX_STATUS AS status,
  index_columns_view.INDEX_COLUMN_NAME AS column_name,
  index_columns_view.INDEX_FIELD_PATH AS field_path,
  columns_view.DATA_TYPE AS data_type
FROM
  mydataset.INFORMATION_SCHEMA.SEARCH_INDEXES indexes_view
INNER JOIN
  mydataset.INFORMATION_SCHEMA.SEARCH_INDEX_COLUMNS index_columns_view
  ON
    indexes_view.TABLE_NAME = index_columns_view.TABLE_NAME
    AND indexes_view.INDEX_NAME = index_columns_view.INDEX_NAME
LEFT OUTER JOIN
  mydataset.INFORMATION_SCHEMA.COLUMNS columns_view
  ON
    indexes_view.INDEX_CATALOG = columns_view.TABLE_CATALOG
    AND indexes_view.INDEX_SCHEMA = columns_view.TABLE_SCHEMA
    AND index_columns_view.TABLE_NAME = columns_view.TABLE_NAME
    AND index_columns_view.INDEX_COLUMN_NAME = columns_view.COLUMN_NAME
ORDER BY
  project_name,
  dataset_name,
  table_name,
  column_name;
```

结果类似于以下内容：

```
+------------+------------+----------+------------+--------+-------------+------------+---------------------------------------------------------------+
| project    | dataset    | table    | index_name | status | column_name | field_path | data_type                                                     |
+------------+------------+----------+------------+--------+-------------+------------+---------------------------------------------------------------+
| my_project | my_dataset | my_table | my_index   | ACTIVE | a           | a          | STRING                                                        |
| my_project | my_dataset | my_table | my_index   | ACTIVE | c           | c.e        | STRUCT<d INT64, e ARRAY<STRING>, f STRUCT<g STRING, h INT64>> |
| my_project | my_dataset | my_table | my_index   | ACTIVE | c           | c.f.g      | STRUCT<d INT64, e ARRAY<STRING>, f STRUCT<g STRING, h INT64>> |
+------------+------------+----------+------------+--------+-------------+------------+---------------------------------------------------------------+
```

### `INFORMATION_SCHEMA.SEARCH_INDEXES_BY_ORGANIZATION` 视图示例

本部分包含 `INFORMATION_SCHEMA.SEARCH_INDEXES_BY_ORGANIZATION` 视图的示例查询。

#### 确定给定区域的消耗量是否超出限制

以下示例说明如果整个组织内利用美国多区域内的共享槽的已编入索引的总基表大小超过 100 TB：

```
WITH
 indexed_base_table_size AS (
 SELECT
   SUM(base_table.total_logical_bytes) AS total_logical_bytes
 FROM
   `region-us`.INFORMATION_SCHEMA.SEARCH_INDEXES_BY_ORGANIZATION AS search_index
 JOIN
   `region-us`.INFORMATION_SCHEMA.TABLE_STORAGE_BY_ORGANIZATION AS base_table
 ON
   (search_index.table_name = base_table.table_name
     AND search_index.project_id = base_table.project_id
     AND search_index.index_schema = base_table.table_schema)
 WHERE
   TRUE
   -- Excludes search indexes that are permanently disabled.
   AND search_index.index_status != 'PERMANENTLY DISABLED'
   -- Excludes BASE_TABLE_TOO_SMALL search indexes whose base table size is
   -- less than 10 GB. These tables don't count toward the limit.
   AND search_index.index_status_details.throttle_status != 'BASE_TABLE_TOO_SMALL'
   -- Excludes search indexes whose project has BACKGROUND reservation purchased
   -- for search indexes.
   AND search_index.use_background_reservation = false
 -- Outputs the total indexed base table size if it exceeds 100 TB,
 -- otherwise, doesn't return any output.
)
SELECT * FROM indexed_base_table_size
WHERE total_logical_bytes >= 109951162777600 -- 100 TB
```

结果类似于以下内容：

```
+---------------------+
| total_logical_bytes |
+---------------------+
|     109951162777601 |
+---------------------+
```

#### 按区域中的项目查找编入索引的基表的总大小

以下示例显示了美国多区域中每个项目的细分信息，包括已编入索引的基表的总大小：

```
SELECT
 search_index.project_id,
 search_index.use_background_reservation,
 SUM(base_table.total_logical_bytes) AS total_logical_bytes
FROM
 `region-us`.INFORMATION_SCHEMA.SEARCH_INDEXES_BY_ORGANIZATION AS search_index
JOIN
 `region-us`.INFORMATION_SCHEMA.TABLE_STORAGE_BY_ORGANIZATION AS base_table
ON
 (search_index.table_name = base_table.table_name
   AND search_index.project_id = base_table.project_id
   AND search_index.index_schema = base_table.table_schema)
WHERE
 TRUE
  -- Excludes search indexes that are permanently disabled.
  AND search_index.index_status != 'PERMANENTLY DISABLED'
  -- Excludes BASE_TABLE_TOO_SMALL search indexes whose base table size is
  -- less than 10 GB. These tables don't count toward limit.
 AND search_index.index_status_details.throttle_status != 'BASE_TABLE_TOO_SMALL'
GROUP BY search_index.project_id, search_index.use_background_reservation
```

结果类似于以下内容：

```
+---------------------+----------------------------+---------------------+
|     project_id      | use_background_reservation | total_logical_bytes |
+---------------------+----------------------------+---------------------+
| projecta            |     true                   |     971329178274633 |
+---------------------+----------------------------+---------------------+
| projectb            |     false                  |     834638211024843 |
+---------------------+----------------------------+---------------------+
| projectc            |     false                  |     562910385625126 |
+---------------------+----------------------------+---------------------+
```

#### 查找节流的搜索索引

以下示例返回组织和区域内所有被节流的搜索索引：

```
SELECT project_id, index_schema, table_name, index_name
FROM
 `region-us`.INFORMATION_SCHEMA.SEARCH_INDEXES_BY_ORGANIZATION
WHERE
 -- Excludes search indexes that are permanently disabled.
 index_status != 'PERMANENTLY DISABLED'
 AND index_status_details.throttle_status IN ('ORGANIZATION_LIMIT_EXCEEDED', 'BASE_TABLE_TOO_LARGE')
```

结果类似于以下内容：

```
+--------------------+--------------------+---------------+----------------+
|     project_id     |    index_schema    |  table_name   |   index_name   |
+--------------------+--------------------+---------------+----------------+
|     projecta       |     dataset_us     |   table1      |    index1      |
|     projectb       |     dataset_us     |   table1      |    index1      |
+--------------------+--------------------+---------------+----------------+
```

## 索引管理选项

要创建索引并让 BigQuery 维护它们，您有两种选择：

* [使用默认共享槽池](#use_shared_slots)：当计划编入索引的数据低于每个组织的[限制](https://docs.cloud.google.com/bigquery/quotas?hl=zh-cn#index_limits)时，您可以使用免费共享槽池来管理索引。
* [使用您自己的预留](#use_your_own_reservation)：要在较大的生产工作负载上实现更可预测且一致的索引编制进度，您可以使用自己的预留来管理索引。

### 使用共享槽

如果您尚未将项目配置为使用[专用预留](#use_your_own_reservation)来执行索引操作，就会在免费的共享槽池中处理索引管理，但存在以下限制。

如果向表添加数据，从而导致编入索引的表的总大小超过组织的[限制](https://docs.cloud.google.com/bigquery/quotas?hl=zh-cn#index_limits)，则 BigQuery 会暂停该表的索引管理。发生这种情况时，[`INFORMATION_SCHEMA.SEARCH_INDEXES` 视图](https://docs.cloud.google.com/bigquery/docs/information-schema-indexes?hl=zh-cn)中的 `index_status` 字段会显示 `PENDING DISABLEMENT`，且该索引会排队等待删除。虽然索引正在等待停用，但它仍然在查询中使用，并且您需要为该索引支付存储费用。索引删除后，`index_status` 字段会将该索引显示为 `TEMPORARILY DISABLED`。在此状态下，查询不使用该索引，并且您不需要为该索引支付存储费用。在这种情况下，[`IndexUnusedReason` 代码](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-cn#indexunusedreason)为 `BASE_TABLE_TOO_LARGE`。

如果您从表中删除数据，并且编入索引的表的总大小低于每个组织的限制，则索引管理将恢复。`INFORMATION_SCHEMA.SEARCH_INDEXES` 视图中的 `index_status` 字段为 `ACTIVE`，查询可以使用该索引，并且您需要为该索引支付存储费用。

您可以使用 [`INFORMATION_SCHEMA.SEARCH_INDEXES_BY_ORGANIZATION` 视图](https://docs.cloud.google.com/bigquery/docs/information-schema-indexes-by-organization?hl=zh-cn)来了解给定区域内的当前使用量（按项目和表细分）是否接近每个组织的限制。

BigQuery 不保证共享池的可用容量或您看到的索引吞吐量。对于生产应用，您可能需要使用专用槽来执行索引处理功能。

### 使用您自己的预留

您可以选择指定使用自己的预留来将表编入索引，而不是使用默认的共享槽池。使用您自己的预留可确保索引管理作业（例如创建、刷新和后台优化）具有可预测且一致的性能。

* 在预留中运行索引作业时，没有表大小限制。
* 使用您自己的预留可以在管理索引时更加灵活。
  如果需要创建非常大的索引或对编入索引的表进行大量更新，您可以暂时为分配空间添加更多的槽。

如需将具有指定预留的项目中的表编入索引，请在表所在的区域中[创建预留](https://docs.cloud.google.com/bigquery/docs/reservations-tasks?hl=zh-cn)。然后，将项目分配到该预留，并将 `job_type` 设置为 `BACKGROUND`，以便在后台优化作业之间共享资源：

### SQL

使用 [`CREATE ASSIGNMENT` DDL 语句](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-cn#create_assignment_statement).

1. 在 Google Cloud 控制台中，前往 **BigQuery** 页面。

   [转到 BigQuery](https://console.cloud.google.com/bigquery?hl=zh-cn)
2. 在查询编辑器中，输入以下语句：

   ```
   CREATE ASSIGNMENT
     `ADMIN_PROJECT_ID.region-LOCATION.RESERVATION_NAME.ASSIGNMENT_ID`
   OPTIONS (
     assignee = 'projects/PROJECT_ID',
     job_type = 'BACKGROUND');
   ```

   请替换以下内容：

   * `ADMIN_PROJECT_ID`：拥有预留资源的[管理项目](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-cn#admin-project)的 ID
   * `LOCATION`：预留的[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-cn)
   * `RESERVATION_NAME`：预留的名称
   * `ASSIGNMENT_ID`：分配的 ID

     此 ID 对项目和位置来说必须是唯一的，以小写字母或数字开头和结尾，并且只能包含小写字母、数字和短划线。
   * `PROJECT_ID`：包含要编入索引的表的项目 ID。此项目已分配到预留。
3. 点击 play\_circle **运行**。

如需详细了解如何运行查询，请参阅[运行交互式查询](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-cn#queries)。

### bq

使用 `bq mk` 命令：

```
bq mk \
    --project_id=ADMIN_PROJECT_ID \
    --location=LOCATION \
    --reservation_assignment \
    --reservation_id=RESERVATION_NAME \
    --assignee_id=PROJECT_ID \
    --job_type=BACKGROUND \
    --assignee_type=PROJECT
```

替换以下内容：

* `ADMIN_PROJECT_ID`：拥有预留资源的[管理项目](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-cn#admin-project)的 ID
* `LOCATION`：预留的[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-cn)
* `RESERVATION_NAME`：预留的名称
* `PROJECT_ID`：要分配到此预留的项目的 ID

#### 查看索引作业

每次在单个表上创建或更新索引时，都会创建一个新的索引作业。如需查看作业的相关信息，请查询 [`INFORMATION_SCHEMA.JOBS*` 视图](https://docs.cloud.google.com/bigquery/docs/information-schema-jobs?hl=zh-cn)。通过在查询的 `WHERE` 子句中设置 `` job_type IS NULL AND SEARCH(job_id, '`search_index`') ``，即可对索引作业进行过滤。以下示例列出了项目 `my_project` 中最新的五个索引作业：

```
SELECT *
FROM
 region-us.INFORMATION_SCHEMA.JOBS
WHERE
  project_id  = 'my_project'
  AND job_type IS NULL
  AND SEARCH(job_id, '`search_index`')
ORDER BY
 creation_time DESC
LIMIT 5;
```

**注意：**您无法查看在默认共享槽池中运行的索引作业的相关信息。

#### 选择预留大小

要为预留选择适当的槽数，您应该考虑何时运行索引管理作业、它们使用的槽数以及您的使用量随时间变化的情况。在以下情况下，BigQuery 会触发索引管理作业：

* 您在表上创建索引。
* 编入索引的表中的数据被修改。
* 表的架构发生了变化，并且此变化影响将哪些列编入索引。
* 索引数据和元数据会定期优化或更新。

表的索引管理作业所需的槽数取决于以下因素：

* 表的大小
* 将数据注入到表中的速率
* 应用于表的 DML 语句的速率
* 构建和维护索引的可接受延迟时间
* 索引的复杂程度，通常由数据属性（例如重复字词数量）决定

##### 初始估算

以下估算可帮助您估计预留所需的槽数。由于索引工作负载的高度可变性，因此在开始将数据编入索引后，应该重新评估您的要求。

* 现有数据：对于 1000 个槽的预留，BigQuery 中的现有表可以每秒最多 4 GiB（平均约为每天 336 TiB）的速度编入索引。
* 新注入的数据：对于新注入的数据，索引通常占用更多资源，因为表及其索引需要经过多轮转换优化。平均而言，与将初次回填的相同数据编入索引相比，将新注入的数据编入索引编入索引将需要三倍的资源数量。
* 不经常修改的数据：对于连续执行的索引维护，进行少量数据修改或根本没有数据修改的已编入索引的表所需的资源大幅减少。对于将初次回填的相同数据编入索引，建议在开始时保持所需槽数的 1/5，且不得少于 250 个槽。
* 在编制索引的过程中，保留的槽数大致随着预留大小而线性扩缩。
  但是对于编制索引，我们不建议使用少于 250 个槽的预留，因为这可能会导致索引进度变慢。
* 这些估算值可能会随着特征、优化和实际用量的变化而变化。
* 如果贵组织的总表大小超出了地区的索引限制，则应为索引操作持续分配非零预留。否则，索引操作可能会回退到默认层级，从而导致意外删除所有索引。

##### 监控用量和进度

评估高效地运行索引管理作业所需的槽数的最佳方法是监控槽利用率并相应地调整预留大小。以下查询生成索引管理作业的每日槽使用量。`us-west1` 地区仅包含过去 30 天的数据：

```
SELECT
  TIMESTAMP_TRUNC(job.creation_time, DAY) AS usage_date,
  -- Aggregate total_slots_ms used for index-management jobs in a day and divide
  -- by the number of milliseconds in a day. This value is most accurate for
  -- days with consistent slot usage.
  SAFE_DIVIDE(SUM(job.total_slot_ms), (1000 * 60 * 60 * 24)) AS average_daily_slot_usage
FROM
  `region-us-west1`.INFORMATION_SCHEMA.JOBS job
WHERE
  project_id = 'my_project'
  AND job_type IS NULL
  AND SEARCH(job_id, '`search_index`')
GROUP BY
  usage_date
ORDER BY
  usage_date DESC
limit 30;
```

如果没有足够的槽来运行索引管理作业，则索引可能会与其表不同步，并且索引作业可能会失败。在此情况下，BigQuery 从头开始重新构建索引。为避免产生不同步索引，请确保您有足够的槽来支持数据注入和优化中的索引更新。如需详细了解如何监控槽使用量，请参阅[管理员资源图表](https://docs.cloud.google.com/bigquery/docs/admin-resource-charts?hl=zh-cn)。

## 最佳做法

* 搜索索引专为大型表而设计。搜索索引的性能随表的大小而提升。
* 不要将仅包含极少量唯一值的列编入索引。
* 请勿将您从未打算与 `SEARCH` 函数或任何其他[受支持的函数和运算符](https://docs.cloud.google.com/bigquery/docs/search?hl=zh-cn#operator_and_function_optimization)搭配使用的列编入索引。
* 在 `ALL COLUMNS` 上创建搜索索引时要小心。每次添加包含 `STRING` 或 `JSON` 数据的列时，该列都会编入索引。
* 您应该在生产应用中[使用您自己的预留](#use_your_own_reservation)进行索引管理。如果您选择为索引管理作业使用默认共享槽池，则需要遵守每个组织的容量[限制](https://docs.cloud.google.com/bigquery/quotas?hl=zh-cn#index_limits)。

## 删除搜索索引

如果不再需要搜索索引，或者想要更改某个表中要编入索引的列，可以删除该表的当前索引。使用 [`DROP SEARCH INDEX` DDL 语句](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-cn#drop_search_index).

如果删除编入索引的表，其索引也会自动删除。

示例：

```
DROP SEARCH INDEX my_index ON dataset.simple_table;
```

## 后续步骤

* 如需简要了解搜索索引用例、价格、所需权限和限制，请参阅 [BigQuery 搜索简介](https://docs.cloud.google.com/bigquery/docs/search-intro?hl=zh-cn)。
* 如需了解如何高效搜索已编入索引的列，请参阅[使用索引进行搜索](https://docs.cloud.google.com/bigquery/docs/search?hl=zh-cn)。




发送反馈

如未另行说明，那么本页面中的内容已根据[知识共享署名 4.0 许可](https://creativecommons.org/licenses/by/4.0/)获得了许可，并且代码示例已根据 [Apache 2.0 许可](https://www.apache.org/licenses/LICENSE-2.0)获得了许可。有关详情，请参阅 [Google 开发者网站政策](https://developers.google.com/site-policies?hl=zh-cn)。Java 是 Oracle 和/或其关联公司的注册商标。

最后更新时间 (UTC)：2026-03-18。




需要向我们提供更多信息？

[[["易于理解","easyToUnderstand","thumb-up"],["解决了我的问题","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["很难理解","hardToUnderstand","thumb-down"],["信息或示例代码不正确","incorrectInformationOrSampleCode","thumb-down"],["没有我需要的信息/示例","missingTheInformationSamplesINeed","thumb-down"],["翻译问题","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["最后更新时间 (UTC)：2026-03-18。"],[],[]]