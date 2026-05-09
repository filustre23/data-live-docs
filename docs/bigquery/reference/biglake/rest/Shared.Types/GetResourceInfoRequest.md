As of April 20th, 2026, BigLake is now called Lakehouse for Apache Iceberg. BigLake metastore is now called the Lakehouse runtime catalog. Lakehouse APIs, client libraries, CLI commands, and IAM names remain unchanged and still reference BigLake.

* [Home](https://docs.cloud.google.com/)
* [BigLake API](https://docs.cloud.google.com/lakehouse/docs)

# GetResourceInfoRequest Stay organized with collections Save and categorize content based on your preferences.

* [JSON representation](#SCHEMA_REPRESENTATION)

Represents request of PolicyCallback.GetResourceInfo method.

| JSON representation |
| --- |
| ``` {   "resourceService": string,   "resourceName": string,   "fields": string,   "rpcRequestMessage": {     "@type": string,     field1: ...,     ...   },   "rpcResponseMessage": {     "@type": string,     field1: ...,     ...   } } ``` |

| Fields | |
| --- | --- |
| `resourceService` | `string`  REQUIRED: The name of the service that this resource belongs to, such as `pubsub.googleapis.com`. The service may be different from the DNS hostname that actually serves the request. |
| `resourceName` | `string`  REQUIRED: The stable identifier (name) of a resource on the `resourceService`. A resource can be logically identified as "//{resourceService}/{resourceName}". The differences between a resource name and a URI are:   * Resource name is a logical identifier, independent of network protocol and API version. For example, `//pubsub.googleapis.com/projects/123/topics/news-feed`. * URI often includes protocol and version information, so it can be used directly by applications. For example, `https://pubsub.googleapis.com/v1/projects/123/topics/news-feed`.   See <https://cloud.google.com/apis/design/resource_names> for details. |
| `fields` | `string (FieldMask format)`  OPTIONAL: field mask indicating which response parameters to return.  This is a comma-separated list of fully qualified names of fields. Example: `"user.displayName,photo"`. |
| `rpcRequestMessage` | `object`  OPTIONAL: The rpc request message in generic format. It contains additional information to be used to create the resource needed by IAM/CAL.  An object containing fields of an arbitrary type. An additional field `"@type"` contains a URI identifying the type. Example: `{ "id": 1234, "@type": "types.example.com/standard/id" }`. |
| `rpcResponseMessage` | `object`  OPTIONAL: The rpc response message in generic format. It contains additional information to be used to customize the CAL logs.  An object containing fields of an arbitrary type. An additional field `"@type"` contains a URI identifying the type. Example: `{ "id": 1234, "@type": "types.example.com/standard/id" }`. |

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2026-04-21 UTC.




[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Hard to understand","hardToUnderstand","thumb-down"],["Incorrect information or sample code","incorrectInformationOrSampleCode","thumb-down"],["Missing the information/samples I need","missingTheInformationSamplesINeed","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2026-04-21 UTC."],[],[]]