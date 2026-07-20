* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback

# ConnectionProperty Stay organized with collections Save and categorize content based on your preferences.

* [JSON representation](#SCHEMA_REPRESENTATION)

A connection-level property to customize query behavior. Under JDBC, these correspond directly to connection properties passed to the DriverManager. Under ODBC, these correspond to properties in the connection string.

Currently supported connection properties:

* **dataset\_project\_id**: represents the default project for datasets that are used in the query. Setting the system variable `@@dataset_project_id` achieves the same behavior. For more information about system variables, see: <https://cloud.google.com/bigquery/docs/reference/system-variables>
* **time\_zone**: represents the default timezone used to run the query.
* **session\_id**: associates the query with a given session.
* **query\_label**: associates the query with a given job label. If set, all subsequent queries in a script or session will have this label. For the format in which a you can specify a query label, see labels in the JobConfiguration resource type: <https://cloud.google.com/bigquery/docs/reference/rest/v2/Job#jobconfiguration>
* **service\_account**: indicates the service account to use to run a continuous query. If set, the query job uses the service account to access Google Cloud resources. Service account access is bounded by the IAM permissions that you have granted to the service account.

Additional properties are allowed, but ignored. Specifying multiple connection properties with the same key returns an error.

| JSON representation |
| --- |
| ``` {   "key": string,   "value": string } ``` |

| Fields | |
| --- | --- |
| `key` | `string`  The key of the property to set. |
| `value` | `string`  The value of the property to set. |




Send feedback

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2025-07-02 UTC.




Need to tell us more?

[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Hard to understand","hardToUnderstand","thumb-down"],["Incorrect information or sample code","incorrectInformationOrSampleCode","thumb-down"],["Missing the information/samples I need","missingTheInformationSamplesINeed","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2025-07-02 UTC."],[],[]]