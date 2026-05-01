On this page

# Workspace search

Quickly find the projects and components in your workspace.

Workspace search allows you to search your workspace to easily find projects and components. You can access workspace search from the upper left corner of the Home page, or via the keyboard shortcut, `/`.

[](/assets/medias/workspace-search-f7bc302034bdb6ca604612ddb62a335c.mp4)

To refine search results, use the filter dropdowns for project creator, date ranges for when the project was last edited or created, project category, and project status.

tip

Don't recall the name of your project? No key words are needed to take advantage of search. Try filtering to projects you created in a certain date range that you remember putting in a certain category.

### Cell search[​](#cell-search "Direct link to Cell search")

By default, workspace search also allows you to locate a project based on the contents within your projects. Text and code from Python cells, SQL cells, R cells, Markdown cells, and Text cells are all included in your search when the **Cell contents (text + code)** box within the **Search by** dropdown is checked.

In this case, I recall working with a dataframe, `trips`, but don't remember what the project was called.

[](/assets/medias/code-search-69ac49951502080834e70f310b7f703e.mp4)

By including project contents in my search and filtering to only projects I created, I was able to find the project I was looking for in just a few seconds. You can jump directly to the first three cells in your project where the keyword is used by clicking on the cell name highlighted on the left. In this example, "Start stations" is a SQL cell that is the first reference to `trips`.

tip

Cell search is currently limited to the first 200 cells or first 9,500 lines of code in a project, whichever is reached first.

### Search and permissions[​](#search-and-permissions "Direct link to Search and permissions")

Workspace search will always respect Hex user roles and project permissions. Unless you are a Hex Admin, projects that have not been shared with you will not show up in search.

If you have at least "Can explore" access to a project, clicking on the project's name will take you to the Notebook view. If the project is published, you'll have the option to go straight to the published app by clicking on the monitor icon on the right.

#### On this page

* [Cell search](#cell-search)
* [Search and permissions](#search-and-permissions)