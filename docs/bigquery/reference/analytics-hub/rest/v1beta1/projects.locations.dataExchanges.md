* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback

# REST Resource: projects.locations.dataExchanges Stay organized with collections Save and categorize content based on your preferences.

* [Resource: DataExchange](#DataExchange)
  + [JSON representation](#DataExchange.SCHEMA_REPRESENTATION)
* [Methods](#METHODS_SUMMARY)

## Resource: DataExchange

A data exchange is a container that lets you share data. Along with the descriptive information about the data exchange, it contains listings that reference shared datasets.

| JSON representation |
| --- |
| ``` {   "name": string,   "displayName": string,   "description": string,   "primaryContact": string,   "documentation": string,   "listingCount": integer,   "icon": string } ``` |

| Fields | |
| --- | --- |
| `name` | `string`  Output only. The resource name of the data exchange. e.g. `projects/myproject/locations/us/dataExchanges/123`. |
| `displayName` | `string`  Required. Human-readable display name of the data exchange. The display name must contain only Unicode letters, numbers (0-9), underscores (\_), dashes (-), spaces ( ), ampersands (&) and must not start or end with spaces. Default value is an empty string. Max length: 63 bytes. |
| `description` | `string`  Optional. Description of the data exchange. The description must not contain Unicode non-characters as well as C0 and C1 control codes except tabs (HT), new lines (LF), carriage returns (CR), and page breaks (FF). Default value is an empty string. Max length: 2000 bytes. |
| `primaryContact` | `string`  Optional. Email or URL of the primary point of contact of the data exchange. Max Length: 1000 bytes. |
| `documentation` | `string`  Optional. Documentation describing the data exchange. |
| `listingCount` | `integer`  Output only. Number of listings contained in the data exchange. |
| `icon` | `string (bytes format)`  Optional. Base64 encoded image representing the data exchange. Max Size: 3.0MiB Expected image dimensions are 512x512 pixels, however the API only performs validation on size of the encoded data. Note: For byte fields, the content of the fields are base64-encoded (which increases the size of the data by 33-36%) when using JSON on the wire.  A base64-encoded string. |

| Methods | |
| --- | --- |
| `create` | Creates a new data exchange. |
| `delete` | Deletes an existing data exchange. |
| `get` | Gets the details of a data exchange. |
| `getIamPolicy` | Gets the IAM policy. |
| `list` | Lists all data exchanges in a given project and location. |
| `patch` | Updates an existing data exchange. |
| `setIamPolicy` | Sets the IAM policy. |
| `testIamPermissions` | Returns the permissions that a caller has. |




Send feedback

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2025-07-02 UTC.




Need to tell us more?

[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Hard to understand","hardToUnderstand","thumb-down"],["Incorrect information or sample code","incorrectInformationOrSampleCode","thumb-down"],["Missing the information/samples I need","missingTheInformationSamplesINeed","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2025-07-02 UTC."],[],[]]