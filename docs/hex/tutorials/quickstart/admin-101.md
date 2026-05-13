On this page

# Admin 101

info

This tutorial is intended for users with an **Admin** role and includes features only available on the [Enterprise plan](https://hex.tech/pricing/).

This tutorial covers the basics of configuring your Hex workspace for success. We’ll review the Admin-controlled settings that cover user management, data access, workspace governance, and security controls. Check out our [**Admin Learning Path**](https://app.hex.tech/hex-public/app/d108422d-a9ec-4e8c-954d-fc6c2da00a34/latest) guide for a deeper dive into the configuration options available to you.

## 1. 🤓 User management and permissions 🤓[​](#1--user-management-and-permissions- "Direct link to 1. 🤓 User management and permissions 🤓")

One of the first things you’ll want to configure in a new workspace is how users on your team will access Hex. Review the settings outlined below to ensure users have the right level of access and avoid any unexpected charges.

* [**User roles**](/docs/collaborate/sharing-and-permissions/roles): Assign roles to dictate user abilities in Hex. Note that you’ll be charged for any paid seats prorated by day from the time of invitation.

  + [**Allowed domains**](/docs/administration/workspace_settings/overview#allowed-domains): Add an allowed email domain to let anyone at your org log into Hex without requiring additional invites. In most cases, it makes sense for these users to default to Viewers so role promotion requests to paid seats can be granted on a case-by-case basis.
* [**Permissions**](/docs/collaborate/sharing-and-permissions/sharing-permissions): Understand resource sharing to manage user access and permission levels.
* [**Groups**](/docs/administration/workspace_settings/overview#groups): Can be used to organize and grant sets of users the same permissions.
* [**Single Sign-On (SSO)**](/docs/administration/sso) ***(Enterprise only)***: Enable or enforce users to log in with your SSO provider. Note that enforcing SSO prevents any user that is not managed in you provider from accessing your Hex workspace.

  info

  If SSO is not enforced and your organization uses Google Workspace or Microsoft 365 for email, users log in to Hex using the one-click options on the sign-in page. When SSO is enforced, users will only see the SSO login button.
* [**Directory sync**](/docs/administration/workspace_settings/directory-sync) ***(Enterprise only)***: Integrate with your directory provider to inherit roles and groups without having to manage them directly in Hex. Note that any users in a group without a specified Hex user role will default to being Viewers in Hex.

tip

No directory provider? No problem. Manually configure [Groups](/docs/administration/workspace_settings/overview#groups) within Hex.

## 2. ☁️ Data management and access ☁️[​](#2-️data-management-and-access-️ "Direct link to 2. ☁️ Data management and access ☁️")

Hex is an incredibly powerful tool for making decisions, but not without your data! Check out the topics below on connecting to various data sources.

* [**Data connections**](/docs/connect-to-data/data-connections/data-connections-introduction): Create a connection to your data warehouse. For sensitive data, you may want to grant different groups of users [“Can query” and “Can view” access](/docs/connect-to-data/data-connections/data-connections-introduction#can-query). Additionally, consider setting your [schema to refresh](/docs/connect-to-data/data-connections/data-connections-introduction#schedule-schema-refreshes) on a daily or weekly cadence so the latest table metadata is shown in the Data browser.
  + [**Workspace SQL caching**](/docs/administration/workspace_settings/overview#workspace-sql-caching): Optimize your apps and save costs on warehouse compute by setting a sensible default caching timeout based on your ETL processes and Hex use cases. Bumping the default to 1 day is a common approach. Note that Editors can adjust this setting for individual projects.
* [**Semantic models**](/docs/connect-to-data/semantic-models/intro-to-semantic-models): Hex seamlessly [syncs](/docs/connect-to-data/semantic-models/semantic-model-sync/intro) semantic models from other providers, such as [Cube](https://cube.dev/docs/product/introduction), [Snowflake](https://docs.snowflake.com/en/user-guide/views-semantic/overview), and [dbt Metricflow](https://docs.getdbt.com/docs/build/about-metricflow?version=1.12). If you have one of those tools, start by syncing a few models. If you don’t, try building one in Hex's [Modeling Workbench](/docs/connect-to-data/semantic-models/semantic-authoring/semantic-authoring-overview#use-the-modeling-workbench)! Semantic models aren't required to use Hex, but we do recommend them as an additional a structured layer in your data model.
* [**Endorse**](/docs/agent-management/context-management/endorsements-in-context-studio) key data connections and tables to highlight trusted resources — useful for both human analysts and AI agents
* [**External file integrations**](/docs/administration/workspace_settings/workspace-assets#external-file-integrations): Have data that lives in Google Drive or S3? This integration is established using one main user, so consider creating a service account to connect with.

tip

All Editors and Explorers in your org have access to the **[Demo] Hex Public Data** connection to explore Hex functionality while you’re getting set up.

## 4. 🤖 Agentic capabilities 🤖[​](#4--agentic-capabilities- "Direct link to 4. 🤖 Agentic capabilities 🤖")

Hex’s AI [Agents](/docs/getting-started/ai-overview) can superpower your team across your projects, workspace, and even outside of Hex, all using natural language. Describe an analysis or ask a business question, and an Agent will work with you to explore your data.

* [**Notebook agent**](/docs/explore-data/notebook-view/notebook-agent): Helps project editors write code, create visualizations, debug errors, apply formatting, and more to iterate on complex data analysis in the Notebook
* [**Threads**](/docs/explore-data/threads): Conversationally answers business questions backed by data analysis, published projects, and context in your Hex workspace
  + Can be saved as a project for continued exploration + logic reviewing
  + Access the Threads agent outside of Hex via Slack, MCP server, and our CLI!
* [**Chat with App**](/docs/explore-data/chat-with-app): Interact with published Apps via natural language to view and summarize information, understand the project's underlying logic, and update inputs and filters
* [**Modeling agent**](/docs/connect-to-data/semantic-models/semantic-authoring/semantic-authoring-overview#modeling-agent): Assists admins and managers in creating and editing semantic projects

## 5. 🎯 Data governance and workspace management 🎯[​](#5--data-governance-and-workspace-management- "Direct link to 5. 🎯 Data governance and workspace management 🎯")

As your team grows and starts creating tons of great content, maintaining an organized workspace will become more important. Hex provides Admins a number of tools to keep projects organized at the user and team level. Without implementing these features, it can be difficult for human analysts and agents to find what they're looking for, which can limit collaboration and lead to duplicative work.

**Organize your workspace with…**

* [**Statuses and categories**](/docs/organize-content/statuses-categories): Label projects, components, and data objects to indicate asset status, such as in-development projects or trusted data tables. [Endorsed statuses](/docs/organize-content/statuses-categories#endorsed-statuses) highlight data assets to prioritize for agent use and signal trusted assets to human analysts as well.
* [**Collections**](/docs/organize-content/collections): Group projects and components to keep your workspace organized — projects can be added to multiple collections!

**Curate [workspace context](/docs/agent-management/context-management) for agents using…**

* Workspace [guides](/docs/agent-management/context-management/guides) to outline business context
* [Endorsements](/docs/agent-management/context-management/endorsements-in-context-studio) to highlight trusted data assets and projects. Endorsed assets are prioritized when agents answer questions and are helpful to signal reviewed and approved data to human analysts as well.
* Tip: [Managers](/docs/collaborate/sharing-and-permissions/roles#types-of-workspace-roles) can be added to assist Admins with curation work! Managers have all the same permissions as an Editor, with the extra capabilities of applying [Endorsed statuses](/docs/organize-content/statuses-categories#endorsed-statuses) to projects and data objects and updating project metadata.

[**Context Studio**](https://learn.hex.tech/docs/agent-management/context-studio): Observe, evaluate, and improve how Hex agents behave across your workspace using…

* The Agent observability [dashboard](/docs/agent-management/context-studio#dashboard-observe-agent-behavior) for high-level agent usage
* [**Thread inspector**](/docs/agent-management/observability#thread-inspector) to review specific agent conversations

For more details, check out the [**Organizing Your Workspace**](https://app.hex.tech/hex-public/app/d9252a16-8089-4872-b0fd-eeafcd40907f/latest) project for additional resources and best practices.

### 💪🏼 Level up your workspace 💪🏼[​](#-level-up-your-workspace- "Direct link to 💪🏼 Level up your workspace 💪🏼")

Covered the basics of Admin 101? Looking to configure integrations, manage users at scale, organize your workspace, and govern content well? Check out the guide [**Admin Learning Paths**](https://app.hex.tech/hex-public/app/d108422d-a9ec-4e8c-954d-fc6c2da00a34/latest) for a deeper dive into optimizing your Hex workspace.

#### On this page

* [1. 🤓 User management and permissions 🤓](#1--user-management-and-permissions-)
* [2. ☁️ Data management and access ☁️](#2-️data-management-and-access-️)
* [4. 🤖 Agentic capabilities 🤖](#4--agentic-capabilities-)
* [5. 🎯 Data governance and workspace management 🎯](#5--data-governance-and-workspace-management-)
  + [💪🏼 Level up your workspace 💪🏼](#-level-up-your-workspace-)