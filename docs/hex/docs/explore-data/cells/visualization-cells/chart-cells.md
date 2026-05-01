On this page

# Chart cells

Chart cells let you visualize and explore the dataframes in a Hex project, without writing code.

tip

We released a new version of Chart cells in October of 2025. Chart cells created before this change are considered legacy and don't have some of the features mentioned in this doc, like support for semantic models or calculations. See [below](#legacy-charts) for info on how to upgrade legacy Chart cells.

info

* Users will need **Can Edit** [permissions](/docs/collaborate/sharing-and-permissions/sharing-permissions#what-permissions-are-there) to create and configure Chart cells.
* Users with **Can Explore** [permissions](/docs/collaborate/sharing-and-permissions/sharing-permissions#what-permissions-are-there) can explore from Chart cells in a published app.
* Users with **Can View App** permissions and higher can view Chart cells in published [Apps](/docs/share-insights/apps/apps-introduction).

Chart cells allows users to interactively explore and aggregate data, creating rich visualizations to share with app users.

Users can filter data with [chart interactions](#interactive-charts). Selecting points of interest in a chart returns a filtered dataframe, which can be referenced downstream in the project. Users with Can Explore access or higher to a published app can [explore from](/docs/share-insights/explore) Chart cells in the app.

[](/assets/medias/chart-cell-demo-be93fe99c0d49783cc661abd102cbb50.mp4)

## Adding a Chart cell[​](#adding-a-chart-cell "Direct link to Adding a Chart cell")

Add a chart cell to your project by:

1. Selecting **Chart** from the **Add cell** menu bar.

2. Choosing **Visualize in chart** in the dataframe menu.

## Configuring a Chart cell[​](#configuring-a-chart-cell "Direct link to Configuring a Chart cell")

1. Choose the data source (dataframe, semantic model, or warehouse table) you'd like to visualize with the **Data** input.
2. Choose the chart type in the **Type** input. The following chart types are supported:
   * Column charts
     + Grouped column
     + Stacked column
     + 100% stacked column
   * Bar charts
     + Grouped bar
     + Stacked bar
     + 100% stacked bar
   * Line & area charts
     + Line
     + Area
     + 100% stacked area
   * Other
     + Histogram
     + Scatter plot
     + Pie chart
3. Map the columns in your data source to the axes of your chart in the **Data** tab of the configuration panel
4. Apply styling as desired under the **Style** tab of the configuration panel

### Set time units for dates and timestamps[​](#set-time-units-for-dates-and-timestamps "Direct link to Set time units for dates and timestamps")

Date and timestamp columns can be truncated to a time period (e.g. hour, day, month) when added to a chart. When combined with an [aggregate function](#aggregating-data), this allows chart editors to interactively explore data at different time grains.

[](/assets/medias/truncating-dates-abebfc383434831b913ac47b4279e3d8.mp4)

If you've set a column's time unit to `Week`, a `Week start` option will be displayed in the column's configuration options. This lets you customize the start of the week to Monday or Sunday, depending on your business's needs. It's also possible to set the `Week start` setting when a chart has been set to facet by a week-truncated column.

### Top N[​](#top-n "Direct link to Top N")

Top N allows you to focus on your most significant data by displaying only the most important values in your visualizations. When working with datasets containing many unique categorical values, Top N helps you simplify your visualization by showing only the top (or bottom) data views based on a measure you select.

#### Using Top N[​](#using-top-n "Direct link to Using Top N")

Apply directly to a field with string scale type in charts (base-axis, color, facet) or pivots (row, column).

You can be found Top N in two places:

1. **Field entrypoint**

2. **Filter entrypoint**

When configuring Top N, you have several options:

* **Direction**: Choose between "top" or "bottom" values
* **Count**: Specify the number of values to display (N)
* **Rank by**: Select which measure to rank your values by
  + By default, ranks by the first y-axis measure (charts) or first values measure (pivots)
  + Can also rank by other measures or aggregated dimensions
* **Other bucket**: Toggle to include or exclude an "Other" category that combines all remaining values

Top N is applied after other aggregations and filters but before sorting and rendering. Multiple Top N configurations can be applied to different dimensions. For large datasets, Top N can significantly improve visualization performance.

### Aggregating data[​](#aggregating-data "Direct link to Aggregating data")

Hex's chart cells allow you to apply pre-built aggregates to your rows, such as `sum`, `count` and `max` functions. This provides an interactive way to explore data when grouping by different columns, without having to reshape the data upstream.

[](/assets/medias/aggregating-data-5d9bd4dbee65b3da16f79bafa05b722a.mp4)

info

The chart cell can take any size of dataframe or warehouse table as input, but can only render 10,000 data points per series *after* aggregates and time-truncation are applied.

Applying the aggregation within the chart cell (as opposed to performing aggregations upstream in the project logic) means the cell holds the row-level data, which makes the cell very useful to [explore from](/docs/share-insights/explore#where-to-use-explore) if it is included in a published app.

If you'd like to define a custom aggregate, you can do so by defining a [calculation](#calculations).

### Calculations[​](#calculations "Direct link to Calculations")

To add a calculation, click the **+** next to **Dimensions** or **Measures** in the field picker, or click **+** in the table below the exploration.

Function definitions, supported syntax, and rules can be found [here](/docs/explore-data/cells/calculations). Once a calculation is defined, it can be added to a visualization or table, like any other column.

Calculations that use [aggregation functions](/docs/explore-data/cells/calculations#-aggregates) like `Sum()`, `Count()` will be represented as measures, and can be used with grouped fields to compare statistics between categories, or over time.

If your cell has a join configured, calculations are currently only able to reference columns in the base table.

### Color by a column[​](#color-by-a-column "Direct link to Color by a column")

For most chart types, you can specify a column to break out and color your data by.

This column will be represented as entries in your legend, with each value rendered with a different color.

[](/assets/medias/color-by-2c7079acdd766508f416f2ab523f48c9.mp4)

### Change a column's scale type[​](#change-a-columns-scale-type "Direct link to Change a column's scale type")

Columns in a chart will render as one of three scale types: `string`, `number`, and `datetime`. The scale type is indicated via an icon in-line with the column name. These types are inherited from the source dataframe, and impact how the data is rendered.

At times, you may need to override a column's type to ensure your chart renders correctly. You can do this by selecting the scale type icon to switch it. This most commonly required when an upstream field is not correctly being interpreted as a datetime type.

Alternatively, consider changing the datatype upstream, for example by casting the column to a timestamp type with [dataframe SQL](/docs/explore-data/cells/sql-cells/sql-cells-introduction#dataframe-sql) (see [the DuckDB docs](https://duckdb.org/docs/sql/functions/dateformat) on timestamp functions for more information).

```
select  
  strptime(release_date, '%b %d %Y') < '2010-01-01' as release_date,  
  * exclude (release_date)  
from movies
```

This will ensure any cells downstream of your dataframe treat the data correctly.

### Ordering data[​](#ordering-data "Direct link to Ordering data")

The chart cell offers a number of options for ordering your data:

* Axes that plot a `number` or `datetime` variable can be sorted in ascending or descending order.
* Axes, colors, and facets that plot a `string` variable can be sorted:
  + In alphabetical order (ascending or descending).
  + In order from least to most (Y-axis ascending) or most to least (Y-axis descending).
  + In a custom sort order.

    [](/assets/medias/axis-sorting-0c04b4c5c549ccd44fe5f39e40927643.mp4)
* When using [multi-series charts](#plot-multiple-columns-in-a-chart-cell), series can be reordered via drag and drop interactions.

### Plot multiple columns in a Chart cell[​](#plot-multiple-columns-in-a-chart-cell "Direct link to Plot multiple columns in a Chart cell")

Hex offers three ways to plot multiple columns from a dataframe in a chart cell: adding data to a series, adding a series or adding a second Y-axis.

1. **Adding a column to a series:** This option is useful if the columns should be plotted as a set of grouped or stacked columns or bars, or stacked areas, although it can be used for line and scatter series as well. The series can be either colored or faceted by column.

[](/assets/medias/wide-input-9d5a3a540bd3a9698583466de222e22d.mp4)

2. **Adding a series:** This option is useful if the two columns should be plotted on the same axis, and share the same unit of measurement, for example comparing revenue and profit. Any number of columns in your dataframe can be added to a chart this way. To add a series, click the **+ Add series** button from the **Data** tab.

[](/assets/medias/add-series-d362931d3a02a392ae0b2371241978e7.mp4)

info

* A chart can have any number of line or scatter series, but at most one (vertical) column series and one area series.
* Series cannot currently be added to (horizontal) bar charts, pie charts or histograms, and such series cannot be added any chart with an existing series.

3. **Adding a second Y-axis:** This option is useful if the two columns should be plotted on different axes, and reflect different units of measurement, for example comparing revenue (in dollars) and number of orders. Only two axes (left and right) can be added to a chart, however each can have multiples series associated with the axis. To add an axis, click the **+ Add Y-axis** button from the **Data** tab.

[](/assets/medias/add-axis-45d0ad0432ae363547bb497689aa63a3.mp4)

Series can be reordered, or assigned to a separate axis, through a drag and drop interaction.

[](/assets/medias/reorder-series-46f68b4b9c9788b64964dec4bc9b132e.mp4)

tip

Only columns from the same dataframe can be plotted in chart cells. If you need to chart columns from different dataframes, consider joining the data upstream in Hex. Check out [this tutorial](https://app.hex.tech/hex-public/app/cab2dfd6-4b94-481c-a304-b924a8dd84cd/latest) for an example.

### Faceting[​](#faceting "Direct link to Faceting")

Use faceting in a Chart cell to split your chart into multiple subplots. At the bottom of the **Data** tab, open the **Faceting** toggle, and select a column or columns to facet by, vertically and/or horizontally.

[](/assets/medias/faceting-956a05b1494a45b71c4089338632b5a5.mp4)

If you are only faceting horizontally, you have the option to wrap the subplots, and set the number of subplot columns.

[](/assets/medias/facet-wrapping-2d0114c147b5d36757c99ab2a02d99a0.mp4)

info

Currently, faceting is not supported for multi-series charts, nor for facets that create more than 100 subplots.

### Adding data labels[​](#adding-data-labels "Direct link to Adding data labels")

To add labels to a chart, open the **Style** heading and toggle on **Data Labels**. Further styling customizations are possible once the setting is enabled.

For stacked bar, column, and area charts, **Total data labels** and **Per color data labels** can be enabled and customized separately.

### Reference lines[​](#reference-lines "Direct link to Reference lines")

Reference lines can be added to the X- and Y- axes of charts. To add a reference line to your chart, open the **Style** tab and click **+ Add** next to **Reference lines** under the **X-axis** or **Y-axis** section. After setting the reference value, optionally adjust the line color, style, and label settings.

Reference lines are not currently available on the Y-axes of dual Y-axis charts.

### Joins[​](#joins "Direct link to Joins")

info

Joins are only supported for cells that use a database table as their data source.

To join data from another database table, click the **+** in the upper right of the field picker, or the **+** **Join data** button at the bottom of the field picker. This will bring up the Data Browser, from which a target table can be selected.

In the modal, select the columns to perform the join on, and the unique key columns for each table. Hex will make a best guess at what the joining and unique columns should be, but will display a warning if no columns can be detected or if an issue is detected with your selected columns.

After **Join table** is clicked, Hex will perform a left join from the base table to the joining table. The columns from the joining table will appear in the field picker.

Once a table is selected, configure which columns to join on and the unique key columns for each table. Hex will make a best guess at what the joining and unique columns should be, but will display a warning if no columns can be detected or if there appear to be any errors with your selected columns. After **Join table** is clicked, Hex will perform a left join from the base table to the joining table.

Hex will detect duplicate rows that may arise as a result of the join. Using the unique keys specified, Hex can accurately calculate aggregations on the base and joining tables of one-to-one, many-to-one, one-to-many, and many-to-many joins.

If there is a mistake in the join logic, Hex will flag a warning in the join config. If you’d like to proceed with the join, acknowledging that the join may produce inaccurate results, click the down arrow from the greyed out **Join table** to force join.

### Outputting a Dataframe[​](#outputting-a-dataframe "Direct link to Outputting a Dataframe")

To reference the data from a Chart cell, users can select `Create output` from the bottom left corner of the cell. This will create a dataframe with a variable name that can be referenced downstream in the project.

By default, the dataframe returned will return data at the row-level grain, with grouped and aggregated rows at the beginning of the dataframe. To have the dataframe only return the grouped and aggregated rows, hover over the `explore_result` pill and toggle off **Include row-level data**.

## Interactive charts[​](#interactive-charts "Direct link to Interactive charts")

All Hex charts are interactive in both the Notebook view and Published App.

* Hovering over a legend will highlight the respective data series
* Clicking the legend, or clicking and dragging over a chart area, will select data points of interest
* Users can then choose to keep or remove the records of interest.
* Permissions permitting, users will be able to view the underlying data that makes up the records of interest - see [View Data](#view-data) below.

Editors can use the filtered records returned by a Chart cell downstream, enabling powerful drilldown workflows for App Users.

### In Notebook view[​](#in-notebook-view "Direct link to In Notebook view")

[](/assets/medias/logic-interactive-charts-4d962d383997b93023a800923293829e.mp4)

1. Interact with the chart to select data — a full list of interactions can be found [below](#visual-filtering-interactions).
2. Choose to keep or remove the selection.

Note that cell-level filters applied by Editors in Notebook view **do not** show up in the Published App, and therefore cannot be altered by a user viewing the Published App. App users are able to add additional filters via chart interactions.

If you choose to [return a dataframe](#outputting-a-dataframe), use the returned dataframe in downstream cells, such as [Table display cells](/docs/explore-data/cells/visualization-cells/table-display-cells) or another Chart cell.

### In Published Apps[​](#in-published-apps "Direct link to In Published Apps")

In a Published App, users can interact with the chart to add additional filters.

If downstream cells use the returned dataframe, these cells will also be updated by any filters that are added.

[](/assets/medias/app-interactive-charts-f3bfb093b6f0b810718556de55b66ac7.mp4)

Users can only add additional filters in a Published App, and cannot view or edit the cell-level filters applied by Editors in Notebook view.

#### View Data[​](#view-data "Direct link to View Data")

tip

This feature is available to workspaces on the [Teams tier](https://hex.tech/pricing/) and higher.

Users with [Can Explore permission](/docs/collaborate/sharing-and-permissions/project-sharing#can-explore) on a project will be able to **View data** in a published app to see the individual records that make up selected points from a visualization or a pivot.

From the resulting modal, users can download the data or [continue exploring](/docs/share-insights/explore).

[](/assets/medias/view-data-45868c17db8122df18bd1be46a2ac3b1.mp4)

In the published app, users can also click on the table icon in the upper right of the cell to view all underlying records of a chart or pivot.

Note that **View data** is not possible from [legacy pivot cells](/docs/explore-data/cells/transform-cells/pivot-cells#legacy-pivots). Upgrade your pivot cell to use **View data**.

### Chart interactions[​](#chart-interactions "Direct link to Chart interactions")

* Column charts
* Bar charts
* Line and Area charts
* Scatterplots
* Histograms

**Selecting a range along the X-axis**: Click and drag horizontally within the chart area to select multiple columns.

**Selecting individual columns or column segments**: Click an individual column (grouped column charts) or column segment (stacked bar charts) to select it. Use `shift + click` to add additional segments to your selection.

**Selecting a legend entry**: Click on a legend entry to highlight this series. Use `shift + click` to add additional series to your selection.

**Reset a selection**: Click within the chart area to reset your selection.

**Selecting a range along the Y-axis**: Click and drag vertically within the chart area to select multiple bars.

**Selecting individual bars or bar segments**: Click an individual bar (grouped bar charts) or bar segment (stacked bar charts) to select it. Use `shift + click` to add additional segments to your selection.

**Selecting a legend entry**: Click on a legend entry to highlight this series. Use `shift + click` to add additional series to your selection.

**Reset a selection**: Click within the chart area to reset your selection.

**Selecting a range along the X-axis**: Click and drag horizontally within the chart area to select multiple datapoints.

**Selecting a legend entry**: Click on a legend entry to highlight this series. Use `shift + click` to add additional series to your selection.

**Reset a selection**: Click within the chart area to reset your selection.

**Selecting a range of data points**: Click and drag within the chart area to select a range of point in any direction. If an aggregate is applied to the Y-axis value, this will create a horizontal range.

**Selecting a legend entry**: Click on a legend entry to highlight this series. Use `shift + click` to add additional series to your selection.

**Reset a selection**: Click within the chart area to reset your selection.

**Selecting a range along the X-axis**: Click and drag horizontally within the chart area to select a range of along the X-axis.

**Reset a selection**: Click within the chart area to reset your selection.

## Chart style configurations[​](#chart-style-configurations "Direct link to Chart style configurations")

### Customize chart colors[​](#customize-chart-colors "Direct link to Customize chart colors")

Hex's chart cells provide fine-grained options for choosing colors.

[](/assets/medias/custom-chart-colors-aebf783d91b0165f5a48e5a052eee8bf.mp4)

To customize the colors of your chart:

1. Open the **Style** heading, tab of the chart editor open the **Color** menu. The default color for each series for each bar, line, area or point will be shown.
2. Click into the current color to customize it. You can choose a color from:
   * **Palette**: The currently active palette. Workspaces on the Team and Enterprise plan can update the palette used for charts by creating a [custom color palette](/docs/administration/workspace_settings/workspace-custom-styling#custom-chart-color-palettes) and setting it as the active palette.
   * **Custom**: Use a color from the provided swatches, or set a custom color. To set a custom color, click into the color code, and update it to your custom value. Color values can be formatted as hex strings, such as `#F5C0C0` or `AD8EB6`, or as [CSS color names](https://developer.mozilla.org/en-US/docs/Web/CSS/named-color), such as `mediumpurple`. You can also click on the color swatch to open and select a shade from the color picker.
3. To reset your colors to the default palette and ordering, hover over the **Color** heading, and select **Reset colors**.

### Additional customizations[​](#additional-customizations "Direct link to Additional customizations")

The **Style** tab also lets you customize:

* **Column**, **Bar**, **Line**, **Area** or **Point style**: Configure options for colors, order and opacity.
* **Chart and axis labels**: Configure the labels rendered on your chart. By default, this map to the column names configured in the **Data** tab.
* **Axis style**: Configure the style, tick count, and minimum and maximum values of your X- and Y-axes.
* **Legend** (if applicable): Configure whether a legend is displayed, and the position on the chart.
* **Tooltip**: Configure whether a tooltip is displayed. By default, the tooltip will show the values on the chart. You can further customize the tooltip values by adding custom tooltip entries with the **+ Tooltip** button.

### Scrollable charts[​](#scrollable-charts "Direct link to Scrollable charts")

By default, charts will fit the height and width of the cell size, but it is possible to override this and make charts scrollable. This is particularly useful for charts with long categorical axes. To enable scrolling, open the **Style** tab in the chart configuration panel and toggle "Fit width" or "Fit height" off (whether the width or height is fixed will depend on the chart type).

Resize the cell in the app builder in order to fix the size of the viewport that the user will see in the published app.

[](/assets/medias/scrollable-gif-94238deada6954f16ea3524721e5d675.mp4)

### Chart style copy & paste[​](#chart-style-copy--paste "Direct link to Chart style copy & paste")

It's possible to copy all of a chart's styling to your clipboard and paste matching styles to a second target chart. Styles can be pasted both within and across projects.

[](/assets/medias/chart-style-transfer-3580827e86e97d25d4a7ff6b05ab2931.mp4)

The underlying data represented in the target chart will never change when styles are pasted. The style configurations are compared between the source and the target cell, so only "applicable" styles are transferred between cells. See the rules below to understand how Hex determines which styles to transfer over from the source to the target cell:

* General, data-agnostic styles like legend position, fit-width, and font size are always transferred.
* Data-dependent styles such as axis labels and bounds, and number formatting are only transferred if the relevant data matches¹:
  + X-axis, horizontal and vertical facets: styles will only be transferred if there is a data match.
  + Y-axes: styles will only be transferred if at least one series in the source cell has a data match to one series in the target on the same side (e.g. to copy the left-side Y-axis label and format, at least one series mapped to the left Y-axis in both the source and the target must have a data match).
  + Per series:
    - Line dash, data labels, etc: transferred from the first series with a Y-axis data match.
    - Color styles: copied from the first series with a Color-by data match.

¹Hex considers two fields to be a "data match" when the field name, aggregation (if applicable), and time unit (if applicable) between the source and the target cell are all the same. For example, if the source cell and target cell both have a field called `order_date` on the X-axis that are both truncated to `Month`, this would be considered a data match (even if the fields trace back to two different dataframes).

If you want to undo the styles you've recently pasted to the target chart, you can use the "Undo" button in the resulting toast. Alternatively, you can use `cmd` + `z` to undo the pasted styles.

## Chart cell timezones[​](#chart-cell-timezones "Direct link to Chart cell timezones")

If one or both of your chart axes uses a timestamp column, Hex will convert timestamps to a target timezone, rendering them in this timezone. In increasing precedence, this target timezone is set by the workspace timezone, the project timezone, and the app session timezone. See [this docs page](/docs/administration/workspace_settings/overview#workspace-timezone) for more information.

## Legacy charts[​](#legacy-charts "Direct link to Legacy charts")

tip

We upgraded our chart cell in October 2025. Chart cells created before this upgrade are considered legacy.

Chart cells created before October 2025 will still run, but are considered legacy and have a "Legacy" tag that is only visible in the notebook.

New charts hold many upgraded features including the ability to use semantic models, the ability to perform no-code joins on warehouse tables, calculations, integration with our AI agents, top N filtering capabilities, and more. Legacy Chart cells will not receive any of these features nor future ones - to use these features in your existing Chart cells, you can upgrade the cell.

### Upgrade legacy Chart cells[​](#upgrade-legacy-chart-cells "Direct link to Upgrade legacy Chart cells")

To upgrade a legacy Chart cell, hover over the "Legacy" tag to see an option to upgrade the cell. The existing chart configuration, styling, and location in the app builder will be maintained in the upgraded version. If you want to reverse the upgrade, you can `cmd`+`z` to undo.

Users will be able to temporarily add new legacy chart cells via the **More** menu in the add-cell bar.

Beginning in October 2025, it is also no longer possible to create visualizations directly within SQL cells. Existing visualizations that have been configured within SQL cells will continue to run, but are considered legacy and do not have any of the upgraded features described above. If you'd like to use the upgraded features in your existing SQL cell visualizations, hover over the "Legacy" tag to see an option to create a new Chart cell based on the existing one.

#### On this page

* [Adding a Chart cell](#adding-a-chart-cell)
* [Configuring a Chart cell](#configuring-a-chart-cell)
  + [Set time units for dates and timestamps](#set-time-units-for-dates-and-timestamps)
  + [Top N](#top-n)
  + [Aggregating data](#aggregating-data)
  + [Calculations](#calculations)
  + [Color by a column](#color-by-a-column)
  + [Change a column's scale type](#change-a-columns-scale-type)
  + [Ordering data](#ordering-data)
  + [Plot multiple columns in a Chart cell](#plot-multiple-columns-in-a-chart-cell)
  + [Faceting](#faceting)
  + [Adding data labels](#adding-data-labels)
  + [Reference lines](#reference-lines)
  + [Joins](#joins)
  + [Outputting a Dataframe](#outputting-a-dataframe)
* [Interactive charts](#interactive-charts)
  + [In Notebook view](#in-notebook-view)
  + [In Published Apps](#in-published-apps)
  + [Chart interactions](#chart-interactions)
* [Chart style configurations](#chart-style-configurations)
  + [Customize chart colors](#customize-chart-colors)
  + [Additional customizations](#additional-customizations)
  + [Scrollable charts](#scrollable-charts)
  + [Chart style copy & paste](#chart-style-copy--paste)
* [Chart cell timezones](#chart-cell-timezones)
* [Legacy charts](#legacy-charts)
  + [Upgrade legacy Chart cells](#upgrade-legacy-chart-cells)