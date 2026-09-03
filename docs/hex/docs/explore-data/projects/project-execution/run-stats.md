On this page

# Run stats

Understand the performance of your project with run stats

Run stats help users with Can Edit permission understand a project's performance by showing cell timings and cache usage.

## Navigate run stats[​](#navigate-run-stats "Direct link to Navigate run stats")

### Notebooks[​](#notebooks "Direct link to Notebooks")

Access run stats via the **Run stats** icon in the upper right corner of your project.

In the panel, you’ll see all runs from the past two days. Each run of the entire project, a selection of cells, or a singular cell will create a new row labeled with the user, date and time, run scope, run time, cache, and session type.

You can sort the list by **Most recent** or **Oldest first**, and use filters to narrow runs by **User**, **Session type**, or **Cache**.

### Published apps[​](#published-apps "Direct link to Published apps")

From the three-dot menu in the upper right corner, select **Advanced > View run stats** and you’ll be redirected to the notebook. When you open the run stats panel, it opens directly to the run associated with the app session you were viewing.

### Run level stats[​](#run-level-stats "Direct link to Run level stats")

After you select a run, the top of the panel provides general information about the run and the legend used to interpret the per cell information. Here, you’ll see the total run time and kernel initialization time - this can be impacted by the time spent loading [files](/docs/explore-data/projects/environment-configuration/files) and imported [GitHub packages](/docs/administration/workspace_settings/workspace-assets#git-package-import)

In the upper right corner of the panel, you can filter by cell type, search by cell name, or sort by **Execution Order**, **Notebook Order**, **Slowest**, or **Fastest**.

### Cell level stats[​](#cell-level-stats "Direct link to Cell level stats")

Click into an individual cell to view the time spent preparing, executing, streaming, reading from cache, and processing.

The legend explains the time spent:

* **Preparing:** The time spent connecting to the warehouse and preparing the query
* **Executing:** The time spent executing the cell's query or code
* **Streaming:** The time spent streaming query results from the warehouse
* **Cache:** The time spent reading from Hex’s cache
* **Processing:** The time spent processing the cell’s query or output before displaying it

#### On this page

* [Navigate run stats](#navigate-run-stats)
  + [Notebooks](#notebooks)
  + [Published apps](#published-apps)
  + [Run level stats](#run-level-stats)
  + [Cell level stats](#cell-level-stats)