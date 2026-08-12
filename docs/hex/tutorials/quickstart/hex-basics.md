On this page

# Hex 101

info

This tutorial is intended for users with an **Editor**, **Manager**, or **Admin** role.

Hex 101 is a practical guide to the core workflows you can use in Hex every day. Once you’ve reviewed this tutorial, check out [**Hex Advanced**](/tutorials/quickstart/hex-advanced) to level up.

## What you can do in Hex[​](#what-you-can-do-in-hex "Direct link to What you can do in Hex")

* Move faster with **AI agents** that understand your data context.
* Explore and analyze data end-to-end in one workspace.
* Build in **notebooks** for SQL, Python, and no-code workflows that stay in sync.
* Share results through interactive **apps** your stakeholders can use.

## 1. 📒 Intro to projects 📒[​](#1--intro-to-projects- "Direct link to 1. 📒 Intro to projects 📒")

A [**project**](/docs/explore-data/projects/projects-introduction) is the core unit of work in Hex. It is where you explore data, build analyses, and publish work that others can use. Every Hex project starts as a notebook and can be published into an app.

Create a project from your Home screen with the top left **+ Project** button.

* [**Notebook**](/docs/explore-data/notebook-view/develop-your-notebook): Notebooks are an interactive workspace where you can access your data, write code, analyze data, create visuals, and document your work with different cell types, assisted by Hex’s [Notebook Agent](/tutorials/ai-best-practices/notebook-agent-best-practices).
* [**App**](/docs/share-insights/apps/apps-introduction): Apps are a published subset of cells from your notebook that can be rearranged and shared with stakeholders. Apps can be built to look like evergreen dashboards, ad hoc reports, internal tools, data apps, etc.

tip

For some advanced projects, browse the [Use Case Gallery](https://hex.tech/use-cases/) to get inspired.

## 2. 🛢️ How to go from data connection → answering a question 🛢️[​](#2-️-how-to-go-from-data-connection--answering-a-question-️ "Direct link to 2. 🛢️ How to go from data connection → answering a question 🛢️")

**Start in the Data browser.** Open it from the left sidebar to see every table available to you. You will be able to search, preview rows, check column types.

In order to view and analyze data, every Hex project is build with [**cells**](/docs/explore-data/notebook-view/develop-your-notebook#everything-in-hex-is-a-cell):

* [**SQL cells**](/docs/explore-data/cells/sql-cells/sql-cells-introduction): Query connected data sources directly. Add a SQL cell to your project and write a query against a data connection that an Admin has granted you access to. This query is returned in a tabular format (a pandas dataframe, for the Python savvy) that can be used in any other cell you add next.
* [**Chart cells**](/docs/explore-data/cells/visualization-cells/chart-cells): Add a chart cell to make a rich visual of your data in just a few clicks. Whether you’d like to get a quick look at your data for some exploratory analysis or you’re building a dashboard-quality stylized viz, chart cells have you covered. Review the linked docs for the many configuration options.
* [**Table cells**](/docs/explore-data/cells/visualization-cells/table-display-cells): Create a table cell to apply spreadsheet-style filters, [calculations](/docs/explore-data/cells/calculations), and aggregations to your dataframe. No coding skills required 😎.
* [**Input cells**](/docs/category/input-cells): The very powerful lineup of input cells allows your apps to be interactive. Inputs store variables that can be referenced downstream to parameterize visuals in your app. If you imported the “Dashboard” template from 📒 **Intro to Projects** 📒, you’ll see a simple example of a multi-select input at work. More to come in [**Hex Advanced**](/tutorials/quickstart/hex-advanced)…
* [**Python code cells**](/docs/explore-data/cells/python-cells): Call APIs and programmatically load data with flexibility.

tip

Unsure where to start? You can ask the [**Notebook Agent**](/docs/explore-data/notebook-view/notebook-agent), "what data is available to me?" or "I am looking to measure weekly retention, show me which tables are relevant."

## 3. 🤖 The quickest way to go from question → insight with agents 🤖[​](#3--the-quickest-way-to-go-from-question--insight-with-agents- "Direct link to 3. 🤖 The quickest way to go from question → insight with agents 🤖")

Hex includes different kinds of [Agents](/docs/getting-started/ai-overview) you can use as to move faster, stay consistent, and automate repeatable work.

* Want to answer a question quickly?
  + **[Threads](/docs/explore-data/threads) is the place to go.** Threads are a standalone chat surface that’s great for quick answers ("what was revenue last quarter?") without opening a project. Threads can pull from your warehouse, projects, run queries, build charts, and hand you back a shareable response.
* Have a question about an existing data app?
  + **Use [Chat with App](/docs/explore-data/chat-with-app) (powered by Threads)!** Chat with App lets viewers have a conversation with your published work in plain English: "break this out by region" or "show me just last quarter." The Agent answers using the app's underlying data and logic.
* **Using AI to do more complex analysis and debugging errors**
  + **The [Notebook Agent](/docs/explore-data/notebook-view/notebook-agent) is the way to go.** Ask the agent to draft SQL against your connected warehouse, explain what a cell is doing, debug an error, or suggest the right metric. It sees your notebook's full context (upstream cells, schemas, parameters) and can query all the data connections you have access to.
* **Creating custom code-generated app experiences**
  + **With [Generative Apps](/docs/share-insights/apps/generative-apps)!** Prompt an agent to build beautiful, interactive data experiences on top of your trusted source of truth so you no longer have to choose between governance + traceability and creative, story-first presentation.

info

For workflows outside Hex, ask a workspace **Admin** about [**Hex Agent in Slack**](/docs/share-insights/hex-agent-in-slack), [**MCP server**](/docs/api-integrations/mcp-server), and the [**CLI**](/docs/api-integrations/cli).

## 4. 📊 Collaborate and share results 📊[​](#4--collaborate-and-share-results- "Direct link to 4. 📊 Collaborate and share results 📊")

Hex is designed so teams can collaborate in one place.

* [**Sharing**](/docs/collaborate/sharing-and-permissions/project-sharing): Share projects, Explores, and Threads with teammates from the **Share** button. To collaborate in a notebook, your teammate will need at least an Editor role. Check out [this matrix](/docs/collaborate/sharing-and-permissions/project-sharing#workspace-roles-and-project-permissions) for a visualization of who can access what. To quickly grant access to your entire workspace, flip the “Invite only” dropdown to “Everyone at *your workspace*.”
* [**App building**](/docs/share-insights/apps/app-builder): When your analysis in the notebook is complete, click over to the App Builder tab on the top of your screen. This is where you can add, remove, drag and drop whichever cells from your analysis you’d like to be displayed in your app. For inspiration on what’s possible, check out our [Use cases page](https://hex.tech/templates/).
* [**Publishing**](/docs/share-insights/apps/publish-and-share-apps): Lastly, the final step in the project lifecycle—publishing! Once your app is configured to your desires, hit publish in the upper right corner. Voila! You’ve crafted a data application that you can be shared across your team.
* [**Comments**](/docs/collaborate/comments) and [**reviews**](/docs/collaborate/reviews): - On published apps, leave inline comments on any cell such as questions, feedback, "why is this filter here?". Tag teammates to loop them in. For work that needs sign-off, use **review mode** to request approval before publishing an app. Reviewers can comment, request changes, or approve without touching your notebook.

## 5. ⚡ Ready to build fast, reliable apps for stakeholders? ⚡[​](#5--ready-to-build-fast-reliable-apps-for-stakeholders- "Direct link to 5. ⚡ Ready to build fast, reliable apps for stakeholders? ⚡")

Before reviewing the settings below, take a moment to consider how fresh the data needs to be for one of your use cases. Do you need data from the top of the hour? Or does data pulled once a week meet your needs?

* [**App run settings**](/docs/share-insights/apps/app-run-settings): When configuring published app run settings, consider setting `Data freshness` to `Rerun the app if stale` and adjusting `Mark app results as stale if older than:` to reflect the expected freshness of your data.
* [**Scheduled runs**](/docs/share-insights/scheduled-runs): Kick off runs of your published apps at a set frequency and serve two main purposes—notifying users at a set cadence and updating the default state of a published app. For apps that are visited with some regularity, consider setting up a scheduled run to update the default state so that the app is never stale per the setting above ⬆️.
* [**Saved views**](/docs/share-insights/apps/saved-views): Create saved views of an app with your common input selections and set up a schedule to update your app with the selections.

You made it through Hex 101 🎉. Continue with [**Hex Advanced**](/tutorials/quickstart/hex-advanced) for deeper workflows, or browse the [Hex Foundations video library](/tutorials/category/hex-foundations).

#### On this page

* [What you can do in Hex](#what-you-can-do-in-hex)
* [1. 📒 Intro to projects 📒](#1--intro-to-projects-)
* [2. 🛢️ How to go from data connection → answering a question 🛢️](#2-️-how-to-go-from-data-connection--answering-a-question-️)
* [3. 🤖 The quickest way to go from question → insight with agents 🤖](#3--the-quickest-way-to-go-from-question--insight-with-agents-)
* [4. 📊 Collaborate and share results 📊](#4--collaborate-and-share-results-)
* [5. ⚡ Ready to build fast, reliable apps for stakeholders? ⚡](#5--ready-to-build-fast-reliable-apps-for-stakeholders-)