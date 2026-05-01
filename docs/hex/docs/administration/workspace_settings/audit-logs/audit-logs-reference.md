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
      "email": "[email protected]",  
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
| Cell | A [cell](/docs/explore-data/cells/sql-cells/sql-cells-introduction) in a Hex project |
| Collection | A [collection](/docs/organize-content/collections) of Hex projects and components |
| Data connection | A [connection](/docs/connect-to-data/data-connections/data-connections-introduction) to an external data warehouse |
| Domain | A domain allowed to be associated with your Hex workspace |
| External file integration | An [integration](/docs/connect-to-data/cloud-storage-integrations) with a cloud storage provider like AWS S3 or Google Drive |
| File | A [file](/docs/connect-to-data/upload-files) uploaded to a Hex project |
| Group | A group of Hex users that can be granted access to resources |
| Magic Api Key | An [API key](/docs/trust/ai-data-privacy#bring-your-own-key-byok) for authenticating magic requests |
| Project | A Hex [project](/docs/explore-data/projects/projects-introduction), [component](/docs/explore-data/components), or [explore](/docs/share-insights/explore) object |
| Project grant | A role (viewer, editor, etc.) given to a user or group for [access to a Hex project](/docs/collaborate/sharing-and-permissions/project-sharing) |
| Project version | A specific [version](/docs/explore-data/projects/history-and-versions) of a Hex project |
| Project view | An object that represents an instance of a user viewing a project |
| Scheduled run | A cron-like [schedule](/docs/share-insights/scheduled-runs) on which a project is run periodically |
| Scheduled run notification | A [notification](/docs/share-insights/scheduled-runs#send-notifications) configured on a scheduled run, to send emails and/or Slack messages when a scheduled run completes or fails |
| Semantic project | A [semantic project](/docs/connect-to-data/semantic-models/intro-to-semantic-models) containing shared definitions for data models |
| Secret | A [secret value](/docs/explore-data/projects/environment-configuration/environment-views#secrets) containing sensitive information that can be referenced in Hex projects |
| Template | A Hex-provided project template |
| User | A Hex user (could be email user, API user, etc.) |
| Workspace | A representation of your Hex workspace |

Some event types include target resources with a type of **principal**. This indicates that this object can be one of multiple types.
For instance, the UPDATE\_PROJECT\_ACCESS event type includes a principal resource which is either a Group or a User.

## Audit log event types[​](#audit-log-event-types "Direct link to Audit log event types")

| Event type | Description | Target resource types |
| --- | --- | --- |
| CREATE\_PROJECT |  | * Project |
| CREATE\_PROJECT\_FROM\_TEMPLATE | Create a project from a [template](https://hex.tech/use-cases/) | * Project * Template |
| DUPLICATE\_PROJECT |  | * Project |
| COPY\_PROJECT\_FROM\_EXTERNAL\_WORKSPACE | Create a project by copying one from a different workspace | * Project |
| IMPORT\_PROJECT | [Import a project](/docs/explore-data/projects/import-export#import-projects) from a project yaml file | * Project |
| CREATE\_EXPLORE\_FROM\_PROJECT\_CELL | Create an "[explore from app](/docs/share-insights/explore)" from a project cell | * Project |
| CREATE\_EXPLORE | Create an Explore | * Project * Cell |
| CONVERT\_EXPLORE\_TO\_PROJECT | Create a project from data created while exploring from an app | * Project |
| VIEW\_PROJECT |  | * Project * Project version * Project view |
| RUN\_PROJECT | Run a project top to bottom | * Project * Project version |
| RUN\_CELL | Run a single cell within a project | * Project * Project version * Cell |
| UPLOAD\_FILE\_TO\_PROJECT |  | * Project * File |
| DOWNLOAD\_FILE\_FROM\_PROJECT |  | * Project * File |
| PUBLISH\_PROJECT |  | * Project |
| DELETE\_PROJECT | Move project to trash | * Project |
| PERMANENTLY\_DELETE\_PROJECT |  | * Project |
| REQUEST\_PROJECT\_ROLE | A user request for an access role to a project | * Project * User |
| GRANT\_USERS\_PROJECT\_ACCESS | Grant a set of users an access role to a project | * Project * User * Project grant |
| GRANT\_GROUPS\_PROJECT\_ACCESS | Grant a set of groups an access role to a project | * Project * Group * Project grant |
| GRANT\_ADMIN\_PROJECT\_ACCESS | Same as `GRANT_USERS_PROJECT_ACCESS`, but only for admins | * Project * User * Project grant |
| UPDATE\_ALLOW\_EMBEDDING | Enable signed embedding for the project | * Project |
| UPDATE\_PROJECT\_ACCESS | Update the access role to a project for a set of users and/or groups | * Project * Principal * Project grant  Principal here refers to either a Group or a User |
| REMOVE\_PROJECT\_ACCESS | Remove a user or group's access to a project | * Project * Principal |
| SHARE\_PROJECT\_WITH\_SUPPORT |  | * Project |
| SHARE\_PROJECT\_WITH\_ORG |  | * Project |
| SHARE\_PROJECT\_WITH\_PUBLIC |  | * Project |
| UPDATE\_PROJECT\_PUBLIC\_DUPLICATION\_ALLOWED | Change whether or not a project can be duplicated by users in another workspace | * Project |
| CREATE\_SCHEDULED\_RUN |  | * Project * Scheduled run |
| EDIT\_SCHEDULED\_RUN |  | * Project * Scheduled run |
| DELETE\_SCHEDULED\_RUN |  | * Project * Scheduled run |
| CREATE\_COLLECTION |  | * Collection |
| EDIT\_COLLECTION |  | * Collection |
| ADD\_PROJECTS\_TO\_COLLECTION | Add a set of projects to a collection | * Collection * Project |
| UPDATE\_COLLECTION\_ROLE\_IN\_PROJECT | Update the access role that a collection has for a project | * Collection * Project |
| CREATE\_WORKSPACE\_DATA\_CONNECTION | Create a data connection usable across the workspace | * Data connection |
| CREATE\_PROJECT\_DATA\_CONNECTION | Create a data connection within a project | * Data connection * Project |
| EDIT\_DATA\_CONNECTION |  | * Data connection |
| REFRESH\_DATA\_CONNECTION\_SCHEMA | Trigger a refresh of the data schema for a data connection | * Data connection |
| UPDATE\_DATA\_CONNECTION\_MAGIC\_USAGE | Update whether or not a [data connection should be used](/docs/explore-data/data-browser#magic-usage) for Magic generation | * Data connection |
| IMPORT\_DATA\_CONNECTION | Import a data connection in a project | * Data connection * Project |
| REMOVE\_DATA\_CONNECTION\_IMPORT | Remove a data connection from a project | * Data connection * Project |
| DELETE\_DATA\_CONNECTION |  | * Data connection |
| SET\_WORKSPACE\_DEFAULT\_DATA\_CONNECTION | Set a data connection as the default for the workspace | * Data connection |
| CREATE\_SEMANTIC\_PROJECT |  | * Semantic project |
| PUBLISH\_SEMANTIC\_PROJECT | Publish changes to a semantic project from the modeling workbench or via Semantic Model Sync | * Semantic project |
| DELETE\_SEMANTIC\_PROJECT |  | * Semantic project |
| CREATE\_USERS |  | * User |
| CREATE\_PASSWORD\_USER | Create a user who is allowed to login using a password | * User |
| INVITE\_USERS | Invite users to join the workspace by email | * Workspace |
| INVITE\_USER\_AS\_ADMIN | Invite a user to join the workspace as an admin | * Workspace |
| ACTIVATE\_USER |  | * User |
| DEACTIVATE\_USER |  | * User |
| EDIT\_USER | Update user metadata (excluding their workspace role) | * User |
| UPDATE\_USER\_ROLE | Update a user's workspace role | * User |
| REQUEST\_ORG\_ROLE | A user's request for a specific role in the workspace | * User |
| GRANT\_USER\_API\_ACCESS | Allow a user to generate API tokens and use them in requests | * User |
| REVOKE\_USER\_API\_ACCESS | Prevent user from creating API tokens and reject requests containing tokens attributed to this user | * User |
| CREATE\_GROUP |  | * Group |
| UPDATE\_GROUP | Update metadata about a group (not its users) | * Group |
| UPDATE\_GROUP\_MEMBERS | Add or remove users from a group | * User * Group |
| DELETE\_GROUP |  | * Group |
| CREATE\_EXTERNAL\_FILE\_INTEGRATION |  | * External file integration |
| EDIT\_EXTERNAL\_FILE\_INTEGRATION |  | * External file integration |
| DELETE\_EXTERNAL\_FILE\_INTEGRATION |  | * External file integration |
| DOWNLOAD\_FILE\_FROM\_EXTERNAL\_FILE\_INTEGRATION |  | * External file integration |
| ADD\_WORKSPACE\_DOMAIN | Add an [allowed domain](/docs/administration/workspace_settings/overview#allowed-domains) to workspace | * Domain |
| DELETE\_WORKSPACE\_DOMAIN |  | * Domain |
| UPDATE\_SSO\_CONFIGURATION | [Configure SSO](/docs/administration/workspace_settings/workspace-security#sso-configuration) auth for the workspace | * Workspace |
| UPDATE\_PUBLIC\_SHARING\_SETTING | Update whether or not projects in the workspace can be shared publicly | * Workspace |
| UPDATE\_API\_TOKEN\_EXPIRATION\_POLICY | Configure [expiration policy](/docs/api-integrations/api/overview#token-expiration) for API tokens | * Workspace |
| UPDATE\_ALLOW\_NOTION\_PREVIEW |  | * Workspace |
| UPDATE\_ALLOW\_CSV\_DOWNLOADS |  | * Workspace |
| UPDATE\_ALLOW\_FILE\_UPLOADS |  | * Workspace |
| SET\_DIRECTORY\_SYNC\_ADMIN\_GROUP | Set a group of users from Directory Sync to be workspace admins | * Workspace |
| SET\_DIRECTORY\_SYNC\_AUTHOR\_GROUP | Set a group of users from Directory Sync to be workspace editors | * Workspace |
| SET\_DATA\_RETENTION\_CELL\_OUTPUTS | Set the data retention period for cell outputs | * Workspace |
| SET\_DATA\_RETENTION\_QUERY\_CACHE | Set the data retention period for query cache entries | * Workspace |
| CREATE\_WORKSPACE\_SECRET | Create a shared workspace secret | * Secret |
| EDIT\_WORKSPACE\_SECRET | Modify properties of a shared workspace secret | * Secret |
| DELETE\_WORKSPACE\_SECRET |  | * Secret |
| IMPORT\_WORKSPACE\_SECRET | Import a shared workspace secret into a project | * Secret |
| UNIMPORT\_WORKSPACE\_SECRET | Unimport a shared workspace secret from a project | * Secret |
| CREATE\_PROJECT\_SECRET | Create a secret usable within a single project | * Secret |
| EDIT\_PROJECT\_SECRET | Modify properties of a project-scoped secret | * Secret |
| DELETE\_PROJECT\_SECRET |  | * Secret |
| CREATE\_SCHEDULED\_RUN\_NOTIFICATION | Create a new notification for a scheduled run | * Scheduled Run * Scheduled Run Notification * Project |
| EDIT\_SCHEDULED\_RUN\_NOTIFICATION | Edit an existing notification for a scheduled run | * Scheduled Run * Scheduled Run Notification * Project |
| DELETE\_SCHEDULED\_RUN\_NOTIFICATION | Delete an existing notification for a scheduled run | * Scheduled Run * Scheduled Run Notification |
| CREATE\_MAGIC\_API\_KEY |  | * Magic API Key |
| DELETE\_MAGIC\_API\_KEY |  | * Magic API Key |
| EXPORT\_AS\_PDF | Export a published app as PDF | * Project * Project version |
| DOWNLOAD\_AS\_CSV | Download outputs from a cell to CSV | * Cell * Project * Project version |
| UPDATE\_NOTEBOOK\_CHAT\_ALPHA\_FEATURE\_SETTING | Show whether the [Notebook Agent](/docs/explore-data/notebook-view/notebook-agent)'s Alpha features are toggled on or off | * User |
| CREATE\_LOGIC\_VIEW\_AGENT\_CHAT\_MESSAGE | Show when a message gets sent to the Notebook agent | * Agent Chat Message |
| MAGIC\_EDIT\_CELL | Notebook agent is used to edit the contents of an existing cell (e.g., modifying code in a SQL or Python cell) | * Magic Event |
| MAGIC\_DESCRIBE\_PROJECT | Notebook agent is used to generate a project's description | * Magic Event |
| MAGIC\_NAME\_PROJECT | Notebook agent names a project | * Magic Event |
| MAGIC\_RENAME\_CELL | Notebook agent renames a cell | * Magic Event |
| MAGIC\_RENAME\_CELL\_OUTPUT | Notebook agent renames the output of a cell | * Magic Event |
| CREATE\_THREAD | A user creates a new Thread | * Project |
| CREATE\_PROJECT\_FROM\_THREAD | A user creates a project initiated from a Thread | * Project |
| DUPLICATE\_THREAD | A user duplicates a Thread that was shared with them | * Project |
| CREATE\_CHAT\_WITH\_APP\_AGENT\_CHAT\_MESSAGE | A user creates a new Chat with App thread | * Project |

#### On this page

* [Audit log event schema](#audit-log-event-schema)
* [Audit log target resource types](#audit-log-target-resource-types)
* [Audit log event types](#audit-log-event-types)