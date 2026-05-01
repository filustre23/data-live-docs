* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback

# Method: projects.locations.workflows.list Stay organized with collections Save and categorize content based on your preferences.

* [HTTP request](#body.HTTP_TEMPLATE)
* [Path parameters](#body.PATH_PARAMETERS)
* [Query parameters](#body.QUERY_PARAMETERS)
* [Request body](#body.request_body)
* [Response body](#body.response_body)
  + [JSON representation](#body.ListMigrationWorkflowsResponse.SCHEMA_REPRESENTATION)
* [Authorization scopes](#body.aspect)
* [IAM Permissions](#body.aspect_1)
* [Try it!](#try-it)

Lists previously created migration workflow.

### HTTP request

`GET https://bigquerymigration.googleapis.com/v2alpha/{parent=projects/*/locations/*}/workflows`

The URL uses [gRPC Transcoding](https://google.aip.dev/127) syntax.

### Path parameters

| Parameters | |
| --- | --- |
| `parent` | `string`  Required. The project and location of the migration workflows to list. Example: `projects/123/locations/us` |

### Query parameters

| Parameters | |
| --- | --- |
| `readMask` | `string (FieldMask format)`  The list of fields to be retrieved. |
| `pageSize` | `integer`  The maximum number of migration workflows to return. The service may return fewer than this number. |
| `pageToken` | `string`  A page token, received from previous `workflows.list` call. Provide this to retrieve the subsequent page.  When paginating, all other parameters provided to `workflows.list` must match the call that provided the page token. |
| `filter` | `string`  Optional. An optional AIP-160 filter to apply. The following attributes are supported: `displayName`, `state`, `task.name`, and `task.type`. |
| `orderBy` | `string`  Optional. An optional AIP-132 order by field. The following attributes are supported: `displayName`, `state`, `task.name`, and `task.type`. |

### Request body

The request body must be empty.

### Response body

Response object for a `workflows.list` call.

If successful, the response body contains data with the following structure:

| JSON representation |
| --- |
| ``` {   "migrationWorkflows": [     {       object (MigrationWorkflow)     }   ],   "nextPageToken": string } ``` |

| Fields | |
| --- | --- |
| `migrationWorkflows[]` | `object (MigrationWorkflow)`  The migration workflows for the specified project / location. |
| `nextPageToken` | `string`  A token, which can be sent as `pageToken` to retrieve the next page. If this field is omitted, there are no subsequent pages. |

### Authorization scopes

Requires the following OAuth scope:

* `https://www.googleapis.com/auth/cloud-platform`

For more information, see the [Authentication Overview](/docs/authentication#authorization-gcp).

### IAM Permissions

Requires the following [IAM](https://cloud.google.com/iam/docs) permission on the `parent` resource:

* `bigquerymigration.workflows.list`

For more information, see the [IAM documentation](https://cloud.google.com/iam/docs).




Send feedback

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2025-07-02 UTC.




Need to tell us more?

[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Hard to understand","hardToUnderstand","thumb-down"],["Incorrect information or sample code","incorrectInformationOrSampleCode","thumb-down"],["Missing the information/samples I need","missingTheInformationSamplesINeed","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2025-07-02 UTC."],[],[]]