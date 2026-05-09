As of April 20th, 2026, BigLake is now called Lakehouse for Apache Iceberg. BigLake metastore is now called the Lakehouse runtime catalog. Lakehouse APIs, client libraries, CLI commands, and IAM names remain unchanged and still reference BigLake.

* [Home](https://docs.cloud.google.com/)
* [BigLake API](https://docs.cloud.google.com/lakehouse/docs)
* [Technology areas](https://docs.cloud.google.com/docs)
* [Reference](https://docs.cloud.google.com/lakehouse/docs/quotas)

# Method: projects.locations.catalogs.databases.tables.create Stay organized with collections Save and categorize content based on your preferences.

* [HTTP request](#body.HTTP_TEMPLATE)
* [Path parameters](#body.PATH_PARAMETERS)
* [Query parameters](#body.QUERY_PARAMETERS)
* [Request body](#body.request_body)
* [Response body](#body.response_body)
* [Authorization scopes](#body.aspect)
* [IAM Permissions](#body.aspect_1)
* [Try it!](#try-it)

Creates a new table.

### HTTP request

`POST https://biglake.googleapis.com/v1alpha1/{parent=projects/*/locations/*/catalogs/*/databases/*}/tables`

The URL uses [gRPC Transcoding](https://google.aip.dev/127) syntax.

### Path parameters

| Parameters | |
| --- | --- |
| `parent` | `string`  Required. The parent resource where this table will be created. Format: projects/{project\_id\_or\_number}/locations/{locationId}/catalogs/{catalogId}/databases/{databaseId} |

### Query parameters

| Parameters | |
| --- | --- |
| `tableId` | `string`  Required. The ID to use for the table, which will become the final component of the table's resource name. |

### Request body

The request body contains an instance of `Table`.

### Response body

If successful, the response body contains a newly created instance of `Table`.

### Authorization scopes

Requires one of the following OAuth scopes:

* `https://www.googleapis.com/auth/bigquery`
* `https://www.googleapis.com/auth/cloud-platform`

For more information, see the [Authentication Overview](/docs/authentication#authorization-gcp).

### IAM Permissions

Requires the following [IAM](https://cloud.google.com/iam/docs) permission on the `parent` resource:

* `biglake.tables.create`

For more information, see the [IAM documentation](https://cloud.google.com/iam/docs).

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2026-04-21 UTC.




[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Hard to understand","hardToUnderstand","thumb-down"],["Incorrect information or sample code","incorrectInformationOrSampleCode","thumb-down"],["Missing the information/samples I need","missingTheInformationSamplesINeed","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2026-04-21 UTC."],[],[]]