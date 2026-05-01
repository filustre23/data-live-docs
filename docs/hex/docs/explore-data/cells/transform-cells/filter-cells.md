On this page

# Filter cells

Filter cells allows editors and app users to interactively filter data from your dataset, in a UI-first way.

info

* Users will need **Can Edit** [permissions](/docs/collaborate/sharing-and-permissions/sharing-permissions#what-permissions-are-there) to create and edit Filter cells.
* Users with **Can View App** permissions and higher can interact with Filter cells in published [Apps](/docs/share-insights/apps/apps-introduction).

A filter cell takes a dataframe or query result as an input, filters it based on your configurations, and returns a result that can be used downstream in your Hex project. The configured filters can also be added to an app, allowing app users to interact with the filters.

[](/assets/medias/filter_cell-ee270d90ac8f836d6571a0be3a9b46b6.mp4)

## Using Filter cells[​](#using-filter-cells "Direct link to Using Filter cells")

1. Create a Filter cell by hovering over "More", and then selecting "Filter".

2. Choose a source dataframe or query result, and then configure the filters to select your data. The available filters will vary depending on your data type. Note that:
   * You can configure multiple filters and filter groups
   * Text filters are case-insensitive by default. This can be adjusted using the "Aa" icon.
   * By default, you are choosing which rows to keep. You can also choose to remove these rows by adjusting the "Keep rows" option in the footer to "Remove rows".
3. Optionally view the compiled SQL from the icon in the top right hand corner.
4. Use the filter result in downstream cells, such as [Table Display](/docs/explore-data/cells/visualization-cells/table-display-cells), [Chart cells](/docs/explore-data/cells/visualization-cells/chart-cells) and [Pivot cells](/docs/explore-data/cells/transform-cells/pivot-cells). Note that filter cells do not show the results by default.

## Considerations when filtering a query result[​](#considerations-when-filtering-a-query-result "Direct link to Considerations when filtering a query result")

Filter cells work seamlessly with query results (i.e. the result a SQL cell that returns data in [query mode](/docs/explore-data/cells/sql-cells/sql-cells-introduction#query-mode)), running the compiled SQL against your warehouse rather than filtering a dataframe in memory. This allows you to work with large datasets in Hex by leveraging the compute engine of your data warehouse.

When filtering a query result:

* In Logic view, the cell needs to be rerun after changing a configuration via the **Run** button, or using `cmd + enter`. This helps avoid unnecessary queries being executed against your data warehouse.
* Value suggestions are disabled, to avoid expensive queries being executed against your data warehouse.
* By default, when filtering a query result, the cell returns another query result. You can adjust this by editing the filter result type.

## Duplicate Filter cells as SQL[​](#duplicate-filter-cells-as-sql "Direct link to Duplicate Filter cells as SQL")

Filter cells can be duplicated as SQL cells, allowing you to adjust the SQL to suit your needs.

## Add Filter cells to an App[​](#add-filter-cells-to-an-app "Direct link to Add Filter cells to an App")

To add a filter cell to an app, use the "Add to app" shortcut in the top-right-hand corner of the cell.

When viewing your project from the App builder view, you can configure whether an app user can configure all parts of the filter (including editing, adding, removing and rearranging filters), or just edit the value input of each filter.

#### On this page

* [Using Filter cells](#using-filter-cells)
* [Considerations when filtering a query result](#considerations-when-filtering-a-query-result)
* [Duplicate Filter cells as SQL](#duplicate-filter-cells-as-sql)
* [Add Filter cells to an App](#add-filter-cells-to-an-app)