On this page

# Develop your notebook

The Notebook view is where you query, transform, visualize, and explore your data.

## Develop your analysis[​](#develop-your-analysis "Direct link to Develop your analysis")

Once you've created your project, you're ready to start developing the [Notebook view](/docs/explore-data/notebook-view/develop-your-notebook).

### Start with SQL or Python[​](#start-with-sql-or-python "Direct link to Start with SQL or Python")

Hex projects typically begin by adding a [SQL cell](/docs/explore-data/cells/sql-cells/sql-cells-introduction) or [Python cell](/docs/explore-data/cells/python-cells) that pulls data from a warehouse connection, CSV file, or API. Add a single cell, or start with a template for a little extra structure.

### Choose your data source[​](#choose-your-data-source "Direct link to Choose your data source")

Browse available [data connections](/docs/connect-to-data/data-connections/data-connections-introduction) in the **Data browser** sidebar. You can also [upload files](/docs/connect-to-data/upload-files) as a data source from the **Files** tab in the left sidebar.

### Bring data into your project[​](#bring-data-into-your-project "Direct link to Bring data into your project")

To quickly bring data into your project from a data connection, click on the data connection from the **Data sources** sidebar, and click **Query** next to any table name. This will automatically create and run a SQL cell with a `select *` limited to 100 rows.

You can also add a SQL cell from the **Add cell bar** at the bottom of your Notebook view, and write your own query from scratch. Click the **Run** button in the upper right of the cell (or `cmd-return`) to run the cell.

If you're querying an [uploaded CSV file](/docs/connect-to-data/upload-files), you'll need to set your SQL cell's [data source](/docs/explore-data/cells/sql-cells/sql-cells-introduction#dataframe-sql) dropdown to "dataframes".

### Quickly visualize and transform your data[​](#quickly-visualize-and-transform-your-data "Direct link to Quickly visualize and transform your data")

[SQL cells](/docs/explore-data/cells/sql-cells/sql-cells-introduction) come with built-in display tables and charts, or you can add new cells to [visualize](/docs/explore-data/cells/visualization-cells/chart-cells) and [transform](/docs/explore-data/cells/transform-cells/pivot-cells) your data in multiple ways.

### Reference your query result[​](#reference-your-query-result "Direct link to Reference your query result")

SQL cell outputs are stored as a dataframe, which is a standard table format with rows and columns. Once created, a dataframe becomes a data source in your project that you can query and reference in downstream cells.

[Python cell](/docs/explore-data/cells/python-cells) outputs are similarly stored as variables, including dataframes, which can be referenced in downstream cells.

### Using the Notebook Agent[​](#using-the-notebook-agent "Direct link to Using the Notebook Agent")

The [Notebook Agent](/docs/explore-data/notebook-view/notebook-agent) offers a natural language experience to assist with code generation and exploratory analysis within Hex projects. Within any Hex project, you can access this from the **Ask a question** modal in the bottom-right corner of the Notebook.

[](/assets/medias/ask-sidebar-to-edit-query-c0425c3c734830f202a8de4a5ddfe160.mp4)

#### On this page

* [Develop your analysis](#develop-your-analysis)
  + [Start with SQL or Python](#start-with-sql-or-python)
  + [Choose your data source](#choose-your-data-source)
  + [Bring data into your project](#bring-data-into-your-project)
  + [Quickly visualize and transform your data](#quickly-visualize-and-transform-your-data)
  + [Reference your query result](#reference-your-query-result)
  + [Using the Notebook Agent](#using-the-notebook-agent)