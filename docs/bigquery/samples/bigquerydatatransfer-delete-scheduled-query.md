Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [範例](https://docs.cloud.google.com/bigquery/docs/samples?hl=zh-tw)

# 刪除排程查詢 透過集合功能整理內容 你可以依據偏好儲存及分類內容。

刪除預定查詢的設定，停止日後執行。

## 程式碼範例

### Go

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Go 設定說明操作。詳情請參閱 [BigQuery Go API 參考說明文件](https://godoc.org/cloud.google.com/go/bigquery)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import (
	"context"
	"fmt"

	datatransfer "cloud.google.com/go/bigquery/datatransfer/apiv1"
	"cloud.google.com/go/bigquery/datatransfer/apiv1/datatransferpb"
)

// deleteScheduledQuery delete a scheduled query based on
// the config ID, stopping any future runs.
// transferConfigID follows the format:
//
//	`projects/{project_id}/locations/{location_id}/transferConfigs/{config_id}`
//	or `projects/{project_id}/transferConfigs/{config_id}`
func deleteScheduledQuery(transferConfigID string) error {
	// transferConfigID := "projects/{project_id}/transferConfigs/{config_id}"
	ctx := context.Background()
	dtc, err := datatransfer.NewClient(ctx)
	if err != nil {
		return fmt.Errorf("datatransfer.NewClient: %w", err)
	}
	defer dtc.Close()

	req := &datatransferpb.DeleteTransferConfigRequest{
		Name: transferConfigID,
	}
	err = dtc.DeleteTransferConfig(ctx, req)
	if err != nil {
		return fmt.Errorf("dtc.DeleteTransferConfig: %w", err)
	}

	return nil
}
```

### Java

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Java 設定說明操作。詳情請參閱 [BigQuery Java API 參考說明文件](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/overview?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import com.google.api.gax.rpc.ApiException;
import com.google.cloud.bigquery.datatransfer.v1.DataTransferServiceClient;
import com.google.cloud.bigquery.datatransfer.v1.DeleteTransferConfigRequest;
import java.io.IOException;

// Sample to delete a scheduled query
public class DeleteScheduledQuery {

  public static void main(String[] args) throws IOException {
    // TODO(developer): Replace these variables before running the sample.
    // i.e projects/{project_id}/transferConfigs/{config_id}` or
    // `projects/{project_id}/locations/{location_id}/transferConfigs/{config_id}`
    String name = "MY_CONFIG_ID";
    deleteScheduledQuery(name);
  }

  public static void deleteScheduledQuery(String name) throws IOException {
    try (DataTransferServiceClient dataTransferServiceClient = DataTransferServiceClient.create()) {
      DeleteTransferConfigRequest request =
          DeleteTransferConfigRequest.newBuilder().setName(name).build();
      dataTransferServiceClient.deleteTransferConfig(request);
      System.out.print("Scheduled query deleted successfully.\n");
    } catch (ApiException ex) {
      System.out.print("Scheduled query was not deleted." + ex.toString());
    }
  }
}
```

## 後續步驟

如要搜尋及篩選其他 Google Cloud 產品的程式碼範例，請參閱[Google Cloud 瀏覽器範例](https://docs.cloud.google.com/docs/samples?product=bigquerydatatransfer&hl=zh-tw)。

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。




[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],[],[],[]]