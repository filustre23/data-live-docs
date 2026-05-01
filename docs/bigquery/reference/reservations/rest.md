* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback

# BigQuery Reservation API Stay organized with collections Save and categorize content based on your preferences.

A service to modify your BigQuery reservations.

* [REST Resource: v1.projects.locations](#v1.projects.locations)
* [REST Resource: v1.projects.locations.capacityCommitments](#v1.projects.locations.capacityCommitments)
* [REST Resource: v1.projects.locations.reservationGroups](#v1.projects.locations.reservationGroups)
* [REST Resource: v1.projects.locations.reservations](#v1.projects.locations.reservations)
* [REST Resource: v1.projects.locations.reservations.assignments](#v1.projects.locations.reservations.assignments)

## Service: bigqueryreservation.googleapis.com

To call this service, we recommend that you use the Google-provided [client libraries](https://cloud.google.com/apis/docs/client-libraries-explained). If your application needs to use your own libraries to call this service, use the following information when you make the API requests.

### Discovery document

A [Discovery Document](https://developers.google.com/discovery/v1/reference/apis) is a machine-readable specification for describing and consuming REST APIs. It is used to build client libraries, IDE plugins, and other tools that interact with Google APIs. One service may provide multiple discovery documents. This service provides the following discovery document:

* <https://bigqueryreservation.googleapis.com/$discovery/rest?version=v1>

### Service endpoint

A [service endpoint](https://cloud.google.com/apis/design/glossary#api_service_endpoint) is a base URL that specifies the network address of an API service. One service might have multiple service endpoints. This service has the following service endpoint and all URIs below are relative to this service endpoint:

* `https://bigqueryreservation.googleapis.com`

## REST Resource: [v1.projects.locations](/bigquery/docs/reference/reservations/rest/v1/projects.locations)

| Methods | |
| --- | --- |
| `getBiReservation` | `GET /v1/{name=projects/*/locations/*/biReservation}`   Retrieves a BI reservation. |
| `searchAllAssignments` | `GET /v1/{parent=projects/*/locations/*}:searchAllAssignments`   Looks up assignments for a specified resource for a particular region. |
| `searchAssignments  (deprecated)` | `GET /v1/{parent=projects/*/locations/*}:searchAssignments`   Deprecated: Looks up assignments for a specified resource for a particular region. |
| `updateBiReservation` | `PATCH /v1/{biReservation.name=projects/*/locations/*/biReservation}`   Updates a BI reservation. |

## REST Resource: [v1.projects.locations.capacityCommitments](/bigquery/docs/reference/reservations/rest/v1/projects.locations.capacityCommitments)

| Methods | |
| --- | --- |
| `create` | `POST /v1/{parent=projects/*/locations/*}/capacityCommitments`   Creates a new capacity commitment resource. |
| `delete` | `DELETE /v1/{name=projects/*/locations/*/capacityCommitments/*}`   Deletes a capacity commitment. |
| `get` | `GET /v1/{name=projects/*/locations/*/capacityCommitments/*}`   Returns information about the capacity commitment. |
| `list` | `GET /v1/{parent=projects/*/locations/*}/capacityCommitments`   Lists all the capacity commitments for the admin project. |
| `merge` | `POST /v1/{parent=projects/*/locations/*}/capacityCommitments:merge`   Merges capacity commitments of the same plan into a single commitment. |
| `patch` | `PATCH /v1/{capacityCommitment.name=projects/*/locations/*/capacityCommitments/*}`   Updates an existing capacity commitment. |
| `split` | `POST /v1/{name=projects/*/locations/*/capacityCommitments/*}:split`   Splits capacity commitment to two commitments of the same plan and `commitment_end_time`. |

## REST Resource: [v1.projects.locations.reservationGroups](/bigquery/docs/reference/reservations/rest/v1/projects.locations.reservationGroups)

| Methods | |
| --- | --- |
| `create` | `POST /v1/{parent=projects/*/locations/*}/reservationGroups`   Creates a new reservation group. |
| `delete` | `DELETE /v1/{name=projects/*/locations/*/reservationGroups/*}`   Deletes a reservation. |
| `get` | `GET /v1/{name=projects/*/locations/*/reservationGroups/*}`   Returns information about the reservation group. |
| `list` | `GET /v1/{parent=projects/*/locations/*}/reservationGroups`   Lists all the reservation groups for the project in the specified location. |

## REST Resource: [v1.projects.locations.reservations](/bigquery/docs/reference/reservations/rest/v1/projects.locations.reservations)

| Methods | |
| --- | --- |
| `create` | `POST /v1/{parent=projects/*/locations/*}/reservations`   Creates a new reservation resource. |
| `delete` | `DELETE /v1/{name=projects/*/locations/*/reservations/*}`   Deletes a reservation. |
| `failoverReservation` | `POST /v1/{name=projects/*/locations/*/reservations/*}:failoverReservation`   Fail over a reservation to the secondary location. |
| `get` | `GET /v1/{name=projects/*/locations/*/reservations/*}`   Returns information about the reservation. |
| `getIamPolicy` | `GET /v1/{resource=projects/*/locations/*/reservations/*}:getIamPolicy`   Gets the access control policy for a resource. |
| `list` | `GET /v1/{parent=projects/*/locations/*}/reservations`   Lists all the reservations for the project in the specified location. |
| `patch` | `PATCH /v1/{reservation.name=projects/*/locations/*/reservations/*}`   Updates an existing reservation resource. |
| `setIamPolicy` | `POST /v1/{resource=projects/*/locations/*/reservations/*}:setIamPolicy`   Sets an access control policy for a resource. |
| `testIamPermissions` | `POST /v1/{resource=projects/*/locations/*/reservations/*}:testIamPermissions`   Gets your permissions on a resource. |

## REST Resource: [v1.projects.locations.reservations.assignments](/bigquery/docs/reference/reservations/rest/v1/projects.locations.reservations.assignments)

| Methods | |
| --- | --- |
| `create` | `POST /v1/{parent=projects/*/locations/*/reservations/*}/assignments`   Creates an assignment object which allows the given project to submit jobs of a certain type using slots from the specified reservation. |
| `delete` | `DELETE /v1/{name=projects/*/locations/*/reservations/*/assignments/*}`   Deletes a assignment. |
| `getIamPolicy` | `GET /v1/{resource=projects/*/locations/*/reservations/*/assignments/*}:getIamPolicy`   Gets the access control policy for a resource. |
| `list` | `GET /v1/{parent=projects/*/locations/*/reservations/*}/assignments`   Lists assignments. |
| `move` | `POST /v1/{name=projects/*/locations/*/reservations/*/assignments/*}:move`   Moves an assignment under a new reservation. |
| `patch` | `PATCH /v1/{assignment.name=projects/*/locations/*/reservations/*/assignments/*}`   Updates an existing assignment. |
| `setIamPolicy` | `POST /v1/{resource=projects/*/locations/*/reservations/*/assignments/*}:setIamPolicy`   Sets an access control policy for a resource. |
| `testIamPermissions` | `POST /v1/{resource=projects/*/locations/*/reservations/*/assignments/*}:testIamPermissions`   Gets your permissions on a resource. |




Send feedback

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2025-12-19 UTC.




Need to tell us more?

[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Hard to understand","hardToUnderstand","thumb-down"],["Incorrect information or sample code","incorrectInformationOrSampleCode","thumb-down"],["Missing the information/samples I need","missingTheInformationSamplesINeed","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2025-12-19 UTC."],[],[]]