* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [範例](https://docs.cloud.google.com/bigquery/docs/samples?hl=zh-tw)

# 使用載入工作新增資料欄 透過集合功能整理內容 你可以依據偏好儲存及分類內容。

使用載入工作附加資料列時，在 BigQuery 資料表中新增資料欄。

## 深入探索

如需包含這個程式碼範例的詳細說明文件，請參閱下列文章：

* [修改資料表結構定義](https://docs.cloud.google.com/bigquery/docs/managing-table-schemas?hl=zh-tw)

## 程式碼範例

### Go

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Go 設定說明操作。詳情請參閱 [BigQuery Go API 參考說明文件](https://godoc.org/cloud.google.com/go/bigquery)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import (
	"context"
	"fmt"
	"os"

	"cloud.google.com/go/bigquery"
)

// createTableAndWidenLoad demonstrates augmenting a table's schema to add a new column via a load job.
func createTableAndWidenLoad(projectID, datasetID, tableID, filename string) error {
	// projectID := "my-project-id"
	// datasetID := "mydataset"
	// tableID := "mytable"
	ctx := context.Background()
	client, err := bigquery.NewClient(ctx, projectID)
	if err != nil {
		return fmt.Errorf("bigquery.NewClient: %w", err)
	}
	defer client.Close()

	sampleSchema := bigquery.Schema{
		{Name: "full_name", Type: bigquery.StringFieldType},
	}
	meta := &bigquery.TableMetadata{
		Schema: sampleSchema,
	}
	tableRef := client.Dataset(datasetID).Table(tableID)
	if err := tableRef.Create(ctx, meta); err != nil {
		return err
	}
	// Now, import data from a local file, but specify field additions are allowed.
	// Because the data has a second column (age), the schema is amended as part of
	// the load.
	f, err := os.Open(filename)
	if err != nil {
		return err
	}
	source := bigquery.NewReaderSource(f)
	source.AutoDetect = true   // Allow BigQuery to determine schema.
	source.SkipLeadingRows = 1 // CSV has a single header line.

	loader := client.Dataset(datasetID).Table(tableID).LoaderFrom(source)
	loader.SchemaUpdateOptions = []string{"ALLOW_FIELD_ADDITION"}
	job, err := loader.Run(ctx)
	if err != nil {
		return err
	}
	status, err := job.Wait(ctx)
	if err != nil {
		return err
	}
	if err := status.Err(); err != nil {
		return err
	}
	return nil
}
```

### Java

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Java 設定說明操作。詳情請參閱 [BigQuery Java API 參考說明文件](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/overview?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import com.google.cloud.bigquery.BigQuery;
import com.google.cloud.bigquery.BigQueryException;
import com.google.cloud.bigquery.BigQueryOptions;
import com.google.cloud.bigquery.Field;
import com.google.cloud.bigquery.FormatOptions;
import com.google.cloud.bigquery.Job;
import com.google.cloud.bigquery.JobId;
import com.google.cloud.bigquery.JobInfo;
import com.google.cloud.bigquery.JobInfo.SchemaUpdateOption;
import com.google.cloud.bigquery.JobInfo.WriteDisposition;
import com.google.cloud.bigquery.LegacySQLTypeName;
import com.google.cloud.bigquery.LoadJobConfiguration;
import com.google.cloud.bigquery.Schema;
import com.google.cloud.bigquery.TableId;
import com.google.common.collect.ImmutableList;
import java.util.ArrayList;
import java.util.List;
import java.util.UUID;

// Sample to append column in existing table.
public class AddColumnLoadAppend {

  public static void main(String[] args) {
    // TODO(developer): Replace these variables before running the sample.
    String datasetName = "MY_DATASET_NAME";
    String tableName = "MY_TABLE_NAME";
    String sourceUri = "/path/to/file.csv";
    // Add a new column to a BigQuery table while appending rows via a load job.
    // 'REQUIRED' fields cannot  be added to an existing schema, so the additional column must be
    // 'NULLABLE'.
    Schema schema =
        Schema.of(
            Field.newBuilder("name", LegacySQLTypeName.STRING)
                .setMode(Field.Mode.REQUIRED)
                .build());

    List<Field> fields = schema.getFields();
    // Adding below additional column during the load job
    Field newField =
        Field.newBuilder("post_abbr", LegacySQLTypeName.STRING)
            .setMode(Field.Mode.NULLABLE)
            .build();
    List<Field> newFields = new ArrayList<>(fields);
    newFields.add(newField);
    Schema newSchema = Schema.of(newFields);
    addColumnLoadAppend(datasetName, tableName, sourceUri, newSchema);
  }

  public static void addColumnLoadAppend(
      String datasetName, String tableName, String sourceUri, Schema newSchema) {
    try {
      // Initialize client that will be used to send requests. This client only needs to be created
      // once, and can be reused for multiple requests.
      BigQuery bigquery = BigQueryOptions.getDefaultInstance().getService();

      TableId tableId = TableId.of(datasetName, tableName);

      LoadJobConfiguration loadJobConfig =
          LoadJobConfiguration.builder(tableId, sourceUri)
              .setFormatOptions(FormatOptions.csv())
              .setWriteDisposition(WriteDisposition.WRITE_APPEND)
              .setSchema(newSchema)
              .setSchemaUpdateOptions(ImmutableList.of(SchemaUpdateOption.ALLOW_FIELD_ADDITION))
              .build();

      // Create a job ID so that we can safely retry.
      JobId jobId = JobId.of(UUID.randomUUID().toString());
      Job loadJob = bigquery.create(JobInfo.newBuilder(loadJobConfig).setJobId(jobId).build());

      // Load data from a GCS parquet file into the table
      // Blocks until this load table job completes its execution, either failing or succeeding.
      Job job = loadJob.waitFor();

      // Check for errors
      if (job.isDone() && job.getStatus().getError() == null) {
        System.out.println("Column successfully added during load append job");
      } else {
        System.out.println(
            "BigQuery was unable to load into the table due to an error:"
                + job.getStatus().getError());
      }
    } catch (BigQueryException | InterruptedException e) {
      System.out.println("Column not added during load append \n" + e.toString());
    }
  }
}
```

### Node.js

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Node.js 設定說明操作。詳情請參閱 [BigQuery Node.js API 參考說明文件](https://googleapis.dev/nodejs/bigquery/latest/index.html)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
// Import the Google Cloud client libraries
const {BigQuery} = require('@google-cloud/bigquery');

// Instantiate client
const bigquery = new BigQuery();

async function addColumnLoadAppend() {
  // Adds a new column to a BigQuery table while appending rows via a load job.

  /**
   * TODO(developer): Uncomment the following lines before running the sample.
   */
  // const fileName = '/path/to/file.csv';
  // const datasetId = 'my_dataset';
  // const tableId = 'my_table';

  // In this example, the existing table contains only the 'Name', 'Age',
  // & 'Weight' columns. 'REQUIRED' fields cannot  be added to an existing
  // schema, so the additional column must be 'NULLABLE'.
  const schema = 'Name:STRING, Age:INTEGER, Weight:FLOAT, IsMagic:BOOLEAN';

  // Retrieve destination table reference
  const [table] = await bigquery.dataset(datasetId).table(tableId).get();
  const destinationTableRef = table.metadata.tableReference;

  // Set load job options
  const options = {
    schema: schema,
    schemaUpdateOptions: ['ALLOW_FIELD_ADDITION'],
    writeDisposition: 'WRITE_APPEND',
    destinationTable: destinationTableRef,
  };

  // Load data from a local file into the table
  const [job] = await bigquery
    .dataset(datasetId)
    .table(tableId)
    .load(fileName, options);

  console.log(`Job ${job.id} completed.`);
  console.log('New Schema:');
  console.log(job.configuration.load.schema.fields);

  // Check the job's status for errors
  const errors = job.status.errors;
  if (errors && errors.length > 0) {
    throw errors;
  }
}
```

### PHP

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 PHP 設定說明操作。詳情請參閱 [BigQuery PHP API 參考說明文件](https://docs.cloud.google.com/php/docs/reference/cloud-bigquery/latest/BigQueryClient?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
use Google\Cloud\BigQuery\BigQueryClient;

/**
 * Append a column using a load job.
 *
 * @param string $projectId The project Id of your Google Cloud Project.
 * @param string $datasetId The BigQuery dataset ID.
 * @param string $tableId The BigQuery table ID.
 */
function add_column_load_append(
    string $projectId,
    string $datasetId,
    string $tableId
): void {
    $bigQuery = new BigQueryClient([
      'projectId' => $projectId,
    ]);
    $dataset = $bigQuery->dataset($datasetId);
    $table = $dataset->table($tableId);
    // In this example, the existing table contains only the 'Name' and 'Title'.
    // A new column 'Description' gets added after load job.

    $schema = [
      'fields' => [
        ['name' => 'name', 'type' => 'string', 'mode' => 'nullable'],
        ['name' => 'title', 'type' => 'string', 'mode' => 'nullable'],
        ['name' => 'description', 'type' => 'string', 'mode' => 'nullable']
        ]
      ];

    $source = __DIR__ . '/../test/data/test_data_extra_column.csv';

    // Set job configs
    $loadConfig = $table->load(fopen($source, 'r'));
    $loadConfig->destinationTable($table);
    $loadConfig->schema($schema);
    $loadConfig->schemaUpdateOptions(['ALLOW_FIELD_ADDITION']);
    $loadConfig->sourceFormat('CSV');
    $loadConfig->writeDisposition('WRITE_APPEND');

    // Run the job with load config
    $job = $bigQuery->runJob($loadConfig);

    // Print all the columns
    $columns = $table->info()['schema']['fields'];
    printf('The columns in the table are ');
    foreach ($columns as $column) {
        printf('%s ', $column['name']);
    }
}
```

### Python

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Python 設定說明操作。詳情請參閱 [BigQuery Python API 參考說明文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
# from google.cloud import bigquery
# client = bigquery.Client()
# project = client.project
# dataset_ref = bigquery.DatasetReference(project, 'my_dataset')
# filepath = 'path/to/your_file.csv'

# Retrieves the destination table and checks the length of the schema
table_id = "my_table"
table_ref = dataset_ref.table(table_id)
table = client.get_table(table_ref)
print("Table {} contains {} columns.".format(table_id, len(table.schema)))

# Configures the load job to append the data to the destination table,
# allowing field addition
job_config = bigquery.LoadJobConfig()
job_config.write_disposition = bigquery.WriteDisposition.WRITE_APPEND
job_config.schema_update_options = [
    bigquery.SchemaUpdateOption.ALLOW_FIELD_ADDITION
]
# In this example, the existing table contains only the 'full_name' column.
# 'REQUIRED' fields cannot be added to an existing schema, so the
# additional column must be 'NULLABLE'.
job_config.schema = [
    bigquery.SchemaField("full_name", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("age", "INTEGER", mode="NULLABLE"),
]
job_config.source_format = bigquery.SourceFormat.CSV
job_config.skip_leading_rows = 1

with open(filepath, "rb") as source_file:
    job = client.load_table_from_file(
        source_file,
        table_ref,
        location="US",  # Must match the destination dataset location.
        job_config=job_config,
    )  # API request

job.result()  # Waits for table load to complete.
print(
    "Loaded {} rows into {}:{}.".format(
        job.output_rows, dataset_id, table_ref.table_id
    )
)

# Checks the updated length of the schema
table = client.get_table(table)
print("Table {} now contains {} columns.".format(table_id, len(table.schema)))
```

## 後續步驟

如要搜尋及篩選其他 Google Cloud 產品的程式碼範例，請參閱[Google Cloud 範例瀏覽工具](https://docs.cloud.google.com/docs/samples?product=bigquery&hl=zh-tw)。

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。




[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],[],[],[]]