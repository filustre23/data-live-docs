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
| ``` {   "id": string,   "type": string,   "state": enum (State),   "processingError": {     object (ErrorInfo)   },   "createTime": string,   "lastUpdateTime": string,   "resourceErrorDetails": [     {       object (ResourceErrorDetail)     }   ],   "resourceErrorCount": integer,   "metrics": [     {       object (TimeSeries)     }   ],   "taskResult": {     object (MigrationTaskResult)   },   "totalProcessingErrorCount": integer,   "totalResourceErrorCount": integer,    // Union field task_details can be only one of the following:   "assessmentTaskDetails": {     object (AssessmentTaskDetails)   },   "translationConfigDetails": {     object (TranslationConfigDetails)   },   "translationDetails": {     object (TranslationDetails)   }   // End of list of possible types for union field task_details. } ``` |

| Fields | |
| --- | --- |
| `id` | `string`  Output only. Immutable. The unique identifier for the migration task. The ID is server-generated. |
| `type` | `string`  The type of the task. This must be one of the supported task types.  Assessment:   * `Assessment_Hive` - Assessment for Hive. * `Assessment_Redshift` - Assessment for Redshift. * `Assessment_Snowflake` - Assessment for Snowflake. * `Assessment_Teradata_v2` - Assessment for Teradata. * `Assessment_Oracle` - Assessment for Oracle. * `Assessment_Hadoop` - Assessment for Hadoop. * `Assessment_Informatica` - Assessment for Informatica.   Translation: See [Supported Task Types](https://docs.cloud.google.com/bigquery/docs/api-sql-translator#supported_task_types) for a list of supported task types. |
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
| Union field `task_details`. The details of the task. `task_details` can be only one of the following: | |
| `assessmentTaskDetails` | `object (AssessmentTaskDetails)`  Task configuration for Assessment. |
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

## TranslationConfigDetails

The translation config to capture necessary settings for a translation task and subtask.

| JSON representation |
| --- |
| ``` {   "sourceDialect": {     object (Dialect)   },   "targetDialect": {     object (Dialect)   },   "sourceEnv": {     object (SourceEnv)   },   "requestSource": string,   "targetTypes": [     string   ],    // Union field source_location can be only one of the following:   "gcsSourcePath": string   // End of list of possible types for union field source_location.    // Union field target_location can be only one of the following:   "gcsTargetPath": string   // End of list of possible types for union field target_location.    // Union field output_name_mapping can be only one of the following:   "nameMappingList": {     object (ObjectNameMappingList)   }   // End of list of possible types for union field output_name_mapping. } ``` |

| Fields | |
| --- | --- |
| `sourceDialect` | `object (Dialect)`  The dialect of the input files. |
| `targetDialect` | `object (Dialect)`  The target dialect for the engine to translate the input to. |
| `sourceEnv` | `object (SourceEnv)`  The default source environment values for the translation. |
| `requestSource` | `string`  The indicator to show translation request initiator. |
| `targetTypes[]` | `string`  The types of output to generate, e.g. sql, metadata etc. If not specified, a default set of targets will be generated. Some additional target types may be slower to generate. See the documentation for the set of available target types. |
| Union field `source_location`. The chosen path where the source for input files will be found. `source_location` can be only one of the following: | |
| `gcsSourcePath` | `string`  The Cloud Storage path for a directory of files to translate in a task. |
| Union field `target_location`. The chosen path where the destination for output files will be found. `target_location` can be only one of the following: | |
| `gcsTargetPath` | `string`  The Cloud Storage path to write back the corresponding input files to. |
| Union field `output_name_mapping`. The mapping of full SQL object names from their current state to the desired output. `output_name_mapping` can be only one of the following: | |
| `nameMappingList` | `object (ObjectNameMappingList)`  The mapping of objects to their desired output names in list form. |

## ObjectNameMappingList

Represents a map of name mappings using a list of key:value proto messages of existing name to desired output name.

| JSON representation |
| --- |
| ``` {   "nameMap": [     {       object (ObjectNameMapping)     }   ] } ``` |

| Fields | |
| --- | --- |
| `nameMap[]` | `object (ObjectNameMapping)`  The elements of the object name map. |

## ObjectNameMapping

Represents a key-value pair of NameMappingKey to NameMappingValue to represent the mapping of SQL names from the input value to desired output.

| JSON representation |
| --- |
| ``` {   "source": {     object (NameMappingKey)   },   "target": {     object (NameMappingValue)   } } ``` |

| Fields | |
| --- | --- |
| `source` | `object (NameMappingKey)`  The name of the object in source that is being mapped. |
| `target` | `object (NameMappingValue)`  The desired target name of the object that is being mapped. |

## NameMappingKey

The potential components of a full name mapping that will be mapped during translation in the source data warehouse.

| JSON representation |
| --- |
| ``` {   "type": enum (Type),   "database": string,   "schema": string,   "relation": string,   "attribute": string } ``` |

| Fields | |
| --- | --- |
| `type` | `enum (Type)`  The type of object that is being mapped. |
| `database` | `string`  The database name (BigQuery project ID equivalent in the source data warehouse). |
| `schema` | `string`  The schema name (BigQuery dataset equivalent in the source data warehouse). |
| `relation` | `string`  The relation name (BigQuery table or view equivalent in the source data warehouse). |
| `attribute` | `string`  The attribute name (BigQuery column equivalent in the source data warehouse). |

## Type

The type of the object that is being mapped.

| Enums | |
| --- | --- |
| `TYPE_UNSPECIFIED` | Unspecified name mapping type. |
| `DATABASE` | The object being mapped is a database. |
| `SCHEMA` | The object being mapped is a schema. |
| `RELATION` | The object being mapped is a relation. |
| `ATTRIBUTE` | The object being mapped is an attribute. |
| `RELATION_ALIAS` | The object being mapped is a relation alias. |
| `ATTRIBUTE_ALIAS` | The object being mapped is a an attribute alias. |
| `FUNCTION` | The object being mapped is a function. |

## NameMappingValue

The potential components of a full name mapping that will be mapped during translation in the target data warehouse.

| JSON representation |
| --- |
| ``` {   "database": string,   "schema": string,   "relation": string,   "attribute": string } ``` |

| Fields | |
| --- | --- |
| `database` | `string`  The database name (BigQuery project ID equivalent in the target data warehouse). |
| `schema` | `string`  The schema name (BigQuery dataset equivalent in the target data warehouse). |
| `relation` | `string`  The relation name (BigQuery table or view equivalent in the target data warehouse). |
| `attribute` | `string`  The attribute name (BigQuery column equivalent in the target data warehouse). |

## Dialect

The possible dialect options for translation.

| JSON representation |
| --- |
| ``` {    // Union field dialect_value can be only one of the following:   "bigqueryDialect": {     object (BigQueryDialect)   },   "hiveqlDialect": {     object (HiveQLDialect)   },   "redshiftDialect": {     object (RedshiftDialect)   },   "teradataDialect": {     object (TeradataDialect)   },   "oracleDialect": {     object (OracleDialect)   },   "sparksqlDialect": {     object (SparkSQLDialect)   },   "snowflakeDialect": {     object (SnowflakeDialect)   },   "netezzaDialect": {     object (NetezzaDialect)   },   "azureSynapseDialect": {     object (AzureSynapseDialect)   },   "verticaDialect": {     object (VerticaDialect)   },   "sqlServerDialect": {     object (SQLServerDialect)   },   "postgresqlDialect": {     object (PostgresqlDialect)   },   "prestoDialect": {     object (PrestoDialect)   },   "mysqlDialect": {     object (MySQLDialect)   },   "db2Dialect": {     object (DB2Dialect)   },   "sqliteDialect": {     object (SQLiteDialect)   },   "greenplumDialect": {     object (GreenplumDialect)   }   // End of list of possible types for union field dialect_value. } ``` |

| Fields | |
| --- | --- |
| Union field `dialect_value`. The possible dialect options that this message represents. `dialect_value` can be only one of the following: | |
| `bigqueryDialect` | `object (BigQueryDialect)`  The BigQuery dialect |
| `hiveqlDialect` | `object (HiveQLDialect)`  The HiveQL dialect |
| `redshiftDialect` | `object (RedshiftDialect)`  The Redshift dialect |
| `teradataDialect` | `object (TeradataDialect)`  The Teradata dialect |
| `oracleDialect` | `object (OracleDialect)`  The Oracle dialect |
| `sparksqlDialect` | `object (SparkSQLDialect)`  The SparkSQL dialect |
| `snowflakeDialect` | `object (SnowflakeDialect)`  The Snowflake dialect |
| `netezzaDialect` | `object (NetezzaDial` |