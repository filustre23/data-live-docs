On this page

# Hex Basics

info

This tutorial is intended for users with an **Editor**, **Manager**, or **Admin** role.

This tutorial covers the basics of getting started as an Editor in Hex. We'll cover key concepts to help you confidently start building analyses in Hex. Once you’ve reviewed the basics of this tutorial, check out [**Hex Advanced**](/tutorials/quickstart/hex-advanced) to level up.

## 1. 📒 Intro to Projects 📒[​](#1--intro-to-projects- "Direct link to 1. 📒 Intro to Projects 📒")

First things first, we're kicking things off by introducing key Hex vocabulary to help you better understand how to make the most of Hex.

* [**Projects**](/docs/explore-data/projects/projects-introduction): Projects are the main entity that you will be creating in Hex, which you can do via the green **+ New Project** button in the upper right corner of your Home screen. Every Hex project starts as a notebook and can be published into an app.
* [**Notebooks**](/docs/explore-data/notebook-view/develop-your-notebook): Notebooks are an interactive workspace where you can access your data, write code, analyze data, create visuals, and document your work with different cell types, assisted by Hex’s [Notebook Agent](/tutorials/ai-best-practices/notebook-agent-best-practices).
* [**Cells**](/docs/explore-data/notebook-view/develop-your-notebook#everything-in-hex-is-a-cell): Cells are the main building block of notebooks. Hex has many different cell types that you can use to access data and build your analyses.
* [**Apps**](/docs/share-insights/apps/apps-introduction): Apps are a published subset of cells from your notebook that can be rearranged and shared with stakeholders. Apps can be built to look like evergreen dashboards, ad hoc reports, internal tools, data apps, etc.

Kickstart your analysis in a new, empty project by asking a question in the purple bar. *What percent has profit increased this year? How many leads does each sales team member have, and how does that compare to this time last quarter?*

For another starting point, import the **Dashboard** template into a new project. Create a new project from your workspace’s Home screen, click into the question mark icon in the bottom left corner, select “Dashboard” under Templates, and then select **Insert template** from the pop up.

tip

For some more advanced projects, browse the [Use Case Gallery](https://hex.tech/use-cases/) of sample projects to get inspired.

## 2. 🛢️ Accessing Data 🛢️[​](#2-️-accessing-data-️ "Direct link to 2. 🛢️ Accessing Data 🛢️")

Hex is quite flexible, giving you many options to access data in whichever way is easiest for you. Review the options below and choose one to get started.

* [**SQL cells**](/docs/explore-data/cells/sql-cells/sql-cells-introduction): A classic! Add a SQL cell to your project and write a query against a data connection that an Admin has granted you access to. This query is returned in a tabular format (a pandas dataframe, for the Python savvy) that can be used in any other cell you add next.
* [**Browse warehouse tables**](/docs/explore-data/data-browser): Don’t know exactly where to start? Open up the Data browser to search and explore the tables in your warehouse. Once you’ve identified a table you’d like to work off of, you can pull in the data in the [cell type of your choice](/docs/explore-data/data-browser#shortcuts).
* [**File uploads**](/docs/explore-data/projects/environment-configuration/files): Have a local CSV floating around you’d like to work with? Upload it to your project in the “Files” tab of the left sidebar. Additionally, if an Admin has established a connection to an [external file integration](/docs/explore-data/projects/environment-configuration/files#external-files), you can access files in Google Drive, GCS, or S3.
* **Pull in data via API**: Just about anything you can do in Python, you can do in Hex. Add a code cell to write python and pull in data programmatically. For an example of this workflow using Google Sheets, check out [this tutorial](/tutorials/connect-to-data/connect-to-google-sheets).

If you’re struggling with SQL or Python syntax, try asking for help via the interlocking circles icon in the upper right corner of SQL and Code cells.

info

All Hex workspaces come equipped with demo data for Editors to explore. If you’re not yet set up to work with your production data in Hex, take a look at the **[Demo] Hex Public Data** Snowflake connection in the Data browser.

## 3. 🔨 Building with cells 🔨[​](#3-building-with-cells "Direct link to 3. 🔨 Building with cells 🔨")

Hex notebooks are composed of different types of cells used to iteratively build your analysis. As a new Hex user (soon-to-be-Hexpert), we’ll start by covering three cell types that give you the most bang (insights) for your buck (time).

* [**Chart cells**](/docs/explore-data/cells/visualization-cells/chart-cells): Add a chart cell to make a rich visual of your data in just a few clicks. Whether you’d like to get a quick look at your data for some exploratory analysis or you’re building a dashboard-quality stylized viz, chart cells have you covered. Review the linked docs for the many configuration options.
* [**Table cells**](/docs/explore-data/cells/visualization-cells/table-display-cells): Create a table cell to apply spreadsheet-style filters, [calculations](/docs/explore-data/cells/calculations), and aggregations to your dataframe. No coding skills required 😎.
* [**Input cells**](/docs/category/input-cells): The very powerful lineup of input cells allows your apps to be interactive. Inputs store variables that can be referenced downstream to parameterize visuals in your app. If you imported the “Dashboard” template from 📒 **Intro to Projects** 📒, you’ll see a simple example of a multi-select input at work. More to come in [**Hex Advanced**](/tutorials/quickstart/hex-advanced)…

tip

Add context to your project with [Text and Markdown cells](/docs/explore-data/cells/text-cells).

## 4. 📊 Sharing and Publishing Apps 📊[​](#4-sharing-and-publishing-apps- "Direct link to 4. 📊 Sharing and Publishing Apps 📊")

Hex projects are private by default, meaning only you (and your Admins) have access. Review the topics below to ensure you’re making the most of Hex’s collaborative environment.

* [**Sharing**](/docs/collaborate/sharing-and-permissions/project-sharing): Share your project with teammates via the “Share” button in the upper right corner. To collaborate in the notebook, your teammate will need at least an Editor role. Check out [this matrix](/docs/collaborate/sharing-and-permissions/project-sharing#workspace-roles-and-project-permissions) for a visualization of who can access what. To quickly grant access to your entire workspace, flip the “Invite only” dropdown to “Everyone at *your workspace*.”
* [**Collaborating**](/docs/collaborate/real-time-collaboration): Hex notebook’s are multi-player, meaning you and your teammates can be working in the same project at the same time (a la Google Docs, Figma, etc.). Once you’ve granted another user “Can edit” or “Full access,” they can visit your notebook, tag you in [comments](/docs/collaborate/comments), or complete a [review](/docs/collaborate/reviews).
* [**App building**](/docs/share-insights/apps/app-builder): When your analysis in the notebook is complete, click over to the App Builder tab on the top of your screen. This is where you can add, remove, drag and drop whichever cells from your analysis you’d like to be displayed in your app. For inspiration on what’s possible, check out our [Use cases page](https://hex.tech/templates/).
* [**Publishing**](/docs/share-insights/apps/publish-and-share-apps): Lastly, the final step in the project lifecycle—publishing! Once your app is configured to your desires, hit publish in the upper right corner. Voila! You’ve crafted a data application that you can be shared across your team.

You made it to the end of Hex Basics 🎉. See the [**Hex Advanced**](/tutorials/quickstart/hex-advanced) tutorial to level up. If you’re looking for more resources, check out our [Hex Foundations Video library](/tutorials/category/hex-foundations), [Use Case Library](https://hex.tech/use-cases/), and the rest of our [Learn site](https://learn.hex.tech/).

#### On this page

* [1. 📒 Intro to Projects 📒](#1--intro-to-projects-)
* [2. 🛢️ Accessing Data 🛢️](#2-️-accessing-data-️)
* [3. 🔨 Building with cells 🔨](#3-building-with-cells)
* [4. 📊 Sharing and Publishing Apps 📊](#4-sharing-and-publishing-apps-)