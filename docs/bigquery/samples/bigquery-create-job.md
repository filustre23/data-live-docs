* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [範例](https://docs.cloud.google.com/bigquery/docs/samples?hl=zh-tw)

# 建立工作 透過集合功能整理內容 你可以依據偏好儲存及分類內容。

在指定位置執行 BigQuery 工作 (查詢、載入、擷取或複製)，並進行額外設定。

## 深入探索

如需包含這個程式碼範例的詳細說明文件，請參閱下列文章：

* [透過程式執行工作](https://docs.cloud.google.com/bigquery/docs/running-jobs?hl=zh-tw)

## 程式碼範例

### C#

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 C# 設定說明操作。詳情請參閱 [BigQuery C# API 參考說明文件](https://docs.cloud.google.com/dotnet/docs/reference/Google.Cloud.BigQuery.V2/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
using Google.Cloud.BigQuery.V2;
using System;
using System.Collections.Generic;

public class BigQueryCreateJob
{
    public BigQueryJob CreateJob(string projectId = "your-project-id")
    {
        string query = @"
            SELECT country_name from `bigquery-public-data.utility_us.country_code_iso";

        // Initialize client that will be used to send requests.
        BigQueryClient client = BigQueryClient.Create(projectId);

        QueryOptions queryOptions = new QueryOptions
        {
            JobLocation = "us",
            JobIdPrefix = "code_sample_",
            Labels = new Dictionary<string, string>
            {
                ["example-label"] = "example-value"
            },
            MaximumBytesBilled = 1000000
        };

        BigQueryJob queryJob = client.CreateQueryJob(
            sql: query,
            parameters: null,
            options: queryOptions);

        Console.WriteLine($"Started job: {queryJob.Reference.JobId}");
        return queryJob;
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

	"github.com/google/uuid"
)

// createJob demonstrates running an arbitrary SQL statement as a query job.
func createJob(projectID, sql string) error {
	// sql := "SELECT country_name from `bigquery-public-data.utility_us.country_code_iso`:"
	ctx := context.Background()
	client, err := bigquery.NewClient(ctx, projectID)
	if err != nil {
		return fmt.Errorf("bigquery.NewClient: %w", err)
	}
	defer client.Close()

	// Demonstrate adding a label to the job.
	q := client.Query(sql)
	q.Labels = map[string]string{"example-label": "example-value"}

	// The library will create job IDs for you automatically, but this can be overridden by
	// setting the Job ID explicitly.  Job IDs are unique within a project and cannot be
	// reused.
	q.JobID = fmt.Sprintf("my_job_prefix_%s", uuid.New().String())

	// Start job execution.
	job, err := q.Run(ctx)
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
import com.google.cloud.bigquery.Job;
import com.google.cloud.bigquery.JobId;
import com.google.cloud.bigquery.JobInfo;
import com.google.cloud.bigquery.QueryJobConfiguration;
import com.google.common.collect.ImmutableMap;
import java.util.UUID;

// Sample to create a job
public class CreateJob {

  public static void main(String[] args) {
    // TODO(developer): Replace these variables before running the sample.
    String query = "SELECT country_name from `bigquery-public-data.utility_us.country_code_iso`";
    createJob(query);
  }

  public static void createJob(String query) {
    try {
      // Initialize client that will be used to send requests. This client only needs to be created
      // once, and can be reused for multiple requests.
      BigQuery bigquery = BigQueryOptions.getDefaultInstance().getService();

      // Specify a job configuration to set optional job resource properties.
      QueryJobConfiguration queryConfig =
          QueryJobConfiguration.newBuilder(query)
              .setLabels(ImmutableMap.of("example-label", "example-value"))
              .build();

      // The location and job name are optional,
      // if both are not specified then client will auto-create.
      String jobName = "jobId_" + UUID.randomUUID().toString();
      JobId jobId = JobId.newBuilder().setLocation("us").setJob(jobName).build();

      // Create a job with job ID
      bigquery.create(JobInfo.of(jobId, queryConfig));

      // Get a job that was just created
      Job job = bigquery.getJob(jobId);
      if (job.getJobId().getJob().equals(jobId.getJob())) {
        System.out.print("Job created successfully." + job.getJobId().getJob());
      } else {
        System.out.print("Job was not created");
      }
    } catch (BigQueryException e) {
      System.out.print("Job was not created. \n" + e.toString());
    }
  }
}
```

### Node.js

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Node.js 設定說明操作。詳情請參閱 [BigQuery Node.js API 參考說明文件](https://googleapis.dev/nodejs/bigquery/latest/index.html)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
// Import the Google Cloud client library and create a client
const {BigQuery} = require('@google-cloud/bigquery');
const bigquery = new BigQuery();

async function createJob() {
  // Run a BigQuery query job.

  // For all options, see https://cloud.google.com/bigquery/docs/reference/rest/v2/Job
  const options = {
    // Specify a job configuration to set optional job resource properties.
    configuration: {
      query: {
        query: `SELECT country_name 
              FROM \`bigquery-public-data.utility_us.country_code_iso\` 
              LIMIT 10`,
        useLegacySql: false,
      },
      labels: {'example-label': 'example-value'},
    },
  };

  // Make API request.
  const response = await bigquery.createJob(options);
  const job = response[0];

  // Wait for the query to finish
  const [rows] = await job.getQueryResults(job);

  // Print the results
  console.log('Rows:');
  rows.forEach(row => console.log(row));
}
```

### Python

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Python 設定說明操作。詳情請參閱 [BigQuery Python API 參考說明文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
from google.cloud import bigquery

# Construct a BigQuery client object.
client = bigquery.Client()

query_job = client.create_job(
    # Specify a job configuration, providing a query
    # and/or optional job resource properties, as needed.
    # The job instance can be a LoadJob, CopyJob, ExtractJob, QueryJob
    # Here, we demonstrate a "query" job.
    # References:
    #     https://googleapis.dev/python/bigquery/latest/generated/google.cloud.bigquery.client.Client.html#google.cloud.bigquery.client.Client.create_job
    #     https://cloud.google.com/bigquery/docs/reference/rest/v2/Job
    #
    # Example use cases for .create_job() include:
    #    * to retry failed jobs
    #    * to generate jobs with an experimental API property that hasn't
    #      been added to one of the manually written job configuration
    #      classes yet
    #
    # NOTE: unless it is necessary to create a job in this way, the
    # preferred approach is to use one of the dedicated API calls:
    #   client.query()
    #   client.extract_table()
    #   client.copy_table()
    #   client.load_table_file(), client.load_table_from_dataframe(), etc
    job_config={
        "query": {
            "query": """
                     SELECT country_name
                     FROM `bigquery-public-data.utility_us.country_code_iso`
                     LIMIT 5
                     """,
        },
        "labels": {"example-label": "example-value"},
        "maximum_bytes_billed": 10000000,
    }
)  # Make an API request.

print(f"Started job: {query_job.job_id}")
```

## 後續步驟

如要搜尋及篩選其他 Google Cloud 產品的程式碼範例，請參閱[Google Cloud 範例瀏覽工具](https://docs.cloud.google.com/docs/samples?product=bigquery&hl=zh-tw)。

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。




[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],[],[],[]]