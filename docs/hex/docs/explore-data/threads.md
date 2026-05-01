On this page

# Threads

With Threads, users can ask natural language questions and get AI-powered insights based on semantic models and warehouse tables, all in a conversational interface.

The Threads agent heavily prioritizes semantic models and [endorsed](/docs/organize-content/statuses-categories#endorsed-statuses) data sources in order to provide high quality answers.

[](/assets/medias/threads-preview-bee1820de1759cfdd8e4d93e134c806c.mp4)

info

* Threads is available in public **Beta** on the [Team and Enterprise plans](https://hex.tech/pricing/), which include monthly per-seat [credit grants](/docs/administration/credits) that can be used towards Hex AI features. While Hex agents are in Beta, credit limits and optional add-on credits are being rolled out in phases and are not yet enforced for all customers. Admins will receive advance notice before limits go into effect for their workspace.
* Users require an [Explorer role](/docs/collaborate/sharing-and-permissions/roles) or higher to use Threads.
* Users with any role except [Guest](/docs/collaborate/sharing-and-permissions/roles) can view Threads shared with them.

## Threads quickstart guide[​](#threads-quickstart-guide "Direct link to Threads quickstart guide")

Threads allow users with the [Explorer role](/docs/collaborate/sharing-and-permissions/roles) or higher to interact with your data conversationally without thinking about code. Here’s a quick checklist for how to get things set up and ensure Threads generate high quality responses:

1. **[Endorse workspace assets with statuses](/docs/organize-content/statuses-categories#using-statuses-and-categories):** Endorsed data & projects are prioritized by all agents to allow more fine-grained control over the self-serve experience and improve response quality from Threads. Admins and Editors can use Threads with endorsed assets prioritized. Enabling [Endorsed Mode](/docs/organize-content/statuses-categories#endorsed-mode) restricts the agent to using only endorsed assets, while turning this off allows the Agent to access all data (with endorsed assets prioritized). By default, Explorers can only use Threads in Endorsed Mode, but Admins can disable this enforcement in [**Settings > AI & agents**](/docs/administration/workspace_settings/enable-ai-and-agents). Start endorsing data and projects to make it easier for agents to know which data is prioritized when answering questions.
2. **[Contribute to Agent Workspace Rules](/docs/agent-management/context-management/guides):** If you want to guide agents with information about your organization or other high-level context about when to use which data, you can add to the Agent Workspace Rules.
3. **[Curate context to improve AI results](/tutorials/ai-best-practices/setup-for-ai-agents):** Provide Hex agents with a focused view on relevant information, leading to more accurate suggestions. Limiting, excluding, or endorsing data helps agents more precisely find what they're looking for.

## Where to find Threads[​](#where-to-find-threads "Direct link to Where to find Threads")

### Within Hex[​](#within-hex "Direct link to Within Hex")

If creating Threads is enabled for a given user, they will see a prompt bar on the homepage. Entering a prompt from the homepage will create a new Thread.

All users will have access to a Threads page on the left side of their homepage. Users without the ability to create threads will see threads that have been [shared](#sharing) with them in this page. Users with the ability to create threads will also see threads they've created in this list and can use a **New thread** button.

All users will see recently created threads that they have access to in the "Jump Back In" section of their homepage.

### Slack[​](#slack "Direct link to Slack")

Hex’s [Slack integration](/docs/share-insights/hex-agent-in-slack) enables you to interact with Hex Threads directly in your Slack workspace. As part of the agent's response in public and private Slack channels, the Hex Agent will return a Threads link.

### MCP Server[​](#mcp-server "Direct link to MCP Server")

The Hex Model Context Protocol ([MCP server](/docs/api-integrations/mcp-server)) enables AI assistants like Claude and Cursor to interact directly with your Hex workspace.

### CLI[​](#cli "Direct link to CLI")

Hex's Command Line Interface ([CLI](/docs/api-integrations/cli)) can be used directly or via a local AI agent to automate Hex workflows, inspect workspace state, and more.

## Data sources[​](#data-sources "Direct link to Data sources")

To answer a user's question, the agent searches across all connections, databases, schemas, and tables that are [included for AI](/docs/explore-data/data-browser#exclusion-and-endorsement) and that the user has access to. It uses connection names, descriptions, and schema metadata to determine which connection contains the relevant data, and can query multiple connections within a single conversation if needed. If your workspace has a default data connection, the agent will search it first before looking at other available connections.

Users can steer the agent toward a particular connection by selecting one via the + menu in the prompt bar. The agent will prioritize that connection first, but can switch to or add other connections in the same conversation when useful.

To understand how to optimize your data connections for the agent, check out our [Optimizing your data connections for the Hex Agent](/tutorials/ai-best-practices/optimizing-data-connections-for-agents) tutorial.

### Endorsed Mode on: Agent can access endorsed assets only[​](#endorsed-mode-on-agent-can-access-endorsed-assets-only "Direct link to Endorsed Mode on: Agent can access endorsed assets only")

When the agent is restricted to only use endorsed assets, Threads will only search for endorsed projects and data in your workspace as context to inform how it answers questions.

### Endorsed Mode off: Agent can access all data[​](#endorsed-mode-off-agent-can-access-all-data "Direct link to Endorsed Mode off: Agent can access all data")

When the agent is not restricted to only use endorsed data, Threads will still prioritize endorsed data when relevant, but can access all data in the connection. Threads will also use metadata like column and table descriptions and [data endorsements](/docs/organize-content/statuses-categories#endorsed-statuses) as context to inform how it answers questions.

## Threads behavior and exploring[​](#threads-behavior-and-exploring "Direct link to Threads behavior and exploring")

To use Threads, it's as simple as asking a question in the prompt bar. After you hit enter on your question, Threads will display the agent's thinking text and show you the tools the agent is calling, as well as the results of those tool calls, in real time.

[](/assets/medias/threads-demo-e34da037ef13bc3941d3d8feb6f136ed.mp4)

The agent has a search tool to find existing published apps in the workspace that may answer the user's question. The tool call searches the workspace for published apps, prioritizing [endorsed](/docs/organize-content/statuses-categories#endorsed-statuses) projects, and the agent judges whether the projects are relevant enough to the user's question. If the agent deems any published apps to be useful, the agent will return the published apps to the user as part of its response. The agent will not look at any unpublished projects.

Other examples of tools include searching for semantic columns, creating visualizations, generating and executing SQL, and looking at visualization results.

When the agent returns a response, the tool calls and thinking text will be collapsed automatically. You can always expand the tool calls and thinking text to understand how the agent arrived at a particular result.

In the agent response, the agent will typically explain the logic it used to arrive at the returned insight, and share results in the form of tables, pivots, and visualizations. Users can interact with results in similar ways that they'd interact with a published app; they can hover over visualizations for tooltips, and explore from cells to make tweaks to visualizations the agent produces. For example, if the agent produces a stacked bar chart to visualize a result, a user could continue analysis manually by exploring from the chart to change the field that is colored by, and change the visualization type.

Of course, users can also ask follow up questions in their threads to tweak results.

If there is a particular data source you want the agent to use when answering your question, you can tag data sources with `@` in your prompt.

### Projects as context[​](#projects-as-context "Direct link to Projects as context")

When answering questions, the agent will search across the workspace for relevant projects on its own, prioritizing [Endorsed](/docs/organize-content/statuses-categories#endorsed-statuses) projects - and if [Endorsed Mode](/docs/organize-content/statuses-categories#endorsed-mode) is enabled, surfacing only those. When the Agent uses a project, it will cite what it used (e.g. links to the project or specific cells) so you can see where the answer came from. Users can also @-mention or paste a URL from a specific project into their prompt to focus the agent's work.

To influence which projects the agent surfaces, optimize the following metadata on your projects:

* **Title** — use clear, descriptive names that reflect the project's content
* **Description** — summarize what the project covers and when it's useful
* [**Category**](/docs/organize-content/statuses-categories#categories) — tag it appropriately so the agent can match it to relevant questions
* [**Endorsed status**](/docs/organize-content/statuses-categories#endorsed-statuses) — mark high-quality projects as Endorsed to ensure the agent prioritizes them. This also allows them to be surfaced in [Endorsed Mode](/docs/organize-content/statuses-categories#endorsed-mode).

info

The agent can surface all projects that you have [Can view app](/docs/collaborate/sharing-and-permissions/project-sharing#can-view-app) or higher access to, but can only view the source code and outputs for projects you have [Can explore](/docs/collaborate/sharing-and-permissions/project-sharing#can-explore) or higher access to.

In order to view a Thread that has been shared with you, you must have at least [Can view results](/docs/connect-to-data/data-connections/data-connections-introduction#can-view-results) access on all data connections that were used in the Thread, including data connections used in the projects the agent used as context.

## Uploading files[​](#uploading-files "Direct link to Uploading files")

info

File uploads in Threads requires the [allow file uploads setting](/docs/administration/workspace_settings/workspace-security#allow-file-uploads) to be turned on.

Upload files to bring external context into Hex quickly. Add a file or image, and the agent can reference it for analysis, summaries, and answers.

### CSV[​](#csv "Direct link to CSV")

Upload and analyze CSV data with Threads. Users can upload CSVs and the agent can craft queries based on the file provided. The agent is also capable of joining the CSV data with existing warehouse data, enabling cross-source insights through a simple file upload.

### Images[​](#images "Direct link to Images")

Upload an image to be used in analysis. Agents can use it to answer questions, extract details, and incorporate the asset into the analysis.

## Sharing[​](#sharing "Direct link to Sharing")

To share, open the **Share** modal in the upper right.

Threads shared with other users are read-only. In the modal, choose to share the thread with individual users, groups of users, or with the entire workspace. A recipient will only be able to view a thread that has been shared with them if they have [Can view results](/docs/connect-to-data/data-connections/data-connections-introduction#can-view-results) access on all data connections that were used in the Thread, including data connections used in the projects the agent used as context.

When a recipient views a Thread that has been shared with them, they will be able to fully interact with the Thread, including exploring from results and expanding tool calls/thinking text. The recipient will be able to see the prompts the sharer has sent. The recipient will not be able to continue the Thread with their own prompts; additional prompts can only be sent by the Thread owner.

If further prompts are sent and analysis is performed in a Thread that has been shared with users, recipients will be able to see the Thread update in real time.

## Saving as a project[​](#saving-as-a-project "Direct link to Saving as a project")

Users with Editor roles or higher will be able to save a Thread as a project. This gives users a familiar environment to review and understand the logic the agent used to produce Thread results. The prompt history will be included in a markdown cell at the top of the project to maintain context. Saving a Thread as a project will copy the underlying logic from the Thread at the time it is saved; further changes made to the Thread will not be reflected in the saved project.

## Sensitive Threads[​](#sensitive-threads "Direct link to Sensitive Threads")

Sensitive threads allow users to ask sensitive questions while reducing their visibility to workspace admins. When a thread is marked as sensitive, its contents are hidden in Context Studio - admins can see that the thread exists, along with the creator and timestamp, but not the messages themselves. Sensitive threads otherwise behave like regular threads. Workspace admins can still access the full contents if they have a direct link to the thread, so sensitive mode does not guarantee absolute privacy.

We recommend that users only use sensitive threads when necessary, because it makes it more difficult for your admins to monitor and improve agent behavior for your workspace.

## OAuth and Threads[​](#oauth-and-threads "Direct link to OAuth and Threads")

When using Threads with an OAuth data connection, the user's personal credentials will be used to execute SQL queries. If the data connection has [credential sharing enabled for notebooks](/docs/connect-to-data/data-connections/oauth-data-connections#credential-sharing), threads can be [shared](#sharing) with other users in the workspace. Recipients of shared Threads will see the outputs that were created using the Thread creator's OAuth credentials.

If the data connection has [credential sharing disabled for notebooks](/docs/connect-to-data/data-connections/oauth-data-connections#credential-sharing), users will not be able to share threads they've created with any other users in the workspace.

## Improving Threads results[​](#improving-threads-results "Direct link to Improving Threads results")

Workspace Managers and Admins can curate context in the workspace to continually improve Threads results. Workspace Managers and Admins can add context in the form of [semantic projects](/docs/connect-to-data/semantic-models/semantic-authoring/semantic-authoring-overview), [project and data endorsements](/docs/agent-management/context-management/guides), [data metadata](/docs/explore-data/data-browser#schema-metadata), and the [agent rules file](/docs/agent-management/context-management/guides). Read more about curating context to improve AI results in Hex [here](/tutorials/ai-best-practices/setup-for-ai-agents).

#### On this page

* [Threads quickstart guide](#threads-quickstart-guide)
* [Where to find Threads](#where-to-find-threads)
  + [Within Hex](#within-hex)
  + [Slack](#slack)
  + [MCP Server](#mcp-server)
  + [CLI](#cli)
* [Data sources](#data-sources)
  + [Endorsed Mode on: Agent can access endorsed assets only](#endorsed-mode-on-agent-can-access-endorsed-assets-only)
  + [Endorsed Mode off: Agent can access all data](#endorsed-mode-off-agent-can-access-all-data)
* [Threads behavior and exploring](#threads-behavior-and-exploring)
  + [Projects as context](#projects-as-context)
* [Uploading files](#uploading-files)
  + [CSV](#csv)
  + [Images](#images)
* [Sharing](#sharing)
* [Saving as a project](#saving-as-a-project)
* [Sensitive Threads](#sensitive-threads)
* [OAuth and Threads](#oauth-and-threads)
* [Improving Threads results](#improving-threads-results)