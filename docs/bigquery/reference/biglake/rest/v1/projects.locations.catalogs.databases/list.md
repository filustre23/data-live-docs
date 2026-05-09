As of April 20th, 2026, BigLake is now called Lakehouse for Apache Iceberg. BigLake metastore is now called the Lakehouse runtime catalog. Lakehouse APIs, client libraries, CLI commands, and IAM names remain unchanged and still reference BigLake.

* [Home](https://docs.cloud.google.com/)
* [BigLake API](https://docs.cloud.google.com/lakehouse/docs)

# Method: projects.locations.catalogs.databases.list Stay organized with collections Save and categorize content based on your preferences.

* [HTTP request](#body.HTTP_TEMPLATE)
* [Path parameters](#body.PATH_PARAMETERS)
* [Query parameters](#body.QUERY_PARAMETERS)
* [Request body](#body.request_body)
* [Response body](#body.response_body)
  + [JSON representation](#body.ListDatabasesResponse.SCHEMA_REPRESENTATION)
* [Authorization scopes](#body.aspect)
* [IAM Permissions](#body.aspect_1)
* [Try it!](#try-it)

List all databases in a specified catalog.

### HTTP request

`GET https://biglake.googleapis.com/v1/{parent=projects/*/locations/*/catalogs/*}/databases`

The URL uses [gRPC Transcoding](https://google.aip.dev/127) syntax.

### Path parameters

| Parameters | |
| --- | --- |
| `parent` | `string`  Required. The parent, which owns this collection of databases. Format: projects/{project\_id\_or\_number}/locations/{locationId}/catalogs/{catalogId} |

### Query parameters

| Parameters | |
| --- | --- |
| `pageSize` | `integer`  The maximum number of databases to return. The service may return fewer than this value. If unspecified, at most 50 databases will be returned. The maximum value is 1000; values above 1000 will be coerced to 1000. |
| `pageToken` | `string`  A page token, received from a previous `databases.list` call. Provide this to retrieve the subsequent page.  When paginating, all other parameters provided to `databases.list` must match the call that provided the page token. |

### Request body

The request body must be empty.

### Response body

Response message for the databases.list method.

If successful, the response body contains data with the following structure:

| JSON representation |
| --- |
| ``` {   "databases": [     {       object (Database)     }   ],   "nextPageToken": string } ``` |

| Fields | |
| --- | --- |
| `databases[]` | `object (Database)`  The databases from the specified catalog. |
| `nextPageToken` | `string`  A token, which can be sent as `pageToken` to retrieve the next page. If this field is omitted, there are no subsequent pages. |

### Authorization scopes

Requires one of the following OAuth scopes:

* `https://www.googleapis.com/auth/bigquery`
* `https://www.googleapis.com/auth/cloud-platform`

For more information, see the [Authentication Overview](/docs/authentication#authorization-gcp).

### IAM Permissions

Requires the following [IAM](https://cloud.google.com/iam/docs) permission on the `parent` resource:

* `biglake.databases.list`

For more information, see the [IAM documentation](https://cloud.google.com/iam/docs).

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2026-04-21 UTC.




[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Hard to understand","hardToUnderstand","thumb-down"],["Incorrect information or sample code","incorrectInformationOrSampleCode","thumb-down"],["Missing the information/samples I need","missingTheInformationSamplesINeed","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2026-04-21 UTC."],[],[]]