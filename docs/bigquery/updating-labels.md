Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 更新標籤

本頁面說明如何為 BigQuery 資源更新標籤。

## 事前準備

授予身分與存取權管理 (IAM) 角色，讓使用者擁有執行本文件各項工作所需的權限。執行工作所需的權限 (如有) 會列在工作「必要權限」部分。

## 更新資料集標籤

資料集標籤的更新方式如下：

* 使用 Google Cloud 控制台
* 使用 SQL [DDL 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw)
* 使用 bq 指令列工具的 `bq update` 指令
* 呼叫 [`datasets.patch`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/datasets/patch?hl=zh-tw) API 方法
* 使用用戶端程式庫

### 所需權限

如要更新資料集標籤，必須具備 `bigquery.datasets.update` IAM 權限。

下列預先定義的 IAM 角色都包含更新資料集標籤所需的權限：

* `roles/bigquery.dataOwner`
* `roles/bigquery.admin`

此外，如果您具備 `bigquery.datasets.create` 權限，可以更新所建立資料集的標籤。

如要進一步瞭解 BigQuery 中的 IAM 角色和權限，請參閱[預先定義的角色與權限](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)一文。

### 更新資料集標籤

如要在資料集中更新標籤，請選取下列其中一個選項：

### 控制台

1. 在 Google Cloud 控制台中選取資料集。
2. 在「Dataset Details」(資料集詳細資料) 頁面中，按一下「Labels」(標籤) 右側的鉛筆圖示。
3. 在「Edit labels」(編輯標籤) 對話方塊中：

   * 如要套用其他標籤，請按一下 [Add Label] (新增標籤)。每個資料集中的每個鍵都只能使用一次，但您可以在同一項專案的不同資料集中使用同一個鍵。
   * 修改現有的鍵或值以更新標籤。
   * 按一下 [Update] (更新)，儲存您所做的變更。

### SQL

使用 [`ALTER SCHEMA SET OPTIONS` DDL 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#alter_schema_set_options_statement)，在現有資料集上設定標籤。設定標籤會覆寫資料集上的所有現有標籤。以下範例會在資料集 `mydataset` 上設定單一標籤：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列陳述式：

   ```
   ALTER SCHEMA mydataset
   SET OPTIONS (labels = [('sensitivity', 'high')]);
   ```
3. 按一下「執行」play\_circle。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

### bq

如要加入其他標籤或更新資料集標籤，請發出 `bq update` 指令並搭配使用 `set_label` 旗標。重複使用這個旗標即可加入或更新多個標籤。

如果資料集位於預設專案以外的專案中，請使用下列格式將專案 ID 新增至資料集：`[PROJECT_ID]:[DATASET]`。

```
bq update \
--set_label key:value \
project_id:dataset
```

其中：

* key:value 是您要加入或更新的標籤的鍵/值組合，如果您指定與現有標籤相同的鍵，系統就會更新現有標籤的值。鍵不得重複。
* project\_id 是您的專案 ID。
* dataset 是您要更新的資料集。

範例：

如要更新 `mydataset` 中的 `department` 標籤，請輸入 `bq update` 指令並指定 `department` 做為標籤鍵。例如，如要將 `department:shipping` 標籤更新為 `department:logistics`，請輸入下列指令。`mydataset` 在 `myotherproject` 中，而不是您的預設專案中。

```
    bq update \
    --set_label department:logistics \
    myotherproject:mydataset
```

輸出內容如下所示。

```
Dataset 'myotherproject:mydataset' successfully updated.
```

### API

如要為現有資料集加入其他標籤或更新標籤，請呼叫 [`datasets.patch`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/datasets/patch?hl=zh-tw) 方法，然後加入或更新[資料集資源](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/datasets?hl=zh-tw)的 `labels` 屬性。

由於 `datasets.update` 方法會取代整個資料集資源，因此建議使用 `datasets.patch` 方法。

### Go

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Go 設定說明操作。詳情請參閱 [BigQuery Go API 參考說明文件](https://godoc.org/cloud.google.com/go/bigquery)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import (
	"context"
	"fmt"

	"cloud.google.com/go/bigquery"
)

// addDatasetLabel demonstrates adding label metadata to an existing dataset.
func addDatasetLabel(projectID, datasetID string) error {
	// projectID := "my-project-id"
	// datasetID := "mydataset"
	ctx := context.Background()
	client, err := bigquery.NewClient(ctx, projectID)
	if err != nil {
		return fmt.Errorf("bigquery.NewClient: %v", err)
	}
	defer client.Close()

	ds := client.Dataset(datasetID)
	meta, err := ds.Metadata(ctx)
	if err != nil {
		return err
	}

	update := bigquery.DatasetMetadataToUpdate{}
	update.SetLabel("color", "green")
	if _, err := ds.Update(ctx, update, meta.ETag); err != nil {
		return err
	}
	return nil
}
```

### Java

這個範例使用 [Java 專用 Google HTTP 用戶端程式庫](https://developers.google.com/api-client-library/java/google-http-java-client/?hl=zh-tw)，將要求傳送至 BigQuery API。

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Java 設定說明操作。詳情請參閱 [BigQuery Java API 參考說明文件](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/overview?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import com.google.cloud.bigquery.BigQuery;
import com.google.cloud.bigquery.BigQueryException;
import com.google.cloud.bigquery.BigQueryOptions;
import com.google.cloud.bigquery.Dataset;
import java.util.HashMap;
import java.util.Map;

// Sample to updates a label on dataset
public class LabelDataset {

  public static void runLabelDataset() {
    // TODO(developer): Replace these variables before running the sample.
    String datasetName = "MY_DATASET_NAME";
    labelDataset(datasetName);
  }

  public static void labelDataset(String datasetName) {
    try {
      // Initialize client that will be used to send requests. This client only needs to be created
      // once, and can be reused for multiple requests.
      BigQuery bigquery = BigQueryOptions.getDefaultInstance().getService();

      // This example dataset starts with existing label { color: 'green' }
      Dataset dataset = bigquery.getDataset(datasetName);
      // Add label to dataset
      Map<String, String> labels = new HashMap<>();
      labels.put("color", "green");

      dataset.toBuilder().setLabels(labels).build().update();
      System.out.println("Label added successfully");
    } catch (BigQueryException e) {
      System.out.println("Label was not added. \n" + e.toString());
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

async function labelDataset() {
  // Updates a label on a dataset.

  /**
   * TODO(developer): Uncomment the following lines before running the sample
   */
  // const datasetId = "my_dataset";

  // Retrieve current dataset metadata.
  const dataset = bigquery.dataset(datasetId);
  const [metadata] = await dataset.getMetadata();

  // Add label to dataset metadata
  metadata.labels = {color: 'green'};
  const [apiResponse] = await dataset.setMetadata(metadata);

  console.log(`${datasetId} labels:`);
  console.log(apiResponse.labels);
}
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
dataset.labels = {"color": "green"}
dataset = client.update_dataset(dataset, ["labels"])  # Make an API request.

print("Labels added to {}".format(dataset_id))
```

## 更新資料表和檢視表標籤

資料表或檢視表建立後，您可以使用以下方式更新標籤：

* 使用 Google Cloud 控制台
* 使用 bq 指令列工具的 `bq update` 指令
* 呼叫 [`tables.patch`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables/patch?hl=zh-tw) API 方法
  + 由於系統會將檢視表當做資料表資源處理，因此可以使用 `tables.patch` 方法來修改檢視表和資料表。
* 使用用戶端程式庫

### 所需權限

如要更新資料表或檢視表標籤，您需要 `bigquery.tables.update` IAM 權限。

下列預先定義的 IAM 角色都包含更新資料表或檢視標籤所需的權限：

* `roles/bigquery.dataEditor`
* `roles/bigquery.dataOwner`
* `roles/bigquery.admin`

此外，如果您具備 `bigquery.datasets.create` 權限，可以更新所建立資料集中的資料表和檢視表標籤。

如要進一步瞭解 BigQuery 中的 IAM 角色和權限，請參閱[預先定義的角色與權限](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)一文。

### 更新資料表或檢視表標籤

如何更新資料表或視圖標籤：

### 控制台

1. 在 Google Cloud 控制台中選取資料表或檢視表。
2. 按一下 [Details] (詳細資料) 分頁標籤，然後按一下「Labels」(標籤) 右側的鉛筆圖示。
3. 在「Edit labels」(編輯標籤) 對話方塊中：

   * 如要套用其他標籤，請按一下 [Add Label] (新增標籤)。每個鍵只能在每個資料表或檢視表使用一次，但在不同資料集的資料表或檢視表中可使用同一個鍵。
   * 修改現有的鍵或值以更新標籤。
   * 按一下 [Update] (更新)，儲存您所做的變更。

### SQL

使用 [`ALTER TABLE SET OPTIONS` DDL 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#alter_table_set_options_statement)在現有資料表上設定標籤，或使用 [`ALTER VIEW SET OPTIONS` DDL 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#alter_view_set_options_statement)在現有檢視區塊上設定標籤。設定標籤會覆寫資料表或檢視表上的所有現有標籤。以下範例會在 `mytable` 資料表上設定兩個標籤：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列陳述式：

   ```
   ALTER TABLE mydataset.mytable
   SET OPTIONS (
     labels = [('department', 'shipping'), ('cost_center', 'logistics')]);
   ```
3. 按一下「執行」play\_circle。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

### bq

如要加入其他標籤或更新資料表/檢視表標籤，請發出 `bq
update` 指令並搭配使用 `set_label` 旗標。重複使用這個旗標即可加入或更新多個標籤。

如果資料表或檢視表位於預設專案以外的專案中，請使用下列格式將專案 ID 新增至資料集：`project_id:dataset`。

```
bq update \
--set_label key:value \
project_id:dataset.table_or_view
```

其中：

* key:value 是您要加入或更新的標籤的鍵/值組合，如果您指定與現有標籤相同的鍵，系統就會更新現有標籤的值。鍵不得重複。
* project\_id 是您的專案 ID。
* dataset 是包含您要更新的資料表/檢視表所屬的資料集。
* table\_or\_view 是您要更新之資料表或視圖的名稱。

範例：

如要更新 `mytable` 中的 `department` 標籤，請輸入 `bq update` 指令並指定 `department` 做為標籤鍵。例如，如要在 `mytable` 中，將 `department:shipping` 標籤更新為的 `department:logistics`，請輸入下列指令。`mytable` 在 `myotherproject` 中，而不是您的預設專案中。

```
    bq update \
    --set_label department:logistics \
    myotherproject:mydataset.mytable
```

輸出內容如下所示：

```
Table 'myotherproject:mydataset.mytable' successfully updated.
```

### API

如要為現有資料表或檢視表加入標籤或更新標籤，請呼叫 [`tables.patch`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables/patch?hl=zh-tw) 方法，然後加入或更新[資料表資源](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables?hl=zh-tw)的 `labels` 屬性。

由於系統會將檢視表當做資料表資源處理，因此可以使用 `tables.patch` 方法來修改檢視表和資料表。

由於 `tables.update` 方法會取代整個資料集資源，因此建議使用 `tables.patch` 方法。

### Go

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Go 設定說明操作。詳情請參閱 [BigQuery Go API 參考說明文件](https://godoc.org/cloud.google.com/go/bigquery)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import (
	"context"
	"fmt"

	"cloud.google.com/go/bigquery"
)

// addTableLabel demonstrates adding Label metadata to a BigQuery table.
func addTableLabel(projectID, datasetID, tableID string) error {
	// projectID := "my-project-id"
	// datasetID := "mydataset"
	// tableID := "mytable"
	ctx := context.Background()
	client, err := bigquery.NewClient(ctx, projectID)
	if err != nil {
		return fmt.Errorf("bigquery.NewClient: %v", err)
	}
	defer client.Close()

	tbl := client.Dataset(datasetID).Table(tableID)
	meta, err := tbl.Metadata(ctx)
	if err != nil {
		return err
	}

	update := bigquery.TableMetadataToUpdate{}
	update.SetLabel("color", "green")
	if _, err := tbl.Update(ctx, update, meta.ETag); err != nil {
		return err
	}
	return nil
}
```

### Java

這個範例使用 [Java 專用 Google HTTP 用戶端程式庫](https://developers.google.com/api-client-library/java/google-http-java-client/?hl=zh-tw)，將要求傳送至 BigQuery API。

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Java 設定說明操作。詳情請參閱 [BigQuery Java API 參考說明文件](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/overview?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import com.google.cloud.bigquery.BigQuery;
import com.google.cloud.bigquery.BigQueryException;
import com.google.cloud.bigquery.BigQueryOptions;
import com.google.cloud.bigquery.Table;
import com.google.cloud.bigquery.TableId;
import java.util.HashMap;
import java.util.Map;

// Sample to adds a label to an existing table
public class LabelTable {

  public static void runLabelTable() {
    // TODO(developer): Replace these variables before running the sample.
    String datasetName = "MY_DATASET_NAME";
    String tableName = "MY_TABLE_NAME";
    labelTable(datasetName, tableName);
  }

  public static void labelTable(String datasetName, String tableName) {
    try {
      // Initialize client that will be used to send requests. This client only needs to be created
      // once, and can be reused for multiple requests.
      BigQuery bigquery = BigQueryOptions.getDefaultInstance().getService();

      // This example table starts with existing label { color: 'green' }
      Table table = bigquery.getTable(TableId.of(datasetName, tableName));
      // Add label to table
      Map<String, String> labels = new HashMap<>();
      labels.put("color", "green");

      table.toBuilder().setLabels(labels).build().update();
      System.out.println("Label added successfully");
    } catch (BigQueryException e) {
      System.out.println("Label was not added. \n" + e.toString());
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

async function labelTable() {
  // Adds a label to an existing table.

  /**
   * TODO(developer): Uncomment the following lines before running the sample.
   */
  // const datasetId = 'my_dataset';
  // const tableId = 'my_table';

  const dataset = bigquery.dataset(datasetId);
  const [table] = await dataset.table(tableId).get();

  // Retrieve current table metadata
  const [metadata] = await table.getMetadata();

  // Add label to table metadata
  metadata.labels = {color: 'green'};
  const [apiResponse] = await table.setMetadata(metadata);

  console.log(`${tableId} labels:`);
  console.log(apiResponse.labels);
}
```

### Python

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Python 設定說明操作。詳情請參閱 [BigQuery Python API 參考說明文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
# from google.cloud import bigquery
# client = bigquery.Client()
# project = client.project
# dataset_ref = bigquery.DatasetReference(project, dataset_id)
# table_ref = dataset_ref.table('my_table')
# table = client.get_table(table_ref)  # API request

assert table.labels == {}
labels = {"color": "green"}
table.labels = labels

table = client.update_table(table, ["labels"])  # API request

assert table.labels == labels
```

## 更新工作標籤

目前尚不支援更新工作標籤。如要更新工作標籤，請指定新的標籤並重新提交工作。

## 更新預訂標籤

您可以更新預訂項目的標籤。使用 SQL 更新標籤會覆寫預留項目上的所有現有標籤。

### 必要的 IAM 角色

如要取得更新預留項目標籤所需的權限，請要求管理員授予管理專案的 [BigQuery 資源編輯者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.resourceEditor)  (`roles/bigquery.resourceEditor`) IAM 角色。如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

這個預先定義的角色具備 `bigquery.reservations.update` 權限，可將標籤更新至預訂項目。

您或許還可透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)取得這項權限。

### 更新預留項目的標籤

如要更新預訂項目的標籤：

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在導覽選單中，按一下「容量管理」。
3. 按一下「運算單元預留項目」分頁標籤。
4. 找出要更新的預訂。
5. 展開「動作」more\_vert選項。
6. 按一下 [編輯]。
7. 如要展開「進階設定」部分，請按一下expand\_more展開箭頭。
8. 更新鍵/值組合的名稱。
9. 按一下 [儲存]。

### bq

如要更新保留項目的標籤，請發出 `bq update` 指令並搭配使用 `set_label` 旗標和 `--reservation` 旗標。如要更新多個標籤，請重複使用這個旗標。

```
bq update --set_label KEY:VALUE  --reservation RESERVATION_NAME
```

更改下列內容：

* `KEY:VALUE`：要更新預訂項目的標籤鍵/值組合。鍵不得重複。鍵和值只能使用小寫字母、數字字元、底線和連字號。所有字元都必須使用 UTF-8 編碼，且可使用國際字元。如要更新預訂中的多個標籤，請重複使用 `--set_label` 旗標，並為每個標籤指定專屬鍵。
* `RESERVATION_NAME`：預訂名稱。

### SQL

如要更新預留項目的標籤，請使用 [`ALTER RESERVATION SET OPTIONS` DDL 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#alter_reservation_set_options_statement)，在現有預留項目中設定標籤。設定標籤會覆寫預留項目上的所有現有標籤。以下範例會在預訂 `myreservation` 上設定標籤：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列陳述式：

   ```
   ALTER RESERVATION myreservation
   SET OPTIONS (
     labels = [('sensitivity', 'high')]);
   ```
3. 按一下「執行」play\_circle。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

## 將標籤轉換為標記

包含具有空白值的鍵的標籤可做為標記。您可以建立不含任何值的新標籤，或是將資料集內的現有標籤轉換成標記。您無法將工作標籤轉換為標記。

如果想幫資源加上標籤，標記是很實用的做法，但您不一定要使用 `key:value` 格式。例如，如果您的資料表包含由多個群組 (支援和開發等) 使用的測試資料，您可以在該資料表中加入 `test_data` 標記以供識別。

### 所需權限

如要將標籤轉換為標記，您必須具備下列 IAM 權限：

* `bigquery.datasets.update` (可轉換資料集標籤)
* `bigquery.tables.update` (可轉換資料表或檢視表標籤)

下列預先定義的 IAM 角色都包含轉換資料集標籤所需的權限：

* `roles/bigquery.dataOwner`
* `roles/bigquery.admin`

下列預先定義的 IAM 角色都包含轉換表格或檢視標籤所需的權限：

* `roles/bigquery.dataEditor`
* `roles/bigquery.dataOwner`
* `roles/bigquery.admin`

此外，如果您擁有 `bigquery.datasets.create` 權限，可以更新您建立的資料集標籤，以及這些資料集中的資料表和檢視表。

如要進一步瞭解 BigQuery 中的 IAM 角色和權限，請參閱[預先定義的角色與權限](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)一文。

### 將標籤轉換為標記

如何將標籤轉換為標記：

### 控制台

1. 在 Google Cloud 控制台中，選取資料集、資料表或檢視表。
2. 如果是資料集，「Dataset Details」(資料集詳細資料) 頁面會自動開啟；如果是資料表和檢視表，請按一下 [Details] (詳細資料) 以開啟詳細資料頁面。
3. 在「Details」(詳細資料) 頁面中，按一下「Labels」(標籤) 右側的鉛筆圖示。
4. 在「Edit labels」(編輯標籤) 對話方塊中：

   * 刪除現有標籤的值。
   * 按一下「Update」。

### bq

如要將標籤轉換為標記，請將 `bq update` 指令搭配 `set_label` 旗標使用。請指定鍵並在後面加入冒號，但不要指定值。這樣就可以將現有的標籤更新為標記。

```
bq update \
--set_label key: \
resource_id
```

其中：

* key: 是您要變更為標記的標籤鍵。
* resource\_id 是有效的資料集、資料表或視圖名稱。如果資源位於預設專案以外的專案中，請使用下列格式加入專案 ID：`project_id:dataset`。

範例：

輸入以下指令，將 `mydataset` 上現有的 `test_data:development` 標籤變更為標記。`mydataset` 在 `myotherproject` 中，而不是您的預設專案中。

```
bq update --set_label test_data: myotherproject:mydataset
```

輸出內容如下所示：

```
Dataset 'myotherproject:mydataset' successfully updated.
```

### API

如要將現有標籤轉換為標記，請呼叫 [`datasets.patch`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/datasets/patch?hl=zh-tw) 方法或 [`tables.patch`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables/patch?hl=zh-tw) 方法，並在[資料集資源](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/datasets?hl=zh-tw)或[資料表資源](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables?hl=zh-tw)中將標籤值替換為空字串 (`""`)。

由於系統會將檢視表當做資料表資源處理，因此可以使用 `tables.patch` 方法來修改檢視表和資料表。此外，因為 `tables.update` 方法會取代整個資料集資源，因此建議使用 `tables.patch` 方法。

## 後續步驟

* 瞭解如何為 BigQuery 資源[加上標籤](https://docs.cloud.google.com/bigquery/docs/adding-labels?hl=zh-tw)。
* 瞭解如何在 BigQuery 資源中[查看標籤](https://docs.cloud.google.com/bigquery/docs/viewing-labels?hl=zh-tw)。
* 瞭解如何[使用標籤篩選資源](https://docs.cloud.google.com/bigquery/docs/filtering-labels?hl=zh-tw)。
* 瞭解如何在 BigQuery 資源中[刪除標籤](https://docs.cloud.google.com/bigquery/docs/deleting-labels?hl=zh-tw)。
* 請參閱 Resource Manager 說明文件中的[使用標籤](https://docs.cloud.google.com/resource-manager/docs/using-labels?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-09 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-09 (世界標準時間)。"],[],[]]