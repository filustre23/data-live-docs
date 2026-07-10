On this page

# Sharing & permissions introduction

Hex makes it easy to share your work and manage access.

## What can you share in Hex?[​](#what-can-you-share-in-hex "Direct link to What can you share in Hex?")

You can share different resources or workspace assets in Hex depending on your workspace [role](/docs/collaborate/sharing-and-permissions/roles).

* Admins and Editors (as well as Guests with the necessary permissions) can share projects, components, and collections.
* Admins, Editors, and Explorers can share Threads.
* Admins can also share workspace assets (data connections and secrets).
* Viewers can copy and distribute existing links to projects, Apps, and components, but cannot grant additional access.

## Sharing inside of Hex[​](#sharing-inside-of-hex "Direct link to Sharing inside of Hex")

1. Share a specific resource or asset ([learn more](/docs/collaborate/sharing-and-permissions/sharing-permissions#share-a-specific-resource-or-asset))
2. Add users to a workspace or group ([learn more](/docs/collaborate/sharing-and-permissions/sharing-permissions#add-users-to-a-workspace-or-group))
3. Add users to a collection ([learn more](/docs/collaborate/sharing-and-permissions/sharing-permissions#add-users-to-a-collection))

### Share a specific resource or asset[​](#share-a-specific-resource-or-asset "Direct link to Share a specific resource or asset")

The simplest way to share your work with collaborators is to invite them directly. You’ll need their email address if they’re not already a member of the workspace.

* Share a specific [project](/docs/collaborate/sharing-and-permissions/project-sharing) or [component](/docs/explore-data/components#component-permissions) with an individual user, group, the entire workspace, or the web.
* Share a specific [Thread](/docs/explore-data/threads#sharing) with an individual user, group, or the entire workspace.
* Share a [data connection or secret](/docs/administration/workspace_settings/workspace-assets) with a group or the entire workspace.
* Share a Git repo for [package import](/docs/administration/workspace_settings/workspace-assets#git-package-import) or [project export](/docs/explore-data/projects/git-export#configuring-a-git-provider) with a group or the entire workspace.

### Add users to a workspace or group[​](#add-users-to-a-workspace-or-group "Direct link to Add users to a workspace or group")

**Admins** can add new users as workspace members, and add workspace members to a user group, which grants access to any projects, components, or collections shared with the workspace or group. This can be done manually from **Settings > Users** and **Settings > Groups**, or be configured with [directory sync](/docs/administration/workspace_settings/directory-sync).

* Add users to your [workspace](/docs/administration/workspace_settings/overview#users--groups) to give them access to everything shared with the workspace.
* Add users to a [user group](/docs/administration/workspace_settings/overview#groups) to give them access to everything shared with that group.

### Add users to a collection[​](#add-users-to-a-collection "Direct link to Add users to a collection")

A [collection](/docs/organize-content/collections) is a way to organize and share related resources with a set of users. You can add a user as a member of a collection to grant them access to all of that collection’s projects or components.

* [Add users to a collection](/docs/organize-content/collections#collection-membership) to give them access to everything shared with the collection.

## Sharing outside of Hex[​](#sharing-outside-of-hex "Direct link to Sharing outside of Hex")

1. Embed an App or cell outside of Hex ([learn more](/docs/collaborate/sharing-and-permissions/sharing-permissions#embed-an-app-or-cell-outside-of-hex))
2. Send project results via email or Slack ([learn more](/docs/collaborate/sharing-and-permissions/sharing-permissions#send-project-results-via-email-or-slack))
3. Start and share Threads outside of Hex ([learn more](/docs/collaborate/sharing-and-permissions/sharing-permissions#start-and-share-threads-outside-of-hex))

### Embed an App or cell externally[​](#embed-an-app-or-cell-externally "Direct link to Embed an App or cell externally")

To share your work outside of Hex, you can [embed](/docs/share-insights/embedding/embedding-introduction) an App or cell in a website, or paste a [Hex link into Notion](/docs/share-insights/embedding/public-and-private-embedding#embed-in-a-notion-page) and generate a preview.

### Send project results via email or Slack[​](#send-project-results-via-email-or-slack "Direct link to Send project results via email or Slack")

[App notifications](/docs/share-insights/app-notifications) can be configured to send upon scheduled run completion or when certain data conditions are met. Notifications can be delivered via in-app notifications, email, or Slack, and can contain content including:

* PNG/PDF screenshots of the entire App or specific cells
* Data exports (CSV, Google Sheets) of any data tables in the published app

### Start and share Threads via external integrations[​](#start-and-share-threads-via-external-integrations "Direct link to Start and share Threads via external integrations")

**Start Threads outside of Hex:**

* [MCP Server](/docs/api-integrations/mcp-server) - allows external AI applications to create and continue Threads conversations directly within your Hex workspace
* [CLI](/docs/api-integrations/cli) - manage and start Threads programmatically via the command line
* [API](/docs/api-integrations/api/overview) - manage and start Threads programmatically using REST API endpoints

**Share Threads outside of Hex:**

* [Hex Agent in Slack](/docs/api-integrations/slack#enable-hex-agent-in-slack) - ask questions, analyze data, and get AI-powered insights with the Hex Agent in public and private Slack channels. Chatting with the Hex Agent in Slack kicks off an underlying Thread that can be viewed and continued in the Hex UI.
* [Tasks](/docs/explore-data/tasks) - schedule the Hex Threads agent to run on a recurring cadence and deliver results via Slack or email.

## What permissions are there?[​](#what-permissions-are-there "Direct link to What permissions are there?")

There are different types of permissions available for different resources.

* Projects can be shared with **Full Access**, **Can Edit**, **Can Explore**, or **Can View App** permissions ([Learn more](/docs/collaborate/sharing-and-permissions/project-sharing#project-permissions)).
* Components can be shared with **Full Access**, **Can Edit**, or **Can Import** permissions ([Learn more](/docs/explore-data/components#component-permissions)).
* Threads can be shared with the **Can view thread** permission ([Learn more](/docs/explore-data/threads#sharing)).

## What if you have conflicting permissions?[​](#what-if-you-have-conflicting-permissions "Direct link to What if you have conflicting permissions?")

### Project permissions are additive[​](#project-permissions-are-additive "Direct link to Project permissions are additive")

tip

In general, **permissions are additive, not restrictive.**

It’s possible for one user to receive different permissions for a single project or component if the user belongs to a group, workspace, or collection. In these cases, the highest permission wins.

For example, say you share a project with an individual and grant **Full Access** permissions. Later, you share the same project with a collection that the individual is a member of, granting **Can Explore** permissions. The individual will retain their **Full Access** permissions.

### Workspace roles and assets can restrict project permissions[​](#workspace-roles-and-assets-can-restrict-project-permissions "Direct link to Workspace roles and assets can restrict project permissions")

tip

In contrast to permissions, workspace **roles and asset access are restrictive.**

* The **Viewer** workspace role restricts users to **Can Explore** or **Can View App** project permissions. If you invite a workspace **Viewer** to a project and attempt to assign **Can Edit** or **Full Access** permissions, you will see a notice that the user is restricted to **Can Explore** permissions based on their role ([Learn more](/docs/collaborate/sharing-and-permissions/roles)).
* Access to workspace assets, including data connections and secrets, also restricts project permissions. A user without access to one of the workspace data connections or secrets used in a project can receive only **Can Explore** or **Can View App** permissions on that project.

#### On this page

* [What can you share in Hex?](#what-can-you-share-in-hex)
* [Sharing inside of Hex](#sharing-inside-of-hex)
  + [Share a specific resource or asset](#share-a-specific-resource-or-asset)
  + [Add users to a workspace or group](#add-users-to-a-workspace-or-group)
  + [Add users to a collection](#add-users-to-a-collection)
* [Sharing outside of Hex](#sharing-outside-of-hex)
  + [Embed an App or cell externally](#embed-an-app-or-cell-externally)
  + [Send project results via email or Slack](#send-project-results-via-email-or-slack)
  + [Start and share Threads via external integrations](#start-and-share-threads-via-external-integrations)
* [What permissions are there?](#what-permissions-are-there)
* [What if you have conflicting permissions?](#what-if-you-have-conflicting-permissions)
  + [Project permissions are additive](#project-permissions-are-additive)
  + [Workspace roles and assets can restrict project permissions](#workspace-roles-and-assets-can-restrict-project-permissions)