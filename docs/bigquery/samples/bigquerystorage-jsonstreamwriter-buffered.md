Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [範例](https://docs.cloud.google.com/bigquery/docs/samples?hl=zh-tw)

# 附加緩衝記錄 透過集合功能整理內容 你可以依據偏好儲存及分類內容。

使用 JSON 串流寫入器，在緩衝模式下附加記錄

## 程式碼範例

### Java

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Java 設定說明操作。詳情請參閱 [BigQuery Java API 參考說明文件](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/overview?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import com.google.api.core.ApiFuture;
import com.google.api.gax.retrying.RetrySettings;
import com.google.cloud.bigquery.storage.v1.AppendRowsResponse;
import com.google.cloud.bigquery.storage.v1.BigQueryWriteClient;
import com.google.cloud.bigquery.storage.v1.CreateWriteStreamRequest;
import com.google.cloud.bigquery.storage.v1.FinalizeWriteStreamRequest;
import com.google.cloud.bigquery.storage.v1.FlushRowsRequest;
import com.google.cloud.bigquery.storage.v1.FlushRowsResponse;
import com.google.cloud.bigquery.storage.v1.JsonStreamWriter;
import com.google.cloud.bigquery.storage.v1.TableName;
import com.google.cloud.bigquery.storage.v1.WriteStream;
import com.google.protobuf.Descriptors.DescriptorValidationException;
import com.google.protobuf.Int64Value;
import java.io.IOException;
import java.util.concurrent.ExecutionException;
import org.json.JSONArray;
import org.json.JSONObject;
import org.threeten.bp.Duration;

public class WriteBufferedStream {

  public static void runWriteBufferedStream()
      throws DescriptorValidationException, InterruptedException, IOException {
    // TODO(developer): Replace these variables before running the sample.
    String projectId = "MY_PROJECT_ID";
    String datasetName = "MY_DATASET_NAME";
    String tableName = "MY_TABLE_NAME";

    writeBufferedStream(projectId, datasetName, tableName);
  }

  public static void writeBufferedStream(String projectId, String datasetName, String tableName)
      throws DescriptorValidationException, InterruptedException, IOException {
    try (BigQueryWriteClient client = BigQueryWriteClient.create()) {
      // Initialize a write stream for the specified table.
      // For more information on WriteStream.Type, see:
      // https://googleapis.dev/java/google-cloud-bigquerystorage/latest/com/google/cloud/bigquery/storage/v1/WriteStream.Type.html
      WriteStream stream = WriteStream.newBuilder().setType(WriteStream.Type.BUFFERED).build();
      TableName parentTable = TableName.of(projectId, datasetName, tableName);
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
      // https://cloud.google.com/java/docs/reference/google-cloud-bigquerystorage/latest/com.google.cloud.bigquery.storage.v1.JsonStreamWriter
      try (JsonStreamWriter writer =
          JsonStreamWriter.newBuilder(writeStream.getName(), writeStream.getTableSchema())
              .setRetrySettings(retrySettings)
              .build()) {
        // Write two batches to the stream, each with 10 JSON records.
        for (int i = 0; i < 2; i++) {
          JSONArray jsonArr = new JSONArray();
          for (int j = 0; j < 10; j++) {
            // Create a JSON object that is compatible with the table schema.
            JSONObject record = new JSONObject();
            record.put("col1", String.format("buffered-record %03d", i));
            jsonArr.put(record);
          }
          ApiFuture<AppendRowsResponse> future = writer.append(jsonArr);
          AppendRowsResponse response = future.get();
        }
        // Flush the buffer.
        FlushRowsRequest flushRowsRequest =
            FlushRowsRequest.newBuilder()
                .setWriteStream(writeStream.getName())
                .setOffset(Int64Value.of(10 * 2 - 1)) // Advance the cursor to the latest record.
                .build();
        FlushRowsResponse flushRowsResponse = client.flushRows(flushRowsRequest);
        // You can continue to write to the stream after flushing the buffer.
      }
      // Finalize the stream after use.
      FinalizeWriteStreamRequest finalizeWriteStreamRequest =
          FinalizeWriteStreamRequest.newBuilder().setName(writeStream.getName()).build();
      client.finalizeWriteStream(finalizeWriteStreamRequest);
      System.out.println("Appended and committed records successfully.");
    } catch (ExecutionException e) {
      // If the wrapped exception is a StatusRuntimeException, check the state of the operation.
      // If the state is INTERNAL, CANCELLED, or ABORTED, you can retry. For more information, see:
      // https://grpc.github.io/grpc-java/javadoc/io/grpc/StatusRuntimeException.html
      System.out.println(e);
    }
  }
}
```

### Rust

```
use anyhow::Result;
use arrow::datatypes::{DataType, Field, Schema};
use arrow::ipc::writer::StreamWriter;
use arrow_json::ReaderBuilder;
use google_cloud_bigquery::client::Write;
use google_cloud_bigquery::model::{ArrowRecordBatch, ArrowSchema};
use google_cloud_bigquery::write::BufferedWriter;
use google_cloud_bigquery::write::format::Arrow;
use std::sync::Arc;
use tokio::task::JoinSet;

// The client library doesn't support a built-in JSON API surface.
//
// This example demonstrates how to write JSON data to BigQuery by first
// converting it to Arrow record batches using the `arrow-json` crate.

pub async fn sample(project_id: &str, dataset_id: &str, table_id: &str) -> anyhow::Result<()> {
    let client = Write::builder().build().await?;

    // Define the table schema
    let schema = Arc::new(Schema::new(vec![
        Field::new("string", DataType::Utf8, false),
        Field::new("int", DataType::Int64, false),
    ]));

    // Initialize an IPC stream writer and extract the serialized schema
    let mut ipc_writer = StreamWriter::try_new(Vec::new(), &schema)?;
    let schema_buf = std::mem::take(ipc_writer.get_mut());

    let table = format!("projects/{project_id}/datasets/{dataset_id}/tables/{table_id}");
    // Create a writer for a buffered stream
    let writer: BufferedWriter<Arrow> = client
        .create_stream(table)
        .build_arrow(ArrowSchema::new().set_serialized_schema(schema_buf))
        .await?;

    // Create a decoder to convert JSON to Arrow
    let mut decoder = ReaderBuilder::new(schema).build_decoder()?;

    let mut writes = JoinSet::new();
    for i in 0..100 {
        for j in 0..10 {
            // Generate example data (JSON bytes)
            let json = format!(r#"{{"string": "batch {i}", "int": {}}}"#, 10 * i + j);
            let _ = decoder.decode(json.as_bytes())?;
        }
        if let Some(batch) = decoder.flush()? {
            // Serialize the batch
            let batch = {
                ipc_writer.write(&batch)?;
                let batch_bytes = std::mem::take(ipc_writer.get_mut());
                ArrowRecordBatch::new().set_serialized_record_batch(batch_bytes)
            };
            // Write the batch to the buffered stream
            writes.spawn(writer.append(batch).set_offset(10 * i).send());
        }
    }
    let results: Result<Vec<_>, _> = writes.join_all().await.into_iter().collect();
    let _ = results?;

    // Flush the buffered rows. Note that the flush offset is inclusive.
    let resp = writer.flush(999).await?;
    println!("Successfully flushed up to offset {}", resp.offset);

    // Finalize the stream, preventing further writes
    let resp = writer.finalize().await?;
    println!(
        "Successfully finalized the stream with {} rows",
        resp.row_count
    );

    Ok(())
}
```

## 後續步驟

如要搜尋及篩選其他 Google Cloud 產品的程式碼範例，請參閱[Google Cloud 範例瀏覽工具](https://docs.cloud.google.com/docs/samples?product=bigquery&hl=zh-tw)。

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。




[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],[],[],[]]