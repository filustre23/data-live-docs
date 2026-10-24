* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback

# AuditData Stay organized with collections Save and categorize content based on your preferences.

* [JSON representation](#SCHEMA_REPRESENTATION)
* [TableInsertRequest](#TableInsertRequest)
  + [JSON representation](#TableInsertRequest.SCHEMA_REPRESENTATION)
* [Table](#Table)
  + [JSON representation](#Table.SCHEMA_REPRESENTATION)
* [TableName](#TableName)
  + [JSON representation](#TableName.SCHEMA_REPRESENTATION)
* [TableInfo](#TableInfo)
  + [JSON representation](#TableInfo.SCHEMA_REPRESENTATION)
* [TableViewDefinition](#TableViewDefinition)
  + [JSON representation](#TableViewDefinition.SCHEMA_REPRESENTATION)
* [EncryptionInfo](#EncryptionInfo)
  + [JSON representation](#EncryptionInfo.SCHEMA_REPRESENTATION)
* [TableUpdateRequest](#TableUpdateRequest)
  + [JSON representation](#TableUpdateRequest.SCHEMA_REPRESENTATION)
* [DatasetListRequest](#DatasetListRequest)
  + [JSON representation](#DatasetListRequest.SCHEMA_REPRESENTATION)
* [DatasetInsertRequest](#DatasetInsertRequest)
  + [JSON representation](#DatasetInsertRequest.SCHEMA_REPRESENTATION)
* [Dataset](#Dataset)
  + [JSON representation](#Dataset.SCHEMA_REPRESENTATION)
* [DatasetName](#DatasetName)
  + [JSON representation](#DatasetName.SCHEMA_REPRESENTATION)
* [DatasetInfo](#DatasetInfo)
  + [JSON representation](#DatasetInfo.SCHEMA_REPRESENTATION)
* [BigQueryAcl](#BigQueryAcl)
  + [JSON representation](#BigQueryAcl.SCHEMA_REPRESENTATION)
* [BigQueryAcl.Entry](#BigQueryAcl.Entry)
  + [JSON representation](#BigQueryAcl.Entry.SCHEMA_REPRESENTATION)
* [DatasetUpdateRequest](#DatasetUpdateRequest)
  + [JSON representation](#DatasetUpdateRequest.SCHEMA_REPRESENTATION)
* [JobInsertRequest](#JobInsertRequest)
  + [JSON representation](#JobInsertRequest.SCHEMA_REPRESENTATION)
* [Job](#Job)
  + [JSON representation](#Job.SCHEMA_REPRESENTATION)
* [JobName](#JobName)
  + [JSON representation](#JobName.SCHEMA_REPRESENTATION)
* [JobConfiguration](#JobConfiguration)
  + [JSON representation](#JobConfiguration.SCHEMA_REPRESENTATION)
* [JobConfiguration.Query](#JobConfiguration.Query)
  + [JSON representation](#JobConfiguration.Query.SCHEMA_REPRESENTATION)
* [TableDefinition](#TableDefinition)
  + [JSON representation](#TableDefinition.SCHEMA_REPRESENTATION)
* [SecureContextValue](#SecureContextValue)
  + [JSON representation](#SecureContextValue.SCHEMA_REPRESENTATION)
* [JobConfiguration.Load](#JobConfiguration.Load)
  + [JSON representation](#JobConfiguration.Load.SCHEMA_REPRESENTATION)
* [JobConfiguration.Extract](#JobConfiguration.Extract)
  + [JSON representation](#JobConfiguration.Extract.SCHEMA_REPRESENTATION)
* [JobConfiguration.TableCopy](#JobConfiguration.TableCopy)
  + [JSON representation](#JobConfiguration.TableCopy.SCHEMA_REPRESENTATION)
* [JobStatus](#JobStatus)
  + [JSON representation](#JobStatus.SCHEMA_REPRESENTATION)
* [JobStatistics](#JobStatistics)
  + [JSON representation](#JobStatistics.SCHEMA_REPRESENTATION)
* [JobStatistics.ReservationResourceUsage](#JobStatistics.ReservationResourceUsage)
  + [JSON representation](#JobStatistics.ReservationResourceUsage.SCHEMA_REPRESENTATION)
* [JobQueryRequest](#JobQueryRequest)
  + [JSON representation](#JobQueryRequest.SCHEMA_REPRESENTATION)
* [JobGetQueryResultsRequest](#JobGetQueryResultsRequest)
  + [JSON representation](#JobGetQueryResultsRequest.SCHEMA_REPRESENTATION)
* [TableDataListRequest](#TableDataListRequest)
  + [JSON representation](#TableDataListRequest.SCHEMA_REPRESENTATION)
* [SetIamPolicyRequest](#SetIamPolicyRequest)
  + [JSON representation](#SetIamPolicyRequest.SCHEMA_REPRESENTATION)
* [TableInsertResponse](#TableInsertResponse)
  + [JSON representation](#TableInsertResponse.SCHEMA_REPRESENTATION)
* [TableUpdateResponse](#TableUpdateResponse)
  + [JSON representation](#TableUpdateResponse.SCHEMA_REPRESENTATION)
* [DatasetInsertResponse](#DatasetInsertResponse)
  + [JSON representation](#DatasetInsertResponse.SCHEMA_REPRESENTATION)
* [DatasetUpdateResponse](#DatasetUpdateResponse)
  + [JSON representation](#DatasetUpdateResponse.SCHEMA_REPRESENTATION)
* [JobInsertResponse](#JobInsertResponse)
  + [JSON representation](#JobInsertResponse.SCHEMA_REPRESENTATION)
* [JobQueryResponse](#JobQueryResponse)
  + [JSON representation](#JobQueryResponse.SCHEMA_REPRESENTATION)
* [JobGetQueryResultsResponse](#JobGetQueryResultsResponse)
  + [JSON representation](#JobGetQueryResultsResponse.SCHEMA_REPRESENTATION)
* [JobQueryDoneResponse](#JobQueryDoneResponse)
  + [JSON representation](#JobQueryDoneResponse.SCHEMA_REPRESENTATION)
* [JobCompletedEvent](#JobCompletedEvent)
  + [JSON representation](#JobCompletedEvent.SCHEMA_REPRESENTATION)
* [TableDataReadEvent](#TableDataReadEvent)
  + [JSON representation](#TableDataReadEvent.SCHEMA_REPRESENTATION)

BigQuery AuditData represents the older AuditData.serviceData log messages.

| JSON representation |
| --- |
| ``` {   "jobCompletedEvent": {     object (JobCompletedEvent)   },   "tableDataReadEvents": [     {       object (TableDataReadEvent)     }   ],    // The following is a list of mutually exclusive fields. At most one of the   // fields will be set in a response:   "tableInsertRequest": {     object (TableInsertRequest)   },   "tableUpdateRequest": {     object (TableUpdateRequest)   },   "datasetListRequest": {     object (DatasetListRequest)   },   "datasetInsertRequest": {     object (DatasetInsertRequest)   },   "datasetUpdateRequest": {     object (DatasetUpdateRequest)   },   "jobInsertRequest": {     object (JobInsertRequest)   },   "jobQueryRequest": {     object (JobQueryRequest)   },   "jobGetQueryResultsRequest": {     object (JobGetQueryResultsRequest)   },   "tableDataListRequest": {     object (TableDataListRequest)   },   "setIamPolicyRequest": {     object (SetIamPolicyRequest)   }   // End of mutually exclusive fields.    // The following is a list of mutually exclusive fields. At most one of the   // fields will be set in a response:   "tableInsertResponse": {     object (TableInsertResponse)   },   "tableUpdateResponse": {     object (TableUpdateResponse)   },   "datasetInsertResponse": {     object (DatasetInsertResponse)   },   "datasetUpdateResponse": {     object (DatasetUpdateResponse)   },   "jobInsertResponse": {     object (JobInsertResponse)   },   "jobQueryResponse": {     object (JobQueryResponse)   },   "jobGetQueryResultsResponse": {     object (JobGetQueryResultsResponse)   },   "jobQueryDoneResponse": {     object (JobQueryDoneResponse)   },   "policyResponse": {     object (Policy)   }   // End of mutually exclusive fields. } ``` |

| Fields | |
| --- | --- |
| `jobCompletedEvent` | `object (JobCompletedEvent)`  A job completion event. |
| `tableDataReadEvents[]` | `object (TableDataReadEvent)`  Information about the table access events. |
| Request data for each BigQuery method. The following is a list of mutually exclusive fields. At most one of the fields will be set in a response: | |
| `tableInsertRequest` | `object (TableInsertRequest)`  Table insert request. |
| `tableUpdateRequest` | `object (TableUpdateRequest)`  Table update request. |
| `datasetListRequest` | `object (DatasetListRequest)`  Dataset list request. |
| `datasetInsertRequest` | `object (DatasetInsertRequest)`  Dataset insert request. |
| `datasetUpdateRequest` | `object (DatasetUpdateRequest)`  Dataset update request. |
| `jobInsertRequest` | `object (JobInsertRequest)`  Job insert request. |
| `jobQueryRequest` | `object (JobQueryRequest)`  Job query request. |
| `jobGetQueryResultsRequest` | `object (JobGetQueryResultsRequest)`  Job get query results request. |
| `tableDataListRequest` | `object (TableDataListRequest)`  Table data-list request. |
| `setIamPolicyRequest` | `object (SetIamPolicyRequest)`  Iam policy request. |
| End of mutually exclusive fields. | |
| Response data for each BigQuery method. The following is a list of mutually exclusive fields. At most one of the fields will be set in a response: | |
| `tableInsertResponse` | `object (TableInsertResponse)`  Table insert response. |
| `tableUpdateResponse` | `object (TableUpdateResponse)`  Table update response. |
| `datasetInsertResponse` | `object (DatasetInsertResponse)`  Dataset insert response. |
| `datasetUpdateResponse` | `object (DatasetUpdateResponse)`  Dataset update response. |
| `jobInsertResponse` | `object (JobInsertResponse)`  Job insert response. |
| `jobQueryResponse` | `object (JobQueryResponse)`  Job query response. |
| `jobGetQueryResultsResponse` | `object (JobGetQueryResultsResponse)`  Job get query results response. |
| `jobQueryDoneResponse` | `object (JobQueryDoneResponse)`  Deprecated: Job query-done response. Use this information for usage analysis. |
| `policyResponse` | `object (Policy)`  Iam Policy. |
| End of mutually exclusive fields. | |

## TableInsertRequest

Table insert request.

| JSON representation |
| --- |
| ``` {   "resource": {     object (Table)   } } ``` |

| Fields | |
| --- | --- |
| `resource` | `object (Table)`  The new table. |

## Table

Describes a BigQuery table. See the [Table](/bigquery/docs/reference/v2/tables) API resource for more details on individual fields. Note: `Table.schema` has been deprecated in favor of `Table.schemaJson`. `Table.schema` may continue to be present in your logs during this transition.

| JSON representation |
| --- |
| ``` {   "tableName": {     object (TableName)   },   "info": {     object (TableInfo)   },   "schemaJson": string,   "view": {     object (TableViewDefinition)   },   "expireTime": string,   "createTime": string,   "truncateTime": string,   "updateTime": string,   "encryption": {     object (EncryptionInfo)   } } ``` |

| Fields | |
| --- | --- |
| `tableName` | `object (TableName)`  The name of the table. |
| `info` | `object (TableInfo)`  User-provided metadata for the table. |
| `schemaJson` | `string`  A JSON representation of the table's schema. |
| `view` | `object (TableViewDefinition)`  If present, this is a virtual table defined by a SQL query. |
| `expireTime` | `string (Timestamp format)`  The expiration date for the table, after which the table is deleted and the storage reclaimed. If not present, the table persists indefinitely.  Uses RFC 3339, where generated output will always be Z-normalized and use 0, 3, 6 or 9 fractional digits. Offsets other than "Z" are also accepted. Examples: `"2014-10-02T15:01:23Z"`, `"2014-10-02T15:01:23.045123456Z"` or `"2014-10-02T15:01:23+05:30"`. |
| `createTime` | `string (Timestamp format)`  The time the table was created.  Uses RFC 3339, where generated output will always be Z-normalized and use 0, 3, 6 or 9 fractional digits. Offsets other than "Z" are also accepted. Examples: `"2014-10-02T15:01:23Z"`, `"2014-10-02T15:01:23.045123456Z"` or `"2014-10-02T15:01:23+05:30"`. |
| `truncateTime` | `string (Timestamp format)`  The time the table was last truncated by an operation with a `writeDisposition` of `WRITE_TRUNCATE`.  Uses RFC 3339, where generated output will always be Z-normalized and use 0, 3, 6 or 9 |