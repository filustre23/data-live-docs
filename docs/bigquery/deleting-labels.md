Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 刪除標籤

您可以透過以下方式從資料集、資料表或檢視表刪除標籤：

* 使用 Google Cloud 控制台
* 使用 SQL [DDL 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw)
* 使用 bq 指令列工具的 `bq update` 指令
* 呼叫 [`datasets.patch`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/datasets/patch?hl=zh-tw) 或 [`tables.patch`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables/patch?hl=zh-tw) API 方法
* 使用用戶端程式庫

## 事前準備

授予身分與存取權管理 (IAM) 角色，讓使用者擁有執行本文件各項工作所需的權限。執行工作所需的權限 (如有) 會列在工作「必要權限」部分。

## 刪除資料集標籤

以下各節將說明刪除資料集標籤的權限和步驟。

### 所需權限

如要刪除資料集標籤，您必須具備下列 IAM 權限：

* `bigquery.datasets.get`
* `bigquery.datasets.update`

下列預先定義的 IAM 角色都具備刪除資料集標籤所需的權限：

* `roles/bigquery.dataOwner`
* `roles/bigquery.admin`

此外，如果您具備 `bigquery.datasets.create` 權限，可以刪除您建立的資料集標籤。

如要進一步瞭解 BigQuery 中的 IAM 角色和權限，請參閱[預先定義的角色與權限](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)一文。

### 刪除資料集標籤

如要從資料集中刪除標籤，請選擇下列其中一個選項：

### 控制台

1. 在 Google Cloud 控制台中選取資料集。
2. 在「Dataset Details」(資料集詳細資料) 頁面中，按一下「Labels」(標籤) 右側的鉛筆圖示。
3. 在「Edit labels」(編輯標籤) 對話方塊中：

   * 針對要刪除的每個標籤，按一下刪除圖示 (X)。
   * 如要儲存變更，請按一下「更新」。

### SQL

使用 [`ALTER SCHEMA SET OPTIONS` DDL 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#alter_schema_set_options_statement)，在現有資料集上設定標籤。設定標籤會覆寫資料集上的所有現有標籤。以下範例會刪除資料集 `mydataset` 的所有標籤：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列陳述式：

   ```
   ALTER SCHEMA mydataset
   SET OPTIONS (labels = []);
   ```
3. 按一下「執行」play\_circle。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

### bq

如要刪除資料集標籤，請發出 `bq update` 指令並搭配使用 `clear_label` 旗標。重複該標記即可刪除多個標籤。

如果資料集位於預設專案以外的專案中，請使用下列格式將專案 ID 新增至資料集：`project_id:dataset`。

```
bq update \
--clear_label key \
project_id:dataset
```

其中：

* key 是要刪除的標籤鍵。
* project\_id 是您的專案 ID。
* dataset 是您要更新的資料集。

範例：

如要從 `mydataset` 刪除 `department:shipping` 標籤，請輸入帶有 `--clear_label` 標記的 `bq update` 指令。`mydataset` 在您的預設專案中。

```
    bq update --clear_label department mydataset
```

如要從 `myotherproject` 的 `mydataset` 刪除 `department:shipping` 標籤，請輸入帶有 `--clear_label` 標記的 `bq update` 指令。

```
    bq update --clear_label department myotherproject:mydataset
```

如要從資料集刪除多個標籤，請重複執行 `clear_label` 標記並指定每個標籤的鍵。舉例來說，如要從預設專案中的 `mydataset` 刪除 `department:shipping` 標籤和 `cost_center:logistics` 標籤，請輸入：

```
    bq update \
    --clear_label department \
    --clear_label cost_center \
    mydataset
```

各範例的輸出內容如下：

```
Dataset 'myproject:mydataset' successfully updated.
```

### API

如要刪除現有資料集的特定標籤，請呼叫 [`datasets.patch`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/datasets/patch?hl=zh-tw) 方法，然後將標籤的鍵值設為 `null`，藉此更新[資料集資源](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/datasets?hl=zh-tw)的 `labels` 屬性。

如要從資料集中刪除所有標籤，請呼叫 [`datasets.patch`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/datasets/patch?hl=zh-tw) 方法並刪除 `labels` 屬性。

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

// deleteDatasetLabel demonstrates removing a specific label from a dataset's metadata.
func deleteDatasetLabel(projectID, datasetID string) error {
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
	update.DeleteLabel("color")
	if _, err := ds.Update(ctx, update, meta.ETag); err != nil {
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
import com.google.cloud.bigquery.Dataset;
import java.util.HashMap;
import java.util.Map;

// Sample tp deletes a label on a dataset.
public class DeleteLabelDataset {

  public static void runDeleteLabelDataset() {
    // TODO(developer): Replace these variables before running the sample.
    String datasetName = "MY_DATASET_NAME";
    deleteLabelDataset(datasetName);
  }

  public static void deleteLabelDataset(String datasetName) {
    try {
      // Initialize client that will be used to send requests. This client only needs to be created
      // once, and can be reused for multiple requests.
      BigQuery bigquery = BigQueryOptions.getDefaultInstance().getService();

      // This example dataset starts with existing label { color: 'green' }
      Dataset dataset = bigquery.getDataset(datasetName);
      // Add label to dataset
      Map<String, String> labels = new HashMap<>();
      labels.put("color", null);

      dataset.toBuilder().setLabels(labels).build().update();
      System.out.println("Dataset label deleted successfully");
    } catch (BigQueryException e) {
      System.out.println("Dataset label was not deleted. \n" + e.toString());
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

async function deleteLabelDataset() {
  // Deletes a label on a dataset.
  // This example dataset starts with existing label { color: 'green' }

  /**
   * TODO(developer): Uncomment the following lines before running the sample.
   */
  // const datasetId = 'my_dataset';

  // Retrieve current dataset metadata.
  const dataset = bigquery.dataset(datasetId);
  const [metadata] = await dataset.getMetadata();

  // Add label to dataset metadata
  metadata.labels = {color: null};
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

# To delete a label from a dataset, set its value to None.
dataset.labels["color"] = None

dataset = client.update_dataset(dataset, ["labels"])  # Make an API request.
print("Labels deleted from {}".format(dataset_id))
```

## 刪除資料表或檢視表標籤

您可以透過下列方式刪除資料表或檢視表標籤：

* 使用 Google Cloud 控制台
* 使用 SQL [DDL 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw)
* 使用 bq 指令列工具的 `bq update` 指令
* 呼叫 [`tables.patch`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables/patch?hl=zh-tw) API 方法
  + 由於系統會將檢視表當做資料表資源處理，因此可以使用 `tables.patch` 方法來修改檢視表和資料表。
* 使用用戶端程式庫

### 所需權限

如要刪除資料表或檢視表標籤，您必須具備下列 IAM 權限：

* `bigquery.tables.get`
* `bigquery.tables.update`

下列每個預先定義的 IAM 角色都包含刪除表格或查看標籤所需的權限：

* `roles/bigquery.dataEditor`
* `roles/bigquery.dataOwner`
* `roles/bigquery.admin`

此外，如果您具備 `bigquery.datasets.create` 權限，可以刪除所建立資料集中資料表和檢視區塊的標籤。

如要進一步瞭解 BigQuery 中的 IAM 角色和權限，請參閱[預先定義的角色與權限](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)一文。

### 刪除資料表或檢視表標籤

如要刪除資料表或檢視表中的標籤，請選擇下列其中一個選項：

### 控制台

1. 在 Google Cloud 控制台中選取資料集。
2. 按一下 [Details] (詳細資料) 分頁標籤，然後按一下「Labels」(標籤) 右側的鉛筆圖示。
3. 在「Edit labels」(編輯標籤) 對話方塊中：

   * 針對要刪除的每個標籤，按一下刪除圖示 (X)。
   * 如要儲存變更，請按一下「更新」。

### SQL

如要在現有資料表上設定標籤，請使用 [`ALTER TABLE SET OPTIONS` DDL 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#alter_table_set_options_statement)；如要在現有檢視區塊上設定標籤，請使用 [`ALTER VIEW SET OPTIONS` DDL 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#alter_view_set_options_statement)。設定標籤會覆寫資料表或檢視表上的所有現有標籤。以下範例會從 `mytable` 資料表刪除所有標籤：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列陳述式：

   ```
   ALTER TABLE mydataset.mytable
   SET OPTIONS (labels = []);
   ```
3. 按一下「執行」play\_circle。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

### bq

如要從資料表或檢視表中刪除標籤，請發出 `bq update` 指令並搭配使用 `clear_label` 標記。重複該標記即可刪除多個標籤。

如果資料表或檢視表位於預設專案以外的專案中，請使用下列格式將專案 ID 新增至資料集：`project_id:dataset`。

```
bq update \
--clear_label key \
project_id:dataset.table_or_view
```

其中：

* key 是要刪除的標籤鍵。
* project\_id 是您的專案 ID。
* dataset 是您要更新的資料集。
* table\_or\_view 是您要更新之資料表或視圖的名稱。

範例：

如要從 `mydataset.mytable` 刪除 `department:shipping` 標籤，請輸入帶有 `--clear_label` 標記的 `bq update` 指令。`mydataset` 在您的預設專案中。

```
    bq update --clear_label department mydataset.mytable
```

如要從 `myotherproject` 的 `mydataset.myview` 刪除 `department:shipping` 標籤，請輸入帶有 `--clear_label` 標記的 `bq update` 指令。

```
    bq update --clear_label department myotherproject:mydataset.myview
```

如要從資料表或檢視表刪除多個標籤，請重複執行 `clear_label` 標記並指定每個標籤的鍵。舉例來說，如要從預設專案中的 `mydataset.mytable` 刪除 `department:shipping` 標籤和 `cost_center:logistics` 標籤，請輸入：

```
    bq update \
    --clear_label department \
    --clear_label cost_center \
    mydataset.mytable
```

各範例的輸出內容如下：

```
Table 'myproject:mydataset.mytable' successfully updated.
```

### API

如要刪除現有資料表或檢視表的特定標籤，請呼叫 [`tables.patch`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables/patch?hl=zh-tw) 方法，然後將標籤的鍵值設為 `null`，藉此更新[資料表資源](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables?hl=zh-tw)的 `labels` 屬性。

如要從資料表或檢視表刪除所有標籤，請呼叫 [`tables.patch`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables/patch?hl=zh-tw) 方法並刪除 `labels` 屬性。

由於系統會將檢視表當做資料表資源處理，因此可以使用 `tables.patch` 方法來修改檢視表和資料表。此外，因為 `tables.update` 方法會取代整個資料集資源，因此建議使用 `tables.patch` 方法。

### Go

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Go 設定說明操作。詳情請參閱 [BigQuery Go API 參考說明文件](https://godoc.org/cloud.google.com/go/bigquery)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import (
	"context"
	"fmt"

	"cloud.google.com/go/bigquery"
)

// deleteTableLabel demonstrates how to remove a specific metadata Label from a BigQuery table.
func deleteTableLabel(projectID, datasetID, tableID string) error {
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
	update.DeleteLabel("color")
	if _, err := tbl.Update(ctx, update, meta.ETag); err != nil {
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
import com.google.cloud.bigquery.Table;
import com.google.cloud.bigquery.TableId;
import java.util.HashMap;
import java.util.Map;

// Sample tp deletes a label on a table.
public class DeleteLabelTable {

  public static void runDeleteLabelTable() {
    // TODO(developer): Replace these variables before running the sample.
    String datasetName = "MY_DATASET_NAME";
    String tableName = "MY_TABLE_NAME";
    deleteLabelTable(datasetName, tableName);
  }

  public static void deleteLabelTable(String datasetName, String tableName) {
    try {
      // Initialize client that will be used to send requests. This client only needs to be created
      // once, and can be reused for multiple requests.
      BigQuery bigquery = BigQueryOptions.getDefaultInstance().getService();

      // This example table starts with existing label { color: 'green' }
      Table table = bigquery.getTable(TableId.of(datasetName, tableName));
      // Add label to table
      Map<String, String> labels = new HashMap<>();
      labels.put("color", null);

      table.toBuilder().setLabels(labels).build().update();
      System.out.println("Table label deleted successfully");
    } catch (BigQueryException e) {
      System.out.println("Table label was not deleted. \n" + e.toString());
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

async function deleteLabelTable() {
  // Deletes a label from an existing table.
  // This example dataset starts with existing label { color: 'green' }

  /**
   * TODO(developer): Uncomment the following lines before running the sample.
   */
  // const datasetId = "my_dataset";
  // const tableId = "my_table";

  const dataset = bigquery.dataset(datasetId);
  const [table] = await dataset.table(tableId).get();

  // Retrieve current table metadata
  const [metadata] = await table.getMetadata();

  // Add label to table metadata
  metadata.labels = {color: null};
  const [apiResponse] = await table.setMetadata(metadata);

  console.log(`${tableId} labels:`);
  console.log(apiResponse.labels);
}
```

### Python

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Python 設定說明操作。詳情請參閱 [BigQuery Python API 參考說明文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
from google.cloud import bigquery

client = bigquery.Client()

# TODO(dev): Change table_id to the full name of the table you wish to delete from.
table_id = "your-project.your_dataset.your_table_name"
# TODO(dev): Change label_key to the name of the label you want to remove.
label_key = "color"
table = client.get_table(table_id)  # API request

# To delete a label from a table, set its value to None
table.labels[label_key] = None

table = client.update_table(table, ["labels"])  # API request

print(f"Deleted label '{label_key}' from {table_id}.")
```

## 刪除預留標籤

你可以刪除預訂標籤。

### 必要的 IAM 角色

如要取得刪除預留標籤所需的權限，請要求系統管理員授予管理專案的 [BigQuery 資源編輯者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.resourceEditor)  (`roles/bigquery.resourceEditor`) IAM 角色。如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

這個預先定義的角色具備 `bigquery.reservations.delete` 權限，可刪除預訂標籤。

您或許還可透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)取得這項權限。

### 刪除預留標籤

如要從預訂項目中刪除標籤，請選擇下列其中一個選項：

### SQL

如要刪除預訂標籤，請使用 [`ALTER RESERVATION SET OPTIONS` DDL 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#alter_reservation_set_options_statement)。
如要刪除預訂項目的標籤，請將標籤設為空陣列。以下範例會刪除預留項目 `myreservation` 的標籤：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列陳述式：

   ```
   ALTER RESERVATION myreservation
   SET OPTIONS (
     labels = []);
   ```
3. 按一下「執行」play\_circle。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

### bq

如要刪除預訂標籤，請發出 `bq update` 指令並搭配使用 `clear_label` 和 `--reservation` 標記。如要刪除多個標籤，請重複執行該標記。

```
bq update --clear_label KEY  --reservation RESERVATION_NAME
```

更改下列內容：

* `KEY`：要從預訂項目刪除的標籤鍵。鍵不得重複。鍵和值只能使用小寫字母、數字字元、底線和連字號。所有字元都必須使用 UTF-8 編碼，且可使用國際字元。如要刪除預訂項目的多個標籤，請重複使用 `--clear_label` 旗標並為每個標籤指定專屬鍵。
* `RESERVATION_NAME`：預訂名稱。

## 刪除工作標籤

目前尚不支援從現有工作中刪除標籤。

## 後續步驟

* 瞭解如何為 BigQuery 資源[加上標籤](https://docs.cloud.google.com/bigquery/docs/adding-labels?hl=zh-tw)。
* 瞭解如何在 BigQuery 資源中[查看標籤](https://docs.cloud.google.com/bigquery/docs/viewing-labels?hl=zh-tw)。
* 瞭解如何在 BigQuery 資源中[更新標籤](https://docs.cloud.google.com/bigquery/docs/updating-labels?hl=zh-tw)。
* 瞭解如何[使用標籤篩選資源](https://docs.cloud.google.com/bigquery/docs/filtering-labels?hl=zh-tw)。
* 請參閱 Resource Manager 說明文件中的[使用標籤](https://docs.cloud.google.com/resource-manager/docs/using-labels?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-12 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-12 (世界標準時間)。"],[],[]]