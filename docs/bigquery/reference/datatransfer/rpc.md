* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback

# BigQuery Data Transfer API Stay organized with collections Save and categorize content based on your preferences.

Schedule queries or transfer external data from SaaS applications to Google BigQuery on a regular basis.

## Service: bigquerydatatransfer.googleapis.com

The Service name `bigquerydatatransfer.googleapis.com` is needed to create RPC client stubs.

## `google.cloud.bigquery.datatransfer.v1.DataTransferService`

| Methods | |
| --- | --- |
| `CheckValidCreds` | Returns true if valid credentials exist for the given data source and requesting user. |
| `CreateTransferConfig` | Creates a new data transfer configuration. |
| `DeleteTransferConfig` | Deletes a data transfer configuration, including any associated transfer runs and logs. |
| `DeleteTransferRun` | Deletes the specified transfer run. |
| `EnrollDataSources` | Enroll data sources in a user project. |
| `GetDataSource` | Retrieves a supported data source and returns its settings. |
| `GetTransferConfig` | Returns information about a data transfer config. |
| `GetTransferResource` | Returns a transfer resource. |
| `GetTransferRun` | Returns information about the particular transfer run. |
| `ListDataSources` | Lists supported data sources and returns their settings. |
| `ListTransferConfigs` | Returns information about all transfer configs owned by a project in the specified location. |
| `ListTransferLogs` | Returns log messages for the transfer run. |
| `ListTransferResources` | Returns information about transfer resources. |
| `ListTransferRuns` | Returns information about running and completed transfer runs. |
| `ScheduleTransferRuns  (deprecated)` | Creates transfer runs for a time range [start\_time, end\_time]. |
| `StartManualTransferRuns` | Manually initiates transfer runs. |
| `UnenrollDataSources` | Unenroll data sources in a user project. |
| `UpdateTransferConfig` | Updates a data transfer configuration. |

## `google.cloud.location.Locations`

| Methods | |
| --- | --- |
| `GetLocation` | Gets information about a location. |
| `ListLocations` | Lists information about the supported locations for this service. |




Send feedback

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2026-03-25 UTC.




Need to tell us more?

[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Hard to understand","hardToUnderstand","thumb-down"],["Incorrect information or sample code","incorrectInformationOrSampleCode","thumb-down"],["Missing the information/samples I need","missingTheInformationSamplesINeed","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2026-03-25 UTC."],[],[]]