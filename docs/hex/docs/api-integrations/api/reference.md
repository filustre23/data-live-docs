* postCreatePresignedUrl
* getListProjects
* postCreateProject
* getGetQueriedTables
* patchEditProjectSharingCollections
* patchEditProjectSharingOrgAndPublic
* patchEditProjectSharingGroups
* postIngestSemanticProject
* patchUpdateSemanticProject
* delCancelRun
* getGetRunStatus
* getGetGroup
* delDeleteGroup
* patchEditGroup
* getListGroups
* postCreateGroup
* postCreateDataConnection
* getListDataConnections
* patchEditDataConnection
* getGetDataConnection
* patchUpdateDataConnectionSchema
* putUpsertGuideDraft
* postPublishGuideDrafts
* delDeleteGuideDraft
* getGetCollection
* patchEditCollection
* getListCollections
* postCreateCollection
* getGetCell
* patchUpdateCell
* delDeleteCell
* getGetCellOutput
* postCreateCell
* getListCells
* getGetChartImageFromLogic
* patchEditProjectSharingUsers
* postExportProject
* getGetChartImageFromRun
* getGetProject
* patchUpdateProject
* getGetProjectRuns
* postRunProject
* postCreateThread
* getListThreads
* getGetThread
* getGetThreadMessages
* postContinueThread
* getMe
* getListUsers
* postDeactivateUser
* getListTopics
* getListDraftGuides

[API docs by Redocly](https://redocly.com/redoc/)

# Hex API (1.0.0)

Download OpenAPI specification:[Download](https://static.hex.site/openapi.json)

License: UNLICENSED

API specification for the Hex External API

## CreatePresignedUrl

Create an embedded url for a project

##### Authorizations:

*bearerAuth*

##### path Parameters

|  |  |
| --- | --- |
| projectId required | string <uuid>  (ProjectId) ^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}...Show pattern  Unique ID for a Hex project. This can be found in the Variables side bar of the Logic View of a project, or by visiting the Project, and copying the UUID after `hex` in the URL. |

##### Request Body schema: application/json required

|  |  |
| --- | --- |
| hexUserAttributes | object  A map of attributes meant to populate hex\_user\_attributes in the app for the running user. This must be a string to string map. For more complexity, you can do json serialization |
| scope | Array of strings  Optionally include additional permissions for a user to do in an embedded app. Valid scopes include:  EXPORT\_PDF: allow users to download the app as a pdf EXPORT\_CSV: allow users to download CSVs from tables |
| inputParameters | object  Optionall sets default values for input states. The keys are the names of the inputs and the values are the default values for those inputs. |
| expiresIn | number <double>  Default:  "15000"  Optionally specify the expiration time of the embedding url in milliseconds. This represents the maximum allowed time between receiving the API response with the single-use signed URL, and requesting the signed URL for the iframe. Default is 15 seconds. Maximum value is 300 seconds (5 minutes). |
| displayOptions | object  Optionally customize the display of the embedded app |
| testMode | boolean  Run the embed API call in test mode. Does not run the app and will not count towards rate limits or embedding usage counts. |
| property name\* additional property | any |

### Responses

**200**

**400**

**403**

**422**

post/v1/embedding/createPresignedUrl/{projectId}

https://app.hex.tech/api/v1/embedding/createPresignedUrl/{projectId}

### Request samples

* Payload

Content type

application/json

Copy

 Expand all  Collapse all

`{

* "hexUserAttributes": {
  + "orgId": "my-org-id",
  + "groupId": "my-group-id"},
* "scope": [
  + "string"],
* "inputParameters": {
  + "property1": null,
  + "property2": null},
* "expiresIn": "15000",
* "displayOptions": {
  + "theme": "light",
  + "showEmbeddedRunButton": true,
  + "noEmbedHeaderPadding": true,
  + "noEmbedBasePadding": true,
  + "noEmbedOutline": true,
  + "noEmbedFooter": true,
  + "property1": null,
  + "property2": null},
* "testMode": true,
* "property1": null,
* "property2": null

}`

### Response samples

* 200
* 400
* 403
* 422

Content type

application/json

Copy

`{

* "url": "string"

}`

## ListProjects

List all viewable projects, sorted by most recently created first.

##### Authorizations:

*bearerAuth*

##### query Parameters

|  |  |
| --- | --- |
| includeArchived | boolean  Default:  false |
| includeComponents | boolean  Default:  false |
| includeTrashed | boolean  Default:  false |
| includeSharing | boolean  Default:  false |
| statuses | Array of strings  Default:  "" |
| categories | Array of strings  Default:  "" |
| creatorEmail | string  Default:  null |
| ownerEmail | string  Default:  null |
| collectionId | string  Default:  null |
| limit | integer <int32>  (PageSize)   [ 1 .. 100 ]  Default:  "25"  Number of results to fetch per page for paginated requests |
| after | any  Default:  null |
| before | any  Default:  null |
| sortBy | string (SortByEnum)  Enum: "CREATED\_AT" "LAST\_EDITED\_AT" "LAST\_PUBLISHED\_AT" |
| sortDirection | string (SortDirectionEnum)  Enum: "DESC" "ASC" |

### Responses

**200**

**400**

**403**

get/v1/projects

https://app.hex.tech/api/v1/projects

### Response samples

* 200
* 400
* 403

Content type

application/json

Copy

 Expand all  Collapse all

`{

* "values": [
  + {
    - "id": "497f6eca-6276-4993-bfeb-53cbbbba6f08",
    - "title": "string",
    - "description": "string",
    - "type": "PROJECT",
    - "creator": {
      * "email": "string"},
    - "owner": {
      * "email": "string"},
    - "status": {
      * "name": "string"},
    - "categories": [
      * {
        + "description": "string",
        + "name": "string"}],
    - "reviews": {
      * "required": true},
    - "analytics": {
      * "publishedResultsUpdatedAt": "string",
      * "lastViewedAt": "string",
      * "appViews": {
        + "lastThirtyDays": 0,
        + "lastFourteenDays": 0,
        + "lastSevenDays": 0,
        + "allTime": 0}},
    - "lastEditedAt": "string",
    - "lastPublishedAt": "string",
    - "createdAt": "string",
    - "archivedAt": "string",
    - "trashedAt": "string",
    - "schedules": [
      * {
        + "cadence": "HOURLY",
        + "enabled": true,
        + "hourly": {
          - "timezone": "string",
          - "minute": 59},
        + "daily": {
          - "timezone": "string",
          - "minute": 59,
          - "hour": 23},
        + "weekly": {
          - "timezone": "string",
          - "minute": 59,
          - "hour": 23,
          - "dayOfWeek": "SUNDAY"},
        + "monthly": {
          - "timezone": "string",
          - "minute": 59,
          - "hour": 23,
          - "day": 1},
        + "custom": {
          - "timezone": "string",
          - "cron": "string"}}],
    - "sharing": {
      * "users": [
        + {
          - "access": "NONE",
          - "user": {
            * "email": "string"}}],
      * "collections": [
        + {
          - "access": "NONE",
          - "collection": {
            * "name": "string"}}],
      * "groups": [
        + {
          - "access": "NONE",
          - "group": {
            * "name": "string"}}],
      * "workspace": {
        + "access": "NONE"},
      * "publicWeb": {
        + "access": "NONE"},
      * "support": {
        + "access": "NONE"}}}],
* "pagination": {
  + "after": "string",
  + "before": "string"}

}`

## CreateProject

Create a new project in the workspace with the specified title, and optionally a description.

This endpoint is subject to the following rate limits:

* `hex-api`: Default rate limit group for the Hex API
  + Max requests per minute may vary (default: 30)
  + Max requests per hour may vary (default: 1800)

##### Authorizations:

*bearerAuth*

##### Request Body schema: application/json required

|  |  |
| --- | --- |
| title required | string  The title of the new project. |
| description | string  An optional description for the new project. |

### Responses

**201** 

Successful response

**400** 

Invalid input data

**403** 

Insufficient access

post/v1/projects

https://app.hex.tech/api/v1/projects

### Request samples

* Payload

Content type

application/json

Copy

`{

* "title": "string",
* "description": "string"

}`

### Response samples

* 201
* 400
* 403

Content type

application/json

Copy

 Expand all  Collapse all

`{

* "id": "string",
* "title": "string",
* "description": "string",
* "type": "PROJECT",
* "creator": {
  + "email": "string"},
* "owner": {
  + "email": "string"},
* "status": {
  + "name": "string"},
* "categories": [
  + {
    - "name": "string",
    - "description": "string"}],
* "reviews": {
  + "required": true},
* "analytics": {
  + "appViews": {
    - "allTime": 0,
    - "lastSevenDays": 0,
    - "lastFourteenDays": 0,
    - "lastThirtyDays": 0},
  + "lastViewedAt": "string",
  + "publishedResultsUpdatedAt": "string"},
* "lastEditedAt": "string",
* "lastPublishedAt": "string",
* "createdAt": "string",
* "archivedAt": "string",
* "trashedAt": "string",
* "schedules": [
  + {
    - "cadence": "HOURLY",
    - "enabled": true,
    - "hourly": {
      * "minute": 0,
      * "timezone": "string"},
    - "daily": {
      * "hour": 0,
      * "minute": 0,
      * "timezone": "string"},
    - "weekly": {
      * "dayOfWeek": "SUNDAY",
      * "hour": 0,
      * "minute": 0,
      * "timezone": "string"},
    - "monthly": {
      * "day": 0,
      * "hour": 0,
      * "minute": 0,
      * "timezone": "string"},
    - "custom": {
      * "cron": "string",
      * "timezone": "string"}}],
* "sharing": {
  + "users": [
    - {
      * "user": {
        + "email": "string"},
      * "access": "NONE"}],
  + "collections": [
    - {
      * "collection": {
        + "name": "string"},
      * "access": "NONE"}],
  + "groups": [
    - {
      * "group": {
        + "name": "string"},
      * "access": "NONE"}],
  + "workspace": {
    - "access": "NONE"},
  + "publicWeb": {
    - "access": "NONE"},
  + "support": {
    - "access": "NONE"}}

}`

## GetQueriedTables

Given a project ID, return the list of warehouse tables queried in the project.

##### Authorizations:

*bearerAuth*

##### path Parameters

|  |  |
| --- | --- |
| projectId required | string <uuid>  (ProjectId) ^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}...Show pattern  Unique ID for a Hex project. This can be found in the Variables side bar of the Logic View of a project, or by visiting the Project, and copying the UUID after `hex` in the URL. |

##### query Parameters

|  |  |
| --- | --- |
| limit | integer <int32>  (PageSize)   [ 1 .. 100 ]  Default:  "25"  Number of results to fetch per page for paginated requests |
| after | any  Default:  null |
| before | any  Default:  null |

### Responses

**200**

**400**

**403**

**404**

**422**

**500**

get/v1/projects/{projectId}/queriedTables

https://app.hex.tech/api/v1/projects/{projectId}/queriedTables

### Response samples

* 200
* 400
* 403
* 404
* 422
* 500

Content type

application/json

Copy

 Expand all  Collapse all

`{

* "values": [
  + {
    - "dataConnectionId": "2e0fe5a4-5860-44c6-b0fa-f448a08c1b28",
    - "dataConnectionName": "string",
    - "tableName": "string"}],
* "pagination": {
  + "after": "string",
  + "before": "string"},
* "traceId": "string"

}`

## EditProjectSharingCollections

Add a project to collections or remove it from collections.
For projects, use `CAN_VIEW` to grant the UI permission labeled "Can explore".
Use `APP_ONLY` to grant the UI permission labeled "Can view app".
Workspace tokens calling this endpoint need to have "Collections -> Write access" scope
in addition to "Projects -> Write access" scope.

##### Authorizations:

*bearerAuth*

##### path Parameters

|  |  |
| --- | --- |
| projectId required | string <uuid>  (ProjectId) ^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}...Show pattern  Unique ID for a Hex project. This can be found in the Variables side bar of the Logic View of a project, or by visiting the Project, and copying the UUID after `hex` in the URL. |

##### Request Body schema: application/json required

|  |  |
| --- | --- |
| sharing required | object |
| |  |  | | --- | --- | | upsert required | object | | |  |  | | --- | --- | | collections required | Array of objects  <= 25 items | | Array (<= 25 items)  |  |  | | --- | --- | | access required | string (AccessLevelEnum)  Enum: "NONE" "APP\_ONLY" "CAN\_VIEW" "CAN\_EDIT" "FULL\_ACCESS" | | collection required | object | | | | | | |

### Responses

**200**

**400**

**403**

**404**

**500**

patch/v1/projects/{projectId}/sharing/collections

https://app.hex.tech/api/v1/projects/{projectId}/sharing/collections

### Request samples

* Payload

Content type

application/json

Copy

 Expand all  Collapse all

`{

* "sharing": {
  + "upsert": {
    - "collections": [
      * {
        + "access": "NONE",
        + "collection": {
          - "id": "497f6eca-6276-4993-bfeb-53cbbbba6f08"}}]}}

}`

### Response samples

* 200
* 400
* 403
* 404
* 500

Content type

application/json

Copy

 Expand all  Collapse all

`{

* "project": {
  + "id": "497f6eca-6276-4993-bfeb-53cbbbba6f08",
  + "title": "string",
  + "description": "string",
  + "type": "PROJECT",
  + "creator": {
    - "email": "string"},
  + "owner": {
    - "email": "string"},
  + "status": {
    - "name": "string"},
  + "categories": [
    - {
      * "description": "string",
      * "name": "string"}],
  + "reviews": {
    - "required": true},
  + "analytics": {
    - "publishedResultsUpdatedAt": "string",
    - "lastViewedAt": "string",
    - "appViews": {
      * "lastThirtyDays": 0,
      * "lastFourteenDays": 0,
      * "lastSevenDays": 0,
      * "allTime": 0}},
  + "lastEditedAt": "string",
  + "lastPublishedAt": "string",
  + "createdAt": "string",
  + "archivedAt": "string",
  + "trashedAt": "string",
  + "schedules": [
    - {
      * "cadence": "HOURLY",
      * "enabled": true,
      * "hourly": {
        + "timezone": "string",
        + "minute": 59},
      * "daily": {
        + "timezone": "string",
        + "minute": 59,
        + "hour": 23},
      * "weekly": {
        + "timezone": "string",
        + "minute": 59,
        + "hour": 23,
        + "dayOfWeek": "SUNDAY"},
      * "monthly": {
        + "timezone": "string",
        + "minute": 59,
        + "hour": 23,
        + "day": 1},
      * "custom": {
        + "timezone": "string",
        + "cron": "string"}}],
  + "sharing": {
    - "users": [
      * {
        + "access": "NONE",
        + "user": {
          - "email": "string"}}],
    - "collections": [
      * {
        + "access": "NONE",
        + "collection": {
          - "name": "string"}}],
    - "groups": [
      * {
        + "access": "NONE",
        + "group": {
          - "name": "string"}}],
    - "workspace": {
      * "access": "NONE"},
    - "publicWeb": {
      * "access": "NONE"},
    - "support": {
      * "access": "NONE"}}},
* "errors": [
  + {
    - "collectionIds": [
      * "497f6eca-6276-4993-bfeb-53cbbbba6f08"],
    - "reason": "string"}]

}`

## EditProjectSharingOrgAndPublic

Update workspace or public-web sharing for a project.
For projects, use `CAN_VIEW` to grant the UI permission labeled "Can explore".
Use `APP_ONLY` to grant the UI permission labeled "Can view app".

##### Authorizations:

*bearerAuth*

##### path Parameters

|  |  |
| --- | --- |
| projectId required | string <uuid>  (ProjectId) ^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}...Show pattern  Unique ID for a Hex project. This can be found in the Variables side bar of the Logic View of a project, or by visiting the Project, and copying the UUID after `hex` in the URL. |

##### Request Body schema: application/json required

|  |  |
| --- | --- |
| sharing required | object |
| |  |  | | --- | --- | | publicWeb | string (PublicWebAccessLevel)  Enum: "NONE" "APP\_ONLY" "CAN\_VIEW" "CAN\_EDIT" "FULL\_ACCESS" | | workspace | string (AccessLevelEnum)  Enum: "NONE" "APP\_ONLY" "CAN\_VIEW" "CAN\_EDIT" "FULL\_ACCESS" | | |

### Responses

**200**

**400**

**403**

**404**

**500**

patch/v1/projects/{projectId}/sharing/workspaceAndPublic

https://app.hex.tech/api/v1/projects/{projectId}/sharing/workspaceAndPublic

### Request samples

* Payload

Content type

application/json

Copy

 Expand all  Collapse all

`{

* "sharing": {
  + "publicWeb": "NONE",
  + "workspace": "NONE"}

}`

### Response samples

* 200
* 400
* 403
* 404
* 500

Content type

application/json

Copy

 Expand all  Collapse all

`{

* "project": {
  + "id": "497f6eca-6276-4993-bfeb-53cbbbba6f08",
  + "title": "string",
  + "description": "string",
  + "type": "PROJECT",
  + "creator": {
    - "email": "string"},
  + "owner": {
    - "email": "string"},
  + "status": {
    - "name": "string"},
  + "categories": [
    - {
      * "description": "string",
      * "name": "string"}],
  + "reviews": {
    - "required": true},
  + "analytics": {
    - "publishedResultsUpdatedAt": "string",
    - "lastViewedAt": "string",
    - "appViews": {
      * "lastThirtyDays": 0,
      * "lastFourteenDays": 0,
      * "lastSevenDays": 0,
      * "allTime": 0}},
  + "lastEditedAt": "string",
  + "lastPublishedAt": "string",
  + "createdAt": "string",
  + "archivedAt": "string",
  + "trashedAt": "string",
  + "schedules": [
    - {
      * "cadence": "HOURLY",
      * "enabled": true,
      * "hourly": {
        + "timezone": "string",
        + "minute": 59},
      * "daily": {
        + "timezone": "string",
        + "minute": 59,
        + "hour": 23},
      * "weekly": {
        + "timezone": "string",
        + "minute": 59,
        + "hour": 23,
        + "dayOfWeek": "SUNDAY"},
      * "monthly": {
        + "timezone": "string",
        + "minute": 59,
        + "hour": 23,
        + "day": 1},
      * "custom": {
        + "timezone": "string",
        + "cron": "string"}}],
  + "sharing": {
    - "users": [
      * {
        + "access": "NONE",
        + "user": {
          - "email": "string"}}],
    - "collections": [
      * {
        + "access": "NONE",
        + "collection": {
          - "name": "string"}}],
    - "groups": [
      * {
        + "access": "NONE",
        + "group": {
          - "name": "string"}}],
    - "workspace": {
      * "access": "NONE"},
    - "publicWeb": {
      * "access": "NONE"},
    - "support": {
      * "access": "NONE"}}},
* "errors": [
  + {
    - "type": "workspace",
    - "reason": "string"}]

}`

## EditProjectSharingGroups

Add groups to a project or update/remove their project sharing access.
For projects, use `CAN_VIEW` to grant the UI permission labeled "Can explore".
Use `APP_ONLY` to grant the UI permission labeled "Can view app".

##### Authorizations:

*bearerAuth*

##### path Parameters

|  |  |
| --- | --- |
| projectId required | string <uuid>  (ProjectId) ^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}...Show pattern  Unique ID for a Hex project. This can be found in the Variables side bar of the Logic View of a project, or by visiting the Project, and copying the UUID after `hex` in the URL. |

##### Request Body schema: application/json required

|  |  |
| --- | --- |
| sharing required | object |
| |  |  | | --- | --- | | upsert required | object | | |  |  | | --- | --- | | groups required | Array of objects  <= 25 items | | Array (<= 25 items)  |  |  | | --- | --- | | access required | string (AccessLevelEnum)  Enum: "NONE" "APP\_ONLY" "CAN\_VIEW" "CAN\_EDIT" "FULL\_ACCESS" | | group required | object | | | | | | |

### Responses

**200**

**400**

**403**

**404**

**500**

patch/v1/projects/{projectId}/sharing/groups

https://app.hex.tech/api/v1/projects/{projectId}/sharing/groups

### Request samples

* Payload

Content type

application/json

Copy

 Expand all  Collapse all

`{

* "sharing": {
  + "upsert": {
    - "groups": [
      * {
        + "access": "NONE",
        + "group": {
          - "id": "497f6eca-6276-4993-bfeb-53cbbbba6f08"}}]}}

}`

### Response samples

* 200
* 400
* 403
* 404
* 500

Content type

application/json

Copy

 Expand all  Collapse all

`{

* "project": {
  + "id": "497f6eca-6276-4993-bfeb-53cbbbba6f08",
  + "title": "string",
  + "description": "string",
  + "type": "PROJECT",
  + "creator": {
    - "email": "string"},
  + "owner": {
    - "email": "string"},
  + "status": {
    - "name": "string"},
  + "categories": [
    - {
      * "description": "string",
      * "name": "string"}],
  + "reviews": {
    - "required": true},
  + "analytics": {
    - "publishedResultsUpdatedAt": "string",
    - "lastViewedAt": "string",
    - "appViews": {
      * "lastThirtyDays": 0,
      * "lastFourteenDays": 0,
      * "lastSevenDays": 0,
      * "allTime": 0}},
  + "lastEditedAt": "string",
  + "lastPublishedAt": "string",
  + "createdAt": "string",
  + "archivedAt": "string",
  + "trashedAt": "string",
  + "schedules": [
    - {
      * "cadence": "HOURLY",
      * "enabled": true,
      * "hourly": {
        + "timezone": "string",
        + "minute": 59},
      * "daily": {
        + "timezone": "string",
        + "minute": 59,
        + "hour": 23},
      * "weekly": {
        + "timezone": "string",
        + "minute": 59,
        + "hour": 23,
        + "dayOfWeek": "SUNDAY"},
      * "monthly": {
        + "timezone": "string",
        + "minute": 59,
        + "hour": 23,
        + "day": 1},
      * "custom": {
        + "timezone": "string",
        + "cron": "string"}}],
  + "sharing": {
    - "users": [
      * {
        + "access": "NONE",
        + "user": {
          - "email": "string"}}],
    - "collections": [
      * {
        + "access": "NONE",
        + "collection": {
          - "name": "string"}}],
    - "groups": [
      * {
        + "access": "NONE",
        + "group": {
          - "name": "string"}}],
    - "workspace": {
      * "access": "NONE"},
    - "publicWeb": {
      * "access": "NONE"},
    - "support": {
      * "access": "NONE"}}},
* "errors": [
  + {
    - "groupIds": [
      * "497f6eca-6276-4993-bfeb-53cbbbba6f08"],
    - "reason": "string"}]

}`

## IngestSemanticProject

Ingest a semantic project from a zip file.

This API endpoint is subject to a maximum of 3 requests per minute.

##### Authorizations:

*bearerAuth*

##### path Parameters

|  |  |
| --- | --- |
| semanticProjectId required | string <uuid>  (SemanticProjectId) ^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}...Show pattern  Unique ID for a Hex semantic project. This can be found from the semantic projects admin panel (in Settings). |

##### Request Body schema: application/json required

|  |  |
| --- | --- |
| verbose | boolean  Default:  true  Whether to respond with detail on which components of the semantic layer were successfully synced |
| debug | boolean  Default:  false  Whether to include additional debug information |
| dryRun | boolean  If enabled, the sync will not actually write to the database |

### Responses

**201**

**400**

**403**

**415**

**500**

**502**

post/v1/semantic-(projects|models)/{semanticProjectId}/ingest

https://app.hex.tech/api/v1/semantic-(projects|models)/{semanticProjectId}/ingest

### Request samples

* Payload

Content type

application/json

Copy

`{

* "verbose": true,
* "debug": false,
* "dryRun": true

}`

### Response samples

* 201
* 400
* 403
* 415
* 500
* 502

Content type

application/json

Copy

 Expand all  Collapse all

`{

* "traceId": "string",
* "contents": [
  + "string"],
* "warnings": [
  + "string"],
* "skipped": {
  + "property1": null,
  + "property2": null},
* "problems": [
  + {
    - "severity": "fatal",
    - "message": "string",
    - "cause_paths": [
      * [
        + "string"]],
    - "impact_paths": [
      * [
        + "string"]],
    - "validated_by_json_schema": true,
    - "display": "string"}],
* "debug": {
  + "metricflowModelSchemas": { }}

}`

## UpdateSemanticProject

Use this endpoint to add or remove a status (including endorsements) from datasets and views within a semantic project

This endpoint uses atomic semantics - if any update in the batch fails validation,
the entire request fails and no changes are applied.

##### Authorizations:

*bearerAuth*

##### path Parameters

|  |  |
| --- | --- |
| semanticProjectId required | string <uuid>  (SemanticProjectId) ^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}...Show pattern  Unique ID for a Hex semantic project. This can be found from the semantic projects admin panel (in Settings). |

##### Request Body schema: application/json required

|  |  |
| --- | --- |
| updates required | Array of objects (SemanticObjectUpdate)  Array of updates to apply |
| Array  |  |  | | --- | --- | | type required | string  Enum: "DATASET" "VIEW"  The type of object to update | | name required | string  The name of the dataset or view | | status required | string or null  The status name to apply, or null to remove the current status | | |

### Responses

**200**

**400**

**403**

**404**

patch/v1/semantic-(projects|models)/{semanticProjectId}

https://app.hex.tech/api/v1/semantic-(projects|models)/{semanticProjectId}

### Request samples

* Payload

Content type

application/json

Copy

 Expand all  Collapse all

`{

* "updates": [
  + {
    - "type": "DATASET",
    - "name": "string",
    - "status": "string"}]

}`

### Response samples

* 200
* 400
* 403
* 404

Content type

application/json

Copy

 Expand all  Collapse all

`{

* "updated": {
  + "views": [
    - {
      * "status": "string",
      * "name": "string"}],
  + "datasets": [
    - {
      * "status": "string",
      * "name": "string"}]}

}`

## CancelRun

Cancel a project run.

##### Authorizations:

*bearerAuth*

##### path Parameters

|  |  |
| --- | --- |
| projectId required | string <uuid>  (ProjectId) ^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}...Show pattern  Unique ID for a Hex project. This can be found in the Variables side bar of the Logic View of a project, or by visiting the Project, and copying the UUID after `hex` in the URL. |
| runId required | string <uuid>  (InputRunId) ^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}...Show pattern  Unique ID for a run of a Hex project. This ID is part of the response returned by the RunProject endpoint. The GetProjectRuns endpoint can also be used to find the specific runs for a project. |

### Responses

**204**

**400**

**403**

**422**

delete/v1/projects/{projectId}/runs/{runId}

https://app.hex.tech/api/v1/projects/{projectId}/runs/{runId}

### Response samples

* 400
* 403
* 422

Content type

application/json

Copy

`{

* "details": "string",
* "traceId": "string",
* "reason": "string"

}`

## GetRunStatus

Get the status of a project run.

This endpoint is subject to the following rate limits:

* `hex-api`: Default rate limit group for the Hex API
  + Max requests per minute may vary (default: 30)
  + Max requests per hour may vary (default: 1800)

##### Authorizations:

*bearerAuth*

##### path Parameters

|  |  |
| --- | --- |
| projectId required | string  The project the run belongs to. |
| runId required | string  The run to retrieve. |

##### header Parameters

|  |  |
| --- | --- |
| enable-expanded-stats | string  Include state events and the run's flag configuration override. Set to `true` to enable. |

### Responses

**200** 

Successful response

**400** 

Invalid input data

**403** 

Insufficient access

**422** 

Unprocessable content

get/v1/projects/{projectId}/runs/{runId}

https://app.hex.tech/api/v1/projects/{projectId}/runs/{runId}

### Response samples

* 200
* 400
* 403
* 422

Content type

application/json

Copy

 Expand all  Collapse all

`{

* "projectId": "string",
* "projectVersion": "string",
* "runId": "string",
* "runUrl": "string",
* "status": "PENDING",
* "runTrigger": "API",
* "startTime": "string",
* "endTime": "string",
* "elapsedTime": 0,
* "flagConfigOverride": "string",
* "traceId": "string",
* "notifications": [
  + {
    - "type": "SUCCESS",
    - "subject": "string",
    - "body": "string",
    - "recipientType": "USER",
    - "includeSuccessScreenshot": true,
    - "screenshotFormat": [
      * "png"],
    - "recipient": {
      * "id": "string",
      * "name": "string",
      * "isPrivate": true}}],
* "stateEvents": [
  + {
    - "type": "string",
    - "value": "string",
    - "timestamp": "string"}]

}`

## GetGroup

##### Authorizations:

*bearerAuth*

##### path Parameters

|  |  |
| --- | --- |
| groupId required | string <uuid>  (GroupId) ^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}...Show pattern  Unique ID for a group. This can be found from the groups page (in Settings). |

### Responses

**200**

**400**

**403**

**500**

get/v1/groups/{groupId}

https://app.hex.tech/api/v1/groups/{groupId}

### Response samples

* 200
* 400
* 403
* 500

Content type

application/json

Copy

`{

* "id": "497f6eca-6276-4993-bfeb-53cbbbba6f08",
* "name": "string",
* "createdAt": "string"

}`

## DeleteGroup

##### Authorizations:

*bearerAuth*

##### path Parameters

|  |  |
| --- | --- |
| groupId required | string <uuid>  (GroupId) ^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}...Show pattern  Unique ID for a group. This can be found from the groups page (in Settings). |

### Responses

**204**

**400**

**403**

**500**

delete/v1/groups/{groupId}

https://app.hex.tech/api/v1/groups/{groupId}

### Response samples

* 400
* 403
* 500

Content type

application/json

Copy

`{

* "details": "string",
* "traceId": "string",
* "reason": "string"

}`

## EditGroup

##### Authorizations:

*bearerAuth*

##### path Parameters

|  |  |
| --- | --- |
| groupId required | string <uuid>  (GroupId) ^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}...Show pattern  Unique ID for a group. This can be found from the groups page (in Settings). |

##### Request Body schema: application/json required

|  |  |
| --- | --- |
| members | object |
| name | string (Name)   non-empty |

### Responses

**200**

**400**

**403**

**500**

patch/v1/groups/{groupId}

https://app.hex.tech/api/v1/groups/{groupId}

### Request samples

* Payload

Content type

application/json

Copy

 Expand all  Collapse all

`{

* "members": {
  + "remove": {
    - "users": [
      * {
        + "id": "497f6eca-6276-4993-bfeb-53cbbbba6f08"}]},
  + "add": {
    - "users": [
      * {
        + "id": "497f6eca-6276-4993-bfeb-53cbbbba6f08"}]}},
* "name": "string"

}`

### Response samples

* 200
* 400
* 403
* 500

Content type

application/json

Copy

`{

* "id": "497f6eca-6276-4993-bfeb-53cbbbba6f08",
* "name": "string",
* "createdAt": "string"

}`

## ListGroups

##### Authorizations:

*bearerAuth*

##### query Parameters

|  |  |
| --- | --- |
| after | any  Default:  null |
| before | any  Default:  null |
| limit | integer <int32>  (LargerPageSize)   [ 1 .. 500 ]  Default:  "25"  Number of results to fetch per page for paginated requests |
| sortBy | string (ListGroupsSortByEnum)  Enum: "CREATED\_AT" "NAME" |
| sortDirection | string (SortDirectionEnum)  Enum: "DESC" "ASC" |

### Responses

**200**

**400**

**403**

**500**

get/v1/groups

https://app.hex.tech/api/v1/groups

### Response samples

* 200
* 400
* 403
* 500

Content type

application/json

Copy

 Expand all  Collapse all

`{

* "values": [
  + {
    - "id": "497f6eca-6276-4993-bfeb-53cbbbba6f08",
    - "name": "string",
    - "createdAt": "string"}],
* "pagination": {
  + "after": "string",
  + "before": "string"}

}`

## CreateGroup

##### Authorizations:

*bearerAuth*

##### Request Body schema: application/json required

|  |  |
| --- | --- |
| members | object (GroupMembers) |
| name required | string (Name)   non-empty |

### Responses

**201**

**400**

**403**

**500**

post/v1/groups

https://app.hex.tech/api/v1/groups

### Request samples

* Payload

Content type

application/json

Copy

 Expand all  Collapse all

`{

* "members": {
  + "users": [
    - {
      * "id": "497f6eca-6276-4993-bfeb-53cbbbba6f08"}]},
* "name": "string"

}`

### Response samples

* 201
* 400
* 403
* 500

Content type

application/json

Copy

 Expand all  Collapse all

`{

* "id": "497f6eca-6276-4993-bfeb-53cbbbba6f08",
* "name": "string",
* "members": {
  + "users": [
    - {
      * "id": "497f6eca-6276-4993-bfeb-53cbbbba6f08"}]}

}`

## CreateDataConnection

##### Authorizations:

*bearerAuth*

##### Request Body schema: application/json required

|  |  |
| --- | --- |
| sharing | object |
| schemaRefreshAccess | string (DataConnectionSchemaRefreshAccess)  Enum: "ADMINS" "USERS\_WITH\_QUERY\_ACCESS" |
| schemaRefreshSchedule | object (SchemaRefreshScheduleApiResource) |
| schemaFilters | object |
| allowWritebackCells | boolean |
| includeMagic | boolean |
| connectViaSsh | boolean |
| description | string |
| connectionDetails required | object or object or object or object or object or object or object (CreateConnectionDetails) |
| type required | string (DataConnectionApiType)  Enum: "athena" "bigquery" "clickhouse" "databricks" "postgres" "redshift" "snowflake" "trino" |
| name required | string (Name)   non-empty |

### Responses

**201**

**400**

**403**

**404**

**422**

**500**

post/v1/data-connections

https://app.hex.tech/api/v1/data-connections

### Request samples

* Payload

Content type

application/json

Copy

 Expand all  Collapse all

`{

* "sharing": {
  + "workspace": {
    - "public": "NONE",
    - "guests": "NONE",
    - "members": "NONE"},
  + "groups": [
    - {
      * "access": "NONE",
      * "group": {
        + "id": "497f6eca-6276-4993-bfeb-53cbbbba6f08"}}]},
* "schemaRefreshAccess": "ADMINS",
* "schemaRefreshSchedule": {
  + "cadence": "HOURLY",
  + "enabled": true,
  + "daily": {
    - "timezoneString": "string",
    - "minute": 59,
    - "hour": 23},
  + "weekly": {
    - "timezoneString": "string",
    - "minute": 59,
    - "hour": 23,
    - "dayOfWeek": "SUNDAY"},
  + "monthly": {
    - "timezoneString": "string",
    - "minute": 59,
    - "hour": 23,
    - "day": 1},
  + "custom": {
    - "timezoneString": "string",
    - "cron": "string"}},
* "schemaFilters": {
  + "tables": {
    - "exclude": {
      * "values": [
        + "string"],
      * "matchType": "EXACT"},
    - "include": {
      * "values": [
        + "string"],
      * "matchType": "EXACT"}},
  + "schemas": {
    - "exclude": {
      * "values": [
        + "string"],
      * "matchType": "EXACT"},
    - "include": {
      * "values": [
        + "string"],
      * "matchType": "EXACT"}},
  + "databases": {
    - "exclude": {
      * "values": [
        + "string"],
      * "matchType": "EXACT"},
    - "include": {
      * "values": [
        + "string"],
      * "matchType": "EXACT"}}},
* "allowWritebackCells": true,
* "includeMagic": true,
* "connectViaSsh": true,
* "description": "string",
* "connectionDetails": {
  + "athena": {
    - "secretAccessKey": "string",
    - "accessKeyId": "string",
    - "workgroup": "string",
    - "catalog": "string",
    - "s3OutputPath": "string",
    - "port": 0.1,
    - "hostname": "string"}},
* "type": "athena",
* "name": "string"

}`

### Response samples

* 201
* 400
* 403
* 404
* 422
* 500

Content type

application/json

Copy

 Expand all  Collapse all

`{

* "id": "497f6eca-6276-4993-bfeb-53cbbbba6f08",
* "name": "string",
* "type": "athena",
* "description": "string",
* "connectionDetails": {
  + "athena": {
    - "accessKeyId": "string",
    - "workgroup": "string",
    - "catalog": "string",
    - "s3OutputPath": "string",
    - "port": 0.1,
    - "hostname": "string"}},
* "connectViaSsh": true,
* "includeMagic": true,
* "allowWritebackCells": true,
* "schemaFilters": {
  + "tables": {
    - "exclude": {
      * "values": [
        + "string"],
      * "matchType": "EXACT"},
    - "include": {
      * "values": [
        + "string"],
      * "matchType": "EXACT"}},
  + "schemas": {
    - "exclude": {
      * "values": [
        + "string"],
      * "matchType": "EXACT"},
    - "include": {
      * "values": [
        + "string"],
      * "matchType": "EXACT"}},
  + "databases": {
    - "exclude": {
      * "values": [
        + "string"],
      * "matchType": "EXACT"},
    - "include": {
      * "values": [
        + "string"],
      * "matchType": "EXACT"}}},
* "schemaRefreshSchedule": {
  + "cadence": "HOURLY",
  + "enabled": true,
  + "daily": {
    - "timezoneString": "string",
    - "minute": 59,
    - "hour": 23},
  + "weekly": {
    - "timezoneString": "string",
    - "minute": 59,
    - "hour": 23,
    - "dayOfWeek": "SUNDAY"},
  + "monthly": {
    - "timezoneString": "string",
    - "minute": 59,
    - "hour": 23,
    - "day": 1},
  + "custom": {
    - "timezoneString": "string",
    - "cron": "string"}},
* "schemaRefreshAccess": "ADMINS",
* "sharing": {
  + "workspace": {
    - "public": "NONE",
    - "guests": "NONE",
    - "members": "NONE"},
  + "groups": [
    - {
      * "access": "NONE",
      * "group": {
        + "name": "string",
        + "id": "497f6eca-6276-4993-bfeb-53cbbbba6f08"}}]}

}`

## ListDataConnections

List the workspace's data connections.

This endpoint is subject to the following rate limits:

* `hex-api`: Default rate limit group for the Hex API
  + Max requests per minute may vary (default: 30)
  + Max requests per hour may vary (default: 1800)

##### Authorizations:

*bearerAuth*

##### query Parameters

|  |  |
| --- | --- |
| after | string or null  Default:  null |
| before | string or null  Default:  null |
| limit | number  [ 1 .. 100 ]  Default:  25 |
| sortBy | string  Default:  "NAME"  Enum: "NAME" "CREATED\_AT" |
| sortDirection | string  Default:  "ASC"  Enum: "ASC" "DESC" |

### Responses

**200** 

Successful response

**400** 

Invalid input data

**401** 

Authorization not provided

**403** 

Insufficient access

**404** 

Not found

**500** 

Internal server error

get/v1/data-connections

https://app.hex.tech/api/v1/data-connections

### Response samples

* 200
* 400
* 401
* 403
* 404
* 500

Content type

application/json

Copy

 Expand all  Collapse all

`{

* "values": [
  + {
    - "id": "string",
    - "name": "string",
    - "type": "athena",
    - "description": "string",
    - "connectionDetails": {
      * "athena": {
        + "hostname": "string",
        + "port": 0,
        + "s3OutputPath": "string",
        + "catalog": "string",
        + "workgroup": "string",
        + "accessKeyId": "string"}},
    - "connectViaSsh": true,
    - "includeMagic": true,
    - "allowWritebackCells": true,
    - "schemaFilters": {
      * "databases": {
        + "include": {
          - "matchType": "EXACT",
          - "values": [
            * "string"]},
        + "exclude": {
          - "matchType": "EXACT",
          - "values": [
            * "string"]}},
      * "schemas": {
        + "include": {
          - "matchType": "EXACT",
          - "values": [
            * "string"]},
        + "exclude": {
          - "matchType": "EXACT",
          - "values": [
            * "string"]}},
      * "tables": {
        + "include": {
          - "matchType": "EXACT",
          - "values": [
            * "string"]},
        + "exclude": {
          - "matchType": "EXACT",
          - "values": [
            * "string"]}}},
    - "schemaRefreshSchedule": {
      * "cadence": "HOURLY",
      * "enabled": true,
      * "daily": {
        + "hour": 0,
        + "minute": 0,
        + "timezoneString": "string"},
      * "weekly": {
        + "dayOfWeek": "SUNDAY",
        + "hour": 0,
        + "minute": 0,
        + "timezoneString": "string"},
      * "monthly": {
        + "day": 0,
        + "hour": 0,
        + "minute": 0,
        + "timezoneString": "string"},
      * "custom": {
        + "cron": "string",
        + "timezoneString": "string"}},
    - "schemaRefreshAccess": "ADMINS",
    - "sharing": {
      * "groups": [
        + {
          - "group": {
            * "id": "string",
            * "name": "string"},
          - "access": "NONE"}],
      * "workspace": {
        + "members": "NONE",
        + "guests": "NONE",
        + "public": "NONE"}}}],
* "pagination": {
  + "before": null,
  + "after": null}

}`

## EditDataConnection

##### Authorizations:

*bearerAuth*

##### path Parameters

|  |  |
| --- | --- |
| dataConnectionId required | string <uuid>  (DataConnectionId) ^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}...Show pattern  Unique ID for a data connection. |

##### Request Body schema: application/json required

|  |  |
| --- | --- |
| sharing | object |
| schemaRefreshAccess | string (DataConnectionSchemaRefreshAccess)  Enum: "ADMINS" "USERS\_WITH\_QUERY\_ACCESS" |
| schemaRefreshSchedule | object or null |
| schemaFilters | object |
| allowWritebackCells | boolean |
| includeMagic | boolean |
| connectViaSsh | boolean |
| description | string |
| connectionDetails | object or object or object or object or object or object or object (EditConnectionDetails) |
| name | string |

### Responses

**201**

**400**

**403**

**404**

**422**

**500**

patch/v1/data-connections/{dataConnectionId}

https://app.hex.tech/api/v1/data-connections/{dataConnectionId}

### Request samples

* Payload

Content type

application/json

Copy

 Expand all  Collapse all

`{

* "sharing": {
  + "workspace": {
    - "public": "NONE",
    - "guests": "NONE",
    - "members": "NONE"},
  + "groups": {
    - "upsert": [
      * {
        + "access": "NONE",
        + "group": {
          - "id": "497f6eca-6276-4993-bfeb-53cbbbba6f08"}}]}},
* "schemaRefreshAccess": "ADMINS",
* "schemaRefreshSchedule": {
  + "cadence": "HOURLY",
  + "enabled": true,
  + "daily": {
    - "timezoneString": "string",
    - "minute": 59,
    - "hour": 23},
  + "weekly": {
    - "timezoneString": "string",
    - "minute": 59,
    - "hour": 23,
    - "dayOfWeek": "SUNDAY"},
  + "monthly": {
    - "timezoneString": "string",
    - "minute": 59,
    - "hour": 23,
    - "day": 1},
  + "custom": {
    - "timezoneString": "string",
    - "cron": "string"}},
* "schemaFilters": {
  + "tables": {
    - "exclude": {
      * "values": [
        + "string"],
      * "matchType": "EXACT"},
    - "include": {
      * "values": [
        + "string"],
      * "matchType": "EXACT"}},
  + "schemas": {
    - "exclude": {
      * "values": [
        + "string"],
      * "matchType": "EXACT"},
    - "include": {
      * "values": [
        + "string"],
      * "matchType": "EXACT"}},
  + "databases": {
    - "exclude": {
      * "values": [
        + "string"],
      * "matchType": "EXACT"},
    - "include": {
      * "values": [
        + "string"],
      * "matchType": "EXACT"}}},
* "allowWritebackCells": true,
* "includeMagic": true,
* "connectViaSsh": true,
* "description": "string",
* "connectionDetails": {
  + "athena": {
    - "secretAccessKey": "string",
    - "accessKeyId": "string",
    - "workgroup": "string",
    - "catalog": "string",
    - "s3OutputPath": "string",
    - "port": 0.1,
    - "hostname": "string"}},
* "name": "string"

}`

### Response samples

* 201
* 400
* 403
* 404
* 422
* 500

Content type

application/json

Copy

 Expand all  Collapse all

`{

* "id": "497f6eca-6276-4993-bfeb-53cbbbba6f08",
* "name": "string",
* "type": "athena",
* "description": "string",
* "connectionDetails": {
  + "athena": {
    - "accessKeyId": "string",
    - "workgroup": "string",
    - "catalog": "string",
    - "s3OutputPath": "string",
    - "port": 0.1,
    - "hostname": "string"}},
* "connectViaSsh": true,
* "includeMagic": true,
* "allowWritebackCells": true,
* "schemaFilters": {
  + "tables": {
    - "exclude": {
      * "values": [
        + "string"],
      * "matchType": "EXACT"},
    - "include": {
      * "values": [
        + "string"],
      * "matchType": "EXACT"}},
  + "schemas": {
    - "exclude": {
      * "values": [
        + "string"],
      * "matchType": "EXACT"},
    - "include": {
      * "values": [
        + "string"],
      * "matchType": "EXACT"}},
  + "databases": {
    - "exclude": {
      * "values": [
        + "string"],
      * "matchType": "EXACT"},
    - "include": {
      * "values": [
        + "string"],
      * "matchType": "EXACT"}}},
* "schemaRefreshSchedule": {
  + "cadence": "HOURLY",
  + "enabled": true,
  + "daily": {
    - "timezoneString": "string",
    - "minute": 59,
    - "hour": 23},
  + "weekly": {
    - "timezoneString": "string",
    - "minute": 59,
    - "hour": 23,
    - "dayOfWeek": "SUNDAY"},
  + "monthly": {
    - "timezoneString": "string",
    - "minute": 59,
    - "hour": 23,
    - "day": 1},
  + "custom": {
    - "timezoneString": "string",
    - "cron": "string"}},
* "schemaRefreshAccess": "ADMINS",
* "sharing": {
  + "workspace": {
    - "public": "NONE",
    - "guests": "NONE",
    - "members": "NONE"},
  + "groups": [
    - {
      * "access": "NONE",
      * "group": {
        + "name": "string",
        + "id": "497f6eca-6276-4993-bfeb-53cbbbba6f08"}}]}

}`

## GetDataConnection

Get a single data connection by its ID.

This endpoint is subject to the following rate limits:

* `hex-api`: Default rate limit group for the Hex API
  + Max requests per minute may vary (default: 30)
  + Max requests per hour may vary (default: 1800)

##### Authorizations:

*bearerAuth*

##### path Parameters

|  |  |
| --- | --- |
| dataConnectionId required | string |

### Responses

**200** 

Successful response

**400** 

Invalid input data

**401** 

Authorization not provided

**403** 

Insufficient access

**404** 

Not found

**500** 

Internal server error

get/v1/data-connections/{dataConnectionId}

https://app.hex.tech/api/v1/data-connections/{dataConnectionId}

### Response samples

* 200
* 400
* 401
* 403
* 404
* 500

Content type

application/json

Copy

 Expand all  Collapse all

`{

* "id": "string",
* "name": "string",
* "type": "athena",
* "description": "string",
* "connectionDetails": {
  + "athena": {
    - "hostname": "string",
    - "port": 0,
    - "s3OutputPath": "string",
    - "catalog": "string",
    - "workgroup": "string",
    - "accessKeyId": "string"}},
* "connectViaSsh": true,
* "includeMagic": true,
* "allowWritebackCells": true,
* "schemaFilters": {
  + "databases": {
    - "include": {
      * "matchType": "EXACT",
      * "values": [
        + "string"]},
    - "exclude": {
      * "matchType": "EXACT",
      * "values": [
        + "string"]}},
  + "schemas": {
    - "include": {
      * "matchType": "EXACT",
      * "values": [
        + "string"]},
    - "exclude": {
      * "matchType": "EXACT",
      * "values": [
        + "string"]}},
  + "tables": {
    - "include": {
      * "matchType": "EXACT",
      * "values": [
        + "string"]},
    - "exclude": {
      * "matchType": "EXACT",
      * "values": [
        + "string"]}}},
* "schemaRefreshSchedule": {
  + "cadence": "HOURLY",
  + "enabled": true,
  + "daily": {
    - "hour": 0,
    - "minute": 0,
    - "timezoneString": "string"},
  + "weekly": {
    - "dayOfWeek": "SUNDAY",
    - "hour": 0,
    - "minute": 0,
    - "timezoneString": "string"},
  + "monthly": {
    - "day": 0,
    - "hour": 0,
    - "minute": 0,
    - "timezoneString": "string"},
  + "custom": {
    - "cron": "string",
    - "timezoneString": "string"}},
* "schemaRefreshAccess": "ADMINS",
* "sharing": {
  + "groups": [
    - {
      * "group": {
        + "id": "string",
        + "name": "string"},
      * "access": "NONE"}],
  + "workspace": {
    - "members": "NONE",
    - "guests": "NONE",
    - "public": "NONE"}}

}`

## UpdateDataConnectionSchema

Use this endpoint to add or remove a status (including endorsements) from databases, schemas, and tables
within a data connection

This endpoint uses atomic semantics - if any update in the batch fails validation,
the entire request fails and no changes are applied

##### Authorizations:

*bearerAuth*

##### path Parameters

|  |  |
| --- | --- |
| dataConnectionId required | string <uuid>  (DataConnectionId) ^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}...Show pattern  Unique ID for a data connection. |

##### Request Body schema: application/json required

|  |  |
| --- | --- |
| updates required | Array of objects (SchemaObjectUpdate)  Array of updates to apply |
| Array  |  |  | | --- | --- | | type required | string  Enum: "DATABASE" "SCHEMA" "TABLE"  The type of object to update | | name required | string  The name of the object - simple for DATABASE, qualified for SCHEMA/TABLE | | status required | string or null  The status name to apply, or null to remove the current status | | |

### Responses

**200**

**400**

**403**

**404**

patch/v1/data-connections/{dataConnectionId}/schema

https://app.hex.tech/api/v1/data-connections/{dataConnectionId}/schema

### Request samples

* Payload

Content type

application/json

Copy

 Expand all  Collapse all

`{

* "updates": [
  + {
    - "type": "DATABASE",
    - "name": "string",
    - "status": "string"}]

}`

### Response samples

* 200
* 400
* 403
* 404

Content type

application/json

Copy

 Expand all  Collapse all

`{

* "updated": {
  + "tables": [
    - {`