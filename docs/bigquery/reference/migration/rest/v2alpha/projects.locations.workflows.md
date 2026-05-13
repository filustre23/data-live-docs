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
* [TranslationTaskDetails](#TranslationTaskDetails)
  + [JSON representation](#TranslationTaskDetails.SCHEMA_REPRESENTATION)
* [TeradataOptions](#TeradataOptions)
* [BteqOptions](#BteqOptions)
  + [JSON representation](#BteqOptions.SCHEMA_REPRESENTATION)
* [DatasetReference](#DatasetReference)
  + [JSON representation](#DatasetReference.SCHEMA_REPRESENTATION)
* [TranslationFileMapping](#TranslationFileMapping)
  + [JSON representation](#TranslationFileMapping.SCHEMA_REPRESENTATION)
* [FileEncoding](#FileEncoding)
* [IdentifierSettings](#IdentifierSettings)
  + [JSON representation](#IdentifierSettings.SCHEMA_REPRESENTATION)
* [IdentifierCase](#IdentifierCase)
* [IdentifierRewriteMode](#IdentifierRewriteMode)
* [TokenType](#TokenType)
* [Filter](#Filter)
  + [JSON representation](#Filter.SCHEMA_REPRESENTATION)
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
* [SourceTargetLocationMapping](#SourceTargetLocationMapping)
  + [JSON representation](#SourceTargetLocationMapping.SCHEMA_REPRESENTATION)
* [SourceLocation](#SourceLocation)
  + [JSON representation](#SourceLocation.SCHEMA_REPRESENTATION)
* [TargetLocation](#TargetLocation)
  + [JSON representation](#TargetLocation.SCHEMA_REPRESENTATION)
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
* [MetadataCaching](#MetadataCaching)
  + [JSON representation](#MetadataCaching.SCHEMA_REPRESENTATION)
* [SuggestionConfig](#SuggestionConfig)
  + [JSON representation](#SuggestionConfig.SCHEMA_REPRESENTATION)
* [SuggestionStep](#SuggestionStep)
  + [JSON representation](#SuggestionStep.SCHEMA_REPRESENTATION)
* [SuggestionType](#SuggestionType)
* [RewriteTarget](#RewriteTarget)
* [State](#State)
* [MigrationTaskOrchestrationResult](#MigrationTaskOrchestrationResult)
  + [JSON representation](#MigrationTaskOrchestrationResult.SCHEMA_REPRESENTATION)
* [AssessmentOrchestrationResultDetails](#AssessmentOrchestrationResultDetails)
  + [JSON representation](#AssessmentOrchestrationResultDetails.SCHEMA_REPRESENTATION)
* [TranslationTaskResult](#TranslationTaskResult)
  + [JSON representation](#TranslationTaskResult.SCHEMA_REPRESENTATION)
* [GcsReportLogMessage](#GcsReportLogMessage)
  + [JSON representation](#GcsReportLogMessage.SCHEMA_REPRESENTATION)
* [MigrationTaskResult](#MigrationTaskResult)
  + [JSON representation](#MigrationTaskResult.SCHEMA_REPRESENTATION)
* [State](#State_1)
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
| ``` {   "id": string,   "type": string,   "details": {     "@type": string,     field1: ...,     ...   },   "state": enum (State),   "processingError": {     object (ErrorInfo)   },   "createTime": string,   "lastUpdateTime": string,   "orchestrationResult": {     object (MigrationTaskOrchestrationResult)   },   "resourceErrorDetails": [     {       object (ResourceErrorDetail)     }   ],   "resourceErrorCount": integer,   "metrics": [     {       object (TimeSeries)     }   ],   "taskResult": {     object (MigrationTaskResult)   },   "totalProcessingErrorCount": integer,   "totalResourceErrorCount": integer,    // Union field task_details can be only one of the following:   "assessmentTaskDetails": {     object (AssessmentTaskDetails)   },   "translationTaskDetails": {     object (TranslationTaskDetails)   },   "translationConfigDetails": {     object (TranslationConfigDetails)   },   "translationDetails": {     object (TranslationDetails)   }   // End of list of possible types for union field task_details. } ``` |

| Fields | |
| --- | --- |
| `id` | `string`  Output only. Immutable. The unique identifier for the migration task. The ID is server-generated. |
| `type` | `string`  The type of the task. This must be one of the supported task types.  Assessment:   * `Assessment_Hive` - Assessment for Hive. * `Assessment_Redshift` - Assessment for Redshift. * `Assessment_Snowflake` - Assessment for Snowflake. * `Assessment_Teradata_v2` - Assessment for Teradata. * `Assessment_Oracle` - Assessment for Oracle. * `Assessment_Hadoop` - Assessment for Hadoop. * `Assessment_Informatica` - Assessment for Informatica.   Translation: See [Supported Task Types](https://docs.cloud.google.com/bigquery/docs/api-sql-translator#supported_task_types) for a list of supported task types. |
| `details` | `object`  DEPRECATED! Use one of the task\_details below. The details of the task. The type URL must be one of the supported task details messages and correspond to the Task's type. |
| `state` | `enum (State)`  Output only. The current state of the task. |
| `processingError` | `object (ErrorInfo)`  Output only. An explanation that may be populated when the task is in FAILED state. |
| `createTime` | `string (Timestamp format)`  Output only. Time when the task was created. |
| `lastUpdateTime` | `string (Timestamp format)`  Output only. Time when the task was last updated. |
| `orchestrationResult (deprecated)` | `object (MigrationTaskOrchestrationResult)`  This item is deprecated!  Output only. Deprecated: Use the taskResult field below instead. Additional information about the orchestration. |
| `resourceErrorDetails[]` | `object (ResourceErrorDetail)`  Output only. Provides details to errors and issues encountered while processing the task. Presence of error details does not mean that the task failed. |
| `resourceErrorCount` | `integer`  Output only. The number or resources with errors. Note: This is not the total number of errors as each resource can have more than one error. This is used to indicate truncation by having a `resourceErrorCount` that is higher than the size of `resourceErrorDetails`. |
| `metrics[]` | `object (TimeSeries)`  Output only. The metrics for the task. |
| `taskResult` | `object (MigrationTaskResult)`  Output only. The result of the task. |
| `totalProcessingErrorCount` | `integer`  Output only. Count of all the processing errors in this task and its subtasks. |
| `totalResourceErrorCount` | `integer`  Output only. Count of all the resource errors in this task and its subtasks. |
| Union field `task_details`. The details of the task. `task_details` can be only one of the following: | |
| `assessmentTaskDetails` | `object (AssessmentTaskDetails)`  Task configuration for Assessment. |
| `translationTaskDetails` | `object (TranslationTaskDetails)`  Task configuration for Batch SQL Translation. |
| `translationConfigDetails` | `object (TranslationConfigDetails)`  Task configuration for CW Batch/Offline SQL Translation. |
| `translationDetails` | `object (TranslationDetails)`  Task details for unified SQL Translation. |

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
| ``` {   "addShareableDataset": boolean } ``` |

| Fields | |
| --- | --- |
| `addShareableDataset` | `boolean`  Optional. Whether to create a dataset containing non-PII data in addition to the output dataset. |

## TranslationTaskDetails

The translation task config to capture necessary settings for a translation task and subtask.

| JSON representation |
| --- |
| ``` {   "inputPath": string,   "outputPath": string,   "filePaths": [     {       object (TranslationFileMapping)     }   ],   "schemaPath": string,   "fileEncoding": enum (FileEncoding),   "identifierSettings": {     object (IdentifierSettings)   },   "specialTokenMap": {     string: enum (TokenType),     ...   },   "filter": {     object (Filter)   },   "translationExceptionTable": string,    // Union field language_options can be only one of the following:   "teradataOptions": {     object (TeradataOptions)   },   "bteqOptions": {     object (BteqOptions)   }   // End of list of possible types for union field language_options. } ``` |

| Fields | |
| --- | --- |
| `inputPath` | `string`  The Cloud Storage path for translation input files. |
| `outputPath` | `string`  The Cloud Storage path for translation output files. |
| `filePaths[]` | `object (TranslationFileMapping)`  Cloud Storage files to be processed for translation. |
| `schemaPath` | `string`  The Cloud Storage path to DDL files as table schema to assist semantic translation. |
| `fileEncoding` | `enum (FileEncoding)`  The file encoding type. |
| `identifierSettings` | `object (IdentifierSettings)`  The settings for SQL identifiers. |
| `specialTokenMap` | `map (key: string, value: enum (TokenType))`  The map capturing special tokens to be replaced during translation. The key is special token in string. The value is the token data type. This is used to translate SQL query template which contains special token as place holder. The special token makes a query invalid to parse. This map will be applied to annotate those special token with types to let parser understand how to parse them into proper structure with type information. |
| `filter` | `object (Filter)`  The filter applied to translation details. |
| `translationExceptionTable` | `string`  Specifies the exact name of the bigquery table ("dataset.table") to be used for surfacing raw translation errors. If the table does not exist, we will create it. If it already exists and the schema is the same, we will re-use. If the table exists and the schema is different, we will throw an error. |
| Union field `language_options`. The language specific settings for the translation task. `language_options` can be only one of the following: | |
| `teradataOptions` | `object (TeradataOptions)`  The Teradata SQL specific settings for the translation task. |
| `bteqOptions` | `object (BteqOptions)`  The BTEQ specific settings for the translation task. |

## TeradataOptions

This type has no fields.

Teradata SQL specific translation task related settings.

## BteqOptions

BTEQ translation task related settings.

| JSON representation |
| --- |
| ``` {   "projectDataset": {     object (DatasetReference)   },   "defaultPathUri": string,   "fileReplacementMap": {     string: string,     ...   } } ``` |

| Fields | |
| --- | --- |
| `projectDataset` | `object (DatasetReference)`  Specifies the project and dataset in BigQuery that will be used for external table creation during the translation. |
| `defaultPathUri` | `string`  The Cloud Storage location to be used as the default path for files that are not otherwise specified in the file replacement map. |
| `fileReplacementMap` | `map (key: string, value: string)`  Maps the local paths that are used in BTEQ scripts (the keys) to the paths in Cloud Storage that should be used in their stead in the translation (the value). |

## DatasetReference

Reference to a BigQuery dataset.

| JSON representation |
| --- |
| ``` {   "datasetId": string,   "projectId": string,   "datasetIdAlternative": [     string   ],   "projectIdAlternative": [     string   ] } ``` |

| Fields | |
| --- | --- |
| `datasetId` | `string`  A unique ID for this dataset, without the project name. The ID must contain only letters (a-z, A-Z), numbers (0-9), or underscores (\_). The maximum length is 1,024 characters. |
| `projectId` | `string`  The ID of the project containing this dataset. |
| `datasetIdAlternative[]` | `string`  The alternative field that will be used when the service is not able to translate the received data to the datasetId field. |
| `projectIdAlternative[]` | `string`  The alternative field that will be used when the service is not able to translate the received data to the projectId field. |

## TranslationFileMapping

Mapping between an input and output file to be translated in a subtask.

| JSON representation |
| --- |
| ``` {   "inputPath": string,   "outputPath": string } ``` |

| Fields | |
| --- | --- |
| `inputPath` | `string`  The Cloud Storage path for a file to translation in a subtask. |
| `outputPath` | `string`  The Cloud Storage path to write back the corresponding input file to. |

## FileEncoding

The file encoding types.

| Enums | |
| --- | --- |
| `FILE_ENCODING_UNSPECIFIED` | File encoding setting is not specified. |
| `UTF_8` | File encoding is UTF\_8. |
| `ISO_8859_1` | File encoding is ISO\_8859\_1. |
| `US_ASCII` | File encoding is US\_ASCII. |
| `UTF_16` | File encoding is UTF\_16. |
| `UTF_16LE` | File encoding is UTF\_16LE. |
| `UTF_16BE` | File encoding is UTF\_16BE. |

## IdentifierSettings

Settings related to SQL identifiers.

| JSON representation |
| --- |
| ``` {   "outputIdentifierCase": enum (IdentifierCase),   "identifierRewriteMode": enum (IdentifierRewriteMode) } ``` |

| Fields | |
| --- | --- |
| `outputIdentifierCase` | `enum (IdentifierCase)`  The setting to control output queries' identifier case. |
| `identifierRewriteMode` | `enum (IdentifierRewriteMode)`  Specifies the rewrite mode for SQL identifiers. |

## IdentifierCase

The identifier case type.

| Enums | |
| --- | --- |
| `IDENTIFIER_CASE_UNSPECIFIED` | The identifier case is not specified. |
| `ORIGINAL` | Identifiers' cases will be kept as the original cases. |
| `UPPER` | Identifiers will be in upper cases. |
| `LOWER` | Identifiers will be in lower cases. |

## IdentifierRewriteMode

The SQL identifier rewrite mode.

| Enums | |
| --- | --- |
| `IDENTIFIER_REWRITE_MODE_UNSPECIFIED` | SQL Identifier rewrite mode is unspecified. |
| `NONE` | SQL identifiers won't be rewrite. |
| `REWRITE_ALL` | All SQL identifiers will be rewrite. |

## TokenType

The special token data type.

|  | |
| --- | --- |