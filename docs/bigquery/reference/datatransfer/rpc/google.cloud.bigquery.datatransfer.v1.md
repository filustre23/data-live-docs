* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback

# Package google.cloud.bigquery.datatransfer.v1 Stay organized with collections Save and categorize content based on your preferences.

## Index

* `DataTransferService` (interface)
* `CheckValidCredsRequest` (message)
* `CheckValidCredsResponse` (message)
* `CreateTransferConfigRequest` (message)
* `DataSource` (message)
* `DataSource.AuthorizationType` (enum)
* `DataSource.DataRefreshType` (enum)
* `DataSourceParameter` (message)
* `DataSourceParameter.Type` (enum)
* `DataplexConfiguration` (message)
* `DeleteTransferConfigRequest` (message)
* `DeleteTransferRunRequest` (message)
* `EmailPreferences` (message)
* `EncryptionConfiguration` (message)
* `EnrollDataSourcesRequest` (message)
* `EventDrivenSchedule` (message)
* `GetDataSourceRequest` (message)
* `GetTransferConfigRequest` (message)
* `GetTransferResourceRequest` (message)
* `GetTransferRunRequest` (message)
* `HierarchyDetail` (message)
* `ListDataSourcesRequest` (message)
* `ListDataSourcesResponse` (message)
* `ListTransferConfigsRequest` (message)
* `ListTransferConfigsResponse` (message)
* `ListTransferLogsRequest` (message)
* `ListTransferLogsResponse` (message)
* `ListTransferResourcesRequest` (message)
* `ListTransferResourcesResponse` (message)
* `ListTransferRunsRequest` (message)
* `ListTransferRunsRequest.RunAttempt` (enum)
* `ListTransferRunsResponse` (message)
* `ManagedTableType` (enum)
* `ManualSchedule` (message)
* `MetadataDestination` (message)
* `PartitionDetail` (message)
* `ResourceDestination` (enum)
* `ResourceTransferState` (enum)
* `ResourceType` (enum)
* `ScheduleOptions` (message)
* `ScheduleOptionsV2` (message)
* `ScheduleTransferRunsRequest` (message)
* `ScheduleTransferRunsResponse` (message)
* `StartManualTransferRunsRequest` (message)
* `StartManualTransferRunsRequest.TimeRange` (message)
* `StartManualTransferRunsResponse` (message)
* `TableDetail` (message)
* `TimeBasedSchedule` (message)
* `TransferConfig` (message)
* `TransferConfig.ParameterConfig` (message)
* `TransferMessage` (message)
* `TransferMessage.MessageSeverity` (enum)
* `TransferResource` (message)
* `TransferResourceStatusDetail` (message)
* `TransferRun` (message)
* `TransferRunBrief` (message)
* `TransferState` (enum)
* `TransferStatusMetric` (message)
* `TransferStatusSummary` (message)
* `TransferStatusUnit` (enum)
* `TransferType` (enum) **(deprecated)**
* `UnenrollDataSourcesRequest` (message)
* `UpdateTransferConfigRequest` (message)
* `UserInfo` (message)

## DataTransferService

This API allows users to manage their data transfers into BigQuery.

| CheckValidCreds |
| --- |
| `rpc CheckValidCreds(CheckValidCredsRequest) returns (CheckValidCredsResponse)`  Returns true if valid credentials exist for the given data source and requesting user.  Authorization scopes  Requires the following OAuth scope:   * `https://www.googleapis.com/auth/cloud-platform`   For more information, see the [Authentication Overview](/docs/authentication#authorization-gcp). |

| CreateTransferConfig |
| --- |
| `rpc CreateTransferConfig(CreateTransferConfigRequest) returns (TransferConfig)`  Creates a new data transfer configuration.  Authorization scopes  Requires the following OAuth scope:   * `https://www.googleapis.com/auth/cloud-platform`   For more information, see the [Authentication Overview](/docs/authentication#authorization-gcp). |

| DeleteTransferConfig |
| --- |
| `rpc DeleteTransferConfig(DeleteTransferConfigRequest) returns (Empty)`  Deletes a data transfer configuration, including any associated transfer runs and logs.  Authorization scopes  Requires the following OAuth scope:   * `https://www.googleapis.com/auth/cloud-platform`   For more information, see the [Authentication Overview](/docs/authentication#authorization-gcp). |

| DeleteTransferRun |
| --- |
| `rpc DeleteTransferRun(DeleteTransferRunRequest) returns (Empty)`  Deletes the specified transfer run.  Authorization scopes  Requires the following OAuth scope:   * `https://www.googleapis.com/auth/cloud-platform`   For more information, see the [Authentication Overview](/docs/authentication#authorization-gcp). |

| EnrollDataSources |
| --- |
| `rpc EnrollDataSources(EnrollDataSourcesRequest) returns (Empty)`  Enroll data sources in a user project. This allows users to create transfer configurations for these data sources. They will also appear in the ListDataSources RPC and as such, will appear in the [BigQuery UI](https://console.cloud.google.com/bigquery), and the documents can be found in the public guide for [BigQuery Web UI](https://cloud.google.com/bigquery/bigquery-web-ui) and [Data Transfer Service](https://cloud.google.com/bigquery/docs/working-with-transfers).  Authorization scopes  Requires the following OAuth scope:   * `https://www.googleapis.com/auth/cloud-platform`   For more information, see the [Authentication Overview](/docs/authentication#authorization-gcp). |

| GetDataSource |
| --- |
| `rpc GetDataSource(GetDataSourceRequest) returns (DataSource)`  Retrieves a supported data source and returns its settings.  Authorization scopes  Requires the following OAuth scope:   * `https://www.googleapis.com/auth/cloud-platform`   For more information, see the [Authentication Overview](/docs/authentication#authorization-gcp). |

| GetTransferConfig |
| --- |
| `rpc GetTransferConfig(GetTransferConfigRequest) returns (TransferConfig)`  Returns information about a data transfer config.  Authorization scopes  Requires the following OAuth scope:   * `https://www.googleapis.com/auth/cloud-platform`   For more information, see the [Authentication Overview](/docs/authentication#authorization-gcp). |

| GetTransferResource |
| --- |
| `rpc GetTransferResource(GetTransferResourceRequest) returns (TransferResource)`  Returns a transfer resource.  Authorization scopes  Requires the following OAuth scope:   * `https://www.googleapis.com/auth/cloud-platform`   For more information, see the [Authentication Overview](/docs/authentication#authorization-gcp). |

| GetTransferRun |
| --- |
| `rpc GetTransferRun(GetTransferRunRequest) returns (TransferRun)`  Returns information about the particular transfer run.  Authorization scopes  Requires the following OAuth scope:   * `https://www.googleapis.com/auth/cloud-platform`   For more information, see the [Authentication Overview](/docs/authentication#authorization-gcp). |

| ListDataSources |
| --- |
| `rpc ListDataSources(ListDataSourcesRequest) returns (ListDataSourcesResponse)`  Lists supported data sources and returns their settings.  Authorization scopes  Requires the following OAuth scope:   * `https://www.googleapis.com/auth/cloud-platform`   For more information, see the [Authentication Overview](/docs/authentication#authorization-gcp). |

| ListTransferConfigs |
| --- |
| `rpc ListTransferConfigs(ListTransferConfigsRequest) returns (ListTransferConfigsResponse)`  Returns information about all transfer configs owned by a project in the specified location.  Authorization scopes  Requires the following OAuth scope:   * `https://www.googleapis.com/auth/cloud-platform`   For more information, see the [Authentication Overview](/docs/authentication#authorization-gcp). |

| ListTransferLogs |
| --- |
| `rpc ListTransferLogs(ListTransferLogsRequest) returns (ListTransferLogsResponse)`  Returns log messages for the transfer run.  Authorization scopes  Requires the following OAuth scope:   * `https://www.googleapis.com/auth/cloud-platform`   For more information, see the [Authentication Overview](/docs/authentication#authorization-gcp). |

| ListTransferResources |
| --- |
| `rpc ListTransferResources(ListTransferResourcesRequest) returns (ListTransferResourcesResponse)`  Returns information about transfer resources.  Authorization scopes  Requires the following OAuth scope:   * `https://www.googleapis.com/auth/cloud-platform`   For more information, see the [Authentication Overview](/docs/authentication#authorization-gcp). |

| ListTransferRuns |
| --- |
| `rpc ListTransferRuns(ListTransferRunsRequest) returns (ListTransferRunsResponse)`  Returns information about running and completed |