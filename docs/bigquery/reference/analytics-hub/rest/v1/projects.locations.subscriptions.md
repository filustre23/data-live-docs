* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback

# REST Resource: projects.locations.subscriptions Stay organized with collections Save and categorize content based on your preferences.

* [Resource: Subscription](#Subscription)
  + [JSON representation](#Subscription.SCHEMA_REPRESENTATION)
* [Methods](#METHODS_SUMMARY)

## Resource: Subscription

A subscription represents a subscribers' access to a particular set of published data. It contains references to associated listings, data exchanges, and linked datasets.

| JSON representation |
| --- |
| ``` {   "name": string,   "creationTime": string,   "lastModifyTime": string,   "organizationId": string,   "organizationDisplayName": string,   "state": enum (State),   "linkedDatasetMap": {     string: {       object (LinkedResource)     },     ...   },   "subscriberContact": string,   "linkedResources": [     {       object (LinkedResource)     }   ],   "resourceType": enum (SharedResourceType),   "commercialInfo": {     object (CommercialInfo)   },   "destinationDataset": {     object (DestinationDataset)   },    // Union field resource_name can be only one of the following:   "listing": string,   "dataExchange": string   // End of list of possible types for union field resource_name.   "logLinkedDatasetQueryUserEmail": boolean } ``` |

| Fields | |
| --- | --- |
| `name` | `string`  Output only. The resource name of the subscription. e.g. `projects/myproject/locations/us/subscriptions/123`. |
| `creationTime` | `string (Timestamp format)`  Output only. Timestamp when the subscription was created.  Uses RFC 3339, where generated output will always be Z-normalized and use 0, 3, 6 or 9 fractional digits. Offsets other than "Z" are also accepted. Examples: `"2014-10-02T15:01:23Z"`, `"2014-10-02T15:01:23.045123456Z"` or `"2014-10-02T15:01:23+05:30"`. |
| `lastModifyTime` | `string (Timestamp format)`  Output only. Timestamp when the subscription was last modified.  Uses RFC 3339, where generated output will always be Z-normalized and use 0, 3, 6 or 9 fractional digits. Offsets other than "Z" are also accepted. Examples: `"2014-10-02T15:01:23Z"`, `"2014-10-02T15:01:23.045123456Z"` or `"2014-10-02T15:01:23+05:30"`. |
| `organizationId` | `string`  Output only. Organization of the project this subscription belongs to. |
| `organizationDisplayName` | `string`  Output only. Display name of the project of this subscription. |
| `state` | `enum (State)`  Output only. Current state of the subscription. |
| `linkedDatasetMap` | `map (key: string, value: object (LinkedResource))`  Output only. Map of listing resource names to associated linked resource, e.g. projects/123/locations/us/dataExchanges/456/listings/789 -> projects/123/datasets/my\_dataset  For listing-level subscriptions, this is a map of size 1. Only contains values if state == STATE\_ACTIVE.  An object containing a list of `"key": value` pairs. Example: `{ "name": "wrench", "mass": "1.3kg", "count": "3" }`. |
| `subscriberContact` | `string`  Output only. Email of the subscriber. |
| `linkedResources[]` | `object (LinkedResource)`  Output only. Linked resources created in the subscription. Only contains values if state = STATE\_ACTIVE. |
| `resourceType` | `enum (SharedResourceType)`  Output only. Listing shared asset type. |
| `commercialInfo` | `object (CommercialInfo)`  Output only. This is set if this is a commercial subscription i.e. if this subscription was created from subscribing to a commercial listing. |
| `destinationDataset` | `object (DestinationDataset)`  Optional. BigQuery destination dataset to create for the subscriber. |
| Union field `resource_name`.  `resource_name` can be only one of the following: | |
| `listing` | `string`  Output only. Resource name of the source Listing. e.g. projects/123/locations/us/dataExchanges/456/listings/789 |
| `dataExchange` | `string`  Output only. Resource name of the source Data Exchange. e.g. projects/123/locations/us/dataExchanges/456 |
| `logLinkedDatasetQueryUserEmail` | `boolean`  Output only. By default, false. If true, the Subscriber agreed to the email sharing mandate that is enabled for DataExchange/Listing. |

| Methods | |
| --- | --- |
| `delete` | Deletes a subscription. |
| `get` | Gets the details of a Subscription. |
| `getIamPolicy` | Gets the IAM policy. |
| `list` | Lists all subscriptions in a given project and location. |
| `refresh` | Refreshes a Subscription to a Data Exchange. |
| `revoke` | Revokes a given subscription. |
| `setIamPolicy` | Sets the IAM policy. |




Send feedback

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2025-11-12 UTC.




Need to tell us more?

[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Hard to understand","hardToUnderstand","thumb-down"],["Incorrect information or sample code","incorrectInformationOrSampleCode","thumb-down"],["Missing the information/samples I need","missingTheInformationSamplesINeed","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2025-11-12 UTC."],[],[]]