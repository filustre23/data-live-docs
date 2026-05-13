* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback

# Method: transferConfigs.list Stay organized with collections Save and categorize content based on your preferences.

* [HTTP request](#body.HTTP_TEMPLATE)
* [Path parameters](#body.PATH_PARAMETERS)
* [Query parameters](#body.QUERY_PARAMETERS)
* [Request body](#body.request_body)
* [Response body](#body.response_body)
* [Authorization scopes](#body.aspect)
* [Try it!](#try-it)

**Full name**: projects.transferConfigs.list

Returns information about all transfer configs owned by a project in the specified location.

### HTTP request

Choose a location:

global asia-south1 asia-south2 europe-west1 europe-west2 europe-west3 europe-west4 europe-west6 europe-west8 europe-west9 me-central2 northamerica-northeast1 northamerica-northeast2 us-central1 us-central2 us-east1 us-east4 us-east5 us-east7 us-south1 us-west1 us-west2 us-west3 us-west4 us-west8

`GET https://bigquerydatatransfer.googleapis.com/v1/{parent=projects/*}/transferConfigs`

The URLs use [gRPC Transcoding](https://google.aip.dev/127) syntax.

### Path parameters

| Parameters | |
| --- | --- |
| `parent` | `string`  Required. The BigQuery project id for which transfer configs should be returned. If you are using the regionless method, the location must be `US` and `parent` should be in the following form:   * `projects/{projectId}   If you are using the regionalized method, `parent` should be in the following form:   * `projects/{projectId}/locations/{locationId}`   Authorization requires the following [IAM](https://cloud.google.com/iam/docs/) permission on the specified resource `parent`:   * `bigquery.transfers.get` |

### Query parameters

| Parameters | |
| --- | --- |
| `dataSourceIds[]` | `string`  When specified, only configurations of requested data sources are returned. |
| `pageToken` | `string`  Pagination token, which can be used to request a specific page of `ListTransfersRequest` list results. For multiple-page results, `ListTransfersResponse` outputs a `next_page` token, which can be used as the `pageToken` value to request the next page of list results. |
| `pageSize` | `integer`  Page size. The default page size is the maximum value of 1000 results. |

### Request body

The request body must be empty.

### Response body

If successful, the response body contains an instance of `ListTransferConfigsResponse`.

### Authorization scopes

Requires the following OAuth scope:

* `https://www.googleapis.com/auth/cloud-platform`

For more information, see the [Authentication Overview](/docs/authentication#authorization-gcp).




Send feedback

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2026-05-12 UTC.




Need to tell us more?

[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Hard to understand","hardToUnderstand","thumb-down"],["Incorrect information or sample code","incorrectInformationOrSampleCode","thumb-down"],["Missing the information/samples I need","missingTheInformationSamplesINeed","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2026-05-12 UTC."],[],[]]