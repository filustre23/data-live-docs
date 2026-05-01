On this page

# Environment views

Manage your project environment from the **Environment**, **Files**, and **Variables** sidebars.

## Environment[​](#environment "Direct link to Environment")

You can adjust your project's compute profile, cell execution settings, and more from the **Environment** sidebar.

### Compute profile[​](#compute-profile "Direct link to Compute profile")

#### Image[​](#image "Direct link to Image")

By default, projects use Python 3.12. You can change which version of Python the project uses via the Image dropdown.

If your organization uses [custom images](/docs/administration/workspace_settings/custom-images), you can use the same dropdown to select a custom image to be used in your projects.

tip

Hex's Python 3.12 image supports `pandas==2.3.3`, `numpy==2.4.2`, and `duckdb==1.4.4`, while also significantly reducing the overall image size and number of pre-installed packages, resulting in lower kernel startup time generally and fewer version conflicts, making in-notebook package installs easier!

If you are missing an expected package, you may need to `!uv pip install` it in your notebook, or change your Image to an earlier Python version -- only 3.11 and 3.12 will be fully patched with the latest fixes for security vulnerabilities in third-party packages.

#### Size[​](#size "Direct link to Size")

Compute profile size determines the CPU, GPU, and memory limits for your [project kernels](/docs/explore-data/projects/environment-configuration/project-kernels). You can adjust compute profile size to meet the needs of your project.

| Size | Memory (GB) | CPUs | GPUs | Availability |
| --- | --- | --- | --- | --- |
| Extra Small | 2 | 4 | 0 | Included |
| Small | 4 | 4 | 0 | Included |
| Medium (default) | 8 | 4 | 0 | Included |
| Large | 16 | 4 | 0 | Pay-as-you-go |
| Extra Large | 32 | 4 | 0 | Pay-as-you-go |
| 2XL | 64 | 8 | 0 | Pay-as-you-go |
| 4XL | 128 | 16 | 0 | Pay-as-you-go |
| L4 GPU | 27 | 6 | 1 | Pay-as-you-go |
| A10G GPU | 27 | 6 | 1 | Pay-as-you-go |

info

* All paid [plans](https://hex.tech/pricing) include up to Medium compute.
* Large+ compute is available [pay-as-you-go](/docs/administration/workspace_settings/compute#what-is-advanced-compute) on Team and Enterprise [plans](https://hex.tech/pricing/?modal=compute).

##### When should I use a larger compute profile?[​](#when-should-i-use-a-larger-compute-profile "Direct link to When should I use a larger compute profile?")

Larger compute profiles are primarily used for data science workflows, like model training, that bring large datasets in-memory (>8GB) and/or require more computational power. There are two primary use cases for larger compute profiles:

1. **High memory requirements**: If you're working with more than 8GB of data, you may choose a larger compute profile size to increase your project memory. However, note that Hex supports both [SQL pushdown with Query mode](/docs/explore-data/cells/sql-cells/sql-cells-introduction#query-mode) and [Python pushdown with Snowpark](/docs/connect-to-data/data-connections/snowpark), which are typically the best solutions for memory constraints alone. Learn more about [managing memory in Hex](/tutorials/develop-notebooks/memory-management-in-hex).
2. **Code threading**: If you're writing computationally-expensive Python code, you may choose a compute profile with more CPUs and/or GPUs, in order to implement code threading or parallel processing. This is a common technique to speed iteration cycles in ML model training workflows.

##### What happens when I update my compute profile size?[​](#what-happens-when-i-update-my-compute-profile-size "Direct link to What happens when I update my compute profile size?")

When you update your project's compute profile size, you will need to either run your project or restart your [kernel](/docs/explore-data/projects/environment-configuration/project-kernels) to apply the changes. Kernels powering published App sessions and scheduled runs will not be updated until you [publish](/docs/share-insights/apps/publish-and-share-apps#publish-a-version) your changes. Note that anonymous users (i.e. users without a Hex account) who view a publicly-shared App will always be limited to Small compute, regardless of the underlying project's compute profile.

tip

Larger compute profiles require a longer kernel startup time before the project begins running. Kernel startup time does not contribute to your compute usage for usage-based billing.

#### Notebook idle timeout[​](#notebook-idle-timeout "Direct link to Notebook idle timeout")

The idle timeout setting dictates how long your [notebook kernel](/docs/explore-data/projects/environment-configuration/project-kernels) will stay alive after it becomes idle. A kernel is considered idle when no cells are running. The default idle timeout is 1 hour, but can be decreased (e.g. to manage costs when using [advanced compute profiles](/docs/administration/workspace_settings/compute)), or increased (e.g. to ensure Python state is preserved if you need to step away during a long-running job).

Idle timeouts >5 hours are available only on [advanced compute profiles](/docs/administration/workspace_settings/compute).

### Cell execution order[​](#cell-execution-order "Direct link to Cell execution order")

Hex uses a project’s DAG to understand dependencies between cells. Instead of running cells linearly according to the notebook ordering, Hex can leverage [this dependency graph](/docs/explore-data/projects/project-execution/graph-view) to perform various runtime optimizations such as parallelizing independent cells and ignoring hidden cells (when in app view).

From the **Environment** sidebar, use the Cell execution order toggle to determine whether the project should run with performance optimization (toggle on) or run linearly (toggle off). Leaving the toggle ON is recommended for the vast majority of cases - when in doubt, leave it alone!

In rare circumstances where Hex is not able to intuit a dependency between python cells, the toggle can be turned OFF to force linear ordering based on the notebook cell order.

## Files[​](#files "Direct link to Files")

From the **Files** sidebar in your Hex project, you can [upload files](/docs/explore-data/projects/environment-configuration/files#upload-files) including CSV and JSON files.

## Variables[​](#variables "Direct link to Variables")

From the **Variables** sidebar in your Hex project, you can add project secrets and environment variables, as well as reference built-in variables and any variables defined in your code.

### Secrets[​](#secrets "Direct link to Secrets")

Keep your sensitive values, like API tokens or passwords, secret by adding them as Secrets. We store all Secrets in a highly-encrypted vault, which is only visible to other users with "Full Access" or "Can Edit" project permissions. Secrets can be referenced in Python cells, but an attempt to display them in the Notebook view or App builder will return `[SECRET VALUE]` .

You can add a Secret to a project by clicking the **+Add** button in the Secrets tab of the left sidebar. If you want to use a Secret which is defined as a shareable, [workspace Secret](/docs/administration/workspace_settings/workspace-assets#shared-secrets), choose **Import workspace secret** from the menu to be presented with Secrets which are available for import. If you want to create a Secret for use only in the given project select **Create project secret**.

To access your Secrets, call them directly in place of where you would hard-code your credentials. In the example below, we're setting up a Snowflake connection and passing the database details as Secrets.

### Environment variables[​](#environment-variables "Direct link to Environment variables")

You can configure environment variables to be used in your projects. Environment variables aren't kept in the encrypted vault, nor are they redacted. Setting an environment variable in the left side panel is equivalent to using the python `os` library directly in your logic.

See more documentation for the `os` library [here](https://docs.python.org/3/library/os.html).

### Built-in variables[​](#built-in-variables "Direct link to Built-in variables")

We also have some variables which are automatically included in your project. These variables can be referenced in any cell.

| Variable | Value | Description |
| --- | --- | --- |
| [hex\_scheduled](/docs/share-insights/scheduled-runs#detecting-scheduled-runs-in-code) | False/True | If the run is being executed as part of a scheduled run, this variable is set to `True`. If the run is executed in any other context, the variable is set to `False`. |
| hex\_user\_email | email | If a user is logged in and viewing a published app, this variable is equal to the email address associated with their user account. Helpful if you want to customize what a given user sees in the app. Check out our Tutorials page for an example. |
| [hex\_run\_context](/docs/share-insights/scheduled-runs#detecting-scheduled-runs-in-code) | "logic", "app", "scheduled", "api-triggered", "publish-preview", "app-refresh&quot | Describes the context that the project is being run in. Helpful if you want to restrict certain logic to only run in particular run contexts. For example, use this if you have some debug code that you want to run in the logic, but don't want to run while a user is interacting with the published app. |
| hex\_timezone | `"America/Los_Angeles"`, `"Australia/Sydney"`, etc. | The timezone selected for the project. By default this is the [workspace timezone](/docs/administration/workspace_settings/overview#workspace-timezone), but can also be overridden at the project level, as well as for specific app sessions. See Chart cell timezones for more information. |
| hex\_project\_id | Project ID i.e. `1f0cfa16-cea1-428a-b950-e56379f2fdac` | A unique project identifier found in the Project's URL |
| hex\_project\_name | Project Name i.e. "Weekly Metrics" | Name given to the project |
| [hex\_status](/docs/getting-started/create-your-first-project#status-category) | "In Progress", "Approved", "Archive", etc. | Status the project is tagged with. Admins can configure custom statuses in the Organization section of workspace settings. |
| [hex\_categories](/docs/getting-started/create-your-first-project#status-category) | ["Q2 projects", "Analytics", etc.] | Category or categories the project is tagged with. Admins can configure custom categories in the Organization section of workspace settings. |
| [hex\_color\_palette](/docs/administration/workspace_settings/workspace-custom-styling#custom-chart-color-palettes) | `['#4C78A8', '#F58518', '#E45756', ... ]` | An array of CSS color codes that map to the currently active [workspace color palette](/docs/administration/workspace_settings/workspace-custom-styling#custom-chart-color-palettes). Using this variable can help create consistently themed visualizations when using both the native [Chart cell](/docs/explore-data/cells/visualization-cells/chart-cells) and visualizations created via Python packages. |

### Mute cells[​](#mute-cells "Direct link to Mute cells")

If there are cells in your project that you only want to execute in specific contexts (e.g. on project runs in Notebook view, only during scheduled runs, etc.), you can do so using the built-in `hex_run_context` and `hex_scheduled` variables. With these variables, you can check the context for when each cell is run and execute the desired logic accordingly. See the below code snippets for some examples code!

```
if hex_run_context == 'logic':  
    ## Something that only needs to happen during a Notebook run  
else:  
    ## otherwise this cell will be muted
```

Similarly, you can do the same in an SQL cell via Jinja.

```
{% if hex_run_context == 'logic' %}  
    -- Something that only needs to happen during a Notebook run  
  
{% endif %}
```

### Variable explorer[​](#variable-explorer "Direct link to Variable explorer")

The Variable explorer allows you to browse the variables generated by your code. For each variable, we show you its name, type, and value.

#### On this page

* [Environment](#environment)
  + [Compute profile](#compute-profile)
  + [Cell execution order](#cell-execution-order)
* [Files](#files)
* [Variables](#variables)
  + [Secrets](#secrets)
  + [Environment variables](#environment-variables)
  + [Built-in variables](#built-in-variables)
  + [Mute cells](#mute-cells)
  + [Variable explorer](#variable-explorer)