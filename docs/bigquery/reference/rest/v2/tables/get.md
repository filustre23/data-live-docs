* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback

# Method: tables.get Stay organized with collections Save and categorize content based on your preferences.

* [HTTP request](#body.HTTP_TEMPLATE)
* [Path parameters](#body.PATH_PARAMETERS)
* [Query parameters](#body.QUERY_PARAMETERS)
* [Request body](#body.request_body)
* [Response body](#body.response_body)
* [Authorization scopes](#body.aspect)
* [TableMetadataView](#TableMetadataView)
* [Try it!](#try-it)

Gets the specified table resource by table ID. This method does not return the data in the table, it only returns the table resource, which describes the structure of this table.

### HTTP request

`GET https://bigquery.googleapis.com/bigquery/v2/projects/{projectId}/datasets/{datasetId}/tables/{tableId}`

The URL uses [gRPC Transcoding](https://google.aip.dev/127) syntax.

### Path parameters

| Parameters | |
| --- | --- |
| `projectId` | `string`  Required. Project ID of the requested table |
| `datasetId` | `string`  Required. Dataset ID of the requested table |
| `tableId` | `string`  Required. Table ID of the requested table |

### Query parameters

| Parameters | |
| --- | --- |
| `selectedFields` | `string`  tabledata.list of table schema fields to return (comma-separated). If unspecified, all fields are returned. A fieldMask cannot be used here because the fields will automatically be converted from camelCase to snake\_case and the conversion will fail if there are underscores. Since these are fields in BigQuery table schemas, underscores are allowed. |
| `view` | `enum (TableMetadataView)`  Optional. Specifies the view that determines which table information is returned. By default, basic table information and storage statistics (STORAGE\_STATS) are returned. |

### Request body

The request body must be empty.

### Response body

If successful, the response body contains an instance of `Table`.

### Authorization scopes

Requires one of the following OAuth scopes:

* `https://www.googleapis.com/auth/bigquery`
* `https://www.googleapis.com/auth/cloud-platform`
* `https://www.googleapis.com/auth/bigquery.readonly`
* `https://www.googleapis.com/auth/cloud-platform.read-only`

For more information, see the [Authentication Overview](/docs/authentication#authorization-gcp).

## TableMetadataView

TableMetadataView specifies which table information is returned.

| Enums | |
| --- | --- |
| `TABLE_METADATA_VIEW_UNSPECIFIED` | The default value. Default to the STORAGE\_STATS view. |
| `BASIC` | Includes basic table information including schema and partitioning specification. This view does not include storage statistics such as numRows or numBytes. This view is significantly more efficient and should be used to support high query rates. |
| `STORAGE_STATS` | Includes all information in the BASIC view as well as storage statistics (numBytes, numLongTermBytes, numRows and lastModifiedTime). |
| `FULL` | Includes all table information, including storage statistics. It returns same information as STORAGE\_STATS view, but may contain additional information in the future. |




Send feedback

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2025-07-02 UTC.




Need to tell us more?

[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Hard to understand","hardToUnderstand","thumb-down"],["Incorrect information or sample code","incorrectInformationOrSampleCode","thumb-down"],["Missing the information/samples I need","missingTheInformationSamplesINeed","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2025-07-02 UTC."],[],[]]