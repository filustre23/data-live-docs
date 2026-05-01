* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback

# BigQuery Migration API Stay organized with collections Save and categorize content based on your preferences.

The migration service, exposing apis for migration jobs operations, and agent management.

* [REST Resource: v2alpha.projects.locations.workflows](#v2alpha.projects.locations.workflows)
* [REST Resource: v2alpha.projects.locations.workflows.subtasks](#v2alpha.projects.locations.workflows.subtasks)
* [REST Resource: v2.projects.locations.workflows](#v2.projects.locations.workflows)
* [REST Resource: v2.projects.locations.workflows.subtasks](#v2.projects.locations.workflows.subtasks)

## Service: bigquerymigration.googleapis.com

To call this service, we recommend that you use the Google-provided [client libraries](https://cloud.google.com/apis/docs/client-libraries-explained). If your application needs to use your own libraries to call this service, use the following information when you make the API requests.

### Discovery document

A [Discovery Document](https://developers.google.com/discovery/v1/reference/apis) is a machine-readable specification for describing and consuming REST APIs. It is used to build client libraries, IDE plugins, and other tools that interact with Google APIs. One service may provide multiple discovery documents. This service provides the following discovery documents:

* <https://bigquerymigration.googleapis.com/$discovery/rest?version=v2>
* <https://bigquerymigration.googleapis.com/$discovery/rest?version=v2alpha>

### Service endpoint

A [service endpoint](https://cloud.google.com/apis/design/glossary#api_service_endpoint) is a base URL that specifies the network address of an API service. One service might have multiple service endpoints. This service has the following service endpoint and all URIs below are relative to this service endpoint:

* `https://bigquerymigration.googleapis.com`

## REST Resource: [v2alpha.projects.locations.workflows](/bigquery/docs/reference/migration/rest/v2alpha/projects.locations.workflows)

| Methods | |
| --- | --- |
| `create` | `POST /v2alpha/{parent=projects/*/locations/*}/workflows`   Creates a migration workflow. |
| `delete` | `DELETE /v2alpha/{name=projects/*/locations/*/workflows/*}`   Deletes a migration workflow by name. |
| `get` | `GET /v2alpha/{name=projects/*/locations/*/workflows/*}`   Gets a previously created migration workflow. |
| `list` | `GET /v2alpha/{parent=projects/*/locations/*}/workflows`   Lists previously created migration workflow. |
| `start` | `POST /v2alpha/{name=projects/*/locations/*/workflows/*}:start`   Starts a previously created migration workflow. |

## REST Resource: [v2alpha.projects.locations.workflows.subtasks](/bigquery/docs/reference/migration/rest/v2alpha/projects.locations.workflows.subtasks)

| Methods | |
| --- | --- |
| `get` | `GET /v2alpha/{name=projects/*/locations/*/workflows/*/subtasks/*}`   Gets a previously created migration subtask. |
| `list` | `GET /v2alpha/{parent=projects/*/locations/*/workflows/*}/subtasks`   Lists previously created migration subtasks. |

## REST Resource: [v2.projects.locations.workflows](/bigquery/docs/reference/migration/rest/v2/projects.locations.workflows)

| Methods | |
| --- | --- |
| `create` | `POST /v2/{parent=projects/*/locations/*}/workflows`   Creates a migration workflow. |
| `delete` | `DELETE /v2/{name=projects/*/locations/*/workflows/*}`   Deletes a migration workflow by name. |
| `get` | `GET /v2/{name=projects/*/locations/*/workflows/*}`   Gets a previously created migration workflow. |
| `list` | `GET /v2/{parent=projects/*/locations/*}/workflows`   Lists previously created migration workflow. |
| `start` | `POST /v2/{name=projects/*/locations/*/workflows/*}:start`   Starts a previously created migration workflow. |

## REST Resource: [v2.projects.locations.workflows.subtasks](/bigquery/docs/reference/migration/rest/v2/projects.locations.workflows.subtasks)

| Methods | |
| --- | --- |
| `get` | `GET /v2/{name=projects/*/locations/*/workflows/*/subtasks/*}`   Gets a previously created migration subtask. |
| `list` | `GET /v2/{parent=projects/*/locations/*/workflows/*}/subtasks`   Lists previously created migration subtasks. |




Send feedback

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2025-07-02 UTC.




Need to tell us more?

[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Hard to understand","hardToUnderstand","thumb-down"],["Incorrect information or sample code","incorrectInformationOrSampleCode","thumb-down"],["Missing the information/samples I need","missingTheInformationSamplesINeed","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2025-07-02 UTC."],[],[]]