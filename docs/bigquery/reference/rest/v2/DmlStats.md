* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback

# DmlStats Stay organized with collections Save and categorize content based on your preferences.

* [JSON representation](#SCHEMA_REPRESENTATION)
* [DmlMode](#DmlMode)
* [FineGrainedDmlUnusedReason](#FineGrainedDmlUnusedReason)

Detailed statistics for DML statements

| JSON representation |
| --- |
| ``` {   "insertedRowCount": string,   "deletedRowCount": string,   "updatedRowCount": string,   "dmlMode": enum (DmlMode),   "fineGrainedDmlUnusedReason": enum (FineGrainedDmlUnusedReason) } ``` |

| Fields | |
| --- | --- |
| `insertedRowCount` | `string (Int64Value format)`  Output only. Number of inserted Rows. Populated by DML INSERT and MERGE statements |
| `deletedRowCount` | `string (Int64Value format)`  Output only. Number of deleted Rows. populated by DML DELETE, MERGE and TRUNCATE statements. |
| `updatedRowCount` | `string (Int64Value format)`  Output only. Number of updated Rows. Populated by DML UPDATE and MERGE statements. |
| `dmlMode` | `enum (DmlMode)`  Output only. DML mode used. |
| `fineGrainedDmlUnusedReason` | `enum (FineGrainedDmlUnusedReason)`  Output only. Reason for disabling fine-grained DML if applicable. |

## DmlMode

Enum to specify the DML mode used.

| Enums | |
| --- | --- |
| `DML_MODE_UNSPECIFIED` | Default value. This value is unused. |
| `COARSE_GRAINED_DML` | Coarse-grained DML was used. |
| `FINE_GRAINED_DML` | Fine-grained DML was used. |

## FineGrainedDmlUnusedReason

Reason for disabling fine-grained DML. Additional values may be added in the future.

| Enums | |
| --- | --- |
| `FINE_GRAINED_DML_UNUSED_REASON_UNSPECIFIED` | Default value. This value is unused. |
| `MAX_PARTITION_SIZE_EXCEEDED` | Max partition size threshold exceeded. [Fine-grained DML Limitations](https://docs.cloud.google.com/bigquery/docs/data-manipulation-language#fine-grained-dml-limitations) |
| `TABLE_NOT_ENROLLED` | The table is not enrolled for fine-grained DML. |
| `DML_IN_MULTI_STATEMENT_TRANSACTION` | The DML statement is part of a multi-statement transaction. |




Send feedback

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2026-02-19 UTC.




Need to tell us more?

[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Hard to understand","hardToUnderstand","thumb-down"],["Incorrect information or sample code","incorrectInformationOrSampleCode","thumb-down"],["Missing the information/samples I need","missingTheInformationSamplesINeed","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2026-02-19 UTC."],[],[]]