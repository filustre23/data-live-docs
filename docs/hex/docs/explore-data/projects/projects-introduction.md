On this page

# What is a project?

Projects are where you’ll explore, analyze and visualize your data, curate your insights, and build interactive, shareable reports.

Projects are notebook-like environments that enable you to seamlessly model and explore your data, document and share your insights, and collaborate with your team. Connect to and query your data with SQL, then layer in Python or R to dig in further.

## The Notebook view[​](#the-notebook-view "Direct link to The Notebook view")

The Notebook view is where you will conduct your full exploration and analysis by adding cells and developing your logic.

If you have used a data science notebook before, you will be right at home. However, Hex extends the notebook model in several key ways, making it easy to build and manage your project directly from a single interface.

Hex projects consist of cells, which are individual building blocks for developing your analysis. Hex supports a variety of code and UI-driven cells, allowing you to do everything from pivoting data on the fly with just a few clicks to writing Python from scratch.

### Project metadata[​](#project-metadata "Direct link to Project metadata")

At the top of the Notebook view, you'll find the project metadata section. Here you can:

* Rename the project
* Apply statuses or categories to the project
* Add a project description

#### Status & Category[​](#status--category "Direct link to Status & Category")

Projects can be tagged with one **status** and multiple **categories**. You can use these project labels to filter the main [Projects home](/docs/explore-data/projects/create-and-manage-projects#projects-home) to organize large numbers of projects. Status and Category can be optionally displayed in a published app via the [App metadata configuration](/docs/share-insights/apps/app-run-settings#app-metadata).

Workspace Admins can edit and add new statuses and categories from the [Settings panel](/docs/administration/workspace_settings/overview).

### **Adding cells**[​](#adding-cells "Direct link to adding-cells")

You can access the **Add Cell** button at the bottom of your project or by hovering your pointer between existing cells.

Click on the **Add cell** button to open the cell **library modal**. Select the cell type you want to add it to your project.

### Cell options[​](#cell-options "Direct link to Cell options")

Access the cell options dropdown by clicking on the three-dot menu in the upper right corner of each cell. Cell options support actions that include reordering cells in your project, duplicating, and embedding, among others.

### Run options[​](#run-options "Direct link to Run options")

The **Run all** button in the upper right corner of the Notebook view screen allows you to execute all the cells in your project with a single click. Select the down arrow next to the button to view more options for how to run project cells, as well as options for managing the project kernel. Read more about [run modes](/docs/explore-data/projects/project-execution/run-modes-and-cell-staleness) and [kernels](/docs/explore-data/projects/environment-configuration/project-kernels).

## App builder[​](#app-builder "Direct link to App builder")

The App builder view allows users to quickly and easily compose elements from the Notebook View into an interactive, beautiful web app that anyone can use.

The first time you navigate to the App builder in a project, Hex auto-generates an app based on the contents of your Notebook view. You can add, remove, reposition, and resize elements to customize the layout of your app. Additionally, you can add multiple tabs to organize cells into different views.

If you prefer to start building from scratch, select the **Remove all elements** option from the **Reset layout** dropdown menu at the top of the **Outline** tab in the left sidebar.

You can drag-and-drop elements from the left-hand Outline panel using the drag handle to its right. Alternatively, you can use the **Add to app** button on each element, from the Outline or Notebook view.

Read more about building apps [here](/docs/share-insights/apps/app-builder).

## **Left sidebar**[​](#left-sidebar "Direct link to left-sidebar")

The left sidebar houses options for navigating and managing your project. This is where you’ll browse or add data sources, configure your environment, and set up automatic refreshes.

The sidebar is visible in both the **Notebook** and **App builder** views.

tip

Option ordering in the left sidebar varies slightly between the Notebook and App builder views. The Outline and Project Search options in the Notebook are placed in a mini-outline beneath the options listed below, but the Outline and Project Search options in the App builder are listed at the top of the sidebar.

### Outline[​](#outline "Direct link to Outline")

The outline provides an easy-to-browse overview of all the cells in a project's Notebook View. Every cell in the outline lists the variables it defines, and cells that return a displayed output (chart cells, Input Parameters, markdown cells, etc.) show a preview of that output when hovered over.

You can click any cell in the outline to automatically jump to where it lives in the Notebook. The outline can also be filtered by cell type. Input elements in the outline are fully interactive, allowing you to adjust upstream parameters without excess scrolling.

### Project Search[​](#project-search "Direct link to Project Search")

Search for text within your project using the **project search** bar at the top of the outline view. If you are searching for a specific variable, field name, or text string, using the project search is a quick way to locate all the cells that contain it.

Replace project elements easily using the 'Replace' feature to the right of the search bar.

### Data Browser[​](#data-browser "Direct link to Data Browser")

Browse available data sources or create a new one to bring into your project. If your Hex Admin configured a metadata integration with dbt Cloud, you will be able to see model, source and column [descriptions](https://docs.getdbt.com/reference/resource-properties/description) and [tests](https://docs.getdbt.com/docs/building-a-dbt-project/tests).

Read more about connecting to data [here](/docs/connect-to-data).

### Environment[​](#environment "Direct link to Environment")

Configure your compute profile, project timezone, SQL caching, and Python packages from the environment tab.

Read more about managing your project environment [here](/docs/explore-data/projects/environment-configuration/environment-views).

### Files[​](#files "Direct link to Files")

You can import up to 100 files (<2GB each) into a project using the **Files** tab in the sidebar. These files will be saved permanently as part of your project. The most common use case for this feature is importing CSVs as source data.

Read more about managing files in projects [here](/docs/explore-data/projects/environment-configuration/files).

### Variables[​](#variables "Direct link to Variables")

Hex supports using **environment variables** and managing sensitive values by storing them in **secrets**.

Read more about managing variables in projects [here](/docs/explore-data/projects/environment-configuration/environment-views#variables).

### Scheduled Runs[​](#scheduled-runs "Direct link to Scheduled Runs")

Hex apps can be configured to be run on a schedule at whatever cadence makes sense for your use case. When a scheduled run succeeds, the entire project's logic is run from top to bottom, executing any queries and writeback cells, running all code, and updating any outputs displayed in your app. Scheduled runs can also be used to update what users see when initially opening an app.

Read more about scheduled runs [here](/docs/share-insights/scheduled-runs).

### History and versions[​](#history-and-versions "Direct link to History and versions")

By default, projects have a simple but powerful version control engine built in that lets you see what's been changing in projects and restore to earlier versions. Versions, edits, and comments are all presented in a chronological timeline, with brief descriptions of who made changes and what they did.

Read more about history and version control [here](/docs/explore-data/projects/history-and-versions).

### Command palette[​](#command-palette "Direct link to Command palette")

You can access the command palette by hitting `cmd+p`. From there, you can filter the available actions by typing in the search bar and press `enter`, or use the corresponding keyboard shortcut, to execute.

Read more about the command palette [here](/docs/explore-data/notebook-view/keyboard-shortcuts).

## Project collaboration features[​](#project-collaboration-features "Direct link to Project collaboration features")

### Comment[​](#comment "Direct link to Comment")

You can leave a comment on any cell in both [Notebook View](/docs/explore-data/notebook-view/develop-your-notebook) and in [published Apps](/docs/share-insights/apps/publish-and-share-apps).

Click the icon in the upper right of an element to trigger the comment popover.

You can add a new comment, reply to an existing thread, or edit or delete any comment you authored. You can mention other users in your organization with @ tagging, and they will receive a notification via email.

Learn more about project comments [here](/docs/collaborate/comments).

### Share[​](#share "Direct link to Share")

You can use the **Share** menu in the upper right of your projects to manage permissions for a project. A project can be shared with individuals, a group of users (defined in **[Users & groups](/docs/administration/workspace_settings/overview#users--groups)**), or widely with the web. For each, you can specify the permissions allowed to shared users.

Read more about sharing and permissions [here](/docs/collaborate/sharing-and-permissions/sharing-permissions).

### Publish[​](#publish "Direct link to Publish")

When you have curated selections from your **Notebook** into a presentation layer in the **App builder** you can publish your app for others to consume. Access publishing options by selecting the **Publish** button in the upper right corner of the screen.

Read more about publishing insights [here](/docs/share-insights/apps/publish-and-share-apps).

#### On this page

* [The Notebook view](#the-notebook-view)
  + [Project metadata](#project-metadata)
  + [**Adding cells**](#adding-cells)
  + [Cell options](#cell-options)
  + [Run options](#run-options)
* [App builder](#app-builder)
* [**Left sidebar**](#left-sidebar)
  + [Outline](#outline)
  + [Project Search](#project-search)
  + [Data Browser](#data-browser)
  + [Environment](#environment)
  + [Files](#files)
  + [Variables](#variables)
  + [Scheduled Runs](#scheduled-runs)
  + [History and versions](#history-and-versions)
  + [Command palette](#command-palette)
* [Project collaboration features](#project-collaboration-features)
  + [Comment](#comment)
  + [Share](#share)
  + [Publish](#publish)