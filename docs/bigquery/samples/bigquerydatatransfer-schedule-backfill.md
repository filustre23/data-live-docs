Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [範例](https://docs.cloud.google.com/bigquery/docs/samples?hl=zh-tw)

# 安排執行補充作業 透過集合功能整理內容 你可以依據偏好儲存及分類內容。

啟動資料回填，將歷來資料載入 BigQuery。如要瞭解可回填的資料量，請參閱資料來源的說明文件。

## 深入探索

如需包含這個程式碼範例的詳細說明文件，請參閱下列文章：

* [管理轉移作業](https://docs.cloud.google.com/bigquery/docs/working-with-transfers?hl=zh-tw)
* [排定查詢](https://docs.cloud.google.com/bigquery/docs/scheduling-queries?hl=zh-tw)

## 程式碼範例

### Java

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Java 設定說明操作。詳情請參閱 [BigQuery Java API 參考說明文件](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/overview?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import com.google.api.gax.rpc.ApiException;
import com.google.cloud.bigquery.datatransfer.v1.DataTransferServiceClient;
import com.google.cloud.bigquery.datatransfer.v1.ScheduleTransferRunsRequest;
import com.google.cloud.bigquery.datatransfer.v1.ScheduleTransferRunsResponse;
import com.google.protobuf.Timestamp;
import java.io.IOException;
import org.threeten.bp.Clock;
import org.threeten.bp.Instant;
import org.threeten.bp.temporal.ChronoUnit;

// Sample to run schedule back fill for transfer config
public class ScheduleBackFill {

  public static void main(String[] args) throws IOException {
    // TODO(developer): Replace these variables before running the sample.
    String configId = "MY_CONFIG_ID";
    Clock clock = Clock.systemDefaultZone();
    Instant instant = clock.instant();
    Timestamp startTime =
        Timestamp.newBuilder()
            .setSeconds(instant.minus(5, ChronoUnit.DAYS).getEpochSecond())
            .setNanos(instant.minus(5, ChronoUnit.DAYS).getNano())
            .build();
    Timestamp endTime =
        Timestamp.newBuilder()
            .setSeconds(instant.minus(2, ChronoUnit.DAYS).getEpochSecond())
            .setNanos(instant.minus(2, ChronoUnit.DAYS).getNano())
            .build();
    scheduleBackFill(configId, startTime, endTime);
  }

  public static void scheduleBackFill(String configId, Timestamp startTime, Timestamp endTime)
      throws IOException {
    try (DataTransferServiceClient client = DataTransferServiceClient.create()) {
      ScheduleTransferRunsRequest request =
          ScheduleTransferRunsRequest.newBuilder()
              .setParent(configId)
              .setStartTime(startTime)
              .setEndTime(endTime)
              .build();
      ScheduleTransferRunsResponse response = client.scheduleTransferRuns(request);
      System.out.println("Schedule backfill run successfully :" + response.getRunsCount());
    } catch (ApiException ex) {
      System.out.print("Schedule backfill was not run." + ex.toString());
    }
  }
}
```

### Python

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Python 設定說明操作。詳情請參閱 [BigQuery Python API 參考說明文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import datetime

from google.cloud.bigquery_datatransfer_v1 import (
    DataTransferServiceClient,
    StartManualTransferRunsRequest,
)

# Create a client object
client = DataTransferServiceClient()

# Replace with your transfer configuration name
transfer_config_name = "projects/1234/locations/us/transferConfigs/abcd"
now = datetime.datetime.now(datetime.timezone.utc)
start_time = now - datetime.timedelta(days=5)
end_time = now - datetime.timedelta(days=2)

# Some data sources, such as scheduled_query only support daily run.
# Truncate start_time and end_time to midnight time (00:00AM UTC).
start_time = datetime.datetime(
    start_time.year, start_time.month, start_time.day, tzinfo=datetime.timezone.utc
)
end_time = datetime.datetime(
    end_time.year, end_time.month, end_time.day, tzinfo=datetime.timezone.utc
)

requested_time_range = StartManualTransferRunsRequest.TimeRange(
    start_time=start_time,
    end_time=end_time,
)

# Initialize request argument(s)
request = StartManualTransferRunsRequest(
    parent=transfer_config_name,
    requested_time_range=requested_time_range,
)

# Make the request
response = client.start_manual_transfer_runs(request=request)

# Handle the response
print("Started manual transfer runs:")
for run in response.runs:
    print(f"backfill: {run.run_time} run: {run.name}")
```

## 後續步驟

如要搜尋及篩選其他 Google Cloud 產品的程式碼範例，請參閱[Google Cloud 瀏覽器範例](https://docs.cloud.google.com/docs/samples?product=bigquerydatatransfer&hl=zh-tw)。

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。




[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],[],[],[]]