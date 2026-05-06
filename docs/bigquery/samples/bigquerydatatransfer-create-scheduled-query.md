Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [範例](https://docs.cloud.google.com/bigquery/docs/samples?hl=zh-tw)

# 建立排程查詢 透過集合功能整理內容 你可以依據偏好儲存及分類內容。

排定每 24 小時執行一次查詢，並根據執行日期設定目的地資料表 ID。

## 深入探索

如需包含這個程式碼範例的詳細說明文件，請參閱下列文章：

* [排定查詢](https://docs.cloud.google.com/bigquery/docs/scheduling-queries?hl=zh-tw)

## 程式碼範例

### Go

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Go 設定說明操作。詳情請參閱 [BigQuery Go API 參考說明文件](https://godoc.org/cloud.google.com/go/bigquery)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import (
	"context"
	"fmt"

	"cloud.google.com/go/bigquery"
	datatransfer "cloud.google.com/go/bigquery/datatransfer/apiv1"
	"cloud.google.com/go/bigquery/datatransfer/apiv1/datatransferpb"
	"google.golang.org/protobuf/types/known/structpb"
)

// createScheduledQuery schedule a query to run every
// 24 hours with a destination table identifier based on the run date.
func createScheduledQuery(projectID, datasetID, query string) error {
	// projectID := "my-project-id"
	// datasetID := "my-dataset-id"
	// query = `SELECT CURRENT_TIMESTAMP() as current_time, @run_time as intended_run_time,
	// @run_date as intended_run_date, 17 as some_integer`
	ctx := context.Background()
	dtc, err := datatransfer.NewClient(ctx)
	if err != nil {
		return fmt.Errorf("datatransfer.NewClient: %w", err)
	}
	defer dtc.Close()

	paramsMap := map[string]interface{}{}
	paramsMap["destination_table_name_template"] = "my_destination_table_{run_date}"
	paramsMap["write_disposition"] = string(bigquery.WriteTruncate)
	paramsMap["partitioning_field"] = ""
	paramsMap["query"] = query
	params, err := structpb.NewStruct(paramsMap)
	if err != nil {
		return fmt.Errorf("structpb.NewStruct: %w", err)
	}

	req := &datatransferpb.CreateTransferConfigRequest{
		Parent: fmt.Sprintf("projects/%s", projectID),
		TransferConfig: &datatransferpb.TransferConfig{
			Destination: &datatransferpb.TransferConfig_DestinationDatasetId{
				DestinationDatasetId: datasetID,
			},
			DisplayName:  "Your Scheduled Query Name",
			DataSourceId: "scheduled_query",
			Params:       params,
			Schedule:     "every 24 hours",
		},
	}

	_, err = dtc.CreateTransferConfig(ctx, req)
	if err != nil {
		return fmt.Errorf("dtc.CreateTransferConfig: %w", err)
	}

	return nil
}
```

### Java

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Java 設定說明操作。詳情請參閱 [BigQuery Java API 參考說明文件](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/overview?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import com.google.api.gax.rpc.ApiException;
import com.google.cloud.bigquery.datatransfer.v1.CreateTransferConfigRequest;
import com.google.cloud.bigquery.datatransfer.v1.DataTransferServiceClient;
import com.google.cloud.bigquery.datatransfer.v1.ProjectName;
import com.google.cloud.bigquery.datatransfer.v1.TransferConfig;
import com.google.protobuf.Struct;
import com.google.protobuf.Value;
import java.io.IOException;
import java.util.HashMap;
import java.util.Map;

// Sample to create a scheduled query
public class CreateScheduledQuery {

  public static void main(String[] args) throws IOException {
    // TODO(developer): Replace these variables before running the sample.
    final String projectId = "MY_PROJECT_ID";
    final String datasetId = "MY_DATASET_ID";
    final String query =
        "SELECT CURRENT_TIMESTAMP() as current_time, @run_time as intended_run_time, "
            + "@run_date as intended_run_date, 17 as some_integer";
    Map<String, Value> params = new HashMap<>();
    params.put("query", Value.newBuilder().setStringValue(query).build());
    params.put(
        "destination_table_name_template",
        Value.newBuilder().setStringValue("my_destination_table_{run_date}").build());
    params.put("write_disposition", Value.newBuilder().setStringValue("WRITE_TRUNCATE").build());
    params.put("partitioning_field", Value.newBuilder().build());
    TransferConfig transferConfig =
        TransferConfig.newBuilder()
            .setDestinationDatasetId(datasetId)
            .setDisplayName("Your Scheduled Query Name")
            .setDataSourceId("scheduled_query")
            .setParams(Struct.newBuilder().putAllFields(params).build())
            .setSchedule("every 24 hours")
            .build();
    createScheduledQuery(projectId, transferConfig);
  }

  public static void createScheduledQuery(String projectId, TransferConfig transferConfig)
      throws IOException {
    try (DataTransferServiceClient dataTransferServiceClient = DataTransferServiceClient.create()) {
      ProjectName parent = ProjectName.of(projectId);
      CreateTransferConfigRequest request =
          CreateTransferConfigRequest.newBuilder()
              .setParent(parent.toString())
              .setTransferConfig(transferConfig)
              .build();
      TransferConfig config = dataTransferServiceClient.createTransferConfig(request);
      System.out.println("\nScheduled query created successfully :" + config.getName());
    } catch (ApiException ex) {
      System.out.print("\nScheduled query was not created." + ex.toString());
    }
  }
}
```

### Python

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Python 設定說明操作。詳情請參閱 [BigQuery Python API 參考說明文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
from google.cloud import bigquery_datatransfer

transfer_client = bigquery_datatransfer.DataTransferServiceClient()

# The project where the query job runs is the same as the project
# containing the destination dataset.
project_id = "your-project-id"
dataset_id = "your_dataset_id"

# This service account will be used to execute the scheduled queries. Omit
# this request parameter to run the query as the user with the credentials
# associated with this client.
service_account_name = "abcdef-test-sa@abcdef-test.iam.gserviceaccount.com"

# Use standard SQL syntax for the query.
query_string = """
SELECT
  CURRENT_TIMESTAMP() as current_time,
  @run_time as intended_run_time,
  @run_date as intended_run_date,
  17 as some_integer
"""

parent = transfer_client.common_project_path(project_id)

transfer_config = bigquery_datatransfer.TransferConfig(
    destination_dataset_id=dataset_id,
    display_name="Your Scheduled Query Name",
    data_source_id="scheduled_query",
    params={
        "query": query_string,
        "destination_table_name_template": "your_table_{run_date}",
        "write_disposition": "WRITE_TRUNCATE",
        "partitioning_field": "",
    },
    schedule="every 24 hours",
)

transfer_config = transfer_client.create_transfer_config(
    bigquery_datatransfer.CreateTransferConfigRequest(
        parent=parent,
        transfer_config=transfer_config,
        service_account_name=service_account_name,
    )
)

print("Created scheduled query '{}'".format(transfer_config.name))
```

## 後續步驟

如要搜尋及篩選其他 Google Cloud 產品的程式碼範例，請參閱[Google Cloud 瀏覽器範例](https://docs.cloud.google.com/docs/samples?product=bigquerydatatransfer&hl=zh-tw)。

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。




[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],[],[],[]]