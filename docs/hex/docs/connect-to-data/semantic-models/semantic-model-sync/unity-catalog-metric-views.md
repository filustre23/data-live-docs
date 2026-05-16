On this page

# Databricks Unity Catalog Metric Views

info

* Unity Catalog Metric Views is currently in **beta**.
* Unity Catalog Metric Views are refreshed with Data connection schema refreshes, but syncing of UC Metric Views is not yet supported.
* Reach out to [[email protected]](/cdn-cgi/l/email-protection#21525451514e5355614944590f55444249) to learn more or [request a demo](https://hex.tech/request-a-demo/).

## Overview[​](#overview "Direct link to Overview")

Unity Catalog (UC) Metric Views are Databricks’ native semantic modeling layer. They provide a centralized way to define and manage consistent business logic in the form of measures and dimensions, which can be used across tools (including Hex!).

For more information, see the [Databricks documentation](https://docs.databricks.com/aws/en/metric-views/).

You can browse UC Metric Views directly in the [Data browser](/docs/explore-data/data-browser) and add them to notebooks for analysis. This allows for on-rails data exploration using governed definitions, while still giving data teams the flexibility to dive deeper when needed.

## Browse Metric Views[​](#browse-metric-views "Direct link to Browse Metric Views")

1. First, define a metric view in [Unity Catalog](https://docs.databricks.com/aws/en/metric-views/create).
2. Create a Databricks [Data connection](/docs/connect-to-data/data-connections/data-connections-introduction) in Hex.
3. Open the [Data browser](/docs/explore-data/data-browser) of your Data connection.
4. Navigate to the metric view you want to explore (you can search by name).
5. Preview the available measures and dimensions, including metadata.

You can then add a metric view directly to your project as a SQL cell by selecting **Query**.

UC Metric Views get updated via Data connection schema refreshes.

## Query Metric Views in SQL Cells[​](#query-metric-views-in-sql-cells "Direct link to Query Metric Views in SQL Cells")

When adding a metric view to a project, Hex will generate a SQL cell that references all measures by default.

You can then edit the query to include only the measures or dimensions relevant to your analysis. For example:

```
select `STAGE_1_DATE`, `FIRST_TOUCH_SOURCE`, MEASURE(`OPPORTUNITY_ARR`) as `OPP_ARR`  
from `main`.`sales_and_marketing`.`sales_marketing_metric_view`  
group by 1,2
```

## Use Metric Views in Analysis[​](#use-metric-views-in-analysis "Direct link to Use Metric Views in Analysis")

Metric views can only be queried directly from SQL cells.

If you want to use a metric view in other cell types, follow this workflow:

1. Query the metric view in a SQL cell.
2. Use the dataframe output from that SQL cell in other cell types. For example: as the source for an [Explore cell](/docs/share-insights/explore), to provide options for an [input parameter](/docs/explore-data/cells/input-cells/input-cells-introduction), or for further manipulation in a [Python cell](/docs/explore-data/cells/python-cells).

This workflow keeps your analysis grounded in governed definitions, while making metric view data available for both no-code exploration and full-code development in Hex.

#### On this page

* [Overview](#overview)
* [Browse Metric Views](#browse-metric-views)
* [Query Metric Views in SQL Cells](#query-metric-views-in-sql-cells)
* [Use Metric Views in Analysis](#use-metric-views-in-analysis)