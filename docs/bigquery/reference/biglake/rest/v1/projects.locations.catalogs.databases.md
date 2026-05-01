As of April 20th, 2026, BigLake is now called Google Cloud Lakehouse. BigLake metastore is now called the Lakehouse runtime catalog. Lakehouse APIs, client libraries, CLI commands, and IAM names remain unchanged and still reference BigLake.

* [Home](https://docs.cloud.google.com/)
* [BigLake API](https://docs.cloud.google.com/lakehouse/docs)

# REST Resource: projects.locations.catalogs.databases Stay organized with collections Save and categorize content based on your preferences.

* [Resource: Database](#Database)
  + [JSON representation](#Database.SCHEMA_REPRESENTATION)
* [HiveDatabaseOptions](#HiveDatabaseOptions)
  + [JSON representation](#HiveDatabaseOptions.SCHEMA_REPRESENTATION)
* [Type](#Type)
* [Methods](#METHODS_SUMMARY)

## Resource: Database

Database is the container of tables.

| JSON representation |
| --- |
| ``` {   "name": string,   "createTime": string,   "updateTime": string,   "deleteTime": string,   "expireTime": string,   "type": enum (Type),    // Union field options can be only one of the following:   "hiveOptions": {     object (HiveDatabaseOptions)   }   // End of list of possible types for union field options. } ``` |

| Fields | |
| --- | --- |
| `name` | `string`  Output only. The resource name. Format: projects/{project\_id\_or\_number}/locations/{locationId}/catalogs/{catalogId}/databases/{databaseId} |
| `createTime` | `string (Timestamp format)`  Output only. The creation time of the database.  Uses RFC 3339, where generated output will always be Z-normalized and use 0, 3, 6 or 9 fractional digits. Offsets other than "Z" are also accepted. Examples: `"2014-10-02T15:01:23Z"`, `"2014-10-02T15:01:23.045123456Z"` or `"2014-10-02T15:01:23+05:30"`. |
| `updateTime` | `string (Timestamp format)`  Output only. The last modification time of the database.  Uses RFC 3339, where generated output will always be Z-normalized and use 0, 3, 6 or 9 fractional digits. Offsets other than "Z" are also accepted. Examples: `"2014-10-02T15:01:23Z"`, `"2014-10-02T15:01:23.045123456Z"` or `"2014-10-02T15:01:23+05:30"`. |
| `deleteTime` | `string (Timestamp format)`  Output only. The deletion time of the database. Only set after the database is deleted.  Uses RFC 3339, where generated output will always be Z-normalized and use 0, 3, 6 or 9 fractional digits. Offsets other than "Z" are also accepted. Examples: `"2014-10-02T15:01:23Z"`, `"2014-10-02T15:01:23.045123456Z"` or `"2014-10-02T15:01:23+05:30"`. |
| `expireTime` | `string (Timestamp format)`  Output only. The time when this database is considered expired. Only set after the database is deleted.  Uses RFC 3339, where generated output will always be Z-normalized and use 0, 3, 6 or 9 fractional digits. Offsets other than "Z" are also accepted. Examples: `"2014-10-02T15:01:23Z"`, `"2014-10-02T15:01:23.045123456Z"` or `"2014-10-02T15:01:23+05:30"`. |
| `type` | `enum (Type)`  The database type. |
| Union field `options`. Options specified for the database type. `options` can be only one of the following: | |
| `hiveOptions` | `object (HiveDatabaseOptions)`  Options of a Hive database. |

## HiveDatabaseOptions

Options of a Hive database.

| JSON representation |
| --- |
| ``` {   "locationUri": string,   "parameters": {     string: string,     ...   } } ``` |

| Fields | |
| --- | --- |
| `locationUri` | `string`  Cloud Storage folder URI where the database data is stored, starting with "gs://". |
| `parameters` | `map (key: string, value: string)`  Stores user supplied Hive database parameters.  An object containing a list of `"key": value` pairs. Example: `{ "name": "wrench", "mass": "1.3kg", "count": "3" }`. |

## Type

The database type.

| Enums | |
| --- | --- |
| `TYPE_UNSPECIFIED` | The type is not specified. |
| `HIVE` | Represents a database storing tables compatible with Hive Metastore tables. |

| Methods | |
| --- | --- |
| `create` | Creates a new database. |
| `delete` | Deletes an existing database specified by the database ID. |
| `get` | Gets the database specified by the resource name. |
| `list` | List all databases in a specified catalog. |
| `patch` | Updates an existing database specified by the database ID. |

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2026-04-21 UTC.




[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Hard to understand","hardToUnderstand","thumb-down"],["Incorrect information or sample code","incorrectInformationOrSampleCode","thumb-down"],["Missing the information/samples I need","missingTheInformationSamplesINeed","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2026-04-21 UTC."],[],[]]