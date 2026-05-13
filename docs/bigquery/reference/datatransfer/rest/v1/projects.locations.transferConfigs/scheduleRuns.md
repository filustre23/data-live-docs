* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback

# Method: transferConfigs.scheduleRuns Stay organized with collections Save and categorize content based on your preferences.

* [HTTP request](#body.HTTP_TEMPLATE)
* [Path parameters](#body.PATH_PARAMETERS)
* [Request body](#body.request_body)
  + [JSON representation](#body.request_body.SCHEMA_REPRESENTATION)
* [Response body](#body.response_body)
* [Authorization scopes](#body.aspect)
* [Try it!](#try-it)

This item is deprecated!

**Full name**: projects.locations.transferConfigs.scheduleRuns

Creates transfer runs for a time range [startTime, endTime]. For each date - or whatever granularity the data source supports - in the range, one transfer run is created. Note that runs are created per UTC time in the time range. DEPRECATED: use transferConfigs.startManualRuns instead.

### HTTP request

Choose a location:

global asia-south1 asia-south2 europe-west1 europe-west2 europe-west3 europe-west4 europe-west6 europe-west8 europe-west9 me-central2 northamerica-northeast1 northamerica-northeast2 us-central1 us-central2 us-east1 us-east4 us-east5 us-east7 us-south1 us-west1 us-west2 us-west3 us-west4 us-west8

`POST https://bigquerydatatransfer.googleapis.com/v1/{parent=projects/*/locations/*/transferConfigs/*}:scheduleRuns`

The URLs use [gRPC Transcoding](https://google.aip.dev/127) syntax.

### Path parameters

| Parameters | |
| --- | --- |
| `parent` | `string`  Required. Transfer configuration name. If you are using the regionless method, the location must be `US` and the name should be in the following form:   * `projects/{projectId}/transferConfigs/{configId}`   If you are using the regionalized method, the name should be in the following form:   * `projects/{projectId}/locations/{locationId}/transferConfigs/{configId}`   Authorization requires the following [IAM](https://cloud.google.com/iam/docs/) permission on the specified resource `parent`:   * `bigquery.transfers.update` |

### Request body

The request body contains data with the following structure:

| JSON representation |
| --- |
| ``` {   "startTime": string,   "endTime": string } ``` |

| Fields | |
| --- | --- |
| `startTime` | `string (Timestamp format)`  Required. Start time of the range of transfer runs. For example, `"2017-05-25T00:00:00+00:00"`. |
| `endTime` | `string (Timestamp format)`  Required. End time of the range of transfer runs. For example, `"2017-05-30T00:00:00+00:00"`. |

### Response body

If successful, the response body contains an instance of `ScheduleTransferRunsResponse`.

### Authorization scopes

Requires the following OAuth scope:

* `https://www.googleapis.com/auth/cloud-platform`

For more information, see the [Authentication Overview](/docs/authentication#authorization-gcp).




Send feedback

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2026-05-12 UTC.




Need to tell us more?

[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Hard to understand","hardToUnderstand","thumb-down"],["Incorrect information or sample code","incorrectInformationOrSampleCode","thumb-down"],["Missing the information/samples I need","missingTheInformationSamplesINeed","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2026-05-12 UTC."],[],[]]