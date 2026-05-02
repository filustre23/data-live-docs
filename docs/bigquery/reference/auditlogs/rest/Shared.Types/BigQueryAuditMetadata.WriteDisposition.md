* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback

# BigQueryAuditMetadata.WriteDisposition Stay organized with collections Save and categorize content based on your preferences.

Describes whether a job should overwrite or append the existing destination table if it already exists.

| Enums | |
| --- | --- |
| `WRITE_DISPOSITION_UNSPECIFIED` | Unknown. |
| `WRITE_EMPTY` | This job should only be writing to empty tables. |
| `WRITE_TRUNCATE` | This job will truncate table data and write from the beginning. This might not preserve table metadata such as table schema, row access policy, column level policy, or column descriptions. This is the default value. |
| `WRITE_APPEND` | This job will append to the table. |
| `WRITE_TRUNCATE_DATA` | This job will truncate table data but preserve table metadata such as table schema, row access policy, column level policy, or column descriptions. |




Send feedback

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2026-05-01 UTC.




Need to tell us more?

[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Hard to understand","hardToUnderstand","thumb-down"],["Incorrect information or sample code","incorrectInformationOrSampleCode","thumb-down"],["Missing the information/samples I need","missingTheInformationSamplesINeed","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2026-05-01 UTC."],[],[]]