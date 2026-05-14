Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 更新資料集屬性

本文說明如何在 BigQuery 中更新資料集屬性。建立資料集後，您可以更新下列資料集屬性：

* [計費模式](#update_storage_billing_models)
* 新資料表的預設[到期時間](#table-expiration)
* 新分區資料表的預設[分區到期時間](#partition-expiration)
* 新資料表的預設[捨入模式](#update_rounding_mode)
* [說明](#update-dataset-description)
* [標籤](https://docs.cloud.google.com/bigquery/docs/adding-using-labels?hl=zh-tw#adding_dataset_labels)
* [時間回溯期](#update_time_travel_windows)

## 事前準備

授予身分與存取權管理 (IAM) 角色，讓使用者擁有執行本文件各項工作所需的權限。

### 所需權限

如要更新資料集屬性，您需要下列 IAM 權限：

* `bigquery.datasets.update`
* `bigquery.datasets.setIamPolicy` (僅在 Google Cloud 控制台中更新資料集存取權控管設定時需要)

`roles/bigquery.dataOwner` 預先定義的 IAM 角色包含更新資料集屬性所需的權限。

此外，如果您具備 `bigquery.datasets.create` 權限，可以更新所建立資料集的屬性。

如要進一步瞭解 BigQuery 中的 IAM 角色和權限，請參閱[預先定義的角色與權限](https://docs.cloud.google.com/bigquery/access-control?hl=zh-tw)一文。

## 更新資料集說明

您可以透過下列方式更新資料集的說明：

* 使用 Google Cloud 控制台。
* 使用 bq 指令列工具的 `bq update` 指令。
* 呼叫 [`datasets.patch`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/datasets/patch?hl=zh-tw) API 方法
* 使用用戶端程式庫。

如要更新資料集的說明：

### 控制台

1. 點選左側窗格中的 explore「Explorer」。

   如果沒有看到左側窗格，請按一下 last\_page「Expand left pane」(展開左側窗格)，開啟窗格。
2. 在「Explorer」窗格中展開專案，按一下「Datasets」(資料集)，然後按一下資料集。
3. 在「詳細資料」窗格中，按一下「編輯詳細資料」mode\_edit
   ，編輯說明文字。

   在隨即顯示的「編輯詳細資料」對話方塊中，執行下列操作：

   1. 在「Description」(說明) 欄位中輸入說明，或編輯現有說明。
   2. 如要儲存新的說明文字，請按一下「儲存」。

### SQL

如要更新資料集的說明，請使用 [`ALTER SCHEMA SET OPTIONS` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#alter_schema_set_options_statement)設定 `description` 選項。

以下範例會為名為 `mydataset` 的資料集設定說明：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列陳述式：

   ```
    ALTER SCHEMA mydataset
    SET OPTIONS (
        description = 'Description of mydataset');
   ```
3. 按一下「執行」play\_circle。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

### bq

發出含有 `--description` 旗標的 `bq update` 指令。如果您要更新非預設專案中的資料集，請使用下列格式將專案 ID 新增至資料集名稱：`project_id:dataset`。

```
bq update \
--description "string" \
project_id:dataset
```

更改下列內容：

* `string`：描述資料集的文字 (以引號表示)
* `project_id`：專案 ID
* `dataset`：要更新的資料集名稱

範例：

輸入下列指令，將 `mydataset` 的說明變更為「Description of mydataset」(mydataset 的說明)。`mydataset` 在您的預設專案中。

```
bq update --description "Description of mydataset" mydataset
```

輸入下列指令，將 `mydataset` 的說明變更為「Description of mydataset」(mydataset 的說明)。該資料集位於 `myotherproject`，而非預設專案。

```
bq update \
--description "Description of mydataset" \
myotherproject:mydataset
```

### API

呼叫 [`datasets.patch`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/datasets/patch?hl=zh-tw) 並更新[資料集資源](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/datasets?hl=zh-tw)中的 `description` 屬性。由於 `datasets.update` 方法會取代整個資料集資源，因此建議使用 `datasets.patch` 方法。

### Go

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Go 設定說明操作。詳情請參閱 [BigQuery Go API 參考說明文件](https://godoc.org/cloud.google.com/go/bigquery)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import (
	"context"
	"fmt"

	"cloud.google.com/go/bigquery"
)

// updateDatasetDescription demonstrates how the Description metadata of a dataset can
// be read and modified.
func updateDatasetDescription(projectID, datasetID string) error {
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
	update := bigquery.DatasetMetadataToUpdate{
		Description: "Updated Description.",
	}
	if _, err = ds.Update(ctx, update, meta.ETag); err != nil {
		return err
	}
	return nil
}
```

### Java

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Java 設定說明操作。詳情請參閱 [BigQuery Java API 參考說明文件](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/overview?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

使用 [Dataset.toBuilder()](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/com.google.cloud.bigquery.Dataset?hl=zh-tw#com_google_cloud_bigquery_Dataset_toBuilder__) 方法，從現有的 [Dataset](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/com.google.cloud.bigquery.Dataset?hl=zh-tw) 執行個體建立 [Dataset.Builder](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/com.google.cloud.bigquery.Dataset.Builder?hl=zh-tw) 執行個體。設定資料集製作工具物件。使用 [Dataset.Builder.build()](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/com.google.cloud.bigquery.Dataset.Builder?hl=zh-tw#com_google_cloud_bigquery_Dataset_Builder_build__) 方法建構經過更新的資料集，並呼叫 [Dataset.update()](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/com.google.cloud.bigquery.Dataset?hl=zh-tw#com_google_cloud_bigquery_Dataset_update_com_google_cloud_bigquery_BigQuery_DatasetOption____) 方法，將更新傳送至 API。

```
import com.google.cloud.bigquery.BigQuery;
import com.google.cloud.bigquery.BigQueryException;
import com.google.cloud.bigquery.BigQueryOptions;
import com.google.cloud.bigquery.Dataset;

public class UpdateDatasetDescription {

  public static void runUpdateDatasetDescription() {
    // TODO(developer): Replace these variables before running the sample.
    String datasetName = "MY_DATASET_NAME";
    String newDescription = "this is the new dataset description";
    updateDatasetDescription(datasetName, newDescription);
  }

  public static void updateDatasetDescription(String datasetName, String newDescription) {
    try {
      // Initialize client that will be used to send requests. This client only needs to be created
      // once, and can be reused for multiple requests.
      BigQuery bigquery = BigQueryOptions.getDefaultInstance().getService();

      Dataset dataset = bigquery.getDataset(datasetName);
      bigquery.update(dataset.toBuilder().setDescription(newDescription).build());
      System.out.println("Dataset description updated successfully to " + newDescription);
    } catch (BigQueryException e) {
      System.out.println("Dataset description was not updated \n" + e.toString());
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

async function updateDatasetDescription() {
  // Updates a dataset's description.

  // Retreive current dataset metadata
  const dataset = bigquery.dataset(datasetId);
  const [metadata] = await dataset.getMetadata();

  // Set new dataset description
  const description = 'New dataset description.';
  metadata.description = description;

  const [apiResponse] = await dataset.setMetadata(metadata);
  const newDescription = apiResponse.description;

  console.log(`${datasetId} description: ${newDescription}`);
}
```

### Python

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Python 設定說明操作。詳情請參閱 [BigQuery Python API 參考說明文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

設定 [Dataset.description](https://docs.cloud.google.com/python/docs/reference/bigquery/latest/google.cloud.bigquery.dataset.Dataset?hl=zh-tw#google_cloud_bigquery_dataset_Dataset_description) 屬性，並呼叫 [Client.update\_dataset()](https://docs.cloud.google.com/python/docs/reference/bigquery/latest/google.cloud.bigquery.client.Client?hl=zh-tw#google_cloud_bigquery_client_Client_update_dataset) 方法，將更新傳送至 API。

```
from google.cloud import bigquery

# Construct a BigQuery client object.
client = bigquery.Client()

# TODO(developer): Set dataset_id to the ID of the dataset to fetch.
# dataset_id = 'your-project.your_dataset'

dataset = client.get_dataset(dataset_id)  # Make an API request.
dataset.description = "Updated description."
dataset = client.update_dataset(dataset, ["description"])  # Make an API request.

full_dataset_id = "{}.{}".format(dataset.project, dataset.dataset_id)
print(
    "Updated dataset '{}' with description '{}'.".format(
        full_dataset_id, dataset.description
    )
)
```

## 更新預設資料表的到期時間

您可以透過下列方式更新資料集的預設資料表到期時間：

* 使用 Google Cloud 控制台。
* 使用 bq 指令列工具的 `bq update` 指令。
* 呼叫 [`datasets.patch`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/datasets/patch?hl=zh-tw) API 方法
* 使用用戶端程式庫。

您可以設定資料集層級的預設資料表到期時間，也可以在建立資料表時設定資料表的到期時間。如果您在建立資料表時設定到期時間，系統將會忽略資料集的資料表預設到期時間。如果您未在資料集層級設定資料表的預設到期時間，也未在建立資料表時設定到期時間，則資料表將永遠不會過期，您必須以手動方式才能[刪除資料表](https://docs.cloud.google.com/bigquery/docs/managing-tables?hl=zh-tw#deleting_tables)。資料表過期後，系統會刪除該資料表和其中所有資料。

更新資料集的資料表預設到期時間設定時：

* 如果您將值從 `Never` 變更為定義好的到期時間，則除非在建立資料表時已為其設定了到期時間，否則資料集中已存在的任何資料表都不會到期。
* 如果您變更了資料表預設到期時間的值，則任何已存在的資料表都將根據原始的資料表到期時間設定到期。除非您在建立資料表時已為其指定不同的資料表到期時間，否則在資料集中建立的任何新資料表都會套用新的資料表到期時間設定。

資料表預設到期時間的值會依該值的設定位置而有不同的表示方式。請使用可為您提供適當精細層級的方法：

* 在 Google Cloud 控制台中，到期時間會以天為單位表示。
* 在 bq 指令列工具中，到期時間會以秒為單位表示。
* 在 API 中，到期時間會以毫秒為單位表示。

如何更新資料集的預設到期時間：

### 控制台

1. 點選左側窗格中的 explore「Explorer」。
2. 在「Explorer」窗格中展開專案，按一下「Datasets」(資料集)，然後按一下資料集。
3. 在「詳細資料」分頁中，按一下「編輯詳細資料」mode\_edit，即可編輯到期時間。
4. 在「Edit details」(編輯詳細資料) 對話方塊的「Default table expiration」(預設資料表到期時間) 區段中，選取「Enable table expiration」(啟用資料表到期時間)，然後輸入「Default maximum table age」(預設資料表存在時間長度上限) 的值。
5. 按一下 [儲存]。

### SQL

如要更新預設資料表到期時間，請使用 [`ALTER SCHEMA SET OPTIONS` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#alter_schema_set_options_statement)設定 `default_table_expiration_days` 選項。

以下範例會更新名為 `mydataset` 的資料集預設資料表到期時間。

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列陳述式：

   ```
    ALTER SCHEMA mydataset
    SET OPTIONS(
        default_table_expiration_days = 3.75);
   ```
3. 按一下「執行」play\_circle。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

### bq

如要更新資料集中新建立之資料表的預設到期時間，請輸入 `bq update` 指令並加上 `--default_table_expiration` 旗標。如果您要更新非預設專案中的資料集，請使用下列格式將專案 ID 新增至資料集名稱：`project_id:dataset`。

```
bq update \
--default_table_expiration integer \
project_id:dataset
```

更改下列內容：

* `integer`：新建立資料表的預設生命週期 (以秒為單位)。最小值是 3600 秒 (1 小時)。到期時間為目前世界標準時間加整數值。指定 `0` 即可移除現有的到期時間。在資料集中建立的任何資料表都會在建立時間後 `integer` 秒刪除。如果您未在[建立](https://docs.cloud.google.com/bigquery/docs/tables?hl=zh-tw#create-table)資料表時設定資料表到期時間，則會套用這個值。
* `project_id`：您的專案 ID。
* `dataset`：要更新的資料集名稱。

範例：

輸入下列指令，將在 `mydataset` 中建立之新資料表的預設到期時間設為距離目前時間兩小時 (7,200 秒)。該資料集位於預設專案中。

```
bq update --default_table_expiration 7200 mydataset
```

輸入下列指令，將在 `mydataset` 中建立之新資料表的預設到期時間設為距離目前時間兩小時 (7,200 秒)。該資料集位於 `myotherproject`，而非預設專案。

```
bq update --default_table_expiration 7200 myotherproject:mydataset
```

### API

呼叫 [`datasets.patch`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/datasets/patch?hl=zh-tw) 並更新[資料集資源](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/datasets?hl=zh-tw)中的 `defaultTableExpirationMs` 屬性。API 中的到期時間是以毫秒為單位表示。由於 `datasets.update` 方法會取代整個資料集的資源，因此建議您使用 `datasets.patch` 方法。

### Go

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Go 設定說明操作。詳情請參閱 [BigQuery Go API 參考說明文件](https://godoc.org/cloud.google.com/go/bigquery)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import (
	"context"
	"fmt"
	"time"

	"cloud.google.com/go/bigquery"
)

// updateDatasetDefaultExpiration demonstrats setting the default expiration of a dataset
// to a specific retention period.
func updateDatasetDefaultExpiration(projectID, datasetID string) error {
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
	update := bigquery.DatasetMetadataToUpdate{
		DefaultTableExpiration: 24 * time.Hour,
	}
	if _, err := client.Dataset(datasetID).Update(ctx, update, meta.ETag); err != nil {
		return err
	}
	return nil
}
```

### Java

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Java 設定說明操作。詳情請參閱 [BigQuery Java API 參考說明文件](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/overview?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

使用 [Dataset.toBuilder()](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/com.google.cloud.bigquery.Dataset?hl=zh-tw#com_google_cloud_bigquery_Dataset_toBuilder__) 方法，從現有的 [Dataset](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/com.google.cloud.bigquery.Dataset?hl=zh-tw) 執行個體建立 [Dataset.Builder](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/com.google.cloud.bigquery.Dataset.Builder?hl=zh-tw) 執行個體。設定資料集製作工具物件。使用 [Dataset.Builder.build()](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/com.google.cloud.bigquery.Dataset.Builder?hl=zh-tw#com_google_cloud_bigquery_Dataset_Builder_build__) 方法建構經過更新的資料集，並呼叫 [Dataset.update()](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/com.google.cloud.bigquery.Dataset?hl=zh-tw#com_google_cloud_bigquery_Dataset_update_com_google_cloud_bigquery_BigQuery_DatasetOption____) 方法，將更新傳送至 API。

使用 [Dataset.Builder.setDefaultTableLifetime()](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/com.google.cloud.bigquery.Dataset.Builder?hl=zh-tw#com_google_cloud_bigquery_Dataset_Builder_setDefaultTableLifetime_java_lang_Long_) 方法設定預設到期時間。

```
import com.google.cloud.bigquery.BigQuery;
import com.google.cloud.bigquery.BigQueryException;
import com.google.cloud.bigquery.BigQueryOptions;
import com.google.cloud.bigquery.Dataset;
import java.util.concurrent.TimeUnit;

public class UpdateDatasetExpiration {

  public static void runUpdateDatasetExpiration() {
    // TODO(developer): Replace these variables before running the sample.
    String datasetName = "MY_DATASET_NAME";
    updateDatasetExpiration(datasetName);
  }

  public static void updateDatasetExpiration(String datasetName) {
    try {
      // Initialize client that will be used to send requests. This client only needs to be created
      // once, and can be reused for multiple requests.
      BigQuery bigquery = BigQueryOptions.getDefaultInstance().getService();

      // Update dataset expiration to one day
      Long newExpiration = TimeUnit.MILLISECONDS.convert(1, TimeUnit.DAYS);

      Dataset dataset = bigquery.getDataset(datasetName);
      bigquery.update(dataset.toBuilder().setDefaultTableLifetime(newExpiration).build());
      System.out.println("Dataset description updated successfully to " + newExpiration);
    } catch (BigQueryException e) {
      System.out.println("Dataset expiration was not updated \n" + e.toString());
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

async function updateDatasetExpiration() {
  // Updates the lifetime of all tables in the dataset, in milliseconds.

  /**
   * TODO(developer): Uncomment the following lines before running the sample.
   */
  // const datasetId = "my_dataset";

  // Retreive current dataset metadata
  const dataset = bigquery.dataset(datasetId);
  const [metadata] = await dataset.getMetadata();

  // Set new dataset metadata
  const expirationTime = 24 * 60 * 60 * 1000;
  metadata.defaultTableExpirationMs = expirationTime.toString();

  const [apiResponse] = await dataset.setMetadata(metadata);
  const newExpirationTime = apiResponse.defaultTableExpirationMs;

  console.log(`${datasetId} expiration: ${newExpirationTime}`);
}
```

### Python

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Python 設定說明操作。詳情請參閱 [BigQuery Python API 參考說明文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

設定
[Dataset.default\_table\_expiration\_ms](https://docs.cloud.google.com/python/docs/reference/bigquery/latest/google.cloud.bigquery.dataset.Dataset?hl=zh-tw#google_cloud_bigquery_dataset_Dataset_default_table_expiration_ms)
屬性，並呼叫
[Client.update\_dataset()](https://docs.cloud.google.com/python/docs/reference/bigquery/latest/google.cloud.bigquery.client.Client?hl=zh-tw#google_cloud_bigquery_client_Client_update_dataset)
，將更新傳送至 API。

```
from google.cloud import bigquery

# Construct a BigQuery client object.
client = bigquery.Client()

# TODO(developer): Set dataset_id to the ID of the dataset to fetch.
# dataset_id = 'your-project.your_dataset'

dataset = client.get_dataset(dataset_id)  # Make an API request.
dataset.default_table_expiration_ms = 24 * 60 * 60 * 1000  # In milliseconds.

dataset = client.update_dataset(
    dataset, ["default_table_expiration_ms"]
)  # Make an API request.

full_dataset_id = "{}.{}".format(dataset.project, dataset.dataset_id)
print(
    "Updated dataset {} with new expiration {}".format(
        full_dataset_id, dataset.default_table_expiration_ms
    )
)
```

## 更新預設分區到期時間

您可以透過下列方式更新資料集的預設分區到期時間：

* 使用 bq 指令列工具的 `bq update` 指令。
* 呼叫 [`datasets.patch`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/datasets/patch?hl=zh-tw) API 方法
* 使用用戶端程式庫。

Google Cloud 控制台不支援設定或更新資料集的預設分區到期時間。

您可以在資料集層級設定預設分區到期時間，該設定會影響所有新建立的分區資料表，也可以在建立分區資料表時設定個別資料表的[分區到期](https://docs.cloud.google.com/bigquery/docs/managing-partitioned-tables?hl=zh-tw#partition-expiration)時間。如果您同時在資料集層級設定了預設分區到期時間和預設資料表到期時間，新建立的分區資料表只會套用分區到期時間。也就是說，如果您同時了設定這兩個選項，預設分區到期時間會覆寫預設資料表到期時間。

如果您在建立分區資料表時即設定了分區到期時間，該值會覆寫資料集層級的預設分區到期時間 (如有)。

如果您未設定資料集層級的預設分區到期時間，也未在建立資料表時設定分區到期時間，則分區永遠不會過期，直到您手動[刪除](#deleting_a_table)分區為止。

當您設定資料集的預設分區到期時間時，到期時間會套用至在資料集中建立之所有分區資料表中的所有分區。當您設定資料表的分區到期時間時，到期時間會套用至在指定資料表中建立的所有分區。您無法對同一資料表中不同的分區套用不同的到期時間。

更新資料集的預設分區到期時間設定時：

* 如果您將值從 `never` 變更為定義好的到期時間，則除非您在建立資料表時已為其設定分區到期時間，否則資料集中分區資料表內的任何既有分區都不會到期。
* 如果您變更了預設分區到期時間的值，既有分區資料表中的任何分區是否到期都將根據原始的分區到期時間設定到期。除非您在建立資料表時已為其指定不同的分區到期時間，否則在資料集中建立的任何新分區資料表都會套用新的預設分區到期時間設定。

預設分區到期時間的值會依該值的設定位置而有不同的表示方式。請使用可為您提供適當精細層級的方法：

* 在 bq 指令列工具中，到期時間會以秒為單位表示。
* 在 API 中，到期時間會以毫秒為單位表示。

如要更新資料集的預設分區到期時間：

### 控制台

Google Cloud 控制台不支援更新資料集的預設分區到期時間。

### SQL

如要更新預設分區到期時間，請使用 [`ALTER SCHEMA SET OPTIONS` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#alter_schema_set_options_statement)設定 `default_partition_expiration_days` 選項。

以下範例會更新名為 `mydataset` 的資料集預設分區到期時間：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列陳述式：

   ```
    ALTER SCHEMA mydataset
    SET OPTIONS(
        default_partition_expiration_days = 3.75);
   ```
3. 按一下「執行」play\_circle。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

### bq

如要更新資料集的預設到期時間，請輸入 `bq update` 指令並加上 `--default_partition_expiration` 旗標。如果您要更新非預設專案中的資料集，請使用下列格式將專案 ID 新增至資料集名稱：`project_id:dataset`。

```
bq update \
--default_partition_expiration integer \
project_id:dataset
```

更改下列內容：

* `integer`：新建立分區資料表中分區的預設生命週期 (以秒為單位)。此旗標沒有最小值。指定 `0` 即可移除現有的到期時間。新建立分區資料表中的任何分區都會在分區的世界標準時間日期起 `integer` 秒後刪除。如果您未在建立資料表時設定資料表的分區到期時間，則會套用這個值。
* `project_id`：您的專案 ID。
* `dataset`：要更新的資料集名稱。

範例：

輸入下列指令，將在 `mydataset` 中建立之新分區資料表的預設分區到期時間設定為 26 小時 (93,600 秒)。該資料集位於預設專案中。

```
bq update --default_partition_expiration 93600 mydataset
```

輸入下列指令，將在 `mydataset` 中建立之新分區資料表的預設分區到期時間設定為 26 小時 (93,600 秒)。該資料集位於 `myotherproject`，而非預設專案。

```
bq update --default_partition_expiration 93600 myotherproject:mydataset
```

### API

呼叫 [`datasets.patch`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/datasets/patch?hl=zh-tw) 並更新[資料集資源](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/datasets?hl=zh-tw)中的 `defaultPartitionExpirationMs` 屬性。到期時間會以毫秒為單位表示。由於 `datasets.update` 方法會取代整個資料集資源，因此建議使用 `datasets.patch` 方法。

## 更新捨入模式

您可以使用 [`ALTER SCHEMA SET OPTIONS` DDL 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#alter_schema_set_options_statement)，更新資料集的預設[捨入模式](https://docs.cloud.google.com/bigquery/docs/schemas?hl=zh-tw#rounding_mode)。以下範例會將 `mydataset` 的預設捨入模式更新為 `ROUND_HALF_EVEN`。

```
ALTER SCHEMA mydataset
SET OPTIONS (
  default_rounding_mode = "ROUND_HALF_EVEN");
```

這會為資料集中建立的新資料表設定預設捨入模式。不會影響新增至現有資料表的資料欄。如果資料集中的資料表已設定預設捨入模式，系統會覆寫這項選項。

## 更新時間回溯期

您可以透過下列方式更新資料集的時空旅行時間範圍：

* 使用 Google Cloud 控制台。
* 使用 [`ALTER SCHEMA SET OPTIONS`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#alter_schema_set_options_statement) 陳述式。
* 使用 bq 指令列工具的
  [`bq update`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_update) 指令。
* 呼叫 [`datasets.patch`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/datasets/patch?hl=zh-tw) 或 [`datasets.update`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/datasets/update?hl=zh-tw) API 方法。`update` 方法會取代整個資料集資源，而 `patch` 方法只會取代提交的資料集資源中提供的欄位。

如要進一步瞭解時間回溯視窗，請參閱「[設定時間回溯視窗](https://docs.cloud.google.com/bigquery/docs/time-travel?hl=zh-tw#configure_the_time_travel_window)」。

如要更新資料集的時間回溯期：

### 控制台

1. 點選左側窗格中的 explore「Explorer」。
2. 在「Explorer」窗格中展開專案，按一下「Datasets」(資料集)，然後按一下資料集。
3. 在「詳細資料」分頁中，按一下「編輯詳細資料」圖示 mode\_edit。
4. 展開「Advanced options」(進階選項)，然後選取要使用的「Time travel window」(時空旅行視窗)。
5. 按一下 [儲存]。

### SQL

使用 [`ALTER SCHEMA SET OPTIONS`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#alter_schema_set_options_statement) 陳述式和 `max_time_travel_hours` 選項，在變更資料集時指定時間旅行視窗。`max_time_travel_hours` 值必須是 24 的倍數 (48、72、96、120、144、168)，且介於 48 (2 天) 和 168 (7 天) 之間。

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列陳述式：

   ```
   ALTER SCHEMA DATASET_NAME
   SET OPTIONS(
     max_time_travel_hours = HOURS);
   ```

   更改下列內容：

   * `DATASET_NAME`：要更新的資料集名稱
   * `HOURS`，並以小時為單位指定時間回溯期的長度。
3. 按一下「執行」play\_circle。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

### bq

使用 [`bq update`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_update) 指令搭配 `--max_time_travel_hours` 旗標，在變更資料集時指定時空旅行時間範圍。`--max_time_travel_hours` 值必須是 24 的倍數 (48、72、96、120、144、168)，且介於 48 (2 天) 和 168 (7 天) 之間。

```
bq update \
--dataset=true --max_time_travel_hours=HOURS \
PROJECT_ID:DATASET_NAME
```

請替換下列項目：

* `PROJECT_ID`：專案 ID
* `DATASET_NAME`：要更新的資料集名稱
* `HOURS`，以小時為單位，表示時間回溯期的長度

### API

呼叫 [`datasets.patch`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/datasets/patch?hl=zh-tw) 或 [`datasets.update`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/datasets/update?hl=zh-tw) 方法，搭配已定義的[資料集資源](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/datasets?hl=zh-tw)，並在其中指定 `maxTimeTravelHours` 欄位的值。`maxTimeTravelHours` 值必須是 24 的倍數 (48、72、96、120、144、168)，且介於 48 (2 天) 和 168 (7 天) 之間。

## 更新儲存空間計費模式

您可以變更資料集的[儲存空間計費模式](https://docs.cloud.google.com/bigquery/docs/datasets-intro?hl=zh-tw#dataset_storage_billing_models)。將 `storage_billing_model` 值設為 `PHYSICAL`，即可在計算儲存空間變更時使用實體位元組；設為 `LOGICAL` 則可使用邏輯位元組。預設為 `LOGICAL`。

變更資料集的計費模式後，需要 24 小時才會生效。

變更資料集的儲存空間計費模式後，必須等待 14 天，才能再次變更儲存空間計費模式。

### 控制台

1. 點選左側窗格中的 explore「Explorer」。
2. 在「Explorer」窗格中展開專案，按一下「Datasets」(資料集)，然後按一下資料集。
3. 在「詳細資料」分頁中，按一下「編輯詳細資料」圖示 mode\_edit。
4. 展開「Advanced options」(進階選項)。
5. 在「儲存空間計費模式」選單中，選取「實體」即可使用實體儲存空間計費模式，選取「邏輯」即可使用邏輯儲存空間計費模式。您也可以選取「Storage\_billing\_model\_unspecified」**Storage\_billing\_model\_unspecified**。
6. 按一下 [儲存]。

### SQL

如要更新資料集的帳單模式，請使用 [`ALTER SCHEMA SET OPTIONS` 陳述式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language?hl=zh-tw#alter_schema_set_options_statement)，並設定 `storage_billing_model` 選項：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中輸入下列陳述式：

   ```
   ALTER SCHEMA DATASET_NAME
   SET OPTIONS(
    storage_billing_model = 'BILLING_MODEL');
   ```

   更改下列內容：

   * `DATASET_NAME`，並換成您要變更的資料集名稱
   * `BILLING_MODEL`，選擇要使用的儲存空間類型，可以是 `LOGICAL` 或 `PHYSICAL`
3. 按一下「執行」play\_circle。

如要進一步瞭解如何執行查詢，請參閱「[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)」。

如要更新專案中所有資料集的儲存空間計費模式，請針對每個資料集所在的區域使用下列 SQL 查詢：

```
FOR record IN
 (SELECT CONCAT(catalog_name, '.', schema_name) AS dataset_path
 FROM PROJECT_ID.region-REGION.INFORMATION_SCHEMA.SCHEMATA)
DO
 EXECUTE IMMEDIATE
   "ALTER SCHEMA `" || record.dataset_path || "` SET OPTIONS(storage_billing_model = 'BILLING_MODEL')";
END FOR;
```

更改下列內容：

* 將 `PROJECT_ID` 改成您的專案 ID
* `REGION`，並加上[區域限定符](https://docs.cloud.google.com/bigquery/docs/information-schema-intro?hl=zh-tw#region_qualifier)
* `BILLING_MODEL`，選擇要使用的儲存空間類型，可以是 `LOGICAL` 或 `PHYSICAL`

### bq

如要更新資料集的計費模式，請使用 [`bq update` 指令](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_update)並設定 `--storage_billing_model` 旗標：

```
bq update -d --storage_billing_model=BILLING_MODEL PROJECT_ID:DATASET_NAME
```

請替換下列項目：

* `PROJECT_ID`：專案 ID
* `DATASET_NAME`：要更新的資料集名稱
* `BILLING_MODEL`：要使用的儲存空間類型，可以是 `LOGICAL` 或 `PHYSICAL`

### API

使用已定義的[資料集資源](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/datasets?hl=zh-tw)呼叫 [`datasets.update` 方法](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/datasets/update?hl=zh-tw)，並設定 `storageBillingModel` 欄位。

以下範例說明如何使用 `curl` 呼叫 `datasets.update`：

```
curl -H "Authorization: Bearer $(gcloud auth print-access-token)" -H "Content-Type: application/json" -L -X PUT https://bigquery.googleapis.com/bigquery/v2/projects/PROJECT_ID/datasets/DATASET_ID -d '{"datasetReference": {"projectId": "PROJECT_ID", "datasetId": "DATASET_NAME"}, "storageBillingModel": "BILLING_MODEL"}'
```

請替換下列項目：

* `PROJECT_ID`：專案 ID
* `DATASET_NAME`：要更新的資料集名稱
* `BILLING_MODEL`：要使用的儲存空間類型，可以是 `LOGICAL` 或 `PHYSICAL`

## 更新存取權控管設定

如要在 BigQuery 中控管資料集存取權，請參閱「[控管資料集存取權](https://docs.cloud.google.com/bigquery/docs/control-access-to-resources-iam?hl=zh-tw)」。如要瞭解資料加密，請參閱「[靜態資料加密](https://docs.cloud.google.com/bigquery/docs/encryption-at-rest?hl=zh-tw)」。

## 後續步驟

* 如要進一步瞭解如何建立資料集，請參閱[建立資料集](https://docs.cloud.google.com/bigquery/docs/datasets?hl=zh-tw)一文。
* 如要進一步瞭解如何管理資料集，請參閱[管理資料集](https://docs.cloud.google.com/bigquery/docs/managing-datasets?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-14 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-14 (世界標準時間)。"],[],[]]