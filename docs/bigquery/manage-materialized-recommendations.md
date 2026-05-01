* [Home](https://docs.cloud.google.com/?hl=zh-cn)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-cn)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-cn)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-cn)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-cn)

发送反馈



使用集合让一切井井有条

根据您的偏好保存内容并对其进行分类。

# 管理物化视图建议

**预览版**

此产品或功能 受[服务专用条款](https://docs.cloud.google.com/terms/service-terms?hl=zh-cn#1)的约束。
非正式版产品和功能“按原样”提供，可能只能获得有限的支持。
如需了解详情，请参阅[发布阶段说明](https://cloud.google.com/products/?hl=zh-cn#product-launch-stages)。

**注意**：如需申请使用此预览版功能，请填写[物化视图建议注册表单](https://forms.gle/M3V75cWZZsHmDBCr6)。
从请求被接受到您可以查看物化视图建议，可能需要长达一周的时间。如需就此预览版提供反馈或提出相关问题，请联系 [bq-mv-help@google.com](mailto:bq-mv-help@google.com)。

本文档介绍了物化视图 Recommender 的工作原理，以及如何查看和应用物化视图建议。

## 简介

BigQuery 物化视图 Recommender 可帮助您提高工作负载性能并节省工作负载执行费用。这些建议基于过去 30 天内的历史查询执行特征。

[具体化视图](https://docs.cloud.google.com/bigquery/docs/materialized-views-intro?hl=zh-cn)是预计算视图，可定期缓存查询结果以提高性能和效率。具体化视图使用[智能调优](https://docs.cloud.google.com/bigquery/docs/materialized-views-use?hl=zh-cn#smart_tuning)以透明方式重写对源表的查询，以使用现有具体化视图来提高性能和效率。

### Recommender 的工作原理

Recommender 会每天为在 BigQuery 中执行查询作业的每个项目生成建议。建议基于过去 30 天的工作负载执行分析。物化视图 Recommender 会查找重复查询句式，并计算在重复子查询可以移动到增量物化视图时可能节省的所有费用。Recommender 会考虑查询时节省的所有费用，并考虑物化视图的维护费用。如果这些综合因素显示显著的积极结果，则 Recommender 会提出建议。

请考虑以下查询示例：

```
WITH revenue   AS
(SELECT l_suppkey as supplier_no,
        sum(l_extendedprice * (1 - l_discount)) as total_revenue
  FROM lineitem
  WHERE
    l_shipdate >= date '1996-01-01'
    AND l_shipdate < date_add(date '1996-01-01', interval 3 MONTH)
  GROUP BY l_suppkey)
SELECT s_suppkey,
      s_name,
      s_address,
      s_phone,
      total_revenue
FROM
supplier,
revenue
WHERE s_suppkey = supplier_no
AND total_revenue =
  (SELECT max(total_revenue)
    FROM revenue)
ORDER BY s_suppkey
```

此查询示例显示有关热门供应商的信息。此查询包含一个名为 `revenue` 的通用表表达式 (CTE)，它表示每个供应商的总收入 (`l_suppkey`)。`revenue` 与供应商表联接，条件是供应商的 `total_revenue` 与所有供应商间的 `max(total_revenue)` 匹配。因此，查询会计算总收入最高的供应商的相关信息（`l_suppkey`、`s_name`、`s_address`、`s_phone`、`total_revenue`）。

整个查询本身过于复杂，无法放入增量物化视图中。但是，`supplier` CTE 是对单个表的聚合（这是增量具体化视图支持的查询句式）。`supplier` CTE 也是查询中计算开销最大的部分。因此，如果对不断变化的源表反复运行示例查询，则物化视图 Recommender 可能会建议将 `supplier` CTE 放入物化视图中。上述示例查询的物化视图建议可能类似于以下内容：

```
CREATE MATERIALIZED VIEW mv AS
SELECT l_suppkey as supplier_no,
         sum(l_extendedprice * (1 - l_discount)) as total_revenue
  FROM lineitem
  WHERE
    l_shipdate >= date '1996-01-01'
    AND l_shipdate < date_add(date '1996-01-01', interval 3 MONTH)
  GROUP BY l_suppkey
```

Recommender API 还会以数据分析的形式返回查询执行信息。[数据分析](https://docs.cloud.google.com/recommender/docs/insights/using-insights?hl=zh-cn)是帮助您了解项目的工作负载的发现结果，提供了有关具体化视图建议如何优化工作负载费用的更多背景信息。

## 限制

* 物化视图 Recommender 不支持[停用数据处理](https://docs.cloud.google.com/recommender/docs/opt-out?hl=zh-cn)的标准流程。如需停止接收物化视图建议，请按照[物化视图建议注册表单](https://forms.gle/M3V75cWZZsHmDBCr6)中的说明操作。
* 物化视图建议无法[导出到 BigQuery](https://docs.cloud.google.com/recommender/docs/bq-export/export-recommendations-to-bq?hl=zh-cn)。

## 准备工作

您需要先[启用 Recommender API](https://docs.cloud.google.com/recommender/docs/enabling?hl=zh-cn)，然后才能查看或应用物化视图建议。

### 所需权限

如需获得访问物化视图建议所需的权限，请让管理员向您授予 [BigQuery Materialized View Recommender Viewer](https://docs.cloud.google.com/iam/docs/roles-permissions/recommender?hl=zh-cn#recommender.bigqueryMaterializedViewViewer) (`roles/recommender.bigqueryMaterializedViewViewer`) IAM 角色。
如需详细了解如何授予角色，请参阅[管理对项目、文件夹和组织的访问权限](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-cn)。

此预定义角色包含访问物化视图建议所需的权限。如需查看所需的确切权限，请展开**所需权限**部分：

#### 所需权限

如需访问物化视图建议，您需要拥有以下权限：

* `recommender.bigqueryMaterializedViewRecommendations.get`
* `recommender.bigqueryMaterializedViewRecommendations.list`

您也可以使用[自定义角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-cn)或其他[预定义角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-cn#predefined)来获取这些权限。

如需详细了解 BigQuery 中的 IAM 角色和权限，请参阅 [IAM 简介](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-cn)。

## 查看物化视图建议

本部分介绍如何使用 Google Cloud 控制台、Google Cloud CLI 或 Recommender API 查看物化视图建议和数据分析。

从下列选项中选择一项：

### 控制台

1. 在 Google Cloud 控制台中，前往 **BigQuery** 页面。

   [转到 BigQuery](https://console.cloud.google.com/bigquery?hl=zh-cn)
2. 在导航菜单中，点击**建议**。
3. 此时会打开 **BigQuery 建议**窗格。在**降低 BigQuery 工作负载费用**下，点击**查看详情**。
4. 此时会出现一个建议列表，其中显示为当前项目生成的所有建议。如需详细了解特定具体化视图建议或表数据分析，请点击**详细信息**。

或者，您也可以点击导航菜单中的**建议**，查看针对您的项目或组织提供的所有建议。

### gcloud

如需查看特定项目的物化视图建议，请使用 [`gcloud recommender recommendations list` 命令](https://docs.cloud.google.com/sdk/gcloud/reference/recommender/recommendations/list?hl=zh-cn)：

```
gcloud recommender recommendations list \
    --project=PROJECT_NAME \
    --location=REGION_NAME \
    --recommender=google.bigquery.materializedview.Recommender \
    --format=FORMAT_TYPE \
```

替换以下内容：

* `PROJECT_NAME`：执行查询作业的项目的名称
* `REGION_NAME`：在其中执行查询作业的区域
* `FORMAT_TYPE`：支持的 [gcloud CLI 输出格式](https://docs.cloud.google.com/sdk/gcloud/reference?hl=zh-cn#--format)，例如 JSON

下表介绍了“建议”回答中的重要字段：

| 属性 | 针对子类型的相关性 | 说明 |
| --- | --- | --- |
| `recommenderSubtype` | `CREATE_MATERIALIZED_VIEW` | 建议类型。 |
| `content.overview.sql` | `CREATE_MATERIALIZED_VIEW` | 用于创建物化视图的建议 DDL 语句。 |
| `content.overview.slotMsSavedMonthly` | `CREATE_MATERIALIZED_VIEW` | 建议视图每月可节省的估算槽毫秒数。 |
| `content.overview.bytesSavedMonthly` | `CREATE_MATERIALIZED_VIEW` | 建议视图每月可节省的估算扫描字节数。 |
| `content.overview.baseTables` | `CREATE_MATERIALIZED_VIEW` | 留待将来使用。 |

* 如需详细了解 `recommendations` 回答中的其他字段，请参阅 [REST 资源：`projects.locations.recommenders.recommendation`](https://docs.cloud.google.com/recommender/docs/reference/rest/v1/projects.locations.recommenders.recommendations?hl=zh-cn#resource:-recommendation)。
* 如需详细了解如何使用 Recommender API，请参阅[使用 API - 建议](https://docs.cloud.google.com/recommender/docs/using-api?hl=zh-cn)。

如需使用 gcloud CLI 查看提示物化视图建议的数据分析，请使用 [`gcloud recommender insights list` 命令](https://docs.cloud.google.com/sdk/gcloud/reference/recommender/insights/list?hl=zh-cn)：

```
gcloud recommender insights list \
    --project=PROJECT_NAME \
    --location=REGION_NAME \
    --insight-type=google.bigquery.materializedview.Insight \
    --format=FORMAT_TYPE \
```

替换以下内容：

* `PROJECT_NAME`：执行查询作业的项目的名称
* `REGION_NAME`：在其中执行查询作业的区域
* `FORMAT_TYPE`：支持的 [gcloud CLI 输出格式](https://docs.cloud.google.com/sdk/gcloud/reference?hl=zh-cn#--format)，例如 JSON

下表介绍了数据分析 API 响应中的重要字段：

| 属性 | 针对子类型的相关性 | 说明 |
| --- | --- | --- |
| `content.queryCount` | `CREATE_MATERIALIZED_VIEW` | 观察期内具有重复模式（可使用物化视图进行优化）的查询数。 |

* 如需详细了解数据分析响应中的其他字段，请参阅 [REST 资源：`projects.locations.insightTypes.insights`](https://docs.cloud.google.com/recommender/docs/reference/rest/v1/projects.locations.insightTypes.insights?hl=zh-cn#resource:-insight)。
* 如需详细了解如何使用数据分析，请参阅[使用 API - 数据分析](https://docs.cloud.google.com/recommender/docs/insights/using-api?hl=zh-cn)。

### REST API

如需查看特定项目的物化视图建议，请使用 REST API。您必须在每个命令中提供一个身份验证令牌，该令牌可使用 gcloud CLI 获取。如需详细了解如何获取身份验证令牌，请参阅[获取 ID 令牌的方法](https://docs.cloud.google.com/docs/authentication/get-id-token?hl=zh-cn)。

您可以使用 `curl list` 请求查看针对特定项目的所有建议：

```
$ curl
-H "Authorization: Bearer $(gcloud auth print-access-token)"
-H "x-goog-user-project: PROJECT_NAME" https://recommender.googleapis.com/v1/projects/PROJECT_NAME/locations/LOCATION/recommenders/google.bigquery.materializedview.Recommender/recommendations
```

替换以下内容：

* `PROJECT_NAME`：包含 BigQuery 表的项目的名称
* `LOCATION`：项目所在的位置。

下表介绍了“建议”回答中的重要字段：

| 属性 | 针对子类型的相关性 | 说明 |
| --- | --- | --- |
| `recommenderSubtype` | `CREATE_MATERIALIZED_VIEW` | 建议类型。 |
| `content.overview.sql` | `CREATE_MATERIALIZED_VIEW` | 用于创建物化视图的建议 DDL 语句。 |
| `content.overview.slotMsSavedMonthly` | `CREATE_MATERIALIZED_VIEW` | 建议视图每月可节省的估算槽毫秒数。 |
| `content.overview.bytesSavedMonthly` | `CREATE_MATERIALIZED_VIEW` | 建议视图每月可节省的估算扫描字节数。 |
| `content.overview.baseTables` | `CREATE_MATERIALIZED_VIEW` | 留待将来使用。 |

* 如需详细了解 `recommendations` 回答中的其他字段，请参阅 [REST 资源：`projects.locations.recommenders.recommendation`](https://docs.cloud.google.com/recommender/docs/reference/rest/v1/projects.locations.recommenders.recommendations?hl=zh-cn#resource:-recommendation)。
* 如需详细了解如何使用 Recommender API，请参阅[使用 API - 建议](https://docs.cloud.google.com/recommender/docs/using-api?hl=zh-cn)。

如需使用 REST API 查看提示物化视图建议的数据分析，请运行以下命令：

```
$ curl
-H "Authorization: Bearer $(gcloud auth print-access-token)"
-H "x-goog-user-project: PROJECT_NAME" https://recommender.googleapis.com/v1/projects/PROJECT_NAME/locations/LOCATION/insightTypes/google.bigquery.materializedview.Insight/insights
```

替换以下内容：

* `PROJECT_NAME`：包含 BigQuery 表的项目的名称
* `LOCATION`：项目所在的位置。

下表介绍了数据分析 API 响应中的重要字段：

| 属性 | 针对子类型的相关性 | 说明 |
| --- | --- | --- |
| `content.queryCount` | `CREATE_MATERIALIZED_VIEW` | 观察期内具有重复模式（可使用物化视图进行优化）的查询数。 |

* 如需详细了解数据分析响应中的其他字段，请参阅 [REST 资源：`projects.locations.insightTypes.insights`](https://docs.cloud.google.com/recommender/docs/reference/rest/v1/projects.locations.insightTypes.insights?hl=zh-cn#resource:-insight)。
* 如需详细了解如何使用数据分析，请参阅[使用 API - 数据分析](https://docs.cloud.google.com/recommender/docs/insights/using-api?hl=zh-cn)。

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

## 应用物化视图建议

您可以通过在 Google Cloud 控制台中执行建议的 `CREATE MATERIALIZED VIEW` 类型 DDL 语句，来应用建议创建物化视图。

**注意**：如需执行建议的 `CREATE MATERIALIZED VIEW` DDL 语句，您必须在以下所有位置拥有[所需权限](https://docs.cloud.google.com/bigquery/docs/materialized-views-create?hl=zh-cn#required_permissions)：

* 查询项目
* 包含源表的数据集
* 包含物化视图的数据集

1. 在 Google Cloud 控制台中，前往 **BigQuery** 页面。

   [转到 BigQuery](https://console.cloud.google.com/bigquery?hl=zh-cn)
2. 在导航菜单中，点击**建议**。
3. 此时会打开 **BigQuery 建议**窗格。在**降低 BigQuery 工作负载费用**下，点击**查看详情**。
4. 此时会出现一个建议列表，其中显示为当前项目或组织（具体取决于所选范围）生成的所有建议。找到具体化视图建议，然后点击**详细信息**。
5. 点击**在 BigQuery Studio 中查看**。此时会打开一个 SQL 编辑器，其中包含 `CREATE MATERIALIZED VIEW` DDL 语句。
6. 在提供的 `CREATE MATERIALIZED VIEW` 语句中，使用唯一的物化视图名称修改 `MATERIALIZED_VIEW` 占位符。
7. 运行 `CREATE MATERIALIZED VIEW` DDL 语句以创建建议的物化视图。

## 排查建议问题

**问题**：特定表未显示任何建议。

在以下情况下，可能不会显示物化视图建议：

* 在项目执行的查询作业中没有任何周期性查询句式。
* 周期性查询句式不满足[增量物化视图方面的限制](https://docs.cloud.google.com/bigquery/docs/materialized-views-create?hl=zh-cn#supported-mvs)，无法置于适合智能调优的物化视图中。
* 可能的物化视图会产生较高的维护费用。例如，源表经常通过数据操纵语言 (DML) 操作进行修改，因此物化视图将进行完全刷新，从而产生更多费用。
* 具有共同周期性句式的查询数量不足。
* 估算的每月节省微不足道（少于 1 个槽）。
* 由项目执行的查询作业已使用具体化视图。

## 价格

查看建议时，无需支付任何费用，也不会对工作负载性能产生负面影响。

通过创建具体化视图来应用建议时，可能会产生存储、维护和查询费用。如需了解详情，请参阅[具体化视图价格](https://docs.cloud.google.com/bigquery/docs/materialized-views-intro?hl=zh-cn#materialized_views_pricing)。




发送反馈

如未另行说明，那么本页面中的内容已根据[知识共享署名 4.0 许可](https://creativecommons.org/licenses/by/4.0/)获得了许可，并且代码示例已根据 [Apache 2.0 许可](https://www.apache.org/licenses/LICENSE-2.0)获得了许可。有关详情，请参阅 [Google 开发者网站政策](https://developers.google.com/site-policies?hl=zh-cn)。Java 是 Oracle 和/或其关联公司的注册商标。

最后更新时间 (UTC)：2026-03-19。




需要向我们提供更多信息？

[[["易于理解","easyToUnderstand","thumb-up"],["解决了我的问题","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["很难理解","hardToUnderstand","thumb-down"],["信息或示例代码不正确","incorrectInformationOrSampleCode","thumb-down"],["没有我需要的信息/示例","missingTheInformationSamplesINeed","thumb-down"],["翻译问题","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["最后更新时间 (UTC)：2026-03-19。"],[],[]]