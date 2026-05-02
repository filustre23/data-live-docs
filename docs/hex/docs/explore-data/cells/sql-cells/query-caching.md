On this page

# Query caching

Hex improves performance, and reduces the load on your data warehouse, by using cached results of previous SQL queries when the same query has been run recently.

info

* Users will need **Can Edit** [permissions](/docs/collaborate/sharing-and-permissions/sharing-permissions#what-permissions-are-there).

## Using cached query results[​](#using-cached-query-results "Direct link to Using cached query results")

Any time a SQL query is run against a data warehouse in a Hex project, Hex checks if the same query has been run recently. If it has, Hex pulls results from its cache, rather than sending the query to your warehouse.

At any time, users can override the cached results. By default, results from the cache will be used if the same query has been run within the last 60 minutes. Admins can [adjust this default for their workspace](#adjusting-cache-settings), while editors can further configure their cache settings per project.

### In Notebook view[​](#in-notebook-view "Direct link to In Notebook view")

In Notebook view, when the results of a SQL query use cached results, it will be indicated on the cell like so:

You can force the query to be re-executed against the data warehouse by clicking the query age indicator and selecting **Run without cached results**.

[](/assets/medias/rerun-without-cache-37c6651541bca3e3f28f046309b858e8.mp4)

You can also force all cells that run SQL to re-execute the query against the data warehouse via the **Run all without cached results** button when rerunning a project.

### In Published Apps[​](#in-published-apps "Direct link to In Published Apps")

When running a published app, Hex uses cached SQL results for cells that execute SQL against a data warehouse. Users can adjust whether or not published apps pull from cache, as well as set the max age of cached results, in a project's [App run settings](/docs/share-insights/apps/app-run-settings). Note that when multiple cached SQL results are used in an app, this number represents the **maximum** age of the results.

An app can be rerun without cached results via the **Refresh** button.

## Adjusting cache settings[​](#adjusting-cache-settings "Direct link to Adjusting cache settings")

By default, Hex will use cached results in both the Notebook and published app if the same query has been run within the last 60 minutes.

info

Query cache settings configure when the query cache will be refreshed. These settings do not configure the length of time the query cache is retained. Hex retains cached query data for up to 30 days after a cached query was last accessed, and cached project data for as long as the given project exists. For more on Hex's data retention policies, see our [Service Agreement](/docs/legal/hex-service-agreement).

### Workspace default[​](#workspace-default "Direct link to Workspace default")

Admins can adjust this default for their workspace, with separate timeouts for developing logic and published apps. To adjust the default timeouts, visit **Settings** → **Environment** under the "Workspace" header, and adjust the settings for **Workspace SQL caching**.

### Notebook settings[​](#notebook-settings "Direct link to Notebook settings")

Editors can override the workspace default for the Notebook caching timeout in the **Environments** tab of the left sidebar:

[](/assets/medias/adjusting-cache-settings-c5b1c7f15e5eafab1e924e3cb0bc050f.mp4)

### Published app settings[​](#published-app-settings "Direct link to Published app settings")

Editors can adjust the published app cache timeout at the project level in the app run settings, or the publish dialog.

If the app is set to "Auto-refresh published results", this is controlled via the staleness timeout:

If the app uses another run behavior, a separate setting is available to configure the cache timeout:

Learn more about [app run settings](/docs/share-insights/apps/app-run-settings).

## Using scheduled runs to refresh the SQL cache[​](#using-scheduled-runs-to-refresh-the-sql-cache "Direct link to Using scheduled runs to refresh the SQL cache")

A [scheduled run](/docs/share-insights/scheduled-runs) of a published app can be configured to ignore the SQL cache, and instead execute SQL queries against the data warehouse, effectively refreshing the SQL cache.

Additionally, rather than set a fixed timeout on cached SQL results in a published app, you can choose to use the timestamp of the most recent scheduled run to determine if a cached result is still valid, as shown in the screenshot above.

This option will only appear if a scheduled run is configured.

Note that if the same query is run elsewhere in Hex (e.g. an Editor runs this query in Notebook view, or the same query is run in another project), the published app will use **the most recent results**, even if they are newer than the results produced by the most recent scheduled run.

## FAQs[​](#faqs "Direct link to FAQs")

**Which cells do caching settings apply to?**

Hex may use cached results for any cell that runs SQL against a data warehouse. This includes SQL cells that use a data connection (and excludes SQL cells using dataframe SQL), as well as Input, Chart, Pivot, Filter and Explore cells that use [query objects](/docs/explore-data/cells/sql-cells/sql-cells-introduction#query-mode) as an input.

**Can I disable caching for my workspace?**

Admins can choose to disable caching for their workspace from the **Workspace SQL caching** settings. Once disabled, Editors will not be able to enable caching for their project.

warning

Disabling caching will lead to increased run times and data warehouse loads. If you are concerned about freshness of data, consider reducing your cache timeout rather than disabling caching.

**Why are my query results not caching?**

There are a few scenarios where you may expect your query results to be cached, but are still seeing queries run against your data warehouse instead of pulling from cache. If your query meets any of the following conditions, Hex is unable to cache the results:

* The query contains statements that are not select statements
* The results of the query are larger than 16 GB
* The query is dependent on a variable whose value is changing (e.g., the query uses Jinja to reference the current timestamp)

If your query does not meet any of these conditions and is still failing to cache, reach out to [[email protected]](/cdn-cgi/l/email-protection#4c3f393c3c233e380c2429346238292f24) for assistance troubleshooting.

**Does running a query without cached results update the results for everyone?**

If you choose to run a query without cached results, the results of this query that are stored in the cache will be updated. This means that if another project uses the same query, the **next** time the cell is run, the more-recent results will be pulled from the cache.

#### On this page

* [Using cached query results](#using-cached-query-results)
  + [In Notebook view](#in-notebook-view)
  + [In Published Apps](#in-published-apps)
* [Adjusting cache settings](#adjusting-cache-settings)
  + [Workspace default](#workspace-default)
  + [Notebook settings](#notebook-settings)
  + [Published app settings](#published-app-settings)
* [Using scheduled runs to refresh the SQL cache](#using-scheduled-runs-to-refresh-the-sql-cache)
* [FAQs](#faqs)