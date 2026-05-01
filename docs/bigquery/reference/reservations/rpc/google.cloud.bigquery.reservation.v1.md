* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback

# Package google.cloud.bigquery.reservation.v1 Stay organized with collections Save and categorize content based on your preferences.

## Index

* `ReservationService` (interface)
* `Assignment` (message)
* `Assignment.JobType` (enum)
* `Assignment.State` (enum)
* `BiReservation` (message)
* `CapacityCommitment` (message)
* `CapacityCommitment.CommitmentPlan` (enum)
* `CapacityCommitment.State` (enum)
* `CreateAssignmentRequest` (message)
* `CreateCapacityCommitmentRequest` (message)
* `CreateReservationGroupRequest` (message)
* `CreateReservationRequest` (message)
* `DeleteAssignmentRequest` (message)
* `DeleteCapacityCommitmentRequest` (message)
* `DeleteReservationGroupRequest` (message)
* `DeleteReservationRequest` (message)
* `Edition` (enum)
* `FailoverMode` (enum)
* `FailoverReservationRequest` (message)
* `GetBiReservationRequest` (message)
* `GetCapacityCommitmentRequest` (message)
* `GetReservationGroupRequest` (message)
* `GetReservationRequest` (message)
* `ListAssignmentsRequest` (message)
* `ListAssignmentsResponse` (message)
* `ListCapacityCommitmentsRequest` (message)
* `ListCapacityCommitmentsResponse` (message)
* `ListReservationGroupsRequest` (message)
* `ListReservationGroupsResponse` (message)
* `ListReservationsRequest` (message)
* `ListReservationsResponse` (message)
* `MergeCapacityCommitmentsRequest` (message)
* `MoveAssignmentRequest` (message)
* `Reservation` (message)
* `Reservation.Autoscale` (message)
* `Reservation.ReplicationStatus` (message)
* `Reservation.ScalingMode` (enum)
* `ReservationGroup` (message)
* `SearchAllAssignmentsRequest` (message)
* `SearchAllAssignmentsResponse` (message)
* `SearchAssignmentsRequest` (message)
* `SearchAssignmentsResponse` (message)
* `SplitCapacityCommitmentRequest` (message)
* `SplitCapacityCommitmentResponse` (message)
* `TableReference` (message)
* `UpdateAssignmentRequest` (message)
* `UpdateBiReservationRequest` (message)
* `UpdateCapacityCommitmentRequest` (message)
* `UpdateReservationRequest` (message)

## ReservationService

This API allows users to manage their BigQuery reservations.

A reservation provides computational resource guarantees, in the form of [slots](https://cloud.google.com/bigquery/docs/slots), to users. A slot is a unit of computational power in BigQuery, and serves as the basic unit of parallelism. In a scan of a multi-partitioned table, a single slot operates on a single partition of the table. A reservation resource exists as a child resource of the admin project and location, e.g.: `projects/myproject/locations/US/reservations/reservationName`.

A capacity commitment is a way to purchase compute capacity for BigQuery jobs (in the form of slots) with some committed period of usage. A capacity commitment resource exists as a child resource of the admin project and location, e.g.: `projects/myproject/locations/US/capacityCommitments/id`.

| CreateAssignment |
| --- |
| `rpc CreateAssignment(CreateAssignmentRequest) returns (Assignment)`  Creates an assignment object which allows the given project to submit jobs of a certain type using slots from the specified reservation.  Currently a resource (project, folder, organization) can only have one assignment per each (job\_type, location) combination, and that reservation will be used for all jobs of the matching type.  Different assignments can be created on different levels of the projects, folders or organization hierarchy. During query execution, the assignment is looked up at the project, folder and organization levels in that order. The first assignment found is applied to the query.  When creating assignments, it does not matter if other assignments exist at higher levels.  Example:   * The organization `organizationA` contains two projects, `project1` and `project2`. * Assignments for all three entities (`organizationA`, `project1`, and `project2`) could all be created and mapped to the same or different reservations.   "None" assignments represent an absence of the assignment. Projects assigned to None use on-demand pricing. To create a "None" assignment, use "none" as a reservation\_id in the parent. Example parent: `projects/myproject/locations/US/reservations/none`.  Returns `google.rpc.Code.PERMISSION_DENIED` if user does not have 'bigquery.admin' permissions on the project using the reservation and the project that owns this reservation.  Returns `google.rpc.Code.INVALID_ARGUMENT` when location of the assignment does not match location of the reservation.  Authorization scopes  Requires one of the following OAuth scopes:   * `https://www.googleapis.com/auth/bigquery` * `https://www.googleapis.com/auth/cloud-platform`   For more information, see the [Authentication Overview](/docs/authentication#authorization-gcp). |

| CreateCapacityCommitment |
| --- |
| `rpc CreateCapacityCommitment(CreateCapacityCommitmentRequest) returns (CapacityCommitment)`  Creates a new capacity commitment resource.  Authorization scopes  Requires one of the following OAuth scopes:   * `https://www.googleapis.com/auth/bigquery` * `https://www.googleapis.com/auth/cloud-platform`   For more information, see the [Authentication Overview](/docs/authentication#authorization-gcp). |

| CreateReservation |
| --- |
| `rpc CreateReservation(CreateReservationRequest) returns (Reservation)`  Creates a new reservation resource.  Authorization scopes  Requires one of the following OAuth scopes:   * `https://www.googleapis.com/auth/bigquery` * `https://www.googleapis.com/auth/cloud-platform`   For more information, see the [Authentication Overview](/docs/authentication#authorization-gcp). |

| CreateReservationGroup |
| --- |
| `rpc CreateReservationGroup(CreateReservationGroupRequest) returns (ReservationGroup)`  Creates a new reservation group.  Authorization scopes  Requires one of the following OAuth scopes:   * `https://www.googleapis.com/auth/bigquery` * `https://www.googleapis.com/auth/cloud-platform`   For more information, see the [Authentication Overview](/docs/authentication#authorization-gcp). |

| DeleteAssignment |
| --- |
| `rpc DeleteAssignment(DeleteAssignmentRequest) returns (Empty)`  Deletes a assignment. No expansion will happen.  Example:   * Organization `organizationA` contains two projects, `project1` and `project2`. * Reservation `res1` exists and was created previously. * CreateAssignment was used previously to define the following associations between entities and reservations: `<organizationA, res1>` and `<project1, res1>`   In this example, deletion of the `<organizationA, res1>` assignment won't affect the other assignment `<project1, res1>`. After said deletion, queries from `project1` will still use `res1` while queries from `project2` will switch to use on-demand mode.  Authorization scopes  Requires one of the following OAuth scopes:   * `https://www.googleapis.com/auth/bigquery` * `https://www.googleapis.com/auth/cloud-platform`   For more information, see the [Authentication Overview](/docs/authentication#authorization-gcp). |

| DeleteCapacityCommitment |
| --- |
| `rpc DeleteCapacityCommitment(DeleteCapacityCommitmentRequest) returns (Empty)`  Deletes a capacity commitment. Attempting to delete capacity commitment before its commitment\_end\_time will fail with the error code `google.rpc.Code.FAILED_PRECONDITION`.  Authorization scopes  Requires one of the following OAuth scopes:   * `https://www.googleapis.com/auth/bigquery` * `https://www.googleapis.com/auth/cloud-platform`   For more information, see the [Authentication Overview](/docs/authentication#authorization-gcp). |

| DeleteReservation |
| --- |
| `rpc DeleteReservation(DeleteReservationRequest) returns (Empty)`  Deletes a reservation. Returns `google.rpc.Code.FAILED_PRECONDITION` when reservation has assignments.  Authorization scopes  Requires one of the following OAuth scopes:   * `https://www.googleapis.com/auth/bigquery` * `https://www.googleapis.com/auth/cloud-platform`   For more information, see the [Authentication Overview](/docs/authentication#authorization-gcp). |

| DeleteReservationGroup |
| --- |
| `rpc DeleteReservationGroup(DeleteReservationGroupRequest) returns (Empty)`  Deletes a reservation. Returns `google.rpc.Code.FAILED_PRECONDITION` when reservation has assignments.  Authorization scopes  Requires one of the following OAuth scopes:   * `https://www.googleapis.com/auth/bigquery` * `https://www.googleapis.com/auth/cloud-platform`   For more information, see the [Authentication Overview](/docs/authentication#authorization-gcp). |

| FailoverReservation |
| --- |
| `rpc FailoverReservation(FailoverReservationRequest) returns (Reservation)`  Fail over a reservation to the secondary location. The operation should be done in the current secondary location, which will be promoted to the new primary location for the reservation. Attempting to failover a reservation in the current primary location will fail with the error code `google.rpc.Code.FAILED_PRECONDITION`.  Authorization scopes  Requires one of the following OAuth scopes:   * `https://www.googleapis.com/auth/bigquery` * `https://www.googleapis.com/auth/cloud-platform`   For more information, see the [Authentication Overview](/docs/authentication#authorization-gcp). |

| GetBiReservation |
| --- |
| `rpc GetBiReservation(GetBiReservationRequest) returns (BiReservation)`  Retrieves a BI reservation.  Authorization scopes  Requires one of the following OAuth scopes:   * `https://www.googleapis.com/auth/bigquery` * `https://www.googleapis.com/auth/cloud-platform`   For more information, see the [Authentication Overview](/docs/authentication#authorization-gcp). |

| GetCapacityCommitment |
| --- |
| `rpc GetCapacityCommitment(GetCapacityCommitmentRequest) returns (CapacityCommitment)`  Returns information about the capacity commitment.  Authorization scopes  Requires one of the following OAuth scopes:   * `https://www.googleapis.com/auth/bigquery` * `https://www.googleapis.com/auth/cloud-platform`   For more information, see the [Authentication Overview](/docs/authentication#authorization-gcp). |

| GetIamPolicy |
| --- |
| `rpc GetIamPolicy(GetIamPolicyRequest) returns (Policy)`  Gets the access control policy for a resource. May return:   * A`NOT_FOUND` error if the resource doesn't exist or you don't have the permission to view it. * An empty policy if the resource exists but doesn't have a set policy.   Supported resources are: - Reservations - ReservationAssignments  To call this method, you must have the following Google IAM permissions:   * `bigqueryreservation.reservations.getIamPolicy` to get policies on reservations.   Authorization scopes  Requires one of the following OAuth scopes:   * `https://www.googleapis.com/auth/bigquery` * `https://www.googleapis.com/auth/cloud-platform`   For more information, see the [Authentication Overview](/docs/authentication#authorization-gcp). |

| GetReservation |
| --- |
| `rpc GetReservation(GetReservationRequest) returns (Reservation)`  Returns information about the reservation.  Authorization scopes  Requires one of the following OAuth scopes:   * `https://www.googleapis.com/auth/bigquery` * `https://www.googleapis.com/auth/cloud-platform`   For more information, see the [Authentication Overview](/docs/authentication#authorization-gcp). |

| GetReservationGroup |
| --- |
| `rpc GetReservationGroup(GetReservationGroupRequest) returns (ReservationGroup)`  Returns information about the reservation group.  Authorization scopes  Requires one of the following OAuth scopes:   * `https://www.googleapis.com/auth/bigquery` * `https://www.googleapis.com/auth/cloud-platform`   For more information, see the [Authentication Overview](/docs/authentication#authorization-gcp). |

| ListAssignments |
| --- |
| `rpc ListAssignments(ListAssignmentsRequest) returns (ListAssignmentsResponse)`  Lists assignments.  Only explicitly created assignments will be returned.  Example:   * Organization `organizationA` contains two projects, `project1` and `project2`. * Reservation `res1` exists and was created previously. * CreateAssignment was used previously to define the following associations between entities and reservations: `<organizationA, res1>` and `<project1, res1>`   In this example, ListAssignments will just return the above two assignments for reservation `res1`, and no expansion/merge will happen.  The wildcard "-" can be used for reservations in the request. In that case all assignments belongs to the specified project and location will be listed.  **Note** "-" cannot be used for projects nor locations.  Authorization scopes  Requires one of the following OAuth scopes:   * `https://www.googleapis.com/auth/bigquery` * `https://www.googleapis.com/auth/cloud-platform`   For more information, see the [Authentication Overview](/docs/authentication#authorization-gcp). |

| ListCapacityCommitments |
| --- |
| `rpc ListCapacityCommitments(ListCapacityCommitmentsRequest) returns (ListCapacityCommitmentsResponse)`  Lists all the capacity commitments for the admin project.  Authorization scopes  Requires one of the following OAuth scopes:   * `https://www.googleapis.com/auth/bigquery` * `https://www.googleapis.com/auth/cloud-platform`   For more information, see the [Authentication Overview](/docs/authentication#authorization-gcp). |

| ListReservationGroups |
| --- |
| `rpc ListReservationGroups(ListReservationGroupsRequest) returns (ListReservationGroupsResponse)`  Lists all the reservation groups for the project in the specified location.  Authorization scopes  Requires one of the following OAuth scopes:   * `https://www.googleapis.com/auth/bigquery` * `https://www.googleapis.com/auth/cloud-platform`   For more information, see the [Authentication Overview](/docs/authentication#authorization-gcp). |

| ListReservations |
| --- |
| `rpc ListReservations(ListReservationsRequest) returns (ListReservationsResponse)`  Lists all the reservations for the project in the specified location.  Authorization scopes  Requires one of the following OAuth scopes:   * `https://www.googleapis.com/auth/bigquery` * `https://www.googleapis.com/auth/cloud-platform`   For more information, see the [Authentication Overview](/docs/authentication#authorization-gcp). |

| MergeCapacityCommitments |
| --- |
| `rpc MergeCapacityCommitments(MergeCapacityCommitmentsRequest) returns (CapacityCommitment)`  Merges capacity commitments of the same plan into a single commitment.  The resulting capacity commitment has the greater commitment\_end\_time out of the to-be-merged capacity commitments.  Attempting to merge capacity commitments of different plan will fail with the error code `google.rpc.Code.FAILED_PRECONDITION`.  Authorization scopes  Requires one of the following OAuth scopes:   * `https://www.googleapis.com/auth/bigquery` * `https://www.googleapis.com/auth/cloud-platform`   For more information, see the [Authentication Overview](/docs/authentication#authorization-gcp). |

| MoveAssignment |
| --- |
| `rpc MoveAssignment(MoveAssignmentRequest) returns (Assignment)`  Moves an assignment under a new reservation.  This differs from removing an existing assignment and recreating a new one by providing a transactional change that ensures an assignee always has an associated reservation.  Authorization scopes  Requires one of the following OAuth scopes:   * `https://www.googleapis.com/auth/bigquery` * `https://www.googleapis.com/auth/cloud-platform`   For more information, see the [Authentication Overview](/docs/authentication#authorization-gcp). |

| SearchAllAssignments |
| --- |
| `rpc SearchAllAssignments(SearchAllAssignmentsRequest) returns (SearchAllAssignmentsResponse)`  Looks up assignments for a specified resource for a particular region. If the request is about a project:   1. Assignments created on the project will be returned if they exist. 2. Otherwise assignments created on the closest ancestor will be returned. 3. Assignments for different JobTypes will all be returned.   The same logic applies if the request is about a folder.  If the request is about an organization, then assignments created on the organization will be returned (organization doesn't have ancestors).  Comparing to ListAssignments, there are some behavior differences:   1. permission on the assignee will be verified in this API. 2. Hierarchy lookup (project->folder->organization) happens in this API. 3. Parent here is `projects/*/locations/*`, instead of `projects/*/locations/*reservations/*`.   Authorization scopes  Requires one of the following OAuth scopes:   * `https://www.googleapis.com/auth/bigquery` * `https://www.googleapis.com/auth/cloud-platform`   For more information, see the [Authentication Overview](/docs/authentication#authorization-gcp). |

| SearchAssignments |
| --- |
| This item is deprecated!  `rpc SearchAssignments(SearchAssignmentsRequest) returns (SearchAssignmentsResponse)`  Deprecated: Looks up assignments for a specified resource for a particular region. If the request is about a project:   1. Assignments created on the project will be returned if they exist. 2. Otherwise assignments created on the closest ancestor will be returned. 3. Assignments for different JobTypes will all be returned.   The same logic applies if the request is about a folder.  If the request is about an organization, then assignments created on the organization will be returned (organization doesn't have ancestors).  Comparing to ListAssignments, there are some behavior differences:   1. permission on the assignee will be verified in this API. 2. Hierarchy lookup (project->folder->organization) happens in this API. 3. Parent here is `projects/*/locations/*`, instead of `projects/*/locations/*reservations/*`.   **Note** "-" cannot be used for projects nor locations.  Authorization scopes  Requires one of the following OAuth scopes:   * `https://www.googleapis.com/auth/bigquery` * `https://www.googleapis.com/auth/cloud-platform`   For more information, see the [Authentication Overview](/docs/authentication#authorization-gcp). |

| SetIamPolicy |
| --- |
| `rpc SetIamPolicy(SetIamPolicyRequest) returns (Policy)`  Sets an access control policy for a resource. Replaces any existing policy.  Supported resources are: - Reservations  To call this method, you must have the following Google IAM permissions:   * `bigqueryreservation.reservations.setIamPolicy` to set policies on reservations.   Authorization scopes  Requires one of the following OAuth scopes:   * `https://www.googleapis.com/auth/bigquery` * `https://www.googleapis.com/auth/cloud-platform`   For more information, see the [Authentication Overview](/docs/authentication#authorization-gcp). |

| SplitCapacityCommitment |
| --- |
| `rpc SplitCapacityCommitment(SplitCapacityCommitmentRequest) returns (SplitCapacityCommitmentResponse)`  Splits capacity commitment to two commitments of the same plan and `commitment_end_time`.  A common use case is to enable downgrading commitments.  For example, in order to downgrade from 10000 slots to 8000, you might split a 10000 capacity commitment into commitments of 2000 and 8000. Then, you delete the first one after the commitment end time passes.  Authorization scopes  Requires one of the following OAuth scopes:   * `https://www.googleapis.com/auth/bigquery` * `https://www.googleapis.com/auth/cloud-platform`   For more information, see the [Authentication Overview](/docs/authentication#authorization-gcp). |

| TestIamPermissions |
| --- |
| `rpc TestIamPermissions(TestIamPermissionsRequest) returns (TestIamPermissionsResponse)`  Gets your permissions on a resource. Returns an empty set of permissions if the resource doesn't exist.  Supported resources are: - Reservations  No Google IAM permissions are required to call this method.  Authorization scopes  Requires one of the following OAuth scopes:   * `https://www.googleapis.com/auth/bigquery` * `https://www.googleapis.com/auth/cloud-platform`   For more information, see the [Authentication Overview](/docs/authentication#authorization-gcp). |

| UpdateAssignment |
| --- |
| `rpc UpdateAssignment(UpdateAssignmentRequest) returns (Assignment)`  Updates an existing assignment.  Only the `priority` field can be updated.  Authorization scopes  Requires one of the following OAuth scopes:   * `https://www.googleapis.com/auth/bigquery` * `https://www.googleapis.com/auth/cloud-platform`   For more information, see the [Authentication Overview](/docs/authentication#authorization-gcp). |

| UpdateBiReservation |
| --- |
| `rpc UpdateBiReservation(UpdateBiReservationRequest) returns (BiReservation)`  Updates a BI reservation.  Only fields specified in the `field_mask` are updated.  A singleton BI reservation always exists with default size 0. In order to reserve BI capacity it needs to be updated to an amount greater than 0. In order to release BI capacity reservation size must be set to 0.  Authorization scopes  Requires one of the following OAuth scopes:   * `https://www.googleapis.com/auth/bigquery` * `https://www.googleapis.com/auth/cloud-platform`   For more information, see the [Authentication Overview](/docs/authentication#authorization-gcp). |

| UpdateCapacityCommitment |
| --- |
| `rpc UpdateCapacityCommitment(UpdateCapacityCommitmentRequest) returns (CapacityCommitment)`  Updates an existing capacity commitment.  Only `plan` and `renewal_plan` fields can be updated.  Plan can only be changed to a plan of a longer commitment period. Attempting to change to a plan with shorter commitment period will fail with the error code `google.rpc.Code.FAILED_PRECONDIT` |