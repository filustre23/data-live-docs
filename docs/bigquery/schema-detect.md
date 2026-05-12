Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 使用結構定義自動偵測功能

## 結構定義自動偵測

BigQuery 結構定義自動偵測功能可推斷 CSV、JSON 或 Google 試算表資料的結構定義。無論是要將資料[載入](https://docs.cloud.google.com/bigquery/docs/loading-data?hl=zh-tw) BigQuery 或是查詢[外部資料來源](https://docs.cloud.google.com/bigquery/external-data-sources?hl=zh-tw)，您都可以使用結構定義自動偵測功能。

啟用自動偵測功能後，BigQuery 會推斷每一欄的資料類型。BigQuery 會隨機選擇資料來源中的檔案，並掃描最多前 500 個資料列來當做代表性樣本。BigQuery 接著會檢查每個欄位，並嘗試根據樣本中的值為各欄位指派資料類型。如果資料欄中的所有資料列都是空白，自動偵測功能會將該資料欄的資料類型預設為 `STRING`。

如果未針對 CSV、JSON 或 Google 試算表資料啟用結構定義自動偵測功能，建立資料表時就必須手動提供結構定義。

Avro、Parquet、ORC、Firestore 匯出檔或 Datastore 匯出檔案都屬於自述式檔案，這些檔案格式是自述式，因此 BigQuery 會自動根據來源資料推論出資料表結構定義。如果是 Parquet、Avro 和 Orc 檔案，您可以選擇提供明確的結構定義，覆寫推斷的結構定義。

您可以透過下列方式查看資料表的結構定義偵測結果：

* 使用 Google Cloud 控制台。
* 使用 bq 指令列工具的 [`bq show`](https://docs.cloud.google.com/bigquery/bq-command-line-tool?hl=zh-tw#tables) 指令。

當 BigQuery 偵測到結構定義時，可能會在極少數情況下更改欄位名稱，這是為了要配合 GoogleSQL 的語法。

如要進一步瞭解資料類型轉換，請參閱以下資訊：

* 在從 Datastore 載入資料時進行[資料類型轉換](https://docs.cloud.google.com/bigquery/docs/loading-data-cloud-datastore?hl=zh-tw#data_type_conversion)
* 在從 Firestore 載入資料時進行[資料類型轉換](https://docs.cloud.google.com/bigquery/docs/loading-data-cloud-firestore?hl=zh-tw#data_type_conversion)
* [Avro 轉換](https://docs.cloud.google.com/bigquery/docs/loading-data-cloud-storage-avro?hl=zh-tw#avro_conversions)
* [Parquet 轉換](https://docs.cloud.google.com/bigquery/docs/loading-data-cloud-storage-parquet?hl=zh-tw#parquet_conversions)
* [ORC 轉換](https://docs.cloud.google.com/bigquery/docs/loading-data-cloud-storage-orc?hl=zh-tw#orc_conversions)

## 使用結構定義自動偵測功能載入資料

如要在載入資料時啟用結構定義自動偵測功能，請使用下列任一方法：

* 在 Google Cloud 控制台的「Schema」(結構定義) 區段中，針對「Auto detect」(自動偵測) 勾選「Schema and input parameters」(結構定義和輸入參數) 選項。
* 在 bq 指令列工具中，使用 `bq load` 指令搭配 `--autodetect` 參數。

啟用結構定義自動偵測功能後，BigQuery 會盡可能嘗試自動推導 CSV 和 JSON 檔案的結構定義。自動偵測邏輯會讀取最多前 500 個資料列，推斷結構定義欄位類型。如果存在 `--skip_leading_rows` 標記，系統會略過前導行。欄位類型會根據欄位最多的資料列而定。
因此，只要至少有一列資料包含所有欄位的值，自動偵測功能就會正常運作。

結構定義自動偵測功能不適用於 Avro 檔案、Parquet 檔案、ORC 檔案、Firestore 匯出檔案或 Datastore 匯出檔案。您將這些檔案載入至 BigQuery 時，系統會透過自述式來源資料自動擷取資料表結構定義。

如何在載入 JSON 和 CSV 資料時使用結構定義自動偵測功能：

### 控制台

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。

   如果沒有看到左側窗格，請按一下「展開左側窗格」圖示 last\_page 開啟窗格。
3. 在「Explorer」窗格中展開專案，按一下「Datasets」(資料集)，然後按一下資料集。
4. 在詳細資料窗格中，按一下 add\_box「建立資料表」。
5. 在「Create table」(建立資料表) 頁面的「Source」(來源) 區段中：

   * 在「Create table from」(使用下列資料建立資料表) 部分，選取來源類型。
   * 在「Source」(來源) 欄位中，瀏覽檔案/Cloud Storage 值區，或輸入 [Cloud Storage URI](#gcs-uri)。請注意， Google Cloud 控制台中無法加入多個 URI，但支援使用[萬用字元](https://docs.cloud.google.com/bigquery/docs/batch-loading-data?hl=zh-tw#load-wildcards)。Cloud Storage 值區的位置必須與待建立資料表所在的資料集位置相同。
   * 在「File format」(檔案格式) 部分，選取 [CSV]  或 [JSON]。
6. 在「Create table」(建立資料表) 頁面的「Destination」(目的地) 區段中：

   * 在「Dataset name」(資料集名稱) 部分選擇適當的資料集。
   * 在「Table name」(資料表名稱) 欄位中，輸入您建立資料表時所使用的名稱。
   * 確認「Table type」(資料表類型) 已設為「Native table」(原生資料表)。
7. 點選「建立資料表」。

### bq

發出 `bq load` 指令並搭配使用 `--autodetect` 參數。

(選用) 提供 `--location` 旗標，並將值設為您的[位置](https://docs.cloud.google.com/bigquery/docs/dataset-locations?hl=zh-tw)。

下方指令會使用結構定義自動偵測功能載入檔案：

```
bq --location=LOCATION load \
--autodetect \
--source_format=FORMAT \
DATASET.TABLE \
PATH_TO_SOURCE
```

更改下列內容：

* `LOCATION`：位置名稱。`--location` 是選用旗標。舉例來說，如果您在東京地區使用 BigQuery，請將該旗標的值設定為 `asia-northeast1`。您可以使用 [.bigqueryrc 檔案](https://docs.cloud.google.com/bigquery/docs/bq-command-line-tool?hl=zh-tw#setting_default_values_for_command-line_flags)設定位置的預設值。
* `FORMAT`：`NEWLINE_DELIMITED_JSON` 或 `CSV`。
* `DATASET`：特定資料集，該資料集包含您要在當中載入資料的資料表。
* `TABLE`：您要載入資料的資料表名稱。
* `PATH_TO_SOURCE`：是 CSV 或 JSON 檔案的位置。

範例：

輸入下列指令，可將 `myfile.csv` 從您的本機載入至儲存於 `mydataset` 資料集內名稱為 `mytable` 的資料表。

```
bq load --autodetect --source_format=CSV mydataset.mytable ./myfile.csv
```

輸入下列指令，可將 `myfile.json` 從您的本機載入至儲存於 `mydataset` 資料集內名稱為 `mytable` 的資料表。

```
bq load --autodetect --source_format=NEWLINE_DELIMITED_JSON \
mydataset.mytable ./myfile.json
```

### API

1. 建立指向來源資料的 `load` 工作。如要瞭解如何建立工作，請參閱「[透過程式執行 BigQuery 工作](https://docs.cloud.google.com/bigquery/docs/running-jobs?hl=zh-tw)」。在 `jobReference` 區段的 `location` 屬性中指定您的位置。
2. 設定 `sourceFormat` 屬性來指定資料格式。如要使用結構定義自動偵測功能，這個值必須設為 `NEWLINE_DELIMITED_JSON` 或 `CSV`。
3. 使用 `autodetect` 屬性將結構定義自動偵測功能設為 `true`。

### Go

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Go 設定說明操作。詳情請參閱 [BigQuery Go API 參考說明文件](https://godoc.org/cloud.google.com/go/bigquery)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import (
	"context"
	"fmt"

	"cloud.google.com/go/bigquery"
)

// importJSONAutodetectSchema demonstrates loading data from newline-delimited JSON data in Cloud Storage
// and using schema autodetection to identify the available columns.
func importJSONAutodetectSchema(projectID, datasetID, tableID string) error {
	// projectID := "my-project-id"
	// datasetID := "mydataset"
	// tableID := "mytable"
	ctx := context.Background()
	client, err := bigquery.NewClient(ctx, projectID)
	if err != nil {
		return fmt.Errorf("bigquery.NewClient: %v", err)
	}
	defer client.Close()

	gcsRef := bigquery.NewGCSReference("gs://cloud-samples-data/bigquery/us-states/us-states.json")
	gcsRef.SourceFormat = bigquery.JSON
	gcsRef.AutoDetect = true
	loader := client.Dataset(datasetID).Table(tableID).LoaderFrom(gcsRef)
	loader.WriteDisposition = bigquery.WriteEmpty

	job, err := loader.Run(ctx)
	if err != nil {
		return err
	}
	status, err := job.Wait(ctx)
	if err != nil {
		return err
	}

	if status.Err() != nil {
		return fmt.Errorf("job completed with error: %v", status.Err())
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
import com.google.cloud.bigquery.FormatOptions;
import com.google.cloud.bigquery.Job;
import com.google.cloud.bigquery.JobInfo;
import com.google.cloud.bigquery.LoadJobConfiguration;
import com.google.cloud.bigquery.TableId;

// Sample to load JSON data with autodetect schema from Cloud Storage into a new BigQuery table
public class LoadJsonFromGCSAutodetect {

  public static void runLoadJsonFromGCSAutodetect() {
    // TODO(developer): Replace these variables before running the sample.
    String datasetName = "MY_DATASET_NAME";
    String tableName = "MY_TABLE_NAME";
    String sourceUri = "gs://cloud-samples-data/bigquery/us-states/us-states.json";
    loadJsonFromGCSAutodetect(datasetName, tableName, sourceUri);
  }

  public static void loadJsonFromGCSAutodetect(
      String datasetName, String tableName, String sourceUri) {
    try {
      // Initialize client that will be used to send requests. This client only needs to be created
      // once, and can be reused for multiple requests.
      BigQuery bigquery = BigQueryOptions.getDefaultInstance().getService();

      TableId tableId = TableId.of(datasetName, tableName);
      LoadJobConfiguration loadConfig =
          LoadJobConfiguration.newBuilder(tableId, sourceUri)
              .setFormatOptions(FormatOptions.json())
              .setAutodetect(true)
              .build();

      // Load data from a GCS JSON file into the table
      Job job = bigquery.create(JobInfo.of(loadConfig));
      // Blocks until this load table job completes its execution, either failing or succeeding.
      job = job.waitFor();
      if (job.isDone()) {
        System.out.println("Json Autodetect from GCS successfully loaded in a table");
      } else {
        System.out.println(
            "BigQuery was unable to load into the table due to an error:"
                + job.getStatus().getError());
      }
    } catch (BigQueryException | InterruptedException e) {
      System.out.println("Column not added during load append \n" + e.toString());
    }
  }
}
```

```
import com.google.cloud.bigquery.BigQuery;
import com.google.cloud.bigquery.BigQueryException;
import com.google.cloud.bigquery.BigQueryOptions;
import com.google.cloud.bigquery.CsvOptions;
import com.google.cloud.bigquery.Job;
import com.google.cloud.bigquery.JobInfo;
import com.google.cloud.bigquery.LoadJobConfiguration;
import com.google.cloud.bigquery.TableId;

// Sample to load CSV data with autodetect schema from Cloud Storage into a new BigQuery table
public class LoadCsvFromGcsAutodetect {

  public static void main(String[] args) {
    // TODO(developer): Replace these variables before running the sample.
    String datasetName = "MY_DATASET_NAME";
    String tableName = "MY_TABLE_NAME";
    String sourceUri = "gs://cloud-samples-data/bigquery/us-states/us-states.csv";
    loadCsvFromGcsAutodetect(datasetName, tableName, sourceUri);
  }

  public static void loadCsvFromGcsAutodetect(
      String datasetName, String tableName, String sourceUri) {
    try {
      // Initialize client that will be used to send requests. This client only needs to be created
      // once, and can be reused for multiple requests.
      BigQuery bigquery = BigQueryOptions.getDefaultInstance().getService();

      TableId tableId = TableId.of(datasetName, tableName);

      // Skip header row in the file.
      CsvOptions csvOptions = CsvOptions.newBuilder().setSkipLeadingRows(1).build();

      LoadJobConfiguration loadConfig =
          LoadJobConfiguration.newBuilder(tableId, sourceUri)
              .setFormatOptions(csvOptions)
              .setAutodetect(true)
              .build();

      // Load data from a GCS CSV file into the table
      Job job = bigquery.create(JobInfo.of(loadConfig));
      // Blocks until this load table job completes its execution, either failing or succeeding.
      job = job.waitFor();
      if (job.isDone() && job.getStatus().getError() == null) {
        System.out.println("CSV Autodetect from GCS successfully loaded in a table");
      } else {
        System.out.println(
            "BigQuery was unable to load into the table due to an error:"
                + job.getStatus().getError());
      }
    } catch (BigQueryException | InterruptedException e) {
      System.out.println("Column not added during load append \n" + e.toString());
    }
  }
}
```

### Node.js

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Node.js 設定說明操作。詳情請參閱 [BigQuery Node.js API 參考說明文件](https://googleapis.dev/nodejs/bigquery/latest/index.html)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
// Import the Google Cloud client libraries
const {BigQuery} = require('@google-cloud/bigquery');
const {Storage} = require('@google-cloud/storage');

/**
 * TODO(developer): Uncomment the following lines before running the sample.
 */
// const datasetId = "my_dataset";
// const tableId = "my_table";

/**
 * This sample loads the JSON file at
 * https://storage.googleapis.com/cloud-samples-data/bigquery/us-states/us-states.json
 *
 * TODO(developer): Replace the following lines with the path to your file.
 */
const bucketName = 'cloud-samples-data';
const filename = 'bigquery/us-states/us-states.json';

async function loadJSONFromGCSAutodetect() {
  // Imports a GCS file into a table with autodetected schema.

  // Instantiate clients
  const bigquery = new BigQuery();
  const storage = new Storage();

  // Configure the load job. For full list of options, see:
  // https://cloud.google.com/bigquery/docs/reference/rest/v2/Job#JobConfigurationLoad
  const metadata = {
    sourceFormat: 'NEWLINE_DELIMITED_JSON',
    autodetect: true,
    location: 'US',
  };

  // Load data from a Google Cloud Storage file into the table
  const [job] = await bigquery
    .dataset(datasetId)
    .table(tableId)
    .load(storage.bucket(bucketName).file(filename), metadata);
  // load() waits for the job to finish
  console.log(`Job ${job.id} completed.`);

  // Check the job's status for errors
  const errors = job.status.errors;
  if (errors && errors.length > 0) {
    throw errors;
  }
}
loadJSONFromGCSAutodetect();
```

### PHP

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 PHP 設定說明操作。詳情請參閱 [BigQuery PHP API 參考說明文件](https://docs.cloud.google.com/php/docs/reference/cloud-bigquery/latest/BigQueryClient?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
use Google\Cloud\BigQuery\BigQueryClient;

/**
 * Imports data to the given table from json file present in GCS by auto
 * detecting options and schema.
 *
 * @param string $projectId The project Id of your Google Cloud Project.
 * @param string $datasetId The BigQuery dataset ID.
 * @param string $tableId The BigQuery table ID.
 */
function import_from_storage_json_autodetect(
    string $projectId,
    string $datasetId,
    string $tableId = 'us_states'
): void {
    // instantiate the bigquery table service
    $bigQuery = new BigQueryClient([
      'projectId' => $projectId,
    ]);
    $dataset = $bigQuery->dataset($datasetId);
    $table = $dataset->table($tableId);

    // create the import job
    $gcsUri = 'gs://cloud-samples-data/bigquery/us-states/us-states.json';
    $loadConfig = $table->loadFromStorage($gcsUri)->autodetect(true)->sourceFormat('NEWLINE_DELIMITED_JSON');
    $job = $table->runJob($loadConfig);

    // check if the job is complete
    $job->reload();
    if (!$job->isComplete()) {
        throw new \Exception('Job has not yet completed', 500);
    }
    // check if the job has errors
    if (isset($job->info()['status']['errorResult'])) {
        $error = $job->info()['status']['errorResult']['message'];
        printf('Error running job: %s' . PHP_EOL, $error);
    } else {
        print('Data imported successfully' . PHP_EOL);
    }
}
```

### Python

如要啟用結構定義自動偵測功能，請將 [LoadJobConfig.autodetect](https://docs.cloud.google.com/python/docs/reference/bigquery/latest/google.cloud.bigquery.job.LoadJobConfig?hl=zh-tw#google_cloud_bigquery_job_LoadJobConfig_autodetect) 屬性設為 `True`。

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Python 設定說明操作。詳情請參閱 [BigQuery Python API 參考說明文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
from google.cloud import bigquery

# Construct a BigQuery client object.
client = bigquery.Client()

# TODO(developer): Set table_id to the ID of the table to create.
# table_id = "your-project.your_dataset.your_table_name

# Set the encryption key to use for the destination.
# TODO: Replace this key with a key you have created in KMS.
# kms_key_name = "projects/{}/locations/{}/keyRings/{}/cryptoKeys/{}".format(
#     "cloud-samples-tests", "us", "test", "test"
# )
job_config = bigquery.LoadJobConfig(
    autodetect=True, source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON
)
uri = "gs://cloud-samples-data/bigquery/us-states/us-states.json"
load_job = client.load_table_from_uri(
    uri, table_id, job_config=job_config
)  # Make an API request.
load_job.result()  # Waits for the job to complete.
destination_table = client.get_table(table_id)
print("Loaded {} rows.".format(destination_table.num_rows))
```

### Ruby

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Ruby 設定說明操作。詳情請參閱 [BigQuery Ruby API 參考說明文件](https://googleapis.dev/ruby/google-cloud-bigquery/latest/Google/Cloud/Bigquery.html)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
require "google/cloud/bigquery"

def load_table_gcs_json_autodetect dataset_id = "your_dataset_id"
  bigquery = Google::Cloud::Bigquery.new
  dataset  = bigquery.dataset dataset_id
  gcs_uri  = "gs://cloud-samples-data/bigquery/us-states/us-states.json"
  table_id = "us_states"

  load_job = dataset.load_job table_id,
                              gcs_uri,
                              format:     "json",
                              autodetect: true
  puts "Starting job #{load_job.job_id}"

  load_job.wait_until_done! # Waits for table load to complete.
  puts "Job finished."

  table = dataset.table table_id
  puts "Loaded #{table.rows_count} rows to table #{table.id}"
end
```

## 自動偵測外部資料來源的結構定義

結構定義自動偵測功能適用於 CSV、JSON 和 Google 試算表外部資料來源。啟用結構定義自動偵測功能後，BigQuery 會盡可能嘗試從來源資料自動推斷結構定義。如果未為這些來源啟用結構定義自動偵測功能，就必須提供明確的結構定義。

查詢外部 Avro、Parquet、ORC、Firestore 匯出或 Datastore 匯出檔案時，不需要啟用結構定義自動偵測功能。這些檔案格式為自述式，因此 BigQuery 會自動根據來源資料推論出資料表結構定義。如果是 Parquet、Avro 和 ORC 檔案，您可以選擇提供明確的結構定義，覆寫推斷的結構定義。

使用 Google Cloud 控制台時，您可以勾選「Auto detect」(自動偵測) 的「Schema and input parameters」(結構定義和輸入參數) 選項，啟用結構定義自動偵測功能。

使用 bq 指令列工具時，您可以在為 CSV、JSON 或 Google 試算表資料建立[資料表定義檔](https://docs.cloud.google.com/bigquery/external-table-definition?hl=zh-tw)時，啟用結構定義自動偵測功能。使用 bq 工具建立資料表定義檔時，請將 `--autodetect` 標記傳送至 `mkdef` 指令，以啟用結構定義自動偵測功能，或傳送 `--noautodetect` 標記來停用自動偵測。

當您使用 `--autodetect` 旗標時，資料表定義檔中的 `autodetect` 設定會設為 `true`。當您使用 `--noautodetect` 旗標時，資料表定義檔中的 `autodetect` 設定會設為 `false`。如果您在建立資料表定義時，沒有提供外部資料來源的結構定義，而且未使用 `--noautodetect` 或 `--autodetect` 旗標，則 `autodetect` 設定會預設為 `true`。

當您使用 API 建立資料表定義檔時，請將 `autodetect` 屬性值設為 `true` 或 `false`。將 `autodetect` 設為 `true` 可啟用自動偵測功能；將 `autodetect` 設為 `false` 則可停用自動偵測功能。

## 自動偵測詳細資料

除了偵測結構定義詳細資料外，自動偵測功能還可識別以下內容：

### 壓縮

BigQuery 在開啟檔案時，可識別與 gzip 相容的檔案壓縮格式。

### 日期和時間值

BigQuery 會根據來源資料的格式偵測日期和時間值。

`DATE` 欄中的值必須採用 `YYYY-MM-DD` 格式。

`TIME` 欄中的值必須採用以下格式：`HH:MM:SS[.SSSSSS]` (秒數的小數部分為選填)。

對於 `TIMESTAMP` 欄，BigQuery 可偵測多種時間戳記格式，包括但不限於以下格式：

* `YYYY-MM-DD HH:MM`
* `YYYY-MM-DD HH:MM:SS`
* `YYYY-MM-DD HH:MM:SS.SSSSSS`
* `YYYY/MM/DD HH:MM`

時間戳記也可包含 UTC 偏移或 UTC 區域指定元 (「Z」)。

以下是 BigQuery 會自動偵測為時間戳記值的範例：

* 2018-08-19 12:11
* 2018-08-19 12:11:35.22
* 2018/08/19 12:11
* 2018-08-19 07:11:35.220 -05:00

如果未啟用自動偵測功能，且值採用上述範例未列出的格式，則 BigQuery 只能將資料欄載入為 `STRING` 資料類型。您可以啟用自動偵測功能，讓 BigQuery 將這些資料欄辨識為時間戳記。舉例來說，如果啟用自動偵測功能，BigQuery 只會將 `2025-06-16T16:55:22Z` 載入為時間戳記。

或者，您也可以先預先處理來源資料，再載入資料。舉例來說，如果您要從試算表匯出 CSV 資料，請將日期格式設為與這裡顯示的其中一個範例相符。您也可以在將資料載入 BigQuery 後進行轉換。

### 自動偵測 CSV 資料的結構定義

#### CSV 分隔符號

BigQuery 可偵測以下分隔符號：

* 半形逗號 ( , )
* 管線符號 ( | )
* 定位點 ( \t )

#### CSV 標頭

BigQuery 會將檔案的第一個資料列與檔案中的其他資料列做比較，藉此推測出標題。如果第一行只包含字串，但其他行包含其他資料類型，BigQuery 會假設第一個資料列是標題資料列。BigQuery 會根據標題列中的欄位名稱指派資料欄名稱。系統可能會修改名稱，以符合 BigQuery 資料欄的[命名規則](https://docs.cloud.google.com/bigquery/docs/schemas?hl=zh-tw#column_names)。例如，空格會替換為底線。

否則，BigQuery 會將第一列視為資料列，並指派一般資料欄名稱，例如 `string_field_1`。請注意，資料表建立完成後，您無法在結構定義中更新資料欄名稱，但可以[手動變更名稱](https://docs.cloud.google.com/bigquery/docs/manually-changing-schemas?hl=zh-tw#changing_a_columns_name)。您也可以提供明確的結構定義，而非使用自動偵測功能。

您可能會有包含標題列的 CSV 檔案，其中所有資料欄位都是字串。在這種情況下，BigQuery 不會自動偵測到第一列是標題。使用 `--skip_leading_rows` 選項可略過標題列。否則系統會將標頭匯入為資料。此外，也請考慮在此情況下提供明確的結構定義，以便指派資料欄名稱。

#### CSV 引用的新行

BigQuery 會偵測 CSV 欄位內引用的新行字元，但不會將引用的新行字元解讀為資料列邊界。

### 自動偵測 JSON 資料的結構定義

#### JSON 巢狀和重複欄位

BigQuery 會推斷 JSON 檔案中的巢狀和重複欄位。如果欄位值是 JSON 物件，BigQuery 會將該資料欄載入為 `RECORD` 型別。如果欄位值是陣列，BigQuery 會將該欄位載入為重複欄位。如需包含巢狀和重複資料的 JSON 資料範例，請參閱「[載入巢狀和重複的 JSON 資料](https://docs.cloud.google.com/bigquery/docs/loading-data-cloud-storage-json?hl=zh-tw#loading_nested_and_repeated_json_data)」。

#### 字串轉換

如果啟用結構定義自動偵測功能，BigQuery 會盡可能將字串轉換為布林值、數值或日期/時間類型。舉例來說，使用下列 JSON 資料時，結構定義自動偵測功能會將 `id` 欄位轉換為 `INTEGER` 資料欄：

```
{ "name":"Alice","id":"12"}
{ "name":"Bob","id":"34"}
{ "name":"Charles","id":"45"}
```

詳情請參閱[從 Cloud Storage 載入 JSON 資料](https://docs.cloud.google.com/bigquery/docs/loading-data-cloud-storage-json?hl=zh-tw)。

### 自動偵測 Google 試算表的結構定義

如果是試算表，BigQuery 會自動偵測第一列是否為標題列，與 CSV 檔案的自動偵測方式類似。如果第一行是標題，BigQuery 會根據標題列中的欄位名稱指派資料欄名稱，並略過該列。系統可能會修改名稱，以符合 BigQuery 中資料欄的[命名規則](https://docs.cloud.google.com/bigquery/docs/schemas?hl=zh-tw#column_names)。例如，空格會替換為底線。

## 表格安全性

如要控管 BigQuery 資料表的存取權，請參閱「[使用 IAM 控管資源存取權](https://docs.cloud.google.com/bigquery/docs/control-access-to-resources-iam?hl=zh-tw)」。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-11 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-11 (世界標準時間)。"],[],[]]