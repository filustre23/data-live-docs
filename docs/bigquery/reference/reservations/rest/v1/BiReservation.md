* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback

# BiReservation Stay organized with collections Save and categorize content based on your preferences.

* [JSON representation](#SCHEMA_REPRESENTATION)
* [TableReference](#TableReference)
  + [JSON representation](#TableReference.SCHEMA_REPRESENTATION)

Represents a BI Reservation.

| JSON representation |
| --- |
| ``` {   "name": string,   "updateTime": string,   "size": string,   "preferredTables": [     {       object (TableReference)     }   ] } ``` |

| Fields | |
| --- | --- |
| `name` | `string`  Identifier. The resource name of the singleton BI reservation. Reservation names have the form `projects/{projectId}/locations/{locationId}/biReservation`. |
| `updateTime` | `string (Timestamp format)`  Output only. The last update timestamp of a reservation.  Uses RFC 3339, where generated output will always be Z-normalized and use 0, 3, 6 or 9 fractional digits. Offsets other than "Z" are also accepted. Examples: `"2014-10-02T15:01:23Z"`, `"2014-10-02T15:01:23.045123456Z"` or `"2014-10-02T15:01:23+05:30"`. |
| `size` | `string (int64 format)`  Optional. Size of a reservation, in bytes. |
| `preferredTables[]` | `object (TableReference)`  Optional. Preferred tables to use BI capacity for. |

## TableReference

Fully qualified reference to BigQuery table. Internally stored as google.cloud.bi.v1.BqTableReference.

| JSON representation |
| --- |
| ``` {   "projectId": string,   "datasetId": string,   "tableId": string } ``` |

| Fields | |
| --- | --- |
| `projectId` | `string`  Optional. The assigned project ID of the project. |
| `datasetId` | `string`  Optional. The ID of the dataset in the above project. |
| `tableId` | `string`  Optional. The ID of the table in the above dataset. |




Send feedback

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2025-08-21 UTC.




Need to tell us more?

[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Hard to understand","hardToUnderstand","thumb-down"],["Incorrect information or sample code","incorrectInformationOrSampleCode","thumb-down"],["Missing the information/samples I need","missingTheInformationSamplesINeed","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2025-08-21 UTC."],[],[]]