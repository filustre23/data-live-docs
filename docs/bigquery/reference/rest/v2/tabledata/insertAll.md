* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback

# Method: tabledata.insertAll Stay organized with collections Save and categorize content based on your preferences.

* [HTTP request](#body.HTTP_TEMPLATE)
* [Path parameters](#body.PATH_PARAMETERS)
* [Request body](#body.request_body)
  + [JSON representation](#body.request_body.SCHEMA_REPRESENTATION)
* [Response body](#body.response_body)
  + [JSON representation](#body.TableDataInsertAllResponse.SCHEMA_REPRESENTATION)
* [Authorization scopes](#body.aspect)
* [Try it!](#try-it)

Streams data into BigQuery one record at a time without needing to run a load job.

### HTTP request

`POST https://bigquery.googleapis.com/bigquery/v2/projects/{projectId}/datasets/{datasetId}/tables/{tableId}/insertAll`

The URL uses [gRPC Transcoding](https://google.aip.dev/127) syntax.

### Path parameters

| Parameters | |
| --- | --- |
| `projectId` | `string`  Required. Project ID of the destination. |
| `datasetId` | `string`  Required. Dataset ID of the destination. |
| `tableId` | `string`  Required. Table ID of the destination. |

### Request body

The request body contains data with the following structure:

| JSON representation |
| --- |
| ``` {   "kind": string,   "skipInvalidRows": boolean,   "ignoreUnknownValues": boolean,   "templateSuffix": string,   "rows": [     {       "insertId": string,       "json": {         object       }     }   ],   "traceId": string } ``` |

| Fields | |
| --- | --- |
| `kind` | `string`  Optional. The resource type of the response. The value is not checked at the backend. Historically, it has been set to "bigquery#tableDataInsertAllRequest" but you are not required to set it. |
| `skipInvalidRows` | `boolean`  Optional. Insert all valid rows of a request, even if invalid rows exist. The default value is false, which causes the entire request to fail if any invalid rows exist. |
| `ignoreUnknownValues` | `boolean`  Optional. Accept rows that contain values that do not match the schema. The unknown values are ignored. Default is false, which treats unknown values as errors. |
| `templateSuffix` | `string`  Optional. If specified, treats the destination table as a base template, and inserts the rows into an instance table named "{destination}{templateSuffix}". BigQuery will manage creation of the instance table, using the schema of the base template table.  See <https://cloud.google.com/bigquery/streaming-data-into-bigquery#template-tables> for considerations when working with templates tables. |
| `rows[]` | `object` |
| `rows[].insertId` | `string`  Insertion ID for best-effort deduplication. This feature is not recommended, and users seeking stronger insertion semantics are encouraged to use other mechanisms such as the BigQuery Write API. |
| `rows[].json` | `object (Struct format)`  Data for a single row. |
| `traceId` | `string`  Optional. Unique request trace id. Used for debugging purposes only. It is case-sensitive, limited to up to 36 ASCII characters. A UUID is recommended. |

### Response body

Describes the format of a streaming insert response.

If successful, the response body contains data with the following structure:

| JSON representation |
| --- |
| ``` {   "kind": string,   "insertErrors": [     {       "index": integer,       "errors": [         {           object (ErrorProto)         }       ]     }   ] } ``` |

| Fields | |
| --- | --- |
| `kind` | `string`  Returns "bigquery#tableDataInsertAllResponse". |
| `insertErrors[]` | `object`  Describes specific errors encountered while processing the request. |
| `insertErrors[].index` | `integer (uint32 format)`  The index of the row that error applies to. |
| `insertErrors[].errors[]` | `object (ErrorProto)`  Error information for the row indicated by the index property. |

### Authorization scopes

Requires one of the following OAuth scopes:

* `https://www.googleapis.com/auth/bigquery`
* `https://www.googleapis.com/auth/cloud-platform`
* `https://www.googleapis.com/auth/bigquery.insertdata`

For more information, see the [Authentication Overview](/docs/authentication#authorization-gcp).




Send feedback

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2025-07-02 UTC.




Need to tell us more?

[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Hard to understand","hardToUnderstand","thumb-down"],["Incorrect information or sample code","incorrectInformationOrSampleCode","thumb-down"],["Missing the information/samples I need","missingTheInformationSamplesINeed","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2025-07-02 UTC."],[],[]]