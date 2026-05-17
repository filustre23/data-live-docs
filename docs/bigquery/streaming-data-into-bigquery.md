Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見

# 使用舊版串流 API 透過集合功能整理內容 你可以依據偏好儲存及分類內容。

本文說明如何使用舊版 [`tabledata.insertAll`](https://docs.cloud.google.com/bigquery/docs/reference/v2/tabledata/insertAll?hl=zh-tw) 方法，將資料以串流方式傳入 BigQuery。

如果是新專案，建議使用 [BigQuery Storage Write API](https://docs.cloud.google.com/bigquery/docs/write-api?hl=zh-tw)，而不要使用 `tabledata.insertAll` 方法。Storage Write API 的定價較低且功能更強大 (包括單次傳送語意)，如果您要將現有專案從 `tabledata.insertAll` 方法遷移至 Storage Write API，建議選取[預設串流](https://docs.cloud.google.com/bigquery/docs/write-api-streaming?hl=zh-tw#at-least-once)。`tabledata.insertAll` 方法仍完全受支援。

## 事前準備

1. 確認您具備目的地資料表所屬資料集的寫入權限。除非您使用範本資料表，否則該資料表在開始寫入資料之前就必須存在。如要進一步瞭解範本資料表，請參閱[使用範本資料表自動建立資料表](#template-tables)。
2. 查看[串流資料的配額政策](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#streaming_inserts)。
3. [確認專案已啟用計費功能 Google Cloud](https://docs.cloud.google.com/billing/docs/how-to/verify-billing-enabled?hl=zh-tw#confirm_billing_is_enabled_on_a_project) 。

[免費方案](https://cloud.google.com/bigquery/pricing?hl=zh-tw#free-tier)並不支援資料串流功能。如果不啟用計費功能，當您嘗試進行資料串流作業時，系統會顯示下列錯誤訊息：`BigQuery: Streaming insert is not allowed in the free tier.`

4. 授予身分與存取權管理 (IAM) 角色，讓使用者擁有執行本文件各項工作所需的權限。

### 所需權限

如要將資料以串流方式傳入 BigQuery，您需要下列 IAM 權限：

* `bigquery.tables.updateData` (可將資料插入表格)
* `bigquery.tables.get` (可取得資料表中繼資料)
* `bigquery.datasets.get` (可取得資料集中繼資料)
* `bigquery.tables.create` (如果您使用[範本資料表](#template-tables)自動建立資料表，則為必要目錄)

下列每個預先定義的 IAM 角色都包含將資料串流至 BigQuery 所需的權限：

* `roles/bigquery.dataEditor`
* `roles/bigquery.dataOwner`
* `roles/bigquery.admin`

如要進一步瞭解 BigQuery 中的 IAM 角色和權限，請參閱[預先定義的角色和權限](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)一文。

## 將資料串流至 BigQuery

### C#

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 C# 設定說明操作。詳情請參閱 [BigQuery C# API 參考說明文件](https://docs.cloud.google.com/dotnet/docs/reference/Google.Cloud.BigQuery.V2/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
using Google.Cloud.BigQuery.V2;

public class BigQueryTableInsertRows
{
    public void TableInsertRows(
        string projectId = "your-project-id",
        string datasetId = "your_dataset_id",
        string tableId = "your_table_id"
    )
    {
        BigQueryClient client = BigQueryClient.Create(projectId);
        BigQueryInsertRow[] rows = new BigQueryInsertRow[]
        {
            // The insert ID is optional, but can avoid duplicate data
            // when retrying inserts.
            new BigQueryInsertRow(insertId: "row1") {
                { "name", "Washington" },
                { "post_abbr", "WA" }
            },
            new BigQueryInsertRow(insertId: "row2") {
                { "name", "Colorado" },
                { "post_abbr", "CO" }
            }
        };
        client.InsertRows(datasetId, tableId, rows);
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

	"cloud.google.com/go/bigquery"
)

// Item represents a row item.
type Item struct {
	Name string
	Age  int
}

// Save implements the ValueSaver interface.
// This example disables best-effort de-duplication, which allows for higher throughput.
func (i *Item) Save() (map[string]bigquery.Value, string, error) {
	return map[string]bigquery.Value{
		"full_name": i.Name,
		"age":       i.Age,
	}, bigquery.NoDedupeID, nil
}

// insertRows demonstrates inserting data into a table using the streaming insert mechanism.
func insertRows(projectID, datasetID, tableID string) error {
	// projectID := "my-project-id"
	// datasetID := "mydataset"
	// tableID := "mytable"
	ctx := context.Background()
	client, err := bigquery.NewClient(ctx, projectID)
	if err != nil {
		return fmt.Errorf("bigquery.NewClient: %w", err)
	}
	defer client.Close()

	inserter := client.Dataset(datasetID).Table(tableID).Inserter()
	items := []*Item{
		// Item implements the ValueSaver interface.
		{Name: "Phred Phlyntstone", Age: 32},
		{Name: "Wylma Phlyntstone", Age: 29},
	}
	if err := inserter.Put(ctx, items); err != nil {
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
import com.google.cloud.bigquery.BigQueryError;
import com.google.cloud.bigquery.BigQueryException;
import com.google.cloud.bigquery.BigQueryOptions;
import com.google.cloud.bigquery.InsertAllRequest;
import com.google.cloud.bigquery.InsertAllResponse;
import com.google.cloud.bigquery.TableId;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

// Sample to inserting rows into a table without running a load job.
public class TableInsertRows {

  public static void main(String[] args) {
    // TODO(developer): Replace these variables before running the sample.
    String datasetName = "MY_DATASET_NAME";
    String tableName = "MY_TABLE_NAME";
    // Create a row to insert
    Map<String, Object> rowContent = new HashMap<>();
    rowContent.put("booleanField", true);
    rowContent.put("numericField", "3.14");
    // TODO(developer): Replace the row id with a unique value for each row.
    String rowId = "ROW_ID";
    tableInsertRows(datasetName, tableName, rowId, rowContent);
  }

  public static void tableInsertRows(
      String datasetName, String tableName, String rowId, Map<String, Object> rowContent) {
    try {
      // Initialize client that will be used to send requests. This client only needs to be created
      // once, and can be reused for multiple requests.
      BigQuery bigquery = BigQueryOptions.getDefaultInstance().getService();

      // Get table
      TableId tableId = TableId.of(datasetName, tableName);

      // Inserts rowContent into datasetName:tableId.
      InsertAllResponse response =
          bigquery.insertAll(
              InsertAllRequest.newBuilder(tableId)
                  // More rows can be added in the same RPC by invoking .addRow() on the builder.
                  // You can omit the unique row ids to disable de-duplication.
                  .addRow(rowId, rowContent)
                  .build());

      if (response.hasErrors()) {
        // If any of the insertions failed, this lets you inspect the errors
        for (Map.Entry<Long, List<BigQueryError>> entry : response.getInsertErrors().entrySet()) {
          System.out.println("Response error: \n" + entry.getValue());
        }
      }
      System.out.println("Rows successfully inserted into table");
    } catch (BigQueryException e) {
      System.out.println("Insert operation not performed \n" + e.toString());
    }
  }
}
```

### Node.js

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Node.js 設定說明操作。詳情請參閱 [BigQuery Node.js API 參考說明文件](https://googleapis.dev/nodejs/bigquery/latest/index.html)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
// Import the Google Cloud client library
const {BigQuery} = require('@google-cloud/bigquery');
const bigquery = new BigQuery();

async function insertRowsAsStream() {
  // Inserts the JSON objects into my_dataset:my_table.

  /**
   * TODO(developer): Uncomment the following lines before running the sample.
   */
  // const datasetId = 'my_dataset';
  // const tableId = 'my_table';
  const rows = [
    {name: 'Tom', age: 30},
    {name: 'Jane', age: 32},
  ];

  // Insert data into a table
  await bigquery.dataset(datasetId).table(tableId).insert(rows);
  console.log(`Inserted ${rows.length} rows`);
}
```

### PHP

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 PHP 設定說明操作。詳情請參閱 [BigQuery PHP API 參考說明文件](https://docs.cloud.google.com/php/docs/reference/cloud-bigquery/latest/BigQueryClient?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
use Google\Cloud\BigQuery\BigQueryClient;

/**
 * Stream data into bigquery
 *
 * @param string $projectId The project Id of your Google Cloud Project.
 * @param string $datasetId The BigQuery dataset ID.
 * @param string $tableId The BigQuery table ID.
 * @param string $data Json encoded data For eg,
 *    $data = json_encode([
 *       "field1" => "value1",
 *       "field2" => "value2",
 *    ]);
 */
function stream_row(
    string $projectId,
    string $datasetId,
    string $tableId,
    string $data
): void {
    // instantiate the bigquery table service
    $bigQuery = new BigQueryClient([
      'projectId' => $projectId,
    ]);
    $dataset = $bigQuery->dataset($datasetId);
    $table = $dataset->table($tableId);

    $data = json_decode($data, true);
    $insertResponse = $table->insertRows([
      ['data' => $data],
      // additional rows can go here
    ]);
    if ($insertResponse->isSuccessful()) {
        print('Data streamed into BigQuery successfully' . PHP_EOL);
    } else {
        foreach ($insertResponse->failedRows() as $row) {
            foreach ($row['errors'] as $error) {
                printf('%s: %s' . PHP_EOL, $error['reason'], $error['message']);
            }
        }
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

# TODO(developer): Set table_id to the ID of table to append to.
# table_id = "your-project.your_dataset.your_table"

rows_to_insert = [
    {"full_name": "Phred Phlyntstone", "age": 32},
    {"full_name": "Wylma Phlyntstone", "age": 29},
]

errors = client.insert_rows_json(table_id, rows_to_insert)  # Make an API request.
if errors == []:
    print("New rows have been added.")
else:
    print("Encountered errors while inserting rows: {}".format(errors))
```

### Ruby

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Ruby 設定說明操作。詳情請參閱 [BigQuery Ruby API 參考說明文件](https://googleapis.dev/ruby/google-cloud-bigquery/latest/Google/Cloud/Bigquery.html)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
require "google/cloud/bigquery"

def table_insert_rows dataset_id = "your_dataset_id", table_id = "your_table_id"
  bigquery = Google::Cloud::Bigquery.new
  dataset  = bigquery.dataset dataset_id
  table    = dataset.table table_id

  row_data = [
    { name: "Alice", value: 5  },
    { name: "Bob",   value: 10 }
  ]
  response = table.insert row_data

  if response.success?
    puts "Inserted rows successfully"
  else
    puts "Failed to insert #{response.error_rows.count} rows"
  end
end
```

**注意：** 如要在資料列中指定 `NUMERIC` 或 `BIGNUMERIC` 值，必須使用雙引號括住該值，例如 `"big_numeric_col":"0.123456789123"`。

插入資料列時，不需要在 `insertID` 欄位中填入資料。
以下範例說明如何避免在串流時為每個資料列傳送 `insertID`。

### Java

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Java 設定說明操作。詳情請參閱 [BigQuery Java API 參考說明文件](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/overview?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import com.google.cloud.bigquery.BigQuery;
import com.google.cloud.bigquery.BigQueryError;
import com.google.cloud.bigquery.BigQueryException;
import com.google.cloud.bigquery.BigQueryOptions;
import com.google.cloud.bigquery.InsertAllRequest;
import com.google.cloud.bigquery.InsertAllResponse;
import com.google.cloud.bigquery.TableId;
import com.google.common.collect.ImmutableList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

// Sample to insert rows without row ids in a table
public class TableInsertRowsWithoutRowIds {

  public static void main(String[] args) {
    // TODO(developer): Replace these variables before running the sample.
    String datasetName = "MY_DATASET_NAME";
    String tableName = "MY_TABLE_NAME";
    tableInsertRowsWithoutRowIds(datasetName, tableName);
  }

  public static void tableInsertRowsWithoutRowIds(String datasetName, String tableName) {
    try {
      // Initialize client that will be used to send requests. This client only needs to be created
      // once, and can be reused for multiple requests.
      final BigQuery bigquery = BigQueryOptions.getDefaultInstance().getService();
      // Create rows to insert
      Map<String, Object> rowContent1 = new HashMap<>();
      rowContent1.put("stringField", "Phred Phlyntstone");
      rowContent1.put("numericField", 32);
      Map<String, Object> rowContent2 = new HashMap<>();
      rowContent2.put("stringField", "Wylma Phlyntstone");
      rowContent2.put("numericField", 29);
      InsertAllResponse response =
          bigquery.insertAll(
              InsertAllRequest.newBuilder(TableId.of(datasetName, tableName))
                  // No row ids disable de-duplication, and also disable the retries in the Java
                  // library.
                  .setRows(
                      ImmutableList.of(
                          InsertAllRequest.RowToInsert.of(rowContent1),
                          InsertAllRequest.RowToInsert.of(rowContent2)))
                  .build());

      if (response.hasErrors()) {
        // If any of the insertions failed, this lets you inspect the errors
        for (Map.Entry<Long, List<BigQueryError>> entry : response.getInsertErrors().entrySet()) {
          System.out.println("Response error: \n" + entry.getValue());
        }
      }
      System.out.println("Rows successfully inserted into table without row ids");
    } catch (BigQueryException e) {
      System.out.println("Insert operation not performed \n" + e.toString());
    }
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

# TODO(developer): Set table_id to the ID of table to append to.
# table_id = "your-project.your_dataset.your_table"

rows_to_insert = [
    {"full_name": "Phred Phlyntstone", "age": 32},
    {"full_name": "Wylma Phlyntstone", "age": 29},
]

errors = client.insert_rows_json(
    table_id, rows_to_insert, row_ids=[None] * len(rows_to_insert)
)  # Make an API request.
if errors == []:
    print("New rows have been added.")
else:
    print("Encountered errors while inserting rows: {}".format(errors))
```

### 傳送日期和時間資料

如果是日期和時間欄位，請在 `tabledata.insertAll` 方法中將資料格式化，如下所示：

| 類型 | 格式 |
| --- | --- |
| `DATE` | 採用 `"YYYY-MM-DD"` |
| `DATETIME` | 採用 `"YYYY-MM-DD [HH:MM:SS]"` |
| `TIME` | 採用 `"HH:MM:SS"` |
| `TIMESTAMP` | 自 1970 年 1 月 1 日 (Unix 紀元) 起算的秒數，或 `"YYYY-MM-DD HH:MM[:SS]"` 格式的字串 |

### 傳送範圍資料

如為 `RANGE<T>` 類型的欄位，請在 `tabledata.insertAll` 方法中將資料格式設為 JSON 物件，並包含 `start` 和 `end` 兩個欄位。`start` 和 `end` 欄位缺少值或值為 NULL，代表無界限。
這些欄位必須採用相同的支援 JSON 格式 (類型為 `T`)，其中 `T` 可以是 `DATE`、`DATETIME` 和 `TIMESTAMP` 其中之一。

在下列範例中，`f_range_date` 欄位代表資料表中的 `RANGE<DATE>` 資料欄。使用 `tabledata.insertAll` API，即可在這個資料欄中插入資料列。

```
{
    "f_range_date": {
        "start": "1970-01-02",
        "end": null
    }
}
```

## 串流資料可用性

BigQuery 成功確認 `tabledata.insertAll` 要求後，您就能立即使用 [GoogleSQL](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql?hl=zh-tw) 查詢，即時分析資料。如果您使用以量計價的運算價格，查詢串流緩衝區中的資料時，系統不會針對串流緩衝區處理的位元組收費。如果採用以容量為準的定價方式，[預留項目](https://docs.cloud.google.com/bigquery/docs/reservations-workload-management?hl=zh-tw)會耗用運算單元，處理串流緩衝區中的資料。

最近以串流方式傳入擷取時間分區資料表的資料列，在 [`_PARTITIONTIME`](https://docs.cloud.google.com/bigquery/docs/querying-partitioned-tables?hl=zh-tw#query_an_ingestion-time_partitioned_table) 虛擬資料欄的值暫時為 NULL。對於這類資料列，BigQuery 會在背景中指派 `PARTITIONTIME` 欄的最終非空值，通常會在幾分鐘內完成。在極少數情況下，這項作業最多可能需要 90 分鐘。

最近串流的資料列可能無法複製到表格，通常會持續幾分鐘。在極少數情況下，這項作業最多可能需要 90 分鐘。如要查看資料表副本是否有資料，請檢查 `tables.get` 回應中名為 [`streamingBuffer`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables?hl=zh-tw#streamingbuffer) 的區段。如果缺少 `streamingBuffer` 部分，則代表您的資料處於可複製的狀態。您也可以使用 `streamingBuffer.oldestEntryTime` 欄位，識別串流緩衝區中的記錄存續時間。

## 盡可能清除重複

為插入的資料列提供 `insertId` 時，BigQuery 會使用這個 ID，盡可能地在最多一分鐘內清除重複資料。也就是說，如果您在該時間範圍內，將同一個資料列和同一個 `insertId` 多次串流至同一個資料表，BigQuery *可能*會刪除該資料列的重複項目，只保留其中一個。

系統會預期具有相同 `insertId` 的資料列也相同。如果兩列的 `insertId` 相同，BigQuery 會保留哪一列則不確定。

一般來說，重複資料刪除功能適用於分散式系統中的重試情境，因為在某些錯誤情況下 (例如系統與 BigQuery 之間的網路發生錯誤，或是 BigQuery 發生內部錯誤)，無法確定串流資料即時插入作業的狀態。如果重試插入作業，請對同一組資料列使用相同的 `insertId`，BigQuery 就會嘗試刪除重複資料。詳情請參閱「[排解串流資料插入的相關問題](#troubleshooting)」一節。

BigQuery 提供的重複資料刪除功能會盡力執行，但不應做為確保資料中沒有重複項目的機制。此外，為確保資料的可靠性和可用性，BigQuery 可能隨時降低盡量去重複的品質。

如果您對資料有嚴格的重複資料刪除要求，可改為使用支援[交易作業](https://docs.cloud.google.com/datastore/docs/concepts/transactions?hl=zh-tw)的 [Google Cloud Datastore](https://docs.cloud.google.com/datastore?hl=zh-tw) 服務。

### 停用盡可能清除重複的功能

您可以透過不在每個插入的資料列中填入 `insertId` 欄位來停用盡可能清除重複的功能。建議使用這個方法插入資料。

#### Apache Beam 和 Dataflow

如要使用 Apache Beam 的 [BigQuery I/O 連接器](https://beam.apache.org/documentation/io/built-in/google-bigquery) (適用於 Java) 時停用盡量去重複功能，請使用 [`ignoreInsertIds()` 方法](https://beam.apache.org/releases/javadoc/current/org/apache/beam/sdk/io/gcp/bigquery/BigQueryIO.Write.html)。

### 手動移除重複內容

為確保串流完成後沒有重複的資料列，請使用下列手動程序：

1. 在資料表結構定義中加入 `insertId` 做為資料欄，並在每列資料中加入 `insertId` 值。
2. 在串流作業停止後，執行下列查詢以檢查是否有重複內容：

   ```
   #standardSQL
   SELECT
     MAX(count) FROM(
     SELECT
       ID_COLUMN,
       count(*) as count
     FROM
       `TABLE_NAME`
     GROUP BY
       ID_COLUMN)
   ```

   假如結果大於 1，表示有重複的項目。
3. 如要移除重複項目，請執行下列查詢。指定目的地資料表、允許大型結果，並停用結果扁平化。

   ```
   #standardSQL
   SELECT
     * EXCEPT(row_number)
   FROM (
     SELECT
       *,
       ROW_NUMBER()
             OVER (PARTITION BY ID_COLUMN) row_number
     FROM
       `TABLE_NAME`)
   WHERE
     row_number = 1
   ```

關於移除重複項目的查詢，請注意以下事項：

* 保守的重複項目移除查詢策略是指定一份新資料表，也可以指定包含 `WRITE_TRUNCATE` 寫入配置的來源資料表。
* 重複項目移除查詢會將 `row_number` 資料欄 (包含 `1` 這個值) 加到資料表結構定義尾端。這項查詢使用 [GoogleSQL](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql?hl=zh-tw) 的 [`SELECT * EXCEPT`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax?hl=zh-tw#select_except) 陳述式，從目的地資料表中排除 `row_number` 資料欄。`#standardSQL` 前置字串會為此查詢[啟用](https://docs.cloud.google.com/bigquery/docs/introduction-sql?hl=zh-tw) GoogleSQL。此外，您也可以選取特定的資料欄名稱來略過此資料欄。
* 如要在移除重複項目後查詢即時資料，您也可以使用重複項目移除查詢來對資料表建立資料檢視。請注意，資料檢視的查詢成本是根據在資料檢視中選取的資料欄計算，這可能會導致位元組掃描大小過大。

## 以串流方式將資料傳入時間分區資料表

以串流方式將資料傳入時間分區資料表時，每個分區都會有一個串流緩衝區。如將 `writeDisposition` 屬性設為 `WRITE_TRUNCATE`，當您在執行會覆寫分區的載入、查詢或複製工作時，系統會保留串流緩衝區。如要移除串流緩衝區，請對分區呼叫 [`tables.get`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables/get?hl=zh-tw)，確認串流緩衝區是空的。

### 依擷取時間分區

將資料串流至擷取時間分區資料表時，BigQuery 會根據目前的 UTC 時間推斷目的地分區。

新抵達的資料會暫時置於 `__UNPARTITIONED__` 分區，並位於串流緩衝區。未分區資料累積到足夠的量以後，BigQuery 就會將資料分區到正確的分區。不過，資料移出 `__UNPARTITIONED__` 分區所需的時間沒有服務水準協議。查詢可以使用虛擬資料欄 ([`_PARTITIONTIME` 或 `_PARTITIONDATE`](https://docs.cloud.google.com/bigquery/docs/querying-partitioned-tables?hl=zh-tw#query_an_ingestion-time_partitioned_table)，視您偏好的資料類型而定) 從 `__UNPARTITIONED__` 分區篩選出 `NULL` 值，藉此從查詢中排除串流緩衝區的資料。

如果以串流方式將資料傳入每日分區資料表，您可以提供分區修飾符做為 `insertAll` 要求的一部分，藉此覆寫日期推斷結果。在 `tableId` 參數中加入修飾符。舉例來說，您可以使用分區修飾符，將資料串流至資料表 `table1` 中對應 2021-03-01 的分區：

```
table1$20210301
```

使用分區修飾符以串流方式傳輸資料時，可以根據目前的世界標準時間，以串流方式將資料傳輸至過去 31 天和未來 16 天之間 (相對於目前日期) 的分區。如要針對前述允許範圍外的日期寫入分區，請改用載入或查詢工作，如[附加並覆寫分區資料表資料](https://docs.cloud.google.com/bigquery/docs/managing-partitioned-table-data?hl=zh-tw#append-overwrite)一文所述。

使用分區修飾符以串流方式傳送資料時，僅支援每日分區資料表。不支援按小時、月或年分區的資料表。

如要進行測試，可以使用 bq 指令列工具 [`bq insert`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_insert) CLI 指令。例如，以下指令會將單一列以串流方式傳入 `mydataset.mytable` 分區資料表中日期為 2017 年 1 月 1 日 (`$20170101`) 的分區：

```
echo '{"a":1, "b":2}' | bq insert 'mydataset.mytable$20170101'
```

**注意：** `bq insert` 指令僅供測試。

### 按時間單位資料欄分區

您可以將資料串流至依 `DATE`、`DATETIME` 或 `TIMESTAMP` 資料欄分區的資料表，但這些資料欄的值必須介於過去 10 年和未來 1 年之間。超出這個範圍的資料會遭到拒絕。

資料進行串流時，一開始會放在 `__UNPARTITIONED__` 分區中。未分區資料累積到足夠的量以後，BigQuery 就會自動重新分區資料，將資料放入適當的分區。不過，資料移出 `__UNPARTITIONED__` 分區所需的時間並無服務水準協議。

* 注意：系統處理每日分區的方式，與每小時、每月和每年分區不同。只有超出日期範圍 (過去 7 天至未來 3 天) 的資料會擷取至 UNPARTITIONED 分區，等待重新分區。另一方面，如果是以小時為單位的分區資料表，資料一律會擷取至 UNPARTITIONED 分區，之後再重新分區。

## 使用範本資料表自動建立資料表

*範本資料表*提供一種機制，可將邏輯資料表分成許多較小的資料表，以便建立較小的資料集 (例如，透過使用者 ID)。範本表格有下列限制。建議改用[分區資料表](https://docs.cloud.google.com/bigquery/docs/partitioned-tables?hl=zh-tw)和[分群資料表](https://docs.cloud.google.com/bigquery/docs/clustered-tables?hl=zh-tw)來達成這個行為。

如要透過 BigQuery API 使用範本資料表，請將 `templateSuffix` 參數新增到 `insertAll` 要求。如果是 bq 指令列工具，請在 `insert` 指令中加入 `template_suffix` 旗標。假如 BigQuery 偵測到 `templateSuffix`
參數或 `template_suffix` 標記，就會將指定資料表視為基礎範本。並建立一份結構定義與指定資料表相同的新資料表，而且該資料表具有包含指定後置字元的名稱：

```
<targeted_table_name> + <templateSuffix>
```

只要使用範本資料表，您就可以省去個別建立資料表以及為每個資料表指定結構定義的負擔。您只需要建立一個範本，並提供不同的後置字元，BigQuery 就能為您建立新資料表。BigQuery 會將資料表放在同一個專案和資料集中。

使用範本資料表建立的資料表通常會在幾秒內顯示。
在極少數情況下，可能需要較長時間才能使用。

### 變更範本資料表結構定義

如果您變更範本資料表結構定義，後續產生的所有資料表都會使用更新後的結構定義。先前產生的資料表不會受到影響，除非現有資料表仍有串流緩衝區。

就仍有串流緩衝區的現有資料表而言，假如您以回溯相容的方式修改範本資料表結構定義，主動串流產生的資料表結構定義也會隨之更新。不過，如果您以非回溯相容的方式修改範本資料表結構定義，使用舊結構定義的所有緩衝資料都將會遺失。此外，如果已產生的現有資料表使用現已不相容的舊結構定義，您就無法將新資料串流傳入表內。

變更範本資料表結構定義後，請等待變更傳播完成，再嘗試插入新資料或查詢產生的資料表。插入新欄位的要求應該會在幾分鐘內成功，而查詢新欄位的嘗試可能需要最多 90 分鐘。

假如您想變更已產生資料表的結構定義，請等到透過範本資料表進行的串流作業停止，且已產生資料表的串流統計資料區塊已不存在 `tables.get()` 回應中 (表示資料表已沒有緩衝資料)，否則請勿變更結構定義。

[分區資料表](https://docs.cloud.google.com/bigquery/docs/partitioned-tables?hl=zh-tw)和[叢集資料表](https://docs.cloud.google.com/bigquery/docs/clustered-tables?hl=zh-tw)不受上述限制影響，建議使用這兩種機制。

### 範本資料表詳細資料

範本後置值
:   `templateSuffix` (或 `--template_suffix`) 值只能包含英文字母 (a-z、A-Z)、數字 (0-9) 或底線 (\_)。資料表名稱和資料表尾碼的總長度上限為 1024 個字元。

配額
:   範本資料表受[串流配額](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#streaming_inserts)限制。專案每秒最多可使用範本表格建立 10 個表格，與 [`tables.insert`](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#tables.insert_calls_per_second) API 類似。這項配額僅適用於正在建立的資料表，不適用於正在修改的資料表。
:   如果應用程式每秒需要建立超過 10 個資料表，建議使用[叢集資料表](https://docs.cloud.google.com/bigquery/docs/clustered-tables?hl=zh-tw)。
    舉例來說，您可以將高基數資料表 ID 放入單一叢集資料表的主鍵欄。

存留時間 (TTL)
:   已產生的資料表會沿用資料集的到期時間。已產生的資料表跟一般的串流資料一樣，無法立即複製。

簡化
:   系統只會針對目的地資料表的相同參照內容刪除重複資料。舉例來說，如果您同時使用範本資料表和一般 `insertAll` 指令，將資料串流至產生的資料表，系統不會對範本資料表和一般 `insertAll` 指令插入的資料列執行重複資料刪除作業。

瀏覽次數
:   範本資料表和產生的資料表不得設為檢視畫面。

## 排解串流資料插入問題

接下來的幾個小節將討論，如何排解您[使用舊版 Streaming API 將資料串流到 BigQuery 中](https://docs.cloud.google.com/bigquery/docs/streaming-data-into-bigquery?hl=zh-tw)時所發生的錯誤。如要進一步瞭解如何解決串流資料即時插入的配額錯誤，請參閱「[串流資料即時插入配額錯誤](https://docs.cloud.google.com/bigquery/docs/troubleshoot-quotas?hl=zh-tw#ts-streaming-insert-quota)」。

### 失敗的 HTTP 回應代碼

如果您收到失敗的 HTTP 回應代碼 (例如網路錯誤)，就無法判斷串流資料即時插入作業是否成功。如果您嘗試重新傳送要求，可能會導致資料表中出現重複的資料列。為防止資料表出現重複的內容，請在傳送要求時設定 `insertId` 屬性。BigQuery 會利用 `insertId` 屬性來清除重複的內容。

如果您收到權限錯誤、資料表名稱無效的錯誤，或是超過配額的錯誤，代表系統沒有插入任何資料列，且整個要求都執行失敗。

### 成功的 HTTP 回應代碼

即使您收到[成功的 HTTP 回應代碼](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tabledata/insertAll?hl=zh-tw#response-body)，您還是需要檢查回應的 `insertErrors` 屬性，判斷資料列的插入作業是否已執行成功，因為 BigQuery 有可能只成功插入了部分資料列。您可能會遇到下列其中一種情況：

* **所有資料列都已成功插入。**如果 `insertErrors` 屬性是空白清單，代表所有資料列都已成功插入。
* **部分資料列已成功插入。**除了發生有任何資料列中結構定義不相符的情況之外，在 `insertErrors` 屬性中列出的資料列都沒有插入資料表，而所有其他的資料列都已成功插入。`errors` 屬性會針對每個插入失敗的資料列，提供失敗的詳細原因。`index` 屬性會針對發生該錯誤的要求，提供從 0 開始的資料列索引。
* **未成功插入任何資料列。**如果 BigQuery 在處理要求中個別的資料列時碰到結構定義不相符的情況，就不會插入任何資料列，並針對每個資料列傳回 `insertErrors` 項目，即使結構定義沒有不相符的資料列也算在內。沒有結構定義不相符的資料列會有 `reason` 屬性設定為 `stopped` 的錯誤，且可讓您照原樣重新傳送。而失敗的資料列會包含關於結構定義不相符的詳細資訊。如要瞭解各個 BigQuery 資料類型支援的通訊協定緩衝區類型，請參閱「[支援的通訊協定緩衝區和 Arrow 資料類型](https://docs.cloud.google.com/bigquery/docs/supported-data-types?hl=zh-tw)」。

### 串流資料插入的中繼資料錯誤

由於 BigQuery 的串流 API 是針對高插入率所設計，因此對基礎資料表中繼資料所做的修改最終會在與串流系統互動時保持一致。在大多數情況下，中繼資料變更會在幾分鐘內生效，但 API 回應在這段期間可能會反映出不一致的資料表狀態。

部分情況包括：

* **結構定義變更**。如果最近有串流資料插入資料表，修改該資料表的結構定義可能會導致回應出現結構定義不相符的錯誤，因為串流系統可能無法立即反映出結構定義的變更。
* **建立/刪除表格**。串流至不存在的資料表會傳回 `notFound` 回應的變化類型。而後續的串流資料插入作業，可能無法立刻辨識出在回應中建立資料表的動作。同樣地，刪除或重新建立資料表時，串流資料插入可能會在一段時間內傳送至舊資料表。新資料表可能不會包含串流插入內容。
* **資料表截斷**。截斷資料表的資料 (例如查詢工作會使用 WRITE\_TRUNCATE 的 writeDisposition 時)，可能會導致後續插入的一致性出現落差。

### 遺失/無法取得資料

串流插入作業會暫時存放在寫入最佳化儲存空間，這類儲存空間的可用性特徵與代管儲存空間不同。BigQuery 中的某些作業不會與寫入最佳化儲存空間互動，例如資料表複製工作和 `tabledata.list` 等 API 方法。近期的串流資料不會出現在目的地資料表或輸出內容中。

### 串流資料即時插入配額錯誤

本節提供相關提示，協助您排解以串流方式將資料傳入 BigQuery 時發生的配額錯誤。

在特定區域中，如果您並未在每個資料列的 `insertId` 欄位中填入資料，則串流資料插入會含有較高的配額。如要進一步瞭解串流資料插入的配額，請參閱[串流資料插入](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#streaming_inserts)。BigQuery 串流的配額相關錯誤取決於 `insertId` 是否存在。

**錯誤訊息**

如果 `insertId` 欄位為空白，則可能會發生下列配額錯誤：

| 配額限制 | 錯誤訊息 |
| --- | --- |
| 每項專案每秒位元組數 | 在區域 REGION 中專案 PROJECT\_ID gaia\_id 為 GAIA\_ID 的實體超過每秒插入位元組數的配額。 |

如果在 `insertId` 欄位填入資料，則可能會發生下列配額錯誤：

| 配額限制 | 錯誤訊息 |
| --- | --- |
| 每項專案每秒資料列數量 | 您在 REGION 的專案 PROJECT\_ID 超過每秒串流資料插入資料列的配額。 |
| 每個資料表每秒資料列數量 | 您的資料表 TABLE\_ID 超出每秒串流資料即時插入資料列的配額。 |
| 每個資料表每秒位元組數 | 您的資料表 TABLE\_ID 超出每秒串流資料即時插入位元組數的配額。 |

`insertId` 欄位的用途是簡化插入的資料列。如果同一個 `insertId` 的多個插入項目均於幾分鐘之內抵達，則 BigQuery 會寫入單一版本的記錄。但是，我們無法保證系統會自動刪除重複的內容。為了達到最大的串流總處理量，建議您不要加入 `insertId`，改成[手動刪除重複內容](https://docs.cloud.google.com/bigquery/docs/streaming-data-into-bigquery?hl=zh-tw#manually_removing_duplicates)。詳情請參閱[確保資料一致性](https://docs.cloud.google.com/bigquery/docs/streaming-data-into-bigquery?hl=zh-tw#dataconsistency)一文。

如果遇到這項錯誤，請[診斷問題](#ts-streaming-insert-quota-diagnose)，然後[按照建議步驟](#ts-streaming-insert-quota-resolution)解決問題。

#### 診斷

使用 [`STREAMING_TIMELINE_BY_*`](https://docs.cloud.google.com/bigquery/docs/information-schema-streaming?hl=zh-tw) 檢視表來分析串流流量。這些檢視表會每隔一分鐘匯總串流統計資料，並依 `error_code` 分類。結果中會顯示配額錯誤，且 `error_code` 等於 `RATE_LIMIT_EXCEEDED` 或 `QUOTA_EXCEEDED`。

根據已達到的特定配額上限查看 `total_rows` 或 `total_input_bytes`。如果錯誤是資料表層級的配額，請依 `table_id` 進行篩選。

舉例來說，下列查詢顯示每分鐘擷取的位元組總數和配額錯誤總數：

```
SELECT
 start_timestamp,
 error_code,
 SUM(total_input_bytes) as sum_input_bytes,
 SUM(IF(error_code IN ('QUOTA_EXCEEDED', 'RATE_LIMIT_EXCEEDED'),
     total_requests, 0)) AS quota_error
FROM
 `region-REGION_NAME`.INFORMATION_SCHEMA.STREAMING_TIMELINE_BY_PROJECT
WHERE
  start_timestamp > TIMESTAMP_SUB(CURRENT_TIMESTAMP, INTERVAL 1 DAY)
GROUP BY
 start_timestamp,
 error_code
ORDER BY 1 DESC
```

#### 解析度

如要解決這項配額錯誤，請按照下列步驟操作：

* 如果您使用 `insertId` 欄位來刪除重複的內容，而您的專案位於支援較高串流配額的區域，則建議移除 `insertId` 欄位。這個解決方案可能需要執行一些其他步驟，以手動方式刪除重複的資料內容。詳情請參閱[手動移除重複內容](https://docs.cloud.google.com/bigquery/docs/streaming-data-into-bigquery?hl=zh-tw#manually_removing_duplicates)。
* 如果您並非使用 `insertId`，或是無法加以移除，請監控 24 小時內的串流流量，並分析配額錯誤：

  + 如果您看到的大多是 `RATE_LIMIT_EXCEEDED` 錯誤而不是 `QUOTA_EXCEEDED` 錯誤，而您的整體流量低於配額的 80%，則這些錯誤可能表示流量暫時暴增。您可以在每次重試之間使用指數輪詢重試作業，以處理這些錯誤。
  + 如果您使用 Dataflow 工作插入資料，請考慮使用載入工作，而非串流插入。詳情請參閱「[設定插入方法](https://beam.apache.org/documentation/io/built-in/google-bigquery/#setting-the-insertion-method)」。如果您使用 Dataflow 和自訂 I/O 連接器，請考慮改用內建 I/O 連接器。詳情請參閱「[自訂 I/O 模式](https://beam.apache.org/documentation/patterns/custom-io/)」。
  + 如果您看到 `QUOTA_EXCEEDED` 錯誤，或整體流量持續超過配額的 80%，請提交增加配額的要求。詳情請參閱「[要求調整配額](https://docs.cloud.google.com/docs/quotas/help/request_increase?hl=zh-tw)」。
  + 您也可以考慮使用較新的 [Storage Write API](https://docs.cloud.google.com/bigquery/docs/write-api?hl=zh-tw) 取代串流插入作業，因為這項 API 的輸送量較高、價格較低，而且提供許多實用功能。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-16 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-16 (世界標準時間)。"],[],[]]