On this page

# Workspace roles

Each user has a workspace role that dictates their workspace access and allowed permissions.

info

* Users will need the Admin workspace role to manage other users' roles.

A user’s role determines what activities they can do in the workspace, and what [permissions](/docs/collaborate/sharing-and-permissions/sharing-permissions#what-permissions-are-there) they are allowed to have on different resources. It also determines their billing status.

## Types of workspace roles[​](#types-of-workspace-roles "Direct link to Types of workspace roles")

Every user in a workspace is assigned one of the following roles: **Admin**, **Manager**, **Editor**, **Explorer**, **Viewer** or **Guest**.

* Admins — Own workspace configuration, access, and governance
* Managers — Endorse assets and contribute to workspace governance
* Editor — Build and edit notebooks and data apps in projects
* Explorer¹ — Build explorations and explore data apps, create Threads
* Viewer — Find and access data apps, view Threads that have been shared with them
* Guest — Ad-hoc access to Hex

**¹Only available on Team and Enterprise plans. [Talk to sales to learn more](https://hex.tech/request-explore-demo/).**

| Capability | Admin | Manager | Editor | Explorer | Viewer | Guest |
| --- | --- | --- | --- | --- | --- | --- |
| View all Projects, Components, and Collections | ✔ |  |  |  |  |  |
| Access workspace settings to manage users, groups, and billing | ✔ |  |  |  |  |  |
| Grant themselves Full Access to projects and components | ✔ |  |  |  |  |  |
| Update metadata (status, categories, title description) of projects they can view | ✔ | ✔ |  |  |  |  |
| Use [endorsed statuses](/docs/organize-content/statuses-categories) | ✔ | ✔ |  |  |  |  |
| Set up and edit [semantic projects](/docs/connect-to-data/semantic-models/intro-to-semantic-models) | ✔ | ✔ |  |  |  |  |
| Create or edit the [workspace context](/tutorials/ai-best-practices/workspace-context-best-practices) | ✔ | ✔ |  |  |  |  |
| Access Observability in [Context Studio](/docs/agent-management/context-studio) | ✔ | ✔ |  |  |  |  |
| See Context Management in [Context Studio](/docs/agent-management/context-studio) | ✔ | ✔ | ✔ | ✔ |  |  |
| See all user's individual [Threads](/docs/explore-data/threads) | ✔ |  |  |  |  |  |
| Create and duplicate projects, components, and collections | ✔ | ✔ | ✔ |  |  |  |
| Use the [Hex API](/docs/api-integrations/api/overview) | ✔ | ✔ | ✔ |  |  |  |
| Create and share [Threads](/docs/explore-data/threads) | ✔ | ✔ | ✔ | ✔ |  |  |
| View [Threads](/docs/explore-data/threads) shared with them | ✔ | ✔ | ✔ | ✔ | ✔ |  |
| Schedule project runs | ✔ | ✔ | ✔ | ✔² |  |  |
| Build, save, and share explorations | ✔ | ✔ | ✔ | ✔ |  |  |
| Subscribe to conditional notifications | ✔ | ✔ | ✔ | ✔ |  |  |
| Access projects shared with workspace | ✔ | ✔ | ✔ | ✔ |  |  |
| Access projects shared with them explicitly | ✔ | ✔ | ✔ | ✔ |  | ✔ |
| Access & use data apps shared with them explicitly | ✔ | ✔ | ✔ | ✔ | ✔³ | ✔ |
| Access & use data apps shared with the workspace | ✔ | ✔ | ✔ | ✔ | ✔³ |  |

²Users with the Explorer role and [Can Explore](/docs/collaborate/sharing-and-permissions/project-sharing#can-explore) project permissions can have one scheduled run per project.
³Users with the Viewer role can only be granted up to [Can View](/docs/collaborate/sharing-and-permissions/project-sharing) access

### Who can manage roles?[​](#who-can-manage-roles "Direct link to Who can manage roles?")

Only Admins can add new workspace members and edit users' workspace roles. Admins can configure workspace roles for [individual users](/docs/administration/workspace_settings/overview#add-and-manage-users), [allowed domains](/docs/administration/workspace_settings/overview#allowed-domains), and [directory sync](/docs/administration/workspace_settings/directory-sync).

## Workspace roles and paid seats[​](#workspace-roles-and-paid-seats "Direct link to Workspace roles and paid seats")

Users with the Admin, Manager, or Editor workspace roles are considered "Paid Author Seats". Users with the Explore workspace role are considered “Paid Explorer Seats”. Users with the Viewer workspace role are considered "Viewer Seats", which may be free or paid depending on your pricing plan.

### How is the Guest role different?[​](#how-is-the-guest-role-different "Direct link to How is the Guest role different?")

Guests are similar to Editors in that they can be granted up to **Full Access** [permissions](/docs/collaborate/sharing-and-permissions/sharing-permissions#what-permissions-are-there) on projects and components. However, Guests also differ from Admin, Manager, Editor, and Viewer workspace roles in a few key ways:

1. Guests do not receive access to resources or assets that are [shared with the workspace](/docs/collaborate/sharing-and-permissions/project-sharing#share-with-workspace). Guests can access *only* projects and components [shared with them as individuals](/docs/collaborate/sharing-and-permissions/project-sharing#share-with-individual-users-or-groups).
2. Guests cannot [view users or groups](/docs/administration/workspace_settings/overview#users--groups) in workspace settings.
3. Guests cannot create new projects or components in the workspace.

## What role is granted by a project invite?[​](#what-role-is-granted-by-a-project-invite "Direct link to What role is granted by a project invite?")

### Existing users[​](#existing-users "Direct link to Existing users")

When an existing user is invited to a project in your workspace, they will keep their existing workspace role. Recall that Viewers are restricted to **Can View** and below [project permissions](/docs/collaborate/sharing-and-permissions/project-sharing#project-permissions). So, if a Viewer is invited to a project with **Can Edit** or **Full Access** permissions, they will be downgraded to **Can View**, unless an Admin promotes them to Editor.

### New users[​](#new-users "Direct link to New users")

When a new user is invited to a project in your workspace, by default they will receive the Guest workspace role. However, a user invited to your workspace via project invite could receive the Viewer, Editor, Manager, or Admin role in either of the following cases:

* The user's email address matches an [allowed domain](/docs/administration/workspace_settings/overview#allowed-domains) for the workspace.
* The user's email address matches the workspace's [directory sync](/docs/administration/workspace_settings/directory-sync).

In these cases, the user will receive the workspace role specified by the allowed domain or directory sync configuration.

#### On this page

* [Types of workspace roles](#types-of-workspace-roles)
  + [Who can manage roles?](#who-can-manage-roles)
* [Workspace roles and paid seats](#workspace-roles-and-paid-seats)
  + [How is the Guest role different?](#how-is-the-guest-role-different)
* [What role is granted by a project invite?](#what-role-is-granted-by-a-project-invite)
  + [Existing users](#existing-users)
  + [New users](#new-users)