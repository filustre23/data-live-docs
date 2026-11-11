On this page

# Collections

Curate your workspace with a flexible, powerful organization and sharing framework.

info

* Available on the **Team** and **Enterprise** [plans](https://hex.tech/pricing/).
* The **Professional** plan is limited to 3 shared collections.

Collections are groups of projects and components that are created and populated by users in a workspace. Collections can be shared with individual users and groups, or with the entire workspace.

Collections contain references to projects, rather than holding the projects themselves. This allows for projects to be in multiple collections, increasing organizational flexibility and decreasing the potential for silos.

## View collections[​](#view-collections "Direct link to View collections")

Users can view the collections they have access to by clicking on the **Collections** page from the homepage. There are tabs to sort by **All collections**, **Created by you**, **Shared with you**, and **Shared with workspace**. Editors, Viewers, and Guests will only ever be able to see collections they are [members of](#collection-membership). Admins will be able to see and manage all collections in the workspace.

After clicking on a collection, users will be able to see the contents of the collection that they have access to.

## Create collections[​](#create-collections "Direct link to Create collections")

Editors and Admins can create collections by clicking on the **+ New collection** button in the upper right of the collections page.

When you create a collection, you automatically become a manager of the collection. Read about how to add other managers & members to a collection in the [membership](#collection-membership) section below.

## Collection membership[​](#collection-membership "Direct link to Collection membership")

Users can either be members or managers of a collection.

* Members can access the contents of a collection.
* Managers of a collection can add and remove its contents, manage its permissions, set metadata, and delete the collection.

Collection managers can manage membership of a collection by clicking **Edit collection** via the **Edit** dropdown, or via the share modal on the right of the collection.

## Add & remove content from a collection[​](#add--remove-content-from-a-collection "Direct link to Add & remove content from a collection")

Users are able to add projects and components to a given collection if they are both a manager of the collection and have access to the underlying project. There are many ways to add a project or component to a collection:

* From the collection, click the green **Add to collection** button in the upper right, then **Existing Project**. From here you can search existing projects and components.
* From a project list (via either Home, Components, All projects, Created by you, Shared with you, or Shared with workspace), click the 3-dot menu and choose **Add to collection**.
* From the share dialog of a project or component, search for a name in order to add it to a collection.

Removing content from a collection is only possible by collection managers who have access to the content. You can remove content from a collection in two ways:

* From within the collection, click the 3-dot menu > **Remove from collection**.
* From within the share dialog of the project or component, click on the collection access > **Remove collection**.

Note that removing a project may revoke access for users who have been granted access to the project via the collection (more on this in the section on [permissions](#permissions) below).

## Permissions[​](#permissions "Direct link to Permissions")

Each project or component in a collection will have an access level associated with it. The access level selected dictates the minimum level of access that all collection members will have to that piece of content.

If the project or component being added to a collection has existing share permissions enabled, the selected collection-level access will be additive to those existing permissions, and will not replace them. If **No additional access** is selected, members of the collection will be granted no additional access to the content, and the existing project or component permissions will be maintained. In order to select a level of access higher than **No additional access**, a manager will need to have share permissions to the underlying content.

Members will only ever see content they have access to in a given collection.

Collection managers can set collection-level access when adding content to a collection, or via the list of collection content. Collection members will not see the collection-level access that's been granted per project/component; they'll instead see the exact access level they have to each piece of content.

There are some nuances to keep in mind when it comes to collection permissions:

* Project and component permissions cannot be absolutely managed at the collection level; that is, users that are not members of a given collection can have access to a project or component that has been added to that collection.
* If a particular user or group needs more advanced access to a piece of content than has been granted to them at the collection level, it is possible to “bump up” their access by changing the permissions at the project/component level (note: you cannot “downgrade” permissions for a user or group in this same way)
* Following from the point above, because individual access can be “bumped up” at the project/component level, different collection members can have different levels of access to a given project/component in a collection. Think of the collection-wide permission that has been set for a project as the **minimum level of access all collection members will have access to**, layering on top of project/component-level access.
* If you ever want to see exactly who has access to a particular piece of content, you can check the share modal of the project or component to see exactly which members of the workspace have access, as well as where that access has been granted (at the collection level or at the project/component level).

## Delete collections[​](#delete-collections "Direct link to Delete collections")

Deleting a collection is only possible by managers of the collection. From the collection’s edit dropdown, select **Delete collection**. Note that this may revoke project/component access that has been granted to users via the collection.

#### On this page

* [View collections](#view-collections)
* [Create collections](#create-collections)
* [Collection membership](#collection-membership)
* [Add & remove content from a collection](#add--remove-content-from-a-collection)
* [Permissions](#permissions)
* [Delete collections](#delete-collections)