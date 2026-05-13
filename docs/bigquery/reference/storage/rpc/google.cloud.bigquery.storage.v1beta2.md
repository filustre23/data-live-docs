* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback

# Package google.cloud.bigquery.storage.v1beta2 Stay organized with collections Save and categorize content based on your preferences.

## Index

* `BigQueryRead` (interface)
* `BigQueryWrite` (interface) **(deprecated)**
* `AppendRowsRequest` (message)
* `AppendRowsRequest.ProtoData` (message)
* `AppendRowsResponse` (message)
* `AppendRowsResponse.AppendResult` (message)
* `ArrowRecordBatch` (message)
* `ArrowSchema` (message)
* `ArrowSerializationOptions` (message)
* `ArrowSerializationOptions.Format` (enum)
* `AvroRows` (message)
* `AvroSchema` (message)
* `BatchCommitWriteStreamsRequest` (message)
* `BatchCommitWriteStreamsResponse` (message)
* `CreateReadSessionRequest` (message)
* `CreateWriteStreamRequest` (message)
* `DataFormat` (enum)
* `FinalizeWriteStreamRequest` (message)
* `FinalizeWriteStreamResponse` (message)
* `FlushRowsRequest` (message)
* `FlushRowsResponse` (message)
* `GetWriteStreamRequest` (message)
* `ProtoRows` (message)
* `ProtoSchema` (message)
* `ReadRowsRequest` (message)
* `ReadRowsResponse` (message)
* `ReadSession` (message)
* `ReadSession.TableModifiers` (message)
* `ReadSession.TableReadOptions` (message)
* `ReadStream` (message)
* `RowError` (message)
* `RowError.RowErrorCode` (enum)
* `SplitReadStreamRequest` (message)
* `SplitReadStreamResponse` (message)
* `StorageError` (message)
* `StorageError.StorageErrorCode` (enum)
* `StreamStats` (message)
* `StreamStats.Progress` (message)
* `TableFieldSchema` (message)
* `TableFieldSchema.Mode` (enum)
* `TableFieldSchema.Type` (enum)
* `TableSchema` (message)
* `ThrottleState` (message)
* `WriteStream` (message)
* `WriteStream.Type` (enum)

## BigQueryRead

BigQuery Read API.

The Read API can be used to read data from BigQuery.

New code should use the v1 Read API going forward, if they don't use Write API at the same time.

| CreateReadSession |
| --- |
| `rpc CreateReadSession(CreateReadSessionRequest) returns (ReadSession)`  Creates a new read session. A read session divides the contents of a BigQuery table into one or more streams, which can then be used to read data from the table. The read session also specifies properties of the data to be read, such as a list of columns or a push-down filter describing the rows to be returned.  A particular row can be read by at most one stream. When the caller has reached the end of each stream in the session, then all the data in the table has been read.  Data is assigned to each stream such that roughly the same number of rows can be read from each stream. Because the server-side unit for assigning data is collections of rows, the API does not guarantee that each stream will return the same number or rows. Additionally, the limits are enforced based on the number of pre-filtered rows, so some filters can lead to lopsided assignments.  Read sessions automatically expire 6 hours after they are created and do not require manual clean-up by the caller. |

| ReadRows |
| --- |
| `rpc ReadRows(ReadRowsRequest) returns (ReadRowsResponse)`  Reads rows from the stream in the format prescribed by the ReadSession. Each response contains one or more table rows, up to a maximum of 100 MiB per response; read requests which attempt to read individual rows larger than 100 MiB will fail.  Each request also returns a set of stream statistics reflecting the current state of the stream. |

| SplitReadStream |
| --- |
| `rpc SplitReadStream(SplitReadStreamRequest) returns (SplitReadStreamResponse)`  Splits a given `ReadStream` into two `ReadStream` objects. These `ReadStream` objects are referred to as the primary and the residual streams of the split. The original `ReadStream` can still be read from in the same manner as before. Both of the returned `ReadStream` objects can also be read from, and the rows returned by both child streams will be the same as the rows read from the original stream.  Moreover, the two child streams will be allocated back-to-back in the original `ReadStream`. Concretely, it is guaranteed that for streams original, primary, and residual, that original[0-j] = primary[0-j] and original[j-n] = residual[0-m] once the streams have been read to completion. |

## BigQueryWrite

This item is deprecated!

BigQuery Write API.

The Write API can be used to write data to BigQuery.

The [google.cloud.bigquery.storage.v1 API](/bigquery/docs/reference/storage/rpc/google.cloud.bigquery.storage.v1) should be used instead of the v1beta2 API for BigQueryWrite operations.

| AppendRows |
| --- |
| This item is deprecated!  `rpc AppendRows(AppendRowsRequest) returns (AppendRowsResponse)`  Appends data to the given stream.  If `offset` is specified, the `offset` is checked against the end of stream. The server returns `OUT_OF_RANGE` in `AppendRowsResponse` if an attempt is made to append to an offset beyond the current end of the stream or `ALREADY_EXISTS` if user provids an `offset` that has already been written to. User can retry with adjusted offset within the same RPC stream. If `offset` is not specified, append happens at the end of the stream.  The response contains the offset at which the append happened. Responses are received in the same order in which requests are sent. There will be one response for each successful request. If the `offset` is not set in response, it means append didn't happen due to some errors. If one request fails, all the subsequent requests will also fail until a success request is made again.  If the stream is of `PENDING` type, data will only be available for read operations after the stream is committed. |

| BatchCommitWriteStreams |
| --- |
| This item is deprecated!  `rpc BatchCommitWriteStreams(BatchCommitWriteStreamsRequest) returns (BatchCommitWriteStreamsResponse)`  Atomically commits a group of `PENDING` streams that belong to the same `parent` table. Streams must be finalized before commit and cannot be committed multiple times. Once a stream is committed, data in the stream becomes available for read operations. |

| CreateWriteStream |
| --- |
| This item is deprecated!  `rpc CreateWriteStream(CreateWriteStreamRequest) returns (WriteStream)`  Creates a write stream to the given table. Additionally, every table has a special COMMITTED stream named '\_default' to which data can be written. This stream doesn't need to be created using CreateWriteStream. It is a stream that can be used simultaneously by any number of clients. Data written to this stream is considered committed as soon as an acknowledgement is received. |

| FinalizeWriteStream |
| --- |
| This item is deprecated!  `rpc FinalizeWriteStream(FinalizeWriteStreamRequest) returns (FinalizeWriteStreamResponse)`  Finalize a write stream so that no new data can be appended to the stream. Finalize is not supported on the '\_default' stream. |

| FlushRows |
| --- |
| This item is deprecated!  `rpc FlushRows(FlushRowsRequest) returns (FlushRowsResponse)`  Flushes rows to a BUFFERED stream. If users are appending rows to BUFFERED stream, flush operation is required in order for the rows to become available for reading. A Flush operation flushes up to any previously flushed offset in a BUFFERED stream, to the offset specified in the request. Flush is not supported on the \_default stream, since it is not BUFFERED. |

| GetWriteStream |
| --- |
| This item is deprecated!  `rpc GetWriteStream(GetWriteStreamRequest) returns (WriteStream)`  Gets a write stream. |

## AppendRowsRequest

Request message for `AppendRows`.

| Fields | |
| --- | --- |
| `write_stream` | `string`  Required. The stream that is the target of the append operation. This value must be specified for the initial request. If subsequent requests specify the stream name, it must equal to the value provided in the first request. To write to the \_default stream, populate this field with a string in the format `projects/{project}/datasets/{dataset}/tables/{table}/_default`.  Authorization requires the following [IAM](https://cloud.google.com/iam/docs/) permission on the specified resource `writeStream`:   * `bigquery.tables.updateData` |
| `offset` | `Int64Value`  If present, the write is only performed if the next append offset is same as the provided value. If not present, the write is performed at the current end of stream. Specifying a value for this field is not allowed when calling AppendRows for the '\_default' stream. |
| `trace_id` | `string`  Id set by client to annotate its identity. Only initial request setting is respected. |
| Union field `rows`. Input rows. The `writer_schema` field must be specified at the initial request and currently, it will be ignored if specified in following requests. Following requests must have data in the same format as the initial request. `rows` can be only one of the following: | |
| `proto_rows` | `ProtoData`  Rows in proto format. |

## ProtoData

Proto schema and data.

| Fields | |
| --- | --- |
| `writer_schema` | `ProtoSchema`  Proto schema used to serialize the data. |
| `rows` | `ProtoRows`  Output only. Serialized row data in protobuf message format. |

## AppendRowsResponse

Response message for `AppendRows`.

| Fields | |
| --- | --- |
| `updated_schema` | `TableSchema`  If backend detects a schema update, pass it to user so that user can use it to input new type of message. It will be empty when no schema updates have occurred. |
| `row_errors[]` | `RowError`  If a request failed due to corrupted rows, no rows in the batch will be appended. The API will return row level error info, so that the caller can remove the bad rows and retry the request. |
| Union field `response`.  `response` can be only one of the following: | |
| `append_result` | `AppendResult`  Result if the append is successful. |
| `error` | `Status`  Error returned when problems were encountered. If present, it indicates rows were not accepted into the system. Users can retry or continue with other append requests within the same connection.  Additional information about error signalling:  ALREADY\_EXISTS: Happens when an append specified an offset, and the backend already has received data at this offset. Typically encountered in retry scenarios, and can be ignored.  OUT\_OF\_RANGE: Returned when the specified offset in the stream is beyond the current end of the stream.  INVALID\_ARGUMENT: Indicates a malformed request or data.  ABORTED: Request processing is aborted because of prior failures. The request can be retried if previous failure is addressed.  INTERNAL: Indicates server side error(s) that can be retried. |

## AppendResult

AppendResult is returned for successful append requests.

| Fields | |
| --- | --- |
| `offset` | `Int64Value`  The row offset at which the last append occurred. The offset will not be set if appending using default streams. |

## ArrowRecordBatch

Arrow RecordBatch.

| Fields | |
| --- | --- |
| `serialized_record_batch` | `bytes`  IPC-serialized Arrow RecordBatch. |

## ArrowSchema

Arrow schema as specified in <https://arrow.apache.org/docs/python/api/datatypes.html> and serialized to bytes using IPC: <https://arrow.apache.org/docs/format/Columnar.html#serialization-and-interprocess-communication-ipc>

See code samples on how this message can be deserialized.

| Fields | |
| --- | --- |
| `serialized_schema` | `bytes`  IPC serialized Arrow schema. |

## ArrowSerializationOptions

Contains options specific to Arrow Serialization.

| Fields | |
| --- | --- |
| `format` | `Format`  The Arrow IPC format to use. |

## Format

The IPC format to use when serializing Arrow streams.

| Enums | |
| --- | --- |
| `FORMAT_UNSPECIFIED` | If unspecified, the IPC format as of Apache Arrow Release 0.15 is used. |
| `ARROW_0_14` | Use the legacy IPC message format from Apache Arrow Release 0.14. |
| `ARROW_0_15` | Use the message format from Apache Arrow Release 0.15. |

## AvroRows

Avro rows.

| Fields | |
| --- | --- |
| `serialized_binary_rows` | `bytes`  Binary serialized rows in a block. |

## AvroSchema

Avro schema.

| Fields | |
| --- | --- |
| `schema` | `string`  Json serialized schema, as described at <https://avro.apache.org/docs/1.8.1/spec.html>. |

## BatchCommitWriteStreamsRequest

Request message for `BatchCommitWriteStreams`.

| Fields | |
| --- | --- |
| `parent` | `string`  Required. Parent table that all the streams should belong to, in the form of `projects/{project}/datasets/{dataset}/tables/{table}`.  Authorization requires the following [IAM](https://cloud.google.com/iam/docs/) permission on the specified resource `parent`:   * `bigquery.tables.updateData` |
| `write_streams[]` | `string`  Required. The group of streams that will be committed atomically. |

## BatchCommitWriteStreamsResponse

Response message for `BatchCommitWriteStreams`.

| Fields | |
| --- | --- |
| `commit_time` | `Timestamp`  The time at which streams were committed in microseconds granularity. This field will only exist when there are no stream errors. **Note** if this field is not set, it means the commit was not successful. |
| `stream_errors[]` | `StorageError`  Stream level error if commit failed. Only streams with error will be in the list. If empty, there is no error and all streams are committed successfully. If non empty, certain streams have errors and ZERO stream is committed due to atomicity guarantee. |

## CreateReadSessionRequest

Request message for `CreateReadSession`.

| Fields | |
| --- | --- |
| `parent` | `string`  Required. The request project that owns the session, in the form of `projects/{project_id}`.  Authorization requires the following [IAM](https://cloud.google.com/iam/docs/) permission on the specified resource `parent`:   * `bigquery.readsessions.create` |
| `read_session` | `ReadSession`  Required. Session to be created.  Authorization requires the following [IAM](https://cloud.google.com/iam/docs/) permission on the specified resource `readSession`:   * `bigquery.tables.getData` |
| `max_stream_count` | `int32`  Max initial number of streams. If unset or zero, the server will provide a value of streams so as to produce reasonable throughput. Must be non-negative. The number of streams may be lower than the requested number, depending on the amount parallelism that is reasonable for the table. Error will be returned if the max count is greater than the current system max limit of 1,000.  Streams must be read starting from offset 0. |

## CreateWriteStreamRequest

Request message for `CreateWriteStream`.

| Fields | |
| --- | --- |
| `parent` | `string`  Required. Reference to the table to which the stream belongs, in the format of `projects/{project}/datasets/{dataset}/tables/{table}`.  Authorization requires the following [IAM](https://cloud.google.com/iam/docs/) permission on the specified resource `parent`:   * `bigquery.tables.updateData` |
| `write_stream` | `WriteStream`  Required. Stream to be created. |

## DataFormat

Data format for input or output data.

| Enums | |
| --- | --- |
| `DATA_FORMAT_UNSPECIFIED` |  |
| `AVRO` | Avro is a standard open source row based file format. See <https://avro.apache.org/> for more details. |
| `ARROW` | Arrow is a standard open source column-based message format. See <https://arrow.apache.org/> for more details. |

## FinalizeWriteStreamRequest

Request message for invoking `FinalizeWriteStream`.

| Fields | |
| --- | --- |
| `name` | `string`  Required. Name of the stream to finalize, in the form of `projects/{project}/datasets/{dataset}/tables/{table}/streams/{stream}`.  Authorization requires the following [IAM](https://cloud.google.com/iam/docs/) permission on the specified resource `name`:   * `bigquery.tables.updateData` |

## FinalizeWriteStreamResponse

Response message for `FinalizeWriteStream`.

| Fields | |
| --- | --- |
| `row_count` | `int64`  Number of rows in the finalized stream. |

## FlushRowsRequest

Request message for `FlushRows`.

| Fields | |
| --- | --- |
| `write_stream` | `string`  Required. The stream that is the target of the flush operation.  Authorization requires the following [IAM](https://cloud.google.com/iam/docs/) permission on the specified resource `writeStream`:   * `bigquery.tables.updateData` |
| `offset` |  |