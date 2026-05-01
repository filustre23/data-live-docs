On this page

# Create and manage projects

Create, delete, duplicate, tag, and otherwise manage your Hex projects.

info

* The Community [plan](https://hex.tech/pricing) is limited to 5 projects.
* Users will need the Editor or Admin [role](/docs/collaborate/sharing-and-permissions/roles) to create and manage projects.

## Projects home[​](#projects-home "Direct link to Projects home")

Your default landing page in Hex is the workspace Home. You can quickly find projects you recently viewed or starred.

Each section of the Projects page can be filtered by the **category** and **status** of projects, which are defined by workspace Admins.

You can also see a variety of metadata about each project, including your level of access, the project creator, the time of last edit, [publication status](/docs/share-insights/apps/publish-and-share-apps), and total number of project views. In the **All Projects** list, projects can be sorted by either the date of most recent access or by its total number of views over all time, or in the last 7, 14, or 21 days.

Your Hex workspace provides a robust search engine that allows you to locate projects down to individual lines of code written within them. Select the workspace search bar or use the keyboard shortcut `/` to begin your search. Narrow your results down by using the filters at the top of the search modal.

## Creating a new project[​](#creating-a-new-project "Direct link to Creating a new project")

You can create projects in Hex from scratch or import them from `.ipynb` or `.yaml` files.

### Create a project from scratch[​](#create-a-project-from-scratch "Direct link to Create a project from scratch")

Select the **New project** button on the Projects page to generate an empty project.

From here, you may name the project and add a [description, status, and any categories](/docs/explore-data/projects/projects-introduction#project-metadata). By default, projects will be created using a Medium compute profile, which offers 8 GB of memory and 2 CPUs. The compute profile can be changed from the project creation modal or via the **Compute profile** section of the [**Environment**](/docs/explore-data/projects/environment-configuration/environment-views) sidebar.

### Upload an existing notebook[​](#upload-an-existing-notebook "Direct link to Upload an existing notebook")

info

While we support upload of any `.ipynb` file, you may run into package-related issues while migrating your work from environment to environment. See the [Package Management](/docs/explore-data/projects/environment-configuration/using-packages) section for more details on configuring your environment in Hex.

You can upload any existing `.ipynb` (Jupyter Notebook) file into Hex. Since this file format typically stores the outputs from the last time it was executed, the outputs will often appear instantly in the project without needing to be re-run.

If you have an existing Hex project `.yaml` file, you can upload that using the **Import** button on the **Projects home** page as well.

## Managing projects[​](#managing-projects "Direct link to Managing projects")

When editing the project, use the menu next to the project name to manage your project:

tip

Many of these actions can be performed on multiple projects at once from the **Projects** page. [Learn more](/docs/organize-content/organize-projects)

### Rename[​](#rename "Direct link to Rename")

Users with **Full Access** [project permission](/docs/collaborate/sharing-and-permissions/sharing-permissions) can rename a project. Additionally, users with the **Admin** or **Manager** [role](/docs/collaborate/sharing-and-permissions/roles) can rename any project they are able to view.

### Duplicate[​](#duplicate "Direct link to Duplicate")

Users with Editor or Admin [roles](/docs/administration/workspace_settings/overview#workspace-roles) that have **[Can Explore](/docs/explore-data/projects/docs/collaborate/sharing-and-permissions/project-sharing#can-explore)** or higher project access can duplicate the project. The new, duplicated project does not inherit any project sharing permissions from the original.

### Export[​](#export "Direct link to Export")

There are two options for file export: `.yaml` or `.ipynb`. Projects can be exported by users with **[Can Explore](/docs/explore-data/projects/docs/collaborate/sharing-and-permissions/project-sharing#can-explore)** project permission or higher. Learn more on how to use the file format options [here](/docs/explore-data/projects/import-export).

### Extract project UUID[​](#extract-project-uuid "Direct link to Extract project UUID")

To enhance readability, Hex URLs incorporate both the project title and a compressed version of the project ID.

If you need to retrieve your project's ID (for example, if you're using the [API](/docs/api-integrations/api/overview) to run/view projects.) you can do so in several ways:

1. From your project notebook, click the help menu (`?`) at the bottom of left of your project, then select "Copy project id".
2. In your project, add a code cell and retrieve the contents of the built-in variable, `hex_project_id`
3. From a published app, click the 3-dot menu at top right -> "Copy project id"
4. Use `hextoolkit` to programmatically extract the full project ID from the compressed ID included in the url. See an example code snippet below.

```
import hextoolkit as htk  
full_project_id = htk.decompress_project_id(compressed_uuid)
```

### Transfer project owner[​](#transfer-project-owner "Direct link to Transfer project owner")

Users with **Full Access** [project permission](/docs/collaborate/sharing-and-permissions/sharing-permissions), or the **Admin** or **Manager** [role](/docs/collaborate/sharing-and-permissions/roles) can transfer ownership of a project.

[Learn more about project owners](/docs/organize-content/project-owners).

### Add to collection[​](#add-to-collection "Direct link to Add to collection")

Users with any [project permission](/docs/collaborate/sharing-and-permissions/sharing-permissions) can add a project to a collection that they are a manager of.

[Learn more about adding projects to collections](/docs/organize-content/collections#add--remove-content-from-a-collection).

### Archive[​](#archive "Direct link to Archive")

Users with **Full Access** [project permission](/docs/collaborate/sharing-and-permissions/sharing-permissions), or the **Admin** or **Manager** [role](/docs/collaborate/sharing-and-permissions/roles) can archive a project.

[Learn more about archiving](/docs/organize-content/archive#manual-archive).

### Move to trash[​](#move-to-trash "Direct link to Move to trash")

Users with **Full Access** [project permission](/docs/collaborate/sharing-and-permissions/sharing-permissions), or the **Admin** or **Manager** [role](/docs/collaborate/sharing-and-permissions/roles) can move projects to the trash.

Projects will remain in the trash for 30 days, at which point they will be permanently deleted. Any permanently deleted projects will be fully removed, along with all historical versions and published apps.

### Clear outputs[​](#clear-outputs "Direct link to Clear outputs")

Clicking "Clear outputs" will clear the outputs from all cells in your project. This option is intended to be used in situations where a cell generates a very large output that crashes or overwhelms your browser. After clearing the project's outputs, it's recommended to avoid rerunning the project in order to avoid regenerating the large output. Instead, identify the cell that generated the large output, and either delete or modify it before rerunning the project.

#### On this page

* [Projects home](#projects-home)
* [Creating a new project](#creating-a-new-project)
  + [Create a project from scratch](#create-a-project-from-scratch)
  + [Upload an existing notebook](#upload-an-existing-notebook)
* [Managing projects](#managing-projects)
  + [Rename](#rename)
  + [Duplicate](#duplicate)
  + [Export](#export)
  + [Extract project UUID](#extract-project-uuid)
  + [Transfer project owner](#transfer-project-owner)
  + [Add to collection](#add-to-collection)
  + [Archive](#archive)
  + [Move to trash](#move-to-trash)
  + [Clear outputs](#clear-outputs)