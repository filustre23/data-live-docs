* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback

# Method: projects.locations.dataExchanges.subscribe Stay organized with collections Save and categorize content based on your preferences.

* [HTTP request](#body.HTTP_TEMPLATE)
* [Path parameters](#body.PATH_PARAMETERS)
* [Request body](#body.request_body)
  + [JSON representation](#body.request_body.SCHEMA_REPRESENTATION)
* [Response body](#body.response_body)
* [Authorization scopes](#body.aspect)
* [IAM Permissions](#body.aspect_1)
* [Try it!](#try-it)

Creates a Subscription to a Data Clean Room. This is a long-running operation as it will create one or more linked datasets. Throws a Bad Request error if the Data Exchange does not contain any listings.

### HTTP request

`POST https://analyticshub.googleapis.com/v1/{name=projects/*/locations/*/dataExchanges/*}:subscribe`

The URL uses [gRPC Transcoding](https://google.aip.dev/127) syntax.

### Path parameters

| Parameters | |
| --- | --- |
| `name` | `string`  Required. Resource name of the Data Exchange. e.g. `projects/publisherproject/locations/us/dataExchanges/123` |

### Request body

The request body contains data with the following structure:

| JSON representation |
| --- |
| ``` {   "destination": string,   "destinationDataset": {     object (DestinationDataset)   },   "subscription": string,   "subscriberContact": string } ``` |

| Fields | |
| --- | --- |
| `destination` | `string`  Required. The parent resource path of the Subscription. e.g. `projects/subscriberproject/locations/us` |
| `destinationDataset` | `object (DestinationDataset)`  Optional. BigQuery destination dataset to create for the subscriber. |
| `subscription` | `string`  Required. Name of the subscription to create. e.g. `subscription1` |
| `subscriberContact` | `string`  Email of the subscriber. |

### Response body

If successful, the response body contains an instance of `Operation`.

### Authorization scopes

Requires one of the following OAuth scopes:

* `https://www.googleapis.com/auth/bigquery`
* `https://www.googleapis.com/auth/cloud-platform`

For more information, see the [Authentication Overview](/docs/authentication#authorization-gcp).

### IAM Permissions

Requires the following [IAM](https://cloud.google.com/iam/docs) permission on the `destination` resource:

* `analyticshub.subscriptions.create`

Requires the following [IAM](https://cloud.google.com/iam/docs) permission on the `name` resource:

* `analyticshub.dataExchanges.subscribe`

For more information, see the [IAM documentation](https://cloud.google.com/iam/docs).




Send feedback

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2025-07-02 UTC.




Need to tell us more?

[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Hard to understand","hardToUnderstand","thumb-down"],["Incorrect information or sample code","incorrectInformationOrSampleCode","thumb-down"],["Missing the information/samples I need","missingTheInformationSamplesINeed","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2025-07-02 UTC."],[],[]]