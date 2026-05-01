* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback

# BigQueryAuditMetadata Stay organized with collections Save and categorize content based on your preferences.

* [JSON representation](#SCHEMA_REPRESENTATION)
* [BigQueryAuditMetadata.JobInsertion](#BigQueryAuditMetadata.JobInsertion)
  + [JSON representation](#BigQueryAuditMetadata.JobInsertion.SCHEMA_REPRESENTATION)
* [BigQueryAuditMetadata.Job](#BigQueryAuditMetadata.Job)
  + [JSON representation](#BigQueryAuditMetadata.Job.SCHEMA_REPRESENTATION)
* [BigQueryAuditMetadata.JobConfig](#BigQueryAuditMetadata.JobConfig)
  + [JSON representation](#BigQueryAuditMetadata.JobConfig.SCHEMA_REPRESENTATION)
* [BigQueryAuditMetadata.JobConfig.Query](#BigQueryAuditMetadata.JobConfig.Query)
  + [JSON representation](#BigQueryAuditMetadata.JobConfig.Query.SCHEMA_REPRESENTATION)
* [BigQueryAuditMetadata.TableDefinition](#BigQueryAuditMetadata.TableDefinition)
  + [JSON representation](#BigQueryAuditMetadata.TableDefinition.SCHEMA_REPRESENTATION)
* [BigQueryAuditMetadata.EncryptionInfo](#BigQueryAuditMetadata.EncryptionInfo)
  + [JSON representation](#BigQueryAuditMetadata.EncryptionInfo.SCHEMA_REPRESENTATION)
* [BigQueryAuditMetadata.JobConfig.Load](#BigQueryAuditMetadata.JobConfig.Load)
  + [JSON representation](#BigQueryAuditMetadata.JobConfig.Load.SCHEMA_REPRESENTATION)
* [BigQueryAuditMetadata.JobConfig.Extract](#BigQueryAuditMetadata.JobConfig.Extract)
  + [JSON representation](#BigQueryAuditMetadata.JobConfig.Extract.SCHEMA_REPRESENTATION)
* [BigQueryAuditMetadata.JobConfig.TableCopy](#BigQueryAuditMetadata.JobConfig.TableCopy)
  + [JSON representation](#BigQueryAuditMetadata.JobConfig.TableCopy.SCHEMA_REPRESENTATION)
* [BigQueryAuditMetadata.JobStatus](#BigQueryAuditMetadata.JobStatus)
  + [JSON representation](#BigQueryAuditMetadata.JobStatus.SCHEMA_REPRESENTATION)
* [BigQueryAuditMetadata.JobStats](#BigQueryAuditMetadata.JobStats)
  + [JSON representation](#BigQueryAuditMetadata.JobStats.SCHEMA_REPRESENTATION)
* [BigQueryAuditMetadata.JobStats.Query](#BigQueryAuditMetadata.JobStats.Query)
  + [JSON representation](#BigQueryAuditMetadata.JobStats.Query.SCHEMA_REPRESENTATION)
* [BigQueryAuditMetadata.AuthorizationResult](#BigQueryAuditMetadata.AuthorizationResult)
  + [JSON representation](#BigQueryAuditMetadata.AuthorizationResult.SCHEMA_REPRESENTATION)
* [BigQueryAuditMetadata.JobStats.Load](#BigQueryAuditMetadata.JobStats.Load)
  + [JSON representation](#BigQueryAuditMetadata.JobStats.Load.SCHEMA_REPRESENTATION)
* [BigQueryAuditMetadata.JobStats.Extract](#BigQueryAuditMetadata.JobStats.Extract)
  + [JSON representation](#BigQueryAuditMetadata.JobStats.Extract.SCHEMA_REPRESENTATION)
* [BigQueryAuditMetadata.JobStats.ReservationResourceUsage](#BigQueryAuditMetadata.JobStats.ReservationResourceUsage)
  + [JSON representation](#BigQueryAuditMetadata.JobStats.ReservationResourceUsage.SCHEMA_REPRESENTATION)
* [BigQueryAuditMetadata.JobChange](#BigQueryAuditMetadata.JobChange)
  + [JSON representation](#BigQueryAuditMetadata.JobChange.SCHEMA_REPRESENTATION)
* [BigQueryAuditMetadata.JobDeletion](#BigQueryAuditMetadata.JobDeletion)
  + [JSON representation](#BigQueryAuditMetadata.JobDeletion.SCHEMA_REPRESENTATION)
* [BigQueryAuditMetadata.DatasetCreation](#BigQueryAuditMetadata.DatasetCreation)
  + [JSON representation](#BigQueryAuditMetadata.DatasetCreation.SCHEMA_REPRESENTATION)
* [BigQueryAuditMetadata.Dataset](#BigQueryAuditMetadata.Dataset)
  + [JSON representation](#BigQueryAuditMetadata.Dataset.SCHEMA_REPRESENTATION)
* [BigQueryAuditMetadata.EntityInfo](#BigQueryAuditMetadata.EntityInfo)
  + [JSON representation](#BigQueryAuditMetadata.EntityInfo.SCHEMA_REPRESENTATION)
* [BigQueryAuditMetadata.BigQueryAcl](#BigQueryAuditMetadata.BigQueryAcl)
  + [JSON representation](#BigQueryAuditMetadata.BigQueryAcl.SCHEMA_REPRESENTATION)
* [BigQueryAuditMetadata.DatasetChange](#BigQueryAuditMetadata.DatasetChange)
  + [JSON representation](#BigQueryAuditMetadata.DatasetChange.SCHEMA_REPRESENTATION)
* [BindingDelta](#BindingDelta)
  + [JSON representation](#BindingDelta.SCHEMA_REPRESENTATION)
* [BigQueryAuditMetadata.AccessChange](#BigQueryAuditMetadata.AccessChange)
  + [JSON representation](#BigQueryAuditMetadata.AccessChange.SCHEMA_REPRESENTATION)
* [BigQueryAuditMetadata.DatasetDeletion](#BigQueryAuditMetadata.DatasetDeletion)
  + [JSON representation](#BigQueryAuditMetadata.DatasetDeletion.SCHEMA_REPRESENTATION)
* [BigQueryAuditMetadata.TableCreation](#BigQueryAuditMetadata.TableCreation)
  + [JSON representation](#BigQueryAuditMetadata.TableCreation.SCHEMA_REPRESENTATION)
* [BigQueryAuditMetadata.Table](#BigQueryAuditMetadata.Table)
  + [JSON representation](#BigQueryAuditMetadata.Table.SCHEMA_REPRESENTATION)
* [BigQueryAuditMetadata.TableViewDefinition](#BigQueryAuditMetadata.TableViewDefinition)
  + [JSON representation](#BigQueryAuditMetadata.TableViewDefinition.SCHEMA_REPRESENTATION)
* [PrivacyPolicy](#PrivacyPolicy)
  + [JSON representation](#PrivacyPolicy.SCHEMA_REPRESENTATION)
* [AggregationThresholdPolicy](#AggregationThresholdPolicy)
  + [JSON representation](#AggregationThresholdPolicy.SCHEMA_REPRESENTATION)
* [DifferentialPrivacyPolicy](#DifferentialPrivacyPolicy)
  + [JSON representation](#DifferentialPrivacyPolicy.SCHEMA_REPRESENTATION)
* [JoinRestrictionPolicy](#JoinRestrictionPolicy)
  + [JSON representation](#JoinRestrictionPolicy.SCHEMA_REPRESENTATION)
* [BigQueryAuditMetadata.TableConstraints](#BigQueryAuditMetadata.TableConstraints)
  + [JSON representation](#BigQueryAuditMetadata.TableConstraints.SCHEMA_REPRESENTATION)
* [BigQueryAuditMetadata.TableConstraints.PrimaryKey](#BigQueryAuditMetadata.TableConstraints.PrimaryKey)
  + [JSON representation](#BigQueryAuditMetadata.TableConstraints.PrimaryKey.SCHEMA_REPRESENTATION)
* [BigQueryAuditMetadata.TableConstraints.ForeignKey](#BigQueryAuditMetadata.TableConstraints.ForeignKey)
  + [JSON representation](#BigQueryAuditMetadata.TableConstraints.ForeignKey.SCHEMA_REPRESENTATION)
* [TimePartitioning](#TimePartitioning)
  + [JSON representation](#TimePartitioning.SCHEMA_REPRESENTATION)
* [RangePartitioning](#RangePartitioning)
  + [JSON representation](#RangePartitioning.SCHEMA_REPRESENTATION)
* [Clustering](#Clustering)
  + [JSON representation](#Clustering.SCHEMA_REPRESENTATION)
* [PartitioningDefinition](#PartitioningDefinition)
  + [JSON representation](#PartitioningDefinition.SCHEMA_REPRESENTATION)
* [PartitionedColumn](#PartitionedColumn)
  + [JSON representation](#PartitionedColumn.SCHEMA_REPRESENTATION)
* [BigQueryAuditMetadata.TableChange](#BigQueryAuditMetadata.TableChange)
  + [JSON representation](#BigQueryAuditMetadata.TableChange.SCHEMA_REPRESENTATION)
* [BigQueryAuditMetadata.TableChange.AlterTableStats](#BigQueryAuditMetadata.TableChange.AlterTableStats)
  + [JSON representation](#BigQueryAuditMetadata.TableChange.AlterTableStats.SCHEMA_REPRESENTATION)
* [BigQueryAuditMetadata.TableDeletion](#BigQueryAuditMetadata.TableDeletion)
  + [JSON representation](#BigQueryAuditMetadata.TableDeletion.SCHEMA_REPRESENTATION)
* [BigQueryAuditMetadata.TableDataRead](#BigQueryAuditMetadata.TableDataRead)
  + [JSON representation](#BigQueryAuditMetadata.TableDataRead.SCHEMA_REPRESENTATION)
* [BigQueryAuditMetadata.TableDataChange](#BigQueryAuditMetadata.TableDataChange)
  + [JSON representation](#BigQueryAuditMetadata.TableDataChange.SCHEMA_REPRESENTATION)
* [BigQueryAuditMetadata.ModelDeletion](#BigQueryAuditMetadata.ModelDeletion)
  + [JSON representation](#BigQueryAuditMetadata.ModelDeletion.SCHEMA_REPRESENTATION)
* [BigQueryAuditMetadata.ModelCreation](#BigQueryAuditMetadata.ModelCreation)
  + [JSON representation](#BigQueryAuditMetadata.ModelCreation.SCHEMA_REPRESENTATION)
* [BigQueryAuditMetadata.Model](#BigQueryAuditMetadata.Model)
  + [JSON representation](#BigQueryAuditMetadata.Model.SCHEMA_REPRESENTATION)
* [BigQueryAuditMetadata.ModelMetadataChange](#BigQueryAuditMetadata.ModelMetadataChange)
  + [JSON representation](#BigQueryAuditMetadata.ModelMetadataChange.SCHEMA_REPRESENTATION)
* [BigQueryAuditMetadata.ModelDataChange](#BigQueryAuditMetadata.ModelDataChange)
  + [JSON representation](#BigQueryAuditMetadata.ModelDataChange.SCHEMA_REPRESENTATION)
* [BigQueryAuditMetadata.ModelDataRead](#BigQueryAuditMetadata.ModelDataRead)
  + [JSON representation](#BigQueryAuditMetadata.ModelDataRead.SCHEMA_REPRESENTATION)
* [BigQueryAuditMetadata.RoutineCreation](#BigQueryAuditMetadata.RoutineCreation)
  + [JSON representation](#BigQueryAuditMetadata.RoutineCreation.SCHEMA_REPRESENTATION)
* [BigQueryAuditMetadata.Routine](#BigQueryAuditMetadata.Routine)
  + [JSON representation](#BigQueryAuditMetadata.Routine.SCHEMA_REPRESENTATION)
* [BigQueryAuditMetadata.RoutineChange](#BigQueryAuditMetadata.RoutineChange)
  + [JSON representation](#BigQueryAuditMetadata.RoutineChange.SCHEMA_REPRESENTATION)
* [BigQueryAuditMetadata.RoutineDeletion](#BigQueryAuditMetadata.RoutineDeletion)
  + [JSON representation](#BigQueryAuditMetadata.RoutineDeletion.SCHEMA_REPRESENTATION)
* [BigQueryAuditMetadata.RowAccessPolicyCreation](#BigQueryAuditMetadata.RowAccessPolicyCreation)
  + [JSON representation](#BigQueryAuditMetadata.RowAccessPolicyCreation.SCHEMA_REPRESENTATION)
* [BigQueryAuditMetadata.RowAccessPolicy](#BigQueryAuditMetadata.RowAccessPolicy)
  + [JSON representation](#BigQueryAuditMetadata.RowAccessPolicy.SCHEMA_REPRESENTATION)
* [BigQueryAuditMetadata.RowAccessPolicyChange](#BigQueryAuditMetadata.RowAccessPolicyChange)
  + [JSON representation](#BigQueryAuditMetadata.RowAccessPolicyChange.SCHEMA_REPRESENTATION)
* [BigQueryAuditMetadata.RowAccessPolicyDeletion](#BigQueryAuditMetadata.RowAccessPolicyDeletion)
  + [JSON representation](#BigQueryAuditMetadata.RowAccessPolicyDeletion.SCHEMA_REPRESENTATION)
* [BigQueryAuditMetadata.UnlinkDataset](#BigQueryAuditMetadata.UnlinkDataset)
  + [JSON representation](#BigQueryAuditMetadata.UnlinkDataset.SCHEMA_REPRESENTATION)
* [BigQueryAuditMetadata.SearchIndexCreation](#BigQueryAuditMetadata.SearchIndexCreation)
  + [JSON representation](#BigQueryAuditMetadata.SearchIndexCreation.SCHEMA_REPRESENTATION)
* [BigQueryAuditMetadata.SearchIndex](#BigQueryAuditMetadata.SearchIndex)
  + [JSON representation](#BigQueryAuditMetadata.SearchIndex.SCHEMA_REPRESENTATION)
* [BigQueryAuditMetadata.SearchIndexChange](#BigQueryAuditMetadata.SearchIndexChange)
  + [JSON representation](#BigQueryAuditMetadata.SearchIndexChange.SCHEMA_REPRESENTATION)
* [BigQueryAuditMetadata.SearchIndexDeletion](#BigQueryAuditMetadata.SearchIndexDeletion)
  + [JSON representation](#BigQueryAuditMetadata.SearchIndexDeletion.SCHEMA_REPRESENTATION)
* [BigQueryAuditMetadata.VectorIndexCreation](#BigQueryAuditMetadata.VectorIndexCreation)
  + [JSON representation](#BigQueryAuditMetadata.VectorIndexCreation.SCHEMA_REPRESENTATION)
* [BigQueryAuditMetadata.VectorIndex](#BigQueryAuditMetadata.VectorIndex)
  + [JSON representation](#BigQueryAuditMetadata.VectorIndex.SCHEMA_REPRESENTATION)
* [BigQueryAuditMetadata.VectorIndexChange](#BigQueryAuditMetadata.VectorIndexChange)
  + [JSON representation](#BigQueryAuditMetadata.VectorIndexChange.SCHEMA_REPRESENTATION)
* [BigQueryAuditMetadata.VectorIndexDeletion](#BigQueryAuditMetadata.VectorIndexDeletion)
  + [JSON representation](#BigQueryAuditMetadata.VectorIndexDeletion.SCHEMA_REPRESENTATION)
* [BigQueryAuditMetadata.ConnectionChange](#BigQueryAuditMetadata.ConnectionChange)
  + [JSON representation](#BigQueryAuditMetadata.ConnectionChange.SCHEMA_REPRESENTATION)
* [BigQueryAuditMetadata.AnalyticsHubSubscribeListing](#BigQueryAuditMetadata.AnalyticsHubSubscribeListing)
  + [JSON representation](#BigQueryAuditMetadata.AnalyticsHubSubscribeListing.SCHEMA_REPRESENTATION)
* [BigQueryAuditMetadata.FirstPartyAppMetadata](#BigQueryAuditMetadata.FirstPartyAppMetadata)
  + [JSON representation](#BigQueryAuditMetadata.FirstPartyAppMetadata.SCHEMA_REPRESENTATION)
* [BigQueryAuditMetadata.SheetsMetadata](#BigQueryAuditMetadata.SheetsMetadata)
  + [JSON representation](#BigQueryAuditMetadata.SheetsMetadata.SCHEMA_REPRESENTATION)

BigQueryAuditMetaData is exposed as part of the new AuditData.metadata messages.

| JSON representation |
| --- |
| ``` {   "firstPartyAppMetadata": {     object (BigQueryAuditMetadata.FirstPartyAppMetadata)   },    // Union field event can be only one of the following:   "jobInsertion": {     object (BigQueryAuditMetadata.JobInsertion)   },   "jobChange": {     object (BigQueryAuditMetadata.JobChange)   },   "jobDeletion": {     object (BigQueryAuditMetadata.JobDeletion)   },   "datasetCreation": {     object (BigQueryAuditMetadata.DatasetCreation)   },   "datasetChange": {     object (BigQueryAuditMetadata.DatasetChange)   },   "datasetDeletion": {     object (BigQueryAuditMetadata.DatasetDeletion)   },   "tableCreation": {     object (BigQueryAuditMetadata.TableCreation)   },   "tableChange": {     object (BigQueryAuditMetadata.TableChange)   },   "tableDeletion": {     object (BigQueryAuditMetadata.TableDeletion)   },   "tableDataRead": {     object (BigQueryAuditMetadata.TableDataRead)   },   "tableDataChange": {     object (BigQueryAuditMetadata.TableDataChange)   },   "modelDeletion": {     object (BigQueryAuditMetadata.ModelDeletion)   },   "modelCreation": {     object (BigQueryAuditMetadata.ModelCreation)   },   "modelMetadataChange": {     object (BigQueryAuditMetadata.ModelMetadataChange)   },   "modelDataChange": {     object (BigQueryAuditMetadata.ModelDataChange)   },   "modelDataRead": {     object (BigQueryAuditMetadata.ModelDataRead)   },   "routineCreation": {     object (BigQueryAuditMetadata.RoutineCreation)   },   "routineChange": {     object (BigQueryAuditMetadata.RoutineChange)   },   "routineDeletion": {     object (BigQueryAuditMetadata.RoutineDeletion)   },   "rowAccessPolicyCreation": {     object (BigQueryAuditMetadata.RowAccessPolicyCreation)   },   "rowAccessPolicyChange": {     object (BigQueryAuditMetadata.RowAccessPolicyChange)   },   "rowAccessPolicyDeletion": {     object (BigQueryAuditMetadata.RowAccessPolicyDeletion)   },   "unlinkDataset": {     object (BigQueryAuditMetadata.UnlinkDataset)   },   "searchIndexCreation": {     object (BigQueryAuditMetadata.SearchIndexCreation)   },   "searchIndexChange": {     object (BigQueryAuditMetadata.SearchIndexChange)   },   "searchIndexDeletion": {     object (BigQueryAuditMetadata.SearchIndexDeletion)   },   "vectorIndexCreation": {     object (BigQueryAuditMetadata.VectorIndexCreation)   },   "vectorIndexChange": {     object (BigQueryAuditMetadata.VectorIndexChange)   },   "vectorIndexDeletion": {     object (BigQueryAuditMetadata.VectorIndexDeletion)   },   "connectionChange": {     object (BigQueryAuditMetadata.ConnectionChange)   },   "analyticsHubSubscribeListing": {     object (BigQueryAuditMetadata.AnalyticsHubSubscribeListing)   }   // End of list of possible types for union field event. } ``` |

| Fields | |
| --- | --- |
| `firstPartyAppMetadata` | `object (BigQueryAuditMetadata.FirstPartyAppMetadata)`  First party (Google) application specific metadata. |
| Union field `event`. BigQuery event information. `event` can be only one of the following: | |
| `jobInsertion` | `object (BigQueryAuditMetadata.JobInsertion)`  Job insertion event. |
| `jobChange` | `object (BigQueryAuditMetadata.JobChange)`  Job state change event. |
| `jobDeletion` | `object (BigQueryAuditMetadata.JobDeletion)`  Job deletion event. |
| `datasetCreation` | `object (BigQueryAuditMetadata.DatasetCreation)`  Dataset creation event. |
| `datasetChange` | `object (BigQueryAuditMetadata.DatasetChange)`  Dataset change event. |
| `datasetDeletion` | `object (BigQueryAuditMetadata.DatasetDeletion)`  Dataset deletion event. |
| `tableCreation` | `object (BigQueryAuditMetadata.TableCreation)`  Table creation event. |
| `tableChange` | `object (BigQueryAuditMetadata.TableChange)`  Table metadata change event. |
| `tableDeletion` | `object (BigQueryAuditMetadata.TableDeletion)`  Table deletion event. |
| `tableDataRead` | `object (BigQueryAuditMetadata.TableDataRead)`  Table data read event. |
| `tableDataChange` | `object (BigQueryAuditMetadata.TableDataChange)`  Table data change event. |
| `modelDeletion` | `object (BigQueryAuditMetadata.ModelDeletion)`  Model deletion event. |
| `modelCreation` | `object (BigQueryAuditMetadata.ModelCreation)`  Model creation event. |
| `modelMetadataChange` | `object (BigQueryAuditMetadata.ModelMetadataChange)`  Model metadata change event. |
| `modelDataChange` | `object (BigQueryAuditMetadata.ModelDataChange)`  Model data change event. |
| `modelDataRead` | `object (BigQueryAuditMetadata.ModelDataRead)`  Model data read event. |
| `routineCreation` | `object (BigQueryAuditMetadata.RoutineCreation)`  Routine creation event. |
| `routineChange` | `object (BigQueryAuditMetadata.RoutineChange)`  Routine change event. |
| `routineDeletion` | `object (BigQueryAuditMetadata.RoutineDeletion)`  Routine deletion event. |
| `rowAccessPolicyCreation` | `object (BigQueryAuditMetadata.RowAccessPolicyCreation)`  Row access policy create event. |
| `rowAccessPolicyChange` | `object (BigQueryAuditMetadata.RowAccessPolicyChange)`  Row access policy change event. |
| `rowAccessPolicyDeletion` | `object (BigQueryAuditMetadata.RowAccessPolicyDeletion)`  Row access policy deletion event. |
| `unlinkDataset` | `object (BigQueryAuditMetadata.UnlinkDataset)`  Unlink linked dataset from its source dataset event |
| `searchIndexCreation` | `object (BigQueryAuditMetadata.SearchIndexCreation)`  Search index creation event. |
| `searchIndexChange` | `object (BigQueryAuditMetadata.SearchIndexChange)`  Search index change event. |
| `searchIndexDeletion` | `object (BigQueryAuditMetadata.SearchIndexDeletion)`  Search index deletion event. |
| `vectorIndexCreation` | `object (BigQueryAuditMetadata.VectorIndexCreation)`  Vector index creation event. |
| `vectorIndexChange` | `object (BigQueryAuditMetadata.VectorIndexChange)`  Vector index change event. |
| `vectorIndexDeletion` | `object (BigQueryAuditMetadata.VectorIndexDeletion)`  Vector index deletion event. |
| `connectionChange` | `object (BigQueryAuditMetadata.ConnectionChange)`  Connection change event. |
| `analyticsHubSubscribeListing` | `object (BigQueryAuditMetadata.AnalyticsHubSubscribeListing)`  Subscribe listing event. |

## BigQueryAuditMetadata.JobInsertion

Job insertion event.

| JSON representation |
| --- |
| ``` {   "job": {     object (BigQueryAuditMetadata.Job)   },   "reason": enum (BigQueryAuditMetadata.JobInsertion.Reason) } ``` |

| Fields | |
| --- | --- |
| `job` | `object (BigQueryAuditMetadata.Job)`  Job metadata. |
| `reason` | `enum (BigQueryAuditMetadata.JobInsertion.Reason)`  Describes how the job was inserted. |

## BigQueryAuditMetadata.Job

BigQuery job.

| JSON representation |
| --- |
| ``` {   "jobName": string,   "jobConfig": {     object (BigQueryAuditMetadata.JobConfig)   },   "jobStatus": {     object (BigQueryAuditMetadata.JobStatus)   },   "jobStats": {     object (BigQueryAuditMetadata.JobStats)   } } ``` |

| Fields | |
| --- | --- |
| `jobName` | `string`  Job URI.  Format: `projects/<projectId>/jobs/<jobId>`. |
| `jobConfig` | `object (BigQueryAuditMetadata.JobConfig)`  Job configuration. |
| `jobStatus` | `object (BigQueryAuditMetadata.JobStatus)`  Job status. |
| `jobStats` | `object (BigQueryAuditMetadata.JobStats)`  Job statistics. |

## BigQueryAuditMetadata.JobConfig

Job configuration. See the [Jobs](https://cloud.google.com/bigquery/docs/reference/v2/jobs) API resource for more details on individual fields.

| JSON representation |
| --- |
| ``` {   "type": enum (BigQueryAuditMetadata.JobConfig.Type),   "labels": {     string: string,     ...   },   "reservation": string,    // Union field config can be only one of the following:   "queryConfig": {     object (BigQueryAuditMetadata.JobConfig.Query)   },   "loadConfig": {     object (BigQueryAuditMetadata.JobConfig.Load)   },   "extractConfig": {     object (BigQueryAuditMetadata.JobConfig.Extract)   },   "tableCopyConfig": {     object (BigQueryAuditMetadata.JobConfig.TableCopy)   }   // End of list of possible types for union field config. } ``` |

| Fields | |
| --- | --- |
| `type` | `enum (BigQueryAuditMetadata.JobConfig.Type)`  Job type. |
| `labels` | `map (key: string, value: string)`  Labels provided for the job.  An object containing a list of `"key": value` pairs. Example: `{ "name": "wrench", "mass": "1.3kg", "count": "3" }`. |
| `reservation` | `string`  User specified reservation for the job. |
| Union field `config`. Job configuration information. `config` can be only one of the following: | |
| `queryConfig` | `object (BigQueryAuditMetadata.JobConfig.Query)`  Query job information. |
| `loadConfig` | `object (BigQueryAuditMetadata.JobConfig.Load)`  Load job information. |
| `extractConfig` | `object (BigQueryAuditMetadata.JobConfig.Extract)`  Extract job information. |
| `tableCopyConfig` | `object (BigQueryAuditMetadata.JobConfig.TableCopy)`  TableCopy job information. |

## BigQueryAuditMetadata.JobConfig.Query

Query job configuration.

| JSON representation |
| --- |
| ``` {   "query": string,   "queryTruncated": boolean,   "destinationTable": string,   "createDisposition": enum (BigQueryAuditMetadata.CreateDisposition),   "writeDisposition": enum (BigQueryAuditMetadata.WriteDisposition),   "defaultDataset": string,   "tableDefinitions": [     {       object (BigQueryAuditMetadata.TableDefinition)     }   ],   "priority": enum (BigQueryAuditMetadata.JobConfig.Query.Priority),   "destinationTableEncryption": {     object ( ``` |