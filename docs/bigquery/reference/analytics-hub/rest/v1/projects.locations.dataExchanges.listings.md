* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback

# REST Resource: projects.locations.dataExchanges.listings Stay organized with collections Save and categorize content based on your preferences.

* [Resource: Listing](#Listing)
  + [JSON representation](#Listing.SCHEMA_REPRESENTATION)
* [BigQueryDatasetSource](#BigQueryDatasetSource)
  + [JSON representation](#BigQueryDatasetSource.SCHEMA_REPRESENTATION)
* [SelectedResource](#SelectedResource)
  + [JSON representation](#SelectedResource.SCHEMA_REPRESENTATION)
* [RestrictedExportPolicy](#RestrictedExportPolicy)
  + [JSON representation](#RestrictedExportPolicy.SCHEMA_REPRESENTATION)
* [Replica](#Replica)
  + [JSON representation](#Replica.SCHEMA_REPRESENTATION)
* [ReplicaState](#ReplicaState)
* [PrimaryState](#PrimaryState)
* [PubSubTopicSource](#PubSubTopicSource)
  + [JSON representation](#PubSubTopicSource.SCHEMA_REPRESENTATION)
* [State](#State)
* [DataProvider](#DataProvider)
  + [JSON representation](#DataProvider.SCHEMA_REPRESENTATION)
* [Category](#Category)
* [Publisher](#Publisher)
  + [JSON representation](#Publisher.SCHEMA_REPRESENTATION)
* [RestrictedExportConfig](#RestrictedExportConfig)
  + [JSON representation](#RestrictedExportConfig.SCHEMA_REPRESENTATION)
* [StoredProcedureConfig](#StoredProcedureConfig)
  + [JSON representation](#StoredProcedureConfig.SCHEMA_REPRESENTATION)
* [StoredProcedureType](#StoredProcedureType)
* [CommercialInfo](#CommercialInfo)
  + [JSON representation](#CommercialInfo.SCHEMA_REPRESENTATION)
* [GoogleCloudMarketplaceInfo](#GoogleCloudMarketplaceInfo)
  + [JSON representation](#GoogleCloudMarketplaceInfo.SCHEMA_REPRESENTATION)
* [CommercialState](#CommercialState)
* [Methods](#METHODS_SUMMARY)

## Resource: Listing

A listing is what gets published into a data exchange that a subscriber can subscribe to. It contains a reference to the data source along with descriptive information that will help subscribers find and subscribe the data.

| JSON representation |
| --- |
| ``` {   "name": string,   "displayName": string,   "description": string,   "primaryContact": string,   "documentation": string,   "state": enum (State),   "icon": string,   "dataProvider": {     object (DataProvider)   },   "categories": [     enum (Category)   ],   "publisher": {     object (Publisher)   },   "requestAccess": string,   "restrictedExportConfig": {     object (RestrictedExportConfig)   },   "storedProcedureConfig": {     object (StoredProcedureConfig)   },   "resourceType": enum (SharedResourceType),    // The following is a list of mutually exclusive fields. At most one of the   // fields will be set in a response:   "bigqueryDataset": {     object (BigQueryDatasetSource)   },   "pubsubTopic": {     object (PubSubTopicSource)   }   // End of mutually exclusive fields.   "discoveryType": enum (DiscoveryType),   "commercialInfo": {     object (CommercialInfo)   },   "logLinkedDatasetQueryUserEmail": boolean,   "allowOnlyMetadataSharing": boolean } ``` |

| Fields | |
| --- | --- |
| `name` | `string`  Output only. The resource name of the listing. e.g. `projects/myproject/locations/us/dataExchanges/123/listings/456` |
| `displayName` | `string`  Required. Human-readable display name of the listing. The display name must contain only Unicode letters, numbers (0-9), underscores (\_), dashes (-), spaces ( ), ampersands (&) and can't start or end with spaces. Default value is an empty string. Max length: 63 bytes. |
| `description` | `string`  Optional. Short description of the listing. The description must not contain Unicode non-characters and C0 and C1 control codes except tabs (HT), new lines (LF), carriage returns (CR), and page breaks (FF). Default value is an empty string. Max length: 2000 bytes. |
| `primaryContact` | `string`  Optional. Email or URL of the primary point of contact of the listing. Max Length: 1000 bytes. |
| `documentation` | `string`  Optional. Documentation describing the listing. |
| `state` | `enum (State)`  Output only. Current state of the listing. |
| `icon` | `string (bytes format)`  Optional. Base64 encoded image representing the listing. Max Size: 3.0MiB Expected image dimensions are 512x512 pixels, however the API only performs validation on size of the encoded data. Note: For byte fields, the contents of the field are base64-encoded (which increases the size of the data by 33-36%) when using JSON on the wire.  A base64-encoded string. |
| `dataProvider` | `object (DataProvider)`  Optional. Details of the data provider who owns the source data. |
| `categories[]` | `enum (Category)`  Optional. Categories of the listing. Up to five categories are allowed. |
| `publisher` | `object (Publisher)`  Optional. Details of the publisher who owns the listing and who can share the source data. |
| `requestAccess` | `string`  Optional. Email or URL of the request access of the listing. Subscribers can use this reference to request access. Max Length: 1000 bytes. |
| `restrictedExportConfig` | `object (RestrictedExportConfig)`  Optional. If set, restricted export configuration will be propagated and enforced on the linked dataset. |
| `storedProcedureConfig` | `object (StoredProcedureConfig)`  Optional. If set, stored procedure configuration will be propagated and enforced on the linked dataset. |
| `resourceType` | `enum (SharedResourceType)`  Output only. Listing shared asset type. |
| Listing source. The following is a list of mutually exclusive fields. At most one of the fields will be set in a response: | |
| `bigqueryDataset` | `object (BigQueryDatasetSource)`  Shared dataset i.e. BigQuery dataset source. |
| `pubsubTopic` | `object (PubSubTopicSource)`  Pub/Sub topic source. |
| End of mutually exclusive fields. | |
| `discoveryType` | `enum (DiscoveryType)`  Optional. Type of discovery of the listing on the discovery page. |
| `commercialInfo` | `object (CommercialInfo)`  Output only. Commercial info contains the information about the commercial data products associated with the listing. |
| `logLinkedDatasetQueryUserEmail` | `boolean`  Optional. By default, false. If true, the Listing has an email sharing mandate enabled. |
| `allowOnlyMetadataSharing` | `boolean`  Optional. If true, the listing is only available to get the resource metadata. Listing is non subscribable. |

## BigQueryDatasetSource

A reference to a shared dataset. It is an existing BigQuery dataset with a collection of objects such as tables and views that you want to share with subscribers. When subscriber's subscribe to a listing, Analytics Hub creates a linked dataset in the subscriber's project. A Linked dataset is an opaque, read-only BigQuery dataset that serves as a *symbolic link* to a shared dataset.

| JSON representation |
| --- |
| ``` {   "dataset": string,   "selectedResources": [     {       object (SelectedResource)     }   ],   "restrictedExportPolicy": {     object (RestrictedExportPolicy)   },   "replicaLocations": [     string   ],   "effectiveReplicas": [     {       object (Replica)     }   ] } ``` |

| Fields | |
| --- | --- |
| `dataset` | `string`  Optional. Resource name of the dataset source for this listing. e.g. `projects/myproject/datasets/123` |
| `selectedResources[]` | `object (SelectedResource)`  Optional. Resource in this dataset that is selectively shared. This field is required for data clean room exchanges. |
| `restrictedExportPolicy` | `object (RestrictedExportPolicy)`  Optional. If set, restricted export policy will be propagated and enforced on the linked dataset. |
| `replicaLocations[]` | `string`  Optional. A list of regions where the publisher has created shared dataset replicas. |
| `effectiveReplicas[]` | `object (Replica)`  Output only. Server-owned effective state of replicas. Contains both primary and secondary replicas. Each replica includes a system-computed (output-only) state and primary designation. |

## SelectedResource

Resource in this dataset that is selectively shared.

| JSON representation |
| --- |
| ``` {    // The following is a list of mutually exclusive fields. At most one of the   // fields will be set in a response:   "table": string,   "routine": string   // End of mutually exclusive fields. } ``` |

| Fields | |
| --- | --- |
| The following is a list of mutually exclusive fields. At most one of the fields will be set in a response: | |
| `table` | `string`  Optional. Format: For table: `projects/{projectId}/datasets/{datasetId}/tables/{tableId}` Example:"projects/test\_project/datasets/test\_dataset/tables/test\_table" |
| `routine` | `string`  Optional. Format: For routine: `projects/{projectId}/datasets/{datasetId}/routines/{routineId}` Example:"projects/test\_project/datasets/test\_dataset/routines/test\_routine" |
| End of mutually exclusive fields. | |

## RestrictedExportPolicy

Restricted export policy used to configure restricted export on linked dataset.

| JSON representation |
| --- |
| ``` {   "enabled": boolean,   "restrictDirectTableAccess": boolean,   "restrictQueryResult": boolean } ``` |

| Fields | |
| --- | --- |
| `enabled` | `boolean`  Optional. If true, enable restricted export. |
| `restrictDirectTableAccess` | `boolean`  Optional. If true, restrict direct table access (read api/tabledata.list) on linked table. |
| `restrictQueryResult` | `boolean`  Optional. If true, restrict export of query result derived from restricted linked dataset table. |

## Replica

Represents the state of a replica of a shared dataset. It includes the geographic location of the replica and system-computed, output-only fields indicating its replication state and whether it is the primary replica.

| JSON representation |
| --- |
| ``` {   "location": string,   "replicaState": enum (ReplicaState),   "primaryState": enum (PrimaryState) } ``` |

| Fields | |
| --- | --- |
| `location` | `string`  Output only. The geographic location where the replica resides. See [BigQuery locations](https://cloud.google.com/bigquery/docs/locations) for supported locations. Eg. "us-central1". |
| `replicaState` | `enum (ReplicaState)`  Output only. Assigned by Analytics Hub based on real BigQuery replication state. |
| `primaryState` | `enum (PrimaryState)`  Output only. Indicates that this replica is the primary replica. |

## ReplicaState

Replica state of the shared dataset.

| Enums | |
| --- | --- |
| `REPLICA_STATE_UNSPECIFIED` | Default value. This value is unused. |
| `READY_TO_USE` | The replica is backfilled and ready to use. |
| `UNAVAILABLE` | The replica is unavailable, does not exist, or has not been backfilled yet. |

## PrimaryState

Primary state of the replica. Set only for the primary replica.

| Enums | |
| --- | --- |
| `PRIMARY_STATE_UNSPECIFIED` | Default value. This value is unused. |