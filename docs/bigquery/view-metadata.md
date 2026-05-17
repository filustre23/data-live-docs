Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 取得檢視表的相關資訊

本文說明如何在 BigQuery 中列出檢視區塊、取得相關資訊，以及查看中繼資料。

## 事前準備

授予身分與存取權管理 (IAM) 角色，讓使用者取得執行本文各項工作所需的權限。

## 清單檢視表

列出檢視表的方法和列出資料表相同。

### 所需權限

如要列出資料集中的檢視表，您需要 `bigquery.tables.list` IAM 權限。

下列每個預先定義的 IAM 角色都包含在資料集中列出檢視區塊所需的權限：

* `roles/bigquery.user`
* `roles/bigquery.metadataViewer`
* `roles/bigquery.dataViewer`
* `roles/bigquery.dataOwner`
* `roles/bigquery.dataEditor`
* `roles/bigquery.admin`

如要進一步瞭解 BigQuery 中的 IAM 角色和權限，請參閱[預先定義的角色與權限](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)一文。

### 列出資料集中的檢視表

如何列出資料集中的檢視表：

### 控制台

1. 點選左側窗格中的 explore「Explorer」。

   如果沒有看到左側窗格，請按一下 last\_page「Expand left pane」(展開左側窗格)，開啟窗格。
2. 在「Explorer」窗格中展開專案，按一下「Datasets」(資料集)，然後選取資料集。
3. 依序點選「總覽」**>「表格」**。捲動清單，即可查看資料集中的檢視區塊。資料表和檢視表會分別以**類型**資料欄中的值呈現。

### SQL

使用
[`INFORMATION_SCHEMA.VIEWS` 檢視畫面](https://docs.cloud.google.com/bigquery/docs/information-schema-views?hl=zh-tw)：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列陳述式：

   ```
   SELECT table_name
   FROM DATASET_ID.INFORMATION_SCHEMA.VIEWS;
   ```

   將 `DATASET_ID` 替換為資料集名稱。
3. 按一下「執行」play\_circle。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

### bq

請發出 `bq ls` 指令。`--format` 旗標可用來控制輸出內容。如果您要列出非預設專案中的檢視表，請採用下列格式將專案 ID 新增至資料集：`project_id:dataset`。

```
bq ls --format=pretty project_id:dataset
```

其中：

* project\_id 是您的專案 ID。
* dataset 是資料集名稱。

執行指令時，`Type` 欄位會顯示 `TABLE` 或 `VIEW`，例如：

```
+-------------------------+-------+----------------------+-------------------+
|         tableId         | Type  |        Labels        | Time Partitioning |
+-------------------------+-------+----------------------+-------------------+
| mytable                 | TABLE | department:shipping  |                   |
| myview                  | VIEW  |                      |                   |
+-------------------------+-------+----------------------+-------------------+
```

範例：

只要輸入下列指令，即可列出預設專案中 `mydataset` 資料集的檢視表。

```
bq ls --format=pretty mydataset
```

只要輸入下列指令，即可列出 `myotherproject` 中 `mydataset` 資料集的檢視表。

```
bq ls --format=pretty myotherproject:mydataset
```

### API

如要使用 API 列出檢視表，請呼叫 [`tables.list`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables/list?hl=zh-tw) 方法。

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

// listTables demonstrates iterating through the collection of tables in a given dataset.
func listTables(w io.Writer, projectID, datasetID string) error {
	// projectID := "my-project-id"
	// datasetID := "mydataset"
	// tableID := "mytable"
	ctx := context.Background()
	client, err := bigquery.NewClient(ctx, projectID)
	if err != nil {
		return fmt.Errorf("bigquery.NewClient: %v", err)
	}
	defer client.Close()

	ts := client.Dataset(datasetID).Tables(ctx)
	for {
		t, err := ts.Next()
		if err == iterator.Done {
			break
		}
		if err != nil {
			return err
		}
		fmt.Fprintf(w, "Table: %q\n", t.TableID)
	}
	return nil
}
```

### Python

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Python 設定說明操作。詳情請參閱 [BigQuery Python API 參考說明文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
from google.cloud import bigquery

# Construct a BigQuery client object.
client = bigquery.Client()

# TODO(developer): Set dataset_id to the ID of the dataset that contains
#                  the tables you are listing.
# dataset_id = 'your-project.your_dataset'

tables = client.list_tables(dataset_id)  # Make an API request.

print("Tables contained in '{}':".format(dataset_id))
for table in tables:
    print("{}.{}.{}".format(table.project, table.dataset_id, table.table_id))
```

## 取得檢視表的相關資訊

取得檢視表相關資訊的方法和取得資料表資訊相同。

### 所需權限

如要取得檢視區塊的相關資訊，您需要 `bigquery.tables.get` IAM 權限。

下列每個預先定義的 IAM 角色都包含您取得檢視區塊資訊所需的權限：

* `roles/bigquery.metadataViewer`
* `roles/bigquery.dataViewer`
* `roles/bigquery.dataOwner`
* `roles/bigquery.dataEditor`
* `roles/bigquery.admin`

此外，如果您具備 `bigquery.datasets.create` 權限，就能取得您所建立資料集中的檢視表資訊。

如要進一步瞭解 BigQuery 中的 IAM 角色和權限，請參閱[預先定義的角色與權限](https://docs.cloud.google.com/bigquery/access-control?hl=zh-tw)一文。

如何取得資料檢視的相關資訊：

### 控制台

1. 點選左側窗格中的 explore「Explorer」。
2. 在「Explorer」窗格中展開專案，按一下「Datasets」(資料集)，然後選取資料集。
3. 依序點選「總覽」**>「表格」**。捲動清單，即可查看資料集中的檢視區塊。資料表和檢視表會分別以**類型**資料欄中的值呈現。
4. 按一下「Details」(詳細資料) 分頁標籤，查看檢視表的說明、相關資訊，以及定義該檢視表的 SQL 查詢。

### SQL

查詢
[`INFORMATION_SCHEMA.VIEWS` 檢視區塊](https://docs.cloud.google.com/bigquery/docs/information-schema-views?hl=zh-tw)。
下列範例擷取了所有資料欄，但保留 `check_option` 以供未來使用。系統傳回的是預設專案中 DATASET\_ID 內所有檢視表的中繼資料：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列陳述式：

   ```
     SELECT
       * EXCEPT (check_option)
     FROM
       DATASET_ID.INFORMATION_SCHEMA.VIEWS;
   ```

   將 `DATASET_ID` 替換為資料集名稱。
3. 按一下「執行」play\_circle。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

### bq

請發出 `bq show` 指令。`--format` 旗標可用來控管輸出。如果您要取得預設專案以外的專案檢視表相關資訊，請使用下列格式將專案 ID 新增至資料集：`[PROJECT_ID]:[DATASET]`。

```
bq show \
--format=prettyjson \
project_id:dataset.view
```

其中：

* project\_id 是您的專案 ID。
* dataset 是資料集名稱。
* view 是視圖的名稱。

範例：

輸入下列指令，系統即會顯示您預設專案中 `mydataset` 資料集中的 `myview` 相關資訊。

```
bq show --format=prettyjson mydataset.myview
```

輸入下列指令，系統即會顯示 `myotherproject` 中 `mydataset` 資料集中的 `myview` 相關資訊。

```
bq show --format=prettyjson myotherproject:mydataset.myview
```

### API

呼叫 [`tables.get`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables/get?hl=zh-tw) 方法，並提供所有相關參數。

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

// getView demonstrates fetching the metadata from a BigQuery logical view and printing it to an io.Writer.
func getView(w io.Writer, projectID, datasetID, viewID string) error {
	// projectID := "my-project-id"
	// datasetID := "mydataset"
	// viewID := "myview"
	ctx := context.Background()
	client, err := bigquery.NewClient(ctx, projectID)
	if err != nil {
		return fmt.Errorf("bigquery.NewClient: %v", err)
	}
	defer client.Close()

	view := client.Dataset(datasetID).Table(viewID)
	meta, err := view.Metadata(ctx)
	if err != nil {
		return err
	}
	fmt.Fprintf(w, "View %s, query: %s\n", view.FullyQualifiedName(), meta.ViewQuery)
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

// Sample to get a view
public class GetView {

  public static void main(String[] args) {
    // TODO(developer): Replace these variables before running the sample.
    String datasetName = "MY_DATASET_NAME";
    String viewName = "MY_VIEW_NAME";
    getView(datasetName, viewName);
  }

  public static void getView(String datasetName, String viewName) {
    try {
      // Initialize client that will be used to send requests. This client only needs to be created
      // once, and can be reused for multiple requests.
      BigQuery bigquery = BigQueryOptions.getDefaultInstance().getService();

      TableId tableId = TableId.of(datasetName, viewName);
      Table view = bigquery.getTable(tableId);
      System.out.println("View retrieved successfully" + view.getDescription());
    } catch (BigQueryException e) {
      System.out.println("View not retrieved. \n" + e.toString());
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

async function getView() {
  // Retrieves view properties.

  /**
   * TODO(developer): Uncomment the following lines before running the sample
   */
  // const datasetId = "my_dataset";
  // const tableId = "my_view";

  // Retrieve view
  const dataset = bigquery.dataset(datasetId);
  const [view] = await dataset.table(tableId).get();

  const fullTableId = view.metadata.id;
  const viewQuery = view.metadata.view.query;

  // Display view properties
  console.log(`View at ${fullTableId}`);
  console.log(`View query: ${viewQuery}`);
}
getView();
```

### Python

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Python 設定說明操作。詳情請參閱 [BigQuery Python API 參考說明文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
from google.cloud import bigquery

client = bigquery.Client()

view_id = "my-project.my_dataset.my_view"
# Make an API request to get the table resource.
view = client.get_table(view_id)

# Display view properties
print(f"Retrieved {view.table_type}: {str(view.reference)}")
print(f"View Query:\n{view.view_query}")
```

## 查看安全性

如要控管 BigQuery 中檢視區塊的存取權，請參閱「[授權檢視區塊](https://docs.cloud.google.com/bigquery/docs/authorized-views?hl=zh-tw)」。

## 後續步驟

* 如要瞭解如何建立檢視表，請參閱[建立檢視表](https://docs.cloud.google.com/bigquery/docs/views?hl=zh-tw)一文。
* 如要瞭解如何建立授權檢視表，請參閱[建立授權檢視表](https://docs.cloud.google.com/bigquery/docs/authorized-views?hl=zh-tw)。
* 如要瞭解管理檢視表的詳情，請參閱[管理檢視表](https://docs.cloud.google.com/bigquery/docs/managing-views?hl=zh-tw)一文。
* 如要查看 `INFORMATION_SCHEMA` 的總覽，請前往 [BigQuery `INFORMATION_SCHEMA` 簡介](https://docs.cloud.google.com/bigquery/docs/information-schema-intro?hl=zh-tw)頁面。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-16 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-16 (世界標準時間)。"],[],[]]