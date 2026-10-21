* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback

# Job Stay organized with collections Save and categorize content based on your preferences.

* [JSON representation](#SCHEMA_REPRESENTATION)
* [JobConfiguration](#JobConfiguration)
  + [JSON representation](#JobConfiguration.SCHEMA_REPRESENTATION)
* [JobConfigurationQuery](#JobConfigurationQuery)
  + [JSON representation](#JobConfigurationQuery.SCHEMA_REPRESENTATION)
* [SystemVariables](#SystemVariables)
  + [JSON representation](#SystemVariables.SCHEMA_REPRESENTATION)
* [ScriptOptions](#ScriptOptions)
  + [JSON representation](#ScriptOptions.SCHEMA_REPRESENTATION)
* [KeyResultStatementKind](#KeyResultStatementKind)
* [JobConfigurationLoad](#JobConfigurationLoad)
  + [JSON representation](#JobConfigurationLoad.SCHEMA_REPRESENTATION)
* [DestinationTableProperties](#DestinationTableProperties)
  + [JSON representation](#DestinationTableProperties.SCHEMA_REPRESENTATION)
* [ColumnNameCharacterMap](#ColumnNameCharacterMap)
* [SourceColumnMatch](#SourceColumnMatch)
* [JobConfigurationTableCopy](#JobConfigurationTableCopy)
  + [JSON representation](#JobConfigurationTableCopy.SCHEMA_REPRESENTATION)
* [OperationType](#OperationType)
* [JobConfigurationExtract](#JobConfigurationExtract)
  + [JSON representation](#JobConfigurationExtract.SCHEMA_REPRESENTATION)
* [ModelExtractOptions](#ModelExtractOptions)
  + [JSON representation](#ModelExtractOptions.SCHEMA_REPRESENTATION)
* [JobStatistics](#JobStatistics)
  + [JSON representation](#JobStatistics.SCHEMA_REPRESENTATION)
* [JobStatistics2](#JobStatistics2)
  + [JSON representation](#JobStatistics2.SCHEMA_REPRESENTATION)
* [ExplainQueryStage](#ExplainQueryStage)
  + [JSON representation](#ExplainQueryStage.SCHEMA_REPRESENTATION)
* [ExplainQueryStep](#ExplainQueryStep)
  + [JSON representation](#ExplainQueryStep.SCHEMA_REPRESENTATION)
* [ComputeMode](#ComputeMode)
* [QueryTimelineSample](#QueryTimelineSample)
  + [JSON representation](#QueryTimelineSample.SCHEMA_REPRESENTATION)
* [PropertyGraphReference](#PropertyGraphReference)
  + [JSON representation](#PropertyGraphReference.SCHEMA_REPRESENTATION)
* [MlStatistics](#MlStatistics)
  + [JSON representation](#MlStatistics.SCHEMA_REPRESENTATION)
* [TrainingType](#TrainingType)
* [ExportDataStatistics](#ExportDataStatistics)
  + [JSON representation](#ExportDataStatistics.SCHEMA_REPRESENTATION)
* [ExternalServiceCost](#ExternalServiceCost)
  + [JSON representation](#ExternalServiceCost.SCHEMA_REPRESENTATION)
* [BiEngineStatistics](#BiEngineStatistics)
  + [JSON representation](#BiEngineStatistics.SCHEMA_REPRESENTATION)
* [BiEngineMode](#BiEngineMode)
* [BiEngineAccelerationMode](#BiEngineAccelerationMode)
* [BiEngineReason](#BiEngineReason)
  + [JSON representation](#BiEngineReason.SCHEMA_REPRESENTATION)
* [Code](#Code)
* [LoadQueryStatistics](#LoadQueryStatistics)
  + [JSON representation](#LoadQueryStatistics.SCHEMA_REPRESENTATION)
* [SearchStatistics](#SearchStatistics)
  + [JSON representation](#SearchStatistics.SCHEMA_REPRESENTATION)
* [IndexUsageMode](#IndexUsageMode)
* [IndexUnusedReason](#IndexUnusedReason)
  + [JSON representation](#IndexUnusedReason.SCHEMA_REPRESENTATION)
* [Code](#Code_1)
* [VectorSearchStatistics](#VectorSearchStatistics)
  + [JSON representation](#VectorSearchStatistics.SCHEMA_REPRESENTATION)
* [IndexUsageMode](#IndexUsageMode_1)
* [StoredColumnsUsage](#StoredColumnsUsage)
  + [JSON representation](#StoredColumnsUsage.SCHEMA_REPRESENTATION)
* [StoredColumnsUnusedReason](#StoredColumnsUnusedReason)
  + [JSON representation](#StoredColumnsUnusedReason.SCHEMA_REPRESENTATION)
* [Code](#Code_2)
* [PerformanceInsights](#PerformanceInsights)
  + [JSON representation](#PerformanceInsights.SCHEMA_REPRESENTATION)
* [StagePerformanceStandaloneInsight](#StagePerformanceStandaloneInsight)
  + [JSON representation](#StagePerformanceStandaloneInsight.SCHEMA_REPRESENTATION)
* [HighCardinalityJoin](#HighCardinalityJoin)
  + [JSON representation](#HighCardinalityJoin.SCHEMA_REPRESENTATION)
* [PartitionSkew](#PartitionSkew)
  + [JSON representation](#PartitionSkew.SCHEMA_REPRESENTATION)
* [SkewSource](#SkewSource)
  + [JSON representation](#SkewSource.SCHEMA_REPRESENTATION)
* [StagePerformanceChangeInsight](#StagePerformanceChangeInsight)
  + [JSON representation](#StagePerformanceChangeInsight.SCHEMA_REPRESENTATION)
* [InputDataChange](#InputDataChange)
  + [JSON representation](#InputDataChange.SCHEMA_REPRESENTATION)
* [QueryInfo](#QueryInfo)
  + [JSON representation](#QueryInfo.SCHEMA_REPRESENTATION)
* [SparkStatistics](#SparkStatistics)
  + [JSON representation](#SparkStatistics.SCHEMA_REPRESENTATION)
* [LoggingInfo](#LoggingInfo)
  + [JSON representation](#LoggingInfo.SCHEMA_REPRESENTATION)
* [MaterializedViewStatistics](#MaterializedViewStatistics)
  + [JSON representation](#MaterializedViewStatistics.SCHEMA_REPRESENTATION)
* [MaterializedView](#MaterializedView)
  + [JSON representation](#MaterializedView.SCHEMA_REPRESENTATION)
* [RejectedReason](#RejectedReason)
* [MetadataCacheStatistics](#MetadataCacheStatistics)
  + [JSON representation](#MetadataCacheStatistics.SCHEMA_REPRESENTATION)
* [TableMetadataCacheUsage](#TableMetadataCacheUsage)
  + [JSON representation](#TableMetadataCacheUsage.SCHEMA_REPRESENTATION)
* [UnusedReason](#UnusedReason)
* [GenAiStats](#GenAiStats)
  + [JSON representation](#GenAiStats.SCHEMA_REPRESENTATION)
* [GenAiErrorStats](#GenAiErrorStats)
  + [JSON representation](#GenAiErrorStats.SCHEMA_REPRESENTATION)
* [GenAiFunctionStats](#GenAiFunctionStats)
  + [JSON representation](#GenAiFunctionStats.SCHEMA_REPRESENTATION)
* [GenAiFunctionErrorStats](#GenAiFunctionErrorStats)
  + [JSON representation](#GenAiFunctionErrorStats.SCHEMA_REPRESENTATION)
* [GenAiFunctionCostOptimizationStats](#GenAiFunctionCostOptimizationStats)
  + [JSON representation](#GenAiFunctionCostOptimizationStats.SCHEMA_REPRESENTATION)
* [GenAiFunctionCacheStats](#GenAiFunctionCacheStats)
  + [JSON representation](#GenAiFunctionCacheStats.SCHEMA_REPRESENTATION)
* [JobStatistics3](#JobStatistics3)
  + [JSON representation](#JobStatistics3.SCHEMA_REPRESENTATION)
* [JobStatistics4](#JobStatistics4)
  + [JSON representation](#JobStatistics4.SCHEMA_REPRESENTATION)
* [CopyJobStatistics](#CopyJobStatistics)
  + [JSON representation](#CopyJobStatistics.SCHEMA_REPRESENTATION)
* [ScriptStatistics](#ScriptStatistics)
  + [JSON representation](#ScriptStatistics.SCHEMA_REPRESENTATION)
* [EvaluationKind](#EvaluationKind)
* [ScriptStackFrame](#ScriptStackFrame)
  + [JSON representation](#ScriptStackFrame.SCHEMA_REPRESENTATION)
* [RowLevelSecurityStatistics](#RowLevelSecurityStatistics)
  + [JSON representation](#RowLevelSecurityStatistics.SCHEMA_REPRESENTATION)
* [DataMaskingStatistics](#DataMaskingStatistics)
  + [JSON representation](#DataMaskingStatistics.SCHEMA_REPRESENTATION)
* [TransactionInfo](#TransactionInfo)
  + [JSON representation](#TransactionInfo.SCHEMA_REPRESENTATION)
* [ReservationEdition](#ReservationEdition)
* [JobStatus](#JobStatus)
  + [JSON representation](#JobStatus.SCHEMA_REPRESENTATION)

| JSON representation |
| --- |
| ``` {   "kind": string,   "etag": string,   "id": string,   "selfLink": string,   "user_email": string,   "configuration": {     object (JobConfiguration)   },   "jobReference": {     object (JobReference)   },   "statistics": {     object (JobStatistics)   },   "status": {     object (JobStatus)   },   "principal_subject": string,   "jobCreationReason": {     object (JobCreationReason)   } } ``` |

| Fields | |
| --- | --- |
| `kind` | `string`  Output only. The type of the resource. |
| `etag` | `string`  Output only. A hash of this resource. |
| `id` | `string`  Output only. Opaque ID field of the job. |
| `selfLink` | `string`  Output only. A URL that can be used to access the resource again. |
| `user_email` | `string`  Output only. Email address of the user who ran the job. |
| `configuration` | `object (JobConfiguration)`  Required. Describes the job configuration. |
| `jobReference` | `object (JobReference)`  Optional. Reference describing the unique-per-user name of the job. |
| `statistics` | `object (JobStatistics)`  Output only. Information about the job, including starting time and ending time of the job. |
| `status` | `object (JobStatus)`  Output only. The status of this job. Examine this value when polling an asynchronous job to see if the job is complete. |
| `principal_subject` | `string`  Output only. [Full-projection-only] String representation of identity of requesting party. Populated for both first- and third-party identities. Only present for APIs that support third-party identities. |
| `jobCreationReason` | `object (JobCreationReason)`  Output only. The reason why a Job was created. |

## JobConfiguration

| JSON representation |
| --- |
| ``` {   "jobType": string,   "query": {     object (JobConfigurationQuery)   },   "load": {     object (JobConfigurationLoad)   },   "copy": {     object (JobConfigurationTableCopy)   },   "extract": {     object (JobConfigurationExtract)   },   "dryRun": boolean,   "jobTimeoutMs": string,   "labels": {     string: string,     ...   },   "reservation": string } ``` |

| Fields | |
| --- | --- |
| `jobType` | `string`  Output only. The type of the job. Can be QUERY, LOAD, EXTRACT, COPY or UNKNOWN. |
| `query` | `object (JobConfigurationQuery)`  [Pick one] Configures a query job. |
| `load` | `object (JobConfigurationLoad)`  [Pick one] Configures a load job. |
| `copy` | `object (JobConfigurationTableCopy)`  [Pick one] Copies a table. |
| `extract` | `object (JobConfigurationExtract)`  [Pick one] Configures an extract job. |
| `dryRun` | `boolean`  Optional. If set, don't actually run this job. A valid query will return a mostly empty response with some processing statistics, while an invalid query will return the same error it would if it wasn't a dry run. Behavior of non-query jobs is undefined. |
| `jobTimeoutMs` | `string (Int64Value format)`  Optional. Job timeout in milliseconds relative to the job creation time. If this time limit is exceeded, BigQuery attempts to stop the job, but might not always succeed in canceling it before the job completes. For example, a job that takes more than 60 seconds to complete has a better chance of being stopped than a job that takes 10 seconds to complete. |
| `labels` | `map (key: string, value: string)`  The labels associated with this job. You can use these to organize and group your jobs. Label keys and values can be no longer than 63 characters, can only contain lowercase letters, numeric characters, underscores and dashes. International characters are allowed. Label values are optional. Label keys must start with a letter and each label in the list must have a different key. |
| `reservation` | `string`  Optional. The reservation that job would use. User can specify a reservation to execute the job. If reservation is not set, reservation is determined based on the rules defined by the reservation assignments. The expected format is `projects/{project}/locations/{location}/reservations/{reservation}`. Forces the query to use on-demand billing when set to `none`, which requires the project or organization to have `reservation_override_mode` set to `ALLOW_ANY_OVERRIDE`. |

## JobConfigurationQuery

JobConfigurationQuery configures a BigQuery query job.

| JSON representation |
| --- |
| ``` {   "query": string,   "destinationTable": {     object (TableReference)   },   "tableDefinitions": {     string: {       object (ExternalDataConfiguration)     },     ...   },   "userDefinedFunctionResources": [     {       object (UserDefinedFunctionResource)     }   ],   "createDisposition": string,   "writeDisposition": string,   "defaultDataset": {     object (DatasetReference)   },   "priority": string,   "preserveNulls": boolean,   "allowLargeResults": boolean,   "useQueryCache": boolean,   "flattenResults": boolean,   "maximumBillingTier": integer,   "maximumBytesBilled": string,   "useLegacySql": boolean,   "parameterMode": string,   "queryParameters": [     {       object (QueryParameter)     }   ],   "schemaUpdateOptions": [     string   ],   "timePartitioning": {     object (TimePartitioning)   },   "rangePartitioning": {     object (RangePartitioning)   },   "clustering": {     object (Clustering)   },   "destinationEncryptionConfiguration": {     object (EncryptionConfiguration)   },   "scriptOptions": {     object (ScriptOptions)   },   "connectionProperties": [     {       object (ConnectionProperty)     }   ],   "createSession": boolean,   "systemVariables": {     object (SystemVariables)   } } ``` |

| Fields | |
| --- | --- |
| `query` | `string`  [Required] SQL query text to execute. The useLegacySql field can be used to indicate whether the query uses legacy SQL or GoogleSQL. |
| `destinationTable` | `object (TableReference)`  Optional. Describes the table where the query results should be stored. This property must be set for large results that exceed the maximum response size. For queries that produce anonymous (cached) results, this field will be populated by BigQuery. |
| `tableDefinitions` | `map (key: string, value: object (ExternalDataConfiguration))`  Optional. You can specify external table definitions, which operate as ephemeral tables that can be queried. These definitions are configured using a JSON map, where the string key represents the table identifier, and the value is the corresponding external data configuration object. |
| `userDefinedFunctionResources[]` | `object (UserDefinedFunctionResource)`  Describes user-defined function resources used in the q |