* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback

# REST Resource: tables Stay organized with collections Save and categorize content based on your preferences.

* [Resource: Table](#Table)
  + [JSON representation](#Table.SCHEMA_REPRESENTATION)
* [TableSchema](#TableSchema)
  + [JSON representation](#TableSchema.SCHEMA_REPRESENTATION)
* [TableFieldSchema](#TableFieldSchema)
  + [JSON representation](#TableFieldSchema.SCHEMA_REPRESENTATION)
* [DataPolicyOption](#DataPolicyOption)
  + [JSON representation](#DataPolicyOption.SCHEMA_REPRESENTATION)
* [DataPolicyList](#DataPolicyList)
  + [JSON representation](#DataPolicyList.SCHEMA_REPRESENTATION)
* [FieldElementType](#FieldElementType)
  + [JSON representation](#FieldElementType.SCHEMA_REPRESENTATION)
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
* [ViewDefinition](#ViewDefinition)
  + [JSON representation](#ViewDefinition.SCHEMA_REPRESENTATION)
* [UserDefinedFunctionResource](#UserDefinedFunctionResource)
  + [JSON representation](#UserDefinedFunctionResource.SCHEMA_REPRESENTATION)
* [PrivacyPolicy](#PrivacyPolicy)
  + [JSON representation](#PrivacyPolicy.SCHEMA_REPRESENTATION)
* [AggregationThresholdPolicy](#AggregationThresholdPolicy)
  + [JSON representation](#AggregationThresholdPolicy.SCHEMA_REPRESENTATION)
* [MaterializedViewDefinition](#MaterializedViewDefinition)
  + [JSON representation](#MaterializedViewDefinition.SCHEMA_REPRESENTATION)
* [MaterializedViewStatus](#MaterializedViewStatus)
  + [JSON representation](#MaterializedViewStatus.SCHEMA_REPRESENTATION)
* [ErrorProto](#ErrorProto)
  + [JSON representation](#ErrorProto.SCHEMA_REPRESENTATION)
* [ExternalDataConfiguration](#ExternalDataConfiguration)
  + [JSON representation](#ExternalDataConfiguration.SCHEMA_REPRESENTATION)
* [FileSetSpecType](#FileSetSpecType)
* [CsvOptions](#CsvOptions)
  + [JSON representation](#CsvOptions.SCHEMA_REPRESENTATION)
* [JsonOptions](#JsonOptions)
  + [JSON representation](#JsonOptions.SCHEMA_REPRESENTATION)
* [BigtableOptions](#BigtableOptions)
  + [JSON representation](#BigtableOptions.SCHEMA_REPRESENTATION)
* [BigtableColumnFamily](#BigtableColumnFamily)
  + [JSON representation](#BigtableColumnFamily.SCHEMA_REPRESENTATION)
* [BigtableColumn](#BigtableColumn)
  + [JSON representation](#BigtableColumn.SCHEMA_REPRESENTATION)
* [BigtableProtoConfig](#BigtableProtoConfig)
  + [JSON representation](#BigtableProtoConfig.SCHEMA_REPRESENTATION)
* [GoogleSheetsOptions](#GoogleSheetsOptions)
  + [JSON representation](#GoogleSheetsOptions.SCHEMA_REPRESENTATION)
* [HivePartitioningOptions](#HivePartitioningOptions)
  + [JSON representation](#HivePartitioningOptions.SCHEMA_REPRESENTATION)
* [DecimalTargetType](#DecimalTargetType)
* [AvroOptions](#AvroOptions)
  + [JSON representation](#AvroOptions.SCHEMA_REPRESENTATION)
* [JsonExtension](#JsonExtension)
* [ParquetOptions](#ParquetOptions)
  + [JSON representation](#ParquetOptions.SCHEMA_REPRESENTATION)
* [MapTargetType](#MapTargetType)
* [ObjectMetadata](#ObjectMetadata)
* [MetadataCacheMode](#MetadataCacheMode)
* [BigLakeConfiguration](#BigLakeConfiguration)
  + [JSON representation](#BigLakeConfiguration.SCHEMA_REPRESENTATION)
* [FileFormat](#FileFormat)
* [TableFormat](#TableFormat)
* [Streamingbuffer](#Streamingbuffer)
  + [JSON representation](#Streamingbuffer.SCHEMA_REPRESENTATION)
* [SnapshotDefinition](#SnapshotDefinition)
  + [JSON representation](#SnapshotDefinition.SCHEMA_REPRESENTATION)
* [CloneDefinition](#CloneDefinition)
  + [JSON representation](#CloneDefinition.SCHEMA_REPRESENTATION)
* [TableConstraints](#TableConstraints)
  + [JSON representation](#TableConstraints.SCHEMA_REPRESENTATION)
* [PrimaryKey](#PrimaryKey)
  + [JSON representation](#PrimaryKey.SCHEMA_REPRESENTATION)
* [ForeignKey](#ForeignKey)
  + [JSON representation](#ForeignKey.SCHEMA_REPRESENTATION)
* [ColumnReference](#ColumnReference)
  + [JSON representation](#ColumnReference.SCHEMA_REPRESENTATION)
* [ExternalCatalogTableOptions](#ExternalCatalogTableOptions)
  + [JSON representation](#ExternalCatalogTableOptions.SCHEMA_REPRESENTATION)
* [StorageDescriptor](#StorageDescriptor)
  + [JSON representation](#StorageDescriptor.SCHEMA_REPRESENTATION)
* [SerDeInfo](#SerDeInfo)
  + [JSON representation](#SerDeInfo.SCHEMA_REPRESENTATION)
* [Methods](#METHODS_SUMMARY)

## Resource: Table

| JSON representation |
| --- |
| ``` {   "kind": string,   "etag": string,   "id": string,   "selfLink": string,   "tableReference": {     object (TableReference)   },   "friendlyName": string,   "description": string,   "labels": {     string: string,     ...   },   "schema": {     object (TableSchema)   },   "timePartitioning": {     object (TimePartitioning)   },   "rangePartitioning": {     object (RangePartitioning)   },   "clustering": {     object (Clustering)   },   "requirePartitionFilter": boolean,   "numBytes": string,   "numLongTermBytes": string,   "numRows": string,   "creationTime": string,   "expirationTime": string,   "lastModifiedTime": string,   "type": string,   "view": {     object (ViewDefinition)   },   "materializedView": {     object (MaterializedViewDefinition)   },   "materializedViewStatus": {     object (MaterializedViewStatus)   },   "externalDataConfiguration": {     object (ExternalDataConfiguration)   },   "biglakeConfiguration": {     object (BigLakeConfiguration)   },   "location": string,   "streamingBuffer": {     object (Streamingbuffer)   },   "encryptionConfiguration": {     object (EncryptionConfiguration)   },   "snapshotDefinition": {     object (SnapshotDefinition)   },   "defaultCollation": string,   "defaultRoundingMode": enum (RoundingMode),   "cloneDefinition": {     object (CloneDefinition)   },   "numTimeTravelPhysicalBytes": string,   "numTotalLogicalBytes": string,   "numActiveLogicalBytes": string,   "numLongTermLogicalBytes": string,   "numTotalPhysicalBytes": string,   "numActivePhysicalBytes": string,   "numLongTermPhysicalBytes": string,   "numPartitions": string,   "maxStaleness": string,   "tableConstraints": {     object (TableConstraints)   },   "resourceTags": {     string: string,     ...   },   "replicas": [     {       object (TableReference)     }   ],   "externalCatalogTableOptions": {     object (ExternalCatalogTableOptions)   },   "partitionDefinition": {     object (PartitioningDefinition)   } } ``` |

| Fields | |
| --- | --- |
| `kind` | `string`  The type of resource ID. |
| `etag` | `string`  Output only. A hash of this resource. |
| `id` | `string`  Output only. An opaque ID uniquely identifying the table. |
| `selfLink` | `string`  Output only. A URL that can be used to access this resource again. |
| `tableReference` | `object (TableReference)`  Required. Reference describing the ID of this table. |
| `friendlyName` | `string`  Optional. A descriptive name for this table. |
| `description` | `string`  Optional. A user-friendly description of this table. |
| `labels` | `map (key: string, value: string)`  The labels associated with this table. You can use these to organize and group your tables. Label keys and values can be no longer than 63 characters, can only contain lowercase letters, numeric characters, underscores and dashes. International characters are allowed. Label values are optional. Label keys must start with a letter and each label in the list must have a different key. |
| `schema` | `object (TableSchema)`  Optional. Describes the schema of this table. |
| `timePartitioning` | `object (TimePartitioning)`  If specified, configures time-based partitioning for this table. |
| `rangePartitioning` | `object (RangePartitioning)`  If specified, configures range partitioning for this table. |
| `clustering` | `object (Clustering)`  Clustering specification for the table. Must be specified with time-based partitioning, data in the table will be first partitioned and subsequently clustered. |
| `requirePartitionFilter` | `boolean`  Optional. If set to true, queries over this table require a partition filter that can be used for partition elimination to be specified. |
| `numBytes` | `string (Int64Value format)`  Output only. The size of this table in logical bytes, excluding any data in the streaming buffer. |
| `numLongTermBytes` | `string (Int64Value format)`  Output only. The number of logical bytes in the table that are considered "long-term storage". |
| `numRows` | `string (UInt64Value format)`  Output only. The number of rows of data in this table, excluding any data in the streaming buffer. |
| `creationTime` | `string (int64 format)`  Output only. The time when this table was created, in milliseconds since the epoch. |
| `expirationTime` | `string (Int64Value format)`  Optional. The time when this table expires, in milliseconds since the epoch. If not present, the table will persist indefinitely. Expired tables will be deleted and their storage reclaimed. The defaultTableExpirationMs property of the encapsulating dataset can be used to set a default expirationTime on newly created tables. |
| `lastModifiedTime` | `string (uint64 format)`  Output only. The time when this table was last modified, in milliseconds since the epoch. |
| `type` | `string`  Output only. Describes the table type. The following values are supported:   * `TABLE`: A normal BigQuery table. * `VIEW`: A virtual table defined by a SQL query. * `EXTERNAL`: A table that references data stored in an external storage system, such as Google Cloud Storage. * `MATERIALIZED_VIEW`: A precomputed view defined by a SQL query. * `SNAPSHOT`: An immutable BigQuery table that preserves the contents of a base table at a particular time. See additional information on [table snapshots](https://cloud.google.com/bigquery/docs/table-snapshots-intro).   The default value is `TABLE`. |
| `view` | `object (ViewDefinition)`  Optional. The view definition. |
| `materializedView` | `object (MaterializedViewDefinition)`  Optional. The materialized view definition. |
| `materializedViewStatus` | `object (MaterializedViewStatus)`  Output only. The materialized view status. |
| `externalDataConfiguration` | `object (ExternalDataConfiguration)`  Optional. Describes the data format, location, and other properties of a table stored outside of BigQuery. By defining these properties, the data source can then be queried as if it were a standard BigQuery table. |
| `biglakeConfiguration` | `object (BigLakeConfiguration)`  Optional. Specifies the configuration of a BigQuery table for Apache Iceberg. |
| `location` | `string`  Output only. The geographic location where the table resides. This value is inherited from the dataset. |
| `streamingBuffer` | `object (Streamingbuffer)`  Output only. Contains information regarding this table's streaming buffer, if one is present. This field will be absent if the table is not being streamed to or if there is no data in the streaming buffer. |
| `encryptionConfiguration` | `object (EncryptionConfiguration)`  Custom encryption configuration (e.g., Cloud KMS keys). |
| `snapshotDefinition` | `object (SnapshotDefinition)`  Output only. Contains information about the snapshot. This value is set via snapshot creation. |
| `defaultCollation` | `string`  Optional. Defines the default collation specification of new STRING fields in the table. During table creation or update, if a STRING field is added to this table without explicit collation specified, then the table inherits the table default collation. A change to this field affects only fields added afterwards, and does not alter the existing fields. The following values are supported:   * 'und:ci': undetermined locale, case insensitive. * '': empty string. Default to case-sensitive behavior. |
| `defaultRoundingMode` | `enum (RoundingMode)`  Optional. Defines the default rounding mode specification of new decimal fields (NUMERIC OR BIGNUMERIC) in the table. During table creation or update, if a decimal field is added to this table without an explicit rounding mode specified, then the field inherits the table default rounding mode. Changing this field doesn't affect existing fields. |
| `cloneDefinition` | `object (CloneDefinition)`  Output only. Contains information about the clone. This value is set via the clone operation. |
| `numTimeTravelPhysicalBytes` | `string (Int64Value format)`  Output only. Number of physical bytes used by time travel storage (deleted or changed data). This data is not kept in real time, and might be delayed by a few seconds to a few minutes. |
| `numTotalLogicalBytes` | `string (Int64Value format)`  Output only. Total number of logical bytes in the table or materialized view. |
| `numActiveLogicalBytes` | `string (Int64Value format)`  Output only. Number of logical bytes that are less than 90 days old. |
| `numLongTermLogicalBytes` | `string (Int64Value format)`  Output only. Number of logical bytes that are more than 90 days old. |
| `numTotalPhysicalBytes` | `string (Int64Value format)`  Output only. The physical size of this table in bytes. This also includes storage used for time travel. This data is not kept in real time, and might be delayed by a few seconds to a few minutes. |
| `numActivePhysicalBytes` | `string (Int64Value format)`  Output only. Number of physical bytes less than 90 days old. This data is not kept in real time, and might be delayed by a few seconds to a few minutes. |
| `numLongTermPhysicalBytes` | `string (Int64Value format)`  Output only. Number of physical bytes more than 90 days old. This data is not kept in real time, and might be delayed by a few seconds to a few minutes. |
| `numPartitions` | `string (Int64Value format)`  Output only. The number of partitions present in the table or materialized view. This data is not kept in real time, and might be delayed by a few seconds to a few minutes. |
| `maxStaleness` | `string`  Optional. The maximum staleness of data that could be returned when the table (or stale MV) is queried. Staleness encoded as a string encoding of sql IntervalValue type. |
| `tableConstraints` | `object (TableConstraints)`  Optional. Tables Primary Key and Foreign Key information |
| `resourceTags` | `map (key: string, value: string)`  Optional. The [tags](https://cloud.google.com/bigquery/docs/tags) attached to this table. Tag keys are globally unique. Tag key is expected to be in the namespaced format, for example "123456789012/environment" where 123456789012 is the ID of the parent organization or project resource for this tag key. Tag value is expected to be the short name, for example "Production". See [Tag definitions](https://cloud.google.com/iam/docs/tags-access-control#definitions) for more details. |
| `replicas[]` | `object (TableReference)`  Optional. Output only. Table references of all replicas currently active on the table. |
| `externalCatalogTableOptions` | `object (ExternalCatalogTableOptions)`  Optional. Options defining open source compatible table. |
| `partitionDefinition` | `object (PartitioningDefinition)`  Optional. The partition information for all table formats, including managed partitioned tables, hive partitioned tables, iceberg partitioned, and metastore partitioned tables. This field is only populated for metastore partitioned tables. For other table formats, this is an output only field. |

## TableSchema

Schema of a table

| JSON representation |
| --- |
| ``` {   "fields": [     {       object (TableFieldSchema)     }   ] } ``` |

| Fields | |
| --- | --- |
| `fields[]` | `object (TableFieldSchema)`  Describes the fields in a table. |

## TableFieldSchema

A field in TableSchema

| JSON representation |
| --- |
| ``` {   "name": string,   "type": string,   "mode": string,   "fields": [     {       object (TableFieldSchema)     }   ],   "description": string,   "policyTags": {     "names": [       string     ]   },   "dataPolicies": [     {       object (DataPolicyOption)     }   ],   "dataPolicyList": {     object (DataPolicyList)   },   "maxLength": string,   "precision": string,   "scale": string,   "roundingMode": enum (RoundingMode),   "collation": string,   "defaultValueExpression": string,   "rangeElementType": {     object (FieldElementType)   } } ``` |

| Fields | |
| --- | --- |
| `name` | `string`  Required. The field name. The name must contain only letters (a-z, A-Z), numbers (0-9), or underscores (\_), and must start with a letter or underscore. The maximum length is 300 characters. |
| `type` | `string`  Required. The field data type. Possible values include:   * STRING * BYTES * INTEGER (or INT64) * FLOAT (or FLOAT64) * BOOLEAN (or BOOL) * TIMESTAMP * DATE * TIME * DATETIME * GEOGRAPHY * NUMERIC * BIGNUMERIC * JSON * RECORD (or STRUCT) * RANGE   Use of RECORD/STRUCT indicates that the field contains a nested schema. |
| `mode` | `string`  Optional. The field mode. Possible values include NULLABLE, REQUIRED and REPEATED. The default value is NULLABLE. |
| `fields[]` | `object (TableFieldSchema)`  Optional. Describes the nested schema fields if the type property is set to RECORD. |
| `description` | `string`  Optional. The field description. The maximum length is 1,024 characters. |
| `policyTags` | `object`  Optional. The policy tags attached to this field, used for field-level access control. If not set, defaults to empty policyTags. |
| `policyTags.names[]` | `string`  A list of policy tag resource names. For example, "projects/1/locations/eu/taxonomies/2/policyTags/3". At most 1 policy tag is currently allowed. |
| `dataPolicies[]` | `object (DataPolicyOption)`  Optional. Data policies attached to this field, used for field-level access control. |
| `dataPolicyList` | `object (DataPolicyList)`  Optional. Specifies data policies attached to this field, used for field-level access control. When set, this will be the source of truth for data policy information. |
| `maxLength` | `string (int64 format)`  Optional. Maximum length of values of this field for STRINGS or BYTES.  If maxLength is not specified, no maximum length constraint is imposed on this field.  If type = "STRING", then maxLength represents the maximum UTF-8 length of strings in this field.  If type = "BYTES", then maxLength represents the maximum number of bytes in this field.  It is invalid to set this field if type ≠ "STRING" and ≠ "BYTES". |
| `precision` | `string (int64 format)`  Optional. Precision (maximum number of total digits in base 10) and scale (maximum number of digits in the fractional part in base 10) constraints for values of this field for NUMERIC or BIGNUMERIC.  It is invalid to set precision or scale if type ≠ "NUMERIC" and ≠ "BIGNUMERIC".  If precision and scale are not specified, no value range constraint is imposed on this field insofar as values are permitted by the type.  Values of this NUMERIC or BIGNUMERIC field must be in this range when:   * Precision (P) and scale (S) are specified: [-10P-S + 10-S, 10P-S - 10-S] * Precision (P) is specified but not scale (and thus scale is interpreted to be equal to zero): [-10P + 1, 10P - 1].   Acceptable values for precision and scale if both are specified:   * If type = "NUMERIC": 1 ≤ precision - scale ≤ 29 and 0 ≤ scale ≤ 9. * If type = "BIGNUMERIC": 1 ≤ precision - scale ≤ 38 and 0 ≤ scale ≤ 38.   Acceptable values for precision if only precision is specified but not scale (and thus scale is interpreted to be equal to zero):   * If type = "NUMERIC": 1 ≤ precision ≤ 29. * If type = "BIGNUMERIC": 1 ≤ precision ≤ 38.   If scale is specified but not precision, then it is invalid. |
| `scale` | `string (int64 format)`  Optional. See documentation for precision. |
| `roundingMode` | `enum (RoundingMode)`  Optional. Specifies the rounding mode to be used when storing values of NUMERIC and BIGNUMERIC type. |
| `collation` | `string`  Optional. Field collation can be set only when the type of field is STRING. The following values are supported:   * 'und:ci': undetermined locale, case insensitive. * '': empty string. Default to case-sensitive behavior. |
| `defaultValueExpression` | `string`  Optional. A SQL expression to specify the [default value](https://cloud.google.com/bigquery/docs/default-values) for this field. |
| `rangeElementType` | `object (FieldElementType)`  Optional. The subtype of the RANGE, if the type of this field is RANGE. If the type is RANGE, this field is required. Values for the field element type can be the following:   * DATE * DATETIME * TIMESTAMP |

## DataPolicyOption

Data policy option. For more information, see [Mask data by applying data policies to a column](https://docs.cloud.google.com/bigquery/docs/column-data-masking#data-policies-on-column).

| JSON representation |
| --- |
| ``` {   "name": string } ``` |

| Fields | |
| --- | --- |
| `name` | `string`  Data policy resource name in the form of projects/projectId/locations/locationId/dataPolicies/data\_policy\_id. |

## DataPolicyList

A list of data policy options. For more information, see [Mask data by applying data policies to a column](https://docs.cloud.google.com/bigquery/docs/column-data-masking#data-policies-on-column).

| JSON representation |
| --- |
| ``` {   "dataPolicies": [     {       object (DataPolicyOption)     }   ] } ``` |

| Fields | |
| --- | --- |
| `dataPolicies[]` | `object (DataPolicyOption)`  Contains a list of data policy options. At most 9 data policies are allowed per field. |

## FieldElementType

Represents the type of a field element.

| JSON representation |
| --- |
| ``` {   "type": string } ``` |

| Fields | |
| --- | --- |
| `type` | `string`  Required. The type of a field element. For more information, see `TableFieldSchema.type`. |

## TimePartitioning

| JSON representation |
| --- |
|  |