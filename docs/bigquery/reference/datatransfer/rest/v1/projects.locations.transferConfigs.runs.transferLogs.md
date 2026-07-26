* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback

# REST Resource: projects.locations.transferConfigs.runs.transferLogs Stay organized with collections Save and categorize content based on your preferences.

* [Resource: TransferMessage](#TransferMessage)
  + [JSON representation](#TransferMessage.SCHEMA_REPRESENTATION)
  + [MessageSeverity](#TransferMessage.MessageSeverity)
* [Methods](#METHODS_SUMMARY)

## Resource: TransferMessage

Represents a user facing message for a particular data transfer run.

| JSON representation |
| --- |
| ``` {   "messageTime": string,   "severity": enum (MessageSeverity),   "messageText": string } ``` |

| Fields | |
| --- | --- |
| `messageTime` | `string (Timestamp format)`  Time when message was logged. |
| `severity` | `enum (MessageSeverity)`  Message severity. |
| `messageText` | `string`  Message text. |

### MessageSeverity

Represents data transfer user facing message severity.

| Enums | |
| --- | --- |
| `MESSAGE_SEVERITY_UNSPECIFIED` | No severity specified. |
| `INFO` | Informational message. |
| `WARNING` | Warning message. |
| `ERROR` | Error message. |

| Methods | |
| --- | --- |
| `list` | Returns log messages for the transfer run. |




Send feedback

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2025-07-02 UTC.




Need to tell us more?

[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Hard to understand","hardToUnderstand","thumb-down"],["Incorrect information or sample code","incorrectInformationOrSampleCode","thumb-down"],["Missing the information/samples I need","missingTheInformationSamplesINeed","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2025-07-02 UTC."],[],[]]