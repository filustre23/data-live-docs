* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback

# QueryParameter Stay organized with collections Save and categorize content based on your preferences.

* [JSON representation](#SCHEMA_REPRESENTATION)
* [QueryParameterType](#QueryParameterType)
  + [JSON representation](#QueryParameterType.SCHEMA_REPRESENTATION)
* [QueryParameterValue](#QueryParameterValue)
  + [JSON representation](#QueryParameterValue.SCHEMA_REPRESENTATION)
* [RangeValue](#RangeValue)
  + [JSON representation](#RangeValue.SCHEMA_REPRESENTATION)

A parameter given to a query.

| JSON representation |
| --- |
| ``` {   "name": string,   "parameterType": {     object (QueryParameterType)   },   "parameterValue": {     object (QueryParameterValue)   } } ``` |

| Fields | |
| --- | --- |
| `name` | `string`  Optional. If unset, this is a positional parameter. Otherwise, should be unique within a query. |
| `parameterType` | `object (QueryParameterType)`  Required. The type of this parameter. |
| `parameterValue` | `object (QueryParameterValue)`  Required. The value of this parameter. |

## QueryParameterType

The type of a query parameter.

| JSON representation |
| --- |
| ``` {   "type": string,   "arrayType": {     object (QueryParameterType)   },   "structTypes": [     {       "name": string,       "type": {         object (QueryParameterType)       },       "description": string     }   ],   "rangeElementType": {     object (QueryParameterType)   } } ``` |

| Fields | |
| --- | --- |
| `type` | `string`  Required. The top level type of this field. |
| `arrayType` | `object (QueryParameterType)`  Optional. The type of the array's elements, if this is an array. |
| `structTypes[]` | `object`  Optional. The types of the fields of this struct, in order, if this is a struct. |
| `structTypes[].name` | `string`  Optional. The name of this field. |
| `structTypes[].type` | `object (QueryParameterType)`  Required. The type of this field. |
| `structTypes[].description` | `string`  Optional. Human-oriented description of the field. |
| `rangeElementType` | `object (QueryParameterType)`  Optional. The element type of the range, if this is a range. |

## QueryParameterValue

The value of a query parameter.

| JSON representation |
| --- |
| ``` {   "value": string,   "arrayValues": [     {       object (QueryParameterValue)     }   ],   "structValues": {     string: {       object (QueryParameterValue)     },     ...   },   "rangeValue": {     object (RangeValue)   } } ``` |

| Fields | |
| --- | --- |
| `value` | `string`  Optional. The value of this value, if a simple scalar type. |
| `arrayValues[]` | `object (QueryParameterValue)`  Optional. The array values, if this is an array type. |
| `structValues` | `map (key: string, value: object (QueryParameterValue))`  The struct field values. |
| `rangeValue` | `object (RangeValue)`  Optional. The range value, if this is a range type. |

## RangeValue

Represents the value of a range.

| JSON representation |
| --- |
| ``` {   "start": {     object (QueryParameterValue)   },   "end": {     object (QueryParameterValue)   } } ``` |

| Fields | |
| --- | --- |
| `start` | `object (QueryParameterValue)`  Optional. The start value of the range. A missing value represents an unbounded start. |
| `end` | `object (QueryParameterValue)`  Optional. The end value of the range. A missing value represents an unbounded end. |




Send feedback

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2025-07-02 UTC.




Need to tell us more?

[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Hard to understand","hardToUnderstand","thumb-down"],["Incorrect information or sample code","incorrectInformationOrSampleCode","thumb-down"],["Missing the information/samples I need","missingTheInformationSamplesINeed","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2025-07-02 UTC."],[],[]]