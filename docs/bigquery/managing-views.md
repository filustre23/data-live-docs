Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 管理邏輯檢視表

本文件說明如何在 BigQuery 中管理檢視表。您可以透過下列方式管理 BigQuery 檢視表：

* [更新檢視表](#update_a_view)
* [複製檢視表](#copy)
* [重新命名檢視表](#rename_a_view)
* [刪除檢視表](#delete_views)

## 事前準備

授予 Identity and Access Management (IAM) 角色，讓使用者具備執行本文件各項工作所需的權限。執行工作所需的權限 (如有) 會列在工作的「必要權限」部分。

## 更新檢視表

建立檢視表後，您可以更新下列檢視表屬性：

* [SQL 查詢](#update-sql)
* [到期時間](#view-expiration)
* [說明](#update-description)
* [標籤](https://docs.cloud.google.com/bigquery/docs/adding-labels?hl=zh-tw#adding_table_and_view_labels)

### 所需權限

如要更新檢視表，您必須具備下列 IAM 權限：

* `bigquery.tables.update`
* `bigquery.tables.get`

下列每個預先定義的 IAM 角色都包含更新檢視表所需的權限：

* `roles/bigquery.dataEditor`
* `roles/bigquery.dataOwner`
* `roles/bigquery.admin`

此外，如果您具備 `bigquery.datasets.create` 權限，則可更新所建立資料集中的資料表和檢視表。

如要更新檢視表的 SQL 查詢，您也必須具備查詢檢視表 SQL 查詢所參照任何資料表的權限。

**注意：** 如要更新[授權檢視表](https://docs.cloud.google.com/bigquery/docs/authorized-views?hl=zh-tw)的 SQL，或[授權資料集](https://docs.cloud.google.com/bigquery/docs/authorized-datasets?hl=zh-tw)中的檢視表，您必須具備檢視表所在資料集的 `bigquery.datasets.update` 權限。您不需要對檢視表讀取的資料集，或包含參照 UDF 的資料集，具備這項權限。標準和授權檢視表更新檢視表的方法相同，例如 `CREATE OR REPLACE VIEW`。更新檢視表會保留其授權狀態。也就是說，如果檢視表已獲得授權，更新後仍會保持授權狀態；如果檢視表未獲得授權，更新後會產生標準檢視表。詳情請參閱[授權檢視表的必要權限](https://docs.cloud.google.com/bigquery/docs/authorized-views?hl=zh-tw#required_permissions)，以及[授權資料集內檢視表的必要權限](https://docs.cloud.google.com/bigquery/docs/authorized-datasets?hl=zh-tw#permissions_datasets)。

如要進一步瞭解 BigQuery 的 IAM 角色和權限，請參閱「[預先定義的角色和權限](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)」。

#### 範例：參照跨專案 UDF 和資料集的檢視表

假設您要更新*專案 A* (`authorized_dataset`) 中的檢視表。這項檢視表查詢會彙整*專案 B* (`shared_dataset`) 中的資料表，並呼叫*專案 C* (`udf_dataset`) 中的 UDF。

必須具備下列權限：

* *專案 A*：您更新的特定檢視表資源`bigquery.tables.update`。
* *專案 B*：參照共用資源的 `bigquery.datasets.get` 和 `bigquery.tables.getData`。
* *專案 C*：`bigquery.routines.get`，用於您呼叫的特定 UDF。

重要的是，您的身分不需要具備*專案 B* 或*專案 C* 的 `bigquery.datasets.update` 權限，即可執行這項更新。

### 更新檢視表的 SQL 查詢

您可以透過以下方式更新用來定義檢視表的 SQL 查詢：

* 使用 Google Cloud 控制台
* 使用 bq 指令列工具的 `bq update` 指令
* 呼叫 [`tables.patch`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables/patch?hl=zh-tw) API 方法
* 使用用戶端程式庫

您可以在 API 或 bq 指令列工具中，將 SQL 方言從舊版 SQL 變更為 GoogleSQL。您無法在Google Cloud 控制台中，將舊版 SQL 檢視表更新為 GoogleSQL。

如何更新檢視表的 SQL 查詢：

### 控制台

1. 點選左側窗格中的 explore「Explorer」。

   如果沒有看到左側窗格，請按一下 last\_page「Expand left pane」(展開左側窗格)，開啟窗格。
2. 在「Explorer」窗格中展開專案，依序點選「Datasets」(資料集) 和資料集。
3. 依序點選**「總覽」>「表格」**，然後選取檢視畫面。
4. 點按「Details」(詳細資料) 分頁標籤。
5. 按一下「查詢」方塊上方的「編輯查詢」。查詢會在查詢編輯器中開啟。
6. 編輯 SQL 查詢，然後依序點選**「儲存 view」 > 「儲存 view」**：

### bq

發出含有 `--view` 旗標的 `bq update` 指令。如要使用 GoogleSQL，或將查詢方言從舊版 SQL 更新為 GoogleSQL，請加入 `--use_legacy_sql` 旗標並設為 `false`。

如果查詢參照儲存在 Cloud Storage 或本機檔案中的外部 user-defined function 資源，請使用 `--view_udf_resource` 旗標指定這些資源。本文不示範 `--view_udf_resource` 旗標。如要進一步瞭解如何使用 UDF，請參閱「[GoogleSQL user-defined function](https://docs.cloud.google.com/bigquery/docs/user-defined-functions?hl=zh-tw)」。

如果您要更新在預設專案以外的專案中的檢視表，請使用下列格式將專案 ID 新增至資料集名稱：`project_id:dataset`。

```
bq update \
    --use_legacy_sql=false \
    --view_udf_resource=path_to_file \
    --view='query' \
    project_id:dataset.view
```

更改下列內容：

* path\_to\_file：程式碼檔案的 URI 或本機檔案系統路徑，該檔案會立即載入並評估為檢視表使用的 user-defined function 資源。請重複該標記以指定多個檔案。
* query：有效的 GoogleSQL 查詢
* project\_id：專案 ID
* dataset：資料集名稱，內含要更新的檢視表
* view：要更新的檢視表名稱

**範例**

輸入下列指令，更新 `mydataset` 中名為 `myview` 之檢視表的 SQL 查詢。`mydataset` 在您的預設專案中。用於更新檢視表的範例查詢會從美國姓名資料[公開資料集](https://docs.cloud.google.com/bigquery/public-data?hl=zh-tw)查詢資料。

```
bq update \
    --use_legacy_sql=false \
    --view \
    'SELECT
      name,
      number
    FROM
      `bigquery-public-data.usa_names.usa_1910_current`
    WHERE
      gender = "M"
    ORDER BY
      number DESC;' \
    mydataset.myview
```

輸入下列指令，更新 `mydataset` 中名為 `myview` 之檢視表的 SQL 查詢。`mydataset` 在 `myotherproject` 中，而不是您的預設專案中。用於更新檢視表的範例查詢會從美國姓名資料[公開資料集](https://docs.cloud.google.com/bigquery/public-data?hl=zh-tw)查詢資料。

```
bq update \
    --use_legacy_sql=false \
    --view \
    'SELECT
      name,
      number
    FROM
      `bigquery-public-data.usa_names.usa_1910_current`
    WHERE
      gender = "M"
    ORDER BY
      number DESC;' \
    myotherproject:mydataset.myview
```

### API

您可以透過下列方式更新檢視表：使用包含已更新 `view` 屬性的[資料表資源](https://docs.cloud.google.com/bigquery/docs/reference/v2/tables?hl=zh-tw)呼叫 [`tables.patch`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables/patch?hl=zh-tw) 方法。由於 `tables.update` 方法會取代整個資料表資源，因此建議使用 `tables.patch` 方法。

### Go

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Go 設定操作說明進行操作。詳情請參閱 [BigQuery Go API 參考文件](https://godoc.org/cloud.google.com/go/bigquery)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import (
	"context"
	"fmt"

	"cloud.google.com/go/bigquery"
)

// updateView demonstrates updating the query metadata that defines a logical view.
func updateView(projectID, datasetID, viewID string) error {
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

	newMeta := bigquery.TableMetadataToUpdate{
		// This example updates a view into the shakespeare dataset to exclude works named after kings.
		ViewQuery: "SELECT word, word_count, corpus, corpus_date FROM `bigquery-public-data.samples.shakespeare` WHERE corpus NOT LIKE '%king%'",
	}

	if _, err := view.Update(ctx, newMeta, meta.ETag); err != nil {
		return err
	}
	return nil
}
```

### Java

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Java 設定操作說明進行操作。詳情請參閱 [BigQuery Java API 參考文件](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/overview?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import com.google.cloud.bigquery.BigQuery;
import com.google.cloud.bigquery.BigQueryException;
import com.google.cloud.bigquery.BigQueryOptions;
import com.google.cloud.bigquery.TableId;
import com.google.cloud.bigquery.TableInfo;
import com.google.cloud.bigquery.ViewDefinition;

// Sample to update query on a view
public class UpdateViewQuery {

  public static void runUpdateViewQuery() {
    // TODO(developer): Replace these variables before running the sample.
    String datasetName = "MY_DATASET_NAME";
    String tableName = "MY_TABLE_NAME";
    String viewName = "MY_VIEW_NAME";
    String updateQuery =
        String.format("SELECT TimestampField, StringField FROM %s.%s", datasetName, tableName);
    updateViewQuery(datasetName, viewName, updateQuery);
  }

  public static void updateViewQuery(String datasetName, String viewName, String query) {
    try {
      // Initialize client that will be used to send requests. This client only needs to be created
      // once, and can be reused for multiple requests.
      BigQuery bigquery = BigQueryOptions.getDefaultInstance().getService();

      // Retrieve existing view metadata
      TableInfo viewMetadata = bigquery.getTable(TableId.of(datasetName, viewName));

      // Update view query
      ViewDefinition viewDefinition = viewMetadata.getDefinition();
      viewDefinition.toBuilder().setQuery(query).build();

      // Set metadata
      bigquery.update(viewMetadata.toBuilder().setDefinition(viewDefinition).build());

      System.out.println("View query updated successfully");
    } catch (BigQueryException e) {
      System.out.println("View query was not updated. \n" + e.toString());
    }
  }
}
```

### Node.js

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Node.js 設定操作說明進行操作。詳情請參閱 [BigQuery Node.js API 參考文件](https://googleapis.dev/nodejs/bigquery/latest/index.html)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
// Import the Google Cloud client library and create a client
const {BigQuery} = require('@google-cloud/bigquery');
const bigquery = new BigQuery();

async function updateViewQuery() {
  // Updates a view named "my_existing_view" in "my_dataset".

  /**
   * TODO(developer): Uncomment the following lines before running the sample.
   */
  // const datasetId = "my_existing_dataset"
  // const tableId = "my_existing_table"
  const dataset = await bigquery.dataset(datasetId);

  // This example updates a view into the USA names dataset to include state.
  const newViewQuery = `SELECT name, state 
  FROM \`bigquery-public-data.usa_names.usa_1910_current\`
  LIMIT 10`;

  // Retrieve existing view
  const [view] = await dataset.table(tableId).get();

  // Retrieve existing view metadata
  const [metadata] = await view.getMetadata();

  // Update view query
  metadata.view = newViewQuery;

  // Set metadata
  await view.setMetadata(metadata);

  console.log(`View ${tableId} updated.`);
}
```

### Python

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Python 設定操作說明進行操作。詳情請參閱 [BigQuery Python API 參考文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
from google.cloud import bigquery

client = bigquery.Client()

view_id = "my-project.my_dataset.my_view"
source_id = "my-project.my_dataset.my_table"
view = bigquery.Table(view_id)

# The source table in this example is created from a CSV file in Google
# Cloud Storage located at
# `gs://cloud-samples-data/bigquery/us-states/us-states.csv`. It contains
# 50 US states, while the view returns only those states with names
# starting with the letter 'M'.
view.view_query = f"SELECT name, post_abbr FROM `{source_id}` WHERE name LIKE 'M%'"

# Make an API request to update the query property of the view.
view = client.update_table(view, ["view_query"])
print(f"Updated {view.table_type}: {str(view.reference)}")
```

**注意：** 如果您更新[授權檢視表](https://docs.cloud.google.com/bigquery/docs/authorized-views?hl=zh-tw)查詢所參照的資料集，則必須[授權檢視表](https://docs.cloud.google.com/bigquery/docs/authorized-views?hl=zh-tw#manage_users_or_groups_for_authorized_views)存取任何新的基礎資料集。

### 更新視圖的到期時間

您可以設定資料集層級 (會同時影響資料表和視圖) 的資料表預設到期時間，也可以在建立視圖時設定視圖的到期時間。如果您在建立檢視表時設定到期時間，系統將會忽略資料集的資料表預設到期時間。如果您未在資料集層級設定預設資料表到期時間，也未在建立檢視表時設定到期時間，則檢視表永遠不會到期，您必須手動刪除檢視表。

建立檢視表後，您隨時可以透過下列方式更新檢視表的到期時間：

* 使用 Google Cloud 控制台
* 使用以 GoogleSQL 語法編寫的資料定義語言 (DDL) 陳述式
* 使用 bq 指令列工具的 `bq update` 指令
* 呼叫 [`tables.patch`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables/patch?hl=zh-tw) API 方法
* 使用用戶端程式庫

**附註：**如果設定的到期時間已過，系統會立即刪除該檢視表。

如何更新檢視表的到期時間：

### 控制台

1. 點選左側窗格中的 explore「Explorer」。
2. 在「Explorer」窗格中展開專案，依序點選「Datasets」(資料集) 和資料集。
3. 依序點選**「總覽」 > 「資料表」**，然後選取檢視表。
4. 按一下「詳細資料」分頁標籤，然後點選「編輯詳細資料」。
5. 在「Edit detail」(編輯詳細資料) 對話方塊的「Expiration time」(到期時間) 選單中，選取「Specify date」(指定日期)。
6. 在「Expiration time」(到期時間) 欄位中，使用日期挑選器工具選取日期和時間。
7. 按一下 [儲存]。更新後的到期時間會顯示在「View info」(查看資訊) 專區的「View expiration」(查看到期時間) 列中。

### SQL

使用 [`ALTER VIEW SET OPTIONS` DDL 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#alter_view_set_options_statement)：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列陳述式：

   ```
    ALTER VIEW DATASET_ID.MY_VIEW
    SET OPTIONS (
     expiration_timestamp = TIMESTAMP('NEW_TIMESTAMP'));
   ```

   替換下列內容：

   * DATASET\_ID：檢視表所在資料集的 ID
   * MY\_VIEW：要更新的檢視表名稱
   * NEW\_TIMESTAMP：[TIMESTAMP 值](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#timestamp_type)
3. 按一下「play\_circle 執行」。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

### bq

發出含有 `--expiration` 旗標的 `bq update` 指令。如果您要更新在預設專案以外的專案中的檢視表，請使用下列格式將專案 ID 新增至資料集名稱：`project_id:dataset`。

```
bq update \
    --expiration integer \
    project_id:dataset.view
```

更改下列內容：

* integer：資料表的預設生命週期 (以秒為單位)。最小值是 3600 秒 (1 小時)。到期時間為目前時間加整數值。
* project\_id：專案 ID
* dataset：資料集名稱，內含要更新的檢視表
* view：要更新的檢視表名稱

**範例**

輸入下列指令，將 `mydataset` 中的 `myview` 到期時間更新為 5 天 (432000 秒)。`mydataset` 位於您的預設專案中。

```
bq update \
    --expiration 432000 \
    mydataset.myview
```

輸入下列指令，將 `mydataset` 中的 `myview` 到期時間更新為 5 天 (432000 秒)。`mydataset` 在 `myotherproject` 中，而不是您的預設專案中。

```
bq update \
    --expiration 432000 \
    myotherproject:mydataset.myview
```

### API

呼叫 [`tables.patch`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables/patch?hl=zh-tw) 方法並使用[資料表資源](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables?hl=zh-tw)中的 `expirationTime` 屬性。由於 `tables.update` 方法會取代整個資料表資源，因此建議使用 `tables.patch` 方法。使用 REST API 時，檢視表到期時間會以毫秒為單位表示。

### Go

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Go 設定操作說明進行操作。詳情請參閱 [BigQuery Go API 參考文件](https://godoc.org/cloud.google.com/go/bigquery)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import (
	"context"
	"fmt"
	"time"

	"cloud.google.com/go/bigquery"
)

// updateTableExpiration demonstrates setting the table expiration of a table to a specific point in time
// in the future, at which time it will be deleted.
func updateTableExpiration(projectID, datasetID, tableID string) error {
	// projectID := "my-project-id"
	// datasetID := "mydataset"
	// tableID := "mytable"
	ctx := context.Background()
	client, err := bigquery.NewClient(ctx, projectID)
	if err != nil {
		return fmt.Errorf("bigquery.NewClient: %v", err)
	}
	defer client.Close()

	tableRef := client.Dataset(datasetID).Table(tableID)
	meta, err := tableRef.Metadata(ctx)
	if err != nil {
		return err
	}
	update := bigquery.TableMetadataToUpdate{
		ExpirationTime: time.Now().Add(time.Duration(5*24) * time.Hour), // table expiration in 5 days.
	}
	if _, err = tableRef.Update(ctx, update, meta.ETag); err != nil {
		return err
	}
	return nil
}
```

### Java

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Java 設定操作說明進行操作。詳情請參閱 [BigQuery Java API 參考文件](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/overview?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
Table beforeTable = bigquery.getTable(datasetName, tableName);

// Set table to expire 5 days from now.
long expirationMillis = DateTime.now().plusDays(5).getMillis();
TableInfo tableInfo = beforeTable.toBuilder()
        .setExpirationTime(expirationMillis)
        .build();
Table afterTable = bigquery.update(tableInfo);
```

### Node.js

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Node.js 設定操作說明進行操作。詳情請參閱 [BigQuery Node.js API 參考文件](https://googleapis.dev/nodejs/bigquery/latest/index.html)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
// Import the Google Cloud client library
const {BigQuery} = require('@google-cloud/bigquery');
const bigquery = new BigQuery();

async function updateTableExpiration() {
  // Updates a table's expiration.

  /**
   * TODO(developer): Uncomment the following lines before running the sample.
   */
  // const datasetId = 'my_dataset', // Existing dataset
  // const tableId = 'my_table', // Existing table
  // const expirationTime = Date.now() + 1000 * 60 * 60 * 24 * 5 // 5 days from current time in ms

  // Retreive current table metadata
  const table = bigquery.dataset(datasetId).table(tableId);
  const [metadata] = await table.getMetadata();

  // Set new table expiration to 5 days from current time
  metadata.expirationTime = expirationTime.toString();
  const [apiResponse] = await table.setMetadata(metadata);

  const newExpirationTime = apiResponse.expirationTime;
  console.log(`${tableId} expiration: ${newExpirationTime}`);
}
```

### Python

更新檢視表到期時間的程序與更新資料表到期時間相同。

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Python 設定操作說明進行操作。詳情請參閱 [BigQuery Python API 參考文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
from google.cloud import bigquery

client = bigquery.Client()

# TODO(dev): Change table_id to the full name of the table you want to update.
table_id = "your-project.your_dataset.your_table_name"

# TODO(dev): Set table to expire for desired days days from now.
expiration = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(
    days=5
)
table = client.get_table(table_id)  # Make an API request.
table.expires = expiration
table = client.update_table(table, ["expires"])  # API request

print(f"Updated {table_id}, expires {table.expires}.")
```

### 更新視圖的說明

您可以透過以下方式更新檢視表的說明：

* 使用 Google Cloud 控制台
* 使用以 GoogleSQL 語法編寫的資料定義語言 (DDL) 陳述式
* 使用 bq 指令列工具的 `bq update` 指令
* 呼叫 [`tables.patch`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables/patch?hl=zh-tw) API 方法
* 使用用戶端程式庫

如何更新檢視表的說明：

### 控制台

使用 Google Cloud 控制台建立檢視表時，無法新增說明。建立檢視表後，您可以在「Details」(詳細資料) 頁面新增說明。

1. 點選左側窗格中的 explore「Explorer」。
2. 在「Explorer」窗格中展開專案，依序點選「Datasets」(資料集) 和資料集。
3. 依序點選**「總覽」 > 「資料表」**，然後選取檢視表。
4. 點按「Details」(詳細資料) 分頁標籤。
5. 按一下「查看資訊」部分的「編輯詳細資訊」。
6. 在「Edit detail」(編輯詳細資料) 對話方塊的「Description」(說明) 欄位中，輸入新說明或編輯現有說明。
7. 如要儲存新的說明，請按一下「儲存」。

### SQL

使用 [`ALTER VIEW SET OPTIONS` DDL 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#alter_view_set_options_statement)：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列陳述式：

   ```
    ALTER VIEW DATASET_ID.MY_VIEW
    SET OPTIONS (
     description = 'NEW_DESCRIPTION');
   ```

   替換下列內容：

   * DATASET\_ID：檢視表所在資料集的 ID
   * MY\_VIEW：要更新的檢視表名稱
   * NEW\_DESCRIPTION：新檢視表說明
3. 按一下「play\_circle 執行」。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

### bq

發出含有 `--description` 旗標的 `bq update` 指令。如果您要更新在預設專案以外的專案中的檢視表，請使用下列格式將專案 ID 新增至資料集名稱：`[PROJECT_ID]:[DATASET]`。

```
bq update \
    --description "description" \
    project_id:dataset.view
```

更改下列內容：

* description：描述檢視畫面的文字，以引號括住
* project\_id：您的專案 ID。
* dataset：資料集名稱，內含要更新的檢視表
* view：要更新的檢視表名稱

**範例**

輸入下列指令，將 `mydataset` 中的 `myview` 說明變更為 「Description of mydataset」(mydataset 的說明)。`mydataset` 位於您的預設專案中。

```
bq update \
    --description "Description of myview" \
    mydataset.myview
```

輸入下列指令，將 `mydataset` 中的 `myview` 說明變更為 「Description of mydataset」(mydataset 的說明)。`mydataset` 在 `myotherproject` 中，而不是您的預設專案中。

```
bq update \
    --description "Description of myview" \
    myotherproject:mydataset.myview
```

### API

呼叫 [`tables.patch`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables/patch?hl=zh-tw) 方法並使用 `description` 屬性更新[資料表資源](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables?hl=zh-tw)中的檢視表說明。由於 `tables.update` 方法會取代整個資料表資源，因此建議使用 `tables.patch` 方法。

### Go

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Go 設定操作說明進行操作。詳情請參閱 [BigQuery Go API 參考文件](https://godoc.org/cloud.google.com/go/bigquery)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import (
	"context"
	"fmt"

	"cloud.google.com/go/bigquery"
)

// updateTableDescription demonstrates how to fetch a table's metadata and updates the Description metadata.
func updateTableDescription(projectID, datasetID, tableID string) error {
	// projectID := "my-project-id"
	// datasetID := "mydataset"
	// tableID := "mytable"
	ctx := context.Background()
	client, err := bigquery.NewClient(ctx, projectID)
	if err != nil {
		return fmt.Errorf("bigquery.NewClient: %v", err)
	}
	defer client.Close()

	tableRef := client.Dataset(datasetID).Table(tableID)
	meta, err := tableRef.Metadata(ctx)
	if err != nil {
		return err
	}
	update := bigquery.TableMetadataToUpdate{
		Description: "Updated description.",
	}
	if _, err = tableRef.Update(ctx, update, meta.ETag); err != nil {
		return err
	}
	return nil
}
```

### Java

更新檢視表說明的程序與更新資料表說明相同。

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Java 設定操作說明進行操作。詳情請參閱 [BigQuery Java API 參考文件](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/overview?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
// String datasetName = "my_dataset_name";
// String tableName = "my_table_name";
// String newDescription = "new_description";

Table beforeTable = bigquery.getTable(datasetName, tableName);
TableInfo tableInfo = beforeTable.toBuilder()
    .setDescription(newDescription)
    .build();
Table afterTable = bigquery.update(tableInfo);
```

### Node.js

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Node.js 設定操作說明進行操作。詳情請參閱 [BigQuery Node.js API 參考文件](https://googleapis.dev/nodejs/bigquery/latest/index.html)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
// Import the Google Cloud client library
const {BigQuery} = require('@google-cloud/bigquery');
const bigquery = new BigQuery();

async function updateTableDescription() {
  // Updates a table's description.

  // Retreive current table metadata
  const table = bigquery.dataset(datasetId).table(tableId);
  const [metadata] = await table.getMetadata();

  // Set new table description
  const description = 'New table description.';
  metadata.description = description;
  const [apiResponse] = await table.setMetadata(metadata);
  const newDescription = apiResponse.description;

  console.log(`${tableId} description: ${newDescription}`);
}
```

### Python

更新檢視表說明的程序與更新資料表說明相同。

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Python 設定操作說明進行操作。詳情請參閱 [BigQuery Python API 參考文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
# from google.cloud import bigquery
# client = bigquery.Client()
# project = client.project
# dataset_ref = bigquery.DatasetReference(project, dataset_id)
# table_ref = dataset_ref.table('my_table')
# table = client.get_table(table_ref)  # API request

assert table.description == "Original description."
table.description = "Updated description."

table = client.update_table(table, ["description"])  # API request

assert table.description == "Updated description."
```

## 複製檢視表

您可以使用 Google Cloud 控制台複製檢視表。

您無法使用 bq 指令列工具、REST API 或用戶端程式庫複製檢視表，但可以[在目標資料集中複製檢視表](https://docs.cloud.google.com/bigquery/docs/views?hl=zh-tw)。

### 所需權限

如要在 Google Cloud 控制台複製檢視表，您必須具備來源和目的地資料集的 IAM 權限。

* 您必須具備來源資料集的下列權限：

  + `bigquery.tables.get`
  + `bigquery.tables.getData` (必須具備這項權限，才能存取檢視表 SQL 查詢參照的資料表)
* 您必須具備下列目的地資料集權限：

  + `bigquery.tables.create` (可在目的地資料集中建立檢視表副本)

下列各項預先定義的 IAM 角色，都包含複製檢視表所需的權限：

* `roles/bigquery.dataEditor`
* `roles/bigquery.dataOwner`
* `roles/bigquery.admin`

此外，如果您具備 `bigquery.datasets.create` 權限，則可複製您建立的資料集中的檢視表。除非您是目的地資料集的建立者，否則也需要該資料集的存取權。

**注意事項：**複製檢視表不需具備 `bigquery.jobs.create` 權限。複製檢視表時，Google Cloud 控制台不會產生複製工作。

如要進一步瞭解 BigQuery 的 IAM 角色和權限，請參閱「[預先定義的角色和權限](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)」。

### 複製檢視表

如要複製檢視畫面，請按照下列步驟操作：

1. 點選左側窗格中的 explore「Explorer」。
2. 在「Explorer」窗格中展開專案，依序點選「Datasets」(資料集) 和資料集。
3. 依序點選**「總覽」>「資料表」**，然後選取檢視表。
4. 在詳細資料窗格中，按一下「複製」。
5. 在「Copy view」(複製檢視表) 對話方塊中，執行下列操作：

   1. 在「Source」(來源) 區段中，確認專案名稱、資料集名稱和資料表名稱正確無誤。
   2. 在「目的地」部分，執行下列操作：

      * 在「Project」(專案) 部分，選擇要將檢視表複製到哪個專案。
      * 在「Dataset」(資料集) 部分，選擇要包含複製檢視表的資料集。
      * 在「Table」(資料表) 中輸入檢視表名稱。您可以在方塊中輸入新的檢視表名稱，以重新命名檢視表。您輸入的新名稱必須遵循[檢視表命名](https://docs.cloud.google.com/bigquery/docs/views?hl=zh-tw#view_naming)規則。
   3. 按一下「複製」：

複製工作須遵守相關限制。詳情請參閱「[配額與限制](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#copy_jobs)」。

## 重新命名檢視表

只有在使用 Google Cloud 控制台複製檢視表時，才能重新命名檢視表。如要瞭解如何在複製檢視表時重新命名，請參閱「[複製檢視表](#copy)」。

您無法使用 bq 指令列工具、API 或用戶端程式庫變更現有檢視表的名稱。因此，您必須以新名稱[重新建立檢視表](https://docs.cloud.google.com/bigquery/docs/views?hl=zh-tw)。

## 刪除檢視

您可以透過下列方式刪除檢視表：

* 使用 Google Cloud 控制台
* 使用 bq 指令列工具的 `bq rm` 指令
* 呼叫 [`tables.delete`](https://docs.cloud.google.com/bigquery/docs/reference/v2/tables/delete?hl=zh-tw) API 方法

無論使用哪種方法，一次只能刪除一個檢視表。

如要在指定時段過後自動刪除檢視表，請設定資料集層級的預設[到期時間](https://docs.cloud.google.com/bigquery/docs/updating-datasets?hl=zh-tw#table-expiration)，或者在[建立檢視表](https://docs.cloud.google.com/bigquery/docs/views?hl=zh-tw)時設定到期時間。

刪除[授權檢視表](https://docs.cloud.google.com/bigquery/docs/authorized-views?hl=zh-tw)後，可能需要 24 小時，才會從來源資料集的*授權檢視表*清單中移除。

**注意：** 檢視畫面刪除後即無法復原。如果重新建立的授權檢視表與刪除的檢視表同名，您必須將新的檢視表新增至來源資料集的*授權檢視表*清單。

刪除檢視表也會一併刪除與該檢視表相關聯的所有權限。重新建立已刪除的檢視表時，您也必須手動[重新設定先前與其相關聯的所有存取權限](https://docs.cloud.google.com/bigquery/docs/control-access-to-resources-iam?hl=zh-tw)。

**注意：**您無法直接復原檢視表，但可以搜尋對應的[稽核記錄活動](https://docs.cloud.google.com/bigquery/docs/introduction-audit-workloads?hl=zh-tw)，復原檢視表建立陳述式。

* 如要瞭解如何使用 Logs Explorer，依稽核記錄名稱查詢活動記錄，請參閱「[稽核記錄總覽](https://docs.cloud.google.com/logging/docs/audit?hl=zh-tw)」。
* 如要瞭解如何使用 `projects/PROJECT_ID/logs/cloudaudit.googleapis.com%2Factivity`，請參閱「[BigQuery 資料政策稽核記錄](https://docs.cloud.google.com/bigquery/docs/column-data-masking-audit-logging?hl=zh-tw)」。

### 所需權限

如要刪除檢視表，您必須具備下列 IAM 權限：

* `bigquery.tables.delete`

下列預先定義的 IAM 角色，都具備刪除檢視表所需的權限：

* `roles/bigquery.dataOwner`
* `roles/bigquery.dataEditor`
* `roles/bigquery.admin`

此外，如果您具備 `bigquery.datasets.create` 權限，則可刪除您建立的資料集中的檢視表。

如要進一步瞭解 BigQuery 的 IAM 角色和權限，請參閱「[預先定義的角色和權限](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)」。

### 刪除檢視表

如何刪除視圖：

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中展開專案，依序點選「Datasets」(資料集) 和資料集。
4. 依序點選**「總覽」 > 「資料表」**，然後點選檢視表。
5. 在詳細資料窗格中，按一下「Delete」(刪除)。
6. 在對話方塊中輸入 `"delete"`，然後點選「刪除」確認。

### SQL

使用 [`DROP VIEW` DDL 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#drop_view_statement)：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列陳述式：

   ```
   DROP VIEW mydataset.myview;
   ```

   替換下列內容：

   * DATASET\_ID：檢視表所在資料集的 ID
   * MY\_VIEW：要更新的檢視表名稱
   * NEW\_DESCRIPTION：新檢視表說明
3. 按一下「play\_circle 執行」。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

### bq

請使用 `bq rm` 指令，搭配 `--table` 旗標 (或 `-t` 捷徑) 來刪除檢視表。使用 bq 指令列工具移除檢視表時，必須確認這項操作。您可以使用 `--force` 旗標 (或 `-f` 捷徑) 來略過確認程序。

如果檢視表位於非預設專案中的資料集裡，請使用下列格式將專案 ID 新增至資料集名稱：`project_id:dataset`。

```
bq rm \
-f \
-t \
project_id:dataset.view
```

其中：

* project\_id 是您的專案 ID。
* dataset 是包含該資料表之資料集的名稱。
* view 是您要刪除的視圖名稱。

範例：

您可以使用 bq 指令列工具執行 `bq` 指令。

在 Google Cloud 控制台中啟用 **Cloud Shell**。

[啟用 Cloud Shell](https://console.cloud.google.com/bigquery?cloudshell=true&hl=zh-tw)

輸入下列指令從 `mydataset` 刪除 `myview`。`mydataset` 在您的預設專案中。

```
bq rm -t mydataset.myview
```

輸入下列指令從 `mydataset` 刪除 `myview`。`mydataset` 在 `myotherproject` 中，而不是您的預設專案中。

```
bq rm -t myotherproject:mydataset.myview
```

輸入下列指令從 `mydataset` 刪除 `myview`。`mydataset` 在您的預設專案中。這個指令使用 `-f` 捷徑略過確認程序。

```
bq rm -f -t mydataset.myview
```

**注意：** 您可以輸入 [`bq ls dataset`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_ls) 指令，確認檢視表已從資料集移除。

### API

呼叫 [`tables.delete`](https://docs.cloud.google.com/bigquery/docs/reference/v2/tables/delete?hl=zh-tw) API 方法並使用`tableId` 參數指定要刪除的檢視表。

### C#

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 C# 設定操作說明進行操作。詳情請參閱 [BigQuery C# API 參考文件](https://docs.cloud.google.com/dotnet/docs/reference/Google.Cloud.BigQuery.V2/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
using Google.Cloud.BigQuery.V2;
using System;

public class BigQueryDeleteTable
{
    public void DeleteTable(
        string projectId = "your-project-id",
        string datasetId = "your_dataset_id",
        string tableId = "your_table_id"
    )
    {
        BigQueryClient client = BigQueryClient.Create(projectId);
        client.DeleteTable(datasetId, tableId);
        Console.WriteLine($"Table {tableId} deleted.");
    }
}
```

### Go

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Go 設定操作說明進行操作。詳情請參閱 [BigQuery Go API 參考文件](https://godoc.org/cloud.google.com/go/bigquery)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import (
	"context"
	"fmt"

	"cloud.google.com/go/bigquery"
)

// deleteTable demonstrates deletion of a BigQuery table.
func deleteTable(projectID, datasetID, tableID string) error {
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
	if err := table.Delete(ctx); err != nil {
		return err
	}
	return nil
}
```

### Java

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Java 設定操作說明進行操作。詳情請參閱 [BigQuery Java API 參考文件](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/overview?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
TableId tableId = TableId.of(projectId, datasetName, tableName);
boolean deleted = bigquery.delete(tableId);
if (deleted) {
  // the table was deleted
} else {
  // the table was not found
}
```

### Node.js

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Node.js 設定操作說明進行操作。詳情請參閱 [BigQuery Node.js API 參考文件](https://googleapis.dev/nodejs/bigquery/latest/index.html)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
// Import the Google Cloud client library
const {BigQuery} = require('@google-cloud/bigquery');
const bigquery = new BigQuery();

async function deleteTable() {
  // Deletes "my_table" from "my_dataset".

  /**
   * TODO(developer): Uncomment the following lines before running the sample.
   */
  // const datasetId = "my_dataset";
  // const tableId = "my_table";

  // Delete the table
  await bigquery
    .dataset(datasetId)
    .table(tableId)
    .delete();

  console.log(`Table ${tableId} deleted.`);
}
```

### PHP

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 PHP 設定操作說明進行操作。詳情請參閱 [BigQuery PHP API 參考文件](https://docs.cloud.google.com/php/docs/reference/cloud-bigquery/latest/BigQueryClient?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
use Google\Cloud\BigQuery\BigQueryClient;

/** Uncomment and populate these variables in your code */
// $projectId = 'The Google project ID';
// $datasetId = 'The BigQuery dataset ID';
// $tableId = 'The BigQuery table ID';

$bigQuery = new BigQueryClient([
    'projectId' => $projectId,
]);
$dataset = $bigQuery->dataset($datasetId);
$table = $dataset->table($tableId);
$table->delete();
printf('Deleted table %s.%s' . PHP_EOL, $datasetId, $tableId);
```

### Python

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Python 設定操作說明進行操作。詳情請參閱 [BigQuery Python API 參考文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
from google.cloud import bigquery

# Construct a BigQuery client object.
client = bigquery.Client()

# TODO(developer): Set table_id to the ID of the table to fetch.
# table_id = 'your-project.your_dataset.your_table'

# If the table does not exist, delete_table raises
# google.api_core.exceptions.NotFound unless not_found_ok is True.
client.delete_table(table_id, not_found_ok=True)  # Make an API request.
print("Deleted table '{}'.".format(table_id))
```

### Ruby

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Ruby 設定操作說明進行操作。詳情請參閱 [BigQuery Ruby API 參考文件](https://googleapis.dev/ruby/google-cloud-bigquery/latest/Google/Cloud/Bigquery.html)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
require "google/cloud/bigquery"

def delete_table dataset_id = "my_dataset_id", table_id = "my_table_id"
  bigquery = Google::Cloud::Bigquery.new
  dataset  = bigquery.dataset dataset_id
  table    = dataset.table table_id

  table.delete

  puts "Table #{table_id} deleted."
end
```

## 還原檢視畫面

您無法直接還原已刪除的檢視表，但某些情況下有替代方案：

* 如果檢視表因父項資料集遭刪除而刪除，您可以[取消刪除資料集](https://docs.cloud.google.com/bigquery/docs/restore-deleted-datasets?hl=zh-tw)，以擷取檢視表。
* 如果檢視表已明確刪除，您可以使用上次建立或更新檢視表時所用的查詢，[重新建立檢視表](https://docs.cloud.google.com/bigquery/docs/views?hl=zh-tw)。您可以在[記錄](https://docs.cloud.google.com/bigquery/docs/reference/auditlogs/rest/Shared.Types/BigQueryAuditMetadata?hl=zh-tw#BigQueryAuditMetadata.TableViewDefinition)中找到檢視表建立或更新作業的查詢定義。

## 查看安全性

如要控管 BigQuery 檢視表的存取權，請參閱「[授權檢視表](https://docs.cloud.google.com/bigquery/docs/authorized-views?hl=zh-tw)」。

## 後續步驟

* 如要瞭解如何建立檢視表，請參閱「[建立檢視表](https://docs.cloud.google.com/bigquery/docs/views?hl=zh-tw)」。
* 如要瞭解如何建立授權檢視表，請參閱[建立授權檢視表](https://docs.cloud.google.com/bigquery/docs/authorized-views?hl=zh-tw)。
* 如要瞭解如何取得檢視表中繼資料，請參閱「[取得檢視表相關資訊](https://docs.cloud.google.com/bigquery/docs/view-metadata?hl=zh-tw)」。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-10-29 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-10-29 (世界標準時間)。"],[],[]]