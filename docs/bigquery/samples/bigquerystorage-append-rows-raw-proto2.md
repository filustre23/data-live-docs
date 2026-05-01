* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [範例](https://docs.cloud.google.com/bigquery/docs/samples?hl=zh-tw)

# 使用靜態通訊協定緩衝區附加資料列 透過集合功能整理內容 你可以依據偏好儲存及分類內容。

這個範例說明如何使用通訊協定緩衝區，將資料寫入 BigQuery 資料表。

## 程式碼範例

### Node.js

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Node.js 設定說明操作。詳情請參閱 [BigQuery Node.js API 參考說明文件](https://googleapis.dev/nodejs/bigquery/latest/index.html)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
const {adapt, managedwriter} = require('@google-cloud/bigquery-storage');
const {WriterClient, Writer} = managedwriter;

const sample_data_pb = require('./sample_data_pb.js');
const {SampleData} = sample_data_pb;

const protobufjs = require('protobufjs');
require('protobufjs/ext/descriptor');

async function appendRowsProto2() {
  /**
   * If you make updates to the sample_data.proto protocol buffers definition,
   * run:
   *   pbjs sample_data.proto -t static-module -w commonjs -o sample_data.js
   *   pbjs sample_data.proto -t json --keep-case -o sample_data.json
   * from the /samples directory to generate the sample_data module.
   */

  // So that BigQuery knows how to parse the serialized_rows, create a
  // protocol buffer representation of your message descriptor.
  const root = protobufjs.loadSync('./sample_data.json');
  const descriptor = root.lookupType('SampleData').toDescriptor('proto2');
  const protoDescriptor = adapt.normalizeDescriptor(descriptor).toJSON();

  /**
   * TODO(developer): Uncomment the following lines before running the sample.
   */
  // projectId = 'my_project';
  // datasetId = 'my_dataset';
  // tableId = 'my_table';

  const destinationTable = `projects/${projectId}/datasets/${datasetId}/tables/${tableId}`;
  const streamType = managedwriter.PendingStream;
  const writeClient = new WriterClient({projectId});

  try {
    const streamId = await writeClient.createWriteStream({
      streamType,
      destinationTable,
    });
    console.log(`Stream created: ${streamId}`);

    const connection = await writeClient.createStreamConnection({
      streamId,
    });

    const writer = new Writer({
      connection,
      protoDescriptor,
    });

    let serializedRows = [];
    const pendingWrites = [];

    // Row 1
    let row = {
      rowNum: 1,
      boolCol: true,
      bytesCol: Buffer.from('hello world'),
      float64Col: parseFloat('+123.45'),
      int64Col: 123,
      stringCol: 'omg',
    };
    serializedRows.push(SampleData.encode(row).finish());

    // Row 2
    row = {
      rowNum: 2,
      boolCol: false,
    };
    serializedRows.push(SampleData.encode(row).finish());

    // Row 3
    row = {
      rowNum: 3,
      bytesCol: Buffer.from('later, gator'),
    };
    serializedRows.push(SampleData.encode(row).finish());

    // Row 4
    row = {
      rowNum: 4,
      float64Col: 987.654,
    };
    serializedRows.push(SampleData.encode(row).finish());

    // Row 5
    row = {
      rowNum: 5,
      int64Col: 321,
    };
    serializedRows.push(SampleData.encode(row).finish());

    // Row 6
    row = {
      rowNum: 6,
      stringCol: 'octavia',
    };
    serializedRows.push(SampleData.encode(row).finish());

    // Set an offset to allow resuming this stream if the connection breaks.
    // Keep track of which requests the server has acknowledged and resume the
    // stream at the first non-acknowledged message. If the server has already
    // processed a message with that offset, it will return an ALREADY_EXISTS
    // error, which can be safely ignored.

    // The first request must always have an offset of 0.
    let offsetValue = 0;

    // Send batch.
    let pw = writer.appendRows({serializedRows}, offsetValue);
    pendingWrites.push(pw);

    // Reset rows.
    serializedRows = [];

    // Row 7
    const days = new Date('2019-02-07').getTime() / (1000 * 60 * 60 * 24);
    row = {
      rowNum: 7,
      dateCol: days, // The value is the number of days since the Unix epoch (1970-01-01)
    };
    serializedRows.push(SampleData.encode(row).finish());

    // Row 8
    row = {
      rowNum: 8,
      datetimeCol: '2019-02-17 11:24:00.000',
    };
    serializedRows.push(SampleData.encode(row).finish());

    // Row 9
    row = {
      rowNum: 9,
      geographyCol: 'POINT(5 5)',
    };
    serializedRows.push(SampleData.encode(row).finish());

    // Row 10
    row = {
      rowNum: 10,
      numericCol: '123456',
      bignumericCol: '99999999999999999999999999999.999999999',
    };
    serializedRows.push(SampleData.encode(row).finish());

    // Row 11
    row = {
      rowNum: 11,
      timeCol: '18:00:00',
    };
    serializedRows.push(SampleData.encode(row).finish());

    // Row 12
    const timestamp = new Date('2022-01-09T03:49:46.564Z').getTime();
    row = {
      rowNum: 12,
      timestampCol: timestamp * 1000, // The value is given in microseconds since the Unix epoch (1970-01-01)
    };
    serializedRows.push(SampleData.encode(row).finish());

    // Offset must equal the number of rows that were previously sent.
    offsetValue = 6;

    // Send batch.
    pw = writer.appendRows({serializedRows}, offsetValue);
    pendingWrites.push(pw);

    serializedRows = [];

    // Row 13
    row = {
      rowNum: 13,
      int64List: [1999, 2001],
    };
    serializedRows.push(SampleData.encode(row).finish());

    // Row 14
    row = {
      rowNum: 14,
      structCol: {
        subIntCol: 99,
      },
    };
    serializedRows.push(SampleData.encode(row).finish());

    // Row 15
    row = {
      rowNum: 15,
      structList: [{subIntCol: 100}, {subIntCol: 101}],
    };
    serializedRows.push(SampleData.encode(row).finish());

    // Row 16
    const timestampStart = new Date('2022-01-09T03:49:46.564Z').getTime();
    const timestampEnd = new Date('2022-01-09T04:49:46.564Z').getTime();
    row = {
      rowNum: 16,
      rangeCol: {
        start: timestampStart * 1000,
        end: timestampEnd * 1000,
      },
    };
    serializedRows.push(SampleData.encode(row).finish());

    offsetValue = 12;

    // Send batch.
    pw = writer.appendRows({serializedRows}, offsetValue);
    pendingWrites.push(pw);

    const results = await Promise.all(
      pendingWrites.map(pw => pw.getResult()),
    );
    console.log('Write results:', results);

    const {rowCount} = await connection.finalize();
    console.log(`Row count: ${rowCount}`);

    const response = await writeClient.batchCommitWriteStream({
      parent: destinationTable,
      writeStreams: [streamId],
    });

    console.log(response);
  } catch (err) {
    console.log(err);
  } finally {
    writeClient.close();
  }
}
```

### Python

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Python 設定說明操作。詳情請參閱 [BigQuery Python API 參考說明文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
"""
This code sample demonstrates using the low-level generated client for Python.
"""

import datetime
import decimal

from google.protobuf import descriptor_pb2

from google.cloud import bigquery_storage_v1
from google.cloud.bigquery_storage_v1 import types, writer

# If you make updates to the sample_data.proto protocol buffers definition,
# run:
#
#   protoc --python_out=. sample_data.proto
#
# from the samples/snippets directory to generate the sample_data_pb2 module.
from . import sample_data_pb2


def append_rows_proto2(project_id: str, dataset_id: str, table_id: str):
    """Create a write stream, write some sample data, and commit the stream."""
    write_client = bigquery_storage_v1.BigQueryWriteClient()
    parent = write_client.table_path(project_id, dataset_id, table_id)
    write_stream = types.WriteStream()

    # When creating the stream, choose the type. Use the PENDING type to wait
    # until the stream is committed before it is visible. See:
    # https://cloud.google.com/bigquery/docs/reference/storage/rpc/google.cloud.bigquery.storage.v1#google.cloud.bigquery.storage.v1.WriteStream.Type
    write_stream.type_ = types.WriteStream.Type.PENDING
    write_stream = write_client.create_write_stream(
        parent=parent, write_stream=write_stream
    )
    stream_name = write_stream.name

    # Create a template with fields needed for the first request.
    request_template = types.AppendRowsRequest()

    # The initial request must contain the stream name.
    request_template.write_stream = stream_name

    # So that BigQuery knows how to parse the serialized_rows, generate a
    # protocol buffer representation of your message descriptor.
    proto_schema = types.ProtoSchema()
    proto_descriptor = descriptor_pb2.DescriptorProto()
    sample_data_pb2.SampleData.DESCRIPTOR.CopyToProto(proto_descriptor)
    proto_schema.proto_descriptor = proto_descriptor
    proto_data = types.AppendRowsRequest.ProtoData()
    proto_data.writer_schema = proto_schema
    request_template.proto_rows = proto_data

    # Some stream types support an unbounded number of requests. Construct an
    # AppendRowsStream to send an arbitrary number of requests to a stream.
    append_rows_stream = writer.AppendRowsStream(write_client, request_template)

    # Create a batch of row data by appending proto2 serialized bytes to the
    # serialized_rows repeated field.
    proto_rows = types.ProtoRows()

    row = sample_data_pb2.SampleData()
    row.row_num = 1
    row.bool_col = True
    row.bytes_col = b"Hello, World!"
    row.float64_col = float("+inf")
    row.int64_col = 123
    row.string_col = "Howdy!"
    proto_rows.serialized_rows.append(row.SerializeToString())

    row = sample_data_pb2.SampleData()
    row.row_num = 2
    row.bool_col = False
    proto_rows.serialized_rows.append(row.SerializeToString())

    row = sample_data_pb2.SampleData()
    row.row_num = 3
    row.bytes_col = b"See you later!"
    proto_rows.serialized_rows.append(row.SerializeToString())

    row = sample_data_pb2.SampleData()
    row.row_num = 4
    row.float64_col = 1000000.125
    proto_rows.serialized_rows.append(row.SerializeToString())

    row = sample_data_pb2.SampleData()
    row.row_num = 5
    row.int64_col = 67000
    proto_rows.serialized_rows.append(row.SerializeToString())

    row = sample_data_pb2.SampleData()
    row.row_num = 6
    row.string_col = "Auf Wiedersehen!"
    proto_rows.serialized_rows.append(row.SerializeToString())

    # Set an offset to allow resuming this stream if the connection breaks.
    # Keep track of which requests the server has acknowledged and resume the
    # stream at the first non-acknowledged message. If the server has already
    # processed a message with that offset, it will return an ALREADY_EXISTS
    # error, which can be safely ignored.
    #
    # The first request must always have an offset of 0.
    request = types.AppendRowsRequest()
    request.offset = 0
    proto_data = types.AppendRowsRequest.ProtoData()
    proto_data.rows = proto_rows
    request.proto_rows = proto_data

    response_future_1 = append_rows_stream.send(request)

    # Create a batch of rows containing scalar values that don't directly
    # correspond to a protocol buffers scalar type. See the documentation for
    # the expected data formats:
    # https://cloud.google.com/bigquery/docs/write-api#data_type_conversions
    proto_rows = types.ProtoRows()

    row = sample_data_pb2.SampleData()
    row.row_num = 7
    date_value = datetime.date(2021, 8, 12)
    epoch_value = datetime.date(1970, 1, 1)
    delta = date_value - epoch_value
    row.date_col = delta.days
    proto_rows.serialized_rows.append(row.SerializeToString())

    row = sample_data_pb2.SampleData()
    row.row_num = 8
    datetime_value = datetime.datetime(2021, 8, 12, 9, 46, 23, 987456)
    row.datetime_col = datetime_value.strftime("%Y-%m-%d %H:%M:%S.%f")
    proto_rows.serialized_rows.append(row.SerializeToString())

    row = sample_data_pb2.SampleData()
    row.row_num = 9
    row.geography_col = "POINT(-122.347222 47.651111)"
    proto_rows.serialized_rows.append(row.SerializeToString())

    row = sample_data_pb2.SampleData()
    row.row_num = 10
    numeric_value = decimal.Decimal("1.23456789101112e+6")
    row.numeric_col = str(numeric_value)
    bignumeric_value = decimal.Decimal("-1.234567891011121314151617181920e+16")
    row.bignumeric_col = str(bignumeric_value)
    proto_rows.serialized_rows.append(row.SerializeToString())

    row = sample_data_pb2.SampleData()
    row.row_num = 11
    time_value = datetime.time(11, 7, 48, 123456)
    row.time_col = time_value.strftime("%H:%M:%S.%f")
    proto_rows.serialized_rows.append(row.SerializeToString())

    row = sample_data_pb2.SampleData()
    row.row_num = 12
    timestamp_value = datetime.datetime(
        2021, 8, 12, 16, 11, 22, 987654, tzinfo=datetime.timezone.utc
    )
    epoch_value = datetime.datetime(1970, 1, 1, tzinfo=datetime.timezone.utc)
    delta = timestamp_value - epoch_value
    row.timestamp_col = int(delta.total_seconds()) * 1000000 + int(delta.microseconds)
    proto_rows.serialized_rows.append(row.SerializeToString())

    # Since this is the second request, you only need to include the row data.
    # The name of the stream and protocol buffers DESCRIPTOR is only needed in
    # the first request.
    request = types.AppendRowsRequest()
    proto_data = types.AppendRowsRequest.ProtoData()
    proto_data.rows = proto_rows
    request.proto_rows = proto_data

    # Offset must equal the number of rows that were previously sent.
    request.offset = 6

    response_future_2 = append_rows_stream.send(request)

    # Create a batch of rows with STRUCT and ARRAY BigQuery data types. In
    # protocol buffers, these correspond to nested messages and repeated
    # fields, respectively.
    proto_rows = types.ProtoRows()

    row = sample_data_pb2.SampleData()
    row.row_num = 13
    row.int64_list.append(1)
    row.int64_list.append(2)
    row.int64_list.append(3)
    proto_rows.serialized_rows.append(row.SerializeToString())

    row = sample_data_pb2.SampleData()
    row.row_num = 14
    row.struct_col.sub_int_col = 7
    proto_rows.serialized_rows.append(row.SerializeToString())

    row = sample_data_pb2.SampleData()
    row.row_num = 15
    sub_message = sample_data_pb2.SampleData.SampleStruct()
    sub_message.sub_int_col = -1
    row.struct_list.append(sub_message)
    sub_message = sample_data_pb2.SampleData.SampleStruct()
    sub_message.sub_int_col = -2
    row.struct_list.append(sub_message)
    sub_message = sample_data_pb2.SampleData.SampleStruct()
    sub_message.sub_int_col = -3
    row.struct_list.append(sub_message)
    proto_rows.serialized_rows.append(row.SerializeToString())

    row = sample_data_pb2.SampleData()
    row.row_num = 16
    date_value = datetime.date(2021, 8, 8)
    epoch_value = datetime.date(1970, 1, 1)
    delta = date_value - epoch_value
    row.range_date.start = delta.days
    proto_rows.serialized_rows.append(row.SerializeToString())

    request = types.AppendRowsRequest()
    request.offset = 12
    proto_data = types.AppendRowsRequest.ProtoData()
    proto_data.rows = proto_rows
    request.proto_rows = proto_data

    # For each request sent, a message is expected in the responses iterable.
    # This sample sends 3 requests, therefore expect exactly 3 responses.
    response_future_3 = append_rows_stream.send(request)

    # All three requests are in-flight, wait for them to finish being processed
    # before finalizing the stream.
    print(response_future_1.result())
    print(response_future_2.result())
    print(response_future_3.result())

    # Shutdown background threads and close the streaming connection.
    append_rows_stream.close()

    # A PENDING type stream must be "finalized" before being committed. No new
    # records can be written to the stream after this method has been called.
    write_client.finalize_write_stream(name=write_stream.name)

    # Commit the stream you created earlier.
    batch_commit_write_streams_request = types.BatchCommitWriteStreamsRequest()
    batch_commit_write_streams_request.parent = parent
    batch_commit_write_streams_request.write_streams = [write_stream.name]
    write_client.batch_commit_write_streams(batch_commit_write_streams_request)

    print(f"Writes to stream: '{write_stream.name}' have been committed.")
```

## 後續步驟

如要搜尋及篩選其他 Google Cloud 產品的程式碼範例，請參閱[Google Cloud 範例瀏覽工具](https://docs.cloud.google.com/docs/samples?product=bigquerystorage&hl=zh-tw)。

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。




[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],[],[],[]]