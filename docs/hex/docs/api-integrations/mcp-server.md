On this page

# Hex MCP Server

Connect AI assistants to Hex through the Model Context Protocol (MCP).

info

* Available on the Team and Enterprise [plans](https://hex.tech/pricing/).
* Hex MCP Server works with Claude Desktop, Claude Code, and Cursor, as well as most standard MCP clients.
* Users will need the Explorer workspace [role](/docs/collaborate/sharing-and-permissions/roles) or higher to use the Hex MCP Server.
* Hex MCP server is currently in beta.

## Overview[​](#overview "Direct link to Overview")

The Model Context Protocol (MCP) allows AI applications to securely connect to external data sources and tools. The Hex MCP server enables AI assistants like Claude to interact directly with your Hex workspace. Through the MCP server, AI assistants can search your projects, create and continue [Threads](/docs/explore-data/threads) conversations, and help you explore your data through natural language.

The Hex MCP server provides four [Tools](#available-actions):

* **search\_projects**: Find projects in your Hex workspace
* **create\_thread**: Start a new Thread conversation
* **get\_thread**: Retrieve messages and results from a Thread
* **continue\_thread**: Add follow-up questions to an existing Thread

The Hex MCP Server can only answer text-based prompts, it is not currently possible to upload files to your conversation and pass them along to Hex.

## Data connection access[​](#data-connection-access "Direct link to Data connection access")

Threads created through Hex MCP Server behave the same as [Threads in the Hex app](/docs/explore-data/threads#data-sources): the agent automatically selects among the data connections the user has access to in order to answer a question. If your workspace has a [default data connection](/tutorials/ai-best-practices/setup-for-ai-agents#setup-the-default-data-connection), the agent searches that connection first.

Admins can restrict which data connections the Hex Agent may use when Threads are started from external integrations, including the Hex MCP Server and [Hex Agent in Slack](/docs/share-insights/hex-agent-in-slack), under **Settings** → **Integrations** → **External integration data connection access**, or on each connection's **Access** tab under **Settings** → **Data sources**. For more information, see [Hex Agent data connection access](/docs/api-integrations/hex-agent-data-connection-access).

For best practices on descriptions, exclusions, and permissions, see [Optimizing your data connections for the Hex Agent](/tutorials/ai-best-practices/optimizing-data-connections-for-agents).

## Configure the Hex MCP Server[​](#configure-the-hex-mcp-server "Direct link to Configure the Hex MCP Server")

### Connect to Claude[​](#connect-to-claude "Direct link to Connect to Claude")

info

Claude owners (on Claude Teams or Enterprise plans) or users (on a Claude Individual plan) can configure the [Hex Connector](https://claude.com/connectors/hex) for their workspace.

#### Add the Hex Connector to your Claude Workspace[​](#add-the-hex-connector-to-your-claude-workspace "Direct link to Add the Hex Connector to your Claude Workspace")

1. In Claude, go to **Settings > Connectors > Browse Connectors** and search for "Hex".

2. Add the connector to your team.

3. Set the server URL to `https://app.hex.tech/mcp` and click "Continue".

tip

For single tenant, EU multi-tenant, or HIPAA multi-tenant customers, replace `app.hex.tech` with your custom Hex URL (e.g., `your-company.hex.tech`, `eu.hex.tech`, `hc.hex.tech`).

info

If you want to connect to multiple workspaces that have different URLs (e.g. `app.hex.tech` vs `eu.hex.tech`), you can configure additional [custom Claude connectors](https://support.claude.com/en/articles/11175166-getting-started-with-custom-connectors-using-remote-mcp).

#### How to use the Hex Connector in Claude[​](#how-to-use-the-hex-connector-in-claude "Direct link to How to use the Hex Connector in Claude")

Once the Hex Connector is [added](#connect-to-claude) by a Claude workspace owner, users can enable it by navigating to Settings -> Connectors and clicking "Connect" next to the Hex Connector.

Once you open a new chat, you should ensure that the Hex Connector is toggled on via the ‘+’ icon in the bottom left:

#### Search for existing projects[​](#search-for-existing-projects "Direct link to Search for existing projects")

You can use the Hex Connector to search for relevant projects in your Hex workspace. Claude will return visual project cards that display the project title, description, and other information and include a link to the project in your Hex workspace.

#### Threads in the Hex Connector in Claude[​](#threads-in-the-hex-connector-in-claude "Direct link to Threads in the Hex Connector in Claude")

You can ask open ended data questions in your Claude chat, and the Hex Connector will kick off a Thread to answer the question. An interactive widget in the Claude chat will appear and show the Hex Threads “thinking” steps, allowing you to follow along with the Thread in realtime without leaving Claude.

tip

You can click into each “thinking” block in the widget to understand what specific actions the Threads agent took to answer your question.

The Hex Connector will continually make `get_thread` calls without user prompting, checking in on the progress of the Thread and keeping you updated on its analysis. If the Threads agent creates any charts or tables in the course of its analysis, the Hex Connector will surface these as a carousel in an interactive widget in your Claude chat.

Once the Thread has finished its analysis, Claude will summarize its key findings and provide a link to the Thread in your Hex workspace. If you ask a follow up question, the Hex Connector in Claude will use a `continue_thread` tool call to continue the Thread within the Claude chat.

info

Interactive widgets that are created by the Hex Connector in a Claude chat, including thinking blocks and chart carousels, will expire after 24 hours.

### Connect to Cursor[​](#connect-to-cursor "Direct link to Connect to Cursor")

In Cursor settings, go to **Settings > Cursor Settings > Tools & MCP**.

From **Tools & MCP** Settings, add the Hex MCP server as a remote MCP server URL: `https://app.hex.tech/mcp` so Hex can connect via OAuth. You can also directly edit your `~/.cursor/mcp.json` file to add Hex as an MCP:

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

For single tenant, EU multi-tenant, or HIPAA multi-tenant customers, replace `app.hex.tech` with your custom Hex URL (e.g., `your-company.hex.tech`, `eu.hex.tech`).

After adding the MCP server, go back to the **Settings** page and select **Connect** to start the OAuth flow. You will be redirected back to our external authentication provider to approve the connection (and specify a workspace if you have access to multiple).

When successfully connected, you should see the connected Hex MCP and you can configure tool permissions under **Tools & MCP**.

### Connect to other MCP Clients[​](#connect-to-other-mcp-clients "Direct link to Connect to other MCP Clients")

Hex MCP Server can be used by MCP Clients other than Claude and Cursor. Any tool that supports MCP integrations can be linked to the Hex MCP Server, including internal tools or other tools for which a native integration is not yet available.

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

After you've added the MCP server to your application, restart the application to apply the configuration. Then, when you first interact with Hex through the MCP, you'll be prompted to authenticate through our external authentication provider.

tip

The Hex ChatGPT Connector has been temporarily de-listed due to recurring bugs in ChatGPT. We will re-list the Hex ChatGPT Connector here when it's recommended for use.

## Available actions[​](#available-actions "Direct link to Available actions")

### Search for projects in your workspace[​](#search-for-projects-in-your-workspace "Direct link to Search for projects in your workspace")

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

### Create a new Thread[​](#create-a-new-thread "Direct link to Create a new Thread")

Create a new Hex [Thread](/docs/explore-data/threads) to ask questions about your data using the Hex Agent.

**Input**: The question or analysis request for the Hex Agent

**Output**: Confirmation message with Thread ID and Thread URL

info

* MCP Threads can make use of any data connections that you have access to and are [accessible from external integrations](/docs/api-integrations/hex-agent-data-connection-access) - you do not need to pick a connection in the client. See [Data sources in Threads](/docs/explore-data/threads#data-sources).
* Threads typically take several minutes to complete as the agent analyzes your data

### Get an existing Thread[​](#get-an-existing-thread "Direct link to Get an existing Thread")

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

### Continue an existing Thread[​](#continue-an-existing-thread "Direct link to Continue an existing Thread")

Continue a conversation by providing a new prompt to an existing Hex [Thread](/docs/explore-data/threads).

**Input**: Thread ID, Thread prompt

**Output**:

* Recent messages in the Thread conversation
* Any charts, tables, or visualizations generated by the agent
* Link to view the full Thread in Hex

warning

You can only continue a Thread once it has finished running. If you try to continue a running Thread, you'll receive an error message asking you to wait for the current operation to complete.

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

#### On this page

* [Overview](#overview)
* [Data connection access](#data-connection-access)
* [Configure the Hex MCP Server](#configure-the-hex-mcp-server)
  + [Connect to Claude](#connect-to-claude)
  + [Connect to Cursor](#connect-to-cursor)
  + [Connect to other MCP Clients](#connect-to-other-mcp-clients)
* [Available actions](#available-actions)
  + [Search for projects in your workspace](#search-for-projects-in-your-workspace)
  + [Create a new Thread](#create-a-new-thread)
  + [Get an existing Thread](#get-an-existing-thread)
  + [Continue an existing Thread](#continue-an-existing-thread)
* [Example workflows](#example-workflows)
  + [Asking a data question](#asking-a-data-question)
  + [Finding and exploring projects](#finding-and-exploring-projects)