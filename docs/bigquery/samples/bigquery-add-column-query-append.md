Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [範例](https://docs.cloud.google.com/bigquery/docs/samples?hl=zh-tw)

# 使用查詢工作新增資料欄 透過集合功能整理內容 你可以依據偏好儲存及分類內容。

使用查詢工作附加資料列時，一併將新資料欄新增至 BigQuery 資料表，並明確指定目的地資料表。

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

	"cloud.google.com/go/bigquery"
)

// createTableAndWidenQuery demonstrates how the schema of a table can be modified to add columns by appending
// query results that include the new columns.
func createTableAndWidenQuery(projectID, datasetID, tableID string) error {
	// projectID := "my-project-id"
	// datasetID := "mydataset"
	// tableID := "mytable"
	ctx := context.Background()
	client, err := bigquery.NewClient(ctx, projectID)
	if err != nil {
		return fmt.Errorf("bigquery.NewClient: %w", err)
	}
	defer client.Close()

	// First, we create a sample table.
	sampleSchema := bigquery.Schema{
		{Name: "full_name", Type: bigquery.StringFieldType, Required: true},
		{Name: "age", Type: bigquery.IntegerFieldType, Required: true},
	}
	original := &bigquery.TableMetadata{
		Schema: sampleSchema,
	}
	tableRef := client.Dataset(datasetID).Table(tableID)
	if err := tableRef.Create(ctx, original); err != nil {
		return err
	}
	// Our table has two columns.  We'll introduce a new favorite_color column via
	// a subsequent query that appends to the table.
	q := client.Query("SELECT \"Timmy\" as full_name, 85 as age, \"Blue\" as favorite_color")
	q.SchemaUpdateOptions = []string{"ALLOW_FIELD_ADDITION"}
	q.QueryConfig.Dst = client.Dataset(datasetID).Table(tableID)
	q.WriteDisposition = bigquery.WriteAppend
	q.Location = "US"
	job, err := q.Run(ctx)
	if err != nil {
		return err
	}
	_, err = job.Wait(ctx)
	if err != nil {
		return err
	}
	return nil
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

async function addColumnQueryAppend() {
  // Adds a new column to a BigQuery table while appending rows via a query job.

  /**
   * TODO(developer): Uncomment the following lines before running the sample.
   */
  // const datasetId = 'my_dataset';
  // const tableId = 'my_table';

  // Retrieve destination table reference
  const [table] = await bigquery.dataset(datasetId).table(tableId).get();
  const destinationTableRef = table.metadata.tableReference;

  // In this example, the existing table contains only the 'name' column.
  // 'REQUIRED' fields cannot  be added to an existing schema,
  // so the additional column must be 'NULLABLE'.
  const query = `SELECT name, year
    FROM \`bigquery-public-data.usa_names.usa_1910_2013\`
    WHERE state = 'TX'
    LIMIT 10`;

  // Set load job options
  const options = {
    query: query,
    schemaUpdateOptions: ['ALLOW_FIELD_ADDITION'],
    writeDisposition: 'WRITE_APPEND',
    destinationTable: destinationTableRef,
    // Location must match that of the dataset(s) referenced in the query.
    location: 'US',
  };

  const [job] = await bigquery.createQueryJob(options);
  console.log(`Job ${job.id} started.`);

  // Wait for the query to finish
  const [rows] = await job.getQueryResults();
  console.log(`Job ${job.id} completed.`);

  // Print the results
  console.log('Rows:');
  rows.forEach(row => console.log(row));
}
```

### PHP

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 PHP 設定說明操作。詳情請參閱 [BigQuery PHP API 參考說明文件](https://docs.cloud.google.com/php/docs/reference/cloud-bigquery/latest/BigQueryClient?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
use Google\Cloud\BigQuery\BigQueryClient;

/**
 * Append a column using a query job.
 *
 * @param string $projectId The project Id of your Google Cloud Project.
 * @param string $datasetId The BigQuery dataset ID.
 * @param string $tableId The BigQuery table ID.
 */
function add_column_query_append(
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
    // A new column 'Description' gets added after the query job.

    // Define query
    $query = sprintf('SELECT "John" as name, "Unknown" as title, "Dummy person" as description;');

    // Set job configs
    $queryJobConfig = $bigQuery->query($query);
    $queryJobConfig->destinationTable($table);
    $queryJobConfig->schemaUpdateOptions(['ALLOW_FIELD_ADDITION']);
    $queryJobConfig->writeDisposition('WRITE_APPEND');

    // Run query with query job configuration
    $bigQuery->runQuery($queryJobConfig);

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
from google.cloud import bigquery

# Construct a BigQuery client object.
client = bigquery.Client()

# TODO(developer): Set table_id to the ID of the destination table.
# table_id = "your-project.your_dataset.your_table_name"

# Retrieves the destination table and checks the length of the schema.
table = client.get_table(table_id)  # Make an API request.
print("Table {} contains {} columns".format(table_id, len(table.schema)))

# Configures the query to append the results to a destination table,
# allowing field addition.
job_config = bigquery.QueryJobConfig(
    destination=table_id,
    schema_update_options=[bigquery.SchemaUpdateOption.ALLOW_FIELD_ADDITION],
    write_disposition=bigquery.WriteDisposition.WRITE_APPEND,
)

# Start the query, passing in the extra configuration.
client.query_and_wait(
    # In this example, the existing table contains only the 'full_name' and
    # 'age' columns, while the results of this query will contain an
    # additional 'favorite_color' column.
    'SELECT "Timmy" as full_name, 85 as age, "Blue" as favorite_color;',
    job_config=job_config,
)  # Make an API request and wait for job to complete.

# Checks the updated length of the schema.
table = client.get_table(table_id)  # Make an API request.
print("Table {} now contains {} columns".format(table_id, len(table.schema)))
```

## 後續步驟

如要搜尋及篩選其他 Google Cloud 產品的程式碼範例，請參閱[Google Cloud 範例瀏覽工具](https://docs.cloud.google.com/docs/samples?product=bigquery&hl=zh-tw)。

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。




[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],[],[],[]]