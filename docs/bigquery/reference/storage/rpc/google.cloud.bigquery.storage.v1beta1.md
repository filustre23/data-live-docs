* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback

# Package google.cloud.bigquery.storage.v1beta1 Stay organized with collections Save and categorize content based on your preferences.

## Index

* `BigQueryStorage` (interface)
* `ArrowRecordBatch` (message)
* `ArrowSchema` (message)
* `AvroRows` (message)
* `AvroSchema` (message)
* `BatchCreateReadSessionStreamsRequest` (message)
* `BatchCreateReadSessionStreamsResponse` (message)
* `CreateReadSessionRequest` (message)
* `DataFormat` (enum)
* `FinalizeStreamRequest` (message)
* `Progress` (message)
* `ReadRowsRequest` (message)
* `ReadRowsResponse` (message)
* `ReadSession` (message)
* `ShardingStrategy` (enum)
* `SplitReadStreamRequest` (message)
* `SplitReadStreamResponse` (message)
* `Stream` (message)
* `StreamPosition` (message)
* `StreamStatus` (message)
* `TableModifiers` (message)
* `TableReadOptions` (message)
* `TableReference` (message)
* `ThrottleStatus` (message)

## BigQueryStorage

BigQuery storage API.

The BigQuery storage API can be used to read data stored in BigQuery.

The v1beta1 API is not yet officially deprecated, and will go through a full deprecation cycle (<https://cloud.google.com/products#product-launch-stages>) before the service is turned down. However, new code should use the v1 API going forward.

| BatchCreateReadSessionStreams |
| --- |
| `rpc BatchCreateReadSessionStreams(BatchCreateReadSessionStreamsRequest) returns (BatchCreateReadSessionStreamsResponse)`  Creates additional streams for a ReadSession. This API can be used to dynamically adjust the parallelism of a batch processing task upwards by adding additional workers. |

| CreateReadSession |
| --- |
| `rpc CreateReadSession(CreateReadSessionRequest) returns (ReadSession)`  Creates a new read session. A read session divides the contents of a BigQuery table into one or more streams, which can then be used to read data from the table. The read session also specifies properties of the data to be read, such as a list of columns or a push-down filter describing the rows to be returned.  A particular row can be read by at most one stream. When the caller has reached the end of each stream in the session, then all the data in the table has been read.  Read sessions automatically expire 6 hours after they are created and do not require manual clean-up by the caller. |

| FinalizeStream |
| --- |
| `rpc FinalizeStream(FinalizeStreamRequest) returns (Empty)`  Causes a single stream in a ReadSession to gracefully stop. This API can be used to dynamically adjust the parallelism of a batch processing task downwards without losing data.  This API does not delete the stream -- it remains visible in the ReadSession, and any data processed by the stream is not released to other streams. However, no additional data will be assigned to the stream once this call completes. Callers must continue reading data on the stream until the end of the stream is reached so that data which has already been assigned to the stream will be processed.  This method will return an error if there are no other live streams in the Session, or if SplitReadStream() has been called on the given Stream. |

| ReadRows |
| --- |
| `rpc ReadRows(ReadRowsRequest) returns (ReadRowsResponse)`  Reads rows from the table in the format prescribed by the read session. Each response contains one or more table rows, up to a maximum of 10 MiB per response; read requests which attempt to read individual rows larger than this will fail.  Each request also returns a set of stream statistics reflecting the estimated total number of rows in the read stream. This number is computed based on the total table size and the number of active streams in the read session, and may change as other streams continue to read data. |

| SplitReadStream |
| --- |
| `rpc SplitReadStream(SplitReadStreamRequest) returns (SplitReadStreamResponse)`  Splits a given read stream into two Streams. These streams are referred to as the primary and the residual of the split. The original stream can still be read from in the same manner as before. Both of the returned streams can also be read from, and the total rows return by both child streams will be the same as the rows read from the original stream.  Moreover, the two child streams will be allocated back to back in the original Stream. Concretely, it is guaranteed that for streams Original, Primary, and Residual, that Original[0-j] = Primary[0-j] and Original[j-n] = Residual[0-m] once the streams have been read to completion.  This method is guaranteed to be idempotent. |

## ArrowRecordBatch

Arrow RecordBatch.

| Fields | |
| --- | --- |
| `serialized_record_batch` | `bytes`  IPC serialized Arrow RecordBatch. |
| `row_count` | `int64`  The count of rows in the returning block. |

## ArrowSchema

Arrow schema.

| Fields | |
| --- | --- |
| `serialized_schema` | `bytes`  IPC serialized Arrow schema. |

## AvroRows

Avro rows.

| Fields | |
| --- | --- |
| `serialized_binary_rows` | `bytes`  Binary serialized rows in a block. |
| `row_count` | `int64`  The count of rows in the returning block. |

## AvroSchema

Avro schema.

| Fields | |
| --- | --- |
| `schema` | `string`  Json serialized schema, as described at <https://avro.apache.org/docs/1.8.1/spec.html> |

## BatchCreateReadSessionStreamsRequest

Information needed to request additional streams for an established read session.

| Fields | |
| --- | --- |
| `session` | `ReadSession`  Required. Must be a non-expired session obtained from a call to CreateReadSession. Only the name field needs to be set. |
| `requested_streams` | `int32`  Required. Number of new streams requested. Must be positive. Number of added streams may be less than this, see CreateReadSessionRequest for more information. |

## BatchCreateReadSessionStreamsResponse

The response from `BatchCreateReadSessionStreams` returns the stream identifiers for the newly created streams.

| Fields | |
| --- | --- |
| `streams[]` | `Stream`  Newly added streams. |

## CreateReadSessionRequest

Creates a new read session, which may include additional options such as requested parallelism, projection filters and constraints.

| Fields | |
| --- | --- |
| `table_reference` | `TableReference`  Required. Reference to the table to read.  Authorization requires the following [IAM](https://cloud.google.com/iam/docs/) permission on the specified resource `tableReference`:   * `bigquery.tables.getData` |
| `parent` | `string`  Required. String of the form `projects/{project_id}` indicating the project this ReadSession is associated with. This is the project that will be billed for usage.  Authorization requires the following [IAM](https://cloud.google.com/iam/docs/) permission on the specified resource `parent`:   * `bigquery.readsessions.create` |
| `table_modifiers` | `TableModifiers`  Any modifiers to the Table (e.g. snapshot timestamp). |
| `requested_streams` | `int32`  Initial number of streams. If unset or 0, we will provide a value of streams so as to produce reasonable throughput. Must be non-negative. The number of streams may be lower than the requested number, depending on the amount parallelism that is reasonable for the table and the maximum amount of parallelism allowed by the system.  Streams must be read starting from offset 0. |
| `read_options` | `TableReadOptions`  Read options for this session (e.g. column selection, filters). |
| `format` | `DataFormat`  Data output format. Currently default to Avro. DATA\_FORMAT\_UNSPECIFIED not supported. |
| `sharding_strategy` | `ShardingStrategy`  The strategy to use for distributing data among multiple streams. Currently defaults to liquid sharding. |

## DataFormat

Data format for input or output data.

| Enums | |
| --- | --- |
| `DATA_FORMAT_UNSPECIFIED` | Data format is unspecified. |
| `AVRO` | Avro is a standard open source row based file format. See <https://avro.apache.org/> for more details. |
| `ARROW` | Arrow is a standard open source column-based message format. See <https://arrow.apache.org/> for more details. |

## FinalizeStreamRequest

Request information for invoking `FinalizeStream`.

| Fields | |
| --- | --- |
| `stream` | `Stream`  Required. Stream to finalize. |

## Progress

| Fields | |
| --- | --- |
| `at_response_start` | `float`  The fraction of rows assigned to the stream that have been processed by the server so far, not including the rows in the current response message.  This value, along with `at_response_end`, can be used to interpolate the progress made as the rows in the message are being processed using the following formula: `at_response_start + (at_response_end - at_response_start) * rows_processed_from_response / rows_in_response`.  Note that if a filter is provided, the `at_response_end` value of the previous response may not necessarily be equal to the `at_response_start` value of the current response. |
| `at_response_end` | `float`  Similar to `at_response_start`, except that this value includes the rows in the current response. |

## ReadRowsRequest

Requesting row data via `ReadRows` must provide Stream position information.

| Fields | |
| --- | --- |
| `read_position` | `StreamPosition`  Required. Identifier of the position in the stream to start reading from. The offset requested must be less than the last row read from ReadRows. Requesting a larger offset is undefined. |

## ReadRowsResponse

Response from calling `ReadRows` may include row data, progress and throttling information.

| Fields | |
| --- | --- |
| `row_count` | `int64`  Number of serialized rows in the rows block. This value is recorded here, in addition to the row\_count values in the output-specific messages in `rows`, so that code which needs to record progress through the stream can do so in an output format-independent way. |
| `status` | `StreamStatus`  Estimated stream statistics. |
| `throttle_status` | `ThrottleStatus`  Throttling status. If unset, the latest response still describes the current throttling status. |
| Union field `rows`. Row data is returned in format specified during session creation. `rows` can be only one of the following: | |
| `avro_rows` | `AvroRows`  Serialized row data in AVRO format. |
| `arrow_record_batch` | `ArrowRecordBatch`  Serialized row data in Arrow RecordBatch format. |
| Union field `schema`. The schema for the read. If read\_options.selected\_fields is set, the schema may be different from the table schema as it will only contain the selected fields. This schema is equivalent to the one returned by CreateSession. This field is only populated in the first ReadRowsResponse RPC. `schema` can be only one of the following: | |
| `avro_schema` | `AvroSchema`  Output only. Avro schema. |
| `arrow_schema` | `ArrowSchema`  Output only. Arrow schema. |

## ReadSession

Information returned from a `CreateReadSession` request.

| Fields | |
| --- | --- |
| `name` | `string`  Unique identifier for the session, in the form `projects/{project_id}/locations/{location}/sessions/{session_id}`. |
| `expire_time` | `Timestamp`  Time at which the session becomes invalid. After this time, subsequent requests to read this Session will return errors. |
| `streams[]` | `Stream`  Streams associated with this session. |
| `table_reference` | `TableReference`  Table that this ReadSession is reading from. |
| `table_modifiers` | `TableModifiers`  Any modifiers which are applied when reading from the specified table. |
| `sharding_strategy` | `ShardingStrategy`  The strategy to use for distributing data among the streams. |
| Union field `schema`. The schema for the read. If read\_options.selected\_fields is set, the schema may be different from the table schema as it will only contain the selected fields. `schema` can be only one of the following: | |
| `avro_schema` | `AvroSchema`  Avro schema. |
| `arrow_schema` | `ArrowSchema`  Arrow schema. |

## ShardingStrategy

Strategy for distributing data among multiple streams in a read session.

| Enums | |
| --- | --- |
| `SHARDING_STRATEGY_UNSPECIFIED` | Same as LIQUID. |
| `LIQUID` | Assigns data to each stream based on the client's read rate. The faster the client reads from a stream, the more data is assigned to the stream. In this strategy, it's possible to read all data from a single stream even if there are other streams present. |
| `BALANCED` | Assigns data to each stream such that roughly the same number of rows can be read from each stream. Because the server-side unit for assigning data is collections of rows, the API does not guarantee that each stream will return the same number or rows. Additionally, the limits are enforced based on the number of pre-filtering rows, so some filters can lead to lopsided assignments. |

## SplitReadStreamRequest

Request information for `SplitReadStream`.

| Fields | |
| --- | --- |
| `original_stream` | `Stream`  Required. Stream to split. |
| `fraction` | `float`  A value in the range (0.0, 1.0) that specifies the fractional point at which the original stream should be split. The actual split point is evaluated on pre-filtered rows, so if a filter is provided, then there is no guarantee that the division of the rows between the new child streams will be proportional to this fractional value. Additionally, because the server-side unit for assigning data is collections of rows, this fraction will always map to to a data storage boundary on the server side. |

## SplitReadStreamResponse

Response from `SplitReadStream`.

| Fields | |
| --- | --- |
| `primary_stream` | `Stream`  Primary stream, which contains the beginning portion of |original\_stream|. An empty value indicates that the original stream can no longer be split. |
| `remainder_stream` | `Stream`  Remainder stream, which contains the tail of |original\_stream|. An empty value indicates that the original stream can no longer be split. |

## Stream

Information about a single data stream within a read session.

| Fields | |
| --- | --- |
| `name` | `string`  Name of the stream, in the form `projects/{project_id}/locations/{location}/streams/{stream_id}`. |

## StreamPosition

Expresses a point within a given stream using an offset position.

| Fields | |
| --- | --- |
| `stream` | `Stream`  Identifier for a given Stream. |
| `offset` | `int64`  Position in the stream. |

## StreamStatus

Progress information for a given Stream.

| Fields | |
| --- | --- |
| `estimated_row_count` | `int64`  Number of estimated rows in the current stream. May change over time as different readers in the stream progress at rates which are relatively fast or slow. |
| `fraction_consumed` | `float`  A value in the range [0.0, 1.0] that represents the fraction of rows assigned to this stream that have been processed by the server. In the presence of read filters, the server may process more rows than it returns, so this value reflects progress through the pre-filtering rows.  This value is only populated for sessions created through the BALANCED sharding strategy. |
| `progress` | `Progress`  Represents the progress of the current stream. |
| `is_splittable` | `bool`  Whether this stream can be split. For sessions that use the LIQUID sharding strategy, this value is always false. For BALANCED sessions, this value is false when enough data have been read such that no more splits are possible at that point or beyond. For small tables or streams that are the result of a chain of splits, this value may never be true. |

## TableModifiers

All fields in this message optional.

| Fields | |
| --- | --- |
| `snapshot_time` | `Timestamp`  The snapshot time of the table. If not set, interpreted as now. |

## TableReadOptions

Options dictating how we read a table.

| Fields | |
| --- | --- |
| `selected_fields[]` |  |