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
| `rpc ListTransferRuns(ListTransferRunsRequest) returns (ListTransferRunsResponse)`  Returns information about running and completed transfer runs.  Authorization scopes  Requires the following OAuth scope:   * `https://www.googleapis.com/auth/cloud-platform`   For more information, see the [Authentication Overview](/docs/authentication#authorization-gcp). |

| ScheduleTransferRuns |
| --- |
| This item is deprecated!  `rpc ScheduleTransferRuns(ScheduleTransferRunsRequest) returns (ScheduleTransferRunsResponse)`  Creates transfer runs for a time range [start\_time, end\_time]. For each date - or whatever granularity the data source supports - in the range, one transfer run is created. Note that runs are created per UTC time in the time range. DEPRECATED: use StartManualTransferRuns instead.  Authorization scopes  Requires the following OAuth scope:   * `https://www.googleapis.com/auth/cloud-platform`   For more information, see the [Authentication Overview](/docs/authentication#authorization-gcp). |

| StartManualTransferRuns |
| --- |
| `rpc StartManualTransferRuns(StartManualTransferRunsRequest) returns (StartManualTransferRunsResponse)`  Manually initiates transfer runs. You can schedule these runs in two ways:   1. For a specific point in time using the 'requested\_run\_time' parameter. 2. For a period between 'start\_time' (inclusive) and 'end\_time' (exclusive).   If scheduling a single run, it is set to execute immediately (schedule\_time equals the current time). When scheduling multiple runs within a time range, the first run starts now, and subsequent runs are delayed by 15 seconds each.  Authorization scopes  Requires the following OAuth scope:   * `https://www.googleapis.com/auth/cloud-platform`   For more information, see the [Authentication Overview](/docs/authentication#authorization-gcp). |

| UnenrollDataSources |
| --- |
| `rpc UnenrollDataSources(UnenrollDataSourcesRequest) returns (Empty)`  Unenroll data sources in a user project. This allows users to remove transfer configurations for these data sources. They will no longer appear in the ListDataSources RPC and will also no longer appear in the [BigQuery UI](https://console.cloud.google.com/bigquery). Data transfers configurations of unenrolled data sources will not be scheduled.  Authorization scopes  Requires the following OAuth scope:   * `https://www.googleapis.com/auth/cloud-platform`   For more information, see the [Authentication Overview](/docs/authentication#authorization-gcp). |

| UpdateTransferConfig |
| --- |
| `rpc UpdateTransferConfig(UpdateTransferConfigRequest) returns (TransferConfig)`  Updates a data transfer configuration. All fields must be set, even if they are not updated.  Authorization scopes  Requires the following OAuth scope:   * `https://www.googleapis.com/auth/cloud-platform`   For more information, see the [Authentication Overview](/docs/authentication#authorization-gcp). |

## CheckValidCredsRequest

A request to determine whether the user has valid credentials. This method is used to limit the number of OAuth popups in the user interface. The user id is inferred from the API call context. If the data source has the Google+ authorization type, this method returns false, as it cannot be determined whether the credentials are already valid merely based on the user id.

| Fields | |
| --- | --- |
| `name` | `string`  Required. The name of the data source. If you are using the regionless method, the location must be `US` and the name should be in the following form:   * `projects/{project_id}/dataSources/{data_source_id}`   If you are using the regionalized method, the name should be in the following form:   * `projects/{project_id}/locations/{location_id}/dataSources/{data_source_id}`   Authorization requires the following [IAM](https://cloud.google.com/iam/docs/) permission on the specified resource `name`:   * `bigquery.transfers.get` |

## CheckValidCredsResponse

A response indicating whether the credentials exist and are valid.

| Fields | |
| --- | --- |
| `has_valid_creds` | `bool`  If set to `true`, the credentials exist and are valid. |

## CreateTransferConfigRequest

A request to create a data transfer configuration. If new credentials are needed for this transfer configuration, authorization info must be provided. If authorization info is provided, the transfer configuration will be associated with the user id corresponding to the authorization info. Otherwise, the transfer configuration will be associated with the calling user.

When using a cross project service account for creating a transfer config, you must enable cross project service account usage. For more information, see [Disable attachment of service accounts to resources in other projects](https://cloud.google.com/resource-manager/docs/organization-policy/restricting-service-accounts#disable_cross_project_service_accounts).

| Fields | |
| --- | --- |
| `parent` | `string`  Required. The BigQuery project id where the transfer configuration should be created. Must be in the format projects/{project\_id}/locations/{location\_id} or projects/{project\_id}. If specified location and location of the destination bigquery dataset do not match - the request will fail.  Authorization requires the following [IAM](https://cloud.google.com/iam/docs/) permission on the specified resource `parent`:   * `bigquery.transfers.update` |
| `transfer_config` | `TransferConfig`  Required. Data transfer configuration to create. |
| `authorization_code (deprecated)` | `string`  This item is deprecated!  Deprecated: Authorization code was required when `transferConfig.dataSourceId` is 'youtube\_channel' but it is no longer used in any data sources. Use `version_info` instead.  Optional OAuth2 authorization code to use with this transfer configuration. This is required only if `transferConfig.dataSourceId` is 'youtube\_channel' and new credentials are needed, as indicated by `CheckValidCreds`. In order to obtain authorization\_code, make a request to the following URL:     ``` https://bigquery.cloud.google.com/datatransfer/oauthz/auth?redirect_uri=urn:ietf:wg:oauth:2.0:oob&response_type=authorization_code&client_id=client_id&scope=data_source_scopes ```  * The client\_id is the OAuth client\_id of the data source as returned by ListDataSources method. * data\_source\_scopes are the scopes returned by ListDataSources method.   Note that this should not be set when `service_account_name` is used to create the transfer config. |
| `version_info` | `string`  Optional version info. This parameter replaces `authorization_code` which is no longer used in any data sources. This is required only if `transferConfig.dataSourceId` is 'youtube\_channel' *or* new credentials are needed, as indicated by `CheckValidCreds`. In order to obtain version info, make a request to the following URL:     ``` https://bigquery.cloud.google.com/datatransfer/oauthz/auth?redirect_uri=urn:ietf:wg:oauth:2.0:oob&response_type=version_info&client_id=client_id&scope=data_source_scopes ```  * The client\_id is the OAuth client\_id of the data source as returned by ListDataSources method. * data\_source\_scopes are the scopes returned by ListDataSources method.   Note that this should not be set when `service_account_name` is used to create the transfer config. |
| `service_account_name` | `string`  Optional service account email. If this field is set, the transfer config will be created with this service account's credentials. It requires that the requesting user calling this API has permissions to act as this service account.  Note that not all data sources support service account credentials when creating a transfer config. For the latest list of data sources, read about [using service accounts](https://cloud.google.com/bigquery-transfer/docs/use-service-accounts). |

## DataSource

Defines the properties and custom parameters for a data source.

| Fields | |
| --- | --- |
| `name` | `string`  Output only. Data source resource name. |
| `data_source_id` | `string`  Data source id. |
| `display_name` | `string`  User friendly data source name. |
| `description` | `string`  User friendly data source description string. |
| `client_id` | `string`  Data source client id which should be used to receive refresh token. |
| `scopes[]` | `string`  Api auth scopes for which refresh token needs to be obtained. These are scopes needed by a data source to prepare data and ingest them into BigQuery, e.g., <https://www.googleapis.com/auth/bigquery> |
| `transfer_type (deprecated)` | `TransferType`  This item is deprecated!  Deprecated. This field has no effect. |
| `supports_multiple_transfers (deprecated)` | `bool`  This item is deprecated!  Deprecated. This field has no effect. |
| `update_deadline_seconds` | `int32`  The number of seconds to wait for an update from the data source before the Data Transfer Service marks the transfer as FAILED. |
| `default_schedule` | `string`  Default data transfer schedule. Examples of valid schedules include: `1st,3rd monday of month 15:30`, `every wed,fri of jan,jun 13:15`, and `first sunday of quarter 00:00`. |
| `supports_custom_schedule` | `bool`  Specifies whether the data source supports a user defined schedule, or operates on the default schedule. When set to `true`, user can override default schedule. |
| `parameters[]` | `DataSourceParameter`  Data source parameters. |
| `help_url` | `string`  Url for the help document for this data source. |
| `authorization_type` | `AuthorizationType`  Indicates the type of authorization. |
| `data_refresh_type` | `DataRefreshType`  Specifies whether the data source supports automatic data refresh for the past few days, and how it's supported. For some data sources, data might not be complete until a few days later, so it's useful to refresh data automatically. |
| `default_data_refresh_window_days` | `int32`  Default data refresh window on days. Only meaningful when `data_refresh_type` = `SLIDING_WINDOW`. |
| `manual_runs_disabled` | `bool`  Disables backfilling and manual run scheduling for the data source. |
| `minimum_schedule_interval` | `Duration` |