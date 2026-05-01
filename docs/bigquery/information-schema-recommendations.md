* [Home](https://docs.cloud.google.com/?hl=zh-cn)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-cn)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-cn)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-cn)
* [参考文档](https://docs.cloud.google.com/bigquery/quotas?hl=zh-cn)

发送反馈



使用集合让一切井井有条

根据您的偏好保存内容并对其进行分类。

# INFORMATION\_SCHEMA.RECOMMENDATIONS 视图

**预览版**

此产品或功能 受[服务专用条款](https://docs.cloud.google.com/terms/service-terms?hl=zh-cn#1)的约束。
非正式版产品和功能“按原样”提供，可能只能获得有限的支持。
如需了解详情，请参阅[发布阶段说明](https://cloud.google.com/products/?hl=zh-cn#product-launch-stages)。

如需就此功能提供反馈或请求支持，请发送电子邮件至 [bq-recommendations+feedback@google.com](mailto:bq-recommendations+feedback@google.com)。

`INFORMATION_SCHEMA.RECOMMENDATIONS` 视图包含有关当前项目中所有 BigQuery 建议的数据。BigQuery 会从 Active Assist 检索所有 BigQuery Recommender 的建议，并将其显示在此视图中。

`INFORMATION_SCHEMA.RECOMMENDATIONS` 视图支持以下建议：

* [分区和集群建议](https://docs.cloud.google.com/bigquery/docs/view-partition-cluster-recommendations?hl=zh-cn)
* [物化视图建议](https://docs.cloud.google.com/bigquery/docs/manage-materialized-recommendations?hl=zh-cn)
* [BigQuery 数据集的角色建议](https://docs.cloud.google.com/policy-intelligence/docs/review-apply-role-recommendations-datasets?hl=zh-cn)

`INFORMATION_SCHEMA.RECOMMENDATIONS` 视图仅显示与 BigQuery 相关的建议。您可以在 Active Assist 中查看 Google Cloud 建议。

## 所需权限

如需使用 `INFORMATION_SCHEMA.RECOMMENDATIONS` 视图查看建议，您必须拥有相应 Recommender 所需的权限。`INFORMATION_SCHEMA.RECOMMENDATIONS` 视图仅返回您有权查看的建议。

请让您的管理员授予查看建议的权限。如需查看每个 Recommender 所需的权限，请参阅以下内容：

* [分区和集群 Recommender 权限](https://docs.cloud.google.com/bigquery/docs/view-partition-cluster-recommendations?hl=zh-cn#required_permissions)
* [物化视图建议权限](https://docs.cloud.google.com/bigquery/docs/manage-materialized-recommendations?hl=zh-cn#required_permissions)
* [针对数据集权限的角色建议](https://docs.cloud.google.com/policy-intelligence/docs/review-apply-role-recommendations-datasets?hl=zh-cn#required-permissions)

## 架构

`INFORMATION_SCHEMA.RECOMMENDATIONS` 视图具有如下架构：

| 列名 | 数据类型 | 值 |
| --- | --- | --- |
| `recommendation_id` | `STRING` | 包含 RecommendationID 和 Recommender 的 Base64 编码 ID。 |
| `recommender` | `STRING` | 建议类型。 例如，`google.bigquery.table.PartitionClusterRecommender` 表示分区和聚簇建议。 |
| `subtype` | `STRING` | 建议的子类型。 |
| `project_id` | `STRING` | 项目的 ID。 |
| `project_number` | `STRING` | 项目编号。 |
| `description` | `STRING` | 有关建议的说明。 |
| `last_updated_time` | `TIMESTAMP` | 此字段表示上次创建建议的时间。 |
| `target_resources` | `STRING` | 此建议的目标完全限定资源名称。 |
| `state` | `STRING` | 建议的状态。如需查看可能值的列表，请参阅[状态](https://docs.cloud.google.com/recommender/docs/reference/rest/v1/billingAccounts.locations.recommenders.recommendations?hl=zh-cn#state)。 |
| `primary_impact` | `RECORD` | 尝试优化主要类别时，此建议可能产生的影响。包含以下字段：  * `category`：此建议尝试优化的类别。如需查看可能值的列表，请参阅[类别](https://docs.cloud.google.com/recommender/docs/reference/rest/v1/billingAccounts.locations.recommenders.recommendations?hl=zh-cn#category)。 * `cost_projection`：如果建议可以预测此建议可节省的费用，则可以填充此值。仅当类别为 `COST` 时才会存在。 * `security_projection`：当类别为 `SECURITY` 时，可能存在。 |
| `priority` | `STRING` | 建议的优先级。如需查看可能值的列表，请参阅[优先级](https://docs.cloud.google.com/recommender/docs/reference/rest/v1/billingAccounts.locations.recommenders.recommendations?hl=zh-cn#priority)。 |
| `associated_insight_ids` | `STRING` | 与建议相关联的完整数据分析名称。数据分析名称是数据分析类型名称和数据分析 ID 的 Base64 编码表示形式。这可用于查询“数据分析”视图。 |
| `additional_details` | `RECORD` | 有关建议的其他详细信息。  * `overview`：JSON 格式的建议概览。此字段的内容可能会根据 Recommender 而变化。 * `state_metadata`：关于建议状态的元数据（采用键值对形式）。 * `operations`：用户可以对目标资源执行的操作列表。其中包含以下字段：  + `action`：用户必须执行的操作类型。这可以是系统在生成建议时设置的自由文本。将始终填充。 + `resource_type`：云资源类型。 + `resource`：完全限定的资源名称。 + `path`：目标字段相对于资源的路径。 + `value`：路径字段的值。 |

为了确保稳定性，我们建议您在信息架构查询中明确列出列，而不是使用通配符 (`SELECT *`)。明确列出列可防止底层架构发生更改时查询中断。

## 范围和语法

针对此视图的查询必须包含[区域限定符](https://docs.cloud.google.com/bigquery/docs/information-schema-intro?hl=zh-cn#syntax)。项目 ID 是可选的。如果未指定项目 ID，则使用运行查询的项目。

| 视图名称 | 资源范围 | 区域范围 |
| --- | --- | --- |
| `` [PROJECT_ID.]`region-REGION`.INFORMATION_SCHEMA.RECOMMENDATIONS[_BY_PROJECT] `` | 项目级 | `REGION` |

请替换以下内容：

* 可选：`PROJECT_ID`：您的 Google Cloud 项目的 ID。如果未指定，则使用默认项目。
* `REGION`：任何[数据集区域名称](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-cn)。
  例如 `` `region-us` ``。**注意：**您必须使用[区域限定符](https://docs.cloud.google.com/bigquery/docs/information-schema-intro?hl=zh-cn#region_qualifier)来查询 `INFORMATION_SCHEMA` 视图。查询执行的位置必须与 `INFORMATION_SCHEMA` 视图的区域相匹配。

## 示例

如需对非默认项目运行查询，请按以下格式添加项目 ID：

```
`PROJECT_ID`.`region-REGION_NAME`.INFORMATION_SCHEMA.RECOMMENDATIONS
```

替换以下内容：

* `PROJECT_ID`：项目的 ID。
* `REGION_NAME`：项目的区域。

例如 `` `myproject`.`region-us`.INFORMATION_SCHEMA.RECOMMENDATIONS ``。

### 查看热门的费用节省建议

以下示例根据预计的 `slot_hours_saved_monthly` 返回前 3 个 `COST` 类别建议：

```
SELECT
   recommender,
   target_resources,
   LAX_INT64(additional_details.overview.bytesSavedMonthly) / POW(1024, 3) as est_gb_saved_monthly,
   LAX_INT64(additional_details.overview.slotMsSavedMonthly) / (1000 * 3600) as slot_hours_saved_monthly,
  last_updated_time
FROM
  `region-us`.INFORMATION_SCHEMA.RECOMMENDATIONS_BY_PROJECT
WHERE
   primary_impact.category = 'COST'
AND
   state = 'ACTIVE'
ORDER by
   slot_hours_saved_monthly DESC
LIMIT 3;
```

**注意：**`INFORMATION_SCHEMA` 视图名称区分大小写。

结果类似于以下内容：

```
+---------------------------------------------------+--------------------------------------------------------------------------------------------------+
|                    recommender                    |   target_resources      | est_gb_saved_monthly | slot_hours_saved_monthly |  last_updated_time
+---------------------------------------------------+--------------------------------------------------------------------------------------------------+
| google.bigquery.materializedview.Recommender      | ["project_resource"]    | 140805.38289248943   |        9613.139166666666 |  2024-07-01 13:00:00
| google.bigquery.table.PartitionClusterRecommender | ["table_resource_1"]    | 4393.7416711859405   |        56.61476777777777 |  2024-07-01 13:00:00
| google.bigquery.table.PartitionClusterRecommender | ["table_resource_2"]    |   3934.07264107652   |       10.499466666666667 |  2024-07-01 13:00:00
+---------------------------------------------------+--------------------------------------------------------------------------------------------------+
```




发送反馈

如未另行说明，那么本页面中的内容已根据[知识共享署名 4.0 许可](https://creativecommons.org/licenses/by/4.0/)获得了许可，并且代码示例已根据 [Apache 2.0 许可](https://www.apache.org/licenses/LICENSE-2.0)获得了许可。有关详情，请参阅 [Google 开发者网站政策](https://developers.google.com/site-policies?hl=zh-cn)。Java 是 Oracle 和/或其关联公司的注册商标。

最后更新时间 (UTC)：2026-03-18。




需要向我们提供更多信息？

[[["易于理解","easyToUnderstand","thumb-up"],["解决了我的问题","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["很难理解","hardToUnderstand","thumb-down"],["信息或示例代码不正确","incorrectInformationOrSampleCode","thumb-down"],["没有我需要的信息/示例","missingTheInformationSamplesINeed","thumb-down"],["翻译问题","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["最后更新时间 (UTC)：2026-03-18。"],[],[]]