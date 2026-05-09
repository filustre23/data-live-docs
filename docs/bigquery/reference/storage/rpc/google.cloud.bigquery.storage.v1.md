* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback

# Package google.cloud.bigquery.storage.v1 Stay organized with collections Save and categorize content based on your preferences.

## Index

* `BigQueryRead` (interface)
* `BigQueryWrite` (interface)
* `AppendRowsRequest` (message)
* `AppendRowsRequest.MissingValueInterpretation` (enum)
* `AppendRowsRequest.ProtoData` (message)
* `AppendRowsResponse` (message)
* `AppendRowsResponse.AppendResult` (message)
* `ArrowRecordBatch` (message)
* `ArrowSchema` (message)
* `ArrowSerializationOptions` (message)
* `ArrowSerializationOptions.CompressionCodec` (enum)
* `ArrowSerializationOptions.PicosTimestampPrecision` (enum)
* `AvroRows` (message)
* `AvroSchema` (message)
* `AvroSerializationOptions` (message)
* `AvroSerializationOptions.PicosTimestampPrecision` (enum)
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
* `WriteStreamView` (enum)

## BigQueryRead

BigQuery Read API.

The Read API can be used to read data from BigQuery.

| CreateReadSession |
| --- |
| `rpc CreateReadSession(CreateReadSessionRequest) returns (ReadSession)`  Creates a new read session. A read session divides the contents of a BigQuery table into one or more streams, which can then be used to read data from the table. The read session also specifies properties of the data to be read, such as a list of columns or a push-down filter describing the rows to be returned.  A particular row can be read by at most one stream. When the caller has reached the end of each stream in the session, then all the data in the table has been read.  Data is assigned to each stream such that roughly the same number of rows can be read from each stream. Because the server-side unit for assigning data is collections of rows, the API does not guarantee that each stream will return the same number or rows. Additionally, the limits are enforced based on the number of pre-filtered rows, so some filters can lead to lopsided assignments.  Read sessions automatically expire 6 hours after they are created and do not require manual clean-up by the caller. |

| ReadRows |
| --- |
| `rpc ReadRows(ReadRowsRequest) returns (ReadRowsResponse)`  Reads rows from the stream in the format prescribed by the ReadSession. Each response contains one or more table rows, up to a maximum of 128 MB per response; read requests which attempt to read individual rows larger than 128 MB will fail.  Each request also returns a set of stream statistics reflecting the current state of the stream. |

| SplitReadStream |
| --- |
| `rpc SplitReadStream(SplitReadStreamRequest) returns (SplitReadStreamResponse)`  Splits a given `ReadStream` into two `ReadStream` objects. These `ReadStream` objects are referred to as the primary and the residual streams of the split. The original `ReadStream` can still be read from in the same manner as before. Both of the returned `ReadStream` objects can also be read from, and the rows returned by both child streams will be the same as the rows read from the original stream.  Moreover, the two child streams will be allocated back-to-back in the original `ReadStream`. Concretely, it is guaranteed that for streams original, primary, and residual, that original[0-j] = primary[0-j] and original[j-n] = residual[0-m] once the streams have been read to completion. |

## BigQueryWrite

BigQuery Write API.

The Write API can be used to write data to BigQuery.

For supplementary information about the Write API, see: <https://cloud.google.com/bigquery/docs/write-api>

| AppendRows |
| --- |
| `rpc AppendRows(AppendRowsRequest) returns (AppendRowsResponse)`  Appends data to the given stream.  If `offset` is specified, the `offset` is checked against the end of stream. The server returns `OUT_OF_RANGE` in `AppendRowsResponse` if an attempt is made to append to an offset beyond the current end of the stream or `ALREADY_EXISTS` if user provides an `offset` that has already been written to. User can retry with adjusted offset within the same RPC connection. If `offset` is not specified, append happens at the end of the stream.  The response contains an optional offset at which the append happened. No offset information will be returned for appends to a default stream.  Responses are received in the same order in which requests are sent. There will be one response for each successful inserted request. Responses may optionally embed error information if the originating AppendRequest was not successfully processed.  The specifics of when successfully appended data is made visible to the table are governed by the type of stream:   * For COMMITTED streams (which includes the default stream), data is visible immediately upon successful append. * For BUFFERED streams, data is made visible via a subsequent `FlushRows` rpc which advances a cursor to a newer offset in the stream. * For PENDING streams, data is not made visible until the stream itself is finalized (via the `FinalizeWriteStream` rpc), and the stream is explicitly committed via the `BatchCommitWriteStreams` rpc. |

| BatchCommitWriteStreams |
| --- |
| `rpc BatchCommitWriteStreams(BatchCommitWriteStreamsRequest) returns (BatchCommitWriteStreamsResponse)`  Atomically commits a group of `PENDING` streams that belong to the same `parent` table.  Streams must be finalized before commit and cannot be committed multiple times. Once a stream is committed, data in the stream becomes available for read operations. |

| CreateWriteStream |
| --- |
| `rpc CreateWriteStream(CreateWriteStreamRequest) returns (WriteStream)`  Creates a write stream to the given table. Additionally, every table has a special stream named '\_default' to which data can be written. This stream doesn't need to be created using CreateWriteStream. It is a stream that can be used simultaneously by any number of clients. Data written to this stream is considered committed as soon as an acknowledgement is received. |

| FinalizeWriteStream |
| --- |
| `rpc FinalizeWriteStream(FinalizeWriteStreamRequest) returns (FinalizeWriteStreamResponse)`  Finalize a write stream so that no new data can be appended to the stream. Finalize is not supported on the '\_default' stream. |

| FlushRows |
| --- |
| `rpc FlushRows(FlushRowsRequest) returns (FlushRowsResponse)`  Flushes rows to a BUFFERED stream.  If users are appending rows to BUFFERED stream, flush operation is required in order for the rows to become available for reading. A Flush operation flushes up to any previously flushed offset in a BUFFERED stream, to the offset specified in the request.  Flush is not supported on the \_default stream, since it is not BUFFERED. |

| GetWriteStream |
| --- |
| `rpc GetWriteStream(GetWriteStreamRequest) returns (WriteStream)`  Gets information about a write stream. |

## AppendRowsRequest

Request message for `AppendRows`.

Because AppendRows is a bidirectional streaming RPC, certain parts of the AppendRowsRequest need only be specified for the first request before switching table destinations. You can also switch table destinations within the same connection for the default stream.

The size of a single AppendRowsRequest must be less than 20 MB in size. Requests larger than this return an error, typically `INVALID_ARGUMENT`.

| Fields | |
| --- | --- |
| `write_stream` | `string`  Required. The write\_stream identifies the append operation. It must be provided in the following scenarios:   * In the first request to an AppendRows connection. * In all subsequent requests to an AppendRows connection, if you use the same connection to write to multiple tables or change the input schema for default streams.   For explicitly created write streams, the format is:   * `projects/{project}/datasets/{dataset}/tables/{table}/streams/{id}`   For the special default stream, the format is:   * `projects/{project}/datasets/{dataset}/tables/{table}/streams/_default`.   An example of a possible sequence of requests with write\_stream fields within a single connection:   * r1: {write\_stream: stream\_name\_1} * r2: {write\_stream: /\*omit\*/} * r3: {write\_stream: /\*omit\*/} * r4: {write\_stream: stream\_name\_2} * r5: {write\_stream: stream\_name\_2}   The destination changed in request\_4, so the write\_stream field must be populated in all subsequent requests in this stream.  Authorization requires the following [IAM](https://cloud.google.com/iam/docs/) permission on the specified resource `writeStream`:   * `bigquery.tables.updateData` |
| `offset` | `Int64Value`  If present, the write is only performed if the next append offset is same as the provided value. If not present, the write is performed at the current end of stream. Specifying a value for this field is not allowed when calling AppendRows for the '\_default' stream. |
| `trace_id` | `string`  Id set by client to annotate its identity. Only initial request setting is respected. |
| `missing_value_interpretations` | `map<string, MissingValueInterpretation>`  A map to indicate how to interpret missing value for some fields. Missing values are fields present in user schema but missing in rows. The key is the field name. The value is the interpretation of missing values for the field.  For example, a map {'foo': NULL\_VALUE, 'bar': DEFAULT\_VALUE} means all missing values in field foo are interpreted as NULL, all missing values in field bar are interpreted as the default value of field bar in table schema.  If a field is not in this map and has missing values, the missing values in this field are interpreted as NULL.  This field only applies to the current request, it won't affect other requests on the connection.  Currently, field name can only be top-level column name, can't be a struct field path like 'foo.bar'. |
| Union field `rows`. Input rows. The `writer_schema` field must be specified at the initial request and currently, it will be ignored if specified in following requests. Following requests must have data in the same format as the initial request. `rows` can be only one of the following: | |
| `proto_rows` | `ProtoData`  Rows in proto format. |

## MissingValueInterpretation

An enum to indicate how to interpret missing values of fields that are present in user schema but missing in rows. A missing value can represent a NULL or a column default value defined in BigQuery table schema.

| Enums | |
| --- | --- |
| `MISSING_VALUE_INTERPRETATION_UNSPECIFIED` | Invalid missing value interpretation. Requests with this value will be rejected. |
| `NULL_VALUE` | Missing value is interpreted as NULL. |
| `DEFAULT_VALUE` | Missing value is interpreted as column default value if declared in the table schema, NULL otherwise. |

## ProtoData

ProtoData contains the data rows and schema when constructing append requests.

| Fields | |
| --- | --- |
| `writer_schema` | `ProtoSchema`  Optional. The protocol buffer schema used to serialize the data. Provide this value whenever:   * You send the first request of an RPC connection. * You change the input schema. * You specify a new destination table. |
| `rows` | `ProtoRows`  Required. Serialized row data in protobuf message format. Currently, the backend expects the serialized rows to adhere to proto2 semantics when appending rows, particularly with respect to how default values are encoded. |

## AppendRowsResponse

Response message for `AppendRows`.

| Fields | |
| --- | --- |
| `updated_schema` | `TableSchema`  If backend detects a schema update, pass it to user so that user can use it to input new type of message. It will be empty when no schema updates have occurred. |
| `row_errors[]` | `RowError`  If a request failed due to corrupted rows, no rows in the batch will be appended. The API will return row level error info, so that the caller can remove the bad rows and retry the request. |
| `write_stream` | `string`  The target of the append operation. Matches the write\_stream in the corresponding request. |
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
| `row_count (deprecated)` | `int64`  This item is deprecated!  [Deprecated] The count of rows in `serialized_record_batch`. Please use the format-independent ReadRowsResponse.row\_count instead. |

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
| `buffer_compression` | `CompressionCodec`  The compression codec to use for Arrow buffers in serialized record batches. |
| `picos_timestamp_precision` | `PicosTimestampPrecision`  Optional. Set timestamp precision option. If not set, the default precision is microseconds. |

## CompressionCodec

Compression codec's supported by Arrow.

| Enums | |
| --- | --- |
| `COMPRESSION_UNSPECIFIED` | If unspecified no compression will be used. |
| `LZ4_FRAME` | LZ4 Frame (<https://github.com/lz4/lz4/blob/dev/doc/lz4_Frame_format.md>) |
| `ZSTD` | Zstandard compression. |

## PicosTimestampPrecision

The precision of the timestamp value in the Avro message. This precision will **only** be applied to the column(s) with the `TIMESTAMP_PICOS` type.

| Enums | |
| --- | --- |
| `PICOS_TIMESTAMP_PRECISION_UNSPECIFIED` | Unspecified timestamp precision. The default precision is microseconds. |
| `TIMESTAMP_PRECISION_MICROS` | Timestamp values returned by Read API will be truncated to microsecond level precision. The value will be encoded as Arrow TIMESTAMP type in a 64 bit integer. |
| `TIMESTAMP_PRECISION_NANOS` | Timestamp values returned by Read API will be truncated to nanosecond level precision. The value will be encoded as Arrow TIMESTAMP type in a 64 bit integer. |
| `TIMESTAMP_PRECISION_PICOS` | Read API will return full precision picosecond value. The value will be encoded as a string which conforms to ISO 8601 format. |

## AvroRows

Avro rows.

| Fields | |
| --- | --- |
| `serialized_binary_rows` | `bytes`  Binary serialized rows in a block. |
| `row_count (deprecated)` | `int64`  This item is deprecated!  [Deprecated] The count of rows in the returning block. Please use the format-independent ReadRowsResponse.row\_count instead. |

## AvroSchema

Avro schema.

| Fields | |
| --- | --- |
| `schema` | `string`  Json serialized schema, as described at <https://avro.apache.org/docs/1.8.1/spec.html>. |

## AvroSerializationOptions

Contains options specific to Avro Serialization.

| Fields | |
| --- | --- |
| `enable_display_name_attribute` | `bool`  Enable displayName attribute in Avro schema.  The Avro specification requires field names to be alphanumeric. By default, in cases when column names do not conform to these requirements (e.g. non-ascii unicode codepoints) and Avro is requested as an output format, the CreateReadSession call will fail.  Setting this field to true, populates avro field names with a placeholder value and populates a "displayName" attribute for every avro field with the original column name. |
| `picos_timestamp_precision` | `PicosTimestampPrecision`  Optional. Set timestamp precision option. If not set, the default precision is microseconds. |

## PicosTimestampPrecision

The precision of the timestamp value in the Avro message. This precision will **only** be applied to the column(s) with the `TIMESTAMP_PICOS` type.

| Enums | |
| --- | --- |
| `PICOS_TIMESTAMP_PRECISION_UNSPECIFIED` | Unspecified timestamp precision. The default precision is microseconds. |
| `TIMESTAMP_PRECISION_MICROS` | Timestamp values returned by Read API will be truncated to microsecond level precision. The value will be encoded as Avro TIMESTAMP type in a 64 bit integer. |
| `TIMESTAMP_PRECISION_NANOS` | Timestamp values returned by Read API will be truncated to nanosecond level precision. The value will be encoded as Avro TIMESTAMP type in a 64 bit integer. |
| `TIMESTAMP_PRECISION_PICOS` | Read API will return full precision picosecond value. The value will be encoded as a string which conforms to ISO 8601 format. |

## BatchCommitWriteStreamsRequest

Request message for `BatchCommitWriteStreams`.

| Fields | |
| --- | --- |
| `parent` | `string`  Required. Parent table that all the streams should belong to, in the form of `projects/{project}/datasets/{dataset}/tables/{table}`.  Authorization requires the following [IAM](https://cloud.google.com/iam/docs/) permission on the specified resource |