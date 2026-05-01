* [Home](https://docs.cloud.google.com/?hl=zh-cn)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-cn)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-cn)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-cn)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-cn)

发送反馈



使用集合让一切井井有条

根据您的偏好保存内容并对其进行分类。

# 映射 SQL 对象名称以进行批量转换

**预览版**

此产品 受[服务专用条款](https://docs.cloud.google.com/terms/service-terms?hl=zh-cn#1)的约束。 非正式版产品“按原样”提供，且可能仅提供有限支持。
如需了解详情，请参阅[发布阶段说明](https://cloud.google.com/products/?hl=zh-cn#product-launch-stages)。

**注意：**只有旧版批量 API 支持使用 JSON 进行对象名称映射。如果您使用的是 [BigQuery Migration API](https://docs.cloud.google.com/bigquery/docs/api-sql-translator?hl=zh-cn) 或从 Google Cloud 控制台启动批量作业，请改用[基于 YAML 的对象名称映射](https://docs.cloud.google.com/bigquery/docs/config-yaml-translation?hl=zh-cn#output_name_mapping)。

本文档介绍如何配置*名称映射*，以在[批量转换](https://docs.cloud.google.com/bigquery/docs/batch-sql-translator?hl=zh-cn)期间重命名 SQL 对象。

## 概览

通过名称映射，您可以标识源文件中 SQL 对象的名称，并在 BigQuery 中为这些对象指定目标名称。您可以使用以下部分或全部组件来配置对象的名称映射：

* 名称映射规则，由以下部分构成：
  + 来源[名称部分](#name_parts)，提供源系统中对象的完全限定名称。
  + [类型](#object_types)，用于标识源对象的类型。
  + 目标名称部分，提供 BigQuery 中对象的名称。
* [默认数据库](#default_database)名称，提供给任何未指定数据库的源对象使用。
* [默认架构](#default_schema)名称，提供给任何未指定架构的源对象使用。

### 名称部分

您可以组合使用以下名称部分，在名称映射规则中提供源和目标对象名称的值：

* **数据库**：命名层次结构的顶层。您的源平台可能使用其他术语，例如*项目*。
* **架构**：命名层次结构的第二级。您的源平台可能使用其他术语，例如*数据集*。
* **关系**：命名层次结构的第三级。您的源平台可能使用其他术语，例如*表*。
* **特性**：命名层次结构的最低级层。您的源平台可能使用其他术语，例如*列*。

### 对象类型

您还必须在名称映射规则中指定要重命名的源对象的类型。支持以下对象类型：

* `Database`：对象层次结构中的顶层对象，例如 **`database`**`.schema.relation.attribute`。您的源平台可能使用其他术语，例如*项目*。将 `database` 指定为对象类型会更改 DDL 和 DML 语句中对源字符串的所有引用。
* `Schema`：对象层次结构中的第二级对象。您的源平台可能使用其他术语，例如*数据集*。将 `schema` 指定为对象类型会更改 DDL 和 DML 语句中对源字符串的所有引用。
* `Relation`：对象层次结构中的第三级对象。您的源平台可能使用其他术语，例如*表*。将 `relation` 指定为对象类型会更改 DDL 语句中对源字符串的所有引用。
* `Relation alias`：第三级对象的别名。例如，在查询 `SELECT t.field1, t.field2 FROM myTable t;` 中，`t` 是关系别名。在查询 `SELECT field1, field2 FROM schema1.table1` 中，`table1` 也是关系别名。将 `relation alias` 指定为对象类型会为 DML 语句中对源字符串的所有引用创建别名。例如，如果将 `tableA` 指定为目标名称，则上述示例将分别转换为 `SELECT tableA.field1, tableA.field2 FROM myTable AS tableA;` 和 `SELECT tableA.field1, tableA.field2 FROM schema1.table1 AS tableA`。
* `Function`：过程，例如 `create procedure db.test.function1(a int)`。将 `function` 指定为对象类型会更改 DDL 和 DML 语句中对源字符串的所有引用。
* `Attribute`：对象层次结构中的第四级对象。您的源平台可能使用其他术语，例如*列*。将 `attribute` 指定为对象类型会更改 DDL 语句中对源字符串的所有引用。
* `Attribute alias`：第四级对象的别名。例如，在查询 `SELECT field1 FROM myTable;` 中，`field1` 是特性别名。将 `attribute alias` 指定为对象类型会更改 DML 语句中对源字符串的所有引用。

#### 对象类型所需的名称部分

如需在名称映射规则中描述对象，请使用下表中为每个对象类型标识的名称部分：

| **类型** | **源对象名称** | | | | **目标对象名称** | | | |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  | **数据库名称部分** | **架构名称部分** | **关系名称部分** | **特性名称部分** | **数据库名称部分** | **架构名称部分** | **关系名称部分** | **特性名称部分** |
| `Database` | X |  |  |  | X |  |  |  |
| `Schema` | X | X |  |  | X | X |  |  |
| `Relation` | X | X | X |  | X | X | X |  |
| `Function` | X | X | X |  | X | X | X |  |
| `Attribute` | X | X | X | X |  |  |  | X |
| `Attribute alias` | X | X | X | X |  |  |  | X |
| `Relation alias` |  |  | X |  |  |  | X |  |

### 默认数据库

如果您要将 BigQuery 项目名称附加到所有已转换的对象，最简单的方法是在[创建转换作业](https://docs.cloud.google.com/bigquery/docs/batch-sql-translator?hl=zh-cn#submit_a_translation_job)时指定一个默认的数据库名称。这适用于使用三部分命名或者使用四部分命名但未指定最高级层对象名称的源文件。

例如，如果您指定默认数据库名称 `myproject`，则 `SELECT * FROM database.table` 等源语句将转换为 `SELECT * FROM myproject.database.table`。如果您的对象已使用数据库名称部分（如 `SELECT * FROM database.schema.table`），则您必须使用名称映射规则才能将 `database.schema.table` 重命名为 `myproject.schema.table`。

### 默认架构

如果要完全限定源文件中未使用四部分命名的所有对象名称，您可以在[创建转换作业](https://docs.cloud.google.com/bigquery/docs/batch-sql-translator?hl=zh-cn#submit_a_translation_job)时同时提供[默认数据库名称](#default_database)和默认架构名称。
默认架构名称作为架构搜索路径选项中的第一个架构名称提供。

例如，如果您指定默认数据库名称 `myproject` 和默认架构名称 `myschema`，则以下源语句：

* `SELECT * FROM database.table`
* `SELECT * FROM table1`

会转换为：

* `SELECT * FROM myproject.database.table`。
* `SELECT * FROM myproject.myschema.table1`

## 名称映射规则行为

以下部分介绍名称映射规则的行为。

### 规则继承会沿着对象层次结构向下传递

影响较高级层对象的名称更改会影响目标对象，及其同一层次结构中的所有子对象。

例如，如果您使用对象类型 `schema` 指定以下名称映射规则：

| **名称部分** | **来源** | **目标** |
| --- | --- | --- |
| 数据库 | `sales_db` | `sales` |
| 架构 | `cust_mgmt` | `cms` |
| 关系 |  |  |
| 属性 |  |  |

应用完成后，`sales_db.cust_mgmt` 架构下的所有 `relation` 和 `attribute` 对象的数据库和架构名称部分也会更改。例如，名为 `sales_db.cust_mgmt.history` 的 `relation` 对象会更改为 `sales.cms.history`。

相反，对较低级层对象进行的名称更改不会影响对象层次结构中处于较高级层或相同级层的对象。

例如，如果您使用对象类型 `relation` 指定以下名称映射规则：

| **名称部分** | **来源** | **目标** |
| --- | --- | --- |
| 数据库 | `sales_db` | `sales` |
| 架构 | `cust_mgmt` | `cms` |
| 关系 | `clients` | `accounts` |
| 属性 |  |  |

应用完成后，处于对象层次结构 `sales_db` 或 `sales_db.cust_mgmt` 级层的其他对象均不会发生更改。

### 应用最具体的规则

一个对象只会应用一个名称映射规则。如果一个对象可能会受到多个规则的影响，那么系统会应用影响最低级层名称部分的规则。例如，如果 `database` 类型名称映射规则和 `schema` 类型名称映射规则可能都会影响 `relation` 对象的名称，那么系统会应用 `schema` 类型名称映射规则。

### 使用唯一的类型和来源值组合

您不能指定多个具有相同类型和来源值的名称映射规则。例如，您不能同时指定以下两个名称映射规则：

|  | **规则 1，类型 `attribute`** | | **规则 2，类型 `attribute`** | |
| --- | --- | --- | --- | --- |
| **名称部分** | **来源** | **目标** | **来源** | **目标** |
| 数据库 | `project` |  | `project` |  |
| 架构 | `dataset1` |  | `dataset1` |  |
| 关系 | `table1` |  | `table1` |  |
| 属性 | `lname` | `last_name` | `lname` | `lastname` |

### 创建匹配的 `attribute` 和 `attribute alias` 名称映射规则

使用 `attribute` 类型名称映射规则更改 DDL 语句中的特性名称时，您还必须创建 `attribute alias` 名称映射规则来更改 DML 语句中相应特性的名称。

### 名称更改不会级联

名称更改不会跨多个名称规则进行级联。例如，如果您创建了一个将 `database1` 重命名为 `project1` 的名称映射规则，以及另一个将 `project1` 重命名为 `project2` 的名称映射规则，那么转换器并不会将 `database1` 映射到 `project2`。

## 处理没有四部分名称的源对象

某些源系统（如 Teradata）使用三个名称部分来完全限定对象名称。许多源系统还允许您在其 SQL 方言中使用部分限定名称，例如使用 `database1.schema1.table1`、`schema1.table1` 和 `table1` 来引用不同上下文中的同一对象。如果源文件包含未使用四部分对象名称的对象，那么您可以在使用名称映射的同时指定[默认数据库名称](#default_database)和[默认架构名称](#default_schema)，以实现所需的名称映射。

如需查看在使用名称映射规则的同时指定默认数据库名称或默认架构名称的示例，请参阅[更改具有不同名称完整级别的对象的数据库名称部分](https://docs.cloud.google.com/bigquery/docs/output-name-mapping?hl=zh-cn#partial-database)和[更改部分限定的关系对象名称](https://docs.cloud.google.com/bigquery/docs/output-name-mapping?hl=zh-cn#partial-relation)。

## 名称映射示例

通过本部分中的示例了解名称映射规则在常见用例中的工作原理。

### 更改完全限定对象的数据库名称部分

以下示例会为具有完全限定名称的所有 `database`、`schema`、`relation` 和 `function` 对象将数据库名称部分由 `td_project` 重命名为 `bq_project`。

**源和目标名称部分**

| **名称部分** | **来源** | **目标** |
| --- | --- | --- |
| 数据库 | `td_project` | `bq_project` |
| 架构 |  |  |
| 关系 |  |  |
| 属性 |  |  |

**类型**

* `database`

**输入示例**

* `SELECT * FROM td_project.schema.table;`
* `SELECT * FROM td_project.schema1.table1;`

**输出示例**

* `SELECT * FROM bq_project.schema.table;`
* `SELECT * FROM bq_project.schema1.table1`

### 更改具有不同名称完整级别的对象的数据库名称部分

在以下示例中，所有对象类型的数据库名称部分都会由 `project` 重命名为 `bq_project`，并且系统会为未指定数据库名称部分的对象添加 `bq_project` 作为其数据库名称部分。

为此，除了指定名称映射规则外，您还必须在配置转换作业时指定默认数据库值。如需详细了解如何指定默认数据库名称，请参阅[提交转换作业](https://docs.cloud.google.com/bigquery/docs/batch-sql-translator?hl=zh-cn#submit_a_translation_job)。

**默认数据库值**

* `project`

**源和目标名称部分**

| **名称部分** | **来源** | **目标** |
| --- | --- | --- |
| 数据库 | `project` | `bq_project` |
| 架构 |  |  |
| 关系 |  |  |
| 属性 |  |  |

**类型**

* `database`

**输入示例**

* `SELECT * FROM project.schema.table;`
* `SELECT * FROM schema1.table1;`

**输出示例**

* `SELECT * FROM bq_project.schema.table;`
* `SELECT * FROM bq_project.schema1.table1`

### 更改完全限定对象的数据库名称部分和架构名称部分

以下示例会将数据库名称部分 `warehouse1` 更改为 `myproject`，并将架构名称部分 `database1` 更改为 `mydataset`。

您还可以使用相同的方式更改 `relation` 对象名称的各个部分，使用 `relation` 类型并为关系名称部分指定源值和目标值。

**源和目标名称部分**

| **名称部分** | **来源** | **目标** |
| --- | --- | --- |
| 数据库 | `warehouse1` | `myproject` |
| 架构 | `database1` | `mydataset` |
| 关系 |  |  |
| 属性 |  |  |

**类型**

* `schema`

**输入示例**

* `SELECT * FROM warehouse1.database1.table1;`
* `SELECT * FROM database2.table2;`

**输出示例**

* `SELECT * FROM myproject.mydataset.table1;`
* `SELECT * FROM __DEFAULT_DATABASE__.database2.table2;`

### 更改完全限定的 `relation` 对象名称

以下示例会将 `mydb.myschema.mytable` 重命名为 `mydb.myschema.table1`。

**源和目标名称部分**

| **名称部分** | **来源** | **目标** |
| --- | --- | --- |
| 数据库 | `mydb` | `mydb` |
| 架构 | `myschema` | `myschema` |
| 关系 | `mytable` | `table1` |
| 属性 |  |  |

**类型**

* `relation`

**输入示例**

* `CREATE table mydb.myschema.mytable(id int, name varchar(64));`

**输出示例**

* `CREATE table mydb.myschema.table1(id integer, name string(64));`

### 更改部分限定的 `relation` 对象名称

以下示例会将 `myschema.mytable` 重命名为 `mydb.myschema.table1`。

**默认数据库值**

* `mydb`

**源和目标名称部分**

| **名称部分** | **来源** | **目标** |
| --- | --- | --- |
| 数据库 | `mydb` | `mydb` |
| 架构 | `myschema` | `myschema` |
| 关系 | `mytable` | `table1` |
| 属性 |  |  |

**类型**

* `relation`

**输入示例**

* `CREATE table myschema.mytable(id int, name varchar(64));`

**输出示例**

* `CREATE table mydb.myschema.table1(id integer, name string(64));`

### 更改 `relation alias` 对象名称

以下示例会将 `relation alias` 对象 `table` 的所有实例重命名为 `t`。

**源和目标名称部分**

| **名称部分** | **来源** | **目标** |
| --- | --- | --- |
| 数据库 |  |  |
| 架构 |  |  |
| 关系 | `table` | `t` |
| 属性 |  |  |

**类型**

* `relation alias`

**输入示例**

* `SELECT table.id, table.name FROM mydb.myschema.mytable table`

**输出示例**

* `SELECT t.id, t.name FROM mydb.myschema.mytable AS t`

### 更改 `function` 对象名称

以下示例会将 `mydb.myschema.myfunction` 重命名为 `mydb.myschema.function1`。

**源和目标名称部分**

| **名称部分** | **来源** | **目标** |
| --- | --- | --- |
| 数据库 | `mydb` | `mydb` |
| 架构 | `myschema` | `myschema` |
| 关系 | `myprocedure` | `procedure1` |
| 属性 |  |  |

**类型**

* `function`

**输入示例**

* `CREATE PROCEDURE mydb.myschema.myprocedure(a int) BEGIN declare i int; SET i = a + 1; END;`
* `CALL mydb.myschema.myprocedure(7)`

**输出示例**

* `CREATE PROCEDURE mydb.myschema.procedure1(a int) BEGIN declare i int; SET i = a + 1; END;`
* `CALL mydb.myschema.procedure1(7);`

### 更改 `attribute` 对象名称

以下示例会将 `mydb.myschema.mytable.myfield` 重命名为 `mydb.myschema.mytable.field1`。由于 `attribute` 对象位于对象层次结构的最低级层，因此该名称映射不会更改任何其他对象的名称。

**源和目标名称部分**

| **名称部分** | **来源** | **目标** |
| --- | --- | --- |
| 数据库 | `mydb` |  |
| 架构 | `myschema` |  |
| 关系 | `mytable` |  |
| 属性 | `myfield` | `field1` |

**类型**

* `attribute`

**输入示例**

* `CREATE table mydb.myschema.mytable(myfield int, name varchar(64), revenue int);`

**输出示例**

* `CREATE table mydb.myschema.mytable(field1 int, name varchar(64), revenue int);`

### 更改 `attribute alias` 对象名称

以下示例会将 `mydb.myschema.mytable.myfield` 重命名为 `mydb.myschema.mytable.field1`。由于 `attribute alias` 对象位于对象层次结构的最低级层，因此该名称映射不会更改任何其他对象的名称。

**源和目标名称部分**

| **名称部分** | **来源** | **目标** |
| --- | --- | --- |
| 数据库 | `mydb` |  |
| 架构 | `myschema` |  |
| 关系 | `mytable` |  |
| 属性 | `myfield` | `field1` |

**类型**

* `attribute alias`

**输入示例**

* `SELECT myfield, name FROM mydb.myschema.mytable;`

**输出示例**

* `SELECT field1, name FROM mydb.myschema.mytable;`

## JSON 文件格式

如果您选择使用 JSON 文件（而不是使用 Google Cloud 控制台）指定名称映射规则，那么该 JSON 文件必须遵循以下格式：

```
{
  "name_map": [
    {
      "source": {
        "type": "string",
        "database": "string",
        "schema": "string",
        "relation": "string",
        "attribute": "string"
      },
      "target": {
        "database": "string",
        "schema": "string",
        "relation": "string",
        "attribute": "string"
      }
    }
  ]
}
```

该文件必须小于 5 MB。

如需详细了解如何为转换作业指定名称映射规则，请参阅[提交转换作业](https://docs.cloud.google.com/bigquery/docs/batch-sql-translator?hl=zh-cn#submit_a_translation_job)。

### JSON 示例

以下示例展示了如何使用 JSON 文件指定名称映射规则。

#### 示例 1

此示例中的名称映射规则会进行如下对象名称更改：

* 将 `project.dataset2.table2` `relation` 对象的实例重命名为 `bq_project.bq_dataset2.bq_table2`。
* 将 `project` `database` 对象的所有实例重命名为 `bq_project`。例如，`project.mydataset.table2` 将更改为 `bq_project.mydataset.table2`，`CREATE DATASET project.mydataset` 将更改为 `CREATE DATASET bq_project.mydataset`。

```
{
  "name_map": [{
    "source": {
      "type": "RELATION",
      "database": "project",
      "schema": "dataset2",
      "relation": "table2"
    },
    "target": {
      "database": "bq_project",
      "schema": "bq_dataset2",
      "relation": "bq_table2"
    }
  }, {
    "source": {
      "type": "DATABASE",
      "database": "project"
    },
    "target": {
      "database": "bq_project"
    }
  }]
}
```

#### 示例 2

此示例中的名称映射规则会进行如下对象名称更改：

* 在 DDL 和 DML 语句中将 `project.dataset2.table2.field1` `attribute` 对象的实例重命名为 `bq_project.bq_dataset2.bq_table2.bq_field`。

```
{
  "name_map": [{
    "source": {
      "type": "ATTRIBUTE",
      "database": "project",
      "schema": "dataset2",
      "relation": "table2",
      "attribute": "field1"
    },
    "target": {
      "database": "bq_project",
      "schema": "bq_dataset2",
      "relation": "bq_table2",
      "attribute": "bq_field"
    }
  }, {
    "source": {
      "type": "ATTRIBUTE_ALIAS",
      "database": "project",
      "schema": "dataset2",
      "relation": "table2",
      "attribute": "field1"
    },
    "target": {
      "database": "bq_project",
      "schema": "bq_dataset2",
      "relation": "bq_table2",
      "attribute": "bq_field"
    }
  }]
}
```




发送反馈

如未另行说明，那么本页面中的内容已根据[知识共享署名 4.0 许可](https://creativecommons.org/licenses/by/4.0/)获得了许可，并且代码示例已根据 [Apache 2.0 许可](https://www.apache.org/licenses/LICENSE-2.0)获得了许可。有关详情，请参阅 [Google 开发者网站政策](https://developers.google.com/site-policies?hl=zh-cn)。Java 是 Oracle 和/或其关联公司的注册商标。

最后更新时间 (UTC)：2026-03-18。




需要向我们提供更多信息？

[[["易于理解","easyToUnderstand","thumb-up"],["解决了我的问题","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["很难理解","hardToUnderstand","thumb-down"],["信息或示例代码不正确","incorrectInformationOrSampleCode","thumb-down"],["没有我需要的信息/示例","missingTheInformationSamplesINeed","thumb-down"],["翻译问题","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["最后更新时间 (UTC)：2026-03-18。"],[],[]]