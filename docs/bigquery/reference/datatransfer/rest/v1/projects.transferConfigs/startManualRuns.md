* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback

# Method: transferConfigs.startManualRuns Stay organized with collections Save and categorize content based on your preferences.

* [HTTP request](#body.HTTP_TEMPLATE)
* [Path parameters](#body.PATH_PARAMETERS)
* [Request body](#body.request_body)
  + [JSON representation](#body.request_body.SCHEMA_REPRESENTATION)
* [Response body](#body.response_body)
* [Authorization scopes](#body.aspect)
* [Try it!](#try-it)

**Full name**: projects.transferConfigs.startManualRuns

Manually initiates transfer runs. You can schedule these runs in two ways:

1. For a specific point in time using the 'requestedRunTime' parameter.
2. For a period between 'startTime' (inclusive) and 'endTime' (exclusive).

If scheduling a single run, it is set to execute immediately (scheduleTime equals the current time). When scheduling multiple runs within a time range, the first run starts now, and subsequent runs are delayed by 15 seconds each.

### HTTP request

Choose a location:

global asia-south1 asia-south2 europe-west1 europe-west2 europe-west3 europe-west4 europe-west6 europe-west8 europe-west9 me-central2 northamerica-northeast1 northamerica-northeast2 us-central1 us-central2 us-east1 us-east4 us-east5 us-east7 us-south1 us-west1 us-west2 us-west3 us-west4 us-west8

`POST https://bigquerydatatransfer.googleapis.com/v1/{parent=projects/*/transferConfigs/*}:startManualRuns`

The URLs use [gRPC Transcoding](https://google.aip.dev/127) syntax.

### Path parameters

| Parameters | |
| --- | --- |
| `parent` | `string`  Required. Transfer configuration name. If you are using the regionless method, the location must be `US` and the name should be in the following form:   * `projects/{projectId}/transferConfigs/{configId}`   If you are using the regionalized method, the name should be in the following form:   * `projects/{projectId}/locations/{locationId}/transferConfigs/{configId}`   Authorization requires the following [IAM](https://cloud.google.com/iam/docs/) permission on the specified resource `parent`:   * `bigquery.transfers.update` |

### Request body

The request body contains data with the following structure:

| JSON representation |
| --- |
| ``` {    // Union field time can be only one of the following:   "requestedTimeRange": {     object (TimeRange)   },   "requestedRunTime": string   // End of list of possible types for union field time. } ``` |

| Fields | |
| --- | --- |
| Union field `time`. The requested time specification - this can be a time range or a specific run\_time. `time` can be only one of the following: | |
| `requestedTimeRange` | `object (TimeRange)`  A time\_range start and end timestamp for historical data files or reports that are scheduled to be transferred by the scheduled transfer run. requestedTimeRange must be a past time and cannot include future time values. |
| `requestedRunTime` | `string (Timestamp format)`  A runTime timestamp for historical data files or reports that are scheduled to be transferred by the scheduled transfer run. requestedRunTime must be a past time and cannot include future time values. |

### Response body

If successful, the response body contains an instance of `StartManualTransferRunsResponse`.

### Authorization scopes

Requires the following OAuth scope:

* `https://www.googleapis.com/auth/cloud-platform`

For more information, see the [Authentication Overview](/docs/authentication#authorization-gcp).




Send feedback

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2026-05-12 UTC.




Need to tell us more?

[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Hard to understand","hardToUnderstand","thumb-down"],["Incorrect information or sample code","incorrectInformationOrSampleCode","thumb-down"],["Missing the information/samples I need","missingTheInformationSamplesINeed","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2026-05-12 UTC."],[],[]]