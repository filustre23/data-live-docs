* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback

# Method: tabledata.list Stay organized with collections Save and categorize content based on your preferences.

* [HTTP request](#body.HTTP_TEMPLATE)
* [Path parameters](#body.PATH_PARAMETERS)
* [Query parameters](#body.QUERY_PARAMETERS)
* [Request body](#body.request_body)
* [Response body](#body.response_body)
  + [JSON representation](#body.TableDataList.SCHEMA_REPRESENTATION)
* [Authorization scopes](#body.aspect)
* [Try it!](#try-it)

tabledata.list the content of a table in rows.

### HTTP request

`GET https://bigquery.googleapis.com/bigquery/v2/projects/{projectId}/datasets/{datasetId}/tables/{tableId}/data`

The URL uses [gRPC Transcoding](https://google.aip.dev/127) syntax.

### Path parameters

| Parameters | |
| --- | --- |
| `projectId` | `string`  Required. Project id of the table to list. |
| `datasetId` | `string`  Required. Dataset id of the table to list. |
| `tableId` | `string`  Required. Table id of the table to list. |

### Query parameters

| Parameters | |
| --- | --- |
| `startIndex` | `string`  Start row index of the table. |
| `maxResults` | `integer (uint32 format)`  Row limit of the table. |
| `pageToken` | `string`  To retrieve the next page of table data, set this field to the string provided in the pageToken field of the response body from your previous call to tabledata.list. |
| `selectedFields` | `string`  Subset of fields to return, supports select into sub fields. Example: selectedFields = "a,e.d.f"; |
| `formatOptions` | `object (DataFormatOptions)`  Output timestamp field value in usec int64 instead of double. Output format adjustments. |

### Request body

The request body must be empty.

### Response body

The response of a tabledata.list request.

If successful, the response body contains data with the following structure:

| JSON representation |
| --- |
| ``` {   "kind": string,   "etag": string,   "totalRows": string,   "pageToken": string,   "rows": [     {       object     }   ] } ``` |

| Fields | |
| --- | --- |
| `kind` | `string`  Will be set to "bigquery#tableDataList". |
| `etag` | `string`  Etag to the response. |
| `totalRows` | `string`  Total rows of the entire table. In order to show default value "0", we have to present it as string. |
| `pageToken` | `string`  When this field is non-empty, it indicates that additional results are available. To request the next page of data, set the pageToken field of your next tabledata.list call to the string returned in this field. |
| `rows[]` | `object (Struct format)`  Repeated rows as result. The REST-based representation of this data leverages a series of JSON f,v objects for indicating fields and values. |

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