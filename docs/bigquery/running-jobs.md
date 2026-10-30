Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 透過程式執行工作

您可以使用 BigQuery REST API 和用戶端程式庫，建立及管理非同步工作，自動執行應用程式的載入、查詢、擷取和複製作業。呼叫 [`jobs.insert`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs/insert?hl=zh-tw) 方法啟動工作後，您可以輪詢工作資源的狀態屬性，追蹤執行作業何時完成，並確認作業是否成功。

## 事前準備

授予 Identity and Access Management (IAM) 角色，讓使用者具備必要權限，可執行本文件中的各項工作。

### 所需權限

如要執行 BigQuery 工作，您必須具備 `bigquery.jobs.create` IAM 權限。

下列各項預先定義的 IAM 角色，都包含執行工作所需的權限：

* `roles/bigquery.user`
* `roles/bigquery.jobUser`
* `roles/bigquery.admin`

此外，建立工作時，系統會自動授予您該工作的下列權限：

* `bigquery.jobs.get`
* `bigquery.jobs.update`

如要進一步瞭解 BigQuery 的 IAM 角色和權限，請參閱「[預先定義的角色和權限](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)」。

## 執行中的工作

如何透過程式執行工作：

1. 呼叫 `jobs.insert` 方法來啟動工作。呼叫 `jobs.insert` 方法時，請加入[工作資源](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs?hl=zh-tw)表示法。
2. 在工作資源的 [`configuration`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#JobConfiguration) 區段中，加入指定工作類型的子項屬性：`load`、`query`、`extract` 或 `copy`。
3. 呼叫 `jobs.insert` 方法後，請使用工作 ID 和位置呼叫 `jobs.get`，並檢查 `status.state` 值，確認工作狀態。當 `status.state` 為 `DONE` 時，表示工作已停止執行。不過，`DONE` 狀態不代表工作已成功完成，僅表示工作已不再執行。

   **注意：** 部分包裝函式會為您管理工作狀態要求。舉例來說，執行 `jobs.query` 會建立工作，並在指定時間內定期輪詢 `DONE` 狀態。
4. 確認工作是否成功。如果工作具有 `errorResult` 屬性，則表示工作失敗。`status.errorResult` 屬性會保留說明失敗工作發生錯誤的資訊。如果沒有 `status.errorResult`，代表工作已成功完成，但可能發生一些非嚴重錯誤，例如在載入工作中匯入幾列時發生問題。非嚴重錯誤會傳回至工作的 `status.errors` 清單。

## 使用用戶端程式庫執行工作

如要使用 BigQuery 適用的 Cloud 用戶端程式庫建立及執行工作，請按照下列步驟操作：

### C#

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 C# 設定操作說明進行操作。詳情請參閱 [BigQuery C# API 參考文件](https://docs.cloud.google.com/dotnet/docs/reference/Google.Cloud.BigQuery.V2/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

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

### Java

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Java 設定操作說明進行操作。詳情請參閱 [BigQuery Java API 參考文件](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/overview?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

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

### Python

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Python 設定操作說明進行操作。詳情請參閱 [BigQuery Python API 參考文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證機制](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
from google.cloud import bigquery

# Construct a BigQuery client object.
client = bigquery.Client()

query_job = client.query(
    "SELECT country_name from `bigquery-public-data.utility_us.country_code_iso`",
    # Explicitly force job execution to be routed to a specific processing
    # location.
    location="US",
    # Specify a job configuration to set optional job resource properties.
    job_config=bigquery.QueryJobConfig(
        labels={"example-label": "example-value"}, maximum_bytes_billed=1000000
    ),
    # The client libraries automatically generate a job ID. Override the
    # generated ID with either the job_id_prefix or job_id parameters.
    job_id_prefix="code_sample_",
)  # Make an API request.

print("Started job: {}".format(query_job.job_id))
```

## 加入工作標籤

您可以使用 bq 指令列工具的 `--label` 旗標，透過指令列將標籤新增至查詢工作。bq 工具僅支援為查詢工作新增標籤。

您也可以在透過 API 提交工作時，在呼叫 [`jobs.insert`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs/insert?hl=zh-tw) 方法時指定工作設定中的 `labels` 屬性，為工作新增標籤。API 可用於在任何工作類型中加入標籤。

您無法在待處理、執行中或已完成的工作中加入或更新標籤。

在工作中加入標籤後，標籤就會納入您的帳單資料中。

詳情請參閱「[新增工作標籤](https://docs.cloud.google.com/bigquery/docs/adding-labels?hl=zh-tw#job-label)」。

## 後續步驟

* 如需啟動及輪詢查詢工作的程式碼範例，請參閱[執行查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#batch)一文。
* 如要進一步瞭解如何建立工作資源表示法，請參閱 API 參考資料中的[工作總覽頁面](https://docs.cloud.google.com/bigquery/docs/reference/v2/jobs?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-10-29 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-10-29 (世界標準時間)。"],[],[]]