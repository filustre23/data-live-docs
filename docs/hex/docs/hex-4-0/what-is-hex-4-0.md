On this page

# What is Hex 4.0?

info

* Hex 4.0 is available to all workspaces as a public beta. If you have not signed an order form to use Hex, a workspace **Admin** will need to email [beta@hex.tech](mailto:beta@hex.tech) to receive access.
* Some features from classic projects aren't yet supported. See [Limitations](#limitations) below.
* Users need an **Editor** role or higher to create 4.0 projects during the beta period.

Hex 4.0 is the next major version of Hex, built to embrace AI agents and code, with the context and controls necessary to make it work for your company at scale. With 4.0, it’s easier than ever to ask questions using Hex’s UI or via external agents, then publish and share your work securely. We've built a new, first-class UI purpose-built for reviewing agent-generated code, so users can understand how results were derived and know whether to trust outputs. 4.0 projects run on an all-new execution engine, so apps load and respond faster, which also lays the foundation for new exciting workflows that weren’t possible before. Read more about [the vision behind 4.0 in our blog](https://hex.tech/blog/introducing-hex-4-0/), or keep reading to see how 4.0 projects work.

## Projects in Hex 4.0[​](#projects-in-hex-40 "Direct link to Projects in Hex 4.0")

Under the hood, 4.0 projects are defined entirely by code. The code lives in a file directory, which both the Hex agent and external agents read from and write to. You don't need to interface with these files of code to use 4.0 projects - we've built a beautiful UI to help you understand and update the logic the agent generates.

### Create a 4.0 project[​](#create-a-40-project "Direct link to Create a 4.0 project")

To create a new 4.0 project, select **New 4.0 project** from the **+** menu on the home page.

While in the beta stage, users with Editor roles or higher can create 4.0 projects.

Prompt the Hex agent to ask a data question or build an app. You can also start from one of our pre-built templates, such as a dashboard, data story, data explorer, what-if analysis, or slides.

tip

4.0 projects can also be created using an external agent, such as Claude, Codex, and Cursor, connected through the [Hex MCP server](/docs/api-integrations/mcp-server). See [Work with external agents via the MCP](#work-with-external-agents-via-the-mcp).

## Work in 4.0 projects[​](#work-in-40-projects "Direct link to Work in 4.0 projects")

### Work with the Hex agent[​](#work-with-the-hex-agent "Direct link to Work with the Hex agent")

Use the Hex agent to answer quick questions, perform deep analysis, and create beautiful data apps.

Projects can be edited within Hex's UI using the Hex agent, or via an external agent of choice connected through the Hex MCP server. Both approaches use your workspace's context, including [semantic models](/docs/connect-to-data/semantic-models/intro-to-semantic-models), [endorsed data](/docs/agent-management/context-management/endorsements-in-context-studio), and [workspace guides](/docs/agent-management/context-management/guides).

[](/assets/medias/prompt-in-action-d3132c5ddcd893a570b63fb07de1af0b.mp4)

#### Query semantic models[​](#query-semantic-models "Direct link to Query semantic models")

In Hex 4.0, you can query [semantic models](/docs/connect-to-data/semantic-models/intro-to-semantic-models) using YAML-based semantic queries instead of Explore cells. When you ask the Hex agent a question that your semantic models can answer, it generates a semantic query, which Hex translates into SQL and runs against your data warehouse.

Semantic queries are saved as `.query.yml` files and return tables you can use throughout your project. You can inspect and edit the YAML directly, or let the agent handle it for you.

For example, this query uses the `pizza_bytes` semantic project to calculate total revenue by pizza type, using a measure and dimension defined in the semantic model.

For configuration options and supported syntax, see the [Semantic query reference](/docs/hex-4-0/semantic-models-in-hex-4-0).

#### Notebook view

The project's Notebook view displays the SQL, Python, and TypeScript logic that underlies a 4.0 project. Users can [manually edit and add cells](#edit-manually) in this view.

[](/assets/medias/4-0-notebook-cells-6281668db7e87df64a2be4d76a40f244.mp4)

#### Generative apps

Generative apps in 4.0 Projects give you full control over presentation and styling, while also providing workflows to inspect and understand the logic behind every element.

As with our existing generative apps, you can prompt the main agent for sweeping style changes, use [quick edits](/docs/share-insights/apps/generative-apps#quick-edits) for targeted quick changes, use [chart controls](#edit-manually) for last-mile manual tweaks, and edit text in-place.

### Inspect agent outputs[​](#inspect-agent-outputs "Direct link to Inspect agent outputs")

Our new **Inspect** view gives you a way to immediately understand the work an agent did to arrive at a given result. Using **Edit** mode, select any element in a generative app and click the **Inspect** view to get a high-level text summary of the underlying logic, all underlying data sources, and a summarized view of the upstream lineage. Use one click to dig deeper and reveal the exact code used. For the highest level of detail, click through to the Notebook view for a full-screen UI with all the inputs and outputs.

[](/assets/medias/inspect-agent-outputs-aba5ba0482934552431a0ae6c6b17bd3.mp4)

#### Use the Graph and Outline views

Use **Preview** mode to preview any interactivity you've built into your app before publishing.

The **Graph** view is accessible from the Notebook in a 4.0 Project. It shows how the cells in a project relate to one another, and offers an easy way to understand the how specific pieces of logic interact and build off of each other. Use the **Lineage** view to focus on a specific subset of related cells.

[](/assets/medias/use-the-graph-view-5c91b24f0012b0f0365e13906de725b9.mp4)

The **Outline** view lists the cells in the Notebook and can be used for quick navigation and organization. Click on a specific cell to focus on it in the UI, and use the **Lineage** view to understand how it interacts with upstream and downstream cells.

[](/assets/medias/use-the-outline-view-a79449b6e2e8eeee749a6982b97757ae.mp4)

### Edit manually[​](#edit-manually "Direct link to Edit manually")

You can make direct edits to the app without prompting the agent with point-and-click chart controls. From the **App** view, select a chart and then select **Style** to open up the style pane. Any chart styling options that are missing can be added by prompting the agent!

[](/assets/medias/manual-chart-controls-27fd58d071cc953afd6c68c9accdc717.mp4)

It's also possible to edit logic directly and add cells manually in the **Notebook** view. Hover over the **Add Cell** bar in between any two cells and select from SQL, Python, or Typescript cells.

[](/assets/medias/add-and-edit-cells-manually-f74a005f773b8a4c976a9748afbb7810.mp4)

#### View and edit the underlying code files

4.0 Projects are defined entirely by files of code, which is the format agents work with best when reading and editing Hex projects. We believe interacting with raw code files isn’t the most efficient way for humans to work, which is why we built the Notebook UI and Inspect workflows to help you review agent-generated logic and develop it yourself. If you'd like to view and edit the underlying files directly, you can do so by opening the dropdown menu next to the project title and selecting "View project files".

[](/assets/medias/inspect-project-files-9b3ffae8016ac6dc8e9560dce7459554.mp4)

## Work with external agents via the MCP[​](#work-with-external-agents-via-the-mcp "Direct link to Work with external agents via the MCP")

Connect your preferred external agent of choice to Hex through the [Hex MCP server](/docs/api-integrations/mcp-server#configure-the-hex-mcp-server) to create, edit, and publish 4.0 projects.

info

**What about the CLI?** 4.0 support for the CLI is in progress and coming soon! In the meantime, we encourage you to try the MCP; creating, editing, and publishing projects are all now possible via the MCP.

Using the MCP, external agents can:

* **Use your workspace context**, including workspace guides, semantic models, table schemas, and existing projects
* **Build 4.0 projects** on your workspace's [data connections](/docs/connect-to-data/data-connections/data-connections-introduction)
* **Check their work** by running queries and previewing the app before it's shared
* **Publish apps** that others open in Hex, with your workspace's permissions
* **Bring existing work into Hex**, such as rebuilding a dashboard created in Claude as a 4.0 project
* **Put data behind a decision:** “Here’s our expansion plan. Use Hex to check which customer segments have the strongest growth and retention.”
* **Go from answer to app:** “Why did revenue drop last quarter? Break it down by segment, then build a Hex app so the team can explore the drivers.”
* **Give your prototype real data:** “Rebuild this customer-health dashboard in Hex using our actual usage and revenue data.”

tip

During the beta period, you will need to explicitly prompt your external agent to use “4.0 project tools” in order to have the agent create a 4.0 project.

Here are some tips for using the MCP with some popular external agents:

#### Claude[​](#claude "Direct link to Claude")

The plugin may need to be refreshed in order for it to be able to pull in the new MCP tools:

1. In the sidebar, click `Customize`
2. Go to the `Connectors` tab
3. Find and click the Hex connector
4. Use the triple dot dropdown menu in the top right to click `Refresh tools list`

#### Codex[​](#codex "Direct link to Codex")

Because Codex bundles their plugins as static snapshots of MCP tools, the best way to use the MCP with Codex is not through the plugin (or you may be using outdated tools). Instead you should instruct the agent to do the following:

`Install the Hex MCP server at this URL: https://app.hex.tech/mcp`

## Limitations[​](#limitations "Direct link to Limitations")

While 4.0 is in beta, some features from classic projects aren't available yet (although we're working on supporting them as quickly as we can!). To see what's in progress, on deck, and shipped, check out the [beta roadmap](https://learn.hex.tech/docs/hex-4-0/beta-roadmap).

info

4.0 projects do not yet support [**App only**](/docs/collaborate/sharing-and-permissions/project-sharing#can-view-app) access. Only share projects with viewers who are permitted to access the underlying code and data, including intermediate results not shown in the app.

#### On this page

* [Projects in Hex 4.0](#projects-in-hex-40)
  + [Create a 4.0 project](#create-a-40-project)
* [Work in 4.0 projects](#work-in-40-projects)
  + [Work with the Hex agent](#work-with-the-hex-agent)
    - [Query semantic models](#query-semantic-models)
  + [Inspect agent outputs](#inspect-agent-outputs)
  + [Edit manually](#edit-manually)
* [Work with external agents via the MCP](#work-with-external-agents-via-the-mcp)
  + [Claude](#claude)
  + [Codex](#codex)
* [Limitations](#limitations)