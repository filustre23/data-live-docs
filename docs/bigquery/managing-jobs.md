Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 管理工作機會

本文說明如何在 BigQuery 中管理工作，包括如何[查看工作詳細資料](#view-job)、[列出工作](#list_jobs_in_a_project)、[取消工作](#cancel_jobs)、[重複執行工作](#repeat_jobs)，以及[刪除工作中繼資料](#delete_job_metadata)。

## 關於 BigQuery 工作

每當您[載入](https://docs.cloud.google.com/bigquery/docs/loading-data?hl=zh-tw)、[匯出](https://docs.cloud.google.com/bigquery/exporting-data-from-bigquery?hl=zh-tw)、[查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw)或[複製資料](https://docs.cloud.google.com/bigquery/docs/managing-tables?hl=zh-tw#copy-table)時，BigQuery 會自動建立、排定及執行工作，追蹤工作進度。

因為工作可能需要長時間才能完成，所以會非同步執行，而且可以輪詢其狀態。執行時間較短的動作 (如列出資源或取得中繼資料) 不會以工作形式管理。

提交工作時，可能會有下列其中一種狀態：

* `PENDING`：工作已排定，等待執行。
* `RUNNING`：工作正在進行中。
* `DONE`：工作已完成。如果工作失敗，系統會顯示 [JobStatus.errorResult](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#JobStatus.FIELDS.error_result)。

### 配額

如需深入瞭解工作配額，請參閱「[配額與限制](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)」頁面中工作類型的說明文件：

* [載入工作](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#load_jobs)
* [複製工作](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#copy_jobs)
* [擷取工作](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#export_jobs)
* [查詢工作](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw#query_jobs)

### 定價

每個工作都與您指定的特定專案相關聯。因工作而產生的任何使用量，均會向連接相關專案的帳單帳戶收取費用。如果您分享專案的存取權，則在該專案中執行的任何工作均會向帳單帳戶收費。

舉例來說，執行查詢工作時，費用會計入執行該工作的專案。因此，若看到格式為 `<project_id>:<region>.<job_id>` 的查詢工作 ID，`project_id` 就是負責支付該查詢費用的專案 ID。

詳情請參閱「[定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw)」。

## 事前準備

授予 Identity and Access Management (IAM) 角色，讓使用者擁有執行本文中各項工作所需的權限。

### 必要的角色

如要取得執行及管理作業所需的權限，請要求管理員在專案中授予您下列 IAM 角色：

* BigQuery 工作使用者 (`roles/bigquery.jobUser`)：執行或重複執行工作、列出工作、查看工作詳細資料，以及取消工作。
* BigQuery 使用者 (`roles/bigquery.user`) - 執行或重複執行工作、列出工作、查看工作詳細資料，以及取消工作 (這個角色的權限比 BigQuery 工作使用者更寬鬆)。
* BigQuery 資源管理員 (`roles/bigquery.resourceAdmin`) - 列出所有工作，並擷取任何工作的中繼資料。
* BigQuery 管理員 (`roles/bigquery.admin`)：列出所有工作、擷取任何工作的中繼資料，以及取消任何工作。

如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

這些預先定義的角色具備執行及管理工作所需的權限。如要查看確切的必要權限，請展開「Required permissions」(必要權限) 部分：

#### 所需權限

如要執行及管理工作，必須具備下列權限：

* `bigquery.jobs.create`
  專案，即可執行或重複執行工作，並列出您的工作。
* `bigquery.jobs.get`
  專案，即可查看任何工作的元資料。
* `bigquery.jobs.update`
  專案，即可取消任何工作。
* `bigquery.jobs.listAll`
  機構、資料夾或專案，即可列出所有工作，並擷取任何使用者所提交之任何工作的中繼資料。如要查看所有工作的詳細資料，也必須具備 `bigquery.jobs.list` 權限。
* `bigquery.jobs.list`
  專案，即可列出所有工作，並擷取任何使用者所提交之任何工作的中繼資料。系統會遮蓋由其他使用者所提交工作的詳細資料和中繼資料。
* `bigquery.jobs.listExecutionMetadata`
  ，列出任何使用者提交的所有工作執行中繼資料 (不含機密資訊)。
* `bigquery.jobs.update`
  專案，即可取消任何工作。
* `bigquery.jobs.delete`
  即可刪除任何工作。

您或許還可透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)取得這些權限。

如要進一步瞭解 BigQuery 中的 IAM 角色和權限，請參閱[預先定義的角色和權限](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)一文。

## 查看工作詳細資料

您可以使用 Google Cloud 控制台、bq 指令列工具、API 或用戶端程式庫，查看工作詳細資料。詳細資料包括資料和中繼資料，例如工作類型、工作狀態，以及建立工作的使用者。

如要查看工作詳細資料，請按照下列步驟操作：

### 控制台

1. 前往「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。

   如果沒有看到左側窗格，請按一下 last\_page「Expand left pane」(展開左側窗格)，開啟窗格。
3. 在「Explorer」窗格中，按一下「Job history」。
4. 選取要查看的工作記錄類型：

   * 如要顯示近期工作資訊，請按一下「Personal history」(個人記錄)。
   * 如要顯示專案中近期工作資訊，請按一下「專案記錄」。
5. 如要查看工作詳細資料，請按一下工作。

   **注意：** 工作時間長度的計算方式為結束時間減去開始時間 (而非建立時間)。

### bq

發出 [`bq show`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_show) 指令並搭配使用 `--job=true` 旗標和工作 ID。

當您提供工作 ID 時，可以使用完整 ID 或簡短格式。舉例來說，在 Google Cloud 控制台中列出的工作 ID 都是完整名稱，也就是包含專案和位置：

`my-project-1234:US.bquijob_123x456_123y123z123c`

在指令列工具中列出的工作 ID 採用簡短格式。其中不含專案 ID 和位置：

`bquijob_123x456_123y123z123c`

如要指定工作位置，請提供 `--location` 標記，並將值設為您的[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)。如果您使用完整工作 ID，則不一定要提供標記。如果您加入 `--location` 標記且使用的是完整工作 ID，則系統會忽略 `--location` 標記。

以下指令要求工作的相關資訊：

```
bq --location=LOCATION show --job=true JOB_ID
```

更改下列內容：

* `LOCATION`：執行工作的位置名稱。舉例來說，如果您在東京區域使用 BigQuery，請將該旗標的值設定為 `asia-northeast1`。您可以使用 [`.bigqueryrc` 檔案](https://docs.cloud.google.com/bigquery/docs/bq-command-line-tool?hl=zh-tw#setting_default_values_for_command-line_flags)設定位置的預設值。如果未在工作 ID 中指定位置，或使用 `--location` 標記，系統會使用預設位置。
* `JOB_ID`：工作 ID

**範例**

下列指令可取得在 `myproject` 中執行的 `US.bquijob_123x456_123y123z123c` 工作摘要資訊：

```
bq show --job=true myproject:US.bquijob_123x456_123y123z123c
```

輸出結果會與下列內容相似：

```
 Job Type    State      Start Time      Duration      User Email       Bytes Processed   Bytes Billed   Billing Tier   Labels
 ---------- --------- ----------------- ---------- ------------------- ----------------- -------------- -------------- --------
 extract    SUCCESS   06 Jul 11:32:10   0:01:41    user@example.com
```

如要查看完整的工作詳細資料，請輸入下列指令：

```
bq show --format=prettyjson --job=true myproject:US.bquijob_123x456_789y123z456c
```

輸出結果會與下列內容相似：

```
{
  "configuration": {
    "extract": {
      "compression": "NONE",
      "destinationUri": "[URI removed]",
      "destinationUris": [
        "[URI removed]"
      ],
      "sourceTable": {
        "datasetId": "github_repos",
        "projectId": "bigquery-public-data",
        "tableId": "commits"
      }
    }
  },
  "etag": "\"[etag removed]\"",
  "id": "myproject:bquijob_123x456_789y123z456c",
  "jobReference": {
    "jobId": "bquijob_123x456_789y123z456c",
    "projectId": "[Project ID removed]"
  },
  "kind": "bigquery#job",
  "selfLink": "https://bigquery.googleapis.com/bigquery/v2/projects/federated-testing/jobs/bquijob_123x456_789y123z456c",
  "statistics": {
    "creationTime": "1499365894527",
    "endTime": "1499365894702",
    "startTime": "1499365894702"
  },
  "status": {
    "errorResult": {
      "debugInfo": "[Information removed for readability]",
      "message": "Operation cannot be performed on a nested schema. Field: author",
      "reason": "invalid"
    },
    "errors": [
      {
        "message": "Operation cannot be performed on a nested schema. Field: author",
        "reason": "invalid"
      }
    ],
    "state": "DONE"
  },
  "user_email": "user@example.com"
}
```

### API

呼叫 [jobs.get](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs/get?hl=zh-tw)，並提供 `jobId` 和 `projectId` 參數。(選用) 提供 `location` 參數，並將值設為執行工作的[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)。如果您使用包含該位置的完整工作 ID (例如 `my-project-1234:US.bquijob_123x456_123y123z123c`)，就不一定要提供這項參數。

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
		return fmt.Errorf("bigquery.NewClient: %v", err)
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

  public static void runGetJob() {
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

### Node.js

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Node.js 設定說明操作。詳情請參閱 [BigQuery Node.js API 參考說明文件](https://googleapis.dev/nodejs/bigquery/latest/index.html)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
// Import the Google Cloud client library
const {BigQuery} = require('@google-cloud/bigquery');
const bigquery = new BigQuery();

async function getJob() {
  // Get job properties.

  /**
   * TODO(developer): Uncomment the following lines before running the sample.
   */
  // const jobId = "existing-job-id";

  // Create a job reference
  const job = bigquery.job(jobId);

  // Retrieve job
  const [jobResult] = await job.get();

  console.log(jobResult.metadata.jobReference);
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

如需更多資訊來排解工作問題，請參閱「[`INFORMATION_SCHEMA.JOBS*`」檢視畫面](https://docs.cloud.google.com/bigquery/docs/information-schema-jobs?hl=zh-tw)和「記錄」。

## 列出工作

BigQuery 會儲存專案所有位置的所有工作，為期六個月。工作記錄包含處於「`RUNNING`」狀態的工作，以及已經「`DONE`」(從回報的「`SUCCESS`」或「`FAILURE`」狀態來判斷) 的工作。

如要列出專案中的工作，請按照下列步驟操作：

### 控制台

1. 前往「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中，按一下「Job history」。
4. 如要列出專案中的所有工作，請按一下「專案記錄」。如果您不是專案擁有者，可能就沒有查看專案中所有工作的權限。系統會優先列出最近的工作。
5. 如要列出工作，請按一下「個人記錄」。

### bq

發出 [`bq ls`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_ls) 指令並搭配使用下列其中一個標記：

* `--jobs=true` 或 `-j`：將工作識別為要列出的資源類型。
* `--all=true` 或 `-a`：列出所有使用者的工作。您必須具備 `bigquery.jobs.listAll` 權限，才能查看所有工作的完整 (未遮蓋的) 詳細資料。
* `--min_creation_time`：列出在已提供的時間戳記值之後的工作。這個值會以毫秒為單位的 [Unix 紀元](https://wikipedia.org/wiki/Unix_time)時間戳記表示。
* `--max_creation_time`：列出在已提供的時間戳記值之前的工作。這個值會以毫秒為單位的 [Unix 紀元](https://wikipedia.org/wiki/Unix_time)時間戳記表示。
* `--max_results` 或 `-n` 用來限制結果數。預設值為 50 個結果。

```
bq ls --jobs=true --all=true \
    --min_creation_time=MIN_TIME \
    --max_creation_time=MAX_TIME \
    --max_results=MAX_RESULTS \
    PROJECT_ID
```

更改下列內容：

* `MIN_TIME`：代表以毫秒為單位的 [Unix Epoch](https://wikipedia.org/wiki/Unix_time) 時間戳記的整數。
* `MAX_TIME`：代表以毫秒為單位的 [Unix Epoch](https://wikipedia.org/wiki/Unix_time) 時間戳記的整數。
* `MAX_RESULTS`：整數，指出傳回的工作數。
* `PROJECT_ID`：專案 ID，該專案含有您要列出的工作。如果[設定預設專案](https://docs.cloud.google.com/sdk/gcloud/reference/config/set?hl=zh-tw)，則不需要提供 `PROJECT_ID` 參數。

**範例**

以下指令會列出當前使用者的所有工作。執行這個指令需要 `bigquery.jobs.list` 權限。

```
bq ls --jobs=true myproject
```

以下指令會列出所有使用者的全部工作。執行這個指令需要 `bigquery.jobs.listAll` 權限。

```
bq ls --jobs=true --all=true myproject
```

以下指令會列出 `myproject` 中 10 個最新的工作：

```
bq ls --jobs=true --all=true --max_results=10 myproject
```

以下指令會列出在 2032 年 3 月 3 日上午 4:04:00 之前提交的所有工作。這個時間戳記 (以毫秒為單位) 等於下列整數值：`1961899440000`。

```
bq ls --jobs=true --max_creation_time=1961899440000
```

### API

呼叫 [`jobs.list` 方法](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs/list?hl=zh-tw)，並提供 `projectId` 參數。如要列出所有使用者的工作，請將 `allUsers` 參數設為 `true`。您必須具備 `bigquery.jobs.listAll` 權限，才能將 `allUsers` 設為 `true`。`jobs.list` 方法不會傳回子項工作。如要列出子項工作，請使用 [`INFORMATION_SCHEMA.JOBS` 檢視畫面](https://docs.cloud.google.com/bigquery/docs/information-schema-jobs?hl=zh-tw#child_jobs)。

### Go

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Go 設定說明操作。詳情請參閱 [BigQuery Go API 參考說明文件](https://godoc.org/cloud.google.com/go/bigquery)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import (
	"context"
	"fmt"
	"io"

	"cloud.google.com/go/bigquery"
	"google.golang.org/api/iterator"
)

// listJobs demonstrates iterating through the BigQuery jobs collection.
func listJobs(w io.Writer, projectID string) error {
	// projectID := "my-project-id"
	// jobID := "my-job-id"
	ctx := context.Background()

	client, err := bigquery.NewClient(ctx, projectID)
	if err != nil {
		return fmt.Errorf("bigquery.NewClient: %v", err)
	}
	defer client.Close()

	it := client.Jobs(ctx)
	// List up to 10 jobs to demonstrate iteration.
	for i := 0; i < 10; i++ {
		j, err := it.Next()
		if err == iterator.Done {
			break
		}
		if err != nil {
			return err
		}
		state := "Unknown"
		switch j.LastStatus().State {
		case bigquery.Pending:
			state = "Pending"
		case bigquery.Running:
			state = "Running"
		case bigquery.Done:
			state = "Done"
		}
		fmt.Fprintf(w, "Job %s in state %s\n", j.ID(), state)
	}
	return nil
}
```

### Java

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Java 設定說明操作。詳情請參閱 [BigQuery Java API 參考說明文件](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/overview?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import com.google.api.gax.paging.Page;
import com.google.cloud.bigquery.BigQuery;
import com.google.cloud.bigquery.BigQueryException;
import com.google.cloud.bigquery.BigQueryOptions;
import com.google.cloud.bigquery.Job;

// Sample to get list of jobs
public class ListJobs {

  public static void runListJobs() {
    listJobs();
  }

  public static void listJobs() {
    try {
      // Initialize client that will be used to send requests. This client only needs to be created
      // once, and can be reused for multiple requests.
      BigQuery bigquery = BigQueryOptions.getDefaultInstance().getService();

      Page<Job> jobs = bigquery.listJobs(BigQuery.JobListOption.pageSize(10));
      if (jobs == null) {
        System.out.println("Dataset does not contain any jobs.");
        return;
      }
      jobs.getValues().forEach(job -> System.out.printf("Success! Job ID: %s", job.getJobId()));
    } catch (BigQueryException e) {
      System.out.println("Jobs not listed in dataset due to error: \n" + e.toString());
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

async function listJobs() {
  // Lists all jobs in current GCP project.

  // List the 10 most recent jobs in reverse chronological order.
  //  Omit the max_results parameter to list jobs from the past 6 months.
  const options = {maxResults: 10};
  const [jobs] = await bigquery.getJobs(options);

  console.log('Jobs:');
  jobs.forEach(job => console.log(job.id));
}
```

### Python

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Python 設定說明操作。詳情請參閱 [BigQuery Python API 參考說明文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
from google.cloud import bigquery

import datetime

# Construct a BigQuery client object.
client = bigquery.Client()

# List the 10 most recent jobs in reverse chronological order.
# Omit the max_results parameter to list jobs from the past 6 months.
print("Last 10 jobs:")
for job in client.list_jobs(max_results=10):  # API request(s)
    print("{}".format(job.job_id))

# The following are examples of additional optional parameters:

# Use min_creation_time and/or max_creation_time to specify a time window.
print("Jobs from the last ten minutes:")
ten_mins_ago = datetime.datetime.utcnow() - datetime.timedelta(minutes=10)
for job in client.list_jobs(min_creation_time=ten_mins_ago):
    print("{}".format(job.job_id))

# Use all_users to include jobs run by all users in the project.
print("Last 10 jobs run by all users:")
for job in client.list_jobs(max_results=10, all_users=True):
    print("{} run by user: {}".format(job.job_id, job.user_email))

# Use state_filter to filter by job state.
print("Last 10 jobs done:")
for job in client.list_jobs(max_results=10, state_filter="DONE"):
    print("{}".format(job.job_id))
```

## 取消工作

您可以取消 `RUNNING` 或 `PENDING` 工作。
取消作業通常不到一分鐘即可完成。

即使是可以取消的工作，也不保證一定能成功取消。工作可能在提交取消要求時剛好完成，或工作也可能處於無法取消的階段。

**注意：** 工作取消後，視工作取消時所處的階段而定，還是可能會產生費用。詳情請參閱[定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw)頁面。

如要取消工作，請按照下列步驟操作：

### 控制台

1. 前往「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 按一下「撰寫新查詢」，然後輸入查詢。
3. 點選「執行」執行查詢。
4. 如要取消工作，請按一下「取消」。

### SQL

使用 `BQ.JOBS.CANCEL` 系統程序：

```
  CALL BQ.JOBS.CANCEL('JOB_ID');
```

將 JOB\_ID 替換為要取消的工作 ID。

如果您位於不同專案，但與要取消的工作位於相同區域，也必須加入專案 ID：

```
  CALL BQ.JOBS.CANCEL('PROJECT_ID.JOB_ID');
```

更改下列內容：

* `PROJECT_ID`：包含要取消工作項目的專案 ID
* `JOB_ID`：要取消的工作 ID

程序會立即傳回，BigQuery 隨後會取消作業。如果工作已成功或失敗，這項程序就不會產生任何效果。

### bq

發出含有 `JOB_ID` 引數的 [`bq cancel`](https://docs.cloud.google.com/bigquery/docs/reference/bq-cli-reference?hl=zh-tw#bq_cancel) 指令。您可以使用 `--nosync=true` 標記要求取消並立即傳回。根據預設，取消要求會等待完成。

提供 `JOB_ID` 引數時，可以使用完整 ID 或簡短格式。舉例來說， Google Cloud 控制台中列出的工作 ID 是完全合格的，也就是包含專案和位置：

`my-project-1234:US.bquijob_123x456_123y123z123c`

bq 指令列工具中列出的工作 ID 採用簡短格式，未納入專案 ID 和位置：

`bquijob_123x456_123y123z123c`

如要指定工作位置，請提供 `--location` 標記，並將值設為您的[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)。如果您使用完整工作 ID，則不一定要提供標記。如果您加入 `--location` 標記且使用的是完整工作 ID，則系統會忽略 `--location` 標記。

以下指令會要求取消工作並等待完成。如果提供完整工作 ID，則系統會忽略 `--location` 標記：

```
bq --location=LOCATION cancel JOB_ID
```

以下指令會要求取消工作並立即傳回。如果提供完整工作 ID，則系統會忽略 `--location` 標記：

```
bq --location=LOCATION --nosync cancel JOB_ID
```

更改下列內容：

* `LOCATION` (選用)：執行工作的位置名稱。舉例來說，如果您在東京區域使用 BigQuery，請將該旗標的值設定為 `asia-northeast1`。您可以使用 [`.bigqueryrc` 檔案](https://docs.cloud.google.com/bigquery/docs/bq-command-line-tool?hl=zh-tw#setting_default_values_for_command-line_flags)設定位置的預設值。
* `JOB_ID`：要取消的工作 ID。如果您從 Google Cloud 控制台複製工作 ID，則專案 ID 和位置會併入工作 ID 中；例如：`my-project-1234:US.bquijob_123x456_123y123z123c`。

**範例**

以下指令會取消在 `my-project-1234` 專案的 `US` 多地區位置執行的 `my-project-1234:US.bquijob_123x456_123y123z123c` 工作，並等待完成。因為使用的是完整工作 ID，所以未提供 location 標記。

```
bq cancel my-project-1234:US.bquijob_123x456_123y123z123c
```

以下指令會取消在 `my-project-1234` 專案的 `US` 多區域位置執行的 `bquijob_123x456_123y123z123c` 工作，並等待完成。因為使用的是簡短格式的工作 ID，所以提供了 `--location` 標記。

```
bq --location=US cancel bquijob_123x456_123y123z123c
```

以下指令會取消在 `my-project-1234` 專案中於 `US` 多區域位置執行的 `bquijob_123x456_123y123z123c` 工作，並立即傳回。因為使用的是完整工作 ID，所以未提供 `--location` 標記。

```
bq --nosync cancel my-project-1234:US.bquijob_123x456_123y123z123c
```

### API

呼叫 [jobs.get](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs/cancel?hl=zh-tw)，並提供 `jobId` 和 `projectId` 參數。提供 `location` 參數，並將值設為執行工作的[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)。

### Go

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Go 設定說明操作。詳情請參閱 [BigQuery Go API 參考說明文件](https://godoc.org/cloud.google.com/go/bigquery)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import (
	"context"
	"fmt"

	"cloud.google.com/go/bigquery"
)

// cancelJob demonstrates how a job cancellation request can be issued for a specific
// BigQuery job.
func cancelJob(projectID, jobID string) error {
	// projectID := "my-project-id"
	// jobID := "my-job-id"
	ctx := context.Background()

	client, err := bigquery.NewClient(ctx, projectID)
	if err != nil {
		return fmt.Errorf("bigquery.NewClient: %v", err)
	}
	defer client.Close()

	job, err := client.JobFromID(ctx, jobID)
	if err != nil {
		return nil
	}
	return job.Cancel(ctx)
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
import java.util.UUID;

// Sample to cancel a job
public class CancelJob {

  public static void runCancelJob() {
    // TODO(developer): Replace these variables before running the sample.
    String query = "SELECT country_name from `bigquery-public-data.utility_us.country_code_iso`";
    cancelJob(query);
  }

  public static void cancelJob(String query) {
    try {
      // Initialize client that will be used to send requests. This client only needs to be created
      // once, and can be reused for multiple requests.
      BigQuery bigquery = BigQueryOptions.getDefaultInstance().getService();

      // Specify a job configuration to set optional job resource properties.
      QueryJobConfiguration queryConfig = QueryJobConfiguration.newBuilder(query).build();

      // The location and job name are optional,
      // if both are not specified then client will auto-create.
      String jobName = "jobId_" + UUID.randomUUID().toString();
      JobId jobId = JobId.newBuilder().setLocation("us").setJob(jobName).build();

      // Create a job with job ID
      bigquery.create(JobInfo.of(jobId, queryConfig));

      // Get a job that was just created
      Job job = bigquery.getJob(jobId);
      if (job.cancel()) {
        System.out.println("Job canceled successfully");
      } else {
        System.out.println("Job was not canceled");
      }
    } catch (BigQueryException e) {
      System.out.println("Job was not canceled.\n" + e.toString());
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

async function cancelJob() {
  // Attempts to cancel a job.

  /**
   * TODO(developer): Uncomment the following lines before running the sample.
   */
  // const jobId = "existing-job-id";

  // Create a job reference
  const job = bigquery.job(jobId);

  // Attempt to cancel job
  const [apiResult] = await job.cancel();

  console.log(apiResult.job.status);
}
```

### Python

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Python 設定說明操作。詳情請參閱 [BigQuery Python API 參考說明文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
from google.cloud import bigquery


def cancel_job(
    client: bigquery.Client,
    location: str = "us",
    job_id: str = "abcd-efgh-ijkl-mnop",
) -> None:
    job = client.cancel_job(job_id, location=location)
    print(f"{job.location}:{job.job_id} cancelled")
```

## 刪除工作的中繼資料

您可以使用 bq 指令列工具和 Python 用戶端程式庫，刪除特定工作的中繼資料。
BigQuery 會保留過去 6 個月內執行的工作記錄。您可以使用這個方法，移除查詢陳述式中可能存在的敏感資訊。工作完成後才能刪除工作的中繼資料。如果工作已建立子項工作，系統也會刪除子項工作。系統不允許刪除子項工作。只能刪除父項或頂層工作。

如要刪除工作的中繼資料，請按照下列步驟操作：

### bq

發出 `bq rm` 指令並搭配使用 `-j` 標記和工作 ID。

當您提供工作 ID 時，可以使用完整 ID 或簡短格式。舉例來說，在 Google Cloud 控制台中列出的工作 ID 都是完整名稱，也就是包含專案和位置：

`my-project-1234:US.bquijob_123x456_123y123z123c`

bq 指令列工具中列出的工作 ID 採用簡短格式。其中不含專案 ID 和位置：

`bquijob_123x456_123y123z123c`

如要指定工作位置，請提供 `--location` 標記，並將值設為您的[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)。如果您使用完整工作 ID，則不一定要提供標記。如果您加入 `--location` 標記且使用的是完整工作 ID，則系統會忽略 `--location` 標記。

下列指令會刪除工作：

```
bq --location=location \
    --project_id=project_id \
    rm -j job_id
```

### Python

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Python 設定說明操作。詳情請參閱 [BigQuery Python API 參考說明文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
from google.api_core import exceptions
from google.cloud import bigquery

# TODO(developer): Set the job ID to the ID of the job whose metadata you
#                  wish to delete.
job_id = "abcd-efgh-ijkl-mnop"

# TODO(developer): Set the location to the region or multi-region
#                  containing the job.
location = "us-east1"

client = bigquery.Client()

client.delete_job_metadata(job_id, location=location)

try:
    client.get_job(job_id, location=location)
except exceptions.NotFound:
    print(f"Job metadata for job {location}:{job_id} was deleted.")
```

## 重複執行工作

系統無法使用相同的工作 ID 重複執行工作，因此您必須使用相同的設定建立新工作。您可以在Google Cloud 控制台或 bq 指令列工具中提交新工作，系統會指派新的工作 ID。如果您使用 API 或用戶端程式庫來提交工作，則必須產生新的工作 ID。

如要重複執行工作，請按照下列步驟操作：

### 控制台

如要重複執行查詢工作，請按照下列步驟操作：

1. 前往「BigQuery」頁面

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中，按一下「Job history」。
4. 如要列出所有工作，請按一下「個人記錄」。如要列出專案中的所有工作，請按一下「專案記錄」。
5. 按一下查詢工作，即可開啟工作詳細資料。
6. 如要重複查詢，請按一下「開啟為新的查詢」。
7. 按一下「執行」。

如要重複執行載入工作，請按照下列步驟操作：

1. 前往「BigQuery」頁面

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中，按一下「Job history」。
4. 如要列出所有工作，請按一下「個人記錄」。如要列出專案中的所有工作，請按一下「專案記錄」。
5. 按一下載入工作，開啟工作詳細資料。
6. 如要重複執行工作，請按一下「重複載入工作」。

**注意：** 您無法透過 Google Cloud 控制台重複執行擷取工作或複製工作。

### bq

重新發出指令，BigQuery 會自動產生具有新工作 ID 的工作。

### API

沒有可以重複執行工作的一次呼叫方法；如要重複特定工作，請執行下列步驟：

1. 呼叫 [`jobs.get`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs/get?hl=zh-tw) 以擷取重複執行工作時所需的資源。
2. 移除「id」、「status」和「statistics」欄位。
   將「jobId」 欄位更改為用戶端程式碼產生的新值。視需要更改任何其他欄位。
3. 使用修改後的資源和新的工作 ID 呼叫 [`jobs.insert`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs/insert?hl=zh-tw)，以啟動新工作。

## 後續步驟

* 瞭解如何[透過程式執行工作](https://docs.cloud.google.com/bigquery/docs/running-jobs?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-16 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-16 (世界標準時間)。"],[],[]]