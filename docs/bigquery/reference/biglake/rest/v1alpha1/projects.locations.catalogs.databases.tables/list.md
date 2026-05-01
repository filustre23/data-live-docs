As of April 20th, 2026, BigLake is now called Google Cloud Lakehouse. BigLake metastore is now called the Lakehouse runtime catalog. Lakehouse APIs, client libraries, CLI commands, and IAM names remain unchanged and still reference BigLake.

* [Home](https://docs.cloud.google.com/)
* [BigLake API](https://docs.cloud.google.com/lakehouse/docs)
* [Technology areas](https://docs.cloud.google.com/docs)
* [Reference](https://docs.cloud.google.com/lakehouse/docs/quotas)

# Method: projects.locations.catalogs.databases.tables.list Stay organized with collections Save and categorize content based on your preferences.

* [HTTP request](#body.HTTP_TEMPLATE)
* [Path parameters](#body.PATH_PARAMETERS)
* [Query parameters](#body.QUERY_PARAMETERS)
* [Request body](#body.request_body)
* [Response body](#body.response_body)
  + [JSON representation](#body.ListTablesResponse.SCHEMA_REPRESENTATION)
* [Authorization scopes](#body.aspect)
* [IAM Permissions](#body.aspect_1)
* [TableView](#TableView)
* [Try it!](#try-it)

List all tables in a specified database.

### HTTP request

`GET https://biglake.googleapis.com/v1alpha1/{parent=projects/*/locations/*/catalogs/*/databases/*}/tables`

The URL uses [gRPC Transcoding](https://google.aip.dev/127) syntax.

### Path parameters

| Parameters | |
| --- | --- |
| `parent` | `string`  Required. The parent, which owns this collection of tables. Format: projects/{project\_id\_or\_number}/locations/{locationId}/catalogs/{catalogId}/databases/{databaseId} |

### Query parameters

| Parameters | |
| --- | --- |
| `pageSize` | `integer`  The maximum number of tables to return. The service may return fewer than this value. If unspecified, at most 50 tables will be returned. The maximum value is 1000; values above 1000 will be coerced to 1000. |
| `pageToken` | `string`  A page token, received from a previous `tables.list` call. Provide this to retrieve the subsequent page.  When paginating, all other parameters provided to `tables.list` must match the call that provided the page token. |
| `view` | `enum (TableView)`  The view for the returned tables. |

### Request body

The request body must be empty.

### Response body

Response message for the tables.list method.

If successful, the response body contains data with the following structure:

| JSON representation |
| --- |
| ``` {   "tables": [     {       object (Table)     }   ],   "nextPageToken": string } ``` |

| Fields | |
| --- | --- |
| `tables[]` | `object (Table)`  The tables from the specified database. |
| `nextPageToken` | `string`  A token, which can be sent as `pageToken` to retrieve the next page. If this field is omitted, there are no subsequent pages. |

### Authorization scopes

Requires one of the following OAuth scopes:

* `https://www.googleapis.com/auth/bigquery`
* `https://www.googleapis.com/auth/cloud-platform`

For more information, see the [Authentication Overview](/docs/authentication#authorization-gcp).

### IAM Permissions

Requires the following [IAM](https://cloud.google.com/iam/docs) permission on the `parent` resource:

* `biglake.tables.list`

For more information, see the [IAM documentation](https://cloud.google.com/iam/docs).

## TableView

View on Table. Represents which fields will be populated for calls that return Table objects.

| Enums | |
| --- | --- |
| `TABLE_VIEW_UNSPECIFIED` | Default value. The API will default to the BASIC view. |
| `BASIC` | Include only table names. This is the default value. |
| `FULL` | Include everything. |

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2026-04-21 UTC.




[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Hard to understand","hardToUnderstand","thumb-down"],["Incorrect information or sample code","incorrectInformationOrSampleCode","thumb-down"],["Missing the information/samples I need","missingTheInformationSamplesINeed","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2026-04-21 UTC."],[],[]]