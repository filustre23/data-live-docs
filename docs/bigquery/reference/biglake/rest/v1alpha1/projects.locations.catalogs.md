As of April 20th, 2026, BigLake is now called Google Cloud Lakehouse. BigLake metastore is now called the Lakehouse runtime catalog. Lakehouse APIs, client libraries, CLI commands, and IAM names remain unchanged and still reference BigLake.

* [Home](https://docs.cloud.google.com/)
* [BigLake API](https://docs.cloud.google.com/lakehouse/docs)
* [Technology areas](https://docs.cloud.google.com/docs)
* [Reference](https://docs.cloud.google.com/lakehouse/docs/quotas)

# REST Resource: projects.locations.catalogs Stay organized with collections Save and categorize content based on your preferences.

* [Resource: Catalog](#Catalog)
  + [JSON representation](#Catalog.SCHEMA_REPRESENTATION)
* [Methods](#METHODS_SUMMARY)

## Resource: Catalog

Catalog is the container of databases.

| JSON representation |
| --- |
| ``` {   "name": string,   "createTime": string,   "updateTime": string,   "deleteTime": string,   "expireTime": string } ``` |

| Fields | |
| --- | --- |
| `name` | `string`  Output only. The resource name. Format: projects/{project\_id\_or\_number}/locations/{locationId}/catalogs/{catalogId} |
| `createTime` | `string (Timestamp format)`  Output only. The creation time of the catalog.  Uses RFC 3339, where generated output will always be Z-normalized and use 0, 3, 6 or 9 fractional digits. Offsets other than "Z" are also accepted. Examples: `"2014-10-02T15:01:23Z"`, `"2014-10-02T15:01:23.045123456Z"` or `"2014-10-02T15:01:23+05:30"`. |
| `updateTime` | `string (Timestamp format)`  Output only. The last modification time of the catalog.  Uses RFC 3339, where generated output will always be Z-normalized and use 0, 3, 6 or 9 fractional digits. Offsets other than "Z" are also accepted. Examples: `"2014-10-02T15:01:23Z"`, `"2014-10-02T15:01:23.045123456Z"` or `"2014-10-02T15:01:23+05:30"`. |
| `deleteTime` | `string (Timestamp format)`  Output only. The deletion time of the catalog. Only set after the catalog is deleted.  Uses RFC 3339, where generated output will always be Z-normalized and use 0, 3, 6 or 9 fractional digits. Offsets other than "Z" are also accepted. Examples: `"2014-10-02T15:01:23Z"`, `"2014-10-02T15:01:23.045123456Z"` or `"2014-10-02T15:01:23+05:30"`. |
| `expireTime` | `string (Timestamp format)`  Output only. The time when this catalog is considered expired. Only set after the catalog is deleted.  Uses RFC 3339, where generated output will always be Z-normalized and use 0, 3, 6 or 9 fractional digits. Offsets other than "Z" are also accepted. Examples: `"2014-10-02T15:01:23Z"`, `"2014-10-02T15:01:23.045123456Z"` or `"2014-10-02T15:01:23+05:30"`. |

| Methods | |
| --- | --- |
| `create` | Creates a new catalog. |
| `delete` | Deletes an existing catalog specified by the catalog ID. |
| `get` | Gets the catalog specified by the resource name. |
| `list` | List all catalogs in a specified project. |

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2026-04-21 UTC.




[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Hard to understand","hardToUnderstand","thumb-down"],["Incorrect information or sample code","incorrectInformationOrSampleCode","thumb-down"],["Missing the information/samples I need","missingTheInformationSamplesINeed","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2026-04-21 UTC."],[],[]]