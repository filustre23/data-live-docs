* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [範例](https://docs.cloud.google.com/bigquery/docs/samples?hl=zh-tw)

# 在載入附加工作期間放寬資料欄 透過集合功能整理內容 你可以依據偏好儲存及分類內容。

在載入附加工作中，將資料欄從必要變更為可為空值。

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

// relaxTableImport demonstrates amending the schema of a table to relax columns from
// not allowing NULL values to allowing them.
func relaxTableImport(projectID, datasetID, tableID, filename string) error {
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
		{Name: "full_name", Type: bigquery.StringFieldType, Required: true},
		{Name: "age", Type: bigquery.IntegerFieldType, Required: true},
	}
	meta := &bigquery.TableMetadata{
		Schema: sampleSchema,
	}
	tableRef := client.Dataset(datasetID).Table(tableID)
	if err := tableRef.Create(ctx, meta); err != nil {
		return err
	}
	// Now, import data from a local file, but specify relaxation of required
	// fields as a side effect while the data is appended.
	f, err := os.Open(filename)
	if err != nil {
		return err
	}
	source := bigquery.NewReaderSource(f)
	source.AutoDetect = true   // Allow BigQuery to determine schema.
	source.SkipLeadingRows = 1 // CSV has a single header line.

	loader := client.Dataset(datasetID).Table(tableID).LoaderFrom(source)
	loader.SchemaUpdateOptions = []string{"ALLOW_FIELD_RELAXATION"}
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
import com.google.cloud.bigquery.CsvOptions;
import com.google.cloud.bigquery.Field;
import com.google.cloud.bigquery.Job;
import com.google.cloud.bigquery.JobInfo;
import com.google.cloud.bigquery.LoadJobConfiguration;
import com.google.cloud.bigquery.Schema;
import com.google.cloud.bigquery.StandardSQLTypeName;
import com.google.cloud.bigquery.Table;
import com.google.cloud.bigquery.TableId;
import com.google.common.collect.ImmutableList;

// Sample to append relax column in a table.
public class RelaxColumnLoadAppend {

  public static void main(String[] args) {
    // TODO(developer): Replace these variables before running the sample.
    String datasetName = "MY_DATASET_NAME";
    String tableName = "MY_TABLE_NAME";
    String sourceUri = "gs://cloud-samples-data/bigquery/us-states/us-states.csv";
    relaxColumnLoadAppend(datasetName, tableName, sourceUri);
  }

  public static void relaxColumnLoadAppend(String datasetName, String tableName, String sourceUri) {
    try {
      // Initialize client that will be used to send requests. This client only needs to be created
      // once, and can be reused for multiple requests.
      BigQuery bigquery = BigQueryOptions.getDefaultInstance().getService();

      // Retrieve destination table reference
      Table table = bigquery.getTable(TableId.of(datasetName, tableName));

      // column as a 'REQUIRED' field.
      Field name =
          Field.newBuilder("name", StandardSQLTypeName.STRING).setMode(Field.Mode.REQUIRED).build();
      Field postAbbr =
          Field.newBuilder("post_abbr", StandardSQLTypeName.STRING)
              .setMode(Field.Mode.REQUIRED)
              .build();
      Schema schema = Schema.of(name, postAbbr);

      // Skip header row in the file.
      CsvOptions csvOptions = CsvOptions.newBuilder().setSkipLeadingRows(1).build();

      // Set job options
      LoadJobConfiguration loadConfig =
          LoadJobConfiguration.newBuilder(table.getTableId(), sourceUri)
              .setSchema(schema)
              .setFormatOptions(csvOptions)
              .setSchemaUpdateOptions(
                  ImmutableList.of(JobInfo.SchemaUpdateOption.ALLOW_FIELD_RELAXATION))
              .setWriteDisposition(JobInfo.WriteDisposition.WRITE_APPEND)
              .build();

      // Create a load job and wait for it to complete.
      Job job = bigquery.create(JobInfo.of(loadConfig));
      job = job.waitFor();
      // Check the job's status for errors
      if (job.isDone() && job.getStatus().getError() == null) {
        System.out.println("Relax column append successfully loaded in a table");
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

async function relaxColumnLoadAppend() {
  // Changes required column to nullable in load append job.

  /**
   * TODO(developer): Uncomment the following lines before running the sample.
   */
  // const fileName = '/path/to/file.csv';
  // const datasetId = 'my_dataset';
  // const tableId = 'my_table';

  // In this example, the existing table contains the 'Name'
  // column as a 'REQUIRED' field.
  const schema = 'Age:INTEGER, Weight:FLOAT, IsMagic:BOOLEAN';

  // Retrieve destination table reference
  const [table] = await bigquery.dataset(datasetId).table(tableId).get();
  const destinationTableRef = table.metadata.tableReference;

  // Set load job options
  const options = {
    schema: schema,
    schemaUpdateOptions: ['ALLOW_FIELD_RELAXATION'],
    writeDisposition: 'WRITE_APPEND',
    destinationTable: destinationTableRef,
  };

  // Load data from a local file into the table
  const [job] = await bigquery
    .dataset(datasetId)
    .table(tableId)
    .load(fileName, options);

  console.log(`Job ${job.id} completed.`);

  // Check the job's status for errors
  const errors = job.status.errors;
  if (errors && errors.length > 0) {
    throw errors;
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

# Retrieves the destination table and checks the number of required fields
table_id = "my_table"
table_ref = dataset_ref.table(table_id)
table = client.get_table(table_ref)
original_required_fields = sum(field.mode == "REQUIRED" for field in table.schema)
# In this example, the existing table has 3 required fields.
print("{} fields in the schema are required.".format(original_required_fields))

# Configures the load job to append the data to a destination table,
# allowing field relaxation
job_config = bigquery.LoadJobConfig()
job_config.write_disposition = bigquery.WriteDisposition.WRITE_APPEND
job_config.schema_update_options = [
    bigquery.SchemaUpdateOption.ALLOW_FIELD_RELAXATION
]
# In this example, the existing table contains three required fields
# ('full_name', 'age', and 'favorite_color'), while the data to load
# contains only the first two fields.
job_config.schema = [
    bigquery.SchemaField("full_name", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("age", "INTEGER", mode="REQUIRED"),
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

# Checks the updated number of required fields
table = client.get_table(table)
current_required_fields = sum(field.mode == "REQUIRED" for field in table.schema)
print("{} fields in the schema are now required.".format(current_required_fields))
```

## 後續步驟

如要搜尋及篩選其他 Google Cloud 產品的程式碼範例，請參閱[Google Cloud 範例瀏覽工具](https://docs.cloud.google.com/docs/samples?product=bigquery&hl=zh-tw)。

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。




[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],[],[],[]]