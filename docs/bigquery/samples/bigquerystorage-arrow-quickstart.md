* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [範例](https://docs.cloud.google.com/bigquery/docs/samples?hl=zh-tw)

# 以 Arrow 資料格式下載資料表資料 透過集合功能整理內容 你可以依據偏好儲存及分類內容。

以 Arrow 資料格式下載資料表資料，並將資料還原序列化為列物件。

## 深入探索

如需包含這個程式碼範例的詳細說明文件，請參閱下列文章：

* [BigQuery Storage API 用戶端程式庫](https://docs.cloud.google.com/bigquery/docs/reference/storage/libraries?hl=zh-tw)

## 程式碼範例

### Java

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Java 設定說明操作。詳情請參閱 [BigQuery Java API 參考說明文件](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/overview?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import com.google.api.gax.rpc.ServerStream;
import com.google.cloud.bigquery.storage.v1.ArrowRecordBatch;
import com.google.cloud.bigquery.storage.v1.ArrowSchema;
import com.google.cloud.bigquery.storage.v1.BigQueryReadClient;
import com.google.cloud.bigquery.storage.v1.CreateReadSessionRequest;
import com.google.cloud.bigquery.storage.v1.DataFormat;
import com.google.cloud.bigquery.storage.v1.ReadRowsRequest;
import com.google.cloud.bigquery.storage.v1.ReadRowsResponse;
import com.google.cloud.bigquery.storage.v1.ReadSession;
import com.google.cloud.bigquery.storage.v1.ReadSession.TableModifiers;
import com.google.cloud.bigquery.storage.v1.ReadSession.TableReadOptions;
import com.google.common.base.Preconditions;
import com.google.protobuf.Timestamp;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import org.apache.arrow.memory.BufferAllocator;
import org.apache.arrow.memory.RootAllocator;
import org.apache.arrow.vector.FieldVector;
import org.apache.arrow.vector.VectorLoader;
import org.apache.arrow.vector.VectorSchemaRoot;
import org.apache.arrow.vector.ipc.ReadChannel;
import org.apache.arrow.vector.ipc.message.MessageSerializer;
import org.apache.arrow.vector.types.pojo.Field;
import org.apache.arrow.vector.types.pojo.Schema;
import org.apache.arrow.vector.util.ByteArrayReadableSeekableByteChannel;

public class StorageArrowSample {

  /*
   * SimpleRowReader handles deserialization of the Apache Arrow-encoded row batches transmitted
   * from the storage API using a generic datum decoder.
   */
  private static class SimpleRowReader implements AutoCloseable {

    BufferAllocator allocator = new RootAllocator(Long.MAX_VALUE);

    // Decoder object will be reused to avoid re-allocation and too much garbage collection.
    private final VectorSchemaRoot root;
    private final VectorLoader loader;

    public SimpleRowReader(ArrowSchema arrowSchema) throws IOException {
      Schema schema =
          MessageSerializer.deserializeSchema(
              new ReadChannel(
                  new ByteArrayReadableSeekableByteChannel(
                      arrowSchema.getSerializedSchema().toByteArray())));
      Preconditions.checkNotNull(schema);
      List<FieldVector> vectors = new ArrayList<>();
      for (Field field : schema.getFields()) {
        vectors.add(field.createVector(allocator));
      }
      root = new VectorSchemaRoot(vectors);
      loader = new VectorLoader(root);
    }

    /**
     * Sample method for processing Arrow data which only validates decoding.
     *
     * @param batch object returned from the ReadRowsResponse.
     */
    public void processRows(ArrowRecordBatch batch) throws IOException {
      org.apache.arrow.vector.ipc.message.ArrowRecordBatch deserializedBatch =
          MessageSerializer.deserializeRecordBatch(
              new ReadChannel(
                  new ByteArrayReadableSeekableByteChannel(
                      batch.getSerializedRecordBatch().toByteArray())),
              allocator);

      loader.load(deserializedBatch);
      // Release buffers from batch (they are still held in the vectors in root).
      deserializedBatch.close();
      System.out.println(root.contentToTSVString());
      // Release buffers from vectors in root.
      root.clear();
    }

    @Override
    public void close() {
      root.close();
      allocator.close();
    }
  }

  public static void main(String... args) throws Exception {
    // Sets your Google Cloud Platform project ID.
    // String projectId = "YOUR_PROJECT_ID";
    String projectId = args[0];
    Integer snapshotMillis = null;
    if (args.length > 1) {
      snapshotMillis = Integer.parseInt(args[1]);
    }

    try (BigQueryReadClient client = BigQueryReadClient.create()) {
      String parent = String.format("projects/%s", projectId);

      // This example uses baby name data from the public datasets.
      String srcTable =
          String.format(
              "projects/%s/datasets/%s/tables/%s",
              "bigquery-public-data", "usa_names", "usa_1910_current");

      // We specify the columns to be projected by adding them to the selected fields,
      // and set a simple filter to restrict which rows are transmitted.
      TableReadOptions options =
          TableReadOptions.newBuilder()
              .addSelectedFields("name")
              .addSelectedFields("number")
              .addSelectedFields("state")
              .setRowRestriction("state = \"WA\"")
              .build();

      // Start specifying the read session we want created.
      ReadSession.Builder sessionBuilder =
          ReadSession.newBuilder()
              .setTable(srcTable)
              // This API can also deliver data serialized in Apache Avro format.
              // This example leverages Apache Arrow.
              .setDataFormat(DataFormat.ARROW)
              .setReadOptions(options);

      // Optionally specify the snapshot time.  When unspecified, snapshot time is "now".
      if (snapshotMillis != null) {
        Timestamp t =
            Timestamp.newBuilder()
                .setSeconds(snapshotMillis / 1000)
                .setNanos((int) ((snapshotMillis % 1000) * 1000000))
                .build();
        TableModifiers modifiers = TableModifiers.newBuilder().setSnapshotTime(t).build();
        sessionBuilder.setTableModifiers(modifiers);
      }

      // Begin building the session creation request.
      CreateReadSessionRequest.Builder builder =
          CreateReadSessionRequest.newBuilder()
              .setParent(parent)
              .setReadSession(sessionBuilder)
              .setMaxStreamCount(1);

      ReadSession session = client.createReadSession(builder.build());
      // Setup a simple reader and start a read session.
      try (SimpleRowReader reader = new SimpleRowReader(session.getArrowSchema())) {

        // Assert that there are streams available in the session.  An empty table may not have
        // data available.  If no sessions are available for an anonymous (cached) table, consider
        // writing results of a query to a named table rather than consuming cached results
        // directly.
        Preconditions.checkState(session.getStreamsCount() > 0);

        // Use the first stream to perform reading.
        String streamName = session.getStreams(0).getName();

        ReadRowsRequest readRowsRequest =
            ReadRowsRequest.newBuilder().setReadStream(streamName).build();

        // Process each block of rows as they arrive and decode using our simple row reader.
        ServerStream<ReadRowsResponse> stream = client.readRowsCallable().call(readRowsRequest);
        for (ReadRowsResponse response : stream) {
          Preconditions.checkState(response.hasArrowRecordBatch());
          reader.processRows(response.getArrowRecordBatch());
        }
      }
    }
  }
}
```

## 後續步驟

如要搜尋及篩選其他 Google Cloud 產品的程式碼範例，請參閱[Google Cloud 範例瀏覽工具](https://docs.cloud.google.com/docs/samples?product=bigquerystorage&hl=zh-tw)。

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。




[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],[],[],[]]