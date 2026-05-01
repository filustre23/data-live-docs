* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [範例](https://docs.cloud.google.com/bigquery/docs/samples?hl=zh-tw)

# 在查詢附加工作中放寬資料欄 透過集合功能整理內容 你可以依據偏好儲存及分類內容。

在查詢附加工作中，將必要資料欄變更為可為空值的資料欄。

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

// relaxTableQuery demonstrates relaxing the schema of a table by appending query results to
// enable the table to allow NULL values.
func relaxTableQuery(projectID, datasetID, tableID string) error {
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
	// Now, append a query result that includes nulls, but allow the job to relax
	// all required columns.
	q := client.Query("SELECT \"Beyonce\" as full_name")
	q.QueryConfig.Dst = client.Dataset(datasetID).Table(tableID)
	q.SchemaUpdateOptions = []string{"ALLOW_FIELD_RELAXATION"}
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

### Java

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Java 設定說明操作。詳情請參閱 [BigQuery Java API 參考說明文件](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/overview?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import com.google.cloud.bigquery.BigQuery;
import com.google.cloud.bigquery.BigQueryException;
import com.google.cloud.bigquery.BigQueryOptions;
import com.google.cloud.bigquery.Job;
import com.google.cloud.bigquery.JobInfo;
import com.google.cloud.bigquery.JobInfo.SchemaUpdateOption;
import com.google.cloud.bigquery.JobInfo.WriteDisposition;
import com.google.cloud.bigquery.QueryJobConfiguration;
import com.google.cloud.bigquery.TableId;
import com.google.cloud.bigquery.TableResult;
import com.google.common.collect.ImmutableList;

public class RelaxTableQuery {

  public static void main(String[] args) throws Exception {
    // TODO(developer): Replace these variables before running the sample.
    String projectId = "MY_PROJECT_ID";
    String datasetName = "MY_DATASET_NAME";
    String tableName = "MY_TABLE_NAME";
    relaxTableQuery(projectId, datasetName, tableName);
  }

  // To relax all columns in a destination table when you append data to it during a query job
  public static void relaxTableQuery(String projectId, String datasetName, String tableName)
      throws Exception {
    try {
      // Initialize client that will be used to send requests. This client only needs to be created
      // once, and can be reused for multiple requests.
      BigQuery bigquery = BigQueryOptions.getDefaultInstance().getService();

      TableId tableId = TableId.of(datasetName, tableName);

      String sourceTable = "`" + projectId + "." + datasetName + "." + tableName + "`";
      String query = "SELECT word FROM " + sourceTable + " WHERE word like '%is%'";

      QueryJobConfiguration queryConfig =
          QueryJobConfiguration.newBuilder(query)
              // Use standard SQL syntax for queries.
              // See: https://cloud.google.com/bigquery/sql-reference/
              .setUseLegacySql(false)
              .setSchemaUpdateOptions(ImmutableList.of(SchemaUpdateOption.ALLOW_FIELD_RELAXATION))
              .setWriteDisposition(WriteDisposition.WRITE_APPEND)
              .setDestinationTable(tableId)
              .build();

      Job queryJob = bigquery.create(JobInfo.newBuilder(queryConfig).build());

      queryJob = queryJob.waitFor();

      // Check for errors
      if (queryJob == null) {
        throw new Exception("Job no longer exists");
      } else if (queryJob.getStatus().getError() != null) {
        // You can also look at queryJob.getStatus().getExecutionErrors() for all
        // errors, not just the latest one.
        throw new Exception(queryJob.getStatus().getError().toString());
      }

      // Get the results.
      TableResult results = queryJob.getQueryResults();

      // Print all pages of the results.
      results
          .iterateAll()
          .forEach(
              rows -> {
                rows.forEach(row -> System.out.println("row: " + row.toString()));
              });

      System.out.println("Successfully relaxed all columns in destination table during query job");
    } catch (BigQueryException | InterruptedException e) {
      System.out.println("Columns not relaxed during query job \n" + e.toString());
    }
  }
}
```

### Node.js

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Node.js 設定說明操作。詳情請參閱 [BigQuery Node.js API 參考說明文件](https://googleapis.dev/nodejs/bigquery/latest/index.html)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
const {BigQuery} = require('@google-cloud/bigquery');
const bigquery = new BigQuery();

async function relaxColumnQueryAppend() {
  // Change required to null in query append job

  /**
   * TODO(developer): Uncomment the following lines before running the sample.
   */
  // const projectId = "my_project"
  // const datasetId = "my_dataset"
  // const tableId = "my_table"

  // Retrieve the destination table and checks the number of required fields.
  const dataset = await bigquery.dataset(datasetId);
  const table = await dataset.table(tableId);
  const [metaData] = await table.getMetadata();

  const requiredFields = metaData.schema.fields.filter(
    ({mode}) => mode === 'REQUIRED',
  ).length;

  console.log(`${requiredFields} fields in the schema are required.`);

  // Create destination table reference
  const tableRef = {
    projectId,
    tableId,
    datasetId,
  };

  /* Configure the query to append the results to a destination table,
   * allowing field relaxation. In this example, the existing table
   * contains 'age' as a required column.
   *
   * For all options, see https://cloud.google.com/bigquery/docs/reference/rest/v2/Job#JobConfigurationQuery
   */
  const queryJobConfig = {
    query: `SELECT age FROM \`${projectId}.${datasetId}.${tableId}\``,
    destinationTable: tableRef,
    schemaUpdateOptions: ['ALLOW_FIELD_RELAXATION'],
    writeDisposition: ['WRITE_APPEND'],
    useLegacySql: false,
  };

  // Configure the job.
  const jobConfig = {
    configuration: {
      query: queryJobConfig,
    },
  };

  // Start the query, passing in the extra configuration.
  const response = await bigquery.createJob(jobConfig);
  const job = response[0];

  // Wait for job to complete.
  await job.getQueryResults(job);

  // Check the updated number of required fields.
  const updatedTable = await dataset.table(tableId);
  const [updatedMetaData] = await updatedTable.getMetadata();

  const updatedRequiredFields = updatedMetaData.schema.fields.filter(
    ({mode}) => mode === 'REQUIRED',
  ).length;

  console.log(
    `${updatedRequiredFields} fields in the schema are now required.`,
  );
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

# Retrieves the destination table and checks the number of required fields.
table = client.get_table(table_id)  # Make an API request.
original_required_fields = sum(field.mode == "REQUIRED" for field in table.schema)

# In this example, the existing table has 2 required fields.
print("{} fields in the schema are required.".format(original_required_fields))

# Configures the query to append the results to a destination table,
# allowing field relaxation.
job_config = bigquery.QueryJobConfig(
    destination=table_id,
    schema_update_options=[bigquery.SchemaUpdateOption.ALLOW_FIELD_RELAXATION],
    write_disposition=bigquery.WriteDisposition.WRITE_APPEND,
)

# Start the query, passing in the extra configuration.
client.query_and_wait(
    # In this example, the existing table contains 'full_name' and 'age' as
    # required columns, but the query results will omit the second column.
    'SELECT "Beyonce" as full_name;',
    job_config=job_config,
)  # Make an API request and wait for job to complete

# Checks the updated number of required fields.
table = client.get_table(table_id)  # Make an API request.
current_required_fields = sum(field.mode == "REQUIRED" for field in table.schema)
print("{} fields in the schema are now required.".format(current_required_fields))
```

## 後續步驟

如要搜尋及篩選其他 Google Cloud 產品的程式碼範例，請參閱[Google Cloud 範例瀏覽工具](https://docs.cloud.google.com/docs/samples?product=bigquery&hl=zh-tw)。

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。




[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],[],[],[]]