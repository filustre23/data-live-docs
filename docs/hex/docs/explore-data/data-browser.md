On this page

# Data browser

Explore and preview data from the homepage or within a project.

info

* Users will need **Can Edit** [permissions](/docs/collaborate/sharing-and-permissions/sharing-permissions#what-permissions-are-there).

Use the Data browser to view the schemas, tables, and [semantic projects](/docs/connect-to-data/semantic-models/semantic-model-sync/intro) available in your data connections. Explore by searching for column or table names, previewing data, and understanding datatypes.

Users can access the Data browser from the homepage, or from within a project.

[](/assets/medias/data-browser-homepage2-c65980a5bc4054d6b6369f7e1c7cccee.mp4)

### Using the Data browser within a project[​](#using-the-data-browser-within-a-project "Direct link to Using the Data browser within a project")

Users can open the **Data browser** tab to access the Data browser within a project. Hovering over a table name will display options to preview or query the data. Clicking the eye icon will open a wider view of the Data browser with a 100-row preview of the table's results.

[](/assets/medias/previewing-data-project-8d4d2e4ac566feb81d40cf8fad0937bf.mp4)

Users can also open this wider Data browser view by clicking on the Data browser icon in the add cell bar.

It is also possible to access the Data browser for a particular connection by hovering over the data source in a SQL cell and selecting **Browse schema**. This will bring you to the data connection in the Data browser.

### Semantic projects in the data browser[​](#semantic-projects-in-the-data-browser "Direct link to Semantic projects in the data browser")

Any semantic projects that have been configured on a data connection are available via the Data browser. Expand the data browser from the left sidebar, and open the **Data models** tab at the top. From here, you can search your projects and models, and view the measures and dimensions of your models. To explore, select **+ Add to project** which will add a [chart cell](/docs/explore-data/cells/visualization-cells/chart-cells) referencing this model in your Hex project.

[](/assets/medias/data-browser-semantic-models-9320a49132880096a3fd5009d2c59361.mp4)

### Schema metadata[​](#schema-metadata "Direct link to Schema metadata")

Any schema metadata configured in your warehouse, [dbt](/docs/connect-to-data/data-connections/dbt-integration), or [from within Hex](#descriptions) will be displayed in the Data browser.

If the selected table is part of a dbt model or defined as a source in dbt, you will see the model's most recent job execution date, source freshness, and the status of any tests configured on the model.

[](/assets/medias/metadata-in-data-browser-f898520ad6518bd04c44ee42d0dc991e.mp4)

### Recently used & favorites[​](#recently-used--favorites "Direct link to Recently used & favorites")

Access the **Recently used** tab at the top of the Data browser to preview or query your recently used tables.

Users can also add favorite schemas and tables by clicking the star icon next to the schema or table name. These favorited items can be accessed via the **Favorites** tab at the top of the Data browser. These favorites are unique to each user and persist across projects. When searching in the schema browser, it's possible to search all contents of the Data browser, or just within your favorited items.

### Data browser search[​](#data-browser-search "Direct link to Data browser search")

Search the contents of your data connection in the search bar at the top of the Data browser. Users can choose to search all contents within the Data browser, or just within their favorited content. Search results can also be filtered to one type of database object by preceding your search with `database:`, `schema:`, or `table:`.

tip

Hover over a table in a SQL cell query and select **Search for table in data browser** to launch a search.

### Link to data objects[​](#link-to-data-objects "Direct link to Link to data objects")

Click the link icon next to a database, schema, or table name to copy a link to the specific data object to your clipboard. Sending this link to another Hex user will open their Data browser to the intended data object.

### Shortcuts[​](#shortcuts "Direct link to Shortcuts")

#### Within a project[​](#within-a-project "Direct link to Within a project")

When viewing the Data browser from within a project, hovering over a table will show options to preview or query the table, and a three-dot menu holds additional shortcuts.

**Preview**: Launch the Data browser modal displaying a 100 row preview of the selected table.

**Query**: Open a SQL cell querying the selected table with a `limit 100` clause.

**Copy qualified table name**: Copy the qualified table name including the database, schema and table.

**Copy all columns**: Copy a SQL query that selects all columns from the selected table to your clipboard. This shortcut can be useful if you need to select all but a few columns.

**Search within table**: Launch a Data browser search filtered to the selected table.

#### From the homepage[​](#from-the-homepage "Direct link to From the homepage")

When selecting a table or semantic model in the Data browser on the homepage, Explorers and Editors have the option to start a new exploration with the **Explore** button in the upper right corner of table previews. Editors have the additional option to open tables in a variety of cell types via the **+ Open in project as...** and open semantic projects as a [Chart cell](/docs/explore-data/cells/visualization-cells/chart-cells) in a new Hex project.

#### Descriptions[​](#descriptions "Direct link to Descriptions")

[](/assets/medias/updating-description-b6de0a6d258234bae6e8e60267f0ffe7.mp4)

Database, schema, table, and column descriptions are inherited from your database and dbt and displayed in the Data browser. If desired, additional descriptions can be added by clicking **Add an additional description...**.

Detailed descriptions of your data connections databases, schemas, tables, and columns help Hex's AI agents identify the purpose of these various data objects. Descriptions can also be used to help provide the AI agents with more context about how to use the data in these data assets, therefore improving the quality of SQL generations.

For example, adding a description to your `dim_users` table that says *“No internal employees are contained in the table”* can help Hex's AI agents (as well as Hex users) understand that this table is best used in queries related to external users. It can also be helpful to describe the formatting in a given column; for example, a description on a `customer_name` column that reads *"Names are formatted as 'Last name, First name'"*

All descriptions may be provided to Hex's AI agents for the purpose of improving responses.

#### Exclusion and endorsement[​](#exclusion-and-endorsement "Direct link to Exclusion and endorsement")

[](/assets/medias/ai-exclude-5c1c8ff1245ef21e2e97b5534c7ebad5.mp4)

Admins and Managers can choose to include, exclude, or endorse data objects for use by Hex's AI agents.

All data objects are **Included** by default. Admins and Managers can choose to **Exclude** certain objects so they are omitted from the agent's default discovery and generation context (for example, when the agent searches metadata or proposes queries). Exclusion does not replace warehouse permissions—users can still query data they can access, and agents may still use data if a user explicitly references it (such as via @mention). If an object is excluded, all of its children will automatically also be excluded. Admins and Managers can also **Endorse** data objects that should be preferred by the agents.

For example, `STG_` tables commonly contain similar dimensions to those downstream, but are not production-ready. Instead, `DIM_` tables are much more relevant and thus should be **Endorsed**. This feature helps Hex's agents understand these preferences.

info

For more details, review [**Context Management**](/docs/agent-management/context-management) to learn more about curating your workspace and data for AI.

### Refresh the Data browser[​](#refresh-the-data-browser "Direct link to Refresh the Data browser")

The contents of the Data browser are generated upon creation of a data connection, and will be cached until the Data browser is manually refreshed. To refresh, click the refresh icon next to the data connection name at the top of the Data browser.

tip

Hex Admins can [schedule automated refreshes](/docs/connect-to-data/data-connections/data-connections-introduction#schedule-automated-refreshes-for-the-data-browser) for each workspace Data connection.

The 100-row table previews displayed in the Data browser can be refreshed individually by clicking on the circular arrows at the upper right of the table preview.

#### On this page

* [Using the Data browser within a project](#using-the-data-browser-within-a-project)
* [Semantic projects in the data browser](#semantic-projects-in-the-data-browser)
* [Schema metadata](#schema-metadata)
* [Recently used & favorites](#recently-used--favorites)
* [Data browser search](#data-browser-search)
* [Link to data objects](#link-to-data-objects)
* [Shortcuts](#shortcuts)
* [Refresh the Data browser](#refresh-the-data-browser)