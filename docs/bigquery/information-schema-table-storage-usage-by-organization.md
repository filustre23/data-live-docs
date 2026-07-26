* [Home](https://docs.cloud.google.com/?hl=zh-cn)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-cn)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-cn)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-cn)
* [参考文档](https://docs.cloud.google.com/bigquery/quotas?hl=zh-cn)

发送反馈



使用集合让一切井井有条

根据您的偏好保存内容并对其进行分类。

# TABLE\_STORAGE\_USAGE\_TIMELINE\_BY\_ORGANIZATION 视图

**预览版**

此产品或功能 受[服务专用条款](https://docs.cloud.google.com/terms/service-terms?hl=zh-cn#1)的约束。
非正式版产品和功能“按原样”提供，可能只能获得有限的支持。
如需了解详情，请参阅[发布阶段说明](https://cloud.google.com/products/?hl=zh-cn#product-launch-stages)。

`INFORMATION_SCHEMA.TABLE_STORAGE_USAGE_TIMELINE_BY_ORGANIZATION` 视图提供以下类型的表在过去 90 天内的每日总存储用量：

* 标准表
* 具体化视图
* 包含基表中字节增量的表克隆
* 包含基表中字节增量的表快照

没有计费字节数的表不包含在 `INFORMATION_SCHEMA.TABLE_STORAGE_USAGE_TIMELINE_BY_ORGANIZATION` 视图中。这包括以下类型的表格：

* 外部表
* 匿名表
* 空表
* 不包含基表中字节增量的表克隆
* 不包含基表中字节增量的表快照

查询 `INFORMATION_SCHEMA.TABLE_STORAGE_USAGE_TIMELINE_BY_ORGANIZATION` 视图时，查询结果包含每天与当前项目关联的整个组织的每个表或物化视图对应的一行。

此表中的数据并非实时提供。表数据大约需要 72 小时才能反映在此视图中。

存储用量以 MiB 秒为单位返回。例如，如果项目在 86,400 秒（24 小时）使用 1,000,000 个物理字节，则物理总用量为 86,400,000,000 字节秒，转换为 82,397 MiB 秒，如以下示例所示：

```
86,400,000,000 / 1,024 / 1,024 = 82,397
```

这是 `BILLABLE_TOTAL_PHYSICAL_USAGE` 列将返回的值。

如需了解详情，请参阅[存储价格详细信息](https://cloud.google.com/bigquery/pricing?hl=zh-cn#storage-pricing-details)。

**注意：**此视图的数据的开始日期为 2023 年 10 月 1 日。您可以查询该日期之前的视图，但返回的数据不完整。

## 所需权限

如需查询 `INFORMATION_SCHEMA.TABLE_STORAGE_USAGE_TIMELINE_BY_ORGANIZATION` 视图，您需要拥有您的组织的以下 Identity and Access Management (IAM) 权限：

* `bigquery.tables.get`
* `bigquery.tables.list`

以下每个预定义的 IAM 角色均可提供上述权限：

* `roles/bigquery.dataViewer`
* `roles/bigquery.dataEditor`
* `roles/bigquery.metadataViewer`
* `roles/bigquery.admin`

此架构视图仅可供已定义[Google Cloud组织](https://docs.cloud.google.com/resource-manager/docs/cloud-platform-resource-hierarchy?hl=zh-cn#organizations)的用户使用。

如需详细了解 BigQuery 权限，请参阅[使用 IAM 进行访问权限控制](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-cn)。

## 架构

`INFORMATION_SCHEMA.TABLE_STORAGE_USAGE_TIMELINE_BY_ORGANIZATION` 视图具有如下架构：

| 列名 | 数据类型 | 值 |
| --- | --- | --- |
| `usage_date` | `DATE` | 所显示字节的结算日期（使用 `America/Los_Angeles` 时区） |
| `project_id` | `STRING` | 该数据集所属项目的项目 ID |
| `table_catalog` | `STRING` | 该数据集所属项目的项目 ID |
| `project_number` | `INT64` | 该数据集所属项目的项目编号 |
| `table_schema` | `STRING` | 包含表或物化视图的数据集的名称，也称为 `datasetId` |
| `table_name` | `STRING` | 表或物化视图的名称，也称为 `tableId` |
| `billable_total_logical_usage` | `INT64` | 总逻辑用量（以 MiB 秒为单位）。  如果数据集使用物理存储[结算模式](https://docs.cloud.google.com/bigquery/docs/datasets-intro?hl=zh-cn#dataset_storage_billing_models)，则返回 0。 |
| `billable_active_logical_usage` | `INT64` | 存在时间少于 90 天的逻辑用量（以 MiB 秒为单位）。  如果数据集使用物理存储[结算模式](https://docs.cloud.google.com/bigquery/docs/datasets-intro?hl=zh-cn#dataset_storage_billing_models)，则返回 0。 |
| `billable_long_term_logical_usage` | `INT64` | 存在时间超过 90 天的逻辑用量（以 MiB 秒为单位）。  如果数据集使用物理存储[结算模式](https://docs.cloud.google.com/bigquery/docs/datasets-intro?hl=zh-cn#dataset_storage_billing_models)，则返回 0。 |
| `billable_total_physical_usage` | `INT64` | 总用量（以 MiB 秒为单位）。这包括用于故障安全和[时间旅行](https://docs.cloud.google.com/bigquery/docs/time-travel?hl=zh-cn)存储的物理字节数。  如果数据集使用逻辑存储[结算模式](https://docs.cloud.google.com/bigquery/docs/datasets-intro?hl=zh-cn#dataset_storage_billing_models)，则返回 0。 |
| `billable_active_physical_usage` | `INT64` | 存在时间少于 90 天的物理用量（以 MiB 秒为单位）。这包括用于故障安全和[时间旅行](https://docs.cloud.google.com/bigquery/docs/time-travel?hl=zh-cn)存储的物理字节数。  如果数据集使用逻辑存储[结算模式](https://docs.cloud.google.com/bigquery/docs/datasets-intro?hl=zh-cn#dataset_storage_billing_models)，则返回 0。 |
| `billable_long_term_physical_usage` | `INT64` | 存在时间超过 90 天的物理用量（以 MiB 秒为单位）。  如果数据集使用逻辑存储[结算模式](https://docs.cloud.google.com/bigquery/docs/datasets-intro?hl=zh-cn#dataset_storage_billing_models)，则返回 0。 |

为了确保稳定性，我们建议您在信息架构查询中明确列出列，而不是使用通配符 (`SELECT *`)。明确列出列可防止底层架构发生更改时查询中断。

## 范围和语法

针对此视图的查询必须包含[区域限定符](https://docs.cloud.google.com/bigquery/docs/information-schema-intro?hl=zh-cn#syntax)。如果您未指定区域限定符，则系统会从所有区域检索元数据。下表说明了此视图的区域范围：

| 视图名称 | 资源范围 | 区域范围 |
| --- | --- | --- |
| `` [PROJECT_ID.]`region-REGION`.INFORMATION_SCHEMA.TABLE_STORAGE_USAGE_TIMELINE_BY_ORGANIZATION `` | 包含指定项目的组织 | `REGION` |

请替换以下内容：

* 可选：`PROJECT_ID`：您的 Google Cloud 项目的 ID。如果未指定，则使用默认项目。
* `REGION`：任何[数据集区域名称](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-cn)。
  例如 `` `region-us` ``。**注意：**您必须使用[区域限定符](https://docs.cloud.google.com/bigquery/docs/information-schema-intro?hl=zh-cn#region_qualifier)来查询 `INFORMATION_SCHEMA` 视图。查询执行的位置必须与 `INFORMATION_SCHEMA` 视图的区域相匹配。

以下示例演示了如何返回组织内指定项目中的表的存储信息：

```
SELECT * FROM myProject.`region-REGION`.INFORMATION_SCHEMA.TABLE_STORAGE_USAGE_TIMELINE_BY_ORGANIZATION;
```

以下示例展示了如何按项目返回组织中表的存储空间信息：

```
SELECT * FROM `region-REGION`.INFORMATION_SCHEMA.TABLE_STORAGE_USAGE_TIMELINE_BY_ORGANIZATION;
```

## 示例

以下示例展示了组织中的所有表在最近使用日期的使用情况。

```
SELECT
  usage_date,
  project_id,
  table_schema,
  table_name,
  billable_total_logical_usage,
  billable_total_physical_usage
FROM
  (
    SELECT
      *,
      ROW_NUMBER()
        OVER (PARTITION BY project_id, table_schema, table_name ORDER BY usage_date DESC) AS rank
    FROM
      `region-REGION`.INFORMATION_SCHEMA.TABLE_STORAGE_USAGE_TIMELINE_BY_ORGANIZATION
  )
WHERE rank = 1;
```

结果类似于以下内容：

```
+--------------+------------+--------------+------------+------------------------------+-------------------------------+
| usage_date   | project_id | table_schema | table_name | billable_total_logical_usage | billable_total_physical_usage |
+--------------+------------+--------------+------------+------------------------------+-------------------------------+
|  2023-04-03  | project1   | dataset_A    | table_x    | 734893409201                 |           0                   |
+--------------+------------+--------------+------------+------------------------------+-------------------------------+
|  2023-04-03  | project1   | dataset_A    | table_z    | 110070445455                 |           0                   |
+--------------+------------+--------------+------------+------------------------------+-------------------------------+
|  2023-04-03  | project1   | dataset_B    | table_y    |            0                 | 52500873256                   |
+--------------+------------+--------------+------------+------------------------------+-------------------------------+
|  2023-04-03  | project1   | dataset_B    | table_t    |            0                 | 32513713981                   |
+--------------+------------+--------------+------------+------------------------------+-------------------------------+
|  2023-04-03  | project2   | dataset_C    | table_m    |   8894535352                 |           0                   |
+--------------+------------+--------------+------------+------------------------------+-------------------------------+
|  2023-04-03  | project2   | dataset_C    | table_n    |   4183337201                 |           0                   |
+--------------+------------+--------------+------------+------------------------------+-------------------------------+
```




发送反馈

如未另行说明，那么本页面中的内容已根据[知识共享署名 4.0 许可](https://creativecommons.org/licenses/by/4.0/)获得了许可，并且代码示例已根据 [Apache 2.0 许可](https://www.apache.org/licenses/LICENSE-2.0)获得了许可。有关详情，请参阅 [Google 开发者网站政策](https://developers.google.com/site-policies?hl=zh-cn)。Java 是 Oracle 和/或其关联公司的注册商标。

最后更新时间 (UTC)：2026-03-10。




需要向我们提供更多信息？

[[["易于理解","easyToUnderstand","thumb-up"],["解决了我的问题","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["很难理解","hardToUnderstand","thumb-down"],["信息或示例代码不正确","incorrectInformationOrSampleCode","thumb-down"],["没有我需要的信息/示例","missingTheInformationSamplesINeed","thumb-down"],["翻译问题","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["最后更新时间 (UTC)：2026-03-10。"],[],[]]