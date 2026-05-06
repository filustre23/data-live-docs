Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [範例](https://docs.cloud.google.com/bigquery/docs/samples?hl=zh-tw)

# 將資料表匯出為 JSON 檔案 透過集合功能整理內容 你可以依據偏好儲存及分類內容。

將資料表匯出至 Cloud Storage bucket 中以換行符號分隔的 JSON 檔案。

## 程式碼範例

### C#

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 C# 設定說明操作。詳情請參閱 [BigQuery C# API 參考說明文件](https://docs.cloud.google.com/dotnet/docs/reference/Google.Cloud.BigQuery.V2/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
using Google.Cloud.BigQuery.V2;
using System;

public class BigQueryExtractTableJson
{
    public void ExtractTableJson(
        string projectId = "your-project-id",
        string bucketName = "your-bucket-name")
    {
        BigQueryClient client = BigQueryClient.Create(projectId);
        string destinationUri = $"gs://{bucketName}/shakespeare.json";
        var jobOptions = new CreateExtractJobOptions()
        {
            DestinationFormat = FileFormat.NewlineDelimitedJson
        };
        BigQueryJob job = client.CreateExtractJob(
            projectId: "bigquery-public-data",
            datasetId: "samples",
            tableId: "shakespeare",
            destinationUri: destinationUri,
            options: jobOptions
        );
        job = job.PollUntilCompleted().ThrowOnAnyError();  // Waits for the job to complete.
        Console.Write($"Exported table to {destinationUri}.");
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

// exportTableAsJSON demonstrates using an export job to
// write the contents of a table into Cloud Storage as newline delimited JSON.
func exportTableAsJSON(projectID, gcsURI string) error {
	// projectID := "my-project-id"
	// gcsURI := "gs://mybucket/shakespeare.json"
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
	gcsRef.DestinationFormat = bigquery.JSON

	extractor := client.DatasetInProject(srcProject, srcDataset).Table(srcTable).ExtractorTo(gcsRef)
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
import com.google.cloud.RetryOption;
import com.google.cloud.bigquery.BigQuery;
import com.google.cloud.bigquery.BigQueryException;
import com.google.cloud.bigquery.BigQueryOptions;
import com.google.cloud.bigquery.FormatOptions;
import com.google.cloud.bigquery.Job;
import com.google.cloud.bigquery.Table;
import com.google.cloud.bigquery.TableId;
import org.threeten.bp.Duration;

public class ExtractTableToJson {

  public static void main(String[] args) {
    // TODO(developer): Replace these variables before running the sample.
    String projectId = "bigquery-public-data";
    String datasetName = "samples";
    String tableName = "shakespeare";
    String bucketName = "my-bucket";
    String destinationUri = "gs://" + bucketName + "/path/to/file";
    // For more information on export formats available see:
    // https://cloud.google.com/bigquery/docs/exporting-data#export_formats_and_compression_types
    // For more information on Job see:
    // https://googleapis.dev/java/google-cloud-clients/latest/index.html?com/google/cloud/bigquery/package-summary.html

    // Note that FormatOptions.json().toString() is not "JSON" but "NEWLINE_DELIMITED_JSON"
    // Using FormatOptions Enum for this will prevent problems with unexpected format names.
    String dataFormat = FormatOptions.json().getType();

    extractTableToJson(projectId, datasetName, tableName, destinationUri, dataFormat);
  }

  // Exports datasetName:tableName to destinationUri as a JSON file
  public static void extractTableToJson(
      String projectId,
      String datasetName,
      String tableName,
      String destinationUri,
      String dataFormat) {
    try {
      // Initialize client that will be used to send requests. This client only needs to be created
      // once, and can be reused for multiple requests.
      BigQuery bigquery = BigQueryOptions.getDefaultInstance().getService();

      TableId tableId = TableId.of(projectId, datasetName, tableName);
      Table table = bigquery.getTable(tableId);

      Job job = table.extract(dataFormat, destinationUri);

      // Blocks until this job completes its execution, either failing or succeeding.
      Job completedJob =
          job.waitFor(
              RetryOption.initialRetryDelay(Duration.ofSeconds(1)),
              RetryOption.totalTimeout(Duration.ofMinutes(3)));
      if (completedJob == null) {
        System.out.println("Job not executed since it no longer exists.");
        return;
      } else if (completedJob.getStatus().getError() != null) {
        System.out.println(
            "BigQuery was unable to extract due to an error: \n" + job.getStatus().getError());
        return;
      }
      System.out.println(
          "Table export successful. Check in GCS bucket for the " + dataFormat + " file.");
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

async function extractTableJSON() {
  // Exports my_dataset:my_table to gcs://my-bucket/my-file as JSON.

  /**
   * TODO(developer): Uncomment the following lines before running the sample.
   */
  // const datasetId = "my_dataset";
  // const tableId = "my_table";
  // const bucketName = "my-bucket";
  // const filename = "file.json";

  // Location must match that of the source table.
  const options = {
    format: 'json',
    location: 'US',
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

destination_uri = "gs://{}/{}".format(bucket_name, "shakespeare.json")
dataset_ref = bigquery.DatasetReference(project, dataset_id)
table_ref = dataset_ref.table("shakespeare")
job_config = bigquery.job.ExtractJobConfig()
job_config.destination_format = bigquery.DestinationFormat.NEWLINE_DELIMITED_JSON

extract_job = client.extract_table(
    table_ref,
    destination_uri,
    job_config=job_config,
    # Location must match that of the source table.
    location="US",
)  # API request
extract_job.result()  # Waits for job to complete.
```

## 後續步驟

如要搜尋及篩選其他 Google Cloud 產品的程式碼範例，請參閱[Google Cloud 範例瀏覽工具](https://docs.cloud.google.com/docs/samples?product=bigquery&hl=zh-tw)。

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。




[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],[],[],[]]