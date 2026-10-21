Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [範例](https://docs.cloud.google.com/bigquery/docs/samples?hl=zh-tw)

# 取得工作屬性 透過集合功能整理內容 你可以依據偏好儲存及分類內容。

擷取指定工作 ID 的工作屬性。

## 深入探索

如需包含這個程式碼範例的詳細說明文件，請參閱下列文章：

* [管理工作](https://docs.cloud.google.com/bigquery/docs/managing-jobs?hl=zh-tw)

## 程式碼範例

### Go

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Go 設定說明操作。詳情請參閱 [BigQuery Go API 參考說明文件](https://godoc.org/cloud.google.com/go/bigquery)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import (
	"context"
	"fmt"
	"io"

	"cloud.google.com/go/bigquery"
)

// getJobInfo demonstrates retrieval of a job, which can be used to monitor
// completion or print metadata about the job.
func getJobInfo(w io.Writer, projectID, jobID string) error {
	// projectID := "my-project-id"
	// jobID := "my-job-id"
	ctx := context.Background()

	client, err := bigquery.NewClient(ctx, projectID)
	if err != nil {
		return fmt.Errorf("bigquery.NewClient: %w", err)
	}
	defer client.Close()

	job, err := client.JobFromID(ctx, jobID)
	if err != nil {
		return err
	}

	status := job.LastStatus()
	state := "Unknown"
	switch status.State {
	case bigquery.Pending:
		state = "Pending"
	case bigquery.Running:
		state = "Running"
	case bigquery.Done:
		state = "Done"
	}
	fmt.Fprintf(w, "Job %s was created %v and is in state %s\n",
		jobID, status.Statistics.CreationTime, state)
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

// Sample to get a job
public class GetJob {

  public static void main(String[] args) {
    // TODO(developer): Replace these variables before running the sample.
    String jobName = "MY_JOB_NAME";
    getJob(jobName);
  }

  public static void getJob(String jobName) {
    try {
      // Initialize client that will be used to send requests. This client only needs to be created
      // once, and can be reused for multiple requests.
      BigQuery bigquery = BigQueryOptions.getDefaultInstance().getService();

      JobId jobId = JobId.of(jobName);
      Job job = bigquery.getJob(jobId);
      System.out.println("Job retrieved successfully");
    } catch (BigQueryException e) {
      System.out.println("Job not retrieved. \n" + e.toString());
    }
  }
}
```

### Python

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Python 設定說明操作。詳情請參閱 [BigQuery Python API 參考說明文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
from google.cloud import bigquery


def get_job(
    client: bigquery.Client,
    location: str = "us",
    job_id: str = "abcd-efgh-ijkl-mnop",
) -> None:
    job = client.get_job(job_id, location=location)

    # All job classes have "location" and "job_id" string properties.
    # Use these properties for job operations such as "cancel_job" and
    # "delete_job".
    print(f"{job.location}:{job.job_id}")
    print(f"Type: {job.job_type}")
    print(f"State: {job.state}")
    print(f"Created: {job.created.isoformat()}")
```

### Rust

```
use google_cloud_bigquery_v2::client::JobService;

pub async fn sample(project_id: &str, job_id: &str) -> anyhow::Result<()> {
    let job_service = JobService::builder().build().await?;
    let job = job_service
        .get_job()
        .set_project_id(project_id)
        .set_job_id(job_id)
        .send()
        .await?;

    if let Some(job_ref) = job.job_reference {
        println!("Job ID: {}", job_ref.job_id);
    }

    if let Some(status) = job.status {
        println!("State: {:?}", status.state);
    }

    if let Some(stats) = job.statistics {
        println!("Creation Time: {:?}", stats.creation_time);
        println!("End Time: {:?}", stats.end_time);
        if let Some(q_stats) = stats.query {
            println!("Total Bytes Processed: {:?}", q_stats.total_bytes_processed);
        }
    }

    Ok(())
}
```

## 後續步驟

如要搜尋及篩選其他 Google Cloud 產品的程式碼範例，請參閱[Google Cloud 範例瀏覽工具](https://docs.cloud.google.com/docs/samples?product=bigquery&hl=zh-tw)。

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。




[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],[],[],[]]