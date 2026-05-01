* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback

# Package google.cloud.bigquery.migration.v2alpha Stay organized with collections Save and categorize content based on your preferences.

## Index

* `MigrationService` (interface)
* `AssessmentFeatureHandle` (message)
* `AssessmentOrchestrationResultDetails` (message)
* `AssessmentTaskDetails` (message)
* `AzureSynapseDialect` (message)
* `BigQueryDialect` (message)
* `BteqOptions` (message)
* `CreateMigrationWorkflowRequest` (message)
* `DB2Dialect` (message)
* `DatasetReference` (message)
* `DeleteMigrationWorkflowRequest` (message)
* `Dialect` (message)
* `ErrorDetail` (message)
* `ErrorLocation` (message)
* `Filter` (message)
* `GcsReportLogMessage` (message)
* `GetMigrationSubtaskRequest` (message)
* `GetMigrationWorkflowRequest` (message)
* `GreenplumDialect` (message)
* `HiveQLDialect` (message)
* `IdentifierSettings` (message)
* `IdentifierSettings.IdentifierCase` (enum)
* `IdentifierSettings.IdentifierRewriteMode` (enum)
* `ListMigrationSubtasksRequest` (message)
* `ListMigrationSubtasksResponse` (message)
* `ListMigrationWorkflowsRequest` (message)
* `ListMigrationWorkflowsResponse` (message)
* `Literal` (message)
* `MetadataCaching` (message)
* `MigrationSubtask` (message)
* `MigrationSubtask.State` (enum)
* `MigrationTask` (message)
* `MigrationTask.State` (enum)
* `MigrationTaskOrchestrationResult` (message)
* `MigrationTaskResult` (message)
* `MigrationWorkflow` (message)
* `MigrationWorkflow.State` (enum)
* `MySQLDialect` (message)
* `NameMappingKey` (message)
* `NameMappingKey.Type` (enum)
* `NameMappingValue` (message)
* `NetezzaDialect` (message)
* `ObjectNameMapping` (message)
* `ObjectNameMappingList` (message)
* `OracleDialect` (message)
* `Point` (message)
* `PostgresqlDialect` (message)
* `PrestoDialect` (message)
* `RedshiftDialect` (message)
* `ResourceErrorDetail` (message)
* `SQLServerDialect` (message)
* `SQLiteDialect` (message)
* `SnowflakeDialect` (message)
* `SourceEnv` (message)
* `SourceEnvironment` (message)
* `SourceLocation` (message)
* `SourceSpec` (message)
* `SourceTargetLocationMapping` (message)
* `SourceTargetMapping` (message)
* `SparkSQLDialect` (message)
* `StartMigrationWorkflowRequest` (message)
* `SuggestionConfig` (message)
* `SuggestionStep` (message)
* `SuggestionStep.RewriteTarget` (enum)
* `SuggestionStep.SuggestionType` (enum)
* `TargetLocation` (message)
* `TargetSpec` (message)
* `TeradataDialect` (message)
* `TeradataDialect.Mode` (enum)
* `TeradataOptions` (message)
* `TimeInterval` (message)
* `TimeSeries` (message)
* `TranslationConfigDetails` (message)
* `TranslationDetails` (message)
* `TranslationFileMapping` (message)
* `TranslationTaskDetails` (message)
* `TranslationTaskDetails.FileEncoding` (enum)
* `TranslationTaskDetails.TokenType` (enum)
* `TranslationTaskResult` (message)
* `TypedValue` (message)
* `VerticaDialect` (message)

## MigrationService

Service to handle EDW migrations.

| CreateMigrationWorkflow |
| --- |
| `rpc CreateMigrationWorkflow(CreateMigrationWorkflowRequest) returns (MigrationWorkflow)`  Creates a migration workflow.  Authorization scopes  Requires one of the following OAuth scopes:   * `https://www.googleapis.com/auth/bigquerymigration` * `https://www.googleapis.com/auth/devstorage.read_only` * `https://www.googleapis.com/auth/cloud-platform`   For more information, see the [Authentication Overview](/docs/authentication#authorization-gcp).  IAM Permissions  Requires the following [IAM](https://cloud.google.com/iam/docs) permission on the `parent` resource:   * `bigquerymigration.workflows.create`   For more information, see the [IAM documentation](https://cloud.google.com/iam/docs). |

| DeleteMigrationWorkflow |
| --- |
| `rpc DeleteMigrationWorkflow(DeleteMigrationWorkflowRequest) returns (Empty)`  Deletes a migration workflow by name.  Authorization scopes  Requires the following OAuth scope:   * `https://www.googleapis.com/auth/cloud-platform`   For more information, see the [Authentication Overview](/docs/authentication#authorization-gcp).  IAM Permissions  Requires the following [IAM](https://cloud.google.com/iam/docs) permission on the `name` resource:   * `bigquerymigration.workflows.delete`   For more information, see the [IAM documentation](https://cloud.google.com/iam/docs). |

| GetMigrationSubtask |
| --- |
| `rpc GetMigrationSubtask(GetMigrationSubtaskRequest) returns (MigrationSubtask)`  Gets a previously created migration subtask.  Authorization scopes  Requires the following OAuth scope:   * `https://www.googleapis.com/auth/cloud-platform`   For more information, see the [Authentication Overview](/docs/authentication#authorization-gcp).  IAM Permissions  Requires the following [IAM](https://cloud.google.com/iam/docs) permission on the `name` resource:   * `bigquerymigration.subtasks.get`   For more information, see the [IAM documentation](https://cloud.google.com/iam/docs). |

| GetMigrationWorkflow |
| --- |
| `rpc GetMigrationWorkflow(GetMigrationWorkflowRequest) returns (MigrationWorkflow)`  Gets a previously created migration workflow.  Authorization scopes  Requires one of the following OAuth scopes:   * `https://www.googleapis.com/auth/bigquerymigration` * `https://www.googleapis.com/auth/bigquerymigration.readonly` * `https://www.googleapis.com/auth/cloud-platform`   For more information, see the [Authentication Overview](/docs/authentication#authorization-gcp).  IAM Permissions  Requires the following [IAM](https://cloud.google.com/iam/docs) permission on the `name` resource:   * `bigquerymigration.workflows.get`   For more information, see the [IAM documentation](https://cloud.google.com/iam/docs). |

| ListMigrationSubtasks |
| --- |
| `rpc ListMigrationSubtasks(ListMigrationSubtasksRequest) returns (ListMigrationSubtasksResponse)`  Lists previously created migration subtasks.  Authorization scopes  Requires the following OAuth scope:   * `https://www.googleapis.com/auth/cloud-platform`   For more information, see the [Authentication Overview](/docs/authentication#authorization-gcp).  IAM Permissions  Requires the following [IAM](https://cloud.google.com/iam/docs) permission on the `parent` resource:   * `bigquerymigration.subtasks.list`   For more information, see the [IAM documentation](https://cloud.google.com/iam/docs). |

| ListMigrationWorkflows |
| --- |
| `rpc ListMigrationWorkflows(ListMigrationWorkflowsRequest) returns (ListMigrationWorkflowsResponse)`  Lists previously created migration workflow.  Authorization scopes  Requires the following OAuth scope:   * `https://www.googleapis.com/auth/cloud-platform`   For more information, see the [Authentication Overview](/docs/authentication#authorization-gcp).  IAM Permissions  Requires the following [IAM](https://cloud.google.com/iam/docs) permission on the `parent` resource:   * `bigquerymigration.workflows.list`   For more information, see the [IAM documentation](https://cloud.google.com/iam/docs). |

| StartMigrationWorkflow |
| --- |
| `rpc StartMigrationWorkflow(StartMigrationWorkflowRequest) returns (Empty)`  Starts a previously created migration workflow. I.e., the state transitions from DRAFT to RUNNING. This is a no-op if the state is already RUNNING. An error will be signaled if the state is anything other than DRAFT or RUNNING.  Authorization scopes  Requires the following OAuth scope:   * `https://www.googleapis.com/auth/cloud-platform`   For more information, see the [Authentication Overview](/docs/authentication#authorization-gcp).  IAM Permissions  Requires the following [IAM](https://cloud.google.com/iam/docs) permission on the `name` resource:   * `bigquerymigration.workflows.update`   For more information, see the [IAM documentation](https://cloud.google.com/iam/docs). |

## AssessmentFeatureHandle

User-definable feature flags for assessment tasks.

| Fields | |
| --- | --- |
| `add_shareable_dataset` | `bool`  Optional. Whether to create a dataset containing non-PII data in addition to the output dataset. |

## AssessmentOrchestrationResultDetails

Details for an assessment task orchestration result.

| Fields | |
| --- | --- |
| `output_tables_schema_version` | `string`  Optional. The version used for the output table schemas. |
| `report_uri` | `string`  Optional. The URI of the Data Studio report. |
| `additional_report_uris` | `map<string, string>`  Optional. Mapping with additional report URIs. This gives a mapping of report names to their URIs. The possible values for the keys are documented in the user guide. |

## AssessmentTaskDetails

Assessment task config.

| Fields | |
| --- | --- |
| `input_path` | `string`  Required. The Cloud Storage path for assessment input files. |
| `output_dataset` | `string`  Required. The BigQuery dataset for output. |
| `querylogs_path` | `string`  Optional. An optional Cloud Storage path to write the query logs (which is then used as an input path on the translation task) |
| `data_source` | `string`  Required. The data source or data warehouse type (eg: TERADATA/REDSHIFT) from which the input data is extracted. |
| `feature_handle` | `AssessmentFeatureHandle`  Optional. A collection of additional feature flags for this assessment. |

## AzureSynapseDialect

This type has no fields.

The dialect definition for Azure Synapse.

## BigQueryDialect

This type has no fields.

The dialect definition for BigQuery.

## BteqOptions

BTEQ translation task related settings.

| Fields | |
| --- | --- |
| `project_dataset` | `DatasetReference`  Specifies the project and dataset in BigQuery that will be used for external table creation during the translation. |
| `default_path_uri` | `string`  The Cloud Storage location to be used as the default path for files that are not otherwise specified in the file replacement map. |
| `file_replacement_map` | `map<string, string>`  Maps the local paths that are used in BTEQ scripts (the keys) to the paths in Cloud Storage that should be used in their stead in the translation (the value). |

## CreateMigrationWorkflowRequest

Request to create a migration workflow resource.

| Fields | |
| --- | --- |
| `parent` | `string`  Required. The name of the project to which this migration workflow belongs. Example: `projects/foo/locations/bar` |
| `migration_workflow` | `MigrationWorkflow`  Required. The migration workflow to create. |

## DB2Dialect

This type has no fields.

The dialect definition for DB2.

## DatasetReference

Reference to a BigQuery dataset.

| Fields | |
| --- | --- |
| `dataset_id` | `string`  A unique ID for this dataset, without the project name. The ID must contain only letters (a-z, A-Z), numbers (0-9), or underscores (\_). The maximum length is 1,024 characters. |
| `project_id` | `string`  The ID of the project containing this dataset. |
| `dataset_id_alternative[]` | `string`  The alternative field that will be used when the service is not able to translate the received data to the dataset\_id field. |
| `project_id_alternative[]` | `string`  The alternative field that will be used when the service is not able to translate the received data to the project\_id field. |

## DeleteMigrationWorkflowRequest

A request to delete a previously created migration workflow.

| Fields | |
| --- | --- |
| `name` | `string`  Required. The unique identifier for the migration workflow. Example: `projects/123/locations/us/workflows/1234` |

## Dialect

The possible dialect options for translation.

| Fields | |
| --- | --- |
| Union field `dialect_value`. The possible dialect options that this message represents. `dialect_value` can be only one of the following: | |
| `bigquery_dialect` | `BigQueryDialect`  The BigQuery dialect |
| `hiveql_dialect` | `HiveQLDialect`  The HiveQL dialect |
| `redshift_dialect` | `RedshiftDialect`  The Redshift dialect |
| `teradata_dialect` | `TeradataDialect`  The Teradata dialect |
| `oracle_dialect` | `OracleDialect`  The Oracle dialect |
| `sparksql_dialect` | `SparkSQLDialect`  The SparkSQL dialect |
| `snowflake_dialect` | `SnowflakeDialect`  The Snowflake dialect |
| `netezza_dialect` | `NetezzaDialect`  The Netezza dialect |
| `azure_synapse_dialect` | `AzureSynapseDialect`  The Azure Synapse dialect |
| `vertica_dialect` | `VerticaDialect`  The Vertica dialect |
| `sql_server_dialect` | `SQLServerDialect`  The SQL Server dialect |
| `postgresql_dialect` | `PostgresqlDialect`  The Postgresql dialect |
| `presto_dialect` | `PrestoDialect`  The Presto dialect |
| `mysql_dialect` | `MySQLDialect`  The MySQL dialect |
| `db2_dialect` | `DB2Dialect`  DB2 dialect |
| `sqlite_dialect` | `SQLiteDialect`  SQLite dialect |
| `greenplum_dialect` | `GreenplumDialect`  Greenplum dialect |

## ErrorDetail

Provides details for errors, e.g. issues that where encountered when processing a subtask.

| Fields | |
| --- | --- |
| `location` | `ErrorLocation`  Optional. The exact location within the resource (if applicable). |
| `error_info` | `ErrorInfo`  Required. Describes the cause of the error with structured detail. |

## ErrorLocation

Holds information about where the error is located.