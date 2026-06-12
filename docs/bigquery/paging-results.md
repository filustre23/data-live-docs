Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 使用 BigQuery API 進行分頁

本文說明如何使用 BigQuery API 搭配分頁功能，讀取大型資料集中的資料表資料和查詢結果。

BigQuery 會使用*分頁*功能，將大型資料集分成較小的區塊，稱為「頁面」。對大多數使用者而言，Cloud 用戶端程式庫會自動處理這項程序，但您也可以手動控制分頁，適用於網頁應用程式等特定用途。

## 使用自動分頁功能

Cloud 用戶端程式庫會處理 API 分頁的低階詳細資料，並提供類似迭代器的體驗。當您逐一查看結果時，程式庫會在需要時自動擷取下一頁資料。

下列範例示範如何自動逐一查看 BigQuery 資料表資料。

### C#

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 C# 設定說明操作。詳情請參閱 [BigQuery C# API 參考說明文件](https://docs.cloud.google.com/dotnet/docs/reference/Google.Cloud.BigQuery.V2/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
using Google.Api.Gax;
using Google.Apis.Bigquery.v2.Data;
using Google.Cloud.BigQuery.V2;
using System;
using System.Linq;

public class BigQueryBrowseTable
{
    public void BrowseTable(
        string projectId = "your-project-id"
    )
    {
        BigQueryClient client = BigQueryClient.Create(projectId);
        TableReference tableReference = new TableReference()
        {
            TableId = "shakespeare",
            DatasetId = "samples",
            ProjectId = "bigquery-public-data"
        };
        // Load all rows from a table
        PagedEnumerable<TableDataList, BigQueryRow> result = client.ListRows(
            tableReference: tableReference,
            schema: null
        );
        // Print the first 10 rows
        foreach (BigQueryRow row in result.Take(10))
        {
            Console.WriteLine($"{row["corpus"]}: {row["word_count"]}");
        }
    }
}
```

### Go

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Go 設定說明操作。詳情請參閱 [BigQuery Go API 參考說明文件](https://godoc.org/cloud.google.com/go/bigquery)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import (
	"context"
	"fmt"
	"io"

	"cloud.google.com/go/bigquery"
	"google.golang.org/api/iterator"
)

// browseTable demonstrates reading data from a BigQuery table directly without the use of a query.
// For large tables, we also recommend the BigQuery Storage API.
func browseTable(w io.Writer, projectID, datasetID, tableID string) error {
	// projectID := "my-project-id"
	// datasetID := "mydataset"
	// tableID := "mytable"
	ctx := context.Background()
	client, err := bigquery.NewClient(ctx, projectID)
	if err != nil {
		return fmt.Errorf("bigquery.NewClient: %v", err)
	}
	defer client.Close()

	table := client.Dataset(datasetID).Table(tableID)
	it := table.Read(ctx)
	for {
		var row []bigquery.Value
		err := it.Next(&row)
		if err == iterator.Done {
			break
		}
		if err != nil {
			return err
		}
		fmt.Fprintln(w, row)
	}
	return nil
}
```

### Java

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Java 設定說明操作。詳情請參閱 [BigQuery Java API 參考說明文件](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/overview?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import com.google.cloud.bigquery.BigQuery;
import com.google.cloud.bigquery.BigQuery.TableDataListOption;
import com.google.cloud.bigquery.BigQueryException;
import com.google.cloud.bigquery.BigQueryOptions;
import com.google.cloud.bigquery.TableId;
import com.google.cloud.bigquery.TableResult;

// Sample to directly browse a table with optional paging
public class BrowseTable {

  public static void runBrowseTable() {
    // TODO(developer): Replace these variables before running the sample.
    String table = "MY_TABLE_NAME";
    String dataset = "MY_DATASET_NAME";
    browseTable(dataset, table);
  }

  public static void browseTable(String dataset, String table) {
    try {
      // Initialize client that will be used to send requests. This client only needs to be created
      // once, and can be reused for multiple requests.
      BigQuery bigquery = BigQueryOptions.getDefaultInstance().getService();

      // Identify the table itself
      TableId tableId = TableId.of(dataset, table);

      // Page over 100 records. If you don't need pagination, remove the pageSize parameter.
      TableResult result = bigquery.listTableData(tableId, TableDataListOption.pageSize(100));

      // Print the records
      result
          .iterateAll()
          .forEach(
              row -> {
                row.forEach(fieldValue -> System.out.print(fieldValue.toString() + ", "));
                System.out.println();
              });

      System.out.println("Query ran successfully");
    } catch (BigQueryException e) {
      System.out.println("Query failed to run \n" + e.toString());
    }
  }
}
```

### Node.js

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Node.js 設定說明操作。詳情請參閱 [BigQuery Node.js API 參考說明文件](https://googleapis.dev/nodejs/bigquery/latest/index.html)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
// Import the Google Cloud client library using default credentials
const {BigQuery} = require('@google-cloud/bigquery');
const bigquery = new BigQuery();

async function browseTable() {
  // Retrieve a table's rows using manual pagination.

  /**
   * TODO(developer): Uncomment the following lines before running the sample.
   */
  // const datasetId = 'my_dataset'; // Existing dataset
  // const tableId = 'my_table'; // Table to create

  const query = `SELECT name, SUM(number) as total_people
    FROM \`bigquery-public-data.usa_names.usa_1910_2013\`
    GROUP BY name 
    ORDER BY total_people 
    DESC LIMIT 100`;

  // Create table reference.
  const dataset = bigquery.dataset(datasetId);
  const destinationTable = dataset.table(tableId);

  // For all options, see https://cloud.google.com/bigquery/docs/reference/rest/v2/Job#jobconfigurationquery
  const queryOptions = {
    query: query,
    destination: destinationTable,
  };

  // Run the query as a job
  const [job] = await bigquery.createQueryJob(queryOptions);

  // For all options, see https://cloud.google.com/bigquery/docs/reference/v2/jobs/getQueryResults
  const queryResultsOptions = {
    // Retrieve zero resulting rows.
    maxResults: 0,
  };

  // Wait for the job to finish.
  await job.getQueryResults(queryResultsOptions);

  function manualPaginationCallback(err, rows, nextQuery) {
    rows.forEach(row => {
      console.log(`name: ${row.name}, ${row.total_people} total people`);
    });

    if (nextQuery) {
      // More results exist.
      destinationTable.getRows(nextQuery, manualPaginationCallback);
    }
  }

  // For all options, see https://cloud.google.com/bigquery/docs/reference/v2/tabledata/list
  const getRowsOptions = {
    autoPaginate: false,
    maxResults: 20,
  };

  // Retrieve all rows.
  destinationTable.getRows(getRowsOptions, manualPaginationCallback);
}
browseTable();
```

### PHP

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 PHP 設定說明操作。詳情請參閱 [BigQuery PHP API 參考說明文件](https://docs.cloud.google.com/php/docs/reference/cloud-bigquery/latest/BigQueryClient?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
use Google\Cloud\BigQuery\BigQueryClient;

/** Uncomment and populate these variables in your code */
// $projectId = 'The Google project ID';
// $datasetId = 'The BigQuery dataset ID';
// $tableId   = 'The BigQuery table ID';
// $maxResults = 10;

$maxResults = 10;
$startIndex = 0;

$options = [
    'maxResults' => $maxResults,
    'startIndex' => $startIndex
];
$bigQuery = new BigQueryClient([
    'projectId' => $projectId,
]);
$dataset = $bigQuery->dataset($datasetId);
$table = $dataset->table($tableId);
$numRows = 0;
foreach ($table->rows($options) as $row) {
    print('---');
    foreach ($row as $column => $value) {
        printf('%s: %s' . PHP_EOL, $column, $value);
    }
    $numRows++;
}
```

### Python

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Python 設定說明操作。詳情請參閱 [BigQuery Python API 參考說明文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
from google.cloud import bigquery

# Construct a BigQuery client object.
client = bigquery.Client()

# TODO(developer): Set table_id to the ID of the table to browse data rows.
# table_id = "your-project.your_dataset.your_table_name"

# Download all rows from a table.
rows_iter = client.list_rows(table_id)  # Make an API request.

# Iterate over rows to make the API requests to fetch row data.
rows = list(rows_iter)
print("Downloaded {} rows from table {}".format(len(rows), table_id))

# Download at most 10 rows.
rows_iter = client.list_rows(table_id, max_results=10)
rows = list(rows_iter)
print("Downloaded {} rows from table {}".format(len(rows), table_id))

# Specify selected fields to limit the results to certain columns.
table = client.get_table(table_id)  # Make an API request.
fields = table.schema[:2]  # First two columns.
rows_iter = client.list_rows(table_id, selected_fields=fields, max_results=10)
rows = list(rows_iter)
print("Selected {} columns from table {}.".format(len(rows_iter.schema), table_id))
print("Downloaded {} rows from table {}".format(len(rows), table_id))

# Print row data in tabular format.
rows = client.list_rows(table, max_results=10)
format_string = "{!s:<16} " * len(rows.schema)
field_names = [field.name for field in rows.schema]
print(format_string.format(*field_names))  # Prints column headers.
for row in rows:
    print(format_string.format(*row))  # Prints row data.
```

### Ruby

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Ruby 設定說明操作。詳情請參閱 [BigQuery Ruby API 參考說明文件](https://googleapis.dev/ruby/google-cloud-bigquery/latest/Google/Cloud/Bigquery.html)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
require "google/cloud/bigquery"

def browse_table
  bigquery = Google::Cloud::Bigquery.new project_id: "bigquery-public-data"
  dataset  = bigquery.dataset "samples"
  table    = dataset.table "shakespeare"

  # Load all rows from a table
  rows = table.data

  # Load the first 10 rows
  rows = table.data max: 10

  # Print row data
  rows.each { |row| puts row }
end
```

## 控制頁面大小

您可以設定網頁大小，指定每個網路要求傳回的資料列數量上限。設定頁面大小有助於最佳化網路用量，或將資料放入記憶體。

在大多數用戶端程式庫中，呼叫 `list_rows` 或 `query` 等方法時，可以使用 `max_results` 或 `page_size` 參數。

## 使用網頁權杖手動分頁

手動分頁功能適用於*無狀態*應用程式，例如使用者點選「下一步」即可查看下一組結果的網路服務。在這個情境中，伺服器不會在要求之間維護有效的疊代器。

請改用*網頁權杖*，如下所示：

1. **要求網頁。**呼叫 API 並接收 `pageToken` 參數和資料列。
2. **繼續。**在下一個要求中，將相同的 `pageToken` 參數傳回 BigQuery，即可擷取下一個資料區塊。

下列範例說明如何擷取分頁符記，並用來擷取下一頁的查詢結果。

### API

讀取 [`jobs.config.query.destinationTable`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#JobConfigurationQuery.FIELDS.destination_table) 欄位，判斷查詢結果寫入的資料表。呼叫 [`tabledata.list`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tabledata/list?hl=zh-tw) 讀取查詢結果。

### Java

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Java 設定說明操作。詳情請參閱 [BigQuery Java API 參考說明文件](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/overview?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import com.google.cloud.bigquery.BigQuery;
import com.google.cloud.bigquery.BigQueryException;
import com.google.cloud.bigquery.BigQueryOptions;
import com.google.cloud.bigquery.QueryJobConfiguration;
import com.google.cloud.bigquery.TableId;
import com.google.cloud.bigquery.TableResult;

// Sample to run query with pagination.
public class QueryPagination {

  public static void main(String[] args) {
    String datasetName = "MY_DATASET_NAME";
    String tableName = "MY_TABLE_NAME";
    String query =
        "SELECT name, SUM(number) as total_people"
            + " FROM `bigquery-public-data.usa_names.usa_1910_2013`"
            + " GROUP BY name"
            + " ORDER BY total_people DESC"
            + " LIMIT 100";
    queryPagination(datasetName, tableName, query);
  }

  public static void queryPagination(String datasetName, String tableName, String query) {
    try {
      // Initialize client that will be used to send requests. This client only needs to be created
      // once, and can be reused for multiple requests.
      BigQuery bigquery = BigQueryOptions.getDefaultInstance().getService();

      TableId tableId = TableId.of(datasetName, tableName);
      QueryJobConfiguration queryConfig =
          QueryJobConfiguration.newBuilder(query)
              // save results into a table.
              .setDestinationTable(tableId)
              .build();

      bigquery.query(queryConfig);

      TableResult results =
          bigquery.listTableData(tableId, BigQuery.TableDataListOption.pageSize(20));

      // First Page
      results
          .getValues()
          .forEach(row -> row.forEach(val -> System.out.printf("%s,\n", val.toString())));

      while (results.hasNextPage()) {
        // Remaining Pages
        results = results.getNextPage();
        results
            .getValues()
            .forEach(row -> row.forEach(val -> System.out.printf("%s,\n", val.toString())));
      }

      System.out.println("Query pagination performed successfully.");
    } catch (BigQueryException | InterruptedException e) {
      System.out.println("Query not performed \n" + e.toString());
    }
  }
}
```

如要設定每頁傳回的資料列數量，請使用 [`GetQueryResults` 工作](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/com.google.cloud.bigquery.Job?hl=zh-tw#com_google_cloud_bigquery_Job_getQueryResults_com_google_cloud_bigquery_BigQuery_QueryResultsOption____)，並設定您傳入的 [`QueryResultsOption` 物件](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/com.google.cloud.bigquery.BigQuery.QueryResultsOption?hl=zh-tw)的 [`pageSize` 選項](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/com.google.cloud.bigquery.BigQuery.QueryResultsOption?hl=zh-tw#com_google_cloud_bigquery_BigQuery_QueryResultsOption_pageSize_long_)，如下列範例所示：

```
TableResult result = job.getQueryResults();
QueryResultsOption queryResultsOption = QueryResultsOption.pageSize(20);

TableResult result = job.getQueryResults(queryResultsOption);
```

### Node.js

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Node.js 設定說明操作。詳情請參閱 [BigQuery Node.js API 參考說明文件](https://googleapis.dev/nodejs/bigquery/latest/index.html)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
// Import the Google Cloud client library using default credentials
const {BigQuery} = require('@google-cloud/bigquery');
const bigquery = new BigQuery();

async function queryPagination() {
  // Run a query and get rows using automatic pagination.

  const query = `SELECT name, SUM(number) as total_people
  FROM \`bigquery-public-data.usa_names.usa_1910_2013\`
  GROUP BY name
  ORDER BY total_people DESC
  LIMIT 100`;

  // Run the query as a job.
  const [job] = await bigquery.createQueryJob(query);

  // Wait for job to complete and get rows.
  const [rows] = await job.getQueryResults();

  console.log('Query results:');
  rows.forEach(row => {
    console.log(`name: ${row.name}, ${row.total_people} total people`);
  });
}
queryPagination();
```

### Python

[`QueryJob.result`](https://docs.cloud.google.com/python/docs/reference/bigquery/latest/google.cloud.bigquery.job.QueryJob?hl=zh-tw#google_cloud_bigquery_job_QueryJob_result) 方法會傳回查詢結果的可疊代項目。或者

1. 讀取 [`QueryJob.destination`](https://docs.cloud.google.com/python/docs/reference/bigquery/latest/google.cloud.bigquery.job.QueryJob?hl=zh-tw#google_cloud_bigquery_job_QueryJob_destination) 屬性。如果未設定這項屬性，API 會將其設為[臨時匿名資料表](https://docs.cloud.google.com/bigquery/docs/writing-results?hl=zh-tw#temporary_and_permanent_tables)的參照。
2. 使用 [`Client.get_table`](https://docs.cloud.google.com/python/docs/reference/bigquery/latest/google.cloud.bigquery.client.Client?hl=zh-tw#google_cloud_bigquery_client_Client_get_table) 方法取得資料表結構定義。
3. 使用 [`Client.list_rows`](https://docs.cloud.google.com/python/docs/reference/bigquery/latest/google.cloud.bigquery.client.Client?hl=zh-tw#google_cloud_bigquery_client_Client_list_rows) 方法，在目的地資料表中的所有資料列上建立可疊代物件。

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Python 設定說明操作。詳情請參閱 [BigQuery Python API 參考說明文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
from google.cloud import bigquery

# Construct a BigQuery client object.
client = bigquery.Client()

query = """
    SELECT name, SUM(number) as total_people
    FROM `bigquery-public-data.usa_names.usa_1910_2013`
    GROUP BY name
    ORDER BY total_people DESC
"""
query_job = client.query(query)  # Make an API request.
query_job.result()  # Wait for the query to complete.

# Get the destination table for the query results.
#
# All queries write to a destination table. If a destination table is not
# specified, the BigQuery populates it with a reference to a temporary
# anonymous table after the query completes.
destination = query_job.destination

# Get the schema (and other properties) for the destination table.
#
# A schema is useful for converting from BigQuery types to Python types.
destination = client.get_table(destination)

# Download rows.
#
# The client library automatically handles pagination.
print("The query data:")
rows = client.list_rows(destination, max_results=20)
for row in rows:
    print("name={}, count={}".format(row["name"], row["total_people"]))
```

## 使用 ETag 進行最佳化

當您使用快取的 `pageToken` 值往前翻頁或跳到任意頁面時，頁面內的資料就有可能會因為最近瀏覽過而變更，為避免發生這種情況，您可以使用 `etag` 屬性。

每個 `collection.list` 方法 (`Tabledata` 除外) 都會在結果中傳回 `etag` 屬性。這個屬性是頁面結果的雜湊值，可用於驗證頁面自上次要求後是否有所變更。當您使用 ETag 值對 BigQuery 進行要求時，BigQuery 會將這個 ETag 值和 API 傳回的 ETag 值進行比較，並依這兩個 ETag 值是否相符來進行回應。您可以按照下列方式使用 ETag，避免多餘的清單呼叫：

* 如要只在值有變更時傳回值，請使用 [HTTP `If-None-Match` 標頭](https://www.rfc-editor.org/rfc/rfc9110.html#name-if-none-match)，藉由先前儲存的 ETag 進行清單呼叫。如果 ETag 相符，BigQuery 會傳回 `HTTP 304 Not Modified` 狀態碼，且不會傳回任何資料，節省頻寬。
* 如要只在值**未**變更時傳回值，請使用 [HTTP `If-Match` 標頭](https://www.rfc-editor.org/rfc/rfc9110.html#name-if-match)。如果頁面已變更，BigQuery 會傳回 `412 Precondition Failed`。

**備註：**雖然 ETag 是避免進行多餘清單呼叫的好方法，不過您可以採用同樣方式來確定是否有任何已變更的物件。例如，您可以針對特定資料表執行 `GET` 要求，並使用 ETag 判斷資料表在傳回完整回應前是否變更過。

## 參考資料：API 限制和條件

在某些情況下，所有 `*collection*.list` 方法都會傳回分頁結果。`maxResults` 屬性會限制每頁的結果數。

| 方法 | 分頁條件 | 預設 `maxResults` 限制 | 最多只能有 `maxResults` 個捷徑 | 最多只能有 `maxFieldValues` 個捷徑 |
| --- | --- | --- | --- | --- |
| `tabledata.list` | 如果回應大小超過 10 MB1 的資料或超過 `maxResults` 個資料列，就會傳回分成數頁的結果。 | 無限制 | 無限制 | 無限制 |
| 所有其他 `*collection*.list` 方法 | 如果回應超過 `maxResults` 個資料列，但未達上限，就會傳回分成數頁的結果。 | 10,000 | 無限制 | 300,000 |

如果結果超出位元組或欄位限制，系統會將結果截斷，以符合限制。如果單一資料列超出位元組或欄位限制，`tabledata.list` 方法最多可傳回 100 MB 的資料1，這與查詢結果的資料列大小上限一致。每個頁面沒有大小下限，因此部分頁面可能會傳回的資料列比其他頁面多。

除非您透過支援服務明確要求更多資料，否則 `jobs.getQueryResults` REST API 方法最多只會傳回 20 MB 的資料。

1資料列大小為約略值，因為此大小是根據資料列資料的內部呈現方式而定。系統會在查詢工作執行作業的某些階段對資料列大小設定上限。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-06-11 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-06-11 (世界標準時間)。"],[],[]]