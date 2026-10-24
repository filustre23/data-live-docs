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