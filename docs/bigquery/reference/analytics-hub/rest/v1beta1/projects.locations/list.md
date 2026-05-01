* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)

Send feedback

# Method: projects.locations.list Stay organized with collections Save and categorize content based on your preferences.

* [HTTP request](#body.HTTP_TEMPLATE)
* [Path parameters](#body.PATH_PARAMETERS)
* [Query parameters](#body.QUERY_PARAMETERS)
* [Request body](#body.request_body)
* [Response body](#body.response_body)
  + [JSON representation](#body.ListLocationsResponse.SCHEMA_REPRESENTATION)
* [Authorization Scopes](#body.aspect)
* [Try it!](#try-it)

Lists information about the supported locations for this service.

### HTTP request

`GET https://analyticshub.googleapis.com/v1beta1/{name=projects/*}/locations`

The URL uses [gRPC Transcoding](https://google.aip.dev/127) syntax.

### Path parameters

| Parameters | |
| --- | --- |
| `name` | `string`  The resource that owns the locations collection, if applicable. |

### Query parameters

| Parameters | |
| --- | --- |
| `filter` | `string`  A filter to narrow down results to a preferred subset. The filtering language accepts strings like `"displayName=tokyo"`, and is documented in more detail in [AIP-160](https://google.aip.dev/160). |
| `pageSize` | `integer`  The maximum number of results to return. If not set, the service selects a default. |
| `pageToken` | `string`  A page token received from the `nextPageToken` field in the response. Send that page token to receive the subsequent page. |

### Request body

The request body must be empty.

### Response body

If successful, the response body contains data with the following structure:

The response message for `Locations.ListLocations`.

| JSON representation |
| --- |
| ``` {   "locations": [     {       object (Location)     }   ],   "nextPageToken": string } ``` |

| Fields | |
| --- | --- |
| `locations[]` | `object (Location)`  A list of locations that matches the specified filter in the request. |
| `nextPageToken` | `string`  The standard List next-page token. |

### Authorization Scopes

Requires one of the following OAuth scopes:

* `https://www.googleapis.com/auth/bigquery`
* `https://www.googleapis.com/auth/cloud-platform`

For more information, see the [Authentication Overview](https://cloud.google.com/docs/authentication/).




Send feedback

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2025-07-02 UTC.




Need to tell us more?

[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Hard to understand","hardToUnderstand","thumb-down"],["Incorrect information or sample code","incorrectInformationOrSampleCode","thumb-down"],["Missing the information/samples I need","missingTheInformationSamplesINeed","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2025-07-02 UTC."],[],[]]