As of April 20th, 2026, BigLake is now called Lakehouse for Apache Iceberg. BigLake metastore is now called the Lakehouse runtime catalog. Lakehouse APIs, client libraries, CLI commands, and IAM names remain unchanged and still reference BigLake.

* [Home](https://docs.cloud.google.com/)
* [BigLake API](https://docs.cloud.google.com/lakehouse/docs)

# ResourceInfo Stay organized with collections Save and categorize content based on your preferences.

* [JSON representation](#SCHEMA_REPRESENTATION)
* [Resource](#Resource)
  + [JSON representation](#Resource.SCHEMA_REPRESENTATION)
* [FederatedResourceHierarchy](#FederatedResourceHierarchy)
  + [JSON representation](#FederatedResourceHierarchy.SCHEMA_REPRESENTATION)
* [FederatedResource](#FederatedResource)
  + [JSON representation](#FederatedResource.SCHEMA_REPRESENTATION)
* [PolicyName](#PolicyName)
  + [JSON representation](#PolicyName.SCHEMA_REPRESENTATION)
* [FederatedGrantPolicy](#FederatedGrantPolicy)
  + [JSON representation](#FederatedGrantPolicy.SCHEMA_REPRESENTATION)
* [VisibleReferences](#VisibleReferences)
  + [JSON representation](#VisibleReferences.SCHEMA_REPRESENTATION)
* [FederatedTags](#FederatedTags)
  + [JSON representation](#FederatedTags.SCHEMA_REPRESENTATION)

Contains IAM resource information.

| JSON representation |
| --- |
| ``` {   "policyType": string,   "policyName": string,   "policyRegion": string,   "resourceContainer": string,   "resource": {     object (Resource)   },   "monitoredResource": {     object (MonitoredResource)   },   "permissions": [     string   ],   "nextExpectedResourceState": {     "@type": string,     field1: ...,     ...   },   "federatedResourceHierarchy": {     object (FederatedResourceHierarchy)   },   "targetResourceLocations": [     string   ] } ``` |

| Fields | |
| --- | --- |
| `policyType` | `string`  OPTIONAL: the resource's policy type. Valid values for policyType might be 'compute\_instances', 'storage\_buckets', 'resourcemanager\_projects', etc. |
| `policyName` | `string`  OPTIONAL: the resource's policy name. Valid values for policyName might be '/myproject/myinstance', '/myproject/mybucket', '/myproject', etc. |
| `policyRegion` | `string`  OPTIONAL: the location of the policy. |
| `resourceContainer` | `string`  OPTIONAL: the resource container name. This can be in one of the following formats: - “projects/” - “folders/” - “organizations/” |
| `resource` | `object (Resource)`  OPTIONAL: The core attributes for a resource. |
| `monitoredResource` | `object (MonitoredResource)`  OPTIONAL: the cloud audit monitored resource. |
| `permissions[]` | `string`  OPTIONAL: the list of the IAM permission names intended to be checked in the format: {serviceName}/{plural}.{verb} or the legacy format: {serviceName}.{plural}.{verb}.   * {serviceName} references the service that owns the resource. * {plural} references the `plural` field of this resource. It must be lowerCamelCase.   Example: ["library.googleapis.com/shelves.get", "library.googleapis.com/shelves.update", "library.shelves.get", "library.shelves.update"] |
| `nextExpectedResourceState` | `object`  **Optional.** The expected view of the resource after performing a mutation.  Example: A `CreateBookRequest` might look like the following: { parent: "projects/project-123" book { author: "Someone Famous" title: "This is a Title" read: false } book\_id: "book-123" }  `nextExpectedResourceState` might be: { name: "projects/project-123/books/book-123" author: "Someone Famous" title: "This is a Title" }  An object containing fields of an arbitrary type. An additional field `"@type"` contains a URI identifying the type. Example: `{ "id": 1234, "@type": "types.example.com/standard/id" }`. |
| `federatedResourceHierarchy` | `object (FederatedResourceHierarchy)`  OPTIONAL: federated resource hierarchy for IAM policy federation. |
| `targetResourceLocations[]` | `string`  OPTIONAL: The locations of the target resource. The operation owner can specify the target locations as either a deduplicated array of GCP region names or ["global"]. Note: no support for multiregion names. |

## Resource

This message defines core attributes for a resource. A resource is an addressable (named) entity provided by the destination service. For example, a file stored on a network storage service.

| JSON representation |
| --- |
| ``` {   "service": string,   "name": string,   "type": string,   "labels": {     string: string,     ...   },   "uid": string,   "annotations": {     string: string,     ...   },   "displayName": string,   "createTime": string,   "updateTime": string,   "deleteTime": string,   "etag": string,   "location": string } ``` |

| Fields | |
| --- | --- |
| `service` | `string`  The name of the service that this resource belongs to, such as `pubsub.googleapis.com`. The service may be different from the DNS hostname that actually serves the request. |
| `name` | `string`  The stable identifier (name) of a resource on the `service`. A resource can be logically identified as "//{resource.service}/{resource.name}". The differences between a resource name and a URI are:   * Resource name is a logical identifier, independent of network protocol and API version. For example, `//pubsub.googleapis.com/projects/123/topics/news-feed`. * URI often includes protocol and version information, so it can be used directly by applications. For example, `https://pubsub.googleapis.com/v1/projects/123/topics/news-feed`.   See <https://cloud.google.com/apis/design/resource_names> for details. |
| `type` | `string`  The type of the resource. The syntax is platform-specific because different platforms define their resources differently.  For Google APIs, the type format must be "{service}/{kind}", such as "pubsub.googleapis.com/Topic". |
| `labels` | `map (key: string, value: string)`  The labels or tags on the resource, such as AWS resource tags and Kubernetes resource labels.  An object containing a list of `"key": value` pairs. Example: `{ "name": "wrench", "mass": "1.3kg", "count": "3" }`. |
| `uid` | `string`  The unique identifier of the resource. UID is unique in the time and space for this resource within the scope of the service. It is typically generated by the server on successful creation of a resource and must not be changed. UID is used to uniquely identify resources with resource name reuses. This should be a UUID4. |
| `annotations` | `map (key: string, value: string)`  Annotations is an unstructured key-value map stored with a resource that may be set by external tools to store and retrieve arbitrary metadata. They are not queryable and should be preserved when modifying objects.  More info: <https://kubernetes.io/docs/concepts/overview/working-with-objects/annotations/>  An object containing a list of `"key": value` pairs. Example: `{ "name": "wrench", "mass": "1.3kg", "count": "3" }`. |
| `displayName` | `string`  Mutable. The display name set by clients. Must be <= 63 characters. |
| `createTime` | `string (Timestamp format)`  Output only. The timestamp when the resource was created. This may be either the time creation was initiated or when it was completed.  Uses RFC 3339, where generated output will always be Z-normalized and use 0, 3, 6 or 9 fractional digits. Offsets other than "Z" are also accepted. Examples: `"2014-10-02T15:01:23Z"`, `"2014-10-02T15:01:23.045123456Z"` or `"2014-10-02T15:01:23+05:30"`. |
| `updateTime` | `string (Timestamp format)`  Output only. The timestamp when the resource was last updated. Any change to the resource made by users must refresh this value. Changes to a resource made by the service should refresh this value.  Uses RFC 3339, where generated output will always be Z-normalized and use 0, 3, 6 or 9 fractional digits. Offsets other than "Z" are also accepted. Examples: `"2014-10-02T15:01:23Z"`, `"2014-10-02T15:01:23.045123456Z"` or `"2014-10-02T15:01:23+05:30"`. |
| `deleteTime` | `string (Timestamp format)`  Output only. The timestamp when the resource was deleted. If the resource is not deleted, this must be empty.  Uses RFC 3339, where generated output will always be Z-normalized and use 0, 3, 6 or 9 fractional digits. Offsets other than "Z" are also accepted. Examples: `"2014-10-02T15:01:23Z"`, `"2014-10-02T15:01:23.045123456Z"` or `"2014-10-02T15:01:23+05:30"`. |
| `etag` | `string`  Output only. An opaque value that uniquely identifies a version or generation of a resource. It can be used to confirm that the client and server agree on the ordering of a resource being written. |
| `location` | `string`  Immutable. The location of the resource. The location encoding is specific to the service provider, and new encoding may be introduced as the service evolves.  For Google Cloud products, the encoding is what is used by Google Cloud APIs, such as `us-east1`, `aws-us-east-1`, and `azure-eastus2`. The semantics of `location` is identical to the `cloud.googleapis.com/location` label used by some Google Cloud APIs. |

## FederatedResourceHierarchy

| JSON representation |
| --- |
| ``` {   "version": integer,   "federatedHierarchy": [     {       object (FederatedResource)     }   ],   "nonFederatedParent": {     object (PolicyName)   } } ``` |

| Fields | |
| --- | --- |
| `version` | `integer`  Specifies the format of this federated hierarchy. Valid values are `0` or `1`. Requests that specify an invalid value are rejected.  This field indicates which federated attributes the client is aware of. Any attributes the client is aware of must have a non-default value set. Any attributes the client is not aware of are considered NOT\_FEDERATED. For a given version the client must be aware of all attributes at and below that version.     ```              +----------+----------------------+              | Version  | Supported Attributes |              +----------+----------------------+              | 0        | grant policies, tags |              +----------+----------------------+              | 1        | grant policies, tags |              +----------+----------------------+ ```   Note: there is no difference between versions 0 and 1. Prefer using 1. |
| `federatedHierarchy[]` | `object (FederatedResource)`  In-order, starting at the leaf node, attributes of resources in this request which have federated information. The policy name of the leaf node name must match the base PolicyName for the resource in the request - CheckPolicyRequest.name, BulkCheckPolicyRequest.requests.name, etc. This list can have at most 15 entries. |
| `nonFederatedParent` | `object (PolicyName)`  Policy name of the nearest ancestor resource that has centrally stored policy and attributes. |

## FederatedResource

| JSON representation |
| --- |
| ``` {   "policyName": {     object (PolicyName)   },   "resourceName": string,    // Union field grant_policy can be only one of the following:   "grantPolicyStatus": enum (FederatedAttributeStatus),   "federatedGrantPolicy": {     object (FederatedGrantPolicy)   }   // End of list of possible types for union field grant_policy.    // Union field tags can be only one of the following:   "tagsStatus": enum (FederatedAttributeStatus),   "federatedTags": {     object (FederatedTags)   }   // End of list of possible types for union field tags. } ``` |

| Fields | |
| --- | --- |
| `policyName` | `object (PolicyName)` |
| `resourceName` | `string`  The relative resource name, not including the / prefix (e.g., "projects/project-id"). See: <https://cloud.google.com/apis/design/resource_names#relative_resource_name>  This field is used for Credential Access Boundaries (CAB) to match the CAB Rule's "availableResource". See <https://cloud.google.com/iam/docs/downscoping-short-lived-credentials> |
| Union field `grant_policy`.  `grant_policy` can be only one of the following: | |
| `grantPolicyStatus` | `enum (FederatedAttributeStatus)` |
| `federatedGrantPolicy` | `object (FederatedGrantPolicy)` |
| Union field `tags`.  `tags` can be only one of the following: | |
| `tagsStatus` | `enum (FederatedAttributeStatus)` |
| `federatedTags` | `object (FederatedTags)` |

## PolicyName

An internal name for an IAM policy, based on the resource to which the policy applies. Not to be confused with a resource's external full resource name. For more information on this distinction.

| JSON representation |
| --- |
| ``` {   "type": string,   "id": string,   "region": string } ``` |

| Fields | |
| --- | --- |
| `type` | `string`  Resource type. Types are defined in IAM's .service files. Valid values for type might be 'storage\_buckets', 'compute\_instances', 'resourcemanager\_customers', 'billing\_accounts', etc. |
| `id` | `string`  Identifies an instance of the type. ID format varies by type. The ID format is defined in the IAM .service file that defines the type, either in path\_mapping or in a comment. |
| `region` | `string`  For Cloud IAM: The location of the Policy. Must be empty or "global" for Policies owned by global IAM. Must name a region from prodspec/cloud-iam-cloudspec for Regional IAM Policies.  For Local IAM: This field should be set to "local". |

## FederatedGrantPolicy

Caller-provided federated grant policy. These values will be used in place of stored policies during CheckPolicy evaluation. Guaranteed to be at most 257 KiB. Raising this limit requires review from services integrated with IAM federation.

| JSON representation |
| --- |
| ``` {   "version": integer,   "policyData": {     "@type": string,     field1: ...,     ...   },   "visibleReferences": {     object (VisibleReferences)   },   "sha256": string } ``` |

| Fields | |
| --- | --- |
| `version` | `integer`  Schema version of this policy object. Any breaking changes to the federated policy schema will result in the version number being incremented. Valid version numbers are: 1: initial version Any other value will result in an invalid argument error. |
| `policyData` | `object`  IAM specific data storing the policy contents. Federated teams should not make assumptions on contents or size of the policy data without approval from IAM. The policy data should not be read or modified outside of IAM owned code.  An object containing fields of an arbitrary type. An additional field `"@type"` contains a URI identifying the type. Example: `{ "id": 1234, "@type": "types.example.com/standard/id" }`. |
| `visibleReferences` | `object (VisibleReferences)` |
| `sha256` | `string (bytes format)`  Hash of the policyData for caching. The same policy on different resources is expected to have the same hash.  A base64-encoded string. |

## VisibleReferences

Principals or other entities that are referenced in the policy. If any of these entities are deleted, the policy should be sent to IAM for cleanup. Entries for each field won't be repeated, but may not be sorted.

| JSON representation |
| --- |
| ``` {   "gaiaIds": [     string   ],   "customRoles": [     string   ],   "cpis": [     string   ],   "projectNumbers": [     string   ] } ``` |

| Fields | |
| --- | --- |
| `gaiaIds[]` | `string (int64 format)` |
| `customRoles[]` | `string`  Custom role name as used in policy. For example: organizations/1234/roles/myRole. |
| `cpis[]` | `string` |
| `projectNumbers[]` | `string (int64 format)`  Project number of projectOwner, projectEditor and projectViewer |

## FederatedTags

A wrapper for a map of tag key/value pairs, because maps cannot be a field in a oneof. Not supported for GCP Service usage yet.

| JSON representation |
| --- |
| ``` {   "tags": {     string: string,     ...   } } ``` |

| Fields | |
| --- | --- |
| `tags` | `map (key: string, value: string)`  An object containing a list of `"key": value` pairs. Example: `{ "name": "wrench", "mass": "1.3kg", "count": "3" }`. |

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2026-04-21 UTC.




[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Hard to understand","hardToUnderstand","thumb-down"],["Incorrect information or sample code","incorrectInformationOrSampleCode","thumb-down"],["Missing the information/samples I need","missingTheInformationSamplesINeed","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2026-04-21 UTC."],[],[]]