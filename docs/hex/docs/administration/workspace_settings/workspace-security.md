On this page

# Workspace security

Workspace Admins can configure their workspace settings to restrict who can access and share what assets.

info

* Available on Team and Enterprise [plans](https://hex.tech/pricing).
* Only workspace Admins can configure these settings.

## Project sharing settings[​](#project-sharing-settings "Direct link to Project sharing settings")

### Share projects to web[​](#share-projects-to-web "Direct link to Share projects to web")

When on, users with **Full Access** and **Can Edit** project permissions will have the option to turn on [**Share to web**](/docs/collaborate/sharing-and-permissions/sharing-permissions#public-share-permissions) at the project level. When enabled in the project, anyone with the link to the project would be able to navigate to and interact with the project.

### Export apps as PDFs[​](#export-apps-as-pdfs "Direct link to Export apps as PDFs")

When on, users can include a screenshot of published apps (including data and visualizations) in [app notifications](/docs/administration/workspace_settings/docs/share-insights/app-notifications) notifications. Any user with "App User" access or higher can be designated as a recipient of the email. This setting also enables any authenticated user with "App User" access to [export PDFs](/docs/share-insights/apps/export-as-pdf) from published apps.

### Allow Notion link preview[​](#allow-notion-link-preview "Direct link to Allow Notion link preview")

When on, workspace users can embed Hex project info including individual cells or full apps in Notion. Embedded project details can be viewed by anyone with access to the Notion page. For more information, see Hex's [embedding documentation](/docs/share-insights/embedding/public-and-private-embedding).

### Generate app links with current inputs[​](#generate-app-links-with-current-inputs "Direct link to Generate app links with current inputs")

When on, workspace users can generate a link to the Published app which includes the current inputs in the URL as query parameters. Inputs are represented as plaintext in the generated URL, so use caution if inputs include sensitive information. For more information, see Hex's [publishing documentation](/docs/share-insights/apps/publish-and-share-apps#current-inputs).

### Download and copy CSVs from tables[​](#download-and-copy-csvs-from-tables "Direct link to Download and copy CSVs from tables")

info

Teams on the Enterprise [plan](https://hex.tech/pricing) can disable this setting.

By default, Hex provides a convenient way for users to download and copy tabular data that they can see (and have access to) in published apps and notebooks. By default, users with Viewer roles can download and copy tabular data they can see in published apps. Users with Explorer roles or higher can download or copy tabular data in published apps and notebooks, and download or copy the data that makes up a chart.

By disabling this feature, users who are **viewing** a project will no longer be able to copy or download data. This includes viewing a published app, or a project's notebook.

Note that users who are editing a project will continue to have access to this button.

**Why can't I disable this functionality for users that are editing projects?**

Due to the flexibility that Python cells provide, users that are editing projects are able to export data via code. Therefore, disabling the ability to download or copy data for when editing a project would not be a true safeguard against moving data outside of Hex. As such, we kept this functionality in place when editing a project.

### Send data to Google Sheets[​](#send-data-to-google-sheets "Direct link to Send data to Google Sheets")

info

Teams on the Enterprise or Team [plan](https://hex.tech/pricing) can export to Google Sheets and disable this setting.

By default, Hex provides a convenient way for users to send tabular data that they can see (and have access to) directly to Google Sheets from published apps, notebooks, and during scheduled runs. Users with Viewer roles can send tabular data they can see in published apps to Google Sheets. Users with Explorer roles or higher can send tabular data from published apps, notebooks, and scheduled runs to Google sheets.

By disabling this feature, users will no longer see the option to send data to Google sheets when viewing a published app, a project's notebook, or creating scheduled notifications.

### Allow file uploads[​](#allow-file-uploads "Direct link to Allow file uploads")

info

Teams on the Enterprise [plan](https://hex.tech/pricing) can disable this setting.

By default, users can upload files to Hex, allowing users to flexibly analyze data from a variety of sources. This includes:

* Uploading files via the [files sidebar](/docs/explore-data/projects/environment-configuration/files)
* Importing files from [external file integrations](/docs/explore-data/projects/environment-configuration/files#external-files)
* Uploading files via the [file upload input cell](/docs/explore-data/cells/input-cells/file-upload-inputs)

Admins can disable file uploads in their workspace which will disable all of the above methods of uploading files.

Note that disabling this feature will only prevent new files from being uploaded — any projects that already have files uploaded will continue to work as they did before this setting was disabled.

### Show workspace secret values in project UI[​](#show-workspace-secret-values-in-project-ui "Direct link to Show workspace secret values in project UI")

info

Teams on the Enterprise [plan](https://hex.tech/pricing) can disable this setting.

By default, users with **Can Edit** access to a project can reveal the value of a secret by clicking the eye icon next to the secret.

Disabling this setting prevents users from revealing the value of a secret in the UI.

Note that this is **not** a failsafe method to prevent a user from accessing this value — Editors can still use methods in Python cells to gain access to the secret's value.

### Allow project-level data connections[​](#allow-project-level-data-connections "Direct link to Allow project-level data connections")

info

Teams on the Enterprise [plan](https://hex.tech/pricing) can disable this setting.

By default, users with the Editor role can create [project data connections](/docs/connect-to-data/data-connections/data-connections-introduction#project-and-workspace-data-connections) that are scoped to the project they are created in.

Admins may choose to disable this feature so that data connections can only be created in workspace settings by Admins.

If disabled, any existing project data connections will continue to work. Reach out to [support](/cdn-cgi/l/email-protection#3b484e4b4b54494f7b535e43154f5e5853) to get a list of projects that are currently using a project data connection.

## SSO configuration[​](#sso-configuration "Direct link to SSO configuration")

Configure Hex to allow authentication via your SSO provider. Hex currently only supports Open ID Connect (OIDC) SSO.

See [Hex's documentation on configuring SSO](/docs/administration/sso) for set-up instructions.

## API settings[​](#api-settings "Direct link to API settings")

### Enable API access[​](#enable-api-access "Direct link to Enable API access")

When on, users will be able to configure and use tokens to access the Hex public API. Admins can specify the maximum expiration for personal access tokens created by users. For more information, see [Hex's public API documentation](/docs/api-integrations/api/overview).

warning

Setting the maximum expiration to a lower value will revoke any existing tokens that have existed longer than the new maximum expiration.

## Workspace SSH key[​](#workspace-ssh-key "Direct link to Workspace SSH key")

This key is used when configuring Data Connections to [connect via SSH](/docs/connect-to-data/data-connections/connect-via-ssh).

#### On this page

* [Project sharing settings](#project-sharing-settings)
  + [Share projects to web](#share-projects-to-web)
  + [Export apps as PDFs](#export-apps-as-pdfs)
  + [Allow Notion link preview](#allow-notion-link-preview)
  + [Generate app links with current inputs](#generate-app-links-with-current-inputs)
  + [Download and copy CSVs from tables](#download-and-copy-csvs-from-tables)
  + [Send data to Google Sheets](#send-data-to-google-sheets)
  + [Allow file uploads](#allow-file-uploads)
  + [Show workspace secret values in project UI](#show-workspace-secret-values-in-project-ui)
  + [Allow project-level data connections](#allow-project-level-data-connections)
* [SSO configuration](#sso-configuration)
* [API settings](#api-settings)
  + [Enable API access](#enable-api-access)
* [Workspace SSH key](#workspace-ssh-key)