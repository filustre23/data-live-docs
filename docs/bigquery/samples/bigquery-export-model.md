Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [範例](https://docs.cloud.google.com/bigquery/docs/samples?hl=zh-tw)

# 匯出模型 透過集合功能整理內容 你可以依據偏好儲存及分類內容。

將現有模型匯出至現有 Cloud Storage bucket。

## 深入探索

如需包含這個程式碼範例的詳細說明文件，請參閱下列文章：

* [匯出模型](https://docs.cloud.google.com/bigquery/docs/exporting-models?hl=zh-tw)

## 程式碼範例

### C#

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 C# 設定說明操作。詳情請參閱 [BigQuery C# API 參考說明文件](https://docs.cloud.google.com/dotnet/docs/reference/Google.Cloud.BigQuery.V2/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
using Google.Cloud.BigQuery.V2;
using System;

public class BigQueryExtractModel
{
    public void ExtractModel(string projectId, string datasetId, string modelId, string destinationUri)
    {
        BigQueryClient client = BigQueryClient.Create(projectId);
        BigQueryJob job = client.CreateModelExtractJob(
            projectId: projectId,
            datasetId: datasetId,
            modelId: modelId,
            destinationUri: destinationUri
        );
        job = job.PollUntilCompleted().ThrowOnAnyError();  // Waits for the job to complete.
        System.IO.File.AppendAllText("log.txt", $"Exported model to {destinationUri}");
        Console.Write($"Exported model to {destinationUri}");
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

// exportModel demonstrates how to export an existing
// BigQuery ML Model to Google Cloud Storage.
func exportModel(projectID, datasetID, modelID, gcsURI string) error {
	// projectID := "my-project-id"
	// datasetID := "dataset-id"
	// modelID := "model-id"
	// gcsURI := "gs://mybucket/path/to/model"
	ctx := context.Background()
	client, err := bigquery.NewClient(ctx, projectID)
	if err != nil {
		return fmt.Errorf("bigquery.NewClient: %w", err)
	}
	defer client.Close()

	gcsRef := bigquery.NewGCSReference(gcsURI)

	extractor := client.DatasetInProject(projectID, datasetID).Model(modelID).ExtractorTo(gcsRef)
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
import com.google.cloud.bigquery.ModelId;

// Sample to extract model to GCS bucket
public class ExtractModel {

  public static void main(String[] args) throws InterruptedException {
    // TODO(developer): Replace these variables before running the sample.
    String projectName = "bigquery-public-data";
    String datasetName = "samples";
    String modelName = "model";
    String bucketName = "MY-BUCKET-NAME";
    String destinationUri = "gs://" + bucketName + "/path/to/file";
    extractModel(projectName, datasetName, modelName, destinationUri);
  }

  public static void extractModel(
      String projectName, String datasetName, String modelName, String destinationUri)
      throws InterruptedException {
    try {
      // Initialize client that will be used to send requests. This client only needs to be created
      // once, and can be reused for multiple requests.
      BigQuery bigquery = BigQueryOptions.getDefaultInstance().getService();

      ModelId modelId = ModelId.of(projectName, datasetName, modelName);

      ExtractJobConfiguration extractConfig =
          ExtractJobConfiguration.newBuilder(modelId, destinationUri).build();

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
      System.out.println("Model extract successful");
    } catch (BigQueryException ex) {
      System.out.println("Model extraction job was interrupted. \n" + ex.toString());
    }
  }
}
```

### Ruby

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Ruby 設定說明操作。詳情請參閱 [BigQuery Ruby API 參考說明文件](https://googleapis.dev/ruby/google-cloud-bigquery/latest/Google/Cloud/Bigquery.html)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
require "google/cloud/bigquery"

##
# Exports a model to a Google Cloud Storage bucket.
#
# @param dataset_id [String] The ID of the dataset that contains the model.
# @param model_id   [String] The ID of the model to export.
# @param destination_uri [String] The Google Cloud Storage bucket to export the model to.
def export_model dataset_id, model_id, destination_uri
  bigquery = Google::Cloud::Bigquery.new
  dataset = bigquery.dataset dataset_id
  model = dataset.model model_id

  puts "Extracting model #{model.model_id} to #{destination_uri}"
  job = model.extract_job destination_uri
  job.wait_until_done!

  if job.failed?
    puts "Error extracting model: #{job.error}"
  else
    puts "Model extracted successfully"
  end
end
```

## 後續步驟

如要搜尋及篩選其他 Google Cloud 產品的程式碼範例，請參閱[Google Cloud 範例瀏覽工具](https://docs.cloud.google.com/docs/samples?product=bigquery&hl=zh-tw)。

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。




[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],[],[],[]]