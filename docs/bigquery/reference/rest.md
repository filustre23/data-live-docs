* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback

# BigQuery API Stay organized with collections Save and categorize content based on your preferences.

A data platform for customers to create, manage, share and query data.

* [REST Resource: v2.datasets](#v2.datasets)
* [REST Resource: v2.jobs](#v2.jobs)
* [REST Resource: v2.models](#v2.models)
* [REST Resource: v2.projects](#v2.projects)
* [REST Resource: v2.routines](#v2.routines)
* [REST Resource: v2.rowAccessPolicies](#v2.rowAccessPolicies)
* [REST Resource: v2.tabledata](#v2.tabledata)
* [REST Resource: v2.tables](#v2.tables)

## Service: bigquery.googleapis.com

To call this service, we recommend that you use the Google-provided [client libraries](https://cloud.google.com/apis/docs/client-libraries-explained). If your application needs to use your own libraries to call this service, use the following information when you make the API requests.

### Discovery document

A [Discovery Document](https://developers.google.com/discovery/v1/reference/apis) is a machine-readable specification for describing and consuming REST APIs. It is used to build client libraries, IDE plugins, and other tools that interact with Google APIs. One service may provide multiple discovery documents. This service provides the following discovery document:

* <https://bigquery.googleapis.com/$discovery/rest?version=v2>

### Service endpoint

A [service endpoint](https://cloud.google.com/apis/design/glossary#api_service_endpoint) is a base URL that specifies the network address of an API service. One service might have multiple service endpoints. This service has the following service endpoint and all URIs below are relative to this service endpoint:

* `https://bigquery.googleapis.com`

## REST Resource: [v2.datasets](/bigquery/docs/reference/rest/v2/datasets)

| Methods | |
| --- | --- |
| `delete` | `DELETE /bigquery/v2/projects/{projectId}/datasets/{datasetId}`   Deletes the dataset specified by the datasetId value. |
| `get` | `GET /bigquery/v2/projects/{projectId}/datasets/{datasetId}`   Returns the dataset specified by datasetID. |
| `insert` | `POST /bigquery/v2/projects/{projectId}/datasets`   Creates a new empty dataset. |
| `list` | `GET /bigquery/v2/projects/{projectId}/datasets`   Lists all datasets in the specified project to which the user has been granted the READER dataset role. |
| `patch` | `PATCH /bigquery/v2/projects/{projectId}/datasets/{datasetId}`   Updates information in an existing dataset. |
| `undelete` | `POST /bigquery/v2/projects/{projectId}/datasets/{datasetId}:undelete`   Undeletes a dataset which is within time travel window based on datasetId. |
| `update` | `PUT /bigquery/v2/projects/{projectId}/datasets/{datasetId}`   Updates information in an existing dataset. |

## REST Resource: [v2.jobs](/bigquery/docs/reference/rest/v2/jobs)

| Methods | |
| --- | --- |
| `cancel` | `POST /bigquery/v2/projects/{projectId}/jobs/{jobId}/cancel`   Requests that a job be cancelled. |
| `delete` | `DELETE /bigquery/v2/projects/{projectId}/jobs/{jobId}/delete`   Requests the deletion of the metadata of a job. |
| `get` | `GET /bigquery/v2/projects/{projectId}/jobs/{jobId}`   Returns information about a specific job. |
| `getQueryResults` | `GET /bigquery/v2/projects/{projectId}/queries/{jobId}`   RPC to get the results of a query job. |
| `insert` | `POST /bigquery/v2/projects/{projectId}/jobs`   `POST /upload/bigquery/v2/projects/{projectId}/jobs`   Starts a new asynchronous job. |
| `list` | `GET /bigquery/v2/projects/{projectId}/jobs`   Lists all jobs that you started in the specified project. |
| `query` | `POST /bigquery/v2/projects/{projectId}/queries`   Runs a BigQuery SQL query synchronously and returns query results if the query completes within a specified timeout. |

## REST Resource: [v2.models](/bigquery/docs/reference/rest/v2/models)

| Methods | |
| --- | --- |
| `delete` | `DELETE /bigquery/v2/projects/{projectId}/datasets/{datasetId}/models/{modelId}`   Deletes the model specified by modelId from the dataset. |
| `get` | `GET /bigquery/v2/projects/{projectId}/datasets/{datasetId}/models/{modelId}`   Gets the specified model resource by model ID. |
| `list` | `GET /bigquery/v2/projects/{projectId}/datasets/{datasetId}/models`   Lists all models in the specified dataset. |
| `patch` | `PATCH /bigquery/v2/projects/{projectId}/datasets/{datasetId}/models/{modelId}`   Patch specific fields in the specified model. |

## REST Resource: [v2.projects](/bigquery/docs/reference/rest/v2/projects)

| Methods | |
| --- | --- |
| `getServiceAccount` | `GET /bigquery/v2/projects/{projectId}/serviceAccount`   RPC to get the service account for a project used for interactions with Google Cloud KMS |
| `list` | `GET /bigquery/v2/projects`   RPC to list projects to which the user has been granted any project role. |

## REST Resource: [v2.routines](/bigquery/docs/reference/rest/v2/routines)

| Methods | |
| --- | --- |
| `delete` | `DELETE /bigquery/v2/projects/{projectId}/datasets/{datasetId}/routines/{routineId}`   Deletes the routine specified by routineId from the dataset. |
| `get` | `GET /bigquery/v2/projects/{projectId}/datasets/{datasetId}/routines/{routineId}`   Gets the specified routine resource by routine ID. |
| `getIamPolicy` | `POST /bigquery/v2/{resource=projects/*/datasets/*/routines/*}:getIamPolicy`   Gets the access control policy for a resource. |
| `insert` | `POST /bigquery/v2/projects/{projectId}/datasets/{datasetId}/routines`   Creates a new routine in the dataset. |
| `list` | `GET /bigquery/v2/projects/{projectId}/datasets/{datasetId}/routines`   Lists all routines in the specified dataset. |
| `setIamPolicy` | `POST /bigquery/v2/{resource=projects/*/datasets/*/routines/*}:setIamPolicy`   Sets the access control policy on the specified resource. |
| `testIamPermissions` | `POST /bigquery/v2/{resource=projects/*/datasets/*/routines/*}:testIamPermissions`   Returns permissions that a caller has on the specified resource. |
| `update` | `PUT /bigquery/v2/projects/{projectId}/datasets/{datasetId}/routines/{routineId}`   Updates information in an existing routine. |

## REST Resource: [v2.rowAccessPolicies](/bigquery/docs/reference/rest/v2/rowAccessPolicies)

| Methods | |
| --- | --- |
| `batchDelete` | `POST /bigquery/v2/projects/{projectId}/datasets/{datasetId}/tables/{tableId}/rowAccessPolicies:batchDelete`   Deletes provided row access policies. |
| `delete` | `DELETE /bigquery/v2/projects/{projectId}/datasets/{datasetId}/tables/{tableId}/rowAccessPolicies/{policyId}`   Deletes a row access policy. |
| `get` | `GET /bigquery/v2/projects/{projectId}/datasets/{datasetId}/tables/{tableId}/rowAccessPolicies/{policyId}`   Gets the specified row access policy by policy ID. |
| `getIamPolicy` | `POST /bigquery/v2/{resource=projects/*/datasets/*/tables/*/rowAccessPolicies/*}:getIamPolicy`   Gets the access control policy for a resource. |
| `insert` | `POST /bigquery/v2/projects/{projectId}/datasets/{datasetId}/tables/{tableId}/rowAccessPolicies`   Creates a row access policy. |
| `list` | `GET /bigquery/v2/projects/{projectId}/datasets/{datasetId}/tables/{tableId}/rowAccessPolicies`   Lists all row access policies on the specified table. |
| `testIamPermissions` | `POST /bigquery/v2/{resource=projects/*/datasets/*/tables/*/rowAccessPolicies/*}:testIamPermissions`   Returns permissions that a caller has on the specified resource. |
| `update` | `PUT /bigquery/v2/projects/{projectId}/datasets/{datasetId}/tables/{tableId}/rowAccessPolicies/{policyId}`   Updates a row access policy. |

## REST Resource: [v2.tabledata](/bigquery/docs/reference/rest/v2/tabledata)

| Methods | |
| --- | --- |
| `insertAll` | `POST /bigquery/v2/projects/{projectId}/datasets/{datasetId}/tables/{tableId}/insertAll`   Streams data into BigQuery one record at a time without needing to run a load job. |
| `list` | `GET /bigquery/v2/projects/{projectId}/datasets/{datasetId}/tables/{tableId}/data`   List the content of a table in rows. |

## REST Resource: [v2.tables](/bigquery/docs/reference/rest/v2/tables)

| Methods | |
| --- | --- |
| `delete` | `DELETE /bigquery/v2/projects/{projectId}/datasets/{datasetId}/tables/{tableId}`   Deletes the table specified by tableId from the dataset. |
| `get` | `GET /bigquery/v2/projects/{projectId}/datasets/{datasetId}/tables/{tableId}`   Gets the specified table resource by table ID. |
| `getIamPolicy` | `POST /bigquery/v2/{resource=projects/*/datasets/*/tables/*}:getIamPolicy`   Gets the access control policy for a resource. |
| `insert` | `POST /bigquery/v2/projects/{projectId}/datasets/{datasetId}/tables`   Creates a new, empty table in the dataset. |
| `list` | `GET /bigquery/v2/projects/{projectId}/datasets/{datasetId}/tables`   Lists all tables in the specified dataset. |
| `patch` | `PATCH /bigquery/v2/projects/{projectId}/datasets/{datasetId}/tables/{tableId}`   Updates information in an existing table. |
| `setIamPolicy` | `POST /bigquery/v2/{resource=projects/*/datasets/*/tables/*}:setIamPolicy`   Sets the access control policy on the specified resource. |
| `testIamPermissions` | `POST /bigquery/v2/{resource=projects/*/datasets/*/tables/*}:testIamPermissions`   Returns permissions that a caller has on the specified resource. |
| `update` | `PUT /bigquery/v2/projects/{projectId}/datasets/{datasetId}/tables/{tableId}`   Updates information in an existing table. |




Send feedback

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2026-03-25 UTC.




Need to tell us more?

[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Hard to understand","hardToUnderstand","thumb-down"],["Incorrect information or sample code","incorrectInformationOrSampleCode","thumb-down"],["Missing the information/samples I need","missingTheInformationSamplesINeed","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2026-03-25 UTC."],[],[]]