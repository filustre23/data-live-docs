Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [範例](https://docs.cloud.google.com/bigquery/docs/samples?hl=zh-tw)

# 授予檢視權限 透過集合功能整理內容 你可以依據偏好儲存及分類內容。

授權並授予檢視權限。

## 程式碼範例

### Go

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Go 設定說明操作。詳情請參閱 [BigQuery Go API 參考說明文件](https://godoc.org/cloud.google.com/go/bigquery)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import (
	"context"
	"fmt"

	"cloud.google.com/go/bigquery"
)

// updateViewDelegated demonstrates the setup of an authorized view, which allows access to a view's results
// without the caller having direct access to the underlying source data.
func updateViewDelegated(projectID, srcDatasetID, viewDatasetID, viewID string) error {
	// projectID := "my-project-id"
	// srcDatasetID := "sourcedata"
	// viewDatasetID := "views"
	// viewID := "myview"
	ctx := context.Background()
	client, err := bigquery.NewClient(ctx, projectID)
	if err != nil {
		return fmt.Errorf("bigquery.NewClient: %w", err)
	}
	defer client.Close()

	srcDataset := client.Dataset(srcDatasetID)
	viewDataset := client.Dataset(viewDatasetID)
	view := viewDataset.Table(viewID)

	// First, we'll add a group to the ACL for the dataset containing the view.  This will allow users within
	// that group to query the view, but they must have direct access to any tables referenced by the view.
	vMeta, err := viewDataset.Metadata(ctx)
	if err != nil {
		return err
	}
	vUpdateMeta := bigquery.DatasetMetadataToUpdate{
		Access: append(vMeta.Access, &bigquery.AccessEntry{
			Role:       bigquery.ReaderRole,
			EntityType: bigquery.GroupEmailEntity,
			Entity:     "example-analyst-group@google.com",
		}),
	}
	if _, err := viewDataset.Update(ctx, vUpdateMeta, vMeta.ETag); err != nil {
		return err
	}

	// Now, we'll authorize a specific view against a source dataset, delegating access enforcement.
	// Once this has been completed, members of the group previously added to the view dataset's ACL
	// no longer require access to the source dataset to successfully query the view.
	srcMeta, err := srcDataset.Metadata(ctx)
	if err != nil {
		return err
	}
	srcUpdateMeta := bigquery.DatasetMetadataToUpdate{
		Access: append(srcMeta.Access, &bigquery.AccessEntry{
			EntityType: bigquery.ViewEntity,
			View:       view,
		}),
	}
	if _, err := srcDataset.Update(ctx, srcUpdateMeta, srcMeta.ETag); err != nil {
		return err
	}
	return nil
}
```

### Java

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Java 設定說明操作。詳情請參閱 [BigQuery Java API 參考說明文件](https://docs.cloud.google.com/java/docs/reference/google-cloud-bigquery/latest/overview?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import com.google.cloud.bigquery.Acl;
import com.google.cloud.bigquery.BigQuery;
import com.google.cloud.bigquery.BigQueryException;
import com.google.cloud.bigquery.BigQueryOptions;
import com.google.cloud.bigquery.Dataset;
import com.google.cloud.bigquery.Table;
import java.util.ArrayList;
import java.util.List;

// Sample to grant view access on dataset
public class GrantViewAccess {

  public static void main(String[] args) {
    // TODO(developer): Replace these variables before running the sample.
    String srcDatasetId = "MY_DATASET_ID";
    String viewDatasetId = "MY_VIEW_DATASET_ID";
    String viewId = "MY_VIEW_ID";
    grantViewAccess(srcDatasetId, viewDatasetId, viewId);
  }

  public static void grantViewAccess(String srcDatasetId, String viewDatasetId, String viewId) {
    try {
      // Initialize client that will be used to send requests. This client only needs to be created
      // once, and can be reused for multiple requests.
      BigQuery bigquery = BigQueryOptions.getDefaultInstance().getService();

      Dataset srcDataset = bigquery.getDataset(srcDatasetId);
      Dataset viewDataset = bigquery.getDataset(viewDatasetId);
      Table view = viewDataset.get(viewId);
      // First, we'll add a group to the ACL for the dataset containing the view. This will allow
      // users within that group to query the view, but they must have direct access to any tables
      // referenced by the view.
      List<Acl> viewAcl = new ArrayList<>(viewDataset.getAcl());
      viewAcl.add(Acl.of(new Acl.Group("example-analyst-group@google.com"), Acl.Role.READER));
      viewDataset.toBuilder().setAcl(viewAcl).build().update();
      // Now, we'll authorize a specific view against a source dataset, delegating access
      // enforcement. Once this has been completed, members of the group previously added to the
      // view dataset's ACL no longer require access to the source dataset to successfully query the
      // view
      List<Acl> srcAcl = new ArrayList<>(srcDataset.getAcl());
      srcAcl.add(Acl.of(new Acl.View(view.getTableId())));
      srcDataset.toBuilder().setAcl(srcAcl).build().update();
      System.out.println("Grant view access successfully");
    } catch (BigQueryException e) {
      System.out.println("Grant view access was not success. \n" + e.toString());
    }
  }
}
```

### Python

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Python 設定說明操作。詳情請參閱 [BigQuery Python API 參考說明文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
from google.cloud import bigquery

client = bigquery.Client()

# To use a view, the analyst requires ACLs to both the view and the source
# table. Create an authorized view to allow an analyst to use a view
# without direct access permissions to the source table.
view_dataset_id = "my-project.my_view_dataset"
# Make an API request to get the view dataset ACLs.
view_dataset = client.get_dataset(view_dataset_id)

analyst_group_email = "example-analyst-group@google.com"
access_entries = view_dataset.access_entries
access_entries.append(
    bigquery.AccessEntry("READER", "groupByEmail", analyst_group_email)
)
view_dataset.access_entries = access_entries

# Make an API request to update the ACLs property of the view dataset.
view_dataset = client.update_dataset(view_dataset, ["access_entries"])
print(f"Access to view: {view_dataset.access_entries}")

# Group members of "data_analysts@example.com" now have access to the view,
# but they require access to the source table to use it. To remove this
# restriction, authorize the view to access the source dataset.
source_dataset_id = "my-project.my_source_dataset"
# Make an API request to set the source dataset ACLs.
source_dataset = client.get_dataset(source_dataset_id)

view_reference = {
    "projectId": "my-project",
    "datasetId": "my_view_dataset",
    "tableId": "my_authorized_view",
}
access_entries = source_dataset.access_entries
access_entries.append(bigquery.AccessEntry(None, "view", view_reference))
source_dataset.access_entries = access_entries

# Make an API request to update the ACLs property of the source dataset.
source_dataset = client.update_dataset(source_dataset, ["access_entries"])
print(f"Access to source: {source_dataset.access_entries}")
```

## 後續步驟

如要搜尋及篩選其他 Google Cloud 產品的程式碼範例，請參閱[Google Cloud 範例瀏覽工具](https://docs.cloud.google.com/docs/samples?product=bigquery&hl=zh-tw)。

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。




[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],[],[],[]]