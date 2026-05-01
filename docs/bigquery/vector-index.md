* [Home](https://docs.cloud.google.com/?hl=zh-cn)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-cn)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-cn)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-cn)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-cn)

发送反馈



使用集合让一切井井有条

根据您的偏好保存内容并对其进行分类。

# 管理向量索引

本文档介绍如何创建和管理向量索引，以加快向量搜索速度。

向量索引是一种数据结构，旨在使 [`VECTOR_SEARCH` 函数](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/search_functions?hl=zh-cn#vector_search)和 [`AI.SEARCH` 函数](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-ai-search?hl=zh-cn) 更高效地执行，尤其是在大型数据集上。
使用索引时，这些搜索函数会使用[近似最近邻 (ANN)](https://en.wikipedia.org/wiki/Nearest_neighbor_search#Approximation_methods) 算法来降低查询延迟和计算成本。虽然 ANN 引入了一定程度的近似，这意味着[召回率](https://developers.google.com/machine-learning/crash-course/classification/precision-and-recall?hl=zh-cn#recallsearch_term_rules)可能不为 100%，但性能提升通常会为大多数应用带来优势。

## 角色与权限

要创建向量索引，您需要对要在其中创建索引的表拥有 [`bigquery.tables.createIndex` IAM 权限](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-cn#bq-permissions)。要删除向量索引，您需要拥有 `bigquery.tables.deleteIndex` 权限。以下每个预定义的 IAM 角色都包含使用向量索引所需的权限：

* BigQuery Data Owner (`roles/bigquery.dataOwner`)
* BigQuery Data Editor (`roles/bigquery.dataEditor`)

## 选择向量索引类型

BigQuery 提供两种向量索引类型：[IVF](#ivf-index) 和 [TreeAH](#tree-ah-index)，每种类型都支持不同的用例。BigQuery 支持通过在 [`VECTOR_SEARCH`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/search_functions?hl=zh-cn#vector_search)中处理多行输入数据来对向量搜索进行批量处理。对于小批量查询，首选 IVF 索引。对于大批量查询，首选 TreeAH 索引，它使用 Google 的 [ScaNN 算法](https://github.com/google-research/google-research/blob/master/scann/docs/algorithms.md)构建。

### IVF 指数

IVF 是倒排文件索引，使用 k-means 算法对向量数据进行聚类，然后根据这些聚类对向量数据进行分区。`VECTOR_SEARCH`和`AI.SEARCH`函数可以使用这些分区来减少为确定结果而需要读取的数据量。

### TreeAH 索引

TreeAH 索引类型的命名源自其树状结构和对称哈希 (AH) 的使用，后者是底层 [ScaNN 算法](https://github.com/google-research/google-research/blob/master/scann/docs/algorithms.md)中的核心量化技术。TreeAH 索引的工作原理如下：

1. 基表被分成更小、更易于管理的分片。
2. 使用从 `CREATE VECTOR INDEX` 语句的 `tree_ah_options` 参数中的 `leaf_node_embedding_count` 选项得到的聚类数量来训练聚类模型。
3. 使用乘积量化来压缩向量，这种技术可减少内存用量。然后，将压缩后的向量，而不是原始向量，存储在索引表中，从而缩减向量索引大小。
4. 在 `VECTOR_SEARCH` 或 `AI.SEARCH` 函数运行时，使用非对称哈希高效地计算每个查询向量的候选列表。该非对称哈希针对近似距离计算进行了硬件优化。然后，使用精确嵌入对这些候选项重新评分和重新排名。

TreeAH 算法针对处理数百个或更多查询向量的批量查询进行了优化。与 IVF 相比，使用产品量化可以显著缩短延迟时间并减少费用，而且有望减少几个数量级。但是，由于开销增加，当您的查询向量较少时，IVF 算法可能更出色。

如果您的用例满足以下条件，我们建议您尝试使用 TreeAH 索引类型：

* 您的表包含的行数不超过 2 亿。
* 您经常执行涉及数百个或更多查询向量的大型批量查询。

对于使用 TreeAH 索引类型的小批量查询，`VECTOR_SEARCH` 或 `AI.SEARCH` 可能会回退为[暴力搜索](https://wikipedia.org/wiki/Brute-force_search)。发生这种情况时，系统会提供 [IndexUnusedReason](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-cn#IndexUnusedReason) 来解释未使用向量索引的原因。

## 创建 IVF 向量索引

如需创建 IVF 向量索引，请使用 [`CREATE VECTOR INDEX`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-cn#create_vector_index_statement) 数据定义语言 (DDL) 语句：

1. 转到 **BigQuery** 页面。

   [转到 BigQuery](https://console.cloud.google.com/bigquery?hl=zh-cn)
2. 在查询编辑器中，运行以下 SQL 语句：

   如需创建 [IVF](#ivf-index) 向量索引，请执行以下操作：

   ```
   CREATE [ OR REPLACE ] VECTOR INDEX [ IF NOT EXISTS ] INDEX_NAME
   ON DATASET_NAME.TABLE_NAME(COLUMN_NAME)
   STORING(STORED_COLUMN_NAME [, ...])
   OPTIONS(index_type = 'IVF',
     distance_type = 'DISTANCE_TYPE',
     ivf_options = '{"num_lists":NUM_LISTS}')
   ```

   替换以下内容：

   * `INDEX_NAME`：您要创建的向量索引的名称。由于索引始终在基表所在的项目和数据集中创建，因此无需在名称中指定这些内容。
   * `DATASET_NAME`：包含该表的数据集的名称。
   * `TABLE_NAME`：包含嵌入数据列的表的名称。
   * `COLUMN_NAME`：包含嵌入数据的列的名称。该列的类型必须是 `ARRAY<FLOAT64>`；如果您使用的是[自主嵌入生成](https://docs.cloud.google.com/bigquery/docs/autonomous-embedding-generation?hl=zh-cn)，则该列的类型必须是 `STRUCT<result ARRAY<FLOAT64>, status STRING>`。

     在所有情况下，嵌入数组中的所有元素都必须为非 `NULL`，且列中的所有值都必须具有相同的数组维度。

     如果列类型为 `STRUCT<result ARRAY<FLOAT64>, status STRING>`，则 `STRUCT` 值可以是 `NULL`，或者 `result` 数组可以是 `NULL`。系统会忽略这些值对应的任何 `NULL` 行。
   * `STORED_COLUMN_NAME`：表中要存储在向量索引中的顶级列的名称。列类型不能为 `RANGE`。如果表具有行级访问权限政策或是列具有政策标记，则不会使用存储列。如需了解如何启用存储列，请参阅[存储列和预先过滤](#stored-columns)。
   * `DISTANCE_TYPE`：指定使用此索引执行向量搜索时要使用的默认距离类型。支持的值为 [`EUCLIDEAN`](https://en.wikipedia.org/wiki/Euclidean_distance)、[`COSINE`](https://en.wikipedia.org/wiki/Cosine_similarity#Cosine_Distance) 和 [`DOT_PRODUCT`](https://en.wikipedia.org/wiki/Dot_product)。默认值为 `EUCLIDEAN`。

     索引创建本身始终使用 `EUCLIDEAN` 距离进行训练，但搜索函数中使用的距离可能不同。

     如果您为 `VECTOR_SEARCH` 或 `AI.SEARCH` 函数的 `distance_type` 参数指定值，则系统会使用该值（而非 `DISTANCE_TYPE` 值）。
   * `NUM_LISTS`：`INT64` 值，指定 IVF 索引将向量数据聚类，然后分区为多少个列表。此值必须小于等于 5,000。在编制索引期间，向量会分配到与其最近的聚类形心对应的列表。如果您省略此参数，BigQuery 会根据数据特征确定一个默认值。默认值适用于大多数用例。

     `NUM_LISTS` 控制查询调整的粒度。值越高，创建的列表就越多，因此您可以将搜索函数的 `fraction_lists_to_search` 选项设置为扫描较小百分比的索引。例如，扫描 100 个列表的 1%，而不是扫描 10 个列表的 10%。这样可以更精细地控制搜索速度和召回率，但会略微增加索引编制成本。请根据您需要的查询范围调整精确程度来设置此参数值。

以下示例在 `my_table` 的 `embedding` 列上创建向量索引：

```
CREATE TABLE my_dataset.my_table(embedding ARRAY<FLOAT64>);

CREATE VECTOR INDEX my_index ON my_dataset.my_table(embedding)
OPTIONS(index_type = 'IVF');
```

以下示例在 `my_table` 的 `embedding` 列上创建矢量索引，并指定要使用的距离类型和 IVF 选项：

```
CREATE TABLE my_dataset.my_table(embedding ARRAY<FLOAT64>);

CREATE VECTOR INDEX my_index ON my_dataset.my_table(embedding)
OPTIONS(index_type = 'IVF', distance_type = 'COSINE',
ivf_options = '{"num_lists": 2500}')
```

以下示例会创建一个启用了[自主生成嵌入内容](https://docs.cloud.google.com/bigquery/docs/autonomous-embedding-generation?hl=zh-cn)的表，并对该表创建向量索引。`description_embedding` 嵌入列是根据 `description` 列自动生成的。

```
CREATE TABLE mydataset.products (
  description STRING,
  description_embedding STRUCT<result ARRAY<FLOAT64>, status STRING>
    GENERATED ALWAYS AS (
      AI.EMBED(description, connection_id => 'us.example_connection',
        endpoint => 'text-embedding-005'))
    STORED OPTIONS( asynchronous = TRUE ));

CREATE VECTOR INDEX my_index ON my_dataset.my_table(description_embedding)
OPTIONS(index_type = 'IVF');
```

## 创建 TreeAH 向量索引

如需创建 TreeAH 向量索引，请使用 [`CREATE VECTOR INDEX`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-cn#create_vector_index_statement) 数据定义语言 (DDL) 语句：

1. 转到 **BigQuery** 页面。

   [转到 BigQuery](https://console.cloud.google.com/bigquery?hl=zh-cn)
2. 在查询编辑器中，运行以下 SQL 语句：

   ```
   CREATE [ OR REPLACE ] VECTOR INDEX [ IF NOT EXISTS ] INDEX_NAME
   ON DATASET_NAME.TABLE_NAME(COLUMN_NAME)
   STORING(STORED_COLUMN_NAME [, ...])
   OPTIONS(index_type = 'TREE_AH',
     distance_type = 'DISTANCE_TYPE',
     tree_ah_options = '{"leaf_node_embedding_count":LEAF_NODE_EMBEDDING_COUNT,
       "normalization_type":"NORMALIZATION_TYPE"}')
   ```

   替换以下内容：

   * `INDEX_NAME`：您要创建的向量索引的名称。由于索引始终在基表所在的项目和数据集中创建，因此无需在名称中指定这些内容。
   * `DATASET_NAME`：包含该表的数据集的名称。
   * `TABLE_NAME`：包含嵌入数据列的表的名称。
   * `COLUMN_NAME`：包含嵌入数据的列的名称。该列的类型必须是 `ARRAY<FLOAT64>`；如果您使用的是[自主嵌入生成](https://docs.cloud.google.com/bigquery/docs/autonomous-embedding-generation?hl=zh-cn)，则该列的类型必须是 `STRUCT<result ARRAY<FLOAT64>, status STRING>`。

     在所有情况下，嵌入数组中的所有元素都必须为非 `NULL`，且列中的所有值都必须具有相同的数组维度。

     如果列类型为 `STRUCT<result ARRAY<FLOAT64>, status STRING>`，则 `STRUCT` 值可以是 `NULL`，或者 `result` 数组可以是 `NULL`。系统会忽略这些值对应的任何 `NULL` 行。
   * `STORED_COLUMN_NAME`：表中要存储在向量索引中的顶级列的名称。列类型不能为 `RANGE`。如果表具有行级访问权限政策或是列具有政策标记，则不会使用存储列。如需了解如何启用存储列，请参阅[存储列和预先过滤](#stored-columns)。
   * `DISTANCE_TYPE`：可选参数，指定使用此索引执行向量搜索时要使用的默认距离类型。支持的值为 [`EUCLIDEAN`](https://en.wikipedia.org/wiki/Euclidean_distance)、[`COSINE`](https://en.wikipedia.org/wiki/Cosine_similarity#Cosine_Distance) 和 [`DOT_PRODUCT`](https://en.wikipedia.org/wiki/Dot_product)。默认值为 `EUCLIDEAN`。

     索引创建本身始终使用 `EUCLIDEAN` 距离进行训练，但搜索函数中使用的距离可能不同。

     如果您为 `VECTOR_SEARCH` 或 `AI.SEARCH` 函数的 `distance_type` 参数指定值，则系统会使用该值（而非 `DISTANCE_TYPE` 值）。
   * `LEAF_NODE_EMBEDDING_COUNT`：一个大于或等于 500 的 `INT64` 值，指定 TreeAH 算法创建的树的每个叶节点中向量的近似数量。TreeAH 算法将整个数据空间划分为若干个列表，每个列表包含大约 `LEAF_NODE_EMBEDDING_COUNT` 个数据点。若值越小，则创建的列表就越多，数据点数量越少；若值越大，则创建的列表就越少，数据点数量越多。默认值为 1,000，适合大多数数据集。
   * `NORMALIZATION_TYPE`：一个 `STRING` 值。支持的值为 `NONE` 或 [`L2`](https://en.wikipedia.org/wiki/Norm_(mathematics)#Euclidean_norm)。默认值为 `NONE`。 标准化会在对基表数据和查询数据执行任何处理之前进行，但不会修改 `TABLE_NAME` 中的嵌入列 `COLUMN_NAME`。根据数据集、嵌入模型以及搜索期间使用的距离类型，对嵌入进行标准化可能会提高召回率。

以下示例在 `my_table` 的 `embedding` 列上创建向量索引，并指定要使用的距离类型和 TreeAH 选项：

```
CREATE TABLE my_dataset.my_table(id INT64, embedding ARRAY<FLOAT64>);

CREATE VECTOR INDEX my_index ON my_dataset.my_table(embedding)
OPTIONS (index_type = 'TREE_AH', distance_type = 'EUCLIDEAN',
tree_ah_options = '{"normalization_type": "L2"}');
```

## 过滤

以下部分介绍了预过滤器和后过滤器如何影响向量搜索结果，以及如何使用向量索引中的存储列和分区进行预过滤。

### 预过滤器和后过滤器

在 BigQuery `VECTOR_SEARCH` 或 `AI.SEARCH` 调用中，预过滤和后过滤都基于与向量嵌入关联的元数据列来应用条件，从而优化搜索结果。了解它们之间的差异、实现和影响非常重要，以便优化查询性能、成本和准确率。

预过滤和后过滤的定义如下：

* **预过滤：**在近似最近邻 (ANN) 搜索对候选向量执行距离计算之前应用过滤条件。这可以缩小搜索期间考虑的向量池。因此，预过滤通常会缩短查询时间并降低计算成本，因为 ANN 搜索评估更少的潜在候选项。
* **后过滤：**在 ANN 搜索识别出初始的 `top_k` 个最近邻后应用过滤条件。这会根据指定的条件优化最终结果集。

`WHERE` 子句的位置决定了过滤器是充当前过滤器还是后过滤器。

如需创建预过滤器，查询的 `WHERE` 子句必须应用于搜索函数的基表参数。谓词必须应用于存储列，否则它实际上会成为后过滤器。

以下示例展示了如何创建预过滤器：

```
-- Pre-filter on a stored column. The index speeds up the query.
SELECT *
FROM
  VECTOR_SEARCH(
    (SELECT * FROM my_dataset.my_table WHERE type = 'animal'),
    'embedding',
    TABLE my_dataset.my_testdata);

SELECT *
FROM
  AI.SEARCH(
    (SELECT * FROM my_dataset.my_table WHERE type = 'animal'),
    'content',
    'dog');

-- Filter on a column that isn't stored. The index is used to search the
-- entire table, and then the results are post-filtered. You might see fewer
-- than 5 matches returned for some embeddings.
SELECT query.test_id, base.type, distance
FROM
  VECTOR_SEARCH(
    (SELECT * FROM my_dataset.my_table WHERE id = 123),
    'embedding',
    TABLE my_dataset.my_testdata,
    top_k => 5);

-- Use pre-filters with brute force. The data is filtered and then searched
-- with brute force for exact results.
SELECT query.test_id, base.type, distance
FROM
  VECTOR_SEARCH(
    (SELECT * FROM my_dataset.my_table WHERE id = 123),
    'embedding',
    TABLE my_dataset.my_testdata,
    options => '{"use_brute_force":true}');
```

如需创建后过滤器，必须在 `VECTOR_SEARCH` 函数之外应用查询的 `WHERE` 子句，以便它过滤搜索返回的结果。

以下示例展示了如何创建后过滤器：

```
-- Use post-filters. The index is used, but the entire table is searched and
-- the post-filtering might reduce the number of results.
SELECT query.test_id, base.type, distance
FROM
  VECTOR_SEARCH(
    TABLE my_dataset.my_table,
    'embedding',
    TABLE my_dataset.my_testdata,
    top_k => 5)
WHERE base.type = 'animal';

SELECT base.id, distance
FROM
  VECTOR_SEARCH(
    TABLE mydataset.base_table,
    'embedding',
    (SELECT embedding FROM mydataset.query_table),
    top_k => 10
  )
WHERE type = 'document' AND year > 2022
```

如果您使用后过滤，或者如果您指定的基表过滤器引用非存储列并因此充当后过滤器，则最终结果集包含的行数可能少于 `top_k`，甚至可能为零（如果谓词具有选择性）。如果您需要过滤后的结果数量达到特定值，请考虑指定更大的 `top_k` 值或在搜索函数调用中提高 `fraction_lists_to_search` 值。

在某些情况下，预过滤也可能会减小结果集的大小，尤其是当预过滤的条件很严格时。如果发生这种情况，请尝试在搜索函数调用中提高 `fraction_lists_to_search` 值。

### 使用存储列进行预过滤

如需进一步提高向量索引的效率，您可以指定基表中的列以存储在向量索引中。使用存储列可通过以下方式优化调用 `VECTOR_SEARCH` 或 `AI.SEARCH` 函数的查询：

* 您不必搜索整个表，而是可以对使用 `WHERE` 子句预先过滤基表的查询语句调用搜索函数。如果您的表具有索引，并且您仅过滤存储列，则 BigQuery 会在搜索之前过滤数据，然后使用索引搜索较小的结果集，从而优化查询。如果您过滤未存储的列，则 BigQuery 会在搜索表后应用过滤（即进行事后过滤）。
* `VECTOR_SEARCH` 和 `AI.SEARCH` 函数会输出名为 `base` 的结构体，其中包含基表中的所有列。如果没有存储列，则需要进行可能开销很大的联接来检索存储在 `base` 中的列。如果您使用 IVF 索引，并且您的查询仅从 `base` 中选择存储列，则 BigQuery 会优化查询以消除该联接。对于 TreeAH 索引，不会移除与基表的联接。
  TreeAH 索引中的存储列仅用于预过滤。

如需存储列，请在 [`CREATE VECTOR INDEX` 语句](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-cn#create_vector_index_statement)的 `STORING` 子句中列出这些列。
存储列会增加向量索引的大小，因此最好仅存储最常使用或过滤后的列。

以下示例创建了一个具有存储列的向量索引，然后运行一个仅选择存储列的向量搜索查询：

```
-- Create a table that contains an embedding.
CREATE TABLE my_dataset.my_table(embedding ARRAY<FLOAT64>, type STRING, creation_time DATETIME, id INT64);

-- Create a query table that contains an embedding.
CREATE TABLE my_dataset.my_testdata(embedding ARRAY<FLOAT64>, test_id INT64);

-- Create a vector index with stored columns.
CREATE VECTOR INDEX my_index ON my_dataset.my_table(embedding)
STORING (type, creation_time)
OPTIONS (index_type = 'IVF');

-- Select only stored columns from a vector search to avoid an expensive join.
SELECT query, base.type, distance
FROM
  VECTOR_SEARCH(
    TABLE my_dataset.my_table,
    'embedding'
    TABLE my_dataset.my_testdata);
```

#### 存储列限制

* 如果基表中列的模式、类型或架构发生更改，并且是向量索引中存储的列，则可能会延迟一段时间才会在向量索引中反映此更改。在为索引应用更新之前，向量搜索查询会使用基表中已修改的存储列。
* 当表的索引具有存储列时，如果从对该表进行的搜索查询的 `query` 输出中选择 `STRUCT` 类型的列，则整个查询可能会失败。

### 使用分区进行预过滤

**预览版**

此产品或功能 受[服务专用条款](https://docs.cloud.google.com/terms/service-terms?hl=zh-cn#1)的约束。
非正式版产品和功能“按原样”提供，可能只能获得有限的支持。
如需了解详情，请参阅[发布阶段说明](https://cloud.google.com/products/?hl=zh-cn#product-launch-stages)。

**注意**：如需就此功能提供反馈或请求支持，请联系 [bq-vector-search@google.com](mailto:bq-vector-search@google.com)

如果您要创建向量索引的表已分区，您可以选择也对向量索引进行分区。对向量索引进行分区具有以下优势：

* 除了表分区之外，分区删减还会应用于向量索引。当向量搜索对分区列的值使用符合条件的过滤条件时，就会进行分区删减。这样一来，BigQuery 就可以扫描与过滤条件匹配的分区，并跳过其余分区。分区删减可以降低 I/O 成本。如需详细了解分区删减，请参阅[查询分区表](https://docs.cloud.google.com/bigquery/docs/querying-partitioned-tables?hl=zh-cn)。
* 如果您对分区列进行预过滤，向量搜索就不太可能遗漏结果。

您只能对 TreeAH 向量索引进行分区。 您无法在[自动生成的嵌入列](https://docs.cloud.google.com/bigquery/docs/autonomous-embedding-generation?hl=zh-cn)上创建分区向量索引。

仅当您使用预过滤将大多数向量搜索限制在几个分区时，才建议对向量索引进行分区。

如需创建分区索引，请使用 [`CREATE VECTOR INDEX` 语句](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-cn#create_vector_index_statement)的 `PARTITION BY` 子句。您在 `CREATE VECTOR INDEX` 语句中指定的 `PARTITION BY` 子句必须与您要为其创建向量索引的表的 [`CREATE TABLE` 语句](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-cn#create_table_statement)中指定的 `PARTITION BY` 子句相同，如以下示例所示：

```
-- Create a date-partitioned table.
CREATE TABLE my_dataset.my_table(
  embeddings ARRAY
  id INT64,
  date DATE,
)
PARTITION BY date;

-- Create a partitioned vector index on the table.
CREATE VECTOR INDEX my_index ON my_dataset.my_table(embeddings)
PARTITION BY date
OPTIONS(index_type='TREE_AH', distance_type='COSINE');
```

如果表使用整数范围或时间单位列分区，则分区列会存储在向量索引中，这会增加存储费用。
如果表列同时用于 `CREATE VECTOR INDEX` 语句的 `STORING` 和 `PARTITION BY` 子句，则系统只会存储该列一次。

如需使用向量索引分区，请对 `VECTOR_SEARCH` 或 `AI.SEARCH` 调用的基本表子查询中的分区列进行过滤。在以下示例中，`samples.items` 表按 `produced_date` 列进行分区，因此 `VECTOR_SEARCH` 语句中的基础表子查询根据 `produced_date` 列进行过滤：

```
SELECT query.id, base.id, distance
FROM VECTOR_SEARCH(
  (SELECT * FROM my_dataset.my_table WHERE produced_date = '2025-01-01'),
  'embedding',
  TABLE samples.test,
  distance_type => 'COSINE',
  top_k => 10
);
```

#### 示例

在日期时间分区表上创建分区向量索引：

```
-- Create a datetime-partitioned table.
CREATE TABLE my_dataset.my_table(
  id INT64,
  produced_date DATETIME,
  embeddings ARRAY
)
PARTITION BY produced_date;

-- Create a partitioned vector index on the table.
CREATE VECTOR INDEX index0 ON my_dataset.my_table(embeddings)
PARTITION BY produced_date
OPTIONS(index_type='TREE_AH', distance_type='COSINE');
```

在时间戳分区表上创建分区向量索引：

```
-- Create a timestamp-partitioned table.
CREATE TABLE my_dataset.my_table(
  id INT64,
  produced_time TIMESTAMP,
  embeddings ARRAY
)
PARTITION BY TIMESTAMP_TRUNC(produced_time, HOUR);

-- Create a partitioned vector index on the table.
CREATE VECTOR INDEX index0 ON my_dataset.my_table(embeddings)
PARTITION BY TIMESTAMP_TRUNC(produced_time, HOUR)
OPTIONS(index_type='TREE_AH', distance_type='COSINE');
```

在整数范围分区表上创建分区向量索引：

```
-- Create a integer range-partitioned table.
CREATE TABLE my_dataset.my_table(
  id INT64,
  embeddings ARRAY
)
PARTITION BY RANGE_BUCKET(id, GENERATE_ARRAY(-100, 100, 20));

-- Create a partitioned vector index on the table.
CREATE VECTOR INDEX index0 ON my_dataset.my_table(embeddings)
PARTITION BY RANGE_BUCKET(id, GENERATE_ARRAY(-100, 100, 20))
OPTIONS(index_type='TREE_AH', distance_type='COSINE');
```

在注入时间分区表上创建分区向量索引：

```
-- Create a ingestion time-partitioned table.
CREATE TABLE my_dataset.my_table(
  id INT64,
  embeddings ARRAY
)
PARTITION BY TIMESTAMP_TRUNC(_PARTITIONTIME, DAY);

-- Create a partitioned vector index on the table.
CREATE VECTOR INDEX index0 ON my_dataset.my_table(embeddings)
PARTITION BY TIMESTAMP_TRUNC(_PARTITIONTIME, DAY)
OPTIONS(index_type='TREE_AH', distance_type='COSINE');
```

### 预过滤限制

* 您不能在预先过滤中使用[逻辑视图](https://docs.cloud.google.com/bigquery/docs/views-intro?hl=zh-cn)。
* 如果您的预先过滤包含[子查询](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/subqueries?hl=zh-cn)，则可能会干扰索引使用。

## 了解数据何时会被编入索引

向量索引由 BigQuery 完全管理，并且会在编入索引的表发生变化时自动刷新。

索引编制是异步的。向基表添加新行与新行反映在索引中之间存在延迟。不过，`VECTOR_SEARCH` 和 `AI.SEARCH` 函数仍会考虑所有行，不会遗漏未编入索引的行。对于已编入索引的记录，这些函数使用索引进行搜索，对于尚未编入索引的记录则使用暴力搜索进行搜索。

如果您在[自动生成的嵌入列](https://docs.cloud.google.com/bigquery/docs/autonomous-embedding-generation?hl=zh-cn)上创建向量索引，那么当至少 80% 的行生成嵌入后，系统就会开始训练索引。

如果您在小于 10 MB 的表上创建向量索引，则系统不会填充该向量索引。同样，如果您从编入索引的表中删除数据，并且该表大小低于 10 MB，则系统会暂时停用向量索引。在这种情况下，向量搜索查询不使用该索引，并且 `Job` 资源的 [`vectorSearchStatistics`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-cn#vectorsearchstatistics) 部分中的 `indexUnusedReasons` 代码为 `BASE_TABLE_TOO_SMALL`。在没有索引的情况下，您的搜索功能会自动转为使用暴力破解来查找嵌入的最近邻。

如果您删除表中编入索引的列或重命名表本身，则向量索引会自动被删除。

## 监控向量索引的状态

您可以通过查询 `INFORMATION_SCHEMA` 视图来监控向量索引的健康状况。以下视图包含有关向量索引的元数据：

* [`INFORMATION_SCHEMA.VECTOR_INDEXES` 视图](https://docs.cloud.google.com/bigquery/docs/information-schema-vector-indexes?hl=zh-cn)具有数据集中的向量索引的相关信息。

  `CREATE VECTOR INDEX` 语句完成后，您在使用索引之前，必须先填充该索引。您可以使用 `last_refresh_time` 和 `coverage_percentage` 列来验证向量索引的就绪情况。如果向量索引尚未就绪，您仍然可以对表使用 `VECTOR_SEARCH` 和 `AI.SEARCH` 函数，只是在没有索引的情况下，其运行速度可能会更慢。
* [`INFORMATION_SCHEMA.VECTOR_INDEX_COLUMNS` 视图](https://docs.cloud.google.com/bigquery/docs/information-schema-vector-index-columns?hl=zh-cn)具有数据集中所有表的向量索引列的相关信息。
* [`INFORMATION_SCHEMA.VECTOR_INDEX_OPTIONS` 视图](https://docs.cloud.google.com/bigquery/docs/information-schema-vector-index-options?hl=zh-cn)具有数据集中向量索引使用的选项的相关信息。

### 向量索引示例

以下示例展示了位于项目 `my_project` 的数据集 `my_dataset` 中表的所有活跃向量索引。它包括索引名称、用于创建索引的 DDL 语句以及索引覆盖率百分比。如果编入索引的基表小于 10 MB，则系统不会填充其索引，在这种情况下，`coverage_percentage` 值为 0。

```
SELECT table_name, index_name, ddl, coverage_percentage
FROM my_project.my_dataset.INFORMATION_SCHEMA.VECTOR_INDEXES
WHERE index_status = 'ACTIVE';
```

结果类似于以下内容：

```
+------------+------------+-------------------------------------------------------------------------------------------------+---------------------+
| table_name | index_name | ddl                                                                                             | coverage_percentage |
+------------+------------+-------------------------------------------------------------------------------------------------+---------------------+
| table1     | indexa     | CREATE VECTOR INDEX `indexa` ON `my_project.my_dataset.table1`(embeddings)                      | 100                 |
|            |            | OPTIONS (distance_type = 'EUCLIDEAN', index_type = 'IVF', ivf_options = '{"num_lists": 100}')   |                     |
+------------+------------+-------------------------------------------------------------------------------------------------+---------------------+
| table2     | indexb     | CREATE VECTOR INDEX `indexb` ON `my_project.my_dataset.table2`(vectors)                         | 42                  |
|            |            | OPTIONS (distance_type = 'COSINE', index_type = 'IVF', ivf_options = '{"num_lists": 500}')      |                     |
+------------+------------+-------------------------------------------------------------------------------------------------+---------------------+
| table3     | indexc     | CREATE VECTOR INDEX `indexc` ON `my_project.my_dataset.table3`(vectors)                         | 98                  |
|            |            | OPTIONS (distance_type = 'DOT_PRODUCT', index_type = 'TREE_AH',                                 |                     |
|            |            |          tree_ah_options = '{"leaf_node_embedding_count": 1000, "normalization_type": "NONE"}') |                     |
+------------+------------+-------------------------------------------------------------------------------------------------+---------------------+
```

### 向量索引列示例

以下查询会提取具有向量索引的列的相关信息：

```
SELECT table_name, index_name, index_column_name, index_field_path
FROM my_project.dataset.INFORMATION_SCHEMA.VECTOR_INDEX_COLUMNS;
```

结果类似于以下内容：

```
+------------+------------+-------------------+------------------+
| table_name | index_name | index_column_name | index_field_path |
+------------+------------+-------------------+------------------+
| table1     | indexa     | embeddings        | embeddings       |
| table2     | indexb     | vectors           | vectors          |
| table3     | indexc     | vectors           | vectors          |
+------------+------------+-------------------+------------------+
```

### 向量索引选项示例

以下查询会提取向量索引选项的相关信息：

```
SELECT table_name, index_name, option_name, option_type, option_value
FROM my_project.dataset.INFORMATION_SCHEMA.VECTOR_INDEX_OPTIONS;
```

结果类似于以下内容：

```
+------------+------------+------------------+------------------+-------------------------------------------------------------------+
| table_name | index_name | option_name      | option_type      | option_value                                                      |
+------------+------------+------------------+------------------+-------------------------------------------------------------------+
| table1     | indexa     | index_type       | STRING           | IVF                                                               |
| table1     | indexa     | distance_type    | STRING           | EUCLIDEAN                                                         |
| table1     | indexa     | ivf_options      | STRING           | {"num_lists": 100}                                                |
| table2     | indexb     | index_type       | STRING           | IVF                                                               |
| table2     | indexb     | distance_type    | STRING           | COSINE                                                            |
| table2     | indexb     | ivf_options      | STRING           | {"num_lists": 500}                                                |
| table3     | indexc     | index_type       | STRING           | TREE_AH                                                           |
| table3     | indexc     | distance_type    | STRING           | DOT_PRODUCT                                                       |
| table3     | indexc     | tree_ah_options  | STRING           | {"leaf_node_embedding_count": 1000, "normalization_type": "NONE"} |
+------------+------------+------------------+------------------+-------------------------------------------------------------------+
```

## 验证向量索引使用情况

运行向量搜索查询的作业的作业元数据中提供了有关向量索引使用情况的信息。您可以使用 Google Cloud 控制台、bq 命令行工具、BigQuery API 或客户端库[查看作业元数据](https://docs.cloud.google.com/bigquery/docs/managing-jobs?hl=zh-cn#view-job)。

使用 Google Cloud 控制台时，您可以在**向量索引使用模式**和**未使用向量索引的原因**字段中找到向量索引使用情况信息。

使用 bq 工具或 BigQuery API 时，您可以在 `Job` 资源的 [`VectorSearchStatistics`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-cn#vectorsearchstatistics) 部分中找到向量索引使用情况信息。

索引使用模式通过提供以下值之一来指示是否使用了向量索引：

* `UNUSED`：未使用向量索引。
* `PARTIALLY_USED`：查询中的某些搜索函数使用向量索引，某些函数则不使用。
* `FULLY_USED`：查询中的每个搜索函数都使用一个向量索引。

当索引使用模式值为 `UNUSED` 或 `PARTIALLY_USED` 时，未使用索引的原因会指明没有在查询中使用向量索引的原因。

例如，`bq show --format=prettyjson -j my_job_id` 返回的以下结果表明，由于在 `VECTOR_SEARCH` 函数中指定了 `use_brute_force` 选项，因此未使用索引：

```
"vectorSearchStatistics": {
  "indexUnusedReasons": [
    {
      "baseTable": {
        "datasetId": "my_dataset",
        "projectId": "my_project",
        "tableId": "my_table"
      },
      "code": "INDEX_SUPPRESSED_BY_FUNCTION_OPTION",
      "message": "No vector index was used for the base table `my_project:my_dataset.my_table` because use_brute_force option has been specified."
    }
  ],
  "indexUsageMode": "UNUSED"
}
```

## 索引管理选项

要创建索引并让 BigQuery 维护它们，您有两种选择：

* [使用默认共享槽池](#use_shared_slots)：当计划编入索引的数据低于每个组织的[限制](https://docs.cloud.google.com/bigquery/quotas?hl=zh-cn#index_limits)时，您可以使用免费共享槽池来管理索引。
* [使用您自己的预留](#use_your_own_reservation)：要在较大的生产工作负载上实现更可预测且一致的索引编制进度，您可以使用自己的预留来管理索引。

### 使用共享槽

如果您尚未将项目配置为使用[专用预留](#use_your_own_reservation)来执行索引操作，就会在免费的共享槽池中处理索引管理，但存在以下限制。

如果向表添加数据，从而导致编入索引的表的总大小超过组织的[限制](https://docs.cloud.google.com/bigquery/quotas?hl=zh-cn#index_limits)，则 BigQuery 会暂停该表的索引管理。发生这种情况时，[`INFORMATION_SCHEMA.VECTOR_INDEXES` 视图](https://docs.cloud.google.com/bigquery/docs/information-schema-vector-indexes?hl=zh-cn)中的 `index_status` 字段会显示 `PENDING DISABLEMENT`，且该索引会排队等待删除。虽然索引正在等待停用，但它仍然在查询中使用，并且您需要为该索引支付存储费用。索引删除后，`index_status` 字段会将该索引显示为 `TEMPORARILY DISABLED`。在此状态下，查询不使用该索引，并且您不需要为该索引支付存储费用。在这种情况下，[`IndexUnusedReason` 代码](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-cn#indexunusedreason)为 `BASE_TABLE_TOO_LARGE`。

如果您从表中删除数据，并且编入索引的表的总大小低于每个组织的限制，则索引管理将恢复。`INFORMATION_SCHEMA.VECTOR_INDEXES` 视图中的 `index_status` 字段为 `ACTIVE`，查询可以使用该索引，并且您需要为该索引支付存储费用。

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

## 重建向量索引

**预览版**

此产品或功能 受[服务专用条款](https://docs.cloud.google.com/terms/service-terms?hl=zh-cn#1)的约束。
非正式版产品和功能“按原样”提供，可能只能获得有限的支持。
如需了解详情，请参阅[发布阶段说明](https://cloud.google.com/products/?hl=zh-cn#product-launch-stages)。

**注意**：如需就此功能提供反馈或请求支持，请发送电子邮件至 [bq-vector-search@google.com](mailto:bq-vector-search@google.com)。

在创建向量索引后，如果表数据发生显著变化，向量索引的效率可能会降低。当向量索引的效率较低时，最初在使用该索引时具有较高[召回率](https://developers.google.com/machine-learning/glossary?hl=zh-cn#recall)的向量搜索查询将具有较低的召回率，因为基表中的数据分布变化未在向量索引中体现出来。

如果您想在不增加搜索查询延迟时间的情况下提高召回率，请重建向量索引。或者，您也可以增加向量搜索的 `fraction_lists_to_search` 选项的值来提高召回率，但这通常会使搜索查询变慢。

您可以使用 [`VECTOR_INDEX.STATISTICS` 函数](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/vectorindex_functions?hl=zh-cn#vector_indexstatistics)来计算索引表的数据在向量索引创建时间与当前时间之间的漂移量。如果表数据发生的变化足以需要重建向量索引，您可以使用 [`ALTER VECTOR INDEX REBUILD` 语句](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-cn#alter_vector_index_rebuild_statement)重建向量索引。

如需重建向量索引，请按照以下步骤操作：

1. 转到 **BigQuery** 页面。

   [转到 BigQuery](https://console.cloud.google.com/bigquery?hl=zh-cn)
2. 在查询编辑器中，运行以下 SQL 语句以检查已建立索引的表的数据漂移：

   ```
   SELECT * FROM VECTOR_INDEX.STATISTICS(TABLE DATASET_NAME.TABLE_NAME);
   ```

   替换以下内容：

   * `DATASET_NAME`：包含已编入索引的表的数据集的名称。
   * `TABLE_NAME`：包含向量索引的表的名称。

   该函数会返回范围为 `[0,1)` 的 `FLOAT64` 值。值越低，表示漂移越小。通常，`0.3` 或更大的值被认为是足够显著的变化，表示向量索引重建可能会有益。
3. 如果 `VECTOR_INDEX.STATISTICS` 函数显示表数据漂移比较明显，请运行以下 SQL 语句重建向量索引：

   ```
   ALTER VECTOR INDEX IF EXISTS INDEX_NAME
   ON DATASET_NAME.TABLE_NAME
   REBUILD;
   ```

   替换以下内容：

   * `INDEX_NAME`：您要重建的向量索引的名称。
   * `DATASET_NAME`：包含已编入索引的表的数据集的名称。
   * `TABLE_NAME`：包含向量索引的表的名称。

## 删除矢量索引

当您不再需要向量索引或想要更改表中编入索引的列时，可以使用 [`DROP VECTOR INDEX` DDL 语句](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-cn#drop_vector_index)删除该表上的索引：

1. 转到 **BigQuery** 页面。

   [转到 BigQuery](https://console.cloud.google.com/bigquery?hl=zh-cn)
2. 在查询编辑器中，运行以下 SQL 语句：

   ```
   DROP VECTOR INDEX INDEX_NAME ON DATASET_NAME.TABLE_NAME;
   ```

   替换以下内容：

   * `INDEX_NAME`：您要删除的向量索引的名称。
   * `DATASET_NAME`：包含已编入索引的表的数据集的名称。
   * `TABLE_NAME`：包含向量索引的表的名称。

如果删除编入索引的表，其索引也会自动删除。

## 将嵌入导出到 Vertex AI Vector Search

为了实现超低延迟的在线应用，请使用 BigQuery 与 Vertex AI [Vector Search](https://docs.cloud.google.com/vertex-ai/docs/vector-search/overview?hl=zh-cn) 的集成，将 BigQuery 嵌入导入到 Vector Search 中，并部署低延迟端点。如需了解详情，请参阅[从 BigQuery 导入索引数据](https://docs.cloud.google.com/vertex-ai/docs/vector-search/import-index-data-from-big-query?hl=zh-cn)。

## 后续步骤

* 如需大致了解向量索引用例、价格和限制，请参阅[向量搜索简介](https://docs.cloud.google.com/bigquery/docs/vector-search-intro?hl=zh-cn)。
* 了解如何使用 [`VECTOR_SEARCH` 函数](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/search_functions?hl=zh-cn#vector_search)执行向量搜索。
* 了解如何使用 [`AI.SEARCH` 函数](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-ai-search?hl=zh-cn)执行语义搜索。
* 详细了解 [`CREATE VECTOR INDEX` 语句](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-cn#create_vector_index_statement)。
* 试用[使用向量搜索来搜索嵌入](https://docs.cloud.google.com/bigquery/docs/vector-search?hl=zh-cn)教程。




发送反馈

如未另行说明，那么本页面中的内容已根据[知识共享署名 4.0 许可](https://creativecommons.org/licenses/by/4.0/)获得了许可，并且代码示例已根据 [Apache 2.0 许可](https://www.apache.org/licenses/LICENSE-2.0)获得了许可。有关详情，请参阅 [Google 开发者网站政策](https://developers.google.com/site-policies?hl=zh-cn)。Java 是 Oracle 和/或其关联公司的注册商标。

最后更新时间 (UTC)：2025-12-23。




需要向我们提供更多信息？

[[["易于理解","easyToUnderstand","thumb-up"],["解决了我的问题","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["很难理解","hardToUnderstand","thumb-down"],["信息或示例代码不正确","incorrectInformationOrSampleCode","thumb-down"],["没有我需要的信息/示例","missingTheInformationSamplesINeed","thumb-down"],["翻译问题","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["最后更新时间 (UTC)：2025-12-23。"],[],[]]