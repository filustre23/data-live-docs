Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [範例](https://docs.cloud.google.com/bigquery/docs/samples?hl=zh-tw)

# 將資料表匯出為壓縮檔 透過集合功能整理內容 你可以依據偏好儲存及分類內容。

將資料表匯出為 Cloud Storage 值區中的壓縮檔。

## 深入探索

如需包含這個程式碼範例的詳細說明文件，請參閱下列文章：

* [將資料表資料匯出至 Cloud Storage](https://docs.cloud.google.com/bigquery/docs/exporting-data?hl=zh-tw)

## 程式碼範例

### Go

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Go 設定說明操作。詳情請參閱 [BigQuery Go API 參考說明文件](https://godoc.org/cloud.google.com/go/bigquery)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import (
	"context"
	"fmt"

	"cloud.google.com/go/bigquery"
)

// exportTableAsCompressedCSV demonstrates using an export job to
// write the contents of a table into Cloud Storage as compressed CSV.
func exportTableAsCompressedCSV(projectID, gcsURI string) error {
	// projectID := "my-project-id"
	// gcsURI := "gs://mybucket/shakespeare.csv"
	ctx := context.Background()
	client, err := bigquery.NewClient(ctx, projectID)
	if err != nil {
		return fmt.Errorf("bigquery.NewClient: %w", err)
	}
	defer client.Close()

	srcProject := "bigquery-public-data"
	srcDataset := "samples"
	srcTable := "shakespeare"

	gcsRef := bigquery.NewGCSReference(gcsURI)
	gcsRef.Compression = bigquery.Gzip

	extractor := client.DatasetInProject(srcProject, srcDataset).Table(srcTable).ExtractorTo(gcsRef)
	extractor.DisableHeader = true
	// You can choose to run the job in a specific location for more complex data locality scenarios.
	// Ex: In this example, source dataset and GCS bucket are in the US.
	extractor.Location = "US"

	job, err := extractor.Run(ctx)
	if err != nil {
		return err
	}
	status, err := job.Wait(ctx)
	if err != nil {
		return err
	}
	if err := status.Err(); err != nil {
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
import com.google.cloud.bigquery.ExtractJobConfiguration;
import com.google.cloud.bigquery.Job;
import com.google.cloud.bigquery.JobInfo;
import com.google.cloud.bigquery.TableId;

// Sample to extract a compressed table
public class ExtractTableCompressed {

  public static void main(String[] args) {
    // TODO(developer): Replace these variables before running the sample.
    String projectName = "MY_PROJECT_NAME";
    String datasetName = "MY_DATASET_NAME";
    String tableName = "MY_TABLE_NAME";
    String bucketName = "MY-BUCKET-NAME";
    String destinationUri = "gs://" + bucketName + "/path/to/file";
    // For more information on export formats available see:
    // https://cloud.google.com/bigquery/docs/exporting-data#export_formats_and_compression_types
    String compressed = "gzip";
    // For more information on Job see:
    // https://googleapis.dev/java/google-cloud-clients/latest/index.html?com/google/cloud/bigquery/package-summary.html
    String dataFormat = "CSV";

    extractTableCompressed(
        projectName, datasetName, tableName, destinationUri, dataFormat, compressed);
  }

  public static void extractTableCompressed(
      String projectName,
      String datasetName,
      String tableName,
      String destinationUri,
      String dataFormat,
      String compressed) {
    try {
      // Initialize client that will be used to send requests. This client only needs to be created
      // once, and can be reused for multiple requests.
      BigQuery bigquery = BigQueryOptions.getDefaultInstance().getService();

      TableId tableId = TableId.of(projectName, datasetName, tableName);

      ExtractJobConfiguration extractConfig =
          ExtractJobConfiguration.newBuilder(tableId, destinationUri)
              .setCompression(compressed)
              .setFormat(dataFormat)
              .build();

      Job job = bigquery.create(JobInfo.of(extractConfig));

      // Blocks until this job completes its execution, either failing or succeeding.
      Job completedJob = job.waitFor();
      if (completedJob == null) {
        System.out.println("Job not executed since it no longer exists.");
        return;
      } else if (completedJob.getStatus().getError() != null) {
        System.out.println(
            "BigQuery was unable to extract due to an error: \n" + job.getStatus().getError());
        return;
      }
      System.out.println("Table extract compressed successful");
    } catch (BigQueryException | InterruptedException e) {
      System.out.println("Table extraction job was interrupted. \n" + e.toString());
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

const bigquery = new BigQuery();
const storage = new Storage();

async function extractTableCompressed() {
  // Exports my_dataset:my_table to gcs://my-bucket/my-file as a compressed file.

  /**
   * TODO(developer): Uncomment the following lines before running the sample.
   */
  // const datasetId = "my_dataset";
  // const tableId = "my_table";
  // const bucketName = "my-bucket";
  // const filename = "file.csv";

  // Location must match that of the source table.
  const options = {
    location: 'US',
    gzip: true,
  };

  // Export data from the table into a Google Cloud Storage file
  const [job] = await bigquery
    .dataset(datasetId)
    .table(tableId)
    .extract(storage.bucket(bucketName).file(filename), options);

  console.log(`Job ${job.id} created.`);

  // Check the job's status for errors
  const errors = job.status.errors;
  if (errors && errors.length > 0) {
    throw errors;
  }
}
```

### Python

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Python 設定說明操作。詳情請參閱 [BigQuery Python API 參考說明文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
# from google.cloud import bigquery
# client = bigquery.Client()
# bucket_name = 'my-bucket'

destination_uri = "gs://{}/{}".format(bucket_name, "shakespeare.csv.gz")
dataset_ref = bigquery.DatasetReference(project, dataset_id)
table_ref = dataset_ref.table("shakespeare")
job_config = bigquery.job.ExtractJobConfig()
job_config.compression = bigquery.Compression.GZIP

extract_job = client.extract_table(
    table_ref,
    destination_uri,
    # Location must match that of the source table.
    location="US",
    job_config=job_config,
)  # API request
extract_job.result()  # Waits for job to complete.
```

## 後續步驟

如要搜尋及篩選其他 Google Cloud 產品的程式碼範例，請參閱[Google Cloud 範例瀏覽工具](https://docs.cloud.google.com/docs/samples?product=bigquery&hl=zh-tw)。

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。




[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],[],[],[]]