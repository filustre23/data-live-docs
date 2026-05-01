On this page

# dbt Semantic layer cells (legacy)

dbt Semantic layer cells allow users of all technical levels to pull in data backed by consistent, governed metrics in their Semantic layer, and be confident in their results.

info

* This is a legacy integration. Check out our new [integration with dbt MetricFlow](/docs/connect-to-data/semantic-models/semantic-model-sync/dbt-metricflow) to learn more about exploring your models in Hex.
* Users will need **Can Edit** [permissions](/docs/collaborate/sharing-and-permissions/sharing-permissions#what-permissions-are-there) to create and reference dbt Semantic layer cells.

## Prerequisites[​](#prerequisites "Direct link to Prerequisites")

To use a dbt Semantic layer cell, first ensure:

* You have enabled the dbt Server integration as outlined [here](/docs/connect-to-data/data-connections/dbt-integration#dbt-server-integration).
* You are using dbt v1.6 or higher. (Legacy versions will only be supported until dbt deprecates them.)

## Configure dbt Semantic layer cells[​](#configure-dbt-semantic-layer-cells "Direct link to Configure dbt Semantic layer cells")

First, add a dbt Semantic layer cell to your project (dbt Semantic layer cells are grouped with the other **Data** type cells). Then, select a metric of interest via the **+Add** button on the left of the cell. Multiple metrics can be added, if desired.

From here, you can specify the time grain and start/end dates for the returned data. You can also specify additional dimensions which are compatible with the selected metric(s). Optionally, you can configure secondary calculations like a period-over-period calculation or running total. Once you have configured the dbt Semantic layer cell, execute the cell to retrieve the results of the query.

## Use dbt Semantic layer results in downstream cells[​](#use-dbt-semantic-layer-results-in-downstream-cells "Direct link to Use dbt Semantic layer results in downstream cells")

dbt Semantic layer cells return a pandas DataFrame with a default naming scheme of `metric_result_n`. This DataFrame can be used in downstream cells anywhere a pandas DataFrame can be used. For example, dbt Semantic layer cell results can be:

* visualized in a [chart cell](/docs/explore-data/cells/visualization-cells/chart-cells)
* transformed in a [pivot](/docs/explore-data/cells/transform-cells/pivot-cells)
* used in a [filter cell](/docs/explore-data/cells/transform-cells/filter-cells)
* reshaped with [DataFrame SQL](/docs/explore-data/cells/sql-cells/sql-cells-introduction#dataframe-sql)
* used as an input to [python cells](/docs/explore-data/cells/python-cells)

#### On this page

* [Prerequisites](#prerequisites)
* [Configure dbt Semantic layer cells](#configure-dbt-semantic-layer-cells)
* [Use dbt Semantic layer results in downstream cells](#use-dbt-semantic-layer-results-in-downstream-cells)