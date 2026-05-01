* [Home](https://docs.cloud.google.com/?hl=zh-cn)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-cn)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-cn)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-cn)
* [参考文档](https://docs.cloud.google.com/bigquery/quotas?hl=zh-cn)

发送反馈



使用集合让一切井井有条

根据您的偏好保存内容并对其进行分类。

# OBJECT\_PRIVILEGES 视图

**预览版**

此产品或功能 受[服务专用条款](https://docs.cloud.google.com/terms/service-terms?hl=zh-cn#1)的约束。
非正式版产品和功能“按原样”提供，可能只能获得有限的支持。
如需了解详情，请参阅[发布阶段说明](https://cloud.google.com/products/?hl=zh-cn#product-launch-stages)。

`INFORMATION_SCHEMA.OBJECT_PRIVILEGES` 视图包含有关在 BigQuery 对象上明确设置的访问权限控制绑定的元数据。此视图不包含有关继承的访问权限控制绑定的元数据。

## 所需权限

要查询 `INFORMATION_SCHEMA.OBJECT_PRIVILEGES` 视图，您需要以下 Identity and Access Management (IAM) 权限：

* `bigquery.datasets.get`（数据集）。
* `bigquery.tables.getIamPolicy`（表和视图）。

如需详细了解 BigQuery 权限，请参阅[使用 IAM 进行访问权限控制](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-cn)。

## 架构

当您查询 `INFORMATION_SCHEMA.OBJECT_PRIVILEGES` 视图时，查询结果会针对资源的每个访问权限控制绑定返回一行。

`INFORMATION_SCHEMA.OBJECT_PRIVILEGES` 视图具有如下架构：

| 列名 | 数据类型 | 值 |
| --- | --- | --- |
| `object_catalog` | `STRING` | 包含资源的项目的项目 ID。 |
| `object_schema` | `STRING` | 包含资源的数据集的名称。如果资源本身是数据集，则为 `NULL`。 |
| `object_name` | `STRING` | 政策应用于的表、视图或数据集的名称。 |
| `object_type` | `STRING` | 资源类型，例如 `SCHEMA`（数据集）、`TABLE`、`VIEW` 和 `EXTERNAL`。 |
| `privilege_type` | `STRING` | 角色 ID，例如 `roles/bigquery.dataEditor`。 |
| `grantee` | `STRING` | 被授予角色的用户类型和用户。 |

为了确保稳定性，我们建议您在信息架构查询中明确列出列，而不是使用通配符 (`SELECT *`)。明确列出列可防止底层架构发生更改时查询中断。

## 范围和语法

针对此视图的查询必须包含[区域限定符](https://docs.cloud.google.com/bigquery/docs/information-schema-intro?hl=zh-cn#syntax)。项目 ID 是可选的。如果未指定项目 ID，则使用运行查询的项目。下表说明了此视图的区域范围：

| 视图名称 | 资源范围 | 区域范围 |
| --- | --- | --- |
| `` [PROJECT_ID.]`region-REGION`.INFORMATION_SCHEMA.OBJECT_PRIVILEGES `` | 项目级 | `REGION` |

请替换以下内容：

* 可选：`PROJECT_ID`：您的 Google Cloud 项目的 ID。如果未指定，则使用默认项目。
* `REGION`：任何[数据集区域名称](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-cn)。
  例如 `` `region-us` ``。**注意：**您必须使用[区域限定符](https://docs.cloud.google.com/bigquery/docs/information-schema-intro?hl=zh-cn#region_qualifier)来查询 `INFORMATION_SCHEMA` 视图。查询执行的位置必须与 `INFORMATION_SCHEMA` 视图的区域相匹配。

**示例**

```
-- Returns metadata for the access control bindings for mydataset.
SELECT * FROM myproject.`region-us`.INFORMATION_SCHEMA.OBJECT_PRIVILEGES
WHERE object_name = "mydataset";
```

## 限制

* `OBJECT_PRIVILEGES` 查询必须包含 `WHERE` 子句，才能将查询限制为单个数据集、表或视图。
* 检索数据集的访问权限控制元数据的查询必须指定 `object_name`。
* 检索表或视图的访问权限控制元数据的查询必须指定 `object_name` 和 `object_schema`。

## 示例

以下示例从 `INFORMATION_SCHEMA.OBJECT_PRIVILEGES` 视图中检索所有列。

如需针对运行查询的项目以外的项目运行查询，请按以下格式将相应项目 ID 添加到区域中：`` `project_id`.`region_id`.INFORMATION_SCHEMA.OBJECT_PRIVILEGES ``。

以下示例获取 `mycompany` 项目中 `mydataset` 数据集的所有访问权限控制元数据：

```
SELECT *
FROM mycompany.`region-us`.INFORMATION_SCHEMA.OBJECT_PRIVILEGES
WHERE object_name = "mydataset"
```

结果应如下所示：

```
  +----------------+---------------+-------------+-------------+---------------------------+-----------------------------------+
  | object_catalog | object_schema | object_name | object_type |  privilege_type           | grantee                           |
  +----------------+---------------+-------------+-------------+---------------------------+-----------------------------------+
  | mycompany      | NULL          | mydataset   | SCHEMA      | roles/bigquery.dataEditor | projectEditor:mycompany           |
  +----------------+---------------+-------------+-------------+---------------------------+-----------------------------------+
  | mycompany      | NULL          | mydataset   | SCHEMA      | roles/bigquery.dataOwner  | projectOwner:mycompany            |
  +----------------+---------------+-------------+-------------+---------------------------+-----------------------------------+
  | mycompany      | NULL          | mydataset   | SCHEMA      | roles/bigquery.dataOwner  | user:cloudysanfrancisco@gmail.com |
  +----------------+---------------+-------------+-------------+---------------------------+-----------------------------------+
  | mycompany      | NULL          | mydataset   | SCHEMA      | roles/bigquery.dataViwer  | projectViewer:mycompany           |
  +----------------+---------------+-------------+-------------+---------------------------+-----------------------------------+
```

以下示例获取 `mydataset` 数据集中 `testdata` 表的所有访问权限控制信息：

```
SELECT *
FROM mycompany.`region-us`.INFORMATION_SCHEMA.OBJECT_PRIVILEGES
WHERE object_schema = "mydataset" AND object_name = "testdata"
```

结果应如下所示：

```
  +----------------+---------------+--------------+-------------+----------------------+------------------------------------+
  | object_catalog | object_schema |  object_name | object_type |  privilege_type      | grantee                            |
  +----------------+---------------+--------------+-------------+----------------------+------------------------------------+
  | mycompany      | mydataset     | testdata     | TABLE       | roles/bigquery.admin | user:baklavainthebalkans@gmail.com |
  +----------------+---------------+--------------+-------------+----------------------+------------------------------------+
```

`INFORMATION_SCHEMA.OBJECT_PRIVILEGES` 视图仅显示明确设置的访问权限控制绑定。第一个示例显示，用户 `cloudysanfrancisco@gmail.com` 拥有对 `mydataset` 数据集的 `bigquery.dataOwner` 角色。用户 `cloudysanfrancisco@gmail.com` 继承了在 `mydataset` 中创建、更新和删除表的权限，包括 `testdata` 表。不过，由于未明确针对 `testdata` 表授予这些权限，因此不会显示在第二个示例的结果中。




发送反馈

如未另行说明，那么本页面中的内容已根据[知识共享署名 4.0 许可](https://creativecommons.org/licenses/by/4.0/)获得了许可，并且代码示例已根据 [Apache 2.0 许可](https://www.apache.org/licenses/LICENSE-2.0)获得了许可。有关详情，请参阅 [Google 开发者网站政策](https://developers.google.com/site-policies?hl=zh-cn)。Java 是 Oracle 和/或其关联公司的注册商标。

最后更新时间 (UTC)：2026-03-18。




需要向我们提供更多信息？

[[["易于理解","easyToUnderstand","thumb-up"],["解决了我的问题","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["很难理解","hardToUnderstand","thumb-down"],["信息或示例代码不正确","incorrectInformationOrSampleCode","thumb-down"],["没有我需要的信息/示例","missingTheInformationSamplesINeed","thumb-down"],["翻译问题","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["最后更新时间 (UTC)：2026-03-18。"],[],[]]