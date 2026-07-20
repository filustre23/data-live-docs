* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback

# REST Resource: projects.dataSources Stay organized with collections Save and categorize content based on your preferences.

* [Resource: DataSource](#DataSource)
  + [JSON representation](#DataSource.SCHEMA_REPRESENTATION)
  + [TransferType](#DataSource.TransferType)
  + [DataSourceParameter](#DataSource.DataSourceParameter)
    - [JSON representation](#DataSource.DataSourceParameter.SCHEMA_REPRESENTATION)
  + [Type](#DataSource.Type)
  + [AuthorizationType](#DataSource.AuthorizationType)
  + [DataRefreshType](#DataSource.DataRefreshType)
* [Methods](#METHODS_SUMMARY)

## Resource: DataSource

Defines the properties and custom parameters for a data source.

| JSON representation |
| --- |
| ``` {   "name": string,   "dataSourceId": string,   "displayName": string,   "description": string,   "clientId": string,   "scopes": [     string   ],   "transferType": enum (TransferType),   "supportsMultipleTransfers": boolean,   "updateDeadlineSeconds": integer,   "defaultSchedule": string,   "supportsCustomSchedule": boolean,   "parameters": [     {       object (DataSourceParameter)     }   ],   "helpUrl": string,   "authorizationType": enum (AuthorizationType),   "dataRefreshType": enum (DataRefreshType),   "defaultDataRefreshWindowDays": integer,   "manualRunsDisabled": boolean,   "minimumScheduleInterval": string } ``` |

| Fields | |
| --- | --- |
| `name` | `string`  Output only. Data source resource name. |
| `dataSourceId` | `string`  Data source id. |
| `displayName` | `string`  User friendly data source name. |
| `description` | `string`  User friendly data source description string. |
| `clientId` | `string`  Data source client id which should be used to receive refresh token. |
| `scopes[]` | `string`  Api auth scopes for which refresh token needs to be obtained. These are scopes needed by a data source to prepare data and ingest them into BigQuery, e.g., <https://www.googleapis.com/auth/bigquery> |
| `transferType (deprecated)` | `enum (TransferType)`  This item is deprecated!  Deprecated. This field has no effect. |
| `supportsMultipleTransfers (deprecated)` | `boolean`  This item is deprecated!  Deprecated. This field has no effect. |
| `updateDeadlineSeconds` | `integer`  The number of seconds to wait for an update from the data source before the Data Transfer Service marks the transfer as FAILED. |
| `defaultSchedule` | `string`  Default data transfer schedule. Examples of valid schedules include: `1st,3rd monday of month 15:30`, `every wed,fri of jan,jun 13:15`, and `first sunday of quarter 00:00`. |
| `supportsCustomSchedule` | `boolean`  Specifies whether the data source supports a user defined schedule, or operates on the default schedule. When set to `true`, user can override default schedule. |
| `parameters[]` | `object (DataSourceParameter)`  Data source parameters. |
| `helpUrl` | `string`  Url for the help document for this data source. |
| `authorizationType` | `enum (AuthorizationType)`  Indicates the type of authorization. |
| `dataRefreshType` | `enum (DataRefreshType)`  Specifies whether the data source supports automatic data refresh for the past few days, and how it's supported. For some data sources, data might not be complete until a few days later, so it's useful to refresh data automatically. |
| `defaultDataRefreshWindowDays` | `integer`  Default data refresh window on days. Only meaningful when `dataRefreshType` = `SLIDING_WINDOW`. |
| `manualRunsDisabled` | `boolean`  Disables backfilling and manual run scheduling for the data source. |
| `minimumScheduleInterval` | `string (Duration format)`  The minimum interval for scheduler to schedule runs.  A duration in seconds with up to nine fractional digits, ending with '`s`'. Example: `"3.5s"`. |

### TransferType

This item is deprecated!

DEPRECATED. Represents data transfer type.

| Enums | |
| --- | --- |
| `TRANSFER_TYPE_UNSPECIFIED` | Invalid or Unknown transfer type placeholder. |
| `BATCH` | Batch data transfer. |
| `STREAMING` | Streaming data transfer. Streaming data source currently doesn't support multiple transfer configs per project. |

### DataSourceParameter

A parameter used to define custom fields in a data source definition.

| JSON representation |
| --- |
| ``` {   "paramId": string,   "displayName": string,   "description": string,   "type": enum (Type),   "required": boolean,   "repeated": boolean,   "validationRegex": string,   "allowedValues": [     string   ],   "minValue": number,   "maxValue": number,   "fields": [     {       object (DataSourceParameter)     }   ],   "validationDescription": string,   "validationHelpUrl": string,   "immutable": boolean,   "recurse": boolean,   "deprecated": boolean,   "maxListSize": string } ``` |

| Fields | |
| --- | --- |
| `paramId` | `string`  Parameter identifier. |
| `displayName` | `string`  Parameter display name in the user interface. |
| `description` | `string`  Parameter description. |
| `type` | `enum (Type)`  Parameter type. |
| `required` | `boolean`  Is parameter required. |
| `repeated` | `boolean`  Deprecated. This field has no effect. |
| `validationRegex` | `string`  Regular expression which can be used for parameter validation. |
| `allowedValues[]` | `string`  All possible values for the parameter. |
| `minValue` | `number`  For integer and double values specifies minimum allowed value. |
| `maxValue` | `number`  For integer and double values specifies maximum allowed value. |
| `fields[]` | `object (DataSourceParameter)`  Deprecated. This field has no effect. |
| `validationDescription` | `string`  Description of the requirements for this field, in case the user input does not fulfill the regex pattern or min/max values. |
| `validationHelpUrl` | `string`  URL to a help document to further explain the naming requirements. |
| `immutable` | `boolean`  Cannot be changed after initial creation. |
| `recurse` | `boolean`  Deprecated. This field has no effect. |
| `deprecated` | `boolean`  If true, it should not be used in new transfers, and it should not be visible to users. |
| `maxListSize` | `string (int64 format)`  For list parameters, the max size of the list. |

### Type

Parameter type.

| Enums | |
| --- | --- |
| `TYPE_UNSPECIFIED` | Type unspecified. |
| `STRING` | String parameter. |
| `INTEGER` | Integer parameter (64-bits). Will be serialized to json as string. |
| `DOUBLE` | Double precision floating point parameter. |
| `BOOLEAN` | Boolean parameter. |
| `RECORD` | Deprecated. This field has no effect. |
| `PLUS_PAGE` | Page ID for a Google+ Page. |
| `LIST` | List of strings parameter. |

### AuthorizationType

The type of authorization needed for this data source.

| Enums | |
| --- | --- |
| `AUTHORIZATION_TYPE_UNSPECIFIED` | Type unspecified. |
| `AUTHORIZATION_CODE` | Use OAuth 2 authorization codes that can be exchanged for a refresh token on the backend. |
| `GOOGLE_PLUS_AUTHORIZATION_CODE` | Return an authorization code for a given Google+ page that can then be exchanged for a refresh token on the backend. |
| `FIRST_PARTY_OAUTH` | Use First Party OAuth. |

### DataRefreshType

Represents how the data source supports data auto refresh.

| Enums | |
| --- | --- |
| `DATA_REFRESH_TYPE_UNSPECIFIED` | The data source won't support data auto refresh, which is default value. |
| `SLIDING_WINDOW` | The data source supports data auto refresh, and runs will be scheduled for the past few days. Does not allow custom values to be set for each transfer config. |
| `CUSTOM_SLIDING_WINDOW` | The data source supports data auto refresh, and runs will be scheduled for the past few days. Allows custom values to be set for each transfer config. |

| Methods | |
| --- | --- |
| `checkValidCreds` | Returns true if valid credentials exist for the given data source and requesting user. |
| `get` | Retrieves a supported data source and returns its settings. |
| `list` | Lists supported data sources and returns their settings. |




Send feedback

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2025-08-13 UTC.




Need to tell us more?

[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Hard to understand","hardToUnderstand","thumb-down"],["Incorrect information or sample code","incorrectInformationOrSampleCode","thumb-down"],["Missing the information/samples I need","missingTheInformationSamplesINeed","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2025-08-13 UTC."],[],[]]