* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback

# Method: datasets.get Stay organized with collections Save and categorize content based on your preferences.

* [HTTP request](#body.HTTP_TEMPLATE)
* [Path parameters](#body.PATH_PARAMETERS)
* [Query parameters](#body.QUERY_PARAMETERS)
* [Request body](#body.request_body)
* [Response body](#body.response_body)
* [Authorization scopes](#body.aspect)
* [DatasetView](#DatasetView)
* [Try it!](#try-it)

Returns the dataset specified by datasetID.

### HTTP request

`GET https://bigquery.googleapis.com/bigquery/v2/projects/{projectId}/datasets/{datasetId}`

The URL uses [gRPC Transcoding](https://google.aip.dev/127) syntax.

### Path parameters

| Parameters | |
| --- | --- |
| `projectId` | `string`  Required. Project ID of the requested dataset |
| `datasetId` | `string`  Required. Dataset ID of the requested dataset |

### Query parameters

| Parameters | |
| --- | --- |
| `datasetView` | `enum (DatasetView)`  Optional. Specifies the view that determines which dataset information is returned. By default, metadata and ACL information are returned. |
| `accessPolicyVersion` | `integer`  Optional. The version of the access policy schema to fetch. Valid values are 0, 1, and 3. Requests specifying an invalid value will be rejected.  Requests for conditional access policy binding in datasets must specify version 3. Dataset with no conditional role bindings in access policy may specify any valid value or leave the field unset.  This field will be mapped to [IAM Policy version](https://cloud.google.com/iam/docs/policies#versions) and will be used to fetch policy from IAM.  If unset or if 0 or 1 value is used for dataset with conditional bindings, access entry with condition will have role string appended by 'withcond' string followed by a hash value. For example : { "access": [ { "role": "roles/bigquery.dataViewer\_with\_conditionalbinding\_7a34awqsda", "userByEmail": "user@example.com", } ] } Please refer <https://cloud.google.com/iam/docs/troubleshooting-withcond> for more details. |

### Request body

The request body must be empty.

### Response body

If successful, the response body contains an instance of `Dataset`.

### Authorization scopes

Requires one of the following OAuth scopes:

* `https://www.googleapis.com/auth/bigquery`
* `https://www.googleapis.com/auth/cloud-platform`
* `https://www.googleapis.com/auth/bigquery.readonly`
* `https://www.googleapis.com/auth/cloud-platform.read-only`

For more information, see the [Authentication Overview](/docs/authentication#authorization-gcp).

## DatasetView

DatasetView specifies which dataset information is returned.

| Enums | |
| --- | --- |
| `DATASET_VIEW_UNSPECIFIED` | The default value. Default to the FULL view. |
| `METADATA` | View metadata information for the dataset, such as friendlyName, description, labels, etc. |
| `ACL` | View ACL information for the dataset, which defines dataset access for one or more entities. |
| `FULL` | View both dataset metadata and ACL information. |




Send feedback

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2025-12-22 UTC.




Need to tell us more?

[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Hard to understand","hardToUnderstand","thumb-down"],["Incorrect information or sample code","incorrectInformationOrSampleCode","thumb-down"],["Missing the information/samples I need","missingTheInformationSamplesINeed","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2025-12-22 UTC."],[],[]]