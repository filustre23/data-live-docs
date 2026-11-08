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
| ``` {   "kind": string,   "schema": {     object (TableSchema)   },   "jobReference": {     object (JobReference)   },   "jobCreationReason": {     object (JobCreationReason)   },   "queryId": string,   "location": string,   "totalRows": string,   "pageToken": string,   "rows": [     {       object     }   ],   "totalBytesProcessed": string,   "jobComplete": boolean,   "errors": [     {       object (ErrorProto)     }   ],   "cacheHit": boolean,   "numDmlAffectedRows": string,   "sessionInfo": {     object (SessionInfo)   },   "dmlStats": {     object (DmlStats)   },   "pageRowCount": string,   "statementType": string,   "totalBytesBilled": string,   "totalSlotMs": string,   "creationTime": string,   "startTime": string,   "endTime": string,    // The following is a list of mutually exclusive fields. At most one of the   // fields will be set in a response:   "arrowSchema": {     object (ArrowSchema)   }   // End of mutually exclusive fields.    // The following is a list of mutually exclusive fields. At most one of the   // fields will be set in a response:   "arrowRecordBatch": {     object (ArrowRecordBatch)   }   // End of mutually exclusive fields. } ``` |

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
| `statementType` | `string`  Output only. The type of query statement, if valid. Possible values:   * `SELECT`: [`SELECT`](https://cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax#select_list) statement. * `ASSERT`: [`ASSERT`](https://cloud.google.com/bigquery/docs/reference/standard-sql/debugging-statements#assert) statement. * `INSERT`: [`INSERT`](https://cloud.google.com/bigquery/docs/reference/standard-sql/dml-syntax#insert_statement) statement. * `UPDATE`: [`UPDATE`](https://cloud.google.com/bigquery/docs/reference/standard-sql/dml-syntax#update_statement) statement. * `DELETE`: [`DELETE`](https://cloud.google.com/bigquery/docs/reference/standard-sql/data-manipulation-language) statement. * `MERGE`: [`MERGE`](https://cloud.google.com/bigquery/docs/reference/standard-sql/data-manipulation-language) statement. * `TRUNCATE_TABLE`: [`TRUNCATE   TABLE`](https://cloud.google.com/bigquery/docs/reference/standard-sql/dml-syntax#truncate_table_statement) statement. * `CREATE_TABLE`: [`CREATE   TABLE`](https://cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language#create_table_statement) statement, without `AS SELECT`. * `CREATE_TABLE_AS_SELECT`: [`CREATE TABLE AS   SELECT`](https://cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language#create_table_statement) statement. * `CREATE_VIEW`: [`CREATE   VIEW`](https://cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language#create_view_statement) statement. * `CREATE_MODEL`: [`CREATE   MODEL`](https://cloud.google.com/bigquery-ml/docs/reference/standard-sql/bigqueryml-syntax-create#create_model_statement) statement. * `CREATE_MATERIALIZED_VIEW`: [`CREATE MATERIALIZED   VIEW`](https://cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language#create_materialized_view_statement) statement. * `CREATE_FUNCTION`: [`CREATE   FUNCTION`](https://cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language#create_function_statement) statement. * `CREATE_TABLE_FUNCTION`: [`CREATE TABLE   FUNCTION`](https://cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language#create_table_function_statement) statement. * `CREATE_PROCEDURE`: [`CREATE   PROCEDURE`](https://cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language#create_procedure) statement. * `CREATE_ROW_ACCESS_POLICY`: [`CREATE ROW ACCESS   POLICY`](https://cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language#create_row_access_policy_statement) statement. * `CREATE_SCHEMA`: [`CREATE   SCHEMA`](https://cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language#create_schema_statement) statement. * `CREATE_EXTERNAL_SCHEMA`: [`CREATE EXTERNAL   SCHEMA`](https://cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language#create_external_schema_statement) statement. * `CREATE_EXTERNAL_TABLE`: [`CREATE EXTERNAL   TABLE`](https://cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language#create_external_table_statement) statement. * `CREATE_SNAPSHOT_TABLE`: [`CREATE SNAPSHOT   TABLE`](https://cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language#create_snapshot_table_statement) statement. * `CREATE_SEARCH_INDEX`: [`CREATE SEARCH   INDEX`](https://cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language#create_search_index_statement) statement. * `CREATE_VECTOR_INDEX`: [`CREATE VECTOR   INDEX`](https://cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language#create_vector_index_statement) statement. * `CREATE_CONNECTION`: [`CREATE   CONNECTION`](https://cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language#create_connection_statement) statement. * `CREATE_DATA_POLICY`: [`CREATE   DATA_POLICY`](https://cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language#create_data_policy_statement) statement. * `CREATE_PROPERTY_GRAPH`: [`CREATE PROPERTY   GRAPH`](https://cloud.google.com/bigquery/docs/reference/standard-sql/graph-schema-statements#gql_create_graph) statement. * `CREATE_CAPACITY`: [`CREATE   CAPACITY`](https://cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language#create_capacity_statement) statement. * `CREATE_RESERVATION`: [`CREATE   RESERVATION`](https://cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language#create_reservation_statement) statement. * `CREATE_ASSIGNMENT`: [`CREATE   ASSIGNMENT`](https://cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language#create_assignment_statement) statement. * `DROP_TABLE`: [`DROP   TABLE`](https://cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language#drop_table_statement) statement. * `DROP_EXTERNAL_TABLE`: [`DROP EXTERNAL   TABLE`](https://cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language#drop_external_table_statement) statement. * `DROP_VIEW`: [`DROP   VIEW`](https://cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language#drop_view_statement) statement. * `DROP_MODEL`: [`DROP   MODEL`](https://cloud.google.com/bigquery-ml/docs/reference/standard-sql/bigqueryml-syntax-drop-model) statement. * `DROP_MATERIALIZED_VIEW`: [`DROP MATERIALIZED   VIEW`](https://cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language#drop_materialized_view_statement) statement. * `DROP_FUNCTION`: [`DROP   FUNCTION`](https://cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language#drop_function_statement) statement. * `DROP_TABLE_FUNCTION`: [`DROP TABLE   FUNCTION`](https://cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language#drop_table_function) statement. * `DROP_PROCEDURE`: [`DROP   PROCEDURE`](https://cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language#drop_procedure_statement) statement. * `DROP_SEARCH_INDEX`: [`DROP SEARCH   INDEX`](https://cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language#drop_search_index) statement. * `DROP_VECTOR_INDEX`: [`DROP VECTOR   INDEX`](https://cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language#drop_vector_index) statement. * `DROP_SCHEMA`: [`DROP   SCHEMA`](https://cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language#drop_schema_statement) statement. * `UNDROP_SCHEMA`: [`UNDROP   SCHEMA`](https://cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language#undrop_schema_statement) statement. * `DROP_SNAPSHOT_TABLE`: [`DROP SNAPSHOT   TABLE`](https://cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language#drop_snapshot_table_statement) statement. * `DROP_ROW_ACCESS_POLICY`: [`DROP [ALL] ROW ACCESS   POLICY|POLICIES`](https://cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language#drop_row_access_policy_statement) statement. * `DROP_CONNECTION`: [`DROP   CONNECTION`](https://cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language#drop_connection_statement) statement. * `DROP_DATA_POLICY`: [`DROP   DATA_POLICY`](https://cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language#drop_data_policy) statement. * `DROP_PROPERTY_GRAPH`: [`DROP PROPERTY   GRAPH`](https://cloud.google.com/bigquery/docs/reference/standard-sql/graph-schema-statements#gql_drop_graph) statement. * `DROP_CAPACITY`: [`DROP   CAPACITY`](https://cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language#drop_capacity_statement) statement. * `DROP_RESERVATION`: [`DROP   RESERVATION`](https://cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language#drop_reservation_statement) statement. * `DROP_ASSIGNMENT`: [`DROP   ASSIGNMENT`](https://cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language#drop_assignment_statement) statement. * `ALTER_TABLE`: [`ALTER   TABLE`](https://cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language#alter_table_set_options_statement) statement. * `ALTER_VIEW`: [`ALTER   VIEW`](https://cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language#alter_view_set_options_statement) statement. * `ALTER_MATERIALIZED_VIEW`: [`ALTER MATERIALIZED   VIEW`](https://cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language#alter_materialized_view_set_options_statement) statement. * `ALTER_SCHEMA`: [`ALTER   SCHEMA`](https://cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language#alter_schema_set_options_statement) statement. * `ALTER_MODEL`: [`ALTER   MODEL`](https://cloud.google.com/bigquery-ml/docs/reference/standard-sql/bigqueryml-syntax-alter-model) statement. * `ALTER_SEARCH_INDEX`: [`ALTER SEARCH`](https://cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language#alter_search_index_statement) |