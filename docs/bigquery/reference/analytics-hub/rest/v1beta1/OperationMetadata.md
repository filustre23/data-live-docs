* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)

Send feedback

# OperationMetadata Stay organized with collections Save and categorize content based on your preferences.

* [JSON representation](#SCHEMA_REPRESENTATION)

Represents the metadata of the long-running operation.

| JSON representation |
| --- |
| ``` {   "createTime": string,   "endTime": string,   "target": string,   "verb": string,   "statusDetail": string,   "cancelRequested": boolean,   "apiVersion": string } ``` |

| Fields | |
| --- | --- |
| `createTime` | `string (Timestamp format)`  Output only. The time the operation was created.  A timestamp in RFC3339 UTC "Zulu" format, with nanosecond resolution and up to nine fractional digits. Examples: `"2014-10-02T15:01:23Z"` and `"2014-10-02T15:01:23.045123456Z"`. |
| `endTime` | `string (Timestamp format)`  Output only. The time the operation finished running.  A timestamp in RFC3339 UTC "Zulu" format, with nanosecond resolution and up to nine fractional digits. Examples: `"2014-10-02T15:01:23Z"` and `"2014-10-02T15:01:23.045123456Z"`. |
| `target` | `string`  Output only. Server-defined resource path for the target of the operation. |
| `verb` | `string`  Output only. Name of the verb executed by the operation. |
| `statusDetail` | `string`  Output only. Human-readable status of the operation, if any. |
| `cancelRequested` | `boolean`  Output only. Identifies whether the user has requested cancellation of the operation. Operations that have been cancelled successfully have [Operation.error][] value with a `google.rpc.Status.code` of 1, corresponding to `Code.CANCELLED`. |
| `apiVersion` | `string`  Output only. API version used to start the operation. |




Send feedback

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2025-07-02 UTC.




Need to tell us more?

[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Hard to understand","hardToUnderstand","thumb-down"],["Incorrect information or sample code","incorrectInformationOrSampleCode","thumb-down"],["Missing the information/samples I need","missingTheInformationSamplesINeed","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2025-07-02 UTC."],[],[]]