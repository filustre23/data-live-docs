* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback

# Method: locations.list Stay organized with collections Save and categorize content based on your preferences.

* [HTTP request](#body.HTTP_TEMPLATE)
* [Path parameters](#body.PATH_PARAMETERS)
* [Query parameters](#body.QUERY_PARAMETERS)
* [Request body](#body.request_body)
* [Response body](#body.response_body)
  + [JSON representation](#body.ListLocationsResponse.SCHEMA_REPRESENTATION)
* [Authorization scopes](#body.aspect)
* [Try it!](#try-it)

**Full name**: projects.locations.list

Lists information about the supported locations for this service.

This method lists locations based on the resource scope provided in the `ListLocationsRequest.name` field:

* **Global locations**: If `name` is empty, the method lists the public locations available to all projects.
* **Project-specific locations**: If `name` follows the format `projects/{project}`, the method lists locations visible to that specific project. This includes public, private, or other project-specific locations enabled for the project.

For gRPC and client library implementations, the resource name is passed as the `name` field. For direct service calls, the resource name is incorporated into the request path based on the specific service implementation and version.

### HTTP request

Choose a location:

global asia-south1 asia-south2 europe-west1 europe-west2 europe-west3 europe-west4 europe-west6 europe-west8 europe-west9 me-central2 northamerica-northeast1 northamerica-northeast2 us-central1 us-central2 us-east1 us-east4 us-east5 us-east7 us-south1 us-west1 us-west2 us-west3 us-west4 us-west8

`GET https://bigquerydatatransfer.googleapis.com/v1/{name=projects/*}/locations`

The URLs use [gRPC Transcoding](https://google.aip.dev/127) syntax.

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
| `extraLocationTypes[]` | `string`  Optional. Do not use this field unless explicitly documented otherwise. This is primarily for internal usage. |

### Request body

The request body must be empty.

### Response body

The response message for `Locations.ListLocations`.

If successful, the response body contains data with the following structure:

| JSON representation |
| --- |
| ``` {   "locations": [     {       object (Location)     }   ],   "nextPageToken": string } ``` |

| Fields | |
| --- | --- |
| `locations[]` | `object (Location)`  A list of locations that matches the specified filter in the request. |
| `nextPageToken` | `string`  The standard List next-page token. |

### Authorization scopes

Requires the following OAuth scope:

* `https://www.googleapis.com/auth/cloud-platform`

For more information, see the [Authentication Overview](/docs/authentication#authorization-gcp).




Send feedback

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2026-05-12 UTC.




Need to tell us more?

[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Hard to understand","hardToUnderstand","thumb-down"],["Incorrect information or sample code","incorrectInformationOrSampleCode","thumb-down"],["Missing the information/samples I need","missingTheInformationSamplesINeed","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2026-05-12 UTC."],[],[]]