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
* `DialectDetectionConfig` (message)
* `DialectDetectionConfig.DetectionMode` (enum)
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
* `LineageOutput` (message)
* `LineageOutput.ProgressReport` (message)
* `LineageOutput.ProgressReport.ProcessingStage` (enum)
* `LineageOutput.ProgressReport.WorkSummary` (message)
* `LineageOutput.ProgressReport.WorkSummary.State` (enum)
* `LineageOutput.RecognizedInput` (message)
* `LineageOutput.RecognizedInput.Type` (enum)
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
* `TaskOutput` (message)
* `TaskOutput.State` (enum)
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
| `rpc StartMigrationWorkflow(StartMigrationWorkflowRequest) returns (Empty)`  Starts a previously created migration workflow. I.e., the state transitions from DRAFT to RUNNING. This is a no-op if the state is already RUNNING. An error will be signaled if the state is anything other than DRAFT or RUNNING.  Authorization scopes  Requires the following OAuth scope:   * `https://www.googleapis.com/auth/cloud-platform`   For more information, see the |