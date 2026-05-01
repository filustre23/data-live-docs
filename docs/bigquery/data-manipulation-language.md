* [Home](https://docs.cloud.google.com/?hl=zh-cn)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-cn)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-cn)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-cn)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-cn)

发送反馈



使用集合让一切井井有条

根据您的偏好保存内容并对其进行分类。

# 使用数据操纵语言 (DML) 转换数据

借助 BigQuery 数据操纵语言 (DML)，您可以在 BigQuery 表中更新、插入和删除数据。

执行 DML 语句的过程与执行 `SELECT` 语句的过程相同，但必须符合以下条件：

* 您必须使用 GoogleSQL。如需启用 GoogleSQL，请参阅[切换 SQL 方言](https://docs.cloud.google.com/bigquery/sql-reference/enabling-standard-sql?hl=zh-cn)。
* 您无法为查询指定目标表。

如需详细了解如何计算 DML 语句处理的字节数，请参阅[按需查询大小计算](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/dml-syntax?hl=zh-cn#on-demand-query-size-calculation)。

## 限制

* 每个 DML 语句都会启动一个隐式事务，这表示在每个 DML 语句成功结束时，系统会自动提交该语句所做的更改。
* 最近使用 `tabledata.insertall` 流式传输方法写入的行无法使用数据操纵语言 (DML) 修改，例如 `UPDATE`、`DELETE`、`MERGE` 或 `TRUNCATE` 语句。最近的写入是指最近 30 分钟内发生的写入。表中的所有其他行仍可以使用 `UPDATE`、`DELETE`、`MERGE` 或 `TRUNCATE` 语句进行修改。流式插入的数据最多可能需要 90 分钟才能用于复制操作。

  或者，可以使用 `UPDATE`、`DELETE` 或 `MERGE` 语句修改最近使用 Storage Write API 写入的行。如需了解详情，请参阅[对最近流式插入的数据使用数据操纵语言 (DML)](https://docs.cloud.google.com/bigquery/docs/write-api?hl=zh-cn#use_data_manipulation_language_dml_with_recently_streamed_data)。
* `MERGE` 语句不支持 `when_clause`、`search_condition`、`merge_update_clause` 或 `merge_insert_clause` 中的关联子查询。
* 包含 [DML 语句](https://docs.cloud.google.com/bigquery/docs/data-manipulation-language?hl=zh-cn)的查询不能将[通配符表](https://docs.cloud.google.com/bigquery/docs/querying-wildcard-tables?hl=zh-cn)用作查询的目标。例如，通配符表可用于 `UPDATE` 查询的 `FROM` 子句，但不能用作 `UPDATE` 操作的目标。

## DML 语句

以下部分介绍了不同类型的 DML 语句以及如何使用这些语句。

### `INSERT` 语句

使用 `INSERT` 语句可向现有表中添加新行。以下示例会将新行插入到明确指定了值的表 `dataset.Inventory` 中。

```
INSERT dataset.Inventory (product, quantity)
VALUES('whole milk', 10),
      ('almond milk', 20),
      ('coffee beans', 30),
      ('sugar', 0),
      ('matcha', 20),
      ('oat milk', 30),
      ('chai', 5)

/+-------------------+----------+
 |      product      | quantity |
 +-------------------+----------+
 | almond milk       |       20 |
 | chai              |        5 |
 | coffee beans      |       30 |
 | matcha            |       20 |
 | oat milk          |       30 |
 | sugar             |        0 |
 | whole milk        |       10 |
 +-------------------+----------+/
```

如需详细了解 INSERT 语句，请参阅 [`INSERT` 语句](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/dml-syntax?hl=zh-cn#insert_statement)。

### `DELETE` 语句

使用 `DELETE` 语句可删除表中的行。以下示例会删除表 `dataset.Inventory` 中 `quantity` 值为 `0` 的所有行。

```
DELETE dataset.Inventory
WHERE quantity = 0

/+-------------------+----------+
 |      product      | quantity |
 +-------------------+----------+
 | almond milk       |       20 |
 | chai              |        5 |
 | coffee beans      |       30 |
 | matcha            |       20 |
 | oat milk          |       30 |
 | whole milk        |       10 |
 +-------------------+----------+/
```

如需删除表中的所有行，请改用 `TRUNCATE TABLE` 语句。如需详细了解 `DELETE` 语句，请参阅 [`DELETE` 语句](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/dml-syntax?hl=zh-cn#delete_statement)。

### `TRUNCATE` 语句

使用 TRUNCATE 语句可从表中移除所有行，但会保持表元数据不变，包括表架构、说明和标签。以下示例会从名为 `dataset.Inventory` 的表中移除所有行。

```
TRUNCATE dataset.Inventory
```

如需删除表中的特定行，请改用 DELETE 语句。如需详细了解 TRUNCATE 语句，请参阅 [`TRUNCATE` 语句](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/dml-syntax?hl=zh-cn#truncate_table_statement)。

### `UPDATE` 语句

使用 `UPDATE` 语句更新表中的现有行。`UPDATE` 语句还必须包含 WHERE 关键字，以指定条件。以下示例会将包含字符串 `milk` 的产品的行的 `quantity` 值减去 10。

```
UPDATE dataset.Inventory
SET quantity = quantity - 10,
WHERE product LIKE '%milk%'

/+-------------------+----------+
 |      product      | quantity |
 +-------------------+----------+
 | almond milk       |       10 |
 | chai              |        5 |
 | coffee beans      |       30 |
 | matcha            |       20 |
 | oat milk          |       20 |
 | whole milk        |        0 |
 +-------------------+----------+/
```

`UPDATE` 语句还可以包含 `FROM` 子句，以包含联接的表。如需详细了解 `UPDATE` 语句，请参阅 [`UPDATE` 语句](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/dml-syntax?hl=zh-cn#update_statement)。

### `MERGE` 语句

MERGE 语句会将 `INSERT`、`UPDATE` 和 `DELETE` 操作合并为一个语句，并以原子方式执行这些操作，以将数据从一个表合并到另一个表。如需详细了解 MERGE 语句并查看相关示例，请参阅 [`MERGE` 语句](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/dml-syntax?hl=zh-cn#merge_statement)。

## 并发作业

BigQuery 管理用于添加、修改或删除表中各行的 DML 语句的并发。

**注意**：DML 语句受到速率限制，例如[表写入速率上限](https://docs.cloud.google.com/bigquery/quotas?hl=zh-cn#standard_tables)。如果您一次针对某个表提交大量作业，则可能会达到速率限制。这些速率不会限制可以运行的 DML 语句总数。如果您收到一条错误消息，指出您[超出了速率限制](https://docs.cloud.google.com/bigquery/docs/troubleshoot-quotas?hl=zh-cn#overview)，请使用两次重试之间的指数退避算法重试操作。

### INSERT DML 并发

在任意 24 小时内，前 1500 个 `INSERT` 语句在提交后便立即运行。达到此限制后，写入表的 `INSERT` 语句的并发限制为 10。其他 `INSERT` 语句会添加到 `PENDING` 队列中。在任何给定时间内，最多可在表中将 100 个 `INSERT` 语句排入队列。`INSERT` 语句完成后，下一个 `INSERT` 语句会从队列中移除并运行。

如果您必须更频繁地运行 DML `INSERT` 语句，请考虑使用 [Storage Write API](https://docs.cloud.google.com/bigquery/docs/write-api?hl=zh-cn) 将数据流式插入到表中。

### UPDATE、DELETE、MERGE DML 并发

`UPDATE`、`DELETE` 和 `MERGE` DML 语句称为*变更型 DML 语句*。如果您在某个表上提交了一个或多个变更型 DML 语句，而该表上有其他变更型 DML 作业仍在运行（或待处理），则 BigQuery 最多并发运行 2 个作业，之后最多可以将 20 个作业加入队列作为 `PENDING` 作业。当上一个运行的作业完成时，系统会将下一个待处理作业移出队列并运行。加入队列的变更型 DML 语句所共享的每个表的最大队列长度为 20。其他超出每个表的最大队列长度的语句会失败，并显示错误消息：`Resources
exceeded during query execution: Too many DML statements outstanding against
table PROJECT_ID:DATASET.TABLE, limit is 20.`

排队时间超过 7 小时的交互式优先级 DML 作业会失败，并显示以下错误消息：

`DML statement has been queued for too long`

### DML 语句冲突

在表上并发运行的 DML 语句会在语句尝试更改同一分区时导致 DML 语句冲突。只要不修改同一分区，语句就会成功。BigQuery 最多尝试重新运行失败的语句三次。

* 在表中插入行的 `INSERT` DML 语句不会与任何其他并发运行的 DML 语句发生冲突。
* 只要 `MERGE` DML 语句仅插入行并且不会删除或更新任何现有行，就不会与其他并发运行的 DML 语句发生冲突。这可能包括具有 `UPDATE` 或 `DELETE` 子句的 `MERGE` 语句，前提是查询运行时未调用这些子句。

## 细粒度 DML

**预览版**

此功能 受[服务专用条款](https://docs.cloud.google.com/terms/service-terms?hl=zh-cn#1)的约束。 您可按照[云端数据处理附录](https://docs.cloud.google.com/terms/data-processing-addendum?hl=zh-cn)的规定，针对 此功能 处理个人数据，但须遵守您据以访问 Google Cloud 的协议中所述的义务与限制。 非正式版功能“按原样”提供，且可能仅提供有限支持。
如需了解详情，请参阅[发布阶段说明](https://cloud.google.com/products/?hl=zh-cn#product-launch-stages)。

**注意：**如需针对此功能提供反馈或请求支持，请发送邮件至 [bq-fine-grained-dml-feedback@google.com](mailto:bq-fine-grained-dml-feedback@google.com)。

细粒度 DML 是一种旨在优化 `UPDATE`、`DELETE` 和 `MERGE` 语句（也称为*变更型* DML 语句）执行的性能增强功能。

### 性能考虑因素

如果不启用细粒度 DML，系统会在文件组级别执行 DML 修改，这可能会导致数据重写效率低下，尤其是在进行稀疏修改时。这会导致额外的槽消耗和更长的执行时间。

细粒度 DML 是一种性能增强功能，旨在通过引入一种更精细的方法来优化这些变更型 DML 语句，从而减少需要在文件组级别重写的数据量。这种方法可以显著减少变更 DML 作业所消耗的处理时间、I/O 时间和槽时间。

使用细粒度 DML 时，需要注意一些性能方面的问题：

* 细粒度 DML 操作采用混合方法处理删除的数据，将重写成本分摊到多次表变更中。每项 DML 操作可能会处理一部分删除的数据，然后将剩余的删除数据处理任务分流到后台垃圾回收进程。如需了解详情，请参阅[已删除的数据注意事项](#deleted_data_considerations)。
* 如果表经常执行变更 DML 操作，后续 `SELECT` 查询和 DML 作业的延迟时间可能会增加。如需评估启用此功能的影响，请对一系列真实的 DML 操作和后续读取操作的性能进行基准比较。
* 对于经常发生变动且超过 2 TB 的大型表，不建议使用细粒度 DML。这些表可能会因后续查询而承受额外的内存压力，从而导致读取延迟增加或查询错误。
* 启用细粒度 DML 不会减少变异 DML 语句本身扫描的字节数。

### 启用细粒度 DML

如需启用细粒度 DML，请在运行 `CREATE TABLE` 或 `ALTER TABLE` DDL 语句时将[`enable_fine_grained_mutations` 表选项](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-cn#table_option_list)设置为 `TRUE`。

如需使用细粒度 DML 创建新表，请使用 [`CREATE TABLE` 语句](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-cn#create_table_statement)：

```
CREATE TABLE mydataset.mytable (
  product STRING,
  inventory INT64)
OPTIONS(enable_fine_grained_mutations = TRUE);
```

如需使用细粒度 DML 更改现有表，请使用 [`ALTER TABLE` 语句](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-cn#alter_table_set_options_statement)：

```
ALTER TABLE mydataset.mytable
SET OPTIONS(enable_fine_grained_mutations = TRUE);
```

如需使用细粒度 DML 更改数据集中的所有现有表，请使用 [`ALTER TABLE` 语句](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-cn#alter_table_set_options_statement)：

```
FOR record IN
 (SELECT CONCAT(table_schema, '.', table_name) AS table_path
 FROM mydataset.INFORMATION_SCHEMA.TABLES)
DO
 EXECUTE IMMEDIATE
   "ALTER TABLE " || record.table_path || " SET OPTIONS(enable_fine_grained_mutations = TRUE)";
END FOR;
```

将 `enable_fine_grained_mutations` 选项设置为 `TRUE` 后，系统会在运行变更型 DML 语句时启用细粒度 DML 功能，并使用现有的 [DML 语句语法](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/dml-syntax?hl=zh-cn)。

如需确定表是否已启用细粒度 DML，请查询 [`INFORMATION_SCHEMA.TABLES` 视图](https://docs.cloud.google.com/bigquery/docs/information-schema-tables?hl=zh-cn)。以下示例用于检查数据集中的哪些表已启用此功能：

```
SELECT
  table_schema AS datasetId,
  table_name AS tableId,
  is_fine_grained_mutations_enabled
FROM
  DATASET_NAME.INFORMATION_SCHEMA.TABLES;
```

将 `DATASET_NAME` 替换为要检查其中是否有任何表启用了细粒度 DML 的数据集的名称。

### 停用细粒度 DML

如需从现有表中停用细粒度 DML，请使用 [`ALTER TABLE` 语句](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-cn#alter_table_set_options_statement)。

```
ALTER TABLE mydataset.mytable
SET OPTIONS(enable_fine_grained_mutations = FALSE);
```

停用细粒度 DML 后，可能需要一段时间才能完全处理所有已删除的数据，请参阅[已删除的数据注意事项](#deleted_data_considerations)。因此，在发生这种情况之前，[细粒度 DML 限制](#fine-grained-dml-limitations)可能会一直存在。

### 价格

为表启用细粒度 DML 可能会产生额外费用。这些费用包括：

* [BigQuery 存储费用](https://docs.cloud.google.com/bigquery/pricing?hl=zh-cn#storage)，用于存储与细粒度 DML 操作关联的额外变更元数据。实际存储费用取决于修改的数据量，但对于大多数情况而言，与表本身的大小相比，预计费用可以忽略不计。
* [BigQuery 计算费用](https://docs.cloud.google.com/bigquery/pricing?hl=zh-cn#analysis_pricing_models)，用于使用分流的[垃圾回收作业](#deleted_data_considerations)处理已删除的数据，以及后续`SELECT`查询处理尚未进行垃圾回收的其他删除元数据。

您可以使用 [BigQuery 预留](https://docs.cloud.google.com/bigquery/docs/reservations-intro?hl=zh-cn)来分配专用的 BigQuery 计算资源，以处理分流的已删除数据作业。借助预留，您可以设置这些操作的费用上限。此方法对于非常大、经常执行细粒度变更 DML 操作的表特别有用，并且通常建议使用此方法，因为其他方法在执行每个分流的删除数据处理作业时，由于要处理大量字节，按需费用较高。

细粒度 DML 的分流删除数据处理作业会被视为后台作业，并且需要使用 [`BACKGROUND` 预留分配类型](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-cn#assignments)，而不是 [`QUERY` 预留分配类型](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-cn#assignments)。如果项目执行细粒度 DML 操作但没有[`BACKGROUND` 分配](https://docs.cloud.google.com/bigquery/docs/reservations-assignments?hl=zh-cn)，则会使用[按需价格](https://docs.cloud.google.com/bigquery/pricing?hl=zh-cn#on_demand_pricing)来处理分流的已删除数据作业。

| 操作 | 按需价格 | 基于容量的价格 |
| --- | --- | --- |
| 变更 DML 语句 | 使用标准 [DML 大小调整](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/dml-syntax?hl=zh-cn#on-demand-query-size-calculation)来确定按需扫描的字节数计算结果。 启用细粒度 DML 不会减少 DML 语句本身扫描的字节数。 | 在语句运行时使用分配的 `QUERY` 类型槽。 |
| 已分流已删除的数据处理作业 | 使用标准 [DML 大小调整](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/dml-syntax?hl=zh-cn#on-demand-query-size-calculation)来确定在运行已删除数据处理作业时按需扫描的字节数计算。 | 在运行已删除的数据处理作业时，使用分配的 `BACKGROUND` 类型槽。 |

### 已删除的数据注意事项

如果项目执行细粒度 DML 操作并分配了 `BACKGROUND`，则会使用槽来处理删除的数据，并且受限于已配置的预留的资源可用性。如果已配置的预留中没有足够的可用资源，则处理删除数据的时间可能会超出预期。

如果项目使用[按需价格](https://docs.cloud.google.com/bigquery/pricing?hl=zh-cn#on_demand_pricing)，或在没有`BACKGROUND`分配的情况下执行细粒度 DML 操作，则会使用[按需价格](https://docs.cloud.google.com/bigquery/pricing?hl=zh-cn#on_demand_pricing)处理删除的数据，并且系统会使用内部 BigQuery 资源定期处理已删除的数据。

如需识别分流的细粒度 DML 删除数据处理作业，请查询 [`INFORMATION_SCHEMA.JOBS` 视图](https://docs.cloud.google.com/bigquery/docs/information-schema-jobs?hl=zh-cn)：

```
SELECT
  *
FROM
  region-us.INFORMATION_SCHEMA.JOBS
WHERE
  job_id LIKE "%fine_grained_mutation_garbage_collection%"
```

### 限制

启用了细粒度 DML 的表会受到下列限制的约束：

* 您无法使用 [`tabledata.list` 方法](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tabledata/list?hl=zh-cn)从启用了细粒度 DML 的表中读取内容。而是使用 `SELECT` 语句来查询表以读取表记录。
* 无法使用 BigQuery 控制台预览启用了细粒度 DML 的表。
* 执行 `UPDATE`、`DELETE` 或 `MERGE` 语句后，您无法[复制已启用细粒度 DML 的表](https://docs.cloud.google.com/bigquery/docs/managing-tables?hl=zh-cn#copy-table)。
* 执行 `UPDATE`、`DELETE` 或 `MERGE` 语句后，您无法为启用了细粒度 DML 的表创建[表快照](https://docs.cloud.google.com/bigquery/docs/table-snapshots-intro?hl=zh-cn)或[表克隆](https://docs.cloud.google.com/bigquery/docs/table-clones-intro?hl=zh-cn)。
* 您无法在[复制的数据集](https://docs.cloud.google.com/bigquery/docs/data-replication?hl=zh-cn)中的表上启用细粒度 DML，也无法复制包含已启用细粒度 DML 的表的数据集。
* 在[多语句事务](https://docs.cloud.google.com/bigquery/docs/transactions?hl=zh-cn)中执行的 DML 语句不会通过细粒度 DML 进行优化。
* 您无法在通过 [`CREATE TEMP TABLE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-cn#create_table_statement) 语句创建的临时表上启用细粒度 DML。

## 最佳做法

为获得最佳性能，Google 建议您使用以下模式：

* 避免提交大量个别行更新或插入操作。而是尽可能将 DML 操作组合在一起。如需了解详情，请参阅[更新或插入单行的 DML 语句](https://docs.cloud.google.com/bigquery/docs/best-practices-performance-patterns?hl=zh-cn#dml_statements_that_update_or_insert_single_rows)。
* 如果更新或删除操作通常发生在旧数据或者特定日期范围内，请考虑对您的表进行[分区](https://docs.cloud.google.com/bigquery/docs/partitioned-tables?hl=zh-cn)。通过分区可确保仅针对表中的特定分区进行更改。
* 如果每个分区中的数据量较小，并且每次更新都会修改大部分分区，请避免对分区表进行分区。
* 如果您经常更新对应的一列或多列位于较小范围值的行，请考虑使用[聚簇表](https://docs.cloud.google.com/bigquery/docs/clustered-tables?hl=zh-cn)。聚簇操作可确保仅对一组特定的块进行更改，从而减少需要读取和写入的数据量。以下是针对一系列列值进行过滤的 `UPDATE` 语句的示例：

  ```
  UPDATE mydataset.mytable
  SET string_col = 'some string'
  WHERE id BETWEEN 54 AND 75;
  ```

  以下是针对一小部分列值进行过滤的类似示例：

  ```
  UPDATE mydataset.mytable
  SET string_col = 'some string'
  WHERE id IN (54, 57, 60);
  ```

  在以下情况下，请考虑对 `id` 列进行聚簇。
* 如果您需要 OLTP 功能，请考虑使用 [Cloud SQL 联合查询](https://docs.cloud.google.com/bigquery/docs/cloud-sql-federated-queries?hl=zh-cn)，使 BigQuery 能够查询 Cloud SQL 中的数据。
* 如需解决并防止出现配额错误 `Too many DML statements outstanding against table,`，请按照 BigQuery 问题排查页面上[针对此错误的指南](https://docs.cloud.google.com/bigquery/docs/troubleshoot-quotas?hl=zh-cn#ts-too-many-dml-statements-against-table-quota)操作。

如需了解优化查询性能的最佳实践，请参阅[优化查询性能简介](https://docs.cloud.google.com/bigquery/docs/best-practices-performance-overview?hl=zh-cn)。

## 后续步骤

* 如需查看 DML 语法信息和示例，请参阅 [DML 语法](https://docs.cloud.google.com/bigquery/sql-reference/dml-syntax?hl=zh-cn)。
* 详细了解如何[使用 DML 更新分区表数据](https://docs.cloud.google.com/bigquery/docs/using-dml-with-partitioned-tables?hl=zh-cn)。
* 如需了解如何在计划查询中使用 DML 语句，请参阅[计划查询](https://docs.cloud.google.com/bigquery/docs/scheduling-queries?hl=zh-cn)。




发送反馈

如未另行说明，那么本页面中的内容已根据[知识共享署名 4.0 许可](https://creativecommons.org/licenses/by/4.0/)获得了许可，并且代码示例已根据 [Apache 2.0 许可](https://www.apache.org/licenses/LICENSE-2.0)获得了许可。有关详情，请参阅 [Google 开发者网站政策](https://developers.google.com/site-policies?hl=zh-cn)。Java 是 Oracle 和/或其关联公司的注册商标。

最后更新时间 (UTC)：2026-01-06。




需要向我们提供更多信息？

[[["易于理解","easyToUnderstand","thumb-up"],["解决了我的问题","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["很难理解","hardToUnderstand","thumb-down"],["信息或示例代码不正确","incorrectInformationOrSampleCode","thumb-down"],["没有我需要的信息/示例","missingTheInformationSamplesINeed","thumb-down"],["翻译问题","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["最后更新时间 (UTC)：2026-01-06。"],[],[]]