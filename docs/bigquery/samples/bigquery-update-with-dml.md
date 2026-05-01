* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [範例](https://docs.cloud.google.com/bigquery/docs/samples?hl=zh-tw)

# 使用 DML 更新資料表 透過集合功能整理內容 你可以依據偏好儲存及分類內容。

使用 DML 查詢更新 BigQuery 資料表中的資料。

## 程式碼範例

### Java

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Java 設定說明操作。詳情請參閱 [BigQuery Java API 參考說明文件](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/overview?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import com.google.cloud.bigquery.BigQuery;
import com.google.cloud.bigquery.BigQueryException;
import com.google.cloud.bigquery.BigQueryOptions;
import com.google.cloud.bigquery.FormatOptions;
import com.google.cloud.bigquery.Job;
import com.google.cloud.bigquery.JobId;
import com.google.cloud.bigquery.QueryJobConfiguration;
import com.google.cloud.bigquery.TableDataWriteChannel;
import com.google.cloud.bigquery.TableId;
import com.google.cloud.bigquery.TableResult;
import com.google.cloud.bigquery.WriteChannelConfiguration;
import java.io.IOException;
import java.io.OutputStream;
import java.nio.channels.Channels;
import java.nio.file.FileSystems;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.UUID;

// Sample to update data in BigQuery tables using DML query
public class UpdateTableDml {

  public static void main(String[] args) throws IOException, InterruptedException {
    // TODO(developer): Replace these variables before running the sample.
    String datasetName = "MY_DATASET_NAME";
    String tableName = "MY_TABLE_NAME";
    updateTableDml(datasetName, tableName);
  }

  public static void updateTableDml(String datasetName, String tableName)
      throws IOException, InterruptedException {
    try {
      // Initialize client that will be used to send requests. This client only needs to be created
      // once, and can be reused for multiple requests.
      BigQuery bigquery = BigQueryOptions.getDefaultInstance().getService();

      // Load JSON file into UserSessions table
      TableId tableId = TableId.of(datasetName, tableName);

      WriteChannelConfiguration writeChannelConfiguration =
          WriteChannelConfiguration.newBuilder(tableId)
              .setFormatOptions(FormatOptions.json())
              .build();

      // Imports a local JSON file into a table.
      Path jsonPath =
          FileSystems.getDefault().getPath("src/test/resources", "userSessionsData.json");

      // The location and JobName must be specified; other fields can be auto-detected.
      String jobName = "jobId_" + UUID.randomUUID().toString();
      JobId jobId = JobId.newBuilder().setLocation("us").setJob(jobName).build();

      try (TableDataWriteChannel writer = bigquery.writer(jobId, writeChannelConfiguration);
          OutputStream stream = Channels.newOutputStream(writer)) {
        Files.copy(jsonPath, stream);
      }

      // Get the Job created by the TableDataWriteChannel and wait for it to complete.
      Job job = bigquery.getJob(jobId);
      Job completedJob = job.waitFor();
      if (completedJob == null) {
        System.out.println("Job not executed since it no longer exists.");
        return;
      } else if (completedJob.getStatus().getError() != null) {
        System.out.println(
            "BigQuery was unable to load local file to the table due to an error: \n"
                + job.getStatus().getError());
        return;
      }

      System.out.println(
          job.getStatistics().toString() + " userSessionsData json uploaded successfully");

      // Write a DML query to modify UserSessions table
      // To create DML query job to mask the last octet in every row's ip_address column
      String dmlQuery =
          String.format(
              "UPDATE `%s.%s` \n"
                  + "SET ip_address = REGEXP_REPLACE(ip_address, r\"(\\.[0-9]+)$\", \".0\")\n"
                  + "WHERE TRUE",
              datasetName, tableName);

      QueryJobConfiguration dmlQueryConfig = QueryJobConfiguration.newBuilder(dmlQuery).build();

      // Execute the query.
      TableResult result = bigquery.query(dmlQueryConfig);

      // Print the results.
      result.iterateAll().forEach(rows -> rows.forEach(row -> System.out.println(row.getValue())));

      System.out.println("Table updated successfully using DML");
    } catch (BigQueryException e) {
      System.out.println("Table update failed \n" + e.toString());
    }
  }
}
```

### Python

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Python 設定說明操作。詳情請參閱 [BigQuery Python API 參考說明文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import pathlib
from typing import Dict, Optional

from google.cloud import bigquery
from google.cloud.bigquery import enums


def load_from_newline_delimited_json(
    client: bigquery.Client,
    filepath: pathlib.Path,
    project_id: str,
    dataset_id: str,
    table_id: str,
) -> None:
    full_table_id = f"{project_id}.{dataset_id}.{table_id}"
    job_config = bigquery.LoadJobConfig()
    job_config.source_format = enums.SourceFormat.NEWLINE_DELIMITED_JSON
    job_config.schema = [
        bigquery.SchemaField("id", enums.SqlTypeNames.STRING),
        bigquery.SchemaField("user_id", enums.SqlTypeNames.INTEGER),
        bigquery.SchemaField("login_time", enums.SqlTypeNames.TIMESTAMP),
        bigquery.SchemaField("logout_time", enums.SqlTypeNames.TIMESTAMP),
        bigquery.SchemaField("ip_address", enums.SqlTypeNames.STRING),
    ]

    with open(filepath, "rb") as json_file:
        load_job = client.load_table_from_file(
            json_file, full_table_id, job_config=job_config
        )

    # Wait for load job to finish.
    load_job.result()


def update_with_dml(
    client: bigquery.Client, project_id: str, dataset_id: str, table_id: str
) -> int:
    query_text = f"""
    UPDATE `{project_id}.{dataset_id}.{table_id}`
    SET ip_address = REGEXP_REPLACE(ip_address, r"(\\.[0-9]+)$", ".0")
    WHERE TRUE
    """
    query_job = client.query(query_text)

    # Wait for query job to finish.
    query_job.result()

    assert query_job.num_dml_affected_rows is not None

    print(f"DML query modified {query_job.num_dml_affected_rows} rows.")
    return query_job.num_dml_affected_rows


def run_sample(override_values: Optional[Dict[str, str]] = None) -> int:
    if override_values is None:
        override_values = {}

    client = bigquery.Client()
    filepath = pathlib.Path(__file__).parent / "user_sessions_data.json"
    project_id = client.project
    dataset_id = "sample_db"
    table_id = "UserSessions"
    load_from_newline_delimited_json(client, filepath, project_id, dataset_id, table_id)
    return update_with_dml(client, project_id, dataset_id, table_id)
```

## 後續步驟

如要搜尋及篩選其他 Google Cloud 產品的程式碼範例，請參閱[Google Cloud 範例瀏覽工具](https://docs.cloud.google.com/docs/samples?product=bigquery&hl=zh-tw)。

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。




[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],[],[],[]]