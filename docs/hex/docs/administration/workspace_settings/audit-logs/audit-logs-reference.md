On this page

# Audit logs event reference

## Audit log event schema[​](#audit-log-event-schema "Direct link to Audit log event schema")

Hex audit logs are emitted in JSON format. Some notable fields in the schema are:

* **action**: type of action taken
* **actor**: identifies the user or client (e.g. API) making the request
* **context**: the location (IP address) and user agent of the actor
* **targets**: Hex resources that are affected or created by this action

The following is an example event object:

```
{



"actor": {



"id": "b44446e6-8264-4af5-a856-fdc2fa8fe132",



"type": "USER",



"metadata": {



"email": "user@hex.tech",



"workspace": "Hex",



"workspaceId": "57c59cf9-c943-4386-afb5-75df1af3b2f7"



}



},



"action": "RUN_CELL",



"context": {



"location": "1.1.1.1",



"user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"



},



"targets": [



{



"id": "f426633a-0993-4bbc-be6a-740e28da2596",



"type": "project",



"metadata": {



"representation": "{\"id\":\"f426633a-0993-4bbc-be6a-740e28da2596\",\"createdDate\":\"2024-04-08T20:15:06.337Z\",\"updatedDate\":\"2024-04-12T15:38:25.265Z\",\"archivedDate\":null,\"creatorId\":\"b44446e6-8264-4af5-a856-fdc2fa8fe132\",\"canEditorsShare\":true,\"projectLanguage\":\"PYTHON\",\"hexType\":\"PROJECT\",\"organizationRole\":null,\"publicRole\":null}"



}



},



{



"id": "60d9ac4d-7eb2-4638-9423-61bdf8a331ef",



"type": "project_version",



"metadata": {



"representation": "{\"id\":\"60d9ac4d-7eb2-4638-9423-61bdf8a331ef\",\"createdDate\":\"2024-04-08T20:15:06.337Z\",\"updatedDate\":\"2024-04-12T15:38:25.127Z\",\"title\":\"Sample Project\",\"description\":\"\",\"hexId\":\"f426633a-0993-4bbc-be6a-740e28da2596\",\"creatorId\":\"b44446e6-8264-4af5-a856-fdc2fa8fe132\",\"timezone\":null,\"version\":\"draft\",\"published\":false,\"import\":false,\"kernelSize\":\"medium\",\"autoRerun\":true,\"cacheAppState\":true}"



}



},



{



"id": "340ba95d-465a-44d2-8b04-8a83c6c5b1e5",



"type": "cell",



"metadata": {



"representation": "{\"id\":\"2e56c683-8151-4071-918f-0050ce854637\",\"createdDate\":\"2024-04-08T20:15:17.810Z\",\"updatedDate\":\"2024-04-08T20:15:17.810Z\",\"cellType\":\"SQL\"}"



}



}



],



"version": 1,



"metadata": {



"result": "SUCCESS",



"requestArgs": "{\"hexId\":\"f426633a-0993-4bbc-be6a-740e28da2596\",\"hexVersionId\":\"60d9ac4d-7eb2-4638-9423-61bdf8a331ef\",\"cellId\":\"2e56c683-8151-4071-918f-0050ce854637\"}",



"failureReason": ""



},



"occurred_at": "2024-04-12T15:38:27.073Z"



}
```

## Audit log target resource types[​](#audit-log-target-resource-types "Direct link to Audit log target resource types")

The following resource types appear as target resources in audit log events:

| Resource type | Notes |
| --- | --- |
| Agent chat message | A message sent to the Notebook agent |
| API client | An API token, either a personal token or a workspace token |
| Cell | A [cell](/docs/explore-data/cells/sql-cells/sql-cells-introduction) in a Hex project |
| Collection | A [collection](/docs/organize-content/collections) of Hex projects and components |
| Data connection | A [connection](/docs/connect-to-data/data-connections/data-connections-introduction) to an external data warehouse |
| Data source database | A database in a data connection's schema browser |
| Data source schema | A schema in a data connection's schema browser |
| Data source table | A table in a data connection's schema browser |
| Docker image repository | A custom Docker image repository connected to the workspace |
| Domain | A domain allowed to be associated with your Hex workspace |
| External file integration | An [integration](/docs/connect-to-data/cloud-storage-integrations) with a cloud storage provider like AWS S3 or Google Drive |
| File | A [file](/docs/connect-to-data/upload-files) uploaded to a Hex project |
| Folder item | A folder, or a project in a folder |
| Folder item grant | A role given to a user or group for access to a folder item |
| Group | A group of Hex users that can be granted access to resources |
| Guide | A workspace guide that gives the Hex agent context |
| Magic API key | An [API key](/docs/trust/ai-data-privacy#bring-your-own-key-byok) for authenticating magic requests |
| MCP server configuration | An MCP server enabled for the workspace |
| Project | A Hex [project](/docs/explore-data/projects/projects-introduction), [component](/docs/explore-data/components), or [explore](/docs/share-insights/explore) object |
| Project grant | A role (viewer, editor, etc.) given to a user or group for [access to a Hex project](/docs/collaborate/sharing-and-permissions/project-sharing) |
| Project ref | A branch of a project |
| Project version | A specific [version](/docs/explore-data/projects/history-and-versions) of a Hex project |
| Project view | An object that represents an instance of a user viewing a project |
| Scheduled run | A cron-like [schedule](/docs/share-insights/scheduled-runs) on which a project is run periodically |
| Scheduled run notification | A [notification](/docs/share-insights/scheduled-runs#send-notifications) configured on a scheduled run, to send emails and/or Slack messages when a scheduled run completes or fails |
| Secret | A [secret value](/docs/explore-data/projects/environment-configuration/environment-views#secrets) containing sensitive information that can be referenced in Hex projects |
| Semantic dataset | A dataset in a semantic model |
| Semantic project | A [semantic project](/docs/connect-to-data/semantic-models/intro-to-semantic-models) containing shared definitions for data models |
| Semantic view | A view in a semantic model |
| Sync repository | A Git repository synced with the workspace |
| Task | A scheduled agent task |
| Template | A Hex-provided project template |
| Thread | A [Thread](/docs/explore-data/threads) with the Hex agent |
| User | A Hex user (could be email user, API user, etc.) |
| User attribute | A workspace-defined attribute that can be set on users |
| User attribute value | A user's value for a user attribute |
| User MCP server connection | A user's connection to an MCP server |
| VCS connection | A connection to a version control provider such as GitHub |
| Workspace | A representation of your Hex workspace |

Some event types include target resources with a type of **principal**. This indicates that this object can be one of multiple types.
For instance, the UPDATE\_PROJECT\_ACCESS event type includes a principal resource which is either a Group or a User.

In the same way, the data asset status events have a single target of type **data\_asset**. Its `resource_type` metadata says which kind of asset it is, such as `data_source_table` or `semantic_dataset`.

## Audit log event types[​](#audit-log-event-types "Direct link to Audit log event types")

Events are grouped by area. When an action fails or is denied, the event is usually still logged, with `result` set to `FAILURE` in its metadata. Failed attempts to create something aren't logged, since there's no created resource to target.

### Sign-in[​](#sign-in "Direct link to Sign-in")

| Event type | Description | Target resource types |
| --- | --- | --- |
| `USER_SIGNED_UP` | A user logs in for the first time | User |
| `USER_LOGGED_IN` | A user logs in or attempts to log in | User |
| `USER_LOGGED_OUT` | A user logs out | User |

### Users[​](#users "Direct link to Users")

| Event type | Description | Target resource types |
| --- | --- | --- |
| `CREATE_USERS` | An admin invites users to the workspace by email | Workspace, User |
| `CREATE_PASSWORD_USER` | An admin creates a user who signs in with a password | User |
| `INVITE_USER_AS_ADMIN` | An admin invites a user to the workspace as an admin | Workspace |
| `ACTIVATE_USER` | An admin reactivates a deactivated user | User |
| `DEACTIVATE_USER` | An admin deactivates a user. If the user's projects are transferred to someone else, that user is also a target | User |
| `EDIT_USER` | An admin edits a user's name, email, password, or workspace role | User |
| `UPDATE_USER_ROLE` | An admin changes a user's workspace role | User |
| `REQUEST_ORG_ROLE` | A user asks workspace admins for a different workspace role | User |
| `VIEW_USER_DRAFTS` | An admin views another user's drafts folder | User |

### Groups[​](#groups "Direct link to Groups")

| Event type | Description | Target resource types |
| --- | --- | --- |
| `CREATE_GROUP` | An admin creates a group | Group |
| `UPDATE_GROUP` | An admin renames a group. A change that also adds or removes members logs `UPDATE_GROUP_MEMBERS` instead | Group |
| `UPDATE_GROUP_MEMBERS` | An admin adds or removes users from a group | Group, User |
| `DELETE_GROUP` | An admin deletes a group | Group |

### User attributes[​](#user-attributes "Direct link to User attributes")

| Event type | Description | Target resource types |
| --- | --- | --- |
| `CREATE_USER_ATTRIBUTE` | An admin creates a user attribute | Workspace, User attribute |
| `RENAME_USER_ATTRIBUTE` | An admin renames a user attribute | User attribute, Workspace |
| `DELETE_USER_ATTRIBUTE` | An admin deletes a user attribute | User attribute, Workspace |
| `SET_USER_ATTRIBUTE_VALUES` | An admin sets a user's user attribute values | Workspace, User |
| `UPSERT_USER_ATTRIBUTE_VALUES` | An admin sets a user attribute's values for one or more users | Workspace, User attribute |
| `CLEAR_USER_ATTRIBUTE_VALUE` | An admin clears a user's value for a user attribute | Workspace, User attribute value |

### Directory sync[​](#directory-sync "Direct link to Directory sync")

| Event type | Description | Target resource types |
| --- | --- | --- |
| `PAUSE_DIRECTORY_SYNC` | An admin pauses directory sync for the workspace | Workspace |
| `RESUME_DIRECTORY_SYNC` | An admin resumes directory sync for the workspace | Workspace |
| `SET_DIRECTORY_SYNC_ADMIN_GROUP` | An admin sets or clears the directory sync group for Admins | Group |
| `SET_DIRECTORY_SYNC_MANAGER_GROUP` | An admin sets or clears the directory sync group for Managers | Group |
| `SET_DIRECTORY_SYNC_AUTHOR_GROUP` | An admin sets or clears the directory sync group for Editors | Group |
| `SET_DIRECTORY_SYNC_EXPLORER_GROUP` | An admin sets or clears the directory sync group for Explorers | Group |

### API tokens[​](#api-tokens "Direct link to API tokens")

Changing a token's description or expiration always regenerates it, so the `UPDATE_*_API_CLIENT` events are the only record of those changes. The old token is the target and the new token is created. The new description and expiration policy are in the event's request arguments.

| Event type | Description | Target resource types |
| --- | --- | --- |
| `GRANT_USER_API_ACCESS` | An admin lets a user create API tokens | User |
| `REVOKE_USER_API_ACCESS` | An admin stops a user from creating API tokens and rejects requests made with that user's tokens | User |
| `CREATE_USER_API_CLIENT` | A user creates a personal API token in settings or through CLI login | API client |
| `UPDATE_USER_API_CLIENT` | A user regenerates a personal API token, revoking the old one and creating a new one | API client |
| `REVOKE_USER_API_CLIENT` | A user revokes a personal API token | API client |
| `CREATE_WORKSPACE_TOKEN_API_CLIENT` | An admin creates a workspace API token | API client |
| `UPDATE_WORKSPACE_TOKEN_API_CLIENT` | An admin regenerates a workspace API token, revoking the old one and creating a new one | API client |
| `REVOKE_WORKSPACE_TOKEN_API_CLIENT` | An admin revokes a workspace API token | API client |
| `UPDATE_API_TOKEN_EXPIRATION_POLICY` | An admin changes the [expiration policy](/docs/api-integrations/api/overview#token-expiration) for API tokens | Workspace |

### Workspace settings[​](#workspace-settings "Direct link to Workspace settings")

| Event type | Description | Target resource types |
| --- | --- | --- |
| `ADD_WORKSPACE_DOMAIN` | An admin adds an [allowed domain](/docs/administration/workspace_settings/overview#allowed-domains) to the workspace | Domain |
| `DELETE_WORKSPACE_DOMAIN` | An admin removes an allowed domain from the workspace | Domain |
| `UPDATE_SSO_CONFIGURATION` | An admin [configures SSO](/docs/administration/workspace_settings/workspace-security#sso-configuration) for the workspace | Workspace |
| `UPDATE_PUBLIC_SHARING_SETTING` | An admin changes whether projects in the workspace can be shared publicly | Workspace |
| `UPDATE_ALLOW_GUESTS_SETTING` | An admin changes whether guest users can be added to the workspace | Workspace |
| `UPDATE_ALLOW_NOTION_PREVIEW` | An admin changes whether Hex links show previews in Notion | Workspace |
| `UPDATE_ALLOW_CSV_DOWNLOADS` | An admin changes whether users can download CSVs | Workspace |
| `UPDATE_ALLOW_FILE_UPLOADS` | An admin changes whether users can upload files to projects | Workspace |
| `UPDATE_ALLOW_EXTERNAL_EXPORTS` | An admin changes whether external exports are allowed in the workspace | Workspace |
| `UPDATE_ALLOW_PROJECT_LEVEL_DATA_CONNECTIONS` | An admin changes whether users can add data connections from projects instead of the admin panel | Workspace |
| `UPDATE_ALLOW_VIEW_WORKSPACE_SECRETS_IN_PROJECT_UI` | An admin changes whether workspace secrets can be viewed from the project UI | Workspace |
| `UPDATE_CUSTOM_ROLE_REQUEST_CONFIG` | An admin changes the role request settings, such as disabling requests or setting a message | Workspace |
| `SET_DATA_RETENTION_CELL_OUTPUTS` | An admin sets the data retention period for cell outputs | Workspace |
| `SET_DATA_RETENTION_QUERY_CACHE` | An admin sets the data retention period for query cache entries | Workspace |
| `TOGGLE_WORKSPACE_QUERY_CACHE` | An admin turns workspace query caching on or off | Workspace |
| `UPDATE_WORKSPACE_LOGIC_QUERY_CACHE_TIMEOUT` | An admin changes the default query cache timeout for notebooks | Workspace |
| `UPDATE_WORKSPACE_PUBLISHED_QUERY_CACHE_TIMEOUT` | An admin changes the default query cache timeout for published apps | Workspace |
| `VIEW_WORKSPACE_SSH_KEY` | An admin views the workspace SSH key | Workspace |
| `CONNECT_CUSTOM_IMAGE_REPO` | An admin connects a Docker Hub, ECR, or Google Artifact Registry image repository | Docker image repository |
| `DISCONNECT_CUSTOM_IMAGE_REPO` | An admin disconnects a custom Docker image repository | Docker image repository |

### AI settings and credits[​](#ai-settings-and-credits "Direct link to AI settings and credits")

| Event type | Description | Target resource types |
| --- | --- | --- |
| `UPDATE_WORKSPACE_MAGIC_SETTINGS` | An admin changes the workspace's AI settings, including the agent's trusted mode policy | Workspace |
| `CREATE_MAGIC_API_KEY` | An admin adds or replaces a [bring-your-own-key](/docs/trust/ai-data-privacy#bring-your-own-key-byok) API key for AI features | Magic API key |
| `DELETE_MAGIC_API_KEY` | An admin deletes a bring-your-own-key API key | Magic API key |
| `UPDATE_ORG_DEFAULT_AI_CREDIT_LIMIT` | An admin changes the default per-user AI credit limit for the workspace | Workspace |
| `SET_USER_AI_CREDIT_LIMIT` | An admin sets a user's AI credit limit | User |
| `REMOVE_USER_AI_CREDIT_LIMIT` | An admin removes a user's AI credit limit | User |
| `SET_GROUP_AI_CREDIT_LIMIT` | An admin sets a group's AI credit limit | Group |
| `REMOVE_GROUP_AI_CREDIT_LIMIT` | An admin removes a group's AI credit limit | Group |
| `UPDATE_AI_CREDIT_TOPUPS_ENABLED` | An admin turns AI credit top-ups on or off for the workspace | Workspace |
| `UPDATE_AI_CREDIT_TOPUP_BATCH_SIZE` | An admin changes how many AI credits each automatic top-up purchases | Workspace |
| `UPDATE_AI_CREDIT_TOPUP_SPEND_LIMIT` | An admin changes the spend limit for automatic AI credit top-ups | Workspace |

### Projects[​](#projects "Direct link to Projects")

| Event type | Description | Target resource types |
| --- | --- | --- |
| `CREATE_PROJECT` | A user creates a project, component, or 4.0 project | Project |
| `CREATE_PROJECT_FROM_TEMPLATE` | A user creates a project from a [template](https://hex.tech/use-cases/) | Project, Template |
| `DUPLICATE_PROJECT` | A user duplicates a project or 4.0 project. Both the original and the copy are targets | Project |
| `COPY_PROJECT_FROM_EXTERNAL_WORKSPACE` | A user copies a project from another workspace into this one | Project |
| `IMPORT_PROJECT` | A user [imports a project](/docs/explore-data/projects/import-export#import-projects) from a YAML file, a Jupyter notebook, or a Claude dashboard | Project |
| `VIEW_PROJECT` | A user opens a project's notebook or app (4.0 projects log `VIEW_CODE_PROJECT`), including through Notion previews, snapshots, and signed embeds | Project, Project version, Project view |
| `RUN_PROJECT` | A project runs top to bottom, whether started by a user, a scheduled run, or the agent | Project, Project version |
| `RUN_CELL` | A user runs a single cell in a project | Project, Project version, Cell |
| `PUBLISH_PROJECT` | A user publishes a project's app, directly or by approving a publish review request | Project |
| `RENAME_PROJECT` | A user renames a project or 4.0 project from its folder | Project |
| `SET_PROJECT_OWNER` | A user transfers ownership of a project or 4.0 project to another user | Project, User |
| `DELETE_PROJECT` | A user moves a project or 4.0 project to the trash | Project |
| `RESTORE_PROJECT` | A user restores a project or 4.0 project from the trash | Project |
| `PERMANENTLY_DELETE_PROJECT` | A user permanently deletes a project, including when its folder is permanently deleted | Project |
| `UPDATE_COMPONENT_IN_HEXES` | An admin updates projects that use a component to its latest published version. The component is the target | Project |
| `UPLOAD_FILE_TO_PROJECT` | A user uploads a file to a project (4.0 projects log `UPLOAD_CODE_PROJECT_FILE`) | Project, File |
| `DOWNLOAD_FILE_FROM_PROJECT` | A user downloads a file uploaded to a project | Project, File |

### Explores[​](#explores "Direct link to Explores")

| Event type | Description | Target resource types |
| --- | --- | --- |
| `CREATE_EXPLORE` | A user creates an [explore](/docs/share-insights/explore) that doesn't start from a project cell | Project |
| `CREATE_EXPLORE_FROM_PROJECT_CELL` | A user starts an explore from a cell in a project or app | Project, Cell |
| `CREATE_PROJECT_FROM_EXPLORE` | A user converts an explore into a project | Project |

### Sharing and access[​](#sharing-and-access "Direct link to Sharing and access")

| Event type | Description | Target resource types |
| --- | --- | --- |
| `REQUEST_PROJECT_ROLE` | A user requests access to a project | Project, User |
| `GRANT_USERS_PROJECT_ACCESS` | A user gives one or more users a role on a project | Project, User, Project grant |
| `GRANT_GROUPS_PROJECT_ACCESS` | A user gives one or more groups a role on a project | Project, Group, Project grant |
| `GRANT_ADMIN_PROJECT_ACCESS` | An admin grants themselves a role on a project | Project, User, Project grant |
| `UPDATE_PROJECT_ACCESS` | A user changes a user's or group's role on a project | Project, Principal, Project grant |
| `REMOVE_PROJECT_ACCESS` | A user removes a user's or group's access to a project | Project, Principal |
| `SHARE_PROJECT_WITH_SUPPORT` | A user shares a project with Hex support | Project |
| `SHARE_PROJECT_WITH_ORG` | A user changes or removes a project's workspace-wide access role | Project |
| `SHARE_PROJECT_WITH_PUBLIC` | A user changes or removes a project's public web access role | Project |
| `UPDATE_PROJECT_PUBLIC_DUPLICATION_ALLOWED` | A user changes whether people in other workspaces can duplicate a project | Project |
| `UPDATE_ALLOW_EMBEDDING` | A user turns signed embedding on or off for a project | Project |

### Folders[​](#folders "Direct link to Folders")

| Event type | Description | Target resource types |
| --- | --- | --- |
| `CREATE_FOLDER` | A user creates a folder | Folder item |
| `RENAME_FOLDER` | A user renames a folder | Folder item |
| `MOVE_FOLDER` | A user moves a folder into another folder | Folder item |
| `DELETE_FOLDER` | A user moves a folder to the trash | Folder item |
| `RESTORE_FOLDER` | A user restores a folder from the trash | Folder item |
| `PERMANENTLY_DELETE_FOLDER` | A user permanently deletes a folder | Folder item |
| `GRANT_FOLDER_ENTRY_ACCESS` | A user gives a user or group access to a folder or project | Folder item, Folder item grant |
| `UPDATE_FOLDER_ENTRY_ACCESS` | A user changes an existing user's or group's access level on a folder or project | Folder item, Folder item grant |
| `REVOKE_FOLDER_ENTRY_ACCESS` | A user removes someone's access to a folder or project in a folder | Folder item, Folder item grant |
| `MOVE_PROJECT_TO_FOLDER` | A user moves a project or 4.0 project into a folder | Project, Folder item |
| `MOVE_PROJECT_TO_DRAFTS` | A user moves a project or 4.0 project to their drafts | Project, Folder item |

### Collections[​](#collections "Direct link to Collections")

| Event type | Description | Target resource types |
| --- | --- | --- |
| `CREATE_COLLECTION` | A user creates a collection | Collection |
| `EDIT_COLLECTION` | A user edits a collection's name, description, managers, or members | Collection |
| `ADD_PROJECTS_TO_COLLECTION` | A user adds projects to a collection | Collection, Project |
| `REMOVE_PROJECT_FROM_COLLECTION` | A user removes a project from a collection | Collection, Project |
| `UPDATE_COLLECTION_ROLE_IN_PROJECT` | A user changes the role a collection has on a project | Collection, Project |

### Scheduled runs[​](#scheduled-runs "Direct link to Scheduled runs")

| Event type | Description | Target resource types |
| --- | --- | --- |
| `CREATE_SCHEDULED_RUN` | A user creates a scheduled run | Project, Scheduled run |
| `EDIT_SCHEDULED_RUN` | A user edits, turns on, or turns off a scheduled run | Project, Scheduled run |
| `DELETE_SCHEDULED_RUN` | A user deletes a scheduled run | Project, Scheduled run |
| `CREATE_SCHEDULED_RUN_NOTIFICATION` | A user adds a notification to a scheduled run | Scheduled run, Scheduled run notification, Project |
| `EDIT_SCHEDULED_RUN_NOTIFICATION` | A user edits a scheduled run's notification | Scheduled run, Scheduled run notification, Project |
| `DELETE_SCHEDULED_RUN_NOTIFICATION` | A user deletes a scheduled run's notification | Scheduled run, Scheduled run notification |

### Data connections[​](#data-connections "Direct link to Data connections")

| Event type | Description | Target resource types |
| --- | --- | --- |
| `CREATE_WORKSPACE_DATA_CONNECTION` | An admin creates a data connection for the workspace | Data connection |
| `CREATE_PROJECT_DATA_CONNECTION` | A user creates a data connection inside a project | Data connection, Project |
| `EDIT_DATA_CONNECTION` | A user edits a data connection's settings | Data connection |
| `DELETE_DATA_CONNECTION` | A user deletes a data connection | Data connection |
| `REFRESH_DATA_CONNECTION_SCHEMA` | A user refreshes a data connection's schema | Data connection |
| `UPDATE_DATA_CONNECTION_MAGIC_USAGE` | An admin or manager changes whether a [data connection is used](/docs/explore-data/data-browser#magic-usage) for AI generation | Data connection |
| `IMPORT_DATA_CONNECTION` | A user adds a data connection to a project | Data connection, Project |
| `REMOVE_DATA_CONNECTION_IMPORT` | A user removes a data connection from a project | Data connection, Project |
| `SET_WORKSPACE_DEFAULT_DATA_CONNECTION` | An admin sets or clears the workspace's default data connection | Data connection |
| `APPLY_DATA_ASSET_STATUS` | A user applies a status, such as an endorsement, to a data asset | One of: Data connection, Data source database, Data source schema, Data source table, Semantic dataset, Semantic view |
| `REMOVE_DATA_ASSET_STATUS` | A user removes the status from a data asset | One of: Data connection, Data source database, Data source schema, Data source table, Semantic dataset, Semantic view |

### Semantic models[​](#semantic-models "Direct link to Semantic models")

| Event type | Description | Target resource types |
| --- | --- | --- |
| `CREATE_SEMANTIC_PROJECT` | An admin or manager creates a semantic project | Semantic project |
| `PUBLISH_SEMANTIC_PROJECT` | A user publishes changes to a semantic project from the modeling workbench, Semantic Model Sync, the API, or a committed context changeset | Semantic project |
| `DELETE_SEMANTIC_PROJECT` | A user deletes a semantic project | Semantic project |

### Secrets[​](#secrets "Direct link to Secrets")

| Event type | Description | Target resource types |
| --- | --- | --- |
| `CREATE_WORKSPACE_SECRET` | An admin creates a shared workspace secret | Secret |
| `EDIT_WORKSPACE_SECRET` | An admin edits a shared workspace secret | Secret |
| `DELETE_WORKSPACE_SECRET` | An admin deletes a shared workspace secret | Secret |
| `IMPORT_WORKSPACE_SECRET` | A user adds a shared workspace secret to a project | Secret |
| `UNIMPORT_WORKSPACE_SECRET` | A user removes a shared workspace secret from a project | Secret |
| `CREATE_PROJECT_SECRET` | A user creates a secret in a single project | Secret |
| `EDIT_PROJECT_SECRET` | A user edits a project secret | Secret |
| `DELETE_PROJECT_SECRET` | A user deletes a project secret | Secret |

### Cloud storage integrations[​](#cloud-storage-integrations "Direct link to Cloud storage integrations")

| Event type | Description | Target resource types |
| --- | --- | --- |
| `CREATE_EXTERNAL_FILE_INTEGRATION` | An admin creates a [cloud storage integration](/docs/connect-to-data/cloud-storage-integrations) | External file integration |
| `EDIT_EXTERNAL_FILE_INTEGRATION` | An admin edits a cloud storage integration | External file integration |
| `DELETE_EXTERNAL_FILE_INTEGRATION` | An admin deletes a cloud storage integration | External file integration |
| `LIST_FILES_FROM_EXTERNAL_FILE_INTEGRATION` | Code running in a project lists files from a cloud storage integration | External file integration |
| `DOWNLOAD_FILE_FROM_EXTERNAL_FILE_INTEGRATION` | A user, or code running in a project, downloads a file from a cloud storage integration | External file integration |

### Exports and downloads[​](#exports-and-downloads "Direct link to Exports and downloads")

| Event type | Description | Target resource types |
| --- | --- | --- |
| `EXPORT_AS_PDF` | A user exports a project's app as a PDF | Project, Project version |
| `EXPORT_TO_GOOGLE_SHEETS` | A user exports a cell's output to Google Sheets | Project, Project version, Cell |
| `DOWNLOAD_AS_CSV` | A user downloads a cell's results as a CSV | Cell, Project, Project version |
| `COPY_RESULTS_TO_CLIPBOARD` | A user copies a cell's results to the clipboard | Cell, Project, Project version |
| `DOWNLOAD_CHART_IMAGE` | A user downloads an image of a chart cell in a project | Cell |
| `DOWNLOAD_DATA_APP_CSV` | A user downloads a CSV from a project's data app | Project, Project version |
| `DOWNLOAD_DATA_APP_FILE` | A user downloads a file generated by a project's data app | Project, Project version |
| `READ_CELL_RESULT` | A user or agent reads a cell's latest output from the draft project | Cell |

### Git[​](#git "Direct link to Git")

| Event type | Description | Target resource types |
| --- | --- | --- |
| `CREATE_VCS_CONNECTION` | An admin connects a version control provider, such as GitHub, to the workspace | VCS connection |
| `EDIT_VCS_CONNECTION` | An admin re-authorizes a self-hosted GitHub or GitLab server connection | VCS connection |
| `DELETE_VCS_CONNECTION` | An admin deletes a Git provider connection | VCS connection |
| `CREATE_SYNC_REPOSITORY` | An admin adds a Git sync repository to the workspace | Sync repository, VCS connection |
| `EDIT_SYNC_REPOSITORY` | A user edits a shared Git repository's settings or import access | Sync repository |
| `DELETE_SYNC_REPOSITORY` | A user deletes a Git sync repository | Sync repository |
| `EXPORT_PROJECT_TO_GIT` | A user publishes a Git-synced project, which queues an export to the repository | Sync repository, Project |

### Threads[​](#threads "Direct link to Threads")

| Event type | Description | Target resource types |
| --- | --- | --- |
| `CREATE_THREAD` | A user starts a new Thread | Project |
| `CREATE_PROJECT_FROM_THREAD` | A user turns a Thread into a project | Project |
| `DUPLICATE_THREAD` | A user duplicates a Thread shared with them | Project |
| `DELETE_THREAD` | A user deletes a Thread | Thread |

### Agents and AI features[​](#agents-and-ai-features "Direct link to Agents and AI features")

| Event type | Description | Target resource types |
| --- | --- | --- |
| `CREATE_LOGIC_VIEW_AGENT_CHAT_MESSAGE` | A user sends a message to the Notebook agent | Agent chat message |
| `SEND_LLM_REQUEST` | Hex sends a request to an LLM provider while handling an agent query | Workspace |
| `MAGIC_DESCRIBE_PROJECT` | A user has AI write a project's description | Project version |
| `MAGIC_NAME_PROJECT` | A user has AI name a project | Project version |
| `MAGIC_RENAME_CELL` | A user has AI name a cell | Cell |
| `MAGIC_RENAME_CELL_OUTPUT` | A user has AI name a cell's output | Cell |
| `PUBLISH_GUIDE` | A user publishes a guide when committing a context changeset | Guide |
| `DELETE_GUIDE` | A user publishes a change that deletes a guide | Guide |

### MCP servers[​](#mcp-servers "Direct link to MCP servers")

| Event type | Description | Target resource types |
| --- | --- | --- |
| `CREATE_ORG_MCP_SERVER` | An admin enables an MCP server for the workspace | MCP server configuration |
| `UPDATE_ORG_MCP_SERVER` | An admin updates a workspace MCP server's configuration | MCP server configuration |
| `DELETE_ORG_MCP_SERVER` | An admin removes an MCP server from the workspace | MCP server configuration |
| `CREATE_USER_MCP_CONNECTION` | A user connects to an MCP server | User MCP server connection |
| `UPDATE_USER_MCP_CONNECTION` | A user updates their MCP server connection, such as credentials or tool settings | User MCP server connection |
| `DELETE_USER_MCP_CONNECTION` | A user removes their connection to an MCP server | User MCP server connection |
| `CALL_MCP_SERVER_TOOL` | The Hex agent calls a tool on a user's connected MCP server | User MCP server connection |

### 4.0 projects[​](#40-projects "Direct link to 4.0 projects")

| Event type | Description | Target resource types |
| --- | --- | --- |
| `VIEW_CODE_PROJECT` | A user opens a 4.0 project's editor or published app | Project, Project view |
| `UPLOAD_CODE_PROJECT_FILE` | A user uploads a file to a 4.0 project | Project ref |
| `WRITE_CODE_PROJECT_FILE` | A user or agent writes a file in a 4.0 project | Project ref |
| `EDIT_CODE_PROJECT_FILE` | A user or agent edits a file in a 4.0 project | Project ref |
| `TRASH_CODE_PROJECT_FILE` | A user or agent deletes a file in a 4.0 project | Project ref |
| `RELOAD_CODE_PROJECT` | A user or agent reloads a 4.0 project's saved source files | Project ref |
| `SCAFFOLD_CODE_PROJECT_APP` | A user or agent scaffolds an app layout in a 4.0 project | Project ref |
| `ADD_CODE_PROJECT_COMPONENT` | A user or agent adds a catalog component to a 4.0 project app | Project ref |
| `CREATE_CODE_PROJECT_CHART` | A user or agent adds a chart to a 4.0 project | Project ref |
| `CREATE_CODE_PROJECT_DISPLAY_TABLE` | A user or agent adds a display table to a 4.0 project | Project ref |
| `CREATE_CODE_PROJECT_INPUT` | A user or agent adds an input to a 4.0 project | Project ref |
| `CREATE_CODE_PROJECT_KPI_CARD` | A user or agent adds a KPI card to a 4.0 project | Project ref |
| `LINK_CODE_PROJECT_DATA_CONNECTION` | A user or agent links a data connection to a 4.0 project | Project ref, Data connection |
| `BUILD_CODE_PROJECT_APP` | A user or agent builds a preview of a 4.0 project app | Project ref |
| `PUBLISH_CODE_PROJECT` | A user or agent publishes a 4.0 project app | Project ref |
| `DOWNLOAD_CODE_PROJECT_SCREENSHOT` | A user or agent takes a screenshot of a 4.0 project's draft preview | Project ref |
| `DOWNLOAD_CODE_APP_SCREENSHOT` | A user or agent takes a screenshot of a published 4.0 project app | Project |

### Tasks[​](#tasks "Direct link to Tasks")

| Event type | Description | Target resource types |
| --- | --- | --- |
| `CREATE_TASK` | A user creates a scheduled agent task, or publishes a draft task | Task |
| `EDIT_TASK` | A user edits a task | Task |
| `PAUSE_TASK` | A user pauses a task | Task |
| `RESUME_TASK` | A user resumes a paused task | Task |
| `DELETE_TASK` | A user deletes a scheduled agent task | Task |

#### On this page

* [Audit log event schema](#audit-log-event-schema)
* [Audit log target resource types](#audit-log-target-resource-types)
* [Audit log event types](#audit-log-event-types)
  + [Sign-in](#sign-in)
  + [Users](#users)
  + [Groups](#groups)
  + [User attributes](#user-attributes)
  + [Directory sync](#directory-sync)
  + [API tokens](#api-tokens)
  + [Workspace settings](#workspace-settings)
  + [AI settings and credits](#ai-settings-and-credits)
  + [Projects](#projects)
  + [Explores](#explores)
  + [Sharing and access](#sharing-and-access)
  + [Folders](#folders)
  + [Collections](#collections)
  + [Scheduled runs](#scheduled-runs)
  + [Data connections](#data-connections)
  + [Semantic models](#semantic-models)
  + [Secrets](#secrets)
  + [Cloud storage integrations](#cloud-storage-integrations)
  + [Exports and downloads](#exports-and-downloads)
  + [Git](#git)
  + [Threads](#threads)
  + [Agents and AI features](#agents-and-ai-features)
  + [MCP servers](#mcp-servers)
  + [4.0 projects](#40-projects)
  + [Tasks](#tasks)