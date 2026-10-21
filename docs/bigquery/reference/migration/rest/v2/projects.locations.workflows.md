* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback

# REST Resource: projects.locations.workflows Stay organized with collections Save and categorize content based on your preferences.

* [Resource: MigrationWorkflow](#MigrationWorkflow)
  + [JSON representation](#MigrationWorkflow.SCHEMA_REPRESENTATION)
* [MigrationTask](#MigrationTask)
  + [JSON representation](#MigrationTask.SCHEMA_REPRESENTATION)
* [AssessmentTaskDetails](#AssessmentTaskDetails)
  + [JSON representation](#AssessmentTaskDetails.SCHEMA_REPRESENTATION)
* [AssessmentFeatureHandle](#AssessmentFeatureHandle)
  + [JSON representation](#AssessmentFeatureHandle.SCHEMA_REPRESENTATION)
* [TranslationConfigDetails](#TranslationConfigDetails)
  + [JSON representation](#TranslationConfigDetails.SCHEMA_REPRESENTATION)
* [ObjectNameMappingList](#ObjectNameMappingList)
  + [JSON representation](#ObjectNameMappingList.SCHEMA_REPRESENTATION)
* [ObjectNameMapping](#ObjectNameMapping)
  + [JSON representation](#ObjectNameMapping.SCHEMA_REPRESENTATION)
* [NameMappingKey](#NameMappingKey)
  + [JSON representation](#NameMappingKey.SCHEMA_REPRESENTATION)
* [Type](#Type)
* [NameMappingValue](#NameMappingValue)
  + [JSON representation](#NameMappingValue.SCHEMA_REPRESENTATION)
* [Dialect](#Dialect)
  + [JSON representation](#Dialect.SCHEMA_REPRESENTATION)
* [BigQueryDialect](#BigQueryDialect)
* [HiveQLDialect](#HiveQLDialect)
* [RedshiftDialect](#RedshiftDialect)
* [TeradataDialect](#TeradataDialect)
  + [JSON representation](#TeradataDialect.SCHEMA_REPRESENTATION)
* [Mode](#Mode)
* [OracleDialect](#OracleDialect)
* [SparkSQLDialect](#SparkSQLDialect)
* [SnowflakeDialect](#SnowflakeDialect)
* [NetezzaDialect](#NetezzaDialect)
* [AzureSynapseDialect](#AzureSynapseDialect)
* [VerticaDialect](#VerticaDialect)
* [SQLServerDialect](#SQLServerDialect)
* [PostgresqlDialect](#PostgresqlDialect)
* [PrestoDialect](#PrestoDialect)
* [MySQLDialect](#MySQLDialect)
* [DB2Dialect](#DB2Dialect)
* [SQLiteDialect](#SQLiteDialect)
* [GreenplumDialect](#GreenplumDialect)
* [SourceEnv](#SourceEnv)
  + [JSON representation](#SourceEnv.SCHEMA_REPRESENTATION)
* [TranslationDetails](#TranslationDetails)
  + [JSON representation](#TranslationDetails.SCHEMA_REPRESENTATION)
* [SourceTargetMapping](#SourceTargetMapping)
  + [JSON representation](#SourceTargetMapping.SCHEMA_REPRESENTATION)
* [SourceSpec](#SourceSpec)
  + [JSON representation](#SourceSpec.SCHEMA_REPRESENTATION)
* [Literal](#Literal)
  + [JSON representation](#Literal.SCHEMA_REPRESENTATION)
* [TargetSpec](#TargetSpec)
  + [JSON representation](#TargetSpec.SCHEMA_REPRESENTATION)
* [SourceEnvironment](#SourceEnvironment)
  + [JSON representation](#SourceEnvironment.SCHEMA_REPRESENTATION)
* [SuggestionConfig](#SuggestionConfig)
  + [JSON representation](#SuggestionConfig.SCHEMA_REPRESENTATION)
* [SuggestionStep](#SuggestionStep)
  + [JSON representation](#SuggestionStep.SCHEMA_REPRESENTATION)
* [SuggestionType](#SuggestionType)
* [RewriteTarget](#RewriteTarget)
* [State](#State)
* [MigrationTaskResult](#MigrationTaskResult)
  + [JSON representation](#MigrationTaskResult.SCHEMA_REPRESENTATION)
* [TranslationTaskResult](#TranslationTaskResult)
  + [JSON representation](#TranslationTaskResult.SCHEMA_REPRESENTATION)
* [GcsReportLogMessage](#GcsReportLogMessage)
  + [JSON representation](#GcsReportLogMessage.SCHEMA_REPRESENTATION)
* [TaskOutput](#TaskOutput)
  + [JSON representation](#TaskOutput.SCHEMA_REPRESENTATION)
* [LineageOutput](#LineageOutput)
  + [JSON representation](#LineageOutput.SCHEMA_REPRESENTATION)
* [RecognizedInput](#RecognizedInput)
  + [JSON representation](#RecognizedInput.SCHEMA_REPRESENTATION)
* [Type](#Type_1)
* [ProgressReport](#ProgressReport)
  + [JSON representation](#ProgressReport.SCHEMA_REPRESENTATION)
* [ProcessingStage](#ProcessingStage)
* [WorkSummary](#WorkSummary)
  + [JSON representation](#WorkSummary.SCHEMA_REPRESENTATION)
* [State](#State_1)
* [State](#State_2)
* [State](#State_3)
* [Methods](#METHODS_SUMMARY)

## Resource: MigrationWorkflow

A migration workflow which specifies what needs to be done for an EDW migration.

| JSON representation |
| --- |
| ``` {   "name": string,   "displayName": string,   "tasks": {     string: {       object (MigrationTask)     },     ...   },   "state": enum (State),   "createTime": string,   "lastUpdateTime": string } ``` |

| Fields | |
| --- | --- |
| `name` | `string`  Output only. Immutable. Identifier. The unique identifier for the migration workflow. The ID is server-generated.  Example: `projects/123/locations/us/workflows/345` |
| `displayName` | `string`  The display name of the workflow. This can be set to give a workflow a descriptive name. There is no guarantee or enforcement of uniqueness. |
| `tasks` | `map (key: string, value: object (MigrationTask))`  The tasks in a workflow in a named map. The name (i.e. key) has no meaning and is merely a convenient way to address a specific task in a workflow. |
| `state` | `enum (State)`  Output only. That status of the workflow. |
| `createTime` | `string (Timestamp format)`  Output only. Time when the workflow was created. |
| `lastUpdateTime` | `string (Timestamp format)`  Output only. Time when the workflow was last updated. |

## MigrationTask

A single task for a migration which has details about the configuration of the task.

| JSON representation |
| --- |
| ``` {   "id": string,   "type": string,   "state": enum (State),   "processingError": {     object (ErrorInfo)   },   "createTime": string,   "lastUpdateTime": string,   "resourceErrorDetails": [     {       object (ResourceErrorDetail)     }   ],   "resourceErrorCount": integer,   "metrics": [     {       object (TimeSeries)     }   ],   "taskResult": {     object (MigrationTaskResult)   },   "totalProcessingErrorCount": integer,   "totalResourceErrorCount": integer,    // The following is a list of mutually exclusive fields. At most one of the   // fields will be set in a response:   "assessmentTaskDetails": {     object (AssessmentTaskDetails)   },   "translationConfigDetails": {     object (TranslationConfigDetails)   },   "translationDetails": {     object (TranslationDetails)   }   // End of mutually exclusive fields. } ``` |

| Fields | |
| --- | --- |
| `id` | `string`  Output only. Immutable. The unique identifier for the migration task. The ID is server-generated. |
| `type` | `string`  The type of the task. This must be one of the supported task types.  Assessment:   * `Assessment_Hive` - Assessment for Hive. * `Assessment_Redshift` - Assessment for Redshift. * `Assessment_Snowflake` - Assessment for Snowflake. * `Assessment_Teradata_v2` - Assessment for Teradata. * `Assessment_Oracle` - Assessment for Oracle. * `Assessment_Hadoop` - Assessment for Hadoop. * `Assessment_Informatica` - Assessment for Informatica.   Translation: See [Supported SQL dialects](https://docs.cloud.google.com/bigquery/docs/enable-sql-translations#supported_sql_dialects) for a list of supported task types. |
| `state` | `enum (State)`  Output only. The current state of the task. |
| `processingError` | `object (ErrorInfo)`  Output only. An explanation that may be populated when the task is in FAILED state. |
| `createTime` | `string (Timestamp format)`  Output only. Time when the task was created. |
| `lastUpdateTime` | `string (Timestamp format)`  Output only. Time when the task was last updated. |
| `resourceErrorDetails[]` | `object (ResourceErrorDetail)`  Output only. Provides details to errors and issues encountered while processing the task. Presence of error details does not mean that the task failed. |
| `resourceErrorCount` | `integer`  Output only. The number or resources with errors. Note: This is not the total number of errors as each resource can have more than one error. This is used to indicate truncation by having a `resourceErrorCount` that is higher than the size of `resourceErrorDetails`. |
| `metrics[]` | `object (TimeSeries)`  Output only. The metrics for the task. |
| `taskResult` | `object (MigrationTaskResult)`  Output only. The result of the task. |
| `totalProcessingErrorCount` | `integer`  Output only. Count of all the processing errors in this task and its subtasks. |
| `totalResourceErrorCount` | `integer`  Output only. Count of all the resource errors in this task and its subtasks. |
| The details of the task. The following is a list of mutually exclusive fields. At most one of the fields will be set in a response: | |
| `assessmentTaskDetails` | `object (AssessmentTaskDetails)`  Task configuration for Assessment. |
| `translationConfigDetails` | `object (TranslationConfigDetails)`  Task configuration for CW Batch/Offline SQL Translation. |
| `translationDetails` | `object (TranslationDetails)`  Task details for unified SQL Translation. |
| End of mutually exclusive fields. | |

## AssessmentTaskDetails

Assessment task config.

| JSON representation |
| --- |
| ``` {   "inputPath": string,   "outputDataset": string,   "querylogsPath": string,   "dataSource": string,   "featureHandle": {     object (AssessmentFeatureHandle)   } } ``` |

| Fields | |
| --- | --- |
| `inputPath` | `string`  Required. The Cloud Storage path for assessment input files. |
| `outputDataset` | `string`  Required. The BigQuery dataset for output. |
| `querylogsPath` | `string`  Optional. An optional Cloud Storage path to write the query logs (which is then used as an input path on the translation task) |
| `dataSource` | `string`  Required. The data source or data warehouse type (eg: TERADATA/REDSHIFT) from which the input data is extracted. |
| `featureHandle` | `object (AssessmentFeatureHandle)`  Optional. A collection of additional feature flags for this assessment. |

## AssessmentFeatureHandle

User-definable feature flags for assessment tasks.

| JSON representation |
| --- |
| ``` {   "addShareableDataset": boolean,   "generateTcoReport": boolean } ``` |

| Fields | |
| --- | --- |
| `addShareableDataset` | `boolean`  Optional. Whether to create a dataset containing non-PII data in addition to the output dataset. |
| `generateTcoReport` | `boolean`  Optional. Whether the TCO report Google Doc generation is allowlisted for the project. |

## TranslationConfigDetails

The translation config to capture necessary settings for a translation task and subtask.

| JSON representation |
| --- |
| ``` {   "sourceDialect": {     object (Dialect)   },   "targetDialect": {     object (Dialect)   },   "sourceEnv": {     object (SourceEnv)   },   "requestSource": string,   "targetTypes": [     string   ],    // The following is a list of mutually exclusive fields. At most one of the   // fields will be set in a response:   "gcsSourcePath": string   // End of mutually exclusive fields.    // The following is a list of mutually exclusive fields. At most one of the   // fields will be set in a response:   "gcsTargetPath": string   // End of mutually exclusive fields.    // The following is a list of mutually exclusive fields. At most one of the   // fields will be set in a response:   "nameMappingList": {     object (ObjectNameMappingList)   }   // End of mutually exclusive fields. } ``` |

| Fields | |
| --- | --- |
| `sourceDialect` | `object (Dialect<` |