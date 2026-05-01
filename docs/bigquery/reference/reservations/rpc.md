* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback

# BigQuery Reservation API Stay organized with collections Save and categorize content based on your preferences.

A service to modify your BigQuery reservations.

## Service: bigqueryreservation.googleapis.com

The Service name `bigqueryreservation.googleapis.com` is needed to create RPC client stubs.

## `google.cloud.bigquery.reservation.v1.ReservationService`

| Methods | |
| --- | --- |
| `CreateAssignment` | Creates an assignment object which allows the given project to submit jobs of a certain type using slots from the specified reservation. |
| `CreateCapacityCommitment` | Creates a new capacity commitment resource. |
| `CreateReservation` | Creates a new reservation resource. |
| `CreateReservationGroup` | Creates a new reservation group. |
| `DeleteAssignment` | Deletes a assignment. |
| `DeleteCapacityCommitment` | Deletes a capacity commitment. |
| `DeleteReservation` | Deletes a reservation. |
| `DeleteReservationGroup` | Deletes a reservation. |
| `FailoverReservation` | Fail over a reservation to the secondary location. |
| `GetBiReservation` | Retrieves a BI reservation. |
| `GetCapacityCommitment` | Returns information about the capacity commitment. |
| `GetIamPolicy` | Gets the access control policy for a resource. |
| `GetReservation` | Returns information about the reservation. |
| `GetReservationGroup` | Returns information about the reservation group. |
| `ListAssignments` | Lists assignments. |
| `ListCapacityCommitments` | Lists all the capacity commitments for the admin project. |
| `ListReservationGroups` | Lists all the reservation groups for the project in the specified location. |
| `ListReservations` | Lists all the reservations for the project in the specified location. |
| `MergeCapacityCommitments` | Merges capacity commitments of the same plan into a single commitment. |
| `MoveAssignment` | Moves an assignment under a new reservation. |
| `SearchAllAssignments` | Looks up assignments for a specified resource for a particular region. |
| `SearchAssignments  (deprecated)` | Deprecated: Looks up assignments for a specified resource for a particular region. |
| `SetIamPolicy` | Sets an access control policy for a resource. |
| `SplitCapacityCommitment` | Splits capacity commitment to two commitments of the same plan and `commitment_end_time`. |
| `TestIamPermissions` | Gets your permissions on a resource. |
| `UpdateAssignment` | Updates an existing assignment. |
| `UpdateBiReservation` | Updates a BI reservation. |
| `UpdateCapacityCommitment` | Updates an existing capacity commitment. |
| `UpdateReservation` | Updates an existing reservation resource. |




Send feedback

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2025-12-19 UTC.




Need to tell us more?

[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Hard to understand","hardToUnderstand","thumb-down"],["Incorrect information or sample code","incorrectInformationOrSampleCode","thumb-down"],["Missing the information/samples I need","missingTheInformationSamplesINeed","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2025-12-19 UTC."],[],[]]