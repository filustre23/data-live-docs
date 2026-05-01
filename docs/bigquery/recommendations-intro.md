* [Home](https://docs.cloud.google.com/?hl=zh-cn)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-cn)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-cn)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-cn)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-cn)

发送反馈



使用集合让一切井井有条

根据您的偏好保存内容并对其进行分类。

# 建议概览

**预览版**

此产品或功能 受[服务专用条款](https://docs.cloud.google.com/terms/service-terms?hl=zh-cn#1)的约束。
非正式版产品和功能“按原样”提供，可能只能获得有限的支持。
如需了解详情，请参阅[发布阶段说明](https://cloud.google.com/products/?hl=zh-cn#product-launch-stages)。

BigQuery 与 Active Assist 配合使用，可提供各种建议，以便您优化 BigQuery 资源。

建议由 Recommender 生成，它们使用机器学习 (ML) 或启发法提供有关如何优化 BigQuery 资源用量的建议。

您可以通过在 Google Cloud 控制台中的 BigQuery 查看和管理不同 Recommender 提供的建议，具体方法是在 BigQuery Active Assist 中查看，或通过 BigQuery Studio 中的建议通知进行管理。您还可以通过项目和组织级别的各种 `INFORMATION_SCHEMA` 视图查看建议。

如需查看您的 BigQuery 建议以及 Google Cloud 控制台中的其他建议，请使用 [Active Assist](https://docs.cloud.google.com/recommender/docs/recommendation-hub/find-recommnedation-hub?hl=zh-cn)。

## BigQuery Recommender

BigQuery 提供以下 Recommender：

* [分区和聚类 Recommender](https://docs.cloud.google.com/bigquery/docs/view-partition-cluster-recommendations?hl=zh-cn)，用于分析查询行为，以寻找优化 BigQuery 表的分区和聚类机会。
* [物化视图 Recommender](https://docs.cloud.google.com/bigquery/docs/manage-materialized-recommendations?hl=zh-cn)，可帮助您找到使用物化视图优化工作流的机会。
* [IAM Recommender](https://docs.cloud.google.com/policy-intelligence/docs/role-recommendations-overview?hl=zh-cn)，用于分析 BigQuery 数据集的权限，并为拥有过多权限的主账号建议更新 Identity and Access Management (IAM) 角色。

## 查看建议

如需使用 Google Cloud 控制台查看建议，请执行以下操作：

1. 在 Google Cloud 控制台中，前往 **BigQuery** 页面。

   [转到 BigQuery](https://console.cloud.google.com/bigquery?hl=zh-cn)
2. 在导航菜单中，点击**建议**。

   系统会打开**建议**页面，其中会显示为当前项目或组织生成的所有建议，具体取决于所选范围。
3. 如需详细了解特定建议或数据分析，请点击相应建议。

### 查看包含 `INFORMATION_SCHEMA` 的建议

您还可以使用 `INFORMATION_SCHEMA` 视图查看建议和数据分析。例如，您可以使用 `INFORMATION_SCHEMA.RECOMMENDATIONS` 视图根据槽节省量查看前三条建议，如以下示例所示：

```
SELECT
   recommender,
   target_resources,
   LAX_INT64(additional_details.overview.bytesSavedMonthly) / POW(1024, 3) as est_gb_saved_monthly,
   LAX_INT64(additional_details.overview.slotMsSavedMonthly) / (1000 * 3600) as slot_hours_saved_monthly,
  last_updated_time
FROM
  `region-us`.INFORMATION_SCHEMA.RECOMMENDATIONS
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

如需了解详情，请参阅以下资源：

* [`INFORMATION_SCHEMA.RECOMMENDATIONS` 视图](https://docs.cloud.google.com/bigquery/docs/information-schema-recommendations?hl=zh-cn)
* [`INFORMATION_SCHEMA.RECOMMENDATIONS_BY_ORGANIZATION` 视图](https://docs.cloud.google.com/bigquery/docs/information-schema-recommendations-by-org?hl=zh-cn)
* [`INFORMATION_SCHEMA.INSIGHTS` 视图](https://docs.cloud.google.com/bigquery/docs/information-schema-insights?hl=zh-cn)

## 后续步骤

* 了解如何[查看分区和聚簇建议](https://docs.cloud.google.com/bigquery/docs/view-partition-cluster-recommendations?hl=zh-cn)。
* 了解如何[应用分区和聚簇建议](https://docs.cloud.google.com/bigquery/docs/apply-partition-cluster-recommendations?hl=zh-cn)。
* 了解如何[管理物化视图建议](https://docs.cloud.google.com/bigquery/docs/manage-materialized-recommendations?hl=zh-cn)。
* 了解如何[使用 IAM Recommender](https://docs.cloud.google.com/policy-intelligence/docs/role-recommendations-overview?hl=zh-cn)。




发送反馈

如未另行说明，那么本页面中的内容已根据[知识共享署名 4.0 许可](https://creativecommons.org/licenses/by/4.0/)获得了许可，并且代码示例已根据 [Apache 2.0 许可](https://www.apache.org/licenses/LICENSE-2.0)获得了许可。有关详情，请参阅 [Google 开发者网站政策](https://developers.google.com/site-policies?hl=zh-cn)。Java 是 Oracle 和/或其关联公司的注册商标。

最后更新时间 (UTC)：2026-02-14。




需要向我们提供更多信息？

[[["易于理解","easyToUnderstand","thumb-up"],["解决了我的问题","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["很难理解","hardToUnderstand","thumb-down"],["信息或示例代码不正确","incorrectInformationOrSampleCode","thumb-down"],["没有我需要的信息/示例","missingTheInformationSamplesINeed","thumb-down"],["翻译问题","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["最后更新时间 (UTC)：2026-02-14。"],[],[]]