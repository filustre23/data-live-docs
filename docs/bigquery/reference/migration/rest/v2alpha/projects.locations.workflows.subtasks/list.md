* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback

# Method: projects.locations.workflows.subtasks.list Stay organized with collections Save and categorize content based on your preferences.

* [HTTP request](#body.HTTP_TEMPLATE)
* [Path parameters](#body.PATH_PARAMETERS)
* [Query parameters](#body.QUERY_PARAMETERS)
* [Request body](#body.request_body)
* [Response body](#body.response_body)
  + [JSON representation](#body.ListMigrationSubtasksResponse.SCHEMA_REPRESENTATION)
* [Authorization scopes](#body.aspect)
* [IAM Permissions](#body.aspect_1)
* [Try it!](#try-it)

Lists previously created migration subtasks.

### HTTP request

`GET https://bigquerymigration.googleapis.com/v2alpha/{parent=projects/*/locations/*/workflows/*}/subtasks`

The URL uses [gRPC Transcoding](https://google.aip.dev/127) syntax.

### Path parameters

| Parameters | |
| --- | --- |
| `parent` | `string`  Required. The migration task of the subtasks to list. Example: `projects/123/locations/us/workflows/1234` |

### Query parameters

| Parameters | |
| --- | --- |
| `readMask` | `string (FieldMask format)`  Optional. The list of fields to be retrieved. |
| `pageSize` | `integer`  Optional. The maximum number of migration tasks to return. The service may return fewer than this number. |
| `pageToken` | `string`  Optional. A page token, received from previous `subtasks.list` call. Provide this to retrieve the subsequent page.  When paginating, all other parameters provided to `subtasks.list` must match the call that provided the page token. |
| `filter` | `string`  Optional. The filter to apply. This can be used to get the subtasks of a specific tasks in a workflow, e.g. `migrationTask = "ab012"` where `"ab012"` is the task ID (not the name in the named map). |

### Request body

The request body must be empty.

### Response body

Response object for a `subtasks.list` call.

If successful, the response body contains data with the following structure:

| JSON representation |
| --- |
| ``` {   "migrationSubtasks": [     {       object (MigrationSubtask)     }   ],   "nextPageToken": string } ``` |

| Fields | |
| --- | --- |
| `migrationSubtasks[]` | `object (MigrationSubtask)`  The migration subtasks for the specified task. |
| `nextPageToken` | `string`  A token, which can be sent as `pageToken` to retrieve the next page. If this field is omitted, there are no subsequent pages. |

### Authorization scopes

Requires the following OAuth scope:

* `https://www.googleapis.com/auth/cloud-platform`

For more information, see the [Authentication Overview](/docs/authentication#authorization-gcp).

### IAM Permissions

Requires the following [IAM](https://cloud.google.com/iam/docs) permission on the `parent` resource:

* `bigquerymigration.subtasks.list`

For more information, see the [IAM documentation](https://cloud.google.com/iam/docs).




Send feedback

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2025-07-02 UTC.




Need to tell us more?

[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Hard to understand","hardToUnderstand","thumb-down"],["Incorrect information or sample code","incorrectInformationOrSampleCode","thumb-down"],["Missing the information/samples I need","missingTheInformationSamplesINeed","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2025-07-02 UTC."],[],[]]