* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback

# BigQueryAuditMetadata.TableDataChange.Reason Stay organized with collections Save and categorize content based on your preferences.

Describes how the table data was changed.

| Enums | |
| --- | --- |
| `REASON_UNSPECIFIED` | Unknown. |
| `JOB` | Table was used as a job destination table. |
| `QUERY` | Table data was updated using a DML or DDL query. |
| `MATERIALIZED_VIEW_REFRESH` | Table data was updated during a materialized view refresh. |
| `WRITE_API_APPEND_ROWS` | Table data was chanegd using the Write API append rows. |
| `WRITE_API_CREATE_WRITE_STREAM` | Table data was changed using the Write API create write stream. |
| `WRITE_API_FINALIZE_WRITE_STREAM` | Table data was changed using the Write API finalize write stream. |
| `WRITE_API_FLUSH_ROWS` | Table data was changed using the Write API flush rows. |
| `WRITE_API_BATCH_COMMIT_WRITE_STREAMS` | Table data was changed using the Write API batch commit stream. |




Send feedback

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2025-07-02 UTC.




Need to tell us more?

[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Hard to understand","hardToUnderstand","thumb-down"],["Incorrect information or sample code","incorrectInformationOrSampleCode","thumb-down"],["Missing the information/samples I need","missingTheInformationSamplesINeed","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2025-07-02 UTC."],[],[]]