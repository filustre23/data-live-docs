* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback

# ResourceErrorDetail Stay organized with collections Save and categorize content based on your preferences.

* [JSON representation](#SCHEMA_REPRESENTATION)
* [ErrorDetail](#ErrorDetail)
  + [JSON representation](#ErrorDetail.SCHEMA_REPRESENTATION)
* [ErrorLocation](#ErrorLocation)
  + [JSON representation](#ErrorLocation.SCHEMA_REPRESENTATION)

Provides details for errors and the corresponding resources.

| JSON representation |
| --- |
| ``` {   "resourceInfo": {     object (ResourceInfo)   },   "errorDetails": [     {       object (ErrorDetail)     }   ],   "errorCount": integer } ``` |

| Fields | |
| --- | --- |
| `resourceInfo` | `object (ResourceInfo)`  Required. Information about the resource where the error is located. |
| `errorDetails[]` | `object (ErrorDetail)`  Required. The error details for the resource. |
| `errorCount` | `integer`  Required. How many errors there are in total for the resource. Truncation can be indicated by having an `errorCount` that is higher than the size of `errorDetails`. |

## ErrorDetail

Provides details for errors, e.g. issues that where encountered when processing a subtask.

| JSON representation |
| --- |
| ``` {   "location": {     object (ErrorLocation)   },   "errorInfo": {     object (ErrorInfo)   } } ``` |

| Fields | |
| --- | --- |
| `location` | `object (ErrorLocation)`  Optional. The exact location within the resource (if applicable). |
| `errorInfo` | `object (ErrorInfo)`  Required. Describes the cause of the error with structured detail. |

## ErrorLocation

Holds information about where the error is located.

| JSON representation |
| --- |
| ``` {   "line": integer,   "column": integer } ``` |

| Fields | |
| --- | --- |
| `line` | `integer`  Optional. If applicable, denotes the line where the error occurred. A zero value means that there is no line information. |
| `column` | `integer`  Optional. If applicable, denotes the column where the error occurred. A zero value means that there is no columns information. |




Send feedback

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2025-07-02 UTC.




Need to tell us more?

[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Hard to understand","hardToUnderstand","thumb-down"],["Incorrect information or sample code","incorrectInformationOrSampleCode","thumb-down"],["Missing the information/samples I need","missingTheInformationSamplesINeed","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2025-07-02 UTC."],[],[]]