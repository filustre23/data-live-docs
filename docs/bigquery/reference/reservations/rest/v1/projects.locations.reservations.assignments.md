* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback

# REST Resource: projects.locations.reservations.assignments Stay organized with collections Save and categorize content based on your preferences.

* [Resource: Assignment](#Assignment)
  + [JSON representation](#Assignment.SCHEMA_REPRESENTATION)
* [JobType](#JobType)
* [State](#State)
* [Methods](#METHODS_SUMMARY)

## Resource: Assignment

An assignment allows a project to submit jobs of a certain type using slots from the specified reservation.

| JSON representation |
| --- |
| ``` {   "name": string,   "assignee": string,   "jobType": enum (JobType),   "state": enum (State) } ``` |

| Fields | |
| --- | --- |
| `name` | `string`  Output only. Name of the resource. E.g.: `projects/myproject/locations/US/reservations/team1-prod/assignments/123`. The assignmentId must only contain lower case alphanumeric characters or dashes and the max length is 64 characters. |
| `assignee` | `string`  Optional. The resource which will use the reservation. E.g. `projects/myproject`, `folders/123`, or `organizations/456`. |
| `jobType` | `enum (JobType)`  Optional. Which type of jobs will use the reservation. |
| `state` | `enum (State)`  Output only. State of the assignment. |

## JobType

Types of job, which could be specified when using the reservation.

| Enums | |
| --- | --- |
| `JOB_TYPE_UNSPECIFIED` | Invalid type. Requests with this value will be rejected with error code `google.rpc.Code.INVALID_ARGUMENT`. |
| `PIPELINE` | Pipeline (load/export) jobs from the project will use the reservation. |
| `QUERY` | Query jobs from the project will use the reservation. |
| `ML_EXTERNAL` | BigQuery ML jobs that use services external to BigQuery for model training. These jobs will not utilize idle slots from other reservations. |
| `BACKGROUND` | Background jobs that BigQuery runs for the customers in the background. |
| `CONTINUOUS` | Continuous SQL jobs will use this reservation. Reservations with continuous assignments cannot be mixed with non-continuous assignments. |
| `BACKGROUND_CHANGE_DATA_CAPTURE` | Finer granularity background jobs for capturing changes in a source database and streaming them into BigQuery. Reservations with this job type take priority over a default BACKGROUND reservation assignment (if it exists). |
| `BACKGROUND_COLUMN_METADATA_INDEX` | Finer granularity background jobs for refreshing cached metadata for BigQuery tables. Reservations with this job type take priority over a default BACKGROUND reservation assignment (if it exists). |
| `BACKGROUND_SEARCH_INDEX_REFRESH` | Finer granularity background jobs for refreshing search indexes upon BigQuery table columns. Reservations with this job type take priority over a default BACKGROUND reservation assignment (if it exists). |

## State

Assignment will remain in PENDING state if no active capacity commitment is present. It will become ACTIVE when some capacity commitment becomes active.

| Enums | |
| --- | --- |
| `STATE_UNSPECIFIED` | Invalid state value. |
| `PENDING` | Queries from assignee will be executed as on-demand, if related assignment is pending. |
| `ACTIVE` | Assignment is ready. |

| Methods | |
| --- | --- |
| `create` | Creates an assignment object which allows the given project to submit jobs of a certain type using slots from the specified reservation. |
| `delete` | Deletes a assignment. |
| `getIamPolicy` | Gets the access control policy for a resource. |
| `list` | Lists assignments. |
| `move` | Moves an assignment under a new reservation. |
| `patch` | Updates an existing assignment. |
| `setIamPolicy` | Sets an access control policy for a resource. |
| `testIamPermissions` | Gets your permissions on a resource. |




Send feedback

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2025-12-22 UTC.




Need to tell us more?

[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Hard to understand","hardToUnderstand","thumb-down"],["Incorrect information or sample code","incorrectInformationOrSampleCode","thumb-down"],["Missing the information/samples I need","missingTheInformationSamplesINeed","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2025-12-22 UTC."],[],[]]