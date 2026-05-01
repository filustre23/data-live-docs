* [Home](https://docs.cloud.google.com/?hl=zh-cn)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-cn)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-cn)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-cn)
* [参考文档](https://docs.cloud.google.com/bigquery/quotas?hl=zh-cn)

发送反馈



使用集合让一切井井有条

根据您的偏好保存内容并对其进行分类。

# INFORMATION\_SCHEMA.INSIGHTS 视图

**预览版**

此产品或功能 受[服务专用条款](https://docs.cloud.google.com/terms/service-terms?hl=zh-cn#1)的约束。
非正式版产品和功能“按原样”提供，可能只能获得有限的支持。
如需了解详情，请参阅[发布阶段说明](https://cloud.google.com/products/?hl=zh-cn#product-launch-stages)。

如需就此功能提供反馈或请求支持，请发送电子邮件至 [bq-recommendations+feedback@google.com](mailto:bq-recommendations+feedback@google.com)。

`INFORMATION_SCHEMA.INSIGHTS` 视图包含有关当前项目中所有 BigQuery 建议的数据分析。BigQuery 会从 Active Assist 检索所有 BigQuery 数据分析类型的数据分析结果，并在此视图中显示。BigQuery 数据分析始终与建议相关联。

`INFORMATION_SCHEMA.INSIGHTS` 视图支持以下建议：

* [分区和聚簇建议](https://docs.cloud.google.com/bigquery/docs/view-partition-cluster-recommendations?hl=zh-cn)
* [物化视图建议](https://docs.cloud.google.com/bigquery/docs/manage-materialized-recommendations?hl=zh-cn)
* [BigQuery 数据集的角色建议](https://docs.cloud.google.com/policy-intelligence/docs/review-apply-role-recommendations-datasets?hl=zh-cn)

## 所需权限

如需使用 `INFORMATION_SCHEMA.INSIGHTS` 视图查看数据分析，您必须拥有相应 Recommender 所需的权限。`INFORMATION_SCHEMA.INSIGHTS` 视图仅从您有权查看的建议中返回数据分析。

请让您的管理员授予查看数据分析的权限。如需查看每个 Recommender 所需的权限，请参阅以下内容：

* [分区和集群 Recommender 权限](https://docs.cloud.google.com/bigquery/docs/view-partition-cluster-recommendations?hl=zh-cn#required_permissions)
* [物化视图建议权限](https://docs.cloud.google.com/bigquery/docs/manage-materialized-recommendations?hl=zh-cn#required_permissions)
* [针对数据集权限的角色建议](https://docs.cloud.google.com/policy-intelligence/docs/review-apply-role-recommendations-datasets?hl=zh-cn#required-permissions)

## 架构

`INFORMATION_SCHEMA.INSIGHTS` 视图具有如下架构：

| 列名 | 数据类型 | 值 |
| --- | --- | --- |
| `insight_id` | `STRING` | 包含数据分析类型和数据分析 ID 的 Base64 编码 ID |
| `insight_type` | `STRING` | 数据分析的类型。例如 `google.bigquery.materializedview.Insight`。 |
| `subtype` | `STRING` | 数据分析的子类型。 |
| `project_id` | `STRING` | 项目的 ID。 |
| `project_number` | `STRING` | 项目编号。 |
| `description` | `STRING` | 建议的说明。 |
| `last_updated_time` | `TIMESTAMP` | 此字段表示上次刷新数据分析的时间。 |
| `category` | `STRING` | 影响的优化类别。 |
| `target_resources` | `STRING` | 此数据分析定位的完全限定资源名称。 |
| `state` | `STRING` | 数据分析的状态。如需查看可能值的列表，请参阅[值](https://docs.cloud.google.com/recommender/docs/reference/rest/v1/billingAccounts.locations.insightTypes.insights?hl=zh-cn#Insight.State)。 |
| `severity` | `STRING` | 数据分析的严重程度。如需查看可能的值列表，请参阅[严重级别](https://docs.cloud.google.com/recommender/docs/reference/rest/v1/billingAccounts.locations.insightTypes.insights?hl=zh-cn#severity)。 |
| `associated_recommendation_ids` | `STRING` | 与此数据分析相关联的完整建议名称。建议名称是 Recommender 类型和推荐 ID 的 Base64 编码表示形式。 |
| `additional_details` | `RECORD` | 有关数据分析的其他详细信息。  * `content`：JSON 格式的数据分析内容。 * `state_metadata`：关于数据分析状态的元数据。包含键值对。 * `observation_period_seconds`：生成数据分析的观察期。 |

为了确保稳定性，我们建议您在信息架构查询中明确列出列，而不是使用通配符 (`SELECT *`)。明确列出列可防止底层架构发生更改时查询中断。

## 范围和语法

针对此视图的查询必须包含[区域限定符](https://docs.cloud.google.com/bigquery/docs/information-schema-intro?hl=zh-cn#syntax)。项目 ID 是可选的。如果未指定项目 ID，则使用运行查询的项目。

| 视图名称 | 资源范围 | 区域范围 |
| --- | --- | --- |
| `` [PROJECT_ID.]`region-REGION`.INFORMATION_SCHEMA.INSIGHTS[_BY_PROJECT] `` | 项目级 | `REGION` |

请替换以下内容：

* 可选：`PROJECT_ID`：您的 Google Cloud 项目的 ID。如果未指定，则使用默认项目。
* `REGION`：任何[数据集区域名称](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-cn)。
  例如 `` `region-us` ``。**注意：**您必须使用[区域限定符](https://docs.cloud.google.com/bigquery/docs/information-schema-intro?hl=zh-cn#region_qualifier)来查询 `INFORMATION_SCHEMA` 视图。查询执行的位置必须与 `INFORMATION_SCHEMA` 视图的区域相匹配。

## 示例

如需对非默认项目运行查询，请按以下格式添加项目 ID：

```
`PROJECT_ID`.`region-REGION_NAME`.INFORMATION_SCHEMA.INSIGHTS
```

替换以下内容：

* `PROJECT_ID`：项目的 ID。
* `REGION_NAME`：项目的区域。

例如 `` `myproject`.`region-us`.INFORMATION_SCHEMA.INSIGHTS ``。

### 查看有效数据分析并节省成本

以下示例将数据分析视图与建议视图联接起来，针对 COST 类别中处于 ACTIVE 状态的数据分析返回 3 条建议：

```
WITH
 insights as (SELECT * FROM `region-us`.INFORMATION_SCHEMA.INSIGHTS),
 recs as (SELECT recommender, recommendation_id, additional_details FROM `region-us`.INFORMATION_SCHEMA.RECOMMENDATIONS)

SELECT
   recommender,
   target_resources,
   LAX_INT64(recs.additional_details.overview.bytesSavedMonthly) / POW(1024, 3) as est_gb_saved_monthly,
   LAX_INT64(recs.additional_details.overview.slotMsSavedMonthly) / (1000 * 3600) as slot_hours_saved_monthly,
   insights.additional_details.observation_period_seconds / 86400 as observation_period_days,
   last_updated_time
FROM
  insights
JOIN recs
ON
  recommendation_id in UNNEST(associated_recommendation_ids)
WHERE
  state = 'ACTIVE'
AND
  category = 'COST'
LIMIT 3;
```

**注意：**`INFORMATION_SCHEMA` 视图名称区分大小写。

结果类似于以下内容：

```
+---------------------------------------------------+---------------------+--------------------+--------------------------+-------------------------+---------------------+
|                    recommender                    |   target_resource   |  gb_saved_monthly  | slot_hours_saved_monthly | observation_period_days |  last_updated_time  |
+---------------------------------------------------+---------------------+--------------------+--------------------------+-------------------------+---------------------+
| google.bigquery.table.PartitionClusterRecommender | ["table_resource1"] |   3934.07264107652 |       10.499466666666667 |                    30.0 | 2024-07-01 16:41:25 |
| google.bigquery.table.PartitionClusterRecommender | ["table_resource2"] | 4393.7416711859405 |        56.61476777777777 |                    30.0 | 2024-07-01 16:41:25 |
| google.bigquery.materializedview.Recommender      | ["project_resource"]| 140805.38289248943 |        9613.139166666666 |                     2.0 | 2024-07-01 13:00:31 |
+---------------------------------------------------+---------------------+--------------------+--------------------------+-------------------------+---------------------+
```




发送反馈

如未另行说明，那么本页面中的内容已根据[知识共享署名 4.0 许可](https://creativecommons.org/licenses/by/4.0/)获得了许可，并且代码示例已根据 [Apache 2.0 许可](https://www.apache.org/licenses/LICENSE-2.0)获得了许可。有关详情，请参阅 [Google 开发者网站政策](https://developers.google.com/site-policies?hl=zh-cn)。Java 是 Oracle 和/或其关联公司的注册商标。

最后更新时间 (UTC)：2026-03-18。




需要向我们提供更多信息？

[[["易于理解","easyToUnderstand","thumb-up"],["解决了我的问题","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["很难理解","hardToUnderstand","thumb-down"],["信息或示例代码不正确","incorrectInformationOrSampleCode","thumb-down"],["没有我需要的信息/示例","missingTheInformationSamplesINeed","thumb-down"],["翻译问题","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["最后更新时间 (UTC)：2026-03-18。"],[],[]]