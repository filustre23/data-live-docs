* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback

# Method: jobs.query Stay organized with collections Save and categorize content based on your preferences.

* [HTTP request](#body.HTTP_TEMPLATE)
* [Path parameters](#body.PATH_PARAMETERS)
* [Request body](#body.request_body)
* [Response body](#body.response_body)
  + [JSON representation](#body.QueryResponse.SCHEMA_REPRESENTATION)
* [Authorization scopes](#body.aspect)
* [QueryRequest](#QueryRequest)
  + [JSON representation](#QueryRequest.SCHEMA_REPRESENTATION)
* [JobCreationMode](#JobCreationMode)
* [QueryResultsFormat](#QueryResultsFormat)
* [ArrowSerializationOptions](#ArrowSerializationOptions)
  + [JSON representation](#ArrowSerializationOptions.SCHEMA_REPRESENTATION)
* [CompressionCodec](#CompressionCodec)
* [PicosTimestampPrecision](#PicosTimestampPrecision)
* [ArrowSchema](#ArrowSchema)
  + [JSON representation](#ArrowSchema.SCHEMA_REPRESENTATION)
* [ArrowRecordBatch](#ArrowRecordBatch)
  + [JSON representation](#ArrowRecordBatch.SCHEMA_REPRESENTATION)
* [Try it!](#try-it)

Runs a BigQuery SQL query synchronously and returns query results if the query completes within a specified timeout.

### IAM Permissions

Requires the `bigquery.jobs.create` permission on the project resource.

Data-level permissions are highly dependent on the SQL statement being executed. While standard queries require data access (such as `bigquery.tables.getData`), complex operations like DDL or DCL may require permissions to manage reservations, IAM policies, or project settings.

### HTTP request

`POST https://bigquery.googleapis.com/bigquery/v2/projects/{projectId}/queries`

The URL uses [gRPC Transcoding](https://google.aip.dev/127) syntax.

### Path parameters

| Parameters | |
| --- | --- |
| `projectId` | `string`  Required. Project ID of the query request. |

### Request body

The request body contains an instance of `QueryRequest`.

### Response body

If successful, the response body contains data with the following structure:

| JSON representation |
| --- |
| ``` {   "kind": string,   "schema": {     object (TableSchema)   },   "jobReference": {     object (JobReference)   },   "jobCreationReason": {     object (JobCreationReason)   },   "queryId": string,   "location": string,   "totalRows": string,   "pageToken": string,   "rows": [     {       object     }   ],   "totalBytesProcessed": string,   "jobComplete": boolean,   "errors": [     {       object (ErrorProto)     }   ],   "cacheHit": boolean,   "numDmlAffectedRows": string,   "sessionInfo": {     object (SessionInfo)   },   "dmlStats": {     object (DmlStats)   },   "pageRowCount": string,   "totalBytesBilled": string,   "totalSlotMs": string,   "creationTime": string,   "startTime": string,   "endTime": string,    // The following is a list of mutually exclusive fields. At most one of the   // fields will be set in a response:   "arrowSchema": {     object (ArrowSchema)   }   // End of mutually exclusive fields.    // The following is a list of mutually exclusive fields. At most one of the   // fields will be set in a response:   "arrowRecordBatch": {     object (ArrowRecordBatch)   }   // End of mutually exclusive fields. } ``` |

| Fields | |
| --- | --- |
| `kind` | `string`  The resource type. |
| `schema` | `object (TableSchema)`  The schema of the results. Present only when the query completes successfully. |
| `jobReference` | `object (JobReference)`  Reference to the Job that was created to run the query. This field will be present even if the original request timed out, in which case jobs.getQueryResults can be used to read the results once the query has completed. Since this API only returns the first page of results, subsequent pages can be fetched via the same mechanism (jobs.getQueryResults).  If jobCreationMode was set to `JOB_CREATION_OPTIONAL` and the query completes without creating a job, this field will be empty. |
| `jobCreationReason` | `object (JobCreationReason)`  Optional. The reason why a Job was created.  Only relevant when a jobReference is present in the response. If jobReference is not present it will always be unset. |
| `queryId` | `string`  Auto-generated ID for the query. |
| `location` | `string`  Output only. The geographic location of the query.  For more information about BigQuery locations, see: <https://cloud.google.com/bigquery/docs/locations> |
| `totalRows` | `string (UInt64Value format)`  The total number of rows in the complete query result set, which can be more than the number of rows in this single page of results. |
| `pageToken` | `string`  A token used for paging results. A non-empty token indicates that additional results are available. To see additional results, query the [`jobs.getQueryResults`](https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs/getQueryResults) method. For more information, see [Paging through table data](https://cloud.google.com/bigquery/docs/paging-results). |
| `rows[]` | `object (Struct format)`  An object with as many results as can be contained within the maximum permitted reply size. To get any additional rows, you can call jobs.getQueryResults and specify the jobReference returned above. |
| `totalBytesProcessed` | `string (Int64Value format)`  The total number of bytes processed for this query. If this query was a dry run, this is the number of bytes that would be processed if the query were run. |
| `jobComplete` | `boolean`  Whether the query has completed or not. If rows or totalRows are present, this will always be true. If this is false, totalRows will not be available. |
| `errors[]` | `object (ErrorProto)`  Output only. The first errors or warnings encountered during the running of the job. The final message includes the number of errors that caused the process to stop. Errors here do not necessarily mean that the job has completed or was unsuccessful. For more information about error messages, see [Error messages](https://cloud.google.com/bigquery/docs/error-messages). |
| `cacheHit` | `boolean`  Whether the query result was fetched from the query cache. |
| `numDmlAffectedRows` | `string (Int64Value format)`  Output only. The number of rows affected by a DML statement. Present only for DML statements INSERT, UPDATE or DELETE. |
| `sessionInfo` | `object (SessionInfo)`  Output only. Information of the session if this job is part of one. |
| `dmlStats` | `object (DmlStats)`  Output only. Detailed statistics for DML statements INSERT, UPDATE, DELETE, MERGE or TRUNCATE. |
| `pageRowCount` | `string (int64 format)`  Output only. The number of rows out of `totalRows` returned in this response.  [Preview](https://cloud.google.com/products/#product-launch-stages) |
| `totalBytesBilled` | `string (int64 format)`  Output only. If the project is configured to use on-demand pricing, then this field contains the total bytes billed for the job. If the project is configured to use flat-rate pricing, then you are not billed for bytes and this field is informational only. |
| `totalSlotMs` | `string (int64 format)`  Output only. Number of slot ms the user is actually billed for. |
| `creationTime` | `string (int64 format)`  Output only. Creation time of this query, in milliseconds since the epoch. This field will be present on all queries. |
| `startTime` | `string (int64 format)`  Output only. Start time of this query, in milliseconds since the epoch. This field will be present when the query job transitions from the PENDING state to either RUNNING or DONE. |
| `endTime` | `string (int64 format)`  Output only. End time of this query, in milliseconds since the epoch. This field will be present whenever a query job is in the DONE state. |
| The schema if `query_results_format` has been specified with value other than default `STRUCT_ENCODING`.  [Preview](https://cloud.google.com/products/#product-launch-stages) The following is a list of mutually exclusive fields. At most one of the fields will be set in a response: | |
| `arrowSchema` | `object (ArrowSchema)`  Output only. Arrow schema |
| End of mutually exclusive fields. | |
| Row data is returned in format when `query_results_format` has been specified with value other than default `STRUCT_ENCODING`.  [Preview](https://cloud.google.com/products/#product-launch-stages) The following is a list of mutually exclusive fields. At most one of the fields will be set in a response: | |
| `arrowRecordBatch` | `object (ArrowRecordBatch)`  Output only. Serialized row data in Arrow RecordBatch format. |
| End of mutually exclusive fields. | |

### Authorization scopes

Requires one of the following OAuth scopes:

* `https://www.googleapis.com/auth/bigquery`
* `https://www.googleapis.com/auth/cloud-platform`
* `https://www.googleapis.com/auth/bigquery.readonly`
* `https://www.googleapis.com/auth/cloud-platform.read-only`

For more information, see the [Authentication Overview](/docs/authentication#authorization-gcp).

## QueryRequest

Describes the format of the jobs.query request.

| JSON representation |
| --- |
| ``` {   "kind": string,   "query": string,   "maxResults": integer,   "defaultDataset": {     object (DatasetReference)   },   "timeoutMs": integer,   "destinationEncryptionConfiguration": {     object (EncryptionConfiguration)   },   "dryRun": boolean,   "preserveNulls": boolean,   "useQueryCache": boolean,   "useLegacySql": boolean,   "parameterMode": string,   "queryParameters": [     {       object (QueryParameter)     }   ],   "location": string,   "formatOptions": {     object (DataFormatOptions)   },   "connectionProperties": [     {       object (ConnectionProperty)     }   ],   "labels": {     string: string,     ...   },   "maximumBytesBilled": string,   "requestId": string,   "createSession": boolean,   "jobCreationMode": enum (JobCreationMode),   "queryResultsFormat": enum (QueryResultsFormat),   "secureContext": {     object (SecureContext)   },   "jobTimeoutMs": string,   "reservation": string,    // The following is a list of mutually exclusive fields. At most one of the   // fields will be set in a response:   "arrowSerializationOptions": {     object (ArrowSerializationOptions)   }   // End of mutually exclusive fields. } ``` |

| Fields | |
| --- | --- |
| `kind` | `string`  The resource type of the request. |
| `query` | `string`  Required. A query string to execute, using Google Standard SQL or legacy SQL syntax. Example: "SELECT COUNT(f1) FROM myProjectId.myDatasetId.myTableId". |
| `maxResults` | `integer`  Optional. The maximum number of rows of data to return per page of results. Setting this flag to a small value such as 1000 and then paging through results might improve reliability when the query result set is large. In addition to this limit, responses are also limited to 10 MB. By default, there is no maximum row count, and only the byte limit applies. |
| `defaultDataset` | `object (DatasetReference)`  Optional. Specifies the default datasetId and projectId to assume for any unqualified table names in the query. If not set, all table names in the query string must be qualified in the format 'datasetId.tableId'. |
| `timeoutMs` | `integer`  Optional. Optional: Specifies the maximum amount of time, in milliseconds, that the client is willing to wait for the query to complete. By default, this limit is 10 seconds (10,000 milliseconds). If the query is complete, the jobComplete field in the response is true. If the query has not yet completed, jobComplete is false.  You can request a longer timeout period in the timeoutMs field. However, the call is not guaranteed to wait for the specified timeout; it typically returns after around 200 seconds (200,000 milliseconds), even if the query is not complete.  If jobComplete is false, you can continue to wait for the query to complete by calling the getQueryResults method until the jobComplete field in the getQueryResults response is true. |
| `destinationEncryptionConfiguration` | `object (EncryptionConfiguration)`  Optional. Custom encryption configuration (e.g., Cloud KMS keys) |
| `dryRun` | `boolean`  Optional. If set to true, BigQuery doesn't run the job. Instead, if the query is valid, BigQuery returns statistics about the job such as how many bytes would be processed. If the query is invalid, an error returns. The default value is false. |
| `preserveNull` |