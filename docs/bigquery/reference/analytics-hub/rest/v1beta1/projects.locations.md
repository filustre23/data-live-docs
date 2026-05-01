* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)

Send feedback

# REST Resource: projects.locations Stay organized with collections Save and categorize content based on your preferences.

* [Resource: Location](#Location)
  + [JSON representation](#Location.SCHEMA_REPRESENTATION)
* [Methods](#METHODS_SUMMARY)

## Resource: Location

A resource that represents Google Cloud Platform location.

| JSON representation |
| --- |
| ``` {   "name": string,   "locationId": string,   "displayName": string,   "labels": {     string: string,     ...   },   "metadata": {     "@type": string,     field1: ...,     ...   } } ``` |

| Fields | |
| --- | --- |
| `name` | `string`  Resource name for the location, which may vary between implementations. For example: `"projects/example-project/locations/us-east1"` |
| `locationId` | `string`  The canonical id for this location. For example: `"us-east1"`. |
| `displayName` | `string`  The friendly name for this location, typically a nearby city name. For example, "Tokyo". |
| `labels` | `map (key: string, value: string)`  Cross-service attributes for the location. For example     ``` {"cloud.googleapis.com/region": "us-east1"} ```   An object containing a list of `"key": value` pairs. Example: `{ "name": "wrench", "mass": "1.3kg", "count": "3" }`. |
| `metadata` | `object`  Service-specific metadata. For example the available capacity at the given location.  An object containing fields of an arbitrary type. An additional field `"@type"` contains a URI identifying the type. Example: `{ "id": 1234, "@type": "types.example.com/standard/id" }`. |

| Methods | |
| --- | --- |
| `get` | Gets information about a location. |
| `list` | Lists information about the supported locations for this service. |




Send feedback

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2025-07-02 UTC.




Need to tell us more?

[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Hard to understand","hardToUnderstand","thumb-down"],["Incorrect information or sample code","incorrectInformationOrSampleCode","thumb-down"],["Missing the information/samples I need","missingTheInformationSamplesINeed","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2025-07-02 UTC."],[],[]]