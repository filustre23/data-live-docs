Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [範例](https://docs.cloud.google.com/bigquery/docs/samples?hl=zh-tw)

# 查詢指令碼 透過集合功能整理內容 你可以依據偏好儲存及分類內容。

執行查詢指令碼。

## 程式碼範例

### Java

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Java 設定說明操作。詳情請參閱 [BigQuery Java API 參考說明文件](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/overview?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import com.google.api.gax.paging.Page;
import com.google.cloud.bigquery.BigQuery;
import com.google.cloud.bigquery.BigQueryException;
import com.google.cloud.bigquery.BigQueryOptions;
import com.google.cloud.bigquery.Job;
import com.google.cloud.bigquery.JobInfo;
import com.google.cloud.bigquery.QueryJobConfiguration;

// Sample to run query script.
public class QueryScript {

  public static void main(String[] args) {
    String script =
        "-- Declare a variable to hold names as an array.\n"
            + "DECLARE top_names ARRAY<STRING>;\n"
            + "-- Build an array of the top 100 names from the year 2017.\n"
            + "SET top_names = (\n"
            + "  SELECT ARRAY_AGG(name ORDER BY number DESC LIMIT 100)\n"
            + "  FROM `bigquery-public-data`.usa_names.usa_1910_current\n"
            + "  WHERE year = 2017\n"
            + ");\n"
            + "-- Which names appear as words in Shakespeare's plays?\n"
            + "SELECT\n"
            + "  name AS shakespeare_name\n"
            + "FROM UNNEST(top_names) AS name\n"
            + "WHERE name IN (\n"
            + "  SELECT word\n"
            + "  FROM `bigquery-public-data`.samples.shakespeare\n"
            + ");";
    queryScript(script);
  }

  public static void queryScript(String script) {
    try {
      // Initialize client that will be used to send requests. This client only needs to be created
      // once, and can be reused for multiple requests.
      BigQuery bigquery = BigQueryOptions.getDefaultInstance().getService();

      QueryJobConfiguration queryConfig = QueryJobConfiguration.newBuilder(script).build();
      Job createJob = bigquery.create(JobInfo.of(queryConfig));
      // Wait for the whole script to finish.
      JobInfo jobInfo = createJob.waitFor();
      String parentJobId = jobInfo.getJobId().getJob();

      // Fetch jobs created by the SQL script.
      Page<Job> childJobs = bigquery.listJobs(BigQuery.JobListOption.parentJobId(parentJobId));
      childJobs
          .iterateAll()
          .forEach(job -> System.out.printf("Child Job Id: ", job.getJobId().getJob()));

      System.out.println("Query script performed successfully.");
    } catch (BigQueryException | InterruptedException e) {
      System.out.println("Query not performed \n" + e.toString());
    }
  }
}
```

### Python

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Python 設定說明操作。詳情請參閱 [BigQuery Python API 參考說明文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
from google.cloud import bigquery

# Construct a BigQuery client object.
client = bigquery.Client()

# Run a SQL script.
sql_script = """
-- Declare a variable to hold names as an array.
DECLARE top_names ARRAY<STRING>;

-- Build an array of the top 100 names from the year 2017.
SET top_names = (
SELECT ARRAY_AGG(name ORDER BY number DESC LIMIT 100)
FROM `bigquery-public-data.usa_names.usa_1910_2013`
WHERE year = 2000
);

-- Which names appear as words in Shakespeare's plays?
SELECT
name AS shakespeare_name
FROM UNNEST(top_names) AS name
WHERE name IN (
SELECT word
FROM `bigquery-public-data.samples.shakespeare`
);
"""
parent_job = client.query(sql_script)

# Wait for the whole script to finish.
rows_iterable = parent_job.result()
print("Script created {} child jobs.".format(parent_job.num_child_jobs))

# Fetch result rows for the final sub-job in the script.
rows = list(rows_iterable)
print(
    "{} of the top 100 names from year 2000 also appear in Shakespeare's works.".format(
        len(rows)
    )
)

# Fetch jobs created by the SQL script.
child_jobs_iterable = client.list_jobs(parent_job=parent_job)
for child_job in child_jobs_iterable:
    child_rows = list(child_job.result())
    print(
        "Child job with ID {} produced {} row(s).".format(
            child_job.job_id, len(child_rows)
        )
    )
```

## 後續步驟

如要搜尋及篩選其他 Google Cloud 產品的程式碼範例，請參閱[Google Cloud 範例瀏覽工具](https://docs.cloud.google.com/docs/samples?product=bigquery&hl=zh-tw)。

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。




[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],[],[],[]]