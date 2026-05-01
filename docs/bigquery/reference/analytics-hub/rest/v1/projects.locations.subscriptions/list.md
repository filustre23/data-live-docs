* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback

# Method: projects.locations.subscriptions.list Stay organized with collections Save and categorize content based on your preferences.

* [HTTP request](#body.HTTP_TEMPLATE)
* [Path parameters](#body.PATH_PARAMETERS)
* [Query parameters](#body.QUERY_PARAMETERS)
* [Request body](#body.request_body)
* [Response body](#body.response_body)
  + [JSON representation](#body.ListSubscriptionsResponse.SCHEMA_REPRESENTATION)
* [Authorization scopes](#body.aspect)
* [IAM Permissions](#body.aspect_1)
* [Try it!](#try-it)

Lists all subscriptions in a given project and location.

### HTTP request

`GET https://analyticshub.googleapis.com/v1/{parent=projects/*/locations/*}/subscriptions`

The URL uses [gRPC Transcoding](https://google.aip.dev/127) syntax.

### Path parameters

| Parameters | |
| --- | --- |
| `parent` | `string`  Required. The parent resource path of the subscription. e.g. projects/myproject/locations/us |

### Query parameters

| Parameters | |
| --- | --- |
| `filter` | `string`  An expression for filtering the results of the request. Eligible fields for filtering are:   * `listing` * `dataExchange`   Alternatively, a literal wrapped in double quotes may be provided. This will be checked for an exact match against both fields above.  In all cases, the full Data Exchange or Listing resource name must be provided. Some example of using filters:   * dataExchange="projects/myproject/locations/us/dataExchanges/123" * listing="projects/123/locations/us/dataExchanges/456/listings/789" * "projects/myproject/locations/us/dataExchanges/123" |
| `pageSize` | `integer`  The maximum number of results to return in a single response page. |
| `pageToken` | `string`  Page token, returned by a previous call. |

### Request body

The request body must be empty.

### Response body

Message for response to the listing of subscriptions.

If successful, the response body contains data with the following structure:

| JSON representation |
| --- |
| ``` {   "subscriptions": [     {       object (Subscription)     }   ],   "nextPageToken": string } ``` |

| Fields | |
| --- | --- |
| `subscriptions[]` | `object (Subscription)`  The list of subscriptions. |
| `nextPageToken` | `string`  Next page token. |

### Authorization scopes

Requires one of the following OAuth scopes:

* `https://www.googleapis.com/auth/bigquery`
* `https://www.googleapis.com/auth/cloud-platform`

For more information, see the [Authentication Overview](/docs/authentication#authorization-gcp).

### IAM Permissions

Requires the following [IAM](https://cloud.google.com/iam/docs) permission on the `parent` resource:

* `analyticshub.subscriptions.list`

For more information, see the [IAM documentation](https://cloud.google.com/iam/docs).




Send feedback

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2025-07-02 UTC.




Need to tell us more?

[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Hard to understand","hardToUnderstand","thumb-down"],["Incorrect information or sample code","incorrectInformationOrSampleCode","thumb-down"],["Missing the information/samples I need","missingTheInformationSamplesINeed","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2025-07-02 UTC."],[],[]]