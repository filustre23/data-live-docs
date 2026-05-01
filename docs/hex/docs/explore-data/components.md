On this page

# Components

Components are groups of cells that can be reused across Hex projects.

info

* Fully available on the Team and Enterprise [plans](https://hex.tech/pricing).
* The Professional plan can share up to three components with members of their workspace.
* Users will need the Editor or Admin role to create and manage components.

Components are reusable groups of cells that can be imported across projects, making it easy for your team to implement [DRY](https://en.wikipedia.org/wiki/Don%27t_repeat_yourself) practices in your Hex workflows. Changes to a component can be made once, and then propagate down into projects that rely on it. Create components from [within projects](#create-components-from-within-projects) or from the **Components** tab in your [home page](#create-components-from-the-home-page).

## Create components from within projects[​](#create-components-from-within-projects "Direct link to Create components from within projects")

There are a few different ways to create a component from within the logic of a project. Each of the following methods begin by selecting multiple cells:

1. From the graph view, select multiple cells with `command + click` or `shift` + dragging your mouse around the desired cells.

[](/assets/medias/selecting-cells-graph-b839f55b0a4091be03afe0c82f1698cf.mp4)

2. From the Notebook view, select multiple cells with `command + click` or by entering command mode (`esc`) and selecting additional cells (`shift + up/down arrow` or `shift + j/k` to select adjacent cells, or `command + click` to select any assortment of cells).

[](/assets/medias/selecting-cells-logic-4a47b0aa084688a694892f158d3974c9.mp4)

3. From the 3-dot menu of a given cell, click **Select cell and…** to select multiple cells (all upstream, all downstream, or all upstream + downstream).

Each of these methods will result in a pop-up with an option to create a **New component**.

It’s also possible to create a new component from a single cell by clicking the cell’s 3-dot menu and selecting **New component from cell**.

Clicking **New component** will open a modal where you can name your component, add a description, and update which cells are selected.

The option **Replace cells with component** will be enabled by default; this will replace the selected cells with the component upon creation. If this option is disabled, the selected cells will remain cells and the component will not be added to the project upon creation.

## Create components from the home page[​](#create-components-from-the-home-page "Direct link to Create components from the home page")

To create a component from the home page, click on the **Components** page in the left sidebar. This will bring you to the components explorer, where you can view existing components and create new ones. To create a component, click the **+ New component** button.

Writing the logic of a component is very similar to writing the logic of a project. All cell types available in projects can be used in components.

Once you've written out the logic for your component, you’ll need to publish it to make it accessible within projects. The publishing flow for components is akin to project publishing — click the green **Publish** button in the top left corner to start the process. The publish modal will display a diff view that shows the logic changes you've made since the last publish. Click **Publish version** to update the published version of the component.

## Import and use components[​](#import-and-use-components "Direct link to Import and use components")

Components can be added to a project just like any other cell type. Use the **Component** button from the **Add cell** menu.

This will bring up an import modal that lists all the published components you have access to. From here you can preview components and import them into your project.

tip

If you can't find a component in the import modal, double check that it's been published. Only published components appear here!

After a component has been imported into a project, its cells can be run just like any other cells. All dataframes, variables, and other outputs of a component can be referenced and used anywhere downstream of the imported component.

It's possible to view component logic from within the project, but any changes must be made within the component itself. If a user has [access](#component-permissions) to the component, they'll be able to navigate to its source via the arrow next to the component's name, or via the its three-dot menu.

## Component permissions[​](#component-permissions "Direct link to Component permissions")

Component permissions are handled similarly to project permissions. See the table below for details:

| Permission | Access |
| --- | --- |
| Full Access | Grants full permissions on a component, including renaming, deleting, and editing, as well as sharing and managing permissions. |
| Can Edit | Grants permission to edit, comment on, and import the component. Also grants ability to manage permissions (unless this has been disabled by a "Full Access" user). |
| Can Import | Grants permission to view, comment on, and import the component. Cannot edit or manage permissions. |

These permissions can be managed from the **Share** button in a Component's logic.

If a user does not have access to a component, but *does* have Can Explore, Can Edit, or Full Access [permissions on a project](/docs/collaborate/sharing-and-permissions/sharing-permissions) that imports that component, the user will be able to view the component's logic *within the project that imports it*. The user will not inherit any permissions to the component, and will not have the option to navigate back to the component source.

## Update components[​](#update-components "Direct link to Update components")

When making updates to a component, the component must be published for these changes to take effect. As part of the publishing, you can optionally send a notification to all project owners that use the component to notify them that a new version is available.

tip

Publishing a new version of a component will **not** automatically update the component in downstream projects.

### Updating component references in bulk[​](#updating-component-references-in-bulk "Direct link to Updating component references in bulk")

Users with the **Admin** role can update references to a component in bulk. Note that this will only update the version on the draft of a project — the project will need to be republished for the changes to take effect in the app.

To update components in bulk, click the number of references in the component header. Then, select the projects to update by hovering over the row, and select **Force update drafts**.

### Updating a single component reference[​](#updating-a-single-component-reference "Direct link to Updating a single component reference")

When a new version of a component is published an **Update available** badge will appear next to the component in each project it's been imported into.

Clicking **Update available** will bring you to a modal with a diff view, which allows you to compare the component's latest changes with the version that you currently have imported. From here, selecting **Update component** will replace the existing component in your project with the latest published version.

## Eject components[​](#eject-components "Direct link to Eject components")

It is possible to eject a component's cells into a project. This will untether the cells from the component, causing the cells to simply be considered part of the project you're ejecting into.

You can eject a component that's already been added to a project via its three-dot menu. If you'd like to import a component as cells straight away, you can do so from the **Import component** dropdown menu in the import modal.

Since ejected cells are no longer attached to the component, you will no longer have the option to update the cells if the component changes. Ejecting cells into a project allows them to be editable from the project.

## View a component's references[​](#view-a-components-references "Direct link to View a component's references")

A component will show the number of references in the header.

Click the number of references to bring up a list of the projects the component is currently being used in, including important information like the version of the component currently being used in both the draft and published app,.

Note that archived and deleted projects are omitted from this list.

Users with the **Admin** role also have the option to force update references to this component to the latest version, see [above](#updating-component-references-in-bulk).

## Delete components[​](#delete-components "Direct link to Delete components")

Users who have Full Access permissions to a component have the option to delete it. This is possible via the "Move to Trash" button found in the dropdown of a component's title. Components will remain in the trash for 7 days, at which point they will be permanently deleted.

When a component has been moved to trash, a warning will appear on any projects that have imported the component.

When a component is in the trash or has been permanently deleted, it is still be possible to [eject the component's cells](#eject-components) into a project that it has been imported into.

#### On this page

* [Create components from within projects](#create-components-from-within-projects)
* [Create components from the home page](#create-components-from-the-home-page)
* [Import and use components](#import-and-use-components)
* [Component permissions](#component-permissions)
* [Update components](#update-components)
  + [Updating component references in bulk](#updating-component-references-in-bulk)
  + [Updating a single component reference](#updating-a-single-component-reference)
* [Eject components](#eject-components)
* [View a component's references](#view-a-components-references)
* [Delete components](#delete-components)