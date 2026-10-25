Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 為資源新增標籤

BigQuery 標籤可讓您將鍵/值中繼資料附加至資源。這類中繼資料可協助您整理工作負載、篩選資產，以及追蹤各項專案的已計費用。

您可以為[資料集](#adding_dataset_labels)、[資料表和檢視表](#adding_table_and_view_labels)、[工作](#job-label)、[工作工作階段](#adding-label-to-session)和[預留項目](#reservation)新增標籤。如要進一步瞭解 BigQuery 中的標籤，請參閱「[標籤簡介](https://docs.cloud.google.com/bigquery/docs/labels-intro?hl=zh-tw)」。

## 事前準備

授予使用者必要的 Identity and Access Management (IAM) 角色，以便執行本文件中的各項工作。每項工作的「必要 IAM 角色」部分會列出執行該工作所需的權限。

## 為資料集新增標籤

使用 bq 指令列工具的 `bq mk` 指令，或呼叫 [`datasets.insert`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/datasets/insert?hl=zh-tw) API 方法，即可在建立 BigQuery 資料集時新增標籤。使用 Google Cloud 控制台建立資料集時，無法為資料集新增標籤。不過，您可以在建立資料集後新增標籤。如要進一步瞭解如何建立資料集，請參閱「[建立資料集](https://docs.cloud.google.com/bigquery/docs/datasets?hl=zh-tw)」。

將標籤新增至資料集時，標籤不會傳播至資料集內的資源。資料表或檢視表不會沿用資料集標籤。此外，當您將標籤新增至資料集時，該標籤會包含在儲存空間帳單資料中，但不會包含在工作相關帳單資料中。

如要進一步瞭解標籤格式，請參閱[標籤規定](https://docs.cloud.google.com/bigquery/docs/labels-intro?hl=zh-tw#requirements)。

### 必要的 IAM 角色

如要取得為現有資料集新增標籤所需的權限，請要求管理員授予您 [BigQuery 資料擁有者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.dataOwner)  (`roles/bigquery.dataOwner`) IAM 角色。如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

這個預先定義的角色具備 `bigquery.datasets.update` 權限，可為現有資料集新增標籤。

您或許還可透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)取得這項權限。

如要進一步瞭解 BigQuery 的 IAM 角色和權限，請參閱「[預先定義的角色和權限](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)」。

### 為資料集新增標籤

如何在建立資料集後加入標籤：

### 控制台

1. 在 Google Cloud 控制台中選取資料集。
2. 在資料集詳細資料頁面的「Labels」(標籤) 部分，按一下 edit「Edit」(編輯)。
3. 在「Edit labels」(編輯標籤) 對話方塊中：

   * 按一下 [Add label] (新增標籤)。
   * 在適當欄位中輸入鍵和值。如要套用其他標籤，請按一下 [Add Label] (新增標籤)。每個鍵在每個資料集中只能使用一次，但您可以在相同專案的不同資料集裡使用同一個鍵。
   * 如要更新標籤，請修改現有的鍵或值。
   * 點按「更新」以儲存變更。

### SQL

使用 [`ALTER SCHEMA SET OPTIONS` DDL 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#alter_schema_set_options_statement)，為現有資料集設定標籤。這項操作會覆寫資料集上的任何現有標籤。以下範例會為 `mydataset` 資料集設定標籤：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列陳述式：

   ```
   ALTER SCHEMA mydataset
   SET OPTIONS (
     labels = [('sensitivity', 'high')]);
   ```
3. 按一下「play\_circle 執行」。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

### bq

如要為現有資料集新增標籤，請使用 `bq update` 指令並加上 `set_label` 旗標。如要新增多個標籤，請重複使用這個旗標。

如果資料集位於預設專案以外的專案，請使用下列格式指定專案 ID：`PROJECT_ID:DATASET`。

```
bq update --set_label KEY:VALUE PROJECT_ID:DATASET
```

更改下列內容：

* `KEY:VALUE`：要新增的標籤鍵/值組合。鍵不得重複。鍵和值只能使用小寫字母、數字字元、底線和連字號。所有字元都必須使用 UTF-8 編碼，且可使用國際字元。
* `PROJECT_ID`：您的專案 ID。
* `DATASET`：要加上標籤的資料集。

範例：

如要新增標籤來追蹤部門，請使用 `bq update` 指令，並指定 `department` 做為標籤鍵。舉例來說，如要將 `department:shipping` 標籤新增至預設專案中的 `mydataset`，請使用：

```
    bq update --set_label department:shipping mydataset
```

如要為資料集新增多個標籤，請重複 `set_label` 旗標，並為每個標籤指定專屬鍵。舉例來說，如要將 `department:shipping` 標籤和 `cost_center:logistics` 標籤新增至預設專案中的 `mydataset`，請使用：

```
    bq update \
    --set_label department:shipping \
    --set_label cost_center:logistics \
    mydataset
```

### API

如要在現有資料集中加入標籤，請呼叫 [`datasets.patch`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/datasets/patch?hl=zh-tw) 方法，然後填入[資料集資源](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/datasets?hl=zh-tw)的 `labels` 屬性。

由於 `datasets.update` 方法會取代整個資料集資源，因此請改用 `datasets.patch` 方法。

### Go

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Go 設定操作說明進行操作。詳情請參閱 [BigQuery Go API 參考文件](https://godoc.org/cloud.google.com/go/bigquery)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

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

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Java 設定操作說明進行操作。詳情請參閱 [BigQuery Java API 參考文件](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/overview?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import com.google.cloud.bigquery.BigQuery;
import com.google.cloud.bigquery.BigQueryException;
import com.google.cloud.bigquery.BigQueryOptions;
import com.google.cloud.bigquery.Dataset;
import java.util.HashMap;
import java.util.Map;

// Sample to updates a label on dataset
public class LabelDataset {

  public static void main(String[] args) {
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

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Node.js 設定操作說明進行操作。詳情請參閱 [BigQuery Node.js API 參考文件](https://googleapis.dev/nodejs/bigquery/latest/index.html)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

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

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Python 設定操作說明進行操作。詳情請參閱 [BigQuery Python API 參考文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

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

## 為資料表和檢視表新增標籤

本文說明如何為現有資料表或檢視表新增標籤。如要進一步瞭解如何在建立資料表或檢視表時新增標籤，請參閱「[建立資料表](https://docs.cloud.google.com/bigquery/docs/tables?hl=zh-tw)」或「[建立檢視表](https://docs.cloud.google.com/bigquery/docs/views?hl=zh-tw)」。

由於系統會將檢視表當做資料表資源處理，因此可以使用 `tables.patch` 方法來修改檢視表和資料表。

帳單資料不含資料表和檢視表標籤。

### 必要的 IAM 角色

如要取得為現有資料表或檢視表新增標籤所需的權限，請要求管理員授予您 [BigQuery 資料編輯者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.dataEditor)  (`roles/bigquery.dataEditor`) IAM 角色。如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

這個預先定義的角色具備為現有資料表或檢視表新增標籤所需的權限。如要查看確切的必要權限，請展開「Required permissions」(必要權限) 部分：

#### 所需權限

您必須具備下列權限，才能為現有資料表或檢視表新增標籤：

* `bigquery.tables.update`
* `bigquery.tables.get`

您或許還可透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)取得這些權限。

如要進一步瞭解 BigQuery 的 IAM 角色和權限，請參閱「[預先定義的角色和權限](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)」。

### 為資料表或檢視表新增標籤

如何在現有資料表或視圖中加入標籤：

### 控制台

1. 在 Google Cloud 控制台中，選取資料表或檢視表。
2. 點按「Details」(詳細資料) 分頁標籤。
3. 在「Labels」(標籤) 區段中，按一下 edit「Edit」(編輯)。
4. 在「Edit labels」(編輯標籤) 對話方塊中：

   * 按一下 [Add label] (新增標籤)。
   * 在適當欄位中輸入鍵和值。如要套用其他標籤，請按一下 [Add Label] (新增標籤)。每個鍵在每個資料集中只能使用一次，但您可以在相同專案的不同資料集裡使用同一個鍵。
   * 修改現有的鍵/值以更新標籤。
   * 按一下 [Update] (更新)，儲存您所做的變更。

### SQL

使用 [`ALTER TABLE SET OPTIONS` DDL 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#alter_table_set_options_statement)設定現有資料表的標籤，或使用 [`ALTER VIEW SET OPTIONS` DDL 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#alter_view_set_options_statement)設定現有檢視表的標籤。這項操作會覆寫資料表或檢視表上的任何現有標籤。以下範例會在 `mytable` 資料表上設定兩個標籤：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列陳述式：

   ```
   ALTER TABLE mydataset.mytable
   SET OPTIONS (
     labels = [('department', 'shipping'), ('cost_center', 'logistics')]);
   ```
3. 按一下「play\_circle 執行」。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

### bq

如要為現有資料表或檢視表新增標籤，請使用 `bq update` 指令並加上 `set_label` 旗標。如要新增多個標籤，請重複使用這個旗標。

如果資料表或檢視表位於預設專案以外的專案，請使用下列格式指定專案 ID：`PROJECT_ID:DATASET`。

```
bq update \
--set_label KEY:VALUE \
PROJECT_ID:DATASET.TABLE_OR_VIEW
```

更改下列內容：

* `KEY:VALUE`：要新增的標籤鍵/值組合。鍵不得重複。鍵和值只能使用小寫字母、數字字元、底線和連字號。所有字元都必須使用 UTF-8 編碼，且可使用國際字元。
* `PROJECT_ID`：您的專案 ID。
* `DATASET`：包含要加上標籤的資料表或
  檢視表的資料集。
* `TABLE_OR_VIEW`：要加上標籤的資料表或檢視表名稱。

範例：

如要新增追蹤部門的資料表標籤，請使用 `bq update` 指令，並將 `department` 指定為標籤鍵。舉例來說，如要將 `department:shipping` 標籤新增至預設專案中的 `mytable`，請使用：

```
    bq update --set_label department:shipping mydataset.mytable
```

如要新增追蹤部門的檢視表標籤，請使用 `bq update` 指令，並將 `department` 指定為標籤鍵。舉例來說，如要將 `department:shipping` 標籤新增至預設專案中的 `myview`，請使用：

```
    bq update --set_label department:shipping mydataset.myview
```

如要在資料表或檢視表中加入多個標籤，請重複使用 `set_label` 旗標並為每個標籤指定專屬鍵。舉例來說，如要將 `department:shipping` 標籤和 `cost_center:logistics` 標籤新增至預設專案中的 `mytable`，請使用：

```
    bq update \
    --set_label department:shipping \
    --set_label cost_center:logistics \
    mydataset.mytable
```

### API

如要在現有資料表或檢視表中加入標籤，請呼叫 [`tables.patch`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables/patch?hl=zh-tw) 方法，然後填入[資料集資源](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables?hl=zh-tw)的 `labels` 屬性。

由於系統會將檢視表當做資料表資源處理，因此可以使用 `tables.patch` 方法來修改檢視表和資料表。

`tables.update` 方法會取代整個資料集資源，因此請改用 `tables.patch` 方法。

### Go

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Go 設定操作說明進行操作。詳情請參閱 [BigQuery Go API 參考文件](https://godoc.org/cloud.google.com/go/bigquery)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

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

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Java 設定操作說明進行操作。詳情請參閱 [BigQuery Java API 參考文件](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/overview?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

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

  public static void main(String[] args) {
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

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Node.js 設定操作說明進行操作。詳情請參閱 [BigQuery Node.js API 參考文件](https://googleapis.dev/nodejs/bigquery/latest/index.html)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

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

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Python 設定操作說明進行操作。詳情請參閱 [BigQuery Python API 參考文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
from google.cloud import bigquery

client = bigquery.Client()

# TODO(dev): Change table_id to the full name of the table you want to create.
table_id = "your-project.your_dataset.your_table_name"

table = client.get_table(table_id)  # API request

labels = {"color": "green"}
table.labels = labels

table = client.update_table(table, ["labels"])  # API request

print(f"Added {table.labels} to {table_id}.")
```

## 為工作新增標籤

您可以使用 bq 指令列工具的 `--label` 旗標，透過指令列將標籤新增至查詢工作。bq 工具僅支援為查詢工作新增標籤。

您也可以在透過 API 提交工作時，在呼叫 [`jobs.insert`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs/insert?hl=zh-tw) 方法時指定工作設定中的 `labels` 屬性，為工作新增標籤。API 可用於在任何工作類型中加入標籤。

您無法在待處理、執行中或已完成的工作中加入或更新標籤。

在工作中加入標籤後，標籤就會納入您的帳單資料中。

### 必要的 IAM 角色

如要取得為工作新增標籤所需的權限，請要求管理員授予您「[BigQuery 使用者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.user) 」(`roles/bigquery.user`) IAM 角色。如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

這個預先定義的角色具備 `bigquery.jobs.create` 權限，可為工作新增標籤。

您或許還可透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)取得這項權限。

如要進一步瞭解 BigQuery 的 IAM 角色和權限，請參閱「[預先定義的角色和權限](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)」。

### 為工作加上標籤

如何在工作中加入標籤：

### bq

如要為查詢工作新增標籤，請使用 `bq query` 指令並搭配 `--label` 旗標。如要新增多個標籤，請重複使用這個旗標。這個旗標表示查詢使用 GoogleSQL 語法。

```
bq query --label KEY:VALUE  'QUERY'
```

更改下列內容：

* `KEY:VALUE`：要新增至查詢工作的標籤鍵/值組合。鍵不得重複。鍵和值只能使用小寫字母、數字字元、底線和連字號。所有字元都必須使用 UTF-8 編碼，且可使用國際字元。如要為查詢工作新增多個標籤，請重複 `--label` 旗標，並為每個標籤指定不重複的鍵。
* `QUERY`：有效的 GoogleSQL 查詢。

範例：

如要為查詢工作新增標籤，請使用：

```
    bq query \
    --label department:shipping \
     \
    'SELECT
       column1, column2
     FROM
       `mydataset.mytable`'
```

如要在查詢工作中加入多個標籤，請重複使用 `--label` 旗標並為每個標籤指定專屬鍵。舉例來說，如要將 `department:shipping` 標籤和 `cost_center:logistics` 標籤新增至查詢工作，請使用：

```
    bq query \
    --label department:shipping \
    --label cost_center:logistics \
     \
    'SELECT
       column1, column2
     FROM
       `mydataset.mytable`'
```

### API

如要為工作新增標籤，請呼叫 [`jobs.insert`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs/insert?hl=zh-tw) 方法，並填入[工作設定](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#jobconfiguration)的 `labels` 屬性。您可以使用 API 在任何類型的工作中加入標籤。

### Python

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Python 設定操作說明進行操作。詳情請參閱 [BigQuery Python API 參考文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
from google.cloud import bigquery

client = bigquery.Client()

sql = """
    SELECT corpus
    FROM `bigquery-public-data.samples.shakespeare`
    GROUP BY corpus;
"""
labels = {"color": "green"}

config = bigquery.QueryJobConfig()
config.labels = labels
location = "us"
job = client.query(sql, location=location, job_config=config)
job_id = job.job_id

print(f"Added {job.labels} to {job_id}.")
```

### 為工作階段中的工作加上標籤

如果您在[工作階段](https://docs.cloud.google.com/bigquery/docs/sessions-intro?hl=zh-tw)中執行查詢，可以使用 BigQuery 多陳述式查詢，為該工作階段中所有日後的查詢工作指派標籤。

### SQL

執行下列查詢，在工作階段中設定 [`@@query_label`](https://docs.cloud.google.com/bigquery/docs/reference/system-variables?hl=zh-tw) 系統變數：

```
  SET @@query_label = "KEY:VALUE";
```

* KEY:VALUE：標籤的鍵/值組合，用於指派給工作階段中日後的所有查詢。您也可以新增多個鍵/值組合，並以半形逗號分隔，例如 `SET @@query_label = "key1:value1,key2:value2"`。鍵不得重複。鍵和值只能使用小寫字母、數字字元、底線和連字號。所有字元都必須使用 UTF-8 編碼，且可使用國際字元。

範例：

```
  SET @@query_label = "cost_center:logistics";
```

### API

如要在[使用 API 呼叫執行查詢](https://docs.cloud.google.com/bigquery/docs/sessions?hl=zh-tw#run-queries)時，為工作階段中的查詢工作新增標籤，請呼叫 [`jobs.insert`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs/insert?hl=zh-tw) 方法，並填入[`connectionProperties`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/ConnectionProperty?hl=zh-tw)
[工作設定](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#jobconfiguration)的 `query_label` 屬性。

將查詢標籤與工作階段建立關聯，並在該工作階段中執行查詢後，即可收集這些查詢的稽核記錄。詳情請參閱「[BigQuery 稽核記錄參考資料](https://docs.cloud.google.com/bigquery/docs/reference/auditlogs?hl=zh-tw)」。

## 為預留項目新增標籤

為預留項目新增標籤後，該標籤就會納入帳單資料。您可以使用標籤，篩選 Cloud Billing 資料中的 Analysis Slots Attribution SKU。

「數據分析運算單元歸因」SKU 只會記錄運算單元用量。不會記錄 BigQuery Reservation API SKU 的費用。BigQuery Reservation API SKU 不支援預留項目標籤做為篩選條件。

如要進一步瞭解如何在帳單資料中使用標籤，請參閱「[使用**篩選器**精細調整資料](https://docs.cloud.google.com/billing/docs/how-to/reports?hl=zh-tw#filter-by-labels)」。

### 必要的 IAM 角色

如要取得為預留項目新增標籤所需的權限，請要求管理員授予管理專案的 [BigQuery 資源編輯者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.resourceEditor)  (`roles/bigquery.resourceEditor`) IAM 角色。如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

這個預先定義的角色具備 `bigquery.reservations.update` 權限，可為預留項目新增標籤。

您或許還可透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)取得這項權限。

### 為預留項目新增標籤

如何為預訂資訊新增標籤：

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在導覽選單中，按一下「Workload management」(工作負載管理)。
3. 點選「Slot reservations」(運算單元預留項目) 分頁標籤。
4. 找出要更新的預訂。
5. 展開 more\_vert「Actions」(動作) 選項。
6. 按一下 [編輯]。
7. 如要展開「Advanced settings」(進階設定) 部分，請按一下expand\_more「expander arrow」(展開箭頭)。
8. 按一下「新增標籤」。
9. 在適當欄位中輸入鍵/值組合。如要套用其他標籤，請按一下「Add label」(新增標籤)。
10. 按一下 [儲存]。

### SQL

如要為預留項目新增標籤，請使用 [`ALTER RESERVATION SET OPTIONS` DDL 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#alter_reservation_set_options_statement)。這項操作會覆寫預留項目中的所有現有標籤。以下範例會為 `myreservation` 預留項目設定標籤：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列陳述式：

   ```
   ALTER RESERVATION myreservation
   SET OPTIONS (
     labels = [('sensitivity', 'high')]);
   ```
3. 按一下「play\_circle 執行」。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

### bq

如要為預留項目新增標籤，請使用 `bq update` 指令，並加上 `set_label` 旗標和 `--reservation` 旗標。如要新增多個標籤，請重複使用 `set_label` 旗標。

```
bq update --set_label KEY:VALUE --location LOCATION --reservation RESERVATION_NAME
```

更改下列內容：

* `KEY:VALUE`：要新增至預留項目的標籤鍵/值組合。鍵不得重複。鍵和值只能使用小寫字母、數字字元、底線和連字號。所有字元都必須使用 UTF-8 編碼，且可使用國際字元。如要為預留項目新增多個標籤，請重複 `--set_label` 旗標，並為每個標籤指定專屬鍵。
* `LOCATION`：預留項目的位置。`location` 旗標不能放在指令最後，否則會傳回 `FATAL Flags positioning` 錯誤。
* `RESERVATION_NAME`：預留項目名稱。

## 新增不含值的標籤

如果標籤的鍵值為空白，有時會稱為標記。請勿與[標記資源](https://docs.cloud.google.com/bigquery/docs/tags?hl=zh-tw)混淆。詳情請參閱「[標籤和標記](https://docs.cloud.google.com/resource-manager/docs/tags/tags-overview?hl=zh-tw)」。您可以建立不含值的新標籤，或移除現有標籤鍵的值。

如果想為資源加上標籤，但不需要鍵/值格式，則可使用不含值的標籤。舉例來說，如果資料表包含多個群組 (例如支援或開發) 使用的測試資料，您可以在資料表中新增 `test_data` 標籤來識別。

如要新增不含值的標籤，請按照下列步驟操作：

### 控制台

1. 在 Google Cloud 控制台中，選取適當的資源 (資料集、資料表或檢視表)。
2. 如果是資料集，系統會自動開啟資料集詳細資料頁面。如果是資料表和資料檢視，請按一下 [Details] (詳細資料) 以開啟詳細資料頁面。
3. 在詳細資料頁面的「Labels」(標籤) 部分，按一下 edit「Edit」(編輯)。
4. 在「Edit labels」(編輯標籤) 對話方塊中：

   * 按一下「新增標籤」。
   * 在適當欄位中輸入新鍵，並將值欄位留空。如要套用其他標籤，請按一下「Add label」(新增標籤)，然後重複上述步驟。
   * 點按「更新」以儲存變更。

### SQL

如要新增不含值的標籤，請使用 [`ALTER TABLE SET OPTIONS` DDL 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#alter_table_set_options_statement)：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列陳述式：

   ```
   ALTER TABLE mydataset.mytable
   SET OPTIONS (
     labels=[("key1", ""), ("key2", "")]);
   ```
3. 按一下「play\_circle 執行」。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

### bq

如要為現有資源新增不含值的標籤，請使用 `bq update` 指令並搭配 `set_label` 旗標。請指定鍵並在後面加入冒號，但不要指定值。

```
bq update --set_label KEY: RESOURCE_ID
```

更改下列內容：

* `KEY:`：要使用的標籤鍵。
* `RESOURCE_ID`：有效的資料集、資料表或檢視表名稱。如果資源位於預設專案以外的專案，請使用下列格式指定專案 ID：`PROJECT_ID:DATASET`。

範例：

使用下列指令，為 `mydataset.mytable` 建立 `test_data` 標籤。`mydataset` 在您的預設專案中。

```
bq update --set_label test_data: mydataset
```

### API

呼叫 [`datasets.patch`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/datasets/patch?hl=zh-tw) 方法或 [`tables.patch`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables/patch?hl=zh-tw) 方法，並在[資料集資源](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/datasets?hl=zh-tw)或[資料表資源](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables?hl=zh-tw)中加入值設為空字串 (`""`) 的標籤。如要移除現有標籤的值，請將值替換為空字串。

由於系統會將檢視表當做資料表資源處理，因此可以使用 `tables.patch` 方法來修改檢視表和資料表。此外，由於 `tables.update` 方法會取代整個資料集資源，因此請改用 `tables.patch` 方法。

## 後續步驟

* 瞭解如何在 BigQuery 資源中[查看標籤](https://docs.cloud.google.com/bigquery/docs/viewing-labels?hl=zh-tw)。
* 瞭解如何[使用標籤識別及分析代理產生的查詢](https://docs.cloud.google.com/bigquery/docs/conversational-analytics?hl=zh-tw#identify-agent-queries)。
* 瞭解如何在 BigQuery 資源中[更新標籤](https://docs.cloud.google.com/bigquery/docs/updating-labels?hl=zh-tw)。
* 瞭解如何[使用標籤篩選資源](https://docs.cloud.google.com/bigquery/docs/filtering-labels?hl=zh-tw)。
* 瞭解如何在 BigQuery 資源中[刪除標籤](https://docs.cloud.google.com/bigquery/docs/deleting-labels?hl=zh-tw)。
* 閱讀 Resource Manager 說明文件中的[使用標籤](https://docs.cloud.google.com/resource-manager/docs/using-labels?hl=zh-tw)相關說明。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-10-24 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-10-24 (世界標準時間)。"],[],[]]