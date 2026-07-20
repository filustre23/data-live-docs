* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback

# DestinationDataset Stay organized with collections Save and categorize content based on your preferences.

* [JSON representation](#SCHEMA_REPRESENTATION)
* [DestinationDatasetReference](#DestinationDatasetReference)
  + [JSON representation](#DestinationDatasetReference.SCHEMA_REPRESENTATION)

Defines the destination bigquery dataset.

| JSON representation |
| --- |
| ``` {   "datasetReference": {     object (DestinationDatasetReference)   },   "friendlyName": string,   "description": string,   "labels": {     string: string,     ...   },   "location": string,   "replicaLocations": [     string   ] } ``` |

| Fields | |
| --- | --- |
| `datasetReference` | `object (DestinationDatasetReference)`  Required. A reference that identifies the destination dataset. |
| `friendlyName` | `string`  Optional. A descriptive name for the dataset. |
| `description` | `string`  Optional. A user-friendly description of the dataset. |
| `labels` | `map (key: string, value: string)`  Optional. The labels associated with this dataset. You can use these to organize and group your datasets. You can set this property when inserting or updating a dataset. See <https://cloud.google.com/resource-manager/docs/creating-managing-labels> for more information.  An object containing a list of `"key": value` pairs. Example: `{ "name": "wrench", "mass": "1.3kg", "count": "3" }`. |
| `location` | `string`  Required. The geographic location where the dataset should reside. See <https://cloud.google.com/bigquery/docs/locations> for supported locations. |
| `replicaLocations[]` | `string`  Optional. The geographic locations where the dataset should be replicated. See [BigQuery locations](https://cloud.google.com/bigquery/docs/locations) for supported locations. |

## DestinationDatasetReference

| JSON representation |
| --- |
| ``` {   "datasetId": string,   "projectId": string } ``` |

| Fields | |
| --- | --- |
| `datasetId` | `string`  Required. A unique ID for this dataset, without the project name. The ID must contain only letters (a-z, A-Z), numbers (0-9), or underscores (\_). The maximum length is 1,024 characters. |
| `projectId` | `string`  Required. The ID of the project containing this dataset. |




Send feedback

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2025-09-02 UTC.




Need to tell us more?

[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Hard to understand","hardToUnderstand","thumb-down"],["Incorrect information or sample code","incorrectInformationOrSampleCode","thumb-down"],["Missing the information/samples I need","missingTheInformationSamplesINeed","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2025-09-02 UTC."],[],[]]