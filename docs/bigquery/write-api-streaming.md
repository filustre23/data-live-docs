Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 使用 Storage Write API 串流資料

本文說明如何使用 [BigQuery Storage Write API](https://docs.cloud.google.com/bigquery/docs/write-api?hl=zh-tw)，將資料串流至 BigQuery。

在串流情境中，資料會持續傳入，且應以最短延遲時間供讀取。使用 BigQuery Storage Write API 處理串流工作負載時，請考量您需要哪些保證：

* 如果應用程式只需要「至少一次」語意，請使用**預設串流**。
* 如需僅一次語意，請在**已提交類型**中建立一或多個串流，並使用串流偏移保證僅寫入一次。

在已提交類型中，伺服器確認寫入要求後，即可查詢寫入串流的資料。預設串流也會使用已提交的類型，但無法提供「只傳送一次」的保證。

## 針對至少一次語意使用預設串流

如果應用程式可接受目的地資料表中出現重複記錄的可能性，建議您使用[預設串流](https://docs.cloud.google.com/bigquery/docs/write-api?hl=zh-tw#default_stream)進行串流作業。

下列程式碼顯示如何將資料寫入預設串流：

### Java

如要瞭解如何安裝及使用 BigQuery 的用戶端程式庫，請參閱「[BigQuery 用戶端程式庫](https://docs.cloud.google.com/bigquery/docs/reference/storage/libraries?hl=zh-tw)」。詳情請參閱 [BigQuery Java API 參考說明文件](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquerystorage/latest/com.google.cloud.bigquery.storage.v1?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import com.google.api.core.ApiFuture;
import com.google.api.core.ApiFutureCallback;
import com.google.api.core.ApiFutures;
import com.google.api.gax.batching.FlowControlSettings;
import com.google.api.gax.core.FixedExecutorProvider;
import com.google.api.gax.retrying.RetrySettings;
import com.google.cloud.bigquery.BigQuery;
import com.google.cloud.bigquery.BigQueryOptions;
import com.google.cloud.bigquery.QueryJobConfiguration;
import com.google.cloud.bigquery.TableResult;
import com.google.cloud.bigquery.storage.v1.AppendRowsRequest;
import com.google.cloud.bigquery.storage.v1.AppendRowsResponse;
import com.google.cloud.bigquery.storage.v1.BigQueryWriteClient;
import com.google.cloud.bigquery.storage.v1.BigQueryWriteSettings;
import com.google.cloud.bigquery.storage.v1.Exceptions;
import com.google.cloud.bigquery.storage.v1.Exceptions.AppendSerializationError;
import com.google.cloud.bigquery.storage.v1.Exceptions.MaximumRequestCallbackWaitTimeExceededException;
import com.google.cloud.bigquery.storage.v1.Exceptions.StorageException;
import com.google.cloud.bigquery.storage.v1.Exceptions.StreamWriterClosedException;
import com.google.cloud.bigquery.storage.v1.JsonStreamWriter;
import com.google.cloud.bigquery.storage.v1.TableName;
import com.google.common.util.concurrent.MoreExecutors;
import com.google.protobuf.ByteString;
import com.google.protobuf.Descriptors.DescriptorValidationException;
import java.io.IOException;
import java.util.Map;
import java.util.concurrent.Executors;
import java.util.concurrent.Phaser;
import java.util.concurrent.atomic.AtomicInteger;
import javax.annotation.concurrent.GuardedBy;
import org.json.JSONArray;
import org.json.JSONObject;
import org.threeten.bp.Duration;

public class WriteToDefaultStream {

  public static void runWriteToDefaultStream()
      throws DescriptorValidationException, InterruptedException, IOException {
    // TODO(developer): Replace these variables before running the sample.
    String projectId = "MY_PROJECT_ID";
    String datasetName = "MY_DATASET_NAME";
    String tableName = "MY_TABLE_NAME";
    writeToDefaultStream(projectId, datasetName, tableName);
  }

  private static ByteString buildByteString() {
    byte[] bytes = new byte[] {1, 2, 3, 4, 5};
    return ByteString.copyFrom(bytes);
  }

  // Create a JSON object that is compatible with the table schema.
  private static JSONObject buildRecord(int i, int j) {
    JSONObject record = new JSONObject();
    StringBuilder sbSuffix = new StringBuilder();
    for (int k = 0; k < j; k++) {
      sbSuffix.append(k);
    }
    record.put("test_string", String.format("record %03d-%03d %s", i, j, sbSuffix.toString()));
    ByteString byteString = buildByteString();
    record.put("test_bytes", byteString);
    record.put(
        "test_geo",
        "POLYGON((-124.49 47.35,-124.49 40.73,-116.49 40.73,-116.49 47.35,-124.49 47.35))");
    return record;
  }

  public static void writeToDefaultStream(String projectId, String datasetName, String tableName)
      throws DescriptorValidationException, InterruptedException, IOException {
    TableName parentTable = TableName.of(projectId, datasetName, tableName);

    DataWriter writer = new DataWriter();
    // One time initialization for the worker.
    writer.initialize(parentTable);

    // Write two batches of fake data to the stream, each with 10 JSON records.  Data may be
    // batched up to the maximum request size:
    // https://cloud.google.com/bigquery/quotas#write-api-limits
    for (int i = 0; i < 2; i++) {
      JSONArray jsonArr = new JSONArray();
      for (int j = 0; j < 10; j++) {
        JSONObject record = buildRecord(i, j);
        jsonArr.put(record);
      }

      writer.append(new AppendContext(jsonArr));
    }

    // Final cleanup for the stream during worker teardown.
    writer.cleanup();
    verifyExpectedRowCount(parentTable, 12L);
    System.out.println("Appended records successfully.");
  }

  private static void verifyExpectedRowCount(TableName parentTable, long expectedRowCount)
      throws InterruptedException {
    String queryRowCount =
        "SELECT COUNT(*) FROM `"
            + parentTable.getProject()
            + "."
            + parentTable.getDataset()
            + "."
            + parentTable.getTable()
            + "`";
    QueryJobConfiguration queryConfig = QueryJobConfiguration.newBuilder(queryRowCount).build();
    BigQuery bigquery = BigQueryOptions.getDefaultInstance().getService();
    TableResult results = bigquery.query(queryConfig);
    long countRowsActual =
        Long.parseLong(results.getValues().iterator().next().get("f0_").getStringValue());
    if (countRowsActual != expectedRowCount) {
      throw new RuntimeException(
          "Unexpected row count. Expected: " + expectedRowCount + ". Actual: " + countRowsActual);
    }
  }

  private static class AppendContext {

    JSONArray data;

    AppendContext(JSONArray data) {
      this.data = data;
    }
  }

  private static class DataWriter {

    private static final int MAX_RECREATE_COUNT = 3;

    private BigQueryWriteClient client;

    // Track the number of in-flight requests to wait for all responses before shutting down.
    private final Phaser inflightRequestCount = new Phaser(1);
    private final Object lock = new Object();
    private JsonStreamWriter streamWriter;

    @GuardedBy("lock")
    private RuntimeException error = null;

    private AtomicInteger recreateCount = new AtomicInteger(0);

    private JsonStreamWriter createStreamWriter(String tableName)
        throws DescriptorValidationException, IOException, InterruptedException {
      // Configure in-stream automatic retry settings.
      // Error codes that are immediately retried:
      // * ABORTED, UNAVAILABLE, CANCELLED, INTERNAL, DEADLINE_EXCEEDED
      // Error codes that are retried with exponential backoff:
      // * RESOURCE_EXHAUSTED
      RetrySettings retrySettings =
          RetrySettings.newBuilder()
              .setInitialRetryDelay(Duration.ofMillis(500))
              .setRetryDelayMultiplier(1.1)
              .setMaxAttempts(5)
              .setMaxRetryDelay(Duration.ofMinutes(1))
              .build();

      // Use the JSON stream writer to send records in JSON format. Specify the table name to write
      // to the default stream.
      // For more information about JsonStreamWriter, see:
      // https://googleapis.dev/java/google-cloud-bigquerystorage/latest/com/google/cloud/bigquery/storage/v1/JsonStreamWriter.html
      return JsonStreamWriter.newBuilder(tableName, client)
          .setExecutorProvider(FixedExecutorProvider.create(Executors.newScheduledThreadPool(10)))
          .setChannelProvider(
              BigQueryWriteSettings.defaultGrpcTransportProviderBuilder()
                  .setKeepAliveTime(org.threeten.bp.Duration.ofMinutes(1))
                  .setKeepAliveTimeout(org.threeten.bp.Duration.ofMinutes(1))
                  .setKeepAliveWithoutCalls(true)
                  .setChannelsPerCpu(2)
                  .build())
          .setEnableConnectionPool(true)
          // This will allow connection pool to scale up better.
          .setFlowControlSettings(
              FlowControlSettings.newBuilder().setMaxOutstandingElementCount(100L).build())
          // If value is missing in json and there is a default value configured on bigquery
          // column, apply the default value to the missing value field.
          .setDefaultMissingValueInterpretation(
              AppendRowsRequest.MissingValueInterpretation.DEFAULT_VALUE)
          .setRetrySettings(retrySettings)
          .build();
    }

    public void initialize(TableName parentTable)
        throws DescriptorValidationException, IOException, InterruptedException {
      // Initialize client without settings, internally within stream writer a new client will be
      // created with full settings.
      client = BigQueryWriteClient.create();

      streamWriter = createStreamWriter(parentTable.toString());
    }

    public void append(AppendContext appendContext)
        throws DescriptorValidationException, IOException, InterruptedException {
      synchronized (this.lock) {
        if (!streamWriter.isUserClosed()
            && streamWriter.isClosed()
            && recreateCount.getAndIncrement() < MAX_RECREATE_COUNT) {
          streamWriter = createStreamWriter(streamWriter.getStreamName());
          this.error = null;
        }
        // If earlier appends have failed, we need to reset before continuing.
        if (this.error != null) {
          throw this.error;
        }
      }
      // Append asynchronously for increased throughput.
      ApiFuture<AppendRowsResponse> future = streamWriter.append(appendContext.data);
      ApiFutures.addCallback(
          future, new AppendCompleteCallback(this, appendContext), MoreExecutors.directExecutor());

      // Increase the count of in-flight requests.
      inflightRequestCount.register();
    }

    public void cleanup() {
      // Wait for all in-flight requests to complete.
      inflightRequestCount.arriveAndAwaitAdvance();

      client.close();
      // Close the connection to the server.
      streamWriter.close();

      // Verify that no error occurred in the stream.
      synchronized (this.lock) {
        if (this.error != null) {
          throw this.error;
        }
      }
    }

    static class AppendCompleteCallback implements ApiFutureCallback<AppendRowsResponse> {

      private final DataWriter parent;
      private final AppendContext appendContext;

      public AppendCompleteCallback(DataWriter parent, AppendContext appendContext) {
        this.parent = parent;
        this.appendContext = appendContext;
      }

      public void onSuccess(AppendRowsResponse response) {
        System.out.format("Append success\n");
        this.parent.recreateCount.set(0);
        done();
      }

      public void onFailure(Throwable throwable) {
        if (throwable instanceof AppendSerializationError) {
          AppendSerializationError ase = (AppendSerializationError) throwable;
          Map<Integer, String> rowIndexToErrorMessage = ase.getRowIndexToErrorMessage();
          if (rowIndexToErrorMessage.size() > 0) {
            // Omit the faulty rows
            JSONArray dataNew = new JSONArray();
            for (int i = 0; i < appendContext.data.length(); i++) {
              if (!rowIndexToErrorMessage.containsKey(i)) {
                dataNew.put(appendContext.data.get(i));
              } else {
                // process faulty rows by placing them on a dead-letter-queue, for instance
              }
            }

            // Retry the remaining valid rows, but using a separate thread to
            // avoid potentially blocking while we are in a callback.
            if (dataNew.length() > 0) {
              try {
                this.parent.append(new AppendContext(dataNew));
              } catch (DescriptorValidationException e) {
                throw new RuntimeException(e);
              } catch (IOException e) {
                throw new RuntimeException(e);
              } catch (InterruptedException e) {
                throw new RuntimeException(e);
              }
            }
            // Mark the existing attempt as done since we got a response for it
            done();
            return;
          }
        }

        boolean resendRequest = false;
        if (throwable instanceof MaximumRequestCallbackWaitTimeExceededException) {
          resendRequest = true;
        } else if (throwable instanceof StreamWriterClosedException) {
          if (!parent.streamWriter.isUserClosed()) {
            resendRequest = true;
          }
        }
        if (resendRequest) {
          // Retry this request.
          try {
            this.parent.append(new AppendContext(appendContext.data));
          } catch (DescriptorValidationException e) {
            throw new RuntimeException(e);
          } catch (IOException e) {
            throw new RuntimeException(e);
          } catch (InterruptedException e) {
            throw new RuntimeException(e);
          }
          // Mark the existing attempt as done since we got a response for it
          done();
          return;
        }

        synchronized (this.parent.lock) {
          if (this.parent.error == null) {
            StorageException storageException = Exceptions.toStorageException(throwable);
            this.parent.error =
                (storageException != null) ? storageException : new RuntimeException(throwable);
          }
        }
        done();
      }

      private void done() {
        // Reduce the count of in-flight requests.
        this.parent.inflightRequestCount.arriveAndDeregister();
      }
    }
  }
}
```

### Node.js

如要瞭解如何安裝及使用 BigQuery 的用戶端程式庫，請參閱「[BigQuery 用戶端程式庫](https://docs.cloud.google.com/bigquery/docs/reference/storage/libraries?hl=zh-tw)」。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
const {adapt, managedwriter} = require('@google-cloud/bigquery-storage');
const {WriterClient, JSONWriter} = managedwriter;

async function appendJSONRowsDefaultStream() {
  /**
   * TODO(developer): Uncomment the following lines before running the sample.
   */
  // projectId = 'my_project';
  // datasetId = 'my_dataset';
  // tableId = 'my_table';

  const destinationTable = `projects/${projectId}/datasets/${datasetId}/tables/${tableId}`;
  const writeClient = new WriterClient({projectId});

  try {
    const writeStream = await writeClient.getWriteStream({
      streamId: `${destinationTable}/streams/_default`,
      view: 'FULL',
    });
    const protoDescriptor = adapt.convertStorageSchemaToProto2Descriptor(
      writeStream.tableSchema,
      'root',
    );

    const connection = await writeClient.createStreamConnection({
      streamId: managedwriter.DefaultStream,
      destinationTable,
    });
    const streamId = connection.getStreamId();

    const writer = new JSONWriter({
      streamId,
      connection,
      protoDescriptor,
    });

    let rows = [];
    const pendingWrites = [];

    // Row 1
    let row = {
      row_num: 1,
      customer_name: 'Octavia',
    };
    rows.push(row);

    // Row 2
    row = {
      row_num: 2,
      customer_name: 'Turing',
    };
    rows.push(row);

    // Send batch.
    let pw = writer.appendRows(rows);
    pendingWrites.push(pw);

    rows = [];

    // Row 3
    row = {
      row_num: 3,
      customer_name: 'Bell',
    };
    rows.push(row);

    // Send batch.
    pw = writer.appendRows(rows);
    pendingWrites.push(pw);

    const results = await Promise.all(
      pendingWrites.map(pw => pw.getResult()),
    );
    console.log('Write results:', results);
  } catch (err) {
    console.log(err);
  } finally {
    writeClient.close();
  }
}
```

### Python

這個範例說明如何使用預設串流插入含有兩個欄位的記錄：

```
from google.cloud import bigquery_storage_v1
from google.cloud.bigquery_storage_v1 import types
from google.cloud.bigquery_storage_v1 import writer
from google.protobuf import descriptor_pb2
import logging
import json

import sample_data_pb2

# The list of columns from the table's schema to search in the given data to write to BigQuery.
TABLE_COLUMNS_TO_CHECK = [
    "name",
    "age"
    ]

# Function to create a batch of row data to be serialized.
def create_row_data(data):
    row = sample_data_pb2.SampleData()
    for field in TABLE_COLUMNS_TO_CHECK:
      # Optional fields will be passed as null if not provided
      if field in data:
        setattr(row, field, data[field])
    return row.SerializeToString()

class BigQueryStorageWriteAppend(object):

    # The stream name is: projects/{project}/datasets/{dataset}/tables/{table}/_default
    def append_rows_proto2(
        project_id: str, dataset_id: str, table_id: str, data: dict
    ):

        write_client = bigquery_storage_v1.BigQueryWriteClient()
        parent = write_client.table_path(project_id, dataset_id, table_id)
        stream_name = f'{parent}/_default'
        write_stream = types.WriteStream()

        # Create a template with fields needed for the first request.
        request_template = types.AppendRowsRequest()

        # The request must contain the stream name.
        request_template.write_stream = stream_name

        # Generating the protocol buffer representation of the message descriptor.
        proto_schema = types.ProtoSchema()
        proto_descriptor = descriptor_pb2.DescriptorProto()
        sample_data_pb2.SampleData.DESCRIPTOR.CopyToProto(proto_descriptor)
        proto_schema.proto_descriptor = proto_descriptor
        proto_data = types.AppendRowsRequest.ProtoData()
        proto_data.writer_schema = proto_schema
        request_template.proto_rows = proto_data

        # Construct an AppendRowsStream to send an arbitrary number of requests to a stream.
        append_rows_stream = writer.AppendRowsStream(write_client, request_template)

        # Append proto2 serialized bytes to the serialized_rows repeated field using create_row_data.
        proto_rows = types.ProtoRows()
        for row in data:
            proto_rows.serialized_rows.append(create_row_data(row))

        # Appends data to the given stream.
        request = types.AppendRowsRequest()
        proto_data = types.AppendRowsRequest.ProtoData()
        proto_data.rows = proto_rows
        request.proto_rows = proto_data

        append_rows_stream.send(request)

        print(f"Rows to table: '{parent}' have been written.")

if __name__ == "__main__":

    ###### Uncomment the below block to provide additional logging capabilities ######
    #logging.basicConfig(
    #    level=logging.DEBUG,
    #    format="%(asctime)s [%(levelname)s] %(message)s",
    #    handlers=[
    #        logging.StreamHandler()
    #    ]
    #)
    ###### Uncomment the above block to provide additional logging capabilities ######

    with open('entries.json', 'r') as json_file:
        data = json.load(json_file)
    # Change this to your specific BigQuery project, dataset, table details
    BigQueryStorageWriteAppend.append_rows_proto2("PROJECT_ID","DATASET_ID", "TABLE_ID ",data=data)
```

這個程式碼範例依附於已編譯的通訊協定模組 `sample_data_pb2.py`。如要建立已編譯的模組，請執行 `protoc --python_out=. sample_data.proto` 指令，其中 `protoc` 是通訊協定緩衝區編譯器。`sample_data.proto` 檔案定義 Python 範例中使用的訊息格式。如要安裝 `protoc` 編譯器，請按照「[通訊協定緩衝區 - Google 的資料交換格式](https://github.com/protocolbuffers/protobuf)」中的操作說明進行。

以下是 `sample_data.proto` 檔案的內容：

```
message SampleData {
  required string name = 1;
  required int64 age = 2;
}
```

這個指令碼會使用 `entries.json` 檔案，其中包含要插入 BigQuery 資料表的範例列資料：

```
{"name": "Jim", "age": 35}
{"name": "Jane", "age": 27}
```

### 使用多工處理

您只能為預設串流在串流寫入器層級啟用[多工](https://docs.cloud.google.com/bigquery/docs/write-api-best-practices?hl=zh-tw#connection_pool_management)。如要在 Java 中啟用多工，請在建構 `StreamWriter` 或 `JsonStreamWriter` 物件時呼叫 `setEnableConnectionPool` 方法。

啟用連線集區後，Java 用戶端程式庫會在背景管理連線，並在現有連線過於忙碌時擴充連線。如要讓自動調整資源配置功能更有效，建議調低 `maxInflightRequests` 限制。

```
// One possible way for constructing StreamWriter
StreamWriter.newBuilder(streamName)
              .setWriterSchema(protoSchema)
              .setEnableConnectionPool(true)
              .setMaxInflightRequests(100)
              .build();
// One possible way for constructing JsonStreamWriter
JsonStreamWriter.newBuilder(tableName, bigqueryClient)
              .setEnableConnectionPool(true)
              .setMaxInflightRequests(100)
              .build();
```

如要在 Go 中啟用多工處理，請參閱「[連線共用 (多工處理)](https://pkg.go.dev/cloud.google.com/go/bigquery/storage/managedwriter#hdr-Connection_Sharing__Multiplexing_)」。

## 使用已提交的型別，確保「僅限一次」語意

如需「僅限一次」寫入語意，請建立已提交類型的寫入串流。在已提交類型中，用戶端收到後端的確認後，即可查詢記錄。

「已提交」類型會使用記錄偏移，在串流中提供「僅傳送一次」的傳遞機制。應用程式會使用記錄偏移值，在每次呼叫 [`AppendRows`](https://docs.cloud.google.com/bigquery/docs/reference/storage/rpc/google.cloud.bigquery.storage.v1?hl=zh-tw#google.cloud.bigquery.storage.v1.BigQueryWrite.AppendRows) 時指定下一個附加偏移值。只有在偏移值與下一個附加偏移值相符時，系統才會執行寫入作業。詳情請參閱「[管理串流偏移，實現精確一次語意](https://docs.cloud.google.com/bigquery/docs/write-api-best-practices?hl=zh-tw#manage_stream_offsets_to_achieve_exactly-once_semantics)」。

如未提供偏移量，記錄會附加至串流目前的結尾。在這種情況下，如果附加要求傳回錯誤，重試要求可能會導致記錄在串流中出現多次。

如要使用已提交類型，請按照下列步驟操作：

### Java

1. 呼叫 `CreateWriteStream`，在已提交的類型中建立一或多個串流。
2. 針對每個串流，在迴圈中呼叫 `AppendRows`，即可寫入批次記錄。
3. 針對每個串流呼叫 `FinalizeWriteStream`，釋放串流。呼叫這個方法後，您就無法再將任何資料列寫入串流。如果是已承諾方案，這個步驟為選用步驟，但有助於避免超出有效串流的限制。詳情請參閱「[限制串流建立速率](https://docs.cloud.google.com/bigquery/docs/write-api-best-practices?hl=zh-tw#limit_the_rate_of_stream_creation)」。

### Node.js

1. 呼叫 `createWriteStreamFullResponse`，在已提交的類型中建立一或多個串流。
2. 針對每個串流，在迴圈中呼叫 `appendRows`，即可寫入批次記錄。
3. 針對每個串流呼叫 `finalize`，釋放串流。呼叫這個方法後，您就無法再將任何資料列寫入串流。如果是已承諾方案，這個步驟為選用步驟，但有助於避免超出有效串流的限制。詳情請參閱「[限制串流建立速率](https://docs.cloud.google.com/bigquery/docs/write-api-best-practices?hl=zh-tw#limit_the_rate_of_stream_creation)」。

您無法明確刪除串流。串流會遵循系統定義的存留時間 (TTL)：

* 如果串流沒有任何流量，已提交的串流 TTL 為三天。
* 如果緩衝串流沒有任何流量，預設存留時間為七天。

以下程式碼顯示如何使用已提交的型別：

### Java

如要瞭解如何安裝及使用 BigQuery 的用戶端程式庫，請參閱「[BigQuery 用戶端程式庫](https://docs.cloud.google.com/bigquery/docs/reference/storage/libraries?hl=zh-tw)」。詳情請參閱 [BigQuery Java API 參考說明文件](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquerystorage/latest/com.google.cloud.bigquery.storage.v1?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import com.google.api.core.ApiFuture;
import com.google.api.core.ApiFutureCallback;
import com.google.api.core.ApiFutures;
import com.google.api.gax.retrying.RetrySettings;
import com.google.cloud.bigquery.storage.v1.AppendRowsResponse;
import com.google.cloud.bigquery.storage.v1.BigQueryWriteClient;
import com.google.cloud.bigquery.storage.v1.CreateWriteStreamRequest;
import com.google.cloud.bigquery.storage.v1.Exceptions;
import com.google.cloud.bigquery.storage.v1.Exceptions.StorageException;
import com.google.cloud.bigquery.storage.v1.FinalizeWriteStreamResponse;
import com.google.cloud.bigquery.storage.v1.JsonStreamWriter;
import com.google.cloud.bigquery.storage.v1.TableName;
import com.google.cloud.bigquery.storage.v1.WriteStream;
import com.google.common.util.concurrent.MoreExecutors;
import com.google.protobuf.Descriptors.DescriptorValidationException;
import java.io.IOException;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.Phaser;
import javax.annotation.concurrent.GuardedBy;
import org.json.JSONArray;
import org.json.JSONObject;
import org.threeten.bp.Duration;

public class WriteCommittedStream {

  public static void runWriteCommittedStream()
      throws DescriptorValidationException, InterruptedException, IOException {
    // TODO(developer): Replace these variables before running the sample.
    String projectId = "MY_PROJECT_ID";
    String datasetName = "MY_DATASET_NAME";
    String tableName = "MY_TABLE_NAME";

    writeCommittedStream(projectId, datasetName, tableName);
  }

  public static void writeCommittedStream(String projectId, String datasetName, String tableName)
      throws DescriptorValidationException, InterruptedException, IOException {
    BigQueryWriteClient client = BigQueryWriteClient.create();
    TableName parentTable = TableName.of(projectId, datasetName, tableName);

    DataWriter writer = new DataWriter();
    // One time initialization.
    writer.initialize(parentTable, client);

    try {
      // Write two batches of fake data to the stream, each with 10 JSON records.  Data may be
      // batched up to the maximum request size:
      // https://cloud.google.com/bigquery/quotas#write-api-limits
      long offset = 0;
      for (int i = 0; i < 2; i++) {
        // Create a JSON object that is compatible with the table schema.
        JSONArray jsonArr = new JSONArray();
        for (int j = 0; j < 10; j++) {
          JSONObject record = new JSONObject();
          record.put("col1", String.format("batch-record %03d-%03d", i, j));
          jsonArr.put(record);
        }
        writer.append(jsonArr, offset);
        offset += jsonArr.length();
      }
    } catch (ExecutionException e) {
      // If the wrapped exception is a StatusRuntimeException, check the state of the operation.
      // If the state is INTERNAL, CANCELLED, or ABORTED, you can retry. For more information, see:
      // https://grpc.github.io/grpc-java/javadoc/io/grpc/StatusRuntimeException.html
      System.out.println("Failed to append records. \n" + e);
    }

    // Final cleanup for the stream.
    writer.cleanup(client);
    System.out.println("Appended records successfully.");
  }

  // A simple wrapper object showing how the stateful stream writer should be used.
  private static class DataWriter {

    private JsonStreamWriter streamWriter;
    // Track the number of in-flight requests to wait for all responses before shutting down.
    private final Phaser inflightRequestCount = new Phaser(1);

    private final Object lock = new Object();

    @GuardedBy("lock")
    private RuntimeException error = null;

    void initialize(TableName parentTable, BigQueryWriteClient client)
        throws IOException, DescriptorValidationException, InterruptedException {
      // Initialize a write stream for the specified table.
      // For more information on WriteStream.Type, see:
      // https://googleapis.dev/java/google-cloud-bigquerystorage/latest/com/google/cloud/bigquery/storage/v1/WriteStream.Type.html
      WriteStream stream = WriteStream.newBuilder().setType(WriteStream.Type.COMMITTED).build();

      CreateWriteStreamRequest createWriteStreamRequest =
          CreateWriteStreamRequest.newBuilder()
              .setParent(parentTable.toString())
              .setWriteStream(stream)
              .build();
      WriteStream writeStream = client.createWriteStream(createWriteStreamRequest);

      // Configure in-stream automatic retry settings.
      // Error codes that are immediately retried:
      // * ABORTED, UNAVAILABLE, CANCELLED, INTERNAL, DEADLINE_EXCEEDED
      // Error codes that are retried with exponential backoff:
      // * RESOURCE_EXHAUSTED
      RetrySettings retrySettings =
          RetrySettings.newBuilder()
              .setInitialRetryDelay(Duration.ofMillis(500))
              .setRetryDelayMultiplier(1.1)
              .setMaxAttempts(5)
              .setMaxRetryDelay(Duration.ofMinutes(1))
              .build();

      // Use the JSON stream writer to send records in JSON format.
      // For more information about JsonStreamWriter, see:
      // https://googleapis.dev/java/google-cloud-bigquerystorage/latest/com/google/cloud/bigquery/storage/v1/JsonStreamWriter.html
      streamWriter =
          JsonStreamWriter.newBuilder(writeStream.getName(), writeStream.getTableSchema(), client)
              .setRetrySettings(retrySettings)
              .build();
    }

    public void append(JSONArray data, long offset)
        throws DescriptorValidationException, IOException, ExecutionException {
      synchronized (this
```