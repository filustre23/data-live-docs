* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback

# Method: transferConfigs.patch Stay organized with collections Save and categorize content based on your preferences.

* [HTTP request](#body.HTTP_TEMPLATE)
* [Path parameters](#body.PATH_PARAMETERS)
* [Query parameters](#body.QUERY_PARAMETERS)
* [Request body](#body.request_body)
* [Response body](#body.response_body)
* [Authorization scopes](#body.aspect)
* [Try it!](#try-it)

**Full name**: projects.transferConfigs.patch

Updates a data transfer configuration. All fields must be set, even if they are not updated.

### HTTP request

`PATCH https://bigquerydatatransfer.googleapis.com/v1/{transferConfig.name=projects/*/transferConfigs/*}`

The URL uses [gRPC Transcoding](https://google.aip.dev/127) syntax.

### Path parameters

| Parameters | |
| --- | --- |
| `transferConfig.name` | `string`  Identifier. The resource name of the transfer config. Transfer config names have the form either `projects/{projectId}/locations/{region}/transferConfigs/{configId}` or `projects/{projectId}/transferConfigs/{configId}`, where `configId` is usually a UUID, even though it is not guaranteed or required. The name is ignored when creating a transfer config. |

### Query parameters

| Parameters | |
| --- | --- |
| `authorizationCode (deprecated)` | `string`  Deprecated: Authorization code was required when `transferConfig.dataSourceId` is 'youtube\_channel' but it is no longer used in any data sources. Use `versionInfo` instead.  Optional OAuth2 authorization code to use with this transfer configuration. This is required only if `transferConfig.dataSourceId` is 'youtube\_channel' and new credentials are needed, as indicated by `dataSources.checkValidCreds`. In order to obtain authorizationCode, make a request to the following URL:     ``` https://bigquery.cloud.google.com/datatransfer/oauthz/auth?redirect_uri=urn:ietf:wg:oauth:2.0:oob&response_type=authorization_code&client_id=clientId&scope=data_source_scopes ```  * The clientId is the OAuth clientId of the data source as returned by ListDataSources method. * data\_source\_scopes are the scopes returned by ListDataSources method.   Note that this should not be set when `serviceAccountName` is used to update the transfer config. |
| `updateMask` | `string (FieldMask format)`  Required. Required list of fields to be updated in this request.  This is a comma-separated list of fully qualified names of fields. Example: `"user.displayName,photo"`. |
| `versionInfo` | `string`  Optional version info. This parameter replaces `authorizationCode` which is no longer used in any data sources. This is required only if `transferConfig.dataSourceId` is 'youtube\_channel' *or* new credentials are needed, as indicated by `dataSources.checkValidCreds`. In order to obtain version info, make a request to the following URL:     ``` https://bigquery.cloud.google.com/datatransfer/oauthz/auth?redirect_uri=urn:ietf:wg:oauth:2.0:oob&response_type=version_info&client_id=clientId&scope=data_source_scopes ```  * The clientId is the OAuth clientId of the data source as returned by ListDataSources method. * data\_source\_scopes are the scopes returned by ListDataSources method.   Note that this should not be set when `serviceAccountName` is used to update the transfer config. |
| `serviceAccountName` | `string`  Optional service account email. If this field is set, the transfer config will be created with this service account's credentials. It requires that the requesting user calling this API has permissions to act as this service account.  Note that not all data sources support service account credentials when creating a transfer config. For the latest list of data sources, read about [using service accounts](https://cloud.google.com/bigquery-transfer/docs/use-service-accounts). |

### Request body

The request body contains an instance of `TransferConfig`.

### Response body

If successful, the response body contains an instance of `TransferConfig`.

### Authorization scopes

Requires the following OAuth scope:

* `https://www.googleapis.com/auth/cloud-platform`

For more information, see the [Authentication Overview](/docs/authentication#authorization-gcp).




Send feedback

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2026-03-25 UTC.




Need to tell us more?

[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Hard to understand","hardToUnderstand","thumb-down"],["Incorrect information or sample code","incorrectInformationOrSampleCode","thumb-down"],["Missing the information/samples I need","missingTheInformationSamplesINeed","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2026-03-25 UTC."],[],[]]