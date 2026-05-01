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
| `reservation` | `string`  Optional. The reservation that job would use. User can specify a reservation to execute the job. If reservation is not set, reservation is determined based on the rules defined by the reservation assignments. The expected format is `projects/{project}/locations/{location}/reservations/{reservation}`. |

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
| `userDefinedFunctionResources[]` | `object (UserDefinedFunctionResource)`  Describes user-defined function resources used in the query. |
| `createDisposition` | `string`  Optional. Specifies whether the job is allowed to create new tables. The following values are supported:   * CREATE\_IF\_NEEDED: If the table does not exist, BigQuery creates the table. * CREATE\_NEVER: The table must already exist. If it does not, a 'notFound' error is returned in the job result.   The default value is CREATE\_IF\_NEEDED. Creation, truncation and append actions occur as one atomic update upon job completion. |
| `writeDisposition` | `string`  Optional. Specifies the action that occurs if the destination table already exists. The following values are supported:   * WRITE\_TRUNCATE: If the table already exists, BigQuery overwrites the data, removes the constraints, and uses the schema from the query result. * WRITE\_TRUNCATE\_DATA: If the table already exists, BigQuery overwrites the data, but keeps the constraints and schema of the existing table. * WRITE\_APPEND: If the table already exists, BigQuery appends the data to the table. * WRITE\_EMPTY: If the table already exists and contains data, a 'duplicate' error is returned in the job result.   The default value is WRITE\_EMPTY. Each action is atomic and only occurs if BigQuery is able to complete the job successfully. Creation, truncation and append actions occur as one atomic update upon job completion. |
| `defaultDataset` | `object (DatasetReference)`  Optional. Specifies the default dataset to use for unqualified table names in the query. This setting does not alter behavior of unqualified dataset names. Setting the system variable `@@dataset_id` achieves the same behavior. See <https://cloud.google.com/bigquery/docs/reference/system-variables> for more information on system variables. |
| `priority` | `string`  Optional. Specifies a priority for the query. Possible values include INTERACTIVE and BATCH. The default value is INTERACTIVE. |
| `preserveNulls` | `boolean`  [Deprecated] This property is deprecated. |
| `allowLargeResults` | `boolean`  Optional. If true and query uses legacy SQL dialect, allows the query to produce arbitrarily large result tables at a slight cost in performance. Requires destinationTable to be set. For GoogleSQL queries, this flag is ignored and large results are always allowed. However, you must still set destinationTable when result size exceeds the allowed maximum response size. |
| `useQueryCache` | `boolean`  Optional. Whether to look for the result in the query cache. The query cache is a best-effort cache that will be flushed whenever tables in the query are modified. Moreover, the query cache is only available when a query does not have a destination table specified. The default value is true. |
| `flattenResults` | `boolean`  Optional. If true and query uses legacy SQL dialect, flattens all nested and repeated fields in the query results. allowLargeResults must be true if this is set to false. For GoogleSQL queries, this flag is ignored and results are never flattened. |
| `maximumBillingTier` | `integer`  Optional. [Deprecated] Maximum billing tier allowed for this query. The billing tier controls the amount of compute resources allotted to the query, and multiplies the on-demand cost of the query accordingly. A query that runs within its allotted resources will succeed and indicate its billing tier in statistics.query.billingTier, but if the query exceeds its allotted resources, it will fail with billingTierLimitExceeded. WARNING: The billed byte amount can be multiplied by an amount up to this number! Most users should not need to alter this setting, and we recommend that you avoid introducing new uses of it. |
| `maximumBytesBilled` | `string (Int64Value format)`  Limits the bytes billed for this job. Queries that will have bytes billed beyond this limit will fail (without incurring a charge). If unspecified, this will be set to your project default. |
| `useLegacySql` | `boolean`  Optional. Specifies whether to use BigQuery's legacy SQL dialect for this query. The default value is true. If set to false, the query uses BigQuery's [GoogleSQL](https://docs.cloud.google.com/bigquery/docs/introduction-sql).  When useLegacySql is set to false, the value of flattenResults is ignored; query will be run as if flattenResults is false. |
| `parameterMode` | `string`  GoogleSQL only. Set to POSITIONAL to use positional (?) query parameters or to NAMED to use named (@myparam) query parameters in this query. |
| `queryParameters[]` | `object (QueryParameter)`  jobs.query parameters for GoogleSQL queries. |
| `schemaUpdateOptions[]` | `string`  Allows the schema of the destination table to be updated as a side effect of the query job. Schema update options are supported in three cases: when writeDisposition is WRITE\_APPEND; when writeDisposition is WRITE\_TRUNCATE\_DATA; when writeDisposition is WRITE\_TRUNCATE and the destination table is a partition of a table, specified by partition decorators. For normal tables, WRITE\_TRUNCATE will always overwrite the schema. One or more of the following values are specified:   * ALLOW\_FIELD\_ADDITION: allow adding a nullable field to the schema. * ALLOW\_FIELD\_RELAXATION: allow relaxing a required field in the original schema to nullable. |
| `timePartitioning` | `object (TimePartitioning)`  Time-based partitioning specification for the destination table. Only one of timePartitioning and rangePartitioning should be specified. |
| `rangePartitioning` | `object (RangePartitioning)`  Range partitioning specification for the destination table. Only one of timePartitioning and rangePartitioning should be specified. |
| `clustering` | `object (Clustering)`  Clustering specification for the destination table. |
| `destinationEncryptionConfiguration` | `object (EncryptionConfiguration)`  Custom encryption configuration (e.g., Cloud KMS keys) |
| `scriptOptions` | `object (ScriptOptions)`  Options controlling the execution of scripts. |
| `connectionProperties[]` | `object (ConnectionProperty)`  Connection properties which can modify the query behavior. |
| `createSession` | `boolean`  If this property is true, the job creates a new session using a randomly generated sessionId. To continue using a created session with subsequent queries, pass the existing session identifier as a `ConnectionProperty` value. The session identifier is returned as part of the `SessionInfo` message within the query statistics.  The new session's location will be set to `Job.JobReference.location` if it is present, otherwise it's set to the default location based on existing routing logic. |
| `systemVariables` | `object (SystemVariables)`  Output only. System variables for GoogleSQL queries. A system variable is output if the variable is settable and its value differs from the system default. "@@" prefix is not included in the name of the System variables. |

## SystemVariables

System variables given to a query.

| JSON representation |
| --- |
| ``` {   "types": {     string: {       object (StandardSqlDataType)     },     ...   },   "values": {     object   } } ``` |

| Fields | |
| --- | --- |
| `types` | `map (key: string, value: object (StandardSqlDataType))`  Output only. Data type for each system variable. |
| `values` | `object (Struct format)`  Output only. Value for each system variable. |

## ScriptOptions

Options related to script execution.

| JSON representation |
| --- |
| ``` {   "statementTimeoutMs": string,   "statementByteBudget": string,   "keyResultStatement": enum (KeyResultStatementKind) } ``` |

| Fields | |
| --- | --- |
| `statementTimeoutMs` | `string (Int64Value format)`  Timeout period for each statement in a script. |
| `statementByteBudget` | `string (Int64Value format)`  Limit on the number of bytes billed per statement. Exceeding this budget results in an error. |
| `keyResultStatement` | `enum (KeyResultStatementKind)`  Determines which statement in the script represents the "key result", used to populate the schema and query results of the script job. Default is LAST. |

## KeyResultStatementKind

KeyResultStatementKind controls how the key result is determined.

| Enums | |
| --- | --- |
| `KEY_RESULT_STATEMENT_KIND_UNSPECIFIED` | Default value. |
| `LAST` | The last result determines the key result. |
| `FIRST_SELECT` | The first SELECT statement determines the key result. |

## JobConfigurationLoad

JobConfigurationLoad contains the configuration properties for loading data into a destination table.

| JSON representation |
| --- |
| ``` {   "sourceUris": [     string   ],   "fileSetSpecType": enum (FileSetSpecType),   "schema": {     object (TableSchema)   },   "destinationTable": {     object (TableReference)   },   "destinationTableProperties": {     object (DestinationTableProperties)   },   "createDisposition": string,   "writeDisposition": string,   "nullMarker": string,   "fieldDelimiter": string,   "skipLeadingRows": integer,   "encoding": string,   "quote": string,   "maxBadRecords": integer,   "schemaInlineFormat": string,   "schemaInline": string,   "allowQuotedNewlines": boolean,   "sourceFormat": string,   "allowJaggedRows": boolean,   "ignoreUnknownValues": boolean,   "projectionFields": [     string   ],   "autodetect": boolean,   "schemaUpdateOptions": [     string   ],   "timePartitioning": {     object (TimePartitioning)   },   "rangePartitioning": {     object (RangePartitioning)   },   "clustering": {     object (Clustering)   },   "destinationEncryptionConfiguration": {     object (EncryptionConfiguration)   },   "useAvroLogicalTypes": boolean,   "referenceFileSchemaUri": string,   "hivePartitioningOptions": {     object (HivePartitioningOptions)   },   "decimalTargetTypes": [     enum (DecimalTargetType)   ],   "jsonExtension": enum (JsonExtension),   "parquetOptions": {     object (ParquetOptions)   },   "preserveAsciiControlCharacters": boolean,   "columnNameCharacterMap": enum (ColumnNameCharacterMap),   "copyFilesOnly": boolean,   "timeZone": string,   "nullMarkers": [     string   ],   "sourceColumnMatch": enum (SourceColumnMatch),   "dateFormat": string,   "datetimeFormat": string,   "timeFormat": string,   "timestampFormat": string } ``` |