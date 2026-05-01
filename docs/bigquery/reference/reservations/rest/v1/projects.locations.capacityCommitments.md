* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback

# REST Resource: projects.locations.capacityCommitments Stay organized with collections Save and categorize content based on your preferences.

* [Resource: CapacityCommitment](#CapacityCommitment)
  + [JSON representation](#CapacityCommitment.SCHEMA_REPRESENTATION)
* [CommitmentPlan](#CommitmentPlan)
* [State](#State)
* [Methods](#METHODS_SUMMARY)

## Resource: CapacityCommitment

Capacity commitment is a way to purchase compute capacity for BigQuery jobs (in the form of slots) with some committed period of usage. Annual commitments renew by default. Commitments can be removed after their commitment end time passes.

In order to remove annual commitment, its plan needs to be changed to monthly or flex first.

A capacity commitment resource exists as a child resource of the admin project.

| JSON representation |
| --- |
| ``` {   "name": string,   "slotCount": string,   "plan": enum (CommitmentPlan),   "state": enum (State),   "commitmentStartTime": string,   "commitmentEndTime": string,   "failureStatus": {     object (Status)   },   "renewalPlan": enum (CommitmentPlan),   "edition": enum (Edition),   "isFlatRate": boolean } ``` |

| Fields | |
| --- | --- |
| `name` | `string`  Output only. The resource name of the capacity commitment, e.g., `projects/myproject/locations/US/capacityCommitments/123` The commitment\_id must only contain lower case alphanumeric characters or dashes. It must start with a letter and must not end with a dash. Its maximum length is 64 characters. |
| `slotCount` | `string (int64 format)`  Optional. Number of slots in this commitment. |
| `plan` | `enum (CommitmentPlan)`  Optional. Capacity commitment commitment plan. |
| `state` | `enum (State)`  Output only. State of the commitment. |
| `commitmentStartTime` | `string (Timestamp format)`  Output only. The start of the current commitment period. It is applicable only for ACTIVE capacity commitments. Note after the commitment is renewed, commitmentStartTime won't be changed. It refers to the start time of the original commitment.  Uses RFC 3339, where generated output will always be Z-normalized and use 0, 3, 6 or 9 fractional digits. Offsets other than "Z" are also accepted. Examples: `"2014-10-02T15:01:23Z"`, `"2014-10-02T15:01:23.045123456Z"` or `"2014-10-02T15:01:23+05:30"`. |
| `commitmentEndTime` | `string (Timestamp format)`  Output only. The end of the current commitment period. It is applicable only for ACTIVE capacity commitments. Note after renewal, commitmentEndTime is the time the renewed commitment expires. So itwould be at a time after commitmentStartTime + committed period, because we don't change commitmentStartTime ,  Uses RFC 3339, where generated output will always be Z-normalized and use 0, 3, 6 or 9 fractional digits. Offsets other than "Z" are also accepted. Examples: `"2014-10-02T15:01:23Z"`, `"2014-10-02T15:01:23.045123456Z"` or `"2014-10-02T15:01:23+05:30"`. |
| `failureStatus` | `object (Status)`  Output only. For FAILED commitment plan, provides the reason of failure. |
| `renewalPlan` | `enum (CommitmentPlan)`  Optional. The plan this capacity commitment is converted to after commitmentEndTime passes. Once the plan is changed, committed period is extended according to commitment plan. Only applicable for ANNUAL and TRIAL commitments. |
| `edition` | `enum (Edition)`  Optional. Edition of the capacity commitment. |
| `isFlatRate` | `boolean`  Output only. If true, the commitment is a flat-rate commitment, otherwise, it's an edition commitment. |

## CommitmentPlan

Commitment plan defines the current committed period. Capacity commitment cannot be deleted during it's committed period.

| Enums | |
| --- | --- |
| `COMMITMENT_PLAN_UNSPECIFIED` | Invalid plan value. Requests with this value will be rejected with error code `google.rpc.Code.INVALID_ARGUMENT`. |
| `FLEX` | Flex commitments have committed period of 1 minute after becoming ACTIVE. After that, they are not in a committed period anymore and can be removed any time. |
| `FLEX_FLAT_RATE` | Same as FLEX, should only be used if flat-rate commitments are still available.  This item is deprecated! |
| `TRIAL` | Trial commitments have a committed period of 182 days after becoming ACTIVE. After that, they are converted to a new commitment based on the `renewalPlan`. Default `renewalPlan` for Trial commitment is Flex so that it can be deleted right after committed period ends.  This item is deprecated! |
| `MONTHLY` | Monthly commitments have a committed period of 30 days after becoming ACTIVE. After that, they are not in a committed period anymore and can be removed any time. |
| `MONTHLY_FLAT_RATE` | Same as MONTHLY, should only be used if flat-rate commitments are still available.  This item is deprecated! |
| `ANNUAL` | Annual commitments have a committed period of 365 days after becoming ACTIVE. After that they are converted to a new commitment based on the renewalPlan. |
| `ANNUAL_FLAT_RATE` | Same as ANNUAL, should only be used if flat-rate commitments are still available.  This item is deprecated! |
| `THREE_YEAR` | 3-year commitments have a committed period of 1095(3 \* 365) days after becoming ACTIVE. After that they are converted to a new commitment based on the renewalPlan. |
| `NONE` | Should only be used for `renewalPlan` and is only meaningful if edition is specified to values other than EDITION\_UNSPECIFIED. Otherwise CreateCapacityCommitmentRequest or UpdateCapacityCommitmentRequest will be rejected with error code `google.rpc.Code.INVALID_ARGUMENT`. If the renewalPlan is NONE, capacity commitment will be removed at the end of its commitment period. |

## State

Capacity commitment can either become ACTIVE right away or transition from PENDING to ACTIVE or FAILED.

| Enums | |
| --- | --- |
| `STATE_UNSPECIFIED` | Invalid state value. |
| `PENDING` | Capacity commitment is pending provisioning. Pending capacity commitment does not contribute to the project's slotCapacity. |
| `ACTIVE` | Once slots are provisioned, capacity commitment becomes active. slotCount is added to the project's slotCapacity. |
| `FAILED` | Capacity commitment is failed to be activated by the backend. |

| Methods | |
| --- | --- |
| `create` | Creates a new capacity commitment resource. |
| `delete` | Deletes a capacity commitment. |
| `get` | Returns information about the capacity commitment. |
| `list` | Lists all the capacity commitments for the admin project. |
| `merge` | Merges capacity commitments of the same plan into a single commitment. |
| `patch` | Updates an existing capacity commitment. |
| `split` | Splits capacity commitment to two commitments of the same plan and `commitment_end_time`. |




Send feedback

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2025-08-21 UTC.




Need to tell us more?

[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Hard to understand","hardToUnderstand","thumb-down"],["Incorrect information or sample code","incorrectInformationOrSampleCode","thumb-down"],["Missing the information/samples I need","missingTheInformationSamplesINeed","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2025-08-21 UTC."],[],[]]