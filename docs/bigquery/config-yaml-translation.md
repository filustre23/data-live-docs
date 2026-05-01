* [Home](https://docs.cloud.google.com/?hl=zh-cn)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-cn)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-cn)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-cn)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-cn)

发送反馈



使用集合让一切井井有条

根据您的偏好保存内容并对其进行分类。

# 使用配置 YAML 文件转换 SQL 转译

本文档介绍如何在将 SQL 代码迁移到 BigQuery 时使用配置 YAML 文件来转换该代码。该文档中提供了供您创建自己的配置 YAML 文件的准则，并提供了此功能支持的各种转译转换的示例。

使用 [BigQuery 交互式 SQL 转换器](https://docs.cloud.google.com/bigquery/docs/interactive-sql-translator?hl=zh-cn)、使用 [BigQuery Migration API](https://docs.cloud.google.com/bigquery/docs/api-sql-translator?hl=zh-cn) 或执行[批量 SQL 转换](https://docs.cloud.google.com/bigquery/docs/batch-sql-translator?hl=zh-cn)时，您可以提供配置 YAML 文件来修改 SQL 查询转换。使用配置 YAML 文件可以在从源数据库转译 SQL 查询时进行进一步自定义。

您可以通过以下方式指定要在 SQL 转译中使用的配置 YAML 文件：

* 如果您使用的是交互式 SQL 转换器，请[在转译设置中指定配置文件的文件路径或批量转换作业 ID](https://docs.cloud.google.com/bigquery/docs/interactive-sql-translator?hl=zh-cn#translate-with-additional-configs)。
* 如果您使用的是 BigQuery Migration API，请将配置 YAML 放在输入 SQL 文件所在的 Cloud Storage 存储桶中。
* 如果您要执行批量 SQL 转译，请将配置 YAML 放在输入 SQL 文件所在的 Cloud Storage 存储桶中。
* 如果您使用的是[批量转换 Python 客户端](https://github.com/google/dwh-migration-tools/tree/main/client#readme)，请将配置 YAML 文件放在本地转译输入文件夹中。

**注意：**对于基于 API 的转换，我们建议您使用 BigQuery Migration API，而不是批量 SQL 转换 API 或客户端。

交互式 SQL 转换器、BigQuery Migration API、批量 SQL 转换器和批量转换 Python 客户端支持在单个转换作业中使用多个配置 YAML 文件。如需了解详情，请参阅[应用多个 YAML 配置](https://docs.cloud.google.com/bigquery/docs/config-yaml-translation?hl=zh-cn#yaml_multiple)。

## 配置 YAML 文件要求

在创建配置 YAML 文件之前，请查看以下信息，以确保您的 YAML 文件与 BigQuery Migration Service 兼容：

* 您必须将配置 YAML 文件上传到包含 SQL 转换输入文件的 Cloud Storage 存储桶的目录。如需了解如何创建存储桶并将文件上传到 Cloud Storage，请参阅[创建存储桶](https://docs.cloud.google.com/storage/docs/creating-buckets?hl=zh-cn)和[从文件系统上传对象](https://docs.cloud.google.com/storage/docs/uploading-objects?hl=zh-cn)。
* 单个配置 YAML 文件的文件大小不得超过 1 MB。
* 单个 SQL 转译作业中使用的所有配置 YAML 文件的总大小不得超过 4 MB。
* 如果您使用 `regex` 语法进行名称匹配，请使用 [RE2/J](https://github.com/google/re2j)。
* 所有配置 YAML 文件名都必须包含 `.config.yaml` 扩展名，例如 `change-case.config.yaml`。
  + 单是 `config.yaml` 并不构成有效的配置文件名称。

## 创建配置 YAML 文件的指南

本部分提供了创建配置 YAML 文件的一些常规准则：

### 标题

每个配置文件都必须包含指定配置类型的标头。`object_rewriter` 类型用于在配置 YAML 文件中指定 SQL 转译。以下示例使用 `object_rewriter` 类型来转换名称大小写：

```
type: object_rewriter
global:
  case:
    all: UPPERCASE
```

### 实体选择

如需执行特定于实体的转换，请在配置文件中指定实体。所有 `match` 属性均为可选属性；仅使用转换所需的 `match` 属性。下面的配置 YAML 公开了为选择特定实体要匹配的属性：

```
match:
  database: <literal_name>
  schema: <literal_name>
  relation: <literal_name>
  attribute: <literal_name>
  databaseRegex: <regex>
  schemaRegex: <regex>
  relationRegex: <regex>
  attributeRegex: <regex>
```

每个 `match` 属性的说明：

* `database` 或 `db`：project\_id 组件。
* `schema`：数据集组件。
* `relation`：表组件。
* `attribute`：列组件。仅对属性选择有效
* `databaseRegex` 或 `dbRegex`：通过正则表达式匹配 `database` 属性（[预览版](https://cloud.google.com/products/?hl=zh-cn#product-launch-stages)）。
* `schemaRegex`：通过正则表达式匹配 `schema` 属性（[预览版](https://cloud.google.com/products/?hl=zh-cn#product-launch-stages)）。
* `relationRegex`：通过正则表达式匹配 `relation` 属性（[预览版](https://cloud.google.com/products/?hl=zh-cn#product-launch-stages)）。
* `attributeRegex`：通过正则表达式匹配 `attribute` 属性。仅适用于属性选择（[预览版](https://cloud.google.com/products/?hl=zh-cn#product-launch-stages)）。

例如，以下配置 YAML 指定了 `match` 属性，以便选择用于临时表转换的 `testdb.acme.employee` 表。

```
type: object_rewriter
relation:
-
  match:
    database: testdb
    schema: acme
    relation: employee
  temporary: true
```

您可以使用 `databaseRegex`、`schemaRegex`、`relationRegex` 和 `attributeRegex` 属性指定正则表达式，以选择实体子集。以下示例会将所有关系从 `testdb` 中的 `tmp_schema` 架构更改为临时，只要其名称以`tmp_` 开头：

```
type: object_rewriter
relation:
-
  match:
    schema: tmp_schema
    relationRegex: "tmp_.*"
  temporary: true
```

字面量属性和 `regex` 属性均不区分大小写。您可以通过配合使用 `regex` 和已停用的 `i` 标志来强制执行区分大小写的匹配，如以下示例所示：

```
match:
  relationRegex: "(?-i:<actual_regex>)"
```

您还可以使用等效的短字符串语法指定完全限定的实体。短字符串语法需要使用正好 3（对于关系选择）或 4（对于属性选择）个名称段并以点分隔，例如 `testdb.acme.employee`。然后，这些名称段会在内部解读，就好像它们分别作为 `database`、`schema`、`relation` 和 `attribute` 传递。也就是说，名称按字面量进行匹配，因此短语法中不允许使用正则表达式。以下示例显示了使用短字符串语法在配置 YAML 文件中指定完全限定的实体：

```
type: object_rewriter
relation:
-
  match : "testdb.acme.employee"
  temporary: true
```

如果表的名称中包含一个点，则不能使用短语法指定该名称。在这种情况下，您必须使用对象匹配。以下示例将 `testdb.acme.stg.employee` 表更改为临时表：

```
type: object_rewriter
relation:
-
  match:
    database: testdb
    schema: acme
    relation: stg.employee
  temporary: true
```

配置 YAML 接受 `key` 作为 `match` 的别名。

### 默认数据库

某些输入 SQL 方言（尤其是 Teradata）不支持限定名称中的 `database-name`。在这种情况下，匹配实体最简单的方法是省略 `match` 中的 `database` 属性。

但是，您可以设置 BigQuery Migration Service 的 `default_database` 属性并在 `match` 中使用该默认数据库。

### 支持的目标属性类型

您可以使用配置 YAML 文件[执行属性类型转换](#change_type_of_a_column_attribute)，你会在其中将列的数据类型从源类型转换为目标类型。配置 YAML 文件支持以下目标类型：

* `BOOLEAN`
* `TINYINT`
* `SMALLINT`
* `INTEGER`
* `BIGINT`
* `FLOAT`
* `DOUBLE`
* `NUMERIC`（支持可选的精度和比例，例如 `NUMERIC(18, 2)`）
* `TIME`
* `TIMETZ`
* `DATE`
* `DATETIME`
* `TIMESTAMP`
* `TIMESTAMPTZ`
* `CHAR`（支持可选精度，例如 `CHAR(42)`）
* `VARCHAR`（支持可选精度，例如 `VARCHAR(42)`）

## 配置 YAML 示例

本部分提供了创建用于 SQL 转译的各种配置 YAML 文件的示例。每个示例都概述了以特定方式转换 SQL 转译的 YAML 语法以及简要说明。
每个示例还提供了 `teradata-input.sql` 或 `hive-input.sql` 文件以及 `bq-output.sql` 文件的内容，以便您比较配置 YAML 对 BigQuery SQL 查询转译的影响。

以下示例使用 Teradata 或 Hive 作为输入 SQL 方言，并使用 BigQuery SQL 作为输出方言。以下示例还使用 `testdb` 作为默认数据库，使用 `testschema` 作为架构搜索路径。

### 更改对象名称大小写

**预览版**

此产品或功能 受[服务专用条款](https://docs.cloud.google.com/terms/service-terms?hl=zh-cn#1)的约束。
非正式版产品和功能“按原样”提供，可能只能获得有限的支持。
如需了解详情，请参阅[发布阶段说明](https://cloud.google.com/products/?hl=zh-cn#product-launch-stages)。

以下配置 YAML 会更改对象名称的大写或小写形式：

```
type: object_rewriter
global:
  case:
    all: UPPERCASE
    database: LOWERCASE
    attribute: LOWERCASE
```

具有此配置 YAML 文件的 SQL 转译可能如下所示：

|  |  |
| --- | --- |
| `teradata-input.sql` | ```       create table x(a int);       select * from x; ``` |
| `bq-output.sql` | ```       CREATE TABLE testdb.TESTSCHEMA.X       (         a INT64       )       ;       SELECT           X.a         FROM           testdb.TESTSCHEMA.X       ; ``` |

### 将表设为临时表

**预览版**

此产品或功能 受[服务专用条款](https://docs.cloud.google.com/terms/service-terms?hl=zh-cn#1)的约束。
非正式版产品和功能“按原样”提供，可能只能获得有限的支持。
如需了解详情，请参阅[发布阶段说明](https://cloud.google.com/products/?hl=zh-cn#product-launch-stages)。

以下配置 YAML 会将常规表更改为[临时表](https://docs.cloud.google.com/bigquery/docs/writing-results?hl=zh-cn#temporary_and_permanent_tables)：

```
type: object_rewriter
relation:
  -
    match: "testdb.testschema.x"
    temporary: true
```

具有此配置 YAML 文件的 SQL 转译可能如下所示：

|  |  |
| --- | --- |
| `teradata-input.sql` | ```     create table x(a int); ``` |
| `bq-output.sql` | ```     CREATE TEMPORARY TABLE x     (       a INT64     )     ; ``` |

### 将表设为短暂表

**预览版**

此产品或功能 受[服务专用条款](https://docs.cloud.google.com/terms/service-terms?hl=zh-cn#1)的约束。
非正式版产品和功能“按原样”提供，可能只能获得有限的支持。
如需了解详情，请参阅[发布阶段说明](https://cloud.google.com/products/?hl=zh-cn#product-launch-stages)。

以下配置 YAML 会将常规表更改为有效期为 60 秒的[临时表](https://docs.cloud.google.com/bigquery/docs/managing-tables?hl=zh-cn#updating_a_tables_expiration_time)。

```
type: object_rewriter
relation:
  -
    match: "testdb.testschema.x"
    ephemeral:
      expireAfterSeconds: 60
```

具有此配置 YAML 文件的 SQL 转译可能如下所示：

|  |  |
| --- | --- |
| `teradata-input.sql` | ```     create table x(a int); ``` |
| `bq-output.sql` | ```     CREATE TABLE testdb.testschema.x     (       a INT64     )     OPTIONS(       expiration_timestamp=timestamp_add(current_timestamp(), interval 60 SECOND)     ); ``` |

### 设置分区有效期

**预览版**

此产品或功能 受[服务专用条款](https://docs.cloud.google.com/terms/service-terms?hl=zh-cn#1)的约束。
非正式版产品和功能“按原样”提供，可能只能获得有限的支持。
如需了解详情，请参阅[发布阶段说明](https://cloud.google.com/products/?hl=zh-cn#product-launch-stages)。

以下配置 YAML 会将[分区表的有效期](https://docs.cloud.google.com/bigquery/docs/managing-partitioned-tables?hl=zh-cn#partition-expiration)更改为 1 天：

```
type: object_rewriter
relation:
  -
    match: "testdb.testschema.x"
    partitionLifetime:
      expireAfterSeconds: 86400
```

具有此配置 YAML 文件的 SQL 转译可能如下所示：

|  |  |
| --- | --- |
| `teradata-input.sql` | ```     create table x(a int, b int) partition by (a); ``` |
| `bq-output.sql` | ```     CREATE TABLE testdb.testschema.x     (       a INT64,       b INT64     )     CLUSTER BY a     OPTIONS(       partition_expiration_days=1     ); ``` |

### 更改表的外部位置或格式

**预览版**

此产品或功能 受[服务专用条款](https://docs.cloud.google.com/terms/service-terms?hl=zh-cn#1)的约束。
非正式版产品和功能“按原样”提供，可能只能获得有限的支持。
如需了解详情，请参阅[发布阶段说明](https://cloud.google.com/products/?hl=zh-cn#product-launch-stages)。

以下配置 YAML 会更改[表的外部位置和格式](https://docs.cloud.google.com/bigquery/docs/external-data-sources?hl=zh-cn#external_tables)：

```
type: object_rewriter
relation:
  -
    match: "testdb.testschema.x"
    external:
      locations: "gs://path/to/department/files"
      format: ORC
```

具有此配置 YAML 文件的 SQL 转译可能如下所示：

|  |  |
| --- | --- |
| `teradata-input.sql` | ```     create table x(a int); ``` |
| `bq-output.sql` | ```     CREATE EXTERNAL TABLE testdb.testschema.x     (       a INT64     )     OPTIONS(       format='ORC',       uris=[         'gs://path/to/department/files'       ]     ); ``` |

### 设置或更改表说明

**预览版**

此产品或功能 受[服务专用条款](https://docs.cloud.google.com/terms/service-terms?hl=zh-cn#1)的约束。
非正式版产品和功能“按原样”提供，可能只能获得有限的支持。
如需了解详情，请参阅[发布阶段说明](https://cloud.google.com/products/?hl=zh-cn#product-launch-stages)。

以下配置 YAML 会设置表的说明：

```
type: object_rewriter
relation:
  -
    match: "testdb.testschema.x"
    description:
      text: "Example description."
```

具有此配置 YAML 文件的 SQL 转译可能如下所示：

|  |  |
| --- | --- |
| `teradata-input.sql` | ```     create table x(a int); ``` |
| `bq-output.sql` | ```     CREATE TABLE testdb.testschema.x     (       a INT64     )     OPTIONS(       description='Example description.'     ); ``` |

### 设置或更改表分区

以下配置 YAML 会更改[表的分区方案](https://docs.cloud.google.com/bigquery/docs/partitioned-tables?hl=zh-cn)：

```
type: object_rewriter
relation:
  -
    match: "testdb.testschema.x"
    partition:
      simple:
        add: [a]
  -
    match: "testdb.testschema.y"
    partition:
      simple:
        remove: [a]
```

具有此配置 YAML 文件的 SQL 转译可能如下所示：

|  |  |
| --- | --- |
| `teradata-input.sql` | ```     create table x(a date, b int);     create table y(a date, b int) partition by (a); ``` |
| `bq-output.sql` | ```     CREATE TABLE testdb.testschema.x     (       a DATE,       b INT64     )     PARTITION BY a;     CREATE TABLE testdb.testschema.y     (       a DATE,       b INT64     )     ; ``` |

### 设置或更改表聚簇

以下配置 YAML 会更改[表的聚簇方案](https://docs.cloud.google.com/bigquery/docs/clustered-tables?hl=zh-cn)：

```
type: object_rewriter
relation:
  -
    match: "testdb.testschema.x"
    clustering:
      add: [a]
  -
    match: "testdb.testschema.y"
    clustering:
      remove: [b]
```

具有此配置 YAML 文件的 SQL 转译可能如下所示：

|  |  |
| --- | --- |
| `hive-input.sql` | ```     create table x(a int, b int);     create table y(a int, b int) clustered by (b) into 16 buckets; ``` |
| `bq-output.sql` | ```     CREATE TABLE testdb.testschema.x     (       a INT64,       b INT64     )     CLUSTER BY a;     CREATE TABLE testdb.testschema.y     (       a INT64,       b INT64     )     ; ``` |

### 更改列属性的类型

**预览版**

此产品或功能 受[服务专用条款](https://docs.cloud.google.com/terms/service-terms?hl=zh-cn#1)的约束。
非正式版产品和功能“按原样”提供，可能只能获得有限的支持。
如需了解详情，请参阅[发布阶段说明](https://cloud.google.com/products/?hl=zh-cn#product-launch-stages)。

以下配置 YAML 会更改列属性的数据类型：

```
type: object_rewriter
attribute:
  -
    match:
      database: testdb
      schema: testschema
      attributeRegex: "a+"
    type:
      target: NUMERIC(10,2)
```

您可以将源数据类型转换为任何[受支持的目标属性类型](#supported_target_attribute_types)。

具有此配置 YAML 文件的 SQL 转译可能如下所示：

|  |  |
| --- | --- |
| `teradata-input.sql` | ```     create table x(a int, b int, aa int); ``` |
| `bq-output.sql` | ```     CREATE TABLE testdb.testschema.x     (       a NUMERIC(31, 2),       b INT64,       aa NUMERIC(31, 2)     )     ; ``` |

**注意：**BigQuery 转译会将数值精度提高到给定额度的最高精度。

### 添加与外部数据湖的连接

**预览版**

此产品或功能 受[服务专用条款](https://docs.cloud.google.com/terms/service-terms?hl=zh-cn#1)的约束。
非正式版产品和功能“按原样”提供，可能只能获得有限的支持。
如需了解详情，请参阅[发布阶段说明](https://cloud.google.com/products/?hl=zh-cn#product-launch-stages)。

下面的配置 YAML 会将源表标记为指向存储在外部数据湖（通过数据湖连接指定）中数据的外部表。

```
type: object_rewriter
relation:
-
  key: "testdb.acme.employee"
  external:
    connection_id: "connection_test"
```

具有此配置 YAML 文件的 SQL 转译可能如下所示：

|  |  |
| --- | --- |
| `hive-input.sql` | ```     CREATE TABLE x     (       a VARCHAR(150),       b INT     ); ``` |
| `bq-output.sql` | ```     CREATE EXTERNAL TABLE x     (       a STRING,       b INT64     )     WITH CONNECTION `connection_test`     OPTIONS(     ); ``` |

### 更改输入文件的字符编码

**预览版**

此产品或功能 受[服务专用条款](https://docs.cloud.google.com/terms/service-terms?hl=zh-cn#1)的约束。
非正式版产品和功能“按原样”提供，可能只能获得有限的支持。
如需了解详情，请参阅[发布阶段说明](https://cloud.google.com/products/?hl=zh-cn#product-launch-stages)。

默认情况下，BigQuery Migration Service 会尝试自动检测输入文件的字符编码。在 BigQuery Migration Service 可能错误地标识文件的编码的情况下，您可以使用配置 YAML 明确指定字符编码。

下面的配置 YAML 将输入文件的明确字符编码指定为 `ISO-8859-1`。

```
type: experimental_input_formats
formats:
- source:
    pathGlob: "*.sql"
  contents:
    raw:
      charset: iso-8859-1
```

### 全局类型转换

**预览版**

此产品或功能 受[服务专用条款](https://docs.cloud.google.com/terms/service-terms?hl=zh-cn#1)的约束。
非正式版产品和功能“按原样”提供，可能只能获得有限的支持。
如需了解详情，请参阅[发布阶段说明](https://cloud.google.com/products/?hl=zh-cn#product-launch-stages)。

下面的配置 YAML 会在所有脚本中将一种数据类型更改为另一种数据类型，并指定在转译的脚本中应避免的源数据类型。这与[更改列属性的类型](https://docs.cloud.google.com/bigquery/docs/config-yaml-translation?hl=zh-cn#change_type_of_a_column_attribute)配置不同，后者仅更改单个属性的数据类型。

BigQuery 支持以下数据类型转换：

* `DATETIME` 至 `TIMESTAMP`
* `TIMESTAMP` 到 `DATETIME`（接受可选时区）
* `TIMESTAMP WITH TIME ZONE` 到 `DATETIME`（接受可选时区）
* `CHAR` 至 `VARCHAR`

在下面的示例中，配置 YAML 会将 `TIMESTAMP` 数据类型转换为 `DATETIME`。

```
type: experimental_object_rewriter
global:
  typeConvert:
    timestamp: DATETIME
```

在 Teradata 等方言中，与日期时间相关的函数（如 `current_date`、`current_time` 或 `current_timestamp`）会根据配置的时区（本地或会话）返回时间戳。另一方面，BigQuery 一律以世界协调时间 (UTC) 返回时间戳。为确保这两种方言之间的行为一致，必须相应地配置时区。

在以下示例中，配置 YAML 会将 `TIMESTAMP` 和 `TIMESTAMP WITH TIME ZONE` 数据类型转换为 `DATETIME`，并将目标时区设置为 `Europe/Paris`。

```
type: experimental_object_rewriter
global:
  typeConvert:
    timestamp:
      target: DATETIME
      timezone: Europe/Paris
    timestamptz:
      target: DATETIME
      timezone: Europe/Paris
```

具有此配置 YAML 文件的 SQL 转译可能如下所示：

|  |  |
| --- | --- |
| `teradata-input.sql` | ```       create table x(a timestamp);       select a from x where a > current_timestamp(0); ``` |
| `bq-output.sql` | ```       CREATE TABLE x       (         a TIMESTAMP       )       ;       SELECT           x.a         FROM           test.x         WHERE x.a > datetime_trunc(current_datetime('Europe/Paris'), SECOND)       ; ``` |

### Select 语句修改

**预览版**

此产品或功能 受[服务专用条款](https://docs.cloud.google.com/terms/service-terms?hl=zh-cn#1)的约束。
非正式版产品和功能“按原样”提供，可能只能获得有限的支持。
如需了解详情，请参阅[发布阶段说明](https://cloud.google.com/products/?hl=zh-cn#product-launch-stages)。

下面的配置 YAML 会更改 `SELECT` 语句中的 starProjection、`GROUP BY` 和 `ORDER BY` 子句。

`starProjection` 支持以下配置：

* `ALLOW`
* `PRESERVE`（默认）
* `EXPAND`

`groupBy` 和 `orderBy` 支持以下配置：

* `EXPRESSION`
* `ALIAS`
* `INDEX`

在下面的示例中，配置 YAML 将 starProjection 配置为 `EXPAND`。

```
type: experimental_statement_rewriter
select:
  starProjection: EXPAND
```

具有此配置 YAML 文件的 SQL 转译可能如下所示：

|  |  |
| --- | --- |
| `teradata-input.sql` | ```       create table x(a int, b TIMESTAMP);       select * from x; ``` |
| `bq-output.sql` | ```       CREATE TABLE x       (         a INT64,         b DATETIME       )       ;       SELECT           x.a           x.b         FROM           x       ; ``` |

### UDF 规范

下面的配置 YAML 指定在源脚本中使用的用户定义的函数 (UDF) 的签名。与[元数据 zip 文件](https://docs.cloud.google.com/bigquery/docs/generate-metadata?hl=zh-cn)非常相似，UDF 定义有助于生成输入脚本的更准确的转换。

```
type: metadata
udfs:
  - "date parse_short_date(dt int)"
```

具有此配置 YAML 文件的 SQL 转译可能如下所示：

|  |  |
| --- | --- |
| `teradata-input.sql` | ```       create table x(dt int);       select parse_short_date(dt) + 1 from x; ``` |
| `bq-output.sql` | ```       CREATE TABLE x       (         dt INT64       )       ;       SELECT           date_add(parse_short_date(x.dt), interval 1 DAY)         FROM           x       ; ``` |

### 设置小数精度严格程度

**预览版**

此产品或功能 受[服务专用条款](https://docs.cloud.google.com/terms/service-terms?hl=zh-cn#1)的约束。
非正式版产品和功能“按原样”提供，可能只能获得有限的支持。
如需了解详情，请参阅[发布阶段说明](https://cloud.google.com/products/?hl=zh-cn#product-launch-stages)。

默认情况下，BigQuery Migration Service 会将数字精度提高到给定小数位数的最高精度。下面的配置 YAML 通过配置精度严格程度来保留源语句的小数精度，从而替换此行为。

```
type: experimental_statement_rewriter
common:
  decimalPrecision: STRICT
```

具有此配置 YAML 文件的 SQL 转译可能如下所示：

|  |  |
| --- | --- |
| `teradata-input.sql` | ```       create table x(a decimal(3,0)); ``` |
| `bq-output.sql` | ```       CREATE TABLE x       (         a NUMERIC(3)       )       ; ``` |

### 设置字符串精度严格程度

**预览版**

此产品或功能 受[服务专用条款](https://docs.cloud.google.com/terms/service-terms?hl=zh-cn#1)的约束。
非正式版产品和功能“按原样”提供，可能只能获得有限的支持。
如需了解详情，请参阅[发布阶段说明](https://cloud.google.com/products/?hl=zh-cn#product-launch-stages)。

默认情况下，BigQuery Migration Service 在转换 `CHAR` 和 `VARCHAR` 列时会省略字符串精度。这有助于防止在写入值时出现截断错误。某些 SQL 方言（例如 Teradata）会在写入时截断超出最大精度的值，而 BigQuery 在这种情况下会返回错误。

如果您的应用不依赖于源方言的截断行为，请考虑在转换后的类型定义中保留列的精度。

下面的配置 YAML 通过配置精度严格程度来保留源语句的字符串精度，从而替换此行为。

```
type: experimental_statement_rewriter
common:
  stringPrecision: STRICT
```

具有此配置 YAML 文件的 SQL 转译可能如下所示：

|  |  |
| --- | --- |
| `teradata-input.sql` | ```       create table x(a varchar(3)); ``` |
| `bq-output.sql` | ```       CREATE TABLE x       (         a STRING(3)       )       ; ``` |

### 输出名称映射

**预览版**

此产品或功能 受[服务专用条款](https://docs.cloud.google.com/terms/service-terms?hl=zh-cn#1)的约束。
非正式版产品和功能“按原样”提供，可能只能获得有限的支持。
如需了解详情，请参阅[发布阶段说明](https://cloud.google.com/products/?hl=zh-cn#product-launch-stages)。

您可以使用配置 YAML 来映射 SQL 对象名称。您可以根据要映射的对象更改名称的不同部分。

#### 静态名称映射

使用静态名称映射来映射实体的名称。如果您只想更改名称的特定部分，并让名称的其他部分保持不变，请仅包含需要更改的部分。

下面的配置 YAML 会将表的名称从 `my_db.my_schema.my_table` 更改为 `my_new_db.my_schema.my_new_table`。

```
type: experimental_object_rewriter
relation:
-
  match: "my_db.my_schema.my_table"
  outputName:
    database: "my_new_db"
    relation: "my_new_table"
```

具有此配置 YAML 文件的 SQL 转译可能如下所示：

|  |  |
| --- | --- |
| `teradata-input.sql` | ```       create table my_db.my_schema.my_table(a int); ``` |
| `bq-output.sql` | ```       CREATE TABLE my_new_db.my_schema.my_new_table       (         a INT64       ) ``` |

您可以使用静态名称映射来更新[公开用户自定义函数](https://github.com/GoogleCloudPlatform/bigquery-utils/tree/master/udfs)中名称所使用的区域。

以下示例将 `bqutil.fn` UDF 中的名称从使用默认的 `us` 多区域更改为使用 `europe_west2` 区域：

```
type: experimental_object_rewriter
function:
-
  match:
    database: bqutil
    schema: fn
  outputName:
    database: bqutil
    schema: fn_europe_west2
```

#### 动态名称映射

使用动态名称映射可同时更改多个对象，并根据映射的对象创建新名称。

下面的配置 YAML 通过向属于 `staging` 架构的表添加前缀 `stg_` 来更改所有表的名称，然后将这些表移动到 `production` 架构。

```
type: experimental_object_rewriter
relation:
-
  match:
    schema: staging
  outputName:
    schema: production
    relation: "stg_${relation}"
```

具有此配置 YAML 文件的 SQL 转译可能如下所示：

|  |  |
| --- | --- |
| `teradata-input.sql` | ```       create table staging.my_table(a int); ``` |
| `bq-output.sql` | ```       CREATE TABLE production.stg_my_table       (         a INT64       )       ; ``` |

### 指定默认数据库和架构搜索路径

**预览版**

此产品或功能 受[服务专用条款](https://docs.cloud.google.com/terms/service-terms?hl=zh-cn#1)的约束。
非正式版产品和功能“按原样”提供，可能只能获得有限的支持。
如需了解详情，请参阅[发布阶段说明](https://cloud.google.com/products/?hl=zh-cn#product-launch-stages)。

下面的配置 YAML 指定[默认数据库](https://docs.cloud.google.com/bigquery/docs/output-name-mapping?hl=zh-cn#default_database)和[架构搜索路径](https://docs.cloud.google.com/bigquery/docs/output-name-mapping?hl=zh-cn#default_schema)。

```
type: environment
session:
  defaultDatabase: myproject
  schemaSearchPath: [myschema1, myschema2]
```

具有此配置 YAML 文件的 SQL 转译可能如下所示：

|  |  |
| --- | --- |
| `teradata-input.sql` | ```       SELECT * FROM database.table       SELECT * FROM table1 ``` |
| `bq-output.sql` | ```       SELECT * FROM myproject.database.table.       SELECT * FROM myproject.myschema1.table1 ``` |

### 全局输出名称重写

**预览版**

此产品或功能 受[服务专用条款](https://docs.cloud.google.com/terms/service-terms?hl=zh-cn#1)的约束。
非正式版产品和功能“按原样”提供，可能只能获得有限的支持。
如需了解详情，请参阅[发布阶段说明](https://cloud.google.com/products/?hl=zh-cn#product-launch-stages)。

下面的配置 YAML 会根据配置的规则更改脚本中所有对象（数据库、架构、关系和属性）的输出名称。

```
type: experimental_object_rewriter
global:
  outputName:
    regex:
      - match: '\s'
        replaceWith: '_'
      - match: '>='
        replaceWith: 'gte'
      - match: '^[^a-zA-Z_].*'
        replaceWith: '_$0'
```

具有此配置 YAML 文件的 SQL 转译可能如下所示：

|  |  |
| --- | --- |
| `teradata-input.sql` | ```       create table "test special chars >= 12"("42eid" int, "custom column" varchar(10)); ``` |
| `bq-output.sql` | ```       CREATE TABLE test_special_chars_employees_gte_12       (         _42eid INT64,         custom_column STRING       )       ; ``` |

### 优化和提升转换后的 SQL 的性能

可以将可选转换应用于转换后的 SQL，以引入更改，从而改善查询性能或节省查询费用。这些优化严格依赖于用例，应针对未经修改的 SQL 输出进行评估，以评估它们对性能的实际影响。

以下配置 YAML 会启用可选转换。该配置可接受优化列表，对于接受参数的优化，可以是包含可选参数值的部分。

```
type: optimizer
transformations:
  - name: PRECOMPUTE_INDEPENDENT_SUBSELECTS
  - name: REWRITE_CTE_TO_TEMP_TABLE
    parameters:
      threshold: 1
```

| 优化 | 可选参数 | 说明 |
| --- | --- | --- |
| `PRECOMPUTE_INDEPENDENT_SUBSELECTS` | `scope: [PREDICATE, PROJECTION]` | 通过添加 `DECLARE` 语句来重写查询，以用预先计算的变量替换 `PREDICATE` 语句或 `PROJECTION` 中的表达式。这将标识为静态谓词，以减少读取的数据量。如果省略范围，则默认值为 `PREDICATE`（即 `WHERE` 和 `JOIN-ON` 语句）。   将标量子查询提取到 `DECLARE` 语句，会使原始谓词变为静态，因此可以改进执行计划。此优化将引入新的 SQL 语句。 |
| `REWRITE_CTE_TO_TEMP_TABLE` | `threshold: N` | 如果对同一通用表表达式的引用超过 `N` 次，则将通用表表达式 (CTE) 重写为临时表。这可以降低查询复杂性，并强制执行一次常规表表达式。如果省略 `N`，则默认值为 4。   如果多次引用非常重要的 CTE，我们建议使用此优化。引入临时表的开销可能比最终多次执行低复杂度或低基数 CTE 的开销更大。此优化将引入新的 SQL 语句。 |
| `REWRITE_ZERO_SCALE_NUMERIC_AS_INTEGER` | `bigint: N` | 如果精度在 `N` 内，则将零比例 `NUMERIC/BIGNUMERIC` 属性重写为 `INT64` 类型。如果省略 `N`，则默认值为 `18`。   在从没有整数类型的源方言进行翻译时，建议使用此优化。若更改列类型，则需要检查类型兼容性和语义更改的所有下游用途。例如，分数除法变为整数除法，也就是需要数值的代码 |
| `DROP_TEMP_TABLE` |  | 为在脚本中创建的所有临时表添加 `DROP TABLE` 语句，并且在脚本结束时不丢弃。这会将临时表的存储结算周期从 24 小时缩短为脚本运行时间。此优化将引入新的 SQL 语句。    如果脚本执行结束后不会再访问临时表来进行任何进一步处理，我们建议使用此优化。此优化将引入新的 SQL 语句。 |
| `REGEXP_CONTAINS_TO_LIKE` |  | 将某些类别的 `REGEXP_CONTAINS` 匹配模式重写为 `LIKE` 表达式。   如果没有其他过程（例如宏替换）依赖于输出 SQL 中保持不变的正则表达式模式字面量时，我们建议使用此优化。 |
| `ADD_DISTINCT_TO_SUBQUERY_IN_SET_COMPARISON` |  | 向用作 `[NOT] IN` 运算符值集的子查询添加 `DISTINCT` 语句。   如果子查询结果的基数（不重复值的数量）明显低于值的数量，我们建议使用此优化。如果不满足此前提条件，此转换可能会对性能产生负面影响。 |

## 创建基于 Gemini 的配置 YAML 文件

**注意：**转换服务可以调用 Gemini 模型，根据 AI 配置 YAML 文件为转换后的 SQL 查询生成建议。

如需生成 AI 输出，包含 SQL 转换输入的源目录必须包含配置 YAML 文件。

### 要求

用于 AI 输出的配置 YAML 文件的后缀必须为 `.ai_config.yaml`。例如 `rules_1.ai_config.yaml`。

### 支持的字段

您可以使用以下字段配置 AI 转换输出：

* `suggestion_type`（可选）：指定要生成的 AI 建议的类型。支持以下建议类型：
  + `QUERY_CUSTOMIZATION`（默认）：根据配置 YAML 文件中指定的转换规则为 SQL 代码生成 AI 建议。
  + `TRANSLATION_EXPLANATION`：生成包含转换后的 GoogleSQL 查询摘要以及源 SQL 查询与转换后的 GoogleSQL 查询之间的差异和不一致的文本。
* `rewrite_target`（可选）：如果您要将转换规则应用于输入 SQL，请指定 `SOURCE_SQL`；如果您要将转换规则应用于输出 SQL，请指定 `TARGET_SQL`（默认）。
* `instruction`（可选）：用自然语言描述对目标 SQL 所做的更改。Gemini 增强型 SQL 转换会评估请求并进行指定的更改。
* `examples`（可选）：提供 SQL 示例，说明您希望如何修改 SQL 模式。

您可以根据需要添加其他 `translation_rules` 和其他 `examples`。

### 示例

以下示例创建基于 Gemini 的配置 YAML 文件，您可以将其与 SQL 转换搭配使用。

#### 移除默认转换输出查询中的 upper 函数

```
translation_rules:
- instruction: "Remove upper() function"
  examples:
  - input: "upper(X)"
    output: "X"
```

#### 创建多个转换规则以自定义转换输出

```
translation_rules:
- instruction: "Remove upper() function"
  suggestion_type: QUERY_CUSTOMIZATION
  rewrite_target: TARGET_SQL
  examples:
  - input: "upper(X)"
    output: "X"
- instruction: "Insert a comment at the head that explains each statement in detail.
  suggestion_type: QUERY_CUSTOMIZATION
  rewrite_target: TARGET_SQL
```

#### 从转换输入查询中移除 SQL 注释

```
translation_rules:
- instruction: "Remove all the sql comments in the input sql query."
  suggestion_type: QUERY_CUSTOMIZATION
  rewrite_target: SOURCE_SQL
```

#### 使用默认 LLM 提示生成转换说明

以下示例使用转换服务提供的默认 LLM 提示来生成文本说明：

```
translation_rules:
- suggestion_type: "TRANSLATION_EXPLANATION"
```

#### 使用您自己的自然语言提示生成转换说明

```
translation_rules:
- suggestion_type: "TRANSLATION_EXPLANATION"
  instruction: "Explain the syntax differences between the source Teradata query and the translated GoogleSQL query."
```

#### 单个配置 YAML 文件中的多种建议类型

```
translation_rules:
- suggestion_type: "TRANSLATION_EXPLANATION"
  instruction: "Explain the syntax differences between the source Teradata query and the translated GoogleSQL query."
- instruction: "Remove upper() function"
  suggestion_type: QUERY_CUSTOMIZATION
  rewrite_target: TARGET_SQL
  examples:
  - input: "upper(X)"
    output: "X"
- instruction: "Remove all the sql comments in the input sql query."
  suggestion_type: QUERY_CUSTOMIZATION
  rewrite_target: SOURCE_SQL
```

## 应用多个 YAML 配置

在批量或交互式 SQL 转译中指定配置 YAML 文件时，您可以在单个转译作业中选择多个配置 YAML 文件以反映多个转换。如果多个配置发生冲突，一个转换可能会替换另一个配置。建议在每个文件中使用不同类型的配置设置，以免同一转译作业中的转换发生冲突。

以下示例列出了为单个 SQL 转译作业提供的两个单独配置 YAML 文件，一个用于更改列的属性，另一个用于将表设置为临时表：

`change-type-example.config.yaml`：

```
type: object_rewriter
attribute:
  -
    match: "testdb.testschema.x.a"
    type:
      target: NUMERIC(10,2)
```

`make-temp-example.config.yaml`：

```
type: object_rewriter
relation:
  -
    match: "testdb.testschema.x"
    temporary: true
```

具有这两个配置 YAML 文件的 SQL 转译可能如下所示：

|  |  |
| --- | --- |
| `teradata-input.sql` | ```     create table x(a int); ``` |
| `bq-output.sql` | ```     CREATE TEMPORARY TABLE x     (       a NUMERIC(31, 2)     )     ; ``` |




发送反馈

如未另行说明，那么本页面中的内容已根据[知识共享署名 4.0 许可](https://creativecommons.org/licenses/by/4.0/)获得了许可，并且代码示例已根据 [Apache 2.0 许可](https://www.apache.org/licenses/LICENSE-2.0)获得了许可。有关详情，请参阅 [Google 开发者网站政策](https://developers.google.com/site-policies?hl=zh-cn)。Java 是 Oracle 和/或其关联公司的注册商标。

最后更新时间 (UTC)：2026-02-12。




需要向我们提供更多信息？

[[["易于理解","easyToUnderstand","thumb-up"],["解决了我的问题","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["很难理解","hardToUnderstand","thumb-down"],["信息或示例代码不正确","incorrectInformationOrSampleCode","thumb-down"],["没有我需要的信息/示例","missingTheInformationSamplesINeed","thumb-down"],["翻译问题","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["最后更新时间 (UTC)：2026-02-12。"],[],[]]