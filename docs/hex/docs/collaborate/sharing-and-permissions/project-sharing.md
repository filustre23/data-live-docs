On this page

# Project sharing

Share Hex projects and grant **Full Access**, **Can Edit**, **Can Explore** or **Can View App** permissions

info

* By default, users need **Can Edit** project permissions or higher to share projects.
* Users with **Full Access** project permissions can disallow **Can Edit** users from sharing.

Hex projects are easy to share with your colleagues, stakeholders, and clients so you can review code, collaborate on analyses, and discuss findings. Sharing a project gives the invited user access to the project with the permissions you specify.

## Share a project[​](#share-a-project "Direct link to Share a project")

To share a project, click **Share** in the upper right of your project. Projects can be shared with specific users and groups, all workspace members, or publicly with the web. For each option, you can specify the permissions granted.

### Share with individual users or groups[​](#share-with-individual-users-or-groups "Direct link to Share with individual users or groups")

Inviting a specific user or [group](/docs/administration/workspace_settings/overview#groups) to a project simply grants that user or users access to the project with the permissions you specify.

If a user is removed from a group that was previously invited to a project, that user will lose access to the project.

### Share with workspace[​](#share-with-workspace "Direct link to Share with workspace")

Select **Share with [my workspace]** from the bottom left hand dropdown to make the project accessible to any Admin, Editor, or Viewer in your workspace. Workspace members will be able to view the project in the **Shared with workspace** section.

Workspace Guests cannot access projects shared with the workspace, unless they were separately invited to the project as an individual user.

### Share to web[​](#share-to-web "Direct link to Share to web")

Select **Anyone with the link** to make your project publicly available. Anyone with the link to your project will be able to navigate to and interact with your project.

Sharing your project publicly offers limited project permissions:

* **Can View App**: Can only see the published App
* **Can Explore**: Can see the entire project, and explore the published App. Cannot edit or run the project.

Note: a Workspace admin may have [disabled **Share to web** functionality](/docs/administration/workspace_settings/workspace-security#share-projects-to-web) for your workspace.

## Project permissions[​](#project-permissions "Direct link to Project permissions")

When you share a project, you grant one of several project permissions, which dictates what the invited user(s) can do on the project.

tip

When **Full Access** or **Can Edit** project permissions are granted to a Hex user who with a Viewer role, that user's permissions to the project will be automatically downgraded **Can View App**. Similarly, if this project permission is granted to a user with an **Explorer** role, they will be downgraded to **Can Explore**.

Learn more about how project permissions and workspace roles interact [here](/docs/collaborate/sharing-and-permissions/sharing-permissions#what-if-you-have-conflicting-permissions).

### Full Access[​](#full-access "Direct link to Full Access")

Grants full permissions on a project, including renaming and deleting the project, as well as sharing and managing project permissions. **Full Access** users can also disallow **Can Edit** users from sharing a specific project.

Users need an Editor, Manager or Admin [role](/docs/collaborate/sharing-and-permissions/roles) to be granted **Full Access** project permissions.

### Can Edit[​](#can-edit "Direct link to Can Edit")

Grants permission to comment on and modify any part of project, including the Notebook view, App builder and published App. Also grants permission to share and manage user project permissions (as long as this hasn’t been disabled by a **Full Access** user). Users with **Can Edit** permission cannot archive or delete the project.

Users need an Editor, Manager or Admin [role](/docs/collaborate/sharing-and-permissions/roles) to be granted **Can Edit** project permissions.

### Can Explore[​](#can-explore "Direct link to Can Explore")

Grants permission to view and comment on any part of the project, including the Notebook view, App builder, and published App, use [Chat with App](/docs/explore-data/chat-with-app) as well as [explore](/docs/share-insights/explore) from Apps. Users with **Can Explore** permissions cannot modify or share the project.

Users need an Explorer, Editor, Manager or Admin role to be granted **Can Explore** project permissions.

tip

Users with **Can Explore** permission who are workspace Editors or Admins *can* duplicate the project (excluding data connection credentials), and will have **Full Access** permissions on the resulting new project.

### Can View App[​](#can-view-app "Direct link to Can View App")

Grants permissions to view and comment on only the published App. Users with **Can View App** permissions cannot access the Notebook view or App builder. **Can View App** permissions also restrict the ability to duplicate, modify, or share the project.

### Workspace roles and project permissions[​](#workspace-roles-and-project-permissions "Direct link to Workspace roles and project permissions")

As mentioned above, each project permission is restricted to particular workspace roles. These are summarized below:

| Capability | Admin | Manager | Editor | Explorer | Viewer | Guest |
| --- | --- | --- | --- | --- | --- | --- |
| Allowed **Full Access** | ✔ | ✔ | ✔ |  |  | ✔ |
| Allowed **Can Edit** | ✔ | ✔ | ✔ |  |  | ✔ |
| Allowed **Can Explore** | ✔¹ | ✔ | ✔ | ✔ |  |  |
| Allowed **Can View App** | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ |

*¹Admins always have **Can Explore** access to a project, even if not explicitly granted it.*

## FAQs & Troubleshooting[​](#faqs--troubleshooting "Direct link to FAQs & Troubleshooting")

### What if a user is granted permissions via multiple shares?[​](#what-if-a-user-is-granted-permissions-via-multiple-shares "Direct link to What if a user is granted permissions via multiple shares?")

It’s possible for a single user to receive different permissions for a project if the user belongs to a group, workspace, or collection. In general, permissions are additive, so in these cases, the highest project permission is granted to the user.

For example, say you share a project with an individual and grant **Full Access** permissions. Later, you share the same project with a collection that the individual is a member of, granting **Can Explore** permissions. The individual will retain their **Full Access** permissions.

### Unable to edit due to missing workspace role[​](#unable-to-edit-due-to-missing-workspace-role "Direct link to Unable to edit due to missing workspace role")

If you were granted **Can Edit** access to a project (including via a group share), but do not have the Editor workspace role, you'll be downgraded to **Can Explore** or **Can View App** permissions (depending on whether you have an Explorer or Viewer seat, respectively). To resolve this issue, request an Editor seat in your workspace.

### Unable to explore due to missing workspace role[​](#unable-to-explore-due-to-missing-workspace-role "Direct link to Unable to explore due to missing workspace role")

Similarly, if you were granted **Can Explore** access to a project (including via a group share), but do not have the Explorer workspace role, you'll be downgraded to **Can View App** permissions. To resolve this issue, request an Explorer seat in your workspace.

### Unable to edit due to missing workspace asset permissions[​](#unable-to-edit-due-to-missing-workspace-asset-permissions "Direct link to Unable to edit due to missing workspace asset permissions")

Workspace assets (which include: [data connections](/docs/connect-to-data/data-connections/data-connections-introduction), [secrets](/docs/administration/workspace_settings/workspace-assets#shared-secrets), [Git export repos](/docs/explore-data/projects/git-export) and [Git packages](/docs/administration/workspace_settings/workspace-assets#git-package-import)) have additional permissions on who is allowed to edit a project when this asset is used in the project.

In some cases, you may have been granted **Can Edit** access to a project, but downgraded to **Can Explore** since you do not have access to all workspace assets used in the project. **This is the feature working as intended**, since it is designed as a security feature that prevents access.

If you require edit access to this project, you can do one of the following:

* **Ask a user with Can Edit access to remove the workspace asset that is preventing you from editing the project.**

  1. Use the warning message to determine which type of workspace asset is preventing you from having Can Edit access.
  2. Check who has Can Edit or Full Access to the project via the Share button in the top right hand corner.
  3. Reach out to one of those users and let them which type of workspace asset is preventing you from editing the project. Ask them to check whether the data connection, workspace secret or Git package is necessary for the project. In some cases, it might be able to be swapped with another asset or removed from the project entirely.
* **Ask a Workspace Admin to grant you access to the workspace asset.** If access is needed to do your job, it may make sense for you to be granted access to the workspace asset.

  1. Use the warning message to determine which type of workspace asset is preventing you from having Can Edit access.
  2. Find the list of Admins on the **Users** page of **Settings**.
  3. Contact an Admin to ask to be added to the workspace asset — include the project you're trying to edit as additional context.

### Unable to view a project due to missing data connection permissions[​](#unable-to-view-a-project-due-to-missing-data-connection-permissions "Direct link to Unable to view a project due to missing data connection permissions")

Workspaces on the Enterprise plan have [an additional data connection permission](/docs/connect-to-data/data-connections/data-connections-introduction#can-view-results) feature that can prevent users from viewing a project when certain data connections are used.

If you do not have access to a project because it uses a data connection you don't have **Can view results** access to, you'll see the following screen. **This is the feature working as intended**.

If you require access to this project, follow the same debugging steps as above.

### Unable to explore from a published app due to missing data connection permissions[​](#unable-to-explore-from-a-published-app-due-to-missing-data-connection-permissions "Direct link to Unable to explore from a published app due to missing data connection permissions")

The [**Can explore**](#can-explore) permission allows users to both view the project's notebook and [explore](/docs/share-insights/explore) from the published app. As mentioned [above](#unable-to-edit-due-to-missing-workspace-asset-permissions), users can see notebooks that use a given data connection without requiring [**Can query** access](/docs/connect-to-data/data-connections/data-connections-introduction#can-query) to that data connection. However, a user's ability to explore from a published app is dependent on the user having **Can query** access to the data connections used in the project.
This means that if a user is granted **Can explore** access to a project that uses a data connection they do not have **Can query** access to, they will be able to view the project's notebook, but not explore from the published app. Users will see a tooltip that explains this lack of connection permissions if they attempt to explore from the app.

### Debugging access to a project[​](#debugging-access-to-a-project "Direct link to Debugging access to a project")

*For Editors or Admins*

If a user has reached out as they are unable to access a project they've been granted access to, here are some debugging tips:

* **Ask them to share a screenshot**: The screenshot often includes useful information (see above for examples).
* **Inspect the share dialog**: If the project was shared directly with the user, the share dialog will show warnings if a permission conflict has occurred. If the project was not shared directly with that user, they may be inheriting access via a Group or Collection.

* **Check imported assets**: Hex prevents access to a project based on whether a workspace asset is **imported** into a project. In some cases, a workspace asset may be imported but not used in the project, which will still restrict access. Remove the data connection from the project via the three-dot menu next to the data connection's name.
* **Republish the project**: If you choose to switch any data connections that are preventing access, you may need to republish the project for these changes to take effect.

#### On this page

* [Share a project](#share-a-project)
  + [Share with individual users or groups](#share-with-individual-users-or-groups)
  + [Share with workspace](#share-with-workspace)
  + [Share to web](#share-to-web)
* [Project permissions](#project-permissions)
  + [Full Access](#full-access)
  + [Can Edit](#can-edit)
  + [Can Explore](#can-explore)
  + [Can View App](#can-view-app)
  + [Workspace roles and project permissions](#workspace-roles-and-project-permissions)
* [FAQs & Troubleshooting](#faqs--troubleshooting)
  + [What if a user is granted permissions via multiple shares?](#what-if-a-user-is-granted-permissions-via-multiple-shares)
  + [Unable to edit due to missing workspace role](#unable-to-edit-due-to-missing-workspace-role)
  + [Unable to explore due to missing workspace role](#unable-to-explore-due-to-missing-workspace-role)
  + [Unable to edit due to missing workspace asset permissions](#unable-to-edit-due-to-missing-workspace-asset-permissions)
  + [Unable to view a project due to missing data connection permissions](#unable-to-view-a-project-due-to-missing-data-connection-permissions)
  + [Unable to explore from a published app due to missing data connection permissions](#unable-to-explore-from-a-published-app-due-to-missing-data-connection-permissions)
  + [Debugging access to a project](#debugging-access-to-a-project)