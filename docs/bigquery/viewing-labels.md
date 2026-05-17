Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 查看標籤

本頁面說明如何查看在 BigQuery 資源上的標籤。

您可以透過下列方式查看標籤：

* 使用 Google Cloud 控制台
* 查詢 `INFORMATION_SCHEMA` 檢視畫面
* 使用 bq 指令列工具的 `bq show` 指令
* 呼叫 [`datasets.get`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/datasets/get?hl=zh-tw) 或 [`tables.get`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables/get?hl=zh-tw) API 方法
* 使用用戶端程式庫

由於系統會將檢視表當做資料表資源處理，因此可以使用 `tables.get` 方法來取得檢視表和資料表的標籤資訊。

## 事前準備

授予身分與存取權管理 (IAM) 角色，讓使用者取得執行本文各項工作所需的權限。

### 所需權限

查看標籤所需的權限取決於可存取的資源類型。如要執行本文中的工作，您需要下列權限。

#### 查看資料集詳細資料的權限

如要查看資料集詳細資料，您需要 `bigquery.datasets.get` IAM 權限。

下列預先定義的 IAM 角色都具備查看資料集詳細資料所需的權限：

* `roles/bigquery.user`
* `roles/bigquery.metadataViewer`
* `roles/bigquery.dataViewer`
* `roles/bigquery.dataOwner`
* `roles/bigquery.dataEditor`
* `roles/bigquery.admin`

此外，如果您具備 `bigquery.datasets.create` 權限，可以查看您建立的資料集詳細資料。

如要進一步瞭解 BigQuery 中的 IAM 角色和權限，請參閱[預先定義的角色與權限](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)一文。

#### 查看資料表或檢視表詳細資料的權限

如要查看資料表或檢視表詳細資料，必須具備 `bigquery.tables.get` IAM 權限。

所有預先定義的 IAM 角色都具備查看表格或詳細資料所需的權限，但 `roles/bigquery.user` 和 `roles/bigquery.jobUser` **除外**。

此外，如果您具備 `bigquery.datasets.create` 權限，可以查看所建立資料集中的資料表和檢視表詳細資料。

如要進一步瞭解 BigQuery 中的 IAM 角色和權限，請參閱[預先定義的角色與權限](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)一文。

#### 查看工作詳細資料的權限

如要查看工作詳細資料，您需要 `bigquery.jobs.get` IAM 權限。

下列每個預先定義的 IAM 角色都包含查看工作詳細資料所需的權限：

* `roles/bigquery.admin` (可查看專案中所有工作的詳細資料)
* `roles/bigquery.user` (可查看工作詳細資料)
* `roles/bigquery.jobUser` (可查看工作詳細資料)

如要進一步瞭解 BigQuery 中的 IAM 角色和權限，請參閱[預先定義的角色與權限](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)一文。

## 查看資料集、資料表和檢視表標籤

如要查看資源的標籤，請選取下列其中一個選項：

### 控制台

1. 如果是資料集，「Dataset Details」(資料集詳細資料) 頁面會自動開啟；如果是資料表和檢視表，請按一下 [Details] (詳細資料) 以開啟詳細資料頁面。標籤資訊會顯示在資源的資訊資料表中。

### SQL

查詢[`INFORMATION_SCHEMA.SCHEMATA_OPTIONS`檢視區塊](https://docs.cloud.google.com/bigquery/docs/information-schema-datasets?hl=zh-tw#schemata_options_view)，即可查看資料集標籤；查詢[`INFORMATION_SCHEMA.TABLE_OPTIONS`檢視區塊](https://docs.cloud.google.com/bigquery/docs/information-schema-table-options?hl=zh-tw)，即可查看資料表標籤。舉例來說，下列 SQL 查詢會傳回名為 `mydataset` 的資料集標籤：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列陳述式：

   ```
   SELECT
     *
   FROM
     INFORMATION_SCHEMA.SCHEMATA_OPTIONS
   WHERE
     schema_name = 'mydataset'
     AND option_name = 'labels';
   ```
3. 按一下「執行」play\_circle。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

### bq

使用 `bq show` 指令並加入資源 ID。`--format` 旗標可用來控制輸出格式。如果資源位於預設專案以外的專案中，請使用下列格式加入專案 ID：`[PROJECT_ID]:[DATASET]`。為了便於閱讀，可以透過將 `--format` 旗標設為 `pretty` 來控制輸出格式。

```
bq show --format=pretty [RESOURCE_ID]
```

其中 `[RESOURCE_ID]` 是有效的資料集、資料表、檢視表或工作 ID。

範例：

輸入下列指令來顯示預設專案中 `mydataset` 的標籤。

```
bq show --format=pretty mydataset
```

輸出內容如下：

```
+-----------------+--------------------------------------------------------+---------------------+
|  Last modified  |                          ACLs                          |       Labels        |
+-----------------+--------------------------------------------------------+---------------------+
| 11 Jul 19:34:34 | Owners:                                                | department:shipping |
|                 |   projectOwners,                                       |                     |
|                 | Writers:                                               |                     |
|                 |   projectWriters                                       |                     |
|                 | Readers:                                               |                     |
|                 |   projectReaders                                       |                     |
+-----------------+--------------------------------------------------------+---------------------+
```

輸入下列指令來顯示 `mydataset.mytable` 的標籤。`mydataset` 在 `myotherproject` 中，而不是您的預設專案中。

```
bq show --format=pretty myotherproject:mydataset.mytable
```

分群資料表的輸出內容如下：

```
+-----------------+------------------------------+------------+-------------+-----------------+------------------------------------------------+------------------+---------+
|  Last modified  |            Schema            | Total Rows | Total Bytes |   Expiration    |               Time Partitioning                | Clustered Fields | Labels  |
+-----------------+------------------------------+------------+-------------+-----------------+------------------------------------------------+------------------+---------+
| 25 Jun 19:28:14 | |- timestamp: timestamp      | 0          | 0           | 25 Jul 19:28:14 | DAY (field: timestamp, expirationMs: 86400000) | customer_id      | org:dev |
|                 | |- customer_id: string       |            |             |                 |                                                |                  |         |
|                 | |- transaction_amount: float |            |             |                 |                                                |                  |         |
+-----------------+------------------------------+------------+-------------+-----------------+------------------------------------------------+------------------+---------+
```

### API

呼叫 [`datasets.get`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/datasets/get?hl=zh-tw) 方法或 [`tables.get`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables/get?hl=zh-tw) 方法。回應包含與這項資源相關聯的所有標籤。

或者，您也可以使用 [`datasets.list`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/datasets/list?hl=zh-tw) 來查看多個資料集的標籤，或使用 [`tables.list`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables/list?hl=zh-tw) 來查看多個資料表和檢視表的標籤。

由於系統會將檢視表當做資料表資源處理，因此可以使用 `tables.get` 和 `tables.list` 方法來查看檢視表和資料表的標籤資訊。

### Go

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Go 設定說明操作。詳情請參閱 [BigQuery Go API 參考說明文件](https://godoc.org/cloud.google.com/go/bigquery)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import (
	"context"
	"fmt"
	"io"

	"cloud.google.com/go/bigquery"
)

// printDatasetLabels retrieves label metadata from a dataset and prints it to an io.Writer.
func printDatasetLabels(w io.Writer, projectID, datasetID string) error {
	// projectID := "my-project-id"
	// datasetID := "mydataset"
	ctx := context.Background()

	client, err := bigquery.NewClient(ctx, projectID)
	if err != nil {
		return fmt.Errorf("bigquery.NewClient: %v", err)
	}
	defer client.Close()

	meta, err := client.Dataset(datasetID).Metadata(ctx)
	if err != nil {
		return err
	}
	fmt.Fprintf(w, "Dataset %s labels:\n", datasetID)
	if len(meta.Labels) == 0 {
		fmt.Fprintln(w, "Dataset has no labels defined.")
		return nil
	}
	for k, v := range meta.Labels {
		fmt.Fprintf(w, "\t%s:%s\n", k, v)
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
import com.google.cloud.bigquery.Dataset;

// Sample to get dataset labels
public class GetDatasetLabels {

  public static void runGetDatasetLabels() {
    // TODO(developer): Replace these variables before running the sample.
    String datasetName = "MY_DATASET_NAME";
    getDatasetLabels(datasetName);
  }

  public static void getDatasetLabels(String datasetName) {
    try {
      // Initialize client that will be used to send requests. This client only needs to be created
      // once, and can be reused for multiple requests.
      BigQuery bigquery = BigQueryOptions.getDefaultInstance().getService();

      Dataset dataset = bigquery.getDataset(datasetName);
      dataset
          .getLabels()
          .forEach((key, value) -> System.out.println("Retrieved labels successfully"));
    } catch (BigQueryException e) {
      System.out.println("Label was not found. \n" + e.toString());
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

async function getDatasetLabels() {
  // Gets labels on a dataset.

  /**
   * TODO(developer): Uncomment the following lines before running the sample.
   */
  // const datasetId = "my_dataset";

  // Retrieve current dataset metadata.
  const dataset = bigquery.dataset(datasetId);
  const [metadata] = await dataset.getMetadata();
  const labels = metadata.labels;

  console.log(`${datasetId} Labels:`);
  for (const [key, value] of Object.entries(labels)) {
    console.log(`${key}: ${value}`);
  }
}
getDatasetLabels();
```

### Python

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Python 設定說明操作。詳情請參閱 [BigQuery Python API 參考說明文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
from google.cloud import bigquery

# Construct a BigQuery client object.
client = bigquery.Client()

# TODO(developer): Set dataset_id to the ID of the dataset to fetch.
# dataset_id = "your-project.your_dataset"

dataset = client.get_dataset(dataset_id)  # Make an API request.

# View dataset labels.
print("Dataset ID: {}".format(dataset_id))
print("Labels:")
if dataset.labels:
    for label, value in dataset.labels.items():
        print("\t{}: {}".format(label, value))
else:
    print("\tDataset has no labels defined.")
```

## 查看資料表標籤

### Go

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Go 設定說明操作。詳情請參閱 [BigQuery Go API 參考說明文件](https://godoc.org/cloud.google.com/go/bigquery)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import (
	"context"
	"fmt"
	"io"

	"cloud.google.com/go/bigquery"
)

// tableLabels demonstrates fetching metadata from a table and printing the Label metadata to an io.Writer.
func tableLabels(w io.Writer, projectID, datasetID, tableID string) error {
	// projectID := "my-project-id"
	// datasetID := "mydataset"
	// tableID := "mytable"
	ctx := context.Background()
	client, err := bigquery.NewClient(ctx, projectID)
	if err != nil {
		return fmt.Errorf("bigquery.NewClient: %w", err)
	}
	defer client.Close()

	meta, err := client.Dataset(datasetID).Table(tableID).Metadata(ctx)
	if err != nil {
		return err
	}
	fmt.Fprintf(w, "Table %s labels:\n", datasetID)
	if len(meta.Labels) == 0 {
		fmt.Fprintln(w, "Table has no labels defined.")
		return nil
	}
	for k, v := range meta.Labels {
		fmt.Fprintf(w, "\t%s:%s\n", k, v)
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
import com.google.cloud.bigquery.Table;
import com.google.cloud.bigquery.TableId;

// Sample to get table labels
public class GetTableLabels {

  public static void main(String[] args) {
    // TODO(developer): Replace these variables before running the sample.
    String datasetName = "MY_DATASET_NAME";
    String tableName = "MY_TABLE_NAME";
    getTableLabels(datasetName, tableName);
  }

  public static void getTableLabels(String datasetName, String tableName) {
    try {
      // Initialize client that will be used to send requests. This client only needs to be created
      // once, and can be reused for multiple requests.
      BigQuery bigquery = BigQueryOptions.getDefaultInstance().getService();

      // This example table starts with existing label { color: 'green' }
      Table table = bigquery.getTable(TableId.of(datasetName, tableName));
      table
          .getLabels()
          .forEach((key, value) -> System.out.println("Retrieved labels successfully"));
    } catch (BigQueryException e) {
      System.out.println("Label was not deleted. \n" + e.toString());
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

async function getTableLabels() {
  // Gets labels on a dataset.

  /**
   * TODO(developer): Uncomment the following lines before running the sample.
   */
  // const datasetId = "my_dataset";
  // const tableId = "my_table";

  // Retrieve current dataset metadata.
  const table = bigquery.dataset(datasetId).table(tableId);
  const [metadata] = await table.getMetadata();
  const labels = metadata.labels;

  console.log(`${tableId} Labels:`);
  for (const [key, value] of Object.entries(labels)) {
    console.log(`${key}: ${value}`);
  }
}
getTableLabels();
```

### Python

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Python 設定說明操作。詳情請參閱 [BigQuery Python API 參考說明文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
from google.cloud import bigquery

client = bigquery.Client()

# TODO(dev): Change table_id to the full name of the table you want to create.
table_id = "your-project.your_dataset.your_table_name"

table = client.get_table(table_id)  # API Request

# View table labels
print(f"Table ID: {table_id}.")
if table.labels:
    for label, value in table.labels.items():
        print(f"\t{label}: {value}")
else:
    print("\tTable has no labels defined.")
```

## 查看工作標籤

如要查看工作上的標籤，請選取下列其中一個選項：

### SQL

查詢[`INFORMATION_SCHEMA.JOB_BY_*`檢視畫面](https://docs.cloud.google.com/bigquery/docs/information-schema-jobs?hl=zh-tw)，即可查看工作標籤。舉例來說，下列 SQL 查詢會傳回目前專案中，目前使用者提交的工作的查詢文字和標籤：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列陳述式：

   ```
   SELECT
     query,
     labels
   FROM
     INFORMATION_SCHEMA.JOBS_BY_USER;
   ```
3. 按一下「執行」play\_circle。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

### bq

如要使用 bq 指令列工具查看查詢工作的標籤，請輸入 `bq show -j` 指令並加入查詢工作的工作 ID。`--format` 旗標可用來控制輸出格式。例如，如果查詢工作的工作 ID 為 `bqjob_r1234d57f78901_000023746d4q12_1`，請輸入下列指令：

```
bq show -j --format=pretty bqjob_r1234d57f78901_000023746d4q12_1
```

輸出內容應如下所示：

```
+----------+---------+-----------------+----------+-------------------+-----------------+--------------+----------------------+
| Job Type |  State  |   Start Time    | Duration |    User Email     | Bytes Processed | Bytes Billed |        Labels        |
+----------+---------+-----------------+----------+-------------------+-----------------+--------------+----------------------+
| query    | SUCCESS | 03 Dec 15:00:41 | 0:00:00  | email@example.com | 255             | 10485760     | department:shipping  |
|          |         |                 |          |                   |                 |              | costcenter:logistics |
+----------+---------+-----------------+----------+-------------------+-----------------+--------------+----------------------+
```

### API

呼叫 [`jobs.get`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs/get?hl=zh-tw) 方法。回應包含與這項資源相關聯的所有標籤。

## 查看預訂標籤

如要查看預訂項目的標籤，請選取下列其中一個選項：

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在導覽選單中，按一下「容量管理」。
3. 按一下「運算單元預留項目」分頁標籤。
4. 每個預訂的標籤會列在「標籤」欄中。

### SQL

查詢[`INFORMATION_SCHEMA.RESERVATIONS`檢視畫面](https://docs.cloud.google.com/bigquery/docs/information-schema-reservations?hl=zh-tw)，即可查看預訂項目的標籤。舉例來說，下列 SQL 查詢會傳回預訂名稱和標籤：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列陳述式：

   ```
   SELECT
     reservation_name,
     labels
   FROM
     INFORMATION_SCHEMA.RESERVATIONS
   WHERE reservation_name = RESERVATION_NAME;
   ```

   請替換下列項目：

   * `RESERVATION_NAME`：預訂名稱。
3. 按一下「執行」play\_circle。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

### bq

使用 [`bq show`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_show) 指令查看預訂標籤。

```
bq show --format=prettyjson --reservation=true --location=LOCATION RESERVATION_NAME
```

更改下列內容：

* `LOCATION`：預訂地點。
* `RESERVATION_NAME`：預訂名稱。

輸出看起來類似以下內容：

```
{
  "autoscale": {
    "maxSlots": "100"
  },
  "creationTime": "2023-10-26T15:16:28.196940Z",
  "edition": "ENTERPRISE",
  "labels": {
    "department": "shipping"
  },
  "name": "projects/myproject/locations/US/reservations/myreservation",
  "updateTime": "2025-06-05T19:37:28.125914Z"
}
```

## 後續步驟

* 瞭解如何為 BigQuery 資源[加上標籤](https://docs.cloud.google.com/bigquery/docs/adding-labels?hl=zh-tw)。
* 瞭解如何在 BigQuery 資源中[更新標籤](https://docs.cloud.google.com/bigquery/docs/updating-labels?hl=zh-tw)。
* 瞭解如何[使用標籤篩選資源](https://docs.cloud.google.com/bigquery/docs/filtering-labels?hl=zh-tw)。
* 瞭解如何在 BigQuery 資源中[刪除標籤](https://docs.cloud.google.com/bigquery/docs/deleting-labels?hl=zh-tw)。
* 請參閱 Resource Manager 說明文件中的[使用標籤](https://docs.cloud.google.com/resource-manager/docs/using-labels?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-16 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-16 (世界標準時間)。"],[],[]]