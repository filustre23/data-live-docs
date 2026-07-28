On this page

# Guides

Provide unstructured context that helps agents interpret questions and respond appropriately.

info

* Available on the Team and Enterprise [plans](https://hex.tech/pricing/).
* **Admins**, **Managers**, **Editors**, and **Explorers** can view the guides tab.
* Only **Admins** and **Managers** can create, edit, and publish guides.

The guides tab is where you can add context about your data and business to help agents interpret questions and respond appropriately across your workspace.

You can provide context in two ways:

* **Workspace context** - always included in every conversation
* **Guide library** - retrieved dynamically when relevant

Use workspace context for broad rules and behavior. Use guides for detailed, task-specific information.

## Workspace context[​](#workspace-context "Direct link to Workspace context")

info

**Recently migrated:** The workspace context file is now part of the same versioning and editing system as your guide library. Existing content has been preserved as a Hex-managed file with the reserved path `hex.md`.

To manage this file outside of Hex, you can delete the Hex-managed guide in the Workbench, and follow the directions below to sync it with your guide library.

Workspace context is a single text file that the Hex Agent reads in every conversation.

Use it to define:

* High-level business context
* Interaction style and tone
* Response expectations that should apply broadly

Keep workspace context concise and focused on information that is relevant to most questions your users will ask. See [Best practices for workspace context](/tutorials/ai-best-practices/workspace-context-best-practices).

### How to configure workspace context[​](#how-to-configure-workspace-context "Direct link to How to configure workspace context")

Only Admins and Managers can configure workspace context.

The workspace context file uses the reserved path `hex.md` and is edited directly in the Context Workbench alongside your other guides. To configure workspace context:

1. Navigate to **Context Studio**
2. Find the **Guides** tab
3. Locate the file with path `hex.md`
4. Edit the file in the Workbench
5. Click **Test and Publish** to preview your changes and publish them live

tip

You can also sync the workspace context file externally using the same CI workflow as the guide library. Ensure that the final path of the file is `hex.md`. If the file lives in a subdirectory in your external source, transform the path with a custom mapping in your [Hex context configuration file](/docs/agent-management/context-management/context-sync#create-a-hex_contextconfigjson-file).

In the Workbench, the context file is denoted with a special icon and description to indicate its special nature. The context file also does not need frontmatter since the agent will always read it.

## Workspace guide library[​](#workspace-guide-library "Direct link to Workspace guide library")

The workspace guide library is a collection of text files that the Hex Agent dynamically retrieves when they are relevant to the conversation or task. These files can expose detailed business context that the agent can use to perform specific analyses.

### When to use the guide library[​](#when-to-use-the-guide-library "Direct link to When to use the guide library")

Use the workspace guide library for:

* Detailed documentation about specific business processes
* Domain-specific terminology and definitions
* Step-by-step procedures for common analyses
* Context that's only relevant to certain types of questions

Unlike workspace context (which is always included), guide library files are selectively retrieved based on relevance, allowing you to provide more detailed context without overwhelming every conversation.

### Writing guides[​](#writing-guides "Direct link to Writing guides")

To make the most of guides, we recommend adding frontmatter to your guide files, which is used by the Hex Agent to determine when a guide is relevant to the conversation or task. Frontmatter is defined at the start of a guide file by `---` delimiters, and can include a name and description.

```
---



name: Customers



description: Understanding Hex's types of customers



---



...
```

### Project mentions in guides[​](#project-mentions-in-guides "Direct link to Project mentions in guides")

You can @-mention projects in guides. When a guide is retrieved, the agent can use mentioned projects as context. This is useful when describing a workflow or analysis that depends on a specific project.

## Context Workbench[​](#context-workbench "Direct link to Context Workbench")

The Context Workbench provides tools to manage your library of workspace guides. Admins and Managers can edit existing files and add new ones. The workbench supports multi-player workflows, allowing multiple team members to collaborate on context improvements at the same time.

Once you've made your edits, click **Test and Publish**. In the Changes view, you can double-check a diff of every edit that has been made. Use the Threads tab to test specific questions and validate how your changes will affect agent responses before publishing them live. This allows you to iterate and immediately verify that agent behavior improves with each edit. Once you're satisfied with the preview, you can publish your changes to your workspace.

### History[​](#history "Direct link to History")

The History page records a complete version timeline of your guides.

You can:

* View and compare previously published versions.
* Copy and paste from any historical version back into your draft.

History provides version control directly in Hex, making it easy to experiment and iterate on guides. History is available for both guides created directly in Hex and those synced from external sources like GitHub.

## Programmatically upload guides to Hex[​](#programmatically-upload-guides-to-hex "Direct link to Programmatically upload guides to Hex")

Alternatively, you can manage your guides externally. Hex supports uploading guides via the Hex CLI or third-party CI like GitHub Actions. See [Context Sync](/docs/agent-management/context-management/context-sync) for more details. Guides uploaded from external sources will be read-only in Hex.

#### On this page

* [Workspace context](#workspace-context)
  + [How to configure workspace context](#how-to-configure-workspace-context)
* [Workspace guide library](#workspace-guide-library)
  + [When to use the guide library](#when-to-use-the-guide-library)
  + [Writing guides](#writing-guides)
  + [Project mentions in guides](#project-mentions-in-guides)
* [Context Workbench](#context-workbench)
  + [History](#history)
* [Programmatically upload guides to Hex](#programmatically-upload-guides-to-hex)