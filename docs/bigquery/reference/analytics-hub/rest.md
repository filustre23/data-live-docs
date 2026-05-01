* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback

# Analytics Hub API Stay organized with collections Save and categorize content based on your preferences.

Exchange data and analytics assets securely and efficiently.

* [REST Resource: v1beta1.organizations.locations.dataExchanges](#v1beta1.organizations.locations.dataExchanges)
* [REST Resource: v1beta1.projects.locations.dataExchanges](#v1beta1.projects.locations.dataExchanges)
* [REST Resource: v1beta1.projects.locations.dataExchanges.listings](#v1beta1.projects.locations.dataExchanges.listings)
* [REST Resource: v1.organizations.locations.dataExchanges](#v1.organizations.locations.dataExchanges)
* [REST Resource: v1.projects.locations.dataExchanges](#v1.projects.locations.dataExchanges)
* [REST Resource: v1.projects.locations.dataExchanges.listings](#v1.projects.locations.dataExchanges.listings)
* [REST Resource: v1.projects.locations.dataExchanges.queryTemplates](#v1.projects.locations.dataExchanges.queryTemplates)
* [REST Resource: v1.projects.locations.subscriptions](#v1.projects.locations.subscriptions)

## Service: analyticshub.googleapis.com

To call this service, we recommend that you use the Google-provided [client libraries](https://cloud.google.com/apis/docs/client-libraries-explained). If your application needs to use your own libraries to call this service, use the following information when you make the API requests.

### Discovery document

A [Discovery Document](https://developers.google.com/discovery/v1/reference/apis) is a machine-readable specification for describing and consuming REST APIs. It is used to build client libraries, IDE plugins, and other tools that interact with Google APIs. One service may provide multiple discovery documents. This service provides the following discovery documents:

* <https://analyticshub.googleapis.com/$discovery/rest?version=v1>
* <https://analyticshub.googleapis.com/$discovery/rest?version=v1beta1>

### Service endpoint

A [service endpoint](https://cloud.google.com/apis/design/glossary#api_service_endpoint) is a base URL that specifies the network address of an API service. One service might have multiple service endpoints. This service has the following service endpoint and all URIs below are relative to this service endpoint:

* `https://analyticshub.googleapis.com`

## REST Resource: [v1beta1.organizations.locations.dataExchanges](/bigquery/docs/reference/analytics-hub/rest/v1beta1/organizations.locations.dataExchanges)

| Methods | |
| --- | --- |
| `list` | `GET /v1beta1/{organization=organizations/*/locations/*}/dataExchanges`   Lists all data exchanges from projects in a given organization and location. |

## REST Resource: [v1beta1.projects.locations.dataExchanges](/bigquery/docs/reference/analytics-hub/rest/v1beta1/projects.locations.dataExchanges)

| Methods | |
| --- | --- |
| `create` | `POST /v1beta1/{parent=projects/*/locations/*}/dataExchanges`   Creates a new data exchange. |
| `delete` | `DELETE /v1beta1/{name=projects/*/locations/*/dataExchanges/*}`   Deletes an existing data exchange. |
| `get` | `GET /v1beta1/{name=projects/*/locations/*/dataExchanges/*}`   Gets the details of a data exchange. |
| `getIamPolicy` | `POST /v1beta1/{resource=projects/*/locations/*/dataExchanges/*}:getIamPolicy`   Gets the IAM policy. |
| `list` | `GET /v1beta1/{parent=projects/*/locations/*}/dataExchanges`   Lists all data exchanges in a given project and location. |
| `patch` | `PATCH /v1beta1/{dataExchange.name=projects/*/locations/*/dataExchanges/*}`   Updates an existing data exchange. |
| `setIamPolicy` | `POST /v1beta1/{resource=projects/*/locations/*/dataExchanges/*}:setIamPolicy`   Sets the IAM policy. |
| `testIamPermissions` | `POST /v1beta1/{resource=projects/*/locations/*/dataExchanges/*}:testIamPermissions`   Returns the permissions that a caller has. |

## REST Resource: [v1beta1.projects.locations.dataExchanges.listings](/bigquery/docs/reference/analytics-hub/rest/v1beta1/projects.locations.dataExchanges.listings)

| Methods | |
| --- | --- |
| `create` | `POST /v1beta1/{parent=projects/*/locations/*/dataExchanges/*}/listings`   Creates a new listing. |
| `delete` | `DELETE /v1beta1/{name=projects/*/locations/*/dataExchanges/*/listings/*}`   Deletes a listing. |
| `get` | `GET /v1beta1/{name=projects/*/locations/*/dataExchanges/*/listings/*}`   Gets the details of a listing. |
| `getIamPolicy` | `POST /v1beta1/{resource=projects/*/locations/*/dataExchanges/*/listings/*}:getIamPolicy`   Gets the IAM policy. |
| `list` | `GET /v1beta1/{parent=projects/*/locations/*/dataExchanges/*}/listings`   Lists all listings in a given project and location. |
| `patch` | `PATCH /v1beta1/{listing.name=projects/*/locations/*/dataExchanges/*/listings/*}`   Updates an existing listing. |
| `setIamPolicy` | `POST /v1beta1/{resource=projects/*/locations/*/dataExchanges/*/listings/*}:setIamPolicy`   Sets the IAM policy. |
| `subscribe` | `POST /v1beta1/{name=projects/*/locations/*/dataExchanges/*/listings/*}:subscribe`   Subscribes to a listing. |
| `testIamPermissions` | `POST /v1beta1/{resource=projects/*/locations/*/dataExchanges/*/listings/*}:testIamPermissions`   Returns the permissions that a caller has. |

## REST Resource: [v1.organizations.locations.dataExchanges](/bigquery/docs/reference/analytics-hub/rest/v1/organizations.locations.dataExchanges)

| Methods | |
| --- | --- |
| `list` | `GET /v1/{organization=organizations/*/locations/*}/dataExchanges`   Lists all data exchanges from projects in a given organization and location. |

## REST Resource: [v1.projects.locations.dataExchanges](/bigquery/docs/reference/analytics-hub/rest/v1/projects.locations.dataExchanges)

| Methods | |
| --- | --- |
| `create` | `POST /v1/{parent=projects/*/locations/*}/dataExchanges`   Creates a new data exchange. |
| `delete` | `DELETE /v1/{name=projects/*/locations/*/dataExchanges/*}`   Deletes an existing data exchange. |
| `get` | `GET /v1/{name=projects/*/locations/*/dataExchanges/*}`   Gets the details of a data exchange. |
| `getIamPolicy` | `POST /v1/{resource=projects/*/locations/*/dataExchanges/*}:getIamPolicy`   Gets the IAM policy. |
| `list` | `GET /v1/{parent=projects/*/locations/*}/dataExchanges`   Lists all data exchanges in a given project and location. |
| `listSubscriptions` | `GET /v1/{resource=projects/*/locations/*/dataExchanges/*}:listSubscriptions`   Lists all subscriptions on a given Data Exchange or Listing. |
| `patch` | `PATCH /v1/{dataExchange.name=projects/*/locations/*/dataExchanges/*}`   Updates an existing data exchange. |
| `setIamPolicy` | `POST /v1/{resource=projects/*/locations/*/dataExchanges/*}:setIamPolicy`   Sets the IAM policy. |
| `subscribe` | `POST /v1/{name=projects/*/locations/*/dataExchanges/*}:subscribe`   Creates a Subscription to a Data Clean Room. |
| `testIamPermissions` | `POST /v1/{resource=projects/*/locations/*/dataExchanges/*}:testIamPermissions`   Returns the permissions that a caller has. |

## REST Resource: [v1.projects.locations.dataExchanges.listings](/bigquery/docs/reference/analytics-hub/rest/v1/projects.locations.dataExchanges.listings)

| Methods | |
| --- | --- |
| `create` | `POST /v1/{parent=projects/*/locations/*/dataExchanges/*}/listings`   Creates a new listing. |
| `delete` | `DELETE /v1/{name=projects/*/locations/*/dataExchanges/*/listings/*}`   Deletes a listing. |
| `get` | `GET /v1/{name=projects/*/locations/*/dataExchanges/*/listings/*}`   Gets the details of a listing. |
| `getIamPolicy` | `POST /v1/{resource=projects/*/locations/*/dataExchanges/*/listings/*}:getIamPolicy`   Gets the IAM policy. |
| `list` | `GET /v1/{parent=projects/*/locations/*/dataExchanges/*}/listings`   Lists all listings in a given project and location. |
| `listSubscriptions` | `GET /v1/{resource=projects/*/locations/*/dataExchanges/*/listings/*}:listSubscriptions`   Lists all subscriptions on a given Data Exchange or Listing. |
| `patch` | `PATCH /v1/{listing.name=projects/*/locations/*/dataExchanges/*/listings/*}`   Updates an existing listing. |
| `setIamPolicy` | `POST /v1/{resource=projects/*/locations/*/dataExchanges/*/listings/*}:setIamPolicy`   Sets the IAM policy. |
| `subscribe` | `POST /v1/{name=projects/*/locations/*/dataExchanges/*/listings/*}:subscribe`   Subscribes to a listing. |
| `testIamPermissions` | `POST /v1/{resource=projects/*/locations/*/dataExchanges/*/listings/*}:testIamPermissions`   Returns the permissions that a caller has. |

## REST Resource: [v1.projects.locations.dataExchanges.queryTemplates](/bigquery/docs/reference/analytics-hub/rest/v1/projects.locations.dataExchanges.queryTemplates)

| Methods | |
| --- | --- |
| `approve` | `POST /v1/{name=projects/*/locations/*/dataExchanges/*/queryTemplates/*}:approve`   Approves a query template. |
| `create` | `POST /v1/{parent=projects/*/locations/*/dataExchanges/*}/queryTemplates`   Creates a new QueryTemplate |
| `delete` | `DELETE /v1/{name=projects/*/locations/*/dataExchanges/*/queryTemplates/*}`   Deletes a query template. |
| `get` | `GET /v1/{name=projects/*/locations/*/dataExchanges/*/queryTemplates/*}`   Gets a QueryTemplate |
| `list` | `GET /v1/{parent=projects/*/locations/*/dataExchanges/*}/queryTemplates`   Lists all QueryTemplates in a given project and location. |
| `patch` | `PATCH /v1/{queryTemplate.name=projects/*/locations/*/dataExchanges/*/queryTemplates/*}`   Updates an existing QueryTemplate |
| `submit` | `POST /v1/{name=projects/*/locations/*/dataExchanges/*/queryTemplates/*}:submit`   Submits a query template for approval. |

## REST Resource: [v1.projects.locations.subscriptions](/bigquery/docs/reference/analytics-hub/rest/v1/projects.locations.subscriptions)

| Methods | |
| --- | --- |
| `delete` | `DELETE /v1/{name=projects/*/locations/*/subscriptions/*}`   Deletes a subscription. |
| `get` | `GET /v1/{name=projects/*/locations/*/subscriptions/*}`   Gets the details of a Subscription. |
| `getIamPolicy` | `POST /v1/{resource=projects/*/locations/*/subscriptions/*}:getIamPolicy`   Gets the IAM policy. |
| `list` | `GET /v1/{parent=projects/*/locations/*}/subscriptions`   Lists all subscriptions in a given project and location. |
| `refresh` | `POST /v1/{name=projects/*/locations/*/subscriptions/*}:refresh`   Refreshes a Subscription to a Data Exchange. |
| `revoke` | `POST /v1/{name=projects/*/locations/*/subscriptions/*}:revoke`   Revokes a given subscription. |
| `setIamPolicy` | `POST /v1/{resource=projects/*/locations/*/subscriptions/*}:setIamPolicy`   Sets the IAM policy. |




Send feedback

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2025-11-12 UTC.




Need to tell us more?

[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Hard to understand","hardToUnderstand","thumb-down"],["Incorrect information or sample code","incorrectInformationOrSampleCode","thumb-down"],["Missing the information/samples I need","missingTheInformationSamplesINeed","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2025-11-12 UTC."],[],[]]