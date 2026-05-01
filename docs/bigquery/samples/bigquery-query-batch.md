* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [範例](https://docs.cloud.google.com/bigquery/docs/samples?hl=zh-tw)

# 以批次做為優先順序執行查詢 透過集合功能整理內容 你可以依據偏好儲存及分類內容。

以批次優先順序執行查詢工作。

## 深入探索

如需包含這個程式碼範例的詳細說明文件，請參閱下列文章：

* [執行查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw)

## 程式碼範例

### Go

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Go 設定說明操作。詳情請參閱 [BigQuery Go API 參考說明文件](https://godoc.org/cloud.google.com/go/bigquery)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import (
	"context"
	"fmt"
	"io"
	"time"

	"cloud.google.com/go/bigquery"
)

// queryBatch demonstrates issuing a query job using batch priority.
func queryBatch(w io.Writer, projectID, dstDatasetID, dstTableID string) error {
	// projectID := "my-project-id"
	// dstDatasetID := "mydataset"
	// dstTableID := "mytable"
	ctx := context.Background()
	client, err := bigquery.NewClient(ctx, projectID)
	if err != nil {
		return fmt.Errorf("bigquery.NewClient: %w", err)
	}
	defer client.Close()

	// Build an aggregate table.
	q := client.Query(`
		SELECT
  			corpus,
  			SUM(word_count) as total_words,
  			COUNT(1) as unique_words
		FROM ` + "`bigquery-public-data.samples.shakespeare`" + `
		GROUP BY corpus;`)
	q.Priority = bigquery.BatchPriority
	q.QueryConfig.Dst = client.Dataset(dstDatasetID).Table(dstTableID)

	// Start the job.
	job, err := q.Run(ctx)
	if err != nil {
		return err
	}
	// Job is started and will progress without interaction.
	// To simulate other work being done, sleep a few seconds.
	time.Sleep(5 * time.Second)
	status, err := job.Status(ctx)
	if err != nil {
		return err
	}

	state := "Unknown"
	switch status.State {
	case bigquery.Pending:
		state = "Pending"
	case bigquery.Running:
		state = "Running"
	case bigquery.Done:
		state = "Done"
	}
	// You can continue to monitor job progress until it reaches
	// the Done state by polling periodically.  In this example,
	// we print the latest status.
	fmt.Fprintf(w, "Job %s in Location %s currently in state: %s\n", job.ID(), job.Location(), state)

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
import com.google.cloud.bigquery.QueryJobConfiguration;
import com.google.cloud.bigquery.TableResult;

// Sample to query batch in a table
public class QueryBatch {

  public static void main(String[] args) {
    // TODO(developer): Replace these variables before running the sample.
    String projectId = "MY_PROJECT_ID";
    String datasetName = "MY_DATASET_NAME";
    String tableName = "MY_TABLE_NAME";
    String query =
        "SELECT corpus"
            + " FROM `"
            + projectId
            + "."
            + datasetName
            + "."
            + tableName
            + " GROUP BY corpus;";
    queryBatch(query);
  }

  public static void queryBatch(String query) {
    try {
      // Initialize client that will be used to send requests. This client only needs to be created
      // once, and can be reused for multiple requests.
      BigQuery bigquery = BigQueryOptions.getDefaultInstance().getService();

      QueryJobConfiguration queryConfig =
          QueryJobConfiguration.newBuilder(query)
              // Run at batch priority, which won't count toward concurrent rate limit.
              .setPriority(QueryJobConfiguration.Priority.BATCH)
              .build();

      TableResult results = bigquery.query(queryConfig);

      results
          .iterateAll()
          .forEach(row -> row.forEach(val -> System.out.printf("%s,", val.toString())));

      System.out.println("Query batch performed successfully.");
    } catch (BigQueryException | InterruptedException e) {
      System.out.println("Query batch not performed \n" + e.toString());
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

async function queryBatch() {
  // Runs a query at batch priority.

  // Create query job configuration. For all options, see
  // https://cloud.google.com/bigquery/docs/reference/rest/v2/Job#jobconfigurationquery
  const queryJobConfig = {
    query: `SELECT corpus
            FROM \`bigquery-public-data.samples.shakespeare\` 
            LIMIT 10`,
    useLegacySql: false,
    priority: 'BATCH',
  };

  // Create job configuration. For all options, see
  // https://cloud.google.com/bigquery/docs/reference/rest/v2/Job#jobconfiguration
  const jobConfig = {
    // Specify a job configuration to set optional job resource properties.
    configuration: {
      query: queryJobConfig,
    },
  };

  // Make API request.
  const [job] = await bigquery.createJob(jobConfig);

  const jobId = job.metadata.id;
  const state = job.metadata.status.state;
  console.log(`Job ${jobId} is currently in state ${state}`);
}
```

### Python

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Python 設定說明操作。詳情請參閱 [BigQuery Python API 參考說明文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
from google.cloud import bigquery

# Construct a BigQuery client object.
client = bigquery.Client()

job_config = bigquery.QueryJobConfig(
    # Run at batch priority, which won't count toward concurrent rate limit.
    priority=bigquery.QueryPriority.BATCH
)

sql = """
    SELECT corpus
    FROM `bigquery-public-data.samples.shakespeare`
    GROUP BY corpus;
"""

# Start the query, passing in the extra configuration.
query_job = client.query(sql, job_config=job_config)  # Make an API request.

# Check on the progress by getting the job's updated state. Once the state
# is `DONE`, the results are ready.
query_job = typing.cast(
    "bigquery.QueryJob",
    client.get_job(
        query_job.job_id, location=query_job.location
    ),  # Make an API request.
)

print("Job {} is currently in state {}".format(query_job.job_id, query_job.state))
```

## 後續步驟

如要搜尋及篩選其他 Google Cloud 產品的程式碼範例，請參閱[Google Cloud 範例瀏覽工具](https://docs.cloud.google.com/docs/samples?product=bigquery&hl=zh-tw)。

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。




[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],[],[],[]]