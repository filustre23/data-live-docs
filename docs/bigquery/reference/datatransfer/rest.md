* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback

# BigQuery Data Transfer API Stay organized with collections Save and categorize content based on your preferences.

Schedule queries or transfer external data from SaaS applications to Google BigQuery on a regular basis.

* [REST Resource: v1.projects](#v1.projects)
* [REST Resource: v1.projects.dataSources](#v1.projects.dataSources)
* [REST Resource: v1.projects.locations](#v1.projects.locations)
* [REST Resource: v1.projects.locations.dataSources](#v1.projects.locations.dataSources)
* [REST Resource: v1.projects.locations.transferConfigs](#v1.projects.locations.transferConfigs)
* [REST Resource: v1.projects.locations.transferConfigs.runs](#v1.projects.locations.transferConfigs.runs)
* [REST Resource: v1.projects.locations.transferConfigs.runs.transferLogs](#v1.projects.locations.transferConfigs.runs.transferLogs)
* [REST Resource: v1.projects.locations.transferConfigs.transferResources](#v1.projects.locations.transferConfigs.transferResources)
* [REST Resource: v1.projects.transferConfigs](#v1.projects.transferConfigs)
* [REST Resource: v1.projects.transferConfigs.runs](#v1.projects.transferConfigs.runs)
* [REST Resource: v1.projects.transferConfigs.runs.transferLogs](#v1.projects.transferConfigs.runs.transferLogs)
* [REST Resource: v1.projects.transferConfigs.transferResources](#v1.projects.transferConfigs.transferResources)

## Service: bigquerydatatransfer.googleapis.com

To call this service, we recommend that you use the Google-provided [client libraries](https://cloud.google.com/apis/docs/client-libraries-explained). If your application needs to use your own libraries to call this service, use the following information when you make the API requests.

### Discovery document

A [Discovery Document](https://developers.google.com/discovery/v1/reference/apis) is a machine-readable specification for describing and consuming REST APIs. It is used to build client libraries, IDE plugins, and other tools that interact with Google APIs. One service may provide multiple discovery documents. This service provides the following discovery document:

* <https://bigquerydatatransfer.googleapis.com/$discovery/rest?version=v1>

### Service endpoint

A [service endpoint](https://cloud.google.com/apis/design/glossary#api_service_endpoint) is a base URL that specifies the network address of an API service. One service might have multiple service endpoints. This service has the following service endpoint and all URIs below are relative to this service endpoint:

* `https://bigquerydatatransfer.googleapis.com`

### Regional service endpoint

A regional service endpoint is a base URL that specifies the network address of an API service in a single region. A service that is available in multiple regions might have multiple regional endpoints. Select a location to see its regional service endpoint for this service.

global asia-south1 asia-south2 europe-west1 europe-west2 europe-west3 europe-west4 europe-west6 europe-west8 europe-west9 me-central2 northamerica-northeast1 northamerica-northeast2 us-central1 us-central2 us-east1 us-east4 us-east5 us-east7 us-south1 us-west1 us-west2 us-west3 us-west4 us-west8

- `https://bigquerydatatransfer.googleapis.com`

## REST Resource: [v1.projects](/bigquery/docs/reference/datatransfer/rest/v1/projects)

| Methods | |
| --- | --- |
| `enrollDataSources` | `POST /v1/{name=projects/*}:enrollDataSources`   Enroll data sources in a user project. |

## REST Resource: [v1.projects.dataSources](/bigquery/docs/reference/datatransfer/rest/v1/projects.dataSources)

| Methods | |
| --- | --- |
| `checkValidCreds` | `POST /v1/{name=projects/*/dataSources/*}:checkValidCreds`   Returns true if valid credentials exist for the given data source and requesting user. |
| `get` | `GET /v1/{name=projects/*/dataSources/*}`   Retrieves a supported data source and returns its settings. |
| `list` | `GET /v1/{parent=projects/*}/dataSources`   Lists supported data sources and returns their settings. |

## REST Resource: [v1.projects.locations](/bigquery/docs/reference/datatransfer/rest/v1/projects.locations)

| Methods | |
| --- | --- |
| `enrollDataSources` | `POST /v1/{name=projects/*/locations/*}:enrollDataSources`   Enroll data sources in a user project. |
| `get` | `GET /v1/{name=projects/*/locations/*}`   Gets information about a location. |
| `list` | `GET /v1/{name=projects/*}/locations`   Lists information about the supported locations for this service. |
| `unenrollDataSources` | `POST /v1/{name=projects/*/locations/*}:unenrollDataSources`   Unenroll data sources in a user project. |

## REST Resource: [v1.projects.locations.dataSources](/bigquery/docs/reference/datatransfer/rest/v1/projects.locations.dataSources)

| Methods | |
| --- | --- |
| `checkValidCreds` | `POST /v1/{name=projects/*/locations/*/dataSources/*}:checkValidCreds`   Returns true if valid credentials exist for the given data source and requesting user. |
| `get` | `GET /v1/{name=projects/*/locations/*/dataSources/*}`   Retrieves a supported data source and returns its settings. |
| `list` | `GET /v1/{parent=projects/*/locations/*}/dataSources`   Lists supported data sources and returns their settings. |

## REST Resource: [v1.projects.locations.transferConfigs](/bigquery/docs/reference/datatransfer/rest/v1/projects.locations.transferConfigs)

| Methods | |
| --- | --- |
| `create` | `POST /v1/{parent=projects/*/locations/*}/transferConfigs`   Creates a new data transfer configuration. |
| `delete` | `DELETE /v1/{name=projects/*/locations/*/transferConfigs/*}`   Deletes a data transfer configuration, including any associated transfer runs and logs. |
| `get` | `GET /v1/{name=projects/*/locations/*/transferConfigs/*}`   Returns information about a data transfer config. |
| `list` | `GET /v1/{parent=projects/*/locations/*}/transferConfigs`   Returns information about all transfer configs owned by a project in the specified location. |
| `patch` | `PATCH /v1/{transferConfig.name=projects/*/locations/*/transferConfigs/*}`   Updates a data transfer configuration. |
| `scheduleRuns  (deprecated)` | `POST /v1/{parent=projects/*/locations/*/transferConfigs/*}:scheduleRuns`   Creates transfer runs for a time range [start\_time, end\_time]. |
| `startManualRuns` | `POST /v1/{parent=projects/*/locations/*/transferConfigs/*}:startManualRuns`   Manually initiates transfer runs. |

## REST Resource: [v1.projects.locations.transferConfigs.runs](/bigquery/docs/reference/datatransfer/rest/v1/projects.locations.transferConfigs.runs)

| Methods | |
| --- | --- |
| `delete` | `DELETE /v1/{name=projects/*/locations/*/transferConfigs/*/runs/*}`   Deletes the specified transfer run. |
| `get` | `GET /v1/{name=projects/*/locations/*/transferConfigs/*/runs/*}`   Returns information about the particular transfer run. |
| `list` | `GET /v1/{parent=projects/*/locations/*/transferConfigs/*}/runs`   Returns information about running and completed transfer runs. |

## REST Resource: [v1.projects.locations.transferConfigs.runs.transferLogs](/bigquery/docs/reference/datatransfer/rest/v1/projects.locations.transferConfigs.runs.transferLogs)

| Methods | |
| --- | --- |
| `list` | `GET /v1/{parent=projects/*/locations/*/transferConfigs/*/runs/*}/transferLogs`   Returns log messages for the transfer run. |

## REST Resource: [v1.projects.locations.transferConfigs.transferResources](/bigquery/docs/reference/datatransfer/rest/v1/projects.locations.transferConfigs.transferResources)

| Methods | |
| --- | --- |
| `get` | `GET /v1/{name=projects/*/locations/*/transferConfigs/*/transferResources/*}`   Returns a transfer resource. |
| `list` | `GET /v1/{parent=projects/*/locations/*/transferConfigs/*}/transferResources`   Returns information about transfer resources. |

## REST Resource: [v1.projects.transferConfigs](/bigquery/docs/reference/datatransfer/rest/v1/projects.transferConfigs)

| Methods | |
| --- | --- |
| `create` | `POST /v1/{parent=projects/*}/transferConfigs`   Creates a new data transfer configuration. |
| `delete` | `DELETE /v1/{name=projects/*/transferConfigs/*}`   Deletes a data transfer configuration, including any associated transfer runs and logs. |
| `get` | `GET /v1/{name=projects/*/transferConfigs/*}`   Returns information about a data transfer config. |
| `list` | `GET /v1/{parent=projects/*}/transferConfigs`   Returns information about all transfer configs owned by a project in the specified location. |
| `patch` | `PATCH /v1/{transferConfig.name=projects/*/transferConfigs/*}`   Updates a data transfer configuration. |
| `scheduleRuns  (deprecated)` | `POST /v1/{parent=projects/*/transferConfigs/*}:scheduleRuns`   Creates transfer runs for a time range [start\_time, end\_time]. |
| `startManualRuns` | `POST /v1/{parent=projects/*/transferConfigs/*}:startManualRuns`   Manually initiates transfer runs. |

## REST Resource: [v1.projects.transferConfigs.runs](/bigquery/docs/reference/datatransfer/rest/v1/projects.transferConfigs.runs)

| Methods | |
| --- | --- |
| `delete` | `DELETE /v1/{name=projects/*/transferConfigs/*/runs/*}`   Deletes the specified transfer run. |
| `get` | `GET /v1/{name=projects/*/transferConfigs/*/runs/*}`   Returns information about the particular transfer run. |
| `list` | `GET /v1/{parent=projects/*/transferConfigs/*}/runs`   Returns information about running and completed transfer runs. |

## REST Resource: [v1.projects.transferConfigs.runs.transferLogs](/bigquery/docs/reference/datatransfer/rest/v1/projects.transferConfigs.runs.transferLogs)

| Methods | |
| --- | --- |
| `list` | `GET /v1/{parent=projects/*/transferConfigs/*/runs/*}/transferLogs`   Returns log messages for the transfer run. |

## REST Resource: [v1.projects.transferConfigs.transferResources](/bigquery/docs/reference/datatransfer/rest/v1/projects.transferConfigs.transferResources)

| Methods | |
| --- | --- |
| `get` | `GET /v1/{name=projects/*/transferConfigs/*/transferResources/*}`   Returns a transfer resource. |
| `list` | `GET /v1/{parent=projects/*/transferConfigs/*}/transferResources`   Returns information about transfer resources. |




Send feedback

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2026-05-12 UTC.




Need to tell us more?

[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Hard to understand","hardToUnderstand","thumb-down"],["Incorrect information or sample code","incorrectInformationOrSampleCode","thumb-down"],["Missing the information/samples I need","missingTheInformationSamplesINeed","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2026-05-12 UTC."],[],[]]