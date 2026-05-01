* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback

# REST Resource: projects.locations.reservations Stay organized with collections Save and categorize content based on your preferences.

* [Resource: Reservation](#Reservation)
  + [JSON representation](#Reservation.SCHEMA_REPRESENTATION)
* [Autoscale](#Autoscale)
  + [JSON representation](#Autoscale.SCHEMA_REPRESENTATION)
* [ScalingMode](#ScalingMode)
* [ReplicationStatus](#ReplicationStatus)
  + [JSON representation](#ReplicationStatus.SCHEMA_REPRESENTATION)
* [Methods](#METHODS_SUMMARY)

## Resource: Reservation

A reservation is a mechanism used to guarantee slots to users.

| JSON representation |
| --- |
| ``` {   "name": string,   "slotCapacity": string,   "ignoreIdleSlots": boolean,   "autoscale": {     object (Autoscale)   },   "concurrency": string,   "creationTime": string,   "updateTime": string,   "edition": enum (Edition),   "primaryLocation": string,   "secondaryLocation": string,   "originalPrimaryLocation": string,   "scalingMode": enum (ScalingMode),   "reservationGroup": string,   "replicationStatus": {     object (ReplicationStatus)   },   "maxSlots": string } ``` |

| Fields | |
| --- | --- |
| `name` | `string`  Identifier. The resource name of the reservation, e.g., `projects/*/locations/*/reservations/team1-prod`. The reservationId must only contain lower case alphanumeric characters or dashes. It must start with a letter and must not end with a dash. Its maximum length is 64 characters. |
| `slotCapacity` | `string (int64 format)`  Optional. Baseline slots available to this reservation. A slot is a unit of computational power in BigQuery, and serves as the unit of parallelism.  Queries using this reservation might use more slots during runtime if ignoreIdleSlots is set to false, or autoscaling is enabled.  The total slotCapacity of the reservation and its siblings may exceed the total slotCount of capacity commitments. In that case, the exceeding slots will be charged with the autoscale SKU. You can increase the number of baseline slots in a reservation every few minutes. If you want to decrease your baseline slots, you are limited to once an hour if you have recently changed your baseline slot capacity and your baseline slots exceed your committed slots. Otherwise, you can decrease your baseline slots every few minutes. |
| `ignoreIdleSlots` | `boolean`  Optional. If false, any query or pipeline job using this reservation will use idle slots from other reservations within the same admin project. If true, a query or pipeline job using this reservation will execute with the slot capacity specified in the slotCapacity field at most. |
| `autoscale` | `object (Autoscale)`  Optional. The configuration parameters for the auto scaling feature. |
| `concurrency` | `string (int64 format)`  Optional. Job concurrency target which sets a soft upper bound on the number of jobs that can run concurrently in this reservation. This is a soft target due to asynchronous nature of the system and various optimizations for small queries. Default value is 0 which means that concurrency target will be automatically computed by the system. NOTE: this field is exposed as target job concurrency in the Information Schema, DDL and BigQuery CLI. |
| `creationTime` | `string (Timestamp format)`  Output only. Creation time of the reservation.  Uses RFC 3339, where generated output will always be Z-normalized and use 0, 3, 6 or 9 fractional digits. Offsets other than "Z" are also accepted. Examples: `"2014-10-02T15:01:23Z"`, `"2014-10-02T15:01:23.045123456Z"` or `"2014-10-02T15:01:23+05:30"`. |
| `updateTime` | `string (Timestamp format)`  Output only. Last update time of the reservation.  Uses RFC 3339, where generated output will always be Z-normalized and use 0, 3, 6 or 9 fractional digits. Offsets other than "Z" are also accepted. Examples: `"2014-10-02T15:01:23Z"`, `"2014-10-02T15:01:23.045123456Z"` or `"2014-10-02T15:01:23+05:30"`. |
| `edition` | `enum (Edition)`  Optional. Edition of the reservation. |
| `primaryLocation` | `string`  Output only. The current location of the reservation's primary replica. This field is only set for reservations using the managed disaster recovery feature. |
| `secondaryLocation` | `string`  Optional. The current location of the reservation's secondary replica. This field is only set for reservations using the managed disaster recovery feature. Users can set this in create reservation calls to create a failover reservation or in update reservation calls to convert a non-failover reservation to a failover reservation(or vice versa). |
| `originalPrimaryLocation` | `string`  Output only. The location where the reservation was originally created. This is set only during the failover reservation's creation. All billing charges for the failover reservation will be applied to this location. |
| `scalingMode` | `enum (ScalingMode)`  Optional. The scaling mode for the reservation. If the field is present but maxSlots is not present, requests will be rejected with error code `google.rpc.Code.INVALID_ARGUMENT`. |
| `reservationGroup` | `string`  Optional. The reservation group that this reservation belongs to. You can set this property when you create or update a reservation. Reservations do not need to belong to a reservation group. Format: projects/{project}/locations/{location}/reservationGroups/{reservationGroup} or just {reservationGroup} |
| `replicationStatus` | `object (ReplicationStatus)`  Output only. The Disaster Recovery(DR) replication status of the reservation. This is only available for the primary replicas of DR/failover reservations and provides information about the both the staleness of the secondary and the last error encountered while trying to replicate changes from the primary to the secondary. If this field is blank, it means that the reservation is either not a DR reservation or the reservation is a DR secondary or that any replication operations on the reservation have succeeded. |
| `maxSlots` | `string (int64 format)`  Optional. The overall max slots for the reservation, covering slotCapacity (baseline), idle slots (if ignoreIdleSlots is false) and scaled slots. If present, the reservation won't use more than the specified number of slots, even if there is demand and supply (from idle slots). NOTE: capping a reservation's idle slot usage is best effort and its usage may exceed the maxSlots value. However, in terms of autoscale.current\_slots (which accounts for the additional added slots), it will never exceed the maxSlots - baseline.  This field must be set together with the scalingMode enum value, otherwise the request will be rejected with error code `google.rpc.Code.INVALID_ARGUMENT`.  If the maxSlots and scalingMode are set, the autoscale or autoscale.max\_slots field must be unset. Otherwise the request will be rejected with error code `google.rpc.Code.INVALID_ARGUMENT`. However, the autoscale field may still be in the output. The autopscale.max\_slots will always show as 0 and the autoscaler.current\_slots will represent the current slots from autoscaler excluding idle slots. For example, if the maxSlots is 1000 and scalingMode is AUTOSCALE\_ONLY, then in the output, the autoscaler.max\_slots will be 0 and the autoscaler.current\_slots may be any value between 0 and 1000.  If the maxSlots is 1000, scalingMode is ALL\_SLOTS, the baseline is 100 and idle slots usage is 200, then in the output, the autoscaler.max\_slots will be 0 and the autoscaler.current\_slots will not be higher than 700.  If the maxSlots is 1000, scalingMode is IDLE\_SLOTS\_ONLY, then in the output, the autoscaler field will be null.  If the maxSlots and scalingMode are set, then the ignoreIdleSlots field must be aligned with the scalingMode enum value.(See details in ScalingMode comments). Otherwise the request will be rejected with error code `google.rpc.Code.INVALID_ARGUMENT`.  Please note, the maxSlots is for user to manage the part of slots greater than the baseline. Therefore, we don't allow users to set maxSlots smaller or equal to the baseline as it will not be meaningful. If the field is present and slotCapacity>=maxSlots, requests will be rejected with error code `google.rpc.Code.INVALID_ARGUMENT`.  Please note that if maxSlots is set to 0, we will treat it as unset. Customers can set maxSlots to 0 and set scalingMode to SCALING\_MODE\_UNSPECIFIED to disable the maxSlots feature. |

## Autoscale

Auto scaling settings.

| JSON representation |
| --- |
| ``` {   "currentSlots": string,   "maxSlots": string } ``` |

| Fields | |
| --- | --- |
| `currentSlots` | `string (int64 format)`  Output only. The slot capacity added to this reservation when autoscale happens. Will be between [0, maxSlots]. Note: after users reduce maxSlots, it may take a while before it can be propagated, so currentSlots may stay in the original value and could be larger than maxSlots for that brief period (less than one minute) |
| `maxSlots` | `string (int64 format)`  Optional. Number of slots to be scaled when needed. |

## ScalingMode

The scaling mode for the reservation. This enum determines how the reservation scales up and down.

| Enums | |
| --- | --- |
| `SCALING_MODE_UNSPECIFIED` | Default value of ScalingMode. |
| `AUTOSCALE_ONLY` | The reservation will scale up only using slots from autoscaling. It will not use any idle slots even if there may be some available. The upper limit that autoscaling can scale up to will be maxSlots - baseline. For example, if maxSlots is 1000, baseline is 200 and customer sets ScalingMode to AUTOSCALE\_ONLY, then autoscalerg will scale up to 800 slots and no idle slots will be used.  Please note, in this mode, the ignoreIdleSlots field must be set to true. Otherwise the request will be rejected with error code `google.rpc.Code.INVALID_ARGUMENT`. |
| `IDLE_SLOTS_ONLY` | The reservation will scale up using only idle slots contributed by other reservations or from unassigned commitments. If no idle slots are available it will not scale up further. If the idle slots which it is using are reclaimed by the contributing reservation(s) it may be forced to scale down. The max idle slots the reservation can be maxSlots - baseline capacity. For example, if maxSlots is 1000, baseline is 200 and customer sets ScalingMode to IDLE\_SLOTS\_ONLY, 1. if there are 1000 idle slots available in other reservations, the reservation will scale up to 1000 slots with 200 baseline and 800 idle slots. 2. if there are 500 idle slots available in other reservations, the reservation will scale up to 700 slots with 200 baseline and 500 idle slots. Please note, in this mode, the reservation might not be able to scale up to maxSlots.  Please note, in this mode, the ignoreIdleSlots field must be set to false. Otherwise the request will be rejected with error code `google.rpc.Code.INVALID_ARGUMENT`. |
| `ALL_SLOTS` | The reservation will scale up using all slots available to it. It will use idle slots contributed by other reservations or from unassigned commitments first. If no idle slots are available it will scale up using autoscaling. For example, if maxSlots is 1000, baseline is 200 and customer sets ScalingMode to ALL\_SLOTS, 1. if there are 800 idle slots available in other reservations, the reservation will scale up to 1000 slots with 200 baseline and 800 idle slots. 2. if there are 500 idle slots available in other reservations, the reservation will scale up to 1000 slots with 200 baseline, 500 idle slots and 300 autoscaling slots. 3. if there are no idle slots available in other reservations, it will scale up to 1000 slots with 200 baseline and 800 autoscaling slots.  Please note, in this mode, the ignoreIdleSlots field must be set to false. Otherwise the request will be rejected with error code `google.rpc.Code.INVALID_ARGUMENT`. |

## ReplicationStatus

Disaster Recovery(DR) replication status of the reservation.

| JSON representation |
| --- |
| ``` {   "error": {     object (Status)   },   "lastErrorTime": string,   "lastReplicationTime": string,   "softFailoverStartTime": string } ``` |

| Fields | |
| --- | --- |
| `error` | `object (Status)`  Output only. The last error encountered while trying to replicate changes from the primary to the secondary. This field is only available if the replication has not succeeded since. |
| `lastErrorTime` | `string (Timestamp format)`  Output only. The time at which the last error was encountered while trying to replicate changes from the primary to the secondary. This field is only available if the replication has not succeeded since.  Uses RFC 3339, where generated output will always be Z-normalized and use 0, 3, 6 or 9 fractional digits. Offsets other than "Z" are also accepted. Examples: `"2014-10-02T15:01:23Z"`, `"2014-10-02T15:01:23.045123456Z"` or `"2014-10-02T15:01:23+05:30"`. |
| `lastReplicationTime` | `string (Timestamp format)`  Output only. A timestamp corresponding to the last change on the primary that was successfully replicated to the secondary.  Uses RFC 3339, where generated output will always be Z-normalized and use 0, 3, 6 or 9 fractional digits. Offsets other than "Z" are also accepted. Examples: `"2014-10-02T15:01:23Z"`, `"2014-10-02T15:01:23.045123456Z"` or `"2014-10-02T15:01:23+05:30"`. |
| `softFailoverStartTime` | `string (Timestamp format)`  Output only. The time at which a soft failover for the reservation and its associated datasets was initiated. After this field is set, all subsequent changes to the reservation will be rejected unless a hard failover overrides this operation. This field will be cleared once the failover is complete.  Uses RFC 3339, where generated output will always be Z-normalized and use 0, 3, 6 or 9 fractional digits. Offsets other than "Z" are also accepted. Examples: `"2014-10-02T15:01:23Z"`, `"2014-10-02T15:01:23.045123456Z"` or `"2014-10-02T15:01:23+05:30"`. |

| Methods | |
| --- | --- |
| `create` | Creates a new reservation resource. |
| `delete` | Deletes a reservation. |
| `failoverReservation` | Fail over a reservation to the secondary location. |
| `get` | Returns information about the reservation. |
| `getIamPolicy` | Gets the access control policy for a resource. |
| `list` | Lists all the reservations for the project in the specified location. |
| `patch` | Updates an existing reservation resource. |
| `setIamPolicy` | Sets an access control policy for a resource. |
| `testIamPermissions` | Gets your permissions on a resource. |




Send feedback

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2026-04-09 UTC.




Need to tell us more?

[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Hard to understand","hardToUnderstand","thumb-down"],["Incorrect information or sample code","incorrectInformationOrSampleCode","thumb-down"],["Missing the information/samples I need","missingTheInformationSamplesINeed","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2026-04-09 UTC."],[],[]]