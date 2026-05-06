Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 使用 Storage Write API 批次載入資料

本文說明如何使用 [BigQuery Storage Write API](https://docs.cloud.google.com/bigquery/docs/write-api?hl=zh-tw)，將資料批次載入 BigQuery。

在批次載入情境中，應用程式會寫入資料，並以單一不可分割的交易提交資料。使用 Storage Write API 批次載入資料時，請在*待處理類型*中建立一或多個串流。待處理類型支援串流層級交易。記錄會緩衝處理，直到您提交串流為止。

對於批次工作負載，也請考慮透過 [Apache Spark SQL 連接器 (適用於 BigQuery)](https://github.com/GoogleCloudDataproc/spark-bigquery-connector#writing-data-to-bigquery) 使用 Storage Write API，並透過 Managed Service for Apache Spark 執行，而非編寫自訂的 Storage Write API 程式碼。

Storage Write API 非常適合*資料管道*架構。主程序會建立多個串流。針對每個串流，系統會指派背景工作執行緒或個別程序，寫入部分批次資料。每個工作站都會建立與串流的連線、寫入資料，並在完成時終止串流。所有工作站向主要程序發出信號，表示成功完成作業後，主要程序就會提交資料。如果工作站發生故障，最終結果就不會顯示該工作站負責的資料部分，且可以安全地重試整個工作站。在更複雜的管道中，工作站會回報寫入主要程序的最後一個偏移量，藉此檢查進度。這種做法可建立強大的管道，即使發生故障也能正常運作。

## 使用待處理類型批次載入資料

如要使用待處理類型，應用程式會執行下列操作：

1. 呼叫 `CreateWriteStream`，在待處理型別中建立一或多個串流。
2. 針對每個串流，在迴圈中呼叫 `AppendRows`，即可寫入批次記錄。
3. 針對每個串流呼叫 `FinalizeWriteStream`。呼叫這個方法後，您就無法再將任何資料列寫入串流。如果您在呼叫 `FinalizeWriteStream` 後呼叫 `AppendRows`，系統會傳回 [`StorageError`](https://docs.cloud.google.com/bigquery/docs/reference/storage/rpc/google.cloud.bigquery.storage.v1?hl=zh-tw#google.cloud.bigquery.storage.v1.StorageError)，且 `google.rpc.Status` 錯誤中會包含 `StorageErrorCode.STREAM_FINALIZED`。如要進一步瞭解 `google.rpc.Status` 錯誤模型，請參閱「[錯誤](https://docs.cloud.google.com/apis/design/errors?hl=zh-tw)」。
4. 呼叫 `BatchCommitWriteStreams` 來提交串流。呼叫這個方法後，資料即可供讀取。如果提交任何串流時發生錯誤，系統會在 [`BatchCommitWriteStreamsResponse`](https://docs.cloud.google.com/bigquery/docs/reference/storage/rpc/google.cloud.bigquery.storage.v1?hl=zh-tw#batchcommitwritestreamsresponse) 的 `stream_errors` 欄位中傳回錯誤。

提交是不可分割的作業，您可以一次提交多個串流。
串流只能提交一次，因此如果提交作業失敗，可以安全地重試。在您提交串流前，資料會處於待處理狀態，且無法讀取。

資料最多可在緩衝區保留 4 小時，待處理的串流必須在 24 小時內提交。
[待處理串流緩衝區的總大小](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#writeapi_pending_stream)設有配額限制。

以下程式碼顯示如何以待處理類型寫入資料：

### C#

如要瞭解如何安裝及使用 BigQuery 的用戶端程式庫，請參閱「[BigQuery 用戶端程式庫](https://docs.cloud.google.com/bigquery/docs/reference/storage/libraries?hl=zh-tw)」。詳情請參閱 [BigQuery C# API 參考說明文件](https://docs.cloud.google.com/dotnet/docs/reference/Google.Cloud.BigQuery.Storage.V1/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
using Google.Api.Gax.Grpc;
using Google.Cloud.BigQuery.Storage.V1;
using Google.Protobuf;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using static Google.Cloud.BigQuery.Storage.V1.AppendRowsRequest.Types;

public class AppendRowsPendingSample
{
    /// <summary>
    /// This code sample demonstrates how to write records in pending mode.
    /// Create a write stream, write some sample data, and commit the stream to append the rows.
    /// The CustomerRecord proto used in the sample can be seen in Resources folder and generated C# is placed in Data folder in
    /// https://github.com/GoogleCloudPlatform/dotnet-docs-samples/tree/main/bigquery-storage/api/BigQueryStorage.Samples
    /// </summary>
    public async Task AppendRowsPendingAsync(string projectId, string datasetId, string tableId)
    {
        BigQueryWriteClient bigQueryWriteClient = await BigQueryWriteClient.CreateAsync();
        // Initialize a write stream for the specified table.
        // When creating the stream, choose the type. Use the Pending type to wait
        // until the stream is committed before it is visible. See:
        // https://cloud.google.com/bigquery/docs/reference/storage/rpc/google.cloud.bigquery.storage.v1#google.cloud.bigquery.storage.v1.WriteStream.Type
        WriteStream stream = new WriteStream { Type = WriteStream.Types.Type.Pending };
        TableName tableName = TableName.FromProjectDatasetTable(projectId, datasetId, tableId);

        stream = await bigQueryWriteClient.CreateWriteStreamAsync(tableName, stream);

        // Initialize streaming call, retrieving the stream object
        BigQueryWriteClient.AppendRowsStream rowAppender = bigQueryWriteClient.AppendRows();

        // Sending requests and retrieving responses can be arbitrarily interleaved.
        // Exact sequence will depend on client/server behavior.
        // Create task to do something with responses from server.
        Task appendResultsHandlerTask = Task.Run(async () =>
        {
            AsyncResponseStream<AppendRowsResponse> appendRowResults = rowAppender.GetResponseStream();
            while (await appendRowResults.MoveNextAsync())
            {
                AppendRowsResponse responseItem = appendRowResults.Current;
                // Do something with responses.
                if (responseItem.AppendResult != null)
                {
                    Console.WriteLine($"Appending rows resulted in: {responseItem.AppendResult}");
                }
                if (responseItem.Error != null)
                {
                    Console.Error.WriteLine($"Appending rows resulted in an error: {responseItem.Error.Message}");
                    foreach (RowError rowError in responseItem.RowErrors)
                    {
                        Console.Error.WriteLine($"Row Error: {rowError}");
                    }
                }
            }
            // The response stream has completed.
        });

        // List of records to be appended in the table.
        List<CustomerRecord> records = new List<CustomerRecord>
        {
            new CustomerRecord { CustomerNumber = 1, CustomerName = "Alice" },
            new CustomerRecord { CustomerNumber = 2, CustomerName = "Bob" }
        };

        // Create a batch of row data by appending serialized bytes to the
        // SerializedRows repeated field.
        ProtoData protoData = new ProtoData
        {
            WriterSchema = new ProtoSchema { ProtoDescriptor = CustomerRecord.Descriptor.ToProto() },
            Rows = new ProtoRows { SerializedRows = { records.Select(r => r.ToByteString()) } }
        };

        // Initialize the append row request.
        AppendRowsRequest appendRowRequest = new AppendRowsRequest
        {
            WriteStreamAsWriteStreamName = stream.WriteStreamName,
            ProtoRows = protoData
        };

        // Stream a request to the server.
        await rowAppender.WriteAsync(appendRowRequest);

        // Append a second batch of data.
        protoData = new ProtoData
        {
            Rows = new ProtoRows { SerializedRows = { new CustomerRecord { CustomerNumber = 3, CustomerName = "Charles" }.ToByteString() } }
        };

        // Since this is the second request, you only need to include the row data.
        // The name of the stream and protocol buffers descriptor is only needed in
        // the first request.
        appendRowRequest = new AppendRowsRequest
        {
            // If Offset is not present, the write is performed at the current end of stream.
            ProtoRows = protoData
        };

        await rowAppender.WriteAsync(appendRowRequest);

        // Complete writing requests to the stream.
        await rowAppender.WriteCompleteAsync();

        // Await the handler. This will complete once all server responses have been processed.
        await appendResultsHandlerTask;

        // A Pending type stream must be "finalized" before being committed. No new
        // records can be written to the stream after this method has been called.
        await bigQueryWriteClient.FinalizeWriteStreamAsync(stream.Name);
        BatchCommitWriteStreamsRequest batchCommitWriteStreamsRequest = new BatchCommitWriteStreamsRequest
        {
            Parent = tableName.ToString(),
            WriteStreams = { stream.Name }
        };

        BatchCommitWriteStreamsResponse batchCommitWriteStreamsResponse =
            await bigQueryWriteClient.BatchCommitWriteStreamsAsync(batchCommitWriteStreamsRequest);
        if (batchCommitWriteStreamsResponse.StreamErrors?.Count > 0)
        {
            // Handle errors here.
            Console.WriteLine("Error committing write streams. Individual errors:");
            foreach (StorageError error in batchCommitWriteStreamsResponse.StreamErrors)
            {
                Console.WriteLine(error.ErrorMessage);
            }            
        }
        else
        {
            Console.WriteLine($"Writes to stream {stream.Name} have been committed.");
        }
    }
}
```

### Go

如要瞭解如何安裝及使用 BigQuery 的用戶端程式庫，請參閱「[BigQuery 用戶端程式庫](https://docs.cloud.google.com/bigquery/docs/reference/storage/libraries?hl=zh-tw)」。詳情請參閱 [BigQuery Go API 參考說明文件](https://pkg.go.dev/cloud.google.com/go/bigquery/storage?tab=doc)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import (
	"context"
	"fmt"
	"io"
	"math/rand"
	"time"

	"cloud.google.com/go/bigquery/storage/apiv1/storagepb"
	"cloud.google.com/go/bigquery/storage/managedwriter"
	"cloud.google.com/go/bigquery/storage/managedwriter/adapt"
	"github.com/GoogleCloudPlatform/golang-samples/bigquery/snippets/managedwriter/exampleproto"
	"google.golang.org/protobuf/proto"
)

// generateExampleMessages generates a slice of serialized protobuf messages using a statically defined
// and compiled protocol buffer file, and returns the binary serialized representation.
func generateExampleMessages(numMessages int) ([][]byte, error) {
	msgs := make([][]byte, numMessages)
	for i := 0; i < numMessages; i++ {

		random := rand.New(rand.NewSource(time.Now().UnixNano()))

		// Our example data embeds an array of structs, so we'll construct that first.
		sList := make([]*exampleproto.SampleStruct, 5)
		for i := 0; i < int(random.Int63n(5)+1); i++ {
			sList[i] = &exampleproto.SampleStruct{
				SubIntCol: proto.Int64(random.Int63()),
			}
		}

		m := &exampleproto.SampleData{
			BoolCol:    proto.Bool(true),
			BytesCol:   []byte("some bytes"),
			Float64Col: proto.Float64(3.14),
			Int64Col:   proto.Int64(123),
			StringCol:  proto.String("example string value"),

			// These types require special encoding/formatting to transmit.

			// DATE values are number of days since the Unix epoch.

			DateCol: proto.Int32(int32(time.Now().UnixNano() / 86400000000000)),

			// DATETIME uses the literal format.
			DatetimeCol: proto.String("2022-01-01 12:13:14.000000"),

			// GEOGRAPHY uses Well-Known-Text (WKT) format.
			GeographyCol: proto.String("POINT(-122.350220 47.649154)"),

			// NUMERIC and BIGNUMERIC can be passed as string, or more efficiently
			// using a packed byte representation.
			NumericCol:    proto.String("99999999999999999999999999999.999999999"),
			BignumericCol: proto.String("578960446186580977117854925043439539266.34992332820282019728792003956564819967"),

			// TIME also uses literal format.
			TimeCol: proto.String("12:13:14.000000"),

			// TIMESTAMP uses microseconds since Unix epoch.
			TimestampCol: proto.Int64(time.Now().UnixNano() / 1000),

			// Int64List is an array of INT64 types.
			Int64List: []int64{2, 4, 6, 8},

			// This is a required field, and thus must be present.
			RowNum: proto.Int64(23),

			// StructCol is a single nested message.
			StructCol: &exampleproto.SampleStruct{
				SubIntCol: proto.Int64(random.Int63()),
			},

			// StructList is a repeated array of a nested message.
			StructList: sList,
		}

		b, err := proto.Marshal(m)
		if err != nil {
			return nil, fmt.Errorf("error generating message %d: %w", i, err)
		}
		msgs[i] = b
	}
	return msgs, nil
}

// appendToPendingStream demonstrates using the managedwriter package to write some example data
// to a pending stream, and then committing it to a table.
func appendToPendingStream(w io.Writer, projectID, datasetID, tableID string) error {
	// projectID := "myproject"
	// datasetID := "mydataset"
	// tableID := "mytable"

	ctx := context.Background()
	// Instantiate a managedwriter client to handle interactions with the service.
	client, err := managedwriter.NewClient(ctx, projectID)
	if err != nil {
		return fmt.Errorf("managedwriter.NewClient: %w", err)
	}
	// Close the client when we exit the function.
	defer client.Close()

	// Create a new pending stream.  We'll use the stream name to construct a writer.
	pendingStream, err := client.CreateWriteStream(ctx, &storagepb.CreateWriteStreamRequest{
		Parent: fmt.Sprintf("projects/%s/datasets/%s/tables/%s", projectID, datasetID, tableID),
		WriteStream: &storagepb.WriteStream{
			Type: storagepb.WriteStream_PENDING,
		},
	})
	if err != nil {
		return fmt.Errorf("CreateWriteStream: %w", err)
	}

	// We need to communicate the descriptor of the protocol buffer message we're using, which
	// is analagous to the "schema" for the message.  Both SampleData and SampleStruct are
	// two distinct messages in the compiled proto file, so we'll use adapt.NormalizeDescriptor
	// to unify them into a single self-contained descriptor representation.
	m := &exampleproto.SampleData{}
	descriptorProto, err := adapt.NormalizeDescriptor(m.ProtoReflect().Descriptor())
	if err != nil {
		return fmt.Errorf("NormalizeDescriptor: %w", err)
	}

	// Instantiate a ManagedStream, which manages low level details like connection state and provides
	// additional features like a future-like callback for appends, etc.  NewManagedStream can also create
	// the stream on your behalf, but in this example we're being explicit about stream creation.
	managedStream, err := client.NewManagedStream(ctx, managedwriter.WithStreamName(pendingStream.GetName()),
		managedwriter.WithSchemaDescriptor(descriptorProto))
	if err != nil {
		return fmt.Errorf("NewManagedStream: %w", err)
	}
	defer managedStream.Close()

	// First, we'll append a single row.
	rows, err := generateExampleMessages(1)
	if err != nil {
		return fmt.Errorf("generateExampleMessages: %w", err)
	}

	// We'll keep track of the current offset in the stream with curOffset.
	var curOffset int64
	// We can append data asyncronously, so we'll check our appends at the end.
	var results []*managedwriter.AppendResult

	result, err := managedStream.AppendRows(ctx, rows, managedwriter.WithOffset(0))
	if err != nil {
		return fmt.Errorf("AppendRows first call error: %w", err)
	}
	results = append(results, result)

	// Advance our current offset.
	curOffset = curOffset + 1

	// This time, we'll append three more rows in a single request.
	rows, err = generateExampleMessages(3)
	if err != nil {
		return fmt.Errorf("generateExampleMessages: %w", err)
	}
	result, err = managedStream.AppendRows(ctx, rows, managedwriter.WithOffset(curOffset))
	if err != nil {
		return fmt.Errorf("AppendRows second call error: %w", err)
	}
	results = append(results, result)

	// Advance our offset again.
	curOffset = curOffset + 3

	// Finally, we'll append two more rows.
	rows, err = generateExampleMessages(2)
	if err != nil {
		return fmt.Errorf("generateExampleMessages: %w", err)
	}
	result, err = managedStream.AppendRows(ctx, rows, managedwriter.WithOffset(curOffset))
	if err != nil {
		return fmt.Errorf("AppendRows third call error: %w", err)
	}
	results = append(results, result)

	// Now, we'll check that our batch of three appends all completed successfully.
	// Monitoring the results could also be done out of band via a goroutine.
	for k, v := range results {
		// GetResult blocks until we receive a response from the API.
		recvOffset, err := v.GetResult(ctx)
		if err != nil {
			return fmt.Errorf("append %d returned error: %w", k, err)
		}
		fmt.Fprintf(w, "Successfully appended data at offset %d.\n", recvOffset)
	}

	// We're now done appending to this stream.  We now mark pending stream finalized, which blocks
	// further appends.
	rowCount, err := managedStream.Finalize(ctx)
	if err != nil {
		return fmt.Errorf("error during Finalize: %w", err)
	}

	fmt.Fprintf(w, "Stream %s finalized with %d rows.\n", managedStream.StreamName(), rowCount)

	// To commit the data to the table, we need to run a batch commit.  You can commit several streams
	// atomically as a group, but in this instance we'll only commit the single stream.
	req := &storagepb.BatchCommitWriteStreamsRequest{
		Parent:       managedwriter.TableParentFromStreamName(managedStream.StreamName()),
		WriteStreams: []string{managedStream.StreamName()},
	}

	resp, err := client.BatchCommitWriteStreams(ctx, req)
	if err != nil {
		return fmt.Errorf("client.BatchCommit: %w", err)
	}
	if len(resp.GetStreamErrors()) > 0 {
		return fmt.Errorf("stream errors present: %v", resp.GetStreamErrors())
	}

	fmt.Fprintf(w, "Table data committed at %s\n", resp.GetCommitTime().AsTime().Format(time.RFC3339Nano))

	return nil
}
```

### Java

如要瞭解如何安裝及使用 BigQuery 的用戶端程式庫，請參閱「[BigQuery 用戶端程式庫](https://docs.cloud.google.com/bigquery/docs/reference/storage/libraries?hl=zh-tw)」。詳情請參閱 [BigQuery Java API 參考說明文件](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquerystorage/latest/com.google.cloud.bigquery.storage.v1?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import com.google.api.core.ApiFuture;
import com.google.api.core.ApiFutureCallback;
import com.google.api.core.ApiFutures;
import com.google.api.gax.retrying.RetrySettings;
import com.google.cloud.bigquery.storage.v1.AppendRowsResponse;
import com.google.cloud.bigquery.storage.v1.BatchCommitWriteStreamsRequest;
import com.google.cloud.bigquery.storage.v1.BatchCommitWriteStreamsResponse;
import com.google.cloud.bigquery.storage.v1.BigQueryWriteClient;
import com.google.cloud.bigquery.storage.v1.CreateWriteStreamRequest;
import com.google.cloud.bigquery.storage.v1.Exceptions;
import com.google.cloud.bigquery.storage.v1.Exceptions.StorageException;
import com.google.cloud.bigquery.storage.v1.FinalizeWriteStreamResponse;
import com.google.cloud.bigquery.storage.v1.JsonStreamWriter;
import com.google.cloud.bigquery.storage.v1.StorageError;
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

public class WritePendingStream {

  public static void runWritePendingStream()
      throws DescriptorValidationException, InterruptedException, IOException {
    // TODO(developer): Replace these variables before running the sample.
    String projectId = "MY_PROJECT_ID";
    String datasetName = "MY_DATASET_NAME";
    String tableName = "MY_TABLE_NAME";

    writePendingStream(projectId, datasetName, tableName);
  }

  public static void writePendingStream(String projectId, String datasetName, String tableName)
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

    // Once all streams are done, if all writes were successful, commit all of them in one request.
    // This example only has the one stream. If any streams failed, their workload may be
    // retried on a new stream, and then only the successful stream should be included in the
    // commit.
    BatchCommitWriteStreamsRequest commitRequest =
        BatchCommitWriteStreamsRequest.newBuilder()
            .setParent(parentTable.toString())
            .addWriteStreams(writer.getStreamName())
            .build();
    BatchCommitWriteStreamsResponse commitResponse = client.batchCommitWriteStreams(commitRequest);
    // If the response does not have a commit time, it means the commit operation failed.
    if (commitResponse.hasCommitTime() == false) {
      for (StorageError err : commitResponse.getStreamErrorsList()) {
        System.out.println(err.getErrorMessage());
      }
      throw new RuntimeException("Error committing the streams");
    }
    System.out.println("Appended and committed records successfully.");
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
      WriteStream stream = WriteStream.newBuilder().setType(WriteStream.Type.PENDING).build();

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

      CreateWriteStreamRequest createWriteStreamRequest =
          CreateWriteStreamRequest.newBuilder()
              .setParent(parentTable.toString())
              .setWriteStream(stream)
              .build();
      WriteStream writeStream = client.createWriteStream(createWriteStreamRequest);

      // Use the JSON stream writer to send records in JSON format.
      // For more information about JsonStreamWriter, see:
      // https://cloud.google.com/java/docs/reference/google-cloud-bigquerystorage/latest/com.google.cloud.bigquery.storage.v1.JsonStreamWriter
      streamWriter =
          JsonStreamWriter.newBuilder(writeStream.getName(), writeStream.getTableSchema())
              .setRetrySettings(retrySettings)
              .build();
    }

    public void append(JSONArray data, long offset)
        throws DescriptorValidationException, IOException, ExecutionException {
      synchronized (this.lock) {
        // If earlier appends have failed, we need to reset before continuing.
        if (this.error != null) {
          throw this.error;
        }
      }
      // Append asynchronously for increased throughput.
      ApiFuture<AppendRowsResponse> future = streamWriter.append(data, offset);
      ApiFutures.addCallback(
          future, new AppendCompleteCallback(this), MoreExecutors.directExecutor());
      // Increase the count of in-flight requests.
      inflightRequestCount.register();
    }

    public void cleanup(BigQueryWriteClient client) {
      // Wait for all in-flight requests to complete.
      inflightRequestCount.arriveAndAwaitAdvance();

      // Close the connection to the server.
      streamWriter.close();

      // Verify that no error occurred in the stream.
      synchronized (this.lock) {
        if (this.error != null) {
          throw this.error;
        }
      }

      // Finalize the stream.
      FinalizeWriteStreamResponse finalizeResponse =
          client.finalizeWriteStream(streamWriter.getStreamName());
      System.out.println("Rows written: " + finalizeResponse.getRowCount());
    }

    public String getStreamName() {
      return streamWriter.getStreamName();
    }

    static class AppendCompleteCallback implements ApiFutureCallback<AppendRowsResponse> {

      private final DataWriter parent;

      public AppendCompleteCallback(DataWriter parent) {
        this.parent = parent;
      }

      public void onSuccess(AppendRowsResponse response) {
        System.out.format("Append %d success\n", response.getAppendResult().getOffset().getValue());
        done();
      }

      public void onFailure(Throwable throwable) {
        synchronized (this.parent.lock) {
          if (this.parent.error == null) {
            StorageException storageException = Exceptions.toStorageException(throwable);
            this.parent.error =
                (storageException != null) ? storageException : new RuntimeException(throwable);
          }
        }
        System.out.format("Error: %s\n", throwable.toString());
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

如要瞭解如何安裝及使用 BigQuery 的用戶端程式庫，請參閱「[BigQuery 用戶端程式庫](https://docs.cloud.google.com/bigquery/docs/reference/storage/libraries?hl=zh-tw)」。詳情請參閱 [BigQuery Node.js API 參考說明文件](https://googleapis.dev/nodejs/bigquery/latest/index.html)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
const {adapt, managedwriter} = require('@google-cloud/bigquery-storage');
const {WriterClient, Writer} = managedwriter;

const customer_record_pb = require('./customer_record_pb.js');
const {CustomerRecord} = customer_record_pb;

const protobufjs = require('protobufjs');
require('protobufjs/ext/descriptor');

async function appendRowsPending() {
  /**
   * If you make updates to the customer_record.proto protocol buffers definition,
   * run:
   *   pbjs customer_record.proto -t static-module -w commonjs -o customer_record.js
   *   pbjs customer_record.proto -t json --keep-case -o customer_record.json
   * from the /samples directory to generate the customer_record module.
   */

  // So that BigQuery knows how to parse the serialized_rows, create a
  // protocol buffer representation of your message descriptor.
  const root = protobufjs.loadSync('./customer_record.json');
  const descriptor = root.lookupType('CustomerRecord').toDescriptor('proto2');
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
    const writeStream = await writeClient.createWriteStreamFullResponse({
      streamType,
      destinationTable,
    });
    const streamId = writeStream.name;
    console.log(`Stream created: ${streamId}`);

    const connection = await writeClient.createStreamConnection({
      streamId,
    });
    const writer = new
```