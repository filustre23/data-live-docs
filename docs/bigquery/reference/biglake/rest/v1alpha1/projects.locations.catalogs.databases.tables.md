As of April 20th, 2026, BigLake is now called Google Cloud Lakehouse. BigLake metastore is now called the Lakehouse runtime catalog. Lakehouse APIs, client libraries, CLI commands, and IAM names remain unchanged and still reference BigLake.

* [Home](https://docs.cloud.google.com/)
* [BigLake API](https://docs.cloud.google.com/lakehouse/docs)
* [Technology areas](https://docs.cloud.google.com/docs)
* [Reference](https://docs.cloud.google.com/lakehouse/docs/quotas)

# REST Resource: projects.locations.catalogs.databases.tables Stay organized with collections Save and categorize content based on your preferences.

* [Resource: Table](#Table)
  + [JSON representation](#Table.SCHEMA_REPRESENTATION)
* [HiveTableOptions](#HiveTableOptions)
  + [JSON representation](#HiveTableOptions.SCHEMA_REPRESENTATION)
* [StorageDescriptor](#StorageDescriptor)
  + [JSON representation](#StorageDescriptor.SCHEMA_REPRESENTATION)
* [SerDeInfo](#SerDeInfo)
  + [JSON representation](#SerDeInfo.SCHEMA_REPRESENTATION)
* [Type](#Type)
* [Methods](#METHODS_SUMMARY)

## Resource: Table

Represents a table.

| JSON representation |
| --- |
| ``` {   "name": string,   "createTime": string,   "updateTime": string,   "deleteTime": string,   "expireTime": string,   "type": enum (Type),   "etag": string,    // Union field options can be only one of the following:   "hiveOptions": {     object (HiveTableOptions)   }   // End of list of possible types for union field options. } ``` |

| Fields | |
| --- | --- |
| `name` | `string`  Output only. The resource name. Format: projects/{project\_id\_or\_number}/locations/{locationId}/catalogs/{catalogId}/databases/{databaseId}/tables/{tableId} |
| `createTime` | `string (Timestamp format)`  Output only. The creation time of the table.  Uses RFC 3339, where generated output will always be Z-normalized and use 0, 3, 6 or 9 fractional digits. Offsets other than "Z" are also accepted. Examples: `"2014-10-02T15:01:23Z"`, `"2014-10-02T15:01:23.045123456Z"` or `"2014-10-02T15:01:23+05:30"`. |
| `updateTime` | `string (Timestamp format)`  Output only. The last modification time of the table.  Uses RFC 3339, where generated output will always be Z-normalized and use 0, 3, 6 or 9 fractional digits. Offsets other than "Z" are also accepted. Examples: `"2014-10-02T15:01:23Z"`, `"2014-10-02T15:01:23.045123456Z"` or `"2014-10-02T15:01:23+05:30"`. |
| `deleteTime` | `string (Timestamp format)`  Output only. The deletion time of the table. Only set after the table is deleted.  Uses RFC 3339, where generated output will always be Z-normalized and use 0, 3, 6 or 9 fractional digits. Offsets other than "Z" are also accepted. Examples: `"2014-10-02T15:01:23Z"`, `"2014-10-02T15:01:23.045123456Z"` or `"2014-10-02T15:01:23+05:30"`. |
| `expireTime` | `string (Timestamp format)`  Output only. The time when this table is considered expired. Only set after the table is deleted.  Uses RFC 3339, where generated output will always be Z-normalized and use 0, 3, 6 or 9 fractional digits. Offsets other than "Z" are also accepted. Examples: `"2014-10-02T15:01:23Z"`, `"2014-10-02T15:01:23.045123456Z"` or `"2014-10-02T15:01:23+05:30"`. |
| `type` | `enum (Type)`  The table type. |
| `etag` | `string`  The checksum of a table object computed by the server based on the value of other fields. It may be sent on update requests to ensure the client has an up-to-date value before proceeding. It is only checked for update table operations. |
| Union field `options`. Options specified for the table type. `options` can be only one of the following: | |
| `hiveOptions` | `object (HiveTableOptions)`  Options of a Hive table. |

## HiveTableOptions

Options of a Hive table.

| JSON representation |
| --- |
| ``` {   "parameters": {     string: string,     ...   },   "tableType": string,   "storageDescriptor": {     object (StorageDescriptor)   } } ``` |

| Fields | |
| --- | --- |
| `parameters` | `map (key: string, value: string)`  Stores user supplied Hive table parameters.  An object containing a list of `"key": value` pairs. Example: `{ "name": "wrench", "mass": "1.3kg", "count": "3" }`. |
| `tableType` | `string`  Hive table type. For example, MANAGED\_TABLE, EXTERNAL\_TABLE. |
| `storageDescriptor` | `object (StorageDescriptor)`  Stores physical storage information of the data. |

## StorageDescriptor

Stores physical storage information of the data.

| JSON representation |
| --- |
| ``` {   "locationUri": string,   "inputFormat": string,   "outputFormat": string,   "serdeInfo": {     object (SerDeInfo)   } } ``` |

| Fields | |
| --- | --- |
| `locationUri` | `string`  Cloud Storage folder URI where the table data is stored, starting with "gs://". |
| `inputFormat` | `string`  The fully qualified Java class name of the input format. |
| `outputFormat` | `string`  The fully qualified Java class name of the output format. |
| `serdeInfo` | `object (SerDeInfo)`  Serializer and deserializer information. |

## SerDeInfo

Serializer and deserializer information.

| JSON representation |
| --- |
| ``` {   "serializationLib": string } ``` |

| Fields | |
| --- | --- |
| `serializationLib` | `string`  The fully qualified Java class name of the serialization library. |

## Type

The table type.

| Enums | |
| --- | --- |
| `TYPE_UNSPECIFIED` | The type is not specified. |
| `HIVE` | Represents a table compatible with Hive Metastore tables. |

| Methods | |
| --- | --- |
| `create` | Creates a new table. |
| `delete` | Deletes an existing table specified by the table ID. |
| `get` | Gets the table specified by the resource name. |
| `list` | List all tables in a specified database. |
| `patch` | Updates an existing table specified by the table ID. |
| `rename` | Renames an existing table specified by the table ID. |

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2026-04-21 UTC.




[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Hard to understand","hardToUnderstand","thumb-down"],["Incorrect information or sample code","incorrectInformationOrSampleCode","thumb-down"],["Missing the information/samples I need","missingTheInformationSamplesINeed","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2026-04-21 UTC."],[],[]]