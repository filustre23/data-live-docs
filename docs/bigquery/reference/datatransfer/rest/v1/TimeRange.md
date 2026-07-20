* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback

# TimeRange Stay organized with collections Save and categorize content based on your preferences.

* [JSON representation](#SCHEMA_REPRESENTATION)

A specification for a time range, this will request transfer runs with runTime between startTime (inclusive) and endTime (exclusive).

| JSON representation |
| --- |
| ``` {   "startTime": string,   "endTime": string } ``` |

| Fields | |
| --- | --- |
| `startTime` | `string (Timestamp format)`  Start time of the range of transfer runs. For example, `"2017-05-25T00:00:00+00:00"`. The startTime must be strictly less than the endTime. Creates transfer runs where runTime is in the range between startTime (inclusive) and endTime (exclusive). |
| `endTime` | `string (Timestamp format)`  End time of the range of transfer runs. For example, `"2017-05-30T00:00:00+00:00"`. The endTime must not be in the future. Creates transfer runs where runTime is in the range between startTime (inclusive) and endTime (exclusive). |




Send feedback

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2025-07-02 UTC.




Need to tell us more?

[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Hard to understand","hardToUnderstand","thumb-down"],["Incorrect information or sample code","incorrectInformationOrSampleCode","thumb-down"],["Missing the information/samples I need","missingTheInformationSamplesINeed","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2025-07-02 UTC."],[],[]]