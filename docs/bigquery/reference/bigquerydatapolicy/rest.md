* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback

# BigQuery Data Policy API Stay organized with collections Save and categorize content based on your preferences.

Allows users to manage BigQuery data policies.

* [REST Resource: v2beta1.projects.locations.dataPolicies](#v2beta1.projects.locations.dataPolicies)
* [REST Resource: v2.projects.locations.dataPolicies](#v2.projects.locations.dataPolicies)
* [REST Resource: v1beta1.projects.locations.dataPolicies](#v1beta1.projects.locations.dataPolicies)
* [REST Resource: v1.projects.locations.dataPolicies](#v1.projects.locations.dataPolicies)

## Service: bigquerydatapolicy.googleapis.com

To call this service, we recommend that you use the Google-provided [client libraries](https://cloud.google.com/apis/docs/client-libraries-explained). If your application needs to use your own libraries to call this service, use the following information when you make the API requests.

### Discovery document

A [Discovery Document](https://developers.google.com/discovery/v1/reference/apis) is a machine-readable specification for describing and consuming REST APIs. It is used to build client libraries, IDE plugins, and other tools that interact with Google APIs. One service may provide multiple discovery documents. This service provides the following discovery documents:

* <https://bigquerydatapolicy.googleapis.com/$discovery/rest?version=v2>
* <https://bigquerydatapolicy.googleapis.com/$discovery/rest?version=v2beta1>
* <https://bigquerydatapolicy.googleapis.com/$discovery/rest?version=v1>
* <https://bigquerydatapolicy.googleapis.com/$discovery/rest?version=v1beta1>

### Service endpoint

A [service endpoint](https://cloud.google.com/apis/design/glossary#api_service_endpoint) is a base URL that specifies the network address of an API service. One service might have multiple service endpoints. This service has the following service endpoint and all URIs below are relative to this service endpoint:

* `https://bigquerydatapolicy.googleapis.com`

## REST Resource: [v2beta1.projects.locations.dataPolicies](/bigquery/docs/reference/bigquerydatapolicy/rest/v2beta1/projects.locations.dataPolicies)

| Methods | |
| --- | --- |
| `addGrantees` | `POST /v2beta1/{dataPolicy=projects/*/locations/*/dataPolicies/*}:addGrantees`   Adds new grantees to a data policy. |
| `create` | `POST /v2beta1/{parent=projects/*/locations/*}/dataPolicies`   Creates a new data policy under a project with the given `data_policy_id` (used as the display name), and data policy type. |
| `delete` | `DELETE /v2beta1/{name=projects/*/locations/*/dataPolicies/*}`   Deletes the data policy specified by its resource name. |
| `get` | `GET /v2beta1/{name=projects/*/locations/*/dataPolicies/*}`   Gets the data policy specified by its resource name. |
| `getIamPolicy` | `POST /v2beta1/{resource=projects/*/locations/*/dataPolicies/*}:getIamPolicy`   Gets the IAM policy for the specified data policy. |
| `list` | `GET /v2beta1/{parent=projects/*/locations/*}/dataPolicies`   List all of the data policies in the specified parent project. |
| `patch` | `PATCH /v2beta1/{dataPolicy.name=projects/*/locations/*/dataPolicies/*}`   Updates the metadata for an existing data policy. |
| `removeGrantees` | `POST /v2beta1/{dataPolicy=projects/*/locations/*/dataPolicies/*}:removeGrantees`   Removes grantees from a data policy. |
| `setIamPolicy` | `POST /v2beta1/{resource=projects/*/locations/*/dataPolicies/*}:setIamPolicy`   Sets the IAM policy for the specified data policy. |
| `testIamPermissions` | `POST /v2beta1/{resource=projects/*/locations/*/dataPolicies/*}:testIamPermissions`   Returns the caller's permission on the specified data policy resource. |

## REST Resource: [v2.projects.locations.dataPolicies](/bigquery/docs/reference/bigquerydatapolicy/rest/v2/projects.locations.dataPolicies)

| Methods | |
| --- | --- |
| `addGrantees` | `POST /v2/{dataPolicy=projects/*/locations/*/dataPolicies/*}:addGrantees`   Adds new grantees to a data policy. |
| `create` | `POST /v2/{parent=projects/*/locations/*}/dataPolicies`   Creates a new data policy under a project with the given `data_policy_id` (used as the display name), and data policy type. |
| `delete` | `DELETE /v2/{name=projects/*/locations/*/dataPolicies/*}`   Deletes the data policy specified by its resource name. |
| `get` | `GET /v2/{name=projects/*/locations/*/dataPolicies/*}`   Gets the data policy specified by its resource name. |
| `getIamPolicy` | `POST /v2/{resource=projects/*/locations/*/dataPolicies/*}:getIamPolicy`   Gets the IAM policy for the specified data policy. |
| `list` | `GET /v2/{parent=projects/*/locations/*}/dataPolicies`   List all of the data policies in the specified parent project. |
| `patch` | `PATCH /v2/{dataPolicy.name=projects/*/locations/*/dataPolicies/*}`   Updates the metadata for an existing data policy. |
| `removeGrantees` | `POST /v2/{dataPolicy=projects/*/locations/*/dataPolicies/*}:removeGrantees`   Removes grantees from a data policy. |
| `setIamPolicy` | `POST /v2/{resource=projects/*/locations/*/dataPolicies/*}:setIamPolicy`   Sets the IAM policy for the specified data policy. |
| `testIamPermissions` | `POST /v2/{resource=projects/*/locations/*/dataPolicies/*}:testIamPermissions`   Returns the caller's permission on the specified data policy resource. |

## REST Resource: [v1beta1.projects.locations.dataPolicies](/bigquery/docs/reference/bigquerydatapolicy/rest/v1beta1/projects.locations.dataPolicies)

| Methods | |
| --- | --- |
| `create` | `POST /v1beta1/{parent=projects/*/locations/*}/dataPolicies`   Creates a new data policy under a project with the given `dataPolicyId` (used as the display name), policy tag, and data policy type. |
| `delete` | `DELETE /v1beta1/{name=projects/*/locations/*/dataPolicies/*}`   Deletes the data policy specified by its resource name. |
| `get` | `GET /v1beta1/{name=projects/*/locations/*/dataPolicies/*}`   Gets the data policy specified by its resource name. |
| `getIamPolicy` | `POST /v1beta1/{resource=projects/*/locations/*/dataPolicies/*}:getIamPolicy`   Gets the IAM policy for the specified data policy. |
| `list` | `GET /v1beta1/{parent=projects/*/locations/*}/dataPolicies`   List all of the data policies in the specified parent project. |
| `patch` | `PATCH /v1beta1/{dataPolicy.name=projects/*/locations/*/dataPolicies/*}`   Updates the metadata for an existing data policy. |
| `setIamPolicy` | `POST /v1beta1/{resource=projects/*/locations/*/dataPolicies/*}:setIamPolicy`   Sets the IAM policy for the specified data policy. |
| `testIamPermissions` | `POST /v1beta1/{resource=projects/*/locations/*/dataPolicies/*}:testIamPermissions`   Returns the caller's permission on the specified data policy resource. |

## REST Resource: [v1.projects.locations.dataPolicies](/bigquery/docs/reference/bigquerydatapolicy/rest/v1/projects.locations.dataPolicies)

| Methods | |
| --- | --- |
| `create` | `POST /v1/{parent=projects/*/locations/*}/dataPolicies`   Creates a new data policy under a project with the given `dataPolicyId` (used as the display name), policy tag, and data policy type. |
| `delete` | `DELETE /v1/{name=projects/*/locations/*/dataPolicies/*}`   Deletes the data policy specified by its resource name. |
| `get` | `GET /v1/{name=projects/*/locations/*/dataPolicies/*}`   Gets the data policy specified by its resource name. |
| `getIamPolicy` | `POST /v1/{resource=projects/*/locations/*/dataPolicies/*}:getIamPolicy`   Gets the IAM policy for the specified data policy. |
| `list` | `GET /v1/{parent=projects/*/locations/*}/dataPolicies`   List all of the data policies in the specified parent project. |
| `patch` | `PATCH /v1/{dataPolicy.name=projects/*/locations/*/dataPolicies/*}`   Updates the metadata for an existing data policy. |
| `rename` | `POST /v1/{name=projects/*/locations/*/dataPolicies/*}:rename`   Renames the id (display name) of the specified data policy. |
| `setIamPolicy` | `POST /v1/{resource=projects/*/locations/*/dataPolicies/*}:setIamPolicy`   Sets the IAM policy for the specified data policy. |
| `testIamPermissions` | `POST /v1/{resource=projects/*/locations/*/dataPolicies/*}:testIamPermissions`   Returns the caller's permission on the specified data policy resource. |




Send feedback

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2025-07-28 UTC.




Need to tell us more?

[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Hard to understand","hardToUnderstand","thumb-down"],["Incorrect information or sample code","incorrectInformationOrSampleCode","thumb-down"],["Missing the information/samples I need","missingTheInformationSamplesINeed","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2025-07-28 UTC."],[],[]]