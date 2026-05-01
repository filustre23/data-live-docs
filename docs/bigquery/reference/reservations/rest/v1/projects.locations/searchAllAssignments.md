* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback

# Method: projects.locations.searchAllAssignments Stay organized with collections Save and categorize content based on your preferences.

* [HTTP request](#body.HTTP_TEMPLATE)
* [Path parameters](#body.PATH_PARAMETERS)
* [Query parameters](#body.QUERY_PARAMETERS)
* [Request body](#body.request_body)
* [Response body](#body.response_body)
  + [JSON representation](#body.SearchAllAssignmentsResponse.SCHEMA_REPRESENTATION)
* [Authorization scopes](#body.aspect)
* [Try it!](#try-it)

Looks up assignments for a specified resource for a particular region. If the request is about a project:

1. Assignments created on the project will be returned if they exist.
2. Otherwise assignments created on the closest ancestor will be returned.
3. Assignments for different JobTypes will all be returned.

The same logic applies if the request is about a folder.

If the request is about an organization, then assignments created on the organization will be returned (organization doesn't have ancestors).

Comparing to assignments.list, there are some behavior differences:

1. permission on the assignee will be verified in this API.
2. Hierarchy lookup (project->folder->organization) happens in this API.
3. Parent here is `projects/*/locations/*`, instead of `projects/*/locations/*reservations/*`.

### HTTP request

`GET https://bigqueryreservation.googleapis.com/v1/{parent=projects/*/locations/*}:searchAllAssignments`

The URL uses [gRPC Transcoding](https://google.aip.dev/127) syntax.

### Path parameters

| Parameters | |
| --- | --- |
| `parent` | `string`  Required. The resource name with location (project name could be the wildcard '-'), e.g.: `projects/-/locations/US`.  Authorization requires the following [IAM](https://cloud.google.com/iam/docs/) permission on the specified resource `parent`:   * `bigquery.reservationAssignments.search` |

### Query parameters

| Parameters | |
| --- | --- |
| `query` | `string`  Please specify resource name as assignee in the query.  Examples:   * `assignee=projects/myproject` * `assignee=folders/123` * `assignee=organizations/456` |
| `pageSize` | `integer`  The maximum number of items to return per page. |
| `pageToken` | `string`  The nextPageToken value returned from a previous List request, if any. |

### Request body

The request body must be empty.

### Response body

The response for `ReservationService.SearchAllAssignments`.

If successful, the response body contains data with the following structure:

| JSON representation |
| --- |
| ``` {   "assignments": [     {       object (Assignment)     }   ],   "nextPageToken": string } ``` |

| Fields | |
| --- | --- |
| `assignments[]` | `object (Assignment)`  List of assignments visible to the user. |
| `nextPageToken` | `string`  Token to retrieve the next page of results, or empty if there are no more results in the list. |

### Authorization scopes

Requires one of the following OAuth scopes:

* `https://www.googleapis.com/auth/bigquery`
* `https://www.googleapis.com/auth/cloud-platform`

For more information, see the [Authentication Overview](/docs/authentication#authorization-gcp).




Send feedback

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2025-07-02 UTC.




Need to tell us more?

[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Hard to understand","hardToUnderstand","thumb-down"],["Incorrect information or sample code","incorrectInformationOrSampleCode","thumb-down"],["Missing the information/samples I need","missingTheInformationSamplesINeed","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2025-07-02 UTC."],[],[]]