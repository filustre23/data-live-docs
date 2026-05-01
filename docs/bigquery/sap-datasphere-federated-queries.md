* [Home](https://docs.cloud.google.com/?hl=zh-cn)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-cn)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-cn)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-cn)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-cn)

发送反馈



使用集合让一切井井有条

根据您的偏好保存内容并对其进行分类。

# SAP Datasphere 联合查询

**预览版**

此产品或功能 受[服务专用条款](https://docs.cloud.google.com/terms/service-terms?hl=zh-cn#1)的约束。
非正式版产品和功能“按原样”提供，可能只能获得有限的支持。
如需了解详情，请参阅[发布阶段说明](https://cloud.google.com/products/?hl=zh-cn#product-launch-stages)。

**注意：**如需获取对此预览版功能的支持或提供反馈，请联系 [bq-sap-federation-support@google.com](mailto:bq-sap-federation-support@google.com)。

作为数据分析师，您可以使用联合查询从 BigQuery 查询 SAP Datasphere 中的关系型数据。

借助 BigQuery SAP Datasphere 联合，BigQuery 能够实时查询驻留在 SAP Datasphere 中的数据，而无需复制或移动数据。

如需在 SAP Datasphere 中运行 SQL 查询，请在 `EXTERNAL_QUERY` 函数中指定 BigQuery 中的该 SQL 查询。随后，系统会将结果从 SAP Datasphere 转移到 BigQuery。

## 限制

* 您只能查询[公开供使用](https://help.sap.com/docs/SAP_DATASPHERE/43509d67b8b84e66a30851e832f66911/d7d56284bb5148c887ac4054689bfbca.html?locale=en-US)的关系型视图。通过 `EXTERNAL_QUERY` 联合的查询将无法访问 SAP Datasphere 中的其他对象。
* 如果直接在 SAP Datasphere 中执行联合查询，其延迟时间可能会明显长于相同的查询。
* 在给定项目中使用 SAP Datasphere 连接的第一个查询可能需要超过一分钟的运行时间。
* SAP Datasphere 不支持其他 [SQL 下推](https://docs.cloud.google.com/bigquery/docs/federated-queries-intro?hl=zh-cn#sql_pushdowns)。
* SAP Datasphere SQL 查询必须指定包含函数结果的列的别名。
* 当查询项目中 Compute Engine API 的使用受 [VPC Service Controls](https://docs.cloud.google.com/vpc-service-controls/docs/overview?hl=zh-cn) 的限制时，联合查询将失败。

## 准备工作

确保您的 BigQuery 管理员已[创建 SAP Datasphere 连接](https://docs.cloud.google.com/bigquery/docs/connect-to-sap-datasphere?hl=zh-cn)并与您[共享](https://docs.cloud.google.com/bigquery/docs/connect-to-sap-datasphere?hl=zh-cn#share_connections)。

### 所需的角色

如需获得查询 SAP Datasphere 所需的权限，请让管理员为您授予项目的 [BigQuery Connection User](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-cn#bigquery.connectionUser) (`roles/bigquery.connectionUser`) IAM 角色。如需详细了解如何授予角色，请参阅[管理对项目、文件夹和组织的访问权限](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-cn)。

您也可以通过[自定义角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-cn)或其他[预定义角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-cn#predefined)来获取所需的权限。

## 查询数据

如需将联合查询从 GoogleSQL 查询发送到 SAP Datasphere，请使用 [EXTERNAL\_QUERY 函数](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/federated_query_functions?hl=zh-cn#external_query)。

以下示例是一个联合查询，该查询联接 SAP Datasphere 中名为 `ORDERS` 的表和 BigQuery 中名为 `mydataset.customers` 的表。

```
SELECT c.customer_id, c.name, rq.first_order_date
FROM mydataset.customers AS c
LEFT OUTER JOIN EXTERNAL_QUERY(
  'connection_id',
  '''SELECT CUSTOMER_ID, MIN(ORDER_DATE) AS first_order_date
     FROM ORDERS
     GROUP BY CUSTOMER_ID''') AS rq
  ON rq.customer_id = c.customer_id
GROUP BY c.customer_id, c.name, rq.first_order_date;
```

## 查看 SAP Datasphere 表架构

以下示例使用 [EXTERNAL\_QUERY 函数](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/federated_query_functions?hl=zh-cn#external_query)从 SAP Datasphere 中的 `SYS` 架构中检索数据库元数据。

```
-- List all views in a schema.
SELECT * FROM EXTERNAL_QUERY(
  'connection_id',
  '''SELECT VIEW_NAME FROM SYS.VIEWS
     WHERE SCHEMA_NAME = 'MY_SCHEMA'''');
```

```
-- List all columns in a view.
SELECT * FROM EXTERNAL_QUERY(
  'connection_id',
  '''SELECT COLUMN_NAME, DATA_TYPE_NAME
     FROM SYS.VIEW_COLUMNS
     WHERE SCHEMA_NAME = 'MY_SCHEMA' AND
           VIEW_NAME = 'my_view'
     ORDER BY POSITION''');
```

## 价格

运行联合查询的费用取决于三个因素：

* 在 SAP Datasphere 中执行查询的计算费用。
* 将查询结果从 SAP Datasphere 转移到 BigQuery 的带宽费用。
* 在 BigQuery 中执行查询的计算费用。

任何与 SAP Datasphere 相关的费用取决于您使用的 SAP 服务类型。为了限制带宽费用，我们建议您在 `EXTERNAL_QUERY` 中编写查询，使其排除所有不需要计算最终结果的列和行。

在 BigQuery 中运行联合查询不会产生额外费用。如需详细了解 BigQuery 价格，请参阅[价格](https://cloud.google.com/bigquery/pricing?hl=zh-cn)。

## 后续步骤

* 了解[联合查询](https://docs.cloud.google.com/bigquery/docs/federated-queries-intro?hl=zh-cn)。
* 了解[不支持的数据类型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/federated_query_functions?hl=zh-cn#unsupported_data_types)。




发送反馈

如未另行说明，那么本页面中的内容已根据[知识共享署名 4.0 许可](https://creativecommons.org/licenses/by/4.0/)获得了许可，并且代码示例已根据 [Apache 2.0 许可](https://www.apache.org/licenses/LICENSE-2.0)获得了许可。有关详情，请参阅 [Google 开发者网站政策](https://developers.google.com/site-policies?hl=zh-cn)。Java 是 Oracle 和/或其关联公司的注册商标。

最后更新时间 (UTC)：2026-03-19。




需要向我们提供更多信息？

[[["易于理解","easyToUnderstand","thumb-up"],["解决了我的问题","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["很难理解","hardToUnderstand","thumb-down"],["信息或示例代码不正确","incorrectInformationOrSampleCode","thumb-down"],["没有我需要的信息/示例","missingTheInformationSamplesINeed","thumb-down"],["翻译问题","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["最后更新时间 (UTC)：2026-03-19。"],[],[]]