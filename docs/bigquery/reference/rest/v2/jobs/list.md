* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback

# Method: jobs.list Stay organized with collections Save and categorize content based on your preferences.

* [HTTP request](#body.HTTP_TEMPLATE)
* [Path parameters](#body.PATH_PARAMETERS)
* [Query parameters](#body.QUERY_PARAMETERS)
* [Request body](#body.request_body)
* [Response body](#body.response_body)
  + [JSON representation](#body.JobList.SCHEMA_REPRESENTATION)
* [Authorization scopes](#body.aspect)
* [Try it!](#try-it)

Lists all jobs that you started in the specified project. Job information is available for a six month period after creation. The job list is sorted in reverse chronological order, by job creation time. Requires the Can View project role, or the Is Owner project role if you set the allUsers property.

### HTTP request

`GET https://bigquery.googleapis.com/bigquery/v2/projects/{projectId}/jobs`

The URL uses [gRPC Transcoding](https://google.aip.dev/127) syntax.

### Path parameters

| Parameters | |
| --- | --- |
| `projectId` | `string`  Project ID of the jobs to list. |

### Query parameters

| Parameters | |
| --- | --- |
| `allUsers` | `boolean`  Whether to display jobs owned by all users in the project. Default False. |
| `maxResults` | `integer`  The maximum number of results to return in a single response page. Leverage the page tokens to iterate through the entire collection. |
| `minCreationTime` | `string`  Min value for job creation time, in milliseconds since the POSIX epoch. If set, only jobs created after or at this timestamp are returned. |
| `maxCreationTime` | `string (UInt64Value format)`  Max value for job creation time, in milliseconds since the POSIX epoch. If set, only jobs created before or at this timestamp are returned. |
| `pageToken` | `string`  Page token, returned by a previous call, to request the next page of results. |
| `projection` | `enum`  Restrict information returned to a set of selected fields  Valid values of this enum field are:   * `MINIMAL` * `FULL` |
| `stateFilter[]` | `enum`  Filter for job state  Valid values of this enum field are:   * `DONE` * `PENDING` * `RUNNING` |
| `parentJobId` | `string`  If set, show only child jobs of the specified parent. Otherwise, show all top-level jobs. |

### Request body

The request body must be empty.

### Response body

JobList is the response format for a jobs.list call.

If successful, the response body contains data with the following structure:

| JSON representation |
| --- |
| ``` {   "etag": string,   "kind": string,   "nextPageToken": string,   "jobs": [     {       "id": string,       "kind": string,       "jobReference": {         object (JobReference)       },       "state": string,       "errorResult": {         object (ErrorProto)       },       "statistics": {         object (JobStatistics)       },       "configuration": {         object (JobConfiguration)       },       "status": {         object (JobStatus)       },       "user_email": string,       "principal_subject": string     }   ],   "unreachable": [     string   ] } ``` |

| Fields | |
| --- | --- |
| `etag` | `string`  A hash of this page of results. |
| `kind` | `string`  The resource type of the response. |
| `nextPageToken` | `string`  A token to request the next page of results. |
| `jobs[]` | `object`  tabledata.list of jobs that were requested. |
| `jobs[].id` | `string`  Unique opaque ID of the job. |
| `jobs[].kind` | `string`  The resource type. |
| `jobs[].jobReference` | `object (JobReference)`  Unique opaque ID of the job. |
| `jobs[].state` | `string`  Running state of the job. When the state is DONE, errorResult can be checked to determine whether the job succeeded or failed. |
| `jobs[].errorResult` | `object (ErrorProto)`  A result object that will be present only if the job has failed. |
| `jobs[].statistics` | `object (JobStatistics)`  Output only. Information about the job, including starting time and ending time of the job. |
| `jobs[].configuration` | `object (JobConfiguration)`  Required. Describes the job configuration. |
| `jobs[].status` | `object (JobStatus)`  [Full-projection-only] Describes the status of this job. |
| `jobs[].user_email` | `string`  [Full-projection-only] Email address of the user who ran the job. |
| `jobs[].principal_subject` | `string`  [Full-projection-only] String representation of identity of requesting party. Populated for both first- and third-party identities. Only present for APIs that support third-party identities. |
| `unreachable[]` | `string`  A list of skipped locations that were unreachable. For more information about BigQuery locations, see: <https://cloud.google.com/bigquery/docs/locations>. Example: "europe-west5" |

### Authorization scopes

Requires one of the following OAuth scopes:

* `https://www.googleapis.com/auth/bigquery`
* `https://www.googleapis.com/auth/cloud-platform`
* `https://www.googleapis.com/auth/bigquery.readonly`
* `https://www.googleapis.com/auth/cloud-platform.read-only`

For more information, see the [Authentication Overview](/docs/authentication#authorization-gcp).




Send feedback

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2026-05-05 UTC.




Need to tell us more?

[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Hard to understand","hardToUnderstand","thumb-down"],["Incorrect information or sample code","incorrectInformationOrSampleCode","thumb-down"],["Missing the information/samples I need","missingTheInformationSamplesINeed","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2026-05-05 UTC."],[],[]]