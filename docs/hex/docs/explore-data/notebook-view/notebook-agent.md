On this page

# Notebook agent

Bring AI-powered assistance directly into your Hex projects.

info

* Notebook agent is available in **Beta** on all [plans](https://hex.tech/pricing/). Paid plans include monthly per-seat [credit grants](/docs/administration/credits) that can be used towards Hex AI features. While Hex agents are in Beta, credit limits and optional add-on credits are being rolled out in phases and are not yet enforced for all customers. Admins will receive advance notice before limits go into effect for their workspace.
* Users need the **Admin**, **Manager**, or **Editor** workspace role and **Can Edit** or higher project permissions to use the Notebook agent.
* The Notebook agent is not compatible with **Published apps**.
* To share suggestions for new features or improvements, reach out to [[email protected]](/cdn-cgi/l/email-protection#ccbfb9bcbca3beb88ca4a9b4e2b8a9afa4).

The Notebook agent offers a natural language experience to assist with code generation and exploratory analysis within Hex projects. The agent has full access to your project context and warehouse schema information, so you can ask questions about - and receive answers for - your data. The agent can also help with syntax, act as a sounding board for brainstorming solutions, or create entirely new lines of analysis.

## Sources for agentic analysis[​](#sources-for-agentic-analysis "Direct link to Sources for agentic analysis")

The Notebook agent can leverage any [Data connections](/docs/connect-to-data/data-connections/data-connections-introduction) or [Semantic models](/docs/connect-to-data/semantic-models/intro-to-semantic-models) that a user has access to in order to properly power analysis. Point the Notebook agent at any Data connection or Semantic model by [mentioning](/docs/explore-data/notebook-view/notebook-agent#mention-cells-and-tables) them in your project.

The agent will also reference any Workspace rules that have been defined in the [Workspace rules file](/docs/agent-management/context-management/guides#workspace-rules).

tip

Check out our [Modeling workbench](/docs/connect-to-data/semantic-models/semantic-authoring/semantic-authoring-overview) to get started on building a Semantic model in Hex, or sync your existing Semantic model into Hex using [Semantic sync](/docs/connect-to-data/semantic-models/semantic-model-sync/intro)!

## Using the Notebook agent[​](#using-the-notebook-agent "Direct link to Using the Notebook agent")

Access the Notebook agent in a Hex project from the **Ask a question** modal in the bottom-right corner of the Notebook.

[](/assets/medias/using-the-notebook-agent-11e84c63b3943f7e5ae74775f94b3fa3.mp4)

### Start a new thread[​](#start-a-new-thread "Direct link to Start a new thread")

Start a new thread from the **+** icon in the top right corner of the agent sidebar. Starting a new thread will allow you to clear the context of the chat to ask a new question.

Staring a new thread will save a version of your project, so you're able to access and restore previous project versions.

### Access chat history[​](#access-chat-history "Direct link to Access chat history")

Access your previous chat history from **History** at the top of the active chat window. Your chat history reflects your personal chat requests, and chat requests persist for 30 days.

[](/assets/medias/view-history-tab-b4134c145a9968bbdd99b63519d68ec9.mp4)

### Mention cells and tables[​](#mention-cells-and-tables "Direct link to Mention cells and tables")

Tag specific cells in the Notebook agent prompt to focus the agent's analysis on specific cells or tables for its primary context. Useful for very large notebooks or cases where you know exactly what you want the agent to do. Mentioning a specific cell in the project will allow you to focus the agent's analysis on that specific cell, and you can mention any Cell, Table, or Dataframe in project memory.

### Confirm or Undo pending changes[​](#confirm-or-undo-pending-changes "Direct link to Confirm or Undo pending changes")

All changes that the agent suggests must be accepted into the Notebook (**Confirm**) or rejected (**Undo**). Pending changes are managed on the individual cell level, and every cell that the agent touches will prompt a new change to confirm or undo.

The **Pending changes** modal will sequentially guide you through the changes that the agent has made, and allow you to handle each one separately. Selecting an individual cell in the **Pending changes** modal will take you to the affected cell, where you can view the cell's logic in the context of your project.

[](/assets/medias/keep-or-undo-1481dc5bf694453ee4218d57bd2496ea.mp4)

### Upload files[​](#upload-files "Direct link to Upload files")

info

File uploads requires the [allow file uploads setting](/docs/administration/workspace_settings/workspace-security#allow-file-uploads) to be turned on.

Upload files to bring external context into Hex quickly. Add a file or image, and the agent can reference it for analysis, summaries, and answers.

### Personal preferences[​](#personal-preferences "Direct link to Personal preferences")

Personal preferences let you specify how the Notebook Agent should respond when working with you. Specify preferred formatting, a specific response style, or other guidance and the agent will use it across all your interactions. These instructions only apply to you and aren’t visible to other users in your workspace. For more details see [Agent personalization](/docs/agent-management/agent-personalization).

[](/assets/medias/user-rules-01f4bd0c1bb62c5dfb559e450d3e8709.mp4)

## Notebook agent capabilities[​](#notebook-agent-capabilities "Direct link to Notebook agent capabilities")

### Generate new cells[​](#generate-new-cells "Direct link to Generate new cells")

The Notebook agent has the ability to create new cells in a project. The agent is capable of creating [Python cells](/docs/explore-data/cells/python-cells), [SQL cells](/docs/explore-data/cells/sql-cells/sql-cells-introduction), [Markdown cells](/docs/explore-data/cells/text-cells), [Pivot cells](/docs/explore-data/cells/transform-cells/pivot-cells), [Input parameters](/docs/explore-data/cells/input-cells/input-cells-introduction), [Single value cells](/docs/explore-data/cells/visualization-cells/single-value-cells), and [Chart cells](/docs/explore-data/cells/visualization-cells/chart-cells). The agent will create the necessary cells to properly accommodate your request.

### Subagents[​](#subagents "Direct link to Subagents")

For complex analytical requests, the Hex Agent uses subagents to break your question into focused workstreams that run in parallel — including finding the right data connections, tables, and schemas, as well as handling chart creation. This means faster, more reliable results on even the most demanding analyses.

We've also expanded the Subagents charting capabilities, so it can now create reference lines, dual y-axis charts, and handle multi-series visualization styling.

### Edit existing cells[​](#edit-existing-cells "Direct link to Edit existing cells")

The Notebook agent can also modify existing cells in your project. To modify a cell, point the Agent at a specific cell in your project via [@ Mention](/docs/explore-data/notebook-view/notebook-agent#mention-cells-and-tables) and state your request.

### Move cells[​](#move-cells "Direct link to Move cells")

The Notebook agent can help with notebook organization by moving cells to different locations in your Notebook. You can ask the agent to move cells before/after other cells, as part of sections, or to the top/bottom of the project. The Agent understands the chain of dependencies present in your project, so it knows where to insert/move cells in cooperation with the project's [Execution model](/docs/explore-data/projects/project-execution/execution-model).

### Delete cells[​](#delete-cells "Direct link to Delete cells")

The Notebook agent can delete cells from your notebook with full awareness of downstream impacts. Before deletion, the agent inspects cell lineage to understand which other cells depend on the cell being removed, including variable references, dataframe dependencies, and input parameter usage. The agent can delete individual cells or multiple cells at once.

Before the agent deletes cells in your project, you must select either **Accept** or **Deny** for the changes to take effect. Select **Don't ask again in this thread** for the agent to skip this step.

### Arrange and publish your app[​](#arrange-and-publish-your-app "Direct link to Arrange and publish your app")

The Notebook agent can create and edit the layout of your [published app](/docs/share-insights/apps/app-builder), as well as publish the app for you. The agent can arrange your cells into rows, columns, and tabs.

### Fix your code[​](#fix-your-code "Direct link to Fix your code")

The agent can fix your code with either **Fix with agent** or **Quick fix**.

**Fix with agent** is best suited for:

* Complex, multi-step fixes that span multiple cells
* Contextual debugging that factors in your data and analysis objectives
* Exploratory fixes, where the agent needs to test queries or validate its logic before delivering an answer
* Consultative troubleshooting that delivers in-depth explanations alongside its fixes

**Quick fix** is best suited for:

* Simple corrections: fixing things like syntax errors, typos, missing imports, incorrect function names, etc.
* Analysis that does not require context on your data or business logic
* Straightforward problems that are contained within a single cell and have a clear solution

### Chat the docs[​](#chat-the-docs "Direct link to Chat the docs")

The Notebook agent is connected to our documentation (i.e., the page you're reading right now), so you can ask the Notebook agent direct questions about Hex functionality and it can help you find relevant documentation or tutorials.

### Summarize cell contents[​](#summarize-cell-contents "Direct link to Summarize cell contents")

The agent can summarize a cell or project's contents, and can answer natural language questions about the project's logic. You can ask it any question about the project or underlying dataset.

tip

Select `Tab` on a currently-selected cell to add that cell to your prompt.

### Projects as context[​](#projects-as-context "Direct link to Projects as context")

The Notebook Agent always uses your current notebook as context. It can see the project's structure, code, and outputs so it can help you edit and extend the notebook. You can also bring in other Hex projects as context for the agent to use. Mention those projects or paste a project URL in your prompt.

For each project you add, the agent can see that project's structure: which cells exist, their types and labels, and how data flows between them. When it needs more detail, it can open specific cells to read source SQL and Python as well as outputs such as tables, charts, and text. That lets it reuse logic, definitions, or results from those projects when editing your notebook. It cites the projects and cells it used so you can see the choices it made.

Only projects you have [**Can Explore**](/docs/collaborate/sharing-and-permissions/project-sharing#can-explore) access or higher on can be added as context.

## Providing feedback[​](#providing-feedback "Direct link to Providing feedback")

Use the in product feedback buttons to report bugs or issues. Our team reviews these reports daily. If you want to share suggestions for new features or improvements, reach out to us directly at [[email protected]](/cdn-cgi/l/email-protection#93e0e6e3e3fce1e7d3fbf6ebbde7f6f0fb).

#### On this page

* [Sources for agentic analysis](#sources-for-agentic-analysis)
* [Using the Notebook agent](#using-the-notebook-agent)
  + [Start a new thread](#start-a-new-thread)
  + [Access chat history](#access-chat-history)
  + [Mention cells and tables](#mention-cells-and-tables)
  + [Confirm or Undo pending changes](#confirm-or-undo-pending-changes)
  + [Upload files](#upload-files)
  + [Personal preferences](#personal-preferences)
* [Notebook agent capabilities](#notebook-agent-capabilities)
  + [Generate new cells](#generate-new-cells)
  + [Subagents](#subagents)
  + [Edit existing cells](#edit-existing-cells)
  + [Move cells](#move-cells)
  + [Delete cells](#delete-cells)
  + [Arrange and publish your app](#arrange-and-publish-your-app)
  + [Fix your code](#fix-your-code)
  + [Chat the docs](#chat-the-docs)
  + [Summarize cell contents](#summarize-cell-contents)
  + [Projects as context](#projects-as-context)
* [Providing feedback](#providing-feedback)