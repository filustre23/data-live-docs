* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback

# Method: jobs.getQueryResults Stay organized with collections Save and categorize content based on your preferences.

* [HTTP request](#body.HTTP_TEMPLATE)
* [Path parameters](#body.PATH_PARAMETERS)
* [Query parameters](#body.QUERY_PARAMETERS)
* [Request body](#body.request_body)
* [Response body](#body.response_body)
  + [JSON representation](#body.GetQueryResultsResponse.SCHEMA_REPRESENTATION)
* [Authorization scopes](#body.aspect)
* [Try it!](#try-it)

RPC to get the results of a query job.

### HTTP request

`GET https://bigquery.googleapis.com/bigquery/v2/projects/{projectId}/queries/{jobId}`

The URL uses [gRPC Transcoding](https://google.aip.dev/127) syntax.

### Path parameters

| Parameters | |
| --- | --- |
| `projectId` | `string`  Required. Project ID of the query job. |
| `jobId` | `string`  Required. Job ID of the query job. |

### Query parameters

| Parameters | |
| --- | --- |
| `startIndex` | `string (UInt64Value format)`  Zero-based index of the starting row. |
| `pageToken` | `string`  Page token, returned by a previous call, to request the next page of results. |
| `maxResults` | `integer`  Maximum number of results to read. |
| `timeoutMs` | `integer`  Optional: Specifies the maximum amount of time, in milliseconds, that the client is willing to wait for the query to complete. By default, this limit is 10 seconds (10,000 milliseconds). If the query is complete, the jobComplete field in the response is true. If the query has not yet completed, jobComplete is false.  You can request a longer timeout period in the timeoutMs field. However, the call is not guaranteed to wait for the specified timeout; it typically returns after around 200 seconds (200,000 milliseconds), even if the query is not complete.  If jobComplete is false, you can continue to wait for the query to complete by calling the getQueryResults method until the jobComplete field in the getQueryResults response is true. |
| `location` | `string`  The geographic location of the job. You must specify the location to run the job for the following scenarios:   * If the location to run a job is not in the `us` or the `eu` multi-regional location * If the job's location is in a single region (for example, `us-central1`)   For more information, see how to [specify locations](https://cloud.google.com/bigquery/docs/locations#specify_locations). |
| `formatOptions` | `object (DataFormatOptions)`  Optional. Output format adjustments. |

### Request body

The request body must be empty.

### Response body

Response object of jobs.getQueryResults.

If successful, the response body contains data with the following structure:

| JSON representation |
| --- |
| ``` {   "kind": string,   "etag": string,   "schema": {     object (TableSchema)   },   "jobReference": {     object (JobReference)   },   "totalRows": string,   "pageToken": string,   "rows": [     {       object     }   ],   "totalBytesProcessed": string,   "jobComplete": boolean,   "errors": [     {       object (ErrorProto)     }   ],   "cacheHit": boolean,   "numDmlAffectedRows": string } ``` |

| Fields | |
| --- | --- |
| `kind` | `string`  The resource type of the response. |
| `etag` | `string`  A hash of this response. |
| `schema` | `object (TableSchema)`  The schema of the results. Present only when the query completes successfully. |
| `jobReference` | `object (JobReference)`  Reference to the BigQuery Job that was created to run the query. This field will be present even if the original request timed out, in which case jobs.getQueryResults can be used to read the results once the query has completed. Since this API only returns the first page of results, subsequent pages can be fetched via the same mechanism (jobs.getQueryResults). |
| `totalRows` | `string (UInt64Value format)`  The total number of rows in the complete query result set, which can be more than the number of rows in this single page of results. Present only when the query completes successfully. |
| `pageToken` | `string`  A token used for paging results. When this token is non-empty, it indicates additional results are available. |
| `rows[]` | `object (Struct format)`  An object with as many results as can be contained within the maximum permitted reply size. To get any additional rows, you can call jobs.getQueryResults and specify the jobReference returned above. Present only when the query completes successfully.  The REST-based representation of this data leverages a series of JSON f,v objects for indicating fields and values. |
| `totalBytesProcessed` | `string (Int64Value format)`  The total number of bytes processed for this query. |
| `jobComplete` | `boolean`  Whether the query has completed or not. If rows or totalRows are present, this will always be true. If this is false, totalRows will not be available. |
| `errors[]` | `object (ErrorProto)`  Output only. The first errors or warnings encountered during the running of the job. The final message includes the number of errors that caused the process to stop. Errors here do not necessarily mean that the job has completed or was unsuccessful. For more information about error messages, see [Error messages](https://cloud.google.com/bigquery/docs/error-messages). |
| `cacheHit` | `boolean`  Whether the query result was fetched from the query cache. |
| `numDmlAffectedRows` | `string (Int64Value format)`  Output only. The number of rows affected by a DML statement. Present only for DML statements INSERT, UPDATE or DELETE. |

### Authorization scopes

Requires one of the following OAuth scopes:

* `https://www.googleapis.com/auth/bigquery`
* `https://www.googleapis.com/auth/cloud-platform`
* `https://www.googleapis.com/auth/bigquery.readonly`
* `https://www.googleapis.com/auth/cloud-platform.read-only`

For more information, see the [Authentication Overview](/docs/authentication#authorization-gcp).




Send feedback

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2025-07-02 UTC.




Need to tell us more?

[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Hard to understand","hardToUnderstand","thumb-down"],["Incorrect information or sample code","incorrectInformationOrSampleCode","thumb-down"],["Missing the information/samples I need","missingTheInformationSamplesINeed","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2025-07-02 UTC."],[],[]]