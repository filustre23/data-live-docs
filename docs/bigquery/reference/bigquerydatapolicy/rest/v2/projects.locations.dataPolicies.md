* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback

# REST Resource: projects.locations.dataPolicies Stay organized with collections Save and categorize content based on your preferences.

* [Resource: DataPolicy](#DataPolicy)
  + [JSON representation](#DataPolicy.SCHEMA_REPRESENTATION)
* [DataMaskingPolicy](#DataMaskingPolicy)
  + [JSON representation](#DataMaskingPolicy.SCHEMA_REPRESENTATION)
* [PredefinedExpression](#PredefinedExpression)
* [DataPolicyType](#DataPolicyType)
* [Version](#Version)
* [Methods](#METHODS_SUMMARY)

## Resource: DataPolicy

Represents the label-policy binding.

| JSON representation |
| --- |
| ``` {   "name": string,   "dataPolicyId": string,   "dataPolicyType": enum (DataPolicyType),   "policyTag": string,   "grantees": [     string   ],   "version": enum (Version),    // Union field policy can be only one of the following:   "dataMaskingPolicy": {     object (DataMaskingPolicy)   }   // End of list of possible types for union field policy.   "etag": string } ``` |

| Fields | |
| --- | --- |
| `name` | `string`  Identifier. Resource name of this data policy, in the format of `projects/{projectNumber}/locations/{locationId}/dataPolicies/{dataPolicyId}`. |
| `dataPolicyId` | `string`  Output only. User-assigned (human readable) ID of the data policy that needs to be unique within a project. Used as {dataPolicyId} in part of the resource name. |
| `dataPolicyType` | `enum (DataPolicyType)`  Required. Type of data policy. |
| `policyTag` | `string`  Output only. Policy tag resource name, in the format of `projects/{projectNumber}/locations/{locationId}/taxonomies/{taxonomyId}/policyTags/{policyTag_id}`. policyTag is supported only for V1 data policies. |
| `grantees[]` | `string`  Optional. The list of IAM principals that have Fine Grained Access to the underlying data goverened by this data policy.  Uses the [IAM V2 principal syntax](https://cloud.google.com/iam/docs/principal-identifiers#v2) Only supports principal types users, groups, serviceaccounts, cloudidentity. This field is supported in V2 Data Policy only. In case of V1 data policies (i.e. verion = 1 and policyTag is set), this field is not populated. |
| `version` | `enum (Version)`  Output only. The version of the Data Policy resource. |
| Union field `policy`. The policy that is bound to this data policy. `policy` can be only one of the following: | |
| `dataMaskingPolicy` | `object (DataMaskingPolicy)`  Optional. The data masking policy that specifies the data masking rule to use. It must be set if the data policy type is DATA\_MASKING\_POLICY. |
| `etag` | `string`  The etag for this Data Policy. This field is used for dataPolicies.patch calls. If Data Policy exists, this field is required and must match the server's etag. It will also be populated in the response of dataPolicies.get, dataPolicies.create, and dataPolicies.patch calls. |

## DataMaskingPolicy

The policy used to specify data masking rule.

| JSON representation |
| --- |
| ``` {    // Union field masking_expression can be only one of the following:   "predefinedExpression": enum (PredefinedExpression),   "routine": string   // End of list of possible types for union field masking_expression. } ``` |

| Fields | |
| --- | --- |
| Union field `masking_expression`. A masking expression to bind to the data masking rule. `masking_expression` can be only one of the following: | |
| `predefinedExpression` | `enum (PredefinedExpression)`  Optional. A predefined masking expression. |
| `routine` | `string`  Optional. The name of the BigQuery routine that contains the custom masking routine, in the format of `projects/{projectNumber}/datasets/{dataset_id}/routines/{routine_id}`. |

## PredefinedExpression

The available masking rules. Learn more here: <https://cloud.google.com/bigquery/docs/column-data-masking-intro#masking_options>.

| Enums | |
| --- | --- |
| `PREDEFINED_EXPRESSION_UNSPECIFIED` | Default, unspecified predefined expression. No masking will take place since no expression is specified. |
| `SHA256` | Masking expression to replace data with SHA-256 hash. |
| `ALWAYS_NULL` | Masking expression to replace data with NULLs. |
| `DEFAULT_MASKING_VALUE` | Masking expression to replace data with their default masking values. The default masking values for each type listed as below:   * STRING: "" * BYTES: b'' * INTEGER: 0 * FLOAT: 0.0 * NUMERIC: 0 * BOOLEAN: FALSE * TIMESTAMP: 1970-01-01 00:00:00 UTC * DATE: 1970-01-01 * TIME: 00:00:00 * DATETIME: 1970-01-01T00:00:00 * GEOGRAPHY: POINT(0 0) * BIGNUMERIC: 0 * ARRAY: [] * STRUCT: NOT\_APPLICABLE * JSON: NULL |
| `LAST_FOUR_CHARACTERS` | Masking expression shows the last four characters of text. The masking behavior is as follows:   * If text length > 4 characters: Replace text with XXXXX, append last four characters of original text. * If text length <= 4 characters: Apply SHA-256 hash. |
| `FIRST_FOUR_CHARACTERS` | Masking expression shows the first four characters of text. The masking behavior is as follows:   * If text length > 4 characters: Replace text with XXXXX, prepend first four characters of original text. * If text length <= 4 characters: Apply SHA-256 hash. |
| `EMAIL_MASK` | Masking expression for email addresses. The masking behavior is as follows:   * Syntax-valid email address: Replace username with XXXXX. For example, [cloudysanfrancisco@gmail.com](mailto:cloudysanfrancisco@gmail.com) becomes [XXXXX@gmail.com](mailto:XXXXX@gmail.com). * Syntax-invalid email address: Apply SHA-256 hash.   For more information, see [Email mask](https://cloud.google.com/bigquery/docs/column-data-masking-intro#masking_options). |
| `DATE_YEAR_MASK` | Masking expression to only show the *year* of `Date`, `DateTime` and `TimeStamp`. For example, with the year 2076:   * DATE : 2076-01-01 * DATETIME : 2076-01-01T00:00:00 * TIMESTAMP : 2076-01-01 00:00:00 UTC   Truncation occurs according to the UTC time zone. To change this, adjust the default time zone using the `time_zone` system variable. For more information, see [System variables reference](https://cloud.google.com/bigquery/docs/reference/system-variables). |
| `RANDOM_HASH` | Masking expression that uses hashing to mask column data. It differs from SHA256 in that a unique random value is generated for each query and is added to the hash input, resulting in the hash / masked result to be different for each query. Hence the name "random hash". |

## DataPolicyType

A list of supported data policy types.

| Enums | |
| --- | --- |
| `DATA_POLICY_TYPE_UNSPECIFIED` | Default value for the data policy type. This should not be used. |
| `DATA_MASKING_POLICY` | Used to create a data policy for data masking. |
| `RAW_DATA_ACCESS_POLICY` | Used to create a data policy for raw data access. |
| `COLUMN_LEVEL_SECURITY_POLICY` | Used to create a data policy for column-level security, without data masking. This is deprecated in V2 api and only present to support GET and LIST operations for V1 data policies in V2 api. |

## Version

The supported versions for the Data Policy resource.

| Enums | |
| --- | --- |
| `VERSION_UNSPECIFIED` | Default value for the data policy version. This should not be used. |
| `V1` | V1 data policy version. V1 Data Policies will be present in V2 List api response, but can not be created/updated/deleted from V2 api. |
| `V2` | V2 data policy version. |

| Methods | |
| --- | --- |
| `addGrantees` | Adds new grantees to a data policy. |
| `create` | Creates a new data policy under a project with the given `data_policy_id` (used as the display name), and data policy type. |
| `delete` | Deletes the data policy specified by its resource name. |
| `get` | Gets the data policy specified by its resource name. |
| `getIamPolicy` | Gets the IAM policy for the specified data policy. |
| `list` | List all of the data policies in the specified parent project. |
| `patch` | Updates the metadata for an existing data policy. |
| `removeGrantees` | Removes grantees from a data policy. |
| `setIamPolicy` | Sets the IAM policy for the specified data policy. |
| `testIamPermissions` | Returns the caller's permission on the specified data policy resource. |




Send feedback

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2025-07-28 UTC.




Need to tell us more?

[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Hard to understand","hardToUnderstand","thumb-down"],["Incorrect information or sample code","incorrectInformationOrSampleCode","thumb-down"],["Missing the information/samples I need","missingTheInformationSamplesINeed","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2025-07-28 UTC."],[],[]]