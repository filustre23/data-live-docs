* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback

# ResourceInfo Stay organized with collections Save and categorize content based on your preferences.

* [JSON representation](#SCHEMA_REPRESENTATION)

Describes the resource that is being accessed.

| JSON representation |
| --- |
| ``` {   "resourceType": string,   "resourceName": string,   "owner": string,   "description": string } ``` |

| Fields | |
| --- | --- |
| `resourceType` | `string`  A name for the type of resource being accessed, e.g. "sql table", "cloud storage bucket", "file", "Google calendar"; or the type URL of the resource: e.g. "type.googleapis.com/google.pubsub.v1.Topic". |
| `resourceName` | `string`  The name of the resource being accessed. For example, a shared calendar name: "example.com[\_4fghdhgsrgh@group.calendar.google.com"](mailto:_4fghdhgsrgh@group.calendar.google.com"), if the current error is `google.rpc.Code.PERMISSION_DENIED`. |
| `owner` | `string`  The owner of the resource (optional). For example, "user:" or "project:". |
| `description` | `string`  Describes what error is encountered when accessing this resource. For example, updating a cloud project may require the `writer` permission on the developer console project. |




Send feedback

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2025-07-02 UTC.




Need to tell us more?

[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Hard to understand","hardToUnderstand","thumb-down"],["Incorrect information or sample code","incorrectInformationOrSampleCode","thumb-down"],["Missing the information/samples I need","missingTheInformationSamplesINeed","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2025-07-02 UTC."],[],[]]