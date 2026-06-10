On this page

# Workspace assets

Share data connections and secrets with your workspace or specific user groups.

Admins can create and configure shared workspace assets from **Settings > Workspace**. Each asset can be shared with your entire workspace, or with specific user groups, according to your needs.

Workspace assets are managed in the following **Settings** tabs:

* **Data sources**: Shared data connections
* **Secrets**: Shared secrets
* **Integrations**: Hex API, Git provider repositories, and cloud storage integrations like S3.

A list of projects which have imported a given workspace asset is available by clicking the link in the **Usage** column.

## Shared data connections[​](#shared-data-connections "Direct link to Shared data connections")

info

* Available on the Professional, Team, and Enterprise [plans](https://hex.tech/pricing/).
* Users will need the Admin workspace [role](/docs/collaborate/sharing-and-permissions/roles) to create and share workspace data connections.
* Users will need **Can Edit** or **Full Access** project [permissions](/docs/collaborate/sharing-and-permissions/project-sharing#project-permissions) to use data connections shared with them.

Admins can create shared data connections that can be used by all users in their workspace. The process to create connections is the same as detailed in [Data connections](/docs/connect-to-data/data-connections/data-connections-introduction).

Admins can chose a default data connection to be used as the default data source in SQL cells. To assign a default data connection, select the three-dot menu to the right of a data connection, and select **Set as default**.

warning

If you delete a shared connection it will be deleted from **all** projects that use it. Deletion cannot be undone.

## Shared Secrets[​](#shared-secrets "Direct link to Shared Secrets")

info

* Available on the Professional, Team, and Enterprise [plans](https://hex.tech/pricing/).
* Users will need the Admin workspace [role](/docs/collaborate/sharing-and-permissions/roles) to create and share workspace secrets.
* Users will need **Can Edit** or **Full Access** project [permissions](/docs/collaborate/sharing-and-permissions/project-sharing#project-permissions) to use secrets shared with them.

Admins can create shared Secrets that can be used across all projects in the Workspace. If a shared Secret is imported into a project, the Secret value will be visible to any user authorized user who has **Can Edit** or greater access to the project.

## Git Package Import[​](#git-package-import "Direct link to Git Package Import")

Connect to a Git provider to access privately-hosted Git packages. Once a package is configured for a workspace, Editors can install the package in their projects.

info

* Available on the Team and Enterprise [plans](https://hex.tech/pricing/).
* Users must be an **Admin** to connect and configure Git packages.
* Users need **Can Edit** permission on a project to import a Git package.

tip

Packages made available via Git Package Import need to be installed and imported into each project they are used in, which can increase kernel startup time. If you have packages that should be available for all Editors, or can take a while to install, consider using [custom images](/docs/administration/workspace_settings/custom-images) instead.

### Supported Git providers[​](#supported-git-providers "Direct link to Supported Git providers")

The following Git providers are supported:

| Git Provider | Notes |
| --- | --- |
| GitHub | Repositories must be hosted on github.com |
| GitHub Enterprise Server | Available to Hex workspaces on the Enterprise plan |
| GitLab | Repositories must be hosted on gitlab.com |
| Bitbucket | Repositories must be hosted on bitbucket.org |

### Set up a Git provider[​](#set-up-a-git-provider "Direct link to Set up a Git provider")

Only Hex Admins are able to set up Git export repositories. The repository access must also be approved by a repository admin on the Git side.

* GitHub
* GitHub Enterprise Server
* GitLab
* Bitbucket

1. Head to the **Settings** → **Integrations** → **Git package import**.
2. Select **+ Git Provider**, and select **GitHub**.
3. Complete the app installation and OAuth flow on GitHub's side. You will be redirected back to Hex when completed.

Note that only one GitHub account can be connected to a given Hex workspace. Similarly, a given GitHub account can only be connected to one Hex workspace.

Workspaces on the [Enterprise](https://hex.tech/pricing/) plan can import repositories that are hosted on a GitHub Enterprise Server deployment.

If you're unsure whether your organization uses GitHub Enterprise Cloud or Server:

* Repos with a URL starting with `github.com` should use the regular GitHub integration
* Repos with a custom URL will require the GitHub Enterprise Server integration

info

If your GitHub Enterprise Server deployment requires a VPN for connection, please contact [[email protected]](/cdn-cgi/l/email-protection#9deee8ededf2efe9ddf5f8e5b3e9f8fef5) for assistance with this integration.

To configure a GitHub Enterprise Server connection:

1. Head to the **Settings** → **Integrations** → **Git package import**.
2. Select **+ Git Provider**, and select **GitHub Enterprise Server**.
3. Provide the GitHub Enterprise Server URL and Organization name, and then select **Next**.

4. Use the **Create GitHub App** button to create a GitHub App on your GitHub Enterprise Instance.

5. You will be redirected to your GitHub Enterprise Server instance to create the app. All fields will be prefilled on the GitHub App creation form. Do not change any fields. You can view the required permissions of the app before creating it.

6. After creating the GitHub App, generate a client secret for it. You will need the Client ID and the Client Secret in the next step.

7. Provide the Client ID and Client Secret to Hex, then authorize the App through the OAuth flow.

1. Head to the **Settings** → **Integrations** → **Git package import**.
2. Select **+ Git Provider**, and select **GitLab**.
3. Complete the app installation and OAuth flow on GitLab's side — you will be redirected back to Hex when completed.

Note that only one GitLab account can be connected to a given Hex workspace. Similarly, a given GitLab account can only be connected to one Hex workspace.

To connect your Bitbucket account to Hex, you will need to generate an App Password. We recommend creating a separate service account on your Bitbucket workspace to support this.

1. In Bitbucket, select **Personal Bitbucket settings** from the top right Settings menu

2. On the left, select App passwords

3. Create an App Password with Read access to Repositories:

Then connect to your Bitbucket account in Hex:

1. Head to the **Settings** → **Integrations** → **Git package import**.
2. Select **+ Git Provider**, and select **Bitbucket**.
3. Provide the Workspace ID, Username and App Password you generated above.

### Configure Packages[​](#configure-packages "Direct link to Configure Packages")

Once you've configured a Git provider, you can select individual repos to be made available as packages. Once a package is configured for a workspace, Editors can import the package to their projects.

To configure a package, select the **+ Package** button.

You can set up a package to install a specific branch, tag, or commit of a package. If you install a branch (e.g. `main`), when the package is imported, code from that branch will be made available. If you would prefer to pin the version of the package which is imported to Hex you should select either the tag or commit SHA of the desired version.

Package install instructions can be customized via the **Install commands** section of the **Add a package** dialog. If no optional commands are provided, by default the GitHub package is zipped and downloaded in its entirety.

If your Git package includes pip-installable modules, you can specify how those packages are installed via a command similar to `uv pip install .` (the command will be run from the root of your repository). The details of your repository structure and content will dictate the specific install commands required.

Since projects that use this package will download and install it every time they run, [we recommend](/docs/explore-data/projects/environment-configuration/using-packages#install-new-packages-through-uv-pip) using `uv pip install` instead of `pip install` for the installation command. This will make the installation much faster, allowing projects that use the package to launch faster.

You can also configure which groups can import the package into a project.

Once you have successfully added a repository and package to Hex, Editors will be able to import it to their projects for use. See [Using packages](/docs/explore-data/projects/environment-configuration/using-packages#git-packages) for instructions on using Git packages in a project.

## External file integrations[​](#external-file-integrations "Direct link to External file integrations")

info

* Available on the Professional, Team, and Enterprise [plans](https://hex.tech/pricing/).

Admins can create workspace-level access to external storage services. To do so, navigate to the **Integrations** tab under the "Workspace" header and click the **Connect** button under the "External file integrations" section. From here, a storage service can be selected. Once the connection is created, users with access can [import the available files into their project](/docs/explore-data/projects/environment-configuration/files#external-files).

### Amazon S3[​](#amazon-s3 "Direct link to Amazon S3")

In order to connect to S3, you will need to input the name of the bucket, the region, and access keys for an IAM user. The IAM user must be allowed to perform the `ListBucket` and `GetObject` actions on the bucket and files and folders in the bucket.

The **Enable writeback** toggle will control whether or not this integration can [export files from Hex to the S3 bucket](/docs/explore-data/projects/environment-configuration/files#export-files-to-external-file-integrations). The IAM user will also need to have `PutObject` permissions in order to update files or create new files in the bucket.

### Google Cloud Storage (GCS)[​](#google-cloud-storage-gcs "Direct link to Google Cloud Storage (GCS)")

In order to connect to GCS, you will need to input the name of the bucket and the service account key. For more detailed instructions on how to set up your Service Account, you can check out [this guide](https://www.analyticsvidhya.com/blog/2020/07/read-and-update-google-spreadsheets-with-python/). You will need to add the `storage.buckets.get` permission to the default “Storage Object User” in GCS. In addition, you can select which groups have access to GCS.

The **Enable writeback** toggle will control whether or not this integration can [export files from Hex to the GCS bucket](/docs/explore-data/projects/environment-configuration/files#export-files-to-external-file-integrations).

## Understand shared asset permissions[​](#understand-shared-asset-permissions "Direct link to Understand shared asset permissions")

As an Admin, you can set who is able to use a workspace asset (which includes Data connections, Secrets, and GitHub packages). By default, a workspace asset is shared with all workspace users. This means users with either Editor or Admin roles can use an asset in projects and Viewers will be able to view them. However, Guests of your workspace will not be able to use or view workspace assets by default, even when they are given **Can Edit** permissions on a project.

caution

Workspace asset permissions do *not* control who can view the results derived from shared workspace assets (e.g. the output from querying a workspace data connection). Access to view a project is defined by its [sharing permissions](/docs/collaborate/sharing-and-permissions/sharing-permissions).

To set the permissions on a workspace asset, head to the **Settings**, then **Data sources** to set permissions for shared data connections, **Secrets** for shared secrets, or **Integrations** for Github or Gitlab repositories. You can either add a new asset, or edit an existing one via the three-dot menu icon. Then, at the bottom of the modal, add the desired groups under the "Groups with access" heading.

Hex provides you with three built-in groups to add to an asset, whose membership is determined via a user's role within your workspace. You can learn more about workspace roles [here](/docs/administration/workspace_settings/overview#user-roles).

* **Workspace** (default): All Viewers, Editors, and Admins.
* **Workspace guests**: Only Guests of a workspace.
* **Public**: All users of a workspace, including users who are viewing an app shared with the web (and are not part of the workspace).

In addition to these groups, you can share a connection with any custom defined groups. You can learn more about defining groups [here](/docs/administration/workspace_settings/overview#groups).

tip

Getting started with workspace connections? We recommend using the default permissions, share with workspace, so that all workspace users have access to the shared connection.

If a user does not have access to a workspace asset, they are not able to edit projects which use that asset, effectively downgrading their project permissions to **Can Explore**. Here are some common scenarios that outline how workspace roles, project permissions, and data connection access may limit a user's access to a project.

| Workspace role | Project permission | Has access to the data connection | Effective project permission | Comment |
| --- | --- | --- | --- | --- |
| Editor | Can Edit or Full Access | Yes | Can Edit or Full Access |  |
| Editor | Can Edit or Full Access | No | Downgraded to Can Explore | Hex will try to prevent you from adding a user with "Can Edit" permissions who does not have access to a workspace asset that is used in the project |
| Admin | Can Edit or Full Access | Always | Can Edit or Full Access | Admins inherit access to all workspace assets |

## Shared data connection permissions in practice[​](#shared-data-connection-permissions-in-practice "Direct link to Shared data connection permissions in practice")

Here are a few common examples to help you wrap your head around the best way to set up your permissions.

* **A data connection used for analytics:** By default, a workspace data connection is shared with all users. This means that anyone with **Can Edit** permissions on a project can use this connection when editing Hex projects. Guests of your workspace will be prevented from using this connection when they have **Can Edit** project permissions.
* **A sensitive data connection:** Consider sharing this data connection with a workspace-defined group, for example "Data Team".

  + When a user of the "Data Team" group creates a project, they will be able to add the connection to their project
  + Anyone outside of that group will not be able to add the data connection to their Hex projects (or see it as an option to be added).
  + If a member of "Data Team" tries to add a user outside of the "Data Team" with **Can Edit** permissions on a project they will not be able to, and will receive a warning to this effect.
  + All Admins can be granted **Can Edit** permissions to any project — because Admins can change permissions on a workspace asset to include themselves, they effectively already have this permission.
* **A data connection for interviewing candidates:** If you're using Hex to run technical assessments for candidates (a great use case!), it's likely that you'll add the candidate as a Guest in your workspace. To allow a Guest to use a data connection, you'll need to explicitly add the "Workspace guests" group to the data connection.

#### On this page

* [Shared data connections](#shared-data-connections)
* [Shared Secrets](#shared-secrets)
* [Git Package Import](#git-package-import)
  + [Supported Git providers](#supported-git-providers)
  + [Set up a Git provider](#set-up-a-git-provider)
  + [Configure Packages](#configure-packages)
* [External file integrations](#external-file-integrations)
  + [Amazon S3](#amazon-s3)
  + [Google Cloud Storage (GCS)](#google-cloud-storage-gcs)
* [Understand shared asset permissions](#understand-shared-asset-permissions)
* [Shared data connection permissions in practice](#shared-data-connection-permissions-in-practice)