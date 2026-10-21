* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback

# Method: projects.locations.dataExchanges.listings.subscribe Stay organized with collections Save and categorize content based on your preferences.

* [HTTP request](#body.HTTP_TEMPLATE)
* [Path parameters](#body.PATH_PARAMETERS)
* [Request body](#body.request_body)
  + [JSON representation](#body.request_body.SCHEMA_REPRESENTATION)
* [Response body](#body.response_body)
  + [JSON representation](#body.SubscribeListingResponse.SCHEMA_REPRESENTATION)
* [Authorization scopes](#body.aspect)
* [DestinationPubSubSubscription](#DestinationPubSubSubscription)
  + [JSON representation](#DestinationPubSubSubscription.SCHEMA_REPRESENTATION)
* [PubSubSubscription](#PubSubSubscription)
  + [JSON representation](#PubSubSubscription.SCHEMA_REPRESENTATION)
* [PushConfig](#PushConfig)
  + [JSON representation](#PushConfig.SCHEMA_REPRESENTATION)
* [OidcToken](#OidcToken)
  + [JSON representation](#OidcToken.SCHEMA_REPRESENTATION)
* [PubsubWrapper](#PubsubWrapper)
* [NoWrapper](#NoWrapper)
  + [JSON representation](#NoWrapper.SCHEMA_REPRESENTATION)
* [BigQueryConfig](#BigQueryConfig)
  + [JSON representation](#BigQueryConfig.SCHEMA_REPRESENTATION)
* [CloudStorageConfig](#CloudStorageConfig)
  + [JSON representation](#CloudStorageConfig.SCHEMA_REPRESENTATION)
* [TextConfig](#TextConfig)
* [AvroConfig](#AvroConfig)
  + [JSON representation](#AvroConfig.SCHEMA_REPRESENTATION)
* [BigtableConfig](#BigtableConfig)
  + [JSON representation](#BigtableConfig.SCHEMA_REPRESENTATION)
* [ColumnFamilyMapping](#ColumnFamilyMapping)
  + [JSON representation](#ColumnFamilyMapping.SCHEMA_REPRESENTATION)
* [RowKeySchema](#RowKeySchema)
* [DelimitedKey](#DelimitedKey)
  + [JSON representation](#DelimitedKey.SCHEMA_REPRESENTATION)
* [ExpirationPolicy](#ExpirationPolicy)
  + [JSON representation](#ExpirationPolicy.SCHEMA_REPRESENTATION)
* [DeadLetterPolicy](#DeadLetterPolicy)
  + [JSON representation](#DeadLetterPolicy.SCHEMA_REPRESENTATION)
* [RetryPolicy](#RetryPolicy)
  + [JSON representation](#RetryPolicy.SCHEMA_REPRESENTATION)
* [MessageTransform](#MessageTransform)
  + [JSON representation](#MessageTransform.SCHEMA_REPRESENTATION)
* [JavaScriptUDF](#JavaScriptUDF)
  + [JSON representation](#JavaScriptUDF.SCHEMA_REPRESENTATION)
* [AIInference](#AIInference)
  + [JSON representation](#AIInference.SCHEMA_REPRESENTATION)
* [UnstructuredInference](#UnstructuredInference)
  + [JSON representation](#UnstructuredInference.SCHEMA_REPRESENTATION)
* [Compression](#Compression)
  + [JSON representation](#Compression.SCHEMA_REPRESENTATION)
* [CompressionAlgorithm](#CompressionAlgorithm)
* [CompressionMode](#CompressionMode)
* [Try it!](#try-it)

Subscribes to a listing.

Currently, with Analytics Hub, you can create listings that reference only BigQuery datasets. Upon subscription to a listing for a BigQuery dataset, Analytics Hub creates a linked dataset in the subscriber's project.

### HTTP request

`POST https://analyticshub.googleapis.com/v1/{name=projects/*/locations/*/dataExchanges/*/listings/*}:subscribe`

The URL uses [gRPC Transcoding](https://google.aip.dev/127) syntax.

### Path parameters

| Parameters | |
| --- | --- |
| `name` | `string`  Required. Resource name of the listing that you want to subscribe to. e.g. `projects/myproject/locations/us/dataExchanges/123/listings/456`. |

### Request body

The request body contains data with the following structure:

| JSON representation |
| --- |
| ``` {    // The following is a list of mutually exclusive fields. At most one of the   // fields will be set in a response:   "destinationDataset": {     object (DestinationDataset)   },   "destinationPubsubSubscription": {     object (DestinationPubSubSubscription)   }   // End of mutually exclusive fields. } ``` |

| Fields | |
| --- | --- |
| Resulting destination of the listing that you subscribed to. The following is a list of mutually exclusive fields. At most one of the fields will be set in a response: | |
| `destinationDataset` | `object (DestinationDataset)`  Input only. BigQuery destination dataset to create for the subscriber. |
| `destinationPubsubSubscription` | `object (DestinationPubSubSubscription)`  Input only. Destination Pub/Sub subscription to create for the subscriber. |
| End of mutually exclusive fields. | |

### Response body

Message for response when you subscribe to a listing.

If successful, the response body contains data with the following structure:

| JSON representation |
| --- |
| ``` {   "subscription": {     object (Subscription)   } } ``` |

| Fields | |
| --- | --- |
| `subscription` | `object (Subscription)`  Subscription object created from this subscribe action. |

### Authorization scopes

Requires one of the following OAuth scopes:

* `https://www.googleapis.com/auth/bigquery`
* `https://www.googleapis.com/auth/cloud-platform`

For more information, see the [Authentication Overview](/docs/authentication#authorization-gcp).

## DestinationPubSubSubscription

Defines the destination Pub/Sub subscription.

| JSON representation |
| --- |
| ``` {   "pubsubSubscription": {     object (PubSubSubscription)   } } ``` |

| Fields | |
| --- | --- |
| `pubsubSubscription` | `object (PubSubSubscription)`  Required. Destination Pub/Sub subscription resource. |

## PubSubSubscription

Defines the destination Pub/Sub subscription. If none of `pushConfig`, `bigqueryConfig`, `cloudStorageConfig`, `bigtableConfig`, `pubsubExportConfig`, or `pubsubliteExportConfig` is set, then the subscriber will pull and ack messages using API methods. At most one of these fields may be set.

| JSON representation |
| --- |
| ``` {   "name": string,   "pushConfig": {     object (PushConfig)   },   "bigqueryConfig": {     object (BigQueryConfig)   },   "cloudStorageConfig": {     object (CloudStorageConfig)   },   "bigtableConfig": {     object (BigtableConfig)   },   "ackDeadlineSeconds": integer,   "retainAckedMessages": boolean,   "messageRetentionDuration": string,   "labels": {     string: string,     ...   },   "enableMessageOrdering": boolean,   "expirationPolicy": {     object (ExpirationPolicy)   },   "filter": string,   "deadLetterPolicy": {     object (DeadLetterPolicy)   },   "retryPolicy": {     object (RetryPolicy)   },   "detached": boolean,   "enableExactlyOnceDelivery": boolean,   "messageTransforms": [     {       object (MessageTransform)     }   ],   "tags": {     string: string,     ...   } } ``` |

| Fields | |
| --- | --- |
| `name` | `string`  Required. Identifier. Name of the subscription. Format is `projects/{project}/subscriptions/{sub}`. |
| `pushConfig` | `object (PushConfig)`  Optional. If push delivery is used with this subscription, this field is used to configure it. |
| `bigqueryConfig` | `object (BigQueryConfig)`  Optional. If delivery to BigQuery is used with this subscription, this field is used to configure it. |
| `cloudStorageConfig` | `object (CloudStorageConfig)`  Optional. If delivery to Google Cloud Storage is used with this subscription, this field is used to configure it. |
| `bigtableConfig` | `object (BigtableConfig)`  Optional. If delivery to Bigtable is used with this subscription, this field is used to configure it. |
| `ackDeadlineSeconds` | `integer`  Optional. The approximate amount of time (on a best-effort basis) Pub/Sub waits for the subscriber to acknowledge receipt before resending the message. In the interval after the message is delivered and before it is acknowledged, it is considered to be *outstanding*. During that time period, the message will not be redelivered (on a best-effort basis).  For pull subscriptions, this value is used as the initial value for the ack deadline. To override this value for a given message, call `ModifyAckDeadline` with the corresponding `ack_id` if using non-streaming pull or send the `ack_id` in a `StreamingModifyAckDeadlineRequest` if using streaming pull. The minimum custom deadline you can specify is 10 seconds. The maximum custom deadline you can specify is 600 seconds (10 minutes). If this parameter is 0, a default value of 10 seconds is used.  For push delivery, this value is also used to set the request timeout for the call to the push endpoint.  If the subscriber never acknowledges the message, the Pub/Sub system will eventually redeliver the message. |
| `retainAckedMessages` | `boolean`  Optional. Indicates whether to retain acknowledged messages. If true, then messages are not expunged from the subscription's backlog, even if they are acknowledged, until they fall out of the `messageRetentionDuration` window. This must be true if you would like to [`Seek` to a timestamp](https://cloud.google.com/pubsub/docs/replay-overview#seek_to_a_time) in the past to replay previously-acknowledged messages. |
| `messageRetentionDuration` | `string (Duration format)`  Optional. How long to retain unacknowledged messages in the subscription's backlog, from the moment a message is published. If `retainAckedMessages` is true, then this also configures the retention of acknowledged messages, and thus configures how far back in time a `Seek` can be done. Defaults to 7 days. Cannot be more than 31 days or less than 10 minutes.  A duration in seconds with up to nine fractional digits, ending with '`s`'. Example: `"3.5s"`. |
| `labels` | `map (key: string, value: string)`  Optional. See [Creating and managing labels](https://cloud.google.com/pubsub/docs/labels).  An object containing a list of `"key": value` pairs. Example: `{ "name": "wrench", "mass": "1.3kg", "count": "3" }`. |
| `enableMessageOrdering` | `boolean`  Optional. If true, messages published with the same `ordering_key` in `PubsubMessage` will be delivered to the subscribers in the order in which they are received by the Pub/Sub system. Otherwise, they may be delivered in any order. |
| `expirationPolicy` | `object (ExpirationPolicy)`  Optional. A policy that specifies the conditions for this subscription's expiration. A subscription is considered active as long as any connected subscriber is successfully consuming messages from the subscription or is issuing operations on the subscription. If `expirationPolicy` is not set, a *default policy* with `ttl` of 31 days will be used. The minimum allowed value for `expirationPolicy.ttl` is 1 day. If `expirationPolicy` is set, but `expirationPolicy.ttl` is not set, the subscription never expires. |
| `filter` | `string`  Optional. An expression written in the Pub/Sub [filter language](https://cloud.google.com/pubsub/docs/filtering). If non-empty, then only `PubsubMessage`s whose `attributes` field matches the filter are delivered on this subscription. If empty, then no messages are filtered out. |
| `deadLetterPolicy` | `object (DeadLetterPolicy)`  Optional. A policy that specifies the conditions for dead lettering messages in this subscription. If deadLetterPolicy is not set, dead lettering is disabled.  The Pub/Sub service account associated with this subscriptions's parent project (i.e., service-{projectNumber}@gcp-sa-pubsub.iam.gserviceaccount.com) must have permission to Acknowledge() messages on this subscription. |
| `retryPolicy` | `object (RetryPolicy)`  Optional. A policy that specifies how Pub/Sub retries message delivery for this subscription.  If not set, the default retry policy is applied. This generally implies that messages will be retried as soon as possible for healthy subscribers. RetryPolicy will be triggered on NACKs or acknowledgement deadline exceeded events for a given message. |
| `detached` | `boolean`  Optional. Indicates whether the subscription is detached from its topic. Detached subscriptions don't receive messages from their topic and don't retain any backlog. `Pull` and `StreamingPull` requests will return FAILED\_PRECONDITION. If the subscription is a push subscription, pushes to the endpoint will not be made. |
| `enableExactlyOnceDelivery` | `boolean`  Optional. If true, Pub/Sub provides the following guarantees for the delivery of a message with a given value of `message_id` on this subscription:   * The message sent to a subscriber is guaranteed not to be resent before the message's acknowledgement deadline expires. * An acknowledged message will not be resent to a subscriber.   Note that subscribers may still receive multiple copies of a message when `enableExactlyOnceDelivery` is true if the message was published multiple times by a publisher client. These copies are considered distinct by Pub/Sub and have distinct `message_id` values. |
| `messageTransforms[]` | `object (MessageTransform)`  Optional. Transforms to be applied to messages before they are delivered to subscribers. Transforms are applied in the order specified. |
| `tags` | `map (key: string, value: string)`  Optional. Input only. Immutable. Tag keys/values directly bound to this resource. For example: "123/environment": "production", "123/costCenter": "marketing" See [Create and manage tags](https://cloud.google.com/pubsub/docs/tags) for more information on using tags with Pub/Sub resources.  An object containing a list of `"key": value` pairs. Example: `{ "name": "wrench", "mass": "1.3kg", "count": "3" }`. |

## PushConfig

Configuration for a push delivery endpoint.

| JSON representation |
| --- |
|  |