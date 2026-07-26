* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)

Send feedback

# Method: operations.list Stay organized with collections Save and categorize content based on your preferences.

* [HTTP request](#body.HTTP_TEMPLATE)
* [Path parameters](#body.PATH_PARAMETERS)
* [Query parameters](#body.QUERY_PARAMETERS)
* [Request body](#body.request_body)
* [Response body](#body.response_body)
  + [JSON representation](#body.ListOperationsResponse.SCHEMA_REPRESENTATION)
* [Authorization Scopes](#body.aspect)
* [Operation](#Operation)
  + [JSON representation](#Operation.SCHEMA_REPRESENTATION)
* [Try it!](#try-it)

Lists operations that match the specified filter in the request. If the server doesn't support this method, it returns `UNIMPLEMENTED`.

NOTE: the `name` binding allows API services to override the binding to use different resource name schemes, such as `users/*/operations`. To override the binding, API services can add a binding such as `"/v1/{name=users/*}/operations"` to their service configuration. For backwards compatibility, the default name includes the operations collection id, however overriding users must ensure the name binding is the parent resource, without the operations collection id.

### HTTP request

`GET https://bigqueryreservation.googleapis.com/v1/{name}`

The URL uses [gRPC Transcoding](https://github.com/googleapis/googleapis/blob/master/google/api/http.proto) syntax.

### Path parameters

| Parameters | |
| --- | --- |
| `name` | `string`  The name of the operation's parent resource. |

### Query parameters

| Parameters | |
| --- | --- |
| `filter` | `string`  The standard list filter. |
| `pageSize` | `integer`  The standard list page size. |
| `pageToken` | `string`  The standard list page token. |

### Request body

The request body must be empty.

### Response body

If successful, the response body contains data with the following structure:

The response message for `Operations.ListOperations`.

| JSON representation | |
| --- | --- |
| ``` {   "operations": [     {       object (Operation)     }   ],   "nextPageToken": string } ``` |

| Fields | |
| --- | --- |
| `operations[]` | `object (Operation)`  A list of operations that matches the specified filter in the request. |
| `nextPageToken` | `string`  The standard List next-page token. |

### Authorization Scopes

Requires one of the following OAuth scopes:

* `https://www.googleapis.com/auth/bigquery`
* `https://www.googleapis.com/auth/cloud-platform`

For more information, see the [Authentication Overview](https://cloud.google.com/docs/authentication/).

## Operation

This resource represents a long-running operation that is the result of a network API call.

| JSON representation | |
| --- | --- |
| ``` {   "name": string,   "metadata": {     "@type": string,     field1: ...,     ...   },   "done": boolean,    // Union field result can be only one of the following:   "error": {     object (Status)   },   "response": {     "@type": string,     field1: ...,     ...   }   // End of list of possible types for union field result. } ``` |

| Fields | |
| --- | --- |
| `name` | `string`  The server-assigned name, which is only unique within the same service that originally returns it. If you use the default HTTP mapping, the `name` should be a resource name ending with `operations/{unique_id}`. |
| `metadata` | `object`  Service-specific metadata associated with the operation. It typically contains progress information and common metadata such as create time. Some services might not provide such metadata. Any method that returns a long-running operation should document the metadata type, if any.  An object containing fields of an arbitrary type. An additional field `"@type"` contains a URI identifying the type. Example: `{ "id": 1234, "@type": "types.example.com/standard/id" }`. |
| `done` | `boolean`  If the value is `false`, it means the operation is still in progress. If `true`, the operation is completed, and either `error` or `response` is available. |
| Union field `result`. The operation result, which can be either an `error` or a valid `response`. If `done` == `false`, neither `error` nor `response` is set. If `done` == `true`, exactly one of `error` or `response` is set. `result` can be only one of the following: | | |
| `error` | `object (Status)`  The error result of the operation in case of failure or cancellation. |
| `response` | `object`  The normal response of the operation in case of success. If the original method returns no data on success, such as `Delete`, the response is `google.protobuf.Empty`. If the original method is standard `Get`/`Create`/`Update`, the response should be the resource. For other methods, the response should have the type `XxxResponse`, where `Xxx` is the original method name. For example, if the original method name is `TakeSnapshot()`, the inferred response type is `TakeSnapshotResponse`.  An object containing fields of an arbitrary type. An additional field `"@type"` contains a URI identifying the type. Example: `{ "id": 1234, "@type": "types.example.com/standard/id" }`. |

## Try it!




Send feedback

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2025-07-02 UTC.




Need to tell us more?

[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Hard to understand","hardToUnderstand","thumb-down"],["Incorrect information or sample code","incorrectInformationOrSampleCode","thumb-down"],["Missing the information/samples I need","missingTheInformationSamplesINeed","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2025-07-02 UTC."],[],[]]