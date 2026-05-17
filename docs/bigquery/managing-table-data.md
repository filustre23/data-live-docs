Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 管理資料表資料

本文件說明如何透過 BigQuery 管理資料表資料。您可以透過以下方法使用 BigQuery 資料表資料：

* 將資料載入資料表
* 附加或覆寫資料表資料
* 瀏覽 (或預覽) 資料表資料
* 查詢資料表資料
* 使用資料操縱語言 (DML) 修改資料表資料
* 複製資料表資料
* 匯出資料表資料

如需管理資料表結構定義的相關資訊，請參閱[修改資料表結構定義](https://docs.cloud.google.com/bigquery/docs/managing-table-schemas?hl=zh-tw)一文。

## 事前準備

授予角色，讓需要執行本文件各項工作的使用者取得必要權限。執行工作所需的權限 (如有) 會列在工作「必要權限」部分。

## 將資料載入至資料表

您可以在建立資料表時[載入資料](https://docs.cloud.google.com/bigquery/docs/loading-data?hl=zh-tw)，或是先建立空白的資料表，之後再載入資料。載入資料時，您可以使用[結構定義自動偵測](https://docs.cloud.google.com/bigquery/docs/schema-detect?hl=zh-tw)功能找出支援的資料格式，也可以[指定結構定義](https://docs.cloud.google.com/bigquery/docs/schemas?hl=zh-tw)。

如要深入瞭解如何載入資料，請參閱說明文件以瞭解來源資料的格式與位置：

* 如要深入瞭解如何從 Cloud Storage 載入資料，請參閱：

  + [載入 Avro 資料](https://docs.cloud.google.com/bigquery/docs/loading-data-cloud-storage-avro?hl=zh-tw)
  + [載入 CSV 資料](https://docs.cloud.google.com/bigquery/docs/loading-data-cloud-storage-csv?hl=zh-tw)
  + [載入 JSON 資料](https://docs.cloud.google.com/bigquery/docs/loading-data-cloud-storage-json?hl=zh-tw)
  + [載入 Parquet 資料](https://docs.cloud.google.com/bigquery/docs/loading-data-cloud-storage-parquet?hl=zh-tw)
  + [載入 ORC 資料](https://docs.cloud.google.com/bigquery/docs/loading-data-cloud-storage-orc?hl=zh-tw)
  + [從 Datastore 匯出內容載入資料](https://docs.cloud.google.com/bigquery/docs/loading-data-cloud-datastore?hl=zh-tw)
  + [從 Firestore 匯出檔案載入資料](https://docs.cloud.google.com/bigquery/docs/loading-data-cloud-firestore?hl=zh-tw)
* 如要進一步瞭解如何從本機來源載入資料，請參閱[從本機檔案載入資料](https://docs.cloud.google.com/bigquery/docs/batch-loading-data?hl=zh-tw)。

## 附加與覆寫資料表資料

您可以使用載入或查詢作業覆寫資料表資料。您可以藉由執行載入附加作業或將查詢結果附加至資料表，將其他資料附加到現有資料表。

如需在載入資料時附加或覆寫至資料表的詳細資訊，請參閱您的來源資料格式適用的說明文件。

* [將 Avro 資料附加或覆寫至資料表](https://docs.cloud.google.com/bigquery/docs/loading-data-cloud-storage-avro?hl=zh-tw#appending_to_or_overwriting_a_table_with_avro_data)
* [將 CSV 資料附加或覆寫至資料表](https://docs.cloud.google.com/bigquery/docs/loading-data-cloud-storage-csv?hl=zh-tw#appending_to_or_overwriting_a_table_with_csv_data)
* [將 JSON 資料附加或覆寫至資料表](https://docs.cloud.google.com/bigquery/docs/loading-data-cloud-storage-json?hl=zh-tw#appending_to_or_overwriting_a_table_with_json_data)
* [將 Parquet 資料附加或覆寫至資料表](https://docs.cloud.google.com/bigquery/docs/loading-data-cloud-storage-parquet?hl=zh-tw#appending_to_or_overwriting_a_table_with_parquet_data)
* [將 ORC 資料附加或覆寫至資料表](https://docs.cloud.google.com/bigquery/docs/loading-data-cloud-storage-orc?hl=zh-tw#append_to_or_overwrite_a_table_with_orc_data)
* [將 Datastore 資料附加或覆寫至資料表](https://docs.cloud.google.com/bigquery/docs/loading-data-cloud-datastore?hl=zh-tw#appending_to_or_overwriting_a_table_with_cloud_datastore_data)

如要使用查詢結果來附加或覆寫至資料表，請指定目的地資料表，並將寫入配置設為下列其中一項：

* Append to table (附加到資料表中)：將查詢結果附加至現有資料表。
* [Overwrite table] (覆寫資料表)：使用查詢結果覆寫名稱相同的現有資料表。

您可以使用下列查詢，將一個資料表的記錄附加到另一個資料表：

```
  INSERT INTO <projectID>.<datasetID>.<table1> (
    <column2>,
    <column3>) (SELECT * FROM <projectID>.<datasetID>.<table2>)
```

如需使用查詢結果來附加或覆寫資料的詳細資訊，請參閱[寫入查詢結果](https://docs.cloud.google.com/bigquery/docs/writing-results?hl=zh-tw#writing_query_results)一文。

## 瀏覽資料表中的資料

您可以透過下列方式瀏覽或讀取資料表中的資料：

* 使用 Google Cloud 控制台
* 使用 bq 指令列工具的 `bq head` 指令
* 呼叫 [`tabledata.list`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tabledata/list?hl=zh-tw) API 方法
* 使用用戶端程式庫

### 所需權限

如要讀取資料表和分區資料，您需要 `bigquery.tables.getData` Identity and Access Management (IAM) 權限。

**注意：** 在 `bigquery.tables.getData` 權限上建立 [IAM 拒絕政策](https://docs.cloud.google.com/iam/docs/deny-overview?hl=zh-tw)時，請考量[特殊情況](https://docs.cloud.google.com/bigquery/docs/control-access-to-resources-iam?hl=zh-tw#special_cases)。

下列每個預先定義的 IAM 角色都包含瀏覽表格和分割區資料所需的權限：

* `roles/bigquery.dataViewer`
* `roles/bigquery.dataEditor`
* `roles/bigquery.dataOwner`
* `roles/bigquery.admin`

如果您擁有 `bigquery.datasets.create` 權限，即可瀏覽所建立資料集中的資料表和分區資料。

如要進一步瞭解 BigQuery 中的 IAM 角色和權限，請參閱[預先定義的角色與權限](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)一文。

### 瀏覽資料表中的資料

如何瀏覽資料表中的資料：

### 控制台

1. 在 Google Cloud 控制台開啟「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」：

   如果沒有看到左側窗格，請按一下「展開左側窗格」圖示 last\_page 開啟窗格。
3. 在「Explorer」窗格中展開專案，點選「Datasets」(資料集)，然後選取資料集。
4. 依序點選「總覽」**>「表格」**，然後選取所需表格。
5. 按一下「詳細資料」，並記下「列數」中的值。使用 bq 指令列工具或 API 時，您可能需要這個值來控管結果的起點。
6. 按一下 [Preview] (預覽)。畫面上會顯示一組資料範例。

### 指令列

發出 `bq head` 指令並搭配使用 `--max_rows` 旗標，即可列出特定資料表列數的所有資料欄。如未指定 `--max_rows`，則預設值為 100。

如要瀏覽資料表中的資料欄子集 (包括巢狀和重複的資料欄)，請使用 `--selected_fields` 旗標並以逗號分隔的清單形式輸入資料欄。

如要指定顯示資料表中的資料前要略過的列數，請使用 `--start_row=integer` 旗標 (或 `-s` 捷徑)。預設值為 `0`。您可以使用 `bq show` 指令[擷取資料表資訊](https://docs.cloud.google.com/bigquery/docs/tables?hl=zh-tw#get_information_about_tables)，以擷取資料表中的列數。

如果您要瀏覽的資料表位於非預設專案中，請使用下列格式將專案 ID 新增至指令：`project_id:dataset.table`。

```
bq head \
--max_rows integer1 \
--start_row integer2 \
--selected_fields "columns" \
project_id:dataset.table
```

其中：

* integer1 是要顯示的列數。
* integer2 是顯示資料前略過的列數。
* columns 是以逗號分隔的資料欄清單。
* project\_id 是您的專案 ID。
* dataset 是包含此資料表的資料集名稱。
* table 是要瀏覽的資料表名稱。

範例：

輸入下列指令，列出 `mydataset.mytable` 中前 10 列的所有資料欄。`mydataset` 在您的預設專案中。

```
bq head --max_rows=10 mydataset.mytable
```

輸入下列指令，列出 `mydataset.mytable` 中前 100 列的所有資料欄。`mydataset` 在 `myotherproject` 中，而不是您的預設專案中。

```
bq head myotherproject:mydataset.mytable
```

輸入下列指令，只顯示 `mydataset.mytable` 中的 `field1` 和 `field2`。這個指令使用 `--start_row` 旗標直接跳到第 100 列。`mydataset.mytable` 在您的預設專案中。

```
bq head --start_row 100 --selected_fields "field1,field2" mydataset.mytable
```

因為 `bq head` 指令不會建立查詢工作，所以 `bq head` 指令不會出現在您的查詢記錄中，也不會產生費用。

### API

呼叫 [`tabledata.list`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tabledata/list?hl=zh-tw) 即可瀏覽整份資料表的資料。在 `tableId` 參數中指定資料表名稱。

設定以下選用參數控管輸出：

* `maxResults`：要傳回的結果數上限
* `selectedFields`：傳回以逗號分隔的資料欄清單。如果未指定，則會傳回所有資料欄
* `startIndex`：讀取的起始列，索引從零開始。

**附註：**如果您要求的 `startIndex` 超過最後一列，則這個方法雖然仍會成功傳回結果，但不會包含 `rows` 屬性。您可以呼叫 [`tables.get`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables/get?hl=zh-tw) 方法並檢查 `numRows` 屬性，藉此查看資料表的列數。

傳回的值會以 JSON 物件包裝，而您必須剖析這個物件，如 [`tabledata.list`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tabledata/list?hl=zh-tw) 參考說明文件所述。

### C#

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 C# 設定操作說明進行操作。詳情請參閱 [BigQuery C# API 參考說明文件](https://docs.cloud.google.com/dotnet/docs/reference/Google.Cloud.BigQuery.V2/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

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

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Go 設定操作說明進行操作。詳情請參閱 [BigQuery Go API 參考說明文件](https://godoc.org/cloud.google.com/go/bigquery)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

根據預設，[Go 專用的 Cloud 用戶端程式庫](https://docs.cloud.google.com/bigquery/docs/reference/libraries?hl=zh-tw)會自動進行分頁，因此您無須自行實作分頁程序，例如：

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

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Java 設定操作說明進行操作。詳情請參閱 [BigQuery Java API 參考說明文件](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/overview?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

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

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Node.js 設定操作說明進行操作。詳情請參閱 [BigQuery Node.js API 參考說明文件](https://googleapis.dev/nodejs/bigquery/latest/index.html)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

根據預設，[Node.js 適用的 Cloud 用戶端程式庫](https://docs.cloud.google.com/bigquery/docs/reference/libraries?hl=zh-tw)會自動進行分頁，因此您無須自行實作分頁程序，例如：

```
// Import the Google Cloud client library and create a client
const {BigQuery} = require('@google-cloud/bigquery');
const bigquery = new BigQuery();

async function browseRows() {
  // Displays rows from "my_table" in "my_dataset".

  /**
   * TODO(developer): Uncomment the following lines before running the sample.
   */
  // const datasetId = "my_dataset";
  // const tableId = "my_table";

  // List rows in the table
  const [rows] = await bigquery
    .dataset(datasetId)
    .table(tableId)
    .getRows();

  console.log('Rows:');
  rows.forEach(row => console.log(row));
}
```

### PHP

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 PHP 設定操作說明進行操作。詳情請參閱 [BigQuery PHP API 參考說明文件](https://docs.cloud.google.com/php/docs/reference/cloud-bigquery/latest/BigQueryClient?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

[PHP 適用的 Cloud 用戶端程式庫](https://docs.cloud.google.com/bigquery/docs/reference/libraries?hl=zh-tw)會透過產生器函式 `rows` 在疊代作業期間擷取下一頁的結果，藉此自動進行分頁。

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

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Python 設定操作說明進行操作。詳情請參閱 [BigQuery Python API 參考說明文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

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

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Ruby 設定操作說明進行操作。詳情請參閱 [BigQuery Ruby API 參考說明文件](https://googleapis.dev/ruby/google-cloud-bigquery/latest/Google/Cloud/Bigquery.html)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

[Ruby 適用的 Cloud 用戶端程式庫](https://docs.cloud.google.com/bigquery/docs/reference/libraries?hl=zh-tw)會透過 `Table#data` 和 `Data#next` 自動進行分頁。

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

## 查詢資料表資料

您可以使用下列其中一種查詢工作類型[查詢 BigQuery 資料](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw)：

* **[互動式查詢作業](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)**。根據預設，BigQuery 會以互動式查詢工作執行查詢，這類工作會盡快開始執行。
* **[批次查詢工作](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#batch)**。批次查詢的優先順序低於互動式查詢。如果專案或預訂項目已用盡所有可用的運算資源，批次查詢就更有可能排入佇列，並留在佇列中。批次查詢開始執行後，運作方式與互動式查詢相同。詳情請參閱「[查詢佇列](https://docs.cloud.google.com/bigquery/docs/query-queues?hl=zh-tw)」。
* **[持續查詢工作](https://docs.cloud.google.com/bigquery/docs/continuous-queries-introduction?hl=zh-tw)**。
  這些工作會持續執行查詢，讓您即時分析 BigQuery 中的輸入資料，然後將結果寫入 BigQuery 資料表，或將結果匯出至 Bigtable 或 Pub/Sub。這項功能可用於執行時間敏感型工作，例如建立洞察資料並立即採取行動、套用即時機器學習 (ML) 推論，以及建構事件導向資料管道。

您可以使用下列方法執行查詢工作：

* 在[Google Cloud 控制台](https://docs.cloud.google.com/bigquery/bigquery-web-ui?hl=zh-tw#overview)中編寫及執行查詢。
* 在 [bq 指令列工具](https://docs.cloud.google.com/bigquery/bq-command-line-tool?hl=zh-tw)中執行 `bq query` 指令。
* 透過程式呼叫 BigQuery [REST API](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2?hl=zh-tw) 中的 [`jobs.query`](https://docs.cloud.google.com/bigquery/docs/reference/v2/jobs/query?hl=zh-tw) 或 [`jobs.insert`](https://docs.cloud.google.com/bigquery/docs/reference/v2/jobs/insert?hl=zh-tw) 方法。
* 使用 BigQuery [用戶端程式庫](https://docs.cloud.google.com/bigquery/docs/reference/libraries?hl=zh-tw)。

關於如何查詢 BigQuery 資料表的詳情，請參閱[查詢 BigQuery 資料簡介](https://docs.cloud.google.com/bigquery/docs/query-overview?hl=zh-tw)。

除了查詢儲存在 BigQuery 表格中的資料外，您還可以查詢儲存在外部的資料。詳情請參閱[外部資料來源簡介](https://docs.cloud.google.com/bigquery/external-data-sources?hl=zh-tw)。

## 修改資料表資料

您可以使用 SQL 中的資料操縱語言 (DML) 陳述式，修改資料表中的資料。您可以使用 DML 陳述式[更新](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/dml-syntax?hl=zh-tw#update_statement)、[合併](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/dml-syntax?hl=zh-tw#merge_statement)、[插入](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/dml-syntax?hl=zh-tw#insert_statement)及[刪除](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/dml-syntax?hl=zh-tw#delete_statement)資料表中的資料列。如需各類型 DML 陳述式的語法參考資料和範例，請參閱「[GoogleSQL 中的資料操縱語言陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/dml-syntax?hl=zh-tw)」。

舊版 SQL 方言不支援 DML 陳述式。若要使用舊版 SQL 更新或刪除資料，您必須先刪除資料表，然後以新資料重新建立該資料表。另外，您也可以撰寫查詢來修改資料，並將查詢結果寫入新的目標資料表。

## 複製資料表資料

您可以透過以下方式複製資料表：

* 使用 Google Cloud 控制台
* 使用 bq 指令列工具的 `bq cp` 指令
* 呼叫 [`jobs.insert` API 方法](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs/insert?hl=zh-tw)並設定[複製工作](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#JobConfigurationTableCopy)
* 使用用戶端程式庫

如要深入瞭解複製資料表，請參閱[複製資料表](https://docs.cloud.google.com/bigquery/docs/managing-tables?hl=zh-tw#copy-table)一文。

## 匯出資料表資料

您可以將資料表資料匯出到 Cloud Storage 值區，格式為 CSV、JSON、Avro 或 Parquet ([預覽版](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages))。系統不支援將資料匯出至本機電腦，但您可使用 Google Cloud 控制台[下載和儲存查詢結果](https://docs.cloud.google.com/bigquery/docs/writing-results?hl=zh-tw#downloading-saving-results-console)。

詳情請參閱[匯出資料表資料](https://docs.cloud.google.com/bigquery/docs/exporting-data?hl=zh-tw)一文。

## 表格安全性

如要控管 BigQuery 資料表的存取權，請參閱「[使用 IAM 控管資源存取權](https://docs.cloud.google.com/bigquery/docs/control-access-to-resources-iam?hl=zh-tw)」。

## 後續步驟

* 如要深入瞭解如何載入資料，請參閱[載入資料簡介](https://docs.cloud.google.com/bigquery/docs/loading-data?hl=zh-tw)。
* 如要深入瞭解如何查詢資料，請參閱[查詢 BigQuery 資料簡介](https://docs.cloud.google.com/bigquery/docs/query-overview?hl=zh-tw)。
* 如要深入瞭解如何修改資料表結構定義，請參閱[修改資料表結構定義](https://docs.cloud.google.com/bigquery/docs/managing-table-schemas?hl=zh-tw)。
* 關於如何建立及使用資料表，請參閱[建立及使用資料表](https://docs.cloud.google.com/bigquery/docs/tables?hl=zh-tw)一文。
* 關於如何管理資料表，請參閱[管理資料表](https://docs.cloud.google.com/bigquery/docs/managing-tables?hl=zh-tw)一文。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-16 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-16 (世界標準時間)。"],[],[]]