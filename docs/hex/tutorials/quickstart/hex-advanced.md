On this page

# Hex Advanced

info

This tutorial is intended for users with an **Editor**, **Manager**, or **Admin** role.

This tutorial covers more advanced functionality for new Editors in Hex. If you’re brand new to Hex, check out [**Hex Basics**](/tutorials/quickstart/hex-basics) first to get started.

## 1. ❔ SQL Deep Dive ❔[​](#1--sql-deep-dive- "Direct link to 1. ❔ SQL Deep Dive ❔")

Hex makes querying your warehouse painless, but there are a number of additional features to improve your workflows and QOL.

* [**Chained SQL**](/docs/explore-data/cells/sql-cells/sql-cells-introduction#chained-sql): Break apart long queries into multiple cells for readability and collaboration, and let Hex do the rest. To see what I mean, select the `{}` icon in the upper right of a SQL cell to view the compiled SQL that is actually sent to the warehouse when chaining SQL.
* [**Dataframe SQL**](/docs/explore-data/cells/sql-cells/sql-cells-introduction#dataframe-sql): Beyond querying the data in your warehouse, Hex allows you to write SQL queries against any dataframe that exists in your project. This can be super useful for quick manipulation, and is faster than querying your warehouse since it all happens within Hex.
* [**SQL caching**](/docs/explore-data/cells/sql-cells/query-caching): By default, SQL caching is enabled in new projects, inheriting a workspace-level setting configured by an Admin. Hex stores a copy of all query results—if you run the same query again within the timeout window, Hex will pull the results from the cache instead of executing in the warehouse, saving time and $$$.

info

This timeout can be overridden in the Environments tab of the left sidebar for the notebook and the Published app run settings section of the app builder right sidebar for the published app.

## 2. 🐍 **Python & Notebooks** 🐍[​](#2--python--notebooks- "Direct link to 2--python--notebooks-")

Hex’s Python support raises the ceiling of what is possible in Hex’s environment—API calls, model training, complex viz, and just about anything else you can think of. Even if you lack experience with Python, review the topics below as Magic may soon be expanding your skill set.

* [**Run modes**](/docs/explore-data/projects/project-execution/run-modes-and-cell-staleness): Hex notebooks default to “Auto” run mode which means any time a cell is run, any stale and descendent cells are also run to maintain the state. Hex infers these relationships between cells which is viewed in a visual representation in the [Graph view](/docs/explore-data/projects/project-execution/graph-view).
* [**Packages**](/docs/explore-data/projects/environment-configuration/using-packages#install-new-packages-through-uv-pip): Every Hex project comes with many pre-installed Python packages displayed in the bottom of the Environments tab of the left sidebar. Other packages not in this list can be used with a `!uv pip install` statement.

  warning

  !pip installing packages can slow down published apps. Every published app session uses a fresh kernel which means the package is installed every time someone visits the app.
* [**Compute**](/docs/explore-data/projects/environment-configuration/environment-views#compute-profile): By default, every Hex project uses a Medium (8GB, 1CPU) Python kernel, but is configurable in the Environments tab of the left sidebar. For more details on memory management in Hex, check out [this tutorial](/tutorials/develop-notebooks/memory-management-in-hex).
* [**Command palette**](/docs/explore-data/notebook-view/keyboard-shortcuts#command-palette): Hex comes equipped with a long list of IDE creature comforts, including many keyboard shortcuts and even [Vim key bindings](/docs/administration/user-settings#preferences). Trigger the command palette to view these options in the notebook with a `CMD`+`K`.

info

Kernels with more memory, CPU, and GPU support are available on a pay-as-you-go basis. [Learn more](/docs/administration/workspace_settings/compute).

## 3. 🎛️ Parameterization and filtering 🎛️[​](#3-️-parameterization-and-filtering️ "Direct link to 3. 🎛️ Parameterization and filtering 🎛️")

Hex is so powerful largely due to its interactivity. Review the options below and if you’re curious, check out [Explore](/docs/share-insights/explore) for another way stakeholders can drill down on data in your apps to self-serve follow up questions.

* [**Input cells**](/docs/category/input-cells): Adding input cells to your app is a great option for adding interactivity for your consumers. Every input cell outputs a variable containing the selected value that can be referenced downstream. For more details on parameterizing your project based on input selections, check out the docs on [using Jinja](/docs/explore-data/cells/using-jinja).

  tip

  If you’re building an app with many input cells, consider setting the [Interaction app run setting](/docs/share-insights/apps/app-run-settings#interaction) to "*Wait for app users to click a run button*” to prevent kicking off unnecessary app runs.
* [**Cell filters**](/docs/explore-data/cells/visualization-cells/table-display-cells#filter-your-table-display-cell): Cell-level filters can be applied directly to SQL, Table, Chart, and Explore cells from both the notebook and the app, without the additional backend configuration required by inputs. You can also apply a filter in Chart cells by clicking an option in the legend or selecting a portion of the chart from either the notebook or the app.
* [**Project filters**](/docs/share-insights/apps/project-filters): A step up from cell-level filters are project-level filters. Project filters can be configured in the notebook and tied to multiple cells. Check out the linked docs for more details.

info

When applying a cell filter in a published app, you may be prompted to apply the filter to multiple cells, creating a [project filter](/docs/share-insights/apps/project-filters#use-project-filters-in-the-published-app).

## 4. ⚡ Building performant apps ⚡[​](#4-building-performant-apps- "Direct link to 4. ⚡ Building performant apps ⚡")

Making your apps snappy for end users is super important for allowing them to derive insights. Before reviewing the settings below, take a moment to consider how fresh the data needs to be for one of your use cases. Do you need data from the top of the hour? Or does the data from this morning meet your needs?

* [**App run settings**](/docs/share-insights/apps/app-run-settings): When configuring published app run settings, consider setting **Data freshness** to *Rerun the app if stale* and adjusting **Mark app results as stale if older than:** to reflect the expected freshness of your data. This approach balances app speed with data up-to-date-ness.
* [**Scheduled runs**](/docs/share-insights/scheduled-runs): Scheduled runs kick off runs of your published apps at a set frequency and serve two main purposes—notifying users at a set cadence and updating the default state of a published app. For apps that are visited with some regularity, consider setting up a scheduled run to update the default state so that the app is never stale per the setting above ⬆️.
* [**Saved views**](/docs/share-insights/apps/saved-views): Create saved views of an app with your common input selections and set up a schedule to update your app with the selections in your saved view.

## 5. 🧭 Navigating your workspace 🧭[​](#5-navigating-your-workspace- "Direct link to 5. 🧭 Navigating your workspace 🧭")

Now that you know the ins and outs of creating a project and publishing an app, we’re wrapping up with some pointers on navigating your Hex workspace.

* [**Home page**](/docs/explore-data/projects/create-and-manage-projects#projects-home): Your Hex Home page displays your recent projects, apps popular in your workspace and a number of places to start a new analysis. Use [workspace search](/docs/organize-content/workspace-search) to locate existing assets, with the ability to search down to the contents of your code!
* [**Collections**](/docs/organize-content/collections): Organize and share your projects with Collections. View existing Collections and create a new one from the “Collections” tab on the left side of your Hex Home screen. Check out [this blog post](https://hex.tech/blog/collections-at-hex/) to learn about how we use Collections internally at Hex.
* [**User settings**](/docs/administration/user-settings): Configure user-level settings per your personal preference such as dark mode and word wrap on different cell types. While you’re there, pop over to the [Notifications](/docs/administration/user-settings#notifications) tab and configure how you’d like to receive updates about different content.

tip

Favorite projects and tables via the ⭐ icon for easy access on the left pane of your Home screen.

You made it. You’re on the way to being a first-class Hexpert! If you’re still hungry for more, check out the [SQL Learning Path](https://app.hex.tech/hex-public/app/7388ee87-3d19-4dc0-8902-4810e89aef8e/latest) or [SQL + Python Learning Path](https://app.hex.tech/hex-public/app/9f75bf22-e512-4b86-865d-a1fc2050111e/latest), as well as the [Hex Foundations Video library](/tutorials/category/hex-foundations).

#### On this page

* [1. ❔ SQL Deep Dive ❔](#1--sql-deep-dive-)
* [2. 🐍 **Python & Notebooks** 🐍](#2--python--notebooks-)
* [3. 🎛️ Parameterization and filtering 🎛️](#3-️-parameterization-and-filtering️)
* [4. ⚡ Building performant apps ⚡](#4-building-performant-apps-)
* [5. 🧭 Navigating your workspace 🧭](#5-navigating-your-workspace-)