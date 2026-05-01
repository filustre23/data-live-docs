* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback

# REST Resource: projects.transferConfigs.runs Stay organized with collections Save and categorize content based on your preferences.

* [Resource: TransferRun](#TransferRun)
  + [JSON representation](#TransferRun.SCHEMA_REPRESENTATION)
* [Methods](#METHODS_SUMMARY)

## Resource: TransferRun

Represents a data transfer run.

| JSON representation |
| --- |
| ``` {   "name": string,   "scheduleTime": string,   "runTime": string,   "errorStatus": {     object (Status)   },   "startTime": string,   "endTime": string,   "updateTime": string,   "params": {     object   },   "dataSourceId": string,   "state": enum (TransferState),   "userId": string,   "schedule": string,   "notificationPubsubTopic": string,   "emailPreferences": {     object (EmailPreferences)   },    // Union field destination can be only one of the following:   "destinationDatasetId": string   // End of list of possible types for union field destination. } ``` |

| Fields | |
| --- | --- |
| `name` | `string`  Identifier. The resource name of the transfer run. Transfer run names have the form `projects/{projectId}/locations/{location}/transferConfigs/{configId}/runs/{run_id}`. The name is ignored when creating a transfer run. |
| `scheduleTime` | `string (Timestamp format)`  Minimum time after which a transfer run can be started. |
| `runTime` | `string (Timestamp format)`  For batch transfer runs, specifies the date and time of the data should be ingested. |
| `errorStatus` | `object (Status)`  Status of the transfer run. |
| `startTime` | `string (Timestamp format)`  Output only. Time when transfer run was started. Parameter ignored by server for input requests. |
| `endTime` | `string (Timestamp format)`  Output only. Time when transfer run ended. Parameter ignored by server for input requests. |
| `updateTime` | `string (Timestamp format)`  Output only. Last time the data transfer run state was updated. |
| `params` | `object (Struct format)`  Output only. Parameters specific to each data source. For more information see the bq tab in the 'Setting up a data transfer' section for each data source. For example the parameters for Cloud Storage transfers are listed here: <https://cloud.google.com/bigquery-transfer/docs/cloud-storage-transfer#bq> |
| `dataSourceId` | `string`  Output only. Data source id. |
| `state` | `enum (TransferState)`  Data transfer run state. Ignored for input requests. |
| `userId` | `string (int64 format)`  Deprecated. Unique ID of the user on whose behalf transfer is done. |
| `schedule` | `string`  Output only. Describes the schedule of this transfer run if it was created as part of a regular schedule. For batch transfer runs that are scheduled manually, this is empty. NOTE: the system might choose to delay the schedule depending on the current load, so `scheduleTime` doesn't always match this. |
| `notificationPubsubTopic` | `string`  Output only. Pub/Sub topic where a notification will be sent after this transfer run finishes.  The format for specifying a pubsub topic is: `projects/{projectId}/topics/{topic_id}` |
| `emailPreferences` | `object (EmailPreferences)`  Output only. Email notifications will be sent according to these preferences to the email address of the user who owns the transfer config this run was derived from. |
| Union field `destination`. Data transfer destination. `destination` can be only one of the following: | |
| `destinationDatasetId` | `string`  Output only. The BigQuery target dataset id. |

| Methods | |
| --- | --- |
| `delete` | Deletes the specified transfer run. |
| `get` | Returns information about the particular transfer run. |
| `list` | Returns information about running and completed transfer runs. |




Send feedback

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2025-07-02 UTC.




Need to tell us more?

[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Hard to understand","hardToUnderstand","thumb-down"],["Incorrect information or sample code","incorrectInformationOrSampleCode","thumb-down"],["Missing the information/samples I need","missingTheInformationSamplesINeed","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2025-07-02 UTC."],[],[]]