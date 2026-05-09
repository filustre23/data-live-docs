As of April 20th, 2026, BigLake is now called Lakehouse for Apache Iceberg. BigLake metastore is now called the Lakehouse runtime catalog. Lakehouse APIs, client libraries, CLI commands, and IAM names remain unchanged and still reference BigLake.

* [Home](https://docs.cloud.google.com/)
* [BigLake API](https://docs.cloud.google.com/lakehouse/docs)
* [Technology areas](https://docs.cloud.google.com/docs)
* [Reference](https://docs.cloud.google.com/lakehouse/docs/quotas)

# REST Resource: projects.locations.catalogs.databases.locks Stay organized with collections Save and categorize content based on your preferences.

* [Resource: Lock](#Lock)
  + [JSON representation](#Lock.SCHEMA_REPRESENTATION)
* [Type](#Type)
* [State](#State)
* [Methods](#METHODS_SUMMARY)

## Resource: Lock

Represents a lock.

| JSON representation |
| --- |
| ``` {   "name": string,   "createTime": string,   "type": enum (Type),   "state": enum (State),    // Union field resources can be only one of the following:   "tableId": string   // End of list of possible types for union field resources. } ``` |

| Fields | |
| --- | --- |
| `name` | `string`  Output only. The resource name. Format: projects/{project\_id\_or\_number}/locations/{locationId}/catalogs/{catalogId}/databases/{databaseId}/locks/{lock\_id} |
| `createTime` | `string (Timestamp format)`  Output only. The creation time of the lock.  Uses RFC 3339, where generated output will always be Z-normalized and use 0, 3, 6 or 9 fractional digits. Offsets other than "Z" are also accepted. Examples: `"2014-10-02T15:01:23Z"`, `"2014-10-02T15:01:23.045123456Z"` or `"2014-10-02T15:01:23+05:30"`. |
| `type` | `enum (Type)`  The lock type. |
| `state` | `enum (State)`  Output only. The lock state. |
| Union field `resources`. The resource that the lock will be created on. `resources` can be only one of the following: | |
| `tableId` | `string`  The table ID (not fully qualified name) in the same database that the lock will be created on. The table must exist. |

## Type

The lock type.

| Enums | |
| --- | --- |
| `TYPE_UNSPECIFIED` | The type is not specified. |
| `EXCLUSIVE` | An exclusive lock prevents another lock from being created on the same resource. |

## State

The lock state.

| Enums | |
| --- | --- |
| `STATE_UNSPECIFIED` | The state is not specified. |
| `WAITING` | Waiting to acquire the lock. |
| `ACQUIRED` | The lock has been acquired. |

| Methods | |
| --- | --- |
| `check` | Checks the state of a lock specified by the lock ID. |
| `create` | Creates a new lock. |
| `delete` | Deletes an existing lock specified by the lock ID. |
| `list` | List all locks in a specified database. |

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2026-04-21 UTC.




[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Hard to understand","hardToUnderstand","thumb-down"],["Incorrect information or sample code","incorrectInformationOrSampleCode","thumb-down"],["Missing the information/samples I need","missingTheInformationSamplesINeed","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2026-04-21 UTC."],[],[]]