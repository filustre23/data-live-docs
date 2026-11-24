On this page

# Migrate from collections to folders

Folders are replacing collections as the primary organization mechanism. Learn more about how they differ, and how to migrate.

info

Workspace **Admins** migrate collections. Collections will be deprecated in **March 2027**.

We've introduced [folders](/docs/organize-content/folders), a more flexible and intuitive way to organize your workspace.

Folders will replace collections as the primary organization mechanism in Hex. Collections will be deprecated in March 2027 — if you're using collections, an admin in your workspace will need to convert them to folders before then.

There are a few key differences between folders and collections to be aware of:

* **Folders can be nested.** You can put folders inside other folders, up to ten levels deep.
* **Only Admins can create folders in the root of the workspace.** Other users can be given permission to create subfolders within those folders.
* **Folder access applies to everything inside.** When you give someone access to a folder, they get that access on every project, component, and subfolder in it.
* **Projects can only be in one folder.** Moving a project into a new folder removes it from its current one.

## Do you need to migrate?[​](#do-you-need-to-migrate "Direct link to Do you need to migrate?")

If your workspace has never used collections, you don't need to do anything — collections will no longer appear in your workspace.

If your workspace has collections, an **Admin** needs to migrate them. Folders handle permissions differently from collections, so Hex can't convert them automatically without changing who can access what.

You can also use the migration as an opportunity to simplify how work is organized, and how access is managed. You don't have to recreate every collection as a folder.

## How folder and collection permissions differ[​](#how-folder-and-collection-permissions-differ "Direct link to How folder and collection permissions differ")

**Collections:** A project is shared with a collection, and each project has its own access level for collection members. In one collection, members can have **Full access** to one project, **Can view** on another, and no additional access to a third.

Access ends up different on every project. A collection also can't give your data team **Can edit** and your marketing team **Can view** across those same projects.

**Folders:** Access is set once, on the folder. Every project in the folder gives the same access to the same people. You can also mix access at the folder level, giving your data team **Can edit** and your marketing team **Can view**.

Folders support three permission levels. Learn more in [Share a folder and manage permissions](/docs/organize-content/folders#share-a-folder-and-manage-permissions).

| Permission | On a folder | Items within the folder |
| --- | --- | --- |
| **Can view** | View the folder | Can view on **all** items in the folder |
| **Can edit** | View, rename, and add items to the folder | Can edit on **all** items in the folder |
| **Full access** | Everything in **Can edit**, plus manage access and delete the folder | Full access on **all** items in the folder |

Sharing a project directly with someone isn't affected. They keep that access after the project moves into a folder.

## Migration steps[​](#migration-steps "Direct link to Migration steps")

As part of your migration, you'll need to:

1. Convert the collections you want to keep into folders. Converting doesn't delete the collection. For details, see below.
2. Delete each collection after its projects have moved.
3. If you're on the Enterprise plan, update your organization settings so folders are shown to all users in your workspace. Go to **Settings → Organization**.
4. Turn off collections so no new collections can be created. Go to **Settings → Organization**.

info

Enterprise workspaces can choose when folders are available to everyone. Until then, only admins can see the folders page, which gives them time to organize the workspace first. Grants created in folders update project access right away, even before the rest of the workspace can see folders.

For these workspaces, folders will be shown to all users on **Dec 15**. You can also turn on folders for everyone earlier in **Settings → Organization**.

## Choose a migration approach[​](#choose-a-migration-approach "Direct link to Choose a migration approach")

| Approach | Best if |
| --- | --- |
| Use an agent | You have many collections, or you want help planning a custom structure |
| Convert each collection to a folder in Hex | Your collections already match how you want to organize your work |
| Set up new folders and move projects into them | Some collections are useful and others aren't, or you want a different structure |

You can combine approaches. For example, convert your well-organized collections, then set up folders for everything else.

### Use an agent[​](#use-an-agent "Direct link to Use an agent")

An agent skill can help with this migration. Use it when you have many collections, or you want help planning your folder structure. You can work with the agent to decide how detailed folder access should be, and to review the access changes before anything moves. The agent will leverage the [Hex CLI](/docs/api-integrations/cli#installation) to make changes.

To get started, send the following prompt to an agent that has command line access:

```
Install the Hex CLI (brew install hex-inc/hex-cli/hex), log me in with



`hex auth login`, then run `hex install agent-skill` and use the skill



to migrate my workspace's collections to folders.
```

### Convert a collection to a folder[​](#convert-a-collection-to-a-folder "Direct link to Convert a collection to a folder")

Use this when a collection already matches the folder you want. Converting creates the folder and moves projects into it. It does not delete the collection, so members keep their collection access until you disable collections.

1. Open the collection.
2. In the **Collections are becoming folders** banner, select **Convert this collection**. Only **Admins** can see this button.
3. Review **New permissions**. For each collection manager and member, Hex shows their **current access** (how many items they can access today, at each level), their **folder access**, and the **change**. You can change someone's folder access, or choose **Remove access** so they aren't added to the folder. Select someone's current access to see the change for each project. That view leaves out access from other sources, and items that are already in a folder.
4. Select **Convert**, then confirm **Convert to folder**.

Hex then:

* Creates a folder with the same name as the collection, at the root of the workspace. You can rename or move it later.
* Gives each person you included the folder access you chose. You become the folder's owner.
* Moves projects and components that aren't already in a folder into the new folder.
* Leaves the collection in place.

By default, Hex suggests the lowest folder access among the projects being moved. If anyone can only view a project, or has no access to one, the suggestion is **Can view**. People who could only view the App, or had no access, may be marked as an upgrade, because a folder can't grant **Can View App**. People who could edit or fully manage every project may be marked as a **possible downgrade**: the folder would give them less than the collection does. They may still have that access from another grant or group. Collection access itself stays until you disable collections.

**Projects that are already in a folder aren't moved.** They stay where they are, and the **Change** column doesn't count them.

### Set up folders and move projects[​](#set-up-folders-and-move-projects "Direct link to Set up folders and move projects")

Use this when you want a structure that's different from your collections, or when only some collections are worth keeping.

1. Go to **Folders** in the sidebar.
2. Create folders at the root of the workspace, and any subfolders you need.
3. Share each folder with the right people and groups, at the right access level.
4. Move projects into the folders from the **Projects** page, or from an existing collection. You can move several projects at once.
5. Delete collections once their projects have been moved.

While a collection still exists, its members keep their collection access to its projects, even after the projects move into a folder. That access goes away when you delete the collection, or when you disable collections in organization settings.

## Turn off collections[​](#turn-off-collections "Direct link to Turn off collections")

Collections will be deprecated in **March 2027**.

After you've migrated, you can turn off collections for your workspace early to avoid stakeholder confusion. In **Settings**, then **Organization**, turn on **Disable collections**. Collections disappear from the sidebar, collection pages stop opening, and access that came from collections stops working. Some people might lose access to projects they could open before. Turn the switch off to bring collections back.

1. Give your team notice that you're turning off collections on a target date.
2. Turn on **Disable collections**.
3. If people report that they've lost access, turn collections back on, fix the folder or project access, then turn collections off again.

If you haven't migrated your collections before March 2027, we'll reach out with additional reminders.

## Best practices for folders[​](#best-practices-for-folders "Direct link to Best practices for folders")

* **Share folders with [groups](/docs/administration/workspace_settings/overview#groups).** Groups are easier to keep up to date when people join, leave, or change teams. Manage group membership in Hex, or with [directory sync](/docs/administration/workspace_settings/directory-sync).
* **Set access on folders.** Folder access applies to everything inside, so it stays consistent as projects are added. Grant access on a project directly when one person needs an exception.
* **Keep the root of the workspace small.** Create a small number of folders there, for example one per team, then let each team organize its own subfolders.

#### On this page

* [Do you need to migrate?](#do-you-need-to-migrate)
* [How folder and collection permissions differ](#how-folder-and-collection-permissions-differ)
* [Migration steps](#migration-steps)
* [Choose a migration approach](#choose-a-migration-approach)
  + [Use an agent](#use-an-agent)
  + [Convert a collection to a folder](#convert-a-collection-to-a-folder)
  + [Set up folders and move projects](#set-up-folders-and-move-projects)
* [Turn off collections](#turn-off-collections)
* [Best practices for folders](#best-practices-for-folders)