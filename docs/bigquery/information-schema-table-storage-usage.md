* [Home](https://docs.cloud.google.com/?hl=zh-cn)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-cn)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-cn)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-cn)
* [参考文档](https://docs.cloud.google.com/bigquery/quotas?hl=zh-cn)

发送反馈



使用集合让一切井井有条

根据您的偏好保存内容并对其进行分类。

# TABLE\_STORAGE\_USAGE\_TIMELINE 视图

**预览版**

此产品或功能 受[服务专用条款](https://docs.cloud.google.com/terms/service-terms?hl=zh-cn#1)的约束。
非正式版产品和功能“按原样”提供，可能只能获得有限的支持。
如需了解详情，请参阅[发布阶段说明](https://cloud.google.com/products/?hl=zh-cn#product-launch-stages)。

`INFORMATION_SCHEMA.TABLE_STORAGE_USAGE_TIMELINE` 视图提供以下类型的表在过去 90 天内的每日总存储用量：

* 标准表
* 具体化视图
* 包含基表中字节增量的表克隆
* 包含基表中字节增量的表快照

没有计费字节数的表不包含在 `INFORMATION_SCHEMA.TABLE_STORAGE_USAGE_TIMELINE` 视图中。这包括以下类型的表：

* 外部表
* 匿名表
* 空表
* 不包含基表中字节增量的表克隆
* 不包含基表中字节增量的表快照

查询 `INFORMATION_SCHEMA.TABLE_STORAGE_USAGE_TIMELINE` 视图时，查询结果包含每天当前项目的每个表或具体化视图对应的一行。

此表中的数据不会实时保留，表数据大约需要 72 小时才能反映在此视图中。

存储用量以 MiB 秒为单位返回。例如，如果项目在 86,400 秒（24 小时）使用 1,000,000 个物理字节，则物理总用量为 86,400,000,000 字节秒，转换为 82,397 MiB 秒，如以下示例所示：

```
86,400,000,000 / 1,024 / 1,024 = 82,397
```

这是 `BILLABLE_TOTAL_PHYSICAL_USAGE` 列将返回的值。

如需了解详情，请参阅[存储价格详细信息](https://cloud.google.com/bigquery/pricing?hl=zh-cn#storage-pricing-details)。

**注意：**此视图返回的数据在 2023 年 10 月 1 日及之后完成。您可以查询该日期之前的视图，但返回的数据不完整。

## 所需权限

如需查询 `INFORMATION_SCHEMA.TABLE_STORAGE_USAGE_TIMELINE` 视图，您需要拥有以下 Identity and Access Management (IAM) 权限：

* `bigquery.tables.get`
* `bigquery.tables.list`

以下每个预定义的 IAM 角色均可提供上述权限：

* `roles/bigquery.dataViewer`
* `roles/bigquery.dataEditor`
* `roles/bigquery.metadataViewer`
* `roles/bigquery.admin`

对于包含区域限定符的查询，您必须拥有项目的权限。

如需详细了解 BigQuery 权限，请参阅[使用 IAM 进行访问权限控制](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-cn)。

## 架构

`INFORMATION_SCHEMA.TABLE_STORAGE_USAGE_TIMELINE` 视图具有如下架构：

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

针对此视图的查询必须包含[区域限定符](https://docs.cloud.google.com/bigquery/docs/information-schema-intro?hl=zh-cn#syntax)。下表说明了此视图的区域范围：

| 视图名称 | 资源范围 | 区域范围 |
| --- | --- | --- |
| `` [PROJECT_ID.]`region-REGION`.INFORMATION_SCHEMA.TABLE_STORAGE_USAGE_TIMELINE[_BY_PROJECT] `` | 项目级 | `REGION` |

请替换以下内容：

* 可选：`PROJECT_ID`：您的 Google Cloud 项目的 ID。如果未指定，则使用默认项目。
* `REGION`：任何[数据集区域名称](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-cn)。
  例如 `` `region-us` ``。**注意：**您必须使用[区域限定符](https://docs.cloud.google.com/bigquery/docs/information-schema-intro?hl=zh-cn#region_qualifier)来查询 `INFORMATION_SCHEMA` 视图。查询执行的位置必须与 `INFORMATION_SCHEMA` 视图的区域相匹配。

以下示例演示了如何返回指定项目中的表的存储信息：

```
SELECT * FROM myProject.`region-REGION`.INFORMATION_SCHEMA.TABLE_STORAGE_USAGE_TIMELINE;
```

以下示例演示了如何返回指定区域中的表的存储信息：

```
SELECT * FROM `region-REGION`.INFORMATION_SCHEMA.TABLE_STORAGE_USAGE_TIMELINE;
```

## 示例

**注意**：`INFORMATION_SCHEMA` 视图名称区分大小写。

**示例 1**

以下示例汇总了指定区域中的项目每天的存储用量。

```
SELECT
  usage_date,
  project_id,
  SUM(billable_total_logical_usage) AS billable_total_logical_usage,
  SUM(billable_active_logical_usage) AS billable_active_logical_usage,
  SUM(billable_long_term_logical_usage) AS billable_long_term_logical_usage,
  SUM(billable_total_physical_usage) AS billable_total_physical_usage,
  SUM(billable_active_physical_usage) AS billable_active_physical_usage,
  SUM(billable_long_term_physical_usage) AS billable_long_term_physical_usage
FROM
  `region-REGION`.INFORMATION_SCHEMA.TABLE_STORAGE_USAGE_TIMELINE
GROUP BY
  1,
  2
ORDER BY
  usage_date;
```

结果类似于以下内容：

```
+-------------------------+------------------------------+-------------------------------+-----------------------------------+-------------------------------+--------------------------------+-------------------------------------+
| usage_date | project_id | billable_total_logical_usage | billable_active_logical_usage | billable_long_term_logical_usage  | billable_total_physical_usage | billable_active_physical_usage | billable_long_term_physical_usage   |
+-------------------------+------------------------------+-------------------------------+-----------------------------------+-------------------------------+--------------------------------+-------------------------------------+
| 2023-04-03 | project_A  | 305085738096                 | 7667321458                    | 297418416638                      | 74823954823                   | 124235724                      | 74699719099                         |
+-------------------------+------------------------------+-------------------------------+-----------------------------------+-------------------------------+--------------------------------+-------------------------------------+
| 2023-04-04 | project_A  | 287033241105                 | 7592334614                    | 279440906491                      | 75071991788                   | 200134561                      | 74871857227                         |
+-------------------------+------------------------------+-------------------------------+-----------------------------------+-------------------------------+--------------------------------+-------------------------------------+
| 2023-04-03 | project_B  | 478173930912                 | 8137372626                    | 470036558286                      | 0                             | 0                              | 0                                   |
+-------------------------+------------------------------+-------------------------------+-----------------------------------+-------------------------------+--------------------------------+-------------------------------------+
| 2023-04-04 | project_B  | 496648915405                 | 7710451723                    | 488938463682                      | 0                             | 0                              | 0                                   |
+-------------------------+------------------------------+-------------------------------+-----------------------------------+-------------------------------+--------------------------------+-------------------------------------+
```

**示例 2**

以下示例展示了使用逻辑存储的数据集中的表在指定日期的存储用量。

```
SELECT
  usage_date,
  table_schema,
  table_name,
  billable_total_logical_usage
FROM
  `region-REGION`.INFORMATION_SCHEMA.TABLE_STORAGE_USAGE_TIMELINE
WHERE
  project_id = 'PROJECT_ID'
  AND table_schema = 'DATASET_NAME'
  AND usage_date = 'USAGE_DATE'
ORDER BY
  billable_total_logical_usage DESC;
```

结果类似于以下内容：

```
+--------------+--------------+------------+------------------------------+
| usage_date   | table_schema | table_name | billable_total_logical_usage |
+--------------+--------------+------------+------------------------------+
|  2023-04-03  | dataset_A    | table_4    | 734893409201                 |
+--------------+--------------+------------+------------------------------+
|  2023-04-03  | dataset_A    | table_1    | 690070445455                 |
+--------------+--------------+------------+------------------------------+
|  2023-04-03  | dataset_A    | table_3    |  52513713981                 |
+--------------+--------------+------------+------------------------------+
|  2023-04-03  | dataset_A    | table_2    |   8894535355                 |
+--------------+--------------+------------+------------------------------+
```

**示例 3**

以下示例展示了使用物理存储的数据集中的表在最近使用日期的存储用量。

```
SELECT
  usage_date,
  table_schema,
  table_name,
  billable_total_physical_usage
FROM
  (
    SELECT
      *,
      ROW_NUMBER()
        OVER (PARTITION BY project_id, table_schema, table_name ORDER BY usage_date DESC) AS rank
    FROM
      `region-REGION`.INFORMATION_SCHEMA.TABLE_STORAGE_USAGE_TIMELINE
  )
WHERE
  rank = 1
  AND project_id = 'PROJECT_ID'
  AND table_schema ='DATASET_NAME'
ORDER BY
  usage_date;
```

结果类似于以下内容：

```
+--------------+--------------+------------+-------------------------------+
| usage_date   | table_schema | table_name | billable_total_physical_usage |
+--------------+--------------+------------+-------------------------------+
|  2023-04-12  | dataset_A    | table_4    |  345788341123                 |
+--------------+--------------+------------+-------------------------------+
|  2023-04-12  | dataset_A    | table_1    |             0                 |
+--------------+--------------+------------+-------------------------------+
|  2023-04-12  | dataset_A    | table_3    | 9123481400212                 |
+--------------+--------------+------------+-------------------------------+
|  2023-04-12  | dataset_A    | table_2    |    1451334553                 |
+--------------+--------------+------------+-------------------------------+
```

**示例 4**

以下示例会联接 `TABLE_OPTIONS` 和 `TABLE_STORAGE_USAGE_TIMELINE` 视图，以根据标记获取存储用量详细信息。

```
SELECT * FROM region-REGION.INFORMATION_SCHEMA.TABLE_OPTIONS
    INNER JOIN region-REGION.INFORMATION_SCHEMA.TABLE_STORAGE_USAGE_TIMELINE
    USING (TABLE_CATALOG, TABLE_SCHEMA, TABLE_NAME)
    WHERE option_name='tags'
    AND CONTAINS_SUBSTR(option_value, '(\"tag_namespaced_key\", \"tag_namespaced_value\")')
```




发送反馈

如未另行说明，那么本页面中的内容已根据[知识共享署名 4.0 许可](https://creativecommons.org/licenses/by/4.0/)获得了许可，并且代码示例已根据 [Apache 2.0 许可](https://www.apache.org/licenses/LICENSE-2.0)获得了许可。有关详情，请参阅 [Google 开发者网站政策](https://developers.google.com/site-policies?hl=zh-cn)。Java 是 Oracle 和/或其关联公司的注册商标。

最后更新时间 (UTC)：2026-03-10。




需要向我们提供更多信息？

[[["易于理解","easyToUnderstand","thumb-up"],["解决了我的问题","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["很难理解","hardToUnderstand","thumb-down"],["信息或示例代码不正确","incorrectInformationOrSampleCode","thumb-down"],["没有我需要的信息/示例","missingTheInformationSamplesINeed","thumb-down"],["翻译问题","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["最后更新时间 (UTC)：2026-03-10。"],[],[]]