* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback

# Method: projects.list Stay organized with collections Save and categorize content based on your preferences.

* [HTTP request](#body.HTTP_TEMPLATE)
* [Query parameters](#body.QUERY_PARAMETERS)
* [Request body](#body.request_body)
* [Response body](#body.response_body)
  + [JSON representation](#body.ProjectList.SCHEMA_REPRESENTATION)
* [Authorization scopes](#body.aspect)
* [Try it!](#try-it)

RPC to list projects to which the user has been granted any project role.

Users of this method are encouraged to consider the [Resource Manager](https://cloud.google.com/resource-manager/docs/) API, which provides the underlying data for this method and has more capabilities.

### HTTP request

`GET https://bigquery.googleapis.com/bigquery/v2/projects`

The URL uses [gRPC Transcoding](https://google.aip.dev/127) syntax.

### Query parameters

| Parameters | |
| --- | --- |
| `maxResults` | `integer`  `maxResults` unset returns all results, up to 50 per page. Additionally, the number of projects in a page may be fewer than `maxResults` because projects are retrieved and then filtered to only projects with the BigQuery API enabled. |
| `pageToken` | `string`  Page token, returned by a previous call, to request the next page of results. If not present, no further pages are present. |

### Request body

The request body must be empty.

### Response body

Response object of projects.list

If successful, the response body contains data with the following structure:

| JSON representation |
| --- |
| ``` {   "kind": string,   "etag": string,   "nextPageToken": string,   "projects": [     {       "kind": string,       "id": string,       "numericId": string,       "projectReference": {         object (ProjectReference)       },       "friendlyName": string     }   ],   "totalItems": integer } ``` |

| Fields | |
| --- | --- |
| `kind` | `string`  The resource type of the response. |
| `etag` | `string`  A hash of the page of results. |
| `nextPageToken` | `string`  Use this token to request the next page of results. |
| `projects[]` | `object`  Projects to which the user has at least READ access. This field can be omitted if `totalItems` is 0. |
| `projects[].kind` | `string`  The resource type. |
| `projects[].id` | `string`  An opaque ID of this project. |
| `projects[].numericId` | `string (int64 format)`  The numeric ID of this project. |
| `projects[].projectReference` | `object (ProjectReference)`  A unique reference to this project. |
| `projects[].friendlyName` | `string`  A descriptive name for this project. A wrapper is used here because friendlyName can be set to the empty string. |
| `totalItems` | `integer`  The total number of projects in the page. A wrapper is used here because the field should still be in the response when the value is 0. |

### Authorization scopes

Requires one of the following OAuth scopes:

* `https://www.googleapis.com/auth/bigquery`
* `https://www.googleapis.com/auth/cloud-platform`
* `https://www.googleapis.com/auth/bigquery.readonly`
* `https://www.googleapis.com/auth/cloud-platform.read-only`

For more information, see the [Authentication Overview](/docs/authentication#authorization-gcp).




Send feedback

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2026-02-25 UTC.




Need to tell us more?

[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Hard to understand","hardToUnderstand","thumb-down"],["Incorrect information or sample code","incorrectInformationOrSampleCode","thumb-down"],["Missing the information/samples I need","missingTheInformationSamplesINeed","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2026-02-25 UTC."],[],[]]