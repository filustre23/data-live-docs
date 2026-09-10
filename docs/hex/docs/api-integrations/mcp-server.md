On this page

# Hex MCP Server

Connect AI assistants to Hex through the Model Context Protocol (MCP).

info

* Available on the Team and Enterprise [plans](https://hex.tech/pricing/).
* Hex MCP server works with Claude Desktop, Claude Code, Cursor, ChatGPT, Codex, and Glean, as well as most standard MCP clients.
* Users will need the Explorer workspace [role](/docs/collaborate/sharing-and-permissions/roles) or higher to use the Hex MCP server. The [project editing tools](#project-editing-tools) additionally require the Editor role or higher.
* MCP access is not governed by the workspace [API access](/docs/administration/workspace_settings/workspace-security#enable-api-access) setting, which only affects personal access tokens. Turning off API access for the workspace, or revoking it for an individual user, does not disable MCP access. To revoke all of a user's access, [deactivate the user](/docs/administration/workspace_settings/overview#deactivate-users).
* Hex MCP server is currently in beta.

## Overview[​](#overview "Direct link to Overview")

The Model Context Protocol (MCP) allows AI applications to securely connect to external data sources and tools. The Hex MCP server enables AI assistants to interact directly with your Hex workspace. Through the MCP server, AI assistants can search your projects, create and continue [Threads](/docs/explore-data/threads) conversations, explore your data through natural language, and build and edit Hex projects.

The Hex MCP server provides two groups of [tools](#available-actions).

**Knowledge tools** let an agent search your workspace and run Threads. These are available to Explorers and above:

* **search\_projects**: Find projects in your Hex workspace
* **create\_thread**: Start a new Thread conversation
* **get\_thread**: Retrieve messages and results from a Thread
* **continue\_thread**: Add follow-up questions to an existing Thread
* **get\_me**: Return the authenticated user and workspace

**Project editing tools** let an agent author and run notebooks. These require the Editor [role](/docs/collaborate/sharing-and-permissions/roles) or above:

* **create\_project** / **get\_project**: Create a project, or read a project's metadata
* **list\_cells**: Read the cells in a project's draft version
* **get\_cell**: Read a single cell by its ID
* **create\_cell** / **update\_cell** / **delete\_cell**: Add, edit, and remove SQL, Python, and Markdown cells
* **run\_cell** / **run\_notebook**: Run a single cell and its dependencies, or the whole draft notebook
* **get\_run** / **get\_cell\_output**: Poll the status of a run, or read a SQL cell's output
* **get\_cell\_image**: Return a rendered PNG of a chart cell
* **list\_data\_connections**: List the workspace's data connections to resolve one by name

It is not currently possible to upload files to your conversation and pass them along to Hex.

## Roles and licensing[​](#roles-and-licensing "Direct link to Roles and licensing")

The knowledge tools require the Explorer [role](/docs/collaborate/sharing-and-permissions/roles) or above. The project editing tools require the Editor role or above, matching the access needed to author projects in the Hex app or through the [CLI](/docs/api-integrations/cli).

An Explorer connected to the MCP server can search projects and run Threads, but cannot create or edit projects.

Workspace roles determine whether a user can edit projects at all. Individual [project permissions](/docs/collaborate/sharing-and-permissions/project-sharing#project-permissions) determine which projects they can edit, and the MCP server enforces both. An agent can read any project the user can view: `get_project`, `list_cells`, and `get_cell` all work with view-level access. Creating, updating, or deleting a cell requires **Can Edit** or **Full Access** on that specific project, and returns a "Not authorized" error otherwise.

info

This applies to workspace Admins as well. The Admin role does not grant edit access to every project in the workspace, so an agent connected as an Admin can still be refused an edit on a project that has not been shared with them.

## Data connection access[​](#data-connection-access "Direct link to Data connection access")

Threads created through the Hex MCP server behave the same as [Threads in the Hex app](/docs/explore-data/threads#data-sources): the agent automatically selects among the data connections the user has access to in order to answer a question. If your workspace has a [default data connection](/tutorials/ai-best-practices/setup-for-ai-agents#setup-the-default-data-connection), the agent searches that connection first.

Admins can mark data connections as **Sensitive** so the Hex Agent treats them carefully in Threads started from external integrations, including the Hex MCP server and [Hex Agent in Slack](/docs/share-insights/hex-agent-in-slack). The MCP server never uses sensitive connections. Configure this under **Settings** → **Integrations** → **Configure sensitive data connections for external integrations**, or on each connection's **Access** tab under **Settings** → **Data sources**. For more information, see [Sensitive data connections for external integrations](/docs/api-integrations/hex-agent-data-connection-access).

For best practices on descriptions, exclusions, and permissions, see [Optimizing your data connections for the Hex Agent](/tutorials/ai-best-practices/optimizing-data-connections-for-agents).

## Configure the Hex MCP Server[​](#configure-the-hex-mcp-server "Direct link to Configure the Hex MCP Server")

### Connect Hex to Claude[​](#connect-hex-to-claude "Direct link to Connect Hex to Claude")

info

Claude owners (on Claude Teams or Enterprise plans) or users (on a Claude Individual plan) can configure the [Hex Connector](https://claude.com/connectors/hex) for their workspace.

#### Add the Hex Connector in Claude[​](#add-the-hex-connector-in-claude "Direct link to Add the Hex Connector in Claude")

1. In Claude, go to **Settings → Connectors → Browse Connectors** and search for "Hex".

2. Add the connector to your team.

3. Set the server URL to `https://app.hex.tech/mcp` and click "Continue".

tip

For single-tenant, EU multi-tenant, or HIPAA multi-tenant customers, replace `app.hex.tech` with your custom Hex URL (e.g., `your-company.hex.tech`, `eu.hex.tech`, `hc.hex.tech`).

info

If you want to connect to multiple workspaces that have different URLs (e.g., `app.hex.tech` vs. `eu.hex.tech`), you can configure additional [custom Claude connectors](https://support.claude.com/en/articles/11175166-getting-started-with-custom-connectors-using-remote-mcp).

#### Use Hex in Claude[​](#use-hex-in-claude "Direct link to Use Hex in Claude")

Once the Hex Connector is [added](#connect-hex-to-claude) by a Claude workspace owner, users can enable it by navigating to **Settings → Connectors** and clicking **Connect** next to the Hex Connector.

Once you open a new chat, ensure that the Hex Connector is toggled on via the **+** icon in the bottom left:

#### Search for projects in Claude[​](#search-for-projects-in-claude "Direct link to Search for projects in Claude")

You can use the Hex Connector to search for relevant projects in your Hex workspace. Claude will return visual project cards that display the project title, description, and other information, including a link to the project in your Hex workspace.

#### Start Threads in Claude[​](#start-threads-in-claude "Direct link to Start Threads in Claude")

You can ask open-ended data questions in your Claude chat, and the Hex Connector will kick off a Thread to answer the question. An interactive widget in the Claude chat will appear and show the Hex Thread's "thinking" steps, allowing you to follow along with the Thread in real time without leaving Claude.

tip

You can click into each "thinking" block in the widget to understand what specific actions the Threads agent took to answer your question.

The Hex Connector will continually make `get_thread` calls without user prompting, checking in on the progress of the Thread and keeping you updated on its analysis. If the Threads agent creates any charts or tables in the course of its analysis, the Hex Connector will surface these as a carousel in an interactive widget in your Claude chat.

Once the Thread has finished its analysis, Claude will summarize its key findings and provide a link to the Thread in your Hex workspace. If you ask a follow-up question, the Hex Connector in Claude will use a `continue_thread` tool call to continue the Thread within the Claude chat.

info

Interactive widgets that are created by the Hex Connector in a Claude chat, including thinking blocks and chart carousels, will expire after 24 hours.

### Connect Hex to Cursor[​](#connect-hex-to-cursor "Direct link to Connect Hex to Cursor")

Cursor supports Hex through the official [Hex plugin](https://cursor.com/marketplace/hex) in the Cursor Marketplace. The official plugin connects to `app.hex.tech` and does not let you specify a custom Hex URL (for example, `eu.hex.tech` or a single-tenant domain).

#### Install the Hex plugin in Cursor[​](#install-the-hex-plugin-in-cursor "Direct link to Install the Hex plugin in Cursor")

*Follow these instructions if you use Hex at `app.hex.tech`.*

1. In Cursor chat, run `/add-plugin hex`, or install from the [Cursor Marketplace](https://cursor.com/marketplace/hex).
2. Complete the OAuth flow to authorize access to your Hex workspace (and specify a workspace if you have access to multiple).

#### Connect via remote MCP[​](#connect-via-remote-mcp "Direct link to Connect via remote MCP")

*Follow these instructions if you use Hex anywhere other than `app.hex.tech`.*

For single-tenant, EU multi-tenant, or HIPAA multi-tenant customers, go to **Settings → Cursor Settings → Tools & MCP** and add the Hex MCP server as a remote MCP server URL. You can also edit your `~/.cursor/mcp.json` file to add Hex as an MCP server:

```
{



"mcpServers": {



"hex": {



"url": "https://app.hex.tech/mcp"



}



}



}
```

tip

Replace `app.hex.tech` with your custom Hex URL (e.g., `your-company.hex.tech`, `eu.hex.tech`, `hc.hex.tech`).

After adding the MCP server, go back to the **Settings** page and select **Connect** to start the OAuth flow. You will be redirected back to our external authentication provider to approve the connection (and specify a workspace if you have access to multiple).

When successfully connected, you should see the connected Hex MCP server and can configure tool permissions under **Tools & MCP**.

#### Use Hex in Cursor[​](#use-hex-in-cursor "Direct link to Use Hex in Cursor")

After installation, start a new chat and ask Cursor to analyze data in Hex, or type `@` to invoke the Hex plugin or one of its bundled skills. You can search for projects, ask data questions, and start Threads. Users with the Editor role or above can also create and modify Hex notebooks, either through the [project editing tools](#project-editing-tools) or through the bundled [Hex CLI](/docs/api-integrations/cli) integration.

### Connect Hex to ChatGPT[​](#connect-hex-to-chatgpt "Direct link to Connect Hex to ChatGPT")

info

On ChatGPT Business and Enterprise workspaces, admins may need to enable the Hex app under **Workspace settings → Apps** before users can connect it.

ChatGPT supports Hex through the official [Hex app](https://chatgpt.com/apps) in the ChatGPT Apps directory. The official app connects to `app.hex.tech` and does not let you specify a custom Hex URL (for example, `eu.hex.tech` or a single-tenant domain).

tip

If your Hex workspace uses a custom URL, connect through a custom MCP connector in [ChatGPT Developer Mode](https://help.openai.com/en/articles/12584461-developer-mode-apps-and-full-mcp-connectors-in-chatgpt-beta/) instead of the official app listing. A workspace admin must enable Developer Mode, then create an app with your Hex MCP server URL (for example, `https://eu.hex.tech/mcp`). Developer Mode is available on Business and Enterprise plans with full MCP support; Plus and Pro users can connect read-only MCP tools.

#### Add the Hex app in ChatGPT[​](#add-the-hex-app-in-chatgpt "Direct link to Add the Hex app in ChatGPT")

1. In ChatGPT, open **Apps** from the sidebar or go to [chatgpt.com/apps](https://chatgpt.com/apps).
2. Search for "Hex" and select the Hex app.
3. Click **Connect** and complete the OAuth flow to authorize access to your Hex workspace (and specify a workspace if you have access to multiple).

#### Use Hex in ChatGPT[​](#use-hex-in-chatgpt "Direct link to Use Hex in ChatGPT")

Once connected, start a new chat and enable the Hex app from the **+** (Tools) menu, or mention `@Hex` in your prompt to invoke it. You can search for projects, ask data questions, and start Threads from your ChatGPT conversation.

### Connect Hex to Codex[​](#connect-hex-to-codex "Direct link to Connect Hex to Codex")

info

On ChatGPT Business and Enterprise workspaces, admins may need to enable the Hex app under **Workspace settings → Apps** before users can install the [Hex plugin](https://developers.openai.com/codex/plugins) in Codex. See [Plugins in Codex](https://help.openai.com/en/articles/20001256-plugins-in-codex) for admin setup details.

#### Install the Hex plugin in Codex[​](#install-the-hex-plugin-in-codex "Direct link to Install the Hex plugin in Codex")

1. In the Codex app, open **Plugins** and search for "Hex".
2. Next to the Hex plugin, select **Connect**.
3. When prompted, connect the bundled Hex app and complete the OAuth flow to authorize access to your Hex workspace.

#### Use Hex in Codex[​](#use-hex-in-codex "Direct link to Use Hex in Codex")

After installation, start a new thread and ask Codex to analyze data in Hex, or type `@` to invoke the Hex plugin or one of its bundled skills. You can search for projects, ask data questions, and start Threads. Users with the Editor role or above can also create and modify Hex notebooks, either through the [project editing tools](#project-editing-tools) or through the bundled [Hex CLI](/docs/api-integrations/cli) integration.

### Connect Hex to Glean[​](#connect-hex-to-glean "Direct link to Connect Hex to Glean")

info

A Glean admin must configure the Hex MCP server in the [Glean Admin Console](https://docs.glean.com/administration/actions/connect-remote-mcp-servers-to-glean) before users can access Hex from Glean Assistant or Glean Agents.

[Glean](https://docs.glean.com/administration/actions/connect-remote-mcp-servers-to-glean) acts as an MCP host, letting admins connect remote MCP servers so users can invoke Hex tools from Glean Assistant and Glean Agents.

#### Add the Hex MCP server in Glean[​](#add-the-hex-mcp-server-in-glean "Direct link to Add the Hex MCP server in Glean")

1. In Glean, open the **Admin Console** and go to **Platform → Actions**.
2. Click **Add**, then either select Hex from the **MCP servers** templates under **Add pre-set actions**, or choose **Import tools from MCP server** to configure it manually:
   * **MCP server URL**: `https://app.hex.tech/mcp`
   * **Transport type**: Streaming HTTP
   * **Authentication method**: OAuth User
3. Click **Connect to server** and complete the OAuth flow.
4. Click **Edit settings** to enable the Hex tools you want to expose in **Glean Assistant** and/or **Agents**, then click **Save**.

tip

For single-tenant, EU multi-tenant, or HIPAA multi-tenant customers, replace `app.hex.tech` with your custom Hex URL (e.g., `your-company.hex.tech`, `eu.hex.tech`, `hc.hex.tech`).

#### Use Hex in Glean[​](#use-hex-in-glean "Direct link to Use Hex in Glean")

Once the MCP action pack is published, users can ask data questions or search for projects in Glean Assistant, or add Hex tools to agent workflows in Agent Builder. On first use, each user completes the OAuth flow to connect their Hex workspace.

### Connect Hex to Figma[​](#connect-hex-to-figma "Direct link to Connect Hex to Figma")

#### Add the Hex Connector in Figma[​](#add-the-hex-connector-in-figma "Direct link to Add the Hex Connector in Figma")

When using the Figma Design Agent, add Hex as a connector — this will prompt you to authenticate. More details can be found in Figma's docs [here](https://help.figma.com/hc/en-us/articles/35440096186007-Use-verified-partner-MCP-connectors-with-the-Figma-agent-and-Figma-Make#h_01KAC4Y0E71YB3NMHJJ9HH4PZ8).

tip

The Hex connector currently only connects to `app.hex.tech`. For single-tenant, EU multi-tenant, or HIPAA multi-tenant customers, ask a Figma Admin to create a custom MCP connector using the URL for your MCP server, e.g. `https://eu.hex.tech/mcp`.

#### Use Hex in Figma[​](#use-hex-in-figma "Direct link to Use Hex in Figma")

To use the connector in chat, call it by @ mentioning Hex, as shown below.

### Connect Hex to other MCP clients[​](#connect-hex-to-other-mcp-clients "Direct link to Connect Hex to other MCP clients")

The Hex MCP server can be used in any MCP clients that supports custom connectors, including internal tools or other tools for which a native integration is not yet available.

To connect to another MCP client, open your configuration file and add the Hex MCP server configuration:

```
{



"mcpServers": {



"hex": {



"url": "https://app.hex.tech/mcp"



}



}



}
```

tip

For single-tenant, EU multi-tenant, or HIPAA multi-tenant customers, replace `app.hex.tech` with your custom Hex URL (e.g., `your-company.hex.tech`, `eu.hex.tech`, `hc.hex.tech`).

After you've added the MCP server to your application, restart the application to apply the configuration. Then, when you first interact with Hex through the MCP, you'll be prompted to authenticate through our external authentication provider.

## Available actions[​](#available-actions "Direct link to Available actions")

### Knowledge tools[​](#knowledge-tools "Direct link to Knowledge tools")

#### Search for projects in your workspace[​](#search-for-projects-in-your-workspace "Direct link to Search for projects in your workspace")

**Input**: Search query to find relevant projects. This action will return both published and unpublished Hex projects.

**Output**:

* `projects` (array): List of matching projects with the following fields:
  + `projectId`: Unique ID for the project
  + `title`: Project title
  + `description`: Project description
  + `generated_summary`: AI-generated summary of the project (if available)
  + `url`: Direct link to the project
  + `type`: Either `"project"` or `"app"`

info

The response structure and fields provided by the call output are subject to change.

#### Create a new Thread[​](#create-a-new-thread "Direct link to Create a new Thread")

Create a new Hex [Thread](/docs/explore-data/threads) to ask questions about your data using the Hex Agent.

**Input**: The question or analysis request for the Hex Agent

**Output**: Confirmation message with Thread ID and Thread URL

info

* MCP Threads can make use of any [non-sensitive](/docs/api-integrations/hex-agent-data-connection-access) data connections that you have access to—you do not need to pick a connection in the client. See [Data sources in Threads](/docs/explore-data/threads#data-sources).
* Threads typically take several minutes to complete as the agent analyzes your data.

#### Get an existing Thread[​](#get-an-existing-thread "Direct link to Get an existing Thread")

Retrieve messages and results from an existing Hex [Thread](/docs/explore-data/threads).

**Input**: Thread ID

**Output**:

If the Thread has not yet completed, the call will return:

* Thread ID
* Thread status
* Wait time

If the Thread has completed, the call will return:

* Recent messages in the Thread conversation
* Any charts, tables, or visualizations generated by the agent
* Link to view the full Thread in Hex

tip

If the Thread hasn't finished, you can call `get_thread` again to check for updates. The tool is designed to be called multiple times until the Thread reaches idle status.

#### Continue an existing Thread[​](#continue-an-existing-thread "Direct link to Continue an existing Thread")

Continue a conversation by providing a new prompt to an existing Hex [Thread](/docs/explore-data/threads).

**Input**: Thread ID, Thread prompt

**Output**:

* Recent messages in the Thread conversation
* Any charts, tables, or visualizations generated by the agent
* Link to view the full Thread in Hex

warning

You can only continue a Thread once it has finished running. If you try to continue a running Thread, you'll receive an error message asking you to wait for the current operation to complete.

info

Threads started through the MCP server are always new, standalone Threads. It is not currently possible to start a Thread on an existing project through the MCP server, or to continue a Thread that was started in the Hex app.

#### Get the current user[​](#get-the-current-user "Direct link to Get the current user")

Return the authenticated user and workspace. Useful for confirming which workspace an agent is connected to, and which role it is operating under.

**Input**: None

**Output**: User ID, name, email, workspace role, and workspace ID

### Project editing tools[​](#project-editing-tools "Direct link to Project editing tools")

These tools let an agent create a project, author its cells, and run it. They require the Editor [role](/docs/collaborate/sharing-and-permissions/roles) or above.

info

Edits made through these tools always apply to a project's **draft** version — the notebook you see in the Hex editor. They do not modify published [app](/docs/share-insights/apps/publish-and-share-apps) versions. To make an agent's work visible to your workspace, publish the project from the Hex app.

#### Create a project[​](#create-a-project "Direct link to Create a project")

Create a new, empty project in the workspace.

**Input**: Project title, and optionally a description

**Output**: The new project, including its ID

#### Get a project[​](#get-a-project "Direct link to Get a project")

Retrieve metadata about a single project.

**Input**: Project ID. Optionally request sharing metadata, which is omitted by default.

**Output**:

* `id`, `title`, `description`, and `type`
* `creator` and `owner`
* `createdAt`, `lastEditedAt`, and `lastPublishedAt` (null if the project has never been published)
* `archivedAt` and `trashedAt`
* `categories`, `status`, `reviews`, and `schedules`
* `analytics`: app view counts and the date the project was last viewed
* `sharing` (only when requested): user, group, collection, workspace, public web, and support access

#### List cells in a project[​](#list-cells-in-a-project "Direct link to List cells in a project")

List the cells in a project's draft version.

**Input**: Project ID. Optionally a page size (25 by default, 100 maximum) and a pagination cursor.

**Output**:

* `values` (array): List of cells, each with the following fields:
  + `id`: The cell's ID within the draft version
  + `staticId`: A stable ID for the cell
  + `cellType`: For example, `SQL`, `CODE`, `MARKDOWN`, or `EXPLORE`
  + `label`: The cell's label, or null if it has none
  + `dataConnectionId`: The attached data connection, or null
  + `contents`: An object with `codeCell`, `sqlCell`, and `markdownCell` keys. All three are always present; the one matching the cell's type holds a `source`, and the others are null. `sqlCell` also carries its `outputDataframe` name.
  + `projectId`: The project the cell belongs to
* `pagination`: `before` and `after` cursors

info

Every cell in the notebook is listed, but `contents` is only populated for code, SQL, and Markdown cells. Other cell types — charts, inputs, and so on — are returned with their type and label, but their configuration is not included and cannot be edited through these tools.

The list is flat and in notebook order. It does not report which cells sit inside a [section](/docs/explore-data/notebook-view/sections), so an agent cannot read a notebook's nesting back out, even though `create_cell` can place a new cell inside a section.

#### Get a cell[​](#get-a-cell "Direct link to Get a cell")

Retrieve a single cell.

**Input**: Cell ID

**Output**: The same cell fields returned by `list_cells`

tip

Read project state before changing it. Calling `get_project` and `list_cells` before `update_cell` or `delete_cell` avoids edits against a stale view of the notebook.

#### List data connections[​](#list-data-connections "Direct link to List data connections")

List the workspace's data connections, so an agent can resolve a connection by name before creating or updating a SQL cell.

**Input**: Optionally a page size (25 by default, 100 maximum), a pagination cursor, and a sort order — by name or creation date, ascending or descending.

**Output**:

* `values` (array): List of data connections. Every connection includes its `id`, `name`, `type`, and `description`. Depending on your access, a connection may also include its connection details, sharing settings, and schema filter and refresh settings.
* `pagination`: `before` and `after` cursors

#### Create a cell[​](#create-a-cell "Direct link to Create a cell")

Add a cell to a project's draft version.

**Input**: Project ID, the cell type, and the matching cell contents:

* **CODE**: A [Python cell](/docs/explore-data/cells/python-cells). Pass the Python source.
* **SQL**: A [SQL cell](/docs/explore-data/cells/sql-cells/sql-cells-introduction). Pass the query source, plus either a data connection ID to query a [data connection](/docs/connect-to-data/data-connections/data-connections-introduction), or a flag to query the results of other SQL cells in the project. These two options are mutually exclusive. You can also set a custom output dataframe name; one is generated automatically if you don't.
* **MARKDOWN**: A [text cell](/docs/explore-data/cells/text-cells). Pass the Markdown source.

You can also pass a label, and a location. By default a new cell is appended to the end of the project; to place it elsewhere, insert it after a specific cell, or add it as a child of a [section](/docs/explore-data/notebook-view/sections) cell at either the beginning or end of that section.

tip

`list_cells` returns the `dataConnectionId` of every SQL cell in a project, so the simplest way to point a new SQL cell at the right warehouse is to reuse the ID from a SQL cell that already queries it. In a new project with no SQL cells yet, use `list_data_connections` to resolve a connection by name.

**Output**: The newly created cell

#### Update a cell[​](#update-a-cell "Direct link to Update a cell")

Update a cell's source. For SQL cells, you can also update the output dataframe name and the data connection.

**Input**: Cell ID and the new contents. For SQL cells, you can also pass a data connection to attach.

**Output**: The updated cell

info

A cell's label cannot be changed after the cell is created. `create_cell` accepts a label, but `update_cell` does not, so an agent that needs a different label must delete the cell and recreate it.

#### Delete a cell[​](#delete-a-cell "Direct link to Delete a cell")

Remove a cell from a project's draft version.

**Input**: Cell ID

caution

Cell edits made through the MCP server apply directly to the project's live draft version. There is no separate staging step, so changes are immediately part of the notebook that collaborators open.

#### Run a cell[​](#run-a-cell "Direct link to Run a cell")

Run a single cell and its upstream dependencies in the draft version. The run is asynchronous.

**Input**: Cell ID. Optionally a dry run, which validates the request without executing it.

**Output**: A `runId` identifying the draft session, and a link to the project in Hex. A dry run returns no `runId`.

For SQL cells, poll `get_cell_output` to read the result or error.

#### Run a notebook[​](#run-a-notebook "Direct link to Run a notebook")

Run the entire draft version of a project. The run is asynchronous.

**Input**: Project ID. SQL cells reuse cached results by default; you can disable this to force fresh queries.

**Output**: A `runId` identifying the draft session, and a link to the project in Hex

Poll `get_run` until the run has finished.

#### Get the status of a run[​](#get-the-status-of-a-run "Direct link to Get the status of a run")

Check the progress of a project run.

**Input**: Project ID and run ID

**Output**: The run's status, along with its `runUrl`, what triggered it, its start and end times, and its elapsed time in milliseconds. The run is finished when the status is `COMPLETED`, `ERRORED`, `KILLED`, or `UNABLE_TO_ALLOCATE_KERNEL`.

#### Get the output of a cell[​](#get-the-output-of-a-cell "Direct link to Get the output of a cell")

Read the latest output preview for a SQL cell in the active draft notebook session.

**Input**: Cell ID

**Output**: The cell's most recent output preview, or its error. The preview returns a limited number of rows and reports the row limit, the number of rows returned, the total row count, and whether the result was truncated — so an agent can tell when it is not seeing the full result. Columns are never dropped.

tip

Poll `get_run` or `get_cell_output` every five seconds until the run has finished.

caution

The `runId` identifies the long-running draft session, not a single execution, so it can correlate with earlier runs of the same project. If the project ran recently, confirm the reported start time is at or after your request before trusting that the run has finished — and after editing a cell, confirm the output you read reflects the new source rather than the previous execution.

#### Get a chart image[​](#get-a-chart-image "Direct link to Get a chart image")

Retrieve a rendered PNG image of a [chart cell](/docs/explore-data/cells/visualization-cells/chart-cells).

**Input**: The cell's ID — either its draft version ID or its static ID. Optionally an image width and height in pixels (between 100 and 2000 — both must be provided to take effect), and whether to include the chart title.

**Output**: The chart rendered as a PNG image

The cell must live in the project's draft version, must already have been executed, and must not be in an error state. Only chart cells are supported; calling it on a SQL or Python cell returns an error. If the cell has not been run, the call returns an error explaining that no image could be generated. `get_thread` also reports the cell ID of each chart in a Thread, so charts produced by the Hex Agent can be fetched this way too.

tip

Some MCP clients, including Claude, render Hex charts natively in an interactive widget. `get_cell_image` is most useful for clients that don't support those widgets, and for agents that need to reason about a chart's appearance. Omit the width and height unless you need more detail: the default image is tens of kilobytes, while a dense chart at the maximum 2000x2000 can exceed 500KB. Request one chart at a time.

## Example workflows[​](#example-workflows "Direct link to Example workflows")

### Asking a data question[​](#asking-a-data-question "Direct link to Asking a data question")

A typical workflow for asking a data question through the MCP server:

1. **User asks a question**:

   ```
   What were our top-selling products last quarter?
   ```
2. **AI assistant creates a Thread**:

   * Uses `create_thread` with the user's question
   * Receives a Thread ID and URL
3. **AI assistant monitors progress**:

   * Calls `get_thread` periodically
   * Checks if status is complete or still processing
   * Shows the user what the agent is thinking
4. **AI assistant returns results**:

   * Presents the agent's analysis, charts, and insights
   * Provides a link to view the full Thread in Hex
5. **User asks a follow-up**:

   ```
   Can you break that down by sales channel?
   ```
6. **AI assistant continues the conversation**:

   * Uses `continue_thread` with the follow-up question
   * Monitors with `get_thread` until complete
   * Presents the updated analysis

### Finding and exploring projects[​](#finding-and-exploring-projects "Direct link to Finding and exploring projects")

To help users discover relevant work:

1. **User asks about existing analysis**:

   ```
   Do we have any projects about customer segmentation?
   ```
2. **AI assistant searches**:

   * Uses `search_projects` with query "customer segmentation"
3. **AI assistant presents results**:

   * Shows project titles, descriptions, and generated summaries
   * Provides direct links to open projects in Hex
4. **User can create a new Thread**:

   * If they want to ask questions about the data in those projects
   * The AI assistant uses `create_thread` to start the analysis

### Building a project[​](#building-a-project "Direct link to Building a project")

A typical workflow for having an agent build a working notebook:

1. **User describes what they want**:

   ```
   Build me a Hex project that tracks weekly active users by plan tier.
   ```
2. **AI assistant creates the project**:

   * Uses `create_project` with a title and description
   * Receives the new project's metadata, including its `projectId`
3. **AI assistant authors the notebook**:

   * Uses `create_cell` to add a Markdown cell describing the analysis
   * Adds a SQL cell with a `dataConnectionId`, naming the output dataframe
   * Adds a Python cell that reads that dataframe and builds the aggregation
4. **AI assistant runs the notebook**:

   * Calls `run_notebook` and receives a `runId`, along with a link to the project in Hex
   * Polls `get_run` until the run has finished
   * If a SQL cell errored, reads the error with `get_cell_output`, fixes the query with `update_cell`, and re-runs
5. **AI assistant reviews the result**:

   * Reads the SQL cell's output with `get_cell_output` to confirm the numbers look right
   * Shares the project link so the user can review, add charts, and publish it in Hex

tip

Editing an existing project follows the same shape, but starts with `get_project` and `list_cells` so the agent is working from the notebook's current state rather than guessing at it.

#### On this page

* [Overview](#overview)
* [Roles and licensing](#roles-and-licensing)
* [Data connection access](#data-connection-access)
* [Configure the Hex MCP Server](#configure-the-hex-mcp-server)
  + [Connect Hex to Claude](#connect-hex-to-claude)
  + [Connect Hex to Cursor](#connect-hex-to-cursor)
  + [Connect Hex to ChatGPT](#connect-hex-to-chatgpt)
  + [Connect Hex to Codex](#connect-hex-to-codex)
  + [Connect Hex to Glean](#connect-hex-to-glean)
  + [Connect Hex to Figma](#connect-hex-to-figma)
  + [Connect Hex to other MCP clients](#connect-hex-to-other-mcp-clients)
* [Available actions](#available-actions)
  + [Knowledge tools](#knowledge-tools)
  + [Project editing tools](#project-editing-tools)
* [Example workflows](#example-workflows)
  + [Asking a data question](#asking-a-data-question)
  + [Finding and exploring projects](#finding-and-exploring-projects)
  + [Building a project](#building-a-project)